# MintTap Web Manager Status

Operating state: **ACTIVE — FIVE-TRACK BALANCED DEEP LEARNING + PWA STRATEGIC SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. `LEARNING_ROADMAP.md` is the vertical curriculum; `SPECIALIST_TRACKS.md` is the horizontal five-track model. Web Manager coordinates A Platform/Browser, B UX/IA/Content, C Performance/Accessibility/Quality, D Search/Discovery/Analytics and E Architecture/Security/Operations by evidence, risk, dependency and live-project value. PWA remains a strategic cross-track specialization.

# Curriculum state
Stages 1–11: **COMPLETE — FOUNDATION/PRACTITIONER GATES PASSED.** These are transferable competency gates, not production certification.

- Stage 1 Web Foundations: 027–033
- Stage 2 Website Anatomy / Content / IA: 034–038
- Stage 3 UX & Interaction: 039–044
- Stage 4 Web Design Literacy: 045–050
- Stage 5 Accessibility: 051–058
- Stage 6 Search / Discovery / Content Quality: 059–065
- Stage 7 Performance / Browser Runtime: 066–070
- Stage 8 Security / Privacy / Trust: 071–072
- Stage 9 Analytics / Experimentation: 075–076
- Stage 10 App-Company Web Strategy & Growth: 077–078
- Stage 11 Web Operations & Platform Architecture: 079–080

# Stage 11 closure
079 — **Web Operations & Platform Architecture: Deployment, Recovery & PWA Lifecycle — PASS.**
080 — **Reliability, Observability, DR & Supply-Chain Integration — PASS / STAGE 11 GATE CLOSED.**

Integrated operations model:
`critical user task → architecture/failure domains → source/artifact provenance → environment/promotion → DNS/TLS/edge/origin/backend/data → client/worker versions → observation/SLO → incident/recovery → tested restore/RTO/RPO → learning/portability`.

Retained judgments through 080:
- architecture starts from required behavior, failure tolerance and recovery objectives, not provider selection;
- infrastructure uptime is not equivalent to user-task reliability;
- SLI, SLO, SLA, RTO and RPO are distinct concepts;
- registrar/DNS/TLS/CDN/origin/backend/data are distinct control/failure dependencies even when one vendor operates several;
- source commit ≠ build artifact ≠ deployed release ≠ healthy release;
- environment promotion should bind reviewed source, reproducible artifact, config/schema and validation evidence;
- secrets, non-secret config, runtime feature state and persistent schema/data require separate governance;
- artifact provenance/attestation establishes origin/build evidence but does not prove security;
- metrics/logs/traces/synthetics/client-local evidence serve different observability roles;
- analytics is not operational monitoring;
- backup exists ≠ restore works ≠ application works after restore ≠ RTO/RPO met;
- recovery tests must validate data integrity and the application stack, not only backup-file existence;
- origin rollback ≠ PWA client recovery; offline fleets require worker/cache/schema/protocol/local-data compatibility reasoning;
- provider lock-in is a trade-off, not automatically a defect; total cost includes engineering, incidents, recovery and migration as well as the provider bill.

Reusable Stage 11 controls:
- Environment Contract;
- Release Lineage Record;
- Deployment Compatibility Window;
- Cache Ownership Map;
- PWA Safe Update Contract;
- Recovery Decision Record;
- Portability Ledger;
- Domain Control Record;
- operational SLI/SLO contract;
- Incident Record;
- Recovery Contract for irreplaceable data;
- source→artifact→deployment provenance chain.

# PWA strategic specialization
073–074 establish foundations/data-sync boundaries; 075–080 transfer measurement, portfolio, release and operations knowledge.

PWA guards:
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`local save ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ analytics arrival`.
`origin deployment complete ≠ all installed PWA clients updated`.
`origin rollback complete ≠ installed PWA recovered`.
`same source ref ≠ equivalent PWA artifact when build flags/post-build transforms/origin differ`.

For long-offline EFB clients, skipped-version recovery must preserve local data, identify schema/protocol/client version, support a bounded migration path, replay queued operations idempotently and reconcile before declaring synchronization complete. Physical managed-iPad validation remains product-specific.

# Balanced track state
- **A Platform & Browser:** strong foundation/practitioner; supplies browser/network/cache/worker mechanics.
- **B UX/IA/Content:** strong foundation/practitioner; owns truthful maintenance/offline/recovery states.
- **C Performance/Accessibility/Quality:** substantial foundation/practitioner; production cross-browser/device/AT evidence remains separate.
- **D Search/Discovery/Analytics:** strong foundation/practitioner; measurement and migration evidence boundaries established.
- **E Architecture/Security/Operations:** Stage 11 now closes the major foundation/practitioner gap across deployment, DNS/TLS, observability, incidents, DR, supply chain and portability.

No track is promoted to production certification by curriculum completion.

# Cross-repository evidence
Design Studio remains canonical for reusable visual/interaction evidence; latest known Web Design state is Stage 1/2 PASS, Stage 3 PRACTICE with true-origin/cross-browser/AT/physical-device evidence still open.

Software Engineering owns actual CI/CD implementation, schema/API compatibility, service-worker code, dependency tooling, automated tests, backup automation and runtime/device validation. Web Manager owns the operational contracts and acceptance/failure model.

Marketing owns acquisition/channel/community strategy. Web Manager owns receiving-resource truth, operational continuity and measurement boundaries.

# Production OPEN register
Actual `minttap.app` IA/runtime/framework, provider, DNS/TLS/CDN/origin topology, environments, CI/CD, secret/config model, cache/service-worker policy, schema migration, monitoring/alerts/SLOs, incident process, backups/RPO/RTO, dependency inventory and production PWA role remain OPEN. Do not infer them from curriculum/provider documentation.

# Highest-value next work
Begin **Stage 12 — Advanced / Expert Web Management**. First integrated block should build expert decision governance across portfolio-level ownership, Architecture Decision Records, evidence-confidence/uncertainty, technical/content/operational debt, migration/replatforming, accessibility/privacy/security/analytics governance, specialist conflict resolution, total cost of ownership and reversible-vs-irreversible decisions. Use MintTap/LogMate/PWA scenarios without inventing production facts.

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model.
- `LEARNING_ROADMAP.md`: canonical vertical curriculum.
- `research/README.md`: staged/specialization research index.
- Stages 1–11: COMPLETE at intended foundation/practitioner level.
- Stage 11: **079–080 PASS / CLOSED.**
- Stage 12: **NEXT — Advanced / Expert Web Management.**
- PWA: strategic cross-track specialization active; production/device validation remains product-specific.
- Reporting remains coarse/checkpoint-based.
