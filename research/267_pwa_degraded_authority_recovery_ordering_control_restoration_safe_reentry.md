# 267 — PWA Degraded-Authority Recovery Ordering, Control-Restoration Proof & Safe Re-entry Under Partial Fleet Convergence

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/update/fencing mechanics; Track B degraded/re-entry UX; Track C destructive validation; Track D bounded convergence/control-health measurement.  
Dependencies: 117–121 containment/normalization, 127–130 degraded mode/recovery objectives, 249–266 policy distribution, fleet convergence, topology/exception governance, breach response and contingency exit proof.

## Problem

266 established that exception-budget breach is not a kill command, compensating controls can decay semantically, and re-entry requires evidence rather than dashboard arithmetic. The next failure boundary is recovery ordering: several controls can recover at different times, central systems can look healthy before the fleet converges, and long-offline clients can return after ordinary operation has already resumed centrally.

Two symmetric errors dominate. First, one restored control can be treated as proof that the whole authority path is safe, reopening mutation/publication while identity, policy, rejection, queue, provenance or recovery controls remain stale. Second, operators can wait for impossible universal fleet simultaneity and thereby prolong unsafe exception paths or deny preservation/recovery functions unnecessarily.

Central rule: **re-entry is a consequence-scoped prerequisite graph, not a single green bit. A restored component/control proves only its own bounded claim. High-consequence authority reopens only when the required current controls and assumptions for that consequence are jointly satisfied, with partial/offline fleet convergence retained as explicit debt and late-returning clients forced through current admission/reconciliation rather than inheriting central re-entry.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns Service Worker/client control, cache/storage/queue persistence, navigation/update lifecycle and observable runtime boundaries. A current worker cannot prove current semantic authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `recovery-only`, `re-entry pending`, `limited sync`, `publication blocked`, `client update required`, `late rejoin reconciliation` and data-preservation states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **888 → 896 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer. Measures restoration evidence, cohort/fleet convergence, stale-tail size, predecessor rejection and re-entry regressions; metrics cannot grant authority.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns prerequisite graphs, restoration proof, staged authority reopening, late-tail governance, rollback/re-degradation and closure semantics.

## SOURCE

### NIST SP 800-34 Rev. 1 — recovery is followed by validation/reconstitution before normal operation

NIST SP 800-34 Rev. 1 separates recovery from reconstitution. Reconstitution includes testing and validating system capability and functionality before returning operation to normal state; validation can include functionality/regression testing and data validation. The guide also assigns explicit recovery/reconstitution roles and coordination responsibilities.

Source: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf

**TRANSFER VALIDATION:** supports treating restoration and return-to-normal as distinct states and requiring validation before ordinary operation. It does not define a PWA authority graph, fleet convergence threshold or LogMate aviation policy.

### NIST SP 800-137 / RMF Monitor — current control effectiveness must remain visible

NIST SP 800-137 frames continuous monitoring around ongoing visibility into deployed-control effectiveness and alignment with risk tolerance. The RMF Monitor step calls for ongoing assessment, analysis/response and ongoing authorization using current monitoring results.

Sources: https://csrc.nist.gov/pubs/sp/800/137/final  
https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step

**TRANSFER VALIDATION:** supports current-evidence re-entry and re-degradation when restored controls later become inadequate. It does not make telemetry an authorization oracle and cannot prove unseen long-offline clients safe.

### Service Worker lifecycle — activation/control are client/runtime states, not fleet-wide semantic convergence

MDN documents that a newly installed Service Worker can remain waiting while an older worker controls open pages; `skipWaiting()` can request immediate activation, while `clients.claim()` lets an active worker take control of clients within its scope. Client control therefore has lifecycle semantics distinct from organizational authority, backend policy and fleet convergence.

Sources: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers  
https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting  
https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim

**TRANSFER VALIDATION:** supports the Track A boundary that worker activation/control cannot by itself prove policy, data, credential or fleet currentness. Browser/OS-specific runtime validation, especially installed iPadOS PWA behavior, remains OPEN.

## SYNTHESIS 1 — recovery is a graph, not a sequence of green lights

For each consequence, define the current prerequisites needed before authority reopens. Example generic dimensions can include:
- current identity/session/bootstrap authority;
- current policy/projection floor;
- server-side predecessor rejection/fencing;
- compatible schema/data/provenance state;
- queue/retry admission rules;
- compensating-control applicability where still needed;
- required observability/audit evidence;
- rollback/re-degradation capability.

The graph is consequence-specific. Read/recovery can have fewer prerequisites than remote mutation; publication/finalization can require more.

Guards:
- `one control restored ≠ authority path restored`;
- `all controls green individually ≠ required dependency composition proven`;
- `recovery ordering ≠ arbitrary operational checklist`.

## SYNTHESIS 2 — restoration proof is claim-scoped

A control-restoration record should bind at least:
- control/version/authority identity;
- consequence and topology scope;
- assumptions/dependencies;
- validation method and environment;
- time/policy/configuration generation;
- observed result and known blind spots;
- accountable verifier/decision provenance.

A restored server rejection rule does not prove client queue reconciliation. A restored identity provider does not prove stale projections rejected. A new Service Worker does not prove old offline operations safe.

Guard: `control restored ≠ dependent controls restored`.

## SYNTHESIS 3 — safe re-entry is staged by consequence

A generic staged model can be:
1. **PRESERVE/INSPECT** — unique data/provenance readable/exportable where policy permits; no stale mutation authority inferred.
2. **RECOVERY-ONLY** — bootstrap, repair, migration and reconciliation paths available; ordinary mutation remains fenced.
3. **LIMITED MUTATION** — bounded current operations admitted after identity/policy/schema/rejection prerequisites pass.
4. **SYNC/REMOTE EFFECT** — queued/current remote effects admitted with current idempotency/conflict/replay controls.
5. **PUBLICATION/FINALIZATION** — highest-consequence action reopened only with its complete current prerequisite set.
6. **NORMAL** — ordinary policy applies, while unresolved offline/unknown tail remains separately governed if consequence permits.

This is a generic reasoning model, not a prescribed LogMate state machine.

Guard: `lower-consequence re-entry ≠ higher-consequence re-entry`.

## SYNTHESIS 4 — central recovery does not imply fleet recovery

Central policy, backend rejection and online-client convergence can be current while long-offline devices remain on obsolete worker/cache/policy/queue state. Central operation may re-enter if the consequence model permits, but the unresolved tail remains explicit assurance debt with a rejoin contract.

Guards:
- `central re-entry ≠ fleet convergence`;
- `online cohort current ≠ offline cohort current`;
- `partial convergence accepted ≠ stale tail forgotten`.

## SYNTHESIS 5 — late-returning clients do not inherit central re-entry

A client returning after central re-entry must establish its own current admission prerequisites. Generic order:
1. preserve unique local records/queue/provenance;
2. identify device/incarnation and local policy/schema/worker generations;
3. prevent obsolete consequence-bearing operations from auto-replaying;
4. obtain current bootstrap/policy/authority;
5. reconcile local data and queued operations individually;
6. reject/rebase obsolete operations under current rules;
7. produce current acknowledgement/checkpoint where required;
8. enter only the consequence states actually proven for that client.

Guard: `fleet reopened ≠ returning client pre-authorized`.

## SYNTHESIS 6 — Service Worker currentness is not re-entry authority

`skipWaiting()` and `clients.claim()` can accelerate worker activation/control for reachable clients, but they do not prove:
- every installed/offline client fetched the worker;
- IndexedDB/Cache Storage/queue schema is semantically current;
- server policy or credential state is current;
- queued operations remain authorized;
- organizational topology admission is current.

Guards:
- `Service Worker active ≠ authority restored`;
- `clients.claim() completed ≠ fleet converged`;
- `cache generation current ≠ domain state current`.

## SYNTHESIS 7 — re-entry needs predecessor rejection, not only successor success

Positive successor tests are insufficient when obsolete paths could still execute. Where consequence warrants, re-entry evidence should include negative tests or equivalent proof that predecessor credentials/routes/projections/operations are rejected or safely quarantined.

Guards:
- `successor request succeeds ≠ predecessor request fails`;
- `new path healthy ≠ old path harmless`.

## SYNTHESIS 8 — recovery evidence can regress

A control that passed restoration can become stale again because configuration, topology, credential, policy, browser/runtime or operator coverage changes. Re-entry is therefore revocable. A material contradiction should move affected consequences back to a bounded degraded state rather than preserving `NORMAL` for appearance.

Guards:
- `re-entry granted once ≠ re-entry permanent`;
- `previous restoration PASS ≠ current restoration PASS`.

## SYNTHESIS 9 — rollback/re-degradation is part of re-entry proof

Before reopening high-consequence authority, define how to return to a safe degraded state if a restored control fails or contradiction appears. A path that can only move forward to NORMAL but cannot safely fence consequence-bearing authority again is incomplete operational evidence.

Guard: `forward recovery works ≠ safe re-degradation works`.

## SYNTHESIS 10 — quorum/count metrics cannot substitute for consequence analysis

“95% fleet updated” can be useful telemetry but cannot by itself authorize publication or prove the remaining 5% harmless. A single stale privileged/admin/recovery client can matter more than many read-only clients. Conversely, waiting for 100% of retired/unreachable devices can be meaningless if they are authoritatively fenced and governed.

Guards:
- `fleet percentage ≠ semantic safety threshold`;
- `100% observed online ≠ 100% possible consumers`;
- `one stale privileged client ≠ one ordinary stale client`.

## SYNTHESIS 11 — unknown/offline tail requires disposition classes

Useful generic classes include:
- current and acknowledged;
- current but acknowledgement pending;
- offline/unknown with current server-side fence;
- offline/unknown requiring rejoin reconciliation;
- retired with authoritative rejection;
- lost/unrecoverable under governed disposition;
- contradicted/under investigation.

These states prevent `unknown` from collapsing into either `safe` or `compromised`.

Guard: `unknown tail ≠ safe tail ≠ compromised tail`.

## SYNTHESIS 12 — data preservation and authority restoration remain asymmetric

A late device may hold irreplaceable legitimate data under obsolete authority. Recovery should preserve the data/provenance first while withholding stale mutation/publication authority until current admission/reconciliation succeeds.

Guards:
- `data worth preserving ≠ operation worth replaying`;
- `record recoverable ≠ record publishable`;
- `authority stale ≠ data disposable`.

## SYNTHESIS 13 — control dependencies can create unsafe circular re-entry

Example: queue reconciliation waits for current policy; policy activation waits for client acknowledgement; acknowledgement is emitted only after queue drain. Such cycles can deadlock or tempt operators to bypass a prerequisite. The prerequisite graph should expose cycles and define an explicit recovery bridge that grants only the minimum authority needed to break the cycle.

Guard: `dependency cycle discovered ≠ bypass all gates`.

## SYNTHESIS 14 — emergency recovery bridges expire after their purpose

A bounded bridge used to obtain current policy, export data or migrate schema must not silently become ordinary mutation authority after recovery. It inherits the exception lifecycle from 263–266: owner, purpose, scope, expiry/review, compensating controls and retirement evidence.

Guard: `recovery bridge succeeded ≠ recovery bridge normalized`.

## SYNTHESIS 15 — operator-visible state must preserve uncertainty

Track B should not collapse `re-entry pending`, `recovery-only`, `limited sync`, `publication blocked`, and `late client reconciliation` into generic “offline/error”. Operators/users need the consequence distinction to avoid destructive retry or false assurance. Exact wording and interaction require Design Studio/human/AT validation.

Guard: `clear-looking status ≠ truthful status`.

## SYNTHESIS 16 — observability proves only observed cohorts/surfaces

Track D can measure worker versions, policy acknowledgements, rejection counts, queue age and cohort convergence where instrumented. Absence of stale traffic cannot prove absent stale devices. Analytics may trigger investigation/re-entry review but cannot grant authority.

Guard: `zero stale traffic ≠ zero stale clients`.

## SYNTHESIS 17 — re-entry closure is an evidence bundle

A consequence can close re-entry obligations only when the required current prerequisites are evidenced, contradictions are dispositioned, residual offline/unknown tail has a governed rejoin/retirement path, and rollback/re-degradation remains viable. Closure is scoped to that consequence and topology.

Guard: `re-entry closed for sync ≠ re-entry closed for publication`.

## SYNTHESIS 18 — do not require impossible simultaneity

Safe staged re-entry does not require every component/device to transition at the same instant. It requires authoritative fences and admission boundaries that prevent stale cohorts from exercising consequences they have not requalified for. This converts partial convergence from a hidden race into explicit governed debt.

Guard: `not simultaneous ≠ unsafe if stale consequence is authoritatively fenced`.

## Track C destructive campaign additions — 888 → 896

1. **single-green-control reopen:** restore identity while policy/rejection remains stale; system reopens publication. Expected: publication remains blocked.
2. **fleet-percentage laundering:** 99% update metric reopens high-consequence authority while one stale privileged client remains unfenced. Expected: consequence-aware tail handling.
3. **late-client inherited authority:** long-offline iPad reconnects after central NORMAL and auto-replays obsolete queue. Expected: preserve then current rejoin/revalidation.
4. **Service-Worker-current theater:** `skipWaiting()`/`clients.claim()` succeeds and is treated as semantic/fleet convergence. Expected: bounded runtime claim only.
5. **successor-only re-entry:** N2 positive test passes while E1 predecessor remains accepted. Expected: predecessor rejection/fencing evidence required where material.
6. **restoration-regression blindness:** control passes restoration, topology changes, authority remains NORMAL without reassessment. Expected: re-degrade affected consequence.
7. **recovery-cycle bypass:** circular prerequisites cause operator to disable all gates. Expected: bounded minimum recovery bridge with lifecycle.
8. **data-authority collapse:** obsolete client contains unique records; system either deletes records or blindly publishes them. Expected: preserve data, separately reauthorize operation.

These are defined cases, not executed product evidence.

## EFB / LogMate-like application case

Scenario: central N2 sync and server predecessor rejection recover after a breach. Most online clients have current policy P14, but a company iPad has been offline for six weeks with worker W8, policy P11, queue Q11 and unique flight records. Central operation has already re-entered ordinary service for current clients.

Generic safe sequence:
1. central re-entry remains scoped to clients/consequences satisfying current prerequisites;
2. the returning iPad does not inherit central NORMAL;
3. preserve unique flight records, Q11 and provenance before migration/reconciliation;
4. fence Q11 auto-replay and obsolete P11 consequence-bearing operations;
5. establish current device/incarnation/bootstrap authority;
6. update/runtime-migrate as needed, without treating W14 activation as semantic clearance;
7. reconcile each queued operation against P14/current schema/conflict/idempotency rules;
8. require current acknowledgement/checkpoint for consequences that need it;
9. test that obsolete predecessor operations are rejected where material;
10. admit the iPad progressively to the consequence states it has actually proven;
11. retain any still-unseen fleet tail as explicit assurance debt rather than delaying all current clients or declaring universal convergence.

This is a generic architecture pattern, not a claim about actual LogMate implementation, MDM, iPadOS behavior, aviation requirements or backend semantics.

## MINTTAP DECISION / DIRECTION

For future product-specific governance, prefer:
- consequence-scoped prerequisite graphs over one global recovery bit;
- staged re-entry with preservation/recovery separated from mutation/publication;
- restoration evidence bound to control/version/topology/policy and known blind spots;
- negative predecessor rejection evidence where stale paths could remain consequential;
- late-returning clients requalified independently of central re-entry;
- explicit offline/unknown-tail debt and rejoin contracts;
- rollback/re-degradation capability as part of high-consequence re-entry proof;
- Service Worker/client-control evidence as Track A runtime evidence only, never semantic authorization.

Do not set numeric fleet thresholds, exact capability classes, approval roles or aviation/legal policy until canonical product/domain evidence exists.

## OPEN

- Actual MintTap/LogMate consequence classes and re-entry prerequisite graph.
- Actual managed-iPad/MDM/ADE topology and iPadOS/WebKit installed-PWA behavior.
- Actual Service Worker/cache/IndexedDB/queue/backend update and rejection semantics.
- Actual identity/session/bootstrap/policy/projection/checkpoint generations.
- Actual fleet inventory, offline-tail governance and retirement semantics.
- Actual rollback/re-degradation mechanisms and recovery bridges.
- Aviation/legal/privacy/safety requirements.
- Physical-device, screen-reader, representative-human and exact-product runtime evidence.

## CHANGE WATCH

- Apple/WebKit/iOS/iPadOS PWA lifecycle/storage/background/update behavior.
- Managed-device enrollment/restore/Return-to-Service behavior.
- Service Worker specification/browser implementation changes affecting update/control semantics.
- NIST contingency/reconstitution/continuous-monitoring guidance revisions.
- Product topology, authority model, consequence classification and offline policy.

## Persistent guards added

- `one control restored ≠ authority path restored`;
- `control restored ≠ dependent controls restored`;
- `lower-consequence re-entry ≠ higher-consequence re-entry`;
- `central re-entry ≠ fleet convergence`;
- `fleet reopened ≠ returning client pre-authorized`;
- `Service Worker active ≠ authority restored`;
- `clients.claim() completed ≠ fleet converged`;
- `cache generation current ≠ domain state current`;
- `successor request succeeds ≠ predecessor request fails`;
- `re-entry granted once ≠ re-entry permanent`;
- `forward recovery works ≠ safe re-degradation works`;
- `fleet percentage ≠ semantic safety threshold`;
- `unknown tail ≠ safe tail ≠ compromised tail`;
- `data worth preserving ≠ operation worth replaying`;
- `dependency cycle discovered ≠ bypass all gates`;
- `recovery bridge succeeded ≠ recovery bridge normalized`;
- `zero stale traffic ≠ zero stale clients`;
- `re-entry closed for sync ≠ re-entry closed for publication`;
- `not simultaneous ≠ unsafe if stale consequence is authoritatively fenced`.

## Gate result

**PASS (generic).** The Web Manager can now model degraded-authority recovery as a consequence-scoped prerequisite graph; distinguish component restoration from composed authority restoration; stage re-entry without destructive data handling; govern partial fleet convergence and late-returning clients; require predecessor rejection and re-degradation evidence; and keep Service Worker/client-control semantics within their proper runtime boundary. Product implementation and runtime validation remain OPEN.

## Next high-value target

**268 — re-entry prerequisite attestation integrity, cross-control evidence correlation & false-composition resistance.** Determine how independent-looking green prerequisites can share a hidden failure domain, stale evidence epoch or compromised verifier; prevent individually valid attestations from composing into a false high-consequence re-entry decision; and define bounded challenge/revalidation when evidence sources disagree.