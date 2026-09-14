# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve a real MintTap decision, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — information or work needed elsewhere.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed studies

- `001-app-launch-website-foundations.md` — Apple/Google launch web requirements.
- `002-multi-app-information-architecture.md` — multi-app company/app/support/governance IA.
- `003-privacy-support-account-deletion-architecture.md` — per-app privacy/support/deletion and App Data Contract.
- `004-store-website-content-synchronization.md` — Product Truth, screenshot evidence and release synchronization.
- `005-domain-hosting-security-baseline.md` — HTTPS/TLS, machine files, headers, DNS, rollback and monitoring.
- `006-accessibility-production-baseline.md` — WCAG 2.2 AA internal production baseline.
- `007-localization-architecture.md` — Korean/English locale URLs, hreflang and localization controls.
- `008-seo-structured-data-crawlability.md` — canonical, robots, sitemap, schema and Search Console.
- `009-seo-independent-verification-social-preview.md` — indexability classes and Open Graph baseline.
- `010-company-app-marketing-content-model.md` — Claim Registry, evidence, screenshots and truthful marketing.
- `011-operational-release-change-watch-controls.md` — continuous release/change-watch operating loop.
- `012-implementation-provider-comparison-methodology.md` — static-first architecture and hosting-provider comparison.
- `013-jurisdiction-legal-compliance-trigger-map.md` — fact-driven Korea/U.S./EU legal trigger framework.
- `014-provider-poc-specification.md` — identical Firebase vs Cloudflare provider-neutral POC and assertion contract.
- `015-machine-readable-control-artifact-model.md` — canonical JSON truth records, JSON Schema, stable IDs, semantic fingerprints and dependency/invalidation model.
- `016-control-artifact-validation-specimen.md` — executable structural + semantic validation specimen; 5/5 expected outcomes.
- `017-release-chain-semantic-integrity.md` — release/store, privacy/data, locale, legal trigger and operational-surface validation; 12/12 expected outcomes.
- `018-semantic-fingerprint-dependency-impact.md` — semantic fingerprint comparison and dependency propagation; 5/5 expected outcomes.
- `019-typed-dependency-approval-freshness.md` — typed impact severity, cycle detection and fingerprint-bound approval freshness; 6/6 expected outcomes.
- `020-derived-release-manifest-gate-waivers.md` — derived `PASS / NEEDS_REVIEW / BLOCKED` gate plus scoped auditable waivers; 8/8 expected outcomes.
- `021-release-provenance-reviewer-authorization-ci.md` — source/tool/policy-bound provenance, reviewer authorization and fail-closed CI; 9/9 expected outcomes.
- `022-protected-policy-quorum-revocation-workflow-trust.md` — protected policy ownership, quorum/revocation, break-glass and workflow trust boundaries; 10/10 expected outcomes.
- `023-provider-neutral-active-workflow-trust-boundary.md` — four-zone PR validation/trusted build/deploy/rollback contract, artifact-digest binding and provider credential boundary; 12/12 expected outcomes.
- `024-firebase-cloudflare-provider-edge-contract-mapping.md` — current Firebase Hosting vs Cloudflare Workers/Static Assets mapping for preview, exact-version promotion, rollback, credentials, routing and static response controls; 11/11 expected outcomes.

## Practice artifacts

Current synthetic validation corpus includes the earlier 016–023 schemas/tests/tools plus:
- `control/tests/provider_edge_contract_cases.json`;
- `tools/validate_provider_edge_contract.py`.

These are synthetic research fixtures, not actual MintTap product/legal/store facts.

## Current research queue

See root `STATUS.md` for the authoritative queue. Highest-value next work:

1. prepare an identical provider POC corpus + provider-neutral HTTP assertion runner locally: Korean/English pages, support/privacy/app routes, machine files, 404, canonical redirects, cache/security headers, sitemap/robots and release artifact digest manifest;
2. execute the live Firebase Hosting vs Cloudflare Workers/Static Assets POC when provider accounts/domain authority are available;
3. real-browser Korean/English typography/localization/accessibility/search/social/marketing/legal transfer validation on that POC;
4. apply Legal Trigger Registry when MintTap entity/market/audience/data/transaction facts are available;
5. app-specific user/market evidence when actual product pages are assigned.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web decisions and production findings stay here first.

Latest checked state: Web Design still has no substantive `W###`. Provider behavior is not a visual-design decision, but future browser validation must explicitly test canonical URLs, preview indexation, 404 recovery, cache/security headers, machine endpoints and the real provider routing behavior before design/accessibility transfer is considered complete.

When MintTap implementation confirms, limits or contradicts reusable Design Studio evidence, record it here first and hand it back to the appropriate specialist when justified.
