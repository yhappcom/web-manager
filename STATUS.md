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
19. **019** Typed Dependency Edges, Cycle Detection & Approval Freshness

Canonical details: `research/001...019`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable control-model PRACTICE evidence**

Production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, real store-console state, legal applicability and real release operations remain incomplete.

## Executable control validation

### 016 first slice

Implemented **app → feature → evidence → claim**.

Result: **5 / 5 expected outcomes matched.**

### 017 release-chain extension

Expanded validation through release/store destination, data practice/processor/privacy, locale claims, legal triggers and critical operational surfaces.

Controlled re-proof result: **12 / 12 expected outcomes matched.**

### 018 semantic fingerprint / dependency impact

Implemented deterministic PRACTICE semantic fingerprints, before/after comparison, old+new dependency graphs and derived downstream review sets.

Controlled result: **5 / 5 expected outcomes matched.**

Validated:
- metadata-only timestamp changes do not trigger semantic invalidation;
- JSON property-order changes do not trigger semantic invalidation;
- semantic upstream changes propagate downstream;
- removed upstream records retain old dependency impact.

### 019 typed dependency / approval freshness

Implemented:
- explicit typed dependency edges: `INFORMATIONAL`, `REVIEW_REQUIRED`, `BLOCKING`;
- backward-compatible ordinary refs defaulting to `REVIEW_REQUIRED`;
- severity-aware downstream propagation;
- dependency-cycle detection;
- `approval_bindings` that record the upstream semantic fingerprint actually reviewed;
- stale-approval detection when the current upstream fingerprint differs.

Controlled result: **6 / 6 expected outcomes matched.**

Validated:
- valid approval binding remains current;
- semantic upstream change makes the approved dependent stale and blocking when edge policy is blocking;
- metadata-only change does not stale approval;
- informational impact stays informational;
- review-required impact does not become release-blocking;
- dependency cycles are mechanically detected.

Professional implication: a downstream file being marked `APPROVED` is insufficient. Approval freshness must be validated against the semantic upstream state it actually reviewed.

## Current control architecture

Principle: **each fact has one canonical owner/record; downstream surfaces reference or derive from it.**

Current direction:
- canonical structured data: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable IDs;
- repository semantic linter;
- semantic fingerprints for meaningful change detection;
- typed dependency graph with explicit impact severity;
- approval freshness bound to upstream semantic fingerprints;
- cycle rejection for freshness/approval dependency graphs;
- derived non-canonical release-impact reports;
- human approval/waiver after impact derivation where required;
- no secrets or customer personal data in this repository.

Practice artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `control/tests/impact_cases.json`
- `control/tests/dependency_governance_cases.json`
- `tools/validate_control.py`
- `tools/compute_impact.py`
- `tools/validate_dependency_governance.py`

Important limitation: current Python serialization is deterministic for the synthetic corpus but is **not yet claimed as full RFC 8785 JCS conformance**.

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
Korean/English locale-specific URLs; self-canonical + reciprocal hreflang; app UI/web/store localization tracked independently; sitemap/canonical/indexability controls; conservative structured data; Product-Truth-governed social previews and marketing claims.

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

- **Web Design** — still no substantive W### at latest check. Web Manager governance states are inputs only; Web Design owns review-state presentation, hierarchy, CTA treatment, disclosure salience, responsive composition and browser/device validation.
- **Layout / Interaction** — current evidence requires critical state meaning to survive color-channel loss. `INFORMATIONAL`, `NEEDS_REVIEW`, `BLOCKED`, stale approval and cycle/error states therefore require textual/structural/programmatic meaning rather than color-only encoding.
- **Typography / Type** — Korean/English governance labels and long release/control strings are useful fallback/wrapping/zoom stress inputs.
- **Color** — severity color may reinforce but never define the governance state by itself.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion and country/region granularity;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- schema support for typed `dependencies` and `approval_bindings`;
- record-type-specific allowed edge/severity policies;
- reviewer identity/authorization and approval expiry;
- multi-source approval policy;
- real localization and claim approval binding;
- screenshot-to-release compatibility invalidation;
- derived release-manifest generation and auditable waiver flow;
- Git commit-to-snapshot automation;
- pinned validator/CI implementation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Derived release manifest + gate decision + auditable waiver model.** Prove a synthetic release resolves to `PASS`, `NEEDS_REVIEW` or `BLOCKED` from semantic integrity, cycles, typed impacts and approval freshness, and prove a waiver cannot silently rewrite canonical truth.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–019.
- Studies 016–019 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 019 adds `tools/validate_dependency_governance.py` and `control/tests/dependency_governance_cases.json`.
- This file is the current operational checkpoint.
