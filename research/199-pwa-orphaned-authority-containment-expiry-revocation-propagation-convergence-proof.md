# 199 — PWA Orphaned-Authority Containment Expiry, Revocation Propagation & Convergence Proof

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + REGION + TOKEN + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA session and offline-state mechanics; Track B revocation/convergence state semantics; Track C destructive assurance; Track D privacy-bounded telemetry.  
Dependencies: 171–198, especially 195–198.

## Problem
198 established that material rotation, authenticator invalidation, session invalidation and effective authority extinction are separate, and that orphan discovery cannot prove absence. The next problem is distributed retirement: even after the authoritative identity or authorization system marks an old authority retired, independent relying parties (RPs), providers, resource servers, regions, authorization caches and long-offline clients may not learn or enforce that change simultaneously.

Some authority can be actively revoked; some is only checked when a server performs introspection or reauthentication; some already-issued bearer authority may remain usable until a verified expiry; some provider/RP sessions are independently managed; and some offline clients cannot receive any revocation signal until reconnect.

Central rule: **revocation requested, revocation accepted, revocation observed and revocation enforced are distinct states. Distributed extinction is therefore a convergence claim over explicit consequential enforcement surfaces, not a boolean inferred from one successful API call.**

## Five-track balance
- **A Platform/Browser:** supplies browser session/cookie/SW/offline mechanics and the fact that an offline PWA cannot receive a server-side revocation event while disconnected. It does not decide server authorization.
- **B UX/IA/Content:** owns operator-facing semantics such as `REVOCATION REQUESTED`, `PROPAGATING`, `BOUNDED UNTIL`, `CONVERGED FOR SCOPED ACTIONS`, and `UNKNOWN`; reusable interaction evidence remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns distributed negative probes, expiry-boundary tests, cache/region fault injection and offline-client rejoin cases. Physical Safari/iPadOS, AT and human execution remain OPEN.
- **D Search/Discovery/Analytics:** consumes coarse propagation/incident metrics only. Analytics is neither a revocation bus nor an authorization oracle.
- **E Architecture/Security/Operations:** **highest-risk owner**; owns retirement floors, propagation graph, enforcement-surface coverage, bounded residual windows and convergence evidence.

## SOURCE

### RFC 7009 — OAuth 2.0 Token Revocation
RFC 7009 defines a revocation endpoint and explicitly permits implementation differences in cascading revocation. Revoking a refresh token may cause related access tokens and the underlying authorization grant to be invalidated; if access-token revocation is not supported, an already-issued access token may remain valid until its own expiry.

Source: https://www.rfc-editor.org/rfc/rfc7009.html

**TRANSFER VALIDATION:** a successful revocation request does not generically prove immediate extinction of every derived token. Exact cascading semantics must be verified for the selected provider/architecture.

### RFC 9700 / BCP 240 — OAuth 2.0 Security Best Current Practice
RFC 9700 (January 2025) requires public-client refresh tokens to be sender-constrained or use refresh-token rotation, recommends restricted token privileges/audiences, and explains how rotation can detect refresh-token replay and revoke the active refresh token family. It also supports short access-token lifetimes as a way to reduce exposure.

Source: https://www.rfc-editor.org/rfc/rfc9700.html

**TRANSFER VALIDATION:** refresh-token family invalidation and short-lived access authority are useful containment mechanisms, not proof that MintTap uses OAuth or any specific lifetime/rotation policy.

### RFC 7662 — OAuth 2.0 Token Introspection
RFC 7662 allows a protected resource to query whether a token is currently active. It explicitly warns that caching introspection responses trades lower load for less-current security information; a revoked token can remain usable at a resource server while that server relies on a stale cached `active` response.

Source: https://www.rfc-editor.org/rfc/rfc7662.html

**TRANSFER VALIDATION:** even centralized revocation state can be undermined by downstream cache freshness. `authoritative inactive ≠ every resource server currently enforcing inactive`.

### NIST SP 800-63B-4 — independent IdP/RP sessions
The current final NIST authentication/session baseline distinguishes authenticator lifecycle from sessions and states that, in federation, IdP and RP sessions are independently managed. Ending one does not generically end the other.

Sources:
- https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- https://pages.nist.gov/800-63-4/sp800-63b/session/

### OpenID Connect logout specifications — explicit propagation mechanisms exist but must be implemented/tested
The OpenID Foundation approved RP-Initiated Logout, Session Management, Front-Channel Logout and Back-Channel Logout as Final Specifications in 2022; Back-Channel Logout later received approved errata. Current conformance testing treats RP-initiated logout and the OP→RP logout mechanisms as distinct profiles.

Sources:
- https://openid.net/the-openid-connect-logout-specifications-are-now-final-specifications/
- https://openid.net/certification/connect_rp_logout_testing/
- https://openid.net/specs/openid-connect-backchannel-1_0.html

**TRANSFER VALIDATION:** protocol support provides a propagation mechanism, not evidence that a selected IdP/RP/provider actually implements it correctly or that every consequential RP participates.

## SYNTHESIS 1 — use a revocation propagation graph
Model retirement as a graph beginning at the authoritative retirement decision and ending at each consequence-bearing enforcement surface.

Representative nodes/edges:
1. personnel/custody decision → authoritative identity/role state;
2. identity state → authenticator binding state;
3. authorization grant → refresh-token/token-family state;
4. authorization server → access-token/introspection state;
5. IdP → each RP session/logout state;
6. provider organization → provider-local session/recovery state;
7. policy/currentness generation → regional enforcement floor;
8. central authorization → resource-server/introspection cache;
9. server currentness → reconnecting PWA/session/queue admission;
10. retirement floor → backup/PITR reconciliation.

A propagation edge is not assumed merely because two nodes are owned by the same vendor.

Persistent guards:
- `revocation request accepted ≠ revocation enforced everywhere`;
- `authoritative inactive ≠ every resource server currently enforcing inactive`;
- `refresh token revoked ≠ already-issued access token immediately unusable`;
- `IdP logout ≠ RP logout`;
- `logout protocol supported ≠ every RP participated successfully`;
- `region configuration updated ≠ region authorization cache converged`;
- `central retirement floor advanced ≠ long-offline PWA has observed it`.

## SYNTHESIS 2 — distinguish hard revocation from bounded expiry
Authority retirement falls into at least three generic classes.

### A. Actively revocable
The verifier/resource server can consult or receive current state and reject the authority before nominal expiry. Strong evidence includes current introspection, server-side session invalidation, token-family invalidation, logout propagation or current policy-floor rejection.

### B. Non-revocable but bounded
An already-issued credential/token cannot be forcibly invalidated at every enforcement point, but verified protocol/provider semantics give it a finite maximum residual lifetime. This is **not** immediate extinction. Record `BOUNDED UNTIL <verified boundary>` and treat the affected consequence-bearing actions according to risk until the boundary has passed and negative probes succeed.

### C. Unknown/unbounded
The team cannot verify whether a surviving path can still authorize or cannot establish a trustworthy upper bound. Keep it `UNKNOWN`; containment must be based on the maximum consequence of that path, not optimistic assumptions.

Persistent guard: **`short-lived ≠ revoked`; `expired by local clock ≠ server-side expiry proven`; `bounded residual authority ≠ zero residual authority`.**

## SYNTHESIS 3 — convergence proof is scoped coverage, not proof of universal absence
A defensible convergence claim should state:
- **retirement generation/floor** being enforced;
- **scope of actions/resources** protected;
- **enumerated consequential enforcement surfaces**;
- **positive current-authority oracle** where availability matters;
- **negative retired-authority oracle** at each tested surface;
- **residual bounded authorities** and their verified expiry;
- **unresolved UNKNOWN surfaces**;
- **test time/currentness evidence**;
- **PITR/region/offline-client reconciliation state**.

A useful status vocabulary is:
- `REQUESTED` — authoritative retirement requested;
- `ACCEPTED` — authority system accepted transition;
- `PROPAGATING` — downstream enforcement is not yet fully evidenced;
- `BOUNDED` — residual authority exists only until a verified upper bound;
- `CONVERGED (SCOPED)` — every enumerated consequential surface for the stated scope either negatively rejects retired authority or has passed its verified residual-expiry boundary and then rejects it;
- `UNKNOWN` — consequential surface cannot yet be bounded/tested.

`CONVERGED (SCOPED)` must never be reported as proof that no hidden authority copy exists.

## SYNTHESIS 4 — revocation freshness has a performance/security trade-off
RFC 7662 makes the cache trade-off explicit: caching authorization state can improve performance but extend stale authorization. Therefore revocation SLOs cannot be defined independently of:
- introspection/cache TTL;
- access-token lifetime;
- RP session lifetime and logout propagation;
- provider-local session behavior;
- regional policy/cache refresh;
- offline-client reconnect behavior;
- failure-mode retry/backoff.

**MINTTAP DIRECTION:** when a consequence-bearing action depends on rapid personnel/emergency-authority retirement, do not choose cache/session/token lifetimes solely for performance or UX. Exact targets remain OPEN pending threat model and provider/runtime evidence.

## SYNTHESIS 5 — logout and revocation are multi-protocol, multi-surface operations
OpenID logout mechanisms show why `logout` is not one universal primitive. RP-Initiated Logout requests logout at the OP; front-channel/back-channel/session-management mechanisms communicate OP-side logout state to RPs in different ways. An architecture may implement only some mechanisms, and a provider-local/admin session may sit outside that federation path entirely.

Therefore a personnel/emergency-authority retirement runbook must identify which surfaces use:
- IdP session termination;
- RP-local session invalidation;
- OP→RP logout propagation;
- OAuth token-family revocation;
- provider-specific console/session invalidation;
- policy/currentness-floor advancement;
- expiry-only containment.

Do not label one provider's `global logout` control as universal without verified semantics.

## SYNTHESIS 6 — region convergence requires independent enforcement evidence
A central policy write is insufficient when regions/resource servers can cache authorization state.

Generic evidence pattern:
1. record admitted retirement generation `R`;
2. obtain region/resource-server observed generation or equivalent evidence where architecture exposes it;
3. run negative retired-authority probes against representative consequence-bearing paths per independent enforcement domain;
4. run positive successor/current-authority probes to distinguish security convergence from total outage;
5. inject or simulate a stale region/cache in non-production or bounded test context and verify fail-safe behavior;
6. reconcile restored/PITR regions against `R` before reopening consequence-bearing operations.

`all probes reject` alone can be an outage. Pair negative retirement oracles with positive current-authority oracles.

## SYNTHESIS 7 — long-offline PWA clients are expected propagation gaps, not exceptions to the floor
A disconnected PWA cannot receive revocation/logout/policy updates while offline. Local UI/session state can therefore be stale by design.

For the LogMate-like company-iPad/EFB scenario, on reconnect after retirement floor `R` advanced:
1. preserve unique local flight/logbook records before destructive auth cleanup;
2. quarantine cached identity/session/custody state from current authorization decisions;
3. obtain authenticated current server policy/security/retirement generation;
4. require server evaluation/rebootstrap of retained session/token under current rules;
5. separate acknowledged history from local-only records;
6. re-admit queued consequence-bearing work under current authority;
7. reject retired personnel authority even if local cached state looks valid;
8. only then retire obsolete local auth artifacts, without erasing unique domain data.

**MINTTAP DIRECTION:** offline utility is allowed to outlive authorization freshness; remote mutation authority is not. A long-offline iPad must not force the server retirement floor backward.

## SYNTHESIS 8 — containment expiry needs an explicit exit ceremony
When residual authority is `BOUNDED`, normal operation should not silently resume because wall-clock time appears to have passed.

Generic exit evidence:
- verified server/provider expiry semantics;
- trusted time/currentness source appropriate to the architecture;
- expiry boundary passed;
- refresh/reissue path already revoked or inaccessible;
- post-boundary negative probes at consequential enforcement surfaces;
- positive current-authority probes;
- no stale region/PITR state reopened before reconciliation;
- incident/custody record transitions `BOUNDED` → `CONVERGED (SCOPED)` or remains `UNKNOWN`.

Client-local clocks, analytics silence or lack of observed misuse are not sufficient expiry evidence.

## SYNTHESIS 9 — observability is evidence, not authority
Useful operational measurements can include propagation latency by enforcement domain, percentage of enumerated regions/RPs with current floor, failed retired-authority probes, residual-bound count and reconnecting stale-client count.

But telemetry can lag, drop, duplicate or be privacy-sensitive. It must not decide whether an operation is authorized. Track D consumes minimized status/outcome data and does not create a personnel behavior dossier.

Persistent guard: `no retired-authority event observed ≠ retired authority unusable`.

## Track C destructive campaign — 352 cases total
Add eight high-value cases to the 344-case campaign:
1. refresh token is revoked but a previously issued access token remains accepted until verified expiry;
2. authorization server marks token inactive while one resource server accepts a cached `active=true` introspection result;
3. IdP session ends but an RP-local session remains effective because logout propagation is absent/fails;
4. back-channel logout reaches two RPs but a third consequential RP is omitted and remains usable;
5. central retirement floor advances while one region retains a stale authorization cache and accepts retired authority;
6. a token is labeled `BOUNDED UNTIL T`; after T, a hidden refresh/reissue path mints fresh authority, proving the bound was false;
7. PITR restores a pre-retirement policy/session state after apparent convergence; reconciliation must block consequence-bearing admission;
8. long-offline iPad reconnects after retirement floor advancement with unique unsynced data and stale session; unique data survives, stale authority is rejected, and local-only work requires current re-admission.

Campaign status: **DEFINED, NOT EXECUTED**. Provider/IAM, physical iPad/Safari/Home Screen, AT, representative-human and canonical product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks
### A → E
Browser/PWA mechanics explain why disconnected clients can retain stale session observations. **CONTRADICTION:** local storage/session age cannot establish server-side revocation or currentness.

### E → B
B must communicate propagation uncertainty without implying compromise or guaranteed completion. `Bounded until` must identify that it is a security validity bound, not a promise that sync/recovery will finish then.

### E → C
C must pair negative retired-authority probes with positive current-authority probes and test cache/region/PITR/offline-client paths. One logout test is insufficient.

### E → D
D may measure propagation latency and coverage, but analytics/log delivery is not the retirement enforcement plane.

### Software Engineering dependency
Implementation validation requires actual IdP/RP/provider/token/session architecture, cache semantics, regional policy propagation, token expiry/revocation APIs, PITR reconciliation and fault-injection harnesses. Software Engineering Studio remains Foundation-stage; bounded Android/Chromium evidence does not transfer to iOS/Safari/EFB or product authorization.

### Design Studio dependency
Design Studio Web remains Stage 3 PRACTICE / NOT PASSED. Reusable interaction evidence for forced reauthentication, bounded-retirement states, unique-local-data preservation and queue re-admission remains execution/physical-device/human validation work there.

## OPEN
- actual MintTap/LogMate identity/federation/provider topology;
- whether OAuth/OIDC is used at all;
- actual access/refresh token lifetimes and revocation/cascade semantics;
- actual RP/provider-local session inventory and logout support;
- actual introspection or authorization-cache TTLs;
- actual regional enforcement domains and propagation behavior;
- actual managed-iPad/WebKit offline session/storage behavior;
- actual high-consequence action classification and acceptable residual validity;
- actual PITR/backup reconciliation of identity/authorization state;
- actual personnel/legal/privacy retention requirements.

## CHANGE WATCH
- OAuth/OIDC provider implementations and global-sign-out/revocation semantics are provider-specific and must be reverified at selection/change time.
- OpenID Connect Back-Channel Logout has approved errata; use the current specification text when implementing/testing.
- WebKit/iPadOS PWA session/storage/background behavior remains platform-sensitive.
- Browser privacy changes can affect front-channel/session-management mechanisms; implementation support must be validated rather than inferred from protocol existence.

## Gate judgment
**PASS (generic).** The Web Manager can now distinguish revocation request/acceptance/observation/enforcement, classify hard-revocable versus bounded-expiry versus UNKNOWN authority, model propagation across federation/provider/region/cache boundaries, define scoped convergence evidence without claiming impossible universal absence, and apply the model to long-offline PWA/EFB rejoin.

This is not production certification. Product/provider/runtime/personnel/physical-device/security/privacy/human evidence remains OPEN.

## Adjacent-value check and next highest-value work
The directly adjacent propagation problem is closed enough at the generic gate to move one layer deeper. The next highest-value target is **PWA retirement-floor admission under partial revocation-plane outage, fail-open/fail-closed boundaries & degraded-mode authorization**: determine which operations may continue when introspection/IdP/provider/currentness services are unavailable; how cached authorization differs from offline local work; how to prevent availability pressure from silently extending retired authority; and how regions/PWAs recover after the revocation plane returns.