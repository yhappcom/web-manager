# 039 — Stage 3 User Action, System State, Feedback, Error & Recovery Foundations

Status: **STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT — COMPLETE**
Research date: 2026-09-15
Scope: transferable UX/interaction judgment for the public website and future web applications of a company shipping Apple and Android apps under `minttap.app`.

## Why this block exists

Stage 2 established where information belongs, how users find it, and what each page must communicate. That is not enough to determine whether a person can successfully *act*.

A page may have correct information architecture and still fail because:

- a user cannot tell what is actionable;
- an action appears accepted when it is only pending;
- validation explains neither the error nor the correction;
- a destructive action has no proportional prevention/recovery strategy;
- a retry can duplicate a remote side effect;
- a keyboard or touch path can enter a state that it cannot leave;
- navigation or interruption destroys task context;
- an interface is visually polished but leaves system state ambiguous.

The unresolved Stage 3 foundation question is therefore:

> **How should Web Manager reason from a user's goal through action, state transition, feedback, commitment, failure and recovery before visual styling or implementation details are chosen?**

This study deliberately transfers and independently checks Design Studio Interaction evidence rather than recreating it.

---

# RELATED DOMAIN CHECK

## Web Manager evidence reused

- 031 — browser document/runtime foundations;
- 032 — rendering/state/navigation foundations;
- 034–038 — task IA, content truth, direct entry, page contracts and recovery-oriented page systems.

Stage 2's integrated contract was:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`

Stage 3 now deepens **task completion** and **recovery**.

## Design Studio evidence checked

Latest repository state on 2026-09-15:

- `research/interaction/007-interaction-agency-feedback-errors.md`;
- `research/interaction/015-directness-state-modes-reversibility.md`;
- `research/interaction/I001-navigation-history-focus-restoration-interruption.md`;
- `research/interaction/I002-latency-pending-optimistic-retry.md`;
- `progress/LAYOUT_STATUS.md` — Interaction through I006, Foundation not yet passed;
- `progress/WEB_STATUS.md` — **W001 is now complete** at Practice/Critique; W002 is next.

This is an important correction to the previous Web Manager dependency note: Web Design is no longer pre-substantive. `W001` now supplies a Web-native relationship/constraint model and bounded browser practice. It still does not provide production interaction PASS.

### Transfer choice

**REUSE + INDEPENDENT PRIMARY-SOURCE CHECK + WEB-MANAGER SYNTHESIS.**

Design Studio owns reusable interaction/design expertise. Web Manager needs enough of that evidence to specify project behavior, identify system/API dependencies, distinguish usability from aesthetics, and know what must be validated by Design Studio/engineering.

---

# 1. SOURCE — usability is an outcome of use, not a visual property

ISO 9241-11:2018 remains the current ISO usability definitions/concepts standard; ISO reports that the 2018 edition was reviewed and confirmed in 2023. The standard frames usability in relation to use of systems/products/services rather than as an inherent visual property.

Primary source checked 2026-09-15:
- ISO 9241-11:2018 — https://www.iso.org/standard/63500.html

## SYNTHESIS

Web Manager must distinguish at least three questions:

1. **Visual presentation** — what the interface looks like;
2. **Interaction design** — what actions/states/transitions/recovery mechanisms exist and how they are communicated;
3. **Usability outcome** — whether specified users can accomplish specified goals in the relevant context with acceptable effectiveness, efficiency and experience.

A beautiful interface can be unusable. A technically accessible control can still create poor task performance. A familiar visual pattern is not proof that the underlying state model is correct.

## VALIDATION

Claims about actual user effectiveness, efficiency, comprehension, confidence or preference require human evidence in the target context. Standards and expert inspection can identify defects/risks but cannot prove real MintTap usability.

---

# 2. SOURCE — affordance and signifier are not synonyms

Don Norman's author-published ACM Interactions essay distinguishes **affordances** from **signifiers**. Affordances concern possible action relationships; signifiers are perceivable cues that help people discover what can be done. Norman explicitly warns that designers often call a visible cue an “affordance” when they are actually discussing a signifier.

Primary author source:
- Don Norman, *Signifiers, not affordances* — https://jnd.org/signifiers-not-affordances/

## SYNTHESIS — action possibility and action discoverability are separate gates

For a web interface ask separately:

- **Possible:** can this user/input mode actually perform the action?
- **Discoverable:** what cue tells the person the action exists?
- **Predictable:** what does the person expect the action to affect?
- **Available now:** is the action valid in the current state?

Examples:

- A card may technically be clickable but have no reliable signifier.
- A disabled-looking button may still activate because styling and operational availability disagree.
- A swipe action may exist for touch but be undiscoverable and have no keyboard/pointer equivalent.
- A text link may clearly signify navigation even though it has little visual “button” styling.

## MINTTAP DIRECTION

Interaction requirements should not say only “make this obvious.” Specify the cue/label, operational availability, object affected and equivalent input routes.

---

# 3. SOURCE — feedback communicates state, result, warning and correction opportunity

Apple's current Human Interface Guidelines describe feedback as helping people understand current status, available next actions, action results, warnings and opportunities to correct mistakes. Apple also recommends matching interruption level to severity rather than presenting every status as an alert.

Primary source checked 2026-09-15:
- Apple HIG — Feedback: https://developer.apple.com/design/human-interface-guidelines/feedback

W3C WCAG 2.2 separately requires certain status messages to be programmatically determinable without necessarily receiving focus (4.1.3).

Primary source:
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/

## SYNTHESIS — feedback and interruption are different decisions

For every state change decide:

1. **what the user must know**;
2. **when they must know it**;
3. **whether it requires attention or only availability**;
4. **whether focus/context must move**;
5. **what channel(s) carry the information**.

Useful classes:

- persistent/passive state — e.g. last synced time;
- transient status — e.g. saved;
- pending/progress state;
- blocking error;
- warning before consequence;
- completed action requiring next step;
- recovery-required condition.

### Failure mode

“Show a toast” is not an interaction requirement. It names a presentation mechanism without defining state importance, persistence, announcement, focus behavior or recovery.

---

# 4. USER ACTION–SYSTEM STATE CONTRACT

The core Stage 3 model is:

`goal → action possibility/signifier → constraint → articulation → requested transition → accepted? → pending/working? → committed state → feedback → recovery/reversal → continuity`

For any significant interaction, document the following.

## 4.1 Goal

What outcome is the user trying to achieve?

Do not start from the control. “Click Save” is an implementation action; “preserve my edited support request” is the goal.

## 4.2 Object/scope

What domain object or resource is affected?

Examples:
- one support request;
- one account;
- one privacy choice;
- one app context;
- one filter/query;
- one uploaded attachment.

Scope errors are interaction errors even if the button works technically.

## 4.3 Signifier and label

What tells the user an action is possible, and what result does the label promise?

Stage 2's “label = destination promise” extends here to **action promise**.

## 4.4 Constraints

What actions are impossible, invalid, unavailable, unsafe or conditional right now?

A constraint may be:
- intrinsic/domain-based;
- permission-based;
- validation-based;
- network/system availability-based;
- workflow-state-based;
- policy/legal consequence-based.

Do not silently collapse all unavailable actions into a generic disabled state when the reason matters to task completion.

## 4.5 Articulation/input

How is the intent expressed?

Examples: click/tap, keyboard activation, typing, selection + action, drag, native form submission.

Input mechanism must not be confused with intent.

## 4.6 Requested transition

What state change does the input request?

Examples:
- idle → editing;
- editing → validating;
- valid → submit requested;
- submit requested → pending;
- pending → confirmed;
- pending → known failure;
- pending → outcome unknown.

## 4.7 Commitment level

What does the visible result actually mean?

Possible distinctions:
- preview;
- local transient state;
- local persisted state;
- queued for synchronization;
- server accepted;
- authoritative confirmed;
- externally/irreversibly committed.

Do not visually label an earlier commitment level as a later one when the difference can affect user decisions.

## 4.8 Recovery/reversal

What can the user do if the result is wrong, incomplete or uncertain?

Possible mechanisms:
- edit/correct;
- cancel before commit;
- undo after commit;
- retry after known failure;
- verify status before retry when outcome is uncertain;
- restore preserved input;
- escalate/contact support.

## 4.9 Continuity

What survives navigation, reload, interruption, device change or return?

State is plural: draft data, filter, scroll, focus, pending operation and authoritative data do not necessarily share one lifecycle.

---

# 5. SOURCE — web forms already contain a native interaction model

The WHATWG HTML Living Standard (updated 2026-09-14 at time of research) defines typed form controls, labels/form association, constraints such as `required`, `min`, `max`, `pattern`, validation state/APIs, form submission behavior and disabled/readonly semantics.

Primary source:
- WHATWG HTML — Forms/input: https://html.spec.whatwg.org/multipage/forms.html
- input/constraint APIs: https://html.spec.whatwg.org/multipage/input.html

W3C's Forms Tutorial, updated 2026-03-27, recommends labels, grouping, instructions, validation, user notifications and logical multi-page grouping. It also emphasizes asking only for information required for the process.

Primary W3C guidance:
- https://www.w3.org/WAI/tutorials/forms/

## SYNTHESIS — a form is a stateful task, not a collection of fields

A production form has at least:

`understand task → provide/choose data → validate → identify/correct error → review if consequence requires → submit → pending → success/failure/unknown → recover or continue`

It therefore needs decisions about:

- labels/instructions;
- required vs optional data;
- grouping/order;
- format tolerance;
- when validation occurs;
- input preservation;
- submission availability;
- duplicate submission behavior;
- asynchronous commitment;
- success confirmation;
- failure recovery;
- navigation/interruption policy.

## MINTTAP DIRECTION

For support/contact/privacy/account-control flows, begin from semantic native form behavior and extend only where project requirements justify it. Do not assume a custom JavaScript field system is the baseline merely because the final visual design is custom.

---

# 6. SOURCE — error prevention, identification, suggestion and recovery are different layers

WCAG 2.2's Input Assistance criteria distinguish error identification, labels/instructions, error suggestions and prevention for high-consequence submissions. W3C's current forms guidance also recommends accessible user notification and correction paths.

Primary/current sources:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Forms — validation: https://www.w3.org/WAI/tutorials/forms/validation/
- W3C Forms — notifications: https://www.w3.org/WAI/tutorials/forms/notifications/
- W3C ARIA21 technique, updated 2026-04-27: https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA21.html

## SYNTHESIS — error handling stack

Use the narrowest mechanism that actually solves the problem:

1. **avoid unnecessary opportunity for error** — do not ask irrelevant data;
2. **constrain** impossible values/actions where appropriate;
3. **accept reasonable equivalent formats** when the domain permits;
4. **detect** an error at a useful time;
5. **identify** exactly what is wrong;
6. **suggest** correction when known;
7. **preserve work** so correction does not require re-entry;
8. **review/confirm** when consequence justifies it;
9. **undo/reverse** when the operation is safely reversible;
10. **escalate/recover** when automated correction is impossible.

These are not interchangeable.

### Counterexample

A confirmation dialog on every Save action is not inherently “safer.” It can add interruption while doing nothing to prevent invalid input, preserve work, explain a failure or make the committed effect reversible.

---

# 7. SOURCE — reversibility must have a predictable target

Apple's current Undo/Redo guidance emphasizes that people need to predict what will be undone/redone and perceive the result of that reversal.

Primary source checked 2026-09-15:
- Apple HIG — Undo and redo: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo

W3C form validation guidance likewise gives review/confirmation and undo as different mechanisms for critical or reversible actions.

## SYNTHESIS — consequence × reversibility determines protection strategy

Before choosing confirmation, undo, delay window or review step, classify:

- consequence severity;
- whether the effect can be reversed;
- reversal time window;
- whether reversal itself has side effects;
- whether another actor/system can observe or depend on the result;
- whether the user can verify the target before committing.

### Practical classes

**Low consequence + easily reversible:** immediate action + clear result + undo may be preferable.

**High consequence but reviewable:** review/confirmation before commit may be required.

**Irreversible/external effect:** prevention and explicit scope/result are more important because “Undo” may be impossible.

**Outcome unknown:** verify before retry if duplicate commitment could be harmful.

No universal rule says “destructive = confirmation dialog.”

---

# 8. SOURCE + TRANSFER — asynchronous UI needs more than loading/success/failure

Design Studio I002 independently assembled primary literature, Apple guidance, WCAG status semantics and RFC 9110 idempotency into an asynchronous model. Web Manager adopts its high-value distinction and connects it to website operations.

Relevant primary source independently retained:
- RFC 9110 §9.2.2 Idempotent Methods: https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods
- Apple HIG — Loading: https://developer.apple.com/design/human-interface-guidelines/loading
- WCAG 2.2 status messages: https://www.w3.org/TR/WCAG22/#status-messages

## SYNTHESIS — authoritative async states

For consequential remote work distinguish at least:

- **idle**;
- **accepted locally**;
- **pending**;
- **progressing** where progress is genuinely measurable;
- **confirmed**;
- **known failed**;
- **canceled** under a defined contract;
- **outcome unknown**.

`timeout` does not logically imply `failed`.

The remote system may have committed before communication was lost.

## MINTTAP DIRECTION

Any future web flow involving account deletion, privacy requests, subscription/account operations, message sending, uploads, purchases or other duplicate-sensitive effects must document:

- authoritative success owner;
- duplicate/retry semantics;
- operation identity/idempotency if available;
- status verification path;
- user-visible pending/unknown/recovery behavior.

A spinner and a Retry button are not sufficient specifications.

---

# 9. Optimistic UI is a state contract, not a performance decoration

## SYNTHESIS from I002 + Stage 1 HTTP/state foundations

Showing the intended result before authoritative confirmation is appropriate only when the product has a defined reconciliation policy.

Before using optimistic state, specify:

- local optimistic result;
- how pending is represented;
- authoritative convergence;
- rollback/conflict result;
- retry/reconciliation;
- what happens if the user navigates away;
- whether another device/session can contradict the local state.

### Failure mode

Immediate green “Success” followed by silent rollback is not merely poor feedback; it misrepresents commitment state.

---

# 10. Modes and hidden state increase interaction risk

Design Studio Study 015 uses primary HCI evidence on mode errors and state modeling. Web Manager retains the transferable rule:

> If the meaning of the same action changes because of persistent context, the current context must be salient and its entry/exit policy explicit.

Examples of mode/state risk on the web:

- bulk-selection mode;
- edit vs view state;
- preview vs published state;
- account/company switch;
- locale/environment switch;
- filter/query state that materially changes what a destructive bulk action affects.

## MINTTAP DIRECTION

For any mode specify:

- entry trigger;
- persistent indication;
- affected controls/actions;
- exit trigger;
- whether navigation/reload preserves it;
- what happens to incomplete work;
- focus/restoration behavior.

Do not encode consequential mode solely through color, subtle icon change or transient animation.

---

# 11. Navigation and interruption are interaction state, not only IA

Stage 2 correctly separated hierarchy from browser history. Design Studio I001 extends this into restoration/interruption.

## SYNTHESIS

A task transition can preserve or lose several independent states:

- semantic location;
- browser traversal history;
- hierarchy context;
- draft/work state;
- presentation state such as filters/scroll;
- focus/selection;
- transient overlay;
- data commitment/pending state.

“Preserve state” is therefore underspecified.

## MINTTAP DIRECTION

For future interactive MintTap web surfaces, a page/flow contract should explicitly say what happens after:

- browser Back/Forward;
- direct/deep-link entry;
- reload;
- temporary navigation away and return;
- modal/dialog dismissal;
- authentication interruption if applicable;
- network disconnect/reconnect where state can be pending.

---

# 12. Pointer, touch and keyboard routes should preserve task semantics

WCAG 2.2 requires keyboard operability for functionality where applicable and adds Dragging Movements (2.5.7), requiring functionality that uses dragging to have a non-dragging pointer alternative unless dragging is essential or provided by the user agent.

Primary source:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

## SYNTHESIS

Input equivalence does **not** mean pixel-identical interaction.

It means the essential task outcome remains achievable with an appropriate interaction contract across supported input modes.

Examples:

- drag reorder may also expose Move Up/Down or another discrete mechanism;
- hover-revealed actions must not be hover-only;
- a pointer-only custom control must not make keyboard completion impossible;
- touch targets can be recomposed without changing action scope or commitment semantics.

Detailed accessibility conformance remains Stage 5; Stage 3 establishes the interaction requirement now so inaccessible state models are not baked into later visual design.

---

# 13. Disabled, unavailable and pending are not synonyms

## SYNTHESIS

A control may be unavailable because:

- prerequisite data is missing;
- permission is lacking;
- the current workflow state forbids the action;
- a conflicting operation is pending;
- service capability is unavailable;
- the action is permanently unsupported.

These states have different recovery possibilities.

### Web Manager rule

When the reason matters, provide enough information for the user to understand **what is required to make progress**. Do not use disabled styling as the sole explanation of a workflow constraint.

A pending operation may justify preventing duplicate activation but should still communicate the operation already in progress.

---

# 14. Interaction failure taxonomy

Before redesigning a flow, classify the failure.

## A. Discoverability/signifier failure

Action exists but users cannot reasonably discover it.

## B. Mapping/scope failure

Users cannot tell what object/result an action affects.

## C. Constraint failure

Invalid action is allowed, or unavailable action has no understandable reason/path forward.

## D. State-visibility failure

Current/pending/selected/mode/commitment state is hidden or ambiguous.

## E. Feedback failure

The system changes but does not communicate acceptance/result at the right level.

## F. Commitment-truth failure

UI says completed when the authoritative effect is only local/pending/unknown.

## G. Validation failure

Input is rejected without precise identification/correction support, or valid equivalent input is unnecessarily rejected.

## H. Prevention/protection mismatch

The protection mechanism is disproportionate or does not address the actual risk.

## I. Recovery failure

User work is lost, retry is unsafe, undo target is ambiguous, or escalation is absent.

## J. Continuity/restoration failure

Navigation/interruption destroys required draft/filter/focus/pending context.

## K. Input-mode failure

One input can enter/complete/exit a state that another supported input cannot.

## L. Semantic-exposure failure

Visible state/action exists but name/role/value/status/focus behavior does not expose the same meaning programmatically.

This taxonomy is intentionally separate from visual-style critique.

---

# 15. Reusable Interaction Contract for MintTap projects

Before Design Studio or engineering implements a consequential flow, Web Manager should be able to supply or review:

| Contract item | Question |
| --- | --- |
| User goal | What real outcome is the person seeking? |
| Object/scope | What exact resource/account/app/data is affected? |
| Action promise | What does the label/signifier imply will happen? |
| Availability | When is the action valid and why might it be unavailable? |
| Input routes | Pointer, touch, keyboard, native submission, other? |
| State model | What user-facing states/transitions exist? |
| Commitment | Preview/local/persisted/queued/remote/external? |
| Feedback | What is shown/announced and at what interruption level? |
| Validation | What can be prevented/detected/corrected? |
| Consequence | What is the cost of an incorrect/duplicate action? |
| Reversibility | Cancel/undo/edit/compensate/none? |
| Async policy | Pending/progress/failure/outcome-unknown? |
| Retry policy | Safe retry, known-failure retry, or verify-before-retry? |
| Continuity | What survives navigation/reload/interruption? |
| Focus/restoration | Where does keyboard/AT interaction continue? |
| Recovery/escalation | What can the user do when automation fails? |
| Evidence | What must be browser-tested, API-tested or human-tested? |

This is not intended as paperwork for trivial links. Use it proportionally for interactions where ambiguity, data loss, duplicate effect, accessibility or recovery risk matters.

---

# 16. Competency checks

## Scenario A — support request form

Weak specification:
> User fills fields and clicks Submit; show success or error.

Professional model:
- identify required information only;
- label/group controls semantically;
- tolerate valid formats where possible;
- local validation can assist but server remains authoritative for server-side rules;
- preserve entered data after correctable failure;
- distinguish submission accepted/pending/confirmed;
- if response is lost, determine whether duplicate submission is safe before offering Retry;
- expose success/failure appropriately without unnecessary focus interruption;
- maintain app context and escalation path.

**PASS diagnosis:** form UX depends on state + backend operation semantics, not field styling.

## Scenario B — account deletion request

This is high consequence and potentially asynchronous.

Required questions:
- exact account/app scope;
- what data/effects deletion covers;
- review/confirmation required by product/policy;
- whether request is immediately reversible/cancelable;
- authoritative completion owner;
- pending duration/status;
- whether repeated submission is safe;
- what “Cancel” means before/after remote processing;
- completion proof and support path.

**PASS diagnosis:** do not use optimistic “Account deleted” merely because request submission succeeded.

## Scenario C — filter controls on support search

Low consequence, usually reversible.

Likely model:
- immediate visible result update can be appropriate;
- filter state remains inspectable and removable;
- Back/history policy depends on whether query state is a meaningful restorable location;
- keyboard/touch can reach equivalent result;
- loading one result region should not necessarily block global navigation.

**PASS diagnosis:** protection/interruption should be proportional to consequence.

## Scenario D — Delete article/bookmark-like low-cost local object

If truly reversible, immediate delete + clear Undo may create better continuity than repeated confirmation.

If deletion has remote irreversible consequences, this model changes.

**PASS diagnosis:** interaction pattern follows the data/consequence contract, not the word “Delete” alone.

---

# 17. SOURCE / SYNTHESIS / OPEN summary

## SOURCE — verified

1. ISO 9241-11:2018 remains current after review/confirmation and frames usability as an outcome of use.
2. Norman distinguishes affordances from signifiers; visible cues are not synonymous with possible action.
3. Apple current HIG treats feedback as communication of state/results/warnings/correction opportunities and recommends severity-proportional interruption.
4. WHATWG HTML defines substantial native form/input/constraint-validation behavior.
5. W3C current forms guidance covers labeling, grouping, instructions, validation, notification and task reduction.
6. WCAG 2.2 distinguishes input assistance/error criteria, keyboard requirements, dragging alternatives and status-message exposure.
7. RFC 9110 conditions automatic retry safety on request semantics/idempotency rather than UI preference.
8. Apple Undo/Redo guidance emphasizes predictable reversal target/result.

## SYNTHESIS — retained professional judgment

1. UX is an action-state-recovery contract, not a collection of controls.
2. Discoverability, action possibility, mapping, availability and commitment truth are separate gates.
3. Feedback should communicate the user's required state while minimizing unnecessary interruption.
4. Forms are stateful task systems.
5. Prevention, validation, confirmation, undo and recovery solve different problems.
6. Async interactions need explicit pending/confirmed/failed/outcome-unknown semantics.
7. Retry policy depends on API/business-effect semantics.
8. Optimistic UI requires reconciliation and rollback/conflict policy.
9. State preservation is plural and must name which state survives which interruption.
10. Input routes may differ physically while preserving task semantics.

## OPEN — not yet known/validated for MintTap

- which website surfaces will contain authenticated or account-changing interactions;
- whether any MintTap app supports web account deletion execution vs request/instruction only;
- support/contact submission backend and duplicate semantics;
- actual privacy-request workflow and service-level expectations;
- actual authentication/session model;
- whether any web flows require uploads, payments, subscriptions or other high-consequence side effects;
- production framework/router/form stack;
- actual supported browser/device/input matrix;
- human usability evidence for target users;
- screen-reader and cross-browser behavior of future implementation.

Do not invent these details from generic patterns.

---

# DESIGN STUDIO DEPENDENCIES / HANDOFFS

## Incoming evidence consumed

- Interaction 007: agency/feedback/error foundation;
- Interaction 015: state/modes/commitment/reversibility;
- I001: history/focus/restoration/interruption;
- I002: latency/pending/optimism/retry/outcome uncertainty;
- W001: Web-native relationship/constraint/browser-participation model.

## Outgoing project handoff

Future Design Studio Web/Interaction work for MintTap should receive the **Interaction Contract** above plus Stage 2 Page Contract.

For consequential flows it should explicitly validate:

1. action signifier and label match the actual operation;
2. action scope remains clear after responsive recomposition;
3. visual state matches programmatic and operational state;
4. pending/confirmed/failed/unknown states are distinguishable when materially different;
5. disabled/unavailable reasons do not create dead ends;
6. validation identifies and supports correction without unnecessary re-entry;
7. destructive/high-consequence protection is proportional to consequence/reversibility;
8. retry/undo/cancel labels match backend reality;
9. keyboard/pointer/touch routes preserve task completion and exit/recovery;
10. focus/history/restoration behavior is specified rather than emergent;
11. long Korean/English feedback/error labels survive reflow;
12. browser-native form/control behavior is preserved unless a custom replacement has a demonstrated reason and equivalent contract.

## Boundary

Web Manager specifies product/task/state/recovery requirements and system dependencies. Design Studio determines and validates interaction/compositional expression. Engineering owns implementation correctness and must expose API/system semantics needed to make the UI truthful.

No Design Studio canonical file is modified by this study.

---

# CHANGE WATCH

Recheck before production decisions:

- WCAG 2.2 remains the current W3C Recommendation while WCAG 3 is still an evolving Working Draft as of 2026;
- WHATWG HTML is a Living Standard and form/platform behavior can evolve;
- Apple/Android platform design guidance can change;
- browser native controls/validation/accessibility mappings require actual target-browser validation.

---

# Stage 3 checkpoint judgment

**PASS — first Stage 3 foundation/practitioner block.**

The Web Manager can now distinguish visual appearance from interaction/usability; model action→state→commitment→feedback→recovery; separate signifier/availability/scope; treat forms as tasks; diagnose prevention/validation/recovery separately; reason about async pending/outcome uncertainty; and specify continuity/input-mode requirements without pretending that reading proves human usability.

This is not Stage 3 completion.

## Highest-value next integrated block

Proceed to **User Goals, Task/Journey Modeling, Cognitive Load, Recognition/Recall, Expectation & Friction**.

Reason:

039 explains *how an individual interaction should behave*. The next prerequisite is deciding **which interactions and steps should exist at all**, how task sequences impose cognitive/decision cost, when progressive disclosure helps or harms, and how friction should be classified as necessary protection vs accidental burden vs manipulative obstruction.

Do not jump yet to conversion optimization or aesthetic microinteraction.