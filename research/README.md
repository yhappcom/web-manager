# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Each major topic matures through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

### Depth and cadence rule

Large domains are not marked complete after one short survey. Study should follow:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

Depth remains high, but persistence/reporting is intentionally coarse. Several related learning sub-blocks should normally be integrated into one professional knowledge checkpoint instead of generating one file/report per small concept.

A foundation core may close when it can be explained, diagnosed and applied at the level required by the curriculum; the same domain can and should be reopened later for advanced security, performance, SEO, accessibility, browser or operations depth.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION/DIRECTION` — project-specific choice or provisional direction.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed prior studies 001–026

Studies 001–026 remain retained as prior knowledge spanning launch requirements, IA, privacy/support, content consistency, security, accessibility, localization, SEO, marketing, legal triggers, provider evaluation, release governance and app-company strategy. They are prior knowledge, not the curriculum order going forward.

## Sequential curriculum studies

### 027 — Web / Internet / URL / Origin
`027-web-foundations-internet-web-client-server-url-origin.md`

**FOUNDATION LAYER COMPLETE.** Internet ≠ Web; client/server roles; resource vs representation; URL; host/domain/origin; origin security significance; failure-layer model.

### 028 — DNS / Domain / Resolution
`028-web-foundations-dns-domain-resolution-hosting-path.md`

**FOUNDATION LAYER COMPLETE.** DNS hierarchy/delegation; resolver/authority; records; TTL/cache; registration/delegation/hosting separation; DNS failure diagnosis.

### 029 — HTTP
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Supporting/integrated artifacts:
- `029-http-foundations-history-semantics-evolution.md`;
- `029a-http-message-anatomy-field-model-framing.md`;
- `029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md`;
- `029-http-operational-diagnosis-range-state-boundaries-competency.md`.

HTTP Stage 1 competency covers history/semantics, methods/statuses, representations and negotiation, caching/validators, intermediaries, HTTP/1.1–3, QUIC relationships, state/auth boundaries and operational diagnosis. It will be reopened in later SEO/performance/security/operations stages.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage includes secure-channel goals; SSL→TLS history; current TLS 1.3 authority; handshake/record reasoning; symmetric/asymmetric roles; X.509 chain/trust anchors; SAN service identity; SNI/ALPN; HSTS/preload; `.app` implications; CT/root-program policy; edge/origin TLS separation; certificate lifetime automation; and failure diagnosis.

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage includes HTML parsing/DOM; semantic HTML; CSS cascade vs layout; ECMAScript vs Web APIs; script timing; events; native controls; accessibility API mapping; DOM/visual/focus-order distinctions; and layered browser-runtime diagnosis.

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage includes build/request/client rendering boundaries; SSR/CSR/SSG/hybrid strategies; hydration; progressive enhancement; browser/runtime/history/cookie/Web Storage/server-state boundaries; RFC 10025 cookie authority; cross-document vs same-document navigation; SPA vs rendering-strategy distinctions; Back/Forward; bfcache; native forms; CDN/edge/static/render/client responsibility boundaries; and rendering/state/navigation failure diagnosis.

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED.**

The review reconstructs the full path from URL interpretation through DNS, TLS, HTTP/intermediaries/cache, rendering boundaries, HTML→DOM, CSS/resource/layout processing, JavaScript/Web APIs, application state, navigation/history/bfcache and accessibility exposure. It tests representative failures by responsible layer rather than vague symptom labels and establishes cross-layer invariants such as `DNS success ≠ TLS success`, `HTTP 200 ≠ correct representation`, and `visual correctness ≠ accessibility correctness`.

### 034 — Stage 2 Website Anatomy, Task-Based IA & Content Ownership
`034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

This study deliberately extends studies 002 and 026 rather than repeating them. It establishes:
- public app-company websites as marketing + support + governance + store-linked operational surfaces;
- task-based IA modeled as `audience/context → intent → task → destination → content object → owner → lifecycle`;
- distinction between sitemap, URL structure, global navigation, contextual navigation, page hierarchy and machine endpoint space;
- company/portfolio, app identity, support/self-service, governance/user-control and machine/infrastructure page systems;
- app identity as a durable context boundary;
- shallow global navigation with deeper stable app/support contexts;
- support context + escalation requirements;
- store-linked URLs as stable external-entry contracts;
- content ownership/change-trigger metadata as part of IA;
- failure diagnosis across missing content, scope ambiguity, labels, placement, orientation, external entry, lifecycle and accessibility/responsive operation;
- a reusable task/destination matrix for real MintTap sitemap work.

### 035 — Stage 2 Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth
`035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Study 035 reuses the Product Truth / Claim Registry / release-governance work from 004, 010 and 011 rather than duplicating it, then formalizes a reusable content operating model:
- separates durable content objects from pages, visual components and channel-specific metadata fields;
- models App, Feature, Product Claim, Support Topic, Support Article, Known Issue, Release Change and Governance/Policy objects with scope, ownership, evidence and lifecycle;
- establishes `claim → evidence → condition → action` as a product-content hierarchy;
- defines semantic page-template content contracts without forcing identical visual layouts or identical app prose;
- distinguishes governed public duplication from independent truth duplication;
- distinguishes canonical content truth, canonical public URL and search canonical URL;
- ties freshness to release/data/account/pricing/platform/support/rebrand change triggers rather than calendar age alone;
- treats localization as a dependency graph with explicit stale/needs-review state;
- adds retirement/redirect/external-dependency checks for store-linked resources;
- treats support as a task-resolution/escalation system rather than an FAQ dump;
- defines a content-failure taxonomy covering truth, scope, evidence, synchronization, localization, ownership, triggers, hierarchy, findability and retirement;
- defines Design Studio handoff as semantic content contracts and stress cases rather than premature visual hierarchy.

Primary/current evidence checked 2026-09-15 includes Apple App Store Connect app/version/privacy references, Google Play store listing/Data safety/User Data/account-deletion guidance, W3C WCAG 2.2/page-structure guidance and Google Search canonicalization documentation.

## Current curriculum position

**Stage 1 — Web Foundations: COMPLETE at intended foundation/practitioner level.**

**Stage 2 — Website Anatomy / Content / Information Architecture: ACTIVE.**

Studies 034–035 now establish the Stage 2 information/content foundation. The highest-value unresolved block is **navigation, wayfinding and findability as an operational system**:
- global vs local/context navigation;
- information scent and destination labels;
- location/orientation cues and breadcrumbs;
- search vs browse vs direct/external entry;
- support/privacy/account-control findability;
- mobile navigation recomposition;
- localization, zoom, keyboard and screen-reader stress;
- deep-link/store/search entry behavior;
- failure modes where correct content exists but cannot be found.

This should be completed before moving into Stage 3 interaction design.

## Study quality standard

A substantial study should normally include:
- origin/history and the problem being solved where useful;
- precise definitions and vocabulary;
- first-principles mechanics;
- authoritative standards and current implementation evidence;
- examples/counterexamples and common misconceptions;
- failure modes and operational diagnosis;
- relationships to security, performance, accessibility, SEO, UX and operations where relevant;
- MintTap relevance without inventing project facts;
- durable principles vs changeable implementation behavior;
- competency/application checks.

Implementation experiments are used only when necessary to answer a material factual question. POC work is not the default learning path.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first. Web Manager should become design-literate enough to brief, critique and validate work while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.

Studies 031–033 provide browser/runtime/navigation constraints. Study 034 adds task/destination and page-system contracts. Study 035 adds semantic content-object/page-contract/lifecycle inputs: App/Feature/Claim/Support/Policy relationships, `claim → evidence → condition → action`, direct-entry constraints, localized-content stress cases, and current/deprecated/known-issue states.

Design Studio Web remains pre-baseline in its own canonical status. Its scope explicitly includes IA, navigation, page hierarchy, content flow, responsive composition and browser validation, so later Stage 2 project work should use it as a cross-validation layer. Web Manager does not edit Design Studio canonical files without authorization.
