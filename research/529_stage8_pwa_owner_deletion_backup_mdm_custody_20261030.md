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


---

## 8. Completed A deletion marker and B second-deletion liveness [SOURCE / REPLICATION, 2026-10-30]

**Higher-confidence conditional source-path finding:** The earlier section described the completed-A marker as possibly interfering with B. The exact pinned repository chain gives a stronger deterministic branch **if** A completes, the same database is reused, B binds, and no intervening repair/reset occurs. This is **not** a product-runtime result.

- [LogMate main@9cc0cd43, repository lines 1007–1034](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1007-L1034): requestAccountDeletion(B, requestB) requires B-bound owner and permits a new request only when phase=none; for any non-none phase, it accepts only exact same UID and requestId replay.
- [Terminal wipe lines 1071–1125](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1071-L1125): the deletion-state store is among 29 dropped stores; fresh initialization occurs; **then completed(A, requestA) is deliberately written back** within the transaction. It is not merely an accidentally undropped old row.
- [AccountDeletionState type](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/domain/account_deletion_state.dart) and [codec](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/account_deletion_state_codec.dart): completed is excluded from locksNormalAccess, but ownerUid and requestId are retained.
- [Owner binding lines 1674–1720](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1674-L1720): createOwnedLedger(B) and bindOwner(B) do not read or clear the completed A marker in their own transactions.
- [Coordinator](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/application/account_deletion_coordinator.dart) delegates request to repository; resume has no completed-to-none transition. [Existing coordinator tests](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/test/application/account_deletion_coordinator_test.dart) cover same-UID completion, retry and reauth mismatch, but not completed A -> B -> second deletion.

**Conditional logical result:** with persisted completed(A, requestA) and successful B binding on the same database, requestAccountDeletion(B, requestB) follows invalidInitialSetupTransition before the remote B deletion saga. This is a source-level branch deduction, **not** proof B startup is reachable, user exposure, or an observed incident. The eight undropped Replica/Sync stores are a separate discrepancy: repairing their drop parity alone does not resolve the completed-marker liveness branch.

## 9. Export / restore / second-delete are independent gates [SOURCE / CONTRADICTION]

[Export lines 422–481](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L422-L481) checks READY, matching unlocked owner B, and deletion locksNormalAccess, then serializes all 37 stores with an unkeyed SHA-256 integrity digest. Export does not invoke the recursive nested Sync owner-reference validator. Completed A is not a normal-access lock, so it need not block a later B export **if** B can bind and pass other guards.

[Restore validation lines 5830–6010](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L5830-L6010) validates manifest owner B and rejects explicit foreign ownerUid in nested Sync evidence. Restore subsequently reads the deletion marker, but the reviewed checks do not prove a completed A marker is reconciled to B. Do not claim universal restore success or failure without executing both no-Sync and seeded A-Sync cases.

| Conditional scenario | Export | Restore / B deletion | Required evidence |
| --- | --- | --- | --- |
| A completed; no residual A Sync; B binds | Shown B-owner/deletion checks can pass; completed A receipt included | B second-delete follows reject branch; B restore outcome unexecuted | Empty-Sync A -> B control |
| A completed; residual A binding/receipt/cursor/hold with explicit or nested UID | No nested-owner precheck at export | Foreign-owner restore can fail closed depending on exact rows; second-delete guard remains | A canaries, B LBK, empty B staging |
| B startup/binding refused elsewhere | No B export | Safe refusal possible, but B activation blocked | Full Auth/Startup trace |
| B uses genuinely independent browser origin/profile | No presumed inheritance of A state | No implied cross-container erasure or transfer | Physical container/MDM test |

**Dual failure mode:** rejecting a foreign-owner restore can be secure while revealing that an earlier accepted export cannot be restored. Export accepted, Files saved, Files independently re-read, restore owner-safe, and B can later delete are separate release oracles. The checksum proves byte integrity, not owner authority.

## 10. Generic browser reset is not a safe unreviewed repair [SOURCE / PLATFORM / CHANGE WATCH]

[W3C Clear Site Data Working Draft (2017-11-30)](https://www.w3.org/TR/clear-site-data/) specifies origin-local IndexedDB and Service Worker removal; it is a Working Draft, not current universal implementation proof. [MDN Clear-Site-Data, consulted 2026-10-30](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data) documents the storage directive clearing IndexedDB and Service Worker registrations, cookies directive extending across the registered domain and subdomains, and browser-dependent cache behavior. Current compatibility documents Safari/iOS Safari support since 17; exact directive behavior in Safari tab, installed Home Screen and managed Web Clip still needs device tests. Older mirrored compatibility pages disagree with current upstream and are not authoritative. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) and [Apple Safari data-clearing guidance](https://support.apple.com/en-us/105082) do not establish automatic clearing of all separately installed containers or independent Files backups.

**MINTTAP DIRECTION (not product authorization):** do not use a blanket Clear-Site-Data wildcard or storage directive on ordinary sign-out, account switching, public pages, Auth Action, or generic error routes. It can destroy the only offline ledger and unregister the Worker before independent backup; the cookies directive can affect sibling-domain sessions. Conversely, deleting 29 Sembast stores is not a complete per-owner deletion protocol. An approved terminal erasure design must explicitly address remote authority, all local stores, completion-receipt lifecycle, separately installed contexts, independent Files copies and user-facing outcome. A broad reset, if ever justified, requires narrowly scoped explicit consent, rollback/recovery design and physical browser/MDM tests.

## 11. Five-track allocation and specialist transfer [SYNTHESIS / DEPENDENCY]

| Track | Evidence maturity | Remaining bottleneck / work |
| --- | --- | --- |
| **E lead** | Pinned 29/37 mismatch and completed A -> B request guard; severe potential privacy/availability impact | Engineering-owned A/B execution, deletion/receipt contract, incident and recovery policy |
| **A** | W3C/MDN/WebKit origin, Worker and Clear-Site-Data semantics; hosted Chrome Sembast 11/11 synthetic | Safari tab vs Home Screen vs MDM Web Clip, actual header and storage behavior |
| **C** | Hosted package provenance and OC01–OC16 negative-control plan | Exact LogMate tests, failure injection, cross-browser/VoiceOver adjudication |
| **B** | Design Studio W121 Stage 3 practice; no physical task evidence | Truthful distinct sign-out, account deleted, local data erased, Files saved/readback and recovery states |
| **D** | Marketing D1–D9 public claims HOLD | Never promise global erasure, durable external backup, unattended EFB sync or universal install |

**TRANSFER VALIDATION:** Engineering D003 migration protocol emphasizes explicit validation before publication; apply that judgment to account lifecycle but do not implement Engineering code here. Marketing owns acquisition; Web D owns web measurement/claims. Design Studio owns visual patterns, Web B owns task/state wording. No specialist repository is modified.

## 12. Prioritized executable acceptance and negative controls [VALIDATION DEFINED / NOT RUN]

**Gate 1, Engineering-approved disposable Sembast fixture:** (a) A with empty Sync -> completed saga -> close/reopen -> B bind -> B deletion request; (b) A with nested A-owned binding/receipt/cursor/hold -> terminal deletion -> B bind -> B export -> inspect 37-store manifest -> B empty-staging restore -> B deletion; (c) failures before/after local terminal transaction and retry; (d) independent fresh B database control. Assert exact typed error, whether any B remote call was reached, no foreign-owner export, no silent reset, and preservation of legitimate same-UID resume. Use synthetic Firebase test identities, not production pilot data.

**Gate 2, exact Web/Files/MDM:** Pin commit, compiled Web artifact, Worker, served HTTPS headers, browser/iPadOS version and MDM profile. For each test, retain before/after owner/deletion/Replica/Sync snapshots, redacted canary fingerprints, external LBK bytes and independent Files readback hash. Run Safari tab, Home Screen app and managed Web Clip as distinct containers. Test offline reopen, network/identity deletion interruption, storage pressure, app-icon removal, blocked managed-to-unmanaged file export, wrong UID, corrupt checksum and two-tab races.

**Gate 3, UX and operations:** Distinguish account deletion initiated, remote deletion completed, local erasure completed, external backups still user-controlled, save requested, saved destination independently verified, restore refused and Manual Sync pending. Never equate an in-memory LBK string or Share Sheet completion with an independently retained file. Do not claim all copies erased when an external backup remains.

**Engineering handoff summary:** P0 LogMate same-profile A -> delete -> B -> export/restore -> B delete. Source confirms 29/37 explicit wipe and completed A marker retained after fresh init; if B binds, B deletion request rejects non-none marker. Verify with empty and seeded nested Sync, exact builds and before/after snapshots. This is a conditional source finding, not a product incident. Web Manager must not patch LogMate.

**Static predicate audit:** 8/8 expected source-path predicates (seven present guards and one expected absent export validator) on pinned repository/type/coordinator files, including negative export nested-owner check; **no Dart/Flutter runtime execution, no managed iPad, no real remote deletion and no external Files readback.** Production validation OPEN, PWA release HOLD.

## 13. Adjacent-question checkpoint

The added source trace resolves a material ambiguity in §7: the completed A marker is written **after** fresh initialization, while B's new deletion requires none or exact same-request replay. The browser-header analysis rejects a tempting but destructive global reset shortcut. Further material advancement now depends on Engineering-owned executable product fixtures and enrolled-device evidence rather than another generic package-level primer. No LogMate/Design Studio/Marketing/Engineering writes.

---

## 14. Material correction: completed-A blocks normal B startup before binding [SOURCE / CONTRADICTION, 2026-10-30]

The earlier conditional finding, "if B binds, B second deletion rejects a new request," remains valid for an alternate explicit binding path. It is **not the first normal account-required startup failure**.

1. [Terminal repository transaction](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1071-L1125) drops 29 stores, initializes fresh state, then **writes completed(A, requestA) back**.
2. [Account-required resolver lines 167–211](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/application/logbook/local_ledger_access_coordinator.dart#L167-L211) reads deletion **before** owner. With completed(A) and signed out, it returns AuthenticationRequired; with completed(A) and signed in B, it returns DeletionLocked **before** the createOwnedLedger(B) branch.
3. [Real SessionGate composition](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L118-L137) uses that resolver. [Render branch](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L538-L573) displays [AccountDeletionLockedScreen](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/screens/session_recovery_screens.dart#L5-L37), which says "Account deletion completed" but has no new-account or recovery action.
4. [Explicit owner-completion service](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/application/logbook/local_ledger_auth_access_service.dart) and [repository bind/create](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1674-L1720) are distinct caller paths; those repository methods do not themselves inspect completed(A). The earlier B second-delete guard is therefore a **separate conditional alternate-path hazard**, not evidence normal B startup succeeds.

| Durable marker and auth | Normal resolver result | Scope |
| --- | --- | --- |
| completed(A), signed out | AuthenticationRequired | Source-level branch |
| completed(A), signed in verified B | DeletionLocked(A) | B owner creation not reached via normal resolver |
| completed(A), auth unavailable | DeletionLocked(A) | No automatic repair |
| completed(A), B bound by alternate explicit path | DeletionLocked(A) on next startup | Separate B second-delete guard can reject; conditional |
| none, independent fresh B DB | Normal B creation path available | Control, not an authorized reset workaround |

**Test gap:** [startup coordinator tests](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/test/application/logbook/local_ledger_access_coordinator_test.dart) do not cover completed(A) followed by B account-required startup. [SessionGate widget tests](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/test/session_gate_test.dart#L109-L123) test localLocked deletion screen, not completed(A) plus B. This is a **focused coverage gap**, not a claim about all tests. No exact compiled product, live deletion or user incident has been observed.

## 15. Public deletion instructions contradict current Settings source [SOURCE / POLICY WATCH]

[Public account-deletion page source lines 22–30](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/account-deletion/index.html#L22-L30) instructs the user to open Settings and choose an account-deletion option. The [current SettingsScreen lines 25–66](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/screens/settings_screen.dart#L25-L66) instead offers Import (no-op), optional Previous Total setup and Sign out, **without a deletion action**. The [startup/auth product specification](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/docs/specs/startup-and-auth-entry-spec.md) also records deployed deletion/revocation adapters and Settings confirmation UI as OPEN. Existing [coordinator tests](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/test/application/account_deletion_coordinator_test.dart) use fake external ports.

This is a **repository-source claim/implementation contradiction**, not proof the static page is deployed, the app has passed store review, or a real user was denied deletion.

- [Google Play account-deletion policy](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en) and [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en) require both in-app and external web-request paths for in-scope account-creating apps. An email/form external request may be permissible; it does not establish an in-app action. Actual Play Console URL, served page, functioning support queue and retention disclosures are UNKNOWN.
- [Apple developer deletion guidance](https://developer.apple.com/support/offering-account-deletion-in-your-app/) requires in-app initiation for account-creating App Store apps, permits proportionate reauthentication and notes limited regulated-industry exceptions; Sign in with Apple requires token revocation. No exception or approval is presumed for LogMate.
- The public page asks for email from the associated address. Apple relay or inaccessible mailboxes could make this impractical; verify a secure alternate identity-proof route rather than assuming a failure or accepting an arbitrary email as UID authority.

**MINTTAP DIRECTION:** public statements of in-app deletion availability, complete local erasure, every installed copy erased, automatic external-backup deletion or store compliance remain **HOLD** until exact shipped UI, served page, operator process and Console evidence agree. Web Manager does not patch product UI or legal copy.

## 16. Identity-delete success before local acknowledgement [SOURCE / FAILURE ANALYSIS]

[AccountDeletionCoordinator lines 62–92](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/application/account_deletion_coordinator.dart#L62-L92) awaits the external identity-delete port and **then** persists firebaseIdentityDeleted. If remote identity deletion succeeds but a process crash or local phase-write failure occurs before that second operation, durable phase may remain remoteDataErased. Resume calls deleteCurrentIdentity(A) again. The abstract port has no specified already-deleted/ambiguous-success reconciliation.

[Firebase client delete docs](https://firebase.google.com/docs/auth/web/manage-users) require recent sign-in; [Firebase JS API](https://firebase.google.com/docs/reference/js/auth) describes deletion as signing out. [Firebase Identity Toolkit REST](https://firebase.google.com/docs/reference/rest/auth) distinguishes USER_NOT_FOUND from INVALID_ID_TOKEN. [Firebase Admin SDK](https://firebase.google.com/docs/auth/admin/manage-users) supports privileged UID deletion but reports error for an unknown UID. These are **generic API facts**, not evidence which concrete adapter LogMate ships. An arbitrary error must not be treated as successful deletion.

| External/local boundary | Ambiguous-success window | Required proof |
| --- | --- | --- |
| Provider revoke then phase advance | Revoke may succeed while phase remains reauthenticated | Same-provider retry/reconciliation without cross-UID effect |
| Remote data erase then phase advance | Remote erasure may succeed while phase remains providerRevoked | Exact UID/idempotency key and server receipt |
| Firebase identity delete then phase advance | Identity may be absent while phase remains remoteDataErased | Independently verify exact UID absent; finish local cleanup without reauth to deleted UID |
| Local wipe commit | Transaction abort vs completed marker and 37 stores | Phase/store/Sync invariant, safe retry and B liveness |

[Existing coordinator tests](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/test/application/account_deletion_coordinator_test.dart) cover fake-port normal success, remote failure before advancement and reauth UID mismatch, **not** identity-delete success followed by phase-persistence failure. No concrete adapter, exact Firebase runtime or product fault test was run.

**PROPOSED OPERATIONAL CONTRACT, not implementation authorization:** distinguish remote-data-erased, identity-deleted, local-wiped and separately installed-context completion receipts. Reconcile ambiguous remote outcomes using exact UID/request identity and minimal durable evidence; never retain raw credentials, assume an unknown-UID error proves success, or require reauth to an already-deleted UID for local cleanup. Engineering owns adapter and fault-injection implementation.

## 17. PWA cross-container deletion and honest recovery [SYNTHESIS / DEPENDENCY]

Firebase UID deletion changes **remote identity authority**, not every offline iPad's origin-private bytes. Safari tab, Home Screen web app, managed Web Clip and native device can have distinct storage and network states. A device disconnected during deletion may retain data until an approved local lifecycle/admission process runs; actual LogMate behavior is **OPEN**. Blanket Clear-Site-Data is not a safe substitute for owner-aware local deletion because it can erase an unsaved offline ledger and Worker. Independently exported LBK files remain user-controlled copies.

User-visible states must distinguish request accepted, remote erasure, identity deletion, active-device wipe, other offline-container **unverified**, external backup **user-retained**, and failed/blocked recovery. No analytics should include raw UID, flight records or backup payload. Track E owns trust/receipt/incident policy; A owns browser container semantics; C owns real device, interruption and accessibility verification; B owns web task/state requirements with Design Studio W121; D owns truthful store/search claims with Marketing D8/D9. Engineering S007/D003/Q006 owns implementation and executable regression.

## 18. Product-first acceptance packet [VALIDATION DEFINED — NOT RUN]

Extend OC01–OC16 with SL01–SL12 using disposable test UIDs, synthetic A-owned Sync canaries, exact approved build and test backend. No production pilot data or real account deletion.

| ID | Test | Independent oracle |
| --- | --- | --- |
| SL01 | Complete A; restart signed out | AuthenticationRequired; no A ledger exposure |
| SL02 | Sign in B on same DB after completed A | Resolver/UI result before owner mutation; DeletionLocked reachability |
| SL03 | Alternate verified owner completion then B deletion | Binding and new-request guard independently observed |
| SL04 | Fresh independent B DB control | B initialization without A state |
| SL05 | Identity remote success; fail local phase write | Verified exact-UID absence, safe local completion without reauth loop |
| SL06 | Revoke/remote erase success; fail phase write | Idempotent/reconciled exact-UID retry and receipts |
| SL07 | Crash/abort around terminal local transaction | 37-store/Replica/Sync classification; no false completed |
| SL08 | A empty/seeded Sync, B export and empty-stage restore | No foreign-owner data; valid 37-store same-UID restore or explicit refusal |
| SL09 | Compiled Settings versus served public page | Actual deletion route, accurate instructions, keyboard/VoiceOver |
| SL10 | External request without app/associated email access | Secure usable request path and truthful completion |
| SL11 | Safari tab, Home Screen and enrolled managed Web Clip offline | Separate container/MDM/Files evidence, not presumed global wipe |
| SL12 | Exact app build + served URL + Play/App Store operator data | In-app/external claim parity; no presumed compliance |

Every result requires source commit, compiled artifact hash, environment, redacted UID/request fingerprint, before/after state, exact failure injection, browser/iPadOS/MDM, and verdict NOT RUN / NON-EXECUTION / FAIL PRODUCT / PASS PRODUCT / PASS DEVICE-MDM. If an adapter cannot be invoked, SL05 is NON-EXECUTION, not PASS.

## 19. Five-track checkpoint [SYNTHESIS / OPEN]

| Track | Evidence and allocation |
| --- | --- |
| **E lead** | Stage 8 source evidence stronger; terminal-marker policy, identity acknowledgement and public deletion trust P0 |
| **A dependency** | Browser/Worker/storage foundation and Chrome package synthetic validated; Safari/managed container still OPEN |
| **C verifier** | Package CI provenance strong; actual product deletion/startup/Files/VoiceOver SL01–SL12 OPEN |
| **B transfer** | Design Studio W121 requires exact execution, not another pre-runtime visual spec; honest recovery UX |
| **D transfer** | Marketing D8/D9 claims HOLD; source public-page/Settings parity must be reconciled before claims |

**Material correction:** normal B startup is blocked by completed(A) **before** owner binding. Prior second-delete rejection remains an alternate-path conditional. Current public deletion instructions disagree with Settings source, and identity-delete acknowledgement failure is an untested saga window. These are **P0 source-based validation priorities, not deployed incidents**.

**Adjacent-question check:** audited real SessionGate composition, startup resolver, recovery screen, Settings, public page, coordinator, existing tests, current Google/Apple/Firebase primary sources, Design Studio W121, Marketing D8/D9 and Engineering S007/Q006. Further promotion needs Engineering-approved exact product runtime and enrolled iPad/MDM/file evidence, not another synthetic primer. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.** No product or peer repository writes.


---

## 20. New security boundary: account identity, local ledger and installed-container custody are not one deletion domain [SOURCE / SYNTHESIS, 2026-10-30]

**Problem/history.** The web platform scopes persistent state to an origin *within a browser storage container*. An application account is a server-side identity, while a PWA installation may be an independent local container. Deleting an identity, clearing a Sembast store, removing a Service Worker, and deleting a user-exported file therefore have different authorities, failure modes and observability. This is especially consequential for an offline EFB, where a second device or installation may not be reachable when deletion is requested elsewhere.

**Pinned product source:** LogMate `yhappcom/logmate` `main@9cc0cd432a317d5dfebbe90e318fb219e53e024a`, declared `1.0.0+1` (source version, **not** deployed build). `sembast_database_opener_web.dart` opens `logmate_ledger` through `sembast_web`. `auth_engine.dart` uses `FirebaseAuth.instance`, Firebase session reload and guarded sign-out; `provider_auth_engine.dart` likewise uses `FirebaseAuth.instance`. In those two complete files there is no explicit `setPersistence` or `instanceFor(...persistence...)`. This bounded absence does **not** prove every initialization path, SDK internal storage detail, or deployed configuration.

**Primary platform authority:** [Firebase Flutter Auth getting started — Persisting authentication state](https://firebase.google.com/docs/auth/flutter/start) (checked 2026-10-30) says FlutterFire Web stores Auth state in IndexedDB by default and supports configurable persistence. [Firebase Web Auth persistence](https://firebase.google.com/docs/auth/web/auth-state-persistence) describes LOCAL/SESSION/NONE and cross-tab synchronization for the JS SDK. These are related but not interchangeable SDK contracts: **do not infer a specific FlutterFire runtime persistence choice solely from the JS default**. [WebKit Tracking Prevention](https://webkit.org/tracking-prevention/) says Home Screen web-app data is isolated from Safari; [WebKit Safari 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/) says cookies can be copied once on installation, while other website storage is not copied and later state is not shared. [WebKit iOS/iPadOS 16.4 web-app identity](https://webkit.org/blog/13878/) explicitly allows multiple installed copies of a web app.

| Custody plane | Owner/authority | What source establishes | What deletion of A in one active instance does **not** establish |
| --- | --- | --- | --- |
| Firebase Auth identity/session | Firebase remote identity; each SDK session/container | Product uses FirebaseAuth; FlutterFire Web documents IndexedDB persistence | Erasure of local Sembast DB, other installed Auth sessions or files |
| LogMate Sembast ledger | Browser container and product repository | Web database name `logmate_ledger`; terminal path explicitly drops 29 of 37 registered stores | Removal of all 37 stores or a second container's ledger |
| Service Worker / Cache Storage | Origin-scoped browser runtime, per storage container | Worker source caches versioned shell and may retain historical builds | That caches contain personal flights, or that an account delete unregisters Worker; both need exact observation |
| External `.lbk`, print, share | User/Files destination and applicable MDM | Public deletion page explicitly excludes exported/printed/shared copies | Revocation or automatic removal of independent copies |
| Server operational/identity data | Firebase/Admin/operator authority | Tracked `firestore.rules` denies direct client read/write; `functions/index.js` documents retired lookup callable; `functions/README.md` documents operator read-only report | Existence/nonexistence of deployed remote deletion coordinator or successful remote erasure |
| Safari tab, Home Screen install #1/#2, managed Web Clip | Browser/OS/MDM container and user/operator | WebKit documents storage isolation and multiple installs | Cross-container immediate erasure, shared login, shared Files permission or uniform MDM policy |

**CONTRADICTION:** "37 stores can be serialized" is a *repository-backup scope*, not a universal account-deletion inventory. "Firebase identity deleted" is a remote authority event, not proof that all offline containers have erased the same UID's ledger. "Safari origin is the same" does not imply Home Screen storage sharing. Conversely, isolated storage does not by itself demonstrate an actual leak: stale bytes, authenticated UI access, and third-party disclosure require separate oracles.

## 21. Remote revocation versus offline-first continuity: an unavoidable availability/privacy trade-off [SOURCE / SYNTHESIS]

Pinned [SessionGate](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L44-L70) sets an initial remote-validation budget of **1500 ms**. [Lines 268–296](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L268-L296) explicitly preserve an established local owner's startup decision after timeout and handle late validation. [Lines 313–345](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L313-L345) preserve the local decision when remote authority is temporarily unreachable or indeterminate, while authoritative rejection triggers guarded Firebase-session clearing. In contrast, [fresh unbound ledger preflight lines 203–260](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L203-L260) fails closed before binding an unverified restored UID. These **different policies are deliberate in source**; do not collapse them into "Firebase offline auth always allowed".

**Counterexample:** EFB installation #1 already has owner A and goes offline. On another online device, A requests and completes remote account deletion. The offline EFB cannot learn that remote fact until an authorized communication channel becomes available. Its previously established local state may remain available under the source's offline-continuity policy. A subsequent successful server rejection can alter Auth/session access but does not, by itself, prove independent EFB file/DB erasure. This is a *conditional offline authority model*, **not an observed deletion bypass**.

**Operational judgment:** No web implementation can truthfully promise instantaneous deletion of every disconnected copy. The product must define and disclose whether "account deleted" means (1) remote identity/data deletion accepted, (2) initiating-device local erasure committed, (3) other enrolled devices eventually reconcile, or (4) user-controlled external copies excluded. For managed EFB, offline availability and immediate remote revocation cannot both be guaranteed without a pre-agreed expiration/lease mechanism, whose flight-safety and usability consequences would require a separate product decision. No such lease is authorized or observed here.

## 22. Same-origin cross-tab, separate installed web app and native phone are three different replication problems [SOURCE / DEPENDENCY]

- **Same browser profile and origin:** Firebase's Web Auth persistence docs describe cross-tab propagation for LOCAL sessions; Sembast's Chrome package probe PS01–PS11 establishes only its own bounded transaction behavior. Neither guarantees that LogMate's actual deletion saga closes every open tab atomically. A tab with an in-flight edit, old JS bundle or retained Sembast handle needs explicit test.
- **Safari tab versus Home Screen app:** WebKit's isolated storage plus one-time cookie copying means sign-out/deletion in Safari is not evidence of a wipe in the installed app. Even a new installation of the same manifest can be another independent state holder. Browser deletion of site data, removal of an icon and a managed Web Clip policy must be tested as distinct actions.
- **PWA versus native phone:** Firebase UID may be shared while local persistence, filesystem custody, app lifecycle and sync state are not. Remote identity revocation can invalidate future server access but cannot erase an unreachable native SQLite/Sembast or Files copy. A future PWA↔native peer transport does not change this authority boundary; it would need authenticated, replay-safe, consented state reconciliation.
- **Server/operator:** Tracked Firebase `firestore.rules` rejects direct client Firestore access; tracked `functions/index.js` does not implement a callable account-deletion coordinator. This **cannot** establish absence of deployed Admin functions, external operator workflows or cloud resources. An operator inventory and actual request/receipt trace are mandatory before a "remote data erased" claim.

**Failure modes:** delete on tab A while tab B is editing; delete while installed copy #2 is offline; stale A Firebase Auth restored in one container but no A Sembast ledger in another; A Sembast ledger present but no Firebase session; provider deletion succeeds but local acknowledgement fails; server erasure succeeds but another device's Sync outbox later reconnects. Treat each as a different authority/ordering test, not one generic "clear storage" test.

## 23. Public deletion request is a human service boundary, not a demonstrated deletion API [SOURCE / POLICY WATCH]

The exact [LogMate account-deletion page](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/account-deletion/index.html#L20-L55) offers an external **mailto** request to `support@minttap.app` from an associated email, with subsequent identity verification and completion notice. It does **not** contain an authenticated web deletion form or live request-status API in that page source. That is not automatically noncompliant: the acceptability of a support-mediated request depends on current policy, accessibility, processing and actual operational fulfillment. The mailbox's delivery, verification process, retention policy, response SLA and operator workflow are **UNKNOWN**.

The same page correctly excludes user-exported files from automatic deletion, but its Settings deletion instructions conflict with the pinned Settings widget (529 §15). This matters more than visual polish: an external request that can be initiated but cannot be securely verified or fulfilled is not a completed deletion service. [Google Play account deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111), [Apple in-app deletion support](https://developer.apple.com/support/offering-account-deletion-in-your-app) and [Firebase Flutter account deletion](https://firebase.google.com/docs/auth/flutter/manage-users) must be rechecked against the **actual shipped** app, served URL, store operator declarations and authenticated request evidence, not merely source copy.

**MINTTAP DIRECTION — recommended, not implemented:** Web B owns truthful entry/status/recovery content; Web E owns secure request intake, privacy/retention, proof of completion and incident handling; Engineering S007 owns provider/remote/local saga implementation; Marketing D8/D9 owns no premature public claims. Do not ask for passwords, Firebase tokens, full pilot records or unredacted backups by email. Preserve the legitimate need to verify an account request without treating possession of a possibly stale email address as sufficient authority by itself.

## 24. Destructive recovery shortcuts and false PASS oracles [CONTRADICTION / VALIDATION]

| Shortcut / green signal | Why insufficient | Stronger acceptance oracle |
| --- | --- | --- |
| Firebase `currentUser == null` | Session absence != identity/data erasure | Remote UID status + authorized data deletion receipt + local store disposition |
| Sembast 29-store terminal drop | Eight registered Replica/Sync stores not explicitly dropped; other containers outside transaction | Full 37-store owner-aware inventory and same-UID/foreign-UID negative controls |
| `Clear-Site-Data: "storage"` | Destructive to offline ledger/Worker in targeted context, not all installed contexts or external Files | Approved explicit container-by-container erasure contract with backup/incident handling |
| Same-origin sign-out in Safari | Installed Home Screen storage is isolated | Separate Safari/Home Screen #1/#2/managed Web Clip test with independent canaries |
| New PWA install opens logged out | No Auth session says nothing about old offline ledger elsewhere | Verify old container's independent data, permissions and eventual server rejection |
| Remote delete request acknowledged | Request receipt != terminal server/provider/local completion | Per-stage idempotency and reconciliation receipts, including ambiguous network outcomes |
| `.lbk` digest matches | Byte integrity != owner authority, restore compatibility or independently saved file | Files readback hash + 37-store manifest + same-UID empty-target restore + wrong-UID reject |
| Hosted Chrome synthetic 11/11 | Pinned package, not exact product or managed WebKit | Exact compiled LogMate, Safari/Home Screen, MDM, offline and human/AT evidence |

A destructive "repair" must never silently erase the sole remaining offline flight record merely to make the account-deletion state machine appear healthy. At the same time, the product must not label account deletion "completed" while it knowingly retains the initiating owner's user data in a store that its own deletion contract requires to erase. Engineering must resolve the invariant, not Web Manager invent a data retention policy.

## 25. MC01–MC20 executable cross-container/authority acceptance [VALIDATION DEFINED / NOT RUN]

**Provenance required per case:** exact LogMate source and compiled artifact SHA, FlutterFire and Sembast lock versions, server/environment IDs, test UID fingerprints only, browser engine/build/iPadOS version, installation identity/manifest, MDM profile, connectivity timeline, before/after 37-store fingerprints and independent file hash, operator remote receipts, screenshot/AT result, and explicit `NOT RUN / NON-EXECUTION / FAIL PRODUCT / PASS PRODUCT / PASS DEVICE-MDM`. Use disposable identities and synthetic flight canaries; never export real pilot PII into CI.

| ID | Scenario | Distinguishing oracle |
| --- | --- | --- |
| MC01 | A in Safari tab; second same-origin tab open; delete in first | Cross-tab Auth propagation, in-flight edit behavior, ledger access after receipt |
| MC02 | A in installed Home Screen #1; A in Safari tab | One-container deletion does not masquerade as second-container wipe |
| MC03 | A in two separately installed Home Screen copies | Distinct local canaries, deletion/launch status per install |
| MC04 | A in managed Web Clip and personal Safari | MDM isolation/managed-data transfer policy, no assumed shared Files |
| MC05 | A offline EFB; delete A remotely on native phone | Local access while offline recorded; eventual server rejection and custody adjudicated separately |
| MC06 | Existing A offline versus fresh/unbound restored A offline | Established-owner continuation vs fresh-owner fail-closed difference |
| MC07 | Firebase Auth cleared; Sembast A ledger persists | No foreign UID access; no false local-erasure PASS |
| MC08 | Sembast wiped; Firebase Auth A persists | New owner admission and stale identity reconciliation, no automatic unsafe bind |
| MC09 | A terminal delete while another tab edits | No post-delete A write, false completion or mixed owner rows |
| MC10 | A completed marker; sign out; B sign in same DB | Actual DeletionLocked/repair state and no B ledger creation before adjudication |
| MC11 | Alternate B binding; second delete request | Exact typed rejection/acceptance, no cross-UID replay |
| MC12 | A seeded nested Sync; B export then restore | 37-store owner checks and explicit foreign-owner refusal |
| MC13 | A empty Sync control; B export/restore | Distinguish owner-mismatch from unrelated restore failure |
| MC14 | Remote deletion succeeds, local phase write fails | Idempotent reconciliation, no duplicate destructive side effect |
| MC15 | Provider revoke succeeds, Firebase identity delete fails | Correct resumable provider phase and same UID |
| MC16 | Auth identity deleted, device crashes before local wipe | Restart locked; no false "all local data erased" |
| MC17 | Files backup exported before deletion | User-owned copy remains explicitly excluded; readback and retention claims truthful |
| MC18 | MDM blocks external Files destination | Explicit failure and recovery, never mark backup saved |
| MC19 | Manual email deletion request, no app installed | Identity verification, durable request/receipt, actual operator completion and accessibility |
| MC20 | App store listing + served page + exact shipped Settings | Discoverable in-app and external paths, content and operator truth parity |

**Negative controls:** wrong UID, deleted UID offline, no Firebase session but residual ledger, same origin/different installed container, stale Sync receipt, duplicate request ID, crash after remote success, no file permission, storage eviction, unsupported WebKit capability, shared/managed iPad policy. **No MC case executed in this research.**

## 26. Five-track and peer allocation after custody-plane decomposition [SYNTHESIS / TRANSFER VALIDATION]

| Track | Current evidence maturity | Next value / dependency |
| --- | --- | --- |
| **E — primary** | Stage 8 source-level account saga, terminal-wipe and multi-container authority model; no product execution | Define deletion completion receipts, per-container custody, safe operator runbook and escalation; Engineering S007 implementation dependency |
| **A — prerequisite** | Firebase/WebKit primary sources and source-based browser-origin map; Chrome package 11/11 synthetic | Actual FlutterFire Web persistence, Safari vs installed copies, Service Worker and storage namespace observation |
| **C — independent verifier** | Hosted package evidence strong, exact deletion/device weak | MC01–MC20 failure injection, immutable artifact and UID/MDM provenance, VoiceOver, no false PASS |
| **B — UX/task transfer** | Design Studio W121 says pre-runtime spec saturated | Distinct remote account, active local store, other offline devices, external Files and support-request states; execute before polishing |
| **D — claims/measurement transfer** | Marketing D8/D9 claim HOLD | Separate request initiation, terminal completion, recoverability and acquisition/Store copy; never instrument PII/UID in public analytics |

**Engineering transfer:** [S007 account-deletion saga](https://github.com/yhappcom/software-engineering-studio/blob/main/research/systems/S007_account_deletion_reauthentication_revocation_saga.md) owns provider revocation, remote erasure, local disposition and resumability. [D003 migration protocol](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) owns validation/publication lessons; neither is an implementation claim. [Design Studio W121](https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md) requires exact runtime, not another speculative UI manifest. [Marketing D8/D9 current queue](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) maintains claim HOLD. No peer repository is modified.

## 27. Checkpoint, release gate and adjacent-question review [MINTTAP DIRECTION / OPEN]

**New material conclusion:** a 37-store Sembast wipe, Firebase account deletion and a PWA install's complete local erasure are three different events. In the offline EFB scenario, remote deletion cannot instantly reach every disconnected installed copy. The source intentionally favors established-owner offline continuity while requiring remote acceptance before a fresh owner bind. Any public completion promise must state its scope and excluded external copies accurately.

**Priority order:** (1) Engineering-approved MC06/MC10/MC14/MC16 on exact LogMate source and compiled Web, to adjudicate startup/ack and offline authority; (2) MC01–MC05 on separate Safari/Home Screen/managed contexts; (3) MC07–MC13 owner/37-store/backup; (4) MC17–MC20 external Files, operator and Store truth. This order avoids falsely treating container isolation as global erasure or treating a Firebase Auth success as product erasure.

**Remaining blockers:** no approved exact compiled deletion fixture, no live Firebase/operator receipts, no independently retained `.lbk` Files readback, no multiple installed physical iPad/MDM execution, no actual shipped Settings or served deletion-page capture. No new product test, server call, account deletion, or device test performed. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

**Adjacent-question check:** authenticated session storage, independent WebKit containers, remote revocation versus offline owner continuity, operator mailto request and exact acceptance were integrated. Further promotion requires actual Engineering/product/device/operator evidence; another synthetic Sembast primer would not reduce the current P0 uncertainty.


---

## 28. Stage 8 continuation — untrusted LBK ingestion is a resource and custody boundary [SOURCE / 2026-10-30]

**Scope and priority.** This continues the same P0 owner-deletion/37-store external-backup study, rather than starting a new file or another Sembast primer. The prior A-deletion → B-startup → independent Files readback/restore gate remains the highest-severity unknown. A closely adjacent question is whether a syntactically valid, owner-matching, checksum-matching but adversarially large or deeply structured LBK can be safely rejected without destabilizing a managed offline iPad or mutating its sole ledger. The answer cannot be inferred from the existing checksum/37-store correctness checks.

**Exact read-only source pins:** LogMate main [9cc0cd43](https://github.com/yhappcom/logmate/commit/9cc0cd432a317d5dfebbe90e318fb219e53e024a); [whole_ledger_backup.dart](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/whole_ledger_backup.dart) blob 711f7845; [sembast_logbook_repository.dart](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart) blob 021d9001, especially lines 422–556 and 5830–6085. No product code was changed, no actual LBK file opened, and no real user data processed.

**Historical/design principle:** a portable backup intentionally crosses the browser origin's storage boundary and may be reintroduced later from Files, another device, email or a transfer. That portability is its value and also why the parser must treat the imported bytes as untrusted, regardless of filename, file type, apparent owner UID or an unkeyed digest. The file can be corrupted, stale, wrong-owner or intentionally crafted. A checksum detects accidental changes relative to its embedded digest; it is not an authenticated release signature or a permission grant.

## 29. Exact parse-to-commit sequence and what each gate actually establishes [SOURCE / REPLICATION]

| Phase | Pinned source behavior | Security/availability implication |
| --- | --- | --- |
| Input acquisition | restoreWholeLedgerBackup receives an already materialized String | Any file-selection, byte-length or MIME preflight in a caller is **not established** by this repository source; the full string exists before this method starts |
| JSON decode | WholeLedgerBackup.decode invokes jsonDecode(source), builds root/manifest/store maps, and materializes each row list | Whole-input parse and object materialization precede owner/digest/registry checks |
| Canonicalization | _validateLbkContainer constructs a new unsigned manifest and calls WholeLedgerBackup(...).encode(); _canonical recursively maps/sorts nested maps and lists | The entire candidate is traversed again to recompute digest; this is not a streaming verifier |
| Digest | lbkSha256 utf8-encodes the canonical String, copies it into a padded byte List and processes 64-byte blocks | More full-size allocations/work before the transaction; digest equality cannot authenticate a maliciously recomputed candidate |
| Manifest/rows | Requires exact 30-store legacy or 37-store sync-aware registry, counts matching row lengths, allowed key types, no duplicate keys, owner and replica consistency | Strong **structural** checks, but no explicit total byte, per-store row, aggregate row or depth budget in these reviewed methods |
| Sync owner metadata | _validateLbkSyncEvidence checks Sync State, revision links, nested ownerUid, canonicalPayload JSON and payloadDigest | Stronger owner/reference validation; nested canonicalPayload is parsed and hashed separately; traversal follows known metadata keys, not arbitrary user text |
| Restore transaction | _requireEmptyLbkDestination, store drops/writes, fresh destination replica preservation, locked owner, reset Sync trust, postwrite capability/reference validation | Semantic failure inside the transaction is designed to roll back; not proof of power-loss persistence, quota recovery, memory safety or external Files custody |

**Important correction against overclaiming:** the source contains meaningful checks. It is **not** an unrestricted blind import, arbitrary-code execution, path traversal, ZIP decompression, or a demonstrated exploit. The reviewed codec is JSON, not a ZIP archive. The exact caller may impose a limit elsewhere; none is proven or disproven by this repository-level inspection. The absence of a size/depth budget **in these reviewed functions** is a static validation gap, not proof that a particular iPad can be crashed.

## 30. Cost and failure-mode model [SYNTHESIS / CONTRADICTION]

Let B be the length of the supplied encoded LBK text, R the aggregate number of store rows, P the aggregate length of nested canonicalPayload strings, and H the maximum nesting depth. The implementation materializes decoded JSON, store-row lists, a canonicalized representation and UTF-8/padded digest buffers. Its expected total work grows with input and nested payloads; multiple live representations can coexist. **No measured peak heap, exact multiplier, time complexity guarantee, Dart VM recursion limit or iPadOS memory threshold is claimed.**

The structural registry fixes the **number of store categories** (30/37), not the number of rows, maximum string length, nested JSON depth or total bytes. An attacker could recompute the unkeyed snapshotDigest for a large candidate; that does not bypass owner/reference checks but can force parsing and digest work before the checks finish. An owner-matching canonicalPayload can also be very large, and its nested JSON is decoded and hashed during Sync validation. The iterative pending-map traversal avoids one form of recursive call-stack growth for recognized Sync envelopes, but _canonical itself is recursive and JSON parsing occurs earlier.

**Counterexamples:**
- A 37/37 registry match is not a memory-budget PASS.
- A checksum match is not an authenticated origin or a safe-size PASS.
- A malformed file rejected after jsonDecode is not necessarily cheap to reject.
- A large *legitimate* pilot history must not be silently truncated or declared corrupt merely to satisfy an arbitrary low limit.
- A transaction rollback after a validation exception is not evidence that the browser process survived an out-of-memory termination or that the external Files copy is independently durable.
- A small synthetic Chrome import does not establish managed Safari/MDM acceptance.
- A preflight based solely on filename extension, MIME type or manifest count can be spoofed; the trust boundary is the actual bytes and validated semantics.

## 31. Authoritative standards and implementation distinction [SOURCE / CHANGE WATCH]

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), checked 2026-10-30, recommends content/type validation and explicit size limits for untrusted file processing. This is general security guidance, **not** a prescribed LogMate numeric threshold and not proof of a product exploit.
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html), checked 2026-10-30, treats internal and externally supplied data as untrusted across receiving boundaries; extension and MIME alone are insufficient.
- [Dart JsonDecoder](https://api.dart.dev/dart-convert/JsonDecoder-class.html) documents building object graphs from JSON and FormatException for invalid syntax; it does **not** promise bounded application memory or a safe maximum backup size.
- [MDN FileReader](https://developer.mozilla.org/en-US/docs/Web/API/FileReader), checked 2026-10-30, describes user-selected file access, not automatic arbitrary Files access or durable save/readback. Browser File/Blob metadata can support a UI preflight, but platform-specific picker, readback and memory behavior still require tests.
- [W3C IndexedDB](https://www.w3.org/TR/IndexedDB/) governs transaction behavior; it does not guarantee browser-process survival under memory pressure, OS crash persistence, or external backup durability.
- [Apple Managed Open In](https://support.apple.com/en-gb/guide/deployment/depaa73a4973/1/web/1.0) and [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) remain separate policy/storage dependencies. A managed Files destination may be prohibited even when the JSON parser is correct.

**Platform separation:** JSON codec/owner validation is Dart product logic; File API is a web standard/browser surface; Safari Home Screen and Web Clip container behavior is WebKit/Apple OS policy; MDM restrictions depend on the actual airline enrollment; FlutterFire/Sembast durability is an implementation question. None can substitute for another layer's evidence.

## 32. Engineering acceptance contract: fail early, fail non-destructively, preserve legitimate scale [MINTTAP DIRECTION / DEPENDENCY]

**Recommended release contract, not an authorized code change:**
1. Determine a justified input-size and aggregate-row budget from real but privacy-safe representative corpus size distributions, platform memory measurements and supported device classes. Do **not** invent a universal 10 MB or N-record limit.
2. When the user selects a file, check available file byte length **before** fully decoding when that browser/file path exposes it; also enforce a repository-level decoded-input budget so alternate callers cannot bypass UI checks.
3. Enforce bounded nesting/metadata depth and bounded nested canonicalPayload parsing, while preserving valid long flight histories and user-authored text. Validate exact owner, format, store registry, key uniqueness, references and digest before any persistent write.
4. Keep the destination empty-stage and new-replica/locked-owner transaction invariant. On invalid input, oversized input, unsupported format, quota failure or interruption, do not silently overwrite the active ledger, erase the sole copy, partially publish capability or claim a successful restore.
5. Separate **file selected**, **file read**, **checksum verified**, **owner/reference validated**, **staging restored**, **reopened and reconciled**, and **independent external copy retained**. Each needs a distinct observable result.
6. A rejected large but legitimate file should have a safe escalation/recovery path, not an instruction to clear site data, disable security checks or share an unredacted LBK with support.
7. Run both instrumented and uninstrumented controls and measure browser heap/elapsed time, tab termination, quota errors, app responsiveness and VoiceOver state. Do not log UID, raw flight records, backup contents or token-bearing URLs.

**Ownership:** Engineering S007/D003 and the product team own codec/resource limits and executable migration/restore implementation. Web E owns trust and non-destructive operational acceptance; A owns browser File/Blob and storage mechanics; C independently measures quality and faults; B owns truthful recovery/task-state content with Design Studio W121; D owns privacy-preserving event definitions and prohibits unsupported claims. This is a transfer contract, not a Web Manager implementation.

## 33. Resource and identity adversarial acceptance matrix [VALIDATION DEFINED / NOT RUN]

| ID | Exact product scenario | Decisive oracle |
| --- | --- | --- |
| RI01 | Genuine small 37-store LBK | Same-UID empty-stage restore, new replica, locked owner, correct Sync trust, full 37-store semantics |
| RI02 | Large **legitimate** synthetic pilot history | Supported maximum established by measured device budget, no silent record truncation or false corruption |
| RI03 | File just below/at/above proposed byte budget | Deterministic preflight and repository-level agreement, no data mutation on rejection |
| RI04 | Many rows in one permitted store with correct count/digest | Bounded parsing/write behavior and truthful rejection or supported restore |
| RI05 | Deep nested metadata with recomputed checksum | Bounded depth/stack/memory behavior; no false digest-authentication inference |
| RI06 | Large canonicalPayload and many Sync bindings with valid matching UID | Bounded nested JSON/digest work; owner/reference correctness |
| RI07 | Foreign owner in nested restoredSourceState or canonicalPayload | Fail closed before publishing, original active ledger untouched |
| RI08 | Valid outer checksum but malformed nested canonicalPayload | Explicit invalid-file error, no partial staging state |
| RI09 | Wrong owner, duplicate key, registry count mismatch, unknown store | Correct differentiated rejection without mutation |
| RI10 | Quota exhaustion after some staging writes | Transaction rollback/reopen evidence, no half-published destination |
| RI11 | Browser process termination during decode vs inside transaction | Distinguish non-execution, recoverable staging, physical durability; no unsupported OS-crash guarantee |
| RI12 | File selected in Safari tab, Home Screen copy and managed Web Clip | File read capability, container identity and MDM transfer limits observed separately |
| RI13 | Files export saved and read back independently before destructive transition | Byte/hash match plus same-UID empty-stage restore, not merely an in-memory digest |
| RI14 | VoiceOver, large text and cancel while validation takes time | Accessible pending/failure/success states, no false "backup safe" or irreversible action |
| RI15 | A deleted, B attempts import of A or B-crafted LBK | B startup/owner gate adjudicated first; no foreign-owner rebind or A Sync resurrection |
| RI16 | Old/new PWA shell and v16/v17 logical schema during restore | Reader/writer/schema/Worker compatibility, no unsafe rollback or silent version upgrade |

**Evidence label per case:** DEFINED NOT RUN, NON-EXECUTION, PASS/FAIL PRODUCT-LAB, PASS/FAIL DEVICE-MDM, and separately operator/Files receipts. A synthetic JSON parser exercise can be used as a negative control but cannot promote the exact LogMate gate. Never run these on production pilot records.

## 34. Cross-track relative-depth and gate reassessment [SYNTHESIS / TRANSFER VALIDATION]

| Track | Current stage/depth | Pressure and allocation |
| --- | --- | --- |
| E (lead) | Stage 8 security source analysis mature, exact deletion/backup/runtime proof absent | Highest severity: A→B owner isolation, external backup integrity and resource-safe restore; owns RI acceptance and incident response |
| A | Browser File/Blob/IndexedDB/Service Worker standards sourced; installed Safari/MDM execution absent | Resolve preflight portability, storage namespace and file readback, not repeat JSON parser primer |
| C | Chrome PS/MT synthetic coverage strong; real product memory, performance, AT and iPad weak | RI02–RI14 fault/scale/device validation; test both measurement perturbation and uninstrumented behavior |
| B | Design Studio W121 Stage 3 execution-priority; no physical recovery task proof | Distinct progress/error/retry/restore states, safe copy and VoiceOver acceptance; no new speculative visual design |
| D | Marketing D9 product claims HOLD; no verified PWA install/backup funnels | Minimal aggregate event taxonomy, no raw UID or file metadata, and no "guaranteed backup" claims |

**Cross-domain contradiction:** source-level stronger owner validation can still be preceded by expensive parsing; a secure rejection can be an availability failure. A usable Files selection interface is not an independently durable backup. A healthy Worker shell does not imply the Sembast restore is safe. Conversely, a failed malformed-file import is not automatically a user-data-loss event; preserve before/after state and failure class.

## 35. Practical validation order and incident criteria [MINTTAP DIRECTION / OPEN]

The order remains **P0 owner/deletion before resource-limit optimization**: (1) Engineering-approved A-delete → signed-out restart → normal B startup (MC10/SL01), (2) full 37-store A Sync canaries, B export, independently saved/reopened Files copy and same-UID empty-stage restore (OC01–OC09), (3) RI01/RI07/RI09/RI10 correctness and failure isolation, (4) RI02–RI06 measured scale/resource budget, (5) managed Safari/Home Screen/Web Clip RI11–RI14, (6) exact Worker FC/TR/SR/CW/VW release tests. Run tests on disposable identities only.

**Escalate as a product incident only on observed product evidence**: wrong-owner data becomes accessible, a completed deletion retains in-scope user data, a valid user backup is destroyed/irrecoverably truncated, or a recovery path overwrites an existing ledger. A source-level absent bound is a conditional reliability/security review item, not an observed incident. A browser tab killed by a crafted test is a lab failure with precise artifact provenance, not evidence of remote compromise.

## 36. Checkpoint and adjacent-question check [OPEN / CHANGE WATCH]

**New reusable finding:** the pinned LBK restore sequence fully decodes and canonicalizes untrusted JSON and recomputes an unkeyed digest **before** transaction-level empty-stage restore; nested Sync payloads are decoded and hashed again. The reviewed codec/repository functions have no explicit byte/row/depth resource budget, while owner/registry/digest/reference checks are substantive. This is a **STATIC CONDITIONAL ingestion/availability gap**, not a reproduced exploit, a proven managed-iPad failure or evidence that the caller lacks preflight.

**No gate change:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD. The meaningful checkpoint adds RI01–RI16 to the existing 529 owner/Files validation program; it does not displace the P0 A→B deletion blocker. LogMate, Design Studio, Marketing and Engineering remain read-only.

**Adjacent-question check:** input selection, full decode, recursive canonicalization, digest allocation, nested Sync validation, transaction atomicity, quota, OS/MDM file custody, legitimate-scale contradiction, accessible recovery and cross-track ownership were integrated. The next decisive question is **measured exact-product resource behavior with Engineering approval**, not more static codec speculation. Stop at this evidence boundary rather than inventing a numeric limit or claiming a device PASS.
