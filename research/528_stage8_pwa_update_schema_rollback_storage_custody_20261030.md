# 528 — Stage 8: PWA update, database capability, rollback and offline custody

Evidence checkpoint: **2026-10-30 KST**. Canonical owner **Track E — Web Architecture, Security & Operations**; Track A supplies Worker/IndexedDB platform semantics; B owns recovery task states; C owns independent runtime/device oracles; D owns public claims/discovery continuity. **SOURCE + SYNTHESIS + DEPENDENCY + TRANSFER VALIDATION + VALIDATION DESIGN + OPEN + CHANGE WATCH**. **No LogMate product modification, real device execution, or release authorization.**

## 1. The historical problem and governing distinction [SYNTHESIS]

AppCache bound an application to a coarse declarative cache with confusing update and failure behavior; Service Workers introduced programmable fetch interception and explicit install/activate lifecycles, but **programmability is not an atomic deployment of app shell + mutable ledger**. A web application can have a verified shell, an old in-memory document, a newly activated controller, a local database at another capability version, and unsent offline edits simultaneously. Those are independent state machines, not one "updated" bit.

For an offline-first pilot logbook, distinguish: **(i)** Worker script installed/activated, **(ii)** verified shell assets downloaded, **(iii)** each client pinned to a consistent shell build, **(iv)** local DB capability readable and writable by that build, **(v)** owner/backup/outbox preserved, **(vi)** a user-approved, independently recoverable rollback path. A browser Worker activation does not prove any of (iii)–(vi).

Failure-first question: *Can an installed EFB PWA keep accepting local flight entries after a partial update, while a different tab or device holds an older build, the new build migrates the ledger, storage is nearly full, and network disappears?* The answer is **OPEN for actual LogMate** until exact authorized runtime evidence exists.

## 2. Normative and implementation evidence [SOURCE; reviewed 2026-10-30]

1. [W3C Service Workers living editor's draft](https://w3c.github.io/ServiceWorker/) specifies install event lifetime via `waitUntil`, waiting/activation, `skipWaiting`, and client control. A rejected install can prevent candidate installation; this does not make application data schema migration transactional with Worker activation.
2. [web.dev Service worker lifecycle](https://web.dev/articles/service-worker-lifecycle/) describes the waiting default, update checks, `skipWaiting` risks, and stale clients; Chromium-oriented guidance, **not a Safari/managed-iPad product acceptance**.
3. [MDN updateViaCache](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache) distinguishes `imports` (default), `all`, and `none` for Worker script/import update checks, **not application CacheStorage policy**. [MDN registration.update](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update) checks for a new Worker; it does not migrate IndexedDB.
4. [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) and [MDN versionchange](https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/versionchange_event): schema upgrades can be blocked by another open database connection; old clients should respond to `versionchange` by closing after safeguarding edits. This is an IndexedDB mechanism, **not proof of LogMate's Sembast-specific migration behavior**.
5. [WHATWG Storage](https://storage.spec.whatwg.org/) defines storage buckets and persistence; quota and eviction are not backup guarantees. [WebKit storage policy, 2023-08-10](https://webkit.org/blog/14403/updates-to-storage-policy/) explicitly covers Cache API, IndexedDB, Service Workers, quota pressure, eviction and persistence heuristics for Safari/standalone apps. A reported quota is a limit, not free disk; physical managed EFB policy is unknown.
6. [MDN Service Worker registration](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration) and [MDN secure-context boundary](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) distinguish registration/HTTPS from background execution promises. **CHANGE WATCH:** Safari/WebKit/iPadOS version and managed Web Clip container behavior require measured provenance.

## 3. Exact read-only LogMate evidence [SOURCE]

Read on **2026-10-30** from `yhappcom/logmate` default `main`:

- `tool/pwa_precache.dart` blob **`90a67954af618a4e18199fa92555491c56167c17`**: build generator includes `databaseCapability = LocalDatabaseCapabilityCodec.currentVersion` in the offline manifest, `appBuildId`, `fontSetId`, per-item SHA-256/size, and requires **724 WOFF2** fonts. Candidate download/inspection and `currentBuildId`/`previousBuildId`/`candidateBuildId` plus `clientBuilds` are kept in a CacheStorage control JSON.
- The Worker source template deliberately **does not call `skipWaiting()`**, does call **`clients.claim()`** after activation, and **does not delete old caches automatically**. It assigns root navigation client IDs to a build and returns **503** when an unassigned client requests an eligible same-origin resource; reserved `auth` and `__/` routes bypass its interception. Existing study 523 already owns the public-route/GET/CSP/header/catalogue risks; **do not treat this as a fresh exploit**.
- The template's `promoteInControl(control, buildId)` checks a known manifest, its verified flag and cache readiness; **this Worker-level function does not compare the local database's actual capability marker with the candidate's `databaseCapability`**. It is a *conditional cross-layer gap*, **not evidence that the Flutter repository layer lacks a migration gate**. `LocalDatabaseCapabilityCodec` blob **`f82b49da619e2fc861edf133eb9e66b195017a03`** has `currentVersion = 17`, explicit historical versions and migration-aware decoders; its existence does not prove every deployed old/new shell pair is safe.
- `ROLLBACK_TO_PREVIOUS` explicitly returns **`NOT_ROLLED_BACK`**: the comment correctly refuses to treat cache metadata or caller booleans as authority over real schema/dirty edits/outbox/auth compatibility. Thus **retaining previous cached shell ≠ supported rollback**. No automatic old-version deletion is a deliberate resilience choice, but persistent retained shell/font versions have a storage-pressure trade-off.
- `web/index.html` blob **`01be77585ac40bf11e80777177a4ab08e4885671`** uses Flutter `$FLUTTER_BASE_HREF` and an external bootstrap; a source template is not a measured served build or current client controller.
- Approved [LogMate Local-First Manual Delta Sync contract](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md) blob **`2240fc1b`**: complete local ledger on each replica, first device transfer via independent `.lbk`, **user-initiated** Manual Delta Sync, original Operation IDs/timestamps, separate Replica IDs, no silent nonempty overwrite/merge. Contract approval is **not production implementation or EFB acceptance**.

**SOURCE LIMIT:** these are file-level observations, not a comprehensive call-graph proof, deployed artifact fingerprint, current hosting response, running Safari instance, or physical managed EFB test. Other repository layers may provide additional guards; do not infer absence beyond the inspected Worker function.

## 4. Independent state machines and false-success traps [SYNTHESIS]

| Layer | Observable fact | Must not be inferred |
| --- | --- | --- |
| Worker | `install` and `activate` completed | Same JS in every open page, or durable user data |
| Shell | SHA/size verified, `candidate.ready` | DB schema compatibility, trusted response headers or clean Owner |
| Client | Build assignment recorded for client ID | Stable mapping across all tab/restoration/navigation cases |
| Database | Capability marker decoded/migrated | Backup independently retained, no unsent operation loss |
| Local editing | Flight transaction committed | Cloud receipt, applied cursor or sync success |
| Backup | `.lbk` prepared in app | Bytes independently saved/read back through iPad Files |
| Rollback | Old cache exists | Old binary can safely open migrated DB or recover unsent edits |
| Installed | Home Screen icon opens | MDM policy, storage persistence or offline restoration proved |

**CONTRADICTION check:** "No `skipWaiting`" is a good default against immediate takeover, **but** new Worker activation can still occur after old clients drain; this does not by itself prevent an older cached shell from being reopened later against a newer database. Likewise, `clients.claim()` and per-client build assignment are separate operations, and a successful Worker controller is not evidence of a compatible client document. A schema marker in a downloadable manifest is not an authorization token.

## 5. Compatibility protocol to evaluate, not prescribe as implemented [MINTTAP DIRECTION — PROVISIONAL]

Before serving a candidate as usable, the **application-owned** compatibility layer should be able to independently report `shellBuild`, `expectedDbCapability`, `actualDbCapability`, `migrationState`, `pendingLocalWrites`, `outboxCount`, `backupReadbackState`, and `ownerState`. The Worker can report its own version and cache readiness, but must not claim it has inspected the full ledger merely because it can read a CacheStorage control record.

A defensible release state machine is **DISCOVERED → CANDIDATE_VERIFIED → CLIENT_QUIESCED → DB_COMPATIBILITY_CONFIRMED → LOCAL_DATA_PROTECTED → READY_FOR_RELOAD → REOPENED_AND_CHECKED**. These are **proposed gates**; no automatic upgrade authorization is implied. A candidate that requires irreversible schema change should not promise one-click rollback to an older binary. Safe alternatives are compatible forward fixes or a separately approved restore path with explicit Owner and outbox preservation.

Where multiple tabs are possible, test IndexedDB `versionchange`/`blocked` and app-level edit transactions. **Never** close a DB connection or force a reload during an uncommitted edit without a durable save/explicit recovery state. A blocked upgrade should show a truthful wait/retry state, not a false successful update.

## 6. Update and failure taxonomy [SYNTHESIS / VALIDATION DESIGN]

1. **Offline while update check begins:** old verified build remains runnable; no "updated" toast.
2. **Install interrupted during 724-font/package download:** reject candidate; last runnable version remains, subject to quota/eviction.
3. **Candidate shell verified but DB upgrade rejects:** do not equate Worker READY with ledger READY.
4. **Old tab holds DB connection:** schema `versionchange`/blocked path preserves pending edit and eventually resolves without forced data loss.
5. **Client reload after new activation:** test page JS version, controller version and per-client assigned build; detect 503 and allow non-destructive retry.
6. **Two tabs with old/new build:** confirm no mixed main.dart.js/CanvasKit/font shell and no schema-incompatible writes.
7. **Cache control JSON corrupted or origin-writable:** fail closed and retain original ledger; do not trust cache catalogue as sole security authority (see 523 §§25–26).
8. **Stored response header mutation:** body SHA alone does not attest CSP/MIME headers; 523 owns this threat and its synthetic evidence.
9. **Quota exhausted:** app must not sacrifice IndexedDB user records to finish optional font cache; preserve recoverability and report capacity failure.
10. **Storage eviction:** neither retained caches nor persistence heuristics replace `.lbk` backup.
11. **Old shell rollback after schema v17 migration:** **not authorized** merely because `previousBuildId` exists; demonstrate actual compatibility or refuse.
12. **Interrupted restore/migration:** no half-committed ledger or "success" status; source backup stays untouched.
13. **UID revoked vs network unreachable:** no automatic destructive wipe of established offline records; distinguish server authority from local availability.
14. **Home Screen vs Safari tab vs MDM Web Clip:** treat as separate containers until observed, even for the same URL.
15. **Cross-origin move and update together:** avoid combining migrations; isolate one destructive dimension at a time (527).
16. **Server rollback to old Worker with new DB:** redeploying old static assets does not reverse local schema migration.
17. **Old and new devices sync later:** original Operation IDs and cursor lineage preserved; no implicit sync on app resume.
18. **Auth callback during Worker upgrade:** `auth` bypass remains functional and does not leak `oobCode` into caches, logs or analytics; 523 owns detailed auth threat.

## 7. Release / rollback gates for an authorized Engineering exercise [VALIDATION — NOT RUN]

**R0 — Provenance:** pin product commit, generated Worker/manifest/build hashes, served HTTPS headers, browser/iPadOS build, install container, MDM policy and source database version. No real pilot data in CI.

**R1 — Independent source custody:** on a disposable full 37-store ledger with pending Operations and Owner, produce `.lbk`, save outside the browser storage bucket, independently read bytes back, validate format/digest and restore into an empty same-UID test destination. A Blob URL is not enough.

**R2 — Baseline:** old installed build starts offline, records a synthetic edit and reopens it; capture Worker/client/DB/Replica/Outbox fingerprints without secrets.

**R3 — Candidate:** deploy compatible and deliberately incompatible synthetic versions, including failed download, corrupt cache/header, quota, stale tab, blocked DB and mixed-client tests. A fail-closed negative control is expected PASS **only for the specific safety oracle**.

**R4 — Forward update:** quiesce safely, validate DB migration, confirm 37-store semantics, original Operation IDs, baseline, tombstones, aggregate consistency, and offline restart. Never infer Manual Sync from this.

**R5 — Rollback decision:** distinguish code rollback with unchanged DB from schema rollback. Test refusal of unsupported downgrade; a real rollback claim needs independent compatibility proof and non-destructive state recovery.

**R6 — Device/operations:** repeat on Chrome, iPadOS Safari tab, installed Home Screen PWA and permitted managed EFB/Web Clip separately; include Files/MDM restrictions, VoiceOver/keyboard, no-network start, app termination and storage pressure. Retain logs with redacted UID/flight data and no Auth Action query tokens.

No gate here authorizes changes to LogMate, deployed domains, product sync policy or existing caches.

## 8. Independent acceptance matrix U01–U26 [VALIDATION DEFINED, NOT RUN]

| ID | Evidence oracle |
| --- | --- |
| U01 | Pin exact source/compiled Worker/manifest/build and served HTTPS response; compare hash and install scope |
| U02 | Old installed shell runs offline and can commit/reopen synthetic Flight before update |
| U03 | Worker `waiting` default and no `skipWaiting` verified on exact compiled build |
| U04 | `clients.claim` and `controllerchange` behavior measured with preexisting and new tabs |
| U05 | Interrupted candidate install leaves prior runnable shell and source DB unchanged |
| U06 | Shell/724-font manifest verification distinguishes body integrity from header trust |
| U07 | Candidate manifest capability and actual DB marker are independently measured |
| U08 | Unsupported old/new DB pairing refuses unsafe write/activation claim |
| U09 | Sembast migration from approved historical marker to current version preserves 37-store semantics |
| U10 | IndexedDB `versionchange` and `blocked` with two tabs preserve durable pending edits |
| U11 | Old tab/new controller/mixed shell requests never silently mix build assets |
| U12 | Client ID assignment survives reload/restoration or shows truthful non-destructive recovery from 503 |
| U13 | Corrupt control JSON/manifest cache does not grant shell promotion or destroy DB |
| U14 | Origin-writable cached headers cannot silently remove required CSP/MIME policy |
| U15 | QuotaExceeded during shell/font caching leaves last verified runnable shell and DB intact |
| U16 | Cache retention growth measured across multiple updates; eviction/cleanup policy requires separate approval |
| U17 | Storage pressure/eviction and `persist()` result recorded without claiming guaranteed durability |
| U18 | Unsupported rollback returns safe refusal with DB and Outbox unchanged |
| U19 | Compatible forward fix works after incompatible older code cannot safely reopen migrated DB |
| U20 | `.lbk` Files independent save/readback and empty same-UID 37-store restore verified |
| U21 | Wrong UID/nonempty destination/corrupt backup fails closed without mutation |
| U22 | Crash/power loss mid-migration or restore never yields false success or cursor advance |
| U23 | Offline relaunch after update retains original Operation IDs, tombstones, Replica and pending Outbox |
| U24 | Auth Action routes and `oobCode` remain outside Worker caches/telemetry during upgrade |
| U25 | Safari tab, installed Home Screen, and managed Web Clip tested separately with device/MDM provenance |
| U26 | UX/accessibility, deletion/support links, privacy-safe measurement and truthful release claims independently checked |

**Evidence rules:** PASS requires exact run URL/commit/build/device + expected and observed assertion, including negative controls. `NOT RUN`, `NON-EXECUTION`, `FAIL`, `PASS SYNTHETIC`, and `PASS PRODUCT` must never be collapsed.

## 9. Cross-track ownership, contradiction and transfer [DEPENDENCY / TRANSFER VALIDATION]

| Track | Relative gate | Owned contribution |
| --- | --- | --- |
| **E (lead)** | Stage 8 high-risk release bottleneck; source mature, product evidence absent | Update/schema/backup trust, incident/rollback policy, release HOLD |
| **A** | Browser platform prerequisite; spec evidence available, WebKit runtime open | Worker lifecycle, client control, cache/IDB versionchange and browser-specific CHANGE WATCH |
| **B** | Recovery task truth before visual execution | Distinguish Downloading/Ready to reload/DB review/Backup saved/Restored/Sync complete; Design Studio W121 owns visual execution |
| **C** | Greatest validation maturity gap | Exact compiled multi-tab/low-quota/physical iPad/VoiceOver test design and independent adjudication |
| **D** | External-claim pressure; Marketing D8/D9 HOLD | No "seamless offline update" or "automatic sync" until evidence; public/support/deletion route continuity, privacy-minimized update analytics |

**RELATED DOMAIN CHECK:** Design Studio `progress/WEB_STATUS.md` Stage 3 PRACTICE/W121 execution gate (no physical/human PASS); Marketing `STATUS.md` 2026-10-29 D8 product claims HOLD/D9 deferred; approved LogMate Manual Delta Sync contract; Web studies 523–527. Other specialists' source material consumed **read-only**. Engineering implementation/validation owner must independently verify schema compatibility; Web Manager does not alter product code.

## 10. Decision register and next evidence [MINTTAP DIRECTION / OPEN / CHANGE WATCH]

- **MINTTAP DIRECTION (not product approval):** keep verified-shell state separate from DB-ready, independent-backup and cloud-sync states; preserve source ledger and old launch path during update/migration; refuse unsafe downgrade. Maintain user-initiated sync and `.lbk` first transfer.
- **SOURCE-confirmed:** current Worker has versioned shell/control cache, no `skipWaiting`, `clients.claim`, no automatic cache deletion, and fail-closed rollback; current local capability codec v17.
- **OPEN:** actual generated NORMAL build behavior; application-level DB compatibility gates; actual iPadOS/MDM storage, file UX and schema upgrade behavior; 37-store restore and post-update sync; deployed CSP/Worker headers; physical quota/eviction and human UX. **No new runtime test in this study.**
- **CHANGE WATCH:** W3C Service Worker and IndexedDB evolving drafts, Chrome update behavior, WebKit/iPadOS storage/installed Web Clip implementation, Firebase hosting/auth changes and managed device policy. Revalidate on actual supported release matrix.
- **Next high-information-gain action:** Engineering-approved exact-source build with paired old/new local DB fixtures and independent U01–U26 adjudication, prioritizing U07–U12/U15/U18–U23. If access unavailable, keep production gate OPEN rather than generating more synthetic green checks.

**Gate: Stage 8 ACTIVE · Source-level update/schema boundary mapped · Production validation OPEN · PWA release HOLD.**
---

## 11. Cross-layer correction: Sembast capability v17 is NOT IndexedDB's physical database version [SOURCE / CONTRADICTION / 2026-10-30]

This continuation closes a material ambiguity in §§4–8. **The product's \`LocalDatabaseCapabilityCodec.currentVersion = 17\` is a *logical record in a Sembast store*, not evidence that the underlying browser's IndexedDB database has physical version 17.** An IndexedDB \`versionchange\`/ \`blocked\` example is an important *separate* platform failure mode, but it must **not** be used as the presumed mechanism for LogMate's v16→v17 application migration.

**Exact product provenance:** [LogMate main \`9cc0cd432a317d5dfebbe90e318fb219e53e024a\`](https://github.com/yhappcom/logmate/commit/9cc0cd432a317d5dfebbe90e318fb219e53e024a), declared \`1.0.0+1\` in \`pubspec.yaml\` (not asserted to be the deployed build), inspected 2026-10-30. Source:
- [\`local_database_capability_codec.dart\`](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/local_database_capability_codec.dart), blob \`f82b49da619e2fc861edf133eb9e66b195017a03\`: \`currentVersion = 17\`, historical migration decoders including exact v16 producer vector. This codec reads/writes a persisted capability marker, not the browser's \`IDBDatabase.version\`.
- [\`sembast_logbook_repository.dart\`](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/sembast_logbook_repository.dart), blob \`021d9001ae1240a824c5df570fb679597edc3875\`, lines ~320–395, ~4211–4660, ~4820–4840: \`open(Database)\` calls \`_prepareDatabase()\`; the entire preparation is enclosed in \`_database.transaction((transaction) async { ... })\`. It reads \`logmate_schema_v1\` / \`repository\` marker; explicitly branches through historical versions; v16 branch calls \`decodeV16ForMigration\`, validates canonical/Owner/Outbox/37-store-adjacent structures, requires newly introduced Sync stores empty, classifies legacy outbound evidence, invokes an optional **test-only** failure seam, then publishes current capability in that same transaction. Current v17 branch validates existing stores. An unknown future marker reaches \`_capabilityCodec.decode(marker)\`, which requires current version and therefore rejects unsupported future representation rather than silently downgrading.
- The repository exposes \`openForMigrationTesting\` with \`SembastMigrationFailurePoint.beforeCapabilityPublication\`; it is an injection seam, **not** a result proving rollback on WebKit. \`_readCapability\` decodes the persisted marker on operations. The explicit application-level capability check is stronger source evidence than the earlier Worker-only analysis, but it does not prove the cross-layer release protocol or live device durability.
- [\`pubspec.yaml\`](https://github.com/yhappcom/logmate/blob/main/pubspec.yaml) declares \`sembast ^3.8.11\` and \`sembast_web ^2.4.6\`. The [sembast_web 2.4.6 package author documentation](https://pub.dev/packages/sembast_web/versions/2.4.6) states it is IndexedDB-backed, loads data into memory, uses \`BroadcastChannel\` for open-tab notification, provides cross-tab-safe transactions and **may rerun a transaction after concurrent changes**; it specifically requires transaction functions to be idempotent. That is a critical *implementation-specific* constraint, not a W3C IndexedDB guarantee.

**Precise correction to §6 item 4 and U10:** distinguish (a) *logical Sembast capability migration and concurrent tab retries/observations* from (b) *physical IndexedDB \`versionchange\`/ \`blocked\` when a browser database's object-store schema is upgraded*. The latter remains a valid independent test only if the exact pinned Sembast Web/idb_shim implementation or a future product change actually triggers an IDB schema upgrade. No direct source/runtime evidence was obtained that LogMate's v16→v17 logical migration itself invokes a physical IDB upgrade.

**Primary standard boundary:** [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) defines exclusive \`versionchange\` transactions for physical object-store/index changes and the \`blocked\`/connection-close flow. It does not define LogMate's Sembast capability marker. The [Software Engineering Studio D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) demonstrates that schema publication and backward binary compatibility are separate even when a migration is transactional; its SQLite fixture is **transfer reasoning**, not a LogMate/WebKit execution result.

## 12. Actual v16→v17 custody and remaining concurrency questions [SOURCE / SYNTHESIS / OPEN]

1. **Transactional boundary:** source-level v16→v17 validation, classification and marker publication occur inside the repository's one Sembast transaction. This **narrows** the previous "missing migration guard" concern: do not claim the product has no application-level migration gate. It does **not** establish that every Sembast Web transaction commits durably under device kill/quota pressure, or that an old binary can reopen v17.
2. **Version vector:** \`decodeV16ForMigration\` requires the exact pre-F1 codec vector; \`decode\` expects v17. Historical v13 Draft dual-codec and v14/v15 migration branches exist. This is meaningful source maturity, not a proof for every possible old binary, legacy data corpus, or production version pairing.
3. **Sync provenance:** the v16 migration requires new Sync stores empty, then classifies legacy outbound evidence rather than treating old audit timestamps as verified Manual Delta operation time. That protects against inventing remote-sync authority from pre-F1 data; verify exact pending Outbox and recovery-hold state after retry and restore.
4. **37-store snapshot boundary:** \`_lbkStoreRegistry\` lists 30 base stores; \`_syncLbkStoreRegistry\` adds seven Sync stores, for **37 named stores**. \`exportWholeLedgerBackup\` checks READY capability, matching unlocked UID and non-deletion state; returns an encoded container without performing Files I/O. \`restoreWholeLedgerBackup\` checks empty destination, runs inside a transaction, preserves destination Replica and resets/restages source Sync authority. This source evidence narrows earlier generic backup uncertainty but **does not** complete the user-facing file handoff, independent byte readback or managed EFB acceptance (524).
5. **Cross-tab retry:** because Sembast Web documents possible transaction re-execution after concurrent writes, assess every migration callback's idempotence and side effects (including random Replica generation, recovery-hold keys, classification, error/fault callbacks). Do not assert a defect without an observed failing interleaving. A transaction callback that can retry must not send network receipts, issue non-repeatable external actions or declare user-visible completion before commit.
6. **Mixed-client compatibility:** an old Web client may already hold in-memory state when a new client publishes v17. Its next transaction/reload/repository open must be evaluated independently. A fail-closed v17 decoder in the new binary does **not** prove old-client refusal or preserved unsaved edits.
7. **Worker isolation:** \`promoteInControl\` in [\`tool/pwa_precache.dart\`](https://github.com/yhappcom/logmate/blob/main/tool/pwa_precache.dart), blob \`90a67954af618a4e18199fa92555491c56167c17\`, still checks shell manifest/cache but not a live Sembast marker. The correct interpretation is **two distinct gates already exist in different layers, but their sequencing and exact served-build coordination are unverified**. Do not propose duplicating DB logic in a Service Worker merely to make its status say READY.
8. **Storage budget:** generator explicitly requires **724 WOFF2 files** plus shell, notices and retained versions; their **actual compressed byte totals and multi-generation growth were not measured**. [MDN \`StorageManager.estimate()\`](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate) returns approximations, not reserved free bytes. [WebKit's 2023-08-10 storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) describes quota/eviction and installed Web App distinctions; neither guarantees a managed iPad will retain the ledger under disk pressure. Measure before proposing automatic cache pruning, and never clear a user's origin storage to repair a font cache.

**Contradiction resolved:** earlier §5's phrase "application-owned compatibility layer should be able to report actualDbCapability" is still valid as a *release-level observability requirement*, but the product already has a Sembast repository capability codec and migration guard. The missing evidence is **end-to-end cross-layer coordination**, not absence of a codec. Earlier §6's IndexedDB blocked scenario is conditional, not established for the logical v17 transition.

## 13. Refined release oracles: separate Sembast retry, physical IDB upgrade and Files durability [VALIDATION DESIGN — NOT RUN]

| ID | Test input / fault | Independent success oracle | Scope boundary |
| --- | --- | --- | --- |
| X01 | Exact compiled Web build with v16 disposable ledger | One v17 marker after reopen, source records and 37-store semantics preserved | No CI/device execution yet |
| X02 | v16 source with nonempty newly introduced Sync store | Fail closed without partial v17 publication or lost source data | Test deliberate invalid input |
| X03 | Inject \`beforeCapabilityPublication\` error | Reopen old marker and original records after failed transaction | Native/unit and Safari separately |
| X04 | Concurrent two-tab v16→v17 opens | Exactly one durable logical migration, no duplicated recovery holds, no lost edits | Sembast Web documented retry behavior |
| X05 | Forced transaction retry with generated Replica ID | Exactly one committed stable Replica identity and no externally visible precommit success | Retry side effects must be checked |
| X06 | Old binary client kept open during new binary migration | Refuse unsafe old write, preserve pending edits, show actionable recovery | Separate from IDB physical blocked |
| X07 | Explicit *physical* IndexedDB schema upgrade, if implementation requires it | \`versionchange\` / \`blocked\` handled without edit loss | Not presumed part of v16→v17 |
| X08 | Worker candidate promoted while DB open is incompatible | Shell ready ≠ ledger ready; app does not accept unsafe edits | Check Worker/app sequencing |
| X09 | 724-font candidate fails mid-download/quota | Last verified shell and source ledger survive; no false update success | Real byte/quota measurement needed |
| X10 | 3 successive builds retained, plus large ledger | Observe actual CacheStorage/IDB usage and failure mode; no eviction assumptions | Safari tab, installed, MDM distinct |
| X11 | Export READY v17 ledger, independent Files readback, restore to empty same UID | 37-store state, original Op IDs, new Replica, safe Cursor/hold state | File I/O not proven by repository code |
| X12 | Backup corrupt/wrong UID/nonempty target, or kill during restore | Explicit rejection, source untouched, no partial destination publication | Physical crash/MDM still OPEN |
| X13 | Old shell against migrated v17 ledger | Safe refusal or independently proven compatible read/write, never implied rollback | Binary matrix required |
| X14 | 2 devices diverge offline then user-triggered Manual Sync | Original Op IDs/UID, receipt, applied cursor and full ledger converge only after actual apply | Contract approved; implementation not proven |
| X15 | Managed EFB blocks Files share/export | Truthful user recovery, no "backup saved" or "sync complete" false claim | Real airline MDM policy unknown |
| X16 | Interrupted update/recovery with VoiceOver and large text | Focus, announced progress/error, retained user edit and recoverable task path | Design Studio W121/Track C evidence OPEN |

**Adjudication:** source audit is **SOURCE**; a deterministic test of pure migration logic is **UNIT/REPOSITORY VALIDATION**; a Chromium synthetic test is **PASS SYNTHETIC**; a real compiled LogMate test is **PASS PRODUCT** only for its exact fixture/build; a physical managed iPad result is **DEVICE/MDM** only for that enrolled policy. Never merge those classes. The critical next exercise is **X01–X06 + X08 + X11–X13** with pinned old/new compiled binaries and a disposable 37-store fixture; then X09–X10/X15–X16 on physical iPad.

## 14. Five-track balance, peer transfer and checkpoint [TRANSFER VALIDATION / OPEN]

- **E (lead):** corrected source-level risk classification; v16→v17 logical migration has a transaction and fail-closed version decode, but cross-version release, external backup custody, quota and downgrade remain OPEN.
- **A (dependency):** owns distinction between IndexedDB *physical* \`versionchange\` and Sembast *logical* capability; documents Worker/client lifecycle and Sembast Web multi-tab retry behavior. Do not duplicate E's release decision.
- **B:** specifies truthful states for "updating", "waiting for another tab", "data needs review", "file saved externally" and "sync complete"; consumes Design Studio [W121 Stage 3 PRACTICE](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) without claiming tested UI.
- **C:** independently owns exact source/compiled/physical test oracles X01–X16, including failure injection and accessibility. The [Engineering Data D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) and [Quality Q006](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/QUALITY_STATUS.md) evidence supplies transfer principles, not product PASS.
- **D:** no user-facing promise of "automatic backup", "safe rollback", "seamless updates" or "automatic device sync"; [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) retains claim HOLD. Public origin/canonical changes remain separately gated under 527.

**Checkpoint / decision:** Stage 8 **ACTIVE**; one misleading mechanism-level inference corrected; stronger product source evidence admitted. **Production validation OPEN · PWA release HOLD.** No LogMate/Design Studio/Marketing/Engineering writes; no new runtime test. The next adjacent valuable work is an Engineering-authorized paired-binary + actual Sembast Web retry/fault exercise. Without a compiled artifact and physical enrolled iPad, repeating abstract green synthetic cases would not close the gate.


---

## 15. Exact pinned dependency, retryable logical migration and durable-custody audit [SOURCE / 2026-10-30]

**Provenance.** Read-only LogMate main source at repository blob `021d9001ae1240a824c5df570fb679597edc3875`, capability codec `f82b49da619e2fc861edf133eb9e66b195017a03`, `pubspec.yaml` blob `49ec62d16f0db7e6e69ad2d19366510711548176`, and **`pubspec.lock` blob `746ef9de51b1096fb1d64784d098ae188abdbd43`**. The lockfile resolves **sembast 3.8.11 and sembast_web 2.4.6**, with package integrity hashes; `^2.4.6` in pubspec.yaml is a constraint, **not proof that a newly published 2.4.6+1 was installed or compiled**. The actual deployed Flutter Web artifact and its lockfile/build provenance remain UNKNOWN. Package author [sembast_web 2.4.6](https://pub.dev/packages/sembast_web/versions/2.4.6) explicitly warns that cross-tab transactions may rerun and must be idempotent; [version history](https://pub.dev/packages/sembast_web/versions) and [changelog](https://pub.dev/packages/sembast_web/changelog) were checked 2026-10-30. The latest 2.4.6+1 listing is **CHANGE WATCH**, not an authorized dependency update.

**SOURCE-confirmed ordering of the v16 branch** in [the repository](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/sembast_logbook_repository.dart): the application opens through `_prepareDatabase()`, starts a Sembast transaction, validates the exact v16 capability and canonical/Owner/Replica/Outbox state, requires all seven new Sync stores empty, writes deterministic legacy hold records, invokes the **test-only** prepublication probe, and publishes the v17 capability marker **in that same transaction**. A later open of a v17 marker uses the current decoder/validation path. A failed callback is expected to reject the transaction; **actual WebKit/Chromium rollback, retry, process termination and durable persistence are not established by source reading**.

**Important narrower result:** the v16 classifier does not turn legacy audit timestamps into verified remote Sync operations. It preserves the original outbox rows and writes holds keyed from existing operation/store keys, with explicit legacy-unproven/review/deferred classifications. The code does not show a network receipt, server acknowledgement or file handoff inside this classifier. That is evidence of *logical re-execution tolerance for these writes*, **not proof that the entire migration or every repository transaction is idempotent**.

## 16. Replica identity and retry semantics: a bounded contradiction test [SOURCE / SYNTHESIS]

`_publishCurrentCapability` first ensures local Replica identity, then ensures Sync State, then writes the schema marker. `_ensureLocalReplicaIdentity` returns if an existing valid record is present; otherwise it generates a 32-byte identifier using `Random.secure()` and writes it inside the transaction. `_ensureSyncState` creates its default row only when absent, linking its originReplicaId to the identity read in the same transaction.

**CONTRADICTION resolved:** the phrase “a transaction callback must produce the same result if run twice” cannot be applied as a literal claim that the random **candidate bytes** are identical across retries. The stronger, relevant invariant is that only the **committed** identity is published and Sync State agrees with it; a discarded candidate must not escape into an external receipt or a different committed row. The source supports that *intended internal ordering*, not browser crash durability or every cross-tab interleaving. The package's idempotence warning therefore warrants a paired-tab test, rather than an automatic defect claim against `Random.secure()`.

**Separate trust boundaries:** `Random.secure()` supplies unpredictable local identity generation; it does not authenticate Firebase UID, prove a device is enrolled in airline MDM, encrypt the ledger, or authorize P2P transport. A new Replica on a *fresh restored destination* is intentional; a retry on the *same already initialized ledger* must not silently rotate a committed Replica or original Operation IDs. Source-generated candidate identities discarded on transaction retry are not themselves an identity-rotation incident.

## 17. 17 deterministic source predicates [VALIDATION — STATIC ONLY]

A connector-backed read of the exact four blobs above was subjected to **17/17 deterministic source-pattern assertions** on 2026-10-30: (1–2) logical current v17 and historical v16 constants; (3) `_prepareDatabase` Sembast transaction wrapper; (4–6) v16 decoder, Owner read and seven-Sync-store-empty guard; (7–8) classification before fault seam before marker publication; (9–10) deterministic legacy record/custom hold-key patterns; (11) no explicit network/file operation tokens inside the bounded classifier; (12) Replica→Sync State→marker source ordering; (13) `Random.secure()`; (14) conditional test-only probe; (15) pubspec caret constraint; (16–17) exact locked sembast_web 2.4.6 and sembast 3.8.11.

**Adjudication:** 17/17 is **STATIC SOURCE-PATTERN PASS**, not Dart analyzer/test, browser execution, Sembast cross-tab retry reproduction, cryptographic audit, physical iPad evidence, 37-store backup/restore, or a product release gate. Negative token absence is **not** a proof of absence of side effects in transitive helper calls. No test fixture, source data or private LogMate code was copied into this public research repository.

## 18. High-information-gain fault and concurrency exercise [VALIDATION DESIGN — NOT RUN]

| Case | Controlled setup and intervention | Required independent oracle |
| --- | --- | --- |
| RT01 | Exact lockfile-resolved Web build; pristine disposable v16 with bound Owner, legacy record/custom outbox and a known Replica | Pre-state full 37-store inventory, original Operation IDs, payload digests and Owner fingerprint retained |
| RT02 | Inject `beforeCapabilityPublication` failure after legacy holds, then close/reopen | v16 marker and all original rows unchanged; **no partial Sync holds**, no false success |
| RT03 | Retry same migration without fault after RT02 | One v17 marker, one hold per original operation, correct classification and original Replica/Owner |
| RT04 | Two tabs concurrently open the same v16 ledger with a controlled competing write | Record actual callback invocation count, committed marker, no lost outbox/duplicate holds; do not assume IDB `versionchange` |
| RT05 | Concurrent first initialization of an empty disposable ledger | Exactly one committed Replica, Sync State originReplicaId matches, no externally visible discarded candidate |
| RT06 | One tab already at v17 while an old compiled v16-capability binary attempts to read/write | Explicit compatibility/refusal behavior and preserved unsaved edit; no silent schema downgrade |
| RT07 | Force quota/write failure while migrating; reopen from a fresh browser process | No falsely published marker or lost source rows; classify any partial persistence as FAIL |
| RT08 | Kill browser/process at chosen stages before/after completion; repeat across engines | Commit acknowledgement, reopened ledger and independently exported backup agree; distinguish atomicity from crash durability |
| RT09 | Save .lbk outside origin storage, independently read bytes, restore empty same-UID target | 37-store semantics, Owner, original Operation IDs, new destination Replica and no implicit server Sync |
| RT10 | Repeat RT02–RT09 on Safari tab, installed Home Screen and managed EFB separately | Device/iPadOS/MDM provenance, Files/Open In restrictions, VoiceOver and offline relaunch recorded |

All tests use synthetic/disposable ledgers, never real pilot records. For RT04, **count callback retries**, not merely final row count; a passing final state may conceal a non-idempotent external effect. For RT07/RT08, separate a browser transaction's atomic commit from the OS/flash persistence and storage-eviction guarantees. The [W3C IndexedDB 3.0 specification](https://www.w3.org/TR/IndexedDB/) defines atomic transaction commit and optional `strict`/`relaxed` durability hints, but **no evidence establishes which hint the pinned Sembast Web/idb_shim path uses or whether Safari honors a requested hint for this build**. [WebKit storage policy, 2023-08-10](https://webkit.org/blog/14403/updates-to-storage-policy/) separately documents quota, eviction and best-effort storage. A transaction commit is **not** an external backup.

## 19. Five-track integrated decision and operational response [DEPENDENCY / TRANSFER VALIDATION]

- **E — lead and owner:** establish a release-state proof ledger distinguishing source migration, committed logical marker, cross-tab retry, independently retained backup, crash reopen and managed-device durability. HOLD unsafe old-binary downgrade and unverifiable restore.
- **A — platform prerequisite:** own Sembast-Web-over-IndexedDB mechanics, BroadcastChannel notification, physical IDB schema versus logical marker, transaction durability hints, Safari/Chromium differences and package version CHANGE WATCH. Do not conflate BroadcastChannel delivery with durable commit.
- **C — independent validation:** execute RT01–RT10 with pinned compiled binaries, exact lockfile, controlled fault injection, multi-tab telemetry and physical enrolled iPad; publish expected/observed evidence and falsification cases. A 17/17 source scan is insufficient.
- **B — UX/task architecture:** distinguish “update downloaded”, “local data migration finished”, “external backup verified”, “restore succeeded” and “cloud Sync completed”. Under failure, show recoverable review state without hiding pending edits; consume Design Studio [W121 Stage 3 PRACTICE](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md), not a claimed validated UI.
- **D — discovery/claims:** maintain [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) HOLD on seamless update, automatic backup, safe downgrade and EFB readiness; do not claim field reliability from synthetic source checks.

**Engineering transfer:** [D003 schema evolution](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) establishes a useful expand/backfill/contract mental model but its SQLite experiment is not Sembast-Web product evidence. Engineering owns LogMate code changes and release fixtures. No peer repository modifications.

## 20. Checkpoint and adjacent-work decision [MINTTAP DIRECTION / OPEN / CHANGE WATCH]

**MINTTAP DIRECTION, not product approval:** retain the existing logical migration guards and source Owner/Outbox custody; demand evidence of *committed-state invariants under actual Sembast Web retries*, rather than demanding literal deterministic random candidates or inventing an IndexedDB v17 physical upgrade. Keep the approved .lbk-first and user-triggered Manual Sync boundary. Do not silently upgrade dependencies, modify LogMate, change deployed origins, prune caches or advertise automatic rollback.

**OPEN:** actual paired old/new compiled binaries; whether migration callback retries occur under specific competing writes; actual persistence after kill/quota; live Worker/app/DB sequencing; external Files readback; same-UID full 37-store restore; installed/managed iPad, MDM, VoiceOver, release provenance and Sync. **Production validation remains OPEN.**

**CHANGE WATCH (checked 2026-10-30):** sembast_web 2.4.6+1 is published, while the checked LogMate lockfile remains 2.4.6; platform/browser storage policies and physical durability behavior must be rechecked against actual shipped versions.

**Meaningful stopping boundary:** static source and package-level uncertainty narrowed; the next high-value question is now a **different evidence class**—Engineering-approved compiled Web/Sembast retry and real-device fault execution. Repeating more abstract model green checks would not promote the gate. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


---

## 21. Pinned Sembast Web browser escalation — 2026-10-30 [SOURCE / VALIDATION DEFINED]

Prior 17/17 checks were STATIC SOURCE-PATTERN only. A new executable research instrument is committed at [pinned-package harness](handoffs/pwa_pinned_sembast_probe/) with [GitHub Actions workflow](../.github/workflows/stage8_pinned_sembast_web.yml). It compiles actual Dart package dependencies, pinned directly to **sembast_web 2.4.6** and **sembast 3.8.11** (the versions observed in LogMate's lockfile), then opens a synthetic Sembast database in two independent same-origin Chromium tabs. It is **not LogMate code, a LogMate fixture, or product validation**.

**SOURCE:** [sembast_web 2.4.6 documentation](https://pub.dev/packages/sembast_web/versions/2.4.6) describes IndexedDB-backed memory-loaded data, BroadcastChannel notification, cross-tab-safe transactions and the possibility of callback re-execution on concurrent change; callback idempotence is a requirement, not proof that a particular overlap always retries. [W3C IndexedDB](https://www.w3.org/TR/IndexedDB/) specifies physical database transaction/version semantics, not Sembast's logical capability marker. [Dart browser test documentation](https://github.com/dart-lang/test/blob/master/pkgs/test/README.md) provides browser test background. The new harness uses compiled Dart JS plus Playwright to coordinate two tabs explicitly.

**Fixture design:** one synthetic store holds logical capability 17, counter 0, and fixed SYNTHETIC-REPLICA; both tabs open the same named database. Concurrent increment callbacks have a deliberate overlap, each records invocation count, and the final committed counter is inspected. A deliberately thrown transaction tests rollback, close/reopen tests browser-session persistence, and indexedDB.databases() separately records physical IDB database versions. The CI workflow records Dart dependency resolution, Chrome version, compiled JS SHA-256 and uploads a JSON result plus generated pubspec.lock. **Direct dependency versions are pinned; transitive dependencies may differ from LogMate's full lockfile** until independently compared.

## 22. PS01–PS06 evidence oracles [VALIDATION — EXECUTION UNVERIFIED]

| Oracle | Required observation | What it does not prove |
| --- | --- | --- |
| PS01 seed | Marker 17, counter 0 and synthetic Replica committed together | Product v16→v17 migration |
| PS02 tab visibility | Already-open second tab observes seed | BroadcastChannel timing SLA |
| PS03 overlap | Two concurrent increments yield final counter 2; report each callback invocation count | A correct result does not necessarily mean a retry occurred |
| PS04 thrown transaction | Intentional exception does not publish counter 999 | Power-loss/quota durability |
| PS05 reopen | Closing and reopening preserves committed state | External Files backup or managed iPad persistence |
| PS06 physical IDB | Browser database names/versions recorded separately from marker 17 | Deployed LogMate physical database version |

**Cross-tab timing safeguard:** second-tab seed visibility and final counter are polled with bounded convergence (25 reads at 160 ms intervals); record the number of polls. An immediate stale read is not automatically a lost write. A failure after the deadline is an observed synthetic timeout requiring package/browser diagnosis, not proof of a LogMate defect. This avoids conflating BroadcastChannel propagation delay with transaction atomicity.

**Failure-first adjudication:** dependency-resolution/compile failure is NON-EXECUTION; browser launch or page-readiness failure is NON-EXECUTION; executed assertion violation is FAIL SYNTHETIC; successful cases are PASS SYNTHETIC only after actual job log/artifact/commit inspection. Preserve the actual retry-observed boolean even if final counter is 2. A failing synthetic harness requires fixture diagnosis before inferring any product problem.

**Execution status:** local Chromium loopback navigation was blocked by ERR_BLOCKED_BY_ADMINISTRATOR before execution. Hosted workflow source is committed and push-triggered, but no hosted run/job/artifact has yet been verified here. **No new runtime PASS is claimed.**

## 23. Cross-track integration and contradiction controls [DEPENDENCY / TRANSFER VALIDATION]

- **A platform owner:** Sembast callback retry, BroadcastChannel propagation, physical IndexedDB version and logical capability marker are separate mechanisms; 2.4.6+1 remains CHANGE WATCH, not the pinned product version.
- **E lead/security/operations:** candidate random Replica generation during a retry is not itself a defect. Required product invariants concern final committed Replica, Sync State, Owner and Outbox consistency and absence of duplicate external effects. A Sembast commit is not OS-crash durability or independently retained backup.
- **C quality/validation:** first adjudicate exact hosted package fixture, then request Engineering-approved exact compiled LogMate old/new Web builds, real migration-failure seam, competing tabs and disposable 37-store data. Physical Safari tab, installed Home Screen and managed EFB/VoiceOver require distinct evidence.
- **B UX architecture:** consume Design Studio W121; distinguish local committed save, migration complete, Files backup verified, restore complete and cloud Manual Sync. Do not call one state another.
- **D discovery/claims:** consume Marketing D8/D9 HOLD; no seamless update, background sync, guaranteed offline persistence, safe rollback or recoverable EFB backup claims.

**CONTRADICTION:** a correct synthetic final counter 2 does not establish that callback re-execution happened unless attempts show it. A browser physical version differing from 17 does not identify LogMate's deployed physical version. Successful reopen is weaker than crash survival, which is weaker than independent external backup. SQLite D003 is a reasoning transfer, not Sembast/WebKit runtime evidence.

## 24. Next evidence boundary [OPEN / MINTTAP DIRECTION / CHANGE WATCH]

First verify hosted workflow execution, dependency lock, compiled JS hash and PS01–PS06 observed outcomes. If valid, hand the resulting concrete retry/propagation behavior to Engineering for exact-product RT01–RT10 (v16/v17, migration failure, old/new shell, two-tab write, Replica/Owner/Outbox and unsupported downgrade). Then verify an external LBK file saved, independently read back and restored to an empty same-UID 37-store destination, followed by physical iPad Safari/Home Screen/managed EFB, offline relaunch, storage pressure, Files/MDM restrictions and VoiceOver. No changes to LogMate or other specialist repositories.

**MINTTAP DIRECTION:** instrument first, claim only observed evidence. **OPEN:** hosted result, exact-product migration and physical backup. **CHANGE WATCH:** Dart/Chrome versions, Sembast Web releases, WebKit storage. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


---

## 25. Native IndexedDB durability and cross-tab rollback observation escalation [SOURCE / SYNTHESIS / 2026-10-30]

**Question:** Does a successful Sembast Web transaction demonstrate durable ledger custody, and can a two-tab fixture distinguish a true package transaction from merely reading an in-memory copy? The answer requires **observed runtime evidence**. Package documentation is a source of expected behavior, not a successful test. The previous PS01–PS06 probe recorded the final state and callback attempt counts but did **not** observe the native IndexedDB transaction's durability hint, inspect the non-faulting tab after a deliberate rollback, or reopen in a newly created tab after closing both original pages. Those are material missing controls, not additional generic theory.

**SOURCE — platform history/standard/implementation:**
- [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) distinguishes atomicity, physical schema \`versionchange\`, and the \`strict\`/\`relaxed\`/\`default\` durability **hint**. It does not define Sembast's logical capability 17, nor promise that a commit is an external backup.
- [Chrome's 2023-11-03 IndexedDB default-durability announcement](https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed/) describes Chrome 121's change to a relaxed default. A completed transaction can precede physical flushing; even \`strict\` is not a universal zero-loss guarantee under hardware failure. This is **Chromium-specific**, not evidence of WebKit behavior or the exact Sembast/idb_shim call options.
- [MDN IDBTransaction.durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability) describes the read-only property as the transaction's selected **hint**, not an independently verified fsync or power-loss result.
- [Pinned sembast_web 2.4.6 package author documentation](https://pub.dev/packages/sembast_web/versions/2.4.6) describes in-memory loading, IndexedDB backing, BroadcastChannel propagation and possible re-execution of concurrent transaction callbacks. This author contract is not a recorded retry occurrence.

**CONTRADICTION control:** The proposition "a Sembast callback resolved, therefore every byte was flushed to nonvolatile storage" is unsupported. Equally, seeing a physical IDB version other than 17 is **not** evidence of a failed LogMate logical v17 migration. An old-tab cached read, a committed Sembast record, an IDB transaction completion, a fresh-tab read, an OS restart and an independently retained \`.lbk\` file are successively different evidence classes, not interchangeable proxies.

## 26. Strengthened pinned-package probe PS07–PS09 [VALIDATION DESIGN — NOT YET ADJUDICATED]

[The existing research-only pinned-package fixture](handoffs/pwa_pinned_sembast_probe/run_probe.py) now adds three bounded controls without copying private LogMate code or modifying product repositories:

| ID | New observation | Positive oracle and interpretation limit |
| --- | --- | --- |
| PS07 | After tab B deliberately throws inside its Sembast transaction, tab A polls the expected committed state | Tab A eventually sees counter 2 rather than an aborted counter 999. This is **cross-tab rollback visibility**, not power-loss durability. |
| PS08 | Both original pages close; a fresh tab opens in the **same Chromium browser context/profile** | Logical marker 17, counter 2 and synthetic Replica remain. This is **new-tab same-profile reopen**, not process crash, new profile, Safari or Files backup. |
| PS09 | Playwright \`add_init_script\` wraps native \`IDBDatabase.prototype.transaction\` before the Dart bundle executes, returning the original transaction unmodified | Record database, mode, requested \`options.durability\` and returned \`transaction.durability\` for at most 100 calls per tab. **OBSERVED** means a native call was intercepted; **NOT_OBSERVED** means no conclusion about the underlying path or durability. The wrapper does not force \`strict\` or claim physical flush. |

**Adjudication requirements:** The original PS01–PS06 and new PS07–PS09 remain **UNVERIFIED** until the exact hosted job checkout SHA, resolved dependency lock, JS digest, Chrome version, execution log, assertion results and artifact are inspected. A workflow being present or a push being accepted is not a PASS. A failed compile/browser launch is NON-EXECUTION; a reached failing assertion is FAIL SYNTHETIC. PS09 is observational and cannot be counted as a semantic PASS for durable storage if no native call was intercepted. Any transaction wrapper side effect must be evaluated by comparing instrumented and uninstrumented runs before generalizing.

**Hosted-result access boundary:** The available GitHub commit-workflow lookup returns only pull-request-associated runs; an empty response does **not** establish that a push-triggered Actions job did not execute. The canonical workflow is [stage8_pinned_sembast_web.yml](../.github/workflows/stage8_pinned_sembast_web.yml). At this checkpoint there is no independently verified run ID/log/artifact for its push execution. Do not silently upgrade PS01–PS09 to PASS or invent an Actions URL.

## 27. Operational judgment, cross-track allocation and next release gate [MINTTAP DIRECTION / DEPENDENCY / TRANSFER VALIDATION / OPEN]

**Track comparison (current Stage 8):** E has the highest security/release decision pressure and source-level depth but lacks production/managed-device validation; A has mature origin/IDB/Worker standards and package semantics but lacks observed pinned Sembast browser behavior; C has the largest independent **execution evidence** gap; B's W121 task/interaction research is Stage 3 PRACTICE, not device or human PASS; D's web acquisition/claim mechanism is adequate to maintain Marketing D8/D9 HOLD but has no valid field reliability claims. **Allocation:** E/A/C receive the bulk of this bundle to resolve durability, callback retry and test-oracle quality; B/D consume truthful state and claims boundaries rather than reauthoring security primers.

- **E owns release custody:** a success banner cannot be inferred from a completed Sembast transaction alone. Require exact owner/operation/Replica invariants, independent backup readback, migration/downgrade refusal and managed EFB retention before lifting PWA HOLD.
- **A owns browser mechanics:** capture whether the pinned package requests any native IDB durability option; distinguish Chrome default, WebKit behavior, physical IDB version and Sembast logical capability. A trace containing \`default\` is not proof of relaxed/strict physical flush.
- **C owns falsification:** compare instrumented versus uninstrumented results, inspect PS01–PS09 CI evidence, then hand the method to Engineering for exact old/new compiled LogMate binaries and RT01–RT10. A successful synthetic fixture must not be promoted to product acceptance.
- **B consumes [Design Studio W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md):** independent states for locally saved, committed/migrated, backed up externally, restored and synced; accessible error/recovery tasks remain OPEN on physical EFB.
- **D consumes [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md):** no guaranteed offline retention, automatic cross-device sync, seamless update or safe rollback copy. The web site must not make release claims based on synthetic browser tests.
- **Engineering transfer:** [D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) demonstrates schema publication versus old-reader compatibility with SQLite, not Sembast product behavior; [Q006](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/QUALITY_STATUS.md) reinforces that a successful CI job shell and semantic product assertion are separate. Engineering owns exact-product fixtures and changes.

**Next meaningful evidence checkpoint:** inspect the push-triggered pinned-package job and its artifacts (PS01–PS09); if execution fails, diagnose compile/fixture issues without calling them LogMate defects. Then run exact-product RT01–RT10 with source/build provenance, followed by \`.lbk\` independent Files save/readback, same-UID empty-destination 37-store restore, and physical Safari/Home Screen/managed EFB under actual MDM policy. **Production validation OPEN · Stage 8 ACTIVE · PWA release HOLD.** No product/peer repository changes.

---

## 28. Instrumentation falsification control and provenance discipline — 2026-10-30 [SOURCE / VALIDATION DESIGN / CONTRADICTION]

**Decision-driving question:** Can PS09's JavaScript interception of native IndexedDB transactions perturb the very cross-tab behavior PS01–PS08 are meant to observe? Yes, in principle. Replacing a prototype method with a wrapper preserves the original return value but adds JavaScript work and changes call timing. A correct instrumented result is not evidence that the uninstrumented package behaves identically, and a retry observed in only one configuration cannot be generalized as an unconditional Sembast guarantee. This is a **test-instrumentation confound**, not an identified LogMate vulnerability.

The research-only [pinned Sembast Web probe](handoffs/pwa_pinned_sembast_probe/run_probe.py) now defines **PS10**, an *uninstrumented comparison context* in the same Chromium process. Unlike the original context, the control context receives **no** \`IDBDatabase.prototype.transaction\` override. Both contexts execute the same compiled Dart JS and the same bounded sequence: three-record synthetic seed, already-open second-tab convergence, overlapping delayed increment transactions, final counter 2, deliberate transaction exception, non-faulting-tab rollback observation, closure of original pages, and new-page same-context reopen. The evidence JSON retains both contexts' result objects and retry-attempt counts. The control has independent browser-context storage, so it cannot read or mutate the instrumented context's synthetic ledger.

**SOURCE:** [GitHub Actions event/path filter documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) specifies that both \`main\` and matching path changes must hold for this workflow's \`push\` trigger; a qualifying push makes a run *eligible*, not proved completed. [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) defines transaction and durability semantics but does not promise any given library's callback retry behavior. [Chrome's 2023-11-03 announcement](https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed/) explains Chrome 121's relaxed default; that policy is not a measurement of LogMate data loss or physical flush. [Sembast Web 2.4.6 author documentation](https://pub.dev/packages/sembast_web/versions/2.4.6) permits callback re-execution under concurrent writes; the observed callback count must be retained, not guessed from final state.

### PS10 acceptance and falsification [VALIDATION — NOT RUN/NOT ADJUDICATED]

| Condition | Interpretation |
| --- | --- |
| Both contexts reach marker 17/counter 2/Replica unchanged, exception rollback, cross-tab visibility and fresh-tab reopen | **Semantic parity in two synthetic contexts** for this one run; no proof of identical scheduling or general non-interference |
| Instrumented passes, uninstrumented fails (or inverse) | **CONTRADICTION requiring fixture/browser diagnosis**; do not attribute the difference to instrumentation without replication and isolated controls |
| Both pass, callback attempts differ | **Not inherently a contradiction**: transaction overlap and BroadcastChannel scheduling are nondeterministic; report attempts separately |
| Both pass, no callback attempts exceed one | Two concurrent increments reached final state, **but no actual retry observed**; cannot claim a retry-path test passed |
| PS09 trace empty or wrapper unavailable | **NOT_OBSERVED** for native interception, not evidence of no IndexedDB transactions, no durability or a product failure |
| Browser launch, Dart compile, dependency resolution, or page readiness fails | **NON-EXECUTION** of downstream assertions; no synthetic or product PASS |
| A reached semantic assertion fails | **FAIL SYNTHETIC**, with exact checkout/build/browser, failed oracle and trace; investigate test assumptions before product inference |

**Important provenance correction:** PS08/PS10 create fresh *pages* inside ephemeral Playwright \`browser.new_context()\` storage containers. They do **not** close and restart Chromium with a persistent user-data directory. Therefore the evidence may support same-context page-reopen visibility, **not** browser-process restart, operating-system crash survival, persistent-profile survival, iPadOS eviction resistance, or external backup custody. An independent disk-backed persistent-profile process-restart test is a **separate future oracle**, not a relabeling of PS08.

### Evidence bundle required for adjudication

The committed workflow invokes \`dart pub get\`, records the resolved dependency graph, compiles Dart JS, hashes \`web_probe.js\`, prints the Chrome version, executes Playwright and uploads bounded JSON/lockfile artifacts even on failure. The direct Sembast dependencies are pinned, but the full transitive graph, Dart stable SDK, Chrome binary and runner image remain run-specific. A proper review must record the *actual* run ID, checkout SHA, resolved \`pubspec.lock\`, Dart and Chrome versions, compiled JS SHA, executed test output and artifact identity. The workflow source, a Git commit, a green job badge without inspected semantic assertions, or an empty PR-only commit-run query cannot substitute for these observations.

**Observed this research cycle:** the source code was updated and the GitHub file-write operation returned a commit SHA. No Dart compilation, Python Playwright execution, push-triggered Actions log, artifact bytes or physical device evidence was obtained. Local environment has no Dart SDK/Chrome executable, and direct public GitHub API access from the container was unavailable; the GitHub connector's commit-workflow endpoint returns PR-associated runs only. **PS01–PS10 remain EXECUTION UNVERIFIED.** This does not mean the workflow failed or was skipped.

**Failure-result refinement:** the harness now explicitly records a phase. A failure before both tabs complete page readiness is labeled \`NON_EXECUTION\`; a failed assertion or command after the two-tab execution boundary is \`FAIL_SYNTHETIC\`; a fully completed run is \`PASS_SYNTHETIC\`. A cleanup exception after assertions complete is reported separately as \`POST_ASSERTION_CLEANUP_FAILURE\`, not mislabeled as an assertion failure or pre-execution setup error. These labels are **fixture-internal prospective outputs**, not observed hosted outcomes. Dart compile failures happen before Python creates its JSON and must be classified from the CI step/log instead. This prevents an infrastructure setup error being reported as a negative Sembast result, while preserving real assertion failures for investigation.

## 29. Integrated failure model and cross-track handoff [SYNTHESIS / DEPENDENCY / TRANSFER VALIDATION]

The strongest defensible chain is **exact-source provenance → actual browser execution → committed synthetic state → independent tab observation → page-reopen observation → real-product migration/Owner/Outbox validation → external Files backup readback → physical installed/managed EFB acceptance**. Each transition is a new evidence class; none is automatically implied by the previous one.

- **Track E (lead, Stage 8 bottleneck):** maintain the security/operations gate and custody sequence. Neither an instrumented transaction trace nor a green package-level fixture licenses destructive migration, automatic rollback or cloud Sync claims. Retain user-initiated Manual Sync and .lbk-first transfer until product decisions are explicitly authorized.
- **Track A (browser prerequisite):** distinguish \`IDBDatabase.version\`, the Sembast logical marker, \`IDBTransaction.durability\`, same-context page reopen and actual persistent-profile restart. The JS wrapper is an observer, not a durability configuration change. WebKit/iPadOS and MDM remain independent CHANGE WATCH.
- **Track C (largest validation gap):** independently adjudicate PS01–PS10, compare control/instrumented semantics and attempt counts, then test a persistent-profile process restart as a separate synthetic scenario if execution access permits. Only Engineering-approved exact LogMate binaries can close RT01–RT10.
- **Track B (Design Studio W121 consumer):** separate truthful states for committed local edit, safe update, external backup saved and independently read, restore success, and cloud Manual Sync. A synthetic counter test offers no human/VoiceOver acceptance.
- **Track D (Marketing D8/D9 consumer):** keep claims of seamless update, unattended EFB↔native sync, guaranteed persistence and safe downgrade on HOLD; successful synthetic browser assertions would still be inadequate public-product evidence.

**TRANSFER VALIDATION:** Software Engineering D003's reader/writer/schema compatibility framework is reusable for the *acceptance matrix* but its SQLite results cannot certify Sembast Web, Chromium durability or WebKit. Design Studio W121 and Marketing D9 are read-only consumers; no changes to those repositories or LogMate were made.

**Adjacent-question check:** the remaining high-value question is not another theoretical IndexedDB primer but actual CI execution and product/device evidence. PS10 resolves a concrete instrumentation-control design gap; further source-only assertion expansion has diminishing value until PS01–PS10 are executed and their failures classified. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**


---

## 30. Hosted pinned Sembast PS01–PS10 adjudication — 2026-10-30 KST [VALIDATION / SOURCE]

**Material checkpoint:** Previously unverified push-triggered GitHub Actions runs were retrieved through the repository Actions runs collection, and their exact jobs, decoded execution logs and artifact metadata were inspected. The PR-filtered commit-workflow helper was not used to infer absence. This is actual hosted execution of a research-only pinned-package fixture, NOT LogMate product runtime.

| Run (UTC 2026-10-29) | Checkout | Job | Semantic verdict | Artifact ZIP SHA-256 |
| --- | --- | --- | --- | --- |
| [40946201094](https://github.com/yhappcom/web-manager/actions/runs/40946201094), 20:07:30 | 247c39725512fd1e8e61d5a9587a7072af9636f6 | 123702088611 | PASS_SYNTHETIC | artifact 12928643135; b73e0213c9df1bfc7ba228afaff815f477054a884c7a820965adb45ea19a4176 |
| [40946412967](https://github.com/yhappcom/web-manager/actions/runs/40946412967), 20:08:56 | caa7eb26513e564ed5ea4955ab89875a3abaacd3 | 123702834889 | PASS_SYNTHETIC | artifact 12928702798; 284a8ffde492a13e1c2e5b1cdac0ac42672f46fd6287d0dad000009a25109b83 |
| [40946454593](https://github.com/yhappcom/web-manager/actions/runs/40946454593), 20:09:13 | 8fbb9810713d391d20f3aa60478c35a8ea1f7aab | 123702979614 | PASS_SYNTHETIC | artifact 12928678634; f44a7bc4bbf218b4407b30b51e48125abca65581103fda40f0472185386b1be2 |

All three jobs completed successfully, with ten named checks and final PASS_SYNTHETIC in decoded JSON. The ZIP digest is reported by GitHub Actions upload logs and artifact metadata; the archive bytes were not independently downloaded/rehashed. Recorded environment: Ubuntu 24.04, Dart 3.13.7, Chrome 156.0.8078.47, Playwright 1.57.0, direct sembast_web 2.4.6 / sembast 3.8.11, idb_shim 2.11.1. All three logs print the same compiled JS SHA-256: 31c67b26f7a21b5b930cffd11cfba36bf5b724a2d3d31b26526e936871f65a23. Resolved dependencies were inspected in logs, but full lockfile artifact bytes were not independently hashed. The latest run precedes the documentation-only HEAD 84f61474.

**Observed in all three successful runs:**

1. PS01: synthetic logical marker 17, counter 0, Replica SYNTHETIC-REPLICA seeded.
2. PS02: second-tab seed visibility after bounded convergence (1 poll).
3. PS03: overlapping 350-ms increment callbacks, tab A 1 attempt, tab B 2 attempts, final counter 2, Replica unchanged. A real callback retry was observed, not inferred solely from the final value.
4. PS04 and PS07: deliberate thrown transaction was caught; counter remained 2 in both the faulting and other tab. This is synthetic rollback visibility, not LogMate Owner/Outbox proof.
5. PS05: same-page Sembast close/open retained marker 17, counter 2 and Replica.
6. PS06: physical IndexedDB database wm-pinned-sembast-246 had version 2 while the application-level marker was 17. They are independent version spaces.
7. PS09: native IDB transaction wrapper installed on both tabs and recorded read/write calls with requestedDurability null and observedDurability default. This is an exposed hint, NOT measured disk flush or strict durability.
8. PS08: after closing original pages, a new page in the same ephemeral Chromium browser context read marker 17/counter 2/Replica.
9. PS10: independent uninstrumented Chromium context reproduced seed, overlapping increments, exception rollback, other-tab visibility and fresh-page reopen; final counter 2, A attempts 1/B attempts 2. Three runs support bounded semantic parity, not universal non-interference.

**Negative comparator preserved:** [run 40928346908](https://github.com/yhappcom/web-manager/actions/runs/40928346908), job 123639800675, checkout 8761ec55757952cca847c1144e2c1683026d11e9, FAILED a reached assertion: immediate second-tab read showed logicalCapability null, counter 0, Replica visible. This is a synthetic fixture assertion failure at that revision, NOT evidence of LogMate data loss. Later bounded convergence passed; the precise cause of the earlier partial observation was not conclusively diagnosed.

**Gate verdict:** PS01–PS10 move from EXECUTION UNVERIFIED to HOSTED CHROME SYNTHETIC PASS in three inspected runs. They do not close exact LogMate v16→v17 migration, old/new mixed clients, UID/Replica/Operation/Outbox integrity, 37-store external backup, OS crash, WebKit, installed Home Screen or managed EFB. Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD.

## 31. Mechanism, failure modes and falsification [SYNTHESIS / CONTRADICTION]

- **Author contract versus observed occurrence:** Sembast Web 2.4.6 documents possible concurrent callback re-execution. In the synthetic fixture, tab B actually executed twice in all three runs. Transaction callback idempotence is therefore a concrete implementation requirement. It does not prove LogMate's migration callback retried or that every concurrent transaction retries.
- **Transaction isolation versus external side effects:** the counter remained 2 after deliberate throw and other-tab observation. The test does not exercise random Replica generation, external network/file/analytics side effects, Owner admission or Outbox mutation within a retryable product callback. Committed Replica→Sync State→capability invariants require Engineering-owned product execution.
- **Version distinction:** observed physical IndexedDB version 2 and logical marker 17 coexist correctly. Native versionchange/blocked must not be misrepresented as the observed LogMate logical v16→v17 migration.
- **Durability ladder:** native IDB default hint, same-page read, other-tab read, fresh page in ephemeral context, separate process with persistent profile, forced termination, OS crash and independently retained Files backup are distinct evidence classes. PS01–PS10 cover only the first four.
- **Instrumentation:** three runs showed semantic parity with and without the IDB wrapper, but the two contexts have separate storage and run sequentially. This is limited reproducibility, not proof that interception never changes timing.
- **Provenance:** exact direct package versions and JS hash were logged. Dart stable and runner Chrome are mutable, and transitive bytes were not independently rehashed. A release-grade reproducibility manifest is still needed.

**Primary sources:** [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/), [Chrome IndexedDB relaxed-default announcement (2023-11-03)](https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed/), [MDN IDBTransaction.durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability), [Sembast Web 2.4.6](https://pub.dev/packages/sembast_web/versions/2.4.6), [GitHub Actions workflow-runs API](https://docs.github.com/en/rest/actions/workflow-runs). All observed runtime claims are Chrome 156 synthetic, not normative WebKit behavior.

## 32. PS11: persistent-profile graceful Chromium process restart [VALIDATION DESIGN / OPEN]

The next adjacent oracle is stronger than PS08. A research-only change to [the pinned Sembast probe](handoffs/pwa_pinned_sembast_probe/run_probe.py) uses Playwright launch_persistent_context with a disposable disk-backed user-data directory. It seeds marker 17/counter 0/Replica, increments to counter 1, gracefully closes the first Chromium context/process, launches a separate Chromium process with the same profile, and asserts marker 17/counter 1/Replica. No LogMate data is used.

**Acceptance:** inspect exact new push Actions run, checkout SHA, compiled JS, dependencies, Chrome, semantic JSON and artifact. A failure requires fixture/environment diagnosis rather than an automatic product-defect claim. A pass means only graceful separate-process same-profile persistence of this synthetic fixture. It is NOT forced kill, OS crash, fsync, eviction, Safari, MDM or independent .lbk Files proof. PS11 execution OPEN at this checkpoint; an eligible push is not a completed run.

## 33. Five-track transfer and production gate [DEPENDENCY / TRANSFER VALIDATION / MINTTAP DIRECTION]

| Track | Evidence maturity and pressure | Owner action |
| --- | --- | --- |
| E (lead) | Stage 8 release/security bottleneck; package retry observed, product ledger custody unproven | Keep PWA HOLD; own UID/Replica/Outbox, migration, independent backup, rollback and non-destructive release criteria |
| A | Strong Worker/IDB foundations; Chrome pinned-package retry, version and hint observed; Safari/install/eviction OPEN | Own browser difference and PS11 process lifecycle interpretation |
| C | Hosted synthetic evidence stronger; exact-product/physical EFB/VoiceOver/crash still major validation gap | Adjudicate PS11; then Engineering-approved RT01–RT10 |
| B | [Design Studio W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) Stage 3 PRACTICE/NOT PASSED | Consume distinct locally saved, migrated, externally backed up, restored and manually synced states |
| D | [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) claims HOLD | Withhold guaranteed retention, unattended sync, seamless update and recovery claims |

**Engineering transfer:** [D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) demonstrates generic old-reader/schema-publication issues in SQLite, not LogMate Web behavior. [Q006](https://github.com/yhappcom/software-engineering-studio/blob/main/progress/QUALITY_STATUS.md) distinguishes green CI shells from inspected semantic assertions; PS01–PS10 now satisfy a synthetic semantic checkpoint only. LogMate [MASTER.md](https://github.com/yhappcom/logmate/blob/main/MASTER.md) retains Firebase UID authority, local-first Manual Sync and incomplete production Sync. No product policy change authorized.

**Next:** adjudicate PS11; then prioritize Engineering-approved exact old/new LogMate compiled RT01–RT10 (interrupted migration, mixed clients, Owner/Replica/Outbox, unsupported downgrade), independently saved/read-back .lbk and same-UID empty-destination 37-store restore. Separately test physical iPad Safari tab versus installed Home Screen versus managed Web Clip under actual MDM, offline relaunch, storage pressure and VoiceOver. Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD. Product and peer repositories read-only.
