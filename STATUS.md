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
22. **022** Protected Policy Ownership, Reviewer Quorum, Revocation & Workflow Threat Model

Canonical details: `research/001...022`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY with executable release-governance PRACTICE evidence**

Production PASS is not claimed. Provider POC, actual MintTap facts, real store-console state, legal applicability, real release operations and active CI/deployment enforcement remain incomplete.

## Executable control validation

- **016** app → feature → evidence → claim: **5/5**.
- **017** release/store, privacy/data, locale, legal trigger and operational-surface semantics: **12/12**.
- **018** semantic fingerprints and dependency impact: **5/5**.
- **019** typed dependency severity, cycles and approval freshness: **6/6**.
- **020** derived release gate + auditable waivers: **8/8**.
- **021** source/tool/policy-bound provenance, issue-class reviewer authorization, self-approval rejection and fail-closed CI: **9/9**.
- **022** protected policy ownership, reviewer quorum/revocation, time-bounded break-glass and workflow trust boundaries: **10/10**.

### 022 validated behaviors

- policy changes without designated owner approval are blocked;
- policy-owner-approved changes may proceed;
- issue classes can require quorum 2;
- inactive/revoked reviewers do not satisfy current quorum;
- release-author self-approval does not count;
- valid emergency override is separately classified `PASS / WITH_BREAK_GLASS`;
- expired/unauthorized break-glass fails closed;
- privileged `pull_request_target` or `workflow_run` paths may not execute untrusted checkout content;
- ordinary pull-request validation may process untrusted code only in a read-only/no-secret/no-deploy trust zone.

## Current control architecture

Principle: **each fact has one canonical owner/record; downstream surfaces reference or derive from it.**

Current direction:
- canonical structured data: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable IDs;
- semantic fingerprints and dependency invalidation;
- typed dependency graph with impact severity;
- fingerprint-bound approval freshness;
- cycle rejection for freshness/approval dependency graphs;
- derived release manifest and gate decision;
- exact-issue/release/source/tool/policy-bound waivers;
- issue-class reviewer authorization;
- separation of duties;
- policy-owner control over governance changes;
- reviewer quorum and revocation-aware current authorization;
- explicit time-bounded break-glass classification;
- workflow trust-zone separation;
- fail-closed release automation;
- canonical truth remains unchanged by waiver/emergency disposition;
- no secrets or customer personal data in this repository.

Practice artifacts now include:
- `control/tests/release_provenance_cases.json`
- `control/tests/policy_workflow_trust_cases.json`
- `tools/evaluate_release_provenance.py`
- `tools/evaluate_policy_workflow_trust.py`
plus the earlier 016–020 schemas/tests/tools.

Important limitation: current deterministic Python JSON serialization is still **not claimed as full RFC 8785 JCS conformance**.

## GitHub/platform evidence retained

Current primary-source findings:
- required status checks can gate merge when repository capability permits;
- CODEOWNERS can support protected path ownership but is not a substitute for issue-class authorization/quorum;
- protected environments can require reviewers and optionally prevent self-review, subject to plan/visibility constraints;
- GitHub secure-use guidance warns against privileged `pull_request_target` / `workflow_run` execution of untrusted PR content;
- `GITHUB_TOKEN` and other credentials should use least privilege;
- current private-repository capability constraints discovered in 021 mean rulesets/environment/artifact-attestation features must not be assumed available without verification.

No active GitHub Actions deployment workflow has been enabled yet.

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
Legal compliance is **facts → trigger → obligation → public/control surface → backend process → validation**, not universal boilerplate. The validator checks consistency with recorded applicability; it does not determine legal applicability itself.

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

Firebase and Cloudflare must run the same static corpus and assertion suite, including file hashes, localized pages, AASA/assetlinks/app-ads/sitemap/robots/404, headers/routing/search/social/accessibility smoke, preview/promote and provider-native rollback.

The POC remains blocked on provider accounts/domain authority.

## Current Design Studio dependencies / handoffs

- **Web Design** — still no substantive W### at latest check. Governance states are semantic inputs only; Web Design owns release/review UI hierarchy and presentation.
- **Layout / Interaction** — clean pass, pass-with-waiver, pass-with-break-glass, needs-review, blocked, stale provenance, quorum incomplete and workflow-security blocks require textual/structural/programmatic distinction, not color-only encoding.
- **Typography / Type** — long reviewer IDs, issue codes, incident references and Korean/English governance strings are stress inputs for wrapping/zoom/fallback testing.
- **Color** — severity/emergency color may reinforce but never define the state alone.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- final schemas for dependencies/approvals/manifests/waivers/reviewer policy/quorum/break-glass;
- authenticated reviewer identity mapping from GitHub/SSO;
- protected policy ownership enforcement in actual repository settings;
- revocation history/effective-time semantics;
- quorum policy ownership;
- signed/cryptographic attestation of internal manifests where justified;
- exact Git source/tree and runtime/dependency identity binding;
- trusted workflow source/pinning and reusable-workflow ownership;
- exact GitHub Actions permission matrix and fork approval behavior;
- deployment provider/OIDC credential boundary;
- rollback authorization and emergency deployment policy;
- active CI enforcement and immutable release history;
- provider accounts/domain authority and POC execution;
- final hosting/framework/CMS/monitoring choice;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Provider-neutral active-workflow trust-boundary contract.** Define exact trigger separation, token permission matrix, trusted workflow/policy ownership, fork behavior, artifact handoff, deployment credential boundary and rollback authority so it can be applied during Firebase vs Cloudflare POC without prematurely enabling deployment automation.
2. Execute Firebase Hosting vs Cloudflare Workers POC when provider accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes 001–022.
- Studies 016–022 have executable PRACTICE artifacts under `control/` and `tools/`.
- 021 canonical artifacts: `tools/evaluate_release_provenance.py`, `control/tests/release_provenance_cases.json`.
- 022 adds `tools/evaluate_policy_workflow_trust.py`, `control/tests/policy_workflow_trust_cases.json`.
- This file is the current operational checkpoint.
