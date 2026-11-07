# PWA Architecture Master — cross-track security, offline and device-custody synthesis

**Snapshot:** 2026-11-07 KST, Web Manager `main@4f5903f411b8c3a353ea4edb552c7bea6c4a2e33`. **Scope:** durable knowledge and bounded LogMate-like EFB application. **Release gate:** Stage 8 ACTIVE / product validation OPEN / PWA release HOLD. **Owners:** A platform facts; E trust/operations; B interaction; C validation; D discoverability/claims. References: [073 PWA foundations](../073-pwa-cross-track-foundations-service-worker-offline-install-storage-update-platform-reality.md), [074 durability/sync](../074-pwa-data-durability-sync-architecture-offline-recovery-transport-boundaries.md), [298 backup](../298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md), [523 remote owner](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md), [528 release/version](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md), [529 deletion](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md), [530 install/MDM](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md).

## 1. Historical problem → standards → operational judgment

**HISTORY:** AppCache coupled application availability to a coarse, failure-prone cache/update manifest. Service Workers enable programmable, secure-origin-controlled fetch interception and explicit install/waiting/activate state, but do **not** make app shell, per-client control, local database and remote authority one atomic system. A PWA can simultaneously contain a V1 tab, V2 waiting worker, retained V1 shell, evolving IDB schema, local unsent edits and intermittent network.

**SOURCE classes:** Service Worker lifecycle/clients/Cache API are Web standards implemented differently by browsers; Web App Manifest addresses presentation and installed identity, not user-data custody; IndexedDB and Cache Storage are distinct origin-managed stores; HTTPS secure context and origin policy provide isolation, not malware-proof script integrity. Browser support for Background Sync/push/badging/File Handling/Web Share, installed container behavior, and MDM control is **version-specific CHANGE WATCH**.

**Five independent states:** (1) installed icon/manifest identity; (2) worker registered/waiting/active; (3) each client actually controlled and assigned a consistent build; (4) shell resources fully verified and cold offline replayable; (5) owner ledger writable, independently backed up and restorable. Only state-specific observations authorize corresponding UI copy.

## 2. Identity and origin matrix

| Identifier | Governs | Does NOT prove |
| --- | --- | --- |
| URL origin (scheme/host/port) | Web security and origin-managed storage bucket | Installed app identity, UID, replica ownership |
| Manifest `id` / `start_url` / `scope` | Install identity/launch/navigation contract | SW controller or data persistence |
| Service Worker registration scope and controller | Controlled client fetch interception | Complete cache, current schema, authenticated account |
| Safari tab / Home Screen web app / managed Web Clip | Browser/OS-specific app/container context | Shared IndexedDB, identical permission or Files access |
| Firebase UID / local Owner / replica ID | Distinct user, local data and replica authorities | Direct peer reachability or automatic Sync |
| Served artifact hash / CacheStorage catalogue | A particular byte representation and lookup | Independent release-signing authority if expected hash is also mutable |

**PRODUCT TRANSFER / OPEN:** Research [530](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) reports a LogMate manifest without explicit `id`/`scope` at its pinned source; URL-resolution implications are **models**, not installed-browser validation. WebKit Home Screen installation/presentation behavior and Managed Web Clip policy cannot be inferred from a Chromium install button. Installation can create a separate storage context; migration between origins/containers must not be assumed. Recheck exact current manifest before any implementation proposal.

## 3. Fetch, caching and offline design

- **App shell/versioned assets:** cache-first can support offline but only with source-pinned resource manifest, digest/integrity, explicit repair/retry, full inventory and safe retirement. A cache entry is an HTTP Response object, including headers; body-only SHA-256 checks do not authenticate cached CSP/MIME headers ([523 §§25–26](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md)).
- **Public informational pages:** network-first plus bounded fallback may be reasonable, but root-scoped worker interception of their CSS/icon/fonts must be tested independently. A working HTML navigation does not guarantee supporting assets; synthetic [523 §§22–24](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) demonstrate a conditional 503 route mechanism, not LogMate NORMAL failure.
- **Authenticated and sensitive responses:** do not treat generic GET caching as an authorization model. Auth Action one-time codes, owner data, private response headers, referrers and telemetry require threat-specific handling; HTTP `no-store` and browser bfcache are separate domains ([527](../527_stage8_pwa_origin_identity_migration_custody_20261029.md), [530 §§15–25](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md)).
- **Durable records/outbox:** IndexedDB/Sembast transaction boundaries, owner fences and local/reconciled operation states are not SW resource caches. Offline shell success is not data persistence or Sync acceptance.
- **Connectivity:** online/offline browser events and network success are hints, not proof that authenticated backends, local peers, quotas or policies permit a specific operation.

## 4. Release/update/rollback invariant sequence

**Track A platform:** worker update script check (`updateViaCache:'none'`, `registration.update()`) → candidate installed/waiting → active worker → controller assigned to a client. **Track E release:** independently verify candidate manifest/asset origin, compatibility with DB capability/schema, old-client continuation, owner/Sync state, storage budget, rollback/recovery. **Track C:** prove each transition on an exact served build with negative controls; **B:** do not say “offline ready” from icon/registration alone; **D:** do not publish unverified features.

**Hazards and research findings:**
1. Worker-global Promise queue does not serialize different SW generations. Shared CacheStorage whole-JSON catalogue can lose cross-generation updates in a **synthetic Chrome** race; IDB `readwrite` get/put inside transaction preserves a modelled pointer, but IDB and Cache Storage are not one atomic commit ([514](../514_stage8_pwa_worker_generation_trace_evidence_data_preserving_recovery_20261024.md), [528](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md)).
2. Download/verification and activation are different. A waiting worker or valid candidate cannot be promoted solely by a download check; an old tab can survive and needs explicit build/schema/owner admission.
3. Mutable cache-catalogue expected hash is not an independent authenticated provenance root. Paired catalogue+body mutation can pass a **research-only negative control**; do not call this observed LogMate compromise ([523](../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md), [528](../528_stage8_pwa_update_schema_rollback_storage_custody_20261030.md)).
4. Version retention and per-client build-map entries can accumulate. Naive old-cache deletion could strand live tabs; measured device cost remains OPEN. Source-derived conditional hash-read cost is not real latency or battery loss.
5. Missing shell, rejected candidate, low quota, process death, network loss and rollback must result in truthful recovered/degraded states, not a misleading universal “updated”/“offline ready” flag.
6. A version-pinned NORMAL build, served HTTPS response, controlled first load, cold offline relaunch, independently reopened 37-store ledger and Files backup each require separate proof.

## 5. Storage, privacy, account deletion and external recovery

Four **non-equivalent claims**: `persisted()` reports browser persistence mode; `estimate()` approximates quota; an IDB transaction completion shows a logical commit to browser-managed state; **independent backup** means a physically separate artifact has been saved, read back and successfully restored in a fresh context. None implies power-loss survival, MDM export permission, app-profile survival or secure Sync.

**Security/owner P0:** [529 §96](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) rechecked an altered source blob and still found 37 backup stores versus 29 explicit deletion drops, with replica and seven Sync stores omitted. `requestAccountDeletion` and active draft-writing guards leave a conditional stale-writer gap. Phase-transition, concurrent deletion drivers and normal A-delete→B startup require executable proof. This is **static risk** and should not be called observed data leakage or incident. Web Manager must not silently rewrite Engineering S007 policy or treat a blanket site wipe as harmless; backup files under user custody are distinct from local owner erasure.

**Untrusted backup and format:** full JSON parsing, canonicalized digests, nested Sync evidence, duplicate key, numeric precision, row budget, provenance and rollback are separate from cryptographic hash equality. [298](../298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md) and [529](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) define exact adversarial tests. Native W-012 positive tests do not prove PWA/Files/MDM.

## 6. iPad/Chromium/standards boundary (CHANGE WATCH)

| Question | Standards/general web | Chromium research | Safari/WebKit and managed EFB |
| --- | --- | --- | --- |
| Install and launch | Manifest and SW optional/related, not equivalent | Synthetic/lab installation behavior, browser-specific | Home Screen presentation and Web Clip MDM policy distinct; permission **OPEN** |
| Offline navigation | Controlled fetch + verified cache + state | Hosted synthetic Worker lifecycle 17/17 PASS | Safari Simulator Acceptance harness PARTIAL; NORMAL installed/physical **OPEN** |
| Local data | IDB transactions, CacheStorage and quota distinct | Synthetic Sembast Web independent tabs 9/9 PASS | Persistent mode/eviction and install containers **OPEN** for actual managed device |
| Background tasks/push | Feature-by-feature APIs, no universal guarantee | Support varies by browser/context | Do not assume unattended execution, push/background sync, file APIs or hotspot permission |
| Transfer to native mobile | No general automatic cross-container database sharing | Research-only protocol/remote ACK models | Managed network, peer discovery, user consent and same-owner authority **OPEN** |
| Data recovery | Export ≠ independent restore | Native component restore PASS at historical SHA | Physical Files egress/reopen/restore/MDM **OPEN** |

**LogMate policy authority:** [MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) specifies **manual** Sync; the server implementation is not certified by this master. A local save, outbox enqueue, remote commit, receipt, ACK, pull, reconcile and independent backup are distinct events. Correct UTC LWW semantics still do not guarantee user-intent chronological order under clock skew ([522](../522_stage8_offline_utc_lww_clock_trust_and_recovery_admission_20261027.md)). Automatic unattended mobile↔EFB transport, background sync, ads and offline persistence are **OPEN** until platform and policy evidence exists.

## 7. Required test/admission order

1. **P0 Engineering:** source-pinned populated 37-store deletion canaries, old-tab write rejection, concurrent saga and A→B normal startup/reopen; compare exact registry/store set and remote receipts. Test failure/rollback, not only happy path.
2. **P0 custody:** export user-allowed synthetic LBK to an actual independent Files location; read back and guarded-restore to fresh clean owner/replica state; validate all relevant stores/Sync metadata.
3. **P1 served NORMAL:** V1↔V2 Worker, old/new controller, corrupt/missing shell, quota/interruption, history/bfcache, report/header policy and cold offline restart on actual served HTTPS.
4. **P1 physical/managed:** independently test Safari tab, installed Home Screen and approved managed Web Clip contexts; record iPadOS version, MDM settings, storage mode, file policy and user-permitted connectivity.
5. **P2 UX/claims/quality:** screen reader/keyboard/reflow, recovery states, performance, accurate external support/deletion and Store claims.

All require attributable timestamp, source/build, browser/OS, fixture data, actual test start and outcome, negative control, independent validation and honest NON-EXECUTION handling. [Evidence register](EVIDENCE_VALIDATION_REGISTER.md) and [open decision queue](RESEARCH_GAPS_AND_SCHEDULE.md) are the operational entrypoints. **No product write or release authorization is created by this synthesis.**


## 8. 2026-11-07 source-pinned Hosting/Worker/cache/route-admission reconciliation [SOURCE / SYNTHESIS / CONTRADICTION / VALIDATION OPEN]

**New independent source check:** read-only LogMate `main@f4bcd2f7b7e77039e29653baa1cc93797673885b`, not a deployment assertion. Exact Git blob IDs: [firebase.json](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/firebase.json) `9ac0972e26749215c4a718360c66315c6caf3cc8`; [web/flutter_bootstrap.js](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/web/flutter_bootstrap.js) `a70625e8bda32aafd5dd23822c017d05229f0e63`; [web/manifest.json](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/web/manifest.json) `8225e76fe032e792c30b0f22efa1f7cafab68119`; [web/index.html](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/web/index.html) `01be77585ac40bf11e80777177a4ab08e4885671`; [web/account-deletion/index.html](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/web/account-deletion/index.html) `f8558e921c3f72743189a82d6f9cefe81b6fb193`; [web/auth/action/index.html](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/web/auth/action/index.html) `39d06a633ab7bee719b3401bc3ac744f8ba175d0`. Exact blob IDs avoid extrapolating beyond these files. No served request, device, browser or Firebase deployment was executed.

### 8.1 Three different cache authorities; an all-path no-store header is neither an offline kill switch nor an integrity proof

**SOURCE:** `firebase.json` declares Hosting public root `build/web` and a wildcard `headers.source="**"` rule with `Cache-Control: no-cache, no-store, must-revalidate`. This is a **source-level Hosting configuration**, not a captured live HTTP response. The [Firebase Hosting response priority](https://firebase.google.com/docs/hosting/full-config) places redirects before exact static matches, then rewrites; this is important for the Auth routes below. [MDN Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) distinguishes HTTP-cache no-store from revalidation, while [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) notes that no-store does **not** erase an already stored old response. The [Service Worker Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache) is explicit script-managed storage rather than automatic HTTP caching. **Critical limitation:** the cache API's handling of response headers, `Cache.put`, and each browser's storage policy must be tested; a blanket “no-store prevents all SW CacheStorage use” or “no-store guarantees data cannot persist” claim is false as a general security proof.

**SYNTHESIS:** There are at least **three independently controlled objects**: HTTP cache entries (server response freshness policy), Service Worker CacheStorage entries (application-script management) and IndexedDB ledger (transaction/data authority). The Hosting wildcard no-store is not equivalent to `CacheStorage.delete`, `caches.keys` inventory, authenticated release catalogue, browser storage deletion or independent backup. Conversely, a successful offline replay from CacheStorage does not prove that the deployed HTTP header policy is the intended one. On each critical URL, observe **both** actual served headers and actual Worker-controlled fetch/cache outcomes. Avoid recommending blanket `Clear-Site-Data` or cache clearing for a local-first ledger without a data-preserving migration/backup plan.

**TRANSFER VALIDATION:** Pin NORMAL artifact SHA, deployment channel and HTTPS origin. Record response body digest, `Cache-Control`, `Content-Type`, `Content-Security-Policy`, `Referrer-Policy`, SW controller, CacheStorage keys/headers, IDB inventory and cold-offline behavior for (a) `/` and `/index.html`, (b) `/flutter_bootstrap.js` and generated `/logmate_service_worker.js`, (c) `/manifest.json`, (d) `/auth/action?mode=...` using **fake codes**, (e) `/account-deletion`, and (f) one versioned font/icon. Verify with and without an old controlled tab, both online and cold offline. HTTP cache bypass and CacheStorage behavior must be reported separately. **NOT RUN**.

### 8.2 Bootstrap and installation identity: source evidence is narrower than installed-client proof

**SOURCE:** `flutter_bootstrap.js` registers `logmate_service_worker.js` at `new URL('./', document.baseURI)` scope, with `updateViaCache:'none'`, triggers `registration.update()` and uses `START_PRECACHE` and `PROMOTE_VERIFIED_CANDIDATE` messages. It deliberately does not block first Flutter paint on registration; `controllerchange` handler uses `{once:true}`. `web/index.html` uses Flutter's build-time `$FLUTTER_BASE_HREF` placeholder and references the manifest. The manifest has `start_url:"."` and `display:"standalone"`, but **no explicit `id` or `scope`** at this pinned blob.

**SYNTHESIS / LIMITATION:** A base-path build can change effective manifest/worker URL and navigation routing; the installed identity may derive from start URL where an explicit manifest `id` is absent. This is a **version/build/OS-dependent risk model**, not evidence of a broken installation. `updateViaCache:'none'` and `registration.update()` cannot certify the app-shell catalogue or whether the new worker controls the current document. The one-time controllerchange handler may be sufficient for an intended lifecycle but must be tested across repeated V1→V2 transitions, process restoration and old tabs before being called safe. The `PROMOTE_VERIFIED_CANDIDATE` message is a client request; only inspection and execution of the **generated actual Worker** can establish its verification guard and the atomicity or integrity of promotion.

**TRANSFER VALIDATION:** Build at root and intended non-root base path (if supported), record manifest resolved `id`/`start_url`/`scope`, registration scope, active/waiting/installing worker URL, controller identity and actual served bytes. Test first online paint → controlled reload → cold offline; V1 old tab while V2 waiting; restored Safari page; interrupted precache; two successive upgrades; origin/path change. Observe *whether* install identity and ledger container survive rather than assuming they do. Do not claim browser or managed-iPad compatibility from source inspection.

### 8.3 Public/Auth route boundaries: real paths and account-state promises

**SOURCE:** Hosting config rewrites `/auth`, `/auth/` and `/auth/action` to `/auth/action/index.html`. [Firebase Hosting response priority](https://firebase.google.com/docs/hosting/full-config) gives exact static matches priority over rewrites; deployed build output and trailing slash behavior must be checked, including `/auth/action/` and direct `/auth/action/index.html`. `web/auth/action/index.html` imports Firebase SDK from `www.gstatic.com` and parses `mode` and `oobCode` from the URL. The page sets `<meta name="robots" content="noindex">`; this is a crawler instruction, not a token-referrer or CSP security control. `web/account-deletion/index.html` tells the user to open Settings and choose deletion, or email support without reinstalling; it also describes remote and active-local deletion intent and exported-file exclusion. The current served site, actual Settings entry, mailbox operations, code handling, and remote deletion receipt are **NOT VERIFIED**.

**SYNTHESIS / CONTRADICTION:** A successful public page render cannot establish that the in-app deletion action exists, that support verifies and fulfills requests, or that the full local 37-store wipe occurs. The exact `529` 37/29 static gap remains an independent P0 and must not be obscured by reassuring public copy. A `noindex` meta tag cannot replace a route-specific `Referrer-Policy`, CSP, token-safe telemetry and a privacy-preserving redirect/callback design. Wildcard Hosting `Cache-Control` does not prove these headers exist in a served response. The third-party SDK import also requires source-specific script/CSP/failure testing rather than an assumption of safe offline authentication.

**TRANSFER VALIDATION:** For `/auth`, `/auth/`, `/auth/action`, `/auth/action/` and `/auth/action/index.html`, inspect exact HTTP status/redirect/rewrite, `Content-Type`, CSP, Referrer-Policy, no-store and `Location`, with synthetic `oobCode` and no actual account. Check a controlled and uncontrolled browser, new tab, back/forward, network failure and external referrer. Ensure sensitive query values are absent from analytics, logs, cross-origin Referer and UI error details. Separately verify public `/account-deletion` instructions against current Settings UI, support ticket intake/identity verification, deletion state/receipt and real P0 erasure oracles. Do not change LogMate/Marketing policy from Web Manager.

### 8.4 Cross-track decision table and stop boundary

| Track | Reusable owner / finding | Consumer and exact next evidence |
| --- | --- | --- |
| **A** | URL/base-path/manifest/SW scope and HTTP vs CacheStorage semantics | E release; C browser two-version/root-vs-subpath and cache inventory |
| **E** | Hosting route/header and Auth trust boundaries; deletion/backup claim custody | Engineering S007 deletion + actual served header/Auth and remote receipt; B/D claim restraint |
| **C** | Source-pinned negative controls and NORMAL build/served/device test provenance | A/E test result classification, Design Studio W121 accessible recovery |
| **B** | Offline/update/auth/deletion status must map to observed states and accessible journeys | Design Studio W121 and actual Settings/Files UI, not copy-only approval |
| **D** | Public account-deletion/discovery/indexability versus confidential action URL | Marketing claim parity and verified published URLs; `noindex` not a security substitute |

**MINTTAP DECISION / OPEN:** Keep **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**. This is a **new current-source multi-route/cache contract**, not an observed exploit, cache failure, actual user deletion problem or production regression. It does not supersede P0 deletion/Files. Highest independent information gain now is the **normal deployed HTTPS route/header/Worker acceptance packet** paired with the Engineering deletion packet. If the exact deployed origin or executable device is unavailable, preserve OPEN and transfer this source-pinned packet rather than rerunning the same static study.

**CHANGE WATCH:** Firebase Hosting priority/headers, browser Cache API handling, WebKit installed-container behavior, manifest identity semantics and Firebase Auth SDK all require version-pinned source checks at implementation/release. Primary docs consulted 2026-11-07; no production claims were tested.


## 9. 2026-11-07 — Restored-document authority is a distinct PWA release boundary [TRACK A→E/C/B/D; SOURCE / SYNTHESIS / VALIDATION OPEN]

**Question selected:** Existing `529` establishes a source-level old-writer/deletion-intent gap; `530` establishes Service Worker and storage state separation; `8 above addresses Hosting/Worker and Auth route control. A different unanswered case is a *browser-managed preserved document* resuming after a local or remote authority change. This section defines an **independent browser lifecycle acceptance packet**, not another static 37/29 re-count or an observed LogMate exploit.

### 9.1 History, platform standard and current browser behavior

**SOURCE (primary platform docs checked 2026-11-07):** [MDN `pageshow`](https://developer.mozilla.org/en-US/docs/Web/API/Window/pageshow_event) documents initial load, history traversal, mobile frozen-page restoration and the `PageTransitionEvent.persisted` discriminator. [Chrome Page Lifecycle](https://developer.chrome.com/docs/web-platform/page-lifecycle-api) distinguishes active/passive/hidden/frozen/terminated/discarded and explicitly warns that a discarded page may receive **no** event; Chromium-specific `freeze`/`resume` must not be treated as a universal Safari API. [Chrome/web.dev bfcache](https://web.dev/articles/bfcache) distinguishes a bfcache-restored DOM/JavaScript heap from a new navigation and notes that `pagehide.persisted=true` is an **intent**, not guaranteed successful caching. [MDN Service Worker lifecycle](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) distinguishes worker activation from control of already-open documents. The HTML session-history `pageshow`/`pagehide` semantics do not promise an account/owner reauthentication check.

**HISTORY → PRINCIPLE:** bfcache exists to avoid reconstructing a whole page and JS state for backward/forward navigation; that performance benefit can preserve *stale application assumptions*. A restored document can have a previously rendered authenticated screen, an in-memory draft and an old local owner token while another tab or device has requested deletion, switched UID, rotated authorization or upgraded the worker. A Service Worker shell-cache digest is irrelevant to the freshness of that in-memory state. A navigation with `pageshow.persisted=false` can still contain stale state if hydration relies on local memory or stale external data; conversely `persisted=true` does not prove a sensitive write occurred.

### 9.2 Five independent clocks and authority layers [SYNTHESIS]

| Clock/authority | Change while tab is hidden/frozen | What the returning page must *not* assume |
| --- | --- | --- |
| **Document/JS heap** | DOM/draft and callbacks may survive bfcache | Visible old account implies current owner permission |
| **Session/auth identity** | Firebase UID/token/reauth or account deletion may change elsewhere | Cached auth UI or local `currentUser` snapshot is an authorization proof |
| **Local ledger/owner epoch** | Another tab may persist deletion intent, erase stores or switch owner | Pre-hide owner ID and draft remain writable |
| **Worker/controller and app schema** | V2 can activate, new clients may get new controller/schema | Existing tab is automatically rehydrated or safe to mutate |
| **Remote receipt/Sync** | Backend deletion/sync admission may change while offline | An old outbox/ACK is accepted or safe to replay |

**Invariant (proposed for product owners):** every sensitive mutation must be authorized **at the durable write/transaction boundary** against the current local owner/deletion epoch and relevant remote authority; `pageshow`/`visibilitychange` can trigger UI revalidation, but are not the security gate. A new page can write before a late `pageshow` asynchronous callback finishes; a restored page may never receive a Chromium-only `resume` on Safari. A hidden tab may also write through an existing callback before any foreground event. UI controls should enter **pending revalidation** on restoration/identity ambiguity; show previously rendered private data only according to approved lock/privacy policy. Never clear or rewrite another owner's ledger merely because a lifecycle event fired.

### 9.3 Concrete cross-context fault matrix [TRANSFER VALIDATION — NOT RUN]

| Case | Setup / controlled intervention | Expected oracle | Distinct failure signal |
| --- | --- | --- | --- |
| **LC01 bfcache history** | A opens draft, navigates to same-origin neutral page; tab B persists A deletion intent; Back | `pageshow.persisted` recorded; no A write until transaction-time owner/phase recheck; lock/recovery state | A draft commit accepted after durable deletion intent |
| **LC02 no bfcache** | Same but force new load or browser evicts bfcache | Same deny-or-recover invariant; rehydration must not bypass guard | Fresh document writes as A |
| **LC03 background freeze** | A hidden; B requests deletion; resume foreground via tab switch, no history traversal | Visibility and platform event provenance; no old-owner writes | Logic only bound to `pageshow` misses tab-return |
| **LC04 process discard** | A hidden, OS/browser discards without callback, restart/reload | Durable lock checked before draft restore; no dependency on `pagehide` | Reopened stale draft or old owner |
| **LC05 old V1 client** | V1 A page stays open while V2 worker/controller changes and B deletes | Worker/version and ledger authority observed independently | Old client bypasses new phase/owner checks |
| **LC06 offline authority** | A offline; remote account deletion accepted on another device; A resumes without network | Explicit local-only/remote-unverified state, deny destructive cross-owner Sync and prevent false “deletion complete” | Claim of global deletion or accepted Sync without receipt |
| **LC07 restored Auth action** | Fake one-time `oobCode` in Auth URL, navigate away/back; observe URL/DOM/SDK/referrer and cached state | Token not transmitted to unauthorized destinations or reused without explicit validity; safe error state | Token in cross-origin Referer/telemetry or action repeated unsafely |
| **LC08 account B** | A draft open; sign out/switch B elsewhere; return to A tab | A data not presented as B or written into B ledger | Mixed owner rows, display or backup |
| **LC09 concurrent callback** | Start async A write; B commits deletion between UI check and IDB transaction | Write rejected at actual durable commit fence | Preflight-only check passes stale write |
| **LC10 UI recovery/AT** | Return from bfcache with deletion-pending, storage failure or offline | Accessible focus/live status, clear lock/restore path, no misleading “offline ready” | Silent spinner, inaccessible lock, lost pending state |
| **LC11 navigation/performance** | Compare same-origin Back/Forward with SW V1/V2 and message broadcasts | Record bfcache hit/miss and performance separately from security | Optimizing cache hit by removing required owner check |
| **LC12 managed WebKit** | Repeat permitted subset Safari tab, Home Screen app and approved managed Web Clip on disposable iPad | Per-container event sequence and independent data/readback, not Chromium inference | Unobserved app-resume or MDM-dependent data/Files behavior |

**Test packet requirements:** Record exact source/served artifact SHA, origin, browser/OS version, installation mode, MDM policy, UID A/B synthetic-only ledger, worker/controller version, `pageshow.persisted`, `pagehide.persisted`, `visibilitychange`, supported lifecycle events, old/new local owner epoch and deletion phase, actual transaction start/commit result, network and remote receipt, cache/IDB inventory and independent reopen. Use separate event-sequence and transaction oracle logs; a browser bfcache miss is not a security test failure if the negative-control variant is exercised. Force positive and deliberately unsafe controls in an isolated test harness; never use production EFB or real flight records.

### 9.4 Correctness versus performance, privacy and product UX

- **Track A owns** browser navigation/lifecycle capability matrix and Worker control. **Track E owns** owner authority, Auth and remote deletion safety. **Track C owns** reproducible exact-build browser tests and the distinction between `pageshow` occurrence and write-denial evidence. **Track B owns** focus and recoverable lock/offline/deletion states, consulting Design Studio W121. **Track D owns** truthful website/Store “resume,” “offline,” “sync,” and “account deletion” claims, and avoids counting bfcache returns as fresh installs or successful Sync.
- **Performance trade-off:** avoid unconditionally installing `unload` handlers merely to disable bfcache; doing so can reduce navigational performance and still cannot enforce transaction authority. A `pageshow` callback can refresh UI state, but it is **not** a substitute for durable mutation fencing. Worker broadcasts may change bfcache eligibility; evaluate performance and correctness as separate dimensions rather than hiding one to improve the other.
- **Privacy:** avoid logging UID, raw `oobCode`, backup content, auth tokens or flight data. Synthetic identifiers and hashed/aggregate event provenance are sufficient. A bfcache-restored private DOM is a **potential exposure scenario**, not evidence that LogMate displays it after deletion.
- **Offline:** remote deletion while disconnected cannot be observed immediately by an isolated device; any requirement for instant worldwide revocation needs an explicit product/network impossibility or limitation statement. Local deletion intent can still fence local writes if durably recorded in that container. Cross-container or remote revocation is a separate authority, not a magical browser event.

### 9.5 Judgment and bounded outcome

**NEW INTEGRATION:** The lifecycle test packet closes a *test-design gap* between the existing 529 old-writer source hypothesis and the 530 worker/storage acceptance plans: restored JS heap, hidden-tab resume, process discard and remote account change require independent tests with a **transaction-time fence oracle**. This is a new **VALIDATION DEFINED / NOT RUN** item, **not** a new product defect, production test PASS or change to the P0 deletion priority. Run LC01–LC09 with Engineering-owned exact LogMate source first; LC10–LC12 need Design Studio, physical browser/device and MDM permission. If current app is SPA-only and never traverses full documents, LC01 is a browser boundary/regression test rather than a presumed current user path; LC03/LC04/LC09 still apply. Do not infer iPadOS bfcache/freeze behavior from Chromium docs.

**Current gate unchanged:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD. No LogMate, Design Studio, Marketing or Engineering repository was changed. **Next material evidence:** exact old-owner mutation canary and observed page lifecycle on a served NORMAL PWA, followed by Files custody and managed WebKit tests.


## 10. 2026-11-07 — WebKit Home Screen ITP exemption ≠ durable managed-EFB storage [A lead; E/C/B/D transfer]

**Research question:** Does a Home Screen PWA on iPad escape Safari's seven-day script-storage deletion rule, and does that make a pilot ledger durable? **SOURCE:** WebKit [Tracking Prevention](https://webkit.org/tracking-prevention/) (checked 2026-11-07) explicitly exempts the **first-party domain of Home Screen web applications** from ITP's **seven-day cap** on script-writeable storage. The same primary source says Home Screen web-app data is **isolated from Safari**. Its general ITP rule includes IndexedDB, LocalStorage, Service Worker registration and cache. Thus “every iOS PWA always loses IDB after seven idle days” is false as a blanket statement; **a managed Web Clip has not been established to be the same installed context**. An ITP exemption is **not** a guarantee against quota pressure, eviction for other reasons, profile removal, device failure or loss of the sole copy.

**Separate SOURCE:** WebKit [Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/) (published **2023-08-10**, rechecked 2026-11-07) distinguishes per-origin quota, overall quota, origin-level eviction, `estimate()`, `persisted()` and `persist()`. Starting Safari 17/iPadOS 17, browser apps have **up to 60% disk per origin / 80% overall**, non-browser apps **up to 15% / 20%**; standalone Home Screen Web Apps have the **browser-app quota tier**. These are **upper bounds**, not reserved space. A quota-consuming write can throw `QuotaExceededError`. Persistent-mode grant is heuristic (Home Screen mode is one factor), not automatic; default origin storage is best-effort. Quota pressure and system pressure are independent of ITP's seven-day interaction rule. Browser-app vs managed Web Clip effective quota class is **OPEN** until exact container evidence exists.

### 10.1 Mechanism/context matrix — distinguish the authority of each claim

| Context | ITP seven-day rule | Quota/persistence | Custody and proof boundary |
| --- | --- | --- | --- |
| Ordinary Safari first-party tab | General interaction-based ITP rule documented; actual applicability and timing require observation | Browser quota tier, best-effort unless persisted | Not assumed to share IDB with Home Screen |
| Safari Private Browsing | WebKit describes per-tab ephemeral private sessions | Never rely on persistent ledger | Reject as sole logbook data home |
| User-added Home Screen standalone | **First-party ITP seven-day exemption** documented | Browser-app quota tier; `persist()` result still heuristic | Website data isolated from Safari; must independently test cold offline and backup |
| Managed Web Clip / company MDM | **UNKNOWN** if equivalent to Home Screen exception | **UNKNOWN** effective quota, persistent-mode grant and profile removal | Operator permission, container identity and Files egress must be tested |
| Third-party iframe/embedded context | WebKit partitions and makes third-party IDB/LocalStorage ephemeral | Partitioned storage/quota distinct | Cannot be assumed to reach first-party flight ledger |
| Native app | Not governed by PWA ITP claim | Separate OS/database semantics | Manual Sync/backup must be explicitly authorized and implemented |

**SYNTHESIS — four independent predicates:** `ITP_exempt` ≠ `persistent_mode` ≠ `quota_available` ≠ `independent_restorable_backup`. Installed icon, `persisted()===true` and an IDB transaction commit each prove different things. None proves managed-EFB permission or a second independent copy. Also, a Safari ledger cannot be assumed present after Home Screen installation just because the URL is identical; WebKit explicitly documents website-data isolation.

**Counterexamples / falsification:**
1. **False pessimism:** all installed iPad PWAs must lose IDB after seven idle days — contradicted by the Home Screen first-party exemption.
2. **False optimism:** ITP-exempt Home Screen installation guarantees records indefinitely — quota/eviction/profile/device loss remain.
3. **False equivalence:** managed Web Clip icon means user-added Home Screen container — no such mapping established by these sources.
4. **False backup:** a successful `persist()` call is an independent LBK backup — it is not.
5. **False migration:** Safari and Home Screen automatically share origin data — contrary to WebKit's documented isolation.
6. **False validation:** moving the device clock forward eight days proves actual inactivity retention — not a controlled elapsed-time test.

### 10.2 Physical acceptance packet WK01–WK16 [VALIDATION DEFINED, NOT RUN]

| ID | Controlled action / evidence oracle |
| --- | --- |
| WK01 | Record exact iPadOS, Safari/WebKit, app origin/manifest id, installed mode, MDM profile, product build/hash and test-owner authorization |
| WK02 | Normal Safari tab: seed synthetic owner A ledger, record `persisted()`/`estimate()`/SW/IDB and process-death reopen |
| WK03 | User-added Home Screen: same-origin **independent** seed; test whether Safari data is visible; never silently merge owners |
| WK04 | Managed Web Clip if policy permits: repeat container/storage/`persist()` observations independently |
| WK05 | Ordinary Safari tab 0/1/8/15 days of real elapsed inactivity, interaction diary, cold readback of IDB/SW/cache |
| WK06 | Home Screen 0/1/8/15 days, same controls; compare ITP exemption claim to observed outcome |
| WK07 | Managed Web Clip real elapsed inactivity under pinned MDM policy; record BLOCKED rather than invent support |
| WK08 | `persist()` grant and deny branches, including accessible UI and user-data preservation |
| WK09 | Safe bounded quota pressure on disposable device: catch `QuotaExceededError`; no success message for failed commit |
| WK10 | Interrupted SW install, owner edit, kill/restart; distinguish shell/worker/ledger and last committed record |
| WK11 | Managed profile removal/reinstall **only on approved disposable device**; observe effect on data/recovery |
| WK12 | Private Browsing ledger attempt: identify non-durable context and prevent unsupported retention promise |
| WK13 | Export owned synthetic LBK to policy-permitted **independent Files** destination; read back and verify artifact |
| WK14 | Fresh empty container/device guarded LBK restore: compare owner, all stores, Replica/Sync and negative rollback |
| WK15 | Cold offline followed by **manual** native↔PWA Sync; require authenticated remote receipt/ACK, no hotspot assumption |
| WK16 | B/C/D accessible offline, storage, backup, install, delete and recovery copy: prohibit “permanent offline storage” claim |

**Evidence minimum:** source/build SHA, real OS/browser/container/MDM, elapsed time, synthetic canary inventory, positive/negative controls, independent readback, exact outcome and reviewer. A policy page is **SOURCE**, not WK PASS. Real idle time is not replaceable by system-clock adjustment. No destructive probe on an operational EFB.

### 10.3 Transfer and decision

- **A** owns WebKit ITP/storage/container mechanics; **E** owns owner deletion, independent Files custody and operational recovery; **C** owns physical controlled WK test provenance; **B** owns truthful accessible offline/backup/error states with Design Studio W121; **D** owns no unverified Store/website claims and Marketing D9 handoff.
- **MINTTAP DIRECTION / OPEN:** A physical managed-iPad matrix must distinguish ordinary Safari, user-added Home Screen and managed Web Clip, while independently verifying backup/restoration. This does **not** change LogMate's Manual Sync contract or approve company EFB deployment.
- **CHANGE WATCH:** WebKit's ITP, quota, installed app and MDM policies are version-specific. Recheck first-party source and real device before release. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD** unchanged.


## 11. Identifier-first email entry versus enumeration protection — exact LogMate Auth/PWA boundary (2026-11-07)

**Owner:** E Security/Trust (lead); A HTTP/Firebase/platform transfer; B identifier-first task and recovery UX; C evidence/oracles; D site/Store/privacy claim integrity. **Classification:** SOURCE (pinned read-only product source), STANDARD/PROVIDER PRIMARY (Google), SYNTHESIS, PRODUCT DECISION (already approved by LogMate owner), OPEN/VALIDATION. This is **not** a product vulnerability finding, a Firebase Console observation, a provider-config change or an authorization to redesign approved onboarding.

### 11.1 Historical problem and architectural collision

An identifier-first flow simplifies Email entry: enter address → determine whether to show Sign in or Create account. That flow requires the client to learn an account-existence bit. Email enumeration protection deliberately removes unauthenticated account-existence signals. This is a genuine **privacy versus product-UX/compatibility tension**, not a PWA install or SW caching defect.

- **PRODUCT AUTHORITY:** [LogMate MASTER](https://github.com/yhappcom/logmate/blob/main/MASTER.md) and [startup-and-auth-entry-spec](https://github.com/yhappcom/logmate/blob/main/docs/specs/startup-and-auth-entry-spec.md) explicitly approve identifier-first, lookup-derived Sign in/Create routing, and acknowledge enumeration tradeoff. Product owner has **not** approved a different flow here. Current exact product runtime and Firebase Console policy remain **OPEN**.
- **SOURCE pinned 2026-11-07:** [email_account_lookup.dart](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/lib/auth/email_account_lookup.dart), blob `8677b1317d0baf1da8d1690735771a5cdc15e690`, POSTs JSON `identifier` and `continueUri` to `identitytoolkit.googleapis.com/v1/accounts:createAuthUri` with platform Firebase API key. It **requires** JSON `registered` to be a boolean, mapping true→existing and false→new; non-2xx, missing/non-boolean, malformed response or transport failure becomes typed `EmailAccountLookupFailure`. No Auth session mutation is made by this lookup.
- **SOURCE pinned:** [email_account_lookup_test.dart](https://github.com/yhappcom/logmate/blob/f4bcd2f7b7e77039e29653baa1cc93797673885b/test/auth/email_account_lookup_test.dart), blob `283e783cf7abde7d6cbfaf54464aeb3990eedb89`, includes **mock-defined** true/false, missing registered, malformed JSON, non-2xx and transport failure. Test code exists; **not executed this cycle**, not actual protected/disabled Firebase response.
- **PRIMARY provider (checked 2026-11-07, last updated 2026-11-03 UTC):** [Google Identity Platform enumeration protection](https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection) says projects created from 2023-09-15 default to protection enabled; `createAuthUri` no longer returns sign-in method lists, and recommends migration away from behavior dependent on that signal. The exact LogMate project creation date and setting are **UNKNOWN**.
- **PRIMARY API (last updated 2026-03-10 UTC):** [accounts.createAuthUri](https://docs.cloud.google.com/identity-platform/docs/reference/rest/v1/accounts/createAuthUri) documents `registered` in the generic response schema and says protection yields an empty provider list. **Important nuance:** Google primary text specifically guarantees removal of sign-in methods, not an unconditional promise about presence/absence of `registered` across all backend configurations. Do **not** assert “protected always omits registered” as a proven platform invariant. The LogMate mock with `{"sessionId":"lookup-only"}` demonstrates fail-closed parsing **only for that mock**; actual protected-project behavior must be captured using synthetic test addresses.

**CONTRADICTION / TRANSFER VALIDATION:** The approved product flow depends on a pre-auth signal that Google's recommended privacy mode is designed to suppress. If the protected backend omits `registered`, LogMate's typed failure prevents accidental “new account” misrouting (good fail-closed behavior), but it may leave all legitimate Email users unable to proceed (availability/UX regression). If the backend returns `registered`, verify the privacy tradeoff and abuse controls. **Neither outcome has been observed on LogMate's production Firebase project in this cycle.**

### 11.2 Trust boundaries and why unrelated controls do not close them

1. **Browser/HTTP:** Firebase API key identifies the project; it is not equivalent to a private backend authorization credential. Public-client access to an account-existence endpoint must be evaluated as public even when the request originates from a Flutter PWA. A website's CSP, CORS or `no-store` header does not itself prevent an arbitrary non-browser caller from querying an exposed Identity Toolkit API. Do not “fix” by hiding the client API key or adding only front-end rate limits.
2. **Provider setting:** protected vs unprotected enumeration is a server-side Google project configuration; no source-only test can prove the live setting. Firebase Emulator behavior is useful for deterministic client-contract tests, not necessarily identical to a production project's anti-enumeration configuration.
3. **Data minimization:** the submitted `identifier` is personal information; `continueUri` is a redirect context, not permission to include email/UID in URL. The current web default uses `Uri.base`; exact production URL/query and redirect allowlist must be checked for query token, account identifier and referrer leakage. No evidence of an actual leak is claimed.
4. **SW/cache:** LogMate's app-shell precache and HTTP `no-store` policy are separate from a direct HTTPS POST to Google's origin. Audit whether any Worker intercepts or logs it, but do not assume an app-shell cache automatically stores the POST or response. Never cache lookup responses keyed by email in shared CacheStorage or analytics.
5. **Offline:** identifier lookup requires an authenticated backend response even though the lookup itself is pre-auth. Existing unlocked same-UID offline ledger use is a **different** LogMate startup policy. An offline first-time Email sign-in/create flow cannot be promised from app-shell availability; retry state must not infer existing/new from a stale lookup.
6. **Account owner:** `registered` is **not** UID ownership, proof of mailbox control, verified session or ledger-binding authority. Only verified Firebase UID after Auth and the product's owner fence can unlock a ledger. The existing design preserves this distinction; tests must retain it.
7. **Abuse/availability:** client-side debouncing, generic messages and telemetry scrubbing reduce UX noise but do not enforce provider-wide request quotas against direct calls. Rate-limit, App Check/reCAPTCHA applicability and monitoring need provider-specific configuration/operational evidence; Google explicitly recommends App Check/reCAPTCHA for signup endpoints that can still reveal `EMAIL_EXISTS`.
8. **Accessibility/privacy UX:** B must preserve the approved initial email-only screen while proposing recovery for lookup unavailable, rate-limited, network offline, ambiguous results and account-provider collisions. Avoid “no account exists” copy unless authoritative signal is present. C/Design Studio W121 owns keyboard/focus/AT/reflow/error-state evidence; no new design implementation is authorized.
9. **External deletion/support:** a user who cannot pass identifier lookup must still have a truthful externally accessible deletion-request/support route. Engineering S007 owns identity/deletion saga; Web B/E owns reachable web entry, D/Marketing only claims accepted operation. Do not couple account-deletion requests to successful in-app lookup.
10. **Policy drift:** Firebase's default depends on project creation date and actual current setting; browser behavior and SDK versions vary. A future provider policy change can break routing without a LogMate code change. Monitor actual response shape and fail-closed user messaging with privacy-safe aggregate error codes, never email addresses.

### 11.3 Falsifiable acceptance matrix (EL01–EL14; **DEFINED, NOT RUN**)

| ID | Controlled scenario | Expected observable/oracle | Status |
| --- | --- | --- | --- |
| EL01 | Owner-approved disposable Firebase project with enumeration **enabled**, known existing test email | Capture redacted `registered` field presence/type and route; never use real account | OPEN |
| EL02 | Same protected project, unknown synthetic email | Compare response shape/status; no inferred account state from missing field | OPEN |
| EL03 | Separate authorized test project with enumeration **disabled** | Measure synthetic existing/new response; identify leakage risk and controls, not production approval | OPEN |
| EL04 | Exact LogMate lookup against response without `registered` | Typed failure; no implicit Create account, no UID/ledger write | Mock source exists; exact integration OPEN |
| EL05 | HTTP 429/5xx, timeout, offline, malformed JSON | No existing/new inference; accessible retry, no persistent secret log | OPEN |
| EL06 | Duplicate Continue / rapid taps / cancel / back / edit email | Latest request only, stale response cannot reroute different address | OPEN |
| EL07 | Native iOS/Android versus Safari tab/Home Screen PWA | Same backend project/setting; bounded platform-specific `continueUri` and error UX | OPEN |
| EL08 | PWA SW V1/V2 and page bfcache restore | No stale email lookup response, Auth session or old-owner ledger reuse | OPEN |
| EL09 | CSP, Referrer-Policy, cross-origin POST and telemetry | No email/query/token in page URLs, referrer, cache, logs, analytics or crash reports | OPEN |
| EL10 | Auth provider collision, Google/Apple private relay | No email-based UID merge/rebind; same-UID verification controls | OPEN |
| EL11 | Password reset for existing/unknown synthetic email | Generic delivery copy; response not promoted to existence oracle | OPEN |
| EL12 | Legitimate repeated probes, IP/identifier abuse and throttling | Dated operator-side quota/monitoring/App Check/reCAPTCHA applicability and evidence | OPEN |
| EL13 | PWA cold offline launch before first Auth | Shell readiness not misrepresented as ability to complete Email lookup; explicit retry | OPEN |
| EL14 | External account-deletion/support entry when lookup unavailable | Independent usable request path and identity verification; no app-reinstall prerequisite | OPEN |

**Decision table (not new product policy):** 
- **Observed `registered` + documented acceptable privacy controls:** Engineering/product owner can evaluate maintaining approved routing, explicitly accepting enumeration risk with server-side controls; privacy review required.
- **Observed no `registered` with protection enabled:** Engineering must propose an owner-approved compatible UX/flow or an explicitly authorized configuration tradeoff; Web Manager cannot silently turn off protection or infer new-account state.
- **Inconsistent, 429, offline or ambiguous:** fail closed for routing/ledger, show accessible retry/support and record privacy-safe operational error classification.
- **No operator response/config evidence:** **UNKNOWN**; do not claim either privacy PASS or Email onboarding production PASS.

**HANDOFF:** Engineering Auth owns exact product integration, Firebase Console/Identity Platform configuration and server-side controls; Web E owns threat/HTTP privacy; A owns PWA/browser transfer; B/C + Design Studio W121 own accessible recovery; D + Marketing D9 owns public claim HOLD. Product owner retains approved identifier-first policy authority. No product/peer writes, no live-user enumeration tests, no runtime result or gate promotion in this research.

### 11.4 Browser URL provenance and identifier-lookup transport — exact-source transfer (2026-11-07)

**SOURCE:** LogMate `lib/auth/email_account_lookup.dart` blob `8677b1317d0baf1da8d1690735771a5cdc15e690` defines `_defaultContinueUri()`: on Web it returns `Uri.base`; on native it constructs the project's `firebaseapp.com/` root. The resulting string is included in the HTTPS JSON body as `continueUri` alongside `identifier` for Google's `accounts:createAuthUri`. The source does not first strip a Web URL's query or fragment. The active page URL may contain route-specific query or fragment state; whether any such state is sensitive, what exact URL is supplied at runtime, and how the provider handles it are **UNKNOWN**. Sending a URL in an HTTPS request body is **not** proof of public referrer leakage, logging or a data breach. Conversely, the request body is a separate disclosure boundary not closed by `Referrer-Policy` alone.

**SYNTHESIS / E+ A dependency:** distinguish four paths: (1) page navigation URL and history; (2) request-body `continueUri` delivered to Identity Toolkit; (3) outgoing HTTP `Referer` header controlled by browser/referrer policy; (4) first-party/third-party logs and analytics. A sanitized, fixed, allowlisted `continueUri` could reduce accidental URL-state transfer, but **MINTTAP DECISION OPEN**: Engineering and the product owner must first verify any legitimate redirect/flow dependency before changing the approved identifier-first behavior. A front-end CSP or `no-store` header does not sanitize the JSON body.

**VALIDATION — additional exact oracles (DEFINED, NOT RUN):**

| Case | Controlled input and observation | Required interpretation |
| --- | --- | --- |
| URL01 | Synthetic Web page `/welcome?probe=public-marker#local-fragment` and intercepted mock HTTP client | Record exact JSON `continueUri` and ensure no real credentials; determine whether both query and fragment are propagated by the source-pinned build |
| URL02 | Synthetic `/auth/action?mode=...&oobCode=TEST_ONLY` while lookup is invoked | Determine reachability and payload propagation; **do not** use live action codes or assume this route invokes lookup |
| URL03 | Ordinary `/welcome` vs deep-linked route, Web vs native | Verify redirect semantics and approved UX after any candidate URL normalization; distinguish client default from provider redirect behavior |
| URL04 | Actual served HTTPS route with privacy-safe network capture | Inspect request-body field, `Referer`, browser history, SW interception and redacted telemetry separately; no unapproved real-user testing |
| URL05 | bfcache restored route or tab A→B transition while lookup is pending | Old request must not override latest identifier or rebind a UID; coordinate with LC/EL oracles and Engineering ownership fence |

**TRANSFER / CONTRADICTION:** Track A owns `Uri.base`/navigation mechanics; E owns payload and trust boundary; B owns routing/error recovery; C owns exact-browser reproducibility and accessibility; D owns no-PII analytics/referrer claims. Engineering owns executable Flutter source tests and any source change. Marketing must not claim email privacy or onboarding readiness from this source inspection. **CHANGE WATCH:** Google Identity Toolkit response and browser referrer rules should be rechecked when provider/platform versions change. This narrows EL09 rather than declaring an incident or new release gate.

**Current gate:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.
