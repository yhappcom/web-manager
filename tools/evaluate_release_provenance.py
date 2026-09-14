#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

EVALUATOR_NAME = "minttap-release-provenance-gate"
EVALUATOR_VERSION = "0.1.0"


def stable_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def issue_fingerprint(issue):
    return stable_hash({
        "code": issue["code"], "record_id": issue.get("record_id"),
        "source_ref": issue.get("source_ref"), "severity": issue["severity"],
        "message": issue.get("message"), "waivable": bool(issue.get("waivable", False)),
    })


def build_issue(raw):
    item = dict(raw)
    item["issue_fingerprint"] = issue_fingerprint(item)
    return item


def reviewer_allowed(policy, reviewer, issue_code):
    for rule in policy.get("reviewers", []):
        if rule.get("identity") != reviewer:
            continue
        allowed = rule.get("allowed_issue_codes", [])
        if "*" in allowed or issue_code in allowed:
            return True, rule.get("role")
    return False, None


def waiver_validation(waiver, issue, case):
    if not issue:
        return False, "ISSUE_FINGERPRINT_MISMATCH"
    if not issue.get("waivable", False):
        return False, "ISSUE_NON_WAIVABLE"
    if waiver.get("release_ref") != case["release_ref"]:
        return False, "WAIVER_WRONG_RELEASE"
    if waiver.get("status") != "APPROVED":
        return False, "WAIVER_NOT_APPROVED"
    if waiver.get("source_commit") != case["source_commit"]:
        return False, "WAIVER_STALE_SOURCE_COMMIT"
    if waiver.get("source_snapshot_digest") != case["source_snapshot_digest"]:
        return False, "WAIVER_STALE_SOURCE_SNAPSHOT"
    if waiver.get("policy_version") != case["reviewer_policy"]["version"]:
        return False, "WAIVER_STALE_POLICY"
    if not waiver.get("approved_by") or not waiver.get("reason"):
        return False, "WAIVER_MISSING_AUDIT_FIELDS"
    if case.get("release_author") and waiver.get("approved_by") == case["release_author"]:
        return False, "WAIVER_SELF_APPROVAL_FORBIDDEN"
    authorized, role = reviewer_allowed(case["reviewer_policy"], waiver.get("approved_by"), issue["code"])
    if not authorized:
        return False, "WAIVER_REVIEWER_UNAUTHORIZED"
    expires_on = waiver.get("expires_on")
    if not expires_on:
        return False, "WAIVER_MISSING_EXPIRY"
    try:
        if date.fromisoformat(expires_on) < date.fromisoformat(case["evaluation_date"]):
            return False, "WAIVER_EXPIRED"
    except ValueError:
        return False, "WAIVER_BAD_EXPIRY"
    return True, role


def evaluate(case):
    issues = [build_issue(item) for item in case.get("canonical_issues", [])]
    issue_by_fp = {i["issue_fingerprint"]: i for i in issues}
    applied, invalid, waived_fps = [], [], set()

    for waiver in case.get("waivers", []):
        issue = issue_by_fp.get(waiver.get("issue_fingerprint"))
        ok, detail = waiver_validation(waiver, issue, case)
        if ok:
            waived_fps.add(issue["issue_fingerprint"])
            applied.append({
                "waiver_id": waiver.get("id"), "issue_fingerprint": issue["issue_fingerprint"],
                "approved_by": waiver.get("approved_by"), "reviewer_role": detail,
                "reason": waiver.get("reason"), "expires_on": waiver.get("expires_on"),
                "source_commit": waiver.get("source_commit"),
                "source_snapshot_digest": waiver.get("source_snapshot_digest"),
                "policy_version": waiver.get("policy_version"),
            })
        else:
            invalid.append({
                "waiver_id": waiver.get("id"),
                "issue_fingerprint": waiver.get("issue_fingerprint"), "reason": detail,
            })

    unresolved = [i for i in issues if i["issue_fingerprint"] not in waived_fps]
    blockers = [i for i in unresolved if i["severity"] == "BLOCKING"]
    review = [i for i in unresolved if i["severity"] == "REVIEW_REQUIRED"]
    decision = "BLOCKED" if blockers else "NEEDS_REVIEW" if review else "PASS"
    pass_mode = ("WITH_WAIVER" if applied else "CLEAN") if decision == "PASS" else None

    input_binding = {
        "release_ref": case["release_ref"], "source_commit": case["source_commit"],
        "source_snapshot_digest": case["source_snapshot_digest"],
        "policy_version": case["reviewer_policy"]["version"],
        "evaluator_name": EVALUATOR_NAME, "evaluator_version": EVALUATOR_VERSION,
        "canonical_issue_fingerprints": [i["issue_fingerprint"] for i in issues],
        "waiver_ids": [w.get("id") for w in case.get("waivers", [])],
    }
    input_digest = stable_hash(input_binding)

    attestation_errors = []
    attestation = case.get("manifest_attestation")
    if attestation:
        expected = {
            "release_ref": case["release_ref"], "source_commit": case["source_commit"],
            "source_snapshot_digest": case["source_snapshot_digest"],
            "policy_version": case["reviewer_policy"]["version"],
            "evaluator_name": EVALUATOR_NAME, "evaluator_version": EVALUATOR_VERSION,
            "input_digest": input_digest,
        }
        for field, value in expected.items():
            if attestation.get(field) != value:
                attestation_errors.append("ATTESTATION_" + field.upper() + "_MISMATCH")

    ci_state = "ALLOW"
    if decision != "PASS" or invalid or attestation_errors:
        ci_state = "FAIL"

    core = {
        "release_ref": case["release_ref"], "source_commit": case["source_commit"],
        "source_snapshot_digest": case["source_snapshot_digest"],
        "decision": decision, "pass_mode": pass_mode,
        "canonical_issues": issues, "unresolved_issues": unresolved,
        "waivers_applied": applied, "invalid_waivers": invalid,
        "provenance": {
            "policy_version": case["reviewer_policy"]["version"],
            "evaluator_name": EVALUATOR_NAME, "evaluator_version": EVALUATOR_VERSION,
            "input_digest": input_digest,
        },
        "attestation_errors": attestation_errors, "ci_state": ci_state,
    }
    return {**core, "manifest_fingerprint": stable_hash(core)}


def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report, expected = evaluate(case), case["expected"]
        observed, passed = {}, True
        for key, value in expected.items():
            if key == "invalid_waiver_reasons":
                actual = [x["reason"] for x in report["invalid_waivers"]]
            elif key == "waiver_count":
                actual = len(report["waivers_applied"])
            elif key == "attestation_errors":
                actual = report["attestation_errors"]
            elif key == "unresolved_issue_codes":
                actual = [x["code"] for x in report["unresolved_issues"]]
            else:
                actual = report.get(key)
            observed[key] = actual
            if actual != value:
                passed = False
        results.append({"name": case["name"], "passed": passed, "expected": expected, "observed": observed})
    ok = all(x["passed"] for x in results)
    print(json.dumps({"ok": ok, "passed": sum(x["passed"] for x in results), "total": len(results), "results": results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-tests")
    ap.add_argument("--case-file")
    args = ap.parse_args()
    if args.run_tests:
        raise SystemExit(run_tests(args.run_tests))
    if args.case_file:
        result = evaluate(json.loads(Path(args.case_file).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result["ci_state"] == "ALLOW" else 1)
    ap.error("--run-tests <path> or --case-file <path> required")


if __name__ == "__main__":
    main()
