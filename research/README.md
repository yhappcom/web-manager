# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and related strategic web-app capability. Canonical curriculum: `../LEARNING_ROADMAP.md`; horizontal ownership: `../SPECIALIST_TRACKS.md`. Learning proceeds FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT.

Evidence vocabulary: `SOURCE`, `SYNTHESIS`, `MINTTAP DECISION/DIRECTION`, `OPEN`, `DEPENDENCY`, `VALIDATION`, `CHANGE WATCH`, `TRANSFER VALIDATION`, `CONTRADICTION`.

## Completed curriculum
- Stage 1 Web Foundations: 027–033 — **PASS**
- Stage 2 Website Anatomy / Content / IA: 034–038 — **PASS**
- Stage 3 UX & Interaction: 039–044 — **PASS**
- Stage 4 Web Design Literacy: 045–050 — **PASS**
- Stage 5 Accessibility: 051–058 — **PASS**
- Stage 6 Search / Discovery / Content Quality: 059–065 — **PASS**
- Stage 7 Performance / Browser Runtime: 066–070 — **PASS**
- Stage 8 Security / Privacy / Trust: 071–072 — **PASS**
- Stage 9 Analytics / Experimentation: 075–076 — **PASS**

All passes are foundation/practitioner curriculum gates, not production validation.

## Stage 9 — Analytics / Experimentation — COMPLETE
075 — **Analytics, Measurement & Experimentation Evidence Foundations — PASS.**  
Builds decision→task semantics→observable evidence→privacy/minimization→event/metric contract→quality validation→aggregation/segmentation→interpretation→decision→re-observation. Separates product state/event/metric/funnel/attribution/causality; defines outcome/diagnostic/guardrail architecture, event contracts, funnel eligibility, segmentation/cohort risks, attribution limits, privacy-aware instrumentation, qualitative+quantitative evidence, experiment validity foundations, risk-weighted decision thresholds and an Analytics Evidence Registry.

076 — **Measurement Reliability, Causal Inference & Pre-Launch Integration — PASS / STAGE 9 GATE.**  
Extends the evidence system through semantic/coverage/data-quality reliability, systematic missingness, observed-vs-modeled evidence, sampling/thresholding, late/duplicate/offline delivery, identity/attribution discontinuity, randomization/blocking/confounding, statistical-vs-practical significance, experiment validity, low-traffic/non-experiment alternatives, pre-launch measurement planning and release/measurement lineage. Extends Analytics Evidence Registry with denominator, missingness, occurrence-vs-ingestion, duplicate policy, data-quality state, identity scope, reconciliation and decision threshold.

Stage 9 integrated model:
`decision → population/task → product truth → observable signal → collection → missingness/selection → transformation/modeling → metric/uncertainty → alternatives → causal design if needed → guardrails → decision → intervention → re-observation`.

Key guards:
- reality ≠ observed data ≠ processed report ≠ modeled estimate ≠ causal effect;
- report completeness ≠ population completeness;
- attribution ≠ causal history;
- event arrival time ≠ event occurrence time;
- statistically significant ≠ practically important;
- non-significant ≠ equivalent;
- experiment outcome ≠ permission to violate accessibility/security/privacy/performance guardrails.

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations: Service Workers, Offline, Install, Storage, Updates & Platform Reality — PASS.**  
Covers AppCache historical lesson; PWA capability composition; secure-context/origin/scope trust; service-worker lifecycle/update; cache-strategy failure modes; CacheStorage vs IndexedDB; quota/persistence/eviction; Safari/iPadOS vs Chromium/Android install reality; update/data-preservation UX; background-capability boundaries; EFB constraints.

074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**  
Separates local transaction, durable outbox, transport, remote idempotent apply, acknowledgement, reconciliation/conflict and independent backup. Covers IndexedDB version/blocked-upgrade behavior, same-origin Web Locks coordination, retry/idempotency ambiguity, long-offline recovery, background-sync limitations, server/WebSocket/WebTransport/WebRTC/Web Bluetooth/direct-LAN boundaries, backup/restore requirements and a managed-EFB validation plan.

075–076 add measurement transfer without changing product-state authority. Offline telemetry can be late/missing/duplicated and must never become sync correctness infrastructure.

Key contradiction guards through 076:
- `cached offline = backed up` — false;
- `local save = synchronized` — false;
- `Background Sync = universal eventual-sync guarantee` — false;
- `WebRTC = automatic nearby-device discovery/background sync` — false;
- `works on ordinary Safari = works on managed EFB` — false without target-device/policy evidence;
- `sync analytics event = product acknowledgement` — false;
- `all available report data = all real users/tasks` — false.

PWA production/device validation remains OPEN. Implementation-level schema, outbox, conflict, backup, transport and telemetry work is a Software Engineering dependency.

## Next vertical curriculum study — Stage 10 App-Company Web Strategy & Growth
Integrate the completed foundations into an Apple/Android app-company operating model:
`company identity → product portfolio → product proof → store/web continuity → support/governance → release lifecycle → localization/growth → retirement/URL continuity`.

Priority areas: company vs product vs campaign/support surfaces; one-app→multi-app architecture; prelaunch/launch/postlaunch; App Store/Google Play continuity; screenshots/demos/proof; pricing/subscription explanation where applicable; support/release/status/account deletion; deep linking; international expansion; portfolio brand/navigation; product retirement. PWA remains an elevated cross-track specialization where strategically relevant.

Marketing owns broader acquisition/community/channel strategy. Track D provides web/search/measurement evidence; B owns web information/task structure; E owns operational/governance lifecycle; A/C supply platform and quality constraints.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns web task/information structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability and measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates.

Design Studio remains canonical for reusable visual/interaction evidence. Latest checked Web status: Stage 1/2 PASS, Stage 3 PRACTICE; W023 integrated Chromium evidence exists but route/network/cross-browser/AT/device/field/human evidence remains OPEN.

Software Engineering Studio latest checked 2026-09-16: Foundation study underway; D001/Q001 provide bounded source-of-truth/durability and validation-contract evidence but no specialist Foundation PASS. Web Manager consumes these boundaries without duplicating implementation engineering.

## Study quality standard
Substantial studies include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, project relevance without invented production facts, durable vs changeable behavior, and competency/application checks.