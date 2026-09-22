# 242 — PWA Governance-Recovery Ceremony Integrity, Recovery-Authority Independence & Split-View Succession Resistance

Status: **PASS (generic) / PRODUCT + CEREMONY + RECOVERY-AUTHORITY + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A successor/currentness observations; Track B recovery/fork UX; Track C destructive validation; Track D recovery-transition observability.  
Dependencies: 223–241, especially recovery custody/bootstrap, monotonic admission floors, fork recovery, topology repair governance, credential/delegation succession and governance-root recovery.

## Problem
241 established that suspected governance-root/quorum compromise cannot be healed merely by letting the same suspect authority certify its successor. The adjacent problem is the recovery ceremony itself. A separately held recovery authority can become an always-on bypass; ceremony participants can authenticate stale instructions; two partitions can each create a plausible successor; a recovered branch can be selectively shown to different clients; or emergency recovery authority can remain live after normal governance returns. A long-offline PWA client may then encounter two cryptographically plausible successor branches.

Central rule: **recovery authority is exceptional bootstrap authority, not parallel everyday governance. Invocation, participant/currentness verification, proposal binding, publication and closure are separate lifecycle steps. Recovery establishes one successor generation only after fork/split-view controls and consequence validation; emergency authority is then explicitly retired. Long-offline clients require canonical successor evidence or bootstrap recovery and never choose a branch by timestamp, reachability or local familiarity.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Supplies client-visible governance generation, trust anchor, fetch/update and stale-branch acceptance observations. One browser/device view cannot establish global non-equivocation.
- **B UX/IA/Content:** very high dependency pressure. Owns comprehensible `RECOVERY-PENDING`, `SUCCESSOR-CONFLICT`, `BOOTSTRAP-REQUIRED`, `RECOVERY-CLOSED` and data-preserving offline rejoin states; consumes Design Studio evidence rather than inventing reusable interaction doctrine.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight ceremony/fork/closure destructive cases; campaign expands **688 → 696 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures invocation frequency, branch observations, convergence/closure latency and stale-generation returns; telemetry cannot elect the canonical successor.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns invocation gates, recovery-authority independence, ceremony transcript/currentness, successor publication, split-view containment and emergency-authority retirement.

## SOURCE

### NIST SP 800-61 Rev.3 — recovery authorization, integrity and return to normal
NIST SP 800-61 Rev.3 remains current final incident-response guidance (April 2025). Its recovery guidance calls for plans to identify authorizations required for recovery, verification of restoration assets before use, validation of restored assets and explicit criteria for declaring recovery complete.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf

**TRANSFER VALIDATION:** this supports explicit recovery authorization, integrity checks and closure criteria. It does not define MintTap governance keys, quorum or recovery ceremony.

### TUF — threshold root compromise and out-of-band recovery precedent
TUF distinguishes ordinary role-key replacement from compromise of a threshold of Root keys; threshold Root compromise requires Root metadata to be re-issued out of band.

Sources:
- https://theupdateframework.io/docs/faq/
- https://theupdateframework.io/spec/

**TRANSFER VALIDATION:** useful precedent for an independent recovery path when normal trust continuity is suspect. TUF is not adopted as MintTap's governance protocol.

### RFC 9162 — append-only consistency and split-view auditing precedent
Certificate Transparency v2 specifies auditing of append-only behavior and consistency of log views. It notes that consistency of the view presented to all entities is harder and may require clients/monitors to compare observations; the RFC discusses gossip as an area for detecting divergent views.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** this is bounded precedent for the principle that one valid signed view does not prove all observers received the same view. It does not imply MintTap should deploy Certificate Transparency or a public transparency log.

## SYNTHESIS 1 — recovery authority must be exceptional, not an always-on alternate admin plane
A recovery basis that can silently publish ordinary topology/governance changes at any time is a standing bypass, not merely recovery. Separate normal governance authority from recovery invocation authority and from successor publication authority where the threat model justifies it.

Recovery invocation should bind to a declared incident/recovery reason, affected governance generation, consequence scope, recovery-policy generation and ceremony identifier. The exact MintTap threshold is OPEN.

Persistent guards: `recovery credential exists ≠ recovery invoked`; `recovery authority available ≠ ordinary governance bypass allowed`.

## SYNTHESIS 2 — ceremony authorization and factual truth are different
A correctly authorized recovery ceremony can still use stale, incomplete or attacker-supplied topology evidence. Conversely, a useful artifact can be factually correct without authorizing a governance transition.

Preserve separate claims for: invocation authorized; participant/credential current; recovery inputs authentic/current enough; successor proposal approved; successor published; successor accepted at consequence boundary; predecessor/emergency authority retired.

`ceremony approved ≠ recovery inputs true`; `successor signed ≠ successor topology correct`.

## SYNTHESIS 3 — participant currentness must be checked at ceremony time
Recovery participants, devices, credentials, offline media and instructions can age independently. A sealed recovery packet from G4 can be authentic but obsolete under G11. Verify participant authorization, recovery-policy generation, credential validity/revocation, intended system identity and applicable currentness floor before exercising recovery authority.

Do not treat physical possession of an offline token or printed instruction as proof that its authority remains current.

## SYNTHESIS 4 — recovery independence is claim-scoped, not location-scoped
Offline storage, a different office or a second cloud account does not prove independence if normal governance and recovery share the same identity recovery, personnel cut, device administration, provider root, signing workstation or custody chain.

Independence must be evaluated against the suspected failure hypothesis. A recovery path can be independent of online signing-key theft but correlated with personnel coercion or provider-account recovery.

`offline ≠ independent`; `different account ≠ different recovery failure domain`.

## SYNTHESIS 5 — ceremony transcript must bind proposal, evidence and generation
A durable non-secret transcript should identify the recovery/incident ID, predecessor governance generation, recovery-policy generation, participant/role identifiers, evidence references, proposal digest, successor generation/root identifier, decisions/exceptions, publication event and validation/closure evidence. Secret/private key material does not belong in the transcript.

Approvals must bind the exact proposal/evidence generation. Editing the successor after approval requires re-evaluation rather than reusing signatures over a friendly name.

## SYNTHESIS 6 — two plausible successors are a fork, not a voting contest
Network partitions, duplicate ceremonies or attacker equivocation can yield successor G12A and G12B, each apparently valid under recovery rules. Do not resolve by newest timestamp, first reachable endpoint, majority of clients, largest telemetry count or whichever branch an offline device already knows.

Enter `SUCCESSOR-CONFLICT`; freeze consequence-bearing governance advancement where the conflict matters; preserve both branches and provenance; compare common predecessor/ceremony identifiers and evidence; and use a separately defined conflict-resolution/recovery rule. If the recovery authority itself is implicated, it cannot unilaterally self-clear.

## SYNTHESIS 7 — one signed successor view does not prove non-equivocation
A server can present G12A to one client and G12B to another. Signature verification establishes authenticity relative to a key, not global uniqueness of the view. Where consequence justifies it, retain/checkpoint successor observations across failure domains or otherwise create a verifiable way to detect inconsistent successor publication.

RFC 9162 is useful precedent for separating valid signed view from consistency across observers. Exact implementation is OPEN; a public transparency log is not presumed necessary.

Persistent guard: `one successor verifies ≠ no competing successor exists`.

## SYNTHESIS 8 — recovery publication needs monotonic admission floors
Once canonical successor G12 is established, restore/PITR environments, provider admin paths, APIs and clients must not accept G11 or competing G12B for current consequence merely because their signatures verify. Intentional rollback of policy content is a new successor generation, not resurrection of a prior generation.

Publication is incomplete until relevant consequence boundaries enforce the successor floor and negative predecessor/competing-branch tests pass.

## SYNTHESIS 9 — emergency recovery authority must close after normal governance returns
Recovery authority that remains usable indefinitely after success becomes latent parallel governance. Closure requires establishment of normal successor governance, invalidation/fencing of temporary sessions/tokens/delegations, retirement or resealing of one-time recovery material as appropriate, negative tests at consequence boundaries, and retention of minimum non-secret recovery lineage.

`normal service restored ≠ emergency authority retired`; `recovery ceremony ended ≠ recovery capability safely closed`.

## SYNTHESIS 10 — recovery closure is explicit and reversible only through a new event
Use explicit states such as `RECOVERY-PENDING → RECOVERY-ACTIVE → SUCCESSOR-PUBLISHED → VALIDATING → RECOVERY-CLOSED`, with `SUCCESSOR-CONFLICT`/`RECOVERY-FAILED` branches. A later contradiction can reopen affected assurance claims, but historical ceremony facts are not rewritten.

NIST SP 800-61 Rev.3's explicit recovery-completion criteria is bounded precedent for not equating apparent service availability with completed recovery.

## SYNTHESIS 11 — long-offline PWA clients need branch-safe bootstrap
A LogMate-like iPad may depart under G7 and return after recovery to G12 while an attacker can still present plausible G11 or G12B. Preserve unique flight/logbook data and stale evidence. Do not choose a branch by local timestamp, cached Service Worker, connectivity path, server latency or local familiarity.

Authenticate the supported canonical successor lineage/checkpoint using product-defined bootstrap evidence. If the client cannot distinguish successors, enter `BOOTSTRAP-REQUIRED`/`SUCCESSOR-CONFLICT`, keep local read/capture/export capabilities that are independent of disputed authority where safe, and quarantine consequence-bearing replay until current trust is established.

Physical iPadOS/WebKit/MDM/bootstrap behavior remains OPEN.

## SYNTHESIS 12 — recovery UX must preserve data while making uncertainty visible
Track B consumes the security state, not invents it. Recovery UI should distinguish unavailable, stale, disputed and recovered authority; avoid telling the user that data is lost merely because trust is unresolved; avoid destructive reset as the default convergence mechanism; and provide a clear path for preserving/exporting unique offline data where product policy permits.

Design Studio Stage 3 remains NOT PASSED, so human/AT/physical-device UX validation remains OPEN.

## SYNTHESIS 13 — observability supports detection, not successor election
Track D may observe branch IDs, recovery invocations, convergence lag, stale returns and closure latency. Telemetry is valuable for detecting split views and lingering emergency use but cannot decide canonical governance by popularity. A compromised collector can also suppress minority-branch evidence.

`more telemetry for branch A ≠ branch A authoritative`.

## SYNTHESIS 14 — ceremony drills must test abuse resistance as well as availability
A recovery drill that only proves keys can be used can accidentally prove a standing bypass exists. Tests should include unauthorized invocation rejection, stale participant/credential rejection, exact proposal binding, duplicate/concurrent ceremony handling, split-view detection, predecessor/competing-branch rejection, emergency-authority retirement and long-offline-client bootstrap without data destruction.

Drill success remains bounded to the tested environment and does not establish production PASS.

## MINTTAP DECISION
For future MintTap/LogMate governance recovery, model recovery as an exceptional, versioned ceremony with explicit invocation, current participant/credential verification, exact proposal/evidence binding, monotonic successor publication, split-view/fork detection, consequence validation and explicit emergency-authority retirement.

Recovery authority must be independent relative to the suspected failure hypothesis and must not become an always-on alternate admin path. Two plausible successors create `SUCCESSOR-CONFLICT`; clients and operators do not resolve it by timestamps, reachability, majority telemetry or stale local preference. Long-offline PWA clients preserve unique data/evidence and require canonical successor bootstrap before consequence-bearing replay.

This is generic direction, not a claim that MintTap or LogMate currently implements this model.

## DEPENDENCY / TRANSFER
- **Track A:** expose exact client-visible governance generation/trust anchor and stale/competing branch acceptance; do not infer global non-equivocation from one client.
- **Track B:** design recovery/conflict/bootstrap states that preserve data and communicate uncertainty; consume Design Studio validation.
- **Track C:** own ceremony invocation/currentness/fork/closure/offline-client destructive tests.
- **Track D:** measure branch/recovery/closure observations without electing authority.
- **Software Engineering:** ceremony state machine, generation binding, anti-rollback storage, branch detection, token/session fencing and fault injection are implementation handoffs after product authorization.

## CONTRADICTION / FAILURE MODES
1. **Always-on recovery bypass:** recovery credential publishes ordinary changes without explicit recovery invocation.
2. **Stale ceremony kit:** authentic old participant list/instructions/token authorize recovery under obsolete policy.
3. **Correlated recovery:** supposedly independent recovery shares the compromised IAM/PAM/provider/personnel cut.
4. **Proposal substitution:** approval for successor digest A is reused after artifact changes to B.
5. **Dual-successor fork:** concurrent/partitioned ceremonies create G12A and G12B and clients pick by timestamp/reachability.
6. **Selective split view:** publisher serves different valid successor branches to different observers while each local signature check passes.
7. **Emergency authority persistence:** temporary recovery sessions/delegations remain consequence-capable after normal governance restoration.
8. **Offline-client branch laundering:** long-offline iPad chooses a plausible stale/attacker branch or is reset to hide the conflict, destroying unique data/evidence.

## Track C destructive additions — 688 → 696 defined cases
Add eight cases corresponding to the failure modes above. Required oracle behavior:
- reject recovery publication without explicit current invocation;
- reject stale ceremony participants/policy/credentials;
- expose correlated recovery dependencies;
- bind approval to exact successor proposal/evidence generation;
- enter conflict rather than elect by timestamp/reachability/majority;
- detect or preserve evidence of inconsistent successor views;
- prove negative retirement of temporary recovery authority;
- preserve offline unique data/evidence while refusing ambiguous branch replay.

**VALIDATION:** these are **defined cases**, not execution PASS. Actual product recovery authority, identity/PAM/provider topology, ceremony mechanism, anti-equivocation implementation, MDM, physical iPad/iPadOS/WebKit and runtime execution remain OPEN.

## OPEN
- Actual MintTap/LogMate governance/recovery authority, threshold, ceremony participants and storage/custody are unknown.
- Actual independent bootstrap basis and split-view detection mechanism are unknown.
- Actual identity/PAM/provider/MDM correlation and emergency-session retirement behavior are unknown.
- Exact canonical-successor distribution and client anti-rollback storage are unknown.
- Physical iPadOS/WebKit/managed-EFB branch/bootstrap behavior remains unvalidated.
- Legal/aviation/safety requirements may require stronger ceremony, custody, witness or retention controls.

## CHANGE WATCH
- NIST SP 800-61 Rev.3 remains current final incident-response guidance; implementation details remain environment-specific.
- TUF remains bounded precedent for threshold-root compromise/out-of-band recovery, not a MintTap protocol dependency.
- RFC 9162 remains bounded precedent for append-only/consistent-view auditing; it does not mandate CT-like infrastructure here.
- Identity/PAM/provider/MDM and browser/OS PWA behavior remain provider/platform-specific CHANGE WATCH.

## Gate judgment
**PASS (generic).** The adjacent competency is closed when Web Manager can keep recovery authority exceptional; authenticate current ceremony participants/artifacts; evaluate recovery independence against the suspected cut; bind approvals to exact successor evidence; treat competing successors as a fork rather than a vote; distinguish signature validity from non-equivocation; enforce monotonic successor admission; close emergency authority after recovery; and rejoin long-offline PWA clients without branch laundering or unique-data destruction.

Production certification is not claimed.