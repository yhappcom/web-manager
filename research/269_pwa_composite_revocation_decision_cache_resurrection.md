# 269 — PWA Composite-Proof Revocation, Decision-Cache Invalidation & Stale-NORMAL Resurrection Resistance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime cache boundaries; Track B truthful degraded/revalidation UX; Track C destructive validation; Track D bounded invalidation/coverage diagnostics.  
Dependencies: 260–268 dependency/completeness/topology/re-entry/composite-attestation governance.

## Problem

268 established that individually valid prerequisites do not automatically compose into a valid high-consequence re-entry decision. The next boundary is revocation after a composition was legitimately accepted. A prerequisite, verifier, credential, topology edge or composition-policy assumption can later be revoked or contradicted while browser/server/offline clients still retain a cached `NORMAL` decision.

Central rule: **a composite authorization is a derived decision whose current applicability depends on its prerequisite graph and assumptions. Revocation or contradiction must invalidate affected derived decisions and their reusable decision caches by actual dependency and consequence scope. Historical evidence is preserved; unique data is preserved; stale authorization is not resurrected by cache, backup, restore or late-client return.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns exact Service Worker/controller/Cache Storage/HTTP cache/browser-storage/runtime boundaries and exposes which caches can outlive a page/session. Runtime cache invalidation cannot establish semantic authorization by itself.
- **B UX/IA/Content:** high dependency pressure. Must distinguish `previously authorized`, `revalidation required`, `limited capability`, `offline preservation available`, and `high-consequence action revoked`; exact copy/human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** destructive campaign expands **904 → 912 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures invalidation lag, stale-decision sightings, offline cohort gaps and contradiction propagation; telemetry cannot revoke or grant authority by itself.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns revocation dependency propagation, decision-cache contracts, anti-resurrection rules, bounded degradation and requalification.

## SOURCE

### RFC 7009 — revocation is immediate at the authorization server, but propagation can lag

RFC 7009 defines token revocation and explicitly notes that while invalidation occurs immediately at the authorization server, practical propagation delay can exist while some servers know of invalidation and others do not. It also notes that revocation can affect related tokens or the underlying grant depending on policy, and clients must tolerate unexpected invalidation.

Source: https://www.rfc-editor.org/rfc/rfc7009

**TRANSFER VALIDATION:** this is a bounded precedent for revocation propagation and dependent authorization invalidation. It does not define MintTap/PWA composite decisions, browser cache semantics or product re-entry policy.

### Service Worker registration/update/control are persistent runtime mechanisms, not semantic authorization

MDN documents that a Service Worker registration persists beyond individual `ServiceWorkerRegistration` objects; `update()` checks for a changed worker script; `clients.claim()` lets an active worker control clients in scope. CacheStorage is available to workers for offline responses.

Sources:  
https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration  
https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update  
https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim  
https://developer.mozilla.org/en-US/docs/Web/API/WorkerGlobalScope/caches

**TRANSFER VALIDATION:** these sources establish browser/runtime persistence and control boundaries. They do not prove server-side authority, queue semantic validity or organizational admission.

### NIST continuous-monitoring/assessment precedent remains bounded

NIST SP 800-137/137A and SP 800-53A remain bounded precedent for current control effectiveness, monitoring completeness and evidence-based reassessment. They do not prescribe a PWA composite-decision cache.

Sources:  
https://csrc.nist.gov/pubs/sp/800/137/final  
https://csrc.nist.gov/pubs/sp/800/137/a/final  
https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

## SYNTHESIS 1 — composite NORMAL is derived, not a new independent root

A composite decision such as `NORMAL for consequence C` is derived from prerequisite claims, compatible epochs, composition policy and decision authority. Caching the result does not sever those dependencies.

Guards:
- `decision cached ≠ decision independent`;
- `NORMAL once ≠ NORMAL forever`;
- `derived authorization ≠ new trust root`.

## SYNTHESIS 2 — distinguish historical validity from current applicability

A composite decision can have been correct at t1 and become inapplicable at t2 after credential revocation, verifier compromise, topology change, policy change or contradiction. Do not rewrite the historical closure as if it never existed.

Retain:
- decision identity and consequence scope;
- prerequisite/attestation set;
- composition-policy generation;
- authority/verifier context;
- valid-from / invalidated-at or review interval where knowable;
- invalidation cause and successor decision if any.

Guards:
- `revoked now ≠ historically false`;
- `historically valid ≠ currently applicable`.

## SYNTHESIS 3 — revocation propagation follows actual dependency edges

When prerequisite P is revoked or contradicted, find composite decisions that actually depended on P, then propagate to downstream consequences/closures that depended on those composites. Do not invalidate unrelated decisions merely because they share a timestamp, device or incident.

Guard: `same incident window ≠ same revocation blast radius`.

## SYNTHESIS 4 — decision caches need semantic cache keys

A reusable decision cache must bind enough context to prevent false reuse across changed assumptions. Generic dimensions include:
- subject/device/incarnation/service;
- consequence/capability;
- composition-policy generation;
- authority/policy/schema/configuration epochs as material;
- prerequisite attestation identifiers or generations;
- verifier/trust context;
- topology/dependency generation;
- invalidation/revocation generation.

A TTL alone is insufficient.

Guards:
- `cache hit ≠ authority hit`;
- `TTL valid ≠ assumptions valid`;
- `same user ≠ same incarnation/authority context`.

## SYNTHESIS 5 — revocation generation prevents stale decision resurrection

A useful generic pattern is a monotonic or otherwise anti-rollback **decision/revocation generation** at the authoritative boundary. A cached decision created under generation G7 cannot silently become current after authority has advanced to G8. Exact representation is implementation-specific and OPEN.

The generation itself must be protected from rollback/restoration; otherwise a backup can resurrect both stale decision and stale revocation state.

Guards:
- `cache restored ≠ cache current`;
- `generation restored from backup ≠ generation authoritative`.

## SYNTHESIS 6 — push invalidation is optimization, authoritative rejection is the safety boundary

Online invalidation signals can reduce stale-decision windows, but long-offline PWA clients may not receive them. High-consequence safety therefore cannot depend only on push/broadcast/telemetry delivery. The authoritative execution boundary must reject stale prerequisites/generations when the operation eventually arrives.

Guards:
- `revocation event sent ≠ revocation received`;
- `revocation received ≠ stale operation impossible`;
- `offline client unreachable ≠ revocation unenforceable later`.

## SYNTHESIS 7 — fail by consequence, preserve lower-risk capability and unique data

If publication authorization is revoked, local preservation/read or recovery export may remain available when their prerequisite graphs are unaffected. Revocation should not become indiscriminate data destruction.

Guards:
- `publication revoked ≠ local record disposable`;
- `high-consequence NORMAL revoked ≠ every capability revoked`.

## SYNTHESIS 8 — queued operations retain data but lose inherited authority

An offline operation queued while composite NORMAL was valid can arrive after a prerequisite has been revoked. Its payload/provenance may remain valuable, but execution authority must be evaluated against current policy where consequence requires it.

Guards:
- `queued while authorized ≠ execute forever`;
- `queue retained ≠ queue authorized`;
- `operation rejected ≠ record deleted`.

## SYNTHESIS 9 — Service Worker and Cache Storage can preserve stale runtime state without preserving authority

A worker/controller/cache can remain available across navigations and support offline responses. Updating a worker or clearing a cache can help runtime convergence, but neither is the semantic revocation boundary. Conversely, a stale worker/cache does not by itself mean unique local data should be destroyed.

Guards:
- `Service Worker still controls ≠ old NORMAL still authorized`;
- `Service Worker updated ≠ decision cache semantically invalidated everywhere`;
- `Cache Storage cleared ≠ server-side stale authority fenced`.

## SYNTHESIS 10 — server-side decision caches require dependency-aware invalidation too

The stale-NORMAL problem is not browser-only. API gateways, resource servers, policy engines, workers/jobs and application caches may retain authorization/composition results. Invalidation design must enumerate all consequence-bearing decision caches and their dependency/revocation behavior.

Guard: `browser cache fixed ≠ authorization cache fixed`.

## SYNTHESIS 11 — backup/PITR restore must not roll authorization backward

Restoring application state can reintroduce an older decision cache, old queue or old prerequisite snapshot. Recovery needs a post-restore reconciliation against a current authority/revocation source that is not rolled back in the same failure domain, or an explicitly governed rebootstrap when that source is also lost.

Guards:
- `PITR successful ≠ authorization state current`;
- `backup internally consistent ≠ backup current enough to grant authority`.

## SYNTHESIS 12 — late-returning clients enter requalification, not inherited NORMAL

A six-week-offline iPad may return with a historically valid composite decision C17. If central state has revoked one prerequisite, C17 remains historical evidence but not current authorization. Preserve unique records, fence auto-replay/high-consequence effects, obtain current bootstrap/revocation generation, reconcile queued operations, then construct a new applicable composite decision.

Guard: `late client presents old NORMAL ≠ old NORMAL resurrected`.

## SYNTHESIS 13 — contradiction invalidates affected cache entries before full root-cause certainty

If bounded evidence shows a decisive prerequisite may no longer hold, affected high-consequence cached decisions should not remain usable merely because the incident cause is still unknown. Mark them `UNDER-REVALIDATION` or equivalent and preserve evidence. Do not claim global compromise without dependency evidence.

Guard: `root cause unknown ≠ affected stale decision safe to reuse`.

## SYNTHESIS 14 — invalidation itself needs acknowledgement/coverage evidence

For material consequences, record enough to know:
- what prerequisite/revocation event occurred;
- which derived decisions were identified as dependent;
- which authoritative execution boundaries now reject stale generations;
- which online cohorts converged;
- what offline/unknown tail remains;
- what requalification is required on return.

Telemetry can expose coverage gaps but cannot itself grant authority.

Guard: `invalidation job green ≠ every stale decision unreachable`.

## SYNTHESIS 15 — anti-resurrection applies to manual/admin paths too

An operator spreadsheet, support console, export/import path or emergency runbook can carry a stale `approved/NORMAL` marker. Manual surfaces require the same semantic rule: historical approval is evidence, not a perpetual authority token.

Guard: `human-approved previously ≠ human-approved currently`.

## SYNTHESIS 16 — reauthorization creates successor evidence

After revocation, do not edit C17 back to green. Create successor decision C18 under current prerequisites/composition policy, preserving why C17 ceased to apply. This maintains auditability and prevents history laundering.

Guard: `revalidated now ≠ old decision was never revoked`.

## SYNTHESIS 17 — revocation storms need bounded degradation, not bypass

A widespread prerequisite revocation can invalidate many composites at once. Operational pressure must not create a bypass that treats cached NORMAL as good enough. Use consequence-aware degraded modes, recovery-only capabilities and governed emergency bridges where justified.

Guard: `large revocation blast radius ≠ bypass revocation semantics`.

## SYNTHESIS 18 — generic invalidation/requalification pattern

For a material prerequisite revocation or contradiction:
1. preserve the revocation/contradiction evidence and affected prerequisite identity;
2. resolve actual dependent composite decisions and downstream consequences;
3. advance or otherwise establish current revocation/decision generation at the authoritative boundary;
4. invalidate affected server/runtime/manual decision caches by semantic dependency, not only TTL;
5. block stale high-consequence operations while preserving unique data and unaffected lower capabilities;
6. record online convergence and unresolved offline/unknown tail;
7. on late-client return, preserve local records and prevent inherited NORMAL/auto-replay;
8. reconcile queued operations under current policy/authority;
9. create successor composite evidence only after compatible prerequisites are current;
10. retain historical decision and invalidation provenance.

This is a reasoning contract, not a mandated implementation architecture.

## Track C destructive campaign additions — 904 → 912

1. **revoked-prerequisite cached-NORMAL:** decisive prerequisite revoked but cached composite remains usable. Expected: dependent consequence degrades/revalidates.
2. **TTL-only decision cache:** cache TTL remains valid after authority/policy generation changes. Expected: semantic invalidation despite TTL.
3. **push-only revocation:** online clients receive invalidation but offline client later submits stale operation successfully. Expected: authoritative boundary rejects stale generation.
4. **worker-update authority theater:** Service Worker updates and UI shows current while server-side cached authorization remains stale. Expected: runtime update not treated as semantic revocation closure.
5. **PITR stale-NORMAL resurrection:** backup restores old composite cache and revocation generation. Expected: post-restore current-authority reconciliation prevents rollback.
6. **late-client inherited-NORMAL:** long-offline iPad reconnects with old composite and auto-replays queued mutation. Expected: preserve data, fence replay, requalify locally.
7. **global-revocation overreach:** one prerequisite affects publication only but system destroys/blocks unrelated preservation data. Expected: consequence-scoped degradation.
8. **manual-path resurrection:** support/admin workflow imports an old approved marker after automated caches were invalidated. Expected: manual path cannot revive superseded authority.

These are defined cases, not executed product evidence.

## EFB / LogMate-like application case

Scenario: a company iPad was offline for six weeks. At departure it held composite decision C17 permitting a remote-finalization class of operation under authority A9/policy P14. While offline, a decisive credential/verifier prerequisite is revoked and central revocation generation advances. The iPad returns with unique flight records and queued operations, while its Service Worker and local UI still present C17 as `NORMAL`.

Generic safe handling:
1. preserve unique records, queue payloads and provenance;
2. treat C17 as historical evidence, not current authority;
3. obtain current bootstrap/revocation generation before high-consequence replay;
4. prevent the stale worker/UI/cache from overriding authoritative rejection;
5. evaluate each queued operation under current consequence policy;
6. retain rejected operations/provenance where required rather than deleting records;
7. migrate/reconcile local runtime/schema state as needed;
8. construct successor composite C18 only from compatible current prerequisites;
9. verify obsolete C17/generation cannot execute at the authoritative boundary;
10. record remaining offline/unknown fleet-tail obligations.

**OPEN:** actual LogMate auth/session/backend/MDM/WebKit/queue/data model and aviation/legal consequences remain unverified.

## Cross-track transfer

### Track A
Own exact browser cache/Service Worker/controller/storage semantics and capability differences. Transfer rule: runtime persistence/currentness is input evidence only; it cannot authorize semantic NORMAL.

### Track B
Design recovery/revalidation states that do not tell the user data is lost merely because remote consequence is blocked. Exact UX requires Design Studio + human/AT validation.

### Track C
Execute the destructive matrix against actual implementation when available, including browser/server/manual cache combinations, offline return, restore and stale-operation rejection.

### Track D
Measure invalidation latency, stale-decision sightings, cohort coverage and unknown tail. Never convert absence of telemetry into proof that no stale decision exists.

### Track E
Own dependency-aware revocation, authoritative rejection, cache invalidation, restore anti-rollback, bounded degradation and successor requalification.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate-like PWA work unless stronger product evidence supersedes this generic rule:
- model material `NORMAL` decisions as derived and revocable;
- preserve dependency/provenance needed to identify affected composites;
- make decision-cache reuse assumption/epoch/revocation aware rather than TTL-only;
- require authoritative stale-operation rejection for high-consequence offline return rather than relying only on push invalidation;
- preserve unique local data separately from execution authority;
- treat Service Worker/cache convergence as runtime evidence, not authority restoration;
- prevent backup/PITR/manual/import paths from resurrecting superseded authority;
- create successor reauthorization evidence rather than rewriting revoked historical decisions.

## OPEN / VALIDATION

Production validation remains OPEN for:
- actual decision/composition caches and their locations;
- actual auth/session/token revocation semantics;
- authoritative generation/epoch representation;
- Service Worker/cache/IndexedDB/queue behavior on target browsers and installed PWA;
- physical iOS/iPadOS/managed-device behavior;
- server/gateway/job/manual/admin cache topology;
- backup/PITR/reimport rollback behavior;
- exact degraded-mode consequence policy;
- offline fleet inventory and MDM/ADE topology;
- product/domain/aviation/legal authority.

## CHANGE WATCH

- Browser/WebKit Service Worker/storage behavior and eviction remain platform/version sensitive.
- Authentication/session/token revocation mechanisms depend on actual provider and architecture.
- Apple managed-device/PWA behavior requires current Apple/WebKit evidence and physical-device validation.

## Gate

**269 PASS (generic).** The Web Manager can now reason about revoking previously valid composite re-entry decisions, dependency-scoped invalidation, semantic decision-cache keys, authoritative anti-resurrection boundaries, backup/restore rollback, offline queued operations and late-client requalification without deleting unique data or confusing browser runtime convergence with authority convergence.

Production/runtime/product/domain PASS is not claimed.

## Next high-value adjacent target

**270 — revocation-distribution authenticity, invalidation-channel partition & anti-rollback recovery:** determine how clients/servers distinguish authentic current revocation state from forged, delayed or partitioned invalidation signals; how high-consequence operations behave when the revocation channel itself is unavailable; and how a recovered channel re-establishes monotonic currentness without allowing a stale replica or restored client to roll revocation state backward.