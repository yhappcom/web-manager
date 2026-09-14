#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


def stable_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def normalize_issue(issue):
    return {
        "code": issue["code"],
        "record_id": issue.get("record_id"),
        "source_ref": issue.get("source_ref"),
        "severity": issue["severity"],
        "message": issue.get("message"),
        "waivable": bool(issue.get("waivable", False)),
    }


def issue_with_fingerprint(issue):
    item = dict(issue)
    item["issue_fingerprint"] = stable_hash(normalize_issue(item))
    return item


def validate_waiver(waiver, issue, reviewers, release_ref, source_snapshot, tool_version, evaluation_date):
    if waiver.get("issue_fingerprint") != issue["issue_fingerprint"]:
        return "ISSUE_FINGERPRINT_MISMATCH"
    if waiver.get("release_ref") != release_ref:
        return "WAIVER_WRONG_RELEASE"
    if waiver.get("source_snapshot") != source_snapshot:
        return "WAIVER_STALE_SOURCE_SNAPSHOT"
    if waiver.get("tool_version") != tool_version:
        return "WAIVER_STALE_TOOL_VERSION"
    reviewer = reviewers.get(waiver.get("approved_by"))
    if not reviewer or not reviewer.get("active") or "WAIVE" not in reviewer.get("permissions", []):
        return "REVIEWER_UNAUTHORIZED"
    if issue["code"] not in reviewer.get("allowed_issue_codes", []):
        return "ISSUE_CLASS_NOT_AUTHORIZED"
    if waiver.get("requested_by") == waiver.get("approved_by"):
        return "SEPARATION_OF_DUTIES_VIOLATION"
    if waiver.get("status") != "APPROVED":
        return "WAIVER_NOT_APPROVED"
    if not waiver.get("reason"):
        return "WAIVER_MISSING_REASON"
    expires_on = waiver.get("expires_on")
    if not expires_on:
        return "WAIVER_MISSING_EXPIRY"
    try:
        if date.fromisoformat(expires_on) < evaluation_date:
            return "WAIVER_EXPIRED"
    except ValueError:
        return "WAIVER_BAD_EXPIRY"
    return None


def evaluate(case):
    release_ref = case["release_ref"]
    source_snapshot = case["current_source_snapshot"]
    tool_version = case["current_tool_version"]
    evaluation_date = date.fromisoformat(case.get("evaluation_date", "2026-09-14"))
    reviewers = {item["id"]: item for item in case.get("reviewers", [])}

    issues = [issue_with_fingerprint(item) for item in case.get("issues", [])]
    issue_by_fp = {item["issue_fingerprint"]: item for item in issues}
    applied = []
    invalid = []

    for waiver in case.get("waivers", []):
        issue = issue_by_fp.get(waiver.get("issue_fingerprint"))
        if issue is None:
            invalid.append({"waiver_id": waiver.get("id"), "reason": "ISSUE_FINGERPRINT_MISMATCH"})
            continue
        reason = validate_waiver(
            waiver, issue, reviewers, release_ref, source_snapshot, tool_version, evaluation_date
        )
        if reason:
            invalid.append({"waiver_id": waiver.get("id"), "reason": reason})
        else:
            applied.append({
                "waiver_id": waiver.get("id"),
                "issue_fingerprint": issue["issue_fingerprint"],
                "approved_by": waiver.get("approved_by"),
                "source_snapshot": source_snapshot,
                "tool_version": tool_version,
            })

    attestation_errors = []
    attestation = case.get("manifest_attestation")
    if attestation:
        if attestation.get("release_ref") != release_ref:
            attestation_errors.append("MANIFEST_WRONG_RELEASE")
        if attestation.get("source_snapshot") != source_snapshot:
            attestation_errors.append("MANIFEST_STALE_SOURCE_SNAPSHOT")
        if attestation.get("tool_version") != tool_version:
            attestation_errors.append("MANIFEST_STALE_TOOL_VERSION")

    waived = {item["issue_fingerprint"] for item in applied}
    unresolved = [item for item in issues if item["issue_fingerprint"] not in waived]

    if invalid or attestation_errors or any(item["severity"] == "BLOCKING" for item in unresolved):
        decision = "BLOCKED"
    elif case.get("review_required", False) or any(item["severity"] == "REVIEW_REQUIRED" for item in unresolved):
        decision = "NEEDS_REVIEW"
    else:
        decision = "PASS"

    pass_mode = None
    if decision == "PASS":
        pass_mode = "WITH_WAIVER" if applied else "CLEAN"

    manifest_core = {
        "release_ref": release_ref,
        "source_snapshot": source_snapshot,
        "tool_version": tool_version,
        "decision": decision,
        "pass_mode": pass_mode,
        "canonical_issues": issues,
        "waivers_applied": applied,
        "invalid_waivers": invalid,
        "attestation_errors": attestation_errors,
        "unresolved_issues": unresolved,
    }
    ci_status = "PASS" if decision == "PASS" else "FAIL"
    return {
        **manifest_core,
        "ci_status": ci_status,
        "manifest_fingerprint": stable_hash(manifest_core),
    }


def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report = evaluate(case)
        expected = case["expected"]
        observed = {}
        passed = True
        for key, value in expected.items():
            if key == "invalid_waiver_reasons":
                actual = [item["reason"] for item in report["invalid_waivers"]]
            elif key == "attestation_errors":
                actual = report["attestation_errors"]
            elif key == "waiver_count":
                actual = len(report["waivers_applied"])
            else:
                actual = report.get(key)
            observed[key] = actual
            if actual != value:
                passed = False
        results.append({"name": case["name"], "passed": passed, "expected": expected, "observed": observed})
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
    ap.add_argument("--case-file")
    ap.add_argument("--run-tests")
    args = ap.parse_args()
    if args.run_tests:
        raise SystemExit(run_tests(args.run_tests))
    if args.case_file:
        case = json.loads(Path(args.case_file).read_text(encoding="utf-8"))
        report = evaluate(case)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(0 if report["ci_status"] == "PASS" else 1)
    ap.error("--case-file <path> or --run-tests <path> is required")


if __name__ == "__main__":
    main()
