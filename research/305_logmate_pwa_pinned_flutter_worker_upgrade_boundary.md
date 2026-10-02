# 305 — LogMate PWA Pinned Flutter Worker Contract & Upgrade Boundary

Status: **PASS (source/contract correction) / EXACT BUILD + RUNTIME + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**
Date: 2026-10-02
Primary owner: **Track E — Web Architecture, Security & Operations**
Dependencies: **A Platform/Browser**, **C Performance/Accessibility/Quality**
Consumes: **304 — LogMate PWA Auth Restoration Production-Adapter Gap & V1 Implementation Handoff**

## SOURCE

Canonical LogMate main is `2bd07b0129c55fdb956adbbd3e007963b0e77c5b`. Its `tool/precache_flutter_web.dart` expects the legacy generated Flutter caching-worker structure: `RESOURCES`, a generated `CORE` array, version-query normalization, install/activate caches and cache matching. It changes CORE to all RESOURCES, broadens query normalization and changes matching to ignore search parameters. `tool/verify_pwa_artifact.dart` requires those post-processing markers.

The exact upstream Flutter 3.38.7 tag still contains that legacy caching-worker template at `packages/flutter_tools/lib/src/web/file_generators/js/flutter_service_worker.js`. It contains RESOURCES/CORE, install TEMP precache, activation revision comparison, version-query normalization, resource lookup, online-first root navigation, cache population, skipWaiting messaging and downloadOffline.

Current Flutter documentation now states that newer Flutter versions no longer generate/manage a caching service worker by default and may emit a self-cleaning stub; applications needing offline/advanced caching should configure their own worker.

## CORRECTION

A prior broad conclusion treated Flutter's newer self-cleaning-worker direction as if it already described LogMate's pinned Flutter 3.38.7 build contract. That is too strong.

Correct boundary:

`pinned Flutter 3.38.7 worker source is structurally compatible with LogMate post-processing != future Flutter upgrade preserves that contract`.

Therefore the current worker patch is not source-failed merely because newer Flutter changed direction. Exact build execution remains OPEN. A Flutter upgrade that changes worker generation is a separate migration gate.

## SYNTHESIS

The current worker has three distinct freshness mechanisms that must not be collapsed:

1. source/build bytes become generated RESOURCES revisions;
2. successor-worker activation compares old and new revisions and replaces changed resources;
3. query normalization controls resource classification/cache matching but is not itself revision authority.

Guards:
- query version changed != generated resource revision changed;
- query ignored during matching != resource revision invalidation absent;
- generated worker source compatible != canonical build PASS;
- worker active != current document/data/auth generation converged;
- pinned-toolchain PASS != upgrade-toolchain PASS.

LogMate's current `?v=logmate-temp-v1` icon URLs therefore cannot be evaluated from query semantics alone. Icon bytes, generated RESOURCES revisions, worker activation/cache migration and installed-OS representation are separate evidence boundaries.

## MINTTAP DECISION

Keep the present 3.38.7 generated-worker path as a bounded pinned-toolchain compatibility adapter until executable evidence says otherwise. Do not force a worker rewrite solely because newer Flutter changed defaults.

Before any Flutter upgrade crossing the generated-worker behavior change:
- freeze exact old/new Flutter revisions;
- build both artifacts;
- diff worker/bootstrap generation;
- classify removed/changed cache semantics;
- choose an explicit application-owned offline worker contract rather than patching an unknown/self-cleaning template;
- execute N to N+1 and rollback tests before release.

Application-owned service-worker architecture remains the preferred long-term direction once leaving the legacy generated-caching contract; implementation shape belongs to Software Engineering.

## VALIDATION

V0:
1. execute canonical `make build-pwa` under exact Flutter 3.38.7;
2. preserve Flutter/Dart revision, final worker hash and RESOURCES map;
3. resolve the independent local-font/verifier filename contradiction before promotion.

V1:
4. test bytes-only, query-only and bytes-plus-query resource changes;
5. observe installing/waiting/active/controller independently;
6. inspect Cache Storage before and after N to N+1;
7. verify root navigation with application query state online and offline;
8. verify missing static resources are not masked as successful SPA documents.

V2+:
9. deployed-origin direct-network versus worker-controlled responses;
10. partial deployment and rollback;
11. physical Safari/Home-Screen iPad fresh-install and existing-install update;
12. representative managed-EFB lifecycle.

## TRACK TRANSFERS

A owns exact worker lifecycle/cache mechanics and Flutter CHANGE WATCH. B consumes the result for update/offline/recovery states. C owns executable build/browser/iPad evidence. D must not treat telemetry as release authority. E owns pinned-toolchain provenance, upgrade admission and rollback boundaries.

## OPEN

Exact canonical 3.38.7 build output; actual generated RESOURCES map; font/verifier reconciliation; deployed-origin behavior; current physical Safari/Home-Screen evidence; representative managed-company-iPad evidence.

## Integrated competency

Framework-current documentation and product-pinned behavior can legitimately differ. Expert release judgment binds claims to the exact toolchain and artifact, treats upstream direction as a migration signal rather than retroactive product fact, and requires a new gate when the toolchain crosses that boundary.
