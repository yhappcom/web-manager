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


---

## 2026-10-27 Stage 8 continuation — LBK plaintext custody, share-target authority and managed-iPad data egress

**Gate:** SOURCE / SYNTHESIS / CONTRADICTION / actionable VALIDATION design. **No actual browser export, OS share sheet, iPad MDM, cryptographic implementation, live file or data exposure was tested.** This extends the existing 298 snapshot/freshness study at a **different trust boundary**: an externally portable, valid recovery file can be simultaneously useful for durability and unsafe for confidentiality. Track E owns the web-specific trust and custody contract; Track A supplies API semantics; C owns runtime/independent oracles; B/D consume the result. No product/peer writes.

### 1. History, threat and exact source [SOURCE]

- **Pinned LogMate main:** \`7caaee998251602e72159eeebda61f701bdea270\` (latest reviewed in this integrated 298 continuation); exact blobs \`lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb\`, lines 419–592, and \`lib/repository/logbook/whole_ledger_backup.dart@711f784534bc686a4d8edd6617ac4d1ac362e0a7\`. The exporter returns a **JSON string** containing the complete v2 **37-store** registry, \`ownerUid\`, \`sourceReplicaId\`, registry names/counts and a SHA-256 \`snapshotDigest\`. Store rows are copied as \`key\`/\`value\` objects; \`WholeLedgerBackup.encode()\` canonicalizes map order and calls \`jsonEncode\`. No encryption or keyed authentication step is present in these inspected exporter/codec methods. The source itself calls the checksum integrity-only. **This is a plaintext-container property of the inspected method, not proof that a caller never encrypts the returned text before writing it.** The exact current caller/file I/O route remains OPEN.
- \`lib/repository/logbook/sync_persistence.dart@fed4f6600f1c0581ddb85c8d1c0730f94f1e0363\` encodes eligible Sync operation maps with \`ownerUid\`, \`recordId\`, \`revisionId\`, \`canonicalPayload\`, \`payloadDigest\` and binding status. Since v2 exports the Sync stores as part of the registry, **populated source fixtures may contain identifiable record/Sync content in the LBK**, subject to actual stored rows. Do not claim all stores are always populated or that an actual user's data has escaped.
- **Platform references, reviewed 2026-10-27:** MDN Web Share API https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API ; \`navigator.share()\` https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share ; \`canShare()\` https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare ; \`showSaveFilePicker()\` https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker . File sharing and picker support vary, require secure contexts/user activation where specified, and can fail, be cancelled or hand data to an OS-selected target. **Share promise resolution is not an independent durable readback or an assurance that the user chose an approved storage location.**
- **Apple management primary sources:** https://support.apple.com/en-gb/guide/deployment/depaa73a4973/web (Managed Open In / managed data flow restrictions) and https://support.apple.com/en-gb/guide/deployment/depbc7c7808/web (managed Web Clip payload/FullScreen). Managed Open In can restrict managed→unmanaged document flows; **a Web Clip payload being installed by MDM does not, without an actual management-policy/runtime check, prove that its generated/downloaded file is classified and protected like a managed native-app document**. Actual enrollment, management domain, Safari/Web Clip mode, Files provider, share destinations and policies are unknown.
- **Security guidance:** OWASP MASVS storage https://mas.owasp.org/MASVS/controls/MASVS-STORAGE-1/ and leakage https://mas.owasp.org/MASVS/controls/MASVS-STORAGE-2/ ; backup exposure weakness https://mas.owasp.org/MASWE-0006/ . These are general risk-control references, not proof of a specific LogMate incident or a legal compliance conclusion.
- **Peer transfer:** Design Studio \`progress/WEB_STATUS.md\` W121 and \`progress/CONTENT_STATUS.md\` CD127 require exact action/state/accessibility runtime before promotion; Marketing Manager D8–D10 retain public PWA/backup/Sync claim HOLD; Software Engineering Studio \`methods/VALIDATION_STANDARD.md\` requires an independent oracle and exact target/environment. Reuse rather than duplicate their disciplines.

### 2. Mechanism and failure-domain separation [SYNTHESIS]

The recovery chain is now two-dimensional, not one “backup successful” Boolean:

1. **Content validity:** parseable 37-store v2 container; declared owner/capability/schema/row counts; digest matches bytes.
2. **Source authority:** actual owner-unlocked export admission; current source cut; no assertion of other-device/server currentness.
3. **Confidentiality at rest:** whether the actual external copy is encrypted and whether keys are recoverable *independently of the lost iPad*.
4. **Destination authorization:** which OS share/save destination receives the file; whether personal/unmanaged destinations are permitted for company EFB data.
5. **External durability:** whether a complete file was actually persisted, re-opened and independently verified outside the origin/device failure domain.
6. **Recovery authority:** whether the importer is entitled to admit the old file to the new owner/device; no implicit Sync/server trust from an old cursor or receipt.
7. **Lifecycle and deletion:** whether stale copies remain in Files, cloud, Downloads, email, shared targets or managed repositories after app-account deletion, and who is responsible for their retention/erasure.

A file can PASS (1) while FAILING (3), (4) or (5). A file can PASS (3) but FAIL (5) because a forgotten key makes it unrecoverable. A file can PASS (1)–(5) but remain stale relative to edits after its source cut (previous 298 BF01/BF12). An external file survives the app origin's storage eviction **only if its custody is actually independent**. The SHA-256 checksum is neither a secret nor a signature; replacing data and recalculating it is not prevented by the codec alone. These distinctions do **not** imply a production exploit.

### 3. Operational alternatives and trade-offs [MINTTAP DIRECTION — NOT PRODUCT APPROVAL]

| Candidate export model | Durability advantage | Confidentiality / operability cost | Release admission |
| --- | --- | --- | --- |
| Plaintext LBK to user-selected file | Simple, portable and inspectable; already source-compatible at codec level | Sensitive contents readable to anyone obtaining file; uncontrolled share destinations and retention | Do not describe as encrypted/private. Require explicit sensitivity notice, destination policy, independent file readback and retention controls before claiming safe EFB backup. |
| Encrypted portable LBK with user-held recovery secret | Limits disclosure after file compromise when cryptography/key handling are sound | Lost secret can destroy recoverability; password-strength, KDF, algorithm agility, versioning and key migration need independent review | Only a design option. Requires Engineering/cryptography review, negative tamper/wrong-key tests, recovery drills and an independently durable key strategy. |
| Organization-managed encrypted backup destination | Potentially centralized policy, retrieval, retention and incident response | MDM/network/offline availability, account lifecycle, provider and organizational custody become failure domains | Only when the actual airline EFB administrator permits and tests the exact source→destination flow; cannot infer from “MDM installed.” |
| Native/server-assisted cross-device backup | May offer a second failure domain and reconciliation | Authentication, remote authorization, transport, receipt and Sync conflicts; cockpit connectivity not assumed | Not equivalent to unattended PWA↔native sync; must prove actual approved transport, custody, owner and restore. |

**Security vs recoverability contradiction:** “encrypt every export” without recoverable keys may improve confidentiality while worsening irreplaceable flight-record loss. “Save to any Files destination” may improve portability while increasing uncontrolled copies. “Delete all backup files on account deletion” may conflict with independently owned lawful/operational retention and may be technically impossible for previously exported files. Resolve these as explicit owner/operator policy choices, not unqualified product defaults. The Web Manager does **not** mandate an encryption algorithm, KDF or key storage implementation.

### 4. Concrete misuse/failure cases and nontransitive oracles [CONTRADICTION / VALIDATION — NOT RUN]

| Case | Stimulus / negative control | Independent evidence needed |
| --- | --- | --- |
| EC01 | Export nonempty v2 fixture; inspect returned LBK before caller I/O | Confirm plaintext JSON shape, presence/absence of known synthetic flight and Sync sentinel; do not log real records. |
| EC02 | Mutate synthetic row and recompute unkeyed digest | Container may pass checksum; distinguish structural integrity from independent author authentication; no claim that this bypasses all restore guards. |
| EC03 | Share/saving UI on Chromium, Safari tab, Home Screen, managed Web Clip | Exact supported API, user gesture, file MIME/name, share targets, OS outcome, actual file existence; no feature assumed across platforms. |
| EC04 | Cancel share sheet / picker or choose unsupported file target | No “backup verified” or destructive source cleanup; distinguish cancellation, API failure and target unavailability. |
| EC05 | Share promise resolves but destination file is absent/inaccessible after restart | UI does not infer durable custody from promise resolution; independent file reopen is required. |
| EC06 | Save to permitted managed destination, then attempt unmanaged/personal target | Actual MDM policy enforcement and data classification measured; do not assume Web Clip == managed native app. |
| EC07 | Files/cloud destination inaccessible offline or after MDM reprovision | Verified recovery from a separate approved location; not merely a filename or local share receipt. |
| EC08 | External file copied outside device, then local ledger deleted/evicted | Independently restore 37 stores from external bytes; owner lock, Sync \`unbound/unverified\`, record semantics and no fabricated remote ACK. |
| EC09 | Wrong owner UID, altered schema, truncated file, unsupported version | Reject before destination mutation; independent clean-staging before/after store diff. |
| EC10 | Old valid file replayed after newer edits on another device | Mark historical/possibly stale; do not auto-overwrite or auto-publish remote authority. |
| EC11 | Optional encrypted export prototype with wrong/missing recovery secret | Wrong key/tamper rejects; lost-key recovery objective and support burden evaluated before adoption. |
| EC12 | Account deletion with prior exported copies in Files/share/cloud | Separate local/remote account deletion from independently exported-file retention; demonstrate only controls actually owned by app/operator. |
| EC13 | Screen reader/VoiceOver, 200% zoom, interrupted export | Announce truthful stages “snapshot prepared”, “file handoff requested”, “external file verified” without false completion; Design Studio owns copy/interaction evidence. |
| EC14 | Synthetic analytics/incident trace | Record status code/OS class/artifact digest only where safe; no UID, record payload, file contents, recovery secret, private file path or share-target identity in telemetry. |
| EC15 | Compare export paths with browser and iPadOS versions | Confirm \`navigator.canShare\`, \`share\`, picker/download fallback and actual behavior separately; update support matrix, do not assume MDN “limited availability” is permanent. |
| EC16 | EFB managed profile update, removal, device replacement | Show independent backup/key custody and full recovery despite lost Web Clip/local origin; record actual management envelope. |

**Evidence contract:** CLAIM → spec/property → exact LogMate ref + NORMAL artifact digest → synthetic prestate/37-store inventory → OS/browser/MDM/share policy → independent expected oracle → observed saved bytes and destination → reopen/restore → verdict PASS/FAIL/UNKNOWN/NOT RUN → limitations. Preserve both **successful** and **blocked** destination controls. A passing native host LBK codec test, V8 model or generic Safari API support does not prove managed Web Clip file export. A successful download is not proof of encryption, authorization, retention or recoverability.

### 5. Five-track allocation, transfer and next decision [DEPENDENCY / TRANSFER VALIDATION / OPEN / CHANGE WATCH]

- **E — primary bottleneck:** source/destination trust boundary, external-file privacy/custody, recovery-key governance, EFB MDM policy, incident/retention and backup release admission. Existing 298 and 319 remain canonical for durability and deletion; this section adds confidentiality/egress without another primer.
- **A — major prerequisite:** web file/share/picker capability and user activation; WebKit/Chromium distinctions, origin storage versus external Files. A supports E's decision rather than owning data policy.
- **C — major execution bottleneck:** EC01–EC16, actual approved NORMAL and representative iPad, accessibility/negative controls and independent restore. **No browser or physical device evidence** yet.
- **B — focused transfer:** use Design Studio W121/CD127 to prevent misleading “encrypted”, “backed up”, “synced” or “saved” labels; verify actual action semantics and accessible state on exact runtime.
- **D — focused transfer:** Marketing D8–D10 backup/offline/managed-iPad claims remain HOLD; only privacy-minimal aggregate failure modes, no record or share-target leakage.
- **Engineering:** owns any implementation, encryption/key design, file I/O harness, test fixtures and release code. Product repos remain read-only.

**OPEN:** actual LogMate LBK UI caller and whether it encrypts the returned string; actual file MIME/download/share path; OS-specific support; real MDM managed/unmanaged classification; EFB data classification/retention policy; independent external backup/key storage; real 37-store file restore; Safari/installed Web Clip/physical managed iPad; consent/telemetry and owner-deletion interaction. **Do not label the whole product's backup “unencrypted” until the caller path is inspected; the inspected B1 codec output is plaintext.**

**CHANGE WATCH:** MDN file/share/picker availability and success semantics, WebKit/iPadOS Home Screen/Web Clip behavior, Apple Managed Open In policy, LogMate export UI/caller, LBK schema, organizational backup and retention requirements.

**Stop/adjacent-value check:** This continuation resolves the **previously under-specified external confidentiality and destination-authorization dimension**, links the actual JSON/Sync fields to Web Share and MDM evidence, evaluates four architecture alternatives and defines falsifiable tests. The next decisive question is the **exact file-export caller and physical managed-iPad destination/readback**; another generic storage or encryption primer would have lower information gain. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


---

## 2026-10-27 Stage 8 continuation — canonical product authority resolves the LBK file-caller question; staged file-security admission

**Evidence gate: canonical product-state reconciliation + platform/crypto SOURCE + integrated operational decision packet; NOT a product test, release, security review, or implementation approval.** This corrects an important uncertainty in the immediately preceding §298 continuation: the product file/export UI is not simply an unidentified existing caller awaiting inspection. The current **canonical product roadmap explicitly classifies the user-facing file workflow as NOT IMPLEMENTED**. The repository codec and an end-user backup are different products. Track E owns release/custody/cryptographic threat boundaries; A owns Web Crypto/browser API prerequisites; C owns execution evidence; B/D consume truthful UX/claim constraints.

### SOURCE — current exact canonical product and peer references

Read on 2026-10-27:
- LogMate **main \`7caaee998251602e72159eeebda61f701bdea270\`**, \`MASTER.md@d665429da245e393a2a52e292b7624de718ab9d5\`, §§0, 13, 20; \`docs/roadmap-reconciliation-2026-10-24.md@741eeb7b0b226ff54e50ab45f5878a54d94d54a1\`, completion matrix **B1 / FILE**; \`docs/stage3-product-integration-acceptance-checklist.md\`, **W-012–W-015**; \`docs/specs/local-first-manual-delta-sync-contract.md@2240fc1b6adf5fcd041a44de0e4660eb1528e92a\`, §§1, 8.
- Canonical roadmap §4 explicitly: **B1 / whole-ledger backup foundation = IMPLEMENTED** repository slice; **FILE / Backup file UX = NOT IMPLEMENTED complete product flow**, with export/pick/share/restore review and failure UX pending. \`MASTER.md\` §13 independently says user Files save/share/restore UI, periodic backup, new-device transfer E2E and physical recovery remain OPEN. The current \`lib/screens/settings_screen.dart@4affdb26f09673cd0d42ff8d13d16f7206e10ee6\` contains Import (empty handler), Previous Total and Sign out; it does not expose an LBK export action. This is **positive canonical status evidence plus one bounded screen observation**, not a repository-wide proof that no experimental/internal call site exists.
- W-012: **READY / NOT STARTED / owner UNASSIGNED**, verify B1 empty-destination same-UID restore and existing evidence, including Sync HOLD and rollback; no file UI or production \`lib/\` changes in that Work. W-013: **CONDITIONAL / NOT STARTED**, depends on W-012, owns file adapters + user-facing export/pick/restore/error/permission UX and requires explicit file UX/permission approval. W-014: **CONDITIONAL / NOT STARTED**, depends on W-013, owns exact Native/EFB PWA file-transfer physical-device acceptance. W-015: **READY / NOT STARTED**, owns *decision materials*, not authorization to decide or implement non-empty merge/replace/reset or automatic backup. All four are user-approval-controlled Work IDs; **READY is not execution approval**.
- \`MASTER.md\` BACKUP-001 (non-empty merge/replace/reset) and BACKUP-002 (automatic backup destination/permission/cadence/recovery) remain **USER DECISION REQUIRED**. Approved Manual Delta Sync contract prioritizes a **full local \`.lbk\` file** for device transfer before later Firebase Delta; it explicitly distinguishes CSV/Excel/PDF from complete backup, forbids silent replacement of unsent work, and requires the product to disclose file sensitivity, permission/protection and encryption choice. It does **not** approve a particular encryption envelope or automatically enabled backup.
- Previous codec-source evidence remains exact: \`sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb\` \`exportWholeLedgerBackup\` returns JSON text and delegates file transport to a caller; \`whole_ledger_backup.dart@711f784534bc686a4d8edd6617ac4d1ac362e0a7\` canonical JSON and SHA-256 are **plaintext/integrity-only at the codec boundary**. A future file adapter may transform the bytes, but the canonical product currently has no completed user file flow to assert either encrypted or plaintext **exported files**.
- Platform crypto: W3C Web Cryptography Level 2 https://www.w3.org/TR/WebCryptoAPI/ ; MDN Web Crypto API https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API ; \`SubtleCrypto.encrypt\` https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/encrypt ; \`deriveKey\` https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/deriveKey (checked 2026-10-27). Web Crypto is a **low-level secure-context primitive**, not a backup product, file permission system, KDF policy, user-secret recovery service, or guarantee that the exact Flutter Web build uses it correctly. MDN recommends authenticated encryption such as AES-GCM and distinguishes PBKDF2 for password input from HKDF for high-entropy input; neither page approves LogMate's actual key-management policy.
- Existing Apple Managed Open In / Web Clip, MDN Web Share/picker, WebKit Home Screen storage and 298 BF/EC evidence remain the platform references. No new OS/MDM capability is inferred from cryptography availability.
- Design Studio \`progress/WEB_STATUS.md@265433cd\` W121 and \`progress/CONTENT_STATUS.md@be7ff67f\` CD127: truthful visible/accessibility state requires exact runtime/action. Marketing Manager \`STATUS.md@962f4730\` D8–D10: production export/re-import, PWA/offline acceptance and ads remain HOLD. Software Engineering Studio \`methods/VALIDATION_STANDARD.md@c8ec2df\`: successful write ≠ durability; crypto present ≠ secure system; independent oracle and negative controls required. Latest Design Studio \`main@9b025f6e\` concerns CrewConnex cross-export evidence and does not promote PWA validation.

### SYNTHESIS / CONTRADICTION — what the new product-authority reading changes

**Prior OPEN:** “Find exact LBK file-export caller; perhaps it encrypts the codec output.”  
**Refined finding:** The authoritative product-state matrix says **user-facing FILE is not implemented**. Do not infer a shipped file export path, working encryption, Files persistence or recoverable backups from the B1 API. A narrow search for a test/internal caller may still be useful for Engineering, but **cannot substitute for W-013 implementation and W-014 acceptance**. Do not spend another research cycle trying to prove a production user workflow by searching for a hypothetical call site.

The four distinct states are:
1. **B1 format/codec ready:** an authenticated, owner-guarded, 37-store local snapshot can be encoded as JSON text and validated/loaded in its supported repository test scope.
2. **User file handoff NOT IMPLEMENTED:** no canonical product acceptance for file selection, OS save/share, error/cancel, readback or restore review.
3. **External backup custody NOT VERIFIED:** no approved independently saved file, encryption/key policy, destination authorization or loss/reprovision recovery evidence.
4. **Sync and currentness NOT VERIFIED:** valid old backup is not remote authority; new device has a fresh replica and Sync \`unbound/unverified\` until separately validated; latest data and pending edits require semantic reconciliation.

This is a **stronger, less speculative release conclusion** than “an unknown UI caller might encrypt the JSON.” It also avoids the opposite error of declaring an actual plaintext file leak or security incident. A repo-code search yielding no matches is **not** evidence of absence; the canonical product-state documents and the bounded Settings implementation supply the classification.

### HISTORY → DESIGN PRINCIPLE → STANDARD → OPERATIONAL JUDGMENT

Why backup cryptography cannot be bolted onto the end of a file picker: the B1 checksum protects **accidental/unauthenticated container alteration detection only under a non-adversarial checksum trust model**. An attacker who can replace the container and recalculate SHA-256 is not excluded by that checksum. Cryptographic authenticated encryption can protect confidentiality and tampering under a well-protected key, but a copied encrypted backup may still be stale, owner-incompatible, unrecoverable after lost key, or in a disallowed Files destination. Encryption also does not establish a current authorized Firebase UID or safe Delta cursor. Treat security as a **composed recovery system**, not a “AES enabled” checkbox.

Candidate future portable-envelope *requirements for owner/Engineering review*, **not a selected format or implementation**:
- Versioned envelope with algorithm/KDF identifiers and parameters, random per-file salt/nonce where applicable, authenticated metadata binding (including format/schema/version/owner context where safe), unambiguous encoding, length bounds and downgrade rejection.
- Threat-model-specific key origin: user-held recovery secret vs independent organization custody vs device-bound key. A key only recoverable from the lost origin/device **defeats independent disaster recovery**. A user-held password introduces guessing/recovery/assistive-UX burdens; an organizational key introduces managed account, incident and offboarding dependencies. Do not invent a numeric KDF work factor or claim Argon2/PBKDF2 choice is approved.
- AEAD authentication failure, wrong secret, truncated file, unsupported format, foreign UID, replayed older valid snapshot and stale current-owner state must be **distinct** observable outcomes. Decrypt and validate in staging before mutating destination; do not log secrets/flight payload.
- Confidentiality and recoverability require opposing tests: stolen file without secret should not expose fixture records; **lost device with only approved independent file + recovery material** should still restore a synthetic full ledger. Both are necessary. Encryption key exportability or Web Crypto availability is not evidence that the actual iPad Web Clip allows a Files destination.
- User-facing state machine must separate \`SNAPSHOT_PREPARED\`, \`FILE_HANDOFF_REQUESTED\`, \`EXTERNAL_FILE_VERIFIED\`, \`RESTORE_VALIDATED\`, \`RECOVERY_COMPLETE\`, and \`UNKNOWN/REVIEW_REQUIRED\`. Do not label share-dialog closure “backup complete”; do not label checksum “encrypted”; do not label local restore “synced”.

### MINTTAP DECISION BOUNDARY — sequencing, ownership and stop conditions

| Owner Work / question | What can be done now | Required promotion evidence | What remains forbidden/OPEN |
| --- | --- | --- | --- |
| **W-012** repository restore | Reuse bounded B1/F1 host fixtures; independent negative controls for same UID, nested Sync/old cursor, staging rollback, owner lock, 37-store semantic readback | Exact source/test runner, populated fixture, negative and positive oracles; record result in original Work | Do not count W-013 file flow, physical EFB or non-empty replacement as passed |
| **W-013** user file UX | Prepare cross-platform capability/permission decision packet and user-action state machine; await explicit Work approval | Implemented actual export/save/pick/cancel/readback + empty-destination restore; exact browser/Native failures | Not authorized merely because W-012 is READY; do not infer encryption/MDM classification |
| **W-014** device transfer | Specify representative managed/unmanaged iPad and native transfer matrix, independent external file and restore oracle | W-013 actual functionality, exact NORMAL archive/HTTPS served bytes, device/MDM evidence, destructive loss/reprovision drill with synthetic data | No cross-device auto-sync, storage persistence, MDM allow, or release PASS from generic Safari docs |
| **W-015 / BACKUP-001/002** policy | Compare no-auto vs automatic backup, managed destination, user-file cadence, non-empty restore and key recovery trade-offs | Explicit owner decision, policy/privacy/MDM review and separate Engineering implementation scope | Do not silently pick merge/replace, cloud full backup, encryption mode, automatic scheduling or remote retention |

**Cross-track pressure:** E remains highest-risk because a bad backup promise can irreversibly lose or disclose records; A must resolve real browser API and storage/crypto capability per target; C must produce independent file+restore evidence; B consumes W121/CD127 to distinguish action/verified outcome; D consumes Marketing D8–D10 and must not advertise “secure encrypted backup”, “offline recovery” or “seamless iPad transfer” before acceptance. Software Engineering owns implementation and test harness, not Web Manager. No peer/product writes.

### VALIDATION — high-information-gain integrated experiment packet (reuse existing BF/EC; NOT RUN)

Rather than inventing another set of 16 micro-test IDs, consolidate the existing BF01–BF16 / EC01–EC16 into **four independent release campaigns**:
1. **Foundation W-012:** synthetic nonempty 37-store source, v1/v2 compatibility, owner mismatch, tampered digest, incomplete nested Sync, duplicate \`restored:\` hold identity, rollback, reopen, fresh destination replica and unverified cursor; independent semantic comparison, not just row count.
2. **File W-013:** exact native, Chromium JS PWA and iPad Safari/Home Screen/managed Web Clip where supported; export user gesture → cancellation/failure → selected external file → independent reopen → owner-locked restore; distinguish \`API_SUPPORTED\`, \`HANDOFF\`, \`PERSISTED\`, \`VERIFIED\`. Screen reader/focus and truthful copy must be checked.
3. **Disaster W-014:** synthetic edits C0→C1 after backup, offline two-tab mutation, app-origin removal/device reprovision, actual external-file + key custody, restore on fresh device, old Sync cursor fenced, later manual Delta convergence; no PASS without independent full-ledger and newest-work comparison.
4. **Policy/crypto W-015:** for *each owner-approved candidate* run stolen-file confidentiality, wrong/lost key, metadata tamper, replay, cancellation, managed→unmanaged destination, retention/deletion and accessible recovery negative controls. Cryptography implementation review is a separate Engineering/security obligation, not implied by Web Crypto primitives.

For every campaign record source SHA, build mode and artifact digest, browser/OS/MDM/install class, synthetic fixture and 37-store inventory, file byte digest, independent destination/readback, destructive stimulus, expected/observed semantic oracle, result PASS/FAIL/UNKNOWN/NOT RUN and failure cleanup. **An artifact SHA, checksum, green host test or successful share promise is never a substitute for an independent restore.**

### OPEN / DEPENDENCY / CHANGE WATCH / ADJACENT-VALUE CHECK

- **Resolved at product-state level:** FILE user-facing flow is **NOT IMPLEMENTED**; W-013/014 cannot be promoted by B1 codec evidence. **Still OPEN:** any experimental internal caller, exact future platform file adapter, user-approved encryption and backup policy, MDM classification, physical EFB evidence, currentness witness and native/server Sync convergence.
- **DEPENDENCY:** W-012 → W-013 → W-014; W-015 may study decisions independently but cannot approve them. Exact NORMAL release artifact and managed iPad access remain independent cross-track blockers.
- **CHANGE WATCH:** LogMate \`MASTER.md\`/W-012–015 Work state and B1/F1 schema, W3C/MDN Web Crypto API and browser file APIs, WebKit/iPadOS Home Screen storage, Apple Managed Open In and airline EFB policy.
- **Adjacent-value decision:** Product-authority review closes the most consequential “maybe an existing file caller encrypts it” ambiguity and identifies a real sequencing gate. Further static cryptography pattern research would not resolve the missing W-013 user flow or physical-file custody. The next valuable work requires **owner-authorized W-012/W-013 Engineering execution, exact NORMAL artifact and physical/managed device evidence**; do not manufacture extra conceptual scenarios in lieu of these prerequisites.

**Gate: Applied Stage 8 ACTIVE; B1 bounded repository foundation, FILE NOT IMPLEMENTED; production backup, physical EFB and release validation OPEN; PWA release HOLD. No production incident, leaked file, encrypted product export, or cross-device transfer claimed.**
---

## 2026-10-27 — Applied Stage 8 LBK restore resource admission and bounded-parser failure domain [SOURCE / SYNTHESIS / CONTRADICTION / VALIDATION PLAN / DEPENDENCY / OPEN / CHANGE WATCH]

### Evidence and actual product reachability

**Source pinned, read-only:** LogMate `main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f`; `lib/repository/logbook/whole_ledger_backup.dart@711f784534bc686a4d8edd6617ac4d1ac362e0a7` lines 15–60 and 67–76; `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb` lines 486–557 and 5807–5880; `test/repository/logbook/whole_ledger_backup_test.dart@2f9d6b0a9a6a494dfd64c95b1e3db8aaa562537b`. Marketing Manager current D8 independently flagged the same resource-admission question. Web Manager owns the **PWA/file-ingress trust and device-availability contract**, not a product code fix.

The current `WholeLedgerBackup.decode(String source)` immediately calls `jsonDecode(source)` before checking the top-level map and 37/30-store registry. It then allocates row maps/lists; `_validateLbkContainer` verifies owner UID, format/capability, source replica shape, registry names/counts, digest, row shape, duplicate keys and exact store inventory **after** the entire JSON has been parsed. Digest verification canonicalizes the entire object recursively and SHA-256 encodes the resulting complete string; SHA-256 itself builds a UTF-8 byte array and padded copy. The inspected entrypoints contain **no explicit maximum encoded-byte/character size, total row count, per-store row count, per-value size, nesting depth or CPU/time work budget**. Registry count equality is **not** an upper bound: a self-consistent manifest can declare very large counts. The unkeyed digest can be recomputed by whoever authors a backup; it is not a resource admission token or authenticated provenance.

**Positive boundary:** `restoreWholeLedgerBackup` performs decode and `_validateLbkContainer` **before** entering the Sembast write transaction, then checks fresh/empty/unbound destination and validates references inside the transaction; existing tests cover malformed/duplicate/digest and injected rollback. Thus this source review does **not** show partial database writes on ordinary decode rejection. It also does not prove safe behavior for memory exhaustion, stack overflow, browser tab termination or an interrupted huge write. The `test/...whole_ledger_backup_test.dart` native file fixture is a developer test, not a shipped end-user file-picker. Canonical MASTER/W-012–W-015 still say **user-facing LBK file import/export is NOT IMPLEMENTED**. Accordingly the risk is a **pre-release file-ingress and parser-availability requirement**, not a demonstrated current malicious-file exploit, data loss or field incident.

### Standards and failure mechanics [SOURCE / HISTORY → STANDARD → IMPLEMENTATION]

- [Dart jsonDecode API](https://api.dart.dev/dart-convert/jsonDecode.html), checked 2026-10-27: parses an input string into an object; its documented API does not supply a per-call byte/row/depth admission policy. [JsonDecoder.convert](https://api.dart.dev/dart-convert/JsonDecoder/convert.html) returns nested maps/lists and can throw FormatException for invalid JSON. This does not imply that every resource exhaustion is safely expressed as FormatException.
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), checked 2026-10-27: validate content/type and **bound file size** with defense in depth. The generic server-upload context transfers to local PWA *file ingestion*, but server-side malware scanning/storage advice does not automatically apply to a user-selected local LBK.
- [MITRE CWE-400](https://cwe.mitre.org/data/definitions/400.html), checked 2026-10-27: uncontrolled limited-resource consumption can affect availability. CWE-400 is a **high-level class**, not evidence of a LogMate CVE or an exploitability verdict.
- [MDN FileReader.readAsText](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsText), checked 2026-10-27: whole-file text reading loads the file into memory and is not suited to large files. Switching to a Blob/stream only reduces pre-read pressure if the **parser and verification path** are also designed to enforce bounds; merely reading in chunks then joining to one giant string is not a solution.
- **Failure chain (conditional):** large or deeply nested selected file → whole-string/JSON allocation → nested row materialization → recursive canonicalization → full-string UTF-8/hash copies → potential UI jank, tab termination or restore denial on memory-constrained Safari/managed iPad. None of those runtime effects has been observed for the product. A valid digest, valid owner UID and 37-store registry do not make the resource workload bounded.

### Proposed W-012→W-013→W-014 admission contract [MINTTAP DECISION — PROPOSED / DEPENDENCY]

1. **W-012 Engineering:** establish representative real-world *synthetic* logbook sizes (rows, fields, nested payloads, Unicode, 30-store v1/37-store v2, Sync receipts, maximum expected operational history), benchmark parse/validate/canonicalize/restore on disposable Dart host and actual JS browser profiles. Select product limits from evidence and pilot-data needs, **not an invented MB ceiling**. Test normal large histories to avoid rejecting legitimate pilots.
2. **W-013 file ingress:** reject oversize files **before full text allocation** using a documented maximum file-byte budget; independently bound decoded nesting, total rows, per-store rows, string/value size and work. Enforce limits at a boundary the parser cannot bypass; metadata, extension, manifest counts, MIME and digest are insufficient alone. If an implementation uses streaming, verify that it actually rejects before unbounded materialization. Keep user-selected files out of executable HTML and never render raw flight text as markup.
3. **W-012/W-013 integrity and authority:** keep exact format/owner/digest/registry and empty-staging checks; do not use a size limit as a substitute for content/owner/duplicate/revision/Sync checks. A digest-valid oversize file must fail **before destination mutation**, with a typed, non-sensitive user-facing explanation. Wrong-owner and invalid versions fail separately; unknown resource outcome is not “backup corrupt” or “restore complete.”
4. **W-014 device envelope:** independently run Safari normal tab, Home Screen PWA and managed EFB Web Clip under permitted MDM/file-provider conditions; include process restart, offline operation and storage pressure. Record OS, build, source/destination, size and peak memory where feasible. A browser-killed parse must not erase existing unique data or silently publish partially restored Sync authority.
5. **UX/measurement:** present “file too large for this version/device” distinctly from malformed, wrong-owner, unsupported version and interrupted restore; preserve source file and existing ledger, offer safe alternative transfer without promising automatic recovery. Telemetry may capture coarse error class/size band, never file bytes, UID, flight contents, auth tokens or raw identifiers.

### Falsifiable integrated tests — RA01–RA12 [VALIDATION PLAN, NOT RUN]

| ID | Positive/negative oracle |
| --- | --- |
| RA01 | Valid representative v1 30-store and v2 37-store LBK both pass; record source byte size, row count and exact semantic restore, not just parse |
| RA02 | One byte above selected input cap rejects before JSON parse/full text allocation; one below still undergoes semantic validation |
| RA03 | Small-byte high-row-count fixture and many empty/short rows hit independent row budget; manifest count self-consistency does not bypass |
| RA04 | Small row count with one oversized nested value hits value/depth budget; no recursive canonicalization crash |
| RA05 | Deeply nested JSON, malformed Unicode/JSON, duplicate row keys and unknown stores fail with typed, bounded errors |
| RA06 | Digest-valid, correct-owner oversize file rejects despite valid checksum; no destination mutation |
| RA07 | Wrong owner, unsupported version, malformed registry, bad digest and invalid Sync references each reject independently |
| RA08 | Inject failure before writes, mid-transaction and during post-write reference validation; compare raw all-store snapshots/replica/owner and retry semantics |
| RA09 | Retain populated *existing* destination and attempt restore; refuse without overwriting local records or outbox |
| RA10 | Browser UI remains responsive or reports an explicit bounded failure under large-but-allowed parse; capture process termination as FAIL/UNKNOWN, not PASS |
| RA11 | Safari/Home Screen/managed Web Clip execute separately; no host/Chrome memory result is promoted into managed-iPad proof |
| RA12 | Cancel file selection, storage pressure, interrupted file read and denied managed-file destination leave ledger intact; independent file reopen/restore remains required |

**Five-track transfer:** **E** owns resource/owner/trust boundaries and safe admission; **A** owns browser File/Blob/worker/OS mechanics; **C** owns RA01–RA12 independent runtime and accessibility/performance oracles; **B** consumes Design Studio W121/CD127 for non-destructive, understandable failure/retry UX; **D** consumes Marketing D8–D10 to avoid claiming robust file restore/managed-EFB support. Engineering owns actual limits, code, fixture and execution; no peer/product changes authorized.

**CONTRADICTIONS:** “valid SHA-256” ≠ “bounded work”; “37 registered stores” ≠ “bounded rows”; “decode failed before transaction” ≠ “browser process survived”; “host fixture passed” ≠ “Safari EFB accepted”; “file adapter planned” ≠ “file import shipped.” **CHANGE WATCH:** product W-012–015 state, codec/registry, Flutter/Dart runtime, WebKit memory policy and real EFB device limits.

**Checkpoint/adjacent-value decision:** The previously unrecorded *preparse resource admission* requirement is now tied to actual pinned decoder/restore code, primary guidance, positive existing rollback protection and twelve falsifiable tests. The next high-information-gain step requires Engineering-approved fixture/limits and actual browser/device execution; further speculative numeric ceilings or malicious-file narratives would be filler. **Stage 8 ACTIVE · source-level conditional resource risk · production file-ingress validation OPEN · PWA release HOLD.**

## 2026-10-27 Stage 8 — LBK JSON interchange ambiguity, canonical digest and future cross-runtime admission (JA01–JA13)

**Evidence status:** SOURCE + SYNTHESIS + executed **synthetic Node 22.16.0 JavaScript JSON diagnostic 13/13 PASS**; **LogMate Dart parser acceptance, actual LBK restore, JS/Wasm build, physical/managed iPad and production validation OPEN**. Pinned source: LogMate `main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f`, `lib/repository/logbook/whole_ledger_backup.dart@711f7845` and `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4`. This is an adjacent **interchange semantics** checkpoint, not another file-size/DoS primer or an allegation of a shipped exploit. User-facing W-013 file import/export remains **NOT IMPLEMENTED**.

### History/problem → principle → standard [SOURCE]

JSON's portability is weaker than “every parser sees the same data.” [RFC 8259 §4](https://www.rfc-editor.org/rfc/rfc8259.html#section-4) says object member names SHOULD be unique and warns that duplicate-name receivers differ. [RFC 7493 §2.3](https://www.rfc-editor.org/rfc/rfc7493.html#section-2.3) strengthens this to **MUST NOT contain duplicate names** after unescaping, while §2.2 limits interoperable numeric precision to the IEEE-754 range and recommends strings for exact larger integers. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) defines a particular interoperable JSON Canonicalization Scheme (JCS) requiring I-JSON input, Unicode validity, ECMAScript-compatible number serialization, UTF-16 code-unit property sorting and UTF-8 output. **Sorting JSON keys alone is not a claim of RFC 8785/JCS conformance.** These sources were checked 2026-10-27.

### Exact current implementation [SOURCE]

- `WholeLedgerBackup.decode(String source)` invokes Dart `jsonDecode` first, then converts already-parsed root/manifest/stores and row objects into maps/lists. It does not inspect raw JSON member-token multiplicity before map construction. This is a **source-visible absence of a duplicate-member admission step**, not proof of Dart's exact duplicate-member runtime behavior.
- `_validateLbkContainer` checks format/version/UID/replica, recomputes `snapshotDigest` from `WholeLedgerBackup(manifest: unsigned, stores: backup.stores).encode()`, validates 30/37 registry entries, row shape and **duplicate row IDs**. The latter is a different concept from duplicate **JSON object property names** that may already have been collapsed by parsing. Exact source lines 5807–5880.
- `WholeLedgerBackup.encode()` recursively sorts map entries then calls Dart `jsonEncode`; `lbkSha256` hashes UTF-8 bytes of that **post-parse canonical representation**. It is an unkeyed checksum, not author authentication, and it does not attest the exact originally selected raw file bytes. This does not by itself mean current valid LogMate-generated backups contain duplicate members.
- The current codec is Dart on native and web builds. A **hypothetical external JS parser, verifier, WebAssembly path, independent recovery tool or future file format** introduces additional cross-runtime semantic risk; it is not proof of present Native↔PWA mismatch.

### Bounded executed diagnostic [VALIDATION — SYNTHETIC ONLY]

A Web Manager-owned, dependency-free Node diagnostic `research/handoffs/lbk_json_interop_ambiguity_lab.mjs` was executed under Node **22.16.0**. **13/13 PASS**. It verifies: (JA01–04) duplicate vs unique JSON texts can have different raw SHA-256 but identical parsed/canonicalized **synthetic JS** digest; (JA05) escaped/literal duplicate member-name collision; (JA06–07) row/nested member collapse; (JA08–11) IEEE-754 safe boundary and precision loss above it, and numeric spelling normalization; (JA12) JS parsing of a lone surrogate escape that RFC 8785/JCS rejects; (JA13) deterministic ASCII property order for the lab's **own** sorter. This is **not** an implementation of JCS, LogMate's Dart canonicalizer or an LBK acceptance harness. No LogMate source was executed in this diagnostic.

**Counterexample:** `{"ownerUid":"A","ownerUid":"B"}` and `{"ownerUid":"B"}` are different raw texts. JavaScript `JSON.parse` yields the same object; a digest over a post-parse JS serialization cannot distinguish their raw source. A valid LogMate digest is recomputable by an author; **actual crafted-file acceptance by Dart remains untested**. Another example: JavaScript parses `9007199254740993` as `9007199254740992`; whether any actual LogMate field ever uses such a JSON number is **OPEN**, not presumed.

### Expert operational judgment [MINTTAP DECISION — PROPOSED, NOT PRODUCT APPROVAL]

1. Preserve the existing v1/v2 LBK format and historical digest contract until owner-approved migration evidence exists. **Do not silently replace its canonicalization with JCS**: doing so may invalidate historical backups even if both algorithms are reasonable. If a stricter future format is approved, version it, specify exact byte/number/Unicode semantics and keep a bounded historical verifier.
2. For W-012 Engineering validation, test **both generated genuine LBK fixtures** and crafted duplicates at root/manifest/row/value nesting; escaped-equivalent keys; large integer, fractional, exponent and Unicode/surrogate cases. Separate **raw file bytes**, **decoded semantic object**, **canonical checksum**, **owner/registry/row/reference validation** and **destination transaction** verdicts. A syntactically parseable JSON document must not automatically be treated as a supported LBK.
3. For W-013 future file ingress, if the product requires I-JSON uniqueness, enforce it with a parser/tokenizer that can see duplicate member tokens **before they are lost**. Checking `map.keys.toSet().length` after `jsonDecode` cannot prove the original source had no duplicate property names. Keep byte/work limits from RA01–RA12 as a separate first-stage gate.
4. Do not assume JavaScript numbers preserve Dart integer semantics for all inputs. Inventory actual manifest/row numeric fields and values before selecting whether future cross-runtime exchange needs bounded numbers or decimal strings; no arbitrary schema change is authorized.
5. For future authentication/integrity, define whether the assurance target is **exact source bytes**, **canonical semantic content**, **authenticated origin**, **current owner authority** or **recovery freshness**. These are independent and a checksum does not supply them all.

### Falsifiable next acceptance campaign [VALIDATION PLAN — NOT RUN]

| Case | Required oracle |
| --- | --- |
| JA14 | Actual Dart `jsonDecode` and LBK `decode` duplicate-member behavior on disposable fixture, with exception class and no destination mutation |
| JA15 | Valid generated v1/v2 LBK round-trip under exact Dart native and compiled JS; verify byte/digest/semantic agreement |
| JA16 | Same-name escaped keys at manifest, row and nested value; reject or explicitly document normalization, without false-green |
| JA17 | Unsafe JSON integer and exponent/decimal input; compare Dart JIT, compiled JS, and only if targeted Wasm |
| JA18 | Unicode surrogate/non-BMP key and value; exact hash and semantic or typed rejection, no silent replacement |
| JA19 | Parser/format migration: historical genuine backup accepted with historical verifier; new strict format cannot downgrade into old acceptance |
| JA20 | Hash-correct but wrong owner/registry/revision/Sync references still fail before any destination write |
| JA21 | Safari/Home Screen/managed Web Clip import path separately exercises chosen parser and preserves unique existing data after negative cases |

**Five-track ownership/transfer:** **E** owns trust-format/version/restore admission and no silent digest migration; **A** supplies JS/Dart/Wasm/browser number/Unicode/stream mechanics; **C** independently tests raw-vs-semantic oracles, negative cases and exact runtime; **B** consumes Design Studio W121/CD127 for distinguishable “unsupported/invalid backup” versus “wrong account” versus “too large” recovery UX; **D** consumes Marketing D8–D10, prohibiting “secure, universally portable backup” or “PWA transfer complete” claims without runtime proof. Software Engineering owns actual Dart/JS parser and format-version implementation, not Web Manager. No peer/product writes.

**CONTRADICTION:** “digest matches reconstructed JSON” ≠ “raw file bytes authenticated”; “duplicate row IDs rejected” ≠ “duplicate JSON property names rejected”; “sorted keys” ≠ “RFC 8785 JCS”; “JS 13/13 PASS” ≠ “Dart LBK acceptance”; “safe in JS” ≠ “exact Dart integer transfer”; “old verifier works” ≠ “new format approved.”

**CHANGE WATCH:** Dart JSON parser behavior, Flutter JS/Wasm compilation, actual LBK field value ranges, format/codec version, Safari/Wasm support, file-ingress W-012–W-014 status. **Meaningful checkpoint:** The prior RA resource gate addressed *bounded work*; this JA continuation addresses *semantic identity and historical verifier compatibility*, a separate pre-release risk. Next high-value evidence is the exact Dart/compiled-JS fixture rather than more speculative format diagrams. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


## 2026-10-27 Stage 8 — genuine historical v1 LBK cross-runtime digest evidence and private-fixture CI boundary (JA22–JA35)

**Scope / pinned custody.** Read-only source at LogMate `main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f`: `lib/repository/logbook/whole_ledger_backup.dart` blob `711f784534bc686a4d8edd6617ac4d1ac362e0a7`, **genuine v16-exported format-v1 fixture** `test/fixtures/f1_v16_populated_format_v1.lbk` blob `e702040503997f5f6c8cf099314c5607537d864c`, and historical W-019 Dart VM test receipt `docs/evidence/w019-f1-backup-boundary-2026-10-27.jsonl` blob `d08cd6ad1c59a9a4f8d48c1e23a7bbeb8c47c674`. The fixture was inspected through the authenticated GitHub connector **in memory only**; its bytes were **not copied into public Web Manager**, logged, embedded in a CI artifact or published in this study. No LogMate or peer-repository writes.

### 1. SOURCE — actual positive Dart evidence exists, but its scope is narrow

The W-019 JSONL records exactly two named, successful **Dart VM native repository** tests in the focused `whole_ledger_backup_test.dart` suite: (a) F1-B01 restoration of a populated v16 genuine format-v1 exporter fixture without inventing Sync authority, and (b) B1 native staged file round-trip of canonical records/outbox. The receipt ends with `success:true`; its source path identifies a controlled local checkout at `7caaee9`. The latest-main test file still contains those tests. **This upgrades the historical v1 native fixture restore evidence from “only planned” to bounded receipt-backed PASS at the recorded checkout**, not to current-main re-execution, v2 cross-runtime compatibility, installed Safari, external user FILE UI, real Firebase or managed EFB. The fixture itself has 30 stores, 4 active records, 9 outbox rows and 9 revision rows; this is not a 37-store v2 specimen.

### 2. VALIDATION — independent JavaScript/V8 digest on the genuine fixture, not another synthetic-only object

An independent, in-memory **V8 JavaScript** SHA-256 implementation was checked against the two published SHA-256 vectors for empty input and `abc` (**2/2 vectors PASS**), then used on the connector-fetched genuine fixture. Its recursive property-name sort, JSON serialization and UTF-8-equivalent ASCII byte hashing produced:

- Actual genuine fixture text length: **41,794 bytes** (ASCII in the inspected fixture); reconstructed unsigned canonical JSON: **41,710 bytes**.
- `snapshotDigest` from manifest: `29ebc34e050fc3f809e87464ed0b61693af37393fdaa8a7dc9411b9cc56c4345`.
- **Independently computed V8 SHA-256 of sorted unsigned JSON: exactly the same digest.**
- Raw original-file SHA-256: `3c90c6cacd300aeaad87aaff7529ddddb15949e3b8319436992364cef5b41873` — a *different referent*, not a mismatch.
- Manifest registry and parsed stores both enumerate **30** stores. The inspected fixture has no numeric values outside JavaScript's safe-integer range and no non-ASCII raw bytes; these are **fixture-specific observations**, not a universal LBK guarantee.

This is stronger than the previous JA01–JA13 synthetic-only Node result: **one actual LogMate-produced historical v1 container has matching Dart-exported digest and independent JavaScript semantic-digest computation**. It is still **not** an executed LogMate Dart→compiled-JS round trip, a complete JS LBK verifier, a format-v2 result, a source-file-byte signature, or a successful browser restore.

### 3. Falsification — two distinct raw files can collapse into the same parsed semantic object

Against the *actual* fixture text, a controlled V8 diagnostic inserted a duplicate root `manifest` property before the original and separately inserted a duplicate manifest `ownerUid` before the original value. In both cases, **raw SHA-256 changed**, but `JSON.parse` returned the **same object** as the original and the recomputed semantic checksum stayed equal. This directly demonstrates the *JavaScript parser's* duplicate-member collapse on the genuine fixture's shape. It does **not** demonstrate that Dart's `jsonDecode` or LogMate's `restoreWholeLedgerBackup` accepts these crafted files; those exact JA14/JA16 cases remain OPEN.

**History → standard → judgment:** RFC 8259 §4 warns that duplicate JSON member names are not interoperable; RFC 7493/I-JSON forbids duplicates, while RFC 8785/JCS requires a specific Unicode/number canonicalization and is **not** the current LBK format. A semantic checksum over a parsed map is useful for corruption detection, but cannot prove original file byte identity, member uniqueness, author identity or current owner authority. The genuine fixture match must not be used to retrofit JCS into v1/v2 or to claim universal JavaScript number/Unicode compatibility. References checked 2026-10-27: https://www.rfc-editor.org/rfc/rfc8259.html ; https://www.rfc-editor.org/rfc/rfc7493.html ; https://www.rfc-editor.org/rfc/rfc8785.html .

### 4. VALIDATION / CONTRADICTION — public research CI cannot automatically read private LogMate

A Web Manager-only, **read-only** GitHub Actions workflow attempted to checkout pinned `yhappcom/logmate` using the Web Manager workflow's ordinary `GITHUB_TOKEN`. [Run 40486599476](https://github.com/yhappcom/web-manager/actions/runs/40486599476) **FAILED before any test**: checkout log reported `Repository not found` / exit 128 for the private cross-repository fetch. This is a **credential-scope / test-fixture availability failure**, not an LBK digest mismatch or product defect. The nonworking automatic workflow was **removed** from `main` to avoid repeated false failures. No personal access token, elevated cross-repository credential, private fixture copy or security exception was added.

A durable [independent Node oracle](handoffs/lbk_genuine_v1_independent_node_oracle.mjs) remains as a **local/Engineering handoff** for an environment already authorized to read both repositories. It pins the fixture blob, genuine manifest checksum, store counts, raw-vs-semantic distinctions, crafted duplicate controls and W-019 receipt. **This Node file was NOT executed in the failed CI**; its tests are **NOT PASS**. The in-memory V8 computation above is separately executed and must not be misreported as this Node file's hosted run. Engineering can run `node --test` after independently checking out the exact private LogMate ref in an approved environment; record Node version, source blobs, test output and no-public-fixture-retention. A future hosted workflow requires explicitly approved, least-privilege private-repository access and a secrets/retention review; do not silently grant it.

### 5. Cross-track assessment and actionable admission

| Track | Evidence maturity / dependency pressure | Ownership or consumption |
| --- | --- | --- |
| **E — highest bottleneck** | Genuine historical v1 checksum interoperability **PARTIAL PASS**, file-authenticity/owner/currentness and version migration OPEN | Owns backup trust model, private-source custody, fail-closed historical reader, no unreviewed credential escalation, release HOLD. |
| **A — prerequisite supplier** | JS/V8 on real ASCII/safe-integer v1 fixture; actual compiled Dart JS/Wasm, WebKit and file APIs OPEN | Owns parser/number/Unicode/browser differences; cannot generalize fixture-specific agreement to v2 or Safari. |
| **C — independent challenger** | Historical Dart VM two-test receipt + V8 digest match; Node hosted run NON-EXECUTION | Owns JA14–JA21 exact-product runtime, fixture provenance, negative controls, browser/process/MDM acceptance. |
| **B — consumer** | Design Studio `progress/WEB_STATUS.md` W121 remains Stage 3 PRACTICE, runtime/AT/human OPEN | Require explicit “historical file unsupported/invalid” versus wrong-owner/too-large/recovery-required states; no generic success toast. |
| **D — consumer** | Marketing `STATUS.md` D8/D9 holds public PWA/backup/Sync claims; no release proof | No “universally portable backup”, “secure encrypted file”, or “installed EFB sync” from this bounded checksum result. |

**TRANSFER VALIDATION:** Software Engineering `research/data/D005_backup_restore_recovery_acceptance.md` separates artifact existence, physical integrity, schema/semantic validation and safe publication; `D006_logmate_inbound_cursor_atomicity_transfer.md` separates atomic cursor+effect publication from backup/Sync trust. This fixture only advances the **historical v1 semantic checksum** layer; it cannot substitute for full 37-store recovery-evidence preservation (see 506), owner-lock/remote ACK, independent external file custody or current NORMAL release identity.

### 6. Next falsifiable integrated acceptance, without micro-test proliferation

- **JA22–JA24:** Engineering reruns genuine pinned v1 in actual Dart VM and compiled JavaScript, compares exact manifest/digest/30-store semantics and verifies the two W-019 tests on the *new* source head. Include real 37-store format-v2 exporter fixture and independent JS check, rather than treating v1 as v2.
- **JA25–JA28:** Exercise raw duplicate root/owner/row/nested properties (including escaped-equivalent names), unsafe integers, exponent spelling, Unicode/surrogates, wrong-owner and correct-checksum malicious inputs through the *actual* Dart decoder and staged restore; assert typed reject/no mutation or explicitly approved compatibility behavior. Enforce preparse resource limits separately.
- **JA29–JA32:** Verify historical v1 reader remains compatible across future versioned strict-format migration, preserve backup provenance and restore trust reset, detect transformed-key Sync hold collision and compare 37-store semantic source/destination with exact owner/replica/receipt oracles.
- **JA33–JA35:** After W-012 repository acceptance and W-013 user FILE implementation, verify independently saved-file reopen, Safari/Home Screen/managed EFB container separation and W-014 owner-authorized transfer; retain the last known-good file and unique offline records under interruption/eviction. No claim of unattended device-to-device Sync.

**OPEN:** actual Dart duplicate behavior, actual compiled-JS v1/v2 agreement, real file UI, non-ASCII and unsafe-number transfer, Node oracle execution in an authorized private-repo environment, cross-version migration, 37-store exact-product restore, physical/managed iPad. **MINTTAP DECISION:** preserve historical v1/v2 format pending versioned migration review; keep private fixture private; do not authorize public CI cross-repo credential escalation solely to make a research test green. **CHANGE WATCH:** LogMate W-012/013/014, fixture/code hashes, Flutter/Dart compiler, WebKit and managed EFB policies.

**Checkpoint:** meaningful partial promotion of genuine historical-v1 *semantic digest* evidence, plus a proven CI access boundary. The adjacent valuable question — whether existing W-019 Dart VM evidence already exists — was resolved in the same run. Further progress now requires a deliberately authorized private-repository execution context and real Dart/browser product tests. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


## 2026-10-28 Stage 8 — RH historical finding superseded by merged W-012 native repair [SOURCE / CONTRADICTION RESOLVED / TRANSFER VALIDATION / OPEN]

**Evidence provenance and correction.** The RH01–RH24 analysis immediately below is an **historical snapshot of LogMate `main@d3bc214` (2026-10-27)**, not a statement of the current product implementation. Re-read LogMate latest `main@2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf` on 2026-10-28: `lib/repository/logbook/sembast_logbook_repository.dart` blob **`021d9001ae1240a824c5df570fb679597edc3875`**, `test/repository/logbook/w012_backup_semantic_verification_test.dart` blob **`36f28135cbefaf0e715802151c5eed60affbb314`**. The B1 codec remains blob `711f7845`. See [merged W-004 product head](https://github.com/yhappcom/logmate/commit/2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf), [actual repository implementation](https://github.com/yhappcom/logmate/blob/2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf/lib/repository/logbook/sembast_logbook_repository.dart), [W-012 regression source](https://github.com/yhappcom/logmate/blob/2f78e7310dfe2c46c1f1cba0583e2abdd269ffdf/test/repository/logbook/w012_backup_semantic_verification_test.dart). The source is private; do not copy private fixtures or pilot records into public research.

### What changed, and what was actually falsified [SOURCE / CONTRADICTION]

1. **Derived recovery-HOLD collision:** The earlier `_resetRestoredSyncTrust` used an unconditional `put` for `restored:<sourceStore>:<rowKey>`. Current lines **569–587** first call `hold.exists(transaction)` and throw `FormatException('LBK recovery evidence key collides.')` if occupied, before `put`. The historical conditional **silent overwrite** path is **no longer supported by the current source**. This is fail-closed **rejection**, not a lossless merge of two distinct evidence events; the colliding v2 file still cannot be restored until an authorized recovery policy addresses the conflict. Do not call it a successful A→B→C migration.
2. **Nonempty staging Sync state:** The old audit saw only twelve record stores in the staging guard. Current `_requireEmptyLbkDestination` lines **6064–6131** explicitly rejects residual rows in six Sync stores (bindings, receipts, applied identities, applied cursor, record heads, HOLDs), and separately validates the five-key fresh `sync_state`, including `ownerUid` key presence, unbound/unverified status and matching fresh replica ID. The historical **visible staging predicate gap** is **superseded in current source**; this does not establish that every possible browser corruption/state anomaly is covered.
3. **Transaction/authority boundary:** `restoreWholeLedgerBackup` lines **486–556** parses/validates before one Sembast transaction, checks fresh staging, writes the registry, preserves destination replica identity, locks the matching Owner, resets remote authority to `unbound/unverified`, then validates restored references before commit. A collision exception is inside that transaction. Sembast documents cancellation/rollback on an error ([primary package documentation](https://pub.dev/documentation/sembast/latest/index.html)); actual native test oracles below, not package documentation alone, establish the observed bounded result. IndexedDB transactions are atomic at the browser storage level but may have crash/durability limitations ([MDN IDBTransaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction)); this does **not** certify Sembast Web's full 37-store restore on Safari.

### Exact current regression evidence and remaining negative controls [VALIDATION / OPEN]

- W-012 source lines **523–611** runs two separate collision cases for **cursor** and **applied identity**. It constructs A→B, preserves the original HOLD, then places a noncolliding row *before* the colliding row, exports B, attempts restore into fresh C, asserts a `FormatException` containing `collides`, checks that **all destination registry stores remain unchanged**, source B is unchanged, replica and Owner state remain fresh, and **reopens C** to confirm rollback. It then retries a clean earlier file successfully, verifies locked Owner, HOLD preservation and reopen. These are materially stronger oracles than a thrown exception or a synthetic Map model.
- W-012 source lines **337–385** exercises residual rows in each of six Sync stores, modified Sync State, and malformed default Sync State; every case rejects and compares pre/post state including reopen. These cases directly answer the old RH staging counterexample **in native Sembast IO**.
- Prior [515 §12](515_stage8_pwa_local_ledger_storage_backup_restore_custody_and_device_transfer_20261024.md) records W-012 focused **70 PASS** and full native **900 PASS / 1 browser-only SKIP** at its pinned verification; this run **did not execute** tests again. Source inspection is independently performed here. The old RH01–RH10 Node model remains a valid demonstration of the **previous unsafe transformation**, not evidence of a present defect.
- **Still OPEN:** exact NORMAL Flutter Web/Sembast Web transaction semantics; 37-store restore with browser quota/termination, same-origin independent-tab interference and persistence after process restart; installed Safari Home Screen and MDM Web Clip; genuine managed EFB file export/picker/readback; non-collision multi-hop recovery that preserves distinct historical events; future authenticated Manual Sync Receipt/Apply/Cursor. Native W-012 PASS cannot be promoted to any of these gates. Existing RH11–RH24 should be interpreted against the **new guarded source**, not used as a demand to reintroduce unsafe overwrite.

### Five-track transfer and operational decision [MINTTAP DECISION / DEPENDENCY / CHANGE WATCH]

**E owns** current collision-rejection and data-custody contract: an unimportable colliding backup is a **blocked, non-destructive recovery** requiring retained source file and an approved conflict-resolution route; never silently rename/drop historical HOLDs. **A** owns Sembast Web/IndexedDB and Safari transaction/container differences; **C** owns exact browser/37-store independent pre/post raw-store and crash/reopen oracles; **B** consumes Design Studio W121/CD115 for accessible `recovery blocked—source preserved` vs `restored` states, without implying data loss; **D** consumes Marketing D8 claim HOLD and must not treat native rollback tests as an EFB backup guarantee. Engineering D005 remains canonical for generic validate-before-publish and W-012→W-014 product implementation. **No new LogMate patch, server/Sync authority change, or new synthetic test is proposed.** Change-watch current LogMate file blob, exact resolved `sembast_web` implementation and Apple/MDM policy.

**Gate:** historical RH silent-overwrite/staging-gap concerns **RESOLVED AT CURRENT NATIVE SOURCE + REGRESSION-TEST LEVEL**; installed/browser/managed EFB recovery **OPEN**, Stage 8 ACTIVE and PWA release **HOLD**. The next high-information-gain step is Engineering-authorized **actual NORMAL Web 37-store** collision/rejection/clean-retry plus file readback, not another pure-state model.

---

## 2026-10-27 Applied Stage 8 — repeated LBK recovery evidence namespace and staging-custody admission (RH01–RH24)

**Scope and provenance [SOURCE].** Read-only exact LogMate \`main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f\`: \`lib/repository/logbook/sembast_logbook_repository.dart\` blob \`d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb\`, \`lib/repository/logbook/whole_ledger_backup.dart\` blob \`711f784534bc686a4d8edd6617ac4d1ac362e0a7\`, \`test/repository/logbook/whole_ledger_backup_test.dart\` blob \`2f9d6b0a9a6a494dfd64c95b1e3db8aaa562537b\`, and approved Sync domain contract \`docs/specs/local-first-manual-delta-sync-contract.md\` blob \`2240fc1b6adf5fcd041a44de0e4660eb1528e92a\`. Web Manager \`main\` before this checkpoint: \`65e0963ddbf7abeda3756c0c8cbe1d8f6f7f0389\`. Relevant independent sources reviewed 2026-10-27: [Sembast RecordRef API](https://pub.dev/documentation/sembast/latest/sembast/RecordRef-class.html) (\`put\` saves/creates, \`add\` creates only if absent; check exact resolved package version before product execution); [Sembast transactions](https://pub.dev/documentation/sembast/latest/) (exception cancels transaction); [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) (preserve integrity, prevent evidence modification/deletion); [NIST SP 800-53 CP-9](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) (backup/recovery control framework, not a product certification). Existing [Engineering D005](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D005_backup_restore_recovery_acceptance.md) separately establishes validate-before-publish, not LogMate runtime proof.

### A. History/problem → failure-domain principle [SYNTHESIS]

A backup is not only the latest projection of Flight rows. In a local-first, later-synchronizing ledger, a recovered destination must distinguish **source historical Sync evidence**, **destination-local remote-apply authority**, and **recovery evidence describing the transition**. A new replica must not inherit the old replica's applied cursor/receipt as its own authority. Equally, it must not silently discard the evidence needed to explain what was previously known or unresolved. Repeated transfers A→B→C, rebootstrap after long dormancy, and restore into a supposedly fresh database are the relevant stress cases. This question is **distinct** from JA JSON duplicate-member ambiguity, RA parser resource limits, and earlier LBK file confidentiality.

### B. Exact implementation and positive controls [SOURCE]

1. Current v2 exporter enumerates **37 stores** (30 legacy + 7 Sync), including \`logmate_sync_holds_v1\`, \`logmate_sync_applied_cursor_v1\` and \`logmate_sync_applied_identities_v1\`. It creates one transactionally read, checksum-bearing container. v1 uses the 30-store registry. The unkeyed digest authenticates neither writer nor organizational currentness.
2. \`restoreWholeLedgerBackup\` parses and validates before opening the destination transaction; within the transaction it calls \`_requireEmptyLbkDestination\`, drops each registry store, restores rows, preserves the **destination's** replica identity, replaces source owner access with matching UID **locked**, and calls \`_resetRestoredSyncTrust\`. For v1 it clears all seven Sync stores and initializes unverified Sync state. A test-only after-writes failure seam and post-write ready/aggregate checks are present. These are important positive controls.
3. \`_resetRestoredSyncTrust\` takes each source cursor/applied-identity row and writes a hold at deterministic key \`restored:\${source.name}:\${row.key}\` using \`_syncHoldStore.record(...).put(transaction, ...)\`; then it drops the cursor/applied stores and resets \`streamBindingStatus=unbound\` and \`remoteBaselineStatus=unverified\`. It preserves the prior Sync state under \`restoredSourceState\`. **No existing-key collision check or versioned recovery-event identity is visible at this write site.**
4. \`_requireEmptyLbkDestination\` explicitly rejects rows in **12** flight/custom/draft/receipt stores and checks fresh structure/configuration, unbound owner and not-started local entry. It **does not directly enumerate the seven Sync stores** as an emptiness precondition. This is not proof that a normal fresh destination can acquire such rows; it is a source-visible admission gap for anomalous/fixture states.
5. \`_validateLbkContainer\` checks store registry, per-store row key uniqueness, checksum and owner UID, but does not check collisions between an existing \`sync_holds\` row key and a **future derived hold key** from cursor/applied identity. \`_validateSyncState\` checks core Sync state fields and replica/owner correspondence; it does not enumerate hold-key uniqueness across generations. Therefore a syntactically valid, digest-valid v2 container is **not automatically a proof of lossless recovery-evidence transformation**.

### C. Conditional collision scenario and falsifier [SYNTHESIS / OPEN]

Let the source v2 backup include a historical hold with key \`restored:logmate_sync_applied_cursor_v1:current\` containing prior recovery evidence E1, and an independently stored current cursor row with key \`current\` containing newer evidence E2. Each store's own row keys are unique; the manifest counts and digest can still be internally consistent. During v2 restore the hold store is first restored with E1. The later \`_resetRestoredSyncTrust\` computes the **same** hold key for E2 and calls \`put\` without an absence guard. Under documented save/update semantics, E2 can replace E1 at that key. The destination remains \`unbound/unverified\` (positive remote-authority fence), but the prior hold's distinct recovery provenance may no longer be represented. A repeated A→B→C chain can make the key reappear after a later cursor is established; whether current product workflows can reach this naturally is **OPEN** because production Manual Sync is not implemented. A crafted/controlled v2 fixture can test the source-level conditional without claiming a real incident.

A second independent scenario: a destination with unbound owner, not-started entry and no 12 checked record rows but with anomalous pre-existing Sync rows may satisfy the **visible** staging predicate. The subsequent registry drops could erase those rows. Whether opening/initialization or another invariant would already reject such a database must be tested on exact Dart/Sembast. Do **not** classify this as a demonstrated user-data loss.

**Important non-equivalences:** successful checksum ≠ no derived-key collision; 37 stores enumerated ≠ lossless inter-store transformation; \`unbound/unverified\` ≠ historical evidence preserved; one transaction ≠ semantic non-overwrite; empty Flight stores ≠ all seven Sync stores empty; a modelled Map overwrite ≠ Dart/Sembast runtime reproduction. The concern is **recovery evidence**, not proof of remote Sync authorization bypass.

### D. Bounded executable model [VALIDATION — SYNTHETIC ONLY]

Added \`research/handoffs/lbk_restore_hold_collision_lab.mjs\` (no private LogMate bytes) and executed \`node --test\` under Node **22.16.0** on 2026-10-27: **10/10 PASS**, RH01–RH10. Positive/negative oracles cover fixed derived namespace, disjoint source stores, no-collision preservation, preexisting-key overwrite in a put-like Map model, applied-identity variant, two independent keys, fail-closed collision rejection, checksum/derived-key independence, repeated recovery, and the independent staging-Sync-row predicate. This is a **JavaScript model of the observed key transformation**, not actual Dart, Sembast, file restore, Safari or managed iPad. No product defect or data-loss PASS/FAIL is asserted.

### E. Required exact-product admission campaign [VALIDATION PLAN — NOT RUN]

| ID | Exact oracle / falsification target |
| --- | --- |
| RH11 | Generate **genuine 37-store v2** with source \`sync_holds\` and \`sync_cursor\` containing the same derived destination key; run actual \`restoreWholeLedgerBackup\` in isolated Dart memory/IO Sembast; compare **all original hold values** with destination preserved provenance, not just row count. |
| RH12 | Repeat RH11 for \`sync_applied_identities\` and two different keys, ensuring both preserved; inspect exact resolved Sembast \`put\` behavior. |
| RH13 | A→B→C sequential restore after a legitimate new cursor is recorded on B; prove E1 and E2 both remain independently recoverable, or explicitly reject before mutation. |
| RH14 | v2 source has unrelated existing \`legacy:\` and \`deferred:\` holds; verify no accidental deletion/rewriting. |
| RH15 | v1 genuine 30-store fixture restores into new v2-capable destination with **no fabricated Sync cursor/receipt**; owner locked, replica regenerated, original Flight/Outbox preserved. |
| RH16 | Staging DB has no Flight rows but has a Sync cursor/hold row; determine whether open/restore rejects, preserves, or drops it. Record exact setup path and avoid labeling impossible normal states as normal product bugs. |
| RH17 | Repeat RH16 for each of seven Sync stores and for structurally nonfresh/owned destinations; require typed rejection and **unchanged original database** on invalid admission. |
| RH18 | Inject \`afterStoreWritesForTesting\` exception and retry; verify rollback of *every* store and no loss of original recovery holds, then check post-commit restart. |
| RH19 | Source checksum-valid but malformed Sync hold/cursor relationship; determine whether actual validator rejects or transforms and whether any evidence is overwritten. |
| RH20 | Owner UID mismatch and source-replica/destination-replica equality/collision negative controls; no destination authority inheritance. |
| RH21 | Re-export after restore and compare semantic evidence lineage: source E1, transferred E2, new destination replica and unverified remote baseline all distinguishable. |
| RH22 | Cross-runtime exact Dart VM / compiled JS v2 case; inspect IndexedDB/Sembast Web transaction and reopen. Do not promote desktop Chromium to Safari. |
| RH23 | Installed Safari/Home Screen and physical managed EFB iPad: offline restore, cold restart, external file custody and storage eviction/dormancy are independent from RH11–RH22. |
| RH24 | Resource/size and namespace-exhaustion negative cases; fail safely without deleting source evidence, leaking private data to logs or accepting an ambiguous “restored” success state. |

**Acceptance invariant [MINTTAP DECISION — PROPOSED, NOT PRODUCT APPROVAL]:** Every source recovery hold remains attributable and recoverable after a successful restore, or the operation explicitly rejects **before publication**; source cursor/applied identities never become destination remote authority; an anomalous nonempty destination cannot be silently treated as empty. Preserve existing v1/v2 file formats and the approved Manual Sync contract; do not mutate LogMate code, change key namespace, retrofit a format migration, or grant a cross-repo CI token without Engineering/owner authorization. A candidate fix may use an explicitly versioned, collision-free recovery-event identity, preserve multiple source evidence records, or reject on collision, but it must be measured against historical fixture compatibility and bounded storage growth. A naïve \`ifNotExists\`/throw can reject legitimate repeat transfers; silent overwrite is not the only alternative.

### F. Five-track integrated decision and dependencies

- **E primary bottleneck:** owns lossless recovery-evidence custody, destination admission, owner/replica/remote-authority separation, rollback and security claim gate. Its existing §298 JA/RA work is reused, not reauthored.
- **A dependency:** supplies Sembast Dart VM vs Web/IndexedDB behavior, deterministic key construction, transaction scope and Safari/MDM container differences; source and standards are distinct from platform runtime.
- **C independent validator:** owns RH11–RH24 positive/negative, before/after snapshots, crash/rollback and exact provenance. 10/10 model PASS is not product PASS.
- **B consumer:** Design Studio W121/CD127 requires distinct “source evidence retained but Sync verification required”, “restore rejected without changing data”, “wrong account” and “not a fresh destination” states; screen-reader/human/real runtime remain OPEN.
- **D consumer:** Marketing D8/D9 public claim HOLD; do not claim lossless multi-hop restore, installed EFB PWA portability or automatic Sync from this evidence.
- **Software Engineering handoff:** D005 validate-before-publish and Q006 false-green controls transfer as independent implementation-test methods. Engineering owns actual Dart/Sembast fixtures and fixes. Product \`MASTER.md\` and the 2026-10-17 Sync contract remain authority; **production Manual Sync NOT IMPLEMENTED**.

**CHANGE WATCH / OPEN:** exact LogMate head and Sembast resolved version (**read-only `pubspec.lock@746ef9de` currently pins `sembast 3.8.11` and `sembast_web 2.4.6`; public API search may display newer 3.9.0, so runtime semantics must be reproduced at pinned versions rather than inferred from latest docs**), current W-012/W-013/W-014 execution, real 37-store v2 fixture with nonempty Sync state, whether hold collision is reachable through supported workflows, cross-runtime transaction/rollback, managed iPad file/MDM policy. **Gate unchanged: Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

**Adjacent-question checkpoint:** This run checked not only repeated-hold collision but the separate anomalous destination Sync-store precondition, historical v1 upgrade, transaction rollback seam, independent exact-product test coverage and platform transfer boundaries. Further positive closure requires authorized exact Dart/Sembast and installed/physical-device execution, not more speculative JSON/Map variants.


## 2026-10-27 Applied Stage 8 — restored Sync binding provenance vs future remote-admission authority (RB01–RB16)

**Evidence scope [SOURCE].** Re-read LogMate \`main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f\` read-only on 2026-10-27. Exact source: [repository implementation](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/repository/logbook/sembast_logbook_repository.dart#L420-L592) (blob \`d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb\`), [restore validation](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/repository/logbook/sembast_logbook_repository.dart#L5825-L5919), [F1 binding writer](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/repository/logbook/sembast_logbook_repository.dart#L2796-L2858), [37-store native restore test](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/test/repository/logbook/whole_ledger_backup_test.dart#L780-L1025) (blob \`2f9d6b0a9a6a494dfd64c95b1e3db8aaa562537b\`), and [approved manual-delta Sync contract](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/specs/local-first-manual-delta-sync-contract.md) (blob \`2240fc1b6adf5fcd041a44de0e4660eb1528e92a\`). This is **source analysis**, not a new Dart, compiled-Web, Safari or physical-iPad execution. The approved contract expressly says production Manual Sync is **NOT IMPLEMENTED**.

### 1. History/problem → principle [SYNTHESIS]

The previous RH01–RH24 checkpoint addressed collisions while *deriving recovery holds* from old applied cursors/identities. A separate adjacent question remains: **what happens to a source replica's pending Sync operation bindings and other remote evidence when a full ledger is restored onto a different replica?** The correct distinction is between preserving an immutable operation's original identity/provenance (necessary for idempotent retry and ACK-loss recovery) and authorizing a *new device* to publish/replay it under current owner, remote stream and server policy. Changing the original operation ID to make it “new” is not a safe recovery fix. Conversely, copying an \`eligibleProven\` classification is not itself a remote-admission proof.

### 2. Exact code trace [SOURCE]

1. \`_writeF1OperationBinding\` stores a canonical binding keyed by original operation ID with \`ownerUid\`, \`originReplicaId\`, \`revisionId\`, \`payloadDigest\` and status \`eligibleProven\` for supported local Flight CREATE; unsupported/deferred mutations receive a different classification. The binding is written in the same local transaction as record/revision/outbox, which is a **positive local atomicity control**, not a server Receipt.
2. The v2 exporter copies all 37 registered stores, including \`logmate_sync_operation_bindings_v1\`, \`logmate_sync_receipts_v1\`, \`logmate_sync_record_heads_v1\`, applied identities, cursors and holds. It emits a digest-bearing container with a source-replica manifest field. The digest does **not** authenticate owner, writer or remote currentness.
3. The v2 restore copies each registry store into a fresh staging transaction, except \`logmate_local_replica_v1\`, then retains the destination-generated replica ID. It locks owner access, calls \`_resetRestoredSyncTrust\`, moves source cursor/applied-identity rows into recovery holds and drops those two stores. It sets destination \`streamBindingStatus=unbound\` and \`remoteBaselineStatus=unverified\`. **It does not drop or reclassify copied Sync operation bindings, Sync receipts or record heads on the v2 path.** The v1 path separately clears all seven Sync stores; do not conflate v1 and v2.
4. The 37-store native test asserts exact equality of source and restored stores **after excluding only local replica and Sync state**. Its populated fixture verifies flight/history/outbox/aggregate preservation and locked→unlocked owner behavior, but does not execute a remote publisher or assert that restored \`eligibleProven\` bindings are re-adjudicated before upload. Thus the test is a positive data-preservation control, not a future Sync admission oracle.
5. In the inspected repository file, \`_syncReceiptStore\` and \`_syncHeadStore\` have declarations, restore/legacy-clear and emptiness checks but **no implemented production remote read/write path**. \`_syncBindingStore\` is currently used by the local F1 binding writer and restore/export; there is no proven future manual Push implementation here. No live remote replay, unauthorized publication or user data loss was observed.

### 3. Trust-state matrix [SYNTHESIS / CONTRADICTION]

| State | Proven from current source | Not thereby proven |
| --- | --- | --- |
| Original local F1 CREATE bound \`eligibleProven\` | Local payload/digest/identity binding in a local transaction | Firebase receipt, authenticated server acceptance, remote convergence |
| Valid v2 backup contains original binding | Serialized source evidence and digest consistency | Authentic file author, unmodified original bytes, current authorization |
| Restored on fresh replica | Destination replica preserved; owner locked; Sync stream unbound; remote baseline unverified; binding rows copied | Source binding has become destination-local current Sync authority |
| Owner later explicitly unlocked | Local matching-owner access can be regained | Remote policy/stream currentness, idempotent ACK state or safe automatic replay |
| Restored ledger exported again | Historical bindings may remain transitively portable as data | Their \`eligibleProven\` marker is a reusable authorization credential |

**CONTRADICTION:** \`preserve original operation identity\` and \`do not inherit remote apply authority\` are compatible requirements, not alternatives. Likewise, \`source binding eligibleProven\` is a source-local classification; \`destination may push now\` must be a separately established decision. \`sync receipt/head copied\` does not establish that the receiving replica applied or independently verified that evidence. Current implementation does provide strong *negative* controls for destination cursor/identity trust and owner locking; do not erase those positives in a risk report.

### 4. Integrated acceptance campaign [VALIDATION PLAN — NOT RUN]

Use actual W-012 Dart/Sembast fixtures and an authorized exact-product test environment, not another synthetic-only JS model. Preserve original source and destination snapshots and compare independently specified expected deltas.

- **RB01–RB04 (source-local positives):** Construct a supported Flight CREATE and an unsupported/deferred mutation; assert binding status, original ID/digest, outbox linkage, source replica and local transaction rollback. Export v2 and assert all 37 stores, counts and manifest checksum. Capture the original \`eligibleProven\` row without fabricating a server Receipt.
- **RB05–RB08 (restore custody):** Restore to a fresh replica with a different ID. Assert owner is locked, Sync state is unbound/unverified, source binding provenance/operation ID/digest remains intact, source cursor/applied-identity authority is removed and held, and receipt/head rows (when seeded) are not accidentally interpreted as destination currentness. Include the previous RH hold-key collision control; source-file checksum alone is not the semantic oracle.
- **RB09–RB12 (transitive and negative):** Unlock owner, export B→C and inspect binding/hold provenance without rewriting original operation IDs. Inject a forged-but-digest-valid binding status, wrong-owner input, missing ACK and repeated original ID with altered payload; require explicit rejection/hold/UNKNOWN outcomes as specified by the approved Sync contract. A stale source-origin binding must not bypass current authenticated owner, server dedup or stream admission. Where Manual Sync is not yet implemented, mark these as **NOT EXECUTABLE**, not PASS.
- **RB13–RB16 (product/browser boundary):** Once Engineering implements Manual Sync and W-013 file I/O, verify exact owner-authorized first Push/Pull, same-ID retry/ACK loss, source/destination operation convergence and last-known-good backup retention. Repeat through compiled Web/Safari Home Screen and a representative managed EFB iPad under actual policy. A native Dart PASS does not imply Safari/MDM PASS, and file transfer does not imply unattended device-to-device Sync.

**Required independent oracles:** exact original operation ID/digest and origin lineage; destination replica identity; local owner lock; source/destination 37-store snapshots with documented intentional transformations; count and content of held cursor/applied evidence; no accidental duplicate server operation; authenticated server Receipt and applied-cursor continuity when implemented; interruption rollback and reopened state. **Do not accept** a green checksum, UI toast, unlocked owner, preserved row count or copied \`eligibleProven\` field as the remote-admission oracle.

### 5. Five-track transfer and operating judgment

- **E (owner; highest risk):** Specify provenance-preserving but fail-closed reauthorization for restored bindings, receipts/heads and old pending operations; distinguish historical source evidence, current local write eligibility and future authenticated remote admission. Do not assert an exploit from a not-yet-implemented Sync publisher.
- **A (dependency):** Supply exact browser storage/Service Worker lifecycle and compiled-JS serialization evidence. IndexedDB survival and cached shell readiness do not supply server authority.
- **C (independent validator):** Own RB01–RB16 product-runtime and cross-device falsification; compare negative controls and source/destination semantic oracles, not just equal store counts. Engineering owns implementation/test changes in LogMate.
- **B (consumer; Design Studio Stage 3 PRACTICE):** Separate “restored locally”, “owner unlocked”, “pending operations awaiting review”, “server accepted” and “fully reconciled” in status/recovery UX. No visual/interaction sign-off without runtime and human/assistive-technology evidence.
- **D (consumer; Marketing handoff):** No public claim of seamless cross-device Sync, automatic replay, secure portable recovery or EFB-ready installation from preserved local bindings. Marketing's canonical claim gate remains independent.

**MINTTAP DECISION — proposed, not approved implementation:** keep immutable original operation identity and historical provenance; require a fresh, explicit destination-side remote-admission decision rather than treating a restored source \`eligibleProven\` marker as authorization. Preserve the owner lock/unbound/unverified guards. Do not automatically delete all source bindings, rewrite operation IDs, or assert that every historical receipt is false; those choices would undermine retry/idempotency and evidence custody. This is a test/contract handoff, not permission to change LogMate.

**OPEN:** actual populated receipt/head fixtures; real Dart collision/rollback outcomes; any future Manual Sync publisher's admission logic; browser and managed-EFB execution; post-restore authenticated server receipts/convergence; W-012/013/014 acceptance. **DEPENDENCY:** LogMate Sync implementation and Software Engineering D005 validate-before-publish; Design Studio W121 runtime gate; Marketing release-claim review. **CHANGE WATCH:** binding schema, restore reset semantics, server contract, Dart/Sembast versions, Safari/WebKit and managed-device policy. **Checkpoint:** a distinct, source-grounded latent-admission boundary was resolved without another synthetic PASS label. The next adjacent question—whether receipts/heads have an actual remote consumer—was checked in the same source file and found unimplemented, so a product exploit claim would be unjustified. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**

---

## 2026-10-28 Applied Stage 8 — executed Dart VM vs compiled-Web JSON semantic divergence (JA36–JA51)

**Question / scope.** The prior 13/13 Node JSON model and genuine v1 JavaScript digest did not establish how the **actual Dart language runtimes** decode duplicate JSON object members or numbers. This continuation closes that narrower generic runtime question without claiming a LogMate LBK restore, file picker, Safari, managed iPad or production PASS. Product authority remains read-only LogMate `main@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f`, [WholeLedgerBackup codec](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/repository/logbook/whole_ledger_backup.dart) (blob `711f784534bc686a4d8edd6617ac4d1ac362e0a7`) and [Sembast restore](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/repository/logbook/sembast_logbook_repository.dart#L445-L590). The codec performs `jsonDecode` before root/manifest/store inspection, recursively sorts keys with `String.compareTo`, and hashes its *re-encoded unsigned semantic object*; the restore verifies that digest before its local transaction. These are **SOURCE observations**, not a finding of a shipped malicious-input path. User-facing W-013 file ingress and Production Manual Sync remain unimplemented.

**Standards / SOURCE (checked 2026-10-28).** [RFC 8259 §4](https://www.rfc-editor.org/rfc/rfc8259#section-4) says JSON member names SHOULD be unique and parser behavior otherwise varies. [RFC 7493 §2.3](https://www.rfc-editor.org/rfc/rfc7493#section-2.3) requires uniqueness after escape processing for I-JSON; [§2.2](https://www.rfc-editor.org/rfc/rfc7493#section-2.2) warns that integers beyond ±(2^53−1) cannot be assumed exact across receivers. [Dart number representation](https://dart.dev/resources/language/number-representation) explicitly distinguishes native 64-bit `int` from web double-based integer precision. [Dart String.compareTo](https://api.dart.dev/dart-core/String/compareTo.html) orders UTF-16 code units; [RFC 8785 §3.2.3](https://www.rfc-editor.org/rfc/rfc8785#section-3.2.3) also sorts canonical JSON property names by UTF-16, **but** requires I-JSON, exact serialization and other rules. The LogMate recursive sort is **not** thereby a JCS implementation. Separately, the approved LogMate Sync contract orders tied **Operation IDs by UTF-8 bytes**; do not reuse the JSON-key sort comparator for Sync IDs.

**Actual executable evidence / VALIDATION.** The standalone public [Dart probe](handoffs/lbk_dart_json_runtime_probe.dart) and [independent expected-observation oracle](handoffs/lbk_dart_json_runtime_oracle.mjs) ran through [GitHub Actions 40537232811](https://github.com/yhappcom/web-manager/actions/runs/40537232811), job `122305828465`, on hosted Ubuntu 24.04 with **Dart SDK 3.12.0**, `dart compile js -O2`, and Node **22.16.0** executing the compiled JavaScript. Exact tested repository ref: `54a59914564aa2b373dad35935dee74fc9e71725`. **17/17 independent bounded assertions PASS**; all actual probe outputs are in job logs. The tests intentionally verify divergences, not universal equality:

| Input / observation | Dart VM 3.12.0 | dart2js JS executed in Node 22.16.0 | Meaning |
| --- | --- | --- | --- |
| Duplicate `owner` member | last `new` value | last `new` value | Parsed Map has lost source-member multiplicity in both |
| Escaped duplicate `owner` + `\\u006fwner` | last `new` value | last `new` value | Escaped-name collision also collapses to same visible key |
| `jsonDecode` reviver visits for either duplicate | **2** visits | **1** visit | **New concrete cross-target divergence**: reviver callback count is NOT a portable duplicate-key rejection oracle |
| JSON integer `9007199254740993` | preserves `9007199254740993` | becomes `9007199254740992` | Re-encoding can alter semantic JSON/digest across targets beyond safe integer range |
| `(1.0).runtimeType` | `double` | `int` | Runtime type tests cannot be assumed portable for numeric shape |
| UTF-16 key ordering vs UTF-8 byte ordering of U+E000/U+10000 | UTF-16 places supplementary first; UTF-8 puts BMP first | same distinction | Two different protocol comparators, each correct for its own contract |
| Nested `key` in distinct objects; `-0.0` JSON encoding | distinct nested keys; `-0.0` | same in this probe | Bounded positives, not full serializer parity |

**Failure-first correction / CONTRADICTION.** Initial [run 40537003779](https://github.com/yhappcom/web-manager/actions/runs/40537003779) failed at a formatting-only gate, **before either runtime probe**. [Run 40537097388](https://github.com/yhappcom/web-manager/actions/runs/40537097388) executed both runtimes but its original oracle incorrectly expected one VM reviver visit; the observed **2 vs 1** was a genuine falsification of that assumption, not a LogMate product failure. The oracle was corrected to *independently require* VM=2 and JS=1 for both ordinary and escaped duplicates, plus a cross-target disagreement assertion. The successful final run checks a fixed **17/17** signature. The intermediate workflow outcomes are not silently relabeled as product FAIL/PASS.

**SYNTHESIS / threat and failure boundary.** A valid-looking parsed JSON object and matching re-encoded unkeyed digest are not proof of original raw-member uniqueness, byte identity, writer authenticity, or portable numeric semantics. A naïve `jsonDecode(reviver: ...)` duplicate detector could work in the observed VM case and miss the same duplicate in compiled Web. If rejecting duplicate members becomes an admission rule, it needs a **pre-map-collapse** parser/tokenizer or independently validated streaming implementation that handles escapes and object scope, with byte/row/depth/work budgets and fail-closed errors. This is a **proposed future W-012/W-013 control**, not authorization to replace the existing LBK v1/v2 checksum, silently rewrite historical files, or assert an exploit. Real 2026 UTC epoch microseconds are below 2^53; the synthetic 2^53+1 case is a **precision boundary**, not evidence that normal current LogMate timestamps are already damaged. Enumerate actual numeric fields and historical maxima before deciding wire changes.

**Engineering acceptance handoff / VALIDATION OPEN (JA36–JA51).** On an authorized exact LogMate checkout, first run the genuine v1/v2 `WholeLedgerBackup.decode` + checksum + Sembast restore on native Dart, then the *exact compiled Flutter Web release* and installed Safari; use independent source-byte, decoded-member, 37-store, original-owner, revision/outbox/Sync-hold and rollback oracles. Include duplicate root/manifest/nested members, escaped-equivalent names, same key in distinct object scopes, safe-boundary ±(2^53−1)/2^53/(2^53+1), valid historical timestamps, negative zero, decimal/exponent, malformed Unicode, over-budget file/depth/row counts, checksum mismatch, wrong owner and interrupted restore. A parse failure, checksum rejection, data mutation, memory exhaustion and UI failure must be recorded as distinct outcomes. Ensure the original staging DB/backup remains recoverable after a rejection. Explicitly preserve backward compatibility unless an owner-approved versioned format migration with fixtures proves otherwise. Node-executed dart2js **is not Safari**; Flutter Wasm (if targeted), actual app build, file API, browser quota/eviction and managed EFB remain separate OPEN targets.

**Five-track integration / DEPENDENCY / TRANSFER VALIDATION.** **E** retains highest-risk ownership of file admission, format authority, authenticity vs integrity, recovery and release HOLD. **A** owns native/Web JSON, UTF-16/UTF-8, secure-context/storage and browser execution prerequisites. **C** now has real cross-runtime executable evidence and owns independent product-runtime failure oracles, not a generic PASS promotion. **B** consumes Design Studio Web W121 Stage 3 PRACTICE for truthful “backup rejected / local data unchanged / safe recovery” states and accessibility/human testing. **D** consumes Marketing D8–D10 claim HOLD: no “guaranteed cross-platform backup compatibility”, “seamless EFB restore” or “automatic device Sync” from this synthetic probe. Software Engineering [VALIDATION_STANDARD](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) owns exact product implementation/oracle execution. No LogMate/Design Studio/Marketing/Engineering repository writes.

**Gate:** Applied Stage 8 **ACTIVE**; generic cross-runtime Dart VM/dart2js JSON probe **EXECUTED 17/17 PASS** at its narrow boundary; actual LogMate v1/v2 restore, Safari Home Screen, physical/managed EFB and Production validation **OPEN**; PWA release **HOLD**. **Adjacent-question check:** source-key multiplicity, escaped names, reviver portability, numeric precision, comparator contract, failure-first CI and five-track consequences were all addressed in this integrated bundle. The next decisive step needs an authorized exact-product W-012→W-013→W-014 run, not another independent Node-only model.


## 2026-10-28 Stage 8 — Safari 26 installability, managed Web Clip, and storage-custody distinctions [SOURCE / SYNTHESIS / CHANGE WATCH]

**Problem/history.** A company-managed EFB iPad may forbid ordinary App Store installation. This makes a Home Screen PWA or MDM Web Clip a possible distribution surface, but it does **not** imply offline availability, persistent flight data, user-controlled installation, background sync, or cross-device connectivity. Older checklists that require a manifest/service worker before a Safari site can become a Home Screen web app are now outdated for current iOS/iPadOS 26. Separate **entry point**, **execution context**, **offline assets**, **durable user state**, **backup**, **MDM policy** and **remote authority**.

### Primary platform evidence [SOURCE; checked 2026-10-28]

1. **Safari 26 Home Screen behavior:** [WebKit Safari 26.0 release article](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) states that on **iOS 26 and iPadOS 26**, any website added to Home Screen opens as a web app by default, with an **Open as Web App** choice; it explicitly says there are no Safari installability prerequisites. This is **Apple/WebKit platform behavior**, not the Chromium installability rubric and not evidence that a site works offline. A manifest still carries identity, icons, display/launch information; a Service Worker still materially affects offline behavior. Older iOS/iPadOS 16.4 WebKit guidance [Web Push for Home Screen apps](https://webkit.org/blog/13878/) describes earlier manifest/display-mode behavior, and is historical for this specific installability question.
2. **Managed Web Clip exists as an MDM configuration:** [Apple deployment Web Clips payload](https://support.apple.com/en-ca/guide/deployment/depbc7c7808/web) and [DeviceManagement WebClip schema](https://developer.apple.com/documentation/devicemanagement/WebClip) specify the `com.apple.webClip.managed` profile, URL/label, `FullScreen`, removability and manifest-scope controls. This is a **managed configuration profile**, not an App Store app install and not automatically identical to a user-created Home Screen PWA. [HomeScreenLayout IconItem](https://developer.apple.com/documentation/devicemanagement/homescreenlayout/iconitem) warns that placing a WebClip in the layout does not create it; the WebClip payload must create it. An operator's specific MDM enrollment, restrictions and approval still determine deployment feasibility.
3. **Safari-to-installed-app storage separation:** [WebKit Safari 17.2 web app cookies](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/) states that when a Home Screen web app is created, **cookies** can be copied to preserve sign-in; **no other local storage** is copied, and subsequent website data is not shared. Therefore a flight log written into Safari IndexedDB must **not** be assumed present in the Home Screen web app. An initial import or verified backup restore may be required. Cookie copy is not permission to disclose historical remote receipts or bypass current server Owner.
4. **Quota/eviction remain failure domains:** [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) says standalone web apps have the same origin/overall quota classes as browser apps and documents origin-level eviction under pressure/quota/inactivity. [WebKit ITP storage policy](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/) explains the seven-day Safari-interaction rule and its different Home Screen app usage counter; it does **not** promise perpetual retention. Neither `navigator.storage.persist()`, an installed icon nor a successful IndexedDB transaction is a physical backup.
5. **Push is not unattended Sync:** [WebKit iOS/iPadOS Web Push](https://webkit.org/blog/13878/) supports Home Screen web app push with user permission and Service Workers on supported versions; [WebKit Declarative Web Push](https://webkit.org/blog/16535/) describes an alternative notification delivery path. These are notification capabilities, **not** a guarantee that arbitrary Sync jobs execute on a company-managed iPad when closed/offline, nor that Wi-Fi/hotspot or direct phone-to-iPad connectivity is allowed.

### Cross-track acceptance matrix [SYNTHESIS / DEPENDENCY]

| Question | Evidence available now | What remains OPEN on company EFB |
| --- | --- | --- |
| Can an icon be provisioned without App Store? | Apple MDM WebClip profile and Safari Home Screen paths exist | Airline MDM restriction, WebClip profile acceptance, `FullScreen` mode, URL filtering and device/OS version |
| Does tapping icon load offline? | Service Worker/Cache API can support offline assets in principle | Exact served LogMate build, first-online bootstrap, service-worker control/update, cold launch in airplane mode after process termination |
| Does existing Safari data migrate into installed PWA? | WebKit says only cookies copied at creation; not IndexedDB | Actual app data import/restore, owner binding, 37-store counts and negative duplicate/stale data cases |
| Can user records persist indefinitely? | WebKit quota/eviction policy explicitly has failure conditions | Device storage pressure, long inactivity, profile removal, app deletion, OS update, MDM wipe and verified export/restore |
| Can it sync automatically with phone? | Push and notification support are separate APIs | Network topology, EFB policy, foreground/background lifecycle, Auth/Owner, data transfer, consent and Manual Sync product runtime |
| Is it safe to claim EFB PWA readiness? | No physical company-device test or product restore evidence | W-012→W-014 exact LogMate build + managed-device/airplane-mode validation + human recovery UX |

### Operational judgment and transfer [MINTTAP DIRECTION / VALIDATION OPEN]

- **E owns** managed WebClip deployment, HTTPS/Service Worker release/update controls, storage/backup custody, Auth/Owner authority and incident recovery. A policy-approved WebClip URL is only an entry point. A successful profile install is **not** a storage durability or release gate.
- **A supplies** Safari 26 vs earlier Safari/Chromium installation mechanics, cookie-only initial copy, Service Worker and offline lifecycle. Track C must run separate **Safari browser tab**, **user-created Home Screen app**, and **MDM-provisioned full-screen WebClip** tests; they may not share a storage or session oracle by assumption.
- **B consumes** truthful states for “first install needs restore”, “saved locally”, “not backed up”, “offline ready”, “pending Manual Sync”, “re-authentication required” and “data cannot be recovered”. Design Studio W121 remains Stage 3 PRACTICE, not tested UX.
- **D consumes** distinct install-icon, successful cold offline launch, local data restored, receipt accepted, cursor applied and backup verified metrics. Marketing D8 managed-EFB/automatic-Sync claim HOLD remains. Do not use “installable” as a proxy for “offline-safe”.
- **Software Engineering owns** actual LogMate v1/v2 LBK, 37-store atomic Apply/Cursor, Flutter Web/Safari compatibility and device tests. No peer repository changes.

**Concrete EFB test order:** (1) inventory airline iPadOS version/MDM/WebClip/Shared-iPad policy; (2) verify HTTPS and actual service-worker scope/manifest/route; (3) compare Safari and Home Screen isolated storage after installation; (4) restore a known LBK with independent counts/digest; (5) airplane-mode cold launch after killing app and reboot; (6) inject storage pressure, app update, stale Auth, owner transfer, incomplete restore and profile removal with verified recovery; (7) test only policy-approved foreground Manual Sync, separately from any background hypothesis. Require original data and export custody to remain available when any test fails.

**Evidence limit:** All points above are primary Apple/WebKit documentation and a test design, **not a physical managed EFB execution**. Exact OS/MDM/Safari build and installed LogMate PWA remain UNKNOWN. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**
