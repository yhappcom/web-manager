# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager owns MintTap company website content, app-launch web requirements and operational consistency. GitHub is canonical long-term memory; chat is temporary working context. Self-directed study continues when no live assignment takes priority.

## Completed foundation / practice studies

Studies **001–023** are complete at the documented Foundation/PRACTICE level. Canonical details are under `research/` and indexed in `research/README.md`.

Latest sequence:
- **016** Control Artifact Validation Specimen — 5/5;
- **017** Release-Chain Semantic Integrity — 12/12;
- **018** Semantic Fingerprints / Dependency Impact — 5/5;
- **019** Typed Dependency / Approval Freshness — 6/6;
- **020** Derived Release Gate / Auditable Waivers — 8/8;
- **021** Release Provenance / Reviewer Authorization / Fail-Closed CI — 9/9;
- **022** Protected Policy Ownership / Quorum / Revocation / Workflow Threat Model — 10/10;
- **023** Provider-Neutral Active Workflow Trust-Boundary Contract — 12/12.

Production PASS is not claimed. Actual MintTap facts, real store-console state, legal applicability, provider accounts/domain authority, live CI/deployment enforcement and browser/device production validation remain incomplete.

## 023 — provider-neutral active workflow contract

New artifacts:
- `research/023-provider-neutral-active-workflow-trust-boundary.md`
- `tools/validate_active_workflow_contract.py`
- `control/tests/active_workflow_contract_cases.json`

Controlled result: **12 / 12 expected outcomes matched.**

The future release workflow is divided into four trust zones:

1. **PR_VALIDATE** — `pull_request`, may execute untrusted code, baseline `contents: read`, no secrets, no OIDC, no deployment authority.
2. **TRUSTED_BUILD** — protected accepted source only; no untrusted PR checkout execution and no deployment credential; outputs digest-bound deployable artifact.
3. **DEPLOY** — requires release manifest `ci_state=ALLOW`, protected workflow/policy source, trusted-build artifact origin and exact approved digest; deployment credential exists only here.
4. **ROLLBACK** — trusted manual action selecting a previously approved immutable artifact digest; no rebuild of current source.

Credential modes:
- `OIDC_SHORT_LIVED` is preferred when the selected provider supports and validates it;
- `ENVIRONMENT_SCOPED_SECRET` is the provider-neutral fallback and must remain deploy-job scoped.

Critical rule: **PR workflow artifacts are test evidence, not deployable release artifacts.** Deployment must follow accepted source → trusted build → artifact digest → release manifest ALLOW → exact digest deployment.

GitHub's built-in artifact digest validation documents a mismatch as a warning. MintTap's release contract is intentionally stricter: an approved-manifest/artifact digest mismatch is release-blocking.

## Current control architecture

Principle: **each fact has one canonical owner/record; downstream surfaces reference or derive from it.**

Current direction includes:
- canonical JSON + JSON Schema;
- stable immutable IDs;
- semantic fingerprints and dependency invalidation;
- typed impact severity and cycle rejection;
- fingerprint-bound approvals;
- derived release manifest and `PASS / NEEDS_REVIEW / BLOCKED` gate;
- exact-issue/release/source/tool/policy-bound waivers;
- reviewer authorization, quorum, revocation and separation of duties;
- protected governance ownership;
- explicit time-bounded break-glass handling;
- source/tool/input provenance and fail-closed CI semantics;
- four-zone workflow trust separation;
- artifact-digest deployment binding;
- credential isolation to deploy/rollback;
- canonical truth remains unchanged by waiver/emergency disposition;
- no secrets or customer personal data in this repository.

Important limitation: current deterministic Python JSON serialization is still **not claimed as full RFC 8785 JCS conformance**.

## Current GitHub/platform evidence

Verified/retained current primary-source findings:
- privileged `pull_request_target` and `workflow_run` flows must not execute untrusted PR content or blindly trust artifacts originating from untrusted workflows;
- least-privilege `GITHUB_TOKEN` permissions are required;
- CODEOWNERS/branch protection can protect sensitive workflow/policy changes when repository capability permits;
- protected environments can gate deployment and secret access, subject to plan/repository visibility constraints;
- OIDC with `id-token: write` can exchange GitHub identity for short-lived provider credentials when the provider trust policy is correctly constrained;
- GitHub upload/download artifacts expose SHA-256 digest validation, but MintTap requires digest mismatch to fail closed;
- full-length commit SHA pinning remains the documented immutable method for third-party actions;
- current private-repository ruleset/environment/attestation capabilities must not be assumed without verification.

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

## Product/site baselines retained

### Security
HTTPS-only direction, TLS 1.2 minimum / TLS 1.3 where supported, exact no-redirect association files, deliberate cache/security headers, secrets outside Git, auditable deployment and rollback.

### Accessibility
WCAG 2.2 AA internal target; semantic HTML; keyboard/focus path; 320 CSS px reflow; 200% text enlargement; accessible forms/errors/status; automation supplements manual evaluation.

### Localization / search / marketing
Korean/English locale-specific URLs; self-canonical + reciprocal hreflang; app UI/web/store localization tracked independently; sitemap/canonical/indexability controls; conservative structured data; Product-Truth-governed social previews and claims.

### Legal trigger model
Compliance remains **facts → trigger → obligation → public/control surface → backend process → validation**. The validator checks consistency with recorded applicability; it does not determine legal applicability itself.

## Current implementation direction

Preferred envelope:

**Git-versioned content/data → build-time static generation → global HTTPS/CDN hosting → isolated dynamic functions only for genuine server workflows.**

Provider shortlist:
1. Firebase Hosting;
2. Cloudflare Workers + Static Assets;
3. Vercel if justified SSR/full-stack need appears;
4. Netlify as viable static alternative.

No provider selected.

The Firebase vs Cloudflare POC must use the same static corpus, release-control contract and assertion suite. Provider-specific tooling may implement the final credential/deploy/rollback edge but must not redefine the trust model.

## Current Design Studio dependencies / handoffs

Latest checked Design Studio state:
- **Web Design** — still no substantive `W###`;
- **Layout / Interaction** — through `L005 / I004`.

Handoff rules:
- validation, trusted build, deploy, rollback, clean/waived/break-glass pass, needs-review, blocked, stale-artifact, quorum incomplete and credential-boundary states require textual/structural/programmatic meaning rather than color-only encoding;
- long digests, release IDs, reviewer IDs, rollback reasons and Korean/English governance strings are future typography/reflow stress content;
- Web Design owns production page/workflow presentation when substantive Web research exists.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- final schemas for dependencies/approvals/manifests/waivers/reviewer/quorum/break-glass/workflow contracts;
- authenticated reviewer identity mapping and repository enforcement;
- exact GitHub branch protection/CODEOWNERS/environment capability verification;
- exact Firebase Hosting auth/deploy/preview/rollback/version behavior;
- exact Cloudflare Workers/Static Assets auth/deploy/preview/rollback/version behavior;
- observed OIDC claims and provider trust policy;
- GitHub artifact retention/immutability for long-term rollback;
- deployment concurrency/serialization;
- signed/cryptographic attestation where justified;
- active CI/deployment workflow and immutable release history;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Firebase Hosting vs Cloudflare provider-edge contract mapping.** Verify current official authentication, preview/production deployment, rollback/version retention, headers/redirect/static-file behavior and constraints against the 023 four-zone contract. Execute only provider-neutral/local assertions that do not require accounts/domain authority; explicitly mark blocked live tests.
2. Execute the live provider POC when provider accounts/domain authority are available.
3. Use the POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when real product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes **001–023**.
- Studies 016–023 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 023 adds `tools/validate_active_workflow_contract.py` and `control/tests/active_workflow_contract_cases.json`.
- This file is the current operational checkpoint.
