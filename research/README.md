# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method. **The curriculum is knowledge-led, not POC-led.** Implementation experiments are used only when they materially validate a web decision; they are not the standing next step.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
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
- `025-identical-provider-poc-corpus-http-assertion.md` — deterministic synthetic provider-neutral corpus, artifact digest manifest and identical preview/production HTTP assertion contract; 8/8 controlled outcomes.
- `026-app-company-web-strategy-information-hierarchy.md` — visitor intent, app landing-page information hierarchy, website→store message continuity, responsive hierarchy and performance-aware first-contact strategy.

## Practice artifacts

Studies 016–025 include synthetic validation artifacts. They remain useful implementation evidence, but are **not a mandatory sequence to continue** and are not actual MintTap product/legal/store facts.

## Current research direction

The highest-value gap is now visitor-facing web expertise. Continue across:

1. app-company / multi-product website IA and navigation decision models;
2. landing-page content strategy, evidence, conversion and CTA design without manipulative patterns;
3. trust architecture for a small/unknown app developer;
4. support/FAQ/self-service information architecture;
5. responsive content hierarchy and mobile-first recomposition;
6. performance-aware marketing design and Core Web Vitals;
7. analytics/measurement framework for company and app pages;
8. systematic precedent/critique of real app-company websites;
9. SEO/discovery, localization, accessibility, privacy/legal and operations revisited when new evidence materially improves prior conclusions.

Provider POC/deployment-adapter work is **deferred until a real implementation decision requires it**. Firebase/Cloudflare knowledge from 012/014/024/025 remains retained for that future project.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy/content/operations stay here first.

Study 026 begins a stronger visitor-facing handoff: Web Manager supplies page purpose, audience evidence, visitor intents, factual content hierarchy, actions, support/governance requirements and constraints. Design Studio owns visual expression through typography, color, layout, interaction and brand application. Future real-browser evidence can flow back to the relevant specialist.
