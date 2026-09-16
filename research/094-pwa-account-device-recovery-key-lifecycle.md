# 094 — PWA Account/Device Recovery & Cryptographic Key Lifecycle

Status: **PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A Web Platform/Browser; Track B recovery-state UX; Track C destructive/recovery validation; Software Engineering implementation evidence; Design Studio recovery interaction evidence.

## Why this block exists

093 separated server session validity, local unlock, offline authorization and local authoritative data. The next failure boundary is recovery: a user can recover an account yet still be unable to decrypt or restore local data; conversely, possession of local decryption capability does not necessarily restore server authentication authority.

The durable guard is:

`account recovery ≠ authenticator recovery ≠ device recovery ≠ local-data recovery ≠ backup recovery ≠ synchronization recovery`.

A second guard is equally important:

`credential rotation ≠ data-encryption-key rotation ≠ re-encryption ≠ old-device revocation`.

This study does **not** select a LogMate/MintTap cryptographic design. It establishes the web/security decision boundaries that an implementation must satisfy.

---

## 1. SOURCE — current standards and platform evidence

### 1.1 Account recovery is an authenticator-lifecycle operation, not data recovery

NIST SP 800-63B-4 (July 2025), §4.2 defines account recovery as recovering from loss of control of authenticators needed to authenticate at the desired assurance level. It identifies recovery methods including saved/issued recovery codes, recovery contacts and repeated identity proofing, and requires recovery notification. This establishes a security-account lifecycle; it does not establish recovery of application ciphertext, IndexedDB records or device-local keys.

Source: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b-4.pdf

**SYNTHESIS:** a successful account-recovery ceremony proves enough authority to bind replacement authenticators under the service policy. It does not imply possession of a key that encrypted offline application data.

### 1.2 WebAuthn explicitly distinguishes single-device and multi-device credentials

Web Authentication Level 3 became a W3C Recommendation on 2026-08-25. Credential backup eligibility (BE) is permanent for a credential source; backup state (BS) can change. `BE=0,BS=0` describes a single-device credential; `BE=1` describes a multi-device credential and BS reports current backup state. The Recommendation says backup may use peer-to-peer, cloud, local-network or manual import/export mechanisms and recommends RPs retain relevant backup-state information when policy depends on it.

Sources:
- https://www.w3.org/TR/2026/REC-webauthn-3-20260825/
- https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/

**SYNTHESIS:** `WebAuthn credential exists` is insufficient recovery information. Credential portability/backup semantics matter. Even then, an authentication credential is not automatically an application data-encryption key.

### 1.3 Apple passkeys provide an example of platform-managed credential recovery, not a generic PWA data-key guarantee

Apple documents passkeys in iCloud Keychain as end-to-end encrypted and synchronized across the user's devices. Apple also documents iCloud Keychain recovery for loss of all associated devices. Apple Developer currently states that managed environments can support passkeys with Managed Apple Accounts and iCloud Keychain subject to access controls.

Sources:
- https://support.apple.com/102195
- https://developer.apple.com/passkeys/

**BOUNDARY:** this is evidence about Apple's passkey/keychain ecosystem. It does not prove that a company-managed EFB permits iCloud Keychain synchronization/recovery, nor that a Home Screen PWA can use a platform passkey as an exportable application encryption key. Exact MDM/Managed Apple Account policy remains product/device evidence.

### 1.4 Web Crypto provides primitives and CryptoKey storage, not lifecycle architecture

The W3C Web Cryptography API allows `CryptoKey` objects to participate in structured clone; IndexedDB is the expected storage mechanism for such keys. The specification explicitly warns that applications/users with device-storage access may recover key material depending on implementation and imposes no normative zeroization requirement after references disappear. MDN documents `CryptoKey.extractable`; only extractable keys can be exported/wrapped. `wrapKey()`/`unwrapKey()` can support portable encrypted key material when the chosen key is exportable.

Sources:
- https://www.w3.org/TR/2017/REC-WebCryptoAPI-20170126/#concepts-key-storage
- https://developer.mozilla.org/en-US/docs/Web/API/CryptoKey/extractable
- https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/wrapKey
- https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/unwrapKey

**SYNTHESIS:** `extractable=false` reduces one export path but does not create hardware-backed, non-recoverable, device-bound or remotely revocable semantics by itself. Conversely, making a key exportable to enable recovery expands the key-handling attack surface. Recovery and confidentiality are a deliberate trade-off.

---

## 2. History/problem → design principle

Offline-first products create a three-way tension:

1. **availability:** irreplaceable records must survive account/device loss where product policy promises recovery;
2. **confidentiality:** a lost or stolen device should not indefinitely expose protected local data;
3. **offline autonomy:** the product must remain useful without continuous contact with a server.

No single `login`, `passkey`, `IndexedDB`, `Web Crypto`, `backup`, or `sync` mechanism resolves all three.

### Design principle

Model recovery as explicit authorities and key relationships rather than as a reset-password screen:

`identity/account authority → authenticator authority → local-unlock authority → data-encryption authority → backup unwrap authority → sync/reconciliation authority`.

Every arrow must be justified. Do not silently assume one authority grants the next.

---

## 3. Key roles that must not collapse

A product may have fewer or more keys, but architecture review must at least distinguish these conceptual roles:

| Role | Purpose | Loss consequence | Rotation consequence |
|---|---|---|---|
| authentication credential | prove identity/account control to RP/server | server login may fail | bind replacement credential; application ciphertext need not change |
| session credential/token | authorize current online session | online authority ends | normally no bulk data re-encryption |
| local-unlock factor/key | gate use of local application state | local use may fail | may require rewrapping local data key |
| data-encryption key (DEK) | encrypt authoritative local records | ciphertext may become unrecoverable | re-encrypt or rewrap strategy required |
| key-encryption/wrapping key (KEK) | protect DEK for device/backup/recovery contexts | wrapped DEK may become unavailable | rewrap DEK where possible |
| backup/recovery secret | permit independent recovery | backup may be unusable | old backup compatibility/revocation policy required |
| device/pairing credential | authenticate a synchronized peer/device | direct sync trust fails | peer re-pair/revocation; not necessarily data re-encryption |

**CONTRADICTION to avoid:** using one credential for all roles appears simple but couples password/passkey reset, device loss, backup, sync and bulk data encryption into one catastrophic lifecycle.

---

## 4. Recovery classes

### Class A — server-assisted recoverable data

Server/account recovery can restore data only if the server (or a recovery service reachable after account recovery) holds authoritative plaintext, an independently usable encrypted backup plus authorized unwrap capability, or enough material to reconstruct the data.

**Guard:** `account recovered ≠ server has recoverable application data`.

### Class B — user-held recovery secret

A user-held recovery code/key may unlock encrypted backup without server knowledge. This can improve confidentiality separation but creates loss/support/usability risks. A recovery code that restores authentication is not necessarily the same secret that unwraps application data.

**Guard:** `recovery code accepted by account service ≠ local ciphertext decryptable`.

### Class C — platform-managed credential/key recovery

Platform ecosystems may synchronize/recover credentials such as passkeys. Product policy must verify what is synchronized, under which account/MDM conditions, and whether the application key itself participates. Do not infer application data recovery from platform authentication recovery.

### Class D — deliberately non-recoverable local-only key

A device-bound/non-exportable design can intentionally make local ciphertext unrecoverable after device/key loss. That can be valid only if product promises, backup architecture and user messaging make this consequence explicit and an independent authoritative copy exists where required.

**Guard:** `stronger device binding may reduce recoverability`.

---

## 5. Device replacement and device revocation are different operations

### Replacement

Replacement asks: how does a legitimate new device obtain enough authority and state to continue?

Possible steps include account recovery/authentication, new authenticator binding, backup import/restore, key unwrap/rebinding, schema migration, state reconciliation and peer re-pairing.

### Revocation

Revocation asks: what authority should the old device lose?

Server-side revocation can deny future online operations once the old device reconnects. It cannot retroactively erase an offline device or guarantee immediate loss of locally cached/decrypted data.

**Persistent guard:**

`new device authorized ≠ old offline device erased or cryptographically contained`.

If immediate offline containment is a requirement, it must come from device/OS management, local expiration/unlock policy, hardware/platform key controls, or another independently validated mechanism—not from a server revocation flag alone.

---

## 6. Rotation semantics

### Authentication credential rotation

Replacing a password/passkey/authenticator changes how the server recognizes the user. It need not rotate the application DEK.

### KEK rotation

If the architecture supports it, a DEK can be rewrapped under a new KEK without re-encrypting every record. Whether Web Crypto/browser/platform behavior supports the intended implementation safely is Software Engineering validation.

### DEK rotation

Changing the DEK requires a migration strategy: re-encrypt records, version ciphertext/key IDs, survive interruption, preserve pending outbox semantics, handle skipped releases and prove backup compatibility.

### Backup-key rotation

Existing backups may remain encrypted under old recovery material. A rotation policy must state whether old backups remain restorable, are rewrapped/recreated, expire, or become intentionally unreadable.

**Guard:** `key rotated ≠ all historical ciphertext/backups migrated`.

---

## 7. Offline-first failure matrix

Implementation handoff must exercise at least:

1. device lost while all records are remotely acknowledged;
2. device lost with authoritative unsynced records;
3. account recovered on a new device but no application backup exists;
4. account recovered and backup exists but unwrap secret is unavailable;
5. passkey/authenticator recovered but application DEK is device-local;
6. application backup restored but server session is revoked;
7. old device reconnects after replacement/revocation;
8. DEK/KEK rotation interrupted mid-migration;
9. backup created before key rotation and restored after several releases;
10. user changes account credential while offline device remains active;
11. device clock is wrong during local expiry/unlock checks;
12. MDM/Managed Apple Account policy prevents assumed credential synchronization;
13. browser/site storage is evicted while independent backup remains;
14. local key remains but ciphertext/database is partially corrupted;
15. ciphertext remains but key is deleted/evicted/unavailable;
16. XSS/compromised origin executes while local key is usable.

A PASS requires data/security invariants, not merely successful UI navigation.

---

## 8. Track integration

### Track A — Platform/Browser dependency

Own exact WebAuthn/Web Crypto/IndexedDB/storage mechanics and browser differences. Track E consumes these mechanics for lifecycle policy. Safari/WebKit implementation details and managed-iPad behavior remain CHANGE WATCH / target-device validation.

### Track B — UX/IA transfer

Recovery UX must truthfully distinguish at least:
- account access restored;
- this device is newly authorized;
- local records on the lost device are not known to be recovered;
- backup found / backup verified / backup restored;
- sync pending / reconciled;
- old device access revoked online but offline containment unknown.

Do not display `Recovered` when only authentication succeeded.

### Track C — Quality/security oracle

Test oracles must verify record count/content integrity, pending-operation preservation, ciphertext/key-generation compatibility, old-device server rejection, new-device restore, skipped-version migration and destructive-action safety. Exact Safari/physical-device/AT evidence remains OPEN.

### Track D — Analytics/privacy

Recovery telemetry should be structural: recovery stage, generation/key identifiers that are non-secret, outcome class, restore verification and error category. Never log raw keys, recovery secrets, authentication tokens or decrypted flight records. Silent/lost offline devices prevent analytics from certifying revocation completeness.

### Track E — owner

Owns threat/recovery policy, authority separation, key lifecycle requirements, device loss/replacement/revocation contract, retention/destruction gates and incident response.

---

## 9. Design Studio transfer

Latest Design Studio Web evidence checked 2026-09-17: Stage 1/2 PASS; Stage 3 remains PRACTICE / NOT PASSED. W045 partial-order merge runtime is ready but execution remains OPEN; no Safari, cross-browser, screen-reader, physical-device/print, field-CWV or human-UX PASS may be inferred.

**DEPENDENCY:** Design Studio should eventually validate recovery language/action hierarchy, destructive confirmation, backup provenance, merge/reconciliation states and accessible status communication. Web Manager supplies semantic truth; Design Studio owns reusable interaction/visual evidence.

---

## 10. Software Engineering transfer

Latest Software Engineering Studio commits checked 2026-09-17 show D006 replication/sync retry-conflict evidence progressing after D004/D005. This strengthens the requirement that restored/local/pending/remote state must reconcile explicitly rather than treating restore as a blind replacement.

Implementation-level questions remain theirs:
- exact key hierarchy and algorithms;
- browser/Flutter/native key storage choice;
- extractability and wrapping implementation;
- schema/ciphertext versioning;
- interruption-safe re-encryption/rewrap;
- platform secure storage/hardware binding;
- managed-iPad execution;
- sync conflict/idempotency semantics.

Web Manager must not claim these are solved from generic Web Crypto evidence.

---

## 11. MINTTAP / LOGMATE DIRECTION

1. Do not promise that account recovery restores offline records until an independent restore path is implemented and tested.
2. Do not use passkey recovery/synchronization as evidence that application encryption keys or IndexedDB records are recoverable.
3. Treat authentication, local unlock, DEK/KEK, backup and pairing credentials as distinct lifecycle roles even if a future implementation intentionally derives/links some of them.
4. Do not make destructive logout/account-recovery/device-replacement cleanup contingent only on server authentication success.
5. For irreplaceable offline records, require a documented answer to: **what exact material survives loss of this device, who can recover it, and what security property is weakened by making it recoverable?**
6. Preserve an independent backup/restore acceptance path where product requirements demand recovery from total device loss.
7. Treat managed-EFB iCloud Keychain/passkey synchronization and MDM behavior as target-device facts, not generic Apple assumptions.

---

## 12. OPEN

Product closure requires exact evidence for:
- authentication provider/session architecture;
- whether passkeys are used and their backup eligibility/state policy;
- Managed Apple Account/iCloud Keychain policy on company EFBs;
- authoritative local record and backup classes;
- actual encryption-at-rest requirement/threat model;
- local-unlock requirement and lifetime;
- chosen DEK/KEK/recovery hierarchy;
- key extractability/wrapping/storage semantics in exact browser/runtime;
- device replacement/revocation UX and security policy;
- account deletion vs device loss vs credential compromise retention;
- old backup/key compatibility window;
- physical managed-iPad restore/revocation tests.

---

## 13. CHANGE WATCH

- WebAuthn Level 3 is a W3C Recommendation dated 2026-08-25; Level 4 is the future development line.
- Credential backup-state interpretation and browser/platform UX can evolve.
- Apple passkey/Managed Apple Account/iCloud Keychain policy and MDM controls are platform-policy-sensitive.
- Web Crypto implementation and storage behavior must be validated per target browser/runtime; the generic API does not establish hardware-backed or zero-knowledge semantics.

---

## 14. Gate decision

**PASS (generic) / PRODUCT CRYPTOGRAPHIC + DEVICE VALIDATION OPEN.**

Generic account/device/key-recovery boundaries are sufficient for product-security and Software Engineering handoff. No production claim is made. The next adjacent high-value question should not repeat cryptographic primitives. Prefer exact implementation evidence when it appears; otherwise investigate **PWA XSS/origin compromise against locally unlocked encrypted data and recovery keys**, because encryption-at-rest can fail to protect data while trusted-origin JavaScript is executing.