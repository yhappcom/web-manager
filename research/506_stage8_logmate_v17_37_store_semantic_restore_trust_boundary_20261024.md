# 506 — Stage 8 LogMate v17 37-store semantic restore and trust-boundary acceptance

Date: 2026-10-24 (Asia/Seoul)  
Status: **SOURCE-BOUNDED INTEGRATED CONTRACT / ENGINEERING HANDOFF; NO PRODUCT BROWSER PASS**  
Owner: **Track E** (restore/release authority); dependencies: A browser/storage, C runtime/semantic oracle, B recovery UX, D evidence/privacy.  
Canonical Web Manager starting head: f3f34e5cd6d632065513c890d3b362d7b3cd0bf1. Product read-only source: LogMate main@5ad78167cb97d6846ed7b5f866151d2a080dcc88. Historical v16: 59cd171176c58b598a4db55d128ffd21d406e862.

## 1. Decision question and evidence ladder [SOURCE / SYNTHESIS]

Can a browser restore be accepted because the LBK v2 manifest enumerates 37 stores, or because 37 store maps match? **No.** The source implementation deliberately changes device/owner/Sync authority on restore, so literal all-store equality is the wrong oracle for a populated source with Sync progress. The correct acceptance target is **semantic preservation of local user work plus non-transfer of remote authority**, followed by real browser/process/device survival evidence.

- **SOURCE (exact LogMate source):** lib/repository/logbook/sembast_logbook_repository.dart lines 227–271 register 30 legacy stores plus 7 Sync stores; 35 string-key and 2 integer-key stores. Lines 422–480 export v2; 486–591 restore and reset trust; 5798–5868 validate manifest/key types/counts/digest; 5870–5924 require an empty staging destination and validate selected restored references.
- **SOURCE (host tests):** test/repository/logbook/whole_ledger_backup_test.dart lines 379–1020 exercise populated Flight/Simulator/Custom/Baseline/Page/Draft/local save receipt and disk reopen; lines 1004–1020 exclude replica and Sync State from source/destination parity. test/repository/logbook/sync_replica_identity_safety_test.dart lines 95–144 explicitly inject source cursor/applied identity, then assert they are removed from destination active authority and copied into holds.
- **SOURCE (browser proposal):** Web Manager research/handoffs/whole_ledger_backup_browser_test_PROPOSAL.dart is a one-flight, 37-store *registry* test with database close/reopen; it is neither a populated 37-store semantic fixture nor a browser-process restart.
- **TRANSFER VALIDATION:** Design Studio research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md forbids promoting another pre-runtime manifest over exact served/runtime evidence. Software Engineering D006_logmate_inbound_cursor_atomicity_transfer.md distinguishes durable cursor progress from actual applied semantic state. Marketing 438 holds first-release PWA ads; neither specialist certifies restored Sync authority.
- **VALIDATION (this study):** Exact GitHub file content and store registry were programmatically enumerated and checked for 30+7 entries, unique names and 35 String/2 int key types. No Dart/Flutter/Chrome/Safari/managed-iPad execution was performed. Current LogMate main CI workflow-run query returned no run at the v17 head; prior main Core run 39881725421 belongs to v16 head and failed.

## 2. Exact v17 store-level semantic acceptance matrix [SOURCE / MINTTAP DECISION]

Each row below is a **required test oracle / source-informed proposed acceptance rule**, not a statement that a populated browser test has passed. “Preserve” means equality of typed semantic content after legitimate normalization; it does not mean that every store must be nonempty in every fixture.

| # | Store | Key | Family | Proposed semantic oracle / special transform |
|---:|---|---|---|---|
| 01 | logmate_schema_v1 | String | Capability | v17 logical marker; exact decoded ready state; never confuse with native IDB version |
| 02 | logmate_active_records_v1 | String | Canonical ledger | Preserve active Flight/Simulator identities and values; compare decoded records |
| 03 | logmate_deleted_records_v1 | String | Canonical ledger | Preserve tombstones and deleted record identity; reject resurrection |
| 04 | logmate_revisions_v1 | String | Canonical ledger | Preserve revision chain/base IDs and accepted UTC |
| 05 | logmate_outbox_v1 | String | Canonical ledger | Preserve pending operation IDs and order; never infer remote ACK |
| 06 | logmate_ledger_meta_v1 | String | Structure | Preserve structure generation and metadata |
| 07 | logmate_day_orders_v1 | String | Structure | Preserve user-confirmed ordering and referential integrity |
| 08 | logmate_deleted_slot_policies_v1 | String | Structure | Preserve deleted-slot policy and target references |
| 09 | logmate_page_policy_v1 | String | Structure | Preserve page policy/manual boundaries |
| 10 | logmate_page_projections_v1 | int | Structure | Preserve typed int keys and page projections |
| 11 | logmate_migration_issues_v1 | String | Structure | Preserve recorded migration diagnostics; do not treat as release clearance |
| 12 | logmate_owner_access_v1 | String | Identity/recovery | TRANSFORM: matching owner rebound LOCKED; source unlocked state must not transfer |
| 13 | logmate_local_entry_v1 | String | Identity/recovery | Preserve local-entry history only subject to product re-entry semantics; no automatic unlock |
| 14 | logmate_initial_setup_v1 | String | Identity/recovery | Preserve setup record; do not infer destination device enrollment |
| 15 | logmate_baseline_v1 | String | Totals | Preserve previous totals/baseline semantic quantities |
| 16 | logmate_ledger_data_generation_v1 | String | Totals | Preserve ledger data generation |
| 17 | logmate_baseline_configuration_generation_v1 | String | Totals | Preserve baseline configuration generation |
| 18 | logmate_aggregate_meta_v1 | String | Totals | Preserve aggregate manifest; validate source generations |
| 19 | logmate_aggregate_checkpoints_v1 | int | Totals | Preserve typed int keys and totals/checkpoint lineage |
| 20 | logmate_account_deletion_v1 | String | Identity/recovery | Preserve deletion state; never override deletion lock |
| 21 | logmate_logbook_configuration_v1 | String | Totals | Preserve configuration revision and settings |
| 22 | logmate_custom_definitions_v1 | String | Custom fields | Preserve definitions, types and stable IDs |
| 23 | logmate_custom_definition_revisions_v1 | String | Custom fields | Preserve definition revision chain |
| 24 | logmate_custom_definition_outbox_v1 | String | Custom fields | Preserve pending definition operations |
| 25 | logmate_custom_values_v1 | String | Custom fields | Preserve typed values and record/definition references |
| 26 | logmate_custom_value_revisions_v1 | String | Custom fields | Preserve value revision chain |
| 27 | logmate_custom_value_outbox_v1 | String | Custom fields | Preserve pending value operations |
| 28 | logmate_flight_entry_drafts_v1 | String | Draft/save | Preserve unfinished draft and custom values; old actorDeviceId provenance requires review |
| 29 | logmate_local_replica_v1 | String | Identity/recovery | TRANSFORM: preserve fresh destination replica ID, not source replica |
| 30 | logmate_flight_entry_save_receipts_v1 | String | Draft/save | Preserve local save receipt and idempotent finalize behavior; not remote Sync receipt |
| 31 | logmate_sync_state_v1 | String | Sync trust | TRANSFORM: destination replica, unbound stream, unverified baseline; retain prior source state as evidence |
| 32 | logmate_sync_operation_bindings_v1 | String | Sync trust | Copy frozen bindings; their presence is not remote acceptance |
| 33 | logmate_sync_receipts_v1 | String | Sync trust | Copied by current v2 restore; NOT proof of destination authenticated remote ACK |
| 34 | logmate_sync_applied_identities_v1 | String | Sync trust | TRANSFORM: remove live applied identities; preserve source rows in recovery holds |
| 35 | logmate_sync_applied_cursor_v1 | String | Sync trust | TRANSFORM: remove live cursor; preserve source rows in recovery holds |
| 36 | logmate_sync_record_heads_v1 | String | Sync trust | Copied by current v2 restore; NOT destination server-stream authority |
| 37 | logmate_sync_holds_v1 | String | Sync trust | AUGMENT: retain source holds and add restored:cursor/applied source-evidence holds |

**Inventory assertion:** 37 unique registry names = 30 base + 7 Sync, with exactly 35 String and 2 int key types. The two int stores are page projections and aggregate checkpoints. Count/type/registry validation is necessary but insufficient to prove valid domain relationships.

## 3. Restore transform as a falsifiable oracle [SOURCE / SYNTHESIS / MINTTAP DECISION]

For a v17/v2 source backup S and newly initialized destination D, with matching verified owner and a nonempty **source** cursor/applied-identity fixture:

1. Validate exact format v2, capability 17, owner, 37 ordered registry entries, typed keys, duplicate-key exclusion and snapshot SHA-256; the digest is **integrity only**, not signer authentication. Source export requires READY, matching unlocked owner, and no pending deletion lock.
2. Demand a fresh staging destination, not an existing populated ledger; capture D's newly generated replica before restore. The restore is one Sembast transaction with a test-only fault seam before commit.
3. For canonical record/history/structure/custom/baseline/draft/local receipt and other ordinary copied stores, compare typed keys, semantic values and domain relationships after restore. Do not count a serialized empty store as a populated semantic test.
4. Replace source replica with D's replica and set owner to matching UID but **locked**. Source draft actorDeviceId and local save-receipt provenance remain source-derived; their exact future device/authorization interpretation is an Engineering review item, not permission to rewrite history.
5. Reset destination Sync State: originReplicaId=D, streamBindingStatus=unbound, remoteBaselineStatus=unverified, and restoredSourceState holds source Sync State when present. Neither source stream state nor an LBK digest authenticates a current server stream.
6. Move every source applied-cursor/applied-identity row out of *live* destination stores into distinct restored:<store>:<key> recovery holds, then leave those live stores empty. Preserve original hold rows. No invented remote Receipt, no cursor advancement and no silent promotion of source applied history.
7. **Critical non-equality exception:** Source Sync receipts, record heads and operation bindings are currently copied, not dropped, in the v2 path. This is not proof they are currently consumed as remote authority by a product Sync implementation. The future consumer must explicitly establish whether copied records are historical evidence, require a hold, or may participate only after authenticated stream re-binding. A whole-store equality test that ignores this distinction is incomplete; declaring a current production bug from copied rows alone is unjustified.
8. Reopen and inspect before owner unlock; then deliberately unlock with matching UID and validate decoded record/page/custom/draft/local-save behavior. Verify post-reopen and after an independently confirmed **browser process exit and relaunch using the same profile**; an IndexedDB connection close is not a process restart.
9. For a genuine historical v16/v1 backup, use the 30-store registry and the explicit v17 migration path: all seven Sync stores are dropped/initialized, schema becomes capability 17, owner stays locked and destination replica is new. Do not claim the v1 backup had v2 source Sync receipts.
10. Preserve failure atomicity: digest-valid malformed structure, wrong owner, unknown version, duplicate keys, nonempty destination, interrupted store writes and invalid references must leave the destination's original replica/owner/data untouched. A test-only fault callback is not a production recovery guarantee.

**CONTRADICTION 1:** “37/37 maps equal” would reject legitimate source-cursor/applied-identity removal and recovery-hold augmentation. **CONTRADICTION 2:** “37/37 registry present” can pass with no simulator, custom values, drafts, remote progress or process restart. **CONTRADICTION 3:** “source Receipt copied” is not “destination remote ACK authenticated.” **CONTRADICTION 4:** “Sembast reopen passed” is not “physical iPad retains unsynced records after OS eviction.”

## 4. Browser evidence campaign: prioritized, non-duplicative [DEPENDENCY / VALIDATION / OPEN]

**P0 — actual LogMate browser, Engineering-owned:** Build exact v17 NORMAL and a testable non-production variant with separately recorded hashes; execute a Chrome IndexedDB *populated* B1 fixture adapted from the host fixture (Flight, Simulator, delete/restore/revision/outbox, Custom definition/value/revision, manual page and aggregate baseline, unfinished draft and idempotent local save receipt). Record source/destination per-store typed row counts and independent decoded semantic assertions; require at least one populated representative per family, not necessarily every infrastructure store. Test wrong owner, tampered digest, duplicate key, preexisting destination, injected transaction rollback and clean retry. Run with a dedicated persisted browser profile, close the process, reopen and compare semantic state without re-seeding.

**P0 — separate Sync trust case:** In a *synthetic authorized fixture*, seed source v2 with a nonempty applied cursor and identity, an operation binding, a source receipt, a record head and a hold; verify source evidence is preserved where specified while destination active cursor/identities are empty, state unbound/unverified, owner locked and replica distinct. Engineering must determine the allowed consumer behavior of copied receipts/heads/bindings before any Sync/ACK UI can claim authenticated completion. No real remote ACK is implied.

**P0 — historical import:** Import the actual pinned v16 populated Format v1 fixture through v17 Chrome, verify 30→37 transition and exact source semantics, then independently reopen. A hand-rewritten v2 fixture is not historical compatibility proof.

**P1 — platform lifecycle:** Execute same-origin old/new real Flutter bundles and Worker control changes separately from B1 restore; distinguish old tab, old Worker, current Worker, logical capability and native IDB version. Repeat Safari tab and installed Home Screen as separate storage contexts; do not infer managed Web Clip equivalence.

**P1 — physical iPad/EFB envelope:** Record device/iPadOS, Safari vs installed vs managed Web Clip, supervision/MDM policy, offline duration, low-storage condition, storage.persisted() result, manual export/reimport, application and device restart, and any profile removal. Capture local record availability and unique unsynced-data recovery; no guarantee of direct unattended device-to-device sync or background execution.

**P2 — remote authority:** Only after actual server implementation and independent authenticated Receipt/cursor evidence exist, test destination manual push/pull, retry after lost ACK, UID isolation, server stream rebinding and conflict/hold disposition. This remains Software Engineering-owned implementation validation.

## 5. Platform standards and operational judgment [SOURCE / CHANGE WATCH]

- IndexedDB uses transactions; transaction complete, browser-process survival, device storage durability and independent export/backup are distinct. Browser shutdown can abort unfinished transactions. MDN: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB and https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability (checked 2026-10-24).
- WebKit describes origin-based storage eviction under pressure, best-effort default and heuristic persistence grants; quota figures are ceilings, not durability promises. WebKit: https://webkit.org/blog/14403/updates-to-storage-policy/ (rechecked 2026-10-24).
- Service Worker lifecycle/control does not migrate Sembast data or replace already executing page JavaScript. W3C: https://w3c.github.io/ServiceWorker/ (checked 2026-10-24). iPadOS installation and MDM-specific policy are CHANGE WATCH, not Chrome-transfer facts.
- Evidence handling: synthetic IDs, sanitized counts/digests, no real flight payloads, tokens, UID, cookies or personal backups in CI logs. A valid digest over an incomplete inventory or a test-controlled recorder is not independent proof.

## 6. Five-track integration and release gate [TRANSFER / MINTTAP DECISION]

**E (owner):** No-destructive-repair, backup trust boundary, owner lock, source-vs-destination Sync authority, deployment custody and release HOLD. **A (dependency):** origin/profile, IndexedDB vs Sembast logical version, Worker generation and Safari storage partition. **C (execution owner):** typed 37-store oracle, semantic population, negative controls, independent process restart, exact build provenance and no false PASS. **B (consumer):** truthful “local saved / export verified / restored locked / Sync unverified / remote acknowledged” states; Design Studio owns human/AT rendering validation. **D (consumer):** privacy-minimized event taxonomy and no claims of seamless PWA update, durable offline backup or cross-device Sync without actual evidence.

**Gate verdict (2026-10-24):** Registry/static restore contract **SOURCE VERIFIED**; host/native tests **SOURCE-OBSERVED, not re-executed this run**; current-head v17 Chrome populated restore **NOT_EXECUTED**; actual browser-process restart **NOT_EXECUTED**; v16/v17 real two-binary overlap **NOT_EXECUTED**; Safari/Home Screen/managed iPad **OPEN**; authenticated remote Sync **OPEN**. **Stage 8 remains active, Track E bottleneck, Production validation OPEN, PWA release HOLD.**

**Adjacent question resolved:** A rich source Sync fixture does **not** admit a naive all-store-equality oracle. The next materially different checkpoint requires a permitted Engineering Flutter/Chrome execution environment and authoritative product/server/device evidence; additional synthetic manifest-only tests should not be promoted as substitutes.

## 7. Primary source pointers (exact paths)

- https://github.com/yhappcom/logmate/blob/5ad78167cb97d6846ed7b5f866151d2a080dcc88/lib/repository/logbook/sembast_logbook_repository.dart
- https://github.com/yhappcom/logmate/blob/5ad78167cb97d6846ed7b5f866151d2a080dcc88/test/repository/logbook/whole_ledger_backup_test.dart
- https://github.com/yhappcom/logmate/blob/5ad78167cb97d6846ed7b5f866151d2a080dcc88/test/repository/logbook/sync_replica_identity_safety_test.dart
- https://github.com/yhappcom/logmate/blob/5ad78167cb97d6846ed7b5f866151d2a080dcc88/test/repository/logbook/sync_operation_binding_acceptance_test.dart
- https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md
- https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_logmate_inbound_cursor_atomicity_transfer.md
- https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md
