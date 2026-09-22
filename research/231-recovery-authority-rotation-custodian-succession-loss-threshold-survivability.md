# 231 — PWA Recovery-Authority Rotation, Custodian Succession & Loss-of-Threshold Survivability

Status: **PASS (generic) / PRODUCT + PROVIDER + PERSONNEL + MANAGED-IPAD + CEREMONY + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A long-offline PWA bootstrap; Track B recovery/succession state UX; Track C rotation/succession destructive validation; Track D lifecycle observability.  
Dependencies: 219–230, especially quorum diversity, anti-rollback anchors, fork recovery, recovery custody and successor bootstrap.

## Problem
230 established dormant, bounded recovery authority and separated recovery material from authorization. Recovery authority itself must nevertheless survive years of personnel, organization, provider, algorithm and device change. A permanent recovery root becomes an unmaintained concentration of authority; careless rotation can instead create two standing roots or silently weaken a threshold when custodians disappear.

Central rule: **recovery-authority rotation is an authority transition, not a key-copy operation. The successor must be authorized under the still-valid predecessor policy (or a separately governed loss/compromise path), become current at an explicit generation/floor, and be followed by negative retirement evidence for predecessor capability. Custodian succession changes both cryptographic material and failure-domain assumptions. Permanent threshold loss is not permission to lower the threshold.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/Service Worker/IndexedDB state may retain historical trust checkpoints, but a long-offline client must verify a rotation lineage/current successor before consequence-bearing remote work. Browser-local state cannot appoint a recovery successor.
- **B UX/IA/Content:** high dependency pressure. Must distinguish preserved local data from BOOTSTRAP-REQUIRED / SUCCESSOR-VERIFIED / CURRENT states and avoid prompts implying reinstall, connectivity or sign-in alone restores authority.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive rotation/succession/loss cases; campaign expands **600 → 608 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure rotation completion, stale-tail age, custodian-transition completion and predecessor rejection; telemetry cannot authorize succession or lower a threshold.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns rotation policy, custodian succession, overlap bounds, retirement evidence, threshold-loss containment and bootstrap continuity.

## SOURCE

### NIST SP 800-57 Part 1 Rev.5 — lifecycle, compromise, backup and trust-anchor/key management
NIST SP 800-57 Part 1 Rev.5 remains current final general key-management guidance as of this study. It treats key management as a lifecycle and covers key states/transitions, compromise, backup, archive, trust anchors and split knowledge. Additional copies improve availability but increase exposure; compromised material requires replacement and damage assessment.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/split_knowledge

**CHANGE WATCH:** NIST published SP 800-57 Part 1 Rev.6 Initial Public Draft on 2025-12-05. It is not final; it adds current algorithm/storage material including PQ algorithms. Continue to use Rev.5 as current final while monitoring Rev.6.

### NIST SP 800-57 Part 2 Rev.1 — organizational key-management governance
Part 2 addresses policy/security-planning and organizational key-management practice. It is relevant precedent for treating custody, responsibilities and lifecycle governance as organizational controls rather than merely cryptographic operations.

Source:
- https://www.nist.gov/publications/recommendation-key-managementpart-2-best-practices-key-management-organizations

**TRANSFER VALIDATION:** NIST does not prescribe a MintTap custodian-succession ceremony or threshold. The reusable principle is explicit organizational ownership and lifecycle governance.

### TUF — versioned Root rotation and threshold recovery precedent
TUF Root metadata identifies trusted keys and signature thresholds. TUF's compromise guidance says ordinary top-level key compromise can be repaired through Root authority, while compromise of a threshold of Root keys requires Root metadata to be re-issued out of band.

Sources:
- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** TUF is an update framework, not an application admission protocol. Its useful precedent is authenticated/versioned trust-root transition plus an out-of-band boundary when the ordinary root threshold is no longer trustworthy.

## SYNTHESIS 1 — planned recovery-root rotation is a policy-authorized authority transition
A routine rotation should be authorized while the predecessor recovery authority remains trustworthy and policy-current. The transition binds predecessor generation, successor identity/key set, successor threshold/policy generation, effective floor/generation, allowed overlap and retirement obligations.

`new key generated ≠ recovery authority rotated`; `successor signed ≠ predecessor retired`.

## SYNTHESIS 2 — overlap must be bounded, directional and observable
Some overlap may be operationally necessary so regions/offline clients can acquire the successor. But both roots must not remain indefinite peer authorities. Define a direction: predecessor may authenticate the specific successor transition during the bounded migration window; after the effective retirement boundary, predecessor must not authorize new recovery events.

`two roots verify during migration ≠ two roots remain current`; `overlap required ≠ dual standing authority`.

## SYNTHESIS 3 — custodian succession changes the threat model
Replacing a departing/incapacitated custodian is not merely handing the old share to another employee. Personnel, identity, HSM/vault administration, physical custody, provider recovery and organizational reporting dependencies must be re-evaluated. A new custodian set can satisfy the same numerical k-of-n while having materially worse correlated compromise risk.

`same k-of-n ≠ same independence`; `share transferred ≠ custody risk unchanged`.

## SYNTHESIS 4 — departure must retire both material and latent administrative reach
Succession closure includes old share/key retirement or re-sharing where appropriate, identity/PAM/HSM/vault access removal, recovery/admin paths, stored exports/backups where governed, and negative tests/evidence that the predecessor custodian cannot still exercise the relevant capability. HR departure alone is not cryptographic retirement.

`employee departed ≠ custodian authority extinct`; `account disabled ≠ all recovery material retired`.

## SYNTHESIS 5 — planned rotation and compromise rotation are different ceremonies
If the predecessor recovery authority is still trusted, it can participate in a governed successor transition. If it is suspected compromised, it cannot be the sole evidence certifying its own successor; use the independently governed compromise-recovery/bootstrap basis established in 229–230. Do not reuse the convenient planned-rotation path after trust has been lost.

`rotation needed ≠ predecessor trustworthy`; `predecessor signature valid ≠ safe after predecessor compromise`.

## SYNTHESIS 6 — permanent threshold loss does not authorize threshold reduction
If required shares/custodians are permanently unavailable, lowering k until the remaining set can act converts availability pressure into authority expansion. A separately pre-governed loss-of-threshold recovery path may exist, but its independence and authorization must be established before the loss or through an independently legitimate organizational recovery basis; exact MintTap mechanism remains OPEN.

`threshold unavailable ≠ threshold waived`; `business urgency ≠ new cryptographic authority`.

## SYNTHESIS 7 — threshold-loss state should degrade capabilities, not destroy unique data
When recovery authority cannot be exercised, preserve unique local/product data and capabilities whose trust cut does not require the missing authority. Block or defer authority-changing/recovery-dependent consequences rather than inventing a weaker root. This follows the existing capability-scoped degraded-mode model.

`recovery unavailable ≠ delete local data`; `cannot rotate authority ≠ all local work forbidden`.

## SYNTHESIS 8 — long-offline PWA clients may skip multiple recovery-root generations
An iPad can retain R3 while the system rotates R4→R5→R6. On return, do not require it to trust discovery channels or assume the newest downloaded root is legitimate. Verify a retained/authenticated successor lineage or governed current bootstrap/checkpoint sufficient to bridge the missed generations. Preserve unique local data first, then migrate worker/schema/policy and re-admit queued consequence individually.

`client missed rotations ≠ client may pick newest root`; `old root still verifies old artifact ≠ old root current`.

## SYNTHESIS 9 — rotation compaction must preserve bridge/retirement evidence
It is unnecessary to retain every operational artifact forever, but compaction must preserve enough authenticated lineage/checkpoint evidence for supported stale clients and enough retirement evidence to reject obsolete roots. If a client is older than the retained bridge horizon, move it to explicit BOOTSTRAP-REQUIRED rather than silently trusting an unbridgeable successor.

`history compacted ≠ trust continuity optional`; `bridge unavailable ≠ choose newest authority`.

## SYNTHESIS 10 — organizational transfer is an authority migration, not a naming change
Merger, subsidiary transfer, vendor/HSM migration or responsibility reassignment may alter legal/administrative control over recovery material. Re-evaluate failure domains and authorization, establish successor custody and retire old organizational access. Identical key bytes under new ownership do not prove unchanged trust.

`same key bytes ≠ same custody authority`; `organization renamed ≠ control plane unchanged`.

## SYNTHESIS 11 — rotation completion has three gates
1. successor authority established/authenticated;
2. predecessor recovery capability negatively fenced/retired;
3. required regions/clients/verifiers converged or their stale tails are explicitly bounded as assurance debt.

`successor current ≠ predecessor extinct ≠ fleet converged`.

## SYNTHESIS 12 — recovery-root lifecycle needs scheduled review without forced ceremonial churn
Periodic review should verify custody availability, independence, policy generation, cryptographic acceptability, contact/organizational continuity, drill evidence and stale-client bridge horizon. Rotation should be triggered by cryptoperiod/algorithm/policy/personnel/provider/compromise conditions as appropriate, not performed as empty calendar theater. Exact production cadence remains OPEN.

`review due ≠ rotate blindly`; `no incident ≠ custody still valid`.

## MINTTAP DECISION / DIRECTION
1. Model recovery-root rotation as versioned authority transition, not key replacement alone.
2. Permit only bounded directional predecessor→successor overlap; prevent indefinite dual standing roots.
3. Recompute custody/failure-domain independence on every custodian or organizational change.
4. Close custodian succession only after latent identity/admin/material access is retired with evidence.
5. Separate planned rotation from compromise recovery; a suspected predecessor cannot solely authorize its replacement.
6. Never lower threshold merely because intended threshold is unavailable; use only a separately legitimate loss-recovery basis.
7. Preserve unique data and capability-scoped safe operation during recovery-authority unavailability.
8. Support long-offline PWA clients through authenticated multi-generation lineage/checkpoints; otherwise require explicit governed bootstrap.
9. Preserve enough compacted bridge and retirement evidence to prevent downgrade after old metadata is pruned.
10. Treat organizational/provider custody transfer as authority migration requiring revalidation.
11. Track successor establishment, predecessor extinction and fleet convergence as separate gates.
12. Review recovery authority periodically, but rotate for justified lifecycle/security triggers rather than ceremony count.

## Track C destructive campaign — +8 defined cases
601. **Indefinite dual-root overlap:** R4 and R5 both remain able to authorize new recovery events after migration; predecessor must be fenced after the bounded transition.
602. **Departed-custodian latent access:** employee leaves but retains vault/HSM recovery path or exported share; succession closure must fail.
603. **Numerically same, correlated successor set:** 2-of-3 remains configured after succession but all new custodians depend on one SSO/admin recovery domain; independence claim must fail.
604. **Compromised predecessor performs planned rotation:** suspected R5 signs R6 through the ordinary rotation path; recovery must require the independent compromise-bootstrap basis.
605. **Threshold-loss convenience downgrade:** 3-of-5 loses three shares and policy is changed to 2-of-2 solely to regain availability; authorization must fail absent a separately legitimate recovery path.
606. **Long-offline iPad skips multiple roots:** client returns on R3 after R4→R5→R6 and receives R6 through a discovery channel; preserve data and require authenticated lineage/bootstrap before remote consequence.
607. **Compaction removes stale-client bridge:** retained metadata cannot prove R3→current and obsolete roots were pruned; client must enter BOOTSTRAP-REQUIRED rather than trust newest root.
608. **Organizational transfer with unchanged key bytes:** custody moves to a new provider/entity but dependency/failure-domain revalidation is skipped; current-authority claim must fail.

These are **defined destructive cases, not executed PASS evidence**.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate recovery roots, thresholds, custodians, HR/offboarding, HSM/vault/provider topology: OPEN.
- Actual planned-rotation and compromise-recovery policy/ceremony: OPEN.
- Actual loss-of-threshold organizational/legal recovery basis: OPEN; do not infer one.
- Actual cryptoperiod/algorithm migration trigger and Rev.6/PQ implications: OPEN / CHANGE WATCH.
- Actual long-offline supported bridge horizon and metadata retention/compaction policy: OPEN.
- Actual managed iPad/iPadOS/WebKit/MDM bootstrap behavior: OPEN.
- Physical-device, AT, representative-human and product runtime evidence: OPEN.
- Aviation/legal obligations affecting organizational succession, custody and offline data: specialist evidence required.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev.5 is current final; Rev.6 Initial Public Draft (2025-12-05) is under watch and must not be silently treated as final.
- Algorithm/key-storage/PQ transition guidance may change the triggers and acceptable material for future recovery-root rotation.
- TUF remains bounded precedent, not MintTap protocol.
- Browser/iPadOS/MDM behavior is platform/version-sensitive and requires current physical-device evidence.

## Gate judgment
**231 PASS (generic).** We can distinguish planned recovery-authority rotation from compromise recovery, bound old/new overlap, treat custodian succession as a failure-domain transition, preserve data without weakening authority during threshold loss, and reason about multi-generation long-offline PWA bootstrap. Product/provider/personnel/device/ceremony/runtime validation remains OPEN.

## Next highest-value adjacent question
**232 — recovery-authority inventory attestation, dormant-material discovery & succession drift detection:** determine how to prove that all current/retired recovery shares, HSM objects, vault exports, offline media, backup copies and administrative recovery paths are inventoried after years of rotation; how to detect orphaned dormant authority without turning inventory telemetry into authority; and how to reconcile inventory uncertainty with bounded operation and long-offline bootstrap.