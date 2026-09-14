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

### 028 — DNS / Domain / Resolution
`028-web-foundations-dns-domain-resolution-hosting-path.md`

### 029 — HTTP
Supporting/integrated 029 artifacts cover semantics, messages/framing, caching/negotiation/intermediaries and operational competency.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED — FOUNDATION/PRACTITIONER LEVEL.**

---

## Stage 2 — Website Anatomy / Content / Information Architecture

### 034 — Website Anatomy, Task-Based IA & Content Ownership
`034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`

### 035 — Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth
`035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`

### 036 — Navigation, Wayfinding & Findability
`036-stage2-navigation-wayfinding-findability-operational-system.md`

### 037 — Page Systems, Content Hierarchy & Scan/Comprehension Architecture
`037-stage2-page-systems-content-hierarchy-scan-comprehension-architecture.md`

### 038 — Stage 2 Integration: Company/App/Support/Governance Page-System Matrix & Competency Review
`038-stage2-integration-page-system-matrix-competency-review.md`

**STAGE 2 INTEGRATION GATE PASSED — FOUNDATION/PRACTITIONER LEVEL.**

Integrated contract:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

---

## Stage 3 — UX & Interaction Foundations

### 039 — User Action, System State, Feedback, Error & Recovery Foundations
`039-stage3-user-action-system-state-feedback-error-recovery-foundations.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Core model:

`goal → action possibility/signifier → constraint → articulation → requested transition → accepted? → pending/working? → committed state → feedback → recovery/reversal → continuity`

Reusable output: **Interaction Contract**.

### 040 — User Goals, Task/Journey Modeling, Cognition, Expectation & Friction Foundations
`040-stage3-user-goals-task-journey-cognition-expectation-friction-foundations.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Core model:

`entry/context → user goal → prerequisites → task/state sequence → decision/commitment → completion / unresolved / abandoned → recovery/escalation`

Reusable output: **Task/Journey Contract**.

040 explicitly rejects magic working-memory item limits, simplistic Hick-law menu-count rules, universal one-question-per-page, minimum-click dogma, “all friction is bad” and conversion-as-usability proof.

### 041 — Forms, Input, Choice, Validation & Multi-Step Transaction Design
`041-stage3-forms-input-choice-validation-multistep-transactions.md`

**FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

041 integrates 039 action/state mechanics with 040 task/journey/cognition judgment in the first major web transaction system.

Established:
- ask why data is needed before selecting a control;
- question protocol for necessity, known context, sensitivity/retention, authority and downstream use;
- label vs legend/group vs instruction/hint vs error separation;
- HTML `type` vs `autocomplete` vs `inputmode` separation;
- native constraint validation vs cross-field/domain/server/security validation;
- client validation as assistance, not authoritative trust boundary;
- error identity/description/correction/local+summary/focus/preservation architecture;
- process-state reuse vs browser autofill vs account/profile prefill;
- WCAG redundant-entry implications;
- choice control based on actual cardinality/decision model;
- conditional-question state lifecycle and stale hidden-value risk;
- multi-step splitting by task logic, not universal one-question folklore;
- progress indicators as truth about the real path;
- consequence × reversibility review/confirmation judgment;
- pending/rejected/known-failure/confirmed/outcome-unknown transaction states;
- WCAG status-message exposure without automatic focus theft;
- password-manager/autofill/copy-paste participation in authentication;
- upload state distinction between transfer and authoritative acceptance;
- save/resume as persistence + identity + privacy + expiry + version contract;
- task completion rather than successful form/HTTP submission as the outcome;
- reusable **Form / Transaction Contract** and form failure taxonomy.

Primary/current evidence checked 2026-09-15:
- WHATWG HTML Living Standard — forms, autofill and constraint validation;
- W3C WCAG 2.2/current Understanding guidance — 1.3.5, 3.3.x, 4.1.3;
- W3C WAI Forms Tutorial — labels, grouping, instructions, validation, notifications, multi-page forms;
- GOV.UK Design System — question pages, radios, checkboxes, text input, error summary, check answers;
- Apple HIG — Text Fields;
- latest Design Studio Web W001/W002 and Layout/Interaction status.

---

## Current curriculum position

**Stage 1 — COMPLETE at intended foundation/practitioner level.**

**Stage 2 — COMPLETE at intended foundation/practitioner level.**

**Stage 3 — ACTIVE.**

039–041 now establish:
1. action/state/error/recovery mechanics;
2. goal/task/journey/cognition/friction architecture;
3. form/input/choice/validation/multi-step transaction contracts.

Next highest-value integrated topic:

**Search, Filtering, Selection, Results & List/Detail Interaction Foundations.**

Expected scope:
- browse vs search vs filter;
- query/scope/result state;
- suggestions and search expectations;
- filter control/cardinality and selected-filter visibility;
- immediate vs explicit apply semantics;
- URL/history/shareability;
- sorting vs filtering vs ranking;
- list/detail selection continuity;
- loading/empty/no-result/error distinctions;
- result count/status exposure;
- keyboard/touch/accessibility;
- responsive/localized stress;
- whether launch-time site search is justified at all.

This block concerns **on-site retrieval interaction**, not SEO/search-engine discovery (Stage 6).

---

## Study quality standard

A substantial study should normally include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, MintTap relevance without invented facts, durable vs changeable behavior, and competency/application checks.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`; MintTap-specific strategy, product/content/IA requirements, platform constraints, measurement and operations stay here first.

Latest specialist-file state checked 2026-09-15:
- Layout/Interaction Stage 1 **PASS**, Stage 2 entry audit next; human/production/platform validation still open;
- Web Design W001/W002 **PRACTICE/CRITIQUE**, Foundation not passed; W003 responsive/adaptive recomposition next;
- W002 supplies bounded Chromium long bilingual + 200%-text page-composition evidence but not browser UI zoom, Safari/Firefox parity, screen-reader PASS or complete form-task validation.

Current project handoff is **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract + 041 Form/Transaction Contract**.

Web Manager does not edit Design Studio canonical files without authorization.
