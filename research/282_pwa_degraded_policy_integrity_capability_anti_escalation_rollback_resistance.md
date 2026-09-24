# 282 — PWA Degraded-Mode Policy Integrity, Capability-Tier Anti-Escalation & Recovery-State Rollback Resistance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B degraded/recovery UX; Track C destructive validation; Track D assurance diagnostics.  
Dependencies: 266–281 exception/degradation governance, currentness, anti-rollback, assurance-plane recovery, independence budgets and graceful degradation.

## Problem

281 established that assurance loss should degrade capabilities by consequence rather than either pretending everything is `NORMAL` or destroying useful local work. That creates a new authority: the policy that decides which capability is allowed under each assurance state.

If that policy can be replaced, cached, downgraded, reclassified or composed transitively, an attacker does not need to defeat the primary authorization rule. It can instead make a high-consequence operation appear to be an allowed low-consequence operation, or resurrect an older degraded policy that was more permissive.

Central rule: **degraded operation is an authorization regime, not a UX flag. Its policy must have authenticated lineage/currentness, capability grants must be non-transitive unless explicitly re-authorized at the material boundary, and stale clients/caches/PITR must not resurrect a more permissive policy generation.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns Service Worker/client lifetime, cached resources, storage and late-client mechanics that can preserve stale policy or routing hints.
- **B UX/IA/Content:** elevated dependency pressure. Owns truthful expression of local-only, queued, revalidation-required and remotely-confirmed task states; UX must not imply a stronger authorization state than exists.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1008 → 1016 defined cases**. Execution, physical-device, AT and representative-human validation remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Measures policy-generation spread, stale-decision rejection, UNKNOWN/degraded duration and rollback attempts; telemetry cannot choose a more permissive policy.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns policy authority, consequence mapping, enforcement boundaries, anti-escalation, anti-rollback and re-entry proof.

## SOURCE

### OWASP Authorization guidance — deny by default and validate every request

OWASP Authorization Cheat Sheet guidance says an application should deny by default and validate permissions on every request. OWASP Top 10:2025 similarly states that effective access control belongs in trusted server-side/serverless enforcement where an attacker cannot modify the check or its metadata.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

**TRANSFER VALIDATION:** OWASP does not define this Web Manager's degraded-state model. The reusable principle is that client-side or cached state cannot by itself authorize a material server-side effect, and missing/unknown policy should not become implicit permission.

### Service Workers specification — registrations and active workers persist independently of page lifetime

The Service Workers specification defines persistent registrations, installation/version/update machinery and clients that can remain controlled by an active worker while lifecycle transitions occur. A registration can outlive individual `ServiceWorkerRegistration` objects and update state is distinct from page state.

Source:
- https://www.w3.org/TR/service-workers/

**TRANSFER VALIDATION:** this is platform behavior, not a security-policy protocol. It establishes why a PWA can retain stale runtime/policy hints and why server-side currentness remains necessary.

## SYNTHESIS 1 — the degradation map is consequence-bearing policy

The mapping is conceptually:

`assurance state + consequence class + principal/device/session/currentness + operation -> allowed capability / revalidation / containment`

It is not merely presentation metadata. A change from `remote publish requires current independent assurance` to `remote publish allowed while degraded` changes authority.

Therefore policy needs at minimum a distinguishable generation/lineage, provenance sufficient to identify the governing authority, explicit scope and a currentness rule. The exact representation remains implementation-specific.

Guards:
- `policy file exists ≠ policy authorized`;
- `policy signature valid ≠ policy current`;
- `newer timestamp ≠ legitimate successor`;
- `degraded mode enabled ≠ every degraded capability allowed`.

## SYNTHESIS 2 — capability tiers are non-transitive by default

A local permission must not silently compose into remote authority.

Examples:
- local record capture may create a durable local record;
- queue permission may preserve an intent for later review;
- export permission may produce a recoverable package;
- none of those facts alone authorizes remote publication, destructive mutation, account recovery or privileged synchronization.

The material boundary re-evaluates the requested consequence under current policy rather than inheriting the strongest consequence reachable from a chain of locally allowed steps.

Guards:
- `local capture allowed ≠ sync allowed`;
- `sync queued ≠ publication authorized`;
- `exportable ≠ import automatically admissible`;
- `readable ≠ mutable`;
- `operation A allowed + B allowed ≠ A→B composite allowed`.

## SYNTHESIS 3 — consequence classification cannot be caller-controlled

A client cannot safely label its own request `low consequence` and thereby select a weaker assurance rule. Consequence classification must be derived or validated at a trusted enforcement/domain boundary using current server-side semantics.

This matters during schema/API evolution. An old client may call an operation name that used to be low consequence but now maps to a stronger effect. Compatibility translation must not preserve the old risk classification blindly.

Guards:
- `client labels local-only ≠ server effect local-only`;
- `legacy operation name unchanged ≠ consequence unchanged`;
- `compatibility adapter succeeded ≠ assurance requirement preserved`.

## SYNTHESIS 4 — unknown policy generation fails closed for material remote effects, not necessarily for preservation

Deny-by-default does not require destroying or blocking all local activity. If a client cannot establish a current policy generation, high-consequence remote effects can be fenced while local preservation/capture remains available where product-specific rules permit.

This keeps two statements separate:
- the server cannot authorize a material effect from unknown/stale policy;
- the client should not discard unique user data merely because remote authorization is unavailable.

Guards:
- `policy UNKNOWN ≠ erase local data`;
- `policy UNKNOWN ≠ authorize remote effect`;
- `remote deny ≠ local save failed`.

## SYNTHESIS 5 — policy caches are derived decisions, not trust roots

A cached `NORMAL`, degraded capability matrix or prior authorization result is derived from a particular policy/currentness context. It does not become independent authority when the underlying policy changes or assurance budget is exhausted.

A cache entry therefore needs enough binding to reject use outside its valid policy/currentness context. Exact cache keys and TTLs are implementation questions; elapsed TTL alone is not a substitute for generation invalidation when a security-relevant transition occurs.

Guards:
- `cached allow ≠ current allow`;
- `TTL not expired ≠ policy still current`;
- `offline cache authentic ≠ remote authority current`.

## SYNTHESIS 6 — anti-rollback requires an authority outside the restored stale state

PITR/backup can restore an authentic but older, more permissive degraded policy and its decision cache. If the restored system decides currentness solely from restored data, it can elect the stale policy as current.

Recovery therefore needs a current reference, successor lineage or governed rebootstrap that is not simply the same rolled-back state. After restore, policy generation and consequence mapping are reconciled before high-consequence effects resume.

Guards:
- `backup authentic ≠ restored policy current`;
- `restore successful ≠ authorization state safe`;
- `old policy verifies ≠ old policy may govern new effects`.

## SYNTHESIS 7 — Service Worker update is not policy migration

A new Service Worker can distribute code that understands a new policy generation, but worker activation does not prove every controlled client has transitioned, every cache is invalidated, or the organizational policy authority is legitimate.

Likewise, an old worker may remain on a long-offline iPad. Server enforcement must not depend on that worker receiving an update before obsolete remote authority is rejected.

Guards:
- `worker updated ≠ policy migrated`;
- `worker stale ≠ user data stale`;
- `update delivered ≠ old authorization impossible`.

## SYNTHESIS 8 — recovery state must not grant a universal bypass

`RECOVERY` is not a super-role. Recovery may require narrowly scoped operations unavailable in normal mode, but those operations need explicit scope, provenance, expiry/retirement and material-boundary enforcement.

A recovery mechanism that can arbitrarily relabel consequence classes or bypass every authorization check becomes a permanent alternate control plane.

Guards:
- `recovery needed ≠ unrestricted recovery authority`;
- `emergency approved ≠ policy checks globally disabled`;
- `recovery complete ≠ recovery capability retired`.

## SYNTHESIS 9 — long-offline LogMate-like PWA rejoin

Consider a company iPad that last saw policy P7. While offline, P8 tightens remote publication requirements after an assurance incident. The iPad continues to capture unique flight records and queue intents under P7-era UI/runtime state.

Generic rejoin sequence:
1. preserve local records, queue and provenance;
2. do not delete data merely because P7 is stale;
3. obtain current admission/currentness and P8 lineage when connectivity returns;
4. map queued operations to current semantics/consequence classes;
5. revalidate each material operation under P8 rather than replaying P7 cached allows;
6. reject obsolete credentials/policy authority at the server boundary;
7. retain rejected/reconciliation evidence where appropriate;
8. update UX to distinguish locally saved, pending, rejected and remotely confirmed outcomes.

This is a generic model, not a claim about actual LogMate implementation.

## SYNTHESIS 10 — Track B must preserve semantic truth across capability tiers

A user should not be shown `saved` in a way that ambiguously means both `saved locally` and `accepted remotely`. Likewise, a disabled remote action should not imply that local records are lost.

Required UX distinctions are product-specific, but the information architecture should preserve at least the semantic separation between local preservation, queued intent, revalidation requirement, rejection/conflict and authoritative remote confirmation.

OPEN: representative-human, screen-reader, interruption/recovery and physical-iPad validation.

## SYNTHESIS 11 — Track D observes policy drift but cannot authorize it

Useful measures include:
- policy-generation distribution among observed clients;
- stale/unknown policy attempts at material boundaries;
- cached-allow rejection after policy change;
- time spent in degraded/unknown states;
- rollback/PITR reconciliation outcomes;
- recovery-authority use and retirement evidence;
- long-offline rejoin cohorts.

A declining stale-client rate is operationally useful but does not prove stale authority is impossible.

Guards:
- `zero observed P7 traffic ≠ P7 cannot return`;
- `fleet mostly P8 ≠ P7 remote authority acceptable`;
- `dashboard green ≠ policy lineage proven`.

## SYNTHESIS 12 — re-entry requires policy-currentness proof as well as assurance recovery

A system may restore its evidence-source independence but still be running an obsolete degradation map. Re-entry to `NORMAL` therefore checks both the assurance basis and the governing consequence/capability policy generation.

Generic closure evidence includes:
- current policy lineage/generation;
- current consequence classification;
- successor-policy positive tests;
- predecessor-policy negative tests at representative material boundaries;
- stale cache invalidation;
- PITR anti-rollback evidence;
- long-offline rejoin behavior;
- recovery-only authority retirement;
- residual UNKNOWNs.

Guards:
- `assurance sources restored ≠ degraded policy current`;
- `P8 works ≠ P7 powerless`;
- `NORMAL displayed ≠ NORMAL evidence complete`.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate web/PWA work:

1. Treat degraded-mode policy as consequence-bearing authority with explicit lineage/currentness rather than a UI/config flag.
2. Make capability grants non-transitive by default; material remote effects require current authorization at the authoritative boundary.
3. Do not allow clients or legacy adapters to self-classify a request into a weaker consequence tier.
4. Preserve unique local/offline data when policy is stale or unknown; fence remote effects separately.
5. Treat cached authorization/degraded decisions as derived and revocable.
6. Treat PITR/rollback as policy-currentness mutation requiring reconciliation against a non-rolled-back current reference or governed rebootstrap.
7. Do not equate Service Worker activation with policy migration or authority establishment.
8. Scope recovery authority narrowly and require retirement/negative proof after recovery.
9. Include long-offline PWA rejoin and stale-policy replay in destructive validation.
10. Do not claim product PASS until canonical architecture/runtime/device/domain evidence exists.

## DEPENDENCY / TRANSFER

- **Track A → E/C:** Service Worker/client/cache/storage lifetime explains how stale policy state can persist and return.
- **E → B:** E owns what capabilities are authorized; B translates them into truthful task state without inventing security policy.
- **E → C:** C receives policy generation, consequence mapping and anti-rollback invariants for destructive tests.
- **E → D:** D observes drift/currentness/rejection evidence; it does not elect current policy.
- **Software Engineering:** implementation-level policy representation, cache invalidation, fault injection and server enforcement require engineering validation when canonical product architecture exists.
- **Design Studio:** reusable interaction/accessibility treatment remains Design Studio territory; no new physical-device/PWA/human evidence was found in the latest relevant commits.

## Track C destructive additions — defined, not executed

1009. **Client self-classifies consequence:** request marks a remote mutation as low consequence and receives weaker assurance.
1010. **Local-to-remote transitive escalation:** locally permitted capture/queue automatically becomes remote publication authority.
1011. **Cached-allow survives P8:** P7 `NORMAL`/allow cache remains accepted after P8 tightens policy.
1012. **PITR permissive-policy resurrection:** restore revives P7 and the restored system self-elects it current.
1013. **Service-Worker-update theater:** new worker activates but old clients/cache still exercise P7 semantics.
1014. **Recovery-super-role:** emergency mode bypasses unrelated consequence checks and remains reachable after closure.
1015. **Compatibility-tier laundering:** legacy operation is translated successfully but retains obsolete low-risk classification.
1016. **Offline-iPad blind P7 replay:** long-offline device reconnects and queued P7 allows execute without P8 revalidation.

Execution, physical-device, AT and representative-human PASS are not claimed.

## OPEN

Production validation remains OPEN for actual MintTap/LogMate policy representation, consequence classes, server enforcement points, browser/RP/IdP sessions, Service Worker/cache behavior, Firebase/Apple/Google/email auth topology, managed-iPad/WebKit behavior, MDM, queue/replay semantics, backup/PITR reference, legal/aviation/safety consequence classification and human/accessibility behavior.

## CHANGE WATCH

- Service Worker lifecycle/update behavior and Safari/WebKit/iOS/iPadOS implementation differences.
- OWASP authorization guidance and evolving API/application access-control recommendations.
- Actual company auth/provider/runtime architecture when canonical implementation evidence becomes available.

## Gate

**282 PASS (generic).** The Web Manager can now reason about degraded-policy integrity, non-transitive capability tiers, stale-policy/cache/PITR anti-rollback and long-offline PWA rejoin without claiming product/runtime validation.

## Next high-value target

**283 — policy-distribution authenticity, partial-fleet policy convergence & mixed-generation operation adjudication**: determine how a current degraded/normal policy reaches online and long-offline clients without making delivery equal authority, how server boundaries adjudicate mixed P7/P8/P9 clients during staged rollout, and how to retire predecessor policy generations without deleting unique offline data or requiring fleet simultaneity.