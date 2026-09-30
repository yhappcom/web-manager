# 300 — PWA Connectivity Evidence, Offline Admission & Rejoin UX Contract

Status: **PASS (generic research/model) / PRODUCT + RUNTIME + PHYSICAL-IPAD + MANAGED-IPAD + AT VALIDATION OPEN**  
Date: 2026-09-30  
Primary owner: **Track B — Web UX, IA & Content Architecture**  
Dependencies: **A Platform/Browser**, **E Architecture/Security/Operations**  
Validation owner: **Track C — Performance, Accessibility & Quality**  
Consumer: **D Search/Discovery/Analytics** for observation only

## Why this gate exists

299 separated managed-iPad provisioning, launch, state lifetime and recovery. The next bottleneck is what the product is allowed to tell a user when connectivity changes.

For an offline-capable EFB/LogMate-like PWA, a device can regain Wi-Fi while DNS, TLS, a managed VPN, the API, authentication, authorization or acknowledgement remains unavailable. Conversely, a remote operation can commit while the client loses the acknowledgement. A binary online/offline label therefore cannot safely represent synchronization authority or convergence.

This gate defines an evidence ladder for reconnect, a bounded UX state model, and deterministic validation cases. It does not assert any MintTap or LogMate production endpoint, auth mechanism, outbox schema, MDM network policy or server acknowledgement protocol.

## SOURCE

### WHATWG HTML — browser online state

The HTML Standard states that `navigator.onLine` returns false when the user agent is definitely offline and true when it might be online. It explicitly calls the attribute inherently unreliable because a computer can be connected to a network without Internet access.

Source: https://html.spec.whatwg.org/multipage/system-state.html#navigator.online

### Apple deployment — Web Clip and managed Safari boundary

Apple documents that managed Web Clips can be delivered to iPhone, iPad and Shared iPad, may be full-screen, and interact with Safari management policy. If Safari is hidden and restricted, a Web Clip must use full-screen mode; Apple also notes that device-management vendors implement settings differently.

Source: https://support.apple.com/guide/deployment/depbc7c7808/web

Apple's supervised-device restrictions further state that disabling Safari prevents users from opening Web Clips. Launch availability is therefore policy-dependent and separate from network/API reachability.

Source: https://support.apple.com/guide/deployment/dep6b5ae23e9/web

### W3C WCAG 2.2 — status messages

WCAG 2.2 Success Criterion 4.1.3 requires status messages that meet its definition to be programmatically determinable through role or properties so assistive technologies can present them without receiving focus. Reconnect, queued-work, success and failure feedback must therefore be evaluated as semantic status, not only visual decoration.

Source: https://www.w3.org/TR/WCAG22/#status-messages

## SYNTHESIS

### 1. Connectivity is evidence, not authority

Use an explicit ladder:

- **N0 — browser/network hint:** `navigator.onLine`, online/offline event, interface state;
- **N1 — route candidate:** a plausible network path exists;
- **N2 — origin reachability:** the required origin responds through the current path;
- **N3 — transport/trust acceptance:** DNS/TLS/certificate/proxy/trust path succeeds;
- **N4 — required service reachability:** the actual API/service needed by the operation responds;
- **N5 — identity/session acceptance:** current credentials/session are accepted;
- **N6 — operation authorization:** the specific operation is permitted under current policy/semantics;
- **N7 — correlated remote acknowledgement:** the client can correlate a durable remote consequence with the stable operation identity;
- **N8 — semantic convergence:** local/remote projections and conflict/rejection state are reconciled to the product's defined invariant.

A PASS at one level does not promote the next level.

### 2. Rejoin is a protocol, not an event

An `online` event can justify attempting work. It cannot justify declaring work synchronized.

A safe conceptual rejoin sequence is:

1. preserve unique local work and provenance;
2. observe a candidate network transition;
3. establish required endpoint/trust reachability;
4. establish current identity/session acceptance;
5. re-adjudicate queued operations under current authorization and schema/policy semantics;
6. execute with stable operation identity/idempotency rules where the product protocol supports them;
7. correlate acknowledgement or explicitly retain UNKNOWN after ambiguous failure;
8. resolve conflict/rejection without silently discarding unique work;
9. establish the product's convergence invariant;
10. only then promote user-visible remote-confirmation state.

### 3. ACK loss is not remote failure

If a server commits and the acknowledgement is lost, retry can create duplication unless the actual protocol has stable operation identity and deduplication/idempotency semantics.

Therefore:

`ACK missing ≠ commit missing`

and

`retry attempted ≠ retry safe`.

The actual LogMate/MintTap protocol remains OPEN.

### 4. Managed network state is multidimensional

A company iPad may have Wi-Fi while a captive portal, DNS failure, TLS interception, VPN policy, content filter, proxy or destination allowlist blocks only part of the path.

A cached PWA shell can also open while the sync API is unreachable. Shell availability must not be presented as remote service availability.

### 5. UX states must map to evidence

Minimum semantic states for product design consideration:

- **local durable** — the product has evidence the local operation was durably admitted under its local contract;
- **waiting to sync** — unique work is retained but N7/N8 are not established;
- **syncing** — a current synchronization attempt is in progress; not a success state;
- **remotely confirmed** — the product's required acknowledgement/convergence evidence is established;
- **needs attention** — a conflict, rejection, reauthentication or recovery action requires user intervention;
- **unknown** — evidence is insufficient to classify safely.

These are semantic requirements, not final UI copy. Design Studio owns reusable visual/interaction treatment.

### 6. Accessibility is part of correctness

Meaningful asynchronous changes such as a queued operation becoming confirmed, a sync attempt failing, or a recovery action becoming required can be status messages. They must not rely only on color, a tiny network glyph or animation.

At the same time, rapid connectivity flapping must not create an unusable stream of repeated assistive-technology announcements. Exact ARIA/live-region strategy requires implementation and AT validation; this study does not prescribe one universal pattern.

## MINTTAP DECISION

For PWA work, especially EFB/LogMate-like offline use:

1. Treat `navigator.onLine` and online/offline events as hints only.
2. Never promote queued work to synchronized solely because Wi-Fi or an online event returned.
3. Keep local durability, queue admission, current authorization, acknowledgement and convergence as separate states.
4. Preserve UNKNOWN when evidence is missing rather than converting missing telemetry into success or failure.
5. Require operation-correlated evidence before user-visible remote confirmation.
6. Treat managed VPN/proxy/filter/trust configuration as part of the representative-device validation envelope.
7. Keep final status copy and visual treatment with product/Design Studio; Web Manager owns the evidence semantics.
8. Production validation remains OPEN until actual endpoint/auth/outbox/ACK topology exists.

## HARD GUARDS

- `Wi-Fi connected ≠ Internet reachable`
- `navigator.onLine === true ≠ API reachable`
- `online event ≠ synchronization complete`
- `cached shell available ≠ backend available`
- `origin reachable ≠ required API reachable`
- `API reachable ≠ authenticated`
- `authenticated ≠ operation authorized`
- `request sent ≠ remote commit`
- `ACK missing ≠ commit missing`
- `retry started ≠ retry safe`
- `local save ≠ queued ≠ remotely confirmed ≠ converged`
- `telemetry missing ≠ normal`
- `visible green indicator ≠ accessible status communication`
- `unmanaged network PASS ≠ managed VPN/filter PASS`
- `automation PASS ≠ physical Safari/iPad PASS`

## DEPENDENCY / TRANSFER

**Track A** owns browser/network mechanics and the limits of browser connectivity signals.  
**Track E** owns trust, endpoint, authentication/authorization, replay/acknowledgement and operational policy boundaries.  
**Track B** owns user-facing state semantics and recovery/task continuity requirements.  
**Track C** owns deterministic failure injection, cross-browser/device evidence and accessibility validation.  
**Track D** may measure transitions and outcomes but analytics is observation, not an authorization or convergence oracle.  
**Design Studio** owns final visual/interaction patterns.  
**Software Engineering** must supply actual endpoint, durable-store, outbox, operation-ID, auth/session, acknowledgement and reconciliation facts before product PASS.

## VALIDATION — deterministic campaign

At minimum test:

1. `navigator.onLine=true` with no Internet.
2. Captive portal while browser reports online.
3. Cached shell loads while API is unreachable.
4. CDN/static origin reachable while API origin fails.
5. API reachable while auth endpoint fails.
6. DNS failure after local commit.
7. TLS/certificate/trust failure.
8. Managed VPN permits shell but blocks sync API.
9. Managed filter permits API but blocks auth dependency.
10. Local durable commit immediately followed by process termination.
11. Server commit followed by acknowledgement loss.
12. Retry after ambiguous acknowledgement with stable operation identity.
13. Retry without proven deduplication/idempotency.
14. Session expires while offline, then network returns.
15. Credential is revoked while queued work exists.
16. Queued operation was valid when created but current policy rejects it.
17. Client schema/runtime generation changes before rejoin.
18. Service Worker changes while queue remains.
19. Partial queue success followed by transport failure.
20. Conflict requires user adjudication.
21. Rejection preserves unique local work and diagnostic evidence.
22. Rapid online/offline flapping.
23. Background/foreground transition during retry.
24. Telemetry is absent; verdict remains UNKNOWN.
25. Visual status changes but assistive technology receives no meaningful status.
26. Repeated flapping causes excessive AT announcements.
27. Unmanaged physical-iPad PASS incorrectly promoted to managed network.
28. Browser automation PASS incorrectly promoted to physical Safari/iPad.

All are **DEFINED / NOT EXECUTED**.

## Validation ladder

- **V0:** endpoint/evidence topology and state model.
- **V1:** deterministic local-store/outbox/network/auth/ACK-loss fixture.
- **V2:** exact Safari/WebKit/iPadOS browser/runtime evidence.
- **V3:** physical unmanaged iPad.
- **V4:** representative managed company iPad with actual MDM/VPN/proxy/filter/trust policy.
- **V5:** actual PWA↔server/native reconciliation and convergence.
- **V6:** assistive-technology and human comprehension validation of asynchronous state communication.

PASS is non-transitive.

## CHANGE WATCH

- WHATWG online/offline semantics.
- Safari/WebKit networking and Service Worker behavior.
- iPadOS managed-network/VPN/filter behavior.
- Apple Web Clip and Safari restriction behavior.
- Accessibility guidance for asynchronous status communication.
- Actual product endpoint/auth/outbox/acknowledgement architecture when it becomes canonical.

## OPEN

- Actual LogMate/MintTap endpoint topology.
- Actual auth/session and offline reauthentication behavior.
- Actual operation identity, outbox, deduplication/idempotency and acknowledgement semantics.
- Actual MDM/VPN/proxy/filter/trust configuration.
- Actual conflict/rejection/convergence semantics.
- Exact product status copy and interaction treatment.
- Physical Safari/iPad and managed-iPad execution.
- Screen-reader/AT and human comprehension evidence.

## Integrated competency

The operational question is not “is the iPad online?” It is:

> What evidence exists for this specific operation, from local durable admission through current endpoint/trust, identity, authorization, acknowledgement and semantic convergence, and what can the user safely be told at this moment?

Until that chain is demonstrated on the representative deployment class, connectivity recovery remains **evidence to attempt rejoin**, not proof that synchronization or authority has recovered.
