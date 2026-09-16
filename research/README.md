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
- Stage 10 App-Company Web Strategy & Growth: 077–078 — **PASS**
- Stage 11 Web Operations & Platform Architecture: 079–080 — **PASS**

All passes are foundation/practitioner curriculum gates, not production validation.

## Stage 11 — Web Operations & Platform Architecture — COMPLETE
079 — **Web Operations & Platform Architecture: Deployment, Recovery & PWA Lifecycle — PASS.**  
Establishes requirements-first architecture, runtime/origin/edge/browser version boundaries, environment contracts, artifact/deployment lineage, cache ownership, PWA update compatibility, rollback boundaries, recovery decisions and portability.

080 — **Reliability, Observability, DR & Supply-Chain Integration — PASS / STAGE 11 GATE.**  
Integrates DNS/domain/TLS control, failure-domain mapping, CI/CD promotion and secret/config boundaries, artifact provenance, SLI/SLO/error-budget reasoning, metrics/logs/traces/synthetic/client-local observability, incident operation, backup/restore/RPO/RTO/DR, bad-worker/skipped-version PWA recovery, supply-chain governance and provider portability/TCO.

Stage 11 integrated model:
`critical user task → architecture/failure domains → source/artifact provenance → environment/promotion → DNS/TLS/edge/origin/backend/data → client/worker versions → observation/SLO → incident/recovery → tested restore/RTO/RPO → learning/portability`.

Key guards:
- infrastructure uptime ≠ user-task reliability;
- SLI ≠ SLO ≠ SLA ≠ RTO ≠ RPO;
- source ≠ artifact ≠ deployed release ≠ healthy release;
- secure secret storage ≠ correct secret scope/workflow trust;
- artifact attestation ≠ artifact security;
- analytics ≠ operational monitoring;
- backup exists ≠ restore works ≠ application recovery;
- origin rollback ≠ installed-PWA recovery;
- redundancy ≠ independent failure domain;
- lowest provider bill ≠ lowest total cost.

## Stage 10 — App-Company Web Strategy & Growth — COMPLETE
077 — App-Company Web Portfolio & Lifecycle Strategy — **PASS**.  
078 — Release Governance, Portfolio Growth & Lifecycle Integration — **PASS / STAGE 10 GATE**.

## Stage 9 — Analytics / Experimentation — COMPLETE
075 — Analytics, Measurement & Experimentation Evidence Foundations — **PASS**.  
076 — Measurement Reliability, Causal Inference & Pre-Launch Integration — **PASS / STAGE 9 GATE**.

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations — PASS.**  
074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

075–080 add measurement, portfolio, release and operational transfer. PWA production/device validation remains OPEN. Implementation-level worker/cache/schema/outbox/conflict/backup/transport/telemetry/deep-link validation is a Software Engineering dependency.

Operational PWA guard set:
`origin deployment complete ≠ all installed clients updated`;
`origin rollback complete ≠ installed client recovered`;
`same source ref ≠ same accepted PWA artifact`;
`persistent browser storage ≠ independent backup`.

## Next vertical curriculum — Stage 12 Advanced / Expert Web Management
Highest-value start:
`portfolio governance → ADR/evidence-confidence → reversible/irreversible decision framing → technical/content/operational debt → migration/replatforming → accessibility/privacy/security/analytics governance → cross-specialist conflict resolution → total cost of ownership → expert judgment under uncertainty`.

Use MintTap/LogMate/PWA cases as bounded applications, without inventing production facts.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns web task/information structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability and measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates.

Design Studio remains canonical for reusable visual/interaction evidence. Marketing owns acquisition/channel/community strategy. Software Engineering owns implementation/code/runtime validation. Cross-repository transfer uses explicit evidence boundaries rather than discipline duplication.

## Study quality standard
Substantial studies include precise vocabulary, first-principles mechanics, authoritative evidence, examples/counterexamples, failure diagnosis, cross-domain effects, project relevance without invented production facts, durable vs changeable behavior, and competency/application checks.
