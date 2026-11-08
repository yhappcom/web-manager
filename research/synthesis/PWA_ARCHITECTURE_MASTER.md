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


### 11.5 Fragment confidentiality is transport-specific, not an absolute secrecy guarantee — normative reconciliation (2026-11-07)

**HISTORY / PROBLEM:** URI fragments were designed for client-side resource subidentifiers. Browser navigation normally omits the fragment from the HTTP request target; engineers sometimes incorrectly extrapolate that rule into “the fragment can never leave the device.” A JavaScript/Dart client that reads and serializes the complete page URL into an API JSON body creates a *different* explicit transport. This distinction is material to LogMate's `Uri.base` → `continueUri` mapping in §11.4.

**SOURCE / STANDARD:** The [WHATWG URL Standard §4.5](https://url.spec.whatwg.org/#url-serializing) defines serialization with `exclude fragment` defaulting to false: the fragment is appended unless the caller explicitly requests exclusion. [MDN URI fragment](https://developer.mozilla.org/en-US/docs/Web/URI/Reference) distinguishes the browser's resource request (fragment not sent) from application code; [MDN Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referer) states that a `Referer` header cannot contain a fragment, while path/query inclusion depends on [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy). These statements concern **different sinks**. A string inserted by application code into an HTTPS JSON POST body is not a browser-generated Referer header and is not automatically sanitized by referrer policy.

**SOURCE / PRODUCT:** [LogMate exact source](https://github.com/yhappcom/logmate/blob/main/lib/auth/email_account_lookup.dart) at blob `8677b1317d0baf1da8d1690735771a5cdc15e690` returns `Uri.base` on Web and serializes `_continueUri.toString()` into `accounts:createAuthUri` request JSON. No fragment/query removal is visible at that source point. This is a **source-level potential transfer**, not observed provider receipt, production-sensitive token presence, an HTTP Referer violation or a demonstrated breach. Provider-side parsing/validation of `continueUri` and actual runtime URLs remain **OPEN**.

**SYNTHESIS / failure-domain matrix:**

| Sink / operation | Fragment behavior supported by standard/source | Decision consequence |
| --- | --- | --- |
| Browser navigation request target | Fragment excluded from the resource request | Does not prove secrecy from page scripts |
| Browser-generated `Referer` header | Fragment excluded; query/path depend on policy | Header capture alone cannot test JSON-body exposure |
| URL serializer used explicitly by application code | Standard permits fragment inclusion by default | Exact Dart `Uri.base.toString()` mock test required |
| Identity Toolkit JSON `continueUri` field | Application source supplies full serialized URI | Observe synthetic request body and provider validation separately |
| Browser history, crash reports, analytics, SW or application logs | Implementation-specific | Inspect each independently; do not infer capture or non-capture |
| Native `firebaseapp.com/` default | Does not use Web `Uri.base` in cited source | Native and Web require distinct acceptance oracles |

**VALIDATION / falsifiable integrated exercise (FR01–FR08; DEFINED, NOT RUN):** FR01 controlled Web URI with query and fragment, inspect `http.MockClient` JSON; FR02 fragment-only and query-only cases, compare; FR03 test `continueUri` with percent-encoded delimiter and Unicode to detect accidental decoding or double encoding; FR04 test page navigation request and HTTP `Referer` independently from JSON body; FR05 repeat under `strict-origin-when-cross-origin` and `no-referrer`, expecting no JSON-body sanitization from either header; FR06 verify whether the email lookup is reachable from an Auth action/deep link before claiming any action-code risk; FR07 compare Web, Android and iOS defaults with synthetic inputs and confirm no cross-account routing; FR08 test any proposed fixed allowlisted `continueUri` against existing approved redirect flows, including failure recovery and account-deletion support. Tests must use synthetic markers, no live one-time codes or real user emails.

**MINTTAP DECISION / OPEN:** Do not assert a token leak or silently change LogMate's approved identifier-first Auth flow. Engineering owns runtime interception, redirect compatibility and any code change; E owns data-flow privacy threat analysis, A owns URL/referrer standards, B owns route/recovery, C owns reproducible browser and assistive-technology checks, D owns analytics minimization and claim discipline. **DEPENDENCY:** Firebase Console configuration and actual provider response/redirect semantics. **CHANGE WATCH:** URL/Fetch/referrer standard updates and provider endpoint behavior; browser/OS differences require targeted tests rather than a blanket Safari/Chromium assumption. **TRANSFER VALIDATION:** Referrer-Policy is valuable defense in depth but cannot be credited as mitigation for an explicitly constructed JSON body. Product validation remains OPEN; release HOLD.


## 12. Service Worker fetch boundary and owner-safe offline response classification (2026-11-07)

**Stage 8 E-led, A platform owner, C test oracle, B recovery, D telemetry. Evidence: SOURCE/SYNTHESIS, NOT product execution.** This is an independent extension of §8 Hosting/Worker and §§9–11 account/lifecycle/URL analysis; it does not repeat their test packets. **Research question:** when a controlled LogMate-like PWA makes network requests, which response classes may be reused across owner changes, and which must never be treated as an offline shell? The question is separate from whether an HTTP server sets `Cache-Control: no-store`, whether the browser considers the app installed, and whether local IndexedDB is preserved.

### 12.1 History → principle → standards → limitations

**HISTORY / FAILURE MODEL:** AppCache blurred app-shell availability with response freshness. Service Workers introduce a programmable fetch decision, but programmability creates an additional trust boundary: an app-controlled Worker may return a stored or synthetic response in place of the network result. An apparently successful offline navigation is not proof that a user's authenticated ledger, token, provider response or write authority is fresh. Conversely, an uncached API failure need not mean the static application shell is unusable.

**SOURCE (checked 2026-11-07):** [MDN ServiceWorkerGlobalScope fetch event](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/fetch_event) documents interception of page navigations and subresource requests for controlled clients; [MDN FetchEvent.respondWith](https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent/respondWith) describes the explicit replacement-response path and response-type restrictions; [web.dev Service Workers](https://web.dev/learn/pwa/service-workers) distinguishes first load/no controller from later controlled clients and cautions that Worker support/control is not universal. These are generic platform mechanics, **not** evidence that LogMate's built artifact intercepts a particular request. Cache API and HTTP cache are distinct; a blanket Hosting `no-store` header is not proof that application-managed CacheStorage or IndexedDB contains no entries. Worker script update checks, cached shell version and per-client controller are also independent.

**CURRENT SOURCE PIN:** LogMate `main` on 2026-11-07: [firebase.json](https://github.com/yhappcom/logmate/blob/main/firebase.json), blob `9ac0972e26749215c4a718360c66315c6caf3cc8`, configures `Cache-Control: no-cache, no-store, must-revalidate` for Hosting paths; [web/index.html](https://github.com/yhappcom/logmate/blob/main/web/index.html), blob `01be77585ac40bf11e80777177a4ab08e4885671`, loads `flutter_bootstrap.js`; [web/manifest.json](https://github.com/yhappcom/logmate/blob/main/web/manifest.json), blob `8225e76fe032e792c30b0f22efa1f7cafab68119`, uses relative `start_url` and `standalone` display. [email_account_lookup.dart](https://github.com/yhappcom/logmate/blob/main/lib/auth/email_account_lookup.dart), blob `8677b1317d0baf1da8d1690735771a5cdc15e690`, POSTs to the external Identity Toolkit origin. These source facts **do not reveal the final built Worker fetch handler or CacheStorage catalogue**; built assets and served headers remain OPEN. The historical source review in §8 must not be promoted to runtime behavior.

### 12.2 Explicit response-class policy to validate, not silently implement

| Request/response class | Candidate operational judgment | Critical contradiction / required evidence |
| --- | --- | --- |
| Versioned static Flutter JS/CSS/fonts/icons | Immutable/version-bound app-shell caching may support offline launch | Asset content hash, V1/V2 coherence, failed install, mixed controller and rollback; an old shell must not silently write to a newer owner/schema |
| Navigation `/` and approved app routes | Explicit offline shell fallback can be useful | Exclude `/auth/action`, deletion/support, token-bearing and server-specific responses; verify navigation mode, final URL, MIME, HTTP errors and redirect chain |
| Firebase `accounts:createAuthUri` and other identity calls | No offline replay of existence/session/verification response; network-required operation | A controlled page can issue cross-origin requests through its Worker; prove actual request route, no CacheStorage/telemetry copies and fail-closed UI when disconnected |
| Auth action / password reset / email verification | One-time token processing and navigation must remain live and time-bounded | Generic shell fallback or stale cached action page cannot be credited as successful verification; preserve independent public support path |
| Owner-bound Sync/replica API and ledger exports | Never classify a cached network response as fresh owner authorization or accepted sync receipt | Transaction-time UID/owner fence, receipt provenance, old-tab revocation, 37-store deletion and file custody require separate Engineering tests |
| Public website marketing/help pages | May use a separately reviewed cache strategy with freshness bounds | Product/Store claim version, external deletion reachability, privacy text changes and search index must not be frozen by offline fallback |
| Error/redirect/opaque responses | Do not indiscriminately cache or treat as success | Verify response status/type/redirected URL, Vary/credentials, authentication context and cache key; cache API behavior differs from HTTP cache |

**SYNTHESIS:** Request method and URL alone are insufficient to classify a response. A GET can be private; a navigation can contain an action token; a response can redirect; a Worker can synthesize a 200 shell for a server 404. A useful test therefore records request mode/destination/method, origin, redirect/result status, content type, controller identity, cache key and owner state. The policy above is a **review contract**, not a statement that current LogMate violates it.

### 12.3 Falsifiable integrated test packet FC01–FC12 (DEFINED, NOT RUN)

| ID | Exact test stimulus | Pass/fail oracle |
| --- | --- | --- |
| FC01 | Clean first visit and subsequent controlled visit to the same source-pinned served build | Record `navigator.serviceWorker.controller`, registration scope and network/Worker path; first-load assumptions are not copied to controlled visits |
| FC02 | Enumerate `caches.keys()` and sanitized request URLs in each cache | Catalogue shell versus auth/owner responses without dumping credentials, identifiers or payloads |
| FC03 | Offline navigation to `/`, a valid app route, and unknown route | Shell availability distinguished from valid route, HTTP 404 and data readiness; no fabricated success |
| FC04 | Offline navigation to `/auth/action` with synthetic, nonfunctional code | No stale verification success, token replay or misleading generic shell as completed Auth |
| FC05 | Synthetic Email lookup with controlled network failure, including old controlled client | No cached account-existence result; fail-closed lookup, no UID/ledger mutation, accessible retry |
| FC06 | A→B owner change while old A page remains controlled by Worker V1 | A page denied at transaction time regardless of cached shell or stale response |
| FC07 | V1 Worker active, V2 waiting, one tab offline, then interrupted V2 install | Per-client shell/controller/cache version recorded; no partial mixed bundle treated as release PASS |
| FC08 | Server 302/401/404/500 for a test route while online/offline | Status and redirect distinguished from Worker-generated 200 fallback; no success telemetry from fallback |
| FC09 | Authenticated synthetic GET and response with `Vary`/credential differences | No cross-owner or cross-credential cache replay; test actual cache keys and response classes |
| FC10 | Delete/recreate local storage and reopen installed PWA | Distinguish CacheStorage shell, IndexedDB owner data, SW registration and independent Files artifact |
| FC11 | Safari tab, Home Screen and managed Web Clip on approved physical iPad | Repeat relevant FC cases with OS/MDM policy and storage partition recorded; no Chromium PASS transfer |
| FC12 | Rollback after V2 deploy with B account and offline pending edits | No old shell bypass of schema/owner fence; rollback preserves export/recovery and does not silently acknowledge sync |

**VALIDATION / EVIDENCE MINIMUM:** Exact LogMate source SHA and built artifact hash; served HTTPS URL and dated response headers; OS/browser/installation mode/MDM policy; controlled client and Worker script hashes; sanitized cache inventory; synthetic A/B account and token fixtures; expected/observed and deliberate negative controls; independent Files restore; reproducible invocation. For each FC test classify PASS/FAIL/NON-EXECUTION/INCONCLUSIVE, never substitute an MDN example or a synthetic fixture for NORMAL product behavior. Product tests and any remediation are Engineering-owned; Web Manager supplies acceptance, threat and evidence adjudication.

### 12.4 Cross-track transfer and operational decision

- **A → E:** Fetch interception is an origin/client-control mechanism, not a blanket permission to persist user data or an identity authority. A owns browser/Worker semantics; E owns cache admission, private response and account-lifecycle threat decisions.
- **E → C:** C must run positive and deliberately unsafe negative controls; Lighthouse or synthetic Chrome-only offline PASS cannot close Safari/managed-EFB, owner deletion, or file custody.
- **E → B:** Offline shell, offline existing-user ledger, offline first-time Auth and offline sync acknowledgement are four distinct UX states. Provide truthful retry/recovery and accessible status without claiming unverified persistence.
- **E → D:** Installed-PWA analytics must not transmit email, auth codes, owner IDs or query fragments; successful shell load is not evidence of successful acquisition, authentication or sync. Marketing's PWA/claim HOLD remains authoritative.
- **DEPENDENCY / CONTRADICTION:** Engineering S007 deletion saga, Design Studio W121 runtime/accessibility gate and Marketing D9 release HOLD remain separate. No peer repo is changed.
- **MINTTAP DECISION:** Keep PWA release HOLD pending exact served-build Worker/cache/owner tests and physical EFB custody. No new product policy or code change is approved.
- **CHANGE WATCH:** Recheck browser-specific Worker navigation fallback, install/MDM policy, response/cache behavior and actual Flutter generated artifacts at each release; avoid a generic Safari=Chromium assumption.

**Next adjacent high-value question:** derive the exact built Worker registration/fetch-handler inventory and test its route exclusions on an authorized served artifact. If build/operator access is unavailable, preserve the FC packet as OPEN and pivot to independent public support/deletion availability or accessible offline-recovery evidence rather than reiterating the same static source.


## 13. Navigation preload, Worker startup and private-route integrity (2026-11-07)

**Stage 8 integrated specialization: A platform owner → E admission/security → C runtime quality → B recovery → D measurement. Classification: SOURCE / SYNTHESIS / TRANSFER VALIDATION / OPEN; no product runtime executed.** This addresses an independent optimization-versus-trust question not resolved by §12's response-class taxonomy: *can parallel network navigation improve startup without sending unintended requests, duplicating fetches, bypassing offline policy or misclassifying sensitive routes?*

### 13.1 Problem, standards and platform boundary

**HISTORY / DESIGN PRINCIPLE:** Service Workers may need startup time before their fetch handler can decide whether to serve a navigation from cache or network. Navigation preload allows the browser to initiate a navigation request while the Worker starts. It is an **opt-in network optimization**, not precaching, not background sync, not a durability mechanism and not a general-purpose API-request accelerator. An offline-first EFB shell that intentionally answers from local cache may derive no benefit from speculative network navigation, and could incur needless radio/network activity.

**PRIMARY / PLATFORM SOURCE (checked 2026-11-07):** [MDN ServiceWorkerRegistration.navigationPreload](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/navigationPreload) describes the registration manager and secure-context constraint; [MDN Using Service Workers, navigation preload](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers#service_worker_navigation_preload) documents enablement in activation and consumption via \`FetchEvent.preloadResponse\`; [MDN FetchEvent.preloadResponse](https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent/preloadResponse) states the promise resolves to a response only for an eligible preloaded navigation, otherwise \`undefined\`. The navigation-preload request may include the [\`Service-Worker-Navigation-Preload\` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Service-Worker-Navigation-Preload); a server returning a variant based on this header must use the appropriate \`Vary\` policy. API availability is not proof of an enabled registration or correctly handled response.

**Standards versus implementations:** The Service Worker mechanism defines registration-level preload and event response handling. Chromium, Firefox and Safari/WebKit versions have different historical support and device lifecycle constraints. MDN currently describes broad availability, but **managed iPadOS policy, a specific Safari version, installed Home Screen context and the deployed LogMate Worker must each be checked separately**. No claim of continuous background operation, cellular transport permission, reliable connectivity or MDM Web Clip parity follows from navigation-preload support.

**SOURCE PIN / LIMITATION:** LogMate \`main\` on 2026-11-07 has [\`firebase.json\`](https://github.com/yhappcom/logmate/blob/main/firebase.json) blob \`9ac0972e26749215c4a718360c66315c6caf3cc8\` with wildcard HTTP \`no-store\`; [\`web/index.html\`](https://github.com/yhappcom/logmate/blob/main/web/index.html) blob \`01be77585ac40bf11e80777177a4ab08e4885671\` loads Flutter bootstrap; [\`web/manifest.json\`](https://github.com/yhappcom/logmate/blob/main/web/manifest.json) blob \`8225e76fe032e792c30b0f22efa1f7cafab68119\` has relative start URL. **Neither those files nor a missing \`web/sw.js\` path establish whether the generated deployed Worker enables preload.** Exact \`build/web\` Worker, registration state, HTTP responses and request traces remain **OPEN**.

### 13.2 Failure-mode analysis and admission contract

1. **Cache-first double work:** If a navigation is preloaded but the Worker immediately serves a cached shell, the network request may be wasted. If the handler also calls \`fetch(event.request)\` instead of consuming \`event.preloadResponse\`, a duplicate network request is possible. Never interpret duplicate requests as evidence of malicious interception without a controlled trace.
2. **Sensitive-route prefetch:** Navigation preload is a browser navigation, not a Firebase POST replay. Nevertheless, a navigation to an auth-action URL, deletion route, token-bearing link or owner-dependent page can be sent to the server before the Worker selects a cache response. The Worker route policy must not assume it can prevent a preload already started. Do not place sensitive tokens in diagnostic URLs or preload logs.
3. **Redirect/status ambiguity:** A preloaded navigation may follow redirects and yield error pages. Returning an app shell with HTTP 200 after an actual 401/404/500 can misrepresent success; inspect final URL, status, content type, \`redirected\`, navigation destination and Worker response separately.
4. **Header variation and cache keys:** If the server intentionally changes content for the preload header, correct \`Vary\` handling and CacheStorage admission must be assessed. Do not cache user-specific HTML or auth responses as a reusable shell based only on URL/method.
5. **Offline-first versus network-first:** Offline startup must remain viable without a preload response. If the Worker waits on a failing network request before consulting an already-cached shell, perceived offline readiness may degrade. Conversely, a network-first navigation can benefit from preload under supported conditions.
6. **Update lifecycle:** Preload state belongs to the registration and may survive Worker script updates; it is not automatically equivalent to the V2 script's intended fetch policy. Test V1 active/V2 waiting/activation and rollback with explicit preload-enabled state and per-client controller.
7. **Owner and data authority:** A faster HTML navigation does not establish Firebase UID continuity, local Sembast owner fence, deletion completion, independent Files backup or accepted sync. Cached shell, preloaded HTML and authenticated data each require distinct admission evidence.
8. **Performance and privacy:** Measure cold Worker startup, navigation timing, transfer bytes and duplicate requests together. Faster first paint is not an acceptable optimization if it causes redundant network traffic, leaks token-bearing URLs into logs or makes offline recovery less reliable.

### 13.3 Falsifiable NP01–NP12 test packet (DEFINED, NOT RUN)

| ID | Controlled stimulus | Evidence / acceptance oracle |
| --- | --- | --- |
| NP01 | Source-pinned served build, first visit versus controlled revisit | Exact Worker script hash, registration scope/controller and \`navigationPreload.getState()\`; do not infer enabled from API support |
| NP02 | Warm Worker versus cold Worker startup on online network-first navigation | Navigation timing and number of requests; compare preload on/off without claiming universal speedup |
| NP03 | Cache-first shell navigation while preload enabled | Whether an avoidable network request occurs; no duplicate \`fetch\` and no misleading cache hit metric |
| NP04 | Eligible GET navigation versus Firebase cross-origin POST | Preload only applies to eligible navigation; no assumption that \`createAuthUri\` POST is preloaded |
| NP05 | Synthetic auth-action navigation with fake nonfunctional token and redirects | Trace whether network request begins before Worker route decision; no real token, false success or stored private response |
| NP06 | 302, 401, 404 and 500 controlled navigation responses | Record network/preload status, redirect chain, Worker-selected response and user-visible error independently |
| NP07 | Response varies by \`Service-Worker-Navigation-Preload\` | Correct server \`Vary\` and no mixed response reuse across header variants |
| NP08 | Offline cold launch with valid cached shell and preload previously enabled | Useful offline shell without indefinite network wait; Auth/Sync still correctly reported unavailable |
| NP09 | V1 Worker active, V2 waiting then activated | Explicit preload state and V1/V2 fetch-policy coherence; no partial shell promotion |
| NP10 | Account A deleted while old A tab remains; B starts normally | No stale Worker/preload response authorizes A write or binds B to A's local ledger |
| NP11 | Approved Safari tab, Home Screen PWA and managed Web Clip on physical iPad | Actual OS/version/policy and preload/network behavior captured separately; no Chromium transfer |
| NP12 | Performance/accessibility and consent-safe analytics under online/offline transitions | Latency, bytes, focus/error announcements and privacy-safe event taxonomy; no claim of successful sync from fast navigation |

**VALIDATION protocol:** Before considering preload, identify the actual generated Worker and whether its fetch strategy is cache-first or network-first for each navigation class. Use synthetic URLs and accounts only. Record exact source/bundle hashes, served HTTPS headers, OS/browser, registration state, DevTools/remote-inspector network trace, \`preloadResponse\` consumption, CacheStorage inventory and expected/observed results. Run deliberate negative controls (offline, redirect, error, old-owner tab). Classify each as PASS/FAIL/INCONCLUSIVE/NON-EXECUTION. An MDN example, source-level inference or a generic synthetic Chromium fixture cannot promote LogMate's physical-EFB release gate.

**TRANSFER / DECISION:** Track A owns preload mechanics and version support; E owns private-route and owner-safe admission; C owns controlled timing, duplicate-request and interruption tests; B owns honest offline/error/update UX; D owns consent-safe acquisition/performance attribution, not inflated app-ready or sync-success events. Engineering owns exact LogMate build/runtime verification and any implementation. Design Studio W121's physical/assistive-technology evidence remains OPEN; Marketing D9's PWA claims remain HOLD. **MINTTAP DECISION:** No automatic recommendation to enable navigation preload; use it only after route-by-route benefit, privacy and offline regression evidence. **CHANGE WATCH:** Browser support, Flutter build output, registration state and MDM rules at the tested release. **Next major evidence target:** actual served Worker script and controlled request trace; if inaccessible, preserve this packet as an Engineering handoff and pivot to a distinct independently testable Stage 8 question.

**Gate unchanged:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## 14. Deployment-base path, manifest navigation scope, worker control scope and auth rewrite — independent boundary reconciliation (2026-11-07)

**Ownership / priority:** A owns browser URL and scope mechanics; E owns deployment/auth trust and incident controls; C owns route/asset test evidence; B owns installation and recovery affordances; D owns canonical URLs, acquisition and truthful installed-PWA claims. **Stage 8 applied; P1**, below deletion/owner custody P0. This section integrates existing install-identity research [530](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md), fetch classification §12 and preload §13; it does **not** repeat their general primers.

### 14.1 Why this matters: four independent route boundaries

A deployment can show a valid standalone icon yet fail its offline startup or redirect, because four different mechanisms resolve paths: (1) HTML `<base>` and browser URL resolution; (2) manifest `start_url`, `scope` and install identity; (3) service-worker script URL, registration scope and **per-client controller**; (4) Hosting rewrites and the response actually served at each URL. A fifth boundary is the Firebase Auth authorized action/continue URL, which must be validated independently. **A URL matching the manifest navigation scope does not prove the URL is controlled by a worker.** Conversely a controlled auth route is not necessarily appropriate for offline app-shell fallback.

**PRIMARY / SOURCE (checked 2026-11-07):**
- [MDN ServiceWorkerContainer.register](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register): default registration scope is the script directory; explicit scope must be within the allowed maximum, with `Service-Worker-Allowed` required for broadening; `updateViaCache` applies to worker scripts/imports, not application resources. Most-specific matching registration controls a document if multiple registrations overlap.
- [MDN Service-Worker-Allowed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Service-Worker-Allowed): widening a script's default directory scope is a **response-header** authorization, not a manifest property.
- [MDN manifest start_url](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/start_url) and [W3C manifest navigation scope](https://www.w3.org/TR/2023/WD-appmanifest-20231028/#navigation-scope): relative `start_url` is resolved against the manifest URL; missing manifest `scope` is inferred from the effective start URL's parent path. **Correction to potentially misleading older tutorials:** do not universally assert that omitted manifest scope is based on the manifest-file directory; that may coincide for root layouts but is not the general processing rule.
- [Google web.dev manifest guidance](https://web.dev/learn/pwa/web-app-manifest) describes install identity/presentation; browser/OS install prompts and installed-container behavior remain implementation-dependent, not interchangeable with the worker scope.

**PINNED PRODUCT SOURCE (read-only, 2026-11-07):**
- LogMate `web/flutter_bootstrap.js` blob `a70625e8bda32aafd5dd23822c017d05229f0e63` defines `logmateBaseUrl = new URL('./', document.baseURI)`, then `new URL('logmate_service_worker.js', logmateBaseUrl)`, registering with `scope: logmateBaseUrl.pathname` and `updateViaCache:'none'`. It starts registration asynchronously without blocking Flutter startup, calls `registration.update()`, posts `START_PRECACHE` and `PROMOTE_VERIFIED_CANDIDATE`, and listens for one `controllerchange`. Comments explicitly say the generated Flutter worker is disabled at build time. This proves **registration intent**, not deployed worker bytes, cache correctness or successful registration.
- `web/index.html` blob `01be77585ac40bf11e80777177a4ab08e4885671` contains `<base href="$FLUTTER_BASE_HREF">` substituted at build and a relative `manifest.json` link. Exact compiled `<base>` remains UNKNOWN without built artifact.
- `web/manifest.json` blob `8225e76fe032e792c30b0f22efa1f7cafab68119` has `"start_url":"."`, `"display":"standalone"`, but no explicit `id` or `scope`. **No claim that this prevents installability**; it creates identity/migration and URL-resolution dependencies to test.
- `firebase.json` blob `9ac0972e26749215c4a718360c66315c6caf3cc8` serves `build/web`, declares wildcard HTTP `no-cache, no-store, must-revalidate`, and rewrites exact `/auth`, `/auth/`, `/auth/action` to `/auth/action/index.html`. It does not, by itself, prove production routing, redirect query preservation, MIME, security headers, or whether an active worker overrides those routes.

### 14.2 Conditional deployment matrix — **MODELS, NOT OBSERVED PROD**

| Deployment / navigation | HTML base + relative worker | Manifest identity / scope | Auth/Worker interaction | Boundary to verify |
| --- | --- | --- | --- | --- |
| Origin root `/` with compiled base `/` | Worker script resolves `/logmate_service_worker.js`, requested scope `/` | Root manifest and `start_url: "."` normally resolve root; missing explicit ID makes migration analysis important | Root-controlled page may route `/auth/action` navigation through worker fetch handler; Hosting rewrite only applies if network reached | Worker exists/JS MIME, registration/controller, auth route bypass/response classification |
| App under `/logmate/` with compiled base `/logmate/` | Script `/logmate/logmate_service_worker.js`, scope `/logmate/` | Manifest expected at `/logmate/manifest.json`; `start_url: "."` resolves `/logmate/` | Hosting exact `/auth/action` is **outside** app worker scope, but same-origin auth callback can navigate to a different container/page | Build base, served subpath assets, Firebase authorized action URL and standalone return |
| Mismatched base/hosting prefix | Worker registration may resolve to nonexistent file or wrong path/scope | Manifest may resolve to different start URL or icon path | Install icon can be present while offline shell/controller is absent | Negative tests for 404, HTML-as-JS MIME, stale prior worker, unexpected origin/path |
| Two installations/registrations on same origin | Overlapping registrations can select most-specific scope; page controller may differ from intended script | Manifest identity and app window routing are independent of registrations | Auth/support route might be controlled by another registration | enumerate registrations, `controller.scriptURL`, `registration.scope`, installed URL and exact route |

**Key synthesis:** Because the current script is located in the same computed base directory as its requested scope, **no broadened `Service-Worker-Allowed` header is intrinsically required in that matched-path model**. Do not recommend adding a broadening header reflexively. If a future deployment moves the script to a nested assets directory while retaining root scope, then the allowed-scope header becomes a real dependency. Separately, an HTTP wildcard `no-store` header does not itself stop an active Worker from returning CacheStorage responses.

### 14.3 Operational failure, privacy and user experience consequences

1. **Cold versus controlled:** first navigation before controller assignment may follow Hosting rewrite, while later navigation may be intercepted by a root Worker. Test both; a single online page load cannot prove auth callback parity.
2. **Auth action isolation:** a real one-time action code must not be treated as an offline shell navigation or cached fallback. Use fake nonfunctional query values in synthetic tests; preserve the full response status and no-cache/no-store semantics without claiming the Hosting config protects Worker caches.
3. **Scope migration:** changing `base-href`, manifest `id` or `start_url`, worker script location, or origin can alter installed app identity, scope and data-container assumptions. Never equate a successful fresh install with in-place upgrade preserving old IndexedDB and Files custody.
4. **MDM Web Clip:** a managed launch URL, Home Screen web app, and Safari tab are separate test rows. Manifest presence does not authorize a claim that company policy permits installation, standalone mode, persistence, background sync or Files export.
5. **Route transparency:** if a network 404/401/500 is transformed into a 200 app shell, accessibility, support and incident telemetry must not claim successful authentication. Preserve request class, final status, source (network/worker/cache) and recovery state without logging auth codes or email.
6. **Discovery and claims:** canonical marketing/support URLs must be reachable without installing the PWA and must not depend on a cached authenticated app shell. Search indexing is a separate decision from SW scope; do not imply manifest installation proves indexing.
7. **Release/rollback:** record both served build hash and active controller script hash. A prior installed Worker may survive a Hosting rollback and keep serving a different shell; test existing installations and fresh profiles independently.

### 14.4 Acceptance packet BP01–BP14 — **DEFINED, NOT RUN**

| ID | Stimulus | Evidence / falsifiable oracle |
| --- | --- | --- |
| BP01 | Exact release build at `/` | Record compiled `<base>`, manifest URL, resolved `start_url`, ID/scope and worker script URL; HTTP status/MIME/hash |
| BP02 | Exact release build at approved subpath | All URL resolutions, registration scope, launch URL and asset paths match intended prefix; no silent root fallthrough |
| BP03 | Missing Worker file or HTML fallback masquerading as script | Registration fails visibly and offline readiness is not falsely reported |
| BP04 | Fresh profile vs existing controlled tab | Capture `navigator.serviceWorker.controller` and registration list, network/worker route decisions separately |
| BP05 | Root Worker and synthetic `/auth/action?mode=...&oobCode=FAKE` | No private token cache; true response class and status; no false 200 shell or unsafe redirect |
| BP06 | Exact Hosting `/auth`, `/auth/`, `/auth/action` and `/auth/action/` | Verify each route independently; do not assume trailing-slash variant covered by declared rewrite |
| BP07 | Manifest `id` absent, start URL change in controlled test | Compare installed identity and update path per browser; no inferred automatic migration |
| BP08 | Move worker script under nested directory with root scope | Confirm failure absent appropriate `Service-Worker-Allowed`, and behavior when explicitly authorized |
| BP09 | Two overlapping registrations / old worker | Most-specific scope/controller selection, old cache isolation, safe unregister/rollback |
| BP10 | Offline app shell vs offline auth/support route | App data remains honest; auth action never misrepresented as completed; public support reachable online without install |
| BP11 | Physical Safari tab/Home Screen/managed Web Clip | OS/MDM policy, launch/container, storage, scope, offline and Files custody separately observed |
| BP12 | Account A deletion, old tab, then B startup | No old-owner write or B→A binding even with stale controller or shell; Engineering P0 remains independent |
| BP13 | Error/redirect, keyboard/AT, 200-shell fallback | Status and error message/focus are truthful; accessible recovery, no success telemetry on error |
| BP14 | Domain/path migration + rollback | Independent backup/restore, origin data continuity or explicit loss warning, per-client Worker/manifest identity and verified recovery |

**VALIDATION:** Record exact repository SHA and compiled artifact hashes, deployed URL/response headers, browser/OS version, registration and controller, manifest-derived IDs, network trace, cache inventory, expected vs observed status, and privacy-safe synthetic query values. Mark PASS/FAIL/INCONCLUSIVE/NON-EXECUTION. Only actual served/installed product evidence can close the corresponding release gate; source and standards are not product PASS.

**DEPENDENCY / TRANSFER:** Engineering owns exact LogMate build, Firebase Hosting deploy and authentication integration; A supplies URL/scope mechanics; E owns route trust and rollback; C/Design Studio W121 supplies runtime, accessibility and cross-browser evidence; B owns honest install/offline/auth recovery; D/Marketing D9 owns website/Store claim integrity. **MINTTAP DECISION:** do not recommend moving Worker, widening scope or changing manifest IDs before capturing current installed identity and migration impact. **OPEN:** generated worker and served auth response, current production base-href, managed iPad, independent Files and owner-deletion. **CHANGE WATCH:** browser manifest identity behavior, Apple WebKit installed container and company MDM policy. **Gate unchanged:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## 15. Cross-context coordination, IndexedDB durability, and owner fencing — 2026-11-08

**RESEARCH CLASSIFICATION:** SOURCE / SYNTHESIS / DEPENDENCY / TRANSFER VALIDATION / OPEN / CHANGE WATCH. **Owner:** E security/operations; A browser concurrency mechanics; C fault validation; B honest conflict/recovery UX; D privacy-safe observability. This adds a missing *coordination-versus-authorization* boundary to [§9 lifecycle LC01–LC12](#9-bfcache-and-page-lifecycle-owner-boundary) and [§14 deployment BP01–BP14](#14-pwa-base-path-manifest-identity-and-worker-scope-2026-11-07). It does not supersede [529 P0 old-writer](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) or Engineering S007.

### 15.1 History/problem → distinct primitives

Two tabs may edit the same local logbook, a Service Worker may update concurrently, and a restored tab may hold stale Auth/owner state. The old failure pattern is treating one browser signal as a universal mutex or authorization decision. Separate five mechanisms:

| Mechanism | Actual guarantee / role | Non-guarantee / failure mode |
| --- | --- | --- |
| **Web Locks** | [MDN Web Locks API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API) describes cooperative, named exclusive/shared locks among eligible same-origin browsing/worker contexts in a secure context; useful to serialize a sync leader or migration coordinator | Not a server lease, user identity, permanent lock, or guarantee that *all* app code participates. A crashed/frozen context and separate storage partition/device must not be assumed to share coordination. Never hold a lock across arbitrary user interaction or await unbounded network operations. |
| **BroadcastChannel** | [MDN Broadcast Channel API](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) conveys messages among contexts sharing an origin **and storage partition**, including workers where available | Best-effort event notification, not durable queue, persisted revocation, security fence, device-to-device transport, or proof that a hidden/frozen tab received a message. Storage partition can isolate otherwise same-origin frames; installed Home Screen/Safari containers need direct testing. |
| **IndexedDB transaction** | [MDN IDB transactions](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) provides transaction-scoped read/write atomicity for included stores, subject to app adapter/schema behavior | Does not make a preceding in-memory owner check atomic with a later write. Read the durable owner/deletion epoch and write dependent data within an appropriate atomic transaction, or prove an equivalent adapter-enforced fence. |
| **IDB durability hint** | [MDN IDBTransaction.durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability) and [IDBDatabase.transaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction) distinguish strict, relaxed, default hints | A hint is not an independent export, power-loss guarantee, quota immunity, backup, or a promise that Sembast/Flutter actually requests strict durability. Physical abrupt-loss/restore evidence remains required. |
| **Server/remote admission** | Authoritative authenticated UID, deletion phase/epoch, replay/idempotency and version checks at remote write/sync boundary | A local Web Lock, BroadcastChannel event, Service Worker message, or installed app identity cannot authorize a remote mutation. |

**SOURCE / platform reality:** MDN labels Web Locks broadly available since March 2022 and secure-context-only; BroadcastChannel broadly available but partition-bound. Exact iPadOS, managed Web Clip, private browsing and installed-container behavior is **CHANGE WATCH / U**, not inferred from baseline badges. IndexedDB durability was Baseline 2024, but older managed OS versions may differ. The browser is not obligated to keep background tabs or workers running for an entire sync.

### 15.2 Operational model: coordination must never replace a durable owner fence

**SYNTHESIS:** Use an epoch-bearing durable ownership state, e.g. {ownerUid, generation, deletionPhase, schemaVersion}, and validate it at the *actual mutation boundary*; this is a **test contract**, not a proposed LogMate schema change. An old tab A may have read generation 7 before deletion; tab B may commit deletion intent generation 8; tab A's later write must be rejected even if A never receives a BroadcastChannel notification. A lock may reduce collisions but must not be the sole reason a write is admitted. The same applies to an old Service Worker, a restored bfcache page, and a reopened offline client.

A practical **falsifiable** acceptance rule is: for every durable write path (draft, import, Sync/Replica, settings, backup metadata, restore, account switch), capture the owner/epoch/phase read and the write commit point; demonstrate that deletion-intent and owner changes cannot interleave so as to admit stale A writes. For writes spanning stores or remote operations, define which boundary is atomic, which is compensating/idempotent, and how recovery detects partial completion. Do not assert that generic IndexedDB transactions automatically cover a Dart Sembast adapter's entire multi-store mutation; inspect the exact adapter.

**Security vs UX:** A visible “Account deleted” message is not proof that other contexts have stopped writing. Broadcast a non-sensitive invalidation notice as a UX accelerator, but on resume/reload, re-read durable state. Do not put emails, tokens, auth action codes or full logbook records in channel names/messages, lock names or analytics. Offline old-owner data may remain viewable only under an explicit product policy; authorization to write/merge is separate.

**Storage/partition transfer:** A Safari tab, installed Home Screen web app, and MDM Web Clip may not share the same data container, so same-origin channel/lock tests within one container do not establish cross-container revocation. A native mobile app is an entirely different OS/application storage and process domain. Coordination across devices requires an independently validated authenticated transport and remote admission contract; local browser APIs are not direct PWA↔native synchronization.

### 15.3 Failure matrix CC01–CC16 — **DEFINED, NOT RUN**

| ID | Stimulus / boundary | Falsifiable oracle |
| --- | --- | --- |
| CC01 | Two same-origin tabs request exclusive Web Lock for sync | Only one cooperating holder runs critical section; queued contender eventually resumes |
| CC02 | Tab holding lock freezes, closes, crashes or is discarded | No permanent corruption/deadlock; retry and lease/epoch handling explicitly observed |
| CC03 | A holds sync lock; B commits deletion intent | A's subsequent local/remote write denied by durable owner/phase, irrespective of lock |
| CC04 | BroadcastChannel deletion notice delivered to active tab | UI invalidates safely; no PII in message; no mutation until durable recheck |
| CC05 | BroadcastChannel message missed during bfcache/frozen tab | On pageshow/resume, stale tab rechecks durable state; cannot write old owner |
| CC06 | Installed Home Screen app vs Safari tab vs managed Web Clip | Identify separate storage partitions/contexts empirically; no assumed shared channel or lock |
| CC07 | Two browser tabs vs native mobile | No claim of cross-device Web Lock/BroadcastChannel; remote sync authority tested independently |
| CC08 | Owner generation changes between read and write | Atomic fence or equivalent adapter contract rejects stale write |
| CC09 | Sembast/IndexedDB transaction abort, quota exception, schema migration | No partial owner-data admission; precise commit/rollback evidence |
| CC10 | Two deletion drivers / duplicate requests | Exactly-once *effects* via idempotent state, even with at-least-once retries; no premature completed claim |
| CC11 | Service Worker V1 and V2, old page still controlled | No stale worker message can override owner phase or schema; worker/cache not ledger authority |
| CC12 | Abrupt process/power termination around transaction completion | Measure committed state on cold restart; durability hint not substituted for physical backup |
| CC13 | Storage pressure / browser eviction | Recover only from independently saved and re-read Files artifact; no data-survival claim |
| CC14 | Lock API unavailable / unsupported secure context / partition | Safe fallback or explicit disabled concurrent operation; no unsafe unlocked mutation |
| CC15 | Background sync interrupted offline / remote conflict | Pending state preserved or safely failed; remote UID/epoch/idempotency prevents replay after deletion |
| CC16 | Account A deletion then B normal startup with two stale contexts | Zero A writes/Sync/Replica resurrection; B remains isolated; redacted event evidence |

**VALIDATION packet:** record exact LogMate SHA and store inventory, adapter transaction code, test context origin/storage partition, browser/iPadOS version, worker/controller hash, owner-generation transitions, ordered timestamps for read/intent/commit, transaction outcome, remote receipt, restart observation and Files readback. Classify PASS/FAIL/INCONCLUSIVE/NON-EXECUTION. Test fixtures must be disposable and non-personal; source reasoning cannot close P0.

### 15.4 Cross-track and product handoff

- **A platform:** verify Web Locks/BroadcastChannel feature detection, partition boundaries, lifecycle interruption, worker compatibility, and standards-versus-WebKit/Chromium differences. No browser feature support implies an MDM policy exception.
- **E security:** define owner fence, deletion phase, idempotency, transaction and remote admission evidence. Locks/channels are optional coordination, not authority.
- **C quality:** execute CC01–CC16 with fault injection, interrupted transactions, accessible recovery, exact build hashes and independent physical-iPad runs; connect Design Studio W121 runtime gate.
- **B UX:** distinguish “sync pending”, “locally saved”, “independently backed up”, “deleted”, and “remote confirmed” in user-facing state; avoid success copy on only a channel event or optimistic UI.
- **D discovery/analytics:** collect aggregate privacy-safe event classes (lock contention, stale epoch denied, failed restore, actual completion) without identity/email, and prevent marketing claims from exceeding observed evidence.

**DEPENDENCY / TRANSFER VALIDATION:** Engineering S007 owns deletion saga, exact LogMate store/adapter transactions and native↔PWA sync. Marketing D9 keeps offline/PWA claims on HOLD. Design Studio W121 requires runtime accessibility. **MINTTAP DECISION:** no new LogMate code change, no blanket recommendation to adopt Web Locks, no assumption of direct device-to-device background sync. **OPEN:** exact transaction/fence implementation, current physical device capability, multi-context runtime evidence, independent Files restore, old-writer P0. **CHANGE WATCH:** WebKit storage partition/installed PWA behavior, IndexedDB durability implementation, OS-managed lifecycle. **Gate:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


---

## 16. User-visible Files backup custody: picker, download, external artifact and recoverable ledger (2026-11-08)

### 16.1 History, source, and platform contract

**HISTORY / FAILURE MODEL:** Offline PWA storage is origin/container-managed. An independent file is a separate failure domain only after bytes leave the browser container and can be read in a new context. File picker availability, download initiation, an in-memory Blob, an origin-private file, an OS Files document and successful re-import are distinct states. This is particularly consequential for company-managed iPads.

**SOURCE / PLATFORM checked 2026-11-08:**
- [MDN showSaveFilePicker](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker) and [showOpenFilePicker](https://developer.mozilla.org/en-US/docs/Web/API/Window/showOpenFilePicker): limited browser availability, secure context, transient user activation, cancellation and permission errors.
- [Web Platform DX file system access](https://web-platform-dx.github.io/web-features-explorer/features/file-system-access/): Chromium supports powerful user-visible picker entry points; Safari/iOS Safari do not. This does NOT establish that ordinary HTML file input, browser download, or Files share UI is impossible in Safari.
- [MDN File System API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API): origin-private file system (OPFS) and user-visible file handles are different custody models. OPFS is not an independently saved Files document.
- [MDN blob URL](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/blob): a Blob URL can initiate download, but creation or navigation does not prove that a file was durably saved or independently restorable.
- [MDN FileSystemFileHandle](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle): file permission lifecycle can change; a retained handle is not an unconditional unattended write authorization.
- [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) and [tracking prevention](https://webkit.org/tracking-prevention/): browser persistence/ITP exceptions do not guarantee an external Files readback.

**PRODUCT BOUNDARY:** Existing [298](../298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md), [529](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md), [530](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md) and EV21 already require independent backup. This study does NOT claim LogMate currently uses powerful file pickers, that its Flutter Web adapter has been executed, or that MDM allows Files transfer. These remain OPEN.

### 16.2 Security and durability state machine

1. **Snapshot requested:** accept explicit user action; check owner, epoch and deletion phase at capture.
2. **Snapshot materialized:** deterministic versioned serialization, record count, size and integrity metadata; in-memory/OPFS state is not independent custody.
3. **External save initiated:** feature-detected picker, HTML download or platform share flow; handle cancellation, denied access, quota and memory errors.
4. **External save observed:** record destination evidence where platform permits; browser JavaScript often cannot attest final Files persistence from download dispatch alone.
5. **Fresh-context readback:** independently select saved artifact in a new context; check actual bytes, hash, schema, owner and counts.
6. **Restore validated:** disposable clean container, preview, duplicate/owner gate, record parity, restart and separate Sync/Replica admission.
7. **Custody survival:** only authorized non-production tests may examine browser eviction, Home Screen removal, MDM profile removal and device replacement.

**SYNTHESIS:** A download click may succeed while the user cancels saving, MDM blocks Files access, a provider writes elsewhere, or the file is corrupt. OPFS persistence remains browser-managed. A checksum detects some corruption, not authenticity or account ownership. A restore file can be syntactically valid yet wrong-owner, outdated, oversized or malicious. Actual adapter transaction and schema checks belong to Engineering.

**CONTRADICTION:** PWA can create a Blob does not entail independent iPad Files backup. Browser storage persisted does not entail survival of MDM uninstall. Download started does not entail recoverable ledger. Powerful picker unsupported in Safari does not entail every Safari export/import mechanism is impossible.

### 16.3 BF01–BF18 falsifiable acceptance — DEFINED, NOT RUN

| ID | Scenario | Required oracle |
| --- | --- | --- |
| BF01 | Chromium HTTPS save picker with user activation | Feature and written bytes verified |
| BF02 | Safari/iPadOS lacks powerful picker | Tested fallback or explicit unavailable state |
| BF03 | Picker canceled or permission denied | No backup-complete claim or ledger mutation |
| BF04 | Async delay loses transient activation | Safe retry, no unattended access claim |
| BF05 | Blob URL/download | Distinguish dispatch from saved file and fresh readback |
| BF06 | Large export / low memory / quota | No partial success or deadlock |
| BF07 | Offline export | Complete local snapshot only when owner data available |
| BF08 | Offline import via ordinary file input | Actual selected bytes parsed |
| BF09 | Safari tab vs Home Screen app | Separate Files chooser/download behaviors observed |
| BF10 | Managed Web Clip and MDM | Authorized physical device observation |
| BF11 | Files provider read-only/unavailable/full | Recoverable error, no success claim |
| BF12 | New container selects saved artifact | Byte/hash/schema/count parity |
| BF13 | Corrupt/truncated/oversized/old-version artifact | Rejection before ledger mutation |
| BF14 | Wrong-owner/stale-epoch restore | No unauthorized rebind or resurrection |
| BF15 | Duplicate import/partial failure | Transaction and undo behavior verified |
| BF16 | Browser eviction/Home Screen removal | Recovery only from independently saved file |
| BF17 | MDM removal/device transfer | Operator-authorized, no destructive live-user action |
| BF18 | Restored ledger then Sync/Replica | Separate remote owner/idempotency admission |

**VALIDATION:** capture source/build SHA, OS/browser/MDM version, installation mode and origin, format/schema, artifact byte count/hash, gesture and save route, actual destination, new-context readback, import result, owner/epoch, count parity, cold restart and remote receipt. Classify PASS/FAIL/INCONCLUSIVE/NON-EXECUTION. Desktop Chromium evidence cannot promote managed-iPad PASS.

### 16.4 Cross-track integration and operational judgment

**A platform** owns picker and download feature detection, user activation and browser differences. **E security** owns custody, owner-fenced export, integrity, restore admission and release gate. **C quality** owns large-file, low-quota, interruption, accessibility and physical-device tests. **B UX** distinguishes preparing, save initiated, file verified and restore verified; never labels click as backup complete. **D discovery/analytics** separates initiated from verified backup in privacy-safe aggregates and prevents unsupported offline claims.

**DEPENDENCY / TRANSFER VALIDATION:** Engineering owns LogMate Flutter Web file adapter, owner transactions and schema; Design Studio W121 owns accessibility execution; Marketing D9 keeps PWA/offline claims on HOLD. **MINTTAP DECISION:** prioritize independently saved and re-read Files artifacts over browser-only persistence as a product acceptance criterion, without authorizing implementation changes. **OPEN:** deployed adapter, MDM policy, installed iPad behavior, file readback, owner-bound restore. **CHANGE WATCH:** Safari/iPadOS file UX, Chromium picker support and managed Web Clip policy. **Gate unchanged:** Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD.


---

## 17. Offline EFB PWA ↔ native mobile: transport discovery, signaling and custody admission (2026-11-08)

**Ownership:** E security/operations owns authorization and durable transfer acceptance; A browser/platform owns transport capability; C executable reliability; B pairing and failure UX; D truthful claims. This section is a connected *architecture decision and falsification packet*, not a new transport implementation, device test, or permission to use a company network.

### 17.1 HISTORY / PROBLEM → PRINCIPLE

An offline PWA is a locally executing web origin, **not** a native iPad process with general access to Bluetooth, Bonjour/Multipeer Connectivity, local sockets or persistent background execution. A native mobile application may have OS capabilities that the installed PWA cannot call. “Both devices have radios” does not imply they share a permitted application transport. Even if a channel transfers bytes, that does not prove the receiver is the intended ledger owner, that the sender's state is current, or that the import survived restart.

Separate six gates: **(1) distribution/install permission, (2) device discovery, (3) signaling/session establishment, (4) permitted reachable transport, (5) authenticated owner/epoch and idempotent transaction admission, (6) durable post-restart receipt and recoverability.** An online bootstrap or one-time pairing does not automatically solve subsequent offline reachability. A company EFB policy may prohibit personal hotspots, ad-hoc Wi-Fi, Bluetooth discovery, local-network browsing or installation; these remain independent operator facts.

### 17.2 SOURCE — standards versus actual browser/OS behavior

- **WebRTC data channel (cross-browser web mechanism):** MDN [RTCDataChannel](https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel) and [Using data channels](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Using_data_channels) describe arbitrary bidirectional data transfer on an RTCPeerConnection, DTLS encryption, message-size and buffered-send considerations. A *signaling path* must exchange offers/answers and ICE information; see [WebRTC connectivity](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity). Signaling need not be a hosted server in principle: an authorized out-of-band channel could carry negotiation material. **But** out-of-band signaling, ICE candidate reachability, WebKit behavior, NAT/firewall, local-network policy, page suspension and native interoperability must each pass on actual devices. Do not infer unattended/offline automatic discovery or sync from API existence.
- **Web Bluetooth:** MDN [Web Bluetooth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API) labels it *Limited availability*, requires secure context and explicit user activation/permission, and does not expose it to Web Workers. This is BLE GATT peripheral access, not an arbitrary iOS native-peer sync protocol; iPadOS Safari/Home Screen support cannot be assumed. Do not propose Web Bluetooth as the default LogMate EFB channel.
- **Apple OS permission boundary:** Apple [Local Network Privacy](https://support.apple.com/en-us/102229) documents iOS/iPadOS app permission for local-network interactions, but this does **not** establish a universal Safari PWA permission API, guarantee EFB MDM allowlisting or authorize hotspot use. An OS-level prompt and an MDM network rule are separate admission conditions.
- **Service Worker / background:** Service Worker fetch and lifecycle features do not grant a continuously running local discovery agent or indefinite WebRTC session. Any background wakeup, push, sync or notification capability is platform- and permission-specific. A foreground-only, explicitly initiated transfer is the conservative baseline for feasibility testing, not an approved product UX.
- **Cryptography and custody:** WebRTC DTLS encrypts the channel, but transport encryption alone is not *product* pairing authorization, verified Firebase UID, owner/epoch admission, conflict resolution or remote receipt. Never equate successful connection with permission to import or overwrite a flight record. Source of product owner rules remains Engineering/LogMate, not Web Manager.

**CHANGE WATCH:** WebKit/iPadOS WebRTC constraints, Web Bluetooth availability, local-network prompts, MDM profiles, private relay/VPN, network isolation, worker/background lifecycle, native OS entitlement and browser permission changes. Record exact OS build, Safari engine, PWA installation mode and policy, not merely “iPad supported.”

### 17.3 Architecture alternatives and decision thresholds

| Option | Possible role | Independent prerequisites | Failure/false-positive to reject |
| --- | --- | --- | --- |
| Authorized internet relay / backend | Store-and-forward after connectivity | User-approved server/data policy, auth, remote owner fence, EFB network access | Online login is not cockpit offline sync; server access may be unavailable |
| WebRTC data channel to native mobile | Experimental foreground peer transfer | Authorized signaling (online or out-of-band), native WebRTC stack, ICE reachability, network/MDM permission, pairing | DTLS or connected event does not prove ledger owner, unattended wakeup or durable commit |
| Native mobile HTTPS local endpoint, PWA fetch | Experimental LAN transfer | Same reachable network, browser mixed-content/private-network policy, TLS/trust, local-network permissions, native listener, MDM approval | A localhost/native listener is not automatically accessible from another device or secure-origin PWA |
| Web Bluetooth / BLE | Capability investigation only | Actual Safari support, GATT design, OS/device permissions, MDM, throughput | BLE presence is not generic peer discovery or an iPad PWA entitlement |
| Files export/import | Explicit user-mediated custody and recovery | Actual iPad Files save/readback, format integrity, owner admission, physical-device permissions | A Blob download/selection is not an unattended device-to-device sync |
| QR/visual out-of-band | Potential *pairing metadata* exchange | Camera/UI/MDM permission, human action, nonce expiry | QR is not suitable proof of bulk reliable flight-record transfer or automatic sync |

**SYNTHESIS:** No currently cited source proves an unattended, automatic, offline, native↔managed-iPad PWA sync route. The architecture should preserve **manual, verifiable backup/restore as an independent recovery plane** and keep peer transfer an experiment until device/MDM and owner-admission evidence exists. A one-time pairing token must be scoped, revocable, bound to owner/device/session and never treated as a perpetual authorization for deleted/replaced owners.

### 17.4 Failure model and operational decision

Sequence a candidate transfer as **capability detection → operator-permitted discovery/signaling → explicit user-approved pairing → authenticated device/session binding → immutable source snapshot with schema/version/owner epoch → chunked transfer with bounds/backpressure/checksum → receiver staging and validation → owner/epoch/idempotency check at write transaction → durable commit → cold-restart receipt and reconciliation**. Transfer interruption, repeated chunk, replayed receipt, concurrent edits, schema mismatch, owner deletion and restored older backup must not bypass owner fence. A hash can detect accidental byte differences but cannot authenticate the sender; channel encryption is not proof of ledger ownership. Pairing UI should distinguish *connected*, *transfer received*, *import validated* and *sync committed*. Privacy-safe analytics should not log flight data, identifiers or pairing secrets.

**MINTTAP DECISION (research recommendation, NOT owner approval):** Do not market automatic offline PWA↔native sync, direct Bluetooth sync, background sync, hotspot-free peer sync or MDM compatibility as delivered. Engineering should first choose a minimal **authorized foreground** candidate and test the physical managed iPad. If policy forbids all usable local channels, this is a real product architecture blocker requiring owner decision, not a web-standard workaround.

### 17.5 SY01–SY20 falsifiable acceptance matrix — DEFINED, NOT RUN

| ID | Test / observable oracle |
| --- | --- |
| SY01 | Record physical iPad model, iPadOS build, Safari/Home Screen/Web Clip mode, MDM restrictions and network operator authorization |
| SY02 | Compare actual foreground API presence/permissions across Safari tab, installed PWA, managed Web Clip and native mobile |
| SY03 | Test WebRTC offer/answer and ICE exchange over explicitly authorized signaling; no inference from constructor existence |
| SY04 | With all internet paths disabled, test whether approved local signaling/ICE/transport can establish a channel |
| SY05 | With hotspot disabled by policy, test only explicitly permitted LAN alternatives; do not bypass policy |
| SY06 | Test corporate Wi-Fi client isolation, VPN, proxy, firewall and captive-network conditions separately |
| SY07 | Distinguish local-network permission prompt, denial, MDM block and transport timeout in logs/UI |
| SY08 | Confirm WebRTC DTLS connected does not permit unpaired/incorrect-owner ledger write |
| SY09 | Native-to-PWA and PWA-to-native payload transfer, schema/version negotiation and maximum message/chunk size |
| SY10 | Backpressure and memory bound under large flight-log payload; no unbounded bufferedAmount |
| SY11 | Kill/foreground/background PWA during transfer; no assumed unattended resume |
| SY12 | Airplane mode, screen lock, tab eviction and Worker V1→V2 transition; explicit resumability or safe abort |
| SY13 | Wrong UID, revoked pairing, owner deletion, stale epoch and restored old ledger reject admission |
| SY14 | Concurrent device edits and duplicate transfer yield deterministic conflict/idempotency outcome |
| SY15 | Interrupted/duplicated/out-of-order/corrupt chunks rejected or resumed without partial ledger mutation |
| SY16 | Receiver's post-commit cold restart shows same record counts, owner binding and transaction receipt |
| SY17 | Actual Files export→fresh-context readback→restore independently succeeds when peer path fails |
| SY18 | No secrets, raw flight details, emails or tokens in URLs, signaling logs, analytics or QR payload |
| SY19 | Accessible pairing, permission-denied, offline, retry, cancellation and failure messaging with screen reader |
| SY20 | Compare permitted network/device modes and document PASS/FAIL/INCONCLUSIVE/NON-EXECUTION per exact build |

**DEPENDENCY / TRANSFER VALIDATION:** Track A must supply browser/platform capability proof; E retains security and admission contract; C owns real device, interruption and reliability tests; B/Design Studio W121 owns accessible pairing/recovery; D/Marketing D9 owns truthful acquisition claims. Software Engineering owns native/Web implementation and test environment, Product/MDM operator owns authorization. **OPEN:** real managed-iPad policy, usable transport, native listener/WebRTC interoperability, one-time pairing semantics, owner-fenced transaction and physical Files custody. **Gate:** Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD.


## 18. WebRTC ICE privacy, relay dependence and genuinely offline EFB transfer — 2026-11-08 (A owns; E/C/B/D transfer)

**HISTORY / PROBLEM:** The preceding §17 established a conditional WebRTC candidate but left a critical conflation: a browser can expose RTCPeerConnection and successfully encrypt a data channel while having **no permitted discovery/signaling path or usable ICE candidate pair** on a company-managed iPad. Even an established connection does not imply the chosen path is local, internet-independent or approved by corporate network policy. The distinction matters more than adding another transport to a feature list.

**SOURCE — IETF, dated:** [RFC 8828 (January 2021)](https://www.rfc-editor.org/rfc/rfc8828.html) describes ICE's host, server-reflexive and relay address disclosure, multi-interface/VPN/proxy privacy concerns, and four IP handling modes; applications should plan for reduced host-candidate visibility and TURN where reachable. This is **protocol/privacy guidance**, not proof of an iPadOS 2026 default. [RFC 8827 (January 2021)](https://www.rfc-editor.org/rfc/rfc8827.html) is the WebRTC security architecture; DTLS transport authentication does not itself authorize a LogMate ledger owner. [RFC 8841 (January 2021)](https://www.rfc-editor.org/rfc/rfc8841.html) negotiates SCTP message size, not persistent storage or end-to-end record admission. [MDN WebRTC data channels, checked 2026-11-08](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Using_data_channels) explains DTLS encryption, negotiated message-size limits, buffering and head-of-line blocking.

**SOURCE — browser-specific, historical:** [WebKit's 2017 ICE candidate restrictions](https://webkit.org/blog/7763/a-closer-look-into-webrtc/) document a privacy policy that could withhold host candidates without media-capture permission. It is **historical WebKit evidence, not current iPadOS 26 behavior**. [W3C WebRTC issue #3109, opened 2026-05-18](https://github.com/w3c/webrtc-pc/issues/3109) reports a macOS local-network prompt from mDNS ICE; it is an issue report, **not** an iPadOS normative rule or confirmation of a LogMate prompt. Do not demand camera/microphone permission as an unapproved workaround for host-candidate restrictions. Browser implementation and MDM policy remain **CHANGE WATCH**.

### 18.1 Independent failure domains and operational interpretation

| Boundary | Necessary observable | Invalid inference |
| --- | --- | --- |
| WebRTC API availability | Construct peer connection in authorized secure page | Constructor means LAN reachable |
| Signaling | Authorized offer/answer/ICE exchange with authenticated peer | WebRTC includes automatic discovery or server-free signaling |
| ICE candidate gathering | Redacted type host/srflx/relay, errors, gathering completion | No host means device lacks Wi-Fi or an MDM block is proven |
| Candidate selection | Selected local/remote candidate types and transport, redacted network topology | DTLS connected means offline direct LAN |
| TURN/STUN | Reachable relay/discovery server and declared internet dependency | TURN success proves no-internet sync |
| Network policy | Explicit allowed SSID, client isolation, VPN/proxy, MDM and local-network controls | General Safari capability implies company EFB permission |
| App identity | Fresh pairing challenge bound to verified owner UID, device, epoch, expiration and purpose | ICE/DTLS fingerprint equals LogMate account owner |
| Durable receipt | Receiver staging, bounded chunks, owner-fenced atomic commit and cold-restart readback | DataChannel sent/ACK means data permanently stored |

**SYNTHESIS:** For a *strict no-internet* claim, test with **all external signaling, STUN, TURN and internet routes blocked**, while preserving only an operator-approved local path. Offline-loaded app shell cannot generate signaling by itself. A manually exchanged QR offer/answer is a potential foreground signaling experiment, not evidence that local host candidates or native compatibility will work. A TURN relay may be useful for connected sync but cannot be represented as direct, local or internet-independent unless the actual relay is itself locally reachable under an approved offline topology; even then it is **relayed**, not direct peer-to-peer. ICE host candidates may be withheld or obfuscated for privacy; never log raw IP addresses, candidate SDP, local hostnames, tokens or pairing secrets in analytics.

**CONTRADICTION:** A platform-level recommendation to provide TURN fallback improves online connection probability but conflicts with the EFB's potential *no-internet* requirement. This is resolved by defining two distinct acceptance profiles: **LOCAL-OFFLINE** (no external signaling/relay/network; approved local discovery, pair and durable receipt) and **CONNECTED** (documented permitted signaling/TURN and cost/privacy controls). Success in one profile never promotes the other.

**MINTTAP DECISION — research recommendation only:** Maintain manual independent Files export/restore as a separate recovery plane. Do not select WebRTC, enable capture permission, bypass MDM, or promise unattended native↔PWA synchronization without operator approval and physical device evidence. Engineering owns the native peer and owner-fenced commit; Web A owns protocol/browser distinctions, E owns trust and incident/privacy, C owns device/transport/fault testing, B/Design W121 owns explicit pairing and failure UX, D/Marketing D9 owns acquisition-claim evidence. **No product approval or code change.**

### 18.2 IP01–IP18 exact acceptance packet — DEFINED, NOT RUN

| ID | Test and falsifiable oracle |
| --- | --- |
| IP01 | Pin exact iPad model/iPadOS build, Safari tab/Home Screen/Web Clip, native peer version, MDM restrictions and operator authorization |
| IP02 | Check API availability without treating it as connectivity; distinguish secure-context/API failure |
| IP03 | Establish a **CONNECTED** baseline with explicitly authorized signaling and document candidate type selected, not raw address |
| IP04 | Repeat with all internet, STUN and TURN blocked, but authorized local network retained; prove or falsify **LOCAL-OFFLINE** |
| IP05 | Test fully disconnected airplane mode; classify absence of transport as expected, not a parser failure |
| IP06 | Test corporate Wi-Fi client isolation separately from candidate privacy restriction |
| IP07 | Compare Safari tab, Home Screen and managed Web Clip host/srflx/relay availability; mark each exact build |
| IP08 | If host candidates absent, diagnose privacy restriction, mDNS resolution and topology without seeking camera/mic permission |
| IP09 | Verify local signaling mechanism, user gesture, QR payload minimization, replay protection and expiration |
| IP10 | Verify native WebRTC stack can negotiate SDP/ICE/DTLS/SCTP with actual PWA; no inferred interoperability |
| IP11 | Record redacted selected candidate pair and prove whether any relay or external route was used |
| IP12 | Test VPN/proxy and dual-stack IPv4/IPv6 under approved policies; avoid IP-address identity binding |
| IP13 | Test negotiated maximum message size, bounded chunk size, bufferedAmount backpressure and large-ledger transfer |
| IP14 | Kill/lock/evict browser during offer/ICE and during chunks; safe abort/resume with no partial ledger mutation |
| IP15 | Wrong UID, stale owner epoch, revoked pairing and old-tab replay cannot pass receiver transaction admission |
| IP16 | Disconnect immediately after sender ACK but before durable commit; receiver cold restart proves actual receipt state |
| IP17 | Collect only privacy-safe categorical telemetry (mode, phase, candidate class, error code); redact raw SDP/IP/UID/flight data |
| IP18 | Demonstrate independent Files backup→fresh-context restore when both local and connected transfer fail |

**VALIDATION:** Protocol and browser documentation inspected; **no live EFB, no peer handshake, no candidate trace, no LogMate integration test**. Engineering/MDM-controlled execution remains OPEN. **CHANGE WATCH:** current Safari/iPadOS ICE policy, mDNS/local-network prompts, installed PWA vs managed Web Clip, native WebRTC stack, company LAN restrictions. **Gate unchanged:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## 19. Service Worker command-channel trust and build-artifact boundary (2026-11-08)

**HISTORY / PROBLEM:** Programmable Service Workers replace AppCache's coarse update model. Page-to-worker commands are useful for prefetch and controlled activation, but message delivery is not authenticated product-owner authority. A stale same-origin tab may still send commands after a user/account transition. Same-origin script injection can send the same commands; origin checks alone do not defeat XSS.

**SOURCE / STANDARD (checked 2026-11-08):** [Service Workers specification](https://w3c.github.io/ServiceWorker/) defines ExtendableMessageEvent with data, origin, source and ports; [MDN message event](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/message_event) documents page-to-worker messaging; [MDN source](https://developer.mozilla.org/en-US/docs/Web/API/ExtendableMessageEvent/source) identifies the sender, which may be Client, ServiceWorker or MessagePort. These interfaces do not authenticate Firebase UID, ledger owner epoch or a durable receipt.

**SOURCE / LOGMATE read-only:** [web/flutter_bootstrap.js](https://github.com/yhappcom/logmate/blob/main/web/flutter_bootstrap.js), blob a70625e8bda32aafd5dd23822c017d05229f0e63, registers logmate_service_worker.js with base-path scope and updateViaCache none. It sends versioned START_PRECACHE (api 1) and PROMOTE_VERIFIED_CANDIDATE (api 2) commands to waiting/active/controller. The source path web/logmate_service_worker.js returned 404 on main during this inspection. This **does not prove** a normal-build or deployed worker is missing: generation during build is possible. The receiving handler, generated build artifact and served SHA remain **UNKNOWN**. A sender comment asserting verified-candidate guarding is not a receiver test.

### 19.1 Trust and operational judgment

| Boundary | Required oracle | Invalid inference |
| --- | --- | --- |
| Command schema | Allowlisted api/type, bounded payload, reject malformed/unknown commands | Any same-origin command is safe |
| Sender and scope | Validate event source/client and intended scope for sensitive operations | Same origin equals authenticated account |
| Worker version | Identify waiting, active and controller recipients independently | One postMessage implies current controller accepted it |
| Cache promotion | Independently verified full candidate inventory before catalogue promotion | PROMOTE command or ACK proves offline readiness |
| Account mutation | Verified UID/epoch and transaction-time write fence | Worker message authorizes erasure, restore or sync |
| Storage custody | CacheStorage, IndexedDB/Sembast, remote ledger and Files tested separately | Worker replacement deletes all 37 stores or creates backup |
| Telemetry | Anonymous command type/version/phase/error | Logging raw payloads, tokens or flight data is acceptable |

**SYNTHESIS / CONTRADICTION:** START_PRECACHE can help offline preparation but cannot prove usable offline ledger; PROMOTE_VERIFIED_CANDIDATE can help update continuity but cannot prove schema rollback, owner deletion or Files recovery. Verify sender/schema and idempotence, but do not claim that a same-origin check blocks XSS. A compromised same-origin script may send permitted messages. Browser/deployment script integrity, CSP and incident response remain separate controls. The authenticated data plane must enforce UID/epoch and transactional authorization independently.

**TRANSFER VALIDATION:** A owns browser lifecycle/message semantics; E owns deployment integrity, security and incident handling; C owns race/fault testing; B/Design Studio W121 owns accessible preparing/verified/update-waiting/offline-error UI; D/Marketing D9 owns truthful offline/install claims. Engineering owns generated worker, exact normal build and real owner-fenced store mutations. No product change authorized.

### 19.2 WM01–WM16 acceptance packet — DEFINED NOT RUN

| ID | Falsifiable scenario |
| --- | --- |
| WM01 | Pin product SHA/build command, generated worker SHA and actual served response; distinguish source-path 404 from build-artifact absence |
| WM02 | Inspect entire receiving message handler, schema, sender checks and cache verification before promotion |
| WM03 | Reject missing, malformed, oversized and unknown api/type without state change or secret logging |
| WM04 | Send messages from V1, V2, restored and wrong-path same-origin tabs; verify intended routing |
| WM05 | Address waiting, active and controller separately; record exact recipient/version and no false ACK |
| WM06 | Try promotion before full shell/font/notice verification and during partial corruption; no promotion |
| WM07 | Duplicate and reorder commands; idempotent state after worker termination/restart |
| WM08 | Interrupt after download but before catalogue commit; known-good offline recovery |
| WM09 | Handle null/non-WindowClient source without unchecked URL dereference |
| WM10 | Old owner A tab messages cannot bypass B UID/epoch transaction fence or revive erased stores |
| WM11 | Compare worker ready/status message with actual cold offline navigation/resource readback |
| WM12 | Isolated same-origin injected-script simulation; origin checks alone must not be credited as XSS protection |
| WM13 | Verify no raw payload, email, token, UID, URL or flight data in console/crash/analytics |
| WM14 | Root/subpath deployment, manifest scope and auth callbacks remain correctly bounded |
| WM15 | Compare exact Safari tab, Home Screen and managed Web Clip builds under operator-approved MDM |
| WM16 | Re-run V1/V2 rollback, terminal deletion and independent Files restore after messaging faults |

**VALIDATION / OPEN:** Standards and pinned bootstrap inspected. Generated/served worker not inspected; WM01–WM16 not run; no physical iPad, account, backup or release evidence. **CHANGE WATCH:** WebKit/Chromium lifecycle differences and generated worker build changes. **MINTTAP DECISION:** no release or worker-activation approval. Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## 20. Connectivity is not sync authority: foreground/offline recovery state contract (2026-11-08)

**HISTORY / PROBLEM — B-owned cross-track application:** A connected network interface has never been equivalent to a reachable service. Captive portals, DNS failure, TLS interception, restricted corporate LANs, local-only Wi-Fi, suspended tabs, stale auth and interrupted responses create materially different states. In an EFB PWA, displaying "online" or "synced" from a browser hint would misrepresent a pilot's logbook custody. This domain builds on §15 (coordination), §17–18 (peer reachability) and §19 (worker commands), rather than re-teaching those mechanisms.

**SOURCE / current platform (checked 2026-11-08):** [MDN Navigator.onLine](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine) explicitly calls the flag inherently unreliable: a LAN can be "online" without internet, and OS/browser heuristics differ. [MDN Background Synchronization API](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API) marks one-shot background sync **Limited availability**, requires secure contexts and describes deferred worker execution, not guaranteed delivery. [MDN Periodic Background Synchronization](https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API) is experimental/limited and browser-scheduled rather than a precise timer. [web.dev network reliability](https://web.dev/explore/reliable) separates offline resource caching from reliable end-to-end user tasks. These are generic platform statements; no Safari managed-iPad feature or LogMate runtime was tested.

### 20.1 State and authority model [SYNTHESIS / E trust consumes A facts]

| Observable | Permitted inference | Must NOT infer |
| --- | --- | --- |
| navigator.onLine true / online event | Browser heuristic says network may be usable; schedule bounded retry | Internet, backend, peer, Firebase, auth or Sync reachable |
| navigator.onLine false / offline event | Useful warning hint; local editing may still be possible | All LAN peer routes necessarily unavailable |
| Successful same-origin fetch | That specific response was obtained; may be SW cache unless bypass/control recorded | Fresh backend, authenticated owner or complete sync |
| Explicit authenticated backend request | This endpoint responded for this request and credential | All pending records accepted or durable receipt |
| Outbox queued in IDB | Local pending work exists if readback succeeds | Remote commit or durable external backup |
| Remote accepted receipt with owner/epoch/version | Server accepted specified operations under recorded authority | Other device reconciled, all local writes durable, Files backup exists |
| Native/PWA peer channel open | Transport is currently negotiated | Same account, allowed policy, durable receiving transaction |
| Cold restart + owner-scoped readback | Data remains in that tested container after restart | Survival after MDM wipe, origin migration or storage eviction |
| Fresh-context Files reopen and guarded restore | Independently recoverable artifact under tested permissions | Continuous automatic synchronization |

**MINTTAP DIRECTION — proposed state vocabulary, not approved UI copy:** `Saved on this device` requires local transaction/readback; `Waiting to sync` requires a nonempty durable outbox; `Connecting` requires an actual attempt; `Syncing` requires accepted in-flight operation; `Synced to account` requires owner/epoch/version-scoped remote receipt and reconciled pending set; `Backup verified` requires independent Files reopen/restore. `Offline ready` requires cold offline shell/resource and owner-ledger readback; a worker registration or online event is insufficient. Separate `Cannot reach service`, `Sign in required`, `Account changed`, `Conflict needs review`, `Storage unavailable` and `Backup needed` rather than collapsing all into "offline".

**Operational security:** A connectivity probe should not leak account identifiers, one-time auth action codes, raw URLs with query/fragment, IP addresses or flight records to telemetry. Avoid unauthenticated GET "health" as an authorization oracle; a health endpoint can be reachable while account-scoped writes are denied. Probes should have bounded timeout/backoff, avoid uncontrolled background battery/radio use, and never silently switch to an unapproved relay/hotspot in managed EFB mode. A success toast must be causally tied to the actual durable receipt, not to the initiation of a request or worker message.

### 20.2 Reconnection, concurrency and release logic [A → E/C/B/D]

1. **Local write:** validate current local owner epoch at the transactional admission point; persist record + outbox intent atomically where supported; read back. If storage fails, show failure and preserve original source data; never claim "saved".
2. **Attempt:** only when a user-approved channel is available, determine the *target* (account backend versus local native peer), check current credential/owner and bounded request semantics. `online` is merely a retry hint.
3. **Retry:** use stable operation IDs, deduplication, bounded exponential backoff/jitter and server/receiver idempotency. Retries after ambiguous ACK loss must not double-create flight entries. Do not assume SW background delivery; foreground resume is a required fallback.
4. **Admit:** receiver verifies UID/owner epoch, record version and conflict policy at commit time, not only during initial pairing. Deletion or A→B owner transition invalidates old queued work before any remote/local replay.
5. **Receipt:** distinguish HTTP transport completion, application acceptance, durable commit and post-restart reconciliation. Do not erase outbox solely on HTTP 200 without the required application receipt.
6. **Recover:** support interrupted sync, browser termination, SW update, network change, account switch, and independent Files restore with a truthful accessible state. User-triggered retry must remain possible when background API is absent.

**Cross-track handoff:** B owns language, navigation, focus/announcement and recovery task structure; A owns online/offline events, SW, storage and browser variance; E owns owner/epoch/receipt and privacy; C owns fault-injection, screen-reader/keyboard and cold-restart oracles; D owns prohibition of unverified "automatic sync", "offline safe" or "fully backed up" claims. Design Studio W121 supplies execution-level UX checks, Engineering S007 owns actual deletion/owner transactions, Marketing owns public claims. No independent sixth specialist.

### 20.3 RC01–RC20 integrated acceptance packet [VALIDATION DEFINED, NOT RUN]

| ID | Falsifiable test |
| --- | --- |
| RC01 | LAN connected but internet blocked: onLine true must not yield remote-ready/synced claim |
| RC02 | Captive portal, DNS failure, TLS failure and HTTP 503 distinguished from user-offline |
| RC03 | SW-cached 200 versus genuine network response identified without private data exposure |
| RC04 | Endpoint reachable but Firebase session expired: auth-required state, no outbox loss |
| RC05 | Correct UID but revoked owner epoch: queued old-owner writes denied |
| RC06 | A→B switch with old tab, old worker and delayed response: no stale receipt promotion |
| RC07 | Transaction storage/quota failure: no false "saved locally" state |
| RC08 | App killed after outbox commit but before send: pending survives cold restart |
| RC09 | Send accepted but response lost: replay same operation ID produces one durable result |
| RC10 | HTTP 200 without application receipt: outbox remains pending |
| RC11 | Receipt arrives after account deletion: no unauthorized local revival |
| RC12 | Sync operation conflicts with newer record version: explicit review/merge state |
| RC13 | Worker Background Sync unavailable: foreground resume/retry remains functional |
| RC14 | Worker Background Sync supported but suspended/throttled: no guaranteed timing claim |
| RC15 | Safari tab, Home Screen and managed Web Clip tested separately with pinned OS/MDM |
| RC16 | LOCAL-OFFLINE peer reachable but cloud unreachable: peer receipt not labeled cloud synced |
| RC17 | CONNECTED relay available but company policy denies it: no automatic fallback |
| RC18 | VoiceOver/keyboard/zoom and slow network: status and retry accessible, no misleading progress |
| RC19 | Logs/analytics contain only categorical phase/error; no UID/email/SDP/flight payload |
| RC20 | Fresh Files artifact reopen/guarded restore and cold offline owner readback independently verified |

**VALIDATION / OPEN:** Source-level generic research and a proposed state machine only. RC01–RC20 **not executed** on LogMate, served PWA, native peer, Safari or managed EFB. **CHANGE WATCH:** iPadOS/WebKit background scheduling, storage containers, enterprise network policy and actual Firebase/API contracts. **Gate unchanged:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD. No product/peer changes.


## 21. Offline authentication persistence is not owner authorization (2026-11-08)

**HISTORY / PROBLEM — E owns trust, A supplies browser mechanics:** Offline-first applications must let an authorized local user resume work without claiming that an unavailable identity provider has revalidated them. Firebase Auth persistence, local logbook custody, cached network responses and the authority to upload changes are four different contracts. This complements §15 concurrency, §19 Worker messaging and §20 reconnect receipts; it does not reassert those findings.

**SOURCE (checked 2026-11-08):** [Firebase Auth web state persistence](https://firebase.google.com/docs/auth/web/auth-state-persistence) defines LOCAL, SESSION and NONE, explains cross-tab behavior and explicitly distinguishes Auth persistence from Firestore offline data persistence. [FlutterFire firebase_auth Persistence enum](https://pub.dev/documentation/firebase_auth/latest/firebase_auth/Persistence.html) additionally exposes INDEXED_DB; exact plugin/version selection matters. [MDN PWA caching](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Caching) and [MDN Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) explain independently managed resource caches and intercepted fetches. These are **generic platform/provider facts**, not LogMate configuration or iPad runtime observations.

### 21.1 Distinct security predicates [SYNTHESIS]

| Predicate | Evidence required | Counterexample / forbidden inference |
| --- | --- | --- |
| Auth SDK remembers prior user | Exact SDK instance, persistence choice, resolved currentUser and account state | LOCAL session state is not a fresh server-side entitlement check |
| Local owner ledger readable | Exact container, owner/replica namespace, transaction readback and lifecycle | Remembered Firebase UID does not grant access to every local record |
| Local edit admitted offline | App-specific owner epoch + deletion/revocation fence checked in same write admission transaction | Offline JWT or cached screen cannot override local terminal deletion |
| Remote mutation authorized | Server verifies current token, UID, owner epoch, operation ID, version and applicable security rules at commit | Previously valid offline session cannot pre-authorize future uploads |
| Cached response safe to reuse | Explicit classification, owner partition, freshness and invalidation policy; inspect actual Worker | Cache hit is not authenticated live response; HTTP no-store alone does not prove SW/IDB erasure |
| Sign-out/deletion completed | Distinguish SDK sign-out, local ledger wipe, queued operations, remote account deletion and Files artifact | Clearing an Auth persistence key is not an erasure proof |
| Offline user can recover | Exact product policy for unlock/reauth, non-destructive recovery, external backup and restricted iPad | Network unavailability must not silently reset, cross-link or discard flight data |

**Operational judgment / proposed product requirements (NOT approved implementation):** Use separate UI states for `Known local owner`, `Local access requires verification`, `Remote session needs sign-in`, `Local write blocked after deletion intent` and `Pending sync requires authorization`. Whether an offline local unlock can be supported is a product security decision requiring explicit threat model for a shared/managed EFB; do not invent an offline credential or assume biometric APIs. On account A→B transition, never infer that SDK cross-tab synchronization fences every open editor or queued write. Transactional owner epoch checks remain required. An offline user may need an accessible non-destructive export/recovery route even when cloud authentication is expired, but any export must satisfy actual custody/authorization policy.

### 21.2 Failure modes, policy boundaries and cross-track transfer

1. **Persistence mismatch:** SESSION/NONE/LOCAL/INDEXED_DB have distinct restart and tab semantics; the actual FlutterFire plugin, initialization path and WebKit container must be inspected. Provider documentation for JS SDK does not establish the app's Dart configuration.
2. **Revocation delay:** a previously authenticated offline session may remain locally visible when remote revocation cannot be queried; deny remote replay until live server admission, and separate any local-only entitlement from cloud identity.
3. **Shared managed iPad:** Home Screen, Safari tab and managed Web Clip can differ in storage context. Test separately; no universal cross-container sign-out or cache purge is assumed.
4. **Cached account response:** ensure no account-scoped API/HTML/token response is served from a stale public cache; audit Worker match/fetch strategy and CacheStorage names in generated/served build.
5. **Sign-out vs deletion:** sign-out can preserve user-owned offline records under an explicitly approved custody model; terminal deletion must instead prove all required stores and queued intents removed. Do not substitute one for the other.
6. **Reauthentication UX:** preserve unsynced edits when remote sign-in is required, prevent duplicate uploads, and make user-visible local/remote scope explicit without revealing email, UID or token in telemetry.
7. **Storage pressure / reset:** Auth persistence, application IndexedDB, CacheStorage and external Files can fail or be evicted independently; verify each with a cold restart and independently reopened artifact.
8. **Policy / privacy:** shared-device access controls, corporate MDM restrictions and permitted retention are product/operator facts, not determined by Firebase SDK defaults.

**Cross-track allocation:** E owns trust boundary and release gates; A owns persistence/container mechanics; C owns cross-browser fault and cold-start oracle; B owns truthful sign-in/offline/recovery flows using Design Studio W121; D owns consent-safe analytics and blocks “offline authenticated”, “fully synced” and “securely backed up” claims absent matching evidence. Engineering owns exact FlutterFire/Sembast/server implementation; Marketing owns public claim approval. No duplication of those disciplines.

### 21.3 AU01–AU18 exact-product validation packet [DEFINED NOT RUN]

| ID | Acceptance question |
| --- | --- |
| AU01 | Pin exact LogMate main SHA, firebase_auth dependency/version and initialization persistence choice |
| AU02 | Compare first sign-in, cold reopen and explicit sign-out under each actually supported persistence mode |
| AU03 | Separate Safari tab, Home Screen PWA and approved managed Web Clip containers |
| AU04 | Offline cold launch with valid prior account but unreachable Firebase: no false remote-auth assertion |
| AU05 | Expired token with cached local records: no automatic remote-success or data loss |
| AU06 | Revoked account while device offline, then reconnect: receiver denies stale unauthorized replay |
| AU07 | Account A→B in second tab while A editor remains open: transaction fence prevents A write into B |
| AU08 | SESSION versus LOCAL cross-tab changes checked against actual plugin behavior, not assumed JS defaults |
| AU09 | Worker cache contains no account-specific auth response accessible to another owner |
| AU10 | Sign-out does not falsely report terminal account deletion or verified Files erasure |
| AU11 | Terminal deletion covers full store registry and pending outbox, then cold-reopen negative canaries |
| AU12 | App restart after quota/IDB error distinguishes lost Auth state from lost local ledger |
| AU13 | Remote login required during pending sync: outbox remains intact and owner-bound |
| AU14 | Sign-in completes for different UID: old outbox not replayed under new UID |
| AU15 | Network restored with old cached 200: explicit server receipt/owner/version required for sync success |
| AU16 | Screen reader, keyboard and low-connectivity sign-in/recovery tasks preserve accessible status |
| AU17 | Crash/telemetry/analytics contain no token, email, raw auth URL, UID or flight data |
| AU18 | Independently reopened Files backup restores in fresh authorized context after browser data reset |

**VALIDATION / OPEN:** AU01–AU18 are **not run**. No exact current FlutterFire persistence, deployed cache, managed iPad, remote admission, offline unlock policy or product behavior verified in this section. **DEPENDENCY:** Engineering-approved disposable account/runtime and physical EFB operator; Q01–Q03 remain P0. **CHANGE WATCH:** Firebase Auth SDK/FlutterFire versions, Safari/WebKit storage partitioning, MDM rules. **MINTTAP DECISION:** no new policy approval; Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## 22. CSP policy rollout across PWA document, Worker and Auth action surfaces (2026-11-08)

**HISTORY / PROBLEM — E owns security policy; A owns browser enforcement:** A site-wide Content Security Policy is often proposed as a single security switch. For a Flutter Web PWA with a separately fetched Service Worker, an auth-action document and dynamically loaded engine resources, that model is incomplete: policy is attached to **responses and execution contexts**, not to the brand or repository. A stringent untested policy can block first paint, Worker installation, offline recovery, Firebase network requests or legitimate authentication, while a permissive policy may not meaningfully reduce XSS risk. This section is an independent Stage 8 deployment-security dependency, not another owner-deletion audit.

**SOURCE — primary/current, checked 2026-11-08:**
- [MDN CSP response-header reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy): fetch-directive fallbacks, multiple policy intersection and independently delivered Worker response policies.
- [MDN worker-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/worker-src): controls Worker/SharedWorker/ServiceWorker script source; absent worker-src falls back through child-src, script-src, default-src.
- [MDN require-trusted-types-for](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for): typed DOM injection-sink enforcement; MDN now labels cross-browser Baseline 2026, **not** evidence that an older managed iPad or a particular Flutter build is compatible.
- [W3C CSP Level 3](https://www.w3.org/TR/CSP3/): normative directive model. Browser support, report delivery and enforcement must be measured per actual runtime.

**Exact product SOURCE (read-only, 2026-11-08; product commit must be pinned separately for execution):** LogMate `firebase.json` blob `9ac0972e26749215c4a718360c66315c6caf3cc8` has wildcard `Cache-Control: no-cache, no-store, must-revalidate` but **no declared CSP response header in that file**. `web/index.html` blob `01be77585ac40bf11e80777177a4ab08e4885671` loads `flutter_bootstrap.js` and manifest relative to `$FLUTTER_BASE_HREF`. `web/flutter_bootstrap.js` blob `a70625e8bda32aafd5dd23822c017d05229f0e63` registers `logmate_service_worker.js` using the resolved base URL, calls `registration.update()`, posts two update commands, and loads Flutter engine with a versioned font fallback URL. **No conclusion about deployed CSP headers, generated Worker script, third-party scripts, app-network endpoints, or security effectiveness follows from these three files alone.** Firebase Hosting config can differ from final served headers via deploy target, proxy/CDN or other infrastructure.

### 22.1 Five distinct policy boundaries [SYNTHESIS]

| Boundary | Enforcement / failure mode | Decisive evidence |
| --- | --- | --- |
| Top-level app document | `script-src` / `style-src` / `connect-src` / `font-src` / `img-src` may block Flutter bootstrap, renderer, fonts, auth and APIs | Actual HTTPS document headers + runtime violation/console/resource trace |
| Worker registration | Document's `worker-src` and fallback govern permitted Worker script source | Normal/installed app `register()` result, worker script URL, scope and policy |
| Worker execution | Worker script response's **own** CSP governs its internal fetch/execution, not automatically the document's CSP | Worker script response headers + install/activate/fetch/candidate-cache traces |
| Auth action/rewrite | `/auth`, `/auth/`, `/auth/action` and final action HTML can have different served headers and query handling | Per-route status/redirect/header capture with synthetic one-time code, no real token |
| Offline cached shell / update | Old document/Worker and new server policy may coexist; an offline shell may not see newly deployed policy until replacement | V1/V2 version-pinned cold start, old tab, offline reload, rollback, cache catalogue and auth negative controls |

**Important nuance:** CSP is a defense-in-depth restriction on execution/resource loading, not authentication, authorization, storage erasure, account deletion or a guarantee of XSS absence. `worker-src 'self'` may be appropriate in principle for a same-origin worker but must not be shipped as an untested blanket rule. CSP `Report-Only` reports violations without enforcement; it is a diagnostic stage, not a security PASS. Multiple enforced CSP headers are restrictive in combination; an additional permissive header does not undo an existing restrictive one. A meta CSP is not equivalent to response-header delivery for all directives or early requests. Trusted Types is a separate sink discipline; enabling it without auditing Flutter/third-party DOM sinks may break legitimate execution.

### 22.2 Proposed staged admission [MINTTAP DECISION — research recommendation, NOT approved deployment]

1. **Inventory:** capture exact normal/acceptance build, served HTTPS routes and resources, including Worker JS, Flutter JS/WASM, fonts, Firebase Auth/API calls, WebSocket/connect endpoints, analytics/consent scripts and auth-action redirects. Avoid inventing an allowlist from static filenames.
2. **Report-only lab:** test a candidate least-privilege policy on a disposable staging origin with privacy-minimized reports. Keep an explicit inventory of violations and justified exceptions; do not send URL query strings, account IDs, flight data or auth codes to reporting endpoints.
3. **Negative controls:** intentionally disallow the Worker script, one required font and one API endpoint *in isolated test environments* to verify telemetry and accessible failure/recovery UI. Do not run these tests against production/operational EFBs.
4. **Cross-context rollout:** separately verify document, Worker script and auth action response policies. Test browser support and policy compatibility on pinned Chromium, Safari tab, installed Home Screen and authorized managed Web Clip; test both online and cold offline after V1→V2.
5. **Progressive enforcement:** move only source-proven, runtime-tested directives from report-only to enforced staging, then a controlled release. Explicit rollback must restore a working shell/Worker without discarding IndexedDB or user Files. Preserve independent owner-deletion and Files custody gates.
6. **Trusted Types decision:** test current Flutter renderer and every DOM-writing dependency under `require-trusted-types-for 'script'` before considering enforcement; browser support does not establish product compatibility. Track older OS versions separately.
7. **Incident observability:** record aggregate directive/resource category, build ID, platform family and failure phase, with query/fragment/token/UID/flight data redacted; sampling and retention require privacy review. Reports can be blocked or lost and are not exhaustive.

### 22.3 CP01–CP18 falsifiable validation packet [DEFINED NOT RUN]

| ID | Acceptance / negative control |
| --- | --- |
| CP01 | Pin exact deployed build, origin and response headers for app HTML, Worker JS, auth action and font assets |
| CP02 | Distinguish CSP absent in source firebase.json from CSP absent on served HTTPS; no inference without capture |
| CP03 | `worker-src` deny negative control blocks test Worker registration and reports the correct directive |
| CP04 | `worker-src 'self'` candidate permits actual same-origin Worker registration at root and subpath |
| CP05 | Worker script response CSP independently permits required install/activate/fetch operations |
| CP06 | `script-src` candidate preserves Flutter bootstrap, engine/WASM and relevant lazy-load paths |
| CP07 | `style-src`, `font-src`, `img-src` preserve offline fallback fonts, icons and accessible error UI |
| CP08 | `connect-src` permits intended Firebase/auth/API endpoints but blocks an intentionally forbidden test endpoint |
| CP09 | `/auth`, `/auth/`, `/auth/action` rewrite/redirect have correct policy, status and no real-token reporting |
| CP10 | Enforced versus report-only modes show expected differences; reports do not imply user-data access |
| CP11 | Multiple CSP headers tested for intersection; permissive second header cannot override restrictive first |
| CP12 | Trusted Types candidate tested on exact Flutter renderer/dependencies, with isolated DOM-sink negative control |
| CP13 | Chrome and pinned Safari/iPadOS behavior tested independently, including unsupported/older versions |
| CP14 | V1 controlled old tab plus V2 Worker policy update: no dead shell, wrong account or silent data loss |
| CP15 | Offline cold launch under previously cached shell and post-update rollback both preserve local owner ledger |
| CP16 | CSP-blocked API/auth yields truthful accessible retry, not false 'offline' or 'synced' state |
| CP17 | Violation telemetry strips query, fragment, auth code, email, UID, SDP and flight data |
| CP18 | Independent Files reopen/restore and 37-store terminal deletion remain separate required P0 proofs |

**TRANSFER VALIDATION:** A provides response/context/Worker fallback semantics; E owns policy design, privacy, staged deployment and rollback; C owns lab/runtime/assistive-technology and fault tests; B owns blocked-resource, sign-in and offline recovery tasks (Design Studio W121 remains visual/accessibility execution dependency); D owns privacy-safe observability and public claim restraint (Marketing D9 remains HOLD). Engineering owns exact Flutter/Hosting policy implementation and tests. No peer/product repository write.

**OPEN / DEPENDENCY:** CP01–CP18 NOT RUN; actual delivered headers, generated Worker and exact Flutter CSP/Trusted Types compatibility unknown. Company-managed iPad policy and installed PWA behavior unknown. Q01–Q03 P0 owner-deletion, old-writer and Files custody remain unchanged. **CHANGE WATCH:** CSP/Trusted Types browser versions, Flutter renderer, Firebase Hosting delivery and OS/MDM updates. **Gate:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.


## §23 — COOP/COEP isolation versus federated authentication and offline PWA continuity (2026-11-08)

**Ownership/gate:** E leads browser security/deployment decision; A owns browsing-context and response-policy mechanics; C owns exact browser regression; B owns accessible login recovery; D consumes truthful acquisition/attribution boundaries. **SOURCE/SYNTHESIS; VALIDATION DEFINED NOT RUN.** No new deployed LogMate evidence, no claim of present vulnerability. Prior §22 CSP/Trusted Types is adjacent but not equivalent: CSP governs permitted content/execution, whereas COOP affects opener browsing-context groups and COEP constrains cross-origin resource embedding.

### History → standard → operational consequence
Cross-origin opener relationships permit limited window references even under the same-origin policy and have enabled XS-Leak classes. COOP can sever those relationships at navigation/window-open boundaries. COEP restricts eligible cross-origin embedded resources and is part of enabling cross-origin isolation for capabilities such as SharedArrayBuffer. Neither header authenticates a user, authorizes IndexedDB writes, guarantees service-worker cache integrity or makes a managed iPad PWA durable. Sources checked 2026-11-08:
- MDN COOP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy (current reference, consulted 2026-11-08).
- Chrome/web.dev cross-origin isolation deployment guide: https://web.dev/articles/coop-coep (Chromium-oriented deployment explanation, consulted 2026-11-08).
- MDN same-origin policy: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy (consulted 2026-11-08).

**SOURCE distinction:** `COOP: same-origin` can separate cross-origin popup browsing-context groups and break opener-reference-dependent OAuth flows. `COOP: same-origin-allow-popups` permits an opener relationship with a popup using `unsafe-none` under the documented window-open conditions, but is **not** interchangeable with the `same-origin` requirement for ordinary cross-origin isolation. `COEP: require-corp` can block otherwise functional cross-origin resources lacking an appropriate CORS/CORP opt-in. `COEP: credentialless` is a distinct policy with browser-support and credential-stripping trade-offs; do not assume Safari parity. Actual result depends on BOTH opener and popup responses, redirect chain, browser and provider SDK. A generic popup mechanism is not proof that LogMate uses it on each platform.

### Failure-mode integration and counterexamples
1. **Security header regression:** globally adding strict COOP to the Firebase Hosting wildcard route could sever provider popup communication while a password/email route still works; an apparent login failure is not proof of Firebase outage.
2. **Resource isolation regression:** COEP enforced on the Flutter shell may block third-party assets, auth helper frames or runtime dependencies unless their response policies opt in. Report-only observation must precede enforcement where available; a clean console in one browser is not cross-browser PASS.
3. **False security equivalence:** choosing `same-origin-allow-popups` to preserve an OAuth popup does not establish `crossOriginIsolated === true`; do not advertise SAB/thread readiness.
4. **False application equivalence:** browser popup completion does not prove current UID, local account generation, remote sync admission or old-owner writer denial.
5. **Deployment mismatch:** shell HTML, `/auth/action` navigation, helper/redirect response, worker JS and static assets may receive different policies via Hosting rewrites, CDN or intermediary. Source `firebase.json` alone cannot establish served response headers.
6. **EFB difference:** iPadOS Safari, Home Screen PWA and managed Web Clip may differ in popup presentation and permitted external authentication; no desktop Chromium result can clear a managed EFB acceptance gate.
7. **Rollback risk:** if V2 changes COOP/COEP and V1 remains worker-controlled, cached shell and live network response can mix; reloading after rollback must be checked with existing local logbook and pending writes intact.
8. **Privacy and attribution:** cross-origin window relationships and referrer/telemetry are separate controls; a change in popup behavior cannot justify claiming safer user-data custody or successful acquisition attribution.

### Transfer validation: executable CI/browser/device packet (OI01–OI18)
**E/A source/served inventory:** OI01 pin current LogMate SHA and all Hosting rules; OI02 capture exact normal HTTPS headers for shell, auth action, worker JS, manifest and provider redirect; OI03 compare no-header, COOP same-origin, same-origin-allow-popups in disposable test origin; OI04 compare COEP absent/report-only/require-corp with asset network traces; OI05 record redirect-chain response headers and opener relationships without real credentials; OI06 distinguish `crossOriginIsolated` from successful sign-in.

**C execution/failure controls:** OI07 email sign-in, OI08 Google popup/redirect, OI09 Apple popup/redirect, OI10 popup closed/cancelled, OI11 blocked third-party cookie/storage or popup, OI12 two-version worker/cache rollback, OI13 offline cold relaunch with pending writes, OI14 Chromium versus Safari/WebKit browser-specific trace, OI15 managed iPad Safari/Home Screen/Web Clip authorized non-destructive trial.

**B/D and owner-security oracles:** OI16 accessible failure/retry with focus, non-leaking status and preserved unsynced logbook; OI17 consent-safe auth conversion telemetry with no codes/tokens/URLs captured; OI18 old-owner tab/account A→B denial at storage and remote-admission points. Negative control: an intentionally isolated disposable popup should demonstrate opener severance; positive control: an allowed disposable popup should complete without asserting product PASS.

**MINTTAP DECISION:** do not recommend blanket COOP/COEP deployment or claim cross-origin isolation as an existing feature. First inventory whether a specific feature requires it; test a disposable exact-built origin and all authentication methods. Use route-specific policy only after complete route and browser coverage, with explicit security review; never weaken policy solely to suppress an error without understanding the opener/resource threat model.

**DEPENDENCY:** Engineering owns exact FlutterFire auth implementation, normal build, test fixtures and product runtime; operator owns live Hosting/MDM authorization; Design Studio W121 owns visual accessibility transfer; Marketing owns product/store claims. **OPEN:** actual deployed headers, auth method implementation, Safari/managed device behavior, COEP subresource inventory, rollback/Files and local ownership checks. **CHANGE WATCH:** browser COOP/COEP support and identity-provider SDK redirect/popup behavior, especially WebKit. **VALIDATION:** OI01–OI18 are defined, not executed. Stage 8 ACTIVE / Production OPEN / PWA release HOLD.


## 24. Stage 8 — HTTP cache, Cache API and Clear-Site-Data as a destructive offline-data boundary (2026-11-08)

**Problem/history:** A security hardening checklist may suggest `Cache-Control: no-store` or `Clear-Site-Data: "storage"` for logout. Those mechanisms address different storage layers and can conflict with an offline-first logbook. A conventional web session may tolerate clearing local state; an EFB containing the only unexported flight record cannot. This is an application of the existing owner/deletion/backup contracts, not evidence of a LogMate production incident.

**SOURCE (reviewed 2026-11-08):**
- MDN [HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) and [Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control): `no-cache` permits storage but requires revalidation; `no-store` prohibits HTTP-cache storage, not deletion of previously cached copies; `private` restricts shared caches.
- MDN [Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache): Cache API is application-managed and **does not honor HTTP caching headers**; `Cache.match` accounts for `Vary`, but `Vary` is not an authorization check. Application code must enforce response admission, expiration, and invalidation.
- MDN [Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data): `"storage"` includes IndexedDB and Service Worker registrations; `"cookies"` may affect the registrable domain/subdomains; `"cache"` has broader browser-cache effects. Header support and directive effects must be verified per engine and device.
- MDN [Using Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers): Worker install and fetch caching are explicit program behavior, separate from ordinary HTTP cache policy.

**SYNTHESIS — five independent boundaries:**
1. HTTP browser/CDN cache: response directives and shared-cache behavior; `no-store` does not purge historical entries.
2. Script-managed CacheStorage: response pairs, possibly including `no-store` responses if explicitly inserted; a cache key or `Vary` match is not UID/owner-epoch proof.
3. IndexedDB/Sembast: canonical offline records/outbox; must not be conflated with disposable app-shell assets.
4. Service Worker registration/lifecycle: can survive page reload and serve older app shell; unregistering does not prove old clients stopped writing.
5. Independently verified Files export: separate custody, not established by a successful download click or by origin storage persistence.

**Security failure modes and counterexamples:** 
- Authenticated JSON is cached via `cache.put` under a URL and replayed after account A→B; HTTP `private` or `no-store` alone cannot authorize a Cache API read. Avoid caching sensitive auth/owner-scoped API responses in the shell cache; enforce UID+generation at the actual data-access/admission boundary.
- A logout endpoint unconditionally returns `Clear-Site-Data: "storage"`, erasing unsynced IndexedDB/outbox and worker registration. This can destroy the sole local copy while an operator believes logout merely ends authentication. Do not apply blanket storage-clearing headers on sign-out, token refresh failure, 401, auth callback, or routine deployment.
- `Clear-Site-Data: "*"` sent from an authentication or shared-origin route can have a wider effect than intended. Domain/subdomain cookie impact, origin scope and cross-browser differences must be separately traced.
- A network response changes to `no-store` while a previous Worker still serves a stale shell or manually cached response. No retroactive purge or upgrade safety follows from the header.
- A supposedly privacy-preserving cache purge removes offline shell needed to reopen and export pending records. Security and recoverability must be jointly tested, not traded silently.
- A `Vary: Authorization` or cookie-dependent response is treated as a reliable per-account data partition. Cache key matching is not a substitute for ownership and session validation.

**MINTTAP DECISION (provisional safety requirement, not implementation approval):** Default to a strict **no-personal-data-in-app-shell-cache** policy; use HTTP `private`/`no-store` for genuinely sensitive responses as appropriate, while explicitly excluding such responses from programmatic Cache API insertion. Do not use `Clear-Site-Data: "storage"` or `"*"` as a generic logout, incident, or deployment recipe for an offline-first product. Destructive owner erasure is a distinct confirmed, recoverable product workflow with exact local/remote ownership fencing and independent-backup checks. Preserve the possibility of intentional user-authorized deletion without conflating it with sign-out. Any actual header change requires route inventory and Engineering/operator approval.

**TRANSFER VALIDATION — HC01–HC20 (defined, not executed):** HC01 pin exact product SHA/normal build and served headers; HC02 inventory shell/API/auth/logout/redirect/worker response classes; HC03 trace HTTP cache vs CacheStorage vs IndexedDB before/after fetch; HC04 prove `no-store` does not delete old Cache API entry; HC05 prove `Vary` matching is not UID authorization; HC06 negative-control manual `cache.put` for a disposable `no-store` synthetic response; HC07 account A→B replay denial; HC08 stale controlled tab after sign-out; HC09 401/expired token with pending outbox; HC10 logout route and redirect header inventory; HC11 deliberate `Clear-Site-Data: "storage"` only in a disposable origin to observe IDB/SW effects; HC12 `"cache"`-only effects; HC13 `"cookies"` registrable-domain impact in a nonproduction isolated domain; HC14 browser restart with unsynced record; HC15 offline cold launch and independent Files export; HC16 worker V1/V2 rollback; HC17 Safari tab vs Home Screen vs managed Web Clip; HC18 Chromium baseline; HC19 screen-reader/focus and truthful unsynced warning; HC20 privacy-safe telemetry with no flight contents, tokens or identifiers. Negative-control origins must never contain user flight data.

**Cross-track ownership:** E owns security/deletion/header policy; A owns browser HTTP/CacheStorage/Clear-Site-Data semantics; C owns independently falsifiable layered-storage oracles; B owns explicit sign-out versus erase, offline/recovery messaging and Design Studio W121 transfer; D owns truthful privacy/backup/sync claims and Marketing HOLD. Engineering owns exact Flutter Web/Sembast/runtime validation. **DEPENDENCY:** route-specific served responses, current Worker code, actual owner-fenced local transaction, managed-device policy. **OPEN:** no actual LogMate response headers, logout behavior, Safari/WebClip storage-clearing or product test has been established here. **CHANGE WATCH:** Clear-Site-Data directive support, WebKit storage behavior, CDN/Hosting rewrites. **VALIDATION:** HC01–HC20 specification only; Stage 8 ACTIVE / Production OPEN / PWA release HOLD.


## 25. Stage 8 — PWA OS share ingress/egress is not a trusted Files backup or cross-device sync channel (2026-11-08)

**Problem and history:** OS share sheets make a web application appear native, but **sharing out** (Web Share) and **being a share target** (manifest `share_target`) are different capabilities. Neither establishes that an external backup exists, that a recipient retained it, or that an incoming file belongs to the current logbook owner. This closes a distinct PWA capability and untrusted-input boundary after §§16–24, not a re-run of blocked managed-iPad Files acceptance.

**SOURCE (primary documentation checked 2026-11-08):**
- [MDN Web Share API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API): secure context, user activation, `navigator.share` and `navigator.canShare`, Permissions Policy; share promise completion is not durable recipient custody.
- [MDN share_target manifest](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/share_target): experimental/limited support, installed PWA registration, `POST multipart/form-data` for files, possible Service Worker fetch interception, untrusted input validation and redirect-after-POST.
- [web.dev OS integration](https://web.dev/learn/pwa/os-integration): documents Android WebAPK/ChromeOS share-target availability in that guidance; this is **not** evidence of iPadOS share-target support or managed-Web-Clip registration.
- [MDN web-share Permissions Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy/web-share): policy gates outgoing `navigator.share`, not proof that the PWA can receive OS shares.

**SYNTHESIS / threat and failure analysis:**
1. Outbound user gesture → share-sheet UI → recipient selection → API settlement → recipient persistence → independent readback → validated restore are separate events. An API-resolved promise is not an externally verified Files backup.
2. Inbound OS share → browser navigation/POST → Service Worker/form-data parse → bounded staging → file authenticity/format/owner checks → explicit user confirmation → atomic import is a separate pipeline. File extension, MIME, name, manifest `accept`, share-sheet selection and HTTPS origin do **not** authenticate contents or user ownership.
3. A Service Worker receiving POST may be restarted, updated, or interrupted; a temporary Cache/IDB handoff is origin-scoped, subject to quota/eviction and stale-client races. Never treat temporary share staging as an independent archive.
4. GET share targets can put text/URLs into navigation query strings, history, referrer and telemetry; use POST for file/side-effect ingress, keep sensitive payloads out of URL/logs, and apply existing auth-route/referrer constraints.
5. Cross-account A→B and old Worker V1→V2 must fence staged shares at the **actual admission transaction**, not at the UI route or Worker message. Repeated POST, refresh and redirect replay require idempotency and explicit conflict handling.
6. A hostile or malformed incoming file may be huge, truncated, duplicate-key JSON, deeply nested, wrong-schema, wrong-account, or have deceptive MIME/extension. Size/row/depth bounds, independent integrity/format admission, no-write preview, rollback and safe rejection must precede mutation.
7. Browser support is asymmetric: outgoing share may work on iPadOS while incoming installed-PWA share-target registration does not. Safari tab, Home Screen PWA, managed Web Clip and Chromium Android must be independently tested. A browser standards draft or desktop Chrome PASS is not a managed EFB capability PASS.
8. OS share UI and native-to-PWA transfer are **user-mediated**, not evidence for unattended device-to-device sync, background operation, hotspot permission or MDM transfer policy.
9. A shared flight logbook is sensitive personal data: outbound share must show destination/data scope and require explicit action; telemetry must not include flight contents, account identifiers, filenames with personal data, file bytes or share URLs.

**MINTTAP DECISION (provisional):** Do not promise OS share as the LogMate EFB backup, import, automatic sync, or installation path. Keep explicit file-picker/Files readback/restore as the independently tested fallback; consider share integration only as an optional, per-platform enhancement after security review. Do not add `share_target` to production manifest merely because a share-sheet demo works.

**TRANSFER VALIDATION — SH01–SH18 (DEFINED, NOT RUN):** SH01 exact manifest and served MIME/headers; SH02 installed Android/ChromeOS inbound availability; SH03 Safari tab/Home Screen/managed Web Clip share-target presence or absence; SH04 outgoing user activation and cancellation; SH05 `canShare` file-type and Permissions Policy denial; SH06 outbound share resolution vs actual recipient Files readback; SH07 offline inbound POST Worker interception; SH08 Worker absent/uncontrolled first navigation; SH09 Worker killed during multipart parse; SH10 oversized/deep/invalid MIME and wrong-extension payload; SH11 duplicate JSON keys/unsafe numeric identity in .lbk; SH12 account A→B while staged file pending; SH13 Worker V1/V2 update and stale client; SH14 repeated POST/refresh and 303 redirect; SH15 quota exhaustion/IDB rollback and zero-write reject; SH16 explicit preview and accessible recovery/focus; SH17 telemetry/referrer/URL privacy; SH18 genuine exported file → separate Files location → fresh-context readback → owner-safe restore. Run only on disposable test data and authorized managed-device configurations.

**Ownership / dependency:** A owns browser OS integration and Worker navigation mechanics; E owns untrusted import, identity, privacy and durability admission; C owns cross-browser and fault-injection oracles; B owns user-mediated share/import/restore UX with Design Studio W121; D owns truthful PWA feature/discovery claims with Marketing D9 HOLD. Engineering owns actual Flutter Web codec and staging tests; device operator owns MDM permissions. **OPEN:** no exact LogMate share-target implementation, managed iPad support, Files recipient custody, or product runtime evidence established by this packet. **CHANGE WATCH:** share-target interoperability, Safari/WebKit OS registration and Permissions Policy, Android install behavior. **VALIDATION:** SH01–SH18 specification only; Stage 8 ACTIVE / Production OPEN / PWA release HOLD.


## 26. Stage 8 — accessible offline custody and recovery are security controls, not cosmetic notifications (2026-11-08)

**Question / novelty:** §§16–25 define data-custody, authentication, share/import and update failure states but do not yet provide a unified *accessible decision-and-recovery admission oracle*. This is a Track C+B evidence bridge for E's destructive-operation gate, not another claim of a LogMate runtime defect.

**SOURCE (W3C primary, checked 2026-11-08):** [WCAG 2.2 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) requires programmatically determinable status changes without moving focus; [WAI-ARIA APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) requires a coherent modal focus sequence and restoration; [APG alert dialog](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/) distinguishes interrupting confirmation from passive status; [WCAG 2.2 new criteria](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) identifies focus-not-obscured (2.4.11 AA). APG examples are implementation guidance, **not** a substitute for product-specific assistive-technology testing. WCAG success criteria are normative; these explanatory/APG documents are informative.

**SYNTHESIS — custody truth before presentation:** An offline logbook has at least six distinct claims: (1) edit accepted in current UI; (2) local transaction committed; (3) local data read back after relaunch; (4) remote owner-authorized ACK; (5) independently saved Files artifact; (6) artifact reopened and restored into a fresh context. Neither a green checkmark, snackbar, progress bar, background task nor an ARIA announcement can promote one claim to another. The accessible name and status text must reflect the *actual evidenced level*; otherwise accessibility can amplify a false safety promise. An offline indicator is not a data-integrity oracle. A modal confirmation is warranted for genuinely destructive owner/deletion/restore decisions; ordinary save/sync progress should not steal focus. When no recovery exists, the interface must not offer a fictional Retry/Restore action.

**Decision/state matrix (provisional product requirements, not observed implementation):**

| Transition | User-facing meaning (example, English product copy subject to Design Studio) | Accessibility and safe-action contract |
| --- | --- | --- |
| Edit committed locally, remote not ACKed | “Saved on this device. Not synced.” | Noninterruptive programmatic status; retain editing focus; no “Backed up” |
| Sync attempt in progress | “Syncing…” | Announce meaningful state changes, not every byte/progress tick; allow continued local use where safe |
| Network/permission denied | “Not synced. Your local changes remain on this device.” **only if verified** | Error summary with Retry only if permitted; preserve user work and focus |
| Account A→B / stale old tab | “This account cannot edit this logbook.” | Deny transaction before mutation; accessible recovery/return path; no leaked A flight details |
| Export API resolves, file not independently read back | “Export started” / “File selected” as actually observed | Never “Backup complete”; guide to independent Files verification |
| Files artifact reopened + fresh-context restore accepted | “Backup restored” **only after committed readback** | Clear result, owner/version details without sensitive log contents; focus to destination |
| SW update ready while unsent edits exist | “Update available. Finish or preserve changes before restarting.” | User-controlled deferral, no surprise modal/refresh; no forced data loss |
| Delete account / clear storage | Explicit irreversible scope, unsynced work, and independently verified backup state | Focus-managed confirmation, distinct cancel/confirm, no auto-confirm; terminal owner fence before destructive operation |

**Failure-mode and contradiction analysis:**
1. A screen reader announces “All synced” after HTTP 200 but before authenticated owner-specific receipt: *false custody assurance*, even if WCAG role/status implementation is technically correct.
2. A “Retry” button triggers duplicate import after an interrupted POST: UI recovery becomes a replay/data-integrity fault. Require operation identity/idempotency and zero-write negative controls.
3. Frequent online/offline oscillation floods live regions and obscures a destructive warning; coalesce repetitive transient updates while preserving materially changed state.
4. An update dialog steals focus during flight entry, then reloads under the old owner: a focus bug can mask a transaction-authorization bug; the latter must be fenced independently.
5. An export/download toast says “Backup complete” without Files readback; neither screen-reader announcement nor share-sheet success proves independent custody.
6. VoiceOver/Safari Home Screen, managed Web Clip, Chromium Android and desktop keyboard differ in focus/announcement behavior. DOM or Flutter semantics-tree inspection is necessary but insufficient for an actual screen-reader PASS.
7. Reflow/zoom, landscape, safe areas, keyboard overlays and sticky action bars can hide focused Cancel/Restore/Delete controls; check 2.4.11 separately from keyboard order and visual contrast.
8. Privacy-safe analytics should count typed transitions/failures, not flight contents, filenames, account identifiers or raw token-bearing URLs. No telemetry event can replace actual restore acceptance.

**TRANSFER VALIDATION — AX01–AX20 (DEFINED, NOT RUN):** AX01 map exact product state transitions and source SHA; AX02 local transaction failure vs success copy; AX03 cold-relaunch readback; AX04 remote ACK lost after commit; AX05 stale A tab during B login; AX06 expired auth while offline; AX07 export initiated but user cancels save; AX08 saved artifact cannot be reopened; AX09 valid independent Files restore; AX10 corrupted/wrong-owner file zero-write; AX11 duplicate import/retry idempotency; AX12 SW update while unsent edit; AX13 forced process kill during modal; AX14 status announcement timing and noninterruptive focus; AX15 repeated connectivity flaps/no live-region spam; AX16 keyboard-only modal trap/return focus; AX17 200% text/reflow/landscape focus visibility; AX18 VoiceOver on actual iPad Safari tab/Home Screen/managed Web Clip (where permitted); AX19 TalkBack/Chromium and desktop screen-reader comparisons; AX20 privacy-safe event trace matched to authoritative ledger state. Each case records *expected state, observed durable store, UI copy, focus/announcement, platform/build, and exact negative-control outcome*. Human/AT testing and Engineering-owned transaction oracles are both necessary; neither alone clears release.

**Ownership:** C owns independent accessibility/quality acceptance; B owns truthful task-state information architecture and recovery copy; E owns authoritative owner/data/deletion admission; A supplies WebKit/Chromium lifecycle and assistive-technology platform differences; D consumes only verified web/Store claims and privacy-safe measurement. Design Studio W121 remains owner of reusable visual/interaction validation; Engineering S007 and LogMate product own actual state machine and tests. Marketing D9 release/claims HOLD is not superseded.

**MINTTAP DECISION / OPEN / CHANGE WATCH:** Treat accessible recovery as a release-safety dependency, not a post-release polish item. No claim of WCAG conformance, screen-reader PASS, actual managed-iPad behavior, backup custody or LogMate defect is established by this document. Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD. Reassess APG/Flutter semantics and WebKit VoiceOver behavior against exact shipped versions before implementing.
## 27. Stage 8 — privacy-safe offline observability and evidence-delivery limits (2026-11-08)

**Question / independent research gap:** §20 distinguishes connectivity hints from sync receipts; §26 governs truthful user-facing custody statuses. Neither makes an application diagnostic beacon, browser policy report or Service Worker callback a durable, received, independently admissible operational proof. This study owns **operational evidence delivery**, not another sync or accessibility primer. **Lead:** E (security/privacy/operations); A supplies browser lifecycle, C test oracles, D privacy-preserving measurement, B recovery messages. **Evidence class:** current platform/standard SOURCE plus architecture SYNTHESIS; **no exact LogMate runtime test**.

### 27.1 HISTORY → standards → browser-platform reality

- **[SOURCE — MDN Beacon API, inspected 2026-11-08](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon):** `navigator.sendBeacon()` asynchronously queues a small POST intended for lifecycle-end diagnostics. Prefer `visibilitychange` when a document becomes hidden over `unload`, which may not fire and can interfere with bfcache. The boolean return means data was **queued for transfer**, not that the origin server accepted it, stored it, or associated it with the correct account/build. `fetch(..., {keepalive:true})` is an alternative with different method/response needs but remains network/lifecycle constrained. **No local offline durability or server-side audit is established by either API.**
- **[SOURCE — MDN ServiceWorkerGlobalScope](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope) and [ExtendableEvent.waitUntil](https://developer.mozilla.org/en-US/docs/Web/API/ExtendableEvent/waitUntil):** an idle Service Worker can be terminated, losing volatile globals. Event-bound `waitUntil()` extends an event's lifetime but cannot be equated with an indefinitely running process or independent disk write. A worker's in-memory diagnostic counter cannot survive a guaranteed kill/restart. Do not promote `sync` event invocation to remote receipt or owner admission.
- **[SOURCE — MDN Background Synchronization](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API) + [Web Features support](https://web-platform-dx.github.io/web-features-explorer/features/background-sync/), inspected 2026-11-08:** Background Sync is **limited availability**; the current compatibility source reports Chromium support and no Safari/iOS Safari support. Chromium retries are constrained. A managed-EFB iPad cannot be assumed to run a deferred diagnostic or flight-data transfer in the background. Exact OS/MDM policy is still **CHANGE WATCH / OPERATOR VALIDATION**, not inferred from the API surface.
- **[SOURCE — W3C Reporting API Working Draft](https://www.w3.org/TR/reporting-1/) / [editor's draft](https://w3c.github.io/reporting/), inspected 2026-11-08:** policy-generated browser reports are **best effort** and may be dropped; the specification expressly does **not** make reporting a reliable communications channel. The draft's capability-URL discussion warns that sensitive URL paths may be exposed despite fragment/credential handling. **Network Error Logging is separately a [W3C Working Draft](https://www.w3.org/TR/network-error-logging/)**; NEL availability, browser implementation, cross-origin/report-to behavior and network-disconnected delivery must be tested, not represented as universal PWA telemetry. Policy reports are about browser/platform conditions, not LogMate's owner-scoped ledger receipts.
- **[SOURCE — MDN StorageManager.estimate](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate) and [storage quotas/eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria):** approximate origin usage/quota does not prove a specific diagnostic record, a complete flight ledger, or a saved Files artifact. IndexedDB logs stored in the same browser origin remain subject to the same container lifecycle and possible loss; `persist()`, if granted, does not constitute an independent backup. Do not report exact free bytes or guaranteed retention from approximate estimates.

**Standards versus deployments:** Beacon and Service Worker lifetime are general Web behavior; Background Sync support is mainly a Chromium-specific extension and not an iPad fallback; Reporting/NEL are draft/implementation-specific; managed iPad policy and app-specific telemetry permission remain independent. This is a **feature/evidence matrix**, not a recommendation to enable all diagnostics.

### 27.2 Six distinct stages of an observable event

| Stage | Permissible claim and evidence | Specifically insufficient |
| --- | --- | --- |
| O0 — state transition inferred | UX or JS observed a candidate event | UI text, `navigator.onLine`, bfcache callback |
| O1 — local diagnostic persisted | Exact scoped record committed/read back in a bounded diagnostic store | In-memory counter, `sendBeacon(true)`, SW global |
| O2 — transport attempted/queued | Redacted request queued or `fetch` attempted | Browser API returned, page hidden |
| O3 — server received/stored | Server-generated receipt with event version, validation and deduplication | HTTP 200 from unrelated endpoint, browser policy report only |
| O4 — exact product authority asserted | Owner/epoch/op-specific authenticated sync or deletion receipt checked by Engineering-owned ledger | Any O1–O3 diagnostic, network state, synthetic browser PASS |
| O5 — independent recoverability demonstrated | New context/device reopens and validates a Files artifact with owner/schema/replica rules | O4 receipt, download/share toast, origin diagnostic log |

**Safety invariant:** no O0–O3 event can authorize an owner-fenced write, mark remote sync complete, declare local owner deletion, or promise backup/restore. Missing reports cannot be inverted into "the user was inactive" or "no failure occurred." A successful report still needs a falsifiable negative control. Duplicate reports and delayed delivery across account A→B must never rebind old-owner data.

**[SYNTHESIS — recommended privacy boundary, NOT a new product telemetry policy]:** If an approved diagnostic channel is later implemented, use an allowlisted event vocabulary such as `shell_verify_failed`, `local_commit_failed`, `remote_ack_ambiguous`, `files_readback_failed`; coarse schema/build/platform classes; short-lived local per-run pseudonymous correlation only when justified. Never emit flight identifiers, airport pairs, crew names, account email/UID, backup contents, auth tokens, raw URLs/query strings, ICE addresses, file paths or retained Sync payloads. Scrub before enqueue **and** again on the receiving endpoint. Bound retention, payload size, event rate, origin, and user/operator permission. Security reports containing full URLs require particular redaction/endpoint scrutiny. On managed EFBs that forbid external telemetry, a privacy-safe user-initiated local support bundle may be evaluated, but it too must have a verified Files custody/consent story and must not be equated with a remote report.

### 27.3 Failure and contradiction matrix

1. **False success:** `sendBeacon` returns `true`, but user disables network, page dies, or server rejects payload. No server receipt; sync and backup statuses unchanged.
2. **False absence:** no beacons arrive while an EFB remains offline for days. Server analytics must not infer zero errors, zero usage or successful synchronization.
3. **SW termination:** an event increments a volatile counter; worker terminates and restarts. Counter vanished while ledger state may be intact. `waitUntil` alone is not durable event storage.
4. **Platform divergence:** synthetic Chrome Background Sync dispatches, Safari/iPadOS lacks that feature. Installed status does not eliminate the gap.
5. **Delayed cross-account upload:** event tagged under A is sent after B signs in; it must not be treated as B's authoritative result or reveal A's data.
6. **Storage pressure:** local diagnostic log and flight ledger share a failure domain; pruning only diagnostics is safe only with strong separation and no interference with ledger/Files.
7. **Stale version:** old tab emits an event under V1 and new SW controls V2; event schema/build identity needs explicit versioning, never blind reinterpretation.
8. **Privacy incident:** automatically generated Reporting/NEL/analytics includes a token-bearing path. Header-level removal of fragments does not guarantee safe path/body content.
9. **Cardinality and abuse:** unbounded per-flight/event payload and retries leak sensitive metadata, inflate cost and prevent useful incident triage.
10. **bfcache duplicate:** `pageshow` reentry emits an apparent second session; metrics require deduplication without treating page lifecycle as ledger truth.
11. **MDM policy:** a managed iPad blocks remote collector or Files export while ordinary Safari permits it; neither behavior generalizes to the other installation mode.
12. **Disaster recovery:** server received a report, but independent Files restore cannot recover the ledger; telemetry success is irrelevant to data-custody PASS.

### 27.4 Falsifiable acceptance packet OB01–OB20 — **DEFINED, NOT RUN**

**Platform and transport (A/C):** OB01 exact NORMAL/acceptance build SHA + served origin, Home Screen/managed Web Clip/container mode; OB02 `sendBeacon` true with server offline and no receipt; OB03 `sendBeacon` false/no queue under payload/queue pressure; OB04 `visibilitychange` hidden vs abrupt app kill/bfcache restore; OB05 `fetch(keepalive)` accepted/failed/ambiguous response; OB06 Worker termination/restart volatile-state loss; OB07 event-bound `waitUntil` interruption; OB08 Safari/iPad unsupported Background Sync versus Chrome capability-detected dispatch; OB09 Reporting/NEL unsupported, disabled, blocked and offline cases; OB10 HTTPS redirect/CSP/Referrer-Policy and collector origin checks.

**Security/custody and measurement (E/C/D):** OB11 exhaustive canary scanner over URL path/query/referrer/body for test email/UID/flight/backup/token/ICE values **before send and after receive**; OB12 A→B and old-tab/version events never relabel owner; OB13 repeated/delayed/duplicated reports idempotent and isolated from ledger; OB14 bounded retention/rate/size/cardinality; OB15 storage pressure and diagnostic purge preserve 37-store ledger and independent Files; OB16 offline/no-report negative control rejects "no incident"; OB17 server-only receipt does not mark UI sync/backup/deletion success; OB18 fresh-context Files restore independently proves custody.

**UX and cross-specialist transfer (B/C/D):** OB19 screen-reader/accessibility state and offline support UX reflects *only* O0–O5 evidenced scope (Design W121/§26); OB20 website/Store/support telemetry and troubleshooting claims audited against Marketing D9 HOLD and actual operator permission. For each test record source SHA, OS/browser build, container/MDM mode, synthetic fixtures, timestamps, expected/actual report & ledger/Files oracle, collector receipt/absence, and failure classification. **No real-user data in fixtures or public logs.**

**Operational judgment / handoff:** The highest-value next proof is **not** a new reporting endpoint: Engineering should expose source-pinned, disposable-data authoritative status transitions and permitted local diagnostic hooks, then jointly test offline kill/restore and owner-fenced Sync/Files independent oracles on actual served PWA and managed iPad. Web Manager can prepare source/standard and acceptance; it cannot consent to telemetry or modify product/MDM infrastructure. A/C produce cross-browser evidence, E approves trust/privacy model, B/Design W121 validates recovery communication, D/Marketing validates public claims. **MINTTAP DECISION (research recommendation, not owner authorization):** operational diagnostics must fail safely and must not be on the critical path of writing flight data. **OPEN:** product log architecture, server collector, permission, actual Safari/MDM behavior, field tests. **CHANGE WATCH:** Reporting/NEL drafts, Background Sync/WebKit capability, retention/privacy regulation and OS background policy. **Gate remains Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

## 28. Stage 8 — WebKit storage policy, ITP inactivity, lifecycle and independent EFB custody (2026-11-08)

**Research question:** Offline EFB pilots may open a PWA after a prolonged interval, under low disk space or after an OS-managed process termination. Is the claim "iPad Safari always deletes data after seven days" true? Can a Home Screen icon or a large quota guarantee the ledger? **Answer: neither.** This reconciles *historical ITP inactivity* and *current quota/eviction* with foreground resume and independent Files custody. E owns trust/release, A owns WebKit/browser behavior, C falsification, B recovery UX, D accurate product claims. **Evidence: SOURCE + SYNTHESIS; no new product/device execution.**

### 28.1 History and source precedence

1. **[SOURCE — WebKit, 2020, historical policy](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/):** WebKit described a seven-day *Safari-use without site interaction* limit for script-writable storage, including IndexedDB and service-worker/cache state. The same source expressly differentiated Home Screen web applications: they have a separate use counter, and the WebKit team did not expect first-party Home Screen app data to be deleted under that inactivity mechanism. **It does not say that all iPad PWAs lose data every seven calendar days**, nor that Home Screen data is immune to all deletion. This is historical policy evidence, not a measured current managed-iPad retention SLA.
2. **[SOURCE — WebKit, 2023 storage-policy update](https://webkit.org/blog/14403/updates-to-storage-policy/):** Safari 17/iPadOS 17 browser origin quota is **up to 60%** of total disk and browser overall quota **up to 80%**; other WebKit apps have lower nominal origin/overall percentages. Standalone Home Screen web apps receive the browser-app quota class. Eviction may occur on overall storage pressure, low disk space or inactivity, normally by origin; persistent storage is a separate protection class. **"Up to" is a policy ceiling, not an allocation, a byte-exact guarantee or independent backup.** WebKit explicitly distinguishes browser-app and other-app quota classes; a managed Web Clip's exact container/quota class must be measured, not inferred from its icon.
3. **[SOURCE — WebKit, 2023 Safari 17](https://webkit.org/blog/14445/webkit-features-in-safari-17-0/):** Storage API and `StorageManager.estimate()` became available in Safari 17, and WebKit reports eviction exemption for an origin in persistent storage mode. **Persistent origin storage does not guarantee device survival, user non-deletion, owner-fenced data semantics, MDM exemption or independent Files artifact.** Reconfirm `persisted()` and `persist()` result per real runtime.
4. **[SOURCE — MDN pagehide](https://developer.mozilla.org/en-US/docs/Web/API/Window/pagehide_event) / [pageshow](https://developer.mozilla.org/en-US/docs/Web/API/Window/pageshow_event) / [Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API):** `pagehide` is bfcache-compatible but may never fire on mobile app-switch→OS kill; `pageshow` can represent a bfcache restore or background/prerendered page, **not necessarily actual user-visible foreground**. `visibilitychange` reflects document visibility but not a durable ledger commit. None is an exclusive last-chance backup hook. **Application safety must be transaction-first, not page-exit-first.**
5. **[SOURCE — MDN Service Worker lifecycle](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers):** installed, waiting, activated and client-controlled are distinct; a registered worker, cache entry or Home Screen installation is not proof of complete offline shell nor current client control. **Worker/cached shell readiness is not flight-data custody.**

**Version-sensitive correction:** Do not mechanically apply the 2020 ITP seven-day description to all Safari 17+ or iPadOS 26 contexts. The current platform's ITP policy, managed configuration and actual retention need fresh vendor/operator verification. Equally, the 2023 quota figures do not establish that a 2026 managed device has unlimited durability. Distinguish Safari tab, Home Screen standalone, MDM Web Clip, third-party WKWebView, different origins, and changed install identity as separate test populations.

### 28.2 Five independent survival claims and recovery transitions

| Claim | Proof required | Invalid shortcut |
| --- | --- | --- |
| S1 shell launch | Cold offline launch, correct served/installed build, navigation and SW control after restart | Home Screen icon, cached HTML alone |
| S2 origin ledger | Transaction commit, readback after kill/relaunch, schema and owner epoch | `StorageManager.estimate()`, `persisted()`, successful screen render |
| S3 owner authority | Current identity, deletion epoch, stale-tab/old-owner rejection, remote ACK where needed | Auth session persistence, network connected, S2 alone |
| S4 independent artifact | User-authorized Files export, independent byte/hash/schema readback, fresh-context restore | Share/download initiated, OPFS or IDB copy, persistent-origin grant |
| S5 device/operator durability | Same tests on allowed managed iPad modes, storage pressure, OS restart, policy-controlled removal and time-separated observation | Safari desktop, simulator, Home Screen assumption, historical ITP blog |

**Architecture consequence [SYNTHESIS]:** For unsynced flight entries, the application should persist at each approved transaction boundary and validate local readback. Treat visibility changes as *opportunities* for best-effort diagnostics/UX, not data-saving triggers. On foreground/cold restart, revalidate ledger integrity, owner fence, outbox and current build before announcing sync or backup. A detected origin reset must enter explicit recovery/no-write handling, not silently initialize an empty account as though all prior flights were zero. If an independent Files backup exists, verify its identity/schema and restore into a fresh context under Engineering-owned rules. If none exists, do not offer a fictional restore or imply recoverability.

**Contradictions / negative cases:**
- ITP seven-day cap quoted as a universal timer → contradicted by WebKit's separate Home Screen exception; exact managed device still unknown.
- `persisted() === true` → not a Files backup, not protection against deliberate clearing or device loss.
- Large quota estimate → does not establish committed transaction or origin survival under OS pressure.
- `pagehide` or `unload` callback → absent on mobile kill; must not be the only save path.
- `pageshow` after bfcache → may carry stale owner/build state; require independent authorization and ledger refresh.
- Offline shell still loads after IDB deletion → visual success conceals missing ledger.
- Origin-level eviction or Clear-Site-Data → may destroy shell and ledger together; an in-origin diagnostic or OPFS copy shares risk.
- Managed Web Clip icon looks like Home Screen → does not prove equivalent quota, persistence, container or MDM policy.
- OS reinstall/MDM wipe/account A→B → different destructive/authorization boundaries, not ordinary cache eviction.
- Browser storage survives 30 days in one synthetic run → cannot prove future retention or device-wide policy.

### 28.3 Falsifiable validation campaign STG01–STG24 — **DEFINED, NOT RUN**

**Browser/runtime matrix (A/C):** STG01 record exact product source/build/served origin, iPadOS/WebKit version, device class, MDM mode; STG02 Safari tab cold offline shell; STG03 Home Screen standalone cold offline shell; STG04 managed Web Clip (only if operator-approved); STG05 `navigator.storage.estimate()` approximate usage/quota with privacy-safe logging; STG06 `persisted()` before/after `persist()` and actual grant/denial; STG07 worker active/waiting/controller vs shell build identity; STG08 explicit IDB transaction/readback before abrupt process kill; STG09 app-switch→OS kill with no `pagehide`; STG10 bfcache `pageshow.persisted` and old owner; STG11 visible/hidden flapping with outbox pending; STG12 cold relaunch after browser/OS restart.

**Data-custody and negative controls (E/C):** STG13 low-disk/overall-quota pressure using **disposable test data only** (no forced destructive tests on crew EFB); STG14 explicit origin data clearing in disposable container; STG15 installed icon/shell survives while ledger missing; STG16 new origin/install identity produces distinct store; STG17 account A→B old tab and epoch rejection; STG18 remote ACK ambiguous/expired auth while offline; STG19 Files export byte/hash/schema readback independent of browser; STG20 fresh-context restore and wrong-owner/corrupt/duplicate zero-write; STG21 time-separated inactivity trial with documented Safari-use/interaction counters, no assumption of universal seven-day deletion; STG22 managed MDM policy/removal test only with operator permission.

**Cross-track product acceptance (B/D/C):** STG23 accessible status and recovery copy explicitly distinguishes "saved here", "not synced", "backup verified", "cannot recover"; STG24 public website/Store/PWA reliability claims audited against observed modes, no "permanent offline storage" or "automatic backup" without evidence. Each case requires exact source/served SHA, browser/OS/MDM mode, fixture IDs, before/after local ledger and Files hashes, owner epoch, negative control, and actual pass/fail/non-execution classification.

**MINTTAP DECISION (research recommendation, not approved product implementation):** Prioritize **independent, verified Files custody plus foreground readback/recovery** over assumptions about storage quota, seven-day timers or background lifecycle hooks. Treat managed EFB deployment policy as a first-class release input. **DEPENDENCY:** Engineering owns exact Sembast Web transaction, migration, owner/restore tests; MDM operator owns physical device/policy permission; Design Studio W121 owns truthful accessible recovery states; Marketing D9 holds unsupported offline claims. **OPEN:** current iPadOS/MDM Web Clip behavior, exact LogMate runtime, Files destination/restore and long-duration device observation. **CHANGE WATCH:** future WebKit ITP/Storage API/quota updates, OS eviction and MDM deployment. **Stage 8 ACTIVE / production OPEN / PWA release HOLD.**

## 29. Stage 8 — public discovery, crawler rendering and private offline PWA trust boundary (2026-11-08)

**Research question / independent value:** The previous E/A/C studies establish shell, storage, owner and Files custody. They do not establish whether a public MintTap app/support page is discoverable, whether an authenticated PWA route can leak private information to a crawler, or whether an offline navigation fallback can accidentally turn a missing public page into an indexable HTTP 200. This is **Track D ownership** (discovery and truthful measurement) with A navigation/rendering, E privacy/hosting, B information architecture and C test transfer. Generic 12-stage D competency is PASS; exact public served evidence remains OPEN. **Classification:** Google Search Central SOURCE (retrieved 2026-11-08) + SYNTHESIS/conditional MINTTAP DIRECTION; no live website or product execution.

### 29.1 History/problem → primary platform evidence

1. **[SOURCE — Google Search Central, How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works):** discovery, crawling, rendering, indexing and serving are distinct. Google may run JavaScript with its rendering service, but inclusion in the index and ranking are not guaranteed. An installed PWA icon, Web App Manifest, service-worker registration or a Lighthouse PWA check proves none of those steps.
2. **[SOURCE — Google Search Central, Fix Search-related JavaScript problems](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript):** Googlebot rendering does not retain Local Storage, Session Storage or HTTP cookies across page loads; crawlers cannot be assumed to supply user permissions, WebRTC/WebSocket content or a prior authenticated/installed PWA session. It documents SPA **soft-404** risk when an error or missing route returns HTTP 200, and advises testing with Search Console URL Inspection / Rich Results Test. Rendering service may omit nonessential analytics requests, so client analytics alone cannot count crawler activity. Fingerprinted asset filenames mitigate stale crawler JS/CSS caching.
3. **[SOURCE — Google Search Central, JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics):** app-shell-only HTML requires successful JS rendering to expose content; server-side rendering or prerendering can improve access and performance, and not every bot executes JavaScript. Crawlable links and real text are necessary for public resources. **No inference:** Flutter Web PWA UI is not automatically an adequate marketing-site renderer.
4. **[SOURCE — Google Search Central, canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls):** server redirects, `rel="canonical"` and sitemap entries are different-strength *signals*, not commands. Self-referential absolute HTTPS canonical links are recommended; sitemap is weaker; robots.txt is not a canonical or confidential-content protection mechanism. Conflicting HTTP header/HTML/JS canonical signals can undermine intended URL selection.
5. **[SOURCE — Google Search Central, developer SEO guidance](https://developers.google.com/search/docs/fundamentals/get-started-developers):** robots.txt controls crawling, not secrecy or guaranteed deindexing. Use authentication for private resources and appropriate `noindex` for public-but-not-indexable pages where crawler access is permitted. Public semantic text, descriptive titles and links matter; a canvas-only view may be inaccessible to textual indexing.
6. **[DEPENDENCY — earlier sections §§12–14, 20–28 of this PWA Master]:** a service-worker navigation fallback, hosted rewrite, canonical origin, authentication redirect and cached shell can produce *different representations* for the same URL. This is an architecture inference to test, **not an observed defect**.

### 29.2 Trust and routing matrix — public SEO must not weaken private ledger

| URL class (proposed) | Intended crawler result | Security/hosting and PWA invariant |
| --- | --- | --- |
| Company homepage and public app listing | Indexable, server-accessible meaningful HTML and canonical HTTPS URL | No login dependency, private app bootstrap or opaque offline shell substitution; claims source-pinned to actual released products |
| Public app details/support/privacy/deletion instructions | Independently reachable canonical public pages, valid title, text and links | Correct status for absent page; content version and Store/legal parity; no personal identifiers in HTML, structured data or URLs |
| Sign-in/verification/reset/callback | Authentication function, **not** a public acquisition landing page | No private tokens or OAuth codes in canonical/sitemap/analytics; avoid caching sensitive responses; test redirect and `noindex` policy without treating it as access control |
| Authenticated logbook/editor/backup/sync | No unauthenticated ledger content; authorization required for each data request | Server and app enforce identity/owner/epoch, regardless of crawler, robots, JS or cached shell; public discovery must not expose private data |
| Missing/retired public route | True HTTP 404/410 where appropriate, or justified permanent redirect | A generic SPA/Service Worker HTML 200 fallback must not create a soft-404 or duplicate canonical page |
| Offline installed-PWA navigation | Offline shell or truthful offline status **for a controlled authorized client** | Offline fallback does not replace public origin server semantics, override owner admission, or claim remote data available |
| Staging/preview/old host/alternate origin | Not an approved production canonical | Protect by access controls; prevent sitemap/canonical/redirect leaks and avoid relying on robots alone |

**SYNTHESIS — important distinction:** The public website and the authenticated PWA may share an organization and brand, but need not share a single app-shell deployment. If they share an origin, path-specific hosting precedence, Service Worker scope and cache rules require explicit adversarial tests. A crawler's unauthenticated view is not a production authenticated user view; neither can prove the other. Likewise a `noindex` response is not a security boundary. An app manifest `start_url` is an installation entry, not an SEO canonical declaration or proof that the URL is public. The offline fallback must not be served as an authoritative page for arbitrary 404/401/403 or token-bearing auth routes.

### 29.3 Cross-track failure analysis and design trade-offs

- **D/A:** Client-only marketing content may render for a logged-in human but be absent from a fresh crawler context. Mitigation candidate: public semantic HTML/prerendered pages independent of authenticated PWA state; verify exact HTTP and rendered DOM, not framework ideology.
- **A/E:** A catch-all rewrite to `index.html` can turn nonexistent public support URLs into 200 soft-404s, or accidentally capture an auth action endpoint. Precedence and response-class tests are mandatory; existing §12 and §14 are prerequisites, not duplicated.
- **E/D:** Private backup or flight route placed in a sitemap or structured data leaks metadata; robots.txt does not revoke a previously public URL or authenticate requests. Owner-scoped data must be unavailable to unauthenticated fetch and cached-public shell.
- **D/B:** Website, app-store, installed PWA and support pages may promise different sync/backup modes. The canonical Product Truth Record and Marketing D1/D9 claims gate must govern public copy; marketing copy must not promote untested physical-EFB capabilities.
- **D/C:** A green Lighthouse SEO audit or synthetic crawler render cannot prove actual Google indexing, human accessibility, field CWV or app installability. Distinguish test scope and use Search Console operator evidence only if authorized.
- **A/D:** Versioned JS/assets and stale service-worker caches can cause crawler and human to see different content. Googlebot's JS resource caching can be independent of a user's CacheStorage. Compare source HTML, HTTP headers, JS-rendered DOM and actual controlled-client output.
- **D/E:** Canonical/redirect changes during domain migration may inadvertently expose an old authenticated route or split public SEO signals; origin changes can also strand private browser storage. SEO redirects are not a storage migration plan (§14/§28).
- **D/privacy:** Analytics requests may be skipped by crawler rendering, blocked by privacy tools or absent offline; zero events cannot prove zero crawls or usage. §27's event/receipt evidence boundary applies to SEO attribution as well.

### 29.4 Falsifiable discovery/privacy acceptance packet DC01–DC24 — **DEFINED, NOT RUN**

**Public rendering and canonical (D/A/C):** DC01 record actual approved `minttap.app` hosting release SHA, canonical domain and response routes; DC02 fetch fresh no-JS homepage HTML and visible title/text; DC03 render same page with clean JS context and compare; DC04 app listing/details/support/privacy/deletion pages without session; DC05 HTML/HTTP canonical consistency and absolute HTTPS targets; DC06 sitemap/robots references and no private URLs; DC07 public nonexistent route returns appropriate 404/410 rather than soft-404 200; DC08 retired/alternate host redirect chain and canonical parity; DC09 fingerprinted assets and stale resource control; DC10 verify crawlable anchor links rather than click-only handlers.

**Security/route adversaries (E/A/C):** DC11 unauthenticated direct deep link to private ledger, no sensitive HTML/API data; DC12 private URL never enters sitemap/structured data/metadata; DC13 auth reset/callback query-token canary absent from canonical, referrer, analytics and cached shell; DC14 server rewrite precedence for auth endpoints, 401/403/404, Worker fetch and offline fallback; DC15 old controlled tab vs fresh crawler without SW and after deployment; DC16 wrong-origin/staging/preview canonical leak negative controls; DC17 owner A→B stale tab cannot expose A in rendered shell, public cache or search metadata; DC18 offline page shows truthful limitations, not remote success.

**UX, quality and external evidence (B/C/D):** DC19 accessible semantic public content, keyboard and screen reader scope handed to Design W121; DC20 app/Store/web/support content truth against actual version and Marketing D1/D9 HOLD; DC21 optional Search Console URL Inspection / indexing evidence with operator permission, not simulated ranking; DC22 compare Search Console crawl stats against telemetry limitations, never assume exact parity; DC23 device responsive and slow-network performance without claiming field Core Web Vitals from lab; DC24 product/private route privacy canary and explicit negative control on release rollback and canonical migration. Record requested URL, status/redirect chain, source HTML, rendered DOM, robots/canonical, served SHA, browser/crawler mode, auth state, SW controller, exact canary expected/observed and classification (PASS/FAIL/NON-EXECUTION/OPEN). **Use synthetic test accounts/data only.**

### 29.5 Operational judgment and handoff

**MINTTAP DIRECTION — proposed, not owner-approved deployment:** separate **public discoverability contract** (semantic HTML, canonical URLs, truthful support/Store information, valid status codes) from **private offline application contract** (authenticated owner authority, durable local ledger, independent Files restore, controlled SW scope). Do not implement crawler-specific deceptive content; render the same public claims to users and crawlers, with implementation fallback only. Prefer one clear canonical host and route policy, then validate the exact deployed responses before Search Console submission. **DEPENDENCY:** Web Manager D owns reusable crawl/index and canonical research; A owns SW/navigation mechanics; E owns hosting/security; B owns IA/content; C owns independent testing; Design W121 owns visual/accessibility execution; Marketing owns actual public claims; Engineering and product own private runtime; domain/hosting operator owns served evidence. **OPEN:** live host, exact deployment configuration, robots/sitemap, real Search Console, public page HTML, physical iPad, production authentication. **CHANGE WATCH:** Google Search rendering/indexing guidance, hosting route precedence, WebKit/Chromium SW lifecycle and app-domain migrations. **Release gate unchanged: Stage 8 ACTIVE / production OPEN / PWA HOLD.**

## 30. Stage 8 — partitioned browser state, federated sign-in and owner-safe PWA admission (2026-11-08)

**Novel boundary / HISTORY:** Traditional third-party cookies allowed cross-site tracking; modern browsers restrict or partition third-party state. The security improvement can break legacy iframe-based single sign-on, but neither granting cookie access nor successfully returning from OAuth establishes authorization to mutate an offline pilot logbook. Earlier §21 covered auth persistence versus owner authority and §23 covered COOP/COEP popup mechanics; this section specifically owns **partitioned versus unpartitioned browser identity state and embed permissions**. Track A owns browser primitives; E owns trust/CSRF/owner fencing; C owns negative controls; B owns explicit sign-in/recovery UX; D owns privacy and truthful support claims.

### 30.1 SOURCE — dated browser/platform evidence (checked 2026-11-08)

- [MDN Storage Access API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API): HTTPS-only third-party embedded content may request access to unpartitioned cookies when blocked; permission activation is context-sensitive and browser semantics differ. Access is not a universal iframe SSO guarantee, and access to a cookie is not proof of a valid current owner.
- [WebKit Storage Access API updates](https://webkit.org/blog/11545/updates-to-the-storage-access-api/): Safari's earlier model requires prior first-party interaction and cookies for third-party storage access. This is dated historical vendor evidence, **not** a blanket statement of all 2026 Safari/iPadOS versions or managed-device policy.
- [MDN CHIPS / Partitioned cookies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Third-party_cookies/Partitioned_cookies): `Partitioned` with `Secure` opts a cookie into a top-level-site keyed jar; a typical cross-site embedded cookie additionally needs `SameSite=None`. CHIPS provides scoped embed continuity, **not** a shared login session across unrelated sites. MDN currently labels CHIPS Baseline 2025, but old Safari/managed OS builds and specific auth libraries require independent checks.
- [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie): `SameSite=Lax` generally limits cross-site subrequests while permitting qualifying top-level safe navigation; `SameSite=None` requires `Secure`; `HttpOnly` prevents ordinary JS cookie reads but does not prevent a browser from attaching cookies to requests. Explicit cookie attributes do not replace CSRF, state/nonce, PKCE or server-side session checks.
- **DEPENDENCY:** OAuth/OIDC redirect versus popup and Firebase provider behavior must be validated against the **exact** product auth adapter, IdP, allowed redirect origin, browser version and deployment configuration. No assumption that WebKit Home Screen, managed Web Clip and Safari tab share cookies, local IndexedDB or an identical sign-in surface.

### 30.2 Independent authority matrix

| State | What it can prove | What it cannot prove |
| --- | --- | --- |
| Top-level first-party IdP cookie | Session exists in that IdP's browser context | App owner identity, embedded access, PWA local ledger authority |
| Embedded partitioned cookie | Embed may retain site-scoped state under one top-level site | Cross-top-level SSO or another device's session |
| Storage Access API granted | Specific third-party context may access unpartitioned state per browser policy | Universal future permission, offline authentication or owner write rights |
| OAuth redirect/popup returned | Browser navigation returned to a callback route | State/nonce/PKCE checked, Firebase token verified, local owner bound |
| Server token validated | Identity claim valid for intended audience/issuer/time | Unsent local flight ownership or restored replica provenance |
| Owner/epoch fenced local transaction | Current owner and deletion epoch admitted exact write | Remote ACK or independent Files backup |
| Owner-specific remote receipt | Remote operation accepted under matching authority | Independent recovery from device loss |

**SYNTHESIS:** Account A signing out and B signing in while A's PWA tab/Worker/IDB transaction remains open is a high-severity **cross-context owner-fence** test even if all cookies are perfectly configured. A cookie partition or Storage Access grant is not a database isolation primitive. A callback must not be cached as a successful offline shell, and neither a shared device session nor an IdP account chooser can silently adopt an unverified local ledger. This complements §21/§23/§29 rather than reopening those primers.

### 30.3 Failure analysis and operational choices

1. Embedded IdP frame denied third-party state: sign-in may fail or require top-level navigation; never present an automatic retry loop that writes flight data.
2. Storage Access permission granted in one iframe but absent in another or after Home Screen relaunch: **auth continuity differs from ledger continuity**.
3. Partitioned cookie established under `minttap.app` then page served from a different canonical top-level site: the partition key changes, so apparent logout does not imply data deletion or remote revocation.
4. OAuth callback opened under a different origin/installation container: redirect can complete yet local replica identity may be inaccessible. Recovery must be explicit and owner-verified.
5. `SameSite=None; Secure` on an auth cookie does not make a cross-site request CSRF-safe; validate state/nonce/PKCE and backend anti-CSRF controls separately.
6. Cookie blocked or expired while device offline: cached UI and IndexedDB may remain available; display limited offline ownership status rather than claiming live reauthentication.
7. A→B transition after popup success while old tab resumes from bfcache: reject old owner writes before mutation, not merely after a BroadcastChannel notification.
8. IdP popup blocked by managed iPad policy: alternate approved full-page flow requires callback-route, app-state and pending-write preservation.
9. Cookie policy differs across WebKit, Chromium and managed Web Clip; a Chrome synthetic PASS does not promote iPad support.
10. Analytics and support screenshots must not expose auth callback codes, tokens, session identifiers or account details; `noindex` does not prevent leaks in logs.

**MINTTAP DIRECTION — proposed, not approved:** Prefer a first-party application boundary and an explicit standards-compliant top-level federated sign-in path over depending on invisible third-party iframe cookies. Evaluate actual provider SDK behavior before choosing redirect/popup. Keep offline ledger read/write admission separate from cookie/IdP session state; do not silently merge owners. Do not change cookie policy, IdP configuration, PWA scope, hosting or account behavior from this research alone.

### 30.4 PA01–PA24 acceptance matrix — DEFINED, NOT RUN

**Browser and IdP (A/E/C):** PA01 exact product SHA/served origin/IdP SDK; PA02 same-site versus cross-site cookie baseline; PA03 `Lax` callback navigation versus POST; PA04 `None;Secure` and HTTPS; PA05 `HttpOnly` JS negative control; PA06 CHIPS top-level site A/B partition isolation; PA07 unsupported/older-browser `Partitioned` fallback; PA08 embedded Storage Access denied; PA09 granted access in same iframe; PA10 new iframe/new tab permission activation; PA11 Safari first-party interaction prerequisite; PA12 managed Safari tab/Home Screen/Web Clip parity; PA13 redirect versus popup and popup-blocked alternative; PA14 callback state/nonce/PKCE invalid/replay negative controls.

**Owner and recovery (E/C/B):** PA15 token audience/issuer/expiry and revoked session; PA16 offline token expiration with retained ledger; PA17 A→B stale tab/bfcache/Worker owner fence; PA18 callback cache and SW navigation fallback cannot expose token; PA19 origin migration and new replica binding; PA20 failed sign-in preserves local unsent edits without cross-owner disclosure; PA21 duplicate callback/idempotent remote operation; PA22 no unauthorized write on wrong owner, stale epoch or revoked session.

**Privacy and public claims (D/C):** PA23 redacted URL/referrer/analytics/diagnostic canary check; PA24 user-facing auth/offline/restore copy and screen-reader focus against Design W121, Marketing claims and actual runtime. Every case must record source/served SHA, OS/browser/container, IdP configuration, synthetic account IDs, expected and observed cookies/requests, owner/ledger negative controls, and PASS/FAIL/NON-EXECUTION. **No actual managed-device or product test was executed here.**

**OPEN / CHANGE WATCH / handoff:** Engineering must inspect exact Flutter Web/Firebase auth adapter and local owner-fence source, hosting must provide redirect/callback configuration, MDM operator must authorize real iPad mode testing, Design W121 must validate failure/recovery interactions, Marketing must avoid unverified "automatic sign-in/sync" promises. Recheck MDN/WebKit compatibility against deployed versions. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

## 31. Stage 8 — installed PWA identity, multiple containers and safe origin/path migration (2026-11-08)

**Novel boundary:** §14 covers routing and §30 covers cookie/owner admission, but neither gives a unified *installed-instance inventory and migration* contract. The install identity, browser/OS storage container, URL origin, manifest navigation scope, Service Worker scope, authenticated owner/epoch, and LogMate replica ID are **seven different identities**. This is Track A/E owned, with B/C/D transfer. **Evidence: SOURCE + SYNTHESIS; NOT actual product/device execution.** Previous §28 storage-eviction and §29 public SEO routing remain controlling.

### 31.1 Primary sources, date and platform distinction

- **[SOURCE — Web App Manifest id, MDN, inspected 2026-11-08](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/id):** `id` identifies the *installed application* to a supporting browser, not the signed-in account, storage partition, device, or LogMate replica. It is same-origin with `start_url`, resolves as a URL, ignores fragments, and defaults to `start_url` if absent/invalid. Changing `id` can make a new install identity. A stable `id` across a changed `start_url` can allow a manifest update **where supported**, but it does not move IndexedDB bytes or grant owner access. MDN marks `id` limited availability; exact browser behavior remains CHANGE WATCH.
- **[SOURCE — Manifest scope and start_url, MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/scope), [start_url](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/start_url):** `scope` is installed *navigation context*, not a security boundary; path-prefix matching means `/app` may also match `/apple`, while `/app/` avoids that ambiguity. Invalid/missing scope falls back based on effective `start_url`. `start_url` is advisory and same-origin restricted; the user agent may override it. None of these settings replaces server authorization, Worker scope or HTTP route protections.
- **[SOURCE — web.dev PWA updates](https://web.dev/learn/pwa/update):** metadata update timing and app replacement vary by browser/OS; changing `id` is a new PWA identity. The page's iOS/iPadOS reinstall guidance must be retested against current platform versions, not elevated to a universal perpetual rule.
- **[SOURCE — WebKit iOS/iPadOS 16.4 Web Push and Manifest ID](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/):** iOS supports multiple installs of the same web app; iOS/iPadOS 16.4 combine user-selected Home Screen name and Manifest ID to distinguish installations, including Focus settings. The post explicitly notes a **Shared iPad** restriction for third-party browser Add to Home Screen; a company-managed EFB may have additional MDM restrictions. Neither Manifest ID nor Home Screen name is a LogMate owner/replica credential.
- **[SOURCE — WebKit Safari 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/):** creating a Home Screen web app copies browser cookies, including login cookies, at creation time (iOS/iPadOS 17.2); **no other local storage is copied** and subsequent website data is not shared. This is a one-time copy, not ongoing synchronization or authorization.
- **[SOURCE — WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/):** standalone Home Screen apps have browser-app-level origin/overall quotas but remain subject to storage pressure/eviction; quota parity is not a persistence SLA. Do not infer that an installed icon guarantees a retained flight ledger.

### 31.2 Identity and migration decision matrix (SYNTHESIS)

| Identity/authority | Example mutation | What can change | What must NOT be inferred |
| --- | --- | --- | --- |
| Manifest `id` | `/logmate` → `/logmate-v2` | Installed-app identity; possibly duplicate icon | Existing data migrated, owner/replica continuity |
| `start_url` | `/app/` → `/pilot/` | Launch entry; app metadata update timing | Old Worker no longer controls old tabs |
| Manifest `scope` | `/app/` → `/` | Installed navigation context | Auth/secret-route protection |
| Worker registration/scope | `/app/sw.js` → `/sw.js` | Fetch control and cached shell generations | IndexedDB schema and unsent edits safe |
| Origin | `old.example` → `new.example` | Same-origin storage/credentials boundary | Browser automatically moves local ledger |
| Container | Safari tab → Home Screen A/B or managed Web Clip | Independent cookies/storage/install lifecycle | One installed icon = one device owner |
| Owner + replica + epoch | Account A→B, restore, reinstall | Authority to read/write/sync and duplicate detection | Same manifest id means same user or safe replica |

**Counterexample 1 — multiple installs:** On one iPad, Home Screen “LogMate Work” and “LogMate Backup” may be separate installed instances with distinct local stores. A naive sync engine treating manifest ID or origin as unique replica identity can silently collide or overwrite. Even if actual WebKit container separation varies by version, the safety design must reject implicit replica equivalence until device evidence is obtained.

**Counterexample 2 — origin migration:** A website redirects to a new domain and the installed app launches there, but old IndexedDB, cached Worker and Files backup remain at independent boundaries. A redirect, DNS alias, stable-looking app icon or shared account session cannot transfer origin-private storage. The only acceptable migration is an owner-authorized, integrity-checked, idempotent export/transfer/restore protocol with a rollback path and independent Files custody; feasibility depends on actual product implementation and policy.

**Counterexample 3 — authentication:** Cookies may be copied into a new Home Screen container at creation, but IndexedDB is not copied. A user can appear logged in while their old local flight history is absent; UI must not call this a deletion, successful migration or synchronized empty logbook. Conversely a logged-out container can still contain owner-bound local data. The source-of-truth is the actual durable owner/replica/epoch admission.

**Counterexample 4 — accidental app split:** A deploy changes `id` or omits it while altering `start_url`; a browser may create another installed app. Both may carry independent unsent edits. Treat both as distinct until explicit ledger reconciliation; never erase the old installation as a “duplicate” merely because the icons match.

### 31.3 Deployment, security and recovery contract (MINTTAP DIRECTION — proposal, NOT approved)

1. Freeze a version-controlled **manifest identity tuple** (`id`, `start_url`, `scope`, `display`, icon/name) per supported channel, and separately record Worker script URL/scope, origin, served release SHA and managed-device install mode. Do not place user/flight/account identifiers or auth tokens in `id` or `start_url`.
2. Prefer stable manifest `id` and explicit trailing-slash `scope` within one origin. Avoid expanding Worker or manifest scope to public support/OAuth routes without independent security and SEO route tests (§14/§29).
3. Before a manifest/Worker/origin migration, inventory actual installed instances, unsent edits, owner/replica identities, current external Files backup and rollback capability. A device operator must approve any managed EFB install/reinstall.
4. Never use a manifest field, Home Screen name, cookie or platform installation ID as a cryptographic owner or replica credential. Require explicit owner+epoch+operation admission and durable post-restart readback.
5. During migration, maintain an old-build read-only or safe-export path until the new context verifies owner-scoped import, deduplication, restore and independent Files readback. Do not promise automatic cross-origin transfer, background sync or a stable icon on iPad.
6. Public marketing and support must say only what has been verified on each Safari/Home Screen/Web Clip/Chromium build; Design W121 owns accessible re-install/restore messaging and Marketing owns claims.

### 31.4 IM01–IM24 falsifiable acceptance — **DEFINED, NOT RUN**

**Identity and routing (A/E/C):** IM01 exact served manifest/response SHA; IM02 resolved `id` absent/valid/invalid; IM03 same `id`, changed `start_url`; IM04 changed `id`, same launch; IM05 `scope=/app` vs `/app/` prefix trap; IM06 manifest/Worker scopes diverge; IM07 old/new Worker controlled tabs and cached shell; IM08 HTTP redirect/rewrites to private/public/OAuth routes; IM09 version-specific metadata update versus reinstall; IM10 installed shortcut/deep link after route change.

**Container, storage, owner (E/A/C):** IM11 Safari tab versus Home Screen cookie one-time copy; IM12 IndexedDB/Cache Storage no-copy and cold-relaunch readback; IM13 two same-origin Home Screen installs, distinguish storage and replica; IM14 same icon/name but different owner/replica; IM15 old/new origin local-data separation; IM16 offline migration attempt zero-write and safe recovery; IM17 A→B stale tab owner fence; IM18 restore duplicate replica/operation rejection; IM19 manifest update with unsent edits and killed process; IM20 managed Web Clip/Shared iPad/MDM restriction matrix with operator approval.

**UX, privacy and proof (B/C/D):** IM21 no token/UID/flight ID in manifest URL/start URL/log/referrer; IM22 200% zoom/VoiceOver and keyboard focus during install/reinstall/restore; IM23 verified Files artifact reopens in new context with owner/schema/hash and no unauthorized writes; IM24 public installation/backup/sync claims matched to observed device behavior and release SHA. For every case record exact OS/browser, installation/container mode, origin, manifest+Worker response, owner/replica/epoch, durable ledger before/after, external Files artifact, expected/actual negative control and PASS/FAIL/NON-EXECUTION. **No actual LogMate, served production, or managed iPad test has been run by this research.**

**TRANSFER / DEPENDENCY / CHANGE WATCH:** A owns manifest/WebKit mechanics; E owns owner/replica trust and migration rollback; C owns independently falsifiable multi-container/device oracles; B/Design W121 owns truthful restore/install messaging; D/Marketing owns public installation claims. Engineering must inspect exact Flutter Web manifest, generated Worker and local DB/Sync adapter; operator must provide approved physical EFB configuration. WebKit Home Screen semantics, iPadOS/MDM policies and browser metadata update behavior are version-sensitive. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

## 32. Stage 8 — PWA launch and external-intent routing are not owner-authorized navigation (2026-11-08)

**HISTORY / PROBLEM:** A website link traditionally navigates a browser tab. An installed PWA can additionally be opened by an OS shortcut, launch target, protocol handler or file/share association, possibly reusing a live window. Reuse and deep-link convenience create a **cross-context input boundary**: an external URL or launch event is an untrusted request, not authorization to select a LogMate ledger, restore a backup, change owner, or accept an import. This integrates §14 route/scope, §25 share ingress, §29 public/private separation, §30 partitioned authentication and §31 installed-container identity. It does not restate those studies. **Lead E trust and A browser mechanics; B navigation/recovery; C falsification; D public link/discovery claims.**

### 32.1 SOURCE — browser and standards boundary (checked 2026-11-08)

1. [MDN Launch Handler API](https://developer.mozilla.org/en-US/docs/Web/API/Launch_Handler_API) and [Window.launchQueue](https://developer.mozilla.org/en-US/docs/Web/API/Window/launchQueue): the manifest's experimental `launch_handler.client_mode` can request `auto`, `focus-existing`, `navigate-existing` or `navigate-new`; `window.launchQueue.setConsumer` may receive `LaunchParams.targetURL`. The API is **limited availability, not Baseline**. An app must not assume `focus-existing` preserves its current route, nor assume a queued target has already been processed. These are browser navigation semantics, not user or ledger authority.
2. [MDN manifest protocol_handlers](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/protocol_handlers): experimental/limited availability; an OS may associate registered schemes with an installed PWA, forwarding a URL through a configured HTTPS handler path within scope. The `%s` substitution is untrusted input. Browser, OS and user policy govern registration. **No Safari/iPadOS managed-EFB support is presumed.**
3. [MDN LaunchQueue](https://developer.mozilla.org/en-US/docs/Web/API/LaunchQueue): `LaunchParams.files` may contain file handles in applicable implementations. A handle or successful launch does not imply the file is a valid, safe or user-authorized LogMate backup. This depends on platform file handling and is not an iPad Files custody guarantee.
4. [WICG Web App Launch Handler draft](https://wicg.github.io/web-app-launch/) and [Manifest Incubations](https://wicg.github.io/manifest-incubations/): incubation proposals and UA implementation are distinct from broadly interoperable normative support. Re-check exact platform versions and OS/MDM restrictions before adopting launch behavior. These references are capability/watch inputs, **not tested product evidence**.

**Boundary taxonomy:** manifest identity determines installation grouping; `scope` constrains which URLs are within an app's navigation envelope; SW control determines fetch handling; launch handler determines client reuse; OS protocol/file/share registration determines external entry; authentication determines current session; owner/epoch admission determines data writes. None implies any of the others. On iPad Safari tab, Home Screen web app and managed Web Clip, launch semantics and data containers may differ even for an identical URL.

### 32.2 SYNTHESIS — secure launch pipeline and failure modes

**Proposed admission pipeline (not implemented or approved):** (L0) receive OS/URL/launch event with provenance class; (L1) parse as data, canonicalize URL and reject unsupported scheme, unexpected origin, credentials, excessive length, malformed encoding, ambiguous duplicate parameters and unauthorized route; (L2) separate public help/store link from private logbook/import action; (L3) resolve actual app instance/container, current build and owner state **after** initialization and durable ledger readback; (L4) if signed out, locked, stale owner, offline or missing container, show a neutral pending-intent/recovery state without revealing flight content; (L5) require user-initiated review and exact owner/epoch/operation admission before any import, restore, sync, deletion or deep-linked mutation; (L6) idempotent commit, durable readback and appropriately scoped receipt. Never let a URL query or protocol payload silently set current owner or overwrite an unsynced draft.

| Input/failure | Unsafe interpretation | Required safe result |
| --- | --- | --- |
| OS launches same PWA while A flight draft is open | Reused window implies permission to replace draft with target | Preserve draft and show non-destructive intent review; do not auto-navigate into destructive operation |
| `focus-existing` target arrives while a modal/restore is active | Focus event is equivalent to explicit user approval | Queue or reject with bounded expiry; explicit confirm after modal closes |
| External `web+...` scheme embeds email, flight number or token | OS deep link is trusted and safe to log | Reject sensitive payload classes; scrub URL/referrer/analytics; avoid secret-bearing link designs |
| Stale A tab, B active | Target path selects A's data | Recheck owner/epoch inside transaction; zero-write denial and no A content leak |
| Link to `/apps/` or support | Same fallback as private offline app | Public HTTP/HTML/canonical must remain independently correct; do not return private cached shell to crawlers |
| App installed twice on iPad | Same manifest id means shared ledger | Treat each container's local state/replica as independent until authenticated owner admission and Files restore |
| File handler supplies backup | Handle equals trusted backup | Size/type/schema/semantic digest/owner validation, preview and independent recovery; reject without mutation |
| URL redirects outside app scope | Installed app can follow it securely by default | Validate origin/route and OAuth return policy; no credential/flight data in external navigation |
| SW V1 + client V2 during launch | New URL implies newest schema or worker | Preserve version fence and safe update/rollback; defer mutation until verified build/schema compatibility |
| Browser lacks Launch Handler | Feature absence means PWA cannot launch | Ordinary HTTPS navigation remains primary fallback; no installed-only promise |

**Operational rule:** keep externally supplied launch payload ephemeral and minimal. A queued intent should be single-use, bounded in size and lifetime, and must not survive owner switch as an actionable mutation. If it must be persisted for recovery, persist only a sanitized, non-sensitive descriptor with explicit owner binding and expiration; verify after cold restart. Reject unknown URL schemes and query keys by default. For OAuth callbacks, use established PKCE/state/nonce and allowlisted redirect routes; an arbitrary `targetURL` is not an authentication callback.

### 32.3 Falsifiable acceptance packet LH01–LH24 — DEFINED, NOT RUN

**Browser/OS capability A+C:** LH01 exact served build/manifest/SW SHA and OS/browser/MDM/container; LH02 `launch_handler` absent/invalid/unsupported fallback; LH03 `focus-existing` vs `navigate-existing` vs `navigate-new` on supported browser; LH04 no existing window/cold start; LH05 launch during bfcache/hidden/resume; LH06 double launch and order/race; LH07 OS protocol handler registration denied/unavailable; LH08 URL encoding, length, duplicate query and foreign-origin rejection; LH09 redirect across `scope` and OAuth route; LH10 Safari tab vs Home Screen vs managed Web Clip capability matrix, with **unsupported** explicitly recorded rather than forced PASS.

**Owner/ledger/Files E+C:** LH11 A unsent draft survives external launch; LH12 A→B switch rejects stale A target with zero writes; LH13 signed-out/offline/expired-auth link cannot read or mutate private ledger; LH14 wrong-owner/corrupt/oversized file handle zero-write reject; LH15 valid backup requires review + fresh-context readback; LH16 two installed containers cannot silently merge replica identity; LH17 SW V1/client V2/schema migration and pending intent; LH18 interrupted import/duplicate launch operation idempotence; LH19 stale pending intent expires after logout/delete/owner epoch change; LH20 local diagnostic and server event traces contain no email, token, flight or file-path canaries.

**B/D/C transfer:** LH21 keyboard/VoiceOver/TalkBack focus and explicit Cancel/Review during reused-window launch; LH22 private launch URL never appears in public canonical/robots/sitemap or crawler-visible cached shell; LH23 public support/store links remain valid HTTP without installed PWA or JS; LH24 marketing/support claim parity with observed iPad/Chromium capability and MDM permissions. Each test needs expected/actual UI, URL/scope, owner/epoch, ledger/Files oracle, source SHA, platform, negative control and disposition.

**CONTRADICTION / transfer:** Launch Handler's existence cannot resolve §17/18 offline peer transport, §16 Files custody, §30 OAuth persistence or §31 installed-container migration. It may **increase** stale-tab and unintended owner-context exposure unless explicitly fenced. Design Studio W121 covers accessible navigation/focus design but does not prove a managed-EFB runtime. Engineering S007 owns deletion/reauth saga; Marketing's current production decisions remain unapproved. LogMate MASTER describes approved manual delta sync as not yet production-complete, so no link-driven automatic sync promise is justified.

**MINTTAP DECISION — recommendation only:** Treat ordinary HTTPS URLs as the portable launch baseline; add optional installed-only handlers only after supported-device and privacy review, with no automatic ledger mutation. **OPEN:** exact LogMate launch/deep-link implementation, generated manifest and SW, authorized managed-iPad behavior, OS registration and product/runtime acceptance. **CHANGE WATCH:** Launch Handler/Protocol Handler incubations, WebKit implementation and iPad MDM policy. **Gate: Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

## 33. Stage 8 — push subscription, declarative notification and owner-deletion trust boundaries (2026-11-08)

**Problem and novel boundary:** §§19, 21, 26, 31–32 discuss Worker commands, offline auth, accessibility, installed containers and external launches. None establishes the separate *server-held push subscription* lifecycle. Notification delivery, click handling, subscription revocation, owner deletion, badge display, remote Sync and independent Files custody are different predicates. **Lead E** (subscription secret/owner revocation/operations); **A** (WebKit/Chromium capability and Worker/declarative delivery); **C** (cross-platform and privacy negative controls); **B** (permission/notification/recovery UX); **D** (truthful public claims and analytics). **Class:** SOURCE + SYNTHESIS + VALIDATION DEFINED, NOT RUN.

### 33.1 Historical development, primary sources and precise platform limits

- **[SOURCE — W3C Push API Working Draft, 2024-09-03](https://www.w3.org/TR/2024/WD-push-api-20240903/):** Push subscriptions are bound to Service Worker registrations under the conventional Push API; unregistering a registration deactivates associated subscriptions. Endpoint privacy and deactivation/reuse restrictions matter. A standard specification does not guarantee exact provider delivery or an MDM allowance.
- **[SOURCE — MDN Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) and [PushSubscription](https://developer.mozilla.org/en-US/docs/Web/API/PushSubscription), inspected 2026-11-08:** the endpoint is a sensitive capability URL and the subscription includes encryption key material. Treat endpoint disclosure as a security event; avoid logging it in diagnostics, analytics, exception messages or exported support files. `unsubscribe()` is not a server-side owner/subscription mapping deletion receipt; server tombstoning and retry reconciliation are separately required.
- **[SOURCE — WebKit iOS/iPadOS 16.4 announcement](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/):** user-initiated notification permission and Web Push were introduced for **Home Screen web apps**, not every Safari tab or arbitrary managed Web Clip. Focus, per-install identity and Badging API are distinct from account/replica authority. Apple Push Notification service participates in Web Push delivery, so **strictly internet-disconnected EFB peer sync cannot rely on push**.
- **[SOURCE — WebKit Safari 18.4](https://webkit.org/blog/16574/webkit-features-in-safari-18-4/) and [Meet Declarative Web Push](https://webkit.org/blog/16535/), 2025:** declarative Web Push shipped for iOS/iPadOS 18.4 Home Screen web apps. It can display notifications **without executing a Service Worker**, with optional Worker processing/fallback. This explicitly refutes the universal claim that every push notification must execute app JS. Conversely, a displayed notification is **not** evidence that app code ran, owner permission was rechecked, an IndexedDB transaction committed, or a Sync receipt was issued.
- **[SOURCE — WebKit Safari 18.5](https://webkit.org/blog/16923/webkit-features-in-safari-18-5/), 2025:** declarative Web Push became available on macOS Safari. This does not establish managed-iPad policy, current exact app implementation, or the same behavior in Chromium. Platform support and notification permission must be checked by feature, install mode, OS version and MDM policy.

**HISTORY → DESIGN PRINCIPLE:** legacy Web Push used JavaScript Service Worker processing; declarative delivery reduces wakeups and provides fallback, but makes the distinction between **user-visible notification** and **executed owner-fenced application operation** more important. Delivery is an untrusted *hint*; an authenticated foreground read and explicit owner/epoch check are required before any private record is shown or changed.

### 33.2 Independent lifecycle and owner-authority states

| State / signal | What it can prove with exact evidence | What it cannot prove |
| --- | --- | --- |
| P0 permission granted | browser/OS notification consent for the relevant installed context | server subscription registered, permanent consent, MDM approval for all containers |
| P1 subscription obtained | current registration returned endpoint/keys | server stored correct owner binding, remote device reachable |
| P2 server accepted mapping | authenticated owner/installation/epoch mapping persisted with versioned consent | message delivered, subscription active forever, same owner after logout |
| P3 push provider accepted | provider acknowledged request | notification shown, Worker executed, ledger synced |
| P4 notification displayed | OS/browser presentation under actual settings | correct current owner, app opened, backup saved, Sync ACK |
| P5 click / launch event | untrusted navigation intent was delivered to a client | authorization to open flight details, import, delete or mutate |
| P6 owner-fenced foreground read | current account/epoch/replica and local ledger validated before view | independent Files recovery or remote Sync completion |
| P7 subscription retirement | server mapping disabled, endpoint removed/reconciled, device unsubscribe where feasible | guaranteed immediate erasure of already queued provider notifications |

**Deletion/owner transition invariant:** account A sign-out, A→B switch, account deletion and installed-container retirement must invalidate server send authority **before** B can receive A-specific push content. Revocation must be idempotent, crash/retry safe and independently reconciled. If local unsubscribe fails offline, server must stop sending; if server is unreachable, the product must not claim that remote notifications were revoked. Do not put account, crew, flight number, airport, route, private backup, token or sync metadata in notification title/body/deep link. Generic content is still a privacy design choice, not an automatically approved policy.

**Declarative-specific contradiction:** a push may be displayed without Worker code running. Therefore notification click, background badge or push acceptance must **never** be an operation commit signal. A stale notification from account A, clicked after account B login or account deletion, must resolve to a safe neutral landing route and require fresh owner authorization, not reuse a cached private view. Scope/manifest identity, push endpoint, OS Focus and LogMate owner/replica remain separate identities.

### 33.3 Failure analysis, alternatives and privacy

1. Safari tab, Home Screen PWA, MDM Web Clip and Chromium installed PWA can expose different permission/subscription surfaces. Treat unsupported as **UNSUPPORTED**, not product failure or evidence of an unavailable API.
2. Offline EFB with no internet cannot receive APNs/Web Push; push must not be part of the required offline-first logging or local peer-sync correctness path.
3. User disables notifications/Focus suppresses display; missing push is not evidence of missing flights or Sync failure.
4. Subscription endpoint leaks in log, URL, analytics or support bundle; it is a capability secret and requires redaction, rotation and abuse analysis.
5. User changes account without retiring old server mapping; A content could appear on B's lock screen. Require server-side owner/epoch invalidation, generic payload and privacy negative control.
6. Delete starts, provider accepts already queued message; an accepted retirement cannot guarantee instantaneous recall. Document residual queue risk; do not claim complete notification erasure prematurely.
7. Multiple Home Screen installations share a manifest id but differ in OS names/Focus and storage contexts; no inference of identical subscription or ledger.
8. SW update or schema change during push event; do not let old event payload mutate new owner/schema state.
9. Notification action or deep link bypasses login; always treat action as untrusted navigation and validate current owner/epoch.
10. Excessive permission prompts, background badges or notification text can compromise cockpit UX and user privacy; user-initiated, reversible, nonessential notification design is the safer research default.
11. Push provider HTTP acceptance and local device receipt are independent; delivery analytics need bounded privacy-safe, consented evidence, not endpoint/UID telemetry.
12. An incident causes subscription DB loss or server compromise; rebuild subscriptions through explicit owner-approved registration, never infer them from cached cookies or public manifest id.

### 33.4 Integrated falsification packet PN01–PN24 — DEFINED, NOT RUN

**A/C platform and lifecycle:** PN01 exact NORMAL/served SHA and iPadOS/Chrome versions; PN02 Safari tab vs Home Screen vs managed Web Clip vs Chromium capability detection; PN03 permission direct-gesture denial/revocation; PN04 iOS 16.4 conventional push vs 18.4 declarative path; PN05 notification display without SW JS (declarative negative control); PN06 SW termination and update; PN07 Focus/OS disabled notification; PN08 no-internet EFB/APNs blocked; PN09 repeated installed copies with distinct subscription and Focus; PN10 badge state versus ledger truth.

**E/C authority, privacy and deletion:** PN11 redacted endpoint/keys and payload canary scanner; PN12 A→B mapping retirement and zero A-specific content; PN13 logout offline, server unreachable, pending revoke status truth; PN14 delete/revoke saga crash and retry; PN15 provider accepted but device never displayed; PN16 already queued message after retirement; PN17 stale A click after B login or deletion zero private-data disclosure; PN18 malicious or duplicate notification action idempotence; PN19 endpoint leak/rotation and retention boundaries; PN20 stale Worker schema/owner epoch rejects writes.

**B/D/C UX and public claims:** PN21 accessible opt-in, deny, revoke and no-notification fallback; PN22 neutral notification copy and lock-screen privacy; PN23 support/Store claim parity with exact Home Screen/MDM feature matrix; PN24 explicit no-push, no-internet, no-background proof of local logging, independent Files restore and manual Sync continuity. For each record source/served SHA, app container, OS/browser, server owner mapping, expected/actual provider/device/ledger observations, privacy canary and zero-write negative control. Never use real flight/user data in public artifacts.

**MINTTAP DECISION — research recommendation, NOT approved product feature:** keep push and badging strictly optional, out of the flight ledger's correctness path, with no private lock-screen content and no automatic mutation from click. Do not implement a push service without product approval, endpoint/consent inventory and Engineering-owned revocation tests. **DEPENDENCY:** Engineering S007 deletion/reauth saga, LogMate owner/replica and Files gates, Design Studio W121 accessible opt-in and Marketing claim HOLD. **OPEN:** no verified LogMate push implementation, server mapping, managed-EFB permission, physical device delivery or runtime tests. **CHANGE WATCH:** WebKit declarative semantics, browser Push API drafts, APNs/MDM rules, OS Focus behavior. **Gate remains Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

## 34. Stage 8 — WebAuthn/passkey assurance versus offline owner authority (2026-11-08)

**Ownership and allocation:** E (trust, authentication, recovery) primary; A (RP ID/origin/browser mechanics) dependency; C (negative-control/device acceptance) test owner; B (account recovery/accessibility) and D (public claims) consumers. This is a **cross-track adjacent Stage 8 question**, not approval to implement passkeys in LogMate. Prior §30 addresses cookies and owner epochs; §31 installed identity; §33 push. None can be substituted for WebAuthn RP-scoped server verification. **Evidence:** SOURCE (current standards and MDN) + SYNTHESIS; product implementation/runtime **UNKNOWN**.

### 34.1 History → standard → browser reality

- **HISTORY / PRINCIPLE:** Password reuse, phishing and SMS interception motivated authenticator-backed asymmetric public-key authentication. The authenticator signs a server challenge with a credential scoped to a Relying Party; the RP verifies the challenge, RP ID hash, origin, credential, signature and required user-presence/verification semantics. This is stronger online authentication, not a guarantee of an unlocked local flight ledger. See [W3C WebAuthn Level 3 Recommendation](https://www.w3.org/TR/webauthn-3/) (25 August 2026) and [MDN Web Authentication API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API).
- **SOURCE — version discipline:** W3C WebAuthn Level 3 is a Recommendation as of 25 August 2026. [Level 4](https://www.w3.org/TR/webauthn/) is a 15 September 2026 First Public Working Draft, **not** an interoperable production guarantee. Feature support must be tested by capability and exact browser/OS, not inferred from the highest draft level. **CHANGE WATCH** Level 4 and browser feature tables.
- **SOURCE — RP scope and related origins:** A passkey belongs to a specific RP ID and authenticators enforce RP constraints; [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) defines Related Origin Requests under constrained, validated rules. A company website at `minttap.app`, a product PWA at another origin, an OAuth provider, and an installed manifest ID are **not automatically interchangeable RP authorities**. A cross-origin iframe or redirect is not a blanket permission to register/use arbitrary credentials. Verify actual origin, RP ID, related-origin authorization, TLS and server challenge binding before adopting any shared-login design.
- **SOURCE — conditional mediation and client capability:** [MDN conditional mediation](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/isConditionalMediationAvailable_static) and [MDN WebAuthn](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API) describe `getClientCapabilities()`, `conditionalGet` versus `conditionalCreate`, and username-field `autocomplete="username webauthn"`. These are separate browser/UI capabilities; a generic WebAuthn API presence check does **not** certify conditional creation, hybrid transport, related origins or managed-iPad credential-provider permission.
- **SOURCE — authentication/recovery distinction:** User verification (UV), user presence (UP), discoverable credential, passkey synchronization across devices and authenticator attestation are different concepts. UV is not an authorization token for every future offline write. A credential's availability or successful assertion does not independently prove the account owner, the current local ledger epoch, or the correct backup key. Enterprise-managed passkey provider, external security key, iCloud Keychain and cross-device transport availability require operator/device testing. The [W3C Level 3 spec](https://www.w3.org/TR/webauthn-3/) is the normative security source; MDN is implementation guidance.

### 34.2 Six distinct authorities and required checks

| State | What may be claimed | What must not be inferred |
| --- | --- | --- |
| P0 — UI suggests a passkey | Credential provider or autofill may have an eligible option | User authenticated, account recovered, ledger unlocked |
| P1 — authenticator signs challenge | Browser obtained a scoped assertion, with RP/user verification semantics | Server accepted, current account identified, remote sync completed |
| P2 — server validates assertion | Fresh challenge, RP ID/origin, signature, flags and credential binding verified; server session may be issued | Offline cached record ownership, backup/restore, durable local write |
| P3 — owner-fenced local admission | Product-specific authenticated owner/epoch, schema and write authority checked independently | Files backup or remote replication has completed |
| P4 — remote ledger receipt | Server accepted specific owner/epoch/op under engineering ledger protocol | Independent recovery of local Files backup |
| P5 — independent recovery | Fresh-context Files artifact validated, restored and reconciled with owner/schema rules | All future sessions or devices will remain accessible |

**Invariant:** P0–P2 may facilitate identity proof for an online session but must never silently reassign pre-existing offline records, erase A on B login, mark unsent edits as synced, or promote a backup/export UI toast to verified custody. WebAuthn cannot function as a guaranteed offline reauthentication step on a disconnected managed EFB unless the product has an independently designed and tested offline authority scheme. Likewise, a passkey's presence does not mean the private key can be exported or used as a generic local data-encryption key. Any PRF extension proposal needs its own availability, key lifecycle, recovery and cryptographic review.

### 34.3 Threats, contradiction tests and recovery UX

1. **Origin mismatch:** marketing and product origins differ; RP-scoped assertion fails, even though manifest `id` looks the same. Do not weaken origin/RP verification to suppress the error.
2. **Challenge replay:** previously accepted assertion is resubmitted or a stale browser tab completes late. Fresh server nonce, timeout and challenge/session binding are required.
3. **Account A→B:** B successfully signs in with a passkey while A's unsynced local edits exist. Keep A's records owner-fenced; do not automatically merge or delete them.
4. **Offline first launch:** the authenticator or network verification is unavailable. Do not imply the user can always recover an account or synchronize offline.
5. **MDM blocks credential provider:** WebAuthn capability exists in Safari generally but managed Web Clip disallows configured passkey provider or cross-device ceremony. Show a supported fallback, not a fabricated success.
6. **Lost device/passkey:** passwordless account recovery must preserve privacy and prevent attacker-driven owner takeover. Neither public website support nor a backup artifact alone can grant server account authority.
7. **Conditional autofill confusion:** password and passkey suggestions can coexist; the displayed identity label is not a verified owner ID until the RP validates the assertion.
8. **Credential deletion/revocation:** deleting a server-side passkey must revoke future authentication; existing sessions and local data require distinct explicit policies. A browser credential cleanup hint is not a deletion receipt.
9. **URL and telemetry leak:** never log credential IDs, user handles, challenges, assertion blobs, recovery tokens or identifiable flight data to marketing analytics; prevent auth URL/query leakage.
10. **Accessibility:** fallback and error states need keyboard/VoiceOver operation, explicit offline messaging and a route to recover without presuming a particular device authenticator.
11. **Related-origin misuse:** an overly broad related-origin authorization creates unexpected login surface; validate domain control and deny unknown origins.
12. **Cryptographic overclaim:** passkey-based authentication does not by itself encrypt IndexedDB, prevent browser-origin eviction or make an independent Files backup recoverable.

### 34.4 WA01–WA24 acceptance packet — DEFINED, NOT RUN

**A/E (protocol and browser):** WA01 served origin, exact RP ID and build SHA; WA02 HTTPS/secure-context enforcement; WA03 valid fresh challenge/signature/origin/RP/UV verification; WA04 wrong RP ID and hostile origin rejection; WA05 replayed/expired challenge rejection; WA06 old tab/redirect race; WA07 conditionalGet supported versus unsupported; WA08 conditionalCreate supported versus unsupported; WA09 related-origin request allow/deny; WA10 hybrid/security-key and managed credential-provider differences.

**E/C (owner, custody, privacy):** WA11 successful assertion for B with A's unsynced records; WA12 account deletion versus authenticator credential cleanup and active session revocation; WA13 authenticator loss/recovery with independent owner check; WA14 network loss before and after RP receipt; WA15 stale server session and offline local write; WA16 offline 37-store ledger/Files recovery independent of WebAuthn; WA17 passkey credential/URL/analytics secret canary scanner; WA18 invalid/duplicate credential mapping; WA19 conditional autofill label versus verified server UID; WA20 server RP migration/rotation rollback with credential continuity plan.

**B/C/D (interaction and claims):** WA21 VoiceOver/keyboard/200% text fallback, cancellation and recovery; WA22 iPad Home Screen versus Safari and Chrome/Android capability matrix; WA23 managed EFB MDM policy/credential-provider actual result; WA24 website/Store/support language claims audit: no guaranteed passkey, offline authentication, backup or sync claims without exact execution. Each packet records exact source SHA, served origin/RP ID, browser/OS/MDM mode, fixture-only account identifiers, expected/actual assertion/owner/Files oracles and negative controls. **No real credentials or user data in public CI artifacts.**

### 34.5 Operational judgment and transfer

**MINTTAP DECISION — research recommendation, not implementation approval:** Retain current approved Apple/Google/email onboarding scope unless the product owner authorizes passkeys; avoid introducing a fourth sign-in method solely because the standard exists. If passkeys are considered later, Engineering owns server RP verification and account recovery, Web Manager owns browser/origin/MDM matrix, Design Studio owns interaction/accessibility, Marketing owns truthful support and Store claims. Prefer recovery/custody validation before new sign-in surfaces. **DEPENDENCY:** exact Flutter Web/Firebase auth implementation and real served origin, configured RP, approved test identities, operator MDM policy and independent Files restore. **OPEN:** whether LogMate implements WebAuthn, exact authentication provider, browser support in approved EFB. **VALIDATION:** WA01–WA24 are defined only; no physical-device or NORMAL runtime PASS. **CHANGE WATCH:** WebAuthn L4 draft, related-origin, credential-management capabilities, managed passkey provider restrictions. **Gate:** Stage 8 ACTIVE · production validation OPEN · PWA release HOLD.

## 35. Stage 8 — deployed code provenance, hostile Service Worker persistence and data-safe incident recovery (2026-11-08)

**Question / novelty:** Previous §§19/28 cover update lifecycle, schema, rollback and storage. This packet asks a distinct *supply-chain and incident-containment* question: how can an operator distinguish an authorized exact build from a substituted HTML/worker/import, and recover from a compromised or wrongly deployed worker **without destroying the only offline flight records**? Track **E owns security/operations**, A supplies worker/browser semantics, C owns independent incident exercises, B recovery interaction, D public incident/support claims. This is a source-derived operational design, not an observed MintTap/LogMate compromise.

### 35.1 SOURCE, history and scope

- **[SOURCE — OWASP HTML5 Security Cheat Sheet, checked 2026-11-08](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html):** a compromised Service Worker can intercept requests for controlled paths, and merely expiring cached content does not unregister it. Restrict registration to an intended origin/scope; never store sensitive responses in Cache API without a deliberate, bounded owner-aware design. The generic OWASP recommendation to use a cache-busting worker filename must be reconciled with Chrome/web.dev's advice to **retain a stable registration URL** for reliable update checks: neither practice alone proves supply-chain integrity. Decide from exact deployed update path, not from one rule in isolation.
- **[SOURCE — MDN Subresource Integrity, checked 2026-11-08](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity):** `integrity` attributes cover document-loaded script and supported link resource types, not a general cryptographic authorization for the entire application or a `navigator.serviceWorker.register()` option. A page whose HTML and hash metadata are both replaced by an attacker may consistently load malicious content. Cross-origin SRI needs CORS. `Integrity-Policy` and report-only modes apply to relevant document subresources, with browser support and deployment behavior requiring exact testing; they are not a substitute for worker/manifest provenance.
- **[SOURCE — MDN ServiceWorkerRegistration.updateViaCache](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache) and [Chrome worker freshness](https://developer.chrome.com/blog/fresher-sw):** `imports` is the default; the browser does not consult the HTTP cache for the top-level worker update check but may for imported scripts, whereas `none` bypasses both. Chrome's worker import byte comparison and HTTP cache handling evolved by version. Changing `updateViaCache` does **not** authenticate deployment bytes, prove the active client controller version, or make an offline worker fetch a newer release.
- **[SOURCE — web.dev worker lifecycle](https://web.dev/learn/pwa/update) and [MDN Using Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers):** waiting/active/controller states and caches are distinct. Deleting a worker script on the server does not automatically unregister a previously installed worker. `skipWaiting()` or `clients.claim()` can expose older pages to newer worker behavior; retaining prior immutable shell assets and explicit client/build compatibility is safer than automatic takeover. Worker cache deletion is not equivalent to account-data deletion.
- **[SOURCE — MDN Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data):** `"storage"` can clear origin storage including service worker registrations where supported. It is a **destructive containment tool** for an offline-first app, not a safe routine rollback. Header delivery and platform support must be verified from a genuine network response, and no incident playbook should prescribe origin-wide clearing before independent Files custody is confirmed.

**Standards / platform / product separation:** SRI, HTTPS and CSP are defense-in-depth, not a universal trusted-code guarantee; SW lifecycle is standards-based with implementation-specific update timing; managed Safari/Web Clip storage and operator network policy are distinct; LogMate's actual served Flutter Web bundle, CDN, headers, build provenance and independent Files state are **UNKNOWN** in this packet.

### 35.2 Distinct proof chain: do not collapse deployment, controller and data custody

| Gate | Minimum evidence | Counterexample that defeats an overclaim |
| --- | --- | --- |
| P0 — authorized source | reviewed Git SHA, dependency lock, reproducible CI build attestation where available | clean repository with compromised delivery CDN |
| P1 — deployed bytes | immutable asset hashes, server/CDN origin and header evidence for served index/worker/import/manifest | HTML points at a different worker or mutable dependency |
| P2 — browser-controlled build | actual client `controller.scriptURL`, worker state, build handshake, cache manifest/hash verification | new V2 deployed while V1 still controls offline tab |
| P3 — storage/owner admission | versioned schema, owner/epoch fencing, transactional zero-write rejection | valid shell whose code writes old-owner records |
| P4 — remote authority | authenticated owner-scoped ACK with operation identity | successful HTTP fetch or telemetry beacon only |
| P5 — independent recovery | separate Files artifact read back, verified and restored in fresh authorized context | origin storage cleared while only local ledger existed |

**Invariant:** a P0 source SHA does not establish P1 served bytes, and P1/P2 do not establish P3–P5. A security incident may justify revoking remote credentials or blocking new writes immediately, but destructive local storage clearing is a different owner-consented operation with a recovery gate. If the origin is compromised, on-origin UI or scripts cannot be assumed to be a trustworthy channel for backup instructions; use a separately authenticated support channel and a known-good build/device where authorized.

### 35.3 Failure modes and response decision tree

1. **Substituted CDN script:** build provenance is clean but served JS differs; quarantine deploy and preserve immutable evidence, disable affected routes at trusted edge, rotate credentials as indicated. SRI may detect a *document subresource* mismatch; do not infer it detects a replaced worker.
2. **Compromised origin HTML plus hashes:** both HTML and integrity values change, so SRI alone does not establish trust. Require out-of-band release manifest/attestation and operator-side served-byte comparison.
3. **Old malicious worker persists:** corrected server file deployed but offline clients remain controlled by old worker. Identify each installed container and exact controller; plan trusted network-mediated recovery, not "deploy fixed HTML = all clients safe."
4. **Accidental `Clear-Site-Data: "storage"`:** registered worker, IDB and caches may be cleared; absent independent Files artifact, local unsynced flights can be lost. A blanket kill-switch response is prohibited until custody and owner authorization are satisfied.
5. **False rollback:** old HTML shell restored but new IndexedDB schema is not backwards compatible. Only an Engineering-approved migration/forward-repair or verified snapshot restore can establish safety.
6. **Mixed immutable assets:** old tab requests removed chunk after new worker takeover; preserve release assets for active clients and test offline lazy routes.
7. **Auth leakage through cache:** authenticated API response or redirected OAuth URL cached into a broadly served navigation fallback. Apply owner-bound route/cache partitioning and cache exclusion, test A→B and stale tabs.
8. **MDM/physical offline EFB:** device cannot reach clean deployment or external support; remote incident response cannot promise immediate worker eviction. Local work must remain safe/read-only where appropriate; independent Files is the fallback only if operator policy permits.
9. **Diagnostic silence:** no reports from offline clients; do not interpret absence as a safe deployment or completed cleanup (§27).
10. **Overbroad scope:** worker installed at site root intercepts unrelated marketing/support pages. Keep least-privilege worker scope and separate origin where security posture requires; URL path is not a separate same-origin security principal.
11. **Header mismatch:** `Cache-Control`, CSP, `Service-Worker-Allowed`, CORS and SRI headers differ between CI preview, CDN edge and actual served origin. Only served responses settle deployed behavior.
12. **Operator emergency:** remote token revocation succeeds but local owner data is still present. Identity/session revocation, local deletion, storage purge and Files retention are independent phases; Engineering S007 owns the deletion saga.

### 35.4 Executable acceptance packet SC01–SC24 — DEFINED, NOT RUN

**E/A deployment and platform:** SC01 exact source/lock/build SHA and signed or otherwise verifiable artifact manifest; SC02 served HTML/worker/import/manifest byte hashes against manifest; SC03 edge/CDN header variation by route; SC04 `updateViaCache=imports/all/none` on actual Safari and Chromium; SC05 V1 active/V2 waiting/client controller/build handshake; SC06 offline worker remains old despite clean server; SC07 `skipWaiting` mixed chunk negative control; SC08 overbroad scope and `Service-Worker-Allowed` restriction; SC09 SRI tampered document subresource blocked; SC10 HTML+SRI both substituted negative control; SC11 CSP/Integrity-Policy report-only vs enforce with actual browser support; SC12 script MIME/redirect/failure path.

**E/C data, identity and incident:** SC13 sensitive authenticated response not admitted to Cache API; SC14 account A→B old-worker cached fallback zero disclosure; SC15 malformed import/old schema write rejected; SC16 `Clear-Site-Data` dry-run on disposable origin with explicit loss accounting; SC17 rollback to incompatible schema rejected, data retained; SC18 remote revocation cannot falsely mark local erasure; SC19 37-store independent local readback plus Files hash/schema/owner restore; SC20 no-network incident support and managed Web Clip policy.

**B/C/D transfer:** SC21 recovery UX with offline/unsynced warning, accessible safe focus and truthful scope; SC22 publicly documented incident status never claims all clients updated from CDN deploy alone; SC23 privacy-safe diagnostic canaries and no flight/UID/token/URL leak; SC24 runbook drill with separate roles for Engineering release/identity, Web Manager edge/worker, Design Studio recovery, Marketing support, EFB operator physical custody. For each case capture exact tested build, origin, OS/browser/MDM mode, controlled synthetic accounts, expected/actual worker/cache/ledger/Files oracles and negative controls. **No actual product or managed-iPad execution occurred.**

### 35.5 Operational judgment and transfer

**MINTTAP DECISION — research recommendation only:** before expanding PWA features, obtain a deploy-to-client provenance and safe rollback/incident matrix. Prefer non-destructive server-side quarantine and owner-fenced read-only states over immediate origin-wide purge when independent backup is unverified. Do not assume a single browser header can reliably remediate every installed EFB context. **DEPENDENCY:** Engineering actual Flutter Web generated artifacts, release/CI SHA and schema, hosted edge/CDN operator, device/MDM permissions, owner-safe backup recovery; **OPEN:** product deployment architecture, current worker scope/headers, incident channel, actual cached sensitive responses. **VALIDATION:** SC01–SC24 specification only. **CHANGE WATCH:** Integrity-Policy browser adoption, SW update algorithm, WebKit container behavior, CSP enforcement, OS storage controls. **Gate unchanged: Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD.**
