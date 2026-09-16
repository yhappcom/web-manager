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
094 — PWA Account/Device Recovery & Cryptographic Key Lifecycle — **PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN**.

## 094 material findings
- `account recovery ≠ authenticator recovery ≠ device recovery ≠ local-data recovery ≠ backup recovery ≠ synchronization recovery`;
- WebAuthn Level 3 distinguishes single-device from multi-device credentials with backup eligibility/state; credential recovery/backup does not imply recovery of an application data-encryption key or IndexedDB records;
- Apple iCloud Keychain/passkey recovery is platform credential evidence, not proof that a managed EFB permits synchronization/recovery or that a PWA application key participates;
- Web Crypto supports CryptoKey storage and export/wrap semantics, but `extractable=false` does not itself prove hardware binding, remote revocability, zeroization or safe recovery architecture;
- authentication credential, session credential, local-unlock authority, DEK, KEK/recovery key, backup secret and device/pairing credential are distinct lifecycle roles;
- `credential rotation ≠ DEK rotation ≠ KEK rewrap ≠ historical backup migration ≠ old-device revocation`;
- new-device authorization cannot prove old offline-device containment; immediate offline containment requires independently validated device/local controls;
- recovery validation must cover unsynced authoritative records, missing unwrap material, skipped releases, interrupted key migration, old backups, reconnect after revocation, MDM restrictions and XSS while keys are usable.

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
`account recovery ≠ data recovery`.
`credential rotation ≠ data-encryption-key rotation`.
`new device authorized ≠ old offline device contained`.
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
- **A Platform/Browser:** strong; supplies WebAuthn/Web Crypto/IndexedDB/storage/session mechanics. WebKit and managed-iPad key/storage behavior remain CHANGE WATCH / target-device evidence.
- **B UX/IA/Content:** owns truthful account-restored/device-authorized/backup-found/backup-restored/sync-reconciled state distinctions; visual realization remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns recovery/key-loss/rotation/reconnect/fault matrices and data/security oracles. Exact Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** consumes privacy-minimized recovery diagnostics; lost/offline devices mean analytics cannot certify revocation or recovery completeness.
- **E Architecture/Security/Operations:** current highest-risk focus; 094 closes generic account/device/key-recovery lifecycle boundaries. Product closure requires exact cryptographic, backup, auth, MDM and device evidence.

# Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W045 partial-order merge runtime ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device/print, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: newest relevant global evidence is D006 replication/sync retry-conflict work, following D004 cache/offline ownership and D005 restore boundaries. Transfer is mechanism-level only; exact key hierarchy, browser/Flutter secure storage, encryption migration and managed-iPad evidence remain OPEN.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery/unsupported UX and AT behavior, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol/API compatibility windows, independent backup/restore, direct unattended PWA↔native transport, Safari inspection/pairing/export permissions, actual diagnostic/telemetry implementation, fleet offline-duration/update policy, emergency-control implementation and privacy approval/retention/access policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, session duration/reauthentication/revocation policy, passkey use and backup policy, Managed Apple Account/iCloud Keychain policy, local unlock/device-bound credentials, offline authorization requirements, locally authoritative record classes, logout/account-deletion/device-revocation retention, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, key extractability/wrapping/storage, old-backup compatibility and physical managed-iPad replacement/revocation/restore evidence.

Supply-chain OPEN includes actual product repository rules/review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN/origin deployment identity, secret/workload-identity model, exact CSP/Trusted Types feasibility, worker-response CSP/scope, DNS/provider recovery authority, credential/key rotation drills and compromised-worker repair on physical managed iPad.

# Next learning mode
094 closes the generic account/device/key-recovery conceptual gap. Avoid repeating Web Crypto/passkey primers and do not choose a cryptographic architecture without Software Engineering/security validation. Highest-value next work should consume exact implementation or Design Studio execution evidence when available. Without it, the next adjacent cross-track question is **PWA XSS/origin compromise against locally unlocked encrypted data and recovery keys**: distinguish encryption-at-rest from protection against trusted-origin script execution, then connect CSP/Trusted Types, worker compromise, key-use lifetime and recovery-secret exposure without duplicating Software Engineering implementation ownership.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–094 PASS**.
- Generic PWA direct-sync, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline coexistence/retirement, release-supply-chain, session/offline-authorization and account/device/key-recovery governance: sufficient for implementation handoff; product/device/AT/security/privacy validation OPEN.
- Reporting remains coarse/checkpoint-based.
