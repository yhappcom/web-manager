# 421 — Stage 8 PWA Catalogue Integrity, Growth and Safe Retirement

**Date:** 2026-10-20. **Owner:** Track E; Track A/C dependencies; B/D transfer. **Canonical baseline:** web-manager main 2efec4bae7c5dcac732569f4690c04aeb15a8990; LogMate main 6101666530cb706a042ac82614c840af441895b1 (read-only). **Gate:** bounded exact archived Worker Node VM; current normal PWA/browser/iPad and production OPEN; PWA release HOLD.

## SOURCE
- Current generator: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/tool/pwa_precache.dart
- W3C Service Workers: https://www.w3.org/TR/service-workers/
- WHATWG Storage: https://storage.spec.whatwg.org/
- MDN Clients.matchAll: https://developer.mozilla.org/en-US/docs/Web/API/Clients/matchAll
- WebKit storage: https://webkit.org/blog/14403/updates-to-storage-policy/
- Prior research: 324 Fetch policy, 415 archive failure, 420 repair/status cost.
- Design Studio W121: https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md
- Engineering M006/Q006: generic browser and CI verdict transfer only; Marketing 438: PWA ads HOLD.

## HISTORY / PRINCIPLE / SOURCE-LEVEL IMPLEMENTATION
AppCache's lifecycle limitations motivated programmable Service Workers. LogMate's owned Worker stores full manifests in a mutable Cache Storage JSON catalogue and records both pre-navigation and resulting client IDs for root navigations. Each navigation rewrites the full catalogue. The source has no client-ID, release-manifest or cache-retirement procedure. Per-Worker Promise serialization is not cross-Worker atomicity. On invalid JSON/schema, readControl silently returns emptyControl, and the next root navigation can overwrite previously recoverable metadata. The executable Shell cache remains separate from this control JSON; data records and independent backup remain separate again.

## VALIDATION — historical exact Worker, bounded Node 22 VM
Fixture: historical Acceptance archive SHA-256 d267bf9a4e8c30b1e40cf8133bdee3acf3e1dfa9cb3937da7b4d009da0180160; unmodified Worker SHA-256 4da9ae8bc6797c478946f3e661487c1ff0e547ad21239930a5912b6fa41d083b. Synthetic Cache Storage, client IDs, versions and quota were injected. These are not real-browser results.

| Scenario | Observation |
| --- | --- |
| One full release manifest | 250259 bytes; initial control JSON 250473 bytes |
| 200 unique synthetic navigations | 400 mappings retained; control JSON 268456 bytes |
| Twelve additional synthetic release manifests | 13 versions; control JSON 3272038 bytes |
| 20 navigations with one version | 5026372 total serialized control-write bytes |
| 20 navigations with 13 versions | 65126900 total serialized control-write bytes |
| Invalid JSON, schema mismatch, missing versions or clientBuilds | Each root navigation returned 503 and replaced catalogue with 120-byte empty state; Shell bytes remained cached |
| Valid schema with stale currentBuildId | 503; stale pointer persisted |
| Injected catalogue write quota | QuotaExceededError; not a measured browser quota |

Repeated navigations are one load experiment, not hundreds of distinct product tests. Logical serialized bytes are not physical writes, latency, energy or on-device storage. The actual frequency of distinct browser IDs and number of retained releases remain unknown. Chromium 144 local navigation was blocked by environment policy: NON-EXECUTION.

## SYNTHESIS / CONTRADICTION
Protecting all old caches against premature deletion creates a separate obligation to retire obsolete catalogue state safely. Full manifest copies multiplied by release count amplify every root-navigation catalogue rewrite. Silent metadata reset can make a verified cached Shell unreachable, without proving loss of user logbook records. A one-time clients.matchAll snapshot is insufficient proof that no in-flight or uncontrolled client needs a version. Cache eviction, record durability, independent .lbk restore and Sync ACK must never be conflated.

## MINTTAP DECISION (PROPOSED; NOT SHIPPED)
1. Separate immutable per-release verified manifests from small mutable pointers/client pins. Evaluate IndexedDB short atomic transactions for cross-Worker registry changes; never hold them over network fetch or long hashing.
2. Distinguish first install from corrupted existing catalogue. Preserve malformed bytes for recovery evidence and fail into CATALOG_RECOVERY_REQUIRED; never silently elect a new release or overwrite established metadata with emptyControl.
3. Preserve current/candidate/previous verified generations and live/in-flight pins until a tested retirement boundary. Do not delete owner records/outbox, clear the origin or rely solely on clients.matchAll for garbage collection.
4. Independently profile control serialization, parse/write, navigation latency, GET_STATUS deep hash cost, quota, and offline recovery on exact normal build and physical iPad.
5. Give users truthful OLD_VERSION_USABLE, CATALOG_RECOVERY_REQUIRED, BACKUP_VERIFIED and SYNC_PENDING states; avoid sensitive telemetry and unsupported install/offline/sync claims.

## VALIDATION / FIVE-TRACK TRANSFER
G01 fresh install vs corrupt established control; G02 release/client-ID growth; G03 old/new tabs and resultingClientId; G04 cross-Worker competing writes; G05 torn JSON, quota and crash; G06 incomplete Shell repair and Firebase reserved paths; G07 safe cache retirement; G08 normal build/upload/Hosting byte parity; G09 Chromium/Safari tab/Home Screen/managed Web Clip; G10 owner-record reopen and independent .lbk restore; G11 accessible recovery and privacy-safe diagnostics; G12 CI negative-control verdict propagation. Each needs exact artifact/engine/OS/context and independent PASS/FAIL/UNKNOWN/BLOCKED.

**E** owns release authority and data-safe retirement; **A** owns client/lifecycle mechanics; **C** owns execution and performance/accessibility oracles; **B** consumes recovery UX requirements from Design Studio; **D** owns privacy-safe diagnostics and public claim integrity, not Marketing's acquisition strategy. Engineering M006 generic Chromium evidence does not transfer to LogMate production.

**OPEN:** current normal artifact, real Worker/browser, Hosting, iPad, managed EFB, data restore, PWA-native Sync. **CHANGE WATCH:** W3C Worker lifecycle, WebKit storage, Flutter generator and Hosting policies. **Stage 8 remains active; production validation OPEN; PWA release HOLD.**
