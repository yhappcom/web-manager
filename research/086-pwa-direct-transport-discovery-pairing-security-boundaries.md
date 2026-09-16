# 086 — PWA Direct Transport, Discovery, Pairing & Security Boundaries

Status: **PASS — continuous expert maintenance checkpoint**  
Date: 2026-09-16

## Purpose
Resolve a high-value LogMate/EFB architecture ambiguity without selecting an implementation prematurely: what current web transport APIs actually provide, what they do not provide, and which missing capabilities must be proven on a managed iPad before unattended PWA↔native synchronization can be considered feasible.

## Integrated model
`peer discovery → addressing/signaling → network reachability/policy → authenticated pairing → secure transport establishment → application protocol → durable send/outbox → acknowledgement → reconciliation → suspension/reconnect → recovery`

The transport is only one layer. A browser API that can move bytes does not solve discovery, pairing, background execution, authorization, conflict handling or backup.

## 1. WebSocket is client↔server transport, not nearby-device discovery
**SOURCE:** The standard WebSocket browser API opens a bidirectional communication session between browser and server. It is mature and broadly supported. The classic API lacks backpressure.

**SYNTHESIS:** WebSocket can support a cloud/relay architecture or a deliberately reachable local server endpoint. Its existence does not let a PWA discover an unknown nearby phone, learn its address, bypass local-network/MDM policy, or remain alive while iPadOS suspends the web app.

Guard: `WebSocket available ≠ peer discovery ≠ local-network permission ≠ unattended background sync`.

## 2. WebTransport is also server-oriented
**SOURCE:** WebTransport is a secure-context API using HTTP/3 to connect a user agent to a server and provides reliable streams plus unreliable datagrams. MDN marks it Baseline 2026 / newly available since March 2026, with support caveats. WebKit's Interop 2026 program includes WebTransport to improve cross-browser interoperability.

**CHANGE WATCH:** Being newly Baseline does not establish behavior on the company's actual managed iPad OS/WebKit version. WebTransport is still an HTTP/3 server transport, not a browser API for arbitrary nearby peer discovery.

**SYNTHESIS:** WebTransport may improve a server-mediated synchronization path, but it does not remove the need for endpoint identity, authentication, server reachability, durable application semantics or offline retry.

Guard: `WebTransport available ≠ direct device-to-device transport`.

## 3. WebRTC DataChannel can carry peer-to-peer arbitrary data, but connection establishment remains a system
**SOURCE:** RTCDataChannel is a widely available bidirectional peer-to-peer data channel. WebRTC data-channel payloads are encrypted using DTLS. WebKit continues active WebRTC interoperability work in 2026; Safari 26.4 included RTCDataChannel/spec fixes and Interop 2026 retains WebRTC as a focus area.

**SOURCE:** WebRTC data-channel establishment still requires peers to negotiate connection information. Application-controlled negotiation/signaling remains necessary; WebRTC does not define a universal application signaling service or nearby-device discovery UX.

**SYNTHESIS:** WebRTC is the strongest generic browser candidate for direct peer data movement, but `RTCDataChannel supported` proves only the transport primitive. It does not prove that an EFB PWA can automatically find a native phone, exchange signaling without infrastructure/user action, traverse the actual network, continue while suspended, or persist a trusted pairing across policy/device changes.

Guard: `WebRTC P2P capability ≠ zero-infrastructure discovery ≠ unattended pairing ≠ background execution`.

## 4. Discovery is separate from transport
A usable direct-sync design must answer separately:
- How does the EFB learn that the correct phone exists?
- How are endpoint identifiers/addresses exchanged?
- What signaling path exists before WebRTC can connect?
- Does discovery require multicast/local-network mechanisms unavailable to normal web content?
- Does the managed iPad/MDM permit the relevant network path?
- What happens when both devices are on cellular networks, different Wi-Fi networks, airplane mode or captive/isolated networks?

**OPEN:** No authoritative evidence in this checkpoint establishes a general Safari/Home-Screen API that gives an arbitrary PWA automatic nearby native-device discovery suitable for the requested one-time-pairing/unattended-sync model.

Therefore discovery remains an explicit product experiment rather than an inferred web capability.

## 5. Pairing and authentication are separate from encryption-in-transit
DTLS/TLS protects an established channel. It does not establish that the peer is the user's intended phone.

Pairing contract requires:
`device/user identity → initial trust ceremony → cryptographic binding/credential → persisted pairing state → reconnect authentication → rotation/revocation → lost/replaced-device recovery`.

Threats include wrong-peer pairing, stale pairing after device transfer, replay, local attacker impersonation, compromised signaling, credential leakage, and revocation while one device remains offline.

**DEPENDENCY:** Concrete key/credential design belongs to Software Engineering/security implementation validation. Web Manager owns the trust and recovery requirements.

## 6. Foreground connectivity is not background availability
Safari/WebKit supporting WebRTC, WebSocket or WebTransport does not establish that a Home Screen PWA remains runnable indefinitely when backgrounded/suspended. Prior 084 evidence already rejects Background Sync as an EFB correctness dependency.

Therefore the correctness architecture remains:
`transactional local save → durable outbox → opportunistic foreground/reconnect/manual/next-launch transport → authenticated/idempotent apply → acknowledgement → reconciliation`.

A direct channel, if later validated, is an optimization/transport option inside this architecture, not the durability foundation.

## 7. Managed-iPad policy is an independent feasibility axis
Generic Safari support does not establish company-EFB feasibility. Target validation must capture:
- exact iPadOS/Safari/WebKit version;
- Home Screen/managed-web-app policy;
- local-network restrictions and network isolation;
- Wi-Fi/cellular/airplane-mode operational states;
- MDM/VPN/proxy/content-filter effects;
- foreground/background/suspension behavior;
- whether signaling/discovery endpoints are reachable;
- persistence of pairing credentials across update/restart/profile changes.

No product architecture is approved until these are measured on the actual device class/policy.

## 8. Candidate architecture classes
### A. Cloud/server relay
Pros: stable addressing/discovery through account/server identity; works across separate networks when Internet exists; operationally observable.  
Costs: infrastructure/auth/privacy/availability; unavailable when neither device has Internet unless local work queues.

### B. Direct WebRTC data channel
Pros: peer-to-peer data path after establishment; encrypted transport; potentially avoids relaying record payloads through application server.  
Costs/open: signaling, discovery, ICE/network policy, pairing identity, suspension/reconnect, managed-iPad validation.

### C. User-mediated export/import
Pros: explicit recovery/fallback path; can be independent of background execution.  
Costs: user friction, file destination/MDM constraints, duplicate/reconciliation requirements.

**SYNTHESIS:** These classes are not mutually exclusive. A robust product may use server-mediated sync for normal operation plus export/import for independent recovery; direct peer transport should be added only if it solves a validated requirement better than its added complexity.

## 9. Transport feasibility matrix
For every candidate record separately:
- transport primitive supported on exact target versions;
- endpoint/discovery mechanism;
- signaling requirement;
- Internet required?;
- same-LAN required?;
- secure-context/certificate requirements;
- peer authentication/pairing;
- foreground/background constraints;
- reconnect behavior;
- MDM/network-policy dependency;
- observability/debuggability;
- failure semantics;
- effect on durability/reconciliation;
- target-device evidence.

Do not collapse these into a single “supported” checkbox.

## 10. Cross-track transfer
**Track A owner:** WebSocket/WebTransport/WebRTC mechanics and platform/change-watch evidence.  
**Track E primary consumer/owner:** trust boundary, pairing, network-policy, operational lifecycle and failure semantics.  
**Track B:** communicates explicit sync states and user-controlled retry/pairing/recovery without promising background magic.  
**Track C:** target-browser/device, suspension, degraded-network and accessibility validation.  
**Track D:** measurement may observe attempts/ack/reconciliation with minimized metadata but cannot prove durability from analytics arrival.

**Design Studio dependency:** current Web Design Stage 3 remains PRACTICE; no Safari/physical-device/human-UX PASS is inferred.

**Software Engineering dependency:** signaling implementation, ICE/TURN/STUN choices, native peer behavior, credential/key design, protocol, idempotency, reconnect and actual target-device experiments remain implementation authority.

## 11. EFB acceptance experiment contract
Before claiming unattended direct sync feasible, test the canonical PWA/native artifacts on target managed hardware for:
1. one-time pairing ceremony and persisted peer identity;
2. foreground direct connection under permitted network topology;
3. termination/background/suspension and later recovery;
4. both devices changed since last contact;
5. duplicate/reordered/retried operation handling;
6. one device offline for long periods / skipped versions;
7. credential revocation/lost phone;
8. MDM/network changes;
9. no-data-loss behavior when direct transport never becomes available;
10. independent backup/restore remains functional.

Failure of direct transport must not lose locally committed flight records.

## 12. Operational judgment
The architecture question is not “Does Safari support WebRTC?” It is:
`Can the exact managed EFB + native-phone system discover and authenticate the intended peer, establish a permitted channel, survive suspension/reconnect, and preserve correctness when the channel is absent?`

Current answer for LogMate: **OPEN**. Generic standards establish useful primitives but not the requested unattended product behavior.

## Sources / change-watch basis
- MDN WebSocket API, accessed 2026-09-16.
- MDN WebTransport API, Baseline 2026, accessed 2026-09-16.
- MDN RTCDataChannel / Using WebRTC data channels, accessed 2026-09-16.
- WebKit, Announcing Interop 2026, accessed 2026-09-16.
- WebKit, Safari 26.4 release notes, accessed 2026-09-16.
- WebKit, Safari 26.6 release notes, accessed 2026-09-16.

## Checkpoint result
**PASS** as generic transport/discovery/security boundary knowledge. **NO PRODUCT FEASIBILITY PASS.** Direct unattended PWA↔native synchronization remains OPEN pending Software Engineering + managed-iPad/native-phone validation.