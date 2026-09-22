# 225 — PWA Dependency-Graph Drift, Change-Triggered Revalidation & Stale-Proof Expiry

Status: **PASS (generic) / PRODUCT + CHANGE-EVENT + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/Service Worker mechanics; Track B degraded/recovery UX; Track C revalidation/regression evidence; Track D drift/coverage telemetry.  
Dependencies: 117–137, 171–224, especially 218–224 distributed currentness, assurance debt, dependency graphs, multi-plane discovery and executable trust cuts.

## Problem
224 established that a dependency graph cannot prove its own completeness and that partial reauthorization requires a scoped, provenance-bearing graph plus positive and negative executable evidence. The adjacent failure is temporal: a correct trust-cut proof at generation G can become wrong after an IAM edit, provider/admin change, DNS or signing change, deployment/update path change, PITR/failover, policy/evaluator change, Service Worker generation change, MDM change, supplier change or previously unknown edge discovery.

A fixed time-to-live is insufficient. A proof can become invalid seconds after it is produced if a material dependency changes, while an unchanged low-risk claim does not become false merely because a calendar interval elapsed. Conversely, absence of detected change does not prove absence of change when the change-observation plane is incomplete.

Central rule: **proof validity is claim-, dependency-, generation- and evidence-specific. Material change invalidates the affected proof closure immediately; time contributes freshness pressure but does not replace change linkage. Revalidation should be incremental where a dependency cut is proven, but UNKNOWN/CONTRADICTED or unobserved material change widens the revalidation scope rather than being silently ignored.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Service Worker script/control generation, scope, update lifecycle, cache behavior, storage/session/schema and reconnect state can mutate the effective client graph. Browser update detection does not itself prove fleet convergence.
- **B UX/IA/Content:** very high dependency pressure. Must distinguish current, stale-proof, revalidating, restricted and data-preserved/sync-blocked states without implying data loss or false global outage.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns change-to-test selection, regression evidence and destructive validation. Campaign expands **552 → 560 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can measure proof age, dependency generation, change-event coverage, invalidation latency and revalidation outcome; telemetry cannot grant authority or prove no hidden change.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns proof dependency manifests, invalidation semantics, change-event trust, incremental revalidation boundaries and stale-proof rejection.

## SOURCE

### NIST SP 800-53 / RMF — configuration change, security impact and continuous monitoring are separate controls
NIST's RMF control catalog distinguishes CM-3 Configuration Change Control, CM-4 Security Impact Analysis, CM-8 component inventory and CA-7 Continuous Monitoring. The reusable principle is that system change, analysis of security impact and ongoing assessment are related but distinct activities.

Sources:
- https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** NIST does not define a MintTap proof-invalidation graph. It supports treating change as an assessment trigger rather than assuming a previously valid control assessment remains current indefinitely.

### NIST SP 800-128 — security impact analysis before/after change and configuration monitoring
SP 800-128 describes security impact analysis as determining how changes affect system security and existing controls, preferably before approval and again after implementation/testing to identify unanticipated effects. It also describes configuration monitoring against baselines and inventories and links that monitoring to ongoing assessment.

Source:
- https://csrc.nist.gov/pubs/sp/800/128/upd1/final

**TRANSFER VALIDATION:** this is configuration-management guidance, not a PWA proof-TTL standard. It supports change-triggered reassessment and post-change verification.

### Service Worker update semantics — client code generation can diverge from server publication
MDN's current ServiceWorkerRegistration documentation states that `update()` fetches the worker script and installs a new worker when it is not byte-for-byte identical to the current worker. MDN also documents `updateViaCache`, which controls HTTP-cache use during worker/import update checks, and the normal lifecycle in which a newly installed worker may wait before activation while old controlled pages remain.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers

**TRANSFER VALIDATION:** these browser mechanics do not prove a deployed LogMate fleet updated, activated or migrated data/policy. They establish why server publication time, registration update discovery, installation, activation and effective client control are separate generations.

## SYNTHESIS 1 — bind every high-consequence proof to a dependency manifest
A proof such as `CAPABILITY C MAY BE REAUTHORIZED` must record more than PASS. Bind it to:
1. claim/capability and operation class;
2. graph generation and scoped denominator;
3. material node/edge IDs and their generations;
4. policy/evaluator generation;
5. code/artifact/signing generation where relevant;
6. provider/IAM/DNS/recovery/update control generations where relevant;
7. evidence-source/collector generation and epistemic state;
8. positive and negative oracle set executed;
9. unresolved UNKNOWN/CONTRADICTED tail accepted or excluded with reason;
10. proof creation and observation interval.

This creates a **proof dependency manifest**. Reuse is permitted only while the material dependencies and assumptions remain valid.

`proof stored ≠ proof current`; `artifact unchanged ≠ authority graph unchanged`; `graph file unchanged ≠ dependency world unchanged`.

## SYNTHESIS 2 — classify changes by claim impact, not file path
Do not invalidate proofs merely because “something changed,” and do not preserve them merely because the application binary did not. Classify change by whether it can affect the consequence-bearing claim.

High-value classes:
- **authority changes:** IAM, credentials, keys, signing, delegated policy, exception/emergency authority;
- **routing/control changes:** DNS, CDN/origin, provider console/API, feature/policy control, gateway, legacy endpoint;
- **code/update changes:** application artifact, Service Worker, imported worker code, CI/CD, package/dependency, update-signing path;
- **data/recovery changes:** schema, migration, backup/PITR, failover, restore, region recreation;
- **evidence changes:** collector permissions/source scope, audit pipeline, attestor, denominator/inventory;
- **client-cohort changes:** new browser/OS/MDM generation, long-offline cohort return, installed-worker generation;
- **supplier changes:** SaaS/provider delegation, platform policy/capability change.

A documentation-only edit may have no consequence; a one-line IAM change can invalidate many proofs.

`small diff ≠ small assurance impact`; `no code diff ≠ no security-impacting change`; `provider-side change ≠ outside product proof`.

## SYNTHESIS 3 — use dependency-directed invalidation rather than global retest by default
For each material change Δ, traverse the typed graph from the changed node/edge to claims whose proof manifests depend on it. Mark those proofs `INVALIDATED-PENDING-REVALIDATION` or `UNKNOWN-IMPACT` when traversal cannot establish a bounded impact set.

Unaffected proofs may remain reusable only when:
- the changed element is outside their consequence-bearing cut;
- graph provenance/currentness is sufficient to establish that separation;
- no material UNKNOWN/CONTRADICTED alternate edge crosses the cut;
- the evidence plane capable of detecting the change remained trustworthy.

This avoids both extremes: full-fleet/full-suite retesting after every cosmetic change and unsafe reuse of a green proof after authority mutation.

`change detected ≠ global invalidation`; `bounded invalidation ≠ assume unrelated`; `unknown impact ≠ unaffected`.

## SYNTHESIS 4 — time freshness is a secondary constraint, not the primary truth model
Time still matters because some dependencies can drift without complete event delivery, providers/platforms can change outside local control, and observations age. Use time-based maximum evidence age as a backstop selected by claim risk and source observability, not as proof of validity.

A proof can expire before its maximum age because of a material change. Reaching a maximum age can force refresh even when no change event was seen. Therefore validity is approximately:

`VALID = dependency generations match ∧ required observations current ∧ no unresolved material contradiction ∧ age within claim-specific backstop`.

Do not infer exact numeric TTLs generically; production values require actual risk, platform and operational evidence.

`within TTL ≠ unchanged`; `TTL expired ≠ claim false`; `no event received ≠ no event occurred`.

## SYNTHESIS 5 — change events themselves are evidence-plane objects
Webhook, audit-log, Git commit, provider event, MDM event or scanner diff can trigger invalidation, but its absence cannot prove no change unless event coverage and retention are themselves established. Record event source, scope, identity, generation/sequence, delivery state and reconciliation result.

Use periodic/state reconciliation to catch missed events. Event-driven invalidation gives low latency; reconciliation gives omission resistance. Neither alone proves completeness.

`webhook delivered ≠ state reconciled`; `no webhook ≠ no change`; `poll shows same state ≠ all hidden planes unchanged`; `event source authenticated ≠ event source complete`.

## SYNTHESIS 6 — revalidation depth follows the changed dependency and oracle closure
After invalidation, choose the minimum sufficient test bundle from the claim graph:
- configuration/IAM change → enumerate effective authority + positive current admission + negative retired/bypass rejection;
- signing/update change → provenance/signature/current-policy acceptance + old signer/update-path rejection;
- recovery/PITR change → restore/rejoin + current authority floor + extinct-path rejection + evidence continuity;
- Service Worker/code generation → update/install/activation/control observation + schema/policy compatibility + stale-worker negative admission where consequence-bearing;
- collector/evidence change → source-scope and independence reassessment before using new green evidence;
- unknown edge discovery → widen blast radius and re-run cut validation until the new edge is classified.

Passing a generic smoke test does not close a claim-specific invalidation.

`retest passed ≠ invalidated claim retested`; `current path works ≠ retired path rejected`; `new worker installed ≠ new worker controls all relevant clients`.

## SYNTHESIS 7 — Service Worker generations make client proof validity explicitly multi-epoch
For PWA claims distinguish at least:
- server-published worker generation;
- registration's discovered/installing generation;
- waiting generation;
- active worker generation;
- controlling-worker generation for a specific client;
- data/schema/policy generation consumed by that client.

A server deploy may invalidate assumptions about compatibility while a long-lived page remains controlled by an older worker. Conversely, an updated worker does not prove local IndexedDB/schema/policy migration completed safely.

`worker published ≠ worker installed`; `worker installed ≠ worker active`; `worker active ≠ every client controlled`; `worker current ≠ data/policy generation current`.

Exact Safari/iPadOS lifecycle timing and managed-device behavior remain Track A/Software Engineering runtime evidence.

## SYNTHESIS 8 — long-offline return is a batch of missed change generations, not one reconnect event
An EFB-like iPad can miss G10→G15 changes across policy, schema, endpoint, signing, Service Worker and provider topology. Do not replay queued operations under the proof that was valid at queue creation.

On return:
1. preserve unique local flight/logbook data first;
2. identify installed/control/data/policy generations where observable;
3. acquire current authenticated policy and compatibility requirements;
4. reconcile required migrations without treating connectivity as authority;
5. re-admit each consequence-bearing queued operation under current proof/policy;
6. retain rejected work/provenance rather than silently discarding user data.

`proof valid when queued ≠ proof valid when replayed`; `multiple generations skipped ≠ sequential authority grandfathering`; `data preserved ≠ mutation authorized`.

## SYNTHESIS 9 — proof expiry must propagate to automation and UI without becoming a destructive global fail-closed
When a high-consequence proof becomes stale/invalidated, automated remote mutation should consume the proof state and enforce the associated restriction. But local/offline capabilities whose trust cut remains outside the affected dependency may continue.

Useful assurance states include `CURRENT`, `INVALIDATED-PENDING-REVALIDATION`, `STALE-BACKSTOP`, `UNKNOWN-IMPACT`, `CONTRADICTED`, and `REVALIDATING`. Track B should translate these into user-comprehensible capability states rather than exposing security jargon.

For LogMate-like offline use, `remote sync restricted` must not be conflated with `local log entry unsafe` unless the dependency graph actually links the incident to local data integrity.

## SYNTHESIS 10 — rollback is also a change and cannot revive the proof generation it resembles
Rolling code/configuration from G15 back to bytes resembling G12 does not make old G12 proof current. Current provider/IAM/policy/recovery/evidence state may differ, and the rollback itself is a graph mutation. Revalidate against the current security floor and current dependency generations.

`same bytes as old release ≠ old proof current`; `rollback complete ≠ authority rollback permitted`; `PITR timestamp old ≠ security generation old is acceptable`.

## SYNTHESIS 11 — supplier/platform CHANGE WATCH must feed proof invalidation when it affects assumptions
Some material changes originate outside the repository: browser behavior, provider IAM semantics, API retirement, platform storage policy, certificate/crypto policy or managed-device capability. Maintain explicit external assumptions in proof manifests. When authoritative platform evidence changes materially, invalidate claims that depend on the old assumption even if MintTap deployed nothing.

This is especially important for Safari/iPadOS PWA capability because support and lifecycle details are platform/version-sensitive. Do not convert generic standards into a claim that a managed company iPad behaves identically.

`no internal deploy ≠ no dependency change`; `standard stable ≠ implementation/policy stable`; `CHANGE WATCH item updated ≠ every product claim invalidated` — only claims with a material dependency are affected.

## SYNTHESIS 12 — proof garbage collection must preserve historical auditability without making stale proof reusable
Retain enough lineage to explain why a capability was authorized at a historical point, what invalidated that proof, what revalidation replaced it and what unresolved interval existed. Mark superseded/invalidated proofs non-current rather than deleting them or allowing generic “latest PASS” queries to select them.

The evidence store therefore needs both current-selection semantics and historical lineage.

`historical PASS ≠ current PASS`; `superseded ≠ false`; `deleted stale proof ≠ stale proof safely retired`.

## MINTTAP DECISION / DIRECTION
1. Represent high-consequence trust-cut/reauthorization evidence as proof objects with dependency manifests, not free-floating PASS labels.
2. Invalidate proofs on material dependency-generation change; use claim-specific time limits only as omission/freshness backstops.
3. Classify changes by consequence-bearing impact, not diff size or repository location.
4. Use graph-directed incremental revalidation when the unaffected cut is itself evidenced; widen to UNKNOWN when impact cannot be bounded.
5. Treat change-event pipelines as evidence components and reconcile events against current state to detect missed notifications.
6. Select revalidation oracles from the changed dependency class, including negative stale/bypass/recovery rejection where relevant.
7. Model Service Worker publication/install/wait/activate/control and data/policy generations separately.
8. Treat long-offline reconnect as reconciliation across every missed material generation; preserve unique data and re-admit queued operations under current authority.
9. Make stale/invalid proof state consumable by enforcement and UX without converting every uncertainty into global data-entry shutdown.
10. Treat rollback/PITR and external platform/provider changes as graph mutations; old-looking state does not revive old proof.
11. Preserve historical proof lineage while preventing superseded proof from satisfying current admission.
12. Keep all production values/topology/TTL thresholds OPEN until canonical runtime/project evidence exists.

## OPEN / DEPENDENCY
- Actual MintTap/LogMate change-event sources, graph/proof schema and generation identifiers: **OPEN**.
- Provider IAM/DNS/CI/signing/recovery/admin event coverage and reconciliation: **OPEN**.
- Claim-specific maximum evidence ages and risk thresholds: **OPEN; must not be invented generically**.
- Managed iPad installed-worker/control/schema/policy observability and Safari/iPadOS lifecycle: **Track A + Software Engineering runtime dependency**.
- Safe product-specific negative tests and aviation/legal/safety boundaries: **OPEN**.
- UX for stale/revalidating/data-preserved-sync-blocked states: **Track B consuming Design Studio; physical/human/AT validation OPEN**.

## Track C destructive campaign — 552 → 560 defined cases
Add:
1. **TTL-only false freshness:** proof remains green inside a 24-hour TTL after an IAM mutation creates a bypass path.
2. **Global-retest waste / local-skip asymmetry:** cosmetic change triggers full retest while provider-root change triggers only app smoke tests; verify impact classification is graph-based.
3. **Dropped change event:** provider webhook is lost; periodic reconciliation must discover generation mismatch and invalidate dependent proof.
4. **Untrusted event source:** compromised collector emits false no-change state; direct/state reconciliation contradicts it and proof must not remain CURRENT.
5. **Service Worker multi-epoch drift:** new worker published/installed while a controlled client remains on old worker; fleet-level proof must not infer convergence.
6. **Rollback proof resurrection:** application bytes roll back to G12 and system incorrectly reuses historical G12 PASS despite current IAM/policy generations.
7. **New hidden edge after partial reauthorization:** discovery finds an alternate admin/recovery edge crossing the supposedly unaffected cut; prior proof becomes invalidated and blast radius widens pending revalidation.
8. **Long-offline iPad skips multiple proof generations:** device returns with old worker/policy/schema and queued writes. Preserve unique data, obtain current generations, migrate safely and re-admit each consequence-bearing operation; do not replay under creation-time proof.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** Service Worker/browser generations are dependency inputs; standards/MDN establish mechanics, not managed-iPad convergence.
- **Track B:** proof state should map to capability-specific system status and recovery guidance, not global “secure/insecure” labels.
- **Track C:** owns executable change→revalidation matrices and regression evidence; 560 cases remain defined, not executed.
- **Track D:** drift/invalidation latency/coverage metrics diagnose evidence freshness but cannot authorize reuse.
- **Design Studio:** Web remains W121 / Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains underway; physical iOS/Safari/iPadOS/EFB and canonical-product runtime remain OPEN.

## Persistent guards added
`proof stored ≠ proof current`; `artifact unchanged ≠ authority graph unchanged`; `graph file unchanged ≠ dependency world unchanged`; `small diff ≠ small assurance impact`; `no code diff ≠ no security-impacting change`; `provider-side change ≠ outside product proof`; `change detected ≠ global invalidation`; `unknown impact ≠ unaffected`; `within TTL ≠ unchanged`; `TTL expired ≠ claim false`; `no event received ≠ no event occurred`; `webhook delivered ≠ state reconciled`; `retest passed ≠ invalidated claim retested`; `new worker installed ≠ new worker controls all relevant clients`; `proof valid when queued ≠ proof valid when replayed`; `same bytes as old release ≠ old proof current`; `no internal deploy ≠ no dependency change`; `historical PASS ≠ current PASS`.

## Gate result
**225 PASS (generic).** The knowledge gate closes because proof dependency manifests, material-change classification, graph-directed invalidation, time-as-backstop freshness, change-event evidence boundaries, claim-specific revalidation, Service Worker multi-epoch state, long-offline reconciliation, rollback semantics, external CHANGE WATCH propagation and historical proof retirement now form one coherent operational model.

Production validation remains OPEN. No claim is made that MintTap/LogMate currently implements this model or that a managed iPad/Safari fleet has been tested.

## Next highest-value target
**226 — proof-generation lineage, invalidation-event authenticity & revalidation-race containment.** Study concurrent deploy/IAM/recovery changes while validation is running; prevent a proof computed against mixed generations from being published as current; bind assessment start/end snapshots; handle TOCTOU between proof issuance and enforcement consumption; and define atomic/monotonic proof publication without requiring impossible global transactions.