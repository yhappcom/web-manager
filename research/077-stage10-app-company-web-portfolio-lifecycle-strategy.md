# 077 — Stage 10 App-Company Web Portfolio & Lifecycle Strategy

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER INTEGRATED CHECKPOINT**
Primary owners: **B Web UX/IA/Content + D Search/Discovery/Analytics + E Architecture/Security/Operations**
Consumers: A Platform/Browser; C Performance/Accessibility/Quality; Marketing; Design Studio; Software Engineering.

## Purpose
Convert Stages 1–9 into an operating model for an app company whose web estate must remain coherent as it grows from one product to several native apps and optional PWA surfaces. The objective is not to design `minttap.app` prematurely; actual routes/runtime/product commitments remain OPEN. The objective is durable judgment about company identity, product resources, store/web continuity, support/governance, deep-link boundaries, release lifecycle, localization, growth evidence and retirement.

## Source basis / CHANGE WATCH
Authoritative platform material rechecked 2026-09-16:
- Apple Developer — Allowing apps and websites to link to your content / Supporting Universal Links: Universal Links are ordinary HTTP(S) URLs backed by a two-way app↔website association; when the app is absent, the web URL remains usable in the browser. Incoming parameters must be validated because links are an app input surface.
- Apple Developer — Associated Domains: `applinks` is an associated-domain service. On iOS 14+ Apple uses an Apple-managed CDN for AASA retrieval; exact cache/testing behavior is platform CHANGE WATCH.
- Android Developers — About/Verify App Links: verified App Links associate website URLs with an Android app using manifest intent filters plus `/.well-known/assetlinks.json`; Android 12+ provides explicit verification tooling and Android 15+ introduces dynamic App Links behavior on supported environments.

Platform versions, store presentation/policy, browser deep-link behavior and verification tooling are CHANGE WATCH. The architectural principle — public web identity and verified native association are different layers — is durable.

## 1. First-principles portfolio model

A web estate for an app company should be modeled as distinct but connected resource classes:

`company identity → product identity → task/proof resources → distribution/store handoff → support → governance/trust → operational status/release → lifecycle/retirement`

These are not automatically separate domains or pages. They are semantic responsibilities. URL/page boundaries should be created when user task, lifecycle, ownership, localization, canonical identity or operational requirements materially differ.

Critical separations:
- company identity ≠ product identity;
- product page ≠ campaign landing page;
- product proof ≠ marketing claim;
- store CTA ≠ installation;
- public URL ≠ native route;
- deep-link eligibility ≠ successful app opening;
- support content ≠ incident status;
- privacy policy ≠ privacy architecture;
- release note ≠ support documentation;
- locale variant ≠ translated string set;
- product retirement ≠ URL deletion.

## 2. One app → multi-app architecture

The first app can tempt a company to make the entire domain equivalent to that product. That creates migration pressure when a second app arrives.

A durable conceptual hierarchy is:
- **Company layer** — who operates the products, portfolio navigation, company-level contact/trust/governance where genuinely shared.
- **Product layer** — stable identity for each app, proposition, supported platforms, proof, distribution links and product-specific trust/support entry.
- **Task/support layer** — durable help, troubleshooting, account/data tasks and product documentation.
- **Governance layer** — privacy/legal/security/account-deletion resources with explicit scope and version/lifecycle.
- **Campaign/editorial layer** — optional time-bound acquisition/content surfaces that link into canonical product/task resources rather than becoming duplicate product truth.

**SYNTHESIS:** architecture should optimize semantic ownership and lifecycle independence before visual uniformity. Shared navigation/design can coexist with separate product truth.

### Domain decision rule
Do not choose root paths vs subdomains vs separate domains from aesthetics. Evaluate:
1. identity continuity;
2. product autonomy;
3. search/canonical consequences;
4. verified app-link host requirements;
5. deployment/security ownership;
6. localization;
7. support/governance scope;
8. migration/retirement cost;
9. analytics boundaries;
10. future portfolio growth.

For MintTap, the exact topology remains **OPEN** until actual company/product scope and production routes are inspected.

## 3. Resource identity beats navigation labels

Navigation is a discovery interface; URLs/resources are lifecycle assets. A durable product resource should survive reasonable redesigns and navigation renaming.

For every material resource maintain a **Resource Identity Record**:
- resource purpose / primary task;
- owning product/company scope;
- canonical URL intent;
- lifecycle state: planned/live/deprecated/retired;
- locale relationships;
- native-app association if any;
- store destinations;
- governance/support dependencies;
- analytics decision purpose;
- replacement/redirect policy;
- owner and review trigger.

This extends Stage 6 Search Opportunity Records and Stage 9 Analytics Evidence Registry into portfolio operations.

## 4. Website ↔ store continuity

The website and App Store/Google Play are separate distribution/presentation systems. They should share product truth but need not duplicate every field or sentence.

Continuity contract:
`same product identity → compatible promise → compatible platform/availability facts → compatible screenshots/proof → correct store destination → explicit unsupported/unknown states`

A web page can explain more context than a store listing, but it must not imply features, pricing, platform availability or privacy behavior that the distributed build does not support.

Store links require release-aware ownership. A CTA should have:
- target platform/store;
- target product/build availability assumption;
- locale/region behavior if relevant;
- fallback behavior;
- validation date;
- analytics semantics that stop at observable handoff unless stronger evidence exists.

`store CTA activation ≠ store page view ≠ download ≠ install ≠ first launch ≠ retained use`.

## 5. Product proof architecture

Claims need evidence appropriate to their type. Useful proof classes:
- actual product UI/screenshots;
- bounded workflow demonstrations;
- supported feature explanation;
- compatibility/platform facts;
- changelog/release evidence;
- support documentation;
- privacy/security behavior with technical/policy basis.

Avoid proof theater: decorative device frames, badges, testimonials or metrics cannot substitute for evidence of a material capability.

Proof lifecycle matters. A screenshot can become false when the UI or workflow changes. Each material proof asset should have product version/release relevance, owner and review trigger.

Design Studio owns reusable visual presentation. Web Manager owns what claim the proof must substantiate, web placement/task context and freshness requirement.

## 6. Deep-link / public-URL contract

Apple Universal Links and Android App Links establish verified relationships between web hosts and native apps, but web architecture must remain valid independently.

Durable model:
`public HTTPS resource → browser-valid fallback → optional verified native association → native route validation → task continuation`

Apple states that Universal Links use the same HTTP(S) URL for web and app and fall back to the website when the app is not installed. Android verified App Links similarly bind declared web URLs to an installed app through Digital Asset Links verification.

Therefore:
- do not create an important URL that is meaningful only when the native app opens;
- do not treat a redirect chain as equivalent to a verified direct association;
- validate all incoming route parameters;
- separate domain association success from in-app route correctness;
- maintain app-link files as production web resources with deployment/monitoring ownership;
- test browser fallback and installed-app behavior separately;
- keep association behavior/version as CHANGE WATCH.

Actual MintTap AASA/assetlinks/package/bundle/signing/route mapping remains OPEN and is a Software Engineering + Web Operations dependency.

## 7. PWA position in a mixed portfolio

PWA is not a company-wide label. It is a capability set for a particular product/task/environment.

Portfolio decision layers:
`public website` / `native app distribution` / `installable web experience` / `offline-capable web task` / `cross-device synchronized product`

These are different commitments.

For a future LogMate/EFB case, a PWA may serve a managed-iPad constraint while phone products remain native. That does not imply the marketing/company website should itself become an offline application.

PWA product resources need explicit communication of:
- supported browser/platform environment;
- install method where relevant;
- offline scope;
- local durability limits;
- update behavior;
- synchronization/backup distinction;
- unsupported managed-device states.

073–076 remain authoritative: `cached ≠ backed up`, `local save ≠ synchronized`, telemetry ≠ sync truth.

## 8. Prelaunch → launch → postlaunch lifecycle

### Prelaunch
Required questions:
- What stable public identity must exist before store release?
- Which support/privacy/account/contact resources are distribution prerequisites or user trust prerequisites?
- Which claims can already be proven?
- What must remain explicitly unavailable/coming later?
- Which URLs should be stable before external links/search indexing begin?
- What measurement is necessary for launch decisions?

Avoid publishing speculative feature pages merely to create search inventory.

### Launch
Release readiness is a consistency problem:
`web truth + store truth + build availability + support truth + governance truth + links + measurement + rollback/incident ownership`

A launch checklist without cross-surface semantic validation can still ship contradictory information.

### Postlaunch
Observe:
- product/support/search demand;
- broken store/deep links;
- stale screenshots/claims;
- release-specific support issues;
- locale gaps;
- performance/accessibility/security regressions;
- acquisition/task outcomes with Stage 9 evidence limits.

Changes should flow from explicit evidence, not continuous homepage churn.

## 9. Support, status, release and account/data surfaces

These surfaces solve different user problems.

**Support:** durable task/problem resolution.

**Status:** current operational condition; should not become permanent documentation.

**Release notes/changelog:** what changed by product/version; not a replacement for task docs.

**Account/data controls:** actionable workflows such as account deletion/data requests where applicable; must match actual product/backend capability and policy.

**Governance:** policy/terms/privacy/security communication with scope/version/owner.

Cross-link them when the user task requires it, but preserve semantic boundaries so an outage does not force editing evergreen support truth and a policy revision does not silently rewrite historical product behavior.

## 10. Localization and international growth

International growth is not “translate every page.” Apply Stage 6:
`market/user need → product/store availability → locale/resource need → localized product truth → locale discovery relationship → support/governance capability → measurement`

Do not launch a localized acquisition page if the corresponding product availability, support, legal/governance or store destination cannot support the implied experience.

Locale expansion needs a **Locale Readiness Contract**:
- product availability;
- store listing/destination;
- core product page;
- support coverage;
- privacy/legal scope;
- screenshots/proof accuracy;
- hreflang/canonical strategy where applicable;
- native/web deep-link behavior;
- measurement/reporting ability;
- owner for ongoing updates.

Translation completeness is not market readiness.

## 11. Growth without duplicating Marketing

Marketing owns channel, positioning, community and campaign strategy. Web Manager owns whether the web estate can receive, explain, route and measure demand truthfully.

Web growth loop:
`qualified demand → correct public resource → understandable proof → supported task/handoff → observable outcome → evidence-quality check → content/product/support diagnosis → bounded improvement`

Do not optimize raw sessions/pageviews independently of task fit. Niche products can rationally prefer lower-volume qualified traffic over broad irrelevant traffic.

Campaign landing pages should exist only when they serve a materially distinct intent/message/task and can remain consistent with canonical product truth. Otherwise use the canonical product resource with campaign attribution where appropriate.

## 12. Product retirement and URL lifecycle

Retirement begins before shutdown. Maintain:
- retirement decision/effective date;
- affected products/platforms/regions;
- user migration/export/data obligations;
- support window;
- store availability change;
- web notice and replacement resource;
- redirect vs retained historical resource decision;
- app-link association changes;
- search/indexing plan;
- analytics end-of-life interpretation;
- privacy/data retention consequences;
- ownership after active development ends.

**CONTRADICTION:** deleting every retired-product URL immediately is not clean lifecycle management. Existing users, external references, support history and search results may still require a stable explanatory resource.

Use redirects only when there is a genuinely equivalent replacement. Do not redirect retired-product support or policy history to an unrelated homepage merely to eliminate 404s.

## 13. Portfolio consistency matrix

Before a material release, validate each product across:
| Dimension | Company web | Product web | Store | Native/PWA | Support/Governance |
| --- | --- | --- | --- | --- | --- |
| Product name/identity | compatible | canonical | compatible | actual | compatible |
| Availability | scoped | explicit | actual | actual | supported |
| Capability claim | bounded | evidence-backed | compatible | implemented | documented |
| Platform | correct | correct | correct | actual | correct |
| Privacy/data claim | scoped | linked/explained | compatible | actual behavior | authoritative policy |
| Distribution/deep link | navigable | correct CTA | destination | route handles | fallback/help |
| Locale | navigable | ready | available | supported | supportable |
| Lifecycle | portfolio state | current | current | release state | current/history |

A mismatch is a release defect even if every individual page is technically valid.

## 14. Failure scenarios / diagnosis

### A. Second app launches and homepage is the first app
Root cause is portfolio identity coupling, not merely navigation. Establish company-level identity and stable per-product resources before adding more campaign links.

### B. Search result lands on a product URL but installed app opens the wrong screen
Separate web resource correctness, association verification and native route mapping. Search correctness does not prove deep-link correctness.

### C. App removed from one region but web CTA remains global
Availability truth has diverged. Repair release/region ownership and locale/store-destination validation; do not infer store availability from a cached web configuration.

### D. Screenshot promises an old workflow
Proof asset freshness failure. Link proof assets to product/release review triggers.

### E. PWA offline claim is true for shell assets but not the user's task/data
Capability claim is overbroad. State task-specific offline behavior and validate target device/storage/update conditions.

### F. Retired product redirects all URLs to company homepage
Historical/support intent is destroyed. Retain explanatory resources or map only genuinely equivalent replacements.

## 15. Cross-specialist handoffs

### Marketing
Provide canonical product/resource inventory, supported claims, store/web handoff evidence, locale readiness and attribution limits. Receive channel/positioning requirements. Do not let campaign copy create a second source of product truth.

### Design Studio
Provide page/task/proof/state requirements, content priority, stale-proof triggers and platform constraints. Receive reusable visual/interaction solutions. Production human validation remains separate.

### Software Engineering
Provide URL/native-route contract, association-file requirements, supported platform/product state, PWA state semantics, account/data workflows, release version and validation expectations. Receive implementation/runtime evidence. Exact production association and route behavior must be verified, not assumed.

## 16. MintTap facts still OPEN
Do not infer:
- current `minttap.app` route hierarchy or whether root domain is company vs MintTap-product identity;
- future product portfolio/domain topology;
- MintTap App Store/Google Play listing URLs/regions/locales;
- production AASA or `assetlinks.json`;
- bundle IDs/package names/signing fingerprints;
- actual deep-link routes;
- support/status/account-deletion implementation;
- PWA production role;
- analytics/attribution stack;
- release automation/content ownership;
- product retirement requirements.

These require live repository/runtime/store evidence.

## 17. Competency gate
PASS this Stage 10 checkpoint if Web Manager can:
1. separate company/product/campaign/support/governance resource responsibilities;
2. plan one-app→multi-app growth without binding domain identity to the first product;
3. maintain store/web/native truth continuity without claiming click=install;
4. treat deep links as verified public-URL/native-route contracts with browser fallback;
5. position PWA as product/task capability rather than a generic website label;
6. define prelaunch/launch/postlaunch consistency and ownership;
7. distinguish support/status/release/account/governance surfaces;
8. gate localization on full experience readiness, not translation alone;
9. integrate Marketing growth requirements without duplicating channel strategy;
10. preserve user/search/support continuity through product retirement.

**Result: PASS — FOUNDATION/PRACTITIONER integrated checkpoint.**

## Next adjacent work
Stage 10 remains ACTIVE. Next bundle should stress-test **portfolio governance, release/store synchronization, product proof/content freshness, lifecycle operations, growth loops and multi-product scenarios**, then close the Stage 10 integration gate if evidence is sufficient. After Stage 10, proceed to Stage 11 Web Operations / Platform Architecture.