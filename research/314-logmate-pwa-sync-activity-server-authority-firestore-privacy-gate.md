# 314 — LogMate PWA Sync-Activity Server Authority, Firestore Isolation & Privacy Gate

Status: **PASS (generic/platform + canonical-source contract) / production Sync implementation + Rules/IAM + runtime + deletion validation OPEN**  
Date: 2026-10-05  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A auth/browser/offline mechanics; Track C deterministic validation; Track B operational-state semantics; Track D privacy-aware measurement.

## Why this checkpoint exists

Canonical LogMate `main` froze V1 member operational metadata at `accountOperationalMeta/{uid}`. The document ID is the verified Firebase UID; the Sync backend writes with Admin/server authority; ordinary app clients are not intended to receive direct write authority; `lastSyncAt` and projection timestamps use server time. Production ledger Sync storage, receipts, cursors, ordering and bootstrap remain separate contracts.

This creates a Stage-8 boundary that cannot be closed by naming a Firestore path. Identity derivation, caller authorization, privileged server mutation, client Rules, backend IAM, event semantics, deletion and PWA offline behavior are distinct controls.

## Evidence chain

### SOURCE — Firebase Authentication server identity

Firebase's current server guidance requires a client ID token to be sent over HTTPS, verified for integrity/authenticity on the backend, and the UID to be taken from the decoded verified token. Normal `verifyIdToken()` verification does **not** by itself check revocation.

Sources:
- https://firebase.google.com/docs/auth/admin/verify-id-tokens
- https://firebase.google.com/docs/auth/admin/manage-sessions

### SOURCE — Firestore client Rules vs server authority

Firestore server client libraries bypass Cloud Firestore Security Rules and authenticate using Google Application Default Credentials/IAM. IAM is therefore an independent server-side control plane and should follow least privilege.

Sources:
- https://firebase.google.com/docs/firestore/security/rules-query
- https://firebase.google.com/docs/firestore/security/iam
- https://firebase.google.com/docs/firestore/security/test-rules-emulator

### SOURCE — deletion semantics

Deleting a Firestore document does not automatically delete documents in subcollections. Recursive/collection deletion is privileged operational work and may be partially complete if interrupted.

Sources:
- https://firebase.google.com/docs/firestore/solutions/delete-collections
- https://firebase.google.com/docs/firestore/manage-data/delete-data

## Canonical LogMate facts observed

At LogMate commit `24cc6a73e92bb58ff7e0a8947c472bc325e20b31`:
- V1 freezes `accountOperationalMeta/{uid}`;
- document ID = verified Firebase UID;
- Sync backend is the writer using Admin/server authority;
- ordinary app clients do not receive direct write authority;
- server time owns `lastSyncAt` and projection timestamps;
- ledger Sync storage/receipts/cursors/ordering/bootstrap remain separate future Sync-contract work.

Later LogMate `main` at `059d643f080781cce71f1bd00ccef659a446de8c` also preserves the rule that member-operations/onboarding server projection is future Sync metadata and **must never become local routing authority**. The future first-use product preview is confirmed in principle but deferred until real product screens can be represented truthfully.

These are source-contract facts, not proof of deployed Firebase configuration or runtime behavior.

## Integrated authority model

For a privileged metadata mutation, the required chain is:

`verified Firebase subject → operation authorization → privileged Firestore mutation`

No earlier link promotes into a later one.

Persistent guards:
- `client-supplied UID ≠ authenticated subject`;
- `valid ID token ≠ revocation policy satisfied`;
- `authenticated caller ≠ authorized Sync mutation`;
- `Firestore Rules deny client writes ≠ backend least privilege proven`;
- `Admin SDK can write ≠ caller is authorized to cause that write`;
- `server timestamp ≠ legitimate foreground Sync event`;
- `lastSyncAt advanced ≠ ledger convergence proven`.

### UID derivation

The backend must derive the subject from the verified token. A UID in path/query/body is untrusted input and must not select another user's `accountOperationalMeta` document.

### Revocation/currentness

Token signature/expiry validation and revocation policy are separate. The production Sync contract must explicitly decide which operations require revocation-aware/current-session checking and test that decision. This study does not invent that policy.

### Rules and IAM

The intended ordinary-client direct-write denial must be tested through Firestore Rules. Server-side access must separately be bounded by IAM/service identity. A broad Admin credential must not be treated as evidence that application-level caller authorization exists.

## PWA / EFB event semantics

Canonical LogMate semantics treat operational activity as successful authenticated **foreground Sync contact**, not generic app activity.

Therefore:
- offline local use can be real product activity while remote `lastSyncAt` remains old;
- network restoration is not foreground Sync;
- a Service Worker/background retry is not automatically activity evidence;
- failed or unauthenticated contact must not advance successful-Sync metadata;
- zero-delta qualifying foreground Sync may advance operational recency without proving ledger mutation or convergence.

For a company iPad/EFB this is essential: lack of remote activity evidence must not be converted into lack of local use, local data loss, or loss of offline routing authority.

## Onboarding projection boundary

The server onboarding projection is operational/support metadata. Canonical local onboarding state remains product/routing authority.

Guards:
- `remote onboarding projection ≠ local onboarding authority`;
- `remote projection missing/stale ≠ local onboarding incomplete`;
- backup/PITR or server rollback of the projection must not roll back a valid local completion state;
- future product-preview onboarding must not introduce a network dependency that breaks established offline local routing.

The latest LogMate decision to defer the product preview is compatible with this gate: truthful real-screen representation is preferred over placeholder/synthetic tutorial state.

## Track transfers

### Track A
Own token transport/browser session/offline mechanics. Do not infer that cached identity or restored connectivity authorizes privileged remote mutation.

### Track B
Operational UI should say **Last sync** / **Recent activity (sync)**, not promote the field to **Last active**. `never synced` is a valid state. Local-saved, queued, failed, remotely-contacted and converged states remain distinguishable.

### Track C
Production acceptance must exercise identity substitution, token failures/currentness, client Rules denial, backend IAM, timestamp semantics, replay/idempotency, offline/reconnect and deletion. Emulator Rules PASS does not prove deployed Rules/IAM.

### Track D
`accountOperationalMeta/{uid}` is user-associated operational metadata, not anonymous analytics. Firebase Auth `lastSignInTime`, analytics events and Sync activity are separate evidence streams. Telemetry observes; it does not elect authority.

## Deterministic validation bundle

Minimum cases before product PASS:

1. no token → privileged mutation denied;
2. malformed token → denied;
3. expired token → denied;
4. valid token for user A + body/path UID B → cannot mutate B;
5. revocation behavior matches explicit production policy;
6. ordinary Web client direct write to `accountOperationalMeta` → denied;
7. ordinary native client direct write → denied;
8. authorized Sync backend identity → only intended mutation succeeds;
9. unrelated server/service identity → denied where least-privilege design requires;
10. client clock spoof → server-owned timestamps unaffected;
11. qualifying zero-delta foreground Sync → allowed metadata advancement;
12. failed Sync → no successful-Sync advancement;
13. unauthenticated Sync → no advancement;
14. background/Service-Worker retry → no foreground-activity promotion;
15. duplicate/replay → deterministic, non-inflating semantics;
16. stale/missing remote onboarding projection → local routing remains governed locally;
17. offline PWA use then reconnect → no false historical activity reconstruction;
18. account deletion → configured user-associated metadata is actually erased and deletion completion is verified.

If subcollections or secondary user-associated stores are later introduced, deletion inventory must expand; parent-document deletion is insufficient evidence.

## MINTTAP DECISION

Treat `accountOperationalMeta/{uid}` as an operational projection written by an authenticated/authorized server boundary, not as product authority, analytics authority, or Sync-convergence authority.

Do not implement a second heartbeat/presence writer merely to manufacture activity. Consume the current LogMate foreground-Sync semantics unless canonical product requirements change.

## OPEN / VALIDATION

Still OPEN:
- actual production Sync backend implementation;
- deployed token/revocation policy;
- deployed Firestore Rules and emulator/deployed parity;
- backend IAM/service-account scope;
- ledger Sync ACK/cursor/order/reconciliation contract;
- replay/idempotency implementation;
- deployed deletion workflow and completion evidence;
- PWA Safari/Home-Screen/physical/managed-iPad runtime behavior;
- privacy/legal retention obligations.

## Gate result

**PASS** for generic platform reasoning and canonical-source contract integration.  
**NO production PASS.** A frozen path and documented authority model are not runtime evidence.
