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
095 — PWA XSS/Origin Compromise Against Unlocked Data & Key-Use Authority — **PASS (generic) / PRODUCT IMPLEMENTATION + TARGET-DEVICE VALIDATION OPEN**.

## 095 material findings
- `encrypted at rest ≠ protected from authorized same-origin script while unlocked`;
- same-origin policy isolates other origins but is not an intra-origin privilege boundary between legitimate application JS and injected hostile JS;
- non-extractable Web Crypto keys can still be security-relevant capabilities: preventing raw export does not prove hostile authorized script cannot invoke decrypt/sign/unwrap paths or observe resulting plaintext;
- CSP is defense in depth and Trusted Types narrows DOM-XSS sinks; neither proves safety against compromised first-party code, unsafe Trusted Types policy, supply-chain compromise or already-authorized worker/application execution;
- Trusted Types is Baseline 2026 and WebKit documents Safari 26.0 support; exact managed-EFB Safari/WebKit version/enforcement remains CHANGE WATCH / target-device evidence;
- Service Worker compromise connects release provenance to runtime key/plaintext exposure: clean origin publication alone does not prove installed clients have left the compromised generation;
- key-use lifetime and plaintext lifetime are separate from key extraction. Shorter lifetime may reduce exposure but `reference dropped ≠ key material zeroized` and `UI locked ≠ cryptographic capability unavailable`;
- sensitive-context third-party execution, analytics/ads and public content should not automatically receive the same execution authority as locally authoritative offline records; exact origin segmentation remains an architecture decision.

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
`encrypted at rest ≠ protected from authorized same-origin script while unlocked`.
`non-extractable key ≠ unusable cryptographic capability`.
`same-origin isolation ≠ isolation from hostile code executing as that origin`.
`CSP/Trusted Types reduce injection risk ≠ origin compromise becomes harmless`.
`different path ≠ different origin security boundary`.
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
- **A Platform/Browser:** strong; supplies origin, Web Crypto, CSP/Trusted Types, Service Worker and storage mechanics. Exact Safari/managed-iPad Trusted Types/CSP/worker behavior remains CHANGE WATCH / target-device evidence.
- **B UX/IA/Content:** owns truthful locked/unlocked/reauth/security-recovery state distinctions and must not equate `encrypted` with universally `safe`; visual realization remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns XSS/sink/CSP/Trusted-Types/worker-recovery/key-use fault matrices and data/security oracles. Exact Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** public discovery surfaces need no unlocked record authority; analytics/diagnostics must remain minimized and should not create unnecessary sensitive-context exfiltration authority.
- **E Architecture/Security/Operations:** current highest-risk focus; 095 closes the generic encryption-at-rest vs runtime-origin-compromise boundary. Product closure requires exact code, CSP, dependency, worker, key/plaintext lifetime and device evidence.

# Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W046 destructive-concurrency runtime ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device/print, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY; latest global evidence Q003 establishes schedule-dependent correctness/flaky-test mechanics, while D006 replication/sync and S001 artifact/integrity/authenticity/authorization/provenance evidence remain relevant. No exact PWA key hierarchy, CSP/Trusted Types, browser secure-storage, worker or managed-iPad evidence exists in that canonical status.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery/unsupported UX and AT behavior, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol/API compatibility windows, independent backup/restore, direct unattended PWA↔native transport, Safari inspection/pairing/export permissions, actual diagnostic/telemetry implementation, fleet offline-duration/update policy, emergency-control implementation and privacy approval/retention/access policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, session duration/reauthentication/revocation policy, passkey use and backup policy, Managed Apple Account/iCloud Keychain policy, local unlock/device-bound credentials, offline authorization requirements, locally authoritative record classes, logout/account-deletion/device-revocation retention, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, key extractability/wrapping/storage, old-backup compatibility and physical managed-iPad replacement/revocation/restore evidence.

Runtime-origin/XSS OPEN includes actual framework/rendering sinks, sanitization/encoding, CSP and Reporting configuration, Trusted Types feasibility/enforcement, first/third-party script graph, analytics/ads/support widgets, allowed network destinations, worker code/scope, key-reference/plaintext lifetime, relock semantics, compromised-worker repair and exact managed-iPad behavior.

Supply-chain OPEN includes actual product repository rules/review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN/origin deployment identity, secret/workload-identity model, exact CSP/Trusted Types feasibility, worker-response CSP/scope, DNS/provider recovery authority, credential/key rotation drills and compromised-worker repair on physical managed iPad.

# Next learning mode
095 closes the generic encryption-at-rest versus trusted-origin runtime-compromise gap. Avoid repeating XSS/CSP/Web Crypto primers. Highest-value next work should consume exact implementation or Design Studio execution evidence when available. Without it, the next adjacent cross-track question is **sensitive-context origin/third-party isolation and capability minimization**: whether marketing/analytics/ads/support/public content should share origin, Service Worker scope and execution authority with an offline locally authoritative PWA, including CSP/connect-src, iframe/sandbox/storage/auth continuity and operational trade-offs.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–095 PASS**.
- Generic PWA direct-sync, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline coexistence/retirement, release-supply-chain, session/offline-authorization, account/device/key-recovery and runtime-origin-compromise governance: sufficient for implementation handoff; product/device/AT/security/privacy validation OPEN.
- Reporting remains coarse/checkpoint-based.
