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

    def emit(code, path, rec, message):
        errors.append({"stage":"semantic","code":code,"file":str(path),"record_id":rec.get("id"),"message":message})

    def resolve_many(rec, field, expected_types, path):
        expected_types = {expected_types} if isinstance(expected_types, str) else set(expected_types)
        value = rec.get(field, [])
        refs = value if isinstance(value, list) else ([value] if value else [])
        found = []
        for rid in refs:
            target = by_id.get(rid)
            if not target:
                emit("MISSING_REF", path, rec, f"{field}: {rid}")
                continue
            if target[1].get("record_type") not in expected_types:
                emit("WRONG_REF_TYPE", path, rec, f"{field}: {rid}")
                continue
            found.append(target[1])
        return found

    live_releases = {}
    for _, rec in records:
        if rec.get("record_type") == "release" and rec.get("release_state") == "LIVE" and rec.get("status") == "VERIFIED":
            live_releases.setdefault((rec.get("app_ref"), rec.get("platform")), []).append(rec)

    for path, rec in records:
        rtype = rec.get("record_type")

        if rtype in {"feature", "release", "store_destination", "data_practice", "locale_coverage"}:
            apps = resolve_many(rec, "app_ref", "app", path)
            if rtype == "release" and rec.get("release_state") == "LIVE":
                for app in apps:
                    if app.get("lifecycle") != "ACTIVE":
                        emit("LIVE_RELEASE_APP_INACTIVE", path, rec, app.get("id"))

        if rtype == "data_practice":
            resolve_many(rec, "processor_refs", "processor", path)

        elif rtype == "claim":
            resolve_many(rec, "app_ref", "app", path)
            features = resolve_many(rec, "feature_refs", "feature", path)
            evidence = resolve_many(rec, "evidence_refs", "evidence", path)
            locales = resolve_many(rec, "locale_coverage_refs", "locale_coverage", path)
            if rec.get("claim_mode") == "CURRENT":
                for feature in features:
                    if feature.get("feature_state") != "SHIPPED":
                        emit("CURRENT_CLAIM_NOT_SHIPPED", path, rec, feature.get("id"))
                for ev in evidence:
                    if ev.get("status") != "VERIFIED":
                        emit("EVIDENCE_NOT_VERIFIED", path, rec, ev.get("id"))
                for locale in locales:
                    if locale.get("app_ui") != "SUPPORTED":
                        emit("CURRENT_LOCALE_CLAIM_UNSUPPORTED", path, rec, locale.get("id"))

        elif rtype == "operational_surface":
            if rec.get("app_ref"):
                resolve_many(rec, "app_ref", "app", path)
            destinations = resolve_many(rec, "destination_ref", "store_destination", path) if rec.get("destination_ref") else []
            sources = resolve_many(rec, "source_refs", {"data_practice", "evidence"}, path)
            if rec.get("surface_kind") == "STORE_CTA":
                if not rec.get("destination_ref"):
                    emit("STORE_CTA_MISSING_DESTINATION", path, rec, "destination_ref")
                for dest in destinations:
                    if dest.get("availability_state") != "AVAILABLE":
                        emit("STORE_DESTINATION_UNAVAILABLE", path, rec, dest.get("id"))
                    key = (dest.get("app_ref"), dest.get("platform"))
                    if not live_releases.get(key):
                        emit("STORE_DESTINATION_NO_LIVE_RELEASE", path, rec, dest.get("id"))
            if rec.get("status") == "VERIFIED":
                for source in sources:
                    if source.get("status") != "VERIFIED":
                        emit("SURFACE_SOURCE_NOT_VERIFIED", path, rec, source.get("id"))
            if rec.get("severity") in {"P0", "P1"}:
                if rec.get("monitoring") in {None, "NONE"} or not rec.get("runbook_ref"):
                    emit("CRITICAL_SURFACE_UNCONTROLLED", path, rec, "monitoring/runbook_ref")

        elif rtype == "legal_trigger" and rec.get("applicability") == "APPLIES":
            refs = rec.get("required_surface_refs", [])
            if not refs:
                emit("LEGAL_TRIGGER_MISSING_SURFACE", path, rec, "required_surface_refs")
            surfaces = resolve_many(rec, "required_surface_refs", "operational_surface", path)
            for surface in surfaces:
                if surface.get("status") != "VERIFIED":
                    emit("LEGAL_SURFACE_NOT_VERIFIED", path, rec, surface.get("id"))

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
