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

## 092 material findings
- the PWA update channel is a privileged code-deployment boundary: HTTPS authenticates/encrypts transport to the origin but does not prove that reviewed source, dependencies, CI/CD, deployment identity or published bytes are trustworthy;
- service-worker script URLs are high-impact injection/update sinks because a worker can persist and intercept requests within scope; worker registration/scope, worker-response CSP and page `worker-src` policy require explicit review;
- page CSP does not generally become the worker's CSP. Worker execution policy must be delivered on the worker response; Trusted Types constrains injection sinks but is not artifact provenance;
- production release evidence should correlate reviewed source/workflow + dependency lock/SBOM + trusted build + immutable artifact digest + authorized deployment + exact origin publication + worker/shell/schema/protocol generations;
- `commit SHA known ≠ deployed bytes proven`; build-once/promote-same-artifact is preferred where architecture permits, while exact MintTap/LogMate build topology remains OPEN;
- deployment authority should be bounded/auditable/revocable and avoid unnecessary long-lived credential reuse; source, workflow, build, publish, production config, DNS and emergency recovery authorities should not collapse into one credential path;
- compromised-update response prioritizes stopping publication, preserving evidence, revoking credentials, identifying exact artifact/window, publishing a verified repair through re-established trust, preserving local authoritative records/outbox and proving installed-client cleanup/reconciliation;
- `origin repaired ≠ installed fleet clean`: an activated malicious/bad worker/cache can outlive the origin repair and requires client-generation recovery evidence;
- SBOM/component inventory supports affected-release identification but does not itself establish exploitability or runtime reachability;
- staged rollout reduces both compatibility and supply-chain blast radius, but current origin traffic cannot certify silent long-offline installed clients.

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
`HTTPS delivered ≠ intended artifact delivered ≠ authorized artifact built ≠ dependency graph uncompromised`.
`service-worker byte change detected ≠ legitimate release authorized`.
`page CSP strong ≠ service-worker CSP strong`.
`commit SHA known ≠ deployed bytes proven`.
`valid certificate ≠ trustworthy publisher state`.
`origin repaired ≠ installed fleet clean`.

# Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; supplies worker/cache/storage/network mechanics. 092 consumes worker scope/register/update/CSP mechanics; Service Worker/WebKit details remain CHANGE WATCH.
- **B UX/IA/Content:** owns truthful local-only/pending/deprecated/unsupported/security-repair/recovery state taxonomy and durable help/action hierarchy; visual realization remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns compatibility/fault/release-security matrices, exact-artifact oracles and accessible degraded/recovery requirements. Exact Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** consumes minimized rollout/health/security signals; silent-client denominator bias means analytics cannot certify fleet safety or compromise absence.
- **E Architecture/Security/Operations:** current highest-risk focus; 092 closes generic source→build→artifact→deploy→worker trust and compromised-update recovery governance. Product closure requires exact CI/hosting/IAM/device/privacy evidence.

# Cross-repository evidence
Design Studio Web checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W043 temporal provenance runtime ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY; D005 recovery/publication evidence remains the newest relevant executable block. Transfer: PWA source→artifact→deployment provenance, credential boundaries, dependency locks/SBOM and compromised-update repair must be validated by exact implementation evidence rather than inferred here.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, worker/cache behavior, offline/deep-link navigation, update waiting/activation/takeover, schema migration/interruption, long-offline skipped-version recovery, storage pressure, accessible degraded/recovery/unsupported UX and AT behavior, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN behavior, pairing credential persistence/revocation, foreground/background/suspension behavior, LogMate outbox/protocol/API compatibility windows, independent backup/restore, direct unattended PWA↔native transport, Safari inspection/pairing/export permissions, actual diagnostic/telemetry implementation, fleet offline-duration/update policy, emergency-control implementation and privacy approval/retention/access policy.

Supply-chain OPEN includes actual product repository rules/review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN/origin deployment identity, secret/workload-identity model, exact CSP/Trusted Types feasibility for Flutter/PWA output, worker-response CSP/scope, DNS/provider recovery authority, credential/key rotation drills and compromised-worker repair on physical managed iPad.

# Next learning mode
092 closes the generic PWA release/update supply-chain trust contract. Avoid another generic supply-chain primer without new implementation evidence. Highest-value next work should consume Software Engineering execution evidence for actual CI/build/deploy/provenance or Design Studio runtime evidence when available. Otherwise examine the adjacent unresolved PWA trust boundary of **authentication/session compromise + offline authorization + security-sensitive cache/data separation during credential revocation/account recovery**, integrating 085 with 092 rather than repeating either. Continue Service Worker/WebKit/CSP/Trusted Types capability CHANGE WATCH.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–092 PASS**.
- PWA generic direct-sync, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline coexistence/retirement and release-supply-chain governance: sufficient for implementation handoff; product/device/AT/security/privacy validation OPEN.
- Reporting remains coarse/checkpoint-based.
