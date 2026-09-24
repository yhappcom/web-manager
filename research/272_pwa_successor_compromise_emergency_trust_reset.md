# 272 — PWA Successor-Authority Compromise During Overlap, Cross-Signature Contamination & Emergency Trust-Reset Convergence

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/storage/rejoin mechanics; Track B truthful recovery UX; Track C destructive validation; Track D bounded incident/convergence diagnostics.  
Dependencies: 260–271 dependency/topology/re-entry/revocation/rotation governance.

## Problem

271 separated planned rollover from predecessor compromise. The harder adjacent case is overlap failure: R2 is compromised before R1 retirement, R1↔R2 cross-evidence becomes contaminated, or every in-band authority capable of certifying the next state is inside the suspected failure domain. A naive system can either preserve malicious continuity or destroy valuable offline data while attempting a reset.

Central rule: **when the current authority lineage is no longer trustworthy enough to authorize its own successor, stop treating in-band continuity as a safety property. Preserve historical evidence and unique data, fence affected consequences, establish a new trust state from an independently governed recovery basis whose assumptions survive the compromise model, and make clients converge forward without allowing restored/offline predecessors to resurrect authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns what Service Workers, Cache Storage, IndexedDB, client lifetimes and reconnect can actually preserve. Browser state is not emergency authority.
- **B UX/IA/Content:** high dependency pressure. Owns truthful `trust reset required`, `recovery-only`, `data preserved`, `revalidation required` and partial-capability states without implying deletion or successful sync.
- **C Performance/Accessibility/Quality:** destructive campaign expands **928 → 936 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures R1/R2 sightings, reset adoption, rejection, unresolved/offline tail and contradictions; telemetry cannot elect R3.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns compromise scoping, emergency trust reset, recovery-root independence, forward convergence and obsolete-authority rejection.

## SOURCE

### RFC 6024 — compromise/disaster recovery is an explicit trust-management requirement

RFC 6024 requires trust-anchor management to support recovery from compromise or loss of a trust anchor private key, including the trust-anchor-manager key, and discusses initial/bootstrap establishment including out-of-band checking. It also warns that compromise can install rogue trust anchors.

Source: https://www.rfc-editor.org/rfc/rfc6024

**TRANSFER VALIDATION:** this is trust-anchor management, not a PWA protocol. The reusable principle is that compromise of the authority managing trust is a distinct recovery problem and may require a separately established management basis.

### RFC 4986 / RFC 5011 — in-band recovery depends on an uncompromised anchor

RFC 4986 requires compromise recovery when at least one configured trust anchor remains known uncompromised. RFC 5011 states that if all trust-anchor keys at a trust point are compromised, manual or other out-of-band update is required.

Sources:  
https://www.rfc-editor.org/rfc/rfc4986  
https://www.rfc-editor.org/rfc/rfc5011

**TRANSFER VALIDATION:** DNSSEC mechanics/timers are not product defaults. The bounded lesson is that an in-band recovery chain cannot manufacture clean trust when every authority capable of certifying that chain is inside the compromise set.

### RFC 5934 — contingency authority can provide a recovery path

TAMP describes an optional contingency private key as a potential way to recover from compromise of an apex trust-anchor operational key.

Source: https://www.rfc-editor.org/rfc/rfc5934

**TRANSFER VALIDATION:** do not copy TAMP architecture into MintTap/LogMate. The reusable concept is pre-positioned recovery authority isolated from ordinary operational authority.

### RFC 6781 — emergency key replacement may require independently authenticated out-of-band verification

DNSSEC operational guidance notes that users updating a compromised anchored key should verify the new key and gives authenticated out-of-band verification as an example.

Source: https://www.rfc-editor.org/rfc/rfc6781

**TRANSFER VALIDATION:** the example transport is protocol/context-specific. The reusable principle is independence from the compromised in-band lineage, not any particular website or channel.

## SYNTHESIS 1 — overlap does not create safety when both authorities are suspect

R1+R2 overlap helps planned migration only while at least one relevant trust path remains valid. If R1 and R2 are both suspected compromised, two signatures or reciprocal cross-signatures can be two outputs of one contaminated domain.

Guards:
- `R1 + R2 signatures ≠ clean quorum when both are suspect`;
- `cross-signed ≠ cross-independent`;
- `overlap available ≠ overlap trustworthy`.

## SYNTHESIS 2 — contaminated cross-evidence remains historical evidence, not current admission evidence

Do not erase R1↔R2 transition objects merely because compromise is suspected. They may be essential incident/provenance evidence. But they cannot bootstrap R3 when the signers that created them are inside the compromise scope.

Guards:
- `historical evidence retained ≠ historical authority retained`;
- `signature mathematically valid ≠ signer currently trustworthy`;
- `contaminated lineage preserved ≠ contaminated lineage may authorize reset`.

## SYNTHESIS 3 — trust reset is a change of trust basis, not a larger generation number

An emergency R3 object with generation 300 does not outrank compromised R2 generation 299 merely by numbering. R3 needs admission through a recovery basis outside the failed trust assumptions, or through a governed rebootstrap when no such basis survives.

Guards:
- `higher generation ≠ clean trust root`;
- `new key ≠ trust reset`;
- `fresh timestamp ≠ independent authority`.

## SYNTHESIS 4 — recovery-root independence must be evaluated by failure domain

A recovery key stored in the same account, HSM administration plane, CI secret store, identity provider, operator workflow or backup as R1/R2 may not be an independent recovery basis. Independence is evaluated against the actual compromise model: credential, administration, deployment, storage, signer, reviewer and provider/control-plane domains.

Guard: `named recovery key ≠ uncompromised recovery path`.

## SYNTHESIS 5 — if no clean in-band authority survives, continuity may need to break

The safe response can be temporary loss of high-consequence availability while preserve/read/recovery remains possible. A system must not keep accepting compromised authority merely to avoid an outage.

Guards:
- `availability continuity ≠ trust continuity`;
- `temporary publication fence ≠ data loss`;
- `cannot authenticate successor in-band ≠ must trust predecessor forever`.

## SYNTHESIS 6 — emergency reset should bind scope and consequence

A reset for revocation-status authority does not automatically replace account administration, data-signing, deployment or every organizational authority. Reset evidence should identify compromised set, replacement scope, consequence, recovery basis, generation/epoch, activation criteria and obsolete-authority rejection requirements.

Guard: `R3 recovery authority for scope S ≠ universal administrator`.

## SYNTHESIS 7 — trust reset must preserve unique data separately from executable intent

Offline PWA records may be valid user-created data even when their queued mutation/publication authority is stale or contaminated. Preserve payload/provenance first; quarantine execution intent until current authority/policy/schema/device prerequisites are re-established.

Guards:
- `authority contaminated ≠ data malicious`;
- `queue cannot replay ≠ record should be deleted`;
- `rebootstrap identity ≠ rewrite historical authorship`.

## SYNTHESIS 8 — late clients converge through reset lineage or governed rebootstrap

A long-offline iPad that knows only R1/R2 cannot safely vote those authorities back into existence. On return it should preserve local records, enter bounded recovery/revalidation, obtain the current reset basis through an authenticated path, reconcile runtime/schema/device state, and revalidate queued operations individually.

Guard: `offline majority of old clients ≠ authority election`.

## SYNTHESIS 9 — reset completion requires negative proof against both contaminated predecessors

R3 positive operation is insufficient. Material execution boundaries must reject affected R1 and R2 consequences across API, job, admin/manual/recovery paths as applicable. Historical verification can remain available in isolated provenance paths.

Guards:
- `R3 works ≠ R1/R2 retired`;
- `old key removed from one store ≠ obsolete authority rejected everywhere`.

## SYNTHESIS 10 — backup/PITR cannot restore the compromised trust basis as current

A restore from before emergency reset can resurrect R1/R2 keys, caches, decision records and queues. Recovery must compare against a rollback-resistant current reset reference outside the restored failure domain or invoke governed rebootstrap.

Guard: `pre-reset backup internally consistent ≠ pre-reset authority current`.

## SYNTHESIS 11 — reset propagation is not reset establishment

Push, MDM, API, Service Worker update and app-shell delivery can distribute R3 material, but none establishes R3 authority unless the client can validate the recovery basis. Delivery and trust are separate layers.

Guards:
- `R3 delivered ≠ R3 trusted`;
- `worker understands R3 ≠ R3 authorized`;
- `MDM delivered configuration ≠ organizational trust proven`.

## SYNTHESIS 12 — emergency channels themselves need abuse resistance

A powerful recovery path can become the easiest takeover path. It should be unavailable to ordinary runtime mutation, narrowly scoped, auditable, tested, and governed proportionately to consequence. A permanently hot universal bypass defeats the purpose of primary controls.

Guards:
- `recovery capable ≠ recovery should be routinely active`;
- `break-glass exists ≠ break-glass may bypass evidence`.

## SYNTHESIS 13 — contradiction after reset reopens affected consequences

If one authoritative boundary rejects R1/R2 but another still accepts them, do not average the result into PASS. Preserve the contradiction, fence the affected consequence and repair the incomplete retirement graph.

Guard: `most paths reject obsolete authority ≠ all material paths safe`.

## SYNTHESIS 14 — fleet convergence is monotonic but not atomic

Central authority may establish R3 while unknown/offline devices remain unqualified. Safety depends on R1/R2 rejection at authoritative boundaries and per-client requalification, not 100% simultaneous installation.

Guards:
- `fleet not 100% R3 ≠ central R3 invalid`;
- `central R3 valid ≠ every client qualified`.

## SYNTHESIS 15 — recovery basis must itself be replaceable

After using a contingency/recovery authority, evaluate whether exposure during the incident changed its trust assumptions. A one-time recovery secret that remains indefinitely universal creates concentrated future risk. Exact rotation/retirement mechanics are product-specific.

Guard: `recovery succeeded once ≠ recovery root safe forever`.

## Generic emergency trust-reset contract

For a material R1/R2 overlap compromise:
1. preserve unique data, queues, transition objects and incident evidence;
2. define suspected/confirmed compromise scope and affected consequences;
3. fence high-consequence R1/R2 effects without destructive data reset;
4. determine whether any pre-established recovery basis survives the compromise model;
5. if yes, validate its independence/currentness; if no, invoke governed out-of-band rebootstrap;
6. establish R3 identity, scope, consequence and reset generation from that clean basis;
7. distribute R3 without confusing transport success with trust establishment;
8. make authoritative execution boundaries reject affected R1/R2 consequences;
9. re-establish policy/schema/device/runtime prerequisites independently;
10. revalidate queued operations rather than replaying inherited intent;
11. requalify online and late/offline clients monotonically;
12. preserve R1/R2 historical verification/provenance in isolated read paths where required;
13. verify backup/PITR cannot roll current authority behind R3;
14. monitor contradictions and unresolved fleet tail without using telemetry as authority;
15. rotate/retire emergency recovery capability when its post-incident risk requires it.

This is a reasoning contract, not a mandated cryptographic architecture.

## LogMate/EFB-like application case

Scenario: R1 is the prior revocation authority; R2 was staged but is compromised before R1 retirement; R1 is also now suspect because the same administrative plane controlled both. A company iPad has been offline for six weeks with unique flight records, R1/R2-era queue entries and an old Service Worker.

Safe generic treatment:
1. preserve records, queue payloads, provenance and local transition evidence;
2. do not let the device's R1/R2 state elect current authority;
3. keep local inspection/recovery available where safe while fencing sync/publication;
4. establish R3 through a recovery basis outside the R1/R2 compromise set or governed rebootstrap;
5. update browser/runtime components only as runtime prerequisites, not as authority proof;
6. reconcile schema/device/session state;
7. revalidate each queued operation under current R3-era policy;
8. prove server-side rejection of R1/R2 affected consequences;
9. admit only proven consequences and retain unresolved records without destructive cleanup.

**MINTTAP DECISION:** retain this as generic architecture guidance only. Do not claim MintTap or LogMate has R1/R2/R3, a recovery root, managed-iPad authority or this exact sync design until canonical product/runtime evidence establishes it.

## Track C destructive campaign additions — 928 → 936

1. **double-compromise-cross-signature theater:** R1 and R2 are both suspect but reciprocal signatures are treated as clean quorum. Expected: contaminated cross-evidence cannot establish R3.
2. **generation-number-reset:** unsigned/weakly admitted R3 wins because its generation is higher. Expected: trust basis, not numbering, establishes reset.
3. **same-plane-recovery-key:** recovery key shares compromised identity/admin/secret plane with R1/R2. Expected: independence challenge fails.
4. **availability-over-trust:** system continues R2 publication because reset would cause outage. Expected: consequence-aware degradation preserves data while fencing unsafe effect.
5. **reset-deletes-offline-data:** late iPad records are deleted because their authority epoch is obsolete. Expected: preserve data/provenance; quarantine/revalidate operations.
6. **R3-positive-only-retirement:** R3 succeeds but R1/R2 remain accepted through a job/admin path. Expected: negative predecessor rejection required.
7. **PITR-pre-reset-resurrection:** restore reactivates R1/R2 decision caches and queues. Expected: anti-rollback current reset reference or governed rebootstrap.
8. **worker-update-equals-trust-reset:** Service Worker update is treated as R3 admission. Expected: runtime update remains orthogonal to semantic authority.

**VALIDATION:** 936 cases are defined, not executed. Physical iOS/iPadOS, installed PWA, Safari/WebKit, AT, human, backend and canonical-product validation remain OPEN.

## Cross-track transfer

- **A → E:** browser persistence/update explains how stale runtime can survive; it does not choose R3.
- **E → B:** UX must distinguish data preservation from authority restoration and show bounded recovery states truthfully.
- **E → C:** quality must test contaminated-overlap, reset rollback, predecessor rejection and late-client convergence, not merely R3 happy path.
- **E → D:** analytics may measure adoption/contradiction/unknown tail but cannot constitute reset authority.
- **Software Engineering handoff:** implementation-level recovery-root storage, server rejection, queue reconciliation, restore and physical-device tests require canonical runtime evidence; no implementation PASS is inferred here.

## OPEN / CHANGE WATCH

OPEN until canonical evidence exists: actual MintTap/LogMate authority model; recovery authority; compromise domains; reset quorum; MDM/ADE/device enrollment; browser storage; Service Worker; auth/session; backend queue/job/manual paths; backup/PITR; schema/data model; aviation/legal obligations; and physical-device validation.

CHANGE WATCH: Apple/WebKit/iPadOS PWA lifecycle/storage behavior and organizational device-management behavior remain version/policy sensitive. Trust-management RFCs above are bounded security precedents, not PWA implementation specifications.

## Gate

**272 PASS (generic).** The Web Manager can distinguish planned rotation, predecessor compromise and overlap/double-compromise; determine when in-band continuity is no longer trustworthy; preserve evidence/data while fencing unsafe consequences; establish a bounded emergency trust reset from a surviving independent basis or governed rebootstrap; and reason about long-offline convergence without allowing obsolete authority resurrection.

## Next highest-value target

**273 — recovery-root compromise, emergency-authority abuse & post-reset recovery-root retirement:** determine what remains when the contingency/rebootstrap authority itself is compromised or abused, how to prevent break-glass authority from becoming a permanent super-root, and how to retire/replace emergency trust after successful reset without recreating the same correlated failure domain.