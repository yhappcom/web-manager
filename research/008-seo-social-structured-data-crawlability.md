# 008 — SEO, Social Sharing, Structured Data & Crawlability Baseline

Status: FOUNDATION / production contract established; real indexing and rich-result validation still required
Date: 2026-09-14
Scope: `minttap.app` company/app/support/privacy/account-control public web surfaces

## Question

How should MintTap make public pages discoverable, correctly canonicalized, understandable to search engines, shareable on social platforms and resistant to indexing mistakes without using SEO tactics that distort product truth?

## RELATED DOMAIN CHECK

### Web Design
- Search metadata must reflect the actual page hierarchy and visible content rather than acting as a separate marketing layer.
- Production validation remains a Web Design/implementation responsibility because titles, headings, navigation and structured data must remain coherent in real pages.

### Typography / Type
- Search/social titles and descriptions are content strings, but visible page titles and localized content still require Korean/English browser/type validation.

### Layout / Interaction
- Crawlable normal hyperlinks and coherent heading/page hierarchy support both wayfinding and search discovery.

### Existing Web Manager studies
- Study 002 established durable app/page hierarchy.
- Study 004 established Product Truth and cross-channel consistency.
- Study 005 established HTTPS/canonical-origin direction.
- Study 007 established locale URLs, self-canonical localized pages and hreflang.

### Overlap decision
This study integrates current Google Search and Open Graph requirements into a MintTap-specific production contract. It does not claim ranking guarantees.

---

## SOURCE — minimum Google Search technical requirements

Google's technical requirements say that a page is eligible for indexing when:
1. Googlebot is not blocked;
2. the page returns HTTP `200`;
3. the page has indexable content.

Meeting these requirements does not guarantee crawling, indexing or ranking.

Primary sources:
- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/essentials/technical

### MINTTAP DECISION — indexability default

Public user-serving pages intended to be found should normally be crawlable and indexable, including:
- localized company/home pages;
- app portfolio pages;
- per-app product pages;
- public support/help pages;
- public privacy policies;
- public account-deletion/data-control pages where applicable;
- public contact/about pages.

Do not use search blocking to hide weak or incomplete public information that stores or users are expected to access. Fix the page instead.

### Non-indexable/private classes

Use access control for genuinely private material:
- staging/preview sites;
- unpublished legal drafts;
- internal release manifests;
- internal data contracts;
- admin/CMS tools;
- private analytics or support consoles.

Public-but-intentionally-nonindexable pages may use `noindex` only after a documented reason.

---

## SOURCE — robots.txt vs noindex

Google explicitly states that `robots.txt` is primarily a crawl-management mechanism, not a reliable mechanism for preventing a web page from appearing in Search. A blocked URL may still be indexed from links. To keep a crawlable page out of Search, Google supports `noindex`; for `noindex` to work, the crawler must be allowed to access the page and see the directive.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/robots/intro
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag

### MINTTAP DECISION

- `robots.txt` must never be used as the sole privacy/security control.
- `robots.txt` must never be the only mechanism for removing an HTML page from Search.
- Confidential content must be authenticated/not publicly exposed.
- Public pages intentionally excluded from search use `noindex` while remaining crawlable.
- Required store-facing URLs must not accidentally inherit `noindex` or staging robots rules at production deploy.

### BLOCKER

Production launch is blocked if a required Privacy, Support, Account Deletion or app product page unexpectedly returns `noindex`, is robots-blocked when intended for discovery, requires authentication, or returns non-200 unexpectedly.

---

## SOURCE — titles and snippets

Google recommends a descriptive, concise, unique `<title>` for every page, avoiding vague titles, keyword stuffing and excessive boilerplate. Google may generate search title links from several sources, including the HTML title, visible main title/headings, Open Graph title and link text.

Google's snippet guidance recommends page-specific meta descriptions that accurately summarize the page. Google may still select other text from the page depending on the query.

Primary sources:
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/snippet

### MINTTAP DECISION — metadata content contract

Every indexable human-facing page gets:
- a unique localized `<title>`;
- a localized meta description that truthfully summarizes the page;
- one clearly dominant visible page heading/title;
- visible content that supports the same factual promise.

The page title, H1, Open Graph title and search description may differ editorially but must not contradict Product Truth.

### Title pattern direction

Do not freeze one rigid template yet, but likely patterns are:
- Home: `MintTap — <concise company/product positioning>`
- App: `<App Name> — <primary user value> | MintTap`
- Support: `<App Name> Support | MintTap`
- Privacy: `<App Name> Privacy Policy | MintTap`
- Account deletion: `Delete <App Name> Account | MintTap`

Localized titles must use the primary language/script of the localized page.

### OPEN

Final brand naming/casing and title templates require actual company positioning and Design Studio content/typography review.

---

## Canonical URLs

Study 007 already establishes self-canonical localized pages.

### MINTTAP DECISION

Every indexable page should emit a single final canonical URL matching:
- HTTPS;
- selected canonical host (`minttap.app` direction from Study 005);
- normalized lowercase/slug rules;
- locale path;
- final non-redirecting URL.

Do not canonicalize Korean to English or English to Korean.

Tracking/query variants should normally canonicalize to the clean content URL unless the parameter materially changes indexable content.

Internal navigation should link directly to canonical URLs rather than relying on redirect chains.

---

## Localized discovery / hreflang

Study 007 remains authoritative:
- unique URL per language;
- self-canonical per translated page;
- reciprocal `hreflang`;
- user-controlled language links;
- no primary reliance on automatic IP/browser-language redirects.

SEO metadata (`title`, description, visible H1/content) must be genuinely localized rather than only the shared navigation/footer.

---

## SOURCE — sitemaps

Google supports XML sitemaps and recommends them as a way to inform Google about new/updated URLs. XML sitemaps can also include information about localized page versions.

Primary source:
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap

### MINTTAP DECISION

Generate `/sitemap.xml` from the same route/content source used to publish the website rather than maintaining it manually once the site grows beyond a trivial number of pages.

Include only URLs that are:
- canonical;
- intended to be indexed;
- production/public;
- final `200` URLs.

Exclude:
- redirects;
- `noindex` pages;
- staging/preview URLs;
- duplicate query variants;
- private/internal artifacts;
- machine verification endpoints such as AASA/assetlinks/app-ads.txt.

Initial hreflang direction remains HTML annotations per Study 007. Do not duplicate hreflang into the XML sitemap merely for redundancy unless automation makes both representations provably consistent.

### Release validation

- sitemap returns `200`;
- XML parses;
- all entries are canonical and indexable;
- no retired/redirected locale URLs remain;
- Search Console accepts the sitemap after production launch.

---

## Crawlable navigation and internal links

Google Search Essentials recommends crawlable links so Google can discover site pages.

### MINTTAP DECISION

Primary and contextual navigation must use normal crawlable anchors with real `href` destinations for page navigation.

JavaScript may enhance navigation, but must not be the only way to discover critical app/support/privacy/account-control routes.

Every app should be reachable through a reasonable internal-link path from the app portfolio/company structure.

Support/privacy/account deletion should also be reachable from the relevant app page and not exist only as hidden store-console URLs.

---

## Structured data strategy

### SOURCE — Organization

Google recommends Organization structured data on the home page or a single organization/about page to help understand and disambiguate an organization. There are no universally required Organization properties; applicable real properties should be used.

Primary source:
- https://developers.google.com/search/docs/appearance/structured-data/organization

### MINTTAP DECISION — Organization JSON-LD

Use `Organization` JSON-LD on the final company home/about surface after MintTap's public legal/entity facts are confirmed.

Candidate factual properties:
- `name`;
- `url`;
- `logo`;
- `sameAs` for verified official profiles only;
- legitimate contact/address fields only if publicly appropriate and verified.

Do not invent company identifiers, address, social accounts or contact data for schema completeness.

---

## SOURCE — SoftwareApplication rich results

Google supports `SoftwareApplication` structured data. For Google's software-app rich-result eligibility, required data includes the app name, an `offers.price` value and either a qualifying aggregate rating or review. Recommended properties include application category and operating system.

Primary source:
- https://developers.google.com/search/docs/appearance/structured-data/software-app

### MINTTAP DECISION — no fabricated app rich-result data

Do **not** add rating/review values copied, synthesized or invented solely to satisfy Google's SoftwareApplication rich-result requirements.

Do not copy App Store/Google Play ratings into structured data unless current Google structured-data policies clearly permit that use and the rating is visibly represented with correct provenance on the page. This requires a separate validation before implementation.

For now:
- Organization structured data is the safer Foundation default.
- SoftwareApplication markup remains **CONDITIONAL / OPEN** per app.
- If later used, every property must match visible page content and Product Truth, and the page must pass Google's Rich Results Test.

### BLOCKER

Structured data that claims a rating, price, availability or platform support not truthfully represented by the current app/page must not ship.

---

## Breadcrumb structured data

For deeper support/help hierarchies, `BreadcrumbList` may be useful because it represents the page's place in the site hierarchy. It is not required on shallow pages.

Implementation is deferred until the final support/help taxonomy exists.

---

## SOURCE — Open Graph social metadata

The Open Graph protocol defines basic metadata including:
- `og:title`;
- `og:type`;
- `og:image`;
- `og:url`;
with optional values including `og:description`, `og:site_name`, `og:locale`, alternate locales and image metadata.

Primary source:
- https://ogp.me/

### MINTTAP DECISION — social preview baseline

Indexable share-worthy pages should provide localized social metadata:
- `og:title`;
- `og:description`;
- `og:type` (normally `website` unless a justified type applies);
- `og:url` exactly matching that locale page's canonical URL;
- `og:image` using a stable HTTPS asset;
- `og:image:alt` describing the image;
- `og:site_name` = MintTap when final brand naming is confirmed.

`og:locale` / alternates may be used when the final locale mapping is established; note that Open Graph locale syntax differs from HTML BCP 47 conventions.

Social images must not claim features, ratings, awards, prices or UI localization unsupported by Product Truth.

### VALIDATION

Before production confidence:
- test shared URLs on actual target social/messaging platforms;
- verify localized title/description/image;
- verify cached previews update after material changes;
- ensure images remain publicly fetchable over HTTPS.

Platform-specific card tags may be added only after checking the current official platform requirements; Open Graph is the initial cross-platform baseline.

---

## SOURCE — favicon and site identity

Google may show a site favicon in search results. It expects a crawlable stable favicon associated from the host-level home page; it uses one favicon per hostname.

Primary source:
- https://developers.google.com/search/docs/appearance/favicon-in-search

### MINTTAP DECISION

Provide one stable MintTap favicon set for `minttap.app`. Locale paths do not get different brand favicons unless a future hostname-level architecture justifies it.

The favicon is a company/site identity asset, not an app icon substitute.

---

## Search Console / production verification

### MINTTAP DECISION

Once a production site exists:
- verify `minttap.app` in Google Search Console;
- submit sitemap;
- inspect representative Korean and English URLs;
- monitor indexing/page errors;
- inspect canonical selection;
- verify hreflang/localized discovery through live indexed behavior;
- validate structured data using Google's Rich Results Test where applicable;
- monitor major release URL changes.

Search Console status is evidence about Google's observed production behavior, not merely a setup task.

---

## SEO release manifest additions

Extend the existing Content Release Manifest with:

- route/URL added, changed or retired;
- expected index state (`index`, `noindex`, private);
- HTTP status;
- canonical URL;
- hreflang set;
- localized title;
- localized meta description;
- H1 / visible content confirmation;
- sitemap inclusion;
- internal-link source(s);
- Open Graph metadata/image;
- structured-data type + validation result, if any;
- Search Console inspection required?;
- redirect migration required?;
- stale preview/cache risk.

---

## Indexability classes

### Class A — discoverable public
Default for company, apps, support, privacy and user account-control guidance. Crawl + index.

### Class B — public but intentionally noindex
Use only with documented rationale, for example a utility/result page that must be publicly reachable but should not appear in search.

### Class C — private
Authentication/access control. Do not rely on robots/noindex for confidentiality.

Every new route must explicitly inherit one of these classes.

---

## Launch / release gate

For each public indexable locale page:

1. HTTPS final URL returns `200`.
2. No accidental robots block or `noindex`.
3. Correct `<html lang>`.
4. Unique localized title and description.
5. Clear visible main heading/content.
6. Self canonical.
7. Correct reciprocal hreflang when alternates exist.
8. Canonical internal links.
9. Sitemap state correct.
10. Open Graph URL/title/description/image match current localized truth.
11. Structured data, if present, matches visible content and passes relevant validator.
12. No Product Truth contradiction.
13. Required accessibility checks from Study 006 still pass.
14. Search Console inspection after production launch for representative/high-risk URLs.

### BLOCKER examples
- required public URL inaccessible or unexpectedly non-200;
- accidental `noindex`/robots behavior;
- Korean page canonicalized to English or vice versa;
- sitemap containing retired redirects/staging URLs;
- title/social preview claims a feature not shipped;
- fabricated ratings/reviews in structured data;
- Organization schema containing invented entity/contact/social facts;
- social image exposes outdated or misleading app UI;
- production release leaves critical pages linked only through JavaScript/non-crawlable UI.

---

## CHANGE WATCH

Periodically recheck:
- Google Search Essentials and indexing controls;
- canonical/hreflang behavior;
- supported structured-data rich-result requirements;
- Organization/SoftwareApplication schemas as interpreted by Google;
- favicon/site-name/search appearance guidance;
- major social platform preview/card requirements.

SEO rules are not timeless; search presentation and supported rich-result features can change.

---

## OPEN items

- Final company legal/entity facts for Organization schema.
- Final company/site name presentation in Google Search.
- Whether SoftwareApplication markup is worthwhile/eligible for each MintTap app.
- Rating/review provenance policy if ever displayed on-site.
- Final social-image art direction and image dimensions per target sharing platform.
- Exact CMS/framework implementation for metadata generation.
- Search Console ownership and alert routing.
- Final support/help taxonomy and BreadcrumbList use.
- Bing/other search-engine submission and verification strategy.
- App-specific content-search demand/keyword research; Foundation intentionally avoids keyword-chasing before product positioning is defined.

---

## HANDOFFS TO DESIGN STUDIO

### Web Design
Actual pages must reconcile search metadata with visible title/hierarchy, social-preview visuals, localization and responsive design rather than treating SEO as hidden tags.

### Typography / Type
Search title/H1 alignment and localized Korean/English page titles are real contexts for long-label/mixed-script validation.

### Layout / Interaction
Internal linking and app/support/privacy discovery should improve both human wayfinding and crawler discovery; SEO must not create hidden or redundant navigation solely for bots.

## Result

MintTap now has a Foundation search/social production contract. Production PASS remains blocked on an implemented site, real company/app content, Search Console observation, actual social preview tests and structured-data validation against live pages.
