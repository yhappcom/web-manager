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
Current W3C/WebKit/Storage evidence; persistence, quota, eviction, independent backup and restore boundaries.

084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS.**  
Current Home Screen/install behavior, Push/Badging vs general background execution, Background Sync limits, cookie-copy semantics and offline-auth state separation.

085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS.**  
Recovery Contract, offline identity/session/local-unlock/authorization boundaries, WebAuthn/Web Crypto limits, XSS/client-storage risk, device-loss/logout/revocation conflicts, export→restore lifecycle and safety-critical Saved/Sync/Backup state semantics.

086 — **PWA Direct Transport, Discovery, Pairing & Security Boundaries — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
Separates server transports from WebRTC peer data transport and transport from discovery/signaling, reachability, pairing identity, background execution and sync correctness.

087 — **PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
Signaling/offer-answer/ICE/STUN/TURN, NAT/firewall/network isolation, ICE restart, managed-network boundaries and managed-iPad/native-phone experiment matrix.

088 — **PWA Offline Navigation, Service-Worker Update Recovery & Observability — PASS (generic) / PRODUCT VALIDATION OPEN.**  
Navigation failure states, worker update/control boundaries, cache ownership, skipped-version recovery, privacy-minimized observability, accessible recovery UX and failure injection.

089 — **PWA Testing, Diagnostics & Release Evidence Architecture — PASS (generic) / TARGET-DEVICE EXECUTION OPEN.**  
Four-tier evidence system, Chromium-vs-Safari worker-test boundaries, fault injection, state/data release invariants, privacy-minimized diagnostic bundles and implementation handoff.

090 — **PWA Release, Support & Incident Evidence + Accessible Recovery Contract — PASS (generic) / TARGET-DEVICE & AT EXECUTION OPEN.**  
Connects exact-artifact release acceptance to Safari/Home-Screen inspection boundaries, privacy-safe support diagnostics, correlation-ID minimization, accessible saved/sync/update/recovery state requirements, telemetry blind spots, incident evidence preservation and rollback-schema compatibility. Consumes Design Studio W040 boundary and Software Engineering D003 compatibility evidence without duplicating their disciplines.

Key guards:
- `storage API available ≠ persistence granted ≠ backup ≠ tested restore`;
- reconstructible cache assets ≠ irreplaceable user records;
- `online signal ≠ usable network ≠ successful navigation ≠ task-ready application`;
- `worker update found ≠ installed ≠ activated ≠ controlling ≠ application-compatible`;
- `automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`;
- `Safari diagnostic capability documented ≠ managed-EFB diagnostic workflow permitted`;
- `release deployed ≠ release accepted ≠ product recovery validated`;
- `rendered page/HTTP 200 ≠ PWA state/data invariant satisfied`;
- `navigation preload ≠ offline fallback ≠ cache correctness`;
- `Home Screen installed ≠ offline-capable ≠ background-sync capable`;
- `push event execution ≠ arbitrary background execution`;
- `previously authenticated ≠ currently server-authorized ≠ indefinitely authorized offline`;
- `HTTPS + same-origin storage ≠ complete device-loss/XSS/data-at-rest security`;
- `Web Crypto available ≠ safe encryption/key-recovery architecture established`;
- `saved locally ≠ synchronized ≠ backed up ≠ restorable`;
- `WebSocket/WebTransport available ≠ nearby peer discovery`;
- `RTCDataChannel available ≠ signaling/discovery/pairing/background correctness`;
- `paired identity ≠ current address/current ICE state`;
- `STUN reachable ≠ peer reachable`;
- `TURN success ≠ direct P2P`;
- `same LAN ≠ peer reachability`;
- `cannot diagnose ≠ user should clear storage`;
- generic platform evidence ≠ managed-EFB product validation.

Generic direct-sync establishment, offline/update/recovery, testing/diagnostic and release/support/incident architecture are sufficient for implementation handoff. Product feasibility requires executable exact-artifact evidence on target managed devices and applicable assistive-technology/security/privacy/operational validation.

## Stage 12 — Advanced / Expert Web Management — COMPLETE
081 — **Expert Web Management Decision Governance — PASS.**  
082 — **Portfolio Governance, Learning & Platform Evolution — PASS / FINAL GATE.**

## Strategic cross-track specialization — PWA
073 — **PWA Cross-Track Foundations — PASS.**  
074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

075–090 transfer measurement, portfolio, release, operations, expert governance, durability, current iOS/iPadOS capability, recovery/offline-auth, direct transport, managed-network establishment, offline/update/recovery, testing/diagnostics and release/support/incident governance. Production/device validation remains OPEN.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns task/information/state structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability/measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates portfolio decisions.

Design Studio remains canonical for reusable visual/interaction evidence. Marketing owns acquisition/channel/community strategy. Software Engineering owns implementation/code/runtime validation. Use explicit handoffs and evidence boundaries.

## Study quality standard
Substantial work includes precise vocabulary, first-principles mechanics, authoritative evidence, counterexamples/failure analysis, cross-domain effects, bounded project relevance, durable-vs-changeable classification, validation requirements and explicit decision ownership.
