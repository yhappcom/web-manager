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

## 096 material findings
- origin is scheme/host/port; route/path separation is not a browser security boundary;
- Service Worker scope can reduce routing/control coupling but does not create independent same-origin storage/script principals;
- public/marketing/analytics/advertising/support surfaces do not automatically require the execution/storage/worker authority of a locally authoritative offline PWA;
- per-response CSP, narrow `connect-src`, `frame-src`/`frame-ancestors`, sandbox and Permissions Policy are useful capability-reduction controls, not substitutes for origin separation where mutual distrust is required;
- cross-origin isolation can be deliberately weakened again through credentialed APIs, CORS, `postMessage`, Storage Access grants or shared identity; these bridges require explicit contracts;
- separate sensitive-app origin is a stronger browser-principal boundary but introduces auth/session, CORS, deployment, DNS/certificate, navigation and support complexity; it is mandatory to evaluate for high-sensitivity PWA topology but not generically mandated;
- advertising/analytics business value does not prove a requirement for top-level execution in the sensitive PWA; measurement continuity and execution authority are separate requirements;
- exact MintTap/LogMate origin, worker, script, analytics/ad/support, CSP, auth and MDM topology remains OPEN.

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
`CSP destination minimization ≠ malicious same-origin code loses all application authority`.  
`sandbox attribute present ≠ embedded third party safely contained`.  
`cross-origin iframe ≠ no cookie/storage relationship`.  
`different origin ≠ no trust bridge`.  
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
- **A Platform/Browser:** strong; supplies origin/storage/Service Worker/CSP/iframe/sandbox/credential mechanics. Exact Safari/managed-iPad storage-access, worker and policy behavior remains CHANGE WATCH / target-device evidence.
- **B UX/IA/Content:** consumes security topology as a continuity constraint; public/support/auth transitions must preserve truthful local/save/sync/recovery state.
- **C Performance/Accessibility/Quality:** owns third-party failure isolation, CSP/sandbox/credential negative tests, embed/fallback accessibility and target-engine/device evidence. Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** public crawl/discovery surfaces need no unlocked-record authority; measurement continuity must not be equated with shared sensitive execution.
- **E Architecture/Security/Operations:** current highest-risk owner; 096 closes the generic origin/third-party capability-minimization prerequisite. Product topology decision requires exact implementation evidence.

## Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W047 retention-boundary runtime ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device/print, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. F004 synchronization evidence and D006/S001 remain relevant, but no exact PWA origin/CSP/worker/third-party/managed-iPad implementation evidence exists in canonical status.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache/update behavior, schema migration, storage pressure, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN, pairing/revocation, foreground/background behavior, outbox/protocol/API compatibility, backup/restore, PWA↔native transport, diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, offline authorization, passkey/local-unlock design, locally authoritative record classes, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, backup compatibility and device replacement/revocation evidence.

Runtime-origin/topology OPEN includes actual framework/rendering sinks, CSP/Reporting/Trusted Types, first/third-party script graph, analytics/ads/support widgets, origin/hostname topology, allowed network destinations, CORS/credential policy, iframe/sandbox/Permissions Policy, Storage Access behavior, worker script/scope, auth continuity, key/plaintext lifetime and compromised-worker repair.

Supply-chain OPEN includes actual repository review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN deployment identity, secret/workload identity, DNS/provider recovery and credential/key rotation drills.

## Next learning mode
096 closes the generic sensitive-context topology/capability-minimization gap. Avoid repeating same-origin/CSP/iframe primers. Highest-value next work should consume exact implementation or Design Studio execution evidence when available. Without it, the next adjacent cross-track question is **explicit cross-context trust bridges**: `postMessage`, CORS/credentialed APIs, auth redirects, deep links/universal links and support/export handoffs — how origin isolation can be accidentally undone by overly broad message origins, credential scope or navigation authority.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–096 PASS**.
- Generic PWA architecture is sufficient for implementation handoff across durability, platform capability, recovery/auth, direct transport, offline/update, diagnostics, release/incident, long-offline compatibility, supply-chain, key lifecycle, runtime-origin compromise and sensitive-context topology.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
