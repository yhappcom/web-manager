#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_PR_PERMISSIONS = {"contents": "read"}
TRUSTED_SOURCES = {"PROTECTED_MAIN", "TRUSTED_MANUAL"}
DEPLOY_CREDENTIAL_MODES = {"OIDC_SHORT_LIVED", "ENVIRONMENT_SCOPED_SECRET"}


def non_none_permissions(job):
    return {k: v for k, v in job.get("permissions", {}).items() if v not in (None, "none")}


def validate_job(job, manifest):
    kind = job["kind"]
    errors = []

    if job.get("workflow_source") != "PROTECTED_BASE":
        errors.append("WORKFLOW_SOURCE_NOT_PROTECTED")
    if job.get("policy_source") != "PROTECTED_BASE":
        errors.append("POLICY_SOURCE_NOT_PROTECTED")

    if kind == "PR_VALIDATE":
        if job.get("trigger") != "pull_request":
            errors.append("PR_VALIDATE_WRONG_TRIGGER")
        if non_none_permissions(job) != ALLOWED_PR_PERMISSIONS:
            errors.append("PR_VALIDATE_EXCESS_TOKEN_PERMISSION")
        if job.get("secrets_available"):
            errors.append("PR_VALIDATE_SECRETS_FORBIDDEN")
        if job.get("id_token"):
            errors.append("PR_VALIDATE_ID_TOKEN_FORBIDDEN")
        if job.get("deployment_authority"):
            errors.append("PR_VALIDATE_DEPLOYMENT_AUTHORITY_FORBIDDEN")

    elif kind == "TRUSTED_BUILD":
        if job.get("source_trust") not in TRUSTED_SOURCES:
            errors.append("BUILD_SOURCE_NOT_TRUSTED")
        if job.get("executes_untrusted_code"):
            errors.append("TRUSTED_BUILD_EXECUTES_UNTRUSTED_CODE")
        if job.get("secrets_available") or job.get("id_token") or job.get("deployment_authority"):
            errors.append("BUILD_PRIVILEGE_BOUNDARY_VIOLATION")
        if job.get("artifact_digest") != manifest.get("artifact_digest"):
            errors.append("BUILD_ARTIFACT_DIGEST_NOT_MANIFEST_BOUND")
        if not job.get("artifact_digest"):
            errors.append("BUILD_ARTIFACT_DIGEST_MISSING")

    elif kind == "DEPLOY":
        if job.get("source_trust") not in TRUSTED_SOURCES:
            errors.append("DEPLOY_SOURCE_NOT_TRUSTED")
        if job.get("executes_untrusted_code"):
            errors.append("DEPLOY_EXECUTES_UNTRUSTED_CODE")
        if manifest.get("ci_state") != "ALLOW":
            errors.append("DEPLOY_GATE_NOT_ALLOW")
        if job.get("artifact_origin") != "TRUSTED_BUILD":
            errors.append("DEPLOY_ARTIFACT_ORIGIN_UNTRUSTED")
        if job.get("artifact_digest") != manifest.get("artifact_digest"):
            errors.append("DEPLOY_ARTIFACT_DIGEST_MISMATCH")
        if not job.get("digest_mismatch_fails_closed"):
            errors.append("DEPLOY_DIGEST_MISMATCH_NOT_FAIL_CLOSED")
        if not job.get("deployment_authority"):
            errors.append("DEPLOY_AUTHORITY_MISSING")
        mode = job.get("credential_mode")
        if mode not in DEPLOY_CREDENTIAL_MODES:
            errors.append("DEPLOY_CREDENTIAL_MODE_INVALID")
        if mode == "OIDC_SHORT_LIVED":
            if not job.get("id_token"):
                errors.append("DEPLOY_OIDC_PERMISSION_MISSING")
            if job.get("long_lived_provider_secret"):
                errors.append("DEPLOY_LONG_LIVED_SECRET_WITH_OIDC")
        if mode == "ENVIRONMENT_SCOPED_SECRET":
            if not job.get("secrets_available"):
                errors.append("DEPLOY_SCOPED_SECRET_MISSING")
            if job.get("secret_scope") != "DEPLOY_JOB_ONLY":
                errors.append("DEPLOY_SECRET_SCOPE_TOO_BROAD")
        if job.get("trigger") in {"pull_request_target", "workflow_run"} and job.get("artifact_from_untrusted_pr"):
            errors.append("PRIVILEGED_TRIGGER_CONSUMES_UNTRUSTED_ARTIFACT")

    elif kind == "ROLLBACK":
        if job.get("trigger") != "workflow_dispatch":
            errors.append("ROLLBACK_NOT_MANUAL")
        if not job.get("authorized"):
            errors.append("ROLLBACK_AUTHORIZATION_MISSING")
        if not job.get("reason"):
            errors.append("ROLLBACK_REASON_MISSING")
        if job.get("rebuilds_source"):
            errors.append("ROLLBACK_REBUILD_FORBIDDEN")
        if job.get("artifact_digest") not in manifest.get("previously_approved_artifact_digests", []):
            errors.append("ROLLBACK_ARTIFACT_NOT_PREVIOUSLY_APPROVED")
        if not job.get("deployment_authority"):
            errors.append("ROLLBACK_DEPLOYMENT_AUTHORITY_MISSING")
        if job.get("credential_mode") not in DEPLOY_CREDENTIAL_MODES:
            errors.append("ROLLBACK_CREDENTIAL_MODE_INVALID")

    if job.get("trigger") == "pull_request_target" and job.get("executes_untrusted_code"):
        errors.append("PULL_REQUEST_TARGET_EXECUTES_UNTRUSTED_CODE")
    if job.get("trigger") == "workflow_run" and job.get("executes_untrusted_artifact"):
        errors.append("WORKFLOW_RUN_EXECUTES_UNTRUSTED_ARTIFACT")

    return sorted(set(errors))


def evaluate(case):
    manifest = case["manifest"]
    results = []
    for job in case["jobs"]:
        errors = validate_job(job, manifest)
        results.append({"name": job["name"], "kind": job["kind"], "errors": errors})
    errors = [{"job": r["name"], "errors": r["errors"]} for r in results if r["errors"]]
    return {"contract_state": "PASS" if not errors else "FAIL", "job_results": results, "errors": errors}


def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        report = evaluate(case)
        expected = case["expected"]
        observed = {
            "contract_state": report["contract_state"],
            "error_codes": sorted({e for x in report["errors"] for e in x["errors"]}),
        }
        passed = all(observed[k] == v for k, v in expected.items())
        results.append({"name": case["name"], "passed": passed, "expected": expected, "observed": observed})
    ok = all(r["passed"] for r in results)
    print(json.dumps({"ok": ok, "passed": sum(r["passed"] for r in results), "total": len(results), "results": results}, indent=2))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-tests")
    ap.add_argument("--case-file")
    args = ap.parse_args()
    if args.run_tests:
        raise SystemExit(run_tests(args.run_tests))
    if args.case_file:
        report = evaluate(json.loads(Path(args.case_file).read_text(encoding="utf-8")))
        print(json.dumps(report, indent=2))
        raise SystemExit(0 if report["contract_state"] == "PASS" else 1)
    ap.error("--run-tests <path> or --case-file <path> required")


if __name__ == "__main__":
    main()
