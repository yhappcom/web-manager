# 085 — PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security

Status: **PASS — continuous expert maintenance checkpoint**
Date: 2026-09-16
Primary owners: **E Architecture/Security/Operations + B UX/IA/Content**
Dependencies: A browser/storage/security mechanics; C accessibility/recovery validation; Software Engineering implementation evidence.

## Purpose
Integrate backup/export/restore, offline authorization, sensitive local storage, device loss, and user-visible durability state for an EFB/LogMate-like PWA that may hold irreplaceable pilot flight records while disconnected.

## Integrated model
`record creation → transactional local commit → durability state → independent recovery copy → optional sync/outbox → remote acknowledgement → reconciliation → backup verification → device loss/replacement → authenticated restore → integrity/schema validation → usable recovered task`

Persistent guard:
`saved locally ≠ persistent ≠ synchronized ≠ backed up ≠ restorable ≠ authorized offline ≠ safe after device loss`.

## 1. Security problem: offline usefulness expands the trust boundary
SOURCE — browser storage is origin-scoped, but client-side storage remains readable/manipulable by JavaScript executing in that origin. OWASP warns that client storage must not be treated as trusted and that XSS can expose stored sensitive data. Session identifiers/tokens should not be placed in localStorage/sessionStorage; HttpOnly/Secure/SameSite cookies or server-side/BFF patterns reduce JavaScript exposure for session credentials.

SYNTHESIS — Same-Origin Policy prevents arbitrary other origins from directly reading IndexedDB/Web Storage, but does not protect records from malicious script that has gained execution in the legitimate origin, nor from a person with sufficient device/local access. Therefore origin isolation is necessary but not a data-at-rest/device-loss guarantee.

CONTRADICTION — “The PWA is HTTPS and IndexedDB is same-origin, therefore locally stored flight records are secure” is false. HTTPS protects transport/secure-context eligibility; SOP isolates origins; neither establishes the product's device-loss, XSS, key-management, authorization or backup guarantees.

## 2. Offline authentication is not one state
Separate:
1. **identity evidence** — who authenticated previously;
2. **server session validity** — whether the server would currently accept credentials/session;
3. **local unlock state** — whether this installed client currently permits local record access;
4. **offline authorization policy** — what operations are permitted without current server contact;
5. **queued mutation authority** — whether an offline-created operation will be accepted when reconnecting;
6. **re-authentication/revocation state** — what happens after logout, credential revocation, account disablement, device loss or long inactivity.

SOURCE — WebAuthn Level 3 became a W3C Recommendation on 2026-08-25. It defines strong, scoped public-key credentials mediated by the user agent/authenticator. This establishes a strong online/web authentication primitive, not a generic product rule for offline authorization or local-database encryption.

SYNTHESIS — offline access requires a product-defined bounded authorization contract. A cached statement that a user authenticated previously cannot by itself prove current server authorization indefinitely.

## 3. Credential storage and local cryptography boundaries
SOURCE — Web Crypto exposes cryptographic primitives in secure contexts. It can encrypt/decrypt data, but the API is deliberately low-level. OWASP storage guidance separately warns about sensitive data and cryptographic material exposed to client-side attack chains.

SYNTHESIS — “encrypt IndexedDB with Web Crypto” is incomplete architecture. Security depends on where the decryption key comes from, whether it is extractable, what unlocks it, whether malicious same-origin script can invoke decryption, recovery/key rotation, multi-device restore, and what happens when credentials are revoked.

A product considering client-side encryption must document:
- threat being mitigated;
- key generation/source;
- key persistence and extractability;
- user/device unlock mechanism;
- recovery/escrow policy if any;
- rotation/revocation;
- backup portability;
- XSS/same-origin script implications;
- lost-device behavior.

OPEN — no LogMate encryption/key architecture is established here. Software Engineering/security validation is required before selecting one.

## 4. Recovery architecture for irreplaceable records
For irreplaceable pilot records, recovery must be designed independently of sync latency.

### Recovery Contract
Record:
- authoritative record identity/version;
- maximum acceptable data loss window;
- local commit semantics;
- independent recovery destination(s);
- export/backup format and schema version;
- integrity metadata/checks;
- encryption/key dependencies where applicable;
- backup trigger and completion evidence;
- restore compatibility window/migrations;
- duplicate/conflict policy;
- new-device restore procedure;
- restore validation by actual user task;
- retention/deletion policy;
- owner and test cadence.

SYNTHESIS — automatic synchronization may produce a remote replica, but “remote replica” should be called backup only if its retention, deletion coupling, corruption propagation, historical recovery and restore behavior satisfy the Recovery Contract.

## 5. Export is not backup until the lifecycle closes
Distinguish:
`export initiated → bytes produced → destination committed → artifact discoverable → integrity/version known → retained independently → import accepted → migration completed → records reconciled → user task verified`.

A share/download/export button proves only the first part of this chain.

For iPad/EFB, destination feasibility is device/MDM specific. Generic browser file/share capability does not establish that the managed company iPad permits a durable user-controlled destination.

OPEN — actual EFB Files/share/export permissions and retention policy require target-device validation.

## 6. Device loss and logout
Device loss can create two distinct risks: **confidentiality** of local records and **availability** of the only surviving copy.

Required questions:
- can a lost device still open local records while offline?
- can remote logout/revocation affect an offline device, and only after what contact?
- what is the maximum offline authorization lifetime?
- does local logout delete records, credentials, encryption keys, or merely lock them?
- could logout accidentally destroy the sole unsynchronized record copy?
- after device replacement, what evidence is required to restore data?

SYNTHESIS — remote revocation cannot instantaneously control a disconnected client. Products must state this residual window rather than imply real-time revocation offline.

CONTRADICTION — aggressive “logout = delete all local data” can improve confidentiality yet create catastrophic availability loss when unsynchronized records exist. The correct behavior depends on threat model, recovery state and product policy; it requires explicit conflict resolution rather than a generic rule.

## 7. User-visible durability state model
B owns the language/state architecture; Design Studio owns visual presentation.

Never collapse the following into one “Saved” indicator:
- **Saved on this device** — local transaction committed;
- **Waiting to sync** — durable outbox contains unapplied operations;
- **Syncing** — transport attempt active;
- **Synced / acknowledged** — remote side acknowledged defined operations;
- **Conflict / review required** — reconciliation cannot complete automatically;
- **Backup current** — independent recovery contract says a sufficiently current recoverable copy exists;
- **Backup overdue/not verified** — recovery objective is not currently evidenced.

SYNTHESIS — state wording is a safety property. False reassurance can cause a user to erase/replace a device believing data is recoverable.

C dependency — state must remain perceivable without color alone, keyboard/AT accessible, and understandable in offline/error/recovery states. Exact UI validation remains Design Studio + implementation/device evidence.

## 8. Long-offline/skipped-version restore
A returning client or backup may be several schemas/protocol versions behind.

Acceptance sequence:
`identify artifact/schema/protocol → preserve original copy → validate integrity → migrate through supported path → preserve stable record/operation IDs → replay queued operations idempotently → reconcile duplicates/conflicts → verify totals/records → only then retire old copy`.

Do not mutate the sole historical backup destructively before successful migration is evidenced.

TRANSFER VALIDATION — Software Engineering evidence that identical call shape can hide changed semantic contracts reinforces that schema/protocol version numbers alone do not prove semantic compatibility.

## 9. Analytics/privacy boundary
D may observe state transitions needed for operational/product diagnosis, but telemetry must not become a second sensitive logbook.

Prefer event semantics such as backup success/failure class, age bucket, migration outcome or sync state where sufficient. Do not send flight-record content, memo text, crew identity or other record payload merely to measure backup/sync UX.

Guard:
`measurement usefulness ≠ permission to replicate sensitive domain data into analytics`.

## 10. EFB acceptance tests required before product claims
VALIDATION — target managed iPad, exact canonical artifact, representative records:
1. create records offline and force-terminate/relaunch;
2. reboot/long-inactivity/storage-pressure scenarios where safely testable;
3. backup/export then remove/replace application state and perform clean restore;
4. restore an older schema artifact through supported migrations;
5. device offline beyond server session/re-auth threshold;
6. logout with pending unsynchronized records;
7. credential/account revocation followed by later reconnect;
8. duplicate/replayed operations after ambiguous acknowledgement;
9. corrupted/incomplete backup detection;
10. accessibility/readability of Saved/Queued/Synced/Backup/Conflict/Recovery states.

No generic browser documentation can substitute for these product tests.

## 11. Five-track integration
- **A owner:** origin/storage/WebAuthn/Web Crypto/browser mechanics and CHANGE WATCH.
- **B co-owner:** explicit durability/auth/recovery state semantics and recovery journeys.
- **C consumer:** resilience, accessibility, destructive-action safety, exact-device regression evidence.
- **D consumer:** privacy-minimized observability; never infer durability from analytics arrival.
- **E primary owner:** threat model, offline authorization, backup/recovery contract, revocation/device-loss/incident policy.

## 12. Operational judgment
For LogMate-like EFB use, the defensible baseline is:
`transactional local save + durable outbox + explicit local/sync/backup states + independent recovery path + tested clean restore + bounded offline authorization + reconnect reconciliation`.

Client-side encryption may be valuable against a defined threat but is not accepted merely because Web Crypto exists. Direct unattended PWA↔native transport remains a separate OPEN problem and is not required to define correct local durability/recovery semantics.

## Sources / freshness
- W3C, Web Authentication Level 3 Recommendation, 2026-08-25 — current standard.
- OWASP HTML5 Security Cheat Sheet — current operational security guidance checked 2026-09-16.
- OWASP Session Management Cheat Sheet — current guidance checked 2026-09-16.
- OWASP Web Security Testing Guide browser-storage guidance — current guidance checked 2026-09-16.
- MDN Web Crypto / SubtleCrypto / Same-Origin Policy / IndexedDB — platform reference checked 2026-09-16.

CHANGE WATCH — WebAuthn Level 4 work, Safari/iPadOS authentication/storage behavior, managed-device policies and browser file/share capabilities can evolve; product conclusions require fresh target-platform evidence.