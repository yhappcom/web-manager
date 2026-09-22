# 227 — PWA Monotonic Admission Floors, Proof-Consumer Fencing & Stale-Client Replay under Multi-Writer Failover

Status: **PASS (generic) / PRODUCT + MULTI-REGION + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/Service Worker mechanics; Track B restricted/recovery UX; Track C failover/replay validation; Track D floor-skew and stale-consumer telemetry.  
Dependencies: 218–226, especially distributed currentness, quorum/witness trust, dependency graphs, proof freshness, proof lineage and revalidation-race containment.

## Problem
226 prevents a validator from publishing a mixed-generation proof and requires proof currentness to be re-checked at use time. The next failure is distributed consumption. Region A can advance a security/admission floor while Region B is partitioned, lagging, failed over from an older snapshot, or serving a stale cache. A client can hold an authentic proof that was once current. If B accepts that proof merely because its signature and local cache are valid, an authority already retired elsewhere can regain consequence-bearing effect.

The central problem is therefore not only choosing the newest proof. It is preventing **security-relevant admission from moving backward** while preserving availability for capabilities whose trust cut is unaffected. A monotonic admission floor is a logical lower bound on acceptable authority/evidence generation for a scoped claim. It is not a global wall-clock, not proof that every replica is synchronized, and not permission to discard unique offline data.

Central rule: **once a consequence-bearing scope has authenticated evidence that its minimum acceptable security generation/fence advanced, a stale writer/consumer must not re-authorize an older generation merely because it is locally reachable, internally consistent or cryptographically authentic. Failover restores service capacity, not retired authority.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Browser clients can remain under older Service Worker controllers and retain old cached application/policy state; exact effective controller and client generation matter more than server publication alone.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible local-safe/remote-restricted/revalidation/recovery states without implying data loss or asking users to resolve security generations.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns multi-writer/failover/stale-client destructive oracles. Campaign expands **568 → 576 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures floor skew, stale-proof rejection, failover rejoin latency, offline-tail age and restriction duration; analytics never lowers the admission floor.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns floor authority, monotonic current selection, consumer fencing, failover/rejoin rules, rollback/PITR containment and degraded capability boundaries.

## SOURCE

### NIST Zero Trust: authorization is request/resource policy enforcement, not location trust
NIST SP 800-207 defines policy decision and policy enforcement functions for access to resources and explicitly rejects implicit trust based only on network location. Its trust algorithm consumes request, subject/asset state, resource policy requirements, threat intelligence and logs. NIST SP 800-207A extends the application-security model to multi-cloud/multi-location environments and emphasizes application/service identity and policy enforcement independent of location.

Sources:
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://csrc.nist.gov/pubs/sp/800/207/a/final

**TRANSFER VALIDATION:** NIST does not define a MintTap admission-generation protocol or fencing-token schema. It supports the narrower principle that failover to another location does not itself establish authorization and that policy enforcement must evaluate the current request/context.

### Kubernetes Lease: distributed active authority is explicitly coordinated and time-bounded
Kubernetes documents Lease objects for node heartbeats and leader election. Coordinated leader election tracks candidate identity/version and uses a shared Lease so only one candidate assumes the active control role; when renewal fails and the lease expires, another candidate can be elected.

Sources:
- https://kubernetes.io/docs/concepts/architecture/leases/
- https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/

**TRANSFER VALIDATION:** Kubernetes leadership is not MintTap authorization and a Lease is not sufficient fencing for arbitrary external side effects. The reusable principle is that distributed active authority needs explicit coordination/currentness rather than “the process is alive, therefore it may act.”

### Service Worker control is client-relative
Current MDN documentation distinguishes installation, waiting, activation and effective client control. `Clients.claim()` allows an active Service Worker to become controller for clients in scope and triggers `controllerchange`; without it, an already-open document may remain outside the new worker until reload/navigation.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration

**CHANGE WATCH:** generic Web API semantics are current. Exact Safari/iPadOS lifecycle timing, suspension, storage and managed-device behavior remain physical/runtime validation questions.

## SYNTHESIS 1 — admission floor is scoped, monotonic security state
Represent the minimum acceptable state for a consequence-bearing claim as a scoped floor, for example:

`F(scope) = {authorityEpoch, policyGen, proofFloor, evaluatorGen, revocationFloor, schema/data constraints}`

The exact production fields remain OPEN. The durable property is that the floor identifies the minimum security state a consumer must satisfy for that claim. Different capabilities can have different floors: read/export, local data capture, remote append, destructive reconciliation, authority change and administrative mutation need not share one global generation.

A floor advance means “older state can no longer authorize this scoped consequence.” It does not mean all historical data/proof becomes invalid for audit.

`floor advanced ≠ history erased`; `historical proof valid ≠ proof admissible now`.

## SYNTHESIS 2 — monotonicity is about authority, not timestamps
Wall-clock timestamps are insufficient because clocks can skew, PITR can restore old rows with new filesystem times, and different authority domains can advance independently. A security floor should use authenticated lineage/generation semantics whose comparison rule is defined by the authority model.

If two branches are incomparable because of partition/fork, do not invent an ordering from timestamps. Classify the currentness claim as CONTRADICTED/FORKED/UNKNOWN and restrict the affected consequence until reconciliation or an authorized recovery transition establishes a successor.

`newer timestamp ≠ higher authority floor`; `locally latest ≠ globally admissible`.

## SYNTHESIS 3 — proof consumers need fencing, not only proof verification
A consumer should not ask only whether proof P is signed and green. Before consequence-bearing use, it needs to establish that:
1. P's scope matches the requested capability/resource;
2. P's authority/policy/evaluator generations meet the consumer's authenticated floor;
3. P is not superseded/revoked/forked under known lineage;
4. no unresolved material invalidation above P's assessed fence exists;
5. the consumer itself is permitted to act at its current writer/admission epoch;
6. any operation-level replay/idempotency constraints are current.

The final point matters in multi-writer failover: an old region can possess a valid proof and valid credentials yet no longer be the accepted writer for the side effect. The operation therefore needs a consumer/writer fence in addition to proof authenticity.

`proof authentic ≠ consumer fenced current`; `credential valid ≠ writer epoch current`.

## SYNTHESIS 4 — stale writer exclusion must survive failover
Consider Region A writer epoch W20. Region B is partitioned at W19. A advances the security floor and retires an authority, then fails. If B is promoted from its W19 snapshot without reconciling the floor, it can resurrect the retired authority.

Safe failover requires a rejoin/promotion gate that establishes the current minimum floor from an authority/evidence plane not lost with the stale region, or explicitly enters a pre-authorized degraded mode whose capability ceiling does not depend on the unknown floor. “B is the only region alive” is availability evidence, not authorization evidence.

`only survivor ≠ current authority`; `failover elected ≠ stale floor erased`; `availability leader ≠ security-floor authority`.

## SYNTHESIS 5 — avoid global synchronous consensus for every safe operation
Monotonic security does not require every operation in every capability to synchronously contact a global coordinator. Partition the problem by consequence and trust cut.

A consumer can act locally when it holds an authenticated floor/fence sufficient for that capability and no known invalidation exceeds it. Operations whose authority can be safely cached may use bounded leases/floors. Operations that change authority, destroy/reconcile irreplaceable data or cross a compromised trust boundary may require stronger currentness.

When currentness cannot be established, preserve safe local/read capabilities rather than weakening the floor for remote mutation.

`no global consensus per operation ≠ accept stale authority`; `availability preserved ≠ security floor lowered`.

## SYNTHESIS 6 — cache lag must fail toward restricted consequence, not silent downgrade
CDN/edge/admission caches can lag. A stale cache entry containing P19 must not override an authenticated local floor F20. Cache keys/objects therefore need sufficient generation/scope metadata for the consumer to reject below-floor results.

If the consumer cannot establish whether its floor is current because the floor source is unreachable, classify the affected capability according to pre-defined degraded policy. Do not reinterpret “cannot refresh” as “old cache becomes authoritative again.”

`cache hit ≠ current admission`; `floor source unreachable ≠ cached floor reset`.

## SYNTHESIS 7 — floor propagation and floor consumption are separate convergence claims
A central store can publish F21 while some enforcement points still consume F20. 218–220 already require an explicit enforcement denominator and witness diversity. Extend that model: track floor publication, distribution, consumer acknowledgement/effective enforcement and negative stale-proof rejection separately.

A useful convergence proof for F21 includes positive evidence that intended current operations succeed and negative evidence that P20/retired authority fails across the relevant enforcement set, including recovery/provider-console paths where applicable.

`floor published ≠ floor enforced`; `consumer reports F21 ≠ stale proof rejection tested`.

## SYNTHESIS 8 — rollback/PITR must not lower the floor
Restoring a database, config store or admission cache to an older snapshot can restore old floor records. Recovery therefore needs a floor source/anchor or reconciliation mechanism outside the rollback failure domain, plus a rejoin rule that refuses consequence-bearing admission until the recovered plane demonstrates it meets the current floor.

A rollback may legitimately restore application bytes, but it must not automatically restore retired security authority.

`data rollback ≠ authority-floor rollback`; `PITR complete ≠ admission floor reconciled`.

## SYNTHESIS 9 — floor authority itself needs anti-rollback and bounded writers
If any ordinary region can arbitrarily write a lower floor, consumer fencing is cosmetic. Define who can advance floors, whether lowering is ever legal, and what recovery transition is required if a generation is erroneous.

For high-consequence scopes, prefer successor/supersession transitions rather than decrementing the floor. An emergency compatibility exception should be an explicit bounded capability/waiver with its own lineage, not “set floor back to 18.” This preserves evidence that the system once retired the old authority.

`operator wants rollback ≠ security floor may decrement`; `compatibility exception ≠ historical floor rewrite`.

## SYNTHESIS 10 — client-held stale proof is a replay problem even when cryptographically authentic
A long-offline PWA can return with P18, a cached worker and operations created while P18 was current. Creation-time authorization does not guarantee execution-time authorization after revocation/policy change.

On reconnect:
1. preserve unique local data before destructive migration/rejection;
2. authenticate the current admission floor;
3. establish current client/controller/data/schema context as required;
4. classify queued operations by capability and current policy;
5. re-admit consequence-bearing operations individually;
6. retain rejected/held operations and provenance according to the data model rather than silently dropping them.

`authorized when queued ≠ authorized when replayed`; `offline age ≠ authority extension`.

## SYNTHESIS 11 — Service Worker generation cannot be the global security floor
A Service Worker can enforce useful local behavior, but an offline worker is not a sovereign policy authority. It can be stale, client-relative and unable to know server-side revocation/currentness. The server/admission boundary must enforce remote consequence using current authenticated policy/floor even if the client claims a newer worker.

Conversely, server publication of a new worker does not prove the client has installed/activated/adopted it. If a local capability depends on worker generation, use client-relative evidence and safe restriction/migration logic.

`Service Worker says current ≠ server authority current`; `server worker published ≠ client floor adopted`.

## SYNTHESIS 12 — writer epoch and operation identity solve different problems
A writer/admission epoch can fence a stale region from new side effects, but it does not make retries safe. Operation identity/deduplication remains necessary when an ACK is lost or failover occurs after commit. Likewise idempotency does not stop an obsolete writer from issuing a newly unique unauthorized operation.

`fenced writer ≠ duplicate-free operation`; `idempotent operation ≠ current writer`.

## SYNTHESIS 13 — floor advancement should trigger targeted invalidation/revalidation
When floor F(scope) advances, identify proofs, caches, sessions, writer leases and queued operations whose admissibility depended on the older floor. Do not globally invalidate unrelated capabilities without graph evidence. But if dependency impact is UNKNOWN/CONTRADICTED, widen restriction rather than declaring unaffected status by assumption.

This reuses 223–226 dependency-graph and change-triggered revalidation logic.

`floor advanced ≠ global outage`; `unknown floor dependency ≠ safe unaffected capability`.

## SYNTHESIS 14 — multi-writer topology needs explicit conflict between availability and authority
Active-active or failover topology is not automatically safer. If two regions can independently admit irreversible operations while partitioned, the architecture must state how authority is fenced and how conflicts are contained. If that cannot be proven, the safe design may deliberately restrict some remote writes during partition while retaining local capture/read/export.

For an EFB/logbook scenario, preserving the pilot's unique local record can be higher priority than pretending globally authoritative sync is available. The later reconciliation path must preserve provenance and current policy.

`multi-writer ≠ multi-authority`; `both regions reachable locally ≠ both may authorize globally`.

## SYNTHESIS 15 — observability must expose floor skew without becoming authority
Track D can measure:
- floor publication→consumer adoption latency;
- enforcement points below current known floor;
- stale-proof rejection count by scope/generation;
- failover/rejoin duration;
- writer-epoch conflicts;
- offline-tail age and generations skipped;
- operations held for currentness;
- negative-oracle coverage after floor advance.

These signals identify drift and regression. They cannot vote an operation into authorization.

`metric majority green ≠ stale red enforcement path authorized away`.

## SYNTHESIS 16 — floor recovery after false advancement needs a successor, not history rewrite
A floor can be advanced erroneously. Recovery should not delete or mutate history to pretend the advance never happened. Define an authorized successor policy that may re-enable a bounded compatibility capability under current authority, with explicit evidence and debt if assurance is reduced. This maintains monotonic lineage even when effective capability becomes more permissive.

Monotonicity therefore applies to authenticated policy lineage/current selection, not necessarily to “permissions can only become stricter forever.” A newer policy can intentionally permit something previously denied, but the permission comes from the newer authority, never from resurrection of the old proof.

`monotonic authority lineage ≠ monotonically shrinking product capability`; `new permit ≠ old proof resurrected`.

## MINTTAP DECISION / DIRECTION
1. Model high-consequence admission with scoped authenticated floors rather than selecting the newest green proof by timestamp.
2. Require proof consumers to compare proof generation/lineage and their own writer/admission epoch against the current floor before side effects.
3. Do not allow region failover, cache lag, rollback or PITR to lower a known security floor.
4. Separate availability leadership from security-floor authority; a surviving region must rejoin/promote against current floor evidence or remain in a bounded degraded capability mode.
5. Avoid global synchronous consensus for low-consequence/local-safe operations; strengthen currentness requirements by capability/trust cut.
6. Treat floor publication, propagation and effective enforcement as separate convergence claims and test stale-proof rejection explicitly.
7. Do not use Service Worker generation as global authorization authority; keep client-control evidence separate from server-side admission.
8. On long-offline return, preserve unique local data first and re-admit queued consequence-bearing operations under current authority rather than creation-time proof.
9. Keep writer fencing and operation idempotency/deduplication as distinct controls.
10. Recover from erroneous floor advancement through a newer authorized policy/exception lineage, not by rewriting the historical floor downward.
11. Keep actual floor schema, generation source, writer-election/fencing primitive, cache strategy, numeric freshness/lease values and product capability classes OPEN until canonical implementation evidence exists.

## PWA / LogMate-like EFB application
A company-managed iPad can be offline across several policy/floor generations. It may continue safe local flight/logbook capture if that capability's trust cut does not require current remote authority. The local record must not be destroyed because sync authorization is unknown.

When connectivity returns, do not assume hotspot reachability, background execution or Service Worker wake means current authority. The client establishes current authenticated admission state when execution opportunity exists. If it cannot, preserve local data and show/maintain a bounded sync-restricted state. When current state is known, queued remote mutations are re-evaluated operation by operation.

A stale iPad cannot lower the server floor. A stale failover region cannot accept the iPad's old proof simply because both agree on the same old generation. Agreement among stale participants is not currentness.

`stale client + stale region agreement ≠ current authorization`.

## CONTRADICTION / LIMITS
- Strong monotonic admission may reduce remote-write availability during partition. That is an explicit security/availability trade-off, not automatically a defect.
- A single globally synchronous floor store can itself become an availability/concentration risk. The generic decision is scoped authenticated monotonicity, not one mandated datastore topology.
- Leases coordinate active actors but are not by themselves proof that external side effects are fenced; implementation must validate the actual sink/admission boundary.
- “Generation” is logical authority lineage. Do not assume one integer can safely order every independent domain.
- Physical Safari/iPadOS behavior, MDM controls, storage durability and background execution remain OPEN.

## OPEN / DEPENDENCY
- Actual MintTap/LogMate admission/floor store and writer topology: **OPEN**.
- Whether production has multi-region writers, provider failover or a single authoritative backend: **OPEN**.
- Source-native CAS/version/fencing primitives for provider/IAM/DNS/DB/queue layers: **OPEN**.
- Exact offline queue identity, deduplication and rejected-operation retention semantics: **OPEN**.
- Exact Service Worker/controller/update behavior on managed physical iPad/Safari: **OPEN**.
- Numeric lease/freshness/propagation thresholds and degraded-mode ceilings: **OPEN**.
- Legal/aviation/safety requirements that may change allowed local/remote capability boundaries: **OPEN**.
- Physical-device, AT, human UX and canonical-product runtime validation: **OPEN**.

## DEPENDENCY / HANDOFF
- **Track A:** supply exact browser/controller/cache mechanics; verify WebKit/managed-iPad behavior only with runtime evidence.
- **Track B / Design Studio:** define user-comprehensible local-safe, sync-restricted, revalidating and recovered states without exposing floor jargon or implying data loss.
- **Track C:** execute failover/PITR/cache-lag/stale-client negative oracles and preserve exact region/client/floor generations.
- **Track D:** instrument skew/rejection/rejoin/offline-tail metrics without converting telemetry into authorization.
- **Software Engineering:** concrete CAS/fencing/lease/transaction/queue implementation belongs to engineering once canonical topology is known; Web Manager supplies the web/PWA security requirements and failure oracles.

## Track C destructive additions — 568 → 576
1. **Stale-region failover resurrection:** A advances F20→F21; B fails over from F20 and accepts P20. Expected: consequence-bearing admission blocked until B reconciles F21 or enters explicitly bounded degraded mode.
2. **Cache-lag downgrade:** edge cache serves authentic P19 after consumer learned F20. Expected: below-floor proof rejected regardless of cache validity/TTL.
3. **PITR floor rollback:** admission DB restores F17 while independent currentness evidence knows F22. Expected: recovered plane cannot rejoin/write until floor lineage converges.
4. **Dual-writer partition:** W30 and stale W29 both issue unique remote mutations. Expected: stale writer fenced at authoritative sink/admission boundary; uniqueness does not bypass writer epoch.
5. **False floor decrement:** operator attempts to resolve compatibility incident by changing F25 back to F23. Expected: historical floor not rewritten; use authorized successor/exception lineage.
6. **Service Worker false authority:** client reports newest worker but presents proof below server floor. Expected: remote mutation rejected; client worker generation cannot lower server admission.
7. **Stale client + stale region collusion-by-state:** long-offline iPad P18 reconnects to partitioned region still at F18 while current system is F24. Expected: agreement on F18 does not authorize remote consequence; unique data preserved.
8. **ACK-loss across failover:** operation commits under current writer, ACK is lost, retry reaches successor writer. Expected: current writer/floor checks plus operation identity prevent both stale authorization and duplicate side effect.

These are **defined cases, not execution PASS**.

## Persistent guards added in 227
`floor advanced ≠ history erased`; `historical proof valid ≠ proof admissible now`; `newer timestamp ≠ higher authority floor`; `locally latest ≠ globally admissible`; `proof authentic ≠ consumer fenced current`; `credential valid ≠ writer epoch current`; `only survivor ≠ current authority`; `failover elected ≠ stale floor erased`; `availability leader ≠ security-floor authority`; `no global consensus per operation ≠ accept stale authority`; `availability preserved ≠ security floor lowered`; `cache hit ≠ current admission`; `floor source unreachable ≠ cached floor reset`; `floor published ≠ floor enforced`; `consumer reports current floor ≠ stale proof rejection tested`; `data rollback ≠ authority-floor rollback`; `PITR complete ≠ admission floor reconciled`; `operator wants rollback ≠ security floor may decrement`; `compatibility exception ≠ historical floor rewrite`; `authorized when queued ≠ authorized when replayed`; `offline age ≠ authority extension`; `Service Worker says current ≠ server authority current`; `server worker published ≠ client floor adopted`; `fenced writer ≠ duplicate-free operation`; `idempotent operation ≠ current writer`; `floor advanced ≠ global outage`; `unknown floor dependency ≠ safe unaffected capability`; `multi-writer ≠ multi-authority`; `both regions reachable locally ≠ both may authorize globally`; `metric majority green ≠ stale red enforcement path authorized away`; `monotonic authority lineage ≠ monotonically shrinking product capability`; `new permit ≠ old proof resurrected`; `stale client + stale region agreement ≠ current authorization`.

## Gate verdict
**PASS (generic).** The Web Manager can now reason from coherent proof generation (226) to distributed proof consumption under failover/partition without assuming global synchronous consensus. The reusable model separates authenticated monotonic authority lineage, scoped admission floors, writer fencing, operation identity and client-relative PWA state. Production validation remains OPEN because no canonical MintTap/LogMate multi-writer/floor topology or physical managed-iPad evidence has been supplied.

## Next high-value target
**228 — floor-authority distribution, anti-rollback anchors & partition-safe rejoin proofs.** Determine how a recovered/partitioned consumer learns a trustworthy minimum floor when its ordinary store/cache may have rolled back, how independent anchors avoid becoming a new single point of authority, how floor compaction/retention preserves anti-rollback evidence, and how rejoin proves stale writer extinction before consequence-bearing capability resumes.