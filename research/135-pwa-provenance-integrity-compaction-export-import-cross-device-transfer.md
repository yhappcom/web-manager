# 135 — PWA Provenance Integrity Under Compaction, Export/Import & Cross-Device Transfer

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + CRYPTO/KEY + BACKUP VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 122–126 evidence/key/verifier recovery; 131–134 reconciliation/provenance; Track A browser-storage/file-transfer mechanics; Track B truthful transfer/recovery UX; Track C corruption/truncation/replay/cross-device oracles; Software Engineering owns eventual serialization/import implementation.

## Purpose

134 defined authoritative acceptance units and partial-history recovery. The adjacent problem is preservation of provenance when lineage is intentionally reduced, exported from one trust/storage context, imported into another, or merged with another device lineage.

Central rule:

> **Compaction, export, transport, import and merge are provenance transformations, not transparent moves. Preserve enough identity, integrity metadata and transformation provenance to state exactly what survived; never convert content unavailability, successful transport, or current authorization into a claim of historical continuity.**

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** browser storage and file/share mechanisms determine what bytes can actually be exported/imported; they do not supply historical trust automatically.
- **B UX/IA/Content — elevated consumer:** owns truthful `backup verified / imported / history compacted / source unavailable / review required` explanations.
- **C Quality — high dependency pressure:** owns byte corruption, truncation, manifest mismatch, duplicate import, partial merge, replay and physical-device transfer tests.
- **D Search/Analytics — constrained consumer:** transfer telemetry can measure outcomes but cannot certify package integrity or lineage.
- **E Architecture/Security/Operations — highest-risk owner:** owns package boundaries, integrity/authenticity semantics, import authority, custody, compaction and recovery interpretation.

Allocation remains E-heavy, with A/C prerequisite-critical and B increasingly important because transfer states are user-visible.

## 2. SOURCE — provenance can itself have provenance

The W3C PROV family is a Recommendation framework for representing and interchanging provenance. PROV bundles allow a set of provenance statements to be named and treated as an entity so that provenance can be expressed about that provenance bundle itself.

Sources checked 2026-09-19:
- https://www.w3.org/TR/prov-overview/
- https://www.w3.org/TR/prov-dm/

**SYNTHESIS:** an exported or compacted provenance package should not masquerade as the original source history. It may be a new derived package with its own exporter, time, policy/version and relationship to source entities.

Guards:
- `exported copy ≠ original storage context`;
- `derived provenance package ≠ original provenance event`;
- `imported successfully ≠ historical attribution newly established`.

## 3. SOURCE — hash/signature semantics do not imply content availability

NIST FIPS 186-5 states that digital signatures can detect unauthorized modification and authenticate the signatory. RFC 9995, published July 2026 as a Proposed Standard, defines a COSE Hash Envelope that can sign/MAC a hash output and explicitly distinguishes payload integrity/identification from availability of the original payload; it provides content-format and availability hints for optional discovery.

Sources checked 2026-09-19:
- https://csrc.nist.gov/pubs/fips/186-5/final
- https://www.rfc-editor.org/rfc/rfc9995.html

**SYNTHESIS:** a retained digest/checkpoint can prove equality/integrity relative to bytes when those bytes are available, but it does not recreate deleted content. A valid signature over a digest authenticates the signed statement under its key/trust context; it does not prove completeness of omitted history or current authorization.

Guards:
- `hash retained ≠ content retained`;
- `hash matches ≠ package complete`;
- `signature valid ≠ omitted history complete`;
- `historical signature authentic ≠ current import/write authority`.

**CHANGE WATCH:** RFC 9995 is new (July 2026). It is evidence for semantics, not a MintTap/LogMate format decision.

## 4. Compaction is a lossy provenance transformation unless proven otherwise

Compaction may retain checkpoints, revision IDs, operation IDs, selected decision facts, hashes or summaries while discarding payload/detail. The compacted artifact must identify:
1. source lineage/range covered;
2. compaction policy and version;
3. what classes of detail were removed;
4. retained integrity/checkpoint material;
5. compaction actor/tool and time;
6. whether original material remains discoverable elsewhere;
7. whether exact reconstruction is possible, partial, or impossible.

Do not call a compacted chain `complete history` merely because its checkpoint hashes validate.

Guards:
- `compacted chain verifies ≠ original detail recoverable`;
- `checkpoint continuity ≠ semantic completeness`;
- `summary retained ≠ rejected/corrected branch retained`.

## 5. Export package boundary

A consequence-bearing portable package should have a manifest/envelope that binds, as appropriate:
- package/export identity and format version;
- source installation/device lineage identifier without pretending device identity equals user identity;
- source authoritative revision/range or provenance heads included;
- artifact inventory with stable identifiers, media/format version and integrity digests;
- compaction/redaction declarations;
- exporter/tool/version and export time;
- encryption/confidentiality metadata when used;
- signature/MAC/checkpoint metadata when used;
- external-content references plus explicit availability status;
- package completeness scope: what the package claims to contain, not `all history` by implication.

OWASP's current APTS evidence-package appendix is non-normative but usefully illustrates a manifest that inventories artifacts, hashes them, records provenance/redaction and supports downstream export integrity. It is supporting evidence, not a Web/PWA standard.

Source checked 2026-09-19:
- https://owasp.org/APTS/standard/appendix/Evidence_Package_Manifest.html

Guard: `manifest present ≠ manifest trustworthy`; the manifest itself needs integrity/custody protection appropriate to consequence.

## 6. Integrity, authenticity, completeness and confidentiality are separate

For an imported package ask independently:
- **Integrity:** are these the bytes represented by the package/checkpoint?
- **Authenticity/attribution:** who/what produced or attested them, under which trust context?
- **Completeness:** does the package contain every item it claims for the declared scope? Are gaps explicit?
- **Confidentiality:** was sensitive content protected during storage/transport/custody?
- **Interpretability:** are schema/canonicalization/verifier semantics still available?
- **Current authorization:** may this importer/device/account publish or mutate remote state now?

No one property substitutes for another.

Guards:
- `integrity PASS ≠ authenticity PASS`;
- `authentic package ≠ complete package`;
- `complete package ≠ confidential package`;
- `decryptable ≠ trustworthy`;
- `trustworthy historical package ≠ currently authorized writer`.

## 7. Import is admission into a new trust context

Import must not silently turn portable bytes into authoritative current state. A generic import pipeline is:
1. preserve original package bytes/read-only reference when consequence warrants;
2. parse format/version without mutating authority;
3. verify manifest/checkpoints/signatures against available verifier context;
4. classify missing/unverifiable content explicitly;
5. map source lineage/identities without overwriting local identities;
6. detect duplicate package/operation/revision imports;
7. perform schema/policy compatibility checks from 132;
8. reconcile against current authoritative revision/policy from 131;
9. create a new import/admission provenance event;
10. only then publish accepted effects under current authorization.

Guards:
- `file opened ≠ import accepted`;
- `package verified ≠ records admitted`;
- `records admitted ≠ remote mutation authorized`;
- `fresh login ≠ imported operation fresh`.

## 8. Cross-device lineage: transfer is not identity collapse

When device B imports device A's package, B must not rewrite A-originated events as B-authored events. Preserve at least:
- original logical operation/event identity;
- source lineage/device/install identity where justified;
- original actor attribution if independently known;
- export/import transformation identity;
- destination admission/reconciliation result.

A device identifier is evidence about a client lineage, not proof of the human actor by itself.

Guards:
- `copied to device B ≠ authored by device B`;
- `same user account ≠ same device lineage`;
- `device lineage ≠ human identity`;
- `new local record ID ≠ new historical event`.

## 9. Merge of independent device histories

Two offline devices may carry overlapping, divergent or causally related histories. Merge should first determine whether items are:
- identical logical operation already seen;
- same base revision with independent operations;
- descendant/ancestor lineage;
- conflicting edits;
- delete/tombstone vs stale update;
- compacted checkpoint with unavailable underlying detail;
- unknown relationship because lineage evidence is missing.

Do not concatenate histories and infer global order from wall clocks. Preserve branch identity until current conflict policy can adjudicate it.

Guards:
- `two valid histories ≠ one automatically ordered history`;
- `later device clock ≠ later authoritative intent`;
- `same resulting value ≠ same provenance`;
- `merge succeeded structurally ≠ semantic convergence proven`.

## 10. Compaction and deletion boundaries

A checkpoint can permit integrity verification of retained/available content while privacy/retention policy removes unnecessary payload. But if removed content was the only evidence for a material historical claim, the assurance state must be downgraded rather than reconstructed from the checkpoint.

Possible states include:
- **FULL-CONTENT VERIFIED**;
- **COMPACTED-CONTINUITY VERIFIED / DETAIL UNAVAILABLE**;
- **PACKAGE-INTEGRITY VERIFIED / SOURCE TRUST UNVERIFIED**;
- **SOURCE-AUTHENTIC / PACKAGE-INCOMPLETE**;
- **IMPORTED / RECONCILIATION-PENDING**;
- **ADMITTED-CURRENT**;
- **UNVERIFIABLE-GAP**.

`UNVERIFIABLE-GAP` is not automatically `INVALID`, but neither is a complete PASS.

## 11. PWA/EFB boundary

For a company-iPad PWA, an export/import path may be strategically valuable because browser-local irreplaceable data cannot be assumed to survive indefinitely. But generic Web APIs do not make an exported file a verified backup, nor do they make a second device an unattended synchronization peer.

Product validation must separately prove:
- what WebKit/iPadOS/managed-device policy permits for file creation/share/import;
- whether all required IndexedDB records/provenance are captured consistently;
- interrupted export/import behavior;
- package confidentiality at rest/in transit;
- destination storage durability;
- user-visible recovery semantics;
- current server-side admission and authorization after import.

Guards:
- `export button works ≠ backup verified`;
- `backup file exists ≠ restore tested`;
- `restore tested in desktop browser ≠ managed-iPad restore PASS`;
- `cross-device import ≠ automatic device-to-device sync`.

## 12. User-visible boundary

Track B should expose consequences rather than cryptographic jargon. Distinguish, where material:
- backup/export created;
- package verified;
- some historical detail was intentionally compacted/unavailable;
- imported locally;
- duplicate/already imported;
- reconciliation required;
- accepted as current;
- cannot verify source/history;
- source verified but current write permission unavailable.

Never label a package `safe`, `complete`, or `synced` based on one check.

Design Studio W086 supplies useful served-runtime reasoning about branch eligibility and stale recovery controls, but persistence/offline/Sync, cross-browser/Safari/Firefox, screen reader, physical device and human UX remain OPEN. No PWA transfer UX PASS transfers.

## 13. Privacy/security boundary

Portable packages increase exfiltration and custody risk. Minimize payload to the justified recovery/audit objective; do not place credentials, reusable session tokens or unnecessary secrets in a provenance package. Encryption protects confidentiality but not necessarily provenance authenticity or completeness. Signature/HMAC/key choice and recovery are architecture-specific and remain OPEN until the actual threat model/key hierarchy exists.

Guards:
- `encrypted export ≠ authentic export`;
- `signed export ≠ confidential export`;
- `portable recovery ≠ portable authority credential`.

## 14. Track C validation campaign

1. export identical state twice → deterministic identities/digests only where format promises determinism;
2. flip one artifact byte → integrity failure;
3. truncate package → completeness/integrity failure;
4. remove manifest entry/artifact → declared-scope mismatch;
5. alter manifest without valid integrity protection → detect;
6. valid manifest + missing externally referenced payload → content unavailable, not hash failure;
7. valid hash + wrong semantic parser/schema → interpretability failure;
8. signature valid under retired historical key → historical authenticity may remain; current authority does not revive;
9. unknown signer/verifier context → UNVERIFIABLE, not guessed trust;
10. encrypted package with wrong key → confidentiality access failure, not proof of corruption;
11. compact history retaining checkpoint → continuity claim limited to retained scope;
12. request removed detail after compaction → unavailable, never reconstructed from hash;
13. duplicate package import → one logical admission/import identity;
14. same package ID with different bytes → reject/quarantine;
15. same operation ID from two packages/same payload → dedup;
16. same operation ID/different payload → reject/quarantine;
17. device A export → device B import → original source lineage preserved;
18. device B re-export → export/import transformations remain distinct from original authorship;
19. two divergent offline device branches → no wall-clock LWW by default;
20. tombstone on A + stale update on B → no silent resurrection;
21. compacted branch + full branch merge → missing detail remains explicit;
22. interrupted export → no false `backup complete` state;
23. interrupted import before local commit → no partial accepted state;
24. import local commit then UI/process termination → reopen discovers actual state;
25. import accepted locally, remote authorization revoked → preserve local recovery; remote mutation denied;
26. package from obsolete schema/policy → migrate/review under 132, no semantic re-authorization;
27. redacted export → redaction declaration retained through re-export;
28. analytics says import success while authoritative admission fails → telemetry cannot certify admission;
29. accessible import/reconciliation flow retains semantic focus and branch ownership;
30. physical Safari/iPadOS managed-device export/import/restart/eviction/reconnect remains required before product PASS.

## 15. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W086 BRANCH-ELIGIBILITY SERVED-RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen reader, physical-device, field-CWV, full-WCAG and human UX remain OPEN.

Software Engineering implementation evidence remains bounded dependency only. Web Manager does not select serialization, database, crypto library, file format or sync transport here.

## 16. MINTTAP DIRECTION

For PWA/EFB-like products, treat compaction/export/import/merge as explicit provenance transformations. Bind portable artifacts to a scoped manifest/envelope, preserve source lineage and transformation provenance, distinguish integrity/authenticity/completeness/confidentiality/interpretability/current authorization, and make import a current-policy admission process rather than authority restoration by file possession. Preserve compacted/unverifiable gaps truthfully.

No production export format, cryptographic scheme, device identifier, backend or LogMate implementation is inferred here.

## 17. OPEN / DEPENDENCY / CHANGE WATCH

**OPEN:** actual MintTap/LogMate export/import requirement; data classes; privacy/legal/aviation retention; source/device identity; package format; canonicalization; encryption/signature/MAC/key hierarchy; verifier recovery; browser file APIs; managed-iPad policy; backup destination; merge policy; server admission; schema/version horizon; real physical-device restore.

**DEPENDENCY:** Software Engineering owns implementation-level serialization/transactions/crypto/file handling and executable import tests once stack/product truth exists. Track B/Design Studio own concrete transfer/recovery UX. Track C owns cross-browser/device destructive validation.

**CHANGE WATCH:** RFC 9995 (July 2026) is newly published and useful for hash-envelope semantics but is not a product mandate. WebKit/iPadOS file/share/storage behavior and managed-device policy require current physical/runtime evidence.

## 18. Gate

**PASS (generic).** The Web Manager can distinguish compaction from complete history, design a scoped portable provenance package, separate integrity/authenticity/completeness/confidentiality/interpretability/current authorization, preserve lineage across import/re-export, diagnose divergent cross-device histories, and apply these boundaries to PWA/EFB recovery without inventing product facts.

Product, managed-iPad, data-model, cryptographic/key, backend and destructive-runtime validation remain OPEN.

## 19. Next highest-value adjacent work

**PWA provenance fork detection, checkpoint anchoring & anti-splicing governance**: determine how to detect omission/reordering/splicing of individually valid provenance segments across exports, compaction epochs and device branches; distinguish cryptographic continuity from semantic legitimacy; govern checkpoint anchoring without assuming blockchain/transparency-log infrastructure is required.