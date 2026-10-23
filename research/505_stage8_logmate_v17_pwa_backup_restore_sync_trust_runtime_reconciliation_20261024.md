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
