# 252 — PWA Gate-Policy Distribution Compromise, Consumer Checkpoint Recovery & Partial-Fleet Convergence Debt

Status: **PASS (generic) / PRODUCT + DISTRIBUTION + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/cache/Service Worker mechanics; Track B degraded/recovery UX; Track C destructive convergence validation; Track D bounded rollout/stale-tail measurement.  
Dependencies: 137, 171–251, especially anti-rollback/fork recovery, branch convergence, witness survivability, corpus promotion/currentness and gate-policy split-brain resistance.

## Problem
251 made the promotion record a scoped authorization object and separated gate-policy generation from app/Service Worker generation. The next failure surface is distribution and consumption: an authentic canonical policy can still be served inconsistently through origin/CDN/cache paths; a client can lose or corrupt its remembered monotonic floor; and a long-offline or legacy tail can remain on an older generation after the control plane has advanced.

Central rule: **distribution success is not authority success. Consequence-bearing consumers must authenticate the policy object and its lineage/currentness independently of the transport/cache path, preserve or safely recover a monotonic checkpoint, and treat non-converged fleet segments as explicit scoped assurance debt rather than silently declaring rollout complete.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns HTTP cache, navigation, Service Worker/cache lifecycle and restart mechanics. These explain how stale bytes can persist; they do not establish policy authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `POLICY-STALE`, `CHECKPOINT-RECOVERY-REQUIRED`, `POLICY-CONFLICT`, `DEGRADED-NONMUTATING`, and `REJOIN-REQUIRED` states without destructive reset.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns distribution/restart/offline/rejoin destructive sequences. Campaign expands **768 → 776 defined cases**; defined cases are not execution PASS.
- **D Search/Discovery/Analytics:** bounded consumer. Measures policy-generation distribution, stale/unknown tails, convergence windows and debt closure with explicit denominators; telemetry does not elect canonical policy.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns authenticated publication/distribution, checkpoint recovery, rollback/fork containment, partial-fleet debt and closure criteria.

## SOURCE

### TUF — authenticated freshness, rollback/freeze resistance and coherent repository state
The Update Framework distinguishes authenticated metadata from freshness/currentness and explicitly addresses rollback/freeze attacks. Snapshot metadata binds coherent metadata versions/hashes, while Timestamp supplies short-lived freshness information. This is bounded precedent for requiring consumers to verify policy identity/currentness rather than trusting CDN/origin freshness or HTTP cache age alone.

Sources:
- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/docs/metadata/

**TRANSFER VALIDATION:** MintTap does not adopt TUF as its gate-policy protocol. The transferable property is authenticated currentness plus rollback/freeze resistance across untrusted or stale distribution paths.

### RFC 9162 — consistency across observers is separate from one valid view
Certificate Transparency v2 defines consistency proofs between tree heads and separately identifies consistency of the log view presented to all query sources as an audit property. A valid signed view at one observer does not establish that all observers received the same view.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** bounded anti-equivocation precedent only; no CT infrastructure decision is made.

### NIST SP 800-53 Release 5.2.0 — controlled change and resilient update precedent
NIST SP 800-53 Release 5.2.0 is current as of this study. Configuration/change-control precedent requires controlled, reviewable change rather than treating successful distribution as sufficient evidence of accepted state; the 5.2.0 release also strengthened software-update/resiliency guidance.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls

**TRANSFER VALIDATION:** this is governance precedent, not a MintTap-specific protocol prescription.

### Service Worker/browser boundary
Service Worker and Cache Storage can retain and serve application-controlled resources across navigations. Their lifecycle/current controller state is a browser/runtime property. Therefore policy authority must not be inferred from `controllerchange`, cache hit, app-shell version, network success or HTTP freshness alone.

**DEPENDENCY:** Track A owns the browser mechanics; Track E consumes them for trust/currentness design.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**. Repaired exact-fixture macOS Safari Service Worker registration→control→V1→V2 update/controller replacement→fresh-WebDriver V2 control recovery is bounded PASS; origin-down fresh cold-start, ordinary Safari installed/profile persistence, physical iOS/iPadOS/EFB and canonical-product runtime remain OPEN.

**DEPENDENCY:** generic distribution/currentness reasoning cannot upgrade these gates.

## SYNTHESIS 1 — transport authenticity and policy authority are separate
HTTPS protects a connection to an authenticated endpoint, but a correctly authenticated CDN/origin can still serve an obsolete, misconfigured or selectively inconsistent policy object. Conversely, an offline cache can contain historically authentic bytes that are no longer current.

Require verification of the policy object's identity, authorization scope, generation/lineage and currentness conditions independently of transport success.

Guards: `HTTPS success ≠ policy current`; `CDN trusted ≠ object current`; `cache hit ≠ authority hit`; `HTTP 200 ≠ canonical policy`.

## SYNTHESIS 2 — distribution paths are allowed to be stale; consequence boundaries are not allowed to forget that
CDN propagation delay, browser cache, Service Worker cache and offline operation create legitimate temporary skew. The design error is not skew itself; it is letting skew silently authorize consequences beyond the policy's allowed interval/scope.

A consumer may continue safe local/read-only work under an explicitly defined stale/degraded mode when product semantics permit. Current mutation/sync/admission requires the applicable currentness rule.

Guard: `temporary distribution skew ≠ permission to ignore policy floor`.

## SYNTHESIS 3 — consumer checkpoint/floor is security state
Once a consequence-bearing consumer has accepted policy generation G20, its remembered minimum acceptable generation/checkpoint is security-relevant state. Clearing browser storage, reinstalling an app shell, replacing a Service Worker or losing local metadata must not silently reset the consumer to accepting G12.

Guard: `local state reset ≠ authority reset`.

## SYNTHESIS 4 — checkpoint loss needs recovery, not rollback
If the consumer loses or corrupts its floor/checkpoint, it enters `CHECKPOINT-RECOVERY-REQUIRED`. It obtains a current bootstrap/currentness assertion from a trust path appropriate to the failure hypothesis and verifies lineage/conflict before consequence-bearing re-admission.

Do not use "highest version seen from the first reachable endpoint" as recovery. Do not select the newest timestamp when conflicting signed successors exist.

Guards: `checkpoint missing ≠ floor zero`; `first reachable server ≠ bootstrap authority`; `newest signed object ≠ canonical successor`.

## SYNTHESIS 5 — checkpoint backup can create a rollback oracle if restored blindly
Backing up consumer checkpoint state improves recoverability, but restoring an old checkpoint after the fleet has advanced can itself enable rollback. A restored checkpoint is historical evidence and a lower bound candidate; it must be reconciled with current authenticated bootstrap/lineage before current authority is granted.

Guard: `checkpoint restored ≠ currentness restored`.

## SYNTHESIS 6 — distribution split-brain must preserve conflicting observations
If region A/CDN edge serves canonical G20 while another path serves conflicting G20B, consumers should preserve the contradictory signed objects/evidence and enter `POLICY-CONFLICT` for affected consequences. Do not resolve by latency, majority of clients, newest HTTP Date, CDN POP count or telemetry volume.

RFC 9162 is bounded precedent that consistency across observers is distinct from one signed view's validity.

Guards: `most-served policy ≠ canonical policy`; `edge majority ≠ governance majority`; `fastest endpoint ≠ trusted successor`.

## SYNTHESIS 7 — partial fleet convergence is a first-class assurance state
A rollout can be canonical at the control plane while only part of the fleet has consumed it. Model at least:
- known current/converged;
- known stale but safely isolated/degraded;
- known stale with prohibited consequence path;
- offline/unknown tail;
- conflicting/forked observation;
- checkpoint-recovery-required.

Do not collapse unknown/offline into current. Do not call rollout complete because active-online clients are green.

Guard: `online fleet converged ≠ fleet converged`.

## SYNTHESIS 8 — convergence debt needs explicit denominator and consequence scope
Partial convergence becomes **assurance debt** when a required population cannot yet consume the successor policy. Record:
1. affected policy generation and consequence boundary;
2. population denominator and known unknown tail;
3. why the tail exists;
4. containment/degraded capability;
5. maximum acceptable duration or revalidation trigger;
6. owner and closure evidence.

A percentage without a denominator or excluded-offline population is not closure evidence.

Guards: `99% current ≠ remaining 1% harmless`; `unknown denominator ≠ 100%`; `telemetry silence ≠ retired device`.

## SYNTHESIS 9 — convergence closure requires negative as well as positive evidence
Closure is stronger than observing G20 acceptance. For required consequence boundaries, validate that:
- canonical G20 is accepted where applicable;
- predecessor G19/G12 is rejected or confined to historical/degraded scope;
- conflicting G20B is rejected/contained;
- checkpoint-loss recovery cannot reset the floor;
- required stale/unknown tail is retired, rejoined or explicitly remains approved debt.

Guard: `new policy accepted ≠ old policy rejected`.

## SYNTHESIS 10 — emergency bypass does not erase convergence debt
An incident may justify temporary operation for a stale/offline segment, but emergency authority must be scoped, expiring and separately auditable. When normal distribution recovers, the emergency path is retired and the segment must still converge/revalidate.

Guards: `emergency access ≠ convergence`; `incident over ≠ emergency authority retired`.

## SYNTHESIS 11 — PWA update mechanics cannot repair lost trust state by themselves
A new Service Worker can refresh app code and caches, but it cannot by itself prove the canonical gate-policy successor or safely reconstruct a lost monotonic floor. Conversely, a stale Service Worker does not justify deleting unique offline data.

Track split:
- A: worker/cache/navigation lifecycle;
- E: bootstrap/currentness/authority;
- C: restart/offline/fork/rejoin validation;
- B: safe user-visible degraded/recovery states.

Guard: `Service Worker updated ≠ trust checkpoint recovered`.

## SYNTHESIS 12 — long-offline LogMate/EFB rejoin
For a company iPad returning with G12 after current governance is G20:
1. preserve unique flight/logbook data and G12 evidence;
2. do not use G12 for current sync/mutation merely because it was once valid;
3. obtain canonical current bootstrap/gate-policy state through an authenticated path;
4. detect rollback/fork/conflict and recover checkpoint/floor if necessary;
5. migrate schema/data separately from authority;
6. re-admit queued operations individually under current policy;
7. preserve rejected operations/evidence according to product retention rules.

If currentness cannot be established, remain in a non-destructive degraded/recovery state. Physical iPadOS/WebKit/MDM behavior remains OPEN.

## MINTTAP DECISION / DIRECTION
For future consequence-bearing PWA policy distribution:
- treat CDN/origin/cache/Service Worker as distribution mechanisms, not authority roots;
- bind policy identity/generation/lineage/scope to authenticated promotion/currentness evidence;
- maintain a monotonic consumer floor/checkpoint appropriate to the trust model;
- define explicit checkpoint-loss recovery that cannot silently reset to an older generation;
- preserve split-view evidence rather than electing by timestamp/majority/latency;
- model partial fleet convergence and unknown/offline tails as explicit assurance states;
- permit stale/degraded operation only where consequence semantics explicitly allow it;
- require negative predecessor/conflict rejection evidence for convergence closure;
- preserve unique offline user data through authority uncertainty.

These are generic directions, not claims about existing MintTap or LogMate implementation.

## Track C — destructive campaign additions
Add eight defined cases:
1. **CDN stale-policy laundering** — authenticated edge serves superseded policy and consumer accepts it as current.
2. **Service-Worker cache authority promotion** — cached signed policy is treated as current because worker controls the page.
3. **checkpoint-loss floor reset** — local checkpoint disappears and client accepts the oldest still-valid policy.
4. **stale checkpoint restore rollback** — backup restores an older floor and current mutation resumes without rebootstrap.
5. **regional split-view majority election** — conflicting policy branches are resolved by POP/client majority.
6. **online-only convergence laundering** — rollout is declared complete while offline/unknown tail is excluded from denominator.
7. **positive-only convergence closure** — successor acceptance is tested but predecessor/conflict rejection is not.
8. **offline-iPad destructive recovery** — stale authority leads to reset/deletion of unique local records instead of preservation + rejoin.

Campaign state: **768 → 776 defined cases. Execution PASS is not claimed.**

## TRANSFER / CONTRADICTION analysis
- Software Engineering's repaired Safari lifecycle PASS strengthens Track A/C understanding that Service Worker generation can advance and recover across a fresh WebDriver session for the exact fixture; it does **not** prove policy currentness, checkpoint persistence, installed-PWA behavior or physical iPad behavior.
- The still-OPEN origin-down fresh cold-start case is directly relevant to partial-fleet/offline recovery and remains a validation dependency, not a contradiction to this generic model.
- Design Studio's open physical-PWA/human/AT gates mean recovery/degraded state comprehension remains unvalidated.

## OPEN / VALIDATION
Production validation remains OPEN for:
- actual policy/promotion schema and signing/currentness mechanism;
- CDN/origin/cache topology and purge/propagation behavior;
- Service Worker policy caching and update behavior;
- persistence/backup/reset behavior of consumer checkpoint state;
- browser profile clearing/reinstall/device replacement semantics;
- installed PWA and physical iOS/iPadOS/WebKit/MDM behavior;
- fleet inventory/denominator and offline-device retirement rules;
- exact degraded capabilities and consequence boundaries;
- runtime anti-rollback/fork/split-view tests;
- actual sync/auth/session/storage architecture.

## CHANGE WATCH
Browser/OS PWA persistence and lifecycle behavior, CDN/provider cache semantics, MDM behavior and provider identity/control-plane capabilities remain platform/provider-specific CHANGE WATCH. TUF and RFC 9162 remain bounded precedents only.

## Gate
**PASS (generic).** The Web Manager can distinguish policy distribution from policy authority, reason about consumer checkpoint loss without rollback, model partial-fleet convergence debt with explicit denominators/consequence scope, and apply these rules to long-offline PWA rejoin without claiming production validation.

## Next high-value target
**253 — convergence-debt expiry, device-retirement authority & stale-tail resurrection resistance**: determine when an unreachable/offline client can be legitimately retired from the required fleet denominator; prevent telemetry silence, account deletion, MDM disappearance or inventory cleanup from becoming proof of retirement; bind retirement to consequence scope and governance authority; and safely handle a supposedly retired device that later reappears with unique data and obsolete policy state.