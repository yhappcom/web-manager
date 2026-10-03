# 308 — PWA Flutter Service-Worker Ownership & Offline-Correctness Gate

Status: **PASS (generic/source-level) / LOGMATE BUILD + DEPLOYED-RUNTIME + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-10-03  
Primary owner: **Track A — Web Platform & Browser**  
Security/operations owner for admission/update consequences: **Track E**  
Consumers: Tracks B/C/D

## Why this checkpoint exists

Recent PWA work correctly separated durable local state, remote acknowledgement, credential freshness and background scheduling. A current Flutter platform change materially sharpens that model: current Flutter documentation states that Flutter **no longer generates or manages a caching service worker by default**. Newer builds may write a self-cleaning stub to remove legacy Flutter service workers. Applications requiring offline support or advanced caching must configure their own service worker using standard web tooling or a third-party solution such as Workbox.

This invalidates any generic assumption that a modern Flutter Web build automatically supplies an application-shell caching worker, Background Sync handler, or offline navigation strategy.

## SOURCE

### Flutter current platform contract

Flutter Web initialization documentation states:
- the default build generates `flutter_bootstrap.js`;
- custom initialization can integrate a custom service worker;
- `{{flutter_service_worker_version}}` remains available for custom configurations;
- Flutter no longer generates a service worker by default.

Flutter Web FAQ is stronger: Flutter no longer generates or manages a caching service worker by default; newer versions write a self-cleaning stub to remove legacy service workers. Offline support or advanced caching requires an application-owned service worker.

Flutter 3.41 release notes record the web changes “Self-cleaning service worker” and deprecation of `--pwa-strategy`. This is CHANGE WATCH evidence for the toolchain transition, not proof of the exact output of LogMate's pinned toolchain.

Sources:
- https://docs.flutter.dev/platform-integration/web/initialization
- https://docs.flutter.dev/platform-integration/web/faq
- https://docs.flutter.dev/release/release-notes/release-notes-3.41.0

### Background Sync platform contract

MDN marks Background Synchronization and `SyncManager` as limited availability and secure-context functionality. Periodic Background Sync is additionally experimental and limited availability.

Chrome/Workbox documentation shows a possible Chromium-oriented pattern: failed requests may be stored in IndexedDB and retried on a later `sync` event; Workbox also has a less effective service-worker-start fallback where Background Sync is unsupported. This is an implementation option, not a portable Web guarantee.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API
- https://developer.mozilla.org/en-US/docs/Web/API/SyncManager
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API
- https://developer.chrome.com/docs/workbox/retrying-requests-when-back-online

### WebKit/iPadOS boundary

WebKit supports Service Workers for Home Screen web apps and, since iOS/iPadOS 16.4, Web Push for Home Screen web apps. Those facts do not establish Background Sync support or arbitrary unattended outbox draining.

Sources:
- https://webkit.org/blog/8090/workers-at-your-service/
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/

## LOGMATE SOURCE OBSERVATION

Canonical `yhappcom/logmate` main inspected at commit `31ecf70f5446d49cf6eb8b566e270ac273b37d61`.

Observed:
- `web/index.html` uses the current simple `<script src="flutter_bootstrap.js" async></script>` bootstrap.
- `web/manifest.json` declares `display: standalone`.
- Repository search did not locate a committed custom `flutter_service_worker.js`, `SyncManager`, `periodicSync`, or explicit Background Sync implementation.
- `pubspec.yaml` uses Dart SDK `^3.10.7`; exact Flutter SDK/build output must still be established from canonical build evidence.

These observations do **not** prove the deployed site has no service worker: build/deployment infrastructure could inject or publish artifacts not committed in the application source, and a pinned Flutter version can differ from the newest documented default.

## SYNTHESIS

The correctness model must distinguish:

`manifest/standalone shell ≠ offline application shell`

`Flutter Web build succeeds ≠ caching service worker exists`

`service worker file exists ≠ worker is application-owned/current/controlling`

`service worker controls client ≠ offline navigation works`

`offline navigation works ≠ mutation outbox is durable`

`durable outbox ≠ background scheduling exists`

`Background Sync available ≠ iPadOS portable behavior`

`network restored ≠ worker awakened ≠ operation admitted ≠ ACK received ≠ convergence`

A modern Flutter PWA that materially depends on offline operation therefore needs explicit ownership of its offline runtime contract. The framework build should not be treated as the owner by default.

## MINTTAP DECISION / DIRECTION

For a LogMate-like EFB PWA, **foreground/open/resume reconciliation is the portable correctness path** until physical-device evidence proves stronger platform-specific behavior. Background scheduling may accelerate convergence on platforms that support it, but must not be the only path that can drain pending work.

If offline application-shell availability is a product requirement, the project must explicitly choose and own an offline strategy rather than relying on historical Flutter-generated caching behavior. That ownership includes:
1. worker source and build integration;
2. registration/scope;
3. navigation fallback policy;
4. asset/runtime cache policy;
5. mutation/outbox boundary;
6. worker/application version compatibility;
7. update/rollback and cache invalidation;
8. observability;
9. cross-browser/device validation.

No recommendation is made here to adopt Workbox specifically. That is an engineering choice after requirements and exact build/runtime evidence are established.

## Track transfers

### Track B — UX/IA
The UI must not imply “offline ready” merely because the app can be installed. Distinguish at least local availability, locally saved/pending, checking connectivity/authority, sending, acknowledged and needs-attention states where product semantics require them.

### Track C — Quality
Add contradiction tests for:
- installable/standalone but no service worker;
- service worker registered but no offline navigation;
- shell cached but required runtime/data absent;
- old legacy Flutter worker still controlling after toolchain migration;
- self-cleaning stub encountered after upgrade;
- worker N controlling app N+1 and vice versa;
- pending local operation survives browser/app restart;
- reconnect while app closed vs explicit reopen/resume;
- Chromium Background Sync optimization vs Safari/Home Screen foreground recovery;
- cache deletion/storage pressure/process eviction;
- failed/partial ACK and retry/idempotency.

### Track D — Analytics
Do not infer sync success from `online`, service-worker activation, registration, or sync-event dispatch. Measure product-level acknowledgement/convergence with privacy-minimized telemetry where authorized.

### Track E — Security/Operations
Treat worker ownership as a deployment trust boundary. A stale or unintended worker can mediate navigation/fetch independently of the newly deployed page. Release evidence must identify the controlling worker generation, cache policy and retirement behavior before making offline/update claims.

## VALIDATION ladder

**V0 — canonical build provenance**
- identify exact Flutter SDK used by CI/release;
- run the canonical release build;
- inventory generated `build/web` artifacts;
- record whether a worker/stub is generated and its exact contents;
- identify any deployment-time worker injection/transformation.

**V1 — clean browser**
- fresh origin, no previous worker/cache;
- inspect registrations/controller/scope;
- installability separately from offline navigation;
- offline cold navigation and required-runtime availability.

**V2 — legacy-upgrade**
- install a known prior build with its worker;
- deploy N+1;
- observe update/self-clean/retirement behavior;
- prove old cache cannot silently preserve an incompatible shell indefinitely.

**V3 — mutation/rejoin**
- create unique local work offline;
- close/terminate;
- restore network while closed;
- observe whether any code actually executes;
- reopen/resume and require deterministic drain/adjudication/ACK/convergence.

**V4 — platform**
- Chromium desktop/mobile;
- Safari browser;
- iPadOS Home Screen web app;
- physical iPad with process termination, lock/unlock, airplane mode and long offline intervals.

**V5 — managed EFB**
- representative MDM/network/storage policy;
- repeat V2–V4;
- no unattended-sync guarantee without observed evidence.

## OPEN

- Exact Flutter SDK/build command used by LogMate canonical CI/release.
- Exact generated release artifacts for that pinned version.
- Deployed worker registrations and cache headers.
- Whether any hosting/deployment layer injects a worker.
- Explicit offline shell requirements and chosen ownership.
- Foreground/resume outbox drainer implementation.
- Physical iPad and managed-iPad behavior.
- Production auth/authorization/ACK/convergence semantics.

## CHANGE WATCH

Flutter's service-worker defaults are actively changing. Current documentation and Flutter 3.41 release notes must be rechecked when the project upgrades Flutter. Browser Background Sync/Periodic Sync and iOS/iPadOS web-app capabilities remain platform/version policy CHANGE WATCH.

## Integrated competency

The reusable expert judgment is not “Flutter PWA has a service worker.” It is:

> Framework/toolchain defaults, installability, worker control, offline shell availability, durable mutation state, scheduling, remote admission and convergence are separate evidence claims. A safety-relevant offline PWA must explicitly own and validate each required claim.
