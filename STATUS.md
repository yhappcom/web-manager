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
21. **021** Release Provenance, Reviewer Authorization & Fail-Closed CI

Canonical details: `research/001...021`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable release-control PRACTICE evidence**

Production PASS is not claimed. Provider POC, browser/device validation, actual MintTap facts, real store-console state, legal applicability, real deployment operations, authenticated reviewer identities, protected policy ownership and active CI enforcement remain incomplete.

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
Implemented `PASS / NEEDS_REVIEW / BLOCKED`, `PASS / CLEAN` vs `PASS / WITH_WAIVER`, exact issue-fingerprint waiver scope, expiry and non-waivable integrity failures. Result: **8 / 8 expected outcomes matched.**

Critical 020 rule: a waiver never deletes or rewrites the canonical issue.

### 021 release provenance / reviewer authorization / CI

Implemented `tools/evaluate_release_provenance.py` and `control/tests/release_provenance_cases.json`.

Added:
- issue-class-specific reviewer authorization policy;
- policy version binding;
- release-author vs approver separation of duties;
- waiver binding to exact source commit and normalized source snapshot digest;
- manifest provenance with evaluator name/version and evaluation-input digest;
- stale supplied-attestation detection;
- separate governance `decision` and deployment/CI `ci_state`;
- command exit `0` only for `ci_state=ALLOW`.

Controlled result: **9 / 9 expected outcomes matched.**

Validated:
- authorized/current waiver → `PASS / WITH_WAIVER`, CI `ALLOW`;
- unknown reviewer → `BLOCKED`, CI `FAIL`;
- known reviewer without authority for that issue class → `BLOCKED`, CI `FAIL`;
- waiver tied to old source commit → `BLOCKED`, CI `FAIL`;
- waiver tied to old normalized snapshot → `BLOCKED`, CI `FAIL`;
- self-approval by release author → rejected;
- clean current release → `PASS / CLEAN`, CI `ALLOW`;
- unresolved `NEEDS_REVIEW` → CI `FAIL`;
- otherwise-clean release with stale evaluator-version attestation → canonical decision `PASS`, CI `FAIL`.

Professional implication: **truth state and authority-to-release are separate dimensions.** A release can be semantically clean while still lacking current trusted provenance, and must then fail closed.

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
- reviewer authorization by issue class and versioned policy;
- self-approval rejection for waiver-based release passage;
- release/waiver binding to source commit + normalized snapshot digest;
- evaluator/tool/input provenance in the manifest;
- CI/deployment authorization separated from canonical truth;
- canonical truth remains unchanged by waiver;
- no secrets or customer personal data in this repository.

Practice artifacts:
- `control/schemas/v1/record.schema.json`
- synthetic records under `control/records/`
- `control/tests/cases.json`
- `control/tests/impact_cases.json`
- `control/tests/dependency_governance_cases.json`
- `control/tests/release_gate_cases.json`
- `control/tests/release_provenance_cases.json`
- `tools/validate_control.py`
- `tools/compute_impact.py`
- `tools/validate_dependency_governance.py`
- `tools/evaluate_release_gate.py`
- `tools/evaluate_release_provenance.py`

Important limitation: current Python serialization is deterministic for the synthetic corpus but is **not yet claimed as full RFC 8785 JCS conformance**.

## Current GitHub capability reality

Verified 2026-09-14:
- `yhappcom/web-manager` is **private**;
- default branch is `main`;
- repository creation time is `2026-09-14T07:34:58Z`;
- repository rulesets endpoint currently returns an upgrade/public-repository requirement, so rulesets are not an evidenced enforcement mechanism for the present repository state;
- branch-protection state could not be inspected with the installed GitHub integration because that endpoint is not accessible to the integration; this is not proof that branch protection itself is unavailable.

Current GitHub documentation also states:
- rulesets can require status checks and can constrain a required status source to a specific GitHub App;
- protected environments can require reviewers and can prevent self-review, with plan/repository-visibility restrictions;
- artifact attestations include workflow/repository/environment/commit provenance and use Sigstore;
- private/internal repository artifact attestations require Enterprise Cloud, so they are not assumed as the current baseline;
- GitHub Actions OIDC exposes source/workflow claims, and repositories created after 2026-07-15 use immutable default subject claims containing owner/repository IDs;
- full-length commit-SHA pinning is GitHub's documented immutable way to consume actions.

Portable baseline: the repository's own evaluator must fail non-zero unless release authorization is current; GitHub-native required checks/environment approvals/attestations are additive hardening when actually supported and verified.

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

- **Web Design** — still no substantive W### at latest check. Governance/release/provenance states are semantic inputs only; Web Design owns how they are presented.
- **Layout / Interaction** — release decision, CI authorization, reviewer authorization, stale source/attestation, clean pass, waiver pass, review-needed and blocker states require textual/structural/programmatic distinction, not color-only encoding.
- **Typography / Type** — reviewer names/roles, commit IDs, digest strings, issue codes and Korean/English audit reasons should later be used as wrapping/zoom/fallback stress content.
- **Color** — severity/authority color may reinforce but never define release meaning by itself.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion and country/region granularity;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- schemas for typed dependencies, approvals, release manifests, waivers and reviewer policies;
- protected ownership/change control for reviewer policy and gate code;
- authenticated GitHub identity mapping for reviewers;
- quorum/two-person approval for selected issue classes;
- reviewer and waiver revocation;
- break-glass/emergency exception model;
- cryptographic signature/attestation for internal manifest;
- actual GitHub Actions gate workflow and threat-model validation;
- required status-check/branch-protection enforcement verification;
- OIDC claim observation and deployment-provider trust configuration;
- multi-source approval policy;
- real localization and claim approval binding;
- screenshot-to-release compatibility invalidation;
- Git commit-to-snapshot automation;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Protected policy ownership + reviewer quorum/revocation + workflow threat model.** Prove selected issue classes require independent authorized approvers, revoked authority becomes ineffective, emergency overrides are explicit/time-bounded, and untrusted PR code cannot alter the gate or obtain deployment authority.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–021.
- Studies 016–021 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 021 adds `tools/evaluate_release_provenance.py` and `control/tests/release_provenance_cases.json`.
- This file is the current operational checkpoint.
