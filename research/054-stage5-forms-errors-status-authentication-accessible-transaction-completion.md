# 054 — Forms, Errors, Status Messages, Authentication & Accessible Transaction Completion

Date: 2026-09-16  
Stage: 5 — Accessibility  
Level: Foundation / Practitioner integrated checkpoint

## Why this block now

051 established barrier/conformance scope, 052 semantic exposure, and 053 operability/focus. Stage 3 already established general form/transaction UX. The unresolved accessibility prerequisite is therefore not generic form design; it is whether a complete support/account/governance transaction remains understandable, correctable, perceivable and completable when input, validation, asynchronous state, authentication and consequential submission are combined.

Core model:

`task/process → input meaning → label/instruction → entry → validation → error identification/suggestion → correction/recovery → async/status communication → authentication → review/error prevention → completion confirmation → complete-process evidence`

---

## 1. Forms are processes, not field inventories

**SOURCE** — W3C WAI's Forms Tutorial (updated 27 March 2026) treats accessible forms as a combination of labeling, grouping, instructions, validation, notifications, multi-page progression and custom-control considerations. WCAG's definition of a process is a series of required user actions needed to complete an activity.

Primary: https://www.w3.org/WAI/tutorials/forms/  
Normative WCAG 2.2: https://www.w3.org/TR/WCAG22/

**SYNTHESIS** — A form can have individually accessible controls and still fail as a transaction. Accessibility must be evaluated across the state path, including what happens after submission, errors, retries, authentication challenges and completion.

**MINTTAP DIRECTION** — For future `minttap.app` support/account/governance work, review the process state graph, not only markup at the initial form state.

---

## 2. Labels, instructions and constraints are different obligations

**SOURCE** — WCAG 2.2 SC 3.3.2 Labels or Instructions is Level A. WAI recommends labels that identify control purpose and instructions where input requirements need explanation. Native `<label>` is the normal mechanism for labelable HTML controls.

Primary: https://www.w3.org/WAI/tutorials/forms/labels/  
Primary: https://www.w3.org/TR/WCAG22/#labels-or-instructions

**SYNTHESIS** — A concise field name, a format constraint, a required-state indication and contextual help are not interchangeable. Accessible-name computation alone does not prove that all information needed to enter a valid value is available at the right time.

Failure example: a field is programmatically named “Verification code”, but the six-digit expiry/format rule is shown only after the first failed submission. The name may be valid while the transaction remains unnecessarily error-prone.

**MINTTAP DIRECTION** — Define for each input: purpose/name, required/optional state, pre-entry constraint, format/example when material, and any relationship to grouped controls. Do not use placeholder text as the sole durable instruction.

---

## 3. Validation has three distinct jobs

### 3.1 Prevent avoidable invalid entry

**SOURCE** — WAI's validation guidance recommends accommodating legitimate input formats and notes that HTML/native validation can assist common inputs. Client-side validation improves feedback but does not replace server-side validation for security.

Primary: https://www.w3.org/WAI/tutorials/forms/validation/

**SYNTHESIS** — Accessibility validation and security validation overlap operationally but prove different things. Client validation can reduce user effort; server validation protects trust boundaries. Neither should be cited as evidence for the other.

### 3.2 Identify the error

**SOURCE** — WCAG 2.2 SC 3.3.1 Error Identification (A): when an input error is automatically detected, the item in error must be identified and the error described to the user in text.

Primary: https://www.w3.org/TR/WCAG22/#error-identification

**SYNTHESIS** — `red border`, `aria-invalid=true`, or an error icon alone is not a complete error description. Programmatic state can assist AT, but the user still needs understandable error information.

### 3.3 Suggest correction when known

**SOURCE** — SC 3.3.3 Error Suggestion (AA) requires correction suggestions when known unless doing so would jeopardize security or the content's purpose. WAI's notification tutorial recommends concise error text and guidance on correction.

Primary: https://www.w3.org/TR/WCAG22/#error-suggestion  
Primary: https://www.w3.org/WAI/tutorials/forms/notifications/

**SYNTHESIS** — “Invalid value” and “Use YYYY-MM-DD” have materially different recovery value. Error identification tells the user what failed; suggestion reduces the work required to recover.

---

## 4. Error discovery must work globally and locally

**SOURCE** — WAI recommends combining overall submission feedback with inline feedback. An error summary can reference each affected label and link to the corresponding control; inline messages can be associated with individual controls. WAI also notes that moving focus to the first invalid input can be convenient after submission.

Primary: https://www.w3.org/WAI/tutorials/forms/notifications/

**SYNTHESIS** — Error accessibility has at least four layers:

`existence → discovery → association → recovery`

A visible inline error far below the viewport can exist without being discovered. A top summary can be discovered without identifying which control it concerns. Focus movement can help but must not substitute for persistent error structure.

**MINTTAP DIRECTION** — For nontrivial forms, define both transaction-level error feedback and field-level association, plus the focus destination after failed submission. Preserve already valid user input unless there is a security or validity reason not to.

---

## 5. Status messages are not the same as focus changes

**SOURCE** — WCAG SC 4.1.3 Status Messages (AA) concerns messages that report success/results, waiting/progress or errors without causing a change of context. Such messages must be programmatically determinable through role/properties so AT can present them without receiving focus. Examples include “Searching…”, result counts and completion states.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

**SYNTHESIS** — `message exists in DOM ≠ message is announced ≠ focus should move to message`.

Use a status mechanism for non-context-changing updates; use deliberate focus management when the task genuinely changes context or requires immediate interaction. Indiscriminately focusing every success/error toast can interrupt the user's task and distort focus order.

**SYNTHESIS — async state model**:

`idle → pending → success | recoverable error | terminal error`

Each transition needs a user-visible and, where applicable, programmatically exposed consequence. “Save” becoming disabled with only a spinner is insufficient if the user cannot determine that work is pending or whether it completed.

**OPEN** — The actual MintTap frontend framework and its live-region/toast implementation are unknown. No runtime announcement behavior is claimed.

---

## 6. Redundant entry is a process-level accessibility issue

**SOURCE** — WCAG 2.2 added SC 3.3.7 Redundant Entry (A). Information previously entered by or provided to the user and required again in the same process must be auto-populated or available to select, except where re-entry is essential, security-required or the prior information is no longer valid. Browser autocomplete alone is not sufficient for this criterion. A process can span domains, including a third-party provider.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html

**SYNTHESIS** — This turns process architecture into accessibility architecture. Repeating an email, account identifier or support-case information on a later step is not merely friction if the same process could carry the value forward.

**MINTTAP DIRECTION** — Map data ownership across multi-step and third-party boundaries before implementation. Minimize re-entry without creating unnecessary persistence or privacy exposure.

**OPEN** — MintTap's real account/support/deletion flows and third-party processors are not yet verified.

---

## 7. Accessible authentication is not “we support passwords”

**SOURCE** — WCAG 2.2 SC 3.3.8 Accessible Authentication (Minimum) is Level AA. A cognitive-function test cannot be required for any authentication step unless an allowed alternative/mechanism/exception applies. W3C explicitly identifies password-manager support and copy/paste as mechanisms that reduce memory/transcription burden. Blocking paste or autofill can fail the criterion unless another conforming path exists. Manual transcription of one-time codes is likewise problematic; paste/autofill must be possible for a code-based path. All steps in multi-factor authentication need a conforming path.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html

**SYNTHESIS** — Security strength and cognitive burden are separate axes. Making a user manually type a password or OTP is not inherently stronger authentication; it can instead disable assistive mechanisms.

**MINTTAP DIRECTION** — If `minttap.app` ever includes authentication, preserve password-manager/autofill/paste mechanisms and evaluate the complete MFA/recovery path. Do not introduce puzzle/transcription requirements without a conforming alternative.

**BOUNDARY** — SC 3.3.8 focuses on authentication of existing users. W3C notes that similar techniques can improve account creation, but the criterion's scope should not be misstated.

**OPEN** — Whether MintTap's company website will authenticate users at all is unknown.

---

## 8. Consequential submissions require error prevention

**SOURCE** — WCAG 2.2 SC 3.3.4 Error Prevention (Legal, Financial, Data) is Level AA. For legal/financial transactions, modification/deletion of user-controllable stored data, or test submissions, at least one of these must apply: submission is reversible; entered data is checked with opportunity to correct; or the user can review, confirm and correct before final submission.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html

**SYNTHESIS** — Not every Save action needs a confirmation dialog. The criterion targets serious consequences, and unnecessary confirmations can themselves add friction and habituation. The design question is consequence severity + reversibility + correction opportunity.

**MINTTAP DIRECTION** — Treat account deletion, destructive stored-data operations and any future consequential transaction as explicit state machines with review/reversal/correction evidence. Do not infer that current `minttap.app` contains such a flow.

---

## 9. Completion feedback is part of transaction accessibility

**SOURCE** — WAI's Forms Tutorial recommends notifying users of successful task completion as well as errors. SC 4.1.3 can apply when completion is communicated as a status message without context change.

**SYNTHESIS** — A request is not experientially complete merely because the server returned 2xx. The user needs to know whether the requested action completed, failed, remains pending, or requires another step.

For consequential actions, completion evidence should answer as applicable:
- what happened;
- whether it is final or pending;
- what happens next;
- whether/how it can be reversed or corrected;
- whether a reference/receipt is available.

---

## 10. Reusable Accessible Transaction Contract

For every material form/process, record:

| Field | Required review |
| --- | --- |
| Task/process | user goal, start/end, required steps, domains/third parties |
| Inputs | purpose, native control, accessible name, required state |
| Instructions | constraints/formats/examples available before error where needed |
| Grouping | programmatic + visual relationships |
| Entry burden | repeated information, autofill/select/carry-forward behavior |
| Validation | client UX vs server trust-boundary responsibility |
| Error identification | text description + affected item |
| Error suggestion | actionable correction when known/safe |
| Error discovery | summary/inline strategy + focus destination |
| State retention | what valid input survives failure/retry |
| Async | pending/success/error states and announcement mechanism |
| Authentication | cognitive test, paste/autofill/password manager/MFA/recovery path |
| Consequence | reversible/checked/review-confirm-correct safeguard |
| Completion | success/result/next-step communication |
| Responsive | no instruction/error/status/focus path lost on narrow/reflow state |
| Evidence | static semantics → browser keyboard/focus → accessibility tree/live region → AT → complete process |

Claim boundary:

`accessible fields < accessible form state < accessible transaction < accessible complete process`

Passing an isolated component does not establish the next level.

---

## 11. Representative failure diagnoses

1. **Error shown only by red outline** → identification/Color reliance failure; add textual identification and programmatic association.
2. **Error text exists but user remains at submit button below a long form** → discovery/focus-flow failure.
3. **AJAX save succeeds visually but AT receives no update** → status exposure failure.
4. **Every live keystroke produces assertive announcements** → notification overload; semantic mechanism exists but interaction is harmful.
5. **OTP split into six boxes and full-code paste fills only first box** → authentication transcription burden.
6. **Step 3 asks again for information entered at Step 1** → evaluate SC 3.3.7; carry forward/select unless exception applies.
7. **Delete account immediately executes from a single accidental activation with no reversal/check/review** → evaluate SC 3.3.4 and task consequence.
8. **Server rejects input and clears unrelated valid fields** → recovery burden and potentially redundant-entry problem within the same process.
9. **Custom toast receives focus for every background save** → conflates status announcement with focus/context change.

---

## 12. Design Studio dependency / handoff

Latest canonical Web specialist state read before this block: `progress/WEB_STATUS.md`, governance sync 2026-09-15 — Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED. W006 integrated search/filter/table/edit async/recovery execution is explicitly OPEN; W005 semantic-control runtime is also OPEN.

**DEPENDENCY — Web Design**
- W006 or successor runtime should include an accessible transaction slice: labeled native inputs, invalid submission, error summary/field association, focus after error, pending state, recoverable failure, success state and announcement exposure.
- Test live-region/status behavior in actual Chromium accessibility representation; do not infer announcement from DOM presence.
- If authentication specimen is later added, verify paste/autofill behavior rather than only visual OTP layout.

**DEPENDENCY — Layout/Interaction**
- Model failed submit, pending, recoverable error, success and destructive confirmation/reversal as explicit states.
- Define focus destination and preserved input at each transition.

**DEPENDENCY — Type**
- Stress long Korean/English validation/help/authentication strings; truncation must not remove correction instructions.

**DEPENDENCY — Color**
- Error/success/required/disabled/pending states cannot rely on hue alone; preserve distinction under relevant user color environments.

Web Manager retains complete-process scope, data/re-entry requirements, authentication/accessibility policy, consequential-action safeguards and evidence/claim boundaries. No Design Studio canonical file is edited here.

---

## 13. Verified facts vs synthesis vs open questions

### VERIFIED / SOURCE
- WCAG 2.2 is a W3C Recommendation and includes SC 3.3.7 and 3.3.8 added in 2.2.
- SC 3.3.1 and 3.3.2 are A; 3.3.3, 3.3.4, 3.3.8 and 4.1.3 are AA; 3.3.7 is A.
- SC 3.3.7 applies to repeated information in the same process with stated exceptions; browser autocomplete alone is not sufficient.
- SC 3.3.8 permits mechanisms such as password managers and paste and applies through authentication steps.
- SC 3.3.4 requires reversibility, checking/correction, or review/confirmation/correction for its scoped consequential actions.
- Status messages that do not change context need programmatic exposure so AT can present them without focus.

### SYNTHESIS
- Accessible transaction quality is a state-path property, not a form-field property.
- Error handling requires existence, discovery, association and recovery.
- Async accessibility should be modeled as state transitions with appropriate visual/programmatic feedback rather than generic toasts.
- Security validation and accessibility validation must cooperate but are not interchangeable evidence.

### OPEN / VALIDATION
- Actual MintTap web forms, authentication, account deletion, support and privacy-control processes are unknown.
- Actual framework/component library, server validation, live-region behavior, password-manager/autofill compatibility and third-party process boundaries are unknown.
- No browser/AT/device or disability-informed human test has been executed for MintTap production.
- Applicable legal accessibility obligations by jurisdiction remain a separate verified legal-policy task; WCAG study does not establish legal compliance.

---

## 14. Checkpoint

**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

The Web Manager can now distinguish field semantics from transaction accessibility; diagnose instruction, validation, error, status, redundant-entry, authentication and consequential-submission failures; and specify a complete-process evidence contract without claiming unperformed runtime/AT validation.

Highest-value next block: **055 — Dynamic Content, Dialogs, Disclosure, Composite Widgets & Accessible Application State**. This should integrate ARIA live/dynamic behavior, dialogs/transient layers, disclosure and composite-widget state while reusing 052–054 and Design Studio runtime gaps rather than repeating generic component theory.

## Primary references

- W3C, WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C WAI, Forms Tutorial (updated 2026-03-27) — https://www.w3.org/WAI/tutorials/forms/
- W3C WAI, Labeling Controls — https://www.w3.org/WAI/tutorials/forms/labels/
- W3C WAI, Validating Input — https://www.w3.org/WAI/tutorials/forms/validation/
- W3C WAI, User Notification — https://www.w3.org/WAI/tutorials/forms/notifications/
- W3C WAI, Understanding SC 3.3.7 Redundant Entry — https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html
- W3C WAI, Understanding SC 3.3.8 Accessible Authentication (Minimum) — https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
- W3C WAI, Understanding SC 3.3.4 Error Prevention — https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html
- W3C WAI, Understanding SC 4.1.3 Status Messages — https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
