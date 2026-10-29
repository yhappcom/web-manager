# 529 — Stage 8: PWA owner-deletion, backup provenance and managed-iPad custody

**Checkpoint:** 2026-10-30 KST. **Lead:** Track E (Web Architecture, Security & Operations); Track A browser mechanics, C independent validation, B truthful recovery IA, D public claims. **Evidence:** SOURCE / SYNTHESIS / DEPENDENCY / TRANSFER VALIDATION / CONTRADICTION / OPEN / CHANGE WATCH. **No product/device PASS.**

## 1. Why this is the bottleneck [HISTORY / PROBLEM]

Studies 527–528 mapped origin isolation and update/schema custody. Hosted Chrome 156 research fixture PS01–PS11 has 11/11 PASS SYNTHETIC, including graceful separate-process persistent-profile reopening, but no real LogMate owner lifecycle, external backup file custody or managed EFB result. The next higher-value threat: account A's evidence must not survive terminal deletion in a form that account B can export, restore, use for Sync, or mistake for B's authority on a shared browser profile. This is simultaneously privacy, trust, recoverability and PWA lifecycle work.

Read-first authority: Web Manager AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research index, studies 527/528 and latest main commits; [LogMate MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md), [Design Studio W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md), [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md), [Engineering D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md). Marketing independently escalated the same conditional source discrepancy at 2026-10-30 06:33 KST. This Web Manager study owns PWA/origin/MDM custody and release-gate implications, not Marketing's acquisition or Engineering's implementation discipline.

## 2. Source-level registry/deletion mismatch [SOURCE / REPLICATION]

**Source:** [LogMate main 9cc0cd432a317d5dfebbe90e318fb219e53e024a](https://github.com/yhappcom/logmate/commit/9cc0cd432a317d5dfebbe90e318fb219e53e024a), [sembast_logbook_repository.dart](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/sembast_logbook_repository.dart), blob **021d9001ae1240a824c5df570fb679597edc3875**, read-only 2026-10-30. Directly compared the 30 base registry entries and seven Sync entries with the 29 store symbols in the terminal deletion drop loop.

| Source path | Observed mechanism | Boundary |
| --- | --- | --- |
| Lines 227–271 | Full backup registry = **30 base + 7 Sync = 37** | Export inventory, not deletion inventory |
| Lines 1070–1125 | Terminal deletion explicitly drops **29 base** stores, reinitializes database and records completed deletion for A | **No explicit drop** of Replica or seven Sync stores |
| Lines 4819–4840 | Current capability publication ensures Replica/Sync; existing Sync State is not reinitialized | Existing state may survive |
| Lines 3378–3394 | Owner write changes Sync State ownerUid, not binding/baseline or nested source evidence | Owner field rewrite is not full rebind |
| Lines 1673–1694 | Fresh owner B binding path does not itself clear residual Sync stores or completed A deletion marker | Actual B startup outcome not executed |
| Lines 422–481 | Export checks READY/unlocked matching owner/deletion lock, serializes 37 stores with digest | No nested Sync owner-reference validator in export path |
| Lines 486–556, 5830–5997 | Restore checks manifest, registry, nested Sync references, fresh destination, new Replica, reset trust | Stronger restore checks, but no Files I/O |

**Eight explicitly undropped stores:** logmate_local_replica_v1; logmate_sync_state_v1; logmate_sync_operation_bindings_v1; logmate_sync_receipts_v1; logmate_sync_applied_identities_v1; logmate_sync_applied_cursor_v1; logmate_sync_record_heads_v1; logmate_sync_holds_v1.

**Replication method:** extract literal names from base/Sync registries; resolve the 29 StoreRef symbols in the terminal-wipe loop to their declared names; calculate the set difference. This reproduces the eight-store mismatch independently of Marketing's conclusion. **STATIC SOURCE REPLICATION ONLY**: it does not prove actual A-to-B leakage, successful deletion saga, a server write, or a production incident.

**Conditional hazard:** If A has nonempty Sync binding/receipt/cursor/hold evidence, terminal wipe completes, B can bind on the same DB, and B can export, residual A-scoped nested evidence may enter B's backup or make later restore fail closed. A completed A deletion record may interfere with B's subsequent deletion. Earlier startup/export refusal is also possible. The full branch matrix is **NOT RUN**; no user-data disclosure is asserted.

## 3. Five independent trust boundaries [SYNTHESIS / THREAT MODEL]

1. **Principal authority:** Firebase UID A/B, local owner, Replica and browser origin are different identities. Same device or installed icon is not a UID proof. Logout, pending deletion and terminal erasure have different contracts.
2. **Ledger custody:** Sembast transaction, logical capability, 37-store snapshot, wipe, owner rebind, receipt and cursor are separate state machines. A missing drop is a concrete source discrepancy but must be exercised before labeling a runtime defect.
3. **PWA container:** Safari tab, user-added Home Screen web app and MDM Web Clip require separate storage and navigation observations. URL equality does not imply automatic local-data migration or shared backup files.
4. **External file:** returned LBK string, Blob URL, download, Share Sheet completion, user-selected Files destination, independent byte readback and empty same-UID restore are separate milestones. Digest verifies bytes, not source authority.
5. **Device policy:** MDM can control Web Clips, Safari, content filtering and managed/unmanaged document flow. A company EFB can prohibit a personal Files/AirDrop target; such refusal must be reported rather than falsely marking backup successful.

Counterexample: 11/11 package-level Sembast tests can pass while application-specific deletion omits seven stores. Likewise, a valid in-memory LBK checksum cannot establish survival after origin eviction or MDM file restrictions.

## 4. Authoritative browser/OS evidence [SOURCE / CHANGE WATCH]

- [WebKit storage policy (2023-08-10)](https://webkit.org/blog/14403/updates-to-storage-policy/): IndexedDB/CacheStorage/Service Worker data face quota/eviction; persistent mode is heuristic. Home Screen standalone receives browser-app quota treatment. The 60%/80% browser and 15%/20% other-app limits are upper policy ceilings, **not** guaranteed free bytes or managed-device retention.
- [WebKit Safari 17.0 (2023)](https://webkit.org/blog/14445/webkit-features-in-safari-17-0/): documented web-app installation copies cookies in described circumstances but **not other local storage**. Do not assume Safari-tab IndexedDB is transferred to an installed container.
- [WebKit Safari 26.0 (2025)](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/): on iOS/iPadOS 26, adding a website to Home Screen defaults to **Open as Web App** even without a manifest or service worker; user may disable. Earlier manifest-only installability statements are not universal current Safari rules. This does not override airline MDM policy.
- [Apple managed Web Clips](https://support.apple.com/en-ca/guide/deployment/depbc7c7808/web): full-screen and non-removable options, Safari restriction interactions and MDM vendor-dependent configuration. Managed Web Clip is not automatically equivalent to a user-installed PWA.
- [Apple Managed Open In](https://support.apple.com/en-gb/guide/deployment/depaa73a4973/1/web/1.0): managed-to-unmanaged document transfer and AirDrop classification can be restricted. The actual airline profile is **UNKNOWN**.
- [MDN Web Share](https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API) and [canShare](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare): secure context, transient user activation and per-file capability; share completion is not independent Files readback.
- [MDN anchor download](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a): download behavior varies by browser/settings and URL scheme. [MDN OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) is origin-private, not an external user-retained backup. Do not assume showSaveFilePicker or a Share Sheet destination exists on managed Safari.
- [W3C IndexedDB](https://www.w3.org/TR/IndexedDB/) specifies transactions but not LogMate's owner/37-store deletion, Files custody or MDM rules.

## 5. Release-blocking acceptance matrix [VALIDATION DEFINED — NOT RUN]

Use disposable synthetic Firebase test UIDs A and B, an approved test backend, a full 37-store fixture with A-owned nested Sync canaries, no production flight data. Pin exact product commit, compiled Web build/lockfile, served origin/headers, iPadOS/browser version, installed container, MDM policy, pre/post snapshots and redacted Operation/receipt fingerprints.

| ID | Scenario | Independent oracle |
| --- | --- | --- |
| OC01 | Fresh A, 37-store snapshot | UID A, Replica and Sync defaults pinned |
| OC02 | Seed A binding/receipt/cursor/hold | Known nested A refs and hashes |
| OC03 | Interrupt each A deletion saga phase | Resumable, no premature success or unlock |
| OC04 | Complete A deletion; reopen offline | No stale actionable A user/Sync authority |
| OC05 | Authenticate B, create ledger | Fresh B state or explicit safe refusal; no A nested evidence |
| OC06 | B export and decode LBK | 37-store manifest, no foreign-owner references; digest not authentication |
| OC07 | Save LBK outside browser and read from Files | Exact bytes/digest independently re-read |
| OC08 | B same-UID empty-stage restore | New Replica, 37-store semantics, safe Sync trust; wrong UID/corrupt/nonempty reject |
| OC09 | B deletion after A completion | No stale A request blocker; no A/B residue |
| OC10 | Old/new Web clients, two tabs | No mixed-owner write, unsafe downgrade or false Worker-ready |
| OC11 | iPadOS 26 Safari tab versus Home Screen | Separate containers, no presumed IDB transfer |
| OC12 | Managed full-screen Web Clip/Safari restricted | Actual launch/offline/file flow under enrolled MDM |
| OC13 | Managed Open In denies external destination | Truthful policy-denied state, not backup-success |
| OC14 | Storage pressure, termination, restart | Preservation or truthful recovery; no persist() guarantee |
| OC15 | Diverged offline then Manual Sync | No background sync; B-only authority and valid receipts |
| OC16 | VoiceOver/large text/keyboard/cancel | Announced save/export/readback/restore/sync states and recoverable errors |

Negative controls: wrong UID, stale nested restoredSourceState, malformed canonicalPayload, corrupt digest, absent Files destination, MDM deny, eviction, concurrent tabs and interrupted deletion. Every result requires exact provenance and classification NOT RUN / NON-EXECUTION / FAIL PRODUCT / PASS PRODUCT / PASS DEVICE-MDM. Package-level synthetic green cannot be promoted.

## 6. Five-track allocation and peer transfer [DEPENDENCY / TRANSFER VALIDATION]

| Track | Maturity / pressure | Ownership |
| --- | --- | --- |
| **E — lead** | Stage 8 source mature, owner-deletion/backup trust unresolved; highest potential severity | P0 conditional risk, security/operations release gate |
| **A** | Chrome package proven, Safari 26/MDM storage not executed | Origin/storage/file API/install capability matrix |
| **C** | 11/11 hosted synthetic PASS, no product/iPad/VoiceOver | OC01–OC16 semantic and negative-control adjudication |
| **B** | Design Studio W121 Stage 3 practice, human task evidence open | Truthful deletion, file saved, readback, restore and Manual Sync states |
| **D** | Marketing D8/D9 claims HOLD | No guaranteed erasure/backup/seamless PWA/automatic EFB sync claims |

**TRANSFER VALIDATION:** Marketing's owner-lifecycle warning is independently reproduced at store-list level; Engineering owns executable regression and any fix; Design Studio owns interaction visuals. **CONTRADICTION:** 37 stores exportable does not imply 37 erased; checksum-valid does not mean owner-safe; Safari 26 installable does not mean MDM permits install, Files export or data retention.

## 7. Operational judgment, blockers and next proof [MINTTAP DIRECTION / OPEN]

**P0 validation recommendation, not a code authorization:** Engineering should run **OC01–OC09 first**, especially A → delete → reopen → B → export → external Files readback → empty same-UID restore → B deletion, with stale A Sync canaries. Treat the 29/37 explicit terminal-wipe parity as a **release-blocking question**, not a proven runtime incident. Any fix must preserve resumable deletion, owner isolation, correct Replica/Sync initialization and honest recovery; Web Manager must not patch LogMate.

After owner isolation, run OC11–OC16 on physical Safari tab, Home Screen PWA and managed Web Clip separately with actual MDM restrictions. If external file custody is prohibited, do not substitute origin-private storage or imagined unattended sync.

**OPEN:** no approved paired product Web builds, no executable A/B deletion saga, no independently retained LBK Files readback, no enrolled iPad/MDM policy, no physical offline/VoiceOver acceptance. **Gate: Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

**Adjacent-question check:** owner-wipe/backup asymmetry, Safari 26 install changes and MDM custody were integrated in this checkpoint. Next promotion requires Engineering-owned product fixtures and actual enrolled-device evidence, not another generic synthetic Sembast green check.
