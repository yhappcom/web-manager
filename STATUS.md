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

## 097 material findings
- origin isolation is only durable if every reconnecting bridge has explicit source/destination, operation, schema, credential, transaction, lifetime and failure semantics;
- `postMessage` exact origin/source validation is necessary but does not authorize message semantics; payload schema, allowed operation, transaction binding and replay behavior remain application responsibilities;
- CORS is response-sharing policy, not authentication or authorization; credentialed CORS broadens a trust bridge and must not be granted merely because an origin is company-controlled;
- OAuth Security BCP requires exact redirect matching, rejects open redirectors and requires transaction protections; current RFC 10017 carries strict in-browser communication discipline into browser-based apps;
- Apple Universal Links/Associated Domains provide stronger website↔app association than custom schemes, but valid association does not make arbitrary deep-link payloads authorized commands;
- navigation, auth, support, export/backup, sync and measurement bridges are different capability classes and must not be collapsed into one generic JSON/URL handoff;
- Universal Links, `postMessage` and CORS do not prove unattended PWA↔native background synchronization; 086/087 product feasibility remains OPEN;
- exact MintTap/LogMate bridge inventory, OAuth/OIDC usage, origin/CORS policy, native-link topology and managed-device behavior remain OPEN.

## Persistent PWA guards
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
- **A Platform/Browser:** strong; supplies origin/storage/Service Worker/CSP/Fetch/CORS/`postMessage`/navigation mechanics. Exact Safari/managed-iPad behavior remains CHANGE WATCH / target-device evidence.
- **B UX/IA/Content:** consumes bridge state as continuity/recovery requirements; redirect, popup, link and export transitions must preserve truthful local/save/sync/recovery state.
- **C Performance/Accessibility/Quality:** owns bridge negative tests, focus/history/AT recovery, cross-browser/device evidence and third-party failure isolation. Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** public discovery and campaign/deep-link parameters are not authorization; measurement continuity must not expand sensitive bridge authority.
- **E Architecture/Security/Operations:** current highest-risk owner; 097 closes the generic explicit trust-bridge prerequisite. Product bridge decisions require exact implementation evidence.

## Cross-repository evidence
Design Studio checked 2026-09-17: global status now reports Web Design Stage 1 PASS / Stage 2 PRACTICE with runtime/browser breadth incomplete; no Safari, screen-reader, physical-device or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. F004 now adds predicate-vs-notification evidence relevant to future bridge/sync event semantics, but no exact PWA bridge/CORS/auth-link/managed-iPad implementation evidence exists.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache/update behavior, schema migration, storage pressure, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN, pairing/revocation, foreground/background behavior, outbox/protocol/API compatibility, backup/restore, PWA↔native transport, diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, offline authorization, passkey/local-unlock design, locally authoritative record classes, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, backup compatibility and device replacement/revocation evidence.

Runtime-origin/topology OPEN includes actual framework/rendering sinks, CSP/Reporting/Trusted Types, first/third-party script graph, analytics/ads/support widgets, origin/hostname topology, allowed network destinations, CORS/credential policy, `postMessage` bridges, iframe/sandbox/Permissions Policy, Storage Access behavior, worker script/scope, auth redirects, deep/native links, support/export handoffs, auth continuity, key/plaintext lifetime and compromised-worker repair.

Supply-chain OPEN includes actual repository review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN deployment identity, secret/workload identity, DNS/provider recovery and credential/key rotation drills.

## Next learning mode
097 closes the generic explicit cross-context trust-bridge gap. Avoid repeating `postMessage`/CORS/OAuth redirect primers. Highest-value next work should consume exact implementation, Design Studio execution or Software Engineering evidence when available. Without it, the next adjacent question is **capability/bridge revocation and stale-client trust**: how an installed/offline client learns that a bridge, origin, credential audience, native association or export/sync protocol is no longer trusted without destroying locally authoritative data.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–097 PASS**.
- Generic PWA architecture is sufficient for implementation handoff across durability, platform capability, recovery/auth, direct transport, offline/update, diagnostics, release/incident, long-offline compatibility, supply-chain, key lifecycle, runtime-origin compromise, sensitive-context topology and explicit cross-context trust bridges.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
