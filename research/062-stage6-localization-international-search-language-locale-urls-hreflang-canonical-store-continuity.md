# 062 — Stage 6: Localization & International Search — Language/Locale URLs, hreflang, Canonical Interaction, Store Continuity & Multilingual Content Quality

Date: 2026-09-16  
State: **PASS — FOUNDATION/PRACTITIONER**

## Why this block now
059 established discovery/index/canonical mechanics, 060 page meaning/content quality, and 061 entity/structured-data boundaries. Locale architecture comes next because URL identity, alternate relationships and translation ownership are structural and costly to retrofit. Keyword tooling is downstream.

## Source set — authoritative primary sources
- Google Search Central, *Localized Versions of your Pages*: https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Search Central, *Managing Multi-Regional and Multilingual Sites*: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Google Search Central, *Overview of International and Multilingual Site Topics*: https://developers.google.com/search/docs/specialty/international
- Google Search Central, *Canonicalization*: https://developers.google.com/search/docs/crawling-indexing/canonicalization
- Google Search Central, *Consolidate duplicate URLs*: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google Search Central Blog, *How x-default can help you*: https://developers.google.com/search/blog/2023/05/x-default
- Apple Developer, *App Store localizations*: https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations
- Apple Developer, *Localize app information*: https://developer.apple.com/help/app-store-connect/manage-app-information/localize-app-information
- Apple Developer, *Localization*: https://developer.apple.com/localization/
- Google Play Console Help, *Translate and localize your app*: https://support.google.com/googleplay/android-developer/answer/9844778?hl=en

Policy/platform details were rechecked 2026-09-16 and are CHANGE WATCH.

---

## 1. First-principles model

`market/user need → language/region content decision → stable locale URL → truthful localized main content → internal discovery → canonical identity → alternate-locale graph → crawler interpretation → locale-appropriate search result → deep entry/orientation → store handoff → app/store/web content continuity → lifecycle maintenance`

International search is not a translation plugin problem. It combines resource identity, content adaptation, search annotations and cross-channel product truth.

### Vocabulary
- **multilingual**: content exists in multiple languages.
- **multi-regional**: content targets users in different countries/regions; variants may share a language.
- **localization**: translation plus adaptation to linguistic/cultural/market context.
- **internationalization (i18n)**: engineering/content structure that makes localization feasible.
- **hreflang**: Google's supported annotation for relationships among localized variants; not a language detector and not a redirect mechanism.
- **canonical**: representative URL preference for duplicate/substantially duplicate resources.

---

## 2. SOURCE — distinct URLs are the robust search unit
Google documents localized page variants as URLs connected through hreflang. Google may fail to crawl/index all locale-adaptive content when the same URL returns different content according to perceived country or preferred language. Google also states that it determines page language algorithmically rather than using `hreflang` or HTML `lang` as its language detector.

### SYNTHESIS
For indexable MintTap content, **locale is normally part of resource identity, not merely runtime presentation state**. A stable URL per materially localized version gives crawling, linking, sharing, canonicalization, diagnostics and deep entry a concrete object.

### MINTTAP DIRECTION
Do not choose automatic same-URL locale adaptation as the primary architecture for important Company/Product/Support/Governance search surfaces. Preserve explicit locale URLs and a visible user-controlled language switch. Exact URL pattern (`/ko/`, `/en/`, etc.) remains OPEN until actual supported locales and routing architecture are verified.

---

## 3. SOURCE — hreflang is an alternate graph, not a magic locale tag
Google supports hreflang via HTML, HTTP headers or XML sitemap and states that the methods are equivalent for Search; maintaining all three gives no Search benefit and can increase management error. Each variant should reference itself and the other variants; return links are required for reliable interpretation. URLs should be fully qualified. Language uses ISO 639-1; optional region uses ISO 3166-1 Alpha 2. `x-default` can designate the fallback for unmatched language/region settings.

### Critical boundaries
`hreflang ≠ language detection ≠ canonicalization ≠ redirect ≠ translation quality ≠ indexing guarantee`

A URL path that says `/ko/` does not itself prove Korean main content. An `hreflang="ko"` declaration does not repair English body content. `x-default` is not a substitute for deciding what fallback experience users actually receive.

### Failure modes
- one-way annotations without return links;
- wrong codes or country-only codes;
- linking locale A to an unrelated page in locale B;
- hreflang graph and canonical graph contradicting each other;
- generating annotations for translations that do not exist or are stale;
- maintaining HTML + sitemap + headers independently until they drift.

### MINTTAP DIRECTION
Choose one primary hreflang implementation mechanism during production architecture, generate it from the same locale-route inventory as navigation/sitemap, and test reciprocity. Use `x-default` only after the fallback behavior is explicitly defined.

---

## 4. SOURCE — canonical and hreflang solve different problems
Google documents same-language regional duplicates as a case where canonicalization and hreflang can be used together. Google also notes that different-language pages are considered duplicates only when the main content remains untranslated; translating only boilerplate while leaving the body unchanged can therefore collapse intended distinctions.

### SYNTHESIS
For genuinely translated Korean and English pages, the normal conceptual model is **each locale URL has its own resource identity and self-consistent canonical**, while hreflang expresses equivalence across language variants. Cross-locale canonicalization should not be used casually to erase a legitimate translated page.

For same-language regional near-duplicates, canonical and hreflang require deliberate coordination because the two signals answer different questions: representative duplicate vs appropriate locale alternative.

### VALIDATION
For every locale cluster inspect:
1. HTTP status and redirects;
2. indexability;
3. main-content language;
4. self/intended canonical;
5. hreflang reciprocity;
6. internal language-switch links;
7. sitemap inclusion if used;
8. Google-selected canonical and indexed locale evidence when available.

---

## 5. Locale selection and redirects
A user's language preference is not equivalent to geography, citizenship or App Store territory. Search crawlers may not exercise locale-adaptive behavior like a human user.

### SYNTHESIS
A language suggestion may improve convenience; a hard redirect can destroy deep-entry predictability and make diagnosis harder. A user who explicitly selects a locale should normally retain control rather than being repeatedly overridden by inference.

### MINTTAP DIRECTION
Prefer stable locale URLs plus user choice. Any automatic redirect/suggestion policy must be separately justified and validated for crawlers, direct links, browser language, unsupported locales, back navigation and persisted preference. Do not infer this policy from store territory alone.

---

## 6. Multilingual content quality: translation is not merely string substitution
Google's people-first guidance from 060 remains controlling: a localized page must satisfy the user's need. Search annotations cannot compensate for weak translation, missing market-specific instructions or stale product facts.

### Localization quality contract
For each localized page verify:
- same underlying product/company truth where truth is universal;
- deliberate differences where law, store availability, support channel, pricing or market behavior differs;
- natural terminology used by the target audience;
- localized title, heading, metadata, navigation, alt text and support instructions where appropriate;
- screenshots/media do not contradict the locale;
- dates/numbers/currency/units are correctly formatted rather than blindly translated;
- legal/privacy text has an accountable owner and is not treated as casual marketing translation;
- untranslated fallback is explicit rather than silently mixed into the page.

### OPEN
MintTap's actual supported web/app/store locales, translation owner, terminology glossary, legal-localization process and review capability are not yet verified.

---

## 7. App Store / Google Play continuity is related but not identical to web locale architecture
### SOURCE — Apple
Apple currently allows localized App Store metadata across supported languages/locales; display can depend on App Store location, device language settings, localizations supplied and the primary language. Apple distinguishes App Store metadata localization from localizing the app binary. Apple also supports localized screenshots/app previews. In March 2026 Apple announced expansion to 50 supported App Store localizations.

### SOURCE — Google Play
Google Play Console supports localized store listings in a documented set of languages/locales and provides translation/localization workflows. The locale code inventory is platform-specific and must be checked rather than assumed to equal web hreflang codes.

### SYNTHESIS
`web locale ≠ App Store localization ≠ app-binary locale ≠ Google Play listing locale`

They should share product truth and terminology, but they are separate publication systems with different locale inventories, fallback behavior, assets and lifecycle.

### MINTTAP DIRECTION — Locale Continuity Matrix
Maintain one cross-channel matrix:

| Concept | Web | iOS app | App Store | Android app | Google Play |
|---|---|---|---|---|---|
| supported locale | verify | verify | verify | verify | verify |
| product/app name | truth source | truth source | localized metadata | truth source | localized listing |
| feature terminology | glossary | glossary | listing copy | glossary | listing copy |
| screenshots/media | web evidence | runtime | store assets | runtime | store assets |
| support/privacy URL | locale destination | in-app link | listing field | in-app link | listing field |
| availability/price claim | market evidence | market evidence | store truth | market evidence | store truth |

A missing localization in one channel does not justify pretending it exists in another. Web pages should not promise a localized in-app experience that the shipped app does not provide.

---

## 8. New reusable artifact — International Search / Locale Contract
For each localized resource cluster record:

1. page/resource ID;
2. purpose and source-of-truth owner;
3. language + optional region target;
4. stable URL;
5. actual main-content language;
6. intended canonical;
7. hreflang cluster and implementation mechanism;
8. x-default/fallback behavior if any;
9. internal locale-switch path;
10. automatic redirect/suggestion behavior if any;
11. localized title/H1/meta and media state;
12. support/privacy/store outbound destination by locale;
13. iOS/Android binary locale availability;
14. App Store/Google Play localization availability;
15. translation/review owner and glossary version;
16. HTTP/crawler/index evidence;
17. stale-content/retirement trigger;
18. CHANGE WATCH date for platform-specific locale rules.

This extends the 059 Search Discovery Evidence Contract, 060 Search Content Intent Contract and 061 Structured Data Evidence Contract rather than replacing them.

---

## 9. Design Studio dependency / handoff
Latest `yhappcom/design-studio/progress/WEB_STATUS.md` checked 2026-09-16: Web Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED; W016 actual Chromium native/custom transfer 14/14. True HTTP direct-entry/reload/404, W015 real Fetch/DOM/network, W011 icon runtime, actual browser-UI zoom and broader browser/device/AT/human evidence remain OPEN.

### Web Design handoff
Future representative route transfer should add at least two locale variants and test:
- direct entry/reload per locale URL;
- localized title/H1/body identity;
- canonical + hreflang consistency;
- crawlable language-switch links;
- preserved deep page when switching locale where an equivalent exists;
- explicit fallback when an equivalent does not exist;
- long localized labels and text expansion;
- no locale inference that traps navigation or overrides explicit user choice.

### Type handoff
Production locale expansion requires actual Korean/Latin typography, punctuation, numerals, fallback and long-label validation. Web Manager owns language/content truth; Type owns typographic evidence.

### Layout/Interaction handoff
Language switching, fallback, text expansion and localized navigation must preserve task continuity and hierarchy. Locale switching is a navigation/state problem as well as content.

### Color
No new Color-specific dependency introduced. Existing state/non-color cue requirements remain applicable.

No Design Studio canonical file was edited.

---

## 10. Verified facts vs synthesis vs open questions
### VERIFIED / SOURCE
- Google supports HTML, HTTP header or sitemap hreflang methods; variants must include self/alternate relationships and reciprocal links.
- Google does not use hreflang or HTML `lang` as its page-language detector.
- Locale-adaptive same-URL pages can leave locale content uncrawled/unindexed.
- Canonical and hreflang are distinct mechanisms; same-language regional duplicates may use both.
- Apple App Store metadata localization and app-binary localization are separate systems.
- Apple and Google Play maintain their own supported localization inventories and publication behavior.

### SYNTHESIS / MINTTAP DIRECTION
- Treat locale as stable resource identity for important indexable surfaces.
- Prefer explicit locale URLs and user-controlled switching over opaque same-URL adaptation.
- Generate search annotations from a single locale-route truth source.
- Maintain cross-channel terminology/product-truth continuity without forcing identical locale inventories.
- Do not claim a localized app experience merely because a localized web/store page exists.

### OPEN
- MintTap/LogMate web locales and target markets;
- exact locale URL scheme and fallback URL;
- whether regional variants beyond language variants are justified;
- app binary locale support on each platform;
- App Store/Google Play listing localizations and exact store URLs;
- translation/review ownership and legal-content workflow;
- production router/server redirect behavior;
- Search Console indexed locale/canonical/hreflang evidence.

---

## 11. Competency check
The Web Manager should now be able to diagnose separately:
- translation-quality failure;
- URL/discovery failure;
- canonical conflict;
- hreflang graph failure;
- locale-switch UX failure;
- crawler locale-adaptation failure;
- store/web/app localization mismatch;
- stale localized content.

**Gate result: PASS — Foundation/Practitioner.** Production implementation remains OPEN until actual MintTap locale, route, app/store and crawler evidence exists.

## Highest-value next block
**063 — Search Measurement & Webmaster Operations: Search Console/Bing Webmaster Tools, Index Coverage, URL Inspection, Sitemaps, Query/Page Evidence & Diagnostic Workflow.**

Reason: 059–062 now define what should exist. The next prerequisite is learning how to observe what search engines actually crawled, indexed, selected and served before moving into keyword/performance optimization.