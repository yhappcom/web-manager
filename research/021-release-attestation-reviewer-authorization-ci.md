# 021 — Manifest/Waiver Provenance, Reviewer Authorization & CI Enforcement

Status: **PRACTICE / CONTROLLED AUTHORIZATION + CI VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can MintTap prevent an otherwise well-formed waiver or manifest from authorizing a release when the reviewer is unauthorized, the approval violates separation of duties, or the attestation was produced against an older source snapshot/tool version?

This study extends 020 into:

**release issue → authorized reviewer → snapshot/tool-bound waiver → manifest attestation → fail-closed CI result**.

All fixtures remain synthetic. No production MintTap release is claimed.

---

## RELATED DOMAIN CHECK

### Web Manager

020 proved that a waiver can alter the gate consequence without rewriting canonical truth. It did not prove that the person applying the waiver had authority or that the waiver still referred to the release state currently being evaluated.

021 closes that gap at PRACTICE level.

### Design Studio

Latest Web Design status still has no substantive `W###`. Governance semantics remain Web Manager-owned inputs.

**HANDOFF:** future review UI must make reviewer authority, stale provenance, separation-of-duties failure and CI blocking understandable without relying on color alone.

---

# SOURCE — separation of duties

NIST SP 800-53 Rev. 5.1 control AC-5 identifies and documents duties requiring separation and defines access authorizations that support that separation.

Primary source, checked 2026-09-14:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### SYNTHESIS

MintTap should not treat a reviewer identity string as sufficient authorization. Approval authority should be an explicit control fact, and selected release exceptions should require separation between requester and approver.

NIST does not prescribe MintTap's reviewer roles or issue-class matrix. Those are project decisions.

---

# SOURCE — CI fail-closed mechanics

GitHub Actions documents that exit code `0` produces success and a non-zero exit code produces failure for an action/check run.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes

GitHub repository rulesets can require status checks to pass before merging. GitHub also permits a required status check to be associated with an expected GitHub App source.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets

### SYNTHESIS

A MintTap release-governance validator can become an enforceable merge/release gate if it exits non-zero for anything other than an acceptable release state and the repository requires that check.

The exact branch/ruleset configuration remains an operational MintTap decision and must be validated against the actual GitHub plan/repository configuration before production use.

---

# MINTTAP DECISION — reviewer registry

A waiver reviewer is authorized only when the current reviewer registry establishes all required facts:

```json
{
  "id": "reviewer:release",
  "active": true,
  "permissions": ["WAIVE"],
  "allowed_issue_codes": ["APPROVAL_STALE"]
}
```

A reviewer must therefore be:
- known;
- active;
- explicitly granted `WAIVE` permission;
- authorized for the specific issue class.

Reviewer authorization is canonical control data. The waiver itself must not be allowed to grant its own reviewer authority.

---

# MINTTAP DECISION — separation of duties

Current PRACTICE baseline rejects a waiver where:

```text
requested_by == approved_by
```

with `SEPARATION_OF_DUTIES_VIOLATION`.

This is intentionally a narrow first rule. Production policy still needs role-specific separation requirements, emergency/break-glass policy and organization ownership.

---

# MINTTAP DECISION — provenance binding

Each effective waiver must bind to:
- exact issue fingerprint;
- exact `release_ref`;
- current source snapshot/commit identifier;
- current validator/tool version;
- authorized reviewer;
- requester;
- approval state;
- reason;
- expiry.

A manifest attestation is separately checked against:
- `release_ref`;
- current source snapshot;
- current tool version.

A waiver or manifest bound to an older source snapshot or validator version is not treated as current merely because its human-readable release name still matches.

---

# MINTTAP DECISION — CI behavior

Current PRACTICE rule:

```text
PASS         → process exit 0 / CI PASS
NEEDS_REVIEW → process exit non-zero / CI FAIL
BLOCKED      → process exit non-zero / CI FAIL
```

This deliberately fails closed. `NEEDS_REVIEW` is not silently deployable just because it is less severe than `BLOCKED`.

A future production workflow may distinguish merge checks from deploy checks, but no automated release should infer approval from an unresolved review state.

---

# IMPLEMENTED PRACTICE

New artifacts:
- `tools/validate_release_attestation.py`
- `control/tests/release_attestation_cases.json`

The validator:
1. derives stable issue fingerprints;
2. verifies reviewer identity against a reviewer registry;
3. checks reviewer active state and `WAIVE` permission;
4. checks issue-class authorization;
5. rejects requester/approver identity equality;
6. binds waiver to source snapshot and tool version;
7. validates manifest attestation provenance;
8. emits `PASS / NEEDS_REVIEW / BLOCKED` plus `ci_status`;
9. exits non-zero for non-PASS case-file evaluation.

---

# CONTROLLED VALIDATION

Result:

```text
8 / 8 expected outcomes matched
```

Validated cases:
1. authorized, current, correctly scoped waiver → `PASS / WITH_WAIVER`, CI PASS;
2. unknown reviewer → `BLOCKED`, CI FAIL;
3. reviewer lacks authorization for the issue class → `BLOCKED`, CI FAIL;
4. requester self-approves → separation-of-duties failure, CI FAIL;
5. waiver bound to old source snapshot → stale waiver, CI FAIL;
6. waiver bound to old tool version → stale waiver, CI FAIL;
7. clean manifest attestation matching current release/snapshot/tool → `PASS / CLEAN`, CI PASS;
8. unresolved `NEEDS_REVIEW` → CI FAIL.

### VALIDATION — key proof

A syntactically valid waiver is insufficient. All of the following must simultaneously remain true:

```text
exact issue
+ exact release
+ exact current source snapshot
+ exact current tool version
+ authorized active reviewer
+ permitted issue class
+ separated requester/approver
+ approved/unexpired waiver
```

Otherwise the exception cannot create a release `PASS`.

---

# REPOSITORY ENFORCEMENT DIRECTION

Production direction:

```text
canonical records
→ validators
→ release manifest / attestation validator
→ non-zero exit on NEEDS_REVIEW or BLOCKED
→ GitHub required status check
→ merge/deploy only when required check passes
```

Where GitHub configuration permits, prefer a required check tied to the expected integration/app source rather than accepting an arbitrary actor as the status producer.

This remains a configuration target, not a claim that the current `web-manager` repository already has such a ruleset enabled.

---

# PROFESSIONAL IMPLICATIONS

## 1. Identity is not authority

`approved_by` is evidence only when matched against current authorization data.

## 2. Authority is issue-class specific

A localization/content reviewer should not automatically gain authority to waive legal/security/release-integrity controls.

## 3. Approval is snapshot-specific

Changing source state invalidates the old decision context unless the approval is re-established against the new snapshot.

## 4. Tool provenance matters

A validator change can alter issue derivation or gate semantics. Old attestations must not silently authorize output produced under materially different validation logic.

## 5. CI must fail closed

Operational enforcement is stronger than a report that humans may accidentally ignore.

---

# OPEN / LIMITS

Still not production PASS:
- reviewer registry schema and canonical storage location;
- role hierarchy and group ownership;
- authenticated identity mapping from GitHub/SSO to reviewer ID;
- signed attestations / cryptographic signature verification;
- actual Git commit/tree digest binding rather than synthetic snapshot strings;
- validator runtime/container digest and dependency lock binding;
- emergency/break-glass workflow;
- legal/security non-waivable policy ownership;
- reviewer revocation propagation;
- durable immutable release history;
- actual GitHub ruleset/required-check configuration;
- CI workflow threat model, fork behavior and permissions hardening;
- schema migration/version negotiation;
- real MintTap release facts.

## Highest-value next block

Implement **actual source-tree/toolchain identity + signed/immutable attestation model and CI threat-model hardening** at controlled specimen level.

Next proof should distinguish:
- Git commit identity from mutable branch names;
- validator source version from runtime/dependency identity;
- unsigned data from authenticated approval evidence;
- trusted CI context from untrusted fork/PR input;
- normal authorization from explicit break-glass procedure.
