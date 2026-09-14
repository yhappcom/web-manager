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
- Established a **Product Truth Record**, **Screenshot Evidence Set** and **Content Release Manifest**.
- Separated product truth from channel-specific expression so website/store copy may differ without factual contradiction.
- Defined localization synchronization and release discrepancy severity (`BLOCKER`, `HIGH`, `NORMAL`).
- Canonical study: `research/004-store-website-content-synchronization.md`.

### 005 — Domain, Hosting & Security Baseline
- Established a provider-independent production contract before choosing hosting/CDN.
- Set modern transport direction: HTTPS only, TLS 1.2 minimum, TLS 1.3 enabled where supported, staged HSTS.
- Established exact no-redirect handling for Apple AASA and Android `assetlinks.json` endpoints.
- Classified `.well-known` and `app-ads.txt` as launch-critical machine-readable operational surfaces with direct status/MIME/cache monitoring.
- Defined cache classes for immutable assets, human-facing HTML/policy/support content and verification files.
- Established initial browser security-header direction: CSP, HSTS, `X-Content-Type-Options`, explicit Referrer Policy and Permissions Policy.
- Added DNSSEC as recommended once operational ownership is mature; CAA after certificate provider selection.
- Defined hosting/CDN acceptance gates, CI/CD secret rules, rollback/observability requirements and post-deploy checks.
- Provisional canonical production origin remains `https://minttap.app/`.
- Canonical study: `research/005-domain-hosting-security-baseline.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — evidence base expanding**

Reading alone does not constitute completion. Policy findings require launch-time revalidation. Architecture and security findings require implementation against a real provider, browser/device validation, external endpoint checks and tested rollback before production PASS.

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

### Machine-readable launch infrastructure
- `/.well-known/apple-app-site-association` — when Apple associated domains are used; direct HTTPS 200/no redirect.
- `/.well-known/assetlinks.json` — when Android App Links are used; direct HTTPS JSON 200/no redirect.
- `/app-ads.txt` — when advertising verification is used.

### Internal truth/control artifacts
- **App Data Contract** — actual data collection, SDK/processors, purposes, sharing, retention/deletion and account behavior.
- **Product Truth Record** — current public product capabilities, availability, identity, support/privacy/store destinations and technical confirmation.
- **Screenshot Evidence Set** — version/platform/locale/feature provenance for public screenshots.
- **Content Release Manifest** — release-by-release impact checklist for web/store/privacy/support/localization/assets/infrastructure.

Exact machine-readable storage formats remain OPEN.

## Security / infrastructure baseline

- Canonical origin direction: `https://minttap.app/`.
- TLS 1.0/1.1 prohibited; TLS 1.2 minimum; TLS 1.3 preferred/enabled where supported.
- Ordinary HTTP routes redirect to HTTPS.
- HSTS introduced only after HTTPS coverage is verified; `includeSubDomains`/preload are later operational decisions.
- AASA and `assetlinks.json` are served directly at every associated hostname and never satisfied through canonical-host redirects.
- CSP should be introduced in report-only/testing form when needed, then enforced after dependency inventory.
- `X-Content-Type-Options: nosniff` and explicit Referrer Policy are baseline response controls.
- Permissions Policy should deny unnecessary powerful browser features.
- DNSSEC is recommended when registrar/DNS ownership and rollover procedures are mature.
- CAA follows actual certificate-provider selection.
- Deployment secrets do not belong in Git; CI/CD must use least privilege and auditable secret storage.
- Production host selection must support exact `.well-known` paths, custom headers/status/cache control, rollback and monitoring.

## Cross-surface BLOCKER examples

- privacy/data disclosure mismatch;
- non-existent feature claimed as shipped;
- broken required support/privacy/deletion URL;
- materially wrong account/subscription explanation;
- wrong store destination;
- misleading screenshot of core functionality;
- broken AASA / `assetlinks.json` when app routing depends on them;
- expired/invalid production TLS certificate;
- deployment that cannot be safely rolled back after a launch-critical regression.

## Important open items

- Exact MintTap legal entity/public contact details are not yet recorded.
- Exact app inventory, versions and account-creation behavior are not yet mapped.
- Exact SDKs, analytics, ads, authentication providers, processors and data flows are not yet mapped.
- App Data Contract / Product Truth Record / Release Manifest storage schemas are not yet selected.
- Store-console ownership and release approval roles are not yet documented.
- Registrar, authoritative DNS, hosting/CDN and certificate issuer are not yet documented/selected.
- Current DNSSEC/CAA state of `minttap.app` is not yet audited.
- Universal/App Link route sets are not yet defined.
- Final CSP and cache TTLs depend on implementation/provider choices.
- Monitoring/incident-response provider and alert owner remain undefined.
- Korean/English locale architecture and localization owner/reviewer roles are not yet selected.
- Screenshot capture/approval workflow is not yet defined.
- Support SLA/escalation and deletion backend workflows remain app-specific and undefined.

## Next research queue

1. **Accessibility production baseline: semantic HTML, keyboard/focus, zoom/reflow, landmarks, forms and status/error behavior.**
2. Localization architecture for Korean/English first, with future-locale scalability.
3. SEO, social sharing, structured data, sitemaps, canonicalization and crawlability.
4. Company/app marketing content model: proof, screenshots, feature hierarchy, trust and conversion without overclaiming.
5. Operational checklist for release, policy change watch, broken links, verification files and freshness monitoring.
6. Jurisdiction-specific legal/compliance web requirements when entity information, launch regions and actual app data practices are known.
7. Compare real hosting/DNS/CDN implementation options only after the baseline is sufficient to evaluate them against explicit gates.

## Current Design Studio dependencies

- **Web Design**: complete page systems, semantic implementation, responsive navigation, browser/device validation, CSP/resource implications and implementation-aware specification.
- **Layout/Interaction**: navigation/wayfinding, state, focus, destructive confirmation, errors/recovery and responsive recomposition.
- **Typography/Type**: Korean/English hierarchy, legal/support reading density, font loading/fallback, zoom and enlarged text.
- **Color**: focus/current/destructive-state semantics, contrast, forced-color behavior, themes and browser/device conditions.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–005.
- Future completed studies must update this file before moving to a materially different research block.
