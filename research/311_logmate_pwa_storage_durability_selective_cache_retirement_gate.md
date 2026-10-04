# 311 — LogMate PWA Storage Durability & Selective Cache Retirement Gate

Status: **PASS (generic + LogMate source-contract) / PERSISTENCE + CURRENT ARTIFACT + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**
Date: 2026-10-04
Primary owner: **Track E — Web Architecture, Security & Operations**
Dependency owner: **Track A — Web Platform & Browser**
Consumers: Tracks B/C/D

## Purpose

310 established that LogMate should migrate from Flutter's retiring generated caching worker toward an explicitly owned worker contract. This checkpoint adds a prerequisite: executable-cache maintenance, Service Worker replacement and durable pilot-log data are separate failure domains.

## SOURCE — platform boundaries

Service Worker Cache Storage is author-managed and separate from the browser HTTP cache. Named caches do not disappear merely because a worker script changes; applications govern cache versioning and retirement.

The Storage API distinguishes best-effort and persistent origin storage. navigator.storage.persist() requests persistent mode and persisted() observes whether it is granted. Granting is browser-policy dependent.

WebKit's published Safari 17+/iOS/iPadOS 17+ policy states that origin storage is best-effort by default; storage-pressure eviction normally occurs at origin granularity; persistent mode can exempt an origin from ordinary eviction; estimate(), persist() and persisted() are supported; and grant heuristics can include Home Screen Web App use.

Sources:
- https://www.w3.org/TR/service-workers/
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
- https://webkit.org/blog/14403/updates-to-storage-policy/

Clear-Site-Data also proves why cache maintenance and product-data reset must not be conflated. Its "storage" directive includes IndexedDB removal and Service Worker unregistration, while "*" composes all supported clearing classes.

Sources:
- https://www.w3.org/TR/clear-site-data/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data
- https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage/delete

## SOURCE — LogMate

Canonical yhappcom/logmate main inspected 2026-10-04.

web/index.html loads flutter_bootstrap.js and contains no hand-written LogMate worker registration. Makefile, precache_flutter_web.dart and verify_pwa_artifact.dart require Flutter's generated flutter_service_worker.js and fail closed if its expected contract is absent.

firebase.json declares Cache-Control: no-cache, no-store, must-revalidate. No Clear-Site-Data policy appears in the inspected hosting configuration.

Repository search found no current source evidence for navigator.storage.persist()/persisted(). This does not prove that runtime/dependency code never requests persistence; current product persistence state remains OPEN.

## SYNTHESIS

An offline EFB must keep four claims independent:
1. executable availability — worker + Cache Storage launch offline;
2. product-data durability — IndexedDB/Sembast ledger and pending operations survive;
3. eviction resistance — browser persistence mode reduces ordinary eviction exposure;
4. independent recovery — export/backup/restore survives origin loss.

Persistent storage is not backup, does not prevent explicit user/site deletion, does not prove record consistency and does not prove remote synchronization.

## MINTTAP / LogMate direction

Owned-worker cache retirement should be namespace-selective:

enumerate caches → identify LogMate executable-cache namespace/version → retain current and required rollback generation → remove only proven-obsolete LogMate executable caches.

Origin-wide website-data clearing, IndexedDB recreation or reinstall should not be ordinary stale-asset/update repair paths when unique unsynchronized flight records may exist.

Because LogMate may hold unique offline records, persisted() plus a bounded persist() request is a high-value implementation candidate. It is not yet a product implementation decision; Software Engineering must validate timing, browser behavior, UX and telemetry/privacy consequences.

## State model

Record independently:
A = artifact generation
R = registration/controller generation
C = executable cache generation
D = loaded document generation
L = local ledger/outbox generation
P = observed persistence mode
S = remote synchronization/ACK state.

P is a browser-storage property, not application authority. S remains remote convergence evidence.

## Persistent guards

- persistent storage granted ≠ backup exists;
- persistent storage granted ≠ explicit deletion impossible;
- best-effort storage ≠ immediate loss;
- quota estimate available ≠ bytes guaranteed;
- worker unregistered ≠ Cache Storage retired;
- worker replaced ≠ IndexedDB migrated;
- HTTP cache cleared ≠ Cache Storage retired;
- executable cache retired ≠ local ledger should be removed;
- origin-wide storage reset ≠ safe cache repair;
- Home Screen installed ≠ persistence granted;
- Safari tab persistence evidence ≠ managed Home Screen evidence;
- local record survives ≠ remote ACK/convergence.

## Cross-track transfer

**A:** own Storage API semantics, registration and Cache Storage lifecycle.
**B:** keep "saved locally", "persistent", "backed up" and "synced" as distinct user states.
**C:** add persistence mode, quota/write pressure and cache-only retirement to fixtures; prove cache maintenance leaves local ledger/outbox unchanged.
**D:** persistence/quota observations are diagnostic only and cannot prove durability or sync.
**E:** own cache namespace inventory, selective retirement, upgrade/rollback and recovery policy.

## VALIDATION

V0 preserve fresh normal Flutter 3.38.7 worker/bootstrap, exact cache names and manifest.
V1 on target Safari/iPad contexts record persisted() before/after one bounded persist() request and estimate() usage/quota.
V2 populate ledger/outbox and executable caches; retire only obsolete LogMate cache names; prove ledger/outbox unchanged.
V3 in disposable profiles compare cache-only retirement, worker unregistration and origin-storage reset to establish distinct blast radii.
V4 test quota/write pressure, termination, offline cold start and update; natural OS eviction still requires physical elapsed/device evidence.
V5 generated-worker N → owned-worker N+1 with pending local work and no IndexedDB reset.
V6 Safari tab → Home Screen → physical iPad → representative managed iPad.

## OPEN

Fresh normal artifact/cache names; current LogMate persistence request/result; physical Safari/iPadOS persistence outcomes; exact Sembast/IndexedDB identity; owned-worker cache namespace; recovery/export behavior; physical storage-pressure evidence; Home Screen/managed-iPad evidence; independent backup/restore; production ACK/convergence.

## CHANGE WATCH

Safari/WebKit quota, eviction and persistence grant heuristics are implementation policy and require revalidation on material platform changes. Flutter worker retirement remains an architecture dependency until LogMate owns its worker/cache contract.

## Integrated competency

> Offline durability requires separating executable cache maintenance from unique local product data. Persistent origin storage can reduce browser eviction risk, but it is neither backup nor synchronization.
