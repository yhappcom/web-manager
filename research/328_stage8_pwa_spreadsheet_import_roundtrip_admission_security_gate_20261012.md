# 328 — Stage 8 PWA Spreadsheet Handoff, Untrusted Import and Semantic Admission Gate

**Checkpoint:** 2026-10-12 Asia/Seoul. **Canonical baseline:** `yhappcom/web-manager/main@526c6500c070dcf42964de16c0f87033cd7cad57`; required AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research/README, research 320–324 and recent commits read. **Read-only LogMate:** `main@827a7deed162bf525313c6b4b9d244e56828a1c1`. **Owner:** E; A supplies browser/File/Share mechanics, B review/recovery task states, C independent negative/runtime oracles, D privacy-safe measurement. Web Manager coordinates, not a sixth specialist. **Gate:** SOURCE/SYNTHESIS + source-bounded diagnosis + synthetic lab only; product/managed-iPad/production OPEN.

## HISTORY / PRINCIPLE / STANDARD

A portable spreadsheet is an editable interchange surface, **not** automatically a trusted backup, receiver commit, native Sync, or authorized mutation. Model distinct boundaries: `file selected → independent custody verified → ZIP/XML container bounded → cell types/date semantics parsed → source provenance mapped → owner/Record ID checked → explicit review → atomic local commit → native readback → separately authorized Manual Sync/remote receipt`. Each arrow has an independent failure oracle. Hash equality proves bytes, not meaning or owner authority.

**SOURCE (reviewed 2026-10-12):**
- OWASP file-upload guidance: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html — extensions/MIME do not suffice; decompression/size/content controls.
- OWASP CSV injection: https://github.com/OWASP/www-community/blob/master/pages/attacks/CSV_Injection.md — formula-like untrusted text may be interpreted by spreadsheet applications; CSV quote/apostrophe mitigations may fail on save/reopen. **CSV rules do not specify OOXML typed-cell behavior.**
- Microsoft Excel external content: https://support.microsoft.com/en-us/office/security-privacy/block-or-unblock-external-content-in-office-documents — workbook links/images/connections can create privacy and integrity risks; app/user policy matters.
- Microsoft Excel date systems: https://support.microsoft.com/en-us/excel/date-systems-in-excel — 1900 vs 1904 serial dates differ by **1,462 days**.
- W3C Web Share: https://www.w3.org/TR/web-share/ — resolved share promise does not prove recipient persistence. Apple Managed Open In: https://support.apple.com/guide/deployment/manage-organizational-data-depaa73a4973/web ; managed Safari domains: https://support.apple.com/guide/deployment/domains-payload-settings-depb4c146c2e/web . Safari-managed downloads are documented; Home Screen/Web Clip generated-file policy remains device-specific OPEN.
- W3C File API https://www.w3.org/TR/FileAPI/ and Service Workers https://www.w3.org/TR/service-workers/ — origin storage, OPFS, downloaded files, browser cache and recipient storage are independent planes.

## SOURCE — exact product boundary

`docs/specs/import-contract.md` (blob `2b7c2871`) explicitly states **no import parser, reconciliation repository, production export or import UI is implemented**. Intended import is optional, local/on-device, staged and user-confirmed; no raw source-file upload merely for parsing. `lib/screens/settings_screen.dart` (blob `4affdb26`) displays Import with inert `onTap: () {}`. `pubspec.yaml` (blob `6f4844c1`) does not declare dedicated picker/XLSX/share dependencies; this observation alone does not prove absence of every alternate implementation. The import contract preserves raw Jeju Air `fltNo`, limits leading-zero display normalization to `7C`, distinguishes calculated Ramp In from imported Ramp In, forbids inventing Takeoff/Landing clocks from Actual duration, keeps `instTme` distinct from IFR/Actual Instrument, and requires review for ambiguous records. Planned workbook sheets are `Logbook`, `Field Definitions`, `Instructions`; exact schema/Custom ID handling remains OPEN.

Historical `docs/evidence/stage-3-sync-ready-storage-audit-2026-10-08.md` records explicit **Manual Sync**, not startup/resume/network-triggered automatic Sync; it is not current runtime proof. Canonical Web Manager 320–324 already owns release/Worker/Auth/Hosting gates; local 327/330 owns custody and MDM. This artifact fills the distinct *untrusted import and semantic admission* boundary. Design Studio W120/W121 prioritizes exact runtime evidence; Engineering S007 owns identity, M006 owns native/PWA runtime; Marketing owns external claims.

## SYNTHESIS — six proof planes

| Plane | Required oracle | Fail-closed counterexample |
|---|---|---|
| F1 independent custody | destination byte hash and reopen after source-origin loss | Share Sheet closed, no receiver file; MDM blocked |
| F2 hostile container | bounded ZIP/XML, duplicate/path, external relationship/macro checks | valid extension conceals zip bomb or external content |
| F3 spreadsheet interpretation | formula vs typed literal, 1900/1904, zeroes, minute precision | date shifted 1,462 days; formula executed; Record ID coerced |
| F4 domain provenance | raw/source locator, approved known/custom mapping, unresolved review | `instTme` silently mapped to IFR; inferred Night or PF/PM |
| F5 owner/record admission | UID/Record ID, explicit diff, atomic commit and rollback | foreign UID or ambiguous match overwrites manual record |
| F6 native/remote continuation | receiver commits/readbacks; separately initiated Sync and server receipt | share resolved or request sent but durable outcome UNKNOWN |

**MINTTAP DIRECTION (conditional):** Keep public/import/export/backup/native handoff claims on HOLD until implemented and independently executed. Prefer a typed, versioned, owner-bound portable recovery archive for irreplaceable records; treat editable XLSX as a separately validated interchange projection unless its schema preserves revisions, tombstones, custom definitions, evidence and authority. No company-managed→personal AirDrop/Files recommendation without exact MDM permission.

## VALIDATION — lab only; product OPEN

A local Python standard-library diagnostic `pwa_ooxml_preflight_lab_20261012.py` created in-memory OOXML-like ZIP/XML fixtures and matched **17/17** expected container classifications (malformed ZIP/XML, traversal, duplicates, expanded-size/ratio, DTD, formula cell, external relationship, macro/external-link part, hidden sheet, 1904 date flag, literal formula-looking text). It is **NOT** an ISO/IEC 29500 parser, real Excel workbook test, Dart implementation or safe-import validator. Lab size/ratio thresholds are illustrative and can reject legitimate files. A benign fixture returns `CONTAINER_PREFLIGHT_ONLY`, never product PASS.

**OPEN executable matrix (28 cases, none executed):** T01–04 Safari/Home Screen/Web Clip acquisition, managed destination, cancel and independent hash; T05–08 ZIP bomb/path/duplicate/external/macro/malformed XML; T09–12 typed text vs formula after Excel/Numbers save/reopen, 1900/1904, leading-zero/large IDs and minute precision; T13–16 `7C` raw/display, missing Ramp In/Actual-only endpoints, `instTme` semantics, Custom stable identity; T17–20 foreign UID, duplicate Record ID, ambiguous match, manual edit protection; T21–24 interrupted commit, duplicate reimport, origin destruction/independent restore, native receiver + Manual Sync receipt; T25–28 accessible preview/errors, privacy-redacted evidence, offline restart and support handoff.

Each executed packet needs source/build/schema hash, browser/OS/install/MDM class, fixture digest, owner alias, before/after record+revision identities, UI/a11y state, receiver result, rollback and remote receipt. Synthetic PASS cannot close these cases. **Production validation OPEN.**

## TRANSFER / DEPENDENCY / CHANGE WATCH

A → E/C: File/Share/origin behavior does not establish managed-policy or recipient durability. E → B: distinct selected/parsing/review/committed/export-verified/receiver-accepted/remote-ACK states. E → C: adversarial real XLSX, interrupted transaction, physical iPad, accessibility. E → D/Marketing: no capability promotion and no raw workbook/owner data in analytics. Engineering must finalize versioned parser, owner-bound schema and conflict policy. **CHANGE WATCH:** Microsoft/Apple/WebKit/browser file capabilities, managed domain policies, OWASP mitigations, ZIP/XML library behavior. No Stage 8 production gate changed.

**Next meaningful checkpoint:** Engineering current-head normal PWA artifact + disposable versioned workbook/import/export fixtures + actual MDM policy, followed by T01–T28. Prior adjacent custody gap is now integrated; further generic synthetic cases do not establish product acceptance.
