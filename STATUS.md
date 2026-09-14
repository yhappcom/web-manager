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
17. **017** Release-Chain Semantic Integrity Validation

Canonical details: `research/001...017`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable control-model PRACTICE evidence**

Production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, real store-console state, legal applicability and real release operations remain incomplete.

## Executable control validation

### 016 first slice

Study 016 implemented:

**app → feature → evidence → claim**

and documented schema failure → revision → re-proof.

Result: **5 / 5 expected outcomes matched.**

### 017 release-chain extension

Study 017 expanded the same validator through:

**app → release → store destination → public CTA**  
**app → data practice → processor → privacy surface**  
**app → locale coverage → current locale claim**  
**legal trigger → required operational surface**  
**critical operational surface → monitoring + runbook**

Current synthetic record types:
- `app`, `feature`, `evidence`, `claim`;
- `release`, `store_destination`;
- `processor`, `data_practice`;
- `locale_coverage`;
- `legal_trigger`;
- `operational_surface`.

Controlled re-proof result: **12 / 12 expected outcomes matched.**

The current validator detects:
- malformed records;
- missing/wrong cross-record references;
- current claim over non-shipped feature;
- stale evidence supporting current claim;
- store CTA to unavailable destination;
- store destination without a verified live same-platform release;
- app-UI locale claim contradicted by locale coverage;
- verified privacy surface backed by stale data practice;
- applicable legal trigger without required control surface;
- P0/P1 operational surface without monitoring/runbook;
- data practice referencing a missing processor.

Professional implication: a public surface is not current merely because its own file is valid. Structural validity and repository-wide product/operational semantics remain separate validation layers.

## Store-distribution evidence update

Current Apple App Store Connect and Google Play primary documentation confirms that app availability is a separate country/region-controlled operational fact. Therefore a stored store URL alone is not proof that a MintTap download CTA is currently valid.

Current simplified semantic rule:

**STORE_CTA → AVAILABLE destination + VERIFIED LIVE same-app/same-platform release.**

Production modeling must later add territory, track, device/account eligibility and external verification timestamp where materially needed.

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

Direction:
- canonical structured data: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable IDs;
- repository semantic linter;
- semantic fingerprints + dependency invalidation for freshness;
- generated release-impact reports, then human approvals;
- no secrets or customer personal data in this repository.

Practice artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `tools/validate_control.py`

## Core product/site baselines retained

### Security
HTTPS-only direction, TLS 1.2 minimum / TLS 1.3 where supported, exact no-redirect association files, deliberate cache/security headers, secrets outside Git, auditable deployment and rollback.

### Accessibility
WCAG 2.2 AA internal target; semantic HTML; full keyboard/focus path; 320 CSS px reflow; 200% text enlargement; accessible forms/errors/status; automated tests supplement rather than replace manual evaluation.

### Localization / search / marketing
Korean/English locale-specific URLs; self-canonical + reciprocal hreflang; app UI/web/store localization tracked independently; sitemap/canonical/indexability controls; conservative structured data; Product-Truth-governed social previews and marketing claims; stale evidence invalidates dependent claims/content.

The executable model now has a first guard against a website claim implying shipped app-UI locale support when canonical locale coverage says otherwise.

### Legal trigger model
Legal compliance is **facts → trigger → obligation → public/control surface → backend process → validation**, not universal boilerplate. Korea PIPA/direct-commerce, U.S. FTC/COPPA/CCPA/other-state and conditional EU GDPR triggers remain dependent on actual MintTap facts.

The validator checks consistency with a recorded `APPLIES` state; it does not determine legal applicability itself.

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

Firebase and Cloudflare must run the same static corpus and assertion suite, including file hashes, localized pages, AASA/assetlinks/app-ads/sitemap/robots/404, response headers/routing/search/social/accessibility smoke, preview/promote and provider-native rollback.

The POC remains blocked on provider accounts/domain authority.

## Current Design Studio dependencies / handoffs

- **Web Design** — still no substantive W001 at latest check. Control records provide truthful states; Web Design owns page hierarchy, CTA treatment, disclosure salience, responsive composition and browser/device validation.
- **Typography / Type** — use generated Korean/English feature/legal/privacy/support strings for fallback/wrapping/zoom stress.
- **Layout / Interaction** — latest status has advanced through L003/I002. Consume canonical states such as store unavailable, privacy stale/blocked, locale unsupported/planned and P0 failure/recovery rather than disconnected mock states.
- **Color** — semantic states exist before visual encoding; color cannot be the sole carrier of meaning.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion and country/region granularity;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- semantic fingerprint implementation and deterministic canonicalization;
- dependency graph / derived release-impact generation;
- localization source-revision invalidation;
- screenshot-to-release compatibility;
- dependency-cycle detection and schema migrations;
- pinned validator/CI implementation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Semantic fingerprint + dependency/invalidation + derived release-impact validation.** Change one upstream canonical record, distinguish semantic from formatting-only changes, compute downstream records needing review and emit a non-canonical impact report.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–017.
- Studies 016–017 have executable practice artifacts under `control/` and `tools/`.
- This file is the current operational checkpoint.
