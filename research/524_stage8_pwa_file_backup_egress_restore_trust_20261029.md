# 524 — Stage 8 PWA file backup, managed-EFB egress and restore trust
Date: 2026-10-29 (KST) | Stage 8 Security / Privacy / Trust | Lead: E, platform dependency: A
Status: **INTEGRATED SOURCE + PRODUCT READ-ONLY AUDIT; RUNTIME VALIDATION OPEN; PWA RELEASE HOLD**

## 1. Question, scope, and curriculum rationale [SYNTHESIS]

The preceding [523 §30](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) established that a Safari tab, installed Home Screen app, and managed Web Clip cannot be treated as one durable storage container. The adjacent operational question is **how a pilot obtains an independently recoverable full-ledger file when browser storage is at risk**, and whether the file actually crosses an airline-managed iPad's OS/MDM boundary. A successful in-memory serializer or share-sheet launch does not establish a durable, accessible, intact, confidential, independently restorable backup.

Historical problem → principle: browser sandboxing deliberately limits arbitrary filesystem access, while managed devices deliberately restrict organizational document movement. The Web platform offers user-mediated file input/download/sharing and some browser-specific file pickers, not an unrestricted portable filesystem. The correct security model separates **local ledger → encoded file → browser handoff → OS-approved destination → independently retained bytes → different destination's verified import → authenticated Owner/replica rules**. Each arrow has a different failure oracle.

This is **web-medium operational custody**, not a replacement for LogMate's Engineering-owned B1 serializer, product Owner policy, Marketing launch claims or Design Studio visual work. No user data, airline device, production endpoint or product repository was modified.

## 2. Authoritative source register, checked 2026-10-29 [SOURCE / CHANGE WATCH]

1. [MDN `<input type="file">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file) (current page checked): user-mediated file selection and File API access are broadly available. `accept` is a chooser hint, **not** validation. `input.value` is not a trustworthy filesystem path; scripts receive selected File objects, not general filesystem read authority. This is an HTML/browser capability, not proof that an airline's Files provider permits an LBK selection.
2. [MDN `showSaveFilePicker()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker) and [`showOpenFilePicker()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showOpenFilePicker): limited-availability File System Access pickers; secure context and transient user activation required for save; abort/security failure branches. Current compatibility does **not** establish Safari/iPadOS support for these picker methods. Distinguish File System Access picker methods from the widely available File API and from origin-private filesystem interfaces.
3. [MDN Web Share API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API), [`navigator.share()`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share), updated **2026-07-16**: a secure-context, transient-activation, OS-target-mediated handoff; `canShare({files})` is capability preflight, not destination persistence. Permission policy, user cancellation, unavailable targets, file type and hostile-share checks can reject. MDN documents platform-dependent Promise resolution (Windows at popup, Android after passing to target); neither establishes byte-for-byte durable Files storage on iPad.
4. [MDN `URL.createObjectURL()`](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static): Blob URLs are document-associated; revoke when safe. This is a possible browser download mechanism, not a file retention or cross-device transfer guarantee. Do not equate URL creation with OS download completion.
5. [Apple Platform Deployment — Manage organizational data](https://support.apple.com/en-ae/guide/deployment/depaa73a4973/web): Managed Open In can restrict managed↔unmanaged document movement, iCloud storage and backup; `allowOpenFromManagedToUnmanaged`, `allowOpenFromUnmanagedToManaged`, managed pasteboard and AirDrop classification are policy controls. These controls exist, but the **classification of a particular Safari/Home Screen/Web Clip, file provider and airline profile remains unknown**.
6. [Apple Device Management Restrictions](https://developer.apple.com/documentation/devicemanagement/restrictions): OS supports managed document-flow restrictions; availability/defaults depend on device/enrollment. A restriction being defined does not prove that it is enabled for LogMate.
7. [WHATWG Storage](https://storage.spec.whatwg.org/) (2026-10-19 version previously reviewed in 523 §30): local browser buckets are not an independently retained backup. A Blob, an object URL or an OPFS file still residing in origin storage does not by itself survive origin deletion.
8. [Engineering Validation Standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md): exact claim/property/target/prestate/independent oracle/environment/observation/verdict/failure/limit required. This study defines tests but does not invent results.

**CHANGE WATCH:** browser support for file pickers, Web Share file types, Safari Home Screen behavior, iPadOS Files providers, MDM Web Clip treatment and airline policy are platform/version/administration-sensitive. Never collapse standards, Chromium, Safari/WebKit and OS/MDM into one capability statement.

## 3. Exact product source and evidence, read-only [SOURCE]

Canonical [LogMate main `9cc0cd432a317d5dfebbe90e318fb219e53e024a`](https://github.com/yhappcom/logmate/commit/9cc0cd432a317d5dfebbe90e318fb219e53e024a), checked 2026-10-29:
- [`MASTER.md`](https://github.com/yhappcom/logmate/blob/main/MASTER.md) and [approved Manual Delta contract §10](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md): structured **whole-ledger `.lbk` Export/Import first** for new-device transfer; no silent replacement/merge of nonempty destination; separate destination replica, verified matching UID, local-first and user-initiated Manual Sync. CSV/PDF/Excel are not full-ledger backup. Cloud full backup, P2P and unattended sync remain unimplemented/unverified.
- [`lib/repository/logbook/whole_ledger_backup.dart`](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/whole_ledger_backup.dart), blob `711f7845`, defines `WholeLedgerBackup` JSON manifest/stores, canonical key ordering, format v1/v2 and a SHA-256 checksum. The source explicitly states it is **an integrity container, not encryption or author authentication**. Do not mistake a self-contained digest for confidentiality, signature or proof that the file came from the rightful Owner.
- [2026-10-24 roadmap §4](https://github.com/yhappcom/logmate/blob/main/docs/roadmap-reconciliation-2026-10-24.md), blob `63ebf702`: **B1 whole-ledger repository foundation IMPLEMENTED**; **FILE backup file UX NOT IMPLEMENTED**; user-facing export/pick/share/restore, device transfer and production recovery unverified. The presence of a serializer is not a completed file pathway.
- [W-012 evidence](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w012-empty-destination-backup-2026-10-27.md), blob `eb0a32f6`: 2026-10-28 **COMPLETE/PASS for authorized Native file-DB empty-destination B1 scope**. The original two failure cases (HOLD key collision and nested foreign Owner) were retained in history and the approved repair was verified at source `63e7c1a`; focused 70 PASS and full 900 PASS/1 SKIP are evidence from that exact source, not this run. It does **not** test browser Files export, MDM, physical EFB or real Firebase Owner login.
- [W-031 iPadOS26.1 Safari Simulator evidence](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w031-simulator-preacceptance-2026-10-27.md), blob `373a03ec`: synthetic Safari **tab** IndexedDB and offline-shell evidence only; **no Home Screen installation, file picker/export, 37-store full ledger, managed iPad or physical Files transfer**. Do not relabel as an LBK test.
- [Product Work checklist](https://github.com/yhappcom/logmate/blob/main/docs/stage3-product-integration-acceptance-checklist.md): W-012 completed in its bounded Native scope; W-013 user-facing file UX, W-014 new-device transfer and W-015 backup policy remain separate work/approval boundaries. No Engineering implementation authority is implied by this research.

**Important correction to overbroad interpretations:** `B1 IMPLEMENTED` means the repository format/restore foundation exists; it does **not** mean the user can press “Backup”, choose an allowed iPad Files destination, retain the file, or restore it later. Similarly, W-012's repaired Owner/HOLD test is positive **Native repository** evidence, not a browser/MDM attestation.

## 4. Platform capability versus actual custody [SYNTHESIS / TRANSFER VALIDATION]

| Mechanism | Web standards / browser meaning | Safari/iPadOS/managed EFB conclusion | Independent acceptance |
| --- | --- | --- | --- |
| `<input type=file>` + File API | User chooses a File; app reads bytes; `accept` is only a hint | General capability is broadly available; **specific .lbk provider/MDM path unverified** | Real selected byte length/hash, correct MIME/extension fallback, cancel/deny, no automatic upload |
| `showOpenFilePicker/showSaveFilePicker` | Limited File System Access picker methods; user activation/secure context | **Do not depend on these APIs for Safari EFB** without fresh exact-version evidence | Feature detection, supported browser alternative and unsupported branch |
| Blob + object URL + anchor download | Creates a browser-associated URL and may request download | iPadOS destination, filename, offline behavior, cancellation and actual Files persistence **unknown** | Independent Files re-open, hash and bytes after browser termination |
| `navigator.canShare({files})` | Tests whether current browser considers payload shareable | File MIME/extension, file size and OS share targets vary; .lbk acceptance **unknown** | Feature probe plus user-visible permitted destination |
| `navigator.share({files})` | User-mediated OS handoff; Promise semantics platform-dependent | **Promise resolution ≠ durable saved backup**, and MDM can restrict egress | Verify actual destination, independent readback and later restore |
| OPFS/IndexedDB/Cache Storage | Origin-local working storage | **Not** an independently exported backup and subject to origin/container custody | Origin deletion vs separately saved file contrasted |
| AirDrop/iCloud/third-party Files | OS/provider transfer destinations | Managed Open In, managed account and airline policy may restrict or forbid | Admin-approved route, explicit user consent and actual destination access |
| Same-UID restored destination | Product identity/replica rule, not a browser feature | No automatic shared IndexedDB/cookie/Replica between Safari/PWA/native | Verified UID, new destination replica, nonempty fail-closed, history/outbox preserved |

A web API feature probe can answer “can I ask the OS to hand off a File?”; it cannot answer “will the airline permit saving this pilot ledger to a personal provider?” or “can the pilot recover it on a different device?”

## 5. Stage 8 trust and threat analysis [SYNTHESIS]

**Confidentiality:** B1's digest is not encryption. A complete LBK can include flight/crew-related records, drafts, history, owner metadata and pending operations. Exporting to a personal cloud, email, shared folder or unmanaged app may expose sensitive user data. Conversely, airline policy may forbid export to unmanaged targets. Neither “always save to iCloud” nor “AirDrop to personal phone” is a safe universal recommendation. Encryption/password/recovery-key design is a separate product/security decision; do not silently invent or promise it.

**Integrity versus authenticity:** SHA-256 can detect accidental byte change against a separately trusted expected digest. An attacker able to alter both content and its unkeyed checksum can recompute it; the file is not signed. The product's matching UID/structure/reference checks and fail-closed restore remain necessary, and are not replaced by the checksum. A local checksum shown by the same untrusted file alone is not an independent source-authority oracle.

**Availability:** “Backup generated” is not “backup exists off-device”; “share sheet opened” is not “destination wrote”; “Files shows a name” is not “bytes survived”; “restore parsed” is not “all 37 stores and Owner/Replica semantics survived close/reopen”. Each must be verified independently. Quota, browser termination, low storage, provider login expiration, offline provider unavailability, MDM revocation, destination denial, canceled dialog and partial writes are separate failure classes.

**Identity and non-destructive restore:** The destination must be an empty/approved replica under the verified same UID, with source cursor/ACK evidence held rather than promoted. Foreign-owner, nested Owner mismatch, wrong version, malformed content, partial files, duplicate IDs, unknown store, nonempty destination and stale schema must reject atomically. No UI copy should suggest importing an LBK merges two active ledgers unless a separate policy is approved.

**Service Worker and update:** The export/import task must work under an offline installed shell without relying on an uncached network API. Worker upgrades, Auth Action routing, CSP, file selection and origin deletion must not erase the source ledger. Blob URL lifetime and download target behavior must be validated after tab/process closure. Worker caching of an exported LBK is not a substitute for OS file custody.

**Privacy/observability:** Never log LBK bytes, filenames containing personal names, UID, exact flight identifiers, local paths, sharing destinations or auth-action codes. Record only coarse error class, platform/MDM capability class and user-approved completion states with retention policy. File picker failure should not trigger automatic upload.

## 6. Operational sequence and truthful UX [MINTTAP DIRECTION — not a new product policy]

1. **Preflight:** explain that the backup contains a complete personal logbook and may be readable without encryption; display available route(s) only after actual capability check. A disabled path is not a promise that the file is protected or saved.
2. **Create:** take a consistent repository snapshot; encode exact format/version, manifest/store registry, UID-bound metadata and checksum; verify bytes against independent source-state oracle. Fail without a success claim on read/encode/storage errors.
3. **Handoff:** require explicit user action; attempt an OS-supported export route; distinguish `USER_CANCELLED`, `UNSUPPORTED`, `POLICY_BLOCKED`, `PROVIDER_UNAVAILABLE`, `TRANSFER_ERROR` and `HANDED_OFF_UNVERIFIED`. Never equate a resolved Web Share Promise to durable storage.
4. **Confirm retention:** independently open the saved file from the chosen allowed destination, verify byte count/hash and parser manifest. If the user cannot re-open it, present **“Backup not verified”**, not “Safe to reset this device”.
5. **Recover:** on a different empty destination, select the file explicitly; authenticate/verify Owner; validate v1/v2 schema and all stores, preserve source operation timestamps/IDs and destination Replica identity; reject atomically when uncertain.
6. **Readback:** close/reopen, compare independent record/revision/outbox/aggregate/owner/replica evidence, then explicitly show **“Restored locally”** while keeping Manual Sync status separate.
7. **Failure recovery:** preserve original ledger and any existing independent backup. Do not clear site data, unregister Worker and delete origin storage, or encourage a device reset merely because a file share failed.

Design Studio W121 is consumed for task-state/visual execution dependencies, not used to claim an approved final layout. Accessibility acceptance includes VoiceOver labels, focus after OS picker return, touch target, interruption recovery and status not conveyed only by color.

## 7. Engineering handoff: independent acceptance matrix [VALIDATION DEFINED — NOT RUN]

The following **BF01–BF18** are new Web Manager acceptance questions, not authorization to implement W-013/014/015. Use disposable synthetic ledgers and administrator-approved test devices; record exact Git SHA/build, browser/iPadOS, installed mode, MDM restrictions, initial UID/replica, independent oracle and negative outcomes.

| ID | Independent oracle / failure model |
| --- | --- |
| BF01 | Exact NORMAL compiled build and version; distinguish Safari tab, user-added Home Screen and managed Web Clip. Capture supported APIs and launch mode; no manifest inference. |
| BF02 | On each context, feature-probe `input[type=file]`, File API, `showOpenFilePicker`, `showSaveFilePicker`, `navigator.canShare({files})`, `navigator.share`, Blob download; record unsupported paths without fallback fiction. |
| BF03 | Produce synthetic full 37-store v2 LBK with independent source snapshot, length/hash, manifest, UID/Replica/Revision/Outbox expectations. |
| BF04 | Offline export from actual installed shell; ensure no Firebase/network dependency and no ledger mutation during serialization. |
| BF05 | Test Blob/download route: filename, MIME, real Files destination, user cancellation, browser termination and independent file reopen/hash. |
| BF06 | Test Web Share with exact LBK MIME/extension/size; distinguish canShare false, NotAllowed, Abort, DataError, resolved handoff, and independently retained file. |
| BF07 | Test large backup and low disk, quota/encoding failure, app kill during creation and destination write; no false “saved” receipt. |
| BF08 | Admin-approved MDM restrictions: managed→unmanaged, unmanaged→managed, iCloud, AirDrop and managed domain; identify which policies apply to **this** Web Clip/Safari context, not merely available OS keys. |
| BF09 | File selection from local Files, permitted managed provider and unavailable/offline provider; verify actual byte content, not just filename/extension. |
| BF10 | Invalid extension, MIME mismatch, truncated/oversized file, duplicate store/row, unknown version, modified manifest and recomputed digest; fail closed without partial destination mutation. |
| BF11 | Foreign UID and nested foreign Owner/binding; actual authenticated same-UID comparator; never infer identity from filename or digest. |
| BF12 | Empty destination v1 and v2 restore: independent 37-store snapshot, source metadata, destination Replica, no inherited ACK/cursor authority; close/reopen. |
| BF13 | Nonempty destination import: reject/review without overwrite or merge; compare pre/post all-store hash. |
| BF14 | Inject process kill/transaction failure during restore and retry; atomic rollback, no staging/HOLD corruption or cursor promotion. |
| BF15 | Export in Safari tab then attempt restore in isolated installed Home Screen/managed Web Clip; no assumed shared IDB or login state. |
| BF16 | Delete disposable origin storage **after independently verifying** an allowed exported file; restore on fresh container; separate shell reinstallation from ledger recovery. |
| BF17 | VoiceOver/keyboard/touch/focus/status on export, cancel, provider denial, wrong UID, restore review and offline recovery; test actual device, not screenshot-only. |
| BF18 | Release review: precise privacy copy, support instructions, retention/telemetry, device-management approval, rollback, user training and no “automatic sync/never loses data” claims. |

**Independent oracle:** a fresh parser and manifest/store count plus pre/post canonical record/revision/outbox/baseline/Owner/Replica readback; avoid an oracle that simply trusts the exporter or reports `share()` resolution. Use hash comparison to detect transfer corruption, and semantic checks to detect internally consistent but wrong/foreign data. No actual BF test executed in this cycle.

## 8. Five-track allocation and external specialist boundary [DEPENDENCY / TRANSFER VALIDATION]

| Track | Stage/gate and maturity | This bundle's responsibility |
| --- | --- | --- |
| **E — Web Architecture, Security & Operations** | Stage 8 major bottleneck; SOURCE+SYNTHESIS, physical/MDM proof missing; highest release and data-loss risk | **Own** file egress, confidentiality, policy boundary, durable backup receipts, non-destructive recovery and release HOLD. Majority allocation. |
| **A — Web Platform & Browser** | Strong storage/Worker standards foundation; Safari picker/file/OS behavior needs exact-version execution | Supply File API versus File System Access, Blob URL, Web Share and Safari-vs-Chromium support distinctions; maintain CHANGE WATCH. |
| **B — Web UX/IA** | Task-state architecture mature in theory; Design Studio W121 runtime gate OPEN | Consume E's failure taxonomy for install/backup/restore status, clear consent, accessibility wording and nonempty-destination review; no new visual system. |
| **C — Quality/Accessibility** | Native B1 tests and Safari tab harness bounded; physical installed/MDM/Files oracles missing | Own independent BF01–BF17 runtime, 37-store checks, interruption, VoiceOver and actual device evidence. |
| **D — Discovery/Analytics** | Marketing D8/D9 product claim HOLD; no field install/backup success data | Do not claim automatic backups, universal EFB availability or zero data loss. Measure only privacy-safe aggregate route completion after product/consent validation. |

**Engineering** owns W-013/014/015, exact product implementation and device tests; [Validation Standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) governs evidence. **Marketing** [D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) retains launch-claim authority. **Design Studio** [W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) retains visual/interaction specialist gates. No peer repository write.

## 9. Contradictions, decision and next boundary [CONTRADICTION / OPEN]

- `SHA-256 backup integrity` **does not imply** confidentiality, author signature or an independently verified origin; LogMate source explicitly says so.
- `B1 Native 70 focused PASS` **does not imply** iPad file export/import, managed destination permission or real Owner Auth PASS.
- `Safari tab IndexedDB offline PASS` **does not imply** Home Screen Files/MDM/backup PASS.
- `navigator.share() resolved` **does not imply** destination wrote durable bytes; no file readback means **UNVERIFIED**.
- `File System Access pickers work in Chromium` **does not imply** Safari EFB support.
- `Managed Open In exists` **does not imply** the airline enabled it or a Web Clip is classified as a managed app.
- `same URL/same email` **does not imply** same storage container, authenticated UID or replica.
- `origin-private file exists` **does not imply** backup survives origin storage deletion.

**MINTTAP DIRECTION:** treat exported full-ledger custody as a separate release gate, require an allowed **independent file readback and restore** before describing backup as completed, and keep the approved local-first/manual-sync/empty-destination policy unchanged. A file UX proposal is not an implementation authorization.

**Stage 8 ACTIVE · Source/product read-only audit complete for this question · BF01–BF18 NOT RUN · Production validation OPEN · PWA release HOLD.**

**Adjacent-value checkpoint:** This bundle covers browser file authority, Safari picker limitation, Blob/download lifetime, Web Share semantics, Apple managed document flow, exact B1 source, Native W-012 positive/negative evidence, Safari W-031 limits, confidentiality/integrity/authenticity, OS custody and 18 independent recovery oracles. The next genuinely different evidence boundary is Engineering-approved **actual installed/managed physical iPad + exact file-flow runtime**. Do not substitute another Chrome synthetic fixture for that boundary.