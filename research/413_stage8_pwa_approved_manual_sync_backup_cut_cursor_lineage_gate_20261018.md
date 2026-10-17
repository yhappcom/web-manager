# 413 — Stage 8 PWA Manual Delta Sync: Approved-Contract Cut Consistency, Backup Lineage and Cursor Admission

**Checkpoint:** 2026-10-18 Asia/Seoul. **Canonical Web Manager intake:** `yhappcom/web-manager/main@1f86961ddf74623534d9ee29df64ca5ef9b91cba`. **Read-only LogMate intake:** `yhappcom/logmate/main@0233d4f9ea0ff43820e3ed6297a837e3e07e0634` (2026-10-17 14:25 UTC). **Owner:** Track E, with A browser/storage mechanics and C validation. **Gate:** source/contract integration + independent deterministic model **36/36 PASS**; **product, backend, browser, physical/managed-iPad, .lbk implementation and deployment OPEN**. This is not production Sync approval.

## 1. MATERIAL CHANGE / CONTRADICTION

The 2026-10-17 LogMate product authority has **approved** `docs/specs/local-first-manual-delta-sync-contract.md` (contract only, implementation NOT IMPLEMENTED), subsequently aligned MASTER and the unified review, and superseded old E-1/E-2A/E-2C blanket anti-LWW/server-canonical-current-state directions **for internal Sync Delta only**. Prior Web Manager working notes 411–412 that called UTC LWW/Manual Sync a *proposal* or the tie/delete policy *unapproved* are **stale as product-authority descriptions**; their bounded protocol counterexamples remain useful. Do not silently change the approved trade-off, or infer deployment from documentation commits.

**Approved:** complete local ledger per independent DB; user-triggered Push/Pull/Apply; one authenticated startup **metadata-only** read (no automatic Delta/lastSyncAt); whole-Record LWW by originating user's `modifiedAtUtc`, tie by normalized UTF-8 Operation ID; immutable Operation ID/digest/receipt; server sequence for delivery/cursor **not** record winner; separate structure/config operations and protected user-confirmed baseline/page/order; .lbk full-ledger bootstrap, new Replica ID; future optional P2P preserving original Op ID; no unverified history/receipt/tombstone GC. **Explicit owner trade-off:** no correction for cross-device clock skew. **Unimplemented:** wire/codec, Firebase admission, full .lbk, migration, production Sync, browser/iPad/P2P proof.

Primary product: https://github.com/yhappcom/logmate/blob/0233d4f9ea0ff43820e3ed6297a837e3e07e0634/docs/specs/local-first-manual-delta-sync-contract.md ; authority reconciliation: https://github.com/yhappcom/logmate/commit/0233d4f9ea0ff43820e3ed6297a837e3e07e0634 .

## 2. HISTORY → PRINCIPLE → STANDARD → PLATFORM LIMIT

Offline replicas can commit a user's change while a server is unreachable. A portable backup must capture not only the visible record but also the identity and delivery obligation of any **unsent operation**. A server acknowledgement cannot be inferred from a local save; a downloaded Delta cannot be inferred applied from its receipt. Therefore three cuts are separate:

1. **Local command cut:** Record + revision/history + pending Outbox + affected projection/aggregate commit as one local logical transaction.
2. **Backup cut:** ledger, outbox, applied IDs, owner, schema/format, structural state and **contiguous applied cursor/epoch** represent one consistent source-DB snapshot; subsequent archive write/verification is another failure boundary.
3. **Remote apply cut:** current Record + losing revision/history + applied Operation IDs + projections/aggregates + **contiguous cursor** commit atomically; no cursor-only advancement.

**SOURCE** (reviewed 2026-10-18):
- W3C IndexedDB 3.0: https://www.w3.org/TR/IndexedDB/ — a transaction atomically writes its scoped changes or aborts; `durability` is a hint, and atomicity does **not** span browser DB, external .lbk file, Firebase and native DB.
- MDN IndexedDB use: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB — interruption and independent transactions can leave partial application states; do not write backup finality on page unload.
- WHATWG Storage: https://storage.spec.whatwg.org/ and WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/ — quota/eviction and installed contexts are not independent backup or guaranteed durable storage.
- Firebase Firestore contention: https://firebase.google.com/docs/firestore/transaction-data-contention — server transaction retry/serializability within Firestore does not create an atomic cross-device transaction.
- Firebase Rules: https://firebase.google.com/docs/firestore/security/rules-structure — privileged server client libraries bypass Firestore Security Rules; IAM and explicit UID admission are separate.
- Web Manager canonical 396: https://github.com/yhappcom/web-manager/blob/main/research/396_stage8_pwa_origin_message_authority_data_custody_gate.md — Service Worker control, origin storage and owner-data custody are separate; do not confuse fetch bypass with origin isolation.

**Platform distinction:** IndexedDB transaction semantics are a Web standard. Actual `strict` durability, quota/eviction, installation/storage partition and process lifetime require Chromium and Safari/WebKit version-specific execution. An iPad MDM Web Clip is an OS/management-policy context, not merely a Chromium PWA with a different icon. Service Worker Cache Storage does not become an authoritative backup of Sembast/IndexedDB. Native Sembast, Flutter Web Sembast and external .lbk serialization require independent Engineering verification.

## 3. SYNTHESIS — FAILURE MODES AND SAFE ORACLES

| Failure or adversarial order | Unsafe shortcut | Required verdict / preservation |
| --- | --- | --- |
| Local edit commits between separately reading ledger and Outbox during export | Backup shows new Flight but omits its unsent Op, or old Flight with new Op | **Torn backup invalid**; use one source-DB consistent cut or equivalent verified snapshot protocol |
| Crash after writing .lbk partial bytes | Existence of file = backup complete | Temporary artifact + integrity/manifest verification + explicit finalization; partial archive not a successful backup |
| Backup restored into empty DB with cursor 7, unsent Op A | Copy cursor and assume Op A server-confirmed | New Replica ID; preserve original Op A/digest; check receipt/retry under authenticated Owner; cursor remains proof-bound |
| Backup imported into nonempty DB with local unsent changes | Replace target | REVIEW_REQUIRED; preserve both, never erase unique local changes |
| Server Delta seq 8 downloaded, local Apply fails | Cursor becomes 8 | Cursor remains 7; replay same Op safely |
| Seq 8 and 10 durably handled, seq 9 missing | Cursor becomes max(8,10)=10 | Cursor is **8** until 9 is durably handled; downloaded/received/receipt != applied |
| Same Operation ID/digest retransmitted after lost ACK | Mint new Op or new seq | Return original receipt/seq; differing digest rejected; Owner scope checked |
| Original 10:05 edit accepted seq 101, 10:00 edit seq 102 | Choose later server sequence | 10:05 wins per approved UTC LWW; loser retained, no clock-skew correction |
| Equal UTC distinct Ops | Choose arbitrary arrival | Normalized UTF-8 Operation ID lexical max; retain loser |
| Old .lbk or Delta replay arrives after later tombstone | Re-stamp replay with current time | Preserve original modifiedAtUtc; old snapshot cannot impersonate new user edit |
| Same owner/date/full airline flight ID but conflicting sector | Silently merge/delete or double-count | Preserve both identities, REVIEW_REQUIRED; alias mapping/representative choice requires exact deterministic engineering contract |
| Safari/PWA storage evicted with unique unsent Op and no external backup | Recover by server latestSequence alone | **UNRECOVERABLE from server-only history** for never-uploaded bytes; no synthetic success |
| App startup latestSequence check | Update lastSyncAt, advance cursor, apply Delta | Metadata-only; stale/unknown remote status shown without changing local state |
| Schema/Custom Definition unknown during Pull | Skip Op and advance cursor | DEFERRED/REVIEW_REQUIRED, preserve payload and cursor gap |
| Backup hash matches but UID does not | Accept as same owner | Reject Owner mismatch; integrity digest != authentication/authorization |

**Key derived invariant:** `local_saved != exported != uploaded != server_receipted != locally_applied != converged`. Success UI must refer to a particular boundary. `lastSyncAt` is not a startup-read timestamp. **A file-only bootstrap cannot be replaced by server Delta if some local operations never reached the server.**

## 4. VALIDATION — INDEPENDENT DETERMINISTIC MODEL, NOT PRODUCT

Executed 2026-10-18 in Python **3.13.5**, single-process, synthetic fixtures: **36/36 assertions PASS**. A read-order schedule enumerator considered **24** combinations (six ledger/outbox/cursor read orders × four commit positions); **8/24** yielded a torn mixed snapshot when the read was not atomic. Both before/after atomic cuts preserved ledger↔Outbox coherence. Other tests covered cursor/apply crash cut, gaps 8/10, dedup receipt and digest collision, restored Replica ID, LWW sequence inversion and equal timestamp, startup read-only, UID/schema/corrupt/dirty-target restore refusal, sector identity review and irreversible never-uploaded data loss.

**This is a constructed counterexample set, not an empirical failure probability.** No real LogMate .lbk writer, Sembast transaction, IndexedDB, Firebase Function, Flutter UI, browser or managed iPad was executed. Tests establish only that the stated oracles distinguish modeled good/bad states; no 36/36 product PASS or 8/24 incidence claim.

### Implementation-level falsification packet (Engineering handoff)

**G0 source/authority:** pin LogMate SHA, approved Sync contract, current codec/DB schema, build/toolchain; reject old archived E-2A as current product policy.

**G1 local cut:** create offline Flight + revision + Outbox + projections; inject failure before/after transaction commit and export at each cut. Reopen source DB and independently parse .lbk. Oracle: every exported current value has its pending/handled provenance and correct cursor, no partial committed state.

**G2 archive/restore:** corrupt/truncate/rename file; wrong UID; unsupported schema; dirty target; pending Op; duplicated import; interrupted restore. Oracle: no loss of preexisting local unique records; new Replica ID, original Op ID, verifiable lineage; no cursor inflation.

**G3 server receipt:** owner A/B isolation, same Op/digest retry, same Op/different digest reject, ACK timeout and duplicate receipt; privileged server authorization vs Firestore direct-client deny-all. Oracle: exactly one admitted logical operation and stable sequence/receipt, no false local success.

**G4 Pull/Apply:** missing seq 9, duplicate 8, unsupported structure, projection crash, commit before/after cursor; restart. Oracle: contiguous cursor and durable ledger/history/projections are one transaction; replay idempotent.

**G5 conflict:** reversed arrival vs UTC winner; tie; DELETE/UPDATE/RESTORE; old backup; independent CREATE alias/sector mismatch; protected baseline/order. Oracle: approved LWW and narrow review/deferred without silent data loss.

**G6 web/device:** exact normal PWA on disposable HTTPS, Chromium + Safari tab + Home Screen + actual managed Web Clip separately; offline cold start, storage pressure/eviction, update/migration, export/import and network reconnect; preserve owner-bound unsent records. **No cross-platform or fleet promotion without execution.**

**G7 user task / privacy:** locally saved, pending, unknown ACK, remotely admitted, locally applied, review required, backup verified must have distinct truthful visible/accessible semantics. Do not log real UID, flight payload, file contents or auth codes. Marketing/install/offline/sync claims remain evidence-bounded.

## 5. FIVE-TRACK BALANCE / TRANSFER

| Track | Gate, pressure and allocation | One-owner transfer |
| --- | --- | --- |
| **E Security/Operations** | **Primary bottleneck / largest allocation**: backup cut, Owner admission, immutable receipt, retention, cost, rollback and loss containment; source/model mature, runtime OPEN | Owns the cross-system custody/release acceptance contract |
| **A Platform/Browser** | Critical prerequisite: IndexedDB transaction, WebKit storage partition, SW vs ledger, secure origin and interrupted lifetime; standards mature, iPad execution OPEN | Supplies browser mechanics to E/C, no second primer |
| **C Quality/Accessibility** | High execution debt: independent negative oracles, exact artifact, crash/restart, Safari/Chromium/iPad, AT; model PASS, product OPEN | Executes the same G0–G7 evidence packet |
| **B UX/IA** | State-truth and recovery dependency: local saved vs ACK vs backup verified; consume Design Studio W120/W121, Stage 3 NOT PASSED | No invented visual system; task-state semantics only |
| **D Discovery/Analytics** | Privacy/claim pressure: no analytics containing flight/UID, no automatic background sync claims, measure bounded Sync costs | Marketing owns acquisition; D owns web measurement/claim provenance |

**Design Studio:** W120/W121 call for exact executable, failure-injection and semantic/accessibility evidence rather than additional pre-runtime manifest files (https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md). **Software Engineering:** D006 demonstrates retry ≠ idempotency and whole-record LWW convergence can discard independent concurrent field edits; that is an **accepted trade-off** under the 2026-10-17 LogMate product policy, not license to replace LWW with fieldwise merge (https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md). **Marketing:** recent Marketing Manager commits focus on MintTap investor/ROC evidence, not a product PWA implementation gate; avoid importing unsupported claims.

## 6. MINTTAP DECISION / OPEN / CHANGE WATCH

**MINTTAP DECISION — preserve approved product authority:** use UTC LWW and Manual Delta exactly as approved; do not resurrect historical causal HOLD or silently change clock policy. **Engineering recommendation, not approved implementation:** require a consistent source-DB backup cut and independently verified finalized .lbk, preserve unsent IDs, and fail closed on cursor/lineage gaps. Do not equate digest with UID authority or a storage persistence grant with backup.

**OPEN:** actual .lbk snapshot protocol/manifest signing or encryption policy, cursor/epoch proof format, restore conflict implementation, operation ID canonical encoding, representative alias selection, Firestore transaction contention/cost, server admission/rate limits, GC/retention economics, current-main normal PWA build, Safari/WebKit/Home Screen/managed-iPad physical tests, accessibility/human verification and native↔PWA end-to-end Sync.

**CHANGE WATCH:** W3C IndexedDB durability hints/browser implementations; WebKit quota/eviction/installed partition and iPadOS MDM; Firebase Functions/Firestore transaction retry/Rules and costs; Flutter/Sembast storage behavior. Recheck actual versions before product acceptance.

**Adjacent-work checkpoint:** source authority reconciliation, backup consistency, server receipt, contiguous cursor, restore identity, clock/alias trade-offs, security/UX/measurement transfer and negative tests are integrated. More synthetic cases alone cannot promote implementation. Next major boundary is Engineering-owned actual .lbk and authenticated Firebase Emulator + disposable HTTPS/iPad evidence. **Stage 8 remains open for production; PWA release HOLD.**
