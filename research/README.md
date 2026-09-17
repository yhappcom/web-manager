# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and related strategic web-app capability. Canonical curriculum: `../LEARNING_ROADMAP.md`; horizontal ownership: `../SPECIALIST_TRACKS.md`.

Evidence vocabulary: `SOURCE`, `SYNTHESIS`, `MINTTAP DECISION/DIRECTION`, `OPEN`, `DEPENDENCY`, `VALIDATION`, `CHANGE WATCH`, `TRANSFER VALIDATION`, `CONTRADICTION`.

## Sequential curriculum — COMPLETE
- Stage 1 Web Foundations: 027–033 — **PASS**
- Stage 2 Website Anatomy / Content / IA: 034–038 — **PASS**
- Stage 3 UX & Interaction: 039–044 — **PASS**
- Stage 4 Web Design Literacy: 045–050 — **PASS**
- Stage 5 Accessibility: 051–058 — **PASS**
- Stage 6 Search / Discovery / Content Quality: 059–065 — **PASS**
- Stage 7 Performance / Browser Runtime: 066–070 — **PASS**
- Stage 8 Security / Privacy / Trust: 071–072 — **PASS**
- Stage 9 Analytics / Experimentation: 075–076 — **PASS**
- Stage 10 App-Company Web Strategy & Growth: 077–078 — **PASS**
- Stage 11 Web Operations & Platform Architecture: 079–080 — **PASS**
- Stage 12 Advanced / Expert Web Management: 081–082 — **PASS / FINAL CURRICULUM GATE**

Curriculum passes are competency gates, not production certification.

## Continuous expert maintenance/application
083 — **PWA Storage Durability & Service-Worker Standards Change Watch — PASS.** Persistence, quota, eviction, independent backup and restore boundaries.  
084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS.** Home Screen/install behavior, Push/Badging vs background execution, Background Sync limits and auth-state separation.  
085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS.** Recovery, offline identity/session/local-unlock/authorization boundaries, device-loss/logout/revocation conflicts and export→restore lifecycle.  
086 — **PWA Direct Transport, Discovery, Pairing & Security Boundaries — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
087 — **PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
088 — **PWA Offline Navigation, Service-Worker Update Recovery & Observability — PASS (generic) / PRODUCT VALIDATION OPEN.**  
089 — **PWA Testing, Diagnostics & Release Evidence Architecture — PASS (generic) / TARGET-DEVICE EXECUTION OPEN.**  
090 — **PWA Release, Support & Incident Evidence + Accessible Recovery Contract — PASS (generic) / TARGET-DEVICE & AT EXECUTION OPEN.**  
091 — **PWA Long-Offline Release Coexistence, API Retirement & Incident Containment — PASS (generic) / PRODUCT EXECUTION OPEN.**  
092 — **PWA Release/Update Supply-Chain Integrity & Secure Deployment Trust — PASS (generic) / PRODUCT IMPLEMENTATION VALIDATION OPEN.** Worker/update channel as privileged deployment; source→dependency→build→artifact→publication evidence and compromised-worker recovery.  
093 — **PWA Session Revocation, Offline Authorization & Security-Sensitive Local Data Separation — PASS (generic) / PRODUCT AUTHORIZATION + DEVICE VALIDATION OPEN.** Identity/session/local-unlock/offline-authorization separation and destructive-cleanup gates.  
094 — **PWA Account/Device Recovery & Cryptographic Key Lifecycle — PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN.** Account/authenticator/device/data/backup/sync recovery and key lifecycle boundaries.  
095 — **PWA XSS/Origin Compromise Against Unlocked Data & Key-Use Authority — PASS (generic) / PRODUCT IMPLEMENTATION + TARGET-DEVICE VALIDATION OPEN.** Encryption-at-rest vs hostile same-origin runtime, CSP/Trusted Types, worker persistence and key/plaintext lifetime.  
096 — **PWA Sensitive-Context Origin, Third-Party Isolation & Capability Minimization — PASS (generic) / PRODUCT TOPOLOGY + TARGET-DEVICE VALIDATION OPEN.** Separates URL paths from browser origins; evaluates same-origin policy separation vs separate sensitive-app origin; integrates Service Worker scope, CSP/connect/frame controls, iframe sandbox, Permissions Policy, storage-access/credential bridges, analytics/advertising authority budgets, auth continuity and exact-artifact validation without inferring current MintTap/LogMate topology.

## Key guards
- `storage API available ≠ persistence granted ≠ backup ≠ tested restore`;
- reconstructible cache assets ≠ irreplaceable user records/outbox;
- `online signal ≠ usable network ≠ successful navigation ≠ task-ready application`;
- `worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`;
- `automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`;
- `Home Screen installed ≠ offline-capable ≠ background-sync capable`;
- `previously authenticated ≠ server session currently valid ≠ local data currently unlocked ≠ offline operation authorized ≠ pending mutation remotely accepted`;
- `credential revoked at server ≠ disconnected PWA instantly aware ≠ local data instantly inaccessible`;
- `logout ≠ origin wipe`;
- `account recovery ≠ authenticator recovery ≠ device recovery ≠ local-data recovery ≠ backup recovery ≠ synchronization recovery`;
- `credential rotation ≠ data-encryption-key rotation ≠ re-encryption ≠ old-device revocation`;
- `new device authorized ≠ old offline device contained`;
- `HTTP cache policy ≠ application-data authorization policy`;
- `HTTPS + same-origin storage ≠ complete device-loss/XSS/data-at-rest security`;
- `Web Crypto available ≠ safe encryption/key-recovery architecture established`;
- `encrypted at rest ≠ protected from authorized same-origin script while unlocked`;
- `non-extractable key ≠ unusable cryptographic capability`;
- `same-origin isolation ≠ isolation from hostile code executing as that origin`;
- `CSP/Trusted Types reduce injection risk ≠ origin compromise becomes harmless`;
- `different path ≠ different origin security boundary`;
- `narrow Service Worker scope ≠ independent origin isolation`;
- `CSP destination minimization ≠ malicious same-origin code loses all application authority`;
- `sandbox attribute present ≠ embedded third party safely contained`;
- `cross-origin iframe ≠ no cookie/storage relationship`;
- `different origin ≠ no trust bridge`;
- `third-party business value ≠ requirement for sensitive-context execution authority`;
- `measurement continuity ≠ shared script authority`;
- `analytics queue ≠ authoritative application outbox`;
- `PWA installed from site ≠ Service Worker should control the entire site`;
- `SSO convenience ≠ every web origin should receive the same session credential`;
- `saved locally ≠ synchronized ≠ backed up ≠ restorable`;
- `RTCDataChannel available ≠ signaling/discovery/pairing/background correctness`;
- `same LAN ≠ peer reachability`;
- `deprecation signal delivered ≠ every installed client informed ≠ migration completed`;
- `remote kill switch configured ≠ offline client contained`;
- `server compatible ≠ local schema compatible ≠ queued operation replayable`;
- `cannot diagnose ≠ user should clear storage`;
- `HTTPS delivered ≠ intended artifact delivered ≠ authorized artifact built ≠ dependency graph uncompromised`;
- `page CSP strong ≠ service-worker CSP strong`;
- `commit SHA known ≠ deployed bytes proven`;
- `origin repaired ≠ installed fleet clean`;
- generic platform evidence ≠ managed-EFB product validation.

Generic PWA architecture through sensitive-context topology is sufficient for implementation handoff. Product feasibility requires executable exact-artifact evidence on target managed devices and applicable assistive-technology/security/privacy/operational validation.

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations — PASS.**  
074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

075–096 transfer measurement, portfolio, release, operations, expert governance, durability, iOS/iPadOS capability, recovery/offline-auth, direct transport, managed-network establishment, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline compatibility/retirement, release-supply-chain, session/offline-authorization, account/device/key-recovery, runtime-origin-compromise and sensitive-context isolation governance. Production/device validation remains OPEN.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns task/information/state structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability/measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates portfolio decisions.

Design Studio remains canonical for reusable visual/interaction evidence. Marketing owns acquisition/channel/community strategy. Software Engineering owns implementation/code/runtime validation. Use explicit handoffs and evidence boundaries.

## Study quality standard
Substantial work includes precise vocabulary, first-principles mechanics, authoritative evidence, counterexamples/failure analysis, cross-domain effects, bounded project relevance, durable-vs-changeable classification, validation requirements and explicit decision ownership.
