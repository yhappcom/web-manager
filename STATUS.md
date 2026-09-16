# MintTap Web Manager Status

Operating state: **ACTIVE — FIVE-TRACK BALANCED DEEP LEARNING + PWA STRATEGIC SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. `LEARNING_ROADMAP.md` is the vertical curriculum; `SPECIALIST_TRACKS.md` is the horizontal five-track model. Web Manager coordinates A Platform/Browser, B UX/IA/Content, C Performance/Accessibility/Quality, D Search/Discovery/Analytics and E Architecture/Security/Operations by evidence, risk, dependency and live-project value. PWA remains a strategic cross-track specialization.

# Curriculum state
Stages 1–10: **COMPLETE — FOUNDATION/PRACTITIONER GATES PASSED.** These are transferable competency gates, not production certification.

Stage 11 Web Operations & Platform Architecture: **ACTIVE — FOUNDATION/PRACTITIONER.**

079 — **Web Operations & Platform Architecture: Deployment, Recovery & PWA Lifecycle — PASS.**

Integrated operations model:
`requirements → rendering/execution model → origin/backend → edge/CDN/cache → DNS/TLS → deployment/version → browser/service-worker/client state → observation → recovery`.

Retained judgments through 079:
- architecture starts from required behavior/failure tolerance, not provider selection;
- build artifact ≠ deployed release ≠ healthy release;
- origin version ≠ edge-cache version ≠ browser cache ≠ service-worker version ≠ open-client version;
- preview frontend ≠ safe sandbox when it targets production backends/data;
- release lineage should connect source commit, build/toolchain, immutable artifact, environment, deployment ID, config/schema and validation evidence;
- cache invalidation is a correctness problem as well as performance work; broad purge can increase origin load;
- deploying components together does not make user-visible rollout atomic because distributed caches, workers, tabs and offline clients persist;
- PWA update lifecycle adds installing/waiting/activation/control states; forced `skipWaiting()`/`clients.claim()` is a compatibility decision rather than a generic best practice;
- rollback of web bytes ≠ configuration rollback ≠ cache recovery ≠ data recovery ≠ safe service-worker recovery;
- an available rollback button does not prove rollback safety after persistent schema/data changes;
- observability requires environment/version/population/time/missingness context;
- provider lock-in is not automatically bad, but replacement/exit cost must be understood explicitly.

Reusable Stage 11 controls added:
- Environment Contract;
- Release Lineage Record;
- Deployment Compatibility Window;
- Cache Ownership Map;
- PWA Safe Update Contract;
- Recovery Decision Record;
- Portability Ledger.

# PWA strategic specialization
073 — PWA Cross-Track Foundations — **PASS**.  
074 — PWA Data Durability & Synchronization Architecture Boundaries — **PASS**.  
075–079 transfer measurement, portfolio, release and operations knowledge.

PWA guards:
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`local save ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ analytics arrival`.
`origin deployment complete ≠ all installed PWA clients updated`.
`origin rollback complete ≠ installed PWA recovered`.

Current standards confirm independently managed service-worker lifecycle; current WebKit releases continue service-worker fixes, so Safari/iPadOS runtime remains CHANGE WATCH. Physical EFB/iPad validation remains OPEN.

# Balanced track state
- **A Platform & Browser:** strong foundation; supplies HTTP/cache/service-worker mechanics consumed by Stage 11.
- **B UX/IA/Content:** strong; consumes update/offline/maintenance/recovery state requirements.
- **C Performance/Accessibility/Quality:** substantial; release regression and cross-browser/device evidence remain production dependencies.
- **D Search/Discovery/Analytics:** strong foundation/practitioner; consumes migration/status/release-lineage evidence and cannot be used as deployment truth.
- **E Architecture/Security/Operations:** **current largest bottleneck and primary Stage 11 owner**; 079 materially improves deployment/cache/recovery architecture but DNS/TLS operations, reliability/SLO, incident/DR, secret/config governance and provider failure/portability stress tests remain.

# Cross-repository evidence
Design Studio latest checked 2026-09-16: Web Design Stage 1/2 PASS, Stage 3 PRACTICE; true-origin, cross-browser, AT and physical-device evidence remains OPEN. Web Manager does not promote bounded design evidence to production validation.

Software Engineering remains implementation authority for actual CI/CD, schema/API compatibility, service-worker code, sync protocol, automated tests and runtime evidence.

Marketing owns acquisition/channel/community strategy; Stage 11 does not duplicate it.

# Production OPEN register
Actual `minttap.app` framework/rendering model, hosting provider, DNS/CDN/origin topology, environments, CI/CD, cache policy, service-worker strategy, IndexedDB/schema migration, observability/alerts, rollback/data recovery, dependency inventory, backup/RPO/RTO and PWA production role remain OPEN.

Do not infer production capability from generic platform/provider documentation.

# Highest-value next work
Continue Stage 11 with a large integrated reliability block: **DNS/domain/TLS operations → origin/CDN failure domains → CI/CD promotion + secret/config governance → monitoring/SLO/incident evidence → backup/RPO/RTO/disaster recovery → dependency/supply-chain release operations → provider portability/cost stress tests**. Use bad-worker recovery, skipped-version offline clients and EFB Safari/iPad constraints as major PWA cases. Then assess whether a second Stage 11 integration block is sufficient to close the gate.

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model.
- `LEARNING_ROADMAP.md`: canonical vertical curriculum.
- `research/README.md`: staged/specialization research index.
- Stages 1–10: COMPLETE at intended foundation/practitioner level.
- Stage 11: **ACTIVE; 079 PASS.**
- PWA: strategic cross-track specialization active; production/device validation OPEN.
- Reporting remains coarse/checkpoint-based.