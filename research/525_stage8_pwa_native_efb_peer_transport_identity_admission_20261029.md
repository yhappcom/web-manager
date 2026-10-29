# 525 — Stage 8: PWA ↔ Native EFB peer transport, identity admission and manual-sync recovery
Date: 2026-10-29 (KST) · Owner: **Track E — Web Architecture, Security & Operations** · Cross-track: A/B/C/D · State: **SOURCE + SYNTHESIS + VALIDATION DESIGN; NO PRODUCT EXECUTION**

## 1. Scope and evidence boundary
**Question:** Can an offline, possibly managed iPad Home Screen PWA reliably and safely exchange LogMate records with a native mobile app when the cockpit has no permitted hotspot, no guaranteed common LAN or internet, and sync must be user-initiated?

This is the next distinct major domain after [524 — whole-ledger file custody](524_stage8_pwa_file_backup_egress_restore_trust_20261029.md), [523 — Worker/Storage/MDM security](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) and [522 — delta/clock admission](522_stage8_offline_utc_lww_clock_trust_and_recovery_admission_20261027.md). Do not duplicate their protocol, storage or backup primers. No connection, transfer, file, managed EFB or product test was run in this cycle.

**Product authority (read-only, checked 2026-10-29):**
- [LogMate MASTER.md](https://github.com/yhappcom/logmate/blob/main/MASTER.md) and [approved Local-First Manual Delta Sync contract](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md), blob `2240fc1b`: Firebase UID is owner authority; local-first commits; Manual Sync only; server receipt, local apply and cursor required for success. Initial online app launch permits a single **read-only metadata check**, not automatic Push/Pull/Apply. QR/WebRTC P2P is **future optional**, not implemented or approved for release. New-device whole-ledger `.lbk` is first-transfer strategy, not silent merge.
- Product P2P semantics (§11): preserve original Operation ID and `modifiedAtUtc`; a recipient B can later upload the original A operation on a user-triggered Firebase Manual Sync, with deduplication. P2P success is not Firebase convergence, cloud backup, or successful server receipt.
- [W-031](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w031-simulator-preacceptance-2026-10-27.md) Safari Simulator **tab** local IDB/offline-shell evidence is not WebRTC/installed Home Screen/MDM evidence. [W-012](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w012-empty-destination-backup-2026-10-27.md) Native B1 restore is not a P2P transport test. [524](524_stage8_pwa_file_backup_egress_restore_trust_20261029.md) already distinguishes `.lbk` custody from in-app P2P.
- EFB policy from owner: cockpit hotspot not permitted; company iPad cannot be assumed to install arbitrary App Store apps. **Unknown:** exact airline policy, MDM Web Clip classification, radio restrictions, Wi-Fi network, peer reachability, Bluetooth permissions, physical iPad model, data export policy. Do not infer these from general Apple documentation.

## 2. History/problem → principle → standard [SOURCE]
Historically, browsers expose network-safe origins, not general-purpose Wi-Fi Direct, raw UDP multicast, arbitrary Bluetooth serial sockets or OS AirDrop automation. WebRTC emerged to negotiate encrypted peer media/data over network paths, while a web page still needs an **out-of-band signaling mechanism** to exchange offer/answer and ICE candidates. The browser does not guarantee that peers share a usable network or that candidate gathering succeeds. [W3C WebRTC Recommendation](https://www.w3.org/TR/webrtc/), [RFC 8827 security architecture](https://www.rfc-editor.org/rfc/rfc8827.html), [MDN signaling/candidate API](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/addIceCandidate).

**Trust decomposition:** (1) capability to run JavaScript, (2) ability to exchange signaling, (3) reachable ICE candidate pair, (4) encrypted DTLS/SCTP data channel, (5) verified peer **application identity / same Firebase UID**, (6) valid Operation/wire admission and durable local commit, (7) optional later authenticated Firebase Manual Sync. A positive result at step N does not establish any later step.

`RTCDataChannel` is a bi-directional channel over SCTP/DTLS and supports reliable or partial-reliability modes. DTLS protects traffic against passive interception, **not** automatically against pairing with the wrong human/device, compromised signaling, foreign UID, forged Operation payload, malicious sender or loss of durable persistence. Authentication/fingerprint binding is an application-level and signaling trust problem. [W3C RTCDataChannel](https://www.w3.org/TR/webrtc/#rtcdatachannel), [RFC 8827](https://www.rfc-editor.org/rfc/rfc8827.html).

## 3. Current browser / OS reality, separated [SOURCE / CHANGE WATCH]
| Layer | Grounded capability | Non-inference for EFB |
| --- | --- | --- |
| **Web standard** | `RTCPeerConnection` + `RTCDataChannel`, ICE candidate exchange, DTLS/SCTP; negotiated `maxMessageSize` and `bufferedAmount` flow control | No mandated peer discovery, no serverless success, no background transfer guarantee |
| **WebKit/Safari** | WebKit documented `RTCPeerConnection`/`RTCDataChannel` support; historical ICE privacy filtering. 2018–19 WebKit work added mDNS host candidates; 2025 WebKit test regression was fixed. | **2017 statement “only srflx/TURN without camera permission” is historical, not a 2026 blanket rule**. Exact iPadOS26.x installed/managed, camera-free, offline mDNS/host ICE and Safari↔native pairing remain untested |
| **Apple OS** | [TN3179](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy) says Safari/WKWebView-originating traffic is exempt from the *native-app* local-network privacy requirement; native app traffic and Bonjour can be subject to OS checks. | An exemption from one prompt **does not** mean reachable LAN, permitted mDNS, unrestricted EFB radios, MDM approval, or automatic peer discovery |
| **Chromium** | [Chrome 142 release](https://developer.chrome.com/release-notes/142) introduced Local Network Access permission for public→private/loopback requests; [Chrome LNA guidance](https://developer.chrome.com/blog/local-network-access) distinguishes initial fetch/subresource gating and staged WebRTC integration. | Do not transfer Chrome LNA prompt behavior to Safari; current WebRTC coverage is version-sensitive and needs actual browser verification |
| **Web Bluetooth** | [MDN Web Bluetooth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API) marks limited availability, BLE peripheral/GATT-oriented, secure-context, user-permission, and not available to Service Workers. | Cannot assume Safari iPad Web Bluetooth or Bluetooth Classic device-to-device sync; not a replacement for arbitrary native Bluetooth transport |
| **Home Screen PWA** | [WebKit Safari 26](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) says Home Screen “Open as Web App” is user-selectable and installation is not evidence of background service. | Foreground connection continuity, termination/relaunch, independent storage, and MDM Web Clip differ and need tests |
| **Native mobile** | Native app may use platform networking APIs subject to OS entitlements, permissions and managed restrictions. | Web page does **not** inherit native app networking APIs; a phone's cellular connection does not automatically create an allowed LAN to the EFB |

**Important current change watch:** [W3C webrtc-pc issue #3109, opened 2026-05-18](https://github.com/w3c/webrtc-pc/issues/3109) reports macOS26 mDNS ICE gathering prompting for Local Network access. This is an active standards issue **about macOS**, not direct evidence that iPadOS26 EFB behaves identically. [WebKit bug 312332](https://bugs.webkit.org/show_bug.cgi?id=312332) documents a Safari26.3–26.4 TURN-relay regression with FIXED tracker status; do not treat a historical or macOS report as an observed iPad failure. Record exact OS/browser build for every transport result.

## 4. Connectivity feasibility is topology-specific [SYNTHESIS]
| Scenario | Signaling | Candidate path | Outcome classification |
| --- | --- | --- | --- |
| Both devices offline, **no shared network/radio link** | QR may exchange offer/answer, but no usable data path | None established | **NO_TRANSPORT**, not a product sync bug; never promise unattended P2P |
| Shared admin-approved LAN, no internet | QR/manual out-of-band may exchange SDP/ICE | Local host/mDNS ICE *might* connect if allowed | **POSSIBLE, NOT VERIFIED** on physical Safari PWA↔native/MDM |
| Both have internet, separate networks | Server-mediated signaling possible; STUN/TURN may be needed | NAT traversal/relay availability/cost | **POSSIBLE, NOT GUARANTEED**; not the offline EFB premise |
| Native phone has cellular, EFB offline without permitted link | Phone can reach cloud, EFB cannot | No implicit shared link | **NOT A BRIDGE**; phone sync does not transfer EFB local changes |
| AirDrop / Files user-mediated | OS share sheet, not WebRTC signaling | Managed OS transfer destination | **FILE CUSTODY PATH**, not in-app P2P or delta sync; see 524 |
| QR alone | Can carry short pairing information or limited manual signaling | No network transport created | **PAIRING ONLY**; not 37-store backup nor full delta transport |
| Native mobile↔PWA via hotspot | May provide network if enabled | Requires OS/network policy | **NOT ADMISSIBLE** in user's cockpit restriction; test only where expressly permitted outside cockpit |
| Bluetooth | Web Bluetooth browser support and native role compatibility unknown | BLE/GATT restrictions | **NO ASSUMED SAFARI PATH**; don't silently substitute |

QR signaling offline may require multiple candidate/answer exchanges and camera/scanner permissions. A single QR is not proof of complete ICE negotiation. Manual signaling must have size limits, expiry, integrity/peer verification and explicit user approval; never embed Firebase tokens, raw full-ledger payloads or persistent secrets in a QR.

## 5. Identity and replay admission [SYNTHESIS / DEPENDENCY on 522]
**DTLS is channel security, not Owner authority.** Before accepting any incoming Operation into a UID-owned ledger, require the Engineering-owned contract for same verified UID, peer consent, bounded session and authenticated pairing proof. An offline PWA that previously unlocked a verified UID may have locally retained owner authority, but an unverified new device cannot invent a UID assertion or use a matching email/QR label as Firebase authentication.

Separate four proofs: **peer intent** (user approves transfer), **transport peer** (fingerprint/SDP binding), **owner** (trusted Firebase UID binding under product rules), **operation** (original ID/digest/owner/schema/record references, replay/duplicate checks). A short displayed pairing code without an authenticated binding to the full session transcript can be spoofed. Do not claim a particular PAKE, QR code format, session token, or trust anchor is already approved.

Transport delivery and `send()` completion are not durable apply. Receiver must stage/validate, atomically commit the original Operation ID and local state, and acknowledge only after verified persistence. On timeout or lost ACK, sender retains the same Operation; receiver must deduplicate idempotently. Preserve history, tombstones, original timestamps, outbox and losing revisions. Do not assign a new local Operation ID to a received remote operation. For a third device, convergence occurs only after **user-initiated authenticated server admission + subsequent pull/apply**; P2P alone cannot attest that state.

**Attack/failure examples:** malicious QR redirects to attacker, mismatched UID with valid DTLS, offer/answer replay, stale/duplicate ICE candidates, candidate path switches, sender abort after partial chunks, replay with same ID/different payload, unknown wire/schema version, oversized decompression, source clock skew, duplicate CREATE identity, recipient process kill after receipt but before commit, old PWA Service Worker active during schema migration, and managed iPad storage eviction. Each is a distinct negative oracle; reuse 522/523/524 semantics instead of new product policy.

## 6. Data-channel operational quality and interruptions [SOURCE / SYNTHESIS]
[MDN `RTCSctpTransport.maxMessageSize`](https://developer.mozilla.org/en-US/docs/Web/API/RTCSctpTransport/maxMessageSize) and [MDN `RTCDataChannel.send`](https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel/send) warn about message-size limits; [`bufferedAmount`](https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel/bufferedAmount) and `bufferedamountlow` support backpressure. For large transfers, use bounded chunks with explicit length, version, transfer ID, ordering, per-chunk integrity where designed, final digest and durable receiver ACK. These are **requirements for a future design**, not an approved wire format or tested performance.

A connected channel may drop when the PWA is backgrounded, screen locks, device changes network, MDM revokes permission, battery policy suspends work, or the browser terminates the page. Neither Service Worker installation nor push notification support proves a live WebRTC channel can continue unattended. Preserve local work and a resumable/retryable **manual** flow; don't show “Synced” after `channel.send()`, a transport ACK, or a QR scan.

## 7. Five-track dependency allocation and expert judgment
| Track | Current stage/evidence maturity | Role in this bundle |
| --- | --- | --- |
| **E — Security/Operations** | Stage8 largest bottleneck: source + threat model, physical trust and Owner binding absent | **Owns** channel/Owner distinction, transport failure, MDM policy, replay/commit and release HOLD; majority effort |
| **A — Platform/Browser** | Standards strong; 2026 Safari ICE/mDNS/installed behavior unverified | Owns ICE, signaling, browser permission/version distinctions and CHANGE WATCH; feeds E |
| **B — UX/IA** | Design Studio W121 Stage3 runtime gate OPEN | Consume E's honest task states: no shared network, pairing required, peer unverified, transfer pending, applied locally, cloud sync pending; no generic visual-system duplication |
| **C — Performance/A11y/Quality** | Synthetic and Safari-tab evidence, no dual-device managed transfer | Owns exact dual-device packet-loss/backpressure, VoiceOver/focus on QR/permissions, interruption and independent DB oracle |
| **D — Discovery/Analytics** | Marketing D8 claims HOLD/D9 deferred | Do not claim seamless offline pairing, automatic synchronization, no-hotspot transfer or “all iPads”; only privacy-minimized capability/failed-path aggregates if product consent exists |

[Design Studio W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) is Stage3 practice/not passed; [Marketing D8/D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) has launch-claim HOLD. [Software Engineering Validation Standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) remains external Engineering authority; Engineering owns actual P2P, Flutter/native, UID/wire implementation and tests. This study makes **no** implementation authorization and no peer repository changes.

## 8. Independent acceptance / diagnostic exercises [VALIDATION DEFINED — NOT RUN]
Use synthetic accounts and disposable 37-store ledgers on two physical devices with exact Git/compiled NORMAL Web SHA, iPad model/iPadOS, Safari tab vs Home Screen vs managed Web Clip, native OS/build, approved network and MDM policy. Capture redacted ICE candidate **types and connectivity state**, not IP addresses, SDP fingerprints, QR payloads, auth tokens or personal flight records.

| ID | Test and independent oracle |
| --- | --- |
| PT01 | Feature-detect `RTCPeerConnection`/`RTCDataChannel` in Safari tab, Home Screen and managed Web Clip; compare real native peer. API presence ≠ connection. |
| PT02 | No network/no hotspot: attempt QR-only signaling; classify **NO_TRANSPORT**, verify no data loss or false success. |
| PT03 | Admin-approved same-LAN/no internet: offline offer/answer/ICE exchange; inspect host/mDNS candidate types and connected state without private IP logging. |
| PT04 | Safari↔native no camera/mic permission; do not grant unrelated capture permissions merely to make P2P pass. |
| PT05 | Disable mDNS, client isolation or UDP in a controlled test network; distinguish ICE failure from auth/record admission failure. |
| PT06 | Test separate-network STUN/TURN case outside EFB; record relay availability, time/cost and privacy; do not infer offline feasibility. |
| PT07 | MDM denies local networking, sharing or Web Clip capability: observe actual policy on exact managed context, fail closed with usable offline ledger. |
| PT08 | QR/SDP mismatch, expired/replayed offer, attacker-controlled fingerprint or wrong peer: reject before any ledger write. |
| PT09 | Same email/label but **foreign Firebase UID**; reject and preserve both original ledgers. |
| PT10 | Matching UID but wrong Replica/duplicate session or missing owner proof: do not silently rebind or merge. |
| PT11 | 1, 100 and large synthetic Operation batches with negotiated max message size/backpressure; independent byte/semantic readback. |
| PT12 | Inject partial chunk, duplicate/reorder, truncated transfer, unknown version and decompression cap; no partial durable apply. |
| PT13 | Kill sender, receiver, browser and native app at distinct stages; restart, retry same IDs, verify idempotency and local outbox. |
| PT14 | Same Operation ID+same digest retry versus same ID+different payload; original timestamp/ID preserved; mismatch rejected. |
| PT15 | Offline A→B transfer, then B authenticated user-initiated Manual Sync; verify server receipt, A duplicate, C pull/apply and independent convergence. |
| PT16 | A/B/C clock skew, tombstone/restore, concurrent CREATE alias, Custom Definition and 37-store dependency; reuse 522 independent oracle. |
| PT17 | PWA Worker upgrade/schema migration, Safari suspension/lock, low storage and storage eviction during pending transfer; source ledger survives. |
| PT18 | VoiceOver, keyboard/QR alternative, denied permission, interruption and recovery copy; no color-only success and no auto-sync promise. |
| PT19 | Verify `.lbk` OS Files export/restore separately under BF01–BF18; **never** count P2P transport as independent backup. |
| PT20 | Production gate: authorized airline policy + exact build/device/MDM + owner/wire admission + negative controls + rollback + user claims; no extrapolation from synthetic Chrome. |

**Diagnostic exercise:** Given “PWA installed + QR scanned + WebRTC encrypted + phone online,” identify the missing proofs: EFB-to-phone network, ICE path, authenticated same UID, operation admission, local atomic commit, independent backup, user-triggered server receipt and third-device apply. Correct answer: **none is implied by those four observations**.

## 9. Decisions, contradictions, next meaningful boundary
- **MINTTAP DIRECTION (not a new product policy):** keep approved `.lbk` first transfer and user-initiated Manual Sync. Treat direct PWA↔native P2P as a **conditional optional research branch**, not a prerequisite for offline logbook use and not a launch promise. The no-hotspot cockpit restriction is an actual product constraint, not a prompt to design a bypass.
- **CONTRADICTION:** “WebRTC supported in Safari” ≠ “two offline devices can communicate”; “DTLS encrypted” ≠ “same authenticated Owner”; “QR pairing” ≠ “transport”; “cellular phone online” ≠ “offline iPad connected”; “local-network privacy prompt exempt” ≠ “airline MDM allows networking”; “transport ACK” ≠ “durable apply”; “P2P received” ≠ “Firebase Manual Sync succeeded”; “same origin” ≠ “same PWA/native storage”.
- **OPEN:** exact Safari26.x mDNS/host candidate behavior on managed iPad; real same-LAN availability and cockpit radio policy; native endpoint permissions; signaling/identity contract; wire limits; EFB file egress; all PT01–PT20; production security/quality acceptance.
- **CHANGE WATCH:** Apple/WebKit ICE candidate privacy and iPadOS26.x, Chrome LNA staging and enterprise policy, Web Bluetooth availability, WebRTC relay regressions, MDM policy, Safari installed/background lifecycle. Recheck before implementation.
- **Next gate:** Engineering-approved dual-device **physical managed EFB + native** network and identity test, or documented airline policy that rules it out. If no permitted network path exists, the correct outcome is **P2P NOT FEASIBLE IN THAT ENVIRONMENT**, with offline-first local operation and later manual sync/approved file custody retained—not a simulated PASS.

**Stage 8 ACTIVE · PT01–PT20 NOT RUN · Production validation OPEN · PWA release HOLD.** This is a substantive standards/product-source integration and validation design, not proof of working transport. Adjacent-value check: covered signaling, ICE/mDNS, Chrome/Apple permission divergence, Web Bluetooth, QR, no-hotspot topology, DTLS vs Owner, replay/atomic apply, chunking/backpressure, suspension, third-device convergence, MDM, accessibility and claims. The remaining decisive question requires materially different **physical device/network/policy** evidence; do not manufacture another synthetic browser PASS.