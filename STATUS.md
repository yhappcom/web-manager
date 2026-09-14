# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The web manager owns MintTap company website content and app-launch web requirements. Production site work has not yet been assigned; current priority is building a reliable professional foundation.

When no live MintTap web task is pending, self-directed professional study continues without a separate order. Each substantial completed block must be saved here, with `STATUS.md` updated before moving to a materially different topic.

## Completed foundation work

### 001 — App Launch Website Foundations
- Established the first Apple/Google app-launch requirement map covering privacy, support, account deletion, app↔web association, advertising verification and release-time revalidation.
- Canonical study: `research/001-app-launch-website-foundations.md`.

### 002 — Multi-App Company Website Information Architecture
- Established a scalable company → app → support/control/governance hierarchy for `minttap.app`.
- Adopted durable first-class per-app pages and baseline URL/navigation rules.
- Canonical study: `research/002-multi-app-information-architecture.md`.

### 003 — Privacy, Support & Account-Deletion Content Architecture
- Revalidated current Apple App Store and Google Play policy requirements from primary sources.
- Established per-app canonical privacy, support and account-deletion URL patterns.
- Defined an internal **App Data Contract** to reconcile client/backend/SDK behavior with web privacy content, Apple App Privacy, Google Data safety and deletion/support surfaces.
- Defined disclosure-review triggers and production validation gates.
- Canonical study: `research/003-privacy-support-account-deletion-architecture.md`.

### 004 — App Store / Google Play ↔ Website Content Synchronization
- Confirmed Apple and Google requirements that store metadata, screenshots and descriptions accurately reflect the real app.
- Established a **Product Truth Record** as the upstream source for app identity, shipped capabilities, account/subscription behavior, availability, privacy/support URLs and screenshot evidence.
- Separated **product truth** from **channel-specific expression** and **temporary campaign content** so copy may differ without factual contradiction.
- Defined a version-linked **Screenshot Evidence Set** and **Content Release Manifest**.
- Established localization synchronization rules and release discrepancy severity (`BLOCKER`, `HIGH`, `NORMAL`).
- Clarified responsibility: Product/Engineering confirms technical truth; Web Manager owns `minttap.app` content/freshness and cross-surface discrepancy detection; store-console publication remains with the assigned console owner unless separately delegated.
- Canonical study: `research/004-store-website-content-synchronization.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — evidence base expanding**

Reading alone does not constitute completion. Policy findings require launch-time revalidation. IA/content models require application to a real MintTap app, browser/accessibility/localization validation and post-publication verification before PASS.

## Current operating model

### Public website structure
- `/` — company/home.
- `/apps/` — app portfolio/index.
- `/apps/<app-slug>/` — durable canonical app page.
- `/apps/<app-slug>/support/` — preferred app-specific support destination.
- `/apps/<app-slug>/privacy/` — canonical app privacy policy.
- `/apps/<app-slug>/account-deletion/` — account-creating apps.
- `/support/` — company support routing hub.
- `/privacy/` — website/company privacy scope when applicable.
- `/contact/` — company contact route.
- `/terms/` — when applicable.

### Internal truth/control artifacts
- **App Data Contract** — actual data collection, SDK/processors, purposes, sharing, retention/deletion and account behavior.
- **Product Truth Record** — current public product capabilities, availability, identity, support/privacy/store destinations and technical confirmation.
- **Screenshot Evidence Set** — version/platform/locale/feature provenance for public screenshots.
- **Content Release Manifest** — release-by-release impact checklist for web/store/privacy/support/localization/assets.

Exact machine-readable formats are still OPEN.

### Cross-surface rule

Website, App Store and Google Play copy do **not** need identical wording. They must not contradict the same underlying product truth.

BLOCKER examples:
- privacy/data disclosure mismatch;
- non-existent feature claimed as shipped;
- broken required support/privacy/deletion URL;
- materially wrong account/subscription explanation;
- wrong store destination;
- misleading screenshot of core functionality.

## Current requirement map

### Launch-critical / policy-facing
- Public privacy policy for every released app.
- Required in-app privacy access/disclosures.
- Apple Support URL with operational contact information.
- Google Play support email; app-specific website preferred.
- Google external account-deletion resource for account-creating apps.
- Apple in-app account deletion for apps supporting account creation.
- Apple App Privacy / Google Data safety / website policy aligned to actual technical behavior.
- Store descriptions, screenshots and claims aligned to actual released functionality.

### Platform/domain infrastructure when used
- Apple `apple-app-site-association`.
- Android `/.well-known/assetlinks.json`.
- Root `app-ads.txt` when advertising inventory requires it.

## Important open items

- Exact MintTap legal entity/public contact details are not yet recorded.
- Exact app inventory, versions and account-creation behavior are not yet mapped.
- Exact SDKs, analytics, ads, authentication providers, processors and data flows are not yet mapped.
- App Data Contract / Product Truth Record / Release Manifest storage schemas are not yet selected.
- Store-console ownership and release approval roles are not yet documented.
- Hosting/CDN/SSL/DNS implementation has not yet been selected or audited.
- Universal/App Link routes are not yet defined.
- `app-ads.txt` publisher/vendor lines cannot be finalized until monetization vendors and IDs are known.
- Jurisdiction-specific legal requirements need separate review once launch regions and app data practices are known.
- Korean/English locale architecture and localization owner/reviewer roles are not yet selected.
- Screenshot capture/approval workflow is not yet defined.
- Support SLA/escalation and deletion backend workflows remain app-specific and undefined.

## Next research queue

1. **Domain/hosting/security baseline for `minttap.app`.**
2. Accessibility production baseline: semantic HTML, keyboard/focus, zoom/reflow, landmarks, forms and status/error behavior.
3. Localization architecture for Korean/English first, with future-locale scalability.
4. SEO, social sharing, structured data, sitemaps, canonicalization and crawlability.
5. Company/app marketing content model: proof, screenshots, feature hierarchy, trust and conversion without overclaiming.
6. Operational checklist for release, policy change watch, broken links, verification files and freshness monitoring.
7. Jurisdiction-specific legal/compliance web requirements when entity information, launch regions and actual app data practices are known.

## Current Design Studio dependencies

- **Web Design**: complete page systems, responsive navigation, browser/device validation and implementation-aware specification.
- **Layout/Interaction**: navigation/wayfinding, state, focus, destructive confirmation, errors/recovery and responsive recomposition.
- **Typography/Type**: Korean/English hierarchy, legal/support reading density, line wrapping, fallback, zoom and enlarged text.
- **Color**: focus/current/destructive-state semantics, contrast, surface hierarchy, themes and browser/device behavior.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–004.
- Future completed studies must update this file before moving to a materially different research block.
