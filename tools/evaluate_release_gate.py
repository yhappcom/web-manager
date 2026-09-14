#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


def stable_hash(value):
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
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


def with_fingerprint(issue):
    item = dict(issue)
    item["issue_fingerprint"] = stable_hash(normalize_issue(item))
    return item


def build_issues(case):
    issues = []

    for err in case.get("integrity_errors", []):
        issues.append(with_fingerprint({
            "code": err.get("code", "SEMANTIC_INTEGRITY_FAILURE"),
            "record_id": err.get("record_id"),
            "source_ref": err.get("source_ref"),
            "severity": "BLOCKING",
            "message": err.get("message", "semantic integrity failure"),
            "waivable": False,
        }))

    for cycle in case.get("cycles", []):
        issues.append(with_fingerprint({
            "code": "DEPENDENCY_CYCLE",
            "record_id": cycle[0] if cycle else None,
            "source_ref": None,
            "severity": "BLOCKING",
            "message": " -> ".join(cycle),
            "waivable": False,
        }))

    approval_errors = case.get("approval_errors", [])
    approval_blocking_records = {
        e.get("record_id")
        for e in approval_errors
        if e.get("severity", "BLOCKING") == "BLOCKING"
    }

    for record_id in case.get("blocking", []):
        if record_id in approval_blocking_records:
            continue
        issues.append(with_fingerprint({
            "code": "BLOCKING_DEPENDENCY_IMPACT",
            "record_id": record_id,
            "source_ref": None,
            "severity": "BLOCKING",
            "message": "typed dependency impact requires release resolution",
            "waivable": False,
        }))

    for record_id in case.get("review_required", []):
        issues.append(with_fingerprint({
            "code": "REVIEW_REQUIRED_DEPENDENCY_IMPACT",
            "record_id": record_id,
            "source_ref": None,
            "severity": "REVIEW_REQUIRED",
            "message": "typed dependency impact requires human review",
            "waivable": False,
        }))

    for err in approval_errors:
        issues.append(with_fingerprint({
            "code": err.get("code", "APPROVAL_STALE"),
            "record_id": err.get("record_id"),
            "source_ref": err.get("source_ref"),
            "severity": err.get("severity", "BLOCKING"),
            "message": err.get("message", "approval binding is not current"),
            "waivable": bool(err.get("waivable", False)),
        }))

    for failure in case.get("control_failures", []):
        issues.append(with_fingerprint({
            "code": failure.get("code", "REQUIRED_CONTROL_FAILURE"),
            "record_id": failure.get("record_id"),
            "source_ref": failure.get("source_ref"),
            "severity": failure.get("severity", "BLOCKING"),
            "message": failure.get("message", "required release control failed"),
            "waivable": bool(failure.get("waivable", False)),
        }))

    return issues


def validate_waiver(waiver, issue_by_fp, release_ref, evaluation_date):
    fp = waiver.get("issue_fingerprint")
    issue = issue_by_fp.get(fp)
    if not issue:
        return False, "ISSUE_FINGERPRINT_MISMATCH", None
    if not issue.get("waivable"):
        return False, "ISSUE_NON_WAIVABLE", issue
    if waiver.get("release_ref") != release_ref:
        return False, "WAIVER_WRONG_RELEASE", issue
    if waiver.get("status") != "APPROVED":
        return False, "WAIVER_NOT_APPROVED", issue
    if not waiver.get("approved_by") or not waiver.get("reason"):
        return False, "WAIVER_MISSING_AUDIT_FIELDS", issue
    expires_on = waiver.get("expires_on")
    if not expires_on:
        return False, "WAIVER_MISSING_EXPIRY", issue
    try:
        if date.fromisoformat(expires_on) < evaluation_date:
            return False, "WAIVER_EXPIRED", issue
    except ValueError:
        return False, "WAIVER_BAD_EXPIRY", issue
    return True, None, issue


def evaluate_release(case):
    release_ref = case["release_ref"]
    evaluation_date = date.fromisoformat(case.get("evaluation_date", "2026-09-14"))
    issues = build_issues(case)
    issue_by_fp = {item["issue_fingerprint"]: item for item in issues}

    waived = {}
    invalid_waivers = []
    for waiver in case.get("waivers", []):
        ok, reason, issue = validate_waiver(
            waiver, issue_by_fp, release_ref, evaluation_date
        )
        if ok:
            waived[issue["issue_fingerprint"]] = {
                "issue_fingerprint": issue["issue_fingerprint"],
                "waiver_id": waiver.get("id"),
                "approved_by": waiver.get("approved_by"),
                "reason": waiver.get("reason"),
                "expires_on": waiver.get("expires_on"),
            }
        else:
            invalid_waivers.append({
                "waiver_id": waiver.get("id"),
                "reason": reason,
                "issue_fingerprint": waiver.get("issue_fingerprint"),
            })

    unresolved = [
        item for item in issues if item["issue_fingerprint"] not in waived
    ]
    blocking = [item for item in unresolved if item["severity"] == "BLOCKING"]
    review = [
        item for item in unresolved if item["severity"] == "REVIEW_REQUIRED"
    ]

    if blocking:
        decision = "BLOCKED"
    elif review:
        decision = "NEEDS_REVIEW"
    else:
        decision = "PASS"

    pass_mode = None
    if decision == "PASS":
        pass_mode = "WITH_WAIVER" if waived else "CLEAN"

    manifest_core = {
        "release_ref": release_ref,
        "decision": decision,
        "pass_mode": pass_mode,
        "canonical_issues": issues,
        "unresolved_issues": unresolved,
        "waivers_applied": list(waived.values()),
        "invalid_waivers": invalid_waivers,
        "informational_records": sorted(case.get("informational", [])),
    }
    return {
        **manifest_core,
        "manifest_fingerprint": stable_hash(manifest_core),
    }


def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report = evaluate_release(case)
        expected = case["expected"]
        observed = {}
        passed = True
        for key, value in expected.items():
            if key == "canonical_issue_codes":
                actual = [item["code"] for item in report["canonical_issues"]]
            elif key == "unresolved_issue_codes":
                actual = [item["code"] for item in report["unresolved_issues"]]
            elif key == "waiver_count":
                actual = len(report["waivers_applied"])
            elif key == "invalid_waiver_reasons":
                actual = [item["reason"] for item in report["invalid_waivers"]]
            else:
                actual = report.get(key)
            observed[key] = actual
            if actual != value:
                passed = False
        results.append({
            "name": case["name"],
            "passed": passed,
            "expected": expected,
            "observed": observed,
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
    ap.add_argument("--case-file")
    ap.add_argument("--run-tests")
    args = ap.parse_args()
    if args.run_tests:
        raise SystemExit(run_tests(args.run_tests))
    if args.case_file:
        case = json.loads(Path(args.case_file).read_text(encoding="utf-8"))
        print(json.dumps(evaluate_release(case), ensure_ascii=False, indent=2))
        return
    ap.error("--case-file <path> or --run-tests <path> is required")


if __name__ == "__main__":
    main()
