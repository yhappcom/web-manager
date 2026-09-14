# 019 — Typed Dependency Edges, Cycle Detection & Approval Freshness

Status: **PRACTICE / CONTROLLED RELEASE-GOVERNANCE VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can MintTap move from a generic “this changed, review downstream records” model to a release-governance model that distinguishes informational impact, review-required impact and release-blocking impact, while proving that an approval becomes stale when its upstream semantic fingerprint changes?

This study extends 018 with:

**semantic change → typed dependency propagation → approval fingerprint check → stale/blocking decision**.

All fixtures remain synthetic and are not production MintTap facts.

---

## RELATED DOMAIN CHECK

### Web Manager

018 implemented semantic fingerprints and transitive impact derivation, but every downstream relation effectively belonged to one undifferentiated review set. The next highest-value gap in `STATUS.md` was typed edge severity, cycle detection and approval/freshness binding.

### Design Studio

Latest Design Studio global status still places Web Design before W001. Web Manager therefore defines machine states only, not their visual treatment.

Layout/Interaction evidence remains relevant: critical state meaning must survive presentation changes. A future web review UI must expose `INFORMATIONAL`, `NEEDS_REVIEW`, `BLOCKED` and stale-approval state through text/structure/programmatic semantics, not color alone.

**HANDOFF:** Web Design/Layout-Interaction should later test how blocking vs non-blocking governance states are communicated without creating false urgency or hiding release-critical states.

---

# SOURCE — invariant fingerprint input

RFC 8785 defines JCS as a deterministic JSON representation suitable for repeatable hashing and explicitly states that the RFC is Informational rather than Standards Track.

Primary source, checked 2026-09-14:
- https://www.rfc-editor.org/rfc/rfc8785

NIST FIPS 180-4 specifies SHA-256 and describes message digests as a mechanism for detecting whether messages changed after the digest was generated.

Primary source, checked 2026-09-14:
- https://csrc.nist.gov/pubs/fips/180-4/upd1/final

### SYNTHESIS

The external sources justify deterministic change fingerprints. They do **not** define MintTap release severity, approval expiry or dependency policy.

Those are project-governance rules and are recorded below as `MINTTAP DECISION`.

---

# MINTTAP DECISION — typed dependency edges

New explicit dependency form:

```json
{
  "dependencies": [
    {
      "ref": "feature:example:portfolio",
      "impact": "BLOCKING"
    }
  ]
}
```

Current impact vocabulary:

- `INFORMATIONAL` — downstream record is relevant to the change but the change alone does not require review or block release.
- `REVIEW_REQUIRED` — downstream record requires explicit review before it can be treated as current for the affected release/surface.
- `BLOCKING` — the dependent cannot remain release-approved until its required review/approval is restored.

This is a project control vocabulary, not an Apple/Google/legal standard.

For compatibility with 016–018 fixtures, unresolved ordinary `*_ref`, `*_refs` and `depends_on` references default to `REVIEW_REQUIRED` until explicitly typed.

### Propagation rule

For one dependency path, the weakest edge limits the propagated severity.

Example:

```text
A --BLOCKING--> B --INFORMATIONAL--> C
```

A change can block B, but C is only informational through that path.

If multiple independent paths reach the same downstream record, the strongest resulting path wins.

This prevents a weak informational relationship from accidentally becoming blocking merely because an upstream record is critical elsewhere.

---

# MINTTAP DECISION — approval freshness binding

A downstream approval can bind itself to the exact semantic fingerprint it reviewed:

```json
{
  "approval_bindings": [
    {
      "ref": "feature:example:portfolio",
      "verified_against": "sha256:...",
      "impact": "BLOCKING"
    }
  ]
}
```

Validation rule:

- referenced upstream record missing → `APPROVAL_SOURCE_MISSING`;
- current semantic fingerprint differs from `verified_against` → `APPROVAL_STALE`;
- matching fingerprint → approval remains current for this binding.

Operational timestamps excluded by the semantic projection do not invalidate the approval by themselves.

### Professional implication

A record's own status field cannot prove its approval is current.

An `APPROVED` localization whose upstream source changed is operationally stale even if nobody edited the localization file.

---

# MINTTAP DECISION — dependency cycles

Canonical truth dependencies should not contain unresolved cycles when those edges are used to establish freshness or approval order.

Example invalid graph:

```text
control:a → control:b → control:a
```

Reason:

- there is no stable upstream/downstream ordering;
- invalidation can become self-referential;
- approval provenance becomes ambiguous;
- release-impact traversal may conceal modeling errors.

The new PRACTICE validator performs DFS-based cycle detection and reports the cycle path.

This is an internal integrity rule, not a claim that every graph in software engineering must be acyclic.

---

# IMPLEMENTED PRACTICE

New artifacts:

- `tools/validate_dependency_governance.py`
- `control/tests/dependency_governance_cases.json`

The tool:

1. computes the same constrained deterministic semantic fingerprint used in 018;
2. reads explicit typed dependencies;
3. retains backward-compatible inferred refs as `REVIEW_REQUIRED`;
4. compares before/after semantic state;
5. propagates typed downstream impact;
6. checks approval bindings against current upstream fingerprints;
7. detects dependency cycles.

The current serializer retains the same 018 limitation: deterministic Python JSON serialization is **not yet claimed as full RFC 8785 JCS conformance**.

---

# CONTROLLED VALIDATION

Exact PRACTICE artifacts were executed locally before persistence.

Result:

```text
6 / 6 expected outcomes matched
```

Validated cases:

1. valid approval binding → no stale error;
2. upstream semantic change → dependent approved localization becomes blocking-impact and fingerprint mismatch is detected;
3. metadata-only upstream change → no semantic change and approval remains valid;
4. informational dependency → informational impact only;
5. review-required dependency → review-required impact only, not release-blocking;
6. two-record dependency cycle → cycle path detected.

### VALIDATION — confirmed at controlled specimen level

The control model can now distinguish:

```text
changed but informational
changed and human review required
changed and release-blocking
approved and still current
approved file whose upstream basis is now stale
invalid cyclic dependency model
```

This materially reduces two opposite risks:

- **under-control:** stale downstream content remains “approved” after source meaning changes;
- **over-control:** harmless/informational changes unnecessarily block a release.

---

# RELEASE-GATE DIRECTION

Preferred control sequence now becomes:

```text
canonical records
→ schema validation
→ semantic integrity validation
→ semantic fingerprint comparison
→ cycle validation
→ typed impact propagation
→ approval freshness validation
→ release gate / human review
→ rendered public surfaces
→ deployment/browser/store validation
```

A future release manifest should consume these derived results rather than manually recopy them.

---

# OPEN / LIMITS

Still not production PASS:

- full RFC 8785 conformance vectors;
- schema support for `dependencies` / `approval_bindings`;
- record-type-specific allowed edge types;
- explicit release-manifest and waiver model;
- reviewer identity/authorization model;
- approval expiry independent of source change;
- multi-source approval policy (`all` vs `any`);
- real localization record integration;
- claim approval binding;
- screenshot-to-release binding;
- CI enforcement;
- real MintTap app/store/data/legal records.

## Highest-value next block

Implement a **derived release manifest + gate decision model** using the current semantic/typed/approval results.

The next validation should prove that a synthetic release is:
- `PASS` when all required controls are current;
- `NEEDS_REVIEW` for non-blocking unresolved review items;
- `BLOCKED` for stale blocking approval, cycle, semantic integrity failure or required release control failure;

and should model explicit, auditable waivers without allowing a waiver to silently rewrite canonical truth.
