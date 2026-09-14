# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager owns MintTap company website content, app-launch web requirements and the operational consistency of public web surfaces. Production implementation has not yet been assigned; the current priority is building a reliable professional baseline that can later drive provider selection and implementation.

When no live MintTap web task is pending, self-directed study continues. Every substantial block is saved in this repository and this status is updated before moving to a materially different topic.

## Completed foundation studies

### 001 — App Launch Website Foundations
Established Apple/Google launch requirements covering privacy, support, account deletion, app↔web association, advertising verification and launch-time policy revalidation.

### 002 — Multi-App Company Website Information Architecture
Established company → apps → support/control/governance hierarchy, durable per-app pages and baseline URL/navigation principles.

### 003 — Privacy, Support & Account-Deletion Content Architecture
Established per-app privacy/support/account-deletion surfaces and an **App Data Contract** that reconciles actual app/backend/SDK behavior with Apple App Privacy, Google Data safety and website disclosures.

### 004 — Store ↔ Website Content Synchronization
Established a **Product Truth Record**, **Screenshot Evidence Set** and **Content Release Manifest**. Store and website copy may differ in expression but may not contradict the same product truth.

### 005 — Domain, Hosting & Security Baseline
Established a provider-independent production contract: HTTPS/TLS baseline, staged HSTS, exact no-redirect Apple/Android association endpoints, cache classes, security-header direction, DNSSEC/CAA guidance, secret handling, rollback and monitoring requirements.

### 006 — Accessibility Production Baseline
Adopted WCAG 2.2 AA as the internal web production target and established semantic HTML, keyboard/focus, reflow, text enlargement, forms/errors/status, target geometry and automated+manual validation gates.

### 007 — Localization Architecture
- Established stable language-specific URLs as the preferred scalable pattern: `/ko/...` and `/en/...` initially.
- Each localized page declares its real HTML language, self-canonicalizes and is reciprocally connected using `hreflang`.
- Automatic IP/browser-language redirection is rejected as the primary architecture; users must be able to reach and remain on explicitly selected locale URLs.
- Established a **Locale Matrix** separating app UI support, website localization, Apple metadata, Google metadata, screenshots, privacy/support/deletion coverage and human review state.
- Established a **Localization Manifest** linked to Product Truth / App Data Contract revisions so translations become stale when product/data/support facts change.
- Store-listing localization, website localization and app-binary/UI localization are tracked as separate facts; none implies the others.
- Localized screenshots must not falsely imply that the app UI itself is translated.
- Real Korean/English typography, fallback and long-label browser proof remains OPEN and must use Design Studio Type/Web validation.
- Canonical study: `research/007-localization-architecture.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — architecture/evidence base expanding**

Reading alone is not PASS. Policy findings require freshness checks; architecture/security/accessibility/localization findings require implementation on real pages, browsers, devices, locales and store consoles before production confidence.

## Current public information architecture

Preferred localized human-facing pattern:

- `/ko/`, `/en/` — localized company/home surfaces, final root strategy still OPEN.
- `/ko/apps/`, `/en/apps/` — localized app portfolio.
- `/ko/apps/<app-slug>/`, `/en/apps/<app-slug>/` — localized durable app pages.
- localized `support/`, `privacy/`, and `account-deletion/` child pages as applicable.
- localized company support/privacy/contact/terms resources where substantively available.

Language-neutral machine endpoints:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

### Root `/` remains OPEN
Acceptable candidates:
1. language-neutral/x-default entry or selector; or
2. a deliberate default-language home with explicit alternate-language links.

Do not finalize until primary audience/market strategy is known.

## Internal truth/control artifacts

- **App Data Contract** — actual data collection, SDK/processors, purposes, sharing, retention/deletion and account behavior.
- **Product Truth Record** — current shipped capabilities, identity, availability, account/subscription behavior and destinations.
- **Screenshot Evidence Set** — version/platform/locale/feature provenance.
- **Content Release Manifest** — release impact across web/store/privacy/support/localization/assets/infrastructure/accessibility.
- **Locale Matrix** — app UI vs website vs store metadata vs privacy/support/deletion/screenshot locale coverage.
- **Localization Manifest** — source revision, target locale, glossary/reviewer, approval/staleness and surface coverage.

Exact machine-readable storage schemas remain OPEN.

## Security / infrastructure baseline

- Canonical origin direction: `https://minttap.app/`.
- TLS 1.0/1.1 prohibited; TLS 1.2 minimum; TLS 1.3 where supported.
- Ordinary HTTP redirects to HTTPS.
- HSTS only after complete HTTPS validation.
- AASA and `assetlinks.json` served directly with correct route/content type and no redirect.
- CSP should be inventoried/tested before enforcement; `nosniff`, explicit Referrer Policy and Permissions Policy are baseline directions.
- Deployment secrets stay outside Git; hosting must support auditable deployment, rollback and monitoring.

## Accessibility baseline

- WCAG 2.2 AA internal target.
- Native semantic HTML before custom ARIA widgets.
- Logical page titles/headings/landmarks and bypass mechanism.
- Required functionality keyboard-operable, visible logical focus and no traps/obscuration.
- 320 CSS px-equivalent reflow and 200% text enlargement without loss of content/functionality.
- Persistent programmatic form labels; textual errors and programmatic dynamic status.
- 24×24 CSS px target criterion treated as minimum floor, not preferred design size.
- Correct page language metadata.
- Automated scanners assist but cannot independently produce PASS.

## Localization baseline

- Locale-specific crawlable URLs, not one URL whose language silently varies.
- Initial architecture uses `ko` and `en`; region subtags only when real regional distinctions exist.
- `<html lang>` uses BCP 47-compatible values.
- Each translated page self-canonicalizes; language variants connect through reciprocal `hreflang`.
- User-controlled language switching uses ordinary links and preserves the equivalent current task/page where possible.
- Translation must preserve Product Truth and App Data Contract meaning.
- Privacy/account-control translation prioritizes substantive equivalence over marketing adaptation.
- Support localization must correspond to the UI/version users actually see.
- Korean/English text growth, fallback, wrapping, mixed-script metrics and 200%/320px behavior require real-browser proof.

## Current release blockers model

Examples include:
- privacy/data-disclosure mismatch;
- required support/privacy/deletion URL broken;
- non-existent feature presented as shipped;
- materially incorrect account/subscription instructions;
- misleading screenshots;
- inaccessible launch-critical support/account-control flow;
- association files redirected/malformed when required;
- localized content materially contradicting source product/data truth;
- website/store copy claiming app UI language support that is not shipped;
- broken canonical/hreflang locale relationships on launch-critical localized pages.

## Important open items

- Exact MintTap legal entity/public contact information.
- Exact app inventory, released versions, account behavior and locale support.
- Exact SDK/analytics/ads/auth/processors/data flows.
- Internal artifact storage schemas and release ownership roles.
- Hosting/CDN/DNS/SSL provider selection and real audit.
- Universal/App Link route inventory.
- app-ads.txt publisher/vendor lines.
- Root `/` language/x-default behavior.
- Source-authoring language per content stream.
- Translation tooling/vendor/reviewer workflow and SLA.
- Locale-aware date/number/currency implementation.
- Real Korean/English browser/type/fallback validation.
- Jurisdiction-specific legal/compliance requirements once launch regions and data practices are fixed.

## Current Design Studio dependencies

- **Web Design** — actual localized page systems, language switching, responsive/browser validation and implementation fidelity.
- **Typography / Type** — Korean/English fallback, mixed-script metrics, long labels, wrapping, numerals and zoom/reflow validation.
- **Layout / Interaction** — navigation, locale switching, task preservation, destructive/account-control flows and responsive recomposition.
- **Color** — contrast/state/focus/theme validation in real localized pages.

## Next research queue

1. **SEO / social sharing / structured data / canonical / sitemap / crawlability baseline.**
2. Company/app marketing content model: positioning, feature hierarchy, proof, screenshots, trust and conversion without unsupported claims.
3. Operational release / policy-change / broken-link / verification-file freshness monitoring.
4. Jurisdiction-specific legal/compliance web requirements when entity, markets and data practices are known.
5. Implementation/provider comparison after Foundation evidence is mature enough to score real hosting/CMS/framework candidates.
6. Real-browser Korean/English localization/accessibility/type transfer validation once an implementation exists.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–007.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
