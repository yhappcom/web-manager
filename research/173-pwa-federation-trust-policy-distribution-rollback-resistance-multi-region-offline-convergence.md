# 173 — PWA Federation Trust-Policy Distribution, Rollback Resistance & Multi-Region/Offline Convergence

Status: **PASS (generic) / PRODUCT + FEDERATION + MULTI-REGION + PROVIDER + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A HTTP/cache/SW/reconnect mechanics; Track B degraded/reconciliation UX; Track C destructive convergence validation; Track D privacy-bounded observability.  
Dependency: 171–172 federation evidence, metadata currentness, split-view and successor-anchor governance.

## Why this study exists

172 established that federation metadata, JWKS, trust chains and local trust-anchor configuration are versioned security state. The next failure boundary is distribution: a correct new trust policy is not operationally effective merely because it exists at one control-plane node. Multi-region servers, edge/cache layers and long-offline PWA clients can observe different generations during rollout, outage, emergency revocation or recovery.

Central rule:

> **Trust-policy publication is a distributed security-state transition. Separate authoring, authorization, publication, regional admission, enforcement and client observation; make rollback detectable; define safe degraded behavior; and prove bounded convergence from authoritative server-side evidence rather than client cache possession.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. HTTP freshness/revalidation, cache invalidation limits, Service Worker control, IndexedDB/local projections and reconnect are transport/storage mechanics, not authority.
- **B UX/IA/Content:** consumes policy states as consequences: access current, refresh required, submission paused, local work preserved, review required. It must not expose raw federation topology.
- **C Quality/Accessibility:** owns rollout/partition/rollback/emergency-revoke/offline-fleet destructive campaigns and accessible degraded/recovery states.
- **D Search/Analytics:** bounded consumer. Convergence telemetry must not become a persistent cross-organization identity graph.
- **E Security/Operations:** **bottleneck/owner**. Owns policy generations, authorization/publication gates, regional admission, anti-rollback floors, emergency distribution, convergence proof and incident recovery.

## SOURCE

### RFC 9111 — HTTP Caching

RFC 9111 distinguishes fresh, stale and successfully revalidated cached responses. `must-revalidate` prevents reuse of stale responses without successful origin validation. It also states that invalidation caused by a state-changing request only affects caches through which that request travels; it does not guarantee global invalidation.

Source: https://www.rfc-editor.org/rfc/rfc9111.html

Transfer: HTTP cache invalidation is not a global trust-policy convergence protocol. Security-critical policy lifetime and HTTP freshness may interact but are not the same semantic lifetime.

### RFC 9205 — Building Protocols with HTTP

RFC 9205 warns that stale responses can be reused in disconnected operation and recommends `must-revalidate` when that is unsuitable. It explicitly says application semantic lifetime can differ from HTTP freshness lifetime and should be represented separately.

Source: https://www.rfc-editor.org/rfc/rfc9205.html

Transfer: a trust-policy generation needs explicit semantic validity/currentness rules; `Cache-Control` alone cannot define authorization authority.

### OpenID Federation 1.0 — Final

OpenID Federation 1.0 models trust from locally trusted anchors through validated trust chains. It provides status checking for Trust Mark instances, with states including active, expired, revoked and invalid. A resolver used by another entity becomes a trusted component because the caller relies on it to validate protected metadata correctly.

Source: https://openid.net/specs/openid-federation-1_0.html

Transfer: federation evidence can have status/currentness separate from its historical cryptographic validity. Local trust-policy distribution must preserve that distinction.

### NIST SP 800-53 Rev.5 — Configuration Management

NIST configuration-management controls treat configuration changes as controlled system changes and include automated deployment of updated baselines across an installed base and automated security response to unauthorized configuration modification.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

Transfer: trust policy is security configuration. Production topology and exact deployment mechanics belong to Software Engineering/operations implementation, but Web Manager requires controlled, observable, reversible-by-correction distribution rather than ad hoc mutable config.

## SYNTHESIS — separate the distribution objects

Do not collapse:

1. **policy content** — accepted issuers/anchors/claim classes/constraints;
2. **policy generation** — monotonic semantic version/epoch used for ordering and anti-rollback;
3. **policy authorization evidence** — who approved this generation and under which governance;
4. **publication state** — generation is available from the authoritative control plane;
5. **regional admission state** — a server/region has validated and admitted the generation;
6. **enforcement state** — requests are actually evaluated against that generation/floor;
7. **client observation** — browser/PWA last observed a projection of policy consequences;
8. **convergence evidence** — bounded evidence showing which controlled enforcement domains have reached the required floor.

Persistent guards:

- `policy authored ≠ policy authorized`;
- `policy authorized ≠ policy published`;
- `policy published ≠ every region admitted it`;
- `region admitted policy ≠ every in-flight request used it`;
- `HTTP 200/cache hit ≠ current trust policy`;
- `cache invalidated ≠ global convergence`;
- `client observed generation G ≠ server currently enforces G`;
- `all sampled clients current ≠ entire fleet converged`;
- `all controlled regions converged ≠ offline/unmanaged copies updated`;
- `newer timestamp ≠ newer authorized policy generation`;
- `rollback technically possible ≠ rollback semantically authorized`;
- `emergency revoke published ≠ revoke effective everywhere`;
- `provider unreachable ≠ stale trust becomes current`;
- `Service Worker updated ≠ trust-policy reconciliation complete`.

## Normal rollout versus emergency revocation

Treat them as different operational protocols.

### Planned policy change

A planned change can use staged admission when consequence boundaries allow it. The authoritative generation advances only through approved governance. Regions validate signature/provenance/schema/dependencies before admission. Mixed generations during a bounded rollout are expected but observable; high-consequence cross-region behavior must not depend on silent last-write-wins.

### Emergency issuer/anchor revoke

Emergency revocation is fail-safe state reduction, not ordinary configuration rollout. Required properties:
- independently authorized emergency path;
- monotonic emergency floor that old snapshots/config cannot silently lower;
- rapid distribution to controlled enforcement points;
- explicit treatment of unreachable regions as `currentness unknown`, not implicitly safe;
- consequence-bearing operations requiring the revoked authority are denied/held where current policy cannot be established;
- unique local user data remains readable/exportable where safe and is not destroyed merely because remote authority is unavailable;
- recovery to a successor trust state creates a new generation; it does not erase the compromise/revocation generation.

Do not invent a generic propagation SLA. Actual maximum acceptable exposure depends on product consequence, provider contract and architecture and remains OPEN.

## Anti-rollback and restore

Rollback resistance requires a security floor outside ordinary mutable application snapshots. A PITR restore, regional image rollback or stale configuration replica may recover generation G-3 while the authoritative floor is G. Before serving consequence-bearing traffic, the restored component must reconcile to at least the current required floor.

`restore completed ≠ authorization safe to reopen`.

A deliberate semantic correction should normally be a new forward generation, not restoration of an old generation number. Historical policy remains evidence; it is not automatically current authority.

## Multi-region convergence model

Generic convergence evidence should answer:
- what generation/floor is authoritative;
- which controlled regions/enforcement classes have admitted it;
- when each last proved enforcement at/above that floor;
- which regions are unreachable/unknown;
- whether materially different concurrent policy views exist;
- whether requests can cross from a current region into a stale authorization dependency;
- whether rollback/PITR can reintroduce an older floor.

Do not claim universal convergence from client telemetry. Client reports are observations and can be stale, spoofed, sampled or absent. Server/control-plane attestation plus independent probes can establish bounded controlled-domain evidence; physical offline clients remain separately classified.

## PWA / managed-iPad offline transfer

A long-offline Home Screen PWA can legitimately miss many policy generations. It may retain app shell/SW, local records, drafts, old session projections and historical federation information.

Reconnect order:
1. preserve unique local operational data;
2. establish transport to a current authoritative server path;
3. obtain current server-side trust/authority floor independent of stale client business state;
4. compare queued-operation authority generation with current floor;
5. refresh federation evidence as required by server policy;
6. admit only operations valid under current authority;
7. quarantine non-admitted work for explicit review/resubmission;
8. update app shell/SW independently from semantic trust reconciliation.

No generic claim is made that Safari/iPadOS refreshes policy, metadata, JWKS, tokens or Service Workers while backgrounded/offline. Physical Safari/Home Screen/MDM transfer remains OPEN.

## UX transfer — Track B

Prefer consequence language:
- `Access needs to be checked before submission.`
- `Your saved records remain on this device.`
- `Your organization access changed while this device was offline.`
- `Service is temporarily limited while access information is updated.`

Do not tell users `policy G173`, raw issuer/anchor identifiers or region topology in ordinary UI.

## Privacy/analytics transfer — Track D

Measure convergence by controlled enforcement class/region/generation where possible, not per-user federation identity. Client-fleet measurements should minimize subject, employee, issuer and organization linkage. Security observability is purpose-bound data processing, not an exemption from minimization.

## MINTTAP DECISION — generic governance

1. Model trust-policy distribution as a versioned distributed security-state transition.
2. Keep semantic policy lifetime distinct from HTTP cache freshness.
3. Use monotonic policy/floor semantics so stale snapshots cannot silently regain authority.
4. Separate normal rollout, emergency revocation and compromise recovery.
5. Do not fail open from `currentness unknown` to stale authority for consequence-bearing operations.
6. Prove bounded convergence over controlled enforcement domains; do not claim universal fleet convergence from client telemetry.
7. Preserve unique offline PWA data while re-establishing current authority before replay.
8. Service Worker/app-shell convergence and authorization-policy convergence are separate.
9. Keep convergence telemetry privacy-bounded.
10. Actual MintTap/LogMate regions, IdPs, federation topology, policy store, SLAs, MDM and physical-iPad behavior remain OPEN.

## VALIDATION — 144-case destructive campaign

Campaign families: planned G→G+1 rollout; partial regional admission; regional outage; stale edge/cache; `must-revalidate` behavior; stale-while-disconnected attempts; control-plane outage; policy signature failure; unauthorized policy; schema mismatch; dependency mismatch; concurrent G/G+1 views; G+1/G+2 leap; region rollback; VM/image rollback; PITR restore; backup restore; stale config replica; emergency issuer revoke; emergency anchor revoke; compromised authorizer; successor anchor; revoke during provider outage; revoke during region partition; unknown-currentness fail-open attempt; fail-safe mutation hold; bounded local read/export; cross-region request routing; stale downstream authorization dependency; split-view detection; false-positive divergence during rollout; generation monotonicity; clock skew; replayed old signed policy; copied policy without provenance; lost publish ACK; duplicate publish; idempotent admission; restart during admission; crash after admission/before enforcement; enforcement before durable admission; observability lag; false convergence dashboard; sampled-client blind spot; spoofed client generation; offline client absent from telemetry; SW stale/current combinations; IndexedDB stale projection; BFCache/history; long-offline cold start; one-generation reconnect; multi-generation reconnect; queued operation authorized-then-revoked; same actor re-authorized under new generation; old queue not auto-executed; explicit resubmission; unique flight record preservation; export during authority outage; provider A→B migration during rollout; key rotation during policy rollout; trust-mark revoked; trust-mark status unavailable; resolver outage/compromise; DNS/TLS failure; region DNS split; CDN cache invalidation incomplete; malicious cache poisoning attempt; physical Safari; Home Screen; managed iPad; Shared iPad/user switch; accessibility of degraded state; keyboard/screen-reader recovery; reduced-motion/non-color-only state; human comprehension; incident reconstruction; privacy-minimized convergence telemetry.

Generic campaign definition is PASS. Execution against actual product/provider/browser/device remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION

- **TRANSFER VALIDATION:** 172's split-view rule remains: materially different concurrent valid-looking trust views are reconciliation/incident conditions, not automatic proof of attack.
- **TRANSFER VALIDATION:** 099/118/119 anti-rollback and emergency-gate principles apply to federation trust policy; this study adds distributed admission/convergence semantics.
- **TRANSFER VALIDATION:** RFC 9111 supports the distinction between HTTP cache freshness and global invalidation; it does not provide global security-state convergence.
- **CONTRADICTION:** `purge CDN/browser cache and therefore federation revoke is complete` is rejected.
- **CONTRADICTION:** `offline client still has old signed policy, therefore it may continue consequence-bearing remote authority indefinitely` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual policy representation/signing; control-plane topology; regional count; deployment mechanism; provider/IdP federation model; maximum propagation/revocation objective; server-side authorization topology; edge/CDN behavior; offline queue semantics; LogMate data model; managed-iPad/MDM; physical Safari/Home Screen; human/AT evidence.

DEPENDENCY — Software Engineering: implementation of monotonic generations, atomic admission, control-plane replication, probes, rollback/PITR gates and queue reconciliation requires project architecture/runtime evidence.

DEPENDENCY — Design Studio: consume accessible degraded/reconciliation-state interaction evidence; do not invent visual system here.

CHANGE WATCH: OpenID Federation ecosystem/provider adoption; Safari/iPadOS PWA behavior; provider-specific key/metadata/status semantics; HTTP/browser cache behavior where implementation-specific.

## Gate

**173 PASS (generic).** The Web Manager can now distinguish policy creation, publication, regional admission, enforcement, client observation and convergence; reason about planned rollout versus emergency revocation; reject cache invalidation as global convergence proof; preserve offline PWA data while re-establishing authority; and define bounded convergence evidence without claiming unknown production facts.

Next adjacent bottleneck: **federation trust-policy availability, emergency fail-safe degradation & recovery objectives** — quantify consequence-specific availability versus security trade-offs under control-plane/provider outage without converting stale trust into indefinite authority or making offline-first PWA data unusable.