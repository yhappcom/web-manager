# 006 — Accessibility Production Baseline for `minttap.app`

Status: **FOUNDATION / PRODUCTION BASELINE**  
Date: 2026-09-14  
Target: MintTap company, app, privacy, support and account-control web surfaces

## Question

What accessibility requirements must be designed into `minttap.app` before visual styling and implementation, and what validation is required before a page can be considered production-ready?

This study converts WCAG/WAI guidance and relevant Design Studio work into a MintTap-specific production contract.

---

## MINTTAP DECISION — WCAG 2.2 AA is the internal production target

MintTap web work should target **WCAG 2.2 Level AA** as its default technical/design baseline unless a later jurisdiction or customer requirement imposes something stronger.

This is an internal quality target. It is not, by itself, a claim that satisfying WCAG resolves every jurisdiction-specific legal accessibility obligation.

Normative source:
- https://www.w3.org/TR/WCAG22/

### Why this matters for MintTap

Accessibility affects launch-critical surfaces, not only marketing pages:

- privacy policies;
- support and FAQ pages;
- contact forms;
- account deletion/data-control flows;
- app download/navigation pages;
- future authenticated web tools.

If these pages are inaccessible, the problem can block users from exercising account/data rights or obtaining support.

---

## SOURCE — page structure must be programmatically meaningful

W3C WAI's Page Structure guidance explains that well-structured content enables efficient navigation and that HTML/WAI-ARIA regions and headings should reflect the logical organization of the page.

Sources:
- https://www.w3.org/WAI/tutorials/page-structure/
- https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
- https://www.w3.org/WAI/tutorials/page-structure/headings/

### MINTTAP DECISION — semantic HTML first

Use native semantic HTML whenever it correctly expresses the interface:

- `<header>` for the site banner area;
- `<nav>` for navigation;
- one primary `<main>` landmark per document context;
- `<footer>` for site-wide footer/content information;
- `<section>` only when it represents a meaningful section, normally with an accessible name/heading;
- native `<button>`, `<a>`, `<input>`, `<select>`, `<textarea>`, `<fieldset>`, `<legend>` rather than generic `<div>` controls.

ARIA supplements semantics; it does not replace correct native HTML without reason.

### Heading contract

- Every normal page has a meaningful page-level `<h1>`.
- Heading levels express document structure, not visual font size.
- Avoid skipping ranks when introducing nested subsections where practical.
- Privacy/legal pages must remain understandable as an outline when headings are listed without body text.
- FAQ question headings should form a predictable hierarchy rather than visually styled anonymous text blocks.

### Landmark contract

- Repeated page regions must be distinguishable when more than one of the same landmark type exists.
- A keyboard/screen-reader user must be able to identify primary navigation, main content and footer/content-info.
- Provide a bypass mechanism/skip-to-main behavior for repeated navigation blocks.

Relevant WCAG:
- 1.3.1 Info and Relationships;
- 2.4.1 Bypass Blocks;
- 2.4.6 Headings and Labels.

---

## SOURCE — native controls reduce accessibility implementation risk

WCAG 2.2 SC 4.1.2 requires user-interface components to expose programmatically determinable names and roles, and appropriate states/properties/values. W3C notes that standard HTML controls used according to specification already provide much of this behavior.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/name-role-value

WAI APG guidance also requires interactive elements to have usable accessible names.

Source:
- https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/

### MINTTAP DECISION

Do not build a custom interactive element merely for visual styling when a native element can express the same function.

Examples:

- navigation destination → `<a href>`;
- action → `<button>`;
- checkbox → native checkbox;
- text input → native input with `<label>`;
- disclosure/accordion → use a proven accessible pattern or native semantics where appropriate.

Every interactive control must expose an accessible name that describes **purpose**, not appearance.

Examples:
- good: `Delete account`, `Close dialog`, `Download on the App Store`;
- weak: `X`, `Icon`, `Click here` where context does not resolve purpose.

---

## SOURCE — all functionality must work through a keyboard

WCAG 2.2 SC 2.1.1 requires all functionality to be operable through a keyboard interface except where the underlying function genuinely depends on movement path. SC 2.1.2 prevents keyboard traps.

Sources:
- https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
- https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html

### MINTTAP DECISION

Every MintTap web task must be completable without a mouse, including:

- opening/closing menus;
- navigating app cards/links;
- expanding FAQ items;
- completing support/contact forms;
- completing account-deletion/data-control forms;
- dismissing dialogs;
- confirming or cancelling destructive actions;
- changing locale if a locale switcher exists.

No component may trap focus unintentionally.

Keyboard validation is mandatory even on pages expected to be used primarily on phones.

---

## SOURCE — focus order, focus visibility and focus obstruction matter

WCAG 2.2 requires logical focus order (2.4.3), visible focus (2.4.7), and at Level AA, focused components must not be entirely hidden by author-created content (2.4.11).

Sources:
- https://www.w3.org/WAI/WCAG22/Understanding/focus-order
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum

### MINTTAP DECISION

- Never globally remove browser focus outlines without providing an equal or stronger visible replacement.
- Prefer `:focus-visible` styling for intentional keyboard focus appearance where appropriate.
- DOM order should normally produce the intended reading/focus order; do not use positive `tabindex` values to patch a visually reordered DOM.
- Sticky headers, cookie/consent surfaces, floating support controls and bottom bars must not cover focused elements.
- Modal/dialog flows must deliberately manage focus entry, containment while modal, and return focus on close.

For irreversible account deletion, the confirmation dialog should bias against accidental destructive confirmation. WAI APG's alert-dialog example places initial focus on the least destructive action.

Source:
- https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/examples/alertdialog/

### MINTTAP DECISION — destructive confirmation

For irreversible destructive actions:

- clearly name the action and consequence;
- provide explicit cancel and confirm controls;
- do not make destructive confirmation the default keyboard focus unless a specific, reviewed reason exists;
- restore focus meaningfully if the dialog is cancelled;
- announce completion/failure programmatically.

---

## SOURCE — responsive design must survive reflow and text enlargement

WCAG Reflow requires content to remain usable without loss of information/functionality and without two-dimensional scrolling at a width equivalent to 320 CSS pixels for normal vertically scrolling content, with exceptions for genuinely two-dimensional content.

Source:
- https://www.w3.org/WAI/WCAG21/Understanding/reflow

WCAG 2.2 SC 1.4.4 requires text to be resizeable up to 200% without loss of content or functionality.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html

### MINTTAP DECISION — stress conditions are part of layout design

Production layouts must be tested at minimum for:

- narrow width equivalent to 320 CSS px;
- 200% text enlargement;
- browser zoom scenarios that trigger responsive recomposition;
- long Korean and English content;
- long unbroken URLs/identifiers on legal/support surfaces.

Normal page content must not require simultaneous horizontal and vertical scrolling merely because the layout was designed as a fixed desktop canvas.

Long URLs, email addresses or technical identifiers must wrap or otherwise remain readable without breaking the page.

### Two-dimensional exception

If a future page contains genuinely two-dimensional content such as a large data table, the exception applies to the two-dimensional object—not as justification for making the entire page horizontally scrolling.

---

## SOURCE — pointer targets have a WCAG 2.2 AA minimum

WCAG 2.2 SC 2.5.8 defines a Level AA minimum target-size rule of 24×24 CSS pixels, with specified exceptions including spacing, inline links and equivalent controls.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum

### MINTTAP DECISION

Treat 24×24 CSS px as a **conformance floor, not a preferred component size**.

For primary buttons, menu controls, locale switchers, FAQ disclosures and destructive/cancel actions, design for comfortable touch/pointer operation beyond the minimum where page density permits.

The actual interactive hit region—not the visual icon size—is what matters.

Do not create rows of tightly packed tiny icon controls merely to achieve visual compactness.

---

## SOURCE — forms need labels, instructions and error feedback

WAI's Forms Tutorial recommends:

- labels for form controls;
- grouping related controls;
- clear instructions;
- validation feedback;
- success/error notifications;
- simple forms requesting only needed information.

Sources:
- https://www.w3.org/WAI/tutorials/forms/
- https://www.w3.org/WAI/tutorials/forms/labels/
- https://www.w3.org/WAI/tutorials/forms/instructions/
- https://www.w3.org/WAI/tutorials/forms/notifications/

WCAG SC 3.3.1 requires automatically detected input errors to identify the item in error and describe the error in text.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html

### MINTTAP DECISION — form contract

For support, contact and account/data-control forms:

- every input has a persistent programmatically associated label;
- placeholders do not replace labels;
- required/optional state is communicated in text/programmatically, not color alone;
- input format instructions are available before error occurs when useful;
- related choices use `fieldset`/`legend` or equivalent correct grouping;
- preserve valid user input after a validation error;
- identify invalid fields in text;
- provide specific correction guidance when possible;
- visually styled error state is supplemental to textual/programmatic error information;
- successful submission produces an explicit confirmation;
- failure produces recovery guidance, not a silent spinner or generic disappearance.

### Account deletion/data request special rule

Do not request unrelated personal data merely because the form can collect it. Ask only for information needed to authenticate/route/execute the request.

If identity verification is required, explain why and what happens next before submission.

---

## SOURCE — status changes must be exposed without unnecessary focus movement

WCAG 2.2 SC 4.1.3 requires status messages to be programmatically determinable so assistive technology can announce them without requiring focus to move to the message.

Source:
- https://www.w3.org/TR/WCAG22/#status-messages

W3C's failure guidance gives examples such as search/result messages that visually update but are not exposed through an appropriate status mechanism.

Source:
- https://www.w3.org/WAI/WCAG22/Techniques/failures/F103

### MINTTAP DECISION

Dynamic states such as:

- `Sending…`;
- `Request submitted`;
- `3 errors found`;
- `Link copied`;
- `No results`;
- network retry/progress messages

must be surfaced programmatically when they qualify as status messages.

Choose the appropriate mechanism (`status`, `alert`, `aria-live`, `output`, etc.) based on urgency and behavior; do not make every routine status assertive.

Do not move focus merely to announce every non-critical status update.

---

## SOURCE — page language must be programmatically determinable

WCAG SC 3.1.1 requires the default human language of each web page to be programmatically determined.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/language-of-page

### MINTTAP DECISION

Every rendered page must declare the correct HTML language tag, initially expected to include at least:

- Korean page → `lang="ko"`;
- English page → `lang="en"`.

Meaningful passages in another language should be marked appropriately when necessary.

This becomes a dependency for the localization architecture study.

---

## SOURCE — help mechanisms should be consistently located

WCAG 2.2 SC 3.2.6 (Level A) requires repeated help mechanisms to occur in the same relative order across a set of pages.

Source:
- https://www.w3.org/WAI/WCAG22/Understanding/consistent-help

### MINTTAP DECISION

MintTap already requires stable support/contact surfaces for app operations. Therefore:

- support/contact access should be predictably located across app pages;
- do not move Help/Support arbitrarily between header, footer and body from app to app without reason;
- if a support mechanism changes responsive position, its semantic/serialized order must remain coherent;
- contact hours/availability should be stated when a human support channel is not continuously staffed.

---

## Color and typography dependencies

This study does not duplicate the full Design Studio Color and Type programs.

However, production accessibility requires their evidence for:

- text/background contrast;
- non-text/focus contrast;
- color-independent state communication;
- readable hierarchy;
- line wrapping and typography under Korean/English expansion;
- font loading/fallback;
- enlarged-text behavior.

### MINTTAP DECISION

No design is considered accessibility-complete based only on semantic HTML if contrast, text scaling or typography behavior fails in actual rendering.

---

## Design Studio reuse

Relevant existing Design Studio study:

`yhappcom/design-studio/research/004-accessibility-reflow-targets-focus.md`

That study already establishes key principles:

- reflow is semantic recomposition, not shrinking a desktop canvas;
- visible graphics and interactive hit regions are distinct;
- focus is structural information, not decoration;
- gesture-dependent functions require alternative operation where applicable.

### TRANSFER VALIDATION

MintTap will use its real privacy/support/account-control surfaces as a production transfer context for these principles.

Findings that confirm or challenge the studio abstractions should be handed back to the relevant Web / Layout & Interaction / Type / Color specialist.

---

## MINTTAP component/page acceptance rules

### Global shell

- semantic header/nav/main/footer structure;
- skip/bypass mechanism;
- logical DOM/read/focus order;
- correct page `<title>` and page `<h1>`;
- consistent support access;
- correct page language;
- keyboard-operable navigation;
- visible non-obscured focus.

### App product page

- store-download buttons/links have clear purpose;
- screenshots have appropriate text alternatives or are intentionally decorative only when their information is fully duplicated;
- feature hierarchy survives 200% text and narrow reflow;
- carousel or gallery, if used, cannot become a keyboard/screen-reader trap;
- no critical feature claim exists only inside an image.

### Privacy/legal page

- heading outline remains coherent;
- long URLs and technical terms wrap;
- text remains usable at 200%;
- links identify their destination/purpose in context;
- no fixed-height text boxes containing policy content;
- update/effective-date information is actual text.

### Support/FAQ

- questions/sections use structural headings/disclosures;
- search/filter status is announced when dynamic;
- support mechanisms remain consistently locatable;
- error/empty results provide next action.

### Account deletion/data control

- irreversible consequences stated before confirmation;
- form labels/instructions persistent;
- validation errors specific and textual;
- keyboard path complete;
- destructive confirmation accessible and deliberately focused;
- success/failure/progress status announced;
- user can cancel without losing orientation;
- no unexplained timeout blocks completion.

---

## Production validation matrix

Accessibility is validated early and repeatedly, not once at launch.

W3C explicitly notes that automated evaluation tools cannot determine all accessibility aspects and that knowledgeable human evaluation is required.

Sources:
- https://www.w3.org/WAI/test-evaluate/
- https://www.w3.org/WAI/test-evaluate/tools/selecting/

### Required automated checks

Use one or more reputable automated accessibility checks in development/CI to catch machine-detectable failures, but never treat a zero-error scan as PASS by itself.

Automatable examples:
- missing/duplicate basic semantics;
- many accessible-name failures;
- some contrast failures;
- invalid ARIA patterns;
- missing page language/title;
- some form-label issues.

### Required manual browser checks

For representative pages:

- keyboard-only traversal from top to bottom;
- reverse traversal (`Shift+Tab`);
- activate every interactive control without pointer;
- verify visible focus and no obscuring sticky surfaces;
- zoom/text resize to 200%;
- reflow at narrow equivalent width;
- verify long Korean/English labels/content;
- validate modal open/close/focus return;
- validate errors and status messages;
- verify pointer/touch target usability.

### Required assistive-technology spot checks

Before production PASS, representative templates and critical flows require screen-reader testing in supported browser/OS combinations.

Priority flows:
- global navigation;
- support/contact;
- privacy page navigation;
- account deletion/data request;
- dynamic errors/status;
- locale switching.

Exact test matrix (VoiceOver/Safari, NVDA/Firefox/Chrome, etc.) remains to be chosen based on target audience/platform support.

### Human validation

Where product risk warrants it, involve users with disabilities or knowledgeable accessibility reviewers. User testing complements but does not replace standards evaluation.

Source:
- https://www.w3.org/WAI/test-evaluate/involving-users/

---

## RELEASE BLOCKERS

The following are accessibility blockers for an affected launch-critical flow:

- required function cannot be completed by keyboard;
- keyboard trap;
- invisible focus on operable controls;
- focused controls hidden by site-authored sticky/overlay content;
- account deletion/support form controls without usable labels;
- errors communicated only by color or not described in text;
- critical success/error/progress status unavailable to assistive technology;
- essential content clipped/lost at required text enlargement/reflow;
- inaccessible destructive confirmation that risks unintended account deletion;
- wrong/missing page language on localized production page where assistive pronunciation is materially affected.

Other accessibility defects are severity-ranked based on task impact but must not be ignored merely because they are outside a launch-critical flow.

---

## OPEN

- Exact supported browser/assistive-technology test matrix is not yet selected.
- Final component target dimensions await Design Studio Layout/Interaction application; WCAG 24×24 is only a minimum floor.
- Final contrast tokens depend on Design Studio Color work and actual page theme.
- Final typography scale/fallback depends on Type and Web Design validation.
- Consent/cookie interfaces are not yet in scope because analytics/cookie architecture is not selected.
- Authentication accessibility is future scope if `minttap.app` gains authenticated account management.
- Multimedia caption/transcript requirements will become material if product videos/audio are added.

---

## CHANGE WATCH

Re-check when:

- WCAG/WAI guidance or target version changes;
- major component library/framework changes;
- navigation/global shell changes;
- new locale/scripts are introduced;
- authenticated flows are added;
- support/contact/account deletion processes materially change;
- a new third-party widget/chat/consent system is introduced.

Third-party widgets do not receive an accessibility exemption merely because MintTap does not author their code.

---

## Foundation conclusion

Accessibility for `minttap.app` is a **page-system and interaction property**, not a visual QA task at the end.

The baseline is:

**semantic structure → native controls → keyboard completeness → logical/visible focus → responsive reflow/text scaling → clear form/error/status behavior → correct language → automated + manual + assistive-technology validation**.

MintTap should not accept production designs that require accessibility to be “added later,” because doing so changes information architecture, component geometry, interaction behavior and content structure after the system has already hardened.
