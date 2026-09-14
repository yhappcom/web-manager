# 037 — Stage 2 Page Systems, Content Hierarchy & Scan/Comprehension Architecture

Status: **STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT — COMPLETE**
Research date: 2026-09-15
Scope: `minttap.app` company/app/product/support/governance pages for an Apple/Android app company

## Why this study exists

Studies 034–036 established task-based information architecture, governed content objects, lifecycle/cross-channel truth, and navigation/findability. They answer **what information exists, who owns it, where it belongs, and how users can reach it**.

The unresolved prerequisite is what happens **after the correct destination loads**:

> How should a page organize its information so a user can rapidly confirm “this is the right place,” understand the important facts, distinguish conditions/evidence/actions, scan to the needed section, and recover when the desired content or service is unavailable?

This is still Stage 2 information architecture. It is not a visual-style study and does not attempt to replace Design Studio’s Web/Layout/Type ownership.

---

## RELATED DOMAIN CHECK

### Web Manager evidence reused

- 034: `audience/context → intent → task → destination → content object → owner → lifecycle`;
- 035: content object ≠ page ≠ component ≠ channel field; `claim → evidence → condition → action`;
- 036: navigation = orientation + movement; direct-entry and critical-destination findability contracts.

Deliberate repetition is limited to **transfer validation**: the prior models are now tested at the intra-page/page-type level rather than recreated.

### Design Studio evidence checked

Current Design Studio status (2026-09-15):
- Web Design is approved but still **Stage 1 Foundation / NOT YET BASELINED**; no substantive `W###` study exists yet.
- Web Design explicitly owns page hierarchy, content flow, scan paths, density, progressive disclosure, responsive composition and real-browser validation.
- Layout L002 provides a stronger general density model: information density, visual density, interaction density and navigation/temporal density are distinct; “more whitespace” and “sparser is always better” are rejected as universal rules.
- Type research treats typography as information architecture but still requires production web reflow/localization/enlarged-text validation.

Relevant Design Studio files checked:
- `AGENTS.md`;
- `progress/STATUS.md`;
- `progress/WEB_STATUS.md`;
- `progress/LAYOUT_STATUS.md`;
- `progress/TYPE_STATUS.md`;
- `research/web/README.md`;
- `research/layout/L002-whitespace-density-spatial-rhythm.md`.

### Boundary

Web Manager owns **page purpose, semantic information priority, required content slots, content/state contracts and page-type selection**.

Design Studio owns **visual composition, typography/color/layout expression, component form, responsive visual treatment and real-browser/device validation**.

This study therefore produces semantic page contracts, not fixed wireframes.

---

# 1. SOURCE — page structure must be available as structure, not only as appearance

WCAG 2.2 requires information and relationships conveyed through presentation to be programmatically determinable or available in text (SC 1.3.1), and meaningful reading sequence must be programmatically determinable when sequence affects meaning (SC 1.3.2). Headings and labels must describe topic or purpose (SC 2.4.6).

W3C WAI’s Page Structure Tutorial, updated 8 April 2026, explains that headings communicate content organization and can be used by browsers and assistive technologies for in-page navigation. WAI also recommends page regions and labels where needed so main content, navigation and complementary regions can be identified.

Primary/current sources checked 2026-09-15:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI Page Structure Tutorial: https://www.w3.org/WAI/tutorials/page-structure/
- WAI Headings: https://www.w3.org/WAI/tutorials/page-structure/headings/
- WAI Page Regions: https://www.w3.org/WAI/tutorials/page-structure/regions/
- WAI Labeling Regions: https://www.w3.org/WAI/tutorials/page-structure/labels/

### SYNTHESIS

A professional page has at least three concurrent hierarchies:

1. **semantic hierarchy** — what information depends on or qualifies other information;
2. **visual hierarchy** — what appears most/least prominent;
3. **interaction/navigation hierarchy** — what can be reached, expanded, acted on or skipped.

These hierarchies should reinforce one another but are not identical.

A large visual title does not create a semantic heading relation. A colored card does not prove the contained information is a distinct section. CSS reordering does not automatically change a meaningful DOM/assistive-technology reading sequence.

### MINTTAP DECISION

Every important page must remain intelligible as an outline of:

`page identity → purpose → sections → facts/conditions → actions`

before visual sophistication is considered.

---

# 2. SOURCE — page type should follow user context and task, not one universal template

Current U.S. Web Design System guidance distinguishes page types by user context:

- a **landing page** often receives users with little context and therefore needs to orient and contextualize;
- a **documentation page** often receives users after a landing page or search and can focus on specific detailed information;
- a **404 page** has a different anatomy: identify the error, explain likely cause where useful, provide recovery actions/support and avoid a dead end.

Current GOV.UK Design System similarly distinguishes task-specific page/pattern types such as start pages, confirmation pages, question pages, page-not-found pages, service-problem pages and service-unavailable pages.

Current sources checked 2026-09-15:
- USWDS Landing page: https://designsystem.digital.gov/templates/landing-page/
- USWDS Documentation page: https://designsystem.digital.gov/templates/documentation-page/
- USWDS 404 page: https://designsystem.digital.gov/templates/404-page/
- GOV.UK Design System Patterns: https://design-system.service.gov.uk/patterns/
- GOV.UK Start using a service: https://design-system.service.gov.uk/patterns/start-using-a-service/
- GOV.UK Page not found: https://design-system.service.gov.uk/patterns/page-not-found-pages/
- GOV.UK Service unavailable: https://design-system.service.gov.uk/patterns/service-unavailable-pages/
- GOV.UK Problem with the service: https://design-system.service.gov.uk/patterns/problem-with-the-service-pages/

### SYNTHESIS

“Consistent site design” must not mean “every URL has the same content anatomy.”

Consistency should preserve reusable orientation, semantics and interaction expectations while allowing page types to differ according to the task.

### PAGE-TYPE PRINCIPLE

Choose a page system by asking:

1. What context does the visitor already have?
2. What decision or task must the page support?
3. What information must be visible before that decision/action is safe?
4. What detail can follow after the user has oriented?
5. What is the failure/recovery path?

---

# 3. Page purpose is a contract, not an internal content category

A page may contain many content objects, but it should have a dominant reason to exist.

Define each page with:

- **primary audience/context**;
- **primary user task**;
- **page promise** — what the user should be able to learn/do here;
- **minimum evidence** needed before the user can act confidently;
- **primary action**, if one exists;
- **secondary/supporting actions**;
- **exit/recovery paths**;
- **source/owner/change trigger** from Studies 034–035.

### Failure mode — catalogue pages without a purpose

A page can be factually complete yet weak when it simply accumulates sections because the organization owns the information.

Examples:
- company homepage containing every app feature, legal notice, support topic and release history;
- app page repeating every store-listing sentence with no task prioritization;
- support article containing company background before the resolution steps.

### MINTTAP DECISION

The content inventory may be organization-centric; the rendered page should be task-centric.

---

# 4. A reusable semantic hierarchy: identity → orientation → decision information → action → depth

Not every page uses every layer, but this is the baseline reasoning model.

## Layer A — Identity

Answer immediately:
- what page/resource is this?
- which app/company/service does it concern?

Possible elements:
- document `<title>`;
- H1;
- app/section context;
- status qualifier when critical (`Beta`, `Retired`, `Known issue`).

## Layer B — Orientation / lead

Answer:
- am I in the right place?
- what can I accomplish here?

This should normally be concise. A lead is useful when the H1 alone does not sufficiently establish scope or purpose; it is not mandatory filler.

## Layer C — Decision-critical information

Information the user must understand **before** acting or relying on a claim.

Examples:
- platform/account/region availability;
- pricing/subscription condition;
- data/account implications;
- current known limitation;
- eligibility/prerequisite;
- support scope.

## Layer D — Evidence / explanation

Provide enough proof/detail for trust and comprehension:
- feature explanation;
- screenshot or behavior evidence;
- steps;
- examples;
- relevant policy explanation;
- troubleshooting rationale.

## Layer E — Action

The action should follow the information required to choose it safely.

Examples:
- App Store / Google Play destination;
- open support path;
- start deletion/account control;
- contact support;
- read full policy;
- continue to next resolution step.

## Layer F — Depth / related information

Secondary detail, related pages, technical notes, version history, citations or advanced troubleshooting.

### SYNTHESIS

This is not a requirement that all important buttons be physically near the top. It is a dependency rule:

> **Do not ask users to act before presenting the information materially required to understand the action.**

---

# 5. “Above the fold” is an unreliable architecture rule

There is no stable universal fold on the Web. Viewport size, browser chrome, dynamic toolbars, zoom, text enlargement, localization, font metrics, cookie banners and user settings all change what appears before scrolling.

W3C’s accessibility model reinforces that content must work under reflow and enlargement rather than rely on one fixed viewport composition. Design Studio L002 likewise treats density as task-dependent and warns against fixed-geometry assumptions.

### SYNTHESIS

The correct requirement is not:

`put everything important above the fold`

It is:

`make page identity, purpose and the next meaningful information/action discoverable without requiring the user to guess that useful content exists below`

### MINTTAP DECISION

For future MintTap pages, specify **priority and sequence**, not pixel-based fold guarantees.

Design Studio may visually arrange hero/content/action patterns differently as long as the semantic priority, discoverability and stress conditions survive.

---

# 6. SOURCE — headings are scan/navigation infrastructure

WAI states that headings communicate content organization and support in-page navigation. WCAG 2.2 Understanding 2.4.6 notes that descriptive headings help users predict what sections contain and help screen-reader users when headings are presented out of context or navigated directly.

GOV.UK’s current heading guidance separates semantic heading tags from visual style and recommends consistent page structure; changes made purely for visual balance require accessibility testing.

Current sources:
- WAI Headings: https://www.w3.org/WAI/tutorials/page-structure/headings/
- WCAG 2.2 Understanding 2.4.6: https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels
- GOV.UK Headings: https://design-system.service.gov.uk/styles/headings/

### HEADING TEST

Read only the H1/H2/H3 text in order.

A good outline should let a reader predict:
- page purpose;
- major questions/tasks;
- where a specific answer likely lives.

If the outline is `Overview / Details / More / Other / Learn more`, hierarchy exists visually but information scent is weak.

### MINTTAP DECISION

Do not use headings as decorative slogans when they are responsible for section navigation. Marketing voice is acceptable only when the heading still predicts the content.

---

# 7. Scan architecture: support selective reading without designing for superficiality

Users do not always read from the first word to the last. Task-oriented web content should permit selective retrieval.

Official GOV.UK content guidance requires published content to meet a valid user need, and its design system emphasizes task-focused start points and clear page patterns. U.S. government design guidance similarly differentiates introductory landing pages from focused documentation pages.

### SYNTHESIS — scan path is not one universal F/Z pattern

Do not turn popular eye-tracking diagrams into page templates.

A scan path depends on:
- user intent;
- whether the target is known;
- heading quality;
- repeated structure;
- localization/script;
- screen width and zoom;
- visual hierarchy;
- content familiarity;
- images/data/components;
- assistive-technology navigation.

Therefore the durable design target is **predictable retrieval structure**, not an assumed universal eye movement.

### INFORMATION-LEVEL SCAN TOOLS

Use, as appropriate:
- descriptive headings;
- front-loaded section leads;
- lists when items are genuinely parallel;
- steps when order matters;
- tables when comparison across shared attributes is the task;
- concise summaries for dense pages;
- in-page links/TOC when page length and retrieval tasks justify them;
- explicit conditions/status labels near affected information.

---

# 8. Content density: preserve task value, remove competition

Design Studio L002 establishes four distinct density dimensions:

1. information density;
2. visual density;
3. interaction density;
4. navigation/temporal density.

This distinction transfers directly to page architecture.

### Example

A support article with every step visible may have higher information density but lower temporal/navigation cost than an accordion that hides every step.

A comparison page can legitimately be denser than a first-visit landing page because simultaneous visibility has task value.

### MINTTAP DECISION

Web Manager should not prescribe “more whitespace” or “fewer cards.” Instead specify:
- what information must remain simultaneously comparable;
- what can be deferred;
- what must remain visible for safe action;
- what may become a secondary link or disclosure;
- what repetition can be eliminated because canonical content exists elsewhere.

Design Studio decides the spatial expression and validates it with real content.

---

# 9. SOURCE — progressive disclosure trades visibility for complexity; hidden content is not free

Current GOV.UK guidance is explicit:

- use **Details** for information only some users need; do not hide information most users need;
- use **Accordion** only when evidence shows users benefit from overview/show-hide behavior; hidden content may be missed;
- test content without an accordion first and consider simpler content, separate pages, headings or in-page links;
- **Tabs** are inappropriate when users need to read all information in order or compare across sections because switching creates memory/interaction cost.

Sources checked 2026-09-15:
- Details: https://design-system.service.gov.uk/components/details/
- Accordion: https://design-system.service.gov.uk/components/accordion/
- Tabs: https://design-system.service.gov.uk/components/tabs/

### SYNTHESIS

Progressive disclosure is a **cost exchange**:

`less simultaneous visual/information load ↔ more discovery, interaction, memory and state-management cost`

### DISCLOSURE TEST

Do not hide content merely because:
- the page looks long;
- the desktop mockup feels busy;
- a card grid is visually attractive;
- mobile has less space.

Hide/defer only when the user does not usually need simultaneous visibility and the additional interaction does not damage comparison, comprehension or recovery.

### MINTTAP DECISION

Critical feature conditions, account/privacy consequences, current service failures and required support steps must not be concealed solely to make a page visually cleaner.

---

# 10. Page-system contracts for MintTap

These are **semantic contracts**, not final templates.

## 10.1 Company / portfolio landing page

Primary job:
- identify the company/portfolio;
- explain what kind of products exist;
- route users to the correct app or company-level destination.

Required hierarchy:
1. company identity/purpose;
2. app portfolio or primary app entry points;
3. concise differentiation/context;
4. company-wide support/governance destinations where appropriate.

Avoid:
- deep feature documentation;
- duplicating each app’s entire detail page;
- turning every legal/support resource into equal hero-level content.

## 10.2 App detail / product page

Primary job:
- establish what the app does, who/what it is for and whether it fits the visitor’s need;
- support store conversion without overstating capability.

Required semantic slots:
1. app identity + canonical purpose;
2. availability/platform/current status;
3. highest-value verified capabilities/benefits;
4. material conditions/limitations near affected claims;
5. evidence or explanation;
6. store/download action where applicable;
7. support/privacy/account-control routes;
8. related deeper content.

Reuse Study 035’s `claim → evidence → condition → action` structure.

## 10.3 Support hub

Primary job:
- route a problem/task to the correct resolution object.

Required hierarchy:
1. app/support scope;
2. prominent common tasks/issues if evidence supports them;
3. browsable categories and/or search if content volume justifies it;
4. escalation/contact path;
5. service/known-issue status where materially relevant.

Do not create site search merely because support exists; expected content volume and retrieval evidence remain OPEN.

## 10.4 Support article

Primary job:
- resolve one task/problem.

Baseline:
1. problem/task-specific H1;
2. scope/prerequisites;
3. direct resolution or ordered steps;
4. branching conditions/exceptions;
5. expected outcome;
6. what to do if it fails;
7. escalation/related content;
8. updated/version applicability when needed.

Company narrative is secondary unless it materially changes resolution.

## 10.5 Privacy / policy page

Primary job:
- state governed facts clearly and make scope/version effective date unambiguous.

Baseline:
1. document identity and affected company/app scope;
2. effective/updated date where required/meaningful;
3. concise orientation/summary that does not replace the authoritative text;
4. clearly sectioned policy content;
5. contact/control mechanisms;
6. related account/data controls;
7. archive/supersession behavior where policy versioning requires it.

Do not optimize legal/governance pages for marketing conversion at the expense of precision.

## 10.6 Account-control/deletion page

Primary job:
- let a user understand and execute the control required by the product/store policy.

Baseline:
1. app/service identity;
2. who can use the control and prerequisites;
3. what will be deleted/retained and relevant consequences, based on verified policy/product facts;
4. action path;
5. confirmation/next step;
6. support/recovery if the control cannot be completed.

Actual requirements depend on the app’s account/data model and store policy; do not infer those facts generically.

## 10.7 Release / known-issue page

Primary job:
- communicate change/status without forcing users to reconstruct product truth from marketing copy.

Baseline:
1. app + release/issue identity;
2. date/version/status;
3. affected scope;
4. user-visible impact;
5. workaround/action where available;
6. resolution state/link;
7. canonical feature/support objects affected.

---

# 11. List, detail and comparison are different information structures

## List

Use when the task is to identify/select one or more objects from a set.

Every repeated item should expose the attributes required to distinguish and choose it. Do not fill repeated cards with the same generic copy/image; USWDS similarly warns repeated card content makes cards harder to distinguish.

## Detail

Use when the user has selected/arrived at one object and needs depth.

Contextual introduction can be shorter when the direct-entry identity remains clear.

## Comparison

Use when the task requires evaluating alternatives across shared attributes.

Do not split comparison-critical facts into tabs/accordions that force memory-based comparison.

### MINTTAP relevance

If MintTap eventually has multiple apps, “one card per app” is not automatically a sufficient portfolio design. The list must expose meaningful differentiators derived from verified product truth.

---

# 12. Empty, missing, error, unavailable and retired states are page anatomy

A complete page system includes non-ideal states.

## Distinguish the states

- **404 / missing** — requested resource does not exist at this URL;
- **unexpected service failure** — resource/service should work but currently fails;
- **planned unavailability** — service intentionally unavailable;
- **empty state** — valid page/context contains no objects/results yet;
- **unsupported condition** — requested platform/account/version/task is not supported;
- **retired/deprecated** — content/product existed but is no longer current;
- **no-result** — valid search/filter produced no matching items.

These require different explanations and recovery actions.

Current USWDS 404 guidance recommends identifying the error, giving recovery actions and avoiding a dead end. GOV.UK separately distinguishes page-not-found, service-problem and service-unavailable patterns and explicitly recommends telling users what happened and what they can do next.

### RECOVERY CONTRACT

For every non-happy state, answer where applicable:
1. what happened?
2. is the user’s data/action safe?
3. what can the user do now?
4. when should they retry?
5. is there an alternate route/support channel?
6. what status should HTTP/monitoring/search receive? (implementation depth reopens in later stages)

### MINTTAP DECISION

Do not use one generic “Something went wrong” component for all of these states.

---

# 13. Responsive page architecture preserves semantic priority, not desktop geometry

WAI page-structure guidance notes that responsive components may collapse/hide at smaller sizes but page structure should remain coherent. WCAG meaningful-sequence/reflow requirements and Design Studio L002/L003 evidence reject fixed desktop-position assumptions.

### SYNTHESIS

Responsive recomposition may change:
- columns → stack;
- sidebar TOC → compact in-page navigation;
- horizontal feature groups → vertical groups;
- media placement;
- component presentation.

But it should not casually change:
- which information is prerequisite to an action;
- heading relationships;
- meaningful reading order;
- app/page identity;
- claim conditions;
- recovery routes.

### ORDER CONTRACT

For each critical page, separately validate:
- DOM/semantic order;
- visual order at each layout;
- keyboard/focus order where interactive;
- screen-reader/landmark/heading traversal;
- action prerequisite order.

Do not assume CSS visual order proves the other four.

---

# 14. Korean/English localization is an architecture stress test

Design Studio Type/Layout evidence already shows mixed-script fallback and text growth can cross wrapping/reflow thresholds. Study 035 established localization as a dependency graph rather than independent truth.

### Page-level consequences

A semantic page contract must survive:
- longer/shorter headings;
- different line breaks;
- Korean/English punctuation/spacing conventions;
- longer button/link labels;
- translated support step expansion;
- policy/legal terminology growth;
- fallback font changes;
- 200% text enlargement and narrow width.

### MINTTAP DECISION

Do not shorten translated labels until they become ambiguous merely to preserve a design frame. Preserve meaning; redesign/recompose the frame.

Translation review should check both:
1. semantic fidelity to canonical content;
2. page hierarchy/comprehension under the rendered locale.

---

# 15. Page comprehension failure taxonomy

When a correct destination still performs poorly, classify the failure before redesigning.

## A. Identity failure
User cannot tell what page/app/context this is.

## B. Purpose failure
User cannot tell what the page enables them to learn/do.

## C. Priority failure
Secondary/promotional content competes with decision-critical information.

## D. Dependency failure
An action appears before prerequisites/conditions required to understand it.

## E. Hierarchy failure
Sections/relationships exist visually but not semantically, or vice versa.

## F. Label/heading failure
Section titles do not predict their contents.

## G. Density failure
Task-relevant information is lost in visual/interaction clutter, or useful simultaneous information is over-hidden.

## H. Disclosure failure
Critical or comparison-relevant content is hidden behind avoidable interaction.

## I. Sequence failure
Responsive/visual reordering changes meaningful reading or prerequisite sequence.

## J. State/recovery failure
Error/empty/retired/unsupported state does not explain what happened or next action.

## K. Localization failure
Translation/content growth destroys hierarchy or forces ambiguous shortening.

## L. Accessibility exposure failure
Visual organization is not available through headings/regions/meaningful sequence/focus structure.

---

# 16. Page Contract — reusable project specification

Before Design Studio creates final visual directions, Web Manager should be able to produce this for each critical page type.

| Field | Question |
|---|---|
| Page type | Landing, app detail, support hub/article, policy, account control, release, error/state, etc. |
| Primary audience/context | Who arrives and from where? |
| Primary task | What must they learn/do? |
| Direct-entry identity | Can a store/search/shared-link visitor orient without the homepage? |
| H1/page promise | What is this page? |
| Lead/orientation | What minimum context is needed? |
| Decision-critical facts | What must be known before action/reliance? |
| Conditions/limitations | Which claims/actions need qualification? |
| Evidence/depth | What proof/explanation is needed? |
| Primary action | What is the dominant next step, if any? |
| Secondary actions | What else is legitimate but lower priority? |
| In-page retrieval | Are headings/TOC/search/filter required? |
| Simultaneous comparison | Which information must remain visible together? |
| Disclosure allowance | What may be hidden/deferred and why? |
| Non-happy states | Empty/error/unavailable/unsupported/retired/no-result behavior |
| Recovery | What can the user do next? |
| Localization stress | Long KO/EN headings, labels, policy/support expansion |
| Accessibility structure | Heading outline, regions, meaningful order, landmark labels |
| Owner/source | Canonical objects and owner from 034–035 |
| Change triggers | Which release/policy/support changes force review? |
| Validation | Direct entry, narrow/reflow, 200% text, keyboard/AT where applicable |

### MINTTAP DECISION

This Page Contract is the preferred handoff unit to Design Studio. A wireframe may be produced later, but the page contract should exist first for critical surfaces.

---

# 17. Validation matrix

A page does not pass because a desktop mockup looks clear.

For each critical page, validate at least:

## Semantic outline
- `<title>` and H1 identify destination;
- headings alone form a meaningful outline;
- regions/labels distinguish repeated landmarks where needed.

## Comprehension
- first-time user can state page purpose;
- user can locate the major task/answer;
- material condition is found before the affected action;
- secondary material does not masquerade as primary.

## Retrieval
- known-item lookup via headings/in-page navigation works;
- direct-entry visitor can recover broader context;
- long pages provide sufficient internal wayfinding when justified.

## Disclosure
- required information is not hidden;
- comparison does not require unnecessary memory switching;
- disclosure state does not create a dead end.

## Responsive/localized stress
- narrow width;
- 200% text enlargement/reflow;
- long Korean and English strings;
- fallback/wrap changes;
- orientation after recomposition.

## Accessibility
- keyboard/focus order where relevant;
- heading/landmark navigation;
- meaningful sequence;
- action labels remain understandable out of visual context.

## Failure/recovery
- 404/error/unavailable/empty/retired/unsupported states are distinguishable;
- next action exists and is credible.

Reading/static inspection can establish a design hypothesis; real browser, assistive-technology and human-task evidence remains required before production confidence.

---

# 18. MintTap implications without inventing project facts

## Verified project-independent direction

A multi-app company under `minttap.app` should prepare reusable semantic contracts for:
- company/portfolio landing;
- app detail;
- support hub;
- support article;
- privacy/policy;
- account control where applicable;
- release/known issue;
- error/empty/unavailable/retired states.

## OPEN project facts

Do not finalize templates until the following are known:
- actual app inventory and launch priority;
- whether MintTap remains one app or becomes a portfolio at launch;
- verified primary audience/acquisition route;
- account/subscription/deletion behavior;
- support article volume;
- whether support search is justified;
- actual privacy/policy complexity;
- localization markets;
- current known-issue/release-note operating model;
- framework/runtime and actual browser/device targets;
- real human usability evidence.

---

# 19. DESIGN STUDIO DEPENDENCY / HANDOFF

No Design Studio canonical file is edited by Web Manager.

## Incoming evidence reused

### Layout/Interaction
- L002: density is multi-dimensional and task-dependent; progressive disclosure adds navigation/temporal cost.
- L003 and current Layout status: mixed-script/fallback can change wrap/reflow and responsive thresholds.

### Type
- typography acts as information architecture;
- actual production web/localization/enlarged-text validation remains open.

### Web Design
- no substantive W### evidence exists yet; Web Design is the intended integration/validation owner for these page contracts.

## Outgoing handoff to Web Design

When Web Design begins MintTap project work, provide:
1. Page Contract table for each critical page;
2. semantic priority and prerequisite/action relationships;
3. heading-outline requirements;
4. simultaneous-comparison requirements;
5. allowed/prohibited disclosure decisions;
6. direct-entry context requirement from Study 036;
7. non-happy-state taxonomy and recovery contract;
8. KO/EN long-content and 200% text stress cases;
9. DOM/visual/focus/AT order as separate validation dimensions;
10. explicit permission to change composition, but not silently change information priority or verified product truth.

## Handoff back expected from Design Studio

Return to Web Manager if visual exploration reveals:
- repeated content needed only to compensate for weak IA;
- impossible hierarchy under real text lengths;
- a page contract with too many competing primary tasks;
- disclosure required only because content is poorly modeled;
- localization/reflow that exposes ambiguous labels;
- component/state requirements missing from the content model.

Those are information-architecture/content-system problems, not styling defects.

---

# 20. Competency checkpoint

Before closing this block, Web Manager should be able to:

1. distinguish site IA from intra-page hierarchy;
2. choose different page systems according to user context/task;
3. explain why semantic, visual and interaction hierarchies are related but not identical;
4. define page purpose and decision-critical prerequisites before styling;
5. reject fixed “above the fold” architecture while preserving top-of-page orientation/discoverability;
6. use headings as retrieval/navigation infrastructure;
7. explain why there is no universal scan-path template;
8. distinguish information/visual/interaction/temporal density;
9. evaluate progressive disclosure as a trade, not a free simplification;
10. specify landing/detail/support/policy/account-control/release page contracts;
11. distinguish list/detail/comparison structures;
12. treat empty/error/unavailable/unsupported/retired states as distinct page anatomy;
13. preserve semantic priority across responsive recomposition;
14. use localization and 200% text as architecture stress tests;
15. hand Design Studio semantic constraints without dictating premature visual templates.

**Result: PASS at Stage 2 foundation/practitioner level.**

This is not a claim of production-ready MintTap page design. Real content, project facts, Web Design exploration, browser/AT tests and human usability evidence remain required.

---

## Highest-value next Stage 2 topic

Proceed to **Stage 2 Forms, Search/Support Retrieval & Content-State Anatomy** only if the curriculum still requires deeper common page mechanics before Stage 3; otherwise perform a Stage 2 integration gate first.

Recommended immediate next block:

**038 — Stage 2 Integration: Company/App/Support/Governance Page-System Matrix & Competency Review**

Reason:
- 034 established site/task/ownership architecture;
- 035 established canonical content/lifecycle;
- 036 established navigation/findability;
- 037 established page-system/comprehension architecture.

The next highest-value step is to prove these four models work together end-to-end before drifting into Stage 3 interaction design.

038 should synthesize, not re-teach, and should test realistic entry/task scenarios such as:
- store visitor → app page → support/privacy;
- search visitor → deep support article → app context/escalation;
- user → account-control destination;
- release/known-issue direct entry;
- retired/missing resource recovery;
- bilingual/reflow stress.

---

## Source register

### Primary / normative
- W3C WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C WAI Page Structure Tutorial — https://www.w3.org/WAI/tutorials/page-structure/
- W3C WAI Headings — https://www.w3.org/WAI/tutorials/page-structure/headings/
- W3C WAI Page Regions — https://www.w3.org/WAI/tutorials/page-structure/regions/
- W3C WAI Labeling Regions — https://www.w3.org/WAI/tutorials/page-structure/labels/
- W3C Understanding SC 2.4.6 — https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels

### Authoritative public design-system / service evidence
- USWDS Landing page — https://designsystem.digital.gov/templates/landing-page/
- USWDS Documentation page — https://designsystem.digital.gov/templates/documentation-page/
- USWDS 404 page — https://designsystem.digital.gov/templates/404-page/
- USWDS Card — https://designsystem.digital.gov/components/card/
- USWDS Summary Box — https://designsystem.digital.gov/components/summary-box/
- GOV.UK Design System Patterns — https://design-system.service.gov.uk/patterns/
- GOV.UK Start using a service — https://design-system.service.gov.uk/patterns/start-using-a-service/
- GOV.UK Headings — https://design-system.service.gov.uk/styles/headings/
- GOV.UK Details — https://design-system.service.gov.uk/components/details/
- GOV.UK Accordion — https://design-system.service.gov.uk/components/accordion/
- GOV.UK Tabs — https://design-system.service.gov.uk/components/tabs/
- GOV.UK Page not found — https://design-system.service.gov.uk/patterns/page-not-found-pages/
- GOV.UK Service unavailable — https://design-system.service.gov.uk/patterns/service-unavailable-pages/
- GOV.UK Problem with the service — https://design-system.service.gov.uk/patterns/problem-with-the-service-pages/

### Internal evidence reused
- Web Manager 034–036;
- Design Studio `progress/STATUS.md`, `WEB_STATUS.md`, `LAYOUT_STATUS.md`, `TYPE_STATUS.md`;
- Design Studio `research/web/README.md`;
- Design Studio `research/layout/L002-whitespace-density-spatial-rhythm.md`.

## Evidence classification

- `SOURCE`: explicit requirements/guidance from W3C/WAI and current public design-system documentation.
- `SYNTHESIS`: page hierarchy model, dependency sequencing, fold/scan-path conclusions, disclosure cost exchange, page failure taxonomy.
- `MINTTAP DECISION`: semantic Page Contract before visual template, verified-truth conditions near affected actions, explicit non-happy-state contracts, localization/reflow stress requirements.
- `OPEN`: actual MintTap app inventory, audiences, support volume, account/policy behavior, localization targets, production stack and human validation.
- `DEPENDENCY`: Design Studio Web/Layout/Type transfer and browser/device/AT/human validation.
- `VALIDATION`: real content + direct entry + narrow width + 200% text + localization + keyboard/AT + human task testing.
- `CHANGE WATCH`: WCAG/WAI guidance and public design-system patterns may evolve; recheck when translating these principles into a live production release.
