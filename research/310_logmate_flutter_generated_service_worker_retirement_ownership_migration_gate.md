# 310 — LogMate Flutter-Generated Service-Worker Retirement & Ownership-Migration Gate

Status: **PASS (generic + LogMate source-contract) / CUSTOM-WORKER MIGRATION + CURRENT ARTIFACT + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-10-04  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependency owner: **Track A — Web Platform & Browser**  
Consumers: Tracks B/C/D

## Purpose

309 made the exact verified PWA artifact the release unit. This checkpoint adds a more strategic dependency: LogMate's canonical offline pipeline currently post-processes Flutter's generated `flutter_service_worker.js`, while current Flutter guidance says Flutter no longer generates/manages a caching service worker by default in newer versions and applications requiring offline support should configure their own worker.

The EFB requirement therefore cannot remain permanently coupled to an upstream generated-worker format that Flutter is retiring.

## SOURCE — current Flutter direction

Flutter Web FAQ, checked 2026-10-04:
- newer Flutter versions no longer generate/manage a caching service worker by default;
- newer tooling may emit a self-cleaning stub to remove legacy Flutter workers;
- applications requiring offline support or advanced caching are directed to configure a service worker themselves with standard web tooling or a third-party solution such as Workbox.

Flutter web initialization documentation likewise states that Flutter no longer generates a service worker by default and documents custom bootstrap/service-worker integration.

Flutter issue #156910 remains open and describes the phased retirement of `flutter_service_worker.js`: first clean up legacy default workers, then stop generating/loading the default worker so applications can own their caching policy.

Sources:
- https://docs.flutter.dev/platform-integration/web/faq
- https://docs.flutter.dev/platform-integration/web/initialization
- https://github.com/flutter/flutter/issues/156910

## SOURCE — LogMate canonical dependency

Canonical `yhappcom/logmate` main inspected at `31ecf70f5446d49cf6eb8b566e270ac273b37d61`.

`Makefile`:
- `build-pwa` and `build-pwa-acceptance` both run `flutter build web`;
- both then run `tool/precache_flutter_web.dart` and `tool/verify_pwa_artifact.dart`.

`tool/precache_flutter_web.dart`:
- requires `build/web/flutter_service_worker.js`;
- exits if the generated worker is absent;
- pattern-matches Flutter's generated `CORE` and query-handling source;
- converts `CORE` to all `RESOURCES` and patches query/cache matching.

`tool/verify_pwa_artifact.dart`:
- requires `flutter_service_worker.js`;
- requires LogMate post-processing markers and required resource keys.

Therefore the present offline build contract has an explicit toolchain-format dependency:

`Flutter-generated worker exists and has expected structure → LogMate patch succeeds → verifier can pass`.

## CONTRADICTION / dependency debt

309 correctly treated the generated+postprocessed worker as application-owned release behavior for the pinned toolchain. That does **not** imply the generated worker is a durable upstream API.

Current Flutter platform direction deliberately removes that default. Therefore:
- `Flutter 3.38.7 pinned ≠ generated-worker contract permanent`;
- `postprocessor fail-closed ≠ migration strategy`;
- `current offline build PASS ≠ future Flutter upgrade ready`;
- `Flutter upgrade succeeds for Dart/UI ≠ PWA offline pipeline survives`;
- `self-cleaning Flutter stub emitted ≠ LogMate offline cache preserved`.

The fail-closed postprocessor is valuable because a future generated-format removal/change should break the build rather than silently ship an unverified offline artifact. But that is a detection control, not lifecycle ownership.

## SYNTHESIS — ownership migration

For an EFB-like offline requirement, Service Worker behavior is product infrastructure, not a disposable framework default. Long-term ownership should move from:

`Flutter generated worker → textual LogMate patch → marker verifier`

toward:

`LogMate-owned worker source/config → explicit precache manifest generation → deterministic worker build → semantic/static verifier → browser/device runtime acceptance`.

This checkpoint does **not** select Workbox or another implementation. Tool choice belongs to implementation validation with Software Engineering. The web requirement is stable ownership of offline/update semantics independent of Flutter's deprecated default-worker generator.

## Upgrade gate

A Flutter upgrade must not be approved solely because compilation/tests succeed. For every candidate toolchain:

1. determine whether Flutter emits a caching worker, cleanup stub, or no worker;
2. verify bootstrap registration behavior;
3. build the normal product artifact;
4. verify the intended LogMate-owned worker/cache contract;
5. test clean install and N→N+1 from the currently deployed generation;
6. test legacy-worker cleanup/migration without destroying IndexedDB/local ledger/outbox;
7. test offline cold start after upgrade;
8. test rollback as a new transition rather than assuming old worker/cache state is restored;
9. repeat Safari tab/Home Screen and representative managed-iPad acceptance before EFB promotion.

A cleanup worker must be treated as a state transition with explicit evidence. Unregistering/replacing a Service Worker and deleting its caches does not establish backup, local-data migration, session correctness or synchronization convergence.

## Cross-track transfer

**A — Platform/Browser:** own registration/scope/update/control and legacy-worker replacement mechanics. Distinguish Service Worker registration, Cache Storage and IndexedDB/local durable data.

**B — UX/IA:** framework/toolchain migration must not surface as unexplained offline loss or destructive reset. Update/recovery states must preserve unsynced local work.

**C — Quality:** add toolchain generation and worker-ownership mode to fixtures. Required transition classes include generated-worker N → owned-worker N+1, legacy cleanup, failed successor install, rollback, offline cold start and physical Safari/Home Screen.

**D — Analytics:** migration telemetry may observe worker/release generations and failures but cannot establish data durability or sync authority.

**E — Security/Operations:** own the deprecation watch, upgrade gate, immutable artifact provenance, migration/rollback plan and retirement of legacy worker/cache authority.

## VALIDATION

**V0 current artifact:** preserve exact Flutter 3.38.7 generated/postprocessed worker and bootstrap bytes.

**V1 prototype ownership:** Software Engineering produces an owned-worker candidate without changing product authority/data semantics.

**V2 differential:** compare resource inventory, navigation handling, install/update/cache cleanup and offline behavior against the pinned current artifact.

**V3 transition:** exercise current generated worker → owned successor with open clients, offline local data and pending work.

**V4 failure/rollback:** successor install failure, activation failure, partial cache population and rollback must preserve unique local data and avoid obsolete remote authority.

**V5 Apple:** Safari tab + Home Screen on physical iPad; then representative managed-iPad policy/network/storage conditions.

## OPEN

- Exact Flutter 3.38.7 generated worker/bootstrap bytes from a fresh normal artifact.
- Exact Flutter version at which LogMate's present pipeline first fails or receives a cleanup stub.
- Choice/design of LogMate-owned worker implementation.
- Deterministic precache-manifest/build approach.
- Generated-worker → owned-worker transition evidence.
- Cache retirement without local IndexedDB/outbox loss.
- Current physical/Home-Screen/managed-iPad runtime evidence.
- Production authentication, synchronization and convergence evidence.

## CHANGE WATCH

Flutter's generated Service Worker is explicitly being retired. Treat every Flutter upgrade as a PWA architecture change until LogMate owns its worker contract independently.

WebKit/iOS/iPadOS Service Worker behavior remains version-sensitive and requires device validation.

## Integrated competency

> A fail-closed patch over a framework-generated Service Worker can be a sound pinned release contract, but it is not durable architecture when the framework is retiring that generator. For an offline EFB, the worker/cache policy must become an explicitly owned, migration-tested product contract before toolchain evolution can be considered routine.
