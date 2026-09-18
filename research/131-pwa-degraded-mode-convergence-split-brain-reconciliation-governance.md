# 131 — PWA Degraded-Mode Convergence & Split-Brain Reconciliation Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 083–130 PWA/recovery chain; Track A offline/browser/storage mechanics; Track B reconciliation UX; Track C conflict/idempotency/destructive tests; Software Engineering Data D006 for implementation-level sync semantics.

## Purpose

130 established that partial recovery must not silently restore stale authority. The next failure appears when two or more clients were independently useful while disconnected and later reconnect with different histories.

Central rule:

> **Connectivity recovery is not convergence. Re-entry requires explicit operation identity, version/provenance checks, deletion semantics and conflict policy; ambiguity must not be converted into authority by timestamp or login freshness.**

`split-brain` is used here descriptively for divergent client/server histories, not as a claim that a particular distributed consensus protocol is implemented.

## 1. Five-track balance

- **A Platform/Browser — dependency supplier:** IndexedDB/Cache Storage, browser lifecycle and intermittent connectivity constrain when local operations can be recorded or retried. Browser storage does not define domain conflict semantics.
- **B UX/IA/Content — elevated consumer:** owns truthful `saved locally / pending / conflict / resolved / authoritative` state, comparison/recovery flows and user-mediated conflict requirements.
- **C Quality — high dependency pressure:** owns duplicate delivery, stale update, delete resurrection, ambiguous ACK, concurrent edit and restart/retry oracles.
- **D Search/Analytics — supporting consumer:** conflict/queue/reconciliation metrics can diagnose outcomes but missing telemetry cannot prove offline population convergence.
- **E Architecture/Security/Operations — highest-risk owner:** owns authority boundaries, operation identity, preconditions, reconciliation policy, tombstone lifecycle and normalization gates.

Allocation remains E-heavy, but the Software Engineering Data handoff is unusually strong because exact sync implementation semantics belong there.

## 2. SOURCE — HTTP already separates retry safety from concurrent-write safety

RFC 9110 defines PUT, DELETE and safe methods as idempotent in intended server effect, allowing automatic retry after an ambiguous transport failure. The same RFC separately defines conditional requests and `If-Match`; state-changing preconditions can prevent the lost-update problem when clients act in parallel.

Sources checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2
- https://www.rfc-editor.org/rfc/rfc9110.html#section-13
- https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1

**SYNTHESIS:** idempotency answers whether repeating one logical operation can avoid an unintended second effect. A version/precondition answers whether that operation is still valid against current state. Neither substitutes for the other.

Guards:
- `retry-safe ≠ conflict-safe`;
- `same operation repeated ≠ two independent user intents`;
- `request succeeded once ≠ stale concurrent intent is valid now`.

The IETF HTTPAPI `Idempotency-Key` draft is **expired as of 2026-04-18**. It remains useful historical design evidence for client-generated logical-operation identity on POST/PATCH, but is not promoted as a current RFC requirement. CHANGE WATCH: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/

## 3. SOURCE — real platforms expose conflict instead of making it disappear

Apple CloudKit `recordChangeTag` changes when a record is saved. When a client saves, CloudKit compares the client's tag with the server tag; mismatch is handled according to save policy. `ifServerRecordUnchanged` proceeds only when tags match, and `serverRecordChanged` exposes ancestor/client/server versions for resolution logic.

Sources checked 2026-09-18:
- https://developer.apple.com/documentation/cloudkit/ckrecord/recordchangetag
- https://developer.apple.com/documentation/cloudkit/ckmodifyrecordsoperation/recordsavepolicy
- https://developer.apple.com/documentation/cloudkit/record-changed-error-keys

CloudKit change tokens separately identify a point in database/zone change history and are opaque; Apple says not to infer order or behavior from token contents. This illustrates the distinction between **replication progress** and **record conflict/version identity**.

Source: https://developer.apple.com/documentation/cloudkit/ckserverchangetoken

**TRANSFER VALIDATION:** this is evidence that mature sync APIs preserve explicit version/progress concepts. It is not a requirement to use CloudKit or its exact conflict model.

## 4. SOURCE — last-write-wins is a policy, not a correctness theorem

Current Firebase Firestore documentation states that offline clients synchronize local changes when connectivity returns and that multiple changes to the same document use **last write wins**. It also exposes cache-origin metadata because cached data may be stale or incomplete.

Source checked 2026-09-18:
- https://firebase.google.com/docs/firestore/enterprise/enable-offline

**SYNTHESIS:** LWW can be a valid product policy for low-consequence replaceable state, but it can discard concurrent intent. Its availability in an SDK does not prove suitability for flight-log-like records, deletions, provenance-sensitive data or irreversible operations.

Guards:
- `SDK syncs automatically ≠ domain conflict policy is correct`;
- `last write wins ≠ latest intent wins`;
- `newest timestamp ≠ most authoritative record`.

Actual LogMate backend/Firestore use is OPEN; no product architecture is inferred here.

## 5. Separate the identities

A robust reconciliation design distinguishes at least:

1. **record identity** — which domain object is affected;
2. **operation identity** — which logical user/system action this is;
3. **actor/device identity** — who/what produced it;
4. **base revision/version** — state the operation believed it was changing;
5. **operation payload** — requested semantic change;
6. **local sequence/provenance** — useful for diagnosis, not automatically global order;
7. **server receipt/application identity** — whether the operation was accepted/applied;
8. **resulting authoritative revision** — state after reconciliation;
9. **deletion/tombstone identity** — deletion is a domain event, not mere absence;
10. **replication cursor/change token** — progress marker, not record authority by itself.

Do not collapse these into one timestamp or auto-increment counter.

## 6. Ambiguous acknowledgement and idempotency

A classic offline/retry failure is:
1. client transmits operation O;
2. server commits O;
3. ACK is lost;
4. client retries O after reconnect/restart.

If O has durable logical identity and the server retains sufficient deduplication/result state, the retry can be recognized as the same logical action. If a new operation ID is generated on every retry, the server can legitimately interpret the retry as new intent.

This aligns with Software Engineering Data D006, which already has executable evidence for server death after commit/before ACK and shows one effect with durable operation identity versus duplicate application without deduplication. Its exact LogMate transfer also establishes that inbound cursor advancement must not outrun durable semantic effects unless another validated replay/reconciliation mechanism exists.

**TRANSFER VALIDATION:** consume D006 as implementation-level distributed-data evidence; Web Manager owns the PWA/web authority requirement, not its database implementation.

Guards:
- `ACK missing ≠ commit missing`;
- `retry request new ≠ logical operation new`;
- `deduplicated ≠ semantically conflict-free`;
- `cursor advanced ≠ every semantic effect safely published`.

## 7. Concurrent edit conflict

Example: server revision R5; iPad A and phone B both go offline from R5. A edits flight remarks; B edits block time. Later A produces R6 and B reconnects with an operation based on R5.

Possible policies include:
- reject B's stale precondition and request reconciliation;
- merge independently safe fields if the domain model explicitly supports it;
- present ancestor/local/server versions for user-mediated resolution;
- domain-specific deterministic merge with preserved provenance.

Blind whole-record LWW is only one policy and may erase A or B's intent. Field-level merge is also not universally safe: two fields can be semantically coupled.

Guard: `different fields changed ≠ changes commute safely`.

## 8. Delete/update conflict and tombstones

Absence is ambiguous in replicated/offline systems. A record missing locally might mean never fetched, evicted cache, filtered view, deletion observed, or corruption. If deletion is represented only by physical absence, a long-offline client can later replay an old update and resurrect a deleted record.

Generic direction:
- represent deletion with durable identity/revision/provenance long enough for the supported offline/retry horizon;
- make update-against-deleted-state an explicit policy decision;
- do not garbage-collect tombstone/dedup state until the system can justify that supported stale clients/operations cannot require it, or a stronger rebootstrap barrier exists.

Guards:
- `record absent ≠ deletion proven`;
- `delete acknowledged ≠ every offline client observed deletion`;
- `tombstone GC safe for current clients ≠ safe for long-offline clients`;
- `old update arrives ≠ deleted record should resurrect`.

Actual tombstone retention horizon remains OPEN.

## 9. Authentication freshness does not repair data history

Fresh login can establish current account/session authority. It does not prove that queued operations were created under current policy, against current record revisions, before a deletion, or outside a compromise interval.

Therefore reconnect should conceptually separate:
1. current authentication/trust/client-generation admission;
2. inbound remote-change catch-up;
3. local queued-operation classification;
4. per-operation precondition/idempotency/conflict checks;
5. user/domain reconciliation where required;
6. authoritative acknowledgement/result publication.

Guard: `fresh login ≠ queued operation fresh`.

## 10. Direct device-to-device sync boundary

Nothing in this study assumes unattended iPad↔phone direct synchronization, background execution, hotspot availability, WebRTC reachability or peer discovery. The reconciliation model applies whether transport is server-mediated, manually exported/imported, or another validated architecture.

Guard: `reconciliation semantics defined ≠ transport capability proven`.

## 11. User-mediated reconciliation — Track B transfer

When automation cannot safely preserve intent, user-mediated reconciliation must expose enough context to make a meaningful choice:
- record identity and recognizable domain context;
- local change vs current authoritative/server version;
- what changed, not merely raw JSON;
- whether deletion occurred;
- saved/synced/acknowledged/conflicted state;
- consequences of keep-local, keep-current, merge or duplicate;
- non-destructive escape/export where feasible.

Do not ask users to resolve conflicts that the system can deterministically and safely resolve, but do not silently automate a choice when domain semantics are unknown.

Accessibility, screen-reader announcements, keyboard order, 200% reflow and physical-device behavior remain runtime validation requirements.

## 12. Normalization/convergence gate

A client does not become `NORMAL` merely because its queue is empty. Relevant claims can include:
1. supported client/worker/API/trust generation;
2. current remote changes fetched through a valid progress boundary;
3. every queued logical operation classified;
4. duplicate retries recognized where required;
5. stale-base operations rejected or reconciled;
6. deletion/tombstone conflicts resolved;
7. no quarantined/unknown operations silently dropped;
8. durable local receipt/progress state does not outrun semantic effects;
9. user-visible status matches authoritative outcomes;
10. negative stale/replay/resurrection tests pass.

Guards:
- `queue empty ≠ converged`;
- `all requests 2xx ≠ all intents reconciled`;
- `client caught up ≠ fleet converged`.

## 13. Track C validation campaign

1. commit-before-ACK loss + identical operation retry → one semantic effect;
2. same payload with distinct operation IDs → distinct intent unless domain rejects it;
3. same operation ID with changed payload → reject/flag identity misuse;
4. stale base revision update → conflict, not overwrite;
5. concurrent same-field edit → explicit policy;
6. concurrent different-field edit with coupled invariant → no unsafe auto-merge;
7. delete vs stale update → no silent resurrection;
8. delete observed on one client, unseen on another → tombstone preserved;
9. tombstone retention expiry + long-offline return → rebootstrap/defined barrier;
10. stale queued op after fresh login → still version/provenance checked;
11. stale worker/current session → remote write gate remains enforced;
12. current worker/stale queue → queue not automatically trusted;
13. cursor/progress commit before entity/tombstone apply + crash → replayability preserved or test fails;
14. entity apply before cursor commit + crash → safe replay/idempotency required;
15. duplicate inbound change → one semantic result;
16. out-of-order changes → revision/precondition prevents regression;
17. local clock rollback → no authority inversion;
18. device clock far ahead → no LWW authority by timestamp;
19. operation ID collision → detectable failure;
20. dedup record GC too early → duplicate replay detected in test;
21. partial batch apply → progress marker cannot falsely cover unapplied effects;
22. conflict UX survives reload/restart;
23. conflict state is keyboard reachable and non-color-only;
24. user chooses keep-current → local losing version remains recoverable/exportable if policy requires;
25. user chooses keep-local → new authoritative revision created through current precondition, not blind overwrite;
26. merge failure → originals preserved;
27. offline client missing telemetry → fleet convergence not inferred;
28. queue empty after silent drop → normalization fails;
29. record absent due cache eviction → not interpreted as delete;
30. direct peer transport unavailable → server/manual recovery path semantics remain coherent.

## 14. Cross-repository evidence

Design Studio Web `progress/WEB_STATUS.md` checked 2026-09-18: **W082 SEMANTIC FOCUS IDENTITY RUNTIME PROVENANCE; Stage 3 PRACTICE / NOT PASSED**. W082 strengthens the requirement that runtime state transitions preserve stable semantic identity rather than ordinal/visual position alone. Cross-browser/Safari/Firefox, persisted configuration, screen-reader, physical-device, field-CWV and human UX remain OPEN.

Software Engineering Data `progress/DATA_STATUS.md` checked 2026-09-18: **Stage 1 IN STUDY / NOT YET PASSED**. D006 has bounded executable replication/idempotency/conflict evidence and an exact-ref LogMate inbound cursor atomicity transfer. It explicitly leaves real mobile/backend, dedup retention/GC, tombstone GC and multi-writer evidence OPEN. This is the correct implementation handoff; do not duplicate D006 here.

## 15. MINTTAP DIRECTION

For a PWA/EFB-like product, design synchronization as an explicit reconciliation protocol rather than `network restored → flush queue`. Preserve logical operation identity and base/version context across restart/offline periods; make deletion explicit; require current authorization separately from operation validity; and use user/domain reconciliation when concurrent intent cannot be safely automated.

Do not select CRDT, event sourcing, CloudKit, Firestore, server-authoritative LWW or another implementation pattern until actual product data invariants, multi-writer requirements, offline horizon and backend architecture are known.

## 16. OPEN / VALIDATION / CHANGE WATCH

**OPEN:** LogMate/MintTap authoritative data model, record/operation IDs, server revisions, allowed offline edits/deletes, backend, actual conflict policy, dedup retention, tombstone retention, batch/cursor semantics, multi-device topology, direct-device transport, safety/legal consequence and managed-iPad behavior.

**VALIDATION:** real browser/IndexedDB restart; physical iPad; mobile/native counterpart; ambiguous network/ACK; concurrent writers; process termination; queue persistence; stale update/delete resurrection; tombstone/dedup expiry; accessibility of reconciliation UX; actual backend transaction/progress semantics.

**CHANGE WATCH:** browser storage/eviction and background behavior; Service Workers; WebKit/iOS/iPadOS PWA policy; selected backend SDK offline/conflict semantics; IETF idempotency work if revived/replaced.

## 17. Persistent guards

`connectivity recovery ≠ convergence`.  
`retry-safe ≠ conflict-safe`.  
`ACK missing ≠ commit missing`.  
`retry request new ≠ logical operation new`.  
`deduplicated ≠ semantically conflict-free`.  
`last write wins ≠ latest intent wins`.  
`newest timestamp ≠ most authoritative record`.  
`different fields changed ≠ changes commute safely`.  
`record absent ≠ deletion proven`.  
`delete acknowledged ≠ every offline client observed deletion`.  
`old update arrives ≠ deleted record should resurrect`.  
`fresh login ≠ queued operation fresh`.  
`queue empty ≠ converged`.  
`client caught up ≠ fleet converged`.  
`reconciliation semantics defined ≠ transport capability proven`.

## Gate

**PASS (generic).** The Web Manager can now separate retry/idempotency from concurrent conflict, distinguish operation/record/revision/progress identities, govern stale updates and tombstones, define a capability-safe convergence gate and hand implementation-level sync semantics to Software Engineering without assuming product facts.

## Next high-value adjacent work

**PWA reconciliation policy evolution & schema/version conflict governance:** determine what happens when long-offline operations were created under an older domain schema, validation rule, conflict policy or operation format; separate syntactic migration from semantic re-authorization, preserve rejected operations for recovery, and prevent a schema upgrade from silently rewriting historical user intent.