# 080 — Stage 11 Reliability Operations: DNS/TLS, SLO, DR, Supply Chain & PWA Recovery

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER INTEGRATED CHECKPOINT; STAGE 11 REMAINS ACTIVE**
Primary owner: **E Web Architecture, Security & Operations**
Consumers: A Platform/Browser; C Performance/Accessibility/Quality; D Search/Analytics; B UX/Content; Software Engineering.

## Purpose
Extend 079 from deployment/version topology into operational reliability: DNS/domain/TLS change safety, CDN/origin failure domains, CI/CD promotion and configuration provenance, SLI/SLO/error-budget reasoning, incident evidence, backup/RPO/RTO/DR, dependency/supply-chain operations, provider portability, and PWA recovery. This is transferable web-operations knowledge, not a claim about current MintTap production infrastructure.

## SOURCE — authoritative evidence rechecked 2026-09-16
- Cloudflare DNSSEC documentation: DNSSEC signs DNS data so validating resolvers can authenticate origin/integrity. DNS-provider migration is operationally sensitive: changing nameservers while stale parent-zone DS records remain can cause validating resolvers to return SERVFAIL. DNSSEC therefore adds security and a change-order dependency; it is not a checkbox isolated from registrar/authoritative-DNS operations.
- Let's Encrypt integration/current documentation: ACME automates domain-control validation and certificate issuance/renewal. Renewal should be automated; current guidance recommends checking ACME Renewal Information regularly and, as a fallback, renewing before the final third of certificate lifetime. HSTS converts certificate problems into hard failures, so TLS automation and monitoring must precede aggressive HSTS assumptions.
- Google SRE Workbook: SLOs should be defined from user-relevant SLIs; error budget is the tolerated unreliability implied by an SLO. SLO monitoring identifies user-impacting reliability loss but normally does not identify root cause, so diagnostic telemetry must connect the symptom to intended changes and causal layers.
- Firebase/Firestore documentation: managed export/import can support recovery, but an export is not necessarily an exact snapshot at export-start time. Firestore disaster-recovery options include backups/PITR/clone/export with different recovery characteristics. Current Firestore PITR documentation describes point-in-time recovery up to seven days and explicitly frames RPO/RTO. These are provider capabilities, not proof that a product has a tested recovery plan.
- W3C Service Worker lifecycle remains the platform basis consumed from 079: deployed origin bytes and controlled PWA clients can remain at different generations.

All provider-specific limits, retention windows, platform behavior and product pricing are **CHANGE WATCH**. Revalidate before production decisions.

## 1. Reliability is a user contract, not uptime decoration

Operational reliability should be modeled as:

`critical user task → service boundary → SLI → target/SLO → tolerated failure/error budget → detection → diagnosis → response → recovery → learning`.

A generic homepage 200-rate may be irrelevant if the critical task is store handoff, support access, PWA first frame, local save or synchronization.

Required distinctions:
- availability ≠ correctness;
- HTTP success ≠ readable/operable task success;
- SLI ≠ SLO ≠ SLA;
- alert ≠ incident ≠ root cause;
- telemetry loss ≠ service failure;
- error budget ≠ permission to ignore failures;
- backup exists ≠ restore works;
- RPO ≠ RTO;
- disaster recovery plan ≠ tested recovery capability.

## 2. DNS/domain control is part of production architecture

A domain depends on a control chain:

`registrant/account → registrar → parent delegation/DS → authoritative DNS → records → CDN/origin → TLS identity → application`.

Failures can occur before application code executes. Track:
- registrar ownership/access and recovery path;
- nameserver delegation;
- authoritative provider;
- DNS record inventory/owner;
- TTL/change window;
- DNSSEC state and DS ownership;
- certificate validation dependencies;
- domain expiration/renewal;
- monitoring from outside the provider account.

### DNS migration guard
A DNS migration is not merely copying A/CNAME records. Record old/new authoritative nameservers, TTLs, DNSSEC/DS state, validation method, rollback window and external resolution evidence. With DNSSEC enabled, order matters: stale DS data pointing at keys no longer served can turn a migration into SERVFAIL.

**SYNTHESIS:** stronger controls can increase change sensitivity. DNSSEC improves authenticity/integrity but creates registrar↔DNS-provider coordination requirements.

## 3. TLS/certificate lifecycle

TLS reliability needs:
`domain control → certificate issuance → deployment → renewal → expiry/chain monitoring → revocation/replacement → incident recovery`.

Prefer automated ACME/provider-managed renewal where requirements permit. Monitor the externally served certificate, not merely provider dashboard state.

HSTS is a browser-enforced policy with operational consequences. Do not deploy long-lived/preload-like policy merely because HTTPS currently works; certificate/domain/subdomain ownership and recovery must be mature first.

Create a **Domain & TLS Control Record**:
- domain/host;
- registrar/authoritative DNS owner;
- DNSSEC/DS state;
- certificate issuer/automation owner;
- validation method;
- renewal/expiry monitor;
- HSTS policy;
- dependent subdomains/app-link files;
- emergency recovery owner;
- last external validation.

## 4. CDN/origin failure domains

CDN and origin are not one availability unit. Distinguish:
- DNS unavailable;
- edge unavailable;
- edge serves stale/wrong content;
- origin unavailable while edge can still serve cache;
- origin healthy but unreachable from edge;
- cache purge/refill overloads origin;
- configuration deploy routes traffic incorrectly;
- TLS between user↔edge or edge↔origin fails;
- backend/API fails while static shell remains available.

A cached marketing page may survive origin loss; a dynamic authenticated API may not. PWA cached shell may open while synchronization is unavailable. Therefore status and alerting should represent **task capability**, not one binary site state.

## 5. CI/CD promotion and configuration provenance

079 established release lineage. Extend it to:

`source → dependency/toolchain lock → build → immutable artifact → security/quality checks → environment config/secrets → preview evidence → promotion decision → production deployment → runtime observation`.

Rules:
- build once/promote same artifact where architecture permits; avoid unrecorded rebuild drift;
- configuration and secret versions are release dependencies even when not stored in source;
- preview passing against different backend/auth/config does not certify production;
- deployment identity must be observable in production diagnostics without leaking secrets;
- emergency/manual changes require reconciliation into canonical configuration/history.

Create a **Promotion Evidence Record** containing source/artifact/config identity, required gates, waived gates with owner/reason, production deployment ID and post-deploy validation.

## 6. Secrets and configuration governance

Separate:
- public runtime configuration that is expected to reach browsers;
- server-side sensitive configuration;
- credentials/tokens/secrets;
- environment-specific identifiers;
- signing/deployment authority.

Browser-delivered values cannot be made secret by minification or build-time embedding. Least privilege, scoped identities, rotation/revocation and auditability are operational requirements. Exact secret tooling belongs to the implementation/platform owner.

**CONTRADICTION:** `.env` is a packaging convention, not a security boundary.

## 7. SLI/SLO and error-budget model

Choose SLIs from critical user journeys. Candidate classes:
- successful document/task response;
- latency/task readiness;
- correct store/deep-link handoff;
- support/governance resource availability;
- PWA readable first-frame success under defined network state;
- synchronization success only when measured from authoritative product state, not analytics delivery.

Each SLO record should include population, measurement point, success definition, exclusions, window, target, evidence limits, owner and review date.

Google SRE's error-budget framing is useful as a governance model: `error budget = 1 - SLO` for the chosen indicator. It should control risk/change pace only when the SLI actually represents user impact. A badly chosen SLI can create precise but irrelevant governance.

### Alert hierarchy
`user-impact/SLO alert → release/environment correlation → layer diagnostics → root-cause evidence`.

Do not alert on every internal metric. Use causal diagnostics after a user-impact signal, and retain deploy/config/version annotations.

## 8. Incident operations

Incident sequence:
`detect → declare/scope → stabilize → identify affected task/population/version → preserve evidence → choose rollback/forward-fix/cache/DNS/data action → validate recovery → communicate bounded facts → monitor → postmortem → verify corrective action`.

Operational roles should distinguish incident coordination, technical investigation/change authority and user/status communication when scale warrants it.

A postmortem should identify contributing system conditions, not stop at the operator who executed the final action. Corrective actions need owner, due condition and verification evidence.

Create an **Incident Evidence Packet**:
- start/detection/recovery times;
- affected task/population/locale/device/version;
- SLI/error-budget impact if defined;
- release/config/DNS/cert/worker identities;
- actions and timestamps;
- evidence preserved before destructive recovery;
- user communication;
- causal findings/confidence;
- corrective actions and validation.

## 9. Backup, RPO, RTO and DR

Definitions:
- **backup**: recoverable copy/version of state;
- **RPO**: maximum acceptable data-loss interval measured backward from incident;
- **RTO**: maximum acceptable time to restore required service/task;
- **DR**: coordinated restoration of service after material failure.

Derive RPO/RTO from data/task criticality rather than provider defaults.

For each state class ask:
1. Is it reproducible from source/build?
2. Is it user-created/irreplaceable?
3. What is authoritative source of truth?
4. What corruption/deletion scenarios exist?
5. What backup/PITR/export exists?
6. Is recovery selective or whole-system?
7. Has restore been tested into an isolated target?
8. Are encryption/permissions/retention and deletion obligations preserved?

Firestore managed export is useful but should not be described as an exact start-time snapshot. Provider backup/PITR availability also does not prove application-level consistency across Firestore, Storage, Auth, external systems or offline device state.

Create a **Recovery Capability Matrix**:
`state class → authority → backup mechanism → frequency/retention → RPO → RTO → restore target → consistency dependencies → last restore test → owner`.

## 10. PWA disaster and bad-worker recovery

A PWA incident can persist on clients after origin repair. Failure classes:
- bad worker installed/waiting/active;
- bad cache generation;
- HTML/worker incompatibility;
- IndexedDB migration partially/irreversibly advanced;
- offline outbox contains unsynchronized user operations;
- stale client returns after support window;
- canonical build artifact differs from tested artifact (079 LogMate transfer).

Recovery priorities for user-created offline data:
`preserve/export user state → stop destructive migration/sync → restore readable shell → establish compatible worker/client → reconcile outbox/data → resume sync → validate backup independence`.

Do not use “clear site data” as a generic support fix for an offline-first app containing irreplaceable local records. It can convert a software incident into permanent user-data loss.

### Bad-worker recovery design requirements
- keep worker scope and update path understood;
- retain ability to serve a corrective worker from the registered script URL;
- avoid irreversible cache deletion before data/task recovery evidence;
- design schema migrations for interruption and skipped versions;
- define minimum-supported client protocol and export/recovery path;
- test fresh install, N→N+1, N→N+k, offline restart, update interruption and rollback/forward-fix scenarios;
- distinguish worker recovery from local database recovery.

**EFB transfer:** months-offline managed iPad recovery is a first-class lifecycle scenario, not an edge case to dismiss. Physical Safari/Home Screen behavior remains VALIDATION OPEN.

## 11. Supply-chain and dependency release operations

Dependency governance is not “update everything immediately.” Maintain:
`dependency → purpose → provenance → pinned/locked version → security advisory channel → transitive exposure → runtime/build-only scope → update compatibility → validation → rollback/removal path`.

For generated PWA artifacts, also track build-tool/plugin/post-build provenance because the output worker/cache behavior can differ even when application source is unchanged.

Software Engineering owns code-level dependency controls; Web Operations owns production release provenance, browser/runtime exposure and incident consequences.

## 12. Provider portability and cost under failure

Portability must include more than source code. Evaluate:
- DNS/domain independence;
- artifact/build portability;
- routing/redirect/header configuration;
- edge/server runtime APIs;
- identity/auth coupling;
- database/storage formats and export path;
- logs/observability export;
- secrets/config migration;
- CI/CD/IaC portability;
- PWA origin continuity;
- operational knowledge/runbooks.

Cost model must include normal traffic plus cache-miss/refill bursts, build/deploy usage, logs, backup/storage/export, egress, recovery operations and human operational complexity.

**SYNTHESIS:** lowest steady-state hosting bill can be the more expensive architecture if recovery, portability or operator burden is poor.

## 13. Stress tests

### A. Registrar/DNS provider migration with DNSSEC
Do not flip nameservers first and investigate later. Validate DS/TTL/order and external resolution. Keep rollback timing explicit.

### B. Certificate renewal fails under HSTS
User bypass may be impossible. Alert before expiry and repair certificate/domain validation; do not rely on browser exception behavior.

### C. CDN purge causes origin overload
Treat as a recovery-induced incident. Rate/target invalidation and protect origin capacity.

### D. SLO dashboard green but PWA offline first frame broken
SLI is incomplete. Add the defined critical offline population/task; do not reinterpret green infrastructure metrics as product correctness.

### E. Database deletion with “backup enabled”
Recovery is not established until correct recovery point, permissions, application consistency and isolated restore are demonstrated.

### F. Bad PWA release followed by origin rollback
Old origin bytes may not evict active bad worker/cache/schema. Choose client recovery/forward-fix based on persistent-state compatibility.

### G. Months-offline EFB returns after protocol/schema changes
Preserve local data first; negotiate supported migration/reconciliation or bounded export/recovery. Never force destructive reset as the default.

### H. Framework update changes generated service worker
Artifact provenance is part of release identity. Re-run canonical offline acceptance rather than assuming application-source equivalence.

## 14. Cross-track transfer
- **A:** DNS/HTTP/TLS/service-worker mechanics remain canonical dependencies; E applies operational ordering/failure control.
- **B:** maintenance/update/recovery messaging must preserve task state and explain bounded capability without false reassurance.
- **C:** critical-task SLI candidates and release gates consume accessibility/performance/cross-browser evidence; automated uptime is not quality certification.
- **D:** release annotations and missingness apply to analytics; search migration and status resources consume DNS/URL lifecycle evidence.
- **Design Studio:** latest Web status remains Stage 3 PRACTICE; W026 improves integrated evidence schema but true-origin/cross-browser/AT/physical evidence remains OPEN. Do not claim production UX quality from operations telemetry.
- **Software Engineering:** implement CI/CD, migration, worker recovery, dependency and restore tests; Web Manager supplies required contracts and evidence boundaries.

## 15. MintTap / LogMate OPEN register
Still unknown until product/runtime evidence:
- `minttap.app` registrar, DNS provider, DNSSEC, certificate/HSTS and CDN/origin topology;
- hosting/rendering/provider and environment separation;
- CI/CD/config/secret implementation;
- production SLIs/SLOs/alerts/status process;
- actual backups/PITR/export/restore tests and required RPO/RTO;
- dependency inventory/SBOM practice;
- PWA worker/cache/schema recovery implementation;
- EFB managed-device network/storage/background behavior;
- LogMate canonical PWA rebuild result after the 079 artifact-provenance failure.

## 16. Competency checkpoint
PASS this block if Web Manager can:
1. map domain reliability from registrar through application rather than treating DNS as plumbing;
2. explain why DNSSEC migration order and TLS automation are operational dependencies;
3. define user-task SLIs/SLOs without confusing dashboards with correctness;
4. correlate incidents with release/config/version evidence;
5. distinguish backup/RPO/RTO/PITR/export/restore/DR;
6. reject untested “backup enabled” as recovery proof;
7. reason about bad-worker/cache/schema recovery while preserving offline user data;
8. govern generated PWA artifact provenance as part of supply-chain/release identity;
9. evaluate portability and cost under failure/recovery, not only normal hosting;
10. keep all production-specific claims OPEN pending actual evidence.

**Result: PASS — Stage 11 reliability checkpoint. Stage 11 remains ACTIVE.**

## Next adjacent work
The remaining high-value Stage 11 gap is **architecture/provider decision practice + operational validation design**: compare realistic static/hybrid/PWA deployment topologies against requirements, build a provider-neutral decision record, deepen domain/redirect/app-link migration runbooks, define synthetic/real-user/physical-device monitoring boundaries, and integrate a Stage 11 release/recovery gate. If that bundle passes without unresolved foundation gaps, close Stage 11 and advance to Stage 12 Expert Web Management. Production MintTap/LogMate validation remains separate.