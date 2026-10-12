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


## 2026-10-12 integrated continuation — OPC graph, browser injection sinks and evidence promotion

**Canonical update scope:** 2026-10-12, latest verified `main@14a691eab40775e84bf3aca3f2960e0bf41bb67f` before this update. This section integrates the noncanonical 327/329/330/331/332 study family into the existing 328 domain artifact, rather than promoting each small local report to a separate canonical study. Original 328 source-bounded conclusions remain valid. **Owner: Track E** (hostile-data admission, owner authority, rollback, custody); A owns browser/Service Worker/DOM and storage mechanics; B consumes truthful user task-state and recovery contracts; C owns independent execution/negative oracles; D owns privacy-minimized capability/incident measurement. Web Manager coordinates, not a sixth track.

### SOURCE — primary platform and security evidence (reviewed 2026-10-12)

- ECMA-376 Office Open XML / OPC: https://ecma-international.org/publications-and-standards/standards/ecma-376/ ; Microsoft Open XML package/relationship reference: https://learn.microsoft.com/en-us/office/open-xml/general/how-to-get-the-contents-of-a-document-part-from-a-package . A ZIP member being readable does **not** prove a valid OPC relationship graph, sheet binding or semantic workbook.
- OWASP File Upload: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html ; OWASP DOM XSS: https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html ; OWASP Cross Site Scripting Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html . Hostile workbook strings remain untrusted after parsing and storage.
- W3C Trusted Types: https://www.w3.org/TR/trusted-types/ ; W3C CSP: https://www.w3.org/TR/CSP3/ ; MDN `require-trusted-types-for`: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for . Trusted Types restrict selected script-capable DOM injection sinks when supported and enforced; they do **not** validate workbook semantics, authorize data mutations, or eliminate all script-execution paths.
- **CHANGE WATCH correction:** WebKit explicitly introduced Trusted Types in **Safari 26.0**: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ . Safari **26.4** notes fixes for Trusted Types CSP violation reporting and DOM-attribute processing: https://webkit.org/blog/17862/webkit-features-for-safari-26-4/ (2026-03-24). Therefore the older generalization "Safari does not support Trusted Types" is stale for current Safari; it remains necessary to test the *exact* installed iPadOS/WebKit version, enforcement mode, specific sink and reporting behavior. MDN marks the directive Baseline 2026; this does not establish managed Web Clip behavior.
- W3C Service Workers: https://www.w3.org/TR/service-workers/ ; Apple managed data/Open In: https://support.apple.com/guide/deployment/manage-organizational-data-depaa73a4973/web . Origin script trust, cached assets, managed file destinations and native receiver durability are distinct boundaries.

### HISTORY → PRINCIPLE → STANDARD → IMPLEMENTATION → FAILURE → OPERATIONAL JUDGMENT

**Problem evolution:** A spreadsheet is both a document and an executable-capable interchange format. The ZIP container, OPC relationships, cell value types, formula/external-content features and application render/export paths are distinct trust boundaries. Client-only parsing avoids an unnecessary server upload but does not turn attacker-supplied bytes into trusted same-origin application content.

**Browser-origin escalation chain to falsify:** `untrusted XLSX → parsed text → persisted local ledger → unsafe HTML/URL/DOM sink → same-origin script execution → available in-origin data, Auth/session state and Service Worker registration interfaces`. A successful injection is **not** demonstrated in LogMate; this is a threat hypothesis. The opposite failure also matters: overbroad escaping or type coercion may destroy flight-number, date, Custom ID and source-provenance meaning. Defense must be context-sensitive and preserve the raw source separately from the displayed value.

**Layered gate:** (1) file custody and MDM destination policy; (2) bounded ZIP/OPC structural preflight, no external/macros/unknown active features; (3) workbook/cell semantics, text ID preservation and formula handling; (4) immutable source provenance and stable domain identity; (5) safe render in every review/detail/export surface; (6) explicit owner-bound preview and conflict resolution; (7) atomic local commit and crash recovery; (8) independent recipient readback/restore; (9) separately authenticated Manual Sync and authoritative remote receipt. Passing an earlier layer never substitutes for a later layer.

**Concrete browser controls:** Use text-only DOM APIs/framework text widgets for untrusted labels; never treat imported rich text, comments, hyperlinks, formulas or custom labels as preapproved HTML/JS/URL. Validate any actual navigation scheme/destination before creating links. Inventory DOM sinks in generated bundles/plugins/HTML interop, including error/preview/print/export paths. A restrictive CSP plus Trusted Types is defense-in-depth **only after** confirming Flutter-generated bootstrap, Firebase Auth helpers, `/__` reserved routes, service-worker scope and third-party integration compatibility. Do not deploy `require-trusted-types-for` blindly as a "security fix": an incompatible bootstrap can make an offline app unusable. Start with a source-pinned inventory and a separately validated report-only/canary plan where applicable, then enforce only with real-browser positive and negative oracles. Never send raw workbook cells, UID, token or logbook content in CSP violation reports or analytics.

**Service Worker trust:** An SW intercepting an authenticated or sensitive path is a privileged origin component, not a file validator. LogMate's source `tool/precache_flutter_web.dart` patches generated worker cache behavior by string replacement; `tool/verify_pwa_artifact.dart` verifies presence/markers/fonts but does not execute navigation, auth-helper isolation, malicious-import rendering or data migration. `firebase.json` retains a catch-all `** → /index.html` rewrite; `web/manifest.json` lacks `share_target`; `settings_screen.dart` has an inert Import action; `docs/specs/import-contract.md` explicitly says import/export are unimplemented. These are exact-source observations, **not** proof of deployed vulnerabilities or operational incidents. A normal successful build, exact served bytes and browser/managed-iPad behavior remain OPEN.

### VALIDATION — reproducible local synthetic evidence, no product promotion

The read-only local research labs were re-executed on 2026-10-12:
- `pwa_ooxml_preflight_lab_20261012_v2.py`: **31/31 expected classifications PASS**. Added OPC case-insensitive identity/invalid-part-name and corrupt-member CRC cases to the earlier 20-case baseline.
- `pwa_opc_relationship_graph_audit_20261012.py`: **9/9 expected classifications PASS**. The narrow graph model finds seven cases accepted as container-only by the ZIP preflight (content-type/relationship/sheet graph failures); external relationship is rejected by both; one benign case is the control. This is a *counterexample to treating ZIP preflight as workbook validity*, not a general OOXML validator.
- An attempt to launch a local Chromium 144 Playwright fixture was **blocked by the execution environment (`net::ERR_BLOCKED_BY_ADMINISTRATOR`) before the test page loaded**. No browser CSP/Trusted Types execution PASS or FAIL is claimed.

**C's next executable acceptance packet (none executed against LogMate):**
| Group | Independent positive/negative oracle | Owner |
|---|---|---|
| P1 exact artifact | Pin build toolchain, commit, artifact digest, served bytes; prove no forbidden Auth/asset rewrite and safe SW navigation scope | A/E/C |
| P2 browser injection | In Chrome, Firefox and exact Safari/iPadOS versions, display malicious-looking text as inert literal; confirm unsafe sink fails under actual enforced policy without breaking valid UI | A/C |
| P3 import semantics | Real Excel/Numbers files: shared strings, typed formulas vs literal text, 1900/1904, large/leading-zero IDs, custom fields and source clocks; save/reopen round-trip | E/C |
| P4 owner/transaction | Foreign UID, ambiguous match, manual edit conflict, duplicate import, interruption, restart; prove no partial or unauthorized local commit | E/C/B |
| P5 offline/install | Safari tab vs Home Screen vs managed Web Clip: offline reopen, data persistence, worker update, storage-pressure recovery and user-visible states | A/B/C/E |
| P6 portable custody | Managed file destination, clipboard/share restrictions, independent byte hash, origin loss and recipient/native readback; do not infer from share-promise resolution | E/C |
| P7 Sync | Foreground retry, unknown ACK, stale authority, server receipt, conflict/convergence; do not infer direct device-to-device or unattended background sync | E/C |
| P8 accessibility/privacy | Screen reader/keyboard/zoom/IME on preview and recovery; event/redaction audit and report-body inspection | B/C/D |

**Evidence levels:** SOURCE and SYNTHESIS are closed for the bounded generic mechanisms; synthetic classifier checks are model-only. No real workbook, deployed LogMate Import/Export, exact browser CSP enforcement, physical managed iPad, native recipient, restored ledger or remote Sync PASS exists here. Product and production validation **OPEN**.

### Five-track allocation and transfer/contradiction

| Track | Current bottleneck / evidence maturity | Work disposition |
|---|---|---|
| **E** | Highest consequence: untrusted import → owner-bound local commit → portable recovery → current remote authority; SOURCE/model strong, real implementation absent | Own this integrated gate and risk/rollback/incident criteria |
| **A** | Platform prerequisite: origin/scope, SW control, DOM/Trusted Types, browser file/storage/MDM differences; generic evidence strong, exact WebKit/runtime absent | Supply browser-specific constraints and change-watch |
| **C** | Highest execution debt: synthetic/CI green is not an independent browser/physical-device/restore oracle | Own P1–P8 execution and failure-first evidence |
| **B** | UI truth debt: selected/parsed/reviewable/local-committed/export-verified/receiver-readback/remote-ACK must not collapse into one "Success" | Transfer to Design Studio W120/W121 and Content/Interaction |
| **D** | Evidence/claim debt: install/acquisition measurement cannot infer offline durability, native handoff or sync; telemetry must exclude raw private records | Hold external capability claims and define redacted evidence |

**TRANSFER VALIDATION:** Design Studio `progress/WEB_STATUS.md` says W121 remains Stage 3 PRACTICE / NOT PASSED and requires exact execution; it does not supply physical PWA/AT/UX PASS. Software Engineering `progress/MOBILE_STATUS.md` M006 provides bounded macOS Safari SW registration/update/restart evidence but reports fresh-WebDriver offline cold-start contradiction; it is not iPad or LogMate evidence. Engineering S007 identity contract and LogMate product import contract govern UID/review semantics; this study does not rewrite engineering's implementation. Marketing's public capability claims remain dependent on independently executed release evidence.

**CONTRADICTION:** A preflight "CONTAINER_PREFLIGHT_ONLY" result is not workbook acceptance; a share-promise resolution is not backup; a browser API existing is not permission or MDM approval; Trusted Types support in Safari 26+ is not evidence that an installed PWA is protected by a particular CSP; and a normal build passing marker checks is not offline, Auth or data-durability validation.

**MINTTAP DECISION (conditional):** Keep product import/export/backup/native-handoff and managed-iPad offline/sync claims on **HOLD** until exact-product runtime evidence clears their independent gates. Preserve unique local records and provenance during failure; do not recommend destructive clear-site-data/cache reset as routine repair. A typed, versioned owner-bound portable recovery archive is the preferred *design direction*, not a shipped capability.

**OPEN / DEPENDENCY:** Need Engineering normal current-head PWA build + exact deployed response headers, real parser/exporter and import fixture corpus, Auth/Sync acceptance backend, exact managed iPadOS/MDM policy, native recipient and independent restore target. **CHANGE WATCH:** WebKit Trusted Types implementation/bugs, Safari 27 and managed contexts, Firefox/Chromium enforcement, Flutter generated bootstrap, Firebase Hosting/Auth reserved routing, OOXML parser dependencies, Apple managed data policies. **Next major target:** evidence-bearing exact-artifact browser/MDM/restore execution, not another narrow synthetic OOXML micro-test.

**Stop-check:** The adjacent high-value source question (Trusted Types availability in Safari and its relevance to imported-data rendering) was resolved from primary WebKit/W3C/OWASP evidence. Further product gate closure requires materially different exact artifact/physical-device evidence. Do not promote generic checks to production PASS.
