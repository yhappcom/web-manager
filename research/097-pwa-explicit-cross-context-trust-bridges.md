# 097 — PWA Explicit Cross-Context Trust Bridges

Status: **PASS (generic) / PRODUCT BRIDGE + TARGET-DEVICE VALIDATION OPEN**  
Evidence date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: A Platform/Browser, B UX/IA/Content, C Quality/Accessibility, D Discovery/Analytics

## Why this block

096 established that separate origins can reduce DOM/storage/Service-Worker authority, but isolation can be deliberately reconnected through message, credential, redirect, link and file/export bridges. The next bottleneck is therefore not another same-origin primer: it is defining each bridge as a narrow protocol with explicit authority, schema, destination and failure semantics.

## Track allocation

- **E owns** trust-boundary design, credentials, redirects and least-authority bridge contracts.
- **A supplies** `postMessage`, origin, Fetch/CORS and navigation mechanics.
- **B consumes** bridge state as user-visible continuity/recovery requirements.
- **C consumes** negative-test, accessibility and cross-browser/device requirements.
- **D consumes** deep-link/discovery/measurement continuity without inheriting sensitive app authority.

Track E remains the highest-risk bottleneck because a broadly configured bridge can undo the isolation established by 096.

## SOURCE — cross-document messaging

WHATWG HTML defines `Window.postMessage()` as a controlled cross-document messaging mechanism. A target origin can be specified; if the target origin does not match, delivery is discarded. `*` deliberately removes that destination restriction.

MDN's current security guidance requires an exact `targetOrigin` when the receiver is known, and requires receivers to validate `event.origin` and, where useful, `event.source`; received message syntax/data must also be validated.

### SYNTHESIS

Origin validation answers **who sent this message**, not **whether this message is authorized to perform this action**. A secure bridge also needs a message schema, allowed operation set, transaction binding, replay/idempotency behavior and state preconditions.

### Guard

`postMessage origin validated ≠ message authorized ≠ payload semantically valid ≠ transaction current`.

Do not use `*` for sensitive payloads when the destination origin is knowable. Do not treat a string command from an allowed origin as authority merely because its sender passed the origin check.

## SOURCE — CORS and credentialed APIs

The WHATWG Fetch Standard separates cross-origin response sharing from credential inclusion. Credentialed cross-origin sharing requires explicit origin approval and `Access-Control-Allow-Credentials: true`; wildcard `Access-Control-Allow-Origin: *` cannot authorize a credentials-mode `include` response.

The Fetch Standard also warns that credentialed CORS requires care because of confused-deputy risk.

### SYNTHESIS

CORS is a browser response-sharing protocol, not authentication or authorization. Allowing `https://public.example` to read an API response does not prove the user or caller may perform a sensitive mutation. Server-side authorization and CSRF/session design remain independent requirements.

### Guard

`CORS allowed ≠ caller authenticated ≠ caller authorized ≠ mutation safe`.

A sensitive PWA origin should not receive a broad credentialed API surface merely to preserve public-site analytics, marketing or support continuity.

## SOURCE — auth redirects and in-browser auth messaging

RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) requires exact redirect-URI matching except the defined localhost native-app exception, rejects open redirectors, requires CSRF defenses, and requires PKCE for public clients. It also states that in-browser authorization responses using mechanisms such as `postMessage` require strict initiator/receiver verification.

RFC 10017 (OAuth 2.0 for Browser-Based Applications, August 2026) carries the same exact-redirect and in-browser communication discipline into current browser-based application guidance.

### SYNTHESIS

An authentication bridge is a transaction protocol, not a convenient navigation callback. Return destinations, authorization response, state/nonce/PKCE binding and initiating client context must not be collapsed into a generic `returnTo=` redirect.

### Guard

`user returned from identity provider ≠ response belongs to this transaction ≠ requested navigation target trusted`.

Do not build an open redirector to restore pre-login navigation. Restore only an allowlisted/internal destination or a server/client-bound opaque state representation.

## SOURCE — native app handoff and universal links

Apple documentation states that custom URL schemes are not uniquely owned: another app can register the same scheme. Apple recommends Universal Links where website association is required. Associated Domains use both an app entitlement and an `apple-app-site-association` file hosted by the domain; each subdomain is separately associated.

RFC 8252 similarly treats claimed HTTPS redirect URIs as preferable on iOS because the operating system can verify domain/app ownership, while public native clients still require PKCE.

### SYNTHESIS

A URL opening the intended app is only the first gate. The receiving app still needs to validate route, operation, identifiers and any transaction-bound state. Universal Links reduce handler-claim ambiguity; they do not make arbitrary URL parameters trustworthy application commands.

### Guards

`Universal Link association valid ≠ deep-link payload authorized`.

`custom URL scheme launches an app ≠ intended app ownership proven`.

## Support/export/file handoff

A support or export flow can bridge a sensitive PWA to email, Files, native share surfaces, another origin or a native app. The bridge should carry the minimum artifact necessary for the task.

### MINTTAP DIRECTION

For sensitive offline records, distinguish:

1. **navigation bridge** — route identifier only;
2. **identity/auth bridge** — short-lived transaction-bound authorization material;
3. **support bridge** — privacy-minimized diagnostic package, not record database dump;
4. **export/backup bridge** — explicit user-directed durable artifact with format/version/integrity metadata;
5. **sync bridge** — authenticated protocol operations with acknowledgement/reconciliation semantics;
6. **measurement bridge** — non-authoritative event/aggregate identifiers, never the authoritative outbox.

Do not reuse one bridge as another merely because both can transport JSON or a URL.

## Bridge contract template

Every cross-context bridge should explicitly declare:

- source principal/origin/app;
- destination principal/origin/app;
- allowed initiation direction;
- transport (`postMessage`, HTTPS API, redirect, Universal Link, file/share, etc.);
- credential class and scope, if any;
- exact allowed operations;
- payload schema and version;
- maximum sensitivity/data class;
- transaction binding / nonce / state where applicable;
- replay/idempotency rules;
- expiry and revocation behavior;
- navigation/focus/history effect;
- offline behavior and retry authority;
- user-visible state and recovery path;
- logging/diagnostic minimization;
- negative tests and target-device evidence.

A bridge with undefined fields remains OPEN rather than being treated as trusted plumbing.

## Failure analysis

### Broad `postMessage`
A receiver accepts any `event.origin` matching a suffix or fails to validate `source`, then treats `event.data.action` as a command. Isolation is effectively replaced with ambient cross-window authority.

### Credentialed CORS sprawl
A public/marketing origin is allowlisted for credentialed API access because it is 'ours'. A later third-party marketing script compromise can now act through that origin's granted API surface.

### Open return URL
Login accepts arbitrary `returnTo` and redirects after authentication. The trusted auth flow becomes a phishing/token-leak navigation primitive.

### Deep-link command injection
A Universal Link is correctly associated with the native app, but arbitrary query parameters trigger destructive/import/sync behavior without a second authorization/validation layer.

### Support/export overreach
A diagnostic bridge exports full local records because it is easier than defining a minimized schema. Support convenience becomes a privacy/data-loss boundary.

### Offline replay ambiguity
A bridge queues an operation while offline but does not distinguish queued, acknowledged and reconciled states. On reconnect, repeated handoff can create duplicate or stale mutation effects.

## Cross-track transfer

### Track A
Own exact browser/platform semantics. Keep `postMessage`, CORS and navigation mechanics distinct from application authorization.

### Track B
Every bridge that can be delayed, denied, expired or interrupted needs truthful state. Avoid language such as 'Synced' when the bridge only queued or handed off data.

### Track C
Negative validation must include wrong origin/source, malformed schema, replayed nonce, expired transaction, CORS denied/credential omitted, popup closed, deep-link handler absent, app not installed, offline handoff, duplicate replay, assistive-technology focus restoration and exact Safari/iPad behavior.

### Track D
Search/social/public acquisition may legitimately navigate into app/web contexts, but discovery identifiers and campaign parameters are not authorization. Analytics continuity must not cause sensitive bridge payload expansion.

## Product/EFB implications

For a LogMate-like managed-iPad PWA, no assumption is made that a PWA can silently invoke or synchronize with a native mobile app. Universal Links are navigation/app-opening mechanisms, not unattended background synchronization. `postMessage` requires simultaneously reachable browsing contexts; CORS requires network reachability; none proves background device-to-device transport.

Therefore direct unattended PWA↔native sync remains under 086/087 product feasibility and Software Engineering target-device validation.

## VALIDATION handoff

Implementation evidence should inventory every cross-context bridge and execute at least:

- exact `postMessage` sender/receiver allowlist and schema rejection;
- unauthorized command despite valid origin;
- credentialed CORS allow/deny matrix with server authorization independent of CORS;
- OAuth exact redirect, state/nonce/PKCE and open-redirect negative cases where OAuth/OIDC is used;
- Universal Link/custom-scheme routing with malformed/unauthorized payloads where native handoff exists;
- offline/interrupted/replayed bridge operations;
- support/export data-minimization review;
- keyboard/focus/AT behavior across popup/redirect/recovery states;
- Safari/Home Screen/managed-iPad execution for actual product topology.

No product PASS is inferred from generic standards evidence.

## CHANGE WATCH

- Browser-based OAuth guidance is actively current: RFC 10017 was published in August 2026.
- Safari/iOS Associated Domains and Universal Link behavior/policy require exact OS/device validation.
- Any future PWA↔native synchronization transport must be evaluated separately from navigation/deep-link capability.

## Integrated judgment

096's isolation boundary is only durable if every reconnecting bridge is narrower than the authority it crosses. The correct design question is not 'Can these contexts communicate?' but:

> What is the smallest explicit capability this source needs to invoke at this destination, with what transaction proof, payload class, lifetime and failure semantics?

That question should govern `postMessage`, CORS, auth redirects, deep links, support/export and future PWA↔native handoffs consistently.
