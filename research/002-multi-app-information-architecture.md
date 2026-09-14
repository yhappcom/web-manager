# 002 — Multi-App Company Website Information Architecture

Checked: 2026-09-14
Scope: `minttap.app` as the company/developer website for multiple Apple and Android applications.

## Research question

How should `minttap.app` be structured so that it remains understandable, accessible, searchable, and operationally maintainable as MintTap launches multiple apps with different support, privacy, account, store and technical requirements?

## RELATED DESIGN STUDIO CHECK

Design Studio governance and the Web Design, Type, Color, and Layout/Interaction status files were reviewed in the preceding foundation sync.

Reusable findings:
- Web Design is responsible for complete page systems, navigation, wayfinding, responsive composition and browser/device validation.
- Layout/Interaction research establishes that grouping, hierarchy, navigation, state and feedback should be validated as systems rather than as isolated decoration.
- Type and Color findings must later be applied under real web content, localization, zoom, responsive and device conditions.

MintTap-specific IA and operational decisions remain canonical in `yhappcom/web-manager`.

## SOURCE — W3C/WAI navigation and page structure

W3C WAI recommends clear and consistent navigation, more than one way to find content, orientation cues such as clear headings and breadcrumbs, and designs that work across viewport sizes. WAI also emphasizes descriptive titles/headings, predictable navigation and semantic page structure using meaningful regions and headings.

Sources:
- https://www.w3.org/WAI/tips/designing/
- https://www.w3.org/WAI/people-use-web/tools-techniques/navigation/
- https://www.w3.org/WAI/fundamentals/accessibility-principles/
- https://www.w3.org/WAI/curricula/designer-modules/navigation-design/
- https://www.w3.org/WAI/tutorials/page-structure/
- https://www.w3.org/WAI/tutorials/page-structure/headings/
- https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/

### Operational consequence

A multi-app developer website should not force users to infer structure from branding alone. Navigation labels, page titles, headings, current-location cues and semantic regions should expose the information hierarchy directly.

## SOURCE — Google Search site and URL structure

Google Search Central recommends a logical site organization and simple, descriptive, human-readable URLs. Important pages should be linked through relevant internal links. Google also notes that sitelinks are derived algorithmically from site structure, page titles, headings and internal link relationships.

Sources:
- https://developers.google.com/search/docs/crawling-indexing/url-structure
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/sitelinks

Google's breadcrumb documentation states that breadcrumbs communicate a page's position in the site hierarchy and can help users explore upward through that hierarchy.

Source:
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

### Operational consequence

MintTap should prefer stable semantic paths over opaque identifiers or ad-hoc one-off URLs. Site structure should be reflected through internal linking even when the exact breadcrumb presentation is designed separately from the physical URL path.

## SOURCE — App structured data

Google Search supports `SoftwareApplication` structured data and extended application types including `MobileApplication` and `WebApplication`. Supported properties include app name, offer/price information, application category and operating system.

Sources:
- https://developers.google.com/search/docs/appearance/structured-data/software-app
- https://schema.org/SoftwareApplication

### Scope limit

Structured data can improve machine understanding and search eligibility, but it does not replace clear visible product content, navigation or app-store metadata. Search appearance is not guaranteed merely because markup exists.

## SYNTHESIS — Separate company, product, support and governance intents

The first foundation study established that store-facing web requirements serve different intents. A scalable information architecture should therefore distinguish at least four conceptual layers:

1. **Company layer** — who MintTap is and what products it makes;
2. **Product layer** — what each app does, who it is for, core capabilities and store destinations;
3. **Support/control layer** — help, contact, account deletion, data requests and app-specific troubleshooting;
4. **Governance/legal layer** — privacy, terms, notices and policy information whose scope may be company-wide or app-specific.

Machine-readable files such as `apple-app-site-association`, `/.well-known/assetlinks.json` and `app-ads.txt` are infrastructure endpoints and should not be treated as ordinary navigation destinations.

## SYNTHESIS — App identity should be first-class

As the number of apps grows, each app should have a durable canonical identity within the website rather than being represented only by a card on the homepage.

A dedicated app surface enables:
- stable marketing/store URLs;
- app-specific support routing;
- app-specific privacy/account-control links when needed;
- search indexing and sharing metadata;
- structured data;
- release notes or documentation later without changing the top-level model.

## MINTTAP DECISION — Baseline IA direction

Use a company-first, app-centered hierarchy rather than a collection of unrelated landing pages.

Provisional architecture:

```text
minttap.app/
├── apps/
│   ├── <app-slug>/
│   │   ├── support/
│   │   ├── privacy/        # only if app-specific policy is required
│   │   ├── account-deletion/  # when applicable
│   │   └── ...future app-owned resources
│   └── <next-app>/
├── support/
├── privacy/
├── terms/                  # when applicable
├── contact/
├── about/                  # if company narrative warrants a separate page
├── .well-known/
│   └── assetlinks.json     # when Android App Links are used
├── apple-app-site-association  # when Apple associated domains are used
└── app-ads.txt             # when advertising verification is used
```

This is a structural baseline, not a frozen sitemap. Top-level navigation should remain smaller than the full URL tree. Utility/legal/infrastructure destinations do not all belong in the primary navigation.

## MINTTAP DECISION — Primary navigation model

For an early-stage company with a small app portfolio, default primary navigation should be deliberately shallow. Candidate user-facing categories are:

- Apps
- Support
- Company/About only if there is meaningful content

Privacy, terms, contact and other governance links can be exposed consistently through support flows and footer/utility navigation unless a specific user task justifies primary placement.

As the product portfolio grows, the architecture can expand without changing each app's canonical path.

## MINTTAP DECISION — Naming and URL rules

Baseline rules:
- use lowercase canonical paths;
- use short readable English slugs for stable cross-locale canonical resources unless a later localization strategy justifies locale-specific routes;
- use hyphens for multiword slugs;
- do not encode version numbers in permanent product-page URLs;
- avoid opaque numeric IDs for public content;
- do not make fragments (`#...`) the only address for distinct crawlable pages;
- redirect retired/renamed paths deliberately rather than silently duplicating content.

These rules align with current Google Search URL guidance and reduce future migration cost.

## SYNTHESIS — Global support vs app-specific support

`/support/` should function as a support hub and routing surface, while `/apps/<app>/support/` should exist when an app has enough distinct troubleshooting, account, billing, data, import/export or platform-specific content to justify a dedicated support context.

This prevents two opposite failures:
- one generic support page that becomes unusable as apps multiply;
- duplicated independent support silos with no company-level wayfinding.

## SYNTHESIS — Privacy scope must be explicit

A URL hierarchy alone cannot decide whether privacy policy should be global or app-specific. The content model must explicitly identify policy scope.

Possible valid models:
- one company policy covering all apps with clearly separated app-specific sections;
- company-level policy plus app-specific supplements;
- distinct app-specific policies.

The correct choice depends on actual data practices, legal review, third-party processors, account models and launch jurisdictions. The website must make the applicable scope obvious to the user and keep store-console links synchronized with it.

## SYNTHESIS — Navigation must survive accessibility and localization stress

The final navigation/component system must be validated for:
- keyboard-only operation;
- visible focus;
- screen-reader landmarks and meaningful headings;
- narrow mobile widths;
- zoom and enlarged text;
- long Korean/English/localized labels;
- touch and pointer use;
- active/current-page indication;
- footer/utility navigation consistency.

A static desktop sitemap is insufficient evidence that the architecture works.

## SEARCH/DISCOVERABILITY CONSEQUENCE

Each app page should later be eligible for app-specific metadata and structured data rather than concentrating all products on the home page. Candidate implementation includes:
- unique page title and meta description;
- canonical URL;
- Open Graph/social metadata;
- `SoftwareApplication`/`MobileApplication` structured data where valid;
- internal links from the company app index and relevant support/legal pages;
- breadcrumb markup where it reflects a meaningful user path.

Implementation must be validated against then-current Google structured-data requirements.

## OPEN

- Final app inventory is not yet recorded in this repository.
- Product names/slugs are not yet approved.
- It is unknown which apps require separate support centers vs a shared support knowledge base.
- It is unknown whether MintTap will operate Korean and English content as locale subdirectories, negotiated content, or another architecture.
- Company legal identity and contact model are not yet fixed.
- Privacy-policy scope requires actual app data maps and legal/compliance review.
- Search functionality is probably unnecessary at the earliest small-site stage but should be reconsidered as support/docs volume grows.

## VALIDATION

Before production approval, build at least one representative app-page/support flow and validate:
- desktop and narrow mobile navigation;
- keyboard/focus order;
- screen-reader landmark/headings structure;
- long Korean and English labels;
- at least 200% zoom/reflow conditions;
- internal-link integrity;
- canonical/redirect behavior;
- structured-data validation if markup is included.

## HANDOFFS TO DESIGN STUDIO

### Web Design
MintTap will eventually provide a real multi-app site case for complete page-system, navigation, responsive, structured-content and browser validation.

### Layout / Interaction
The proposed company → app → support hierarchy creates a concrete context for navigation, wayfinding, current-location cues, responsive menu behavior and task-flow validation.

### Typography / Type
App names, long localized navigation labels, support headings and dense legal text will create real browser stress cases for hierarchy, line wrapping, fallback and scaling.

### Color
Current-location, focus, link/state and surface hierarchy will provide real semantic-color contexts; color must not be the sole navigation/state indicator.
