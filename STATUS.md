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
099 PWA Trust-Policy Authenticity, Authority Recovery & Anti-Rollback Boundaries — **PASS (generic) / PRODUCT CRYPTOGRAPHIC + CONTROL-PLANE VALIDATION OPEN**.

## 099 material findings
- a security-critical policy is not independently authenticated merely because it arrived from the configured origin over valid HTTPS; origin/control-plane compromise can serve attacker-chosen policy over a valid transport;
- signature verification must bind an authorized signer/key, semantic policy context, version/generation and freshness requirements; `signature valid ≠ signer authorized ≠ policy current`;
- TUF supplies reusable evidence for role separation, threshold trust, persisted anti-rollback state, expiry/freeze detection and chained root-key transition, but adopting TUF is not a MintTap/LogMate decision;
- a pure web PWA has a bootstrap/self-protection limitation: if the same compromised origin supplies verifier code, policy and newly fetched verification key, Web Crypto alone does not create an independent trust root;
- planned key rotation, lost-key recovery and compromise recovery are distinct operations; a compromised old key cannot by itself prove a trustworthy successor;
- rollback, freeze and fast-forward are distinct attacks; monotonic generation alone does not solve freshness, trusted-time or malicious high-version problems;
- long-offline EFB policy freshness failure must constrain the smallest unsafe bridge/replay capability without converting stale trust into user-data deletion;
- exact product signing authority, bootstrap, trusted-time, key custody, recovery root, anti-rollback persistence and managed-iPad feasibility remain OPEN.

## Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.  
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.  
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.  
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.  
`automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.  
`previously authenticated ≠ server session currently valid ≠ local data currently unlocked ≠ offline operation authorized ≠ pending mutation remotely accepted`.  
`authority revoked remotely ≠ disconnected client informed ≠ local capability immediately unavailable`.  
`network restored ≠ trust restored ≠ replay authorized`.  
`sync denied ≠ local record should be deleted`.  
`outbox replay paused ≠ outbox discarded`.  
`bridge untrusted ≠ origin storage should be wiped`.  
`stale trust metadata ≠ corrupted user data`.  
`HTTPS policy fetch succeeded ≠ policy authorized by an independent trust root`.  
`signature mathematically valid ≠ signer authorized for this policy`.  
`valid old signature ≠ current policy`.  
`signed payload ≠ signed interpretation context`.  
`SubtleCrypto.verify available ≠ trustworthy policy-update system established`.  
`public key fetched from compromised origin ≠ independent authenticity proof`.  
`key rotated ≠ old key proven uncompromised`.  
`successor signed only by compromised key ≠ compromise recovery proven`.  
`monotonic version check ≠ freeze resistance`.  
`expiry check ≠ trustworthy wall clock`.  
`highest version seen ≠ legitimate authority transition`.  
`policy expired ≠ local records expired`.  
`new signed policy accepted ≠ compromised worker/runtime repaired`.  
`logout ≠ origin wipe`.  
`account recovery ≠ data recovery`.  
`credential rotation ≠ data-encryption-key rotation`.  
`new device authorized ≠ old offline device contained`.  
`HTTP cache policy ≠ application-data authorization policy`.  
`reconstructible cache ≠ authoritative user records/outbox`.  
`encrypted at rest ≠ protected from authorized same-origin script while unlocked`.  
`non-extractable key ≠ unusable cryptographic capability`.  
`CSP/Trusted Types reduce injection risk ≠ origin compromise becomes harmless`.  
`different path ≠ different origin security boundary`.  
`narrow Service Worker scope ≠ independent origin isolation`.  
`different origin ≠ no trust bridge`.  
`postMessage origin validated ≠ message authorized ≠ payload semantically valid ≠ transaction current`.  
`CORS allowed ≠ caller authenticated ≠ caller authorized ≠ mutation safe`.  
`Universal Link association valid ≠ deep-link payload authorized`.  
`third-party business value ≠ requirement for sensitive-context execution authority`.  
`measurement continuity ≠ shared script authority`.  
`analytics queue ≠ authoritative application outbox`.  
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
- **A Platform/Browser:** strong; supplies origin/storage/Service Worker/Web Crypto/update mechanics. Exact Safari/managed-iPad trust-bootstrap, clock and storage-reset behavior remain target-device evidence.
- **B UX/IA/Content:** consumes unverifiable/expired-policy states as truthful continuity/recovery requirements; policy freshness failure must not be phrased as local-data corruption.
- **C Performance/Accessibility/Quality:** owns invalid-signature, unauthorized-key, rollback/freeze/fast-forward, key-transition, clock and cross-browser/device negative evidence. Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** remote config, campaign, analytics and discovery channels are not implicit security-policy roots.
- **E Architecture/Security/Operations:** current highest-risk owner; 099 closes the generic policy-authenticity/authority-recovery prerequisite. Product cryptographic/control-plane design requires exact implementation evidence.

## Cross-repository evidence
Design Studio checked 2026-09-17: Web Design is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE; W050 offline-outbox tenant-binding runtime is ready but execution remains OPEN. No Safari, screen-reader, physical-device or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. F005 distinguishes error/timeout observation from cleanup/terminal resource state; D006 retains retry/idempotency/conflict work. These support failure/replay state semantics but do not prove browser/PWA signing/bootstrap behavior.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache/update behavior, schema migration, storage pressure, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN, pairing/revocation, foreground/background behavior, outbox/protocol/API compatibility, backup/restore, PWA↔native transport, diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, offline authorization, passkey/local-unlock design, locally authoritative record classes, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, backup compatibility and device replacement/revocation evidence.

Runtime-origin/topology OPEN includes actual framework/rendering sinks, CSP/Reporting/Trusted Types, first/third-party script graph, analytics/ads/support widgets, origin/hostname topology, allowed network destinations, CORS/credential policy, `postMessage` bridges, iframe/sandbox/Permissions Policy, Storage Access behavior, worker script/scope, auth redirects, deep/native links, support/export handoffs, auth continuity, key/plaintext lifetime, bridge-policy generation and compromised-worker repair.

Trust-policy/control-plane OPEN includes exact security-critical policy assets, signing roles/keys, bootstrap trust material, canonical signed envelope, anti-rollback state, trusted-time assumptions, planned rotation, compromise-recovery authority, threshold/key custody, offline freshness policy and whether same-origin runtime can bypass verification.

Supply-chain OPEN includes actual repository review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN deployment identity, secret/workload identity, DNS/provider recovery and credential/key rotation drills.

## Next learning mode
099 closes the generic revocation-policy authenticity and authority-recovery prerequisite. Avoid inventing a product signing hierarchy without implementation/security evidence. Highest-value next work should consume exact implementation, Design Studio execution or Software Engineering evidence when available. Without it, the next adjacent question is **trusted-state persistence and reset/reinstallation recovery**: anti-rollback memory, storage eviction/reset, reinstall/new-device bootstrap and recovery when the client loses its previously trusted generation/root metadata. This must remain distinct from user-record backup/restore.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–099 PASS**.
- Generic PWA architecture now covers durability, platform capability, recovery/auth, direct transport, offline/update, diagnostics, release/incident, long-offline compatibility, supply-chain, key lifecycle, runtime-origin compromise, sensitive-context topology, trust bridges, stale-client revocation and trust-policy authenticity/authority recovery.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
