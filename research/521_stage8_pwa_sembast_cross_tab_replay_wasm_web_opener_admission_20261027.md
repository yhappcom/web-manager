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

**Post-checkpoint CI confirmation [VALIDATION — 2026-10-28]:** [strict final run 40556727926](https://github.com/yhappcom/web-manager/actions/runs/40556727926), job `122374651411`, exact `b5d31da3b3e5b2020f01e980057d61f152740678`, Ubuntu 24.04, Dart 3.12.0, Chrome **155.0.8059.39**: strict `dart format --output=none --set-exit-if-changed test` **0 changed**, analyzer **0 issues**, **SB01–SB06 6/6 PASS**. No new fixture source mutation occurred between the formatted code commit and this run. Exact LogMate `main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f` read-only recheck confirms the web opener still selects `dart.library.html`; no product runtime executed. The public fixture still lacks a committed full transitive lockfile; repeatability is bounded by recorded resolved versions and source ref. Stage 8 and product HOLD unchanged.

---

## 12. Independent Chrome tabs / Sembast 2.4.6 controlled interleaving campaign — executable bridge, outcome OPEN [SOURCE / SYNTHESIS / DEPENDENCY / VALIDATION / OPEN / CHANGE WATCH — 2026-10-28]

### Why §11's green result is not enough

The six-case Chrome job exercised two `openDatabase` calls **inside one browser page**. The version-matched [Sembast Web 2.4.6 author contract](https://pub.dev/packages/sembast_web/versions/2.4.6) explicitly describes cross-tab synchronization through BroadcastChannel and warns that concurrent writes can **re-execute transaction callbacks**. An application that sends remote requests, increments nontransactional counters, or displays irreversible success from a callback could therefore create side effects even when durable local rows remain deduplicated. This is a **risk model**, not a finding that LogMate does so.

[MDN Broadcast Channel](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) scopes communication to compatible origin/**storage partition**, not merely identical URL text; [IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) separates logical transaction completion from a guarantee of physical power-loss survival. WebKit's [storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) discusses quota and eviction but does not transfer Chrome-tab evidence to Safari Home Screen or managed iPad. These standards and platform facts remain distinct.

### Executable fixture and independent evidence chain [VALIDATION — NOT YET EXECUTED]

A new, public, **product-independent** bridge was committed under `research/handoffs/sembast_web_246_browser_probe/`:

- `web/two_tab_probe.dart`: compiled Dart-to-JavaScript adapter using the same declared direct dependencies as the prior fixture; exposes test-only open/apply/hold/release/read/close functions. Stable Operation ID/digest logic is **fixture-owned**, not copied from LogMate.
- `web/index.html` and `scripts/two_tab_probe.mjs`: a local same-origin HTTP server and **two distinct Playwright Chrome pages** in one browser context, followed by a **fresh third page** for reopened ledger counts. The third-page readback is stronger than same-page two opens, but it still uses the same Sembast adapter and is **not a raw independent IndexedDB oracle**.
- `.github/workflows/stage8_public_sembast_web_246_two_tab.yml`: public-only Ubuntu 24.04 / Dart 3.12.0 / installed Chrome / pinned direct `playwright-core@1.56.1` execution; no LogMate checkout, private secrets, Firebase or real flight data. `dart compile js -O2` builds the test-only bridge. The browser-driver dependency's full transitive graph and Chrome version must be recorded from an actual job before repeatability is promoted.

**TB01** opens two actual tabs on the same origin and DB, commits operation/digest B, then retries identical digest in A. Expected `NEW` then `REPLAY`, with one flight/revision/outbox after closing both and reopening in a third tab.

**TB02** repeats the same two-tab sequence with different digests. Expected B `NEW`, A `REJECTED`, and the original digest preserved with one durable row per synthetic store. These two baselines test cross-tab observation and fixture-level identity admission; **they do not force a concurrent callback replay**.

**TB03** holds A inside a transaction callback after reading its existing record, attempts a conflicting write from B, and releases A after a bounded window. It records whether B actually committed **before** A resumed. If the desired ordering is not established, the result is **INCONCLUSIVE**, not a replay PASS. The callback count is separate from the durable row count: `calls > 1` is required to claim observed callback re-execution. A no-replay observation is not proof that replay cannot occur.

**Execution verdict at this checkpoint:** source and workflow **COMMITTED; no completed hosted job log or actual test output retrieved**. Compile, two-tab baseline and overlap remain **OPEN**. In particular, the earlier six-case [run 40556727926](https://github.com/yhappcom/web-manager/actions/runs/40556727926) must not be reused as proof for this new fixture. CI checkout/analyze/compile failures must be classified as **NON-EXECUTION** of the browser assertions.

### Eight connected operational judgments [SYNTHESIS / TRANSFER VALIDATION / CONTRADICTION]

1. **Platform (A):** same-page DB handles, independent tabs, separate browser profiles, Safari tab vs installed Home Screen, and managed EFB are five different isolation experiments. Neither BroadcastChannel delivery nor IndexedDB origin sharing proves the next tier.
2. **Transaction authority (E):** retry identity and digest must be admitted in the transaction; callback invocation count is not durable commit count. Post-commit remote effects require separate idempotency and current authority.
3. **Quality oracle (C):** require independent tab objects, controlled order, reopen/row counts, raw IndexedDB inspection later, reproducible versions and a negative control that fails when digest is changed.
4. **Failure injection (E/C):** browser/tab termination before/after commit, quota exhaustion, UNKNOWN commit receipt and stale tab after owner deletion remain separate TX08–TX11 gates.
5. **UX transfer (B):** `Saved locally`, `Unknown`, `Retry`, `Backed up`, and `Synced` must not collapse into one green success state. Design Studio W121/CD127 remains Stage 3 practice, not runtime-certified UI.
6. **Discovery/claims (D):** Marketing D8's LogMate PWA/managed-iPad claim HOLD remains valid even if Chrome two-tab fixture succeeds; installation, backup, synchronization and fleet support require independent evidence.
7. **Device durability (A/E):** a Chrome reopen proves neither OS power-loss durability nor Safari/WebKit storage retention. EFB no-App-Store/no-hotspot constraints must be checked against actual management/network policies.
8. **Engineering ownership:** general instrumentation and exact product 37-store W-012/W-013/W-014 execution belong to Software Engineering/Product. This public fixture is a dependency-level experiment; do not modify peers or LogMate to make the test green.

**Stop/next decision:** Obtain exact hosted compile and two-tab results; if TB03 is inconclusive, refine the interleaving rather than claim replay. Then add independent raw IndexedDB counts, stale-owner/deletion fencing and physical Safari/managed-EFB transfer. **Stage 8 ACTIVE · Public same-page Chrome 6/6 PASS (previous ref) · New independent-tab execution OPEN · Production validation OPEN · PWA release HOLD.**


---

## 13. 2026-10-28 two-tab adversarial oracle upgrade — source committed, hosted verdict OPEN

**Why another adjacent block was warranted [SYNTHESIS]:** §12 created a true independent-tab bridge, but its first two baselines were sequential, its third-tab reader reused the same Sembast abstraction, and its conditional overlap might report INCONCLUSIVE while the process exited successfully. A passing workflow could therefore be misread as evidence for callback replay or raw IndexedDB integrity. This continuation closes part of that *evidence-quality* gap rather than writing another package primer.

### SOURCE — browser standards and platform boundaries (rechecked 2026-10-28)

- [W3C Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB/) and [MDN IDBFactory](https://developer.mozilla.org/en-US/docs/Web/API/IDBFactory) define browser-side database discovery/opening; [IDBDatabase.transaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction) permits read-only object-store inspection. The inspection is independent of Sembast's high-level `find` path, but shares the same browser, origin, IndexedDB implementation and failure domain.
- [MDN Broadcast Channel](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) limits delivery by storage partition, not URL equality alone. Two pages in one browser context are a useful same-partition test, **not** two independent devices or browser profiles.
- [MDN IndexedDB usage](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) distinguishes transaction completion from physical power-loss persistence. Even a raw read-only inspection after close/reopen does **not** prove fsync, storage survival after eviction, or backup recoverability.
- [Sembast Web 2.4.6](https://pub.dev/packages/sembast_web/versions/2.4.6) warns about transaction callback reexecution under concurrent writes; this is an upstream contract, not an observed LogMate incident or a guarantee that a particular artificial interleaving will reproduce replay.

### VALIDATION — new exact public fixture (NOT EXECUTED in this checkpoint)

The existing `research/handoffs/sembast_web_246_browser_probe/scripts/two_tab_probe.mjs` was extended without changing LogMate or the public Dart adapter:

1. **Raw read-only IndexedDB inventory:** after both writers close, the fresh third tab calls `indexedDB.databases()`, opens each discovered DB without requesting an upgrade, enumerates object stores and reads their **raw entry counts** through native IndexedDB transactions. It asserts that the browser exposes the inventory and at least one physical object-store entry exists, in addition to the previous Sembast semantic flight/revision/outbox/digest assertions. The inventory records only synthetic database names, versions and counts, not flight payloads.
2. **TB04 — simultaneous same-digest race:** two independent tabs call the fixture's same logical operation at once; expected unordered outcomes are exactly `NEW` and `REPLAY`, followed by one semantic row per synthetic store and a raw-IDB inventory.
3. **TB05 — simultaneous conflicting-digest race:** the same concurrency shape uses different digests; expected unordered outcomes are `NEW` and `REJECTED`, with the winner's digest retained after third-tab reopen. The winning tab is deliberately **not predetermined**.
4. **TB03 remains a distinct conditional experiment:** it only promotes the desired ordering when B completes as `NEW` before A is released and A rejects. It reports **INCONCLUSIVE** otherwise; `calls > 1` is separately required for an observed callback-replay claim. A TB03 INCONCLUSIVE does not invalidate a genuine TB01/TB02/TB04/TB05 baseline PASS, but must not be advertised as a TB03 PASS.
5. **Explicit deterministic count:** exactly four baseline/race cases must complete. Failure of a race expectation, native-IDB inventory or semantic readback should produce a nonzero process exit, rather than a merely optimistic log.

**Evidence limitations / possible diagnostic false positives [CONTRADICTION]:** Raw IndexedDB object-store **entry counts are not Sembast logical row counts**; a journal, metadata or shared store may encode multiple semantic records in one entry. The raw snapshot is an *independent API path*, not an independent physical storage medium or an independent product parser. Likewise, two Playwright pages share a browser profile/storage partition, and simultaneous Promise scheduling does not force a particular IndexedDB conflict window. Neither TB04/TB05 nor a TB03 INCONCLUSIVE can prove that callback replay never happens. The full transitive Dart/npm dependency graph remains unpinned in this fixture.

**Exact result state:** Source change committed, **no completed hosted execution/job logs obtained for the upgraded fixture**; compilation, TB01/TB02/TB04/TB05 and raw-IDB assertions remain **OPEN**. The previous 6/6 same-page Chrome PASS at run 40556727926 is valid **only for the previous fixture**. Do not transfer it to this change.

### Five-track integration, project transfer and expert judgment [DEPENDENCY / TRANSFER VALIDATION]

| Track | Owns/consumes | Consequence |
| --- | --- | --- |
| **E (primary)** | Transaction authority, stable intent/digest, owner/deletion fences, durable backup/recovery and release admission | A raw entry count or local callback success is not remote authorization, durable receipt, or safe restore |
| **A (major)** | Browser IndexedDB, partition/origin, BroadcastChannel and Sembast package mechanics | Two same-origin tabs can share local DB without establishing Safari Home Screen or managed Web Clip continuity |
| **C (major)** | Test provenance, independent native-IDB inspection, concurrency/failure controls and falsifiable PASS/FAIL/INCONCLUSIVE | Preserve exact commit, package graph, browser version, tab identity, raw counts, callback attempts and durable rows separately |
| **B (consumer)** | Design Studio W121/CD127 truthful saving/UNKNOWN/recovery states | Do not show `Synced` or `Backed up` merely because a local write completed |
| **D (consumer)** | Marketing D8–D10 web/install/discovery claim gate | Public PWA/managed-iPad/offline-sync claims remain HOLD pending product/device evidence |

**External specialist boundary:** Design Studio `progress/WEB_STATUS.md` and `progress/LAYOUT_STATUS.md` remain Stage 3 PRACTICE with actual runtime/AT/physical-device evidence OPEN; Marketing `STATUS.md` retains LogMate D8 product-claim HOLD. Software Engineering owns exact product implementation and product-grade instrumentation. Public dependency fixture findings can be handed off, but no peer repository or LogMate source was modified.

### Adjacent diagnostic and release gate

1. Retrieve the exact GitHub Actions job for the upgraded two-tab fixture, distinguish compile/test NON-EXECUTION from test FAIL and record Chrome/Dart/resolved packages/commit and all four baseline outcomes.
2. If TB04/TB05 fail, preserve their failure-first traces and investigate Sembast transaction ordering, callback attempts, raw-IDB rows and fixture semantics before modifying expectations. If TB03 is inconclusive, design a stronger deterministic conflict window; do not silently promote it.
3. Follow with stale-tab owner/deletion fencing, crash/UNKNOWN-commit and quota controls, actual LogMate 37-store LBK W-012/013/014, then Safari installed PWA and managed-EFB physical evidence. A browser fixture cannot substitute for any of these.

**MINTTAP DIRECTION (research only):** Keep public exact-package synthetic evidence separate from actual LogMate release authority. Preserve Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD. **CHANGE WATCH:** IndexedDB browser implementations, Sembast callback replay/version, Dart JS/Wasm selector, Safari partition/storage policy and enterprise iPad management.


---

## 14. 2026-10-28 hosted independent-tab execution — callback replay observed, target-bound oracle follow-up

### VALIDATION — exact hosted execution (promoted only within synthetic Chrome scope)

- [GitHub Actions run 40574988642](https://github.com/yhappcom/web-manager/actions/runs/40574988642), job `122438893368`, checkout `f8b9e0c4b9f41e54714ce23dae1481dc44e308e1`, completed **SUCCESS** at 2026-10-27 20:06 UTC. Logs explicitly show Dart SDK **3.12.0**, Chrome **155.0.8059.39**, direct `sembast_web 2.4.6` and Playwright `1.56.1` (workflow pin), on GitHub-hosted Ubuntu 24.04. Transitive lockfile is not committed.
- **TB01 PASS:** independent tab A/B same-digest sequential retry -> `NEW` then `REPLAY`, one semantic record in each of three synthetic stores after third-tab reopen.
- **TB02 PASS:** changed digest -> `NEW` then `REJECTED`, first digest retained.
- **TB04 PASS:** concurrent same-digest -> `NEW` and `REPLAY`, losing callback invoked **twice** (`calls=2`), one semantic record/store after reopen.
- **TB05 PASS:** concurrent different-digest -> `NEW` and `REJECTED`, losing callback invoked **twice**, one semantic record/store after reopen.
- **TB03 conditional overlap PASS in this run:** B completed `NEW` before held A was released; A rejected with `calls=2`; third tab retained B's digest. This is an **observed interleaving**, not a promise that every run or browser will reproduce it.
- Raw read-only IndexedDB inventory returned synthetic database versions `2` with object stores `entry:3`, `info:2` in the run. These are physical API-path counts, **not** semantic row counts, independent storage, fsync, backup, Safari evidence or product behavior. The original raw assertion was too broad: it accepted *any* previously created DB with a positive count. It did not independently require the current scenario's target DB.

### CONTRADICTION / corrective oracle improvement

A source follow-up at [commit f03074bb](https://github.com/yhappcom/web-manager/commit/f03074bb4ca6e854dabc2e5bb68fcb195e759a95) now restricts native IndexedDB inventory to the **exact scenario database name**, asserts exactly one matching DB and requires a positive entry in that DB. This prevents earlier successful scenario databases from satisfying a later scenario's raw inventory. **The previous hosted PASS applies to the earlier f8b9 fixture only**; the strengthened source requires a new exact-commit CI run before its own PASS can be claimed.

### Failure-first provenance and five-track transfer

- Earlier [run 40566298388](https://github.com/yhappcom/web-manager/actions/runs/40566298388) reached the browser step but failed after `page.evaluate: Target page, context or browser has been closed`; this is a failed fixture execution, not evidence of a Sembast data-integrity defect. [Run 40566347623](https://github.com/yhappcom/web-manager/actions/runs/40566347623) subsequently passed the earlier TB01/TB02/TB03 fixture. The later f8b9 run establishes the upgraded four-baseline + conditional-overlap result.
- **E owns** atomic admission and idempotency boundaries: the observed callback replay is direct evidence that callback side effects cannot be equated to one durable commit. Any future LogMate transaction callback must avoid irreversible external effects or rely on separately proven idempotency/current authority.
- **A supplies** Chrome/IndexedDB/Sembast browser mechanics and strict isolation-tier labels; same browser-context tabs do not transfer to independent profiles, Safari Home Screen or managed iPad.
- **C owns** exact-commit reproducibility, scenario-specific raw oracle, callback-count versus committed-row distinction and failure-first controls. Repeatability under browser updates and fault injection remains OPEN.
- **B consumes** Design Studio W121/CD127 local-save/retry/UNKNOWN recovery-state requirements; a local transaction is not a remote Sync or verified backup.
- **D consumes** Marketing D8 claim HOLD; no public managed-EFB/offline cross-device Sync or durability claim is justified by this synthetic result.

**Gate decision [MINTTAP DIRECTION / OPEN]:** **Synthetic independent Chrome tabs: TB01/TB02/TB04/TB05 4/4 PASS + TB03 observed PASS at f8b9; strengthened exact-target raw oracle execution OPEN until its own CI run.** Product 37-store LBK, owner/deletion, crash/quota, Safari installed PWA, managed EFB, remote Sync and physical durability remain OPEN. Stage 8 ACTIVE; PWA release HOLD. Next: verify the f03074bb workflow, then test stale-owner/deletion fences and crash/UNKNOWN receipt without conflating fixture admission with LogMate implementation.


### VALIDATION — exact-target corrected oracle re-executed successfully

The corrected source at [f03074bb](https://github.com/yhappcom/web-manager/commit/f03074bb4ca6e854dabc2e5bb68fcb195e759a95) was independently executed in [run 40583569941](https://github.com/yhappcom/web-manager/actions/runs/40583569941), job `122469062809`, **SUCCESS**. Dart 3.12.0 / Chrome 155.0.8059.39 / direct Sembast Web 2.4.6. **TB01/TB02/TB04/TB05 4/4 PASS**; conditional **TB03 PASS** with B's early commit and A callback invoked twice. TB04 and TB05 again observed callback reexecution (`calls=2`). Each fresh third-tab native IndexedDB inventory now returned **exactly the scenario-specific database**, with `entry:3`, `info:2` in that target; the Sembast semantic observer independently found one flight, one revision, one outbox and the expected digest. The result closes the previously OPEN *exact-target raw oracle CI execution* subgate, **not** physical durability, product restore or remote authority. Two distinct successful commits demonstrate bounded repeatability but not a statistical reliability claim. The next valuable evidence boundary is product-owned owner/deletion admission and crash/UNKNOWN commit outcomes, followed by Safari/managed-iPad validation.


### SOURCE / CHANGE WATCH — upstream contract and durability limits rechecked 2026-10-28

- The [exact upstream Sembast Web 2.4.6 package documentation](https://pub.dev/packages/sembast_web/versions/2.4.6) explicitly says concurrent cross-tab transactions **may rerun the transaction callback**, and describes in-memory state, IndexedDB persistence and BroadcastChannel coordination. The executed TB03/TB04/TB05 traces now independently instantiate that stated failure mode in Chrome; they do not establish its frequency or every browser's behavior.
- The [package catalog](https://pub.dev/packages/sembast_web/versions/2.4.6%2B1) now exposes `2.4.6+1`. This is a **version CHANGE WATCH**, not a recommendation to update LogMate or proof that behavior changed. Direct-version comparison and lockfile/reproducibility are separate Engineering gates.
- [MDN IndexedDB usage](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) and [IDBDatabase.transaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction) distinguish a completed transaction and readback from physical flush/OS-power-loss durability. A native raw API inventory still shares the same browser storage failure domain.
