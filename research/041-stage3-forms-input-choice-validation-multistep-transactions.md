# 041 — Stage 3 Forms, Input, Choice, Validation & Multi-Step Transaction Design

Status: **STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT**  
Research date: 2026-09-15  
Scope: public and authenticated web form/task systems relevant to an Apple/Android app company operating under `minttap.app`.

## Why this block exists

039 established action/state/error/recovery mechanics. 040 established goal/task/journey/cognition/friction judgment. The next unresolved prerequisite is where those two contracts meet a real web task: forms and transactions.

This study therefore does **not** repeat “forms are stateful tasks.” It answers the more operational question:

> What should MintTap ask, how should the browser/user/system share the work, when should input be checked, how should errors be recovered from, and when is a multi-step review/commit flow justified?

A form is treated as a task protocol, not as a collection of fields.

---

# 1. RELATED DOMAIN CHECK

## Existing Web Manager evidence reused

- 035 content objects/canonical truth;
- 037 Page Contract;
- 038 direct-entry/task-completion integration;
- 039 Interaction Contract;
- 040 Task/Journey Contract.

## Design Studio status checked

Latest specialist status re-read 2026-09-15:

- Web Design is Stage 1 PRACTICE/CRITIQUE, Foundation not passed. W001 and W002 exist; W003 responsive/adaptive recomposition is next. Forms/task surfaces remain only partially Web-baselined.
- Layout/Interaction Stage 1 is PASS under its current curriculum. Later human/production/platform validation remains explicitly open. Its reusable evidence includes state/error/recovery, navigation/restoration, async/retry and ownership contracts.

### Boundary

Web Manager owns task necessity, information requirements, semantic/runtime constraints, transaction/state contracts and operational acceptance criteria. Design Studio owns final form/page composition, control presentation, responsive transfer and browser/device interaction validation.

---

# 2. SOURCE — first reduce the amount of user input

W3C WAI's Forms Tutorial states that forms should ask users only for information required to complete the transaction or process and notes that irrelevant/excessive requests increase abandonment risk. GOV.UK's Question Pages guidance independently says teams should know why every question is being asked and request only information actually needed.

Sources checked 2026-09-15:
- W3C WAI Forms Tutorial: https://www.w3.org/WAI/tutorials/forms/
- GOV.UK Design System — Question pages: https://design-system.service.gov.uk/patterns/question-pages/

### SYNTHESIS

The first form-design question is not “which control?” It is:

`why does the system need this fact at this point?`

Every requested datum should have at least one defensible reason:
- task completion;
- routing/disambiguation;
- eligibility;
- security/authentication;
- legal/policy requirement;
- fraud/abuse prevention;
- recovery/contact;
- user-requested personalization.

### MINTTAP DIRECTION

For support/contact/privacy/account-control flows, maintain a **question protocol** before UI design:

`field/question → why needed → source already known? → user must supply? → retention/sensitivity → validation authority → downstream consumer`

If MintTap already knows the app, locale, signed-in account, deep-link source or selected support topic and it is safe/appropriate to reuse that context, do not ask the user to reconstruct it merely because the backend form historically expects it.

---

# 3. SOURCE — label, instructions, grouping and control semantics are different layers

W3C's current Forms Tutorial separates:
- labeling controls;
- grouping related controls;
- instructions;
- validation;
- notifications;
- multi-page forms.

Explicit `<label>` association gives controls programmatic names and expands the clickable target. `<fieldset>` + `<legend>` provides native grouping semantics for related controls such as radio/checkbox groups.

Sources checked 2026-09-15:
- Labels: https://www.w3.org/WAI/tutorials/forms/labels/
- Grouping: https://www.w3.org/WAI/tutorials/forms/grouping/
- Instructions: https://www.w3.org/WAI/tutorials/forms/instructions/

### SYNTHESIS

Do not make one text string perform four jobs accidentally.

A robust field can have:
- **label** — what value/action this control represents;
- **group legend/question** — what decision a set of controls answers;
- **hint/instruction** — format, condition or explanation needed before input;
- **error message** — what is wrong and, where possible, how to correct it.

Placeholder text is not a durable replacement for a label because it disappears as the user enters data. Apple HIG text-field guidance reaches the same practical conclusion: placeholder text can help communicate purpose, but a separate label remains useful because placeholder text disappears during entry.

Source checked 2026-09-15:
- Apple HIG — Text fields: https://developer.apple.com/design/human-interface-guidelines/text-fields

---

# 4. SOURCE — `type`, `autocomplete`, and `inputmode` are separate decisions

The WHATWG HTML Standard explicitly distinguishes these concepts:

- `type` determines what kind of form control the user agent exposes;
- `autocomplete` describes what the value represents and supports autofill semantics;
- `inputmode` indicates the expected input modality/virtual keyboard behavior without changing the semantic data type.

Source checked 2026-09-15:
- WHATWG HTML — Forms introduction/control infrastructure: https://html.spec.whatwg.org/multipage/forms.html
- WHATWG HTML — Form control infrastructure/autofill: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html

WCAG 2.2 SC 1.3.5 additionally requires the purpose of supported user-information inputs to be programmatically determinable. W3C identifies HTML `autocomplete` tokens as a sufficient mechanism in relevant cases.

Sources:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/#identify-input-purpose
- Understanding 1.3.5, updated 2026-06-12: https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose

### SYNTHESIS

Example: an email address field may reasonably use all three dimensions:

- semantic/control behavior: `type=email`;
- meaning for autofill: `autocomplete=email` when the field actually requests the user's email;
- keyboard hint: often implied by `type=email`; explicit `inputmode` may be unnecessary.

Do not select attributes merely to force a keyboard while accidentally changing validation/data semantics.

---

# 5. SOURCE — native HTML already includes a constraint-validation system

HTML defines validation states including missing required value, type mismatch, pattern mismatch, length constraints, range underflow/overflow, step mismatch, bad input and custom errors. It also defines `checkValidity()`, `reportValidity()`, `setCustomValidity()` and interactive validation behavior.

Source checked 2026-09-15:
- WHATWG HTML — Constraint validation: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constraints

### SYNTHESIS

Before building custom validation, classify the rule:

1. **syntactic/native constraint** — missing value, type, range, length, simple pattern;
2. **cross-field rule** — one answer depends on another;
3. **domain rule** — e.g. account is eligible, code exists, state transition allowed;
4. **authoritative remote rule** — requires server/current backend truth;
5. **security/authorization rule** — must be enforced at trusted boundary.

Native browser constraints can solve part of layer 1. They cannot establish current domain truth or authorization.

---

# 6. SOURCE — client-side validation is assistance, not authority

W3C's validation tutorial explicitly states that client-side validation alone does not ensure security and that data also needs server-side validation.

Source checked 2026-09-15:
- W3C WAI — Validating Input: https://www.w3.org/WAI/tutorials/forms/validation/

### SYNTHESIS — two validation objectives

**Early assistance** tries to help the user notice/fix problems before submission.

**Authoritative validation** decides whether the requested transaction is valid and may commit.

They can share rules, but they are not the same trust boundary.

### Operational rule

Never create a UI state implying authoritative acceptance merely because local JavaScript says the field is valid.

For a server-validated transaction the meaningful sequence is closer to:

`draft → local assistance → submit attempt → server validation/authorization → accepted/rejected → commit/pending outcome → confirmed result`

This extends the state model from 039.

---

# 7. SOURCE — error identification and correction are separate obligations

WCAG 2.2 SC 3.3.1 requires automatically detected input errors to identify the item and describe the error in text. SC 3.3.3 requires correction suggestions where known, unless doing so would jeopardize security or purpose.

Sources checked 2026-09-15:
- Understanding 3.3.1: https://www.w3.org/WAI/WCAG22/Understanding/error-identification
- Understanding 3.3.3: https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html

W3C's Forms Tutorial also separates inline and overall notifications, and says users must be notified whether submission succeeded or errors occurred.

Source:
- https://www.w3.org/WAI/tutorials/forms/notifications/

### SYNTHESIS — error architecture

For each detected error decide:
- **identity** — which value/question failed;
- **description** — what is wrong;
- **correction** — what would satisfy the rule, when safe/known;
- **location** — local message near the input;
- **overview** — summary when multiple/off-screen errors exist;
- **focus/announcement** — how keyboard/AT users discover it;
- **preservation** — keep unaffected answers;
- **authority** — browser/client/server/domain source of the rule.

Do not erase correct answers after one field fails.

### Pattern evidence, not universal law

GOV.UK's production design system uses both an error summary at the top and field-local messages, moves keyboard focus to the summary on error pages, and links summary errors to their relevant controls.

Source checked 2026-09-15:
- https://design-system.service.gov.uk/components/error-summary/

This is strong, field-tested pattern evidence but not a normative requirement that every MintTap form must copy GOV.UK's exact component.

---

# 8. SOURCE — prevent redundant entry within a process

WCAG 2.2 SC 3.3.7 Redundant Entry requires information previously entered by or provided to the user during the same process to be auto-populated or available for selection, subject to exceptions such as essential re-entry or security.

Source checked 2026-09-15:
- https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html

### SYNTHESIS

There are three different mechanisms and they should not be confused:

1. **process-state reuse** — reuse information already supplied earlier in this transaction;
2. **browser autofill** — user-agent reuse through `autocomplete` semantics;
3. **account/profile prefill** — application-owned known data.

Each has different privacy, freshness and correction risks.

### MINTTAP DIRECTION

Prefill must remain editable unless the value is truly authoritative/read-only. If an account email is shown as fixed identity, communicate that it is account identity rather than presenting a disabled-looking field without explanation.

---

# 9. Choice controls: encode the actual decision

HTML and W3C grouping semantics give the structural baseline. GOV.UK's current guidance is useful applied evidence:

- radio buttons when exactly one option is selected;
- checkboxes when multiple selections are possible;
- do not rely only on visual differences to communicate selection cardinality;
- preselection can lead users to miss a question or submit an unintended answer;
- conditional reveal is appropriate for simple related questions, while complex follow-up work should move to a clearer subsequent step.

Sources checked 2026-09-15:
- https://design-system.service.gov.uk/components/radios/
- https://design-system.service.gov.uk/components/checkboxes/

### SYNTHESIS

The control should represent the decision model:

- binary independent state → checkbox/toggle-like decision where appropriate;
- one-of-many → radios/select depending option count/content/context;
- many-of-many → checkboxes or richer multi-selection only when justified;
- open value → typed input;
- search/lookup → search/combobox pattern only when the set and task justify it.

Do not use a dropdown merely to save vertical space if users need simultaneous comparison of a small set of meaningful choices.

---

# 10. Conditional questions are task branching, not decorative disclosure

A conditional field introduces state and branching:

`answer A → branch question becomes relevant → answer branch → change A → branch may become irrelevant`

### SYNTHESIS

A conditional question therefore needs policy for:
- whether hidden prior branch data is retained or cleared;
- whether it is submitted when hidden;
- whether returning to the branch restores prior input;
- how validation handles hidden controls;
- how assistive technology is notified of changes;
- whether the branch is simple enough to remain inline.

GOV.UK documents a known issue in which users are not always programmatically notified when conditional radio/checkbox content appears/disappears and explicitly warns that complicated conditional questions confused tested users.

Source:
- https://design-system.service.gov.uk/components/checkboxes/

### MINTTAP DIRECTION

Treat hidden-but-still-submitted stale branch values as a correctness risk. The submitted payload must reflect the user's current decision state, not leftover invisible answers.

---

# 11. Multi-step forms: split by task logic, not a universal one-question rule

W3C recommends dividing long forms into logical stages where useful, repeating overall instructions as needed and indicating progress. It does not establish “one question per page” as a universal requirement.

Source checked 2026-09-15:
- https://www.w3.org/WAI/tutorials/forms/multi-page/

This is consistent with 040's rejection of “one question per page always reduces cognitive load.”

### SYNTHESIS — reasons to split

A new step/page is justified when it materially helps:
- logical grouping;
- branching;
- eligibility gating;
- privacy/security boundary;
- expensive/remote validation;
- review/commit distinction;
- interruption/resume;
- major change in task context.

A new step is weakly justified when it exists only because the database has another object or an internal team owns the next fields.

### Progress truth

If showing progress, it must reflect the real journey. Avoid a fixed “Step 2 of 3” promise when conditional branching can make the total materially different unless the model explains that behavior.

---

# 12. Review-before-commit depends on consequence

WCAG 2.2 SC 3.3.4 requires safeguards for legal/financial transactions, modification/deletion of user-controllable stored data and test-response submission: the action must be reversible, checked with correction opportunity, or reviewable/confirmable before finalization.

Source checked 2026-09-15:
- https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data

GOV.UK's Check Answers pattern is applied evidence that review pages can increase confidence and provide a second chance to catch errors before submission.

Source:
- https://design-system.service.gov.uk/patterns/check-answers/

### SYNTHESIS

Do not add confirmation/review pages to every trivial form. Use consequence × reversibility from 039.

Review becomes more valuable when:
- the commit is high consequence;
- multiple entered facts jointly determine the result;
- correction after commit is costly;
- the result affects account/data/legal/financial state.

For a simple support message, an extra review page may be needless friction. For account deletion or consequential privacy controls, explicit review/confirmation/reversal may be justified or required depending on the actual operation.

---

# 13. Submission, pending, success and failure must be distinct states

A submit button is not the end of the task.

### Transaction state model

`editing`
→ `locally valid/invalid`
→ `submission requested`
→ `pending`
→ one of:
- `rejected with correctable errors`;
- `known failure`;
- `committed/confirmed`;
- `outcome unknown`;
- `canceled where cancellation is real`.

039 already established that timeout does not prove server failure. This form study applies that directly: a network timeout after a deletion/support/payment-like request must not automatically reset the UI to “nothing happened” if the business effect could already have occurred.

### SOURCE — status messages

WCAG 4.1.3 requires qualifying status messages to be programmatically determinable so assistive technology can present them without moving focus.

Source checked 2026-09-15:
- https://www.w3.org/WAI/WCAG22/#status-messages
- https://www.w3.org/WAI/WCAG21/Understanding/status-messages

### SYNTHESIS

“Saving…”, “Message sent”, “3 errors”, “Upload complete” and similar dynamic feedback need an announcement strategy, but not every status should steal focus or become a modal interruption.

---

# 14. Authentication/input assistance: do not sabotage user tools

WCAG 2.2 SC 3.3.8 guidance explains that users must be able to rely on mechanisms such as password managers, copy/paste or non-cognitive authentication alternatives under its conditions. Blocking paste into password or verification-code fields can create a failure unless another compliant method exists.

Source checked 2026-09-15:
- https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html

### SYNTHESIS

For future MintTap authentication flows:
- do not equate “security” with forcing manual transcription;
- allow password-manager/autofill/copy-paste workflows where applicable;
- treat authentication UX and authentication security as jointly constrained but distinct disciplines;
- do not invent account/auth behavior for current MintTap products until actual requirements are known.

---

# 15. File/upload inputs require a larger state model than a filename

This block does not deeply study storage/security scanning, which belongs to later Security/Operations stages. At UX foundation level, an upload can pass through:

`not selected → selected locally → client precheck → uploading → received → server validation/scanning/processing → accepted/rejected → attached/committed`

### SYNTHESIS

Do not display “uploaded successfully” merely because bytes left the browser if the backend still needs to validate type, size, content, ownership or processing. Define which state the message represents.

### OPEN

Production upload guidance requires actual MintTap use cases, permitted file types/sizes, storage provider, malware/content-validation requirements, privacy retention and retry semantics.

---

# 16. Save/resume and interruption are transaction continuity problems

040 established that interruption recovery needs enough evidence to reconstruct location, prior commitment and remaining work.

For forms this becomes explicit:

- what draft data exists;
- where it is stored;
- for how long;
- whether it is account-bound/device-bound/session-bound;
- whether sensitive fields are intentionally excluded;
- what happens after logout/account switch;
- whether the user is told a draft exists;
- whether server-side rules have changed since the draft was saved.

### SYNTHESIS

“Autosave” is not one feature. It is a contract across persistence, identity, privacy, versioning and recovery.

Do not promise save/resume before those boundaries are defined.

---

# 17. Reusable Form / Transaction Contract

Before final design/implementation of a material form, specify:

1. **user outcome** — what task is actually completed;
2. **entry context** — what is already known;
3. **questions/data** — why each is required;
4. **source** — user input / browser autofill / account data / system-derived;
5. **field semantics** — type, purpose/autocomplete, modality/inputmode where appropriate;
6. **group/choice semantics** — cardinality and relationships;
7. **required/optional truth** — no ambiguous asterisk-only convention;
8. **instructions** — format/conditions before error occurs;
9. **validation layers** — native/client/cross-field/server/domain/security;
10. **error contract** — identification, correction, summary/local, focus/announcement, preservation;
11. **branching contract** — relevance, retention/clearing, hidden submission behavior;
12. **step model** — why each step exists and how progress is represented;
13. **draft/resume** — persistence, identity, expiry, sensitivity, version changes;
14. **review/commit** — consequence, reversibility and confirmation requirement;
15. **submission state** — pending/rejected/failed/confirmed/outcome-unknown;
16. **retry/idempotency dependency** — backend/business-effect requirement from 039;
17. **success proof** — what confirms task completion, not merely form submission;
18. **accessibility/input modes** — keyboard/touch/AT/autofill/copy-paste;
19. **responsive/localization stress** — long KO/EN labels/errors, zoom/reflow;
20. **human validation** — tasks/error recovery/comprehension claims requiring users.

---

# 18. Failure taxonomy

Use this before redesigning a form visually.

- **question-necessity failure** — asking for data not needed;
- **known-context failure** — re-requesting safely reusable information;
- **semantic-input failure** — wrong control/type/purpose;
- **label/instruction failure** — purpose or required format unclear;
- **choice-model failure** — UI cardinality disagrees with decision model;
- **grouping failure** — related controls lack clear shared question/context;
- **validation-layer failure** — client result mistaken for server/domain authority;
- **validation-timing failure** — feedback too early/noisy or too late/costly;
- **error-discovery failure** — user cannot find what failed;
- **error-recovery failure** — error identified but correction path unclear;
- **answer-loss failure** — unrelated valid input disappears on error/back/reload;
- **redundant-entry failure** — same-process information unnecessarily retyped;
- **branch-staleness failure** — hidden outdated conditional answer still affects payload;
- **step-fragmentation failure** — arbitrary pages without task reason;
- **progress-truth failure** — progress indicator misrepresents actual path;
- **commitment failure** — consequential submission lacks proportionate protection;
- **pending-truth failure** — UI claims success/failure before authoritative outcome;
- **status-exposure failure** — dynamic result invisible to AT or overly interruptive;
- **resume failure** — draft state cannot be safely reconstructed;
- **tool-blocking failure** — paste/autofill/password-manager/browser behavior unnecessarily defeated;
- **evidence failure** — expert assumption presented as validated human usability.

---

# 19. MintTap application without invented product facts

Likely website categories that can use this framework include:
- support/contact request;
- privacy/data request;
- account-control/deletion if an app actually has accounts;
- newsletter/feedback only if the company chooses to provide them;
- authenticated web tasks only if later products require them.

### MINTTAP DIRECTION

Do **not** create forms simply because a generic company site has them. For example, if support is better handled through a direct email/helpdesk link initially, a custom support form adds data handling, validation, delivery, spam, accessibility, retention and operational obligations.

Form existence itself must pass the task/operations justification gate.

---

# 20. Design Studio dependency / handoff

## To Web Design

Consume the **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract + 041 Form/Transaction Contract** together.

Validate in real browser contexts:
- native versus custom control choice;
- labels/hints/errors under long Korean/English strings;
- 200% text and browser zoom/reflow;
- mobile keyboard and control ergonomics;
- keyboard sequence and error-summary/local-error navigation;
- `autocomplete` and autofill behavior;
- paste/password-manager behavior where authentication exists;
- conditional reveal announcement/sequence;
- progress and back-navigation behavior;
- state persistence after validation error/back/reload;
- pending/success/status announcement without inappropriate focus theft.

W002 already provides bounded Chromium evidence for long bilingual content and 200%-text stress, but it explicitly does not prove actual browser zoom, Safari/Firefox parity or forms as complete task systems. 041 should therefore become input to a future Web form/task-surface study rather than being treated as browser validation.

## To Layout/Interaction

Use existing state/recovery/async evidence to challenge:
- form pending/outcome-unknown behavior;
- conditional state changes;
- review/confirmation proportionality;
- resume/restoration;
- duplicate-sensitive submission/retry where real APIs are involved.

No Design Studio canonical file is edited by Web Manager.

---

# 21. OPEN / VALIDATION / CHANGE WATCH

## OPEN — MintTap facts

Unknown until a real project provides evidence:
- whether any public support form is required;
- account/authentication/deletion model;
- privacy/data-request procedure;
- subscription/payment or financial operations;
- fields genuinely required for support routing;
- file-upload requirement;
- backend validation and idempotency guarantees;
- draft/save-resume need;
- locale/market-specific form requirements;
- retention/security policy for submitted data.

## VALIDATION

Production confidence requires, as applicable:
- semantic HTML inspection;
- keyboard-only completion;
- Safari/Firefox/Chromium and physical mobile checks;
- screen-reader/AT checks;
- browser zoom/reflow;
- autofill/password-manager/copy-paste behavior;
- server-side invalid/expired/conflict scenarios;
- slow/offline/timeout/duplicate-submit behavior;
- localization stress;
- human task/error-recovery evaluation where usability claims matter.

## CHANGE WATCH

Recheck before launch:
- current WCAG/WAI guidance;
- browser form/autofill behavior;
- Apple/Google platform/account policy where a web form is store-linked;
- authentication/security standards when auth flows exist.

---

# 22. Competency checkpoint

A Web Manager passes this block when able to explain and defend:

1. why a field exists before choosing its component;
2. `type` vs `autocomplete` vs `inputmode`;
3. native constraint validation vs authoritative server/domain validation;
4. label vs hint vs group vs error roles;
5. error identification vs correction vs notification;
6. same-process redundant-entry prevention;
7. choice control based on actual decision cardinality;
8. conditional-answer lifecycle and stale-hidden-data risk;
9. multi-step splitting by task logic rather than folklore;
10. review/confirmation according to consequence and reversibility;
11. pending/confirmed/outcome-unknown transaction states;
12. save/resume as persistence/privacy/versioning contract;
13. accessibility/autofill/paste/browser-tool participation;
14. why task completion, not successful HTTP/form submission, is the success criterion.

**Verdict: FOUNDATION/PRACTITIONER CHECKPOINT PASS.**

This establishes a reusable form/transaction model but does not claim production browser, AT or human usability validation for any MintTap flow.

---

# 23. Highest-value next Stage 3 block

Proceed to **Search, Filtering, Selection, Results & List/Detail Interaction Foundations**.

Reason:
- Stage 2 established findability and support/content architecture;
- 039–041 now establish local interaction, journey and transaction mechanics;
- app-company/support websites frequently require users to locate an app, support topic, issue or document among growing content;
- search/filter systems introduce query state, empty/no-result/error/loading states, URL/history continuity, result ranking/scope, multi-select filters and responsive constraints that are not yet integrated at Stage 3.

Do not drift into SEO/search-engine discovery yet; that belongs to Stage 6. The next block concerns **on-site user retrieval interaction**.