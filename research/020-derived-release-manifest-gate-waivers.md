# 020 — Derived Release Manifest, Gate Decision & Auditable Waivers

Status: **PRACTICE / CONTROLLED RELEASE-GATE VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can MintTap combine structural/semantic integrity, dependency cycles, typed downstream impacts and approval freshness into one derived release decision, while allowing tightly scoped exceptions without falsifying the canonical truth?

This study extends 016–019 into:

**validated canonical state → derived issues → release gate → explicit waiver disposition → immutable audit-visible manifest**.

All fixtures remain synthetic. No production MintTap release is claimed.

---

## RELATED DOMAIN CHECK

### Web Manager

Study 019 established three impact severities plus fingerprint-bound approval freshness. It did not yet answer the operational release question: **can this release proceed?**

The highest-value unresolved item in `STATUS.md` was therefore a derived release manifest with deterministic `PASS / NEEDS_REVIEW / BLOCKED` behavior and an auditable waiver model.

### Design Studio

Latest Web Design status still has no substantive `W###`. Web Manager therefore defines semantic governance states only.

**HANDOFF:** a future release/review UI must distinguish:
- `PASS / CLEAN`;
- `PASS / WITH_WAIVER`;
- `NEEDS_REVIEW`;
- `BLOCKED`;
- invalid/expired waiver;
- non-waivable failure.

These distinctions must remain understandable through text/structure/programmatic semantics and must not depend on color alone.

---

# SOURCE — provenance should describe what produced an artifact

SLSA 1.2 describes provenance as verifiable information that tracks an artifact through the components that produced it, including where, when and how it was produced.

Primary source, checked 2026-09-14:
- https://slsa.dev/spec/v1.2/provenance

SLSA 1.2 build requirements state that build provenance identifies output packages by cryptographic digest and records how they were produced.

Primary source, checked 2026-09-14:
- https://slsa.dev/spec/v1.2/build-requirements

### SYNTHESIS

A release manifest is more useful when it is a **derived attestation/report tied to known inputs and decisions**, not a hand-maintained parallel truth document.

SLSA does not define MintTap website/release approval severity or waiver policy. Those remain project-specific governance decisions.

---

# MINTTAP DECISION — gate vocabulary

The release gate exposes exactly three top-level decisions:

- `PASS` — no unresolved review-required or blocking issue remains;
- `NEEDS_REVIEW` — no blocker remains, but at least one review-required issue is unresolved;
- `BLOCKED` — at least one unresolved blocking issue exists.

A `PASS` is additionally classified as:

- `CLEAN` — no waiver was needed;
- `WITH_WAIVER` — one or more valid waivers affected the gate result.

This prevents an exception-based release from looking identical to a clean release.

Informational impact remains visible in the manifest but does not change the gate by itself.

---

# MINTTAP DECISION — canonical issue vs gate consequence

The release manifest carries separate collections:

- `canonical_issues` — all derived issues detected from the validated state;
- `waivers_applied` — explicit exceptions that affect gate consequence;
- `invalid_waivers` — attempted exceptions that failed policy;
- `unresolved_issues` — canonical issues still active after valid waiver disposition.

Critical rule:

> **A waiver never deletes, edits or reclassifies the canonical issue.**

A waiver changes only whether a specific issue blocks this specific release.

This preserves the factual record and makes exception use auditable.

---

# MINTTAP DECISION — waiver validity

The current PRACTICE waiver must satisfy all of the following:

1. the issue itself is explicitly marked `waivable`;
2. the waiver references the exact `issue_fingerprint`;
3. the waiver is scoped to the same `release_ref`;
4. waiver state is `APPROVED`;
5. `approved_by` is present;
6. a non-empty `reason` is present;
7. an `expires_on` date is present and not expired at evaluation time.

Issue fingerprints are deterministic hashes over normalized issue semantics:
- issue code;
- record ID;
- source reference;
- severity;
- message;
- waivable flag.

This prevents a waiver for one known issue from silently applying to a materially different issue that merely has a similar human label.

### Non-waivable baseline

Current PRACTICE policy treats:
- semantic-integrity failures; and
- dependency cycles

as non-waivable.

The model deliberately does **not** claim every future MintTap blocker must be non-waivable. Record-type/jurisdiction/security policies still need explicit classification.

---

# IMPLEMENTED PRACTICE

New artifacts:

- `tools/evaluate_release_gate.py`
- `control/tests/release_gate_cases.json`

The evaluator consumes already-derived governance findings:
- semantic integrity errors;
- dependency cycles;
- informational impacts;
- review-required impacts;
- blocking impacts;
- approval freshness errors;
- required-control failures;
- waiver records.

It emits:
- `decision`;
- `pass_mode`;
- `canonical_issues`;
- `unresolved_issues`;
- `waivers_applied`;
- `invalid_waivers`;
- informational records;
- a deterministic `manifest_fingerprint`.

The manifest is derived output. It does not become the canonical owner of product/store/privacy/legal facts.

---

# CONTROLLED VALIDATION

Exact PRACTICE artifacts were executed locally before repository persistence.

Result:

```text
8 / 8 expected outcomes matched
```

Validated cases:

1. clean release → `PASS / CLEAN`;
2. informational-only impact → `PASS / CLEAN`;
3. unresolved review-required item → `NEEDS_REVIEW`;
4. stale blocking approval → `BLOCKED`;
5. dependency cycle + attempted waiver → remains non-waivable `BLOCKED`;
6. valid exact-issue/release-scoped/unexpired waiver → `PASS / WITH_WAIVER`, while the canonical issue remains present;
7. expired waiver → remains `BLOCKED`;
8. semantic integrity failure + attempted waiver → remains non-waivable `BLOCKED`.

### VALIDATION — key proof

The waiver test specifically confirms:

```text
canonical_issues = [APPROVAL_STALE]
waivers_applied = [valid waiver]
unresolved_issues = []
decision = PASS
pass_mode = WITH_WAIVER
```

The factual issue therefore remains visible even when policy permits the release to proceed.

---

# RELEASE PIPELINE AFTER 020

Preferred sequence:

```text
canonical records
→ schema validation
→ semantic integrity validation
→ semantic fingerprint comparison
→ cycle detection
→ typed impact propagation
→ approval freshness validation
→ derived issue set
→ waiver validation
→ release manifest
→ PASS / NEEDS_REVIEW / BLOCKED
→ rendered public surfaces
→ deployment/browser/store validation
```

This is now a coherent controlled release model at PRACTICE level.

---

# PROFESSIONAL IMPLICATIONS

## 1. “Approved” is not enough

Approval must still match the upstream semantic state.

## 2. “Waived” is not “fixed”

A waiver acknowledges an unresolved issue under a bounded exception. It must never mutate the source fact to make the repository appear clean.

## 3. Clean and exception-based releases are operationally different

`PASS / WITH_WAIVER` must remain visible in release history and later revalidation.

## 4. Not every warning should stop shipment

`INFORMATIONAL` and `REVIEW_REQUIRED` remain distinct from `BLOCKING`, reducing unnecessary release friction.

## 5. Some integrity failures should remain outside ordinary exception handling

A malformed/cyclic control model cannot provide trustworthy release provenance and therefore remains non-waivable in the current baseline.

---

# DESIGN STUDIO HANDOFF

Future Web Design / Layout-Interaction validation should test:

- whether `PASS / WITH_WAIVER` is visible without being visually conflated with `PASS / CLEAN`;
- whether `NEEDS_REVIEW` communicates required action without presenting false outage severity;
- whether `BLOCKED` exposes the actual blocker and recovery path;
- whether expired/invalid waiver states clearly explain why an exception no longer applies;
- whether keyboard/focus/status semantics support a release-review workflow;
- whether long issue IDs/reasons remain usable under Korean/English, narrow widths and enlarged text.

No visual treatment is prescribed here.

---

# OPEN / LIMITS

Still not production PASS:

- manifest/waiver JSON Schema;
- reviewer identity registry and authorization rules;
- separation of duties;
- authenticated approval signatures/attestations;
- binding manifest to Git commit/source snapshot;
- binding manifest to validator/tool/runtime versions;
- waiver issue-class authorization policy;
- jurisdiction/legal/security issue classes that must be absolutely non-waivable;
- approval and waiver expiry/revocation;
- CI enforcement;
- release-history storage/immutability;
- full RFC 8785/JCS conformance;
- real MintTap data/store/release facts.

## Highest-value next block

Implement **manifest/waiver provenance + reviewer authorization + CI enforcement**.

The next controlled proof should show:
- an authorized reviewer can approve the allowed issue class;
- an unauthorized reviewer cannot produce an effective waiver;
- a waiver/manifest bound to an old source snapshot cannot authorize a newer release state;
- the manifest records source commit/snapshot, tool version and evaluation inputs;
- CI can fail closed on `BLOCKED` or unauthorized/stale attestation without rewriting canonical truth.
