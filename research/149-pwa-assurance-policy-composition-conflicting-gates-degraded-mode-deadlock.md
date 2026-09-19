# 149 — PWA Assurance Policy Composition, Conflicting Gates & Degraded-Mode Deadlock Avoidance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + POLICY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 145 evidence graph; 146 event authenticity/reconciliation; 147 coverage continuity; 148 consequence-based gating; Track A observable SW/browser/device state; Track B degraded/recovery UX; Track C policy fault injection; Track D diagnostic telemetry only.

## Why this study exists

148 established that stale/gapped evidence should gate only consequence-bearing capabilities that actually depend on it. The next failure mode appears when several individually reasonable gates compose. A release gate can require current recovery policy; recovery can require a trusted runtime; runtime activation can require a release; sync can require reconciliation that itself needs a policy refresh. Without explicit composition semantics, a weaker rule can accidentally reopen a stronger restriction, or mutually dependent prerequisites can create a recovery deadlock.

The objective is a small-company-compatible policy model in which ordinary authorization is monotonic toward restriction under uncertainty, recovery paths are explicit and bounded, and no client-local degraded-mode rule can silently manufacture authority.

## SOURCE

### Policy decision and enforcement are distinct responsibilities
NIST SP 800-207 defines a policy decision point and policy enforcement point; the policy engine makes grant/deny/revoke decisions from enterprise policy and supporting information, while enforcement applies those decisions to protected resources. This supports separating evidence acquisition from authority decisions and enforcement.

Sources:
- https://doi.org/10.6028/NIST.SP.800-207
- https://pages.nist.gov/zero-trust-architecture/VolumeB/architecture.html

### Granular policies need coordinated enforcement
NIST SP 800-207A describes granular application-level policies and technology components that enforce them across application/service boundaries. It does not prescribe this PWA model, but it supports treating authorization as explicit policy evaluated from multiple identity/status inputs rather than ambient client trust.

Source: https://doi.org/10.6028/NIST.SP.800-207A

### Deny by default is the safe baseline for unmatched authorization
OWASP Authorization Cheat Sheet recommends explicit deny-by-default because complex rule sets can leave requests unmatched or mishandled. This is transfer evidence for authority-critical composition; it does not mean every telemetry defect should globally disable the product.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

### Multiple policies require explicit combination semantics
NIST work on multi-policy access control documents the need to combine multiple independently meaningful access-control policies. Historical XACML/Policy Machine material also demonstrates that rule-combining behavior is an explicit design problem, not something safely left to incidental evaluation order.

Source: https://www.nist.gov/publications/restricting-insider-access-through-efficient-implementation-multi-policy-access-control-systems

## SYNTHESIS — compose requirements, not booleans from arbitrary subsystems

For a consequence-bearing capability, represent each required policy/evidence condition as a typed prerequisite rather than letting subsystems independently set one global `allowed` flag.

Generic decision model:

- **PERMIT** — every mandatory prerequisite for this capability is satisfied in the required scope/generation.
- **RESTRICT** — one or more mandatory prerequisites are known unsatisfied.
- **REVALIDATE** — evidence is stale/gapped/insufficient but an approved observation/reconciliation path can resolve it.
- **RECOVERY-ONLY** — normal capability remains restricted, but a separately authorized bounded action exists to restore prerequisites.
- **UNKNOWN/INDETERMINATE** — policy/evidence cannot support permit; for authority-critical action this does not collapse to permit.

Persistent guards:
- `one policy permits ≠ capability permitted`;
- `one policy restricts capability X ≠ whole app unavailable`;
- `weaker fallback policy ≠ override of stronger mandatory gate`;
- `UNKNOWN ≠ PERMIT` for authority-critical decisions;
- `policy evaluation order ≠ policy precedence`;
- `UI enabled ≠ server authority granted`;
- `offline local capability ≠ remote mutation authority`;
- `recovery path exists ≠ normal gate bypassed`;
- `break-glass authorized ≠ all controls disabled`;
- `cycle detected ≠ safe to drop one prerequisite`.

## Monotonic restriction principle

Within one policy generation and capability scope, loss of assurance may retain or reduce authority but must not accidentally increase authority. A degraded-state fallback may preserve already-authorized local read/export/data capture when product semantics permit; it must not convert uncertainty into new remote write/recovery authority.

A later increase in authority requires a recognized transition: fresh evidence, reconciliation, approved recovery, policy-generation transition, or bounded emergency authorization. Merely changing evaluation order, restarting the PWA, updating the Service Worker or clearing local state is not such a transition.

This is not a claim that every policy system must implement a formal lattice. It is an operational guard: ordinary degraded transitions should be monotonic toward equal/narrower authority.

## Capability-scoped composition

Do not use a single global security switch. Define protected capabilities and prerequisites separately, for example:

- local read/export;
- local offline record creation/editing where product semantics permit;
- remote sync/mutation;
- release promotion;
- trust-policy update;
- recovery/reset;
- break-glass activation.

A release-health gate can pause rollout without disabling local records. A trust/revocation uncertainty can block remote mutation without deleting local data. Recovery can remain available through a bounded control plane even when the normal data plane is restricted.

## Precedence must be semantic, not accidental

A future policy engine should make combination semantics explicit. Generic precedence for authority-critical decisions:

1. explicit incident/compromise containment applicable to the capability;
2. current mandatory authority/revocation/trust prerequisites;
3. bounded exception or recovery authorization that explicitly names which restriction it may supersede and for what effect;
4. ordinary capability policy;
5. default deny if no valid permit path is established.

This is not a universal implementation algorithm. Product policy may need different categories, but **no lower-strength rule may silently erase a higher-consequence mandatory restriction**.

Exceptions are typed edges, not global `override=true`. They must bind subject/scope/effect/generation/expiry/provenance and cannot supersede restrictions outside their declared authority.

## Deadlock model

Construct a prerequisite graph whose nodes are capabilities/actions/evidence and whose directed edges mean `requires-current`. A cycle is operationally dangerous when every node in the strongly connected component requires another member to become current and there is no independently authorized entry edge.

Example bad cycle:

`activate current SW -> requires current trust policy -> requires online reconciliation -> requires current client runtime -> requires current SW`.

Dropping one check ad hoc is not recovery; it is an authorization bypass.

### Safe deadlock resolution patterns

1. **Independent bootstrap/recovery plane** — minimal trusted path can fetch/verify successor trust/runtime material without depending on the blocked normal capability.
2. **Pre-authorized compatibility bridge** — bounded old→new transition material established before retirement, with expiry and anti-downgrade semantics.
3. **Out-of-band recovery evidence** — when threat model requires it, separately authenticated recovery material/authority can re-establish a root prerequisite.
4. **Local data preservation path** — export/read remains available without granting remote authority, preventing security deadlock from becoming data-loss pressure.
5. **Human/break-glass path** — only through the bounded lifecycle already established in 141–143; it does not mean disable all gates.

If no independent entry path exists, report **RECOVERY DEADLOCK / MANUAL RECOVERY REQUIRED**. Do not fabricate permit.

## Policy-generation transitions

Composition rules themselves are versioned security state. A new policy generation must not reinterpret old UNKNOWN/RESTRICT evidence as PERMIT merely because defaults changed. Transition must define:
- predecessor/successor generation identity;
- authenticated authorization for transition;
- which existing evidence remains applicable;
- which gates/prerequisites require revalidation;
- exception migration/retirement;
- rollback policy;
- device/offline compatibility horizon.

`new policy deployed ≠ old device evaluated under new policy`.
`policy syntax valid ≠ transition semantics safe`.

## PWA / Service Worker application

A Service Worker can affect fetch/navigation/cache behavior, but it is not the final authority oracle for server-side remote mutation. A stale or compromised worker must not be able to clear a server recovery/revocation gate by presenting a local degraded-mode flag.

For a long-offline EFB-like iPad:
- preserve irreplaceable local records where product semantics permit;
- distinguish local runtime/SW generation from server policy generation;
- reconnect into revalidation/reconciliation rather than immediate full authority;
- if current runtime requires a trust update and trust update requires a runtime capability, use a deliberately designed bootstrap path or stop at bounded local operation/manual recovery;
- never infer that connectivity restoration itself resolves a policy cycle.

`network online ≠ prerequisite graph resolved`.
`Service Worker activated ≠ recovery authority current`.

Actual WebKit/MDM/background/install/storage behavior remains OPEN until physical/project evidence exists.

## Cross-track transfer

### Track A — Platform & Browser
Own which Service Worker/runtime/storage/navigation states can actually be observed and what activation/control means. Supply facts to policy; do not let browser lifecycle implicitly define authorization precedence.

### Track B — UX / IA
Own truthful presentation of LOCAL-AVAILABLE, SYNC-GATED, REVALIDATION-REQUIRED, RECOVERY-ONLY and MANUAL-RECOVERY states. Recovery affordances must not imply that local data is lost or that a disabled remote capability means the entire app is unusable.

### Track C — Performance / Accessibility / Quality
Own policy-composition tests, cycle detection fixtures, transition/fault injection and accessible recovery/degraded-state validation. Validate effects, not merely rule-engine output.

### Track D — Search / Discovery / Analytics
Diagnostic telemetry can expose gate frequency, cycle detection and recovery duration, but cannot clear authorization gates or become the sole oracle for policy truth.

### Track E — Owner
Own capability taxonomy, mandatory prerequisite semantics, precedence/combining policy, recovery-plane independence, exception authority and policy-generation lifecycle.

## MINTTAP DECISION — minimal sufficient composition model

If implemented for MintTap/LogMate-like systems:

1. enumerate consequence-bearing capabilities rather than one global allow/deny;
2. define mandatory prerequisites and acceptable evidence state per capability;
3. make UNKNOWN fail non-permissively for authority-critical operations;
4. combine restrictions monotonically within a policy generation;
5. permit exceptions only as bounded typed authorizations;
6. keep local data-preservation capability independent where safe;
7. model prerequisite dependencies and reject unresolved cycles before rollout;
8. require at least one independently authorized recovery entry path for any critical strongly connected prerequisite set;
9. version policy-composition semantics and validate transitions/rollback;
10. enforce remote authority server-side even if the PWA UI/runtime is stale or compromised.

No production capability taxonomy, threshold, actual recovery plane or WebKit behavior is asserted.

## VALIDATION — 36-case campaign

1. two mandatory permits allow capability; 2. permit+mandatory restrict yields restrict; 3. permit+authority-critical UNKNOWN does not yield permit; 4. diagnostic UNKNOWN does not block unrelated capability; 5. policy evaluation order changes but result does not; 6. weaker fallback cannot erase containment gate; 7. exception supersedes only named restriction; 8. expired exception cannot permit; 9. exception for release cannot authorize recovery; 10. stale client UI says enabled but server rejects; 11. server permit does not claim stale iPad runtime current; 12. local read remains while remote mutation gates; 13. local export remains during trust revalidation; 14. SW update does not clear recovery gate; 15. network reconnect does not clear trust gate; 16. prerequisite DAG evaluates normally; 17. direct two-node cycle detected; 18. indirect multi-node cycle detected; 19. cycle with independent bootstrap edge can recover; 20. cycle without independent entry reports deadlock; 21. operator cannot resolve deadlock by silently dropping prerequisite; 22. break-glass has bounded effect/expiry; 23. break-glass retirement restores normal policy; 24. policy generation update invalidates only affected evidence; 25. policy rollback cannot silently restore superseded weak defaults; 26. stale backup restores old policy state but not old authority; 27. offline iPad spans several policy generations and enters revalidation; 28. compromised worker cannot forge server permit; 29. server policy cannot falsely claim physical SW activation; 30. contradictory evidence produces non-permit/revalidation rather than arbitrary winner; 31. simultaneous gate changes are idempotently recomputed; 32. partial policy update fails closed for affected authority, not global data deletion; 33. recovery bootstrap material is unavailable and system preserves local data/manual path; 34. analytics instrumentation outage does not become authorization deadlock; 35. accessible UI exposes capability-scoped state and recovery action; 36. end-to-end long-offline reconnect with stale SW + trust-policy change + sync gate reaches either bounded convergence or explicit manual recovery without false permit or unnecessary local-data loss.

## CONTRADICTION / failure-mode analysis

### Permit-overrides theater
Treating any positive subsystem signal as sufficient can let low-strength policy erase a revocation/containment gate.

### Deny-everything theater
Global fail-closed on every evidence defect converts diagnostics problems into product outages and creates pressure for unsafe overrides.

### Evaluation-order theater
`last rule wins` or incidental configuration order is not a defensible security precedence model.

### Recovery-bypass theater
A hidden admin button that ignores normal gates is not a recovery architecture. It creates a standing universal authority path.

### Circular-safety theater
Two controls that each require the other can look individually strict while making legitimate recovery impossible. Operational impossibility eventually encourages ad hoc bypass.

### Client-authority theater
A PWA/Service Worker can present local state but cannot be trusted to grant server-side authority merely because it reports successful recovery.

## OPEN

Actual MintTap/LogMate capability taxonomy, server/API authorization model, policy engine, trust/revocation state, recovery bootstrap, exception authority, policy generations, Service Worker update design, managed-iPad/WebKit/MDM constraints, offline-edit semantics, local authoritative-data rules, backend availability and safety/legal requirements remain unknown. Production composition rules are not claimed.

## CHANGE WATCH

- Browser/WebKit/MDM lifecycle and observability can change; Track A must keep platform facts current.
- Authorization frameworks can have different default/combining semantics; implementation must explicitly configure and test intended behavior rather than inherit library defaults.
- NIST SP 800-207/207A are architecture guidance, not PWA-specific standards; transfer remains conceptual.
- Product consequence/recovery topology changes can introduce new prerequisite cycles and must trigger policy-graph validation.

## Gate result

**PASS (generic).** The Web Manager can now compose multiple assurance gates by capability and prerequisite rather than global booleans; preserve non-permissive handling of authority-critical uncertainty without global outage; detect circular prerequisite deadlocks; and require bounded independent recovery entry rather than silently weakening policy.

Product/provider/managed-iPad policy runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA policy-graph rollout safety, shadow evaluation & decision-diff validation.** Composition can be logically sound yet a new policy generation can still unexpectedly gate or permit real traffic. The next bottleneck is how to evaluate candidate policy against representative/current decision contexts, compare old/new decisions without making shadow results authoritative, identify dangerous permit expansions and recovery-path regressions, and roll out/rollback policy semantics without letting stale offline clients or observability gaps create false confidence.