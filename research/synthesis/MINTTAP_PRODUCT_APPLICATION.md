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

## 6. Prelaunch site/release readiness contract (future, NOT RUN)

1. **Identity/content:** verified company developer/legal identity, contact, apps and exact version; page and Store truth matrix including locale and screenshots.
2. **Support/privacy/deletion:** real reachable routes and request handling, current App Data Contract, permitted retention and accurate local vs remote deletion states; handle failed/retry states accessibly.
3. **Transport/security:** inspect real HTTPS certificates, canonical redirects, route-specific `Referrer-Policy`/CSP and asset links, OAuth callback, SW scope, escaped telemetry fields, safe deployment/rollback.
4. **UX/accessibility:** desktop/mobile/tablet, light/dark where product applies, keyboard/AT/zoom/reflow/slow/failure UX; Design Studio W121 evidence and representative users.
5. **Discovery/measurement:** URL/index/canonical and Store handoff; use consent-safe events with test and real-field provenance. Avoid fabricated traffic/performance success.
6. **PWA/EFB:** close all P0 owner/Files hazards and in-scope P1 NORMAL/browser/physical managed-EFB oracles before any “safe offline flight logbook / supported EFB” claim.
7. **Operations:** owner for policy/claims, change watch, incident response, restore test, artifact/served-version tracking, accessible support and release rollback.

**PROJECT DECISION boundary:** This file records candidate requirements and no actual launch approval; owners must explicitly decide provider, app-specific published routes, release scope and acceptable residual risks. See [open decisions and work protocol](RESEARCH_GAPS_AND_SCHEDULE.md).
