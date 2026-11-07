# 531 — MintTap Web Manager Integrated Knowledge, Evidence, Decisions and Research Operating Master

**Consolidation checkpoint:** 2026-11-07 KST. **Original consolidation baseline:** `yhappcom/web-manager` `main@4f5903f411b8c3a353ea4edb552c7bea6c4a2e33`. **Later integration:** five focused synthesis masters and roadmap correction on 2026-11-07 (see links below). This document is a historical synthesis, not a newer authoritative snapshot than current `STATUS.md`. **Authority:** this document is a navigational synthesis and operating control, **not** a replacement for the primary studies, product MASTER, standards, or execution logs. Historical studies remain intact. **Status:** CONSOLIDATED RESEARCH / Stage 8 applied security ACTIVE / product and physical managed-EFB validation OPEN / PWA release HOLD.

## 1. Scope, provenance and how to read this master

**SOURCE:** Reviewed `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, the latest Web Manager commits, studies [298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md), [523](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md), [528](528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md), [529](529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md), [530](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md); [Design Studio WEB_STATUS](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md); [Marketing STATUS](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md); [Engineering S007](https://github.com/yhappcom/software-engineering-studio/blob/main/research/systems/S007_account_deletion_reauthentication_revocation_saga.md); and [LogMate MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md). The Engineering root STATUS path was not found; S007 is the directly read Engineering authority for account deletion. Source-specific execution dates and SHAs remain in the cited primary studies. No product, Design Studio, Marketing, or Engineering repository was changed.

**Authority precedence:** (1) current product MASTER and approved contracts for *product policy*; (2) exact pinned source and runtime/CI evidence for *implementation facts*; (3) current standards/vendor documentation for *platform behavior*; (4) original Web Manager studies for evidence and analysis; (5) this master for *cross-study navigation and current interpretation*. A later source change invalidates any unqualified claim of current implementation. Distinguish **SOURCE** (observed/documented), **SYNTHESIS** (reasoned), **MINTTAP DECISION** (approved vs merely proposed), **VALIDATION** (exact executed vs designed), **OPEN**, **DEPENDENCY**, **TRANSFER VALIDATION**, **CONTRADICTION**, and **CHANGE WATCH**.

## 2. Consolidated competency map — five tracks, one coordinator

The sequential Stage 1–12 **curriculum competency gates are PASS** (studies 027–082; see [research index](README.md)). PWA foundation 073–074 also PASS. These are **knowledge gates, not product certification**. Stage 8 remains **ACTIVE** as a deeper *applied* security/privacy/trust specialization. Do not describe the whole curriculum as unfinished or the PWA product as ready.

| Track | Reusable knowledge owner | Evidence maturity / pressure | Current consumption / next transfer |
|---|---|---|---|
| **A — Platform & Browser** | Origin, HTTP/TLS, navigation, Service Worker lifecycle/fetch/control, Cache API vs HTTP cache, manifest/install identity, WebKit/Chromium differences, IndexedDB and storage persistence | Mature standards synthesis and some hosted Chrome execution; physical Safari/managed EFB OPEN | Explain exact browser partition/controller/old-client semantics to E/C; no unsupported install/background promises |
| **B — UX, IA & Content** | Company/app IA, product/support/privacy/deletion page structure, offline/install/update/restore state language, accessible recovery tasks | Conceptual structure mature; Design Studio W121 runtime interaction and representative user proof OPEN | Consume A/E state invariants; never display “offline ready”, “backup verified”, or “deletion complete” on weaker evidence |
| **C — Performance, Accessibility & Quality** | CWV/WCAG, offline performance, failure injection, CI provenance, device/browser acceptance, positive and negative controls | Synthetic and bounded historical CI PASS; current exact product/managed-iPad proof OPEN | Execute independently reproducible acceptance; keep non-execution, synthetic PASS, historic product PASS and current product PASS distinct |
| **D — Search, Discovery & Analytics** | Crawl/index, app↔website continuity, Store claims, analytics consent/provenance, privacy-safe measurement | Curriculum PASS; actual launch/account-side attribution and claims evidence OPEN | Consume B/E approved content and C execution, not reassert lab outcomes as product/marketing claims |
| **E — Architecture, Security & Operations** | Secure context, identity/owner boundaries, deletion saga, remote receipts, schema/update/rollback, backup/recovery custody, incident/release governance | **P0 bottleneck:** strong source and adversarial synthesis, missing exact populated-store product acceptance | Lead 37-store erasure, stale writer, A→B, Files restore, MDM release gates; Engineering S007 owns implementation |

**Allocation judgment:** E > A > C > B > D until P0 security custody is resolved. Allocate by risk and prerequisite pressure, not equal file counts. Web Manager coordinates and does not become a sixth specialist. No track repeats another track's primer; link to its source and record dependency/contradiction.

## 3. Company website knowledge and practical application

**SOURCE / SYNTHESIS:** Early 001–026 studies cover company/app launch obligations, multi-app IA, support/privacy/account deletion, Store↔site content synchronization, DNS/hosting/TLS/security headers, SEO, accessibility and operations. [002](002-multi-app-information-architecture.md), [003](003-privacy-support-account-deletion-architecture.md), [004](004-store-website-content-synchronization.md), [005](005-domain-hosting-security-baseline.md), [026](026-app-company-web-strategy-information-hierarchy.md) are starting points. The `minttap.app` company surface and per-app support/privacy/deletion responsibilities must be separable; suggested paths are **IA proposals**, not deployed URL assertions. Claims should trace to current product behavior and platform/store policies; app-company marketing, accessibility conformance and privacy compliance cannot be inferred from a document or mock.

**DEPENDENCY:** LogMate MASTER explicitly says production Manual Delta Sync is not implemented; the current approved product contract is **Manual Sync only**, not unattended auto-sync. It also identifies external deletion-request surface, actual deployment/reachability and remote adapters as unverified. This overrides earlier historical no-account/no-login proposals. Engineering owns the deletion coordinator, Web Manager the public web request/status semantics, Design Studio the interaction, Marketing the claims.

## 4. PWA cross-track master — eight non-equivalent state machines

**HISTORY → STANDARD → IMPLEMENTATION:** AppCache's opaque update behavior motivated programmable Service Workers, but programmable caching does not atomically upgrade a local-first ledger. Treat as separate:
1. HTTPS origin / installed app identity / manifest id / SW scope / storage partition;
2. first online render and successful registration;
3. worker installed, waiting, active, controller per client;
4. complete authenticated shell/resource Cache Storage and offline cold relaunch;
5. IndexedDB write success, quota, persistence mode, user/MDM removal and schema capability;
6. authenticated owner, offline authorization, account deletion and stale-client write fencing;
7. queued local change, server authenticated admission, receipt, client ACK and reconciliation;
8. external independent backup location, file readback, restore and post-restore owner/replica checks.

**CONTRADICTIONS resolved:** `updateViaCache:'none'` or `registration.update()` is *worker script update checking*, not Cache Storage freshness, activation, data migration or offline readiness [530 §§43–44](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md). `persisted()===true`, `estimate()`, committed IndexedDB and independently restored Files are **four distinct claims** [298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md), [530 §44](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md). Installed icon ≠ same container ≠ full offline shell ≠ unique offline data protected. Chrome PASS ≠ WebKit PASS ≠ managed iPad permission. Browser network availability ≠ authorized native↔PWA transport; current product policy rejects automatic payload Sync. Push/background, file egress, advertising and direct device-to-device capability are platform/version/MDM-specific **CHANGE WATCH**, never assumed.

**Primary platform sources to refresh at change:** [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/), [Safari 26 WebKit](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/), [MDN SW updateViaCache](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache), [MDN SW update](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update), [MDN SW lifecycle](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers), [MDN storage quotas](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria). These are source references, **not** claims of a fresh external check in this consolidation.

## 5. Evidence register — bounded achievements and unresolved product claims

| Evidence / provenance | Confirmed bounded result | Not proven |
|---|---|---|
| [523](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) Firebase Auth/Firestore emulator FE01–FE23 | Research-only **23/23 PASS** at pinned source | Deployed backend, real provider revocation, LogMate canonical wire/Apply |
| [523](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) hosted Chrome synthetic BP01–BP16 | **16/16 PASS**, including negative control | Product PWA, Safari, managed EFB |
| [521](521_stage8_pwa_sembast_cross_tab_replay_wasm_web_opener_admission_20261027.md) hosted Chrome independent tabs | 4/4 plus conditional TB03 observed PASS; exact raw-IDB oracle | Real owner authority or deployed product |
| [530 §41](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) historical LogMate CI run 41046987456 | Historical `114acad7...` PWA artifact workflow **success**, inventory verified | Current main served HTTPS, cold offline, iPad, owner deletion, Files |
| [530 §42](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) historical Chrome IndexedDB reopen | Bounded historical CI PASS | Managed device, current product, full recovery |
| [529 §§84–96](529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) current product static analysis | Registry **37 stores**, explicit terminal wipe **29**, 8 omitted; changed source blob rechecked 2026-11-03 | Populated omitted stores actually leaking, B accessing A, real user incident, product runtime FAIL |
| [298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md) W-012 Native restore | Bounded historical Native test evidence | Independent managed iPad Files restore, current Web |
| [529 WP01–WP20](529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md), [530 ST01–ST12](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) | Detailed acceptance **DEFINED** | **NOT RUN** |

**VALIDATION vocabulary:** `SOURCE STATIC`, `SYNTHETIC EXECUTED`, `HISTORICAL PRODUCT CI EXECUTED`, `CURRENT PRODUCT RUNTIME EXECUTED`, `PHYSICAL MANAGED DEVICE EXECUTED`, `DEFINED NOT RUN`, `NON-EXECUTION`. Every PASS needs commit, build hash, harness version, runtime/device, result, negative control and evidence URL. A build or test success never silently upgrades an unrelated claim.

## 6. P0 decision register and executable acceptance chain

**P0-1 — Account deletion parity [SOURCE / OPEN]:** [529 §96](529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) rechecked 30 base/37 combined stores and 29 explicit drops at a newer source blob; seven Sync stores and Replica store omitted. `ownerUid=null` reinitialization is not subordinate row deletion. No exact seeded 37-store product wipe has run. **Engineering S007 owns remediation and tests; Web Manager E owns web/MDM release implications.** Execute WP01–WP10 and WP15 with synthetic A/B data, full pre/post canary inventory, close/reopen, normal B startup, independent compiled-Web check. Preserve possible alternative policy decisions as **OPEN**, not approved fixes.

**P0-2 — Deletion races and remote authority [OPEN]:** Old tab may still have a writer; deletion state must be transaction-time fenced, not UI-only. Validate RW/RC interleavings, duplicate drivers, process crash, provider revocation, remote receipt and post-Auth deletion. Server admission/ACK and local receipt are separate; Emulator is not deployed service evidence [523](523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md). Avoid blanket `Clear-Site-Data` because it can destroy unrelated local data and external user-controlled recovery.

**P0-3 — Independent backup custody [OPEN]:** Verify a user-approved LBK export into an actually permitted external Files destination, independent fresh-context file readback and guarded restore with owner/replica checks. Do not call `persist()` a backup or count two files in one failure domain as independent.

**P1-1 — Exact two-version offline release [OPEN]:** [528](528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md), [530 §§35–44](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md): ordinary vs acceptance builds separately hashed; first paint vs SW control vs cache complete vs cold offline restart; V1/V2 waiting worker, interrupted downloads, stale tabs, schema compatibility, quota pressure, rollback. Release HOLD until exact source and served artifacts are validated.

**P1-2 — Physical company iPad [OPEN]:** [530 ST01–ST12](530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md): pin OS/Safari/MDM, distinguish Safari tab, Home Screen and managed Web Clip; test cold offline, storage eviction, profile removal only on disposable devices, Files egress, independent restore. No unattended native↔PWA sync or hotspot assumptions.

**P2 — Website launch and claims [OPEN]:** Verify live `minttap.app` routes, public deletion request/status, privacy/support, store claims, accessible states, real analytics/consent and release ops against actual served build. Design Studio [W121](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) remains Stage 3 practice, runtime evidence required. Marketing current D1/D2/D8 claims remain HOLD in their own domain; do not duplicate that research.

**Gate:** Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD. No release authorization, product mutation, or operational incident is inferred.

## 7. Research consolidation and hourly operating protocol

**MINTTAP RESEARCH OPERATING DIRECTION (proposed, not product policy):** Retain **hourly trigger cadence**, but make each execution **evidence-delta-driven, integrated and substantial**. Do not spawn more parallel Web Manager schedules or spend a run on one microquestion. Each run:
1. Read latest `main` and `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, **this master**, recent commits and relevant original studies. Check Design Studio/Engineering/Marketing only where transfer is material.
2. Compare exact source SHA, standards/platform change, new product/CI/device evidence, unresolved gate and cross-track pressure. Select one **highest-information-gain bottleneck** (E→A→C→B→D by default, re-rank when evidence changes).
3. Perform a **substantive integrated bundle** (several adjacent source checks, contradiction resolution, diagnostic exercise, failure matrix, acceptance/handoff) rather than a single shallow block. Continue until meaningful checkpoint or genuine evidence blocker; no filler.
4. Update **the owning integrated study or this master** only for new reusable knowledge, changed decision, newly executed proof, resolved contradiction or changed blocker. Link the source; do not append near-duplicate hourly notes to giant `STATUS.md`/`research/README.md`. Preserve raw studies.
5. Record `SOURCE / SYNTHESIS / MINTTAP DECISION / OPEN / DEPENDENCY / VALIDATION / CHANGE WATCH / TRANSFER VALIDATION / CONTRADICTION`; keep exact PASS provenance and a clear **NOT RUN** state. Do not modify LogMate, Design Studio, Marketing or Engineering.
6. Update `STATUS.md` **only on a meaningful gate, owner, priority or major-domain transition**; keep it a current-status gateway, not a per-run diary. Maintain index links when a new integrated artifact is created; avoid repeated historical prose.
7. Before stopping ask: *Can the next adjacent valuable question be resolved now using available authoritative evidence?* If yes continue; if only product/physical device evidence can close the gap, record a precise Engineering handoff and stop rather than speculate.
8. User-facing reporting only on gate change, new product/runtime evidence, important contradiction, critical blocker or substantive integration. Otherwise no repetitive progress announcement.

**Suggested run allocation (adaptive, not quotas):** 60–70% E/A PWA security/platform risk, 20–30% C exact validation and B recovery/accessible task transfer, remainder D/website/standards change watch. If P0 cannot advance without Engineering, do not endlessly repeat its static diagnosis: perform a distinct adjacent source or standards reconciliation, or pause that gate pending runtime proof.

**Review cadence:** Hourly trigger for fresh high-value evidence; weekly consolidated contradiction/priority review; monthly stage/domain audit and link integrity. These are review rhythms inside the existing task, **not new scheduled tasks**. No need to send hourly messages without material changes.

## 8. Research debt and contradiction watch

- **STATUS/index volume:** historically accumulated `STATUS.md` and `research/README.md` are large chronological ledgers. This master supplies a stable entry point; future maintenance may refactor the front-page current snapshot **without deleting primary evidence**. Avoid wholesale rewrite during concurrent automation.
- **Roadmap stale position — RESOLVED 2026-11-07:** `LEARNING_ROADMAP.md` tail was corrected in commit [`c275785`](https://github.com/yhappcom/web-manager/commit/c275785be18c944a9e2c28f2b0f85c98b0dbe81f). It now explicitly records Stage 1–12 competency PASS and applied Stage 8 ACTIVE; do not continue treating this as unresolved debt.
- **Historical vs current product:** exact artifact hashes and SHA matter. A historical CI success does not prove current deployed behavior; re-pin current LogMate HEAD before runtime acceptance.
- **Policy/version watch:** Apple/WebKit storage/install/MDM, Service Worker updates, Firebase Auth/Apple revoke, Google Play deletion, W3C IndexedDB/manifest, accessibility and analytics consent need release-time current-source checks.
- **Cross-specialist responsibility:** Engineering S007 for implementation, Design Studio W121 for visual/accessibility runtime, Marketing for public claims, Web Manager for web/PWA trust and release conditions. Transfer rather than duplicate.

## 9. Meaningful checkpoint and next target

**Integration outcome:** unified five-track ownership, curriculum-versus-product gate, PWA state-machine taxonomy, bounded evidence register, 37/29 P0 risk, execution packets, external specialist handoffs and delta-driven hourly research method. **No new product runtime, managed-iPad PASS or release approval** occurred during consolidation.

**Next high-value target:** Engineering-authorized exact current LogMate source-pin and seeded 37-store terminal-wipe/reopen/A→B/old-writer canary campaign (529 WP01–WP20 P0 subset), then independently saved Files readback and compiled-Web/managed-iPad transfer. If execution access is unavailable, study only genuinely new adjacent evidence or changes; do not repackage the same open risk as fresh progress.

## 10. Post-consolidation canonical navigation correction (2026-11-07) [SOURCE / CONTRADICTION RESOLVED]

The first synthesis preceded a second, more granular integration. The **current navigation set** is [Web Knowledge Master](synthesis/WEB_KNOWLEDGE_MASTER.md), [PWA Architecture Master](synthesis/PWA_ARCHITECTURE_MASTER.md), [Evidence & Validation Register](synthesis/EVIDENCE_VALIDATION_REGISTER.md), [MintTap Product Application](synthesis/MINTTAP_PRODUCT_APPLICATION.md) and [Research Gaps & Scheduled Learning Protocol](synthesis/RESEARCH_GAPS_AND_SCHEDULE.md). [AGENTS](../AGENTS.md), [research index](README.md) and [STATUS](../STATUS.md) were updated to point to those documents. This 531 synthesis remains a preserved broad integration checkpoint and must not override more recent exact-source corrections in the focused masters.

**Evidence freshness rule:** “latest main” must be confirmed from the repository branch HEAD at the start of each run; GitHub API listing caches and individual file refs can differ during rapid writes. Do not imply the historical 531 baseline SHA is current. **Release gate remains Stage 8 ACTIVE / production validation OPEN / PWA release HOLD.**
