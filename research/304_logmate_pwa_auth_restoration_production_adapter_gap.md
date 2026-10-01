# 304 — LogMate PWA Auth Restoration Production-Adapter Gap & V1 Implementation Handoff

Status: **PASS (source/contract diagnosis) / ADAPTER IMPLEMENTATION + V1 EXECUTION + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**
Date: 2026-10-01
Primary owner: **Track E — Web Architecture, Security & Operations**
Dependencies: **A Platform/Browser**, **C Performance/Accessibility/Quality**
Consumes: **303 — LogMate PWA Auth Restoration V1 Fixture & Acceptance Contract**

## SOURCE
Canonical LogMate main defines AuthEngine.readCurrentSession() as a nullable Future snapshot. SessionGate tests prove the UI can remain pending while an injected startup resolver is unresolved, but the fake Auth engine returns an immediate nullable snapshot. Firebase Flutter documentation states authStateChanges() emits current Auth state after listener registration and Web Auth persists in IndexedDB by default. Firebase Web guidance recommends an observer to avoid reading current user during intermediate initialization. WebKit documents iOS/iPadOS 17.2 Home-Screen creation copies cookies but no other local storage and does not share website data afterward.

## SYNTHESIS
303 requires U = restoration unresolved, S0 = first settled signed-out, S1(uid) = first settled signed-in, T = post-settlement transition. A nullable snapshot can encode S0/S1 only after settlement is independently known; null alone cannot distinguish U from S0. Presentation already has a pending startup state, so the principal readiness gap is the production adapter boundary.

## CONTRADICTION
303 requires no Welcome/Auth or protected-state reveal until first-settled Firebase Auth observation plus owner adjudication. Current production interface exposes readCurrentSession() -> Future<AuthSessionSnapshot?>. Current widget evidence handles a pending resolver safely but does not reproduce FlutterFire restoration ordering.

Guard: widget pending-resolver PASS != production Firebase-adapter PASS.

This is a source-level readiness contradiction, not evidence of a production incident.

## HARD GUARDS
- Firebase.initializeApp complete != Auth restoration settled.
- currentUser == null != first settled signed-out unless settlement is independently established.
- fixed delay elapsed != restoration settled.
- first settled UID != durable ledger-owner match != fresh remote authorization.
- new startup generation active != stale prior completion may mutate route/lock/session state.
- Safari signed in != newly installed Home-Screen PWA signed in.
- cookie transfer != IndexedDB transfer.
- Auth persistence != backup or ledger-owner authority.

## MINTTAP DECISION
Do not solve restoration ambiguity with polling or arbitrary sleep. Software Engineering should expose a production seam based on Firebase Auth observer/stream semantics that represents unresolved versus first-settled state and is deterministically controllable in tests. Web Manager does not prescribe the Dart class shape.

Required behavior:
1. startup waits for first-settled Auth state before treating null as signed-out;
2. owner/ledger adjudication remains separate from Firebase identity restoration;
3. remote reload/validation remains separate from local restoration;
4. retry/generation replacement prevents stale async work mutating newer startup state;
5. later Auth transitions remain transitions rather than being reclassified as first settlement.

## VALIDATION — V1
Minimum deterministic campaign: delayed matching UID; genuine settled null; immediate matching UID; wrong UID; unverified password UID; federated UID; Firebase initialization failure; Auth observation failure; offline delayed settlement; established owner plus remote timeout; fresh ledger plus remote timeout; remotely deleted account; remotely disabled account; UID A validation while Auth changes to UID B; explicit sign-out race; retry N+1 with stale N completion; provider success then reload; Auth-only persistence loss; ledger-only loss; accessible pending/failure state without protected-data exposure.

V1 is DEFINED / NOT EXECUTED until tests exercise the production seam rather than a delayed nullable-Future substitute.

## PWA TRANSFER VALIDATION
After V1 adapter evidence, validate exact Flutter-Web persistence/reload, then physical Safari and Home-Screen installation separately. WebKit's cookie-only installation transfer means Safari login cannot be promoted into installed-PWA login evidence for default IndexedDB-backed FlutterFire Auth. Physical and managed-iPad PASS remain non-transitive.

## TRACK TRANSFERS
A owns observer/restoration/storage mechanics and Safari/Home-Screen separation. B keeps pending restoration, signed-out, owner mismatch, remote-unreachable and local-data-loss states semantically distinct. C owns deterministic V1 and physical/managed-device validation. D must not emit raw email, UID, existence labels or protected ledger details for startup diagnostics and must not assume browser/PWA session identity continuity. E owns authority separation, stale-generation containment, deployment/runtime evidence and release gate.

## OPEN
Production first-settled observer seam; deterministic V1 execution; exact Flutter-Web persisted-session automation; Safari restart/Home-Screen runtime evidence; physical and representative managed-company-iPad evidence; real Firebase offline/reauthentication/rejoin/convergence evidence.

## Integrated competency
A secure PWA startup is not established because Firebase initialized or because a nullable user snapshot was read. Release evidence must show Auth restoration reached a first-settled state, durable owner adjudication completed, stale asynchronous work cannot alter a newer decision, and protected state is not revealed before those boundaries are satisfied.
