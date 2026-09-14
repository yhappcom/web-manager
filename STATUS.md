# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager owns MintTap company website content, app-launch web requirements and the operational consistency of public web surfaces. Production implementation has not yet been assigned. Current priority is completing a defensible Foundation that can drive actual technology/provider selection and later production validation.

When no live MintTap web task is pending, self-directed study continues. Every substantial block is saved in this repository and this status is updated before moving to a materially different topic.

## Completed foundation studies

1. **001 App Launch Website Foundations** — privacy/support/account deletion, app↔web association, advertising verification and policy revalidation.
2. **002 Multi-App Information Architecture** — company → apps → app → support/control/governance hierarchy and durable URL/navigation rules.
3. **003 Privacy / Support / Account Deletion** — per-app surfaces and App Data Contract.
4. **004 Store ↔ Website Synchronization** — Product Truth Record, Screenshot Evidence Set, Content Release Manifest.
5. **005 Domain / Hosting / Security** — HTTPS/TLS, verification files, caching, security headers, DNS, secrets, rollback/monitoring contract.
6. **006 Accessibility Production Baseline** — WCAG 2.2 AA internal target, semantic HTML, keyboard/focus, reflow, text enlargement, forms/status, manual validation.
7. **007 Localization Architecture** — `/ko/` and `/en/`, HTML language, reciprocal hreflang, Locale Matrix, Localization Manifest.
8. **008 SEO / Structured Data / Crawlability** — canonical, robots, sitemap, conservative schema and Search Console.
9. **009 SEO Independent Verification / Social Preview** — route indexability classes, robots vs noindex, localized title/meta and Open Graph baseline.
10. **010 Company / App Marketing Content Model** — Claim Registry, evidence/screenshots, feature hierarchy, trust/store CTA, price/subscription and stale-claim controls.
11. **011 Operational Release & Change-Watch Controls** — continuous operational verification, Policy Change Register, Operational Surface Registry, deploy/scheduled/event/human watch layers, release gates, incident severity and ownership continuity.

Canonical details remain in `research/001...011`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — architecture / policy / operations baseline substantially established**

Reading alone is not PASS. Policy, architecture, security, accessibility, localization, search/social, marketing and operational controls require implementation on real pages, stores, devices, browsers and production systems before production confidence.

## Current public information architecture

Preferred localized human-facing pattern:
- `/ko/`, `/en/` — localized company/home surfaces; final root strategy remains OPEN.
- `/ko/apps/`, `/en/apps/` — app portfolio.
- `/ko/apps/<app-slug>/`, `/en/apps/<app-slug>/` — durable app pages.
- localized app `support/`, `privacy/`, `account-deletion/` child pages as applicable.
- localized company support/privacy/contact/terms resources where substantively available.

Language-neutral machine endpoints:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

Root `/` remains OPEN between a language-neutral/x-default entry and a deliberate default-language home.

## Internal truth / control artifacts

- **App Data Contract** — actual data collection, SDK/processors, purposes, sharing, retention/deletion and account behavior.
- **Product Truth Record** — shipped capabilities, identity, availability, account/subscription behavior and official destinations.
- **Screenshot Evidence Set** — app/platform/version/locale/feature provenance and staleness.
- **Claim Registry** — material marketing claims, evidence, approved locale expression, owner, expiry/invalidation state and surfaces using them.
- **Content Release Manifest** — release impact across web/store/privacy/support/localization/assets/infrastructure/accessibility/search/social/marketing.
- **Locale Matrix** — app UI vs website vs store metadata vs privacy/support/deletion/screenshot locale coverage.
- **Localization Manifest** — source revision, target locale, reviewer, approval/staleness and surface coverage.
- **Policy Change Register** — policy source, announcement/effective dates, impact, owner, action, severity and verification status.
- **Operational Surface Registry** — production URL/console surface, expected behavior, owner, monitoring method/cadence, last validation, severity and runbook.

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
- Logical page title/headings/landmarks and bypass mechanism.
- Full keyboard operation, visible logical focus, no traps/obscuration.
- 320 CSS px-equivalent reflow and 200% text enlargement without loss of content/functionality.
- Persistent programmatic form labels; textual errors and programmatic dynamic status.
- Automated scanners assist but cannot independently produce PASS.

## Localization / search / marketing baseline

- Locale-specific crawlable URLs; `ko` and `en` initially.
- Each translated page self-canonicalizes and uses reciprocal `hreflang`.
- App UI, website and store localization remain separate facts.
- Public pages default to discoverable/indexable unless a documented reason exists.
- `robots.txt` is not secrecy/access control and is not a reliable de-indexing tool by itself.
- Sitemap contains final canonical indexable URLs only.
- Structured data describes only real visible facts; no fabricated ratings/reviews/pricing/entity data.
- Social previews must align with Product Truth / Screenshot Evidence / locale support.
- Marketing facts derive from Product Truth/App Data Contract/evidence; copy does not create facts.
- High-risk claims require evidence/provenance and invalidation rules.
- Screenshots/videos represent real current product or are clearly labeled as concept/future.

## Operational release / change-watch baseline

### Policy watch

- Apple App Review Guidelines, Developer News changes and Upcoming Requirements are watched sources.
- Google Play Policy Announcements, Policy Deadlines and Policy Archive are watched sources.
- Search Central documentation updates are a watched feed.
- Applicable Android App Links / AdMob app-ads documentation becomes watched when those features are active.

A source change triggers relevance assessment; it does not automatically create a product change.

### Monitoring layers

1. **Deploy-time validation** — critical URL, redirect, Privacy/Support/Deletion, store destination, verification files, robots/noindex/canonical/hreflang, accessibility smoke and evidence approval.
2. **Scheduled synthetic checks** — critical URLs/machine endpoints hourly-or-better when monitoring exists; TLS/certificate and store-link/site-metadata sanity on an appropriate recurring schedule.
3. **Event-driven watches** — App Store Connect webhooks, Play policy communications, Search update feed, deployments/releases, SDK/data/auth/ads changes and claim/screenshot invalidation.
4. **Human freshness review** — full affected-app review before every app release; weekly policy/deadline review; monthly evidence/content parity review; quarterly ownership/access/alert continuity review.

These cadences are MintTap operating defaults, not platform-mandated intervals.

### Propagation-aware validation

- AASA origin success does not mean immediate Apple CDN/device convergence; Apple documents CDN request timing and roughly weekly device refresh after install.
- Android App Links require actual domain verification, and Android tooling supports forced re-verification for testing.
- app-ads.txt origin correctness is separate from AdMob recognition, which may take days and sometimes longer.
- Search indexing/social preview cache delays are not automatically release blockers when production origin/configuration is correct and the propagation delay is understood.

### Release close condition

A release is not operationally complete merely because the deployment or store review succeeded.

Post-release validation checks actual live store destinations, website CTA, released product/support/privacy/deletion alignment, changed deep links, production canonical/locale metadata, relevant social previews and monitoring/webhook health.

## Incident severity

### P0 — user / distribution critical
Examples: domain/HTTPS outage; required Privacy/Support/Deletion unavailable; material privacy mismatch; wrong critical store destination; broken core deep-link verification; false account-deletion outcome.

### P1 — high
Examples: stale material price/subscription claim; misleading screenshot/claim; material locale contradiction; app-ads origin failure on monetized app; significant canonical/noindex/indexing configuration error; broken notification path with no fallback owner.

### P2 — normal
Examples: non-critical social preview stale; minor search title quality issue; non-material help article staleness with a correct current support route.

Severity follows user/policy/distribution impact, not visual prominence.

## Current release blockers model

Includes:
- privacy/data-disclosure mismatch;
- required support/privacy/deletion URL broken;
- unshipped feature presented as current;
- materially incorrect account/subscription/price instructions;
- misleading/stale critical screenshots or claims;
- inaccessible launch-critical support/account-control flow;
- required AASA/App Links broken or malformed;
- DNS/TLS/production host failure;
- localized content materially contradicting Product Truth;
- website/store/social claim of app UI locale support that is not shipped;
- canonical/hreflang pointing to wrong app/locale/staging target;
- production staging `noindex`/crawl rules;
- fabricated structured-data/marketing evidence;
- wrong/unavailable official store destination.

## Ownership / continuity principle

No launch-critical operational capability may exist only in one person's memory/account.

Production must eventually document ownership/recovery for registrar, DNS/CDN/hosting, Apple Developer/App Store Connect, Google Play Console, policy recipients, Search Console, monitoring alerts, CI/CD, support/privacy inboxes and P0/P1 escalation.

Secrets are never stored in this repository.

## Important open items

- exact MintTap legal entity/public contact information;
- exact app inventory, released versions, pricing, account behavior and locale support;
- exact SDK/analytics/ads/auth/processors/data flows;
- storage schemas for internal control artifacts;
- release approval/console ownership roles;
- hosting/CDN/DNS/CMS/framework/deployment/monitoring provider selection;
- Universal/App Link route inventory;
- actual app-ads.txt use and publisher/vendor lines;
- root `/` locale strategy;
- translation tooling/reviewer workflow;
- locale-aware number/date/currency behavior;
- real Korean/English browser/type/fallback validation;
- Search Console organizational ownership;
- company/group email addresses for policy/alerts;
- App Store Connect webhook receiver/backend;
- escalation SLA/on-call expectations;
- jurisdiction-specific legal/compliance requirements once markets/data practices are fixed.

## Current Design Studio dependencies / handoffs

- **Web Design** — real responsive page systems, operational/error/maintenance states, metadata generation and browser/device production validation. Current Web Design remains Foundation/not yet baselined.
- **Typography / Type** — Korean/English headings, qualifications, support/error/legal strings, wrapping/fallback and zoom/reflow.
- **Layout / Interaction** — CTA priority, support/account-control recovery, maintenance/error/retry, modal/focus/navigation behavior and responsive recomposition.
- **Color** — semantic state/focus/disabled/unavailable behavior and operational notices without mechanically mapping internal severity colors to user-facing semantics.

## Next research queue

1. **Implementation/provider comparison methodology and candidate scoring** — evaluate hosting/CDN/CMS/framework/deployment/monitoring options against Studies 002–011 rather than popularity.
2. Jurisdiction-specific legal/compliance web requirements when entity, launch regions and actual data practices are known.
3. Real-browser Korean/English localization/accessibility/type/search/social/marketing transfer validation once an implementation exists.
4. App-specific user/market evidence when actual product pages are assigned.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–011.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
