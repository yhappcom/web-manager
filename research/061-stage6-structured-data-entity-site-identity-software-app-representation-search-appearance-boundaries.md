# 061 — Stage 6: Structured Data, Entity/Site Identity, Software-App Representation & Search Appearance Boundaries

Date: 2026-09-16  
Status: **PASS — FOUNDATION/PRACTITIONER**

## Why this block now

059 established discovery/crawl/render/index/canonical mechanics. 060 established truthful page purpose, searcher intent, titles/snippets and internal linking. Structured data is therefore studied only after the underlying resource is discoverable and meaningful; markup must describe reality rather than manufacture it.

## Core model

`real entity/resource → truthful visible page → schema vocabulary/type/property → engine-supported interpretation/feature rules → syntax/policy validation → crawl/index observation → eligibility → engine selection/presentation → monitoring/lifecycle`

The key diagnostic separation is:

`schema-valid ≠ engine-supported ≠ feature-eligible ≠ feature-shown ≠ ranking guarantee`.

---

## 1. Vocabulary and search-feature support are different layers

### SOURCE
Schema.org is a shared vocabulary for describing entities, relationships and actions. It supports multiple encodings including JSON-LD, RDFa and Microdata. Its vocabulary is broader than any one search engine's supported search appearances.

Source: Schema.org, accessed 2026-09-16: https://schema.org/

Google describes structured data as a standardized format for providing information about a page and classifying page content, but individual Search features publish their own supported types, required/recommended properties and guidelines.

Source: Google Search Central, Software app structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/software-app

### SYNTHESIS
A property can be legitimate Schema.org vocabulary yet irrelevant to a particular Google rich-result feature. Conversely, passing a syntax validator does not establish content truth, policy compliance or display eligibility.

### MINTTAP DECISION
Maintain two explicit columns in any future markup inventory:
1. **semantic vocabulary purpose** — what entity/page fact the markup expresses;
2. **consumer/search-feature purpose** — which documented engine feature, if any, is expected to consume it.

Do not add properties merely because Schema.org permits them.

---

## 2. Structured data must describe the page/entity truth

### SOURCE
Google's structured-data feature documentation repeatedly requires Search Essentials and general structured-data guidelines. Feature guidance also warns that markup/content mismatch can invalidate eligibility and that policy/manual-action issues may exist even when syntax tests do not detect them.

Sources:
- Google Search Central, Organization structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/organization
- Google Search Central, Software app structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/software-app

### SYNTHESIS
Structured data is an explicit assertion layer, not a substitute content layer. A JSON-LD statement that claims an app price, rating, organization identity, platform or relationship that is absent, stale, unsupported or inconsistent with the authoritative product truth increases rather than reduces ambiguity.

### MINTTAP DECISION
Every production structured-data field needs a truth owner/source and lifecycle trigger. The markup must be generated from or checked against the same authoritative product/company data used by visible content where practical.

---

## 3. Organization identity: describe the company once, accurately

### SOURCE
Google recommends Organization markup on the home page or a single organization-describing page such as About; it need not be repeated on every page. Google recommends the most specific applicable Organization subtype and says there are no required Organization properties in this feature guidance; applicable recommended facts include name/alternateName, URL/logo and real-world/online presence information.

Source: Google Search Central, Organization structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/organization

Schema.org defines `Organization` as an organization such as a corporation, NGO, school or club and provides a broad property vocabulary.

Source: Schema.org Organization, accessed 2026-09-16: https://schema.org/Organization

### SYNTHESIS
Organization markup is most useful as a stable identity assertion, not as boilerplate copied independently into every template. Repetition from multiple independently maintained sources creates drift risk.

### OPEN
The actual legal/public organization name behind `minttap.app`, official logo URL, public contact data, legal address if publicly appropriate, and authoritative social/profile URLs have not been verified in this study. Do not invent them.

### MINTTAP DIRECTION
When production facts are available, maintain one canonical organization entity identifier (`@id`) and reuse that identifier when product/app entities need to reference the publisher/provider. Exact implementation awaits real site architecture.

---

## 4. SoftwareApplication is semantically relevant, but Google rich-result eligibility is narrower

### SOURCE
Schema.org defines `SoftwareApplication` as a software application and exposes properties such as `applicationCategory`, `operatingSystem`, `version` and others.

Source: Schema.org SoftwareApplication, accessed 2026-09-16: https://schema.org/SoftwareApplication

Google currently documents a SoftwareApplication Search feature. Its published required fields for rich-result eligibility include `name`, `offers.price`, and either `aggregateRating` or `review`; it recommends `applicationCategory` and `operatingSystem`. Google also supports `MobileApplication` and `WebApplication` subtypes in this context. Google explicitly states that structured-data features are not guaranteed to appear.

Source: Google Search Central, Software app structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/software-app

### SYNTHESIS
For a small app company, two goals must not be conflated:
- **semantic app identity**: accurately tell machines that a page is about a mobile/software application;
- **Google Software App rich-result eligibility**: satisfy Google's current feature-specific requirements.

A product page may have truthful SoftwareApplication markup yet not qualify for Google's Software App rich result, particularly when no eligible review/rating data exists. That is not a reason to fabricate ratings or reviews.

### MINTTAP DECISION
Never invent or self-manufacture aggregate ratings/reviews merely to satisfy feature requirements. If verified applicable rating/review evidence is unavailable, accept that Google Software App rich-result eligibility may not exist even if semantic markup is otherwise useful.

### OPEN
For each MintTap app, verify actual public app name, platform availability, store URLs, price model, operating-system requirements, category, publisher identity, current version strategy and whether any rating/review source is both truthful and compliant with Google's applicable review guidance before implementation.

---

## 5. App identity across website and stores is a graph, not a duplicated string

### SYNTHESIS
A mobile app company's identity graph can contain at least:
- company/organization;
- website/domain;
- individual app/product;
- iOS App Store listing;
- Google Play listing;
- support/privacy/governance resources.

These resources are related but not interchangeable. The company is not the app; the product page is not the store listing; an iOS instance and Android instance may represent the same product family while carrying platform-specific availability/version/store facts.

### MINTTAP DIRECTION
Future production modeling should establish stable identifiers and explicit relationships instead of stuffing all facts into one undifferentiated object. Product-specific markup belongs on the product's authoritative page. Organization identity should reference verified organization truth. Store URLs may be represented as relationships only after their exact official URLs are known.

### OPEN
Whether each MintTap product should be modeled as one cross-platform SoftwareApplication with platform/offer relationships or separate platform-specific MobileApplication nodes must be decided against the actual page/store architecture and consumer behavior; no generic pattern is promoted to production truth here.

---

## 6. Eligibility is not presentation, and presentation is not ranking

### SOURCE
Google's SoftwareApplication documentation explicitly says Google does not guarantee that features consuming structured data will show in results. It recommends Rich Results Test validation, deployment to a small number of pages, URL Inspection, and monitoring after indexing. Similar caveats recur throughout current structured-data documentation.

Source: Google Search Central, Software app structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/software-app

### SYNTHESIS
There are at least five distinct evidence states:
1. markup parses;
2. markup satisfies documented feature fields/guidelines;
3. Google crawls/indexes the intended page and sees the markup;
4. the page becomes eligible for an enhancement;
5. the enhancement is actually selected/shown for some searches.

None establishes a general ranking improvement.

### MINTTAP DECISION
Do not report “rich result implemented” when only validation passed. Report exact evidence: `syntax valid`, `feature eligible per test`, `Google observed`, `Search Console valid item`, or `observed search appearance`.

---

## 7. Validation must include semantics, not just validators

### SOURCE
Google's recommended deployment workflow includes adding required properties, following guidelines, validating with Rich Results Test, deploying a few pages, checking with URL Inspection, then allowing recrawl/reindexing. Google notes that syntax tools cannot identify every reason a result may be missing, including spammy content/markup usage.

Source: Google Search Central, Software app structured data, accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/software-app

### SYNTHESIS
A validator answers bounded questions about parseability/known feature requirements. Human review must still answer:
- Is this the correct entity?
- Is every asserted fact true and current?
- Does markup match visible/authoritative content?
- Is the marked page the right canonical resource?
- Are IDs/relationships stable?
- Are platform/store/product distinctions preserved?

### MINTTAP DECISION — Structured Data Evidence Contract
For every marked production page record:

| Field | Required evidence |
|---|---|
| URL/canonical resource | intended canonical + observed canonical |
| page/entity purpose | Company / Product / Support / other |
| entity type(s) | schema type and rationale |
| stable identifier | `@id` strategy if used |
| property | value + truth source/owner |
| visible-content relation | matching/supporting page evidence |
| engine feature target | documented feature or `semantic only` |
| required/recommended rules | dated engine documentation |
| syntax validation | validator/date/result |
| rendered/crawler visibility | URL Inspection/render evidence |
| Search Console state | valid/invalid/warning if report exists |
| observed appearance | query/date/device/locale if actually observed |
| lifecycle trigger | app release, price, logo, name, store URL, rating etc. |
| change watch | engine/schema policy requiring periodic review |

---

## 8. Breadcrumbs and other features remain page-purpose decisions

### SOURCE
Google documents BreadcrumbList as a way to express a page's position in site hierarchy and recommends breadcrumbs representing a typical user path rather than merely mirroring URL structure.

Source: Google Search Central, Breadcrumb structured data, updated 2026-09-08 / accessed 2026-09-16: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

### SYNTHESIS
Breadcrumb markup can reinforce IA already established by Stage 2/060, but markup cannot repair weak hierarchy or missing user-visible orientation. Similarly, the existence of a Schema.org type does not justify deploying every possible structured-data feature.

### MINTTAP DIRECTION
Select markup by real page/entity/task value. Likely candidates for later production evaluation are Organization, SoftwareApplication/MobileApplication and BreadcrumbList where the actual page architecture supports them. Other types remain opt-in only when matching content genuinely exists.

---

## Failure patterns

1. **Markup-first SEO** — creating schema before the page has stable identity/content.
2. **Schema.org = Google support** — assuming every valid type/property produces a Google feature.
3. **Validator = production proof** — stopping at Rich Results Test.
4. **Eligibility = display** — promising a rich result after satisfying requirements.
5. **Display = ranking** — treating enhanced presentation as a ranking guarantee.
6. **Rating fabrication** — creating unsupported ratings/reviews to satisfy SoftwareApplication requirements.
7. **Entity collapse** — treating organization, product, platform app and store listing as one thing.
8. **Stale assertions** — price/version/logo/store links drift while JSON-LD remains unchanged.
9. **Hidden truth divergence** — structured data says something the authoritative visible page does not support.
10. **Boilerplate identity drift** — organization markup duplicated independently across templates.

---

## Design Studio dependency / handoff

Latest `yhappcom/design-studio/progress/WEB_STATUS.md` checked 2026-09-16: Web Stage 1 PASS / Stage 2 PRACTICE NOT PASSED. W016 now provides actual Chromium native/custom control transfer 14/14. True HTTP direct-entry/reload/404, real Fetch/network integrated-state transfer, icon runtime, actual browser UI zoom and broader browser/device/AT/human evidence remain OPEN.

061 adds these implementation handoffs:
- **Web Design:** representative Company/Product routes should eventually expose structured data on the same canonical HTTP resources whose direct-entry/status/render behavior is validated; inspect final rendered DOM/source and crawler-visible JSON-LD rather than design mockups.
- **Layout/Interaction:** user-visible breadcrumb/orientation and machine BreadcrumbList must derive from the same intended IA; structured markup must not become a hidden substitute for deep-entry orientation.
- **Type:** organization/app names and visible page identity must remain legible and consistent with machine identity; typography does not determine schema but can reveal identity conflicts.
- **Color:** no new specialist dependency.

Web Manager retains entity/content truth ownership, type/feature applicability, source-of-truth mapping, search-engine validation/monitoring and change-watch responsibility. No Design Studio canonical file is edited.

---

## CHANGE WATCH

Search-engine supported structured-data types, required/recommended properties, feature availability and result presentation can change. Google Search Central documentation must be rechecked before implementation/release. Schema.org development vocabulary also evolves; semantic availability does not imply stable consumer support.

---

## Competency check

The Web Manager should now be able to explain and defend:
- why structured data follows rather than precedes crawlability and truthful page meaning;
- the difference between Schema.org vocabulary and Google-supported Search features;
- why syntactic validity, eligibility and actual display are separate states;
- why Organization and SoftwareApplication represent different entities;
- why app/store/platform identity requires explicit relationships rather than string duplication;
- why ratings must never be fabricated for feature eligibility;
- how to validate markup from truth source through crawler observation and Search Console rather than stopping at a validator.

**Result: PASS.**

## Highest-value next block

062 — **Localization & International Search: Language/Locale URLs, hreflang, Canonical Interaction, App-Store Locale Continuity & Multilingual Content Quality**.

Reason: after URL discovery, page meaning and explicit entity classification, a company serving Apple/Android users needs to understand how language/region variants become distinct crawlable resources without duplicate/canonical conflicts. This should precede keyword tooling or search-performance optimization because locale architecture is structural and expensive to retrofit.
