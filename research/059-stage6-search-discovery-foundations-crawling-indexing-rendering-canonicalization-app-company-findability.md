# 059 — Stage 6 Search & Discovery Foundations: Crawling, Indexing, Rendering, Canonicalization & App-Company Findability

Date: 2026-09-16  
Stage: 6 — Search / Discovery / Content Quality  
State: **PASS — FOUNDATION/PRACTITIONER CHECKPOINT**

## Purpose

Establish a first-principles model of external web discovery before keyword tactics, structured data, content promotion or ranking optimization. The target is an Apple/Android app company operating under `minttap.app`, with Company, Product/App, Support and Governance page families.

This block deliberately does **not** infer the current production architecture, robots directives, sitemap, canonical implementation, Search Console state, rendering model or indexed URL inventory of `minttap.app`. Those remain project-mode facts requiring direct inspection.

---

## 1. Core model

`publish resource → expose stable URL → discover URL → crawl/fetch → parse → render when applicable → extract content/links/signals → index/deduplicate → select canonical representation → serve/rank for a query → revisit after change`

### SOURCE — Google Search pipeline

Google documents three broad Search stages: crawling, indexing and serving results. URL discovery can occur through known pages/links and submitted sitemaps. During crawling Google renders pages and runs JavaScript with a recent Chrome; during indexing it analyzes content and key metadata, detects duplicate/similar pages, clusters them and chooses a canonical representative. Google explicitly states that crawling, indexing and serving are not guaranteed merely because technical requirements are met.

Primary source: Google Search Central, *In-depth guide to how Google Search works*  
https://developers.google.com/search/docs/fundamentals/how-search-works

### SYNTHESIS

Search visibility is a pipeline, not one event. A failure at discovery, fetchability, rendering, indexability, canonical selection, content relevance or serving can produce the same user-visible symptom — “this page is not found in search” — while requiring different diagnosis.

### MINTTAP DIRECTION

Web Manager diagnostics should never jump directly from “not ranking” to content/keyword changes. First locate the failing pipeline stage.

---

## 2. Discovery is not indexing

### SOURCE

Google states that most pages are discovered automatically through crawling; links from known pages and sitemaps can provide URLs for discovery. Google’s developer guide recommends crawlable `<a>` links, ensuring pages are reachable from another findable page, and sitemaps as discovery support. Bing likewise describes sitemaps as a mechanism to tell Bing about URLs, particularly URLs otherwise difficult for crawlers to discover.

Primary sources:
- https://developers.google.com/search/docs/fundamentals/how-search-works
- https://developers.google.com/search/docs/fundamentals/get-started-developers
- https://www2.bing.com/webmasters/help/sitemaps-3b5cf6ed

### SYNTHESIS

A sitemap is a discovery inventory/signal, not an indexing command. Internal linking remains structurally important because it provides both user navigation and crawler-discoverable relationships.

### Counterexample

A newly launched `/support/account-delete` URL appears in `sitemap.xml` but is isolated from the visible Support/Governance architecture. Sitemap submission may expose the URL, but it does not repair poor user wayfinding, guarantee indexing or establish that the page is the preferred representation.

---

## 3. Crawlability, indexability and privacy are different controls

### SOURCE

Google describes `robots.txt` as controlling crawler requests. Google also warns that a URL blocked by `robots.txt` may still be indexed without being crawled, and explicitly says not to use robots.txt to protect private content; authentication is required for private resources. For `noindex` to work, Google must be allowed to crawl/access the page so it can see the directive. Bing documents the same practical dependency for its supported `noindex` directive: the page must be crawlable for Bing to see the tag.

Primary sources:
- https://developers.google.com/crawling/docs/robots-txt/useful-robots-txt-rules
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://www.bing.com/webmasters/help/robots-meta-tags-and-attributes-that-bing-supports-5198d240

### Durable distinction

- **crawl control**: whether a crawler may request a resource;
- **index control**: whether a fetched resource should be eligible to remain in a search index;
- **access control**: whether an unauthorized party can obtain the resource at all.

These controls are not interchangeable.

### MINTTAP DIRECTION

Never use `robots.txt` as a security/privacy boundary for user, account, draft, internal or otherwise sensitive content. Stage 8 will treat authorization separately.

---

## 4. HTTP status is part of search meaning

### SOURCE

Google’s minimum technical requirements for indexing eligibility include that Googlebot is not blocked, the page returns HTTP `200`, and the page has indexable content. Eligibility still does not guarantee indexing. Google’s JavaScript documentation notes that pages returning `200` are queued for rendering unless indexing directives prevent it, while non-`200` responses such as `404` may skip rendering.

Primary sources:
- https://developers.google.com/search/docs/essentials/technical
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics

### SYNTHESIS

The browser-visible screen alone is insufficient evidence. A client-rendered “not found” view served with HTTP `200` communicates a different machine-level state from a genuine `404`; similarly, a redirect implemented only after client boot is not equivalent to an HTTP redirect at fetch time.

### Design Studio dependency

Web Design W013 has partial same-document Chromium history/navigation evidence but explicitly leaves true HTTP direct-entry/reload/404 validation OPEN. Search discovery adds another reason that this gap matters: route semantics must survive direct crawler/server requests, not merely client-side navigation.

---

## 5. JavaScript rendering: supported does not mean architecture-neutral

### SOURCE

Google documents a crawl → render → index flow for JavaScript applications. Googlebot parses initial HTML for links, queues eligible pages for rendering, uses headless Chromium to execute JavaScript, then parses rendered HTML and can discover additional links. Google states that server-side or pre-rendering remains a good idea because it can be faster for users and crawlers and because not all bots run JavaScript. Google’s developer guidance also says that JavaScript apps with one HTML page should give each screen or individually meaningful content its own URL.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- https://developers.google.com/search/docs/fundamentals/get-started-developers

### SYNTHESIS

“Google runs JavaScript” is not sufficient architecture justification for a client-only app shell. Searchability depends on stable URLs, successful fetches, renderable resources, DOM-visible meaningful content, crawlable links and correct status/canonical/indexing signals.

### MINTTAP DIRECTION

For public Company/Product/Support/Governance content, rendering architecture should be judged by user performance, resilience, accessibility, crawler observability and operational complexity together. Do not choose SSR/SSG/prerender/client rendering solely because of an SEO slogan.

### OPEN

Actual `minttap.app` rendering architecture is unknown in this curriculum run.

---

## 6. Canonicalization is representative selection, not URL redirection

### SOURCE

Google defines canonicalization as selecting a representative URL from duplicate or very similar content. Signals include redirects, sitemap inclusion and `rel="canonical"`; Google can choose a different canonical than the site owner’s preference. Google explicitly describes canonical preference as a hint rather than an absolute rule.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization
- https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting

### Durable distinction

- **redirect** changes the resource/navigation path presented to a requester;
- **canonical signal** expresses which URL should represent duplicate/similar content in search;
- **indexing decision** is made by the search engine and is not guaranteed by either signal alone.

### Failure modes relevant to an app company

Possible duplicate families include:
- protocol/host variants;
- trailing-slash or route variants;
- tracking/query-parameter URLs;
- staging/demo URLs accidentally public;
- locale/region variants implemented incorrectly;
- old/new app landing pages after product renaming or migration;
- filter/sort states that expose near-identical content at many URLs.

These are examples, not claims about current MintTap production.

### MINTTAP DIRECTION

Define one intended public representation per content identity and make internal links, redirects, canonical hints and sitemap inventory consistent with that identity. Contradictory signals are a governance defect.

---

## 7. Localization creates a content-identity problem before it creates a keyword problem

### SOURCE

Google’s canonicalization documentation states that language versions are treated as duplicates only when primary content remains in the same language; regional variants in the same language may require canonicalization plus `hreflang` to help select the appropriate regional URL.

Primary source: https://developers.google.com/search/docs/crawling-indexing/canonicalization

### SYNTHESIS

For future Korean/English `minttap.app` pages, URL identity, translated primary content, canonical relationships and language/region annotations must be designed as one system. Translating only navigation chrome while leaving primary content unchanged is not equivalent to a genuinely localized content representation.

### DEPENDENCY

Stage 6 later needs a dedicated international discovery/localization block. Do not prematurely prescribe URL paths or `hreflang` topology without the actual locale/market strategy.

---

## 8. Search controls must align with page-family purpose

### Company
Public company identity, contact/trust and product-navigation surfaces normally need deliberate discoverability if they are intended as acquisition/trust entry points.

### Product/App
Each independently meaningful app/product should have a stable public identity/URL if users may search for that product. Product claims and store links remain subject to the cross-channel truth contracts from Stage 2/4.

### Support
High-value support answers can be search entry points. Their value depends on stable content identity, useful text in the DOM, crawlable internal relationships and lifecycle accuracy — not merely on a support UI search box.

### Governance
Privacy, terms, account-deletion/help and similar public obligations may need durable direct URLs for store/reviewer/user access. Whether each should be indexed is a page-specific decision; “governance page” does not automatically imply either index or noindex.

### SYNTHESIS

External search creates additional entry points into the IA. A user may land directly on a deep Support or Governance page without first traversing Home. Stage 2 wayfinding therefore remains a search/discovery dependency: deep pages must carry sufficient identity, context and onward navigation.

---

## 9. Observability: diagnose what the crawler actually received

### SOURCE

Google recommends URL Inspection to understand how Google sees managed URLs and provides Page Indexing/Search Console reports for indexing diagnosis. Bing URL Inspection exposes discovery, crawl and index status plus downloaded HTML/HTTP response details; Bing Site Explorer exposes indexed, error, robots-disallowed, noindex, redirecting and canonical-related URL states.

Primary sources:
- https://developers.google.com/search/docs/fundamentals/get-started-developers
- https://www.bing.com/webmasters/help/url-inspection-55a30305
- https://www.bing.com/webmasters/help/site-explorer-c680da37

### SYNTHESIS

Search management is an observability discipline. Source code intention is weaker evidence than crawler-observed HTTP/HTML/rendered state and index-system reports.

### MINTTAP DIRECTION — Search Discovery Evidence Contract

For every strategically important public URL, record when project mode begins:

1. content identity / page family / owner;
2. intended public URL and locale;
3. discoverability paths: internal links, sitemap, external/store references;
4. fetch result: DNS/TLS/HTTP status/redirect chain;
5. robots crawl permission;
6. index directive/meta/header;
7. initial HTML meaningful content;
8. rendered DOM meaningful content and crawlable links;
9. intended canonical and observed search-engine canonical where available;
10. sitemap inclusion and last modification policy;
11. direct-entry/reload/404 behavior;
12. index status and last crawl evidence;
13. lifecycle state: current/moved/retired/replaced;
14. validation date/tool and unresolved contradiction.

This contract separates **intent**, **implementation**, **crawler observation** and **index outcome**.

---

## 10. Freshness/submission mechanisms are notifications, not guarantees

### SOURCE

Google states that recrawl requests can take days to weeks, repeated requests do not accelerate crawling, and crawl requests do not guarantee indexing. Bing currently recommends IndexNow for faster automated notification of added/updated/deleted URLs while still supporting sitemaps and other submission mechanisms.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl (last updated 2025-12-10 UTC in source)
- https://www4.bing.com/webmasters/help/url-submission-62f2860b

### CHANGE WATCH

Submission APIs, quotas, crawler behavior, webmaster-tool UI and IndexNow participation are platform behavior and must be rechecked before implementation.

### SYNTHESIS

Publishing and notifying are distinct from being crawled, indexed and served. Release workflows should verify eventual search state rather than mark discovery “done” when a sitemap or submission call succeeds.

---

## 11. Anti-patterns rejected

1. **“Put it in the sitemap, therefore it will be indexed.”** — discovery assistance is not an indexing guarantee.
2. **“robots.txt keeps a page private.”** — false security boundary.
3. **“Block crawl and add noindex for extra certainty.”** — crawl blocking can prevent the crawler from seeing `noindex`.
4. **“Google executes JavaScript, so client-only rendering has no search trade-off.”** — rendering is supported but still introduces pipeline and observability dependencies.
5. **“rel=canonical forces Google to use our URL.”** — canonical preference is a signal/hint; Google selects the representative.
6. **“Search Console says indexed, therefore users will find it for relevant queries.”** — indexing and serving/ranking are different stages.
7. **“SEO starts with keywords.”** — content cannot perform if URL identity/discovery/fetch/render/index/canonical foundations are defective.
8. **“A successful SPA route click proves crawler route correctness.”** — direct HTTP entry/status/redirect semantics require separate validation.

---

## 12. Design Studio dependencies / handoffs

Latest checked specialist state: `progress/WEB_STATUS.md`, 2026-09-16. Web Design is Stage 1 PASS / Stage 2 PRACTICE, with W015 deterministic integrated state/recovery execution complete but real browser/network transfer still open.

### Web Design handoff

When W013 or a successor gains true HTTP execution, include:
- direct entry to representative Company/Product/Support/Governance routes;
- correct `200`/redirect/`404` behavior;
- initial HTML vs rendered DOM content identity;
- crawlable `<a href>` relationships;
- route-specific title/canonical/index directives where applicable;
- client navigation and browser history without loss of URL identity.

This is not a request to turn Design Studio into an SEO owner. Web Manager owns search intent, index/canonical strategy and search-system evidence; Web Design can provide runtime transfer evidence for page/route behavior.

### Layout/Interaction handoff

External search means deep pages are entry surfaces. Preserve page identity, local/global wayfinding and recovery when users bypass Home.

### Type handoff

Search-visible titles/headings/body text must survive real KO/EN/mixed content rendering and font fallback, but font styling is not a substitute for DOM text/content semantics.

### Color handoff

No new color-specific dependency in this block beyond existing state/contrast obligations.

No Design Studio canonical file was edited.

---

## 13. Verified facts vs synthesis vs open questions

### VERIFIED / SOURCE
- Google describes Search as crawling → indexing → serving.
- Google discovers URLs through mechanisms including crawlable links and sitemaps.
- Google renders eligible pages with Chromium and uses rendered HTML for indexing/link extraction.
- robots.txt is crawl control, not privacy/access control.
- `noindex` must be crawl-visible to be acted upon.
- indexing eligibility and indexing itself are different; indexing is not guaranteed.
- Google canonical selection can differ from a site-declared preference.
- Google and Bing provide URL/index inspection tooling.

### SYNTHESIS
- Search visibility should be diagnosed as a staged pipeline.
- URL identity is shared infrastructure across IA, navigation, localization, analytics, release operations and search.
- Public app-company pages should be governed by content identity and user task rather than blanket index/noindex rules by page type.
- Crawler-observed state is stronger operational evidence than implementation intention.

### OPEN — requires live MintTap evidence
- actual rendering framework and deployment architecture;
- current route/URL inventory;
- `robots.txt`, robots meta/X-Robots-Tag and sitemap state;
- current canonical tags and redirects;
- current indexed/canonical coverage in Google/Bing;
- Search Console/Bing Webmaster ownership and reports;
- locale URL strategy;
- staging/demo exposure;
- server handling of direct entry, redirects and 404s;
- whether IndexNow is useful for the eventual publishing cadence.

---

## 14. Competency check

This checkpoint passes if the Web Manager can:

- distinguish discovery, crawl, render, index, canonical selection and serving;
- diagnose why sitemap submission is not an indexing guarantee;
- explain why robots crawl control, noindex and authentication solve different problems;
- explain JavaScript rendering without claiming that Google’s JS support makes architecture irrelevant;
- distinguish redirect behavior from canonical preference;
- map Company/Product/Support/Governance pages to intentional discovery rather than blanket SEO treatment;
- request crawler-observed evidence before making a production search claim;
- identify W013’s true-HTTP gap as both navigation/runtime and search-discovery relevant.

**Result: PASS at Foundation/Practitioner checkpoint.**

---

## 15. Next highest-value block

**060 — Search Content Semantics, Titles/Snippets, Helpful Content, Internal Linking & Query-to-Page Intent.**

Reason: after establishing how a URL becomes discoverable/indexable, the next prerequisite is how a search system and a human searcher can understand what a page is for. Study semantic HTML/content signals, title/snippet mechanics, internal anchor/context, query intent and useful people-first app/support content before structured data or keyword tooling.
