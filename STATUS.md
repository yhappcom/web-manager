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
6. **006 Accessibility Production Baseline** — WCAG 2.2 AA internal target, semantic HTML, keyboard/focus, reflow, text enlargement, forms/status and manual validation.
7. **007 Localization Architecture** — `/ko/` and `/en/`, HTML language, reciprocal hreflang, Locale Matrix, Localization Manifest.
8. **008 SEO / Structured Data / Crawlability** — canonical, robots, sitemap, conservative schema and Search Console.
9. **009 SEO Independent Verification / Social Preview** — route indexability classes, robots vs noindex, localized title/meta and Open Graph baseline.
10. **010 Company / App Marketing Content Model** — Claim Registry, evidence/screenshots, feature hierarchy, trust/store CTA, price/subscription and stale-claim controls.
11. **011 Operational Release & Change-Watch Controls** — continuous verification, Policy Change Register, Operational Surface Registry, deploy/scheduled/event/human watch layers, release gates, incident severity and ownership continuity.
12. **012 Implementation / Hosting Provider Comparison Methodology** — static-first architecture, provider hard gates, weighted comparison, Firebase Hosting / Cloudflare Workers / Vercel / Netlify assessment and POC-before-selection rule.

Canonical details remain in `research/001...012`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — core architecture / policy / operations / implementation-selection baseline established**

Reading alone is not PASS. Policy, architecture, security, accessibility, localization, search/social, marketing, operational and provider-selection conclusions require real implementation and transfer validation before production confidence.

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
- Social previews align with Product Truth / Screenshot Evidence / locale support.
- Marketing facts derive from Product Truth/App Data Contract/evidence; copy does not create facts.
- High-risk claims require evidence/provenance and invalidation rules.
- Screenshots/videos represent real current product or are clearly labeled as concept/future.

## Operational release / change-watch baseline

### Policy watch
- Apple App Review Guidelines, Developer News and Upcoming Requirements are watched sources.
- Google Play Policy Announcements, Policy Deadlines and Policy Archive are watched sources.
- Search Central documentation updates are a watched feed.
- Android App Links / AdMob app-ads documentation is watched when those features are active.

### Monitoring layers
1. deploy-time deterministic validation;
2. scheduled synthetic checks for critical URLs/machine endpoints/TLS/store destinations/search configuration;
3. event-driven watches such as App Store Connect webhooks, Play policy communications, Search update feed and product/data/provider changes;
4. human freshness review before releases and on weekly/monthly/quarterly governance rhythms.

### Release close condition
A release is not operationally complete merely because deployment or store review succeeded. Post-release checks confirm live store destination, website CTA, current Product Truth/Privacy/Support/Deletion alignment, changed deep links, production metadata and monitoring health.

## Incident severity

- **P0 — user/distribution critical:** domain/HTTPS outage, required policy/control URL unavailable, material privacy mismatch, wrong critical store destination, broken core deep-link association, false deletion outcome.
- **P1 — high:** stale material pricing/claim/screenshot, material locale contradiction, monetization verification failure, significant search/canonical/noindex error, broken notification path with no fallback.
- **P2 — normal:** non-critical social preview/search-copy/help-content issue without material product/control impact.

## Current implementation architecture direction

### Preferred architecture envelope

**Git-versioned content/data → build-time static generation → global HTTPS/CDN hosting → isolated dynamic functions only where a real workflow requires server execution.**

Current content/legal/support/app-marketing surfaces do not justify universal SSR or a persistent application server.

### Provider hard gates
A production host must support:
- apex custom domain + managed TLS;
- exact direct `.well-known` and root machine files;
- route-specific content type/cache/security headers;
- redirects/rewrites without breaking verification paths;
- preview/test deploys;
- version traceability and fast rollback;
- Git/CI workflow;
- locale/static metadata/sitemap/robots output;
- monitoring/log inspection and safe secret handling for optional dynamic functions.

### Preliminary provider shortlist

1. **Firebase Hosting** — current simplest strong static-first fit; managed CDN/TLS, custom headers/rewrites, preview channels, rollback, optional Functions/Cloud Run escape hatch.
2. **Cloudflare Workers + Static Assets** — strongest control/flexibility alternative; excellent headers/routing/versioning/rollback, but Workers custom-domain adoption ties authoritative DNS to Cloudflare and increases platform surface.
3. **Vercel** — fully capable; becomes more compelling if a justified Next.js/SSR/full-stack requirement appears.
4. **Netlify** — mature viable static alternative, but no current MintTap requirement makes it clearly superior to the top two.

No provider is selected yet.

### POC-before-selection rule

Firebase Hosting and Cloudflare Workers should host the same minimum specimen before final selection:
- Korean/English home + app page;
- privacy/support/account-deletion pages;
- AASA / assetlinks / app-ads sample;
- sitemap/robots;
- custom 404;
- security headers;
- canonical/hreflang/Open Graph;
- controlled redirect;
- preview + rollback test.

Selection follows transfer validation, not documentation comparison alone.

### Framework/content direction

- Prefer Git-reviewable content as canonical source.
- Prefer static HTML/lightweight SSG or static-capable component framework.
- Adopt full-stack SSR only after a concrete server-rendering requirement exists.
- Do not choose Next.js/Nuxt/Remix/etc. solely because a hosting vendor optimizes for it.

Exact static generator/framework/CMS remains OPEN pending Design Studio Web requirements and authoring needs.

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

No launch-critical operational capability may exist only in one person's memory/account. Production must eventually document ownership/recovery for registrar, DNS/CDN/hosting, Apple Developer/App Store Connect, Google Play Console, policy recipients, Search Console, monitoring, CI/CD, support/privacy inboxes and P0/P1 escalation. Secrets are never stored here.

## Important open items

- exact MintTap legal entity/public contact information;
- exact app inventory, released versions, pricing, account behavior and locale support;
- exact SDK/analytics/ads/auth/processors/data flows;
- storage schemas for internal control artifacts;
- release approval/console ownership roles;
- final hosting/CDN/DNS/framework/CMS/deployment/monitoring selection;
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
- provider pricing/plan/access-control assumptions at implementation time;
- jurisdiction-specific legal/compliance requirements once markets/data practices are fixed.

## Current Design Studio dependencies / handoffs

- **Web Design** — actual page/component complexity, responsive states, interaction/runtime requirements and proof of whether any surface genuinely needs SSR; production browser/device validation.
- **Typography / Type** — Korean/English headings, support/error/legal strings, mixed-script wrapping/fallback and zoom/reflow in the future POC.
- **Layout / Interaction** — navigation, support/account-control recovery, maintenance/error/retry and responsive recomposition in the future POC.
- **Color** — semantic state/focus/disabled/unavailable behavior and real browser surface validation.

## Next research queue

1. **Jurisdiction-specific legal/compliance scope map** only to the extent it can be researched without inventing MintTap entity/market/data facts; mark application as conditional until those facts exist.
2. Provider POC specification refinement and eventual Firebase Hosting vs Cloudflare Workers implementation when authorized.
3. Real-browser Korean/English localization/accessibility/type/search/social/marketing transfer validation on that POC.
4. App-specific user/market evidence when actual product pages are assigned.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–012.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
