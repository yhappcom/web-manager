# 232 — PWA Recovery-Authority Inventory Attestation, Dormant-Material Discovery & Succession Drift Detection

Status: **PASS (generic) / PRODUCT + PROVIDER + PERSONNEL + HSM/VAULT + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A long-offline/bootstrap state; Track B bounded recovery UX; Track C destructive inventory validation; Track D lifecycle observability.  
Dependencies: 215 inventory attestation; 223–225 dependency/discovery/drift; 229–231 fork recovery, custody/bootstrap, rotation/succession.

## Problem
231 made recovery-root rotation and custodian succession explicit authority transitions. Over years, however, authority can survive outside the intended current topology: an HSM object can remain enabled, a vault export or offline share can persist, a provider break-glass role can outlive its owner, backup/PITR can resurrect retired material, and a long-offline client can retain historical trust state. A canonical inventory that lists only what operators expect is therefore not proof that no other authority-bearing path exists.

Central rule: **inventory is an evidence system, not an authority system. Recovery-authority completeness requires reconciliation across independent discovery planes plus negative retirement tests; a listed object is not necessarily current, an unlisted object is not necessarily absent, and telemetry silence cannot authorize destructive cleanup or a weaker recovery policy. Inventory uncertainty must narrow consequence-bearing authority without destroying unique local data.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker, IndexedDB, Cache Storage and retained trust metadata can expose historical generations but cannot attest server-side recovery-material completeness or appoint current authority.
- **B UX/IA/Content:** high dependency pressure. Must distinguish LOCAL-SAFE / INVENTORY-UNCERTAIN / BOOTSTRAP-REQUIRED / CURRENT without telling users that reinstall, sign-in or network return proves recovery safety.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive inventory/orphan/drift cases; campaign expands **608 → 616 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure inventory coverage, orphan age, reconciliation lag and retired-path rejection, but analytics cannot establish authority completeness.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns recovery-object identity, inventory/discovery reconciliation, dormant-material containment, retirement evidence and capability-scoped response to uncertainty.

## SOURCE

### NIST SP 800-57 Part 1 Rev.5 — key inventory is a first-class key-management function
NIST SP 800-57 Part 1 Rev.5 section 9.2.1 requires key inventories to carry key metadata/reference information such as owner/sharer, key type, algorithm, use and expiration, and describes inventory as supporting compromise notification, owner de-authorization and algorithm/key replacement. It explicitly says an inventory need not contain secret/private key material unless also serving backup/archive functions.

Sources:
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf
- https://csrc.nist.gov/projects/key-management/key-management-guidelines

**TRANSFER VALIDATION:** this is strong precedent for accountable cryptographic inventory, not proof that one database is complete or that MintTap has any specific HSM/vault topology.

### NIST key-management function — accounting, storage/recovery, revocation/replacement and destruction are distinct
NIST's glossary sourced to SP 800-57 Part 2 Rev.1 defines key-management functions to include establishing keys/certificates, accounting for all keys/certificates, storage/recovery, revocation/replacement and destruction.

Source:
- https://csrc.nist.gov/glossary/term/key_management_function

**SYNTHESIS:** inventory/accounting is necessary but distinct from retirement/destruction. A record marked RETIRED does not itself make the underlying capability extinct.

### CISA asset-inventory precedent — discovery, classification and dependencies matter
CISA's 2025 asset-inventory guidance treats asset inventory as a maintained operational capability, including backup/recovery, remote access and security-management assets rather than only primary workloads. CISA ransomware guidance likewise recommends comprehensive logical/physical asset inventory and interdependency understanding.

Sources:
- https://www.cisa.gov/sites/default/files/2025-08/joint-guide-foundations-for-OT-cybersecurity-asset-inventory-guidance_508c.pdf
- https://www.cisa.gov/stopransomware/ransomware-guide

**TRANSFER VALIDATION:** OT/ransomware inventory is not a MintTap recovery-key protocol. The transferable principle is multi-class asset discovery plus dependency-aware inventory rather than application-only enumeration.

### OWASP secrets-management precedent — retirement requires revocation, not deletion from the visible configuration
OWASP recommends secret rotation/revocation and warns that removing a secret from current source/configuration does not erase historical copies such as repository history.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- https://cornucopia.owasp.org/cards/DVOQ

**TRANSFER VALIDATION:** this is supporting application-security guidance, not the authority for recovery-root custody design.

## SYNTHESIS 1 — recovery inventory records references and authority semantics, not secret bytes
Canonical inventory should identify an object/path without copying private material into the inventory plane. Useful fields include stable object/path identity, authority class, lifecycle state, generation, intended capability/scope, owner/sponsor/custodian set, storage/admin/recovery failure domains, provider/HSM/vault reference, predecessor/successor, last independent observation, retirement obligation and evidence status.

`inventory record exists ≠ secret material belongs in inventory`; `secret copied for inventory ≠ inventory improved`.

## SYNTHESIS 2 — completeness cannot be self-attested by one control plane
Reconcile multiple discovery planes: declared policy/IaC, HSM/KMS/vault enumeration, IAM/PAM/provider recovery paths, backup/PITR/media catalog, CI/CD and historical export locations, custody/personnel records, audit/use observations and negative retired-path tests. One plane owns no universal truth.

`inventory says complete ≠ discovery complete`; `provider list complete ≠ offline media complete`.

## SYNTHESIS 3 — distinguish CURRENT, RETIRED-VERIFIABLE, RETIREMENT-PENDING, ORPHAN, UNKNOWN and LOST
A binary active/inactive flag hides the security question. A retired public verifier may legitimately remain for historical verification while retired private recovery capability must not authorize new transitions. ORPHAN means discovered but not reconciled to legitimate ownership/lineage; UNKNOWN means evidence cannot establish state; LOST means expected material/path cannot be located and therefore may require loss/compromise handling.

`inactive ≠ retired`; `retired metadata retained ≠ retired private authority retained`.

## SYNTHESIS 4 — orphan discovery is a containment event, not automatic destruction
An unexpected HSM object, vault export, share or admin role must first be preserved as evidence and scoped. Immediate deletion can erase provenance or destroy the only bridge needed for legitimate recovery. But discovery also must not promote it to current authority.

`orphan discovered ≠ orphan authorized`; `orphan discovered ≠ delete immediately`.

## SYNTHESIS 5 — absence of use is weak evidence of absence of authority
Dormant recovery material is expected to be rarely used. Zero audit events, zero production calls or no recent access therefore cannot prove retirement. Prefer direct enumeration plus negative capability tests/fencing and independent administrative evidence.

`zero observed use ≠ zero latent authority`; `quiet key ≠ dead key`.

## SYNTHESIS 6 — succession drift is a graph problem
Personnel/provider/organization changes can alter who can reach HSMs, vaults, backups and break-glass paths even when key bytes and threshold configuration are unchanged. Reconcile inventory after material identity/PAM/provider/organizational changes and recompute failure-domain independence.

`same key identifier ≠ same custody graph`; `same threshold ≠ same reachability`.

## SYNTHESIS 7 — backup/PITR/media are part of the authority inventory when they can resurrect capability
If backup, snapshot, image, escrow or offline media can restore private recovery capability or an admin path, it is not merely data-retention inventory. Track its authority consequence, retention/expiry, custody and restore fencing. Test that restore cannot silently reintroduce a retired root into current authority.

`backup copy ≠ harmless historical copy`; `restored object verifies ≠ restored object current`.

## SYNTHESIS 8 — inventory attestations need provenance, scope, generation and observation interval
An attestation should state which discovery sources, scopes and generations were reconciled, when, with what blind spots and contradictions. A signature on `inventory complete=true` is not useful if scanners lacked permissions or offline media were out of scope.

`signed inventory ≠ complete inventory`; `fresh attestation ≠ complete scope`.

## SYNTHESIS 9 — inventory telemetry never lowers authority requirements
Inventory may trigger containment/review but cannot change thresholds, appoint a successor or declare a lost share harmless. If inventory completeness becomes uncertain across a relevant trust cut, consequence-bearing recovery/authority changes remain blocked or require the separately governed recovery path.

`inventory uncertainty ≠ threshold waived`; `telemetry majority ≠ recovery authority`.

## SYNTHESIS 10 — uncertainty should be capability-scoped
Do not convert one uncertain recovery object into indiscriminate data destruction or global application shutdown. Follow the dependency graph: preserve local capture/read/export where its trust cut is independent, while blocking recovery-root changes, remote destructive reconciliation or other consequences that depend on the uncertain authority.

`inventory uncertainty ≠ delete unique data`; `one unknown path ≠ every capability compromised`.

## SYNTHESIS 11 — long-offline PWA state belongs in stale-tail inventory, not recovery-authority inventory
A company iPad may retain old Service Worker/data/schema/trust checkpoints. Track supported stale-tail generations/horizons so return paths can be tested, but browser-local material is historical client evidence rather than a server recovery share. If it returns beyond the authenticated bridge horizon, preserve unique data and enter BOOTSTRAP-REQUIRED.

`stale client exists ≠ recovery share exists`; `old client root verifies history ≠ client can appoint current root`.

## SYNTHESIS 12 — inventory closure requires reconciliation plus negative retirement evidence
For a rotation/succession checkpoint, closure means expected current objects/paths are found and authenticated, expected retired paths are negatively fenced, contradictions/orphans are resolved or bounded as assurance debt, discovery coverage is current enough for the claim, and backup/PITR resurrection has been considered. Inventory rows alone are not closure.

`all rows reconciled ≠ retired authority extinct`; `asset count stable ≠ succession closed`.

## MINTTAP DECISION / DIRECTION
1. Maintain a reference/metadata inventory for recovery authority; do not centralize secret/private bytes merely to inventory them.
2. Reconcile independent discovery planes rather than allowing HSM, vault, IAM, IaC or telemetry alone to self-attest completeness.
3. Use explicit lifecycle/evidence states including CURRENT, RETIRED-VERIFIABLE, RETIREMENT-PENDING, ORPHAN, UNKNOWN and LOST.
4. Treat unexpected dormant material as evidence requiring containment and lineage analysis, not automatic authority or automatic deletion.
5. Require direct/negative retirement evidence because zero observed use is insufficient for dormant authority.
6. Recompute custody/failure-domain reachability after personnel/provider/organization/PAM changes even when key bytes are unchanged.
7. Include backup/PITR/offline media in authority analysis whenever restoration can resurrect recovery capability.
8. Bind inventory attestations to scope, generation, source coverage, provenance and observation interval; preserve blind spots/contradictions.
9. Never let inventory telemetry lower thresholds or appoint successor authority.
10. Scope degraded operation by dependency graph; preserve unique local data while withholding consequences that depend on uncertain authority.
11. Track long-offline PWA stale-tail generations separately from recovery-key inventory and require governed bootstrap beyond the bridge horizon.
12. Close rotation/succession inventory only with reconciliation plus negative retirement/resurrection evidence.

## Track C destructive campaign — +8 defined cases
609. **Self-attesting HSM inventory:** HSM enumeration reports all expected objects but scanner lacks access to a legacy partition; completeness claim must fail.
610. **Quiet orphan mistaken for extinct:** unreferenced vault export has no audit use for years and is declared harmless; require lineage/containment and retirement evidence.
611. **Backup resurrects retired root:** PITR restores an old HSM/vault reference or private recovery capability; current authority must reject/fence it.
612. **Departed custodian survives through provider recovery:** primary account is disabled but provider break-glass/PAM path still reaches recovery material; succession closure must fail.
613. **Signed but scope-incomplete attestation:** inventory attestation is authentic but excludes offline media/backup domain; completeness claim must fail.
614. **Orphan auto-delete destroys only legitimate bridge:** scanner deletes unknown recovery artifact before provenance analysis; recovery process must preserve evidence and avoid destructive automation.
615. **Telemetry-driven threshold downgrade:** missing inventory object is treated as permanently lost and threshold is reduced from remaining telemetry; reject absent separately legitimate loss-recovery authority.
616. **Long-offline iPad conflated with recovery authority:** historical client root/Service Worker state is counted as a current recovery share or allowed to select newest root; preserve local data and require authenticated bootstrap.

These are **defined destructive cases, not executed PASS evidence**.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate HSM/KMS/vault/provider/PAM/backup/offline-media topology: OPEN.
- Actual recovery keys/shares, custodians, exports, break-glass paths and inventory system: OPEN; do not infer existence.
- Discovery-source permissions, coverage, identifiers, event ordering and reconciliation implementation: OPEN.
- Actual negative retirement/destruction tests and backup/PITR resurrection behavior: OPEN.
- Actual managed iPad/iPadOS/WebKit/MDM stale-tail inventory and bootstrap horizon: OPEN.
- Legal/aviation requirements for custody, destruction, retention and evidentiary preservation: specialist evidence required.
- Physical-device, representative-human, AT and canonical-product runtime validation: OPEN.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev.5 remains current final; Rev.6 Initial Public Draft (2025-12-05) remains non-final and includes expanded keying-material storage discussion/PQ material.
- NIST/CISA inventory guidance and provider/HSM inventory APIs are implementation/freshness-sensitive; product controls require current provider evidence.
- Browser/iPadOS/MDM behavior remains version-sensitive and requires physical-device validation.

## Gate judgment
**232 PASS (generic).** We can define recovery-authority inventory semantics, distinguish inventory from authority, reconcile multi-plane discovery, reason about dormant/orphaned material and succession drift, include resurrection paths, and degrade capability safely when completeness is uncertain. Product/provider/personnel/HSM/vault/device/runtime validation remains OPEN.

## Next highest-value adjacent question
**233 — recovery-material destruction assurance, unverifiable-erasure boundaries & residual-copy containment:** determine what can actually be proven when HSM objects, vault exports, offline media, snapshots or historical provider copies are retired; distinguish cryptographic erasure/revocation/fencing from physical deletion; avoid claiming impossible universal erasure; and define when residual-copy uncertainty becomes bounded assurance debt versus compromise requiring wider authority replacement.