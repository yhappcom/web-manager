# 084 — Change Watch: iOS/iPadOS PWA Install, Background & Authentication Reality, 2026-09

Status: **PASS — continuous expert maintenance checkpoint**  
Date: 2026-09-16  
Primary owners: **A Platform/Browser + E Architecture/Security/Operations**  
Consumers: B install/offline/session UX; C resilience/device validation; D install/acquisition measurement.

## Trigger and track balance
The sequential curriculum is complete. Current canonical risk is PWA capability truth for a LogMate/EFB-like managed-iPad scenario. 083 updated storage durability. The highest-value adjacent gap is now the difference between **Home Screen installation, foreground execution, event-driven background work, persistent authentication, and unattended synchronization**.

A and E own this checkpoint because platform mechanics and operational guarantees are prerequisites. B/C/D consume the resulting capability boundaries rather than duplicating browser research.

## Integrated capability model
`user can create Home Screen web app → app can launch standalone → foreground task works → local state survives → authentication state is usable → service worker may handle supported events → connectivity returns → application gets an execution opportunity → queued work is retried → server acknowledges → reconciliation completes`

Every arrow is a separate capability/evidence boundary.

## 1. iOS/iPadOS 26 materially changes Home Screen installability
**SOURCE:** WebKit, *WebKit Features in Safari 26.0* (2025-09-15), states that on iOS 26 and iPadOS 26 every website added to the Home Screen opens as a web app by default. The user can disable **Open as Web App**. WebKit explicitly says there are now zero developer-side requirements for “installability” in Safari; a manifest is no longer required merely to obtain the Home Screen web-app experience. WebKit also states that Service Workers have never been an iOS/iPadOS Home Screen installability requirement.

**SOURCE:** Current Apple iPad User Guide likewise documents Safari → Add to Home Screen → Open as Web App, and says the resulting icon exists only on the device where it was added.

**CONTRADICTION / historical correction:** Older iOS/iPadOS guidance tied standalone Home Screen behavior to a manifest `display` mode or Apple meta tag. That remains useful historical evidence, but it must not be used as the current iOS/iPadOS 26 installability rule.

**SYNTHESIS:**
`Home Screen installability ≠ manifest quality ≠ offline capability ≠ service-worker capability ≠ product suitability`.

A manifest still provides product metadata/presentation benefits. A Service Worker can still provide offline/runtime behavior. Neither is proof that the installed experience satisfies an EFB requirement.

**CHANGE WATCH:** This is current iOS/iPadOS 26 behavior and is platform policy/implementation, not a timeless Web standard.

## 2. Home Screen creation remains user/device state
Apple documents a user-driven Add to Home Screen flow. The icon is device-local. Therefore a public URL being reachable does not imply the PWA is installed, retained, or permitted by a company-managed-device policy.

**OPEN:** Exact MDM restrictions, Shared iPad status, Safari/share-sheet policy, allowed Home Screen creation, profile retention and device reset/reprovision behavior for the company EFB fleet remain unverified.

**MINTTAP/LOGMATE DECISION BOUNDARY:** Do not describe a managed-EFB PWA as “installable” in the operational sense until the target device policy permits and retains the required Home Screen experience. Generic iPadOS support only establishes platform capability.

## 3. Push/badging proves specific event-driven background capability, not general background execution
**SOURCE:** WebKit added standards-based Web Push for Home Screen web apps in iOS/iPadOS 16.4. Permission must be requested in response to direct user interaction. WebKit documents that Badging API operations can occur while the web app is foregrounded or while it handles push events in the background.

**SOURCE:** Apple Developer documentation continues to describe Web Push for Home Screen web apps on iOS 16.4 or later using Push API, Notifications API, Badging API and Service Worker standards.

**SOURCE:** WebKit's Declarative Web Push work is available for testing from iOS/iPadOS 18.4 and reduces reliance on Service Worker JavaScript for notification display. This is notification delivery evolution, not a general background-compute primitive.

**SYNTHESIS:**
`push event can wake supported processing ≠ arbitrary background timer ≠ continuous worker ≠ guaranteed unattended sync`.

A push-delivery path is server-triggered and permission/network/policy dependent. It should not be repurposed as proof that an offline outbox will automatically synchronize whenever connectivity returns.

## 4. Service Workers are event-driven and disposable
**SOURCE:** The Service Worker model allows the user agent to terminate an idle worker and restart it for supported events. Worker global in-memory state is therefore not a durable application state store.

**SYNTHESIS:** Critical sync state must live in durable storage/protocol state, not worker globals. A worker execution opportunity is a trigger to inspect durable work, not the work ledger itself.

Operational guard:
`worker registered ≠ worker continuously alive ≠ execution opportunity at desired time ≠ operation acknowledged`.

## 5. Background Sync is not a cross-browser correctness primitive
**SOURCE:** MDN marks Background Synchronization API and `ServiceWorkerRegistration.sync` as **Limited availability / not Baseline** because they do not work in some widely used browsers. Periodic Background Sync is also Limited availability and Experimental.

**VALIDATION BOUNDARY:** Current authoritative Apple/WebKit material found for this checkpoint documents Web Push and event-driven worker behavior but does not establish Background Sync/Periodic Background Sync as a dependable iOS/iPadOS Home Screen capability for the target fleet.

**SYNTHESIS:** For cross-browser and especially managed-iPad correctness, do not make eventual synchronization depend on Background Sync or Periodic Background Sync.

Required correctness path remains:
`durable outbox → retry while app is open/resumed/reconnected/manual-sync/next-launch → idempotent server apply → acknowledgement → pull/reconciliation`.

If a supported browser provides an additional background execution opportunity, treat it as latency optimization, not the sole correctness mechanism.

## 6. Authentication state and Home Screen installation are distinct
**SOURCE:** WebKit Safari 17.2 introduced iOS/iPadOS behavior where creating a Home Screen web app copies the current website cookies into the new web app, including login state **only when authentication state is cookie-based**. WebKit explicitly says other local storage is not copied, and after creation no other website data is shared between the browser and web app.

**SYNTHESIS:**
`logged in in browser ≠ all auth/application state cloned into Home Screen web app`.

Installation-time cookie transfer can improve continuity, but it is not ongoing shared state. Token material stored only in LocalStorage/IndexedDB must not be assumed to migrate from browser context. Conversely, browser logout/login later must not be assumed to synchronize Home Screen state automatically.

## 7. Offline authentication needs a product contract
When offline, a server cannot freshly validate credentials or revoke a session. A PWA may still allow local access if the product deliberately supports an offline-authorized state, but this is an application security decision rather than a generic PWA feature.

Separate:
- **identity established previously**;
- **local device/user may access cached records now**;
- **server session currently valid**;
- **server authorization for a mutation currently confirmed**;
- **queued mutation accepted later**.

**DEPENDENCY — Software Engineering/Security:** Product implementation must define credential/token storage, expiry, device-loss behavior, logout semantics, local-data encryption/protection where required, offline authorization window, server rejection/reconciliation and re-authentication UX. Web Manager does not infer these from cookie-copy support.

## 8. Fetch credentials and cross-origin architecture
**SOURCE:** Fetch defaults credentials to `same-origin`; cross-origin credential inclusion requires explicit `credentials: include` and is still constrained by cookie SameSite/CORS policy. Service Worker interception does not erase these browser security rules.

**SYNTHESIS:** Moving API/auth to another origin can materially change session behavior. Offline shell architecture, API topology and authentication design must therefore be reviewed together rather than treating CORS/cookies as deployment details.

## 9. EFB capability matrix — evidence status
| Capability | Generic current evidence | Product/EFB conclusion |
| --- | --- | --- |
| Add site as Home Screen web app | Supported/user-driven on current iPadOS; iPadOS 26 defaults Open as Web App | **OPEN** under company MDM/device policy |
| Manifest required for install | No on iOS/iPadOS 26 | Manifest still recommended for controlled product metadata; not an offline guarantee |
| Service Worker required for install | No | Still useful/needed for chosen offline interception strategy |
| Offline shell/data | Web platform supports SW/Cache/IndexedDB patterns | **OPEN** for exact canonical artifact + managed iPad |
| Web Push | Home Screen web apps supported since iOS/iPadOS 16.4 | Optional notification path; permission/server/policy dependent |
| Background event execution | Specific push events can run supported work | Not general continuous/background sync proof |
| Background Sync | Not cross-browser Baseline | Must not be correctness dependency for EFB |
| Periodic Background Sync | Limited/experimental cross-browser | Must not be correctness dependency |
| Browser→Home Screen login continuity | Cookie state copied at creation since iOS/iPadOS 17.2 | Only cookie-based state; no ongoing general storage sharing |
| Persistent local storage | Platform mechanisms exist; 083 documents current WebKit policy | **OPEN** exact fleet grant/survival/recovery |
| Unattended PWA↔native phone sync | No generic evidence established | **OPEN — implementation/device/network validation required** |

## 10. Cross-track consequences
### A Platform/Browser — owner
Maintain current iOS/iPadOS installability, Service Worker lifecycle, Push/Badging, cookie/storage boundary and background-capability change-watch. Keep Web standard semantics separate from WebKit implementation/policy.

### B UX/IA/Content — consumer
Installation UX must reflect the actual user-driven Home Screen flow. Offline/session UX should expose meaningful states such as **offline/local**, **authentication required**, **sync pending**, **sync failed/rejected**, and **synced** instead of implying background completion.

### C Performance/Accessibility/Quality — consumer
Acceptance must include foreground→terminate→offline relaunch, expired/revoked-session cases, long-offline resume, worker update with pending data, accessible recovery messaging, and target Safari/iPad execution. Push receipt is not a substitute for sync/recovery testing.

### D Search/Discovery/Analytics — consumer
Website visit, Add-to-Home-Screen opportunity, installed launch, push permission and synchronized task completion are different events. Some install state is not directly observable from ordinary web analytics; do not infer installed population from page visits.

### E Architecture/Security/Operations — co-owner
Authentication/session, durable outbox, data recovery, notification infrastructure, service-worker deployment and managed-device policy are separate trust/failure domains. Security decisions must define offline authorization and device-loss/revocation behavior.

## 11. Software Engineering transfer
Current Software Engineering Studio evidence emphasizes semantic compatibility beyond source signatures. This directly applies to PWA skipped-version/offline clients: protocol/schema compatibility must preserve prior consumer meaning and invariants, not merely parse the same fields. Web Manager consumes this as a dependency; executable protocol/schema/device validation remains Software Engineering ownership.

## 12. Failure diagnoses
1. **“iPadOS can install any site, so LogMate PWA is approved.”** False. Platform capability does not establish MDM permission, offline correctness, data durability or recovery.
2. **“Service Worker exists, so it will sync when the network returns.”** False. Worker registration/lifecycle does not guarantee a desired background execution opportunity.
3. **“Push wakes a worker, therefore background sync is solved.”** False. Push is a specific server-triggered capability with permission/network/policy dependencies.
4. **“User was logged in before install, so all state carries over.”** False. WebKit documents installation-time cookie copying, not arbitrary local-storage copying or ongoing shared state.
5. **“Background Sync API exists in the Web platform, so Safari can be designed around it.”** False. It is not Baseline across widely used browsers and no target-fleet validation is established here.
6. **“Offline access means server authorization is current.”** False. Offline authorization must be explicitly bounded and reconciled when server authority returns.

## 13. Operational acceptance contract for LogMate-like EFB PWA
Before claiming operational suitability, obtain evidence for:
1. exact managed-iPad OS/WebKit/MDM Home Screen policy;
2. canonical production-equivalent artifact installation;
3. cookie/session/login behavior before and after Home Screen creation;
4. offline authorization/re-authentication rules;
5. terminate→offline relaunch and local read/write;
6. durable outbox after process/device restart;
7. reconnect while foregrounded and deterministic retry;
8. reconnect while closed — record what actually happens, without assuming background sync;
9. server acknowledgement/reconciliation after duplicate/retry/rejection;
10. Service Worker update with pending local operations;
11. skipped-version schema/protocol migration;
12. independent backup/restore and device-loss path;
13. push/badging only as optional independently validated capability;
14. accessibility of install/offline/auth/sync/recovery states.

## OPEN
- target company iPad OS/WebKit version and MDM restrictions;
- Shared iPad status and whether Home Screen creation is allowed/retained;
- exact authentication/session design for LogMate;
- offline authorization policy and local-data protection;
- exact foreground/resume retry implementation;
- whether any target-fleet background execution beyond push is available/reliable;
- direct unattended PWA↔native transport/discovery;
- actual backup/export/restore UX and destination.

## Sources checked 2026-09-16
- WebKit, *WebKit Features in Safari 26.0* (2025-09-15) — current iOS/iPadOS 26 Home Screen web-app behavior.
- Apple Support, *Turn a website into an app in Safari on iPad* — current user flow and device-local icon behavior.
- WebKit, *Web Push for Web Apps on iOS and iPadOS* (2023-02-16) — Home Screen Web Push/Badging behavior.
- Apple Developer, *Sending web push notifications in web apps and browsers* — current Apple Web Push developer guidance.
- WebKit, *Meet Declarative Web Push* (2025-03-27) — notification evolution; tested on iOS/iPadOS 18.4.
- WebKit, *WebKit Features in Safari 17.2* — installation-time login-cookie copying and no general local-storage copying.
- MDN, Background Synchronization API / Periodic Background Synchronization API — current limited-availability status.
- MDN, ServiceWorkerGlobalScope and Fetch credentials — worker lifecycle and credential semantics.

## Maintenance result
This checkpoint removes a major ambiguity in the EFB strategy: **current iPadOS Home Screen web-app creation is broadly available at the platform level, but automatic synchronization is a completely separate capability and must not be inferred from installability, Service Worker presence, Web Push, or generic Background Sync documentation.**