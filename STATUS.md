# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-17  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification.

# Continuous expert maintenance checkpoints
083 — **PWA Storage Durability & Service-Worker Standards Change Watch — PASS.**  
084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS.**  
085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS.**  
086 — **PWA Direct Transport, Discovery, Pairing & Security Boundaries — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
087 — **PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
088 — **PWA Offline Navigation, Service-Worker Update Recovery & Observability — PASS (generic) / PRODUCT VALIDATION OPEN.**

## 088 material findings
- navigation readiness is a state machine: network signal, usable transport, worker presence/boot, route cache, shell/data availability, schema compatibility and fetch-handler correctness are independent axes;
- `online ≠ usable network ≠ successful navigation ≠ task-ready application`;
- service-worker update states remain distinct: update detected/installed/waiting/activated/controlling/compatible;
- `skipWaiting()`/`Clients.claim()` can accelerate takeover but do not establish shell/cache/schema/protocol compatibility;
- navigation preload can reduce worker-start navigation latency but does not provide offline fallback or update correctness;
- cache ownership now separates immutable assets, shell/navigation, reconstructible reference data, irreplaceable user records and durable outbox state;
- routine recovery must never use destructive site-data clearing when unsynchronized authoritative records may exist;
- long-offline N→N+k recovery requires version identification, data/outbox preservation, bounded migration, compatible activation, idempotent replay/reconciliation and delayed obsolete-cache retirement;
- recovery observability must distinguish worker/shell/schema generations and navigation/recovery outcomes while minimizing record content/identifiers;
- accessible degraded/update/recovery states are a data-safety control, not cosmetic messaging;
- Safari 26.6 (2026-07-27) still shipped service-worker fixes, so exact WebKit behavior remains CHANGE WATCH and target-device validation is mandatory.

# Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.
`navigation preload ≠ offline fallback ≠ cache correctness`.
`reconstructible cache ≠ authoritative user records/outbox`.
`Home Screen installed ≠ background synchronization available`.
`push event execution ≠ arbitrary background execution`.
`previously authenticated ≠ currently server-authorized ≠ authorized indefinitely offline`.
`HTTPS + same-origin storage ≠ complete device-loss/XSS/data-at-rest security`.
`Web Crypto available ≠ safe key-management/recovery architecture established`.
`WebSocket/WebTransport available ≠ peer discovery`.
`WebRTC P2P capability ≠ zero-infrastructure discovery ≠ unattended pairing ≠ background execution`.
`paired identity ≠ current address ≠ current ICE candidates ≠ signaling delivered`.
`STUN reachable ≠ peer reachable`; `TURN success ≠ direct P2P`.
`same LAN ≠ direct reachability`.
`origin deployment complete ≠ all installed clients updated`.
`origin rollback complete ≠ installed client recovered`.

# Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; 088 refreshes worker lifecycle/update/cache/navigation-preload mechanics and current standards/WebKit change-watch.
- **B UX/IA/Content:** consumes explicit offline/cached/local-only/sync/update/recovery state semantics; generic `Offline` or `Saved` labels are insufficient for data-safety tasks.
- **C Performance/Accessibility/Quality:** now has a canonical failure-injection matrix; exact Safari/device, AT, degraded-network and recovery execution remains OPEN.
- **D Search/Discovery/Analytics:** consumes minimized navigation/update/recovery telemetry; absence of offline telemetry cannot prove absence of failures and analytics cannot certify durability.
- **E Architecture/Security/Operations:** highest-consequence PWA owner; 088 defines compatibility/recovery hierarchy, cache ownership, observability and acceptance invariants. Remaining closure is implementation/device evidence.

# Cross-repository evidence
Design Studio Web Design checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W039 bounded correction-chain contract ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering checked 2026-09-17: global Foundation still IN STUDY; current data evidence distinguishes serialization/publication/transactions/indexes and explicitly does not transfer Linux process-level evidence to iOS/Android durability. This reinforces 088's requirement that schema/outbox/cache recovery and interruption behavior be executed on target platforms rather than inferred.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol, independent backup/restore and direct unattended PWA↔native transport.

# Next learning mode
Generic direct-transport and generic offline/update/recovery theory are now sufficient for handoff. Highest-value product evidence requires Software Engineering + exact managed-iPad execution using 087/088 matrices.

Without new implementation evidence, next autonomous PWA block should avoid repeating service-worker primers and examine **PWA testing/diagnostic architecture across browser devtools, automated browser tests, offline/network fault injection, storage/schema fixtures, release acceptance and support-safe diagnostics**, then connect it to privacy-minimized observability and Design Studio degraded-state evidence. Continue current Safari/WebKit change-watch.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–088 PASS**.
- PWA generic direct-sync establishment and offline/update/recovery architecture: sufficient for implementation handoff; product/device validation OPEN.
- Reporting remains coarse/checkpoint-based.
