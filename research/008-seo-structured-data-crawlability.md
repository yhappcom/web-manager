# 008 — SEO, Structured Data, Sitemap, Canonical & Crawlability

Status: **FOUNDATION STUDY / IMPLEMENTATION NOT YET VALIDATED**  
Research date: **2026-09-14**

## Question

What technical search-discovery baseline should `minttap.app` use so company pages, app pages and localized support/privacy resources are crawlable, correctly canonicalized, discoverable and eligible for useful search features without creating misleading markup?

This study defines architecture and release controls. It does not claim ranking outcomes or rich-result eligibility until the real site is implemented, indexed and validated in Search Console / Rich Results Test.

## RELATED DOMAIN CHECK

### Localization

Study 007 establishes stable `/ko/` and `/en/` user-facing locale URLs, reciprocal `hreflang`, correct `<html lang>` and self-canonical localized pages.

SEO must preserve those rules rather than collapse language versions into one canonical URL.

### Information architecture

Study 002 establishes company → apps → app detail → support/control hierarchy. Search navigation and structured data should reflect, not replace, the user-facing hierarchy.

### Accessibility / Web Design

Search metadata cannot compensate for inaccessible or thin visible content. Structured data must describe real visible page content and actual product facts.

## SOURCE — canonical URL is a representative URL, not a guarantee

Google describes canonicalization as selecting a representative URL from duplicate or highly similar pages. Signals include redirects, sitemap inclusion and `rel="canonical"`, but Google may select a different canonical.

Source:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization

### MINTTAP DECISION

Every indexable MintTap page gets an explicit canonical pointing to its final HTTPS public URL.

Examples:
- `https://minttap.app/ko/apps/minttap/` → itself
- `https://minttap.app/en/apps/minttap/` → itself

Canonical links must not point to:
- HTTP URLs;
- redirecting URLs;
- a different language merely because content is related;
- staging/preview hosts;
- tracking-parameter variants.

Internal links and sitemap entries should reinforce the same preferred URLs.

## SOURCE — localized pages need localization annotations, not cross-language canonical collapse

Google's current canonical documentation states that different-language versions are only treated as duplicates when primary content remains untranslated; same-language regional variants may need canonicalization plus `hreflang`.

Source:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization

### MINTTAP DECISION

Retain Study 007 rule:
- substantive Korean page → Korean self-canonical;
- substantive English page → English self-canonical;
- `hreflang` connects equivalents.

## SOURCE — structured data must describe real page/application facts

Google supports `SoftwareApplication` / mobile-application structured data and requires factual app properties. For software-app rich-result eligibility, required fields include app name, an offer/price, and either rating or review; recommended fields include operating system and application category. Google does not guarantee a rich result even when markup is valid.

Source:
- https://developers.google.com/search/docs/appearance/structured-data/software-app

### MINTTAP DECISION — use structured data conservatively

Per-app canonical pages may use `SoftwareApplication` or the applicable subtype only when the visible page provides matching information.

Do **not** invent:
- ratings;
- reviews;
- prices;
- availability;
- supported operating systems;
- app categories.

If MintTap does not have legitimate review/rating data satisfying Google's requirements, do not add synthetic data merely to pursue a rich result.

Structured-data truth must derive from the Product Truth Record and store/release data already established in Study 004.

## SOURCE — Organization markup belongs on the organization surface

Google recommends placing `Organization` structured data on the home page or a single organization/about page rather than redundantly on every page. Relevant properties include name, URL, logo and applicable real-world/online contact information.

Source:
- https://developers.google.com/search/docs/appearance/structured-data/organization

### MINTTAP DECISION

Add one canonical Organization entity definition on `/` or the selected company/about surface after MintTap's legal/public company identity is confirmed.

Do not publish guessed address, telephone, legal name or social-profile links.

OPEN fields already identified in STATUS — legal entity and public contact details — block final Organization markup.

## SOURCE — Breadcrumb structured data expresses hierarchy

Google's `BreadcrumbList` guidance says breadcrumbs communicate page position in a site hierarchy and may help users understand and navigate the site.

Source:
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

### MINTTAP DECISION

Use visible, accessible breadcrumbs on deeper pages when they materially improve orientation, then mirror the same hierarchy in `BreadcrumbList` JSON-LD.

Potential hierarchy:
- Home → Apps → App
- Home → Apps → App → Support
- Home → Apps → App → Privacy

Do not add schema-only breadcrumbs that have no coherent user-facing hierarchy.

## SOURCE — structured data is optional and search features change

Google's Search documentation changes supported structured-data features over time; the Search update log documents removals and deprecations. Valid markup does not guarantee display.

Sources:
- https://developers.google.com/search/docs/appearance/structured-data/software-app
- https://developers.google.com/search/updates

### CHANGE WATCH

Structured-data support is a **change-watch domain**. Revalidate supported Google Search types before building a dependency on a particular rich-result presentation.

## robots.txt policy

Google implements the Robots Exclusion Protocol and supports `user-agent`, `allow`, `disallow` and sitemap references; unsupported directives such as `crawl-delay` should not be relied on.

Source:
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec

### MINTTAP DECISION

Production `robots.txt` should be intentionally minimal.

Baseline intent:
- allow crawling of public company/app/help/privacy pages;
- block only paths that genuinely should not be crawled and where robots exclusion is appropriate;
- reference the production sitemap;
- never treat `robots.txt` as an access-control/security mechanism.

Staging/preview systems should use actual authentication and/or explicit `noindex` controls as appropriate, not merely `Disallow` and hope content remains private.

## sitemap policy

Google recommends submitting a sitemap to help discover and keep track of URLs; structured-data documentation repeatedly recommends sitemap submission after deploying changes.

Sources:
- https://developers.google.com/search/docs/appearance/structured-data/software-app
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

### MINTTAP DECISION

Generate an XML sitemap containing only final canonical, indexable public URLs.

Include:
- localized company pages;
- `/apps/` indexes;
- canonical per-app pages;
- indexable support/help pages where useful;
- public privacy/account-control pages when intended for search discovery.

Exclude:
- redirect sources;
- staging/preview URLs;
- duplicate query-parameter URLs;
- `noindex` pages;
- machine-readable verification endpoints (`.well-known`, `app-ads.txt`) unless a specification or search need explicitly requires otherwise.

The sitemap is a discovery/canonical signal, not an authorization list.

## crawlability contract

An indexable MintTap page must normally satisfy:

1. public HTTPS final URL;
2. HTTP 200;
3. not blocked by authentication;
4. not blocked from crawling unintentionally;
5. no accidental `noindex`;
6. meaningful visible primary content in HTML/rendered output;
7. crawlable internal links from the site hierarchy;
8. correct canonical;
9. correct localized alternates where applicable;
10. sitemap inclusion if part of the indexable public corpus.

### RELEASE BLOCKER

For launch-critical app pages, classify as blocker when:
- canonical points to staging/wrong locale/wrong app;
- production accidentally carries `noindex` from staging;
- robots rules block the app portfolio or required public support/privacy URLs;
- sitemap publishes staging/obsolete/wrong-host URLs;
- localized pages are inaccessible behind forced locale negotiation;
- store-facing public URLs return soft-404/404/error pages.

## page titles and search snippets

### MINTTAP DECISION

Every indexable page requires a unique, descriptive localized page title that reflects visible page content and hierarchy.

Initial pattern concepts, not final copy:
- Korean app page: `<App Name> — <clear product purpose> | MintTap`
- English app page: `<App Name> — <clear product purpose> | MintTap`
- Support: `<App Name> 지원 | MintTap`
- Privacy: `<App Name> 개인정보처리방침 | MintTap`

Meta descriptions should be useful, factual summaries rather than keyword stuffing. They may differ across locale and page type but remain aligned to visible content and Product Truth.

Exact copy awaits content/marketing research and actual app inventory.

## app-page structured-data model — provisional

When factual fields are available, app pages may use JSON-LD along these lines:

```json
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "Example App",
  "operatingSystem": "iOS, Android",
  "applicationCategory": "FinanceApplication",
  "offers": {
    "@type": "Offer",
    "price": "0"
  }
}
```

This is **illustrative only**, not approved MintTap production markup. Actual price/category/platform data must come from the Product Truth Record. Google's current SoftwareApplication rich-result requirements also involve a legitimate rating or review, so the absence of those must not be worked around with fabricated data.

## social sharing metadata — preliminary

Search SEO and social-preview metadata are different concerns. Open Graph/social cards should be studied/implemented as a separate presentation layer but must reuse the same page title, description, canonical URL and approved image truth where appropriate.

Provisional baseline fields:
- `og:title`
- `og:description`
- `og:url`
- `og:image`
- page-type-specific social fields where justified.

Do not let campaign-specific Open Graph copy contradict canonical page content or shipped product truth.

A deeper platform-specific social-card study can be done if actual channels require it.

## favicon / brand search identity

Google supports one favicon per hostname and recommends a stable, square, crawlable brand-representative favicon; search display is not guaranteed.

Source:
- https://developers.google.com/search/docs/appearance/favicon-in-search

### MINTTAP DECISION

`minttap.app` should use a stable company favicon at hostname level. Per-app subdirectory pages should not assume they can get different Google Search favicons because Google treats favicon identity at hostname scope.

This has a direct brand-architecture implication: if multiple apps remain under `minttap.app/apps/...`, search favicon identity will remain MintTap-company-level rather than app-specific.

## measurement and validation

Before declaring SEO foundation implemented:

### Pre-deploy
- validate canonical and hreflang output;
- validate robots.txt syntax/intent;
- validate generated sitemap URLs;
- validate JSON-LD syntax;
- run Google Rich Results Test for supported types;
- verify visible content matches markup;
- verify production hostname in all metadata.

### Post-deploy
- register/verify the applicable Search Console property;
- submit sitemap;
- inspect representative URLs with URL Inspection;
- check Google-selected canonical vs declared canonical;
- check indexing of Korean/English app pages;
- inspect structured-data reports where available;
- monitor 404/soft-404/redirect/crawl anomalies;
- revalidate after major routing/localization/site migrations.

## Search Console ownership

OPEN: exact Google account/organizational ownership is not yet documented.

MINTTAP DECISION: Search Console must not be tied to an undocumented single-person account with no recovery/continuity plan. Ownership/access policy should be recorded as part of operational governance.

## content quality principle

Technical SEO cannot compensate for weak/thin app pages.

Each app page should eventually answer real user questions such as:
- what is this app;
- who is it for;
- what does it actually do;
- supported platforms;
- current availability;
- key limitations/requirements where material;
- how to download;
- where to get support/privacy/account control.

This becomes the bridge to the next research topic: company/app marketing content model.

## HANDOFFS TO DESIGN STUDIO

### Web Design

Future implementation should validate:
- metadata generation across `/ko/` and `/en/` page templates;
- breadcrumbs that remain usable on mobile/reflow;
- structured-data fields generated from the same visible component/content model;
- no JavaScript/rendering architecture accidentally hides primary content from initial/processed HTML.

### Typography / Layout

Search titles/snippets and actual pages create long Korean/English label/page-heading stress contexts. Visible breadcrumb and page-title hierarchy should be tested under responsive/localized conditions.

## CHANGE WATCH

Recheck periodically:
- Google Search structured-data support/deprecations;
- SoftwareApplication eligibility requirements;
- canonical/localized-site guidance;
- crawler/robots behavior;
- search appearance/favicons;
- sitemap limits/guidance if the site grows materially.

## OPEN items

- final app inventory and canonical slugs;
- actual organization/legal/public contact data;
- real app categories/pricing/store IDs;
- whether legitimate first-party rating/review data will exist and be appropriate for markup;
- exact social platforms requiring card metadata;
- Search Console account/access ownership;
- production framework and server-side/rendering behavior;
- whether support articles should all be indexable or selectively `noindex` based on content value/risk.

## Foundation conclusion

MintTap SEO should be implemented as a **truthful discovery layer over the real site architecture**, not as a parallel marketing database.

The baseline is:

**stable final URLs + self-consistent canonical/hreflang + crawlable visible content + deliberate robots/sitemap controls + conservative structured data derived from Product Truth + post-launch Search Console validation + continuous change watch.**