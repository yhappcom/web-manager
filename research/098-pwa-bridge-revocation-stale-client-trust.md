# 098 — PWA Bridge Revocation, Stale-Client Trust & Data-Preserving Containment

Status: **PASS (generic) / PRODUCT REVOCATION + TARGET-DEVICE VALIDATION OPEN**  
Evidence date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: A Platform/Browser, B UX/IA/Content, C Quality/Accessibility, D Discovery/Analytics

## Why this block

097 defined explicit cross-context trust bridges. The unresolved failure is temporal: an installed PWA may remain offline while an origin, credential audience, native association, API/export/sync protocol or bridge generation is revoked. Revocation at the authority does not imply that a disconnected client has learned the new fact, and destructive cleanup can erase locally authoritative records before recovery.

## Track allocation

- **E owns** revocation authority, compatibility windows, containment and recovery policy.
- **A supplies** browser/network/update/storage mechanics and the fact that disconnected execution cannot receive remote state.
- **B consumes** stale-trust states as truthful task/recovery requirements.
- **C owns** stale-client, reconnect, accessibility and target-device negative evidence.
- **D consumes** campaign/deep-link/measurement retirement without converting stale discovery state into authorization.

Track E remains the highest-risk bottleneck. A/E foundations are mature generically; exact product runtime remains the blocker.

## SOURCE — credential revocation is server-side authority

RFC 7009 defines OAuth token revocation and requires refresh-token revocation support. It explicitly notes that clients must be prepared for unexpected invalidation and that propagation delay can exist. RFC 9700 further recommends refresh-token protection, rotation or sender constraint where applicable, inactivity expiry, and permits revocation after security events such as password change or logout.

### SYNTHESIS

A server can stop accepting a credential without an offline PWA knowing that fact. The disconnected client can only act on trust state already embedded or persisted locally until it reconnects or a locally enforceable expiry/constraint is reached.

### Guard

`authority revoked remotely ≠ disconnected client informed ≠ local capability immediately unavailable`.

Do not model remote revocation as an instantaneous broadcast to an offline EFB.

## Revocation classes are not interchangeable

A bridge can become unsafe because of different authorities:

1. **credential revocation** — token/grant/session/audience no longer accepted;
2. **origin revocation** — a destination/source origin is no longer trusted;
3. **protocol generation retirement** — old payload/operation semantics are no longer accepted;
4. **native association change** — website↔native association or handled path changes;
5. **key/signing/deployment incident** — previously trusted release/deployment authority is compromised;
6. **device/pairing revocation** — one peer/device must no longer synchronize;
7. **business integration retirement** — support/export/analytics third party is removed.

### Guard

`bridge retired ≠ every credential revoked ≠ every installed client updated ≠ every local record unsafe`.

Revocation must name the authority being withdrawn rather than collapsing all cases into “app blocked.”

## SOURCE — Apple Associated Domains are eventually refreshed

Apple documents that iOS 14+/macOS 11+ obtain `apple-app-site-association` data through an Apple-managed CDN. Current Supporting Associated Domains guidance says the CDN may fetch a domain file within 24 hours and devices check for updates approximately weekly after app installation. Apple also documents managed alternate mode for MDM-controlled devices. Universal-link handlers must still validate incoming parameters and avoid dangerous direct actions.

### SYNTHESIS

Changing an AASA file is not an instantaneous fleet-wide revocation channel. Cached association state can remain temporally stale. A managed-device deployment may have additional controls, but those require exact MDM/product evidence.

### Guards

`AASA changed at origin ≠ Apple CDN refreshed ≠ every device association refreshed`.

`native association removed ≠ stale offline client learned removal`.

Universal-link association must not be the sole emergency authorization control for sensitive operations.

## SOURCE — installed PWA metadata/update state can lag

Chromium-specific web.dev documentation shows manifest updates are checked/applied asynchronously and can be delayed; behavior differs by platform. Existing PWA research already establishes separately that Service Worker update discovery, installation, activation and control are distinct states.

### SYNTHESIS

Manifest, worker, bridge-policy and server generations can diverge. A bridge policy delivered only in a new shell/worker cannot contain a client that never receives that release.

### Guard

`new trust policy deployed ≠ installed PWA enforcing new trust policy`.

Remote policy is useful after contact; safety-critical offline behavior must also have bounded local rules where the threat model requires them.

## Data-preserving containment model

When stale trust is detected on reconnect, evaluate capabilities independently:

| Capability | Default generic posture after bridge trust failure |
| --- | --- |
| local read of authoritative records | preserve unless product security policy proves otherwise |
| local pending-record visibility | preserve |
| local write | product/threat dependent; do not infer |
| export/recovery | preserve through a trusted, explicit path where safe |
| remote read | reauthorize/revalidate |
| remote mutation | stop until current authorization/protocol is proven |
| outbox replay | pause; do not discard |
| retired bridge invocation | deny |
| diagnostics | privacy-minimized and versioned |

This is a generic safety direction, not a LogMate production policy.

### Guards

`sync denied ≠ local record should be deleted`.

`outbox replay paused ≠ outbox discarded`.

`bridge untrusted ≠ origin storage should be wiped`.

## SOURCE — destructive origin cleanup is broad

`Clear-Site-Data: "storage"` signals deletion of origin storage including IndexedDB and Service Worker registrations in supporting browsers. `"cookies"` also has domain-wide implications for cookies. This is intentionally broad cleanup, not a precise bridge-revocation primitive.

### MINTTAP DIRECTION

Do not use broad site-data clearing as the default response to token, peer, protocol, native-association or third-party bridge revocation when irreplaceable local records/outbox may exist.

A destructive wipe requires a separate data-destruction authorization and recovery/backup assessment.

## Revocation epoch / generation model

For bridges whose trust can change, implementation handoff should consider an explicit monotonic policy/generation concept rather than ambient booleans. A reconnecting client can compare its last-known generation with current authority and enter reconciliation before remote mutation.

A generic bridge record may need:

- bridge identifier and protocol/schema generation;
- credential audience/scope and expiry;
- peer/device identity where applicable;
- last authority validation time/generation;
- minimum accepted generation;
- operation classes allowed offline;
- queued operation generation;
- reason/state for retirement;
- migration/recovery path;
- diagnostic schema version.

This does **not** prove that a client with an old generation is malicious or wrong. It proves only that current authority must decide whether that generation remains acceptable.

### Guard

`stale trust metadata ≠ corrupted user data`.

## Reconnect state machine

A safe generic reconnect sequence is:

`offline/local-capable → connectivity candidate → authenticate current authority → fetch current trust/protocol policy → compare generations/audiences/peer status → freeze unsafe replay → migrate/re-authorize if supported → reconcile authoritative local/outbox state → resume only allowed capabilities`.

Do not make “network came back” equivalent to “flush queue immediately.”

### Guard

`network restored ≠ trust restored ≠ replay authorized`.

This transfers directly to Software Engineering D006/F005 semantics: a timeout, late completion or prior queued operation can coexist with a new authority decision, so terminal operation state must not be inferred from caller waiting state.

## Revocation race/failure analysis

### Credential revoked while offline
The PWA continues locally under last-known offline policy. On reconnect, remote mutation must re-establish current authorization before replay.

### Peer/device revoked while both sides have pending data
Revocation prevents new trusted synchronization but must not silently delete pending authoritative records. Recovery/export/reconciliation policy is separate.

### Protocol N retired while client N has queued operations
The server should not blindly accept unknown semantics; the client should not drop the queue. A migration/translation or explicit unsupported recovery path is required.

### Origin/third-party bridge removed after compromise
New clients stop using it, but stale clients may still possess old URLs/configuration. Server-side rejection and credential revocation are stronger containment than relying only on a future client update.

### AASA/native association changed
The association may remain cached for a period. Receiving native code must continue validating route/operation authorization even while association state is transitioning.

### Release/signing/deployment incident
A repaired origin does not prove installed workers/clients are clean. 092/095 recovery evidence remains required before sensitive bridge authority resumes.

## UX/content contract

Track B/Design Studio should distinguish at least:

- **Saved locally — sync authorization must be renewed**;
- **Sync paused — this device/connection is no longer trusted**;
- **Update required before synchronization — records remain on this device**;
- **Recovery/export available** where actually true;
- **Do not erase local data** where unsynced authoritative records exist.

Do not claim “signed out”, “revoked”, “updated” or “synced” from a weaker observed state.

## Accessibility/quality validation

Track C should exercise:

- revocation arriving before replay;
- revocation during replay;
- credential expiry while offline;
- old client reconnect after N+k releases;
- peer/device revoked with pending records;
- protocol retired with old outbox entries;
- AASA/native route changed while stale association remains;
- compromised bridge removed while stale shell/worker remains;
- server unreachable during revocation check;
- false-positive/temporary authorization failure;
- keyboard/focus/status-message behavior for paused/recovery states;
- Chromium plus independent engine; Safari and managed iPad separately;
- no destructive cleanup as a hidden test precondition.

Production PASS requires exact artifact, server policy, target device and applicable AT evidence.

## Track D transfer

Search/social/campaign URLs can remain indexed or shared after a route/integration retires. Discovery staleness is not authorization. Retired campaign/deep-link parameters should degrade to safe navigation/help, not regain privileged bridge operations. Analytics continuity must not preserve credentials or sensitive bridge authority merely to maintain attribution.

## Product/EFB implications

For a LogMate-like company EFB, exact offline authorization duration, local unlock policy, MDM revocation, pairing identity, native association, sync protocol and data-destruction policy are unknown and remain OPEN. Generic web evidence cannot prove unattended revocation delivery to an offline managed iPad.

If immediate containment while disconnected is a requirement, Web/PWA server revocation alone is insufficient evidence; exact OS/MDM/device-bound controls and their failure behavior require Software Engineering/security/managed-device validation.

## DEPENDENCY / transfer evidence

- **Design Studio:** current Web Design is Stage 3 PRACTICE; W049 runtime execution, Safari, screen-reader and physical-device evidence remain OPEN. Consume its state/recovery interaction evidence but do not infer target-device PASS.
- **Software Engineering Studio:** Foundation remains IN STUDY. F005 distinguishes caller timeout from underlying operation cancellation; D006 owns retry/idempotency/conflict evidence. This supports the requirement to freeze/reconcile replay after trust changes, but does not prove browser/PWA implementation behavior.

## VALIDATION handoff

Engineering/product evidence should inventory every revocable bridge and record:

1. revocation authority and trigger;
2. online enforcement point;
3. offline knowledge/expiry rule;
4. server-side rejection independent of client update;
5. client policy generation and stale-client behavior;
6. pending authoritative data/outbox preservation;
7. migration/recovery/export path;
8. exact error/status semantics;
9. incident diagnostics without secrets/record overcollection;
10. managed-iPad/Safari/native-app execution where applicable.

## CHANGE WATCH

- OAuth/browser-based-app security guidance and sender-constrained token practices remain current-security material.
- Apple Associated Domains CDN/update behavior and managed alternate modes are platform policy/implementation and require periodic recheck.
- Manifest/install metadata update behavior differs across browsers/platforms and must not be generalized from Chromium documentation.
- Any future managed-EFB MDM revocation or native sync mechanism requires exact current Apple/vendor evidence.

## Integrated judgment

Revocation is not deletion and it is not instantaneous knowledge. The durable design rule is:

> Withdraw the smallest unsafe capability at the authority that can actually enforce it, make stale clients prove current trust before remote mutation/replay, and preserve locally authoritative data until an independently authorized recovery/destruction decision exists.

This closes the generic stale-client trust prerequisite. Product validation remains OPEN.