# 186 — PWA Transparency Archive Integrity, Historical-Verifier Isolation & Evidence-Deletion/Crypto-Erasure Governance

Status: **PASS (generic) / PRODUCT + SECURITY + ARCHIVE-TOPOLOGY + LEGAL/RETENTION + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A historical browser/cache state; Track B deletion/recovery UX; Track C destructive archive/verifier/deletion validation; Track D privacy-bounded evidence health.
Dependencies: 183–185 exact-artifact/transparency evidence, witness independence, evidence retention and key succession.

## Problem
185 separated current authority from historical verification material and established that compromise-era uncertainty must survive rotation/PITR. The adjacent problem is lifecycle closure: retained evidence can itself be modified, restored from stale backup, rendered unverifiable by verifier retirement, or retained indefinitely under the false banner of security. Conversely, deletion can destroy evidence needed for an active incident, legal hold or continuity claim. Crypto-erasure can make encrypted material practically inaccessible, but only when the actual key hierarchy, copies and implementation support the intended sanitization claim.

Central rule:

> **Archive evidence is evidence, not authority. Protect and verify its integrity independently enough for the claims it must support; isolate historical verification from current mutation authority; make deletion/hold/crypto-erasure explicit governed state transitions; and never let either retention or deletion silently rewrite incident history.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Cache Storage/IndexedDB/SW may retain or lose old evidence unpredictably and are not the durable archive or deletion oracle.
- **B UX/IA/Content:** consumer. Owns comprehensible states for local data preserved, remote evidence unavailable, deletion pending/blocked by policy where disclosure is appropriate, and verification uncertainty without exposing cryptographic internals.
- **C Performance/Accessibility/Quality:** validator. Owns archive substitution, stale restore, verifier sandbox escape, deletion/hold races, crypto-erasure false-success and offline-client campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Archive/deletion health telemetry must avoid raw evidence payloads and identity-rich retention dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns archive integrity, verifier isolation, deletion/hold state, sanitization evidence and recovery governance.

## SOURCE
### NIST SP 800-88 Rev.2 — current media-sanitization baseline
NIST SP 800-88 Rev.2 became final on 2025-09-26 and superseded Rev.1. It reframes sanitization as an organizational program, includes logical sanitization for modern/cloud environments, retains cryptographic erase as a technique, and emphasizes validation/assurance of sanitization outcomes. Rev.1 is withdrawn and must not be treated as the current baseline.

Sources: https://csrc.nist.gov/pubs/sp/800/88/r2/final ; https://csrc.nist.gov/news/2025/guidelines-for-media-sanitization-rev-2

**TRANSFER VALIDATION:** media sanitization is not identical to application-record deletion. The transferable principle is that deletion/sanitization claims require method, scope and validation appropriate to the actual storage/key topology.

### NIST SP 800-57 Part 1 Rev.5 — historical verification and current key use are different lifecycle concerns
SP 800-57 Part 1 Rev.5 remains the current final general key-management baseline. It covers key lifecycle, archive, backup, compromise, trust anchors and protection requirements. Historical public verification material may remain necessary after a key is no longer acceptable for new protection/signing; retaining verification capability does not imply retaining private signing authority.

Source: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

### RFC 3161 — long-lived evidence can outlive the finite lifetime of its original signing context
RFC 3161 notes that timestamping keys have finite lifetimes and describes re-timestamping/notarization/evidence-record approaches to renew confidence over time. It also notes privacy/linkability implications when identical message imprints are observable.

Source: https://www.rfc-editor.org/rfc/rfc3161.html

**TRANSFER VALIDATION:** RFC 3161 does not mandate a MintTap timestamp architecture. The transferable lesson is that long-term evidence validity is a lifecycle problem and that evidence metadata can itself create privacy linkage.

## SYNTHESIS — archive integrity is not archive authority
Keep these layers separate:
1. **authoritative current state** — current policy/admission/runtime authority;
2. **archive object** — retained historical checkpoint/conflict/provenance evidence;
3. **archive integrity envelope** — digest/signature/MAC/immutable-object identity or other mechanism used to detect substitution according to the real design;
4. **historical verification context** — versioned verifier, public keys, algorithms, canonicalization and policy needed to interpret old evidence;
5. **archive provenance** — where/when/how an archived object was captured, copied, compacted, migrated or restored;
6. **retention/hold state** — why evidence remains and whether ordinary deletion is suspended;
7. **deletion/sanitization state** — logical deletion, physical/media sanitization, cryptographic erase or other actual mechanism;
8. **deletion evidence** — bounded proof that the intended deletion/sanitization workflow completed and was validated.

Persistent guards:
- `archive readable ≠ archive authentic`;
- `archive signature valid ≠ archive complete`;
- `archive integrity PASS ≠ archived statement semantically legitimate`;
- `archive restored ≠ archive current`;
- `historical verifier retained ≠ historical verifier may authorize current mutation`;
- `legacy algorithm verifies history ≠ legacy algorithm approved for new signing`;
- `record hidden from UI ≠ record deleted`;
- `database row deleted ≠ all replicas/backups/caches sanitized`;
- `encryption key deleted ≠ crypto-erasure proven`;
- `crypto-erasure claimed ≠ every relevant key copy/wrapping path eliminated`;
- `legal/incident hold active ≠ retain unrelated data forever`;
- `retention period expired ≠ destroy active incident evidence blindly`;
- `PITR restored deleted evidence ≠ deletion automatically undone legitimately`;
- `deletion completed ≠ incident history may be rewritten`.

## Archive integrity and restore
An evidence archive should be able to detect substitution, truncation or stale restore to the extent required by its claims. The generic design does not mandate WORM, a public transparency log, a vendor or blockchain. It requires an explicit failure-domain analysis and authenticated identity/provenance sufficient to distinguish:
- the intended archived object from a substituted object;
- a complete retained set from a partial set where completeness is part of the claim;
- a current archive generation from a stale backup/PITR snapshot;
- an original captured object from a later migration/re-serialization;
- known conflict/compromise records from a pre-incident restore that lacks them.

A restore is therefore followed by reconciliation against surviving current retention/hold/security metadata before archive health is declared green. Missing intervals remain UNKNOWN when they cannot be reconstructed from authenticated surviving evidence.

## Historical-verifier isolation
Historical verification is potentially dangerous because it intentionally retains old parsers, canonicalization rules, algorithms and public-key contexts. Generic direction:
- version verifier context explicitly;
- make historical verification read-only with respect to current admission/mutation state;
- do not select verifier by trial-and-error downgrade until something passes;
- do not expose legacy verifier code on the primary consequence-bearing request path when architecture permits isolation;
- constrain input/output and resource use because old parser/verifier code can itself be an attack surface;
- preserve exact bytes/canonicalization evidence when old signatures depend on them;
- migrate or re-attest long-lived evidence only with provenance that preserves the distinction between original evidence and later assurance material.

**DEPENDENCY:** exact process/container/sandbox/API isolation belongs to Software Engineering/Security implementation evidence; no runtime PASS is claimed here.

## Deletion, retention and hold governance
Deletion is a governed state transition, not a boolean column. A generic evidence lifecycle can include:
`active evidence → retention eligible → deletion scheduled → hold blocks ordinary deletion → hold released/re-evaluated → deletion/sanitization executed → validation recorded → residual copies/backups age out or are sanitized according to policy`.

The exact legal basis, retention duration, aviation obligation, incident hold and user deletion rights are **OPEN**. Web Manager does not invent them.

Useful requirements:
- purpose/retention class is explicit and bounded;
- hold scope is evidence-specific rather than account-wide by default;
- hold creation/removal is auditable and cannot silently become permanent retention;
- deletion workflow accounts for replicas, backups, exports, caches and derived copies according to actual topology;
- restored backups reapply surviving deletion/hold state rather than resurrecting deleted authority/data silently;
- deletion evidence contains no more personal/business data than needed to prove the workflow.

## Cryptographic erase boundary
SP 800-88 Rev.2 treats cryptographic erase as a sanitization technique whose assurance depends on the implementation and key sanitization. Application-level crypto-erasure therefore cannot be claimed merely because one database key reference was removed.

Before relying on crypto-erasure, implementation evidence must establish, as applicable:
- target data was actually encrypted under the intended data-encryption key hierarchy;
- all relevant plaintext copies, caches, exports and replicas are understood;
- all usable copies/wrappings/backups of the key material are covered by the erase design;
- shared keys do not unintentionally erase unrelated retained evidence;
- externally managed keys/provider recovery paths do not preserve an undeclared decryption route;
- sanitization/key destruction completion can be validated;
- later PITR cannot restore usable key material without reconciling current deletion state.

`destroyed key handle ≠ destroyed all key material`.

Crypto-erasure may intentionally make content unrecoverable while a minimal tombstone/digest/deletion-event record survives. Whether that is lawful or useful for a real product is a legal/privacy/security/data-model decision, not a generic default.

## PWA/EFB boundary
A company iPad can hold local flight/logbook data, cached archive observations and obsolete verifier material while offline. Generic direction:
1. never treat local browser deletion as proof that server/archive copies were deleted;
2. never treat server deletion as proof that an offline client copy vanished;
3. preserve unique local operational records unless a verified product deletion policy specifically governs them;
4. on reconnect, obtain current deletion/retention/security state before remote queue drain;
5. do not let stale SW/IndexedDB verifier policy resurrect deleted remote authority or historical signing eligibility;
6. distinguish user-visible local-data removal from remote-account/evidence deletion status;
7. do not assume WebKit storage persistence, managed-device wipe, MDM behavior or background reconciliation without physical-device evidence.

This preserves offline utility without turning a managed iPad into either the authoritative archive or the deletion oracle.

## Privacy boundary
Security archives can become privacy dossiers. Generic minimization:
- retain claim-specific evidence, not maximal raw payloads;
- separate incident/security evidence from analytics;
- avoid stable device/user identifiers when checkpoint/generation/digest evidence is sufficient;
- do not retain raw flight/location/network history merely to make archive investigation convenient;
- deletion/hold metadata itself receives bounded access/retention;
- historical verification services should not become broad search interfaces over archived personal data.

## Track C destructive campaign
Define a **248-case generic campaign** spanning:
- archive object substitution with valid filename/metadata;
- truncation where latest checkpoint survives but conflict evidence disappears;
- stale PITR archive accepted as current;
- archive copy authentic but provenance lost;
- archive migration reserializes signed bytes;
- verifier selects obsolete algorithm by trial-and-error downgrade;
- legacy parser exploit attempts to escape read-only verifier boundary;
- historical verifier writes current admission state;
- old public key accidentally promoted to current trust anchor;
- old private signing key retained with verifier package;
- legal/incident hold races scheduled deletion;
- hold silently never expires/reviews;
- deletion removes active conflict evidence;
- deletion job reports success while replica/export remains;
- backup later resurrects deleted object;
- PITR restores erased key wrapping metadata;
- crypto-erasure deletes one key copy while provider recovery retains another;
- shared key erasure destroys unrelated evidence;
- crypto-erasure succeeds but plaintext export survives;
- crypto-erasure false-green due to unvalidated key destruction;
- deletion tombstone leaks excessive user/flight data;
- analytics receives hold/deletion incident payloads;
- long-offline iPad retains data after remote deletion;
- long-offline iPad locally deletes unique record before sync due to stale policy;
- stale SW serves obsolete verifier/deletion rules;
- IndexedDB eviction is mistaken for verified deletion;
- client reinstall is mistaken for fleet-wide sanitization;
- MDM wipe assumption is false on physical device;
- current server deletion state unavailable while local draft remains safe;
- reconnect drains queued privileged operation before deletion/security reconciliation;
- screen reader cannot distinguish local removal from remote deletion pending;
- human operator mistakes archive verification success for current authorization;
- archive service compromise attempts to become a new trust anchor.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat archives as evidence stores, never as current authorization sources.
2. Integrity-protect archive identity/provenance according to the claims that must survive and detect stale restore/known-conflict loss.
3. Isolate historical verification from current mutation/admission authority; retain old public verification capability only for bounded historical purposes.
4. Do not keep historical private signing authority merely to verify old evidence.
5. Model deletion, hold, sanitization and crypto-erasure as explicit governed transitions with validation, not UI/database booleans.
6. Use NIST SP 800-88 Rev.2, not withdrawn Rev.1, as the current media-sanitization baseline when that domain applies.
7. Never claim crypto-erasure without evidence for the actual encryption/key-copy/wrapping/backup topology and validation of key sanitization.
8. Reconcile PITR/restores against surviving current deletion/hold/security state before declaring archive recovery complete.
9. Preserve genuine incident/conflict evidence when a valid hold requires it, while keeping scope/purpose bounded; security is not a justification for indefinite unrelated retention.
10. Keep PWA client deletion/retention state non-authoritative; preserve unique local data unless verified product policy says otherwise and reconcile current server state on reconnect.
11. Keep product retention periods, legal holds, aviation obligations, provider topology, archive technology, key hierarchy and sanitization mechanism OPEN until canonical evidence exists.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate needs constitutional transparency archives at all: **OPEN**.
- Actual archive technology, replication, immutability/integrity mechanism and failure domains: **Software Engineering/Security dependency**.
- Actual verifier process isolation/sandboxing and supported legacy algorithms/parsers: **Software Engineering/Security dependency**.
- Actual encryption/key hierarchy, KMS/HSM/provider recovery and suitability for crypto-erasure: **OPEN**.
- Retention/deletion/legal-hold/user-right/aviation requirements: **Privacy/legal/aviation dependency**.
- Backup/PITR/export/cache/derived-copy topology: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad deletion/storage behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 248-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- NIST SP 800-88 Rev.2 is the current final sanitization baseline; re-check its FAQ and referenced standards before implementation.
- NIST SP 800-57 key-management revisions and post-quantum transitions may affect historical-verifier and algorithm-retirement policy.
- Legacy verifier/parser isolation is implementation-specific and must be revalidated as runtimes/toolchains age.
- Browser/iPadOS/MDM storage, wipe and background behavior remains change-sensitive.

## Adjacent next bottleneck
**PWA archive migration, algorithm-retirement & long-term evidence re-attestation without authority laundering**: determine how evidence remains interpretable when storage formats, canonicalization, signature/hash algorithms and verifier runtimes become obsolete; how later timestamps/re-attestations preserve original provenance without pretending to recreate original trust; and how long-offline clients converge after historical-verifier retirement.