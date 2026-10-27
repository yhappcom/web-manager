# 521 — Stage 8 PWA Sembast Cross-Tab Replay, Ledger Admission and Wasm Web-Opener Gate

Status: **SOURCE / SYNTHESIS / CONTRADICTION / bounded static audit; browser, Wasm, installed/managed-iPad and production VALIDATION OPEN**  
Reviewed: **2026-10-27 (KST)**  
Canonical owner: **Track E — Web Architecture, Security & Operations**. Track A supplies browser/platform foundations; Track C owns independent execution; B/D consume cross-track evidence. Web Manager coordinates, not a sixth specialist.

## 1. Problem, history and decision pressure [HISTORY / DEPENDENCY]

Previous 312/319/516/519/520 studies already establish source-bounded Auth, account-deletion, Service Worker, artifact-custody and EFB questions. They need exact NORMAL/browser/device execution, not another speculative Worker micro-study. A distinct under-integrated dependency is the behavior of LogMate's **actual web database adapter** under concurrent same-origin tabs and a potential future Dart Wasm build.

"Database transaction is cross-tab safe" does not mean (a) the application callback executes exactly once, (b) the same user intent cannot be submitted twice, (c) remote effects are acknowledged, (d) browser storage survives loss/eviction, or (e) a future compiler chooses the intended web database factory. The distinction matters for an offline flight logbook with revision history, outbox, backup and account ownership.

## 2. Pinned sources and freshness [SOURCE]

- Web Manager run-start main **b58a02b1a2fd666ce4dc07130674dd5e108713e9**. Read AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research/README and relevant 312/319/516/519/520, plus latest commits. Generic Stage 1–12 PASS is not applied release certification.
- LogMate latest main **7caaee998251602e72159eeebda61f701bdea270**, eight commits after 26d2d7c. Compare shows W-001 native-file test/evidence/checklist paths only, not production lib/web/schema/dependency changes: https://github.com/yhappcom/logmate/compare/26d2d7c...7caaee998251602e72159eeebda61f701bdea270 .
- Web opener selector: lib/repository/logbook/sembast_database_opener.dart **22251c6fd6ff7957420ab0e9d94248069063c2a7**; web implementation **87f043d582375a7d11a8183889f2f23195396ef1**; fallback **6ee14b6e4a720e4fb827d603724dc87e65f130f2**. Browser DB name: **logmate_ledger**.
- Sembast adapter: lib/repository/logbook/sembast_logbook_repository.dart **d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb** (6,156 lines). Stable caller mutation identity: repository_types.dart **eeb25e1609679fa603c120b1ec6ef40fee4c9d35**; canonical plan: ledger_mutation_plan.dart **378bb616a2cda8b786f109673a29a0ba5867da8d**; F1 persistence: sync_persistence.dart **fed4f6600f1c0581ddb85c8d1c0730f94f1e0363**.
- Lockfile **746ef9de51b1096fb1d64784d098ae188abdbd43** pins **sembast_web 2.4.6, sembast 3.8.11, idb_shim 2.9.9**. Upstream current master is not a substitute for these locked runtime bytes.
- **Version-matched package-author contract**, reviewed 2026-10-27: https://pub.dev/packages/sembast_web/versions/2.4.6 . States that web content is synchronized across open tabs, transactions are cross-tab safe, and **transaction callbacks must be idempotent because they may be run again after concurrent changes**. Supporting author description of journal revisions/BroadcastChannel: https://github.com/tekartik/sembast.dart/blob/master/sembast_web/doc/implementation_details.md (master documentation, not a pinned implementation test).
- **Browser primary references:** https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB ; https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction ; https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API . IndexedDB commit/abort, physical durability, partition and BroadcastChannel notification are separate semantics.
- **Dart/Flutter primary references**, reviewed 2026-10-27: https://dart.dev/interop/js-interop/package-web ; https://dart.dev/tools/pub/create-packages ; https://docs.flutter.dev/platform-integration/web/wasm ; https://docs.flutter.dev/platform-integration/web/faq . Modern JS+Wasm web conditional selection uses dart.library.js_interop; dart.library.html is legacy and not Wasm-compatible.
- **Peer transfer:** Design Studio W121 and CD115 (runtime and truthful recovery-language evidence remains OPEN), Marketing Manager STATUS D8/D9/D10 (LogMate PWA/Sync/deletion public claims HOLD), Software Engineering methods/VALIDATION_STANDARD.md (independent oracle contract). Peer repos read-only.

## 3. Three distinct transaction layers [SYNTHESIS]

**Browser IndexedDB:** Transactions are scoped, can abort for quota/I/O/process failures, and their completion is not an external backup or unconditional physical disk-flush guarantee. Do not promote a JavaScript success callback into a device-loss recovery receipt.

**Sembast Web:** The package author documents a memory-loaded journal database, incrementing revisions and BroadcastChannel change notifications. A concurrent tab change can lead the package to reload data and **re-invoke the application's transaction function**. BroadcastChannel is neither a global security authority nor an automatic PWA-to-native-device sync channel.

**LogMate logical intent:** RevisionId, OperationId and acceptedAtUtc are supplied by callers as LocalMutationIdentity. Canonical plans include record-revision and structure-generation compare-and-swap (CAS); outbox presence is pending local work, not a server acknowledgement. Callback replay, user double-submit, unknown-commit retry, remote replay and distinct user edits are different phenomena.

Required properties: (I1) no material external side effect in replayable callbacks; (I2) one logical intent keeps stable identity/time; (I3) active record, revision, outbox, Sync binding and aggregate state commit together or not at all; (I4) stale plans reject or explicitly replan, never silently overwrite; (I5) deletion and owner locks fence material access; (I6) installed browser storage is not independently verified backup.

## 4. Exact-source audit: positive controls and limits [SOURCE / VALIDATION]

A bounded lexical scanner of the pinned Sembast adapter found **54 explicit _database.transaction(...) sites** and matched their parenthesized callback spans. This is **not a Dart AST, full helper call graph or runtime trace**.

| Area | Verified source design | What remains unproven |
| --- | --- | --- |
| Direct create/update/delete/restore (approximately 2140–2355) | Caller-supplied LocalMutationIdentity; _requireUnusedMutationIds checks revision/outbox uniqueness; record, revision, outbox and generation writes share a transaction. No network call appears in those bodies. | Prior 312/319 found missing direct owner-lock checks; retained second-tab handles require runtime authorization tests. A fresh OperationId on user retry is a new identity. |
| Canonical commitLedgerMutation (2121 and 2390 onward) | _prepareRecordMutation checks revision CAS and uniqueness; structure generation CAS; writes and checkpoints stay in transaction path. | Actual two-tab replay, conflicting plan handling and interrupted commit not executed. |
| finalizeFlightEntryDraftSave (787–978) | Durable receipt keyed by draft ID/revision plus payload fingerprint returns prior result for matching retry; changed payload/stale revision rejects. | This is a **scoped** dedupe safeguard, not global exactly-once or server ACK. |
| Backup export/restore (423–556) | Snapshot constructed inside read transaction; restore stages multiple store writes and validates before publish. | Files custody, snapshot age, interrupted restore and actual iPad recovery remain OPEN. |
| Test-only probes | Nine scanned callback bodies reference test hooks (restore, draft save, two baseline flows, four CRUD, migration). Production open() does not install the test probes; openForTesting variants do. | Probe invocation count may exceed durable commits under callback replay; do not label this a production external side effect. |
| Replica initialization | _newLocalReplicaId uses Random.secure() only if no replica row exists. | A replay can create different uncommitted candidates; only the committed row is authoritative. Not proof of two durable replicas. |

The adapter has no DateTime.now call in this file; that does **not** prove every transitive helper or caller is pure. The inspected source does **not** demonstrate a duplicated durable operation, a browser exploit or a user incident. LogMate W-001 **49/49 focused tests** (six new plus 43 unchanged; run at 89300a6) are valid **native host file-Sembast** evidence, not Sembast_web/BroadcastChannel/browser evidence.

## 5. Independent future Wasm opener contradiction [SOURCE / CONTRADICTION / CHANGE WATCH]

LogMate's conditional selector uses this form:

    import 'sembast_database_opener_stub.dart'
        if (dart.library.io) 'sembast_database_opener_io.dart'
        if (dart.library.html) 'sembast_database_opener_web.dart' as platform;

The fallback raises UnsupportedError ("Sembast local ledger is not configured for this platform."). Dart's modern conditional-import documentation selects web via **dart.library.js_interop**, including Wasm. Dart/Flutter documentation explicitly says **dart.library.html is not available for Wasm**. Thus a **future Wasm target** is source-predicted to choose the fallback, even though upstream sembast_web advertises Wasm support. Other dependencies might fail compilation earlier.

**Boundary:** No approved Wasm target, exact Wasm build or runtime was tested; this is **not** evidence that today's NORMAL JavaScript PWA fails. Flutter 3.50+ no-deprecated-js-interop is a future-toolchain watch, not a flag used by the pinned Flutter 3.47.5 W-001 host test. A Wasm proposal requires full import-graph review, JS and Wasm builds, and both targets' real create→close→reopen→readback before release.

## 6. Failure modes and diagnostic counterexamples [SYNTHESIS / EXPERT JUDGMENT]

1. A network send inside a retryable callback may happen twice even when local writes commit once. No such production send was established in the inspected direct bodies; future side effects belong behind a durable post-commit outbox.
2. UNKNOWN local commit + newly minted OperationId on UI retry can represent a second logical intent. Reconcile the original ID/receipt before generating another.
3. Two legitimate edits of the same record may conflict at revision CAS. Reject/review the stale plan; last-write-wins is not an acceptable default.
4. Callback invoked twice does **not** mean two durable transactions committed. Count raw committed operation IDs independently.
5. Sign-out or deletion in tab A is not itself a security fence for tab B. Re-read owner/deletion state at each material admission; reuse 312/319 negative controls.
6. Browser process death, quota and OS power loss are not equivalent to ordinary transaction callback rejection; verify persisted state after reopening.
7. Safari tab, Home Screen web app and managed Web Clip cannot be presumed one storage container. WebKit's Safari 17.2 description: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ .
8. Different hostnames or localhost ports mean different IndexedDB origins. The package author explicitly warns that changing debug port changes the DB.
9. Service Worker update and shell repair do not prove database migration, durable outbox continuity or external backup.
10. A Wasm-compatible upstream package is insufficient if LogMate's own import selector chooses a stub.
11. In-memory journal load and cross-tab reload may affect large-ledger memory/latency; no field performance or actual Safari timing evidence exists.
12. Diagnostic analytics must exclude raw flight payload, UID, auth code, token and LBK contents.

## 7. One existing Engineering execution campaign: TX01–TX16 [VALIDATION — NOT EXECUTED]

Reuse W-031/W-036 browser/PWA release, W-012/013/014 backup, W-030 deletion and F1 Sync. Use synthetic A/B owners, exact approved NORMAL archive/HTTPS origin, locked package version, independent raw-store/receipt/record/aggregate oracles, and exact source/ref, artifact hash, browser/OS/partition, initial state, interleaving, callback attempts, committed row counts and post-reopen readback.

| ID | Discriminating positive/negative test |
| --- | --- |
| TX01 | JavaScript NORMAL create→commit→close→reopen; active/revision/outbox/generation consistency. |
| TX02 | Two same-origin Chromium tabs force same-OperationId conflict; distinguish callback attempts from durable effects. |
| TX03 | Two different IDs update same revision; one succeeds, other explicitly stale/reviewed, never silently overwritten. |
| TX04 | Controlled concurrent writer causes documented Sembast_web callback replay; independently verify final raw store. |
| TX05 | Test-only probe/counter demonstrates callback invocation is not a durable-commit count; never enable in production. |
| TX06 | UNKNOWN commit retry with stable draft ID/revision/payload returns prior receipt; changed payload rejects. |
| TX07 | Interrupted active/revision/outbox/Sync-binding/aggregate publication; all-or-none after reopen. |
| TX08 | Tab A signs out or changes owner while B retains edit handle; no unauthorized read/write. |
| TX09 | Tab A enters deletion localLocked while B writes; no post-fence mutation; reuse 319 DE04/DE05. |
| TX10 | Quota/write failure and restart; atomic rollback or explicit UNKNOWN, no false "Saved"/"Synced". |
| TX11 | Browser kill around commit; reconcile durable identity, not merely callback/visual state. |
| TX12 | Safari same-origin tabs, then separate Safari→Home Screen installed context; measure partitions independently. |
| TX13 | Physical managed iPad/Web Clip, OS/MDM policy, cold offline restart, ledger and LBK readback. |
| TX14 | Canonical host vs Firebase default host vs another localhost port; demonstrate origin-scoped DB and no implicit migration. |
| TX15 | Exact JS versus proposed Wasm build: conditional selection, real DB open, create→reopen; stub is explicit negative. |
| TX16 | If Flutter 3.50+ / no-deprecated-interop is adopted, compile/runtime negative control; otherwise CHANGE WATCH only. |

**Oracle independence:** raw typed store keys and counts, stable operation/revision IDs, value/aggregate parity, deletion/owner state, no duplicate durable outbox, verified external LBK file, and server receipt only if a real server participates. A native file widget PASS, JS model, browser tab PASS, installed Safari PASS and managed-EFB PASS are different evidence tiers. Apply Engineering's CLAIM→SPEC→TARGET→INPUT→ORACLE→ENVIRONMENT→OBSERVATION→VERDICT→LIMIT contract.

## 8. Five-track allocation and transfer [DEPENDENCY / TRANSFER VALIDATION]

**E primary:** replay-safe local authority, owner/deletion fences, post-commit side effects, rollback, backup and release governance.  
**A major:** IndexedDB, Sembast journal/BroadcastChannel, origin/partition and JS/Wasm conditional import; other tracks consume rather than duplicate its primer.  
**C major:** actual TX01–TX16 concurrency/fault/device and accessibility/performance oracles; W-001 host evidence remains scoped.  
**B consumer:** Design Studio CD115/W121 truthful Saving, Saved locally, UNKNOWN, Retry and recovery; avoid blind duplicate action and verify focus/AT on real PWA.  
**D consumer:** Marketing D8/D9/D10 claim HOLD; distinguish local save, remote Sync, installed acquisition and verified backup; privacy-minimized measurement.  
**Software Engineering:** owns implementation, package-runtime instrumentation, Dart/browser tests and build target decisions. No peer/product edits.

## 9. Operational judgment, OPEN and stop check [MINTTAP DIRECTION / CHANGE WATCH]

**MINTTAP DIRECTION (research only):** Preserve stable logical intent IDs through UNKNOWN retries, keep external effects outside replayable callbacks, require durable owner/deletion admission at material access, and do not promote a package's "cross-tab safe" label into application-level data/authority certification. Keep the current JS path separate from any future Wasm migration until exact build/readback evidence.

**OPEN:** real Sembast_web two-tab replay; exact NORMAL/served artifact; JS opener runtime; Wasm compilation/selection; stale-tab authorization; quota/crash; large-ledger memory; Safari/Home Screen/managed EFB; 37-store/Sync/LBK recovery; real remote Sync and deployed deletion workflow.

**CHANGE WATCH:** pinned 2.4.6 vs upstream updates; Flutter/Dart Wasm and no-deprecated flags; IndexedDB durability/partition changes; LogMate callback/caller/Sync writers and release topology.

**Stop check:** This integrated cycle read latest governance and commits, version-matched upstream behavior, exact web opener/fallback/lockfile, 54 transaction-site lexical inventory, identity/CAS/receipt/outbox and test-hook positives, Dart/Flutter Wasm contradiction, W-001 bounded evidence, browser standards and all five tracks. Remaining decisive evidence requires **actual Dart/browser/physical-device execution**, not more T0 mock studies. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


---

## 10. 2026-10-28 exact-version browser execution bridge — fixture committed, execution not yet verified

**Why this continuation:** The earlier 54-transaction-site lexical review, W-001 native-file Sembast tests and upstream `sembast_web` package statement are not a browser execution of the exact web adapter. Rather than add another synthetic Node-only model or repeat the package primer, this checkpoint creates a **real Dart/Chrome browser probe** against the exact package versions, with a narrow independently observable transaction/reopen contract.

### SOURCE / version and standards boundaries

- [sembast_web 2.4.6 author documentation](https://pub.dev/packages/sembast_web/versions/2.4.6): IndexedDB-backed web DB, cross-tab synchronization and transaction-callback replay warning. Package documentation is not evidence that this specific application was executed.
- [Dart official browser-test instructions](https://dart.dev/web/debugging): `dart test -p chrome` is a supported browser-test route. Browser execution is not equivalent to Node executing dart2js.
- [W3C IndexedDB 3.0 transaction durability](https://www.w3.org/TR/IndexedDB/): `strict`, `relaxed` and `default` are **durability hints**; a transaction completion or close/reopen in a running browser does not establish physical power-loss durability, independent backup or storage-eviction immunity.
- Exact product dependency versions from LogMate `main@d3bc214f`: `sembast_web 2.4.6`, `sembast 3.8.11`, `idb_shim 2.9.9`. This standalone research package declares those exact direct versions, but **does not preserve a resolved transitive lockfile**. A hosted `dart pub deps` output is required before any stronger dependency-provenance claim.

### Executable research artifact / VALIDATION status

- [Fixture source](handoffs/sembast_web_246_browser_probe/test/sembast_web_probe_test.dart), [package definition](handoffs/sembast_web_246_browser_probe/pubspec.yaml), [scope README](handoffs/sembast_web_246_browser_probe/README.md), [read-only GitHub Actions workflow](../.github/workflows/stage8_public_sembast_web_246_browser.yml).
- `SB01`: one transaction writes three synthetic stores; close/reopen and read each value. Oracle: explicit values and identities after reopen.
- `SB02`: deliberately throw inside a three-store transaction; close/reopen and independently require absence of all three attempted writes. Oracle: no partial logical publication.
- `SB03`: fixture-defined stable operation ID and digest; identical retry returns `REPLAY` and only one synthetic revision/outbox/flight remains. **This is a test of the fixture's own idempotency algorithm atop the package, not proof of LogMate's production algorithm.**
- `SB04`: fixture-defined same ID with different digest rejects; reopen and require the original digest and exactly one revision/outbox. This is a bounded identity-collision control, not authenticated server or LBK behavior.
- The workflow pins Dart **3.12.0**, runs on **Ubuntu 24.04** in headless **Chrome**, checks `dart analyze`, records the dependency graph and requires exactly four non-hidden successful browser test results. It has no private checkout, token, product data or Firebase connection.
- **At documentation checkpoint, no completed hosted job log or PASS has been retrieved.** The public fixture and workflow are committed, but execution is **UNKNOWN / NOT PROMOTED**. A workflow file's existence, or a green commit unrelated to this job, is not execution evidence. Record exact run ID, job log, package resolution and browser build before changing the verdict. A failure before browser tests is NON-EXECUTION; a browser assertion failure is a real bounded fixture failure.

### Interpretation / CONTRADICTION / transfer

The tests can close a **narrow exact-package Chrome same-tab persistence/rollback** question if they actually execute. They cannot settle cross-tab callback replay (TX02–TX05), UNKNOWN crash durability (TX10–TX11), stale owner/deletion tab authority (TX08–TX09), Safari/Home Screen/managed EFB (TX12–TX13), exact LogMate 37-store LBK recovery, future Wasm selection or Manual Delta Sync. Reopening with the same Sembast API is also not a fully independent raw IndexedDB oracle; exact product tests must add independent store-level inspection and failure injection.

**E** owns transaction/authority/release limits; **A** supplies package/browser/IndexedDB mechanics; **C** owns executed Chrome evidence, raw-store negative oracles and later Safari/physical-device transfer. **B** consumes UNKNOWN/saved-locally/restore UX boundaries from Design Studio W121; **D** consumes Marketing D8 claim HOLD and must not call a synthetic Chrome probe EFB readiness. Software Engineering's [validation evidence contract](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) supplies CLAIM→TARGET→ORACLE→ENVIRONMENT→OBSERVATION→VERDICT discipline; implementation and product test modifications remain Engineering-owned.

**MINTTAP DIRECTION (research, not product approval):** treat this as a dependency-level execution bridge. First obtain actual hosted results; next run TX02–TX05 with independent tabs and raw-store commit counts, then exact LogMate W-012/W-013 and Safari/managed EFB. Do not infer physical durability or cross-device sync from local transaction success.

**Gate unchanged:** Applied Stage 8 ACTIVE; exact-package Chrome **execution verdict OPEN**; LogMate product validation OPEN; PWA release HOLD. **Adjacent-question check:** tested scope, negative rollback, identity replay, package provenance, physical durability and peer transfer are included here; remaining decisive work requires browser execution evidence and product-authorized tests rather than further speculative micro-studies.


## 11. Exact-version Chrome fixture executed, six-case bounded checkpoint [VALIDATION / CONTRADICTION / TRANSFER VALIDATION — 2026-10-28 KST]

**Evidence chain:** [initial pre-test failure 40547093383](https://github.com/yhappcom/web-manager/actions/runs/40547093383) → [four-case success 40556099657](https://github.com/yhappcom/web-manager/actions/runs/40556099657) → [six-case success 40556384695](https://github.com/yhappcom/web-manager/actions/runs/40556384695). The six-case job `122373449345` checked out `51ff377f455af513679f00616db152c877a261f1`, ran Dart SDK 3.12.0 on Ubuntu 24.04 with `/usr/bin/google-chrome`, resolved direct packages `sembast_web 2.4.6`, `sembast 3.8.11`, `idb_shim 2.9.9`, passed analysis, and reported `SB01-SB06 completed: 6 results: success,success,success,success,success,success`. Browser version and transitive lockfile hash were not recorded by that run. The next strict-format CI execution must be independently checked; do not project this run's result onto later commits.

**CLAIM/SPEC:** For a synthetic three-store local ledger, a completed transaction should expose all intended rows after ordinary close/reopen, an explicitly thrown transaction should expose none, and a fixture-owned stable Operation ID/digest admission rule should avoid duplicate durable rows or conflicting reuse. The first two are bounded database behavior; the latter are **application rules written into this research fixture**, not claims about LogMate's production code.

**TARGET/INPUT/ORACLE:** Exact public fixture [test](handoffs/sembast_web_246_browser_probe/test/sembast_web_probe_test.dart), Chrome IndexedDB via `databaseFactoryWeb`; synthetic flights/revisions/outbox; independent post-reopen row lookups/counts and return/error assertions. SB01 commit/reopen; SB02 explicit abort/reopen; SB03 same ID/digest sequential; SB04 same ID/different digest sequential; SB05 same-page two opens concurrent same ID/digest; SB06 same-page two opens concurrent differing digests. Six test completions are not six independent browser contexts, and row-count oracles cannot independently establish true cross-tab transaction callback replay.

**Failure-first classification:** Initial CI checkout, SDK and `pub get` succeeded, but `dart analyze --fatal-infos` rejected a redundant `sembast` import; Chrome step was SKIPPED, **not** a product/transaction failure. The import removal led to 4/4 green. The six-case extension passed, with exactly one `NEW` and one `REPLAY` for same digest and one `NEW` plus one `REJECTED` for differing digests, with one durable operation/revision/flight row after reopening. Concurrent scheduling and whether the factory internally reuses one DB instance remain unproven; the test does **not** assert two independent tabs.

**SOURCE cross-check (2026-10-28):** Version-matched [package author contract](https://pub.dev/packages/sembast_web/versions/2.4.6) warns that transaction callbacks can re-execute on concurrent changes, so callback side effects must be idempotent. [MDN IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) distinguishes transaction completion from power-loss durability. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) documents quotas and eviction, not guaranteed lifetime preservation; Home Screen quota parity does not establish Safari-tab data sharing or managed-EFB persistence. These are separate standards/platform/package claims, not a transfer PASS.

**Five-track and peer synthesis:** E owns authorization/transaction/release HOLD; A supplies package, IndexedDB, origin and lifecycle semantics; C owns CI provenance, negative controls and next true two-tab/device oracles; B consumes Design Studio W121/CD127 for accurate `Saved locally`, `Unknown` and recovery states; D consumes Marketing D8–D10 to avoid claiming Sync/backup/managed-iPad readiness. Software Engineering `methods/VALIDATION_STANDARD.md` owns the general claim→oracle→environment→failure→limit discipline and product implementation. No peer/product edits.

**OPEN / next discriminating campaign:** TX02/TX04 require two independent same-origin Chrome tabs with a controlled interleaving, callback-invocation counters **separate from durable row counts**, and process/transaction abort controls; TX08/TX09 owner/deletion fences; TX10/TX11 quota/crash/UNKNOWN; TX12/TX13 Safari Home Screen and managed EFB; W-012/013/014 exact LogMate 37-store LBK/file/restore. No actual LogMate code, remote Firebase Sync, physical durability or installed PWA was executed. **Stage 8 ACTIVE · Public exact-package Chrome synthetic 6/6 PASS · Production validation OPEN · PWA release HOLD.**
