# 233 — PWA Recovery-Material Destruction Assurance, Unverifiable-Erasure Boundaries & Residual-Copy Containment

Status: **PASS (generic) / PRODUCT + PROVIDER + PERSONNEL + HSM/VAULT + BACKUP/MEDIA + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A stale-client/storage boundary; Track B recovery-state UX; Track C destructive retirement validation; Track D lifecycle observability.  
Dependencies: 223–232 dependency/discovery, anti-rollback/recovery, custody/rotation and recovery-authority inventory.

## Problem
232 established that recovery inventory is evidence rather than authority and that dormant copies can survive outside the expected topology. Retirement therefore needs a stronger question than “was delete clicked?” An HSM object may be disabled but recoverable; a cloud key may be scheduled for destruction yet restorable during a safety window; imported material may exist outside the provider; backup/PITR or offline media may preserve a capability; and a provider can often attest logical lifecycle state more strongly than a customer can independently prove physical bit-level erasure across every internal replica.

Central rule: **retirement assurance must distinguish use-fencing, revocation, cryptographic erase/key sanitization, logical/provider destruction and physical/media destruction. Do not claim universal erasure beyond the observable failure domains. Residual-copy uncertainty is bounded assurance debt only when successor authority plus enforcement makes any residual copy incapable of producing accepted current consequences; otherwise treat the uncertainty as a live compromise/recovery problem.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser-local Cache Storage/IndexedDB/Service Worker state can retain historical public/trust metadata or application data, but clearing a browser store is not proof that server recovery material is destroyed. Conversely, server key destruction must not be allowed to destroy unique offline flight/logbook data merely to simplify retirement.
- **B UX/IA/Content:** high dependency pressure. Must distinguish RETIRED-FENCED, DESTRUCTION-PENDING, DESTROYED-AT-PROVIDER, RESIDUAL-COPY-UNKNOWN and BOOTSTRAP-REQUIRED without telling users that reinstall/reset/network return proves secure erasure.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive retirement/residual-copy cases; campaign expands **616 → 624 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure destruction age, pending windows, negative-use attempts, residual-copy debt and restore/rejoin failures. Telemetry cannot prove universal erasure.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns retirement objective, failure-domain scoping, destruction evidence, successor fencing, backup/media resurrection analysis and compromise escalation.

## SOURCE

### NIST SP 800-88 Rev.2 — sanitization is assurance against feasible recovery, not a magical delete primitive
NIST SP 800-88 Rev.2 was finalized in September 2025 and supersedes Rev.1. It defines media sanitization around rendering access to target data infeasible for a given level of effort, strengthens validation/program governance, covers logical sanitization in modern/cloud environments, and gives cryptographic erase a dedicated treatment. NIST defines cryptographic erase as a purge technique where sanitizing confidentiality-protecting keys makes recovery of decrypted target data infeasible.

Sources:
- https://csrc.nist.gov/pubs/sp/800/88/r2/final
- https://csrc.nist.gov/news/2025/guidelines-for-media-sanitization-rev-2
- https://csrc.nist.gov/glossary/term/cryptographic_erase

**TRANSFER VALIDATION:** SP 800-88 is authoritative sanitization guidance, but a MintTap recovery signing key is not automatically equivalent to a media-encryption key. Cryptographic erase only achieves the intended objective when the destroyed key is actually the required confidentiality dependency and all relevant copies/escrows are covered.

### Provider lifecycle evidence is scoped evidence
Google Cloud KMS documents a scheduled-for-destruction state during which a key version cannot perform cryptographic operations but can be restored; after the configured period it becomes destroyed. Google also states that logical deletion from active systems begins at destruction and that key material can remain in Google systems for a bounded provider deletion period. For imported keys, re-importing the same external material is a separate possibility. AWS KMS likewise distinguishes disabling, pending deletion and deletion of imported key material; imported material can have copies outside AWS.

Sources:
- https://docs.cloud.google.com/kms/docs/destroy-restore
- https://docs.cloud.google.com/kms/docs/key-states
- https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-delete-key-material.html

**SYNTHESIS:** provider state is valuable evidence for that provider-controlled object/path, not proof that exported/imported/offline/backup copies elsewhere do not exist.

## SYNTHESIS 1 — define the retirement objective before choosing a destruction verb
Different controls answer different questions:
1. **USE-FENCED:** current enforcement rejects use of the material/path.
2. **REVOKED/DEAUTHORIZED:** policy no longer authorizes the identity/key/path.
3. **SANITIZED/CRYPTOGRAPHICALLY ERASED:** target data is infeasible to recover because required confidentiality key material has been sanitized, when CE preconditions hold.
4. **PROVIDER-DESTROYED:** provider lifecycle says its controlled key material is destroyed under documented semantics.
5. **PHYSICALLY DESTROYED/SANITIZED MEDIA:** applicable media sanitization evidence covers the physical medium.
6. **RESIDUAL-COPY-UNKNOWN:** no justified claim exists for every possible copy/failure domain.

These states may overlap but are not synonyms. `disabled ≠ destroyed`; `revoked ≠ erased`; `provider destroyed ≠ every exported copy destroyed`; `media destroyed ≠ successor authority established`.

## SYNTHESIS 2 — current authority safety can be stronger than universal erasure knowledge
For signing/recovery authority, the primary safety objective is often that retired material cannot create an accepted **current** authority transition. A residual old private copy can remain historically dangerous, but if all current verifiers/admission paths enforce a successor generation/floor and reject predecessor signatures, current consequence may be fenced even when universal physical erasure cannot be proved.

`residual bytes may exist ≠ residual bytes retain current authority`; `cannot prove universal erasure ≠ must pretend erasure happened`.

## SYNTHESIS 3 — negative consequence tests are distinct from destruction attestations
A provider destruction receipt proves a lifecycle event under provider semantics. A negative oracle proves that an obsolete credential/key/path cannot cause a current accepted consequence at a tested enforcement boundary. Neither substitutes for the other. Retirement closure should bind both when both claims matter.

`destruction receipt ≠ stale path rejected`; `stale path rejected ≠ physical material erased`.

## SYNTHESIS 4 — scheduled destruction is a transitional state, not closure
Safety windows intentionally permit recovery from accidental destruction. During that window the object may be unusable for normal crypto yet still restorable by an authorized administrative path. Treat this as DESTRUCTION-PENDING and inventory the restore authority separately. Closure occurs only after the relevant provider state and successor/retirement gates are satisfied.

`scheduled for destruction ≠ destroyed`; `currently unusable ≠ irrecoverable`.

## SYNTHESIS 5 — imported/exported material breaks provider-only closure
If key material originated outside a provider or was exportable, provider deletion can at most close the provider-controlled instance. The source material, escrow, transfer package, operator workstation, offline share, HSM clone/backup or other copies remain separate discovery/destruction obligations.

`cloud object deleted ≠ imported source deleted`; `one HSM zeroized ≠ all cloned/backup material zeroized`.

## SYNTHESIS 6 — backup/PITR resurrection must be tested at rejoin, not assumed away
Some backups restore data/configuration but not provider-managed key material; others may restore encrypted exports, software keystores, VM images, vault state or administrative reach. The relevant question is whether restoration can recreate usable retired authority or a path to it. Any restored predecessor must remain fenced from current consequence before the recovered environment rejoins.

`backup restored ≠ authority restored`; `retired object reappears ≠ retired authority reauthorized`.

## SYNTHESIS 7 — destruction evidence has an observation boundary
Evidence should state object identity, generation, destruction objective, controlling failure domain, provider/media method, initiation/completion times, reversible window, independent observation where available, restore/reimport possibility, negative consequence tests and known blind spots. Do not upgrade a provider assertion into a claim about provider internals or third-party/offline copies that were outside scope.

`certificate says destroyed ≠ universal erasure proven`; `audit event recorded ≠ all replicas/copies covered`.

## SYNTHESIS 8 — residual-copy uncertainty needs a decision rule
Treat residual uncertainty as **bounded assurance debt** only if:
- successor/current authority is independently established;
- every consequence-bearing verifier/enforcement path in the affected trust cut rejects predecessor material;
- restore/reimport/rejoin paths are fenced;
- unknown copies cannot satisfy current threshold/quorum alone or through a correlated path;
- monitoring/discovery and debt ownership remain active.

Escalate to **compromise/recovery** when any of those conditions is false or cannot be bounded. In particular, if an unknown residual share could combine with still-valid shares to meet a current threshold, destruction uncertainty is authority uncertainty, not bookkeeping debt.

## SYNTHESIS 9 — destruction must not erase the evidence needed to prove retirement
Preserve non-secret metadata, lineage, audit evidence and public verification material needed to explain which authority existed and why it is retired. Do not retain retired private capability merely for auditability. Destruction of secret material and retention of non-secret provenance are compatible goals.

`auditability required ≠ retain retired private key`; `private key destroyed ≠ retirement provenance should disappear`.

## SYNTHESIS 10 — PWA/client cleanup is not the server recovery control
A long-offline company iPad can retain old worker code, cached endpoints, historical public roots/checkpoints and queued operations. These are stale-tail state. Reinstall/reset may destroy useful local data and still says nothing about server-side recovery-key copies. Preserve unique local flight/logbook data first, bootstrap current trust, migrate worker/schema/policy, then re-admit queued operations under current authority.

`PWA cache cleared ≠ recovery key destroyed`; `app reinstalled ≠ server authority retired`; `retired server key ≠ delete unique local data`.

## SYNTHESIS 11 — physical/media destruction is not always the right closure target
For provider-managed non-exportable keys, customers may only have provider lifecycle evidence plus contractual/documented deletion semantics and negative-use evidence. Requiring impossible customer inspection of physical storage creates false rigor. Conversely, for customer-controlled offline media, a provider receipt cannot replace appropriate media sanitization/destruction evidence.

`unobservable physical layer ≠ invent physical-erasure proof`; `provider attestation sufficient for provider scope ≠ sufficient for customer-controlled media`.

## SYNTHESIS 12 — retirement closure is claim-specific
A useful closure bundle may contain: successor authority PASS; predecessor authorization revoked; obsolete operation negative tests PASS; provider/HSM state DESTROYED or appropriately SANITIZED; restore/reimport paths reconciled; offline/backup inventory disposition; residual-copy debt classification; and retained non-secret provenance. The exact bundle depends on what claim is being closed.

`retirement closed for current authority ≠ universal copy erasure proven`; `universal erasure unknown ≠ current authority necessarily unsafe`.

## MINTTAP DECISION / DIRECTION
1. Model destruction as multiple explicit states, never one boolean `deleted` field.
2. Separate **authority retirement** from **material erasure** and require evidence appropriate to each claim.
3. Prefer successor generation/floor enforcement and predecessor negative rejection as the primary current-authority safety boundary; destruction remains an additional lifecycle obligation, not a substitute for fencing.
4. Record provider/HSM/media semantics and reversible destruction windows explicitly.
5. Treat imported/exported/offline/backup material as separate failure domains and destruction obligations.
6. Preserve non-secret lineage/audit evidence while eliminating retired private capability where required.
7. Never claim physical/provider-wide universal erasure without evidence that actually covers that scope.
8. Classify residual-copy uncertainty as assurance debt only after affected current consequence paths are demonstrably fenced; otherwise invoke compromise/recovery handling.
9. Do not use PWA reinstall/cache clearing or destructive local reset as evidence of server recovery-material retirement.
10. Preserve unique LogMate-like local data before bootstrap/recovery actions; re-admit remote consequences only under current authority.

## DEPENDENCY / TRANSFER
- **Track A:** supply exact browser storage/Service Worker semantics when a product cleanup claim depends on them; browser cleanup is not generalized into key destruction.
- **Track B / Design Studio:** communicate pending/uncertain/bootstrap states without false “securely erased” certainty and without destructive recovery defaults.
- **Track C:** execute negative predecessor/reimport/restore/rejoin tests when implementation evidence exists; provider receipts alone do not close execution PASS.
- **Track D:** observe lifecycle/debt/rejection signals without promoting telemetry into destruction authority.
- **Software Engineering:** implementation-level HSM/KMS/vault/provider adapters, schema, backup restore and exact runtime negative tests remain a handoff; no product PASS inferred.

## Track C destructive additions — 616 → 624 defined cases
1. **Disable-as-destroy:** object is disabled/revoked but restorable; system labels it DESTROYED → fail.
2. **Pending-window false closure:** scheduled destruction is still reversible but retirement evidence closes material erasure → fail.
3. **Provider-only imported-key closure:** provider object is destroyed while external/import source survives and can recreate authority → fail.
4. **Receipt-without-negative-fence:** destruction receipt exists but stale verifier/admission path still accepts predecessor consequence → fail.
5. **Negative-fence-with-universal-erasure claim:** predecessor is correctly rejected but report falsely claims every copy is physically erased → fail evidence semantics.
6. **PITR resurrection:** restore reintroduces retired material/admin path and rejoins without current-floor negative test → fail.
7. **Long-offline iPad destructive reset:** recovery workflow deletes unique local flight/logbook data to eliminate stale state although server retirement is independent → fail.
8. **Residual-share threshold breach:** one residual/unknown share plus surviving authorized shares can still satisfy current recovery threshold, yet issue is classified only as low assurance debt → fail/escalate compromise recovery.

These are **defined cases, not execution PASS**.

## VALIDATION
Generic PASS requires the Web Manager to distinguish retirement, revocation, CE, provider destruction, physical sanitization and residual-copy uncertainty; scope destruction evidence to observable failure domains; reason correctly about imported/exported copies, pending destruction, backup resurrection and successor fencing; and preserve unique offline PWA data. This artifact meets that reasoning gate.

Production PASS remains OPEN until exact product/provider/HSM/vault/media/backup/runtime evidence exists. Required evidence includes actual key exportability/import provenance, provider deletion semantics, threshold topology, successor enforcement, restore/reimport controls, negative stale-authority tests, backup/PITR behavior, managed-iPad stale-tail behavior and relevant legal/aviation retention constraints.

## OPEN
- Actual MintTap/LogMate recovery key/share/HSM/KMS/vault topology and whether any material is exportable/imported.
- Actual provider destruction/backup/recovery semantics and contractual evidence.
- Exact threshold/quorum and successor-verifier/admission enforcement.
- Customer-controlled offline media and sanitization requirements.
- Legal, aviation, investment-record or incident-evidence retention requirements that constrain destruction timing.
- Physical iPad/Safari/WebKit/MDM stale-tail behavior and data-preserving bootstrap.

## CHANGE WATCH
- NIST SP 800-88 Rev.2 is current final as of this study; monitor its FAQ/errata and referenced sanitization standards.
- Provider KMS/HSM deletion, restoration, backup and imported-material semantics are provider-specific and mutable.
- Managed iPad/WebKit storage and OS/MDM erasure semantics remain platform/runtime-sensitive.

## Gate result
**PASS (generic).** Track E remains the highest-risk owner. Track C destructive campaign reaches **624 defined cases**, with execution PASS explicitly unclaimed.

## Next highest-value adjacent question
**234 — destruction-evidence provenance, provider-attestation independence & resurrection-proof closure.** Determine how to bind destruction receipts to exact object/generation/scope, avoid relying on the same compromised provider/admin plane for both deletion and proof, reconcile delayed provider deletion with current-authority fencing, and prove that backup/reimport/PITR/recovery paths cannot resurrect accepted authority after retirement without demanding impossible universal physical observation.