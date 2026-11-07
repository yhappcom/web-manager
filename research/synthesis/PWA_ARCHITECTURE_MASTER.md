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
