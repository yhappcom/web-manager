# 309 — LogMate PWA Exact-Artifact Promotion & Worker-Update Provenance Gate

Status: **PASS (generic + LogMate source-contract) / CURRENT ARTIFACT + DEPLOYED-BYTES + HOME-SCREEN + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-10-03  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependency owner: **Track A — Web Platform & Browser**  
Consumers: Tracks B/C/D

## Purpose

308 established that current Flutter defaults cannot be treated as proof of offline correctness. Canonical LogMate evidence now closes part of that OPEN: DATA-001 has a pinned, application-owned acceptance build contract. The next assurance boundary is whether one exact verified artifact remains identifiable through promotion, HTTP delivery, Service Worker update/control and device acceptance.

## SOURCE — LogMate canonical build contract

Canonical `yhappcom/logmate` main inspected at `31ecf70f5446d49cf6eb8b566e270ac273b37d61`.

`.github/workflows/data001-pwa-artifact-validation.yml`:
- pins Flutter `3.38.7` stable;
- records source SHA and `make build-pwa-acceptance`;
- requires a clean lockfile;
- uploads `build/web`;
- explicitly says the uploaded directory is the EFB acceptance unit and should be promoted/deployed without rebuilding.

`Makefile` builds Web with local web resources, then runs LogMate-owned post-processing and verification.

`tool/precache_flutter_web.dart` requires the generated `flutter_service_worker.js`, fails closed on an unexpected generated format, expands `CORE` to `Object.keys(RESOURCES)`, normalizes query keys and uses query-insensitive navigation cache matching.

`tool/verify_pwa_artifact.dart` requires the worker and core entry files, local CanvasKit, required local fonts, required worker resource keys and LogMate post-processing markers. It also enforces the acceptance-harness boundary.

Therefore:

`no hand-written worker source ≠ no application-owned worker contract`.

The source-level DATA-001 toolchain/build command is now PASS. A successful current artifact and deployed runtime remain OPEN.

## SOURCE — Web platform

Service Worker update is separate from ordinary application-asset caching. `ServiceWorkerRegistration.updateViaCache` controls whether HTTP cache is consulted for the worker script/imports; the default `imports` does not use HTTP cache for the main worker script. `ServiceWorkerRegistration.update()` checks for new worker bytes and installs a successor when the script differs.

Cache Storage is separate from the browser HTTP cache. Author-created caches are not automatically updated or deleted merely because a worker script changes; applications must govern cache versions/retirement.

Sources:
- https://w3c.github.io/ServiceWorker/
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers

## SOURCE — Hosting configuration

Canonical `firebase.json` serves `build/web`, rewrites the SPA shell to `/index.html`, and declares `Cache-Control: no-cache, no-store, must-revalidate` for all paths.

This is configuration evidence, not proof of current production response headers or bytes. Firebase Hosting can deploy static content and roll back releases; that capability does not prove that a particular LogMate deployment came from the exact CI-validated artifact.

Sources:
- https://firebase.google.com/docs/hosting/
- https://firebase.google.com/docs/cli

## SYNTHESIS — release evidence chain

`source SHA`
→ `pinned Flutter/toolchain`
→ `canonical build`
→ `generated worker/RESOURCES`
→ `LogMate post-processing`
→ `verifier PASS`
→ `immutable build/web artifact`
→ `same-artifact promotion`
→ `served bytes/headers`
→ `registration/update`
→ `installed/waiting/active worker`
→ `controller`
→ `offline runtime`
→ `local durability`
→ `remote ACK/convergence`.

Every arrow is an independent evidence boundary.

Persistent guards:
- `CI contract committed ≠ CI run passed`;
- `CI run passed ≠ exact artifact retained`;
- `artifact retained ≠ same artifact deployed`;
- `same source rebuilt ≠ same artifact bytes`;
- `firebase.json header policy ≠ served header observed`;
- `worker URL fresh ≠ successor installed`;
- `installed ≠ activated ≠ controlling`;
- `worker current ≠ Cache Storage compatible`;
- `worker current ≠ local data schema current`;
- `offline shell PASS ≠ pending mutation durable`;
- `pending mutation durable ≠ remote ACK/convergence`;
- `Safari tab PASS ≠ Home Screen PASS ≠ managed-iPad PASS`.

## Full-precache consequence

LogMate deliberately changes generated `CORE` to all `RESOURCES`. This increases intended fresh-offline completeness but also increases the number of resources participating in installation/cache population.

The exact Flutter 3.38.7 generated worker must be inspected from a fresh artifact before asserting its complete install-failure semantics for LogMate. The validation question is whether a missing/slow/failed resource prevents successor installation and whether predecessor N remains safely usable while N+1 fails.

`more precache coverage ≠ monotonically better update reliability`.

## MINTTAP / LogMate direction

Artifact identity is part of an EFB acceptance fixture. A physical-device result should record source SHA, workflow/run, Flutter version, artifact identity/hash, deployment/release identity, critical served-byte hashes, worker hash, registration scope/controller state, browser/OS/device mode and scenario result.

“Built from the same commit” is not equivalent to “the same validated artifact” where generated/postprocessed files are part of the assurance claim.

Foreground/open/resume reconciliation remains the portable correctness path. Worker activation or network-online state is not synchronization success.

## Cross-track transfer

**A — Platform/Browser:** own registration, scope, `updateViaCache`, install/wait/activate/control and Cache Storage lifecycle. Keep HTTP cache distinct from Cache Storage.

**B — UX/IA:** a successor can be found/installed while the current client remains on N. Do not label the app “updated” solely from successor discovery. Preserve unsynced local-work semantics across update/reload UX.

**C — Quality:** artifact identity and worker generation become fixture dimensions. Test clean install; N→N+1; one precache resource 404/5xx/slow/interrupted; multiple open clients; terminate while waiting; stale predecessor cache/fresh HTML; offline cold start; storage pressure; Safari tab/Home Screen; physical and managed iPad. Record installing/waiting/active/controller, cache names and critical hashes.

**D — Analytics:** privacy-minimized telemetry may observe release/worker generation and convergence outcome but cannot elect release authority. Do not log sensitive flight payloads or credentials.

**E — Security/Operations:** own immutable promotion, served-byte verification and rollback provenance. Rollback is a new transition and must not silently restore a worker/data contract incompatible with current local state.

## VALIDATION

**V0 fresh CI:** preserve source SHA, run ID, exact Flutter version, artifact ID, recursive inventory/hashes and exact postprocessed worker.

**V1 promotion:** deploy the downloaded validated artifact without rebuild and record release identity.

**V2 served-byte proof:** compare critical deployed files and actual headers with the artifact.

**V3 lifecycle:** on clean and predecessor profiles record registration/scope, `updateViaCache`, worker hash, installing/waiting/active/controller and cache inventory.

**V4 offline/data:** prove cold-start availability separately from IndexedDB/local-record durability, pending-operation retention and foreground rejoin.

**V5 Safari/iPad:** Safari tab and Home Screen on physical iPad; process termination, lock/unlock, airplane mode and long-offline intervals are distinct cases.

**V6 managed EFB:** repeat under representative MDM/network/storage policy.

## OPEN

- Fresh current intended-source DATA-001 successful artifact and exact worker bytes.
- Recursive artifact inventory/hashes.
- Exact generated Flutter 3.38.7 install/cache lifecycle after LogMate patch.
- Proof of no-rebuild promotion of the validated artifact.
- Current deployed response headers and critical served-byte identity.
- Current registration/`updateViaCache`/controller/cache state.
- Current Safari-tab, Home-Screen and managed-iPad results.
- Foreground/resume outbox drainer and ACK/convergence evidence.
- Production authentication/authorization evidence.

## CHANGE WATCH

Flutter generated-worker behavior is toolchain-sensitive and changing in newer Flutter releases. Browser/iPadOS Service Worker behavior and hosting/deployment topology require revalidation on material version or architecture changes.

## Integrated competency

> Offline PWA release assurance is a provenance problem as well as a caching problem. The verified release unit must remain identifiable from source/toolchain through served bytes and controlling worker, while offline/data correctness is tested against that same identity.
