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
