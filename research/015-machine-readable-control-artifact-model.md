# 015 — Machine-Readable Control Artifacts / Single Source of Truth

Status: **FOUNDATION DATA-CONTRACT STUDY / SCHEMAS NOT YET IMPLEMENTED**  
Research date: **2026-09-14**

## Question

How should MintTap represent Product Truth, data practices, claims, localization, evidence, legal triggers, operational surfaces and release state so the website can be generated and validated from one coherent fact system rather than maintaining the same fact manually in multiple documents?

The goal is not to build an internal ERP. The goal is the smallest structured control layer that prevents cross-surface contradiction and can later drive static-site generation, release checks and change-watch automation.

---

## RELATED DOMAIN CHECK

### Existing Web Manager studies

This study normalizes artifacts introduced earlier:
- Study 003 — App Data Contract;
- Study 004 — Product Truth Record, Screenshot Evidence Set, Content Release Manifest;
- Study 007 — Locale Matrix, Localization Manifest;
- Study 010 — Claim Registry;
- Study 011 — Policy Change Register, Operational Surface Registry;
- Study 013 — Legal Trigger Registry;
- Study 014 — provider-neutral assertion/report model.

These artifacts currently exist as conceptual contracts. Without a machine-readable relationship model, the same facts could be copied independently and drift.

### Design Studio

This study does not define visual design. It creates stable structured inputs that future Web Design can consume without turning engineering/database structure into page hierarchy.

Relevant handoff principle:
- Design Studio chooses how information is presented;
- Web Manager truth/control data determines what may truthfully be presented and what is stale/blocked.

---

# 1. SOURCE — JSON AND JSON SCHEMA

RFC 8259 defines JSON as a lightweight, text-based, language-independent structured-data format with objects, arrays, strings, numbers, booleans and null.

Primary source:
- https://www.rfc-editor.org/rfc/rfc8259

JSON Schema Draft 2020-12 provides structural validation, reusable schema references through `$id` / `$ref`, required fields, enums and other constraints. Its validation specification makes clear that JSON Schema validates instance structure and values against asserted constraints.

Primary sources:
- https://json-schema.org/draft/2020-12
- https://json-schema.org/draft/2020-12/json-schema-core
- https://json-schema.org/draft/2020-12/json-schema-validation

### SYNTHESIS

JSON Schema is appropriate for validating **record shape**, but MintTap also needs repository-wide semantic checks such as:
- does `claim.feature_refs` point to a real shipped feature?;
- does a screenshot reference an existing release?;
- is a localized page approved against the latest source revision?;
- does an `APPLIES` legal trigger have a mapped notice/control?;
- does a P0 operational surface have an owner/runbook?;
- are dependency cycles present?

Those are business/repository integrity rules and require a separate linter/validator layer in addition to JSON Schema.

### MINTTAP DECISION

Use **JSON as the canonical structured-control format** for Foundation implementation, validated with **JSON Schema Draft 2020-12** plus MintTap-specific cross-record validation.

Why JSON rather than YAML as the canonical truth layer:
- one standardized data model and parser behavior;
- direct JSON Schema validation;
- fewer implicit typing/anchor/merge semantics;
- deterministic build/tooling behavior;
- easy consumption by JavaScript/TypeScript, Dart, Python and CI tooling.

This does not prohibit Markdown or a future CMS for editorial prose. Narrative content remains a separate authoring layer that **references** canonical truth IDs.

---

# 2. CANONICAL DATA VS PRESENTATION CONTENT

## MINTTAP DECISION — two-layer model

### Layer A — canonical structured truth/control

Machine-readable JSON records for facts, evidence, dependencies, approvals and operational state.

Examples:
- app identity/platform availability;
- releases;
- features/capabilities;
- account/subscription behavior;
- data practices/processors;
- supported app UI locales;
- store destinations;
- claims/evidence;
- screenshots;
- legal applicability;
- policy watch;
- operational surfaces.

### Layer B — localized editorial presentation

Human-facing copy such as:
- hero copy;
- feature explanation;
- FAQ prose;
- privacy narrative;
- support instructions;
- page titles/descriptions.

Layer B may vary editorially by locale but must reference Layer A facts/claims and may not silently redefine them.

### Anti-pattern

Do not separately type these facts into:
- homepage copy;
- app page copy;
- App Store notes;
- Google Play notes;
- JSON-LD;
- FAQ;
- privacy page;
- release checklist;
without a shared canonical source or explicit validated derivation.

---

# 3. NORMALIZED ENTITY MODEL

## Core record types

### `app`
Stable app identity.

Canonical facts:
- immutable app ID;
- public product name;
- platform package/bundle identifiers when approved for repository storage;
- lifecycle state;
- intended markets/audience classification references;
- app UI locale IDs;
- current release refs;
- store destination refs.

### `release`
A specific released/planned app version per platform.

Fields conceptually include:
- app ref;
- platform;
- version/build;
- lifecycle (`planned`, `beta`, `submitted`, `released`, `retired`);
- release/effective date;
- feature refs;
- data-contract revision ref;
- locale refs;
- store listing ref/status.

### `feature`
A capability independent of marketing wording.

Fields:
- app ref;
- stable feature ID;
- state (`planned`, `beta`, `shipped`, `deprecated`, `removed`);
- platform scope;
- release introduction/removal refs;
- material conditions/limits;
- technical verification refs.

### `data-practice`
Actual collection/use/share/retention behavior.

Fields:
- app ref;
- data category;
- collection source;
- purpose;
- processor refs;
- third-party provision/sharing classification;
- retention/deletion;
- sensitive-data classification;
- country/transfer refs;
- account-deletion consequence;
- evidence/engineering owner.

### `processor`
Reusable external/internal processor/vendor entity.

Fields:
- entity name;
- service;
- role;
- official privacy/DPA reference;
- processing/storage region facts when known;
- data categories/purposes refs;
- change-watch status.

Do not put secret API keys, project secrets or private credentials here.

### `store-destination`
Official public store destination and publication state.

Fields:
- app;
- platform/store;
- public URL;
- store/app ID;
- availability markets;
- publication state;
- last verified time.

### `evidence`
Generic proof that supports product facts/claims.

Evidence classes may include:
- engineering confirmation;
- released-build observation;
- test report;
- official store state;
- screenshot/video;
- analytics metric snapshot;
- external authoritative source.

### `screenshot`
Specialized evidence record.

Fields:
- app/release/platform;
- locale shown;
- feature refs;
- capture date;
- sample/live/staged data classification;
- asset path/hash;
- approval state;
- invalidation triggers.

### `claim`
Marketing assertion, never the underlying product fact itself.

Fields:
- claim class;
- app;
- upstream feature/fact refs;
- evidence refs;
- conditions/qualifiers;
- approved locale expressions or content refs;
- status;
- verification/expiry;
- surfaces using claim.

### `locale-coverage`
Machine-readable Locale Matrix.

Separate booleans/states for:
- app UI;
- website;
- Apple store metadata;
- Google Play metadata;
- privacy;
- support;
- account deletion;
- screenshots.

Never infer one from another.

### `localization`
Translation approval/staleness record.

Fields:
- source record/content ID;
- source semantic revision;
- target locale;
- translator/reviewer role or owner ref;
- glossary/version;
- status (`draft`, `reviewed`, `approved`, `stale`);
- approval date;
- invalidation reason.

### `legal-trigger`
Study 013 applicability record.

Fields:
- jurisdiction/law;
- trigger fact refs;
- state (`UNKNOWN`, `CONDITIONAL`, `APPLIES`, `DOES_NOT_APPLY`);
- required notice/control refs;
- operational process refs;
- source URLs/effective dates;
- legal review state;
- freshness.

### `operational-surface`
A production URL/console/machine endpoint requiring monitoring.

Fields:
- surface class;
- expected URL/host;
- expected status/MIME/redirect behavior;
- owner;
- severity;
- monitoring cadence/method;
- runbook ref;
- last validation result;
- dependency refs.

### `policy-watch`
Tracked platform/legal policy source.

Fields:
- authority/source URL;
- jurisdiction/platform;
- announcement/effective/deadline dates;
- impacted app/control refs;
- review state;
- next action.

### `release-manifest`
A release-specific **derived + approved** impact record.

It should not be a second hand-maintained copy of all facts.

It should contain:
- release ref;
- changed canonical record IDs;
- automatically calculated impacted claims/localizations/pages/legal triggers/surfaces;
- required checks;
- human approvals/waivers;
- final release decision.

---

# 4. STABLE IDENTIFIERS

## MINTTAP DECISION

Every canonical record gets an immutable logical ID independent of filename, display name or locale.

Example namespace pattern:

```text
app:minttap
release:minttap:ios:1.0.19
feature:minttap:portfolio-tracking
processor:google:firebase-auth
claim:minttap:portfolio-overview
screenshot:minttap:ios:1.0.19:portfolio-home:ko:001
surface:minttap:privacy:ko
legal:kr:pipa:privacy-policy
```

Rules:
- lowercase ASCII IDs where possible;
- IDs are never recycled after retirement;
- public display names may change without ID change;
- paths may change without ID change;
- locale is only in ID when the record is actually locale-specific;
- references use IDs, not filenames or display strings.

### Why

A renamed app/page should not break historical release evidence or claim dependencies.

---

# 5. COMMON RECORD ENVELOPE

Every critical canonical record should expose a small common envelope.

Conceptual example:

```json
{
  "schema_version": 1,
  "record_type": "feature",
  "id": "feature:minttap:portfolio-tracking",
  "status": "VERIFIED",
  "owner": "role:product",
  "updated_at": "2026-09-14T08:00:00Z",
  "verified_at": "2026-09-14T08:00:00Z",
  "source_refs": ["evidence:..."],
  "depends_on": ["app:minttap"],
  "notes": null
}
```

### Status vocabulary

For canonical/control records use a small shared lifecycle where meaningful:
- `DRAFT`;
- `VERIFIED`;
- `STALE`;
- `BLOCKED`;
- `RETIRED`.

Domain-specific states remain separate fields. Example: a legal trigger has an applicability state **and** a record freshness/verification state.

Do not overload one `status` field to mean both legal applicability and editorial approval.

---

# 6. SCHEMA DESIGN RULES

## SOURCE — JSON Schema structural validation

Draft 2020-12 supports constraints including type, enum, required properties, array uniqueness and object-property rules; `$id` gives a schema resource a canonical URI and `$ref` composes reusable schemas.

Primary sources:
- https://json-schema.org/draft/2020-12/json-schema-core
- https://json-schema.org/draft/2020-12/json-schema-validation

## MINTTAP DECISION

### Each schema must
- declare `$schema` as Draft 2020-12;
- have a stable absolute `$id` identifier;
- require `schema_version`, `record_type`, `id` and required domain fields;
- use enums for controlled state values;
- reject unknown critical properties using `additionalProperties: false` or an equally deliberate rule where practical;
- reuse common definitions through `$ref`;
- document fields with `title`/`description` where useful;
- validate date/time strings using an implementation configured to assert the applicable format rather than assuming every validator enforces `format` identically.

### Important distinction

JSON Schema `$ref` is for **schema composition**.

Business-record fields such as `feature_refs` or `processor_refs` are ordinary stable-ID strings. Their existence and semantic compatibility are checked by the repository integrity linter, not confused with JSON Schema `$ref`.

---

# 7. REPOSITORY-WIDE INTEGRITY LINTER

## MINTTAP DECISION

A successful JSON Schema validation is **necessary but insufficient**.

The MintTap validator must also load all canonical records into an ID index and run semantic rules.

### Required integrity classes

#### Referential integrity
- every referenced record ID exists;
- referenced type is allowed;
- no duplicate IDs;
- retired IDs are not used by new active records unless explicitly allowed.

#### Dependency graph
- detect dependency cycles where the model expects a DAG;
- list upstream and downstream dependents;
- compute impact set when an upstream record changes.

#### Product truth
- a factual “currently available” claim cannot reference only `planned`/`removed` features;
- a public store CTA cannot reference unavailable/retired destination as active;
- platform/locale claims must agree with app/release/locale coverage.

#### Privacy/data
- public privacy state must reference the current approved data-contract semantic revision;
- active processors referenced by data practices must exist and have review state;
- a data practice with cross-border processing cannot silently omit known processor/location metadata;
- account-deletion text/control scope must reconcile with account/data-practice facts.

#### Evidence/claims
- material factual/quantified/security/privacy claims require permitted evidence class;
- expired/stale evidence makes dependent claim `STALE` or build-blocking according to severity;
- screenshot referenced as current must map to a compatible released version/feature state.

#### Localization
- approved translation must reference the current source semantic revision;
- website/store/app UI locale states remain independent;
- marketing localization may not map to a stronger claim ID than source authorization permits;
- legal/privacy translations become stale after relevant source/data-contract change.

#### Legal
- `APPLIES` legal trigger must have required control/surface/process mapping where the trigger definition requires it;
- unresolved required legal review blocks relevant release gate;
- `DOES_NOT_APPLY` should record supporting trigger facts/review date rather than be a naked boolean.

#### Operations
- P0/P1 operational surface requires owner, monitoring method/cadence and runbook/reference;
- required public surface must have expected URL/status behavior;
- launch-critical machine endpoints must exist in the POC/production surface set when the feature is enabled.

---

# 8. SEMANTIC REVISION / STALENESS

## Problem

Git history tells us that a file changed, but downstream records need to know whether the **meaning they were approved against** changed.

Whitespace/reformatting alone should not invalidate every translation or claim.

## SOURCE — JSON Canonicalization Scheme

RFC 8785 describes deterministic JSON canonicalization for repeatable hashing/signing, using constrained JSON data and deterministic property ordering.

Primary source:
- https://www.rfc-editor.org/rfc/rfc8785

### MINTTAP DECISION — semantic fingerprint

For selected upstream canonical records, compute a `semantic_fingerprint` from the subset of fields that define downstream meaning.

Suggested process:
1. remove operational metadata such as `updated_at`, comments/notes and generated fingerprint itself;
2. construct the defined semantic projection for that record type;
3. serialize using an RFC 8785-compatible canonicalization implementation;
4. SHA-256 the canonical bytes;
5. store/emit the resulting fingerprint in generated validation output, not necessarily hand-edit it.

Derived records store the upstream fingerprint they were approved/verified against.

Example:

```json
{
  "source_ref": "feature:minttap:portfolio-tracking",
  "verified_against": "sha256:..."
}
```

If the current semantic fingerprint differs:
- localization → `STALE`;
- claim → revalidation required;
- screenshot → evaluate trigger scope;
- legal/privacy document → re-review if changed fields are relevant.

### Caution

RFC 8785 is informational, not an IETF Standards Track standard. It is adopted here as a deterministic project mechanism, not as a legal/platform requirement.

---

# 9. INVALIDATION GRAPH

## MINTTAP DECISION

The build/release tool must be able to answer:

> “If this fact changes, what must be reviewed?”

Examples:

### Feature becomes removed
Invalidate/review:
- claims referencing feature;
- screenshots showing feature;
- localized feature copy;
- store metadata references;
- support articles/instructions;
- structured data if capability represented;
- app page blocks.

### Processor/SDK added
Invalidate/review:
- App Data Contract;
- privacy pages/localizations;
- Apple App Privacy / Google Data safety mapping;
- Legal Trigger Registry, especially cross-border/vendor triggers;
- account/deletion consequences if applicable;
- security/CSP/domain dependencies if web SDK added.

### App UI locale added
Review:
- Locale Matrix;
- app/store/website claims;
- screenshots;
- support content;
- localization manifest;
- store metadata opportunity.

Do **not** automatically mark website translation complete just because app UI locale becomes shipped.

### Price/subscription changes
Invalidate/review:
- Product Truth;
- price-related claims;
- website qualification copy;
- store-link state;
- structured data offer fields if used;
- direct-commerce legal triggers if model changes.

### Market launch added
Invalidate/review:
- Product Truth market list;
- Legal Trigger Registry;
- privacy/legal notices;
- store availability;
- localization;
- analytics/ads/data transfer review.

---

# 10. FILE / DIRECTORY DIRECTION

Exact implementation may change, but the Foundation structure should separate schemas, canonical records, editorial content and generated state.

Provisional structure:

```text
control/
  schemas/
    v1/
      common.schema.json
      app.schema.json
      release.schema.json
      feature.schema.json
      data-practice.schema.json
      processor.schema.json
      claim.schema.json
      evidence.schema.json
      screenshot.schema.json
      locale-coverage.schema.json
      localization.schema.json
      legal-trigger.schema.json
      operational-surface.schema.json
      policy-watch.schema.json
      release-manifest.schema.json
  records/
    apps/
    releases/
    features/
    data-practices/
    processors/
    store-destinations/
    evidence/
    screenshots/
    claims/
    locales/
    localizations/
    legal-triggers/
    operational-surfaces/
    policy-watch/
  generated/
    dependency-graph.json
    validation-report.json
    impact-report.json
content/
  ko/
  en/
```

### MINTTAP DECISION

`generated/` data is reproducible output and must never become the canonical source of facts.

Whether generated files are committed to Git depends on CI/review needs; the source records remain canonical either way.

---

# 11. ONE RECORD PER FILE VS GIANT REGISTRIES

## MINTTAP DECISION

Prefer **small records / bounded collections** over one enormous global JSON object.

Benefits:
- clearer Git diffs;
- lower merge conflict risk;
- simpler ownership/review;
- easier record-level invalidation;
- more precise history.

Exceptions are reasonable for naturally tiny, tightly-coupled lists.

The runtime/build system may aggregate them into indexed structures after validation.

---

# 12. SECRETS / PERSONAL DATA BOUNDARY

## MINTTAP DECISION

The control repository is not a secret manager and not a production user database.

Never store:
- API/private keys;
- auth tokens;
- signing certificates/private keys;
- passwords;
- real customer personal data;
- raw privacy-rights requests;
- production support tickets with personal content;
- private legal advice intended to remain confidential unless repository access/storage policy explicitly supports it.

Store only:
- public identifiers when appropriate;
- secret **references/names**, never values;
- synthetic fixture data;
- approved organizational/public contact details.

Provider secret stores / CI secret systems remain the proper runtime secret location.

---

# 13. BUILD / RELEASE GATES

## Validation stages

### Stage 1 — syntax
Every JSON file parses as RFC 8259-compatible JSON.

### Stage 2 — schema
Every record passes its Draft 2020-12 schema.

### Stage 3 — repository integrity
All IDs/refs/dependency/type rules pass.

### Stage 4 — freshness
Semantic fingerprints and expiry/review dates are current.

### Stage 5 — surface generation
Generated web/store/legal/search inputs reconcile without contradiction.

### Stage 6 — release policy
No BLOCKED/P0/P1 condition prevents release; any waiver is explicit, owned and auditable.

### MINTTAP DECISION

CI should fail on structural/referential errors and defined release-blocking semantic errors.

Warnings may exist for non-blocking freshness or future-review items, but warning severity must be explicit; CI must not become a wall of ignored warnings.

---

# 14. RELEASE MANIFEST SHOULD BE PARTLY GENERATED

## SYNTHESIS

A fully manual Content Release Manifest would reintroduce the duplication this model is intended to remove.

### MINTTAP DECISION

Generate the initial release impact set from:
- Git diff of canonical records;
- dependency graph;
- semantic fingerprints;
- enabled jurisdiction/platform features.

Human reviewers then add:
- approval decisions;
- justified exceptions;
- release notes;
- evidence that cannot be inferred automatically.

The machine proposes **what needs review**; humans decide **whether the review passes**.

---

# 15. EXAMPLE CROSS-RECORD FLOW

Suppose a new release adds analytics SDK `processor:example:analytics`.

1. Engineering updates processor + data-practice records.
2. App Data Contract semantic fingerprint changes.
3. Validator computes dependents.
4. Privacy localization records become stale.
5. Apple/Google privacy disclosure mapping is marked for review.
6. Korean overseas-transfer legal trigger is re-evaluated if relevant.
7. Claim “we do not use analytics” becomes BLOCKED if present.
8. Release Manifest receives all affected surfaces automatically.
9. Release cannot close until required privacy/legal/store/web reviews pass.

This is the intended value of the control model: **one technical fact change produces the correct review fan-out.**

---

# 16. SCHEMA MIGRATION

## MINTTAP DECISION

Separate:
- `schema_version` — structure of a record;
- product/release version — app behavior;
- semantic fingerprint — meaning of a specific record instance.

When schema structure changes:
- add/migrate schema version deliberately;
- provide migration tooling or explicit manual migration procedure;
- do not reinterpret old records silently;
- validator should reject unsupported schema versions;
- migration must preserve immutable record IDs.

Do not tie schema version to app version.

---

# 17. DESIGN STUDIO HANDOFFS

## Web Design

Structured records are **inputs**, not page templates. Web Design remains free to compose different layouts/flows as long as presentation accurately represents approved facts, claims, conditions and legal controls.

Future Web implementation should expose components with stable references back to canonical IDs where practical for audit/debugging.

## Typography / Type

Structured locale/content fixtures can generate repeatable Korean/English stress datasets:
- long feature names;
- legal processor names;
- currency/date strings;
- account/delete warnings;
- support labels.

## Layout / Interaction

Data/control records can drive realistic states:
- unavailable store destination;
- stale claim;
- blocked legal trigger;
- deletion consequence;
- support error/recovery;
- locale coverage mismatch.

These are stronger interaction specimens than generic lorem ipsum states.

## Color

State records provide semantic states before visual encoding: verified/stale/blocked/retired, available/unavailable, warning/destructive/success. Color should encode these without becoming the only carrier of meaning.

---

# 18. OPEN / IMPLEMENTATION DEPENDENCIES

- exact validator implementation language/tool;
- exact JSON Schema validator and its `format` assertion behavior;
- final schema `$id` URI namespace;
- whether editorial content uses Markdown, another text format or future CMS;
- exact role/owner identity model;
- whether semantic JCS fingerprints are stored in source files or generated only;
- exact CI platform;
- Git branch/review protection model;
- how App Store / Google Play console state is imported vs manually confirmed;
- whether Firebase/Cloudflare/provider metadata can be ingested automatically;
- whether internal control records remain in `web-manager` or later move to a shared company-operations repository as scope grows.

---

## Foundation conclusion

MintTap should evolve from a set of individually correct documents into a **dependency-aware truth system**:

**canonical JSON records → JSON Schema structural validation → stable-ID referential integrity → semantic fingerprints → dependency/invalidation graph → derived release impact → human approvals → generated web/store/operations outputs.**

The single-source-of-truth rule is not “put everything in one file.” It is:

> **each fact has one canonical owner/record, and every other surface references or derives from that fact rather than re-inventing it.**

This is the data foundation required before the website can safely scale across multiple apps, locales, policies and jurisdictions.