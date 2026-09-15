# 056 — Reading, Reflow, Zoom, Motion, Timing & User-Preference Accessibility

Date: 2026-09-16  
Stage: 5 — Accessibility  
Level: Foundation / Practitioner integrated checkpoint

## Why this block now

051–055 established barrier/conformance scope, semantics, operability, transactions and dynamic application state. The next unresolved prerequisite is **adaptation resilience**: can the same task survive when a user enlarges text/content, changes spacing, uses a narrow effective viewport, fixes device orientation, suppresses motion, or needs more time?

This block deliberately reuses Stage 4 typography/responsive/color work and Design Studio responsive evidence. The new value is not another responsive-design tutorial; it is the accessibility contract that distinguishes authored appearance from user-controlled presentation and time.

Core model:

`user need/preference → user-agent/platform transformation → effective presentation/state → layout/content adaptation → task invariant → failure/recovery → validation`

---

## 1. Accessibility resilience is not “mobile responsiveness”

**SOURCE** — WCAG 2.2 SC 1.4.4 Resize Text (AA) requires text, except captions and images of text, to resize up to 200% without loss of content or functionality. W3C explains that scaling is primarily a user-agent responsibility while authors must not prevent effective scaling and must ensure the content survives it.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/resize-text

**SOURCE** — WCAG 2.2 SC 1.4.10 Reflow (AA) requires content to be presentable without loss of information/functionality and without two-dimensional scrolling at an equivalent width of 320 CSS px for vertically scrolling content, with exceptions for content whose usage or meaning requires two-dimensional layout. W3C notes that 320 CSS px corresponds to a 1280 CSS-pixel starting viewport at 400% zoom.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/reflow

**SYNTHESIS** — A site can be excellent at common phone breakpoints and still fail low-vision adaptation. Conversely, reflow conformance is not proof that the resulting reading/task experience is good. The accessibility question is not “does the mobile layout exist?” but “does user-driven enlargement preserve information, functionality, relationships and task continuation?”

**MINTTAP DIRECTION** — Test zoom/reflow as a transformation of real page/process contracts, not as a screenshot width checklist. Preserve primary task, labels, values, status, recovery controls and evidence/claim context when the effective viewport collapses.

---

## 2. Resize Text and Reflow are related but not interchangeable

**SOURCE** — Resize Text is explicitly 200% text enlargement. Reflow addresses one-dimensional reading/operation at 320 CSS px equivalent width (or 256 CSS px height for horizontally scrolling content). WCAG permits bounded two-dimensional regions where a 2-D layout is essential, including examples such as data tables, maps and diagrams.

Primary: https://www.w3.org/WAI/WCAG22/quickref/#reflow  
Primary: https://www.w3.org/WAI/WCAG22/Understanding/resize-text

**SYNTHESIS** — Four independent failure classes follow:

1. **scale prevention** — the user cannot effectively enlarge;
2. **content loss** — clipping/truncation/overlap hides text or controls;
3. **relationship loss** — labels, values, headings or actions become ambiguous after recomposition;
4. **task loss** — the user can read the content but cannot complete the action.

A fifth class is **unbounded 2-D navigation**: the whole page requires horizontal plus vertical traversal even though only one intrinsic artifact, such as a comparison table, genuinely needs local horizontal movement.

**MINTTAP DIRECTION** — Localize legitimate two-dimensional scrolling to the intrinsic artifact. Do not use the Reflow exception as permission for the entire page shell to overflow horizontally.

**DEPENDENCY — Design Studio Web/Layout** — W003 already established adaptation ownership and explicitly treats semantic data tables as intrinsic 2-D artifacts. Reuse that model: page shell owns page reflow; component owns local recomposition; intrinsic artifact owns only the bounded overflow it actually needs.

---

## 3. Responsive breakpoint changes do not waive enlargement obligations

**SOURCE** — W3C's current Resize Text Understanding document explicitly addresses responsive sites: each automatically presented variation remains in scope. Zoom may activate another breakpoint, but it must still be possible to achieve the required enlargement relative to the default presentation.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/resize-text

**SYNTHESIS** — A common false pass is: “At 200% zoom the site switched to mobile, therefore it passes.” The relevant question is whether the resulting text is actually enlarged and whether content/functionality survives. A breakpoint that compensates for zoom by shrinking authored text can defeat the user's intent.

**MINTTAP DIRECTION** — For future production validation, record actual browser zoom/text-resize behavior and resulting rendered geometry. Do not infer browser-UI zoom from viewport emulation alone.

**VALIDATION** — Design Studio currently lists actual browser-UI zoom as OPEN. Chromium viewport/responsive transfer evidence must not be promoted to zoom evidence.

---

## 4. Text Spacing is a resilience requirement, not a house typography recipe

**SOURCE** — WCAG 2.2 SC 1.4.12 Text Spacing (AA) requires no loss of content/functionality when users override line height, paragraph spacing, letter spacing and word spacing to specified metrics. W3C explicitly states that authors are **not required to use those values by default** or provide a built-in spacing control. The criterion also contains a language/script exception for properties not used by a writing system.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing

**SYNTHESIS** — This confirms the Stage 4 rule: WCAG spacing metrics are not a universal typographic design prescription. They are a stress condition. A visually refined default can still fail if fixed heights, clipping, absolute positioning or narrow control geometry cannot tolerate user overrides.

**MINTTAP DIRECTION** — Stress real KO/EN strings, including mixed Korean/Latin app names, tickers, URLs, policy text and long support labels. Test for clipping, overlap, hidden actions and broken label/value association. Language-sensitive typography remains a Type handoff; Web Manager owns whether task/content survives the override.

---

## 5. Orientation is user control over physical use, not a layout preference

**SOURCE** — WCAG 2.2 SC 1.3.4 Orientation (AA) says content must not restrict view and operation to a single display orientation unless that orientation is essential. W3C specifically cites users whose devices are mounted in a fixed orientation and distinguishes author-imposed restrictions from user/device orientation locks.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/orientation

**SYNTHESIS** — “Landscape looks better” is not an essential exception. The relevant test is whether the information/function fundamentally requires a particular orientation and cannot be achieved conformingly another way.

**MINTTAP DIRECTION** — The company/support/product website should assume both orientations unless a future feature has a demonstrably essential reason. Responsive recomposition may differ by available geometry; view/operation must not be blocked merely because the device is in the “wrong” orientation.

**OPEN** — No MintTap production orientation-lock behavior is known.

---

## 6. Motion has multiple accessibility regimes

**SOURCE** — WCAG 2.2 SC 2.2.2 Pause, Stop, Hide (A) covers moving/blinking/scrolling information that starts automatically, lasts more than five seconds and is presented alongside other content, and auto-updating information presented alongside other content. Users need a mechanism to pause, stop or hide/control update frequency unless essential.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide

**SOURCE** — SC 2.3.3 Animation from Interactions is **AAA**, not AA. It requires interaction-triggered motion animation to be disableable unless essential. W3C identifies `prefers-reduced-motion` as one sufficient technique, but WCAG techniques are not the only conforming implementation path.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions  
Technique: https://www.w3.org/WAI/WCAG22/Techniques/css/C39

**SOURCE** — SC 2.3.1 Three Flashes or Below Threshold is Level A. Motion/distraction and flash/seizure risk therefore must not be collapsed into one “reduce motion” check.

Normative quick reference: https://www.w3.org/WAI/WCAG22/quickref/#seizures-and-physical-reactions

**SYNTHESIS** — Distinguish at least:
- auto-starting motion/update → pause/stop/hide/frequency obligations;
- interaction-triggered non-essential motion → AAA disableability and strong inclusive-design value;
- flashing → separate seizure threshold obligation;
- essential movement → may remain, but “essential” is a high bar tied to functionality/information, not branding preference.

**MINTTAP DIRECTION** — Default to restraint for decorative parallax, large spatial transitions and auto-advancing product media. Respect an available reduced-motion preference for non-essential motion. Do not claim AA requires SC 2.3.3; treat reduced-motion support as a strong product-quality direction and AAA-related evidence unless another applicable requirement establishes more.

---

## 7. `prefers-reduced-motion` is a signal, not a complete motion policy

**SOURCE** — W3C documents `prefers-reduced-motion` as a sufficient technique for preventing interaction-triggered motion animation under SC 2.3.3.

Primary: https://www.w3.org/WAI/WCAG22/Techniques/css/C39

**SYNTHESIS** — A media query can communicate a user preference to CSS, but it does not decide which motion is essential, whether JS-driven animation also stops, whether an auto-updating carousel needs pause controls, or whether a flashing effect violates SC 2.3.1. Those are author/task decisions.

**MINTTAP DIRECTION** — Future motion inventory should classify each effect by trigger, purpose, spatial intensity, duration/repetition, essentiality, preference response and fallback. Reduced-motion behavior should preserve state change and task feedback even when spatial animation is removed.

**DEPENDENCY — Design Studio Layout/Interaction/Web** — Motion variants must preserve the same task/state transition. Removing animation must not remove confirmation, loading state, expanded/collapsed state or route change evidence.

---

## 8. Timing is part of task accessibility

**SOURCE** — WCAG 2.2 SC 2.2.1 Timing Adjustable (A) requires content-set time limits to be turned off, adjusted over a wide range, or extendable with warning and a simple action, subject to defined real-time/essential/>20-hour exceptions. W3C states that server-controlled time limits under the organization's control are included.

Primary: https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable

**SOURCE** — W3C notes that users with low vision, blindness, dexterity impairments, cognitive/language limitations and other needs may require more time. It also explains that a disappearing toast may not create a time limit if the same information remains discoverable elsewhere.

**SYNTHESIS** — `temporary presentation ≠ time-limited task` and `security timeout ≠ automatic accessibility exception`.

A timeout contract needs:

`what expires → who controls it → why it exists → warning → extension/alternative → retained state/data → re-auth/recovery → exact continuation point`

**MINTTAP DIRECTION** — Avoid time pressure where it is not intrinsic. For future account/support/auth flows, classify session expiry, OTP validity, temporary status/toast messages, auto-refresh and any reservation-like deadline separately. Security rationale does not by itself remove WCAG timing responsibility.

**DEPENDENCY — Stage 8 Security/Privacy** — Security/session controls and accessibility timing can conflict. Stage 8 must revisit this block and optimize both threat reduction and task preservation rather than allowing either discipline to silently override the other.

---

## 9. User preference support is broader than one CSS media query

**SOURCE** — WCAG's adaptability/resilience model permits users and user agents to alter presentation. Text spacing explicitly anticipates user styles/extensions; resize relies substantially on user-agent mechanisms; reduced motion can use OS/browser preference signaling.

**SYNTHESIS** — The durable principle is **author presentation must tolerate legitimate user override**. This applies across text size/spacing, effective viewport, orientation, motion and timing. Stage 4 forced-colors/color-scheme evidence belongs to the same architectural family but is not repeated here.

Preference pipeline:

`user setting/need → platform or browser signal/action → author response → semantic/task invariant → runtime evidence`

**MINTTAP DIRECTION** — Never treat author defaults as the only valid rendering. Component contracts should state what may change and what must remain invariant under user-driven presentation changes.

---

## 10. Failure taxonomy

### A. Breakpoint false pass
Mobile layout appears at zoom, but authored text shrinks enough that the user never receives the required enlargement.

### B. Fixed-height clipping
Larger or spaced text is cut off inside buttons/cards/banners/dialogs.

### C. Whole-page overflow
One wide artifact causes the entire page to require two-dimensional navigation instead of containing overflow locally.

### D. Responsive semantic loss
A narrow/zoomed variant removes a label, status, warning or evidence qualifier required to understand the task.

### E. Hidden duplicate interaction
Desktop and narrow variants coexist in the DOM and the visually hidden copy remains focusable/operable.

### F. Motion-only state communication
A slide/bounce/spatial transition is the only cue that state changed; reduced motion removes the meaning.

### G. Decorative essentiality claim
Brand animation is labeled “essential” merely because stakeholders prefer it.

### H. Pause-that-captures-the-user
Motion pauses only while focus/hover remains on the moving region, forcing the user to keep focus there and preventing normal page use; W3C explicitly says this is not a sufficient pause mechanism for SC 2.2.2.

### I. Security-timeout shortcut
A timeout is assumed exempt because it is “for security,” without evaluating whether it is content-controlled, adjustable, recoverable or genuinely essential.

### J. Expiring-only feedback
Critical success/error information disappears with no durable alternative path.

---

## 11. Reusable Adaptation / User-Preference Accessibility Contract

For each page, component or complete process, record:

| Field | Required question |
| --- | --- |
| Task invariant | What must remain understandable and operable under adaptation? |
| Text enlargement | Can text reach 200% without content/function loss? |
| Reflow | At 320 CSS-px equivalent width, what recomposes and what bounded artifact legitimately retains 2-D scrolling? |
| Zoom mechanism | Is evidence actual browser zoom/text resize, or only viewport emulation? |
| Text-spacing stress | What happens under WCAG spacing overrides, including KO/EN mixed text? |
| Orientation | Does either portrait or landscape become blocked? Is any restriction genuinely essential? |
| Motion inventory | What moves, who triggers it, why, how long/repeated, and is it essential? |
| Reduced-motion behavior | What changes when motion is suppressed, and is state/task feedback preserved? |
| Auto-update | Can moving/auto-updating information be paused/stopped/hidden or frequency-controlled where required? |
| Flash risk | Is flashing evaluated separately from general motion? |
| Time limits | What expires, who sets it, and what off/adjust/extend/exception path applies? |
| Recovery | Is user state/data preserved after timeout, re-authentication or adaptation? |
| User preference | Which browser/platform/user overrides are supported and what invariant survives? |
| Evidence | static → browser zoom/reflow → preference emulation/real setting → keyboard/AT/device → complete task → human evidence |

---

## 12. Validation ladder

1. **Static inspection** — fixed heights, overflow clipping, viewport restrictions, motion/timer inventory.
2. **Browser text resize/zoom** — actual user-agent mechanisms; verify 200% text enlargement and intermediate states.
3. **Reflow** — evaluate 320 CSS-px equivalent width and local 2-D exceptions.
4. **Text-spacing override** — apply all SC 1.4.12 metrics simultaneously and inspect content/function loss.
5. **Orientation** — portrait/landscape where relevant on actual or credible device/browser environment.
6. **Motion preference** — reduced-motion preference plus explicit controls for applicable auto motion/update.
7. **Timing** — warning, extension, expiry, retained state and recovery path.
8. **Input/AT regression** — ensure recomposition does not break focus order, semantics, announcements or hidden-variant behavior.
9. **Complete-task validation** — execute actual support/account/product task through transformed states.
10. **Human evidence** — low-vision/cognitive/vestibular and other disability-informed evaluation where production risk warrants it.

**VALIDATION BOUNDARY** — Passing scripted viewport/DOM assertions does not establish actual browser zoom, screen magnifier behavior, vestibular comfort, cognitive readability or disability-informed usability.

---

## 13. Design Studio dependencies / handoffs

Latest specialist state checked 2026-09-16: Web Design Stage 1 PASS / Stage 2 PRACTICE, with actual browser-UI zoom, broader browser/device/AT and human evidence explicitly OPEN.

### Web Design
- Add actual browser-UI zoom/reflow/text-spacing execution when environment permits; do not substitute viewport emulation for zoom.
- Extend W006-style integrated state execution with timeout/recovery and durable status where a real project requires timing.
- Inventory auto-motion/update and reduced-motion variants in any future product-media specimen.

### Layout / Interaction
- Reuse relationship/adaptation ownership from W003: page, component and intrinsic artifact must own different transformations.
- Define motion removal as an alternate transition presentation, not removal of the state transition itself.
- Preserve focus/state when layout recomposes.

### Type
- Stress actual KO/EN/mixed-script content under 200% enlargement and SC 1.4.12 spacing overrides.
- Diagnose clipping/wrapping/reading failures without treating WCAG spacing metrics as default typography prescriptions.

### Color
- Reuse existing forced-colors/user-environment evidence; no duplicate color study here.
- Ensure reduced-motion alternatives do not fall back to color-only state communication.

Web Manager owns page/process scope, normative requirement classification, timing/motion essentiality claim boundaries, task invariants and production evidence thresholds. No Design Studio canonical file was edited.

---

## 14. MintTap unknowns / OPEN

No production evidence currently establishes:
- actual `minttap.app` zoom/reflow/text-spacing behavior;
- viewport meta configuration or zoom restrictions;
- actual production typography/container sizing;
- page/component overflow behavior;
- orientation restrictions;
- animation, carousel, parallax, auto-update or flashing inventory;
- reduced-motion handling;
- session/auth/OTP/time-limit behavior;
- supported browser/OS/device/screen-magnifier matrix;
- disability-informed reading/motion/timing evaluation.

Do not infer these from generic app-company patterns or Design Studio exercises.

---

## 15. Competency checkpoint

**PASS — Foundation/Practitioner checkpoint.**

The Web Manager can now:
- distinguish resize-text, reflow and text-spacing obligations;
- explain why responsive/mobile behavior is not sufficient zoom evidence;
- preserve intrinsic 2-D artifacts without allowing whole-page overflow;
- separate normative motion/flash/timing requirements by trigger and conformance level;
- treat `prefers-reduced-motion` as one mechanism rather than a complete motion policy;
- distinguish temporary feedback from a time-limited task;
- connect security timeouts to accessibility recovery rather than assuming exemption;
- define a reusable adaptation/user-preference contract and validation ladder;
- identify which evidence remains runtime, device, AT or human OPEN.

## Highest-value next block

057 — **Media Accessibility, Captions, Transcripts, Audio Description & Product-Demo Communication**.

Reason: MintTap is an app company whose website may use app previews, tutorials, support media or product demonstrations. Stage 4 established product media as evidence; Stage 5 must now establish how time-based media communicates equivalent information across hearing/vision needs, while avoiding unnecessary repetition of static-image accessibility already covered in 048. After that, perform a Stage 5 integration/conformance competency review before advancing to Search/Discovery unless a prerequisite gap emerges.
