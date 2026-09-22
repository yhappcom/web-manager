# 243 — PWA Recovery-Branch Convergence Proof, Witness/Checkpoint Survivability & Post-Recovery Anti-Equivocation Monitoring

Status: **PASS (generic) / PRODUCT + WITNESS + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A client/currentness observations; Track B convergence/conflict UX; Track C destructive validation; Track D monitoring.  
Dependencies: 223–242, especially anti-rollback/fork recovery, corroboration independence, topology repair and governance-recovery ceremony integrity.

## Problem
242 established that recovery may create a plausible successor yet still face split-view publication. The adjacent question is how to demonstrate that one recovered successor has become canonical across relevant consequence boundaries without turning telemetry, popularity or a single witness into authority. The same incident can also destroy or compromise witnesses/checkpoints, a competing branch can appear after apparent closure, and a long-offline PWA client can be selectively served an obsolete or competing branch.

Central rule: **recovery convergence is a scoped assurance claim, not a popularity result. Canonicality comes from the authorized successor lineage plus enforcement at relevant consequence boundaries; independently governed observations provide anti-equivocation evidence. Witness/checkpoint loss reduces assurance rather than electing a branch. Late contradictory evidence reopens affected claims without rewriting historical facts.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns exact client-visible successor generation, trust anchor, worker/runtime and stale/competing-branch acceptance observations; one client view cannot prove fleet convergence.
- **B UX/IA/Content:** high dependency pressure. Owns understandable `CONVERGING`, `SUCCESSOR-CONFLICT`, `BOOTSTRAP-REQUIRED`, `RECOVERY-CLOSED` states while preserving unique offline data; reusable interaction doctrine remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight convergence/witness/late-branch destructive cases; campaign expands **696 → 704 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures branch observations, convergence lag, stale-tail returns and monitor health; telemetry cannot establish canonicality.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns convergence claim scope, witness/checkpoint independence/survivability, late contradiction reopening and monitor normalization.

## SOURCE

### NIST SP 800-61 Rev.3 — post-recovery validation and monitoring
NIST SP 800-61 Rev.3 remains current final guidance (April 2025). RC.RP-04/05/06 require validation of restoration, confirmation of return to normal operations, monitoring restored-system performance, verification before production use and explicit recovery-completion criteria.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf

**TRANSFER VALIDATION:** supports post-recovery validation/monitoring and explicit closure. It does not define MintTap governance branches or witnesses.

### RFC 9162 — inconsistent-view detection precedent
Certificate Transparency v2 identifies conflicting views as log misbehavior and explains that multiple clients comparing signed tree heads can detect append-only violations; gossip is described as an active research area rather than fully specified by the RFC.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** bounded precedent that a locally valid signed view does not prove global consistency. CT infrastructure is not adopted here.

### TUF — rollback/freeze resistance precedent
TUF explicitly treats rollback and indefinite-freeze attacks as threats and uses version/currentness metadata to prevent clients from accepting obsolete trusted metadata.

Sources:
- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/spec/

**TRANSFER VALIDATION:** bounded precedent for client-side currentness/anti-rollback. TUF is not the MintTap governance protocol.

## SYNTHESIS 1 — canonicality and convergence are different claims
An authorized recovery ceremony can establish canonical successor G12 while some consequence boundaries or clients still serve/accept G11 or G12B. Conversely, most observed clients can show G12 without proving G12 was validly authorized.

Separate: `successor authorized`, `successor published`, `boundary enforces successor floor`, `observer saw successor`, `relevant population converged`, `no known competing branch`, and `anti-equivocation assurance sufficient`.

Persistent guards: `canonical successor ≠ fleet converged`; `fleet majority converged ≠ successor canonical`.

## SYNTHESIS 2 — convergence proof is consequence-scoped
Do not require proof about every byte or every offline device before closing every recovery claim. Define the relevant consequence boundary: governance publication, write admission, recovery action, authentication/session issuance, sync mutation, restore/PITR writer or other authority-bearing path. Prove successor acceptance and predecessor/competing-branch rejection there.

A stale read-only offline copy may remain without retaining current mutation authority. Its presence is still operational debt and may matter for confidentiality or future replay, but it is not automatically equivalent to a live writer.

## SYNTHESIS 3 — negative rejection evidence is essential
Positive G12 acceptance alone is insufficient. At each material boundary test rejection of G11, G12B and stale recovery/emergency authority where applicable. A successful current request does not show obsolete authority is fenced.

`G12 accepted ≠ G11 rejected`; `service healthy ≠ branch floor enforced`.

## SYNTHESIS 4 — witnesses observe; they do not become governance roots
An independent witness/checkpoint can strengthen evidence that different observers saw the same successor and can expose equivocation. It must not be able to mint or authorize governance merely because it recorded a branch.

Witness evidence should bind branch/generation, observation time/context, predecessor lineage and witness identity/provenance. Independence is evaluated against the incident failure hypothesis, not by counting hosts or accounts.

`witness observed G12 ≠ witness authorized G12`; `three witnesses ≠ three independent failure domains`.

## SYNTHESIS 5 — witness/checkpoint survivability must cross the recovery failure cut
If governance, witness, audit store and checkpoint anchor all depend on the same IAM/provider/admin/MDM plane, the incident that forces recovery can erase or rewrite all of them together. Survivability therefore requires at least one evidence path outside the relevant suspected cut when consequence justifies it.

This does not mandate blockchain, public transparency or multi-cloud. The mechanism can be much smaller; the requirement is claim-scoped independence and recoverability.

## SYNTHESIS 6 — witness loss reduces assurance; it does not select a winner
After an incident, unavailable or unverifiable witnesses create `ASSURANCE-DEGRADED`, not an automatic fallback to the branch with more remaining observations. Recovery can proceed under a product-defined degraded-assurance policy only if consequence and independent evidence justify it; debt and required revalidation remain explicit.

`witness unavailable ≠ competing branch disproven`; `surviving majority ≠ canonicality`.

## SYNTHESIS 7 — post-recovery monitoring is an anti-equivocation detector, not an election system
During convergence, monitor branch/generation observations, predecessor rejection, competing-branch sightings, emergency-authority use, stale-tail return and monitor/witness health. Alerts should preserve minority observations rather than suppress them as noise.

Track D telemetry supports detection and latency measurement. Popularity, sample count or geographic majority never elects governance.

## SYNTHESIS 8 — monitoring can normalize only after explicit closure criteria
Enhanced recovery monitoring need not run forever at emergency intensity. Normalize after the canonical successor is established, material consequence boundaries enforce the floor, emergency authority is retired, required witness/checkpoint paths are healthy or accepted debt is explicit, and a defined observation horizon shows no unresolved competing branch.

Normalization is not deletion of recovery lineage. Minimum non-secret evidence needed for later contradiction analysis remains retained under the applicable retention model.

## SYNTHESIS 9 — late competing branches reopen affected claims, not history
If G12B is discovered after G12 recovery was closed, preserve the original ceremony/closure facts. Reopen the claims that depended on `no known competing branch`, convergence or affected consequence boundaries. Determine where G12B was served/accepted and whether it retained authority.

Do not rewrite the historical record to say recovery never occurred, and do not globally invalidate unrelated controls without dependency evidence.

`late contradiction ≠ historical event erased`; `one late branch ≠ every closure claim invalid`.

## SYNTHESIS 10 — long-offline PWA clients are both stale tails and useful witnesses
A LogMate-like iPad returning after a long partition can carry an authentic old governance generation, cached Service Worker, local data and branch observations. Preserve unique flight/logbook data and stale evidence. The device cannot elect canonical governance, but a previously unknown competing successor presented to it can reopen anti-equivocation/convergence claims.

Before consequence-bearing replay: obtain supported canonical successor/bootstrap evidence, reject obsolete/competing authority, migrate worker/schema/policy as required, and re-admit queued operations individually. If canonicality cannot be established, remain `BOOTSTRAP-REQUIRED`/`SUCCESSOR-CONFLICT` rather than reset the device.

Physical iPadOS/WebKit/MDM behavior remains OPEN.

## SYNTHESIS 11 — offline duration creates a tail bound, not proof of extinction
A fleet may contain devices absent beyond the normal observation horizon. Lack of sightings cannot prove those devices or stale artifacts no longer exist. Product policy must distinguish `not observed`, `known retired`, `fenced from consequence`, and `physically/data-erased` claims.

A server-side monotonic admission floor can make an unknown stale client unable to mutate current state even when its local bytes survive.

## SYNTHESIS 12 — drills must include selective serving and witness failure
Recovery drills should test: canonical successor plus stale boundary; positive successor acceptance plus negative predecessor/competitor rejection; one compromised or unavailable witness; selective branch serving; monitor suppression; late competing-branch discovery; monitoring normalization; and long-offline rejoin without data destruction.

Drill PASS is bounded to the tested topology/environment and is not production certification.

## MINTTAP DECISION
For future MintTap/LogMate recovery, treat branch convergence as a consequence-scoped assurance claim. Canonical successor authority comes from the authorized recovery lineage; independently governed witnesses/checkpoints and monitoring detect equivocation and measure convergence but do not elect authority. Require negative predecessor/competitor rejection at material boundaries, explicit degraded-assurance handling when witnesses are lost, scoped reopening for late branch evidence, and data-preserving bootstrap for long-offline PWA clients.

This is generic direction, not a claim that current MintTap/LogMate implements these controls.

## DEPENDENCY / TRANSFER
- **Track A:** expose client-visible generation/trust anchor and branch acceptance without inferring global convergence.
- **Track B:** express converging/conflict/bootstrap states while preserving unique data; consume Design Studio evidence.
- **Track C:** own selective-serving, witness-loss, negative-floor and late-branch destructive tests.
- **Track D:** measure branch/witness/monitor health and convergence latency without authority election.
- **Software Engineering:** implementation handoff for anti-rollback state, branch observation/checkpointing, fault injection and selective-serving tests after authorization.

## CONTRADICTION / FAILURE MODES
1. **Majority-as-canonical:** most telemetry shows G12, so authorization/lineage is skipped.
2. **Positive-only convergence:** G12 works but G11/G12B rejection is never tested.
3. **Correlated witnesses:** three witnesses share the same compromised control plane.
4. **Witness-loss election:** surviving witness majority chooses a branch after the incident destroys others.
5. **Selective-serving blind spot:** minority G12B observations are suppressed as noise.
6. **Premature monitor normalization:** emergency monitoring stops before floors/authority retirement are validated.
7. **Late-branch blanket rewrite:** G12B discovery either gets ignored or globally erases unrelated historical closure.
8. **Offline-iPad laundering:** returning device chooses a branch by cached/local state or is reset, destroying unique data/evidence.

## Track C destructive additions — 696 → 704 defined cases
Add eight cases corresponding to the failure modes above. Required oracle behavior:
- reject popularity as canonicality evidence;
- prove both successor acceptance and predecessor/competitor rejection;
- expose witness failure-domain correlation;
- degrade assurance rather than elect by surviving count;
- preserve minority/selective-serving evidence;
- block monitoring normalization until closure criteria pass;
- reopen only affected claims on late competing-branch evidence;
- preserve offline unique data/evidence while refusing ambiguous replay.

**VALIDATION:** these are **defined cases**, not execution PASS. Actual product recovery topology, witness/checkpoint mechanism, provider/PAM/MDM, physical iPad/iPadOS/WebKit and runtime execution remain OPEN.

## OPEN
- Actual MintTap/LogMate canonical-successor distribution, witness/checkpoint and monitor topology are unknown.
- Actual consequence boundaries and admission floors are unknown.
- Actual observation horizon and stale/offline fleet population are unknown.
- Actual provider/IAM/PAM/MDM failure-domain independence is unknown.
- Physical iPadOS/WebKit/managed-EFB selective-serving/bootstrap behavior remains unvalidated.
- Legal/aviation/safety obligations may require stronger independent witnessing, retention or recovery evidence.

## CHANGE WATCH
- NIST SP 800-61 Rev.3 remains current final incident-response guidance; recovery implementation remains environment-specific.
- RFC 9162 remains bounded precedent for inconsistent-view detection; it does not mandate CT-like infrastructure.
- TUF remains bounded precedent for rollback/freeze resistance and currentness; it is not adopted as MintTap governance protocol.
- Provider identity/PAM/MDM and browser/OS PWA behavior remain provider/platform-specific CHANGE WATCH.

## Gate judgment
**PASS (generic).** The adjacent competency is closed when Web Manager can separate canonical authorization from convergence; scope convergence to consequence boundaries; require negative stale/competitor rejection; use witnesses as independent observers rather than authority; reason about witness survivability/loss; monitor for post-recovery equivocation without voting; normalize monitoring only after explicit closure criteria; reopen affected claims on late branch evidence; and rejoin long-offline PWA clients without branch laundering or unique-data destruction.

Production certification is not claimed.