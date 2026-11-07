# PWA Architecture Master — cross-track security, offline and device-custody synthesis

**Snapshot:** 2026-11-07 KST, Web Manager `main@4f5903f411b8c3a353ea4edb552c7bea6c4a2e33`. **Scope:** durable knowledge and bounded LogMate-like EFB application. **Release gate:** Stage 8 ACTIVE / product validation OPEN / PWA release HOLD. **Owners:** A platform facts; E trust/operations; B interaction; C validation; D discoverability/claims. References: [073 PWA foundations](../073-pwa-cross-track-foundations-service-worker-offline-install-storage-update-platform-reality.md), [074 durability/sync](../074-pwa-data-durability-sync-architecture-offline-recovery-transport-boundaries.md), [298 backup](../298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md), [523 remote owner](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md), [528 release/version](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md), [529 deletion](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md), [530 install/MDM](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md).

## 1. Historical problem → standards → operational judgment

**HISTORY:** AppCache coupled application availability to a coarse, failure-prone cache/update manifest. Service Workers enable programmable, secure-origin-controlled fetch interception and explicit install/waiting/activate state, but do **not** make app shell, per-client control, local database and remote authority one atomic system. A PWA can simultaneously contain a V1 tab, V2 waiting worker, retained V1 shell, evolving IDB schema, local unsent edits and intermittent network.

**SOURCE classes:** Service Worker lifecycle/clients/Cache API are Web standards implemented differently by browsers; Web App Manifest addresses presentation and installed identity, not user-data custody; IndexedDB and Cache Storage are distinct origin-managed stores; HTTPS secure context and origin policy provide isolation, not malware-proof script integrity. Browser support for Background Sync/push/badging/File Handling/Web Share, installed container behavior, and MDM control is **version-specific CHANGE WATCH**.

**Five independent states:** (1) installed icon/manifest identity; (2) worker registered/waiting/active; (3) each client actually controlled and assigned a consistent build; (4) shell resources fully verified and cold offline replayable; (5) owner ledger writable, independently backed up and restorable. Only state-specific observations authorize corresponding UI copy.

## 2. Identity and origin matrix

| Identifier | Governs | Does NOT prove |
| --- | --- | --- |
| URL origin (scheme/host/port) | Web security and origin-managed storage bucket | Installed app identity, UID, replica ownership |
| Manifest `id` / `start_url` / `scope` | Install identity/launch/navigation contract | SW controller or data persistence |
| Service Worker registration scope and controller | Controlled client fetch interception | Complete cache, current schema, authenticated account |
| Safari tab / Home Screen web app / managed Web Clip | Browser/OS-specific app/container context | Shared IndexedDB, identical permission or Files access |
| Firebase UID / local Owner / replica ID | Distinct user, local data and replica authorities | Direct peer reachability or automatic Sync |
| Served artifact hash / CacheStorage catalogue | A particular byte representation and lookup | Independent release-signing authority if expected hash is also mutable |

**PRODUCT TRANSFER / OPEN:** Research [530](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) reports a LogMate manifest without explicit `id`/`scope` at its pinned source; URL-resolution implications are **models**, not installed-browser validation. WebKit Home Screen installation/presentation behavior and Managed Web Clip policy cannot be inferred from a Chromium install button. Installation can create a separate storage context; migration between origins/containers must not be assumed. Recheck exact current manifest before any implementation proposal.

## 3. Fetch, caching and offline design

- **App shell/versioned assets:** cache-first can support offline but only with source-pinned resource manifest, digest/integrity, explicit repair/retry, full inventory and safe retirement. A cache entry is an HTTP Response object, including headers; body-only SHA-256 checks do not authenticate cached CSP/MIME headers ([523 ``25–26](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md)).
- **Public informational pages:** network-first plus bounded fallback may be reasonable, but root-scoped worker interception of their CSS/icon/fonts must be tested independently. A working HTML navigation does not guarantee supporting assets; synthetic [523 ``22–24](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) demonstrate a conditional 503 route mechanism, not LogMate NORMAL failure.
- **Authenticated and sensitive responses:** do not treat generic GET caching as an authorization model. Auth Action one-time codes, owner data, private response headers, referrers and telemetry require threat-specific handling; HTTP `no-store` and browser bfcache are separate domains ([527](../527_stage8_pwa_origin_identity_migration_custody_20261029.md), [530 ``15–25](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md)).
- **Durable records/outbox:** IndexedDB/Sembast transaction boundaries, owner fences and local/reconciled operation states are not SW resource caches. Offline shell success is not data persistence or Sync acceptance.
- **Connectivity:** online/offline browser events and network success are hints, not proof that authenticated backends, local peers, quotas or policies permit a specific operation.

## 4. Release/update/rollback invariant sequence

**Track A platform:** worker update script check (`updateViaCache:'none'`, `registration.update()`) → candidate installed/waiting → active worker → controller assigned to a client. **Track E release:** independently verify candidate manifest/asset origin, compatibility with DB capability/schema, old-client continuation, owner/Sync state, storage budget, rollback/recovery. **Track C:** prove each transition on an exact served build with negative controls; **B:** do not say “offline ready” from icon/registration alone; **D:** do not publish unverified features.

**Hazards and research findings:**
1. Worker-global Promise queue does not serialize different SW generations. Shared CacheStorage whole-JSON catalogue can lose cross-generation updates in a **synthetic Chrome** race; IDB `readwrite` get/put inside transaction preserves a modelled pointer, but IDB and Cache Storage are not one atomic commit ([514](../514_stage8_pwa_worker_generation_trace_evidence_data_preserving_recovery_20261024.md), [528](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md)).
2. Download/verification and activation are different. A waiting worker or valid candidate cannot be promoted solely by a download check; an old tab can survive and needs explicit build/schema/owner admission.
3. Mutable cache-catalogue expected hash is not an independent authenticated provenance root. Paired catalogue+body mutation can pass a **research-only negative control**; do not call this observed LogMate compromise ([523](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md), [528](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md)).
4. Version retention and per-client build-map entries can accumulate. Naive old-cache deletion could strand live tabs; measured device cost remains OPEN. Source-derived conditional hash-read cost is not real latency or battery loss.
5. Missing shell, rejected candidate, low quota, process death, network loss and rollback must result in truthful recovered/degraded states, not a misleading universal “updated”/“offline ready” flag.
6. A version-pinned NORMAL build, served HTTPS response, controlled first load, cold offline relaunch, independently reopened 37-store ledger and Files backup each require separate proof.

## 5. Storage, privacy, account deletion and external recovery

Four **non-equivalent claims**: `persisted()` reports browser persistence mode; `estimate()` approximates quota; an IDB transaction completion shows a logical commit to browser-managed state; **independent backup** means a physically separate artifact has been saved, read back and successfully restored in a fresh context. None implies power-loss survival, MDM export permission, app-profile survival or secure Sync.

**Security/owner P0:** [529 `96](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) rechecked an altered source blob and still found 37 backup stores versus 29 explicit deletion drops, with replica and seven Sync stores omitted. `requestAccountDeletion` and active draft-writing guards leave a conditional stale-writer gap. Phase-transition, concurrent deletion drivers and normal A-delete→B startup require executable proof. This is **static risk** and should not be called observed data leakage or incident. Web Manager must not silently rewrite Engineering S007 policy or treat a blanket site wipe as harmless; backup files under user custody are distinct from local owner erasure.

**Untrusted backup and format:** full JSON parsing, canonicalized digests, nested Sync evidence, duplicate key, numeric precision, row budget, provenance and rollback are separate from cryptographic hash equality. [298](../298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md) and [529](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) define exact adversarial tests. Native W-012 positive tests do not prove PWA/Files/MDM.

## 6. iPad/Chromium/standards boundary (CHANGE WATCH)

| Question | Standards/general web | Chromium research | Safari/WebKit and managed EFB |
| --- | --- | --- | --- |
| Install and launch | Manifest and SW optional/related, not equivalent | Synthetic/lab installation behavior, browser-specific | Home Screen presentation and Web Clip MDM policy distinct; permission **OPEN** |
| Offline navigation | Controlled fetch + verified cache + state | Hosted synthetic Worker lifecycle 17/17 PASS | Safari Simulator Acceptance harness PARTIAL; NORMAL installed/physical **OPEN** |
| Local data | IDB transactions, CacheStorage and quota distinct | Synthetic Sembast Web independent tabs 9/9 PASS | Persistent mode/eviction and install containers **OPEN** for actual managed device |
| Background tasks/push | Feature-by-feature APIs, no universal guarantee | Support varies by browser/context | Do not assume unattended execution, push/background sync, file APIs or hotspot permission |
| Transfer to native mobile | No general automatic cross-container database sharing | Research-only protocol/remote ACK models | Managed network, peer discovery, user consent and same-owner authority **OPEN** |
| Data recovery | Export ≠ independent restore | Native component restore PASS at historical SHA | Physical Files egress/reopen/restore/MDM **OPEN** |

**LogMate policy authority:** [MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) specifies **manual** Sync; the server implementation is not certified by this master. A local save, outbox enqueue, remote commit, receipt, ACK, pull, reconcile and independent backup are distinct events. Correct UTC LWW semantics still do not guarantee user-intent chronological order under clock skew ([522](../522_stage8_offline_utc_lww_clock_trust_and_recovery_admission_20261027.md)). Automatic unattended mobile↔EFB transport, background sync, ads and offline persistence are **OPEN** until platform and policy evidence exists.

## 7. Required test/admission order

1. **P0 Engineering:** source-pinned populated 37-store deletion canaries, old-tab write rejection, concurrent saga and A→B normal startup/reopen; compare exact registry/store set and remote receipts. Test failure/rollback, not only happy path.
2. **P0 custody:** export user-allowed synthetic LBK to an actual independent Files location; read back and guarded-restore to fresh clean owner/replica state; validate all relevant stores/Sync metadata.
3. **P1 served NORMAL:** V1↔V2 Worker, old/new controller, corrupt/missing shell, quota/interruption, history/bfcache, report/header policy and cold offline restart on actual served HTTPS.
4. **P1 physical/managed:** independently test Safari tab, installed Home Screen and approved managed Web Clip contexts; record iPadOS version, MDM settings, storage mode, file policy and user-permitted connectivity.
5. **P2 UX/claims/quality:** screen reader/keyboard/reflow, recovery states, performance, accurate external support/deletion and Store claims.

All require attributable timestamp, source/build, browser/OS, fixture data, actual test start and outcome, negative control, independent validation and honest NON-EXECUTION handling. [Evidence register](EVIDENCE_VALIDATION_REGISTER.md) and [open decision queue](RESEARCH_GAPS_AND_SCHEDULE.md) are the operational entrypoints. **No product write or release authorization is created by this synthesis.**
