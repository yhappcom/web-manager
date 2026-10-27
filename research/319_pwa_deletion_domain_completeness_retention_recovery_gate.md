# 319 — PWA Account-Deletion Domain Completeness, Retention, Tombstones & Recovery Proof

Status: **PASS (generic/platform + bounded canonical-source contradiction) / PRODUCTION, RELEASE, PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-10-08  
Owner: **Track E — Web Architecture, Security & Operations**  
Depends on: 315–318 (logical operation identity, current admission, idempotency, account-deletion authority retirement).  
Transfer: A browser/storage mechanics; B deletion/recovery UX and public-content parity; C independent negative tests; D privacy-minimized measurement. Web Manager coordinates, not a sixth track.

## SOURCE — primary evidence and limits

1. Firestore deleting a parent document does **not** recursively delete its subcollections. Collection deletion is non-atomic: https://firebase.google.com/docs/firestore/solutions/delete-collections
2. Firebase Delete User Data extension is limited to configured Firestore/Realtime Database/Storage scopes. Recursive traversal and discovery depth must be configured; embedded UID references in arrays/maps or deeper paths are not automatically complete: https://firebase.google.com/docs/extensions/official/delete-user-data
3. Firestore TTL is asynchronous, generally within 24 hours; expired records may remain readable until removed, and deleting a parent does not delete child subcollections: https://firebase.google.com/docs/firestore/ttl
4. Managed bulk deletion is collection-group scoped and non-atomic; it omits documents added or modified after job start. Deleting a parent collection does not implicitly delete child collection groups: https://firebase.google.com/docs/firestore/manage-data/bulk-delete
5. Firestore managed export is **not** a point-in-time snapshot taken at export start; changes during export may be included. Import overwrites matching IDs, leaves nonmatching documents and does not trigger Cloud Functions. Selected collection-group exports require explicit scope checks: https://firebase.google.com/docs/firestore/manage-data/export-import
6. In-place restore deletes and restores under the same database ID; Firestore warns that offline cached writes may later flush into the restored database. PITR and backups preserve historical data but not necessarily current deletion authority: https://firebase.google.com/docs/firestore/restore-in-place ; https://firebase.google.com/docs/firestore/pitr ; https://firebase.google.com/docs/firestore/disaster-recovery
7. Firebase Admin bulk user deletion does not emit per-user Authentication deletion handlers: https://firebase.google.com/docs/auth/admin/manage-users
8. WebKit's iOS/iPadOS 17.2 Home Screen web-app installation copies cookies but not other browser local storage, and website data is not shared after installation. This is **version-scoped platform evidence**, not proof of the exact managed-iPad deployment: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/
9. Clear-Site-Data requests browser cleanup only when the response is actually received/processed; support and directives are browser-dependent. It cannot remotely wipe a never-reconnected iPad: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data
10. Apple requires qualifying account-creating App Store apps to provide discoverable in-app account-deletion initiation; ordinary support email is not a substitute except under applicable regulated-industry conditions. Delayed/manual deletion requires transparent progress and completion confirmation. Provider revocation is a separate responsibility: https://developer.apple.com/support/offering-account-deletion-in-your-app/ ; https://developer.apple.com/documentation/technotes/tn3194-handling-account-deletions-and-revoking-tokens-for-sign-in-with-apple

## HISTORY / PROBLEM → PRINCIPLE → IMPLEMENTATION → EXPERT JUDGMENT

An identity-delete API or a deletion-job success response is an *event*, not a complete account-erasure proof. Modern offline-first applications create a graph of authoritative records, derived projections, nested collections, receipts, exports, processor copies, pending work and device-local storage. Asynchronous cleanup, restore/import and long-offline devices make single-UID-string deletion insufficient.

**C1 — authority retirement:** predecessor identity/credential/outbox cannot cause new material remote effects. **C2 — active-domain erasure:** all in-scope active stores are inventoried, erased and independently checked. **C3 — historical/recovery containment:** backups/PITR/exports/retention exceptions are classified and restored predecessor bytes cannot silently become current authority. These planes require separate evidence and honest completion language.

Version each deletion-domain inventory entry with: ownership and classification (primary/derived/queue/receipt/cache/export/log/backup/processor); direct and indirect identity edges including nested arrays/maps/foreign keys; all writer paths (foreground, admin, worker, webhook, import, stale offline); actual deletion/traversal method and race limitations; independent survivor oracle; retry/UNKNOWN reconciliation; lag/escalation; exception purpose/legal basis/access/expiry; recovery treatment; inventory version and evidence date.

**Ordering:** REQUESTED → SUBJECT_VERIFIED → MATERIAL_WRITERS_FENCED → ERASURE_IN_PROGRESS → ACTIVE_DOMAINS_VERIFIED → RECOVERY_CONTAINED → COMPLETED. Per-domain UNKNOWN, FAILED_RETRYABLE, ESCALATED, EXCEPTION_RETAINED must be explicit. Stable deletion request ID supports idempotent resume but is not authorization. Fence each material writer before erasure; reconcile in-flight effects and independently rescan after async/race windows. Do not equate a worker's own success flag with negative proof.

**Tombstone/retention paradox:** A deletion receipt may be necessary for anti-replay, but indefinite raw email/UID/provider-subject tombstones can recreate a shadow identity database. Separate minimal current-authority generation/revocation predicates from short-lived worker receipts, narrowly justified legal retention exceptions and erasable product records. Hashing is not automatically anonymization. Retention horizon, key custody, linkability and legal authority require product review. Tombstone expiry must not re-enable stale mutation authority.

## Recovery-proof independence — key integrated finding

A deletion ledger or current authority generation stored **only in the database being rolled back** can disappear when a pre-deletion snapshot is restored. This is an inferred architecture failure mode, not evidence of LogMate implementation. Recovery must re-establish current deletion/authority state from a source protected from the relevant rollback failure domain (or through an explicit trusted re-establishment process). If that source is unavailable: **RECOVERY AUTHORITY UNKNOWN / HOLD**, never fall back to the old snapshot's permissive policy.

Recovery acceptance sequence: identify artifact, time and coverage (including mixed-time exports and omitted collection groups); hold material writes; independently establish current subject/retirement/authority generation; overlay deletion and retained-exception policy; independently scan survivors and late writers; test authorized successor positively and retired predecessor negatively; reopen only validated consequence classes; record minimal expiring evidence and rollback trigger. A successful restore, same database ID, authentic historical token or restored local queue is not present authorization.

**Operational counterexamples:** parent deleted/child remains; TTL expired/record still queryable; bulk-delete job completes/late writer survives; batch Auth delete bypasses cleanup trigger; managed import reintroduces data without Functions; old recovery snapshot removes deletion fence; stale iPad reconnects after database-ID reuse; support page promises nonexistent Settings action; local browser wipe leaves Home Screen context unverified; permanent raw-UID tombstone creates unnecessary retained identity.

## Canonical LogMate source transfer / CONTRADICTION

Inspected LogMate main at 2026-10-08, commit `6537503de85b284d149145ba9ec58d874cbe4224`. `web/account-deletion/index.html` tells users to open Settings and select an account-deletion option; `lib/screens/settings_screen.dart` currently offers Import, Previous Total setup and Sign out but no deletion action. `functions/index.js` only documents retirement of an earlier lookup callable, not deployed destructive adapters. `.github/workflows/member-operations-validation.yml` is manual `workflow_dispatch` only. **Public instruction ≠ shipped path; source-level coordinator ≠ deployed erasure backend; workflow exists ≠ automatic enforcement.** Actual production release, backend/IAM, legal classification and App Store applicability remain OPEN.

Latest Design Studio change `199663083d0cccd3d99ade3531fa1933e8714483` concerns CrewConnex PDF decoding, not PWA/managed-iPad proof. Marketing claim-registry guidance transfers only the principle that public deletion promises need verified released-feature evidence. Software Engineering remains owner of implementation/fault-injection realization, not Web Manager generic primers.

## VALIDATION — designed cases 69–92, continuation of 318's 53–68

69 indirect/nested/processor identity graph complete; 70 deleted parent leaves child; 71 extension shallow/depth omission; 72 separate data service omitted; 73 TTL expired but readable; 74 TTL parent removed/child survives; 75 TTL field changed/removed; 76 bulk-delete late writer survives; 77 cancelled/partial bulk-delete safe resume; 78 destructive success response lost and UNKNOWN reconciled; 79 Admin batch deletion bypasses per-user handler; 80 indirect foreign-key survivor; 81 externally exported user copies disclosed without impossible wipe promise; 82 retention exception purpose/basis/expiry/access; 83 excessive tombstone shadow-identity rejected; 84 receipt expires but long-offline predecessor still denied; 85 PITR/backup rollback reapplies retirement; 86 import without Functions requires explicit re-audit; 87 same database ID does not admit stale iPad write; 88 recreated email/provider identity isolates predecessor outbox; 89 delayed worker/webhook cannot recreate deleted effects; 90 accessible truthful REQUESTED/UNKNOWN/COMPLETED UX; 91 public page vs Settings vs release/backend plus separate Safari/Home Screen local cleanup; 92 successor-positive and predecessor-negative proof (zero observed traffic is not rejection proof).

**R1–R8 recovery fault-injection extensions (subcases, not new numbered PASS):** R1 pre-deletion snapshot restore; R2 deletion fence stored only in restored DB; R3 concurrent changes during non-snapshot export; R4 partial collection-group import; R5 current-authority source outage; R6 delayed privileged writer after restore; R7 dormant managed iPad return; R8 excessive retained identity/receipt graph. Expected: fail-closed current material admission, independent survivor oracle, explicit local preservation/reconciliation and minimized retention.

Every case requires fixture, exact build/ref, initial state, injected fault, material boundary, independent oracle, PASS/FAIL/UNKNOWN, timestamps, CI execution proof, OS/browser/MDM envelope where applicable. These cases are **specified, not executed**. Earlier 1072 defined campaign + 16 in 318 + 24 in 319 = 1112 *if* the 1072 baseline remains current; not an execution count.

## Five-track bottleneck allocation / TRANSFER VALIDATION

- **E primary bottleneck:** versioned deletion graph, all-writer fence, independent authority recovery, exception/retention governance, destructive UNKNOWN and incident reopen.
- **A prerequisite supplier:** service-worker/IndexedDB/Cache/browser-context semantics, Safari vs installed app and offline delivery; no claim of background wipe/sync.
- **B focused consumer:** truthful deletion request/progress/completion UX, installed vs Safari local-state disclosure, public content and shipped Settings parity; Design Studio owns general visual design.
- **C challenger:** independent negative oracles, fault injection, device/AT/human/CI enforcement; test specification never promoted to production PASS.
- **D bounded consumer:** privacy-minimized deletion/recovery observability, public claim invalidation; telemetry cannot elect current authority.

## MINTTAP DECISION

Require versioned deletion-domain inventory and independent current-authority recovery proof before declaring a deletion complete. Distinguish server retirement, active erasure, retained exceptions, independent user exports, and unreachable local copies. For EFB/LogMate, preserve unique permissible offline data and offer explicit recovery/reconciliation without reviving predecessor remote authority. Avoid selecting an unverified vendor or sync topology.

## OPEN

Actual LogMate/MintTap production data graph; Firebase project/tenant policy, deployed backend/adapters/IAM; all privileged writers and delayed jobs; retention/legal horizon; receipt/tombstone schema; independent currentness source; restore/import configuration; physical Safari/Home Screen/managed-iPad tests; deployed UI and public content parity; destructive CI enforcement; provider revocation, deletion completion and user notifications. Production validation OPEN.

## CHANGE WATCH

Firebase extension depth/coverage, TTL/bulk-delete/import/backup/PITR/restore, Apple account-deletion and Sign in with Apple rules, Safari/WebKit/iPadOS context isolation and storage, exact LogMate release source and managed-device policy. Recheck primary sources and production config before release.


---

## 2026-10-27 applied LogMate v17 deletion-domain inventory and owner-lock transfer — SOURCE-LEVEL CONTRADICTION (not production validation)

**Canonical source pin:** LogMate `main@26d2d7cf2c20c55026c6f84b838dcb6442f7a3f1`; `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb`, `lib/application/account_deletion_coordinator.dart@8e844e888b39d3b5e1648aeb84be26e6582ed60f`, `lib/domain/account_deletion_state.dart@499037bd3a50058757f8155d2287e7f301f2eafc`, `test/application/account_deletion_coordinator_test.dart@54dac071bf0cd34a93dd674cff5f5106037079d0`. Reviewed 2026-10-27. The earlier generic deletion-domain graph is now applied to the **actual 37-store v17 adapter**, not merely a hypothetical Firebase cleanup.

### 1. Store-coverage reconciliation [SOURCE / VALIDATION / CONTRADICTION]

The source declares **37** distinct Sembast store names in the v2 LBK registry (30 legacy + 7 Sync), but `wipeLocalUserDataAndCompleteDeletion` (lines 1051–1104) calls `drop(transaction)` on **29** stores. A mechanical symbol/name comparison of the exact adapter identified **eight** stores absent from the local wipe:

| Surviving store symbol | Durable store name | Possible retained category / consequence |
| --- | --- | --- |
| `_localReplicaStore` | `logmate_local_replica_v1` | Previous device/replica identity retained after account deletion. |
| `_syncStateStore` | `logmate_sync_state_v1` | Existing stream/baseline state and other fields may survive owner reinitialization. |
| `_syncBindingStore` | `logmate_sync_operation_bindings_v1` | F1 operation bindings can include **old owner UID, record identity and encoded payload**. |
| `_syncReceiptStore` | `logmate_sync_receipts_v1` | If populated, old receipt evidence remains. |
| `_syncAppliedIdentityStore` | `logmate_sync_applied_identities_v1` | If populated, prior applied-operation identity evidence remains. |
| `_syncCursorStore` | `logmate_sync_applied_cursor_v1` | If populated, prior stream cursor remains. |
| `_syncHeadStore` | `logmate_sync_record_heads_v1` | If populated, prior record-head evidence remains. |
| `_syncHoldStore` | `logmate_sync_holds_v1` | If populated, deferred/recovery evidence may remain. |

The 29 dropped stores include canonical flight records, revisions, drafts, custom fields and the deletion-state row. This is **not** a claim that those 29 stores survive. Nor does every undropped Sync store necessarily contain records in every deployment. The defect class is **incomplete inventory coverage when nonempty**, not proof of observed residual flight data on a real device. Sembast documents `StoreRef.drop` as deleting a store and its contents; leaving a store out is not equivalent to dropping it. Primary: https://github.com/tekartik/sembast.dart/blob/master/sembast/doc/how_to.md .

**Strongest source-derived counterexample:** `_writeF1OperationBinding` (lines 2804–2859) writes a Sync binding containing `ownerUid`, `recordId`, `revisionId` and an encoded record payload for eligible operations. If a disposable fixture first creates a bound owner A and an eligible F1 binding, then successfully completes the account-deletion saga, the wipe loop does not drop the Sync binding store. The exact executable result remains **NOT RUN**; the control-flow/store-coverage mismatch is directly visible.

### 2. Fresh initialization is not a fresh Sync trust domain [SOURCE / SYNTHESIS]

The deletion wipe calls `_initializeFreshDatabase` after dropping the 29 stores. Its `_writeReadyMigration → _publishCapabilityV7 → _writeOwnerAccess(unbound)` path **does update the surviving Sync State's `ownerUid` to null** (lines 3357–3373). This is an important correction to a tempting but wrong inference: the old owner UID is **not necessarily left in that particular Sync State field**. However, the same owner-write helper does not reset `streamBindingStatus`, `remoteBaselineStatus`, receipts, cursors, heads, holds or operation bindings. `_ensureSyncState` (lines 4807–4817) returns immediately when the old state row exists; `_ensureLocalReplicaIdentity` (2942–2952) preserves the old replica. `_validateSyncState` (4868–4889) checks owner-field equality and replica identity, but does not independently establish a fresh account's remote authority or require the seven Sync stores to be empty.

Consequently, a subsequent owner-B bind can rewrite only the Sync State owner UID to B while leaving **A-origin operation bindings** and the prior replica/trust indicators intact. This is a **conditional cross-owner contamination and deletion-completeness risk**, not evidence that remote Sync would accept the old operations. Independent remote authorization, currentness and receipt acceptance remain OPEN. A source-only “37-store backup” success does not prove deletion: the backup registry and the wipe registry are different mechanisms.

**Positive contrast:** `restoreWholeLedgerBackup` deliberately calls `_resetRestoredSyncTrust` (lines 562–592), clears applied cursor/identity authority and reclassifies source evidence under recovery holds; the v1 restore branch explicitly drops all seven Sync stores. This shows that the adapter already distinguishes *preserving recovery evidence on a verified restore* from *resetting local Sync authority*. Account deletion requires a different, more destructive, versioned all-store erasure policy; blindly copying the restore behavior into deletion would retain old-user evidence.

### 3. Deletion-phase lock is not enforced by the shared owner guard [SOURCE / CONTRADICTION]

`requestAccountDeletion` (986–1016) checks owner UID and writes `AccountDeletionPhase.localLocked` into deletion metadata, but does **not** change `LocalOwnerAccessLock.unlocked` or invoke `lockForExplicitSignOut`. `_requireUnlockedBoundOwner` (2983–2991) reads only the owner-lock state, **not** `AccountDeletionState.locksNormalAccess`. Therefore even several otherwise owner-guarded repository methods do not enforce a pending deletion phase at that shared boundary. Direct record `create/update/delete/restore` and `readActive/readActiveRecords` also lack the owner guard in their method bodies (previous 312 audit). This is a **source-level write-fence inconsistency** during the deletion saga; reachability, caller-level gates, and a real in-flight write remain untested.

**Positive control:** `exportWholeLedgerBackup` (422–439) independently checks the deletion phase and rejects export while deletion is pending. `LocalLedgerAccessCoordinator.resolveAccountRequiredStartup` checks deletion state before normal route admission. The latter is a **startup/UI gate**, not proof that an already-open tab or retained repository handle cannot write. Do not conflate the account-deletion phase, explicit-sign-out lock, Firebase session and remote server authority.

### 4. Independent source audit, limits and falsification packet [VALIDATION / OPEN]

A reproducible **12/12 static structural audit** over the pinned adapter and deletion-coordinator test asserted: 37 declared/registered stores; 29 wipe drops; exactly eight omitted (replica + seven Sync); deletion request not mutating owner lock; shared owner guard not checking deletion phase; export's positive deletion check; owner rewrite touching only Sync owner UID; Sync initialization preserving an existing row; replica initialization preserving an existing row; Sync validation not rejecting every unbound-owner/old-binding-status combination; F1 binding recording owner/payload; and deletion-coordinator test's lack of Sync-store assertions. This is a **T0 source-text audit**, not a Dart test, executed Sembast transaction, real account deletion, Chrome/Safari/MDM run, or proof of user harm. The existing coordinator test covers happy-path completion, remote retry and UID mismatch, but does not independently enumerate all 37 stores after erasure.

Engineering-owned **discriminating tests** (extend existing account-deletion test, W-030 F-01 and W-012/W-013/W-014/W-036; no duplicate test framework):

| Case | Fixture and stimulus | Required independent oracle |
| --- | --- | --- |
| DE01 | Populate all 37 store classes with safe synthetic A-owner data, including eligible F1 bindings and nonempty Sync holds/receipts/cursors | Before/after **typed-key and semantic** inventory, not only “deletion phase completed”. |
| DE02 | Complete full saga with stubbed successful external ports, then close/reopen same Sembast DB | Zero old-owner data across all in-scope stores, new replica identity, fresh unbound/unverified Sync state, no old payload/binding. |
| DE03 | Bind verified B after A deletion in same DB | No A-owned operation/payload/replica/trust inherited; no fabricated remote receipt/ACK; independent UID/owner/Sync checks. |
| DE04 | Request deletion then call guarded and direct read/mutation APIs on retained repository handle | All product-policy-disallowed operations reject; before/after record/revision/outbox/Sync digests unchanged. |
| DE05 | Race deletion phase request, in-flight transaction, remote-erasure completion and stale sibling tab | Deterministic ordering/fence; no late writer survives successful erasure; explicit retry/UNKNOWN state where needed. |
| DE06 | Fail provider revocation, remote erasure, identity deletion, or local wipe at each boundary | Correct durable phase, no premature completion, idempotent resume, no accidental loss of permissible recovery evidence. |
| DE07 | Attempt independent external .lbk restore and old offline PWA rejoin after deletion | No predecessor remote authority revival; old file and disconnected copy classified separately; truthful local cleanup scope. |
| DE08 | Safari tab vs Home Screen vs managed Web Clip with distinct storage containers | Per-container deletion/retention/MDM policy measured; never claim a server deletion automatically wipes an offline device. |
| DE09 | New owner account and Sync State with `bound/verified` old values after wipe | Prove fresh account cannot inherit remote admission or old operation bindings; source-level possibility is not server exploit proof. |
| DE10 | Run existing coordinator tests and new deletion regression on exact pinned Dart toolchain and NORMAL PWA | Record code ref, schema, environment, fixture, independent oracle, result and limitations; actual PASS only after execution. |

**Failure-first oracle:** do not mark account deletion complete solely from `AccountDeletionPhase.completed`, empty `_activeStore`, or a cleared Firebase identity. Compare the complete versioned local store registry, remote data domains, external backups and offline containers separately. An external user-owned backup is not automatically erasable by the app; a deleted remote account is not proof that an unreachable managed iPad has been wiped. Firebase's official Delete User Data extension explicitly deletes only configured domains: https://firebase.google.com/docs/extensions/official/delete-user-data .

### 5. Five-track ownership, cross-repository transfer and gate [MINTTAP DIRECTION / DEPENDENCY / CHANGE WATCH]

**E — primary/highest-risk owner:** 37-store deletion completeness, all-writer fence, cross-owner Sync state retirement, deletion vs restore semantics, remote/identity/local sequencing and data-retention classification. **A — prerequisite:** Sembast Web/IndexedDB transactional store semantics, multi-tab handles, WebKit Home Screen storage partitions and offline lifecycle. **C — high-priority challenger:** actual Dart negative/positive tests DE01–DE10, typed inventory, process reopen, browser/physical-device evidence and independent oracle per Software Engineering `methods/VALIDATION_STANDARD.md`. **B — bounded transfer:** Design Studio `progress/WEB_STATUS.md` W121 Stage 3 PRACTICE; user-facing deletion progress must not promise “all devices erased” or “backup deleted” without evidence. **D — bounded transfer:** Marketing Manager D9 claim hold; privacy-minimized evidence can report domain completion classes but must not collect UID, raw flight payloads, backup contents or auth codes. No peer or product repository is modified here.

**MINTTAP DIRECTION (research-level, not product change authorization):** Ask product Engineering to reconcile the deletion wipe with the **entire current 37-store registry**, establish an explicit pending-deletion write fence at each relevant material access boundary, and test both zero-survivor erasure and independent recovery/retirement semantics. Treat Sync State/replica/receipt/binding remnants as separate classes rather than erasing evidence indiscriminately before safe audit. Do not infer actual deployed deletion flow, actual user records, remote Sync privilege, or real device incident from this source audit.

**OPEN:** executable v17 Sembast deletion with nonempty seven Sync stores; UI/coordinator production reachability; server-side erasure/revocation adapter; actual Firebase/MDM/runtime release; cross-tab races; per-container local erasure; independent 37-store and external-file verification; privacy/legal retention policy. **CHANGE WATCH:** future LogMate schema/store additions must update the deletion-domain inventory and negative tests; Sembast/WebKit/FlutterFire behavior is version-sensitive. **Stop check:** compared full 37-store registry, wipe, owner rewrite, fresh init, replica reuse, Sync validation, F1 payload binding, backup-restore reset, deletion-phase fence, existing tests and multi-container semantics. Further T0 mock work has lower information gain than **actual Dart DE01–DE06 and exact NORMAL browser/managed-iPad DE07–DE10**. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**.


---

## 2026-10-27 applied continuation — deletion-saga safety, restart liveness, terminal re-entry and cross-context PWA admission

**Status: SOURCE / SYNTHESIS / CONTRADICTION / 18/18 bounded structural checks; actual Dart, web, Firebase, physical/managed iPad and deployed deletion VALIDATION OPEN.** This is a substantive continuation of the same Stage 8 deletion-domain study, not a new generic saga primer or proof of production failure. Canonical owner: **Track E**. Track A supplies browser/partition and state-transition prerequisites; C owns independent execution; B/D consume UX/claim implications. Product and peer repositories remain read-only.

### A. History/problem → principle → current implementation [SOURCE / DEPENDENCY]

Account deletion is a durable, potentially multi-system saga: reauthentication, provider revocation, remote erasure, Firebase identity deletion and local cleanup cannot be committed as one browser/database transaction. A **safety** invariant prevents unauthorized skipping, post-deletion mutation and cross-owner data inheritance. A **liveness** invariant ensures that after an interruption a legitimate subject/operator can resume, reconcile UNKNOWN, reach a terminal outcome and subsequently use the product with a new account without erasing evidence needed for anti-replay. Fail-closed UI alone can satisfy neither property.

Read-only product source pin: **LogMate main@7caaee998251602e72159eeebda61f701bdea270** (2026-10-27), unchanged relevant blobs from prior 319: account_deletion_state.dart@499037bd3a50; account_deletion_coordinator.dart@8e844e888b39; local_ledger_access_coordinator.dart@3fd1bb719d9a; session_gate.dart@5bcd6bf2089e; session_recovery_screens.dart@035ca07f1c86; settings_screen.dart@4affdb26f096; sembast_logbook_repository.dart@d7e4efd4f6dc; account_deletion_coordinator_test.dart@54dac071bf0c. These are **main source bytes**, not a verified production artifact or deployed backend. Prior 319's 37-store versus 29-drop/7-Sync-retention and pending-delete owner-fence findings remain distinct, complementary evidence.

**Primary platform/policy sources, rechecked 2026-10-27:**
- Firebase client account deletion requires recent sign-in: https://firebase.google.com/docs/auth/web/manage-users .
- Firebase Admin batch delete does not emit individual deletion triggers: https://firebase.google.com/docs/auth/admin/manage-users ; https://firebase.google.com/docs/functions/auth-events .
- Apple account-creating App Store apps ordinarily need a discoverable in-app initiation route; regulated-industry customer-service exceptions are conditional, not automatic for pilots: https://developer.apple.com/support/offering-account-deletion-in-your-app/ .
- Google Play requires an in-app deletion path and externally accessible web request resource; an email request route can be acceptable for the external resource if it works: https://support.google.com/googleplay/android-developer/answer/13327111 .
- Browser Clear-Site-Data is an HTTP response-triggered, support-dependent browser cleanup mechanism, not remote deletion authority for disconnected or separately installed contexts: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data .
- WebKit 17.2 documents distinct post-install Home Screen website storage and only cookie copying at creation: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ .

**Cross-repository transfer (not duplicated ownership):** Marketing Manager STATUS D9 independently identified phase-skip/retry/re-entry/public-claim gaps; this continuation checked the exact current product source and places web release, recovery and platform admission requirements under Web Manager E. Design Studio progress/WEB_STATUS W121 remains Stage 3 PRACTICE with human/AT/device validation OPEN; its content/interaction discipline owns recovery presentation, not Web Manager. Software Engineering methods/VALIDATION_STANDARD.md owns executable independent-oracle practice and implementation changes.

### B. Exact source state machine: safety and liveness are separate [SOURCE / CONTRADICTION]

The durable enum contains **nine** phases in this order: none(0), requested(1), localLocked(2), reauthenticated(3), providerRevoked(4), remoteDataErased(5), firebaseIdentityDeleted(6), retryableIncomplete(7), completed(8). The normal coordinator starts at localLocked, handles phases 2–6 in sequence, and calls the local wipe only from firebaseIdentityDeleted. Positive: it verifies reauthenticated UID equality, uses a stable request ID for remote erasure and persists each completed external boundary before moving forward. Existing three memory-Sembast coordinator tests cover happy path, remote failure/resume when manually invoked, and UID mismatch.

**B1 — phase-transition contract is weaker than the coordinator's normal ordering.** The repository's public advanceAccountDeletion verifies ownerUid/requestId, forbids none/completed and decreasing enum index, but **does not require the immediate successor phase or verify the preceding external boundary's receipt**. A trusted caller invoking it with the matching identifiers can conditionally jump from localLocked to remoteDataErased; a subsequent coordinator resume would then call Firebase identity deletion without re-running reauthentication/provider revocation/remote erasure. This is a **repository API contract weakness**, not proof of an untrusted user input path, existing malicious caller, or actual deletion bypass. The normal coordinator itself does not make that jump.

**B2 — retryableIncomplete is a possible durable dead-end.** The repository permits advance to retryableIncomplete from earlier nonterminal phases, but coordinator.resume() has no branch for retryableIncomplete (nor requested). The coordinator's normal error path instead leaves the last completed phase and propagates an exception. Therefore an externally persisted retryableIncomplete/requested phase can yield a locked startup whose available resume method returns the same phase without progress. No current caller was proven to write retryableIncomplete; the issue is a reachable **API/state-space condition**, not an observed user failure.

**B3 — restart route has no inspected recovery action.** LocalLedgerAccessCoordinator.resolveAccountRequiredStartup checks deletion **before** owner/session handling. Any non-none phase returns LocalLedgerDeletionLocked except completed+signed-out, which returns authentication required. SessionGate maps deletionLocked to AccountDeletionLockedScreen(phase), a static screen with no resume/retry/reauthentication callback. SessionGate's inspected composition contains no AccountDeletionCoordinator instantiation or resume invocation. The separate StartupFailureScreen has Retry, but it is not the deletion-locked route. Thus the documented resumable coordinator does **not establish a resumable user journey** in the inspected production UI path. Other uninspected external entrypoints or a deployed administrative process are UNKNOWN; do not claim global absence.

**B4 — completed(A) can block signed-in B after a successful wipe.** The local wipe intentionally recreates a fresh unbound ledger and then persists AccountDeletionPhase.completed with **A's ownerUid and requestId**. createOwnedLedger(B) and bindOwner(B) do not reset this deletion record. At next account-required startup, completed+signed-out goes to authentication required, but completed+**any signed-in** observation returns deletionLocked before B can be considered for fresh owner binding. This is a **source-predicted terminal re-entry/liveness contradiction**, not an executed Flutter/Firebase result. A completed deletion receipt may be useful anti-replay evidence, but retaining A's UID/requestId in the active routing predicate indefinitely also raises a data-minimization and successor-use question. Do not erase it blindly without defining current-authority/retention policy.

**B5 — public web instructions and actual UI are inconsistent.** The source page web/account-deletion/index.html says to open Settings and choose account deletion; inspected SettingsScreen exposes Import, Previous Total setup and Sign out, with no deletion action. The external support mailto route is a documented **request channel**, not verified monitored mailbox, UID-proof flow, deployed erasure or App Store compliance. Apple and Google Play impose different in-app/external requirements; do not assume the Google Play email allowance satisfies Apple's ordinary in-app rule. The company's actual release, jurisdictional/regulated-industry classification and console declarations remain OPEN.

**B6 — do not conflate replica retention with owner-data retention.** Previous 319 identified one opaque local replica ID and seven Sync stores omitted from the 29-store wipe. Marketing D9 flags that retaining a non-account-linked opaque replica identity may be intentional. The correct Web Manager admission rule is **classification and independent owner-linkage proof**, not an unqualified demand to regenerate every device identifier. Seven Sync stores still need explicit A-owned payload/authority retirement; reusing a stable opaque replica ID is acceptable only if the product's privacy/Sync contract and independent B-after-A negative controls establish it cannot carry A's account data or authority. This refines prior DE02/DE03 “new replica identity” wording; those are proposed negative controls, not a fixed product policy decision.

### C. Integrated counterexamples and operational judgment [SYNTHESIS / EXPERT JUDGMENT]

- **Safety without liveness:** deletion locks the startup UI, but no resume action is available; user cannot reach either a verified completion or a safely recoverable state through the inspected route.
- **Liveness without safety:** an unrestricted retry advances to a later phase without receipts and may skip revocation/erasure; successful “completed” is not valid proof.
- **Terminal poisoning:** completed(A) survives local wipe, signed-out shows sign-in, signed-in B immediately sees deletion-locked again; a stable receipt is being used as an access gate.
- **Cross-tab race:** tab A enters localLocked; tab B retains repository handles and may not observe deletion phase at material write admission (prior 312/319). A retry screen cannot repair missing write fences.
- **Cross-container false completion:** server account deletion and Safari-tab cleanup do not demonstrate Home Screen Web App, MDM Web Clip or native device data removal. A disconnected EFB cannot be remotely wiped by a response it never receives.
- **Blind Clear-Site-Data repair:** an origin-wide storage purge can delete unique offline flight records and Service Worker registration, while not proving cleanup of a separate installed context or user-owned LBK file. Do not use as a default fix for an incomplete seven-store erasure.
- **Provider delete succeeds, response lost:** Firebase's recent-login requirement and external asynchronous effects make UNKNOWN reconciliation essential; re-running every external operation unconditionally can be incorrect.
- **Recovery after identity deletion:** a local-only resume may be possible from firebaseIdentityDeleted, but the inspected UI does not expose it. Recovery must not require a deleted account to authenticate again merely to complete local cleanup.

**MINTTAP DIRECTION (research, not authorization to change LogMate):** Specify an explicit deletion-state transition graph with phase-specific evidence/receipt preconditions and idempotent UNKNOWN reconciliation. Define terminal completion as two distinct concerns: a minimal privacy-reviewed deletion receipt/anti-replay fence, and a **nonblocking new-owner startup decision**. Provide a recoverable in-app/user-or-operator continuation path consistent with Apple/Google policy, and make local write admission independent of the screen route. Account A data retirement and account B fresh start require independent positive/negative evidence.

### D. Falsifiable validation packet — DL01–DL16 [VALIDATION — NOT EXECUTED]

Reuse existing LogMate W-030 F-01, W-012/013/014, W-031/036, and 319 DE01–DE10. No duplicate test framework or product code change is made by Web Manager. Engineering must record exact source/ref, compiled target, 37-store typed inventory, phase, current/previous UID, external-port call receipts, interruption point, before/after raw store and backup digests, browser/OS/MDM context and negative/positive verdict.

| Case | Independent discriminating oracle |
| --- | --- |
| DL01 | For each normal phase 2–6, force process interruption; close/reopen and resume **through the actual supported UI/operator path**; no repeated completed external effects. |
| DL02 | Persist requested(1) fixture and restart; explicit supported recovery/migration disposition, never permanent silent lock. |
| DL03 | Persist retryableIncomplete(7); verify explicit retry/reconcile/escalate path or documented rejection, not inert resume. |
| DL04 | Direct advance localLocked→remoteDataErased with matching UID/requestId; assert forbidden absent independent evidence of required intermediate effects. |
| DL05 | Attempt advance with wrong UID/key, backward phase, completed/none, and same-phase retry; verify precise contract and no material effects. |
| DL06 | Provider revoke/remote erase/Firebase identity delete success with lost response; reconcile authoritative receipt and continue exactly once per logical request. |
| DL07 | Completed(A) + signed-out cold start → usable authentication route; then signed-in verified B → **fresh unbound B onboarding**, not deletion lock or A access. |
| DL08 | Completed(A) + signed-in A/stale Firebase token; no A-data revival or automatic owner rebinding; route is safe and recoverable. |
| DL09 | A deletion followed by B binding and B deletion request; no A receipt collision or old Sync bindings; B request has independent identity. |
| DL10 | During localLocked, stale second-tab direct/guarded CRUD, outbox, restore and draft operations all honor current deletion fence; raw stores unchanged. |
| DL11 | Populated 37-store A fixture including seven Sync stores; terminal wipe, close/reopen and B bind; prove owner-linked A data/authority retired; separately classify permitted opaque device ID. |
| DL12 | Real public HTTPS deletion page and app Settings against exact NORMAL/native build; link, email intake, identity proof, state tracking and actual backend receipts, not source text alone. |
| DL13 | VoiceOver/TalkBack/keyboard/zoom and failure/restart: pending, UNKNOWN, recoverable and completed states are truthful and actionable, no focus trap. |
| DL14 | Safari tab, Home Screen PWA and MDM Web Clip with exact OS/policy: measure independent storage containers; never treat server completion as remote wipe of offline device. |
| DL15 | Real Firebase/provider port and remote data erasure with current deployment/IAM: verify correct UID, idempotency, current authority and late-writer rejection. |
| DL16 | Regression enforcement: deliberate phase-skip, stuck-state, terminal-B and Sync-survivor mutants must fail the exact required CI job; manual workflow PASS is not automatic release gate. |

**Evidence contract:** SOURCE → independent oracle → exact executable target → fault/prestate → observed result → verdict → limits. A source-text check, model, in-memory Sembast test, JS PWA, native app, physical iPad and managed EFB are **nontransitive tiers**. No DL case is marked PASS here.

### E. Bounded verification and five-track transfer [VALIDATION / TRANSFER VALIDATION]

An 18-condition exact-source structural checker (2026-10-27) matched the pinned nine-phase enum, request/advance/wipe guards, coordinator branches, startup exception, SessionGate static locked screen, Settings omission, completed receipt retention, owner binding behavior and three existing tests: **18/18 predicates matched**. This is a **lexical/static audit**; no Dart compiler, runtime state machine, browser, Firebase, real account deletion or user incident was executed. In particular, the checker does not prove that any untrusted actor can call advanceAccountDeletion, nor that the normal coordinator writes retryableIncomplete.

- **E highest-value bottleneck:** deletion safety+liveness, transition authorization, terminal receipt, A→B isolation, 37-store Sync retirement, multi-device recovery and release gate.
- **A prerequisite:** browser session/IndexedDB/Service Worker/context isolation, cross-tab lifecycle, secure-context and Clear-Site-Data limits; no repeated platform primer.
- **C high dependency:** DL01–DL16 actual Dart/browser/physical-iPad, fault injection, accessibility and CI independent oracles; three existing in-memory tests are positive but insufficient.
- **B bounded consumer:** truthful, actionable account deletion/request/resume/UNKNOWN/completed and new-account journeys; Design Studio W121 and CD115 own interaction/copy expertise and still need execution.
- **D bounded consumer:** web account-deletion content parity, Play external resource, Apple native initiation dependency, minimal measurement and Marketing D9 launch-claim HOLD; no raw UID/flight data in analytics.
- **Software Engineering transfer:** owns state-machine implementation, executable tests, Firebase/provider integration, CI enforcement and exact NORMAL release artifacts; Web Manager records the admission requirement, not code changes.

**OPEN:** actual deployed account deletion or provider-revocation path, terminal-B re-entry execution, source-wide reachability of resume, 37-store semantics, runtime owner fences, iPadOS/MDM policy, external mailbox processing, privacy retention/legal exception, Store Console status, current production artifact and user outcome. **CHANGE WATCH:** future deletion enum/order changes (numeric index transitions are fragile), Firebase/FlutterFire recent-auth/provider behavior, Apple/Google policies, WebKit storage and product route changes.

**Stop check:** This bundle independently checked current eight product blobs, phase graph, coordinator, startup/UI, 37-store prior contradiction, Design Studio/Marketing/Engineering transfer and current Apple/Google/Firebase/WebKit/MDN sources; it reconciles **safety, liveness, terminal re-entry and cross-context erasure** rather than adding another micro-topic. The next high-value step requires executable product/served NORMAL evidence; further speculative T0 cases have lower value. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**
