# 283 — PWA Policy-Distribution Authenticity, Partial-Fleet Convergence & Mixed-Generation Operation Adjudication

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-25  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B mixed-generation/rejoin UX; Track C destructive validation; Track D convergence diagnostics.  
Dependencies: 266–282 degradation governance, authority/currentness, anti-rollback, long-offline rejoin, assurance recovery and degraded-policy integrity.

## Problem

282 established that degraded-mode policy is consequence-bearing authority, capability grants are non-transitive, and stale policy/cache/PITR cannot be allowed to self-elect as current. The next problem is distribution: real fleets do not update atomically. Online clients, installed PWAs, long-offline iPads, server workers and compatibility paths can simultaneously carry P7, P8 and P9-era runtime state.

Central rule: **policy delivery is not policy authority; mixed-generation clients may coexist while authoritative boundaries adjudicate material effects under current policy, and convergence closes when predecessor generations can no longer create obsolete material consequences—not when every client has received identical bytes.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns Service Worker/client lifecycle, HTTP/browser cache behavior, update delivery and late-client persistence mechanics.
- **B UX/IA/Content:** elevated dependency pressure. Owns truthful distinctions among locally saved, policy update required, queued for revalidation, rejected/conflict and remotely confirmed states.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1016 → 1024 defined cases**. Execution, physical-device, AT and representative-human validation remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Measures observed generation spread, predecessor attempts/rejections, rejoin latency and contradiction; telemetry cannot elect current policy.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns policy lineage/currentness, authoritative mixed-generation adjudication, predecessor retirement and convergence closure.

## SOURCE

### RFC 9111 — HTTP freshness/revalidation is cache semantics, not organizational policy authority

RFC 9111 requires a cache to satisfy defined reuse conditions; stale responses subject to `must-revalidate` cannot be reused until successful validation. It also explicitly separates cache freshness from user-agent history/display behavior.

Source:
- https://www.rfc-editor.org/rfc/rfc9111.html

**TRANSFER VALIDATION:** HTTP validators, freshness and `must-revalidate` can help distribute policy representations safely, but HTTP freshness does not establish organizational policy lineage or consequence authority. A response can be HTTP-fresh while its policy generation is obsolete under an out-of-band security transition.

### W3C Service Workers — runtime update/control is not fleet simultaneity

Service Worker registrations and active workers have lifecycle/update/control semantics independent of individual page lifetime. Existing controlled clients and long-offline installations can therefore lag a newly deployed worker.

Source:
- https://www.w3.org/TR/service-workers/

**TRANSFER VALIDATION:** Service Worker mechanics explain delayed runtime convergence. They do not define MintTap/LogMate policy authority, and worker activation is not proof of organizational-policy convergence.

### RFC 9700 — resource servers validate privilege at the resource boundary

OAuth 2.0 Security BCP recommends restricting access-token privileges to required resources/actions and requires resource servers to reject tokens not intended for the requested resource/action.

Source:
- https://www.rfc-editor.org/rfc/rfc9700.html

**TRANSFER VALIDATION:** MintTap/LogMate is not assumed to use OAuth. The reusable principle is that possession of client-side authority material does not remove the material resource boundary's obligation to validate current applicability to the requested consequence.

## SYNTHESIS 1 — distribution plane and authority plane are separate

A CDN response, Service Worker update, push, MDM action, application bootstrap response or API payload can deliver policy material. Delivery success proves transport/distribution facts, not that the delivered policy is legitimate current authority.

Policy acceptance requires its governing lineage/currentness rules at the authoritative boundary. Conversely, a client that has not yet received P9 does not thereby gain permission to continue P8-era remote effects.

Guards:
- `policy delivered ≠ policy authorized`;
- `policy cached ≠ policy current`;
- `worker activated ≠ fleet policy converged`;
- `push received ≠ authoritative state changed`;
- `delivery failed ≠ unique local data invalid`.

## SYNTHESIS 2 — transport freshness and security-policy currentness are different clocks

HTTP cache freshness answers whether a stored representation can be reused under HTTP semantics. Security-policy currentness answers whether a generation may govern a material consequence now.

Therefore an HTTP-fresh P8 representation may still be organizationally obsolete after an emergency P9 transition. Likewise an HTTP-stale representation is not automatically malicious; it may remain useful historical evidence or local UI context while being denied authority for new remote effects.

Guards:
- `HTTP fresh ≠ policy current`;
- `HTTP stale ≠ data corrupt`;
- `ETag matches ≠ authority current`;
- `304 Not Modified ≠ organizational reauthorization`.

## SYNTHESIS 3 — mixed-generation fleet is a normal rollout condition, not automatic split-brain

P7/P8/P9 clients can coexist without creating authority split-brain if current server/material boundaries have one authoritative adjudication regime. The client generation becomes input/evidence, not a vote for which policy governs.

A split-brain problem exists when two consequence-bearing boundaries can independently accept incompatible generations as current for the same effect—not merely because two clients display different local runtime generations.

Guards:
- `mixed clients ≠ mixed authority`;
- `client P7 exists ≠ server P7 authority exists`;
- `fleet heterogeneity ≠ authorization ambiguity`;
- `two authoritative boundaries disagree ≠ harmless rollout lag`.

## SYNTHESIS 4 — material operations are adjudicated under current semantics

When a P7 client submits an operation during P9, the authoritative boundary does not simply execute the P7 allow decision. It maps the requested operation to current semantics/consequence and decides whether to reject, require revalidation/migration, translate safely, or accept under P9.

Compatibility translation cannot lower the current consequence class merely because the old client lacks a new field or uses an old operation name.

Guards:
- `old request parseable ≠ old authorization acceptable`;
- `compatibility translation succeeded ≠ current policy satisfied`;
- `client generation known ≠ consequence classification delegated`;
- `queued under P7 ≠ authorized under P9`.

## SYNTHESIS 5 — policy-generation claims from clients are untrusted hints

A client can report `policy=P9`, but a compromised or stale client can lie. Server-side authorization cannot rely on that label alone. The material boundary uses server-known current policy and whatever authenticated/current context is actually required.

Likewise, missing generation metadata should not be silently mapped to the most permissive legacy policy.

Guards:
- `client says P9 ≠ P9 enforcement proven`;
- `missing generation ≠ legacy allow`;
- `new UI ≠ new authorization semantics`.

## SYNTHESIS 6 — convergence is consequence closure, not 100% byte simultaneity

Requiring every dormant/offline client to install P9 before central policy transition can close is often impossible. A bounded closure criterion is stronger and more useful: obsolete generations cannot produce obsolete material remote effects without current admission/revalidation.

Residual offline clients can retain unique records and stale runtime material. They become late-rejoin cohorts rather than blockers to central authority closure, provided the server rejects obsolete authority and revalidates operations on return.

Guards:
- `100% observed P9 ≠ only way to close migration`;
- `99% observed P9 ≠ proof P8 powerless`;
- `zero P8 traffic ≠ no P8 client can return`;
- `P8 client can return ≠ P8 remote authority must remain`.

## SYNTHESIS 7 — predecessor retirement requires negative proof at material boundaries

P9 positive tests show the successor works. They do not prove P8 is powerless. Retirement requires representative negative evidence that P8-era policy/credentials/cached allows cannot create obsolete material effects at API, worker, admin/recovery, background and compatibility boundaries that matter.

A retired P8 representation may remain for historical verification, diagnostics or data interpretation without retaining current consequence-bearing authority.

Guards:
- `P9 works ≠ P8 retired`;
- `P8 file deleted ≠ P8 authority impossible`;
- `historical P8 retained ≠ P8 current authority retained`.

## SYNTHESIS 8 — distribution fallback must not become downgrade

If P9 distribution is temporarily unavailable, a client may need to keep local preservation functions. That does not imply it may fetch or select P8 as a more permissive remote-authority fallback.

Fallback semantics are capability-specific: preserve local work where defensible, but fail closed or require current revalidation for material remote effects.

Guards:
- `latest policy unavailable ≠ use any valid old policy`;
- `offline fallback ≠ authorization downgrade`;
- `availability pressure ≠ predecessor authority restoration`.

## SYNTHESIS 9 — policy update acknowledgement is not authority acknowledgement

A client acknowledgement that P9 bytes were downloaded, parsed or activated is useful rollout evidence but not proof that all queued operations, sessions, compatibility adapters and cached decisions now obey P9.

Convergence evidence therefore distinguishes delivery, activation/understanding, operation adjudication and predecessor rejection.

Conceptual progression:
`distributed → locally recognized → current admission established → material operations adjudicated under current policy → predecessor effects rejected`.

These are evidence states, not prescribed product enums.

## SYNTHESIS 10 — long-offline LogMate-like iPad rejoin

Consider an iPad last online under P7 while the service progressed through P8 to P9. It has an old worker, local flight records and queued operations.

Generic sequence:
1. preserve unique local records, queue and provenance;
2. treat P7/P8 runtime hints as stale evidence, not current authority;
3. establish current server admission/currentness and P9 lineage;
4. map each queued operation to current semantics/consequence;
5. migrate/revalidate operation payloads where lossless and authorized;
6. reject or hold operations that cannot satisfy P9 rather than deleting source data;
7. record remote acknowledgement/rejection distinctly from local preservation;
8. update runtime/policy representation when platform delivery permits;
9. keep server-side P7/P8 authority fenced even if the device cannot update immediately.

This is a generic model, not a claim about actual LogMate implementation.

## SYNTHESIS 11 — Track B must expose mixed-generation consequences, not version trivia

Users generally need task truth rather than raw `P7/P9` labels. Relevant states may include locally saved, waiting for connection, update/revalidation required, rejected/conflict, and remotely confirmed. Exact language and interaction design require Design Studio and representative-human/AT validation.

A stale client must not claim `synced` merely because an upload request was sent, and an update-required state must not imply unique local records were lost.

## SYNTHESIS 12 — Track D measures convergence but cannot elect current policy

Useful diagnostics include:
- observed client/runtime generation distribution;
- current-policy bootstrap success/failure;
- predecessor-generation attempts and rejection outcomes;
- queue age and late-rejoin cohort size;
- time from reconnect to current admission;
- compatibility translation/revalidation outcomes;
- predecessor negative-test coverage;
- contradiction between claimed client generation and observed enforcement behavior.

Telemetry remains incomplete for dormant/offline clients and cannot make P8 current because P8 remains common.

Guards:
- `majority generation ≠ authoritative generation`;
- `telemetry absent ≠ client absent`;
- `rollout dashboard green ≠ predecessor consequence impossible`.

## SYNTHESIS 13 — PITR/rollback can recreate distribution split-brain

A restore can revive old policy endpoints, caches, bootstrap metadata or compatibility workers even after P9 authority was established. Restore therefore requires reconciliation against a current reference outside the rolled-back state before high-consequence effects resume.

Guards:
- `restored distribution endpoint works ≠ restored policy current`;
- `backup authentic ≠ bootstrap metadata current`;
- `old CDN object valid ≠ old policy authoritative`.

## SYNTHESIS 14 — current-policy outage has a bounded degraded response

If the authoritative current-policy service is unavailable, the system should not silently infer currentness from the newest locally available policy. Depending on consequence, it may preserve local work, queue intent, expose UNKNOWN/degraded state, or fence remote effects.

Exact availability/security trade-offs remain product-specific.

Guards:
- `policy service unavailable ≠ newest cached policy authoritative`;
- `cannot prove current ≠ erase user data`;
- `cannot prove current ≠ permit high-consequence effect`.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate web/PWA work:

1. Separate policy distribution from policy authority/currentness.
2. Permit mixed client/runtime generations without permitting mixed authoritative policy for the same material effect.
3. Re-adjudicate material operations under current server-side semantics; never inherit a stale client allow decision blindly.
4. Treat client-reported generation as evidence/hint, not authorization authority.
5. Define convergence by predecessor consequence closure rather than fleet simultaneity.
6. Require successor positive proof plus predecessor negative proof before retirement closure.
7. Do not use old valid policy as an authorization fallback merely because current distribution is unavailable.
8. Preserve unique offline data and provenance while fencing obsolete remote authority.
9. Treat PITR/rollback as a policy-distribution/currentness mutation requiring reconciliation.
10. Keep production PASS OPEN until canonical implementation/device/runtime/domain evidence exists.

## DEPENDENCY / TRANSFER

- **Track A → E/C:** browser cache, Service Worker and client lifetime explain partial-fleet runtime convergence and stale representations.
- **E → B:** E defines consequence/authority states; B communicates task truth without inventing security policy.
- **E → C:** C receives mixed-generation adjudication and predecessor-retirement invariants for destructive testing.
- **E → D:** D measures observed convergence and contradictions; it cannot elect current policy.
- **Software Engineering:** implementation-level policy format, server enforcement, compatibility adapters, queue migration, fault injection and cache invalidation remain engineering validation.
- **Design Studio:** reusable interaction/accessibility treatment remains external; latest relevant commits remain portfolio work and provide no new physical-device/PWA, screen-reader or representative-human validation.

## Track C destructive additions — defined, not executed

1017. **Delivery-equals-authority theater:** client receives signed P9 bytes and server assumes P9 authority without current lineage/adjudication.
1018. **HTTP-fresh stale-policy acceptance:** HTTP-fresh P8 cache remains accepted after emergency P9 authority transition.
1019. **Mixed-client-equals-mixed-authority:** P7 client existence causes server to preserve P7 remote authorization semantics.
1020. **Client-generation self-assertion:** compromised client labels itself P9 and bypasses stale-policy checks.
1021. **Compatibility downgrade laundering:** P7 operation translates to P9 schema but keeps obsolete lower consequence class.
1022. **Fleet-percentage closure theater:** migration closes at a rollout percentage without predecessor negative proof.
1023. **PITR distribution split-brain:** restore revives P8 bootstrap/cache/worker path that again produces material effects.
1024. **Offline-iPad predecessor fallback:** P7 iPad reconnects while P9 distribution is unavailable and server authorizes P7 remote effects for availability.

Execution, physical-device, AT and representative-human PASS are not claimed.

## OPEN

Production validation remains OPEN for actual MintTap/LogMate policy representation/distribution, server enforcement points, Service Worker/cache behavior, managed-iPad/WebKit update timing, MDM, auth/session/token topology, compatibility endpoints, queue/replay/migration semantics, policy-service availability, CDN/bootstrap topology, PITR reference, consequence classes, legal/aviation/safety requirements and human/accessibility behavior.

## CHANGE WATCH

- Service Worker lifecycle/update behavior and Safari/WebKit/iOS/iPadOS implementation differences.
- HTTP caching behavior as standards evolve; HTTP freshness remains distinct from organizational-policy currentness.
- OAuth/security BCP evolution as bounded authorization precedent only.
- Actual company auth/provider/runtime architecture when canonical implementation evidence becomes available.

## Gate

**283 PASS (generic).** The Web Manager can now reason about policy distribution vs authority, mixed-generation fleet operation, current-boundary adjudication, predecessor retirement and long-offline PWA convergence without requiring fleet simultaneity or claiming product/runtime validation.

## Next high-value target

**284 — policy-transition atomicity across distributed acceptance boundaries, partial rollout failure & cross-boundary consequence consistency**: determine how API, worker, admin/recovery and compatibility boundaries avoid accepting mutually inconsistent policy generations during a staged server rollout, how to contain partial deployment failure without restoring predecessor authority globally, and what evidence proves one consequence is adjudicated consistently across all material boundaries.