#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED = {
    "preview_isolated": True,
    "production_separate_from_preview": True,
    "rollback_without_source_rebuild": True,
    "static_headers_supported": True,
    "redirects_supported": True,
    "custom_404_supported": True,
}

def evaluate(provider):
    failures = []
    for key, expected in REQUIRED.items():
        if provider.get(key) != expected:
            failures.append(f"REQUIRED_{key.upper()}")

    cred = provider.get("ci_credential_mode")
    if cred not in {"OIDC_SHORT_LIVED", "SCOPED_API_TOKEN"}:
        failures.append("UNACCEPTABLE_CI_CREDENTIAL_MODE")

    if provider.get("preview_artifact_promotable_exactly") is not True:
        failures.append("NO_EXACT_PREVIEW_TO_PROD_PROMOTION")

    if provider.get("rollback_retention_bounded") is not True:
        failures.append("ROLLBACK_RETENTION_NOT_EXPLICITLY_BOUNDED")

    if provider.get("dynamic_state_rollback_complete") is not False:
        failures.append("DYNAMIC_STATE_ROLLBACK_ASSUMPTION_UNSAFE")

    if provider.get("live_account_validation_required") is not True:
        failures.append("LIVE_VALIDATION_REQUIREMENT_MISSING")

    return {"provider": provider["provider"], "ok": not failures, "failures": failures}

def run_tests(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        observed = evaluate(case["provider_contract"])
        passed = observed == case["expected"]
        results.append({"name": case["name"], "passed": passed, "expected": case["expected"], "observed": observed})
    ok = all(x["passed"] for x in results)
    print(json.dumps({"ok": ok, "passed": sum(x["passed"] for x in results), "total": len(results), "results": results}, indent=2))
    return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-tests")
    args = ap.parse_args()
    if not args.run_tests:
        ap.error("--run-tests required")
    raise SystemExit(run_tests(args.run_tests))

if __name__ == "__main__":
    main()
