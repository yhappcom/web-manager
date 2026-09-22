# 239 — PWA Dependency-Graph Reconciliation Conflicts, Authoritative-Source Hierarchy & Safe Topology Repair

Status: **PASS (generic) / PRODUCT + GRAPH-RECONCILIATION + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/client evidence; Track B conflict/containment UX; Track C destructive validation; Track D reconciliation observability.  
Dependencies: 223–238, especially hidden-dependency discovery, drift/currentness, contradiction intake, corroboration independence and graph-poisoning resistance.

## Problem
238 established that the dependency graph is evidence, not truth: it can be authentic yet incomplete, stale or semantically wrong. The next failure is reconciliation. IaC may declare two independent services while provider enumeration shows a shared project; IAM/PAM may reveal one recovery administrator across both; MDM may claim a trust package is retired while a returning iPad still presents the old generation; audit evidence may disagree with runtime behavior. A naive `source of truth` hierarchy lets a compromised nominal authority overwrite contradictory evidence. A naive union of all observations preserves false/stale edges forever and can cause unnecessary global containment.

Central rule: **source authority is field-, scope-, generation-, time- and failure-hypothesis-specific. Reconciliation must preserve contradictory provenance, distinguish desired/declared/observed/effective state, and repair topology through evidence-backed supersession rather than silent overwrite. No source wins globally merely because it is called authoritative.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Runtime/browser/device evidence can establish what one client actually received or exercised, but cannot by itself establish management/provider topology.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `DEPENDENCY-CONFLICT`, `RECONCILIATION-PENDING`, `TOPOLOGY-REPAIRED-PENDING-VALIDATION` and bounded degraded states while preserving user tasks/data.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight reconciliation/topology-repair destructive cases; campaign expands **664 → 672 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures conflict age, unresolved high-consequence edges, source concentration, repair/revalidation latency and recurring divergence; telemetry does not decide truth.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns source fitness, conflict classification, consequence cuts, topology repair, supersession lineage and reclosure criteria.

## SOURCE

### NIST SP 800-53 / 800-53A — inventories should reflect systems and be reconciled through lifecycle change evidence
NIST SP 800-53 CM-8 requires a system component inventory that accurately reflects the system and is reviewed/updated. CM-8(1) ties updates to installation, removal and system updates. SP 800-53A assesses inventory through multiple potential evidence objects including inventories, reviews/update records, change-control records and installation/removal records.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final
- https://www.nist.gov/news-events/news/2025/08/nist-revises-security-and-privacy-control-catalog-improve-software-update

**TRANSFER VALIDATION:** inventory accuracy is maintained through lifecycle evidence, not by declaring one database infallible. This is precedent for reconciliation, not a MintTap topology prescription.

### NIST SP 800-61 Rev.3 — incident analysis integrates multiple observations; correlation is not authority voting
NIST finalized SP 800-61 Rev.3 in April 2025, superseding Rev.2. It integrates incident detection/analysis/response/recovery into cybersecurity risk management. Multiple-source correlation is analysis input, not a rule that the nominal system of record automatically defeats contradictory runtime evidence.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

### NIST SP 800-18 Rev.2 — lifecycle system planning supports environment/component/data-flow context
NIST finalized SP 800-18 Rev.2 on 2026-06-30. Current RMF material describes machine-readable system planning and lifecycle risk decisions spanning system context.

Sources:
- https://csrc.nist.gov/projects/risk-management
- https://csrc.nist.gov/pubs/sp/800/18/r2/final

**TRANSFER VALIDATION:** structured system context supports topology reconciliation, but a planning artifact remains declared evidence and can diverge from runtime reality.

## SYNTHESIS 1 — there is no universal authoritative-source hierarchy
Authority must be scoped to the claim. Examples:
- IaC/configuration may be strongest for **intended** topology at a specific revision;
- provider enumeration may be strongest for provider-visible **current objects**;
- IAM/PAM may be strongest for configured administrative/recovery reach;
- MDM may be strongest for declared fleet assignment;
- a physical/client runtime observation may be strongest for what that client **actually received or executed**;
- an independent audit export may preserve historical evidence when a live control plane changes.

None of these proves every other dimension. `authoritative for field X ≠ authoritative for topology Y`.

## SYNTHESIS 2 — separate desired, declared, observed and effective state
A useful reconciliation model records at least:
1. **desired** — policy/IaC says what should exist;
2. **declared** — provider/MDM/IAM control plane reports what it believes exists;
3. **observed** — audit/runtime/client evidence records what was seen;
4. **effective** — consequence tests show what can actually authorize/control/reach the operation.

Conflict between these layers is evidence. Do not collapse them into one mutable `current topology` row before investigation.

Persistent guards: `desired ≠ deployed`; `declared ≠ observed`; `observed ≠ effective authority`.

## SYNTHESIS 3 — source fitness is claim-specific and adversary-aware
For each conflicting assertion evaluate:
- exact field/object/generation scope;
- observation time and freshness;
- provenance/authenticity;
- directness to the consequence;
- known blind spots;
- whether the source shares the suspected failure domain;
- whether it can self-edit both state and evidence;
- whether another plane can independently challenge it.

A provider-admin API should not win a dispute about provider-admin compromise merely because it is normally authoritative for provider objects.

Persistent guard: `nominal source of record compromised or in-scope ≠ privileged arbiter of its own correctness`.

## SYNTHESIS 4 — conflicts need taxonomy before repair
Classify disagreement rather than overwrite it:
- **TEMPORAL** — observations are valid at different times;
- **GENERATION/IDENTITY** — same alias names different objects/generations;
- **SCOPE** — sources describe different layers or subsets;
- **SEMANTIC** — fields/edges mean different things;
- **PROPAGATION** — desired change has not converged;
- **OBSERVATION-LAG** — audit/telemetry is delayed;
- **UNMODELED-DEPENDENCY** — one source reveals a missing edge;
- **POTENTIAL-COMPROMISE/POISONING** — disagreement cannot be explained safely.

Only after classification should topology be repaired.

## SYNTHESIS 5 — repair is append/supersede, not silent mutation
Topology repair should preserve:
- original assertions and provenance;
- conflict record and affected consequence cut;
- investigation/corroboration evidence;
- repair decision and authority;
- successor graph version;
- explicit supersession/tombstone relation;
- required negative/positive revalidation;
- residual blind spots.

A corrected graph must not erase why the old graph was wrong. `graph repaired ≠ contradictory evidence deleted`.

## SYNTHESIS 6 — union and intersection are both unsafe generic reconciliation rules
Taking the union of every observed edge can preserve stale/fabricated dependencies indefinitely and unnecessarily deny service. Taking the intersection can delete real dependencies seen by only one source. Majority voting has the same weakness as prior corroboration counting.

Use claim-specific provenance and consequence tests. Where uncertainty can change a high-consequence independence/authority judgment, downgrade to `DEPENDENCY-CONFLICT` / `INSUFFICIENT-INDEPENDENCE` and apply narrow reversible containment.

## SYNTHESIS 7 — topology repair needs effective-state validation
A repair is not complete because the graph document changed. Validate the consequence boundary. Examples:
- after removing an old recovery-admin edge, prove the retired principal can no longer satisfy recovery/admission;
- after splitting two paths, demonstrate the relevant fault hypothesis no longer collapses both;
- after MDM trust-package retirement, returning clients must not regain consequence authority merely by presenting the old package;
- after provider migration, stale restore/PITR paths must not reintroduce the retired dependency.

Persistent guard: `graph edit complete ≠ topology repair effective`.

## SYNTHESIS 8 — conflict containment is consequence-partitioned
A conflict over recovery authority need not disable demonstrably independent local read/capture/export. A conflict over the only writer/admission path may require stronger restriction. The containment boundary follows the uncertain dependency cut, not the graph file as a whole.

States:
- `RECONCILED-CURRENT` — conflict resolved with current evidence and effective-state validation;
- `DEPENDENCY-CONFLICT` — material sources disagree;
- `RECONCILIATION-PENDING` — investigation/corroboration active;
- `TOPOLOGY-REPAIRED-PENDING-VALIDATION` — successor graph recorded but consequence oracle incomplete;
- `INSUFFICIENT-INDEPENDENCE` — separation cannot be established;
- `PRECAUTIONARY-CONTAINMENT` — bounded reversible restriction for affected consequences.

## SYNTHESIS 9 — repair authority must be separate from topology truth
Someone or some workflow needs permission to publish a successor graph, but that governance authority does not make its factual assertions true. Conversely, a runtime contradiction can reopen a published graph without itself becoming policy authority.

`authorized to repair graph ≠ graph facts proven`; `runtime contradiction ≠ runtime client may rewrite policy`.

## SYNTHESIS 10 — PWA/EFB reconciliation must preserve stale-client evidence and user data
A long-offline LogMate-like iPad may contradict MDM/provider claims: MDM says trust generation G19 is universal while the device returns with G12; backend inventory says old authority retired while a queued operation still reaches an old acceptance path. Preserve unique flight/logbook data and the stale artifact. Do not reset the iPad to make inventory converge.

Treat the device as an observation bound to its old graph/authority epoch. Quarantine consequence-bearing replay, bootstrap current trust, reconcile server/MDM/runtime evidence, then re-admit operations individually under current authority. Exact physical iPadOS/WebKit/MDM behavior remains OPEN.

## SYNTHESIS 11 — recurring conflicts are evidence about the discovery/control system
If the same dependency repeatedly disappears from the graph after repair, the issue is not just one bad edge. Investigate collector scope, identity normalization, provider API coverage, IaC drift, MDM reporting, change-event loss or adversarial suppression. Track D may measure recurrence and latency, but metrics cannot close the defect.

## SYNTHESIS 12 — source hierarchy itself is versioned configuration
Even a carefully defined field-level source-precedence matrix can become stale after provider migration, organizational change, new MDM, IAM federation or collector redesign. Record its version and revalidate when control ownership changes. Never embed an eternal `IaC > provider > runtime` ordering.

Persistent guard: `source-precedence policy current once ≠ current forever`.

## MINTTAP DECISION
For future MintTap/LogMate dependency reconciliation, use **claim-scoped source fitness plus provenance-preserving supersession**, not a universal source-of-truth hierarchy. Preserve desired/declared/observed/effective layers. A material conflict remains explicit until its cause is classified and the affected consequence is validated against the repaired topology.

If the nominal authoritative plane is itself within the suspected failure domain, do not let it self-clear the conflict. Use independent evidence where available or downgrade assurance and contain only the affected consequence cut. This is generic guidance, not a claim that MintTap or LogMate currently implements such reconciliation.

## DEPENDENCY / TRANSFER
- **Track A:** provide exact runtime/browser/device facts and generation identity; do not generalize one client observation into fleet/provider topology.
- **Track B:** make conflict/reconciliation/degraded states understandable and preserve user data/task continuity; consume Design Studio evidence for interaction treatment.
- **Track C:** own destructive tests for wrong-source precedence, silent overwrite, stale-edge resurrection and repaired-topology effective-state validation.
- **Track D:** measure conflict age/recurrence/source concentration/revalidation latency without deciding authority.
- **Software Engineering:** graph schema, typed assertions, reconciliation engine, identity normalization and fault-injection implementation are implementation-level handoffs once canonical product/source authorization exists.

## CONTRADICTION / FAILURE MODES
1. **IaC-wins laundering:** compromised/stale IaC says paths are independent while provider/IAM evidence shows a shared recovery administrator; system silently trusts IaC.
2. **Provider self-clear:** suspected provider-admin plane reports no shared dependency and is allowed to close its own conflict.
3. **Runtime-overreach:** one client sees old trust material and rewrites global topology rather than opening scoped contradiction.
4. **Union trap:** stale/fabricated edges are unioned forever, causing permanent unnecessary containment.
5. **Intersection trap:** a real dependency visible to only one source is discarded because other sources omit it.
6. **Silent repair:** graph row is overwritten, destroying contradictory provenance and preventing later review.
7. **Paper repair:** successor graph removes an edge but retired authority still succeeds at the consequence boundary.
8. **Offline iPad convergence destruction:** device is reset to match MDM inventory, deleting unique local data/evidence before reconciliation.

## Track C destructive additions — 664 → 672 defined cases
Add eight cases corresponding to the failure modes above. Required oracle behavior:
- preserve source-specific assertions and provenance;
- classify rather than silently overwrite conflicts;
- refuse universal source precedence when the source is within the suspected failure domain;
- bound containment to affected consequences;
- require effective-state negative/positive validation after repair;
- preserve unique offline client data and stale-epoch evidence;
- retain supersession lineage;
- keep topology publication authority separate from factual truth.

**VALIDATION:** these are **defined cases**, not execution PASS. Product reconciliation engine, provider/IAM/PAM/MDM sources, physical iPad/iPadOS/WebKit and runtime validation remain OPEN.

## OPEN
- Actual MintTap/LogMate desired/declared/observed/effective topology sources and reconciliation schema are unknown.
- Actual provider/IAM/PAM/MDM/IaC/audit failure domains and source fitness are unknown.
- Exact conflict severity thresholds, containment cuts and revalidation SLAs require product consequence evidence.
- Physical iPadOS/WebKit/MDM stale-client behavior remains unvalidated.
- Legal/aviation/safety requirements may impose stronger evidence retention or approval requirements.

## CHANGE WATCH
- NIST SP 800-53 Release 5.2.0 remains current as of this study; provider-specific inventory/configuration APIs remain change-sensitive.
- NIST SP 800-61 Rev.3 remains current final incident-response guidance.
- NIST SP 800-18 Rev.2 is final as of 2026-06-30.
- Browser/OS PWA and MDM behavior remains platform/provider-specific; physical iPad validation remains required before product claims.

## Gate judgment
**PASS (generic).** The adjacent generic competency is closed when Web Manager can explain why no source is universally authoritative, distinguish desired/declared/observed/effective topology, classify conflicts, preserve contradictory provenance, publish successor topology without erasing lineage, validate repair at the consequence boundary, partition containment and apply the model to long-offline managed-iPad PWA evidence without inventing production facts.

Production certification is not claimed.
