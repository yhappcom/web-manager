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

## Practice artifacts

Current synthetic validation corpus includes the earlier 016–022 schemas/tests/tools plus:
- `control/tests/active_workflow_contract_cases.json`;
- `tools/validate_active_workflow_contract.py`.

These are synthetic research fixtures, not actual MintTap product/legal/store facts.

## Current research queue

See root `STATUS.md` for the authoritative queue. Highest-value next work:

1. map current Firebase Hosting and Cloudflare Workers/Static Assets official authentication, preview/production deployment, rollback/version retention and static-routing/header behavior onto the 023 four-zone contract; execute only assertions that do not require provider accounts/domain authority;
2. execute the live provider POC when provider accounts/domain authority are available;
3. real-browser Korean/English typography/localization/accessibility/search/social/marketing/legal transfer validation on that POC;
4. apply Legal Trigger Registry when MintTap entity/market/audience/data/transaction facts are available;
5. app-specific user/market evidence when actual product pages are assigned.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web decisions and production findings stay here first.

Latest checked state: Web Design still has no substantive `W###`; Layout/Interaction is through `L005 / I004`. Web Manager governance states remain semantic/control inputs only. Validation/build/deploy/rollback, clean/waived/break-glass pass, needs-review, blocked, stale-artifact and credential-boundary states must later be expressed textually/structurally/programmatically rather than by color alone.

When MintTap implementation confirms, limits or contradicts reusable Design Studio evidence, record it here first and hand it back to the appropriate specialist when justified.
