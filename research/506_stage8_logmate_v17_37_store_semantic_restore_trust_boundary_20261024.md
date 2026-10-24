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


## 8. F1 consumer-path and recovery-hold collision audit [SOURCE / SYNTHESIS / CONTRADICTION / OPEN]

**Source pin and method:** 2026-10-24, LogMate read-only `main@5ad78167cb97d6846ed7b5f866151d2a080dcc88`; directly inspected the full 6,148-line `lib/repository/logbook/sembast_logbook_repository.dart`, all 137 lines of `sync_persistence.dart`, `sync_operation_binding_acceptance_test.dart`, `sync_replica_identity_safety_test.dart`, the B1 test inventory, F1 acceptance closure and current `MASTER.md`. Searched exact store-reference uses within the complete repository adapter, not merely excerpts. This is a **bounded static source audit**, not a compiled whole-app call graph, executed Flutter test or deployed Sync adapter audit. GitHub code-search returned no indexed matches and cannot be used to claim a whole-repository negative.

### 8.1 Ownership and consumer census [SOURCE]

| Store / seam | Observed exact adapter usage | Consequence |
|---|---|---|
| `_syncStateStore` | initialization, owner-UID rewrite, state validation, restore reset, legacy drop/empty check, durable-data count | Local state is not proof of authenticated stream binding. `_validateSyncState` checks shape/owner/replica consistency, not server authority. |
| `_syncBindingStore` | frozen binding get/put in `_writeF1OperationBinding`, restore/legacy drop, empty/count | A supported simple Flight CREATE can create `eligibleProven` **local payload evidence** atomically with record/revision/outbox. It is not an ACK. |
| `_syncReceiptStore` | declaration, v1 restore drop, legacy empty check, durable-data count | **No direct receipt read or write in this audited adapter**. A v2 restore copies its rows generically via the 37-store registry. No authenticated remote Receipt consumer is demonstrated. |
| `_syncHeadStore` | declaration, v1 restore drop, legacy empty check, durable-data count | **No direct record-head read or write in this audited adapter**. V2 generic copy is not current server-head authority. |
| `_syncCursorStore`, `_syncAppliedIdentityStore` | restore-to-hold/drop, legacy drop/empty check, durable-data count | No normal inbound apply/cursor advancement consumer observed in the adapter. Source progress is historical evidence on restore, not destination progress. |
| `_syncHoldStore` | deferred/legacy hold creation, restored cursor/identity hold put, v1 drop, legacy empty/count | Recovery holds are evidence custody. Their key uniqueness across *successive restorations* requires additional validation (8.3). |
| `confirmPendingOperation` | explicit deprecated API always throws `invalidMutationPlan` | Unverified caller cannot delete Outbox through this API. It does not prove future server receipt validation. |

**Specific source points:** adapter lines 191–208 (store refs), 419–480 (v2 export), 483–592 (restore/reset), 2380–2386 (fail-closed legacy confirm), 2455–2467 and 2746–2755 (atomic F1 binding), 2802–2859 (binding eligibility and deferred holds), 3350–3365 (owner/state coupling), 4799–4882 (Sync state validation), 5918–5924 (restore reference checks). `sync_persistence.dart` explicitly states that F1 has no remote-operation decoder; `F1-R03` remains NOT VERIFIED in the acceptance record. The product `MASTER.md` likewise leaves Manual Delta Sync, authenticated Receipt, remote apply and convergence unimplemented at this source pin.

**TRANSFER VALIDATION:** Engineering D006's cursor/application atomicity invariant remains applicable to a *future* inbound adapter, not proof that an inbound adapter exists today. Design Studio W121's exact-runtime evidence gate and Marketing 438's PWA ad-free / no false Sync-complete contract are unchanged.

### 8.2 Correct authority interpretation [MINTTAP DECISION / DEPENDENCY]

1. `eligibleProven` means a locally frozen, digest-bound eligible outbound operation; **not** sent, accepted, applied, remotely acknowledged, or converged. The operation's `originReplicaId` is the *source* replica. Copying the binding during restore does not make it a new destination-origin operation.
2. Source Sync receipts and record heads are **copied bytes of unknown current authority**. No consumer is observed in the audited adapter, so report a *future consumer contract requirement*, not a demonstrated remote-ACK exploit.
3. `_resetRestoredSyncTrust` sets destination `unbound/unverified` and moves live source applied cursor/identities to holds; copied receipts/heads/bindings must never bypass that state when a future consumer is added.
4. `snapshotDigest` is an unkeyed integrity checksum. A checksum-correct LBK, matching caller-supplied `verifiedOwnerUid`, local owner unlock or local `eligibleProven` binding cannot authenticate server Receipt provenance. Server-side admission must establish owner, operation/digest, stream/epoch, freshness, replay/idempotency and destination authority independently.
5. `_validateRestoredLbkReferences` calls canonical ready-state and aggregate-manifest checks. It is **not a receipt signature/provenance verifier**. Absence of such verification is expected while remote Receipt handling is intentionally unimplemented; it is a release requirement, not proof of a shipped vulnerability.

### 8.3 New conditional collision counterexample: recovery hold overwrite [SOURCE / CONTRADICTION / OPEN]

**Source-level sequence:** v2 restore first generically copies every source `logmate_sync_holds_v1` row. It then iterates live source cursor and applied-identity rows, writing to `_syncHoldStore.record('restored:${source.name}:${row.key}').put(...)` (adapter lines 496–507 and 569–580). The `put` has **no prior-key-exists check**. A collision with a preexisting source hold of that exact key therefore replaces the older hold value in the destination transaction.

**Falsifiable minimal source fixture** (synthetic, not production): source `sync_holds` contains key `restored:logmate_sync_applied_cursor_v1:stream` with historical evidence A; source *live* `sync_applied_cursor` contains key `stream` with newer evidence B. A valid v2 export carries both. A fresh destination v2 restore copies A, then writes B at the same destination hold key. Post-restore only B is at that key: **historical hold A is not preserved under its original key**. The same conditional collision applies to `restored:logmate_sync_applied_identities_v1:<operationId>`. The current F1 product has no observed normal remote cursor writer; consequently this is a **source-level, future-Sync/repeated-recovery compatibility risk**, not an observed user-data-loss incident or proven currently reachable production path.

**Why it matters:** A device restored from an earlier backup can retain recovery holds, then eventually acquire new live Sync progress after a future authenticated adapter is implemented. A later backup/restore may reuse the same cursor key or applied operation ID. Treating every restore as a fresh one-time import conceals this multi-generation evidence-custody edge. This is distinct from duplicate keys *within a single store* (already checked by `_validateLbkContainer`); the collision occurs **between two different source stores after transformation**.

**Decision for Engineering:** Before any authenticated Sync rollout, either (a) fail closed on hold-key collision inside the existing restore transaction and preserve source/destination unchanged, or (b) introduce an explicitly versioned, collision-safe recovery-evidence lineage key with independent provenance and semantic migration tests. Do **not** silently overwrite, discard older evidence, rewrite history, or infer authority from either hold. Engineering owns implementation and may choose a better compatible scheme after testing. This study changes no LogMate source.

### 8.4 Twelve-case executable handoff [VALIDATION / DEPENDENCY]

| Case | Fixture / action | Required independent oracle |
|---|---|---|
| R01 | v2 populated source with no prior holds and one live cursor | Destination cursor empty; one new source-evidence hold; state unbound/unverified. |
| R02 | v2 populated source with no prior holds and one applied identity | Destination applied store empty; one new identity hold; source operation ID retained. |
| R03 | v2 source with preexisting hold and **same generated cursor-hold key** | No silent loss of either evidence A or B; current implementation is a **conditional overwrite candidate**. |
| R04 | v2 source with preexisting hold and **same generated identity-hold key** | Same preservation or fail-closed requirement as R03. |
| R05 | v2 source with different hold keys | Existing holds and newly generated holds all retained; no unintended merge. |
| R06 | backup→restore→re-export→later nonempty progress→restore | Provenance survives multiple generations, not just first restore. |
| R07 | copied `eligibleProven` binding with source replica ID | Remains historical source-origin binding; cannot be reclassified as destination ACK. |
| R08 | copied receipt/head shaped like accepted remote result | Locked/unbound destination must not emit remote-complete or advance cursor. Future consumer must validate authenticated stream. |
| R09 | forged-but-self-consistent checksum / altered receipt/head | Digest validation alone cannot authorize remote state; no trust promotion. |
| R10 | `confirmPendingOperation` invoked with fabricated operation | Throws; original Outbox remains. Current source-level expectation, not server acceptance test. |
| R11 | injected exception after store writes during restore | Whole transaction rolls back, including copied holds and transformed rows; fresh destination unchanged. |
| R12 | actual v17 Chrome IndexedDB process exit/relaunch, then Safari/Home Screen and managed-iPad envelopes | Compare semantic source/restore/hold state with exact build/provenance; no Chrome→iPad inference. |

**Priority:** R03–R04 are newly exposed **P0 design/negative-fixture review before remote Sync consumer implementation**, not a current production severity classification. R01–R02, R05–R11 should be executed on exact current Flutter/Sembast source by Engineering; R12 requires permitted browser and device environments. Synthetic map/digest tests alone cannot promote a product gate. Avoid real owner UIDs, flight payloads, tokens or receipt secrets in shared logs.

### 8.5 Platform and cross-track transfer [SOURCE / CHANGE WATCH / TRANSFER]

- **Track E (primary):** owns restore evidence custody, trust reset, non-overwrite, no ACK promotion, incident/recovery rollback and release HOLD. The new collision question is a preservation invariant, not a generic browser quota question.
- **Track A:** owns Service Worker control, origin/profile and IDB transaction boundaries. Worker activation does not establish Sync receipt authority or prevent a logical recovery-hold key collision. Source: https://w3c.github.io/ServiceWorker/spec/service_worker/ (checked 2026-10-24).
- **Track C:** owns R01–R12 typed semantic oracle, populated fixture, negative cases, independently confirmed browser-process restart, and separate physical-iPad evidence. IDB transaction completion does not equal crash-proof disk flush or independent backup. Source: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB and https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability (checked 2026-10-24).
- **Track B:** distinguish `local saved`, `eligible outbound`, `restored locked`, `source progress held`, `remote unverified`, `authenticated ACK`; a copied receipt must not render “Sync complete.” Design Studio owns visual/AT/human execution.
- **Track D:** measure restoration/hold-collision/revalidation outcomes using privacy-minimized counts and explicit `UNKNOWN` states. Marketing 438's first-release PWA ad-free recommendation is unaffected; no Sync-success or durable-offline marketing claim without actual evidence.
- **WebKit/iPad CHANGE WATCH:** browser origin quota, eviction and persistent storage are platform/OS/context-dependent; Safari/Home Screen/MDM evidence cannot be inferred from Chrome. Source: https://webkit.org/blog/14403/updates-to-storage-policy/ (checked 2026-10-24). Independent export/restore is still necessary for irreplaceable offline EFB data.

### 8.6 Evidence verdict and adjacent-work checkpoint

**SOURCE VERIFIED:** Exact current adapter and F1 contract, local binding creation, fail-closed legacy confirmation, copied receipt/head rows, restore trust reset and the **conditional hold-key overwrite path**. **SYNTHESIS:** Cross-store transform can overwrite prior recovery evidence even when each source store individually has unique keys. **OPEN:** Reachability under future real Sync progress, chosen remediation, full-app consumer graph, actual Chrome execution, independent NORMAL artifact/Hosting, physical Safari/managed iPad, authenticated remote Receipt. **VALIDATION:** No Flutter/Chrome/managed-device or production run executed here; this is static inspection and a falsifiable fixture specification, not a reproduced product incident.

**Gate unchanged:** Stage 8 applied Security/Privacy/Trust; E highest-value bottleneck; A/C execution dependencies; B/D truthful-state/claim transfer. **Production validation OPEN; PWA release HOLD.** The next materially different checkpoint is Engineering's real current-head tests of R03/R04 plus R01/R02/R07/R08, exact Chrome populated 37-store restore and a permitted retained-profile process restart. Additional generic manifest-only micro-tests would not close this blocker.

## 9. R03/R04 collision-contract executable handoff and restore-transaction decision (2026-10-24) [SOURCE / SYNTHESIS / VALIDATION / OPEN]

### 9.1 Canonical refresh and bottleneck choice

**SOURCE (read-only, 2026-10-24):** Web Manager governance `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, latest Web Manager commits and §§1–8 of this study were reread. LogMate `main@5ad78167cb97d6846ed7b5f866151d2a080dcc88` remains the observed current head; historical v16 is not substituted. Exact source points: `sembast_logbook_repository.dart` export/restore lines 419–592, container validation and fresh-destination guard lines ~5840–5924, `whole_ledger_backup.dart` canonicalization/digest, `whole_ledger_backup_test.dart`, and `sync_replica_identity_safety_test.dart`. Relevant external canonical transfer was reread: Design Studio W121, Engineering D006 and Marketing 438. No edits were made to those repositories or to LogMate.

**Bottleneck comparison:** E is the primary Stage-8 expert-application owner: source-level recovery-evidence custody has a falsifiable loss condition and high consequence before remote Sync admission. A is a prerequisite supplier (Sembast logical key/transaction, IndexedDB browser lifetime, Worker/update independence); C is the high-pressure execution/semantic-oracle owner; B consumes the restored-locked/remote-unverified user-state contract; D consumes privacy-minimized release/measurement claims. Curriculum Stages 1–12 are already passed at their generic gates; this is **Stage-8 applied security**, not a reset of the curriculum. Work was intentionally concentrated on E→C transfer, rather than equal primers or additional synthetic Worker manifest tests.

| Track | Current applied gate | Missing prerequisite/evidence | Pressure / this bundle |
| --- | --- | --- | --- |
| **E** | Source-level v17 restore and trust-reset contract known; collision path SOURCE VERIFIED | Decide collision handling, preservation invariant, implementation/runtime proof, backup custody | **Highest**; fail-closed-vs-lineage decision and adversarial evidence |
| **A** | Worker/IDB/Sembast boundaries established generically | Actual current Chrome/Safari runtime and managed-iPad storage context | High dependency; no assumption that browser lifecycle prevents key overwrite |
| **C** | 37-store semantic matrix and R01–R12 specified | Compiled current-head Dart tests, browser process restart, exact build provenance | **High**; four-case real-repository handoff |
| **B** | Recovery-state vocabulary and Design Studio transfer established | Human/AT/physical-device states and safe interruption copy | Consumer; do not say `Sync complete` on copied evidence |
| **D** | Discovery/analytics privacy boundaries and Marketing transfer established | Deployed events, trustworthy server ACK/claim evidence | Consumer; measure `recovery collision/rejected` separately from `remote acknowledged` |

### 9.2 What the exact implementation proves—and does not

**SOURCE:** `exportWholeLedgerBackup` copies the v17 37-store registry under one Sembast transaction and computes `snapshotDigest` over canonicalized JSON. `restoreWholeLedgerBackup` validates the container and requires a fresh, unbound staging destination; it generically copies source stores, excluding local replica, then resets owner and Sync trust in one destination transaction. The reset loops live source cursor/applied-identity rows and executes `_syncHoldStore.record('restored:${source.name}:${row.key}').put(transaction, ...)`. Existing source holds have already been copied under their original keys. No collision test precedes this `put`. This is a **cross-store transformed-key collision**; the per-store duplicate-key validator does not detect it.

**SYNTHESIS:** A source `sync_holds` row with key `restored:logmate_sync_applied_cursor_v1:stream` and historical payload A plus a source `sync_applied_cursor` row keyed `stream` with newer payload B creates two distinct, individually valid source-store rows. On restore both target the same destination hold key. Under the inspected code path B replaces A in the transaction. The same construction applies to `logmate_sync_applied_identities_v1:op-source`. A successful atomic transaction can therefore publish a semantically lossy result; **atomicity alone does not prove preservation**. The source backup remains available if independently retained, but the destination's historical evidence is not intact.

**Scope:** The test seeds synthetic Sync rows directly at the Sembast persistence boundary; the current F1 implementation does not demonstrate a production remote-cursor writer or authenticated Receipt consumer. The counterexample is valid for the restore function given such an input, not proof that current user flows naturally generate it, nor proof of a deployed data-loss incident. It is a conditional pre-Sync design defect candidate. A valid LBK digest only checks integrity, not source authenticity; it does not solve the collision or authorize a server ACK.

### 9.3 Durable executable proposal (Engineering-owned integration)

**Handoff file:** `research/handoffs/recovery_hold_collision_test_PROPOSAL.dart` in Web Manager. It uses the actual `SembastLogbookRepository.open`, `createOwnedLedger`, `exportWholeLedgerBackup`, `restoreWholeLedgerBackup`, `WholeLedgerBackup.decode`, `StoreRef` and the in-memory Sembast factory from the pinned LogMate tests. It is **not** a rewritten JSON model, not a fake digest and not an app patch.

- **R03 (intentionally RED against pinned main):** preexisting cursor recovery hold A and live cursor B generate the same destination key. The proposed *conservative fail-closed* contract expects `FormatException` and an untouched staging database. Current code is expected to complete the restore and overwrite A, so the test should fail until fixed.
- **R04 (intentionally RED):** same construction for applied identity `op-source`; require rejection and unchanged destination.
- **R05 (expected GREEN control):** distinct old hold key plus live cursor and applied identity; restore should preserve all three holds, clear live destination cursor/identity, keep a fresh destination replica, lock owner and mark Sync `unbound/unverified`. A fix must not indiscriminately reject all nonempty holds.
- **R11 (expected GREEN control):** use a **noncolliding** old hold plus live cursor, inject `StateError` after writes, verify destination remains fresh/unbound with zero copied holds and source unchanged. The control intentionally avoids a collision so a future pre-write collision guard does not preempt the fault hook. This tests rollback, not disk durability.

**Execution truth:** The Dart proposal has been saved but **Dart/Flutter is not installed in this run environment**; no compile, analyze, Flutter test, Chrome or device run occurred. RED/GREEN above are **source-derived expectations**, not observed test results. Engineering should copy the proposal into a controlled LogMate worktree, run `dart format`, `flutter analyze`, `flutter test` on the exact source head, and preserve the expected-red baseline before applying a fix. Never report expected-red as a product PASS. The test-only direct StoreRef writes are not evidence that product UI can reach the same prestate.

### 9.4 Remediation decision tree and counterexample critique [MINTTAP DECISION / OPEN]

**Conservative first implementation candidate — fail closed:** While still inside the same restore transaction, check `_syncHoldStore.record(generatedKey).exists(transaction)` **before** writing the generated hold. If occupied, throw a typed restoration error and abort the entire staging restore. This preserves the input backup and destination prestate; no partial publication or silent loss. The check must be done transactionally, not as a preflight read in a separate transaction. Engineering decides the actual error class and whether a generic `FormatException` is appropriate; the proposed R03/R04 tests encode that class only as an initial candidate. Do not automatically delete the old hold to make room.

**Long-term alternative — collision-safe lineage:** Introduce a versioned identity for evidence instances that is independent of the mutable source store/key alone. Its uniqueness must be established across repeated backup→restore→re-export generations, not only within one import. Preserve *both* evidence payloads, source replica and backup lineage, original store/key, generation and uncertainty. Define canonical ordering/serialization and bounded growth/retention. A new format or migration may be necessary; it is **not** proven compatible with v1/v2 import by this study. A lineage scheme is not an authorization scheme: historical holds remain untrusted for remote cursor advancement until independently authenticated.

**Negative controls/diagnostics:** (1) identical keys across different source stores are not duplicates until the transform targets one hold namespace; (2) distinct keys must remain accepted; (3) duplicate keys *within* one source store should still be rejected by container validation; (4) a digest-valid, caller-crafted backup does not become authenticated; (5) a valid receipt/head/binding copied alongside holds cannot upgrade `unbound/unverified`; (6) a transaction rollback proves no partial local publication, not browser crash durability; (7) browser process reopen is not an independent backup; (8) Safari/Home Screen/MDM storage pressure can invalidate local-only custody regardless of collision handling.

**Operational recovery judgment:** When a collision is detected, do not mutate the original `.lbk`, clear the staging database outside a controlled transaction, invent a server ACK, or discard unique offline records. Expose a recoverable, non-success state and require an independent backup/export path before destructive repair. If fail-closed would block a user's only available recovery, Engineering must design a separately governed forensic/import path that preserves *both* payloads, rather than relaxing the default invariant silently.

### 9.5 Cross-track transfer and external evidence boundaries

**TRANSFER VALIDATION — Engineering D006:** Cursor progression is protocol state; atomic apply+cursor publication avoids a split-state loss, but does not guarantee semantically correct restore lineage. Here the transaction is atomic yet its *key projection* can discard historical evidence. The two findings are complementary, not competing. Engineering owns any production adapter, migrations, tests and server Receipt protocol.

**TRANSFER VALIDATION — Design Studio W121:** Exact-source runtime, accessibility and human evidence outrank further pre-runtime manifests. A rejected collision must be a legible, non-destructive recovery state, not a generic success toast or an inaccessible blocking dialog. The design system/AT testing remains Design Studio-owned.

**TRANSFER VALIDATION — Marketing 438:** The PWA remains ad-free by the conditional first-release recommendation. A Sync or recovery surface must not depend on ad display, and no restored Receipt or locally frozen binding can support a public `Sync complete` or seamless offline durability claim. Marketing owns vendor/ad decisions; D owns web analytics evidence.

**SOURCE / CHANGE WATCH — platform:** MDN IndexedDB documentation distinguishes transaction abort and browser shutdown; WebKit documents best-effort origin eviction, quota and persistence heuristics. These platform failure modes are independent of the deterministic Sembast key collision. Current primary references (checked 2026-10-24):
- https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/abort_event
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://w3c.github.io/ServiceWorker/

### 9.6 Checkpoint and next real evidence

**SOURCE VERIFIED:** exact v17 restore order, unconditional transformed-key `put`, source-container validation boundary, native memory test conventions, v17 37-store format. **SYNTHESIS:** collision can cause loss of older recovery evidence despite transactional atomicity. **MINTTAP DECISION:** fail closed or preserve two evidence instances under a versioned lineage; never silently overwrite. **VALIDATION:** Engineering-ready real-repository Dart proposal with two expected RED cases and two expected GREEN controls, **not compiled/executed**. **OPEN:** actual compiled R03/R04 behavior; selected remediation and its regressions; product-reachable remote Sync progress; Chrome IndexedDB, retained-profile process restart, exact NORMAL artifact/Hosting, physical Safari/Home Screen/managed iPad and authenticated remote Receipt. **DEPENDENCY:** Engineering execution and product decision before release-gate promotion. **CONTRADICTION:** “37 stores present + transaction committed” is not sufficient for semantic recovery-evidence preservation.

**Gate unchanged:** Stage 8 applied Security/Privacy/Trust; E major bottleneck, A/C dependencies; Production validation **OPEN**, PWA release **HOLD**. Adjacent valuable questions were checked: additional generic Worker/manifest studies cannot resolve the identified semantic collision. The next meaningful checkpoint is Engineering's exact-head execution of R03/R04/R05/R11, a reviewed remediation, then real Chrome populated 37-store restore and independent process-restart evidence, followed by separate managed-iPad testing.
