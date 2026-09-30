# 303 — LogMate PWA Auth Restoration V1 Fixture & Acceptance Contract

Status: **PASS (test-contract design) / V1 EXECUTION + PHYSICAL-IPAD + MANAGED-IPAD + PRODUCTION VALIDATION OPEN**  
Date: 2026-10-01  
Primary owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: **E Architecture/Security/Operations**, **A Platform/Browser**

## Why this gate exists

302 established that Firebase app initialization and Firebase Auth restoration readiness are not the same boundary. Canonical LogMate already has a quiet startup gate, but the production Auth adapter snapshot-reads FirebaseAuth.instance.currentUser. This gate defines the executable oracle for distinguishing restoration-unresolved from settled signed-out without flashing Welcome/Auth or admitting the wrong owner.

## SOURCE

Canonical LogMate main: FirebaseAuthEngine.readCurrentSession() snapshot-reads FirebaseAuth.instance.currentUser; SessionGate supports pending startup resolution; Firebase UID remains owner authority.

Firebase: Flutter authStateChanges() emits current auth state after registration and Web Auth state persists in IndexedDB (https://firebase.google.com/docs/auth/flutter/start). Firebase Web guidance warns currentUser can be null while Auth initialization is incomplete and recommends an observer for resolved state (https://firebase.google.com/docs/auth/web/manage-users).

## SYNTHESIS

The V1 oracle requires U = restoration unresolved; S0 = first settled signed-out; S1(uid) = first settled signed-in; T = post-settlement transition. A nullable user snapshot alone cannot encode U versus S0.

The fixture must independently control and record Firebase-app initialization, optional early currentUser snapshot, unresolved interval, first settled observation, later Auth transition, durable ledger-owner adjudication, remote validation, startup generation/retry identity, route reveal, and stale completion from a superseded generation. A fixed sleep is not a readiness oracle.

## HARD GUARDS

- Firebase.initializeApp complete ≠ Auth restoration settled.
- snapshot currentUser == null ≠ settled signed-out.
- fixed delay elapsed ≠ restoration settled.
- settled UID ≠ durable ledger-owner match ≠ remote authorization.
- new startup generation active ≠ old completion may mutate state.
- widget pending-resolver PASS ≠ production Firebase-adapter PASS.

## ACCEPTANCE INVARIANTS

1. With a persisted matching UID whose first settled observation is deliberately delayed, Welcome/Auth must not be exposed before settled observation plus owner adjudication.
2. A genuinely settled null must resolve to signed-out rather than hang indefinitely.
3. A UID that does not match the durable ledger owner must never unlock that ledger.
4. Once startup generation N+1 supersedes N, late completion from N must not alter route, owner, lock or session state.
5. Transient remote-validation failure for an established permitted offline owner must not be synthesized into signed-out.
6. Fresh/unbound owner establishment remains fail-closed until required authority checks pass.

## VALIDATION — V1 deterministic campaign

Test: early null→delayed matching UID; early null→settled null; early matching UID→same UID; wrong UID; unverified password UID; federated UID; Firebase initialization failure; Auth restoration failure; offline delayed restoration; established owner+remote timeout; fresh ledger+remote timeout; deleted/disabled-account rejection; UID A validation while Auth transitions to UID B; explicit sign-out race; retry N+1 with stale N completion; Auth-only persistence loss; ledger-only storage loss; provider success immediately followed by reload; rapid post-settlement transition; and accessible startup status without protected-data exposure.

All are **DEFINED / NOT EXECUTED**.

## Validation ladder

V0 source/code/contract review — **PASS**. V1 deterministic restoration-order fixture; V2 exact Flutter-Web persisted-session automation; V3 physical iPad Safari; V4 installed Home-Screen PWA; V5 representative managed company iPad; V6 real Firebase + offline mutation + reauthentication + rejoin/convergence; V7 VoiceOver/keyboard/human recovery — **OPEN**. PASS is non-transitive.

## DEPENDENCY / HANDOFF

Software Engineering owns adapter/test-seam implementation. Web Manager owns this Web/PWA behavioral contract. The minimum seam must make restoration ordering controllable; a fake that merely returns a delayed nullable Future does not prove the production boundary.

## OPEN

V1 execution; exact FlutterFire timing; physical Safari/Home-Screen/managed-iPad evidence; real provider/Firebase operational acceptance; integration with actual sync/outbox/ACK topology.

## Integrated competency

The release question is whether positive evidence shows Auth restoration settled and durable owner adjudication completed before protected state is revealed, while stale asynchronous work is prevented from changing a newer startup decision.
