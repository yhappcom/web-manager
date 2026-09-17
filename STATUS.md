# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-17  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification.

## Continuous expert maintenance checkpoints
083 PWA Storage Durability & Service-Worker Standards Change Watch — **PASS**.  
084 iOS/iPadOS PWA Install, Background & Authentication Reality — **PASS**.  
085 PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — **PASS**.  
086 PWA Direct Transport, Discovery, Pairing & Security Boundaries — **PASS (generic) / PRODUCT FEASIBILITY OPEN**.  
087 PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — **PASS (generic) / PRODUCT FEASIBILITY OPEN**.  
088 PWA Offline Navigation, Service-Worker Update Recovery & Observability — **PASS (generic) / PRODUCT VALIDATION OPEN**.  
089 PWA Testing, Diagnostics & Release Evidence Architecture — **PASS (generic) / TARGET-DEVICE EXECUTION OPEN**.  
090 PWA Release, Support & Incident Evidence + Accessible Recovery Contract — **PASS (generic) / TARGET-DEVICE & AT EXECUTION OPEN**.  
091 PWA Long-Offline Release Coexistence, API Retirement & Incident Containment — **PASS (generic) / PRODUCT EXECUTION OPEN**.  
092 PWA Release/Update Supply-Chain Integrity & Secure Deployment Trust — **PASS (generic) / PRODUCT IMPLEMENTATION VALIDATION OPEN**.  
093 PWA Session Revocation, Offline Authorization & Security-Sensitive Local Data Separation — **PASS (generic) / PRODUCT AUTHORIZATION + DEVICE VALIDATION OPEN**.  
094 PWA Account/Device Recovery & Cryptographic Key Lifecycle — **PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN**.  
095 PWA XSS/Origin Compromise Against Unlocked Data & Key-Use Authority — **PASS (generic) / PRODUCT IMPLEMENTATION + TARGET-DEVICE VALIDATION OPEN**.  
096 PWA Sensitive-Context Origin, Third-Party Isolation & Capability Minimization — **PASS (generic) / PRODUCT TOPOLOGY + TARGET-DEVICE VALIDATION OPEN**.  
097 PWA Explicit Cross-Context Trust Bridges — **PASS (generic) / PRODUCT BRIDGE + TARGET-DEVICE VALIDATION OPEN**.  
098 PWA Bridge Revocation, Stale-Client Trust & Data-Preserving Containment — **PASS (generic) / PRODUCT REVOCATION + TARGET-DEVICE VALIDATION OPEN**.

## 098 material findings
- revocation is an authority decision, not instantaneous knowledge at a disconnected client; an offline PWA cannot receive a remote revocation until contact or a locally enforceable expiry/constraint occurs;
- credential, origin, protocol, native-association, device/pairing, deployment and business-integration revocation are different classes and must not collapse into one global `app blocked` state;
- reconnect must re-establish current trust/protocol policy before remote mutation or outbox replay; `network restored ≠ trust restored ≠ replay authorized`;
- revocation should withdraw the smallest unsafe capability while preserving locally authoritative records/outbox until a separately authorized recovery/destruction decision exists;
- broad `Clear-Site-Data: "storage"` is not a precise bridge-revocation primitive because it can remove IndexedDB and Service Worker registrations;
- Apple Associated Domains data is CDN/cached and refreshed asynchronously; changing AASA is not an instantaneous fleet-wide emergency revocation channel;
- stale trust metadata is not evidence of corrupted user data; explicit policy/protocol generations can support reconnect comparison without treating old clients as malicious;
- exact MintTap/LogMate offline authorization duration, MDM revocation, pairing identity, sync protocol and data-destruction policy remain OPEN.

## Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.  
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.  
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.  
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.  
`automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.  
`Home Screen installed ≠ background synchronization available`.  
`previously authenticated ≠ server session currently valid ≠ local data currently unlocked ≠ offline operation authorized ≠ pending mutation remotely accepted`.  
`credential revoked at server ≠ disconnected PWA instantly aware ≠ local data instantly inaccessible`.  
`authority revoked remotely ≠ disconnected client informed ≠ local capability immediately unavailable`.  
`network restored ≠ trust restored ≠ replay authorized`.  
`sync denied ≠ local record should be deleted`.  
`outbox replay paused ≠ outbox discarded`.  
`bridge untrusted ≠ origin storage should be wiped`.  
`AASA changed at origin ≠ Apple CDN refreshed ≠ every device association refreshed`.  
`stale trust metadata ≠ corrupted user data`.  
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
`narrow Service Worker scope ≠ independent origin isolation`.  
`different origin ≠ no trust bridge`.  
`postMessage origin validated ≠ message authorized ≠ payload semantically valid ≠ transaction current`.  
`CORS allowed ≠ caller authenticated ≠ caller authorized ≠ mutation safe`.  
`user returned from identity provider ≠ response belongs to this transaction ≠ requested navigation target trusted`.  
`Universal Link association valid ≠ deep-link payload authorized`.  
`custom URL scheme launches an app ≠ intended app ownership proven`.  
`third-party business value ≠ requirement for sensitive-context execution authority`.  
`measurement continuity ≠ shared script authority`.  
`analytics queue ≠ authoritative application outbox`.  
`PWA installed from site ≠ Service Worker should control the entire site`.  
`SSO convenience ≠ every web origin should receive the same session credential`.  
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

## Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; supplies origin/storage/Service Worker/CSP/Fetch/CORS/message/navigation/update mechanics. Exact Safari/managed-iPad revocation/update behavior remains CHANGE WATCH / target-device evidence.
- **B UX/IA/Content:** consumes stale-trust/revocation state as truthful continuity/recovery requirements; remote-sync denial must not be phrased as local-data loss.
- **C Performance/Accessibility/Quality:** owns revocation-before/during-replay, stale-client reconnect, focus/status-message, cross-browser/device evidence. Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** retired campaign/deep-link state is not authorization; discovery staleness must degrade safely without preserving privileged bridge authority.
- **E Architecture/Security/Operations:** current highest-risk owner; 098 closes the generic stale-client trust/revocation prerequisite. Product policy requires exact implementation/MDM evidence.

## Cross-repository evidence
Design Studio checked 2026-09-17: Web Design is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE; W049 tenant-context cache-isolation runtime is ready but execution remains OPEN. No Safari, screen-reader, physical-device or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. F005 distinguishes waiter timeout from underlying operation cancellation; D006 retains replication/idempotency/conflict work. These support replay/reconciliation semantics but do not prove browser/PWA revocation behavior.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache/update behavior, schema migration, storage pressure, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN, pairing/revocation, foreground/background behavior, outbox/protocol/API compatibility, backup/restore, PWA↔native transport, diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, offline authorization, passkey/local-unlock design, locally authoritative record classes, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, backup compatibility and device replacement/revocation evidence.

Runtime-origin/topology OPEN includes actual framework/rendering sinks, CSP/Reporting/Trusted Types, first/third-party script graph, analytics/ads/support widgets, origin/hostname topology, allowed network destinations, CORS/credential policy, `postMessage` bridges, iframe/sandbox/Permissions Policy, Storage Access behavior, worker script/scope, auth redirects, deep/native links, support/export handoffs, auth continuity, key/plaintext lifetime, bridge-policy generation and compromised-worker repair.

Supply-chain OPEN includes actual repository review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN deployment identity, secret/workload identity, DNS/provider recovery and credential/key rotation drills.

## Next learning mode
098 closes the generic stale-client trust/revocation prerequisite. Avoid repeating token/AASA/reconnect primers. Highest-value next work should consume exact implementation, Design Studio execution or Software Engineering evidence when available. Without it, the next adjacent high-value question is **revocation-policy authenticity and recovery from authority compromise**: how a client distinguishes a legitimate trust-policy change from a compromised origin/control plane, including policy signing/provenance, key rotation, rollback/freeze resistance and offline bootstrap/recovery boundaries without inventing a product cryptographic design.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–098 PASS**.
- Generic PWA architecture is sufficient for implementation handoff across durability, platform capability, recovery/auth, direct transport, offline/update, diagnostics, release/incident, long-offline compatibility, supply-chain, key lifecycle, runtime-origin compromise, sensitive-context topology, explicit cross-context trust bridges and stale-client revocation/containment.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
