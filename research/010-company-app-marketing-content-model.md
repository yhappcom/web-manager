# 010 — Company / App Marketing Content Model

Status: **FOUNDATION STUDY / PRODUCTION CONTENT NOT YET VALIDATED**  
Research date: **2026-09-14**

## Question

How should `minttap.app` present MintTap and each app so users can quickly understand what is offered, why it matters, what evidence supports the claims, and how to download or get help—without overstating capabilities, fabricating proof, contradicting store listings, or letting campaign copy drift away from the real shipped product?

This study defines the content and evidence model for company/app marketing pages. It does not choose final visual design, final copy, or app-specific positioning because the exact app inventory and product facts remain incomplete.

---

## RELATED DOMAIN CHECK

### Existing Web Manager studies

- Study 002 established company → apps → app → support/control/governance information architecture.
- Study 004 established Product Truth Record, Screenshot Evidence Set, Content Release Manifest and the rule that store/web copy may differ in expression but not in underlying fact.
- Study 007 established locale-specific `/ko/` and `/en/` content architecture and translation staleness controls.
- Studies 008–009 established truthful search/social metadata, canonical discovery and social-preview constraints.

### Design Studio

The Web Design specialist owns complete page hierarchy, scan paths, responsive layouts, landing/marketing surfaces, component behavior and browser/device validation. Current Web Design status is still Foundation / not yet baselined, so this study may define MintTap content requirements but must not invent an unvalidated universal layout style.

Primary dependency:
- `yhappcom/design-studio/progress/WEB_STATUS.md`

Typography, Color and Layout/Interaction remain validation dependencies for real page hierarchy, readable evidence density, localized long text, CTA states and responsive composition.

---

## SOURCE — Apple prohibits misleading marketing inside and outside the App Store

Apple App Review Guideline 2.3 requires accurate metadata. Apple also states that marketing an app in a misleading way—for example promoting content/services the app does not actually offer or promoting a false price—whether within or outside the App Store can be grounds for removal or other enforcement.

Apple also requires descriptions/screenshots/previews to make additional purchases clear when featured content requires them.

Primary source:
- https://developer.apple.com/app-store/review/guidelines/

### MINTTAP DECISION

The website is not a policy-free marketing channel.

All factual product claims on `minttap.app` are governed by the same Product Truth Record used for store synchronization.

A web page may use different wording, emphasis and depth from an App Store listing, but it may not:
- describe an unshipped feature as currently available;
- imply a free capability is included when it requires purchase/subscription unless that condition is clear;
- advertise a false or stale price;
- imply platform/device support that is not actually shipped;
- imply account, privacy, offline, sync, export, security or localization behavior that the released app does not provide.

---

## SOURCE — Google requires metadata and visual assets to accurately describe the real app

Google Play's Deceptive Behavior / Misleading Claims policy requires accurate descriptions and images/video of app functionality and prohibits false or misleading claims in titles, descriptions, icons and screenshots.

Google's Metadata policy requires clear, well-written descriptions and prohibits misleading, irrelevant, excessive or inappropriate metadata. It also prohibits unauthenticated/anonymous testimonials and certain ranking, price and promotional claims in sensitive metadata fields.

Primary sources:
- https://support.google.com/googleplay/android-developer/answer/17006354
- https://support.google.com/googleplay/android-developer/answer/9898842
- https://support.google.com/googleplay/android-developer/answer/13393723

### SYNTHESIS

Even where a specific Google Play metadata restriction does not literally govern an independent website page, the underlying trust constraint transfers: users should not see a website promise that materially differs from the actual app experience they reach after install.

### MINTTAP DECISION

MintTap website marketing follows a stricter cross-channel truth rule rather than exploiting differences between store and web policies.

---

## SOURCE — screenshots and previews are evidence of user experience

Apple describes screenshots and app previews as a way to visually communicate the app's user experience. Apple asset guidance also warns against unverifiable awards/recognition, specific pricing/discounts/URLs in App Store assets and cross-platform marketplace references in those store assets.

Primary sources:
- https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots
- https://developer.apple.com/app-store/asset-best-practices/

### MINTTAP DECISION — screenshot role on the website

Website screenshots are treated as **evidence**, not decorative filler.

Each public screenshot/recording must trace to Screenshot Evidence Set fields such as:
- app;
- platform;
- app version/build where material;
- locale shown;
- feature shown;
- source capture date;
- whether content is live data, sample data or staged/demo data;
- approval state;
- replacement/staleness trigger.

Website mockups may frame or crop real screenshots for presentation, but they must not materially fabricate the product experience.

If a concept image or future feature is shown, it must be conspicuously labeled as concept/planned rather than visually presented as the current shipped app.

---

## SOURCE — official App Store badges are calls to action and must follow brand rules

Apple's Marketing Resources and Identity Guidelines define App Store badges as calls to action, provide localized official artwork, prohibit badge modification and require badges to remain subordinate to the main message rather than becoming dominant artwork.

Primary source:
- https://developer.apple.com/app-store/marketing/guidelines/

### MINTTAP DECISION — download CTA

For released iOS apps, use current official App Store badge artwork linked directly to the correct product page.

Do not recreate, recolor, distort or translate the badge independently.

For Android, use the current official Google Play badge/brand assets from Google's active brand resources at implementation time. Because Google brand resources can change, exact badge artwork/clear-space rules are a CHANGE WATCH item and must be revalidated before production.

Store badges are **destination controls**, not the page's primary value proposition.

The page should explain the app first; badges complete the action.

---

# MARKETING CONTENT MODEL

## Principle 1 — Product Truth is upstream; marketing is downstream

Marketing copy is not an independent factual database.

For every meaningful claim, the source chain should be:

**Product Truth / App Data Contract / approved evidence → claim → localized expression → page component → store/social derivatives**

Examples:

| Claim | Required upstream evidence |
| --- | --- |
| “Works offline” | Product Truth + engineering confirmation of actual offline scope |
| “Syncs across devices” | Product Truth + supported-device/account/sync constraints |
| “No account required” | current authentication/account behavior |
| “Export to Excel” | shipped export functionality and supported formats |
| “Available on iPhone and Android” | current live store availability per platform |
| “Supports Korean and English” | shipped UI locale support, not merely translated website/store copy |
| “Free” | real current acquisition/subscription/IAP state and qualifying limitations |
| “Private” / “secure” | defined technical/privacy claim with supportable meaning; avoid vague absolutes |

### BLOCKER

A material claim without an identified evidence source may not ship as factual marketing copy.

---

## Principle 2 — distinguish claim classes

Create a **Claim Registry** per app.

### A. Product fact
Objectively verifiable current behavior.

Examples:
- supported platforms;
- export format;
- account requirement;
- locale support;
- subscription availability.

Evidence: Product Truth / release build / store state.

### B. User-value interpretation
A reasonable description of why a factual capability matters.

Example:
- fact: transactions are categorized and summarized;
- interpretation: “See your portfolio activity in one place.”

Evidence: underlying feature plus actual user task.

These statements may be more editorial, but must not introduce unsupported capability.

### C. Quantified claim
Numbers, percentages, rankings, speed/time savings, scale, accuracy, user counts or performance comparisons.

Examples:
- “50% faster”;
- “used by 10,000 investors”;
- “#1 YieldMax tracker”;
- “99.9% accurate.”

Default state: **REQUIRES EVIDENCE**.

Record:
- metric definition;
- data source;
- sample/time period;
- owner;
- last verification date;
- expiration/review date.

If evidence is absent/stale, remove or qualify the claim.

### D. Testimonial / review claim
Quotation or summarized user endorsement.

Requires:
- identifiable permitted source/provenance;
- permission/usage basis when needed;
- accurate wording/context;
- date/current-product relevance;
- no anonymous/unattributed representation where prohibited by a target surface.

Do not invent composites or unattributed praise.

### E. Comparative claim
Comparison with another product, old workflow or alternative.

Requires an explicit comparison basis and current evidence.

Avoid “best”, “simplest”, “most accurate”, “only” or competitor-superiority claims without support.

### F. Future / roadmap claim
Not shipped.

Must be separated visually and linguistically from current functionality.

Use explicit states such as:
- planned;
- in development;
- beta;
- coming later;
only when internally authorized and reasonably current.

Roadmap statements need review dates because stale promises damage trust even when not technically false at publication time.

---

## Principle 3 — page order follows user questions, not internal feature taxonomy

A strong app page should answer in sequence:

1. **What is this?**
2. **Who is it for / what problem does it address?**
3. **What can I actually do with it now?**
4. **Can I see evidence of the real experience?**
5. **What constraints, cost or platform requirements matter?**
6. **Why should I trust this publisher/app?**
7. **Where do I download it?**
8. **Where do I get support, privacy information or account controls?**

This sequence is a content hierarchy, not a rigid visual template. Web Design determines the final composition and responsive presentation.

---

# APP PAGE CONTENT CONTRACT

## 1. Identity / hero

Required concepts:
- current app name;
- one concise value proposition grounded in current Product Truth;
- supported/live platform status;
- primary download CTA(s) only where actually available;
- one strong representative product visual when useful.

Avoid:
- multiple competing slogans;
- vague superlatives;
- giant store badges with no product explanation;
- “AI-powered”, “secure”, “smart”, “revolutionary” and similar labels unless they convey a specific verifiable user benefit.

### Hero copy test

A first-time visitor should be able to answer within the first meaningful viewport/content block:
- what category of product this is;
- the principal task/value;
- whether it is available for their relevant platform.

This is a validation target, not a claim that every design must literally fit all information above the fold.

---

## 2. Problem / user context

Explain the real task or friction the app addresses.

Preferred evidence:
- actual target-user workflow;
- support questions;
- product rationale;
- verified user research when available.

Do not manufacture pain points merely to create dramatic marketing copy.

---

## 3. Capability hierarchy

Do not dump every feature equally.

Group capabilities into:

### Primary capabilities
The few reasons the product exists.

### Supporting capabilities
Functions that make primary tasks easier/safer/more complete.

### Advanced / conditional capabilities
Features requiring a subscription, account, particular platform, import source, network state, permission or other condition.

The page must make material conditions visible near the relevant capability rather than hiding them in an FAQ when they change the meaning of the claim.

---

## 4. Evidence blocks

A claim may be supported by one or more evidence forms:
- real screenshot;
- short real workflow sequence;
- annotated screenshot that preserves underlying UI truth;
- factual capability list;
- public documentation/support article;
- verified metric with provenance;
- clearly sourced testimonial;
- security/privacy disclosure where relevant.

### Evidence proximity rule

High-risk or high-specificity claims should have nearby evidence or qualification rather than relying on a distant footer/legal page.

Examples:
- subscription-only feature → label the condition near feature/CTA;
- “offline” → describe what remains available offline if scope is partial;
- “automatic sync” → state account/network/device prerequisites if material.

---

## 5. Screenshots / visual storytelling

Recommended narrative logic:
- show the principal user task first;
- use later visuals for secondary/advanced tasks;
- avoid galleries where every image looks identical or has no explanatory context;
- localize screenshots only when that locale accurately represents either the app UI or clearly labeled localized explanatory framing;
- avoid obsolete UI after material redesigns.

### Screenshot freshness trigger

Re-review website screenshots when:
- major navigation changes;
- feature shown is removed/renamed;
- pricing/paywall behavior changes materially;
- app locale support changes;
- visual data disclosure becomes inaccurate;
- platform UI materially changes the represented experience.

---

## 6. Availability / price / purchase conditions

The website must not infer pricing from old store state.

When showing price-related information:
- identify whether download is free, paid or has IAP/subscription only from current store/product truth;
- avoid hard-coded regional prices unless there is a reliable localization/update process;
- disclose material subscription or purchase requirements near the relevant feature/CTA;
- link users to the store for final local price/availability where appropriate.

If no stable price-maintenance process exists, prefer language that accurately explains the commercial model without embedding fragile currency values.

---

## 7. Trust / publisher information

Trust must come from verifiable operational facts, not decorative trust badges.

Potential elements when real:
- clear publisher/company identity;
- support/contact route;
- privacy policy;
- account deletion/data controls where applicable;
- transparent platform availability;
- changelog/release recency when maintained;
- real security/privacy statements with defined meaning;
- official store links.

Do not create invented awards, certifications, “trusted by” logos or review-star graphics.

---

## 8. Download CTA

CTA hierarchy:
1. official App Store / Google Play destination for released app;
2. pre-order/waitlist only if genuinely applicable and clearly labeled;
3. unsupported platform should not display an active misleading download CTA.

Before publishing each store badge/link verify:
- correct app;
- correct market destination where applicable;
- app currently available;
- official current badge asset;
- localized badge where appropriate;
- accessible link name/alt/context;
- reasonable keyboard/focus behavior from Study 006.

---

## 9. Support / privacy / account controls

Every app page should expose direct routes to the relevant operational resources when applicable:
- Support;
- Privacy;
- Account deletion/data controls;
- Terms or subscription details where material.

These are part of product trust, not footer clutter.

---

# COMPANY HOME CONTENT CONTRACT

The company home should not repeat every app page.

Its primary jobs are:
1. identify MintTap as the publisher/company;
2. explain the portfolio-level purpose or area of work without falsely forcing unrelated apps into one slogan;
3. route users to current apps;
4. provide company-level support/privacy/contact identity;
5. establish trust through real products and operational transparency.

### MINTTAP DECISION

If MintTap's apps later span materially different categories, prefer a clear publisher/portfolio framing over an artificial single-product mission claim.

The exact company positioning is OPEN until the app portfolio and business strategy are confirmed.

---

# CLAIM REGISTRY

Each marketing-relevant claim should have fields such as:

- `claimId`
- app/company scope
- source statement / factual basis
- claim class (A–F above)
- approved Korean expression
- approved English expression
- evidence reference(s)
- platform/locale conditions
- commercial condition
- owner
- verifiedAt
- invalidation trigger
- expires/reviewBy where needed
- surfaces using the claim (web/store/social/etc.)
- current state: approved / needs evidence / stale / retired

Exact machine-readable format remains OPEN.

### Why this matters

The Claim Registry prevents:
- a marketing slogan surviving after a feature is removed;
- Korean and English pages making different promises;
- social graphics using obsolete performance numbers;
- website copy claiming a feature before store release;
- screenshots and text drifting apart.

---

# CONTENT RELEASE INTEGRATION

Extend the existing Content Release Manifest with marketing fields:

- product facts changed?;
- claims invalidated?;
- capability hierarchy changed?;
- screenshots stale?;
- CTA/store destination changed?;
- pricing/commercial model changed?;
- testimonial/metric review date reached?;
- Korean/English expression needs update?;
- title/meta/social preview impacted?;
- support/privacy links still correct?;
- roadmap statement still valid?;
- store badge/pre-order state changed?;
- page accessibility/reflow revalidation required after content growth?

---

# CONTENT RISK LEVELS

## Low risk
General factual descriptions that change rarely.

Example: “Available for iPhone.”

Still requires Product Truth but can use ordinary release review.

## Medium risk
Feature claims tied to evolving product behavior.

Example: “Import your flight records from PDF.”

Requires feature/version/source support confirmation.

## High risk
- price/payment claims;
- privacy/security claims;
- numerical performance/accuracy claims;
- user-count/ranking/award claims;
- competitor comparisons;
- health/financial/legal outcome implications;
- “automatic”, “real-time”, “unlimited”, “always”, “never” absolutes;
- roadmap/timing promises.

High-risk claims require explicit evidence, owner and review/expiry state before publication.

---

# LOCALIZATION RULES

Marketing localization is not literal word replacement.

Allowed:
- natural Korean/English phrasing;
- different sentence length/order;
- culturally natural CTA wording;
- localized explanatory emphasis.

Not allowed:
- stronger claim in one locale;
- omitting a material condition in one locale;
- translating “planned” into language that implies “available now”;
- showing Korean explanatory graphics that imply the app UI is Korean when it is not;
- localized numbers/awards/testimonials without equivalent provenance.

Study 007's Localization Manifest must carry Claim Registry revision dependencies.

---

# DESIGN STUDIO HANDOFFS

## Web Design

When real app content exists, Web Design should validate:
- hero comprehension and first scan path;
- capability grouping and progressive disclosure;
- screenshot/evidence composition;
- trust/support links as part of the page system;
- store badge hierarchy and responsive behavior;
- long Korean/English content under mobile widths;
- page performance impact of screenshot/video media;
- real browser/device behavior.

The Web Manager supplies truth/evidence/content hierarchy. Web Design determines the visual/page system.

## Typography / Type

Stress-test:
- Korean vs English hero/title length;
- long feature headings;
- comparison/qualification text;
- compact store CTA areas;
- mixed-script app/product names;
- screenshots with annotations.

## Layout / Interaction

Validate:
- CTA priority;
- feature/evidence grouping;
- mobile recomposition;
- carousel/gallery controls if used;
- disclosure visibility for purchase/platform limitations;
- navigation from marketing surface to support/privacy/account controls.

## Color

Validate:
- CTA/state hierarchy;
- screenshot framing vs content contrast;
- brand use without fake “trust badge” semantics;
- focus/hover/disabled store-destination states.

---

# VALIDATION PLAN

Before an app marketing page is considered production-ready:

## Truth audit
- every material claim mapped to Product Truth / approved evidence;
- no stale claim state;
- current platform/availability/pricing conditions;
- current screenshots;
- current support/privacy/account-control links.

## Cross-channel audit
Compare against:
- live app build;
- App Store listing;
- Google Play listing;
- current privacy/data disclosures;
- social preview;
- localized variants.

Differences in phrasing are acceptable; contradictions are not.

## User-comprehension test
With representative users or internal proxy testing when users are unavailable, verify whether a first-time visitor can correctly state:
- what the app does;
- who it is for;
- current main capabilities;
- relevant platform/price/account conditions;
- where to download;
- where to find support/privacy.

Record misunderstandings rather than judging success from aesthetic preference.

## Accessibility / responsive test
Retain Study 006 requirements after real marketing content and media are inserted:
- keyboard;
- visible focus;
- 320 CSS px-equivalent reflow;
- 200% text enlargement;
- meaningful image alt where appropriate;
- non-text content not required to understand essential claims when a text alternative is needed;
- reduced-motion behavior if promotional animation/video is used.

---

# RELEASE BLOCKERS

Do not publish / promote when any of the following are true:

- hero or feature copy claims an unshipped capability as current;
- screenshot materially fabricates/overstates the actual interface or capability;
- platform badge links to wrong/unavailable app;
- paid/subscription condition materially changes a promoted feature but is concealed;
- price claim is stale/false;
- app UI locale support is implied but not shipped;
- quantified claim has no evidence/provenance or is past review date;
- award/ranking/testimonial is invented, unverifiable or materially misleading;
- privacy/security promise conflicts with App Data Contract;
- future/roadmap item is presented as current;
- Korean and English variants make materially different promises;
- obsolete marketing survives after Product Truth invalidation;
- launch-critical support/privacy/account-control links are broken.

---

# CHANGE WATCH

Recheck periodically:
- Apple App Review metadata/marketing truth requirements;
- Apple App Store marketing/badge/asset guidelines;
- Google Play Deceptive Behavior / Metadata policy;
- Google Play badge/brand guidelines before production asset use;
- target store availability and purchase-model changes;
- social/marketing claims when product behavior changes.

Policy/brand asset rules are not timeless.

---

# OPEN ITEMS

- Exact MintTap app portfolio and product categories.
- Actual current app names, store IDs, platform availability and pricing models.
- Final company positioning / legal identity.
- Per-app primary audience and user problem evidence.
- Whether any legitimate quantified metrics/testimonials exist.
- Final screenshot capture and approval workflow.
- Final Google Play badge source/rules at implementation time.
- Exact Korean/English copy tone and source-authoring language.
- Whether product videos/interactive demos are useful for specific apps.
- Final Web Design page composition and visual hierarchy.
- Real user-comprehension validation.

---

## Foundation conclusion

MintTap marketing content should function as a **controlled presentation layer over verified product truth**, not as an independent creative facts layer.

The production model is:

**Product Truth + evidence → Claim Registry → localized page hierarchy → screenshots/proof → store CTA → support/privacy controls → release invalidation/revalidation.**

This allows the website to be persuasive without becoming unreliable: clarity and evidence carry the conversion burden, while unsupported superlatives, fabricated proof and stale feature claims are rejected.