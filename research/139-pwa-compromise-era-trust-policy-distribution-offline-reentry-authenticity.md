# 139 — PWA Compromise-Era Trust-Policy Distribution & Offline Re-entry Authenticity

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + TRUST-METADATA + RECOVERY-PATH + PHYSICAL-DEVICE VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 099–102 trust-policy anti-rollback/rebootstrap; 117–121 containment/normalization; 135–138 provenance/crypto/compromise recovery; Track A Service Worker/cache lifecycle; Track B truthful re-entry UX; Track C destructive stale-client validation; Software Engineering owns implementation.

## Purpose

138 established that a compromised authority cannot safely be the sole authority for its successor. The adjacent problem is distribution: after successor trust exists centrally, how can a long-offline PWA authenticate the new minimum trust/revocation state without accepting replayed old policy, stale caches, or an attacker-selected successor?

Central rule:

> **Re-entry is not “fetch latest and trust it.” A client needs an authenticated trust-transition path plus locally durable anti-rollback state; stale runtime/cache state may transport candidate policy but must not choose the accepted trust epoch.**

This study does not prescribe TUF, PKI, transparency logs, HSM/KMS, MDM, a specific browser API, or a LogMate implementation.

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** Service Worker update, Cache Storage, navigation and long-offline lifecycle determine what stale code/data may execute or be presented; they do not establish cryptographic freshness.
- **B UX/IA/Content — elevated consumer:** owns truthful `local data available`, `trust update required`, `sync blocked`, `re-entry failed`, `review required`, and partial-recovery states.
- **C Quality — high dependency pressure:** owns rollback/freeze/mix-and-match, stale-cache, reinstall/restore, clock, interruption and physical-iPad matrices.
- **D Search/Analytics — constrained consumer:** fleet/version telemetry can estimate observed adoption but cannot authenticate a client's trust state or prove fleet completeness.
- **E Architecture/Security/Operations — highest-risk owner:** owns trust metadata, minimum accepted epoch, recovery bootstrap, policy distribution, compromise-era revocation and re-entry acceptance.

Allocation remains E-heavy with A/C prerequisites and B consequence communication.

## 2. SOURCE — secure update systems need rollback, freeze and mix-and-match defenses

The Update Framework (TUF) Specification **v1.0.36, modified 5 August 2026**, is a current reference architecture for secure update metadata. It explicitly targets rollback, indefinite freeze, mix-and-match, fast-forward and key-compromise attacks. Clients persist trusted metadata, reject metadata older than previously trusted versions, enforce expiry, bind snapshot metadata to timestamp metadata, and use signed role/threshold relationships.

Source checked 2026-09-19: https://theupdateframework.github.io/specification/latest/

TUF is transfer evidence, not a MintTap implementation mandate.

**SYNTHESIS:** TLS and a valid signature on one downloaded object are insufficient to establish that a long-offline client has the newest acceptable trust policy. Freshness, monotonicity, role authority and cross-object consistency are separate claims.

Guards:
- `HTTPS fetch succeeded ≠ trust policy is current`;
- `policy signature valid ≠ policy is fresh`;
- `fresh-looking timestamp ≠ trusted monotonic progress`;
- `newer version number ≠ legitimate successor`;
- `all files individually valid ≠ files belong to one legitimate policy snapshot`.

## 3. SOURCE — root compromise requires out-of-band recovery in a mature update model

TUF states that the client ships with trusted root keys and that root metadata delegates top-level authority. It further states that if a threshold of root keys is compromised, root keys should be updated out-of-band. This reinforces 138's rule that an attacker controlling the old root must not be allowed to self-authorize an attacker successor.

Source: https://theupdateframework.github.io/specification/latest/

**TRANSFER VALIDATION:** the reusable principle is independent rebootstrap, not TUF's exact role model.

Guards:
- `old root signs new root ≠ safe recovery after threshold compromise`;
- `server says successor is current ≠ successor independently trusted`;
- `same HTTPS origin ≠ same recovered provenance authority`;
- `new Service Worker fetched from origin ≠ compromise-era trust reset proven`.

## 4. Minimum accepted trust state is a floor, not a suggestion

A re-entering client needs a locally durable representation of the strongest trust state it has already accepted, sufficient for the declared threat model. Candidate dimensions may include trust-policy epoch/version, root/verifier generation, revocation floor, accepted lineage/checkpoint, and compatibility policy. Exact fields are product-dependent.

The floor must not be silently lowered by:
- restored browser backup;
- stale IndexedDB/Cache Storage;
- imported recovery package;
- old Service Worker/application generation;
- server/mirror replay;
- device clock rollback;
- user reinstall unless a separately authenticated reset/rebootstrap policy authorizes it.

Guards:
- `local state restored ≠ trust floor may roll back`;
- `app reinstalled ≠ compromise history erased`;
- `cache contains signed policy ≠ cache policy may lower accepted epoch`;
- `imported package is older but valid ≠ current authority rolls back`.

**OPEN:** browser-origin storage alone may not survive deletion/reinstall/device replacement and therefore cannot be assumed to provide a device-lifetime monotonic root. Exact durable floor storage requires implementation/platform evidence.

## 5. Freshness is not one mechanism

Freshness can be supported by monotonic versioning, bounded expiry, independently trusted checkpoints/receipts, current server state under successor trust, or other architecture-specific evidence. Wall-clock time alone is insufficient when device clocks can be wrong or manipulated.

TUF's client workflow combines version monotonicity and expiry and explicitly notes bogus-clock support as an open concern in the specification. This is useful evidence that freshness is compositional.

Guards:
- `not expired according to device clock ≠ globally fresh`;
- `higher epoch ≠ authentic epoch`;
- `authentic epoch ≠ complete revocation state`;
- `client knows current root ≠ client knows current policy snapshot`.

## 6. Freeze and denial-of-update must remain distinguishable from safe acceptance

A network attacker can often prevent an update even when unable to forge a valid one. TUF explicitly distinguishes protection against accepting bad updates from guaranteed update availability during attack.

**MINTTAP DIRECTION:** when current trust cannot be established, do not silently accept stale policy merely to restore availability. Preserve safe local read/export where product semantics permit, but block consequence-bearing remote mutation until re-entry requirements are met.

Guards:
- `cannot update trust policy ≠ accept old policy`;
- `availability pressure ≠ rollback authorization`;
- `re-entry blocked ≠ local irreplaceable data should be deleted`;
- `local read available ≠ remote write authority restored`.

## 7. Service Worker and Cache Storage are runtime state, not trust oracles

The W3C Service Workers specification states that Cache instances are distinct from the HTTP cache, are author-managed, do not automatically update, and do not disappear merely because the Service Worker script updates. The current nightly specification also specifies update-fetch cache behavior for Service Worker scripts.

Source checked 2026-09-19: https://www.w3.org/TR/service-workers/

**SYNTHESIS:** compromise-era policy must not be accepted merely because a current worker controls the page, and an updated worker must explicitly account for stale application caches/state.

Guards:
- `Service Worker current ≠ cached trust policy current`;
- `worker activated ≠ every open client converged`;
- `cache entry signed ≠ cache entry fresh`;
- `cache cleared ≠ trusted floor safely reset`.

## 8. Re-entry acceptance should be staged

Generic state model:
1. `LOCAL-PRESERVED / TRUST-UNKNOWN` — irreplaceable local data retained; no current remote authority claimed.
2. `REENTRY-CANDIDATE-RECEIVED` — candidate successor policy/recovery package obtained.
3. `SUCCESSOR-AUTHENTICATED` — candidate bound through accepted independent recovery path.
4. `ANTI-ROLLBACK-CHECKED` — candidate does not violate local/current minimum trust floor.
5. `POLICY-CONSISTENCY-CHECKED` — root/verifier/revocation/compatibility objects form one acceptable state rather than a mix-and-match set.
6. `LOCAL-LINEAGE-CLASSIFIED` — pre-compromise, affected-window and post-containment local records classified.
7. `REMOTE-AUTHORITY-RESTORED` — allowed remote capabilities re-enabled under current policy.
8. `RECONCILIATION-PENDING` or `NORMALIZED` — affected records resolved or residuals remain explicit.

Do not collapse steps 3–7 into a generic `online` state.

## 9. Recovery packages need anti-replay and context binding

An offline/portable recovery package can be useful when ordinary online trust is suspect, but its validity must bind to the intended product/lineage, successor trust context, policy epoch/range and any expiry/revocation semantics. Package integrity alone does not prove it is the newest acceptable recovery package.

Guards:
- `recovery package authentic ≠ recovery package current`;
- `recovery package current ≠ imported local records authorized`;
- `package from support channel ≠ cryptographically authenticated recovery authority`;
- `QR/file/manual transfer ≠ out-of-band trust by itself`.

## 10. Reinstall, storage loss and device replacement are distinct rebootstrap cases

If the browser's local anti-rollback floor is lost, the client cannot pretend it remembers the strongest previously accepted state. Recovery must use an independently authenticated bootstrap source or explicitly enter an `UNKNOWN/REENTRY-REQUIRED` state.

This is especially important for PWA/EFB because browser storage durability and managed-device policies remain product evidence questions.

Guards:
- `no local floor found ≠ floor was zero`;
- `new device ≠ clean trust history automatically`;
- `same account login ≠ same prior device trust state recovered`;
- `cloud backup restored ≠ trust metadata freshness independently established`.

## 11. Trust-policy publication must be atomic enough for its claims

A successor root/verifier, revocation set, minimum client/API generation and compatibility policy may be stored in different objects/systems. A client must not observe a combination that never constituted an accepted policy state.

TUF's snapshot/timestamp binding is a mature reference pattern against mix-and-match. Software Engineering D006 independently supplies bounded evidence that durable progress markers must not outrun semantic effects.

**DEPENDENCY:** Software Engineering owns the eventual transactional/publication implementation. Web Manager requires a verifiable policy snapshot/receipt boundary.

Guards:
- `root updated ≠ revocation policy updated`;
- `policy cursor advanced ≠ all required policy effects durable`;
- `objects individually authentic ≠ combined state authorized`;
- `server reports epoch N ≠ client safely persisted epoch N`.

## 12. UX boundary

Track B should communicate consequence and available action, not cryptographic internals. Candidate states:
- local records remain available; online synchronization is blocked until security information is updated;
- security information could not be verified; retry when a trusted connection/recovery path is available;
- current trust is restored, but records from an affected period still require review;
- this device's previous trust state is unavailable, so re-entry verification is required.

Never claim “secure”, “synced” or “up to date” solely because connectivity returned.

Design Studio Web remains Stage 3 PRACTICE / NOT PASSED (W089 at run start). Persistence/offline/Sync, Safari/Firefox, screen reader, physical-device/layout/IME and human UX evidence remain OPEN.

## 13. Track D measurement boundary

Telemetry may record observed application/worker/trust-policy generations and re-entry outcomes subject to privacy minimization. It cannot prove:
- total fleet denominator;
- authenticity of a client's local state;
- that all offline devices received revocation;
- compromise start time;
- absence of replay/fork merely because no error was observed.

Guards:
- `100% of observed online clients updated ≠ 100% of fleet updated`;
- `no rollback telemetry ≠ rollback impossible`;
- `analytics event says re-entry success ≠ security oracle passed`.

## 14. Destructive validation campaign

Track C handoff:
1. valid current successor policy → accept under declared recovery chain;
2. compromised old root signs attacker successor → reject;
3. stale but valid pre-compromise policy replay → reject rollback/freeze as applicable;
4. higher version signed by unauthorized successor → reject;
5. root current but revocation set stale → reject inconsistent policy snapshot;
6. revocation current but compatibility floor stale → reject inconsistent state;
7. stale Service Worker serves old policy → worker/cache cannot lower floor;
8. new Service Worker with old Cache Storage → stale cache cannot choose trust;
9. device clock rolled back → version/other evidence still prevents rollback;
10. device clock far forward → expiry failure does not trigger unsafe fallback;
11. network attacker blocks all current policy → fail closed for remote mutation, preserve safe local data;
12. recovery package authentic but superseded → reject as current bootstrap;
13. recovery package for wrong product/lineage → reject;
14. recovery package imported twice → idempotent outcome;
15. recovery interrupted after successor auth before floor persistence → no false success;
16. floor persisted before required policy objects → recovery atomicity failure detected;
17. backup restores old floor → current independent source prevents rollback;
18. local floor missing after storage deletion → `UNKNOWN/REENTRY-REQUIRED`, not epoch zero;
19. reinstall with stale CDN/service-worker path → no implicit reset;
20. new device with same account → no device-lineage inference;
21. old export imported after re-entry → historical admission separated from current authority;
22. affected-window local operation → preserve/quarantine, no auto-publish;
23. old API accepts retired epoch → server/current policy rejects;
24. client offline across multiple trust epochs → sequential/direct transition policy validated explicitly;
25. two mirrors provide inconsistent signed metadata → consistency oracle rejects invalid combination;
26. server ACK lost after trust-floor commit → retry idempotent;
27. accessibility: blocked/re-entry/review states are programmatically and visually distinguishable;
28. restart after partial re-entry → state remains truthful;
29. telemetry misses offline client → no fleet-complete claim;
30. physical managed Safari/iPadOS offline→compromise→re-entry→reconciliation remains mandatory before product PASS.

## 15. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W089; Stage 3 PRACTICE / NOT PASSED**. No persistence/offline/Sync, Safari/Firefox, screen-reader, physical-device or human UX PASS transfers.

Software Engineering Studio Data `progress/DATA_STATUS.md` checked 2026-09-19: **Stage 1 IN STUDY / NOT YET PASSED**. D005/D006 provide bounded durability/cursor/ambiguous-ACK evidence only. Actual LogMate Flutter/mobile persistence, key storage, policy publication and re-entry implementation remain OPEN.

## 16. MINTTAP DIRECTION

For any future consequence-bearing PWA trust design:
- define a minimum accepted trust/policy floor that stale runtime/cache/import state cannot silently lower;
- authenticate successor trust through a recovery path independent enough for the compromise model;
- bind root/verifier/revocation/compatibility state into a coherent accepted policy snapshot;
- treat Service Worker and Cache Storage as transport/runtime state, not freshness/trust authorities;
- preserve irreplaceable local data while blocking remote authority when re-entry cannot be authenticated;
- make loss of local trust-floor state explicit rather than assuming a clean bootstrap;
- validate offline-through-compromise and multi-epoch re-entry on physical target devices.

Do not adopt TUF wholesale merely because its threat model is instructive. Select mechanisms only after actual product consequence, key hierarchy, storage, backend and managed-device constraints are known.

## 17. CHANGE WATCH / OPEN

- TUF latest checked as v1.0.36, modified 2026-08-05; monitor specification evolution.
- Service Worker specification/browser behavior remains platform-sensitive; physical Safari/WebKit validation is required.
- Actual managed-iPad MDM/storage deletion/reinstall behavior is OPEN.
- Actual trust metadata format, key hierarchy, recovery authority, local durable floor, backend publication transaction, account/device model and LogMate synchronization architecture are OPEN.
- Legal/safety requirements for aviation records are outside this generic security gate.

## 18. Gate assessment

**PASS (generic).** The coordinator can now distinguish successor creation from authenticated distribution, policy authenticity from freshness, monotonic trust floor from browser cache/runtime state, and safe local preservation from current remote authority. TUF provides a strong transfer reference for rollback/freeze/mix-and-match defenses without being promoted to a product mandate.

Product/device/runtime validation remains OPEN.

## Next highest-value adjacent target

**PWA trust-floor persistence, reset authorization & device-loss recovery without rollback loopholes.** The next bottleneck is what happens when the only local monotonic floor is deleted, evicted, restored from an old backup, or absent on a replacement device: define reset authorization, independent evidence and recovery semantics without converting “lost local state” into an attacker-controlled downgrade path.