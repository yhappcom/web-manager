# 007 — Localization Architecture for minttap.app

Status: FOUNDATION / architecture baseline established; production validation still required
Date: 2026-09-14
Scope: Korean + English first, scalable to additional locales

## Question

How should `minttap.app` structure language variants so that website navigation, App Store / Google Play metadata, privacy/support/account-control content, screenshots, accessibility, SEO and future language expansion remain coherent?

## RELATED DOMAIN CHECK

### Typography / Type
- `yhappcom/design-studio/progress/TYPE_STATUS.md` currently lists systematic Latin/Korean fallback, mixed-script vertical metrics, long labels and browser/device proof as unresolved.
- Reuse: localization must not assume translated strings have the same width, wrapping, line-height, fallback or numeral behavior.
- Transfer need: real Korean/English browser specimens must later validate typography, wrapping and fallback.

### Web Design
- Web Design owns complete page systems, responsive behavior and real browser validation.
- Reuse: localization must be treated as a real page-system condition, not only a string-substitution layer.

### Layout / Interaction
- Localized labels can change navigation, controls, forms, support flows and error states.
- Transfer need: narrow widths, long labels and locale switching require layout/interaction validation.

### Accessibility
- Study 006 already requires correct document language metadata and accessible, consistent support/account-control flows.

### Overlap decision
This study establishes MintTap-specific localization architecture and operations. It does not claim browser typography or responsive PASS; those remain Design Studio / implementation validation dependencies.

---

## SOURCE — HTML document language

W3C Internationalization guidance states that an HTML page should declare its default language with the `lang` attribute on the `html` element. Language values follow BCP 47. When content inside a page changes language, the relevant element should declare the different language.

Primary sources:
- https://www.w3.org/International/questions/qa-html-language-declarations.html
- https://www.w3.org/International/docs/bp-html-lang/

### MINTTAP DECISION

Every localized HTML document must declare its actual primary language.

Initial values:
- Korean page: `<html lang="ko">`
- English page: `<html lang="en">`

Use a more specific BCP 47 tag only when region/script distinctions materially affect the content, for example `en-US`, `en-GB`, `zh-Hans`, or `zh-Hant`.

Do not use locale-specific tags merely because a market exists; region variants must represent a real content or linguistic distinction.

---

## SOURCE — separate URLs for separate language versions

Google Search recommends different URLs for different language versions rather than changing a single URL based on cookies, browser settings, IP location or `Accept-Language`.

Google also warns that automatic language redirects may prevent users and crawlers from reaching every language version. It recommends explicit links between language versions.

Primary sources:
- https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- https://developers.google.com/search/docs/specialty/international/locale-adaptive-pages

### MINTTAP DECISION — language-specific URLs

MintTap user-facing content will use stable, crawlable locale-specific URLs.

Preferred scalable pattern:

- `/ko/...`
- `/en/...`

Examples:
- `/ko/apps/<app-slug>/`
- `/en/apps/<app-slug>/`
- `/ko/apps/<app-slug>/support/`
- `/en/apps/<app-slug>/support/`
- `/ko/apps/<app-slug>/privacy/`
- `/en/apps/<app-slug>/privacy/`
- `/ko/apps/<app-slug>/account-deletion/`
- `/en/apps/<app-slug>/account-deletion/`

This supersedes the earlier unprefixed paths as the preferred structure for localized human-facing documents. The underlying information hierarchy from Study 002 remains unchanged.

### OPEN — root `/` behavior

Do not finalize `/` until the public audience and primary-language strategy are confirmed.

Two acceptable candidates remain:

1. language-neutral entry / selector that acts as `x-default`, or
2. a deliberate default-language home page with equivalent locale links.

Do not implement invisible IP/browser-language forced redirects as the primary architecture.

Machine-readable infrastructure remains language-neutral unless the platform specification requires otherwise:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

---

## SOURCE — hreflang relationships

Google supports `hreflang` to identify language/region variants. Localized versions should list themselves and all other variants. Google accepts HTML, HTTP header, or sitemap implementation; one correctly maintained method is sufficient.

Primary source:
- https://developers.google.com/search/docs/advanced/crawling/localized-versions

### MINTTAP DECISION

Use HTML `<link rel="alternate" hreflang="…">` initially because:
- relationships remain visible beside the page implementation;
- browser/page QA can inspect them directly;
- the initial site is expected to have a manageable number of locales.

For a Korean/English pair, each page should contain reciprocal annotations for:
- `ko`
- `en`
- `x-default` only after the root/default strategy is deliberately selected.

If the site later grows to many locales or becomes CMS-driven, sitemap-based hreflang may be adopted instead. Do not maintain HTML + sitemap + HTTP hreflang redundantly unless tooling guarantees consistency.

### VALIDATION

For every localized pair:
- self-reference exists;
- reciprocal alternate exists;
- URLs return indexable `200` responses;
- annotations point to final canonical URLs, not redirecting URLs;
- no stale language variant remains after deletion/retirement.

---

## SOURCE — canonicalization and language variants

Google states that fully translated pages are separate language versions, while regional variants with substantially the same language/content can require canonicalization plus `hreflang` handling.

Primary sources:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization
- https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting

### MINTTAP DECISION

A genuinely translated Korean page must not canonicalize to its English counterpart, and vice versa.

Default rule:
- Korean page self-canonicalizes to its Korean URL.
- English page self-canonicalizes to its English URL.
- `hreflang` connects the variants.

Cross-language canonicalization is prohibited unless a specific exceptional duplicate-content case is reviewed.

---

## SOURCE — App Store localization

Apple App Store Connect allows localized app metadata. App Store metadata language is distinct from localization of the app binary. Apple also allows localized app name, description/keywords and privacy policy URL. Screenshots can be localized.

Primary sources:
- https://developer.apple.com/help/app-store-connect/manage-app-information/localize-app-information
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations
- https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information

## SOURCE — Google Play localization

Google Play Console supports translated store listings and localized graphic assets. When a user's language preference matches an added translation, the translated listing is shown.

Primary source:
- https://support.google.com/googleplay/android-developer/answer/9844778

### SYNTHESIS — website locale and store locale are separate release surfaces

A website translation does not mean the corresponding App Store / Google Play localization exists, and store localization does not mean the app binary itself is translated.

Therefore three states must be tracked independently:

1. app UI/binary locale support;
2. store-listing locale support;
3. `minttap.app` locale support.

### MINTTAP DECISION — Locale Matrix

Each app receives a **Locale Matrix** with at least:

| Field | Meaning |
| --- | --- |
| localeTag | BCP 47-style internal locale identifier |
| appUiSupported | app binary/UI translated and validated |
| websiteSupported | localized web content exists |
| appleMetadataSupported | App Store metadata localization exists |
| googleMetadataSupported | Google Play listing translation exists |
| screenshotsLocalized | locale-specific screenshots approved |
| privacyLocalized | privacy content exists and is current |
| supportLocalized | support content exists and is current |
| deletionLocalized | deletion/data-control content exists if applicable |
| reviewer | human reviewer/owner |
| sourceVersion | product/app version the translation reflects |
| lastReviewedAt | freshness checkpoint |

No channel may imply that the app itself supports a language merely because marketing/store/web copy has been translated.

---

## Translation source-of-truth model

### MINTTAP DECISION

Localization must consume product facts from the existing **Product Truth Record** and privacy facts from the **App Data Contract**.

Translations are not allowed to invent or reinterpret product behavior.

Add a **Localization Manifest** per app/release containing:

- source locale;
- target locale;
- source content revision;
- translated content revision;
- terminology/glossary version;
- reviewer;
- status: draft / reviewed / approved / stale;
- affected surfaces: web / Apple / Google / screenshots / privacy / support / deletion;
- known exceptions;
- last verified app version.

### Release invalidation triggers

A translation becomes potentially stale when any of the following changes:
- product feature/availability claim;
- subscription/payment wording;
- account behavior;
- privacy/data practice;
- support process;
- deletion workflow;
- app/store name;
- screenshot UI;
- legal entity/contact information;
- material CTA or navigation destination.

---

## Content translation policy by surface

### Marketing/product pages
Localization may adapt wording and hierarchy for natural language and market comprehension, but underlying product claims must remain equivalent to the Product Truth Record.

### Privacy / account control
Meaning must remain substantively equivalent across supported languages. Marketing-style adaptation is inappropriate where it can change rights, obligations, data categories, retention/deletion behavior or contact instructions.

### Support
Troubleshooting steps must reflect the UI language/version users actually see. If the app UI is not localized into a language, translated support must not pretend that localized in-app labels exist.

### Screenshots
Localized screenshots must have version/platform/locale provenance in the existing Screenshot Evidence Set. Do not reuse an English screenshot under translated captions where the resulting presentation falsely implies the app UI itself is localized.

---

## Language switcher behavior

### MINTTAP DECISION

A language switcher should:
- use normal hyperlinks to equivalent locale URLs;
- preserve the current page/task when an equivalent translation exists;
- fall back to the target-language app/home index only when the exact page does not exist, and make the fallback understandable;
- identify language choices by language names understandable to users (for example `한국어`, `English`), not flag icons alone;
- not auto-redirect users away from a manually selected language;
- be keyboard accessible and remain usable under zoom/reflow.

### OPEN

Remembering a manually selected locale in a cookie/local storage value may improve convenience, but must not make alternate locale URLs inaccessible or non-crawlable. Implementation details remain for later Web Design/engineering validation.

---

## Typography and layout stress requirements

Because the Design Studio Type program still lacks systematic Latin/Korean mixed-script/browser proof, no fixed typography assumption is promoted here.

Production validation must include:
- Korean and English navigation labels;
- long support article titles;
- privacy/legal paragraphs;
- button/CTA expansion;
- breadcrumbs;
- form labels and errors;
- dates, currencies, percentages and version strings;
- mixed Latin ticker/app names inside Korean content;
- font loading failure/fallback;
- 200% text enlargement;
- 320 CSS px-equivalent reflow.

Layout must adapt to content; translators must not be forced to shorten text merely to preserve a fixed visual box.

---

## Search/indexing rules

For every supported locale page:
- unique indexable URL;
- localized visible main content, not only localized navigation/footer;
- localized `<title>` and meta description;
- self canonical;
- reciprocal hreflang;
- correct `<html lang>`;
- internal links point to the intended locale where possible;
- XML sitemap includes only canonical, indexable URLs;
- no locale is hidden behind JavaScript-only switching or login.

---

## Locale launch gate

A locale is not considered `LIVE` merely because translation files exist.

Minimum launch gate:

1. Locale Matrix completed.
2. Product Truth / App Data Contract revision linked.
3. Core web pages translated and human-reviewed.
4. Privacy/support/deletion coverage verified for applicable apps.
5. Correct `lang`, title, metadata, canonical and hreflang.
6. Language switcher path tested.
7. Store localization state explicitly recorded (including unsupported state).
8. Screenshots do not misrepresent UI localization.
9. Broken-link and fallback behavior tested.
10. Keyboard, zoom/reflow and responsive tests completed.
11. Long-label / Korean-English typography stress test completed.
12. Release Manifest updated.

### BLOCKER examples
- translated privacy page materially contradicts the App Data Contract;
- locale claims UI language support that the released app does not have;
- localized account-deletion instructions cannot be completed;
- Korean and English variants canonicalize incorrectly to one language;
- broken/one-way hreflang that points to nonexistent or redirected variants;
- automatic locale redirect prevents a user from remaining on a manually chosen language;
- screenshots imply localized UI that is not shipped.

---

## CHANGE WATCH

Periodically recheck:
- Apple App Store Connect supported localizations and metadata behavior;
- Google Play translation/localization behavior;
- Google Search internationalization/hreflang/canonical guidance;
- W3C/IETF language-tag guidance when new locale/script needs arise.

---

## OPEN items

- Final root `/` behavior and `x-default` destination.
- Whether English or Korean is the source-authoring locale for each app/company content stream.
- Exact initial website/store locale coverage per app.
- Translation tooling/vendor/workflow.
- Human reviewer ownership and approval SLA.
- Whether localized support content will share one knowledge-base system or app-specific repositories.
- Locale-aware date/number/currency formatting implementation.
- Real browser Korean/English typography/fallback validation.
- Jurisdiction-specific legal translation/review requirements.

---

## HANDOFFS TO DESIGN STUDIO

### Typography / Type
MintTap now has an explicit Korean/English validation context: navigation, app names, privacy/support text, forms, breadcrumbs, numerical data and 200%/320px stress cases. This can serve as a future real-web transfer context for Latin/Korean fallback research.

### Web Design
Future production design should test the language switcher, locale-prefixed route system, long-label responsive composition, missing-translation fallback and `hreflang`/canonical output in actual browsers.

### Layout / Interaction
Language switching must preserve orientation/current task where possible, and localized text growth must drive responsive recomposition rather than truncation-by-default.

## Result

Foundation localization architecture is established. Production PASS remains blocked on real content, actual app locale inventory, browser/layout/type validation, store-console implementation and human translation review.
