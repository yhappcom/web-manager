# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**  
Last sync: 2026-09-15  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play

## Mission state

Build professional Web Manager judgment from first principles through advanced cross-domain reasoning. GitHub is canonical memory; chat is temporary context.

Canonical curriculum: `LEARNING_ROADMAP.md`.

Learning remains intentionally coarse-grained: study several related subtopics deeply, then persist one integrated checkpoint. Major subjects follow:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

---

# Stage 1 — Web Foundations

**COMPLETE — FOUNDATION/PRACTITIONER CURRICULUM GATE PASSED.**

Completed 027–033 covering Web/Internet/URL/Origin, DNS, HTTP, TLS/browser trust, HTML/CSS/JS/DOM/accessibility tree, rendering/state/navigation and end-to-end integration.

Stage 1 remains available for advanced reopening in later SEO, performance, security, accessibility and operations stages.

---

# Stage 2 — Website Anatomy / Content / Information Architecture

**COMPLETE — FOUNDATION/PRACTITIONER CURRICULUM GATE PASSED.**

Completed 034–038 covering task-based anatomy/content ownership, content modeling/lifecycle/cross-channel truth, navigation/findability, page systems/comprehension and integrated Company/App/Support/Governance competency.

Integrated Stage 2 model:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

Reusable handoff: task/destination matrix + content-object/lifecycle model + critical-destination findability matrix + Page Contract + direct-entry/non-happy/localization/reflow/semantic-order constraints.

---

# Stage 3 — UX & Interaction Foundations

**CURRENT MAJOR CURRICULUM STAGE — ACTIVE.**

## 039 — User Action, System State, Feedback, Error & Recovery

`research/039-stage3-user-action-system-state-feedback-error-recovery-foundations.md`

**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Core model:

`goal → action possibility/signifier → constraint → articulation → requested transition → accepted? → pending/working? → committed state → feedback → recovery/reversal → continuity`

Reusable output: **Interaction Contract**.

Retained judgment includes explicit state modeling, prevention/validation/error/correction/confirmation/undo/recovery separation, consequence × reversibility, pending/confirmed/known-failed/canceled/outcome-unknown, timeout ≠ failure, retry/idempotency dependency, optimistic reconciliation, continuity and browser-native-control baseline.

---

## 040 — User Goals, Task/Journey Modeling, Cognition, Expectation & Friction

`research/040-stage3-user-goals-task-journey-cognition-expectation-friction-foundations.md`

**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Core model:

`entry/context → user goal → prerequisites → task/state sequence → decision/commitment → completion / unresolved / abandoned → recovery/escalation`

Reusable output: **Task/Journey Contract**.

Retained judgment:
- critical path means smallest justified work, not fewest clicks/screens;
- working-memory/Hick evidence does not justify magic UI item-count rules;
- reduce unnecessary recall by preserving/externalizing context;
- progressive disclosure follows decision dependency;
- friction is necessary / protective / accidental / manipulative-obstructive;
- conversion alone does not prove usability or informed choice;
- actual cognition/task-performance claims require human validation.

---

## 041 — Forms, Input, Choice, Validation & Multi-Step Transaction Design

`research/041-stage3-forms-input-choice-validation-multistep-transactions.md`

**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

### Core form/transaction model

A form is a task protocol, not a field collection.

`needed information → semantic control/input assistance → draft/choice state → validation assistance → authoritative validation → pending/commit → success/recovery/unknown outcome`

### Retained judgment

- first decide **why a datum is needed** before choosing a control;
- maintain a question protocol: `question → reason → already known? → user must supply? → sensitivity/retention → validation authority → downstream consumer`;
- label, group/legend, instruction/hint and error are distinct semantic roles;
- HTML `type`, `autocomplete` and `inputmode` solve different problems;
- native HTML constraint validation is valuable but cannot establish current domain truth, authorization or server security;
- client-side validation is user assistance, not authoritative acceptance;
- classify validation as native/syntactic, cross-field, domain, authoritative remote, and security/authorization;
- error architecture includes identity, description, correction, local location, overview, focus/announcement, answer preservation and validation authority;
- same-process redundant entry should be eliminated where not essential/security-required; distinguish process-state reuse, browser autofill and account/profile prefill;
- choice controls should encode actual decision cardinality rather than save space;
- conditional questions require lifecycle rules for retained/cleared values, hidden submission, restoration and validation;
- hidden stale branch values must not silently affect current submission state;
- multi-step forms should split by task logic, not a universal one-question-per-page rule;
- progress indicators must represent the real branch/path honestly;
- review/confirmation should scale with consequence × reversibility; do not add review pages to trivial forms automatically;
- submission state distinguishes editing, local invalid/valid, requested, pending, rejected, known failure, confirmed and outcome unknown;
- dynamic status messages require an AT exposure strategy without unnecessary focus theft;
- do not sabotage password managers, autofill, copy/paste or other user-agent assistance in the name of generic “security”;
- upload success must distinguish bytes-sent from server validation/scanning/processing acceptance;
- save/resume is a persistence + identity + privacy + expiry + versioning contract, not one generic feature;
- task completion, not form/HTTP submission alone, defines success.

### Reusable output — Form / Transaction Contract

For material flows specify:
1. user outcome and entry context;
2. why each question/data item is required;
3. source of the value (user/browser/account/system);
4. `type`/purpose/autocomplete/input modality semantics;
5. grouping and choice cardinality;
6. required/optional truth and instructions;
7. validation layers and authority;
8. error summary/local/focus/announcement/preservation;
9. conditional-branch state policy;
10. step/progress model;
11. draft/save-resume contract;
12. review/commit/reversibility requirement;
13. pending/rejected/failure/confirmed/outcome-unknown state;
14. retry/idempotency dependency;
15. accessibility/autofill/paste/input-mode requirements;
16. responsive/localization stress;
17. human validation needed for usability claims.

### Primary/current evidence checked 2026-09-15

- WHATWG HTML Living Standard — forms, autofill and constraint validation;
- W3C WCAG 2.2 and current Understanding guidance for Identify Input Purpose, Input Assistance, Error Identification/Suggestion, Redundant Entry, Error Prevention, Status Messages and Accessible Authentication;
- W3C WAI Forms Tutorial, including labels/grouping/instructions/validation/notifications/multi-page forms;
- GOV.UK Design System current question-page, radio, checkbox, text-input, error-summary and check-answers guidance;
- Apple HIG Text Fields;
- Design Studio Web W001/W002 status and Layout/Interaction Stage 1 status.

---

## Highest-value next integrated block

Proceed to **Search, Filtering, Selection, Results & List/Detail Interaction Foundations**.

Purpose:
- Stage 2 established findability/content architecture but not on-site retrieval interaction;
- 039–041 establish state, journey and form/transaction mechanics;
- app-company/support websites may need users to locate apps, support topics, known issues or documents as content grows;
- search/filter systems introduce query state, scope, ranking, filter cardinality, URL/history continuity, loading/empty/no-result/error states, selection and responsive composition.

Required scope:
- browse vs search vs filter distinctions;
- query/scope/result state;
- search suggestions and user expectations;
- filter controls and selected-filter visibility;
- immediate vs explicit apply semantics;
- URL/history/shareability where justified;
- sorting vs filtering vs ranking;
- list/detail and selection continuity;
- loading/empty/no-results/error differentiation;
- accessibility, keyboard/touch, result count/status exposure;
- responsive/localization stress;
- whether launch-time site search is justified at all.

Do not drift into SEO/search-engine discovery yet; that is Stage 6.

---

# Design Studio relationship

Latest synchronized Design Studio state 2026-09-15:

- coordinator `progress/STATUS.md` is stale relative to specialist files;
- **Layout/Interaction Stage 1 is PASS** in its specialist status; Stage 2 entry audit is next. Human/production/platform validation remains open;
- **Web Design W001 and W002** are PRACTICE/CRITIQUE; Web Foundation is not passed; W003 responsive/adaptive recomposition is next;
- W002 includes bounded Chromium long bilingual + 200%-text stress and local-overflow validation, but explicitly does not prove browser UI zoom, Safari/Firefox parity, screen-reader PASS or complete form-task systems.

### Current outgoing handoff

Future MintTap work should consume **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract + 041 Form/Transaction Contract** together.

Web Design should validate:
- native/custom control choice;
- labels/hints/errors with long KO/EN strings;
- browser zoom/reflow and physical mobile keyboard behavior;
- keyboard/error-summary/local-error navigation;
- autocomplete/autofill/copy-paste/password-manager behavior;
- conditional reveal semantics and sequence;
- progress/back/history behavior;
- state preservation after validation error/back/reload;
- pending/success/status announcements without inappropriate focus theft.

Layout/Interaction should challenge pending/outcome-unknown behavior, conditional state, review/confirmation proportionality, restoration and duplicate-sensitive retry when a real API exists.

No Design Studio canonical file was edited.

---

# Important unknown MintTap facts

Real project decisions still require verified evidence for:
- actual app inventory/launch priorities and user goals;
- current store-linked website URLs;
- whether a public support/contact form is needed;
- account/authentication/deletion behavior;
- subscription/payment model;
- privacy/data-control procedures;
- support backend/escalation workflow;
- fields actually required for support routing;
- file upload requirements;
- backend validation/idempotency guarantees;
- draft/save-resume needs;
- actual audience/accessibility/locales;
- target browser/device/input matrix;
- real human comprehension/usability evidence;
- legal jurisdictions/service classifications.

Do not infer these from generic app-company patterns.

---

# Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- Stage 1: COMPLETE at intended foundation/practitioner level.
- Stage 2: COMPLETE, 034–038, integration gate passed.
- Stage 3: ACTIVE; 039–041 foundation/practitioner checkpoints passed.
- Current next major work: **Search, Filtering, Selection, Results & List/Detail Interaction Foundations**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.
