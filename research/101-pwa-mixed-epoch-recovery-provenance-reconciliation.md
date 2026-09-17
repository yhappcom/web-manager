# 101 — PWA Mixed-Epoch Recovery Provenance & Reconciliation

Status: **PASS (generic) / PRODUCT RECOVERY-MANIFEST + RECONCILIATION VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A storage/browser mechanics; 091 release coexistence; 094 key lifecycle; 098 stale-client trust; 099 trust-policy authenticity; 100 trusted-state reset/rebootstrap; Software Engineering D003/D005/D006.

## Purpose

100 established that a restore is a state-composition event: user records, trust metadata, encryption-key state, schema/protocol generation and pending outbox can survive or be restored from different points in time. This study asks the next operational question: **what evidence is sufficient to treat that composed state as coherent, and what must be quarantined or reconciled before replay?**

The goal is not to invent a MintTap/LogMate database or cryptographic design. It is to define a web/PWA recovery acceptance contract that Software Engineering can implement and target devices can validate.

---

## 1. Track allocation

- **A Platform/Browser — dependency supplier.** Origin storage can disappear or be restored independently of server state; browser persistence does not supply recovery provenance.
- **B UX/IA/Content — consumer.** Recovery UI must distinguish `restored`, `verified`, `compatible`, `reconciled`, `sync-ready` and `quarantined`; one generic `Restore complete` state is insufficient.
- **C Performance/Accessibility/Quality — validation owner.** Must test partial/mixed restores, missing components, stale outbox, incompatible readers, interrupted reconciliation and accessible recovery states.
- **D Search/Discovery/Analytics — low direct pressure.** Analytics timestamps/event IDs are not authoritative recovery provenance or sync checkpoints.
- **E Architecture/Security/Operations — highest-value owner.** Owns recovery manifest semantics, provenance/authenticity boundary, compatibility gating, quarantine and replay authorization.

**Allocation:** E remains the highest-risk bottleneck; Software Engineering D003/D005/D006 are consumed rather than duplicated.

---

## 2. SOURCE — integrity is not provenance or semantic acceptance

### RFC 9530 — HTTP Digest Fields

RFC 9530 defines `Content-Digest` and `Repr-Digest` for integrity of HTTP content/representations. It explicitly states that the digest fields do not provide authentication, authorization or privacy, and that a malicious actor can substitute both content and digest unless another mechanism authenticates them. It also distinguishes content integrity from representation integrity.

Source: https://www.rfc-editor.org/rfc/rfc9530.html

**SYNTHESIS:** a hash can prove that bytes match a referenced digest under the assumed algorithm. It does not prove who authorized those bytes, when they belonged to the user's accepted state, which schema/key/protocol can interpret them, or whether replay is safe.

**Guards:**
- `hash matches ≠ artifact provenance established`;
- `artifact provenance established ≠ application semantics accepted`.

### NIST digital-evidence preservation

NIST's digital-evidence work emphasizes reliable capture/preservation without unintended alteration and traceability of digital objects. This is forensic evidence guidance rather than a PWA backup standard, but the transferable principle is useful: integrity evidence is stronger when acquisition/source identity and preservation history are retained rather than relying only on a final file's existence.

Sources:
- https://www.nist.gov/digital-evidence
- NISTIR 8387: https://www.nist.gov/publications/digital-evidence-preservation-considerations-evidence-handlers

**TRANSFER VALIDATION:** use provenance/traceability as an operational principle only. Do not claim forensic chain-of-custody requirements apply to ordinary PWA backups.

### OWASP key-management recovery boundary

OWASP Key Management guidance notes that encrypted data whose required encryption keys are lost cannot be recovered, and distinguishes backup/escrow considerations for encryption keys from signing keys.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

**SYNTHESIS:** a record artifact can be intact while its required key generation is unavailable. Conversely a key can be available while the ciphertext/metadata it belongs to is stale or missing.

**Guard:** `ciphertext intact ≠ decryptable ≠ correctly bound to the restored key generation`.

---

## 3. Consume Software Engineering evidence rather than recreating it

### D005 — recovery acceptance pipeline

Software Engineering D005 establishes with executable SQLite fixtures that backup existence, physical integrity, schema compatibility, semantic validity and safe publication are distinct claims. Its bounded validate-before-publish model preserves last-known-good state when an invalid candidate or pre-publication failure occurs.

**TRANSFER:** PWA recovery should stage restored/composed state as a candidate and validate it before enabling destructive replacement or remote replay when architecture permits.

**Guard:** `restore bytes copied ≠ recovery candidate accepted ≠ live state safely published`.

### D003 — schema compatibility

D003 demonstrates that schema migration is a protocol across readers/writers/stored state/migration metadata, and that a newer schema can make an older reader fail. It also demonstrates that version metadata alone does not prove migration success.

**TRANSFER:** a recovery manifest's `schemaGeneration=N` is descriptive metadata, not an acceptance oracle. The actual reader must validate compatibility and required invariants.

**Guard:** `schema version label matches ≠ migration/reader acceptance proven`.

### D006 — replay, acknowledgement and stale operations

D006 demonstrates bounded failures where ambiguous retry duplicates an effect without stable logical operation identity and where a stale update can resurrect a deleted record if deletion history is discarded.

**TRANSFER:** restored outbox entries must retain logical operation identity, acknowledgement/replay state and compatibility context. Replaying every restored pending item merely because it is present is unsafe.

**Guard:** `outbox item present ≠ never applied remotely ≠ replay authorized`.

---

## 4. Recovery is a vector of epochs, not one timestamp

A candidate recovery state can be modeled conceptually as a vector, not as a single `backupDate`:

`R = <recordEpoch, trustGeneration, keyGeneration, schemaGeneration, protocolGeneration, outboxCheckpoint, serverAckCheckpoint, backupIdentity>`

These dimensions do not necessarily advance together.

Examples:
- records from Tuesday + trust metadata from Monday;
- records from Tuesday + key generation rotated Wednesday;
- schema V4 records + application reader only validated through V3;
- outbox captured before a remote acknowledgement that occurred later;
- trust generation 42 + protocol generation 7 where server now rejects protocol <9;
- backup file created after records were written but before all IndexedDB transactions/outbox metadata reached a declared consistency point.

**Guard:** `one backup timestamp ≠ one coherent application epoch`.

A wall-clock timestamp is also not a universal causality token. Clock skew, offline operation and asynchronous acknowledgements can make chronological labels insufficient to prove dependency ordering.

**Guard:** `later timestamp ≠ causally newer state`.

---

## 5. Recovery manifest — requirements, not implementation choice

A recoverable system benefits from an explicit manifest or equivalent independently inspectable metadata. This study does not prescribe JSON, a database table or a cryptographic envelope. The logical contract should be able to identify, where applicable:

- product/application identity and environment;
- backup/artifact identity;
- declared consistency point / creation procedure;
- record-store representation/schema generation;
- trust-policy/root generation or explicit `unknown`;
- encryption/wrapping-key generation references without exposing secret material;
- protocol/API generation expected by queued operations;
- outbox logical-operation identities and local state/checkpoint;
- known remote acknowledgement/reconciliation checkpoint, if one exists;
- source device/profile identity where product policy uses it;
- artifact digests/integrity evidence;
- provenance/authenticity evidence if the threat model requires it;
- compatibility/readers required to interpret the state;
- manifest format/version itself.

**Important:** a self-reported manifest stored beside the data can improve diagnosability but is not independent authenticity proof.

**Guard:** `manifest present ≠ manifest authentic ≠ components mutually coherent`.

If authenticity is security-critical, 099's independent authority/bootstrap problem applies to the manifest as well.

---

## 6. Acceptance pipeline for mixed-epoch recovery

Generic recovery should proceed through explicit gates rather than a binary restored/not-restored flag.

### Gate 0 — preserve current known-good state

Do not destroy the current accepted state merely to inspect a restore candidate when the architecture permits candidate staging. This consumes D005's validate-before-publish principle.

### Gate 1 — artifact integrity/readability

Can each required artifact be read and does integrity evidence match? Missing or corrupted members fail closed for operations that depend on them.

This does not establish provenance.

### Gate 2 — provenance/authenticity

Can the system establish where the candidate came from and, where required by the threat model, that the manifest/artifact was authorized rather than merely intact?

Unknown provenance need not imply record deletion; it may require quarantine or reduced capabilities.

### Gate 3 — cryptographic availability/binding

Are required keys available and valid for the referenced encrypted components? Does the metadata bind the expected key generation to the ciphertext/records being interpreted?

Do not silently try unrelated keys until plaintext happens to parse.

### Gate 4 — reader/schema/domain acceptance

Can the current application actually interpret the schema and validate required domain invariants? Version labels alone are insufficient.

### Gate 5 — trust/protocol compatibility

Is restored trust state current or safely rebootstrap-able? Is the queued operation protocol still accepted? A valid record store does not make an obsolete bridge/protocol safe.

### Gate 6 — outbox/ack reconciliation

For every queued logical operation, determine whether it is:
- definitely unacknowledged and replayable;
- already acknowledged/deduplicable;
- stale/obsolete under newer state;
- conflicting and requiring domain reconciliation;
- incompatible with the current protocol/schema;
- unknown and therefore unsafe for blind replay.

### Gate 7 — publication / capability enablement

Only after applicable gates pass should the candidate become authoritative live state or remote replay/sync capability be enabled. Publication of local readable data and authorization of remote replay can be separate decisions.

**Guard:** `local recovery accepted ≠ remote replay authorized`.

---

## 7. Quarantine is a first-class recovery state

A mixed candidate does not have to collapse into either `accept everything` or `delete everything`.

Quarantine can preserve:
- readable user records;
- original backup artifact;
- pending operations and their identities;
- provenance/diagnostic metadata;
- current known-good live state where present.

while withholding:
- destructive migration/publication;
- remote writes/replay;
- trust-sensitive bridge use;
- automatic key rotation/rewrap that would destroy older recovery paths.

**Guards:**
- `candidate incompatible ≠ candidate worthless`;
- `replay quarantined ≠ records should be erased`;
- `record recovery success ≠ sync recovery success`.

Whether users may edit quarantined/restored records is product/domain policy and remains OPEN.

---

## 8. Compatibility and reconciliation matrix

At minimum, implementation validation should cover these combinations:

| Records | Trust/key/schema | Outbox/ack | Default generic treatment |
|---|---|---|---|
| current/intact | current/compatible | none | candidate for ordinary acceptance |
| intact | trust missing | none | preserve records; rebootstrap trust before sensitive bridges |
| intact | key missing | any | ciphertext/data may be unrecoverable until correct key recovery; do not claim record recovery |
| newer | older trust | pending | mixed epoch; block blind replay; establish current authority |
| older | newer trust | none | data rollback risk; trust freshness does not make records current |
| compatible | current | pending, ack unknown | reconcile/deduplicate before replay |
| compatible | current | stale delete/update conflict | apply domain conflict/delete semantics; do not replay by timestamp alone |
| schema newer than reader | any | any | quarantine until compatible reader/migration path is proven |
| schema label compatible but invariants fail | any | any | reject publication; preserve candidate for recovery/diagnosis |
| all components individually valid but provenance epochs disagree | mixed | mixed | no aggregate PASS; member-level reconciliation required |

No row is a MintTap/LogMate implementation decision; it is a validation taxonomy.

---

## 9. B/C requirements — truthful and accessible recovery states

The UI/state model should not use `Restore complete` when only file import/copy has completed. Distinguishable user-facing concepts may include:

- backup found/imported;
- records verified/readable;
- security state needs re-establishment;
- records preserved but sync paused;
- some pending changes need reconciliation;
- backup incompatible with this app version;
- recovery candidate quarantined; export/support path available;
- synchronization safe to resume.

Design Studio owns final language/interaction. Web Manager supplies the semantic truth conditions.

Current Design Studio Web evidence (2026-09-17): Stage 1 PASS, Stage 2 PASS, Stage 3 PRACTICE / NOT PASSED; W052 dependency reconciliation is ready but execution remains OPEN. Its principle transfers directly: dispatch/batch membership is not dependency satisfaction, just as membership in one backup package is not proof that all members share a coherent recovery epoch.

**TRANSFER VALIDATION:** semantic dependency/reconciliation transfer only; no browser, Safari, AT, physical-device or human UX PASS is inferred.

---

## 10. C validation matrix

High-value executable scenarios for the eventual product stack:

1. valid records + missing trust metadata;
2. valid records + wrong/missing key generation;
3. newer records + older trust generation;
4. old records + new trust generation;
5. compatible schema label + violated domain invariant;
6. newer schema + older reader;
7. outbox captured before remote ack, then restored after ack;
8. duplicate replay with stable operation identity vs without it;
9. restored stale update after newer delete/tombstone;
10. interruption after candidate validation but before publication;
11. interruption during reconciliation before replay enablement;
12. partial backup where manifest exists but one member is missing/corrupt;
13. digest-valid but unauthorized/tampered provenance metadata;
14. storage reset after restore but before trust rebootstrap;
15. old offline client restores old backup then reconnects to server N+k;
16. accessible recovery/quarantine flow at 200% text, keyboard/screen reader and target Safari/Home Screen PWA;
17. exact managed-iPad reset/reinstall/storage-clearing and recovery behavior.

Use explicit independent oracles per gate. A single green `restore()` return value is not a sufficient oracle.

---

## 11. EFB/LogMate-like product relevance

For an EFB-like PWA with potentially irreplaceable locally entered flight records, the safe generic bias is:

`preserve candidate bytes/records → establish integrity/provenance → establish key/schema readability → re-establish current trust/protocol → reconcile outbox/remote acknowledgements → enable replay`.

Do not assume server state always wins. Do not assume local restored state always wins. Authority is component- and domain-specific.

**MINTTAP/LOGMATE DIRECTION:** require a recovery manifest/equivalent and explicit acceptance/reconciliation gates before implementation handoff. Exact schema, key hierarchy, backend conflict policy and storage representation remain Software Engineering/product decisions.

---

## 12. Persistent guards added by 101

- `hash matches ≠ artifact provenance established`;
- `artifact provenance established ≠ application semantics accepted`;
- `ciphertext intact ≠ decryptable ≠ correctly bound to the restored key generation`;
- `restore bytes copied ≠ recovery candidate accepted ≠ live state safely published`;
- `schema version label matches ≠ migration/reader acceptance proven`;
- `outbox item present ≠ never applied remotely ≠ replay authorized`;
- `one backup timestamp ≠ one coherent application epoch`;
- `later timestamp ≠ causally newer state`;
- `manifest present ≠ manifest authentic ≠ components mutually coherent`;
- `local recovery accepted ≠ remote replay authorized`;
- `candidate incompatible ≠ candidate worthless`;
- `replay quarantined ≠ records should be erased`;
- `record recovery success ≠ sync recovery success`.

---

## 13. OPEN / VALIDATION

1. Exact MintTap/LogMate storage/backup format and repository implementation evidence.
2. Exact consistency point across IndexedDB/OPFS/other stores if used.
3. Whether backups include or exclude trust metadata, outbox and key references.
4. Product conflict/delete/recreate policy and remote acknowledgement model.
5. Actual cryptographic authenticity/provenance design, if required.
6. Target Safari/Home Screen/managed-iPad backup, reset and restore behavior.
7. Accessible quarantine/reconciliation UX execution.
8. Cross-version restore matrix across real supported app/schema/protocol generations.
9. Crash/power-loss behavior during publication/reconciliation.
10. Privacy/retention policy for old backup artifacts, tombstones and diagnostic provenance.

Production validation remains OPEN.

---

## 14. Next high-value boundary

101 closes the generic mixed-epoch provenance/reconciliation prerequisite sufficiently for implementation handoff. The next adjacent security/operations question is **recovery artifact confidentiality, portability and custody**: user-controlled Files/cloud export, encryption/key availability, metadata leakage, sharing/import authority, retention/version rotation and how a portable backup avoids becoming a bearer credential or silent trust-policy downgrade. This should be pursued only at generic requirement level until exact product backup architecture exists.
