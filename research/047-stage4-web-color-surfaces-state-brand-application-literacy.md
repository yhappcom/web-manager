# 047 — Web Color, Surfaces, State & Brand Application Literacy

Date: 2026-09-15  
Stage: 4 — Web Design Literacy  
Level: Foundation / Practitioner checkpoint

## Purpose

Develop Web Manager judgment for applying and reviewing color on real `minttap.app` pages without duplicating the Design Studio Color Specialist's color-science curriculum. The concern here is the browser/page system: brand expression, foreground/background relationships, interaction/state meaning, user color preferences, forced-color behavior, imagery interaction, and validation.

Core model:

`content/task role → semantic color role → foreground/surface pair → interaction/state cue → user/UA color environment → rendered result → accessibility + browser + human validation`

---

## 1. SOURCE — what the platform and standards actually establish

### 1.1 CSS color is richer than hex/sRGB

The current W3C CSS Color Module Level 4 defines CSS `<color>` forms including `rgb()`, HSL/HWB, Lab/LCH, Oklab/Oklch and `color()` predefined spaces. CSS colors are no longer restricted to sRGB, and interpolation results depend on the interpolation color space.

Source: W3C CSS Color Module Level 4, current Candidate Recommendation Draft, 2026-08-25: https://www.w3.org/TR/css-color-4/

**Boundary:** availability of a color syntax or wide-gamut space does not establish that a MintTap brand palette should use it, nor that all target browsers/displays will render a visually identical result.

### 1.2 Color cannot be the only visual carrier of information

WCAG 2.2 SC 1.4.1 requires that color not be the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element. W3C explicitly notes that red-versus-green validity still needs another indicator when accurate color identification is required.

Source: W3C Understanding SC 1.4.1: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html

This affects errors, success/warning states, selected states, links, charts and status indicators.

### 1.3 Text contrast and non-text contrast are different obligations

WCAG distinguishes text contrast from non-text contrast. Non-text Contrast covers visual information required to identify UI components/states and graphical objects, with its own applicability and exceptions. Contrast math alone does not establish hierarchy quality, brand fitness, or human comfort.

Sources:
- W3C Understanding SC 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C Understanding SC 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

### 1.4 Light/dark scheme support is negotiation, not a palette generator

CSS Color Adjustment Level 1 defines `color-scheme` and interaction with user preferences. `light` and `dark` describe supported scheme classes, not exact palettes. User-agent controlled UI such as form controls and scrollbars can follow the used scheme. The specification warns that pairing UA/system colors with unrelated author colors cannot guarantee contrast; foreground/background pairs may need to be specified together.

Source: W3C CSS Color Adjustment Module Level 1: https://www.w3.org/TR/css-color-adjust-1/

### 1.5 Forced colors can replace author color decisions at used-value/paint time

Forced-colors mode allows a user agent to enforce a user-selected palette. CSS Color Adjustment specifies affected color properties and additional changes: for example `box-shadow` and `text-shadow` compute to `none`, and non-URL background images can be removed. System colors expose the user's palette. `forced-color-adjust: none` opts an element out, but the specification says authors should use it only when they themselves support the user's color/contrast needs.

Source: W3C CSS Color Adjustment Module Level 1: https://www.w3.org/TR/css-color-adjust-1/

**Operational consequence:** a control boundary, selection, focus cue, or hierarchy that exists only as a shadow/background tint can disappear under forced colors.

### 1.6 User contrast preference and forced colors are not the same thing

Media Queries exposes preference/environment signals such as `prefers-contrast`; forced colors is a distinct condition where the UA enforces a palette. These must not be collapsed into one generic "high contrast mode" mental model.

Current compatibility is a deployment question and must be checked against MintTap's supported browser matrix rather than inferred from the standard alone.

---

## 2. SYNTHESIS — the page-level color system

A production page should not start with swatches. It should start with semantic obligations.

Useful role layers:

1. **content roles** — primary text, secondary text, muted/supporting content, links;
2. **surface roles** — canvas, elevated/grouped surface, inset/secondary surface, overlays;
3. **action roles** — primary, secondary, destructive or consequential action where justified;
4. **state roles** — success, warning, error, information, selected/current, disabled, pending;
5. **boundary/focus roles** — borders, separators, control boundaries, focus indication;
6. **brand/decorative roles** — identity and atmosphere that do not carry sole operational meaning;
7. **data roles** — series/categories/positive-negative semantics only when a real data task requires them.

A token name such as `mint-500` describes a value family; a semantic token such as `action-primary-background` describes a job. Web Manager should reason primarily in jobs and leave exact color authorship to Color/Web specialists.

---

## 3. Brand application: identity is not semantic overload

### 3.1 Brand color is not automatically the primary-action color

A brand hue may fail against text, conflict with semantic states, become too salient when repeated, or disappear/change in user-controlled environments. Therefore:

`brand identity role != action role != success role != selection role`

They may share a value only after the actual pair/state/context is validated.

### 3.2 MintTap brand evidence is currently incomplete

The repository does not establish a current production brand system, approved palette, dark scheme, shipped web assets, or exact production background/text pairs.

**OPEN:** do not infer a final `minttap.app` palette from prior conversational brand-color references or Design Studio exercises. A real project must establish current approved brand evidence first.

### 3.3 Brand survival should be structural as well as chromatic

If forced colors removes brand fills, a MintTap page should remain identifiable and operable through name/logo semantics, typography/content, layout and native interaction structure. Brand color can enrich identity; it should not be the only carrier of product identity or task meaning.

---

## 4. Surfaces and hierarchy

Surface hierarchy is not equivalent to "more shades". A surface distinction is justified when it clarifies grouping, containment, layering or interaction context.

Failure modes:
- low-contrast cards that are visible on one display but merge on another;
- every section receiving a tinted card, destroying figure/ground hierarchy;
- separators used decoratively without a relationship role;
- text color weakened to manufacture hierarchy until readability becomes fragile;
- shadow-only boundaries that vanish in forced colors;
- brand-tinted surfaces competing with screenshots/product evidence.

**SYNTHESIS:** first establish hierarchy through content structure, spacing and typography; color/surface should reinforce that hierarchy rather than manufacture it alone. This aligns with Design Studio Color C015's grayscale-first evidence without treating that exercise as production MintTap validation.

---

## 5. State and interaction color

A state is a system fact, not a hue.

For each meaningful state ask:

`what changed? → how is it expressed semantically/programmatically? → what non-color visual cue exists? → what color reinforces it? → what survives forced/user colors?`

Examples:
- invalid field: message + association/state + visible non-color cue; red may reinforce;
- selected filter: selected semantics + shape/boundary/text/check cue; tint may reinforce;
- current navigation item: current-page semantics + non-color differentiation; color may reinforce;
- success: explicit outcome text/iconography where appropriate; green alone is insufficient;
- disabled: actual disabled/non-operable semantics and appropriate affordance; low opacity alone is not the state definition.

Focus is similarly not "the blue ring". The focus indicator must remain perceptible under the actual state/surface environment; later Accessibility stage will perform the formal WCAG-focused audit.

---

## 6. Links and action differentiation

A text link must be discoverable in its surrounding reading context. Color can be part of differentiation, but relying on hue alone is fragile. Inline links, navigation links and button-like actions are different content/interaction roles and should not be forced into one visual treatment merely for consistency.

**MINTTAP DIRECTION:** support, privacy and policy pages should prioritize reliable link recognition and visited/navigation utility over decorative minimalism.

---

## 7. Light, dark and user-controlled color environments

### 7.1 Dark mode is a separate composition/state system, not inversion

A legitimate dark scheme must reconsider foreground/surface relationships, image edges/transparency, control states, focus, disabled content, screenshots, logos and UA controls. `color-scheme` communicates supported schemes to the UA; it does not author the page palette.

**OPEN:** MintTap has no verified requirement for a site-level dark scheme yet. Do not add one solely because the OS exposes a preference.

### 7.2 Forced colors is an operability test

Minimum forced-colors review:
- essential controls remain identifiable;
- links/actions remain distinguishable;
- focus remains visible;
- selected/current/error states remain understandable;
- information is not lost when author fills/shadows disappear;
- SVG/icon behavior is checked rather than assumed;
- opt-outs are exceptional and justified.

### 7.3 Contrast preference is progressive adaptation

Where supported and useful, `prefers-contrast` may inform adaptations, but core MintTap readability/operability cannot depend on it. User preference features are enhancement signals, not substitutes for a robust default design.

---

## 8. Imagery, screenshots and color

App screenshots are evidence-bearing content, not merely color blocks. Their visual salience can dominate a page and distort the intended hierarchy.

Review:
- screenshot background versus page surface separation;
- whether a device frame or boundary is actually needed;
- transparent image behavior in light/dark contexts;
- text embedded inside screenshots versus surrounding HTML text;
- whether decorative gradients/tints reduce product legibility;
- whether screenshots are being recolored in a way that misrepresents the shipped product.

**SYNTHESIS:** web brand color should frame product evidence, not repaint it into false consistency.

---

## 9. Wide gamut and modern CSS color: capability is not requirement

CSS Color 4 enables wide-gamut and perceptual color spaces. That is useful implementation capability, but adoption adds validation obligations:
- fallback for target browsers;
- gamut mapping and out-of-gamut behavior;
- display/browser differences;
- screenshot/export asset color management;
- token/toolchain compatibility.

**MINTTAP DIRECTION:** default to the simplest color representation that satisfies the approved visual system and target-platform evidence. Escalate to Display-P3/OKLCH or other spaces when they solve a demonstrated authoring/rendering problem, not because they are newer.

Design Studio Color owns deeper gamut/colorimetry judgment.

---

## 10. Validation ladder

A computed contrast ratio is useful but narrow evidence.

Recommended ladder:

1. semantic-role review;
2. foreground/background pair calculation where applicable;
3. non-color state/meaning review;
4. actual component/page rendering;
5. light/dark scheme where supported;
6. forced-colors/user override stress;
7. keyboard/focus/state interaction;
8. representative Chrome/Safari/Firefox and mobile browsers according to project matrix;
9. real device/environment checks when material;
10. human recognition/readability/usability validation for claims that require it.

Do not convert automated contrast PASS into "color design PASS".

---

## 11. Reusable Web Color / Surface / State Contract

For each real MintTap surface record:

- page/task identity;
- approved brand evidence and version;
- semantic content roles;
- surface/grouping roles;
- action roles;
- state roles and non-color cues;
- focus/boundary obligations;
- text foreground/background pairs;
- non-text component/graphic pairs where applicable;
- link differentiation;
- imagery/screenshot interaction;
- supported light/dark schemes;
- forced-colors behavior;
- contrast-preference behavior if used;
- wide-gamut/fallback policy if used;
- browser/device matrix;
- automated checks;
- human-validation questions;
- OPEN claims that must not be made yet.

This contract is the Web Manager handoff; it is not a final palette specification.

---

## 12. Design Studio dependency / handoff

Latest canonical Color specialist status checked 2026-09-15: **Stage 1 PASS; Stage 2 entry audit next (C016)**. Its PASS is explicitly bounded: it does not claim production Color, physical-device validation, human-observer research, Web integration or the full specialist curriculum. Relevant existing bridge evidence includes C001 user overrides, C002 semantic tokens, C006 transfer, C010 gamut work, C011 forced-colors resilience and C015 perceptual-context capstone.

### Outgoing to Color Specialist

Provide the actual MintTap Web Color / Surface / State Contract, exact content/surface pairs, real screenshots/assets, supported theme/browser matrix and semantic state requirements. Ask Color to author/critique viable color solutions and margins; do not ask for an abstract palette detached from tasks and surfaces.

### Outgoing to Web Design

Provide complete page states including forced-colors/theme stress, image/screenshot conditions, hover/focus/selected/error variants and responsive surfaces. Web Design owns composition/browser integration.

### Outgoing to Layout/Interaction

Escalate any case where a color/surface distinction is compensating for weak grouping, hierarchy, state coupling or interaction affordance. Geometry and state semantics remain L/I concerns.

### Outgoing to Type

Escalate text-color decisions whose viability depends on exact font weight/size/rendering/fallback. Contrast math does not substitute for exact typography evidence.

No Design Studio canonical file is edited by Web Manager.

---

## 13. Verified facts vs synthesis vs open questions

### SOURCE / VERIFIED
- CSS Color 4 supports multiple modern color spaces and color interpolation depends on interpolation space.
- WCAG prohibits color as the sole visual carrier for specified informational/action distinctions.
- WCAG text and non-text contrast are separate criteria with defined scopes.
- `color-scheme` communicates supported schemes and affects UA-provided UI; light/dark are not exact palettes.
- forced-colors can replace author colors and remove effects such as shadows; system colors expose the enforced palette.
- `forced-color-adjust: none` is an exceptional opt-out, not a general brand-preservation mechanism.

### SYNTHESIS
- semantic roles should precede palette values;
- brand, action and semantic-state roles should not be conflated by default;
- hierarchy should survive grayscale/author-color loss because structure, typography and spacing carry part of the load;
- forced-colors is a strong stress test for whether color is carrying hidden interaction meaning;
- product screenshots should remain evidence-bearing and should not be recolored into false brand consistency.

### OPEN
- current approved MintTap web brand palette and token system;
- whether `minttap.app` needs a dark scheme;
- exact target browser/device matrix;
- production screenshot/logo color profiles and export pipeline;
- whether wide-gamut CSS/assets provide material value;
- real Windows forced-colors, Safari/Firefox, mobile and physical-display behavior for the future implementation;
- human recognition/readability/preferences in the actual MintTap audience.

---

## 14. Competency checkpoint

Web Manager should now be able to:
- distinguish brand color from semantic/state roles;
- specify color obligations before exact values;
- diagnose color-only meaning and shadow/fill-only state failures;
- explain `color-scheme` versus `prefers-color-scheme` versus forced colors without conflation;
- recognize when contrast calculation is necessary but insufficient;
- keep screenshots/product evidence truthful while integrating brand surfaces;
- decide when modern/wide-gamut CSS color is justified versus gratuitous;
- produce a testable handoff to Color/Web/Type/Layout specialists.

**047 FOUNDATION/PRACTITIONER CHECKPOINT: PASS.**

Next highest-value Stage 4 block: **048 — Web Imagery, Iconography, App Screenshots & Product Demonstration Literacy**, integrating truthful product evidence, responsive media, image semantics, non-text signals and store↔web visual continuity without duplicating specialist iconography or later performance work.