# 091 — PWA Long-Offline Release Coexistence, API Retirement & Incident Containment

Status: **PASS (generic governance/compatibility contract) / PRODUCT EXECUTION OPEN**  
Date: 2026-09-17

## Purpose
Extend 090 from exact-release support into fleet reality: installed PWAs may remain offline across multiple releases, then reconnect with old shell/worker/schema/protocol/outbox state. Track E owns the compatibility/retirement/containment contract; A supplies worker/platform mechanics, B owns truthful unsupported/degraded task states, C owns compatibility/fault acceptance, and D consumes bounded fleet evidence without treating reporting clients as the fleet denominator.

## Integrated model
`release generation → supported compatibility envelope → staged rollout → coexistence observation → deprecation notice → migration opportunity → retirement gate → reconnect containment → recovery/reconciliation → evidence-based retirement`.

## SOURCE — HTTP deprecation and sunset are distinct
RFC 9745 (Standards Track, March 2025) defines the `Deprecation` HTTP response header. Declaring a resource deprecated does not itself change resource behavior. RFC 9745 explicitly allows `Sunset` to be used in addition when the deprecated resource is expected to become unresponsive at a specific time, and requires the Sunset timestamp not to precede Deprecation.

RFC 8594 defines `Sunset` as an informational signal that a URI/resource/service is likely to become unresponsive at a specified future time. It treats retirement as distinct from the earlier phase where an API is merely no longer preferred.

**SYNTHESIS:** `deprecated ≠ unavailable`; `sunset announced ≠ safe to retire`. HTTP headers can communicate lifecycle intent to connected clients, but a long-offline PWA cannot receive a header while disconnected. Therefore server-side signaling is one evidence/communication channel, not the retirement safety mechanism.

Guard: `deprecation signal delivered ≠ every installed client informed ≠ migration completed`.

## SOURCE — Service Worker implementation remains change-watch
W3C Service Workers continued Candidate Recommendation Draft publication through 2026-08-12. Safari 26.6 (2026-07-27) included service-worker and networking fixes. The lifecycle model is mature enough for architecture, while exact WebKit behavior remains CHANGE WATCH and target-device execution remains required.

## 1. Compatibility envelope, not “latest version”
For a long-offline fleet define support over a tuple:
`client/shell generation × controlling-worker generation × persisted-schema generation × API/protocol generation × queued-operation format × server acceptance rules`.

A server may be on N+k while a returning client is still N. A worker update alone cannot prove that persisted data or queued mutations are compatible.

### Compatibility record
For each consequential release retain:
- release/build generation;
- worker/shell generation;
- readable local-schema range;
- writable local-schema range;
- API/protocol versions emitted and accepted;
- outbox/event versions emitted and replayable;
- migration paths, including skipped-version paths;
- oldest supported returning generation;
- downgrade/rollback limitations;
- remote feature/operation gates;
- evidence tier and exact tested combinations.

Guard: `server compatible ≠ local schema compatible ≠ queued operation replayable`.

## 2. Deprecation lifecycle
Use lifecycle states rather than a binary supported/unsupported flag:
1. **current/preferred** — normal support;
2. **supported-old** — still accepted; migration/update encouraged;
3. **deprecated** — behavior remains available but retirement intent/documentation is explicit;
4. **retirement-pending** — sunset criteria/date may be announced, but evidence gate is not yet closed;
5. **remote-write restricted** — unsafe remote mutation is blocked while safe local preservation/read may remain;
6. **remote protocol retired** — server no longer accepts that protocol/operation version;
7. **recovery-only** — client must preserve/export/migrate authoritative local data before normal remote operation;
8. **retired** — only after defined recovery/retention obligations are satisfied.

Do not map HTTP Deprecation/Sunset mechanically to these product states; they are protocol signals that can support the broader lifecycle.

## 3. Offline-safe retirement gate
Before retiring an old protocol or queued-operation format require evidence for:
- minimum plausible offline duration and return population are understood or explicitly unknown;
- supported-old client can receive/update when it reconnects;
- skipped-version migration is tested;
- authoritative local records survive unsupported remote state;
- old queued operations are either replayable, transformable, or explicitly recoverable without silent loss;
- user can distinguish local preservation from remote acknowledgement;
- independent backup/restore path is not invalidated;
- support can diagnose generation/schema/outbox state without destructive clearing;
- rollback/forward-fix consequences are known;
- retirement owner and emergency extension authority are explicit.

**MINTTAP/LOGMATE DIRECTION:** for irreplaceable flight records, server protocol retirement must never silently convert “pending local authoritative data” into “discarded because client is old.” Product implementation remains OPEN.

## 4. Unsupported client is a capability state, not necessarily an app-wide lockout
Separate capabilities:
`local read | local write | export/backup | migration | remote read | remote write | sync replay | diagnostics/support`.

An obsolete remote protocol may justify blocking remote writes while preserving local read/export/recovery. A forced full-screen lockout can increase data-loss risk when the device holds the only authoritative unsynchronized record.

### Track B truthful states
Examples requiring product-language/design validation:
- update recommended; normal operation remains supported;
- update required before remote synchronization;
- records remain saved on this device; synchronization is paused;
- migration required; do not clear local data;
- recovery/export required before this version can reconnect;
- remote service unavailable for this version, but local records remain accessible where safe.

Visual/interaction realization belongs to Design Studio. Exact wording is product/legal/support dependent.

## 5. Kill switch design must be narrower than “disable app”
Emergency controls should target the smallest unsafe capability:
- disable a specific remote mutation;
- reject a dangerous protocol/event version;
- force server read-only for a generation;
- stop background/retry replay while preserving outbox;
- prevent activation of a known-bad migration/update where technically possible;
- require recovery/update before a particular operation.

A kill switch needs authenticated configuration, bounded scope, expiry/review, audit trail and a failure mode when the device is offline and cannot receive the switch.

Guard: `remote kill switch configured ≠ offline client contained`.

Therefore offline safety must be built into the shipped artifact/invariants; remote controls are supplementary containment.

## 6. Rollback vs forward-fix
Separate:
`origin/server rollback ≠ service-worker rollback ≠ shell rollback ≠ persisted-schema rollback ≠ outbox-format rollback`.

If a new client has already performed an irreversible local migration or emitted a new operation format, reverting the server or static origin may create a worse compatibility pair. Release records must state whether rollback is safe for each generation combination; otherwise forward-fix/recovery may be the safer incident action.

### Decision rule
Prefer rollback only when the older serving stack is proven compatible with already-published client/schema/outbox states. Otherwise contain the unsafe capability and forward-fix/migrate.

## 7. Diagnostic schema evolution
Diagnostics themselves need a compatibility contract:
- diagnostic schema version;
- stable core fields for release/worker/schema/outbox/recovery state;
- additive evolution preferred where feasible;
- unknown-field tolerance;
- server parser support window;
- privacy/redaction version independent of application schema;
- no requirement to expose authoritative payload content merely because an old diagnostic schema is hard to parse.

Guard: `application protocol compatible ≠ diagnostic schema compatible`.

Silent old clients remain denominator-unknown; telemetry from reporting clients cannot prove fleet-wide retirement safety.

## 8. Staged rollout for installed/offline clients
A percentage rollout of origin traffic is insufficient as the sole model because installed clients may not contact origin during the rollout. Observe/validate generation diversity:
- current generation clean install;
- N-1 returning client;
- oldest supported N-k returning client;
- pending-outbox client;
- migration-interrupted fixture;
- storage-pressure/reconstructed-cache fixture;
- client reconnecting after API deprecation notice was missed while offline.

Acceptance focuses on data/task invariants, not merely successful navigation.

## 9. Incident containment matrix
When a release/protocol defect is discovered classify:
- can unsafe behavior occur fully offline?
- does it require remote response/config?
- can server reject the unsafe mutation without destroying local intent?
- can the client preserve/export authoritative data?
- is schema already migrated?
- are pending operations transformable/idempotent?
- will rollback create an older-code/newer-state pair?
- can support identify the affected generation without collecting sensitive payloads?

Containment priority:
`prevent irreversible corruption/loss → preserve authoritative local data/outbox → restrict smallest unsafe capability → communicate truthful state → recover/migrate → reconcile → restore normal capability`.

## 10. Cross-repository transfer
### Design Studio
Latest Web status (2026-09-17): Stage 1/2 PASS; Stage 3 PRACTICE / NOT PASSED. W042 export→live authority recheck is ready but execution OPEN; no Safari/cross-browser/screen-reader/physical-device/human-UX PASS exists. Transfer: unsupported/deprecated/recovery-only states need durable authority/freshness disclosure, but Web Manager does not claim their visual/runtime validation.

### Software Engineering
Latest Studio status (2026-09-17): Foundation IN STUDY. D005 executable bounded evidence demonstrates `backup artifact exists ≠ physical integrity ≠ schema compatibility ≠ semantic recovery`. Transfer: protocol retirement and client update must not invalidate the independent recovery contract; a structurally valid restored store can still be unreadable by the intended application generation.

Required implementation evidence includes exact LogMate compatibility matrices, skipped-version migration, old-outbox replay/transformation, restore into intended reader generation, and managed-iPad interruption/network tests.

## 11. Five-track balance after 091
- **A:** strong mechanics; current Service Worker/WebKit implementation remains CHANGE WATCH.
- **B:** consumes lifecycle states into truthful update/deprecation/recovery IA; Design Studio execution dependency remains.
- **C:** owns compatibility matrix/fault-oracle evidence; physical Safari/iPad/AT remains OPEN.
- **D:** owns rollout/analytics interpretation but cannot certify silent offline populations from telemetry alone.
- **E:** remains highest-risk live bottleneck; 091 adds lifecycle retirement, kill-switch and containment governance.

No track requires another foundation primer. Next work should consume executable product evidence if available; otherwise examine security/supply-chain/update-integrity controls for the PWA release path or a fresh platform change-watch gap.

## OPEN / VALIDATION
- actual LogMate API/protocol/outbox/schema generations do not yet exist as validated product evidence;
- maximum/typical EFB offline duration and fleet update policy are unknown;
- actual MDM update/control capability is unknown;
- exact managed-iPad Home Screen update/retention and interruption behavior remains unexecuted;
- server-side compatibility/deprecation policy is not yet a product decision;
- recovery-only/read-only UX and AT behavior require Design Studio + target-device execution;
- emergency control/kill-switch implementation and authorization are OPEN.

## CHANGE WATCH
- Service Worker specification and WebKit implementation;
- Safari/iPadOS Home Screen behavior and managed-device policy;
- RFC/application ecosystem adoption of Deprecation and Sunset signaling;
- product backend/API evolution once implementation exists.

## Competency checkpoint
**PASS at generic expert-governance level.** The Web Manager can now govern long-offline PWA release coexistence, distinguish deprecation from retirement, define compatibility envelopes, avoid destructive unsupported-client lockout, reason about rollback vs forward-fix, and define offline-aware incident containment. Product acceptance remains OPEN pending exact artifact/backend/managed-device evidence.

## Sources
- RFC 9745, `The Deprecation HTTP Response Header Field`, Standards Track, March 2025; accessed 2026-09-17.
- RFC 8594, `The Sunset HTTP Header Field`, Informational, May 2019; accessed 2026-09-17.
- W3C Service Workers publication history, Candidate Recommendation Draft through 2026-08-12; accessed 2026-09-17.
- WebKit, `WebKit Features for Safari 26.6`, 2026-07-27; accessed 2026-09-17.
- `yhappcom/design-studio` `progress/WEB_STATUS.md`, checked 2026-09-17.
- `yhappcom/software-engineering-studio` `progress/STATUS.md`, checked 2026-09-17.