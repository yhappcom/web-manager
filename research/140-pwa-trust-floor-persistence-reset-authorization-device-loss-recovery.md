# 140 — PWA Trust-Floor Persistence, Reset Authorization & Device-Loss Recovery

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + ACCOUNT/DEVICE + RESET-AUTHORITY + PHYSICAL-DEVICE VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 099–102 trusted-state reset/rebootstrap; 135–139 provenance/crypto/compromise/re-entry; Track A browser storage semantics; Track B recovery UX; Track C destructive reset/restore validation; Software Engineering owns implementation.

## Purpose

139 established that a long-offline client needs an authenticated trust transition and a minimum accepted trust floor; loss of that floor must not silently become epoch zero. The adjacent problem is recovery when the floor itself is absent, stale, restored from backup, or unavailable on a replacement device.

Central rule:

> **Loss of local monotonic state is evidence loss, not rollback authorization. Recovery must re-establish a trustworthy lower bound from evidence independent enough for the threat model before consequence-bearing remote authority is restored.**

This study does not prescribe TUF, Secure Enclave/TPM, passkeys, MDM, a cloud account, a particular backend, or a LogMate implementation.

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** owns what origin storage, persistence requests, browser clearing, WebKit storage policy and PWA isolation can actually guarantee. Browser storage can hold a floor but cannot be assumed to be a device-lifetime anti-rollback root.
- **B UX/IA/Content — elevated consumer:** owns truthful `local data preserved`, `previous trust state unavailable`, `security re-verification required`, `recovery source rejected`, `review required`, and replacement-device states.
- **C Quality — high dependency pressure:** owns deletion/eviction/reinstall/old-backup/new-device/interrupted-reset/cross-browser/physical-iPad matrices.
- **D Search/Analytics — constrained consumer:** recovery telemetry may measure observed paths and failure rates but cannot reconstruct missing trust state or authenticate reset authority.
- **E Architecture/Security/Operations — highest-risk owner:** owns floor semantics, reset authority, recovery evidence independence, anti-rollback, account/device boundaries, and recovery incident governance.

Allocation remains E-heavy because a weak reset path can nullify all earlier anti-rollback work.

## 2. SOURCE — Web storage persistence reduces eviction risk; it is not an immutable trust anchor

The WHATWG Storage Living Standard, last updated 15 March 2026 when checked, defines local storage buckets as initially `best-effort` and provides `persist()` / `persisted()` for persistent storage. It explains that persistent buckets are protected from user-agent storage-pressure clearing without user consent, while the platform still exposes storage as user-agent-managed state. IndexedDB, Cache API and Service Worker registrations are storage endpoints in this model.

Source checked 2026-09-19: https://storage.spec.whatwg.org/

WebKit's storage-policy documentation states that browser storage can be evicted under storage pressure in best-effort mode, and that Safari/WebKit support persistent storage requests. Home Screen Web Apps have storage-policy behavior distinct from ordinary Safari browsing; their first-party domain is explicitly exempt from ITP's seven-day script-writable-storage cap, but this does not make their state an immutable device root.

Sources checked 2026-09-19:
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://webkit.org/tracking-prevention/

**SYNTHESIS:** persistence is a storage-retention property, not proof of continuity after user deletion, app/site-data clearing, reinstall/reprovisioning, backup restoration, origin change, or device loss.

Guards:
- `persisted() == true ≠ trust floor cannot be deleted`;
- `Home Screen PWA storage ≠ hardware monotonic storage`;
- `eviction-resistant ≠ rollback-resistant`;
- `origin storage available ≠ previous device trust state present`;
- `storage API success ≠ device-lifetime continuity proven`.

**CHANGE WATCH:** current WebKit storage behavior is implementation-specific and can evolve. Physical target-device evidence remains mandatory.

## 3. SOURCE — mature recovery guidance rejects unauthorized rollback

NIST SP 800-193 is firmware-focused, so it is transfer evidence rather than a PWA requirement. It nevertheless supplies a useful recovery principle: recovery should protect against unauthorized recovery to an earlier version containing a security weakness, and administrator-forced recovery should be authorized. It also recognizes trusted known-good recovery data and multi-stage recovery.

Source checked 2026-09-19: https://doi.org/10.6028/NIST.SP.800-193

**TRANSFER VALIDATION:** a recovery mechanism is not safe merely because it restores availability. The reset path itself needs authority and an anti-rollback policy.

Guards:
- `recovery succeeded ≠ recovery target authorized`;
- `factory/reset state available ≠ oldest trust state acceptable`;
- `administrator/user requested reset ≠ security floor may be arbitrarily lowered`;
- `recovery credential valid ≠ requested rollback legitimate`.

## 4. SOURCE — secure-update continuity assumes retained trusted state; missing state is a different bootstrap problem

The current TUF client workflow loads a trusted root assumed to have arrived out-of-band, then updates roots sequentially. Each successor root must be signed by the predecessor's threshold and its own threshold, version N+1 must follow N, and trusted root metadata is persisted to non-volatile storage. TUF also rejects rollback in timestamp/snapshot metadata and binds snapshot state to verified timestamp state.

Source checked 2026-09-19: https://theupdateframework.github.io/specification/latest/

**SYNTHESIS:** normal monotonic update and state-loss recovery are different security problems. If the previously trusted root/floor is gone, the ordinary predecessor-chain check has lost its local starting evidence. Pretending that this is a first-ever install silently converts state loss into a downgrade/bootstrap path.

Guards:
- `trusted metadata missing ≠ first install proven`;
- `fresh installation bits ≠ fresh trust bootstrap`;
- `server offers root N ≠ root N is a valid bootstrap root`;
- `same origin serves recovery metadata ≠ independent reset authority`.

## 5. Define the floor as a lower-bound claim, not a cache entry

The minimum accepted trust floor is the strongest lower-bound claim the client has accepted for consequence-bearing authority. Exact fields are product-dependent; possible dimensions include:
- trust/root/verifier epoch;
- revocation or containment epoch;
- minimum client/API generation;
- accepted lineage/checkpoint;
- compatibility/security-policy epoch;
- recovery-authority generation.

The floor is not necessarily one integer and should not be conflated with cached metadata content. A client can possess metadata newer than its durably accepted floor after an interrupted update, or an old backup can contain internally consistent metadata that is below the current floor.

Guards:
- `metadata version ≠ complete trust floor`;
- `cache newest object ≠ durable accepted lower bound`;
- `floor persisted ≠ all associated policy effects persisted`;
- `one monotonic counter ≠ every security dimension monotonic`.

## 6. Reset is an authorization event, not deletion handling

A reset that permits the client to accept trust state below its prior lower bound changes security authority. It therefore needs an explicit reset/rebootstrap policy rather than being triggered by `IndexedDB missing`, cache clear, reinstall, or a support instruction.

Generic reset evidence may come from one or more independent-enough sources, depending on the threat model:
- a currently trusted server/account recovery path authenticated under successor trust;
- a separately protected recovery credential or package;
- an organizational/administrator recovery authority;
- an independently retained checkpoint/receipt;
- managed-device evidence where actual MDM capabilities support the claim;
- user-mediated recovery with authenticated, context-bound evidence.

No single mechanism is mandated. The security question is whether the recovery evidence remains trustworthy under the failure/compromise that destroyed or invalidated the local floor.

Guards:
- `local state missing ≠ reset authorized`;
- `user can delete site data ≠ user intended security downgrade`;
- `support agent says reset ≠ reset cryptographically/operationally authorized`;
- `same account authenticated ≠ old device floor reconstructed`;
- `new device enrolled ≠ old device history inherited automatically`.

## 7. Reset authority must be scoped and independently survivable

The reset authority is itself high consequence. If ordinary origin compromise, ordinary account takeover, or the same compromised signing root can both erase the remembered floor and authorize a lower replacement, anti-rollback collapses.

A useful threat-model test is:
1. What event caused floor loss?
2. Which authority approves rebootstrap?
3. Could the same attacker/failure control both?
4. What minimum state may the recovery authority establish?
5. Can it authorize arbitrary historical epochs, or only a current recovery epoch?
6. Is the recovery action auditable and revocable?

**MINTTAP DIRECTION:** prefer recovery authority that establishes a current or bounded-safe trust state, not a general-purpose permission to choose any old epoch.

Guards:
- `reset authority exists ≠ arbitrary rollback authority exists`;
- `recovery credential powerful enough to restore ≠ should be powerful enough to downgrade`;
- `independent label/vendor ≠ independent failure domain`;
- `recovery package decrypts ≠ recovery policy authorizes its epoch`.

## 8. New device and lost device are not equivalent to clean first install

A genuinely first-ever user/device bootstrap, a replacement device for an existing account, and a wiped/reinstalled former device have different available evidence.

Generic classification:
- `FIRST-BOOTSTRAP` — no prior account/device lineage is claimed; use the product's current bootstrap trust path.
- `KNOWN-ACCOUNT / NEW-DEVICE` — account continuity may be known, but prior device-local floor is not automatically inherited.
- `KNOWN-DEVICE / FLOOR-MISSING` — prior device identity/lineage is known but local floor evidence is missing; treat as recovery, not first install.
- `BACKUP-RESTORED / FLOOR-STALE-OR-UNKNOWN` — restored state may be older than server/current trust and must pass anti-rollback/re-entry checks.
- `DEVICE-LOSS / REPLACEMENT` — old device authority may need containment/revocation separately from new-device bootstrap.

Guards:
- `same user ≠ same device`;
- `same device name ≠ same device identity`;
- `backup restored ≠ security state current`;
- `replacement device trusted ≠ lost device revoked`;
- `lost device revoked ≠ local unsynced data recovered`.

## 9. Account recovery and trust-floor recovery are related but distinct

NIST SP 800-63B's current authenticator guidance distinguishes device-bound and syncable authenticators and treats recovery/event management as explicit security processes. This is identity-system evidence, not a prescription for MintTap.

Sources checked 2026-09-19:
- https://pages.nist.gov/800-63-4/sp800-63b/syncable/
- https://pages.nist.gov/800-63-4/sp800-63b/events/

**SYNTHESIS:** authenticating the human/account can authorize participation in a recovery workflow, but it does not by itself prove the strongest trust epoch the lost device had accepted. Conversely, a valid recovery package can establish system trust context without proving the current human is authorized to mutate a specific account.

Guards:
- `account recovery PASS ≠ trust-floor recovery PASS`;
- `trust-floor recovery PASS ≠ account authorization PASS`;
- `syncable authenticator available ≠ authenticator was synced`;
- `device-bound credential absent ≠ old device lineage never existed`.

## 10. Backup restore needs anti-rollback reconciliation

A backup can restore irreplaceable local data and still contain stale trust metadata. Data recovery and authority recovery therefore need separate acceptance paths.

Generic restore sequence:
1. restore bytes into a quarantined/local-preserved state;
2. identify any embedded trust-floor/recovery metadata and its provenance;
3. obtain current independently authenticated trust/revocation state;
4. compare restored floor against current minimum accepted policy;
5. never let restored state lower a stronger floor already known elsewhere;
6. classify restored operations/records under current reconciliation rules;
7. restore remote mutation only after current account + trust + policy requirements pass.

Guards:
- `backup authentic ≠ backup current`;
- `backup newest available ≠ backup above current trust floor`;
- `restore completed ≠ remote authority restored`;
- `old local record valuable ≠ old embedded credential remains authorized`.

## 11. Persisting a floor and publishing a floor must fail safely

If acceptance of epoch N and persistence of the local floor are separate operations, interruption can produce dangerous ambiguity. A client must not report re-entry success while only volatile state knows N and durable state still permits N-1 after restart.

Generic states:
- `CANDIDATE-VERIFIED`;
- `FLOOR-PERSIST-PENDING`;
- `FLOOR-DURABLE`;
- `POLICY-EFFECTS-VERIFIED`;
- `REMOTE-AUTHORITY-RESTORED`.

On restart after ambiguity, prefer re-verification over assuming the strongest volatile state survived.

Guards:
- `candidate verified ≠ floor durable`;
- `floor durable ≠ policy effects complete`;
- `UI said success ≠ restart state proves success`;
- `ACK missing ≠ floor write missing`.

Software Engineering owns eventual transactional/idempotent implementation. Web Manager requires the semantic states and failure behavior.

## 12. Local preservation during reset/rebootstrap failure

Failure to reconstruct current trust must not destroy irreplaceable offline records. Preserve local data, provenance and export where product semantics permit, while consequence-bearing remote mutation remains blocked.

Possible generic state: `LOCAL-PRESERVED / TRUST-FLOOR-UNKNOWN / REMOTE-WRITE-BLOCKED`.

This is especially relevant to the EFB/LogMate-like scenario: a company iPad may contain unsynced flight records even when its browser trust state is unavailable. The correct generic response is neither silent downgrade nor destructive reset.

Guards:
- `trust state unrecoverable now ≠ local data disposable`;
- `local data preserved ≠ local data currently authoritative remotely`;
- `export available ≠ recovery complete`;
- `security rebootstrap blocked ≠ invent synchronization success`.

## 13. UX boundary

Track B should communicate consequence and next safe action rather than exposing cryptographic jargon. Required distinctions include:
- previous security state is unavailable; local records remain on this device;
- online synchronization is blocked until security information is re-verified;
- restored backup contains usable local data but security state must be updated before synchronization;
- this replacement device has been verified, but records from another device may still require reconciliation;
- recovery information is valid but too old / not valid for this account or product;
- recovery failed without deleting local data.

Never present `reinstalled`, `restored`, `signed in`, or `online` as synonyms for `security state current`.

Design Studio Web at run start is **W090 / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, Safari/Firefox, screen reader, physical-device/input and human UX remain OPEN; no UX PASS transfers.

## 14. Track D measurement boundary

Privacy-minimized telemetry may measure:
- fraction of observed clients with missing/old/current floor states;
- reset path selected;
- recovery success/failure class;
- time spent remote-write-blocked;
- observed device replacement/reinstall cohorts.

It cannot prove:
- why local state disappeared;
- that an apparent new device is genuinely new;
- that every lost device is revoked;
- authenticity of recovery evidence;
- completeness of the offline fleet.

Guards:
- `telemetry says floor missing ≠ eviction caused it`;
- `new installation event ≠ first-ever bootstrap`;
- `no stale-floor event observed ≠ no stale device exists`.

## 15. Destructive validation campaign

Track C handoff:
1. best-effort storage evicted → floor absence enters recovery, not epoch zero;
2. persistent storage granted → still test user clearing/reinstall/device replacement;
3. site data manually cleared → no silent downgrade;
4. PWA removed/re-added → no assumption of prior floor continuity;
5. old backup restores N-3 while server requires N → reject rollback, preserve local data;
6. backup restores N+valid local records but revoked credential → data admitted separately from authority;
7. new device same account → account auth does not fabricate prior device floor;
8. known old device floor missing → recovery path, not first bootstrap;
9. attacker deletes local floor then replays old signed metadata → reject unless independent bootstrap authorizes;
10. ordinary account takeover attempts floor reset → reset-authority policy enforced;
11. compromised old root issues reset package → reject under successor recovery policy;
12. valid recovery package for wrong product/lineage → reject;
13. valid but superseded recovery package → reject as current reset evidence;
14. recovery package imported twice → idempotent;
15. reset interrupted before floor persistence → no success claim;
16. floor persisted but required policy effects absent → remote authority remains blocked;
17. crash immediately after floor persistence → restart revalidates coherent state;
18. server ACK lost after accepted reset → retry does not lower/duplicate state;
19. device clock rollback/forward → no clock-only reset authorization;
20. stale Service Worker serves reset UI/metadata → worker cannot lower floor;
21. Cache Storage contains old bootstrap root → cache cannot choose reset trust;
22. restored browser profile contains old floor → current independent state prevents rollback;
23. replacement device verified while lost device still active → old-device containment remains separate;
24. lost device later reconnects → current revocation/re-entry policy applies;
25. local unsynced records survive failed reset → read/export remain truthful;
26. recovery source unavailable → fail closed for remote mutation without deleting data;
27. accessibility: recovery-required/blocked/restored/review states distinguishable programmatically and visually;
28. Safari/WebKit storage clearing and Home Screen removal/re-add tested physically;
29. managed-iPad MDM wipe/reprovision/backup behavior tested against actual policy;
30. full offline→floor-loss→replacement/restore→rebootstrap→reconciliation drill required before product PASS.

## 16. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W090 SERVED POINTER-REORDER TRANSFER CLOSURE; Stage 3 PRACTICE / NOT PASSED**. It explicitly keeps persistence/offline/sync dormant until implemented and keeps Safari/Firefox, screen-reader, physical-device and human UX evidence OPEN.

Software Engineering implementation evidence remains a dependency rather than being duplicated here. Actual LogMate persistence/sync, key storage, account/device identity, backup format, reset token/package, MDM integration and server-side minimum epoch enforcement remain OPEN.

## 17. MINTTAP DIRECTION

For a future consequence-bearing PWA:
- treat browser-local floor as useful state but not an immutable device root;
- distinguish first bootstrap, known-account/new-device, known-device/floor-missing, backup restore and device-loss cases;
- never map missing state to epoch zero;
- define reset/rebootstrap as an explicit high-consequence authorization event;
- ensure reset evidence is independent enough from the failure/compromise that caused floor loss;
- prefer reset authority that establishes a bounded current-safe state rather than arbitrary rollback power;
- separate account authentication, device lineage, trust-floor recovery, data restore and remote mutation authorization;
- quarantine/restage stale backup trust metadata while preserving irreplaceable user records;
- persist accepted floor before claiming restored remote authority;
- validate clearing, removal/re-add, backup restore, replacement and managed-device behavior on physical target devices.

## 18. OPEN / CHANGE WATCH

- Exact MintTap/LogMate trust-floor fields and storage location: OPEN.
- Whether a server-side/account-bound floor, device-bound protected state, MDM-managed state, recovery package, or combination is appropriate: OPEN pending threat model and implementation evidence.
- Safari/iPadOS/Home Screen storage behavior after user deletion, device backup/restore, app removal/re-add and MDM reprovisioning: OPEN and requires current physical-device testing.
- Account/device identity model and lost-device revocation: OPEN.
- Recovery authority custody, independence, audit and abuse controls: OPEN.
- Legal/aviation requirements for recovery/audit/record retention: OPEN.
- WHATWG/WebKit storage behavior: CHANGE WATCH.
- TUF is reference architecture only, not an implementation decision.

## 19. Gate assessment

**PASS (generic).** The coordinator can now distinguish storage persistence from anti-rollback durability, state loss from reset authorization, first bootstrap from known-device recovery, account recovery from trust-floor recovery, backup restoration from authority restoration, and local data preservation from remote mutation authority.

Product/device/runtime validation remains OPEN.

## Next highest-value adjacent target

**PWA recovery-authority abuse resistance, quorum/independence & emergency reset governance.** Once reset is recognized as a high-consequence authority, the next bottleneck is preventing a single compromised support/admin/account channel from abusing it: define separation of duties, threshold/quorum where consequence warrants it, break-glass constraints, replay/idempotency, recovery-event provenance and emergency lifecycle without building unnecessary enterprise ceremony for a small app company.