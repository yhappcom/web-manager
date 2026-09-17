# 103 — PWA Backup Freshness, Completeness, Recoverability Evidence & Privacy-Safe Assurance

Status: **PASS (generic) / PRODUCT RESTORE-DRILL + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 074 durability/sync boundaries; 088 testing/diagnostics; 100 trusted-state reset; 101 mixed-epoch recovery; 102 portable artifact custody/import; Track A storage/file mechanics; Track C validation; Software Engineering D003/D005/D006/Q003/Q005/F006.

## Purpose

102 established that a portable backup is a new trust boundary. This study asks the next operational question: what evidence is required before a product may truthfully claim that user data is backed up and recoverable?

The objective is not to prescribe a LogMate/MintTap backup implementation. It establishes an assurance model that separates capture freshness, completeness, durable custody, integrity, decryptability, reader/schema compatibility, semantic recovery, reconciliation and restore rehearsal — while preventing backup telemetry from becoming a new privacy/secrets channel.

---

## 1. Track allocation

- **A Platform/Browser — dependency supplier.** Supplies local storage/file/share mechanics and target-browser evidence; browser API success is not backup assurance.
- **B UX/IA/Content — consumer.** Owns truthful distinctions among saved locally, backup attempted, externally saved, verified, stale, restore-tested and recovery-ready.
- **C Performance/Accessibility/Quality — major validation consumer.** Owns interruption/fault/cross-version/large-state/accessibility/physical-device restore matrices and reproducible evidence packages.
- **D Search/Discovery/Analytics — privacy boundary.** Recovery telemetry must be operationally useful without collecting records, filenames, secrets or unnecessary stable identity.
- **E Architecture/Security/Operations — highest-risk owner.** Owns assurance semantics, evidence lifecycle, restore exercises, retention/monitoring and incident implications.

**Allocation:** E remains the highest-value bottleneck. C receives substantial transfer because assurance without restore/failure evidence is incomplete. Do not duplicate Software Engineering database/retry implementation work.

---

## 2. SOURCE — a backup strategy includes testing and recovery exercises

NIST SP 1339, *OT Backup Quick Start Guide* (June 2026), states that effective backup management includes integrating backups with change/risk management, creating them regularly, testing them and reviewing them during recovery exercises. It calls for backup frequency/location based on information change rate and risk, integrity/availability mechanisms, redundant storage and protection against unauthorized modification/destruction.

Source: https://doi.org/10.6028/NIST.SP.1339

NIST SP 800-53 Rev. 5 CP-9 distinguishes testing backup reliability/integrity from testing restoration of selected system functions. It notes that reliably retrieving/decrypting backup information can test one assurance property, while restoring functions from sampled backup information tests whether the recovered system operates as intended.

Source: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

CISA's #StopRansomware Guide likewise recommends offline encrypted backups and regular testing of backup availability/integrity in a disaster-recovery scenario.

Source: https://www.cisa.gov/stopransomware/ransomware-guide

**SYNTHESIS:** a file's existence or successful write is not evidence that the user's latest authoritative state can be restored into a functioning supported application.

**Guards:**
- `backup file exists ≠ backup current ≠ backup complete ≠ restore works`;
- `backup integrity verified ≠ semantic recovery verified`;
- `decrypt/read succeeded ≠ supported application state restored`;
- `backup job reported success ≠ recovery objective proven`.

---

## 3. Backup assurance is a chain, not one boolean

For an offline-first PWA, useful assurance should distinguish at least:

1. **capture eligibility** — what authoritative state was intended to be protected;
2. **capture point** — the local record/outbox/trust/schema/key/protocol frontier represented by the candidate;
3. **serialization completion** — candidate construction completed under a bounded format contract;
4. **destination handoff** — bytes were handed to the selected external destination mechanism;
5. **durable-custody evidence** — the product has evidence appropriate to that destination that the artifact remains available; this may be impossible to prove after a generic share-sheet handoff;
6. **integrity/authenticity evidence** — the artifact has not been silently corrupted/substituted under the chosen model;
7. **key availability** — required recovery authority can still be obtained without treating the artifact as an unsafe bearer credential;
8. **reader/schema support** — a supported build can parse and validate it;
9. **semantic restore** — expected authoritative records/state survive candidate validation/publication;
10. **reconciliation readiness** — restored outbox/ack/trust/protocol state can be safely reconciled before remote replay;
11. **restore rehearsal recency** — the recovery path has actually been exercised under a defined supported environment recently enough for the product's risk tolerance.

A product may have evidence for some links and not others. Do not collapse them into `backup=true`.

**Guard:** `one green backup indicator ≠ end-to-end recoverability evidence`.

---

## 4. Freshness is measured against authoritative change, not wall-clock age alone

A backup created five minutes ago can already be stale if authoritative local records/outbox changed after its capture point. A backup created yesterday can still represent the latest state if nothing authoritative changed.

Useful freshness evidence therefore needs a product-defined monotonic/logical frontier, for example an application-controlled committed-state generation/checkpoint or equivalent stable identity. Exact representation belongs to Software Engineering.

The frontier must not be inferred from:
- UI render time;
- file modification time alone;
- `Date.now()` alone;
- last sync time;
- analytics event arrival;
- background task invocation;
- "backup started" timestamp.

For offline-first data, remote acknowledgement and backup freshness are orthogonal. Unsynced local records may be the most important state to protect.

**Guards:**
- `recent timestamp ≠ latest authoritative state captured`;
- `last sync current ≠ local backup current`;
- `remote state current ≠ unsynced local state protected`;
- `backup started after edit ≠ edit durably included`.

**MINTTAP/LOGMATE DIRECTION:** define freshness relative to a stable committed local frontier, not merely elapsed time. Exact generation/checkpoint design remains implementation-owned.

---

## 5. Completeness is set membership plus dependency closure

A candidate can be fresh for one table/object and incomplete for the recovery contract as a whole. Completeness must be defined against explicit required classes, not "database copied".

Potential classes include:
- authoritative user records;
- tombstones/conflict metadata required for safe interpretation;
- pending outbox logical operations;
- schema/format metadata;
- cryptographic wrapping/recovery metadata where justified;
- trust/protocol metadata required for local interpretation, without allowing old backup state to override current authority;
- user settings that materially affect record interpretation;
- attachments/files referenced by records, if part of the product's recovery promise.

A manifest/count can support diagnostics but is not itself proof that the underlying domain invariants hold.

**Guards:**
- `latest record present ≠ recovery set complete`;
- `all files copied ≠ dependency closure proven`;
- `record count matches ≠ semantic completeness proven`;
- `backup package complete locally ≠ destination received every required byte`.

This consumes 101's mixed-epoch rule: component completeness must also be checked for coherent/acceptable epochs.

---

## 6. Destination handoff is not durable custody

A browser/PWA can often know that it generated bytes or invoked a file/share flow. It may not be able to prove that a user-selected cloud provider, Files destination, email recipient or other share target durably retained the artifact after control leaves the application.

Therefore evidence vocabulary should distinguish:
- `GENERATED`;
- `HANDOFF_COMPLETED` where the platform can establish it;
- `APP-VERIFIED_DURABLE` only where the product can actually re-open/re-read or otherwise verify under the destination contract;
- `USER-MANAGED_EXTERNAL` where continued custody is outside application observability.

**Guard:** `export/share completion ≠ externally durable custody verified`.

Do not fake certainty in UI/telemetry where the platform does not expose it.

---

## 7. Restore drill is stronger evidence than backup creation

A restore drill should exercise the real recovery path sufficiently to discover missing dependencies and incompatible readers. NIST/CISA guidance supports regular backup testing and recovery exercises; CISA specifically notes that full restore testing can reveal previously unknown dependencies.

For PWA/offline-first products, a high-value drill eventually includes:
1. start from a clean/quarantined candidate environment rather than overwriting the only known-good state;
2. obtain the artifact from the intended custody path;
3. validate integrity/provenance and bounded parsing;
4. obtain the legitimate recovery key/authority;
5. decrypt/read with a currently supported build;
6. validate schema/domain invariants;
7. compare expected recovery frontier/set against recovered state;
8. preserve/inspect pending outbox and acknowledgement ambiguity;
9. perform reconciliation before any remote replay;
10. verify degraded/error UX and accessible recovery paths;
11. preserve reproducible test evidence without retaining sensitive record content.

**Guard:** `restore UI reached ≠ restore drill passed`.

A destructive production restore is not required merely to prove backups; drills can use controlled fixtures/copies. Exact fixture architecture is implementation/quality owned.

---

## 8. Change invalidates old assurance selectively

A previously successful restore drill does not prove every future artifact/build combination. Assurance should be reconsidered when changes affect the recovery chain, including:
- backup format/schema;
- serialization/parser code;
- encryption/wrapping/key recovery;
- storage/destination integration;
- authoritative data model;
- outbox/reconciliation semantics;
- service-worker/application deployment behavior relevant to recovery;
- supported browser/OS versions;
- MDM/file-sharing policy;
- dependency/runtime versions with recovery-path impact.

NIST SP 1339 explicitly links backup strategy with change management.

**SYNTHESIS:** restore evidence has an applicability envelope: build/version + format generation + platform/runtime + recovery-key path + scenario/fixture.

**Guard:** `restore drill passed once ≠ all future builds/artifacts recoverable`.

---

## 9. Privacy-safe backup telemetry

Operational assurance needs observability, but recovery telemetry is itself a trust boundary. OWASP Logging guidance recommends logging relevant import/export/security events while excluding or masking session IDs, access tokens, passwords, encryption keys, sensitive PII and data above the logging system's classification. It also warns that event data from other trust zones can be missing, modified, forged or replayed.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

**Do not send by default:**
- raw flight/investment/user records;
- backup payload bytes;
- recovery passphrases/DEKs/KEKs/wrapped secrets;
- session/refresh/device credentials;
- user-selected filenames/paths;
- imported free-form metadata/memos;
- stable backup IDs that unnecessarily permit cross-device/user tracking;
- raw attachment names/content.

Potentially useful bounded evidence, subject to privacy review:
- application/format/schema version class;
- coarse backup outcome/failure class;
- whether required component classes were included, expressed without content;
- local freshness-lag bucket rather than record content;
- restore-drill outcome for controlled fixtures;
- target platform/browser class when needed for compatibility evidence;
- cryptographic operation outcome class without keys/ciphertext.

**Guards:**
- `more recovery telemetry ≠ more trustworthy recovery`;
- `backup observability ≠ permission to export backup metadata`;
- `client reports backup success ≠ independently trustworthy durable-custody proof`.

Track D consumes these boundaries; it does not turn backup health into acquisition analytics.

---

## 10. Truthful-state model for B/Content Design handoff

Avoid one generic "Backed up" state. Candidate semantics include:

- **Not yet protected externally** — authoritative changes exceed last evidenced capture frontier.
- **Backup being prepared** — serialization is in progress; no custody claim yet.
- **Backup created on this device** — candidate exists locally; external durability not implied.
- **Saved to external destination** — only when destination handoff is known; continued custody may still be user-managed.
- **Backup verification passed** — specify whether this means integrity/readability, not full semantic restore.
- **Restore tested** — only when a defined restore drill passed for a stated support envelope.
- **Backup may be stale** — authoritative local frontier advanced after the last evidenced capture.
- **Recovery compatibility unknown** — artifact exists but current reader/key/platform path has not been verified.

Final language/interaction belongs to Content/Design Studio. Web Manager owns the truth conditions.

---

## 11. C validation matrix

Minimum future implementation evidence should include:

1. edit committed immediately before backup capture;
2. edit committed during backup construction;
3. outbox pending but remote offline;
4. local record committed but backup process interrupted;
5. destination handoff cancelled/fails after serialization;
6. artifact bit corruption;
7. missing component/attachment;
8. wrong/missing recovery key;
9. older supported backup → current supported reader;
10. current backup → oldest supported recovery reader, if promised;
11. schema migration failure after successful decrypt;
12. restore candidate semantic rejection with known-good live state preserved;
13. restored outbox contains operation already applied remotely but acknowledgement lost;
14. restore/replay while protocol/trust generation has advanced;
15. storage pressure/reset/reinstall before next backup;
16. device clock wrong while freshness evidence remains logically correct;
17. managed-iPad Files/iCloud/share restriction;
18. 200% text/zoom, keyboard/focus and screen-reader recovery flow;
19. power/process termination at serialization, write, verify and publication boundaries;
20. telemetry inspection proving no record/key/token/filename leakage.

Where exact interleavings matter, consume Software Engineering Q003/D006/F006 methodology rather than inventing web-specific concurrency theory.

---

## 12. E operational evidence record

A future production backup-health record should be designed around evidence, not user-content replication. Conceptually it may need to answer:
- what supported app/format/platform produced the evidence;
- what authoritative local frontier was intended/captured;
- which required component classes passed inclusion validation;
- whether integrity/authenticity verification passed;
- what custody claim is actually supportable;
- whether key/read/schema/domain recovery paths were last tested and under what envelope;
- whether authoritative state has advanced since the last evidenced backup;
- whether a change invalidated the previous restore-test envelope.

This is a requirements model, not a telemetry schema. Privacy/legal review and implementation evidence are required before product collection.

---

## 13. Failure diagnosis

When a user says "my backup didn't work", do not collapse all causes into file failure. Diagnose the first broken assurance link:

`capture → serialize → handoff/custody → integrity/authenticity → key → reader/schema → domain → publish → reconcile → replay`

Examples:
- artifact exists, wrong key → recoverability/key-custody failure;
- decrypts, parser rejects → reader/schema failure;
- parses, missing attachment/outbox dependency → completeness failure;
- local restore succeeds, sync rejected → trust/protocol/reconciliation failure;
- backup generated, external copy unavailable → custody failure;
- all recovery succeeds but telemetry says failure → observability/evidence failure.

This consumes Software Engineering Q005 symptom→isolation→causal-test method without claiming its fixtures are PWA runtime evidence.

---

## 14. MINTTAP / LogMate bounded direction

For an EFB/offline-first LogMate-like product, the critical recovery promise should eventually be framed around **latest committed authoritative local data**, including unsynced state where the product contract requires it. Server sync cannot substitute for local backup when the device may remain offline.

Do not claim automatic safe backup merely because:
- IndexedDB write succeeded;
- `navigator.storage.persist()` was granted;
- a backup file was generated;
- Files/share UI returned successfully;
- cloud sync exists generically;
- an old restore test passed;
- the server has a recent state.

Exact automatic-backup feasibility on company-managed iPad remains OPEN because file destination access, background execution, MDM policy and external-custody verification require exact target-device evidence.

MintTap-specific production backup requirements remain OPEN until its actual authoritative local/server data model and recovery contract are inspected.

---

## 15. CHANGE WATCH

Recheck when materially relevant:
- Safari/iPadOS Home Screen file/share/storage behavior;
- managed-device Files/iCloud restrictions;
- File System / Web Share capability changes;
- supported backup reader/version policy;
- WebCrypto/recovery-key implementation changes;
- privacy/telemetry policy or legal requirements;
- product data-authority/sync architecture changes.

---

## 16. Gate result

**PASS (generic).** The Web Manager can now distinguish backup creation from freshness, completeness, custody, integrity, decryptability, reader/schema compatibility, semantic restore, reconciliation and tested recoverability; can define a restore-assurance chain; can identify when change invalidates old evidence; and can specify privacy-safe observability boundaries.

**OPEN:** product backup contract; exact frontier/checkpoint implementation; backup format/key hierarchy; automatic backup feasibility; external durable-custody verification; supported reader/migration window; actual restore drills; managed-iPad/MDM/Files/iCloud behavior; accessibility/physical-device evidence; production telemetry/privacy review.

## Next high-value boundary

With generic backup assurance now established, the next useful security/operations question is **recovery objectives and failure budgets for offline-first PWA data**: how RPO-like local-data exposure, backup lag, restore-test recency, recovery time, sync backlog and long-offline operation should be expressed without importing server-centric disaster-recovery metrics blindly. This should connect user-visible guarantees, operational alerting and target-device constraints while leaving exact SLO numbers product-evidence-driven.