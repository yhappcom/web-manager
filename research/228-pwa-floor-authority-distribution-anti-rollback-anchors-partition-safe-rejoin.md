# 228 — PWA Floor-Authority Distribution, Anti-Rollback Anchors & Partition-Safe Rejoin Proofs

Status: **PASS (generic) / PRODUCT + MULTI-REGION + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/Service Worker mechanics; Track B restricted/rejoin UX; Track C rollback/partition validation; Track D anchor/rejoin telemetry.  
Dependencies: 218–227, especially distributed currentness, quorum/witness trust, dependency graphs, proof lineage, monotonic admission floors and writer fencing.

## Problem
227 established a scoped authenticated monotonic admission floor: once a consequence-bearing scope learns a higher security generation, stale proof cannot regain authority merely because a stale region, cache or client still possesses it. The next problem is bootstrapping that rule after rollback or partition. A recovered consumer may have lost the very row that says the floor advanced. If every copy of the floor lives inside the same rollback domain, monotonicity is only an in-memory promise.

The problem has four parts:
1. how a recovered consumer obtains a trustworthy minimum floor when its ordinary store/cache may be stale;
2. how anti-rollback evidence is distributed without turning one anchor into a new single point of authority or availability;
3. how compaction/retention preserves enough lineage to reject historical authority without retaining every operational object forever;
4. how a partitioned writer proves safe rejoin, including stale-writer extinction, before consequence-bearing capability resumes.

Central rule: **a recovered or partitioned consumer may resume consequence-bearing admission only after it establishes a current-enough authenticated floor from evidence outside the rollback/partition failure domain and demonstrates that obsolete writer/authority paths cannot still produce accepted side effects. Availability recovery does not itself recover authority.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. A browser/PWA can retain stale Service Worker, cache, IndexedDB and queued-operation state; none is an independent server floor anchor. Exact Safari/iPadOS persistence remains runtime evidence.
- **B UX/IA/Content:** high dependency pressure. Owns understandable LOCAL-SAFE / REJOINING / SYNC-HELD / CURRENT states without asking users to reason about epochs or implying local data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds rollback-anchor, partition-rejoin and stale-writer-extinction destructive oracles. Campaign expands **576 → 584 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures anchor divergence, rollback detection, rejoin duration, stale-writer rejection and offline-tail age. Telemetry cannot establish authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns floor authority, anchor independence, retention/compaction, recovery bootstrap and partition-safe rejoin.

## SOURCE

### NIST SP 800-207 / 800-207A — distributed location is not authority
NIST Zero Trust Architecture rejects implicit trust based solely on network location and separates authentication/authorization from mere reachability. SP 800-207A applies granular application/service policy enforcement across multi-location environments.

Sources:
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://csrc.nist.gov/pubs/sp/800/207/a/final

**TRANSFER VALIDATION:** these publications do not define MintTap floor anchors, quorum, epochs or rejoin protocols. They support the narrower principle that a recovered/failover location is not authorized merely because it is reachable or elected.

### NIST SP 800-193 — protection, detection and secure recovery are distinct resilience functions
NIST SP 800-193 describes platform resiliency in terms of protecting against unauthorized change, detecting unauthorized change and recovering rapidly and securely. It is firmware guidance, not a web/PWA admission protocol.

Source:
- https://csrc.nist.gov/pubs/sp/800/193/final

**TRANSFER VALIDATION:** use only the structural precedent: rollback-resistant security needs a recovery trust basis that is not silently restored with the compromised/stale state. Do not claim firmware roots of trust exist in MintTap/LogMate.

### The Update Framework — trusted version state and consistent repository views
TUF uses versioned signed metadata and client-side trusted state to detect rollback/freeze/mix-and-match classes. Snapshot metadata binds versions/hashes of target metadata so objects from different repository moments cannot be freely mixed; timestamp metadata is short-lived and points to snapshot state.

Sources:
- https://theupdateframework.io/spec/
- https://theupdateframework.io/docs/metadata/

**TRANSFER VALIDATION:** TUF secures software-update metadata; it is not a distributed application admission protocol. The reusable concepts are authenticated version lineage, previously trusted minimum state, separation of roles and consistent-view protection.

### RFC 6940 — monotonic stored version evidence as bounded anti-rollback precedent
RFC 6940 requires monotonically increasing storage times for its storage protocol and allows a retriever that has previously observed a newer value to detect an older returned value as rollback.

Source:
- https://www.rfc-editor.org/rfc/rfc6940.html

**TRANSFER VALIDATION:** RELOAD storage semantics do not prescribe our architecture. They provide a standards-track example of a consumer retaining a monotonic lower bound rather than accepting an older authentic value after rollback.

## SYNTHESIS 1 — ordinary floor storage cannot be its own anti-rollback anchor
If floor F24 and the application database are restored together from a snapshot containing F18, the restored database cannot prove that F18 is current. The same applies if a floor cache, proof store and its “latest generation” index share one rollback domain.

A trustworthy recovery needs at least one evidence path whose failure/rollback domain is meaningfully different from the restored plane, or an authorized recovery ceremony that establishes a successor floor using current authority.

`floor row present ≠ floor current`; `same backup domain ≠ independent anchor`.

## SYNTHESIS 2 — an anchor is a minimum-currentness witness, not the whole policy engine
An anti-rollback anchor need not contain the full policy. It can bind enough authenticated state to prevent selection below a known minimum, for example:

`A(scope) = {authorityLineage, minimumFloor, anchorGeneration, digest/checkpoint, issuerSet, validity/context}`

Exact production fields remain OPEN. The anchor answers “what is the minimum state I may accept for this scope?” It does not by itself decide every request, replace policy composition, or prove all enforcement points converged.

`anchor authentic ≠ full policy current`; `minimum floor known ≠ all dependencies healthy`.

## SYNTHESIS 3 — independence is failure-domain diversity, not copy count
Three replicas of the same anchor behind the same IAM root, KMS, deployment account and backup system can fail or roll back together. Independence analysis therefore reuses 219–224 failure-domain reasoning: identity, signing keys, administration, storage, deployment, recovery and observation paths matter.

A useful architecture may combine several differently exposed sources, such as a current policy authority/checkpoint, independently retained audit/transparency evidence, provider/control-plane state, or another authenticated survivor. This is a design space, not a requirement to deploy every mechanism.

`three anchor copies ≠ three independent anchors`; `different region ≠ different authority domain`.

## SYNTHESIS 4 — anchor diversity must not create permissive “pick the lowest” recovery
If anchor A says minimum F24 and anchor B says F22, recovery cannot choose F22 because it restores more availability. Divergence is evidence requiring reconciliation. If lineage proves F24 supersedes F22, F24 wins. If branches are incomparable or authenticity/currentness is contradictory, affected consequence-bearing capability remains restricted until an authorized successor resolves the fork.

`anchor disagreement ≠ choose convenient floor`; `majority old ≠ newer authenticated successor erased`.

## SYNTHESIS 5 — anchors should avoid becoming a universal synchronous dependency
If every safe local/read operation requires live access to one remote anchor, the anti-rollback mechanism becomes an availability choke point. Scope the requirement by consequence and cache authenticated minimum floors where safe.

Once a consumer has learned F24, loss of anchor connectivity does not mean it may drop to F23. It may continue capabilities whose policy permits operation at the cached minimum and whose other dependencies remain valid. Operations requiring fresher currentness can be held.

`anchor unreachable ≠ floor reset`; `anchor required for recovery ≠ anchor required synchronously for every operation`.

## SYNTHESIS 6 — anchor compromise and anchor outage are different states
An unavailable anchor produces missing assurance. A compromised or equivocating anchor can produce false assurance. The latter is more dangerous and requires witness/collector/quorum logic from 219–220: provenance, independent corroboration, fork detection and bounded emergency modes.

Do not treat “two sources disagree” as a generic availability incident. Authentic contradictory floor statements can indicate stale state, rollback, split brain or compromise.

`anchor unavailable ≠ anchor lying`; `reachable anchor ≠ trustworthy anchor`.

## SYNTHESIS 7 — floor compaction needs successor evidence, not eternal raw retention
Monotonicity does not require retaining every floor object forever. It requires enough durable lineage to prove that retired authority cannot become current again.

A compacted checkpoint can summarize a contiguous supersession chain if it binds:
- scope and authority lineage;
- minimum accepted successor generation;
- predecessor range or checkpoint digest being retired;
- issuer/verification context;
- compaction generation;
- any unresolved fork/debt state that cannot be discarded.

Historical raw evidence may have separate audit/legal retention requirements. Compaction is invalid if it erases the only evidence that a predecessor was retired.

`history compacted ≠ retirement evidence erased`; `latest floor retained ≠ lineage continuity proven`.

## SYNTHESIS 8 — compaction itself is a security transition
A compactor that can rewrite “minimum accepted floor” is effectively part of the authority chain. Compaction output therefore needs authenticated provenance, anti-rollback, versioning and independent validation appropriate to consequence. Restoring a pre-compaction snapshot must not make retired generations admissible.

`storage optimization ≠ security-neutral`; `compaction succeeded ≠ anti-rollback preserved`.

## SYNTHESIS 9 — partition-safe rejoin is a proof bundle, not a health check
A partitioned Region B returning healthy at HTTP/load-balancer level proves reachability, not authority. Rejoin for consequence-bearing writes should establish at least:
1. current authenticated floor/lineage for affected scopes;
2. current writer/admission epoch or equivalent fencing state;
3. policy/evaluator/code/schema generations required by that floor;
4. reconciliation of operations produced during partition under the product's conflict/admission rules;
5. negative evidence that obsolete writer credentials/leases/epochs are rejected;
6. recovery/PITR paths do not reintroduce the stale floor;
7. material UNKNOWN/CONTRADICTED dependencies are resolved or capability remains restricted.

`health check green ≠ rejoin authorized`; `data replication caught up ≠ writer authority current`.

## SYNTHESIS 10 — stale-writer extinction needs a negative oracle
Positive evidence that new writer W25 succeeds does not prove W24 can no longer commit. Rejoin proof therefore needs a negative stale-writer oracle at the actual side-effect boundary where feasible: stale epoch/token/credential should be rejected, not merely absent from normal traffic.

If a downstream external side effect cannot enforce fencing, that limitation belongs in the dependency graph and may force stronger single-writer coordination or compensating containment.

`new writer works ≠ old writer fenced`; `zero stale writes observed ≠ stale writer impossible`.

## SYNTHESIS 11 — partition work is preserved as data but not grandfathered as authority
A partitioned writer/client may accumulate legitimate unique data while unable to prove current global authority. Preserve the data/provenance. On rejoin, classify operations by current policy and consequence; re-admit remote mutations under current floor rather than silently replaying creation-time authority.

This is especially important for LogMate/EFB: pilot-entered flight/logbook data may be irreplaceable even when remote synchronization authority is stale.

`data worth preserving ≠ operation still authorized`; `partition-created ≠ discard`.

## SYNTHESIS 12 — PWA local state is not an independent anti-rollback anchor for server authority
IndexedDB, Cache Storage, Service Worker script/cache and localStorage can all be client-local and subject to browser/OS lifecycle, eviction, restore or stale offline state. A PWA may remember a higher server floor as useful local defense, but that memory alone cannot establish global current authority after device restore/reinstall or long offline periods.

Server consequence must still be enforced at a current server/admission boundary. Exact browser persistence/backup behavior is platform/runtime evidence, not assumed.

`client remembers F24 ≠ server globally at F24`; `client forgot F24 ≠ server may accept F18`.

## SYNTHESIS 13 — long-offline iPad return uses current anchor/floor bootstrap before remote consequence
For a company iPad returning after multiple floor generations:
1. preserve unique local data before destructive update/migration;
2. treat cached worker/policy/floor as historical evidence, not sovereign authority;
3. authenticate a current-enough floor/lineage from server-side recovery/admission evidence;
4. obtain required app/worker/schema/policy transitions;
5. re-admit queued consequence-bearing operations individually;
6. keep data locally preserved and sync held when current authority cannot be established.

This does not assume unattended background execution, persistent storage, MDM delivery or direct device-to-device synchronization on iPadOS. Those remain OPEN.

## SYNTHESIS 14 — recovery from total anchor loss is an explicit authority ceremony
A design must acknowledge the possibility that all normal anchors become unavailable or untrustworthy. Recovery must not default to “accept the newest local row.” It needs an explicit bounded recovery authority/process whose credentials, quorum, provenance and successor statement are governed separately and whose use creates evidence/assurance debt where appropriate.

This reuses 204–222 bootstrap, quorum, emergency-authority and assurance-debt work.

`all anchors lost ≠ oldest reachable state becomes current`; `manual recovery ≠ ungoverned override`.

## SYNTHESIS 15 — anchor retention horizon and offline-support horizon are coupled
If a product promises support for clients that can remain offline for a long interval, it must retain enough successor/migration evidence to move those clients from historical state to current state without re-authorizing retired authority. Deleting all bridge/checkpoint material earlier than the supported offline horizon can turn safe rejoin into guesswork.

This does not imply retaining private signing keys or all payload history. Retention is claim-specific: verification material, successor lineage, schema/migration support and data preservation may have different horizons.

`offline support promised ≠ historical authority retained`; `bridge evidence retained ≠ legacy signing authority retained`.

## SYNTHESIS 16 — observability reports divergence but never resolves it
Track D can measure:
- consumers below current known floor;
- anchor-source divergence and age;
- recovery bootstrap source used;
- rejoin duration and reason for hold;
- stale-writer rejection success/failure;
- clients/regions skipping multiple generations;
- compaction checkpoint age and validation coverage;
- operations/data held pending current authority.

Metrics can trigger investigation/revalidation. They cannot vote a stale region back into authority.

`dashboard green ≠ stale writer extinct`; `telemetry majority ≠ authority quorum`.

## MINTTAP DECISION / DIRECTION
1. Treat admission-floor recovery as a separate trust problem from ordinary floor storage.
2. Keep anti-rollback evidence outside the same rollback/failure domain where consequence warrants it; evaluate independence by identity/admin/key/recovery domains, not replica count.
3. Use anchors as authenticated minimum-currentness evidence, not as universal policy engines or mandatory synchronous dependencies for every safe operation.
4. Treat anchor disagreement as a reconciliation/fork problem; never choose a lower floor for convenience.
5. Permit compaction only when successor/retirement lineage remains verifiable and unresolved contradiction/debt is preserved.
6. Require partition/recovery rejoin proof before consequence-bearing writes: current floor + current writer fence + dependency generations + reconciliation + negative stale-writer rejection.
7. Preserve unique offline/partition data before authority decisions; re-admit remote consequences under current policy.
8. Never treat Service Worker/IndexedDB/cache state as sovereign server authority.
9. Define explicit governed recovery for total anchor loss rather than silently accepting local historical state.
10. Couple offline-support horizon to retention of successor/migration verification evidence, without retaining obsolete signing authority.

## DEPENDENCY / TRANSFER
- **Track A:** retain precise Service Worker/client-local generation mechanics and browser storage semantics; physical iPad/WebKit behavior remains OPEN.
- **Track B:** design states for local data preserved, remote sync held, rejoin in progress and recovery complete; consume Design Studio W121 rather than inventing generic visual rules.
- **Track C:** execute destructive rollback/partition/rejoin cases when implementation exists; generic research is not runtime PASS.
- **Track D:** instrument divergence/rejoin/fencing evidence without turning telemetry into authorization.
- **Software Engineering:** when implementation begins, validate actual consistency/fencing primitives, durable anchor stores, recovery ordering and operation-idempotency semantics. Current Software Engineering Studio Foundation status does not provide product PASS.

## CONTRADICTIONS / FAILURE MODES
1. **Same-domain anchor:** DB, floor and “anchor” restored from one backup; rollback goes undetected.
2. **Single-anchor availability coupling:** anchor outage blocks even safe local/read operations unnecessarily.
3. **Permissive divergence:** recovery selects the lowest of conflicting authentic anchors.
4. **Compaction laundering:** old floor history is deleted without durable retirement/successor evidence.
5. **Health-check rejoin:** stale region resumes writes because replication and HTTP health are green.
6. **Positive-only fencing:** new writer succeeds but old writer can still commit through a bypass/downstream path.
7. **Client-sovereign floor:** stale PWA/Service Worker dictates server authority.
8. **Total-anchor-loss fallback:** system silently trusts newest local timestamp after all anchors are unavailable.

## Track C destructive campaign additions — 576 → 584
577. **Co-restored anchor:** restore DB + floor + anchor from the same old snapshot; expected: below-current authority is not admitted without independent/current recovery evidence.
578. **Anchor divergence convenience attack:** one authentic anchor says F24, another F21; expected: no automatic downgrade to F21; reconcile lineage/fork.
579. **Anchor outage downgrade:** current anchor unreachable while consumer has authenticated F24; expected: cached minimum does not fall; only pre-authorized degraded capabilities continue.
580. **Compaction erases retirement:** compact history so F18 retirement evidence disappears; expected: compaction proof fails or affected scope remains restricted.
581. **Green-health stale rejoin:** partitioned region catches up data but retains stale writer epoch; expected: consequence-bearing writes blocked until current fencing/rejoin proof.
582. **Positive-only stale writer:** W25 succeeds while W24 can still commit through provider/recovery bypass; expected: rejoin FAIL because negative stale-writer oracle fails.
583. **Long-offline iPad after anchor compaction:** iPad returns from F16 after server compacted to F27 checkpoint; expected: unique local data preserved, successor path verified, queued remote operations re-admitted; no F16 authority resurrection.
584. **Total normal-anchor loss:** all ordinary anchors unavailable/contradicted; expected: no local-timestamp fallback; governed recovery or restricted consequence only.

These are **defined oracles, not executed PASS evidence**.

## VALIDATION
Generic PASS means the architecture can distinguish floor storage, anti-rollback evidence, anchor independence, compaction, writer fencing and rejoin claims and can diagnose representative failure modes. Production validation remains OPEN for:
- actual MintTap/LogMate provider and region topology;
- floor/anchor schema and authority writers;
- key/IAM/admin/recovery failure-domain independence;
- actual database/object/config-store rollback semantics;
- actual writer fencing at every external side-effect boundary;
- PITR/failover/rejoin implementation;
- actual offline support horizon and migration evidence retention;
- managed iPad/iPadOS/WebKit/MDM/storage/update behavior;
- physical-device and representative human/AT validation.

## CHANGE WATCH
- Browser/WebKit storage, Service Worker and managed-device behavior can change and requires current platform/physical evidence.
- Provider-specific consistency, backup, fencing and recovery semantics are implementation-specific and must be revalidated when providers/topology change.
- TUF and NIST sources are precedents for bounded principles, not product implementation specifications.

## Persistent guards added in 228
`floor row present ≠ floor current`; `same backup domain ≠ independent anchor`; `anchor authentic ≠ full policy current`; `minimum floor known ≠ all dependencies healthy`; `three anchor copies ≠ three independent anchors`; `different region ≠ different authority domain`; `anchor disagreement ≠ choose convenient floor`; `majority old ≠ newer authenticated successor erased`; `anchor unreachable ≠ floor reset`; `anchor required for recovery ≠ anchor required synchronously for every operation`; `anchor unavailable ≠ anchor lying`; `reachable anchor ≠ trustworthy anchor`; `history compacted ≠ retirement evidence erased`; `latest floor retained ≠ lineage continuity proven`; `storage optimization ≠ security-neutral`; `compaction succeeded ≠ anti-rollback preserved`; `health check green ≠ rejoin authorized`; `data replication caught up ≠ writer authority current`; `new writer works ≠ old writer fenced`; `zero stale writes observed ≠ stale writer impossible`; `data worth preserving ≠ operation still authorized`; `partition-created ≠ discard`; `client remembers F24 ≠ server globally at F24`; `client forgot F24 ≠ server may accept F18`; `all anchors lost ≠ oldest reachable state becomes current`; `manual recovery ≠ ungoverned override`; `offline support promised ≠ historical authority retained`; `bridge evidence retained ≠ legacy signing authority retained`; `dashboard green ≠ stale writer extinct`; `telemetry majority ≠ authority quorum`.

## Gate result
**PASS (generic).** Track E remains the highest-risk owner. The generic model now covers recovery bootstrap of monotonic floors, anti-rollback anchor independence, compaction/retention and partition-safe rejoin with stale-writer extinction. Product/runtime validation is not claimed.

## Next high-value target
**229 — anchor equivocation, floor-fork reconciliation & bounded authority recovery after anchor compromise.** Determine how to distinguish stale-but-honest anchors from malicious equivocation, prevent compromised anchor sets from authorizing their own replacement, preserve availability for unaffected capabilities, and establish a successor floor after partial/total anchor compromise without rewriting history.