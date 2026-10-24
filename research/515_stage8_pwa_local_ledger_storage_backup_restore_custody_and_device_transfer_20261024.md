# 515 — Stage 8 PWA ledger durability, 37-store backup/restore custody and EFB transfer

Date: 2026-10-24 KST  
State: **SOURCE AUDIT / INTEGRATED ACCEPTANCE DESIGN; WEB + EFB PRODUCT VALIDATION OPEN; PWA RELEASE HOLD**  
Owner: Track E. Dependencies: A platform/storage, C independent quality/runtime. Consumers: B state/IA, D privacy/measurement. Web Manager coordinates.

## 1. Canonical refresh and track allocation [SOURCE / DEPENDENCY]

Web Manager main@742111b9ae7dcdc2a69ecc4bd7ea4e7e925a1332: AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research index, 513/514 and latest commits read. LogMate read-only main@4101ec7380796300f68fa60dbc7e5b6061f00080: AGENTS, MASTER, current Manual Delta Sync contract, backup codec, Sembast repository, Web opener, native backup tests, Web IndexedDB reopen tests and latest roadmap. The 15 commits since 27f926aa touch documentation/contract/prompt, not the audited implementation paths. Current main is the source anchor.

Peer dependencies read: Design Studio WEB_STATUS W121 and CONTENT_STATUS CD127 (runtime, accessibility, human semantic validation OPEN); Software Engineering Studio research index M006/Q006 (bounded browser/CI test transfer, not product proof); Marketing Manager STATUS D8 (LogMate working export/import/PWA/Sync promotional claims HOLD). No product or peer writes.

Track E remains the major bottleneck because local pilot flight data loss is higher-consequence than another generic Worker primer. Track A supplies origin, IndexedDB, CacheStorage, WebKit partition, quota and eviction facts. Track C must falsify real browser/file/restore behavior and runner exit states. Track B translates local-save/offline/export/restore/Sync authority into accessible task states. Track D restricts telemetry and public claims. This is unequal allocation by risk, dependency and current evidence maturity.

## 2. History → principle → standard → platform [SOURCE / SYNTHESIS]

AppCache and Service Workers primarily concern offline resource delivery. The Service Worker Cache API, the Sembast Web IndexedDB ledger, an external .lbk backup file and an authenticated remote Sync receipt have different owners, failure modes and lifetimes. A verified shell does not imply a surviving ledger; a surviving ledger does not imply an offline runnable shell; a checksum-valid backup is not a verified restored ledger.

The WHATWG Storage Standard and StorageManager govern browser storage buckets and persistence requests. StorageManager.estimate() is an estimate, not guaranteed future capacity; persist() may return false; granted persistent mode is not an independent backup and does not prevent user/management removal. QuotaExceededError and origin eviction require explicit handling. Sources reviewed 2026-10-24: https://storage.spec.whatwg.org/ ; https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist ; https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate .

WebKit primary policy (2023, CHANGE WATCH) distinguishes per-origin/overall quota, storage pressure and persistent mode. Published iOS/iPadOS 17-era quotas (browser origin up to 60% of disk, other WebKit app up to 15%) are upper bounds, not reserved capacity or durability guarantees. WebKit Safari 17.2 says a *user-created* Home Screen web app copies login cookies when applicable but does **not** copy IndexedDB/other local storage; later storage is separate. Do not transfer this automatically to MDM Web Clips. Sources: https://webkit.org/blog/14403/updates-to-storage-policy/ ; https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ .

Apple managed Web Clip configuration (including FullScreen, IsRemovable and IgnoreManifestScope) governs a managed shortcut, not proof of storage identity, offline cold launch or persistence: https://developer.apple.com/documentation/devicemanagement/webclip . Safari tab, user Home Screen app, managed Web Clip and managed full-screen Web Clip require separate device evidence.

## 3. Exact LogMate source audit [SOURCE / VALIDATION]

- The Web opener uses Sembast Web databaseFactoryWeb.openDatabase('logmate_ledger'). This is **one named IndexedDB-backed database**, not 37 databases. Worker control uses a separate CacheStorage catalogue.
- WholeLedgerBackup defines format 'logmate.full-ledger-backup', v1 and Sync-aware v2, canonical JSON and SHA-256 snapshot digest. Source explicitly limits SHA-256 to integrity; it does **not** authenticate author or encrypt the flight records.
- The exact current repository source contains **30 base .lbk stores plus seven Sync-local stores = 37 unique registry names**, with no duplicate names. The extra seven are sync state, operation bindings, receipts, applied identities, applied cursor, record heads and holds. Two base stores use integer keys. This is a real static source inventory, not a Flutter test PASS.
- Export runs inside a Sembast transaction; requires READY capability, matching unlocked owner UID and no pending account-deletion lock. It returns encoded text and registry counts/checksum; external file destination, save confirmation and durable readback are separate caller responsibilities.
- Restore validates format/capability/UID/registry/key types/counts/duplicate keys/digest and permits only a fresh, otherwise empty staging database. Its transaction writes all stores, preserves the destination's new replica ID, binds matching owner in a locked state, clears applied cursor/identity authority and records prior source evidence in recovery holds. v1 30-store restore migrates to v17 with no invented receipt/cursor. Test-only failure injection exists after multiple writes.
- Native test source 'whole_ledger_backup_test.dart' has nine top-level tests, including a populated **37-store IO staged-file round trip** and rollback injection. Existing 'sembast_web_reopen_test_browser.dart' exercises real IndexedDB create/delete/restore close/reopen but contains **no Web .lbk export/restore invocation**. These tests are not interchangeable; neither was run here.
- Current approved Manual Delta Sync contract explicitly states **Production Manual Sync NOT IMPLEMENTED**, F1 local persistence implemented. Independent .lbk transfer and separate replica identity are approved design, not proof of shipped Web backup UI or cloud convergence.

Source anchors: LogMate main@4101ec7380796300f68fa60dbc7e5b6061f00080; repository blob d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb; codec 711f784534bc686a4d8edd6617ac4d1ac362e0a7; Web opener 87f043d582375a7d11a8183889f2f23195396ef1; native test 2f9d6b0a9a6a494dfd64c95b1e3db8aaa562537b; browser test b019fe94de1c1f9945c342ce8654541289f45b92.

## 4. Non-transitive data durability/authority ladder [SYNTHESIS / MINTTAP DECISION]

1. SHELL_CACHED — verified Worker and assets exist, not necessarily client-routed.
2. CLIENT_RUNNABLE — current client receives coherent shell, not necessarily cold offline reopen.
3. LEDGER_COMMITTED — local record/revision/outbox/projection transaction/readback, not necessarily restart durability.
4. LEDGER_REOPENED — exact same storage container/profile survives a real browser-process restart, not eviction immunity.
5. BACKUP_ENCODED — valid format/digest and owner-checked export string, not yet an external file.
6. BACKUP_EXTERNALIZED — independently stored file reopened with byte/digest verification, not yet semantic restore.
7. RESTORE_SEMANTIC — fresh destination restores records, tombstones, history, outbox, custom fields, drafts, pages/baselines and invariant checks; destination replica stays new and Sync authority resets.
8. SYNC_ACKED / CONVERGED — authenticated remote receipt and applied cursor prove actual effects; not implemented in production LogMate.

No predicate may be promoted into another. Never clear IndexedDB/CacheStorage as a blind Worker-503 repair, use persistent-storage permission as a backup claim, infer owner identity from checksum, or call a fresh .lbk import 'synced'.

## 5. Integrated destructive and negative-control matrix [VALIDATION]

All tests use synthetic flight records, disposable owners and independent offline snapshots; never upload real .lbk or owner tokens to research/CI logs.

| ID | Real execution and fail-closed proof obligation |
| --- | --- |
| D01 | Exact NORMAL source/tree/Worker hash and actual hosted or trustworthy test origin; reject Acceptance or stale artifact. |
| D02 | Populate nontrivial 37-store v2 source; record semantic baseline for active/deleted/revisions/outbox/custom/draft/page/aggregate. |
| D03 | First network navigation/Worker claim, controlled reload and offline process reopen; prove client shell and ledger independently. |
| D04 | Terminate browser process, reopen same persistent profile and compare semantic ledger/outbox readbacks; tab reload is insufficient. |
| D05 | Use actual Web export UI/caller; save .lbk externally, reopen independently and check exact bytes/digest. In-memory encode is insufficient. |
| D06 | Restore into fresh Web IndexedDB staging; compare all 37 store classes, owner locked, new replica ID, unverified remote baseline. |
| D07 | Inject failure after multiple restore writes; verify rollback and safe retry, no partial state or fabricated ACK. |
| D08 | Wrong UID, digest mutation, duplicate key, unknown store, wrong format/key type/count must reject before destination mutation. |
| D09 | Nonempty destination (records, saved config, claimed owner) must reject without destroying existing data. |
| D10 | Real v16 format-v1 30-store fixture to v17 migration preserves history/custom fields; no Sync authority invention. |
| D11 | v17 source cursor/identities/holds and R03/R04 collisions; independently inspect hold provenance, cursor reset, no silent overwrites. |
| D12 | Interrupted export/file write, canceled picker, insufficient space and missing file: no 'Backup complete' before external readback. |
| D13 | QuotaExceededError, storage pressure and partial Worker update with pending outbox: no automatic destructive site-data clear. |
| D14 | Explicit site-data/profile deletion: prove independent file survives outside origin and restores in fresh context. |
| D15 | Safari tab then user-created Home Screen: do not presume IndexedDB copy; test explicit file migration and separate login-cookie state. |
| D16 | MDM Web Clip and full-screen: record actual MDM payload, OS, container identity, cold offline launch, removal/redeployment and backup. |
| D17 | Worker/schema vN→vN+1 with outbox and offline dormancy: preserve records/tombstones/restore trust after update/rollback. |
| D18 | Native ↔ PWA file transfer uses new replica; direct unattended P2P, hotspot, background Sync and cloud convergence stay separate OPEN gates. |
| D19 | Keyboard/screen-reader/human interruption tests for saved-local, offline-not-ready, backup-created, restore-locked and Sync-pending states. |
| D20 | Privacy negative control: no flight payload, UID, client ID, tokens or .lbk bytes in general analytics/CI; only bounded sanitized evidence. |

All D01–D20 are **defined, not executed**. A single browser cohort cannot certify Safari, user Home Screen or managed iPad.

## 6. Cross-track transfer and operational decision [TRANSFER VALIDATION / CONTRADICTION]

A→E: WebKit user Home Screen cookie-only copy and separate storage cannot be generalized to managed Web Clips; quota upper bound or persist() does not guarantee retention. C→E: native 37-store test + browser reopen test does not compose into Web 37-store backup/restore PASS. E→B: statuses must distinguish 'saved locally', 'offline ready on this device', 'external backup file verified', 'restored but owner locked' and 'remote Sync confirmed'; final copy requires Design Studio/AT/human validation. E→D/Marketing: an offline-first design goal is not evidence for EFB-installed offline durability, working backup UI or automatic Sync marketing claims. Engineering owns Flutter implementation, runner, fault injection and fail-closed exit semantics.

**SOURCE-VERIFIED conditional collision, not an observed runtime incident:** existing source holds can share transformed cursor/identity hold keys. Study 506 §§8–10 already owns the exact code audit and unexecuted Engineering Dart R03/R04 regression proposal; do not duplicate or infer observed user data loss.

## 7. Engineering handoff, actual attempts and exit criteria [VALIDATION / OPEN]

Prerequisite: exact LogMate source and verified NORMAL archive/hosted bytes from studies 509–512, pinned Worker SHA, disposable owner and synthetic ledger oracle, browser/OS/profile/MDM metadata. Execute existing native backup tests and existing Chromium IndexedDB reopen tests at exact HEAD, then implement a **new browser 37-store .lbk export → external file → fresh Web restore** integration test; neither existing test covers this end-to-end. On physical iPad test Safari, user Home Screen, managed Web Clip and full-screen separately, including removal/reinstall, offline cold start, storage pressure and external backup recovery.

Verdicts must remain scoped: SOURCE_INVENTORY_VERIFIED (30+7 source audit), NATIVE_TEST_PASS (actual Flutter execution), WEB_REOPEN_PASS (real browser persistence), WEB_BACKUP_RESTORE_PASS (external file and semantic restore), MANAGED_IPAD_PASS (physical target MDM), and INCOMPLETE/EXECUTION_ENVIRONMENT_BLOCKED. No synthetic/source-only verdict is release approval.

**Actual run evidence:** static source audit verifies 30+7 unique names; native and Web test code inspected, not executed. A fresh minimal Chromium/Playwright localhost attempt with /usr/bin/chromium again returned net::ERR_BLOCKED_BY_ADMINISTRATOR. No Flutter/Dart executable or actual NORMAL artifact is present in this environment. This is an environment/evidence blocker, not a product failure or PASS.

## 8. Open register, change watch and adjacent-value check [OPEN / CHANGE WATCH]

OPEN: real Web .lbk export UI/external file; populated 37-store browser semantic restore; R03/R04; origin eviction/dormancy; physical Safari/Home Screen/managed EFB; actual NORMAL/HTTPS Worker, Manual Sync/receipts, accessible/human recovery. CHANGE WATCH: WebKit/iPadOS storage heuristics and managed Web Clip behavior, Chrome eviction/partition, browser file APIs, Sembast Web and LogMate schema, Worker updates and platform policy.

**Adjacent-value decision:** Another synthetic-only oracle would add less value than actual Engineering-controlled Web backup/restore and physical device evidence. Stop at this meaningful implementation/runtime boundary, not a manufactured PASS.

**Final gate: applied Stage 8 ACTIVE, Track E primary with A/C critical suppliers; Production validation OPEN; PWA release HOLD.** Product/peer repositories unchanged.


## 9. Integrated continuation — Web file custody, untrusted LBK import and managed-iPad data-flow policy (2026-10-24) [SOURCE / SYNTHESIS / CHANGE WATCH]

### 9.1 Why this is a distinct Stage-8 bottleneck [SYNTHESIS / DEPENDENCY]
Earlier sections establish a 37-store in-database snapshot and a missing Web export-to-file-to-fresh-restore execution. The next independent failure boundary is **whether a file can leave the browser, remain recoverable in a genuinely independent destination, and return through a safe, policy-permitted import path**. This is not solved by another R03/R04 key-collision model: study 506 §§8–10 already owns that exact source counterexample and an unexecuted, real-repository Dart regression proposal. No duplicate synthetic hold model is promoted here.

Track E owns file custody, privacy, import resource admission and organizational policy; A supplies File API/browser storage mechanics; C owns actual file/MDM/restore negative oracles; B owns explicit, accessible completion/cancellation/recovery states; D owns privacy-minimized metrics and claim challenge. Generic curriculum stages remain PASS; this is applied Stage 8 with product/runtime gates OPEN.

### 9.2 Browser capabilities are not a universal save-to-Files guarantee [SOURCE / CONTRADICTION]
Primary and implementation references checked 2026-10-24:
- MDN HTML anchor download: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a — a download filename is a suggestion; user agent/settings can prompt, save, open or otherwise handle a file. A Blob URL click does not provide a general cross-browser durable external-file receipt.
- MDN file input: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file — broadly supported user-selected file read path; the accept attribute is a hint, **not validation**.
- MDN FileReader: https://developer.mozilla.org/en-US/docs/Web/API/FileReader — user-selected File/Blob access, not arbitrary filesystem path access.
- MDN showSaveFilePicker: https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker — limited availability, secure context and transient user activation; do not make it the sole iPadOS path.
- Apple iPad Downloads: https://support.apple.com/guide/ipad/find-your-downloaded-files-on-ipad-ipad8cef35dc/ipados — documents a Safari/Files Downloads path, not a promise for every standalone PWA/Web Clip and MDM envelope.
- WebKit Safari 17.2: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ — when a user creates a Home Screen web app, cookies may be copied, but other local storage is not copied. The user Home Screen and Safari ledger containers must be treated separately.

**SYNTHESIS:** exportWholeLedgerBackup() returns encoded text, not an OS file receipt. A download trigger or browser download event proves neither a completed user-selected destination write nor a recoverable, independent copy. A user re-selecting the actual saved .lbk file and comparing exact bytes/digest supplies stronger point-in-time readback, but not independent failure-domain survival: a copy in the same iPad's local Files may disappear with that device. Cloud/off-device custody is a separate user/organizational policy decision, not automatic PWA Sync. An unverified Web Clip should not inherit Safari-tab behavior.

**MINTTAP DECISION / PROPOSED CONTRACT:** separate BACKUP_ENCODED, DOWNLOAD_REQUESTED, FILE_VISIBLE, FILE_REOPENED_AND_HASH_MATCHED, INDEPENDENT_COPY_CONFIRMED, and FRESH_RESTORE_SEMANTIC. Each status requires its own evidence. If a browser cannot supply a programmatic save completion receipt, do not invent one; use an honest user-controlled file re-selection/readback flow and clearly label its limitations. A second failure domain must be evidenced, not inferred from the word "Files".

### 9.3 Managed Open In can make an otherwise valid file-transfer design unavailable [SOURCE / CHANGE WATCH]
Apple primary management sources checked 2026-10-24:
- Manage organizational data: https://support.apple.com/guide/deployment/manage-organizational-data-depaa73a4973/web — Managed Open In restricts transfers between managed/unmanaged apps and accounts; managed Safari domains classify Safari downloads as managed documents.
- Managed Domains payload: https://support.apple.com/en-is/guide/deployment/depb4c146c2e/web — Safari downloads from managed domains may be subject to Managed Open In controls, including restrictions on transfer to unmanaged destinations.
- Web Clip configuration: https://developer.apple.com/documentation/devicemanagement/webclip — FullScreen, IsRemovable and IgnoreManifestScope are management properties, not proof of file-system, storage-partition or offline capability.

**SYNTHESIS:** an airline/company iPad may prohibit moving an LBK file from a managed domain/source to an unmanaged personal Files provider, cloud account or native mobile handoff. Conversely, an organization may authorize an approved managed destination. The *actual* enrollment, supervised state, managed domain list, document restrictions, allowed providers and Web Clip classification must be read from the target MDM configuration and tested. Apple's Safari-domain rule is **not automatically proof** that a particular Web Clip download is classified identically.

**MINTTAP DECISION:** do not bypass company data-flow controls using alternate URLs, personal email, clipboard, share sheets or an undocumented native bridge. If no permitted independent backup destination exists, mark the EFB external-backup requirement BLOCKED_BY_POLICY and do not advertise backup or device migration as working. Escalate the policy/design trade-off to the operator and Engineering; the Web Manager cannot grant MDM permissions.

### 9.4 Untrusted .lbk admission and resource limits [SOURCE / CONTRADICTION]
Read-only source pin: LogMate main 4101ec7380796300f68fa60dbc7e5b6061f00080; WholeLedgerBackup codec blob 711f784534bc686a4d8edd6617ac4d1ac362e0a7 and repository adapter blob d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb.

Exact code observations:
1. WholeLedgerBackup.decode(source) calls jsonDecode(source) before any explicit byte-count or nesting-depth budget in the inspected codec. The restore entry point decodes before _validateLbkContainer. An upstream UI/file caller might have a limit; none was verified here.
2. The validator checks format/version/UID/sourceReplicaId, canonical SHA-256 digest, 30-or-37 registry shape, store key types/counts, per-store duplicate keys and unknown stores. A digest is not a signature, encryption or provenance. A caller-created digest-valid file is still an untrusted input.
3. The decoder materializes a nested JSON object and the restore constructs per-store rows in memory. There is no explicit input-size/depth limit in the audited entry point. **Potential resource exhaustion is a source-level hypothesis**, not an observed iPad crash or a proven browser quota failure.
4. The fresh-staging predicate enumerates selected ledger/user stores and semantic defaults but does not explicitly scan all seven Sync stores for arbitrary preexisting rows. This is a **conditional staging-isolation review item**: the supported caller is expected to supply a newly opened staging DB, and no normal user path creating hostile Sync rows in such a DB was demonstrated.
5. The positive v2 test in sync_replica_identity_safety_test.dart explicitly verifies one cursor and one applied identity become holds with a new replica/unverified baseline. This is real source-level positive test coverage; it is not the R03/R04 collision negative or a Web file test. Study 506 §§8–10 already owns the collision-specific real Dart proposal. Do not duplicate it or claim an executed failure.

**MINTTAP DECISION / proposed engineering admission:** bound selected-file byte length *before* JSON decoding; define and test depth, row-count, per-store and total materialization budgets against representative iPad memory; reject unsupported schema/manifest extensions deliberately; verify UID with actual current owner authority rather than checksum; validate record/domain references and Sync-state semantics in isolated staging; reject preexisting unapproved staging Sync rows; ensure failure/abort leaves prior user data and source file untouched. Do not pick arbitrary production thresholds without real corpus/device evidence. Do not automatically trust a matching digest, file extension, MIME hint, file name, file picker selection, or the fact that the file came from a managed destination.

**PRIVACY:** the inspected .lbk is plaintext canonical JSON. It can contain flight history, custom fields, drafts and identifiers. Neither Web Manager nor CI should upload actual user .lbk content or log its raw bytes, owner UID, source replica ID or filenames containing personal data. Encryption-at-rest and approved destination requirements remain separate product/security/legal decisions; this research does not claim the current .lbk format is encrypted or authenticated.

### 9.5 Engineering execution matrix F01–F24 [VALIDATION / OPEN]
All cases are **defined, NOT EXECUTED**. Use synthetic flight data, exact NORMAL build/Worker identity, pinned source and controlled device/MDM policy evidence. Distinguish UI event, browser event, file re-selection, hash readback and independent-destination receipt.

| Case | Required falsification |
| --- | --- |
| F01–F03 | Safari tab, user Home Screen, managed Web Clip/full-screen each generate an LBK; capture exact OS/browser/container/MDM provenance and whether export is actually offered. |
| F04–F06 | Download click vs actual file existence vs independent user re-selection/readback; reject "backup complete" on click alone; test filename rewrite and extension/MIME mismatch. |
| F07–F09 | Cancelled picker, interrupted download and storage-full/error; preserve source ledger and do not claim external backup. |
| F10–F12 | Same-iPad local Files, authorized managed provider and authorized off-device destination; distinguish readable-now from independent loss-domain survival. |
| F13–F15 | Managed domain/Managed Open In allow vs deny; explicit prohibited destination, user-initiated permitted path and Web Clip versus Safari policy equivalence test. No bypass. |
| F16–F18 | Oversized but syntactically valid LBK, deep JSON, excessive rows/large nested values; bounded memory/time and no partial staging publication. Thresholds from actual device profiling. |
| F19–F20 | Digest-valid but semantically invalid/extra fields; wrong UID/format; file extension and accept hint never substitute validation. |
| F21–F22 | Restore into fresh staging and deliberately nonfresh Sync-only staging; independently assert all source evidence, new replica, locked owner, unbound/unverified state and no invented ACK. |
| F23 | Keyboard, VoiceOver and user interruption: status distinguishes requested download, verified external file, blocked-by-policy and restored-but-locked without false success. |
| F24 | Privacy audit: no raw LBK/UID/flight data in logs/analytics; verify safe synthetic diagnostics and controlled artifact retention. |

Run existing native and Web tests first, then an exact-current-head Web export→external readback→fresh restore integration test, then physical Safari/Home Screen and **policy-envelope-matched** managed EFB. Source review, V8/Node fixture, CI success, or an unmanaged iPad cannot replace these distinct tiers.

### 9.6 Cross-track transfer, contradiction register and meaningful checkpoint [TRANSFER VALIDATION / OPEN]
- **A→E:** showSaveFilePicker is not a universal iPadOS guarantee; file input is user-selected read, and Blob/download does not prove durable external storage. Service Worker CacheStorage is a separate failure domain from the LBK and Sembast ledger.
- **E→C:** the decisive test is a real externally reselected file plus semantic restore and negative MDM policy tests, not a synthetic hash-only PASS. Resource-limit tests must observe actual process/memory/failure outcomes.
- **E→B / Design Studio W121/CD127:** a disabled or denied file export is a real recovery state, not a successful backup; copy, focus and VoiceOver outcomes require exact-runtime evidence. No new visual design authority is asserted.
- **E→D / Marketing 437:** advertising or analytics must not intercept or delay backup/recovery. Public "offline backup", "iPad transfer" or "Sync complete" claims require independently verified capabilities; PWA web ads remain HOLD.
- **E→Engineering D005/D006:** independent candidate validation/publication and remote Sync receipt/cursor authority are separate from browser file-custody and MDM. Engineering owns actual implementation, limits, faults and device runs.

**CONTRADICTIONS:** encoded ≠ externally saved; downloaded ≠ independently recoverable; checksum valid ≠ authentic/authorized; file picker available ≠ managed destination permitted; Safari Files instructions ≠ standalone managed Web Clip proof; local transaction atomic ≠ cross-device file custody; accepted JSON ≠ resource-safe/semantically valid; MDM enrollment ≠ known exact restriction policy.

**CHANGE WATCH:** WebKit/iPadOS File API and Home Screen behavior, browser File System Access support, managed Web Clip semantics, Managed Open In and managed-domain settings, Flutter Web download implementation, LBK format/codec and future authenticated Sync. No production environment or airline policy facts were inferred.

**Adjacent-value check:** Prior 506 already resolves the R03/R04 source counterexample and owns its Dart test proposal; this continuation instead resolves three distinct prerequisites in one bundle: browser file-delivery evidence, MDM data-flow authorization and untrusted import/resource admission. The next decisive boundary is a real policy-authorized external-file round trip on the exact Web artifact and physical managed iPad. **Stage 8 applied ACTIVE / Production validation OPEN / PWA release HOLD.** No product or peer repository changed.


## 10. Product-authority reconciliation and executable file-flow admission (2026-10-24, later checkpoint) [SOURCE / CONTRADICTION / MINTTAP DECISION / VALIDATION]

### 10.1 Canonical product status changes the next action [SOURCE / CONTRADICTION]

Read-only product authority at LogMate `main@4101ec7380796300f68fa60dbc7e5b6061f00080`: `AGENTS.md` requires `MASTER.md` first, and `docs/roadmap-reconciliation-2026-10-24.md` completion matrix explicitly distinguishes:
- **B1 / Whole-ledger backup foundation:** implemented repository slice, merged PR #18, host-CI bounded validation; actual file/device transfer is **NOT VERIFIED**.
- **FILE / Backup file UX:** **NOT IMPLEMENTED complete product flow**. Export/pick/share/restore review and failure UX are future integration; do not presume an existing production Web file UI can simply be tested.
- **OUTPUT / Export and print:** production output **NOT IMPLEMENTED**; formatted Excel/PDF/print and interchange are different from full-ledger LBK recovery.
- **IMPORT / Production import:** engine **NOT IMPLEMENTED**; roster/third-party candidate review is not LBK owner-locked recovery.
- **BACKUP-001/002:** nonempty destination merge/replace/reset and automatic/continuous backup remain owner decisions **OPEN**. Neither is a prerequisite for testing an approved empty-staging B1 path; neither may be silently chosen by Web Manager.

This corrects a possible ambiguity in §§7–9: “test the real Web export UI” is not an assertion that the complete FILE UI exists. **Next actionable engineering gate is product-approved minimal file-flow implementation plus its exact-build acceptance, not another static UI-only test of a nonexistent complete flow.** Repository source is still the authority for actual methods at its pinned SHA; roadmap status is the authority for product-completion claims. GitHub code search returned no indexed matches, so this study does not infer absence of every partial caller from search emptiness.

### 10.2 Source-verified method boundaries and state ownership [SOURCE / SYNTHESIS]

Exact LogMate `lib/repository/logbook/sembast_logbook_repository.dart` source at `main@4101ec7`, blob `d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb`:
- Lines 419–481: `exportWholeLedgerBackup(verifiedOwnerUid)` requires READY capability, matching **unlocked** owner and no deletion lock, takes a transaction-consistent snapshot of the 37-store registry, and returns **String**. Comment explicitly assigns file selection and I/O to the caller. Snapshot SHA-256 detects corruption but is not an authentication signature.
- Lines 483–556: `restoreWholeLedgerBackup(encodedBackup, verifiedOwnerUid)` decodes and validates, requires fresh otherwise-empty staging, preserves a new destination replica, locks the matching owner, resets destination Sync trust, and verifies references before transaction commit. Test-only fault callback is not user-facing rollback proof.
- Lines 559–591: source cursor/applied-identity evidence moves into recovery holds while live destination authority resets. R03/R04 collision negative is owned by study 506; this section does not duplicate it.
- Lines 5806–5924: manifest/registry/digest/typed-key checks and empty-staging checks are explicit. The inspected decoder performs `jsonDecode` before an explicit file-byte/depth budget. This is an **input resource-admission review**, not a demonstrated browser crash.

`MASTER.md` §0 requires Firebase UID owner authority and allows an **already established unlocked owner** to retain offline local use during transient network/token failure. This does not prove a never-authenticated fresh iPad can import an LBK offline: destination owner verification/first sign-in is a separate prerequisite. The approved Sync contract is **manual delta**, not automatic PWA↔native background replication. A copied LBK is data-transfer evidence, not a Firebase Sync receipt.

### 10.3 Minimal viable FILE boundary — proposed Engineering acceptance, not an owner-approved UI design [MINTTAP DECISION / DEPENDENCY]

Do not invent a nonempty merge/reset flow, silent cloud backup, or universal save-picker capability. Implement and validate a **user-initiated, explicit-file, fresh-staging** path only after product owner approves its task/action contract:

1. **Export admission:** established matching unlocked owner, capability READY, deletion not pending; snapshot returns encoded LBK. A failure must not be labeled “backup created.”
2. **File handoff:** a user-activated browser-supported save/download path, with platform-specific fallback; record which path was used, not merely a generic “Files saved” claim. A canceled picker, blocked download, tab termination or zero-byte output is an incomplete attempt.
3. **External custody proof:** user reselects the *actual destination file*, reads exact bytes, verifies digest/format and identifies destination class without logging sensitive path/name/content. This proves point-in-time readable file, **not** second-device/failure-domain independence.
4. **Fresh restore:** a separate unclaimed staging DB, independently established matching Firebase UID authority, bounded untrusted-file admission, transaction rollback, semantic 37-store verification and owner locked until legitimate unlock. Never overwrite a nonempty existing ledger merely to make import succeed.
5. **Independent recovery:** after a permitted independent copy is evidenced, destroy a disposable source origin/profile and restore in a fresh destination; verify local semantic state, new replica and unverified remote Sync. Distinguish this from a normal same-profile reopen.
6. **User completion semantics:** only a verified file readback may support “file verified”; only a successful fresh restore may support “recovery verified”; neither implies cloud backup, cross-device Sync, or persistent EFB offline launch.

Engineering owns actual Flutter Web caller, file picker/download integration, data-size admission and tests. Track E owns trust/failure-domain requirements, Track A browser capability distinction, Track C runtime/negative oracles, Track B state/action requirements, Track D privacy/claim controls. Design Studio Content CD127 requires exact-build state→accessible-name/action parity, not static wording approval. Design Studio Web W121 keeps real device/AT/human validation OPEN.

### 10.4 Managed-iPad authority and failure-domain decision table [SOURCE / CHANGE WATCH / VALIDATION]

Apple's organizational-data and Domains deployment documentation (checked 2026-10-24) says **Safari downloads** from managed domains may be managed documents and `allowOpenFromManagedToUnmanaged=false` restricts movement to unmanaged destinations. It does **not** establish that an arbitrary managed Web Clip's download or a specific airline iPad is configured the same way:
- https://support.apple.com/guide/deployment/manage-organizational-data-depaa73a4973/web
- https://support.apple.com/en-asia/guide/deployment/depb4c146c2e/web
- https://developer.apple.com/documentation/devicemanagement/webclip

| Actual device/policy evidence | Permitted engineering judgment | Prohibited inference |
| --- | --- | --- |
| Safari tab + allowed local Files destination | Test export/reopen in that context | Local Files on same iPad = independent disaster backup |
| User-created Home Screen app + allowed destination | Test separate app container, picker/download and reimport | Safari IndexedDB was copied; Home Screen is same ledger |
| MDM Web Clip + managed domain/destination approved | Test exact MDM payload, file classification, allowed provider and cold restart | Safari-tab PASS transfers to Web Clip |
| Managed source → unmanaged destination blocked | Return policy-blocked/alternate approved route, preserve source ledger | Evade via email/clipboard/AirDrop/alternate domain |
| No verified independent destination | Mark external disaster recovery **OPEN/BLOCKED_BY_POLICY** | Claim “automatic backup” or “safe device migration” |

WebKit's 17.2 Home Screen storage-copy rule and Safari 26.0 “Open as Web App” toggle require **recording actual OS/version/installation mode/storage container**, not merely “Added to Home Screen.” Storage quota/persist() and OPFS remain same-origin failure domains and cannot replace an external LBK recovery copy. Sources: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ ; https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ ; https://webkit.org/blog/14403/updates-to-storage-policy/ ; https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system . The `showSaveFilePicker()` API is limited-availability and user-activation dependent, not an assumed iPadOS route: https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker .

### 10.5 Ordered acceptance campaign and negative controls [VALIDATION / OPEN]

This is a **sequencing and evidence-admission overlay** on existing D01–D20 and F01–F24, not another micro-case stream:
- **Gate P (product authority):** owner-approved FILE scope; exact `MASTER`/roadmap/Sync contract pin; UI actions preserve “backup vs formatted export vs import” distinctions; BACKUP-001/002 remain undecided.
- **Gate S (source+unit):** exact LogMate HEAD, actual Dart codec and adapter tests, bounded file size/depth/row materialization limits supported by representative device corpus, wrong UID/digest/format/duplicate/unknown store, R03/R04 negative regression from study 506, transactional rollback.
- **Gate W (Web runtime):** verified NORMAL artifact and served bytes, first Service Worker claim/controlled reload, populated 37-store synthetic ledger, real Web file handoff and user reselect/hash readback, fresh staged restore, actual browser process exit/reopen and explicit profile deletion recovery.
- **Gate I (iPad context):** Safari tab, user-created Home Screen web app and *actual* managed Web Clip separately; policy-allowed and policy-denied destinations, interrupted file flow, storage pressure, accessibility and manual offline cold start.
- **Gate X (cross-device and claims):** new replica identity, old source cursor/receipt not promoted to authenticated destination authority, manual Firebase Sync independent; sanitized evidence only, Marketing D8 remains PRODUCT CLAIM HOLD until target-specific PASS.

A structural source audit, synthetic test, browser download event, checksum-valid LBK, one platform PASS or MDM policy document alone **cannot** promote any subsequent gate. Reject false green from test skipped/blocked, unsupported picker, same-device copy counted as independent, restored cursor counted as ACK, or missing browser process restart.

### 10.6 Five-track judgment, dependencies and next checkpoint [TRANSFER VALIDATION / OPEN]

Allocation by risk: **E primary** (high consequence of pilot data loss and policy violation); **A/C critical suppliers** (WebKit/Safari/Worker/storage and independent runtime/failure oracle); **B** elevated because a premature “backup complete” or “synced” message misrepresents irreversible user decisions; **D** challenger because public claims/telemetry must not exceed evidence. One reusable source finding per owner, no duplicated Design Studio/Engineering/Marketing primers.

**TRANSFER:** Software Engineering Studio `research/README.md` records D006 sync interruption and M006 browser lifecycle as bounded non-product transfer; its Q006 CI evidence guards against successful job status hiding failed semantic oracles. Marketing Manager `STATUS.md` (2026-10-24 22:37 KST) explicitly keeps LogMate PWA/import/export/Sync promotional claims on HOLD. Design Studio W121/CD127 require exact-run implementation/accessible/human evidence; none authorizes visual copy from a static protocol.

**NEXT DECISIVE ACTION:** Engineering should implement the *owner-approved minimal FILE task surface* and execute the populated, synthetic, 37-store external-file round trip on exact NORMAL Web artifacts; then run the physical managed-iPad policy envelope. This is a materially different implementation/runtime boundary, so another synthetic-only model is not a substitute.

**Verdict:** Stage 8 applied security/trust remains ACTIVE; generic curriculum PASS unchanged; product FILE complete-flow **NOT IMPLEMENTED** per canonical roadmap; Production validation **OPEN**; PWA release **HOLD**. No LogMate, Design Studio, Marketing or Engineering files modified.
