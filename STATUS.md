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
20. **020** Derived Release Manifest, Gate Decision & Auditable Waivers

Canonical details: `research/001...020`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable release-control PRACTICE evidence**

Production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, real store-console state, legal applicability, real release operations, reviewer authorization and CI enforcement remain incomplete.

## Executable control validation

### 016 first slice
Implemented **app → feature → evidence → claim**. Result: **5 / 5 expected outcomes matched.**

### 017 release-chain extension
Expanded validation through release/store destination, data practice/processor/privacy, locale claims, legal triggers and critical operational surfaces. Result: **12 / 12 expected outcomes matched.**

### 018 semantic fingerprint / dependency impact
Implemented deterministic PRACTICE semantic fingerprints, before/after comparison, old+new dependency graphs and derived downstream review sets. Result: **5 / 5 expected outcomes matched.**

### 019 typed dependency / approval freshness
Implemented typed dependency severity, cycle detection and upstream-fingerprint-bound approval freshness. Result: **6 / 6 expected outcomes matched.**

### 020 derived release manifest / gate / waiver

Implemented `tools/evaluate_release_gate.py` and `control/tests/release_gate_cases.json`.

The derived release manifest consumes governance findings and resolves a synthetic release to:
- `PASS`;
- `NEEDS_REVIEW`;
- `BLOCKED`.

For `PASS`, it separately records:
- `CLEAN`;
- `WITH_WAIVER`.

Controlled result: **8 / 8 expected outcomes matched.**

Validated:
- clean release → `PASS / CLEAN`;
- informational-only impact → `PASS / CLEAN`;
- unresolved review-required item → `NEEDS_REVIEW`;
- stale blocking approval → `BLOCKED`;
- dependency cycle → non-waivable `BLOCKED`;
- valid, release-scoped, approved, reasoned and unexpired waiver over an explicitly waivable exact issue fingerprint → `PASS / WITH_WAIVER`;
- expired waiver → remains `BLOCKED`;
- semantic integrity failure → non-waivable `BLOCKED`.

Critical rule: **a waiver never deletes or rewrites the canonical issue.** The manifest retains `canonical_issues`, records `waivers_applied`, and derives `unresolved_issues` separately.

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
- derived release manifest and gate decision;
- explicit waiver audit record bound to one release and one exact issue fingerprint;
- canonical truth remains unchanged by waiver;
- no secrets or customer personal data in this repository.

Practice artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `control/tests/impact_cases.json`
- `control/tests/dependency_governance_cases.json`
- `control/tests/release_gate_cases.json`
- `tools/validate_control.py`
- `tools/compute_impact.py`
- `tools/validate_dependency_governance.py`
- `tools/evaluate_release_gate.py`

Important limitation: current Python serialization is deterministic for the synthetic corpus but is **not yet claimed as full RFC 8785 JCS conformance**.

## Source/provenance note

SLSA 1.2 treats provenance as verifiable information connecting artifacts to where, when and how they were produced, and its build requirements use cryptographic digests to identify output packages.

MintTap uses that as useful provenance design evidence only. SLSA does **not** define MintTap's `PASS / NEEDS_REVIEW / BLOCKED` gate or waiver policy; those remain project-specific governance decisions.

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

- **Web Design** — still no substantive W### at latest check. Release manifest states are semantic inputs only; Web Design owns how clean pass, pass-with-waiver, needs-review and blocked states are presented.
- **Layout / Interaction** — `PASS / CLEAN`, `PASS / WITH_WAIVER`, `NEEDS_REVIEW`, `BLOCKED`, invalid waiver and non-waivable failure require textual/structural/programmatic distinction, not color-only encoding.
- **Typography / Type** — long waiver reasons, release identifiers, issue codes and Korean/English governance strings should later be used as wrapping/zoom/fallback stress content.
- **Color** — severity color may reinforce, but a waiver or blocker must remain understandable with authored color removed.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion and country/region granularity;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- schema support for typed `dependencies`, `approval_bindings`, release manifests and waiver records;
- record-type-specific allowed edge/severity/waiver policies;
- reviewer identity, authorization, separation-of-duties and approval expiry;
- cryptographic/authenticated attestation of manifest/waiver provenance;
- multi-source approval policy;
- real localization and claim approval binding;
- screenshot-to-release compatibility invalidation;
- Git commit-to-snapshot automation;
- pinned validator/CI implementation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Manifest/waiver provenance + reviewer authorization + CI enforcement model.** Define who may approve/waive which issue classes, bind decisions to source snapshot/commit and tool version, and prove unauthorized or stale attestations cannot produce a release `PASS`.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–020.
- Studies 016–020 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 020 adds `tools/evaluate_release_gate.py` and `control/tests/release_gate_cases.json`.
- This file is the current operational checkpoint.
