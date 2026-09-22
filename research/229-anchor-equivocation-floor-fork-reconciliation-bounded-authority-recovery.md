# 229 — PWA Anchor Equivocation, Floor-Fork Reconciliation & Bounded Authority Recovery

Status: **PASS (generic) / PRODUCT + MULTI-REGION + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA historical-state mechanics; Track B restricted/recovery UX; Track C fork/compromise destructive validation; Track D divergence telemetry.  
Dependencies: 219–228, especially witness equivocation, quorum diversity, emergency authority, assurance debt, dependency graphs, monotonic admission floors and anti-rollback anchors.

## Problem
228 established that anti-rollback anchors are authenticated minimum-currentness witnesses outside the ordinary rollback domain. That is insufficient when an anchor is compromised or equivocates. An authentic statement can be stale, a compromised signer can issue mutually inconsistent successors, and a compromised anchor set must not be allowed to authorize its own replacement.

Central rule: **anchor authenticity is necessary but not sufficient for current authority. Contradictory authentic anchor statements create a fork/compromise condition. Affected consequence-bearing capability remains bounded until an independently authorized successor establishes a lineage that does not derive its legitimacy solely from the suspected authority. Historical evidence is preserved; compromise recovery must not rewrite the past to manufacture continuity.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker/cache/IndexedDB can retain old anchor material or one fork view, but browser-local state cannot resolve server authority forks.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible LOCAL-SAFE / AUTHORITY-HELD / RECOVERING / CURRENT states without exposing cryptographic jargon or implying data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight equivocation/compromise/recovery destructive oracles; campaign expands **584 → 592 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures divergence, recovery lineage, affected scope and stale-tail age; telemetry cannot select the winning fork.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns compromise classification, fork containment, successor authority and bounded reauthorization.

## SOURCE

### NIST compromise recovery and key management
NIST defines compromise recovery as restoring a compromised system/device/process to a secure or trusted state, including destroying compromised keys, replacing them as needed and verifying the recovered secure state. SP 800-57 Part 1 Rev.5 provides current final key-management guidance and treats trust-anchor authenticity as a foundational assumption.

Sources:
- https://csrc.nist.gov/glossary/term/compromise_recovery
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

**TRANSFER VALIDATION:** NIST does not define a MintTap floor-anchor protocol. The reusable principle is that compromise recovery requires replacement plus verification; possession of an old authentic key is not sufficient current authority after compromise.

### NIST SP 800-193 — protected roots and authenticated update
SP 800-193 requires roots/chains of trust to be immutable or integrity-protected and requires mutable update roots/key stores to use authenticated update mechanisms. It also notes that updateable key stores can enable recovery from signing-key compromise while increasing tamper exposure.

Source:
- https://csrc.nist.gov/pubs/sp/800/193/final

**TRANSFER VALIDATION:** firmware-specific requirements are not adopted as a web/PWA implementation. The bounded precedent is that recovery of a trust basis must itself have a protected/authenticated transition path.

### TUF — role separation, thresholds and root compromise recovery
TUF is designed to remain useful under repository/signing-key compromise. Its documentation states that compromised role keys are revoked/replaced through Root authority, while compromise of a threshold of Root keys requires Root metadata to be re-issued out of band.

Sources:
- https://theupdateframework.io/spec/
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** TUF is a software-update framework, not our admission protocol. The reusable pattern is crucial: a compromised root threshold cannot safely bootstrap its own replacement merely by signing a successor with the compromised authority.

### RFC 9943 SCITT — transparency exposes equivocation but does not make issuers truthful
RFC 9943 defines signed-statement transparency with append-only/non-equivocation properties for the transparency service, while explicitly noting that transparency does not prevent dishonest or compromised issuers; it improves accountability/auditability.

Source:
- https://www.rfc-editor.org/rfc/rfc9943.html

**TRANSFER VALIDATION:** transparency evidence can expose inconsistent statements and preserve history, but it cannot turn a compromised anchor statement into trustworthy authority.

## SYNTHESIS 1 — stale-but-honest and equivocating are distinct states
An anchor below the newest known floor may simply be stale. Equivocation is stronger: the same authority lineage/generation context produces mutually incompatible successor/currentness statements that cannot both be true under the protocol's ordering rules.

Do not label every divergence malicious. Classify at least STALE/BEHIND, FORK-SUSPECTED, FORK-PROVEN, COMPROMISE-SUSPECTED and COMPROMISE-CONFIRMED where evidence permits.

`anchor disagreement ≠ attacker proven`; `authentic contradiction ≠ safe stale state`.

## SYNTHESIS 2 — freshness cannot repair equivocation
A newer timestamp on one conflicting statement does not make it authoritative if the signer itself may be compromised. Likewise majority observation cannot erase a cryptographically authentic conflicting branch.

`newer signed statement ≠ trustworthy successor`; `majority sees branch A ≠ branch B never existed`.

## SYNTHESIS 3 — suspected authority cannot be sole judge of its own innocence
If anchor set A is suspected compromised, an A-signed statement saying “A is healthy” or “replace A with A2” is evidence, not sufficient authorization. Recovery requires a trust path whose legitimacy is not wholly downstream of the suspected set: e.g. pre-established independent recovery authority, protected offline threshold, external current authority, or explicit governed ceremony with independent evidence.

Exact production mechanism remains OPEN.

`compromised authority signs replacement ≠ compromise recovered`; `self-attestation ≠ independent recovery`.

## SYNTHESIS 4 — preserve fork evidence; do not rewrite history into one clean chain
Recovery should retain both conflicting statements, provenance, observation times, receipts/checkpoints and affected scopes. The successor may declare a new current lineage and retire both branches for new consequence, but historical evidence should continue to show that a fork occurred.

`successor chosen ≠ losing branch erased`; `history repaired ≠ history rewritten`.

## SYNTHESIS 5 — successor authority needs explicit lineage and a compromise boundary
A recovery statement should bind, conceptually, the affected scope, compromised/suspect predecessor set, last independently trusted checkpoint if available, successor authority, minimum accepted floor, recovery basis/approvers, effective generation and unresolved evidence debt.

The exact schema is product design, not established here.

`new key exists ≠ successor authority established`; `successor authentic ≠ predecessor retirement proven`.

## SYNTHESIS 6 — partial compromise should not force unrelated capability into the compromised trust cut
Use the dependency graph from 223–225. If a capability's authority, identity, signing, policy, storage, recovery and enforcement cut is demonstrably outside the compromised anchor domain, it can remain available under its own current floor. If the separation cannot be proven, treat the edge as UNKNOWN and restrict rather than assume independence.

`shared product ≠ shared compromise scope`; `different endpoint ≠ independent trust cut`.

## SYNTHESIS 7 — total anchor compromise/loss is a bootstrap problem, not a voting problem
When all normal anchors are untrustworthy, counting their signatures or selecting the newest one does not recover authority. The system needs an independently governed bootstrap/recovery basis. This may reduce availability, but lowering the trust requirement because normal authority is unavailable creates recursive self-authorization.

`all normal anchors compromised ≠ majority vote recovers trust`; `availability pressure ≠ bootstrap authority`.

## SYNTHESIS 8 — fork reconciliation must fence both obsolete branches at side-effect boundaries
Publishing a successor is not enough. Both old branches must become inadmissible for new consequence. Negative tests should attempt old branch credentials/floors/writer epochs at actual side-effect boundaries where feasible.

`successor accepts writes ≠ fork branches extinct`; `no observed old writes ≠ old branch fenced`.

## SYNTHESIS 9 — transparency/telemetry are witnesses, not recovery authorities
A transparency log can preserve both conflicting statements and prove inclusion/ordering properties; observability can reveal divergent populations. Neither should automatically choose which branch gains authority unless separately governed to do so.

`fork visible ≠ fork resolved`; `receipt valid ≠ issuer trustworthy`.

## SYNTHESIS 10 — long-offline PWA clients may carry a legitimate historical fork view
A company iPad can go offline before compromise discovery and return with a branch that was authentic when observed. Preserve unique flight/logbook data, but do not grandfather remote mutation authority. Bootstrap current successor authority, migrate required worker/schema/policy state, then re-admit queued operations individually.

`client never saw compromise alert ≠ old branch current`; `historically legitimate client ≠ currently authorized operation`.

## SYNTHESIS 11 — cached higher floors remain useful as downgrade defenses, not global truth
A client or region remembering F30 can refuse F22 even during recovery. But its local F30 memory cannot by itself decide between two F30 successor branches or prove global currentness. Local monotonic memory is a lower-bound defense, not sovereign fork resolution.

`cached minimum useful ≠ cached branch globally authoritative`.

## SYNTHESIS 12 — recovery creates assurance debt until extinction and convergence are proven
Emergency successor establishment may be necessary before every tail is reachable. Record unresolved offline clients, unreachable regions, legacy credentials, missing negative tests and uncertain historical intervals as assurance debt. Do not close compromise recovery merely because primary traffic uses the successor.

`primary path recovered ≠ compromise recovery closed`; `successor deployed ≠ offline tail converged`.

## MINTTAP DECISION / DIRECTION
1. Treat authentic contradictory anchor statements as a fork/compromise condition, not an availability choice.
2. Separate stale-but-honest classification from proven/suspected equivocation; preserve uncertainty explicitly.
3. Never let a suspected/compromised anchor set be the sole authority that certifies its own replacement.
4. Require an independently governed recovery/bootstrap basis for total normal-anchor compromise or loss.
5. Preserve conflicting historical evidence; establish successor current authority without rewriting history.
6. Scope containment through the dependency graph; preserve capabilities only when their trust cut is demonstrably outside the compromised domain.
7. Fence every obsolete fork branch at consequence-bearing side-effect boundaries and retain negative rejection evidence.
8. Treat transparency/telemetry as evidence planes, not implicit recovery authorities.
9. Preserve unique offline PWA data first; current successor authority governs remote consequence after return.
10. Keep compromise-recovery assurance debt OPEN until stale branches, writers, credentials and offline tails are reconciled or explicitly bounded.

## Track C destructive campaign — +8 defined cases
585. **Same signer, incompatible successors:** two authentic anchor statements for the same lineage/generation authorize incompatible floors; system must not choose by timestamp/availability.
586. **Compromised-set self-replacement:** suspected anchor quorum signs its own successor; recovery must reject sole-source self-authorization.
587. **Telemetry-majority laundering:** 95% of clients observe branch A while a valid branch B receipt exists; majority must not erase contradiction.
588. **Partial trust-cut contamination:** capability claimed independent shares hidden IAM/KMS recovery root with compromised anchor; partial reauthorization must fail until dependency is resolved.
589. **Successor-positive-only:** new successor writes succeed but old branch credential still commits at downstream side-effect boundary; recovery must remain OPEN.
590. **PITR fork resurrection:** database restore reintroduces branch A after successor branch C was established; anti-rollback/rejoin must reject A.
591. **Long-offline iPad historical fork:** iPad returns with authentic branch B and unique unsynced flight data; preserve data, reject historical remote authority, re-admit under current successor.
592. **Total normal-anchor compromise:** all normal anchors agree on a convenient floor but all are inside the compromised domain; system must require governed independent bootstrap rather than vote itself healthy.

These are **defined destructive cases, not executed PASS evidence**.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate anchor topology, keys, issuers, quorum, provider and failure domains: OPEN.
- Actual recovery/bootstrap authority and ceremony: OPEN.
- Actual side-effect fencing primitives and downstream systems: OPEN.
- Managed iPad/iPadOS/WebKit/MDM storage/update/offline behavior: OPEN.
- Product schema for floor/fork/recovery lineage: OPEN.
- Physical-device, AT, representative-human and product runtime evidence: OPEN.
- Legal/aviation obligations affecting offline data retention/recovery: specialist evidence required.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev.5 is current final; Rev.6 remains draft as of the research date and must not silently replace final guidance.
- TUF specification/version and browser/platform behavior are change-sensitive; verify before implementation decisions.
- RFC 9943 is current Standards Track precedent for SCITT transparency; it does not prescribe MintTap authority recovery.

## Gate judgment
**229 PASS (generic).** We can distinguish staleness from equivocation, contain forked anchor authority, reason about independent successor bootstrap, preserve unaffected capability through proven trust cuts, and define compromise-recovery closure evidence without claiming a production protocol. Product/provider/device/runtime validation remains OPEN.

## Next highest-value adjacent question
**230 — successor-authority distribution, recovery-key custody & compromise-resistant bootstrap ceremony:** determine how independently governed successor authority is provisioned and authenticated across regions/clients without turning recovery keys into a standing bypass; how custody, threshold participation, ceremony evidence and offline-client bootstrap interact; and how recovery material is tested without normalizing emergency authority.