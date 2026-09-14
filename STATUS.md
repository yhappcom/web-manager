# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager owns MintTap company website content, app-launch web requirements and operational consistency. GitHub is canonical long-term memory; chat is temporary working context. Self-directed study continues when no live assignment takes priority.

## Completed foundation / practice studies

1. **001** App Launch Website Foundations
2. **002** Multi-App Information Architecture
3. **003** Privacy / Support / Account Deletion
4. **004** Store ↔ Website Synchronization
5. **005** Domain / Hosting / Security
6. **006** Accessibility Production Baseline
7. **007** Localization Architecture
8. **008** SEO / Structured Data / Crawlability
9. **009** SEO Independent Verification / Social Preview
10. **010** Company / App Marketing Content Model
11. **011** Operational Release & Change-Watch Controls
12. **012** Implementation / Hosting Provider Comparison Methodology
13. **013** Jurisdiction-Specific Legal / Compliance Trigger Map
14. **014** Provider POC Specification
15. **015** Machine-Readable Control Artifacts / Single Source of Truth
16. **016** Control Artifact Validation Specimen

Canonical details: `research/001...016`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with first executable control-model PRACTICE evidence**

The knowledge architecture is broad enough to guide a real site, but production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, store association, legal applicability and real release operations remain incomplete.

## 016 executable evidence

Study 016 implemented a limited vertical slice:

**app → feature → evidence → claim**

Artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `tools/validate_control.py`

### Failure → revision → re-proof

Initial schema design incorrectly placed `unevaluatedProperties: false` inside the subtype branch of an `allOf`, causing valid shared base properties to be rejected.

Revision:
- move `unevaluatedProperties: false` to the schema object wrapping the complete `allOf` evaluation.

Re-proof result using the exact specimen content:
- valid baseline → PASS;
- claim missing required evidence → `SCHEMA_INVALID`;
- claim references nonexistent feature → `MISSING_REF`;
- CURRENT claim references PLANNED feature → `CURRENT_CLAIM_NOT_SHIPPED`;
- claim relies on STALE evidence → `EVIDENCE_NOT_VERIFIED`.

**5 / 5 expected outcomes matched.**

Professional implication: JSON/JSON Schema validity does not establish product truth. Structural validation and repository-wide semantic validation must remain separate layers.

## Current public information architecture

Preferred localized pattern:
- `/ko/`, `/en/`
- `/ko/apps/`, `/en/apps/`
- `/ko/apps/<app-slug>/`, `/en/apps/<app-slug>/`
- localized app `support/`, `privacy/`, `account-deletion/` where applicable.

Machine endpoints:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

Root `/` strategy remains OPEN.

## Internal truth / control model

Principle: **each fact has one canonical owner/record; downstream surfaces reference or derive from it.**

Planned record families:
- app / release / feature;
- data-practice / processor;
- store-destination;
- evidence / screenshot;
- claim;
- locale-coverage / localization;
- legal-trigger;
- operational-surface;
- policy-watch;
- derived release-manifest.

Direction:
- canonical structured data: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable IDs;
- repository semantic linter;
- semantic fingerprint / dependency invalidation for freshness;
- generated impact reports, then human approvals;
- no secrets or customer personal data in this repository.

## Core product/site baselines retained

### Security
HTTPS-only direction, TLS 1.2 minimum / TLS 1.3 where supported, exact no-redirect association files, deliberate cache/security headers, secrets outside Git, auditable deployment and rollback.

### Accessibility
WCAG 2.2 AA internal target; semantic HTML; full keyboard/focus path; 320 CSS px reflow; 200% text enlargement; accessible forms/errors/status; automated tests supplement rather than replace manual evaluation.

### Localization / search / marketing
Korean/English locale-specific URLs; self-canonical + reciprocal hreflang; app UI/web/store localization tracked independently; sitemap/canonical/indexability controls; conservative structured data; Product-Truth-governed social previews and marketing claims; stale evidence invalidates dependent claims/content.

### Legal trigger model
Legal compliance is **facts → trigger → obligation → public/control surface → backend process → validation**, not universal boilerplate. Korea PIPA/direct-commerce, U.S. FTC/COPPA/CCPA/other-state and conditional EU GDPR triggers remain dependent on actual MintTap entity/market/audience/data/transaction facts.

### Operations
Policy Change Register + Operational Surface Registry; deploy-time, scheduled, event-driven and human freshness checks; release does not close until production/store/web/control surfaces are revalidated.

## Current implementation direction

Preferred envelope:

**Git-versioned content/data → build-time static generation → global HTTPS/CDN hosting → isolated dynamic functions only for genuine server workflows.**

Provider shortlist:
1. Firebase Hosting;
2. Cloudflare Workers + Static Assets;
3. Vercel if justified SSR/full-stack need appears;
4. Netlify as viable static alternative.

No provider selected.

### Provider POC gate

Firebase and Cloudflare must run the same static corpus and assertion suite, including:
- file hashes;
- localized pages;
- AASA / assetlinks / app-ads / sitemap / robots / real 404;
- status/MIME/redirect/cache/security headers;
- canonical/hreflang/Open Graph/noindex;
- keyboard/200%/320px smoke;
- V1 → V2 preview → promote → provider-native rollback;
- rollback of content + headers + redirects + machine endpoints.

## Current Design Studio dependencies / handoffs

- **Web Design** — control records are truth inputs, not page hierarchy; neutral POC styling is not final design.
- **Typography / Type** — use generated Korean/English feature/legal/support strings for browser fallback/wrapping/zoom stress.
- **Layout / Interaction** — consume real semantic states such as unavailable, stale, blocked, delete, error and recovery rather than disconnected mock states.
- **Color** — semantic states exist before visual encoding; color cannot be the sole carrier of meaning.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- expanded schemas for release/store/data/locale/legal/operational records;
- semantic fingerprint and dependency graph implementation;
- pinned validator/CI implementation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Expand executable control validation** through release, store destination, processor/data practice, locale/localization, legal trigger and operational-surface records; then derive release impact.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–016.
- Study 016 has executable practice artifacts under `control/` and `tools/`.
- This file is the current operational checkpoint.
