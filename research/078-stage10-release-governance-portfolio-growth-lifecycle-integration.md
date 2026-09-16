# 078 — Stage 10 Release Governance, Portfolio Growth & Lifecycle Integration

Date: 2026-09-16
State: **PASS — STAGE 10 FOUNDATION/PRACTITIONER GATE CLOSED**
Primary owners: **B Web UX/IA/Content + D Search/Discovery/Analytics + E Architecture/Security/Operations**
Consumers: A Platform/Browser; C Performance/Accessibility/Quality; Marketing; Design Studio; Software Engineering.

## Purpose
Stress-test 077's portfolio model against the conditions that make app-company websites fail in practice: asynchronous store releases, phased/staged rollout, regional availability, stale proof, campaign/store variants, multi-product growth, localization drift, URL migration, retirement and mixed native/PWA lifecycles.

This study closes Stage 10 at FOUNDATION/PRACTITIONER only. It does **not** certify `minttap.app`, MintTap, LogMate or any production store listing. Production topology, store state, routes, release automation, product claims and runtime remain OPEN until inspected.

## Source basis / CHANGE WATCH — rechecked 2026-09-16
Authoritative current sources used for this checkpoint:
- Apple App Store Connect Help — release options; phased release; app availability; removing apps/versions; custom product pages; screenshot/app-preview management.
- Google Play Console Help — production/testing releases; country availability; custom store listings; store-listing experiments.
- Google Search Central — redirects and site moves/migrations.

Current platform facts relevant to the operating model:
- Apple supports manual, automatic and scheduled-after-review release options. An approved/released version can take time to appear in the store.
- Apple's phased release for eligible updates distributes automatic updates progressively over seven days (1%, 2%, 5%, 10%, 20%, 50%, 100%); users may still manually download the update, and a phased release can be paused under Apple's current rules.
- Apple availability is country/region scoped and can change after release; removing availability does not imply that every previous user instantly loses the app or updates.
- Apple custom product pages can carry distinct screenshots/previews/promotional text/keywords and unique URLs; current App Store Connect supports many variants and requires review before visibility.
- Google Play production availability and testing country targeting are separate concepts; custom store listings can vary by country, URL/campaign and other supported segments.
- Google Play supports store-listing experiments, so store presentation itself can be a versioned/experimental surface rather than one timeless artifact.
- Google Search recommends permanent server-side redirects for permanent URL moves, URL-to-URL mapping, avoidance of irrelevant mass redirects, updating canonicals/internal links/sitemaps, and maintaining redirects for a substantial period; current guidance says generally at least one year for site moves.

Exact store UI, limits, review behavior, rollout controls, country rules, experimentation features and search-engine operational details are **CHANGE WATCH**. Durable principles below do not depend on today's exact limits.

---

## 1. The central failure: release is not one atomic event

A naïve model is:
`new app version shipped → website can now describe new version`

The real cross-surface model is asynchronous:
`code/build readiness → store submission/review → metadata/proof readiness → approval → release decision → country/region availability → rollout population → web publication → support readiness → deep-link/PWA compatibility → measurement observation`

These transitions can occur at different times and can partially fail.

Therefore the Web Manager must never model a launch as a single boolean `released=true`.

### Release-state dimensions
For each product/platform maintain independently:
- build/version identity;
- review state;
- release state;
- rollout state/percentage or equivalent where applicable;
- region/country availability;
- minimum/compatible versions where relevant;
- store-listing/default/custom-page state;
- web claim/proof version;
- support/documentation version;
- governance/privacy state if behavior changed;
- deep-link association/route compatibility;
- PWA/web-app version/cache/schema compatibility if applicable;
- measurement/instrumentation version.

**SYNTHESIS:** a portfolio consistency defect can exist even when every individual system is internally valid.

---

## 2. Release Truth Record

077 introduced Resource Identity Record and Portfolio Consistency Matrix. Add a **Release Truth Record** for every material release.

Required fields:
- product;
- platform/surface;
- release/build/version identifier;
- capability delta and evidence owner;
- submission/review state;
- release method: manual/automatic/phased/staged/other;
- rollout population state;
- country/region availability;
- store default/custom listing dependencies;
- web resources/claims affected;
- proof assets affected;
- support/release-note resources affected;
- privacy/governance impact;
- deep-link/public-route impact;
- PWA worker/cache/schema/data impact where relevant;
- analytics schema/decision impact;
- earliest safe web-publication condition;
- rollback/pause/containment path;
- validation evidence and timestamp;
- owner.

### MINTTAP DIRECTION
Do not publish a feature claim merely because the build containing it was uploaded or approved. Define the **earliest safe claim state** according to the claim.

Examples:
- A universal capability claim may require broad production availability, not merely review approval.
- A release-note entry can describe a phased rollout if it explicitly says rollout is gradual.
- A region-specific page may claim availability only for the verified region.
- A support article may need version scoping while old and new versions coexist.

---

## 3. Mixed-version reality during rollout

Apple's current phased-release model demonstrates why `latest release` is not synonymous with `all active users run latest version`: automatic updates progress over days, while manual downloads can bypass the phased percentage.

This creates a **mixed-version population**.

Operational consequences:
- support documentation may need old/new version branches;
- screenshots can be accurate for new users but confusing for existing old-version users;
- deep-link targets must account for route support by installed version;
- backend/API changes must not be inferred safe from store approval;
- analytics must segment by app/release version when the decision requires it;
- web copy should avoid implying simultaneous universal transition unless verified.

### Failure exercise — feature removed in v3, rollout at 10%
Bad response: immediately rewrite all help content as if v2 no longer exists.

Correct diagnosis:
1. identify populations still on v2;
2. identify whether users can manually update;
3. scope support instructions by version if necessary;
4. ensure web/store proof does not create impossible instructions;
5. monitor rollout/support evidence;
6. retire v2-specific support only after an explicit lifecycle condition.

---

## 4. Region availability is part of product truth

Apple and Google both expose country/region availability controls, but the exact account/location semantics differ by platform. Therefore `available worldwide` must never be inferred from a single successful store visit.

Model:
`product capability × platform × country/region × store state × version/rollout × locale/support readiness`

A localized web page can be technically excellent while sending users to an unavailable product.

### Availability Contract
For any public distribution CTA record:
- product/platform;
- intended countries/regions;
- store destination;
- current availability evidence/date;
- locale shown;
- unsupported-region behavior;
- fallback/support route;
- owner/change trigger.

**CONTRADICTION:** language and geography are not interchangeable. Korean-language content does not prove Korean store availability; an English page does not imply only English-speaking markets.

---

## 5. Default store page, custom store page and campaign page are separate presentation states

Both major stores provide mechanisms for differentiated listing experiences. This breaks another naïve assumption:
`website product page ↔ one immutable store listing`

A better model:
`canonical product truth → bounded audience/message variant → web campaign/resource → intended store variant → actual product capability`

Variants may emphasize different features, but they may not invent different products.

### Variant Governance Record
For each material web/store variant:
- audience/intent;
- canonical product claim source;
- allowed emphasis;
- screenshots/proof version;
- locale/region;
- unique destination/URL;
- deep-link destination if used;
- review/publication state;
- campaign owner;
- measurement contract;
- expiry/review trigger.

Marketing owns audience/channel/positioning strategy. Web Manager owns resource continuity, canonical truth, destination correctness and web measurement boundaries.

### CONTRADICTION
`custom listing exists → every visitor sees it` is false. Visibility depends on platform-specific targeting/link/search/campaign rules.

---

## 6. Product proof freshness is release governance, not a design cleanup task

A screenshot can be visually polished and factually obsolete.

Proof lifecycle:
`claim → evidence asset → product/release applicability → publication surfaces → freshness trigger → validation → retirement/replacement`

### Proof Asset Ledger
Record:
- asset ID;
- claim(s) supported;
- product/platform;
- app/web version represented;
- locale;
- source capture/provenance;
- surfaces using it: company/product/campaign/store/support;
- accessibility alternative/caption requirements;
- review trigger;
- replacement asset;
- owner.

Triggers include:
- UI/workflow change;
- capability change;
- platform support change;
- store asset requirement change;
- localization change;
- privacy/security wording change;
- retirement.

Track C validates media/performance/accessibility cost. Design Studio owns visual treatment. Web Manager owns semantic proof scope and freshness.

### Failure exercise — old screenshot survives a redesign
Do not solve only by replacing the homepage image. Query the Proof Asset Ledger to locate every dependent surface: store variants, support, social/campaign resources and localized copies.

---

## 7. Portfolio governance under multiple products

As product count increases, duplicated truth becomes the primary content risk.

Use a **Product Truth Registry** with fields such as:
- canonical product name;
- current lifecycle state;
- platforms;
- supported markets;
- canonical proposition/capability boundaries;
- store identities/destinations;
- support root;
- privacy/governance scope;
- public URL identity;
- PWA/native role;
- owner;
- release truth source.

Pages consume this registry conceptually; they do not each become independent authorities.

### Ownership rule
- Company surface owns portfolio/company truth.
- Product surface owns stable public product truth.
- Store owns distribution/store presentation state.
- Product/runtime owns actual capability state.
- Support owns task-resolution truth.
- Governance owns authoritative policy/legal/security communication.
- Marketing owns campaign strategy, not capability truth.

When two sources disagree, resolve authority first; do not average the wording.

---

## 8. Cross-product navigation and brand growth

A portfolio navigation should help users answer:
1. where am I — company or which product?
2. what other products exist?
3. which support/governance resource applies to this product?
4. can I return to company-level context without losing my task?

Do not force every product to expose every sibling product in every task flow. Cross-product navigation is context-sensitive.

### Stress test — MintTap + LogMate + future Product C
A durable conceptual structure must survive:
- one product being native-only;
- one product having native phone + PWA/EFB surfaces;
- one product unavailable in a region;
- different support maturity;
- different privacy/data models;
- one product retiring while company continues.

If a shared company header or root URL makes any of these states impossible to communicate accurately, architecture is over-coupled.

---

## 9. Localization drift and release drift compound each other

A locale can become stale even if its translation was once correct.

Model:
`source truth version → locale adaptation version → product/store release version → proof version → support/governance version`

Therefore localization needs lineage, not only translation status.

Extend 077 Locale Readiness Contract with:
- source-content version;
- translated/adapted version;
- product release applicability;
- store metadata/listing version;
- proof-asset version;
- support/governance freshness;
- last semantic review;
- owner.

### Failure exercise
English product page is updated for v4; Korean page still describes v3 but remains indexed and has a valid store CTA.

This is not merely a translation defect. It is a release-consistency defect affecting search, trust, support and measurement.

---

## 10. Retirement is a state machine

Use explicit lifecycle states rather than `live/deleted`:
`active → maintenance/limited → deprecation announced → distribution restricted/removed → support transition → retired historical state → eventual archival decision`

Not every product needs every state, but retirement must answer:
- can existing users still run it?
- can previous purchasers redownload/update it?
- is backend service still available?
- can users export/delete data?
- what support remains?
- what store regions remain?
- what happens to public/deep links?
- what happens to PWA cached/local data?
- what privacy/retention obligations remain?
- which historical resources should remain indexable?

Apple's current availability behavior is a useful warning: removing an app from sale does not necessarily erase the installed/purchased population. Product retirement and distribution removal are separate events.

---

## 11. URL migration and retirement mapping

Google Search's current migration guidance reinforces a durable user principle: redirects should map old intent to a genuinely corresponding new resource.

### Migration table
For every changed/retired URL:
- old URL;
- old user intent/resource identity;
- lifecycle reason;
- exact equivalent replacement, if any;
- redirect type/policy;
- canonical update;
- internal-link update;
- sitemap update;
- app-link association impact;
- external high-value links/campaigns to update;
- monitoring period;
- final archival/removal decision.

Rules:
- permanent equivalent move → permanent server-side redirect is generally appropriate;
- temporary displacement → preserve original identity and use temporary behavior where justified;
- no equivalent replacement → return a truthful retired/404/410-style outcome as architecture requires rather than an irrelevant homepage redirect;
- avoid redirect chains; map old resources directly to final equivalents where possible;
- retain migration evidence long enough for users/search/external links to transition.

**CONTRADICTION:** `no 404s = healthy migration` is false. An irrelevant redirect can be worse than a truthful missing/retired state.

---

## 12. PWA lifecycle joins the portfolio release model

PWA introduces another asynchronous release surface:
`server deployment → service-worker discovery/install → waiting/activation → controlled clients → cache generation → data-schema compatibility → user task`

This is not equivalent to native store rollout.

A mixed native/PWA product therefore needs a **Surface Compatibility Matrix**:
- public web version;
- active service-worker generations;
- cache/schema compatibility;
- native iOS versions;
- native Android versions;
- server/API compatibility;
- sync protocol/version;
- deep-link route compatibility;
- backup/export format compatibility.

074 remains authoritative for data correctness. Web Manager does not design the implementation protocol; Software Engineering validates actual versioning, migration, sync and rollback behavior.

### Critical guard
A website release can be instant at the origin while a PWA client remains controlled by an older worker and local data schema. Therefore `deployment complete` does not prove `all installed PWAs updated`.

---

## 13. Release synchronization operating loop

Create a reusable **Cross-Surface Release Gate**:

`release intent → capability evidence → Release Truth Record → Product Truth Registry update → store state/region check → web claim/proof update → support/governance update → link/deep-link validation → locale readiness → quality guardrails → publication → mixed-version monitoring → correction/rollback → lifecycle cleanup`

Gate questions:
1. What changed in actual product behavior?
2. Which populations can actually receive it now?
3. Which web/store/support claims become true, false or version-dependent?
4. Which proof assets become stale?
5. Which locales/regions can support the change?
6. Does any deep link/public route change?
7. Does privacy/security/data behavior change?
8. Does PWA cache/schema/update behavior change?
9. What measurement distinguishes rollout from instrumentation effects?
10. What is the containment/rollback communication path?

---

## 14. Growth loop without content sprawl

Portfolio growth should not become page-count growth.

Decision rule for a new resource:
`distinct user intent + durable semantic responsibility + maintainable truth owner + discoverability need + lifecycle value > duplication/freshness cost`

Before creating a new campaign/product/feature page ask:
- Is the user task materially distinct?
- Is there a stable canonical resource already?
- Will this page require separate localization/support/proof upkeep?
- Can campaign parameters/custom store variants solve the need without duplicating product truth?
- What happens after the campaign/release ends?

Track D measures qualified task outcomes, not raw page proliferation.

---

## 15. Incident and rollback communication boundary

A release defect can create contradictory web/store/support states.

Do not rewrite evergreen documentation to describe a temporary outage unless the underlying durable behavior changed.

Use the right surface:
- status/incident surface → current transient operational state;
- support → workaround/task recovery;
- release note → version change/history;
- product page → stable supported capability;
- governance → policy/data/security commitments;
- campaign → acquisition message, paused when truth is invalid.

During containment, the safest web action may be to disable/qualify a claim or CTA rather than immediately restructure URLs/content.

Stage 11 will deepen incident/rollback infrastructure; Stage 10 establishes the semantic operating boundary.

---

## 16. Integrated diagnostic exercises

### Scenario A — iOS phased release, Android full release, website says “new workflow available now”
Diagnosis: cross-platform/population overclaim.
Action: scope claim by platform/version/rollout or delay universal claim; version support/proof; preserve measurement by release population.

### Scenario B — Korean custom store listing points to a feature absent in current Korean web proof
Diagnosis: presentation continuity failure, not necessarily product failure.
Action: validate actual capability/region first, then reconcile canonical claim/proof and variant lineage.

### Scenario C — second product launches and `/support` has no product identity
Diagnosis: support IA does not scale with portfolio.
Action: establish product-scoped task entry while retaining company-level support routing where useful; do not duplicate every article.

### Scenario D — app removed from sale but old users still need export instructions
Diagnosis: distribution retirement was confused with user-lifecycle completion.
Action: retain product/support/data resources until the explicit user/data support condition is met.

### Scenario E — PWA deployment fixed a sync bug, but installed EFB still behaves old
Diagnosis: origin deployment state was confused with worker/client control/update state.
Action: inspect service-worker generation/control/schema/runtime evidence; do not tell users “fixed” universally until target-client validation supports it.

### Scenario F — all retired product URLs redirect to company home
Diagnosis: intent-destructive migration.
Action: map equivalent resources; retain historical retirement/support resource when needed; truthful missing state where no replacement exists.

### Scenario G — store experiment wins installs but increases support failures
Diagnosis: local acquisition metric improved while guardrail degraded.
Action: Stage 9 decision contract applies; do not declare portfolio improvement from install conversion alone.

### Scenario H — marketing needs five campaign pages for five channels with identical product intent
Diagnosis: likely duplicate truth/content debt.
Action: prefer canonical resource + campaign attribution/store variant unless a materially distinct user task/message justifies separate resource.

---

## 17. Cross-track and specialist transfer

### Track A — Platform/Browser
Owns deep-link/browser/PWA mechanics. Stage 10 consumes verified behavior; does not redefine platform rules.

### Track B — UX/IA/Content
Owns resource/task identity, support/product hierarchy, version-scoped user communication and portfolio wayfinding.

### Track C — Performance/Accessibility/Quality
Owns release quality guardrails, proof/media cost, accessible status/support states and cross-browser/device evidence. Design or acquisition gains cannot waive quality constraints.

### Track D — Search/Discovery/Analytics
Owns canonical/redirect/discovery evidence, release/locale measurement and experiment boundaries. Search traffic does not define resource truth.

### Track E — Architecture/Security/Operations
Owns release-state operation, association resources, governance, retirement/migration control and operational continuity. Stage 11 will deepen deployment/monitoring/rollback architecture.

### Marketing
Receives canonical product truth, availability/locale state, approved proof and destination contracts. Returns channel/audience/positioning requirements. Custom campaign/store variants must remain bounded by actual capability.

### Design Studio
Latest checked Web Design evidence on 2026-09-16: Stage 1/2 PASS, Stage 3 PRACTICE; W025 identifies true-origin/cross-browser/AT/physical-device evidence still OPEN. Therefore polished/Chromium-bounded design evidence cannot certify production cross-surface release quality.

### Software Engineering
Latest checked Studio evidence remains Foundation study underway. D001/Q001 boundaries support source-of-truth/validation thinking, but no implementation PASS is imported. Engineering must validate actual release identifiers, app-link files/routes, PWA update/schema compatibility, APIs/sync, rollback and runtime behavior.

---

## 18. Production OPEN register
Still unknown and not inferred:
- actual `minttap.app` company/product IA and URL topology;
- actual MintTap/LogMate store IDs/listings/custom pages/regions/locales;
- actual current versions, release method or rollout automation;
- actual screenshot/proof inventory and freshness;
- actual support/status/release/account/data resources;
- actual AASA/assetlinks/deep-link mappings;
- actual PWA deployment/worker/cache/schema state;
- actual analytics/experiments;
- actual retirement/migration requirements;
- actual content/store release ownership or CI automation.

Production validation remains OPEN.

---

## 19. Stage 10 competency gate
Stage 10 FOUNDATION/PRACTITIONER PASS requires ability to:
1. model company/product/support/governance/campaign resources as separate lifecycle responsibilities;
2. grow one app into a multi-product portfolio without binding company identity to one product;
3. synchronize web/store/support/proof claims under asynchronous review, rollout and regional availability;
4. reason correctly about mixed-version user populations;
5. govern default/custom store and campaign variants without creating conflicting product truth;
6. maintain proof freshness with release lineage;
7. separate language, locale, region, store availability and support readiness;
8. design retirement as a user/data/search/support lifecycle rather than URL deletion;
9. map URL migrations by intent/equivalence and avoid irrelevant mass redirects;
10. integrate PWA worker/cache/schema lifecycle with portfolio release semantics without claiming implementation correctness;
11. use analytics/experiments as bounded evidence rather than allowing local conversion to override quality/trust guardrails;
12. hand implementation/design/marketing work to the correct specialist with explicit evidence boundaries.

**Result: PASS — Stage 10 FOUNDATION/PRACTITIONER gate closed.**

The evidence now supports a complete app-company web strategy at the intended curriculum level. Actual MintTap project decisions still require production/store/runtime inspection.

---

## 20. Next major target
Proceed to **Stage 11 — Web Operations & Platform Architecture**.

Highest-value integrated starting bundle:
`requirements → rendering/hosting model → DNS/CDN/origin topology → environments/CI-CD → deployment atomicity → cache invalidation → observability/SLO signals → rollback/recovery → dependency/update governance → provider cost/lock-in/portability`.

PWA remains elevated: service-worker deployment, cache generations, schema migration, offline clients, rollback impossibility/forward-fix boundaries and managed-EFB operation should be major Stage 11 application cases.
