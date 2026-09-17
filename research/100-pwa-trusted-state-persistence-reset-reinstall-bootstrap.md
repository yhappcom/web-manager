# 100 — PWA Trusted-State Persistence, Reset/Reinstall Bootstrap & Recovery

Status: **PASS (generic) / PRODUCT STORAGE + BOOTSTRAP + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A storage/origin/browser mechanics; 085 recovery, 091 long-offline coexistence, 094 key lifecycle, 098 stale-client revocation, 099 trust-policy authenticity.

## Purpose

099 established that signed trust policy requires an authenticated authority, semantic context, freshness and anti-rollback state. This study asks the next failure question: **what happens when the client loses the local state that remembered what it previously trusted?**

This is especially important for a long-offline EFB-like PWA. A client may lose origin storage through browser/user clearing, storage pressure where persistence was not granted, device replacement, profile/reset behavior, application removal/reinstallation semantics, or other platform lifecycle events. A fresh-looking client can therefore coexist with user records restored from backup, server state from a newer generation, or an old offline artifact.

The study deliberately separates **security trust-state recovery** from **user-record backup/restore**. The two may interact, but neither proves the other.

---

## 1. Track allocation and bottleneck decision

### Track comparison

- **A Platform/Browser — strong dependency supplier.** The key prerequisite is origin storage semantics: default best-effort storage, persistent mode, origin-wide eviction behavior and Safari/WebKit policy. Exact managed-iPad reset/reinstall behavior remains execution evidence, not a generic conclusion.
- **B UX/IA/Content — consumer.** Must distinguish `security state must be re-established` from `your records are lost/corrupt` and expose safe recovery/export states without telling users to erase storage reflexively.
- **C Performance/Accessibility/Quality — validation owner.** Must exercise reset, partial restore, old backup, stale trust state, missing trust state and contradictory server/client state across target engines/devices.
- **D Search/Discovery/Analytics — low direct pressure.** Public discovery/config/analytics state must not become an implicit security bootstrap authority.
- **E Architecture/Security/Operations — highest-value bottleneck.** Owns bootstrap trust, anti-rollback continuity, recovery authority, reset containment and operational runbooks.

**Allocation:** most work remains in E with A supplying standards/platform facts and B/C consuming the resulting state model. No equal-work rotation is justified.

---

## 2. SOURCE — Web storage persistence is useful, but it is not a security root

### WHATWG Storage Standard

The WHATWG Storage Living Standard (last updated 2026-03-15 when checked) defines storage buckets, persistence and quota. Best-effort storage may be cleared under storage pressure. A persistent bucket requires the `persistent-storage` permission and cannot be cleared by the user agent without involvement from the origin or user. When a bucket is cleared, the standard says it is cleared in its entirety.

Source: https://storage.spec.whatwg.org/

### MDN StorageManager

`navigator.storage.persist()` requests persistent storage and resolves to whether persistence was granted. `persisted()` reports whether the current storage bucket is persistent. Browser policy may approve or deny persistence according to browser-specific rules. `estimate()` provides approximate usage/quota, not an exact durability guarantee.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persisted
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria

### WebKit storage policy

WebKit documents that Safari 17 / iOS 17 / iPadOS 17 and later support the Storage API, including persistent mode. WebKit normally evicts website data on an origin basis under relevant pressure/policy conditions. It also documents that Home Screen web-app first-party domains are exempt from ITP's seven-day script-writable-storage cap; this exemption is **not** a guarantee against explicit user deletion, device loss, implementation defects, or every other reset mechanism.

Sources:
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://webkit.org/tracking-prevention/

### Apple user-controlled deletion

Apple documents user controls that remove Safari website data. This proves an important operational boundary: web storage can be deliberately removed by the user/platform UI. It does **not** by itself establish the exact relationship between every Safari clearing action and a particular installed Home Screen PWA on every iOS/iPadOS version; that remains target-device validation.

Source: https://support.apple.com/en-ae/105082

### SYNTHESIS

`persisted() === true` is a storage-retention property, not a cryptographic continuity proof. A security design must still define what happens after explicit clearing, profile/device replacement, corruption, application lifecycle changes or a new device with no prior local anti-rollback memory.

**Guard:** `persistent storage granted ≠ trust state can never disappear`.

---

## 3. The state classes that must not be collapsed

A reset/recovery design should distinguish at least:

1. **Reconstructible runtime state** — shell assets, caches, downloaded projections.
2. **Authoritative local user data** — records not safely reconstructible elsewhere.
3. **Durable outbox / pending operations** — accepted locally but not remotely acknowledged.
4. **Authentication/session state** — cookies/tokens/session bindings.
5. **Cryptographic application state** — DEKs/KEKs/wrapped-key metadata where applicable.
6. **Security trust state** — trusted root/key identifiers, accepted policy generation, anti-rollback/freeze metadata, protocol/bridge trust generation.
7. **Recovery metadata** — backup version, restore provenance, device identity/pairing state, reconciliation checkpoint.
8. **Diagnostics** — enough evidence to distinguish reset, migration failure, corruption and policy rejection without containing unnecessary sensitive records.

A single origin bucket may physically contain several of these classes, but physical co-location does not make their semantics identical.

**Guard:** `same origin bucket ≠ same data authority ≠ same recovery policy`.

---

## 4. Reset taxonomy

### 4.1 UA storage-pressure eviction

If best-effort origin storage is evicted, application data and local trust metadata can disappear together. The client can return looking like a first install even though the server has historical state and external backups may exist.

Persistent storage materially reduces this class of automatic eviction when granted, but it is not a backup and does not solve explicit deletion/device loss.

### 4.2 Explicit user/site-data clearing

User-controlled clearing can intentionally remove website data. Previous studies already rejected `Clear-Site-Data: "storage"` as a generic troubleshooting/logout mechanism for offline-authoritative applications. The same principle applies here: clearing origin state can destroy both user records and the security memory used to reject stale trust policy.

**Guard:** `storage reset ≠ benign cache reset`.

### 4.3 Application removal/reinstallation

Generic Web standards do not provide a universal contract saying that removing/re-adding an installed PWA preserves or deletes every origin data class identically across platforms. Exact Safari/Home Screen behavior on the company's managed iPad fleet is therefore **OPEN** and requires controlled device execution.

**CONTRADICTION prevented:** do not infer native-app uninstall semantics for a PWA merely because it has an icon and standalone display mode.

### 4.4 New device / replacement device

A new device has no prior local anti-rollback state unless that state is restored or independently re-established. Account recovery, passkey recovery or successful login does not automatically restore application trust roots/generations, local records, DEKs or outbox state.

**Guard:** `new device authenticated ≠ previous trusted-state continuity restored`.

### 4.5 Backup restore / selective restore

A backup can contain user records without current trust metadata, trust metadata without current user records, or both from different points in time. Therefore a restore is a **state composition event**, not a simple time reversal.

**Guard:** `backup restored ≠ trust state restored ≠ restored trust state current`.

---

## 5. Anti-rollback memory is itself security-sensitive state

Suppose a client previously accepted trust-policy generation 42. If local memory of `42` disappears and bootstrap simply accepts any validly signed policy, an attacker able to replay an older still-validly-signed generation may turn a local reset into an anti-rollback bypass.

But persisting `42` only in the same resettable origin bucket does not solve reset recovery. The problem becomes:

`trust policy authenticity + freshness + prior accepted state + recovery authority`.

A robust design therefore needs an explicit answer for a client with **no trusted local memory**. Possible architectural families include server-assisted rebootstrap, independently anchored trust material, device/platform management, recovery packages, or other security architecture. This study does **not** choose one for MintTap/LogMate because the exact product threat model and implementation evidence are not available.

### Important distinction

A client with no trust state is not equivalent to a client that positively knows generation 0.

**Guard:** `trust state missing ≠ lowest generation trusted`.

Missing state should be modeled as **unknown bootstrap state**, not silently normalized into a version number.

---

## 6. Bootstrap modes

A useful operational model separates four modes.

### Mode A — continuity bootstrap

The client retains previously trusted root/generation metadata and can validate a successor according to the established transition rules.

This is the strongest ordinary continuity case.

### Mode B — fresh-device bootstrap

The client has no prior application trust state and must establish initial authority from a product-defined bootstrap root/process. This is not anti-rollback continuity because there is no prior local generation to compare.

### Mode C — reset/recovery bootstrap

The client previously existed but its trust state is missing or cannot be proven continuous. Treating it as an ordinary fresh install can erase evidence that a rollback boundary was lost. The system may need server/account/device/recovery evidence before enabling sensitive bridges.

### Mode D — restored-state bootstrap

A backup supplies trust metadata and/or user data. The system must establish the backup's provenance/version and compare restored trust state against currently authorized trust before replay/sync.

**MINTTAP DIRECTION:** keep these states distinguishable in architecture and diagnostics. Do not collapse all four into `firstRun=true`.

---

## 7. Data-preserving containment when trust state is missing

For an offline-authoritative EFB-like PWA, missing trust metadata should not automatically delete local records. The safer generic response is capability minimization:

- preserve authoritative local records;
- preserve durable pending outbox;
- allow only locally safe operations whose authorization model permits them;
- block or pause security-sensitive remote replay/bridge operations that require current trust;
- expose export/recovery where policy permits;
- re-establish trust before replay;
- reconcile after authority is restored.

This extends 098/099.

**Guards:**
- `trust state missing ≠ user records untrusted`;
- `anti-rollback memory lost ≠ local record should be deleted`;
- `rebootstrap required ≠ destructive reset required`.

Whether local read/write remains allowed is product policy and threat-model dependent; no universal decision is asserted here.

---

## 8. Backup/restore composition matrix

At minimum, implementation validation should cover:

| User records | Trust metadata | Outbox | Meaning |
|---|---|---|---|
| absent | absent | absent | genuine fresh/reset-like state; must establish bootstrap authority |
| present | absent | present/absent | data exists but anti-rollback continuity is unknown; preserve data, constrain unsafe bridges |
| absent | present | absent | trust memory exists without user data; do not infer user-data recovery |
| present | present, same backup epoch | present | candidate coherent restore; still compare to current authority/schema/protocol |
| present | present, older epoch | present | rollback/replay risk; current authority must decide compatibility |
| newer records | older trust state | pending | high-risk mixed restore; block blind replay |
| older records | newer trust state | absent | data rollback risk distinct from security-policy rollback |

This matrix should be expanded with encryption-key availability and schema/protocol generations in Software Engineering implementation work.

---

## 9. Persistence request timing and UX

The Storage Standard and browser implementations permit a site to request persistent storage. For an app whose locally created records may be irreplaceable, requesting persistence can be appropriate after the user establishes meaningful use/data rather than treating storage durability as an invisible assumption.

However:

- `persist()` can return false;
- browser policy differs;
- persistence is not backup;
- persistence does not protect against explicit user deletion/device loss;
- a UI that says `Your records are safe` solely because persistence was granted would overclaim.

### B dependency

User-facing state should communicate concrete facts, e.g. whether records are local, whether a backup exists, whether sync is acknowledged, whether storage persistence is granted, and whether trust must be re-established. Content Design/Design Studio should own final wording/interaction validation.

---

## 10. Safari / Home Screen PWA boundary

Current WebKit documentation provides two useful generic facts:

1. Home Screen web-app first-party domains are exempt from ITP's seven-day script-writable-storage cap.
2. Safari 17 / iOS/iPadOS 17-era WebKit supports StorageManager persistence and documents standalone web apps as having comparable origin quota behavior.

These facts remove one common misconception: **the seven-day ITP rule should not be generalized into “installed iPad PWA data is always deleted after seven days.”**

They do not prove:

- exact managed-EFB retention under the company's MDM configuration;
- behavior after Home Screen removal/re-add;
- behavior after OS upgrade/profile migration;
- interaction with Safari website-data clearing in every version;
- storage behavior under extreme device pressure;
- backup/restore behavior;
- trust-state durability.

All remain target-device validation.

**CHANGE WATCH:** Safari/WebKit storage policy and managed-device behavior can change and should be rechecked against the actual supported OS fleet.

---

## 11. Cross-repository transfer

### Design Studio

Latest checked Web Design status: Stage 1 PASS, Stage 2 PASS, Stage 3 PRACTICE / NOT PASSED; W051 batch partial-ack reconciliation is ready but execution remains OPEN. Its key transferable principle is that aggregate completion does not prove member-level acknowledgement/atomicity. For this study, a parallel applies: `restore completed` cannot stand in for member-level proof that records, trust metadata, keys and outbox all belong to a coherent recovery epoch.

**TRANSFER VALIDATION:** semantic transfer only; no browser/device runtime PASS is inferred.

### Software Engineering Studio

Latest checked global status remains Foundation IN STUDY. Q003's explicit event-order matrix showed naive retry violating at-most-one logical effect in 12/24 bounded schedules, while stable operation identity + dedup did not in that model. D006 owns replication/sync semantics. This supports a future reset/recovery schedule matrix: reset may occur before/after local acceptance, backup, remote acknowledgement, policy update and replay.

**TRANSFER VALIDATION:** method/state semantics transfer only; it does not prove PWA/browser persistence or production correctness.

---

## 12. Validation contract

### Track A / target browser-device

Execute on exact supported browser/OS/PWA modes:

1. inspect `persisted()` before/after `persist()`;
2. record IndexedDB, Cache Storage, Service Worker registration, local trust metadata and authoritative test records separately;
3. test ordinary close/reopen and reboot;
4. test storage pressure where safely reproducible;
5. test Safari website-data clearing paths;
6. test Home Screen removal/re-add behavior;
7. test OS update/device migration if operationally relevant;
8. verify whether browser and standalone contexts share/isolate the expected storage on exact versions;
9. preserve raw device/version/MDM evidence.

### Track C negative/recovery matrix

Test at least:

- records present + trust metadata missing;
- trust metadata present + records missing;
- old backup + newer server policy;
- newer local records + old restored trust metadata;
- reset after local acceptance but before remote acknowledgement;
- reset after remote acknowledgement but before local acknowledgement persistence;
- key available + DB missing;
- DB available + key missing;
- policy generation lost while offline;
- fresh device authenticates successfully but has no prior trust continuity;
- reinstall/reset followed by stale signed-policy replay;
- invalid/expired/current policy after reset;
- inaccessible network during rebootstrap;
- accessibility of blocked/recovery/export states.

### Security acceptance

Do not claim product PASS until exact architecture answers:

- where anti-rollback/trust state lives;
- what resets it;
- what independently bootstraps authority after loss;
- how compromise recovery differs from ordinary rotation;
- how restored trust state is compared to current authority;
- what operations remain available while trust is unknown;
- how local records/outbox are preserved;
- how diagnostics distinguish fresh install from reset/recovery;
- how backup epochs, schema/protocol and cryptographic key versions compose.

---

## 13. Operational judgment

For ordinary PWA data, origin persistence is a useful browser feature. For an offline-first professional record system, however, **durability, backup, trust continuity and recovery are four different contracts**.

The system should be designed as though any one of them can fail independently:

`local durability`  
`≠ backup availability`  
`≠ trust-policy continuity`  
`≠ cryptographic-key recoverability`  
`≠ remote synchronization correctness`.

A safe recovery architecture therefore does not use “clear site data and sign in again” as a universal reset. That procedure can simultaneously destroy the only local user record and the only local anti-rollback memory while giving the appearance of a clean installation.

---

## 14. MINTTAP / LogMate bounded decisions

### MINTTAP DIRECTION

- Treat trust metadata as explicit security state, not incidental cache.
- Treat missing trust state as `UNKNOWN/REBOOTSTRAP REQUIRED`, not generation zero.
- Keep trust recovery separate from record backup/restore.
- Preserve locally authoritative data during trust recovery unless an explicit product/security requirement says otherwise.
- Use StorageManager persistence where appropriate as a durability layer, never as the backup/recovery claim.
- Require exact target-device tests before making managed-iPad durability/reinstall claims.

### OPEN

- exact MintTap/LogMate origin/storage topology;
- exact IndexedDB/outbox/trust metadata/key stores;
- whether `persist()` is requested and granted on target fleet;
- managed iPad OS/WebKit/MDM versions and policies;
- Home Screen remove/re-add semantics on target fleet;
- backup contents and epoch/version metadata;
- bootstrap/recovery authority after local trust-state loss;
- whether independent trust anchoring is required by the threat model;
- allowed local capabilities while trust continuity is unknown.

No product cryptographic hierarchy is invented here.

---

## 15. New canonical guards

- `persistent storage granted ≠ trust state can never disappear`.
- `same origin bucket ≠ same data authority ≠ same recovery policy`.
- `storage reset ≠ benign cache reset`.
- `PWA installed ≠ native uninstall/reinstall storage semantics`.
- `new device authenticated ≠ previous trusted-state continuity restored`.
- `backup restored ≠ trust state restored ≠ restored trust state current`.
- `trust state missing ≠ lowest generation trusted`.
- `trust state missing ≠ user records untrusted`.
- `anti-rollback memory lost ≠ local record should be deleted`.
- `rebootstrap required ≠ destructive reset required`.
- `restore completed ≠ records/trust/keys/outbox share one coherent recovery epoch`.
- `Home Screen ITP exemption ≠ universal durability guarantee`.
- `local durability ≠ backup availability ≠ trust continuity ≠ key recoverability ≠ sync correctness`.

---

## Gate result

**100 PASS (generic).** The generic prerequisite for trusted-state loss/reset/reinstall bootstrap is sufficiently modeled for implementation handoff. Product validation remains OPEN because the exact application storage layout, trust bootstrap, backup composition, cryptographic architecture, Safari/managed-iPad lifecycle behavior and recovery policy are not yet evidenced.

### Next highest-value adjacent work

Do not continue inventing abstract trust machinery without implementation evidence. If exact project evidence becomes available, consume it first. Otherwise the next adjacent generic question is **recovery provenance and mixed-epoch reconciliation**: how a restored record set, trust metadata, encryption-key generation, schema, protocol generation and outbox checkpoint from different times can be proven coherent—or safely quarantined—before remote replay. This should reuse Software Engineering D003/D005/D006 rather than duplicate database/sync foundations.