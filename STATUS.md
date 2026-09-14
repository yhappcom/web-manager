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
18. **018** Semantic Fingerprints, Dependency Invalidation & Release Impact

Canonical details: `research/001...018`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable control-model PRACTICE evidence**

Production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, real store-console state, legal applicability and real release operations remain incomplete.

## Executable control validation

### 016 first slice

Implemented:

**app → feature → evidence → claim**

Result: **5 / 5 expected outcomes matched.**

### 017 release-chain extension

Expanded validation through:

**app → release → store destination → public CTA**  
**app → data practice → processor → privacy surface**  
**app → locale coverage → current locale claim**  
**legal trigger → required operational surface**  
**critical operational surface → monitoring + runbook**

Controlled re-proof result: **12 / 12 expected outcomes matched.**

### 018 semantic fingerprint / dependency impact

Implemented a separate PRACTICE tool that:
- computes a semantic projection per record;
- excludes selected operational metadata from fingerprint meaning;
- hashes deterministic serialized projections with SHA-256;
- compares before/after canonical snapshots;
- discovers canonical dependencies through `depends_on`, `*_ref` and `*_refs` fields;
- combines old and new graph edges so removals still invalidate prior dependents;
- emits `added`, `removed`, `modified`, `direct_impact`, `transitive_impact` and a derived `review_set`.

Controlled result: **5 / 5 expected outcomes matched.**

Validated behaviors:
- metadata-only timestamp change does not trigger semantic invalidation;
- JSON property-order change does not trigger semantic invalidation;
- data-practice semantic change propagates to privacy surface and then legal trigger;
- added upstream processor plus changed data-practice reference causes downstream review;
- removed upstream record preserves old dependency impact so dependents still require review.

Important limitation: the current serializer is deterministic for the constrained synthetic corpus but is **not yet claimed as full RFC 8785 JCS conformance**. Production promotion requires official/conformance-vector testing for ECMAScript number serialization, UTF-16 property ordering and I-JSON constraints.

## Current control architecture

Principle: **each fact has one canonical owner/record; downstream surfaces reference or derive from it.**

Current direction:
- canonical structured data: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable IDs;
- repository semantic linter;
- semantic fingerprints for meaningful change detection;
- dependency graph and derived non-canonical release-impact reports;
- human approval/waiver after impact derivation where required;
- no secrets or customer personal data in this repository.

Practice artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `control/tests/impact_cases.json`
- `tools/validate_control.py`
- `tools/compute_impact.py`

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

## Core product/site baselines retained

### Security
HTTPS-only direction, TLS 1.2 minimum / TLS 1.3 where supported, exact no-redirect association files, deliberate cache/security headers, secrets outside Git, auditable deployment and rollback.

### Accessibility
WCAG 2.2 AA internal target; semantic HTML; full keyboard/focus path; 320 CSS px reflow; 200% text enlargement; accessible forms/errors/status; automated tests supplement rather than replace manual evaluation.

### Localization / search / marketing
Korean/English locale-specific URLs; self-canonical + reciprocal hreflang; app UI/web/store localization tracked independently; sitemap/canonical/indexability controls; conservative structured data; Product-Truth-governed social previews and marketing claims; stale evidence invalidates dependent claims/content.

### Legal trigger model
Legal compliance is **facts → trigger → obligation → public/control surface → backend process → validation**, not universal boilerplate. The validator checks consistency with a recorded applicability state; it does not determine legal applicability itself.

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

- **Web Design** — still no substantive W### at latest check. Web Manager truth/control records and derived impact states are inputs only; Web Design owns page hierarchy, review-state presentation, CTA treatment, disclosure salience, responsive composition and browser/device validation.
- **Layout / Interaction** — latest specialist status is through L003 and I003. I003 confirms that interaction-critical states must survive authored color-channel loss. Future web review states such as `STALE`, `NEEDS_REVIEW`, `BLOCKED`, direct impact and transitive impact must therefore have textual/structural/programmatic meaning rather than color-only encoding.
- **Typography / Type** — generated Korean/English feature/legal/privacy/support/review-state strings remain useful fallback/wrapping/zoom stress inputs.
- **Color** — semantic state exists before visual encoding; color is reinforcement, not sole meaning.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion and country/region granularity;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- record-type-specific semantic projections;
- typed dependency edges and severity;
- dependency-cycle detection;
- downstream approval/freshness binding using recorded upstream fingerprints;
- localization source-revision invalidation;
- screenshot-to-release compatibility invalidation;
- derived release-manifest generation and approval/waiver flow;
- Git commit-to-snapshot automation;
- pinned validator/CI implementation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Cycle detection + typed dependency edges + approval/freshness binding.** Prove at least one downstream class (localization or claim) becomes stale/release-blocking when its recorded upstream fingerprint no longer matches, and distinguish informational impact from release-blocking impact.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–018.
- Studies 016–018 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 018 adds `tools/compute_impact.py` and `control/tests/impact_cases.json`.
- This file is the current operational checkpoint.
