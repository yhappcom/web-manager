# 318 — LogMate PWA Account Deletion, Authority Retirement & Recovery Anti-Rollback Gate

Status: **PASS (generic/platform + bounded canonical-source contract) / PRODUCTION + DEPLOYED-ADAPTER + RECOVERY + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-10-08  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A platform/storage/session mechanics; Track B deletion/recovery UX; Track C fault/regression/device validation; Track D privacy-minimized observability.

## Purpose

Extend 315–317's logical-operation identity, current admission authority, idempotency and replay model through account deletion, provider credential revocation, stale-device return and backup/PITR restore. The gate prevents a historically valid offline operation, restored database, old provider credential or predecessor account state from regaining mutation authority merely because bytes, identifiers or connectivity reappear.

## SOURCE

- Firebase user deletion is security-sensitive and requires recent authentication for client-side deletion. Firebase Authentication can also disable end-user account creation/deletion at project/tenant policy level; a client API existing therefore does not prove that deployed self-service deletion is permitted.  
  https://firebase.google.com/docs/auth/users  
  https://firebase.google.com/docs/auth/android/manage-users
- Firebase Admin bulk `deleteUsers()` does not fire per-user Authentication deletion events. Cleanup correctness cannot depend on such a trigger unless the actual deletion path is proven compatible.  
  https://firebase.google.com/docs/functions/1st-gen/auth-events
- Firestore managed import overwrites documents whose IDs are present in the import but leaves unaffected documents in place; imports do not trigger Cloud Functions. PITR can expose historical data from the prior seven days.  
  https://firebase.google.com/docs/firestore/manage-data/export-import
- Firestore in-place restore is implemented by deleting the database and restoring a backup under the same database ID. Firebase explicitly warns that offline-cache writes from a client connected to the deleted database can later flush into the restored database.  
  https://firebase.google.com/docs/firestore/restore-in-place
- Apple TN3194 (published 2025-10-03) separates product-account deletion from Sign in with Apple credential revocation. If revocation material is unavailable, the product deletion request must still be fulfilled; local/web-client account data must also be removed where applicable.  
  https://developer.apple.com/documentation/technotes/tn3194-handling-account-deletions-and-revoking-tokens-for-sign-in-with-apple

## SYNTHESIS — authority retirement is multi-plane

Deletion is not one API call. Treat these as independently observable planes:

1. **local mutation authority** — stop new local mutations and quarantine pending outbox work;
2. **current-subject proof** — establish that the destructive request belongs to the currently authenticated subject;
3. **provider authorization** — retire/revoke Apple/Google/provider linkage where required and possible;
4. **remote product data** — erase the complete account-owned deletion domain, subject only to explicit retention obligations;
5. **application/Firebase identity** — retire authentication identity and server admission authority;
6. **local product data** — erase or render inaccessible account-linked active local state where applicable;
7. **recovery authority** — ensure backup, PITR, import, restore or a long-offline device cannot resurrect predecessor mutation authority.

No single plane proves another completed.

Hard guards:

- `identity deleted ≠ provider authorization revoked`
- `identity absent ≠ deletion trigger emitted ≠ downstream cleanup completed`
- `client delete API exists ≠ deployed project permits client deletion`
- `historical bytes authentic ≠ currently authoritative`
- `restore/import succeeded ≠ predecessor authority restored`
- `same UID/database/document identifier ≠ same authority epoch`
- `network restored ≠ stale queued mutation reauthorized`
- `workflow exists ≠ automatic regression enforcement`

## Canonical LogMate transfer evidence

Current `main` supplies bounded evidence, not production certification.

**CONTRADICTION — public deletion path vs inspected UI.**  
`web/account-deletion/index.html` tells users to open Settings and choose an account-deletion option. Current `lib/screens/settings_screen.dart` exposes Import, Previous Total setup and Sign out, but no deletion action. This is release-content/runtime parity debt until either shipped UI or public instructions change.

**CONTRADICTION — public deletion promise vs inspected backend source.**  
The public page describes remote account/data deletion and provider-linkage retirement where applicable. Current `functions/index.js` only records retirement of an earlier account-existence lookup; it does not establish a deployed deletion backend. `firestore.rules` denies all direct client Firestore reads/writes and says operational metadata is server-owned. Do not infer an unobserved server deletion implementation.

**VALIDATION GOVERNANCE.**  
Current `.github/workflows/core-product-validation.yml` and `member-operations-validation.yml` are `workflow_dispatch` only. They are useful executable checks when run, but are not evidence that destructive-lifecycle regressions are automatically blocked on push/merge.

## Failure/UNKNOWN model

External destructive effects can succeed while the response is lost. Provider revocation, remote erasure and identity deletion therefore need either an idempotent repeat operation or authoritative reconciliation. Ordinary retry logic is insufficient when success state is UNKNOWN.

Deletion-domain inventory must include every authoritative product store, sync/backup material, account linkage, queued operation/receipt, operational metadata and explicitly retained exception. A successful identity delete cannot substitute for that inventory.

## Recovery anti-rollback

Backup/PITR/import/restore recover **data**, not automatically **authority**. Restored predecessor records require current-policy admission. A restored database using the same identifier needs a distinguishable current authority epoch/generation or equivalent server-side fencing. Long-offline clients must not be allowed to replay predecessor outbox entries merely because authentication or connectivity becomes available again.

A successor account or re-created identity must not inherit predecessor queued operations solely from reused email, provider subject, UID-like identifier or restored local state. Any legitimate migration requires explicit authenticated lineage semantics.

## Cross-track transfer

- **A:** prove browser/PWA storage, session and offline-queue mechanics; do not equate persistence with authority.
- **B:** own deletion/recovery status UX, reauthentication UX, destructive confirmation and public-instruction parity.
- **C:** run interruption, UNKNOWN, stale-device, restore/import and physical Safari/Home-Screen tests; verify regression enforcement separately.
- **D:** measure deletion/recovery funnel with minimized telemetry; deletion analytics must not recreate deleted product identity.
- **E:** owns ordering, idempotency/reconciliation, complete deletion inventory, retention exceptions, recovery fencing and incident procedure.

## VALIDATION campaign — cases 53–68

53. interrupt after local lock; restart cannot unlock predecessor outbox.  
54. reauthentication returns a different UID/subject; destructive progression stops.  
55. provider revocation succeeds but response is lost; reconciliation/retry cannot duplicate harmful effects.  
56. remote erase partially succeeds; resume converges without skipping undeleted domains.  
57. Firebase identity deletion is UNKNOWN; determine authoritative state before advancing.  
58. bulk identity deletion path bypasses per-user trigger; cleanup still completes or path is rejected.  
59. deletion inventory omits a subcollection/backup/sync store; gate fails.  
60. delayed asynchronous cleanup remains observable and bounded; completion is not claimed early.  
61. long-offline iPad returns after account retirement; stale outbox is rejected/quarantined.  
62. PITR/backup restore reintroduces predecessor bytes; current authority does not roll back.  
63. managed import overwrites matching IDs while unrelated stale data remains; deletion completeness is re-evaluated.  
64. same database ID after in-place restore does not admit old cached writes without current authorization.  
65. successor/re-created account cannot inherit predecessor queued operations by identifier reuse.  
66. final local wipe interruption resumes safely without restoring remote authority.  
67. public deletion instructions match the actually shipped initiation path, or release content is corrected.  
68. destructive-lifecycle tests have explicit execution/enforcement evidence; manual-only workflow presence is not promoted to automatic protection.

## MINTTAP DECISION

Treat account deletion as an **authority-retirement protocol**, not a single identity-delete call. Recovery mechanisms may restore historical data but must never silently restore predecessor mutation authority. Preserve logical-operation identity for reconciliation while requiring fresh/current admission proof after revocation, restore or successor creation.

## OPEN

Production remains OPEN until evidence exists for: deployed deletion/provider/remote-erasure adapters; Firebase project/tenant self-service deletion policy; complete deletion-domain inventory and retention exceptions; UNKNOWN reconciliation; public-content/shipped-UI parity; backup/PITR/import recovery fencing; successor-lineage negative proof; stale-outbox rejection; automatic or otherwise enforced destructive-lifecycle validation; exact Safari/Home-Screen behavior; and representative physical/managed-iPad validation.

## CHANGE WATCH

Firebase Authentication deletion policy, Auth trigger behavior, Firestore backup/PITR/import/restore semantics, Apple account-deletion/token-revocation requirements, Safari/WebKit PWA storage/lifecycle behavior, and LogMate validation/deletion implementation are change-sensitive and must be rechecked against current primary evidence before production release.
