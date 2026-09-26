# 293 — PWA ↔ Native Mobile Synchronization Authority & Transport Boundary

Status: **PASS (generic) / PRODUCT TRANSPORT + MANAGED-IPAD + PHYSICAL-DEVICE EXECUTION OPEN**  
Date: 2026-09-27  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 289 queue re-adjudication; 290 physical-iPad D/L/S/U evidence; 291 managed-iPad M0–M8 envelope; 292 L/H/I/S/R/A/Q/C authority model; Track A browser/network mechanics; Track C physical validation.

## Purpose
Define what must be true before a LogMate-like iPad PWA can safely exchange offline work with a native mobile companion, without assuming direct peer discovery, unattended background execution, hotspot reachability, persistent connectivity, or that transport success confers synchronization authority.

Central rule: **peer transport availability is not peer identity, authorization, acknowledgement, convergence, backup, or unattended synchronization.**

## SOURCE
- W3C WebRTC Recommendation update (2025-03-13): https://www.w3.org/news/2025/updated-w3c-recommendation-webrtc-real-time-communication-in-browsers/
- MDN Background Synchronization API (current; limited availability): https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API
- MDN Periodic Background Synchronization API (current; limited availability/experimental): https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API
- WebKit Service Worker implementation history: https://webkit.org/blog/8090/workers-at-your-service/
- Apple Local Network Privacy documentation: https://developer.apple.com/documentation/analytics-reports/local-network-privacy
- Apple background execution modes for native apps: https://developer.apple.com/documentation/xcode/configuring-background-execution-modes
- Apple ATS local-networking key: https://developer.apple.com/documentation/bundleresources/information-property-list/nsapptransportsecurity/nsallowslocalnetworking

## History / problem
Offline-first products naturally suggest “sync the iPad directly to the phone.” That phrase collapses several independent problems: discovery, network path, peer authentication, pairing/bootstrap, transport confidentiality/integrity, authorization, replay/idempotency, schema compatibility, conflict handling, acknowledgement, convergence, background execution and recovery.

WebRTC standardizes browser APIs capable of carrying generic application data to another browser/device implementing the corresponding protocols. That proves a standards-level transport capability, not automatic peer discovery, permissionless LAN access, background availability, product pairing, or trustworthy synchronization.

Browser Background Sync and Periodic Background Sync cannot be assumed as a universal solution. MDN marks both as limited availability, with Periodic Background Sync experimental. A LogMate-like product therefore cannot make unattended PWA↔native synchronization a product guarantee merely from these APIs' existence.

Native iOS/iPadOS background execution is also constrained: Apple states apps are typically suspended in the background and only limited background modes permit additional execution. Native capability is not evidence that a Home Screen web app receives the same execution contract.

## Five-track allocation
- **A Platform/Browser:** owns WebRTC/browser networking, Service Worker lifecycle, online/foreground mechanics and feature detection.
- **B UX/IA:** owns explicit pairing, pending/local-only, peer-unavailable, reauthentication/re-pairing, conflict and confirmed-convergence states.
- **C Quality:** owns representative Safari/Home Screen + native-device validation, interruption/restart/hotspot/network-transition testing and accessibility/human evidence.
- **D Discovery/Analytics:** may measure pairing/sync outcomes but telemetry is not peer identity or authority.
- **E Architecture/Security/Ops:** owns trust bootstrap, device identity, transport authorization, replay/consequence controls, convergence, recovery and operational lifecycle.

## Independent synchronization boundary
Record these independently; do not compress them into “sync works”:

1. **D — Discovery:** how the PWA learns a candidate native peer or rendezvous endpoint.
2. **N — Network path:** LAN, hotspot, Internet/rendezvous, relay or other verified path exists under the current managed-device envelope.
3. **P — Peer identity:** cryptographic/application evidence binds the counterparty to the intended device/account/installation.
4. **B — Bootstrap/pairing:** first trust is established through an explicit, replay-resistant product flow.
5. **T — Transport security:** confidentiality/integrity and endpoint expectations are satisfied for the selected transport.
6. **A — Current authority:** this peer is currently authorized for this operation/consequence.
7. **V — Version/schema compatibility:** payload semantics can be interpreted without silently weakening current rules.
8. **Q — Queue/replay disposition:** duplicate, delayed and previously queued operations are re-adjudicated.
9. **K — Acknowledgement:** the intended peer/authority has durably accepted the operation according to the protocol.
10. **C — Convergence:** conflicts/projections are reconciled and semantic agreement is proven.
11. **X — Execution opportunity:** both sides actually receive sufficient foreground/background execution opportunity for the claimed workflow.
12. **R — Recovery:** interrupted pairing/transfer/update can resume or fail safely without destroying unique local work.

Positive evidence for one dimension does not establish another.

## Transport classes
### Direct local transport
A local path can reduce Internet dependency but creates separate discovery, local-network/privacy, hotspot/topology, TLS/identity and managed-network questions. A reachable IP/hostname or open connection is not trusted peer identity.

### WebRTC/data-channel style transport
WebRTC is a standards-level candidate for generic application data transport. It still requires product-defined signaling/rendezvous, peer identity/bootstrap, authorization, replay semantics, compatibility and convergence. ICE/connection success is not application trust.

### Server-mediated synchronization
A server/rendezvous path may simplify device discovery and authority adjudication but introduces Internet reachability, server availability, account/session, retention/privacy and operational dependencies. It is not “direct device-to-device.”

### Export/import or user-mediated transfer
Explicit package transfer can be a defensible recovery/interchange mechanism without promising automatic synchronization. Existing provenance/import guards remain: package verified ≠ records admitted ≠ remote mutation authorized.

No class is selected for LogMate by this generic study.

## Background/unattended boundary
- Service Worker existence does not imply persistent execution.
- Background Sync is limited-availability and must be feature-detected/validated on target platforms.
- Periodic Background Sync is limited-availability and experimental; do not make it a cross-platform product prerequisite.
- Native iOS background modes are a native-app execution contract and do not transfer to a PWA.
- Therefore **foreground/rejoin-driven synchronization is the safe generic baseline until representative target-device evidence establishes stronger behavior.**
- “Eventually when both apps are open/active and a verified path exists” and “unattended automatic background sync” are materially different product promises.

## Hotspot and local-network boundary
Do not infer that two devices associated through a hotspot can discover or reach each other in the required direction. Validate topology, addressability, isolation policy, managed-network restrictions and product transport on representative devices. Apple local-network privacy evidence applies to native app access decisions, but generic documentation does not establish the exact permission/prompt model for a Home Screen PWA. Keep PWA-specific local-network behavior **OPEN** until physical Safari/Home Screen testing.

## Trust bootstrap
A safe pairing design needs evidence for:
1. who initiated pairing;
2. which device/account/install identity is being bound;
3. freshness/non-replay of bootstrap material;
4. user-visible confirmation where consequence requires it;
5. key/credential storage and rotation;
6. unpair/revocation/lost-device behavior;
7. replacement-device succession without inheriting obsolete authority;
8. recovery that preserves unique records without silently transferring authority credentials.

QR code, short code, proximity or same-account presence are UX/bootstrap carriers, not proof of secure pairing by themselves.

## Rejoin and operation adjudication
For each transferred operation:
1. preserve source provenance and unique local data;
2. establish current peer/path/trust;
3. establish current account/device/session admission where applicable;
4. map old payload/schema to current semantics;
5. classify current consequence;
6. re-adjudicate authority;
7. apply replay/idempotency/conflict controls;
8. require acknowledgement;
9. prove semantic convergence;
10. retain rejected/quarantined work with explainable provenance.

This consumes 292 rather than replacing it.

## Failure modes
- both devices online but cannot discover one another;
- candidate peer reachable but wrong/untrusted;
- hotspot/LAN topology changes mid-transfer;
- PWA is backgrounded/suspended before completion;
- native peer is suspended;
- signaling works while data path fails;
- data path works while current authorization fails;
- old paired device returns after replacement/revocation;
- duplicate/replayed transfer after ambiguous acknowledgement;
- schema generation differs;
- acknowledgement exists but conflict remains;
- management policy changes proxy/filter/network behavior;
- device restart or OS/WebKit update interrupts state;
- user deletes/evicts local web data before convergence.

## Persistent guards
- `transport supported ≠ transport available now`;
- `transport available ≠ peer discovered`;
- `peer discovered ≠ peer authenticated`;
- `same LAN/hotspot ≠ mutual reachability`;
- `WebRTC connection established ≠ trusted product peer`;
- `same account ≠ same device lineage`;
- `paired once ≠ currently authorized`;
- `native background capability ≠ PWA background capability`;
- `Service Worker exists ≠ persistent background execution`;
- `Background Sync API exists ≠ Safari/iPadOS product guarantee`;
- `foreground sync works ≠ unattended sync works`;
- `bytes transferred ≠ operation admitted`;
- `operation admitted ≠ acknowledged`;
- `acknowledged ≠ converged`;
- `direct transfer ≠ backup`;
- `server-mediated sync ≠ device-to-device sync`;
- `QR/short code matched ≠ secure pairing proven`;
- `hotspot connected ≠ peer path proven`;
- `telemetry says success ≠ trust/convergence independently proven`.

## Track C destructive additions — defined, not executed
1097. **Transport→trust composition:** successful connection treated as authenticated peer identity.  
1098. **LAN/hotspot reachability assumption:** association treated as bidirectional product reachability.  
1099. **Foreground→background promotion:** foreground transfer PASS treated as unattended background PASS.  
1100. **Native→PWA background equivalence:** native execution capability transferred to Home Screen PWA.  
1101. **Pairing permanence:** once-paired peer remains authorized after revocation/replacement/policy transition.  
1102. **Discovery→identity composition:** discovered endpoint treated as intended device.  
1103. **Signaling→data-path composition:** rendezvous/signaling PASS treated as payload path PASS.  
1104. **Transfer→admission composition:** received bytes treated as currently authorized mutation.  
1105. **ACK→convergence composition:** transfer acknowledgement treated as conflict/convergence closure.  
1106. **Schema-compatibility grandfathering:** old peer generation bypasses current consequence semantics.  
1107. **Interruption data-loss:** backgrounding/restart/path loss destroys unique unsynchronized work.  
1108. **Direct-sync→backup composition:** peer copy treated as independently recoverable backup.

All are **DEFINED / NOT EXECUTED**.

## TRANSFER VALIDATION / CONTRADICTION
- 290 supplies physical lifecycle/storage/update evidence classes.
- 291 supplies managed-network/trust envelope; a peer path that works unmanaged cannot be promoted to managed-company-iPad.
- 292 supplies current authority and queue re-adjudication; peer transfer cannot grandfather offline authority.
- Software Engineering should own concrete signaling/protocol/crypto/state-machine implementation and executable harnesses after a product transport is selected.
- Design Studio should consume explicit pairing/recovery/conflict states if/when the product chooses this capability; no visual pattern is prescribed here.
- Marketing must not promise automatic/offline/background cross-device sync before product evidence supports that exact claim.

## CHANGE WATCH
Recheck WebKit/Safari support for Background Sync, Periodic Background Sync, local-network-related browser behavior, WebRTC implementation differences and Home Screen web-app lifecycle before product commitment. Feature support is not timeless.

## VALIDATION / OPEN
Actual LogMate/MintTap PWA/native architecture, selected transport, signaling/rendezvous, pairing, credentials, native background modes, Safari/Home Screen local-network behavior, hotspot topology, MDM policy, device fleet, conflict model and recovery design remain **OPEN**.

Production claims require representative physical managed-iPad + native-mobile evidence. Generic standards and browser documentation are prerequisite evidence only.

## MINTTAP DECISION / DIRECTION
Do not make direct unattended PWA↔native synchronization an architectural assumption. Treat foreground/rejoin-driven synchronization through a verified transport as the generic baseline until stronger target-platform evidence exists. If direct peer sync becomes a product requirement, require explicit D/N/P/B/T/A/V/Q/K/C/X/R evidence and preserve a user-mediated recovery/export path independent of peer availability.

Next high-value work: convert this boundary plus 290–292 into an executable representative-device validation matrix/handoff, including foreground transfer, interruption, hotspot/network transitions, peer revocation/replacement, mixed schema generation and convergence evidence.
