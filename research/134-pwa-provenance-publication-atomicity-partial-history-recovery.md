# 134 — PWA Provenance Publication Atomicity & Partial-History Recovery

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 131–133 reconciliation/provenance; Track A IndexedDB transaction mechanics; Track B truthful partial-history UX; Track C crash/recovery oracles; Software Engineering Data D005/D006 bounded transaction/cursor evidence.

## Purpose

133 established that authoritative state and provenance are distinct. The adjacent failure is publication split-brain: business state commits while provenance/receipt does not, provenance appears to commit while business state did not, or an acknowledgement is lost after a valid commit.

Central rule:

> **A system must define the atomic acceptance unit for authoritative effect, provenance and progress/receipt claims; when they cannot share one transaction, it must preserve a durable recoverable intermediate rather than infer missing history from the current projection.**

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** IndexedDB provides atomicity only inside a transaction/database scope; worker/page lifecycle does not make cross-system publication atomic.
- **B UX/IA/Content — elevated consumer:** owns truthful `saved locally / accepted remotely / history incomplete / repair required` explanation.
- **C Quality — high dependency pressure:** owns crash-point, duplicate, truncation, rebuild and false-success oracles.
- **D Search/Analytics — constrained consumer:** telemetry can observe failures but is neither commit record nor provenance authority.
- **E Architecture/Security/Operations — highest-risk owner:** owns acceptance boundaries, durable publication, repair authority, integrity and incident interpretation.

Allocation remains E-heavy; A/C are prerequisite-critical because publication claims cannot exceed the transaction and durability primitives actually provided.

## 2. SOURCE — transaction atomicity has a defined scope

IndexedDB 3.0 requires a transaction commit to atomically write the changes made by requests in that transaction; abort rolls back changes. If a transaction cannot finish because the implementation crashes, it is aborted. This is a useful browser-local atomicity primitive, not a cross-origin/server transaction.

Source checked 2026-09-18:
- https://www.w3.org/TR/IndexedDB-3/

SQLite documents atomic commit/recovery using rollback journals; a hot journal can be replayed after interruption to restore a sane database state. This demonstrates that crash recovery depends on the storage engine's explicit commit/recovery protocol, not application optimism.

Source checked 2026-09-18:
- https://sqlite.org/atomiccommit.html

PostgreSQL 18 documents durability as preserving committed transactions through crashes/power loss, and notes that non-durable settings such as disabling synchronous commit change what a reported completion guarantees.

Source checked 2026-09-18:
- https://www.postgresql.org/docs/18/non-durability.html

**SYNTHESIS:** transaction atomicity is scoped. `business row + provenance row` can be atomic when the chosen store/transaction actually encloses both. `browser IndexedDB + remote API`, `database + analytics`, or two independent services are not made atomic by sequential `await` calls.

Guards:
- `two writes in one function ≠ one atomic commit`;
- `transactional locally ≠ transactional across browser/server`;
- `success callback observed ≠ every downstream publication durable`;
- `projection durable ≠ provenance durable`.

## 3. Define the acceptance unit before choosing publication order

For each consequence-bearing operation, define which facts must become durable together. A generic server-side acceptance unit may include:
1. logical operation identity;
2. base/current revision precondition outcome;
3. authoritative business effect or tombstone;
4. resulting authoritative revision;
5. minimal provenance/decision envelope;
6. deduplication/receipt state needed to make ambiguous retry safe;
7. replication progress/cursor only if all semantic effects through that progress point are durable.

Not every telemetry/log message belongs in this atomic unit. Analytics, notifications and derived search indexes can often follow asynchronously if their lag/failure cannot falsely change business authority.

Guard: `same request ≠ same atomicity requirement`.

## 4. The dangerous split-publication states

### A. Projection committed, provenance missing
Current state is real, but the system cannot safely invent who/what/policy produced it. If provenance is required for correction/reconciliation/security consequence, mark history incomplete and repair from independent durable evidence where possible.

### B. Provenance committed, projection missing
A provenance entry must not claim `applied` merely because an attempt began. It can record `received/attempted` if that is the fact actually committed. An `applied` claim without the corresponding effect is a false history.

### C. Projection + provenance committed, ACK lost
This is an ambiguous acknowledgement, not an ambiguous server effect if durable operation identity/receipt can prove the prior result. Retry should return/reconstruct the same logical outcome rather than apply again.

### D. Effect committed, progress cursor advanced separately
A cursor that outruns durable semantic effects can make replay skip missing work. Software Engineering Data D006 has bounded executable evidence for this exact invariant; Web Manager consumes it rather than duplicating implementation ownership.

Guards:
- `history missing ≠ effect absent`;
- `provenance entry exists ≠ business effect committed`;
- `ACK missing ≠ commit missing`;
- `cursor advanced ≠ every semantic effect safely published`.

## 5. Preferred publication hierarchy

Where consequence justifies it:

**Preferred:** put authoritative effect + minimal provenance + operation receipt/dedup state in one durable transaction owned by one authoritative store.

**If derived publication must leave that transaction:** commit a durable outbox/publication-intent record in the same transaction, then publish asynchronously and mark delivery separately. The durable intent is not proof that the downstream consumer applied it.

**If atomic co-location is impossible:** use explicit state transitions and repairable identities. Never collapse `prepared`, `accepted`, `applied`, `published`, `acknowledged` into one boolean `synced`.

This is an architecture direction, not a selection of a particular database/message broker.

Guards:
- `outbox committed ≠ downstream applied`;
- `downstream applied ≠ client received ACK`;
- `retry delivered ≠ duplicate effect permitted`;
- `eventually consistent ≠ unobservable intermediate states acceptable`.

## 6. Projection rebuild and provenance rebuild are asymmetric

A full trustworthy provenance/event history may be able to rebuild a projection if semantics, ordering and interpreters are retained and that was an explicit design goal. A current projection usually cannot reconstruct lost provenance: it does not reveal rejected branches, original intent, transformer/policy version or correction actor.

Therefore:
- rebuild current projection from history only when replay semantics are intentionally supported and tested;
- do not synthesize missing provenance from `updatedAt`, current value or analytics;
- preserve `UNKNOWN/INCOMPLETE` when evidence cannot establish a claim;
- a recovery statement created later must identify itself as recovery, not masquerade as original provenance.

Guards:
- `current projection ≠ invertible history`;
- `projection rebuildable from history ≠ history rebuildable from projection`;
- `repair created provenance ≠ original provenance recovered`;
- `unknown actor/policy ≠ infer most likely actor/policy`.

## 7. Partial-history recovery states

Use explicit assurance states rather than silently filling gaps:
- **COMPLETE-VERIFIED** — required effect/provenance continuity is present and verified at selected assurance level;
- **EFFECT-VERIFIED / HISTORY-INCOMPLETE** — authoritative effect is established, but required lineage is missing;
- **HISTORY-CLAIM / EFFECT-UNVERIFIED** — history says an effect occurred but authoritative effect cannot be established;
- **REPAIR-PENDING** — independent durable evidence can likely close the gap;
- **REPAIRED-WITH-PROVENANCE** — recovery action and evidence are themselves recorded;
- **UNVERIFIABLE** — evidence is insufficient; do not manufacture continuity.

`UNVERIFIABLE` is not synonymous with `INVALID`, but neither is a PASS.

## 8. Repair authority and evidence order

Potential repair inputs, depending on architecture, include authoritative transaction/WAL state, durable operation receipts, independent protected provenance sink, retained client operation identity/payload, backup snapshot plus post-snapshot durable log, or signed/verified recovery evidence from prior studies 122–126.

Repair must preserve:
- what survived;
- what was missing;
- which evidence was used;
- which actor/tool performed repair;
- repair time/version;
- whether exact history was recovered or only a new corrective assertion was created.

Do not use analytics delivery as proof of business commit. Do not use client clock as authoritative global order. Do not re-sign guessed history and call it recovered.

## 9. PWA/EFB boundary

For a long-offline company iPad, at least three publication domains may exist:
1. browser-local IndexedDB transaction;
2. remote authoritative API/database transaction;
3. later replication/receipt/provenance publication.

A local transaction can atomically store an offline operation and its local lineage if they share its IndexedDB transaction. It cannot atomically commit the future remote server effect. Reconnect therefore requires durable logical operation identity and explicit remote acceptance state.

Service Worker termination/restart must not be treated as a continuously running transaction coordinator. Network return must not change `queued` directly to `synced` without authoritative receipt/reconciliation evidence.

Guards:
- `local transaction committed ≠ remote transaction committed`;
- `Service Worker handled fetch ≠ remote business effect durable`;
- `queue item removed ≠ authoritative receipt preserved`;
- `browser local history survives now ≠ durable independent audit archive`.

## 10. User-visible recovery boundary

Track B should expose consequence, not internal storage jargon. Examples of truthful states include:
- saved on this device;
- waiting to send;
- received by server, final reconciliation pending;
- accepted and current;
- current value preserved, but change history is incomplete;
- conflict/history repair requires review.

Do not show `Synced` merely because an HTTP request returned, an analytics event fired, or a queue became empty. A repair UI must distinguish a recovered historical fact from a new user correction.

Design Studio W085 supplies useful runtime reasoning about causal Undo/focus identity, but persistence/offline/Sync, Safari/Firefox, screen reader and physical-device evidence remain OPEN; no PWA UX PASS transfers.

## 11. Privacy/minimization boundary

Atomic provenance does not require copying every business payload into an audit row. The atomic unit should contain the minimum lineage required for consequence and repair. Large/sensitive recovery objects may use separately governed references where exact reconstruction is justified. Retention/erasure rules from 133 remain applicable.

Guard: `atomic provenance required ≠ duplicate full sensitive payload per revision`.

## 12. Track C validation campaign

1. crash before authoritative transaction commit → neither effect nor `applied` provenance survives;
2. crash after effect/provenance transaction commit before ACK → retry yields one logical effect;
3. duplicate retry with same operation ID/same payload → same result;
4. same operation ID/different payload → reject/quarantine;
5. effect and provenance deliberately split → oracle detects mismatch;
6. provenance `applied` written before effect → test rejects false history;
7. durable outbox committed, publisher crashes → restart republishes without duplicate business effect;
8. downstream publish succeeds, outbox ACK/update crashes → duplicate delivery remains idempotent downstream;
9. analytics succeeds while business transaction aborts → analytics cannot certify commit;
10. business commits while analytics fails → business authority remains valid;
11. cursor/progress crash before semantic effects → no advancement;
12. crash after semantic effects before cursor → replay safe/idempotent;
13. cursor advanced ahead of effect → semantic oracle detects gap;
14. projection survives, required provenance row deleted → HISTORY-INCOMPLETE;
15. provenance survives, projection corrupt/missing → effect is not inferred blindly;
16. rebuild projection from intentionally replayable history → compare semantic invariant;
17. attempt to rebuild history from projection only → remains incomplete where information lost;
18. repair from protected receipt/WAL evidence records repair provenance;
19. repair from untrusted client-only claim → consequence-appropriate review/quarantine;
20. compaction removes detail → UI/API does not claim full reconstruction;
21. backup restore plus post-backup log → verify no duplicate/missing operation IDs;
22. local IndexedDB transaction stores operation+local lineage atomically;
23. browser termination before local transaction finishes → no false local `saved` state;
24. browser termination after local commit before UI confirmation → reopen discovers durable local state;
25. remote commit after local send, worker termination before local ACK update → retry reconciles same operation;
26. queue deletion before durable remote receipt → destructive test must expose loss;
27. stale worker uses old provenance envelope → preserve original and migrate/reject explicitly;
28. privacy retention removes payload but keeps justified minimal lineage → no false recoverability claim;
29. accessible repair/correction flow preserves semantic focus/causal ownership after state transition;
30. physical Safari/iPadOS process termination, eviction and reconnect → remains required before product PASS.

## 13. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-18: **W085 CAUSAL-UNDO SERVED-RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen reader, physical device, field-CWV and human UX remain OPEN.

Software Engineering Studio Data checked 2026-09-18: **Stage 1 IN STUDY / NOT YET PASSED**. D005 supplies bounded SQLite crash/capacity evidence; D006 supplies server-commit-before-ACK and cursor/effect atomicity evidence, including an exact-ref LogMate pre-implementation invariant. Real mobile/backend/Flutter/device durability remains OPEN.

## 14. MINTTAP DIRECTION

For PWA/EFB-like products, define the authoritative acceptance unit before implementation. Prefer one durable transaction for business effect + minimal material provenance + operation receipt/dedup state when one authoritative store can own them. Use durable publication intent for asynchronous derivatives rather than pretending sequential writes are atomic. Preserve explicit incomplete-history states and repair provenance; never reconstruct lost authorship/policy/ordering from the current projection by guesswork.

No production architecture, database, event bus or LogMate implementation is inferred here.

## 15. OPEN / DEPENDENCY / CHANGE WATCH

**OPEN:** actual MintTap/LogMate authoritative store, provenance schema, transaction scope, outbox/event mechanism, operation receipt, cursor semantics, retention, repair authority, local IndexedDB design, backend durability and managed-iPad behavior.

**DEPENDENCY:** Software Engineering must own implementation-level transaction/outbox/idempotency design and executable crash testing once the actual stack exists. Track B/Design Studio own concrete recovery UI; Track C owns cross-browser/device destructive validation.

**CHANGE WATCH:** IndexedDB implementation/device durability and WebKit lifecycle/storage behavior require current runtime evidence. Database durability depends on actual engine/configuration/storage stack; generic documentation is not product proof.

## 16. Gate

**PASS (generic).** The Web Manager can distinguish transaction atomicity from multi-system publication, define an acceptance unit, diagnose projection/provenance split-brain, separate ACK ambiguity from commit ambiguity, design bounded partial-history recovery states, and apply these boundaries to offline PWA/EFB flows without inventing product facts.

Product, managed-iPad, data-model, backend and destructive-runtime validation remain OPEN.

## 17. Next highest-value adjacent work

**PWA provenance integrity under compaction/export/import and cross-device transfer**: determine how bounded lineage remains attributable and non-misleading when history is compacted, exported for backup/device migration, imported into a new trust context, or merged with another device's lineage; separate chain continuity from content availability and current authorization.