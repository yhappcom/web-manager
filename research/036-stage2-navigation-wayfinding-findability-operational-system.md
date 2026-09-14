# 036 — Stage 2 Navigation, Wayfinding & Findability as an Operational System

Status: **STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT — PASS**  
Research date: 2026-09-15  
Curriculum: Stage 2 — Website Anatomy / Content / Information Architecture

## Why this block exists

Studies 034–035 established what MintTap public information should exist, how it is scoped, and how content truth/lifecycle should be governed. That is not sufficient.

A correct support article, privacy destination or app page can still fail if users:

- cannot predict where it lives;
- cannot distinguish one destination from another;
- do not know where they currently are;
- enter directly from App Store, Google Play or search and lose context;
- encounter a different navigation model at narrow width, zoom or localization;
- cannot traverse the structure with keyboard or assistive technology;
- receive a visually convincing but semantically incoherent navigation system.

This study therefore treats navigation as an **operational information-finding system**, not as a header component.

It deliberately does not repeat Study 034's task-based IA or Study 035's content-object model. Instead it asks:

> Given that the right content exists, how does a user reliably find, identify, orient within, enter, leave and return to it across real entry modes and accessibility conditions?

---

## 1. Core model: navigation has two jobs

### SOURCE

W3C's WCAG 2.2 guidance for Guideline 2.4 states that navigation has two main functions:

1. tell the user where they are;
2. enable the user to go somewhere else.

WCAG 2.2 then supports those functions through criteria including page titles, focus order, link purpose, multiple ways, headings/labels, location, consistent navigation and consistent identification.

### SYNTHESIS

For MintTap, a complete navigation system must therefore solve both:

`orientation + movement`

A system that provides many links but weak location cues is incomplete. A system that clearly identifies the current page but provides poor routes onward is also incomplete.

This yields a useful operational model:

`entry → identify destination → establish context → choose route → traverse → confirm arrival → recover/continue`

Each step can fail independently.

---

## 2. Navigation is not the sitemap

### FOUNDATION

Keep these layers separate:

- **content model** — what durable information objects exist;
- **IA / hierarchy** — how those objects are conceptually grouped and related;
- **URL space** — how public resources are addressed;
- **sitemap** — one representation of site resources/hierarchy;
- **global navigation** — repeated high-level destinations;
- **local/context navigation** — destinations relevant inside a section/app/task context;
- **utility navigation** — support, language, account or other cross-cutting utilities where appropriate;
- **footer navigation** — persistent secondary/recovery routes, not a dumping ground;
- **breadcrumbs** — hierarchical orientation/path affordance where hierarchy adds value;
- **search** — query-based retrieval;
- **direct/deep link** — entry that bypasses preceding navigation;
- **browser history** — user-agent navigation continuity;
- **in-page navigation** — movement within a long document.

### SYNTHESIS

The mistake `sitemap = navigation menu` forces the global menu to expose the whole content tree. That does not scale for a multi-app company.

Study 034's app-context boundary remains useful: global navigation can stay relatively stable while app-local/support-local navigation becomes deeper.

---

## 3. Findability is a system property, not a single menu property

### SOURCE

WCAG 2.2 SC 2.4.5 Multiple Ways requires more than one way to locate a page within a set of pages, except where the page is the result of or a step in a process. W3C guidance gives mechanisms such as navigation links, site map, table of contents and search.

W3C's current accessibility design guidance similarly recommends clear and consistent navigation, more than one method where appropriate, and orientation cues such as breadcrumbs and clear headings.

### SYNTHESIS

A resource's findability should be evaluated through all realistic paths, not by asking whether it appears in the header.

For a MintTap support article, relevant paths can include:

- app page → Support;
- support landing → topic → article;
- site search → article;
- search engine → article;
- App Store Support URL → support context;
- Google Play website/support route → support context;
- direct shared/bookmarked URL → article;
- related article → article;
- footer/help route → support.

A resource can be findable through some paths and effectively invisible through others.

### Operational concept — route redundancy without clutter

Multiple ways does not mean duplicating every link everywhere. It means providing distinct retrieval modes that match different user strategies:

- **browse** for users who know the category but not exact wording;
- **search** for users who can express a query;
- **direct entry** for store/search/shared URLs;
- **contextual links** when the next destination follows from the current task.

---

## 4. Labels are promises about destinations

### SOURCE

WCAG 2.2 SC 2.4.4 requires link purpose to be determinable from the link text or link text together with programmatically determined context. SC 2.4.6 requires headings and labels to describe topic or purpose. SC 3.2.4 requires components with the same functionality to be identified consistently across a set of pages.

### SYNTHESIS — information scent

For Web Manager purposes, **information scent** is the degree to which a navigation label and its surrounding context let a user predict that the destination is relevant before following it.

This is a synthesis/UX concept, not a separate WCAG requirement.

Good destination labels answer:

- What will I find there?
- Is it about this app or the company generally?
- Is it information, an action, support, or policy?
- Will selecting it navigate, download, open another site, or perform an action?

### Failure examples

Weak:
- `Learn More`
- `Resources`
- `Info`
- `More`

Potentially stronger when context requires distinction:
- `MintTap Support`
- `Privacy Policy`
- `Delete Account`
- `Release Notes`
- `CONY Data Guide`

This does **not** mean every link must be verbose. The correct label depends on surrounding programmatic context and repeated-system consistency.

### MintTap rule

Do not optimize labels for symmetry or shortness before destination predictability. If Korean/English labels have materially different lengths, design must absorb that rather than weakening meaning to fit a component.

---

## 5. Global navigation and local navigation solve different scopes

### FOUNDATION

**Global navigation** answers:

> What are the stable top-level areas of this company/site?

**Local/context navigation** answers:

> Within the current app, support area or information collection, what related destinations are available?

### SYNTHESIS

For an app company that can grow from one app to many, top-level navigation should not mechanically gain one new item for every app capability, support topic or policy object.

A scalable pattern is:

`stable global structure → app context → local task destinations`

Example conceptually:

`Apps → MintTap → Overview / Support / Privacy / Release information`

This is a structural model, not a final MintTap menu decision; actual app inventory remains unknown.

### Failure mode — context collapse

If a user enters `MintTap Support` and every next destination returns them to generic company-level navigation with no app context, the hierarchy exists in data but not in the user's experience.

---

## 6. Current location is a first-class requirement

### SOURCE

WCAG Guideline 2.4 explicitly treats orientation as part of navigability. SC 2.4.2 requires page titles describing topic or purpose. W3C guidance for page titles notes that titles help users identify and distinguish pages and can identify current location without requiring inspection of page content.

WCAG AAA SC 2.4.8 Location requires information about the user's location within a set of pages. While AAA is not automatically a MintTap conformance requirement, the orientation principle is operationally valuable.

W3C menu guidance recommends indicating the current item and documents `aria-current="page"` as one implementation mechanism.

### SYNTHESIS

Orientation can be supplied by several reinforcing cues:

- document title;
- page heading;
- current navigation state;
- breadcrumb when hierarchy is meaningful;
- app/section identity;
- URL;
- contextual heading/labeling;
- selected local-navigation state.

Do not rely on color alone or one visual underline as the only current-location signal.

### SPA relevance

From Stage 1, same-document navigation can change the view without loading a new document. W3C guidance for Page Titled explicitly notes that SPA views representing distinct topics should update the page title dynamically.

Therefore client routing must maintain orientation semantics, not merely replace screen pixels.

---

## 7. Breadcrumbs: hierarchy aid, not browser history

### SOURCE

W3C APG describes a breadcrumb trail as an ordered list of links to parent pages of the current page, helping users find their place in a website/application. It recommends a navigation landmark with a label and `aria-current="page"` for a linked current-page item.

Google Search Central states that breadcrumbs indicate a page's position in site hierarchy and recommends breadcrumbs representing a typical user path rather than simply mirroring URL structure. Google supports multiple breadcrumb trails when multiple meaningful paths exist.

As of Google Search Central's September 8, 2026 documentation, breadcrumb rich-result support continues on desktop. Google removed breadcrumb display from mobile search results beginning in January 2025, while continuing to support breadcrumb markup.

### FOUNDATION

Breadcrumbs answer:

> Where does this resource sit in a hierarchy, and how can I move upward?

They do **not** answer:

> What pages did I personally visit before this?

That latter function belongs to browser/session history.

### SYNTHESIS

A breadcrumb should not be generated by naively splitting `/apps/minttap/support/article-x` into path segments. It should represent meaningful user information structure.

For a flat site or a task whose parent hierarchy adds no useful orientation, breadcrumbs may add noise rather than value.

### CHANGE WATCH

Google's search-result breadcrumb presentation is product behavior and can change; structured-data support and visible SERP presentation must be rechecked during SEO implementation.

---

## 8. Direct entry changes the design problem

### FOUNDATION

Users do not necessarily begin at the home page.

They may arrive through:

- App Store;
- Google Play;
- Google Search or another search engine;
- shared link;
- email/support response;
- bookmark;
- QR/deep link;
- browser history.

Studies 034–035 already established store-linked URLs as external-entry contracts and app identity as a durable context boundary.

### SYNTHESIS

Every important destination should pass the **direct-entry test**:

> If this is the first MintTap page a user sees, can they identify the company/app, understand the page purpose, know whether it applies to them, and find the next relevant destination?

This is especially important for:

- support articles;
- privacy/policy resources;
- account-control pages;
- release/known-issue information;
- app-specific landing pages.

### Failure example

A support article titled only `Import problem` with no visible app identity, platform scope or route back to the relevant support collection may work when reached through an internal wizard but fail as a search-engine or App Store direct landing.

---

## 9. Search and browse are complementary, not substitutes

### FOUNDATION

Browse navigation exploits known categories and visible relationships. Search exploits query terms and indexing/retrieval.

### SYNTHESIS

Search cannot repair an incoherent IA by itself:

- users may not know the site's vocabulary;
- content may use different terminology than the query;
- search results can lose app/scope context;
- policy/control destinations should not depend on users guessing exact terms;
- empty/no-result/error states create additional recovery needs.

Conversely, browse-only support systems become inefficient as content grows.

### MintTap operational rule

Before adding site search, establish:

1. a coherent content taxonomy;
2. predictable destination labels;
3. app/platform scope metadata;
4. result title and excerpt rules;
5. no-result/recovery behavior;
6. analytics for query success/failure;
7. accessibility of search and results.

Search belongs to the findability system but its interaction mechanics are deferred to Stage 3/9 where appropriate.

---

## 10. Footer and utility navigation have specific jobs

### SYNTHESIS

The footer is useful for:

- persistent recovery routes;
- governance/legal destinations;
- company identity/contact context;
- secondary destinations inappropriate for primary navigation;
- language/region or support access where project requirements justify it.

It should not become a dumping ground for every page omitted from the header.

Utility navigation can hold recurrent cross-cutting functions such as support, language or account access when they exist, but the function and label should remain predictable.

### SOURCE CONNECTION

WCAG SC 3.2.3 requires repeated navigational mechanisms to occur in the same relative order across a set of pages unless changed by the user. SC 3.2.6 similarly requires repeated help mechanisms to maintain relative order.

Thus header/footer/help placement is not merely visual consistency; predictability has accessibility consequences.

---

## 11. Responsive navigation is recomposition, not arbitrary replacement

### SOURCE

W3C's current Menu Structure tutorial states that menu structure should remain consistent across screen sizes. Some items may be collapsed or moved into sub-navigation, but items that remain shown should keep the same order, wording and destination.

WCAG SC 1.4.10 Reflow requires content at the specified narrow equivalent viewport to remain available without loss of information/functionality, except content inherently requiring two-dimensional layout. SC 1.4.4 requires text to be resizable to 200% without loss of content/functionality.

### SYNTHESIS

Responsive navigation may change **presentation and disclosure**, but it should not silently change the site's information model.

Examples of legitimate recomposition:

- desktop horizontal global navigation → narrow-width disclosure control;
- persistent local side navigation → in-flow section navigation;
- visible secondary actions → clearly labeled overflow region.

Potential failure:

- desktop has `Apps / Support / Company`, while mobile replaces them with unrelated labels/order/destinations that users cannot map to the same system.

### Design constraint

Navigation must be tested with:

- narrow viewport;
- 200% text enlargement;
- WCAG reflow-equivalent narrow width;
- long Korean and English labels;
- system font/fallback changes;
- keyboard operation;
- screen reader landmarks and names.

This is a direct Design Studio dependency.

---

## 12. Keyboard/focus order is part of navigation coherence

### SOURCE

WCAG SC 2.4.3 requires focusable components to receive focus in an order that preserves meaning and operability. W3C clarifies that focus order does not have to match visual layout exactly, but it must remain logical and should reinforce the reading order implied by the visual presentation where practical.

W3C menu guidance also emphasizes mouse and keyboard operability for navigation menus.

### SYNTHESIS

A menu that looks correct but tabs in a surprising sequence is an IA/interaction handoff failure, not merely an implementation polish issue.

Responsive CSS reordering is especially risky when visual order diverges from DOM/focus order.

From Study 031, keep four orders distinct:

- content/DOM order;
- visual order;
- focus order;
- accessibility reading/exposure order.

Navigation quality must survive all four.

---

## 13. Landmarks make navigation regions programmatically identifiable

### SOURCE

W3C ARIA Authoring Practices identifies `navigation` landmarks as groups of links intended for website or page navigation and recommends native HTML `nav` for such regions. When multiple navigation landmarks exist, labels should distinguish them; identical navigation sets can use the same label.

W3C's region-labeling guidance gives examples such as labeling separate main navigation and sub-navigation regions.

### FOUNDATION

Multiple navigation systems on a page are legitimate:

- primary/site navigation;
- app-local navigation;
- breadcrumb navigation;
- in-page table of contents.

But they should not become an undifferentiated series of screen-reader announcements all called simply `navigation`.

### MintTap validation

For a future app support page, check whether a user traversing landmarks can distinguish:

- site-level navigation;
- app/support navigation;
- breadcrumb/in-page navigation where present;
- main content;
- footer/content info.

This is a semantic requirement separate from visual styling.

---

## 14. Navigation consistency does not mean global sameness

### SOURCE

WCAG SC 3.2.3 concerns navigation mechanisms repeated within a **set of web pages** and requires repeated mechanisms to remain in the same relative order. W3C explicitly notes that sub-navigation and functionally different page sets can exist.

### SYNTHESIS

MintTap should preserve consistency **within a coherent context**, not force every page to expose exactly the same navigation.

Examples:

- company marketing pages may share one global shell;
- support pages may add app/topic navigation;
- a focused account-deletion flow may legitimately reduce unrelated navigation if this is an intentionally distinct process;
- language versions can be structurally equivalent without requiring byte-identical labels.

The test is whether users can form and reuse a stable mental model, not whether every header has identical pixel geometry.

---

## 15. Navigation failure taxonomy

When users cannot find or correctly identify content, diagnose the failure rather than saying "navigation is confusing."

### A. Coverage failure
Required destination has no discoverable route.

### B. Label/scent failure
Route exists but its label does not predict the destination.

### C. Scope failure
User cannot tell whether destination applies to company, app, platform, account type or version.

### D. Placement failure
Destination is technically linked but located where users cannot reasonably predict it.

### E. Orientation failure
User cannot identify current page/section/app or parent context.

### F. Consistency failure
Same destination/function changes label, order or behavior across equivalent page contexts.

### G. External-entry failure
A deep-linked page assumes prior internal context that an external entrant does not have.

### H. Responsive recomposition failure
Narrow width/zoom hides, renames or breaks access to necessary destinations.

### I. Semantic/accessibility failure
Visual menu exists but landmarks, accessible names, current state, focus order or keyboard operation are defective.

### J. Search/retrieval failure
Content exists but site search/taxonomy/query vocabulary does not surface it.

### K. Recovery failure
No useful route from 404, no-results, deprecated content, stale link or unsupported task state.

### L. History/deep-link continuity failure
Browser Back, direct refresh or copied URL does not restore/identify the intended state.

This taxonomy extends Studies 034–035: correct content and correct ownership are necessary but do not prove findability.

---

## 16. Evaluation matrix for MintTap projects

For each critical destination, test at least:

| Dimension | Questions |
| --- | --- |
| Identity | Can the user tell what page/app/company this is? |
| Purpose | Does the title/heading describe the task/topic? |
| Entry | Does the page work when entered directly? |
| Global route | Is there an appropriate site-level path? |
| Local route | Is there an appropriate app/topic path? |
| Alternate route | Is another suitable findability mechanism available? |
| Label | Does link text predict the destination? |
| Current state | Is current location identified semantically and visually? |
| Parent/up route | Can users move to the meaningful parent/context? |
| Continuation | Is the likely next task/destination available? |
| Browser continuity | Do refresh, Back/Forward and copied URLs behave coherently? |
| Responsive | Does access survive narrow width/zoom/reflow? |
| Localization | Do Korean/English labels preserve meaning and fit? |
| Keyboard | Is traversal and disclosure operable in logical focus order? |
| Screen reader | Are navigation landmarks/names/current states distinguishable? |
| Lifecycle | Do deprecated/renamed/moved resources recover via redirects or guidance? |

This matrix is a Web Manager requirement set, not a final visual design.

---

## 17. MintTap provisional architecture implications

These are **SYNTHESIS / DIRECTION**, not finalized project IA because actual app inventory, audiences and launch priorities remain unknown.

1. Keep global navigation relatively stable as the app portfolio grows.
2. Treat each app as a durable context with app-local product/support/governance relationships.
3. Make Support, Privacy and any required account-control resource independently understandable on direct entry.
4. Do not require Home → App → Support traversal before a deep resource makes sense.
5. Use breadcrumbs where hierarchy materially improves orientation; do not mirror URL syntax mechanically.
6. Give critical user-control/support destinations more than one sensible retrieval route where appropriate.
7. Preserve labels/destinations across responsive recomposition even if the presentation changes.
8. Treat long Korean/English labels as input constraints, not exceptions to trim away.
9. Preserve browser-native Back/Forward and deep-link expectations established in Stage 1.
10. Separate semantic navigation requirements from final Design Studio visual composition.

---

## 18. Design Studio dependency and handoff

### RELATED DOMAIN CHECK

Latest Design Studio status checked 2026-09-15:

- global Design Studio remains ACTIVE;
- Web Design Specialist remains **Stage 1 Foundation / NOT YET BASELINED**;
- its explicit scope includes IA, navigation/wayfinding, responsive composition, content flow, accessibility and real-browser/device validation;
- Layout/Interaction evidence includes hierarchy, responsive transfer, navigation/state/feedback foundations but still has unresolved real-browser multilingual/enlarged-text and running keyboard/focus validation gaps.

### HANDOFF TO WEB DESIGN

When a real MintTap page system is designed, Web Manager should provide:

1. task/destination matrix from Study 034;
2. content-object/page contracts from Study 035;
3. critical destination findability matrix from this study;
4. global vs local/context navigation scope;
5. direct-entry scenarios from stores/search/shared links;
6. current-location requirements;
7. breadcrumb eligibility/hierarchy model;
8. long Korean/English labels;
9. narrow-width + 200% text + reflow stress conditions;
10. DOM/visual/focus/accessibility-order constraints;
11. multiple-navigation-landmark labeling requirements;
12. Back/Forward/deep-link continuity cases;
13. failure/recovery routes for deprecated, missing and no-result states.

### RETURN PATH FROM DESIGN STUDIO

Web Design should return evidence when:

- semantic label quality conflicts with available spatial budget;
- local/global navigation hierarchy becomes visually ambiguous;
- responsive recomposition breaks expected location or order;
- translated labels create component/system failures;
- focus/reading order diverges from visual hierarchy;
- actual browser/device testing reveals a structural issue.

Those findings should return to Web Manager as IA/content constraints rather than being hidden with styling.

No Design Studio canonical file is edited by this study.

---

## 19. What is SOURCE vs SYNTHESIS vs OPEN

### SOURCE — verified

- W3C WCAG 2.2 navigation/predictability requirements and current Understanding guidance.
- W3C WAI Menu Structure/Styling guidance for semantic structure, current item and responsive consistency.
- W3C APG breadcrumb/navigation-landmark patterns.
- Google Search Central breadcrumb guidance and current desktop/mobile search-result behavior.
- Study 034–035 prior verified store-linked external-entry and content-lifecycle requirements.

### SYNTHESIS — transferable professional judgment

- navigation as `orientation + movement`;
- entry→context→route→arrival→recovery lifecycle;
- information scent as destination predictability;
- route redundancy without link duplication everywhere;
- direct-entry test;
- global-stable/local-deep multi-app architecture;
- navigation failure taxonomy;
- critical-destination evaluation matrix;
- responsive navigation as information-model-preserving recomposition.

### OPEN — MintTap project facts not yet known

- exact app inventory and launch order;
- whether `minttap.app` launches with one app or portfolio navigation;
- actual support taxonomy and volume;
- whether site search is justified at launch;
- account creation/deletion flows;
- language/market launch scope;
- company/developer identity presentation;
- final global/local/footer/utility navigation labels;
- actual analytics evidence for navigation success;
- chosen web framework/component architecture.

### VALIDATION — required before production

- direct-entry tests for every store/search-linked destination;
- keyboard-only navigation and disclosure tests;
- screen-reader landmark/current-page checks;
- browser Back/Forward, refresh and copied deep-link tests;
- narrow mobile, 200% text resize and WCAG reflow-equivalent tests;
- Korean/English long-label stress;
- 404/deprecated/no-result recovery;
- real-user or task-based validation once audiences/tasks are known.

### CHANGE WATCH

- Google Search breadcrumb SERP presentation and structured-data behavior;
- WCAG/WAI explanatory guidance revisions;
- App Store / Google Play external-link and support/account requirements inherited from Studies 034–035.

---

## 20. Competency checkpoint

Stage 2 navigation/wayfinding foundation is retained only if Web Manager can explain and apply all of the following:

1. Why navigation is both orientation and movement.
2. Why sitemap, hierarchy, URL space and navigation are not the same artifact.
3. Why search, browse, direct entry and contextual links are complementary retrieval modes.
4. How label quality controls destination predictability.
5. Why global and local navigation require different scope.
6. How page titles, current state and breadcrumbs establish location.
7. Why breadcrumbs represent hierarchy rather than personal browser history.
8. How App Store/search direct entry changes page requirements.
9. Why responsive navigation may change presentation but should preserve the information model.
10. Why DOM/visual/focus/accessibility order must be validated separately.
11. How multiple navigation landmarks should remain distinguishable.
12. Why consistent navigation is contextual consistency, not universal sameness.
13. How to classify a findability failure before redesigning a menu.
14. How to hand semantic requirements to Design Studio without prematurely fixing visual form.

**Checkpoint result: PASS at Foundation/Practitioner level.**

This does not claim mastery of interaction pattern design, search UX, analytics or advanced accessibility. Those reopen in later stages.

---

## 21. Highest-value next Stage 2 block

With content existence, modeling and navigation/findability now established, the next unresolved prerequisite is **Page Systems, Content Hierarchy & Scan/Comprehension Architecture**.

The next integrated block should study:

- page purpose and primary task;
- page-title / heading / lead / evidence / action hierarchy;
- landing page vs detail page vs support article vs policy/control page;
- above-the-fold myths vs prioritization and scroll behavior;
- progressive disclosure at the information level;
- sectioning, headings and in-page navigation;
- content density and scan paths;
- comparison/list/detail structures where relevant;
- empty/error/deprecated states as part of page anatomy;
- mobile order/recomposition while preserving semantics;
- localization expansion and accessibility stress;
- Design Studio handoff as semantic page contracts rather than visual templates.

Do not drift into Stage 3 microinteraction or visual styling yet.

---

## Primary/current sources

1. W3C — Web Content Accessibility Guidelines (WCAG) 2.2  
   https://www.w3.org/TR/WCAG22/

2. W3C WAI — Understanding Guideline 2.4: Navigable, updated 2026  
   https://www.w3.org/WAI/WCAG22/Understanding/navigable

3. W3C WAI — Understanding SC 2.4.2 Page Titled  
   https://www.w3.org/WAI/WCAG22/Understanding/page-titled

4. W3C WAI — Understanding SC 2.4.3 Focus Order  
   https://www.w3.org/WAI/WCAG22/Understanding/focus-order

5. W3C WAI — Understanding SC 2.4.6 Headings and Labels  
   https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels

6. W3C WAI — Understanding SC 3.2.3 Consistent Navigation, updated 2026  
   https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation

7. W3C WAI — Understanding SC 3.2.4 Consistent Identification  
   https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification

8. W3C WAI — Understanding SC 3.2.6 Consistent Help  
   https://www.w3.org/WAI/WCAG22/Understanding/consistent-help

9. W3C WAI — Menu Structure, updated 2024  
   https://www.w3.org/WAI/tutorials/menus/structure/

10. W3C WAI — Menus Tutorial, updated 2026  
    https://www.w3.org/WAI/tutorials/menus/

11. W3C WAI ARIA APG — Breadcrumb Pattern  
    https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/

12. W3C WAI ARIA APG — Navigation Landmark Example  
    https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/examples/navigation.html

13. W3C WAI — Understanding SC 1.4.4 Resize Text  
    https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html

14. W3C WCAG 2.2 — SC 1.4.10 Reflow  
    https://www.w3.org/TR/WCAG22/#reflow

15. Google Search Central — Breadcrumb structured data, last updated 2026-09-08  
    https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

16. Google Search Central — Simplifying the visible URL element on mobile search results, 2025-01-23  
    https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs

## Internal dependencies

- `034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`
- `035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`
- `031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`
- `032-application-rendering-state-navigation-foundations.md`
- Design Studio `progress/STATUS.md`
- Design Studio `progress/WEB_STATUS.md`
