# 223 — PWA Assurance-Debt Dependency Graphs, Transitive Blast-Radius Proof & Safe Partial Reauthorization

Status: **PASS (generic) / PRODUCT + DEPENDENCY-GRAPH + POLICY-ENGINE + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline mechanics; Track B restricted/recovery UX; Track C destructive validation; Track D dependency/debt telemetry.  
Dependencies: 117–137, 171–222, especially 218–222 distributed enforcement, witness/quorum, emergency authority and assurance-debt governance.

## Problem
222 established that unresolved assurance debt should constrain the capability it actually affects, but that a narrow label is not proof of a narrow blast radius. The adjacent problem is transitivity. A debt apparently attached to one API, region, key or provider may propagate through shared identity, signing roots, policy evaluators, telemetry/evidence planes, deployment authority, recovery paths, Service Worker/update channels or data stores. Conversely, one unresolved debt must not become a reason to shut down every safe local/offline capability when there is evidence that some capability lies outside the affected trust path.

Central rule: **partial reauthorization is a positive proof problem. A capability may resume only when its complete consequence-bearing dependency cut is known enough, affected/unknown dependencies are excluded or bounded, current authority is reacquired, and the exact operation is re-admitted under current policy. Absence of an observed path from debt to capability is not proof of independence.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker control, cached policy, storage, secure context, browser session state and delayed reconnect are graph nodes/edges, not independent authority.
- **B UX/IA/Content:** very high dependency pressure. Must expose capability-specific states such as local-save available / remote-sync blocked / recovery pending without implying global health.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **536 → 544 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can measure graph coverage, unknown edges, debt fan-out and reauthorization outcomes; telemetry cannot prove graph completeness or grant authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns dependency semantics, blast-radius derivation, trust-cut proof, partial reauthorization gates and re-expansion governance.

## SOURCE

### NIST CSF 2.0 — risk governance includes supply-chain/dependency concerns
NIST CSF 2.0 is current final guidance and explicitly increases emphasis on governance and cybersecurity supply-chain risk management. Its outcomes are intentionally non-prescriptive: organizations identify, assess, prioritize and communicate cybersecurity risk rather than treating a component inventory as a complete architecture proof.

Sources:
- https://doi.org/10.6028/NIST.CSWP.29
- https://www.nist.gov/cyberframework

**TRANSFER VALIDATION:** CSF does not define a MintTap dependency graph or partial-reauthorization algorithm. It supports treating external/internal dependencies and governance as part of risk reasoning rather than assuming product boundaries equal failure boundaries.

### NIST SP 1305 — supplier requirements and C-SCRM are explicit governance work
NIST SP 1305 (final, October 2024) uses CSF 2.0's GV.SC category to establish and operate cybersecurity supply-chain risk management and communicate supplier requirements.

Source:
- https://csrc.nist.gov/pubs/sp/1305/final

**TRANSFER VALIDATION:** provider/vendor identity is a dependency dimension, but different vendors do not prove independent identity, control plane, PKI, DNS, cloud, library or operator failure domains.

### NIST SP 800-207 / 800-207A — authorization depends on identities and policy enforcement, not location alone
NIST Zero Trust Architecture removes implicit trust based merely on network location/ownership; SP 800-207A applies granular application/service identity policy enforcement across multi-location/cloud environments.

Sources:
- https://doi.org/10.6028/NIST.SP.800-207
- https://doi.org/10.6028/NIST.SP.800-207A

**TRANSFER VALIDATION:** these publications do not prescribe MintTap debt propagation. They support evaluating actual identity/policy/enforcement dependencies instead of inferring trust from region, subnet, device ownership or UI surface.

### NIST SP 800-53A Rev.5 — assessment evidence is distinct from the control claim
SP 800-53A Rev.5 remains current assessment guidance and provides procedures for assessing security/privacy controls.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** a diagram or declared dependency boundary is not sufficient evidence that the boundary is effective. Runtime/administrative evidence is required where the claim depends on implementation.

## SYNTHESIS 1 — model dependencies by consequence, not component names
A useful assurance graph needs typed nodes and edges. Candidate node classes include capability/operation, authority/policy, identity/credential/key/trust root, evaluator, enforcement point, deployment/update path, provider/control plane, storage/data, evidence/witness/collector, recovery/PITR, network/name-resolution dependency and client/browser state.

Edges should describe why compromise/uncertainty can propagate: `authorizes`, `verifies`, `deploys`, `configures`, `stores`, `observes`, `recovers`, `inherits`, `controls-update-of`, `shares-admin-plane-with`, `shares-root-with`, or `depends-on-for-currentness`.

`same product ≠ same blast radius`; `different component name ≠ different failure domain`; `graph node exists ≠ relevant edge modeled`.

## SYNTHESIS 2 — debt propagation is claim-specific
Debt does not automatically taint every downstream object. Propagation depends on the assurance claim being made.

Example: uncertainty about analytics collector integrity may invalidate a fleet-convergence assurance claim without invalidating cryptographically authenticated local flight-record bytes. Conversely, compromise of an update-signing or policy-authority root can affect many apparently unrelated capabilities because the same root can change their code or authorization rules.

Represent debt as `D -> claim/control/authority -> affected capability` rather than as a global red flag. Preserve UNKNOWN where edge relevance cannot be resolved.

`dependency exists ≠ every claim depends on it`; `data unaffected ≠ authority unaffected`; `telemetry compromised ≠ underlying event proven false`.

## SYNTHESIS 3 — blast radius is the reachable consequence-bearing subgraph under explicit edge semantics
Compute/inspect transitive reachability only across edge types relevant to the debt claim. Then challenge the result for missing shared roots and hidden recovery paths.

A declared blast radius is credible only with:
1. a versioned graph denominator/scope;
2. provenance for material nodes/edges;
3. explicit unknown/unreachable dependencies;
4. transitive traversal rules tied to the claim;
5. challenge evidence for shared roots/control planes;
6. runtime/administrative validation where reading cannot settle the edge.

`no known path ≠ proven no path`; `one-hop review ≠ transitive blast-radius review`; `inventory complete enough for operations ≠ graph complete enough for every assurance claim`.

## SYNTHESIS 4 — prove safe partial reauthorization with an unaffected trust cut
For capability C, define the minimal consequence-bearing dependency set/cut needed to authorize and execute C under current policy. Partial reauthorization requires evidence that every mandatory element in that cut is current and acceptable, and that affected/unknown dependencies are not able to mutate or authorize C through an alternate path.

The proof must include negative-path questions: can the compromised key still sign an accepted policy? can a stale provider console bypass the current gateway? can PITR resurrect old authority? can an old Service Worker invoke a legacy endpoint? can shared IAM/admin credentials reconfigure the supposedly isolated path?

`healthy direct path ≠ safe capability if alternate authority path remains`; `primary enforcement current ≠ bypass path extinct`.

## SYNTHESIS 5 — reauthorization is operation-specific and current-policy based
Do not restore an entire account/device/region because one capability's cut is proven. Reauthorize the specific operation/capability and maintain restrictions elsewhere.

Queued offline operations are re-admitted, not grandfathered. A write created when old authority was valid is data/provenance to preserve; whether it may mutate remote state now is decided by current policy, current identity and current dependency assurance.

`capability A reauthorized ≠ capability B reauthorized`; `queued while authorized ≠ authorized on replay`; `device healthy ≠ every queued operation admissible`.

## SYNTHESIS 6 — shared roots dominate apparent isolation
Particularly dangerous transitive roots include shared SSO/IAM, DNS/registrar, CI/CD credentials, signing keys, KMS/HSM administration, cloud organization/root account, policy database/evaluator, package/update pipeline, MDM, recovery/PITR authority, observability/evidence store and human emergency authority.

Two regions/providers may be runtime-isolated yet share a root that can rewrite both. Partial reauthorization must reason about these administrative/control dependencies, not only request/data flow.

`separate runtime ≠ separate authority`; `multi-region ≠ independent control plane`; `different provider ≠ independent identity/recovery`.

## SYNTHESIS 7 — unknown edges constrain claims without forcing unnecessary data loss
When a material edge is UNKNOWN, do not relabel it unaffected merely to restore service. But the restriction should target the consequence-bearing capability dependent on that edge.

For a LogMate-like PWA, an unknown remote-sync authorization dependency can justify `LOCAL DATA ENTRY/PRESERVATION AVAILABLE; REMOTE MUTATION BLOCKED`. It need not destroy or prevent capture of unique flight data when local capture itself does not rely on the uncertain remote authority.

`UNKNOWN edge ≠ safe edge`; `UNKNOWN remote authority ≠ local unique data must be discarded`; `restricted sync ≠ app globally unusable`.

## SYNTHESIS 8 — dependency graphs themselves drift and need provenance
A graph can become stale when providers, libraries, IAM, deployment paths, Service Worker routes, recovery procedures or organization roles change. Attach source/provenance and observed generation to material edges; trigger review on architecture/release/provider/recovery changes.

Graph freshness is not a timestamp alone. A recently regenerated graph from an incomplete source remains incomplete.

`graph generated today ≠ graph current`; `CMDB current ≠ runtime dependency current`; `static architecture diagram ≠ executable dependency evidence`.

## SYNTHESIS 9 — re-expansion after partial recovery is monotonic only with evidence
Recovery can proceed capability by capability, but each expansion must preserve prior restrictions unless new evidence closes them. Do not let one successful partial recovery become an implicit global NORMAL transition.

A useful state progression is `BLOCKED -> DATA-PRESERVED/RESTRICTED -> PARTIALLY-READMITTED -> NORMAL`, with debt items and evidence attached to each transition. A later contradiction can demote the affected capability again without rewriting prior evidence.

`partial recovery succeeded ≠ incident globally closed`; `one green operation ≠ dependency cut proven`; `NORMAL label ≠ all debt extinct`.

## SYNTHESIS 10 — offline PWA return is a graph reconciliation event
A long-offline iPad returns carrying cached code/Service Worker, local data, credentials, policy generation, schema/evaluator assumptions and queued operations. These are multiple graph nodes at potentially different epochs.

Preserve unique local data first. Then reacquire current authenticated policy and required runtime/schema/verifier state; reject extinct authority; evaluate the current dependency cut for each consequence-bearing operation; re-admit safe operations and retain blocked operations with reason/provenance. Do not treat network reconnection as graph convergence.

`online again ≠ dependency graph reconciled`; `Service Worker updated ≠ authority/currentness graph reconciled`; `data migrates ≠ operation reauthorized`.

## MINTTAP DECISION / DIRECTION
1. Model assurance debt against a typed, versioned dependency graph rather than a flat capability label.
2. Derive blast radius using claim-specific transitive edges and preserve UNKNOWN/unreachable dependencies.
3. Require positive evidence for an unaffected trust cut before partial reauthorization; absence of observed compromise is insufficient.
4. Include alternate/bypass/recovery/update/admin paths in the cut, not only primary request flow.
5. Reauthorize specific capabilities/operations under current policy; never grandfather queued offline work.
6. Preserve safe local/offline data capture when remote authority is unresolved and the local capability's dependency cut remains outside the affected trust path.
7. Treat shared identity, signing, deployment, provider-admin, recovery and evidence roots as potential transitive blast-radius multipliers.
8. Version/provenance the dependency graph and review it on material architecture/release/provider/recovery changes.
9. Keep partial recovery, incident closure and systemic corrective-control closure separate.
10. Keep these as generic directions until canonical MintTap/LogMate runtime/topology evidence exists.

## OPEN / DEPENDENCY
- Actual MintTap/LogMate capability/dependency graph and edge provenance: **OPEN**.
- Actual identity/provider/key/policy/evaluator/deployment/recovery/evidence topology: **OPEN**.
- Actual alternate/bypass paths and enforcement-set denominator: **OPEN**.
- Managed-iPad/iPadOS/WebKit/MDM/Service Worker/offline behavior: **Track A + Software Engineering runtime dependency**.
- Capability-specific degraded/recovery UX: **Track B consuming Design Studio; human/accessibility validation OPEN**.
- Legal/aviation/safety consequence boundaries: **OPEN**.

## Track C destructive campaign — 536 → 544 defined cases
Add:
1. **Hidden shared IAM root:** two apparently isolated capabilities share an IAM/admin root compromised by the debt; one is incorrectly reauthorized based only on separate runtime paths.
2. **One-hop blast-radius truncation:** review checks direct dependencies but misses a transitive signing/update dependency that can mutate the capability.
3. **Missing-edge false safety:** dependency graph omits provider-console bypass; `no path found` is treated as proof of independence.
4. **Healthy primary / stale alternate:** current gateway rejects retired authority but a recovery/legacy endpoint still accepts it.
5. **Queued-operation grandfathering:** offline write created under old policy is replayed after reconnect without current per-operation admission.
6. **Graph rollback after PITR:** production recovery restores an older dependency graph that predates a shared-root discovery and narrows blast radius incorrectly.
7. **Partial-recovery laundering:** one safe read-only capability succeeds and system promotes the entire account/region to NORMAL including unresolved mutation paths.
8. **Long-offline iPad mixed epochs:** device returns with current user identity but stale Service Worker/policy/schema and queued writes; unique data is preserved while each remote operation waits for current dependency-cut proof.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** browser/offline state supplies dependency nodes and epoch mechanics; cached state does not create authority.
- **Track B:** state communication must be capability-specific; a reassuring global banner must not hide unresolved remote authority.
- **Track C:** dependency-cut, alternate-path, PITR and mixed-epoch claims require executable evidence before product PASS.
- **Track D:** graph/debt telemetry can reveal drift/fan-out/recurrence but cannot prove completeness or authorize recovery.
- **Design Studio:** Web remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/iPadOS/EFB and canonical-product runtime remain OPEN.

## Persistent guards added
`same product ≠ same blast radius`; `different component name ≠ different failure domain`; `graph node exists ≠ relevant edge modeled`; `dependency exists ≠ every claim depends on it`; `data unaffected ≠ authority unaffected`; `no known path ≠ proven no path`; `one-hop review ≠ transitive blast-radius review`; `healthy direct path ≠ safe capability if alternate authority path remains`; `primary enforcement current ≠ bypass path extinct`; `capability A reauthorized ≠ capability B reauthorized`; `queued while authorized ≠ authorized on replay`; `separate runtime ≠ separate authority`; `multi-region ≠ independent control plane`; `UNKNOWN edge ≠ safe edge`; `restricted sync ≠ app globally unusable`; `graph generated today ≠ graph current`; `static architecture diagram ≠ executable dependency evidence`; `partial recovery succeeded ≠ incident globally closed`; `online again ≠ dependency graph reconciled`.

## Gate result
**223 PASS (generic).** The knowledge gate closes because typed dependency semantics, claim-specific transitive propagation, blast-radius proof boundaries, unaffected trust-cut requirements, alternate-path analysis, operation-specific reauthorization, unknown-edge handling, graph drift/provenance, partial-recovery progression and offline mixed-epoch reconciliation now have explicit evidence boundaries and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**224 — dependency-graph discovery completeness, hidden-control-plane detection & executable cut-set validation**: determine how to build and challenge the graph from independent configuration/runtime/evidence sources, detect undeclared control/recovery/update paths, quantify unknown coverage without claiming impossible absolute completeness, and convert a proposed unaffected trust cut into executable negative/positive validation across provider, recovery and offline-PWA paths.