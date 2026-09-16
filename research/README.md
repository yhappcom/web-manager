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

All passes are foundation/practitioner curriculum gates, not production validation.

## Stage 9 — Analytics / Experimentation
075 — **Analytics, Measurement & Experimentation Evidence Foundations — PASS.**  
Builds decision→task semantics→observable evidence→privacy/minimization→event/metric contract→quality validation→aggregation/segmentation→interpretation→decision→re-observation. Separates product state/event/metric/funnel/attribution/causality; defines outcome/diagnostic/guardrail architecture, event contracts, funnel eligibility, segmentation/cohort risks, attribution limits, privacy-aware instrumentation, qualitative+quantitative evidence, experiment validity foundations, risk-weighted decision thresholds and an Analytics Evidence Registry.

PWA application transfer in 075 preserves 073–074 state truth: local save, queued sync, transport attempt, acknowledgement, conflict and backup remain distinct; telemetry may observe but never define synchronization correctness. Offline/delayed/duplicate analytics delivery and platform-specific install observability are explicit boundaries.

**Stage 9 remains ACTIVE.** Next integrated block: measurement reliability, missingness/attribution, causal inference/experiment validity and pre-launch measurement planning; then integration gate if evidence is sufficient.

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations: Service Workers, Offline, Install, Storage, Updates & Platform Reality — PASS.**  
Covers AppCache historical lesson; PWA capability composition; secure-context/origin/scope trust; service-worker lifecycle/update; cache-strategy failure modes; CacheStorage vs IndexedDB; quota/persistence/eviction; Safari/iPadOS vs Chromium/Android install reality; update/data-preservation UX; background-capability boundaries; EFB constraints.

074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**  
Separates local transaction, durable outbox, transport, remote idempotent apply, acknowledgement, reconciliation/conflict and independent backup. Covers IndexedDB version/blocked-upgrade behavior, same-origin Web Locks coordination, retry/idempotency ambiguity, long-offline recovery, background-sync limitations, server/WebSocket/WebTransport/WebRTC/Web Bluetooth/direct-LAN boundaries, backup/restore requirements and a managed-EFB validation plan.

Key contradiction guards through 074:
- `cached offline = backed up` — false;
- `local save = synchronized` — false;
- `IndexedDB transaction = cross-device transaction` — false;
- `reliable transport = no idempotency needed` — false;
- `Background Sync = universal eventual-sync guarantee` — false;
- `WebRTC = automatic nearby-device discovery/background sync` — false;
- `same-origin Web Lock prevents cross-device duplicates` — false;
- `works on ordinary Safari = works on managed EFB` — false without target-device/policy evidence.

PWA production/device validation remains OPEN. Implementation-level schema, outbox, conflict, backup and transport work is a Software Engineering dependency.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns web task/information structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability and measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates.

Design Studio remains canonical for reusable visual/interaction evidence. Latest checked Web status: Stage 1/2 PASS, Stage 3 PRACTICE; W023 integrated Chromium evidence exists but route/network/cross-browser/AT/device/field/human evidence remains OPEN. Software Engineering owns implementation validation when substantive project evidence is available. Marketing owns acquisition/channel/community strategy; Track D provides measurement evidence and attribution limitations.

## Study quality standard
Substantial studies include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, project relevance without invented production facts, durable vs changeable behavior, and competency/application checks.