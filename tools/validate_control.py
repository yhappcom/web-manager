#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_records(root: Path):
    return [(p, load_json(p)) for p in sorted(root.rglob("*.json"))]


def schema_errors(schema, records):
    validator = Draft202012Validator(schema)
    errors = []
    for path, rec in records:
        for e in validator.iter_errors(rec):
            errors.append({
                "stage": "schema",
                "code": "SCHEMA_INVALID",
                "file": str(path),
                "record_id": rec.get("id"),
                "message": e.message,
            })
    return errors


def semantic_errors(records):
    errors = []
    by_id = {}
    for path, rec in records:
        rid = rec.get("id")
        if rid in by_id:
            errors.append({"stage":"semantic","code":"DUPLICATE_ID","file":str(path),"record_id":rid,"message":rid})
        else:
            by_id[rid] = (path, rec)

    def resolve_many(rec, field, expected_type, path):
        found = []
        for rid in rec.get(field, []):
            target = by_id.get(rid)
            if not target:
                errors.append({"stage":"semantic","code":"MISSING_REF","file":str(path),"record_id":rec.get("id"),"message":f"{field}: {rid}"})
                continue
            if target[1].get("record_type") != expected_type:
                errors.append({"stage":"semantic","code":"WRONG_REF_TYPE","file":str(path),"record_id":rec.get("id"),"message":f"{field}: {rid}"})
                continue
            found.append(target[1])
        return found

    for path, rec in records:
        rtype = rec.get("record_type")
        if rtype == "feature":
            app = by_id.get(rec.get("app_ref"))
            if not app:
                errors.append({"stage":"semantic","code":"MISSING_REF","file":str(path),"record_id":rec.get("id"),"message":f"app_ref: {rec.get('app_ref')}"})
            elif app[1].get("record_type") != "app":
                errors.append({"stage":"semantic","code":"WRONG_REF_TYPE","file":str(path),"record_id":rec.get("id"),"message":"app_ref"})
        elif rtype == "claim":
            app = by_id.get(rec.get("app_ref"))
            if not app:
                errors.append({"stage":"semantic","code":"MISSING_REF","file":str(path),"record_id":rec.get("id"),"message":f"app_ref: {rec.get('app_ref')}"})
            features = resolve_many(rec, "feature_refs", "feature", path)
            evidence = resolve_many(rec, "evidence_refs", "evidence", path)
            if rec.get("claim_mode") == "CURRENT":
                for feature in features:
                    if feature.get("feature_state") != "SHIPPED":
                        errors.append({"stage":"semantic","code":"CURRENT_CLAIM_NOT_SHIPPED","file":str(path),"record_id":rec.get("id"),"message":feature.get("id")})
            for ev in evidence:
                if ev.get("status") != "VERIFIED":
                    errors.append({"stage":"semantic","code":"EVIDENCE_NOT_VERIFIED","file":str(path),"record_id":rec.get("id"),"message":ev.get("id")})
    return errors


def validate_records(schema, records):
    errors = schema_errors(schema, records)
    if errors:
        return errors
    return semantic_errors(records)


def baseline(root: Path):
    return load_records(root / "control" / "records")


def run_tests(root: Path):
    schema = load_json(root / "control" / "schemas" / "v1" / "record.schema.json")
    base_records = baseline(root)
    base_errors = validate_records(schema, base_records)
    results = [{
        "name": "valid-baseline",
        "passed": not base_errors,
        "expected": "PASS",
        "observed_codes": [e["code"] for e in base_errors],
    }]
    cases = load_json(root / "control" / "tests" / "cases.json")
    for case in cases:
        records = list(base_records)
        for j, rec in enumerate(case.get("additional_records", [])):
            records.append((Path(f"<case:{case['name']}:additional:{j}>"), rec))
        records.append((Path(f"<case:{case['name']}:record>"), case["record"]))
        errors = validate_records(schema, records)
        matched = any(e["stage"] == case["expected_stage"] and e["code"] == case["expected_code"] for e in errors)
        results.append({
            "name": case["name"],
            "passed": matched,
            "expected": f"{case['expected_stage']}:{case['expected_code']}",
            "observed_codes": [f"{e['stage']}:{e['code']}" for e in errors],
        })
    ok = all(r["passed"] for r in results)
    print(json.dumps({"ok":ok,"passed":sum(r["passed"] for r in results),"total":len(results),"results":results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--run-tests", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    if args.run_tests:
        raise SystemExit(run_tests(root))
    schema = load_json(root / "control" / "schemas" / "v1" / "record.schema.json")
    errors = validate_records(schema, baseline(root))
    print(json.dumps({"ok":not errors,"errors":errors}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
