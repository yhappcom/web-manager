# 150 — PWA Policy-Graph Rollout Safety, Shadow Evaluation & Decision-Diff Validation

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + POLICY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 145 evidence graph; 146 event authenticity/reconciliation; 147 coverage continuity; 148 consequence-based gating; 149 policy composition/deadlock avoidance; Track A runtime-generation facts; Track B truthful rollout/revalidation UX; Track C differential/fault validation; Track D diagnostic sampling only.

## Why this study exists

149 made policy composition explicit, capability-scoped and deadlock-aware. The next risk is transition: a candidate policy can be syntactically valid and internally coherent yet change real decisions in unsafe ways. A rollout can accidentally expand remote mutation authority, deny legitimate recovery, strand stale offline clients, or create a prerequisite cycle only for contexts absent from ordinary tests.

The objective is a small-company-compatible rollout discipline that compares predecessor and candidate policy generations over representative decision contexts before candidate output becomes authoritative, treats decision differences by consequence rather than raw count, and preserves a known recovery path through rollout and rollback.

## SOURCE

### Schema validation is useful but not behavioral equivalence
Amazon Verified Permissions can run Cedar policy validation in STRICT mode against a schema and reject new/updated policies that fail validation. Its test bench can simulate authorization requests and return allow/deny plus determining-policy diagnostics. These capabilities support pre-deployment structural and scenario testing, but neither proves that a candidate policy preserves intended decisions across real production contexts.

Sources:
- https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_ValidationSettings.html
- https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/test-bench.html

### Authorization combination semantics matter to diffs
Cedar uses default deny; a satisfied `forbid` overrides satisfied `permit`; evaluation errors are reported diagnostically and the erroneous policy is skipped for the authorization result. This is implementation-specific evidence that a decision diff must retain determining-policy/error diagnostics rather than compare only final booleans.

Source:
- https://docs.cedarpolicy.com/auth/authorization.html

### Policy/schema engine upgrades can change compatibility
Amazon documents Cedar 2→4 compatibility changes affecting policy/schema/request syntax, validator precision and built-in behavior, and disabled authorization APIs for remaining Cedar 2 stores beginning April 2026. This is direct evidence that policy-language/runtime generation is part of rollout state rather than timeless configuration.

Source:
- https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/cedar4-faq.html

### Canarying limits blast radius but requires evaluation
Google SRE describes canarying as partial, time-limited deployment plus evaluation against a control, with rollout proceeding or pausing/rolling back based on evaluation. Transfer is operational: policy rollout also benefits from staged exposure and explicit evaluation, but authorization consequences require stricter semantics than generic error-rate canaries.

Source:
- https://sre.google/workbook/canarying-releases/

## SYNTHESIS — four distinct rollout phases

Treat policy rollout as four different activities:

1. **STATIC/STRUCTURAL VALIDATION** — syntax, schema/type checks, policy-graph integrity, prerequisite-cycle analysis, generation lineage and required recovery entry paths.
2. **REPLAY / FIXTURE DIFFERENTIAL** — evaluate predecessor and candidate over curated decision contexts, historical contexts where retention/privacy permits, boundary cases and destructive fixtures.
3. **SHADOW EVALUATION** — for live requests, compute the candidate decision in a non-authoritative plane while the predecessor remains the sole authority.
4. **BOUNDED AUTHORITATIVE ROLLOUT** — only after diff review, make the candidate authoritative for an explicitly bounded population/capability, observe consequences, then expand or halt.

Persistent guards:
- `policy validates ≠ policy behavior safe`;
- `shadow evaluated ≠ shadow authorized`;
- `same final decision ≠ same decision basis`;
- `small diff count ≠ low-risk diff`;
- `zero observed diff ≠ semantic equivalence`;
- `representative traffic ≠ exhaustive state space`;
- `canary healthy ≠ offline fleet compatible`;
- `candidate deployed ≠ candidate authoritative everywhere`;
- `rollback config restored ≠ predecessor authority safely restored`;
- `client reports candidate generation ≠ server should trust candidate decision`.

## Shadow plane must have no authority

A shadow evaluator may receive the same normalized decision context as the authoritative evaluator and emit candidate decision/diagnostics for comparison. It must not:
- grant/deny the user request;
- mutate authoritative trust/recovery state;
- clear containment/revocation gates;
- write data that later becomes an implicit authorization input without separate admission;
- trigger destructive recovery or reset;
- become a fallback when the authoritative evaluator fails.

Shadow failure is diagnostic degradation. It must not silently switch the system to candidate authority.

`shadow unavailable ≠ use candidate as fallback`.

## Decision-diff model

Compare more than `ALLOW/DENY`. A useful diff record binds:
- predecessor/candidate policy generation and evaluator/runtime generation;
- capability/action, subject class, resource class and relevant context class;
- old decision and new decision;
- determining policy/restriction categories and evaluation errors;
- evidence/prerequisite state class used by each generation;
- environment/device/runtime cohort where known;
- consequence class;
- provenance/time sufficient for debugging without retaining unnecessary sensitive payloads.

Classify at minimum:

1. **PERMIT EXPANSION** — predecessor non-permit → candidate permit. Highest scrutiny for remote mutation, trust-policy update, recovery/reset and break-glass.
2. **NEW RESTRICTION** — predecessor permit → candidate non-permit. May be intended containment, but can break ordinary use or recovery.
3. **BASIS CHANGE / SAME RESULT** — final decision unchanged but determining prerequisite/policy/error path changed. Important because future evidence changes may diverge.
4. **ERROR/INDETERMINATE CHANGE** — evaluator errors or UNKNOWN handling differs.
5. **RECOVERY-PATH REGRESSION** — normal restriction may be correct but candidate removes the only independently authorized recovery edge.
6. **OFFLINE/GENERATION COMPATIBILITY REGRESSION** — stale supported client cannot enter revalidation/bootstrap under candidate semantics.

Do not rank by raw frequency alone. One permit expansion of reset authority can dominate thousands of benign new denials.

## Coverage and false-confidence control

A zero-diff shadow window proves only `no observed difference within the observed contexts and evidence envelope`. It does not prove equivalence. Coverage should be reasoned over dimensions relevant to the policy graph, for example:
- capability/consequence class;
- principal/account/device class;
- evidence state: current/stale/gapped/contradicted/unknown;
- exception/break-glass states;
- policy/runtime/SW generation;
- online/offline/reconnect state;
- recovery/bootstrap path;
- browser/device cohort when client state affects prerequisites.

Rare recovery paths should be exercised with fixtures/tabletop/isolated validation rather than waiting for production traffic.

Track D may measure observed-context coverage, but absence in analytics is not proof that a context cannot occur.

## Rollout gates

Generic promotion gates before candidate authority:
- structural/schema validation passes;
- no unresolved critical prerequisite cycle;
- required recovery/bootstrap entry path remains valid;
- known permit expansions are explicitly reviewed by consequence;
- new restrictions affecting recovery/data preservation are explicitly reviewed;
- evaluator errors/UNKNOWN semantics are understood;
- representative differential fixtures pass;
- shadow coverage is adequate for common paths, with rare critical paths validated separately;
- rollback/forward-fix path is itself authorized and tested at the generic level;
- stale/offline client compatibility horizon is explicit rather than assumed.

No universal sample count, percentage or duration is asserted.

## Bounded authoritative rollout

When architecture permits, candidate authority should expand by a bounded dimension that can be identified and reversed: environment, internal/test cohort, account cohort, capability, region or other product-appropriate boundary. The chosen boundary must not accidentally split a transaction/recovery invariant across policy generations.

Security-sensitive rollout differs from ordinary feature flags:
- the flag/control plane itself is authority-bearing;
- cohort assignment must be authenticated where it changes authorization;
- clients cannot self-select a weaker generation;
- rollback cannot resurrect a generation whose trust/key/revocation assumptions have become invalid;
- old and new decisions during partial rollout must not create cross-generation privilege escalation.

## Rollback is a security transition, not a file restore

A candidate defect may justify rollback, but predecessor restoration is safe only if predecessor assumptions remain valid. If the candidate was deployed because the predecessor had a security defect or trust epoch was retired, simple rollback can re-open the original vulnerability.

Possible outcomes:
- **SAFE ROLLBACK** — predecessor remains authorized/current for the affected scope;
- **FORWARD FIX REQUIRED** — predecessor is no longer safe/compatible;
- **BOUNDED CONTAINMENT** — keep affected authority gated while recovery policy is repaired;
- **MANUAL RECOVERY** — if neither generation has a valid automated recovery edge.

`known-good operationally ≠ still-authorized cryptographically/security-wise`.

## PWA / Service Worker / EFB application

Policy generation, server evaluator generation, served application generation and physical Service Worker/runtime generation are separate state.

For a long-offline company iPad:
- do not include it in `candidate compatible` merely because online shadow traffic shows no diff;
- explicitly fixture supported stale runtime/SW generations and reconnect states;
- preserve local data/read/export where product semantics allow if candidate rejects remote mutation;
- require candidate policy to preserve a bounded bootstrap/revalidation path for supported stale generations;
- if a client is beyond the supported compatibility horizon, stop at truthful local preservation/manual recovery rather than silently selecting an older permissive policy;
- never allow the PWA to self-assert cohort/policy generation to obtain weaker server authorization.

Actual Safari/WebKit/MDM/storage/background behavior remains OPEN until physical/project evidence exists.

## Cross-track transfer

### Track A — Platform & Browser
Own observable SW/runtime/browser/storage generation facts and the mechanics of stale-client activation/reconnect. Supply cohort facts; do not define authorization.

### Track B — UX / IA
Own truthful rollout/revalidation/recovery presentation. A candidate-policy denial must distinguish temporary revalidation, unsupported client and manual recovery without claiming local data loss.

### Track C — Performance / Accessibility / Quality
Own differential fixture suites, shadow-vs-authoritative isolation tests, policy-generation fault injection, rollout/rollback regression tests and accessible degraded/recovery state validation.

### Track D — Search / Discovery / Analytics
Own privacy-aware diagnostic aggregation for decision-diff frequency/coverage. Analytics cannot authorize rollout, prove impossible contexts, or clear security gates.

### Track E — Owner
Own candidate/predecessor lineage, consequence classification, promotion gates, authoritative rollout boundary, rollback authorization and recovery-path preservation.

## MINTTAP DECISION — minimal sufficient rollout model

If implemented for MintTap/LogMate-like systems:
1. version policy semantics and evaluator/runtime generation explicitly;
2. validate candidate structure and prerequisite graph before runtime comparison;
3. maintain curated destructive/boundary fixtures for critical capabilities;
4. run candidate shadow evaluation without enforcement authority;
5. diff decision + determining basis + errors, not just boolean outcome;
6. classify permit expansion, new restriction, basis change, recovery regression and stale-client incompatibility separately;
7. require explicit review of authority expansion and recovery-path loss regardless of raw frequency;
8. use bounded authoritative rollout when feasible;
9. keep client-local generation/cohort claims non-authoritative;
10. treat rollback as an authenticated policy transition and use forward-fix/containment when predecessor is no longer safe.

No production policy engine, cohort, threshold, traffic sample, compatibility horizon or WebKit behavior is asserted.

## VALIDATION — 40-case campaign

1. invalid syntax rejected; 2. schema mismatch rejected; 3. prerequisite cycle rejected; 4. recovery edge regression detected; 5. identical permit decisions/basis; 6. identical deny decisions/basis; 7. deny→permit classified expansion; 8. permit→deny classified restriction; 9. same decision/different determining policy classified basis change; 10. evaluator error delta retained; 11. UNKNOWN semantic delta retained; 12. shadow permit cannot affect authoritative deny; 13. shadow deny cannot block authoritative permit; 14. shadow outage leaves predecessor authoritative; 15. shadow cannot mutate trust state; 16. shadow telemetry cannot clear gate; 17. one critical reset expansion blocks promotion despite low frequency; 18. many benign denials do not numerically hide critical expansion; 19. common-path zero diff does not mark rare recovery path covered; 20. fixture exercises break-glass; 21. fixture exercises stale evidence; 22. fixture exercises contradictory evidence; 23. fixture exercises expired exception; 24. supported stale SW can bootstrap/revalidate; 25. unsupported stale SW reaches local-preservation/manual state; 26. client cannot self-select predecessor policy; 27. client cannot forge rollout cohort; 28. partial rollout preserves transaction invariant; 29. old/new generation cross-request cannot escalate privilege; 30. rollout event and policy generation provenance retained; 31. candidate evaluator version mismatch detected; 32. policy-language/runtime upgrade included in diff scope; 33. canary healthy but offline compatibility regression still blocks full promotion; 34. rollback to still-safe predecessor succeeds; 35. rollback to retired vulnerable predecessor rejected; 36. forward-fix path works while authority remains bounded; 37. stale backup cannot restore old policy authority; 38. long-offline iPad spans several generations and enters revalidation without data deletion; 39. accessible UX exposes local-available/sync-gated/manual-recovery truth; 40. end-to-end candidate rollout with permit expansion + stale client + recovery-path change halts safely without shadow authority or unnecessary local-data loss.

## CONTRADICTION / failure-mode analysis

### Validation theater
A schema-valid policy can be semantically wrong for the product.

### Shadow-authority theater
A `dry run` path that can affect enforcement is not shadow evaluation.

### Zero-diff theater
No observed differences can mean insufficient coverage, not equivalence.

### Count-based safety theater
Diff percentages can hide one catastrophic authority expansion.

### Canary theater
Healthy online canary users do not represent long-offline PWA clients or rare recovery states.

### Rollback theater
Restoring yesterday's policy text does not prove yesterday's trust assumptions are still authorized.

### Client-cohort theater
Allowing a stale client to request the old policy generation turns compatibility into downgrade authority.

## OPEN

Actual MintTap/LogMate policy engine, decision context schema, authorization server, policy-language/runtime, rollout tooling, cohort mechanism, traffic/evidence retention, compatibility horizon, Service Worker strategy, managed-iPad fleet, recovery plane and consequence taxonomy remain unknown. Production rollout semantics are not claimed.

## CHANGE WATCH

- Authorization engine/language semantics and validation behavior can change; pin and test the actual runtime generation.
- Provider eventual-consistency behavior can affect rollout observation and must be verified if a managed policy service is used.
- Safari/WebKit/MDM lifecycle and stale-client behavior require current Track A evidence and physical validation.
- Product capability/recovery topology changes require refreshing differential fixtures and rollout gates.

## Gate result

**PASS (generic).** The Web Manager can now distinguish policy structural validation, fixture differential testing, non-authoritative shadow evaluation and bounded authoritative rollout; classify decision diffs by consequence; preserve recovery/stale-client paths; and treat rollback as a security transition rather than configuration restore.

Product/provider/managed-iPad/policy-runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA policy rollout cohort integrity, cross-generation transaction consistency & split-policy convergence.** Partial rollout can leave requests/devices/transactions evaluated under different policy generations. The next bottleneck is preventing client-controlled cohort downgrade, cross-generation privilege escalation and non-atomic multi-step operations while still permitting bounded rollout and long-offline PWA convergence.