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
083 — **PWA Storage Durability & Service-Worker Standards Change Watch — PASS.**  
084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS.**  
085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS.**  
086 — **PWA Direct Transport, Discovery, Pairing & Security Boundaries — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
087 — **PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
088 — **PWA Offline Navigation, Service-Worker Update Recovery & Observability — PASS (generic) / PRODUCT VALIDATION OPEN.**  
089 — **PWA Testing, Diagnostics & Release Evidence Architecture — PASS (generic) / TARGET-DEVICE EXECUTION OPEN.**  
090 — **PWA Release, Support & Incident Evidence + Accessible Recovery Contract — PASS (generic) / TARGET-DEVICE & AT EXECUTION OPEN.**  
091 — **PWA Long-Offline Release Coexistence, API Retirement & Incident Containment — PASS (generic) / PRODUCT EXECUTION OPEN.**  
092 — **PWA Release/Update Supply-Chain Integrity & Secure Deployment Trust — PASS (generic) / PRODUCT IMPLEMENTATION VALIDATION OPEN.**  
093 — **PWA Session Revocation, Offline Authorization & Security-Sensitive Local Data Separation — PASS (generic) / PRODUCT AUTHORIZATION + DEVICE VALIDATION OPEN.**  
094 — **PWA Account/Device Recovery & Cryptographic Key Lifecycle — PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN.**  
095 — **PWA XSS/Origin Compromise Against Unlocked Data & Key-Use Authority — PASS (generic) / PRODUCT IMPLEMENTATION + TARGET-DEVICE VALIDATION OPEN.**  
096 — **PWA Sensitive-Context Origin, Third-Party Isolation & Capability Minimization — PASS (generic) / PRODUCT TOPOLOGY + TARGET-DEVICE VALIDATION OPEN.**  
097 — **PWA Explicit Cross-Context Trust Bridges — PASS (generic) / PRODUCT BRIDGE + TARGET-DEVICE VALIDATION OPEN.** Defines least-authority contracts for `postMessage`, credentialed CORS/API, auth redirects, Universal Links/deep links and support/export/sync/measurement handoffs.  
098 — **PWA Bridge Revocation, Stale-Client Trust & Data-Preserving Containment — PASS (generic) / PRODUCT REVOCATION + TARGET-DEVICE VALIDATION OPEN.** Separates remote authority revocation from disconnected-client knowledge; requires current-trust revalidation before replay while preserving authoritative local records/outbox.  
099 — **PWA Trust-Policy Authenticity, Authority Recovery & Anti-Rollback Boundaries — PASS (generic) / PRODUCT CRYPTOGRAPHIC + CONTROL-PLANE VALIDATION OPEN.** Separates HTTPS delivery from independent policy authority; integrates signed semantic context, bootstrap, key-transition, rollback/freeze/fast-forward and long-offline recovery boundaries.  
100 — **PWA Trusted-State Persistence, Reset/Reinstall Bootstrap & Recovery — PASS (generic) / PRODUCT STORAGE + BOOTSTRAP + TARGET-DEVICE VALIDATION OPEN.** Separates browser persistence from backup/security trust continuity; models missing anti-rollback state, reset/reinstall/new-device bootstrap, mixed restore epochs and data-preserving containment.

## Key guards
- `storage API available ≠ persistence granted ≠ backup ≠ tested restore`;
- `persistent storage granted ≠ trust state can never disappear`;
- `same origin bucket ≠ same data authority ≠ same recovery policy`;
- `storage reset ≠ benign cache reset`;
- `PWA installed ≠ native uninstall/reinstall storage semantics`;
- `new device authenticated ≠ previous trusted-state continuity restored`;
- `backup restored ≠ trust state restored ≠ restored trust state current`;
- `trust state missing ≠ lowest generation trusted`;
- `trust state missing ≠ user records untrusted`;
- `anti-rollback memory lost ≠ local record should be deleted`;
- `rebootstrap required ≠ destructive reset required`;
- `restore completed ≠ records/trust/keys/outbox share one coherent recovery epoch`;
- `Home Screen ITP exemption ≠ universal durability guarantee`;
- `local durability ≠ backup availability ≠ trust continuity ≠ key recoverability ≠ sync correctness`;
- reconstructible cache assets ≠ irreplaceable user records/outbox;
- `online signal ≠ usable network ≠ successful navigation ≠ task-ready application`;
- `worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`;
- `automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`;
- `authority revoked remotely ≠ disconnected client informed ≠ local capability immediately unavailable`;
- `network restored ≠ trust restored ≠ replay authorized`;
- `sync denied ≠ local record should be deleted`;
- `outbox replay paused ≠ outbox discarded`;
- `stale trust metadata ≠ corrupted user data`;
- `HTTPS policy fetch succeeded ≠ policy authorized by an independent trust root`;
- `signature mathematically valid ≠ signer authorized for this policy`;
- `valid old signature ≠ current policy`;
- `signed payload ≠ signed interpretation context`;
- `SubtleCrypto.verify available ≠ trustworthy policy-update system established`;
- `public key fetched from compromised origin ≠ independent authenticity proof`;
- `successor signed only by compromised key ≠ compromise recovery proven`;
- `monotonic version check ≠ freeze resistance`;
- `expiry check ≠ trustworthy wall clock`;
- `policy expired ≠ local records expired`;
- `new signed policy accepted ≠ compromised worker/runtime repaired`;
- `logout ≠ origin wipe`;
- `account recovery ≠ authenticator recovery ≠ device recovery ≠ local-data recovery ≠ backup recovery ≠ synchronization recovery`;
- `encrypted at rest ≠ protected from authorized same-origin script while unlocked`;
- `non-extractable key ≠ unusable cryptographic capability`;
- `different path ≠ different origin security boundary`;
- `narrow Service Worker scope ≠ independent origin isolation`;
- `different origin ≠ no trust bridge`;
- `postMessage origin validated ≠ message authorized ≠ payload semantically valid ≠ transaction current`;
- `CORS allowed ≠ caller authenticated ≠ caller authorized ≠ mutation safe`;
- `Universal Link association valid ≠ deep-link payload authorized`;
- `third-party business value ≠ requirement for sensitive-context execution authority`;
- `measurement continuity ≠ shared script authority`;
- `analytics queue ≠ authoritative application outbox`;
- `RTCDataChannel available ≠ signaling/discovery/pairing/background correctness`;
- `remote kill switch configured ≠ offline client contained`;
- `server compatible ≠ local schema compatible ≠ queued operation replayable`;
- `cannot diagnose ≠ user should clear storage`;
- `HTTPS delivered ≠ intended artifact delivered ≠ authorized artifact built ≠ dependency graph uncompromised`;
- `page CSP strong ≠ service-worker CSP strong`;
- `commit SHA known ≠ deployed bytes proven`;
- `origin repaired ≠ installed fleet clean`;
- generic platform evidence ≠ managed-EFB product validation.

Generic PWA architecture through trusted-state reset/rebootstrap is sufficient for implementation handoff. Product feasibility requires executable exact-artifact evidence on target managed devices and applicable security/privacy/accessibility/operational validation.

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations — PASS.**  
074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

075–100 transfer measurement, portfolio, release, operations, expert governance, durability, iOS/iPadOS capability, recovery/offline-auth, direct transport, managed-network establishment, offline/update/recovery, testing/diagnostics, release/support/incident, long-offline compatibility/retirement, release-supply-chain, session/offline-authorization, account/device/key-recovery, runtime-origin-compromise, sensitive-context isolation, explicit trust-bridge governance, stale-client revocation/containment, trust-policy authenticity/authority recovery and trusted-state reset/rebootstrap. Production/device validation remains OPEN.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns task/information/state structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability/measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates portfolio decisions.

Design Studio remains canonical for reusable visual/interaction evidence. Marketing owns acquisition/channel/community strategy. Software Engineering owns implementation/code/runtime validation. Use explicit handoffs and evidence boundaries.

## Study quality standard
Substantial work includes precise vocabulary, first-principles mechanics, authoritative evidence, counterexamples/failure analysis, cross-domain effects, bounded project relevance, durable-vs-changeable classification, validation requirements and explicit decision ownership.
