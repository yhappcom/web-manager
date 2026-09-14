# 035 — Stage 2 Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth

Status: **STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT — COMPLETE**
Research date: 2026-09-15
Scope: `minttap.app` company/app/product/support/governance content across web, Apple App Store and Google Play

## Why this study exists

Study 034 established that information architecture should be derived from audience/context, intent, task, destination, content object, owner and lifecycle. Earlier studies 004 and 010 already established a Product Truth Record, claim traceability, cross-store truth consistency and release synchronization.

The unresolved question is therefore not “what pages should MintTap have?” or “how should marketing copy sound?” It is:

> **How should MintTap model public information so that product, support and governance content can be reused, localized, reviewed, retired and synchronized without turning every page, store listing and translation into an independent source of truth?**

This study deliberately extends prior work rather than repeating it.

---

## RELATED DOMAIN CHECK

### Existing Web Manager evidence reused

- Study 003 — privacy/support/account-deletion architecture;
- Study 004 — Product Truth Record, three content layers, Screenshot Evidence Set and Content Release Manifest;
- Study 007 — localization architecture and stale-translation risk;
- Study 010 — marketing content model and Claim Registry;
- Study 011 — release/change-watch controls;
- Study 034 — task-based IA, page systems and content ownership.

### Design Studio status checked

Latest Design Studio global status says Web Design remains Stage 1 Foundation / not yet baselined. Its declared scope includes IA, page hierarchy, content flow, responsive composition, component/page systems, localization stress and browser/accessibility validation.

Relevant canonical files checked:
- `yhappcom/design-studio/progress/STATUS.md`;
- `yhappcom/design-studio/progress/WEB_STATUS.md`;
- `yhappcom/design-studio/research/web/README.md`.

### Boundary

Web Manager owns **content truth, information model, lifecycle, scope and publishing requirements**. Design Studio owns the visual/compositional expression and web-specific validation of that content system. A content model is not a wireframe, and a visual component is not a content source of truth.

---

# 1. SOURCE — store metadata is a public product contract, not disposable promotional copy

## Apple

Current App Store Connect references establish that:
- app name and subtitle are defined public app information;
- the version description describes app features/functionality;
- Support URL points to the support website;
- Privacy Policy URL is required for all apps;
- app privacy responses describe actual data practices and are reflected on the App Store product page.

Apple also distinguishes fields by editability/localization/version state.

Primary sources checked 2026-09-15:
- App information: https://developer.apple.com/help/app-store-connect/reference/app-information/app-information
- Platform version information: https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- App privacy: https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
- Manage app privacy: https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy

## Google Play

Current Play Console guidance establishes that:
- store listings contain app name, short description and full description;
- app metadata and screenshots must accurately reflect actual functionality;
- Data safety declarations are developer responsibility and must accurately represent app data behavior;
- account-creation apps must expose account/data deletion pathways under the User Data policy;
- Google can take enforcement action when app behavior and declarations disagree.

Primary sources checked 2026-09-15:
- Create and set up your app: https://support.google.com/googleplay/android-developer/answer/9859152
- Store listing best practices: https://support.google.com/googleplay/android-developer/answer/13393723
- Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- User Data policy: https://support.google.com/googleplay/android-developer/answer/10144311
- Account deletion requirements: https://support.google.com/googleplay/android-developer/answer/13327111
- Publishing guidance: https://support.google.com/googleplay/android-developer/answer/15191715

### SYNTHESIS

The website, App Store listing and Google Play listing are **separate publication surfaces with different field constraints**, but they refer to one underlying product reality.

Therefore MintTap needs:

`one product truth → multiple governed expressions`

not:

`website truth + App Store truth + Play Store truth + support truth`

Literal wording can differ. Material facts cannot.

---

# 2. SOURCE — content structure must remain understandable independently of styling

WCAG 2.2 requires programmatically determinable information/relationships, descriptive headings/labels, meaningful sequence, consistent navigation/identification and determinable page language. W3C WAI guidance further explains that headings communicate content organization and can support in-page navigation.

Primary sources:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI Headings tutorial: https://www.w3.org/WAI/tutorials/page-structure/headings/
- WCAG 2.2 G141: https://www.w3.org/WAI/WCAG22/Techniques/general/G141.html

### SYNTHESIS

Content hierarchy is not only a visual-design concern. If a page's logic exists only because one paragraph is larger, one card is colored, or one item is positioned higher on desktop, the information model is weak.

A content model should preserve relationships such as:
- app → feature;
- issue → resolution;
- policy → scope;
- claim → evidence;
- release → change;
- locale → translation state;
- account-control page → affected app;

before visual presentation is applied.

This makes the same information more robust under responsive recomposition, screen-reader navigation, search indexing, localization and future redesign.

---

# 3. FOUNDATIONAL MODEL — content object ≠ page ≠ component ≠ field

Four layers must be separated.

## Content object

A reusable unit of meaning with identity and lifecycle.

Examples:
- App;
- Product Claim;
- Feature;
- Support Topic;
- Support Article;
- Known Issue;
- Release Note;
- Policy Document;
- Account-Control Procedure;
- Store Destination;
- Screenshot Evidence Asset.

## Page

A user-facing composition that satisfies one or more tasks using content objects.

Example:
`/apps/minttap/` may compose App + current Feature objects + claims + store destinations + support entry points.

## Component

A presentation/interaction pattern used to display or manipulate content.

Example:
a feature card may render a Feature object, but the feature must not exist only as text embedded inside that card's code.

## Channel field

A platform-specific expression with its own limits/rules.

Examples:
- App Store subtitle;
- Google Play short description;
- HTML title;
- social preview description.

### MINTTAP DECISION

Do not make page-builder blocks or store metadata fields the canonical data model.

The canonical model should represent the durable meaning first. Page templates and channel fields consume that model.

---

# 4. MINTTAP CONTENT OBJECT MODEL

This is a reusable baseline, not a claim that every future app needs every object.

## A. App object

Minimum fields:
- stable internal ID;
- canonical public name;
- slug;
- app status: planned / beta / released / retired;
- supported platforms;
- bundle/package identifiers;
- one-sentence canonical purpose;
- target user/task summary;
- account requirement state;
- pricing/subscription state;
- supported locales;
- store destinations;
- support destination;
- privacy scope reference;
- deletion/control reference where applicable;
- Product Truth version/date;
- owning product/engineering confirmer.

## B. Feature object

Fields:
- feature ID;
- app relation;
- canonical factual capability statement;
- user value interpretation;
- availability state;
- platform/plan/region/account constraints;
- evidence source/build/version;
- screenshot/evidence references;
- first release / removal release;
- localization state;
- last verified date;
- review trigger.

### Why separate fact from benefit

“Exports XLSX files” and “Take your records into your existing spreadsheet workflow” are not the same statement.

The first is a product fact. The second is an interpretation of user value. Keeping them distinct allows copy to change without corrupting the factual product record.

## C. Product Claim object

Study 010's Claim Registry becomes a formal reusable object.

Fields:
- claim ID;
- related app/feature;
- claim class: product fact / value interpretation / quantified / comparative / security/privacy / testimonial;
- canonical proposition;
- evidence;
- permitted qualifiers;
- prohibited overstatement;
- target channels;
- current state: approved / needs evidence / expired / withdrawn;
- owner;
- verification date;
- expiration/review trigger.

## D. Support Topic object

A topic is a user problem/task grouping, not necessarily an article.

Fields:
- topic ID;
- app;
- user intent/task;
- audience/context;
- category;
- priority/severity;
- likely entry routes;
- escalation route;
- related articles;
- related known issues;
- keywords/synonyms;
- owner.

## E. Support Article object

Fields:
- article ID;
- app/scope;
- task/problem statement;
- prerequisites;
- supported app/platform/version range;
- resolution steps;
- expected result;
- failure branch / escalation path;
- related feature/release/known issue;
- screenshots/version evidence;
- reviewed-on date;
- review trigger;
- localization state;
- retired/replacement relationship.

### MINTTAP DECISION

A support article must declare **scope**. Generic “How to export” copy without saying which app/platform/version behavior it describes is fragile.

## F. Known Issue object

Fields:
- issue ID;
- affected app/version/platform;
- symptom;
- confirmed cause if known;
- workaround if validated;
- status;
- first observed/confirmed date;
- expected fix version if public and confirmed;
- support escalation notes;
- retirement trigger.

## G. Release Change object

Fields:
- app/version;
- release state/date;
- added/changed/removed behavior;
- affected Feature/Claim/Support objects;
- privacy/data impact;
- account/pricing impact;
- screenshot impact;
- localization impact;
- web/store update status.

This operationalizes Study 004's Content Release Manifest at content-object level.

## H. Governance/Policy object

Fields:
- document type: privacy / terms / account deletion / user privacy choices / other;
- legal/developer entity;
- app scope;
- jurisdiction/locale scope where applicable;
- effective date;
- published date;
- current version ID;
- supersedes/superseded-by;
- canonical URL;
- store dependencies;
- data-practice/account dependencies;
- owner/reviewer;
- next review/change trigger;
- localization relationship.

### Important

Version fields do not imply that MintTap should invent arbitrary legal-document versioning. The operational need is to know what is currently authoritative, when it became effective, which apps it applies to and what change invalidates it.

---

# 5. CONTENT HIERARCHY — claim → evidence → condition → action

For product communication, a robust hierarchy is:

1. **Claim** — what users can expect;
2. **Evidence** — screenshot, concrete capability, workflow or supported fact;
3. **Condition** — platform/account/plan/region/version limitation when material;
4. **Action** — install, learn, compare, get support, manage data, etc.

### Example structure

Weak:
> Powerful portfolio tracking for everyone.

Better model:
- claim: track supported portfolio activity;
- evidence: actual summary/history capability;
- condition: supported data/import/account scope;
- action: view app details / download.

Final copy must wait for actual app facts.

### SYNTHESIS

This structure reduces two common failures:
- persuasive copy becoming detached from evidence;
- important limitations being hidden far below the headline.

It also gives Design Studio a reliable semantic hierarchy to visualize without making visual prominence the sole carrier of meaning.

---

# 6. PAGE-TEMPLATE CONTENT CONTRACTS

Templates should define **required semantic slots**, not force every app into identical marketing prose.

## App overview contract

Typical required content:
- app identity;
- canonical purpose;
- primary user outcome/task;
- verified major capabilities;
- material constraints;
- supported platforms/store destinations;
- screenshots/evidence where available;
- support route;
- privacy/governance route.

Optional depending on product:
- pricing/subscription explanation;
- account requirement;
- changelog/release highlights;
- FAQ preview;
- testimonials/metrics only when evidenced.

## Support article contract

Required:
- task/problem title;
- app/platform scope;
- prerequisites when needed;
- ordered resolution/instruction;
- outcome;
- escalation/fallback when appropriate;
- freshness metadata internally.

## Governance page contract

Required internally:
- entity;
- app scope;
- effective/current state;
- canonical source;
- change owner;
- store dependencies.

User-visible fields depend on the actual legal/policy requirement; do not publish internal workflow metadata unless useful.

### MINTTAP DECISION

A content contract is a minimum semantic guarantee, not a universal visual layout.

Design Studio may compose the same contract differently across desktop/mobile or app contexts as long as hierarchy, completeness and findability survive.

---

# 7. CANONICAL TRUTH VS DELIBERATE DUPLICATION

## A frequent misconception

“Single source of truth” does **not** mean every sentence should appear only once on the public internet.

Users legitimately need overlapping information in:
- website product pages;
- App Store and Google Play listings;
- support pages;
- privacy/account-control pages;
- search/social metadata;
- release notes.

### SYNTHESIS — two different kinds of duplication

#### Governed duplication

Several surfaces express the same underlying fact through references to one canonical internal object.

Example:
- Product Truth says account required = false;
- website says “No account required”;
- store listing phrases the same fact within its own field constraints.

This is acceptable if both derive from the same current fact.

#### Ungoverned duplication

The same fact is manually copied into several places with no ownership or dependency relation.

This creates drift.

### MINTTAP DECISION

The target is not “no duplication.” It is **no independent truth duplication**.

---

# 8. SEARCH CANONICALIZATION IS NOT CONTENT-GOVERNANCE CANONICALIZATION

Google Search defines canonicalization as selecting a representative URL among duplicate/similar URLs for search purposes.

Primary source:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization

### Important distinction

SEO `rel=canonical` does not solve:
- App Store vs website claim contradiction;
- stale Korean translation;
- obsolete support instructions;
- mismatched privacy disclosures;
- an old screenshot describing removed functionality.

Those are content-governance failures, not search duplicate-URL problems.

### MINTTAP DECISION

Use “canonical” with qualifiers:
- **canonical content truth** — internal authoritative fact/object;
- **canonical public URL** — primary public destination for an object;
- **search canonical URL** — URL selected/signaled for indexing/deduplication.

Never treat these as interchangeable.

---

# 9. CHANGE-TRIGGER MODEL

Calendar review alone is insufficient because many high-risk facts change immediately when the app changes.

Each object should declare event-driven triggers.

## Product release trigger

Review:
- feature objects;
- product claims;
- screenshots;
- app page;
- support articles;
- App Store/Play descriptions where affected;
- structured/search/social metadata where affected.

## Data-practice/privacy trigger

Review:
- privacy policy scope/content;
- Apple App Privacy responses;
- Google Data safety responses;
- User Privacy Choices/account-control surfaces;
- marketing privacy/security claims;
- support instructions involving personal data.

## Account/authentication trigger

Review:
- “no account required” or login claims;
- support onboarding/recovery articles;
- privacy/data deletion paths;
- Google Play account-deletion requirements if account creation exists;
- store screenshots/descriptions.

## Pricing/subscription/IAP trigger

Review:
- website pricing claims;
- feature availability/plan qualifiers;
- store descriptions/screenshots where relevant;
- support billing/cancellation guidance.

## Platform/OS/device support trigger

Review:
- platform availability claims;
- download CTAs;
- compatibility/support articles;
- screenshots/device framing.

## Support-process trigger

Review:
- escalation path;
- contact details;
- response expectation wording;
- App Store Support URL target;
- repeated help mechanisms.

## Rename/rebrand trigger

Review:
- app/company identity object;
- URLs/slugs/redirects;
- stores;
- privacy/governance references;
- support articles;
- screenshots/assets;
- metadata/social/search.

### SYNTHESIS

A content item is “fresh” when its dependencies remain true, not merely when its review date is recent.

---

# 10. LOCALIZATION IS A DEPENDENCY GRAPH, NOT A COPY-PASTE TASK

Apple and Google both support localized store information. The website will also need locale-specific content when MintTap targets multiple languages.

### MINTTAP DECISION

Every localized content object should carry at least:
- source-locale object/version;
- target locale;
- translation state: draft / reviewed / published / stale;
- translator/reviewer ownership where operationally relevant;
- last source revision translated;
- locale-specific legal/product divergence if intentionally approved.

### Staleness rule

If the source object changes materially, translations become **needs-review/stale** until confirmed, even if the translated text still appears linguistically correct.

### Example

English support article says:
“Export → XLSX and CSV.”

A release removes CSV.

Updating only the English sentence while leaving Korean unchanged is not simply a translation defect. It is a dependency/lifecycle failure.

---

# 11. CONTENT RETIREMENT AND URL LIFECYCLE

Deleting text is not sufficient when an object has external links or search/store dependencies.

Every retired public object should answer:
- Is the content obsolete or replaced?
- Is there a successor object/page?
- Must the old URL redirect?
- Is keeping the historical content useful?
- Does an App Store/Google Play field still point to it?
- Are internal links/search indexes/sitemaps affected?
- Are localized versions also retired?

### MINTTAP DECISION

Never retire a Support URL, Privacy URL, account-deletion URL or other store-linked public resource solely from the CMS side. First confirm and update all external dependencies.

---

# 12. SUPPORT CONTENT IS A RESOLUTION SYSTEM, NOT AN FAQ COLLECTION

Generic FAQs tend to organize information around what the publisher remembers to write rather than what users are trying to accomplish.

### Better support model

`user task/problem → scope → resolution → failure branch → escalation → related issue/release`

### Failure modes

- dozens of unrelated questions on one long FAQ page;
- no app/platform/version scope;
- instructions based on old UI;
- no escalation when steps fail;
- duplicated articles with contradictory instructions;
- search labels that use internal engineering terminology rather than user vocabulary;
- store Support URL landing on a generic company homepage.

### MINTTAP DIRECTION

Support taxonomy should derive from user tasks and product concepts, while Support Article objects remain independently addressable and maintainable where the task warrants it.

The real support architecture cannot be finalized until MintTap's support operating model and app inventory are known.

---

# 13. GOVERNANCE CONTENT NEEDS STRONGER CONTROL THAN MARKETING COPY

Governance surfaces include privacy, user-data/account controls and other policy/legal information.

### SOURCE

Apple requires a Privacy Policy URL for all apps and exposes app-privacy information based on developer declarations.

Google makes developers responsible for accurate Data safety declarations and can enforce discrepancies between app behavior and declarations.

Google's account-deletion policy requires applicable web deletion resources to be functional, relevant in scope and capable of supporting a deletion request.

### SYNTHESIS

Governance content has a tighter correctness requirement than ordinary promotional copy because:
- stores may depend on the URL;
- users may depend on it to exercise data/account rights;
- inaccurate content can conflict with platform declarations;
- stale scope can affect several apps at once.

### MINTTAP DECISION

Governance pages must never be “set and forget.” Their lifecycle is bound to:
- actual data practices;
- account/authentication model;
- app inventory/scope;
- developer/legal entity;
- store declarations;
- jurisdictional triggers handled in later legal work.

No specific legal conclusion is made in this study.

---

# 14. PRODUCT / STORE / SUPPORT CONSISTENCY MATRIX

For each material fact, MintTap should be able to inspect a row like:

| Truth object | Website | Apple | Google Play | Support | Governance | Trigger |
| --- | --- | --- | --- | --- | --- | --- |
| app name | app page | name | app name | article scope | policy scope | rename |
| account required | product copy | description/privacy if relevant | description/Data safety if relevant | onboarding/recovery | deletion/privacy | auth change |
| feature availability | product/feature | description/screenshots | description/screenshots | instructions | usually n/a | release |
| data collection | careful factual claims | App Privacy | Data safety | relevant help | privacy policy | SDK/data change |
| account deletion | control link | privacy choices if used | deletion web link if applicable | help article | deletion/privacy | account model |

The exact surfaces vary by app. The matrix exists to expose dependencies, not force irrelevant duplication.

---

# 15. FAILURE TAXONOMY

Content problems should be diagnosed precisely.

## Truth failure
A public statement is factually wrong.

## Scope failure
The statement may be true for one app/platform/version but is presented universally.

## Evidence failure
A claim cannot be substantiated.

## Synchronization failure
Two channels describe contradictory current states.

## Localization failure
A translation no longer matches the source/product state.

## Ownership failure
No person/process is responsible for reviewing an object.

## Trigger failure
The product changed but no content review was initiated.

## Hierarchy failure
Correct information exists but relationships/priorities are unclear.

## Findability failure
The destination exists but users cannot reasonably locate it from relevant entry points.

## Retirement failure
Old public content remains linked/indexed and conflicts with current behavior.

## Presentation masquerading as content structure
Meaning depends only on visual styling/position rather than semantic/document structure.

This taxonomy should be used during future content QA and incident diagnosis.

---

# 16. DESIGN STUDIO HANDOFF

No Design Studio canonical file was edited.

For future Web Design work, Web Manager should hand off **content contracts rather than finished visual hierarchy**.

Minimum outgoing package:
1. task/destination matrix from Study 034;
2. App/Feature/Claim/Support/Policy object relationships;
3. required vs optional page-template content slots;
4. claim → evidence → condition → action hierarchy;
5. direct external-entry requirements from stores/search/deep links;
6. long/localized content and stale-translation test cases;
7. content states: current / unavailable / deprecated / known issue / error / empty;
8. mobile/zoom/keyboard/screen-reader requirement that semantic hierarchy survive visual recomposition.

### Design Studio validation questions

- Can users still understand the claim and its condition when the layout collapses to one column?
- Does evidence remain associated with the correct claim under responsive rearrangement?
- Can long Korean/English labels and headings reflow without changing semantic order?
- Are support escalation and governance controls discoverable without making the visual system noisy?
- Are app-specific contexts visually distinct enough to prevent users from applying one app's instructions/policy to another?
- Does the page still communicate hierarchy when color, imagery or large-screen spatial grouping are removed?

### Return path

If real Web Design work shows that the content model creates excessive repetition, ambiguous grouping, impossible responsive ordering or weak user vocabulary, return that evidence to Web Manager. Do not solve structural content defects solely with decoration or layout tricks.

---

# 17. OPEN MINTTAP FACTS

Still unknown and must not be invented:
- actual current app inventory and release states;
- actual feature set for each app;
- pricing/subscription/account models;
- current Apple/Google listing values and URLs;
- support taxonomy and escalation process;
- data practices and policy scope per app;
- target locales and translation workflow;
- named content owners/approvers;
- chosen CMS/framework/content-storage mechanism.

These block production content, but they do not block establishing the operating model.

---

# 18. VALIDATION REQUIREMENTS FOR A REAL MINTTAP PROJECT

Before a content system is production-ready:

1. instantiate the model for at least one real MintTap app;
2. map each high-risk claim to evidence;
3. map current App Store/Google Play fields to the same truth objects;
4. validate Support/Privacy/deletion URLs from external entry points;
5. simulate one feature removal and verify all dependent content is discovered;
6. simulate a data-practice change and verify privacy/store declarations enter the review queue;
7. change source-locale content and confirm translations become stale/needs-review;
8. retire one support article and test replacement/redirect/external dependencies;
9. render key pages with CSS disabled/zoomed/narrow viewport to verify semantic hierarchy is not styling-only;
10. run Design Studio responsive/accessibility/content-density validation once Web Design baseline exists.

---

# 19. COMPETENCY CHECKPOINT

This block is retained only if the Web Manager can now:

1. distinguish content object, page, component and channel field;
2. explain why single-source truth does not mean zero public duplication;
3. distinguish content canonicalization from SEO URL canonicalization;
4. model app, feature, claim, support and policy content with scope/lifecycle;
5. identify event-driven content change triggers;
6. explain how localization creates dependency and staleness risk;
7. diagnose truth, scope, evidence, synchronization, hierarchy, ownership and retirement failures separately;
8. produce a Design Studio content contract without dictating premature visual layout;
9. connect Apple/Google store declarations to website/support/governance lifecycle;
10. refuse to invent real MintTap content before product facts are available.

**Result: PASS at Stage 2 foundation/practitioner level.**

---

# 20. HIGHEST-VALUE NEXT TOPIC

The next unresolved prerequisite is not another content-object taxonomy. It is **navigation, wayfinding and findability as an operational system**.

Study next as one integrated Stage 2 block:
- global vs local/context navigation;
- destination labels and information scent;
- current-location/orientation mechanisms;
- breadcrumbs and hierarchy;
- search vs browse vs direct-deep-link entry;
- footer/support/governance discovery;
- mobile navigation recomposition;
- keyboard/zoom/screen-reader and localization stress;
- external entry from Apple/Google/Search;
- failure modes where content exists but cannot be found;
- Design Studio cross-validation boundary.

This advances Stage 2 without prematurely entering Stage 3 interaction design.

---

## Evidence classification summary

- `SOURCE` — Apple/Google public metadata, privacy/data-safety/account-deletion requirements; W3C WCAG/page-structure guidance; Google Search canonicalization documentation.
- `SYNTHESIS` — content-object/page/component/channel separation; governed duplication; event-driven freshness; dependency graph model; failure taxonomy.
- `MINTTAP DECISION/DIRECTION` — canonical product truth feeding governed channel expressions; baseline content objects; page content contracts; lifecycle and translation-state rules; Design Studio handoff package.
- `OPEN` — actual MintTap product, account, pricing, data, locale, support and ownership facts.
- `DEPENDENCY` — future Design Studio Web validation; actual product/engineering/privacy/support facts.
- `VALIDATION` — instantiate model on a real app and perform change/retirement/localization simulations.
- `CHANGE WATCH` — Apple App Store Connect field behavior/policy; Google Play User Data/Data safety/account-deletion/store-listing requirements; search presentation behavior.
