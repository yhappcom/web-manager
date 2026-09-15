# 055 — Dynamic Content, Dialogs, Disclosure, Composite Widgets & Accessible Application State

Date: 2026-09-16  
Stage: 5 — Accessibility  
Level: Foundation / Practitioner integrated checkpoint

## Why this block now

051 established barrier/conformance scope; 052 semantic exposure and native-first boundaries; 053 keyboard/focus/input operability; 054 complete transaction accessibility. The next unresolved prerequisite is application state: when content appears, disappears, updates, overlays another task, or coordinates multiple controls, does the visual state remain synchronized with DOM focus, programmatic state, keyboard behavior and assistive-technology exposure?

Core model:

`task state → visible state → DOM/semantic state → focus state → selection/active state → announcement state → input behavior → recovery/continuation → complete-task validation`

This deliberately reuses Stage 3 interaction and Design Studio W005/W006 state models. The new value is the accessibility synchronization contract, not another component catalogue.

---

## 1. Dynamic accessibility is synchronization, not “add ARIA”

**SOURCE** — WAI-ARIA provides roles, states and properties for dynamic content and advanced UI controls. WAI-ARIA 1.2 is a W3C Recommendation (6 June 2023); ARIA 1.3 remains draft work. APG provides authoring guidance for patterns and explicitly defines keyboard/focus/state behavior for widgets.

Primary: https://www.w3.org/WAI/standards-guidelines/aria/  
Normative: https://www.w3.org/TR/wai-aria-1.2/  
Guidance: https://www.w3.org/WAI/ARIA/apg/patterns/

**SYNTHESIS** — A dynamic component has several concurrent representations. Accessibility fails when they diverge even if each representation looks plausible in isolation.

Examples:
- panel is visibly open while `aria-expanded=false`;
- a tab is visually highlighted but `aria-selected` identifies another tab;
- DOM focus remains on a combobox while the visually active option changes, but `aria-activedescendant` does not;
- a modal is visible while background controls remain operable;
- a result count changes visually but its status is never exposed to AT.

**MINTTAP DIRECTION** — Treat visual, semantic, focus, selection, announcement and data state as one synchronized application-state contract.

---

## 2. Disclosure is a small state machine, not a chevron animation

**SOURCE** — APG Disclosure defines a button that toggles content. The control exposes `aria-expanded=true|false`; `aria-controls` is optional. Enter and Space activate the control.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

**SYNTHESIS** — The durable contract is:

`trigger identity + operability + expanded state + controlled content visibility`

A rotating icon is presentation only. If the icon rotates but semantic state or content visibility is stale, the component is inconsistent.

**MINTTAP DIRECTION** — Prefer native button behavior for disclosure triggers. Do not add application-menu semantics to ordinary site navigation simply because it visually “drops down.” WAI's navigation-menu guidance distinguishes site navigation from application menus and recommends alternate reachability for fly-out submenu destinations.

Primary: https://www.w3.org/WAI/tutorials/menus/flyout/

---

## 3. Modal dialog accessibility is an interaction boundary

**SOURCE** — APG Modal Dialog requires focus to move inside when opened, Tab/Shift+Tab to remain within the dialog, Escape to close, and focus normally to return to the invoker when closed unless workflow logic requires another destination. A modal dialog uses `role=dialog`, `aria-modal=true`, and an accessible label. Content outside a modal is inert from the user's interaction perspective.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

**SOURCE** — APG explicitly notes that initial focus is contextual. Large/structured content may warrant focusing a static element near the beginning; irreversible final-step dialogs may warrant the least destructive action; a simple continuation dialog may focus the likely action. It also recommends a visible close control in the tab sequence.

**SYNTHESIS** — `modal appearance ≠ modal behavior ≠ modal semantics`.

A dim backdrop does not prove modality. `aria-modal=true` does not itself implement focus containment or background inertness. A focus trap without dialog semantics is also incomplete.

Dialog state contract:

`invoker → open → background unavailable → initial focus → contained operation → cancel/commit → close → logical focus destination`

**MINTTAP DIRECTION** — For future support/account/destructive flows, define initial and return focus from task semantics, not a universal “first button” rule. Preserve 054's error-prevention/recovery requirements inside the dialog.

**OPEN** — No MintTap production dialog implementation is known or validated.

---

## 4. Additional content on hover/focus has persistence obligations

**SOURCE** — WCAG 2.2 SC 1.4.13 Content on Hover or Focus (AA) requires author-created additional content triggered by hover/focus to be dismissible, hoverable when pointer-triggered, and persistent until trigger removal, dismissal, or invalidation, subject to stated exceptions.

Primary: https://www.w3.org/TR/WCAG22/#content-on-hover-or-focus

**SOURCE / BOUNDARY** — APG's Tooltip pattern is explicitly work in progress and does not yet have task-force consensus. It describes a non-focusable tooltip whose trigger references it via `aria-describedby`; interactive popup content should not be treated as a tooltip.

Guidance: https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/

**SYNTHESIS** — Do not promote APG tooltip draft guidance to a stable universal implementation rule. The normative WCAG behavior obligations are firmer than the unfinished pattern guidance.

**MINTTAP DIRECTION** — Essential help must not depend on hover-only discovery. If popup content contains interactive controls, model it as an appropriate interactive layer rather than a tooltip.

---

## 5. Status/live updates are different from dialogs and focus changes

**SOURCE** — WCAG 2.2 SC 4.1.3 Status Messages (AA) requires qualifying status messages to be programmatically determinable so AT can present them without receiving focus. WAI-ARIA defines live-region semantics for updates likely to occur dynamically.

Primary: https://www.w3.org/TR/WCAG22/#status-messages  
Primary: https://www.w3.org/TR/wai-aria-1.2/

**SYNTHESIS** — Dynamic communication has at least three different mechanisms:

1. **status/live update** — context remains; announce without focus movement where appropriate;
2. **focus movement** — task context/attention genuinely moves;
3. **modal interruption** — user must address a bounded interaction before returning.

Using one mechanism for all three causes overload or lost context. A toast should not automatically become a modal; a modal warning should not be reduced to a transient live-region message.

**MINTTAP DIRECTION** — Classify every async message by task consequence before choosing live region, persistent inline state, focus movement or dialog.

---

## 6. Composite widgets change the keyboard model

**SOURCE** — APG Tabs defines one Tab entry into the tablist, arrow-key movement among tabs, `aria-selected` for the active tab, and tab↔tabpanel relationships. Automatic activation is recommended only when panel display has no noticeable latency; otherwise focus movement can be materially slowed.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

**SOURCE** — APG Toolbar and Grid patterns similarly use a managed internal focus model to reduce flat tab stops. Grid guidance notes that arrow keys used for grid navigation are then unavailable for editing/caret movement until the interaction mode changes appropriately.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/  
Primary: https://www.w3.org/WAI/ARIA/apg/patterns/grid/

**SYNTHESIS** — Composite semantics are an interaction commitment. Applying `role=tablist`, `grid`, `menu`, or `toolbar` because the layout resembles one creates keyboard and state expectations that a flat collection of links/buttons does not satisfy.

**MINTTAP DIRECTION** — Use composite patterns only when their interaction model serves the actual task. Do not “upgrade” simple website navigation or static data tables into application widgets merely to sound more accessible.

---

## 7. Focus and selection are independent state dimensions

**SOURCE** — APG Tabs distinguishes keyboard focus from selected/active tab. APG Combobox can keep DOM focus on the combobox while `aria-activedescendant` identifies the active option in a popup; the selected value is exposed separately with `aria-selected` where applicable.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/  
Primary: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

**SYNTHESIS** — `DOM focus ≠ active descendant ≠ selection ≠ current value`.

This matters in search suggestions, filters, tabs, grids and future app-like web surfaces. A single CSS `.active` class is not an adequate state model when these dimensions differ.

**MINTTAP DIRECTION** — Component specifications must name each independent state and its owner. Visual emphasis must map to the intended state, not collapse focus/selection/current/expanded into one appearance.

---

## 8. Latency changes the accessible interaction strategy

**SOURCE** — APG Tabs recommends automatic activation on focus only when the associated panel appears without noticeable latency; otherwise automatic activation can hamper keyboard navigation efficiency.

Primary: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

**SYNTHESIS** — Performance is not merely Stage 7 polish. Latency can change which accessibility interaction model is appropriate. An interaction that is usable with preloaded local content may become harmful when every arrow movement triggers a slow network fetch.

**DEPENDENCY** — Stage 7 Performance should revisit this as a cross-domain constraint: readiness/latency evidence can determine whether automatic or manual activation is the safer interaction contract.

---

## 9. Responsive recomposition must preserve application state

**SYNTHESIS**, reusing 043/049 and Design Studio W005/W006 — When a wide-layout component becomes a disclosure, sheet/dialog, stacked region or alternate control on narrow screens, responsive transformation must preserve the task state rather than merely redraw it.

State migration questions:
- Does the selected/current item survive recomposition?
- Does hidden content remain incorrectly focusable?
- If a side panel becomes a modal sheet, is modality/focus behavior changed accordingly?
- Does an expanded desktop region map truthfully to the narrow-screen state?
- Are live updates and error/status associations preserved?
- Is the same action still reachable by keyboard/touch without duplicate active controls in two responsive variants?

**MINTTAP DIRECTION** — Add `state migration` to responsive contracts whenever the semantic interaction pattern changes across breakpoints.

---

## 10. Reusable Accessible Application-State Contract

For each dynamic/composite component or task layer, record:

| Field | Required review |
| --- | --- |
| Task role | why this dynamic pattern exists |
| Native baseline | native element/pattern available before custom behavior |
| Visible states | open/closed, selected, current, pending, error, etc. |
| Programmatic states | role/state/property mapping and ownership |
| DOM focus | actual focused element by transition |
| Active descendant | if used, valid referenced item and visual synchronization |
| Selection/value | independent from focus where applicable |
| Keyboard model | entry/exit/internal navigation/activation/cancel |
| Pointer/touch | equivalent task path and cancellation behavior |
| Background | operable, inert, hidden, or unaffected? |
| Announcement | none/status/live/dialog/focus; why |
| Latency | whether async delay changes activation strategy |
| Responsive migration | invariant + state conversion across layouts |
| Recovery | cancel/close/retry/commit and logical next focus |
| Evidence | static semantics → DOM/focus/state assertions → accessibility tree → keyboard/pointer → AT → complete task |

Core invariant:

`visible state == semantic state == interaction state == task truth`

Not literal implementation equality: each representation differs technically, but they must communicate the same authoritative task state.

---

## 11. Representative failure diagnoses

1. **Accordion opens visually; `aria-expanded` stays false** → semantic-state synchronization failure.
2. **Dialog has `aria-modal=true`; Tab reaches page behind it** → modality/operability failure.
3. **Dialog closes and focus falls to document body** → continuation/restoration failure.
4. **Tooltip contains links/buttons** → pattern-role mismatch; interactive popup needs a different interaction model.
5. **Every AJAX update uses assertive live announcements** → announcement overload; mechanism exists but priority is wrong.
6. **Tabs put every tab in sequential Tab order** → composite keyboard-model mismatch.
7. **Auto-activating tabs fetch slow remote content on every arrow key** → latency/accessibility coupling failure.
8. **Combobox highlight moves but `aria-activedescendant` is stale** → active-option synchronization failure.
9. **Mobile layout hides desktop panel with CSS but leaves controls focusable** → responsive semantic/focus failure.
10. **Navigation dropdown given application `menu` semantics without menu keyboard behavior** → semantic overreach.

---

## 12. Design Studio dependency / handoff

Latest canonical Web specialist state checked before this block: `progress/WEB_STATUS.md` (governance sync 2026-09-15), Stage 1 PASS / Stage 2 PRACTICE NOT PASSED. W005 and W006 are conceptual/practice evidence; their browser execution remains a highest-value gap. W013 supplies partial Chromium dialog close→invoker focus-restoration evidence but not a complete accessible modal/AT proof.

**DEPENDENCY — Web Design**
- Execute W005 native/custom runtime with at least disclosure + one true composite (tabs or combobox), asserting keyboard model, computed role/name/state, focus vs selection, and visual/programmatic synchronization.
- Extend W006 integrated runtime with dynamic result status, pending/recoverable state and a modal or transient task layer; assert background inoperability, initial/return focus and state retention.
- Do not infer screen-reader announcement from DOM or accessibility-tree presence; AT evidence remains separate.

**DEPENDENCY — Layout/Interaction**
- Treat modal/transient layers, composite selection and responsive pattern changes as explicit state transitions with ownership and cancellation paths.
- Preserve the distinction `focus != selection != current != expanded != pending`.

**DEPENDENCY — Type**
- Stress dialog headings/descriptions, disclosure labels and dynamic KO/EN status text; wrapping must not hide close/cancel/recovery actions.

**DEPENDENCY — Color**
- Focus, selected/current, expanded, disabled and pending/error states require distinguishable channels; hue alone is insufficient and focus must not be visually conflated with selection.

Web Manager retains task semantics, complete-process scope, state/announcement classification, responsive state migration and evidence boundaries. No Design Studio canonical file is edited.

---

## 13. Verified facts vs synthesis vs open questions

### VERIFIED / SOURCE
- WAI-ARIA 1.2 is a W3C Recommendation; ARIA 1.3 is still under development.
- APG Disclosure exposes expanded/collapsed state with `aria-expanded` and uses button activation behavior.
- APG Modal Dialog specifies contained Tab navigation, Escape close, contextual initial focus and normal focus return to the invoker/logical successor.
- WCAG 2.2 SC 1.4.13 requires dismissible/hoverable/persistent behavior for scoped hover/focus-triggered additional content.
- WCAG 2.2 SC 4.1.3 requires qualifying status messages to be programmatically determinable without receiving focus.
- APG composite patterns define keyboard/state models that differ from flat tabbable controls.
- APG Tabs explicitly conditions automatic activation on sufficiently low display latency.
- APG Tooltip guidance is work in progress and lacks task-force consensus; it is not treated here as settled normative pattern law.

### SYNTHESIS
- Accessible dynamic UI is primarily a cross-representation state-synchronization problem.
- Modal visual treatment, modal semantics and modal behavior are separate obligations.
- Focus, active descendant, selection and current value must be modeled independently where the pattern requires it.
- Latency can determine the appropriate accessible interaction strategy.
- Responsive semantic-pattern changes require explicit state migration, not only CSS rearrangement.

### OPEN / VALIDATION
- Actual MintTap dynamic components, dialogs, disclosures, search suggestions, tabs, filters, live regions and responsive pattern changes are unknown.
- Actual framework/router/component library and use of native `<dialog>`, `inert`, custom focus traps or ARIA libraries are unknown.
- No MintTap browser accessibility-tree, keyboard, screen-reader, switch/speech, touch or disability-informed human validation has been executed.
- Browser/AT interoperability for any future custom composite must be tested on the actual supported matrix.

---

## 14. Checkpoint

**FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

The Web Manager can now distinguish dynamic visual change from accessible application state; diagnose dialog/disclosure/composite synchronization failures; separate focus, selection, active descendant, status announcement and modality; and specify runtime evidence without claiming unperformed AT validation.

Highest-value next block: **056 — Reading, Reflow, Zoom, Motion, Timing & User-Preference Accessibility**. Integrate low-vision/cognitive/vestibular resilience across zoom/reflow/text spacing/orientation/motion/timing and user preferences, reusing Stage 4 typography/color/responsive work instead of repeating visual-design theory.

## Primary references

- W3C WAI, WAI-ARIA Overview — https://www.w3.org/WAI/standards-guidelines/aria/
- W3C, WAI-ARIA 1.2 — https://www.w3.org/TR/wai-aria-1.2/
- W3C WAI, ARIA APG Patterns — https://www.w3.org/WAI/ARIA/apg/patterns/
- W3C WAI, Disclosure Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- W3C WAI, Modal Dialog Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- W3C WAI, Tabs Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
- W3C WAI, Combobox Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
- W3C WAI, Toolbar Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/
- W3C WAI, Grid Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/grid/
- W3C WAI, Tooltip Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
- W3C, WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C WAI, Fly-out Menus — https://www.w3.org/WAI/tutorials/menus/flyout/
