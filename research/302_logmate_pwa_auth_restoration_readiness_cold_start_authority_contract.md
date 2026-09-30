# 302 — LogMate PWA Auth Restoration Readiness & Cold-Start Authority Contract

Status: **PASS (V0 code/contract audit) / V1–V7 RUNTIME VALIDATION OPEN**
Date: 2026-10-01
Primary owner: **Track E — Web Architecture, Security & Operations**
Dependencies: **A Platform/Browser**, **C Quality/Validation**, **B UX/IA**
Predecessors: 300 connectivity/rejoin; 301 Firebase Auth/offline authority.

## Why this gate exists

Canonical LogMate code now supplies enough implementation evidence to inspect cold-start authority rather than treating Auth restoration as generic PWA theory. The production `FirebaseAuthEngine.readCurrentSession()` initializes Firebase, then snapshots `FirebaseAuth.instance.currentUser`. LogMate's startup specification separately requires unresolved Auth initialization to remain behind a quiet startup gate and never flash Welcome.

Firebase's current Web documentation warns that `currentUser` can be null while the Auth object is still initializing and recommends an Auth observer to avoid that intermediate state. FlutterFire documents that `authStateChanges()` emits an immediate current-state event after listener registration and that Web Auth state is persisted in IndexedDB.

This creates a concrete validation obligation: initialization of the Firebase app and settlement of persisted Auth restoration must not be conflated.

## SOURCE — canonical LogMate implementation

At LogMate main `d51882cf55a56a1894de8ffdf7e5162fd0f84a53`:

- `lib/auth/auth_engine.dart`: `FirebaseAuthEngine._auth` awaits `Firebase.initializeApp()` when necessary; `readCurrentSession()` then reads `(await _auth).currentUser` once and maps null to no session.
- `lib/app/session_gate.dart`: production startup composes `LocalLedgerAuthAccessService(FirebaseAuthEngine(), ...)`; startup remains unresolved until its resolver returns and renders a startup gate meanwhile.
- `test/session_gate_test.dart`: `auth initialization never flashes Welcome` proves the presentation seam when an injected startup resolver is deliberately held pending.
- `docs/specs/startup-and-auth-entry-spec.md`: “Auth initialization unresolved” routes to Startup gate and must never flash Welcome; transient Auth/network/token failure with an established unlocked owner preserves offline local access.

Existing widget tests therefore validate the pending-resolver UI invariant, but they do **not** establish that the production Firebase adapter stays pending until persisted-session restoration has settled.

## SOURCE — Firebase current contract

Primary sources checked 2026-10-01:

- https://firebase.google.com/docs/auth/web/manage-users
  - Firebase recommends observing Auth state.
  - It explicitly warns that `currentUser` may be null because Auth has not finished initializing.
- https://firebase.google.com/docs/auth/flutter/start
  - `authStateChanges()` emits immediately after listener registration and on sign-in/sign-out.
  - On Web, Auth state is persisted in IndexedDB; persistence can be configured.
- https://firebase.google.com/docs/auth/users
  - Auth listeners are notified when Auth finishes initializing and restores a previously signed-in user.

## SYNTHESIS

### R0–R7 authority sequence

- **R0** Firebase app initialization unresolved.
- **R1** Firebase Auth persisted-session restoration unresolved.
- **R2** first settled Auth observation is null.
- **R3** first settled Auth observation is UID.
- **R4** durable ledger-owner adjudication.
- **R5** local ledger-access decision.
- **R6** current remote-session acceptance.
- **R7** operation-specific remote authorization.

No state may be promoted by implication across these boundaries.

### Hard guards

- `Firebase.initializeApp() complete ≠ Auth restoration settled`.
- `currentUser == null while restoration unresolved ≠ signed out`.
- `restored UID ≠ durable ledger-owner match`.
- `ledger-owner match ≠ current remote-session acceptance`.
- `remote-session acceptance ≠ operation authorization`.
- `remote/network failure ≠ explicit sign-out`.

### Code-level contradiction / validation requirement

The current production adapter performs a one-shot `currentUser` read. Firebase documents an initialization interval in which that property can be null. Therefore the adapter does not, from static evidence alone, prove that a null observation is a **settled signed-out observation**.

This is **not** a production-bug claim. Exact FlutterFire/Web timing may make the risk unobservable in the deployed build. The correct status is:

**V0 code/contract risk confirmed / V1 reproduction OPEN.**

The existing `SessionGate` architecture already has the correct presentation seam: unresolved startup stays on `StartupGateScreen`. The implementation question is whether production Auth restoration keeps the resolver unresolved until the first settled Auth observation.

## MINTTAP DECISION

1. Preserve the quiet startup gate; do not replace it with optimistic Welcome.
2. Do not treat a one-shot early `currentUser == null` as sufficient evidence of settled sign-out until V1 resolves the FlutterFire timing contract.
3. Preserve fresh-ledger fail-closed behavior: a restored UID cannot create/bind a new ledger without the existing remote validation policy.
4. Preserve established-owner offline continuity: temporary network/token failure must not synthesize sign-out.
5. Prefer a readiness-aware Auth observation boundary if V1 reproduces or cannot exclude the early-null race; Software Engineering owns the implementation form.
6. Do not infer Safari/Home-Screen persistence durability from Firebase IndexedDB persistence; gates 298–299 remain authoritative for eviction/reprovision failure domains.

## VALIDATION — V1 deterministic fixture

The fixture must control the ordering of:

1. Firebase app initialization completion;
2. Auth restoration unresolved;
3. optional early snapshot null;
4. first settled Auth event;
5. ledger-owner read;
6. route reveal.

Minimum cases:

1. delayed restoration → matching UID;
2. delayed restoration → settled null;
3. early snapshot null → matching UID;
4. early snapshot null → settled null;
5. delayed wrong UID;
6. delayed unverified password UID;
7. delayed federated UID;
8. established unlocked matching owner + remote unavailable;
9. fresh/unbound ledger + remote unavailable;
10. explicit-sign-out lock racing restoration;
11. UID A restoration followed by UID B auth mutation;
12. Auth persistence lost while ledger remains;
13. ledger storage lost while Auth persists;
14. offline cold restart;
15. provider success followed immediately by reload;
16. retry after initialization failure.

### Critical executable invariant

For a valid persisted matching UID whose restoration is intentionally delayed:

**Welcome/Auth must not render for even one frame before the first settled Auth observation and ledger-owner adjudication.**

A settled null may route to Welcome. A matching settled UID proceeds to owner adjudication. A wrong UID fails closed.

## VALIDATION ladder

- **V0 — PASS:** canonical code + product contract + current Firebase primary-source review.
- **V1 — OPEN:** deterministic Auth-restoration timing fixture.
- **V2 — OPEN:** Flutter Web persisted-session browser automation.
- **V3 — OPEN:** physical iPad Safari tab.
- **V4 — OPEN:** physical installed Home-Screen PWA.
- **V5 — OPEN:** representative managed company iPad.
- **V6 — OPEN:** real Firebase + offline mutation/re-auth/rejoin convergence.
- **V7 — OPEN:** VoiceOver/keyboard/human startup-state validation.

Passes do not transfer upward automatically.

## TRACK TRANSFER

- **A:** owns browser/FlutterFire persistence and lifecycle mechanics consumed here.
- **B:** consumes the readiness model; it must not invent “signed out” copy while R1 is unresolved.
- **C:** owns V1–V7 evidence and the no-Welcome-flash regression.
- **D:** no acquisition/analytics event may label R1 as signed-out or count an auth funnel exit until state is settled.
- **E:** owns authority boundaries and fail-closed/fail-continuity policy.

## OPEN / DEPENDENCY

- Exact FlutterFire version/runtime restoration ordering on current LogMate Web build.
- Whether a production-adapter V1 seam requires an interface extension or a readiness-aware implementation behind the existing `AuthEngine` contract.
- Exact physical Safari/Home-Screen behavior.
- Managed-device storage/network policy.
- Sync/outbox/ACK topology needed to close 300→301→302 into end-to-end convergence.

## CHANGE WATCH

Re-check Firebase/FlutterFire Auth initialization and persistence semantics when the dependency is upgraded, when Web bootstrap changes, or when PWA hosting/auth-domain architecture changes.
