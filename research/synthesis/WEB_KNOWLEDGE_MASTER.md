# Web Knowledge Master — integrated curriculum and specialist judgment

**Snapshot:** 2026-11-07 KST, Web Manager `main@4f5903f411b8c3a353ea4edb552c7bea6c4a2e33`. **Status:** integrated navigation/synthesis, **not** replacement for primary research, new standards certification, deployed-site audit, or a new learning gate. **Coordinator:** Web Manager. **Canonical research:** [index](../README.md), [roadmap](../../LEARNING_ROADMAP.md), [tracks](../../SPECIALIST_TRACKS.md), [historical status](../../STATUS.md). Other masters: [PWA](PWA_ARCHITECTURE_MASTER.md) · [evidence](EVIDENCE_VALIDATION_REGISTER.md) · [MintTap application](MINTTAP_PRODUCT_APPLICATION.md) · [open work and cadence](RESEARCH_GAPS_AND_SCHEDULE.md).

## 1. Authority and interpretation

**SOURCE:** Studies [001–026](../001-app-launch-website-foundations.md) established app-company launch foundations; studies 027–082 cover the 12-stage sequential curriculum; 073/074 established strategic PWA foundations; later numbered studies include deep maintenance, operational counterexamples, simulations and read-only application of LogMate source. The [research index](../README.md) records Stage 1–12 **PASS** and 073/074 **PASS** as **competency gates**. Current work is **applied Stage 8 Security/Privacy/Trust ACTIVE**, with **production validation OPEN and PWA release HOLD**. These statements are compatible: revisiting Stage 8 for product risk does **not** revoke previously completed generic Stage 1–12 learning.

**Evidence authority precedence:** (1) current product policy and exact released/served/runtime evidence for product facts (LogMate [MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md)); (2) source-pinned executable observations, bounded by fixture/build/platform; (3) source-pinned static findings; (4) authoritative standards/browser/platform documentation with date and version; (5) synthesis/design/validation plan. Web Manager cannot promote its research proposal to approved product implementation. Design Studio, Marketing and Software Engineering retain their canonical disciplines.

**Explicit correction:** [LEARNING_ROADMAP.md](../../LEARNING_ROADMAP.md) once ended with a historical “return to Stage 1” position, superseded by the completed sequential gate in [research/README](../README.md). Neither a current Stage-8 focus nor an older roadmap paragraph establishes Stage 1 as today's active curriculum stage.

## 2. Twelve-stage canonical learning map

| Stage / primary owner(s) | Mature reusable competence | Canonical anchors | Product proof needed before claiming rollout |
| --- | --- | --- | --- |
| 1 Web Foundations / A | URL/origin, DNS, HTTP/TLS, HTML/CSS/JS/DOM, browser lifecycle and state | [033 integration](../033-stage1-end-to-end-integration-competency-review.md), [029 HTTP](../029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md) | Actual production host, headers, network trace |
| 2 Content and IA / B | App/company/support/privacy resource identities, content ownership, navigation and wayfinding | [038 integration](../038-stage2-integration-page-system-matrix-competency-review.md), [002 IA](../002-multi-app-information-architecture.md) | Usability, actual content, public URL reachability |
| 3 UX and Interaction / B + C | User tasks, state/error/recovery, forms, responsive input and interrupted journeys | [044 integration](../044-stage3-integration-complete-task-usability-interaction-competency-review.md) | Exact native/web and human/task evidence |
| 4 Web Design Literacy / B + Design Studio | Hierarchy, type/color, screenshots, components and responsive governance | [050 integration](../050-stage4-integration-app-company-web-design-literacy-competency-review.md) | Design Studio runtime/W121, not static mockups |
| 5 Accessibility / C + B | Semantic HTML/ARIA boundaries, keyboard, focus, authentication, reflow, media | [058 integration](../058-stage5-integration-accessibility-conformance-complete-process-evidence-app-company-competency-review.md) | Manual AT/real devices, WCAG evaluation, errors/recovery |
| 6 Search and Discovery / D + B | Crawl/index/canonical, structured data, international search and query intent | [065 integration](../065-stage6-integration-search-discovery-content-quality-competency-niche-app-operating-system.md) | Live crawler/index/Search Console provenance |
| 7 Performance / C + A | Critical rendering path, LCP/INP/CLS, causality, budgets, third-party cost | [070 integration](../070-stage7-integration-performance-diagnostic-release-operating-system.md) | Representative RUM/field evidence, device trace |
| 8 Security/Privacy/Trust / E + A | Threat model, SOP/CORS, auth/session, CSP, supply chain, privacy and claims | [071 foundations](../071-stage8-security-privacy-trust-integrated-foundations.md), [072 integration](../072-stage8-integration-security-privacy-release-readiness-operating-system.md) | Product and deployment-specific threat-control tests |
| 9 Analytics / D | Events/funnels, attribution limits, validity, privacy-preserving measurement | [076 integration](../076-stage9-measurement-reliability-causal-inference-prelaunch-integration.md) | Real measurement consent, instrumentation and cohort proof |
| 10 App-company Strategy / B + D + E | Product-truth provenance, website↔Store, lifecycle/support/account actions | [077 portfolio](../077-stage10-app-company-web-portfolio-lifecycle-strategy.md), [078 governance](../078-stage10-release-governance-portfolio-growth-lifecycle-integration.md) | Shipped claim/version and public endpoint parity |
| 11 Architecture/Operations / E + A + C | Hosting, CDN/origin, deployment, rollback, SLO/incident and recovery | [079 platform](../079-stage11-web-operations-platform-architecture-deployment-recovery-pwa.md), [080 reliability](../080-stage11-reliability-observability-dr-supply-chain-integration.md) | Served bytes, disaster drill, operator/MDM constraints |
| 12 Expert Management / coordinator | Decision records, conflicting evidence, ethical/operational trade-offs, specialist handoffs | [081 judgment](../081-stage12-expert-web-management-decision-governance.md), [082 integration](../082-stage12-portfolio-governance-postmortem-platform-evolution-final-integration.md) | Real decision outcome and ongoing maintenance |

**SYNTHESIS:** These are not 12 independent project implementations. They compose a dependency graph: A supplies substrate → B defines tasks and information → C validates quality → D connects external discovery/measurement → E assures trust and operational lifecycle. The coordinator adjudicates gates and transfer, but is not a sixth research track.

## 3. Five-track reuse map and relative bottleneck

| Track | Reusable knowledge owner | Current highest-value unresolved question | Required transfer |
| --- | --- | --- | --- |
| **E** (lead, first) | Web architecture, storage/identity custody, account-erasure, deployment/recovery and threat model | Can exact LogMate deletion, old-tab revocation and independent Files backup satisfy owner-safety and release invariants? | Engineering S007 exact product test; A platform context, C acceptance, B truthful UX, D claims |
| **A** (second) | Browser/origin/SW lifecycle, fetch, CacheStorage, IDB, manifest and platform divergence | Can two real Worker generations, installed WebKit containers and cold-offline relaunch preserve safe service and data authority? | E controls, C browser/device testing |
| **C** (third) | Quality oracles, accessibility, performance, regression/failure analysis | Which research/synthetic PASS transfers to a pinned NORMAL build and physical iPad? | Design Studio W121; A/E runtime dependency |
| **B** (fourth) | Web journeys, IA, content identity, offline/update/deletion/recovery task states | Are actual support/deletion and recovery states accessible and truthful? | Design Studio visual/interaction; Engineering actual state |
| **D** (fifth) | Indexability, canonical/Store continuity, measurement and privacy of claims | Are public claims, Search/Analytics and consent supported by an actually served version? | Marketing public claims, product evidence |

This **E → A → C → B → D** ranking is a **current allocation**, not permanent merit ranking. Re-rank when a product intervention, new primary platform fact or independent test shifts expected information gain.

## 4. Company website doctrine — reusable decisions, not deployment claims

1. **User purposes:** discover, evaluate, act, and obtain support/governance. The [026 hierarchy](../026-app-company-web-strategy-information-hierarchy.md) is a planning model, not measured MintTap customer behavior.
2. **Information architecture:** company-first, app-centered public resources; small shallow navigation and enduring per-app support/privacy/deletion identifiers ([002](../002-multi-app-information-architecture.md), [003](../003-privacy-support-account-deletion-architecture.md)). A URL proposal is not a live page.
3. **Product truth:** maintain an internal version- and platform-specific [Product Truth Record](../004-store-website-content-synchronization.md), App Data Contract, screenshot provenance, claim registry and release-linked channel expressions. Website/Store phrasing may differ, facts may not.
4. **Transport/identity:** HTTPS, controlled redirects, direct AASA/assetlinks verification endpoints, selective HSTS, per-route security headers and provenance of served payloads ([005](../005-domain-hosting-security-baseline.md)). Header presence or a CI fixture does not certify live host compliance.
5. **Usability/quality:** responsive semantic page systems, error/recovery paths, keyboard/screen reader compatibility, performance budgets and representative field telemetry; Lighthouse/CI/simulator are scoped signals, not comprehensive conformance.
6. **Legal/operational triggers:** platform policy, jurisdiction, analytics/ads and data-flow obligations depend on actual product, markets, processors and live Console declarations. Use [013 legal trigger map](../013-jurisdiction-legal-compliance-trigger-map.md); do not turn it into legal advice.
7. **Portfolio sustainability:** preserve public URL identity through launch, updates and retirement; treat website/support/privacy/deletion resources as operational surfaces, not campaign decoration ([077](../077-stage10-app-company-web-portfolio-lifecycle-strategy.md)).

## 5. Evidence discipline and contradictions resolved

- **COMPETENCY PASS ≠ production PASS.** Sequential and generic PWA gates remain PASS; browser/devices/product validation remains separately OPEN.
- **Synthetic runtime PASS ≠ exact product runtime PASS.** Synthetic Chrome/Node/Firestore outcomes can establish a mechanism, not a LogMate deployed defect or absence of one.
- **Authentication ≠ owner authority ≠ backup ≠ Sync.** UID identity, local-owner state, independent Files custody, remote accepted receipt and reconciliation must each be observed.
- **SW script freshness ≠ CacheStorage freshness ≠ controller activation ≠ offline readiness.** See [530 `43–44](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md).
- **37-store exported registry ≠ 29 explicit terminal-wipe stores.** [529 `96](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) reconfirmed a source-level omission at a changed LogMate source blob, not a proven runtime leak.
- **Design Studio Stage 3 PRACTICE ≠ Web Manager Stage 3 competency PASS.** Different domain gates, different test scopes: [Design W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md).

**CHANGE WATCH:** Always pin source SHA, browser/OS/MDM version, policy date, test artifact, actual delivery URL and negative controls when material. Keep prior original records for provenance; modify this synthesis only when an actual contradiction, meaningful new evidence or authority decision changes it.

## 6. Using this master

Before new research: start with [open decisions/cadence](RESEARCH_GAPS_AND_SCHEDULE.md), inspect the exact source study and [evidence register](EVIDENCE_VALIDATION_REGISTER.md), then decide whether the question is genuinely new. Transfer a reusable finding to its owner only; other tracks record their dependency, not a duplicate primer. For product implementation and release, use [MintTap application](MINTTAP_PRODUCT_APPLICATION.md) and exact current product sources. No product/peer repository changes are authorized by this master.
