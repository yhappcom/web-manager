# 080 — Stage 11 Reliability, Observability, DR & Supply-Chain Integration

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER INTEGRATED CHECKPOINT / STAGE 11 GATE**
Primary owner: **E Web Architecture, Security & Operations**
Consumers: A Platform/Browser; B UX/IA/Content; C Performance/Accessibility/Quality; D Search/Discovery/Analytics; Software Engineering.

## Purpose
Close the Stage 11 foundation/practitioner operating model by integrating DNS/domain/TLS ownership, failure domains, CI/CD promotion, secret/config governance, observability/SLOs, incident response, backup/RPO/RTO/disaster recovery, software-supply-chain provenance, provider portability and PWA/offline recovery.

This is architecture/operations knowledge, not a claim about the current `minttap.app` production stack. Actual provider, topology, DNS, TLS, CI/CD, backup and monitoring remain OPEN until inspected.

## Source basis
Authoritative material rechecked 2026-09-16:
- Google Cloud Well-Architected reliability guidance: reliability should be scoped from user-experience goals; metrics/logs/traces provide complementary observation; 100% reliability is generally not a rational universal target; recovery from data loss must be tested and evaluated for data integrity, RTO and RPO.
- Google Cloud DR guidance: RTO answers how long service may take to recover; RPO answers how much recent data loss is tolerable. DR must consider application dependencies, not infrastructure in isolation.
- GitHub Actions documentation: deployment environments can gate jobs, restrict branches, require approvals and delay access to environment secrets until protection rules pass. Artifact attestations establish build provenance but do not prove an artifact is secure.
- Firebase Hosting documentation: previous live releases can be retained and rolled back, but this is a hosting-content rollback and does not imply data/config/service-worker recovery.

Provider features and plan availability are CHANGE WATCH. The architecture principles below are provider-independent.

## 1. Reliability starts with a user contract

Do not begin with `99.99%` because it looks professional. Define the user-visible operation first.

`critical user task → acceptable failure mode → SLI → SLO → error budget → detection → response → recovery objective`

Examples of different contracts:
- public marketing page readable;
- support/privacy resource reachable;
- PWA starts offline with previously available local data;
- local flight record can be saved without network;
- queued change can eventually synchronize;
- backup can restore irreplaceable records.

These are different reliability promises and may deserve different objectives.

**CONTRADICTION:** infrastructure uptime alone is not product reliability. A site can return HTTP 200 while serving stale or unusable content; a PWA shell can launch while its core offline task fails.

## 2. SLI / SLO / SLA / RTO / RPO boundaries

- **SLI**: measured indicator of service behavior.
- **SLO**: target for an SLI over a defined population/window.
- **SLA**: external/service agreement; not synonymous with an internal SLO.
- **RTO**: maximum intended recovery duration after a defined disruption.
- **RPO**: maximum intended amount/age of data loss after a defined disruption.

`availability SLO ≠ RTO ≠ RPO`.

For an offline-first product, server availability may degrade while local task availability remains good. Conversely, perfect server uptime does not protect local-only data from device loss.

## 3. DNS, domain and TLS are control-plane dependencies

The domain is a durable product/company identity asset. Treat registrar, authoritative DNS, DNS records, certificate issuance/renewal and hosting binding as separately owned dependencies.

Maintain a **Domain Control Record**:
- registrar and account ownership;
- authoritative DNS provider;
- nameservers;
- critical A/AAAA/CNAME/TXT/CAA or provider-specific records;
- DNSSEC state if used;
- certificate/ACME or managed-certificate ownership;
- renewal/expiry observation;
- app-link/security verification records/files affected by host changes;
- emergency owner and recovery path;
- migration/rollback notes.

A provider outage, accidental DNS change, expired certificate and origin failure are different incidents even if users see the same symptom: site unreachable.

## 4. Failure-domain mapping

Map dependencies before buying redundancy.

`user → recursive DNS → authoritative DNS → network/edge/CDN → origin/runtime → backend/API → persistent data → external dependency`

For each critical task ask:
1. What can fail independently?
2. What shares a provider/account/region/configuration and therefore fails together?
3. Can the task degrade gracefully?
4. Is recovery a data-plane operation or does it require a potentially unavailable management/control plane?
5. What evidence distinguishes one failure domain from another?

**SYNTHESIS:** two services from the same provider are not automatically independent failure domains. Multi-provider complexity is not automatically justified either; use consequence and recovery objectives.

## 5. CI/CD promotion is controlled state transition

Pipeline model:
`source ref → reviewed change → reproducible build → tests/quality gates → immutable artifact/provenance → environment promotion → deployment → health validation → observation window → release acceptance`

Production deployment should not be equivalent to “someone ran a build command from a laptop.”

GitHub environments demonstrate useful generic controls: deployment targets, branch restrictions, reviewers/protection rules and environment-scoped secrets. Exact feature availability depends on plan/repository state and is CHANGE WATCH.

### Secret/config governance
Separate:
- source-controlled non-secret configuration;
- environment-specific non-secret configuration;
- secrets/credentials;
- runtime feature/config state;
- schema/data state.

Rules:
- least privilege and shortest practical credential lifetime;
- environment separation;
- no production secrets in preview artifacts/logs/client bundles;
- rotate/revoke without source rewrite where practical;
- record which release/config version was active during an incident;
- prefer workload identity/OIDC or similarly bounded short-lived authentication over long-lived static cloud keys where the chosen provider supports it.

`secret stored securely ≠ secret safely scoped ≠ workflow safely trusted`.

## 6. Artifact provenance and supply chain

079 established that PWA acceptance attaches to the exact build artifact, not source code alone. Extend that to all production artifacts.

Maintain:
`commit → workflow/toolchain → dependencies/lockfile → build flags → post-build transforms → artifact digest/version → provenance/attestation → environment → deployment ID`

GitHub artifact attestations can cryptographically connect an artifact to workflow/repository/commit/environment provenance. They are useful evidence, but GitHub explicitly notes that an attestation does **not** guarantee artifact security. Verification policy is still required.

Supply-chain operations include:
- pinned/controlled dependency versions;
- dependency update ownership;
- vulnerability/security advisory response;
- build-action/workflow trust review;
- artifact integrity/provenance;
- SBOM where justified;
- emergency dependency replacement path.

Do not add enterprise ceremony without risk justification, but do not accept unverifiable production artifacts for critical offline clients.

## 7. Observability is evidence, not a dashboard collection

Use complementary evidence:
- **metrics** for aggregate rate/latency/error/capacity trends;
- **logs** for timestamped discrete events/state transitions;
- **traces** for request/transaction paths across components;
- **synthetic checks** for controlled externally observed tasks;
- **real-user/product evidence** for actual populations;
- **client-local diagnostics** where offline/PWA state cannot immediately reach the server.

Observation contract:
`signal → population/environment/version → expected range → threshold/burn condition → owner → diagnostic links → action`.

Alert on user-impacting conditions and actionable precursors, not every metric movement. Alert fatigue is a reliability defect.

**CONTRADICTION:** analytics is not deployment monitoring. Stage 9 product analytics can be blocked, sampled, delayed or intentionally minimized; operational health needs independent evidence.

## 8. Error budgets and change velocity

A reliability target implies tolerated failure. Error-budget reasoning prevents two extremes:
- treating any failure as unacceptable and freezing useful change;
- shipping continuously despite repeated reliability regression.

For a niche app company, use simple risk-weighted rules before complex SRE machinery. Example principle:
- healthy budget → normal release cadence;
- accelerated burn or repeated severe incidents → slow risky changes, prioritize reliability work;
- exhausted budget on a critical task → restore reliability before discretionary optimization.

Exact numeric SLOs are **OPEN** until product traffic, user consequences and business requirements are known.

## 9. Incident operating model

`detect → declare/triage → establish scope → contain → communicate → mitigate/recover → validate user task → monitor → preserve evidence → postmortem → corrective action`

Maintain an **Incident Record**:
- start/detection/mitigation/recovery times;
- affected user task/population/version/region;
- symptoms vs confirmed cause;
- release/config/dependency changes;
- actions and decision owner;
- data-integrity implications;
- communication/support impact;
- validation evidence;
- follow-up actions and owner.

Do not force root-cause certainty during early response. Preserve `hypothesis` vs `confirmed cause`.

## 10. Backup, restore, RPO and RTO

A backup is useful only if it can be restored into a functioning system with acceptable integrity/time/data loss.

`backup exists ≠ restore works ≠ application works with restored data ≠ RTO/RPO met`.

Google Cloud reliability guidance explicitly recommends testing restoration in a non-production environment and evaluating data integrity, RTO and RPO across the application stack.

Maintain a **Recovery Contract** per irreplaceable data class:
- authoritative source;
- backup mechanism/frequency;
- retention/versioning;
- independence from primary failure domain;
- encryption/access ownership;
- RPO target;
- RTO target;
- restoration procedure;
- schema/application compatibility;
- last tested restore and result.

For LogMate-like flight records, browser IndexedDB persistence is not an independent backup. A sync copy can improve redundancy but may propagate corruption/deletion; backup semantics still need independent recovery history.

## 11. PWA / offline disaster-recovery model

A PWA introduces client fleets that can remain disconnected during server recovery.

Potential simultaneous populations:
- old HTML/JS with old worker/cache/schema;
- new origin with waiting worker;
- old controlled tab after deployment;
- offline EFB that missed several releases;
- device with unsynchronized outbox;
- device whose local schema migrated before a server rollback;
- device returning after an incident with stale auth/config.

Therefore recovery must reason about:
`server recovery + protocol compatibility + client-version window + local-data integrity + queued-operation replay + user-visible recovery state`.

### Bad service-worker case
A broken worker can interfere with the very navigation used to deliver its replacement. Recovery planning should include:
- worker/script cache-header strategy;
- version detection;
- safe activation rules;
- compatibility window;
- browser-online recovery path;
- user-visible recovery instructions where automatic repair cannot be guaranteed;
- target Safari/iPad validation.

Do not claim that origin rollback automatically removes an already installed worker.

### Skipped-version EFB case
For an EFB returning from N to N+4:
1. preserve local records before destructive migration;
2. identify local schema/protocol/client version;
3. support bounded upgrade path or explicit migration bridge;
4. make queued operations idempotent/deduplicable;
5. reconcile before declaring sync complete;
6. verify backup/export path;
7. test physical managed-iPad constraints.

Implementation remains Software Engineering authority.

## 12. Graceful degradation

Not every dependency failure should make every task fail.

Examples:
- analytics unavailable → core page/task continues;
- marketing image/CDN issue → semantic content remains readable where possible;
- sync server unavailable → local save continues and clearly indicates pending state if product contract permits;
- status/support dependency issue → preserve a minimal independent incident communication path when justified.

But degradation must not silently claim success. `saved locally` and `synchronized` remain separate states.

## 13. Provider portability and cost

Portability is a spectrum, not a binary property.

Track in the existing **Portability Ledger**:
- data export format and egress cost/time;
- DNS/domain portability;
- runtime/API proprietary dependencies;
- auth/identity coupling;
- deployment/build coupling;
- observability/log export;
- serverless/database semantics;
- PWA origin/URL stability;
- migration skill/time;
- outage/exit procedure.

Provider-specific managed features can rationally reduce operational burden. Lock-in is acceptable when benefit exceeds switching/recovery cost and the exit path is understood.

Cost model should include:
`provider bill + engineering time + incident/recovery burden + migration cost + observability/storage cost + reliability complexity`.

Cheapest monthly hosting price is not necessarily lowest total cost.

## 14. Cross-track transfer

### A Platform & Browser
Own DNS/HTTP/cache/browser/service-worker mechanics. Supply actual browser behavior and target-platform change watches.

### B UX/IA/Content
Own maintenance/update/offline/error/recovery communication requirements. Avoid false success states.

### C Performance/Accessibility/Quality
Own release regression, synthetic/real-device validation and accessible degraded states. Reliability fixes must not bypass accessibility/performance gates without explicit incident trade-off.

### D Search/Discovery/Analytics
Consume migration/status/release evidence. Analytics remains observational and cannot substitute for operational truth.

### Software Engineering
Own CI/CD implementation, schema/API compatibility, service-worker code, dependency tooling, tests, backup automation and target-device execution. Web Manager provides requirements, failure models and acceptance contracts.

## 15. Stage 11 competency gate

PASS foundation/practitioner Stage 11 when Web Manager can:
1. derive architecture from behavior/failure/recovery requirements rather than provider preference;
2. distinguish origin/edge/browser/worker/client/data versions;
3. define environment/promotion/config/secret boundaries;
4. connect source→artifact→deployment provenance;
5. map DNS/TLS/CDN/origin/backend/data failure domains;
6. define meaningful SLI/SLO and separate them from SLA/RTO/RPO;
7. design actionable observability and incident evidence;
8. distinguish backup from tested restoration and specify RPO/RTO;
9. reason about PWA/offline client recovery across skipped versions and bad workers;
10. evaluate provider lock-in/portability/cost without assuming either managed or portable architecture is universally superior.

**Result: PASS — Stage 11 FOUNDATION/PRACTITIONER gate closed.**

## Remaining OPEN / next stage
No production certification is implied. `minttap.app` runtime/provider/DNS/TLS/CI-CD/monitoring/backups remain unknown.

Next vertical curriculum: **Stage 12 — Advanced / Expert Web Management**. Move from domain-by-domain competence to portfolio governance, architecture decision records, evidence confidence, debt, migrations/replatforming, cross-specialist conflict resolution, total cost of ownership and expert judgment under ambiguity.
