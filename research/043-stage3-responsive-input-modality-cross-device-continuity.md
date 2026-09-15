# 043 — Stage 3 Responsive Web Interaction, Input Modality & Cross-Device Continuity

Status: **FOUNDATION/PRACTITIONER CHECKPOINT — PASS**  
Research date: 2026-09-15  
Scope: responsive interaction behavior for `minttap.app` company/app/support/governance surfaces across desktop, tablet and mobile web contexts.

## Why this block exists

039–042 established contracts for action/state/recovery, task journeys, forms/transactions and retrieval. Design Studio W003 separately established a useful responsive ownership model. The unresolved Web Manager question is operational:

> When viewport geometry, browser chrome, zoom, on-screen keyboard and available input mechanisms change, which interaction/task invariants must survive and which adaptations are justified?

This study does not repeat W003's composition research. It validates platform/input facts independently and converts them into a cross-device interaction contract for MintTap.

---

## RELATED DOMAIN CHECK

### Web Manager evidence reused
- 036 navigation/wayfinding and focus-sensitive responsive navigation requirements;
- 037 page contracts and localized/reflow stress;
- 039 Interaction Contract;
- 040 Task/Journey Contract;
- 041 Form/Transaction Contract;
- 042 Retrieval Contract.

### Design Studio evidence checked
Latest `yhappcom/design-studio/progress/WEB_STATUS.md` checked 2026-09-15:
- Web W001–W003 are PRACTICE/CRITIQUE; Foundation NOT PASSED;
- W003 models responsive work as `task → relationship → stress signal → owner → adaptation → invariant → validation`;
- W003 measured Playwright results remain OPEN because its environment could not execute the harness;
- W003 explicitly leaves hover-independent essential actions, actual browser zoom, Firefox/Safari/physical iOS/Android and navigation disclosure transfer open.

### Boundary
Web Manager owns task/state/input requirements and production validation criteria. Design Studio owns reusable composition/interaction expertise and should test these contracts in real page designs and browsers.

---

# 1. SOURCE — viewport width is not an input-device detector

CSS Media Queries Level 5 defines interaction media features:
- `pointer`: accuracy of the **primary pointing device** (`none`, `coarse`, `fine`);
- `hover`: whether the primary pointing device can conveniently hover;
- `any-pointer` / `any-hover`: capabilities across available pointing devices.

The specification explicitly states that these features do **not** detect non-pointing input mechanisms such as keyboards. It also warns that devices can have multiple pointing devices and that the user agent may change which device is considered primary.

Primary source checked 2026-09-15:
- W3C — Media Queries Level 5, §7 Interaction Media Features: https://www.w3.org/TR/mediaqueries-5/#mf-interaction

### SYNTHESIS

Do not infer:
- narrow viewport = touch-only;
- wide viewport = mouse/keyboard;
- `pointer:fine` = no touch;
- `hover:hover` = essential actions may be hover-only;
- `any-pointer:fine` = small targets are safe for everyone.

A touch-enabled laptop, tablet with trackpad/keyboard, desktop browser at narrow window width, or phone with external keyboard breaks device-class assumptions.

### MINTTAP DECISION

Responsive layout triggers and input-capability adaptations are separate decisions. Width/container queries may control composition. Pointer/hover queries may provide enhancements, but core task completion must not depend on an inferred device class.

---

# 2. SOURCE — concurrent input mechanisms are normal, not an edge case

WCAG 2.2 Guideline 2.5 covers input modalities, including 2.5.6 Concurrent Input Mechanisms. Current W3C guidance treats pointer/touch/motor accessibility as a range of possible mechanisms rather than a mutually exclusive desktop/mobile split.

Primary/current source checked 2026-09-15:
- W3C WAI — Understanding Guideline 2.5 Input Modalities: https://www.w3.org/WAI/WCAG22/Understanding/input-modalities.html

### SYNTHESIS

A responsive mode must tolerate **input switching while the page remains open**. A user may tap, then attach/use a keyboard or trackpad, or use keyboard navigation on a touch device.

### Failure example

A narrow-layout filter drawer that is visually usable by touch but traps or loses keyboard focus is not a valid mobile adaptation. Conversely, a desktop disclosure whose essential controls appear only on hover is fragile on a hybrid device.

---

# 3. SOURCE — hover is an enhancement channel, not an essential-information channel

Media Queries Level 5 says layouts should not depend on hover to remain fully usable when `hover:none` applies and warns that secondary devices can differ. WCAG also has requirements for content that appears on hover/focus.

### SYNTHESIS

Hover can add preview, emphasis or convenience. It must not be the only way to reveal:
- required action labels;
- destructive-action consequences;
- support escalation;
- validation instructions;
- critical product facts;
- navigation needed to complete the task.

### MINTTAP DECISION

Any essential hover-triggered information/action requires a keyboard/focus and non-hover route. Touch users must not need to discover a hidden hover state by accident.

---

# 4. SOURCE — pointer target size and gesture complexity are accessibility constraints

WCAG 2.2 establishes:
- 2.5.1 Pointer Gestures: multipoint/path-based functionality needs a single-pointer non-path alternative unless essential;
- 2.5.7 Dragging Movements: author-provided drag functionality needs a single-pointer non-drag alternative unless essential;
- 2.5.8 Target Size (Minimum): pointer targets are at least 24×24 CSS px or satisfy listed spacing/equivalent/inline/user-agent/essential exceptions.

Primary sources checked 2026-09-15:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Understanding Pointer Gestures: https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html
- Understanding Dragging Movements: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
- Understanding Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

### SYNTHESIS

`pointer:fine` does not justify shrinking critical controls below an accessibility/task-safe baseline. Media queries describe capabilities; they do not override accessibility requirements or user motor variability.

### MINTTAP DIRECTION

For ordinary company/support/forms/retrieval surfaces, prefer simple activation over gesture-dependent custom controls. If drag is introduced later, define a non-drag task-equivalent operation before considering it complete.

---

# 5. SOURCE — layout viewport and visual viewport are distinct

CSSOM View defines viewport concepts; the VisualViewport interface exposes the currently visible portion of the page. Pinch zoom and on-screen keyboards can reduce the visual viewport while leaving the layout viewport unchanged.

Current explanatory/spec-linked source checked 2026-09-15:
- MDN VisualViewport / CSSOM View: https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport
- CSSOM View specification is linked from that reference.

### SYNTHESIS

A page can satisfy its CSS layout breakpoint while the user's **actually visible working area** is materially smaller. Fixed/sticky controls, focused form fields, error messages and bottom action bars can therefore become obscured even when no layout breakpoint changes.

### MINTTAP DECISION

Do not define responsive correctness only by `window width` screenshots. Form and transaction validation must include focused-input + on-screen-keyboard conditions and pinch/browser zoom where relevant.

---

# 6. SOURCE — dynamic browser UI makes viewport height non-constant

Modern CSS defines small, large and dynamic viewport variants (`sv*`, `lv*`, `dv*`) because browser interfaces can expand/retract. Dynamic viewport units can track the changing viewport but may cause resizing while browser UI changes.

Current spec-linked reference checked 2026-09-15:
- MDN CSS length / viewport units: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#relative_length_units_based_on_viewport

### SYNTHESIS

`100vh` is not a universal synonym for “the unobscured screen.” Full-height heroes, modal-like sheets, sticky footers and form layouts need deliberate viewport behavior rather than copied viewport-unit recipes.

### OPEN / VALIDATION

Exact behavior varies by browser/platform and evolves. Production use requires target-browser tests, especially Safari/iOS and Chromium/Android.

---

# 7. SOURCE — VirtualKeyboard API is not a universal baseline

The VirtualKeyboard API can expose keyboard geometry and opt into overlay behavior, but current compatibility references mark it as limited/experimental rather than universally available.

Current reference checked 2026-09-15:
- MDN VirtualKeyboard API: https://developer.mozilla.org/en-US/docs/Web/API/VirtualKeyboard_API

### SYNTHESIS

Do not make core MintTap form usability depend on this API. Browser-native scrolling/focus behavior and robust flow layout remain the baseline. VirtualKeyboard/VisualViewport handling can be progressive enhancement when a concrete sticky-action or app-like surface justifies it.

---

# 8. SOURCE — orientation must not be arbitrarily locked

WCAG 2.2 SC 1.3.4 requires content not to restrict operation to a single display orientation unless a specific orientation is essential. W3C lists orientation locking or telling users to rotate as common failures when no essential exception applies.

Primary/current source checked 2026-09-15:
- W3C WAI — Understanding 1.3.4 Orientation: https://www.w3.org/WAI/WCAG22/Understanding/orientation.html

### MINTTAP DECISION

Company/app/support/privacy/account-control pages have no known essential orientation requirement. They should function in portrait and landscape. Do not use “rotate your device” as a repair for weak responsive composition.

---

# 9. SOURCE — zoom, text enlargement and reflow are related but distinct stressors

WCAG 2.2 separately addresses Resize Text (1.4.4) and Reflow (1.4.10). Browser/pinch zoom can also alter the visual viewport differently from author-controlled text enlargement.

Primary source:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

### SYNTHESIS

Do not treat one 200% CSS font-size simulation as proof of browser zoom behavior. It is useful text-growth evidence but not equivalent to:
- browser UI zoom;
- pinch zoom;
- OS text settings;
- localized expansion;
- narrow viewport reflow.

### DESIGN STUDIO HANDOFF

This directly bounds W002/W003 evidence. Their controlled text-size stress is valuable, but actual browser zoom remains a separate required validation.

---

# 10. SOURCE — responsive visual reordering must not silently corrupt keyboard/task order

The HTML Standard defines sequential focus navigation independently of visual CSS layout. A focusable area omitted from sequential focus navigation is unreachable by that mechanism.

Primary source checked 2026-09-15:
- WHATWG HTML — Interaction / Sequential focus navigation: https://html.spec.whatwg.org/multipage/interaction.html#sequential-focus-navigation

### SYNTHESIS

CSS Grid/Flex reordering, portals/disclosures or responsive DOM changes can make visual order diverge from sequential focus/task order. Screenshot review cannot prove interaction continuity.

### MINTTAP DECISION

When responsive recomposition changes presentation order, preserve a coherent source/reading/focus/task sequence. If a genuinely different interaction sequence is required, it must be explicitly designed and tested rather than produced accidentally by CSS.

---

# 11. Contract preservation across 039–042

Responsive adaptation is valid only if the underlying task contract survives.

## 039 Interaction Contract invariants
- action meaning does not change merely because viewport/input changes;
- pending/confirmed/failed/outcome-unknown remain distinguishable;
- focus/recovery routes remain operable;
- destructive consequence is not hidden in a compact mode.

## 040 Task/Journey Contract invariants
- necessary steps do not appear/disappear solely for cosmetic compactness;
- previously known context is preserved;
- interruption/resume remains reconstructable;
- protective friction does not become accidental friction on mobile.

## 041 Form/Transaction Contract invariants
- labels/instructions/errors remain associated and discoverable;
- focused fields and correction controls remain visible with on-screen keyboard;
- entered valid data survives recomposition/orientation where technically feasible;
- submit/pending/result state is not lost when layout mode changes.

## 042 Retrieval Contract invariants
- query/scope/filter/sort state remains inspectable;
- compact filter disclosure does not silently change filter semantics;
- result identity remains sufficient to choose;
- list→detail→Back continuity survives responsive mode;
- loading/empty/error/partial/stale states remain distinguishable.

---

# 12. Cross-device continuity is primarily state continuity, not pixel continuity

### SYNTHESIS

Desktop and mobile do not need identical layouts. They need continuity of:
- identity and app context;
- user goal;
- authoritative data/state;
- commitment status;
- saved draft where promised;
- URL/shareable safe retrieval state where designed;
- recovery/escalation path.

### OPEN

True desktop↔mobile continuation across separate devices depends on product architecture: account/session model, server-side persistence, privacy/security, draft storage and authentication. No MintTap implementation facts are currently verified, so this study does not assume cross-device synchronized drafts.

### MINTTAP DECISION

Use “cross-device continuity” as a requirement category, not a promise. For anonymous/public pages continuity can come from stable URLs. For user-specific transactions, require verified backend/session capability before promising resume on another device.

---

# 13. Responsive/Input Continuity Contract

For every material interactive surface specify:

1. **task invariant** — what user outcome must survive;
2. **state invariant** — what data/commitment/retrieval state must survive;
3. **layout trigger** — viewport/container/content stress that justifies recomposition;
4. **input assumptions** — ideally none beyond standards; identify any capability enhancement;
5. **hover dependency** — none for essential operation;
6. **pointer/gesture contract** — target size, alternatives to complex gestures/drag;
7. **keyboard/focus contract** — source/sequential order, disclosure entry/exit, restoration;
8. **visual-viewport contract** — focused controls, keyboard occlusion, sticky/fixed surfaces;
9. **orientation contract** — behavior in portrait/landscape;
10. **zoom/reflow contract** — browser zoom, text enlargement, localized growth, narrow width;
11. **responsive-state migration** — what happens if mode changes while a task is in progress;
12. **URL/history continuity** — where applicable;
13. **cross-device continuity** — none/local URL/server-backed, explicitly bounded;
14. **fallback/progressive enhancement** — behavior without optional APIs;
15. **validation matrix** — browser, OS/device, viewport, input, keyboard, zoom, language and human-task checks.

---

# 14. Minimum validation matrix for future MintTap production work

This is a validation framework, not a claim that all cells have been tested.

### Geometry/content
- wide desktop;
- medium/tablet-like allocation;
- narrow phone-like allocation;
- portrait + landscape;
- long Korean and English labels/content;
- browser zoom/reflow and text enlargement as distinct tests.

### Input
- keyboard-only;
- mouse/trackpad;
- touch;
- mixed/hybrid where target hardware supports it.

### Dynamic viewport
- on-screen keyboard with focused form fields;
- browser chrome expanded/retracted where relevant;
- pinch zoom where relevant to task.

### Continuity
- resize/orientation while form has data;
- disclosure mode change while focus is inside;
- retrieval list→detail→Back;
- pending/error state while geometry changes.

### Accessibility
- visible and unobscured focus;
- no keyboard trap;
- coherent source/focus/task order;
- non-hover route to essential content;
- pointer target/gesture alternatives;
- status/error exposure.

---

# 15. Failure taxonomy

Diagnose responsive interaction failures as:

1. **device-class inference failure** — width treated as input identity;
2. **capability overreach** — media feature treated as exclusive guarantee;
3. **hover dependency failure**;
4. **target/gesture failure**;
5. **focus/order failure**;
6. **visual-viewport occlusion failure**;
7. **orientation failure**;
8. **zoom/reflow conflation failure**;
9. **state migration failure** — layout mode changes and task data/state disappears;
10. **contract-semantic drift** — compact mode changes meaning or available outcome;
11. **progressive-enhancement failure** — optional API becomes mandatory;
12. **cross-device promise failure** — UI promises resume/sync without verified persistence.

---

# VERIFIED FACTS vs SYNTHESIS vs OPEN

## VERIFIED FACTS
- CSS interaction media features describe primary/all pointing-device capabilities and do not detect keyboards.
- WCAG 2.2 covers orientation, keyboard operation, pointer gestures, concurrent input, dragging and minimum pointer target sizing.
- layout and visual viewports can differ; zoom and on-screen keyboard can change the visible viewport.
- modern CSS provides small/large/dynamic viewport unit families.
- VirtualKeyboard API is not universally supported.
- sequential focus navigation is a document/browser interaction concept independent of mere visual placement.

## SYNTHESIS / MINTTAP JUDGMENT
- viewport width and input capability must be separate design dimensions;
- essential tasks must remain hover-independent;
- responsive correctness is contract preservation, not screenshot similarity;
- cross-device continuity should be specified as state continuity and bounded by actual persistence architecture;
- optional viewport/keyboard APIs should be progressive enhancement unless target-browser evidence justifies stronger dependence.

## OPEN
- actual MintTap target browser/device matrix;
- whether any future MintTap web product requires app-like sticky input/action surfaces;
- whether authenticated drafts or user state will exist and support cross-device resume;
- physical iOS Safari / Android Chrome / tablet/hybrid behavior;
- screen-reader and human usability evidence;
- W003 executable measured results.

---

# DESIGN STUDIO DEPENDENCIES / HANDOFFS

## To Web Design
Use this **Responsive/Input Continuity Contract** together with W003's adaptation-ownership model. Validate complete MintTap page/task surfaces rather than isolated responsive components. Required challenge cases: hybrid input, hover-independent essential actions, actual browser zoom, on-screen keyboard occlusion, portrait/landscape, long KO/EN content, disclosure focus continuity and in-progress state migration.

## To Layout / Interaction
Challenge responsive mode transitions while interaction is pending, invalid, filtered, partially complete or focused inside a disclosure. Verify that visual recomposition does not alter action semantics, recovery, focus or state ownership.

## To Type
Future browser zoom/OS text/localization tests should use actual delivered preferred/fallback fonts; simulated font-size growth is not equivalent to full font/runtime/zoom transfer.

## To Color
Every responsive/input state, including focus, error, disabled, pending and forced-colors modes, must preserve semantic distinctions; color work should not be validated only in wide desktop mode.

No Design Studio canonical file was edited.

---

# CHANGE WATCH

Recheck before production:
- Media Queries interaction feature specification/support;
- viewport and virtual-keyboard behavior across Safari/Chrome/Firefox;
- VirtualKeyboard API compatibility;
- WCAG/current accessibility requirements and applicable legal adoption;
- target device/browser support matrix.

---

# COMPETENCY CHECK

Checkpoint passes at Foundation/Practitioner level because the Web Manager can now:
- explain why responsive geometry and input capability are independent;
- distinguish primary/all pointer and hover capabilities without treating them as keyboard/device detectors;
- specify hover-independent, keyboard/touch/pointer-compatible task behavior;
- reason about layout vs visual viewport, dynamic browser UI and on-screen keyboard risk;
- separate browser zoom, pinch zoom, text enlargement, localization and narrow reflow as different stresses;
- preserve 039–042 contracts across recomposition;
- define cross-device continuity without inventing backend persistence;
- hand Design Studio a testable interaction/state contract rather than prescribing arbitrary breakpoints.

This is not production PASS. Real browser/device, assistive-technology and human-task validation remain required.

## Highest-value next block

Proceed to **Stage 3 Integration Gate — complete-task usability and interaction competency**. Integrate 039–043 across representative MintTap public tasks (app evaluation→store action, support→resolution/escalation, privacy/account control, form transaction, retrieval/list-detail) and determine whether Stage 3 can close at Foundation/Practitioner level before moving to Stage 4 Web Design Literacy.