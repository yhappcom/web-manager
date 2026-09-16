# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-17  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification.

# Continuous expert maintenance checkpoints
083 — PWA Storage Durability & Service-Worker Standards Change Watch — **PASS**.  
084 — iOS/iPadOS PWA Install, Background & Authentication Reality — **PASS**.  
085 — PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — **PASS**.  
086 — PWA Direct Transport, Discovery, Pairing & Security Boundaries — **PASS (generic) / PRODUCT FEASIBILITY OPEN**.  
087 — PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — **PASS (generic) / PRODUCT FEASIBILITY OPEN**.  
088 — PWA Offline Navigation, Service-Worker Update Recovery & Observability — **PASS (generic) / PRODUCT VALIDATION OPEN**.  
089 — PWA Testing, Diagnostics & Release Evidence Architecture — **PASS (generic) / TARGET-DEVICE EXECUTION OPEN**.  
090 — PWA Release, Support & Incident Evidence + Accessible Recovery Contract — **PASS (generic) / TARGET-DEVICE & AT EXECUTION OPEN**.  
091 — PWA Long-Offline Release Coexistence, API Retirement & Incident Containment — **PASS (generic) / PRODUCT EXECUTION OPEN**.

## 091 material findings
- long-offline PWA support is governed by a compatibility envelope across client/shell, worker, persisted schema, API/protocol, queued-operation format and server acceptance rules—not a single latest-version number;
- RFC 9745 Deprecation and RFC 8594 Sunset are distinct lifecycle signals: deprecated does not mean unavailable, and connected-client signaling cannot prove an offline installed fleet has received or completed migration;
- retirement requires an offline-safe evidence gate: skipped-version migration, old outbox replay/transformation/recovery, local-authoritative-data preservation, independent restore and support diagnosis must survive the compatibility-window closure;
- unsupported-client handling is capability-specific. Remote write/sync can be restricted while safe local read/write/export/recovery remains available; app-wide lockout can increase loss risk when the device holds the only unsynchronized record;
- emergency controls should disable the smallest unsafe capability. A remote kill switch cannot contain a client that is offline and never receives it;
- origin/server rollback, worker rollback, shell rollback, persisted-schema rollback and outbox-format rollback are separate. Forward-fix can be safer after irreversible local migration/publication;
- diagnostic schema has its own compatibility/privacy contract; telemetry from reporting clients cannot certify silent long-offline populations;
- staged rollout must test generation diversity (N, N-1, supported N-k, pending outbox, interrupted migration), not only a percentage of current origin traffic;
- Software Engineering D005 transfers directly: backup artifact existence, physical integrity, schema compatibility and semantic recovery are separate; protocol retirement/update cannot invalidate the recovery reader contract.

# Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.
`automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.
`Safari diagnostic capability documented ≠ managed-EFB diagnostic workflow permitted`.
`release deployed ≠ release accepted ≠ product recovery validated`.
`rendered/HTTP 200 ≠ PWA state/data invariant satisfied`.
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
`deprecation signal delivered ≠ every installed client informed ≠ migration completed`.
`remote kill switch configured ≠ offline client contained`.
`server compatible ≠ local schema compatible ≠ queued operation replayable`.
`cannot diagnose ≠ user should clear storage`.

# Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; supplies worker/cache/storage/network mechanics. Service Worker/WebKit details remain CHANGE WATCH.
- **B UX/IA/Content:** owns truthful local-only/pending/deprecated/unsupported/recovery state taxonomy and durable help/action hierarchy; visual realization remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns compatibility/fault matrices, release oracles and accessible degraded-state requirements. Exact Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** consumes minimized rollout/health signals; silent-client denominator bias means analytics cannot certify fleet retirement safety.
- **E Architecture/Security/Operations:** current highest-risk focus; 091 adds compatibility-window, retirement, kill-switch and incident-containment governance. Product closure requires implementation/device/privacy evidence.

# Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W042 export→live authority recheck ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. D005 executable bounded evidence establishes backup artifact exists ≠ physical integrity ≠ schema compatibility ≠ semantic recovery. Transfer: PWA release retirement/restore acceptance must test the intended reader generation and independent recovery contract explicitly.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery/unsupported UX and AT behavior, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol/API compatibility windows, independent backup/restore, direct unattended PWA↔native transport, Safari inspection/pairing/export permissions, actual diagnostic/telemetry implementation, fleet offline-duration/update policy, emergency-control implementation and privacy approval/retention/access policy.

# Next learning mode
091 closes the generic long-offline compatibility/retirement/containment contract. Without new runtime artifacts, avoid another versioning primer. Highest-value next work should consume new Software Engineering/Design Studio execution evidence; otherwise examine **PWA release/update supply-chain integrity and secure deployment trust**, including service-worker script integrity/trust boundaries, dependency/build provenance, CSP/Trusted Types where applicable, deployment authorization, compromised-origin/CDN scenarios, emergency key/credential rotation and recovery. Continue Service Worker/WebKit/manifest capability CHANGE WATCH.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–091 PASS**.
- PWA generic direct-sync, offline/update/recovery, testing/diagnostics, release/support/incident and long-offline coexistence/retirement governance: sufficient for implementation handoff; product/device/AT/privacy validation OPEN.
- Reporting remains coarse/checkpoint-based.
