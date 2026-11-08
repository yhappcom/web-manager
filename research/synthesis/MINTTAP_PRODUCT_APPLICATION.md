# MintTap Product Application — company website and LogMate EFB transfer

**Snapshot:** 2026-11-07 KST. **Classification:** evidence-bound product *requirements and evaluation*, **not** a new MintTap policy approval, public website release, LogMate code modification or provider-console fact. Current Web Manager base `4f5903f411b8c3a353ea4edb552c7bea6c4a2e33`. Product authority: [LogMate MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) and its current approved spec; Web Manager may only read product/peer sources. Consult [Web Master](WEB_KNOWLEDGE_MASTER.md), [PWA Master](PWA_ARCHITECTURE_MASTER.md), [Evidence Register](EVIDENCE_VALIDATION_REGISTER.md), [open queue](RESEARCH_GAPS_AND_SCHEDULE.md).

## 1. Scope, customers and material uncertainty

MintTap develops Apple/Android apps and owns `minttap.app`. The website must work as a reliable company and app-support/governance surface, not merely a landing image. A LogMate-like product also needs an offline-first tablet PWA route where a company EFB iPad may restrict ordinary App Store installation. **These are project requirements/constraints, not proof of published website pages or approved managed-device features.**

Research [001](../001-app-launch-website-foundations.md), [002](../002-multi-app-information-architecture.md), [003](../003-privacy-support-account-deletion-architecture.md), [004](../004-store-website-content-synchronization.md) and [077](../077-stage10-app-company-web-portfolio-lifecycle-strategy.md) are the foundational company resources. Do **not** infer current live pages, HTTPS behavior, app availability, market geography, legal status, analytics consent, PWA distribution permission or advertising status from a URL or from this research.

## 2. Intended company/site resource model [MINTTAP DIRECTION]

| Resource / candidate path | Visitor task | Canonical facts / release proof |
| --- | --- | --- |
| `/` | Discover company, app portfolio and credibility | Legal developer identity, actual published apps and current contact |
| `/apps/` | Compare specific published products | Product Truth Records and store versions |
| `/apps/<slug>/` | Evaluate capabilities and act | Truthful screenshots/build/locale/platform availability and App Store/Play destination |
| `/apps/<slug>/support/` | Solve problems, obtain contact/status | Actual operational support route and app-supported recovery behaviors |
| `/apps/<slug>/privacy/` | Understand specific data use | Actual App Data Contract plus App Privacy/Data safety and effective date |
| `/apps/<slug>/account-deletion/` | Initiate/request and understand deletion | Real in-app/external request routes, authentication, remote/local status and retention exceptions |
| `/privacy/` | Understand **website** processing | Website services/cookies/analytics/processors independently from app data |
| `/.well-known/apple-app-site-association` and `/.well-known/assetlinks.json` | Verify native↔web link association | Correct exact host/path, 200/MIME, signing/bundle/package identities, no inappropriate redirects |

**OPEN:** Paths are a proposed durable architecture, not verified deployed URLs. Domain/hosting and AASA/assetlinks decisions are staged [005 requirements](../005-domain-hosting-security-baseline.md), not proof of a selected/live hosting stack. If no account creation exists for an app, evaluate deletion link policy from its exact product/account state rather than copying another app's page blindly.

## 3. Channel truth and version traceability

The [Product Truth Record](../004-store-website-content-synchronization.md) is upstream of web copy, Store metadata, screenshots, feature claims and support instructions. It must identify app/bundle/package, current served/shipped build, capability and locale, account requirements, offline/Sync/backup caveats, privacy/data processors, proof source, owner and review date. A change in product source, live version, Store claim or privacy practice invalidates relevant dependent copy until reconciled.

**Cross-channel distinction:** A short Store value statement and a longer product page can phrase the same truth differently, but may not assert contradictory product capability. “Offline first,” “syncs automatically,” “backed up,” “account deleted everywhere,” “PWA supported on company iPad,” “ad-free while offline,” and “privacy compliant” are independently falsifiable claims, **not promotional defaults**. Consent/advertising and Play Financial features specifics remain Marketing's operational HOLD until operator-side evidence is supplied; Web D owns webpage/search/measurement implementation, not monetization policy.

**Screenshot and policy provenance:** Record exact device/build/source/locale/screenshot origin, user-visible feature, policy checked date, revision and retirement. Do not show a proposed or harness-only UI as the released app without explicit labeling. Do not invent conversion statistics or trust badges.

## 4. LogMate-like EFB transfer: what is known and unknown

**PRODUCT SOURCE:** The inspected [LogMate MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) specifies account-required Firebase UID ownership, explicit **Manual Sync** (rather than background/automatic payload transfer), local-first records, and a voluntary-account-deletion saga with local access lockdown. The Manual Sync contract is **approved direction**, not proof that product Sync/backend has shipped. The MASTER itself has historical implementation timestamps; re-pin HEAD/build for any current product decision.

| Product/OS question | Known researched boundary | Must verify before claiming support |
| --- | --- | --- |
| Company iPad without Store | WebKit Home Screen and managed Web Clip are potential but distinct routes | EFB MDM permission, approved URL/origin, install/container mode and company rules |
| Offline flight recording | SW/CacheStorage may serve shell; IndexedDB can store local ledger | NORMAL build cold offline, **all** owner data intact after relaunch/low quota |
| Native↔PWA transfer | Independent native and web storage/replica identity; Manual Sync policy | Actual permissible connectivity, explicit operator action, server/peer trust, receipt/ACK and conflicts |
| Background tasks | No universal WebKit/MDM promise | Feature-, installed-mode-, power-, network- and policy-specific evidence |
| PWA updates | Worker lifecycle separate from shell/data state | V1/V2 old-tab, cache integrity/repair and schema/owner compatibility |
| PWA backup | Origin persistence not an independent copy | User-allowed Files egress, saved LBK, fresh-context readback/restore, owner authority |
| Account deletion | [529 §96](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) shows **37 export stores/29 explicit wipe stores** at its pinned updated source | Populated 37-store deletion, stale-tab writer fence, remote receipt, A→B normal startup |
| Public deletion guidance | Pinned [523 §21](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) finds mismatch between public Settings deletion instruction and inspected actual UI | Current served page, current UI, operator request/retry/status path |

**Critical safety boundary:** Even if a managed iPad allows Home Screen web apps, it does not establish the airline permits persistence, background communication, hotspot use, file export or any radio/peer link on a flight deck. Neither an iOS simulator nor a synthetic Chrome run resolves company-specific rules. Use test-owned, disposable devices and synthetic ledger data; never run deletion/quota/profile-removal destructive probes on operational crew EFBs.

## 5. Five-track acceptance and external specialists

| Track | Website duty | EFB duty | Handoff |
| --- | --- | --- | --- |
| **A** | HTTPS origin, URL, links, caching mechanics | Safari/Chrome installed scope, SW/IDB, storage partitions | E/C/Engineering |
| **B** | Company→app→support/privacy task structure, readable policies | Offline-ready, update pending, backup verified, deletion pending and recovery task states | Design Studio W121 |
| **C** | Semantic/keyboard/AT, reflow, Core Web Vitals source-qualified quality | Exact served build/physical managed iPad performance, crash, quota, accessible error recovery | Design Studio W121; Engineering |
| **D** | Canonicals, social/search/Store continuity, consent-aware measurements | No unsupported PWA/offline/device claims; privacy-safe product conversion measurement | Marketing D1/D2/D8 |
| **E** | Hosting/security headers, incident/deploy rollback and true external deletion URL | Owner erasure, cross-origin trust, data custody, backup/Sync release evidence | Engineering S007, product owner |

**Canonical peer evidence:** [Design Studio WEB_STATUS](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) Stage 3 PRACTICE / execution priority W121; [Marketing STATUS](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) distinct launch/ads/claims HOLD; [Engineering S007](https://github.com/yhappcom/software-engineering-studio/blob/main/research/systems/S007_account_deletion_reauthentication_revocation_saga.md) requires immediate normal local access revocation and full local owner-data deletion. Those peer statuses are not interchangeable with Web Manager curriculum PASS.

### Auth/public-support compatibility transfer — 2026-11-07

**SOURCE / PRODUCT AUTHORITY:** LogMate's [MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) approves identifier-first Email lookup, not a new website account-discovery API. The current app [lookup source](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/lib/auth/email_account_lookup.dart) relies on Firebase `createAuthUri.registered`, while [Google enumeration protection](https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection) recommends not depending on enumeration-sensitive behavior. **OPEN:** actual provider setting, safe response and abuse controls, accessible fallback. The proposed MintTap support/account-deletion pages must remain available when in-app Email lookup is unavailable; public pages must not infer UID/account existence from a typed lookup failure or claim delivery of a reset/deletion request merely from UI acknowledgement. Engineering owns Auth/S007 and console evidence; Web E/B owns secure, truthful independent support/deletion route; C/Design Studio owns accessible retry; D/Marketing owns claims. Detailed [PWA Master §11](PWA_ARCHITECTURE_MASTER.md) and [EV22](EVIDENCE_VALIDATION_REGISTER.md). **No website implementation or product policy change is authorized.**

## 6. Prelaunch site/release readiness contract (future, NOT RUN)

1. **Identity/content:** verified company developer/legal identity, contact, apps and exact version; page and Store truth matrix including locale and screenshots.
2. **Support/privacy/deletion:** real reachable routes and request handling, current App Data Contract, permitted retention and accurate local vs remote deletion states; handle failed/retry states accessibly.
3. **Transport/security:** inspect real HTTPS certificates, canonical redirects, route-specific `Referrer-Policy`/CSP and asset links, OAuth callback, SW scope, escaped telemetry fields, safe deployment/rollback.
4. **UX/accessibility:** desktop/mobile/tablet, light/dark where product applies, keyboard/AT/zoom/reflow/slow/failure UX; Design Studio W121 evidence and representative users.
5. **Discovery/measurement:** URL/index/canonical and Store handoff; use consent-safe events with test and real-field provenance. Avoid fabricated traffic/performance success.
6. **PWA/EFB:** close all P0 owner/Files hazards and in-scope P1 NORMAL/browser/physical managed-EFB oracles before any “safe offline flight logbook / supported EFB” claim.
7. **Operations:** owner for policy/claims, change watch, incident response, restore test, artifact/served-version tracking, accessible support and release rollback.

**PROJECT DECISION boundary:** This file records candidate requirements and no actual launch approval; owners must explicitly decide provider, app-specific published routes, release scope and acceptable residual risks. See [open decisions and work protocol](RESEARCH_GAPS_AND_SCHEDULE.md).
## 7. Product-source-pinned backup handoff — approved .lbk before speculative encryption (2026-11-08)

**New evidence class S — product source directly inspected, no runtime execution.** Read-only inspection of LogMate \`main\` [MASTER.md](https://github.com/yhappcom/logmate/blob/main/MASTER.md), blob \`5a6fd944abf24a95efed3b4a31db214d2e24a662\`, and [approved local-first Manual Sync contract](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md), blob \`97faecf317df1346f4b1b58c8d37c891f805e436\`, provides a more authoritative product answer than the generic encryption threat model in [PWA Master §36](PWA_ARCHITECTURE_MASTER.md). The inspected contract §§2, 4 and 7 approves **structured whole-ledger \`.lbk\` export/import first** for device transfer, followed by explicit Firebase delta Manual Sync; optional cloud full backup is separate. CSV/Excel/PDF are not whole-ledger backup. The contract explicitly calls for communicating file sensitivity, permissions/protection and **encryption choice**, but does **not** select a cipher, key-custody scheme, password KDF or mandatory encryption envelope. Its final state marks implementation/full backup/P2P/production deployment **NOT IMPLEMENTED/NOT VERIFIED** at the contract checkpoint. MASTER reports bounded F1 format-v1 reader and Sync-aware v2 restore/local-replica foundations, not production full-backup/Manual Sync closure. **Do not infer that current \`.lbk\` is encrypted, plaintext, fully portable, complete, or currently restorable in a fresh EFB environment from these source statements alone.**

**Reconciled authority and dependency:** §36 is a conditional *if encrypted backups are chosen* threat model, not a recommendation that the approved product has already chosen encryption. Engineering/product must first identify the exact current export writer, format reader, file envelope, canonical record inventory, UID/replica/epoch binding and currently available user-facing route on the relevant HEAD/build. The product owner must explicitly choose confidentiality and recovery policy with an operator-allowed Files flow before a crypto architecture is promoted. Existing LogMate rules about Manual Sync, old-backup tombstone non-resurrection, no silent Replace/Merge on a populated destination, wrong-UID/unknown-schema rejection and destination replica preservation remain governing constraints; a cryptographic checksum cannot override them. If no portable key is approved, do not add an origin-only CryptoKey dependency to the primary offline device-transfer path by default.

### 7.1 Transfer sequence and falsifiable custody levels

| Gate | Evidence needed | Prohibited inference |
| --- | --- | --- |
| P0 source authority | Exact LogMate HEAD, approved \`.lbk\` contract, actual writer/reader source SHA | A written contract means the current app shipped it |
| P1 export inventory | Disposable complete owner-ledger snapshot, format/schema/record count, all relevant stores/lineage | A CSV/PDF export or one restored Flight is whole-ledger backup |
| P2 independent file | User-selected Files destination; reopen exact bytes/hash from independent container after process exit | Download toast, Web Share success, origin-held Blob, File picker invocation |
| P3 fresh-context restore | Independent iPad/PWA/native replica, supported codec, explicit owner authorization, UID/epoch/replica rules, zero-write negative controls | Matching login, valid hash or successful decrypt alone authorizes import |
| P4 cold readback | Restart after committed restore; complete ledger, custom definitions/values, config, order, baseline, revision, tombstones, outbox/Sync recovery holds and 37-store audit where applicable | UI success or partial visible records proves all state |
| P5 optional Manual Sync | User-initiated authenticated push/pull/apply and owner-specific durable receipt; conflict/duplicate/ACK-loss tests | Restore implies server replica convergence or unattended EFB sync |

**EFB admission and privacy:** On a managed iPad, obtain device-operator permission for Files export/reopen and use synthetic flights only. Browser tab, Home Screen and managed Web Clip are distinct environments; an ordinary Safari success cannot authorize a Web Clip claim. Never test destructive storage deletion, account deletion or key loss on operational crew EFBs. Before offering "backup complete" or "ready on new device," B/C/Design W121 must use the highest independently observed P-stage, and D/Marketing must avoid claims of encryption or background sync without product and operator evidence. **Public website** should explain user custody and support paths accurately without publishing raw ledger or token-bearing URLs.

### 7.2 Decision/contradiction and test bundle — LB01–LB24 (DEFINED NOT RUN)

**Product source and policy (E/Engineering):** LB01 pin exact HEAD/build, approved \`.lbk\` spec and current source paths; LB02 enumerate actual writer/reader, format versions, encoding and cipher presence/absence; LB03 compare exported record kinds and 37-store inventory to current authoritative registry; LB04 map owner/UID, replica ID, schema and epoch validation; LB05 compare old backup timestamp/operation lineage with tombstone rules; LB06 confirm whether user/operator has approved an encryption and recovery-key policy; LB07 verify current native vs Web import/export entry points and disabled routes; LB08 prove no implicit cloud/full backup or auto-sync claim.

**Cross-context durability and security (A/E/C):** LB09 Files export cancel versus verified independent save; LB10 byte/hash reopen after browser process termination; LB11 new Safari tab/Home Screen/MDM Web Clip distinct-container import; LB12 native phone independent replica restore; LB13 wrong UID, deleted owner/epoch and unknown schema zero-write; LB14 malformed/truncated/oversized file zero-write; LB15 duplicate and older backup cannot silently overwrite new work or resurrect tombstones; LB16 local replica identity preserved and foreign cursor/ACK treated as hold; LB17 all stores, custom fields/config/baseline/order/tombstones/outbox cold readback; LB18 restart/kill during restore with rollback/no partial mutation; LB19 key loss and portable-secret recovery **only if encryption is actually adopted**; LB20 no allowed Files channel → honest unsupported/fallback status, not a fabricated recovery.

**UX/discovery/ops (B/C/D):** LB21 truthful export/save/verify/restore status and keyboard/VoiceOver focus; LB22 website/Store wording and consent-safe diagnostics avoid "encrypted," "backed up" or "auto synced" without evidence; LB23 user-help instructions differentiate Files custody, local browser data and Firebase Manual Sync; LB24 source-pinned operator-approved dry run with failure-injection report, exact OS/browser/MDM/build and independent negative controls.

**Five-track transfer:** E owns actual web custody/security admission and coordinates Engineering/product; A owns WebKit/Chromium container/Files mechanics; C owns independent negative controls and accessibility test execution; B owns recovery/first-device/new-device information architecture with Design W121; D owns support/search/Store claims with Marketing D9/D10. **No product or peer files modified.** **OPEN:** writer/reader exact code path, file contents and cipher, full inventory, operator Files permissions, actual device execution, full sync. **MINTTAP DECISION:** prioritize existing approved \`.lbk\` transfer contract and obtain exact implementation evidence before any new crypto or PWA feature selection. **VALIDATION:** LB01–LB24 defined, not run. **Gate unchanged:** applied Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD.

