# 052 — Semantic Structure, Native HTML, Accessible Names/Roles/States & ARIA Boundary

Date: 2026-09-15  
Stage: 5 — Accessibility  
Status: **FOUNDATION/PRACTITIONER CHECKPOINT PASS**

## Why this block now

051 established accessibility as a barrier/evidence problem and defined the conformance boundary. The next prerequisite is understanding what browsers and assistive technologies can actually derive from authored markup before studying keyboard/focus and richer widgets. This block therefore connects HTML semantics → accessibility tree/API exposure → accessible name/role/state/property → interaction behavior, and defines when ARIA is legitimate.

This deliberately does **not** repeat Stage 1 HTML/DOM mechanics or Design Studio W005/W011 theory. It establishes the Web Manager's diagnostic and handoff contract for production work.

## Core model

`user/task meaning → native HTML semantics → DOM → user-agent accessibility mapping → accessible object (role/name/state/property) → platform accessibility API → AT presentation/action → task outcome`

A second, equally important chain is:

`ARIA declaration → semantic exposure only → required authored behavior/state synchronization → runtime validation`

ARIA can change or augment what is exposed; it does not automatically supply the intrinsic browser behavior that a native control has.

---

## 1. Native HTML is the semantic baseline

### SOURCE

WAI-ARIA 1.2 is a W3C Recommendation (6 June 2023). It states that ARIA is intended to provide missing semantics, and that when the host language provides a semantic element for an object, authors should use the native feature rather than create the object with style/script plus ARIA. It gives `h1` rather than `div role=heading` as an example.

Source: https://www.w3.org/TR/wai-aria-1.2/

ARIA in HTML, a W3C Recommendation module with subsequent maintained corrections/additions, defines author conformance requirements for ARIA on HTML. It says redundant implicit roles are not recommended and prohibits conflicting ARIA/native semantics in defined cases.

Source: https://www.w3.org/TR/html-aria/

HTML Accessibility API Mappings (HTML-AAM) defines how user agents expose HTML elements/attributes and their default ARIA semantics to platform accessibility APIs.

Source: https://www.w3.org/TR/html-aam-1.0/

### SYNTHESIS

“Native first” is not merely a style preference. A native element is a bundled contract across semantics, browser behavior, keyboard behavior, focusability, state, form behavior and accessibility mapping. Rebuilding only the visual appearance and `role` recreates only part of that contract.

A useful diagnostic distinction is therefore:

`semantic equivalence != behavioral equivalence != accessibility equivalence`

### Failure example

A clickable `div role="button"` may expose a button role but still lack native button keyboard activation, disabled behavior, form participation, focus behavior or state handling unless each relevant behavior is implemented correctly. The semantic label does not manufacture those behaviors.

### MINTTAP DIRECTION

For company/product/support/governance surfaces, choose native HTML by task semantics first. Custom ARIA widgets require an explicit reason and a larger validation burden. Visual styling alone is not a sufficient reason to abandon a native control without checking whether the native element can meet the requirement.

---

## 2. Semantics are an exposed model, not the pixels

### SOURCE

HTML-AAM requires user agents to expose HTML elements/attributes with default semantics through platform accessibility APIs according to the accessibility mapping specifications.

Accessible Name and Description Computation describes the DOM element as the starting point for computing accessible names/descriptions; the resulting accessible objects are exposed through accessibility APIs for assistive technologies.

Stable Recommendation baseline: https://www.w3.org/TR/accname-1.1/  
Current 1.2 work in progress: https://www.w3.org/TR/accname-1.2/

### SYNTHESIS

The rendered visual interface and the programmatic accessibility representation are related but non-identical views of the same product. A control can look correct while exposing the wrong role/name/state; conversely, correct semantic exposure does not prove usable visual, keyboard, touch or cognitive behavior.

Web Manager review must therefore inspect at least:

1. authored semantic intent;
2. browser-exposed accessibility representation where material;
3. actual interaction behavior;
4. task outcome.

DOM inspection alone is not sufficient evidence for the final three.

---

## 3. Role, name, description, state and property are separate obligations

### SOURCE

WAI-ARIA defines roles, states and properties used to communicate UI and structural semantics. Accessible Name and Description Computation defines how user agents compute accessible names and descriptions. AccName 1.2 is currently a Working Draft, not a Recommendation; 1.1 remains the latest Recommendation baseline. The current draft explicitly distinguishes names from descriptions and defines precedence/role-dependent name computation.

Sources:
- https://www.w3.org/TR/wai-aria-1.2/
- https://www.w3.org/TR/accname-1.1/
- https://www.w3.org/TR/accname-1.2/

### SYNTHESIS

Do not collapse “accessible label” into “accessibility.” A control may have:

- correct role but no useful name;
- useful name but wrong role;
- correct role/name but stale state;
- correct role/name/state but broken keyboard behavior;
- correct control semantics but a description that hides prerequisite/error information from the user's task flow.

Review as a tuple:

`role + name + description(if needed) + state/property + behavior + relationship/context`

### Important accessible-name boundary

The accessible name is computed by an algorithm with precedence rules; adding `aria-label` is not a harmless annotation. Depending on element/role and other markup, an author-provided name can become the exposed name instead of visible content. Naming is also prohibited for some roles/elements under ARIA/HTML rules.

### MINTTAP DIRECTION

Prefer visible labels and native host-language labeling mechanisms where they correctly express the task. Use ARIA naming/describing features deliberately when they add required programmatic meaning. Do not use `aria-label` as a routine patch for unclear visible UI.

---

## 4. ARIA is a semantic extension layer, not a behavior polyfill

### SOURCE

ARIA in HTML explains that ARIA can extend native semantics, for example `aria-pressed` can augment a native `button` with a pressed state. It also gives an important counterexample: `aria-disabled="true"` on a hyperlink can expose a disabled state to assistive technology but does not itself make the hyperlink functionally disabled.

Source: https://www.w3.org/TR/html-aria/

The W3C's archived “Using ARIA” guidance states the durable first rule: use native HTML when it supplies the needed semantics and behavior; interactive ARIA controls must also be keyboard usable.

Source: https://www.w3.org/TR/2026/DISC-using-aria-20260224/

### SYNTHESIS

ARIA has two legitimate broad uses:

1. **augment** a native semantic object with information HTML does not directly expose for the use case;
2. **supply missing semantics** for a genuinely custom construct when no suitable native control exists.

It is not a mechanism for making an arbitrary element automatically behave like the declared widget.

### Operational rule

`If native fits → use native.`  
`If native nearly fits → native + narrowly scoped ARIA augmentation.`  
`If native cannot represent the required interaction → custom widget + full semantic/keyboard/focus/state contract + runtime/AT validation.`

The third path carries the highest implementation and regression burden.

---

## 5. Native semantics must not be casually overridden

### SOURCE

ARIA in HTML defines per-element allowed roles/states/properties and explicitly warns against overriding interactive elements with non-interactive roles, redundant roles, side effects and violations of either HTML or ARIA rules. WAI-ARIA also defines host-language conflict behavior.

Sources:
- https://www.w3.org/TR/html-aria/
- https://www.w3.org/TR/wai-aria-1.2/

### SYNTHESIS

Changing `role` is not analogous to changing a CSS class. It can alter the object that assistive technology perceives while intrinsic HTML behavior remains governed by the host element. That can create a split-brain control: browser behavior says one thing, accessibility semantics another.

### Diagnostic question

For every explicit role, ask:

1. What native semantic is being replaced or augmented?
2. Why is the implicit semantic insufficient?
3. Is this role allowed on this HTML element?
4. What keyboard/focus/state behavior does the resulting widget require?
5. Is the visual state synchronized with the programmatic state?
6. What browser/AT evidence proves the intended result?

If question 2 has no concrete answer, the explicit role is probably unnecessary.

---

## 6. Semantic structure matters beyond controls

### SYNTHESIS grounded in HTML/ARIA mapping model

Accessibility semantics include document and relationship structure as well as widgets: headings, landmarks, lists, forms, labels, tables and other meaningful groupings can support navigation and comprehension. Visual grouping alone does not guarantee that these relationships are available programmatically.

This connects Stage 2 IA and Stage 4 visual hierarchy to Stage 5: the intended information hierarchy must survive into authored semantics rather than exist only in typography, spacing or color.

### MINTTAP DIRECTION

For an app-company site, semantic review must cover at least:

- company/global navigation and page identity;
- product feature/evidence sections;
- store/download actions;
- support navigation, search/results and instructions;
- forms and validation relationships;
- privacy/account-control processes;
- tabular or comparative information where used;
- status/error/success information.

This is a scope model, not a claim that MintTap currently has all of these surfaces.

---

## 7. Static conformance checking and runtime evidence answer different questions

### SOURCE

ARIA in HTML defines author conformance rules intended for conformance checkers. HTML-AAM and AccName define user-agent mapping/computation behavior. These are different specification layers.

### SYNTHESIS

A validator can identify forbidden/redundant/invalid ARIA patterns, but valid markup does not prove:

- the computed accessible name is useful;
- the accessibility tree matches author intent in target browsers;
- state changes remain synchronized;
- keyboard/focus behavior is correct;
- screen readers or other AT present the control effectively;
- the complete user task is accessible.

The evidence ladder from 051 remains authoritative:

`static/conformance → browser accessibility representation → keyboard/input/focus runtime → AT/browser/device → complete process → disability-informed human evaluation`

Do not promote a lower layer into a higher-layer claim.

---

## 8. App-company failure patterns

### Pattern A — icon-only store/action control

Failure: visible icon has a click handler; no native interactive element or reliable accessible name.  
Diagnosis: visual affordance exists; semantic/action contract incomplete.  
Preferred direction: native link/button according to task, meaningful name, then icon as presentation.

### Pattern B — clickable product card

Failure: nested/competing interactive regions or a generic container made clickable with role and JS.  
Diagnosis: task destinations and focus/semantic structure were not modeled before visual composition.  
Direction: identify the actual navigation/action targets and use native link/button semantics rather than turning the entire visual box into an ambiguous custom widget by default.

### Pattern C — custom tabs/filter chips

Failure: role names copied from a design-system example but keyboard model, selected state or relationships are absent/stale.  
Diagnosis: ARIA vocabulary was copied without the widget interaction contract.  
Direction: first ask whether simpler native controls/navigation meet the task; if a true composite widget is required, treat it as an interaction implementation requiring Design Studio/runtime/AT evidence.

### Pattern D — disabled destructive/account action

Failure: `aria-disabled=true` communicates disabled state but click behavior still executes.  
Diagnosis: semantic state and operational state diverge.  
Direction: synchronize semantics, behavior and visible state; verify complete process behavior.

### Pattern E — responsive relabeling

Failure: desktop visible text disappears on mobile and an icon remains, but the accessible name becomes absent, generic or inconsistent.  
Diagnosis: responsive visual transformation changed the semantic contract.  
Direction: semantic/name invariants belong in the responsive component contract.

---

## 9. Reusable Semantic Accessibility Contract

For each meaningful structure/control/component, record:

| Field | Question |
| --- | --- |
| task/meaning | What user goal or information relationship does it serve? |
| native candidate | Which HTML element/attribute naturally represents it? |
| implicit semantics | What role/state/property does the native element expose? |
| accessible name | Where should the usable name come from? |
| description | Is supplementary description required, and why? |
| state/property | What dynamic state must be exposed and synchronized? |
| ARIA delta | What meaning is ARIA adding/changing that native HTML lacks? |
| behavior | What pointer/keyboard/default/form behavior must exist? |
| focus | How is focusability/order/return handled? |
| relationships | What labels, ownership, grouping or controlled regions matter? |
| responsive invariant | What semantics/name/state must survive recomposition? |
| static validation | Is the HTML/ARIA usage conforming? |
| browser validation | What computed role/name/state/accessibility-tree evidence is needed? |
| AT/input validation | What target browser/AT/input combinations matter? |
| process validation | Does the complete task remain accessible? |
| open evidence | What is still unproven? |

### Review heuristic

`native candidate → implicit semantics → ARIA delta → required behavior → computed exposure → runtime state → task validation`

Do not begin with “which ARIA role should we add?”

---

## 10. Design Studio dependency / handoff

Latest `progress/WEB_STATUS.md` checked 2026-09-15: Web Design is **Stage 1 PASS / Stage 2 PRACTICE, NOT PASSED**. Its highest-value executable gaps explicitly include W005 native-vs-custom keyboard/focus/semantic behavior and W011 icon accessible-name/target/enlargement/forced-color runtime. This study does not claim those gaps are closed.

### Outgoing handoff

**Web Design**
- For W005/runtime transfer, use this Semantic Accessibility Contract to compare native control vs custom ARIA implementation across computed role/name/state, keyboard activation, focus and state synchronization.
- For W011, preserve accessible-name semantics across icon-only responsive variants.

**Layout / Interaction**
- Treat role/name/state as part of the state machine, not metadata added after interaction design.
- Explicitly connect state transitions, disabled/pending/error/success behavior and focus restoration to semantic state updates.

**Type**
- Visible-label removal/substitution under responsive stress cannot be judged only by geometry; flag cases where truncation or icon substitution changes naming/comprehension.

**Color**
- Programmatic state does not replace visible/non-color state cues; selected/error/disabled/focus require coordinated semantic and perceivable treatment.

Web Manager retains page/process scope, native-vs-custom justification, semantic contract, evidence ladder and release-claim boundary.

---

## 11. Verified facts vs synthesis vs open questions

### VERIFIED / SOURCE

- WAI-ARIA 1.2 is a W3C Recommendation; ARIA 1.3 is still a draft as of this research date.
- ARIA in HTML is a W3C Recommendation module and defines allowed/prohibited ARIA usage on HTML.
- HTML-AAM specifies accessibility-API mappings for HTML semantics.
- AccName defines user-agent computation of accessible names/descriptions; 1.2 is a Working Draft, while 1.1 is the current Recommendation baseline.
- Native HTML is preferred when it provides the needed semantics/behavior; ARIA can augment or supply missing semantics but does not itself implement all widget behavior.
- `aria-disabled` can communicate state without functionally disabling an HTML hyperlink.

### SYNTHESIS

- Treat native controls as bundled semantic/behavioral contracts, not merely default-styled widgets.
- Every explicit ARIA role creates a justification and validation burden.
- Accessibility review should inspect `role + name + description + state/property + behavior + context`, not “has ARIA?”
- Responsive transformations need semantic invariants in addition to visual/layout invariants.
- Production evidence must climb from static validity to computed exposure, runtime interaction, AT/device and complete-task evidence.

### OPEN

- Actual MintTap frontend framework/component library and whether custom controls exist.
- Actual page/process inventory and semantic markup.
- Target browser/OS/AT support matrix.
- Whether third-party widgets introduce inaccessible/custom semantics.
- Actual account deletion/support/search/form implementations.
- Production accessibility-tree and AT behavior.
- Human disability-informed evaluation.

No production accessibility claim is authorized by this study.

---

## 12. Competency check

Checkpoint passes if the Web Manager can:

1. explain how native HTML semantics reach accessibility APIs/AT at a conceptual level;
2. distinguish role, name, description, state/property and behavior;
3. explain why ARIA does not recreate native behavior;
4. justify native vs native+ARIA vs custom-ARIA choices;
5. identify semantic/behavior divergence in realistic app-company components;
6. define evidence needed beyond markup validity;
7. produce a specialist handoff without claiming unexecuted runtime/AT proof.

**Result: PASS at Foundation/Practitioner checkpoint.**

---

## Highest-value next block

**053 — Keyboard, Focus, Input Modality & Operable Interaction Accessibility.**

Reason: once semantics are correct, the next prerequisite is whether users can actually reach, operate, sequence and recover from controls without pointer-only assumptions. Study native keyboard behavior, sequential focus navigation, focus visibility/order/management, modal/transient focus, composite-widget boundary, pointer/target considerations and responsive/input continuity. Reuse Stage 3 and Design Studio runtime evidence rather than re-teaching interaction theory.
