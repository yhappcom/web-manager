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
- Preferred scalable locale paths: `/ko/...` and `/en/...` initially.
- Localized pages self-canonicalize, declare the correct document language and connect through reciprocal `hreflang`.
- Automatic locale redirection is not the primary architecture; explicit locale URLs remain reachable.
- Established **Locale Matrix** and **Localization Manifest**.
- Website/store/app UI localization remain separate facts.
- Real Korean/English typography, fallback and long-label browser proof remains OPEN.
- Canonical study: `research/007-localization-architecture.md`.

### 008 — SEO, Structured Data, Sitemap, Canonical & Crawlability
- Established final-HTTPS self-canonical rules and localized canonical/hreflang consistency.
- Defined public crawlability contract and minimal `robots.txt` policy.
- Defined XML sitemap inclusion/exclusion rules.
- Established conservative `Organization`, conditional `SoftwareApplication` and visible-hierarchy `BreadcrumbList` direction.
- Added Search Console ownership/continuity, indexing/canonical monitoring and structured-data change watch.
- Canonical study: `research/008-seo-structured-data-crawlability.md`.

### 009 — SEO Independent Verification & Social Preview Metadata
- Formalized **A discoverable public / B public noindex / C private access-controlled** route classes.
- Reconfirmed that robots is crawl management, not privacy or reliable de-indexing.
- Established localized title/meta-description rules.
- Established Product-Truth-governed Open Graph baseline and social-preview validation requirements.
- Canonical companion study: `research/009-seo-independent-verification-social-preview.md`.

### 010 — Company / App Marketing Content Model
- Confirmed from current Apple and Google primary sources that app marketing/metadata must not misrepresent actual functionality; Apple explicitly treats misleading app marketing outside the App Store and false pricing as enforcement risks.
- Established marketing as a **downstream presentation layer over Product Truth**, not an independent factual database.
- Established a **Claim Registry** with claim classes: product fact, user-value interpretation, quantified claim, testimonial/review, comparative claim and future/roadmap claim.
- Required evidence/provenance, verification date, locale/surface conditions and invalidation/review triggers for material claims.
- Established an app-page content contract: identity/value → user problem/context → primary/supporting/conditional capabilities → evidence/screenshots → availability/purchase conditions → trust → official store CTA → support/privacy/account controls.
- Screenshots are treated as evidence with app/platform/version/locale/feature/capture provenance and staleness triggers; concepts/future UI must be clearly labeled rather than passed off as current product.
- Established company-home role as publisher/portfolio orientation rather than repetition of every app page.
- Established price/subscription disclosure principles and high-risk-claim handling for security/privacy, quantified performance, rankings/awards, comparisons, absolutes and roadmap timing.
- Marketing localization may adapt wording but may not strengthen claims, omit material conditions or imply app UI localization that is not shipped.
- Added marketing-claim, screenshot, store-CTA and roadmap invalidation fields to the Content Release Manifest.
- Canonical study: `research/010-company-app-marketing-content-model.md`.

## Current maturity

Stage: **Foundation**
State: **IN STUDY — architecture/evidence base expanding**

Reading alone is not PASS. Policy findings require freshness checks; architecture/security/accessibility/localization/search/social/marketing findings require implementation on real pages, browsers, devices, locales, search tools, social channels, store consoles and actual app releases before production confidence.

## Current public information architecture

Preferred localized human-facing pattern:
- `/ko/`, `/en/` — localized company/home surfaces; final root strategy remains OPEN.
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
- **Claim Registry** — material marketing claim, class, evidence, approved locale expressions, conditions, owner, verification/expiry/invalidation state and surfaces using it.
- **Content Release Manifest** — release impact across web/store/privacy/support/localization/assets/infrastructure/accessibility/search/social/marketing.
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
- Translation must preserve Product Truth, App Data Contract and Claim Registry meaning.
- Privacy/account-control translation prioritizes substantive equivalence over marketing adaptation.
- Support localization must correspond to the UI/version users actually see.
- Korean/English text growth, fallback, wrapping, mixed-script metrics and 200%/320px behavior require real-browser proof.

## Search / discovery / social baseline

### Indexability classes
- **A — discoverable public:** default for company/app/support/privacy/account-control pages intended to be found.
- **B — public/noindex:** exceptional public utility pages with a documented reason.
- **C — private:** staging/internal/admin/draft material protected through actual access control.

### Search contract
- Every indexable public page has one final HTTPS URL and explicit self-consistent canonical.
- Localized pages keep their own canonical and reciprocal hreflang relationships.
- Public pages expose meaningful visible content and crawlable links; metadata/JSON-LD cannot substitute for real content.
- `robots.txt` is not secrecy/access control and is not the sole de-indexing mechanism.
- XML sitemap contains final canonical indexable URLs only.
- Each important indexable page gets a unique localized title/meta description aligned with visible content and Product Truth.
- Structured data describes only visible/real facts; no fabricated ratings/reviews, pricing, legal identity or contact data.
- Search Console ownership, sitemap submission, URL Inspection and canonical/indexing monitoring are production operations.

### Social preview contract
- Share-worthy pages use localized Open Graph title/description.
- `og:url` equals the final locale canonical URL.
- `og:image` is a stable publicly fetchable HTTPS asset.
- Social preview copy/images may not contradict Product Truth, Screenshot Evidence, Claim Registry or real locale support.
- Platform-specific preview/card/cache behavior requires validation on actual channels adopted by MintTap.

## Marketing content baseline

- Marketing facts derive from Product Truth/App Data Contract/evidence; copy does not create new facts.
- Every material/high-risk claim should have Claim Registry provenance.
- High-risk claim classes include price/payment, privacy/security, quantified performance/accuracy, user count/ranking/award, comparison, outcome implications, absolutes and roadmap timing.
- Feature hierarchy distinguishes primary, supporting and conditional/advanced capabilities.
- Material purchase/account/platform/network/permission conditions appear near the relevant claim rather than being hidden far away.
- Screenshots and videos must represent real current experience or be explicitly labeled as concept/future.
- Store badges are official destination controls and must link to the correct current app; they are not the page's main value proposition.
- Support, privacy and account controls are trust/product surfaces, not expendable footer clutter.
- Korean/English marketing may differ editorially but may not differ materially in promise or qualification.

## Current release blockers model

Examples include:
- privacy/data-disclosure mismatch;
- required support/privacy/deletion URL broken;
- non-existent feature presented as shipped;
- materially incorrect account/subscription instructions;
- misleading screenshots/social previews;
- inaccessible launch-critical support/account-control flow;
- association files redirected/malformed when required;
- localized content materially contradicting source product/data truth;
- website/store/social content claiming app UI language support that is not shipped;
- canonical/hreflang pointing to wrong app/locale/staging/redirect targets;
- production accidentally retaining staging `noindex` or crawl blocks;
- sitemap publishing staging/obsolete/wrong-host URLs;
- private material protected only by robots/noindex;
- fabricated ratings/reviews/pricing/entity facts in structured data;
- material marketing claim with no evidence/provenance;
- stale/false price or subscription condition;
- unsupported ranking/award/quantified claim;
- roadmap/concept presented as current functionality;
- official store badge linking to the wrong/unavailable app;
- Korean and English pages making materially different product promises.

## Important open items

- Exact MintTap legal entity/public contact information.
- Exact app inventory, released versions, account behavior, pricing and locale support.
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
- Search Console organizational ownership/access model.
- Actual app categories/pricing/store IDs and whether legitimate review/rating data suitable for structured markup exists.
- Which support pages should be indexable vs selectively excluded based on value/risk.
- Final social distribution channels and preview-image art direction/dimensions.
- Per-app primary audience/problem evidence, legitimate quantified metrics/testimonials and screenshot approval workflow.
- Final company positioning and current official Google Play badge/brand requirements at implementation time.
- Jurisdiction-specific legal/compliance requirements once launch regions and data practices are fixed.

## Current Design Studio dependencies / handoffs

- **Web Design** — turn the new app-page content contract into real scan paths, responsive hierarchy, evidence/screenshot composition, trust surfaces, badge placement and browser/device validation. Current Web Design state remains Foundation/not yet baselined, so this study does not dictate one visual template.
- **Typography / Type** — validate Korean/English hero/title/feature/qualification lengths, mixed-script product names, annotation typography, wrapping and zoom/reflow.
- **Layout / Interaction** — validate CTA priority, capability/evidence grouping, purchase/platform limitation disclosure, galleries/carousels when used, support/privacy routing and mobile recomposition.
- **Color** — validate CTA/state hierarchy, screenshot framing, brand semantics, disabled/unavailable destinations and focus/hover behavior without fake trust-badge semantics.

## Next research queue

1. **Operational release / change-watch controls:** policy freshness, broken links, verification files, indexing, social previews, screenshots, Claim Registry staleness and store availability.
2. Jurisdiction-specific legal/compliance web requirements when entity, markets and actual data practices are known.
3. Implementation/provider comparison after the Foundation evidence baseline is mature enough to score hosting/CMS/framework candidates.
4. Real-browser Korean/English localization/accessibility/type/search/social/marketing transfer validation once an implementation exists.
5. App-specific user/market evidence when actual MintTap product pages are assigned.

## Persistence state

- `AGENTS.md` contains the autonomous continuous-learning directive.
- `research/README.md` indexes studies 001–010.
- Completed study details are canonical in `research/`.
- This file is the current operational checkpoint.
