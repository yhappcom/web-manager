# 053 — Keyboard, Focus, Input Modality & Operable Interaction Accessibility

Date: 2026-09-15  
Stage: 5 — Accessibility  
Status: **FOUNDATION/PRACTITIONER CHECKPOINT PASS**

## Why this block now

051 established barrier/conformance scope and 052 established semantic exposure. The next prerequisite is operability: a correctly named and mapped control is still inaccessible if a user cannot reach, operate, leave, track, or recover from it with the input interface they use.

This block reuses Stage 3 interaction/responsive knowledge and Design Studio W005/W011 gaps rather than repeating generic UX theory.

## Core model

`task/function → available input paths → focusability/reachability → activation/navigation → visible/predictable focus → state transition → focus continuation/restoration → task outcome → runtime/AT/human evidence`

Input equivalence is not pixel or gesture sameness. The obligation is that the underlying task remains operable without imposing an inaccessible input technique.

---

## 1. Keyboard accessibility is about functionality, not merely tabbability

### SOURCE

WCAG 2.2 SC 2.1.1 Keyboard (Level A) requires all content functionality to be operable through a keyboard interface without requiring specific timing for individual keystrokes, except where the underlying function requires path-dependent input. It explicitly distinguishes the underlying function from the input technique and does not discourage additional pointer input.

Source: https://www.w3.org/WAI/WCAG22/Understanding/keyboard

SC 2.1.2 No Keyboard Trap (Level A) requires that when keyboard focus can enter a component, it can also leave using a keyboard interface; if a nonstandard exit method is required, the user must be advised of it.

Source: https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html

### SYNTHESIS

`focusable != operable != usable task`

A control can appear in the Tab sequence but fail activation, expose a stale state, trap focus, or strand the user after DOM changes. Conversely, WCAG 2.1.1 does not literally require every pointer-visible control to itself be keyboard focusable if equivalent functionality is available by keyboard. For ordinary app-company UI, however, native multi-input controls are usually the simpler and more discoverable baseline.

### MINTTAP DIRECTION

Test keyboard accessibility by complete function/task, not by counting `tabindex` or proving that focus can touch each element.

---

## 2. Sequential focus order must preserve meaning and operation

### SOURCE

WCAG 2.2 SC 2.4.3 Focus Order (Level A) requires focusable components to receive focus in an order that preserves meaning and operability when sequential navigation order affects them.

Source: https://www.w3.org/WAI/WCAG22/Understanding/focus-order

WAI-ARIA APG keyboard-interface guidance states that the default tab sequence follows DOM order and strongly advises against positive `tabindex` values for authoring an alternate sequence. It distinguishes Tab/Shift+Tab movement between components from arrow-key movement within many composite widgets.

Source: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

### SYNTHESIS

Visual layout order, DOM/reading order, and sequential focus order are separate layers that should normally reinforce the same task model. CSS responsive rearrangement can make an originally logical DOM order confusing without changing the DOM itself.

Positive `tabindex` is not a robust repair for a structurally wrong DOM: it can create a keyboard order that diverges from reading/navigation order and becomes difficult to maintain across responsive variants.

### Review rule

`semantic/reading order → DOM order → visual recomposition → sequential focus order`

If these diverge, document why and validate the resulting task, rather than patching the symptom with numeric focus ordering.

---

## 3. Focus must be visible, persistent, predictable and not author-obscured

### SOURCE

WCAG 2.2 SC 2.4.7 Focus Visible (Level AA) requires a mode in which keyboard focus is visible. W3C's current Understanding document also notes that focus indication is visual information and can be subject to SC 1.4.11 Non-text Contrast.

Source: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible

WCAG 2.2 added SC 2.4.11 Focus Not Obscured (Minimum) (Level AA): when a component receives keyboard focus, it must not be entirely hidden by author-created content. Sticky headers/footers, cookie banners and persistent overlays are representative risks.

Source: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum

SC 2.4.13 Focus Appearance is Level AAA, not an AA requirement; it specifies stronger size/change-of-contrast requirements for authored focus indicators.

Source: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html

### SYNTHESIS

A focus system has at least four independent obligations:

1. **existence** — there is an active interaction point;
2. **visibility** — sighted keyboard users can perceive it;
3. **spatial availability** — authored overlays do not hide it;
4. **predictability/continuity** — after an action, focus lands somewhere task-logical rather than silently collapsing to an arbitrary location/body.

Do not claim WCAG AA requires the exact AAA focus-indicator geometry. AAA is useful as a stronger design target but must retain its conformance-level label.

---

## 4. Focus management is state management

### SOURCE

WAI-ARIA APG keyboard-interface guidance emphasizes maintaining visible/predictable focus and managing cases where the focused element is hidden or removed. Its dialog and composite patterns provide pattern-specific focus behavior, but APG is guidance/examples rather than WCAG itself.

Source: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

### SYNTHESIS

Programmatic focus should answer a task-state transition, not decorate an animation. Common transitions requiring an explicit focus decision include:

- opening/closing a modal task;
- validation failure;
- destructive deletion/removal of the focused item;
- route/view changes in a client-side application;
- disclosure or dynamic result insertion where the next interaction point changes;
- async completion/error where the prior target disappears or becomes unavailable.

A useful state invariant is:

`before action focus → action/state transition → resulting task context → intended next focus → visible confirmation/recovery`

Focus restoration to the invoker is common after transient dialogs, but it is not a universal rule: if the invoker was removed or the completed task logically moves elsewhere, the next meaningful target must be chosen from the resulting state.

This directly reuses Design Studio W013 evidence that route identity, transient task layer and focus restoration require separate assertions; it does not elevate that Chromium surrogate to MintTap production proof.

---

## 5. Native controls reduce authored keyboard burden; custom composites increase it

### SOURCE

WAI-ARIA APG explicitly states that browsers do not provide keyboard support merely because ARIA is applied to custom GUI components; authors must implement required keyboard support. APG describes common composite conventions: Tab moves between components while arrow keys commonly move within radio groups, tablists, menus, grids and similar composites. It documents roving `tabindex` and `aria-activedescendant` as distinct focus-management techniques.

Source: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

### SYNTHESIS

This strengthens 052's rule:

`custom semantics → custom behavior burden → focus/state synchronization burden → larger runtime/AT regression surface`

Do not turn a set of ordinary links/buttons into a menu/grid/tab composite simply because the visual design resembles one. Composite semantics imply learned keyboard conventions and state relationships.

### MINTTAP DIRECTION

For product navigation, store links, support navigation, disclosure, forms and governance actions, prefer the simplest native interaction model that expresses the task. Use composite widgets only when the composite interaction itself provides material task value.

---

## 6. Focus and selection are not the same state

### SOURCE

APG distinguishes keyboard focus from selected state. Focus is the current interaction point; selection can persist while focus moves elsewhere. It warns that selection-follow-focus can be harmful when moving focus triggers expensive loading or page refreshes.

Source: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

### SYNTHESIS

Design and code must not use one visual/programmatic state to stand in for both focus and selection/current state. This connects directly to Stage 4 Color: focus, selected, current, pressed and disabled are separate semantic roles even if some visual tokens overlap.

For any tab/filter/list selection design, specify whether navigation merely moves focus or also commits selection. Automatic activation must be evaluated against latency and task consequences.

---

## 7. Keyboard equivalence does not exhaust input-modality accessibility

### SOURCE

WCAG 2.2 SC 2.5.2 Pointer Cancellation (Level A) limits activation on pointer down-events unless cancellation/undo/reversal or an essential exception applies.

Source: https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation

SC 2.5.7 Dragging Movements (Level AA) requires functionality using dragging to have a single-pointer alternative without dragging unless dragging is essential or user-agent controlled. W3C explicitly notes that keyboard accessibility alone does not automatically satisfy this criterion.

Source: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements

WCAG 2.2 SC 2.5.8 Target Size (Minimum) (Level AA) sets a 24×24 CSS-pixel target-size baseline with defined spacing/equivalent/inline/user-agent/essential exceptions.

Source: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/

### SYNTHESIS

Accessibility must not be reduced to a binary mouse-vs-keyboard matrix. Touch, stylus, switch-like keyboard interfaces, speech/voice pointer emulation and users who alternate modalities expose different failure modes.

`keyboard alternative` and `single-pointer non-drag alternative` are separate obligations.

### App-company examples

- screenshot carousel: swipe/drag alone is insufficient if authored functionality depends on it; provide operable controls where applicable;
- reorderable support/admin list: keyboard move controls do not by themselves satisfy the non-drag single-pointer requirement;
- tiny icon-only external-store link: semantic naming can be correct while target geometry remains a motor-access barrier;
- destructive action on pointer-down: accidental activation/recovery must be considered independently of keyboard support.

These are diagnostic examples, not claims that MintTap currently implements these patterns.

---

## 8. Responsive recomposition must preserve operability invariants

### SYNTHESIS grounded in Stage 3 + WCAG focus/input requirements

Responsive design can change more than geometry. A desktop toolbar may become an overflow menu; visible labels may become icon-only; a side panel may become a modal sheet. Each transformation can change focus entry/exit, naming, target geometry, state discoverability and task sequence.

Required responsive invariants include:

- the same essential task remains reachable;
- focus does not jump into hidden/inert content;
- hidden variants are not accidentally left in the active focus sequence;
- opening a transient layer establishes a coherent interaction context;
- closing/removing it returns or advances focus logically;
- visible and programmatic selected/current/expanded state stay synchronized;
- keyboard, pointer and touch paths converge on the same underlying task state.

This extends the Stage 3 Responsive/Input Continuity Contract with explicit accessibility evidence requirements.

---

## 9. Reusable Operability / Focus Contract

For each interactive component or complete process, record:

| Field | Question |
| --- | --- |
| task/function | What outcome must remain operable? |
| native interaction baseline | What behavior does native HTML/user agent already provide? |
| keyboard path | How is the function reached, operated and exited? |
| sequential order | Does focus order preserve meaning/operation? |
| internal navigation | Is this a composite; what keys and focus model apply? |
| focus indicator | How is current focus visibly distinguishable? |
| obscuration risks | Can sticky/overlay/transient content hide focus? |
| state distinction | Are focus/selected/current/pressed/disabled distinct? |
| focus transition | After open/close/delete/route/error/success, where does focus go and why? |
| pointer activation | Can accidental pointer activation be cancelled/undone as required? |
| drag/gesture alternative | Is equivalent single-pointer non-drag operation required/provided? |
| target geometry | What SC 2.5.8 condition/exception applies? |
| responsive invariant | What must survive component transformation? |
| static evidence | Markup/ARIA/focusability checks available? |
| browser runtime | Tab/Shift+Tab/keys/focus state/scroll/overlay behavior executed? |
| AT/device evidence | Which combinations remain untested? |
| process evidence | Can the complete task be finished/recovered? |
| open/human evidence | What usability/disability-informed validation remains? |

### Review heuristic

`function → native behavior → input paths → focus path → state transition → focus continuation → responsive variant → complete-task validation`

Do not start with “make everything tabindex=0.”

---

## 10. Design Studio dependency / handoff

Latest `progress/WEB_STATUS.md` checked 2026-09-15: Web Design remains **Stage 1 PASS / Stage 2 PRACTICE, NOT PASSED**. Its highest-value executable gaps still explicitly include W005 native-vs-custom keyboard/focus/semantic execution and W011 accessible-name/target/enlargement/forced-color icon runtime. W013 provides partial Chromium navigation/history/focus evidence but not MintTap production, true HTTP route, AT, Safari/Firefox or physical-device proof.

### Outgoing handoff

**Web Design**
- W005 execution should compare native vs custom controls across Tab entry/exit, activation keys, visible focus, computed semantics, state synchronization and focus after state changes.
- W011 should add target-size conditions and input-path checks to accessible-name/enlargement/forced-color runtime.
- Integrated specimens should test sticky/overlay focus obscuration and responsive hidden-variant focus leakage.

**Layout / Interaction**
- Treat focus destination/restoration as an explicit transition in interaction state diagrams.
- Distinguish focus from selected/current/pressed state and specify modal/transient entry/exit behavior.

**Color**
- Focus indication must remain visually distinguishable from selected/current/error state and survive relevant user color environments; do not use color-state coincidence as proof.

**Type**
- Label truncation/removal under responsive variants can change task discoverability even when focus mechanics remain valid; include real KO/EN labels in later runtime transfer.

Web Manager retains complete-process scope, input-equivalence obligations, conformance-level boundaries, MintTap browser/AT/input matrix and release claim governance.

---

## 11. Verified facts vs synthesis vs open questions

### VERIFIED / SOURCE

- WCAG 2.2 SC 2.1.1 Keyboard and 2.1.2 No Keyboard Trap are Level A.
- SC 2.4.3 Focus Order is Level A; SC 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured (Minimum) are Level AA; SC 2.4.13 Focus Appearance is Level AAA.
- SC 2.5.2 Pointer Cancellation is Level A; SC 2.5.7 Dragging Movements and SC 2.5.8 Target Size (Minimum) are Level AA.
- WCAG's keyboard requirement concerns functionality and allows a path-dependent exception only where the underlying function requires it.
- Keyboard operability does not by itself satisfy Dragging Movements' single-pointer non-drag requirement.
- ARIA roles do not automatically implement custom-widget keyboard behavior.
- APG distinguishes Tab navigation between components from pattern-specific internal composite navigation and distinguishes focus from selection.

### SYNTHESIS

- Operability should be reviewed as a complete focus/state path rather than a tabbability inventory.
- Focus management is part of interaction state management.
- Positive tabindex is a poor architectural repair for DOM/reading-order problems.
- Responsive component substitution needs focus/input invariants, not merely equivalent pixels.
- Custom composite widgets create a materially larger keyboard/focus/state/runtime validation burden than suitable native controls.
- Keyboard, pointer cancellation, drag alternatives and target geometry are related but independently testable obligations.

### OPEN

- Actual MintTap interactive component/process inventory.
- Actual DOM/focus order, sticky layers, dialogs, carousels, custom controls or drag interactions.
- Frontend framework/router behavior and focus-management implementation.
- Target browser/OS/keyboard/AT/touch/speech-input matrix.
- Physical mobile and external-keyboard behavior.
- Complete-process keyboard/AT evidence and disability-informed human evaluation.

No MintTap production accessibility or WCAG-conformance claim is authorized by this study.

---

## 12. Competency check

Checkpoint passes if the Web Manager can:

1. distinguish keyboard functionality from mere focusability;
2. diagnose focus-order, trap, visibility, obscuration and restoration failures;
3. distinguish focus from selection and native from composite keyboard models;
4. explain why keyboard equivalence does not exhaust pointer/drag/target obligations;
5. specify responsive input/focus invariants;
6. produce an Operability / Focus Contract for a complete app-company task;
7. preserve WCAG A/AA/AAA and runtime/human evidence boundaries.

**Result: PASS at foundation/practitioner checkpoint.**

---

## Highest-value next block

054 — **Forms, Errors, Status Messages, Authentication & Accessible Transaction Completion**.

Reason: Stage 3 already established generic form/transaction UX. Stage 5 should now integrate labels/instructions, error identification/suggestion, status announcements, redundant entry, accessible authentication, async/pending states and recovery into complete support/account/governance processes. This is higher value than isolated screen-reader technique study because it connects semantics + keyboard/focus to real app-company transactions and WCAG 2.2's newer cognitive/accessibility requirements.
