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

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED.**

The review reconstructs the full path from URL interpretation through DNS, TLS, HTTP/intermediaries/cache, rendering boundaries, HTML→DOM, CSS/resource/layout processing, JavaScript/Web APIs, application state, navigation/history/bfcache and accessibility exposure.

### 034 — Stage 2 Website Anatomy, Task-Based IA & Content Ownership
`034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Establishes app-company websites as marketing + support + governance + store-linked operational surfaces; task-based IA; distinctions among sitemap/URL/navigation/page systems; app identity as a durable context boundary; external-entry contracts; and content ownership/change triggers.

### 035 — Stage 2 Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth
`035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Separates durable content objects from pages/components/channel fields; models App/Feature/Claim/Support/Known Issue/Release/Policy objects; establishes `claim → evidence → condition → action`; distinguishes canonical truth from public/search canonical URLs; and defines change-trigger/localization/retirement governance.

### 036 — Stage 2 Navigation, Wayfinding & Findability as an Operational System
`036-stage2-navigation-wayfinding-findability-operational-system.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Study 036 extends 034–035 rather than repeating their IA/content work. It establishes:
- navigation as both **orientation + movement**;
- separation among sitemap, hierarchy, URL space, global/local/utility/footer navigation, breadcrumbs, search, direct entry and browser history;
- findability as a multi-route system across browse/search/contextual/direct/store/search-engine entry;
- destination labels as promises that create or destroy information scent;
- stable global navigation plus deeper app/support-local contexts for multi-app scaling;
- current-location support through page title, heading, current state, context and breadcrumbs where useful;
- breadcrumbs as hierarchy rather than personal browser history, with Google guidance favoring representative user paths over URL mirroring;
- direct-entry requirements for support/privacy/account-control/release resources;
- search and browse as complementary retrieval modes;
- responsive navigation as presentation/disclosure recomposition that preserves the information model;
- accessibility constraints across keyboard/focus order, navigation landmarks, current state, zoom/reflow and localized labels;
- a navigation failure taxonomy covering coverage, label/scent, scope, placement, orientation, consistency, external entry, responsive, semantic/accessibility, search/retrieval, recovery and history/deep-link continuity;
- a critical-destination evaluation matrix for real MintTap projects;
- explicit Design Studio handoff for semantic navigation requirements and stress cases.

Primary/current evidence checked 2026-09-15 includes WCAG 2.2 normative criteria/current WAI Understanding guidance, WAI menu/navigation/breadcrumb guidance, ARIA APG navigation landmarks, and Google Search Central breadcrumb documentation updated 2026-09-08.

## Current curriculum position

**Stage 1 — Web Foundations: COMPLETE at intended foundation/practitioner level.**

**Stage 2 — Website Anatomy / Content / Information Architecture: ACTIVE.**

Studies 034–036 now establish:
1. task-based website anatomy and ownership;
2. governed content objects/hierarchy/lifecycle;
3. operational navigation, orientation and findability.

The highest-value unresolved prerequisite is **Page Systems, Content Hierarchy & Scan/Comprehension Architecture**:
- page purpose and primary task;
- page-title/heading/lead/evidence/action hierarchy;
- landing/detail/support/policy-control page types;
- prioritization vs the simplistic “above the fold” rule;
- sectioning, headings and in-page navigation;
- information density and scan paths;
- progressive disclosure at the information level;
- list/detail/comparison structures where relevant;
- empty/error/deprecated states as page anatomy;
- mobile semantic order/recomposition;
- localization expansion and accessibility stress;
- Design Studio handoff as semantic page contracts rather than premature visual templates.

This should be completed before moving into Stage 3 interaction design.

## Study quality standard

A substantial study should normally include origin/problem where useful, precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, MintTap relevance without invented project facts, durable principles vs changeable behavior, and competency/application checks.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first. Web Manager should become design-literate enough to brief, critique and validate work while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.

Study 036 adds a concrete Web Design handoff: critical-destination findability matrix, global/local scope, direct-entry cases, orientation/breadcrumb requirements, long localized labels, narrow-width/zoom/reflow stress, multiple navigation-landmark labeling, DOM/visual/focus/accessibility-order constraints, browser history/deep-link continuity and recovery cases.

Design Studio Web remains pre-baseline in its own canonical status. Web Manager does not edit Design Studio canonical files without authorization.
