# 132 — PWA Reconciliation Policy Evolution & Schema/Version Conflict Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 083–131 PWA/recovery chain; Track A IndexedDB/Service Worker version mechanics; Track B rejected-operation/recovery UX; Track C migration/replay/conflict oracles; Software Engineering Data D003/D006 for implementation-level schema/sync evidence.

## Purpose

131 established that reconnect is reconciliation rather than queue flushing. A harder case occurs when the queued operation itself was created under an older schema, validation rule, authorization model, conflict policy, operation encoding or client generation.

Central rule:

> **Syntactic migration can make old data readable; it does not make old intent semantically valid or currently authorized. Preserve original intent/provenance, classify compatibility explicitly, and never let an upgrade silently manufacture a new user decision.**

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** IndexedDB versionchange and Service Worker lifecycle explain local schema/code transitions but do not define domain semantics.
- **B UX/IA/Content — elevated consumer:** owns truthful `needs review / unsupported old operation / recovered copy / current authoritative result` states and non-destructive user recovery.
- **C Quality — high dependency pressure:** owns old-reader/new-writer, new-reader/old-writer, interrupted migration, stale-policy replay, unknown-field loss and semantic-drift oracles.
- **D Search/Analytics — supporting consumer:** schema-version telemetry can diagnose population state; absence of events cannot prove long-offline clients are upgraded.
- **E Architecture/Security/Operations — highest-risk owner:** owns compatibility contracts, policy epochs, admission gates, migration provenance and retirement boundaries.

Allocation remains E-heavy because an apparently successful migration can silently convert obsolete authority into current mutation authority.

## 2. SOURCE — Web storage schema version is structural, not domain authorization

IndexedDB opens with an integer database version. Structural changes such as object-store/index creation or deletion occur in a `versionchange` transaction during `upgradeneeded`; old open connections can block an upgrade until they close. MDN also documents `VersionError` for attempts to open with an older version after a newer database version exists.

Sources checked 2026-09-18:
- https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/versionchange_event
- https://developer.mozilla.org/en-US/docs/Web/API/IDBRequest/transaction

**SYNTHESIS:** browser database versioning answers whether local storage structure can be upgraded transactionally. It does not prove that every stored operation remains meaningful under the new domain model.

Guards:
- `IndexedDB upgrade committed ≠ queued intent semantically migrated`;
- `schema structurally current ≠ record semantically current`;
- `local migration succeeded ≠ server accepts old operation`.

## 3. SOURCE — Service Worker/client versions can overlap during rollout

The Service Worker lifecycle permits a newly installed worker to wait while an older worker controls existing pages; activation/control can be accelerated with `skipWaiting()` and `clients.claim()`. Therefore code/worker/storage/API generations must not be assumed to switch atomically as one unit.

Sources checked 2026-09-18:
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting
- https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim

**SYNTHESIS:** forced activation can reduce rollout latency but cannot by itself prove compatibility between a newly controlling worker, already-loaded application code, local IndexedDB schema, queued operations and current API semantics.

Guards:
- `new worker active ≠ every client/data schema migrated`;
- `skipWaiting + claim ≠ atomic application migration`;
- `worker generation current ≠ operation-policy generation current`.

## 4. SOURCE — format compatibility is directional and can be lossy

Protocol Buffers documents wire-safe, wire-unsafe and conditionally compatible schema changes. Binary protobuf preserves unknown fields, while converting through JSON or field-by-field copying can lose unknown fields. ProtoJSON documents changes that remain parseable but can still lose information or require carefully staged rollout.

Sources checked 2026-09-18:
- https://protobuf.dev/programming-guides/proto3/#updating
- https://protobuf.dev/programming-guides/proto3/#unknowns
- https://protobuf.dev/programming-guides/json/#json-options

RFC 9170 further observes that protocol extension/version-negotiation mechanisms need active use or deployment ossification can make later evolution unreliable.

Source: https://www.rfc-editor.org/rfc/rfc9170.html

**TRANSFER VALIDATION:** these are protocol-evolution examples, not a requirement to use protobuf. They establish that compatibility is relational among reader, writer, representation and rollout state, and that parseability is weaker than semantic preservation.

Guards:
- `parseable ≠ lossless`;
- `lossless representation ≠ same domain meaning`;
- `backward-readable ≠ backward-writable`;
- `unknown field ignored ≠ unknown intent safely discarded`.

## 5. SOURCE — operation semantics can depend on a known base

RFC 5789 defines PATCH as instructions applied to an existing resource and warns that some patch formats require a known base point; it recommends conditional requests such as strong ETag/If-Match where collisions could corrupt state. It also requires the directly affected patch changes to be applied atomically or not at all.

Source checked 2026-09-18: https://www.rfc-editor.org/rfc/rfc5789.html

**SYNTHESIS:** an old operation cannot be made safe merely by translating its field names. Its base revision, operation semantics and current invariants remain relevant.

Guard: `operation translated ≠ operation valid against current base`.

## 6. Separate the version dimensions

Do not collapse `version` into one integer. A reconciliation envelope may need to distinguish:

1. **storage schema version** — local IndexedDB structure;
2. **record/domain schema version** — fields/types/invariants understood when record was authored;
3. **operation format version** — how queued intent is encoded;
4. **validation-policy epoch** — rules under which the intent was locally accepted;
5. **authorization/trust epoch** — authority context when intent was created;
6. **conflict-policy epoch** — merge/reject semantics expected by the producer;
7. **API/protocol generation** — remote contract targeted;
8. **application/worker generation** — code interpreting local state;
9. **base authoritative revision** — record state the operation intended to change;
10. **migration provenance** — transformations applied after original creation.

A single `schemaVersion=7` cannot safely stand in for all ten.

## 7. Compatibility is a matrix, not a flag

For each supported transition evaluate at least:
- old writer → new reader;
- new writer → old reader;
- old operation → new server;
- new remote record → old client;
- old local database → new application;
- new application rollback → already-upgraded local database;
- old conflict policy → new conflict policy;
- old validation/authorization epoch → current admission policy.

A transition can be read-compatible but not write-compatible, format-compatible but semantically incompatible, or reversible for records but irreversible for queued operations.

Guards:
- `backward compatible ≠ bidirectionally compatible`;
- `record migration reversible ≠ operation migration reversible`;
- `old reader survives ≠ old writer remains authorized`.

## 8. Migration must preserve original intent and transformation provenance

For queued/offline operations, retain enough immutable original context to answer:
- what did the user/system originally request;
- against which record/base revision;
- under which schema/operation/policy epoch;
- what migration transformed it;
- which fields were defaulted, dropped, split, combined or derived;
- whether the transformed operation still has identical semantics.

Prefer transformation into a **candidate current operation** rather than overwriting the historical envelope in place. If equivalence cannot be demonstrated, classify for review/rejection/recovery rather than silently publishing.

Guards:
- `migration function returned success ≠ semantic equivalence proven`;
- `default inserted ≠ user chose default`;
- `field renamed ≠ meaning unchanged`;
- `new representation signed/stored ≠ user re-authorized transformed intent`.

## 9. Validation and authorization rule evolution

Example: an old client allowed a flight record field to be blank; the current domain requires a value. Possible outcomes include:
- deterministic lossless derivation from preserved authoritative context;
- explicit grandfathered historical record that remains readable but not newly writable;
- user-mediated completion;
- quarantine/rejection with original operation recoverable/exportable.

Do **not** invent a value merely to satisfy the new schema and then claim the user supplied it.

Security-sensitive rule changes are stricter. If a capability is no longer authorized, syntactic migration must not reactivate it. Current server-side admission remains authoritative for remote mutation.

Guards:
- `valid under old policy ≠ valid under current policy`;
- `current schema requires value ≠ system may fabricate user intent`;
- `historical record grandfathered ≠ obsolete mutation authority grandfathered`.

## 10. Conflict-policy evolution

Suppose v1 used LWW and v2 requires revision preconditions/user mediation. A v1 queued operation returning after v2 rollout must not be processed with LWW merely because that was the old client's expectation if current consequence policy rejects that behavior.

Conversely, replaying v1 intent through v2 semantics can produce a different outcome. Preserve that distinction explicitly: **the old operation is historical evidence; the v2 reconciliation decision is a new system/user decision.**

Guard: `old conflict policy recorded ≠ old conflict policy remains executable`.

## 11. Unknown fields and semantic opacity

An old client may carry fields it cannot interpret or a new client may encounter opaque historical extensions. Preservation can be safer than discard when round-trip fidelity matters, but preserved opaque data must not be granted semantics it does not have.

For provenance-sensitive records:
- retain unknown original bytes/fields where the chosen representation supports it and policy requires fidelity;
- do not normalize unknown fields away through a lossy intermediate format without explicit acceptance;
- do not let unknown fields bypass current validation/authorization merely because they are opaque.

Guards:
- `opaque preserved ≠ opaque trusted`;
- `unknown ignored for display ≠ unknown safe for write-through`.

## 12. Migration ordering and crash boundaries

A dangerous local sequence is:
1. mark database/schema as current;
2. begin converting queued operations;
3. crash after some operations are rewritten;
4. restart and skip migration because version marker already advanced.

This mirrors Software Engineering Data D003/D006 publication-order findings. Migration completion/progress must not outrun durable semantic effects unless replay/recovery is independently proven.

**DEPENDENCY:** Data D003 owns executable schema-migration mechanics; D006 owns replication/cursor atomicity. Web Manager consumes their principle rather than duplicating fixtures.

Guards:
- `version marker advanced ≠ every semantic migration completed`;
- `database opens cleanly ≠ migration complete`;
- `structural integrity check PASS ≠ semantic migration PASS`.

## 13. Rejected-operation recovery

An obsolete operation can be unsafe to execute yet valuable to the user. Rejection should not automatically mean destruction.

Generic recovery envelope:
- original immutable operation/provenance;
- rejection reason and current policy/schema mismatch;
- current authoritative record where available;
- safe human-readable comparison;
- export/copy/manual reconstruction path where justified;
- explicit state preventing automatic retry.

For EFB/LogMate-like data, local historical record accessibility and remote mutation authority remain separate. This does not establish any legal/safety retention requirement; those remain OPEN.

Guard: `operation rejected ≠ user data should be silently deleted`.

## 14. Compatibility retirement

Long-offline support cannot mean every historical writer remains executable forever. Define support horizons per capability and preserve a stronger recovery path beyond the mutation horizon:
- supported current mutation;
- supported migration/reconciliation;
- read/export/recovery only;
- unsupported/unverifiable with explicit preservation where feasible.

Retiring an API/schema writer must be paired with a stale-client admission barrier so a long-offline client cannot resurrect retired semantics after reconnect.

Guards:
- `old data recoverable ≠ old writer supported`;
- `old client can open ≠ old client may mutate remotely`;
- `compatibility retired ≠ historical evidence deleted`.

## 15. Track B degraded/reconciliation UX transfer

User-visible states should distinguish at least:
- migration in progress;
- local data readable but sync temporarily unavailable;
- operation needs review because rules changed;
- operation rejected but original preserved;
- current authoritative result;
- recovery/export available.

Do not present `Updated successfully` merely because local schema conversion completed. Accessibility of comparison/recovery flows remains runtime validation, not a generic PASS.

## 16. Track C validation campaign

1. old DB/new app structural upgrade commits atomically;
2. old tab blocks versionchange → truthful update/reload state;
3. crash before version marker → migration safely retries;
4. crash after partial transform/before completion marker → no skipped operations;
5. marker advanced before effects → oracle detects false completion;
6. new app rollback against newer DB → fail/recovery path, not silent downgrade;
7. old operation/new server parseable but invalid under new rule → explicit rejection;
8. old operation field renamed with changed semantics → no blind translation;
9. required new field has no historical source → no fabricated user value;
10. deterministic derivation exists → provenance records derivation;
11. unknown field survives supported lossless round trip;
12. JSON/intermediate conversion drops unknown field → test detects loss;
13. opaque unknown field cannot bypass current authorization;
14. old LWW op under new precondition policy → conflict/review, not LWW fallback;
15. old authorization epoch after privilege removal → denied despite migration;
16. fresh login + old operation → operation still policy/version checked;
17. old operation against deleted/tombstoned record → no resurrection;
18. operation migration changes payload → original remains recoverable;
19. same operation migrated twice → deterministic/idempotent candidate result or explicit failure;
20. migration code version changes → provenance identifies transformer;
21. record migration succeeds but operation migration fails → no false NORMAL;
22. API generation retired → read/export path remains separate from write;
23. old worker/new DB mismatch → controlled recovery, not corruption;
24. new worker/old loaded page via claim → compatibility oracle catches mixed generation;
25. offline for longer than mutation-support horizon → rebootstrap/review barrier;
26. rejected operation survives reload/restart;
27. user-mediated correction creates a new current operation, not mutation of historical evidence;
28. queue empty because incompatible operations were silently dropped → normalization fails;
29. telemetry misses offline clients → fleet compatibility not inferred;
30. physical iPad/browser termination during migration → product validation required before PASS.

## 17. Cross-repository evidence

Design Studio Web `progress/WEB_STATUS.md` checked 2026-09-18: **W083 DYNAMIC FOCUS-REMOVAL RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. It strengthens semantic destination/fallback requirements when active UI objects disappear, useful for migration/reconciliation states. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device and human UX remain OPEN.

Software Engineering Data `progress/DATA_STATUS.md` checked 2026-09-18: **Stage 1 IN STUDY / NOT YET PASSED**. D003 already establishes reader/writer/schema compatibility as relational and split-publication migration hazards; D006 establishes cursor/effect atomicity and idempotency/conflict boundaries. These are consumed as implementation dependencies, not promoted into PWA/product PASS.

## 18. MINTTAP DIRECTION

For a PWA/EFB-like product, version the meanings that can evolve rather than relying on one schema integer. Preserve original offline operation/provenance, migrate into a candidate current representation, re-check current authorization/base revision/domain invariants, and quarantine/recover when semantic equivalence is not demonstrable.

Do not choose a concrete migration framework, schema registry, event-sourcing model or compatibility horizon until actual LogMate/MintTap data contracts and consequence requirements are known.

## 19. OPEN / VALIDATION / CHANGE WATCH

**OPEN:** actual local DB/schema; operation envelope; API generations; validation/authorization epochs; conflict-policy evolution; compatibility horizon; rejected-operation retention; backend; actual migrations; managed-iPad lifecycle; safety/legal retention requirements.

**VALIDATION:** real IndexedDB upgrade/restart; old/new tab and worker mixtures; Safari/iPadOS; physical iPad termination; actual backend old-operation admission; rollback; unknown-field preservation; user recovery accessibility; actual mobile/native counterpart.

**CHANGE WATCH:** IndexedDB/WebKit behavior; Service Worker lifecycle/platform policy; chosen serialization/backend compatibility; supported browser/iPadOS generations; product schema/API contracts.

## 20. Persistent guards

`syntactic migration ≠ semantic re-authorization`.  
`schema structurally current ≠ record semantically current`.  
`parseable ≠ lossless ≠ same domain meaning`.  
`backward-readable ≠ backward-writable`.  
`new worker active ≠ every client/data schema migrated`.  
`skipWaiting + claim ≠ atomic application migration`.  
`operation translated ≠ operation valid against current base`.  
`migration function success ≠ semantic equivalence proven`.  
`default inserted ≠ user chose default`.  
`valid under old policy ≠ valid under current policy`.  
`historical record grandfathered ≠ obsolete mutation authority grandfathered`.  
`old conflict policy recorded ≠ old conflict policy remains executable`.  
`opaque preserved ≠ opaque trusted`.  
`version marker advanced ≠ every semantic migration completed`.  
`database opens cleanly ≠ semantic migration PASS`.  
`operation rejected ≠ user data should be silently deleted`.  
`old data recoverable ≠ old writer supported`.  
`compatibility retired ≠ historical evidence deleted`.

## Gate

**PASS (generic).** The Web Manager can now distinguish storage/domain/operation/policy/API/worker versions, reason about directional compatibility, preserve original intent through migration, prevent schema upgrades from manufacturing current authority, define rejected-operation recovery and hand executable migration/sync mechanics to Software Engineering.

## Next high-value adjacent work

**PWA reconciliation auditability & user-correction provenance:** once old/new operations can be classified, determine how automated migration, conflict resolution and later user correction should preserve an explainable chain from original local intent to authoritative current state without turning every record into heavyweight event sourcing. Cover correction vs mutation, provenance compaction, privacy/minimization, audit retention, and user-visible explanation boundaries.