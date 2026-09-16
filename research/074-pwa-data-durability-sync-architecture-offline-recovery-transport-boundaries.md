# 074 — PWA Data Durability & Synchronization Architecture Boundaries

State: **PASS — FOUNDATION/PRACTITIONER CROSS-TRACK SPECIALIZATION CHECKPOINT**  
Date: 2026-09-16  
Primary owners: **Track A Web Platform & Browser + Track E Architecture/Security/Operations**  
Consumers: B UX/IA, C Quality, D Analytics/Discovery  
Production status: **OPEN — no LogMate/MintTap synchronization implementation is inferred**

## Why this block
073 established service-worker/offline/install/storage foundations but deliberately left the hardest EFB question open: preserving irreplaceable local records and eventually reconciling them with another replica. This block separates browser persistence, backup, synchronization protocol and transport so that “offline” or “PWA” is never mistaken for durable multi-device sync.

## Core model

`local durable transaction → immutable operation/change identity → outbox pending state → transport opportunity → authenticated delivery → remote idempotent apply → acknowledgement → local sync-state advance → conflict/reconciliation if concurrent → backup/export independent of sync`

Critical separation:

`local save ≠ queued for sync ≠ transmitted ≠ remotely accepted ≠ replicated elsewhere ≠ backed up`

---

## 1. IndexedDB is transactional structured origin storage, not a synchronization system

**SOURCE:** IndexedDB operations occur in transactions. Database schema/version changes occur through a `versionchange` transaction during `upgradeneeded`; another open connection can block the upgrade and triggers `blocked`. Sources: MDN `IDBDatabase`, `IDBOpenDBRequest/upgradeneeded`, `IDBOpenDBRequest/blocked` (checked 2026-09-16).

**SYNTHESIS:** A data-bearing PWA needs explicit database-version and multi-client upgrade behavior. A service-worker update and a database-schema update are separate state machines and may overlap.

Recommended invariant: user mutation plus creation/update of its outbox/change record should be committed atomically in one local transaction where the schema permits. Otherwise a crash between “save record” and “enqueue sync” can create locally valid but permanently unsynchronized data.

**CONTRADICTION:** `IndexedDB transaction = cross-device transaction` is false. Atomicity ends at the local database boundary.

### Schema migration contract
- schema version is explicit;
- migrations are deterministic and resumable/recoverable where possible;
- old tabs/workers receive version-change handling and do not indefinitely block upgrades;
- destructive migrations require verified backup/recovery strategy;
- service-worker/page/schema compatibility windows are defined before forced activation;
- migration success is verified before declaring the new app version ready.

**DEPENDENCY — Software Engineering:** exact migration framework, data model and rollback code are implementation architecture, not inferred here.

---

## 2. Multi-tab/worker coordination is a local concurrency problem

**SOURCE:** Web Locks lets same-origin tabs/workers coordinate access to named resources; MDN explicitly gives “only one tab syncs between network and IndexedDB” as a leader-election example. It is secure-context functionality and does not coordinate other devices. Source: MDN Web Locks API, checked 2026-09-16.

**SYNTHESIS:** A PWA may need local leadership/locking to avoid two same-origin contexts replaying the same outbox concurrently. This is optional architecture, not a substitute for server-side idempotency.

**CONTRADICTION:** a local Web Lock does not prevent duplicate delivery from another device, an old retry, restored backup or restarted process.

---

## 3. Synchronization requires protocol semantics above the transport

A robust offline-capable sync design needs, at minimum:
- stable record IDs that do not depend on network availability;
- stable operation/change IDs for replay detection;
- per-change creation metadata/version or equivalent ordering context;
- an outbox whose entries survive reload/update/offline periods;
- retry policy that assumes duplicate delivery can happen;
- idempotent remote application or deduplication by operation ID;
- acknowledgement that identifies what remote state accepted;
- pull/reconciliation cursor or equivalent remote-change discovery;
- explicit deletion/tombstone semantics if deletes synchronize;
- conflict policy for concurrent edits;
- bounded error/recovery state visible to the user.

**SYNTHESIS:** Transport reliability does not remove application-level retry/idempotency requirements. A connection can fail after the remote side commits but before the sender receives acknowledgement; retry then creates an ambiguous duplicate unless the protocol can recognize the operation.

### State language for Track B
`local-only → queued → sending → acknowledged/synced` plus `retrying`, `conflict`, `blocked/auth-required`, and `failed/recovery-required`.

Never label `local-only` as “synced.”

---

## 4. Conflict is a product/data-semantics decision, not a generic last-write-wins checkbox

Concurrent replicas can both validly edit while disconnected. Candidate policies include field/domain-specific merge, user review, append-only event reconciliation, server-authoritative resolution, or carefully justified last-write-wins. No universal policy is selected here.

For logbook-like records, silently overwriting one replica is high risk because records may be historical and user-authored. Conflict evidence should retain both competing values and provenance until resolution policy is proven.

**OPEN:** actual LogMate normalized record identity, editable fields, deletion semantics and authoritative replica are not established in this repository.

---

## 5. Backup is deliberately independent from synchronization

073 established that browser-origin storage can be best-effort and can be cleared/evicted. WebKit documents persistent-mode requests and origin eviction behavior; Safari 17+ supports StorageManager estimate/persist APIs, but user clearing and application defects remain outside a simple persistence guarantee. Source: WebKit “Updates to Storage Policy”, checked 2026-09-16.

Therefore:

`sync replica ≠ backup` and `persistent browser storage ≠ backup`.

A durability design for irreplaceable records should define:
- exportable versioned backup format;
- integrity/version metadata;
- explicit backup completion evidence;
- restore into an empty/new installation;
- restore into an installation with existing data, including duplicate/conflict policy;
- schema migration of old backups;
- failure/corruption handling;
- periodic recovery drill on representative devices.

**MINTTAP/LOGMATE-LIKE DIRECTION:** do not call an EFB PWA “safe for logbook storage” until restore from an independently held backup has been demonstrated on target devices.

**OPEN:** target iPad file/export policy and permitted destination are not verified.

---

## 6. Background sync cannot be a correctness dependency

**SOURCE / CHANGE WATCH:** Background Synchronization is currently marked Limited Availability by MDN; Periodic Background Sync is Limited Availability and experimental. They are distinct optional APIs, not baseline PWA capabilities. Sources: MDN Background Synchronization API and Web Periodic Background Synchronization API, checked 2026-09-16.

**SOURCE — Apple boundary:** Apple documents Web Push for iOS/iPadOS Home Screen web apps, but Safari does not support invisible push notifications. This establishes event-specific background capability, not arbitrary continuous execution. Source: Apple “Sending web push notifications in web apps and browsers”, checked 2026-09-16.

**SYNTHESIS:** Correctness must not depend on “the PWA will eventually wake itself and sync.” The foreground/open/resume path must inspect durable pending work and retry it. Background APIs, where supported and policy-appropriate, can reduce delay but are accelerators rather than the sole recovery mechanism.

Recommended trigger family:
- after local mutation when online;
- application launch/resume/foreground;
- explicit user “sync now”;
- connectivity recovery while active;
- optional supported background event;
- periodic reconciliation while active.

---

## 7. Transport matrix: server relay and peer transport solve different problems

### HTTPS request/response
Broadest ordinary web primitive. Suitable for durable server/cloud relay when reachable. Can carry idempotent push/pull synchronization without requiring a persistent connection.

### WebSocket
**SOURCE:** WebSocket is widely available and connects the browser to a WebSocket server. Source: MDN WebSocket, checked 2026-09-16.

Useful for live server-mediated updates while open, but it is not peer discovery, background execution or offline durability. The classic API also lacks automatic backpressure.

### WebTransport
**SOURCE / CHANGE WATCH:** MDN marks WebTransport as newly Baseline 2026 for latest browsers, but older browser/device support may differ. It connects a user agent to an HTTP/3 server and supports streams/datagrams. Source: MDN WebTransport API, checked 2026-09-16.

It remains server-oriented transport, not automatic nearby-device discovery, and is unnecessary unless its semantics materially solve a requirement.

### WebRTC RTCDataChannel
**SOURCE:** RTCDataChannel can securely exchange arbitrary peer data; establishing the peer connection requires negotiation/signaling logic. Source: MDN “Using WebRTC data channels”, checked 2026-09-16.

**SYNTHESIS:** WebRTC proves that browser peer data transport exists; it does **not** prove zero-intervention nearby-device discovery, no signaling dependency, reliable operation under managed iPad/network policy, or background synchronization while suspended.

### Web Bluetooth
**SOURCE / CHANGE WATCH:** MDN marks Web Bluetooth Limited Availability/experimental and exposes BLE peripheral access through permission-oriented APIs. Source: MDN Web Bluetooth API, checked 2026-09-16.

**CONTRADICTION:** It cannot be assumed as an iPad-Safari ↔ native-phone synchronization foundation. Target Safari support, permission UX, role topology and managed-device policy require direct evidence.

### Local-network/direct HTTP
A native phone could in principle expose a network service, but a web client still needs reachability, addressing/discovery, browser mixed-content/secure-context constraints, OS local-network/privacy policy and company network policy. None is established for the EFB scenario.

**OPEN/VALIDATION:** Bonjour/mDNS discovery, local-network permissions, TLS certificate/trust, hotspot restrictions and browser access on the actual managed EFB require a separate target-device engineering experiment. Do not infer them from generic LAN networking.

---

## 8. EFB scenario: architecture options after evidence separation

### Option A — server/cloud relay when connectivity exists
PWA and native app each keep a local replica/outbox and synchronize to a reachable service when online.

Strengths: avoids direct peer discovery; server can provide acknowledgement/deduplication/change history.  
Costs: requires backend/account/device identity/security/operations and connectivity eventually. This conflicts with any hard “no server/account ever” product constraint and therefore is not selected without product decision.

### Option B — direct peer synchronization
Could use a viable peer/local transport if target iPad PWA and native phone both support it under policy.

Strength: may operate without Internet/server.  
Risks: discovery, pairing, authentication, connectivity, browser suspension, managed-device restrictions, transport compatibility and recovery all become product responsibilities.

### Option C — user-mediated file/export transfer
A versioned export/import can provide backup and a fallback synchronization/recovery path.

Strength: conceptually robust fallback and useful even if automatic transport fails.  
Cost: not automatic; conflict/duplicate handling still required.

**SYNTHESIS:** Automatic peer sync and backup should not be one mechanism. Even if direct sync becomes feasible, an independent export/restore path remains valuable for disaster recovery.

---

## 9. Long-offline recovery protocol

Weeks of disconnection should be treated as normal, not exceptional, for an EFB/offline product.

Recovery sequence:
1. open local DB and verify schema/integrity;
2. surface pending/local-only state without blocking normal offline reading/entry;
3. establish authenticated transport opportunity;
4. exchange replica/cursor/version context;
5. push durable outbox idempotently;
6. receive acknowledgements;
7. pull remote changes since known cursor/version;
8. detect conflicts/deletions;
9. apply reconciliation transactionally;
10. retain unresolved conflicts for user review;
11. advance sync checkpoint only after successful apply;
12. expose final `synced` state only when defined invariants hold.

A partial failure resumes from durable checkpoints; it does not restart by blindly replaying an unbounded full dataset.

---

## 10. Security/privacy boundary

Synchronization introduces device identity, authentication, authorization, replay, data-at-rest, data-in-transit and lost-device risks. Stage 8 applies directly:
- pairing is not authentication unless cryptographic/device identity semantics establish it;
- encrypted transport does not prove the remote replica is authorized;
- operation IDs must not leak unnecessary personal information;
- logs/telemetry should not copy full flight records merely for debugging;
- backup files containing personal/logbook data need confidentiality/integrity handling appropriate to the product threat model;
- revoked/lost devices need a defined consequence if shared/cloud state exists.

No auth design is selected without product architecture.

---

## 11. Cross-track transfers

### Track A — owner
IndexedDB transaction/version behavior, Web Locks local coordination, service-worker lifecycle, transport/browser capability boundaries.

### Track E — co-owner
Replica trust, idempotency/replay requirements, backup/restore, migration/release safety, data-loss incident and transport/security architecture.

### Track B
Own explicit local-only/queued/syncing/synced/conflict/recovery UX and user control. Automatic behavior must remain inspectable and recoverable.

### Track C
Validation matrix now includes crash between local-save/outbox, multi-tab replay, schema-upgrade blocked state, offline weeks, duplicate acknowledgement loss, partial pull/apply failure, storage pressure, backup restore, update during pending outbox, and target Safari/Chromium/device runs.

### Track D
Future analytics must never define “saved” or “synced” from button clicks. Measurement should consume the synchronization state machine and privacy gate; offline events require delayed-upload/idempotency semantics of their own.

### Design Studio
Latest Web evidence (W023) is integrated Chromium transfer but not route/network/cross-browser/AT/device/field evidence. Sync/offline/conflict UX therefore remains a requirements handoff, not validated interaction quality.

### Software Engineering handoff
Implementation validation is now the principal dependency for: data model/IDs, transaction boundaries, migration harness, outbox protocol, idempotent endpoint, conflict algorithm, backup format, transport feasibility and target managed-iPad tests. Web Manager owns the web capability/risk contract, not the code implementation.

---

## 12. Target-device validation plan before choosing direct sync

On the actual managed company EFB, record exact iPadOS/Safari policy and test separately:
1. Home Screen web-app installation/launch;
2. service-worker controlled offline launch after reboot/extended idle;
3. IndexedDB persistence and `StorageManager` behavior;
4. export/restore route permitted by policy;
5. app suspension/resume with pending outbox;
6. feature detection for candidate background APIs;
7. candidate direct transport availability and required user gestures/permissions;
8. reachability under allowed Wi-Fi/cellular/airplane-mode states;
9. peer discovery/addressing without forbidden hotspot/manual reconnection assumptions;
10. authentication/pairing persistence;
11. sync after long offline interval and duplicate/retry failure injection;
12. data survival through PWA/service-worker/schema update.

A capability is PASS only for the tested device/OS/browser/policy matrix. “Safari supports X” is insufficient for managed-EFB acceptance.

---

## 13. Competency gate

PASS at foundation/practitioner specialization level if Web Manager can:
1. separate local persistence, sync, acknowledgement, replication and backup;
2. explain IndexedDB schema/version/blocked-upgrade risk;
3. require atomic local mutation + durable outbox semantics where applicable;
4. explain why retries require idempotency/deduplication;
5. distinguish conflict policy from transport choice;
6. design recovery for weeks offline and partial failure;
7. reject background sync as a universal correctness dependency;
8. compare server relay, WebSocket/WebTransport, WebRTC, Web Bluetooth and file fallback without inventing support;
9. define target managed-iPad validation before selecting direct peer sync;
10. hand implementation details to Software Engineering while retaining web-platform requirements.

**Result: PASS.** Production/device validation remains OPEN.

## Next high-value work
The strategic PWA foundation is now materially stronger: 073 covers lifecycle/offline/install/storage; 074 covers durability/sync/recovery/transport boundaries. The largest vertical curriculum gap is again Track D Stage 9 Analytics/Experimentation. Begin Stage 9 next, while carrying PWA offline event-delivery and install/standalone measurement as application cases. A later PWA implementation-validation block should resume when Software Engineering or target managed-EFB evidence becomes available.