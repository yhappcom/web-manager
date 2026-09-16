# 073 — PWA Cross-Track Foundations: Service Workers, Offline, Install, Storage, Updates & Platform Reality

State: **PASS — FOUNDATION/PRACTITIONER CROSS-TRACK SPECIALIZATION CHECKPOINT**  
Date: 2026-09-16  
Primary owners: **Track A Web Platform & Browser + Track E Architecture/Security/Operations**  
Consumers: Track B UX/IA, Track C Quality, Track D Discovery/Analytics  
Production status: **OPEN — no MintTap/LogMate production PWA runtime is inferred**

## Why this block now
Stages 1–8 have passed their foundation/practitioner gates. PWA is now a strategic cross-track dependency for a company app scenario involving an iPad, offline usefulness and later synchronization. It is therefore higher immediate transfer value than beginning generic Stage 9 measurement work in this run. Stage 9 remains the next vertical curriculum stage; this block is an intentional cross-track specialization checkpoint, not a replacement for it.

## Evidence vocabulary
- **SOURCE** — directly established by a cited primary/platform/standards source.
- **SYNTHESIS** — transferable operational conclusion from sources.
- **OPEN** — project/platform fact not yet established.
- **DEPENDENCY** — evidence/work required from another track/specialist.
- **VALIDATION** — runtime/device test required.
- **CHANGE WATCH** — browser/OS capability or policy requiring periodic recheck.
- **TRANSFER VALIDATION** — prior Web Platform/Security/Performance knowledge successfully applied to PWA.
- **CONTRADICTION** — a common assumption rejected by evidence.

---

# 1. Historical problem: AppCache did not provide the control model modern offline apps needed

**SOURCE:** Chromium removed AppCache support; its old model revolved around a declarative application-cache manifest. Chrome's retained DevTools documentation marks Application Cache deprecated/removed.  
Source: https://developer.chrome.com/docs/devtools/storage/applicationcache

**SYNTHESIS:** The important historical lesson is not merely “AppCache was deprecated.” Offline behavior is a consistency/distribution problem: the application needs explicit control over request handling, version transitions, cache population/cleanup, failure fallback and observability. Service workers move this logic into an event-driven programmable intermediary rather than a static cache manifest.

**CONTRADICTION:** `PWA = AppCache replacement` is too shallow. A service worker is a programmable request/event execution environment with lifecycle and control semantics; it is not merely a cache list.

---

# 2. PWA is a capability composition, not one binary platform type

A useful model is:

`ordinary secure web app + manifest/presentation metadata + service-worker/runtime capabilities + origin storage + optional OS integrations + product-specific offline/update/data rules`

**SOURCE:** Service workers can intercept requests for controlled clients and respond from network/cache/custom responses. CacheStorage stores Request/Response pairs and is available in secure contexts.  
Sources: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API ; https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage

**SOURCE / CHANGE WATCH:** Safari 26/iOS 26/iPadOS 26 changed its Home Screen model: any website added to Home Screen can open as a web app by default, and WebKit explicitly says there are zero Safari “installability” requirements; manifest and service workers remain optional enhancement layers.  
Source: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

**SOURCE / CHANGE WATCH:** Chromium/Android installation behavior is different. Chrome removed a service-worker fetch handler as an Android installation requirement, and manifest/install promotion remains a Chromium-specific platform behavior rather than a universal PWA law.  
Source: https://developer.chrome.com/blog/whats-new-in-web-on-android-io2023/

**SYNTHESIS:** Never use one boolean `isPWA` as a capability model. Maintain a platform/capability matrix and feature-detect where possible.

---

# 3. Service-worker trust and scope model

**SOURCE:** Service workers are origin-partitioned and service-worker functionality is restricted to secure contexts in normal remote deployment.  
Sources: https://webkit.org/blog/8090/workers-at-your-service/ ; https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts

**TRANSFER VALIDATION — Stage 8:** HTTPS is not merely transport optimization for a PWA. A service worker can mediate future requests for clients in its scope; therefore trustworthy delivery of the worker script is a prerequisite to granting that power.

Core boundary:
`origin + registration scope + active controller → which clients/requests can be mediated`

**SYNTHESIS:** Service-worker scope should be treated as a security and release blast-radius boundary, not simply a convenient routing setting.

**OPEN:** Actual `minttap.app`/future app subdomain origin topology, worker scope and deployment architecture are unknown.

---

# 4. Lifecycle: install, waiting, activate, control

**SOURCE:** A new worker installs; when an older active worker controls pages, the new version normally waits. After old controlled pages close, the new worker activates. `skipWaiting()` can accelerate activation; `clients.claim()` can make an active worker control existing clients.  
Sources: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers ; https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting

**SOURCE:** Service-worker update checks compare fetched worker resources; `updateViaCache` controls whether HTTP cache participates in worker/import update checks.  
Source: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache

Critical version model:
`page/app-shell version ↔ active service-worker version ↔ cached asset version ↔ data/schema version`

**SYNTHESIS:** These versions can temporarily differ. Safe PWA updates are therefore compatibility/migration problems, not merely “download newest JS.”

**CONTRADICTION:** `skipWaiting() + clients.claim() = best update UX` is false as a general rule. Immediate takeover can cause an old page to issue later requests through a newly activated worker, creating mixed-version behavior.

**MINTTAP DIRECTION:** For data-bearing/offline applications, do not default to forced immediate activation. Define a compatibility window and update state machine first.

---

# 5. Offline is a product contract, not a cache strategy name

A useful separation:
1. **app shell/static assets** — HTML/CSS/JS/icons/fonts;
2. **read-mostly reference content** — docs/help/static metadata;
3. **mutable server data** — freshness-sensitive records;
4. **user-authored durable records** — potentially irreplaceable local state;
5. **queued operations** — local intentions awaiting remote acknowledgement.

**SOURCE:** A service worker `fetch` handler can return cached responses, network responses or fallbacks. Cache API stores HTTP request/response objects.  
Source: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Caching

Common strategy families and their failure boundary:
- cache-first: fast/reliable for versioned static assets; stale-content risk;
- network-first: fresher when online; latency/failure handling required;
- stale-while-revalidate: responsive reads with temporary staleness; unacceptable where stale state can mislead consequential actions unless clearly modeled;
- network-only: correct for operations that must not be replayed/offlined, but no offline utility;
- cache-only/precache: deterministic shell/reference assets, but deployment/version invalidation must be correct.

**SYNTHESIS:** Strategy is selected per resource/data class and task semantics. There is no single “offline-first cache strategy” for an application.

**TRANSFER VALIDATION — Track B:** Offline UX must distinguish `locally available`, `possibly stale`, `queued`, `syncing`, `synced`, `conflict`, and `failed`. A green “saved” state must not imply server/device synchronization when only local persistence succeeded.

---

# 6. Cache Storage is not the application database

**SOURCE:** CacheStorage is Request/Response storage. IndexedDB is the web platform's structured client-side database mechanism for significant structured data. Browser storage is generally origin-scoped.  
Sources: https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage ; https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference

**SYNTHESIS:** For a logbook-like offline application:
- CacheStorage fits app shell/assets and cacheable HTTP responses;
- IndexedDB is the natural browser-side candidate for structured flight/user records;
- neither automatically provides backup, cross-device synchronization or permanent durability.

**CONTRADICTION:** `cached offline = backed up` is false.

---

# 7. Storage durability: quota, persistence and eviction are first-class product risks

**SOURCE:** Browser origin data is normally best-effort. `navigator.storage.persist()` can request persistent storage, but the user agent decides whether to grant it. `estimate()` can report approximate usage/quota.  
Sources: https://developer.mozilla.org/en-US/docs/Web/API/StorageManager ; https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist ; https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria

**SOURCE / CHANGE WATCH — WebKit:** Safari 17+ changed quota policy; WebKit documents origin/overall quotas and origin-level eviction. A standalone Home Screen web app uses the same origin quota/overall quota model as browser use.  
Source: https://webkit.org/blog/14403/updates-to-storage-policy/

**SYNTHESIS:** A PWA containing user-authored records must design for the possibility of storage deletion caused by explicit user clearing, device/storage pressure, browser policy or application bugs even if persistence is requested.

**MINTTAP/LOGMATE-LIKE DIRECTION:** Local browser storage must not be the sole authoritative backup for irreplaceable flight records. A separate export/backup/replication design is required before calling the PWA durable.

**OPEN:** Whether the target managed/company iPad permits persistent storage behavior, file export destinations, or backup workflows has not been validated.

---

# 8. Installation/presentation is platform-specific

**SOURCE / CHANGE WATCH — Apple:** In Safari 26 on iOS/iPadOS 26, every website added to Home Screen can open as a web app by default; users can choose not to open it as a web app. A manifest still supplies presentation metadata/icons.  
Source: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

**SOURCE — older Apple behavior for compatibility context:** iOS/iPadOS 16.4 introduced Web Push for Home Screen web apps and broader Add to Home Screen support.  
Source: https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/

**SOURCE / CHANGE WATCH — cross-browser summary:** PWA installation/promotion behavior differs by desktop/mobile browser; Android Chrome/WebAPK behavior is not equivalent to iOS Home Screen web apps.  
Source: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable

**SYNTHESIS:** Product requirements should say “Home Screen web app on target iPadOS/browser” or “Android installed WebAPK/PWA” rather than generic “installed PWA.”

**EFB SCENARIO:** Absence of App Store access does not by itself prevent a Home Screen web app. But company browser/MDM/content restrictions may prevent adding/using it. **OPEN/VALIDATION:** target EFB policy and actual iPadOS version must be tested on the managed device.

---

# 9. Update UX must preserve user data and version coherence

Recommended state model:
`no update → update downloading → new worker waiting → migration compatibility checked → user-safe activation point → activation/reload → schema verification → success or rollback/recovery`

**SOURCE:** A new service worker may remain waiting until old clients are gone; update events can expose installation state; old cached assets are not automatically deleted simply because a new worker was installed.  
Sources: https://web.dev/learn/pwa/update ; https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers

**SYNTHESIS:** “New version available — refresh” is only safe if local writes, pending sync operations, schema versions and old/new asset compatibility have been designed for interruption.

**DEPENDENCY — Software Engineering:** schema migration, transactionality, backward/forward compatibility, conflict resolution and rollback implementation require engineering ownership. The software-engineering-studio repository currently exposes no substantive canonical evidence, so no implementation maturity is inferred.

---

# 10. Navigation and performance interaction

**SOURCE:** Navigation Preload can start a navigation network request in parallel with service-worker startup, avoiding worker-startup delay in supported browsers.  
Source: https://developer.mozilla.org/en-US/docs/Web/API/NavigationPreloadManager

**TRANSFER VALIDATION — Stage 7:** A service worker can improve repeat/offline performance but can also add startup, cache lookup, routing or stale-response costs. PWA does not imply fast. Measure cold navigation, warm controlled navigation, offline launch, update transition and resumed/standalone contexts separately.

**Track C validation matrix:**
- first online visit, uncontrolled;
- first controlled reload/navigation;
- warm online visit;
- slow/flaky network;
- fully offline launch;
- stale cache/update waiting;
- post-update activation;
- storage pressure/cleared data recovery;
- standalone vs browser context;
- representative Safari/WebKit and Chromium devices.

---

# 11. Background capability must never be assumed

**SOURCE:** The web platform includes APIs such as Background Sync, Push, Notifications and Badging, but capability availability differs by browser/platform. MDN's PWA reference enumerates them as distinct APIs, not guaranteed PWA features.  
Source: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference

**SOURCE / CHANGE WATCH — Apple:** Web Push is supported for Home Screen web apps from iOS/iPadOS 16.4; Apple requires user permission initiated from a user gesture for traditional Web Push and does not support invisible push notifications.  
Source: https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers

**SOURCE / CHANGE WATCH:** WebKit added Declarative Web Push in newer releases, reducing service-worker dependence for notification display. This is Apple-platform evolution, not proof of arbitrary background execution.  
Source: https://webkit.org/blog/16535/meet-declarative-web-push/

**CONTRADICTION:** `installed PWA can keep running/syncing in the background like a native app` is not established and must not be used as architecture.

**OPEN:** Background Sync/Periodic Background Sync suitability and support on the target company iPad are not established in this block. Direct device-to-device unattended synchronization is likewise unproven.

---

# 12. EFB / LogMate-like offline + native-mobile synchronization boundary

What this research establishes:
- **SUPPORTED IN PRINCIPLE:** a secure web app can use a service worker/cache for offline shell/content and IndexedDB for structured local data;
- **SUPPORTED WITH PLATFORM CONDITIONS:** an iPad Home Screen web-app experience exists on modern iOS/iPadOS, with materially changed behavior in version 26;
- **NOT A BACKUP GUARANTEE:** browser-origin storage can be cleared/evicted and requires independent durability strategy;
- **NOT ESTABLISHED:** unattended PWA↔native device synchronization merely because devices are nearby;
- **NOT ESTABLISHED:** reliable background execution/synchronization while the PWA is closed/suspended;
- **NOT ESTABLISHED:** target company EFB permits Add to Home Screen, required network origins, storage, push or file operations;
- **NOT ESTABLISHED:** hotspot/Bluetooth/local-network mechanisms satisfy zero-intervention synchronization requirements.

Architecture questions that must be answered separately:
1. What is the authoritative record replica: phone, PWA, cloud relay, or multi-master set?
2. What transport can both managed iPad PWA and native phone actually use under company/network policy?
3. How are records uniquely identified and changes versioned?
4. How are concurrent edits/conflicts represented?
5. How are unsynced local writes protected from update/storage loss?
6. What acknowledgement proves remote persistence?
7. What happens after weeks offline?
8. What is the manual recovery/export path when automatic sync fails?

**DEPENDENCY — Software Engineering:** CRDT/version-vector/change-log/server-relay/direct-transport choices belong to implementation architecture validation after web/platform constraints are established.

---

# 13. Cross-track ownership and handoffs

## Track A — owner
Owns service-worker lifecycle/scope/control, Fetch/Cache/IndexedDB/storage mechanics, manifest/platform capability distinctions and browser/OS differences.

## Track E — co-owner
Owns secure-context/origin trust, update/deployment/cache invalidation, storage durability policy, backup/restore requirements, incident/rollback and service-worker blast radius.

## Track B — consumer/handoff
Must design explicit install, offline, stale, queued, syncing, conflict, update-required, storage-risk and recovery states. App-like presentation must not erase browser/web navigation and recovery affordances without evidence.

## Track C — consumer/handoff
Must validate offline/runtime performance, cache correctness, keyboard/focus/reflow/accessibility, update transitions, storage-loss recovery and Safari/Chromium/device parity. Design Studio W022 still lacks integrated browser/runtime evidence; do not convert deterministic design evidence into PWA runtime PASS.

## Track D — consumer/handoff
Public indexable web resources and installed/offline application state are distinct surfaces. Service-worker routing must not accidentally hide canonical public resources from normal navigation/crawling. Acquisition/install analytics must distinguish website visit, install/add-to-home-screen where observable, standalone launch and native-store continuation without assuming cross-platform event equivalence.

## Marketing boundary
Marketing owns acquisition strategy and messaging. Web Manager owns install/runtime capability truth; marketing claims such as “works offline” or “syncs automatically” require the contracts and validation defined here.

---

# 14. PWA evidence contract

For every target platform/device record:
- OS + version;
- browser/engine + version;
- browser vs standalone context;
- secure-context/origin;
- manifest URL/id/start_url/scope/display;
- service-worker script URL/scope/version/state/controller;
- cache namespaces/asset version;
- structured-data schema version;
- persistence requested/granted state;
- approximate storage usage/quota;
- online/offline/flaky-network scenario;
- install/add-to-home-screen path actually observed;
- update/waiting/activation behavior;
- unsynced-write count and acknowledgement state;
- recovery/export path;
- capability feature-detection results;
- accessibility/performance observations;
- test timestamp and evidence artifact.

No production claim without this kind of target-runtime evidence.

---

# 15. Competency stress tests

### Case A — new worker available while offline edits exist
Do not force activation merely to deploy latest UI. Preserve local transaction state, confirm schema compatibility, expose update state, activate at a safe boundary, verify records after migration.

### Case B — cached shell opens but records disappear
Do not report “offline works.” Separate shell cache from IndexedDB/data durability, inspect origin/storage state and recovery path.

### Case C — app works offline for one day on developer iPad
Insufficient evidence. Test storage clearing/pressure, prolonged offline use, update transition, managed target device, Safari/standalone lifecycle and recovery.

### Case D — product requests automatic PWA↔phone sync when devices are near
Treat transport/background/discovery as OPEN. Do not infer native-style peer-to-peer capability from PWA installation.

### Case E — marketing wants “install our app” button everywhere
Platform install affordance and observability differ. Track B/D/Marketing must use capability/platform-aware language and fallback, not a universal install flow.

### Case F — immediate `skipWaiting()` appears to fix update complaints
Reject as incomplete. Determine whether mixed old-page/new-worker behavior and schema/cache compatibility remain safe before adopting.

---

# 16. Gate result

**PASS — PWA FOUNDATION/PRACTITIONER CROSS-TRACK CHECKPOINT.**

The Web Manager can now:
1. explain why service workers exist beyond AppCache-style caching;
2. distinguish PWA capability composition from platform-specific installation;
3. reason about worker lifecycle/control/update hazards;
4. select cache strategies by resource/task semantics;
5. separate CacheStorage, IndexedDB, persistence and backup;
6. identify storage eviction/data-loss risk;
7. distinguish Safari/iPadOS and Chromium/Android installation realities;
8. reject unsupported background/P2P/sync assumptions;
9. define update/offline/recovery UX requirements;
10. create a target-device evidence contract before production claims.

This does **not** validate a production PWA or the EFB synchronization architecture.

# 17. Next high-value PWA block

Before or alongside Stage 9, deepen the strategic specialization with a second integrated block focused on **PWA Data Durability & Synchronization Architecture Boundaries**:
- IndexedDB transaction/schema/migration mental model;
- local-first write log/outbox and acknowledgement semantics;
- conflict/idempotency/retry foundations;
- backup/export/restore distinction;
- online/offline transition and long-offline recovery;
- browser suspension/background limitations by platform;
- feasible web↔native synchronization transports and their security/policy boundaries;
- target EFB device validation plan.

That block should coordinate closely with Software Engineering once substantive canonical engineering evidence exists.
