#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def evaluate(case):
    policy = case["policy"]
    reviewers = {item["id"]: item for item in case.get("reviewers", [])}
    errors = []

    policy_change = case.get("policy_change")
    if policy_change and policy_change.get("changed"):
        approved = set(policy_change.get("approved_by", []))
        owners = set(policy.get("policy_owners", []))
        if not (approved & owners):
            errors.append("POLICY_OWNER_APPROVAL_MISSING")

    workflow = case.get("workflow", {})
    event = workflow.get("event")
    untrusted = bool(workflow.get("checkout_untrusted", False))
    privileged = any([
        workflow.get("token_write", False),
        workflow.get("secrets_available", False),
        workflow.get("deployment_authority", False),
    ])
    if event in {"pull_request_target", "workflow_run"} and untrusted and privileged:
        errors.append("UNTRUSTED_CODE_IN_PRIVILEGED_WORKFLOW")
    if workflow.get("self_hosted", False) and untrusted:
        errors.append("UNTRUSTED_CODE_ON_SELF_HOSTED_RUNNER")

    unresolved = []
    release_author = case.get("release_author")
    for issue in case.get("issues", []):
        code = issue["code"]
        rule = policy.get("issue_rules", {}).get(code, {})
        quorum = int(rule.get("quorum", 1))
        eligible = set()
        for reviewer_id in issue.get("approvals", []):
            reviewer = reviewers.get(reviewer_id)
            if not reviewer or not reviewer.get("active", False):
                continue
            if code not in reviewer.get("allowed_issue_codes", []):
                continue
            if reviewer_id == release_author:
                continue
            eligible.add(reviewer_id)
        if len(eligible) < quorum:
            unresolved.append(code)

    emergency_mode = False
    break_glass = case.get("break_glass")
    if unresolved and break_glass:
        reviewer = reviewers.get(break_glass.get("actor"))
        try:
            not_expired = date.fromisoformat(break_glass.get("expires_on", "1900-01-01")) >= date.fromisoformat(case.get("evaluation_date", "2026-09-14"))
        except ValueError:
            not_expired = False
        issue_allowed = all(code in policy.get("break_glass_issue_codes", []) for code in unresolved)
        valid = all([
            break_glass.get("status") == "APPROVED",
            reviewer is not None,
            bool(reviewer and reviewer.get("active", False)),
            bool(reviewer and "BREAK_GLASS" in reviewer.get("permissions", [])),
            break_glass.get("actor") != release_author,
            bool(break_glass.get("reason")),
            bool(break_glass.get("incident_ref")),
            not_expired,
            issue_allowed,
        ])
        if valid:
            emergency_mode = True
            unresolved = []
        else:
            errors.append("BREAK_GLASS_INVALID")

    decision = "BLOCKED" if errors or unresolved else "PASS"
    pass_mode = None
    if decision == "PASS":
        pass_mode = "WITH_BREAK_GLASS" if emergency_mode else "CLEAN"
    ci_state = "ALLOW" if decision == "PASS" else "FAIL"

    return {
        "decision": decision,
        "pass_mode": pass_mode,
        "ci_state": ci_state,
        "errors": errors,
        "unresolved_issue_codes": unresolved,
        "emergency_mode": emergency_mode,
    }


def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report = evaluate(case)
        expected = case["expected"]
        observed = {key: report.get(key) for key in expected}
        passed = observed == expected
        results.append({"name": case["name"], "passed": passed, "expected": expected, "observed": observed})
    ok = all(item["passed"] for item in results)
    print(json.dumps({"ok": ok, "passed": sum(item["passed"] for item in results), "total": len(results), "results": results}, ensure_ascii=False, indent=2))
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
        raise SystemExit(0 if report["ci_state"] == "ALLOW" else 1)
    ap.error("--case-file <path> or --run-tests <path> is required")


if __name__ == "__main__":
    main()
