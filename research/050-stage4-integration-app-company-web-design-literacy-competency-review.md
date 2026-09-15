# 050 — Stage 4 Integration: App-Company Web Design Literacy Competency Review

Date: 2026-09-15  
Stage: 4 — Web Design Literacy  
Gate target: FOUNDATION / PRACTITIONER INTEGRATION

## Purpose

045–049 established separate professional contracts for hierarchy/composition, typography/reading, color/surface/state, product media/non-text content, and component/page-system governance. This block tests whether those domains can be reasoned about together on representative app-company page families without collapsing into aesthetic preference or pretending that standards review proves production usability.

This is a competency integration review, not a MintTap redesign. Actual `minttap.app` inventory, shipped assets, production components, approved brand rules and user evidence remain unverified.

## Integrated model

`user task → page semantic structure → attention hierarchy → reading system → state/color obligations → product evidence → component/page contracts → responsive transformation → cross-channel truth → runtime/human validation`

A page is not design-literate merely because each layer looks acceptable in isolation. The layers must preserve the same task and truth.

---

## 1. Verified source anchors

### SOURCE — accessibility is structural and cross-layer

WCAG 2.2 is a W3C Recommendation. Its requirements span perceivable, operable, understandable and robust behavior. Relevant Stage 4 implications include programmatically determinable information/relationships, meaningful sequence, reflow, text/non-text contrast and non-color communication. Passing one visual check therefore does not establish page-level accessibility or usability.

Primary source:
- https://www.w3.org/TR/WCAG22/

### SOURCE — Apple requires accurate, current product representation

Apple App Review Guidelines 2.3 state that app metadata, including descriptions, screenshots and previews, must accurately reflect the app's core experience and remain up to date. Guideline 2.3.3 says screenshots should show the app in use rather than merely title art, login or splash screens. Apple also states that marketing an app misleadingly, including outside the App Store, can be grounds for enforcement.

Primary source checked 2026-09-15:
- https://developer.apple.com/app-store/review/guidelines/

### SOURCE — Google Play likewise requires truthful metadata/product imagery

Google Play's deceptive-behaviour guidance requires metadata, including store listing, screenshots and title, to precisely reflect app functionality. Its store-listing guidance recommends screenshots of actual in-app experiences and localized assets where screenshot text is used.

Primary sources checked 2026-09-15:
- https://support.google.com/googleplay/android-developer/answer/17006354
- https://support.google.com/googleplay/android-developer/answer/13393723

**SYNTHESIS:** for an app-company website, visual design and product truth cannot be governed independently. A beautiful page that exaggerates or ages out of the shipped app is a product-evidence failure.

---

## 2. Representative page-family integration

The following are diagnostic families, not claims that these exact MintTap pages currently exist.

### A. Company / home surface

Primary question: `Who is this company, what products exist, and where should I go next?`

Integrated obligations:
- semantic structure exposes company identity and product choices;
- attention hierarchy favors real user routes over decorative branding;
- typography distinguishes company proposition, product identity and supporting copy;
- brand color may establish identity but cannot obscure link/action/state semantics;
- product imagery must be attributable to real shipped/current products;
- repeated product presentations share a stable component contract without forcing all products into identical expression;
- narrow layouts preserve product comparison and route clarity rather than merely stacking every block.

Failure example: visually dominant hero imagery pushes product identity and store route below the fold while decorative mint surfaces make every card equally salient. This is not primarily a color problem; it is hierarchy + page-task + component-role failure.

### B. App / product detail surface

Primary question: `Is this app relevant to me, what does it actually do, and where can I get or learn about it?`

Integrated obligations:
- claim hierarchy maps to user evaluation tasks;
- screenshots/demos are evidence for the claims they accompany;
- screenshot crop/art direction cannot remove the UI evidence needed to support the claim;
- captions and surrounding HTML carry explanatory meaning instead of baking all text into images;
- platform/store actions remain distinguishable and truthful;
- KO/EN text growth does not detach a feature claim from its evidence;
- component variants preserve semantic roles across different apps/platforms.

Failure example: a responsive mobile crop looks cleaner but removes the control that demonstrates the advertised feature. The visual adaptation passes aesthetics and fails evidence integrity.

### C. Support / help surface

Primary question: `Can I solve a problem quickly and know what to do if I cannot?`

Integrated obligations:
- reading/navigation hierarchy outranks promotional expression;
- heading semantics and visible hierarchy agree;
- long Korean/English instructions survive wrapping, text spacing and reflow;
- warning/error/status meaning does not rely on hue alone;
- screenshots used as procedural aids have a text-equivalent path and remain version-current;
- support result/article components preserve retrieval and Back/resume context from Stage 3;
- responsive changes do not hide prerequisites, escalation paths or recovery.

Failure example: a support screenshot contains the only instruction for where to tap. This is both a non-text/accessibility problem and a lifecycle problem when the app UI changes.

### D. Governance / privacy / account-control surface

Primary question: `What happens to my data/account, and how can I exercise the available control?`

Integrated obligations:
- semantic and reading structure outrank visual compactness;
- destructive/irreversible actions are not visually conflated with ordinary navigation;
- prerequisites, consequences and recovery are adjacent to the relevant action;
- color is supplementary to warning/state semantics;
- components preserve form/transaction contracts from Stage 3;
- narrow layouts, zoom and virtual-keyboard conditions do not obscure consequences or final actions;
- visual branding cannot make legal/operational content less legible.

Failure example: an account-deletion action is styled as the same low-emphasis text link as policy navigation. Visual consistency exists, semantic consistency fails.

---

## 3. Cross-layer diagnostic method

When a design problem is observed, diagnose in this order:

1. **Task:** what is the visitor trying to establish or do?
2. **Truth:** what product/company fact must remain accurate?
3. **Structure:** what semantic order and relationships carry that task?
4. **Attention:** does visual priority follow task priority?
5. **Reading:** do language, font fallback, wrapping and density preserve comprehension?
6. **State:** are action/current/error/selected/focus meanings distinguishable without color alone?
7. **Evidence:** do screenshots/icons/media support rather than distort the claim?
8. **System:** is the component/variant legitimate or drift?
9. **Responsive:** what changes, what state migrates, what invariant must survive?
10. **Validation:** what can be asserted from standards/static review, and what still needs browser/device/AT/human evidence?

This prevents superficial prescriptions such as “increase contrast,” “make the CTA bigger,” or “use the same card everywhere” before the failure class is known.

---

## 4. Integration stress cases

### Long localized heading

A Korean or English heading grows to three lines.

Wrong response: shrink font until it fits.

Correct diagnostic path: determine semantic importance, available measure, line-breaking policy, relationship to adjacent CTA/media, responsive recomposition options and hierarchy survival. Type and Layout/Web specialists validate exact geometry.

### Brand accent used for status

A mint brand color is reused for success and selected state.

Wrong response: approve because the palette is consistent.

Correct diagnostic path: separate brand role from semantic state, check non-color cues, contrast and forced-color resilience, then decide whether value reuse is semantically safe.

### Shared product card

Two apps need different amounts of product evidence.

Wrong response: force identical card height/content to preserve consistency.

Correct diagnostic path: preserve shared semantic role and interaction contract while allowing a named evidence-density variant if the task difference is real.

### Store/web mismatch

Website hero shows a feature UI from an older app build while the current store listing and shipped app have materially changed.

Classification: evidence drift. Redesign is not the first remedy; update/retire the evidence and its claim linkage.

---

## 5. What Stage 4 competency now supports

At Foundation/Practitioner level the Web Manager can now:

- distinguish semantic hierarchy from visual attention and diagnose contradictions;
- treat typography as a runtime reading system rather than static font styling;
- separate semantic color obligations from exact palette values;
- govern screenshots/demos/icons as purpose-bound non-text/product evidence;
- distinguish resource selection from art direction and preserve evidence under crop/recomposition;
- define components by semantic/state/interaction contracts rather than silhouette;
- distinguish legitimate variants from system drift;
- reason about tokens as decision/value infrastructure without treating them as proof of quality;
- integrate Stage 3 task/state/responsive contracts with Stage 4 visual systems;
- identify which findings belong to Web Manager versus Type, Color, Layout/Interaction or Web Design specialists;
- preserve explicit OPEN/VALIDATION boundaries when browser/device/AT/human evidence is absent.

## 6. What Stage 4 competency does NOT prove

It does not prove:
- a production MintTap visual system is correct;
- WCAG conformance;
- measured usability or comprehension;
- actual Korean/English reading quality;
- browser/device parity;
- screen-reader/AT behavior;
- physical-display color quality;
- icon recognition;
- screenshot comprehension or conversion performance;
- production design-token/component implementation quality.

Those require project artifacts and/or later-stage validation.

---

## 7. Design Studio dependency / handoff

Latest specialist status checked 2026-09-15:

- **Web Design:** Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED. W012/W013 provide Chromium responsive and partial navigation/history runtime transfer. True HTTP direct-entry/reload, integrated task-state execution, icon runtime, performance/readiness, broader browser/device/AT and human evidence remain OPEN.
- **Type:** Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED. T021 has actual raster evidence and an identified lowercase drawing defect. Browser/product typography remains a later transfer.
- **Color:** Stage 1 PASS; Stage 2 entry audit next. Existing quantitative/browser exercises do not establish production web/device/human color validation.
- **Layout/Interaction:** Stage 1 PASS with substantial runtime/state evidence; exact current specialist evidence should be re-read before a live handoff.

### Outgoing integrated handoff

For real MintTap work, send Design Studio a single evidence package rather than disconnected style requests:

- page family + primary user task;
- semantic/content hierarchy;
- real KO/EN stress content;
- product claims + Product Evidence Ledger entries;
- component role/state/variant matrix;
- semantic color obligations;
- typography/reading constraints;
- responsive transformation + state migration invariants;
- browser/device/input validation matrix;
- known OPEN questions and forbidden claims.

Design Studio then owns specialist visual/interaction exploration and validation. Web Manager retains product/site truth, content/task requirements, cross-channel governance and release/operations accountability.

No Design Studio canonical file is edited by this study.

---

## 8. Gate decision

**STAGE 4 FOUNDATION/PRACTITIONER INTEGRATION GATE: PASS.**

Reason: 045–049 cover the necessary visual-system domains and this integration demonstrates a coherent diagnostic/governance method across representative app-company page families without relying on unverified MintTap facts. No missing Stage 4 prerequisite was exposed that justifies another isolated visual-literacy block before curriculum progression.

This PASS is intentionally bounded to literacy and governance. Production design competence remains dependent on actual project transfer and Design Studio execution evidence.

## 9. Next curriculum move

Proceed to **Stage 5 — Accessibility**.

Highest-value first integrated block: **051 — Accessibility Foundations: Disability, Barriers, Standards, Conformance & App-Company Web Responsibility**.

Do not begin with a checklist of WCAG success criteria. Start from disability/access needs and barrier mechanisms, then establish WCAG 2.2 structure/conformance, semantic/keyboard/focus/non-text/visual/responsive relationships, limits of automated testing, and the distinction between technical conformance evidence and actual accessibility/usability. Reuse prior accessibility evidence where it adds validation rather than repeating it.

---

## Evidence classification summary

**SOURCE:** WCAG 2.2 W3C Recommendation; current Apple App Review metadata/product-representation requirements; current Google Play deceptive-behaviour/store-listing guidance.  
**SYNTHESIS:** design quality is a cross-layer task/truth preservation problem; visual consistency must be subordinate to semantic consistency; product imagery is governed evidence.  
**MINTTAP DIRECTION:** use the integrated diagnostic sequence and evidence package for future `minttap.app` design handoffs.  
**OPEN:** actual MintTap production inventory, brand system, assets, components, browsers/devices, user evidence and platform-specific requirements.  
**DEPENDENCY:** Design Studio specialist execution for exact Type/Color/Layout/Web decisions.  
**VALIDATION:** production browser/device/AT/human evidence remains required before production-ready claims.  
**CHANGE WATCH:** Apple/Google store and metadata policies are living requirements and must be rechecked near release.