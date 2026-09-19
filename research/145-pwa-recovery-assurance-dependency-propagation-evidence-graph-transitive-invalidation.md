# 145 — PWA Recovery-Assurance Dependency Propagation, Evidence-Graph Consistency & Transitive Invalidation

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + EVIDENCE-GRAPH RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A browser/PWA generations; Track B degraded/blocked UX; Track C evidence provenance/validation; Track D bounded telemetry; studies 120–144, especially 127–129 and 143–144.

## Why this study exists

144 established semantic evidence freshness and explicit invalidation triggers. The unresolved problem is propagation. If an IdP, signing key, recovery provider, custody path, browser generation or managed-device policy changes, which claims become stale? Invalidating too little leaves stale green assurance; invalidating everything creates expensive blanket revalidation and eventually trains operators to ignore the system.

The useful abstraction is a small **typed evidence/dependency graph**, not a heavyweight GRC platform.

## SOURCE

### Continuous monitoring must preserve visibility into changing system/control state
NIST SP 800-137 defines information-security continuous monitoring as providing visibility into assets, threats/vulnerabilities and deployed-control effectiveness, with information sufficient to respond when observations indicate controls are inadequate. Its process is iterative rather than a one-time certification.

Source: https://doi.org/10.6028/NIST.SP.800-137

NIST SP 800-137A provides a methodology for assessing continuous-monitoring programs; this supports treating monitoring quality itself as assessable rather than assuming collected status is automatically trustworthy.

Source: https://doi.org/10.6028/NIST.SP.800-137A

### Assessment evidence is scoped and structured, not a timeless Boolean
NIST OSCAL's Assessment Results model represents assessment scope, activities, observations/evidence, findings and risks and supports both periodic and continuous assessments. This is useful transfer evidence for keeping claim/evidence/scope relationships explicit.

Source: https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/

### Provenance systems bind outputs to inputs/dependencies by reference
SLSA v1.2 Build Provenance records resolved dependencies that influenced an artifact, while the current draft Dependency Provenance model records per-ingestion attestations and composes release inventories by reference. This is software-supply-chain evidence, not a PWA recovery specification, but it provides a useful structural lesson: dependency claims should be explicit and referential rather than flattened into one opaque status.

Sources:
- https://slsa.dev/spec/v1.2/build-provenance
- https://slsa.dev/spec/draft/dependency-provenance

## SYNTHESIS — typed graph, bounded propagation

Represent material assurance state with typed nodes and edges.

### Minimal node classes
- **CLAIM** — e.g. `lost-device recovery cannot lower trust floor`;
- **EVIDENCE** — drill/result/attestation/inspection supporting or contradicting a claim;
- **DEPENDENCY** — IdP, key/trust epoch, provider, custody path, browser/WebKit generation, Service Worker generation, MDM policy, recovery API;
- **EXCEPTION** — bounded accepted deviation from a claim/control;
- **POLICY/GENERATION** — versioned rule set against which evidence was evaluated;
- **ENVIRONMENT/SCOPE** — production/staging, managed iPad, browser family, account/device class.

### Minimal edge semantics
- `EVIDENCE SUPPORTS CLAIM`;
- `EVIDENCE CONTRADICTS CLAIM`;
- `CLAIM DEPENDS_ON DEPENDENCY`;
- `EVIDENCE OBSERVED_UNDER DEPENDENCY/ENVIRONMENT/POLICY`;
- `EXCEPTION NARROWS/WAIVES CLAIM`;
- `CLAIM REQUIRES CLAIM` where one assurance claim logically depends on another;
- `SUPERSEDES` only where a newer object actually replaces the older object's current-decision role.

Do not use an untyped generic `related_to` edge for invalidation decisions.

## Propagation rule

A dependency change first invalidates or narrows **evidence whose validity envelope explicitly depended on that dependency**. Current claim state is then recomputed from remaining applicable evidence, contradictions, required prerequisite claims and exceptions.

This is intentionally different from recursively marking every reachable node `FAIL`.

Persistent guards:
- `dependency changed ≠ every downstream claim failed`;
- `dependency changed ≠ unaffected evidence stale`;
- `evidence invalidated ≠ historical evidence deleted`;
- `supporting evidence invalidated ≠ claim proven false`;
- `one supporting edge remains ≠ claim fully assured`;
- `graph reachable ≠ semantically dependent`;
- `new evidence exists ≠ old contradiction disappears`;
- `dependency restored ≠ old evidence automatically revalidated`.

### Recompute states, do not mutate history into failure
If an IdP generation changes, evidence collected under the old IdP may become `INVALIDATED-BY-CHANGE` for current assurance while remaining a truthful historical record. The claim can become `REVALIDATION-DUE`, `PARTIAL/BOUNDED`, `UNKNOWN` or remain `CURRENT-VERIFIED` if independent applicable evidence still covers the claim. It becomes `CONTRADICTED` only when evidence actually contradicts it.

## Dependency closure without false transitivity

Not every dependency relation is transitive in the same way.

Example:
- Recovery Claim R depends on Approval Claim A.
- A was tested with IdP generation I1.
- I1 changes to I2.

The I1 evidence for A is invalidated. A is recomputed. R is affected only because R explicitly requires A's current assurance, not merely because I1 is somewhere upstream in a generic graph.

Therefore transitive propagation follows **typed semantic edges** and claim prerequisites, not raw graph reachability.

`A depends on B` and `B observed under C` does not automatically mean every property of A depends on every property of C.

## Graph consistency rules

### Orphans
A current assurance claim with no applicable supporting evidence is not green. A current evidence item with unknown subject/scope/policy provenance is `UNKNOWN/PARTIAL`, not silently attached by label similarity.

`orphan evidence exists ≠ claim supported`.

### Cycles
Cycles are not automatically invalid: two operational claims can legitimately interact. But **circular assurance** is invalid when A is considered verified only because B is verified and B only because A is verified, with no independent evidence/root premise.

`cycle exists ≠ defect`; `cycle is sole proof basis ≠ assurance`.

Detect strongly connected prerequisite components and require at least one independently evidenced/rooted basis for current assurance.

### Contradictions
A newer PASS does not erase a prior FAIL unless the changed condition and scope explain why the contradiction is resolved. Preserve both evidence objects and record the resolution relation/rationale.

`latest evidence wins ≠ contradiction resolved`.

### Supersession
Supersession is scoped. A new Safari/iPadOS drill can supersede the current-decision role of an older equivalent drill for that environment, but does not erase historical provenance or supersede Chromium evidence for a different environment.

## MINTTAP DECISION — minimum viable assurance graph

Do not build a general-purpose GRC graph database now. A small app company can implement the model with ordinary records/tables/documents if needed later.

Minimum durable fields:

`nodeId | type | claim/control | scope | generation/environment | state | provenance | observedAt | invalidators | owner`

and typed edges:

`fromId | edgeType | toId | scope/condition | createdAt | provenance`

Required operations are modest:
1. register/change a material dependency generation;
2. find directly affected evidence by explicit edge;
3. mark that evidence invalidated/bounded without deleting it;
4. recompute affected claims through typed prerequisite edges;
5. surface UNKNOWN/CONTRADICTED/EXCEPTION states;
6. enqueue targeted revalidation;
7. preserve an audit trail of propagation and later normalization.

No universal technology choice or production schema is asserted.

## Change-event handling

For each material change event:
1. authenticate/validate the event source where required;
2. identify exact dependency identity + old/new generation;
3. query direct evidence dependencies;
4. apply the evidence validity rule for that dependency/claim type;
5. recompute directly supported claims;
6. propagate only across typed `REQUIRES` relations;
7. stop when downstream state does not change or no semantic prerequisite edge exists;
8. create targeted revalidation tasks;
9. preserve event, propagation result and unresolved uncertainty.

A missed change event remains a major weakness. Periodic reconciliation from 143/144 remains the backstop.

## Cross-track transfer

### Track A — Platform & Browser
Own precise identity of platform generations that can invalidate claims: Service Worker deployment generation, browser/WebKit behavior, storage lifecycle and managed-device state where verified. Do not claim a browser upgrade is material to every recovery claim; declare the dependency only where mechanics matter.

### Track B — UX / IA
Consume recomputed states. Present `revalidation required`, `scope not assessed`, `local data preserved / remote write blocked`, contradiction and exception states without exposing graph internals to ordinary users. Operator UX should show why a claim changed and what evidence is required next.

### Track C — Quality
Own scenario/evidence IDs, environment, repetitions and targeted regression selection. The graph should make selective retesting possible: a WebKit generation change should select relevant physical-iPad/Safari scenarios, not unrelated server-only tests.

### Track D — Analytics
Telemetry can generate a candidate change/anomaly event but cannot define dependency truth, close contradictions or authorize risk acceptance. Instrumentation itself is a dependency for telemetry claims.

### Track E — Owner
Own graph semantics, material-dependency taxonomy, propagation rules, exception interaction, contradiction resolution requirements and assurance decision state.

## PWA / EFB application

For a company iPad that has been offline across several epochs, current server recovery evidence may remain valid while device-path evidence becomes bounded/unknown because WebKit, Service Worker, MDM or trust-policy generations differ. Conversely a server IdP change should not automatically invalidate a purely local IndexedDB export-format test unless that test actually relied on the IdP.

This supports the operational principle:

`targeted invalidation + preserved local data + gated remote authority`.

Do not infer direct unattended device sync, background execution, persistent storage, managed-iPad installability or transport capability from this graph model. Those remain separate platform/product validation.

## VALIDATION — 30-case campaign

1. IdP I1→I2 invalidates only I1-bound approval evidence; 2. unrelated local export evidence stays current; 3. signing-key epoch change selects signature-verification claims; 4. WebKit generation change selects physical-iPad scenarios; 5. Service Worker generation change selects cache/update claims; 6. MDM policy change selects managed-device claims; 7. provider API change selects provider-bound recovery evidence; 8. custody-owner departure invalidates custody evidence; 9. direct evidence invalidation recomputes one prerequisite claim; 10. prerequisite degradation propagates to dependent recovery claim; 11. graph reachability without typed dependency does not propagate; 12. two independent evidence items, one invalidated, claim remains bounded/current if coverage is sufficient; 13. sole evidence invalidated makes claim unknown/due, not false; 14. contradictory FAIL remains visible after new PASS; 15. contradiction resolution requires scoped rationale; 16. orphan evidence cannot support claim; 17. orphan claim cannot remain green; 18. circular A↔B with no independent evidence is rejected as circular assurance; 19. cycle with independent evidence is evaluated normally; 20. superseded evidence retained historically; 21. imported stale assurance graph cannot lower current dependency generation; 22. backup restore cannot resurrect superseded green state; 23. exception edge expires and claim recomputes; 24. compensating-control evidence invalidates transitively only where exception relies on it; 25. analytics anomaly creates review trigger but not automatic FAIL; 26. missed provider-change event is caught by periodic reconciliation; 27. duplicate change event is idempotent; 28. partial propagation interruption resumes without double-invalidating history; 29. long-offline iPad reconnect crosses multiple dependency generations and receives targeted revalidation; 30. full change→direct invalidation→claim recompute→targeted validation→new evidence→normalization preserves provenance end to end.

## CONTRADICTION / failure-mode analysis

A dependency graph can itself create false precision. Missing edges produce stale green assurance; over-broad edges produce blanket invalidation; cycles can manufacture circular confidence; stale graph state can become worse than a simple explicit UNKNOWN. Therefore graph completeness is never assumed.

Use reconciliation and uncertainty states:
- unknown dependency provenance → do not infer an edge;
- material claim with unexplained evidence basis → flag for graph review;
- dependency inventory change with zero affected evidence → investigate whether that is legitimate or a missing-edge symptom;
- unexpectedly huge invalidation fan-out → investigate over-broad edge semantics before accepting it as correct.

## OPEN

Actual MintTap/LogMate evidence store, dependency identities/generations, IdP/provider topology, Service Worker deployment model, WebKit/MDM fleet, account/device model, claim taxonomy, exception workflow, runtime event sources, graph storage, propagation implementation and consequence thresholds are unknown. No production PASS is claimed.

## CHANGE WATCH

- NIST OSCAL and continuous-monitoring guidance evolve; preserve source/version in any implementation mapping.
- SLSA draft Dependency Track is explicitly draft and is transfer evidence only; do not treat its current schema as stable PWA architecture.
- Browser/WebKit/MDM/provider behavior remains change-sensitive and requires platform/provider-specific evidence after selection.

## Gate result

**PASS (generic).** The Web Manager can now propagate assurance changes through typed dependencies without confusing invalidation with failure, preserve historical evidence, detect orphan/circular/contradictory graph conditions, and select targeted revalidation rather than blanket retesting.

Production, managed-EFB and evidence-graph runtime assurance remain **OPEN**.

## Next highest-value adjacent question

**PWA assurance-graph change-event authenticity, missed-event detection & reconciliation integrity.** Dependency propagation only works if the graph receives trustworthy change events and periodically detects drift between recorded dependency generations and real provider/browser/deployment/custody state. The next bottleneck is preventing forged events from causing denial-of-service invalidation, missed events from preserving stale green assurance, and reconciliation itself from becoming an over-privileged oracle.