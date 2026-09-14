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

### 003 — Privacy, Support & Account-Deletion Content Architecture
- Revalidated current Apple App Store and Google Play policy requirements from primary platform sources.
- Confirmed per-app privacy-policy requirements and the need to synchronize policy content with actual data/SDK behavior and store disclosures.
- Established `/apps/<app-slug>/privacy/` as MintTap's preferred canonical app privacy-policy pattern, separate from website/company privacy scope.
- Confirmed that Google requires an external web account-deletion resource for account-creating apps and that Apple requires in-app account deletion while allowing/expecting a direct web completion path when the workflow goes to the web.
- Established `/apps/<app-slug>/account-deletion/` as a durable first-class resource for every MintTap app that enables account creation.
- Established `/apps/<app-slug>/support/` as the preferred Apple Support URL / Google website-support destination for each app.
- Defined a single internal **App Data Contract** to reconcile app/client behavior, backend behavior, SDKs/processors, privacy policy, Apple App Privacy, Google Data safety, account deletion and support metadata.
- Defined privacy-impact release triggers and production validation gates.
- Jurisdiction-specific privacy law remains a separate dependency and must not be inferred from platform policy alone.
- Canonical study: `research/003-privacy-support-account-deletion-architecture.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — evidence base expanding**

Reading alone does not constitute completion. Policy findings require source tracking and launch-time revalidation. Design/IA findings require representative browser, accessibility, responsive and localization validation before production PASS. The privacy/support/deletion architecture remains below PASS until applied to at least one real MintTap app and reconciled against actual client/backend/SDK behavior.

## Current requirement map

### Launch-critical / policy-facing
- Company/product website on `minttap.app`.
- Public per-app privacy policy URL for every released app.
- Privacy-policy link/content accessible from inside each app as required by Apple/Google policy.
- Apple Support URL with real, operational contact information.
- Google Play app support email; app-specific support website strongly preferred by MintTap and recommended by Google.
- External account-deletion web resource for Google Play when an app allows account creation.
- In-app account deletion for Apple apps that support account creation.
- Privacy disclosures synchronized with Apple App Privacy and Google Play Data safety declarations.

### Platform/domain infrastructure when used
- Apple `apple-app-site-association` for Universal Links / associated domains.
- Android `/.well-known/assetlinks.json` for verified App Links.
- Root `app-ads.txt` when app advertising inventory requires it; not universally mandatory, but strongly recommended by Google AdMob.

### Baseline information architecture
- `/` — company/home.
- `/apps/` — app portfolio/index.
- `/apps/<app-slug>/` — durable canonical app page.
- `/apps/<app-slug>/support/` — preferred app-specific support destination.
- `/apps/<app-slug>/privacy/` — canonical app-specific privacy policy.
- `/apps/<app-slug>/account-deletion/` — account-creating apps.
- `/support/` — company support hub/routing.
- `/privacy/` — website/company privacy surface when applicable; not a substitute for clearly scoped per-app policies.
- `/contact/` — stable company contact route.
- `/terms/` — when applicable.
- Infrastructure endpoints remain outside ordinary user navigation.

### Internal operating model now established
- Maintain one App Data Contract per app.
- Reconcile technical behavior, SDK/processors, web privacy policy, Apple App Privacy, Google Data safety, deletion flow and support metadata before release.
- Treat new SDKs, analytics/ads, authentication, data fields/permissions, processing/sharing, retention/deletion, subscriptions and contact changes as disclosure-review triggers.
- Store-policy requirements are CHANGE WATCH items and must be rechecked at launch.

### Company/product web surfaces still to study deeply
- Home/company positioning and trust signals.
- Per-app product/marketing content model.
- Support/help/FAQ taxonomy and operational escalation.
- Contact and support response model.
- Jurisdiction-specific privacy/terms/legal content architecture.
- App Store / Google Play download destinations.
- Localization architecture and language routing.
- Accessibility production requirements.
- SEO/search previews/social metadata.
- Release/update/freshness ownership.

## Important open items

- Exact MintTap legal entity/public contact details are not yet established in this repository.
- Exact app inventory and which apps create accounts are not yet mapped here.
- Exact analytics, advertising SDKs, authentication providers, data collection and third-party processors are not yet mapped.
- App Data Contract storage format is not yet selected.
- Hosting/CDN/SSL/DNS implementation has not yet been selected or audited.
- Universal/App Link routes are not yet defined.
- `app-ads.txt` publisher/vendor lines cannot be finalized until monetization vendors and IDs are known.
- Jurisdiction-specific legal pages beyond store/platform requirements need separate legal/compliance review when launch regions and app data practices are fixed.
- Locale architecture for Korean/English and future languages is not yet selected.
- Final primary-navigation labels and product naming/slugs depend on actual app portfolio and Design Studio validation.
- Support SLA/escalation and account-deletion backend workflows remain app-specific and undefined.

## Next research queue

1. Apple/Google store metadata ↔ website content synchronization and release ownership.
2. Domain/hosting/security baseline for `minttap.app`.
3. Accessibility production baseline: semantic HTML, keyboard/focus, zoom/reflow, landmarks, forms and status/error behavior.
4. Localization architecture for Korean/English first, with future-locale scalability.
5. SEO, social sharing, structured data, sitemaps, canonicalization and crawlability for app/company pages.
6. Company/app marketing content model: proof, screenshots, feature hierarchy, trust and conversion without overclaiming.
7. Operational checklist for release, policy change watch, broken links, verification files and freshness monitoring.
8. Jurisdiction-specific legal/compliance web requirements when actual launch regions, entity information and app data practices are known.

## Current Design Studio dependencies

- **Web Design**: complete page systems, responsive navigation, browser/device validation and implementation-aware specification.
- **Layout/Interaction**: navigation/wayfinding, state, focus, destructive confirmation, errors/recovery, responsive recomposition and support/account-control flows.
- **Typography/Type**: real browser hierarchy, Korean/English line wrapping, fallback, legal/support density, zoom and enlarged text.
- **Color**: focus/current-state/destructive-state semantics, surface hierarchy, contrast, themes and device/browser behavior.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–003.
- Future completed studies must update this file before the manager advances to a materially different research block.
