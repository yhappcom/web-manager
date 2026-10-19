# 424 — Stage 8 PWA URL Authority and Release Compatibility

Date: 2026-10-20. Owner: Track E; Track A/C prerequisites; B/D transfer. Baselines: web-manager main e6eebb396d1dbb7646c780202d45da97c54bc8f5; LogMate main 6101666530cb706a042ac82614c840af441895b1 (read-only). Stage 8 active; production/browser/managed-iPad validation OPEN; PWA release HOLD.

## SOURCE
- WHATWG URL: https://url.spec.whatwg.org/
- W3C Service Workers: https://w3c.github.io/ServiceWorker/spec/service_worker/
- Firebase Hosting reserved URLs: https://firebase.google.com/docs/hosting/reserved-urls
- MDN Cache.match: https://developer.mozilla.org/en-US/docs/Web/API/Cache/match
- LogMate generator: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/tool/pwa_precache.dart
- Design Studio W121 and Engineering M006/Q006 remain bounded transfer evidence; Marketing 438 keeps PWA ads on HOLD.

## SYNTHESIS
Service Worker URL classification, parsed URL spelling, HTTP server resolution and version-pinned cache identity are distinct layers. A verified manifest asset is protected only if the complete route policy prevents unknown executable paths from silently falling through to a different release. Network-only API, authentication and reserved Firebase requests require separate classification before client-version lookup. Query handling must be explicitly specified rather than inferred from Cache API defaults.

## VALIDATION
Exact historical Acceptance ZIP SHA-256 d267bf9a4e8c30b1e40cf8133bdee3acf3e1dfa9cb3937da7b4d009da0180160; Worker SHA-256 4da9ae8bc6797c478946f3e661487c1ff0e547ad21239930a5912b6fa41d083b. Node 22 VM executed 34 behavioral checks; all matched expected Worker decisions. A separate illustrative classifier model passed 17 design assertions. Local Python HTTP alias probe met 5 expected results; five deliberately altered Worker variants were all rejected by the test oracle. These are bounded synthetic and local-server results, NOT Firebase Hosting, Chromium, Safari, physical iPad or production PASS. The historical archive contains 952 manifest resources and is missing one previously documented required hidden file; current normal build remains unavailable.

## MINTTAP DECISION (PROPOSED, NOT SHIPPED)
Define one reviewed URL-to-release authority policy: distinguish reserved/auth routes, explicit network-only APIs, root navigation, version-bound static/executable resources and unknown paths; prevent unknown executable requests from crossing verified release boundaries; do not equate arbitrary URL decoding with canonicalization. Require exact served-byte and route-behavior verification before any release claim. Preserve flight records, pending edits, outbox and independent backup through every repair path.

## DEPENDENCY / TRANSFER
Track E owns route/release trust and Hosting operations; A supplies URL parsing, scope and Service Worker client semantics; C owns actual browser/Hosting negative tests, performance and accessibility; B specifies recoverable offline/auth UX using Design Studio evidence; D owns privacy-safe diagnostics and truthful discoverability claims. Software Engineering owns implementation and CI integration. No track duplicates another specialist's foundational discipline.

## VALIDATION / OPEN / CHANGE WATCH
Next gate: current normal PWA build and CI artifact, exact Worker/manifest/bootstrap agreement, Firebase Hosting Emulator and deployed-byte parity, old/new-client executable routing, Chromium/Safari update/offline behavior, then physical/managed iPad and independent logbook backup/restore. Production facts, actual Firebase URL resolution, iPad storage and PWA-native Sync remain OPEN. Watch WHATWG URL, W3C Worker, Firebase Hosting, WebKit and Flutter changes. Stop further synthetic URL variants until real runtime evidence becomes available.
