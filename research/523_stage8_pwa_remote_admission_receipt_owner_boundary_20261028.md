# 523 — Stage 8 PWA Remote Admission, Receipt Ambiguity and Owner-Fence Boundary

**Date reviewed:** 2026-10-28 KST. **Owner:** E — Web Architecture, Security & Operations. A owns HTTP/browser request mechanics, C owns independent runtime oracles, B consumes truthful recovery-state requirements, D consumes claims/measurement boundaries. Web Manager coordinates. **State:** SOURCE + SYNTHESIS + executable HTTP model + exact hosted synthetic CI **18/18 PASS**; product/Firebase/managed-EFB VALIDATION OPEN. **Product/Firebase/managed-EFB VALIDATION OPEN.**

## 1. Why this domain now [HISTORY / DEPENDENCY]
[521 §§14–17](521_stage8_pwa_sembast_cross_tab_replay_wasm_web_opener_admission_20261027.md) actually executed independent Chrome tabs (9/9 deterministic and conditional TB03 observed) and showed Sembast transaction callback replay, local owner-epoch fence and restart behavior. Its in-browser owner flag was test-writable, so **not authenticated remote authority**. The next bottleneck is the separation between (a) a locally committed outbox operation, (b) a server-side authenticated admission, (c) a durable server receipt, (d) a response reaching the client, and (e) the client atomically applying pulled deltas. Repeating local tab tests will not cross that boundary.

**Product authority:** [LogMate approved Manual Delta Sync contract, 2026-10-17](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md). It approves local-first manual push/pull, immutable original Operation ID/digest, current UID Owner checks, serverSequence for delivery (not LWW), UTC modifiedAtUtc winner, lost-ACK UNKNOWN retry, no clock correction, delete tombstones, recoverable losing history and startup latest-only read. **Production Manual Sync is NOT IMPLEMENTED**; F1 local persistence is narrower. Do not change the approved product policy in a Web Manager research fixture.

## 2. Primary sources and standards [SOURCE / CHANGE WATCH]
- [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2): an HTTP POST is not automatically idempotent merely because a caller retries. An application-specific stable operation identity and server receipt are necessary to safely reconcile an unknown result.
- [Firebase Firestore transactions](https://firebase.google.com/docs/firestore/manage-data/transactions): transactions are atomic; contention can re-execute the transaction function. No external side effect or client-visible ACK should be issued from a replayable callback. Offline transaction limitations are distinct from LogMate local-first edits.
- [Firestore server client libraries](https://firebase.google.com/docs/firestore/client/libraries): privileged server libraries **bypass Firestore Security Rules** and rely on IAM. A client-side deny-all rule is not an authorization check for Admin SDK code. Server endpoints must verify the authenticated principal and current ledger Owner/stream authority before material operations.
- [Firebase App Check enforcement](https://firebase.google.com/docs/app-check/enable-enforcement): app attestation is not a UID Owner grant or immutable operation dedup. Limited-use token replay protection is a distinct, capability- and endpoint-specific control; it cannot replace receipts. Recheck provider/product support before release.
- [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/): local commit and storage durability do not prove remote acceptance or independent backup. [Chrome relaxed IndexedDB durability](https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed/) is another separate failure class.
- [521](521_stage8_pwa_sembast_cross_tab_replay_wasm_web_opener_admission_20261027.md), [522](522_stage8_offline_utc_lww_clock_trust_and_recovery_admission_20261027.md) and [298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md) own the local replay, UTC identity and restored-binding provenance evidence respectively.

## 3. Security model [SYNTHESIS / CONTRADICTION]
The request's owner field, generation, replica ID, original modifiedAtUtc, operation ID and digest are **untrusted data** until an authenticated server checks their meaning against current authority. A client-reported generation is only a stale-client hint; it is **not proof of a current grant**. A same-ID/same-digest receipt can describe a historically accepted operation, but **must not become a new authorization grant after deletion/revocation/Owner transfer**. A server should decide explicitly whether a previously accepted receipt may be disclosed to a revoked caller; this fixture takes the conservative deny-before-replay path.

**Critical independent layers:**
1. Transport request and authenticated subject (Firebase ID token verification in the real product; synthetic token lookup in the lab).
2. Current UID Owner, stream status and authority generation, checked at material admission and reads.
3. Immutable original operation ID/digest and per-Owner receipt/sequence within a transactional uniqueness boundary.
4. Record winner comparison by **original** UTC microseconds, not server arrival sequence. Preserve losing revisions and tombstones.
5. Client response/ACK receipt; response loss creates **UNKNOWN**, not proof of noncommit.
6. Local Pull/Apply and contiguous applied cursor; only actual successful Manual Sync may update lastSyncAt.
7. Independent LBK export/restore and managed iPad data custody, not inferred from any server response.

**Potential defect found during synthetic design:** a globally keyed operation receipt that checks digest but fails to bind the **original receipt Owner** can return a prior Owner's receipt after ownership changes. The fixture explicitly rejects this in RA09. This is a *model design counterexample*, **not** an observed LogMate/Firebase vulnerability. The production data key/tenant scope is OPEN.

## 4. Executable network diagnostic [VALIDATION]
[Research-only Node HTTP probe](handoffs/pwa_remote_receipt_probe.mjs) uses Node's real loopback HTTP request/response and socket termination. The server is **in-memory**, with an explicitly **fake token-to-UID lookup**, synchronous event-loop admission, synthetic Owner/generation transitions, fixed 32-digit lowercase hex operation IDs and fixed-width microsecond UTC. There is **no Firebase Auth JWT verification, App Check, Firestore transaction, durable server restart, real digest recomputation, real LogMate wire codec or real EFB network**. A local successful test is evidence for the *model only*.

| Cases | Independent oracle |
| --- | --- |
| RA01–RA02 | Missing subject or forged owner hint cannot create a server operation |
| RA03–RA04 | Same immutable ID/digest returns original receipt; changed digest rejects |
| RA05 | Server commits in memory then drops TCP response; client sees UNKNOWN and same-ID retry returns original receipt with no new sequence |
| RA06–RA09 | Revoked/current Owner and generation checks, cross-UID denial and previous-Owner receipt isolation |
| RA10–RA13 | Arrival sequence not LWW; approved future-clock dominance; tombstone/older update; explicit later RESTORE with original timestamps |
| RA14–RA15 | Startup latest-only is nonmutating; revoked cached subject cannot read latest/delta |
| RA16–RA17 | Twelve concurrent same-ID HTTP requests converge to one acceptance; different digest conflicts |
| RA18 | Malformed ID/time and an exposed owner-change route fail closed |

**Local development observation:** a longer exploratory 21-case Node 22.16.0 loopback model passed 21/21 on 2026-10-28, but that separate exploratory source was not persisted; **do not promote that count to committed-source CI evidence**. This committed 18-case probe requires its **own exact-ref CI** before any PASS claim. The hosted workflow pins Node 22 and runs only the public fixture; no secrets or Firebase calls.

**Limits:** synchronous in-memory mutation makes concurrent HTTP requests serialize in one process; it does **not** reproduce Firestore multi-instance races or persistence across server crash. Socket destruction proves only the client response can be lost after the in-memory effect. The fixture compares fixed-width ASCII and UTC strings; the production normalized UTF-8 ID comparator, canonical digest and date codec remain Engineering tests. No server history compaction or cross-replica applied cursor is implemented in the fixture.

### Exact hosted execution [VALIDATION — SYNTHETIC ONLY]

[GitHub Actions run 40599506021](https://github.com/yhappcom/web-manager/actions/runs/40599506021), job `122523810262`, exact checkout `012799eb572030b4f16f68c9bd8bcf5a68f95de4`, completed **SUCCESS** on 2026-10-27 23:04 UTC (2026-10-28 08:04 KST). GitHub-hosted Ubuntu 24.04, Node **v22.23.3**, `node --check` PASS, `node --test` **18/18 PASS, 0 FAIL**. Actual job log includes RA01–RA18 and the exact checkout SHA. The prior local exploratory 21-case model is not the committed oracle; the hosted 18-case file is.

**Evidence boundary:** The model intentionally destroys an HTTP socket after an **in-memory** admission. It demonstrates a real network response-loss ambiguity and same-ID reconciliation **within that one Node process**, not a Firestore durable receipt, multi-instance atomicity, Firebase Auth verification, App Check, IAM, production LogMate Manual Sync, Safari or managed EFB. In-memory synchronous request handlers do not prove server transaction retry or crash recovery. No product release gate advances.

## 5. Cross-track transfer [DEPENDENCY / TRANSFER VALIDATION]
- **E (primary bottleneck):** current server-side Owner/UID, receipt scoping, deletion/revocation, replay-safe admission, privileged SDK IAM and recovery. Product implementation must use a transactional server uniqueness/authority boundary; a test-only in-memory map is not a substitute.
- **A:** RFC 9110 retry ambiguity, HTTP socket termination, service-worker foreground/background limits and IndexedDB/local-outbox separation; browser request APIs cannot elect remote Owner.
- **C:** independent server log/receipt and client ACK oracles; test first failure, 2 simultaneous clients, restart/ACK loss, negative Owner transfer and exact commit/version. Real Firestore Emulator/Functions tests remain OPEN.
- **B:** user-visible states must distinguish Saved locally, Pending, UNKNOWN, Denied, Remote accepted, Locally applied, Converged and Verified backup. Design Studio [WEB_STATUS](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) / [LAYOUT_STATUS](https://github.com/yhappcom/design-studio/blob/main/progress/LAYOUT_STATUS.md) remain Stage 3 PRACTICE, not physical runtime certification.
- **D:** Marketing [STATUS](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) retains D8 PWA/managed EFB/Sync claim HOLD; do not count local save, HTTP receipt, applied cursor or installed PWA as the same funnel event. Privacy-minimized aggregate diagnostics only.
- **Software Engineering:** owns exact product code, Firestore Emulator/Functions implementation, server transaction and Auth verification, W-012/013/014 37-store LBK, compiled Flutter Web and physical-device tests. No peer repository edits.

## 6. Product-grade falsification plan [OPEN / MINTTAP DIRECTION]
**Do not change the approved UTC LWW policy or add automatic background sync.** Once product Engineering can run the actual server:
1. With verified UID A and B, test forged body Owner, expired/revoked Auth, deleted stream, stale replica and privilege escalation through every endpoint including latest-only reads, direct Firestore client writes and server Admin SDK paths.
2. Commit Operation X with server transaction, lose ACK after durable commit, retry **X with same digest** and compare exact Receipt/sequence; retry changed digest and require collision. Run with 2 server instances and injected Firestore transaction retry, not just one Node event loop.
3. Revoke/transfer Owner between original acceptance and receipt lookup; verify current disclosure policy and that old identity cannot cause a new material effect. Include restored v2 LBK binding with historical eligibleProven and new Replica ID.
4. Verify exact original modifiedAtUtc microseconds and UTF-8 tie-break, DELETE/RESTORE and independent CREATE identity/sector collision. ServerSequence must not decide winner.
5. On clients, inject failure after Pull but before atomic 37-store Apply/Cursor; ensure no cursor advance or false lastSyncAt. Test interrupted backup, schema migration, Safari installed PWA, MDM-managed iPad offline cold start and explicit manual recovery.
6. Separate app attestation, authenticated UID, current Owner, immutable receipt and local backup custody. No single green test substitutes for another gate.

**Stage 8 ACTIVE · synthetic HTTP model bounded · authenticated Firebase product validation OPEN · PWA release HOLD.** Adjacent next evidence: exact hosted Node CI result, then authenticated Emulator/Functions and product-owned 37-store restoration; further untrusted-token toy-model extensions have diminishing value.

**CHANGE WATCH:** Firebase server-SDK rules/IAM behavior, App Check endpoint-specific replay support, Firestore transaction retries, Safari/WebKit storage partitions, actual LogMate Sync implementation and managed EFB policy.


## 7. Canonical Software Engineering transfer and non-duplication [TRANSFER VALIDATION / CONTRADICTION]

Read-only canonical peer evidence (2026-10-28): [Software Engineering Studio validation standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md), [Data D006 real TCP ambiguous retry across process restart](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_real_tcp_ambiguous_retry_restart.md), [Data D006 inbound cursor/apply atomicity](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_logmate_inbound_cursor_atomicity_transfer.md), and current [Data](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/DATA_STATUS.md) / [Quality](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/QUALITY_STATUS.md) / [Systems](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/SYSTEMS_STATUS.md) specialist gates.

**Evidence hierarchy correction:** Engineering D006 already executed a **stronger persistence-focused ACK-loss experiment** than RA05: real TCP, SQLite durable dedup, a separate server process killed after commit/before ACK, restart and same-ID retry; a deliberately unsafe control duplicated the effect. RA05 adds an HTTP request/socket and **current-Owner admission composition**, but its in-memory server cannot claim to reproduce or improve on D006's crash-durable proof. The Web Manager owns *web endpoint authorization/receipt exposure/PWA release consequences* and **consumes**, rather than rewriting, D006's distributed-system durability foundation.

**Cursor dependency:** Engineering D006 separately demonstrated that publishing an inbound cursor before the entity apply can make an unapplied change unreachable after crash even when SQLite reports a healthy database. The approved 2026-10-17 LogMate contract now explicitly requires atomic local Apply plus contiguous cursor. RA01–RA18 do **not** test a client cursor; they must not promote any server receipt into completed Manual Sync.

**Validation-standard cross-check:** CLAIM = a synthetic HTTP boundary can preserve operation identity and reject stale-owner requests in one process; TARGET = committed public Node model at \`012799eb\`; SPEC = approved LogMate contract plus RFC 9110/Firebase primary sources; ORACLE = RA01–RA18 independent response/state assertions; ENVIRONMENT = Node 22.23.3 on Ubuntu 24.04; OBSERVATION = hosted 18/18; FAILURE MODEL = lost response, stale/revoked owner, digest collision, replay, UTC order; EVIDENCE LIMIT = no cryptographic auth, Firestore transaction/durability, multi-instance crash, client cursor, actual LogMate, Safari/managed EFB. Engineering Data/Quality/Systems Stage 1 remains IN STUDY; their specialist gates are **not** implicitly advanced by this Web Manager CI.

**Consolidated next boundary:** The next useful test is an *actual* authenticated Firestore Emulator/Functions transaction with UID/Owner and receipt, plus an exact LogMate local Apply/Cursor oracle. Another in-memory ACK-loss permutation would duplicate D006 and add little evidence.
