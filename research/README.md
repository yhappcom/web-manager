# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning now proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Major stages:
1. Web Foundations;
2. Website Anatomy / Content / IA;
3. UX & Interaction Foundations;
4. Web Design Literacy;
5. Accessibility;
6. Search / Discovery / Content Quality;
7. Performance / Browser Runtime;
8. Security / Privacy / Trust;
9. Analytics / Experimentation;
10. App-Company Web Strategy / Growth;
11. Web Operations / Platform Architecture;
12. Advanced / Expert Web Management.

Each major topic should mature through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed prior studies

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
- `020-derived-release-manifest-gate-waivers.md` — derived gate plus scoped auditable waivers; 8/8 expected outcomes.
- `021-release-provenance-reviewer-authorization-ci.md` — source/tool/policy-bound provenance, reviewer authorization and fail-closed CI; 9/9 expected outcomes.
- `022-protected-policy-quorum-revocation-workflow-trust.md` — protected policy ownership, quorum/revocation, break-glass and workflow trust boundaries; 10/10 expected outcomes.
- `023-provider-neutral-active-workflow-trust-boundary.md` — four-zone workflow trust contract; 12/12 expected outcomes.
- `024-firebase-cloudflare-provider-edge-contract-mapping.md` — Firebase vs Cloudflare provider-edge mapping; 11/11 expected outcomes.
- `025-identical-provider-poc-corpus-http-assertion.md` — deterministic synthetic provider-neutral corpus and assertion contract; 8/8 controlled outcomes.
- `026-app-company-web-strategy-information-hierarchy.md` — visitor intent, landing-page hierarchy, store continuity, responsive hierarchy and performance-aware first-contact strategy.

These files are **prior knowledge**, not the curriculum order going forward.

## Current curriculum position

**Stage 1 — Web Foundations**.

Next studies:
- `027` — Internet, Web, client/server, browser, origin and URL;
- `028` — DNS, domains, resolution and hosting path;
- `029` — HTTP request/response, methods, status codes, headers and cache basics;
- `030` — HTTPS, TLS, certificates and browser trust basics;
- `031` — HTML, CSS, JavaScript, DOM and accessibility tree;
- `032` — static/dynamic, SSR/CSR/SSG, browser state/storage/navigation;
- `033` — Stage 1 integration and competency review.

The purpose of revisiting apparently familiar subjects is to establish a complete first-principles mental model rather than relying on isolated advanced knowledge.

## Study quality standard

A substantial study should normally include:
- precise definitions and vocabulary;
- first-principles explanation;
- authoritative or high-quality evidence;
- examples and counterexamples;
- common misconceptions;
- failure modes;
- MintTap relevance;
- boundaries between durable principles and changeable platform behavior;
- a competency/application check when useful.

Implementation experiments are used only when necessary to answer a material factual question. POC work is not the default learning path.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first.

Web Manager should become design-literate enough to brief, critique and validate web work, while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.
