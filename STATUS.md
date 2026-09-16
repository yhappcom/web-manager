# MintTap Web Manager Status

Operating state: **ACTIVE — FIVE-TRACK BALANCED DEEP LEARNING + PWA STRATEGIC SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. `LEARNING_ROADMAP.md` is the vertical beginner→expert curriculum; `SPECIALIST_TRACKS.md` is the horizontal five-track expertise model. Web Manager coordinates A Platform/Browser, B UX/IA/Content, C Performance/Accessibility/Quality, D Search/Discovery/Analytics and E Architecture/Security/Operations by evidence/risk/dependency value rather than equal volume. PWA is a strategic high-priority cross-track specialization, not a sixth track.

# Curriculum state
Stages 1–8: **COMPLETE — FOUNDATION/PRACTITIONER GATES PASSED.** These are transferable competency gates, not production certification.

- Stage 1 Web Foundations: 027–033
- Stage 2 Website Anatomy / Content / IA: 034–038
- Stage 3 UX & Interaction: 039–044
- Stage 4 Web Design Literacy: 045–050
- Stage 5 Accessibility: 051–058
- Stage 6 Search / Discovery / Content Quality: 059–065
- Stage 7 Web Performance / Browser Runtime: 066–070
- Stage 8 Security / Privacy / Trust: 071–072

# Stage 9 — Analytics / Experimentation
**ACTIVE — FOUNDATION/PRACTITIONER.**

075 — **Analytics, Measurement & Experimentation Evidence Foundations — PASS.**

Established evidence chain:
`decision → user/business question → task/state semantics → observable evidence → privacy/minimization → event/metric contract → delivery/quality validation → aggregation/segment → interpretation/alternatives → decision threshold → intervention → re-observation`.

Retained judgments through 075:
- product state, analytics event, metric, funnel, attribution and causal explanation are separate layers;
- event count is not task success and funnel drop-off does not establish cause;
- measurement plans should separate outcome, diagnostic and guardrail metrics plus decision-relevant context;
- event contracts require exact trigger semantics, parameters/cardinality, version, privacy purpose, duplication/offline behavior, validation and blind spots;
- attribution models assign credit under rules/observable data and are not historical or motivational ground truth;
- segmentation/cohorts can reveal heterogeneity but introduce noise/privacy/bias risks and require pre-specified interpretation;
- privacy minimization precedes instrumentation; secure or consented collection is not unlimited collection;
- quantitative, qualitative and controlled-experiment evidence answer different questions and should be combined;
- experiments require pre-defined hypothesis, treatment/control, randomization unit, eligibility, primary outcome, guardrails, exposure logging, stopping/analysis rules and validity checks;
- statistical detectability and practical value are different; non-significance does not prove equality;
- instrumentation definitions must be versioned/governed rather than silently changed across comparison periods;
- an **Analytics Evidence Registry** now joins metric/event ownership, decision purpose, schema/version, privacy, QA, missingness/duplication and downstream use.

## PWA transfer through 075
073–074 product-state truth remains authoritative. Analytics may observe browser visit/install opportunity/standalone launch/local save/queued sync/transport/acknowledgement/conflict only where supported and justified; it must not define those states.

Key guards:
- local save ≠ sync queued ≠ transport attempt ≠ acknowledgement ≠ backup;
- telemetry delivery/retry cannot become a synchronization correctness dependency;
- offline telemetry can arrive late/out of ingestion order;
- analytics duplicate delivery must remain separate from product outbox/idempotency semantics;
- platform-specific install/standalone observability is CHANGE WATCH and cannot be assumed equivalent across Safari/iPadOS and Chromium/Android.

# PWA strategic specialization
073 — PWA Cross-Track Foundations — **PASS**.  
074 — PWA Data Durability & Synchronization Architecture Boundaries — **PASS**.  
Production/device validation remains OPEN; implementation-level schema/outbox/conflict/backup/transport is a Software Engineering dependency.

# Balanced track state
- **A Platform & Browser:** strong foundation; PWA lifecycle/storage/transport mechanics now consumed by Stage 9 event semantics.
- **B UX/IA/Content:** foundation/practitioner complete; owns task/state/eligibility semantics consumed by analytics.
- **C Performance/Accessibility/Quality:** substantial foundation/practitioner; supplies measurement guardrails and telemetry runtime-cost validation.
- **D Search/Discovery/Analytics:** search/discovery mature; **Stage 9 ACTIVE, 075 PASS. Still highest-value vertical bottleneck.**
- **E Architecture/Security/Operations:** Stage 8 foundation/practitioner PASS; privacy/data-flow/retention/third-party governance constrains analytics.

# Cross-repository evidence
Design Studio latest checked 2026-09-16: Web Design Stage 1/2 PASS, Stage 3 PRACTICE; W023 provides bounded integrated Chromium transfer but route/network/cross-browser/AT/physical-device/field/human evidence remains OPEN. Analytics evidence may identify a candidate UX/design problem but cannot substitute for human/Design Studio validation.

Software Engineering remains implementation owner for production telemetry schema/code, durable offline telemetry if selected, experiment assignment infrastructure, sync correctness and target-device validation. Web Manager owns web measurement semantics/evidence contracts.

Marketing owns channel/acquisition/community strategy. Track D supplies observed web/search/acquisition evidence with attribution and missingness limits rather than duplicating Marketing strategy.

# Production OPEN register
Actual `minttap.app` routes/runtime, hosting/CDN/origin, production accessibility/search/performance/security evidence, analytics vendor/property/tagging, consent/retention, event schema, funnels, web→store attribution, experiment infrastructure, traffic/baselines and PWA telemetry remain OPEN.

PWA additionally requires actual manifest/worker/storage/update/offline/backup/sync/managed-EFB validation. Do not infer production capability from generic platform evidence.

# Highest-value next work
Continue Stage 9 with a substantial integrated block on **measurement reliability + causal inference/experiment validity + attribution/missingness + pre-launch measurement planning**, then perform the Stage 9 integration gate if competency evidence is sufficient. Use PWA as an application case without letting analytics become product-state truth.

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model.
- `LEARNING_ROADMAP.md`: canonical vertical curriculum.
- `research/README.md`: staged/specialization research index.
- Stages 1–8: COMPLETE at intended foundation/practitioner level.
- Stage 9: **ACTIVE; 075 PASS.**
- PWA: 073–074 specialization checkpoints PASS; production/device validation OPEN.
- Reporting remains coarse/checkpoint-based.