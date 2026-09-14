# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager owns MintTap company website content, app-launch web requirements and operational consistency. GitHub is canonical long-term memory; chat is temporary working context. Self-directed study continues when no live assignment takes priority.

## Completed foundation / practice studies

Studies **001–024** are complete at the documented Foundation/PRACTICE level. Canonical details are under `research/` and indexed in `research/README.md`.

Latest sequence:
- **016** Control Artifact Validation Specimen — 5/5;
- **017** Release-Chain Semantic Integrity — 12/12;
- **018** Semantic Fingerprints / Dependency Impact — 5/5;
- **019** Typed Dependency / Approval Freshness — 6/6;
- **020** Derived Release Gate / Auditable Waivers — 8/8;
- **021** Release Provenance / Reviewer Authorization / Fail-Closed CI — 9/9;
- **022** Protected Policy Ownership / Quorum / Revocation / Workflow Threat Model — 10/10;
- **023** Provider-Neutral Active Workflow Trust-Boundary Contract — 12/12;
- **024** Firebase Hosting vs Cloudflare Provider-Edge Contract Mapping — 11/11.

Production PASS is not claimed. Actual MintTap facts, real store-console state, legal applicability, provider accounts/domain authority, live CI/deployment enforcement and browser/device production validation remain incomplete.

## 024 — Firebase vs Cloudflare provider-edge mapping

New artifacts:
- `research/024-firebase-cloudflare-provider-edge-contract-mapping.md`
- `tools/validate_provider_edge_contract.py`
- `control/tests/provider_edge_contract_cases.json`

Controlled result: **11 / 11 expected outcomes matched.**

### Firebase Hosting mapping

Verified from current official Firebase/Google Cloud documentation:
- permanent live channel plus temporary preview channels;
- preview channels documented **beta**, default 7-day expiry, configurable up to 30 days;
- deployed releases point to version objects;
- `firebase hosting:clone` can promote an already tested version to another channel; same-site clone can preserve the exact version ID;
- live rollback creates a new release serving a previous version;
- release retention is configurable per channel and old retained content can be deleted;
- Firebase CLI recommends Application Default Credentials for CI; legacy `FIREBASE_TOKEN` is less secure and no longer recommended;
- Google Cloud Workload Identity Federation can exchange GitHub OIDC identity for short-lived Google credentials used through ADC;
- `firebase.json` controls redirects, rewrites, headers, deploy directory and custom 404 behavior.

Preferred MintTap path:

**GitHub OIDC → Google Cloud WIF → ADC → Firebase CLI → preview/tested Hosting version → exact-version clone to live.**

Live validation is still required for exact IAM roles and CLI behavior.

### Cloudflare Workers + Static Assets mapping

Verified from current official Cloudflare documentation:
- Worker versions include bundled code, static assets, bindings and compatibility settings;
- external storage state such as KV/R2/D1/Durable Objects is not versioned with the Worker;
- `wrangler versions upload` creates a version without immediately deploying it;
- `wrangler versions deploy --version-id` can later promote the exact uploaded version;
- version preview URLs are available when enabled and are public by default unless protected with Cloudflare Access;
- external GitHub Actions deployment docs currently use scoped Cloudflare API token + account ID;
- rollback creates a new deployment for a selected previous version and is limited to the 100 most recent published versions;
- rollback does not restore external bound-resource state;
- `_headers`, `_redirects`, `assets.html_handling` and static routing configuration control static response behavior.

Preferred MintTap path:

**trusted source → `wrangler versions upload` → capture version ID + preview → release manifest ALLOW → `wrangler versions deploy --version-id <approved>`**.

Current evidenced credential baseline for external CI is **scoped API token**, not OIDC. OIDC-equivalent Cloudflare deployment auth remains OPEN.

## 023/024 common provider contract

A provider is acceptable for the live POC only if:
1. preview is isolated from production traffic;
2. production promotion is separate from preview creation;
3. the exact reviewed provider version can be promoted without source rebuild;
4. rollback can re-point to a prior retained provider version without rebuilding current source;
5. rollback retention is explicitly bounded and monitored;
6. static security/cache headers are configurable and verifiable;
7. redirect/canonical URL behavior is explicit;
8. custom 404 behavior is explicit;
9. deployment credentials exist only in DEPLOY/ROLLBACK trust zones;
10. dynamic/external state is not assumed to roll back with the provider version;
11. provider version ID and MintTap artifact digest are both recorded in release provenance;
12. real account/domain validation is required before production PASS.

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
- time-bounded break-glass handling;
- source/tool/input provenance and fail-closed CI semantics;
- four-zone workflow trust separation;
- provider version + artifact-digest deployment binding;
- credential isolation to deploy/rollback;
- provider-specific auth adapter without changing the provider-neutral trust model;
- canonical truth remains unchanged by waiver/emergency disposition;
- no secrets or customer personal data in this repository.

Important limitation: current deterministic Python JSON serialization is still **not claimed as full RFC 8785 JCS conformance**.

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

Provider shortlist remains:
1. Firebase Hosting;
2. Cloudflare Workers + Static Assets;
3. Vercel if justified SSR/full-stack need appears;
4. Netlify as viable static alternative.

No provider selected.

Firebase and Cloudflare both remain viable after 024. The provider POC must use the same content corpus, HTTP assertion suite and release-control contract. Provider-specific deployment tooling may implement only the final adapter edge.

## Current Design Studio dependencies / handoffs

Latest checked Design Studio Web state still has no substantive `W###`.

Handoff rules:
- provider behavior must be tested as part of real browser design QA, not treated as invisible infrastructure;
- canonical/trailing-slash behavior, preview indexation, 404 recovery, cache/security headers and machine endpoints are explicit Web validation inputs;
- localized Korean/English routes and long governance/release strings remain future layout/type/accessibility stress cases;
- visual treatment remains Web Design ownership once substantive Web research exists.

## Important open items

- actual MintTap entity/public contact/contracting entity;
- real app inventory/releases/pricing/accounts/locales/markets/audience;
- real App Store Connect / Play Console state ingestion;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- legal applicability/signoff process;
- full RFC 8785/JCS conformance validation;
- final schemas for dependencies/approvals/manifests/waivers/reviewer/quorum/break-glass/workflow/provider contracts;
- authenticated reviewer identity mapping and repository enforcement;
- exact GitHub branch protection/CODEOWNERS/environment capability verification;
- Firebase WIF/ADC minimum IAM roles and exact live Hosting CLI behavior;
- Cloudflare minimum API-token permissions and external-CI short-lived credential alternatives;
- Firebase preview-backend isolation policy because previews can reach real project resources;
- Cloudflare preview visibility/Access policy;
- exact custom-domain/DNS implications for `minttap.app`;
- observed OIDC claims and provider trust policy;
- deployment concurrency/serialization;
- immutable release history / long-term rollback retention;
- signed/cryptographic attestation where justified;
- active CI/deployment workflow;
- real App Links/AASA/app-ads identifiers/routes;
- real-browser Korean/English design/accessibility transfer validation;
- Search Console/policy-alert/webhook/escalation ownership.

## Next research queue

1. **Identical provider POC corpus + provider-neutral HTTP assertion runner.** Build the local corpus for `/ko/`, `/en/`, app/support/privacy routes, exact machine files, 404, canonical redirects, sitemap/robots, cache/security headers and artifact-digest manifest. This work must remain deploy-provider-neutral.
2. Execute the live Firebase Hosting vs Cloudflare Workers/Static Assets POC when provider accounts/domain authority are available.
3. Use the live POC for Design Studio real-browser Korean/English/accessibility/layout/type/color transfer validation.
4. Apply Legal Trigger Registry when actual entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when actual product pages are assigned.

## Persistence state

- `AGENTS.md` contains autonomous continuous-learning rules.
- `research/README.md` indexes **001–024**.
- Studies 016–024 have executable PRACTICE artifacts under `control/` and `tools/`.
- Study 024 adds `tools/validate_provider_edge_contract.py` and `control/tests/provider_edge_contract_cases.json`.
- This file is the current operational checkpoint.
