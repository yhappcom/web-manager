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
13. **013 Jurisdiction-Specific Legal / Compliance Trigger Map** — fact-driven Legal Trigger Registry; Korea PIPA/privacy-rights/overseas-transfer and conditional direct-commerce triggers; U.S. FTC/COPPA/California CCPA; other-state change watch; conditional EU GDPR trigger; integration with App Data Contract/provider selection/release controls.

Canonical details remain in `research/001...013`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — core architecture / policy / operations / legal-trigger / implementation-selection baseline established**

Reading alone is not PASS. Policy, legal applicability, architecture, security, accessibility, localization, search/social, marketing, operations and provider-selection conclusions require actual MintTap facts and real implementation/transfer validation before production confidence.

## Current public information architecture

Preferred localized human-facing pattern:
- `/ko/`, `/en/` — localized company/home surfaces; final root strategy remains OPEN.
- `/ko/apps/`, `/en/apps/` — app portfolio.
- `/ko/apps/<app-slug>/`, `/en/apps/<app-slug>/` — durable app pages.
- localized app `support/`, `privacy/`, `account-deletion/` child pages as applicable.
- localized company support/privacy/contact/terms resources only where substantively required.

Language-neutral machine endpoints:
- `/.well-known/apple-app-site-association`
- `/.well-known/assetlinks.json`
- `/app-ads.txt`

Root `/` remains OPEN between a language-neutral/x-default entry and a deliberate default-language home.

## Internal truth / control artifacts

- **App Data Contract** — actual data collection, SDK/processors, purposes, sharing, retention/deletion, account behavior, controller/entity, processor location/cross-border transfer, sensitive-data/audience classifications and rights implementation.
- **Product Truth Record** — shipped capabilities, identity, availability, account/subscription behavior, official destinations, intended markets/audience and transaction model.
- **Screenshot Evidence Set** — app/platform/version/locale/feature provenance and staleness.
- **Claim Registry** — material marketing claims, evidence, approved locale expression, owner, expiry/invalidation state and surfaces using them.
- **Content Release Manifest** — release impact across web/store/privacy/support/localization/assets/infrastructure/accessibility/search/social/marketing/legal triggers.
- **Locale Matrix** — app UI vs website vs store metadata vs privacy/support/deletion/screenshot locale coverage.
- **Localization Manifest** — source revision, target locale, reviewer, approval/staleness and surface coverage.
- **Policy Change Register** — policy/legal source, announcement/effective dates, impact, owner, action, severity and verification status.
- **Operational Surface Registry** — production URL/console surface, expected behavior, owner, monitoring method/cadence, last validation, severity and runbook.
- **Legal Trigger Registry** — jurisdiction, law, trigger facts, applicability state, required public/operational controls, source, dependencies, owner, legal review and freshness.

Exact machine-readable schemas remain OPEN.

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

## Legal / compliance trigger baseline

### Operating rule

Legal compliance is managed as **facts → trigger → obligation → web/control surface → backend process → validation**, not as a universal collection of Privacy/Terms/Cookie boilerplate.

### Korea
- PIPA Article 30 privacy-policy requirements become relevant when MintTap is a regulated personal-information controller; policy must match actual App Data Contract.
- PIPA rights procedures must be publicly explained and, where Article 38 applies, may not be more difficult than the collection method.
- Overseas provision/processing outsourcing/storage is a separate legal trigger; cloud/SDK provider location and legal role are now provider-selection inputs.
- Direct website order/payment/subscription would trigger a separate Korean electronic-commerce review; current known plan does not justify assuming a direct-commerce footer/checkout regime.

### United States
- FTC truth-in-advertising/privacy/security expectations reinforce Product Truth, Claim Registry and App Data Contract controls.
- COPPA requires a dedicated review when an app is child-directed under 13 or MintTap has actual knowledge of under-13 collection.
- California CCPA applicability is threshold- and nexus-based; it must be computed from entity/revenue/data-volume/sale-share facts rather than inferred from California availability.
- Other U.S. state privacy laws remain launch-time inventory/change-watch work; California controls are not assumed to satisfy every state.

### European Union
- GDPR remains CONDITIONAL; global website reach alone does not establish applicability. Re-open if EU establishment or intentional goods/services/behavior-monitoring triggers under Article 3 become real.

### Terms
- `/terms/` remains conditional. Do not publish generic boilerplate merely for footer completeness; create terms when a real service/account/licensing/direct-transaction contract requires them.

## Operational release / change-watch baseline

### Policy watch
- Apple App Review Guidelines, Developer News and Upcoming Requirements.
- Google Play Policy Announcements, Policy Deadlines and Policy Archive.
- Search Central documentation updates.
- Android App Links / AdMob app-ads when active.
- Korean PIPA / Enforcement Decree / PIPC guidance.
- Korean e-commerce law if direct sales become relevant.
- FTC privacy/security/advertising/COPPA.
- CPPA CCPA regulations/thresholds.
- Other U.S. states / EU only when market triggers become active.

### Monitoring layers
1. deploy-time deterministic validation;
2. scheduled synthetic checks;
3. event-driven policy/store/product/provider/data change watches;
4. human freshness review before releases and on governance cadence.

### Release close condition
A release is not operationally complete merely because deployment or store review succeeded. Post-release checks confirm live store destination, website CTA, Product Truth/Privacy/Support/Deletion/legal-trigger alignment, deep links, production metadata and monitoring health.

## Incident severity

- **P0 — user/distribution critical:** domain/HTTPS outage, required policy/control URL unavailable, material privacy mismatch, wrong critical store destination, broken core deep-link association, false deletion outcome.
- **P1 — high:** stale material pricing/claim/screenshot, material locale/legal disclosure contradiction, monetization verification failure, significant search/canonical/noindex error, broken notification path with no fallback.
- **P2 — normal:** non-critical social preview/search-copy/help-content issue without material product/control impact.

## Current implementation architecture direction

Preferred envelope:

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
- monitoring/log inspection and safe secret handling for optional dynamic functions;
- enough provider/data-location transparency for legal cross-border review when personal data is processed.

### Preliminary shortlist
1. **Firebase Hosting** — current simplest strong static-first fit.
2. **Cloudflare Workers + Static Assets** — strongest control/flexibility alternative.
3. **Vercel** — compelling if justified Next.js/SSR/full-stack needs appear.
4. **Netlify** — mature viable static alternative without a current decisive advantage.

No provider is selected yet.

### POC-before-selection rule
Firebase Hosting and Cloudflare Workers should host the same minimum specimen before final selection, including localized pages, legal/support surfaces, verification files, metadata, security headers, redirect behavior, preview and rollback. Selection follows transfer validation, not documentation comparison alone.

## Current release blockers model

Includes:
- privacy/data-disclosure mismatch;
- required support/privacy/deletion/rights URL broken where applicable;
- unshipped feature presented as current;
- materially incorrect account/subscription/price instructions;
- misleading/stale critical screenshots or claims;
- inaccessible launch-critical support/account-control flow;
- required AASA/App Links broken or malformed;
- DNS/TLS/production host failure;
- localized content materially contradicting Product Truth;
- canonical/hreflang pointing to wrong app/locale/staging target;
- production staging `noindex`/crawl rules;
- fabricated structured-data/marketing evidence;
- wrong/unavailable official store destination;
- applicable privacy policy materially contradicting processing;
- applicable legal rights route missing/hidden/impractical;
- unreviewed overseas transfer when Korean PIPA transfer requirements apply;
- child-directed/known-under-13 collection without COPPA review where applicable;
- direct web commerce introduced without reopening transaction-law triggers;
- one jurisdiction's privacy template presented as universally compliant.

## Ownership / continuity principle

No launch-critical operational capability may exist only in one person's memory/account. Production must eventually document ownership/recovery for registrar, DNS/CDN/hosting, Apple Developer/App Store Connect, Google Play Console, policy/legal recipients, Search Console, monitoring, CI/CD, support/privacy inboxes and P0/P1 escalation. Secrets are never stored here.

## Important open items

- exact MintTap legal entity/place of establishment/public contact information;
- contracting/publishing entity per app/store;
- exact app inventory, released versions, pricing, account behavior and locale support;
- intended launch countries/states;
- direct web payment/subscription model;
- intended audience/age classifications;
- exact SDK/analytics/ads/auth/processors/data flows and processing/storage countries;
- CCPA/state privacy threshold facts and sale/share/targeted-ad classifications;
- EU targeting/monitoring facts;
- legal reviewer/signoff process;
- storage schemas for internal control artifacts;
- release approval/console ownership roles;
- final hosting/CDN/DNS/framework/CMS/deployment/monitoring selection;
- Universal/App Link route inventory;
- actual app-ads.txt use and publisher/vendor lines;
- root `/` locale strategy;
- translation tooling/reviewer workflow;
- real Korean/English browser/type/fallback validation;
- Search Console organizational ownership;
- company/group email addresses for policy/alerts;
- App Store Connect webhook receiver/backend;
- escalation SLA/on-call expectations.

## Current Design Studio dependencies / handoffs

- **Web Design** — actual page/component complexity, legal notice placement, rights forms, contextual disclosures, responsive states and production browser/device validation.
- **Typography / Type** — Korean/English legal/support long-copy, processor names, contacts, tables, mixed-script wrapping/fallback and zoom/reflow.
- **Layout / Interaction** — navigation, rights/withdrawal/account-delete flows, denial/appeal/recovery, material disclosure salience and maintenance/error states.
- **Color** — semantic state/focus/destructive/disabled behavior; legal choices/rights may not rely on color alone.

## Next research queue

1. **Provider POC specification refinement** for an identical Firebase Hosting vs Cloudflare Workers transfer test.
2. Real-browser Korean/English localization/accessibility/type/search/social/marketing/legal-surface transfer validation on that POC.
3. Apply the Legal Trigger Registry when MintTap entity/market/audience/data/transaction facts are available.
4. App-specific user/market evidence when actual product pages are assigned.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–013.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
