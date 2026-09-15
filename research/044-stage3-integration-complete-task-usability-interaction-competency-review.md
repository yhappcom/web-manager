# 044 — Stage 3 Integration: Complete-Task Usability & Interaction Competency Review

Status: **STAGE 3 FOUNDATION/PRACTITIONER INTEGRATION GATE — PASS**  
Research date: 2026-09-15  
Scope: integration of studies 039–043 for `minttap.app` public company/app/support/governance tasks.

## Why this block exists

039–043 separately established reusable contracts for action/state/recovery, task/journey/cognition, forms/transactions, retrieval/list-detail and responsive/input continuity. The remaining Stage 3 question is not whether another interaction pattern can be collected. It is:

> Can the Web Manager combine these models to diagnose and specify a complete user task without confusing structural correctness, accessibility requirements, system truth and actual measured usability?

This is deliberately an integration/competency review rather than a sixth isolated UX topic.

---

## RELATED DOMAIN CHECK

### Web Manager evidence integrated

- 038 Stage 2 integration and Page Contract;
- 039 Interaction Contract;
- 040 Task/Journey Contract;
- 041 Form / Transaction Contract;
- 042 Retrieval Contract;
- 043 Responsive/Input Continuity Contract.

### Design Studio evidence/status checked

Latest `yhappcom/design-studio/progress/WEB_STATUS.md` (2026-09-15) now reports **W001–W005**, not W001–W003. Web Design remains Stage 1 PRACTICE/CRITIQUE / Foundation NOT PASSED. W004 covers IA/URL/navigation/history/direct entry; W005 covers component/page systems, native semantics and independent state dimensions; W006 is planned around complete task surfaces.

Latest Layout/Interaction specialist status remains **Stage 1 PASS / Stage 2 entry audit next**, explicitly without claiming production/browser/device/AT/human validation.

### Overlap decision

**INTEGRATION + TRANSFER PREPARATION, not duplicate study.** Web Manager owns the product/task/system contract and evidence boundary. Design Studio Web W006 should own visual/compositional implementation and browser-context practice for complete task surfaces.

---

# 1. SOURCE — usability is an outcome of use, not a property proved by a specification

ISO 9241-11:2018 remains current; ISO reports it was reviewed and confirmed in 2023. Its abstract explicitly says usability is an **outcome of use** and provides a framework for understanding usability rather than a specific design/evaluation method.

Primary source checked 2026-09-15:
- ISO 9241-11:2018 — https://www.iso.org/standard/63500.html

### SYNTHESIS

A standards-conformant interaction specification can eliminate known failure classes, but it cannot by itself prove that target MintTap users complete a task effectively, efficiently or satisfactorily in their context.

Therefore Stage 3 may pass as a **Foundation/Practitioner competency gate** while production usability remains OPEN pending representative human-task evidence.

### MINTTAP DECISION

Never label source review, heuristic critique, automated browser assertions or Design Studio critique as “usability tested” unless actual users/tasks and method support that claim.

---

# 2. SOURCE — complete-task accessibility crosses multiple interaction layers

Current W3C WCAG/WAI material treats keyboard access, focus order/visibility, reflow, labels/instructions, error identification/suggestion/prevention and status messages as distinct requirements. W3C's Forms curriculum likewise connects forms to responsive design, information design, interaction design and prototyping rather than treating accessibility as a field-level add-on.

Primary sources checked 2026-09-15:
- WCAG 2 overview/current publication status — https://www.w3.org/WAI/standards-guidelines/wcag/
- WAI Forms Design curriculum — https://www.w3.org/WAI/curricula/designer-modules/forms-design/
- WCAG 2.2 normative specification — https://www.w3.org/TR/WCAG22/

### SYNTHESIS

A task can have correctly labeled controls and still fail because focus is obscured after responsive recomposition, an async result is never announced, validation destroys entered data, a disclosure loses context, or Back returns to a reset list.

The correct unit of review is therefore the **complete task/state path**, not an isolated component screenshot.

---

# 3. Complete-task integration model

The Stage 2 and Stage 3 contracts combine into:

`entry context → goal/orientation → available action → prerequisite/input → transition → pending/validation → authoritative outcome → next task or recovery → continuity`

Every consequential step must answer five different questions:

1. **User question:** What am I trying to accomplish and what do I believe will happen?
2. **Interface question:** What action is discoverable/operable now?
3. **System question:** What state transition was requested, accepted and committed?
4. **Recovery question:** What can I do if the result is invalid, failed, interrupted or unknown?
5. **Continuity question:** Does the task survive navigation, responsive recomposition, input change or legitimate interruption?

### Failure diagnosis

Do not collapse these into “bad UX.” Diagnose the broken contract:
- wrong task or unnecessary step → Journey failure;
- unclear action/state/feedback → Interaction failure;
- invalid question/validation/commit protocol → Form/Transaction failure;
- lost query/filter/list context → Retrieval failure;
- geometry/input change destroys task/state → Responsive/Input failure;
- wrong page/destination/context → Stage 2 IA/Page failure.

---

# 4. Scenario matrix — app evaluation → store action

## Task contract

External/search/company entry → identify app → understand material value/conditions → determine platform availability → choose correct store action → leave website with correct expectation.

### Required invariants

- app identity and platform/store destination remain unambiguous;
- material claims derive from canonical product truth rather than visual marketing copy;
- CTA promise matches destination;
- unavailable platform is represented as unavailable, not as a dead or misleading CTA;
- essential evaluation information is not hover-only;
- narrow/zoom/localized layouts preserve claim-condition-action relationships.

### Failure examples

- iOS and Android buttons visually identical but one links to the wrong product;
- CTA says “Download” although destination is a waitlist;
- decisive compatibility condition appears only after store departure;
- mobile layout hides evidence/conditions solely to reduce page length.

### OPEN / VALIDATION

Actual MintTap app inventory, launch platforms, store URLs, claims and conversion priorities remain unknown. Human evidence is required before claiming the chosen hierarchy optimizes evaluation/conversion.

---

# 5. Scenario matrix — support entry → resolution → escalation

## Task contract

Store/search/direct support entry → preserve app context → identify problem/task → self-service attempt → resolution or explicit escalation → recoverable return.

### Required invariants

- direct entry identifies company/app and article/task scope;
- support article states applicable conditions/version/platform where material;
- self-service instructions expose success/failure branches;
- escalation retains enough context to avoid needless re-entry;
- form validation preserves valid user work;
- pending submission is distinct from confirmed receipt;
- timeout/unknown outcome is not falsely presented as known failure;
- Back or responsive disclosure does not silently discard support context.

### SOURCE relevance

Apple's current App Store Connect model continues to require a Privacy Policy URL for all apps; store-linked web destinations therefore remain operational public contracts rather than decorative pages. Apple also states app privacy responses must remain accurate and up to date.

Primary Apple sources checked 2026-09-15:
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
- https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy

### OPEN

Actual MintTap support channel, service-level expectation, ticket backend and app/version context propagation are not verified.

---

# 6. Scenario matrix — privacy/account-control direct entry

## Task contract

Store/search/direct URL → identify affected app/company → understand control and consequences → authenticate/verify only as justified → request/perform action → distinguish pending from completed deletion/control → explain retained-data exceptions where applicable → recovery/contact.

### SOURCE — current platform boundary

Apple currently requires a privacy-policy URL for all apps and allows an optional public User Privacy Choices URL for data access/deletion/change choices.

Google Play's current Developer Programme Policy says that if an app allows users to create an account within the app, users must be able to request account deletion both in-app and externally through a designated web resource; associated user data must also be deleted subject to stated legitimate retention requirements, and temporary freezing is not deletion.

Primary/current sources checked 2026-09-15:
- Apple App Privacy — https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
- Google Play Developer Programme Policy — https://support.google.com/googleplay/android-developer/answer/17517561

### SYNTHESIS

This flow is a high-value integration test because IA/direct-entry, trust, form semantics, consequential-action protection, authentication, pending/outcome state and recovery all meet in one task.

### CHANGE WATCH / OPEN

Store policies can change. Applicability depends on actual MintTap account behavior. Do not infer that every MintTap app creates accounts or needs the Google deletion flow.

---

# 7. Scenario matrix — form/transaction

Use a support/contact/privacy request as a neutral model without assuming MintTap has that exact form.

### Complete state path

`entry → editing → local validation → authoritative validation → submission requested → pending → confirmed / rejected / known failure / outcome unknown → recovery or next action`

### Competency checks

- every question has a reason and known context is not redundantly requested without justification;
- semantic HTML/native behavior is preferred where it matches the task;
- client validity is not confused with server acceptance;
- field errors identify the problem and support correction;
- valid entries survive unrelated errors;
- conditional branches do not submit stale hidden values;
- review/confirmation is proportional to consequence/reversibility;
- duplicate retry risk is governed by backend/business semantics;
- focus/status behavior remains coherent after errors and async completion;
- virtual keyboard/visual viewport cannot obscure the only route to correction/submit.

### PASS judgment

The Web Manager can now specify and critique the transaction protocol without prescribing one visual component library. Production correctness still depends on backend/API behavior and browser/AT validation.

---

# 8. Scenario matrix — retrieval → detail → Back/resume

### Complete state path

`information need → query/scope → results → filter/sort → select → detail → Back/resume`

### Required invariants

- draft and submitted query are not conflated during async retrieval;
- search, filter, sort and ranking remain distinct concepts;
- success-empty is distinct from retrieval failure;
- stale responses cannot overwrite newer query state;
- result identity remains stable enough for selection/detail continuity;
- safe/public retrieval state may be addressable where useful, while sensitive query data is not exposed merely for shareability;
- Back/resume restores meaningful query/filter/sort/list context;
- responsive filter disclosure does not silently reset applied state;
- dynamic result status is exposed appropriately without excessive announcements.

### MINTTAP DECISION

No site-search requirement is created by this gate. Search remains conditional on real corpus/task evidence.

---

# 9. Stress matrix — the same task must survive changing conditions

A complete task should be challenged across independent stress dimensions rather than a single “mobile version”:

| Stress | What must remain true |
| --- | --- |
| narrow layout | task/content/state relationships remain available |
| long KO/EN text | labels/conditions/actions retain meaning without clipping or ambiguity |
| browser zoom/reflow | content/action/focus remain operable and perceivable |
| keyboard | all essential actions operable; focus sequence and restoration coherent |
| touch/coarse pointer | no hover dependency; gesture alternatives/target requirements respected |
| mixed input | switching input does not reset task state |
| on-screen keyboard | focused field/error/action not irrecoverably obscured |
| portrait/landscape | ordinary task remains usable without unjustified orientation lock |
| async delay/failure | pending, known failure and unknown outcome remain distinct |
| interruption/navigation | recoverable state survives where product/system contract promises it |

### VALIDATION boundary

039–043 and this gate establish what to test and why. They do **not** prove Safari/Firefox/mobile/AT/device behavior or human task performance. Those require executable/browser/device/manual/human evidence in later stages or project validation.

---

# 10. Trust and uncertainty are interaction-state properties

Trust is not created by adding badges after the interaction is designed.

### SYNTHESIS

A user loses justified confidence when the system:
- hides material conditions until after commitment;
- says an action succeeded before authoritative confirmation;
- loses entered work without warning;
- makes destructive or privacy controls materially harder than acquisition;
- cannot distinguish “no result” from “system unavailable”;
- changes task meaning across responsive modes;
- presents stale public/store information as current.

Conversely, uncertainty reduction comes from truthful state, consequence, scope, evidence and recovery communication.

### MINTTAP DECISION

Treat trust as an emergent property of the full contract stack, not a standalone visual section.

---

# 11. Stage 3 competency verdict

## Exit capability 1 — critique whether a user can understand, navigate and complete a task

**PASS at Foundation/Practitioner level.** 038–044 now provide a traceable method from entry/task through state, input, validation, retrieval, responsive stress and recovery.

## Exit capability 2 — distinguish visual attractiveness from usability

**PASS conceptually.** ISO's outcome-of-use framing and the contract stack prevent visual polish or source conformance from being mislabeled as measured usability.

## Exit capability 3 — write interaction/state requirements for Design Studio/engineering

**PASS at specification level.** Reusable deliverable stack:

`Page Contract + Task/Journey Contract + Interaction Contract + Form/Transaction Contract + Retrieval Contract + Responsive/Input Continuity Contract`

## Explicit non-PASS claims

Stage 3 closure does **not** mean:
- MintTap production usability is tested;
- WCAG conformance is established;
- screen-reader/AT behavior is validated;
- Safari/Firefox/iOS/Android browser parity is proven;
- conversion is optimized;
- backend transaction/idempotency/session behavior is known;
- actual MintTap support/account/privacy/search flows have been verified.

---

# 12. DESIGN STUDIO HANDOFF

Latest Web Design status has advanced to W001–W005; W006 is explicitly queued for complete task surfaces. This creates a strong handoff boundary.

Provide W006/project work with:
- representative complete-task scenarios from sections 4–8;
- independent state dimensions rather than a generic component state enum;
- long bilingual/zoom/reflow stress cases;
- keyboard/touch/mixed-input and focus-restoration requirements;
- async pending/error/outcome-unknown cases;
- list/detail Back-resume and responsive filter-state cases;
- direct-entry privacy/support/account-control cases.

Web Design should return:
- browser-rendered composition/state evidence;
- failures caused by component/page-system decisions;
- responsive disclosure/focus/history findings;
- native-vs-custom control evidence;
- any contradiction that requires Web Manager to revise the task/system contract.

Layout/Interaction should challenge state ownership and mode transitions, especially pending/invalid/filtered/focused/interrupted conditions.

No Design Studio canonical file is edited by Web Manager.

---

# 13. OPEN / DEPENDENCY / VALIDATION / CHANGE WATCH

## OPEN — MintTap facts

Need real project evidence for app inventory, target audiences/goals, store URLs, support operations, account creation/deletion, privacy controls, subscriptions/payments, search corpus/query need, analytics constraints, authenticated persistence and target browser/device/locale matrix.

## DEPENDENCY

- Design Studio Web W006 and later complete-project exercise for visual/browser transfer;
- engineering/backend contracts for authoritative transaction state, idempotency, persistence and index freshness;
- product/legal/privacy ownership for consequential and regulated flows.

## VALIDATION

Later project gates should include actual browser zoom/reflow, keyboard/focus, touch/mixed input, Safari/Firefox/Chromium, physical iOS/Android where relevant, screen-reader/manual accessibility and representative human-task evaluation.

## CHANGE WATCH

Recheck Apple/Google store-linked web requirements and WCAG/current standards before production release. Apple explicitly requires privacy responses to stay accurate and current; platform policy is not timeless.

---

# Final Stage 3 judgment

**STAGE 3 — USER EXPERIENCE & INTERACTION FOUNDATIONS: COMPLETE AT THE INTENDED FOUNDATION/PRACTITIONER CURRICULUM LEVEL.**

The gate closes because the Web Manager can now model, diagnose and specify complete tasks across content/IA, action/state, cognition, forms, retrieval and responsive/input conditions while maintaining a strict evidence boundary between source-grounded requirements and measured usability.

Next curriculum stage: **Stage 4 — Web Design Literacy.** The first block should integrate Design Studio W001–W006/current Type/Color/Layout evidence into Web Manager judgment about visual hierarchy, composition, typography, color, imagery/product demonstration and component/page-system decisions—without duplicating specialist research or inventing a universal MintTap style.