# 031 — Browser Document & Runtime Foundations: HTML, CSS, JavaScript, DOM and Accessibility Tree

Status: **STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Purpose

This study establishes the browser/document mental model required before moving into rendering architectures, storage/state, navigation and later accessibility/performance work.

The objective is not to learn frontend coding syntax. The objective is to understand what the browser receives, which internal structures it creates, how HTML/CSS/JavaScript interact, why those technologies are separate, how dynamic mutation changes the page, and why the accessibility representation is not simply a copy of the DOM.

The Web Manager must be able to distinguish:

- source HTML from the parsed DOM;
- document semantics from visual presentation;
- CSS cascade from layout;
- ECMAScript language semantics from browser-provided Web APIs;
- DOM events from arbitrary application callbacks;
- DOM structure from accessibility API exposure;
- a visible defect from the layer that actually caused it.

---

# 1. Historical problem: the Web needed structure, presentation and programmability

## SOURCE

W3C records that Tim Berners-Lee created the first version of HTML as the Web's primary publishing format alongside the early URI and HTTP specifications.

W3C's CSS history explains that HTML intentionally emphasized document structure rather than presentation. By 1994, HTML was widely used, but authors needed richer presentation control. Work on CSS began at CERN in 1994, and CSS1 became a W3C Recommendation in December 1996.

Ecma records that work on ECMAScript standardization began in November 1996 and the first ECMA-262 edition was approved in 1997, following the emergence of JavaScript in browsers.

Primary historical references:
- W3C Web history: https://www.w3.org/about/history/
- W3C CSS1 history/press release: https://www.w3.org/press-releases/1996/css1-rec/
- W3C CSS history: https://www.w3.org/Style/CSS20/history.html
- Ecma-262 history: https://ecma-international.org/news/ecma-262-the-ecmascript-javascript-the-most-popular-web-scripting-standard-is-celebrating-its-20th-birthday/

## SYNTHESIS

The familiar separation into HTML, CSS and JavaScript is not arbitrary tooling convention. It reflects three distinct needs that emerged as the Web grew:

1. **document/content structure and semantics**;
2. **presentation and layout**;
3. **programmable behavior and stateful interaction**.

The separation is not absolute—each layer can influence the others—but it remains one of the Web's most important architectural boundaries.

### Durable mental model

- HTML says primarily **what the document contains and what those things mean**.
- CSS says primarily **how those document structures are presented and laid out**.
- JavaScript/ECMAScript provides a programming language that, together with browser Web APIs, can **observe and change document/runtime state and respond to events**.

This is a conceptual model, not a claim that modern framework code maps one file per layer.

---

# 2. HTML is a language with defined parsing behavior, not merely angle-bracket text

## SOURCE — WHATWG HTML Living Standard

The HTML Standard defines a specific parser for `text/html`. It tokenizes input and performs tree construction to dynamically build/modify a DOM `Document`. The specification explicitly notes that HTML has its own parsing rules; it is not XML or SGML parsing in modern browsers.

Current reference checked 2026-09-14:
- WHATWG HTML parsing: https://html.spec.whatwg.org/multipage/parsing.html

## FOUNDATION

When a browser receives HTML source, it does not simply display the source text. Conceptually:

`HTML bytes/text → tokenization → tree construction → DOM Document`

That process matters because malformed or omitted markup can be repaired/interpreted according to HTML's defined error-recovery rules.

### Consequence

**View Source ≠ DOM inspector.**

The source shows received/serialized author markup. The DOM inspector shows the browser's current parsed and possibly mutated node tree.

JavaScript can later add/remove/reorder nodes, and the parser itself can create a tree that differs from a naïve reading of malformed markup.

### Web Manager diagnostic rule

When a page structure appears wrong, ask separately:

1. What HTML was delivered?
2. What DOM did the HTML parser construct?
3. Did JavaScript mutate that DOM later?
4. Is CSS making correct structure appear visually different?

---

# 3. Semantics and appearance are different dimensions

## FOUNDATION

HTML elements carry semantics that can matter to:

- browser default behavior;
- keyboard interaction;
- form submission;
- accessibility API mapping;
- search/document interpretation;
- scripting APIs;
- user-agent features such as context menus or link handling.

A semantic element does not need a special visual appearance. CSS can change how it looks without changing its underlying HTML meaning.

Likewise, a generic `div` styled to look like a button does not automatically acquire native button behavior, keyboard activation semantics or accessibility mapping.

## SOURCE / ACCESSIBILITY CROSS-CHECK

W3C ARIA Authoring Practices explicitly advises using native HTML elements wherever possible when equivalent semantics exist. Native elements often provide browser behavior and accessibility semantics automatically.

Reference:
- W3C APG structural roles: https://www.w3.org/WAI/ARIA/apg/practices/structural-roles/

## SYNTHESIS

This creates an important Web Manager principle:

> Visual equivalence does not imply semantic or behavioral equivalence.

This will become central in Stage 5 Accessibility and Stage 4 Web Design Literacy.

---

# 4. The DOM is a browser/platform object model, not the original HTML file

## SOURCE — WHATWG DOM Standard

The DOM Standard defines node trees, documents, event targets and event dispatch. A document tree is a node tree rooted in a `Document`. It also defines shadow trees and event behavior.

Current reference checked 2026-09-14:
- WHATWG DOM Standard: https://dom.spec.whatwg.org/

## FOUNDATION

DOM stands for Document Object Model. It provides structured objects/interfaces through which browser features and script can inspect and manipulate the document.

A DOM node tree can include:
- document nodes;
- elements;
- text nodes;
- comments;
- shadow roots and related tree structures where used.

### Important distinction

`HTML source → parser → DOM`

but:

`DOM ≠ source code`

The DOM is runtime state.

### Dynamic example

An initial HTML response may contain an empty container. JavaScript may fetch data and append rows later. A user sees the generated rows even though they were absent from the original response body.

Therefore diagnostics for SEO, accessibility, hydration/rendering bugs and performance must distinguish **delivered source** from **runtime DOM**.

---

# 5. CSS is a rule system whose first problem is value resolution, not 'making things pretty'

## SOURCE — W3C CSS Cascading and Inheritance

CSS is defined as a language for describing rendering of structured documents. The cascade resolves competing declarations into values for properties on elements. The modern cascade considers origin/importance, encapsulation context, style attributes, cascade layers, specificity, scoping proximity and source order according to the applicable specification level.

References:
- CSS Cascading and Inheritance Level 6: https://www.w3.org/TR/css-cascade-6/
- CSS Display: https://www.w3.org/TR/css-display-3/
- CSS Box Model: https://www.w3.org/TR/css-box-4/

Note: Cascade Level 6 is a Working Draft; its page explicitly says implementers should use Level 5 as the stable reference where appropriate. The Stage 1 lesson here uses durable cascade concepts, not unstable Level-6-only features as production requirements.

## FOUNDATION

Before layout occurs, browsers must determine **which value applies** when multiple CSS declarations target the same property.

This is the cascade problem.

The common beginner shortcut:

`higher specificity always wins`

is incomplete. Specificity is only one stage in cascade ordering. Origin/importance and other cascade dimensions can outrank it.

### Inheritance

Some computed/property values can inherit from parent elements; others do not. Inheritance is separate from selector matching and cascade precedence.

### Web Manager implication

A CSS defect may be caused by:
- selector not matching;
- declaration losing in the cascade;
- inherited value;
- property invalid at computed-value time;
- layout algorithm behavior;
- intrinsic size/available space;
- browser default/user style;
- responsive condition/media/container query;
- animation/transition state.

Calling all of these “CSS specificity problems” is poor diagnosis.

---

# 6. DOM tree and CSS box/layout structures are related but not identical

## SOURCE

CSS Display and Box Model specifications define formatting/box behavior applied to document elements. CSS can suppress or alter box generation and select different formatting contexts.

## FOUNDATION

The browser does not simply draw one rectangle for every DOM element.

Examples:
- `display: none` can prevent an element/subtree from generating ordinary boxes;
- pseudo-elements can generate visual content not represented as ordinary author DOM elements;
- CSS layout modes such as block, flex and grid establish different formatting behavior;
- positioned elements can appear visually far from their DOM-order neighbors.

### Critical principle

**DOM order, visual order and accessibility/navigation order can diverge.**

That divergence is sometimes legitimate, but it creates risk when visual rearrangement changes the perceived sequence while keyboard or assistive-technology navigation continues to follow another order.

This becomes a direct handoff point to Design Studio Layout/Interaction and Web Design.

---

# 7. JavaScript language ≠ browser platform APIs

## SOURCE — TC39 / ECMAScript

TC39 maintains the ECMAScript language specification. The current live specification states that the TC39 document is the most up-to-date ECMAScript definition, including finished proposals beyond the latest annual snapshot.

Reference:
- https://tc39.es/ecma262/

## FOUNDATION

JavaScript in a browser is commonly discussed as if everything available to script were “JavaScript.” This is imprecise.

### ECMAScript provides language machinery
Examples:
- types and values;
- objects/functions;
- promises;
- modules;
- language syntax and execution semantics.

### Browser standards provide Web APIs
Examples include:
- `document` / DOM interfaces;
- event targets;
- `fetch`;
- timers;
- history/navigation APIs;
- storage APIs;
- many device/media capabilities.

## SYNTHESIS

A runtime bug can therefore come from at least two different conceptual sources:

1. language/application logic;
2. browser/Web API behavior or lifecycle timing.

This distinction becomes important in framework debugging and browser compatibility work.

---

# 8. Script loading can interact with HTML parsing

## SOURCE — WHATWG HTML

For classic external scripts:
- without `async` or `defer`, fetching/evaluation can block HTML parsing;
- `defer` permits parallel fetching and evaluates after parsing;
- `async` permits parallel fetching and evaluates when ready, potentially before parsing finishes.

For module scripts, dependencies are fetched in parallel and modules normally execute after parsing unless `async` changes that behavior; `defer` has no effect on module scripts.

Reference:
- WHATWG HTML scripting: https://html.spec.whatwg.org/multipage/scripting.html

## FOUNDATION

This explains a fundamental class of runtime defects:

A script can execute before a DOM element it expects has been parsed/created.

The lesson is broader than “put scripts at the bottom.” Modern loading modes and modules provide explicit lifecycle behavior.

### Performance connection

Parser blocking is also a Stage 7 performance concern. The current Stage 1 requirement is only to understand that **resource loading/execution timing affects document construction and interactivity**.

---

# 9. Events are a platform model for signaling and interaction

## SOURCE — WHATWG DOM

The DOM Standard defines `EventTarget`, event listeners and event dispatch through phases including capture, target and bubble behavior where applicable.

## FOUNDATION

Events allow browser/platform occurrences and user interactions to be observed without scripts continuously polling all state.

Typical events may signal:
- user activation/input;
- focus changes;
- document/resource lifecycle;
- network-related API completion;
- custom application-defined occurrences.

### Important distinction

An event listener attached to an ancestor can observe events from descendants when propagation rules permit. Therefore event behavior follows the runtime tree/event path rather than merely the source line where an element was written.

### Web Manager relevance

When an interface appears to “ignore clicks” or “trigger twice,” root causes can include:
- incorrect DOM target;
- propagation/bubbling;
- duplicate listeners;
- default browser behavior;
- overlay/layout interception;
- disabled/inert state;
- application state logic.

The visible symptom alone does not identify the layer.

---

# 10. Browser defaults are part of the platform, not accidental styling

## SYNTHESIS FROM HTML/CSS/ARIA SOURCES

Native elements combine several capabilities:
- semantics;
- built-in interaction behavior;
- default styles supplied by the user agent;
- keyboard/focus behavior;
- form behavior where applicable;
- accessibility API mappings;
- platform integration.

Custom widgets can reproduce these, but then authors assume responsibility for the missing behavior.

This is why “resetting all browser defaults and rebuilding everything” has a real engineering/accessibility cost even if the visual result is attractive.

### MintTap direction

For future `minttap.app` work, Web Manager should treat **native semantics and controls as the default baseline**, customizing them when project requirements justify the cost rather than assuming bespoke components are inherently superior.

This is a provisional architectural direction, not a visual design rule.

---

# 11. Accessibility tree/API exposure is not a direct DOM clone

## SOURCE — W3C Core-AAM and HTML-AAM

Core Accessibility API Mappings describes how user agents expose web semantics through platform accessibility APIs. HTML-AAM defines how HTML elements/attributes map to those APIs.

Current references checked 2026-09-14:
- Core-AAM 1.2 Candidate Recommendation Draft, 5 Aug 2026: https://www.w3.org/TR/core-aam/
- HTML-AAM 1.0 Working Draft, 5 Aug 2026: https://www.w3.org/TR/html-aam/

These specifications are evolving documents; exact mappings remain implementation/change-watch territory.

## FOUNDATION

Assistive technologies generally do not consume “the DOM” as a raw one-to-one tree. Browsers compute and expose relevant accessibility information through platform accessibility APIs.

That exposure can include concepts such as:
- role;
- accessible name;
- state/property;
- relationships;
- value;
- actions/events.

Some DOM nodes may be omitted from accessibility exposure, while semantics may be derived from native HTML or ARIA.

### Example

A decorative image with appropriate empty alternative semantics can be omitted from meaningful accessibility exposure, while an interactive control needs role/name/state information.

### Critical principle

`DOM tree ≠ accessibility tree/API representation`

and

`visual tree/layout ≠ accessibility tree`

This is why screenshots alone cannot establish accessibility correctness.

---

# 12. Accessible name, role and state are computed semantics

## SOURCE

W3C accessibility guidance documents accessible naming mechanisms and the role of native HTML labels and ARIA labeling.

Reference:
- W3C APG Names and Descriptions: https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/

## FOUNDATION

A control that visually contains an icon may have no meaningful accessible name unless naming semantics are provided.

Conversely, an element's accessible name can come from multiple sources according to host-language and accessibility-name rules.

### Implication

Accessibility cannot be judged only from:
- visible text;
- DOM tag name;
- CSS appearance;
- ARIA attribute presence.

Correctness depends on the computed semantic result exposed by the browser and on actual keyboard/assistive-technology behavior.

This will be studied rigorously in Stage 5.

---

# 13. ARIA supplements semantics; it does not magically implement behavior

## SOURCE

W3C APG advises native HTML where possible. ARIA roles/properties can communicate semantics but do not automatically implement the full native interaction model.

## FOUNDATION

For example, assigning `role="button"` to a generic element does not by itself guarantee:
- keyboard focusability;
- Space/Enter activation behavior;
- disabled behavior;
- form integration;
- all browser-native interaction details.

### Durable rule

**ARIA can change/expose semantics; JavaScript/CSS/HTML structure may still be required to implement behavior and state correctly.**

This is why ARIA is not a universal repair layer for non-semantic markup.

---

# 14. Hiding something has multiple meanings across the platform

## FOUNDATION

“Hidden” is ambiguous without naming the layer.

An element can be:
- absent from DOM;
- present but visually suppressed by CSS;
- not exposed to accessibility APIs;
- outside the viewport;
- covered by another element;
- inert/noninteractive;
- visually transparent while still interactive;
- removed only after a script action.

W3C accessibility rules demonstrate that mechanisms such as `display: none`, visibility and `aria-hidden` can affect programmatic exposure differently.

### Diagnostic rule

Never diagnose “the element is hidden” without asking:

**hidden from whom and in which representation?**

- visual user?
- keyboard navigation?
- screen reader/accessibility API?
- search/indexing system?
- JavaScript query?

---

# 15. Search engines and assistive technologies consume different projections of a web page

## SYNTHESIS

A public webpage may simultaneously have:
- HTTP response representation;
- HTML source;
- parsed DOM;
- styled/layout output;
- dynamically mutated DOM;
- accessibility API representation;
- crawler/rendered-search interpretation.

These projections overlap but are not identical.

### Web Manager implication

A page can look correct to a sighted user yet still fail because:
- headings/landmarks are semantically wrong;
- controls have no accessible names;
- script-generated content is unavailable at the relevant crawler/lifecycle moment;
- visual order conflicts with DOM/focus order;
- CSS suppresses content needed by users;
- source/metadata is incomplete even though runtime JavaScript fills the screen.

This is the conceptual bridge to later accessibility, SEO and rendering-architecture stages.

---

# 16. Progressive enhancement as an architectural idea

## SYNTHESIS

Progressive enhancement is best understood at Stage 1 as a resilience principle:

1. start with meaningful structure/content and native platform behavior where possible;
2. add presentation;
3. add richer script behavior without needlessly discarding the underlying semantics and core task path.

It is not an absolute requirement that every advanced web application function fully without JavaScript. Rather, it is a design lens for asking whether unnecessary dependency on one runtime layer makes content, navigation or critical actions more fragile than they need to be.

### MintTap relevance

For a company/app marketing/support site, much core information—product explanation, support links, privacy/legal content, store destinations—usually has strong value even before rich JavaScript behavior. That makes semantic document-first architecture particularly attractive unless product requirements show otherwise.

This is a provisional synthesis; actual rendering architecture remains an open project decision.

---

# 17. Failure diagnosis by layer

A strong Web Manager should avoid the phrase “frontend bug” when a more precise layer can be identified.

## Layer model

### A. Delivery/source problem
Symptoms:
- wrong/missing HTML/CSS/JS resource;
- wrong content type;
- stale asset;
- failed network request.

Evidence:
- Network panel / response source / status / cache.

### B. HTML parsing / DOM construction problem
Symptoms:
- unexpected nesting;
- missing/reparented nodes;
- malformed markup repaired differently than author expected.

Evidence:
- delivered source vs DOM inspector.

### C. CSS cascade/style problem
Symptoms:
- expected declaration not applied;
- unexpected inherited/default value.

Evidence:
- matched rules, cascade precedence, computed style.

### D. Layout/formatting problem
Symptoms:
- clipping, overflow, overlap, incorrect sizing/reflow.

Evidence:
- computed box dimensions, formatting context, constraints.

### E. JavaScript/runtime problem
Symptoms:
- content never inserted;
- state not updated;
- exception;
- lifecycle timing bug.

Evidence:
- console, breakpoints, runtime DOM/state, network/API response.

### F. Event/interaction problem
Symptoms:
- keyboard/click/focus behavior incorrect.

Evidence:
- event listeners/propagation, focus state, native behavior, overlay hit testing.

### G. Accessibility exposure problem
Symptoms:
- correct visual control but missing/wrong role/name/state;
- focusable item hidden from assistive technology;
- reading/navigation structure wrong.

Evidence:
- browser accessibility inspector plus keyboard/AT validation.

### Operational lesson

A screenshot tells you **what happened visually**, not **why**.

---

# 18. What should remain native vs custom

## SYNTHESIS

Native platform semantics offer accumulated browser behavior, compatibility and accessibility mappings. Custom components can be justified by product needs, but each replacement increases the implementation/validation surface.

For future MintTap projects, the Web Manager should ask before approving a custom control:

1. Is there a native HTML element that already expresses this semantic/task?
2. What native keyboard/focus/form/accessibility behavior would be lost?
3. Does custom styling materially require replacing the element, or can the native element be styled?
4. What browser/device/input tests become necessary?
5. Does the visual gain justify the interaction/accessibility/runtime cost?

This is a **handoff boundary** with Design Studio Web Design: Design Studio decides the interaction/visual solution; Web Manager should ensure the design brief includes the platform cost of overriding native behavior.

---

# 19. MintTap-specific application

No current `minttap.app` implementation stack is assumed.

For a future company/app website, the default Web Manager requirements emerging from this study are:

- critical public information should have meaningful HTML structure;
- visual styling should not be relied upon as the only carrier of document meaning;
- native links/buttons/forms should be preferred when they fit the task;
- DOM order, keyboard order and visual sequence should be reviewed when layout reorders content;
- JavaScript should enhance or implement required behavior deliberately, with loading/lifecycle effects understood;
- source/DOM/accessibility output should be independently inspectable during QA;
- browser DevTools should be used by layer: Network, Elements/DOM, Computed Styles, Console/Debugger and Accessibility views;
- framework abstractions must not replace understanding of the browser model beneath them.

## OPEN

Actual project decisions remain unknown until MintTap chooses:
- framework/build system;
- static/SSR/CSR/hybrid rendering strategy;
- component architecture;
- localization strategy implementation;
- analytics/third-party scripts;
- accessibility target/testing stack;
- supported browser/device matrix.

---

# 20. Design Studio dependency and handoff

## DEPENDENCY — current Design Studio state

`yhappcom/design-studio/progress/WEB_STATUS.md` currently places Web Design at **Stage 1 Foundation / not yet baselined** and explicitly expects frontend literacy in semantic HTML, CSS cascade, DOM/events/focus, accessibility implementation and browser behavior.

`research/web/README.md` confirms Web Design is design-led, with frontend technology serving implementation fidelity and validation rather than software-engineering study for its own sake.

## HANDOFF FROM THIS STUDY

Reusable findings that should inform future Design Studio Web work:

1. **Native semantic elements are not visually restrictive primitives; CSS can change appearance without discarding semantic/browser behavior.**
2. **DOM order, visual order and accessibility/focus order can diverge**, so responsive recomposition should be validated beyond screenshots.
3. **A custom widget inherits the burden of recreating native interaction/accessibility behavior.**
4. **Accessibility tree/API exposure is not a DOM clone**, so design QA needs accessibility inspection/AT testing in addition to DOM review.
5. **CSS cascade and layout are distinct failure layers**; design-to-code critique should identify which is actually failing.
6. **Script loading/runtime timing can change when content and interactions become available**, creating design/performance/accessibility consequences.

No Design Studio files are modified from this repository. These findings are recorded here as an outgoing handoff for later synchronization.

---

# 21. Common misconceptions corrected

1. **“HTML is what the browser displays.”** Incomplete. HTML is parsed into a DOM and then participates in styling/layout/runtime processing.
2. **“The DOM is the HTML source.”** False. The DOM is runtime document state and may differ due to parser recovery or JavaScript mutation.
3. **“CSS is just colors and spacing.”** False. CSS includes cascading/value resolution and multiple layout/formatting systems.
4. **“Specificity decides every CSS conflict.”** False. It is one dimension of the cascade.
5. **“JavaScript includes all browser APIs.”** False. ECMAScript defines the language; Web APIs come from browser/platform specifications.
6. **“A div styled as a button is a button.”** False semantically/behaviorally unless the required semantics and interaction behavior are recreated.
7. **“The accessibility tree is the DOM read aloud.”** False. Browsers map relevant semantics/state into platform accessibility APIs.
8. **“ARIA adds behavior.”** Generally false; ARIA communicates semantics/state but does not automatically recreate native interaction mechanics.
9. **“If it looks correct, accessibility is correct.”** False.
10. **“All frontend defects belong to one layer.”** False; source, parser, cascade, layout, runtime, event and accessibility exposure failures require different evidence.

---

# 22. Integrated competency check

Stage 1 competency for this domain is passed only if the Web Manager can explain and apply the following:

1. Why HTML, CSS and JavaScript evolved as distinct concerns.
2. How `text/html` is parsed conceptually into a DOM tree.
3. Why source HTML and runtime DOM can differ.
4. Why semantic meaning and visual appearance are independent dimensions.
5. What the CSS cascade does before layout and why specificity alone is not enough.
6. Why DOM structure and generated visual boxes/order need not match one-to-one.
7. Why ECMAScript and browser Web APIs are separate specifications/concepts.
8. How script loading/execution can affect parser timing.
9. How DOM events propagate conceptually.
10. Why native elements carry useful behavior beyond styling.
11. Why accessibility API exposure is not a raw DOM copy.
12. Why ARIA cannot be treated as a substitute for implementing widget behavior.
13. How to diagnose a defect by delivery, parser/DOM, CSS cascade, layout, JS runtime, event or accessibility layer.
14. Which findings belong to Web Manager vs Design Studio Web Design.

**Result: PASS for Stage 1 progression.**

This does not mean mastery of CSS layout, frontend frameworks, accessibility, performance or browser runtime. Those subjects are deliberately reopened in later stages.

---

# 23. Next prerequisite after this block

The remaining high-value Stage 1 domain is the **browser application/state/rendering architecture layer**:

- static vs dynamic sites;
- server-side rendering vs client-side rendering vs static generation at conceptual level;
- hydration and browser/application state basics;
- cookies vs Web Storage vs server session concepts;
- browser navigation/history;
- forms/basic input submission flow;
- CDN/edge/hosting/deployment vocabulary integration;
- full Stage 1 end-to-end competency review.

This should again be studied as a consolidated block rather than micro-reports.

---

# Sources

## Primary / authoritative

- WHATWG HTML Living Standard — Parsing HTML documents: https://html.spec.whatwg.org/multipage/parsing.html
- WHATWG HTML Living Standard — Scripting: https://html.spec.whatwg.org/multipage/scripting.html
- WHATWG DOM Living Standard: https://dom.spec.whatwg.org/
- TC39 ECMAScript specification: https://tc39.es/ecma262/
- W3C CSS Cascading and Inheritance: https://www.w3.org/TR/css-cascade-6/
- W3C CSS Display Module: https://www.w3.org/TR/css-display-3/
- W3C CSS Box Model: https://www.w3.org/TR/css-box-4/
- W3C Core Accessibility API Mappings: https://www.w3.org/TR/core-aam/
- W3C HTML Accessibility API Mappings: https://www.w3.org/TR/html-aam/
- W3C ARIA Authoring Practices — Structural Roles: https://www.w3.org/WAI/ARIA/apg/practices/structural-roles/
- W3C ARIA Authoring Practices — Names and Descriptions: https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/

## Historical primary/high-authority context

- W3C Web history: https://www.w3.org/about/history/
- W3C CSS1 Recommendation history: https://www.w3.org/press-releases/1996/css1-rec/
- W3C CSS history: https://www.w3.org/Style/CSS20/history.html
- Ecma ECMAScript history: https://ecma-international.org/news/ecma-262-the-ecmascript-javascript-the-most-popular-web-scripting-standard-is-celebrating-its-20th-birthday/

---

# Evidence classification

- `SOURCE` — WHATWG HTML/DOM, TC39 ECMAScript, W3C CSS, Core-AAM/HTML-AAM/APG establish parsing, runtime tree/event, language, cascade and accessibility-mapping concepts.
- `SYNTHESIS` — layered diagnostic model, progressive-enhancement framing, native-vs-custom cost model and cross-tree reasoning.
- `MINTTAP DIRECTION` — prefer semantic/native browser primitives for ordinary public-site tasks unless project evidence justifies custom replacements; validate source/DOM/style/runtime/accessibility layers separately.
- `OPEN` — actual MintTap framework, rendering architecture, supported browsers, component stack and accessibility testing stack.
- `DEPENDENCY` — Design Studio Web Design owns reusable web-design application/interaction judgment; Web Manager supplies platform constraints and project requirements.
- `VALIDATION` — real project QA must inspect actual browsers/devices and accessibility output; standards knowledge alone does not prove implementation quality.
- `CHANGE WATCH` — WHATWG Living Standards, ECMAScript live spec, evolving CSS modules and 2026 Core-AAM/HTML-AAM drafts must be rechecked when implementation depends on exact contemporary behavior.
