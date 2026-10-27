# 298 — PWA Durable Local State vs Device Backup / Restore Failure-Domain Contract

Status: **PASS (generic research/model) / PRODUCT + PHYSICAL-IPAD + MANAGED-IPAD + BACKUP-RESTORE VALIDATION OPEN**  
Date: 2026-09-30  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: **A Platform/Browser**, **C Quality/Validation**  
Consumers: **B UX/IA**, **D Analytics/Diagnostics**

## Why this gate exists

The prior recovery-root handoff established that a local store, native peer, server copy, export and device backup cannot be counted as independent recovery roots merely because they have different names. The next high-value question is narrower and operational:

> What can a PWA legitimately claim after local persistence succeeds, and what additional evidence is required before a company iPad backup, restore or reprovision path may be called a recovery path for unique offline work?

This matters for an EFB/LogMate-like PWA because a device may hold unique offline work for a material period. A successful IndexedDB write or persistent-storage grant protects one failure class; it does not prove survival of device loss, explicit deletion, profile removal, reprovision, backup omission, corrupt backup, incompatible restore, or post-restore reconciliation failure.

## SOURCE

### WebKit storage policy

WebKit documents that Safari 17 / iOS 17 / iPadOS 17 support the Storage API, including `estimate()`, `persist()` and `persisted()`. Best-effort origins may be evicted under overall quota/storage pressure; an origin in persistent mode is excluded from that automatic eviction class. Standalone Home Screen web apps receive the same origin and overall quota class as browser apps.

Source: https://webkit.org/blog/14403/updates-to-storage-policy/

### Web Storage API semantics

`navigator.storage.persist()` is a request. A true result means persistent storage was granted for that origin; `persisted()` reports that state. This is browser-storage persistence evidence, not a device-backup manifest or restore proof.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persisted
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria

### Apple managed-device backup/restore

Apple Platform Deployment documents iPhone/iPad backup and restore as a deployment workflow. Device backups can contain Home Screen layout, app data, device settings and other classes of data, while backup method, encryption, enrollment and restrictions affect what is retained. Apple separately documents that managed-app data inclusion can be controlled. This documentation does **not** establish that an installed PWA's IndexedDB/Cache Storage/Service Worker state or a managed Web Clip's website data is included and restored as a usable application recovery root.

Source: https://support.apple.com/guide/deployment/depd44f04xc5/web

### Apple Web Clip management

Apple documents `com.apple.webClip.managed` as a Home Screen Web Clip payload and permits full-screen launch. The payload controls presentation/provisioning properties; the documentation does not establish PWA website-data backup semantics.

Source: https://support.apple.com/ko-kr/guide/deployment/depbc7c7808/web

### Safari iCloud synchronization

Apple's documented Safari iCloud synchronization set includes bookmarks, Reading List, history, open tabs and tab groups. It does not document IndexedDB, Cache Storage, Service Worker registrations or PWA outbox state as Safari-iCloud synchronized data.

Source: https://support.apple.com/guide/icloud/mm9b8da4f328/icloud

## SYNTHESIS

### 1. Persistence, backup and recovery are different claims

Use this consequence ladder:

`local commit`
→ `restart-surviving local state`
→ `persistent-storage mode`
→ `independent backup copy exists`
→ `backup contains required unique state`
→ `restore reconstructs required state`
→ `restored state is schema/runtime compatible`
→ `reconciliation preserves provenance and pending operations`
→ `remote acknowledgement/convergence proven`.

No lower step promotes a higher step.

### 2. Persistent storage narrows eviction risk; it does not create a second failure domain

A persistent origin remains on the same device and within the same browser/OS storage lineage. It is useful protection against user-agent eviction, but it is not an independent copy against:
- device loss or hardware failure;
- explicit website-data deletion;
- destructive reset/reprovision;
- origin or installation-context loss;
- corruption;
- incompatible schema migration;
- account/authority loss;
- backup omission or restore failure.

Therefore:

`persisted() === true ≠ backup exists`.

### 3. Device backup documentation cannot be promoted into PWA backup assurance

Apple's managed-device backup documentation is broad. It describes device/app-data classes and management restrictions, but does not provide a contract that a particular Home Screen PWA or managed Web Clip's IndexedDB, Cache Storage, Service Worker registrations, local credentials and outbox will be included and restored with the semantics the product requires.

The correct evidence state is **OPEN** until a representative backup→destruction/replacement→restore experiment demonstrates the exact required state.

### 4. Icon/profile restoration is not data restoration

Home Screen layout or Web Clip reprovisioning may recreate an entry point without restoring origin data. Conversely, origin data might survive a lifecycle event while the launch surface changes. Treat:
- provisioning state;
- installation/launch identity;
- origin storage;
- Service Worker/control state;
- credentials;
- unique records;
- outbox/provenance

as separate evidence dimensions.

### 5. Backup presence is not restore competence

A byte-present backup is not enough. Recovery requires a supported restore path plus semantic checks:
- record counts and stable identities;
- tombstones/deletions;
- operation IDs/outbox disposition;
- schema/version;
- provenance;
- credential disposition;
- remote acknowledgement horizon;
- conflicts and convergence.

A backup that restores only a projection while omitting pending unique operations is not a complete recovery root for those operations.

## MINTTAP DECISION

For an EFB/LogMate-like PWA:

1. Treat persistent browser storage as **local durability control**, not backup.
2. Do not label device/iCloud/Finder/Configurator backup as a PWA recovery path until exact physical-device restore evidence exists.
3. Do not infer PWA/Web Clip website-data inclusion from Apple's generic “app data” wording.
4. Unique offline work should have an explicitly designed recovery path independent of the primary origin failure being claimed against.
5. Product states such as **Saved**, **Backed up**, **Synced**, **Recovered** and **Remotely confirmed** must map to different evidence.
6. Reprovisioning/reinstall must preserve evidence before destructive repair where unique local work may exist.
7. Recovery acceptance requires post-restore semantic reconciliation, not merely successful launch.

## HARD GUARDS

- `local write succeeded ≠ persistent storage granted`
- `persistent storage granted ≠ independent backup`
- `device backup exists ≠ PWA origin data included`
- `PWA origin data included ≠ complete unique-work recovery`
- `Home Screen icon restored ≠ origin state restored`
- `Web Clip profile restored ≠ PWA data restored`
- `backup bytes present ≠ restore executable`
- `restore executable ≠ schema compatible`
- `records visible ≠ outbox/provenance complete`
- `restore succeeded ≠ current authority restored`
- `Safari iCloud sync enabled ≠ IndexedDB/Cache/outbox synchronized`
- `managed device ≠ managed PWA backup semantics known`

## DEPENDENCY / TRANSFER

### Track A
Owns the browser-side storage facts: origin storage, persistence mode, quota/eviction, Service Worker/control and installation-context mechanics.

### Track C
Owns destructive validation and must prove or falsify recovery claims under representative devices/builds.

### Track B
Consumes the evidence boundary for user-facing states. UX must not collapse local durability, backup and remote confirmation into one reassuring “Saved” state.

### Track D
May measure backup/restore/rejoin outcomes, but telemetry is evidence of observed events, not proof that omitted state did not exist.

### Software Engineering handoff
When implementation topology exists, provide:
- exact durable stores and schema;
- unique-record/operation identity;
- outbox and acknowledgement semantics;
- export/import format if any;
- backup assumptions;
- restore/reconciliation path;
- installation class and MDM path.

Do not infer these from generic PWA architecture.

## VALIDATION — deterministic campaign

Define at least these contradiction cases:

1. `persist()` denied; unique work is captured offline.
2. `persisted()===true`; explicit website-data deletion occurs.
3. Persistent origin survives pressure but device is lost.
4. Device backup exists but PWA origin state is absent after restore.
5. Records restore but outbox does not.
6. Outbox restores but stable operation IDs change.
7. Records/outbox restore but tombstones do not.
8. Restore recreates shell/icon only.
9. Managed Web Clip profile is restored but website data is not.
10. Website data restores but Service Worker registration/controller does not.
11. Data restores under a newer worker/schema.
12. Older backup restores into a newer server/API policy.
13. Backup contains stale credential/session material.
14. Restore succeeds locally but predecessor credential can still mutate remotely.
15. ACK was lost before backup; restored queue retries the already-committed operation.
16. Export exists but import rejects the schema.
17. Export imports but provenance is incomplete.
18. Safari iCloud synchronization is enabled; unique IndexedDB work is not present on another device.
19. MDM restriction disables iCloud backup.
20. Finder/Configurator backup is unencrypted and required secret-bearing state is intentionally absent.
21. Reprovision restores launch surface but not unique work.
22. Restore appears successful in telemetry while consequence reconciliation fails.
23. Unmanaged physical-device restore passes; managed-device restore differs.
24. One iPad/build passes; another OS/build cannot be promoted without evidence.

All are **DEFINED / NOT EXECUTED**.

## Validation ladder

- **V0 — model/static:** storage/backup/recovery topology and required state inventory.
- **V1 — deterministic fixture:** local DB/outbox/schema/ACK-loss/export/import destruction and restore.
- **V2 — exact browser/OS/build:** named Safari/WebKit/iPadOS and installation class.
- **V3 — physical unmanaged iPad:** real backup/destruction/restore plus semantic reconciliation.
- **V4 — representative managed company iPad/EFB:** actual enrollment, restrictions, backup method, reprovision and network/trust envelope.
- **V5 — representative PWA↔native↔server topology:** full recovery, acknowledgement, convergence, credential retirement and rollback boundaries.

PASS is non-transitive.

## CHANGE WATCH

- Safari/WebKit storage quota/persistence/eviction behavior.
- iOS/iPadOS Home Screen web-app and Web Clip storage context.
- Apple Platform Deployment backup/restore restrictions and managed-account behavior.
- MDM-vendor implementation of Web Clip and backup/reprovision workflows.

## OPEN

- Whether the actual company-iPad path is user-installed Home Screen PWA, managed Web Clip, or another deployment class.
- Exact target iPad/iPadOS/WebKit/MDM build and restrictions.
- Whether the target backup method includes the PWA's required origin data.
- Exact LogMate-like durable store, outbox, schema, auth and acknowledgement semantics.
- Whether an independent native/server/export recovery root exists and is complete/current.
- Actual physical-device restore evidence.

## Gate result

**PASS at generic Stage-8/PWA judgment level.** The Web Manager can now distinguish local persistence from device backup and executable recovery, and can specify the evidence needed to promote an EFB backup/reprovision claim. Product and production validation remain OPEN.


---

## 2026-10-27 applied Stage 8 continuation — LogMate LBK temporal completeness, external-file custody and recovery freshness

**Scope and gate:** SOURCE + SYNTHESIS + bounded 18-condition source-structure audit; **no Dart, exact NORMAL PWA, actual file export, Chrome/Safari, physical/managed iPad, or restore execution**. This is a substantive application of 298's independent-backup failure-domain contract, **not** a second generic IndexedDB/backup primer. Track **E** owns backup-currentness/authority/recovery; **A** supplies transaction/browser/file mechanics; **C** challenges with independent execution; **B** consumes truthful recovery task states; **D** consumes privacy-safe evidence/claims. The Web Manager coordinates.

### SOURCE — pinned product and primary platform evidence

- Read-only LogMate current \`main@7caaee998251602e72159eeebda61f701bdea270\` (2026-10-27). \`lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb\`, lines 419–480, 486–592 and 5806–5932; \`lib/repository/logbook/whole_ledger_backup.dart@711f784534bc686a4d8edd6617ac4d1ac362e0a7\`.
- \`exportWholeLedgerBackup\` executes the 37-store registry enumeration in one \`_database.transaction\`, gated on READY capability, matching unlocked owner UID, and absence of pending deletion. It builds an unsigned manifest containing \`formatId\`, \`backupFormatVersion\`, \`sourceCapability\`, \`ownerUid\`, \`sourceReplicaId\`, \`storeRegistry\` entries with counts, then adds \`snapshotDigest\` (SHA-256 of canonical unsigned container). **There is no explicit global snapshot-creation time, source-wide generation/head or external-file completion witness in that manifest.** Row-local revision/time fields may exist and must not be conflated with a global export cut.
- \`WholeLedgerBackup.encode\` canonically sorts map keys before JSON serialization. \`_validateLbkContainer\` checks format/version, expected capability, matching owner UID, replica format, digest, store names/counts, row shape and duplicate keys. These establish **container structural integrity and matching claimed owner** under the supplied verification input; the digest is not an author signature, trusted time source, or freshness proof. The export code explicitly describes the checksum as integrity-only.
- Restore requires a fresh staging database, preserves a destination-generated replica ID, locks the restored owner, moves source cursor/applied-identity evidence to recovery holds, and marks destination Sync \`unbound\` / remote baseline \`unverified\`. This is an important positive safeguard against treating a restored source Sync cursor as destination acknowledgement. Existing 519 §21 separately owns the direct 12-record-store empty-stage versus seven Sync-store admission question; do **not** count that question as solved here.
- IndexedDB 3.0 transaction isolation: https://www.w3.org/TR/IndexedDB/ (read-only transaction results remain constant while live; overlapping read/write transactions are serialized by scope). **Transfer limit:** these browser semantics support a coherent read-cut expectation, but do not themselves prove exact \`sembast_web 2.4.6\` transaction scope/retry behavior, successful external file save, or whether a later edit was included.
- WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/ (origin storage may be evicted under pressure; Home Screen presentation does not make it an independent backup).
- MDN \`showSaveFilePicker\`: https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker (limited availability, secure-context and user-activation requirements); Apple iPad Safari Files flow: https://support.apple.com/en-sg/guide/ipad/ipade2917f90/ipados (explicit Save to Files example). Neither proves LogMate's exact PWA export route, its OS share/download result or a managed EFB's file permissions.
- Peer boundary: Marketing Manager \`STATUS.md\` D8 independently identified missing global snapshot cut/freshness witness and external file custody OPEN. Design Studio \`progress/WEB_STATUS.md\` W121 and \`progress/CONTENT_STATUS.md\` CD127 require exact runtime/action/accessible-state evidence; Software Engineering Studio \`methods/VALIDATION_STANDARD.md\` defines independent oracle and nontransitive evidence tiers. Reuse these, do not duplicate their disciplines.

### HISTORY → PRINCIPLE → FAILURE MODES → OPERATIONAL JUDGMENT

A local database transaction answers **what set of rows was read at one database cut**, not **whether the exported file is the latest recoverable version of a user's work**. The durable chain is:

\`local edit committed → export transaction cut selected → canonical container serialized → browser presents export → bytes saved outside origin → independent reopen/hash/readback → source-vs-export semantic comparison → clean restore → post-restore reconciliation\`.

Each arrow can fail independently. In particular:

1. **Consistent but stale:** export completes at cut C0, edit E1 commits at C1, old file is saved at C2. The file can pass every digest/store-count check and still omit E1. This is **expected historical snapshot behavior**, not proof of a broken database transaction.
2. **Unknown cut ordering:** export overlaps a second-tab write. A successful read transaction should produce a coherent cut under its actual scope, but its order relative to that write and Sembast's callback retry behavior need exact two-tab execution. Do not assert mixed-store corruption or that every concurrent edit is necessarily included.
3. **Exported text is not an external backup:** returning a String is not an OS file write. A download prompt, share sheet, MDM block, user cancellation, browser crash or Files-provider failure can leave no independently accessible file. A UI "Backup created" label must not be inferred from \`exportWholeLedgerBackup\` completion.
4. **External file exists but is unusable:** file may be truncated, inaccessible after device loss, copied to an untrusted account, or rejected on restore because of schema/owner/capability. Independent file readback and a disposable clean restore are different oracles.
5. **Integrity is not provenance:** an attacker who can rewrite the container can recalculate its unkeyed digest; a correct digest does not establish trusted origin, timestamp, device custody, confidentiality or current authority. No claim of actual tampering is made.
6. **Local freshness is not global convergence:** even a locally latest export cannot prove another native device's later edits, remote ACK or merged head. A source-wide generation/cut marker could improve local comparison only if bound to the relevant transactional write paths and independently rechecked; an ordinary device-clock timestamp alone cannot prove freshness or causality.
7. **Restore is not remote authorization:** the current \`unbound/unverified\` Sync reset is correctly conservative. Preserved source receipts/heads/bindings remain historical evidence, not new destination ACK; reconciliation and predecessor-negative tests are separate.
8. **Owner identity and portability tension:** a matching \`ownerUid\` guard prevents casual A→B import but cannot by itself solve lost-account recovery, legitimate account succession, compromised credentials, or data-minimization policy. Any alternative must have an independently authorized recovery procedure, not bypass owner checks.
9. **Installed-context isolation:** Safari tab, Home Screen PWA and managed Web Clip can have distinct local state; an exported file from one context is not automatically a backup of another context's latest edits.
10. **Loss of the only recovery root:** a file stored solely on the same managed iPad may not survive device destruction/reprovision. A second location must be verified independently, including organizational policy and actual retrieval.

**MINTTAP DECISION (research admission, not product-code authorization):** Represent at least four separate statuses: \`local save committed\`, \`snapshot captured (cut/freshness not yet verified)\`, \`external backup independently verified\`, \`restore and currentness reconciled\`. Treat remote sync as a fifth independent status. Never promise "all records backed up" or "latest data safe" based solely on an in-memory digest, downloaded filename or historical snapshot. Define a source-currentness witness and acceptance criteria **before** choosing a new LBK schema or UX implementation; do not silently add manifest keys to the existing v2 format without compatibility tests.

### VALIDATION — high-information-gain executable acceptance bundle, **all NOT RUN**

Reuse LogMate W-012/W-013/W-014/W-030/W-031/W-036, Web Manager 298/319/519 §21/520 and Engineering's existing validation contract. Use disposable A/B owners and flight fixtures only; preserve exact artifact, browser/OS/MDM, transaction cut, file bytes/hash, source and restored 37-store readbacks, and independent expected revision/outbox set.

| ID | Fault / comparison | Independent decisive oracle |
| --- | --- | --- |
| BF01 | Export at C0, save to Files, edit E1 at C1, restore old file | Restore contains C0, not E1; stale snapshot is honestly identified, not falsely declared latest. |
| BF02 | Edit before export transaction starts, then export | Committed edit included under exact transaction semantics; no missing committed revision. |
| BF03 | Two-tab writer races with export transaction; repeat ordering | Single coherent 37-store cut, with observed retry/order; no assumed universal ordering. |
| BF04 | Export text succeeds, user cancels file/save/share flow | No external-backup VERIFIED status and no destructive cleanup. |
| BF05 | Managed iPad disallows destination/Files provider; offline | Explicit actionable failure, source ledger intact; no implied device-backup root. |
| BF06 | External file saved, device rebooted, reopen file independently | Exact bytes and digest/owner/schema readback; verify access after restart. |
| BF07 | Truncated/altered/cross-owner/unsupported-version LBK | Reject without mutating existing destination; no untrusted fallback. |
| BF08 | Legitimate old v1 and v2 fixture restores into fresh staging | Version-specific registry, owner lock and unverified Sync semantics; no fabricated ACK. |
| BF09 | Backup from Safari vs Home Screen vs MDM Web Clip | Per-container provenance and latest-record comparison; do not assume shared origin storage. |
| BF10 | Delete/reinstall/profile removal/reprovision after export | Recovery only from independently retained external copy; no reliance on evicted IndexedDB. |
| BF11 | Source Sync receipt/cursor in backup, destination freshly restored | Historical source evidence preserved as hold; destination cannot claim remote ACK. |
| BF12 | Post-export edits on native mobile or server, then restore PWA | Local backup may be valid but global latest/merge remains UNKNOWN until reconciliation. |
| BF13 | Same file/digest, fabricated "created" time or replayed old file | Time label/digest cannot authorize currentness; trusted source head or explicit uncertainty. |
| BF14 | Two independent backup locations; one unavailable/corrupt | Demonstrate recoverability from remaining verified copy, not mere file count. |
| BF15 | Simulated quota/storage eviction during export/restart | Preserve unique source data if present, never assume backup completed from export callback. |
| BF16 | VoiceOver/keyboard/large text and interrupted file workflow | User can distinguish local save, pending export, verified backup, stale backup and restore; no unsupported copy. |

**Evidence tiers:** source/static predicates ≠ Dart transaction ≠ browser file flow ≠ physical iPad ≠ managed EFB ≠ native/PWA/server convergence. Exact artifact and independent negative/positive oracles required; do not manufacture PASS counts for specified tests.

### Bounded source audit [VALIDATION / CONTRADICTION]

A 2026-10-27 direct-source structural check of the pinned adapter and LBK encoder confirmed **18/18 substantive predicates** for single transaction, READY/unlocked-owner/deletion gates, 37-store registry enumeration, row counts, source replica, canonical digest, absent explicit global timestamp/head in export, format/owner/digest/count checks, absence of external-current-head validation, canonical encoding, and conservative restored Sync reset. This is **lexical/source evidence**, not a compiled or executed Dart assertion. The absence of a manifest field does **not** prove the absence of all row-level timestamps or an external backup workflow elsewhere in the product.

### Five-track depth comparison / TRANSFER VALIDATION / OPEN

- **E highest bottleneck:** backup currentness, independent file custody, replay/authority containment, owner succession, release HOLD. Strong generic theory and source mapping; actual export/recovery authority OPEN.
- **A major dependency:** IndexedDB transaction scope and WebKit/Safari/Files API differences; spec evidence strong, Sembast callback replay and installed-context execution OPEN.
- **C major dependency:** BF01–BF16, two-tab/browser/physical managed-device readback and accessibility. Static source and mock tests are not runtime proof.
- **B focused consumer:** truthful, actionable recovery state taxonomy, file-picker cancellation and no false "backup complete"; Design Studio W121/CD127 still requires exact UX/AT/human execution.
- **D bounded consumer:** privacy-minimized recovery telemetry and public claim parity; Marketing D8–D10 retains PWA/offline/Sync/backup claim HOLD. No raw UID, flight payload, file path or token in analytics.
- **Software Engineering handoff:** owns implementation choice for transactional source-currentness witness, schema migration, file/save/readback harness, CI negative controls and actual managed iPad test. Web Manager records admission requirements only.

**OPEN:** current file-export UI/path and OS file-provider behavior; actual two-tab Sembast read-cut; user-owned external file existence, independent custody, snapshot age after edits, source-currentness marker, v1/v2 compatibility after any schema change, loss/reprovision recovery, managed MDM policy, 37-store restore execution and native/server reconciliation. **CHANGE WATCH:** IndexedDB/WebKit/Sembast transaction behavior, File System Access support, iPadOS/MDM Files and share paths, LogMate backup schema and source head, public backup claims.

**Stop/adjacent check:** reconciled read-cut, metadata, digest/author authenticity, file save, file re-open, two-tab race, v1/v2 restore, Sync authority, Safari/installed partition, managed EFB, data loss, UX and privacy/claims. The next adjacent high-value question is **exact product file I/O and two-tab/managed-device runtime evidence**; another speculative static scenario has lower value. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**. No product or peer repository writes.
