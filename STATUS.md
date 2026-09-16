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
092 — PWA Release/Update Supply-Chain Integrity & Secure Deployment Trust — **PASS (generic) / PRODUCT IMPLEMENTATION VALIDATION OPEN**.  
093 — PWA Session Revocation, Offline Authorization & Security-Sensitive Local Data Separation — **PASS (generic) / PRODUCT AUTHORIZATION + DEVICE VALIDATION OPEN**.

## 093 material findings
- authentication is not one durable boolean: identity binding, server-session validity, local unlock, offline authorization, mutation acknowledgement and recovery state are separate;
- `credential revoked at server ≠ disconnected PWA instantly aware ≠ local data instantly inaccessible`; server revocation cannot provide immediate offline containment by itself;
- HTTP cache directives, Service Worker Cache Storage, IndexedDB records, session material and durable outbox have different mechanics and semantic roles; storage location does not determine authority;
- `Clear-Site-Data` is intentionally broad and can clear storage/service-worker state. For an offline-first product containing irreplaceable unsynchronized records it is a security/recovery tool, not a safe generic logout primitive;
- `logout ≠ origin wipe`: terminate online authority, lock/restrict local access, stop sync, preserve required unacknowledged records/outbox, optionally purge reconstructible state, and erase only under an explicit recovery/retention contract;
- local capabilities must be policy-separated during expiry/revocation/recovery: local read, local write, export/backup, remote read, remote write and outbox replay need not fail together;
- destructive cleanup requires proof that authoritative local data is remotely acknowledged/reconciled, independently restorable, or intentionally abandoned under approved policy;
- Software Engineering D004/D005 transfer supports separating confirmed base/pending mutation/cache and backup existence/semantic restore; exact Flutter/iOS/managed-iPad behavior remains OPEN.

# Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.
`automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.
`Home Screen installed ≠ background synchronization available`.
`previously authenticated ≠ server session currently valid ≠ local data currently unlocked ≠ offline operation authorized ≠ pending mutation remotely accepted`.
`credential revoked at server ≠ disconnected PWA instantly aware ≠ local data instantly inaccessible`.
`logout ≠ origin wipe`.
`HTTP cache policy ≠ application-data authorization policy`.
`reconstructible cache ≠ authoritative user records/outbox`.
`HTTPS + same-origin storage ≠ complete device-loss/XSS/data-at-rest security`.
`Web Crypto available ≠ safe key-management/recovery architecture established`.
`WebRTC P2P capability ≠ zero-infrastructure discovery ≠ unattended pairing ≠ background execution`.
`origin deployment complete ≠ all installed clients updated`.
`origin rollback complete ≠ installed client recovered`.
`remote kill switch configured ≠ offline client contained`.
`server compatible ≠ local schema compatible ≠ queued operation replayable`.
`cannot diagnose ≠ user should clear storage`.
`HTTPS delivered ≠ intended artifact delivered ≠ authorized artifact built ≠ dependency graph uncompromised`.
`page CSP strong ≠ service-worker CSP strong`.
`commit SHA known ≠ deployed bytes proven`.
`origin repaired ≠ installed fleet clean`.

# Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; supplies cookie/session, HTTP cache, worker/cache/storage/origin mechanics. Service Worker/WebKit/Clear-Site-Data details remain CHANGE WATCH.
- **B UX/IA/Content:** owns truthful local-only/pending/expired/revoked/recovery state taxonomy and action hierarchy; visual realization remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns expiry/revocation/reconnect/fault matrices and data/security oracles. Exact Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** consumes privacy-minimized health/security signals; silent offline clients mean analytics cannot certify revocation completion or fleet safety.
- **E Architecture/Security/Operations:** current highest-risk focus; 093 closes generic session-revocation/offline-authorization/local-data-lifecycle contract. Product closure requires exact auth, retention, backup, device and security evidence.

# Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W043 temporal provenance runtime ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. Newest relevant global evidence is D004 cache/offline ownership: confirmed base, pending mutation and cache/projection semantics must not collapse; D005 retains restore-acceptance boundaries. Transfer is mechanism-level only; exact FlutterFire/iOS product evidence remains OPEN.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery/unsupported UX and AT behavior, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol/API compatibility windows, independent backup/restore, direct unattended PWA↔native transport, Safari inspection/pairing/export permissions, actual diagnostic/telemetry implementation, fleet offline-duration/update policy, emergency-control implementation and privacy approval/retention/access policy.

Auth/security OPEN includes actual authentication/session/token/cookie architecture, session duration/reauthentication/revocation policy, local unlock/device-bound credentials, offline authorization requirements, locally authoritative record classes, logout/account-deletion/device-revocation retention, IndexedDB/Cache separation, encryption/key-management, backup/restore guarantees and managed-iPad device-level data protection.

Supply-chain OPEN includes actual product repository rules/review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN/origin deployment identity, secret/workload-identity model, exact CSP/Trusted Types feasibility, worker-response CSP/scope, DNS/provider recovery authority, credential/key rotation drills and compromised-worker repair on physical managed iPad.

# Next learning mode
093 closes the generic session-revocation/offline-authorization/local-data-lifecycle conceptual gap. Avoid repeating generic session or storage primers. Highest-value next work should consume Software Engineering exact runtime evidence or Design Studio execution evidence when available. Without new product evidence, the next adjacent cross-track question is **PWA account/device recovery and cryptographic/local-unlock key lifecycle under offline-first constraints**: distinguish account recovery from data recovery, credential rotation from data-encryption key rotation, device replacement from revocation, and server-assisted recovery from zero-knowledge/local-only claims. Do not choose a cryptographic architecture without Software Engineering/security validation.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–093 PASS**.
- Generic PWA direct-sync, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline coexistence/retirement, release-supply-chain governance and session-revocation/offline-authorization governance: sufficient for implementation handoff; product/device/AT/security/privacy validation OPEN.
- Reporting remains coarse/checkpoint-based.
