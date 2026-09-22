# 220 — PWA Convergence-Attestation Quorum, Witness Diversity Degradation & Emergency Assurance Modes

Status: **PASS (generic) / PRODUCT + QUORUM-POLICY + WITNESS-TOPOLOGY + DISTRIBUTED-ENFORCEMENT + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline mechanics; Track B degraded-assurance UX; Track C destructive validation; Track D assurance telemetry.  
Dependencies: 122–137, 171–219 and prior authority/currentness/recovery/evidence work.

## Problem
219 established that enforcement point, witness, collector and independent attestor are distinct trust roles, and that authentic contradictory evidence cannot be averaged away. The adjacent question is how multiple corroborators may legitimately close a convergence claim. A naive `2 of 3 green` rule fails when the three observations share one credential, source, administrator, cloud account or collector; a simple majority can also suppress one authentic red witness that identifies a materially dangerous stale path.

Central rule: **a convergence quorum is a policy over claims, failure domains, evidence freshness and contradiction state—not a count of signatures. Missing or correlated assurance may lower confidence or restrict capabilities; it does not create authorization. Emergency availability must use an explicitly narrower assurance mode, never an implicit quorum bypass.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Offline/cached state and reconnect timing affect evidence freshness but do not define quorum semantics.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `corroborated`, `degraded`, `contradicted`, `emergency-restricted`, and `data preserved / sync blocked` states while consuming Design Studio evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **512 → 520 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures diversity, witness age, contradiction, quorum health and emergency-mode duration; analytics cannot grant authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns quorum policy, failure-domain model, contradiction veto/handling, assurance-mode transition and restoration gates.

## SOURCE

### NIST IR 8214 / NIST threshold-cryptography program — threshold numbers depend on a system/adversary model
NIST IR 8214 describes threshold schemes as achieving a security goal despite compromise of some components, and explicitly treats threshold type, platform, interfaces, setup/maintenance and security tradeoffs as characterizing properties. NIST's threshold-cryptography project likewise frames distribution of trust as avoiding a single critical operator.

Sources:
- https://doi.org/10.6028/NIST.IR.8214
- https://csrc.nist.gov/projects/threshold-cryptography
- https://csrc.nist.gov/pubs/ir/8214/c/final

**TRANSFER VALIDATION:** these sources concern cryptographic threshold schemes, not MintTap convergence telemetry. They are bounded precedent for the principle that `k-of-n` has meaning only relative to component independence, adversary/failure assumptions and lifecycle rules. They do not prescribe MintTap's quorum number.

### NIST SP 800-207 / SP 800-207A / SP 1800-35 — policy decision and distributed enforcement remain explicit
Zero Trust Architecture removes implicit trust based on location/ownership and requires explicit authentication/authorization. SP 800-207A and SP 1800-35 show policy decisions enforced through distributed application/service enforcement points.

Sources:
- https://doi.org/10.6028/NIST.SP.800-207
- https://doi.org/10.6028/NIST.SP.800-207A
- https://csrc.nist.gov/pubs/sp/1800/35/final

**TRANSFER VALIDATION:** degraded observation does not erase the authorization/enforcement boundary. These publications do not define MintTap's witness quorum or emergency assurance policy.

### RFC 9162 / RFC 9943 — authentic evidence may conflict; transparency does not establish truth
RFC 9162's split-view threat shows why multiple valid signed views may still conflict and require comparison. RFC 9943 separates signed statements from transparency receipts; registration/auditability does not make the underlying statement true.

Sources:
- https://www.rfc-editor.org/rfc/rfc9162.html
- https://www.rfc-editor.org/rfc/rfc9943.html

**TRANSFER VALIDATION:** a majority of authentic green statements cannot automatically erase a materially scoped authentic red statement. Exact conflict policy is product/risk dependent.

## SYNTHESIS 1 — quorum eligibility precedes quorum arithmetic
Before counting an observation toward quorum, determine whether it is eligible for the claim:
1. identity and key/currentness valid;
2. evidence fresh enough for the capability and threat window;
3. correct endpoint/capability/policy generation tested;
4. denominator membership known;
5. collector/attestor lineage current;
6. required failure-domain independence satisfied;
7. no unresolved substitution/replay/fork condition invalidates the observation.

`three signatures ≠ three eligible votes`; `eligible vote ≠ independent vote`.

## SYNTHESIS 2 — diversity is a vector, not a vendor count
Model independence across dimensions relevant to the claim: credential/root of trust, raw telemetry source, policy publisher, collector database, deployment/admin plane, cloud/provider/account, network path, codebase/library, personnel/recovery authority and time/checkpoint source.

Two witnesses can be independent for one failure class and correlated for another. Therefore quorum policy should name the failure assumptions it is intended to tolerate rather than attach a universal weight to a service.

`different vendor ≠ independent failure domain`; `different credential ≠ independent telemetry source`; `2-of-3 ≠ tolerate one compromise unless the assumed compromise domains are actually separated`.

## SYNTHESIS 3 — weights cannot manufacture independence
Weighted quorum can express consequence or confidence, but assigning two logical votes to one correlated source does not create another failure domain. A high weight may be justified for a stronger evidence class; it cannot transform shared-root observations into independent corroboration.

`weight 2 ≠ two failure domains`; `more dashboards ≠ more assurance`.

## SYNTHESIS 4 — contradiction policy is separate from quorum threshold
A quorum rule needs an explicit contradiction policy. For high-consequence claims such as retired-authority extinction, a fresh authentic red witness from an in-scope endpoint should normally prevent `CORROBORATED-CURRENT` closure until it is resolved, excluded by authenticated denominator change, or proven invalid under the evidence policy.

This is not the same as allowing any untrusted red signal to veto service indefinitely. Eligibility and provenance are checked first.

`majority green ≠ authentic red resolved`; `red exists ≠ red is eligible`; `quorum met numerically ≠ closure safe`.

## SYNTHESIS 5 — quorum is claim- and capability-specific
A read-only public-content availability claim and a remote mutation/authority-extinction claim need not require the same corroboration. Define quorum policy against a named claim and consequence class. Avoid one global `system healthy` quorum.

Possible assurance classes, without fixing product numbers:
- low-consequence/read-only: unilateral current evidence may be acceptable;
- consequence-bearing mutation: stronger corroboration and contradiction handling;
- authority/recovery/security-floor transition: highest independence and negative predecessor evidence.

Exact thresholds remain **OPEN** pending product topology and risk evidence.

## SYNTHESIS 6 — witness-diversity degradation is an assurance event
If one independent path fails, remaining enforcement can still be correct while assurance becomes weaker. Preserve distinct states:
- **CORROBORATED** — required diversity/threshold met;
- **DEGRADED-CORROBORATION** — current evidence exists but diversity requirement is not met;
- **PARTIAL/UNKNOWN** — evidence or denominator incomplete;
- **CONTRADICTED/FORKED** — eligible evidence conflicts;
- **EMERGENCY-RESTRICTED** — explicitly authorized bounded capability mode under reduced assurance.

Do not relabel degraded corroboration as normal simply because service is available.

`assurance lost ≠ enforcement lost`; `enforcement appears healthy ≠ assurance restored`.

## SYNTHESIS 7 — emergency assurance mode is not emergency authorization creation
Availability pressure can justify a predesigned reduced-assurance mode only if authority for that mode already exists under current emergency policy. The mode should bind:
- triggering evidence and reason;
- permitted capability subset;
- explicitly prohibited capabilities;
- scope/cohort/region;
- expiry/termination condition;
- required monitoring and evidence capture;
- recovery/normalization owner;
- post-event review/debt.

If the normal quorum is unavailable, that fact alone does not authorize the emergency mode.

`quorum unavailable ≠ emergency permission`; `monitoring degraded ≠ policy absent`; `emergency mode active ≠ baseline rewritten`.

## SYNTHESIS 8 — fail-open/fail-closed is too coarse for offline-first PWA
A LogMate-like PWA can preserve useful local work while blocking consequence-bearing remote operations. Emergency assurance therefore should be capability-shaped rather than globally open/closed:
- preserve/create unique local records where local safety policy permits;
- allow read-only access to already trusted local data where appropriate;
- queue remote work with explicit pending state;
- block remote mutation, authority change, destructive reconciliation or trust reset when current admission assurance is insufficient;
- export/recovery only under separately defined capability policy.

`remote sync blocked ≠ local data entry blocked`; `offline utility ≠ offline global authority`.

## SYNTHESIS 9 — emergency transitions require monotonic evidence and an exit gate
Record NORMAL→DEGRADED→EMERGENCY-RESTRICTED transitions as security-relevant state changes. Expiry must not depend only on a potentially uncertain wall clock; bind policy generation/sequence and authenticated termination where architecture permits. Returning to NORMAL requires restored quorum/diversity, contradiction resolution, current policy/evaluator state and negative tests for any temporary/stale authority introduced during the incident.

`service recovered ≠ assurance recovered`; `collector returned ≠ diversity restored`; `emergency ended ≠ temporary authority extinct`.

## SYNTHESIS 10 — partitioned regions cannot each spend the same missing assurance
If a network partition leaves two regions each with partial corroborators, neither branch should independently promote itself to full quorum by treating unreachable witnesses as implicitly green. Emergency capability must be bounded by policy established before or independently of the partition, and reconciliation must preserve branch evidence.

`unreachable vote ≠ abstention that lowers denominator`; `partition ≠ threshold automatically shrinks`; `two local quorums ≠ one global quorum unless policy/failure assumptions explicitly support it`.

## SYNTHESIS 11 — quorum policy itself is versioned security logic
Quorum membership, eligibility, weights, contradiction rules, diversity requirements and emergency transitions must have authenticated versioning and anti-rollback treatment. A stale quorum policy can be as dangerous as stale authorization policy.

`current witnesses + stale quorum rule ≠ current assurance`; `policy update published ≠ all collectors evaluate new quorum semantics`.

## SYNTHESIS 12 — closure statements include diversity and degraded tail
A defensible closure statement names: claim/capability, enforcement-set revision, quorum-policy version, eligible witness set, relevant independence dimensions, freshness window, contradictions, unreachable tail and emergency mode if any. Avoid `3/3 green` without describing what the three represent.

## MINTTAP DECISION / DIRECTION
1. Treat quorum as **claim-specific security policy**, not a dashboard count.
2. Evaluate eligibility and failure-domain independence before threshold arithmetic.
3. Do not let weights or vendor count manufacture independence.
4. Preserve eligible contradictory evidence outside ordinary majority aggregation.
5. Model witness-diversity loss as an assurance degradation, not implicit permission.
6. Predefine any emergency reduced-assurance mode as a bounded capability policy with explicit entry/exit evidence; missing quorum alone never grants it.
7. For LogMate-like offline PWA operation, preserve unique local data while blocking consequence-bearing remote actions when current admission assurance is insufficient.

These are generic directions, not claims about current MintTap/LogMate architecture.

## OPEN / DEPENDENCY
- Exact MintTap/LogMate quorum topology, witness membership, failure domains, weights and thresholds: **OPEN**.
- Exact emergency/degraded capability policy and risk classification: **OPEN**.
- Whether current products use independent attestors or signed currentness witnesses: **OPEN**.
- Exact iPadOS/WebKit/background/storage/MDM behavior: **Track A + Software Engineering runtime dependency**.
- Degraded/emergency operator and pilot UX: **Track B consuming Design Studio; human/accessibility validation OPEN**.
- Legal/aviation/safety constraints on degraded offline operation: **OPEN**.

## Track C destructive campaign — 512 → 520 defined cases
Add:
1. **Pseudo-quorum:** three green collectors share one credential/database and incorrectly satisfy `2-of-3`.
2. **Weight inflation:** one strong collector is assigned weight 2 and treated as two independent failure domains.
3. **Majority launders contradiction:** two green witnesses outvote one fresh authentic red witness for the exact stale provider path.
4. **Diversity collapse:** one independent path fails; system continues to label assurance `CORROBORATED` rather than degraded.
5. **Dynamic denominator shrink:** partition makes a witness unreachable and evaluator silently lowers `2-of-3` to `2-of-2`.
6. **Emergency-by-outage:** collector outage alone activates remote mutation without pre-existing emergency authority.
7. **Stale quorum-policy rollback:** witnesses are current G12 but restored evaluator applies old permissive quorum policy Q9.
8. **Long-offline iPad during degraded quorum:** unique data is preserved, local safe capability remains usable, but consequence-bearing sync does not resume until current admission assurance is restored.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** browser/offline state can explain evidence delay but cannot lower security quorum.
- **Track B:** degraded/emergency states require clear, accessible status and recovery guidance without a user-controlled security bypass.
- **Track C:** quorum independence, partition, rollback and emergency-mode transitions require executable validation; reading is not runtime PASS.
- **Track D:** metrics may report quorum/diversity health but cannot redefine eligibility or suppress contradiction.
- **Design Studio:** Web remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/EFB and exact-product runtime remain OPEN.

## Persistent guards added
`three signatures ≠ three eligible votes`; `eligible vote ≠ independent vote`; `different vendor ≠ independent failure domain`; `weight 2 ≠ two failure domains`; `majority green ≠ authentic red resolved`; `quorum met numerically ≠ closure safe`; `assurance lost ≠ enforcement lost`; `quorum unavailable ≠ emergency permission`; `emergency mode active ≠ baseline rewritten`; `remote sync blocked ≠ local data entry blocked`; `service recovered ≠ assurance recovered`; `unreachable vote ≠ denominator reduction`; `partition ≠ threshold automatically shrinks`; `current witnesses + stale quorum rule ≠ current assurance`.

## Gate result
**220 PASS (generic).** The knowledge gate closes because quorum eligibility, failure-domain diversity, weighting limits, contradiction handling, assurance degradation, emergency capability shaping, partition behavior, policy versioning and offline-PWA consequences now have explicit evidence boundaries and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**221 — quorum-policy authority, emergency-mode abuse resistance & assurance-debt closure**: determine who may change quorum/diversity requirements, prevent incident-time threshold weakening from self-authorizing, separate emergency activation from policy authorship, preserve evidence when emergency mode persists, and prove temporary assurance debt/authority is retired before normal operation is declared.