# 088 — PWA Offline Navigation, Service-Worker Update Recovery & Observability

Status: **PASS — generic cross-track recovery architecture / PRODUCT VALIDATION OPEN**  
Date: 2026-09-17

## Purpose
Move beyond the completed direct-transport primer and address the next high-consequence PWA gap: an installed application can have a network connection, an offline cache, and a registered service worker yet still fail to produce a usable navigation or recover cleanly after an update. This study integrates Track A browser mechanics, Track B degraded-state UX, Track C resilience/accessibility/quality, Track D bounded telemetry, and Track E deployment/recovery operations.

## 1. History and problem
HTML AppCache attempted declarative offline application caching. WebKit's historical release notes explicitly describe Service Workers as its successor, centered on programmable resource loading without network access. The successor is more capable but transfers correctness responsibility to application code: routing, cache population, update activation, compatibility and fallback behavior become an application lifecycle problem rather than a manifest-only feature.

**SOURCE:** WebKit Safari Technology Preview 46 (2017) identifies Service Workers as successor to Offline Application Cache.

## 2. Navigation availability is a state machine, not `navigator.onLine`
A navigation may encounter at least these independent states:
- network unavailable;
- network technically connected but stalled/captive/unusable;
- service worker absent or registration lost;
- worker boot/activation delay;
- requested route not cached;
- shell cached but required data absent;
- stale shell incompatible with current local schema/data;
- network response succeeds but is semantically unusable;
- cached response exists but is corrupt/stale/incompatible;
- worker fetch handler throws or returns no valid response.

Therefore:
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.

**SOURCE:** Chrome Workbox documents network-first timeout/fallback specifically for connections that exist but are too slow or effectively unusable. This is Chromium/tooling-specific guidance, not a Web standard requirement.

## 3. Service-worker update lifecycle
The generic lifecycle remains:
`update check → new script differs → install → waiting while old controlled clients remain → activate → control eligible clients`.

MDN documents that a newly installed worker normally waits until pages using the previous worker are gone. `Clients.claim()`/`skipWaiting()` can accelerate control transitions, but immediate takeover is not equivalent to safe takeover when page code, cached assets, IndexedDB schema or protocol semantics changed.

`new worker available ≠ activated ≠ controlling this client ≠ compatible with this client/data`.

**SOURCE:** `ServiceWorkerRegistration.update()` attempts a worker update and installs a byte-different script. `updateViaCache` controls whether the HTTP cache participates in update script fetching. These are update mechanics, not application compatibility guarantees.

**CHANGE WATCH:** W3C Service Workers continues active Candidate Recommendation Draft publication; publication history includes 12 August 2026. Stable mental models should be retained while exact specification/platform behavior remains freshness-sensitive.

## 4. Cache ownership and compatibility
Separate cache classes:
1. immutable/versioned static assets — reconstructible;
2. navigation/app shell — reconstructible but version-sensitive;
3. runtime fetched reference data — possibly reconstructible, freshness-sensitive;
4. irreplaceable user records — must not be treated as Cache Storage shell assets;
5. pending mutation/outbox state — durable transactional application data, not merely response cache.

Cache deletion during `activate` is safe only when the application knows no still-valid client/data path requires that cache. A cache name change is not itself a migration protocol.

**SYNTHESIS:** aggressive cleanup plus immediate worker takeover can create a split-generation failure: an old page executes against a new worker/new cache contract, or a new shell opens against old local schema. Version compatibility must be explicit.

## 5. Navigation preload
Navigation Preload can begin a navigation network request in parallel with service-worker startup and expose it through `FetchEvent.preloadResponse`. MDN marks the mechanism widely available and documents feature detection through `registration.navigationPreload`.

It can reduce worker-start navigation delay, but:
`navigation preload ≠ offline fallback ≠ cache correctness ≠ update recovery`.

If preload and ordinary responses vary, server/cache semantics such as `Vary: Service-Worker-Navigation-Preload` matter.

## 6. Safe update contract for long-offline clients
For an EFB-like client returning after a long offline interval:
`identify client/worker/shell/schema/protocol generation → preserve irreplaceable local records/outbox → determine supported migration path → stage new reconstructible assets → migrate/bridge schema transactionally → activate compatible worker/shell → replay pending operations idempotently → reconcile → retire obsolete caches only after compatibility proof`.

Do not require every historical client to upgrade directly forever. Define a bounded compatibility window and an explicit recovery path for versions outside it.

**DEPENDENCY — Software Engineering:** executable schema migration, worker/cache implementation, rollback/forward-fix and target-device lifecycle tests.

## 7. Recovery hierarchy
A PWA must distinguish recoverable layers.

1. **network retry** — transient transport failure;
2. **cached navigation fallback** — valid compatible shell/page exists;
3. **generic offline/degraded route** — requested content unavailable but application can explain status/actions;
4. **worker update/reload** — safe only when local data is preserved and compatibility is established;
5. **cache reconstruction** — only reconstructible assets;
6. **application data migration/reconciliation** — preserve records/outbox;
7. **independent restore/import** — when local application state is damaged/lost;
8. **support/escalation** — when automatic recovery cannot establish data safety.

`clear site data` is not a generic troubleshooting step for an application containing unsynchronized irreplaceable records.

## 8. Observable state model
Operational telemetry should distinguish, without collecting unnecessary record contents:
- client build/shell generation;
- active/waiting worker generation;
- schema/protocol generation;
- navigation outcome: network/cache/preload/offline fallback/error;
- cache-miss/fetch-failure category;
- migration start/success/failure;
- pending outbox count or bounded state indicator;
- last remote acknowledgement/reconciliation state;
- backup freshness/verification state where product policy permits;
- recovery action/outcome.

**Track D boundary:** analytics may reveal aggregate failure frequency but cannot prove individual durability. Telemetry design must minimize identifiers and record content.

**Track E boundary:** absence of telemetry from an offline/broken client is not evidence of absence of failure. Client-local diagnostic evidence and support-safe export may be required.

## 9. Accessible degraded/update/recovery UX
The UI must communicate the state that matters to the user's task rather than internal worker jargon.

Required semantic distinctions include:
- available offline and safe to continue;
- viewing cached/stale reference content;
- changes saved only on this device;
- synchronization pending/failed;
- update available but deferred because work/data must be preserved;
- update/recovery requires restart/reload;
- requested content unavailable offline;
- recovery could affect local unsynchronized data — destructive action prohibited without explicit evidence/backup.

Status must not rely on color alone. Focus, keyboard/touch reachability, reflow/zoom, live status announcements where appropriate and recovery-action ordering require Design Studio + accessibility validation.

**DEPENDENCY — Design Studio:** latest Web Design status remains Stage 3 PRACTICE; no Safari, cross-browser, screen-reader, physical-device or human-UX PASS is transferable.

## 10. Safari/WebKit vs Chromium evidence boundary
- Core Service Worker lifecycle/update semantics are standards-based and broadly implemented.
- Workbox strategy/timeouts are Chromium ecosystem tooling/pattern evidence, not Safari behavior guarantees.
- Safari/WebKit continues shipping service-worker bug fixes; Safari 26.6 (27 July 2026) includes service-worker fixes, demonstrating that implementation details remain CHANGE WATCH.
- Historical WebKit statements about quotas/registration cleanup must not be promoted to current policy without current evidence.

**VALIDATION:** target Safari/iPadOS Home Screen behavior must be exercised on the exact managed device/artifact before product acceptance.

## 11. Failure injection matrix
Software Engineering acceptance should inject at least:
- first launch online then hard offline navigation;
- deep-link navigation offline to cached and uncached routes;
- network connected but blackholed/high-latency;
- worker install succeeds but activation waits;
- immediate takeover attempt with old page open;
- old shell + new worker;
- new shell + old schema;
- migration interruption/process termination;
- missing/corrupt reconstructible cache;
- outbox pending during update;
- long-offline N → N+k return inside and outside compatibility window;
- server rollback while newer worker/client exists;
- cache purge/origin deploy mismatch;
- storage pressure/removal of reconstructible cache;
- reload/restart after recovery;
- accessibility checks on every degraded/recovery state.

For every case preserve: artifact/build ID, OS/browser/container, worker generation, cache/schema generation, network condition, local-data checksum/count where safe, visible user state, recovery action and final data/sync outcome.

## 12. Acceptance invariants
A recovery design does not PASS merely because the home screen renders. Require:
- no acknowledged user record silently disappears;
- no unsynchronized local record is destroyed by routine update/recovery;
- stale UI does not falsely claim remote synchronization/backup;
- incompatible client/schema/protocol combinations fail boundedly rather than corrupting data;
- reconstructible cache can be rebuilt without erasing authoritative local records;
- user can distinguish offline/cached/local-only/synced/recovery-required states;
- recovery remains operable under accessibility requirements;
- exact target-device evidence exists for Safari/iPadOS claims.

## 13. Cross-track synthesis
- **A owns:** worker lifecycle, fetch/cache/navigation preload and browser implementation distinctions.
- **B consumes:** converts runtime states into task-safe offline/update/recovery IA and language.
- **C consumes:** failure injection, performance, accessibility, cross-browser/device evidence and regression gates.
- **D consumes:** minimized navigation/update/recovery telemetry and measurement limits.
- **E owns operational integration:** version compatibility, deployment/cache policy, recovery hierarchy, incident diagnostics and data-safety gates.

Track E remains highest-consequence owner, but the next closure evidence is implementation/device validation rather than more generic primer work.

## 14. Expert judgment for LogMate/EFB
A long-offline flight-record PWA should be designed as a durable local application whose web shell is reconstructible. Offline navigation and update convenience are subordinate to record preservation. A worker/cache recovery action that risks unsynchronized flight records is unacceptable even if it restores UI availability faster.

Do not claim production feasibility until exact managed-iPad tests demonstrate worker/update/cache behavior, schema migration, offline navigation, record/outbox preservation, accessible recovery and independent restore.

## Sources / freshness
- W3C Service Workers publication history — Candidate Recommendation Draft through 2026-08-12.
- MDN `Using Service Workers`, `ServiceWorkerRegistration.update()`, `updateViaCache`, `NavigationPreloadManager`, `FetchEvent.preloadResponse` — accessed 2026-09-17.
- WebKit, `Release Notes for Safari Technology Preview 46` — historical AppCache→Service Worker context.
- WebKit, `WebKit Features for Safari 26.6`, 2026-07-27 — current implementation change-watch.
- Chrome for Developers / Workbox, network timeout strategy — Chromium ecosystem failure-pattern evidence only.
