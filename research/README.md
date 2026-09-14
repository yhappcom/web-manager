# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Each major topic matures through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

### Depth and cadence rule

Large domains are not marked complete after one short survey. Study should follow:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

Depth remains high, but persistence/reporting is intentionally coarse. Several related learning sub-blocks should normally be integrated into one professional knowledge checkpoint instead of generating one file/report per small concept.

A foundation core may close when it can be explained, diagnosed and applied at the level required by the curriculum; the same domain can and should be reopened later for advanced security, performance, SEO, accessibility, browser or operations depth.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION/DIRECTION` — project-specific choice or provisional direction.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed prior studies 001–026

Studies 001–026 remain retained as prior knowledge spanning launch requirements, IA, privacy/support, content consistency, security, accessibility, localization, SEO, marketing, legal triggers, provider evaluation, release governance and app-company strategy. They are prior knowledge, not the curriculum order going forward.

## Sequential curriculum studies

### 027 — Web / Internet / URL / Origin
`027-web-foundations-internet-web-client-server-url-origin.md`

**FOUNDATION LAYER COMPLETE.** Internet ≠ Web; client/server roles; resource vs representation; URL; host/domain/origin; origin security significance; failure-layer model.

### 028 — DNS / Domain / Resolution
`028-web-foundations-dns-domain-resolution-hosting-path.md`

**FOUNDATION LAYER COMPLETE.** DNS hierarchy/delegation; resolver/authority; records; TTL/cache; registration/delegation/hosting separation; DNS failure diagnosis.

### 029 — HTTP
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Supporting/integrated artifacts:
- `029-http-foundations-history-semantics-evolution.md`;
- `029a-http-message-anatomy-field-model-framing.md`;
- `029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md`;
- `029-http-operational-diagnosis-range-state-boundaries-competency.md`.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED.**

The review reconstructs the full path from URL interpretation through DNS, TLS, HTTP/intermediaries/cache, rendering boundaries, HTML→DOM, CSS/resource/layout processing, JavaScript/Web APIs, application state, navigation/history/bfcache and accessibility exposure.

### 034 — Stage 2 Website Anatomy, Task-Based IA & Content Ownership
`034-stage2-website-anatomy-task-based-information-architecture-content-ownership.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Establishes app-company websites as marketing + support + governance + store-linked operational surfaces; task-based IA; distinctions among sitemap/URL/navigation/page systems; app identity as a durable context boundary; external-entry contracts; and content ownership/change triggers.

### 035 — Stage 2 Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth
`035-stage2-content-modeling-hierarchy-lifecycle-cross-channel-truth.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Separates durable content objects from pages/components/channel fields; models App/Feature/Claim/Support/Known Issue/Release/Policy objects; establishes `claim → evidence → condition → action`; distinguishes canonical truth from public/search canonical URLs; and defines change-trigger/localization/retirement governance.

### 036 — Stage 2 Navigation, Wayfinding & Findability as an Operational System
`036-stage2-navigation-wayfinding-findability-operational-system.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Establishes navigation as orientation + movement, separates sitemap/hierarchy/URL/navigation/breadcrumb/search/history layers, treats findability as multi-route, defines direct-entry requirements, and provides a critical-destination/failure taxonomy for responsive and accessible navigation.

### 037 — Stage 2 Page Systems, Content Hierarchy & Scan/Comprehension Architecture
`037-stage2-page-systems-content-hierarchy-scan-comprehension-architecture.md`

**STAGE 2 FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Establishes pages as task contracts; semantic/visual/interaction hierarchy separation; page-type selection by user context; decision-critical sequence; heading/scan/comprehension rules; task-dependent density/disclosure; differentiated non-happy states; responsive semantic invariants; localization/reflow stress; and the reusable Page Contract.

### 038 — Stage 2 Integration: Company/App/Support/Governance Page-System Matrix & Competency Review
`038-stage2-integration-page-system-matrix-competency-review.md`

**STAGE 2 INTEGRATION GATE PASSED — FOUNDATION/PRACTITIONER LEVEL.**

Study 038 does not add another isolated Stage 2 model. It integrates 034–037 across realistic external and internal journeys and establishes:

- one end-to-end contract: `entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`;
- a company/app/support/governance/error-state page-system matrix;
- App Store / Google Play / search → app/support/privacy direct-entry tests;
- support-article → resolution → escalation tests;
- privacy/account-control direct-entry and destructive-action scope tests;
- release/known-issue lifecycle tests;
- differentiated 404/retired/unavailable/unsupported/empty/no-result recovery;
- Korean/English + narrow-width + enlarged-text/reflow structural invariants;
- heading/landmark/meaningful-order gate;
- an integrated failure taxonomy spanning entry contract, identity/scope, truth, destination, label/scent, hierarchy/sequence, recovery, lifecycle, localization/reflow and semantic exposure;
- a production handoff package for future Design Studio Web work;
- explicit OPEN items for real MintTap app inventory, account creation, store URLs, support model, localization, acquisition channels and human usability evidence.

Current primary evidence was revalidated 2026-09-15 against Apple App Store Connect, Google Play account-deletion/User Data guidance, W3C/WAI page-structure guidance and WCAG-related reflow guidance. Design Studio status and Layout L002 were also re-read; Web Design still has no substantive `W###` evidence, so browser/visual/human validation remains a downstream dependency.

## Current curriculum position

**Stage 1 — Web Foundations: COMPLETE at intended foundation/practitioner level.**

**Stage 2 — Website Anatomy / Content / Information Architecture: COMPLETE at intended foundation/practitioner level.**

Stage 2 completed sequence:
1. 034 — task-based website anatomy and ownership;
2. 035 — governed content objects/hierarchy/lifecycle;
3. 036 — operational navigation/orientation/findability;
4. 037 — page systems, hierarchy, scan/comprehension and states;
5. 038 — integrated page-system matrix and competency review.

No unresolved Stage 2 prerequisite currently blocks curriculum progression. Stage 2 should reopen later at advanced/expert depth when real MintTap analytics, support volume, localization, browser validation, production content and human usability evidence exist.

**Next: Stage 3 — UX & Interaction Foundations.**

The first Stage 3 integrated block should begin from first principles around:

`user goal → possible action/affordance → system state → feedback → error/prevention/recovery → continuity across interruption`.

It should incorporate existing Design Studio Interaction evidence without merely duplicating it, while keeping Web Manager's focus on transferable web/product management judgment.

## Study quality standard

A substantial study should normally include origin/problem where useful, precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, MintTap relevance without invented project facts, durable principles vs changeable behavior, and competency/application checks.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first. Web Manager should become design-literate enough to brief, critique and validate work while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.

Stage 2's completed handoff package now includes:
- task/destination matrix;
- semantic content-object/lifecycle relationships;
- critical-destination findability matrix;
- semantic Page Contracts and non-happy-state/recovery requirements;
- integrated external-entry/company/app/support/governance page-system matrix;
- direct-entry competency test;
- global/local scope and heading/orientation requirements;
- simultaneous-comparison/disclosure constraints;
- long localized content, enlarged-text/reflow and DOM/visual/focus/AT-order stress;
- instruction to return structural content/IA failures to Web Manager rather than mask them visually.

Design Studio Web remains pre-baseline with no substantive `W###` study at this checkpoint. Web Manager does not edit Design Studio canonical files without authorization.
