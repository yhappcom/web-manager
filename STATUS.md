# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification.

# Continuous expert maintenance checkpoints
083 — **PWA Storage Durability & Service-Worker Standards Change Watch — PASS.**  
084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS.**  
085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS.**  
086 — **PWA Direct Transport, Discovery, Pairing & Security Boundaries — PASS (generic) / PRODUCT FEASIBILITY OPEN.**  
087 — **PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract — PASS (generic) / PRODUCT FEASIBILITY OPEN.**

## 087 material findings
- WebRTC establishment is a system: intended peer identity → signaling → offer/answer → ICE candidate gathering/exchange → connectivity checks → selected candidate pair → encrypted DataChannel → application authentication/acknowledgement/reconciliation.
- Persistent pairing identity is not a persistent network route. Fresh signaling/ICE can be required after network change, suspension/process restart or ICE restart.
- STUN can expose NAT-mapped reachability information; it is not a relay and does not guarantee peer reachability. TURN supplies relay candidates when direct paths are unavailable.
- `P2P payload path ≠ infrastructure-free system`; signaling and STUN/TURN may still be required. `TURN relay ≠ application-record authority`, but relay use still has privacy, cost, availability and metadata consequences.
- Same LAN and Internet availability are not sufficient feasibility evidence. Client isolation, firewall, NAT, VPN, proxy/content filtering, MDM/network policy and browser/container behavior are independent axes.
- Apple documents local-network privacy/management controls for native/managed apps, but those controls do not establish equivalent Safari/Home-Screen PWA behavior. Exact managed-PWA behavior remains target-device evidence.
- A successful connection once does not establish durable reconnect. `restartIce()` itself still requires renegotiation/signaling.
- Direct WebRTC remains an opportunistic transport inside the durability contract, not the durability foundation.
- Candidate architecture classes now distinguish server application sync, server signaling + STUN/direct WebRTC, signaling + STUN/TURN direct-or-relayed WebRTC, and explicit export/import recovery.
- A target-device experiment matrix is now defined for same LAN, isolated LAN, separate networks, cellular/managed Wi-Fi, VPN/proxy/content-filter, offline/reconnect, airplane-mode transitions, STUN-only, TURN fallback, signaling loss, suspension/process restart, network change and long-offline return.

# Persistent PWA guards
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore`.
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

# Five-track state
All tracks have integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong; 087 closes the generic ICE/STUN/TURN/signaling/restart prerequisite needed to interpret direct-peer claims.
- **B UX/IA/Content:** consumes pairing/connection/pending/retry/recovery semantics; invisible-sync claims remain prohibited without runtime evidence.
- **C Performance/Accessibility/Quality:** exact browser/device, degraded-network, suspension/reconnect and accessible recovery evidence remains OPEN.
- **D Search/Discovery/Analytics:** strong; may measure connection/candidate/ack states with minimized metadata but analytics cannot certify durability.
- **E Architecture/Security/Operations:** highest-consequence PWA owner; 087 now converts remaining direct-sync uncertainty into managed-network and fallback acceptance tests rather than more generic transport theory.

# Cross-repository evidence
Design Studio Web Design latest checked 2026-09-16: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W038 compensation-race transfer contract ready but execution OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering owns executable signaling/ICE/TURN/STUN implementation, native peer behavior, credential/key design, protocol/idempotency/reconnect, schema/outbox/reconciliation, backup/import and target-device experiments. Web Manager now supplies the 087 experiment/acceptance contract rather than duplicating implementation research.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy, Home Screen retention, network isolation/VPN/proxy/content filtering, actual local-network permission behavior for the PWA container, signaling reachability, selected ICE candidate behavior, TURN requirement/cost/privacy, pairing credential persistence/revocation, foreground/background/suspension behavior, native-phone counterpart behavior, LogMate schema/outbox/protocol, independent backup/restore and direct unattended PWA↔native transport.

# Next learning mode
The generic direct-transport primer is no longer the bottleneck. **Highest-value next step for LogMate direct sync is implementation/target-device evidence from Software Engineering using the 087 matrix.** Until that evidence exists, do not manufacture feasibility conclusions.

For autonomous Web Manager study without new implementation evidence, rotate to the next high-value PWA cross-track gap rather than repeating WebRTC: **offline/cache navigation failure architecture + service-worker update/recovery observability and accessible degraded-state UX**, with current Safari/WebKit vs Chromium evidence and long-offline EFB failure cases. Preserve the transport-agnostic durability contract.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–087 PASS**.
- PWA direct-sync generic establishment knowledge: sufficient for handoff; product/device validation OPEN.
- Reporting remains coarse/checkpoint-based.
