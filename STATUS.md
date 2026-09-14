# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The web manager has been appointed as the owner of MintTap's company website content and app-launch web requirements. Production site work has not yet been assigned; current priority is building a reliable professional foundation.

When no live MintTap web task is pending, self-directed professional study continues without a separate order. Each substantial completed block must be saved here, with `STATUS.md` updated before moving to a materially different topic.

## Completed foundation work

### 001 — App Launch Website Foundations
- Confirmed Design Studio governance and the Web Design specialist's integration role.
- Confirmed that MintTap-specific website decisions belong here while reusable design research remains in `yhappcom/design-studio`.
- Established the first app-launch requirement map covering Apple, Google Play, privacy, support, account deletion, app↔web association and advertising verification.
- Canonical study: `research/001-app-launch-website-foundations.md`.

### 002 — Multi-App Company Website Information Architecture
- Established a scalable company → app → support/control/governance hierarchy for `minttap.app`.
- Adopted stable first-class per-app canonical pages instead of unrelated landing pages.
- Established provisional path patterns such as `/apps/<app-slug>/`, app support/privacy/account-deletion child resources when needed, plus company-level support/privacy/contact layers.
- Established shallow primary-navigation guidance: Apps, Support and Company/About only when meaningful; legal/utility resources do not automatically belong in primary navigation.
- Added baseline URL rules: lowercase, readable semantic slugs, hyphens, no public opaque IDs, no version numbers in permanent app URLs, and deliberate redirects for renamed/retired paths.
- Integrated current W3C/WAI navigation/page-structure guidance and Google Search URL/site-structure/SoftwareApplication guidance.
- Canonical study: `research/002-multi-app-information-architecture.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — evidence base expanding**

Reading alone does not constitute completion. Policy findings require source tracking and launch-time revalidation. Design/IA findings require representative browser, accessibility, responsive and localization validation before production PASS.

## Current requirement map

### Launch-critical / policy-facing
- Company/product website on `minttap.app`.
- Public privacy policy URL.
- Apple Support URL with real contact information.
- Google Play support/contact website presence.
- External account-deletion web resource for Google Play when an app allows account creation.
- Privacy disclosures synchronized with Apple App Privacy and Google Play Data safety declarations.

### Platform/domain infrastructure when used
- Apple `apple-app-site-association` for Universal Links / associated domains.
- Android `/.well-known/assetlinks.json` for verified App Links.
- Root `app-ads.txt` when app advertising inventory requires it; not universally mandatory, but strongly recommended by Google AdMob.

### Baseline information architecture
- `/` — company/home.
- `/apps/` — app portfolio/index.
- `/apps/<app-slug>/` — durable canonical app page.
- `/apps/<app-slug>/support/` — app-specific support when justified.
- `/apps/<app-slug>/privacy/` — when app-specific privacy scope is required.
- `/apps/<app-slug>/account-deletion/` — when applicable.
- `/support/` — company support hub/routing.
- `/privacy/` — company/global privacy surface when applicable.
- `/contact/` — stable company contact route.
- `/terms/` — when applicable.
- Infrastructure endpoints remain outside ordinary user navigation.

### Company/product web surfaces still to study deeply
- Home/company positioning and trust signals.
- Per-app product/marketing content model.
- Support/help/FAQ taxonomy.
- Contact and escalation model.
- Privacy/terms/legal content architecture.
- Account/data-control request UX.
- App Store / Google Play download destinations.
- Localization architecture and language routing.
- Accessibility production requirements.
- SEO/search previews/social metadata.
- Release/update/freshness ownership.

## Important open items

- Exact MintTap legal entity/public contact details are not yet established in this repository.
- Exact app inventory and which apps create accounts are not yet mapped here.
- Exact analytics, advertising SDKs, authentication providers, data collection and third-party processors are not yet mapped.
- Hosting/CDN/SSL/DNS implementation has not yet been selected or audited.
- Universal/App Link routes are not yet defined.
- `app-ads.txt` publisher/vendor lines cannot be finalized until monetization vendors and IDs are known.
- Jurisdiction-specific legal pages beyond store/platform requirements need separate legal/compliance review when launch regions are fixed.
- Locale architecture for Korean/English and future languages is not yet selected.
- Final primary-navigation labels and product naming/slugs depend on actual app portfolio and Design Studio validation.

## Next research queue

1. Privacy/support/account-deletion page content architecture and consistency controls.
2. Apple/Google store metadata ↔ website content synchronization and release ownership.
3. Domain/hosting/security baseline for `minttap.app`.
4. Accessibility production baseline: semantic HTML, keyboard/focus, zoom/reflow, landmarks, forms and status/error behavior.
5. Localization architecture for Korean/English first, with future-locale scalability.
6. SEO, social sharing, structured data, sitemaps, canonicalization and crawlability for app/company pages.
7. Company/app marketing content model: proof, screenshots, feature hierarchy, trust and conversion without overclaiming.
8. Operational checklist for release, policy change watch, broken links, verification files and freshness monitoring.

## Current Design Studio dependencies

- **Web Design**: complete page systems, responsive navigation, browser/device validation and implementation-aware specification.
- **Layout/Interaction**: navigation/wayfinding, state, focus, responsive recomposition and support/account-control flows.
- **Typography/Type**: real browser hierarchy, Korean/English line wrapping, fallback, legal/support density, zoom and enlarged text.
- **Color**: focus/current-state semantics, surface hierarchy, contrast, themes and device/browser behavior.

## Persistence state

- `AGENTS.md` now contains the autonomous continuous-learning directive.
- Future completed studies must update this file before the manager advances to a materially different research block.
