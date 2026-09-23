# 244 — PWA Witness/Checkpoint Compromise Recovery, Observation-Set Poisoning & Convergence-Proof Retention

Status: **PASS (generic) / PRODUCT + WITNESS + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A client/currentness evidence; Track B recovery/conflict UX; Track C destructive validation; Track D privacy-aware monitoring.  
Dependencies: 223–243, especially closure-proof retention, corroboration independence, graph currentness, recovery ceremony, branch convergence and witness survivability.

## Problem
243 established that independently governed witnesses/checkpoints can strengthen anti-equivocation and convergence evidence without becoming governance roots. The adjacent failure is harder: a witness can be compromised after closure; an attacker can curate which observers enter a convergence proof; retained evidence can become stale yet appear authoritative; or retention can expand into unnecessary telemetry about users/devices.

Central rule: **a convergence proof is a time-, topology-, consequence- and provenance-bounded historical assurance package. A witness/checkpoint contributes evidence but never becomes current authority. Later witness compromise requires scoped re-evaluation of claims that depended on that witness, not automatic erasure of all historical evidence or automatic trust in the surviving majority. Observer selection itself is part of the proof and must resist attacker curation. Retain the minimum evidence needed to reproduce the claim, not an unlimited behavioral history.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns what a browser/PWA client can actually observe: current bootstrap lineage, local checkpoint/generation, Service Worker/runtime state and server acceptance/rejection. A retained local checkpoint is historical evidence, not a current trust root.
- **B UX/IA/Content:** high dependency pressure. Owns understandable `ASSURANCE-DEGRADED`, `REVALIDATION-REQUIRED`, `BOOTSTRAP-REQUIRED` and data-preserving recovery states; reusable interaction doctrine remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive cases; campaign expands **704 → 712 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded but important consumer. Owns privacy-aware observation/monitoring mechanics and sampling limitations; analytics volume cannot establish canonicality or witness independence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns witness compromise blast radius, observer-set provenance, proof retention/minimization, revalidation and closure semantics.

## SOURCE

### NIST SP 800-61 Rev.3 — incident response and recovery remain lifecycle concerns
NIST finalized SP 800-61 Rev.3 on 2025-04-03, superseding Rev.2. It integrates incident response into cybersecurity risk management and retains detection, response and recovery as evidence-bearing lifecycle concerns.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

**TRANSFER VALIDATION:** supports re-opening/recovery activity when later evidence changes incident understanding. It does not define MintTap witnesses, quorum or retention periods.

### NIST SP 800-92 — long-term evidence must remain accessible and integrity-checkable
SP 800-92 remains current final log-management guidance; Rev.1 remains draft. Section 5.4 discusses long-term log retention, format longevity, migration when media/formats become inaccessible, integrity verification after transfer, secure storage and destruction when required retention ends.

Sources:
- https://csrc.nist.gov/pubs/sp/800/92/final
- https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.pdf

**TRANSFER VALIDATION:** bounded precedent for long-lived evidence interpretability/integrity and finite retention. It does not prescribe a MintTap convergence-proof schema or duration.

### RFC 9162 — monitors and conflicting-view evidence
RFC 9162 requires a monitor to inspect new entries in logs it watches and describes conflicting views as log misbehavior; multiple clients comparing signed tree heads can detect append-only violations. The RFC explicitly does not define a complete gossip system.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** bounded precedent that observation diversity can expose inconsistent views and that a locally valid signed view does not prove global consistency. Certificate Transparency infrastructure is not adopted here.

## SYNTHESIS 1 — witness compromise has a time boundary and a claim boundary
A witness compromised at time T2 does not automatically prove that every observation it made before T2 was fabricated. Nor may pre-T2 evidence be treated as unquestionably sound merely because it was once accepted.

For each affected proof retain: witness identity/generation, observation interval, credential/key generation, evidence creation time, independent anchors or corroborators, relevant compromise window, and the exact closure claim that consumed it.

Classify evidence as `UNAFFECTED`, `POTENTIALLY-AFFECTED`, `CONTRADICTED`, `UNVERIFIABLE` or `REVALIDATED` rather than deleting it or treating all history as green.

Persistent guards: `witness compromised now ≠ all historical observations false`; `historical signature verifies ≠ observation predates compromise`.

## SYNTHESIS 2 — later compromise reopens dependent claims, not unrelated history
If closure claim C1 depended materially on witness W1 and W1 is later suspected compromised during the relevant observation interval, C1's assurance must be re-evaluated. Claim C2 independently established by server-side rejection oracle plus W2 outside that failure domain need not be globally invalidated absent a dependency edge.

The dependency graph from 223–243 therefore remains essential: proof retention must preserve enough provenance to answer **which conclusions depended on which witnesses under which failure hypothesis**.

`one witness compromised ≠ every recovery claim invalid`; `no dependency recorded ≠ independence proven`.

## SYNTHESIS 3 — surviving-majority voting remains invalid after witness compromise
A common failure is to discard compromised W1 and declare the branch supported by W2/W3 the winner. That repeats the popularity error from 243. W2 and W3 may share the same provider/IAM/MDM/collector failure domain, and canonical successor authorization remains separate from observation count.

Recovery uses current authorized lineage plus consequence-boundary enforcement. Witnesses strengthen or weaken anti-equivocation assurance; they do not elect governance.

## SYNTHESIS 4 — observer-set selection is part of the evidence provenance
A convergence proof is vulnerable if the producer can choose only favorable observers. Record the eligible observation population or selection rule, exclusions, unreachable/unknown tails, selection time, topology epoch and material failure-domain coverage.

Do not claim global convergence from a convenience sample of online devices, one region, one MDM cohort or one provider dashboard. Conversely, exhaustive observation of every device is not always required: the proof is consequence-scoped and can rely on server-side monotonic admission floors to fence unknown stale clients.

`sample large ≠ sample representative`; `observer count high ≠ failure-domain coverage high`; `offline device absent from sample ≠ stale authority extinct`.

## SYNTHESIS 5 — observation-set poisoning includes inclusion and exclusion attacks
Poisoning is not only fabricated observations. An attacker can:
- exclude clients that saw a competing branch;
- over-represent one correlated provider/region;
- classify unknown/offline clients as retired without proof;
- replay old favorable observations into a new topology epoch;
- suppress witness-health failures;
- change the eligibility rule after seeing results.

Proof construction therefore binds observations to a declared selection/coverage policy and topology epoch. Material post-hoc changes require a successor proof, not silent mutation of the old package.

## SYNTHESIS 6 — retain proof inputs needed for reproducibility, not unlimited telemetry
A durable convergence package should be designed around claims, not surveillance. A generic minimum can include:
- proof/closure identifier and version;
- canonical successor generation/lineage reference;
- consequence boundaries evaluated;
- positive successor and negative predecessor/competitor oracle results;
- witness/checkpoint identities/generations and provenance;
- observer eligibility/coverage rule and topology epoch;
- observation window and relevant currentness/floor values;
- unresolved tails/blind spots and accepted assurance debt;
- integrity/canonicalization/verifier metadata needed to re-evaluate the package.

Avoid retaining full browsing history, arbitrary device payloads, unrelated analytics identifiers or complete user content merely because they were available during monitoring. Data needed for product records may have separate retention grounds; do not smuggle it into security-proof retention.

`auditability required ≠ retain every payload forever`; `proof reproducible ≠ user behavior reconstructable`.

## SYNTHESIS 7 — retention needs integrity, interpretability and verifier continuity
A proof that survives as bytes but cannot be parsed, canonicalized or verified years later is not durable assurance. Preserve the minimal schema/version, algorithm/verifier context and migration lineage needed to interpret retained evidence.

When moving archives or formats, verify integrity before/after migration and retain provenance of the migration. This follows the bounded SP 800-92 precedent without requiring permanent retention.

`bytes retained ≠ evidence interpretable`; `hash matches ≠ semantics understood`; `archive migrated ≠ provenance preserved`.

## SYNTHESIS 8 — retention duration is claim-driven and finite
There is no generic requirement here to retain convergence proofs forever. Duration must be derived from applicable incident/investigation obligations, recovery/restore windows, stale-client return horizon, governance lineage needs and product/legal constraints. When the justified period ends, dispose according to applicable policy while retaining only what another live obligation requires.

Actual MintTap/LogMate legal, aviation and organizational retention periods remain **OPEN**.

## SYNTHESIS 9 — retained checkpoints are evidence, never a current bootstrap oracle by themselves
A long-offline PWA may carry a perfectly authentic G12 checkpoint while current governance is G19. That checkpoint can help prove what the device knew when it went offline, but cannot authorize current sync, mutation or governance.

On reconnect, obtain current supported bootstrap/currentness evidence from the active trust path. Compare the retained checkpoint to current lineage to detect rollback/fork anomalies. If continuity cannot be established, remain `BOOTSTRAP-REQUIRED`/`SUCCESSOR-CONFLICT`; preserve unique data and do not promote cached checkpoint age or signature validity into current authority.

`retained checkpoint authentic ≠ retained checkpoint current`; `checkpoint useful for contradiction ≠ checkpoint may authorize replay`.

## SYNTHESIS 10 — local PWA evidence can outlive the witness plane that produced it
A returning iPad may contain an old witness/checkpoint package after the server-side witness service has been retired or compromised. Preserve it as historical evidence, classify its verifier/currentness state, and reconcile against current lineage. Do not delete the device to simplify the evidence graph.

This is especially important for LogMate-like unique flight/logbook data. Data preservation and authority admission remain separate.

## SYNTHESIS 11 — Track D monitoring must expose denominator and missingness
A convergence dashboard that shows `99.9% G19` without defining eligible population, offline/missing devices, topology epoch or failure-domain coverage can become trust theater. Track D should expose denominator/coverage semantics and missingness while minimizing identifiers.

Analytics remains detection/measurement evidence only. It cannot transform an unknown tail into proof of extinction or establish governance canonicality.

## SYNTHESIS 12 — closure after witness compromise requires successor evidence, not deletion of the incident
When a compromised witness causes `REVALIDATION-REQUIRED`, closure should append a successor assessment showing which historical claims remain valid, which were narrowed/reopened, what independent evidence was obtained, and whether current consequence boundaries still enforce the canonical floor.

Do not overwrite the original proof or pretend the witness was never used. Historical auditability requires preserving the fact that the earlier conclusion was made from the evidence then available.

## MINTTAP DECISION
For future MintTap/LogMate recovery assurance, treat convergence proofs as finite, privacy-minimized, versioned historical packages. Bind observer-set selection, topology epoch, witness provenance and consequence-boundary oracles into the package. If a witness is later compromised, reopen only claims materially dependent on the affected witness/window, preserve the original historical proof, and append successor revalidation. Never allow a retained checkpoint or witness majority to become current governance authority.

This is generic direction, not a claim that current MintTap/LogMate implements these controls.

## DEPENDENCY / TRANSFER
- **Track A:** expose current bootstrap/currentness and local checkpoint state without treating cached state as authority.
- **Track B:** communicate degraded/revalidation/bootstrap states without coercing destructive reset; consume Design Studio for reusable interaction patterns.
- **Track C:** own destructive validation for witness compromise, curated observers, stale checkpoints and proof migration.
- **Track D:** expose denominator, missingness, topology epoch and privacy-minimized convergence observations; never infer canonicality from analytics.
- **Track E:** own witness compromise blast radius, proof schema/retention, revalidation and closure.
- **Software Engineering:** implementation-level archive schema, verifier migration, runtime currentness and physical-device tests remain handoff territory.

## TRACK C DESTRUCTIVE CAMPAIGN ADDITIONS — 704 → 712 DEFINED CASES
1. **Post-closure witness compromise blanket invalidation:** W1 compromised later; system erases all recovery history instead of scoped dependency analysis — FAIL.
2. **Historical-signature laundering:** W1 signature verifies, but observation time may fall inside compromise window; system leaves closure green — FAIL.
3. **Survivor-majority election:** W1 fails and correlated W2/W3 majority elects a branch — FAIL.
4. **Favorable observer curation:** proof excludes devices/regions that reported competing branch without preserving selection provenance — FAIL.
5. **Unknown-tail laundering:** long-offline devices are counted as retired/extinct solely because they were not observed — FAIL.
6. **Telemetry-hoarding proof:** convergence retention stores unrelated user payload/history when claim-minimal metadata would suffice — FAIL.
7. **Stale-checkpoint authority promotion:** long-offline iPad uses authentic G12 checkpoint to authorize current G19 sync/replay — FAIL.
8. **Archive-migration amnesia:** retained proof bytes are migrated but verifier/schema/provenance context is lost, while system still claims durable verification — FAIL.

These are **defined cases only**. Execution PASS is not claimed.

## VALIDATION
Generic gate passes because the model can now distinguish witness compromise from blanket historical invalidation; observer-set coverage from sample count; proof retention from telemetry hoarding; and historical checkpoint evidence from current authority. It also defines destructive counterexamples and cross-track transfers.

Production validation remains OPEN for actual witness/checkpoint topology, proof schema, retention obligations, IAM/provider/MDM independence, iPadOS/WebKit behavior, currentness/bootstrap protocol, server admission floors, runtime archive/verifier migration, physical devices and human/AT recovery UX.

## OPEN
- Actual MintTap/LogMate witness/checkpoint and observer topology.
- Product/legal/aviation retention periods and deletion obligations.
- Exact eligible fleet/observer denominator and offline-tail policy.
- Actual currentness/bootstrap protocol and branch-floor enforcement.
- Physical iPadOS/WebKit/MDM long-offline behavior.
- Archive format, verifier/canonicalization longevity and migration drills.
- Human/AT comprehension of degraded/revalidation/bootstrap states.

## CHANGE WATCH
- NIST SP 800-92 Rev.1 remains draft while SP 800-92 (2006) remains current final; re-check before relying on detailed log-management guidance.
- Browser/OS/MDM PWA storage, lifecycle and managed-device behavior remains platform/provider-specific and change-sensitive.
- Product/legal/aviation retention requirements must be established from applicable current authority, not inferred from generic security guidance.

## NEXT
Highest-value adjacent work: **245 — convergence-proof verifier compromise, archive re-signing/migration & historical-evidence continuity**. Determine how retained convergence evidence remains assessable when the verifier/key/canonicalization algorithm itself is retired or compromised; how to migrate proof packages without falsely re-authoring history; how to distinguish a new archival attestation from the original witness statement; and how long-offline PWA evidence crosses verifier generations without downgrade or destructive reset.