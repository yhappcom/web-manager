# 065 — Stage 6 Integration: Search / Discovery / Content-Quality Competency Review & Niche App Search Operating System

Date: 2026-09-16  
State: **PASS — STAGE 6 FOUNDATION/PRACTITIONER INTEGRATION GATE**

## Why this block now
059–064 cover resource discovery/index mechanics, truthful page meaning, structured/entity representation, locale architecture, webmaster observation and niche demand/opportunity. Before advancing to performance/runtime, integrate them and test whether the Web Manager can diagnose an app-company search system end to end rather than merely recall isolated SEO topics.

The Stage 6 roadmap also names social-preview concepts and app links/universal links. These are not search-ranking mechanics, but they affect public URL continuity and app↔web discovery journeys, so this integration closes their foundation-level boundary before the gate.

## Source basis
This integration retains the authoritative primary-source sets documented in 059–064 and rechecks the cross-platform link boundary against:
- Apple Developer — Allowing apps and websites to link to your content: https://developer.apple.com/documentation/xcode/allowing-apps-and-websites-to-link-to-your-content/
- Apple Developer — Associated Domains Entitlement: https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.associated-domains
- Apple Developer — TN3155 Debugging universal links: https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links
- Android Developers — About App Links: https://developer.android.com/training/app-links/about
- Android Developers — Add Intent filters for App Links: https://developer.android.com/training/app-links/add-applinks
- Android Developers — Verify App Links: https://developer.android.com/training/app-links/verify-applinks

Platform behavior is CHANGE WATCH and was rechecked 2026-09-16.

---

## 1. Integrated mental model

`real user need → public resource identity → URL/discovery path → fetch/render → index/canonical/locale interpretation → truthful page/entity representation → search/store/social exposure → direct deep entry → web or verified app continuation → user task → measured outcome → diagnosis/change → recrawl/re-observation`

This model deliberately keeps layers separate. “SEO” is not one subsystem.

### Diagnostic boundaries
- `crawlable ≠ indexable ≠ indexed ≠ canonical ≠ ranked/served`;
- `page title ≠ visible heading ≠ engine-generated title link`;
- `meta description ≠ guaranteed snippet`;
- `schema-valid ≠ engine-supported ≠ eligible ≠ displayed`;
- `hreflang ≠ language detection ≠ canonical ≠ redirect`;
- `query ≠ proven intent ≠ demand census`;
- `impression/click ≠ successful user task`;
- `web URL ≠ app route`, although verified app-link systems can deliberately associate them.

---

## 2. Public URL continuity across web and installed apps

### SOURCE — Apple
Apple documents Universal Links as ordinary HTTP/HTTPS URLs associated bidirectionally with an app and website. When the app is installed and association/handling conditions are satisfied, a universal link can open corresponding app content; otherwise the URL can open in the browser. Apple requires an Associated Domains entitlement plus an `apple-app-site-association` relationship. Apple also warns that incoming URL data must be validated and sensitive/destructive actions should not be blindly triggered.

Apple's current technote documents an operational complication: on iOS 14 and later Apple's CDN retrieves/caches the AASA file. This creates a platform observation/cache clock distinct from website deployment.

### SOURCE — Android
Android App Links are verified HTTP/HTTPS deep links. Android verifies website↔app association using Digital Asset Links (`assetlinks.json`) and app declarations. Verified links can route matching URLs directly to the app; without the app, the same web URL remains a browser resource. Android's documentation also distinguishes ordinary web/custom deep links from verified App Links.

### SYNTHESIS
For a multi-platform app company, the durable object should be a meaningful public HTTPS resource where one exists, with platform association layered on top. Deep-link configuration must not turn a useful public URL into an app-only opaque identifier.

`public HTTPS identity → browser fallback + optional verified native continuation`

### MINTTAP DIRECTION
Do not implement Universal Links/App Links merely because they are available. First identify which real web resources have a corresponding safe native destination and what the browser fallback should do. Association files, app identifiers/signing fingerprints, route mappings and installed/uninstalled behavior are production facts and remain OPEN.

### VALIDATION
When implemented, test at least:
- installed and uninstalled states;
- direct browser navigation vs tapped external link;
- representative path mapping;
- invalid/malformed parameters;
- authentication-required destination behavior;
- fallback behavior;
- iOS AASA and Android assetlinks availability/association;
- platform cache/update timing;
- locale/deep-page continuity where relevant.

---

## 3. Social previews belong to representation, not product truth

Stage 6 roadmap includes Open Graph/social preview concepts. Foundation judgment: social/share metadata is another representation layer around the canonical public resource. It must not become a parallel source of product claims.

### SYNTHESIS
Treat social-preview title/description/image as derived publication metadata whose factual claims come from the same page/product truth contract. Search-engine title/snippet behavior and social-card behavior are different consumers and must not be collapsed.

### OPEN / CHANGE WATCH
Exact preview tags, image constraints, cache invalidation and renderer behavior are platform-specific and changeable. They should be validated against the actual target social platforms during a live launch rather than frozen as a universal SEO rule here.

---

## 4. Niche App Search Operating System

### A. Resource registry
For every public Company/Product/Support/Governance resource:
- stable canonical URL and page family;
- locale and alternate relationships;
- intended index state;
- truth owner/lifecycle owner;
- main user need/task;
- app/store relationship where applicable.

### B. Discovery/index contract
Join 059 evidence:
- internal discovery path;
- HTTP status/redirect;
- robots/index directive;
- initial/rendered content identity;
- canonical;
- sitemap membership;
- lifecycle/retirement behavior.

### C. Meaning/content contract
Join 060:
- distinct need/page purpose;
- truthful visible answer/evidence;
- title/H1/meta relationship;
- descriptive internal-link context;
- deep-entry orientation.

### D. Entity/structured representation
Join 061:
- organization/app/platform/store entities remain distinct;
- schema property truth source;
- engine feature support/eligibility separately recorded;
- validation does not imply rich-result display.

### E. Locale contract
Join 062:
- stable locale resource;
- actual localized main content;
- canonical + hreflang relationship;
- fallback/language switch;
- web/app/store locale continuity without assuming identical inventories.

### F. Observation ledger
Join 063:
- deploy clock;
- crawler/index clock;
- report clock;
- engine-specific inspection/index/canonical state;
- query/page exposure;
- intervention and re-observation.

### G. Demand/opportunity record
Join 064:
- need/query family;
- evidence source/surface/date;
- limitations;
- intent/task hypothesis;
- existing resource;
- unique product/company value;
- maintenance cost;
- create/improve/merge/observe/reject decision.

### H. Cross-surface continuation
For URLs that correspond to native destinations:
- browser resource/fallback;
- iOS Universal Link mapping;
- Android App Link mapping;
- store destination if app unavailable/acquisition is the task;
- security/auth boundary;
- measured downstream outcome where instrumentation permits.

---

## 5. Representative diagnostic exercises

### Scenario 1 — Product page is live but absent from search
Correct sequence:
1. confirm page is intended to be public/indexable;
2. direct-fetch HTTP/robots/index/canonical/rendered identity;
3. inspect discovery/internal links/sitemap;
4. inspect engine URL/index evidence and timestamps;
5. distinguish live fix from stale indexed state;
6. change only the causal layer;
7. re-observe.

Wrong response: rewrite keywords first.

### Scenario 2 — Korean and English pages exist but Google shows the wrong variant
Inspect actual body language, stable locale URLs, canonical graph, hreflang reciprocity, internal locale links and engine-selected canonical. Do not treat `lang` or hreflang as a language detector or cross-locale canonical as a universal repair.

### Scenario 3 — A low-volume specialist problem has Trends `0`
Do not reject it automatically. Check first-party queries/store/support/community evidence, verified product relevance, whether an authoritative resource already exists and lifecycle cost. Trends zero is bounded evidence, not proof of zero need.

### Scenario 4 — Search impressions rise but downloads do not
Do not call this an SEO or UX failure from aggregate metrics alone. Segment query/page/locale, identify the landing task, check whether store handoff is appropriate and measurable, then hand observed task evidence to UX/Content when warranted.

### Scenario 5 — HTTPS product link should open installed app
Do not replace the web URL with a custom scheme by default. Determine whether web and native content truly correspond, establish verified iOS/Android association, preserve browser fallback, validate route parameters and test installed/uninstalled behavior.

---

## 6. Stage 6 competency gate

### Foundation
PASS — can explain crawler/index/canonical, metadata/content, structured data, localization, webmaster evidence, demand/query evidence and verified app-link concepts without collapsing them.

### Practitioner
PASS — can diagnose representative discovery/index/locale/query problems, choose the correct evidence source, define contracts/ledgers, reject keyword-volume folklore and specify cross-platform validation.

### Advanced
NOT CLAIMED. Requires real production evidence, broader search-result/store/social measurement, migration/lifecycle cases and cross-domain performance/security/analytics knowledge from later stages.

### Expert judgment
NOT CLAIMED. Requires actual MintTap/app portfolio facts and longitudinal operational evidence.

**Stage 6 integration result: PASS at intended FOUNDATION/PRACTITIONER level.**

---

## 7. Design Studio / Content / UX dependencies

Latest canonical relationship retained from STATUS:
- Web Design has Stage 1 PASS / Stage 2 practice evidence, but true HTTP/direct-entry/network breadth remains relevant production validation;
- Content Design is user-managed and has current foundation/source-literacy work in Design Studio;
- UX is user-managed.

### Web Design handoff
A future real route harness should expose the HTTP/rendering/link contract needed to join browser/runtime truth with crawler/search evidence. App-link implementation adds installed/uninstalled deep-entry and fallback states but does not replace normal web route validation.

### Content Design handoff
Provide observed query language, page/task context and result-representation evidence as inputs. Do not order interface wording from search volume. Social-preview copy must remain truthful to the canonical product/content source.

### UX handoff
Provide evidence when direct search/social/deep-link arrivals fail orientation, continuation or task completion. Search metrics alone are not UX proof.

No Design Studio canonical file is edited by this block.

---

## 8. OPEN MintTap production facts
- actual `minttap.app` deployed route/content/locale inventory;
- rendering/router/hosting architecture;
- robots/sitemap/canonical/redirect state;
- Search Console/Bing ownership and evidence;
- App Store/Google Play acquisition/search evidence;
- actual iOS bundle/team IDs and Android package/signing fingerprints needed for association;
- AASA/assetlinks deployment state;
- which web resources should map to native routes;
- installed/uninstalled/authenticated fallback policy;
- social platforms actually used and preview requirements;
- web→store/app attribution and downstream task evidence;
- content/translation/lifecycle owners.

Do not infer these from generic patterns.

---

## 9. Stage 6 closure
Stage 6 is complete at the roadmap's intended FOUNDATION/PRACTITIONER curriculum level. Production search quality is not claimed.

Reusable Stage 6 system:
1. Search Discovery Evidence Contract;
2. Search Content Intent Contract;
3. Structured Data Evidence Contract;
4. International Search / Locale Contract;
5. Search Operations Evidence Ledger;
6. Search Opportunity Record;
7. cross-platform public-URL/app-continuation validation layer.

## Next highest-value block
066 — **Stage 7 Web Performance Foundations: Navigation Lifecycle, Critical Rendering Path, Resource Loading, Main-Thread/Rendering Work & Perceived Readiness.**

Begin Stage 7 from first principles before Core Web Vitals optimization. Understand where time is spent from navigation through usable/rendered state, then layer metrics and budgets on top.