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


## §11 — Canonical PWA origin, Firebase default-host aliases and offline-ledger continuity (2026-10-26 KST)

**Evidence class:** SOURCE / SYNTHESIS / CONTRADICTION / MINTTAP DECISION (proposed release admission) / DEPENDENCY / VALIDATION (not executed) / TRANSFER VALIDATION / CHANGE WATCH. **Track E owns** release/domain/authority and irreversible local-data consequences; A owns origin/manifest/Worker mechanics; C owns falsifying runtime evidence; B/D consume the finding. This is a *new origin-topology contradiction* complementary to §§9–10 and 519 §24, not a new backup or Sync implementation.

### 11.1 History/problem → principle → standard [SOURCE / FOUNDATION]

Early web deployment treated a URL change as mostly a navigation/SEO problem. A local-first installed PWA changes the consequence: its service-worker registration, Cache Storage and IndexedDB live in a browser storage context keyed by origin (and potentially further partitioned by user agent). A hostname change can therefore strand the only copy of an offline ledger while showing the user the same app name, icon and authenticated Firebase account.

- **Origin ≠ site ≠ Firebase project ≠ product identity.** A web origin is scheme + host + port; different subdomains are different origins. WHATWG Storage Standard storage keys currently include origin; partitioning implementation details are a separate browser change watch. The same Sembast database name on different origins does **not** refer to one physical IndexedDB database. Same Firebase project and even the same UID do not imply a shared local ledger.
- **Worker/manifest separation.** Service workers register against same-origin script/scope. Web App Manifest \`id\` must be same-origin with \`start_url\`; if absent it defaults to \`start_url\`. A manifest ID cannot turn two origins into one IndexedDB or migrate an installed iPad app's data. HTTP redirects, \`rel=canonical\` and DNS CNAMEs change navigation/discovery/routing, **not** browser storage ownership.
- **Historical evolution:** AppCache's implicit document-bound caching model was replaced by explicit Service Worker registration/fetch/lifecycle controls; neither model authorizes cross-origin access to another site's IndexedDB. For offline-first systems, URL topology is part of data-custody architecture, not merely branding.
- **iPad extra dimension:** WebKit documents that a Home Screen web app's data is isolated from Safari; iOS/iPadOS 17.2 creation copies eligible *cookies only*, not IndexedDB. Safari 26 permits Home Screen creation as a web app by default or a browser bookmark by choice. Thus \`same origin\` is necessary but **not sufficient** to assert \`same storage container\` across Safari/Home Screen/MDM Web Clip.

Primary current standards/platform sources checked 2026-10-26:
- WHATWG Storage Standard: https://storage.spec.whatwg.org/
- MDN same-origin policy: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy
- W3C Web Application Manifest, \`id\`, \`start_url\`, scope: https://w3c.github.io/manifest/
- W3C Service Workers: https://w3c.github.io/ServiceWorker/
- WebKit Safari 17.2 one-time cookie copy: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/
- WebKit Safari 26 Home Screen installation choice: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

### 11.2 Exact LogMate repository and host census [SOURCE / STATIC VALIDATION]

Pinned read-only source: \`yhappcom/logmate main@26d2d7cf2c20c55026c6f84b838dcb6442f7a3f1\` (checked 2026-10-26). Source objects and their exact meanings:

| Source | Observed exact property | Consequence / evidence limit |
| --- | --- | --- |
| \`docs/operations/domains-and-auth-email.md\` | Canonical PWA/public target \`logmate.minttap.app\`; Web \`authDomain\` same host; sender \`auth.logmate.minttap.app\`. Owner-observed signup verification at custom host 2026-10-04. | The *target* host is established; this is not a current live three-host HTTP response census. Sender subdomain is not the PWA origin. |
| \`lib/repository/logbook/sembast_database_opener_web.dart\` | \`databaseFactoryWeb.openDatabase('logmate_ledger')\`. | Same database **name** under multiple origins yields different origin-local storage; the adapter does not implement cross-host migration. |
| \`lib/firebase_options.dart\` | Web Firebase project \`logmate-pilot-logbook\`, \`authDomain: logmate.minttap.app\`. | One Auth backend can be used by pages at multiple origins, but the project/UID is not a browser-storage namespace. API keys and other configuration values are intentionally not copied into this study. |
| \`web/manifest.json\` | \`start_url: "."\`, \`display: "standalone"\`; no explicit \`id\` or \`scope\`. | With root-hosted manifest, the standards fallback identity is the **root URL of each served origin**; no cross-origin identity continuity is established. This is a specification-level derivation, not an actual iPad install observation. |
| \`web/index.html\` | Relative manifest link; Flutter base-href substitution; no inspected hostname restriction in this file. | The same generated site can be opened on multiple hosts if Hosting serves it; the actual deployed bytes/host policy remain OPEN. |
| \`firebase.json\` | Hosting \`public: build/web\`, global \`no-cache, no-store, must-revalidate\` header, three \`/auth*\` rewrites; **no configured redirects** or host-specific routing in this source. | A source-level host-canonicalization gap, **not** proof all three hosts currently serve HTTP 200. Firebase Hosting's reserved \`/__/*\` namespace and redirect/asset/rewrite precedence matter. |
| \`docs/specs/local-first-manual-delta-sync-contract.md\` | Backup-file transfer prioritized; manual delta sync approved but production Sync not implemented. | An alternate-host ledger cannot be presumed to reappear via unattended cloud/device sync. |

Firebase Hosting's **default-site documentation**, updated in the 2026-10-15 default-site creation transition, says the default site has two provider domains (\`SITE_ID.web.app\`, \`SITE_ID.firebaseapp.com\`) that serve deployed site content. LogMate's existing project predates that creation-policy change; its documented default aliases are \`logmate-pilot-logbook.web.app\` and \`logmate-pilot-logbook.firebaseapp.com\`. The custom host is a third distinct origin. The repository's 2026-10-04 Firebase Authorized Domains inventory included all three. **An Authorized Domains allowlist is not a Hosting HTTP reachability/redirect observation.**

Deterministic **URL-resolution diagnostic** (Python \`urllib.parse\`, not a browser run): applying the root \`manifest.json\` and relative \`start_url "."\` to the three documented URLs produces three distinct implicit IDs:

| Candidate served origin | Implicit manifest ID, if the manifest is served at root |
| --- | --- |
| \`https://logmate.minttap.app\` | \`https://logmate.minttap.app/\` |
| \`https://logmate-pilot-logbook.web.app\` | \`https://logmate-pilot-logbook.web.app/\` |
| \`https://logmate-pilot-logbook.firebaseapp.com\` | \`https://logmate-pilot-logbook.firebaseapp.com/\` |

**Live admission attempted, not established:** read-only GETs through the available web retrieval interface to all three hosts returned inaccessible-tool results, not trustworthy HTTP status/redirect/body evidence. A separate live-scrape provider failed with insufficient credits. Record **LIVE HOST RESPONSE = UNKNOWN**, not \`404\`, \`200\`, \`redirect verified\` or an outage. No browser, Dart, Firebase Console, deployment or physical iPad execution occurred.

Provider sources:
- Firebase default Hosting site and 2026-10-15 creation policy: https://firebase.google.com/docs/hosting/default-site
- Firebase Hosting config and precedence (\`/__/*\` reserved → redirects → exact static → rewrites): https://firebase.google.com/docs/hosting/full-config
- Firebase multisite/related domains: https://firebase.google.com/docs/hosting/multisites

### 11.3 Threat/failure-mode chain and discriminating counterexamples [SYNTHESIS / CONTRADICTION]

1. **Same product, different local ledger.** A pilot saves F1 offline at the provider host and later opens the branded host. Both pages could present LogMate and allow authentication with the same Firebase UID while the new host's \`logmate_ledger\` is empty. **Conditional source/platform consequence, not an observed lost flight.** This is distinct from ordinary account/UID mismatch.
2. **A premature redirect can hide irreplaceable data.** Redirecting the old host before exporting its populated ledger may make the old origin difficult to reopen online; changing DNS or removing old Hosting content does not copy IndexedDB. A stale installed Worker may keep an offline old-origin app usable for a time, but that is neither a migration mechanism nor a recoverability guarantee.
3. **Canonical metadata solves a different problem.** \`rel=canonical\` can consolidate search signals; it does not redirect human navigation or move storage. A \`301/308\` can direct users and search engines but **also does not transfer IndexedDB**. A CNAME is a DNS resolution alias, not a browser-origin alias. A common Firebase project/UID is not a storage bridge.
4. **Manifest ID does not merge origins.** Adding \`"id": "/"\` can stabilize an app's identity *within one origin* under appropriate browser support; the standard's same-origin rule means \`id: "/"\` at the three hosts remains three identities. The missing explicit ID also deserves same-origin path/start URL change testing; it is not proof a current installed icon is broken.
5. **Auth can succeed while local state remains absent.** The custom \`authDomain\` and \`/auth\` action handler can process verification independently of which origin contains the ledger. Same UID may be a necessary backup-restore ownership condition but is not proof that the source data is present, that a file was transferred, or that a Sync receipt exists.
6. **Installed iPad multiplies the problem.** Safari tab, installed Home Screen web app, MDM Web Clip and another installed copy must not be assumed to share storage merely because their URL host strings match. Conversely, an MDM restriction may block the external Files handoff needed for migration. A “reinstall” instruction without a verified independent LBK is unsafe.
7. **Old host remains a possible stale client.** If both hosts can launch, old-host clients may continue offline local writes under a different Worker/cache generation. Future Sync must reconcile authenticated operation lineage/replica and explicit receipts, not infer current authority from host, Firebase project or timestamp. Production Manual Sync remains OPEN.
8. **A global redirect rule may break unrelated paths.** Firebase Hosting's reserved \`/__/*\` Auth helpers and custom \`/auth\` action routes need independent host/path behavior. A naive \`"source": "**"\` redirect applied to a shared Hosting site is not an approved solution; it may affect the canonical host as well as provider aliases, and redirects outrank rewrites/static files.
9. **Duplicate search URLs ≠ duplicate data.** Google Search Central ranks redirects/canonical/sitemaps as canonicalization signals. Search de-duplication and attribution must be treated separately from browser ledger continuity; fixing SEO alone cannot authorize deleting an old-origin dataset.
10. **Host policy must survive operational transitions.** A future custom-domain renewal, Hosting site split, CDN move, MDM bookmark update or incident rollback could reintroduce an alternate origin. Rollback to the previous hostname is not a data rollback or remote-authority reset; the old origin's storage and installed Worker may persist.

**Security invariant:** Do not retire, redirect, erase or revoke an origin that may hold unique user data solely because another hostname serves a valid PWA build. Preserve user-owned data and a verifiable recovery path *before* switching navigation/installation authority. This is a **proposed release guard** pending product owner/Engineering/MDM approval, not permission to deploy a redirect or collect private flight data.

### 11.4 One integrated remediation/operational decision [MINTTAP DECISION — PROPOSED, NOT IMPLEMENTED]

**A. Canonical host admission first.** The already documented target is \`https://logmate.minttap.app/\`. Engineering/operations should verify exact live responses, redirect chains, \`/auth\` and Firebase reserved namespaces, Worker script/manifest, and installed launch origin on **each** documented host. Do not infer host behavior from Firebase Console Authorized Domains, DNS records or repository config alone. Distinguish which Hosting sites/targets actually serve which artifact.

**B. If alternate hosts are empty/unreleased:** prefer one approved launch/install URL and a **host-aware** alternate-host navigation policy *after* verifying no real pilot ledger is stranded. A host-aware redirect may require separate Hosting site/configuration or infrastructure controls; \`firebase.json\` path rules alone are not an established host-specific switch. Preserve Auth helper behavior and signed action links. Document the chosen canonical host in user-facing instructions, Store links, QR codes and MDM Web Clip payloads.

**C. If an alternate host may already contain data:** do not auto-redirect it away on first request. Provide a controlled *old-origin* read/export and independent file readback, confirm a permitted external custody destination, then establish matching verified owner and fresh empty staging at the canonical origin, restore/compare all 37 stores with the intentional Replica-ID and Sync-authority rules from 515/516/519, and only then retire the old launch path. A redirect-only cutover is a **FAIL**. Any later automatic Sync bridge is a distinct owner-approved product feature and cannot be substituted for verified file custody today.

**D. Identity and installation governance.** Propose a stable explicit same-origin manifest \`id\` and \`scope\` **only** after Engineering validates compatibility with already installed versions, Worker scope and iPad behavior; changing manifest fields alone does not migrate storage. On managed EFB, obtain actual Web Clip/Managed Open In policy and allowed export destination. If policy prohibits a verified independent copy, mark migration **BLOCKED_BY_POLICY**, preserve the old origin and escalate rather than bypassing controls.

**E. User/AT language.** B consumes Design Studio CD115 (local saved/synced/unknown) and CD052 (recovery authority). The product must distinguish \`This installation has no local records\` from \`Your records were deleted\`; \`Backup file verified\` from \`New installation restored\`; \`Signed in\` from \`Records transferred\`. Avoid inventing specific UI copy or promising recovery before Engineering provides a real path. C verifies focus/status/accessibility on real Web runtime; W121 keeps physical/human validation OPEN.

**F. Search/analytics and privacy.** D consumes Google Search Central canonical/redirect evidence and Marketing D8/D9 HOLD. Publish canonical host references and prevent duplicate acquisition routing, but never put Firebase UID, flight record IDs, backup contents, action-link tokens or file paths into URL parameters, manifest start URL, referrer telemetry or analytics. A canonical URL signal is not proof of local-data migration.

### 11.5 Falsifiable acceptance overlay on existing product Work [VALIDATION / DEPENDENCY]

Reuse LogMate **W-012/013/014** for real B1 file round trip, **W-030** for account/UID continuity, **W-031** for installed PWA and **W-036** for release. This is one multi-host **variant of the existing campaign**, not another permanent parallel micro-test suite.

| Boundary / negative control | Minimum independent evidence | Fail/UNKNOWN rule |
| --- | --- | --- |
| Three-host route inventory | DNS/TLS + final URL/status/headers/body hash + redirect chain for root, manifest, Worker, \`/auth\`, \`/__/*\`, privacy/account-deletion; exact approved NORMAL artifact identity | Unreachable tool, unapproved environment, missing route, or HTML-only assertion = UNKNOWN; no \`LIVE PASS\`. |
| Same-origin storage separation | Disposable F1 created and DB transaction-completed on host A; independent clean host B read and host A reopen; separately capture browser profile/container | A visible F1 on B without a documented transfer requires investigation; absent F1 on B is expected isolation, not deletion proof. |
| Same UID vs distinct local DB | Independently authenticate disposable same UID on both origins and compare *local* 37-store semantic state/replica, without remote Sync | Same UID alone cannot PASS data continuity; an empty B is not proof A lost data. |
| Manifest/Worker/install identity | Fetch exact served manifest; assert effective \`id/start_url/scope\`, Worker registration/controller, browser display mode, launch URL, origin and container | \`Add to Home Screen\` screenshot or Worker \`active\` alone is not proof. |
| Populated old-origin retirement | F1+F2 on old host; explicit LBK file export, independent readback, new-host fresh restore and semantic comparison; old Worker offline launch before/after cutover | Redirect before independent custody or loss of old-origin access without recovery = FAIL/HOLD. |
| Wrong-owner and interrupted transfer | Wrong UID, corrupt/oversized file, canceled picker, mid-restore termination and DB reopen; no active-ledger overwrite | Digest match or picker close is not restore PASS; preserve original file and ledger. |
| Auth and reserved-route parity | Firebase action links and \`/__/*\` behavior per host, no token leakage/redirect-loop, signup verified only where actually tested | Do not generalize 2026-10-04 signup smoke to reset/recover-email. |
| Device/policy matrix | macOS Safari, iPad Safari tab, Home Screen web app, and actual supervised MDM Web Clip as **separate** tiers; allowed/denied managed Files destination | Desktop Chromium/Playwright WebKit does not certify managed iPad. |
| User/AT and discovery | Exact state→action→result/accessible status; canonical Search/Store links, privacy-safe host/variant metrics | \`Synced\` or \`Recovered\` without proof, or canonical SEO PASS counted as ledger PASS = FAIL. |
| Rollback/old-client | Reopen old-origin installed client offline after canonical switch, then reconnect under explicit current owner/Sync admission; inspect any old queued operations | Old client remote authority is not inherited; no blind replay or forced origin clearing. |

Evidence tiers: **T0** repository source + deterministic URL derivation (this study); **T1** verified hosted responses/actual artifact; **T2** real browser/profile + data readback; **T3** physical Safari/Home Screen; **T4** representative MDM EFB + independent Files destination; **T5** production release and incident/recovery authorization. A tier never implies the next. **This run reaches T0 only.**

### 11.6 Five-track allocation, cross-specialist transfer and checkpoint [TRANSFER VALIDATION / OPEN]

| Track | Curriculum/evidence maturity and pressure | Owner/transfer |
| --- | --- | --- |
| **E — Security/Operations** | Stage 8 dominant; source evidence strong, host/runtime/MDM unknown; possible irrecoverable local ledger consequence | Own canonical-host, retirement order, old-origin custody, deployment/rollback, authority and release HOLD. |
| **A — Platform/Browser** | Standards and exact manifest/opener available; installed-context behavior unresolved | Supply scheme/host/port, Worker origin/scope, manifest identity, IndexedDB and WebKit container distinction. |
| **C — Quality/Accessibility** | High diagnostic pressure; no three-host or real iPad execution | Independently falsify host split, actual file recovery, AT/human and negative controls, provenance-bearing verdict. |
| **B — UX/IA/Content** | CD115/CD052 state taxonomy mature, product migration UI absent | Consume data-presence/recovery truth; no premature deleted/synced/recovered language. |
| **D — Search/Discovery/Analytics** | SEO primary standards mature; live canonical/Store metrics unknown | Consume canonical-host policy, check redirects/canonical links and privacy-minimized acquisition, Marketing owns claims. |

**Cross-specialist evidence:** Design Studio \`research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md\`, \`research/content-design/CD115-runtime-status-recovery-language-20260920.md\`, \`research/content/CD052-delete-update-recovery-language-system.md\` (static semantic only; runtime/human OPEN); Software Engineering Studio \`research/README.md\` M006/D005/D006/Q006 (bounded lifecycle/recovery/Sync/CI transfer, not product execution); Marketing Manager \`STATUS.md\` D8/D9/D10 (PWA/import/export/Sync/ads claims HOLD). Peers are **read-only**; Web Manager does not duplicate or change their domain artifacts.

**Additional primary discovery sources checked 2026-10-26:**
- Firebase Hosting custom domain: https://firebase.google.com/docs/hosting/custom-domain
- Google Search Central canonical methods (SEO only): https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google Search Central site migration/redirect guidance: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- MDN Service Worker register same-origin requirement: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
- MDN Manifest \`id\` browser support watch: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/id

**CHANGE WATCH:** 2026-10-15 Firebase default-site creation policy applies to new projects differently, not retrospectively to LogMate's older existing site; Firebase custom-host/redirect configuration; W3C Manifest identity and browser implementation; Chromium origin-migration experiments (do **not** assume Safari/managed-iPad support or storage transfer); WebKit iOS 26 Home Screen installation toggle; Apple MDM Managed Open In; exact LogMate NORMAL Hosting and Auth deployments; approved file-flow and Manual Sync implementations.

**Adjacency check and stop:** This section resolves the previously unarticulated *same-app/multiple-origin/local-data split* with pinned source, current standards, explicit counterexamples and an existing-Work execution bridge. The immediately adjacent question—can any of the three hosts currently serve or redirect a populated, installed LogMate ledger?—requires live approved response/browser/MDM/FILE evidence unavailable in this run. More speculative host-specific redirect code or synthetic test cases would not close that gate. **Stage 8 ACTIVE; generic curriculum PASS unchanged; source-level host-topology contradiction newly recorded; production validation OPEN; PWA release HOLD.** No product, Marketing, Design Studio or Software Engineering modifications.


## §12 — 2026-10-28 product-main reconciliation: W-004/W-012 native closure is not installed-PWA ledger custody [SOURCE / SYNTHESIS / CONTRADICTION / TRANSFER VALIDATION / OPEN]

### 12.1 Why this changes the evidence map, not the release gate [SOURCE]
Read-only latest LogMate `main@2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf` (merge PR #31 at 2026-10-28 10:28 UTC), seven commits ahead of previously audited `1c4fb1b`. Exact compare reports changes to Draft Repository, its new native test and W-004 evidence/checklist; **`tool/pwa_precache.dart` remains blob `90a67954af618a4e18199fa92555491c56167c17`**. Thus the earlier Worker source-level repair and cross-generation questions have **not** been fixed or invalidated by this new product merge. The Draft Repository is now blob `021d9001ae1240a824c5df570fb679597edc3875`.

The product's own [Stage 3 acceptance checklist](https://github.com/yhappcom/logmate/blob/2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf/docs/stage3-product-integration-acceptance-checklist.md) now records 37 Work items: **4 COMPLETE (W-001/W-004/W-012/W-019), 1 IN PROGRESS (W-031), 32 NOT STARTED**. This is a Work-card count, **not** product release percentage. W-005 Draft UI, W-013 File UX, W-014 device transfer, W-020/021 authenticated remote Sync/Apply and W-036 release remain unexecuted in their respective scopes.

| Exact product evidence | Bounded verified claim | Claim that must NOT transfer |
| --- | --- | --- |
| [W-004 source `911b85a`](https://github.com/yhappcom/logmate/commit/911b85a7234e53eddc35630fe0bb08475bf5999c), [raw results](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w004-draft-fix-2026-10-28/test-results.json) | macOS host `sembast_io` temp-file DB, focused **52 PASS**, full **931 PASS/1 SKIP**; previously observed Custom field Revision/key/null cannot be silently rebaselined, while a genuinely unobserved field may be first-observed; file close/reopen, CAS, retry and selected rollback seams | Actual `sembast_web` IndexedDB W-004 regression, concurrent browser tabs, Safari installed container, power loss, Owner Auth or UI PASS |
| [W-012 native review](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w012-empty-destination-backup-2026-10-27.md), source `63e7c1a` | Native B1 empty-destination v1/v2 restore, collision/foreign-owner fail-closed, 37-store rollback and trust reset, focused **70 PASS**, full **900 PASS/1 SKIP** at original test SHA | Browser File picker/export, managed Open In, nonempty merge, cross-device file custody, PWA restore, new remote Receipt/ACK or verified destination Apply |
| [W-031 Safari evidence](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w031-simulator-preacceptance-2026-10-27.md) | iPadOS 26.1 Safari **tab**, synthetic unbound Acceptance Harness: limited IndexedDB reopen, Worker registration/control and cached relaunch with origin unavailable | Authenticated NORMAL ledger, installed Home Screen, MDM Web Clip, physical EFB, quota/eviction or 37-store restore |
| [Web reopen test source](https://github.com/yhappcom/logmate/blob/main/test/repository/logbook/sembast_web_reopen_test_browser.dart) | A browser-specific test exists for canonical create/delete/restore and reopen | The native W-004 full-suite **1 SKIP** explicitly identifies browser-only reopen; the host test did **not** execute this browser path |

**CONTRADICTION:** The product now has materially stronger native-file correctness evidence than this study's older baseline, but neither a green native suite nor an unchanged PWA Worker is evidence of web storage durability or safe cross-container migration. The original W004-F01 failure was **Draft baseline reclassification**, not a demonstrated overwritten Flight; the corrected native guard is real code, not a generic assurance of all web interleavings. The original W012-B01/B02 red cases were resolved within the approved native empty-destination scope; they do not authorize automatic backup or Sync.

### 12.2 First principles → standards → failure domains [SOURCE / SYNTHESIS]
- **Transaction safety versus durability:** a completed IndexedDB transaction is an application-level commit boundary, not proof of power-loss persistence, external backup, or eventual synchronization. Browsers may abort transactions on I/O/quota/crash; do not split a destructive clear and repopulation into independent transactions. [MDN IndexedDB transaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction); [MDN Using IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB).
- **Storage persistence versus custody:** `navigator.storage.persist()` is a request with browser-dependent grant behavior, not a guaranteed backup. WebKit may evict an origin under storage pressure/overall quota; `persisted()` must be observed in the actual context and still cannot replace a tested external file. [WebKit storage policy, 2023-08-10](https://webkit.org/blog/14403/updates-to-storage-policy/); [MDN StorageManager.persist](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist).
- **Origin versus installed container:** WebKit states iOS/iPadOS 17.2 Home Screen creation may copy cookies once, but **no other local storage** is copied; after creation, data is not shared. The 2026 iPadOS 26 install UI change does not repeal this documented data boundary. The Safari-tab W-031 result therefore cannot imply an installed app starts with the tab's ledger. [WebKit Safari 17.2, 2023-12](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/); [WebKit Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/). Current physical iPad behavior remains **CHANGE WATCH / OPEN**.
- **Data authority:** a restored operation/history/Receipt is *source provenance*, not a fresh destination server ACK or applied Cursor. W-012's restored HOLD/trust-reset protections and W-004's immutable observation baselines are separate invariants; one cannot substitute for the other. An old client pinned to a verified shell is also not automatically the current authorized Owner.

### 12.3 One product-owned discriminating campaign, not another pure-state fixture [DEPENDENCY / VALIDATION OPEN]
The next high-information-gain test must use an **Engineering-approved exact NORMAL artifact** with source/Worker SHA, real `sembast_web` IndexedDB, disposable verified Owner fixture, and independently captured raw store snapshots. Reuse existing product Work W-004/W-005/W-012/W-013/W-014/W-031 and the RP01–RP12 gates from research 514; do not create an unapproved product Work or rewrite their implementations.

| Gate | Positive control | Negative / false-green control | Evidence status |
| --- | --- | --- | --- |
| WEB-D01 | On same-origin NORMAL web DB, Edit Draft with already-observed Custom field, reopen, original Revision preserved | Other tab updates observed Revision, then stale Draft update attempts to replace observation: **reject, full-store snapshot unchanged**; test absent key vs explicit null separately | OPEN; native W-004 is not this test |
| WEB-D02 | New unobserved Custom field's valid first observation and explicit intent succeeds after reopen | Reject false first observation, lost intent CAS, changed record baseline and cleared review fence | OPEN |
| WEB-D03 | Two real tabs, same Owner, concurrent Draft updates: only authorized CAS winner, loser retains original recoverable Draft; repeat after tab close/reopen | A UI 'ready' message or one-row count alone is insufficient; compare record/Custom/Outbox/Receipt/aggregate and whole registry | OPEN |
| WEB-B01 | Native-produced, authenticated and format-validated .lbk exported through an approved file route; independently transferred to a *different* empty installed web container; 37-store semantic readback and Owner lock | Foreign Owner/Replica, malformed/digest-invalid archive, HOLD key collision and interrupted import must reject without partial mutation | OPEN; W-013/W-014 prerequisites |
| WEB-B02 | Restore under distinct destination Replica/Owner policy and preserve source provenance | No new ACK, applied Cursor, Sync READY, verified backup or same-origin data-sharing claim from restore success alone | OPEN |
| WEB-P01 | Same exact NORMAL build across Safari tab, separately installed Home Screen, managed Web Clip and physical EFB; each independently writes/reopens and performs approved file backup/restore | Start Home Screen after tab-only write: do **not** silently report tab data as migrated; blocked MDM file route is a distinct failure | OPEN |
| WEB-R01 | Worker update/repair while Draft and pending Outbox exist: verified old shell, stable data and non-destructive recovery | Delete active shell, cross-generation catalogue collision, offline repair, storage eviction and interrupted candidate; no cache-clear-as-repair | OPEN; research 514 synthetic results not product |

**Execution custody:** use disposable account and test data; do not export real pilot records, secrets or auth tokens into public Web Manager CI. Capture source/commit/build/Worker hash, browser/OS/device, origin and installed context, fault injection, actual response/store bytes and negative-control outcomes. The product owner/Software Engineering must approve any test requiring private runtime, source modification or managed-device enrollment. Do not infer that normal mobile network availability implies direct unattended native↔PWA device Sync or hotspot permission.

### 12.4 Five-track allocation, decisions and adjacent-value check [TRANSFER VALIDATION / MINTTAP DECISION / OPEN]
- **E — primary bottleneck:** release provenance, backup file custody, restore trust reset, Owner/Receipt authority, Worker repair without origin-data deletion, deployment rollback and managed-device operational constraints.
- **A — platform dependency:** IndexedDB transaction boundaries, `sembast_web` close/reopen and cross-tab lifecycle, Service Worker generations, Safari tab versus installed-container storage isolation.
- **C — independent oracle:** exact source/run binding; original W004 red-to-green distinction; full registry snapshots; browser-only skip interpretation; screen-reader/keyboard/zoom and failure-path accessibility remain unverified.
- **B — recovery UX consumer:** distinguish stale Draft requiring review, safe new observation, absent local ledger, imported backup not yet trusted, and shell-repair-required; Design Studio W121 Stage 3 PRACTICE remains the interaction authority.
- **D — claims/measurement consumer:** native test PASS is not an offline-installed/automatic-Sync promise; Marketing D8 holds EFB/offline/Sync claims pending actual approved device evidence.

**MINTTAP DECISION (research gate only):** recognize W-004/W-012 as **native-scope product Work closures**, update the Web Manager's evidence ledger, and keep **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**. Do not approve a Web UI, file-flow implementation, direct P2P Sync or release from this transfer. **OPEN:** WEB-D/B/P/R gates above, actual installed WebKit and managed EFB, real 37-store web restore, authenticated Manual Sync/Apply and destructive-fault recovery. **CHANGE WATCH:** WebKit storage/installation/MDM, browser quota/eviction and future LogMate source revisions.

**Adjacent-value decision:** the material new fact was the actual merged native product source and verified test scope; it has been reconciled against platform standards and existing browser/backup gates. A further synthetic case-count expansion cannot close the remaining product-runtime, file-transport or managed-device boundary. Next useful execution is Engineering-owned exact NORMAL web W004 baseline regression plus W012 file flow and W031 installed-device context. No peer/product repository was modified.


## §13 — 2026-10-28 untrusted .lbk file admission, confidentiality and managed-iPad recovery proof [SOURCE / SYNTHESIS / DEPENDENCY / VALIDATION OPEN]

**Owner:** Track E (backup admission, data-custody and security). **Suppliers:** A (File/Blob/IndexedDB browser mechanics), C (failure-oracle and memory/device execution). **Consumers:** B (recoverable status and action architecture), D (claims and privacy-preserving telemetry). This section strengthens the *existing* W-012/013/014/031 product campaign, not a new Work item or another synthetic state model. It does not alter the approved Manual Delta Sync policy.

### 13.1 Exact source checkpoint and trust boundary [SOURCE]

Read-only LogMate main **2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf**, 2026-10-28. The Web opener **lib/repository/logbook/sembast_database_opener_web.dart**, blob **87f043d582375a7d11a8183889f2f23195396ef1**, opens a named Sembast Web database. The B1 codec **lib/repository/logbook/whole_ledger_backup.dart**, blob **711f784534bc686a4d8edd6617ac4d1ac362e0a7**, declares an integrity container, *not* encryption or author authentication. It accepts JSON with exactly the two root keys manifest and stores; each store value must be a list and each row a map. It materializes the entire jsonDecode result, builds another map of per-store row lists, and canonicalizes recursively when encoding. Its SHA-256 helper first UTF-8 encodes the whole string and copies it into a padded integer list. **No explicit byte, row-count, depth or cumulative field-size admission bound appears in this codec source.** That is a static observation about this file, not proof of a browser crash, exploit or unbounded behavior of the surrounding restore caller.

The approved Manual Delta Sync contract (blob **2240fc1b6adf5fcd041a44de0e4660eb1528e92a**) states that an independent restored database receives a new Replica ID; a source receipt or applied cursor is not a fresh destination server acknowledgement. W-012 native empty-destination restore is product-tested in its own scope; it does not execute this Web file-picker and browser-memory path.

### 13.2 First principles: a checksum-valid file is still an untrusted file [SYNTHESIS / SECURITY]

The crossing is **outside file provider or browser download → user-selected bytes → parser → semantic validation → destination transaction → independently read-back local ledger**. A user choosing a file is consent to *read it*, not evidence of file origin, ownership, freshness, safe size, safe structure, or authorization to replace a ledger. An attacker who can edit plaintext JSON can recompute an unkeyed SHA-256 checksum; a digest checks accidental or unsanctioned change against an expected value, not who produced it. Firebase login and file Owner checks remain separate gates.

The file is plaintext and may contain sensitive pilot flight history and local Sync metadata. It is **not encrypted** merely because it has a SHA-256 digest, a .lbk extension, an opaque filename or HTTPS delivery. The exact contents and whether a particular file contains personal information depend on the populated source ledger; do not export production records into public test fixtures. Confidentiality requires an owner-approved storage/destination and, if necessary, a separately designed encryption/key-recovery policy. Do **not** silently add encryption that makes a user's only recovery copy unrecoverable.

### 13.3 Browser File API capability versus a completed external backup [SOURCE / CHANGE WATCH]

A standard HTML file input is widely supported and gives the page File objects explicitly selected by the user; its accept attribute is a **chooser hint, not a validation boundary**. File.size is available for a pre-read budget check. File/Blob streaming APIs can support chunked processing, but calling a streaming read before a full in-memory jsonDecode does not make the JSON parse bounded. The File System Access showOpenFilePicker/showSaveFilePicker methods are **limited-availability** and require secure context and transient user activation. Therefore an iPad backup design cannot depend on them without exact Safari/installed-app testing. A Blob object URL can enable download flows where supported, but the application must revoke it when safe; neither URL creation nor a download event proves a durable, retrievable file at a policy-approved destination.

Primary references checked 2026-10-28: [MDN file input](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file), [File API](https://developer.mozilla.org/en-US/docs/Web/API/File_API), [Blob.stream](https://developer.mozilla.org/en-US/docs/Web/API/Blob/stream), [showOpenFilePicker](https://developer.mozilla.org/en-US/docs/Web/API/Window/showOpenFilePicker), [showSaveFilePicker](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker), [revokeObjectURL](https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static).

**Validation distinction:** DOWNLOAD_TRIGGERED ≠ USER_SELECTED_DESTINATION ≠ FILE_EXISTS ≠ INDEPENDENT_READBACK_VERIFIED ≠ NEW_INSTALLATION_RESTORED. A same-origin OPFS copy is still subject to that origin's storage-failure domain and is not an independent disaster-recovery copy.

### 13.4 Resource-exhaustion and interrupted-admission failure model [SOURCE / SYNTHESIS]

The codec's full JSON parse, per-row materialization and SHA helper can each create live allocations proportional to input size; nested maps/lists add recursive work. Peak live memory is not simply the on-disk file size, and no safe numerical ceiling can be inferred from source alone. The relevant adversarial inputs are (a) oversized but syntactically valid JSON; (b) many tiny rows; (c) few enormous string fields; (d) deeply nested values; (e) duplicated or unexpected store names and malformed row types; (f) correct syntax but wrong UID, Replica, digest, version or schema; (g) interrupted file read; (h) app suspension/termination during validation or destination commit; (i) quota exhaustion; and (j) a valid old snapshot that predates later edits or tombstones.

**Admission ordering proposed for Engineering review, not implemented:** check browser File.size against a device-calibrated byte budget before reading; reject unsupported media/format *by parsed content* rather than trusting extension/MIME; use bounded parse and row/depth/field/total-work budgets where the chosen parser actually enforces them; validate the complete manifest/store inventory, owner and semantic invariants before destination mutation; stage and commit atomically; reopen the destination and compare all 37 store families plus protected trust metadata. If the parser cannot enforce a required limit before full materialization, that limit remains **OPEN**, not a documented guarantee. A preflight file-size check alone does not bound expansion, row count or nesting. No threshold is approved until measured on representative low-memory iPad/browser profiles with ordinary large logbooks and hostile fixtures.

### 13.5 Transaction consistency and backup age are independent [SYNTHESIS / CONTRADICTION]

A transactionally consistent snapshot can still become stale the moment a later flight edit commits. A file may pass checksum, format, UID and all-store validation yet omit that later edit. A downloaded file's name, file modified timestamp or a client clock cannot prove the latest ledger generation. Conversely, a failed export must not be reported as a failed local save. Preserve source provenance and a user-visible, evidence-based backup age/verification state where product metadata actually supports it; the existing B1 manifest does **not** establish a globally attested current-head generation. A restore must not mint new modification UTC timestamps for historical operations, silently resurrect a later deletion, or treat restored source receipts/cursors as new server ACKs. This follows the approved Manual Sync contract, not a new LWW policy.

### 13.6 Apple managed-iPad policy is a security authority, not a UI inconvenience [SOURCE / CHANGE WATCH]

Apple's deployment guidance states that Safari downloads from a **managed domain** can be classified as managed documents, and Managed Open In settings may prohibit movement to unmanaged destinations. It does **not** establish the actual airline MDM payload, classification of a particular Home Screen/MDM Web Clip export, or which Files provider is permitted. On a denied route, the correct outcome is **BLOCKED_BY_POLICY**, preserving the source ledger and offering only an administrator-approved recovery path. Do not suggest emailing a file, using AirDrop, changing hostnames or clipboard transfers to evade restrictions. An allowed on-device Files location is not automatically independent of device loss or MDM wipe. Source: [Apple Manage organizational data](https://support.apple.com/guide/deployment/manage-organizational-data-depaa73a4973/1/web/1.0) (published 2025-09-24); [Apple Web Clip](https://developer.apple.com/documentation/devicemanagement/webclip). WebKit confirms Home Screen app creation may copy login cookies but **not other local storage**; Safari 26's installation-choice change does not prove migration: [WebKit Safari 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/), [Safari 26](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/).

### 13.7 One evidence chain for a meaningful “backup verified” statement [VALIDATION / OPEN]

| Boundary | Required observation | Explicit false-green to reject |
| --- | --- | --- |
| Source ledger | Pinned exact NORMAL build, origin/container, authenticated Owner and populated disposable 37-store fixture | Native-only tests, empty DB, Acceptance Harness |
| Snapshot | Stable transaction and inventory/digest with source version; concurrent edit before/after bracketed | Snapshot exists ⇒ most recent data included |
| Export admission | Browser- and policy-allowed file route, completed user action | Blob URL, download click, success toast |
| Independent custody | User/administrator-approved destination outside source origin and preferably device-failure domain; file can be selected/read back | Same-origin Cache/OPFS, same-device-only file as disaster recovery |
| Untrusted import | Size/resource/shape/version/UID/digest and semantic checks, negative controls | .lbk extension or digest alone authenticates source |
| Atomic restore | Fresh empty destination, full 37-store transaction/rollback, new Replica ID, preserved source operation/history/tombstones | Partial store counts, successful parser return |
| Independent reopen | Close/restart browser or installed app, inspect semantic records/holds/owner, re-export and compare | Same-page in-memory view or UI success |
| Remote authority | Separately authenticated Manual Sync Receipt, Apply and Cursor checks when implemented | Restored historical receipt/cursor or sign-in ⇒ Sync complete |

**Evidence packet:** exact source/Worker/served-artifact SHA; OS/browser build; Safari tab vs user Home Screen vs MDM Web Clip; origin; MDM profile and managed-domain classification where disclosed; test data inventory; byte size and peak-memory/latency; file provider and failure domain; actions/permissions; before/after raw-store oracles; result including explicit SKIP/BLOCKED/UNKNOWN; accessibility/keyboard/VoiceOver status; sanitized artifacts only. Do not invent or publish real pilot data.

### 13.8 High-information-gain negative controls to add to existing product Work [VALIDATION / DEPENDENCY]

These are grouped scenarios for Engineering-owned W-012/013/014/031, not a new micro-case suite: **(1)** oversized input rejected before unsafe mutation; **(2)** small compressed-looking or deeply nested/many-row JSON rejected under a proven work budget; **(3)** extension/MIME accepted by picker but malformed body rejected; **(4)** valid checksum recomputed on foreign-Owner/changed payload still rejected; **(5)** valid old backup does not override newer tombstone/authority; **(6)** cancelled picker, denied permission or blocked MDM destination leaves ledger untouched; **(7)** browser process kill mid-parse and mid-commit leaves either old or complete new state; **(8)** quota exhaustion produces no partial 37-store restore; **(9)** completed file write but failed independent readback does not show verified backup; **(10)** Safari tab write does not magically appear in new Home Screen/managed container; **(11)** concurrent edit after export proves snapshot-age distinction; **(12)** restored historical Sync metadata does not produce a fabricated destination ACK. Negative controls must assert unchanged destination bytes and correct user-visible/accessible failure states, not merely thrown exceptions.

### 13.9 Five-track transfer and operational judgment [TRANSFER VALIDATION / MINTTAP DECISION PROPOSED]

**E** owns the untrusted-file and MDM authority boundary, confidentiality/durability threat model, restore admission and incident/rollback conditions. **A** supplies File API support, user activation, browser storage/container mechanics and memory-observation hooks. **C** owns exact-device low-memory tests, semantic/transaction oracles, failure injection and accessible negative controls. **B** consumes Design Studio **CD115** (Saved locally / Unknown / Retry / Synced are different states) and **W121** (exact-run/human/AT evidence required), rather than rewriting visual design. **D** consumes Marketing D8's product-claim HOLD; acquisition/analytics may count a backup-action initiation without logging UID, flight data, file name/path, contents or treating that event as verified recovery. Software Engineering Studio M006/D005/D006/Q006 remains canonical for generic runtime/crash/sync/CI mechanics; Web Manager owns the web-medium-specific acceptance contract.

**Proposed gate:** no “backup complete”, “device migration supported”, “EFB offline safe” or “Sync complete” product/release claim from a checksum-valid plaintext .lbk, a green native test or a browser download event. The next discriminating evidence is an Engineering-approved exact NORMAL **37-store Web file round trip** with resource budgets and independent custody/readback, followed by installed Safari and policy-approved managed iPad. Until then **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**. No product or peer repository changes; no new browser execution is claimed.

**Adjacency check:** Additional generic File API primer or synthetic Node cases would not resolve the actual Web adapter, browser memory, iPad Files provider and managed-device permission boundaries. These require implementation/physical-runtime evidence. Keep this integrated source-level checkpoint and move next to the existing product Work gates, not a new standalone test-count program.
