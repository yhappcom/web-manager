# 240 — PWA Topology-Repair Authorization, Dual Governance & Repair-Race/Rollback Resistance

Status: **PASS (generic) / PRODUCT + GOVERNANCE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A generation/runtime evidence; Track B repair/degraded-state UX; Track C destructive validation; Track D governance/revalidation observability.  
Dependencies: 223–239, especially proof races, monotonic admission floors, anti-rollback/fork recovery, contradiction/corroboration, graph currentness and provenance-preserving topology repair.

## Problem
239 established that topology repair is append/supersede, not silent overwrite, and that authorization to publish a graph does not prove its facts. The next risk is the repair mechanism itself. A compromised operator, automation identity or stale workflow can use legitimate repair privilege to publish a convenient topology that hides a dependency. Two individually valid repair proposals can race and overwrite one another. A stale but correctly signed graph can be replayed after a newer repair. Dual approval can become theater if both approvers share one identity/recovery/admin failure domain. Long-offline PWA clients can miss several graph transitions and later attempt to rejoin using obsolete trust/topology assumptions.

Central rule: **topology repair is a governed, versioned state transition over evidence—not an administrator edit. Approval authorizes publication, not factual truth. High-consequence repair requires separation appropriate to the threat model, optimistic/concurrency guards, monotonic anti-rollback state and effective-state validation. Offline clients consume authenticated successor lineage; they do not vote on or roll back global topology.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Supplies exact client graph/authority epoch and runtime acceptance observations; cannot authorize topology repair.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `REPAIR-PROPOSED`, `APPROVAL-PENDING`, `REPAIR-CONFLICT`, `REPAIR-PUBLISHED-PENDING-VALIDATION`, `BOOTSTRAP-REQUIRED` and bounded degraded states while preserving user data/tasks.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight repair-governance/race/rollback destructive cases; campaign expands **672 → 680 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures repair age, superseded-proposal recurrence, approval concentration, rollback rejection and validation latency; telemetry never grants approval or factual truth.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns repair capability, separation/dual authorization policy, proposal lineage, compare-and-swap semantics, anti-rollback floor, emergency handling and closure criteria.

## SOURCE

### NIST SP 800-53 Release 5.2.0 — separation of duties and configuration change control
NIST SP 800-53 Rev.5 AC-5 requires organizations to identify duties requiring separation and define access authorizations supporting that separation. NIST's glossary describes separation of duty as preventing one user from holding enough privilege to misuse a system alone; dynamic separation can use a two-person rule. NIST also describes configuration control as protecting systems from improper modifications before, during and after implementation. CM-3 is the configuration-change-control family precedent; SP 800-171 Rev.3 likewise separates duties and calls out configuration change control, including testing/validation/documentation as related control structure.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/glossary/term/Separation_of_Duty
- https://csrc.nist.gov/glossary/term/two_person_control
- https://csrc.nist.gov/glossary/term/configuration_control
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html

**TRANSFER VALIDATION:** separation/dual authorization is a bounded precedent for high-consequence topology publication. NIST does not prescribe a universal MintTap `2-of-N` topology-repair quorum; actual thresholds and roles require product threat/consequence evidence.

### TUF — threshold roles, versioned root transitions and rollback resistance
The Update Framework (TUF) root metadata defines trusted keys and a signature threshold for top-level roles. TUF update metadata includes versions and expiry; root update processing is explicitly versioned, and rollback protection rejects older metadata. This is useful precedent for successor authority, threshold authorization and monotonic client state.

Sources:
- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/overview/
- https://theupdateframework.io/spec/

**TRANSFER VALIDATION:** TUF secures software-update metadata, not MintTap dependency graphs. We transfer the principles of threshold roles, sequential/versioned successor state and rollback resistance—not its exact role model or protocol.

## SYNTHESIS 1 — repair capability is a separate privilege
Do not let ordinary graph ingestion, collector administration, evidence-store administration or runtime operators automatically publish successor topology. Define distinct capabilities such as:
- propose repair;
- attach/corroborate evidence;
- approve high-consequence repair;
- publish successor graph;
- validate effective state;
- invoke emergency containment/recovery.

A person or service may hold more than one capability only when the threat model permits it. `can edit graph storage ≠ authorized to publish topology`; `can approve repair ≠ can manufacture evidence`.

## SYNTHESIS 2 — two-person governance is useful only when the two persons are meaningfully separated
Dual authorization reduces single-principal abuse only if the approvers are distinct for the relevant failure hypothesis. Two human accounts recovered by one IAM administrator, two approvals executed through one compromised privileged workstation, or an operator plus automation controlled by the same credential are not automatically independent.

Do not hard-code `2-of-2` or `2-of-3` as universal policy. Select separation/threshold based on consequence, emergency availability requirements and correlated-failure analysis.

Persistent guards: `two approvals ≠ two independent failure domains`; `two signatures ≠ two independent judgments`.

## SYNTHESIS 3 — approval authorizes a transition; it does not prove topology facts
An approved proposal may still contain wrong or incomplete edges. Preserve:
- proposal ID and base graph generation;
- asserted changes and affected consequence cuts;
- evidence/provenance references;
- proposer/approver identities and policy version;
- approval times and independence assumptions;
- successor generation;
- required effective-state validation.

`governance signature valid ≠ topology assertion true`; `policy-compliant approval ≠ effective-state validation PASS`.

## SYNTHESIS 4 — use compare-and-swap semantics for concurrent repairs
A proposal should target an explicit base graph generation/hash. Publication succeeds only if the expected base is still current or the proposal is explicitly rebased/reconciled against intervening changes. If P240-A and P240-B both target G20, and A publishes G21 first, B must not blindly publish its old full snapshot over G21.

Safe outcomes include:
- reject B as stale and require rebase;
- automatically merge only if a formally defined, consequence-safe operation proves non-conflict;
- open `REPAIR-CONFLICT` for human/system reconciliation.

Persistent guards: `approved against G20 ≠ approved against G21`; `different fields ≠ independent consequences`.

## SYNTHESIS 5 — successor graph generations require monotonic anti-rollback state
A validly signed old graph is still old. Clients/control planes need a trusted currentness floor or authenticated successor lineage so an attacker cannot replay G18 after G24. A rollback request is itself a new forward transition—e.g. G25 whose content intentionally restores a prior edge—not permission to reinstall G18 as current.

`content rollback ≠ generation rollback`; `signature valid ≠ generation current`; `emergency rollback ≠ bypass anti-rollback floor`.

## SYNTHESIS 6 — do not make approval policy itself timeless
Approval roles, thresholds and separation assumptions are versioned governance state. Organizational changes, IAM federation, provider migration, PAM redesign or emergency-role changes can invalidate the independence assumptions behind an old policy.

A repair proposal records the governance-policy generation under which it was approved. A proposal waiting across a material governance change must be re-evaluated before publication.

`proposal approved once ≠ approval current forever`; `same approver names ≠ same custody/recovery graph`.

## SYNTHESIS 7 — emergency repair must be bounded, visible and repay assurance debt
An emergency may justify faster containment or a narrower approval path when availability/safety consequences demand it, but emergency privilege must not become a permanent single-admin repair bypass. Record scope, reason, expiry/review condition and required post-event independent validation. Preserve monotonic graph generation even during emergency transitions.

If normal approval independence is unavailable, degrade only affected consequences where possible and explicitly create assurance debt. Do not silently lower the threshold and call the resulting graph normally governed.

## SYNTHESIS 8 — validation authority should challenge publication authority
Where practical, the party/path validating that the repaired topology actually changes the consequence boundary should not be identical to the publisher's only evidence source. Examples:
- published removal of a recovery edge → negative test that retired principal cannot satisfy recovery;
- provider migration → restore/PITR test cannot resurrect retired authority;
- MDM trust transition → stale device package cannot regain consequence authority.

This is not a demand for a separate organization for every test. It is a demand to avoid self-certifying the exact failure hypothesis under investigation.

## SYNTHESIS 9 — long-offline PWA clients need successor lineage, not graph voting
A LogMate-like iPad may leave at graph G18 and return after G19→G24. Preserve unique flight/logbook data and the device's stale evidence. The client must not force server topology back to G18 because its local state is authentic. Nor should the server erase the device to obtain superficial convergence.

Rejoin sequence:
1. preserve unique local data and graph/authority epoch;
2. quarantine consequence-bearing replay;
3. authenticate current successor graph/trust basis or enter `BOOTSTRAP-REQUIRED` if the supported bridge is missing;
4. migrate worker/schema/policy as required;
5. re-admit queued operations individually under current policy;
6. retain contradictions that reopen server/fleet claims.

Exact physical iPadOS/WebKit/MDM behavior remains OPEN.

## SYNTHESIS 10 — repair history must distinguish supersession from rejection
A proposal can be `PROPOSED`, `APPROVAL-PENDING`, `APPROVED-NOT-PUBLISHED`, `SUPERSEDED`, `REJECTED`, `REPAIR-CONFLICT`, `PUBLISHED-PENDING-VALIDATION`, `EFFECTIVE-CURRENT`, or `REOPENED`. Do not delete stale/rejected proposals: they can explain later contradictions or attempted laundering.

A proposal superseded because its base changed is not necessarily factually false. A rejected proposal is not automatically malicious. State semantics matter for incident review.

## SYNTHESIS 11 — rollback/fork resistance spans publisher and consumers
It is insufficient for the central graph store to reject older generations if a stale verifier, cache, restore environment, offline client or disaster-recovery copy can still accept an older graph as current. Anti-rollback testing therefore covers:
- primary publication store;
- cached/verifier state;
- backup/PITR restore;
- offline/bootstrap client paths;
- emergency/admin tools;
- deployment automation.

A restore that contains G18 may be valid historical data but must reacquire current floor/successor state before consequence-bearing rejoin.

## SYNTHESIS 12 — availability pressure must not silently collapse governance
If one approver is unavailable, the system must not reinterpret `two-person required` as `one available person is enough`. Predefine degraded/emergency authority and consequence partitioning. Availability can motivate a governed emergency transition; it cannot retroactively change what the normal threshold meant.

Persistent guard: `required approver unavailable ≠ threshold satisfied`.

## MINTTAP DECISION
For future MintTap/LogMate dependency-topology repair, treat publication as a **versioned governed transition**. Separate proposal, approval, publication and validation capabilities where the consequence model warrants it. High-consequence changes use separation/dual authorization chosen from actual threat/failure-domain analysis, not a universal fixed quorum.

Every proposal binds to an explicit base graph generation and governance-policy generation. Stale concurrent proposals fail closed into rebase/reconciliation rather than overwriting newer state. Currentness is monotonic: intentional content rollback is published as a new generation. Approval proves authorization only; effective-state tests close the factual/consequence claim.

This is generic direction, not a claim that MintTap or LogMate currently implements these mechanisms.

## DEPENDENCY / TRANSFER
- **Track A:** expose exact graph/trust epoch and runtime acceptance; do not authorize global repair from client state.
- **Track B:** design comprehensible approval/conflict/bootstrap/degraded states without exposing security theater or deleting user data; consume Design Studio interaction evidence.
- **Track C:** own concurrency, rollback, correlated-approver, stale-client and effective-state destructive validation.
- **Track D:** measure repair/approval/validation latency and concentration without deciding truth or quorum.
- **Software Engineering:** typed proposal state machine, compare-and-swap publication, signatures/threshold implementation, immutable/superseding lineage and fault injection are implementation handoffs once canonical product authorization exists.

## CONTRADICTION / FAILURE MODES
1. **Single-admin laundering:** one privileged operator proposes, approves and publishes removal of the edge that would expose their own shared dependency.
2. **Dual-approval monoculture:** two accounts approve, but both depend on the same IAM/PAM recovery/admin path relevant to the threat.
3. **Stale approved overwrite:** proposals A and B target G20; A publishes G21, then B blindly overwrites with its G20-based snapshot.
4. **Signed rollback replay:** attacker presents valid old G18 after G24 and consumer accepts it because signature validity is checked without currentness.
5. **Governance-policy drift:** proposal remains pending across role/threshold/recovery changes but publishes under obsolete approval assumptions.
6. **Emergency bypass persistence:** temporary single-principal emergency path becomes ordinary standing repair privilege.
7. **Self-validation:** publisher's own control plane is the only oracle proving the repaired edge no longer exists.
8. **Offline-iPad rollback pressure:** authentic G18 device state is allowed to roll global graph/trust state backward, or device is erased to force convergence.

## Track C destructive additions — 672 → 680 defined cases
Add eight cases corresponding to the failure modes above. Required oracle behavior:
- reject unauthorized/single-principal laundering where policy requires separation;
- evaluate approver independence against the relevant failure hypothesis;
- bind proposals to explicit base and governance generations;
- reject/reconcile stale concurrent publication;
- reject validly signed graph rollback below current floor;
- expire/re-evaluate approval after material governance change;
- bound emergency authority and require post-event validation;
- preserve offline unique data while preventing stale client authority rollback.

**VALIDATION:** these are **defined cases**, not execution PASS. Product governance schema, identities/PAM, graph store, provider/MDM, physical iPad/iPadOS/WebKit and runtime execution remain OPEN.

## OPEN
- Actual MintTap/LogMate repair roles, consequence classes, approval thresholds and emergency policy are unknown.
- Actual IAM/PAM/recovery failure domains and whether two-person governance is warranted for each change class are unknown.
- Actual graph-store concurrency primitive, signature/threshold mechanism and trusted currentness floor are unknown.
- Physical iPadOS/WebKit/MDM stale-client/bootstrap behavior remains unvalidated.
- Legal/aviation/safety obligations may require stronger approval, retention or audit controls.

## CHANGE WATCH
- NIST SP 800-53 Release 5.2.0 remains current as of this study; organizational tailoring determines actual separation/configuration controls.
- TUF specification and implementations remain maintained; use as update-security precedent, not as a MintTap protocol dependency.
- Provider IAM/PAM/MDM and browser/OS PWA behavior remain provider/platform-specific and require current validation.

## Gate judgment
**PASS (generic).** The adjacent competency is closed when Web Manager can separate repair capability from evidence truth; explain when dual authorization helps and when correlated approval makes it theater; bind repair to base/governance generations; prevent stale concurrent overwrite and signed rollback; model emergency authority without permanent bypass; validate repaired effective state; and safely rejoin a long-offline PWA client without global rollback or local-data destruction.

Production certification is not claimed.