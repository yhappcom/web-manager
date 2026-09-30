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
