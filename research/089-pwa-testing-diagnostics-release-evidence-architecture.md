# 089 — PWA Testing, Diagnostics & Release Evidence Architecture

Status: **PASS (generic evidence architecture) / TARGET-DEVICE EXECUTION OPEN**  
Date: 2026-09-17

## Purpose
Convert the PWA failure/recovery models in 083–088 into an executable evidence system without confusing Chromium automation with Safari/iPad validation. The highest-value bottleneck is now Track C quality/validation consuming Track A mechanics and Track E recovery/security invariants.

## Integrated model
`release candidate → deterministic fixtures → browser automation → fault injection → lifecycle/storage assertions → accessibility/degraded-state assertions → target-device execution → privacy-minimized diagnostic bundle → acceptance/rejection → retained evidence`

## SOURCE — current tooling and standards boundaries
- Playwright documents service-worker inspection/routing as Chromium-only. It can enumerate workers, wait for activation, identify worker-owned requests and determine whether a response came from a service worker. Therefore it is useful for deterministic lifecycle/network diagnostics but cannot establish Safari/WebKit service-worker correctness.
- Playwright network routing can miss requests intercepted by service workers; its own guidance notes that blocking service workers changes behavior. Tests that disable workers are useful control tests, not evidence for the installed/offline product path.
- WebKit documents separate WebContent, Network and Storage processes; IndexedDB/Service Worker storage sits behind the StorageProcess. Web Inspector can attach to service workers and inspect fetch/postMessage/cache behavior. This supports engine-specific diagnosis but not unattended managed-iPad acceptance by itself.
- W3C Service Workers remained a Candidate Recommendation Draft with repeated publications through 2026-08-12. Exact implementation behavior remains CHANGE WATCH.
- Design Studio Web evidence is Stage 3 PRACTICE / NOT PASSED and explicitly lacks Safari, physical-device, screen-reader and human-UX PASS; those claims cannot be imported from design artifacts.

## SYNTHESIS — four evidence tiers
### Tier 1 deterministic unit/protocol tests
Pure logic: schema migrations, cache-key/version selection, outbox idempotency, conflict resolution, diagnostic redaction. Fast and broad, but no browser-runtime claim.

### Tier 2 browser automation
Use Chromium automation for reproducible service-worker lifecycle, routing, cache/network failures, update generations and accessibility state-machine checks. Run independent browser engines for ordinary page behavior where tooling permits. Chromium worker automation must be labeled Chromium evidence.

### Tier 3 engine/device diagnostics
Safari/WebKit execution verifies Safari-specific lifecycle/storage/navigation behavior. Simulator evidence is not physical-device/MDM evidence. Preserve OS/browser/build/device/container/network conditions.

### Tier 4 product acceptance
Exact production-like artifact on managed EFB iPad plus native-phone counterpart where synchronization is involved. Include real MDM/VPN/proxy/content-filter/network topology and interruption/recovery scenarios. Only this tier can close LogMate EFB product feasibility claims.

Guard: `automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.

## Canonical failure-injection matrix
Every release path affecting PWA state should select applicable cases from:
1. hard offline cold start;
2. hard offline deep link;
3. DNS/connectivity present but origin blackholed/timeout;
4. partial asset/API failure;
5. corrupt/missing reconstructible cache;
6. old shell + new worker;
7. new shell + old schema;
8. waiting worker with active old client;
9. takeover/reload interruption;
10. schema migration interrupted by process termination;
11. pending authoritative outbox during update;
12. duplicate retry after lost acknowledgement;
13. server rejection after offline mutation;
14. N→N+k skipped-version return;
15. storage pressure/eviction of reconstructible state;
16. device/process restart before sync acknowledgement;
17. network switch/VPN/proxy change during transport;
18. server rollback while newer installed client remains;
19. inaccessible degraded/update/recovery status;
20. diagnostics unavailable because the client itself is offline/broken.

For each case record: precondition/generations, injected fault, user-visible state, authoritative-record preservation, pending outbox, network/cache source, migration result, acknowledgement/reconciliation, recovery path, accessibility assertions and evidence artifact.

## Release acceptance invariants
A PWA release touching worker/cache/schema/sync is rejected when any applicable invariant fails:
- authoritative local record survives reconstructible-cache loss;
- pending mutation is never represented as remotely acknowledged;
- retries are idempotent or explicitly reconciled;
- unsupported generation combinations fail safely rather than silently corrupting data;
- migration interruption has a bounded restart/recovery path;
- destructive site-data clearing is not the routine recovery path for unsynchronized records;
- offline/degraded/update states remain operable and understandable without color-only or transient-only communication;
- diagnostics do not require collecting record contents to identify worker/shell/schema/network/recovery state;
- absence of telemetry from an offline/broken client is not counted as successful health evidence.

## Diagnostic bundle contract
Support-safe diagnostics should prefer structural metadata:
- app/build/release ID;
- worker script/generation and lifecycle state;
- shell/cache schema generation;
- local DB schema generation;
- outbox count/state categories, not flight-record content;
- last attempted/acknowledged sync timestamps where justified;
- navigation source class: network/cache/preload/offline fallback/error;
- migration/recovery outcome code;
- storage persistence/quota estimate when available and relevant;
- browser/OS/container class and connectivity class;
- correlation/run ID generated for the diagnostic event.

Do not collect record payloads, crew names, route details or stable identifiers merely to diagnose worker/cache/version state. Any production telemetry requires privacy/security review and explicit retention/access rules.

## Test oracle discipline
A test is weak when it asserts only that a page rendered or a request returned 200. PWA oracles should assert state transitions and data invariants. Examples:
- `saved locally` requires durable local commit evidence;
- `synced` requires remote acknowledgement/reconciliation evidence;
- `updated` requires compatible controlling generation, not only worker installation;
- `offline ready` requires required task routes/data to work after network removal;
- `recovered` requires authoritative records/outbox preserved and task readiness restored.

## Cross-track transfer
- **A Platform/Browser owns** lifecycle/cache/storage/network mechanics and engine-specific evidence labels.
- **B UX/IA consumes** state truth to specify local-only, pending, conflict, update-required, degraded and recovery-required user states.
- **C Quality owns this testing architecture**, accessibility assertions, fault injection and evidence classification.
- **D Analytics consumes** privacy-minimized health signals but cannot use missing telemetry as durability proof.
- **E Architecture/Operations consumes** acceptance invariants, release lineage, rollback/forward-fix and incident diagnostic bundles.

## Software Engineering handoff
Implementation should produce an executable matrix keyed by release/build and exact artifact. Required engineering outputs include deterministic fixtures for DB/outbox generations, scripted network/storage/process faults where platform tooling permits, retained raw results, and physical managed-iPad runs for Safari/EFB claims. Web Manager does not prescribe the test framework beyond evidence requirements.

## Design Studio dependency
Design Studio owns actual visual/interaction treatment. Web acceptance requires the truthful semantic states and accessibility behavior; current Design Studio evidence does not yet close Safari/AT/physical-device/human validation.

## OPEN / VALIDATION
- exact Safari remote-inspection capabilities for the managed company iPad configuration;
- whether MDM permits required inspection/log/export workflows;
- exact automated Safari/WebKit coverage available in the product CI environment;
- real storage-pressure and process-termination reproducibility on target iPadOS;
- exact LogMate worker/cache/schema/outbox implementation;
- privacy/legal approval for any production diagnostic telemetry.

## CHANGE WATCH
- Service Worker specification and WebKit fixes;
- Safari/iPadOS Web Inspector and Home Screen Web App behavior;
- Playwright worker support (currently Chromium-specific);
- managed-device policies affecting inspection, storage, networking and export.

## Competency checkpoint
PASS at generic architecture level: testing now has explicit evidence tiers, failure matrix, release invariants, diagnostic minimization, engine boundaries and product handoff. Product validation remains OPEN until exact managed-iPad execution exists.

## Sources
- Playwright Service Workers and Network documentation, accessed 2026-09-17.
- WebKit Workers at Your Service; Debugging WebKit / Web Inspector documentation, accessed 2026-09-17.
- W3C Service Workers publication history, latest listed Candidate Recommendation Draft 2026-08-12, accessed 2026-09-17.
- `yhappcom/design-studio` Web Design status, checked 2026-09-17.