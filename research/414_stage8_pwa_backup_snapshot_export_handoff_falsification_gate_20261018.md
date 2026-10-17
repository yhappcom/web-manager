# 414 — Stage 8 PWA Backup Snapshot, Export Handoff and Restore-Finality Gate

**Checkpoint:** 2026-10-18 Asia/Seoul. **Canonical Web Manager base:** `main@9a765ba5056b5609899aa0e479cd22218d143d0c`. **Read-only LogMate source:** `main@0233d4f9ea0ff43820e3ed6297a837e3e07e0634`. **Owner:** E (data custody/recovery); A supplies browser transaction/file mechanics, C negative/runtime validation, B truthful task-state UX, D privacy-safe claim/measurement transfer. **Gate:** SOURCE + SYNTHESIS + source-specific contradiction + synthetic model **12/12 PASS**; **NO** actual LogMate backup implementation, .lbk, Safari/iPad, browser IndexedDB, native, Firebase or production PASS. **Stage 8 focused maintenance; PWA release HOLD.**

## 1. HISTORY / PROBLEM → PRINCIPLE

Offline-first makes the device's local ledger the only copy of some untransmitted user records. Service Worker/Cache Storage and the web app's IndexedDB persistence improve offline operation but are not independent recoverable copies. A "backup" has at least **four non-equivalent events**: (a) one logically consistent source-DB cut, (b) deterministic archive encoding and integrity validation, (c) browser/OS file handoff, and (d) independent re-open/restore proof. Export UI must not promote (c) into (d), nor confuse a locally created archive with server-confirmed Sync.

Study 413 proved the generic torn-read counterexample. This study resolves an adjacent implementation boundary: **which current LogMate repository reads can actually establish one backup cut, and which browser APIs can prove that a user-visible file was durably retained?**

## 2. SOURCE — PRIMARY PLATFORM AND PINNED PRODUCT (consulted 2026-10-18)

- W3C IndexedDB 3.0: https://www.w3.org/TR/IndexedDB/ — a live read-only transaction returns a stable view within its scoped object stores; scope and transaction lifetime matter. `durability` is a hint for commits, not a guarantee of device-independent backup.
- MDN IndexedDB transaction lifetime: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB and https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction — transactions become inactive between event-loop tasks and auto-commit when outstanding requests end. Do not assume an arbitrary asynchronous file-encoding `await` can occur inside an active transaction.
- MDN File System Access: https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker — limited availability, secure context and transient user activation; **not** a universal iPad Safari file-save API.
- MDN Web Share: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share — file sharing depends on `canShare`, permissions policy, activation, and target support. Resolution does **not** prove that the target saved and later re-opened the file.
- MDN anchor `download`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a — same-origin/blob/data download hint; actual handling depends on browser, settings and user action.
- WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/ — quota/eviction and standalone web app treatment; available storage is not an external backup guarantee.
- LogMate approved Sync contract: https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md — approved 2026-10-17: local-first, user-invoked Manual Delta, UTC record-level LWW, immutable Op ID, contiguous applied Cursor, full `.lbk` file transfer preferred for device replacement; implementation explicitly **NOT IMPLEMENTED**.
- LogMate `lib/repository/logbook/sembast_database_opener_web.dart` at blob `87f043d5`: `databaseFactoryWeb.openDatabase('logmate_ledger')`.
- LogMate `lib/repository/logbook/sembast_logbook_repository.dart` at blob `0ed503ce`: `readRevisions(ref)` and `readPendingOperations()` use separate `_revisionStore.find(_database)` and `_outboxStore.find(_database)` calls, **not one enclosing repository transaction**. `readPendingCustomFieldDefinitionOperations()`, `readPendingCustomFieldValueOperations()` and `readLocalReplicaIdentity()` each use their **own** `_database.transaction(...)`. The repository has many transactional local mutations, but independently calling these public readers does not itself establish a single multi-store backup snapshot.
- LogMate `lib/repository/logbook/local_database_capability_codec.dart` at blob `e9487c37`: current capability `16`. `test/repository/logbook/sembast_web_reopen_test_browser.dart` tests IndexedDB-backed create/delete/restore/reopen; it is **not** an all-store .lbk export/restore test.
- Design Studio W121: https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md — exact runtime and failure injection, not more pre-runtime visual manifests.
- Software Engineering D006: https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md — retry/idempotency and conflict-model distinction; do not rewrite the approved product LWW policy.
- Prior Web Manager 413: https://github.com/yhappcom/web-manager/blob/main/research/413_stage8_pwa_approved_manual_sync_backup_cut_cursor_lineage_gate_20261018.md .

## 3. CONTRADICTION / SYNTHESIS — CURRENT READER COMPOSITION IS NOT A BACKUP CUT

**Confirmed source-level gap, not a production defect:** current repository APIs offer multiple independent read transactions. A hypothetical `.lbk` exporter that calls `readRevisions()`, `readPendingOperations()`, custom-field readers, baseline, page structure and cursor in sequence can observe an accepted local mutation between reads. Individual atomic **writes** do not make a series of independent **reads** a snapshot.

**Implementation requirement (Engineering handoff, not an approved implementation):** create an explicit `readConsistentBackupSnapshot` boundary at the Sembast repository layer, covering every authoritative store needed by the approved Sync contract, including owner identity, capability/schema, record lifecycle/current values, revision and deleted history, every pending/applied Op family, custom definitions/values, user-confirmed structure/page/baseline/config, replica identity, cursor/epoch proof and relevant generation/checkpoint lineage. Decide explicitly whether drafts/setup state belong to the archive. Fail closed on missing or incompatible objects; do not silently omit new stores added by schema upgrades.

**Transaction qualification:** W3C read-only snapshot guarantees apply to one underlying IndexedDB transaction's scoped stores. They do not prove that Sembast Web's Dart transaction wrapper, all its backing object stores, or a large cross-store read maps to exactly that primitive. Engineering must inspect `sembast_web` implementation/version and demonstrate concurrent-writer snapshot behavior in Chromium **and** WebKit. Never serialize huge ZIP data or wait for OS file UI while holding an IndexedDB transaction open. Read/copy a bounded consistent snapshot first, release transaction, then encode/handoff outside it. For large ledgers, design a verified chunked snapshot/epoch or bounded writer fence; **generation-before/after alone is not proof** unless every relevant mutation advances the same generation and a stable cut is enforced.

## 4. PROPOSED SAFE PIPELINE — SIX DISTINCT BOUNDARIES

| Boundary | Evidence / invariant | Failure policy |
| --- | --- | --- |
| P0 local owner and source | unlocked bound owner, supported capability v16, complete store inventory, pending Op families; source DB remains untouched | unsupported/locked/unknown => no export success |
| P1 snapshot | one logically consistent ledger/history/outbox/cursor/structure/owner cut; independently checked record↔Op references and source generation | torn/unknown => abort; never delete or confirm pending Op |
| P2 archive | versioned canonical serialization; bounded memory/size; manifest of counts/schema/owner/lineage and digest over exact bytes | corrupt/truncated/unknown => invalid; digest is integrity, **not** authentication |
| P3 file handoff | feature-detect platform; Chromium desktop picker if supported; iPad Safari share sheet or Blob/download only if **actually tested**; explicit user action | cancel/unsupported/target failure => keep source, report handoff failed/unknown |
| P4 independently verified copy | user chooses saved file; separate reader parses, validates manifest, hash, schema, owner and required stores; optionally disposable restore/reopen | no re-open proof => `HANDOFF_UNVERIFIED`, never claim durable backup |
| P5 restore and reconciliation | owner authenticated; empty/dirty target distinction; new Replica ID, original Op IDs, cursor proof and schema compatibility; staged atomic publish after verification | dirty target => REVIEW_REQUIRED, no destructive replace; unproven cursor => no Sync success |

**UX transfer:** `LOCAL_SAVED`, `BACKUP_PREPARED`, `FILE_HANDOFF_STARTED`, `FILE_HANDOFF_UNVERIFIED`, `BACKUP_VERIFIED`, `RESTORE_STAGED`, `REMOTE_ACK_UNKNOWN`, `REMOTE_APPLIED` are distinct. A Web Share promise, browser download prompt, file-picker write resolution, or visible filename is not independently verified recovery. Use accessible status text and recovery actions; Design Studio owns visual treatment.

**Security/privacy transfer:** a .lbk contains private flight history and possibly owner metadata; a SHA-256 digest only detects changes relative to the recorded digest and does not authenticate an untrusted file. Require strict parser limits (file size, archive entries, decompression ratio, depth, supported codecs), no dynamic code/HTML execution, UID authorization independent of file contents, no flight payload or UID in telemetry, and a separate decision for user-facing encryption/key recovery. Never assume MDM permits Files/share/export or that a company iPad can install arbitrary native software.

## 5. PLATFORM-SPECIFIC CHANGE WATCH / DECISION MATRIX

| Context | Known platform principle | OPEN exact-device evidence |
| --- | --- | --- |
| Desktop Chromium HTTPS | `showSaveFilePicker` may be available with user activation; File System Access API not baseline | exact permission, write/close, user re-open, large-file/memory and crash |
| Android Chromium PWA | Do not extrapolate desktop picker; Web Share/download are separately gated | export destination and independent restore on target device |
| iPadOS Safari tab | IndexedDB and browser file/share primitives have lifecycle and user-gesture constraints | save destination, file type handling, app switching, background suspension, Files access |
| iPadOS Home Screen app | standalone context can have distinct website data from Safari; quota/eviction remain risks | same-owner data separation, file handoff, re-open, cold-start, app update |
| Managed iPad Web Clip | OS/MDM enrollment and policy envelope are separate from web standards | actual restrictions, Files/share availability, Web Clip storage identity, device wipe/redeploy |
| Native mobile | Sembast native backend is not necessarily the same storage adapter as Web | portable .lbk schema, owner/replica transition, crash/rollback |

**CHANGE WATCH:** Safari/iPadOS 26 install UX and file capabilities; WebKit storage/eviction; `sembast_web` exact version and IndexedDB transaction mapping; browser file/share activation semantics; future Sync schema/operation families. No general web API support claim is a managed-fleet deployment certification.

## 6. VALIDATION — EXECUTED INDEPENDENT SYNTHETIC MODEL, NOT PRODUCT

**2026-10-18:** Python stdlib `unittest` model: **12/12 tests PASS**. Enumerated six orderings of ledger/outbox/cursor reads × four commit placements: **8/24** produce a torn ledger↔Outbox combination if reads are independent; both coherent before/after snapshots pass. Negative checks: hash tampering, truncated archive, wrong owner, unsupported schema, dirty-target refusal, preserved original Operation ID, new Replica ID and cursor lineage unverified, export handoff != verified backup, restore staged != remote applied. Fixture owner/records are synthetic. This is a small falsification model, **not** an empirical failure rate, Sembast integration test, real .lbk file or browser test.

**C-owned executable G0–G6 packet:**
- **G0 exact source:** pin LogMate main SHA, Flutter/Dart, Sembast/sembast_web, capability v16, approved Sync contract and generated PWA artifact.
- **G1 atomic read:** inject a real concurrent local Flight edit and Custom Definition mutation at every store-read boundary; verify full source snapshot and that no accepted operation disappears.
- **G2 large snapshot:** memory pressure, quota, transaction inactivity, app suspension/kill, schema migration and partial writes; no silent export completion.
- **G3 iPad handoff:** physical Safari tab/Home Screen/managed Web Clip independently: user gesture, share/download, destination, file re-open, digest and restore; no silent success.
- **G4 restore:** wrong UID, tampered/truncated/zip-bomb, dirty target, unknown schema, interrupted import; original local DB remains intact.
- **G5 replica/Sync:** restored new Replica ID, original pending Op IDs, receipt replay, contiguous cursor proof and authenticated Firebase Emulator; no cursor-only advancement.
- **G6 UX/privacy:** screen reader/keyboard/zoom and truthful states; telemetry contains no flight content, UID or backup bytes; marketing/offline/recovery claims bounded by executed evidence.

## 7. FIVE-TRACK ALLOCATION / TRANSFER

- **E (primary):** owns snapshot/restore custody, integrity vs owner authority, file finality, destructive recovery fencing, deployment/data-loss decision.
- **A (critical prerequisite):** owns IndexedDB transaction lifetime, Sembast Web adapter verification, user-gesture/file/share/browser/OS support and origin storage distinctions.
- **C (high execution debt):** owns G0–G6 independent negative oracles and physical Safari/iPad, accessibility and failure injection; source/model success is not product success.
- **B (targeted transfer):** owns truthful backup and recovery task-state architecture; Design Studio W121 owns executable interaction/accessibility proof.
- **D (targeted transfer):** owns privacy-minimized measurement and search/install claim provenance; Marketing owns acquisition strategy, not Sync truth.

## 8. MINTTAP DECISION / OPEN / NEXT GATE

**MINTTAP DECISION (unchanged approved product):** local-first + user Manual Delta + UTC LWW + .lbk device transfer remain authoritative. **Engineering recommendation, NOT implementation approval:** do not build backup from independent public getter calls; introduce an explicitly tested source-DB consistent cut and independently verified archive/restore path. Keep source data and all pending Operations until separate verified/acknowledged evidence permits lifecycle changes.

**OPEN:** all-store snapshot API and actual `.lbk` format/writer/reader, archive encryption/recovery keys, cross-platform file UI, managed iPad restrictions, real browser transaction behavior, actual Sync implementation, Firebase receipt/cursor runtime, exact normal PWA artifact and deployed headers, product/physical-iPad/AT validation.

**Adjacent-work stop check:** source-specific independent-read gap, standards, file-finality boundary, cross-platform capability, restore authorization, security, UX/measurement and falsifiable test packet are integrated. More synthetic examples cannot promote the product gate. Next context boundary is Engineering-owned real Sembast snapshot/export + disposable HTTPS and physical iPad. **Stage 8 remains focused / Production validation OPEN / PWA release HOLD.**
