# 159 — PWA Recovery-Effect Closure Proof, Downstream Reconciliation & Residual-Risk Expiry

Status: **PASS (generic) / PRODUCT + PROVIDER + DOWNSTREAM + MANAGED-IPAD + RISK-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 157 abort/safe restart; 158 effect reconciliation/compensation; Track A SW/offline mechanics; Track B truthful state UX; Track C destructive closure validation; Track D diagnostics only.

## Why this study exists

158 established that compensation is a new forward transaction and that local success is not proof of semantic rollback. The next failure is premature closure: the originating system marks an incident/effect `CLOSED` after its own compensation succeeds even though another authority domain, downstream consumer, derived artifact, cached client or long-offline PWA still observes or can act on the escaped effect. A second failure is permanent exception drift: residual risk is accepted once and silently becomes an indefinite authority bypass.

## SOURCE

### NIST SP 800-61 Rev. 3 — recovery belongs to continuing risk management
NIST SP 800-61 Rev. 3 (final 2025-04-03) integrates incident response into CSF 2.0 risk management rather than treating recovery as a terminal technical event. Recovery and subsequent improvement remain connected to organizational risk decisions.

Source: https://csrc.nist.gov/pubs/sp/800/61/r3/final

**TRANSFER VALIDATION:** a successful local compensation call is evidence about one action, not sufficient evidence that incident consequences have ceased across all relevant domains.

### NIST SP 800-137 / RMF Monitor — accepted risk remains observable
SP 800-137 defines continuous monitoring as ongoing awareness of security posture, threats/vulnerabilities and control effectiveness so risk can be kept within organizational tolerance and responses can change when controls prove inadequate. NIST's RMF Monitor step likewise requires ongoing assessment, analysis and response rather than a one-time acceptance decision.

Sources:
- https://csrc.nist.gov/pubs/sp/800/137/final
- https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step

**TRANSFER VALIDATION:** residual-risk acceptance cannot be modeled as an immortal boolean. It requires scope, owner/authority, evidence basis, review/expiry triggers and monitoring sufficient to detect when assumptions cease to hold.

### NIST SP 800-39 — risk response and residual risk are organizational decisions
SP 800-39 provides the organization/mission/system model for assessing, responding to and monitoring information-security risk. NIST defines risk response to include accepting, avoiding, mitigating, sharing or transferring risk, and risk tolerance as the level of risk/uncertainty the organization is prepared to bear.

Sources:
- https://csrc.nist.gov/pubs/sp/800/39/final
- https://csrc.nist.gov/glossary/term/risk_response
- https://csrc.nist.gov/glossary/term/risk_tolerance

**TRANSFER VALIDATION:** an operator cannot convert an unresolved consequence into `CLOSED` merely by acknowledging it; acceptance must be attributable to appropriate risk authority and remain bounded by the assumptions under which it was accepted.

### OWASP Top 10:2025 A09 — logging without alerting/action is insufficient
OWASP A09:2025 emphasizes that high-value/auditable events, integrity-protected logs, monitoring, alert thresholds and response escalation are necessary for detection and response. Local-only logs and unmonitored events weaken incident understanding.

Source: https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/

**TRANSFER VALIDATION:** closure proof cannot rely solely on an originating service's success log. Relevant downstream observations and contradiction signals must remain diagnosable.

## SYNTHESIS — closure is a claim with a proof scope

`CLOSED` is not a synonym for `worker finished`, `HTTP 200`, `compensation succeeded`, `ticket resolved`, or `operator accepted risk`.

A consequential recovery effect may move to closure only relative to a declared **closure scope** and **closure invariant**. Conceptually record:
- effect identity and causal lineage;
- escaped consequence and affected authority/data domains;
- downstream dependency/observer set known at decision time;
- each dependency's reconciliation state and evidence freshness;
- future-authority containment evidence;
- compensation/correction/notification results where applicable;
- unresolved residual consequence;
- risk-response decision and authorized owner when residual risk remains;
- acceptance start, expiry/review condition and invalidation triggers;
- monitoring/contradiction signals after closure;
- closure generation and verifier/evidence references.

Persistent guards:
- `local compensation success ≠ effect closure`;
- `provider success ≠ downstream convergence`;
- `all known consumers reconciled ≠ no unknown consumer exists`;
- `closure evidence complete for declared scope ≠ universal absence proven`;
- `risk accepted ≠ risk eliminated`;
- `risk accepted once ≠ risk accepted forever`;
- `ticket closed ≠ authority path closed`;
- `notification sent ≠ recipient state corrected`;
- `cached client stale ≠ server authority stale`;
- `telemetry quiet ≠ consequence absent`.

## Downstream reconciliation graph

Treat a consequential effect as a graph, not one provider row. Nodes can include the authoritative source, IdP/KMS/provider, replicated policy stores, queues, derived projections, notification systems, export artifacts, partner APIs, user-visible caches and offline clients. Edges describe propagation or reliance.

Do not require infinite enumeration. Instead classify dependencies:
1. **authoritative/mandatory** — closure blocked until reconciled or explicitly accepted;
2. **known derived/consumer** — correction, invalidation, notification or bounded residual-risk treatment required according to consequence;
3. **best-effort/non-authoritative** — may not block closure but must not be represented as authoritative truth;
4. **unknown/unobservable** — uncertainty is recorded rather than converted into false certainty.

Closure therefore proves a bounded proposition: the declared invariant holds across the required scope with stated uncertainty. It does not prove that no stale byte or human memory exists anywhere.

## Closure states

A useful generic lifecycle is:
`DETECTED → RECONCILING → CONTAINED → CORRECTING/COMPENSATING → RESIDUAL-RISK-REVIEW → CLOSED-MONITORED`

Branches may include `UNKNOWN`, `MANUAL REVIEW`, `IRREVERSIBLE-CONTAINED`, or `REOPENED`.

`CLOSED-MONITORED` means the declared closure invariant is currently supported and any accepted residual risk remains within its valid governance window. A contradiction or expiry can reopen the effect without erasing the previous closure decision.

## Closure proof

For consequence-bearing effects, closure evidence should answer:
1. **Future authority:** can the escaped credential/grant/policy/lease still authorize new consequence?
2. **Authoritative target:** what does the current authoritative system say?
3. **Mandatory downstreams:** have required consumers converged, invalidated, corrected or been explicitly isolated?
4. **Irreversible consequence:** what remains impossible to undo?
5. **Residual risk:** who accepted it, for what exact scope and assumptions?
6. **Freshness:** is evidence current enough for the consequence?
7. **Contradiction handling:** what signal would reopen the case?

No universal proof algorithm is claimed. The proof burden is consequence-specific.

## Residual-risk acceptance is a lease, not a tombstone

Model acceptance as bounded governance state rather than a permanent exemption. At minimum bind it to:
- specific effect/risk identity and scope;
- explicit assumptions and compensating controls;
- authorized risk owner/decision provenance;
- start time/generation;
- expiry or mandatory review condition;
- event-driven invalidation triggers;
- monitoring evidence needed to keep the acceptance valid;
- required action at expiry: re-evaluate, mitigate, renew through new authority, or remove acceptance.

Expiry does not necessarily mean instant global shutdown. It means the old acceptance no longer independently justifies continued exposure. The consequence-specific policy determines fail-closed, degrade, isolate or require review.

A renewal is a new decision with current evidence; it must not mutate the original acceptance into an apparently timeless approval.

## Event-driven invalidation

Acceptance should become invalid/review-required before nominal expiry when material assumptions change, including examples such as:
- new downstream consumer discovered;
- provider reports contradictory state;
- control/credential/key/policy generation changes;
- accepted containment control fails;
- severity or exposure estimate materially increases;
- legal/regulatory/product requirement changes;
- stale offline client reconnects with an effect that can still alter consequence;
- monitoring evidence becomes unavailable beyond the declared confidence bound.

Exact triggers remain product-specific.

## PWA / Service Worker / managed-iPad application

For a LogMate/EFB-like PWA:
- an old Service Worker or IndexedDB record retaining the historical effect does not by itself mean server authority remains open;
- conversely, a server-side `CLOSED` flag does not prove every offline device has converged;
- reconnect must validate current server authority before replaying queued mutations;
- stale local projections should be corrected/annotated without destroying unique flight data or provenance;
- unsupported/long-offline iPads can remain `LOCAL DATA PRESERVED / REMOTE AUTHORITY REVALIDATION REQUIRED` rather than forcing false convergence;
- closure telemetry may detect reconnect anomalies but cannot authorize replay or establish semantic truth;
- physical WebKit/MDM/storage/background behavior remains OPEN until runtime evidence exists.

## Cross-track integration

### Track A — Platform & Browser
Own exact SW/cache/storage/offline-queue lifecycle. Dependency: distinguish stale local observation from current remote authority and test reconnect invalidation/revalidation.

### Track B — UX / IA / Content
Own truthful states: `RECONCILING`, `CONTAINED`, `RESIDUAL RISK — REVIEW DATE`, `CLOSED — MONITORED`, `REOPENED`, and local-data-preservation states. Avoid `Fixed`/`Undone` where only bounded containment is proven.

### Track C — Performance / Accessibility / Quality
Own destructive closure tests, stale/offline clients, contradictory downstream evidence, expiry/reopen behavior and accessible status/review UX. A passing local API test is not closure proof.

### Track D — Search / Discovery / Analytics
Own diagnostic measurement only. Telemetry can reveal unexpected residual activity or stale-client reconnects; absence of events is not proof of absence and analytics cannot accept risk.

### Track E — Owner
Own closure invariant/scope, downstream classification, risk-acceptance authority, expiry/reopen semantics and evidence governance.

## MINTTAP DECISION — minimal generic model

1. Never derive `CLOSED` solely from local compensation success.
2. Define closure scope/invariant per consequence class and enumerate mandatory downstream authority/consumer domains.
3. Preserve uncertainty: unknown consumers or unknown provider state remain explicit.
4. Require future-authority containment before closure where escaped authority can create new effects.
5. Treat irreversible consequence separately from containment; do not label acknowledgement as compensation.
6. Bind residual-risk acceptance to scope, authority, assumptions, monitoring and expiry/review triggers.
7. Renewal is a new current-evidence decision; old acceptance remains historical provenance.
8. Reopen automatically or require review when a material contradiction/invalidation trigger appears.
9. Keep PWA local-data preservation independent from remote authority convergence.
10. Do not claim product PASS until real provider, downstream, managed-iPad and organizational risk-authority evidence exists.

## VALIDATION — 68-case closure/downstream/residual-risk campaign

1 local compensation 200 but provider unchanged; 2 provider changed but replica stale; 3 replica fixed but queue retains escaped grant; 4 queue drained; 5 derived projection stale; 6 projection invalidated; 7 notification sent; 8 recipient not corrected; 9 mandatory consumer unavailable; 10 mandatory consumer contradictory; 11 unknown consumer discovered after closure; 12 reopen; 13 authoritative credential revoked; 14 stale token presented; 15 reject; 16 lease retired; 17 PITR restores old authority row; 18 anti-resurrection floor rejects; 19 irreversible disclosure; 20 future access contained; 21 correction issued; 22 residual consequence documented; 23 risk acceptance by unauthorized operator; 24 reject; 25 authorized scoped acceptance; 26 expiry reached; 27 old acceptance cannot justify continuation; 28 renewal with current evidence; 29 renewal changes scope and gets new identity; 30 control failure before expiry; 31 acceptance invalidated; 32 provider contradiction before expiry; 33 reopen; 34 severity increase; 35 review; 36 monitoring unavailable; 37 uncertainty raised; 38 analytics quiet but mandatory provider unknown; 39 do not close; 40 all known mandatory consumers reconciled; 41 closure records declared scope not universal absence; 42 new downstream added after closure; 43 dependency graph update; 44 closure re-evaluated; 45 stale SW shows `fixed`; 46 server remains reconciling; 47 server closed but old SW stale; 48 local UI refresh/revalidation; 49 offline queue reconnects after acceptance expiry; 50 replay not authorized by old acceptance; 51 unique local flight data remains readable; 52 export works while remote mutation blocked; 53 local correction preserves provenance; 54 device clock wrong; 55 server/risk generation controls expiry; 56 duplicate closure worker; 57 stable closure generation prevents duplicate consequence; 58 evidence store partial loss; 59 closure confidence degrades/review; 60 accessibility exposes status, expiry and action without color alone; 61 keyboard/focus works; 62 screen-reader wording distinguishes contained from undone; 63 audit excludes bearer secrets; 64 telemetry correlates effect IDs without becoming authority; 65 closure contradiction alert fires; 66 operator cannot suppress mandatory reopen evidence silently; 67 end-to-end long-offline iPad reconnect after monitored closure; 68 drill proves reopen and reclosure without erasing original lineage.

## CONTRADICTION / failure-mode analysis

### Green-dashboard closure
Every local component reports green, but a mandatory external authority remains unknown. Availability telemetry is not semantic reconciliation.

### Infinite-enumeration paralysis
Demanding proof that no stale copy exists anywhere makes closure impossible. Define authoritative and consequence-relevant scope instead of universal byte erasure.

### Permanent waiver
An accepted residual risk without expiry/review becomes silent policy. Treat acceptance as bounded state with currentness requirements.

### Renewal laundering
Editing the original acceptance date/scope destroys provenance. Renewal is a new decision linked to the old one.

### Quiet-telemetry proof
No alerts can mean no problem, no traffic, broken instrumentation or blind spots. Silence is not proof of containment.

### Offline-device false convergence
Deleting or overwriting unique local PWA data to make dashboards converge sacrifices user data without proving remote safety. Preserve local data and separately govern remote authority.

## OPEN

Product/runtime evidence is required for actual downstream graph, authoritative providers, effect classes, closure invariants, risk owners/tolerance, acceptance duration/triggers, alerting/evidence retention, provider reconciliation semantics, LogMate operation identities, offline queue behavior, Service Worker implementation, WebKit/managed-iPad behavior, native-mobile sync and legal/aviation obligations.

## CHANGE WATCH

- NIST incident-response/RMF/continuous-monitoring guidance;
- OWASP logging/alerting guidance;
- provider APIs and commit/reconciliation semantics;
- WebKit/iPadOS storage/background/PWA behavior;
- product/legal/aviation requirements affecting residual-risk authority or retention.

## Gate result

**PASS (generic).** Track E now has a reusable closure-proof/downstream-reconciliation/residual-risk-expiry model. Production validation remains OPEN.

## Next highest-value adjacent work

**PWA recovery-closure evidence retention, verifier independence & closure-claim anti-forgery** — determine how closure evidence remains verifiable without turning the incident ledger into a mutable self-attestation, how independent/provider evidence is retained with privacy minimization, and how stale/forged closure claims are detected across backup/restore, replicas and offline clients.