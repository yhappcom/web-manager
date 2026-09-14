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

Integrated contract:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

**Stage 2 COMPLETE at intended foundation/practitioner level.**

---

## Stage 3 — UX & Interaction Foundations

### 039 — User Action, System State, Feedback, Error & Recovery Foundations
`039-stage3-user-action-system-state-feedback-error-recovery-foundations.md`

**STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Core model:

`goal → action possibility/signifier → constraint → articulation → requested transition → accepted? → pending/working? → committed state → feedback → recovery/reversal → continuity`

Established:
- usability vs interaction design vs visual presentation separation;
- action possibility/signifier/mapping/availability/commitment-truth gates;
- explicit state modeling;
- forms as stateful tasks;
- prevention/constraint/validation/error/correction/confirmation/undo/recovery separation;
- async outcome-unknown and retry-safety semantics;
- optimistic reconciliation/rollback;
- state continuity and input-mode equivalence;
- browser-native controls/forms baseline;
- reusable Interaction Contract and failure taxonomy;
- human usability proof as a separate validation gate.

### 040 — User Goals, Task/Journey Modeling, Cognition, Expectation & Friction Foundations
`040-stage3-user-goals-task-journey-cognition-expectation-friction-foundations.md`

**STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Core journey model:

`entry/context → user goal → prerequisites → task/state sequence → decision/commitment → completion / unresolved / abandoned → recovery/escalation`

Study 040 extends 039 rather than repeating local interaction mechanics. It establishes:
- goal / task / step / action / control / system-operation separation;
- journeys as user-work and state/commitment sequences rather than funnel diagrams;
- a user critical path defined by smallest **justified work**, not fewest clicks/screens;
- justification categories for necessary/protective steps;
- working-memory evidence without magic UI item-count rules;
- externalized/preserved context to reduce unnecessary recall;
- recognition-vs-recall across entire journeys;
- interruption/resumption reconstruction requirements;
- Hick/Hyman choice-reaction evidence as bounded uncertainty evidence, not a universal menu-count formula;
- progressive disclosure as decision-dependent information timing;
- semantic expectation/transfer consistency rather than pixel sameness;
- friction taxonomy: necessary / protective / accidental / manipulative-obstructive;
- FTC and EU DSA Article 25 as current regulatory evidence with explicit applicability caveats;
- uncertainty reduction before consequential commitments;
- conversion metrics separated from usability, informed choice and task success;
- reusable **Task/Journey Contract**;
- journey failure taxonomy covering goal mismatch, fragmentation, redundant/premature work, recall dependency, choice structure, expectation, interruption, commitment, friction/asymmetry and evidence failures.

Explicitly rejected as professional rules:
- fixed “4±1” or “7±2” UI item limits;
- “Hick's Law means always show fewer choices”;
- “one question per page automatically reduces cognitive load”;
- “fewer clicks/screens always means better UX”;
- “all friction is bad”;
- “higher conversion proves a better journey.”

Primary/current evidence checked 2026-09-15 includes:
- ISO 9241-210:2019, current after 2025 confirmation;
- GOV.UK whole-problem/user-needs/service measurement guidance;
- W3C Cognitive Accessibility memory/interruption guidance;
- Cowan 2001 working-memory review;
- Hick 1952 / Hyman 1953 choice-reaction research plus modern limitations review;
- FTC 2022 dark-pattern report/enforcement;
- Regulation (EU) 2022/2065 Article 25;
- Design Studio Interaction 007, I001 and Web W001;
- current Design Studio Web and Layout/Interaction statuses.

---

## Current curriculum position

**Stage 1 — COMPLETE at intended foundation/practitioner level.**

**Stage 2 — COMPLETE at intended foundation/practitioner level.**

**Stage 3 — ACTIVE.**

039 and 040 now establish the action/state layer and the goal/task/journey/cognition/friction layer.

Next highest-value integrated topic:

**Forms, Input, Choice, Validation & Multi-Step Transaction Design.**

Expected scope:
- deciding what information should be requested at all;
- labels/instructions/grouping and field semantics;
- native inputs and browser behavior;
- required vs optional information;
- defaults/prefill/known context;
- client/server validation authority and timing;
- inline errors, summaries and focus;
- conditional questions;
- multi-step sequence, review/commit and save/resume;
- redundant-entry prevention;
- accessibility and mixed input;
- task completion rather than form completion as the outcome.

---

## Study quality standard

A substantial study should normally include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, MintTap relevance without invented facts, durable vs changeable behavior, and competency/application checks.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`; MintTap-specific strategy, product/content/IA requirements, platform constraints, measurement and operations stay here first.

Current synchronized Design Studio state:
- Layout/Interaction Stage 1 is **PASS** under its current curriculum, with Stage 2 entry audit next; this does not imply human/production/platform validation;
- Web Design `W001` is Practice/Critique and W002 is next; Web Foundation is not passed;
- Interaction 007 and I001 directly inform recognition/recall, familiarity, navigation, interruption and restoration;
- W001 informs purpose/task/direct-entry and Web-native relationship constraints.

Current project handoff is now **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract**.

Web Manager does not edit Design Studio canonical files without authorization.
