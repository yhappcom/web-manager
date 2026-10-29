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
