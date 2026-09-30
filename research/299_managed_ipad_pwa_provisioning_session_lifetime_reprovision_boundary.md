# 299 — Managed-iPad PWA Provisioning, Session Lifetime & Reprovision Boundary Contract

Status: **PASS (generic research/model) / PRODUCT + PHYSICAL-IPAD + MANAGED-IPAD + INSTALLATION-CONTEXT VALIDATION OPEN**  
Date: 2026-09-30  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: **A Platform/Browser**, **C Quality/Validation**  
Consumers: **B UX/IA**, **D Analytics/Diagnostics**

## Why this gate exists

298 separated local persistence from backup and executable recovery. The next bottleneck is the management boundary itself: a company iPad can receive a Web Clip, restrict Safari, use device/user enrollment, be Shared iPad, or be erased/reprovisioned. None of those management facts alone establish the lifetime or recoverability of PWA origin data.

For an EFB/LogMate-like PWA, provisioning must therefore be modeled separately from runtime/storage/session identity.

## SOURCE

### Apple Web Clip management

Apple documents the `com.apple.webClip.managed` payload for iOS/iPadOS, including Device Enrollment, Automated Device Enrollment, User Enrollment and Shared iPad user channels. Multiple Web Clips may be delivered. A Web Clip can be non-removable and can open full-screen; when Safari is hidden and restricted, Apple requires full-screen Web Clip use. Apple also warns that device-management vendors implement these settings differently.

Source: https://support.apple.com/guide/deployment/depbc7c7808/web

### Safari restriction

Apple's supervised-device restrictions state that disabling Safari makes Safari unavailable and also prevents users from opening Web Clips. Therefore an icon/payload being present is not proof that its launch path remains usable under the active policy envelope.

Source: https://support.apple.com/guide/deployment/dep6b5ae23e9/web

### Shared iPad temporary sessions

Apple documents that when a Shared iPad Temporary Session guest logs out, all that user's local data, including browsing history, is deleted. Temporary sessions also do not require a Managed Apple Account and may not support services that depend on iCloud/cloud storage.

Source: https://support.apple.com/guide/deployment/dep9a34c2ba2/web

### Managed-device backup

Apple documents iCloud/Finder/Configurator backup classes and management restrictions, but managed-app backup controls are defined for managed apps. Apple does not state that those managed-app controls constitute a backup contract for Web Clip website data.

Sources:
- https://support.apple.com/guide/deployment/depd44f04xc3/web
- https://support.apple.com/102017

### Web-app storage-context creation

WebKit documents that on iOS/iPadOS 17.2, creating a Home Screen web app copies current cookies from the browser but no other local storage; after creation, other website data is not shared. This is evidence that visually related launch surfaces can have distinct website-data contexts.

Source: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/

## SYNTHESIS

### 1. Provisioning, launch, storage and recovery are separate state machines

Use four independent dimensions:

- **P — provisioning:** absent / user-created / MDM Web Clip / Shared-iPad-user payload / removed;
- **L — launch:** Safari / Home Screen web app / Web Clip browser mode / Web Clip full-screen / policy-blocked;
- **S — state lifetime:** origin data present / unknown / session-scoped / deleted / restored-but-unverified;
- **R — recovery:** none / local persistence / export / device backup candidate / tested restore / remotely converged.

A transition in P or L must not silently promote S or R.

### 2. Management persistence is not data persistence

A non-removable Web Clip means the user cannot remove that launch object without removing the installing profile. It does not mean IndexedDB, Cache Storage, Service Worker registrations, credentials or outbox are non-evictable or independently backed up.

`non-removable icon ≠ non-removable origin data`.

### 3. Web Clip is not automatically a managed-app backup subject

Apple provides explicit backup controls for MDM-installed managed apps. Web Clips are configuration payloads. Current Apple documentation does not establish that managed-app backup semantics apply to Web Clip website data. Treat that transfer as OPEN until physical-device evidence or explicit Apple documentation establishes it.

### 4. Shared-iPad session class can dominate application durability

If the actual EFB deployment ever uses Shared iPad Temporary Sessions, logout is a destructive local-data boundary by Apple contract. Unique offline work cannot be admitted under an assumption that browser/PWA state survives that logout. A dedicated-device PASS cannot be transferred to Shared iPad Temporary Session.

### 5. Policy can invalidate launch without removing the payload

Safari restrictions can prevent Web Clips from opening. Therefore support diagnostics must record the active management-policy envelope, not merely whether the Web Clip profile/icon exists.

### 6. Reprovision is a destructive transition until proven otherwise

Erase/reprovision/profile removal/re-enrollment can change provisioning, storage, credential and trust state independently. Recovery claims require pre-destruction inventory and post-restore semantic checks. Recreated icon/profile is only provisioning evidence.

## MINTTAP DECISION

For an EFB/LogMate-like PWA:

1. Record installation/provisioning class explicitly; never infer it from appearance.
2. Treat MDM Web Clip, Safari-created Home Screen web app, browser tab and Shared iPad user session as distinct validation classes.
3. Do not rely on managed-app backup settings as proof for Web Clip origin-data backup.
4. If Shared iPad Temporary Session is in scope, unique offline work must have an independent recovery/sync path before logout.
5. Treat profile removal, erase/reprovision and enrollment changes as destructive transitions requiring data-preservation checks.
6. Support tooling should capture policy envelope, launch class, controller/storage generations, local unique-work/outbox count and last remote acknowledgement horizon.
7. Production validation remains OPEN until representative managed hardware is tested.

## HARD GUARDS

- `Web Clip installed ≠ Web Clip launchable`
- `Web Clip launchable ≠ Home Screen web-app equivalence`
- `full-screen ≠ same storage context`
- `non-removable Web Clip ≠ non-evictable data`
- `managed app backup setting ≠ Web Clip website-data backup proven`
- `profile restored ≠ origin state restored`
- `same URL ≠ same website-data lineage`
- `Shared iPad user ≠ dedicated-device storage lifetime`
- `Temporary Session logout ≠ recoverable local state`
- `re-enrolled ≠ re-authorized`
- `icon present ≠ Service Worker controlling`
- `offline launch works ≠ unique work recoverable`

## DEPENDENCY / TRANSFER

**Track A** owns browser/WebKit storage and Service Worker mechanics.  
**Track C** owns destructive validation across installation/session classes.  
**Track B** must represent blocked launch, local-only work, pending sync and recovery-required states without false reassurance.  
**Track D** may observe class/policy/rejoin outcomes but telemetry cannot prove omitted state never existed.  
**Software Engineering** must supply actual installation path, durable stores, auth/session, outbox/ACK semantics and support diagnostics before product validation.

## VALIDATION — deterministic campaign

At minimum test:

1. User Home Screen web app vs MDM full-screen Web Clip at same URL.
2. Same URL with both launch surfaces present.
3. Web Clip payload present while Safari restriction blocks launch.
4. Safari hidden but not restricted vs hidden+restricted.
5. Non-removable Web Clip with website-data deletion.
6. Profile removal while unique local work exists.
7. Profile reinstall recreates icon but not origin data.
8. Erase/reprovision with device backup candidate.
9. Re-enrollment with stale credentials.
10. Service Worker registration absent after launch-surface restoration.
11. IndexedDB restored but Cache Storage absent.
12. Records restored but outbox absent.
13. Outbox restored with lost-ACK retry.
14. Dedicated-device PASS transferred incorrectly to Shared iPad.
15. Shared iPad Temporary Session logout with unsynced work.
16. Shared iPad new session receives Web Clip but no prior local data.
17. MDM vendor implementation differs from Apple payload expectation.
18. Network/trust restriction allows shell but blocks API.
19. Policy changes while app is offline.
20. Policy rollback recreates launch but predecessor remote authority remains.
21. Same-device restore vs new-device restore.
22. Managed-app backup option assumed to cover Web Clip without evidence.
23. Unmanaged physical iPad PASS promoted to managed EFB.
24. Simulator/browser automation PASS promoted to physical iPad.

All are **DEFINED / NOT EXECUTED**.

## Validation ladder

- **V0:** provisioning/launch/storage/recovery topology record.
- **V1:** deterministic local-state/outbox/session destruction fixture.
- **V2:** exact Safari/WebKit/iPadOS + installation class.
- **V3:** physical unmanaged iPad comparison.
- **V4:** representative managed company iPad with actual MDM policy/enrollment/reprovision.
- **V5:** actual PWA↔native↔server recovery, reauthorization and convergence.

PASS is non-transitive.

## CHANGE WATCH

- Apple Web Clip payload semantics and Safari restrictions.
- Shared iPad session behavior and future authenticated guest modes.
- iOS/iPadOS Home Screen web-app storage-context behavior.
- MDM-vendor handling of Web Clips, backup, profile removal and reprovision.
- Apple backup/restore documentation as it relates specifically to website data.

## OPEN

- Actual LogMate iPad provisioning class.
- Whether company devices are dedicated, Shared iPad, or temporary-session capable.
- Exact MDM vendor, enrollment, Safari restrictions and backup policy.
- Exact website-data behavior of the chosen Web Clip path on representative hardware.
- Actual durable store/outbox/auth/server topology.
- Physical backup/reprovision/rejoin evidence.

## Integrated competency

The operational question is not “can MDM put the PWA on the Home Screen?” It is:

> Under the exact enrollment, session, launch and policy class, what local state exists, how long does it live, what event can destroy it, what independent recovery root exists, and what evidence proves safe reauthorization and convergence afterward?

Until those questions have representative-device evidence, managed-iPad PWA deployment remains **OPEN**, even when provisioning itself succeeds.
