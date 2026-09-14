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
- Set HTTPS-only transport direction, TLS 1.2 minimum, TLS 1.3 where supported and staged HSTS.
- Established exact no-redirect handling for Apple AASA and Android `assetlinks.json` endpoints.
- Classified `.well-known` and `app-ads.txt` as launch-critical operational surfaces requiring exact route/MIME/cache/monitoring control.
- Defined cache classes, browser security-header direction, DNSSEC/CAA guidance, CI/CD secret rules, rollback/observability requirements and hosting/CDN acceptance gates.
- Canonical study: `research/005-domain-hosting-security-baseline.md`.

### 006 — Accessibility Production Baseline
- Adopted **WCAG 2.2 AA** as MintTap's internal web production target, without treating it as a substitute for jurisdiction-specific legal review.
- Established semantic HTML/native-control first principles, logical headings/landmarks and skip/bypass behavior.
- Made complete keyboard operation, logical focus order, visible focus and focus-not-obscured behavior production requirements.
- Added 320 CSS px-equivalent reflow and 200% text enlargement stress tests.
- Treated 24×24 CSS px pointer targets as a minimum floor, not a preferred compact design size.
- Defined accessible form labeling, instructions, grouping, text-based errors, success/failure feedback and programmatic status-message rules.
- Added special destructive-confirmation requirements for account deletion/data-control flows.
- Added correct page language metadata (`ko`, `en` initially) and consistent support/help location requirements.
- Established automated + manual keyboard/zoom/reflow + assistive-technology validation; automated scans alone cannot produce PASS.
- Classified inaccessible launch-critical support/privacy/account-control behavior as release blockers.
- Canonical study: `research/006-accessibility-production-baseline.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — evidence base expanding**

Reading alone does not constitute completion. Policy findings require launch-time revalidation. Architecture, security and accessibility findings require implementation against real pages/providers, browser/device/assistive-technology validation, and tested operational procedures before production PASS.

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
- **Content Release Manifest** — release-by-release impact checklist for web/store/privacy/support/localization/assets/infrastructure/accessibility.

Exact machine-readable storage formats remain OPEN.

## Security / infrastructure baseline

- Canonical origin direction: `https://minttap.app/`.
- TLS 1.0/1.1 prohibited; TLS 1.2 minimum; TLS 1.3 enabled where supported.
- Ordinary HTTP routes redirect to HTTPS.
- HSTS introduced only after HTTPS coverage is verified; `includeSubDomains`/preload are later operational decisions.
- AASA and `assetlinks.json` are served directly at every associated hostname and never satisfied through canonical-host redirects.
- CSP should be tested/report-only where needed, then enforced after dependency inventory.
- `X-Content-Type-Options: nosniff`, explicit Referrer Policy and Permissions Policy are baseline controls.
- DNSSEC is recommended when registrar/DNS ownership and rollover procedures are mature; CAA follows certificate-provider selection.
- Deployment secrets do not belong in Git; CI/CD must use least privilege and auditable secret storage.
- Production host selection must support exact `.well-known` paths, custom headers/status/cache control, rollback and monitoring.

## Accessibility baseline

- WCAG 2.2 AA is the internal default target.
- Native semantic HTML before custom ARIA widgets.
- Meaningful page title, one primary main landmark, coherent heading outline, bypass repeated navigation.
- All required functionality keyboard-operable with no keyboard traps.
- Focus order preserves meaning; visible focus cannot be removed or obscured by sticky/overlay UI.
- Normal vertically scrolling content must survive 320 CSS px-equivalent reflow; text must survive 200% enlargement without loss of content/functionality.
- Form labels are persistent/programmatically associated; placeholder-only labeling is rejected.
- Errors must identify the field/problem in text and provide useful correction guidance when possible.
- Dynamic result/progress/error status must be programmatically exposed without unnecessary focus movement.
- Localized pages declare correct page language.
- Repeated help/support mechanisms stay predictably located.
- Automated accessibility tooling assists testing but does not substitute for human/manual evaluation.

## Cross-surface / release BLOCKER examples

- privacy/data disclosure mismatch;
- non-existent feature claimed as shipped;
- broken required support/privacy/deletion URL;
- materially wrong account/subscription explanation;
- wrong store destination;
- misleading screenshot of core functionality;
- broken AASA / `assetlinks.json` when app routing depends on them;
- expired/invalid production TLS certificate;
- deployment that cannot be safely rolled back after a launch-critical regression;
- launch-critical function cannot be completed by keyboard;
- keyboard trap;
- invisible/fully obscured focus in required flow;
- unlabeled account-deletion/support controls;
- errors only communicated by color or not exposed in text;
- critical status/progress/failure unavailable to assistive technology;
- essential content/function lost at required text enlargement/reflow;
- inaccessible destructive confirmation creating account-deletion risk.

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
- Exact browser/assistive-technology accessibility test matrix is not yet selected.
- Korean/English locale architecture and localization owner/reviewer roles are not yet selected.
- Final accessible contrast tokens and typography/fallback behavior require Design Studio Color/Type/Web validation.
- Screenshot capture/approval workflow is not yet defined.
- Support SLA/escalation and deletion backend workflows remain app-specific and undefined.

## Next research queue

1. **Localization architecture for Korean/English first, with future-locale scalability.**
2. SEO, social sharing, structured data, sitemaps, canonicalization and crawlability.
3. Company/app marketing content model: proof, screenshots, feature hierarchy, trust and conversion without overclaiming.
4. Operational checklist for release, policy change watch, broken links, verification files and freshness monitoring.
5. Jurisdiction-specific legal/compliance web requirements when entity information, launch regions and actual app data practices are known.
6. Compare real hosting/DNS/CDN implementation options after the baseline is sufficient to evaluate options against explicit gates.
7. Define concrete browser/assistive-technology test matrix when implementation stack and audience support policy are chosen.

## Current Design Studio dependencies

- **Web Design**: complete page systems, semantic implementation, responsive navigation, real-browser validation, CSP/resource implications and implementation-aware specification.
- **Layout/Interaction**: navigation/wayfinding, target geometry, focus, destructive confirmation, status/errors/recovery and responsive recomposition.
- **Typography/Type**: Korean/English hierarchy, legal/support reading density, line wrapping, font loading/fallback, zoom and enlarged text.
- **Color**: text/non-text/focus contrast, state semantics, color-independent feedback, themes and forced-color/browser/device behavior.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–006.
- Future completed studies must update this file before moving to a materially different research block.
