# 087 — PWA WebRTC Establishment, Managed-Network Reality & Fallback Experiment Contract

Status: **PASS — generic establishment/reliability knowledge / PRODUCT FEASIBILITY OPEN**  
Date: 2026-09-16

## Purpose
Continue 086 at the highest-value unresolved boundary: a WebRTC DataChannel primitive exists, but can the exact EFB PWA and native phone establish and re-establish a usable channel across real network policy? This checkpoint separates signaling, ICE, STUN, TURN, NAT/firewall behavior, local-network policy, suspension/restart and fallback correctness, then converts the uncertainty into a target-device experiment contract for Software Engineering.

## Integrated model
`known intended peer → signaling reachability → offer/answer → ICE candidate gathering → candidate exchange → connectivity checks → selected candidate pair → DTLS/SCTP/DataChannel → authenticated application session → transfer/ack → network change or suspension → ICE restart/re-signaling/reconnect → durable reconciliation`

A peer-to-peer payload path is not an infrastructure-free system. Establishment and recovery can depend on signaling and STUN/TURN services even when application payloads ultimately flow directly.

## 1. Signaling is application infrastructure, not part of ICE magic
**SOURCE:** Current MDN WebRTC connectivity/signaling guidance shows offer/answer and ICE candidates being transported to the intended peer through an application signaling path. WebRTC does not prescribe one universal signaling protocol.

**SYNTHESIS:** A one-time pairing credential can identify a peer, but it does not by itself deliver fresh SDP/ICE state after network changes, process restart or ICE restart. A design claiming “pair once, then zero infrastructure forever” needs separate evidence for how fresh negotiation information reaches the peer under every required topology.

Guard: `paired identity ≠ current address ≠ current ICE candidates ≠ signaling delivered`.

## 2. ICE, STUN and TURN solve different parts of reachability
**SOURCE:** ICE gathers candidate routes and connectivity-checks candidate pairs. Candidate classes include host, server-reflexive (`srflx`), peer-reflexive and relay. STUN can expose a NAT-mapped address; TURN supplies a relay candidate when a direct path is not usable.

**SYNTHESIS:** STUN is not a relay and cannot guarantee a direct path. TURN is deliberately not direct P2P: payload traffic traverses relay infrastructure. Therefore a product requirement framed as “no server stores flight records” is materially different from “no server or relay is used at all.” A TURN relay may carry encrypted WebRTC packets without becoming application-record authority, but privacy, cost, metadata and availability still require assessment.

Guard: `STUN reachable ≠ peer reachable`; `TURN success ≠ direct P2P`; `relay transport ≠ server-side application storage`.

## 3. NAT/firewall/network policy can defeat direct candidates
**SOURCE:** WebRTC connectivity guidance explicitly treats NAT/firewall topology as a reason that host/server-reflexive candidates may fail and relay candidates may be needed.

**SYNTHESIS:** Same Wi-Fi, different Wi-Fi, carrier NAT, enterprise Wi-Fi, VPN, proxy/content filtering and client isolation are different experiments. “Both devices have Internet” does not establish that direct peer packets are permitted. “Both devices are on the same LAN” also does not establish peer-to-peer reachability when access-point isolation or managed policy blocks lateral traffic.

**OPEN:** The company EFB network topology and policy remain unknown. No generic standard can certify them.

## 4. Local-network permission/policy is a separate Apple/MDM axis
**SOURCE:** Apple documents Local Network privacy controls for iOS/iPadOS apps and current device-management settings include a LocalNetwork privacy default for managed apps. Apple also documents native App Transport Security handling of local-network resources.

**BOUNDARY:** Those native-app controls do not establish the exact permission UX or reachability semantics of a Safari/Home-Screen PWA. A browser-hosted web app and a native phone counterpart have different platform containers and may encounter different policy surfaces.

**SYNTHESIS:** Managed-device feasibility requires the exact Home Screen PWA artifact, native counterpart, OS versions and MDM/network profile. Do not infer browser permission behavior from a native Info.plist key or managed-app setting.

## 5. Candidate success must be observed, not inferred
For each connection attempt capture at least:
- signaling path and latency;
- ICE gathering/connection state transitions;
- candidate types gathered;
- selected candidate pair and whether host/srflx/relay;
- TURN use and transport where observable;
- connection establishment time;
- DataChannel open/close/error state;
- network change/suspension event;
- reconnect or ICE-restart path;
- application acknowledgement/reconciliation result.

**Track D boundary:** telemetry may measure these operational states with minimized identifiers, but analytics arrival is not proof that the underlying flight record is durably synchronized.

## 6. Network change and reconnect are first-class states
**SOURCE:** `RTCPeerConnection.restartIce()` is a broadly available mechanism that requests fresh ICE gathering/negotiation; the new offer still has to pass through the signaling mechanism.

**SYNTHESIS:** A connection established once cannot be assumed to survive Wi-Fi changes, VPN changes, suspension, IP/NAT rebinding, browser process termination or long offline periods. Recovery may require fresh signaling and new candidates. Persisting a pairing identity is useful, but persisting old network coordinates is not a substitute for renegotiation.

Guard: `paired once ≠ connected forever`; `reconnect ≠ replay correctness`.

## 7. Suspension/background remains a product blocker for invisible sync
Prior 084/086 evidence remains controlling: browser transport support does not establish indefinite background execution. Therefore even if direct WebRTC succeeds in foreground, LogMate correctness cannot require an iPad Home Screen PWA to wake invisibly whenever the phone appears.

The safe architecture remains:
`transactional local save → durable outbox → explicit/foreground/resume/reconnect opportunity → transport establishment → authenticated/idempotent apply → acknowledgement → reconciliation → independent backup`.

**B UX transfer:** if the platform cannot guarantee invisible synchronization, UI must expose truthful pending/synced/conflict/backup states and a manual/foreground recovery action rather than presenting an always-synced fiction.

## 8. Fallback architecture should be requirement-driven
Compare four modes, not one “P2P yes/no” checkbox:

### Mode A — server-mediated application sync
Server identifies peers/users and carries application operations. Highest infrastructure role; easiest cross-network reachability/observability when Internet exists.

### Mode B — server signaling + STUN, direct WebRTC payload where possible
Infrastructure establishes peers; application payload can remain direct when a viable candidate pair exists. Directness is conditional.

### Mode C — server signaling + STUN/TURN, WebRTC payload direct-or-relayed
Most robust WebRTC establishment class across difficult NAT/firewalls, but TURN can carry payload packets and incurs relay availability/cost/privacy considerations.

### Mode D — explicit export/import recovery
No automatic transport assumption; highest user friction but useful as independent recovery/escape path if permitted by managed-device file policy.

**SYNTHESIS:** A robust product may deliberately combine modes. Direct transport should be an optimization/architecture choice, not the sole recovery path for irreplaceable records.

## 9. Target-device feasibility experiment matrix
Software Engineering should execute canonical artifacts on actual managed EFB + representative native phone. Record PASS/FAIL/INCONCLUSIVE with raw evidence, not prose-only conclusions.

### Topologies
1. same permitted Wi-Fi/LAN;
2. same Wi-Fi with client isolation if available;
3. separate Internet networks;
4. iPad managed Wi-Fi + phone cellular;
5. VPN/proxy/content-filter active where company policy uses them;
6. one/both devices temporarily offline then reconnect;
7. airplane-mode transitions consistent with operational policy;
8. captive/restricted network if relevant.

### Establishment variants
- signaling reachable + STUN only;
- signaling reachable + TURN fallback;
- deliberately block direct candidate paths to prove relay behavior;
- signaling unavailable after prior pairing;
- TURN unavailable;
- stale pairing credential;
- revoked/replaced phone.

### Lifecycle variants
- both foreground;
- PWA backgrounded then foregrounded;
- PWA/browser process terminated and relaunched;
- native counterpart background/terminated as platform permits;
- Wi-Fi/network changes during active transfer;
- long-offline/skipped client versions;
- duplicate/reordered/retried operations after reconnect.

### Acceptance evidence
- intended peer authenticated;
- exact candidate/relay path known;
- no committed local record lost;
- retry is idempotent;
- remote acknowledgement distinguished from transport success;
- conflicts surfaced/reconciled;
- failure leaves durable pending state;
- independent backup/restore still works;
- user-visible state remains truthful and accessible.

## 10. Decision matrix for LogMate architecture selection
Do not choose by transport novelty. Compare:
- required offline duration;
- whether Internet is normally available at sync time;
- whether payload must avoid application servers or merely avoid server authority/storage;
- acceptable infrastructure/cost/privacy;
- managed-network reachability;
- background expectations;
- pairing/revocation burden;
- observability/support burden;
- battery/performance impact;
- correctness under failure;
- backup/recovery independence.

**MINTTAP/LOGMATE DIRECTION:** No architecture selection yet. Evidence supports designing the data layer transport-agnostically and testing server relay vs WebRTC direct/relay paths against the same durable outbox/reconciliation contract.

## 11. Five-track integration
**A owner:** ICE/STUN/TURN/signaling/candidate/restart mechanics and browser CHANGE WATCH.  
**E primary owner:** managed-network trust/policy, relay/privacy/availability, pairing/revocation, fallback and operational acceptance.  
**B consumer:** truthful pairing/connection/pending/retry/recovery UX states.  
**C consumer:** degraded-network, suspension, performance, accessibility and exact-device regression matrix.  
**D consumer:** minimized operational measurement without conflating telemetry with durable state.

Design Studio evidence remains bounded: Web Stage 3 PRACTICE, with no Safari/physical-device/human-UX PASS inferred. Software Engineering owns executable WebRTC/native/signaling/TURN/protocol experiments and artifacts.

## 12. Contradictions resolved
**CONTRADICTION:** “WebRTC is P2P, therefore no server is needed.”  
Resolution: payload may be peer-to-peer, while signaling and STUN/TURN infrastructure may still be required; TURN explicitly relays packets.

**CONTRADICTION:** “One-time pairing means later connection can be automatic without fresh discovery/signaling.”  
Resolution: persistent identity and current network coordinates are different. Network changes can require new ICE candidates and signaling.

**CONTRADICTION:** “Same LAN guarantees direct connection.”  
Resolution: network isolation, firewall/MDM policy and browser/platform constraints must be measured.

**CONTRADICTION:** “TURN fallback means cloud application sync.”  
Resolution: TURN relays transport packets; it need not become application data authority, though it is still infrastructure with privacy/cost/availability consequences.

## 13. Operational checkpoint
Generic establishment knowledge is now sufficient to hand off a bounded implementation experiment. The remaining uncertainty is empirical and product-specific, not a missing WebRTC primer.

Stop condition reached: further useful resolution of direct unattended LogMate sync now requires actual managed-iPad/native-phone/network-policy evidence or Software Engineering executable artifacts. Until then, Web Manager should not manufacture a product feasibility conclusion.

## Sources / change-watch basis
- MDN WebRTC connectivity, signaling, ICE candidate and `restartIce()` documentation, accessed 2026-09-16.
- Apple Developer documentation for Local Network Privacy / device-management LocalNetwork policy and native ATS local networking, accessed 2026-09-16. Native controls are retained only as policy-boundary evidence, not PWA equivalence evidence.

## Checkpoint result
**PASS** for generic WebRTC establishment/fallback architecture reasoning. **PRODUCT FEASIBILITY OPEN.** The next direct-sync step is Software Engineering + target managed-device execution, not another generic transport survey.