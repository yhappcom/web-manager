# 009 — SEO Independent Verification & Social Preview Metadata

Status: FOUNDATION / deliberate independent verification and extension of Study 008
Date: 2026-09-14

## Purpose

Study 008 already establishes MintTap's canonical, sitemap, crawlability and structured-data baseline. This study deliberately repeats selected high-impact search controls against current primary sources and extends the area that Study 008 leaves preliminary: page-title/snippet behavior and Open Graph social-preview metadata.

This is intentional overlap for independent verification, not a competing canonical SEO architecture.

## RELATED STUDY

Canonical SEO architecture remains:
- `008-seo-structured-data-crawlability.md`

This study confirms/extends it and should be read as a companion.

---

## REPLICATION — minimum indexability

Google's current technical requirements state that a page is eligible for indexing when Googlebot is not blocked, the page returns HTTP 200, and the page has indexable content. Eligibility does not guarantee indexing or ranking.

Primary sources:
- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/essentials/technical

### Confirmation

Study 008's crawlability contract is consistent with the current source.

### MINTTAP consequence

Launch-critical public surfaces such as app pages, support, privacy and account-deletion guidance should not accidentally inherit staging authentication, non-200 responses, crawl blocks or `noindex`.

---

## REPLICATION — robots.txt is not an indexing/privacy control

Google states that `robots.txt` manages crawling and is not a reliable mechanism for preventing an HTML URL from appearing in Search. A disallowed URL may still be known/indexed from external references. Google supports `noindex` for preventing a crawlable page from being indexed; the crawler must be able to access the page to see the directive.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/robots/intro
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag

### Confirmation / refinement

Study 008 correctly rejects `robots.txt` as security. Add the following operational distinction:

- **Private/confidential** → authentication/access control; never rely on robots or noindex.
- **Public but intentionally absent from search** → crawlable `noindex`, with documented rationale.
- **Public and discoverable** → crawlable/indexable, no accidental `noindex`.

### Indexability classes

- **A — discoverable public:** company, app, support, privacy and user account-control pages by default.
- **B — public/noindex:** exceptional utility/result pages with an explicit reason.
- **C — private:** staging, internal contracts/manifests, admin and unpublished drafts protected by access control.

Every new route should inherit a deliberate class.

---

## SOURCE — title links

Google recommends a concise, descriptive, unique `<title>` for every page, avoiding vague titles, keyword stuffing and repeated boilerplate. Google can generate title links from the HTML title, visible headings, Open Graph title, link text and other prominent page content.

Google also recommends that the title use the same language and writing system as the primary page content.

Primary source:
- https://developers.google.com/search/docs/appearance/title-link

### MINTTAP DECISION

Every indexable localized page gets:
- a unique localized `<title>`;
- one clearly dominant visible page heading/title;
- title language/script matching the localized page;
- factual alignment with Product Truth.

Possible pattern direction, not final marketing copy:
- Home: `MintTap — <company/product positioning>`
- App: `<App Name> — <primary user value> | MintTap`
- Support: `<App Name> Support | MintTap`
- Privacy: `<App Name> Privacy Policy | MintTap`
- Account deletion: `Delete <App Name> Account | MintTap`

Korean equivalents must be written naturally in Korean rather than mechanically retaining an English template.

---

## SOURCE — meta descriptions / snippets

Google may use a page's meta description for a search snippet when it better describes the page, but may also select visible page text based on the query. Meta descriptions should accurately summarize the page rather than act as keyword stuffing.

Primary source:
- https://developers.google.com/search/docs/appearance/snippet

### MINTTAP DECISION

Each important indexable page receives a localized, factual meta description. It is a summary hint, not a guaranteed search-result rendering.

Descriptions must not contain:
- unshipped feature claims;
- unsupported superlatives;
- stale price/subscription facts;
- unsupported language/platform claims.

---

## SOURCE — XML sitemap independent verification

Google supports XML sitemaps and recommends them for communicating new/updated canonical URLs; XML sitemaps can also carry localized-version information.

Primary source:
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap

### Confirmation

Study 008's rule is retained: sitemap contains only final canonical indexable public URLs. Redirects, staging, noindex pages, private artifacts and machine verification endpoints do not belong in the ordinary page sitemap.

Study 007 currently chooses HTML `hreflang`; do not duplicate hreflang into sitemap solely for redundancy unless automation makes both outputs consistent.

---

## SOURCE — Open Graph protocol

The Open Graph protocol defines four basic metadata properties:
- `og:title`
- `og:type`
- `og:image`
- `og:url`

Optional properties include `og:description`, `og:site_name`, `og:locale`, alternate locales and structured image properties such as `og:image:alt`.

Primary source:
- https://ogp.me/

## MINTTAP DECISION — social-preview baseline

Share-worthy public pages should provide localized Open Graph metadata:
- `og:title`;
- `og:description`;
- `og:type` — normally `website` unless a justified type exists;
- `og:url` — exactly the locale page's final canonical URL;
- `og:image` — stable public HTTPS asset;
- `og:image:alt` — description of the image;
- `og:site_name` — MintTap after final public brand naming is confirmed.

`og:locale` / `og:locale:alternate` can be added when the final locale mapping is fixed. Open Graph locale syntax is not identical to HTML BCP 47 syntax, so mappings must be explicit rather than copied blindly.

### Product-truth rule

Social preview copy and imagery are another public product surface and therefore consume the same Product Truth Record / Screenshot Evidence Set.

Do not show:
- unshipped features;
- invented ratings/awards;
- stale UI;
- a localized app UI that is not actually shipped;
- unsupported price/subscription claims.

### VALIDATION

Production PASS requires testing representative URLs on the actual target social/messaging channels because preview caching and supported metadata differ by platform.

Platform-specific card metadata should be added only after checking the current official requirements for the channels MintTap actually uses.

---

## SOURCE — SoftwareApplication rich-result requirements recheck

Google's current SoftwareApplication rich-result documentation requires an app name, an offer price and either a qualifying aggregate rating or review; recommended data includes application category and operating system.

Primary source:
- https://developers.google.com/search/docs/appearance/structured-data/software-app

### Confirmation

Study 008's conservative policy is confirmed.

Do not manufacture or synthesize rating/review data to qualify for a rich result. Do not assume App Store/Google Play ratings can simply be copied into site structured data; provenance and current structured-data policy require explicit validation before any such implementation.

Organization markup remains the safer company-level Foundation default once real public entity facts are known.

---

## Release Manifest additions

Add these fields to the existing Content Release Manifest for indexable/shareable pages:

- expected indexability class A/B/C;
- HTTP status;
- canonical URL;
- robots/noindex state;
- localized `<title>`;
- localized meta description;
- visible H1/title confirmation;
- hreflang set;
- sitemap inclusion;
- `og:title` / description / URL / image / image alt;
- structured-data type and validation result if present;
- search/social cache refresh risk;
- Search Console inspection required after release?;
- target-channel social preview test required?

---

## BLOCKER examples

- staging `noindex` reaches a production app/privacy/support page;
- robots block is mistakenly treated as confidentiality;
- title/social preview claims a feature not shipped;
- `og:url` differs from the intended canonical locale URL;
- social image contains obsolete UI or false localization;
- fabricated rating/review is added to SoftwareApplication markup;
- a private/internal page is merely disallowed in robots instead of actually protected.

---

## CHANGE WATCH

Recheck periodically:
- Google Search indexing/robots/noindex behavior;
- title/snippet guidance;
- SoftwareApplication rich-result requirements;
- Open Graph protocol and actual platform preview behavior;
- official platform-specific social-card requirements for channels MintTap adopts.

## Result

Study 008's technical SEO architecture is independently confirmed in the areas rechecked. The additional reusable result is a clearer indexability-class model plus a Product-Truth-governed title/snippet/Open Graph contract. Actual search indexing and social previews remain implementation evidence, not Foundation reading PASS.
