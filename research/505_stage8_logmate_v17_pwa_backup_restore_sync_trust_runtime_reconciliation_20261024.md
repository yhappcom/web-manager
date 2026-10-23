# 505 — Stage 8 LogMate capability-v17 PWA backup/restore, Sync trust and browser evidence reconciliation

Date: 2026-10-24 (Asia/Seoul)  
Status: **INTEGRATED SOURCE/EXECUTION-EVIDENCE CHECKPOINT — PWA RELEASE HOLD / CURRENT-MAIN RUNTIME OPEN**  
Owner: **Track E — Web Architecture, Security & Operations**. Track A owns browser/storage mechanics; C owns execution oracles; B and D consume state/claim implications. Web Manager coordinates, not a sixth track.

## 0. Executive decision and evidence boundary

**MINTTAP DECISION:** The earlier 504/30-store browser handoff must not be used unchanged against LogMate current `main`. As of this review, canonical LogMate `main@5ad78167cb97d6846ed7b5f866151d2a080dcc88` has merged F1 local Sync persistence, capability **v17**, and B1 **Format v2 / 37 stores**. The old v16 **Format v1 / 30 stores** remains an explicit legacy import/migration contract, not the current export shape. A v17 restore deliberately changes destination-local replica/Sync authority; blindly comparing all stores after excluding only replica identity is a false oracle.

**VALIDATION:** GitHub connector read of both repositories, current branch refs, commit comparison, source, tests, PR #19 and CI job steps. This run updated three **Web Manager-only Engineering proposals** to current source and source-level invariants. No Flutter/Chrome process, PWA artifact, managed iPad, Hosting, Sync server or product deployment was executed; no LogMate file was modified. A local direct GitHub download attempt was blocked by DNS, so the revised Python reporter fixtures were **not rerun**. Previous reporter 25/25 synthetic outcomes remain historical for unchanged checker logic, not a new runtime claim.

**Gate:** Stage 8 applied Security/Privacy/Trust; Track E highest-consequence bottleneck; A/C runtime dependencies; Production validation **OPEN**, PWA release **HOLD**. F1's local persistence improvement is not equivalent to remote Sync or installed-PWA safety.

## 1. Why the previous evidence became stale [HISTORY / PROBLEM / CONTRADICTION]

Previous 504 research and the 2026-10-24 30-store census pinned LogMate `main@59cd171176c58b598a4db55d128ffd21d406e862`. Between that pin and this run, `main` advanced by **12 commits** to `5ad78167` (GitHub compare API). PR **#19**, F1 local Sync persistence, was **merged and closed** at 2026-10-23 16:42:17 UTC; its merge commit is current main. The earlier `docs/evidence/sync-f1-acceptance-closure.md` still says “PR #19 remains Draft” and “must not be merged automatically.” This is now **stale documentation**: actual GitHub PR state outranks a historical pre-merge planning sentence. The document's F1-R03 **NOT VERIFIED** boundary remains meaningful and is **not** invalidated by merge.

- **SOURCE:** https://github.com/yhappcom/logmate/commit/5ad78167cb97d6846ed7b5f866151d2a080dcc88
- **SOURCE:** https://github.com/yhappcom/logmate/pull/19 (merged, 2026-10-23)
- **SOURCE:** https://github.com/yhappcom/logmate/blob/5ad78167cb97d6846ed7b5f866151d2a080dcc88/docs/evidence/sync-f1-acceptance-closure.md
- **CONTRADICTION:** old main's 798 PASS / 4 Golden FAIL / 1 SKIP at run 39881725421 is historical; it must not be labeled the latest current-main execution verdict. The exact integrated F1 branch at `03fb6db6` has successful Core run **39987013844** (all substantive job steps green). **No GitHub Actions run with head SHA `5ad78167` was returned** by the head-SHA query during this review. Branch-green is valuable predecessor evidence, not current merge-SHA proof.
- **SOURCE:** https://github.com/yhappcom/logmate/actions/runs/39987013844
- **SOURCE:** https://github.com/yhappcom/logmate/actions/runs/39881725421

The following unchanged Git blobs were checked at both old and new main: `tool/pwa_precache.dart`, `.github/workflows/data001-pwa-artifact-validation.yml`, `.github/workflows/data001-browser-persistence-validation.yml`, `firebase.json`, `web/manifest.json`. Therefore F1's persistence merge **does not close** the 504 NORMAL artifact custody, Hosting projection, Worker generation, Safari/managed-iPad or old browser workflow gaps. This is blob-identity evidence, not a fresh runtime failure.

## 2. Data-contract inventory [SOURCE / FOUNDATION → PRACTITIONER]

The repository defines `_lbkStoreRegistry` with **30** legacy stores (**28 String keys, 2 integer keys**), and `_syncLbkStoreRegistry` as those 30 plus **seven String-key Sync stores**: `logmate_sync_state_v1`, `logmate_sync_operation_bindings_v1`, `logmate_sync_receipts_v1`, `logmate_sync_applied_identities_v1`, `logmate_sync_applied_cursor_v1`, `logmate_sync_record_heads_v1`, `logmate_sync_holds_v1`. Thus v17 export is **37 stores = 35 String + 2 integer**.

| Backup route | Source capability | Format | Store count | Operational interpretation |
|---|---:|---:|---:|---|
| Historical v16 export, current v17 import | 16 | 1 | 30 | Authentic legacy bytes; migration initializes unverified Sync basis without invented server authority |
| Current v17 export and import | 17 | 2 | 37 | Includes Sync evidence stores, but restore rebinds to a new destination replica and fences source apply authority |
| Unsupported version/capability/store list | any unsupported | other/mismatch | invalid | Reject before destination mutation; no silent coercion |

**SOURCE:** `lib/repository/logbook/sembast_logbook_repository.dart` lines ~220–271, 420–598, 5803–5865; `whole_ledger_backup.dart` (`formatVersion=1`, `syncAwareFormatVersion=2`); `local_database_capability_codec.dart` (`legacySyncPersistenceVersion=16`, `currentVersion=17`).

**Security principle:** The LBK `snapshotDigest` is unkeyed SHA-256 over canonical JSON; it detects accidental/tampered bytes against the supplied digest but **does not authenticate the creator, establish current owner authorization, or encrypt sensitive flight records**. An adversary able to replace both payload and digest is not stopped by the checksum. `verifiedOwnerUid` is a caller-provided validation input whose provenance must be established at the integration boundary; do not call it proof of server-authenticated ownership without an actual identity/provider contract.

## 3. Restore is a trust transition, not a byte-for-byte clone [SOURCE / SYNTHESIS]

Current `exportWholeLedgerBackup` requires READY capability, a matching unlocked bound owner and no deletion lock; it emits Format v2 with a registry and digest. `restoreWholeLedgerBackup` checks manifest/version/digest/row keys, requires a fresh unclaimed staging database, performs writes in a transaction, preserves a new CSPRNG destination replica identity, and leaves the owner **locked**. It then calls `_resetRestoredSyncTrust`:

1. Previous source Cursor and Applied Identity rows are retained as **recoveryRequired HOLD evidence**, not installed as destination apply authority.
2. Destination Sync State `originReplicaId` becomes the destination's replica, `streamBindingStatus='unbound'`, `remoteBaselineStatus='unverified'`; prior Sync State is nested as historical `restoredSourceState` when present.
3. Format v1 (30-store) restore creates a fresh Sync State and v17 capability inside the staging transaction, without fabricating receipt/cursor evidence.
4. Failed/invalid restore and injected after-write exception must leave destination unchanged; successful restore must not unlock automatically.

**TRANSFER VALIDATION:** `test/repository/logbook/whole_ledger_backup_test.dart` already compares a rich host/native v2 fixture's source and destination store maps after excluding `logmate_local_replica_v1` and `logmate_sync_state_v1`, then **separately asserts** destination Sync State's new replica and unverified remote baseline. The current browser proposal previously excluded only the replica; this is wrong under v17. A passing source/destination equality check over Sync State would actually contradict the required trust reset.

**MINTTAP DECISION:** Do not replace source authority with destination authority by copying Sync State wholesale. For a browser test, assert the *expected transformation* rather than raw equality for intentional trust fields, and assert unchanged canonical record/outbox/Custom/Draft evidence separately. HOLD evidence must not be misrepresented as an ACK or a proven remote cursor.

**DEPENDENCY:** Engineering D006 is canonical for operation identity, retry, idempotency, ACK and conflict semantics; Web Manager owns the browser/restore/release boundary only.

## 4. Migration, binding and browser evidence [SOURCE / ADVANCED]

- The authentic 41,794-byte v16 Format v1 fixture `test/fixtures/f1_v16_populated_format_v1.lbk` is pinned in the F1 evidence file with SHA-256 `3c90c6cacd300aeaad87aaff7529ddddb15949e3b8319436992364cef5b41873`. Host migration tests retain legacy store bytes except capability marker; **nine record Outbox + five Custom Outbox rows** become **14 HOLD rows**; no fabricated Receipt/Cursor/Applied Identity. Fault injection before v17 publication preserves capability 16 and all 37 pre-migration inspected stores. These are source/test-reported host results, **not Chrome results**.
- F1 creates an immutable eligible operation Binding in the same local transaction as record/revision/outbox for eligible cases; it rejects conflicting digest and holds unsupported/ambiguous Custom intent. A Binding marked `eligibleProven` is **local canonical payload evidence**, not remote acceptance.
- `test/repository/logbook/sembast_web_reopen_test_browser.dart` now checks Sync State and Binding across IndexedDB **connection close/reopen**. F1 documentation reports a local Chrome run; exact integrated branch CI is green. **Neither constitutes browser-process restart, 37-store B1 Chrome restore, PWA Worker upgrade or iPad validation**.
- F1-R03 remains **NOT VERIFIED**: no authenticated server Receipt validation or Push/Pull/Remote Apply/remote ACK. PR merge is a code governance event, not an authorization proof.
- The unchanged `data001-browser-persistence-validation.yml` still pins Flutter 3.38.7 and only feature/data001-domain push; it does not automatically validate current main. Existing Web Manager browser CI proposals remain **review-only**, not installed.

**CONTRADICTION register:** `37 registered` ≠ `37 populated semantic fixtures`; `B1 host PASS` ≠ `Chrome B1 PASS`; `Chrome database reopen` ≠ `browser process restart`; `local Binding eligible` ≠ `server Receipt authenticated`; `merged PR` ≠ `current-main CI run`; `LBK checksum valid` ≠ `LBK publisher trusted`; `source replica preserved in backup` ≠ `destination replica authorized as source`.

## 5. Engineering handoff reconciliation completed [MINTTAP DECISION / VALIDATION]

Updated in **Web Manager only**:
- `research/handoffs/whole_ledger_backup_browser_test_PROPOSAL.dart`: pin current main v17, expect Format v2/37 stores and one Sync Binding, assert restored owner remains locked, destination Sync State is unbound/unverified and points at destination replica, Receipt/Cursor empty, and exclude intentionally rewritten Sync State from byte-parity comparison. The fixture remains deliberately minimal (one synthetic Flight/Outbox).
- `research/handoffs/browser_b1_whole_ledger_workflow_PROPOSAL.yml`: pin current main and exact renamed 37-store test.
- `research/handoffs/test_browser_reopen_result_gate.py`: rename the expected test in synthetic reporter fixtures. The oracle implementation itself is unchanged.

**VALIDATION LIMIT:** Connector source inspection and deterministic text-contract reconciliation only. Revised Dart has **not** been compiled or run. The Python fixture rename has **not** been rerun; a direct runtime fetch from the container failed DNS resolution. Do not carry forward a new “25/25 executed” claim. Engineering must run `dart format`, analyzer, pinned Flutter Chrome, machine-result oracle and actual test assertions on the exact implementation SHA. The existing Chrome proposal still lacks rich semantic parity and browser-process restart.

## 6. Next execution packet — not another paper-only primer [VALIDATION / C OWNERSHIP]

Use the **current v17 code** and separate tests into explicitly bounded envelopes:

| ID | Test and exact oracle | Required provenance | Current verdict |
|---|---|---|---|
| V17-01 | Real Format v2 export includes 37 exact registered stores, typed keys and digest | source/toolchain/Chrome version, full test result | NOT_EXECUTED |
| V17-02 | Rich Flight + Simulator + revisions + deleted/restore + Custom + baseline/page + Draft/receipt + Outbox semantic readback | non-sensitive synthetic fixture, expected store counts and semantic hashes | NOT_EXECUTED |
| V17-03 | Fresh staging restore keeps new replica, locks owner, resets Sync State to unbound/unverified | source/destination sanitized state diff | NOT_EXECUTED |
| V17-04 | Source Cursor/Applied Identity evidence becomes HOLD, not destination authority | before/after sanitized cursor/hold counts | NOT_EXECUTED |
| V17-05 | Actual v16 Format v1 fixture imported on Chrome and upgraded to v17 without invented receipt/cursor | verified fixture digest, browser-safe fixture delivery | NOT_EXECUTED |
| V17-06 | Digest-valid duplicate keys, malformed row/registry, wrong owner and unsupported version reject without mutation | per-case snapshot + error category | NOT_EXECUTED |
| V17-07 | Fault after multiple store writes aborts atomically; retry succeeds | exact before/after 37-store snapshots | NOT_EXECUTED |
| V17-08 | Browser process terminates after committed write; **new process with retained profile and identical origin** reads the same data | two process IDs, profile identity, origin, committed marker, readback | NOT_EXECUTED |
| V17-09 | Process terminates during write/migration; no partial capability publication or fabricated Sync authority | fault timing, previous capability, row/cursor counts | NOT_EXECUTED |
| V17-10 | Old-active/new-waiting Worker update and interrupted precache preserve unsynced v17 data, client assignment and old shell | exact NORMAL worker/assets, two-generation interleaving, offline readback | NOT_EXECUTED |
| V17-11 | Safari tab vs Home Screen vs managed Web Clip: independent storage/backup/reopen/recovery | iPadOS/WebKit, mode, MDM profile, real external .lbk restore | NOT_EXECUTED |
| V17-12 | Quota failure, storage eviction, denied persistence, cache retirement and restored backup | separate failure causes, backup independent of origin | NOT_EXECUTED |
| V17-13 | No local Binding/HOLD/backup/Worker event becomes remotely acknowledged without authenticated server Receipt | negative state transitions, no remote adapter assumption | NOT_EXECUTED |
| V17-14 | Verified NORMAL artifact → archive → fresh download → Hosting preview byte/MIME/scope proof | SHA, workflow, inventory, served bytes and config | NOT_EXECUTED |

**Process-restart protocol (Track A/C):** Do not use `database.close(); database.open()` in one browser test as proof. Run a controlled two-phase browser harness using a **persistent user-data directory**, a **stable origin**, and a deterministic synthetic fixture. Phase 1 writes and waits for committed readback, records a sanitized marker and closes the **browser process**; Phase 2 starts a **new browser process** with the same profile/origin, reads the marker and full semantic fixture, and proves no re-seeding occurred. Add separate abrupt termination during a transaction and a normal quit. New private/incognito profile, different port/origin, tab reload, or worker restart alone is a different envelope and must not be counted as process-restart persistence. Keep test-only hooks out of production authority and never upload real flight records.

**Safety ordering:** Verify exact current-main CI + browser runtime first; then NORMAL custody and Worker upgrade, then physical Safari/managed iPad. If a new source contradiction emerges, amend this domain artifact instead of opening another micro-study. A browser PASS cannot certify WebKit or MDM.

## 7. PWA platform and cross-track implications [STANDARDS / OPERATIONS]

**SOURCE:** IndexedDB can persist application data across sessions, but shutdown can abort outstanding transactions; use a transaction boundary and independent recovery. MDN `Using IndexedDB`: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB (checked 2026-10-24). MDN `StorageManager.persist()`: https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist (checked 2026-10-24); persistence request may be denied and is not an independent backup. WebKit storage-policy documentation: https://webkit.org/blog/14403/updates-to-storage-policy/ (checked 2026-10-24); origin-level eviction is a distinct risk from quota write rejection. Platform/OS/MDM support is CHANGE WATCH, not a universal guarantee.

| Track | Relative depth / pressure | Ownership and transfer |
|---|---|---|
| **E** | Highest consequence; source model matured, current-main release/backup/ACK evidence incomplete | Own v17 trust-reset, backup custody, privacy, recovery authority, Worker/update/rollback release HOLD |
| **A** | High prerequisite pressure; generic browser mechanics mature, actual persistent-profile/iPad execution OPEN | Own IndexedDB connection vs process, origin/profile isolation, Service Worker generation and WebKit storage differences |
| **C** | High execution pressure; host/branch evidence improved, merged-main and device proof OPEN | Own real CI, 37-store semantic oracle, process restart, fault injection, accessibility/performance evidence |
| **B** | State architecture known, user/AT tests OPEN | Own `local saved` vs `backup verified` vs `restored locked` vs `remote ACK` task language; consume Design Studio W121 |
| **D** | Web measurement mature, installed-PWA acquisition/runtime proof OPEN | Own provenance-minimized test metrics and non-misleading install/offline/Sync claims; consume Marketing 438 |

**TRANSFER VALIDATION:** Design Studio W121 explicitly prioritizes exact-source runtime over new pre-runtime manifests (https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md). Engineering D006 owns retry/ACK/conflict (https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md). Marketing 438 conditionally recommends first-release PWA ads exclusion (https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md). No cross-specialist discipline is duplicated.

**CHANGE WATCH:** Flutter/Dart browser test machine reporter; current main and CI SHA; PWA generated Worker and Hosting config; Safari/iPadOS install/display/storage identity; MDM/Web Clip restrictions; WebKit quota/persistence; any new Sync adapter's authenticated Receipt and conflict policy; changes to backup registry/format/schema. Do not assume unattended device-to-device Sync, background work, advertising, storage permanence, or iPad installation rights.

## 8. Stop rule and next major checkpoint

This integrated checkpoint resolves the **stale-source test contract** and makes current v17 restore semantics explicit. The next highest-value question cannot be answered by more generic source synthesis: **Does Engineering-run current-main Chrome v17 37-store semantic restore survive process restart, and can a NORMAL PWA be independently archived/served/upgraded without losing unsynced data on the actual target browser/device?** Until the exact runtime evidence exists, keep Production validation OPEN and PWA release HOLD. Preserve the F1-R03 remote-authenticated-Receipt boundary separately.

## 9. Adjacent high-value contradiction — old v16 client vs migrated v17 database [SOURCE / CONTRADICTION / OPEN]

The F1 merge changes **database capability**, while the unchanged owned Service Worker can retain and serve older build-specific shell assets to an existing client (`tool/pwa_precache.dart` `clientBuilds` / `currentBuildId`, lines ~602–643). These are independent lifecycles. **No `skipWaiting`** protects takeover ordering, but does not establish a global application-schema single-writer guarantee.

Source-level two-version audit (2026-10-24):
- Old `main@59cd1711` `LocalDatabaseCapabilityCodec.currentVersion=16`; current `main@5ad78167` uses **17**. The old decoder rejects an unsupported v17 capability on a **fresh open**, and old canonical `_commitLedgerMutation` calls `_requireReadyCapability` inside its transaction. This supports a **bounded** fail-closed claim for canonical mutation after the marker changes.
- However, both versions expose public legacy direct `create/update/delete/restore` repository entry points whose inspected transaction bodies do **not** call `_requireReadyCapability` before writing active/deleted/revision/Outbox rows. An **already-open** v16 repository instance could therefore have a different downgrade-fence behavior from a fresh v16 open or canonical commit. This is a **source-level bypass candidate**, not evidence that production UI calls these methods, that an old tab and new tab share the exact Sembast transaction behavior, or that a damaging mutation has occurred.
- The v17 migration test validates one-process host transaction rollback and legacy byte preservation, but not concurrent old v16 JavaScript and new v17 JavaScript tabs against the same IndexedDB origin. The old Worker client-pinning test is likewise not a mixed-capability database writer test.

**MINTTAP DECISION / DEPENDENCY:** Before treating v16→v17 installed-PWA upgrade as data-safe, Engineering must (a) audit actual production callers of the four legacy direct entry points; (b) prove every **reachable** old-version mutation is fenced when v17 is published, including already-open tabs, not merely newly opened repositories; (c) run a two-tab, two-binary, same-origin deterministic migration/write interleaving; (d) preserve unique unsynced data before any destructive recovery; and (e) define update UX when a stale client cannot safely write. Adding a guard only to new v17 code cannot retroactively protect already-deployed v16 binaries. A product fix/rollout policy is **OPEN** pending Engineering and actual runtime evidence.

**New runtime oracle V17-15 (NOT_EXECUTED):** Keep a v16 app tab and its repository open, open v17 in another tab and complete v16→v17 migration, then attempt both (i) old canonical `commitLedgerMutation` and (ii) each reachable old direct CRUD entry point. Record whether the operation is rejected before any 37-store mutation; compare all data and Sync trust state after browser process restart. Repeat with reversed timing and interrupted migration. A fresh old-v16 open must reject the v17 marker, but that is not a substitute for the already-open case. This is a new meaningful Stage 8 execution dependency, not a confirmed product defect.

**TRANSFER:** A owns old/new tab and Worker control mechanics; E owns schema downgrade-fence and data preservation; C owns interleaving oracle; B must present a safe stale-client/read-only/recovery state; D must not claim seamless updates without this evidence. Design Studio W121's exact-runtime stop rule remains applicable.

## 10. Caller-reachability and two-version platform-boundary audit — 2026-10-24 [SOURCE / CONTRADICTION / TRANSFER VALIDATION]

**Scope and provenance:** Re-read Web Manager canonical instructions/track model/roadmap/status/index, study 505, Design Studio W121, Engineering D006 and Marketing 438. Rechecked LogMate `main@5ad78167cb97d6846ed7b5f866151d2a080dcc88` against predecessor `59cd171176c58b598a4db55d128ffd21d406e862`. The GitHub comparison reports 12 commits and **21 changed paths; none under `lib/application/`, `lib/screens/`, `lib/app/` or `lib/debug/`**. Therefore those unchanged production-layer source files are a bounded common caller snapshot for both v16 and v17. This is a static source review, not compiled whole-program call-graph proof.

### 10.1 Direct mutation reachability narrowed [SOURCE / SYNTHESIS]

The audit retrieved and lexically inspected **61 Dart files** spanning all 57 `lib/application/logbook/` and `lib/screens/` files in the current tree plus `lib/app/logmate_app.dart`, `lib/app/session_gate.dart`, `lib/application/account_deletion_coordinator.dart` and `lib/debug/persistence_acceptance_harness.dart`. Inspected calls to `.create(`, `.update(`, `.delete(`, `.restore(`, `commitLedgerMutation(`, and references to `LocalMutationIdentity`/`LocalMutationResult`. The matches included **four explicit canonical application mutation call sites** and no observed calls to `LogbookRepository.create/update/delete/restore` in these 61 files:

| Production application seam | Exact source line (current main) | Observed write route |
|---|---|---|
| `ManualFlightCreateService.create` | `lib/application/logbook/manual_flight_create_service.dart:60` | `_repository.commitLedgerMutation(planning.plan)` |
| `ManualFlightNonStructuralUpdateService.update` | `lib/application/logbook/manual_flight_non_structural_update_service.dart:78` | `_repository.commitLedgerMutation(...)` |
| `ManualFlightStructureChangeService.commit` | `lib/application/logbook/manual_flight_structure_change_service.dart:131` | `_repository.commitLedgerMutation(preview.plan)` |
| `ManualPageManagementService.commit` | `lib/application/logbook/manual_page_management_service.dart:53` | `_repository.commitLedgerMutation(preview.plan)` |

`ManualFlightCreateBindingService` invokes a *service* `.create`, and `ManualFlightEditBindingService` invokes a *service* `.update`; these are **not** direct repository CRUD calls. `orientationController.restore()` is UI orientation cleanup, not record restore. The source explicitly documents canonical create/update services as not falling back to simple CRUD. All four direct repository CRUD methods remain in the public `LogbookRepository` interface and both Sembast implementations, so the API surface exists even when inspected app callers do not use it.

**MINTTAP DECISION — risk refinement:** Revise the earlier phrase “reachable production bypass” to **“unguarded legacy public repository API, with no direct production call observed in the bounded 61-file application/screen audit; actual stale-tab bypass reachability remains OPEN.”** This was the initial bounded 61-file UI/application audit; **§11 extends the static scan to all 169 current `lib/**/*.dart` files**, including auth, presentation, platform and repository. It still cannot certify dynamic dispatch, test/external consumers, future versions or runtime safety. A lexical scan is not a Dart analyzer/call graph. Do not declare a confirmed vulnerability or silently remove the release validation gate.

### 10.2 Mechanism check: guard and capability publication [SOURCE / FOUNDATION → ADVANCED]

- Both v16 and v17 `SembastLogbookRepository.create/update/delete/restore` begin a transaction but **do not call `_readCapability` or `_requireReadyCapability` inside their own bodies**. Their shared `_advanceLedgerDataGeneration` helper only reads and writes the generation counter; it does not supply an implicit capability check. The four paths mutate active/deleted records, revision and Outbox and advance data generation.
- Both versions' canonical `_commitLedgerMutation` calls `_requireReadyCapability(transaction)` before its record/structure changes. The old v16 decoder rejects a v17 capability marker. Therefore an already-open v16 client using the inspected **canonical** mutation path should reject a published v17 marker *if the transaction observes that marker*. Browser interleaving and retry behavior still require execution evidence.
- The v17 migration's `_prepareDatabase` handles the v16 marker, validates prior canonical state, requires Sync stores empty, classifies legacy outbound evidence and publishes the v17 marker within the migration transaction. This is a **logical application capability marker**, not proof that the underlying browser's native IndexedDB schema version was incremented.
- Exact browser opener: `lib/repository/logbook/sembast_database_opener_web.dart` calls `databaseFactoryWeb.openDatabase('logmate_ledger')`. `pubspec.lock` pins **`sembast_web 2.4.6`**. The package documentation describes IndexedDB-backed, in-memory Sembast state, BroadcastChannel cross-tab updates and transaction callback reruns under concurrent changes. A browser's IndexedDB `versionchange`/`blocked` events are for **native IndexedDB database-version/schema operations**, not a guaranteed event for an application record containing `schemaVersion:17`. Therefore an `onversionchange` listener cannot be assumed to fence this v16→v17 logical migration.
- Service Worker old/new control and page JavaScript schema compatibility are separate from both application capability and native IndexedDB schema version. `skipWaiting`/activation ordering does not itself serialize repository mutations. A service-worker controller switch does not prove a stale page's JavaScript was replaced.

**Authoritative sources checked 2026-10-24:** [IndexedDB usage and blocked/versionchange](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB); [IndexedDB versionchange event](https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/versionchange_event); [Sembast Web 2.4.6 cross-tab and transaction limitations](https://pub.dev/packages/sembast_web/versions/2.4.6); [W3C Service Workers current specification](https://w3c.github.io/ServiceWorker/). **CHANGE WATCH:** actual compiled Sembast Web transaction replay, cross-tab notification timing and installed Safari/managed-iPad differences must be observed, not inferred from generic docs.

### 10.3 Falsifiable two-binary acceptance campaign [C EXECUTION OWNERSHIP / E RELEASE AUTHORITY]

Pin two **real, separately built** app bundles to the exact v16 and v17 source SHAs. Use one controlled **same-origin** HTTPS test host with immutable versioned asset paths, a single persistent browser profile, a non-production synthetic ledger and deterministic phase markers. Record origin (scheme/host/port), browser/build hashes, application capability, native IndexedDB version *separately*, Sembast package, client/worker controller, transaction attempts/retries, source/destination row counts and sanitized semantic digests. Do not substitute hot-reload, one JS bundle with a mocked version constant, two origins, or two independent profiles for two-binary shared-origin proof.

| Case | Required interleaving and negative oracle | Expected evidence boundary |
|---|---|---|
| M01 | v16 canonical commit, v17 migration, v16 canonical commit again in already-open tab | Post-migration old canonical write rejected **without** any changed 37-store payload/Sync authority; actual result NOT_EXECUTED |
| M02 | v16 direct `create` in old already-open tab after v17 marker | Observe rejection **or** prove actual write reachability; absence of observed app callers is not runtime proof |
| M03 | Repeat M02 for direct `update`, `delete`, `restore` with valid preconditions | Per-operation transaction/row diff; never conflate no-op precondition failure with capability fencing |
| M04 | Start old transaction before migration, pause at controlled boundary, release after new version attempts migration | Establish serial ordering, whether migration blocks/retries, and post-commit capability; no partial state |
| M05 | New v17 migration begins while v16 tab holds repository open; old tab never closes | Distinguish Sembast logical marker migration from native IndexedDB `versionchange`/blocked; do not assume tab eviction |
| M06 | New tab migrates, then old tab reloads or freshly opens v16 bundle | Old decoder must reject v17; separate from already-open old instance |
| M07 | Concurrent old/new mutation with Sembast cross-tab transaction retry | Count callback attempts and effects; no duplicate revision/Outbox, no unguarded external side effects |
| M08 | Old-controlled Worker shell and new waiting/activated Worker overlap with v17 DB | Record client/controller/build mapping, offline old-shell behavior and write rejection; Worker lifecycle ≠ schema fence |
| M09 | Browser process exits and relaunches with same profile and origin after mixed-generation test | No re-seeding; 37-store semantic readback, new replica/Sync trust invariants, no fabricated remote Receipt |
| M10 | Inject migration fault before v17 marker publication, then retry | v16 remains usable/consistent if rollback; no half-published v17 or orphaned Sync authority |
| M11 | Explicit sign-out/locked owner and stale-tab action during/after migration | No unauthorized local mutation or automatic unlock; exact auth/currentness remains separate |
| M12 | Run on Safari tab, installed Home Screen and managed Web Clip **separately** | Each mode's storage/update/recovery evidence remains its own gate; Chrome PASS does not transfer |

**PASS definition:** Exact built source and browser provenance, relevant tests actually executed, expected rejection for every **reachable** stale write after v17 publication, unchanged canonical/Outbox/Sync state on rejected actions, no loss of unique unsynced records, and a fresh-process readback. **FAIL:** an old client can mutate the migrated ledger contrary to current capability/owner policy, or a migration partially publishes trust/capability. **BLOCKED/UNKNOWN:** only host tests, synthetic model, missing two-binary host, blocked browser runtime, or a precondition failure that does not exercise the intended guard. Test-only pause hooks must never be shipped as production authority.

### 10.4 Architecture alternatives and release decision [MINTTAP DECISION / DEPENDENCY]

1. **Preferred invariant:** Every supported **material** repository mutation is capability/owner-fenced **inside the same atomic transaction** that writes canonical state, including future legacy compatibility routes. This can harden future builds, but **cannot retroactively patch already-deployed v16 JavaScript**.
2. **Transitional containment:** Preserve unsynced local data and allow safe read/export/recovery where supported; prevent unsafe writes from stale clients; coordinate version handoff with explicit user-visible update/reopen instructions. Do not force reload, clear storage, unregister Worker or delete caches before proving data survival. A UI “update required” banner without a write-side guard is insufficient.
3. **Alternative rollout:** Delay v17 logical migration until incompatible v16 clients are quiescent, or use a genuinely version-isolated data namespace with explicit verified migration. Both have liveness/storage/recovery costs; neither is declared implemented. Worker-client visibility is not an authoritative inventory of every dormant client.
4. **Rejected shortcuts:** “native IndexedDB versionchange will close old tabs”; “new Worker is active so old JS cannot write”; “new v17 guard protects old v16 code”; “one fresh v16 open failed so already-open v16 is safe”; “no direct UI calls means public API cannot be reached.” Each confuses different boundaries.

**Five-track allocation:** E remains owner of release/owner/backup/trust policy; A owns app capability vs native IDB version vs Worker control and origin mechanics; C owns two-binary runtime interleaving, rollback and semantic oracles; B consumes the stale/read-only/export/reopen state contract without inventing completed Sync; D records privacy-minimized rejection/recovery metrics and does not promote an untested seamless-update claim. Design Studio W121's runtime-evidence stop rule applies; Engineering D006 retains operation/retry/ACK/conflict ownership; Marketing 438's first-release PWA-ad exclusion remains conditional transfer, not Web Manager advertising policy.

### 10.5 Actual execution status and adjacent-question stop check [VALIDATION / OPEN]

**VALIDATION performed:** GitHub source/tree/blob/compare review; bounded 61-file caller scan; both v16/v17 direct-method and canonical-commit inspection; shared helper guard inspection; exact Sembast Web opener and lockfile inspection; current GitHub Actions head-SHA query. At 2026-10-24 the `main@5ad78167` workflow-run query returned **zero runs**; last visible `main` Core run `39881725421` belongs to **old `59cd1711` and failed**. These are API observations, not a claim that no external/manual validation exists.

**NOT_EXECUTED:** Flutter/Dart compile, Chrome two-binary M01–M11, Safari/managed iPad M12, NORMAL custody/Hosting, authenticated remote Receipt. No LogMate source changed. The immediately adjacent valuable question—whether the inspected production callers use the unguarded CRUD paths—has been narrowed by source audit. The remaining decisive question is **actual old-tab/new-tab execution**, which cannot be answered responsibly with another paper-only primer. Stage 8 remains active, Track E primary bottleneck, Production validation OPEN, PWA release HOLD.

## 11. Whole-lib caller census and priority correction — 2026-10-24 [SOURCE / VALIDATION / CONTRADICTION]

**Adjacent-question completion:** Rather than stop at the initial 61-file sample, enumerated the exact `main@5ad78167` Git tree and read the remaining **108** `lib/**/*.dart` files in connector batches. The full census is **169/169** `lib` Dart paths: 61 initial application/screen/app/debug, 31 additional auth/presentation/platform/entry/utility, 37 domain, and 40 repository (including the already-inspected Sembast implementation). All fetches completed without reported errors. Lexically inspected calls to `.create/update/delete/restore`, `commitLedgerMutation` and legacy mutation identity/result types; differentiated service/UI calls from the repository interface.

**Observed:** In the current `lib` tree, the four application mutation seams enumerated in §10 call guarded `commitLedgerMutation`; the four unguarded `LogbookRepository` legacy CRUD methods are **declared and implemented**, but **no direct repository CRUD call site was observed in any of the other 167 Dart files** (the repository interface and implementation account for the two definition files). Additional lexical hits were model type declarations, service-layer `.create/.update` calls and orientation `.restore`, not repository CRUD. GitHub compare confirms none of the 61 app/screen files changed between the old v16 and new v17 refs; the remaining code was inspected at current v17, not every historical old-v16 blob. This is a **complete current-`lib` static lexical census**, not a compiled interprocedural proof, nor a scan of test/tools/third-party packages.

**Independent corroboration of API role:** Inspected five representative repository test files. `test/repository/logbook/sembast_logbook_repository_test.dart` invokes direct `repository.create` (e.g. lines 81, 109), `update` (line 120), `delete` (line 144), and `restore` (line 150), demonstrating the unguarded API is exercised by **tests**. The inspected browser reopen and whole-ledger backup tests use canonical `commitLedgerMutation` for record writes. This does not prove *all* test-only or external call sites have been enumerated.

**Risk reclassification (MINTTAP DECISION):** The highest-value immediate issue is **not** a demonstrated live stale-tab direct-CRUD exploit. It is a **latent public API capability-fence gap** with no observed current product-`lib` caller, plus an **unexecuted two-binary canonical stale-tab/migration interaction**. Engineering should keep the four public legacy methods fail-closed in future compatibility designs, but prioritize current-main Chrome v17 semantic recovery, NORMAL artifact custody and actual two-generation PWA runtime over additional hypothetical direct-CRUD primers. A future implementation may remove/restrict legacy methods only after reviewing tests, migration compatibility and consumers; Web Manager does not authorize product edits.

**Verdict:** `169/169 current lib static files reviewed` = **PASS for bounded lexical inventory only**; `production direct legacy CRUD caller observed` = **NO within inspected current lib**; `all reachable writes are runtime capability-fenced` = **OPEN**; `M01–M12 Chrome/iPad` = **NOT_EXECUTED**; `Production validation` = **OPEN**; `PWA release` = **HOLD**. This resolves the adjacent static reachability question without manufacturing a runtime PASS.


## 12. Executable mixed-generation evidence-admission gate — 2026-10-24 [SOURCE / VALIDATION / TRANSFER / OPEN]

**Checkpoint purpose:** The 169-file lexical caller census narrowed the suspected old-client bypass but did not establish a real Chrome interleaving. To prevent an Engineering trace from being promoted to a false product PASS, Web Manager now supplies an **executable evidence-consistency gate** and deterministic negative controls. This is a concrete next-step handoff, not another generic Service Worker primer.

**Pinned SOURCE:** historical v16 commit `59cd171176c58b598a4db55d128ffd21d406e862` (GitHub commit resolution, 2026-10-24); v17 `5ad78167cb97d6846ed7b5f866151d2a080dcc88`. Source-owned `tool/pwa_precache.dart` still pins shell resources by client/build; this is separate from Sembast's logical capability. W3C Service Worker lifecycle: https://w3c.github.io/ServiceWorker/spec/service_worker/ ; MDN IndexedDB transaction/shutdown caveats: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB ; Playwright persistent-profile process boundary: https://playwright.dev/docs/api/class-browsertype . Reviewed 2026-10-24. A persistent profile is a test fixture, **not a guarantee of disk flush, data permanence or WebKit equivalence**.

**Artifacts (Web Manager only):**
- `research/handoffs/mixed_generation_trace_gate.py` — deterministic parser/oracle for **one bounded** M01/M06/M09 canonical-write + restart trace. It requires two exact source SHAs, two build hashes, same secure origin/profile, distinct simultaneous tab identities, v17 migration to 37 stores, old-v16 canonical write rejected with no 37-store digest change, nonempty unsynced state, zero fabricated remote Receipt/authority, a browser-process exit and a different process with identical readback.
- `research/handoffs/test_mixed_generation_trace_gate.py` — 16 synthetic contract tests covering one structurally consistent envelope and 15 negative perturbations. Local Python `unittest`: **16/16 expected**; `py_compile` PASS. These tests exercise the **Python trace oracle**, not Chrome, Flutter, IndexedDB or product safety.

**Critical admission distinction [CONTRADICTION]:** A JSON trace can be fabricated. Even a structurally consistent trace returns `TRACE_CONSISTENT_UNVERIFIED`, **never `PRODUCT_PASS`**. A zero process exit code means only the shape checks passed. The synthetic reference test intentionally uses invented browser/process evidence and therefore cannot attest runtime. Independent CI run URL, actual binary provenance, raw machine logs, process/profile evidence, source-to-build mapping, and reviewer verification remain mandatory. Instrumented test builds must be labeled `test_instrumented` and cannot silently substitute for independently inventoried NORMAL deploy bytes.

**Required Engineering execution sequence [DEPENDENCY / C owner]:**
1. Compile two **real** pinned v16/v17 Flutter web binaries; archive build inventories and hashes. Expose an explicitly test-only, non-production mutation/inspection bridge if normal UI cannot deterministically exercise the repository. Independently review instrumentation diff against normal runtime; never install the bridge in production.
2. Serve both binaries under one HTTPS origin (or localhost secure-context exception), with **different URL paths and correct Flutter base/asset resolution**. Confirm the old tab remains on the old JavaScript bundle while the new tab migrates the **same exact Sembast database name**. Path separation is a DB-interleaving fixture; it **does not** by itself exercise the production root-only Worker fetch/activation policy.
3. Pre-seed a synthetic nonempty unsynced ledger; record exact 37-store normalized digest **after** v17 migration, and record owner lock/unlock state separately. Attempt old v16 `commitLedgerMutation` from the **already-open** old tab. Verify explicit rejection, identical pre/post digest and no invented remote Receipt. Then exit the browser process; relaunch with a persistent profile and identical origin, without reseeding, and re-read semantic state.
4. Independently run the legacy CRUD reachability variant, migration interruption/reversed timing, Worker old-active/new-waiting update, and NORMAL artifact/Hosting checks. This first trace gate **does not** certify M02–M05, M07–M08 or M10–M12, nor Safari/managed iPad. A fresh old-v16 open rejection is a different test from an already-open v16 tab.
5. Collect privacy-minimized evidence (no flight records, UID, access token, cookie, raw backup, personal data). Archive exact source/build/test-harness SHAs, environment, run ID, Chrome version, process IDs, sanitized digest, independent test logs, and the trace-oracle output. Any missing real execution yields `NOT_EXECUTED/UNKNOWN`, not a PASS.

**Alternative/failure judgment [E owner]:** If the old canonical writer is fenced, this does **not** prove the four legacy direct entry points are safe. If an old write succeeds after v17 publication, do not repair by clearing origin storage, force-reloading all clients or invoking Worker rollback: preserve unsynced data and escalate to Engineering's atomic capability-fence/rollout decision. If the browser process cannot be launched, keep runtime validation OPEN; a synthetic trace gate PASS is not a workaround. If instrumented binaries differ in relevant mutation logic, require normal-binary/real-UI replication before release promotion.

**Five-track transfer:** E owns release HOLD and data-preserving recovery authority; A owns origin/profile, worker-vs-database generation and secure-context mechanics; C owns falsifiable execution/oracle and independent evidence admission; B consumes distinct stale-client read-only/recovery vs remote-ACK states using Design Studio W121; D consumes only aggregate provenance/rejection metrics and cannot promote an unverified seamless-update claim. Engineering D006 remains canonical for Sync ACK/retry semantics; Marketing 438's PWA-ad exclusion remains a separate conditional handoff.

**Stage/gate reconciliation:** The repository's sequential 12-stage curriculum is historically marked complete; this work is **Stage 8 security/trust application and expert maintenance**, not a claim the entire curriculum has reverted to Stage 8. No production runtime result was obtained. **Production validation OPEN; PWA release HOLD.** Adjacent static question resolved: a concrete false-positive-resistant trace contract now exists; the next decisive step requires real two-binary Chrome and independently verified NORMAL custody, not further speculative paper tests.

## 13. Evidence-admission false-positive hardening — 2026-10-24 [SOURCE / CONTRADICTION / VALIDATION / MINTTAP DECISION]

**Scope:** This is an integrated continuation of §12, not a new micro-study or an assertion that Chrome/LogMate passed. At run start re-read canonical Web Manager `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, this study, recent Web Manager and LogMate commits, Design Studio W121, Engineering D006 and Marketing 438. Confirmed Web Manager pre-run `main@9592fd9c` and LogMate read-only `main@5ad78167`; no new LogMate source commit was visible. No other specialist repository was changed.

### 13.1 Concrete false-positive classes [SOURCE / SYNTHESIS]

The §12 trace gate already refuses to return `PRODUCT_PASS`, but source inspection found additional ways a *structurally consistent* envelope could be misread as a valid capability-fence observation:

1. **Source commit ≠ executed artifact:** Historical event field `binary_sha` actually held a 40-character Git source commit, while only the top-level envelope contained 64-character build hashes. An event could claim the correct source commit while referring to the wrong built JavaScript. Preserve the legacy field for compatibility, explicitly label it a *source claim*, and require separate per-event `build_sha256` values for old-open, migration, stale-write and restart readback.
2. **Any rejection ≠ capability rejection:** The previous oracle accepted any nonempty error code on a rejected old write. A locked owner, invalid request or unmet precondition could produce the same apparent no-mutation outcome. Require an explicit *recorded* `preconditions_validated=true`, `capability_marker_observed=17` and `rejection_class=capability_version_guard`. Engineering must still independently map that classification to the real v16 decoder/exception and raw logs; a self-reported label is not evidence of the branch taken.
3. **Two tab IDs ≠ simultaneous live old tab:** Require old tab marked open at initial observation and `old_tab_still_open=true` during both migration and stale attempt. A recorder can lie, so process/tab lifecycle logs remain independent evidence.
4. **New process ID ≠ preserved browser profile:** Require recorded `all_tabs_closed=true`, `profile_reused=true` and `reseeded=false` in addition to distinct process IDs and identical origin/profile identifiers. This is a stronger admission contract, not proof of an OS-level exit or persisted disk flush.
5. **Python boolean ≠ count:** Python treats `False == 0` and `isinstance(True, int)` as true. Strict nonnegative integer checks now reject booleans for remote Receipt and unsynced counts.
6. **HTTPS string ≠ bare trustworthy origin:** URL validation now rejects embedded userinfo and invalid ports; browser version requires a four-part numeric claim. The verifier does not establish that the hostname is under test operator control, nor that the observed TLS/HTTP response came from the intended server.
7. **SHA-256 text ≠ semantic completeness:** Matching 64-hex-character digests can still be fabricated or computed over incomplete stores. Independent 37-store typed-key inventory, deterministic normalization, before/after raw fixtures and no reseeding must be reviewed outside the trace gate.

**CONTRADICTION:** An apparent `TRACE_CONSISTENT_UNVERIFIED` with a locked-owner error is not evidence that the v16 client observed and rejected the v17 capability. A source commit in an event is not a build digest. An application capability v17 marker is not an IndexedDB native database version. These distinctions are not interchangeable.

### 13.2 Durable code changes and exact local validation [VALIDATION]

Updated **Web Manager only**:
- `research/handoffs/mixed_generation_trace_gate.py` — fail-closed admission on the seven classes above; blob `2ed3926e84374b009590b21d61e3a7122bc08c07`.
- `research/handoffs/test_mixed_generation_trace_gate.py` — **33 deterministic unittest cases** (16 original, 16 targeted adversarial additions, one deterministic 1,000-envelope malformed-type robustness test); blob `3809187370f1740fda14fef4df308fb4bda6a158`.

**Actual execution:** GitHub connector content was reproduced *byte-for-byte* in a disposable Python 3.13.5/Linux environment. Local Git blob SHA-1 calculations matched **both exact GitHub blob IDs** above. `python -m unittest -q test_mixed_generation_trace_gate.py` returned **33/33 PASS**; `python -m py_compile *.py` PASS. A separate seeded 10,000-envelope mutation probe returned **zero uncaught exceptions** (not a claim of complete fuzz coverage). Explicit negative probes for wrong artifact hash and owner-lock error classification returned `INVALID`; the synthetic reference returned only `TRACE_CONSISTENT_UNVERIFIED`.

**Evidence tier:** This is **exact committed Python-oracle execution**, not Chrome, Flutter, two-binary, IndexedDB, PWA, Safari, managed-iPad or production validation. Even 33/33 PASS cannot authenticate the JSON recorder or prove a release-safe schema migration. A `TRACE_CONSISTENT_UNVERIFIED` verdict is deliberately non-promoting.

### 13.3 Platform standards and cross-track integration [SOURCE / TRANSFER VALIDATION]

- **Track A (browser):** `launchPersistentContext(userDataDir)` retains a browser storage profile and closing its context closes that browser; Playwright warns against using the user's default Chrome profile and simultaneous browser instances on one data directory. The test must use a dedicated non-personal profile, close phase 1 before launching phase 2, and independently prove same-origin/same-profile readback. SOURCE: https://playwright.dev/docs/api/class-browsertype (checked 2026-10-24).
- **Track A/E (storage/security):** IndexedDB transaction completion, transaction durability hints, actual OS/power-loss persistence and independent backup are distinct claims. The `strict`/`relaxed`/`default` durability option is a user-agent hint, not an EFB data-retention guarantee. SOURCE: https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability (checked 2026-10-24).
- **Track A/E (Worker):** Service Worker client control and `clients.claim()` may change fetch interception without replacing a page's already-loaded JavaScript or enforcing its application-schema marker. SOURCE: https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim (checked 2026-10-24).
- **Track C (quality):** Own the executed evidence, exact build-to-event mapping, precondition-positive/guard-negative proof, semantic digests, restart and fault-injection oracles. The synthetic trace gate is an auxiliary check, not a replacement for the runner.
- **Track B (UX):** If a stale client cannot safely mutate, require explicit read-only/export/update/reopen/recovery states; never present a failed capability check as a remote Sync failure or authenticated ACK. Consume Design Studio W121's exact-runtime/AT/human validation gate.
- **Track D (discovery/analytics):** Retain only aggregate rejection class, build cohort and outcome metadata; do not log flight content, owner IDs, cookies, tokens or raw backups, and do not market seamless offline update or Sync based on a synthetic oracle. Marketing 438's first-release PWA ad exclusion remains conditional and separate.
- **Track E (primary bottleneck):** Own source-to-build custody, capability/owner trust fence, no-destructive-recovery rule, migration/rollback decision and release HOLD. Engineering D006 remains canonical for retry/idempotency/remote Receipt semantics.

### 13.4 Next decisive evidence and stop check [OPEN / DEPENDENCY / CHANGE WATCH]

The adjacent question “Can the existing trace validator accidentally admit wrong-build or unrelated-error evidence?” is now **resolved at the bounded Python contract level**. Another directly adjacent valuable question—whether malformed nested JSON can crash the validator—was exercised with deterministic 1,000-case regression plus 10,000 additional mutation probes. No runtime PASS is inferred.

**Next evidence-changing step:** Engineering must build actual pinned v16/v17 Flutter bundles; independently inventory NORMAL and instrumented artifacts; run M01/M06/M09 in a real Chrome persistent-profile, same-origin, two-tab sequence with a genuine capability-fence exception and an independently logged process restart; then run richer 37-store B1, Worker update/Hosting, and Safari/Home Screen/managed-iPad cases separately. Preserve unsynced data before any repair. If the exact runtime or test bridge is unavailable, record `NOT_EXECUTED` rather than synthetic success. **Production validation OPEN; PWA release HOLD.**

**CHANGE WATCH:** exact LogMate main SHA, generated Flutter bootstrap/Worker, Sembast Web version and cross-tab retry behavior, Playwright/Chrome profile policies, IndexedDB durability/storage eviction, WebKit/iPadOS/MDM execution context, and authenticated remote Receipt semantics.


## 14. Same-origin mixed-generation browser-lab execution attempt and environmental blocker — 2026-10-24 [SOURCE / VALIDATION / CONTRADICTION / OPEN]

**Question / operational competency:** Can the previously specified M01/M06/M09 browser boundaries be exercised with an independently launched browser, rather than merely asserting self-reported JSON? Which parts can be tested in this execution environment without implying LogMate product safety? The answer is a concrete reusable browser lab, a verified **execution blocker**, and a sharper separation of platform mechanics from product proof.

### 14.1 Exact provenance and five-track allocation [SOURCE / DEPENDENCY]

Re-read Web Manager `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, this 505 study and recent commits. At run start Web Manager `main@f5078f9e87409b604b2d2d0e8956e0d6a92eee66`; LogMate read-only `main@5ad78167cb97d6846ed7b5f866151d2a080dcc88` (historical v16 `59cd171176c58b598a4db55d128ffd21d406e862`). Checked Design Studio `W121` (runtime execution over another pre-runtime manifest), Engineering `D006` (logical operation, retry, ACK and conflict authority), and Marketing `438` (conditional native Manual Sync ad proposal; PWA ad-free default, production HOLD). These specialist boundaries are consumed, not rewritten.

| Track | Stage 8 evidence maturity / dependency pressure | Allocation and owned decision |
| --- | --- | --- |
| **E** | Highest product-loss and release-authority risk; real artifact/device evidence OPEN | **Primary:** separate synthetic lab, real runtime and production admission; no-destructive-repair, NORMAL custody and rollback governance |
| **A** | Foundational supplier; platform semantics sourced but LogMate old/new Worker behavior unexecuted | Browser origin, native IndexedDB vs application capability, SW client control, install/storage partition |
| **C** | High execution pressure; prior Python oracle tests PASS but no product browser proof | Browser lab, falsifiable guarded/unguarded controls, actual process-restart oracle and independent logs |
| **B** | State architecture mature; human/AT validation OPEN | Distinguish stale-read-only, local saved, backup verified, restored locked and remote ACK; Design Studio W121 owns presentation validation |
| **D** | Analytics/source provenance mature; PWA acquisition/continuity proof OPEN | Sanitized cohort/trace outcomes, no promotional seamless-update/offline/Sync claims without real runtime |

### 14.2 First principles and failure modes [SOURCE / SYNTHESIS]

AppCache's declarative application cache lacked a sufficiently controllable request/update lifecycle; the Service Worker model supplies a scoped event-driven fetch intermediary and separately managed Cache Storage. **That is not a database transaction or a JS hot-reload mechanism.** W3C Service Workers defines client/control, activation, registration scope and update as distinct concepts. The active Worker that intercepts a page's later fetches need not equal the generation of JS already loaded into that page. `clients.claim()` changes control; it does not retroactively re-evaluate the page's JS. `skipWaiting()` can cause a new Worker to handle old-page fetches and must not be assumed safe for incompatible assets.

IndexedDB names are scoped to an origin, and an IDB database has its own *native* version. The LogMate `LocalDatabaseCapabilityCodec.currentVersion=17` is a **logical Sembast application marker**, not a native `indexedDB.open(name, version)` upgrade. A native `versionchange` event cannot be promoted to proof of v16→v17 LogMate logical capability fencing. Multiple tabs at the same origin may use the same database name while running different JS generations. A transaction-scoped application capability check is a different control from Worker activation.

**Current product source transfer:** LogMate's `web/index.html` uses a Flutter build-time `<base href="$FLUTTER_BASE_HREF">`; the source Worker generator uses its registration scope and a version catalogue; `web/manifest.json` uses relative `start_url` and `standalone`; `sembast_database_opener_web.dart` opens the fixed `logmate_ledger` database. A two-build `/old/` + `/new/` lab on one origin is appropriate to isolate database-generation interaction **only after** verifying compiled base href/asset paths and that both versions truly open the same logical DB. It is **not** a production-root Worker update test: path/scope mapping and the source-owned cache catalogue differ. For the actual release Worker, independently test root navigation, reserved Auth routes, old/new client assignment, cache promotion, offline restart and rollback.

Primary references reviewed 2026-10-24:
- W3C Service Workers editor's draft (2026-09-17): https://w3c.github.io/ServiceWorker/
- MDN `ServiceWorkerContainer.controller`: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controller
- MDN IndexedDB usage and transaction shutdown caveats: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- Playwright `launchPersistentContext`: https://playwright.dev/docs/api/class-browsertype
- WebKit storage policy (Safari 17-era baseline, platform-version CHANGE WATCH): https://webkit.org/blog/14403/updates-to-storage-policy/

### 14.3 Durable executable lab, test sequence and evidence [VALIDATION / CONTRADICTION]

New **Web Manager-only** research handoffs:
- `research/handoffs/pwa_mixed_generation_browser_lab.py`: a disposable localhost HTTP server + Playwright persistent-profile Chromium runner. Its **synthetic** old/new JS versions share one plain IndexedDB native-version-1 database, first with logical marker 16 and then 17. It deliberately tests a guarded stale writer (rejected/no mutation) and an unsafe writer (mutates after migration), changes a **synthetic** Worker from V1 to V2 using `skipWaiting/clients.claim`, checks that old page JS remains generation 16, closes the persistent browser context, and reopens the same profile to read the synthetic payload. **The unsafe writer is an intentional counterexample, not LogMate code.** No real personal/flight records or production origin.
- `research/handoffs/test_pwa_mixed_generation_browser_lab.py`: seven stdlib HTTP/source contract tests; source tests alone cannot assert JS execution or storage semantics.

**Actually executed in this run (Python 3.13.5, Playwright 1.57.0, Chromium 144.0.7559.96, Node 22.16):**
1. `python -m unittest -q test_pwa_mixed_generation_browser_lab.py` → **7/7 PASS** for localhost old/new routes, shared JS/native-version fixture, changed Worker response, cache headers, and network marker.
2. `python -m py_compile` both files → PASS; `node --check` extracted embedded application JS → PASS.
3. **Attempted real** `launch_persistent_context` with a disposable profile and `page.goto(http://127.0.0.1:<ephemeral>/old/)` → **`net::ERR_BLOCKED_BY_ADMINISTRATOR` before application load**. The container's managed Chromium policy includes `URLBlocklist: ["*"]`. No attempt was made to disable/bypass organizational policy. Thus **zero** browser-side IDB/Worker/migration assertions executed. The error is an **execution-environment navigation blocker**, not a LogMate failure or evidence of a PWA incompatibility.

The committed Python/HTTP fixture and syntax are source/host validated. The 16 browser assertions in the script are **NOT_EXECUTED**; do not label them 17 PASS. A later `BROWSER_LAB_PASS_NOT_PRODUCT_PASS` in a permitted browser would still prove only this synthetic native-IDB model, not Flutter, Sembast, LogMate, iPadOS, MDM or physical data durability.

### 14.4 Independent evidence ladder and adversarial counterexamples [MINTTAP DECISION / DEPENDENCY]

**T0** source/standards and product static pin → **T1** server fixture + Python/JS syntax → **T2** real Chromium synthetic lab → **T3** exact two compiled LogMate v16/v17 binaries with independently verified artifact inventories and application guard provenance → **T4** current NORMAL PWA bytes, root Worker/Hosting, rich 37-store v17 semantic B1 recovery, process restart and negative/fault variants → **T5** Safari tab/Home Screen and *policy-envelope-matched managed company iPad*, plus authenticated remote Sync ACK if claimed. **No tier is transitive.** Current run reaches T1 only for the new lab, while prior bounded host/product source evidence remains as separately pinned studies.

Critical negative controls for Engineering:
1. An old v16 tab that *loads fresh* after v17 migration is not the same as an **already-open** v16 tab.
2. A locked owner or invalid operation rejection is not a capability-version guard.
3. Distinct `/old/` and `/new/` paths do not imply separate origin storage, but two different ports/hosts do.
4. Root Worker control of an old page does not mean old JS or local Sembast code has been replaced.
5. A native IDB `versionchange` is not a LogMate logical v17 migration.
6. Matching counts or a self-reported 37-store digest does not prove all 37 typed-key/value semantics, source-to-build custody or no re-seeding.
7. `IDBTransaction.complete` / browser process restart / power-loss durability / independent `.lbk` backup / tested restore are separate.
8. `local saved`, unsynced outbox, request sent, remote Receipt, remote convergence and backup are separate; no synthetic Receipt may be invented.
9. A Chromium localhost secure-context exception does not certify real HTTPS, Safari/WebKit storage partitions or managed Web Clip policy.
10. A Python/HTTP PASS, Playwright navigation policy error or synthetic browser PASS must not silently promote a NORMAL release gate.

**EFB/managed-iPad decision:** Keep unique offline data non-destructively, preserve export/recovery options and distinguish storage persistence from independent backup. The company iPad installation route (Safari tab, Home Screen web app, managed Web Clip), profile/storage partition, background execution, hotspot/peer connectivity, MDM restrictions, and foreground/manual Sync opportunities each require independent version-specific evidence. No unattended peer Sync, automatic cross-device communication or App Store bypass entitlement is inferred.

### 14.5 Stop check / next meaningful checkpoint [OPEN / CHANGE WATCH]

The adjacent valuable question was pursued beyond source review: a browser runner was constructed, its HTTP/JS/Python surfaces tested, and actual Chromium navigation attempted. **The environment blocks the first navigation by administrative policy.** Continuing with additional synthetic-only trace gates would not resolve the product risk. The next responsible checkpoint is Engineering-owned, policy-permitted real Chrome with two pinned Flutter builds and genuine Sembast capability-guard instrumentation, followed by NORMAL custody/Hosting and managed-iPad acceptance. No LogMate source or external specialist repository was changed.

**Gate:** Stage 8 security/trust application remains active; historical Stages 1–12 curriculum gates remain complete. **Track E primary bottleneck; Production validation OPEN; PWA release HOLD.** CHANGE WATCH: LogMate HEAD, Flutter/Worker build pipeline, browser policies and Playwright version, IndexedDB/Sembast cross-tab behavior, Safari/WebKit storage policy, managed-iPad MDM configuration and Sync Receipt implementation.
