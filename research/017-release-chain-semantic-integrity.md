# 017 — Release-Chain Semantic Integrity Validation

Status: **PRACTICE / CONTROLLED CROSS-RECORD RE-PROOF COMPLETED**  
Research date: **2026-09-14**

## Question

Can the Study 015/016 control model prevent a website release from presenting a coherent-looking but operationally false state across app release, store availability, privacy/data processing, localization, legal triggers and monitored public surfaces?

Study 016 proved the narrow chain:

**app → feature → evidence → claim**.

Study 017 extends that proof through the next high-value release chain:

**app → release → store destination → public CTA**  
**app → data practice → processor → privacy surface**  
**app → locale coverage → localized product claim**  
**legal trigger → required operational surface**  
**critical operational surface → monitoring + runbook**

All records remain synthetic research fixtures. They are not MintTap production facts.

---

# SOURCE — current store availability is a separate operational fact

Apple App Store Connect currently manages app availability by country/region and exposes availability status per country/region. Apple states that availability changes may take up to 24 hours to become visible to all users.

Primary source, checked 2026-09-14:
- https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-for-your-app-on-the-app-store

Google Play similarly distinguishes production app availability from country targeting and manages countries/regions from the Production track.

Primary source, checked 2026-09-14:
- https://support.google.com/googleplay/android-developer/answer/7550024

### SYNTHESIS

A stored App Store / Play URL is not sufficient proof that MintTap should render an active download CTA.

A public current CTA needs at least:
- a destination whose availability is currently acceptable for the intended surface; and
- a compatible live release for the same app/platform.

Country/device/account-specific real-world visibility still requires external store validation; the repository cannot prove every user's store eligibility from static records alone.

### MINTTAP DECISION

The validator now rejects:
- `STORE_DESTINATION_UNAVAILABLE`; and
- `STORE_DESTINATION_NO_LIVE_RELEASE`.

This prevents a known unavailable destination or a destination without a verified live same-platform release from silently becoming a current CTA.

---

# SOURCE — JSON Schema remains structural, not cross-record product truth

JSON Schema Draft 2020-12 defines validation vocabulary and `unevaluatedProperties` behavior. It validates an instance against a schema; MintTap's repository-wide business relationships remain application-level semantics.

Primary source, checked 2026-09-14:
- https://json-schema.org/draft/2020-12
- https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-00

### SYNTHESIS

The 016 architecture remains correct after extension:

**JSON parse → Draft 2020-12 structural validation → repository-wide semantic integrity validation**.

No attempt is made to encode every cross-file relationship in JSON Schema.

---

# IMPLEMENTED EXTENSION

## Schema record types now exercised

`control/schemas/v1/record.schema.json` now recognizes:
- `app`;
- `feature`;
- `evidence`;
- `claim`;
- `release`;
- `store_destination`;
- `processor`;
- `data_practice`;
- `locale_coverage`;
- `legal_trigger`;
- `operational_surface`.

## New synthetic valid baseline records

Added:
- `control/records/releases/example-ios-1.0.0.json`;
- `control/records/store-destinations/example-ios.json`;
- `control/records/processors/example-cloud.json`;
- `control/records/data-practices/example-analytics.json`;
- `control/records/locales/example-ko.json`;
- `control/records/surfaces/example-privacy.json`;
- `control/records/surfaces/example-store-ios.json`;
- `control/records/legal/example-privacy.json`.

Combined with the existing 016 fixtures, the valid graph now includes:

```text
app:example [ACTIVE]
├─ feature:example:portfolio [SHIPPED]
│  └─ claim:example:portfolio-overview [CURRENT]
│     └─ evidence:example:portfolio-release [VERIFIED]
├─ release:example:ios:1.0.0 [IOS / LIVE]
│  └─ store:example:ios [AVAILABLE]
│     └─ surface:example:store-ios [STORE_CTA / P1]
├─ processor:example:cloud [VERIFIED]
│  └─ data:example:analytics [VERIFIED]
│     └─ surface:example:privacy [PRIVACY / P1]
│        └─ legal:example:privacy [APPLIES]
└─ locale:example:ko [app UI SUPPORTED / web SUPPORTED]
```

---

# SEMANTIC RULES ADDED

## Release / store

- a `LIVE` release must reference an existing app;
- a current store CTA must reference a `store_destination`;
- that destination must be `AVAILABLE`;
- a verified `LIVE` release must exist for the destination's same app/platform.

## Data / privacy

- each `data_practice.processor_refs` entry must resolve to a `processor`;
- a `VERIFIED` operational surface that cites `source_refs` may not rely on a stale/unverified source;
- privacy therefore cannot remain approved while its canonical data-practice source is `STALE`.

This is deliberately a provenance rule, not a claim that the current simple `data_practice` schema is a complete privacy-law data model.

## Locale / claims

A `CURRENT` claim may optionally reference `locale_coverage` records. If it does, a claim implying shipped UI locale support requires `app_ui = SUPPORTED`.

This directly protects the prior rule that website/store localization must not be confused with app UI localization.

## Legal trigger / required controls

When `legal_trigger.applicability = APPLIES`:
- at least one required surface must be declared when the trigger model requires a public/control surface;
- referenced surfaces must exist;
- referenced surfaces must be `VERIFIED`.

The validator determines consistency with the recorded trigger state. It does **not** determine whether the law actually applies; that still requires the factual/legal analysis defined in Study 013.

## Operational reliability

P0/P1 surfaces require:
- monitoring other than `NONE`; and
- a non-empty `runbook_ref`.

The repository stores the runbook reference, not operational secrets.

---

# CONTROLLED RE-PROOF

The exact current schema, synthetic baseline, validator behavior and test definitions were mirrored and executed with Python `jsonschema` Draft 2020-12 validation.

Result:

```text
12 / 12 expected outcomes matched
```

## Passing baseline

The expanded valid repository graph produced no structural or semantic error.

## Expected failure cases

1. missing required claim evidence → `schema:SCHEMA_INVALID`
2. missing feature reference → `semantic:MISSING_REF`
3. current claim over planned feature → `semantic:CURRENT_CLAIM_NOT_SHIPPED`
4. current claim backed by stale evidence → `semantic:EVIDENCE_NOT_VERIFIED`
5. store CTA points to unavailable destination → `semantic:STORE_DESTINATION_UNAVAILABLE`
6. available Android destination without verified live Android release → `semantic:STORE_DESTINATION_NO_LIVE_RELEASE`
7. current Korean-UI claim with app UI marked unsupported → `semantic:CURRENT_LOCALE_CLAIM_UNSUPPORTED`
8. verified privacy surface sourced from stale data practice → `semantic:SURFACE_SOURCE_NOT_VERIFIED`
9. applicable legal trigger with no required surface → `semantic:LEGAL_TRIGGER_MISSING_SURFACE`
10. P0 surface without active monitoring/runbook → `semantic:CRITICAL_SURFACE_UNCONTROLLED`
11. data practice references missing processor → `semantic:MISSING_REF`

Plus the valid baseline gives twelve expected outcomes total.

Test definitions:
- `control/tests/cases.json`

Validator:
- `tools/validate_control.py`

---

# WHAT THIS VALIDATES

## VALIDATION — confirmed at controlled specimen level

The repository can now mechanically catch several classes of cross-channel drift **before rendering public content**:

- website download CTA vs actual recorded distribution state;
- website locale promise vs recorded app UI coverage;
- privacy page approval vs data-practice freshness;
- applicable legal trigger vs required public/control surface;
- critical surface vs operational ownership/monitoring discipline;
- data practice vs processor inventory.

This is materially stronger than manually reviewing separate markdown pages.

## SYNTHESIS — public-page generation should consume validated records

The next implementation should avoid generating a current CTA, localization badge, privacy statement or legal-control link directly from free-form page content when a canonical control record exists.

Preferred pipeline:

```text
canonical records
  → schema validation
  → semantic integrity validation
  → derived release-impact / build inputs
  → generated/rendered public surfaces
  → deployment/browser/store validation
```

A build should stop before rendering/deployment for release-blocking semantic failures.

---

# LIMITS / OPEN QUESTIONS

This is still **PRACTICE**, not production PASS.

Not yet proven:
- real App Store Connect / Play Console ingestion;
- country-specific destination state rather than one simplified availability enum;
- device compatibility / account-country visibility;
- release-build IDs and screenshot-to-release compatibility;
- actual App Data Contract detail: categories, purposes, sharing, retention, deletion, SDK behavior, controller/processor roles;
- overseas-transfer legal evaluation;
- localization source revision/fingerprint staleness;
- generated Content Release Manifest / dependency impact;
- policy records and effective-date gates;
- dependency-cycle detection;
- schema migrations;
- CI execution from the GitHub repository itself;
- ownership identity registry;
- real runbook existence/access checks;
- real MintTap app records.

## OPEN — availability needs finer granularity

The current `store_destination.availability_state` is intentionally simplified. Apple and Google availability can vary by country/region; Google can also have track distinctions and device eligibility consequences.

A production model should likely separate:
- public destination identity/URL;
- platform release state;
- country/region availability;
- distribution method/track where material;
- last external verification timestamp.

Do not prematurely encode every store-console field until the first real app integration establishes what the website/release process actually needs.

---

# DESIGN STUDIO DEPENDENCIES / HANDOFFS

## Web Design

Web Design remains at pre-W001 substantive baseline, so no visual pattern is inferred.

The validator can now provide truthful input states such as:
- download available / unavailable;
- locale supported / unsupported / planned;
- privacy information current / stale;
- required legal/control surface present / blocked.

Web Design should decide how these states affect page hierarchy, messaging, CTA presentation and responsive behavior. It should not redefine the underlying truth state.

## Layout / Interaction

Current Design Studio Layout/Interaction work has progressed through L003/I002 and explicitly separates state semantics from presentation. This validator provides canonical state conditions suitable for future real-browser interaction specimens.

High-value transfer scenarios:
- store CTA becomes unavailable after a release/territory change;
- privacy/support surface is blocked before launch;
- locale selector leads to web content even though app UI locale is unavailable;
- P0 account/privacy control has a failure/recovery state.

## Typography / Color

- locale/legal/privacy records can generate realistic long Korean/English labels for wrapping/reflow tests;
- unavailable/stale/blocked/verified remain semantic states before Color encoding;
- status meaning must not rely on color alone.

---

# NEXT HIGHEST-VALUE VALIDATION

The next non-blocked research should implement **derived release impact / staleness propagation** rather than add more disconnected record types.

Required proof:
1. calculate dependency edges from canonical records;
2. change one upstream record semantically;
3. automatically identify downstream claims/surfaces/localizations/releases requiring review;
4. distinguish semantic change from formatting-only change;
5. generate a release-impact report without making that report canonical truth.

This directly tests Study 015's proposed semantic fingerprint/invalidation model and closes the gap between record validation and actual release governance.

Provider deployment POC remains blocked on provider accounts/domain authority and therefore is not the highest-value executable task available inside the repository alone.

## Result

Study 016's structural-vs-semantic architecture successfully transferred from a four-record marketing slice to a broader app-release operating chain.

The central finding is:

> **A public MintTap surface should not be considered current merely because its own file is valid. It must remain consistent with the release, distribution, privacy/data, locale, legal and operational records it depends on.**
