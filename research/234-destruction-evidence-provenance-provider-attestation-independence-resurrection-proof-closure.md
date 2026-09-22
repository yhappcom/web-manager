# 234 — PWA Destruction-Evidence Provenance, Provider-Attestation Independence & Resurrection-Proof Closure

Status: **PASS (generic) / PRODUCT + PROVIDER + AUDIT + HSM/VAULT + BACKUP/RESTORE + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A stale-client/runtime boundary; Track B retirement/recovery-state UX; Track C destructive closure validation; Track D lifecycle observability.  
Dependencies: 223–233 dependency/discovery, proof lineage/currentness, anti-rollback/recovery, custody/rotation/inventory and destruction/residual-copy assurance.

## Problem
233 separated current-authority retirement from universal material erasure. The next failure mode is evidentiary: a deletion event can be genuine yet refer to the wrong object, generation or failure domain; the same compromised provider/admin plane can both perform deletion and issue the only proof; a delayed provider deletion state can be confused with current-authority safety; and a backup/reimport/PITR path can resurrect retired material after a superficially complete closure.

Central rule: **destruction closure is a claim-specific, provenance-bound proof bundle. Bind every receipt/attestation to exact object, generation, provider/account/region or HSM domain, lifecycle transition and observation time; separate provider lifecycle evidence from independent current-authority negative enforcement evidence; and keep restore/reimport/PITR paths outside consequence-bearing service until they prove predecessor non-admission under the current floor. Do not demand impossible customer observation of provider physical media, but do not upgrade provider self-attestation beyond its documented scope.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/Service Worker/IndexedDB state can preserve stale trust metadata and queued operations but cannot independently attest server-key destruction. Long-offline clients remain replay/resurrection consumers that must re-bootstrap current authority.
- **B UX/IA/Content:** high dependency pressure. Must distinguish provider destruction completion, authority retirement, residual-copy uncertainty and restore/rejoin quarantine without presenting one as another. Design Studio remains visual/interaction authority.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight provenance/independence/resurrection destructive cases; campaign expands **624 → 632 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can measure event/receipt age, provider state, restore attempts and stale-authority rejection, but telemetry is evidence input rather than authority or universal-erasure proof.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns evidence identity/provenance, independence, provider-scope semantics, closure bundles, restore/reimport/PITR fencing and compromise escalation.

## SOURCE

### NIST SP 800-88 Rev.2 — sanitization assurance requires verification/validation, not a delete verb
NIST SP 800-88 Rev.2 is the current final NIST media-sanitization guidance (September 2025, superseding Rev.1). It strengthens sanitization validation/program governance and treats sanitization assurance as a process whose method and evidence must fit the media/data and sanitization objective. It does not justify claiming physical or provider-wide erasure beyond the evidence boundary.

Sources:
- https://csrc.nist.gov/pubs/sp/800/88/r2/final
- https://csrc.nist.gov/news/2025/guidelines-for-media-sanitization-rev-2

**TRANSFER VALIDATION:** the Web Manager uses this as authoritative sanitization-process guidance, not as proof that a cloud-provider receipt independently proves every physical replica was erased.

### Google Cloud KMS — key-version identity and delayed destruction are distinct facts
Current Google Cloud KMS documentation states that destruction applies to a **key version**, that a version remains Scheduled for destruction during a configurable period and can be restored during that period, and that after the state becomes Destroyed logical deletion from active systems has begun. Google states that key material can remain in its systems for up to 45 days from the scheduled destruction time, including removal from active systems and data-center backups. Previously imported material is a separate re-import exception.

Source:
- https://docs.cloud.google.com/kms/docs/destroy-restore

**SYNTHESIS:** a receipt/state observation must bind the exact key/version and lifecycle phase. `key destroyed` without version/scope/time is insufficient evidence language.

### AWS KMS — deletion events are auditable but provider event and external-copy extinction are different claims
Current AWS KMS documentation states that key deletion has a mandatory 7–30 day waiting period, records scheduling/deletion in CloudTrail, and distinguishes imported key-material deletion from KMS-key deletion. AWS documents that imported key material can be reimported and that deleting imported material is therefore a different lifecycle event. Current imported-material documentation also exposes key-material identifiers and CloudTrail records for deletion/expiration events.

Sources:
- https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html
- https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-delete-key-material.html
- https://docs.aws.amazon.com/kms/latest/developerguide/ct-deleteexpiredkeymaterial.html

**SYNTHESIS:** provider audit events are strong evidence about the provider-controlled object and event, but do not prove an imported source, offline export, another region/object or customer backup does not exist.

## SYNTHESIS 1 — destruction evidence needs a stable evidence identity
A useful destruction-evidence record binds at least:
- authority/material logical ID and cryptographic/public fingerprint where safe/useful;
- provider/HSM/vault object ID and exact version/material ID;
- provider account/project/tenant, region/key-store/HSM failure domain where applicable;
- origin/import/export classification;
- lifecycle state before/after and event type;
- request actor/authorization context and provider event/receipt ID;
- request, scheduled-completion and observed-completion times;
- documented reversible/deletion window;
- attestation/evidence source and collection path;
- current successor/floor generation;
- required negative consequence oracles;
- restore/reimport/PITR inventory disposition and known blind spots.

A human label such as `recovery-key-old` is not sufficient provenance. `same alias/name ≠ same key generation`; `same logical role ≠ same material`; `receipt exists ≠ receipt refers to retired object`.

## SYNTHESIS 2 — provider lifecycle evidence and authority-safety evidence answer different questions
Provider state/receipt can answer whether a provider-controlled object entered/completed a documented lifecycle transition. A current verifier/admission negative oracle answers whether retired material can still cause an accepted current consequence. These are deliberately different evidence planes.

A provider may be the only practical authority for internal physical deletion semantics; demanding impossible customer inspection creates false rigor. But the provider should not also be treated as the sole proof that every application verifier, stale region, restore path and imported external copy rejects predecessor authority.

`provider attests destruction ≠ application retirement proven`; `application rejects predecessor ≠ provider physical deletion proven`.

## SYNTHESIS 3 — independence is claim-relative, not absolute
No cloud customer can make provider-internal deletion evidence fully independent of the provider that operates the storage. Independence must therefore be evaluated per claim:
- provider lifecycle claim → provider-native state/audit/contract/documentation may be the strongest available evidence;
- application authority-retirement claim → independently controlled verifier/admission negative tests should not depend solely on the same deletion event;
- external/imported/offline-copy claim → inventory/custody/media evidence belongs to those separate failure domains;
- restore/rejoin claim → recovered environment must demonstrate current-floor predecessor rejection before consequence-bearing rejoin.

`same provider involved ≠ all evidence worthless`; `same compromised admin path controls deletion and only closure proof ≠ independent closure`.

## SYNTHESIS 4 — compromised control planes require provenance downgrade, not invented certainty
If the provider tenant/admin identity, audit configuration or evidence-export path is suspected compromised during the relevant interval, a signed/valid provider event may still be useful but its evidentiary weight changes. Preserve the raw event, provider resource identity, external copies of audit evidence where already available, successor/floor evidence and negative runtime results. Do not erase contradiction by selecting the most convenient source.

`event authentic ≠ event context uncompromised`; `audit log silent ≠ deletion did not occur`; `audit log says delete ≠ every required closure condition passed`.

## SYNTHESIS 5 — delayed provider deletion and current-authority fencing can progress on separate clocks
A retired predecessor can be current-authority safe before provider physical deletion finishes if successor authority is independently established and every affected current consequence path rejects predecessor material. The material-erasure claim remains DESTRUCTION-PENDING until provider semantics support stronger closure.

This prevents two opposite errors: keeping obsolete authority accepted merely because provider deletion is delayed, and falsely claiming physical/material destruction merely because authority is already fenced.

`authority retirement complete ≠ material destruction complete`; `material deletion pending ≠ predecessor must remain authorized`.

## SYNTHESIS 6 — resurrection-proof closure is a rejoin property
Backups and PITR images can preserve software keystores, encrypted exports, IAM/configuration, stale policy, cached credentials or administrative reach even when a provider-managed non-exportable key itself is not restored. Therefore the invariant is not “the backup contains no old bytes”; it is “restoring any supported recovery artifact cannot produce an accepted retired authority transition without current governed reauthorization.”

Recovered environments enter a quarantine/reconciliation state. Before writer/admission rejoin they must acquire current floor/successor state, enumerate restored predecessor material/paths, run required negative tests, reconcile reimport/admin paths and only then regain consequence-bearing capability.

`restore succeeded ≠ rejoin authorized`; `old material absent in one backup scan ≠ resurrection impossible`; `retired material restored ≠ retired authority accepted`.

## SYNTHESIS 7 — reimport is an explicit resurrection edge
Imported key material creates a special edge: deleting provider-held material may leave the external source capable of reimport. Closure therefore records whether origin was provider-generated/non-exportable or external/imported, whether reimport is possible, and whether current policy/floor would reject a re-created/reimported predecessor even if cryptographic material matches.

For authority systems, identity should not be reduced to private-key bytes alone. Generation/floor/policy lineage must prevent an old material copy from regaining current authority merely by being reintroduced into a fresh provider object.

`same key bytes reimported ≠ current authority restored`; `new provider object ≠ new authority generation automatically trusted`.

## SYNTHESIS 8 — closure should survive audit/log retention expiry
Provider audit logs can have finite retention or customer-controlled deletion/configuration. Durable closure therefore retains a minimal non-secret evidence package sufficient to identify what claim was closed: object/version/material ID, lifecycle result, relevant timestamps, evidence digest/reference, successor/floor generation, negative-oracle result and residual-copy disposition. Do not retain private key material merely to prove that it was retired.

`log retention expired ≠ retirement history should become unknowable`; `retain proof ≠ retain retired secret`.

## SYNTHESIS 9 — PWA stale tails test authority closure, not key destruction
A long-offline LogMate-like iPad may return with stale worker code, historical trust metadata and queued operations from before retirement. This is a valuable negative-authority test: current server admission should reject obsolete authority and require current bootstrap/re-admission. It is not evidence about provider physical deletion.

Preserve unique local flight/logbook data first. Do not reset the iPad merely to make stale-tail evidence disappear.

`stale iPad rejected ≠ server key physically erased`; `stale iPad data preserved ≠ stale operation authorized`.

## SYNTHESIS 10 — closure is monotonic only while its dependencies remain current
A destruction/retirement proof bundle depends on successor authority, admission-floor enforcement, restore/reimport fencing, inventory scope and evidence provenance. If any of those dependencies materially changes, the relevant closure claim may require revalidation even though the historical deletion event remains true.

Example: provider key deletion remains a historical fact, but a later policy regression that accepts predecessor signatures breaks current-authority retirement. Conversely, a new inventory discovery of an external copy changes universal-erasure/residual-debt classification without falsifying the provider deletion event.

`historical deletion fact stable ≠ all closure claims permanently current`.

## MINTTAP DECISION / DIRECTION
1. Treat destruction evidence as provenance-bound records, not free-text receipts or boolean flags.
2. Bind every provider/HSM/vault event to exact logical authority, object/version/material ID, failure domain, lifecycle phase and observation time.
3. Keep provider lifecycle evidence separate from application-level predecessor rejection and restore/rejoin evidence.
4. Do not demand customer-observable physical proof where provider internals are inherently opaque; state the provider attestation scope explicitly.
5. If deletion and the only proof are controlled by the same suspected-compromised admin/evidence plane, downgrade closure and seek independent current-authority/negative evidence rather than self-certifying recovery.
6. Allow current-authority retirement to close before delayed provider erasure only when successor/floor enforcement and negative predecessor rejection are independently established; keep material destruction pending.
7. Treat backup/PITR/reimport as explicit resurrection edges. Quarantine recovered environments until current-floor reconciliation and predecessor negative tests pass.
8. Preserve a minimal non-secret closure package beyond ordinary audit-log retention; never retain retired private capability solely for auditability.
9. Treat newly discovered residual copies as claim-specific evidence changes: reassess threshold/current-consequence reach rather than rewriting the historical provider event.
10. Preserve unique long-offline PWA data and use stale clients as authority-rejection tests; never equate client cleanup with server-key destruction.

## DEPENDENCY / TRANSFER
- **Track A:** supplies exact Service Worker/storage/client-control semantics when stale-client tests depend on browser behavior. Browser evidence is not generalized into provider destruction.
- **Track B / Design Studio:** consumes explicit RETIRED-FENCED, DESTRUCTION-PENDING, PROVIDER-DESTROYED, RESIDUAL-COPY-UNKNOWN, RESTORE-QUARANTINED and BOOTSTRAP-REQUIRED states; no reusable visual system is invented here.
- **Track C:** owns execution of object-binding, stale-verifier, reimport, restore/PITR and long-offline-client destructive oracles once implementation evidence exists.
- **Track D:** observes lifecycle and rejection events, but analytics/log silence cannot close erasure or resurrection claims.
- **Software Engineering:** exact provider adapters, audit-event schemas, proof-store implementation, restore harness and runtime enforcement remain implementation handoffs. Current Studio evidence includes bounded macOS Safari runtime transfer but not Safari PWA lifecycle, physical iPad/EFB or product runtime.

## Track C destructive additions — 624 → 632 defined cases
1. **Wrong-generation receipt:** valid deletion receipt for object alias/current label is attached to a different historical key version than the retired authority → fail provenance binding.
2. **Self-attested compromised plane:** suspected-compromised admin/audit plane performs deletion and supplies the sole closure evidence; no independent successor/negative enforcement evidence exists → fail closure independence.
3. **Pending-provider/false-erasure:** predecessor is correctly fenced while provider deletion remains in reversible/delayed state, but report labels material physically destroyed → fail evidence semantics.
4. **Receipt-only application closure:** provider deletion is complete but a stale verifier still accepts predecessor signatures → fail current-authority retirement.
5. **PITR resurrection rejoin:** restored environment recreates stale policy/software keystore/admin reach and becomes writer before current-floor predecessor negative test → fail.
6. **Reimport resurrection:** imported source material recreates provider crypto capability and stale policy accepts it as current because bytes match → fail lineage/floor enforcement.
7. **Audit-retention amnesia:** ordinary provider audit retention expires and organization can no longer bind historical closure to object/version/successor evidence → fail durable provenance.
8. **Long-offline iPad stale-tail:** device returns with old worker/trust metadata and queued operation; server accepts historical authority because provider key is gone and assumes replay impossible → fail; preserve local data and require current bootstrap/re-admission.

These are **defined cases, not execution PASS**.

## VALIDATION
Generic PASS requires the Web Manager to bind destruction evidence to exact object/generation/scope; distinguish provider lifecycle attestation from independent current-authority enforcement; reason about compromised evidence planes without demanding impossible physical observation; separate delayed erasure from authority fencing; and make backup/reimport/PITR closure a tested rejoin property. This artifact meets that reasoning gate.

Production PASS remains OPEN until exact product/provider/HSM/vault/audit/backup/runtime evidence exists. Required evidence includes actual provider object/version IDs and origin/exportability; audit retention/export controls; successor/floor enforcement; stale-verifier negative tests; restore/PITR/reimport harness results; exact recovery topology; and managed-iPad stale-tail behavior.

## OPEN
- Actual MintTap/LogMate provider/KMS/HSM/vault objects, key origins/exportability and generation mapping.
- Actual provider/admin/audit failure-domain independence and audit retention/export configuration.
- Exact successor/admission-floor enforcement and stale-authority rejection at all consequence boundaries.
- Actual backup/PITR/reimport behavior and quarantine/rejoin workflow.
- Actual closure evidence store, retention and integrity controls.
- Physical iPad/Safari/WebKit/MDM stale-tail and data-preserving bootstrap behavior.
- Legal/aviation/investment/incident-evidence requirements affecting destruction and evidence retention.

## CHANGE WATCH
- NIST SP 800-88 Rev.2 is current final; monitor errata/FAQ and referenced standards.
- Google Cloud KMS and AWS KMS deletion/restoration/import/audit semantics are provider-specific and mutable.
- Provider audit retention, event schemas, multi-region behavior and key-import capabilities can change.
- Managed iPad/WebKit storage/update/runtime behavior remains execution-sensitive.

## Gate result
**PASS (generic).** Track E remains highest-risk owner. Track C destructive campaign reaches **632 defined cases**, with execution PASS explicitly unclaimed.

## Next highest-value adjacent question
**235 — closure-proof retention, evidence-store compromise & post-closure contradiction handling.** Determine how long claim-specific non-secret closure evidence must remain verifiable, how to preserve it without turning the evidence store into a new authority root, how to recover when evidence storage is corrupted/lost, and how a later contradictory discovery (residual key copy, stale verifier, restored policy path) reopens only the affected closure claims without rewriting historical facts or globally invalidating unrelated capabilities.