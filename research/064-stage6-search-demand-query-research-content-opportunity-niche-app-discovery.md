# 064 — Stage 6: Search Demand, Query Research, Content Opportunity & Niche App Discovery Strategy

Date: 2026-09-16  
State: **PASS — FOUNDATION/PRACTITIONER**

## Why this block now
059–063 established resource identity, truthful page meaning, entity/locale relationships and crawler/index/result observability. Demand research can now be treated as evidence about user language and unmet/served needs rather than as a keyword-volume contest.

This is especially important for a company whose products may serve narrow professional/investment niches: low aggregate volume does not by itself establish low product relevance, while broad high-volume topics do not by themselves justify content production.

## Source set — authoritative primary sources
- Google Search Console Help, *Performance report (Search results): Overview and basic setup*: https://support.google.com/webmasters/answer/7576553
- Google Search Console Help, *Performance report: Common tasks and use cases*: https://support.google.com/webmasters/answer/17010961
- Google Search Console Help, *Performance report: Dimensions and data groupings*: https://support.google.com/webmasters/answer/17011259
- Google Search Console Help, *Performance report: Advanced filtering and comparison*: https://support.google.com/webmasters/answer/17011165
- Google Trends Help, *FAQ about Google Trends data*: https://support.google.com/trends/answer/4365533
- Google Ads Help, *Refine your new keywords in Keyword Planner*: https://support.google.com/google-ads/answer/6325025
- Apple Developer, *App Store Connect Analytics — Acquisition*: https://developer.apple.com/help/app-store-connect-analytics/acquisition/acquisition
- Google Play Console Help, *Understand and grow your app's user base*: https://support.google.com/googleplay/android-developer/answer/9859173
- Google Play Console Help, *Download and export monthly reports*: https://support.google.com/googleplay/android-developer/answer/6135870

Platform/report behavior is **CHANGE WATCH** and was rechecked 2026-09-16.

---

## 1. First-principles model

`real user need → language/query expression → observable demand evidence → intent/task classification → existing authoritative resource? → evidence gap/opportunity → page/content decision → search/store exposure → visit/store-view → task/install outcome → re-observation`

Search demand is not synonymous with keyword volume. A query is an observable expression made in a particular search surface and context. The underlying need may have multiple expressions, may be too rare to appear in a tool, or may occur in web search, App Store search, Google Play search, communities, support channels or direct navigation differently.

### Standing distinction
`user need ≠ query string ≠ tool-reported volume ≠ business relevance ≠ content opportunity ≠ conversion value`

---

## 2. SOURCE — first-party observed queries are bounded but high-value evidence
Google Search Console Performance reports expose queries that caused a site to appear in Google Search, with clicks/impressions and page/country/device/time dimensions. Google also supports query/page filtering and RE2 regular expressions for grouping related strings.

Google explicitly documents two important limitations: some queries are anonymized for privacy, and table data is truncated to important rows; not every query is shown. Therefore an absent query is not proof that no such search occurred.

### SYNTHESIS
Once `minttap.app` has sufficient data, Search Console is evidence of **observed web-search exposure**, not a complete census of market demand. Group query families rather than treating every wording variant as a separate content need.

Useful families include:
- branded/company/app-name queries;
- product/category queries;
- problem/task queries;
- feature/capability queries;
- comparison/alternative queries where factually supportable;
- support/troubleshooting queries;
- governance/trust/privacy queries;
- locale/language variants.

### Failure mode
Creating one page per long-tail wording variation. 060 already established that materially distinct user needs, not keyword variants, justify distinct resources.

---

## 3. SOURCE — Google Trends is relative sampled interest, not absolute niche volume
Google Trends states that it uses a sample of actual Google searches, anonymizes/categorizes/aggregates them, normalizes results by time and geography, then scales them 0–100. It also filters searches made by very few people; low-volume terms can therefore appear as `0`. Statistical noise is most noticeable for low/no-interest queries.

### SYNTHESIS
For niche app markets, `Trends = 0` does **not** mean `demand = 0`. Trends is useful for relative direction, seasonality, geography and comparison when enough data exists. It is weak evidence for deciding that a specialized professional/problem query is worthless merely because the tool suppresses it.

### MINTTAP DIRECTION
Never use a Google Trends zero as a veto on a page that is otherwise justified by verified product capability, user/support need or first-party evidence.

---

## 4. SOURCE — Keyword Planner is an advertising planning tool, not product truth
Google Ads describes Keyword Planner as a tool for discovering/refining keyword ideas for Search campaigns and exposes fields such as average monthly searches and bid ranges. Access to basic keyword-discovery features currently requires completing account setup including billing information.

### SYNTHESIS
Keyword Planner can contribute vocabulary and broad demand estimates, but its primary context is paid Search campaign planning. Its numbers should not be treated as exact organic-search counts, nor should high advertiser competition be equated with high relevance for a MintTap product page.

### Failure mode
`high monthly searches → publish article` is not a valid decision rule.

---

## 5. SOURCE — app-store discovery is a separate evidence surface
Apple App Store Connect Analytics distinguishes acquisition sources including App Store search, App Store browse, app referrer, web referrer and custom campaigns. It supports acquisition-funnel metrics such as impressions, product-page views, downloads and conversion, with territory/device segmentation. Apple notes that App Store search source includes views/downloads from ads in App Store search results, so source totals are not automatically pure organic-search evidence.

Google Play's current store-listing reporting allows analysis by traffic source and search terms. Google documents that low-volume search terms can be grouped into `Other` when reporting thresholds are not met. Google also changed the primary store-listing performance metrics in 2026 toward unique intent clicks rather than successful acquisition outcomes, while legacy metrics remain available in some exports/statistics contexts.

### SYNTHESIS
`web search demand ≠ App Store search demand ≠ Google Play search demand`.

The three surfaces should share product truth and terminology but retain separate observation columns. A phrase that matters in Play search may have weak observable web volume; a support query may matter on Google Search but not store search.

### CHANGE WATCH
Apple/Google store analytics definitions, attribution and privacy thresholds can change. Preserve report date and metric definition with every comparison.

---

## 6. Niche demand requires triangulation, not one-tool authority
For a narrow app category, use an evidence ladder rather than a single volume threshold.

### Evidence classes
1. **Observed first-party behavior** — Search Console query/page data, Play search terms, App Store acquisition-source data, internal support/search data when available.
2. **Platform-relative demand** — Trends direction/seasonality, Keyword Planner estimates, store reporting.
3. **Verified product/user evidence** — recurring support questions, documented workflow problems, research findings, community questions where provenance can be preserved.
4. **Product truth** — an actual capability, limitation, requirement or trust question that users need to understand even if search volume is tiny.
5. **Speculative idea** — plausible topic with no observed need or product justification yet.

### SYNTHESIS
Lower-numbered evidence is not universally “better”; each answers a different question. The important discipline is to label the evidence and avoid converting speculation into measured demand.

---

## 7. Query intent is task classification, not mind reading
A query string does not prove a user's private motive. Intent classification is an operational hypothesis based on wording, result context and observed behavior.

### Reusable intent classes for an app company
- **navigate/entity** — find MintTap/company/app/store/support;
- **understand/problem** — learn a domain/product problem;
- **evaluate** — determine capability, compatibility, privacy, price or fit;
- **act/acquire** — reach store/download/start;
- **support/recover** — solve an error, restore data, import/export, account/data issue;
- **trust/governance** — privacy, support ownership, deletion, security/policy information.

A single query can remain ambiguous. Record `OPEN` rather than forcing one intent.

---

## 8. Content opportunity decision model
A content opportunity exists when there is a defensible user need and MintTap can provide a uniquely useful, truthful resource better than the current site/resource inventory.

### Search Opportunity Record
For each candidate need/query family record:

| Field | Purpose |
| --- | --- |
| need/query family | semantic unit, not spelling variant |
| evidence source + date | provenance |
| surface | Google web / App Store / Play / support / other |
| observed metric | impressions/clicks/search term/source etc. |
| evidence limitation | privacy threshold, sampling, attribution, truncation |
| likely task/intent | hypothesis |
| audience/locale | scope |
| existing MintTap resource | avoid duplication |
| product-truth owner | factual authority |
| unique value/evidence | why MintTap can answer |
| lifecycle/maintenance cost | operational burden |
| acquisition/support/trust role | business/user function |
| downstream success measure | task/install/support resolution |
| decision | create / improve / merge / observe / reject |
| confidence | observed / supported synthesis / speculative |

### Decision principle
Do not calculate a pseudo-scientific numeric SEO score when inputs have incompatible scales and uncertainty. Preserve evidence dimensions and make an explicit reasoned decision.

---

## 9. Content that should often NOT be created
Reject or defer when:
- the topic has volume but little connection to the actual app/user task;
- MintTap has no unique knowledge, product evidence or maintained answer;
- the proposed page merely rewrites an existing page around a keyword variant;
- facts would require expertise/authority the company does not possess;
- content would become stale quickly without an owner;
- the only justification is a third-party tool's volume number;
- a support/product/governance page is the correct solution instead of a blog article.

### SYNTHESIS
For niche products, **coverage quality of the real problem space** is more defensible than publishing breadth. Search is a discovery mechanism for useful product/company resources, not a reason to manufacture an unrelated media business.

---

## 10. Cross-surface discovery model for MintTap-style products
Keep three evidence streams distinct but joinable:

`Web search query → minttap.app landing resource → store referral → store page → app outcome`

`App Store search/browse → product page → download/use`

`Google Play search/explore → store listing → install/open intent/outcome`

Where attribution permits, compare them; where it does not, preserve the boundary rather than inventing end-to-end causality.

### Example diagnostic logic
If web impressions for a problem-query family rise but store referrals do not, inspect whether the landing page's task is informational, whether a store handoff is appropriate, and whether referral measurement is available. Do not assume the page “failed conversion” without those facts.

---

## 11. Design Studio / Content / UX handoffs
Latest Design Studio repository head checked 2026-09-16. Content Design has advanced through CD006 foundation/source-literacy work, while the user currently manages Content Design and UX directly. Web Manager does not assume management of those specialists.

### Content Design handoff
When real query families exist, provide **aggregated, privacy-safe query language and page/task context**, not keyword instructions. Content Design can use this as one evidence source for terminology, comprehension and information needs. Search volume does not dictate interface wording.

### UX handoff
When a search landing page receives qualified visits but downstream task evidence suggests orientation/action problems, hand off the observed landing/task evidence. Do not label it a UX defect from search metrics alone.

### Web Design handoff
Existing Stage 6 runtime dependency remains: representative routes need true HTTP/direct-entry/rendering/crawlable-link evidence. 064 adds that deep-entry pages should orient a user arriving directly from a specific query/need without requiring homepage context.

No Design Studio canonical file is edited here.

---

## 12. OPEN MintTap facts
- actual Search Console query/page history;
- whether sufficient data exists for meaningful branded/non-branded segmentation;
- App Store Connect Analytics access and actual acquisition-source history;
- Google Play Console search-term/store-listing history;
- actual web→store referral instrumentation;
- current product/store terminology and supported locales;
- verified support/community query corpus and privacy constraints;
- actual content inventory and maintenance owners;
- whether MintTap and future apps should share company-level discovery content or maintain app-specific knowledge surfaces.

Do not fabricate keyword targets until these inputs exist.

---

## 13. Competency check
PASS at FOUNDATION/PRACTITIONER if Web Manager can:
1. distinguish user need, query string, tool volume, relevance and opportunity;
2. explain Search Console query-data privacy/truncation limits;
3. explain why Trends `0` is not proof of zero niche demand;
4. use Keyword Planner as bounded advertising-market evidence rather than organic truth;
5. keep web/App Store/Play discovery evidence separate;
6. classify query intent as a hypothesis rather than mind reading;
7. decide create/improve/merge/observe/reject using evidence, product truth and lifecycle cost;
8. hand query-language/task evidence to Content/UX without allowing SEO volume to dictate interface design.

**Result: PASS.**

## Next highest-value block
065 — **Stage 6 Integration: Search/Discovery/Content-Quality Competency Review & Niche App Search Operating System.**

059–064 now cover discovery/index mechanics, truthful content, structured/entity representation, internationalization, webmaster observation and demand/query opportunity. Before Stage 7 Performance/Browser Runtime, integrate these into one diagnostic operating model and test whether Stage 6's foundation/practitioner gate is actually satisfied rather than adding another isolated SEO topic.