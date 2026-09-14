# 018 — Semantic Fingerprints, Dependency Invalidation & Release Impact

Status: **PRACTICE / CONTROLLED IMPACT-PROPAGATION VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can MintTap distinguish non-semantic repository edits from actual product/control meaning changes, then mechanically identify which downstream website/release artifacts require review?

This study implements the next step from Studies 015–017:

**canonical record change → semantic fingerprint comparison → dependency graph → direct/transitive review set → derived non-canonical impact report**.

All records and tests remain synthetic research fixtures. No production MintTap release state is claimed.

---

## RELATED DOMAIN CHECK

### Web Manager

Study 015 specified semantic fingerprints and dependency invalidation conceptually. Study 017 proved cross-record semantics for release/store/privacy/localization/legal/operational chains. The highest-value unresolved gap in `STATUS.md` was executable invalidation and impact derivation.

### Design Studio

Latest Layout/Interaction status now includes I003 forced-colors semantic-resilience validation. It reinforces a useful separation: a state must exist semantically before visual encoding, and critical states must survive presentation changes. Web Design still has no substantive W### result at the latest check.

**DEPENDENCY / HANDOFF:** this study defines machine truth states such as changed, directly impacted and transitively impacted. It does not prescribe badges, colors, page hierarchy or review UI. Future Web Design/Layout-Interaction work should decide how these states are presented without making color the sole carrier of meaning.

---

# SOURCE — deterministic JSON representation

RFC 8785 defines the JSON Canonicalization Scheme (JCS) for creating a deterministic JSON representation suitable for hashing/signing. It builds on I-JSON, ECMAScript primitive serialization and deterministic property sorting.

Primary source, checked 2026-09-14:
- https://www.rfc-editor.org/rfc/rfc8785

Important scope note: RFC 8785 is an **Informational RFC**, not an IETF Standards Track requirement. MintTap may adopt it as an internal engineering mechanism; Apple, Google or law do not require MintTap to use JCS for this control model.

### SOURCE — SHA-256

NIST FIPS 180-4 specifies SHA-256 among the Secure Hash Standard algorithms and describes message digests as a mechanism for detecting message changes with very high probability.

Primary source, checked 2026-09-14:
- https://csrc.nist.gov/pubs/fips/180-4/upd1/final

### SYNTHESIS

A semantic revision should not be inferred from raw file bytes alone. Whitespace, property ordering or selected operational metadata can change without changing the meaning a downstream approval relied on.

Conversely, an upstream semantic change must not remain hidden merely because the downstream JSON file itself was untouched.

---

# MINTTAP DECISION — semantic projection before hashing

For the current practice model, compute a fingerprint from a semantic projection of each canonical record.

Excluded non-semantic fields in the practice tool:
- `updated_at`;
- `verified_at`;
- `last_checked_at`;
- `last_verified_at`;
- `generated_at`;
- `notes`;
- `semantic_fingerprint`.

Everything else remains semantically significant by default.

This is intentionally conservative. A future record-type-specific projection may exclude or normalize additional fields only when there is a documented reason that downstream meaning is unchanged.

### VALIDATION LIMIT — current serializer is not yet production JCS

`tools/compute_impact.py` currently uses Python deterministic JSON serialization with sorted keys, compact separators, UTF-8 and `allow_nan=False`.

This is adequate for the present constrained synthetic corpus, but it is **not claimed as full RFC 8785 conformance**. Production promotion requires JCS conformance vectors, especially for:
- ECMAScript-compatible number serialization;
- UTF-16 property ordering for non-ASCII property names;
- I-JSON constraints.

Until that proof exists, fingerprint output is PRACTICE evidence only.

---

# IMPLEMENTED DEPENDENCY MODEL

`tools/compute_impact.py` discovers record dependencies from:
- `depends_on`;
- fields ending in `_ref`;
- fields ending in `_refs`.

Only references resolving to known canonical record IDs become graph edges. External identifiers such as a runbook name do not become canonical graph edges unless represented as actual records.

Graph direction:

```text
upstream canonical fact → downstream record that references it
```

Example from the current synthetic corpus:

```text
data:example:analytics
  → surface:example:privacy
    → legal:example:privacy
```

When comparing two snapshots, the tool combines edges from both the before and after graphs. This is necessary so removal of an upstream record still invalidates records that depended on it before deletion.

---

# DERIVED IMPACT REPORT

The tool emits:
- `added` record IDs;
- `removed` record IDs;
- `modified` IDs whose semantic fingerprint changed;
- `unchanged` IDs;
- `direct_impact`;
- `transitive_impact`;
- `review_set` = changed + all downstream impacted IDs;
- before/after fingerprints.

### MINTTAP DECISION

The impact report is **derived, non-canonical output**. It must not become a second manually maintained truth source.

Human approval/waiver records may later cite the generated impact report, but the source of truth remains the canonical records and their dependency relationships.

---

# CONTROLLED VALIDATION

New artifacts:
- `tools/compute_impact.py`;
- `control/tests/impact_cases.json`.

The exact implementation was mirrored and executed locally before repository persistence.

Result:

```text
5 / 5 expected outcomes matched
```

Validated cases:

1. metadata-only `updated_at` change → no semantic modification and no review set;
2. JSON property-order change → no semantic modification and no review set;
3. semantic data-practice change → data practice modified; privacy surface direct impact; legal trigger transitive impact;
4. added processor plus changed data-practice reference → processor/data-practice changed and privacy surface requires review;
5. removed upstream data practice → old dependency edge is preserved for impact calculation; privacy surface and legal trigger require review.

### VALIDATION — confirmed at controlled specimen level

The model can now distinguish at least two important classes:

**non-semantic edit**  
→ fingerprint unchanged  
→ no automatic downstream invalidation.

**semantic upstream edit**  
→ fingerprint changed  
→ downstream dependency closure becomes a review set even when those files themselves were untouched.

---

# PROFESSIONAL IMPLICATION

Website freshness cannot be defined as “the page file changed recently.”

A privacy page, store CTA, locale promise or legal control may become stale because an upstream canonical fact changed elsewhere.

The preferred release pipeline is therefore:

```text
canonical snapshots
  → structural validation
  → semantic integrity validation
  → semantic fingerprint comparison
  → dependency impact derivation
  → human review/approval where required
  → generated/rendered public surfaces
  → deployment/browser/store validation
```

This keeps change detection separate from presentation and prevents formatting churn from creating unnecessary review noise.

---

# OPEN / NEXT

Not yet production-proven:
- full RFC 8785 conformance and official test vectors;
- record-type-specific semantic projections;
- explicit dependency-cycle detection;
- dependency edge typing/severity;
- localization records storing `verified_against` fingerprints;
- screenshot/release compatibility invalidation;
- release manifest generation and approval/waiver workflow;
- Git commit-to-snapshot automation;
- CI integration and pinned runtime/dependencies;
- real MintTap records;
- browser/UI presentation of `STALE` / `NEEDS_REVIEW` / `BLOCKED` states.

## Highest-value next block

Implement **cycle detection + typed dependency edges + approval/freshness binding** for at least one downstream class (localization or claim), so the tool can distinguish “is impacted” from “is release-blocking” and prove that a derived approval becomes stale when its recorded upstream fingerprint no longer matches.
