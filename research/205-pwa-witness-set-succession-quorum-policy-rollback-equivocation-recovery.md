# 205 — PWA Witness-Set Succession, Quorum-Policy Rollback & Equivocation Recovery

Status: **PASS (generic) / PRODUCT + WITNESS + QUORUM + REGION + IDENTITY + PROVIDER + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime state; Track B recovery/degraded-state semantics; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–204, especially 199–204.

## Problem

204 established that a witness constrains rollback but does not invent a successor. The next layer is constitutional: witness membership and threshold policy themselves can change. A previously legitimate witness set can become stale; a new set can be maliciously substituted; loss of enough witnesses can tempt operators to lower a threshold merely to restore availability; and long-offline clients can return carrying authentic quorum evidence that has since been retired.

Central rule: **witness-set membership and threshold are versioned authority policy, not ambient configuration. Succession must be authorized through the currently admitted policy lineage; witness loss does not silently lower the security floor.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Browser/PWA storage may retain an old witness-policy observation, but cannot establish global membership/currentness.
- **B UX/IA/Content:** high dependency pressure. Consumes `WITNESS-POLICY-STALE`, `QUORUM-UNAVAILABLE`, `EQUIVOCATION`, `RE-ADMISSION REQUIRED`, `LOCAL-ONLY`, `QUARANTINED`, `UNKNOWN` without implying local-data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns succession, quorum-loss, split-view, rollback and long-offline-client destructive tests. Campaign reaches **400 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can surface policy fingerprints, witness availability and equivocation evidence; cannot elect membership or lower thresholds.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns witness-policy lineage, succession, threshold-change admission, loss recovery and equivocation containment.

## SOURCE

### TUF Specification 1.0.36 — root policy is versioned; threshold and membership are signed policy

Current TUF Specification 1.0.36 (modified 2026-08-05) defines root metadata that names trusted keys and signature thresholds for roles. Clients must not replace trusted metadata with a lower version. For root succession, a client downloads each intermediate root version and the next root must be signed by both a threshold of keys trusted by the current root and a threshold of keys trusted by the new root. Root versions advance exactly N→N+1. When root keys change, clients preserve this chain of trust across all intermediate roots.

Source: https://theupdateframework.github.io/specification/latest/

**TRANSFER VALIDATION:** dual authorization across predecessor and successor policy is a strong precedent for changing a high-level witness/quorum policy without allowing an unrelated new set to self-appoint. TUF is not adopted as MintTap architecture.

### TUF — threshold compromise is qualitatively different from witness/key loss

TUF keeps root keys offline and states that if fewer than a threshold are compromised, normal root-key rotation can revoke them; if a threshold of root keys is compromised, root update must occur out-of-band and safe recovery is extremely difficult. Its FAQ likewise distinguishes ordinary replacement from threshold compromise.

Sources:
- https://theupdateframework.github.io/specification/latest/
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** loss/unavailability and compromise are distinct recovery states. A system must not solve either by silently weakening the admitted threshold.

### Sigstore — distributed threshold root is operational precedent, not a universal number

Sigstore's current security/threat-model documentation uses TUF for trust-root distribution and describes threshold signing, offline root keys, rotation/revocation and geographically/organizationally distributed root key holders. The documented public-good root uses five keyholders; Sigstore's threat model gives a 3-of-5 example.

Sources:
- https://docs.sigstore.dev/about/security/
- https://docs.sigstore.dev/about/threat-model/

**TRANSFER VALIDATION:** distributed custody and threshold authorization are useful operational precedent. No Sigstore count or threshold is copied into MintTap/LogMate.

## SYNTHESIS 1 — witness policy is itself a lineage object

A reusable witness-policy object conceptually binds:
- policy generation/identity;
- predecessor or authorized-succession relationship;
- witness identities/keys and roles;
- threshold/counting rule;
- independence assumptions/failure-domain declarations where required;
- scope of what the witness set may attest or constrain;
- activation/currentness bounds;
- recovery/succession rule;
- retirement state.

`witness signatures valid ≠ witness policy current`.

## SYNTHESIS 2 — membership succession needs predecessor authorization and successor acceptance

Generic safe succession from policy W to W+1 should establish both:
1. the currently admitted W authorizes the transition according to W's succession rule; and
2. W+1 satisfies its own admission rule so an attacker cannot install an unusable or attacker-only successor.

This is analogous to TUF root rotation's predecessor+successor threshold verification. Exact MintTap cryptography and threshold semantics remain OPEN.

`new witness set self-signs ≠ old policy authorized succession`.

## SYNTHESIS 3 — threshold change is security-policy change, not availability tuning

Changing 3-of-5 to 2-of-5, changing which identities count, or changing independence requirements can materially weaken the authority model even when all signatures are authentic. Such changes therefore require the same lineage/admission discipline as membership changes.

`quorum unavailable ≠ quorum requirement obsolete`; `outage pressure ≠ authority to lower threshold`.

## SYNTHESIS 4 — witness loss and witness compromise require different handling

Useful states:
- **AVAILABLE/CURRENT:** required admitted threshold can be satisfied;
- **DEGRADED-BUT-SATISFIABLE:** some witnesses lost but threshold and assumptions still hold;
- **QUORUM-UNAVAILABLE:** honest/current policy cannot currently reach threshold;
- **COMPROMISE-SUSPECTED:** one or more witness authorities may be hostile;
- **THRESHOLD-COMPROMISE/UNKNOWN:** admitted assumptions no longer justify ordinary succession;
- **RECONSTITUTION REQUIRED:** exceptional recovery authority must establish a new admitted policy without pretending ordinary quorum succeeded.

Loss may justify reduced availability. It does not justify forging continuity. Threshold compromise may require independent/out-of-band reconstitution and explicit incident evidence.

## SYNTHESIS 5 — old quorum evidence remains historical but cannot resurrect retired authority

After W→W+1, a correctly signed W statement may remain useful to verify history. It is not current authority merely because enough old witnesses still exist. A client that already admitted W+1 must reject W as current even if W's old threshold is fully satisfied.

`historically valid quorum ≠ currently authorized quorum`.

## SYNTHESIS 6 — equivocation is not resolved by counting whichever set is larger

If two current-looking policies or heads each satisfy a threshold under apparently valid evidence, the conflict is security evidence. Before selecting a branch, determine whether one is an authorized successor of the other under the admitted lineage. If neither ordering can be proven, quarantine consequence-bearing authority and preserve both views.

Do not resolve by wall clock, arrival order, region majority, telemetry count, witness-set size, or numeric policy generation alone.

`two threshold-valid views ≠ one may be chosen by popularity`.

## SYNTHESIS 7 — reconstitution cannot masquerade as ordinary succession

When the admitted threshold is unavailable or compromised beyond its ordinary recovery rule, a separate exceptional recovery path may be necessary. It must be explicit, incident-bound, independently authorized enough for the threat, scoped, evidenced, and followed by extinction of exceptional authority as established in studies 188–198.

The resulting successor policy should record that its provenance is **reconstitution**, not fabricate signatures from the unavailable predecessor.

`reconstitution success ≠ predecessor quorum was satisfied`.

## SYNTHESIS 8 — long-offline PWA must update witness policy before remote authority

A company iPad may return carrying W while the service has progressed W→W+2. Generic handling:
1. preserve unique local records/provenance;
2. treat cached W and its signatures as historical observation;
3. obtain current authenticated witness-policy lineage/floor from the server/recovery authority;
4. verify authorized succession as far as the client design requires, or obtain a current rebootstrap statement from an already trusted current channel;
5. reject W for current remote authority;
6. re-evaluate session/token/queued work under current policy;
7. preserve any historical gap/UNKNOWN rather than claiming the device observed W+1.

Client compatibility pressure must not cause the server to reactivate W.

## SYNTHESIS 9 — quorum arithmetic is insufficient without independence assumptions

A 3-of-5 threshold only means what the five authorities and their failure domains mean. If three witnesses share the same administrative identity, HSM/KMS recovery, deployment plane or recovery authority, nominal quorum can collapse to one correlated compromise.

Therefore policy evidence should preserve the independence assumptions relevant to the threat model. Exact organizational topology remains product evidence.

`threshold count met ≠ independence assumptions met`.

## SYNTHESIS 10 — recovery proof is scoped and paired

A succession/reconstitution checkpoint should record:
- predecessor policy and floor;
- successor policy and admission path;
- threshold/membership change;
- unavailable/compromised/retired witnesses;
- independence assumptions and UNKNOWNs;
- regions/enforcement domains that admitted the successor;
- negative probes proving retired policy cannot authorize consequential operations;
- positive probes proving successor authority works;
- offline/PITR/restored-client reconciliation state.

Absence of observed old-policy use is not proof of extinction.

## Track C destructive campaign — 400 cases total

Add eight cases to the 392-case campaign:
1. old W policy satisfies its full old threshold after W+1 was admitted — old quorum cannot resurrect current authority;
2. attacker presents self-signed W+1 with a weaker threshold — predecessor authorization missing, reject;
3. legitimate W→W+1 lowers threshold under an explicitly authorized current-policy transition — treat as policy change and preserve evidence, not runtime tuning;
4. two witnesses lost but admitted threshold remains satisfiable — service continues only within unchanged assumptions;
5. witness loss makes threshold unavailable — consequence-bearing policy succession blocks rather than silently lowering threshold;
6. threshold compromise suspected and ordinary W succession evidence cannot be trusted — enter explicit reconstitution path, do not fabricate continuity;
7. two threshold-valid conflicting heads are visible in different regions — quarantine and preserve equivocation evidence; no majority/popularity election;
8. long-offline iPad returns with W after W→W+2 — unique data preserved, old quorum historical-only, remote queue re-admitted under current policy without rewriting missed history.

Campaign status: **DEFINED, NOT EXECUTED**. Exact witness keys, thresholds, independence, region topology, provider identity, WebKit/iPadOS runtime, AT/human and product execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Browser storage may cache witness-policy evidence but browser persistence, local clock and Service Worker state cannot prove global policy currentness.

### E → B
B consumes explicit witness-policy stale/quorum unavailable/equivocation/re-admission states. UX must preserve local work while making remote consequence-bearing unavailability understandable; it must not present quorum failure as data loss.

### E → C
C receives membership/threshold rollback, witness loss/compromise, equivocation, reconstitution and long-offline-client tests.

### E → D
D can monitor witness availability, policy fingerprints, regional adoption and conflicting heads. Analytics/telemetry counts are not quorum-policy authority.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN. This artifact defines state semantics and assurance requirements, not interaction styling.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage with no specialist Foundation PASS. Exact policy serialization, cryptographic threshold verification, secure storage, regional distribution, routing quarantine, restore/PITR and PWA rebootstrap remain implementation/runtime dependencies.

## MINTTAP DECISION / DIRECTION

1. Treat witness membership and threshold as versioned authority policy with explicit lineage; never as ambient configuration.
2. Require authorized succession from the currently admitted policy and admission under the successor policy; do not permit self-appointed witness sets.
3. Do not lower quorum/threshold merely because witnesses are unavailable. Availability loss is not authority to weaken policy.
4. Distinguish witness loss from compromise; threshold compromise or unrecoverable quorum loss requires explicit exceptional reconstitution, not fabricated ordinary continuity.
5. Retain old quorum evidence for historical verification while denying it current remote authority after retirement.
6. Treat threshold-valid conflicting views as equivocation/incident evidence until authorized lineage resolves them; no clock/majority/popularity election.
7. Preserve unique offline PWA data while updating witness-policy lineage before admitting remote consequence-bearing work.
8. Keep actual witness count, threshold, key custody, independence, recovery mechanism and product topology OPEN until canonical runtime evidence exists.

## OPEN / VALIDATION

- actual MintTap/LogMate witness-set membership, threshold and independence assumptions;
- actual policy serialization/signature/lineage mechanism;
- actual emergency reconstitution authority and compromise model;
- actual regional policy distribution/enforcement/routing behavior;
- actual restore/PITR handling of retired witness policies;
- actual session/token/queue admission during witness-policy succession;
- WebKit/iPadOS storage/update/background/restart behavior;
- physical-device, managed-EFB, AT, human, security/privacy, safety/legal/aviation validation.

## VALIDATION / GATE

**PASS (generic).** The Web Manager can now treat witness membership/threshold as governed authority policy, distinguish ordinary succession from exceptional reconstitution, prevent old quorum evidence from resurrecting retired authority, and contain equivocation/witness loss without silently weakening the security floor. Product/runtime validation remains OPEN.

## Next highest-value adjacent question

**206 — witness-policy reconstitution anchoring, client bootstrap after total witness loss & anti-downgrade recovery packages.** Determine how a new witness policy is anchored when no ordinary predecessor quorum remains trustworthy; how a restored/new/long-offline client distinguishes an authorized recovery bootstrap from attacker-supplied trust reset; how recovery packages are scoped, one-way and non-replayable; and how successful rebootstrap proves retired witness policy cannot regain remote authority.