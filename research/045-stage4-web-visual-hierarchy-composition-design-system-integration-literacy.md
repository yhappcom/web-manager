# 045 — Stage 4 Web Visual Hierarchy, Composition & Design-System Integration Literacy

Status: **STAGE 4 FOUNDATION/PRACTITIONER CHECKPOINT — COMPLETE**  
Research date: 2026-09-15  
Scope: Web Manager judgment for `minttap.app` company/app/support/governance surfaces; Apple/Android app-company context.

## Why this block exists

Stages 2–3 already define what a page/task must communicate and how interaction state must behave. Design Studio now owns substantial specialist evidence in Type, Color, Layout/Interaction and Web Design. The highest-value Stage 4 prerequisite is therefore not another visual-design curriculum inside Web Manager. It is the ability to translate product/task/content priority into a **reviewable web-design contract**, diagnose which layer owns a failure, and request the right specialist/browser validation.

Core model:

`task importance → semantic structure → attention order → grouping → typographic hierarchy → color/surface hierarchy → responsive recomposition → component/system consistency → product evidence → browser validation`

---

## RELATED DOMAIN CHECK

### Design Studio Web

Latest `progress/WEB_STATUS.md` checked 2026-09-15: W001–W008 exist; Web Foundation remains NOT YET PASSED pending W009 closure audit. W008 materially closes the prior complete-project integration gap. Web Manager therefore reuses Web's composition, responsive, component, state and performance models rather than duplicating them.

### Type

Latest Type status: Foundation NOT PASSED; evidence extends through T016 downloadable-webfont loading/failure/fallback geometry. Production Korean/complex-script, Firefox/Safari/native shaping and human reading evidence remain open.

### Color

Latest Color status: Stage 1 PASS, narrowly bounded; production/device/human/Web integration remains separate.

### Layout / Interaction

Latest specialist status: Stage 1 PASS; production/browser/device/AT/human completion is not implied.

### Boundary

**Web Manager owns:** task/content priority, truth/evidence, required page states, channel continuity, acceptance criteria, project trade-offs and escalation to specialists.  
**Design Studio owns:** reusable specialist visual/interaction judgment and authored design solutions.  
**Shared validation:** real browser/device/accessibility evidence where visual decisions affect task completion.

---

# 1. SOURCE — visual hierarchy cannot replace document semantics

WCAG 2.2 requires information, structure and relationships conveyed through presentation to be programmatically determinable or available in text (1.3.1), and requires a meaningful reading sequence where sequence affects meaning (1.3.2).

Primary source:
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/

### SYNTHESIS

A large/bold line that merely *looks* like a heading is not equivalent to a semantic heading. Likewise, CSS reordering can produce a visually attractive page whose reading/focus order contradicts the intended task.

### MINTTAP DECISION

Every important page must have two compatible maps:

1. **semantic/task hierarchy** — identity, heading structure, regions, sequence, controls and states;
2. **visual attention hierarchy** — prominence, grouping, spacing, type, surface/color, imagery and motion.

Visual hierarchy may enrich the semantic hierarchy, but must not be the only carrier of meaning.

---

# 2. Hierarchy is task-relative, not a universal size ladder

### SYNTHESIS

“Important” has several meanings that must not be collapsed:
- primary task importance;
- urgency/risk;
- frequency;
- current state relevance;
- marketing emphasis;
- legal/governance necessity.

A privacy link can be legally/operationally critical without being the dominant hero element. A destructive error can deserve temporary high salience even though it is not the page's primary task.

### MINTTAP DECISION — attention contract

Before visual design, specify:
- primary task;
- first orientation fact;
- decision-critical facts required before action;
- primary and secondary actions;
- assurance/governance facts;
- exceptional states that may temporarily outrank normal hierarchy.

Do not specify pixel sizes as a substitute for this contract.

---

# 3. Composition expresses relationships; it must survive recomposition

Design Studio W003's reusable model is retained:

`task → relationship → stress signal → owner → adaptation → invariant → validation`

### SYNTHESIS

Desktop proximity, columns or sidebars are presentations of relationships, not the relationships themselves. Narrow width, text growth, localization or component containment may require a different composition while preserving comparison, sequence, ownership and action context.

### FAILURE EXAMPLES

- support escalation visually detached from the issue it resolves after mobile stacking;
- app name disappears while a store CTA remains, losing product identity;
- comparison attributes become separated from their values;
- sticky action obscures focused/error content under an on-screen keyboard;
- visual reorder contradicts DOM/task order.

### MINTTAP DECISION

Responsive review asks **what relationship must survive?**, not “does the mobile screenshot look clean?”

---

# 4. SOURCE — web typography is a runtime system, not a static mockup

CSS Fonts Level 4 defines ordered font-family fallback and font matching. It also defines downloadable font behavior and notes that fallback metrics can cause reflow; authors are advised to choose metric-compatible fallback where appropriate.

Primary source checked 2026-09-15:
- W3C CSS Fonts Module Level 4: https://www.w3.org/TR/css-fonts-4/

### VERIFIED FACT

Actual rendered fonts can differ by glyph availability, loading/failure state and platform-installed fallback. A design-tool screenshot does not establish production typography.

### SYNTHESIS

Web Manager should review typography by **role and resilience**, not by prescribing a universal type scale:
- heading/body/label/value/action roles remain distinguishable;
- long Korean/English strings wrap without losing ownership;
- numeric/data comparison remains legible where relevant;
- fallback/loading does not destroy hierarchy or geometry;
- enlarged text/reflow preserves information and actions.

### DEPENDENCY — Type

Exact font choice, metrics, mixed-script pairing and fallback calibration remain Type-owned. Production project work should supply exact shipped fonts/content to Type/Web for transfer validation.

---

# 5. SOURCE — color must support meaning, not become its only carrier

WCAG 2.2 1.4.1 prohibits color as the only visual means of conveying information/action/state. WCAG 1.4.3 defines minimum text contrast requirements and 1.4.11 covers non-text contrast for relevant UI/graphical information.

Primary source:
- https://www.w3.org/TR/WCAG22/

### SYNTHESIS

Brand color, semantic state color, action emphasis and decoration are different jobs. A visually coherent palette can still fail if success/error/selection/focus is understandable only through hue or if secondary text is made faint merely to appear spacious.

### MINTTAP DECISION

Web Manager specifies **semantic color obligations**, not final palette values:
- what information/state must remain distinguishable;
- which elements require text/non-text contrast evaluation;
- what must remain understandable without hue;
- where brand emphasis must not overpower task/error hierarchy.

### DEPENDENCY — Color

Final palette/ramp/theme/surface decisions and perceptual/device validation remain Color/Web Design work.

---

# 6. Components are contracts, not visual stamps

Design Studio W005 separates semantic role, native primitive, state machine, content contract, adaptation and visual treatment.

### SYNTHESIS

Two boxes that look alike are not necessarily the same component; two components with visual variants can still share one semantic/state contract.

### MINTTAP DECISION

Reuse is justified when the following remain materially shared:
- semantic role;
- task promise;
- content schema;
- state dimensions;
- interaction/accessibility behavior;
- adaptation rules.

Local variation is justified when task/content differs. “Consistency” must not force a support result, app-discovery card and destructive account-control panel into one generic card merely because all are rectangular.

### FAILURE MODE

**System drift:** the same role behaves differently across pages without a task reason.  
**False consistency:** different roles are forced into one visual/component abstraction and lose necessary distinctions.

---

# 7. SOURCE — product imagery must remain truthful

Apple's current App Review Guidelines 2.3.3 say screenshots should show the app in use rather than merely title art/login/splash screens. Apple's asset guidance says screenshots should show what people can expect and focus on the core user experience. Google Play current publishing guidance says store listing information, screenshots and images should accurately reflect app functionality; misleading discrepancies can cause rejection.

Primary sources checked 2026-09-15:
- Apple App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple App Store Asset Best Practices: https://developer.apple.com/app-store/asset-best-practices/
- Google Play Console Help — Helpful tips to get your app published: https://support.google.com/googleplay/android-developer/answer/15191715
- Google Play Console Help — Store listing best practices: https://support.google.com/googleplay/android-developer/answer/13393723

### SYNTHESIS

The website is not identical to a store listing, but the same product-truth problem applies. A polished mockup can imply functionality, state or availability that the shipped app does not have.

### MINTTAP DECISION — evidence rule

For website screenshots/demos, record:
- source app/build/version/date;
- platform/device context when material;
- whether imagery is actual capture, composited capture or conceptual illustration;
- claim(s) the image is intended to support;
- localization status;
- retirement trigger when the UI/function changes.

Do not present conceptual/future UI as current shipped behavior without explicit qualification.

---

# 8. Visual polish cannot repair contract failure

### SYNTHESIS

The review order matters. Fixing visual symptoms before structural causes can create attractive failure.

Preferred diagnostic order:

1. product/content truth;
2. task/page contract;
3. semantic structure and state;
4. relationship/composition;
5. typography/color/imagery hierarchy;
6. component/system coherence;
7. browser/device/accessibility validation;
8. aesthetic refinement.

Examples:
- a beautiful CTA pointing to the wrong store is a destination-contract failure;
- an elegant empty state shown during retrieval failure is a state-truth failure;
- low-contrast metadata cannot be defended as “secondary hierarchy” when users need it for the decision;
- a responsive layout that hides required comparison data is not improved by cleaner spacing.

---

# 9. Reusable Visual/Web Design Review Contract

For each significant MintTap page/surface, provide Design Studio with:

1. **Page/task identity** — user, entry context, primary outcome.
2. **Semantic hierarchy** — H1/regions/sequence/control roles/state ownership.
3. **Attention hierarchy** — first orientation, decision-critical facts, actions, assurance, exceptional states.
4. **Relationship invariants** — what must stay grouped/comparable/associated across widths.
5. **Typography stress** — KO/EN, long strings, numerals/data, fallback/loading, enlargement.
6. **Color obligations** — semantic states, contrast-sensitive elements, non-color channels.
7. **Imagery evidence** — source/version/claim/localization/truth status.
8. **Component contract** — role/content/state/adaptation; allowed variants.
9. **Responsive contract** — stress trigger, owner, adaptation and invariant.
10. **Runtime validation** — target browsers/devices/inputs, zoom/reflow, keyboard/focus, font loading, forced colors where relevant.
11. **Open evidence** — what cannot yet be claimed from static review.

This contract intentionally does not dictate a universal MintTap visual style.

---

# 10. Validation boundary

### VERIFIED

Standards and current platform guidance establish structural, accessibility, font-runtime and store-asset constraints described above.

### NOT VERIFIED BY THIS STUDY

- that any particular MintTap palette/typeface/layout is optimal;
- actual target-browser rendering for a future MintTap site;
- production font loading/fallback behavior;
- WCAG conformance;
- screen-reader behavior;
- physical-device color appearance;
- human comprehension, preference or conversion effect;
- current shipped-app screenshots/assets, because actual project inventory was not supplied here.

These require project-specific artifacts and testing.

---

# 11. Design Studio handoffs

### Web Design

Incoming: Page + Task/Journey + Interaction + Form + Retrieval + Responsive contracts plus this Visual/Web Design Review Contract.  
Ask Web Design to author/critique complete page directions and return browser evidence for hierarchy, responsive recomposition, component/state consistency, native semantics and runtime performance.

Latest canonical Web status has advanced to W001–W008 with W009 closure audit next; do not describe it as W001–W005.

### Type

Provide exact project fonts, Korean/English strings, numeric/data cases and loading/fallback conditions. Ask for hierarchy/wrap/metric transfer evidence rather than generic font recommendations.

### Color

Provide exact semantic states, surfaces and brand constraints. Ask for palette/state/contrast evaluation in actual page context, not isolated swatches.

### Layout / Interaction

Provide relationship invariants and complete task/state paths. Ask for challenge of grouping, density, focus, layered ownership, interruption and responsive state transfer.

No Design Studio canonical file is edited by Web Manager.

---

# 12. OPEN / CHANGE WATCH

- **OPEN:** actual MintTap app inventory, brand system, launch page priorities, shipped screenshots, supported locales and target browser/device matrix.
- **OPEN:** Web Design W009 closure verdict; latest status says Foundation not yet passed pending audit.
- **OPEN:** Type Foundation closure and production mixed-script/browser transfer.
- **VALIDATION:** exact future MintTap designs must be tested with real content and runtime assets.
- **CHANGE WATCH:** Apple App Review/asset guidance and Google Play metadata/store-listing policies are changeable platform requirements; recheck before release.

---

# Competency checkpoint

**PASS at Stage 4 Foundation/Practitioner checkpoint for this block.**

The Web Manager can now distinguish task/semantic hierarchy from visual attention, review composition as relationship preservation, treat typography/color/imagery as runtime/truth systems, diagnose component consistency versus false consistency, and hand project-specific design obligations to the correct Design Studio specialist without pretending to replace specialist authorship.

## Highest-value next block

**046 — Web Typography, Reading, Localization & Content Presentation Literacy.**

Focus on real web reading systems—headings/body/support/policy/data text, line wrapping, mixed Korean/English, font loading/fallback, zoom/reflow and content presentation—while reusing Type evidence rather than repeating type-design construction research.