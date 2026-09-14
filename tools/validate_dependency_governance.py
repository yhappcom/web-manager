#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

NON_SEMANTIC_FIELDS = {
    "updated_at", "verified_at", "last_checked_at", "last_verified_at",
    "generated_at", "notes", "semantic_fingerprint",
}
IMPACT_STRENGTH = {"INFORMATIONAL": 0, "REVIEW_REQUIRED": 1, "BLOCKING": 2}


def semantic_projection(value):
    if isinstance(value, dict):
        return {k: semantic_projection(v) for k, v in value.items() if k not in NON_SEMANTIC_FIELDS}
    if isinstance(value, list):
        return [semantic_projection(v) for v in value]
    return value


def semantic_fingerprint(record):
    raw = json.dumps(
        semantic_projection(record),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def record_map(records):
    result = {}
    for rec in records:
        rid = rec["id"]
        if rid in result:
            raise ValueError(f"duplicate id: {rid}")
        result[rid] = rec
    return result


def typed_dependencies(record):
    result = {}
    for dep in record.get("dependencies", []):
        ref = dep.get("ref")
        impact = dep.get("impact", "REVIEW_REQUIRED")
        if ref and impact in IMPACT_STRENGTH:
            current = result.get(ref)
            if current is None or IMPACT_STRENGTH[impact] > IMPACT_STRENGTH[current]:
                result[ref] = impact

    for key, value in record.items():
        if key in {"dependencies", "approval_bindings"}:
            continue
        refs = []
        if key == "depends_on" or key.endswith("_refs"):
            if isinstance(value, list):
                refs = [item for item in value if isinstance(item, str)]
        elif key.endswith("_ref") and isinstance(value, str):
            refs = [value]
        for ref in refs:
            result.setdefault(ref, "REVIEW_REQUIRED")
    return result


def detect_cycles(records):
    deps = {
        rid: [ref for ref in typed_dependencies(rec) if ref in records]
        for rid, rec in records.items()
    }
    state = {}
    stack = []
    seen = set()
    found = []

    def canonical_cycle(core):
        rotations = [tuple(core[i:] + core[:i]) for i in range(len(core))]
        reverse = list(reversed(core))
        rotations += [tuple(reverse[i:] + reverse[:i]) for i in range(len(reverse))]
        return min(rotations)

    def visit(node):
        state[node] = 1
        stack.append(node)
        for upstream in deps[node]:
            if state.get(upstream, 0) == 0:
                visit(upstream)
            elif state.get(upstream) == 1:
                start = stack.index(upstream)
                key = canonical_cycle(stack[start:].copy())
                if key not in seen:
                    seen.add(key)
                    found.append(list(key) + [key[0]])
        stack.pop()
        state[node] = 2

    for rid in sorted(records):
        if state.get(rid, 0) == 0:
            visit(rid)
    return sorted(found)


def approval_errors(records):
    fingerprints = {rid: semantic_fingerprint(rec) for rid, rec in records.items()}
    errors = []
    for rid, rec in records.items():
        for binding in rec.get("approval_bindings", []):
            source_ref = binding.get("ref")
            severity = binding.get("impact", "BLOCKING")
            if source_ref not in records:
                errors.append({
                    "record_id": rid,
                    "code": "APPROVAL_SOURCE_MISSING",
                    "source_ref": source_ref,
                    "severity": severity,
                })
                continue
            if binding.get("verified_against") != fingerprints[source_ref]:
                errors.append({
                    "record_id": rid,
                    "code": "APPROVAL_STALE",
                    "source_ref": source_ref,
                    "severity": severity,
                    "verified_against": binding.get("verified_against"),
                    "current_fingerprint": fingerprints[source_ref],
                })
    return errors


def combined_graph(before, after):
    graph = defaultdict(dict)
    for records in (before, after):
        for dependent, rec in records.items():
            for upstream, impact in typed_dependencies(rec).items():
                if upstream not in records:
                    continue
                current = graph[upstream].get(dependent)
                if current is None or IMPACT_STRENGTH[impact] > IMPACT_STRENGTH[current]:
                    graph[upstream][dependent] = impact
    return graph


def compare(before, after):
    before_fp = {rid: semantic_fingerprint(rec) for rid, rec in before.items()}
    after_fp = {rid: semantic_fingerprint(rec) for rid, rec in after.items()}
    common = set(before) & set(after)
    changed = (
        (set(before) ^ set(after))
        | {rid for rid in common if before_fp[rid] != after_fp[rid]}
    )

    graph = combined_graph(before, after)
    effects = {}
    queue = deque((rid, None) for rid in changed)

    while queue:
        upstream, inherited = queue.popleft()
        for dependent, edge_impact in graph.get(upstream, {}).items():
            if dependent in changed:
                continue
            path_impact = edge_impact if inherited is None else min(
                (inherited, edge_impact), key=lambda item: IMPACT_STRENGTH[item]
            )
            current = effects.get(dependent)
            if current is None or IMPACT_STRENGTH[path_impact] > IMPACT_STRENGTH[current]:
                effects[dependent] = path_impact
                queue.append((dependent, path_impact))

    return {
        "changed": sorted(changed),
        "informational": sorted(rid for rid, level in effects.items() if level == "INFORMATIONAL"),
        "review_required": sorted(rid for rid, level in effects.items() if level == "REVIEW_REQUIRED"),
        "blocking": sorted(rid for rid, level in effects.items() if level == "BLOCKING"),
        "cycles_before": detect_cycles(before),
        "cycles_after": detect_cycles(after),
        "approval_errors_after": approval_errors(after),
    }


def run_tests(path: Path):
    cases = json.loads(path.read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report = compare(record_map(case["before_records"]), record_map(case["after_records"]))
        expected = case["expected"]
        passed = all(report.get(key) == value for key, value in expected.items())
        results.append({
            "name": case["name"],
            "passed": passed,
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
    ap.add_argument("--run-tests")
    args = ap.parse_args()
    if args.run_tests:
        raise SystemExit(run_tests(Path(args.run_tests)))
    ap.error("--run-tests <path> is required for this PRACTICE tool")


if __name__ == "__main__":
    main()
