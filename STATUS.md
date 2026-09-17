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
100 PWA Trusted-State Persistence, Reset/Reinstall Bootstrap & Recovery — **PASS (generic) / PRODUCT STORAGE + BOOTSTRAP + TARGET-DEVICE VALIDATION OPEN**.

## 100 material findings
- the WHATWG storage model makes best-effort vs persistent storage meaningful, but persistent storage is a retention mode rather than a backup or independent security root;
- security trust state must be separated from reconstructible runtime state, authoritative local records, outbox, session state, cryptographic keys, backup/recovery metadata and diagnostics even when several classes physically share one origin bucket;
- `persisted() === true` does not prove trust state can never disappear: explicit user clearing, device loss/replacement, corruption and platform/application lifecycle events remain separate reset paths;
- missing anti-rollback memory is not equivalent to generation zero. Model it as unknown bootstrap state so reset cannot silently downgrade the client's prior trust boundary;
- fresh-device bootstrap, continuity bootstrap, reset/recovery bootstrap and restored-state bootstrap have different evidence and must not collapse into one `firstRun` state;
- restoring user records and restoring trust metadata are independent operations. Mixed-epoch restores can combine newer records with older trust metadata or outbox and therefore require coherence/reconciliation checks before replay;
- WebKit documents Home Screen web-app first-party exemption from ITP's seven-day script-writable-storage cap and StorageManager support from Safari/iOS/iPadOS 17-era releases, but this is not a universal managed-iPad durability or reinstall guarantee;
- exact Home Screen removal/re-add, Safari website-data clearing, storage pressure, OS/MDM lifecycle and backup behavior remain target-device OPEN;
- trust recovery should constrain the smallest unsafe bridge/replay capability while preserving locally authoritative records/outbox unless an explicit product/security requirement says otherwise.

## Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.  
`online signal ≠ usable network ≠ successful navigation ≠ task-ready application`.  
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.  
`worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`.  
`automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`.  
`persistent storage granted ≠ trust state can never disappear`.  
`same origin bucket ≠ same data authority ≠ same recovery policy`.  
`storage reset ≠ benign cache reset`.  
`PWA installed ≠ native uninstall/reinstall storage semantics`.  
`new device authenticated ≠ previous trusted-state continuity restored`.  
`backup restored ≠ trust state restored ≠ restored trust state current`.  
`trust state missing ≠ lowest generation trusted`.  
`trust state missing ≠ user records untrusted`.  
`anti-rollback memory lost ≠ local record should be deleted`.  
`rebootstrap required ≠ destructive reset required`.  
`restore completed ≠ records/trust/keys/outbox share one coherent recovery epoch`.  
`Home Screen ITP exemption ≠ universal durability guarantee`.  
`local durability ≠ backup availability ≠ trust continuity ≠ key recoverability ≠ sync correctness`.  
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
- **A Platform/Browser:** strong; supplied WHATWG Storage/StorageManager and WebKit Home Screen/storage mechanics. Exact managed-iPad reset/reinstall/storage-pressure/clearing behavior remains target-device evidence.
- **B UX/IA/Content:** consumes reset/rebootstrap states as truthful continuity/recovery requirements; trust-state loss must not be phrased as record corruption or automatic data loss.
- **C Performance/Accessibility/Quality:** owns mixed-epoch restore, missing trust state, reset timing, storage-clearing, stale-policy replay and accessible recovery negative evidence. Safari/AT/physical-device execution remains OPEN.
- **D Search/Discovery/Analytics:** discovery/config/analytics channels remain non-authoritative for security bootstrap.
- **E Architecture/Security/Operations:** current highest-risk owner; 100 closes the generic trusted-state-loss/reset bootstrap prerequisite. Product bootstrap and recovery architecture requires exact implementation evidence.

## Cross-repository evidence
Design Studio checked 2026-09-17: Web Design is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE; W051 batch partial-ack reconciliation is ready but execution remains OPEN. Its member-level reconciliation principle transfers to mixed recovery epochs, but no browser/device PASS is inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain Foundation IN STUDY. Q003's event-order matrix and D006 replication/sync work provide methods for future reset/recovery schedule validation; they do not prove browser/PWA persistence or production behavior.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention/removal/re-add behavior, worker/cache/update behavior, schema migration, storage pressure/clearing, accessible degraded/recovery UX, network isolation/VPN/proxy/content filtering, signaling/ICE/TURN, pairing/revocation, foreground/background behavior, outbox/protocol/API compatibility, backup/restore, PWA↔native transport, diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture, offline authorization, passkey/local-unlock design, locally authoritative record classes, encryption-at-rest threat model, DEK/KEK/recovery hierarchy, backup compatibility, device replacement/revocation, trust-state store, anti-rollback persistence and reset/rebootstrap evidence.

Runtime-origin/topology OPEN includes actual framework/rendering sinks, CSP/Reporting/Trusted Types, first/third-party script graph, analytics/ads/support widgets, origin/hostname topology, allowed network destinations, CORS/credential policy, `postMessage` bridges, iframe/sandbox/Permissions Policy, Storage Access behavior, worker script/scope, auth redirects, deep/native links, support/export handoffs, auth continuity, key/plaintext lifetime, bridge-policy generation and compromised-worker repair.

Trust-policy/control-plane OPEN includes exact security-critical policy assets, signing roles/keys, bootstrap trust material, canonical signed envelope, anti-rollback state, trusted-time assumptions, planned rotation, compromise-recovery authority, threshold/key custody, offline freshness policy, reset/reinstall bootstrap, restore provenance and whether same-origin runtime can bypass verification.

Supply-chain OPEN includes actual repository review enforcement, CI runner/action trust, dependency pinning, SBOM/provenance/signing, immutable artifact promotion, hosting/CDN deployment identity, secret/workload identity, DNS/provider recovery and credential/key rotation drills.

## Next learning mode
100 closes the generic trusted-state persistence/reset/rebootstrap prerequisite. Avoid inventing a product trust hierarchy without implementation/security evidence. Highest-value next work should consume exact implementation, Design Studio execution or Software Engineering evidence when available. Without it, the next adjacent question is **recovery provenance and mixed-epoch reconciliation**: how restored records, trust metadata, encryption-key generation, schema/protocol generation and outbox checkpoints from different times can be proven coherent or safely quarantined before replay. Reuse Software Engineering D003/D005/D006 rather than duplicate their foundations.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–100 PASS**.
- Generic PWA architecture now covers durability, platform capability, recovery/auth, direct transport, offline/update, diagnostics, release/incident, long-offline compatibility, supply-chain, key lifecycle, runtime-origin compromise, sensitive-context topology, trust bridges, stale-client revocation, trust-policy authenticity/authority recovery and trusted-state reset/rebootstrap.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
