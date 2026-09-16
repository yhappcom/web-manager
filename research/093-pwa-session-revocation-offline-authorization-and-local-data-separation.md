# 093 — PWA Session Revocation, Offline Authorization & Security-Sensitive Local Data Separation

Status: **PASS (generic) / PRODUCT AUTHORIZATION + DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A browser/session/storage mechanics; Track B truthful recovery/account-state UX; Track C fault/security acceptance; Track D privacy-minimized measurement.  
Related: 084, 085, 088–092.

## Why this block exists

085 separated prior authentication, current server authorization, local unlock and offline authorization. 092 separated trusted transport from trusted release/update authority. The remaining high-risk boundary is what happens when an authenticated installed PWA becomes disconnected, a credential/session is revoked or an account enters recovery while authoritative records and pending mutations still exist locally.

For an EFB-like product this cannot be reduced to ordinary website logout. Confidentiality may favor deletion, while availability/recoverability may require preserving the only copy of an unsynchronized flight record. The system therefore needs an explicit authorization-and-data-lifecycle contract rather than a single `loggedIn` flag or indiscriminate origin wipe.

## SOURCE — current authoritative/high-quality evidence

### Session continuity and invalidation

NIST SP 800-63B states that continuity of an authenticated session is based on possession of a verifier-issued session secret and requires periodic reauthentication. This supports treating server session continuity as a time-bounded authorization mechanism rather than durable proof that an offline client remains authorized forever.

Source: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-63b.pdf

OWASP Session Management guidance requires server-side session invalidation on expiry/logout and recommends secure cookie controls. It also distinguishes session invalidation from residual sensitive content that may remain in browser caches/storage.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

### Cache semantics are not authorization semantics

HTTP `Cache-Control: no-store` prevents caches from storing a response; `private` prevents shared-cache reuse of personalized responses; `no-cache` permits storage but requires revalidation before reuse. These HTTP cache directives do not themselves define whether application-owned IndexedDB records may remain available offline.

Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control

Service Worker Cache Storage is application-managed and distinct from the browser HTTP cache. Current Service Worker specifications preserve origin/security boundaries; application cache contents therefore require explicit ownership/lifecycle policy rather than assuming HTTP response directives alone govern all PWA local data.

Source: https://www.w3.org/TR/service-workers/

### Clear-Site-Data is powerful and destructive

`Clear-Site-Data` can instruct a user agent to clear cookies, cache and origin storage; the `storage` category includes DOM-accessible storage and service-worker registrations. The specification explicitly frames local data as both sensitive and valuable. MDN documents the header as a secure-context mechanism with broad clearing effects.

Sources:
- https://www.w3.org/TR/clear-site-data/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data

This makes it a security tool, not a safe generic logout primitive for an offline-first application containing irreplaceable unsynchronized records.

## SYNTHESIS — authentication is not one state

A durable PWA should model at least these independently:

1. **Identity binding** — which account/device context local data belongs to.
2. **Server session validity** — whether current online requests are accepted under a live session/credential.
3. **Local unlock state** — whether this device currently permits access to protected local material.
4. **Offline authorization lease/policy** — what operations are permitted without current server confirmation, and for how long/under what conditions.
5. **Mutation authority** — whether a locally accepted mutation is merely pending or is already acknowledged by the authoritative remote system.
6. **Recovery state** — whether account recovery, credential rotation, device replacement or suspected compromise changes what may be viewed, edited, exported or synchronized.

Guard:

`identity previously proven ≠ server session currently valid ≠ local data currently unlocked ≠ offline operation authorized ≠ pending mutation remotely accepted`.

## SYNTHESIS — revocation is a propagation problem

Server-side revocation can immediately reject requests that reach the server. It cannot retroactively reach a device that is offline. Therefore:

`credential revoked at server ≠ disconnected PWA instantly aware ≠ local data instantly inaccessible`.

This is structurally similar to the offline kill-switch limitation established in 091. A product requiring immediate offline revocation needs a device/platform enforcement mechanism that exists independently of server reachability; generic PWA evidence does not establish such a mechanism for the managed-iPad scenario.

### Required revocation states

A reconnecting client should be able to distinguish at least:
- session expired but account otherwise valid;
- credential rotated/revoked;
- account recovery in progress;
- account disabled/deleted;
- device/pairing revoked;
- server temporarily unreachable/indeterminate.

These states should not all collapse to `401 → delete local data`.

## SYNTHESIS — classify local data by security and recoverability role

A single origin can contain materially different data classes:

| Class | Example role | Default lifecycle principle |
| --- | --- | --- |
| Reconstructible public assets | shell/static assets | replace/evict freely when compatible |
| Reconstructible account data | server-confirmed projection/reference data | may be discarded and refetched if recoverability is proven |
| Session/auth material | session identifiers/tokens | minimize persistence; invalidate/rotate according to auth contract |
| Security-sensitive derived state | cached privilege/account flags | never treat stale local copy as current server authority |
| Authoritative local record | offline-created unsynced record | preserve until independently recoverable/acknowledged unless explicit destructive policy applies |
| Durable outbox | pending operations | preserve with identity/protocol metadata until acknowledged/reconciled or deliberately abandoned |
| Backup/export material | independent recovery copy | separate lifecycle, protection and user-visible verification |
| Diagnostics | structural state metadata | minimize, version and exclude credentials/user-record payload by default |

This classification prevents a security response from deleting irreplaceable data merely because cookies and IndexedDB share one browser origin.

## CONTRADICTION — generic logout advice vs offline-first safety

Conventional web guidance often recommends clearing local sensitive data at logout. That is reasonable when the server remains authoritative and local content is reconstructible. In an offline-first EFB-like application, the same action can destroy the only copy of an accepted local record.

Resolution: logout must be split into distinct actions/semantics:

- terminate/revoke online session;
- lock or hide protected local material;
- stop remote synchronization until reauthentication;
- preserve unacknowledged authoritative local records/outbox when required for recovery;
- optionally purge reconstructible caches;
- destructive erasure only after explicit policy/precondition proves data is recoverable or intentionally abandoned.

`logout ≠ origin wipe`.

## MINTTAP / LOGMATE DIRECTION — authorization matrix before implementation

No product-specific auth implementation is assumed. Before implementation, define a matrix across these operations:

| State | Read local confirmed | Read local pending | Create/edit local | Export/backup | Remote read | Remote write/replay |
| --- | --- | --- | --- | --- | --- | --- |
| online + session valid | policy-defined | policy-defined | policy-defined | policy-defined | allowed | allowed |
| offline + within offline policy | explicit | explicit | explicit | explicit | unavailable | queued only |
| offline + authorization age exceeded | explicit degraded policy | preserve | block or quarantine unless explicitly allowed | recovery policy | unavailable | unavailable |
| reconnect + session expired | preserve | preserve | degraded policy | recovery policy | reauth required | reauth required |
| credential/device revoked | confidentiality/recovery policy | preserve-before-destruction decision | normally stop authoritative mutation | controlled recovery path | denied | denied |
| account recovery/deletion | explicit recovery/retention contract | explicit recovery/retention contract | normally restricted | explicit | policy | policy |

The exact cells are a product/security decision and remain OPEN. The reusable finding is that each capability must be decided independently.

## MINTTAP / LOGMATE DIRECTION — no destructive cleanup before recovery invariant

For irreplaceable offline records, a destructive client cleanup should require evidence equivalent to one of:

1. every authoritative local record/outbox entry has remote acknowledgement and reconciliation; or
2. an independent backup/export has been created and restore-tested under the applicable schema/protocol; or
3. the user/administrator intentionally invokes a destructive workflow under an approved retention/security policy.

A support script must not default to `Clear-Site-Data: "storage"`, browser-site-data clearing, reinstall, or origin reset before checking this invariant.

## TRANSFER VALIDATION — Software Engineering Studio

Software Engineering `D004` executable evidence separates confirmed base, pending mutation and cache/projection semantics. That directly supports this Web Manager contract: authentication cleanup must not collapse pending authoritative mutation into disposable cache. `D005` further separates backup existence from semantic restore acceptance.

Transfer boundary: those fixtures are Python/Linux mechanism evidence, not FlutterFire/iOS/managed-iPad runtime proof. Exact product behavior remains Software Engineering/target-device validation.

## DEPENDENCY — Design Studio

Track B requires truthful user-visible states such as:
- session expired — records remain saved on this device;
- reauthentication required before sync;
- offline authorization expired — viewing/export may remain available while editing/sync is restricted;
- device/account access revoked — recovery action required;
- local records pending — do not erase site data;
- backup verified / backup not verified.

Design Studio owns visual/interaction realization. Current Design Studio Web Stage 3 remains PRACTICE; no Safari, screen-reader, physical-device or human-UX PASS is inferred.

## Track integration

### Track A — Platform & Browser
Owns cookie, HTTP cache, Service Worker Cache Storage, IndexedDB/origin and Clear-Site-Data mechanics. Key transfer: storage mechanisms share an origin but do not share semantic authority.

### Track B — UX / IA / Content
Consumes the authorization-state matrix and makes local/remote/recovery status comprehensible without implying data loss or successful sync.

### Track C — Performance / Accessibility / Quality
Acceptance must fault-inject session expiry/revocation during offline work, reconnect, pending outbox, update/migration and recovery. Assertions target data/security invariants, not only UI response codes.

### Track D — Search / Discovery / Analytics
Authentication/recovery telemetry must remain privacy-minimized. An offline revoked device may emit no telemetry; absence of events cannot prove fleet revocation completion.

### Track E — Architecture / Security / Operations
Owns revocation propagation, authorization lease/policy, data-class lifecycle, account/device recovery, incident handling and destructive-cleanup gates.

## Validation matrix for implementation handoff

Exact-artifact tests should include:

1. session expiry while online with no pending data;
2. session expiry while offline with new unsynced records;
3. logout while pending outbox exists;
4. server credential revocation while client is offline, then reconnect;
5. device/pairing revocation while offline;
6. password/account recovery while another installed PWA remains offline;
7. `401/403` during replay after local acceptance;
8. account deletion/disable response with local pending records;
9. browser/site-data clearing attempted with unverified backup;
10. cache purge that must not remove authoritative records/outbox;
11. worker update/migration concurrent with reauthentication;
12. long-offline N→N+k client returning with old auth state and old queued-operation format;
13. accessibility of expired/revoked/recovery states without forced focus loss;
14. physical managed-iPad process termination/relaunch across each critical state.

Required oracles include record count/content identity, outbox identity, local commit state, remote acknowledgement, server rejection reason, current session generation, local authorization state, backup/restore verification and destructive-action audit evidence.

## CHANGE WATCH

- browser behavior/support for `Clear-Site-Data` directives and storage clearing;
- Service Worker/Storage specification changes;
- Safari/WebKit Home Screen storage/session behavior;
- WebAuthn/session-management guidance and applicable identity standards;
- managed-iPad/MDM controls that could provide stronger device-level revocation or data protection than generic web APIs.

## OPEN

Product closure requires exact evidence for:
- actual authentication/session/token/cookie architecture;
- session duration/reauthentication/revocation rules;
- whether any local unlock/device-bound credential exists;
- offline authorization requirements and maximum disconnected duration;
- which records are authoritative locally before sync;
- logout/account-deletion/device-revocation retention policy;
- actual IndexedDB/Cache Storage separation and encryption/key-management model;
- backup/restore guarantees;
- managed-iPad data-protection/MDM behavior;
- physical Safari/Home Screen execution and accessibility/security review.

## Gate judgment

**PASS (generic).** The reusable web-security/operations model now closes the conceptual gap between session revocation, offline authorization and local-data lifecycle. It does not certify any MintTap/LogMate implementation. Production validation remains OPEN until exact authentication, storage, recovery and managed-device evidence exists.
