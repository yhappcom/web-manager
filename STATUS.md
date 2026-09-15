# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**  
Last sync: 2026-09-15  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play

## Mission state

Build professional Web Manager judgment from first principles through advanced cross-domain reasoning. GitHub is canonical memory; chat is temporary context. Canonical curriculum: `LEARNING_ROADMAP.md`.

Learning remains coarse-grained and evidence-led:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

---

# Stage 1 — Web Foundations

**COMPLETE — FOUNDATION/PRACTITIONER CURRICULUM GATE PASSED.**

027–033 cover Web/Internet/URL/Origin, DNS, HTTP, TLS/browser trust, HTML/CSS/JS/DOM/accessibility tree, rendering/state/navigation and end-to-end integration. Reopen later for advanced SEO/performance/security/accessibility/operations depth.

# Stage 2 — Website Anatomy / Content / Information Architecture

**COMPLETE — FOUNDATION/PRACTITIONER CURRICULUM GATE PASSED.**

034–038 cover task-based anatomy/content ownership, content modeling/lifecycle/cross-channel truth, navigation/findability, page systems/comprehension and integrated Company/App/Support/Governance competency.

Integrated model:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

Reusable output: task/destination matrix + content-object/lifecycle model + critical-destination findability matrix + Page Contract.

---

# Stage 3 — UX & Interaction Foundations

**CURRENT MAJOR CURRICULUM STAGE — ACTIVE.**

## 039 — User Action, System State, Feedback, Error & Recovery

`research/039-stage3-user-action-system-state-feedback-error-recovery-foundations.md`  
**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Core: explicit action/state/feedback/recovery, consequence × reversibility, pending/confirmed/known-failed/canceled/outcome-unknown, timeout ≠ failure, retry/idempotency dependency and continuity. Reusable output: **Interaction Contract**.

## 040 — User Goals, Task/Journey Modeling, Cognition, Expectation & Friction

`research/040-stage3-user-goals-task-journey-cognition-expectation-friction-foundations.md`  
**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Core: smallest justified work rather than fewest clicks; no magic working-memory/Hick item counts; reduce unnecessary recall; progressive disclosure follows decision dependency; classify friction as necessary/protective/accidental/manipulative-obstructive. Reusable output: **Task/Journey Contract**.

## 041 — Forms, Input, Choice, Validation & Multi-Step Transaction Design

`research/041-stage3-forms-input-choice-validation-multistep-transactions.md`  
**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Core: form as task/transaction protocol; question necessity before control selection; semantic HTML input purpose; native/cross-field/domain/remote/security validation authority; error architecture; redundant-entry reduction; conditional-state lifecycle; consequence × reversibility review; pending/outcome-unknown transaction states; save/resume and retry/idempotency contracts. Reusable output: **Form / Transaction Contract**.

## 042 — Search, Filtering, Selection, Results & List/Detail Interaction

`research/042-stage3-search-filter-selection-results-list-detail-foundations.md`  
**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

### Core retrieval model

`information need → query/scope → submitted retrieval state → result set → refinement → selection → detail → return/resume`

### Retained judgment

- browse/navigation, search, filter, sort and ranking are distinct operations;
- do not add launch-time site search merely because a search component is conventional;
- search does not repair missing content or weak IA;
- distinguish draft query, submitted query, scope, active filters, sort/rank, retrieval status, result set, selection and list context;
- immediate retrieval/filtering and explicit Apply have different state/concurrency contracts;
- filter cardinality and AND/OR semantics must be explicit;
- active constraints must remain inspectable/removable;
- URL representation can improve reload/share/bookmark/history for safe public state, but sensitive queries must not be serialized by default;
- result objects need enough identity/evidence to choose correctly without exposing irrelevant metadata;
- distinguish idle/loading/results/success-empty/partial/stale/known-error/canceled/outcome-unknown;
- **0 results ≠ retrieval failure**;
- diagnose no-result cause: query mismatch, overconstraint, wrong scope, genuine absence or index lag;
- stale async responses must not overwrite newer query state;
- dynamic result status needs an AT exposure strategy without indiscriminate focus movement;
- list → detail → Back should preserve query/filter/sort plus meaningful position/selection context where appropriate;
- suggestions/autocomplete are a separate retrieval surface with source, semantics, keyboard/touch and privacy requirements;
- responsive recomposition must preserve retrieval-state invariants rather than merely hide controls.

### Reusable output — Retrieval Contract

For material retrieval surfaces specify corpus, user need, browse-vs-search justification, searchable fields/scope, draft/submitted query, suggestions, filter cardinality/logic/application, sort/ranking, active-state visibility, URL/history/privacy, result identity, pagination model, all retrieval states, no-result recovery, stale-response protection, list/detail continuity, input/accessibility behavior, responsive/localization stress, analytics/privacy and human-validation requirements.

### Primary/current evidence checked 2026-09-15

- WHATWG HTML Living Standard — search input, GET form submission and navigation/history;
- WHATWG URL Standard — URL/query model;
- W3C WAI-ARIA 1.2 / APG Search Landmark;
- WCAG 2.2 / Understanding 4.1.3 Status Messages;
- latest Design Studio Web W003 status.

---

## Highest-value next integrated block

Proceed to **Responsive Web Interaction, Input Modality & Cross-Device Continuity**.

Required scope:
- viewport/layout width must not be treated as a proxy for input capability;
- pointer/touch/keyboard/mixed-input and hover/no-hover;
- coarse/fine pointer and media-feature limits;
- focus/keyboard continuity through responsive recomposition;
- virtual keyboard and viewport changes;
- orientation and dynamic viewport behavior;
- browser zoom/reflow/text enlargement distinctions;
- touch target/gesture/direct-manipulation implications;
- desktop↔mobile task/state continuity where applicable;
- preservation of 039–042 contracts under recomposition;
- browser/device/human validation boundaries.

This should consume Design Studio W003's adaptation-ownership model but independently validate web-platform/input facts from authoritative standards.

---

# Design Studio relationship

Latest specialist-file state checked 2026-09-15:

- **Web Design W001–W003: PRACTICE/CRITIQUE; Foundation NOT PASSED.** W003 adds responsive/adaptive recomposition and an executable Playwright harness; measured results remain OPEN because its environment could not execute repository code.
- W003 model: `task → relationship → stress signal → owner → adaptation → invariant → validation`.
- Web's largest remaining Foundation gaps include IA/navigation, component/page systems, complete task surfaces, integrated state/accessibility and broader browser/device transfer.
- Layout/Interaction Stage 1 PASS remains reusable peer evidence, with human/production/platform validation still bounded.

### Current outgoing handoff

Future MintTap work should consume **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract + 041 Form/Transaction Contract + 042 Retrieval Contract** together.

Web Design should validate retrieval under responsive composition, long KO/EN content, real zoom, keyboard/touch, filter disclosures, result-list/detail return, focus restoration and dynamic status exposure. Layout/Interaction should challenge immediate-vs-explicit apply, stale-response handling, selection continuity and partial/stale/outcome-unknown states.

No Design Studio canonical file was edited.

---

# Important unknown MintTap facts

Real project decisions still require verified evidence for actual app inventory/launch priorities, user goals, store-linked URLs, support/contact/account/deletion behavior, subscription/payment model, privacy/data-control procedures, support backend, actual support corpus size/growth, search need/query patterns, backend/index freshness, analytics/privacy constraints, target browsers/devices/inputs/locales and human usability evidence.

Do not infer these from generic app-company patterns.

---

# Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- Stage 1: COMPLETE at intended foundation/practitioner level.
- Stage 2: COMPLETE, 034–038, integration gate passed.
- Stage 3: ACTIVE; 039–042 foundation/practitioner checkpoints passed.
- Current next major work: **Responsive Web Interaction, Input Modality & Cross-Device Continuity**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.
