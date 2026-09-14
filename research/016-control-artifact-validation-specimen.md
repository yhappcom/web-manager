# 016 — Control Artifact Validation Specimen

Status: **PRACTICE / FAILURE→REVISION→RE-PROOF COMPLETED FOR LIMITED MODEL**  
Research date: **2026-09-14**

## Question

Can the machine-readable model from Study 015 actually distinguish:

1. structurally valid records from malformed records; and
2. individually valid records from repository-wide semantic contradictions?

This study implements a deliberately small specimen. It is not the complete production schema.

---

## RELATED DOMAIN CHECK

### Study 015

015 defines the target architecture:
- canonical JSON records;
- JSON Schema Draft 2020-12 structural validation;
- stable IDs;
- repository-wide semantic linting;
- downstream staleness/invalidation.

016 tests only the first working vertical slice:

**app → feature → evidence → claim**

### Design Studio

The specimen has no visual-design authority. Its value to Design Studio is that future pages can receive realistic semantic states such as current/planned/stale/blocked rather than arbitrary mock-state labels.

---

# IMPLEMENTED SPECIMEN

## Schema

Path:
- `control/schemas/v1/record.schema.json`

Current record types:
- `app`;
- `feature`;
- `evidence`;
- `claim`.

Common lifecycle:
- `DRAFT`;
- `VERIFIED`;
- `STALE`;
- `BLOCKED`;
- `RETIRED`.

Domain state examples:
- app lifecycle: `PLANNED / ACTIVE / RETIRED`;
- feature: `PLANNED / BETA / SHIPPED / DEPRECATED / REMOVED`;
- claim mode: `CURRENT / ROADMAP`.

## Valid synthetic dataset

Paths:
- `control/records/apps/example.json`
- `control/records/features/portfolio.json`
- `control/records/evidence/portfolio-release.json`
- `control/records/claims/portfolio.json`

The data is intentionally synthetic and uses `app:example` rather than actual MintTap facts.

Relationship:

```text
app:example
  └─ feature:example:portfolio [SHIPPED]
       └─ claim:example:portfolio-overview [CURRENT]
            └─ evidence:example:portfolio-release [VERIFIED]
```

## Validator

Path:
- `tools/validate_control.py`

Current behavior:
1. parses JSON;
2. validates each record with `Draft202012Validator`;
3. creates a repository ID index;
4. detects duplicate IDs;
5. resolves app/feature/evidence references;
6. checks reference type;
7. rejects a `CURRENT` claim backed by a feature not in `SHIPPED` state;
8. rejects claim evidence not in `VERIFIED` state;
9. can execute controlled expected-failure tests.

This is a research specimen, not a hardened production validator.

---

# SOURCE BASIS

JSON Schema Draft 2020-12 defines structural validation and keywords such as required properties, enums and schema composition. `$id` and `$ref` identify/reuse schema resources; these are distinct from MintTap's business-record ID references.

Primary sources:
- https://json-schema.org/draft/2020-12
- https://json-schema.org/draft/2020-12/json-schema-core
- https://json-schema.org/draft/2020-12/json-schema-validation

RFC 8259 remains the JSON data-format basis.

Primary source:
- https://www.rfc-editor.org/rfc/rfc8259

---

# FAILURE → REVISION → RE-PROOF

## Initial failure

The first schema implementation attempted to put `unevaluatedProperties: false` inside only the record-specific branch of an `allOf` composition.

Observed result:
- even the valid `app` record failed;
- shared base properties such as `schema_version`, `id`, `status` and `owner` were reported as unevaluated/unexpected by the subtype branch.

This was a useful implementation failure: the schema looked conceptually correct but did not behave as intended under actual Draft 2020-12 evaluation.

## Revision

Moved `unevaluatedProperties: false` to the schema object that wraps the **entire `allOf`**, allowing annotations/evaluation from both:
- shared base schema; and
- record-specific schema
before rejecting unknown properties.

## Re-proof

The revised schema was executed using Python `jsonschema` Draft 2020-12 validation against the exact specimen content now saved in the repository.

Final test result:

```text
5 / 5 expected outcomes matched
```

### Case 1 — valid baseline

Expected:
- PASS

Observed:
- PASS

### Case 2 — structurally invalid claim

Fixture omits required `evidence_refs`.

Expected:
- `schema:SCHEMA_INVALID`

Observed:
- `schema:SCHEMA_INVALID`

### Case 3 — missing business reference

Claim references:
- `feature:example:not-real`

The JSON itself is structurally valid.

Expected:
- `semantic:MISSING_REF`

Observed:
- `semantic:MISSING_REF`

### Case 4 — product-truth contradiction

Claim mode:
- `CURRENT`

Referenced feature:
- `PLANNED`

Expected:
- `semantic:CURRENT_CLAIM_NOT_SHIPPED`

Observed:
- `semantic:CURRENT_CLAIM_NOT_SHIPPED`

### Case 5 — stale evidence

Claim references evidence whose control status is:
- `STALE`

Expected:
- `semantic:EVIDENCE_NOT_VERIFIED`

Observed:
- `semantic:EVIDENCE_NOT_VERIFIED`

Test definitions are stored in:
- `control/tests/cases.json`

---

# PROFESSIONAL CONCLUSION FROM THE SPECIMEN

## CONFIRMED — structural and semantic validation must stay separate

A record may be perfectly valid JSON and fully satisfy JSON Schema while still being wrong for the product.

Example:

```text
claim CURRENT
feature PLANNED
```

Both records can be structurally valid. The contradiction only appears when their relationship is evaluated.

Therefore the architecture from Study 015 is confirmed at small scale:

**JSON parser → JSON Schema → repository integrity/semantic linter**

is materially stronger than JSON Schema alone.

---

# LIMITS OF CURRENT EVIDENCE

This specimen does **not** yet validate:
- release/version relationships;
- store destinations;
- processors/data practices;
- App Data Contract;
- screenshot/release compatibility;
- locale coverage/localization staleness;
- semantic fingerprints;
- Legal Trigger Registry;
- operational surfaces;
- policy-watch records;
- dependency-cycle detection;
- automatic impact calculation;
- schema migration;
- CI integration;
- generated website content.

Current evidence level is therefore:

**PRACTICE / controlled proof of the structural-vs-semantic validation architecture.**

It is not production PASS.

---

# NEXT VALIDATION EXPANSION

Highest-value extension is not to add every possible record immediately.

Add the next records that close an actual cross-surface release chain:

1. `release`;
2. `store-destination`;
3. `data-practice` / `processor`;
4. `locale-coverage` / `localization`;
5. `legal-trigger`;
6. `operational-surface`;
7. derived `release-manifest` impact.

Then test concrete contradictions such as:
- released screenshot references planned build;
- website says Korean UI supported while locale coverage says no;
- privacy is approved against stale data-practice revision;
- legal trigger `APPLIES` but required control route is missing;
- store CTA points to unavailable destination;
- P0 surface has no monitoring owner.

---

# CI DIRECTION

## MINTTAP DECISION

When this specimen becomes a real repository gate:

- pin validator dependencies;
- run baseline validation on every pull request touching `control/` or generated public content;
- run expected-failure tests so validator regressions are detected;
- emit machine-readable validation output;
- block merge/release on defined structural/semantic errors;
- do not make warnings so noisy that teams routinely ignore them.

Exact GitHub Actions/CI implementation remains OPEN until the schema slice is mature enough to justify maintenance.

---

# HANDOFFS TO DESIGN STUDIO

## Web Design

The control model can eventually produce real UI states:
- feature unavailable/planned;
- evidence stale;
- store destination unavailable;
- locale coverage missing;
- legal/support route required.

Web Design should decide how those states are exposed to users; the validator defines when the underlying condition exists.

## Layout / Interaction

Future interaction specimens should consume the same semantic states rather than creating disconnected mock truth.

Examples:
- disabled/unavailable download destination;
- stale instruction warning;
- destructive account control;
- request failure/recovery.

## Type / Color

Future generated fixtures can provide real long labels and semantic states for rendering/contrast/focus validation.

---

# OPEN

- production validator package/version/pinning;
- schema modularization into per-record files;
- final schema `$id` namespace;
- semantic fingerprint implementation using RFC 8785-compatible canonicalization;
- full dependency graph;
- CI gate;
- role/owner identity registry;
- final folder ownership if control data eventually serves apps beyond website operations.

## Result

Study 015's core architecture survived its first executable test after one documented schema-design failure and revision.

The strongest confirmed lesson is:

> **Structural validity is not product truth. MintTap needs both schema validation and cross-record semantic validation before public content can be trusted.**
