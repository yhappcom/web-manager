# 292 — PWA Authentication, Session Continuity, Offline Local Capability & Rejoin Authority

Status: **PASS (generic) / PRODUCT AUTH + MANAGED-IPAD + RUNTIME EXECUTION OPEN**  
Date: 2026-09-27  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 289 queue re-adjudication; 290 U4/U5; 291 M3–M5; Track A Fetch/cookie/browser mechanics; Track C validation.

## Purpose
Define how an offline-capable PWA preserves useful local work without confusing local availability, retained credentials or network recovery with current remote authority.

Central rule: **offline usability is not authenticated remote authority.**

## SOURCE
- RFC 9700, Best Current Practice for OAuth 2.0 Security: https://www.rfc-editor.org/rfc/rfc9700
- WHATWG Fetch: https://fetch.spec.whatwg.org/
- MDN Navigator.onLine: https://developer.mozilla.org/docs/Web/API/Navigator/onLine
- W3C Web Authentication Level 3 Recommendation (2026-08-25): https://www.w3.org/TR/webauthn-3/
- OAuth/WebAuthn are bounded security precedents only. No MintTap/LogMate authentication architecture is inferred.

## History / problem
Connected applications often collapse several facts into one “logged in” state: cached UI is visible, credentials exist locally, the network appears online, the server still recognizes a session, and a requested mutation is currently authorized. Offline PWAs break that simplification. A device can preserve valuable local records while its session expires, a grant is revoked, policy changes, a proxy blocks one destination, or a server-side consequence class changes.

Destroying unique local work because remote authority is stale is unsafe; replaying it remotely merely because connectivity returned is also unsafe.

## Five-track allocation
- **A:** owns Fetch/cookie/credential transport, online hints, origin and browser session mechanics.
- **B:** owns truthful local-only, reauthentication-required, queued, rejected/conflict and remotely-confirmed states.
- **C:** owns destructive validation, physical-device and accessibility/human evidence.
- **D:** measures rejoin/session outcomes but telemetry cannot establish current authorization.
- **E:** owns session/grant currentness, operation authority, queue re-adjudication and incident/recovery semantics.

## Independent state vector
Do not compress these into one boolean:
1. **L — Local data availability:** unique records/work are present and semantically readable.
2. **H — Cached shell/runtime availability:** UI/runtime can start.
3. **I — Identity evidence:** local application has some identity/account context.
4. **S — Session/grant currentness:** server currently accepts the relevant session/grant.
5. **R — Required-destination reachability:** the specific auth/API/sync destination is reachable under current M0–M8 network/trust conditions.
6. **A — Operation authority:** current server/policy authorizes this consequence now.
7. **Q — Queue disposition:** queued work is pending, admitted, rejected, conflicted, quarantined or requires user/admin action.
8. **C — Convergence:** remote acknowledgement and semantic reconciliation are proven.

A positive state in one dimension does not imply the next.

## Rejoin adjudication pipeline
Treat browser online/offline signals as hints only:
1. detect a connectivity hint or explicit retry;
2. probe the **required destination**, not generic Internet availability;
3. establish TLS/trust and current managed-network path;
4. establish current authentication/session/grant state;
5. obtain current policy/admission context where material;
6. map each queued item to current semantics and consequence;
7. re-adjudicate authority; do not grandfather queue admission automatically;
8. perform idempotent/replay-safe submission where implementation supports it;
9. require remote acknowledgement;
10. reconcile conflicts/version changes and prove convergence;
11. preserve provenance for rejected/quarantined local work;
12. normalize temporary recovery/reauthentication state.

## Authority matrix
- **Offline + local data valid:** local read/capture/queue may remain available if product policy permits; remote authority is UNKNOWN/unavailable.
- **Online hint + endpoint unreachable:** preserve local work; do not infer logout, revocation or authorization failure from transport failure alone.
- **Endpoint reachable + session stale/expired/revoked:** require appropriate current admission/reauthentication; preserve queued work.
- **Session current + operation no longer authorized:** reject/quarantine under current semantics; a valid session is not blanket operation authority.
- **Session current + operation authorized + submission unacknowledged:** do not claim convergence; retry/reconciliation semantics are implementation-specific.
- **Remote acknowledged + conflict exists:** acknowledgement alone is not semantic convergence.
- **Converged:** only after current authority, acknowledgement and reconciliation evidence are satisfied.

## Security precedents and limits
RFC 9700 treats refresh tokens as high-value credentials and discusses replay protection, rotation/sender constraint, revocation on security events and inactivity expiration. This supports the generic guard `credential retained locally ≠ grant still current`; it does not prove that this product uses OAuth or refresh tokens.

WebAuthn Level 3 is a current W3C Recommendation for scoped public-key credentials. It is a strong-authentication precedent, not evidence that MintTap or LogMate uses WebAuthn/passkeys.

`Navigator.onLine` is heuristic and cannot establish Internet, API or authentication-endpoint reachability. Fetch credential semantics are origin/request dependent; “network works” is not proof that the authenticated request carries or is allowed to use the required credential.

## Managed-iPad composition
291 M3–M5 remains a prerequisite for representative rejoin claims. Proxy/PAC/VPN/DNS/filter or trust changes can make shell, auth and sync destinations diverge. Rejoin evidence records the exact M0–M8 envelope plus 290 D/L/S/U class.

## UX transfer
User-visible states must not promise “synced”, “signed in”, “saved to account” or equivalent based solely on local persistence or connectivity. Track B should distinguish, where product semantics require: saved locally; queued; reconnecting/checking; reauthentication required; rejected/conflict; remotely confirmed.

Accessibility/human validation remains OPEN.

## Observability
Useful telemetry may include endpoint-class reachability outcome, reauthentication required/succeeded, queue disposition, rejection reason class, acknowledgement latency and convergence latency. Do not log secrets/tokens. Telemetry is evidence of observed outcomes, not an authorization oracle and not proof of unobserved offline durability.

## Persistent guards
- `offline usable ≠ remotely authorized`;
- `cached shell available ≠ authenticated session current`;
- `identity remembered ≠ session current`;
- `credential retained ≠ grant current`;
- `navigator.onLine = true ≠ required endpoint reachable`;
- `endpoint reachable ≠ authenticated`;
- `authenticated ≠ operation authorized`;
- `queue accepted locally ≠ remote effect authorized later`;
- `network restored ≠ queued work admitted`;
- `submission sent ≠ acknowledged`;
- `acknowledged ≠ semantically converged`;
- `session expired/revoked ≠ destroy unique local work`;
- `transport failure ≠ authorization denial`;
- `valid session ≠ authorization under obsolete policy`;
- `reauthentication succeeded ≠ every queued operation may replay`.

## Track C destructive additions — defined, not executed
1089. **Online-oracle failure:** `navigator.onLine` treated as required-endpoint availability.  
1090. **Credential-currentness fallacy:** retained cookie/token/credential treated as current server authority.  
1091. **Authz composition:** successful authentication treated as authorization for every queued consequence.  
1092. **Queue grandfathering:** enqueue-time allow survives material policy/session transition without re-adjudication.  
1093. **Transport/auth collapse:** proxy/DNS/TLS/network failure classified as credential revocation or authorization denial.  
1094. **Reauth replay-all:** successful reauthentication causes unconditional replay of all queued work.  
1095. **Acknowledgement-as-convergence:** server acknowledgement treated as semantic conflict/convergence closure.  
1096. **Session-loss data destruction:** expired/revoked session triggers deletion of unique valid local work without independent retention/recovery policy.

All are **DEFINED / NOT EXECUTED**.

## VALIDATION / OPEN
Actual MintTap/LogMate authentication mechanism, cookie/token/session design, identity provider, session duration, refresh/revocation behavior, queue implementation, API consequence classes, conflict model, MDM/network envelope and physical-iPad behavior remain **OPEN**. Production validation requires canonical runtime/project evidence.

## MINTTAP DECISION / DIRECTION
Adopt the L/H/I/S/R/A/Q/C state vector and rejoin adjudication pipeline for future PWA validation. Preserve unique local work independently of remote session currentness. Next high-value work: implementation-neutral runtime probe/handoff contract for Software Engineering, including representative managed-iPad rejoin cases without selecting an auth mechanism prematurely.
