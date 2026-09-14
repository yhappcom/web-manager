#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

NON_SEMANTIC_FIELDS = {
    "updated_at",
    "verified_at",
    "last_checked_at",
    "last_verified_at",
    "generated_at",
    "notes",
    "semantic_fingerprint",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_record_map(root: Path):
    records = {}
    for path in sorted(root.rglob("*.json")):
        rec = load_json(path)
        rid = rec.get("id")
        if not rid:
            raise ValueError(f"record without id: {path}")
        if rid in records:
            raise ValueError(f"duplicate id: {rid}")
        records[rid] = rec
    return records


def semantic_projection(value):
    if isinstance(value, dict):
        return {
            key: semantic_projection(child)
            for key, child in value.items()
            if key not in NON_SEMANTIC_FIELDS
        }
    if isinstance(value, list):
        return [semantic_projection(child) for child in value]
    return value


def canonical_bytes(value):
    # PRACTICE implementation: deterministic UTF-8 JSON for the current constrained
    # corpus. Production JCS compatibility still requires RFC 8785 conformance vectors,
    # especially ECMAScript number serialization and UTF-16 property ordering.
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_fingerprint(record):
    digest = hashlib.sha256(canonical_bytes(semantic_projection(record))).hexdigest()
    return f"sha256:{digest}"


def reference_ids(record):
    refs = set()
    for key, value in record.items():
        if key == "depends_on" or key.endswith("_refs"):
            if isinstance(value, list):
                refs.update(item for item in value if isinstance(item, str))
        elif key.endswith("_ref") and isinstance(value, str):
            refs.add(value)
    return refs


def downstream_graph(record_map):
    known = set(record_map)
    graph = defaultdict(set)
    for rid, rec in record_map.items():
        for upstream in reference_ids(rec):
            if upstream in known:
                graph[upstream].add(rid)
    return graph


def compare_record_maps(before, after):
    before_fp = {rid: semantic_fingerprint(rec) for rid, rec in before.items()}
    after_fp = {rid: semantic_fingerprint(rec) for rid, rec in after.items()}

    before_ids = set(before)
    after_ids = set(after)
    common = before_ids & after_ids

    added = sorted(after_ids - before_ids)
    removed = sorted(before_ids - after_ids)
    modified = sorted(rid for rid in common if before_fp[rid] != after_fp[rid])
    unchanged = sorted(rid for rid in common if before_fp[rid] == after_fp[rid])
    changed = set(added) | set(removed) | set(modified)

    graph = downstream_graph(after)
    old_graph = downstream_graph(before)
    for upstream, dependents in old_graph.items():
        graph[upstream].update(dependents)

    direct = set()
    impacted = set()
    queue = deque()

    for rid in changed:
        for dependent in graph.get(rid, ()):
            if dependent not in changed:
                direct.add(dependent)
                impacted.add(dependent)
                queue.append(dependent)

    while queue:
        rid = queue.popleft()
        for dependent in graph.get(rid, ()):
            if dependent not in changed and dependent not in impacted:
                impacted.add(dependent)
                queue.append(dependent)

    transitive = impacted - direct

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
        "direct_impact": sorted(direct),
        "transitive_impact": sorted(transitive),
        "review_set": sorted(changed | impacted),
        "before_fingerprints": before_fp,
        "after_fingerprints": after_fp,
    }


def map_from_records(records):
    result = {}
    for rec in records:
        rid = rec["id"]
        if rid in result:
            raise ValueError(f"duplicate id in test fixture: {rid}")
        result[rid] = rec
    return result


def run_tests(root: Path):
    cases = load_json(root / "control" / "tests" / "impact_cases.json")
    results = []
    for case in cases:
        report = compare_record_maps(
            map_from_records(case["before_records"]),
            map_from_records(case["after_records"]),
        )
        expected = case["expected"]
        matched = all(report.get(key) == value for key, value in expected.items())
        results.append({
            "name": case["name"],
            "passed": matched,
            "expected": expected,
            "observed": {key: report.get(key) for key in expected},
        })

    ok = all(item["passed"] for item in results)
    print(json.dumps({
        "ok": ok,
        "passed": sum(item["passed"] for item in results),
        "total": len(results),
        "results": results,
    }, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--before")
    ap.add_argument("--after")
    ap.add_argument("--run-tests", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()

    if args.run_tests:
        raise SystemExit(run_tests(root))

    if not args.before or not args.after:
        ap.error("--before and --after are required unless --run-tests is used")

    report = compare_record_maps(
        load_record_map(Path(args.before)),
        load_record_map(Path(args.after)),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
