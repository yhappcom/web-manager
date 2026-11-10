# Stage 8 — exact LogMate whole-ledger backup source and PWA custody boundary

**Inspected 2026-11-10 KST.** Evidence: pinned **SOURCE** from LogMate `main@f4bcd2f7b7e77039e29653baa1cc93797673885b`, plus **SYNTHESIS** and proposed **VALIDATION**. **No new tests run; production OPEN / PWA release HOLD.** This corrects the narrower source-location UNKNOWN in [Evidence Register EV42](EVIDENCE_VALIDATION_REGISTER.md) and [Research Gaps Q29](RESEARCH_GAPS_AND_SCHEDULE.md); it does **not** supersede their unknown deployed Files/export UI or product PASS.

## SOURCE — resolved paths, versions, exact boundaries

A complete, **non-truncated** Git tree for the pinned LogMate commit identified:
- [WholeLedgerBackup codec](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/lib/repository/logbook/whole_ledger_backup.dart), blob `711f784534bc686a4d8edd6617ac4d1ac362e0a7`;
- [whole-ledger backup test](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/test/repository/logbook/whole_ledger_backup_test.dart), blob `2f9d6b0a9a6a494dfd64c95b1e3db8aaa562537b`;
- `lib/repository/logbook/sembast_logbook_repository.dart` (repository export/restore entrypoints referenced in test);
- [approved Manual Sync contract](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/docs/specs/local-first-manual-delta-sync-contract.md).

The codec explicitly describes itself as a **narrow integrity container, not encryption or author authentication**. `WholeLedgerBackup` serializes a JSON object with exactly `manifest` and `stores`, sorts map keys recursively using Dart string comparison, accepts versions 1 and 2 as constants, and provides an internal SHA-256 helper over UTF-8. This establishes **codec behavior**, not a claim that every exported file is valid or that checksum alone authenticates a sender. In particular, an attacker who can change both payload and unkeyed checksum is not stopped by SHA-256.

The test file contains source-visible cases for a populated v16/v1 fixture, 30-store legacy import, version-17 destination schema, destination replica preservation, owner locked after restore, tamper rejection, transactional rollback/retry, occupied destination rejection and duplicate store-key rejection. These are **test definitions at the pinned SHA**; historical executed native tests are separately indexed in [Evidence Register EV06](EVIDENCE_VALIDATION_REGISTER.md). Reading a test file does not constitute executing that test today.

The approved Sync contract requires a structured `.lbk` full-ledger transfer, verified UID, owner-safe fresh replica, no silent overwrite of an occupied ledger, and separately authenticated Manual Sync. It explicitly distinguishes the current contract from implemented full backup, P2P and production deployment. It does not authorize treating `.lbk` as encrypted, externally stored, or safely restorable on a managed EFB.

## SYNTHESIS — three trust boundaries and counterexamples

1. **Container integrity vs confidentiality/authenticity (E owns).** A valid JSON manifest and recomputed SHA-256 detect accidental mismatch but cannot establish an authorized author or hide flight records. Do not label an unencrypted export “secure backup” without separate protection, transport and custody evidence. Wrong-owner checks and destination zero-write must be verified at the repository admission boundary, not inferred from `decode()`.
2. **Repository restore vs independent Files custody (A/E/C).** In-memory/native Sembast tests can demonstrate a transaction rollback and owner/replica invariants, but cannot establish a managed iPad can save, locate, reopen and restore a file after the PWA origin/profile disappears. Export generation, Files save, independent readback and fresh-container restore are four different checkpoints.
3. **Historical v1/v2 vs current 37-store inventory (E/C).** A 30-store v1 fixture and an updated destination schema do not establish current v2's complete 37-store transfer, deletion parity, pending/receipt/cursor integrity or cross-platform codec equivalence. The [37-export/29-drop static concern](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) remains a **separate** deletion gate; backup completeness cannot be inferred from that count alone.

**CONTRADICTION resolved:** Prior Web Manager Q29 said the exact writer/reader path had not been independently identified after code search returned no results. A full Git tree reveals a real codec and repository test. The prior “unknown file path” is now resolved **for the pinned checkout**, but the exact user-facing export UI, deployed artifact, current PWA file transfer, encryption status of any additional wrapper, and managed EFB Files handling remain OPEN. No prior product FAIL/PASS is inferred.

## Five-track transfer and operational judgment

- **E primary:** backup authorization, owner/schema/epoch, checksum vs MAC/signature, encrypted-at-rest choice, deletion/retention and incident recovery; do not prescribe encryption without owner decision.
- **A dependency:** JSON/UTF-8 canonicalization, browser Blob/File APIs, WebKit storage and managed Web Clip isolation; browser availability is version/policy dependent.
- **C independent validation:** exact pinned Dart VM/compiled-Web fixtures, wrong UID, duplicate key, malformed JSON, oversized/deep input, interrupted write, fresh reopen, 37-store counts and canary comparisons.
- **B transfer:** label “Export prepared”, “Saved to Files”, “File verified” and “Restored in new installation” only after corresponding observations; preserve non-destructive recovery UX and accessible error paths.
- **D transfer:** no public “encrypted”, “automatically backed up”, “offline-proof” or “synced” claims from the codec alone; Marketing controls acquisition claims, Design Studio owns visual interaction specifications.

## VALIDATION — prioritized executable packet (DEFINED, NOT RUN)

**LB-S01–S04 source:** Engineering pins current LogMate HEAD, full writer/reader and UI invocation paths, v1/v2 manifest validation and full store registry; independently inspect digest computation/verification, owner/epoch admission and transaction scope. Confirm whether any higher-layer encryption wrapper exists; do not extrapolate from this codec.

**LB-R05–R10 runtime:** export populated 37-store disposable ledger with tombstones, custom values, revisions, pending/receipts/cursors; verify byte hash and complete inventory; import to an empty independent DB and cold reopen; prove destination replica differs; corrupt manifest, duplicate keys and wrong UID produce zero mutation; interrupted restore rolls back; native and compiled-Web decoding agree on canonical bytes and supported limits.

**LB-D11–D16 device:** on an *authorized disposable* managed iPad, separately test Safari tab, Home Screen web app and permitted managed Web Clip; generate export, explicitly save in Files, reopen by independent user action, remove/recreate the disposable app container only with approved safeguards, and restore into a fresh context. Record OS/MDM policy, browser build, source/build SHA, origin, storage context, file hash, owner/replica and post-restart ledger checks. Do not clear the only operational flight logbook or assume hotspot/direct peer Sync.

**LB-X17–X20 security/UX:** wrong-owner file and occupied destination must be non-destructive; checksum-valid maliciously altered JSON must not bypass semantic/owner validation; lost file permission, quota and cancelled share must not show success; accessibility status and analytics must not disclose flight data or action tokens. A Files save is not a server ACK.

**MINTTAP DECISION:** preserve Stage 8 ACTIVE, production OPEN, PWA HOLD. **DEPENDENCY:** Engineering exact repository entrypoints and disposable build, owner-approved backup/encryption policy, authorized MDM device operator and Design Studio recovery UX. **CHANGE WATCH:** WebKit Files/share/installed storage, MDM restrictions and cross-platform JSON handling. Next major target: source-pinned current `sembast_logbook_repository.dart` export/restore checks and actual NORMAL PWA/managed-EFB custody tests.