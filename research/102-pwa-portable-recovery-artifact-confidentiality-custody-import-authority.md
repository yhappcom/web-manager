# 102 — PWA Portable Recovery Artifact Confidentiality, Custody & Import Authority

Status: **PASS (generic) / PRODUCT BACKUP-CRYPTO + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 094 key lifecycle; 099 trust-policy authenticity; 100 reset/rebootstrap; 101 mixed-epoch recovery; Track A file/browser mechanics; Software Engineering D003/D005/D006.

## Purpose

101 established that recovery is a mixed-epoch acceptance/reconciliation problem. This study asks what changes when the recovery artifact leaves origin storage and becomes a user-portable file: Files/cloud storage, system share sheet, email/message transfer, removable/user-accessible storage or later import.

The objective is not to prescribe a LogMate/MintTap backup format or cryptographic hierarchy. It is to establish the security, privacy, portability, custody and import-authority requirements that an implementation must satisfy.

---

## 1. Track allocation

- **A Platform/Browser — dependency supplier.** File selection and sharing are user-mediated browser/OS capabilities; capability availability is platform-dependent.
- **B UX/IA/Content — consumer.** Exported, shared, encrypted, imported, verified, unlocked, accepted and sync-ready are distinct states.
- **C Performance/Accessibility/Quality — validation owner.** Owns large/corrupt/hostile file, interruption, wrong-key, cross-version, accessibility and target-device matrices.
- **D Search/Discovery/Analytics — low direct pressure.** Backup filenames, paths, manifests and diagnostic metadata must not become analytics/discovery payloads.
- **E Architecture/Security/Operations — highest-risk owner.** Owns confidentiality, key custody, metadata minimization, import trust, retention/versioning and recovery authority boundaries.

**Allocation:** E remains highest value. Do not duplicate Software Engineering's parser/database/reconciliation implementation work.

---

## 2. SOURCE — portability crosses the origin-storage boundary

### W3C File API

The 23 August 2026 File API Working Draft models files selected from the underlying system and explicitly assumes user selection for ordinary file reading. Its security considerations call out malicious selection loops, system-sensitive files and changes after selection.

Source: https://www.w3.org/TR/FileAPI/

**SYNTHESIS:** importing a portable backup is an explicit trust-boundary crossing. A user selecting a file grants the application access to bytes; it does not establish that those bytes are a legitimate backup, belong to this account/product, are current, are safe to parse, or are authorized to replace live state.

**Guard:** `user selected file ≠ trusted recovery artifact`.

### Web Share API

MDN's current Web Share documentation records that file sharing is secure-context-only, requires transient user activation, is controlled by the `web-share` Permissions Policy, uses OS-selected targets, and remains limited-availability rather than Baseline. The Web Share API is not available in Web Workers.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API
- https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share
- https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare

**CHANGE WATCH:** exact file-share support and share-target behavior must be validated on supported Safari/Home Screen PWA and managed iPad versions.

**SYNTHESIS:** the application can initiate a user-mediated share where supported, but does not control the ultimate destination or its retention/security policy.

**Guard:** `share sheet completed ≠ destination confidential ≠ backup still under application custody`.

---

## 3. SOURCE — encrypted backup and key custody are separate systems

OWASP Cryptographic Storage and Key Management guidance requires threat-model-driven encryption, separation of keys and data where possible, explicit key lifecycle/recovery planning and secure backup/escrow for encryption keys when long-term encrypted data must remain recoverable. It also notes the fundamental availability trade-off: encrypted data cannot be recovered when the necessary key is lost.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

W3C Web Cryptography Level 2 specifies that `wrapKey()` effectively exports the wrapped key and therefore requires that key to be extractable; `unwrapKey()` can create a non-extractable key. API availability does not define a safe backup key hierarchy.

Source: https://www.w3.org/TR/WebCryptoAPI/

**SYNTHESIS:** portable ciphertext is useful only if the recovery path can obtain the correct decryption authority. Placing ciphertext and an immediately usable plaintext/raw key in the same portable package collapses much of the intended separation. Conversely, making the only key permanently device-local can turn device loss into permanent backup loss.

**Guards:**
- `backup encrypted ≠ backup recoverable`;
- `backup encrypted ≠ key independently protected`;
- `ciphertext + directly usable key in same artifact ≠ meaningful key/data separation`;
- `device-bound key ≠ portable recovery capability`;
- `portable recovery key ≠ acceptable bearer-secret exposure`.

Exact DEK/KEK/passphrase/recovery-key design remains a Software Engineering/security decision.

---

## 4. Cloud/Files custody is not one universal security property

Apple's current iCloud security documentation distinguishes Standard Data Protection from Advanced Data Protection. Under standard protection, Apple can hold keys needed to recover many iCloud data categories; Advanced Data Protection extends end-to-end encryption to additional categories such as iCloud Backup. Apple also documents that some metadata remains under standard protection. Apple Platform Security notes that administrators can disable services such as iCloud Drive/iCloud Backup through device-management configuration.

Sources:
- https://support.apple.com/en-ie/102651
- https://support.apple.com/guide/security/secacde2d0da/web

**SYNTHESIS:** `saved in Files/iCloud` is not a complete confidentiality statement. Security depends on destination, account protection mode, metadata, sharing, enterprise policy and whether the user later copies the artifact elsewhere.

**CHANGE WATCH:** exact managed-EFB Apple Account/iCloud Drive/Files policy is product evidence, not inferred from generic Apple capability.

**Guards:**
- `saved to cloud ≠ end-to-end encrypted under every account configuration`;
- `file contents encrypted ≠ filename/size/timestamps/manifest metadata confidential`;
- `Files destination available on consumer iPad ≠ permitted on managed EFB`.

---

## 5. Portable artifact threat model

A portable recovery artifact creates at least these threat classes:

1. **Disclosure:** another app/person/cloud provider obtains records or metadata.
2. **Key co-location:** artifact includes sufficient key material to decrypt itself.
3. **Bearer authority:** possession of the file silently grants account/device/trust-policy authority.
4. **Malicious import:** attacker supplies crafted/corrupt/oversized/parser-hostile content.
5. **Rollback/downgrade:** old valid backup restores obsolete trust/protocol/security state.
6. **Cross-account/product confusion:** structurally valid backup is imported into the wrong identity/environment.
7. **Partial/mixed epoch:** records, keys, trust, schema, protocol and outbox do not share a coherent recovery point.
8. **Unbounded retention:** old backups preserve deleted records, tombstones, secrets or obsolete key material indefinitely.
9. **Accidental forwarding:** share sheet/email/message workflow moves the file outside intended custody.
10. **Metadata leakage:** filename, product/account/device identity, dates or manifest disclose information without decrypting records.

A backup can be useful and still be dangerous under several of these simultaneously.

---

## 6. Import is hostile-input processing before it is recovery

OWASP File Upload guidance recommends defense in depth: allowlisted required formats, independent type/content validation rather than trusting `Content-Type`, size limits, safe filename handling, authorization, safe storage and caution around archive/parser bombs and active content.

Source: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html

The guidance targets upload systems broadly, not PWA backup restore specifically. The transferable principle is that imported bytes are untrusted until parsed and validated under a narrow contract.

**TRANSFER VALIDATION:** apply hostile-input/parser discipline; do not copy server-upload architecture mechanically into a local PWA.

**Guards:**
- `recognized extension ≠ recognized content ≠ valid manifest ≠ authorized recovery`;
- `decrypt succeeded ≠ semantic validation succeeded`;
- `manifest says account/device X ≠ importer authorized as X`.

Import should preserve 101's staged acceptance: bounded read/parse → integrity/provenance → cryptographic binding → schema/domain validation → trust/protocol validation → reconciliation → publication/replay authorization.

---

## 7. A portable backup must not silently become a bearer credential

The artifact may contain user data and recovery metadata, but possession alone should not automatically grant unrelated live authority unless that is an explicit, justified security model.

Security-sensitive classes to review separately:
- authentication/session tokens;
- refresh tokens;
- device/pairing credentials;
- trust-policy signing/private keys;
- server API credentials;
- encryption DEKs/KEKs/recovery secrets;
- outbox logical-operation identities;
- user records and tombstones;
- diagnostic/provenance metadata.

**MINTTAP/LOGMATE DIRECTION:** portable backup must have an explicit inclusion/exclusion policy per authority class. Defaulting to “serialize the whole origin database” is not an acceptable security specification.

**Guards:**
- `backup proves possession of old data ≠ current account authentication`;
- `backup import accepted ≠ old session/device credential should be reactivated`;
- `restored trust metadata ≠ authority to downgrade current trust policy`;
- `restored pairing state ≠ remote peer currently authorized`.

---

## 8. Metadata minimization and unlinkability

Encrypting record bodies while leaving descriptive metadata plaintext can still disclose product use, backup dates, account/device identifiers, record counts, schema generation or operational history.

A recovery manifest may require some plaintext bootstrap information, but every field should have a reason to be outside the protected envelope. Human-friendly filenames should avoid unnecessary sensitive identity unless product requirements justify it.

**MINTTAP/LOGMATE DIRECTION:** classify manifest fields as `required-before-unlock`, `safe diagnostic`, or `confidential`; minimize stable identifiers exposed outside authenticated encryption.

**Guard:** `payload encrypted ≠ backup privacy complete`.

Analytics must not receive backup filenames, manifest IDs, recovery secrets, raw record counts or user-controlled imported metadata unless separately justified and privacy-reviewed.

---

## 9. Retention, rotation and deletion are part of the backup protocol

Old backups can be valuable for recovery while simultaneously retaining:
- records the user later deleted;
- old tombstones/conflict history;
- obsolete schema/protocol state;
- old wrapped keys;
- revoked device/pairing metadata;
- vulnerable-format artifacts.

Therefore “keep every backup forever” and “always keep only latest” are both unsupported defaults.

A product policy needs explicit answers for:
- number/age of retained versions;
- whether old key generations remain decryptable and for how long;
- migration/reader support window;
- how a user can identify backup age/version without exposing sensitive metadata;
- whether export replaces or supplements automatic backup;
- deletion/retirement behavior;
- whether restoring an old artifact requires online revalidation before sync.

**Guard:** `more backup copies ≠ monotonically safer recovery`.

---

## 10. Recovery authority matrix

A portable artifact should be evaluated independently for capabilities rather than granted an aggregate PASS.

| Capability | Possession of backup alone sufficient? | Generic default |
|---|---:|---|
| Inspect non-sensitive header/version | possibly | bounded parser only |
| Decrypt user records | no automatic assumption | require correct recovery authority |
| Read restored records locally | after validation | may be allowed independently of sync |
| Replace current live state | no | validate candidate and preserve known-good state |
| Authenticate current account | no | separate auth/recovery flow |
| Restore session/refresh token | no default | generally security-sensitive; product proof required |
| Restore device/pairing trust | no | revalidate current authority |
| Downgrade trust/security policy | no | current trust rules win unless authenticated recovery protocol says otherwise |
| Replay outbox | no | reconcile current server/protocol/ack state first |
| Export/share again | product policy | warn/mediate according to sensitivity |

This matrix is a requirements model, not a finished product policy.

---

## 11. B/C truthful-state and validation requirements

User-facing semantics must distinguish:
- backup created vs saved to a destination;
- saved vs independently recoverable;
- encrypted vs key available;
- imported vs verified;
- decrypted vs compatible;
- records recovered vs account/session recovered;
- local recovery vs synchronization ready;
- share initiated vs destination controlled.

Design Studio owns final interaction/copy. Current Design Studio Web evidence is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE, with W053 graph-integrity closure ready but runtime execution OPEN. No Safari/AT/physical-device PASS is inferred.

High-value eventual validation matrix:
1. correct backup + correct recovery authority;
2. correct backup + missing/wrong key;
3. tampered ciphertext/tag/manifest;
4. renamed extension/MIME mismatch;
5. oversized and archive/decompression-bomb candidate if archives are supported;
6. valid old backup after trust/protocol/key rotation;
7. valid backup from another account/product/environment;
8. backup containing obsolete session/device/pairing credentials;
9. share destination unavailable or canceled;
10. share succeeds but app cannot know destination retention;
11. Files/iCloud disabled by managed-device policy;
12. offline export and later offline import;
13. interruption during export, import, decrypt, validation and publication;
14. 200% text, keyboard/screen reader and accessible error/recovery states;
15. exact Safari/Home Screen PWA managed-iPad file selection/share behavior.

---

## 12. Cross-repository transfer

Software Engineering Studio remains Foundation IN STUDY. Its D003/D005/D006 evidence is consumed for reader compatibility, validate-before-publish and replay/reconciliation. 102 adds web/PWA requirements around portable custody and hostile import; it does not replace implementation-level parser, database, crypto or sync design.

Design Studio W053's graph-integrity direction reinforces a useful transfer: an artifact may contain all expected members yet still fail dependency/coherence validation. No runtime/design PASS is imported.

---

## 13. Persistent guards added by 102

- `user selected file ≠ trusted recovery artifact`;
- `share sheet completed ≠ destination confidential ≠ backup still under application custody`;
- `backup encrypted ≠ backup recoverable`;
- `backup encrypted ≠ key independently protected`;
- `ciphertext + directly usable key in same artifact ≠ meaningful key/data separation`;
- `device-bound key ≠ portable recovery capability`;
- `portable recovery key ≠ acceptable bearer-secret exposure`;
- `saved to cloud ≠ end-to-end encrypted under every account configuration`;
- `file contents encrypted ≠ filename/size/timestamps/manifest metadata confidential`;
- `Files destination available on consumer iPad ≠ permitted on managed EFB`;
- `recognized extension ≠ recognized content ≠ valid manifest ≠ authorized recovery`;
- `decrypt succeeded ≠ semantic validation succeeded`;
- `backup proves possession of old data ≠ current account authentication`;
- `backup import accepted ≠ old session/device credential should be reactivated`;
- `payload encrypted ≠ backup privacy complete`;
- `more backup copies ≠ monotonically safer recovery`.

---

## 14. OPEN / VALIDATION

1. Exact MintTap/LogMate backup/export format and component inclusion policy.
2. Exact encryption/key-recovery design and threat model.
3. Whether user-controlled export is primary backup, supplemental backup or migration artifact.
4. Managed-iPad Files/iCloud/share policy and target Safari/Home Screen support.
5. Actual cloud destination and organizational custody requirements.
6. Metadata confidentiality requirements.
7. Retention/version rotation and old-reader/key support window.
8. Hostile import parser limits and sandbox/streaming strategy.
9. Account/device/pairing/session material inclusion/exclusion.
10. Cross-version/cross-account/cross-environment restore behavior.
11. Accessible target-device export/import/recovery execution.

Production validation remains OPEN.

---

## 15. Next high-value boundary

102 closes the generic portable-artifact confidentiality/custody/import-authority prerequisite sufficiently for implementation handoff. The next adjacent high-value question is **backup freshness, completeness and recoverability evidence**: how the product proves that an automatic/manual backup actually captured the latest authoritative local records/outbox, reached durable external custody, remains decryptable/readable across supported versions, and has been restore-tested without turning telemetry into a privacy leak. This should consume Software Engineering recovery/fault-injection evidence when available rather than inventing implementation details.