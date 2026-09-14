# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The objective is professional judgment for real Apple/Android app launches and website operations, not generic article accumulation.

## Curriculum model

Canonical curriculum: `../LEARNING_ROADMAP.md`.

Learning proceeds `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT` and normally follows:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

Depth remains high while persistence/reporting remains coarse.

## Evidence labels

- `SOURCE` — authoritative evidence explicitly establishes the fact/requirement.
- `SYNTHESIS` — transferable conclusion derived from evidence.
- `MINTTAP DECISION/DIRECTION` — project-specific choice or provisional direction.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — information/work needed elsewhere.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — platform/policy/standard behavior requiring re-checking.

## Completed prior studies 001–026

Studies 001–026 remain retained prior knowledge across launch requirements, IA, privacy/support, content consistency, security, accessibility, localization, SEO, marketing, legal triggers, provider evaluation, release governance and app-company strategy. They are evidence, not the curriculum order.

---

# Sequential curriculum studies

## Stage 1 — Web Foundations

### 027 — Web / Internet / URL / Origin
`027-web-foundations-internet-web-client-server-url-origin.md`

**FOUNDATION LAYER COMPLETE.**

### 028 — DNS / Domain / Resolution
`028-web-foundations-dns-domain-resolution-hosting-path.md`

**FOUNDATION LAYER COMPLETE.**

### 029 — HTTP
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Supporting/integrated artifacts:
- `029-http-foundations-history-semantics-evolution.md`;
- `029a-http-message-anatomy-field-model-framing.md`;
- `029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md`;
- `029-http-operational-diagnosis-range-state-boundaries-competency.md`.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE.**

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE.**

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE.**

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED.**

Reconstructs URL → DNS → TLS → HTTP/cache/intermediaries → rendering → HTML/DOM → CSS/resources/layout → JS/Web APIs → state → navigation/history/bfcache → accessibility exposure.

---

## Stage 2 — Website Anatomy / Content / Information Architecture

### 034 — Website Anatomy, Task-Based IA & Content Ownership
`034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 035 — Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth
`035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 036 — Navigation, Wayfinding & Findability
`036-stage2-navigation-wayfinding-findability-operational-system.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 037 — Page Systems, Content Hierarchy & Scan/Comprehension Architecture
`037-stage2-page-systems-content-hierarchy-scan-comprehension-architecture.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 038 — Stage 2 Integration: Company/App/Support/Governance Page-System Matrix & Competency Review
`038-stage2-integration-page-system-matrix-competency-review.md`

**STAGE 2 INTEGRATION GATE PASSED — FOUNDATION/PRACTITIONER LEVEL.**

Integrated Stage 2 contract:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

Key outputs:
- company/app/support/governance/error-state page-system matrix;
- direct-entry tests for stores/search/shared links;
- support resolution→escalation contract;
- privacy/account-control scope tests;
- release/known-issue lifecycle tests;
- differentiated non-happy-state recovery;
- KO/EN + narrow-width + enlarged-text/reflow invariants;
- heading/landmark/meaningful-order gate;
- integrated failure taxonomy;
- production Design Studio handoff package.

**Stage 2 COMPLETE at intended foundation/practitioner level.**

---

## Stage 3 — UX & Interaction Foundations

### 039 — User Action, System State, Feedback, Error & Recovery Foundations
`039-stage3-user-action-system-state-feedback-error-recovery-foundations.md`

**STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Study 039 transfers and independently checks Design Studio Interaction evidence rather than duplicating it.

Core model:

`goal → action possibility/signifier → constraint → articulation → requested transition → accepted? → pending/working? → committed state → feedback → recovery/reversal → continuity`

Established:
- usability vs interaction design vs visual presentation separation;
- affordance/action possibility vs signifier/discoverability distinction;
- mapping/scope, availability and commitment truth as separate interaction gates;
- severity-proportional feedback/interruption;
- explicit user-facing state modeling before styling;
- preview/local/persisted/queued/remote/external commitment distinctions;
- forms as stateful tasks rather than field collections;
- prevention/constraint/validation/error/suggestion/confirmation/undo/recovery separation;
- consequence × reversibility protection strategy;
- async `pending / confirmed / known failed / canceled / outcome unknown` distinctions;
- retry safety as API/business-effect semantics rather than UI choice;
- optimistic UI reconciliation/rollback requirement;
- disabled/unavailable/pending distinction;
- plural state continuity across navigation/reload/interruption;
- pointer/touch/keyboard task-semantic equivalence;
- browser-native forms/controls as the baseline to evaluate before custom replacement;
- interaction failure taxonomy and reusable MintTap Interaction Contract;
- explicit separation between standards/expert diagnosis and human usability proof.

Primary/current evidence checked 2026-09-15:
- ISO 9241-11:2018 current usability standard;
- Don Norman author-published affordance/signifier clarification;
- Apple HIG Feedback, Loading and Undo/Redo;
- WHATWG HTML Living Standard forms/constraint behavior, current 2026-09-14;
- W3C Forms Tutorial updated 2026-03-27, WCAG 2.2 and current techniques;
- RFC 9110 idempotency semantics;
- Design Studio Interaction 007/015/I001/I002;
- current Design Studio Layout/Interaction and Web status;
- Web Design `W001` — now substantive Practice/Critique evidence.

## Current curriculum position

**Stage 1 — COMPLETE at intended foundation/practitioner level.**

**Stage 2 — COMPLETE at intended foundation/practitioner level.**

**Stage 3 — ACTIVE.**

Next highest-value integrated topic:

**User Goals, Task/Journey Modeling, Cognitive Load, Recognition/Recall, Expectation & Friction.**

039 explains how an action-state loop should behave. The next prerequisite is determining which interactions/steps should exist at all, how sequences affect memory/decision burden, and how to distinguish necessary or protective friction from accidental or manipulative friction before later conversion work.

Expected scope:
- goals vs system steps;
- task decomposition/critical path;
- journey as task/state sequence rather than marketing diagram;
- recognition vs recall/externalized context;
- attention/working-memory constraints without folklore magic numbers;
- consistency/expectation and transfer learning;
- decision complexity without blindly applying Hick-style formulas;
- progressive disclosure/information timing;
- interruption/resumption cues;
- friction taxonomy and trust/uncertainty reduction;
- ethical boundary before conversion optimization.

---

## Study quality standard

A substantial study should normally include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, MintTap relevance without invented facts, durable vs changeable behavior, and competency/application checks.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`; MintTap-specific strategy, product/content/IA requirements, platform constraints, measurement and operations stay here first.

Current Design Studio state relevant to Web Manager:
- Web Design `W001` is complete at PRACTICE/CRITIQUE; previous Web Manager notes saying there was no substantive `W###` evidence are superseded;
- Layout/Interaction has substantive I001–I006/L001–L006 evidence but remains Foundation/CRITIQUE, not production PASS;
- human/project validation remains deferred rather than simulated.

Current project handoff is now **Stage 2 Page Contract + Stage 3 Interaction Contract**, including action scope, state/commitment truth, async/retry/recovery behavior, input-mode equivalence, focus/history/restoration, localization/reflow, and browser-native-vs-custom validation.

Web Manager does not edit Design Studio canonical files without authorization.
