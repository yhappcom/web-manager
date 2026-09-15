# 048 — Web Imagery, Iconography, App Screenshots & Product Demonstration Literacy

Date: 2026-09-15  
Stage: 4 — Web Design Literacy  
Checkpoint target: FOUNDATION / PRACTITIONER

## Why this block exists

MintTap is an Apple/Android app company. Its website will often need to explain products visually: app screenshots, icons, logos, illustrations, store badges and possibly short demonstrations. Those assets are not interchangeable decoration. They can carry product claims, task meaning, interaction meaning and accessibility obligations.

This block deliberately does **not** duplicate later image-delivery/performance work such as codec selection, compression pipelines, CDN policy or detailed LCP optimization. It establishes Web Manager judgment about **what an image means, whether it is truthful, how it survives responsive presentation, and what Design Studio must validate**.

Core model:

`communication purpose → evidence/semantic role → source/provenance → representation/crop → responsive context → accessible equivalent → product/store consistency → lifecycle/freshness → browser/human validation`

---

# 1. SOURCE — HTML images are selected resources, not fixed pixels

The WHATWG HTML Standard defines `srcset`/`sizes` for resolution/viewport-sensitive candidate selection and `picture`/`source` for art direction. The user agent can select a candidate based on effective display density, zoom and other conditions. Art direction may legitimately use different crops/content at different viewport conditions.

Primary source:
- WHATWG HTML — Images: https://html.spec.whatwg.org/dev/images.html

### SYNTHESIS

Responsive imagery has two distinct problems:

1. **resource selection** — same meaning/composition, different resolution/size;
2. **art direction** — different crop/composition because the available visual region changes.

Confusing these can either waste bytes or, more importantly for Stage 4, remove the very UI detail that supported the page claim.

### MINTTAP DIRECTION

A mobile crop of an app screenshot must preserve the evidence needed for the nearby claim. A crop that makes the composition prettier while hiding the relevant control/state is a communication failure even if the image remains technically responsive.

---

# 2. SOURCE — image alternatives depend on purpose and context

W3C WAI's current Images Tutorial (updated 2026-04-08) distinguishes informative, decorative, functional, images-of-text and complex images. Informative images need an equivalent for the information they convey; decorative images should normally use an empty text alternative; functional images need alternatives describing their function; complex information needs a fuller equivalent.

WAI also explicitly says the author determines an image's category from its purpose, context and content. The same bitmap can therefore require different alternative treatment in different uses.

Primary sources:
- W3C WAI Images Tutorial: https://www.w3.org/WAI/tutorials/images/
- W3C WAI alt Decision Tree: https://www.w3.org/WAI/tutorials/images/decision-tree/
- W3C WAI Decorative Images: https://www.w3.org/WAI/tutorials/images/decorative/
- W3C WAI Functional Images: https://www.w3.org/WAI/tutorials/images/functional/

### SYNTHESIS

`alt text != visual caption != filename description`.

The correct question is not “What is in this image?” but “What information or function would be lost here if the image were unavailable?”

### Example

A MintTap portfolio screenshot beside text already explaining the same three metrics may be largely redundant and need a concise or empty alternative depending on context. The same screenshot used as the only evidence of those metrics becomes informative and needs an equivalent that communicates the relevant information.

### FAILURE MODE

Automatically generating alt text such as `MintTap screenshot` for every screenshot creates little useful equivalence and can add repetitive screen-reader noise.

---

# 3. SOURCE — readable text should generally remain real text

W3C WAI recommends actual styled text rather than images of text because real text can resize and adapt to user presentation preferences. If image text must be used, its equivalent must carry the same words; logos are a recognized special case in WCAG treatment.

Primary source:
- W3C WAI Images of Text: https://www.w3.org/WAI/tutorials/images/textual/

### SYNTHESIS

Marketing copy should not be baked into a hero image merely to preserve a composition. This couples localization, zoom, text resizing, responsive adaptation and content maintenance to an image-production pipeline.

### MINTTAP DIRECTION

Keep headings, feature claims, CTA labels, support instructions and policy text as HTML text. Text embedded inside a **truthful app screenshot** is different: it is evidence of the actual product UI, not a substitute for the website's own prose.

---

# 4. SOURCE — app-store imagery is product evidence

Apple states that screenshots and app previews visually communicate the app's user experience. App Store Connect currently allows 1–10 screenshots per supported screenshot set and supports localization/device-size handling. Apple also says app previews must remain within the app itself and should avoid creating a false impression of the experience.

Google Play states that preview assets showcase app features/functionality and that screenshots must demonstrate the actual in-app/in-game experience, focusing on core features so users can anticipate the experience. Google recommends localized screenshots where screenshots contain text.

Primary/current sources checked 2026-09-15:
- Apple — Upload app previews and screenshots: https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots
- Apple — App Previews: https://developer.apple.com/app-store/app-previews/
- Google Play — Add preview assets to showcase your app: https://support.google.com/googleplay/android-developer/answer/9866151
- Google Play — Best practices for your store listing: https://support.google.com/googleplay/android-developer/answer/13393723

### SYNTHESIS — evidence continuity

The website is not identical to either store and may use different framing, crops and explanatory copy. But the underlying product evidence should remain consistent:

`website claim ↔ website screenshot/demo ↔ shipped app behavior ↔ store representation`

A polished mockup is not automatically deceptive, but it must not be presented as evidence of a shipped capability that does not exist.

### MINTTAP DECISION — Product Evidence Ledger

For important website screenshots/demos, maintain at least:

- app/product;
- platform (iOS/Android/web if applicable);
- source build/version;
- capture date;
- locale;
- actual capture / composited capture / concept classification;
- claim(s) supported;
- crop/framing variants;
- store-asset relationship if reused;
- known redactions or synthetic data;
- owner;
- retirement trigger (UI change, feature removal, terminology change, policy change).

This is a governance contract, not a claim that MintTap currently has such a ledger.

---

# 5. Screenshot framing: device frame, crop and annotation are claims

### SYNTHESIS

A screenshot can be technically genuine while its presentation becomes misleading through:

- cropping away prerequisites or warnings;
- enlarging a minor feature until it appears primary;
- combining UI states that cannot coexist;
- inserting labels inside the screenshot that resemble shipped UI;
- using a device frame that implies unsupported hardware/platform;
- recoloring the shipped UI to match the website brand;
- retaining an obsolete UI after the product changed.

Therefore screenshot truth has at least three layers:

`pixel provenance → presentation integrity → claim-context integrity`.

### MINTTAP DIRECTION

Annotations should be visibly external to the app UI unless they actually exist in the shipped UI. If a composited marketing treatment is used, its role must remain distinguishable from the captured product state.

Do not recolor actual screenshots merely to harmonize with the web palette. The screenshot is product evidence; the surrounding surface should adapt around it.

---

# 6. Iconography: glyph, meaning and control are separate

Design Studio Web W011 has already established direct iconography/non-text-signal practice; Web Manager should not duplicate icon drawing theory. The current Web specialist status also lists W011 runtime accessible-name/target/enlargement/forced-color validation as still open.

### SYNTHESIS

For website governance, separate:

- **glyph** — visual mark;
- **semantic meaning** — what the mark communicates;
- **control role** — what happens if it is interactive;
- **accessible name** — programmatic/user-facing equivalent where needed;
- **state** — selected/expanded/error/etc.;
- **target geometry** — interactive hit area;
- **environment resilience** — enlargement, forced colors, localization/context.

An icon that looks familiar does not prove that users understand it in a particular MintTap task.

### MINTTAP DIRECTION

Prefer visible text labels for unfamiliar, consequential or ambiguous actions. Icon-only controls require a defensible space/task reason plus accessible naming and later recognition/usability validation. Do not remove labels at narrow widths merely because an icon exists.

WAI explicitly cautions that responsive layouts sometimes drop icon labels and says the icon must remain readable/understandable and have a text description.

Source:
- W3C WAI Images Tips: https://www.w3.org/WAI/tutorials/images/tips/

---

# 7. Logos and brand marks

### SYNTHESIS

A company/app logo has an identity role different from an illustrative image. It may legitimately contain stylized text, but the surrounding HTML still needs to preserve the site's semantic identity/navigation purpose.

Logo usage must also avoid becoming an accessibility or responsive-layout trap: extremely wide lockups, text baked into decorative hero art, or relying on a mark alone for an unfamiliar product can weaken comprehension.

### OPEN

The repository does not currently establish the final production MintTap corporate logo system, app-by-app logo/wordmark rules, approved clear-space/minimum-size rules or dark/light asset variants. Do not invent them from previous exercises.

### DEPENDENCY — Design Studio

Color: validate brand-mark/surface combinations and forced-color/theme behavior where relevant.  
Web Design: validate logo/wordmark placement, responsive behavior and hierarchy in complete pages.  
Type: review wordmark-adjacent typography only if exact type relationships matter.

---

# 8. Responsive screenshot/product-demo contract

For every product-evidence media block define:

| Field | Question |
| --- | --- |
| purpose | What user question does this media answer? |
| evidence claim | Which exact feature/state does it prove or illustrate? |
| provenance | Which app/build/platform/locale produced it? |
| semantic class | informative, decorative, functional, complex, identity? |
| alt/equivalent | What information/function must survive without pixels? |
| crop invariant | What must never be cropped away? |
| art-direction freedom | What may change between wide/narrow composition? |
| annotation boundary | Which labels are website annotation vs shipped UI? |
| text/localization | Is meaningful text trapped inside the image? Is a locale-specific asset needed? |
| theme/color | Is this actual shipped appearance? Does surrounding UI preserve distinction? |
| responsive layout | What happens at narrow widths/zoom/text enlargement? |
| lifecycle | What product change invalidates this asset? |
| validation | Which browser/device/human checks remain required? |

This becomes the **Product Media / Non-Text Contract**.

---

# 9. Failure taxonomy for MintTap review

1. **Decorative masquerading as evidence** — attractive phone mockup adds no useful product understanding.
2. **Evidence without provenance** — no one knows which build produced the screenshot.
3. **Stale evidence** — UI changed but website asset did not.
4. **Crop destroys claim** — responsive art direction removes the relevant control/state.
5. **Image-of-text dependency** — website copy/localization trapped in raster media.
6. **Alt redundancy/noise** — adjacent prose and alt repeat the same content without value.
7. **Missing equivalent** — screenshot/chart contains unique information unavailable otherwise.
8. **Icon ambiguity** — familiar-looking glyph has uncertain task meaning.
9. **Icon-only responsive regression** — label disappears on mobile without evidence that recognition survives.
10. **False visual continuity** — screenshot recolored/composited so users expect a UI the app does not ship.
11. **Platform implication error** — framing suggests iPhone/Android/tablet support not actually established.
12. **Asset-localization drift** — website locale changes but screenshot language remains mismatched without deliberate reason.

---

# 10. Design Studio handoff

## Web Design

Provide the Product Media / Non-Text Contract plus actual product assets. Ask Web Design to validate:
- media hierarchy inside complete pages;
- crop/art-direction behavior;
- icon label retention and responsive treatment;
- screenshot/card/component composition;
- real browser enlargement/forced-color behavior where relevant.

Current specialist state checked 2026-09-15: **Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED**. W012 adds executed Chromium responsive transfer, but integrated icon runtime and broader browser/device/AT evidence remain open.

## Color

Current specialist state: **Stage 1 PASS; Stage 2 entry audit next**. Ask Color to validate screenshot/surface coexistence, logo variants, semantic non-color cues and theme/forced-color cases. Do not treat Color Foundation PASS as production Web integration.

## Layout / Interaction

Hand off icon-control state/target/label cases and any screenshot gallery/carousel interaction. Geometry and interaction semantics remain L/I responsibilities.

## Type

Hand off only where text inside/around product imagery, wordmarks or localization creates exact type/fallback/wrapping dependencies.

No Design Studio canonical file is modified by this study.

---

# 11. What is verified vs not verified

## VERIFIED / SOURCE

- HTML supports responsive image candidate selection and art direction through `srcset`/`sizes` and `picture`/`source`.
- Image alternatives depend on information/function/context; decorative images should normally be ignored with an empty alternative.
- WAI recommends real text over images of text for ordinary readable content.
- Apple screenshots/previews are intended to communicate app user experience; current App Store Connect permits 1–10 screenshots per supported set.
- Google Play requires/recommends preview assets that demonstrate actual in-app experience and recommends localization when screenshot text is present.
- Design Studio Web has Stage 1 PASS and Stage 2 practice; W011 iconography practice exists but runtime icon validation remains open per current specialist status.

## SYNTHESIS

- Product screenshots should be governed as evidence, not decoration.
- Screenshot truth requires provenance, presentation integrity and claim-context integrity.
- Responsive art direction must preserve claim-relevant evidence.
- Icon glyph familiarity does not prove task comprehension.
- Website/store visual continuity should preserve product truth without requiring identical composition.

## OPEN

- actual MintTap/LogMate website media inventory;
- production logo/wordmark system;
- approved screenshot sources and current app builds;
- actual supported locales and device/platform presentation requirements;
- whether website dark mode is required;
- browser/device/AT validation matrix;
- human icon recognition and screenshot comprehension evidence;
- policy for synthetic/redacted user data in captures.

---

# 12. Competency check

This checkpoint is PASS at Foundation/Practitioner level if the Web Manager can:

- distinguish decorative, informative, functional, identity and complex non-text content by purpose;
- decide when a screenshot is evidence and identify what claim it supports;
- distinguish responsive resource selection from art direction;
- diagnose misleading crop/composite/stale-asset failures;
- specify an accessible equivalent without mechanically describing pixels;
- separate icon glyph, semantic meaning, control role, accessible name and state;
- maintain store↔web product truth while allowing different compositions;
- hand exact media obligations to Design Studio without taking over specialist visual authorship;
- identify unresolved product/build/browser/human evidence rather than claiming production readiness.

**Checkpoint verdict: PASS — FOUNDATION/PRACTITIONER.**

The checkpoint does **not** establish WCAG conformance, production asset correctness, current MintTap product truth, store approval, cross-browser/device parity or human comprehension.

---

# 13. Next highest-value Stage 4 block

**049 — Components, Page Systems, Visual Consistency & Responsive Design-System Governance.**

Reason: 045–048 now establish hierarchy/composition, typography/reading, color/state and imagery/non-text literacy. The next prerequisite is to integrate these into reusable components/page systems without confusing visual sameness with semantic consistency. This should cover component role/state contracts, variants, responsive composition, design tokens as implementation contracts, drift detection and app-company multi-product reuse. Avoid duplicating frontend engineering depth or later performance/accessibility stages.
