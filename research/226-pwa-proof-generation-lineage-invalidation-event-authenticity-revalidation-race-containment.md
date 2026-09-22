# 226 — PWA Proof-Generation Lineage, Invalidation-Event Authenticity & Revalidation-Race Containment

Status: **PASS (generic) / PRODUCT + EVENT-PIPELINE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/Service Worker mechanics; Track B revalidation/recovery UX; Track C race/regression evidence; Track D invalidation/revalidation telemetry.  
Dependencies: 218–225, especially proof dependency manifests, multi-plane discovery, graph drift, change-triggered invalidation and stale-proof expiry.

## Problem
225 made proof validity dependent on claim, dependency generations, evidence state and freshness. The next failure is concurrency. A revalidation can begin against generation G, observe some dependencies, continue while IAM, provider policy, recovery state, deployment, Service Worker or evidence collectors move to G+1, and then publish a green result assembled from mutually incompatible observations. Even if every individual observation was authentic, the aggregate proof may never have described one real system state.

Central rule: **a proof must identify the generation/observation interval it actually assessed and must not be published as CURRENT when material dependencies changed outside the bounded assessment snapshot. Event authenticity, event completeness and state currentness are separate claims. Revalidation must contain TOCTOU races without assuming an impossible global transaction across browsers, providers and offline clients.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Service Worker waiting/active/controller transitions can race with validation and differ per client. Browser mechanics supply generation facts but do not prove fleet-wide atomicity.
- **B UX/IA/Content:** high dependency pressure. A capability can be REVALIDATING or generation-skewed while local data remains safe; UI must not collapse this into false data loss or false global-current claims.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns race oracles, start/end snapshot assertions and negative stale-generation tests. Campaign expands **560 → 568 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures invalidation latency, event lag, proof publication lag, generation skew and race retries; telemetry does not make a proof authoritative.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns proof lineage, event provenance, snapshot/fence semantics, monotonic publication and enforcement consumption.

## SOURCE

### NIST continuous monitoring / configuration-change precedent
NIST RMF/SP 800-53 separates configuration change control, security-impact analysis and continuous monitoring. NISTIR 8212 provides an assessment methodology for information-security continuous-monitoring programs. Reusable principle: observation and assessment are ongoing processes; a previous assessment is not a timeless statement about a changing system.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://www.nist.gov/publications/iscma-information-security-continuous-monitoring-program-assessment

**TRANSFER VALIDATION:** NIST does not define a MintTap generation-fence protocol. It supports explicit assessment scope/currentness rather than assuming a mutable system stayed unchanged while it was assessed.

### TOCTOU is a real security failure class
NVD records concrete CWE-367 Time-of-check Time-of-use vulnerabilities, including CVE-2024-7348 and CVE-2024-50379. The reusable principle is not the affected software: a security decision can become invalid when the object/state changes between check and use.

Sources:
- https://nvd.nist.gov/vuln/detail/CVE-2024-7348
- https://nvd.nist.gov/vuln/detail/CVE-2024-50379

**TRANSFER VALIDATION:** these CVEs do not prescribe web assurance architecture. They validate TOCTOU as a concrete failure class and motivate binding assessment and consumption to current state.

### Service Worker lifecycle is explicitly non-atomic across publication, activation and client control
Current MDN documentation distinguishes installation, waiting, activation and effective client control. `skipWaiting()` can move a waiting worker toward activation; `Clients.claim()` lets an active worker take control of clients in scope and emits `controllerchange` for affected clients. These mechanics make per-client generation skew normal rather than exceptional.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting
- https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim

**CHANGE WATCH:** generic API mechanics are current; exact Safari/iPadOS/managed-EFB lifecycle behavior and timing require physical/runtime evidence.

## SYNTHESIS 1 — proof lineage needs an assessed interval, not only a creation timestamp
A high-consequence proof should record at least:
1. proof ID and predecessor/supersession lineage;
2. claim/capability and scoped enforcement denominator;
3. assessment start fence/vector;
4. dependency generations observed during assessment;
5. assessment end fence/vector;
6. material changes/events observed inside the interval;
7. event-source provenance and reconciliation state;
8. positive/negative oracle set and results;
9. publication generation;
10. validity preconditions consumed by enforcement.

A green test created at 14:05 does not mean the system was one coherent 14:05 state.

`proof timestamp ≠ coherent assessed state`; `all observations authentic ≠ observations co-temporal`.

## SYNTHESIS 2 — reject mixed-generation proof publication
Example: validation reads IAM G20, then provider routing changes G31→G32, then the validator reads recovery G11 and tests the application artifact. Every read can be authentic while the resulting bundle describes no single accepted security state.

Before publication, compare the end fence/current dependency vector with the dependencies assumed by the assessment. If a material dependency changed, either:
- re-run only the affected claim closure when a bounded unaffected cut is proven; or
- invalidate/restart the wider assessment when impact is UNKNOWN/CONTRADICTED.

`each check PASS ≠ aggregate proof PASS`; `latest value per field ≠ coherent snapshot`.

## SYNTHESIS 3 — use fences/vectors, not an assumed global transaction
Web/provider/browser/offline systems generally cannot participate in one global serializable transaction. Do not invent one. Use explicit generation/fence tokens per material dependency or authority domain and a claim-specific vector of required generations.

Publication can be monotonic if a proof is accepted only when:
- its predecessor/current-selection lineage is known;
- its required dependency vector is not older than the enforced security floor;
- no material invalidation event after the assessed fence is unresolved;
- any changed dependency has been revalidated or proven outside the claim cut.

This is a logical assurance fence, not a claim that distributed state is physically simultaneous.

`no global transaction ≠ no race containment`; `monotonic generation ≠ wall-clock order`.

## SYNTHESIS 4 — invalidation-event authenticity, completeness and ordering are separate
A signed provider webhook may be authentic yet delayed, duplicated, reordered or incomplete. A poll may observe current state yet miss intermediate security-relevant transitions. Record source identity, event ID/sequence when available, event generation, observed-at time, delivery/reconciliation status and affected dependency.

State reconciliation closes some omission risk; event history preserves transition evidence. Neither alone replaces the other.

`event authentic ≠ event complete`; `event sequence present ≠ no omitted event`; `current state same as before ≠ no consequential intermediate transition`.

## SYNTHESIS 5 — proof issuance and proof consumption form another TOCTOU boundary
Even a coherent proof can become stale immediately after publication. Enforcement must not ask only “is proof P signed/green?” It must compare P's dependency/security floor with the current admission floor and known invalidations at use time.

For high-consequence operations, consumption should fail or restrict when:
- a required dependency generation is newer than P;
- an unresolved material invalidation exists;
- proof lineage is superseded/revoked;
- the consumer cannot establish the required current floor.

`proof valid when issued ≠ proof valid when consumed`; `proof signature valid ≠ admission current`.

## SYNTHESIS 6 — race-safe revalidation needs bounded restart semantics
Do not allow endless full-suite restart for irrelevant churn. When change Δ arrives during assessment:
1. map Δ to claims through the dependency graph;
2. preserve unaffected completed evidence only if its cut remains proven;
3. invalidate affected observations/oracles;
4. re-run from the earliest dependency boundary needed for closure;
5. widen to full restart only when impact cannot be bounded.

This prevents both unsafe mixed-generation reuse and operational denial caused by unrelated noisy changes.

`change during validation ≠ always full restart`; `partial reuse ≠ reuse without dependency proof`.

## SYNTHESIS 7 — Service Worker control makes PWA validation client-relative
A validator observing registration.active does not prove every relevant client is controlled by that worker. `Clients.claim()` can alter control of existing clients, and `controllerchange` exposes a client-side transition. Therefore PWA proof can require a cohort/client-control denominator when the claim depends on effective worker control.

For long-lived/offline clients, distinguish published, installed/waiting, active and client-controlling generations plus data/schema/policy generations.

`active worker observed ≠ target client controlled`; `controller changed ≠ data/schema migration complete`.

## SYNTHESIS 8 — long-offline return cannot consume historical proof atomically
A LogMate-like iPad may reconnect while server-side revalidation is itself in progress. Preserve unique local flight/logbook data first. Do not use an old proof because it was current when the operation was queued, and do not use a new proof until the admission service can bind it to the current security floor.

If current admission is indeterminate, local data entry may continue when its trust cut is unaffected, while consequence-bearing remote sync remains restricted. Once current authority is established, queued operations are re-admitted individually.

`reconnected during revalidation ≠ authorized by old or future proof`; `data preservation ≠ proof consumption`.

## SYNTHESIS 9 — rollback/PITR can create lineage forks, not just older versions
A restored evidence database can contain proof P12 as “latest” while another surviving plane knows P15 and its invalidations. Recovery must reconcile proof lineage/current-selection state before admission resumes. A restored historical proof cannot win because its local database clock or row version appears newest.

`restored latest row ≠ globally current proof`; `PITR success ≠ proof-lineage convergence`.

## SYNTHESIS 10 — evidence collectors must expose observation generation
Collector output without the source generation/observation interval invites false composition. Where source-native generation is unavailable, record the strongest available bounded observation context and classify uncertainty rather than inventing exactness.

A collector upgrade or permission change can itself invalidate evidence assumptions and requires revalidation of source coverage.

`collector says green ≠ source generation known`; `unknown generation ≠ current by default`.

## SYNTHESIS 11 — enforcement should consume current-selection semantics, not “latest PASS” queries
Never select proof by maximum timestamp alone. Current selection must reject invalidated/superseded/forked proofs and enforce claim/security-floor compatibility. Historical proof remains queryable for audit but cannot satisfy current admission.

`latest timestamp ≠ current authority`; `historical lineage retained ≠ historical proof reusable`.

## SYNTHESIS 12 — publication races need negative tests
A correct implementation must test more than successful publication:
- dependency changes between last oracle and publish;
- event arrives after publish but carries an earlier effective generation;
- duplicate/out-of-order event delivery;
- proof DB PITR restores an older current pointer;
- Service Worker controller changes during client validation;
- collector permission changes during assessment;
- long-offline client reconnects during proof transition;
- two validators race to publish proofs over different dependency vectors.

The oracle is not “one proof won.” It is that no proof becomes CURRENT unless its claim-specific dependency floor and lineage are valid.

## MINTTAP DECISION / DIRECTION
1. Extend high-consequence proof objects with start/end assessment fences, dependency-generation vectors and predecessor/supersession lineage.
2. Reject mixed-generation proof publication when material dependencies changed during assessment and were not revalidated or proven outside the claim cut.
3. Use per-domain generation/fence semantics; do not assume a global transaction across provider/browser/offline systems.
4. Treat event authenticity, completeness, ordering and state reconciliation as separate evidence claims.
5. Re-check proof currentness at enforcement consumption, not only at proof issuance.
6. Use graph-directed bounded restart semantics for changes during revalidation; widen on UNKNOWN impact.
7. Treat Service Worker effective control as client/cohort-relative where the claim depends on worker control.
8. Preserve long-offline unique data during revalidation, while re-admitting remote consequence-bearing work only under current proof/security floor.
9. Reconcile proof lineage after rollback/PITR before restoring admission authority.
10. Keep production generation identifiers, atomicity mechanisms, event sequence guarantees, retry limits and numeric timing thresholds OPEN until actual architecture/runtime evidence exists.

## OPEN / DEPENDENCY
- Actual MintTap/LogMate proof store, admission service and dependency-generation schema: **OPEN**.
- Provider/IAM/DNS/CI/MDM/recovery event sequence guarantees and reconciliation APIs: **OPEN**.
- Exact Safari/iPadOS Service Worker activation/control timing and managed-device behavior: **OPEN**.
- Whether production systems expose source-native generation/ETag/version tokens sufficient for fences: **OPEN**.
- Appropriate restart/backoff/starvation controls under high change rate: **OPEN**.
- Physical-device, AT, human UX and canonical-product runtime validation: **OPEN**.

## DEPENDENCY / HANDOFF
- **Track A:** verify exact browser/WebKit controller/update observations when runtime access exists; do not generalize Chromium evidence to managed iPad.
- **Track B / Design Studio:** translate REVALIDATING/generation-skew/data-preserved-sync-blocked into comprehensible states without exposing internal proof jargon.
- **Track C:** execute race/fork/recovery oracles and preserve exact environment/generation evidence.
- **Track D:** instrument invalidation latency, event lag/reordering, restart count, proof publication/consumption rejection and unknown-generation rate without converting metrics into authority.
- **Software Engineering:** implementation-level compare-and-swap/fencing/event-deduplication/persistence choices belong there once canonical product architecture exists.

## Track C destructive additions — 560 → 568
1. **Mixed-generation green:** IAM changes midway; validator publishes PASS assembled across generations. Expected: publish rejected/revalidation scoped.
2. **Last-oracle TOCTOU:** material dependency changes after final test but before CURRENT pointer update. Expected: stale proof cannot become current.
3. **Out-of-order authentic events:** G32 arrives before G31. Expected: no rollback of current floor and reconciliation detects ordering gap where observable.
4. **Duplicate event replay:** authentic invalidation event is delivered twice. Expected: idempotent handling; no false authority transition.
5. **PITR current-pointer fork:** proof store restores P12 while surviving attestor knows P15. Expected: rejoin blocked until lineage reconciliation.
6. **Service Worker controller race:** target client changes controller during validation. Expected: client-relative proof invalidated/re-observed; registration.active alone insufficient.
7. **Collector permission race:** collector loses a scope during assessment but still emits green from remaining sources. Expected: evidence coverage invalidates affected claim.
8. **Long-offline reconnect during transition:** iPad returns between P20 invalidation and P21 publication. Expected: unique data preserved; consequence-bearing sync waits for current admission and is not grandfathered.

These are **defined cases, not execution PASS**.

## Persistent guards added in 226
`proof timestamp ≠ coherent assessed state`; `all observations authentic ≠ observations co-temporal`; `each check PASS ≠ aggregate proof PASS`; `latest value per field ≠ coherent snapshot`; `no global transaction ≠ no race containment`; `monotonic generation ≠ wall-clock order`; `event authentic ≠ event complete`; `event sequence present ≠ no omitted event`; `current state same as before ≠ no consequential intermediate transition`; `proof valid when issued ≠ proof valid when consumed`; `proof signature valid ≠ admission current`; `change during validation ≠ always full restart`; `partial reuse ≠ reuse without dependency proof`; `active worker observed ≠ target client controlled`; `controller changed ≠ data/schema migration complete`; `reconnected during revalidation ≠ authorized by old or future proof`; `restored latest row ≠ globally current proof`; `PITR success ≠ proof-lineage convergence`; `collector says green ≠ source generation known`; `unknown generation ≠ current by default`; `latest timestamp ≠ current authority`; `historical lineage retained ≠ historical proof reusable`.

## Gate
**226 PASS (generic).** The Web Manager can now reason about proof lineage and concurrent revalidation without assuming an impossible global transaction, separate authentic events from complete/current evidence, prevent mixed-generation publication and issuance→consumption TOCTOU, and apply the model to Service Worker/client-control and long-offline PWA cases. Production implementation and runtime validation remain OPEN.

## Next high-value target
**227 — monotonic admission floors, proof-consumer fencing & stale-client replay under multi-writer failover.** Determine how multiple admission/enforcement writers maintain a non-decreasing security floor across region failover, cache lag and PITR; prevent a stale region or client from consuming an older but authentic proof after another region advanced; and distinguish availability-preserving read/local-data capability from consequence-bearing mutation authority without requiring global synchronous consensus for every operation.