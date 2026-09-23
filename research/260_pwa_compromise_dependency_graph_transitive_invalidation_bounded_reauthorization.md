# 260 — PWA Compromise Dependency-Graph Reconstruction, Closure-Claim Transitive Invalidation & Bounded Reauthorization

Status: **PASS (generic) / PRODUCT + DOMAIN-AUTHORITY + DATA-MODEL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**
Date: 2026-09-24
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A credential/session mechanics; Track B impact/reverification UX; Track C destructive validation; Track D bounded assurance measurement.
Dependencies: 122–125, 138–141, 161, 198–200, 241–259, especially acknowledgement applicability, credential compromise intervals, ledger correction, downstream revocation and closure provenance.

## Problem
259 established that credential compromise scopes uncertainty rather than deleting all history, and that dependent closure claims may need review. The next failure boundary is reconstructing the actual blast radius. Two opposite errors are dangerous: global panic reopening every historical claim because one credential/operator was compromised, or reviewing only direct ACKs and missing closures, exports, queued operations and successor claims that transitively depended on them.

Central rule: **compromise impact follows explicit evidence/authority dependencies and consequence scope, not mere temporal proximity or shared device identity. Reauthorization is a new bounded decision over the affected subgraph; it must preserve unaffected evidence, retain contradiction history, and prove both successor acceptance and predecessor rejection where controllable.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns credential/session/storage/Service Worker mechanics and can expose which technical artifacts reference an epoch; it cannot infer semantic dependency from cache/session adjacency.
- **B UX/IA/Content:** high dependency pressure. Owns truthful affected/under-review/unaffected/reverified states and non-destructive recovery paths. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **832 → 840 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. May measure affected-node classes, reauthorization debt and convergence latency; telemetry correlation cannot create dependency edges or closure authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns dependency reconstruction, transitive invalidation, cut-set containment, bounded reauthorization and closure recomputation.

## SOURCE

### NIST SP 800-61 Rev. 3 — incident response is integrated risk management
NIST finalized SP 800-61 Rev. 3 in April 2025 and frames incident response across cybersecurity risk-management activities, with the goal of reducing incident impact and improving detection, response and recovery.

Source: https://csrc.nist.gov/pubs/sp/800/61/r3/final

**TRANSFER VALIDATION:** supports explicit impact analysis and recovery rather than treating credential revocation as the entire incident response. It does not define a LogMate dependency graph.

### NIST SP 800-53 — least privilege limits failure/misuse impact
NIST SP 800-53 secure-system-design discussion states that least privilege limits a component's actions and therefore minimizes the security impact of failure, corruption or misuse; it also favors fine-grained privilege decomposition.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** bounded precedent for limiting reauthorization and blast radius to required consequence scope. It does not prescribe graph algorithms or product roles.

### RFC 5280 / RFC 6024 — trust is path/context dependent
RFC 5280 certificate path validation evaluates a target through a path to a trust anchor and permits different applications to rely on different trust anchors. RFC 6024 emphasizes that trust-anchor associated data constrains the scope for which a key is trusted.

Sources: https://www.rfc-editor.org/rfc/rfc5280 ; https://www.rfc-editor.org/rfc/rfc6024

**TRANSFER VALIDATION:** bounded precedent that trust is contextual and dependency/path based. Product ACK/closure dependencies are not X.509 certification paths.

## SYNTHESIS 1 — model compromise impact as a typed dependency graph
A useful generic graph has typed nodes such as credential/operator epoch, recipient incarnation, ACK, projection, closure claim, export/remediation obligation, queued operation, correction/resolution, policy/verifier generation and successor reauthorization. Edges are typed assertions such as `produced-by`, `verified-under`, `required-by`, `derived-from`, `closed-because-of`, `exported-from`, `authorized-by`, `supersedes`, `reverified-by`.

A shared timestamp, device, user or database row is not automatically a dependency edge.

Guard: `co-located ≠ dependent`; `correlated ≠ relied upon`; `same incident window ≠ same blast radius`.

## SYNTHESIS 2 — start from compromised roots and traverse only consequence-bearing edges
If K4 is compromised, seed the review with K4 and evidence materially produced/authorized/verified by K4. Traverse forward through edges that were necessary to a consequence. Do not automatically include every object merely viewed, cached or transmitted while K4 existed.

Record why each node entered the affected set. A node with no reconstructable material edge remains `UNKNOWN` or `UNPROVEN-DEPENDENCY`, not silently affected or silently safe.

Guard: `reachable by metadata ≠ materially dependent`; `edge missing ≠ independence proven`.

## SYNTHESIS 3 — direct invalidation and transitive invalidation are different
An ACK directly dependent on K4 can become `REVERIFICATION-REQUIRED`. A closure C12 that required that ACK inherits review transitively. An export generated from the disputed projection may create a remediation obligation. But an unrelated closure supported by independent K7 evidence does not reopen merely because it is stored in the same ledger.

Guard: `direct evidence questioned ≠ every ledger claim questioned`; `transitive dependency omitted ≠ closure remains sound`.

## SYNTHESIS 4 — preserve unaffected subgraphs
Incident response should not destroy independent evidence. Mark unaffected nodes with the basis for independence when material, and preserve historical proofs. Global deletion/reissue obscures blast-radius analysis and can convert a bounded incident into an organization-wide provenance loss.

Guard: `compromise response ≠ global history rewrite`; `safe node retained ≠ incident minimized falsely`.

## SYNTHESIS 5 — uncertainty is a first-class graph state
If old schemas failed to record which ACK closed C12, do not invent an edge. Represent `DEPENDENCY-UNKNOWN`, define the conservative consequence boundary, and create assurance debt for reconstruction or re-verification. The absence of provenance can widen the review set, but should remain distinguishable from proof that every candidate edge existed.

Guard: `cannot reconstruct dependency ≠ no dependency`; `conservative quarantine ≠ historical proof of compromise`.

## SYNTHESIS 6 — containment uses cut sets, not destructive resets
A bounded containment cut can fence compromised credential/operator epochs, affected ACKs and consequence-bearing mutation paths while leaving unique local data readable/recoverable. For a long-offline PWA, blocking outbound publication under K4 does not require deleting flight records, caches needed for evidence, or unrelated current data.

Guard: `authority fenced ≠ data erased`; `containment boundary ≠ device factory reset`.

## SYNTHESIS 7 — reauthorization is new evidence, not graph relabeling
After independent-enough successor bootstrap, reauthorization should create new nodes/edges: e.g. K5 `reverified` A12' under current policy, which supports new closure C13. Do not mutate K4-era A12/C12 to pretend they were always K5-backed.

Guard: `reauthorized now ≠ originally authorized by successor`; `new closure ≠ old closure never existed`.

## SYNTHESIS 8 — bounded reauthorization follows least privilege/consequence scope
Do not grant K5 or a remediation operator universal authority merely to repair one affected subgraph. Reauthorization should cover only the recipient, subject, projection/floor, operation class and consequence needed. Higher-consequence claims may require stronger independent evidence than low-risk read-only recovery.

Guard: `can repair node ≠ can authorize graph`; `incident role ≠ permanent superuser`.

## SYNTHESIS 9 — recompute closure from current prerequisites
A closure should become current only when its required prerequisites are current or explicitly accepted under policy. Recompute rather than copying the prior boolean. If one prerequisite remains `UNDER-COMPROMISE-REVIEW`, the closure cannot silently return to final merely because other prerequisites pass.

Guard: `all but one prerequisite current ≠ closure current`; `old closure boolean ≠ recomputed closure proof`.

## SYNTHESIS 10 — negative predecessor evidence remains necessary
Where the system controls the consequence boundary, prove K4/O7 cannot recreate affected closure, inject an old ACK into the successor graph, or reauthorize itself. Positive K5 success alone does not establish that the compromised path is extinct.

Guard: `successor path works ≠ compromised path blocked`.

## SYNTHESIS 11 — graph versioning and correction provenance are mandatory
Dependency graphs themselves can be wrong. Preserve graph version, source evidence and correction event when an edge is added/removed after investigation. Do not silently edit the graph and then claim the revised topology was always known.

Guard: `current graph ≠ historical knowledge`; `edge corrected ≠ prior decision context erased`.

## SYNTHESIS 12 — analytics is observation, not graph authority
Track D can report affected-node counts, unresolved unknown-edge debt, time-to-reverification and offline-tail convergence. Analytics event co-occurrence, funnel sequence or device last-seen cannot establish a consequence-bearing dependency edge.

Guard: `telemetry correlation ≠ authorization dependency`.

## SYNTHESIS 13 — Service Worker/cache/session topology is not semantic topology
A Service Worker may have delivered K4-era state to many pages, but that alone does not mean every record/closure depended semantically on K4. Conversely, a fresh Service Worker does not remove K4 dependencies from durable data/closures.

Guard: `same Service Worker controller ≠ same authority dependency`; `Service Worker replaced ≠ compromised subgraph reauthorized`.

## SYNTHESIS 14 — offline resurrection requires graph reconciliation before mutation
A long-offline iPad can return with old K4 ACKs, queued operations and unique data. Preserve them, identify their recorded dependency epochs, establish current bootstrap, reconstruct affected edges, revalidate only consequence-bearing operations, and generate successor evidence. Do not replay the queue wholesale or discard it wholesale.

Guard: `queue retained ≠ queue authorized`; `queue old ≠ queue disposable`.

## SYNTHESIS 15 — product facts remain OPEN
This study does not assert that MintTap/LogMate has a graph database, signed ACKs, OAuth credentials, K4/K5 keys, specific MDM controls or a particular closure engine. A dependency graph is a reasoning/data-model requirement; implementation can be relational/event-sourced/document-based if it preserves the needed semantics.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. reconstruct compromise impact with typed, provenance-bearing dependency edges;
2. distinguish direct, transitive, unknown and independent nodes;
3. preserve unaffected evidence and unique data;
4. fence compromised authority with minimal containment cuts rather than destructive reset;
5. treat missing provenance as explicit assurance debt/uncertainty;
6. create successor reauthorization as new evidence under current policy;
7. recompute closure from current prerequisites rather than copying old booleans;
8. limit repair authority to required consequence scope;
9. prove predecessor rejection where controllable;
10. version/correct the dependency graph itself with provenance.

## EFB / LogMate-like application case
Assume K4/I4 produced ACK A12; closure C12 depended on A12; report E12 was exported from projection P12; queued operations Q1/Q2 were created while offline. Later K4 is compromised. Q1 explicitly references P12/K4 authorization, Q2 is a locally authored flight record whose authorship/provenance does not depend on K4 publication authority.

Safe generic sequence:
1. preserve I4 data, A12/C12/E12/Q1/Q2 and historical graph evidence;
2. fence K4 from current consequence-bearing mutation;
3. mark A12 directly affected and C12 transitively review-required;
4. create E12 remediation obligation if its published meaning depended on P12/C12;
5. keep Q2's unique record data while withholding publication until current admission checks; do not label its authorship false solely because K4 was compromised;
6. classify Q1 by its explicit K4 dependency and revalidate/rebase under current policy;
7. establish K5/current incarnation through independent-enough bootstrap;
8. create new current ACK/closure evidence rather than rewriting A12/C12;
9. verify K4 cannot replay A12 or close the current consequence;
10. retain unknown edges/debt where historical provenance cannot resolve dependency.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
833. **Global panic reopen** — K4 compromise reopens/deletes every closure regardless of dependency. Expected: fail.
834. **Direct-only impact analysis** — A12 is flagged but C12/E12 transitive dependencies remain current without review. Expected: fail.
835. **Correlation-as-edge laundering** — same device/time/session is treated as proof of semantic dependency. Expected: fail.
836. **Missing-edge means safe** — absent historical provenance is treated as proof of independence. Expected: fail.
837. **Reauthorization history rewrite** — K5 current evidence overwrites K4-era A12/C12 provenance. Expected: fail.
838. **Incident superuser inflation** — remediation operator receives universal permanent authority to repair a bounded subgraph. Expected: fail.
839. **Positive-only graph recovery** — K5 closes C13 but K4 replay/self-reauthorization remains accepted. Expected: fail.
840. **Offline queue all-or-nothing** — returning iPad either replays every K4-era operation wholesale or deletes every queued/unique record. Expected: fail.

**VALIDATION:** these are defined destructive cases, not executed PASS.

## Cross-track transfer
- **A → E:** browser/session/credential references supply technical dependency evidence; E determines consequence-bearing semantic edges.
- **E → B:** UX must distinguish affected, unknown, unaffected and reverified states without false accusations or false finality.
- **E → C:** validation must exercise direct/transitive/unknown dependency, predecessor rejection and offline-return branches.
- **E → D:** measurement may quantify graph/reverification debt but cannot infer authoritative edges from correlation.

## External specialist boundary
Design Studio Web remains Stage 3 PRACTICE / NOT PASSED with physical-device/PWA, screen-reader and representative-human evidence OPEN. Software Engineering Studio remains Foundation IN STUDY; Safari/PWA and offline-attestation evidence are bounded transfer evidence only. Installed/physical iOS/iPadOS and canonical-product runtime remain OPEN. This study promotes neither external gate.

## OPEN / VALIDATION
- actual acknowledgement/closure/export/queue data model and dependency recording;
- exact recipient/operator credential architecture and compromise evidence;
- backend transaction/event/outbox behavior;
- graph reconstruction from existing production data;
- managed-iPad restore/reinstall/re-enrollment behavior;
- actual domain authority and aviation/legal correction/remediation rules;
- physical-device, AT, human, security and incident-response validation.

## Gate result
**PASS (generic).** The Web Manager can now reconstruct compromise impact as a scoped typed dependency problem, distinguish direct/transitive/unknown/unaffected evidence, preserve unaffected history and unique offline data, and perform bounded successor reauthorization without granting global repair authority or rewriting predecessor provenance.

Production validation remains OPEN.

## Next high-value target
**261 — dependency-graph completeness assurance, hidden-edge discovery & reauthorization-proof expiry.** Study how to know whether the recorded graph is sufficiently complete for a consequence, discover dependencies hidden in exports/caches/jobs/manual workflows, avoid declaring closure from an incomplete graph, and expire/recheck reauthorization evidence when policy/topology changes.