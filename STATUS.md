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
13. **013 Jurisdiction-Specific Legal / Compliance Trigger Map** — fact-driven Legal Trigger Registry; Korea PIPA/privacy-rights/overseas-transfer and conditional direct-commerce triggers; U.S. FTC/COPPA/California CCPA; other-state change watch; conditional EU GDPR trigger.
14. **014 Provider POC Specification** — identical Firebase vs Cloudflare static corpus, deterministic manifest, machine-endpoint/HTTP/header/cache/search/social/404/a11y assertions, preview/promote/rollback and provider-neutral verification harness.
15. **015 Machine-Readable Control Artifacts / Single Source of Truth** — canonical JSON records, JSON Schema Draft 2020-12 structural validation, immutable stable IDs, semantic fingerprints, dependency/invalidation graph, cross-record integrity linter and generated release-impact model.

Canonical details remain in `research/001...015`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — architecture / policy / operations / legal triggers / provider POC / internal truth model established**

Reading alone is not PASS. Current conclusions require actual MintTap facts, executable validation specimens, provider POC and real browser/device/store/legal/operational transfer validation before production confidence.

## Current public information architecture

Preferred localized pattern:
- `/ko/`, `/en/` — localized company/home surfaces; final root behavior remains OPEN.
- `/ko/apps/`, `/en/apps/` — app portfolio.
- `/ko/apps/<app-slug>/`, `/en/apps/<app-slug>/` — durable app pages.
- localized app `support/`, `privacy/`, `account-deletion/` child pages as applicable.
- company support/privacy/contact/terms only where substantively required.

Language-neutral machine endpoints:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

## Internal truth / control architecture

### Canonical principle

Each fact has one canonical owner/record. Other surfaces reference or derive from it rather than retyping the fact independently.

### Record families

- **App / Release / Feature** — identity, lifecycle, platform availability and shipped capabilities.
- **App Data Contract / Data Practice / Processor** — collection/use/share/retention/deletion, vendors, locations and account effects.
- **Store Destination** — official public store URL/availability state.
- **Evidence / Screenshot Evidence** — technical/store/test/visual proof with provenance and staleness.
- **Claim Registry** — marketing assertions that reference Product Truth/features/evidence rather than becoming new facts.
- **Locale Coverage / Localization Manifest** — app UI, web, store, privacy/support/deletion and translation review remain independent facts.
- **Legal Trigger Registry** — jurisdiction/law/trigger facts/applicability/required controls/review freshness.
- **Policy Change Register** — authority/source/effective dates/impact/actions.
- **Operational Surface Registry** — production URL/console expectations, owner, monitoring, severity and runbook.
- **Content Release Manifest** — increasingly derived from canonical record changes/dependencies, then completed with human approvals.

### Machine-readable direction

- canonical structured records: JSON;
- structural validation: JSON Schema Draft 2020-12;
- stable immutable logical IDs for cross-record references;
- repository integrity linter for references and business rules that JSON Schema alone cannot express;
- lifecycle/freshness states separated from domain states;
- semantic fingerprints for selected upstream records, using deterministic canonicalization/hashing, so formatting-only changes need not invalidate downstream approvals;
- dependency graph computes what must be reviewed when a fact changes;
- generated files/reports never become canonical facts.

### Key semantic validation examples

A release/build must detect cases such as:
- a current claim referencing only planned/removed features;
- a store CTA pointing at unavailable destination;
- a screenshot not matching compatible release/feature state;
- a privacy surface approved against an obsolete App Data Contract;
- translation approved against an old semantic source revision;
- an `APPLIES` legal trigger without required surface/process mapping;
- P0/P1 operational surface without owner/monitoring/runbook;
- unknown/duplicate/retired record references or invalid dependency cycles.

### Repository boundary

This repository is not a secret manager or user database. Never store API/private keys, tokens, signing private keys, passwords, raw customer data, privacy-rights requests or sensitive support tickets. Secret references may be stored; secret values remain in provider/CI secret systems.

## Security / infrastructure baseline

- Canonical origin direction: `https://minttap.app/`.
- TLS 1.0/1.1 prohibited; TLS 1.2 minimum; TLS 1.3 where supported.
- Ordinary HTTP redirects to HTTPS.
- HSTS only after complete HTTPS validation.
- AASA and `assetlinks.json` served directly with correct route/content type and no redirect.
- CSP inventoried/tested before enforcement; `nosniff`, explicit Referrer Policy and Permissions Policy are baseline directions.
- Deployment secrets stay outside Git; hosting must support auditable deployment, rollback and monitoring.

## Accessibility baseline

- WCAG 2.2 AA internal target.
- Native semantic HTML before custom ARIA widgets.
- Logical title/headings/landmarks and bypass mechanism.
- Full keyboard operation, visible logical focus, no traps/obscuration.
- 320 CSS px-equivalent reflow and 200% text enlargement without loss.
- Persistent programmatic form labels; textual errors and programmatic status.
- Automated scanners assist but cannot independently produce PASS.

## Localization / search / marketing baseline

- locale-specific crawlable URLs; `ko` and `en` initially;
- self-canonical translated pages + reciprocal hreflang;
- app UI, website and store localization remain separate facts;
- public pages default to indexable unless documented otherwise;
- robots is not secrecy/access control;
- sitemap contains final canonical indexable URLs only;
- structured data/social previews/marketing derive from real visible Product Truth;
- high-risk claims require evidence/provenance and invalidation rules;
- screenshots/videos represent current product or are explicitly labeled as concept/future.

## Legal / compliance trigger baseline

Legal compliance is managed as **facts → trigger → obligation → web/control surface → backend process → validation**.

- **Korea:** PIPA privacy/rights/overseas-transfer requirements depend on actual controller/data/vendor facts; direct web contracting/payment reopens e-commerce requirements.
- **United States:** FTC truth/privacy/security baseline; COPPA depends on child/actual-knowledge triggers; CCPA is threshold/nexus based; other state laws require current inventory when U.S. scope is active.
- **EU:** GDPR remains conditional on actual Article 3 establishment/offering/monitoring facts, not global reach alone.
- **Terms:** `/terms/` remains conditional on an actual contractual relationship requiring it.

## Operational release / change-watch baseline

Watched sources include Apple/Google platform policy, Search documentation, Android App Links/AdMob when active, Korean PIPA/e-commerce when applicable, FTC/COPPA, California and other activated jurisdictions.

Monitoring layers:
1. deploy-time deterministic validation;
2. scheduled synthetic checks;
3. event-driven platform/product/provider/data changes;
4. human freshness review.

A release is not closed merely because deployment/store review succeeds; production destinations, policy/control surfaces, deep links, metadata, truth/legal alignment and monitoring health must be rechecked.

## Current implementation architecture direction

**Git-versioned content/data → build-time static generation → global HTTPS/CDN hosting → isolated dynamic functions only where a real workflow requires server execution.**

Preliminary provider shortlist:
1. Firebase Hosting;
2. Cloudflare Workers + Static Assets;
3. Vercel if justified SSR/full-stack needs appear;
4. Netlify as viable static alternative.

No provider is selected yet.

## Provider POC contract

Firebase Hosting and Cloudflare Workers must run the same provider-neutral static corpus and verification suite.

Required proof includes:
- identical common-file SHA-256 manifest;
- localized app/legal/support fixture;
- exact AASA / assetlinks / app-ads / robots / sitemap / 404 behavior;
- status/MIME/redirect/cache/security-header assertions;
- canonical/hreflang/Open Graph/noindex separation;
- keyboard/200%/320px accessibility smoke;
- V1 live → V2 preview → V2 promote → native rollback V1;
- rollback restoring content + headers + redirects + machine endpoints;
- provider-neutral structured assertion report.

POC PASS is not production PASS.

## Release blockers model

Includes material privacy/data mismatch; broken required support/privacy/deletion/rights routes; unshipped feature claims; incorrect account/subscription/price instructions; stale misleading screenshots/claims; inaccessible launch-critical controls; broken AASA/App Links/DNS/TLS; locale/canonical/noindex errors; fabricated marketing/structured data; wrong store destination; missing applicable legal control; unreviewed applicable overseas transfer; COPPA trigger without review; direct web commerce without legal re-evaluation; and equivalent structural/semantic control-record validation failures.

## Ownership / continuity principle

No launch-critical capability may exist only in one person's memory/account. Registrar, DNS/CDN/hosting, Apple/Google consoles, policy/legal recipients, Search Console, monitoring, CI/CD, support/privacy inboxes and incident escalation require documented ownership/recovery. Secrets are never stored here.

## Important open items

- exact MintTap legal entity/place/public contact and contracting entity per app;
- actual app inventory/releases/pricing/accounts/locales/markets/audience;
- SDK/analytics/ads/auth/processors/data flows and processing locations;
- U.S./EU legal-trigger facts and legal reviewer/signoff process;
- actual JSON Schema files, validator implementation and schema `$id` namespace;
- exact editorial format/CMS and CI/review tooling;
- final hosting/CDN/DNS/framework/monitoring selection;
- actual provider accounts, permissions and domain authority for POC;
- Universal/App Link routes and app-ads use;
- root locale strategy and translation workflow;
- real Korean/English browser/type/fallback validation;
- Search Console/policy-alert/webhook/escalation operational ownership.

## Current Design Studio dependencies / handoffs

- **Web Design** — structured truth is input, not page hierarchy; final component/page behavior and browser/device validation remain Web Design work. Neutral POC styling is not final design.
- **Typography / Type** — structured records can generate repeatable Korean/English legal/support/feature stress strings for fallback/wrapping/zoom tests.
- **Layout / Interaction** — canonical states can drive realistic unavailable/stale/blocked/delete/error/recovery scenarios rather than placeholder states.
- **Color** — verified/stale/blocked/retired and warning/destructive/success are semantic states before visual encoding; color may not be the sole carrier.

## Next research queue

1. **Controlled validation specimen for Study 015:** actual JSON Schemas + valid/invalid records + repository integrity validator + documented failure→revision→re-proof cycle.
2. Execute Firebase Hosting vs Cloudflare Workers POC when accounts/domain authority are available.
3. Real-browser Korean/English localization/accessibility/type/search/social/marketing/legal transfer validation on the POC.
4. Apply Legal Trigger Registry when entity/market/audience/data/transaction facts are available.
5. App-specific user/market evidence when actual product pages are assigned.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–015.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
