# 431 — Stage 8 PWA HTTP Cache, Cache API and Update-Currentness Boundary

**Checkpoint:** 2026-10-20 KST. **Canonical:** `yhappcom/web-manager/main@6ba4f1df34ea4cdc6cad28ac2c16377b9a166829`. **Product read-only:** `yhappcom/logmate/main@6101666530cb706a042ac82614c840af441895b1`. **Owner:** Track E, with Track A browser mechanics, C execution/quality, B recovery UX and D discovery/measurement transfer. **Gate:** SOURCE + source-level SYNTHESIS; Chromium browser probe NON-EXECUTION; current NORMAL build, Firebase Emulator, deployed HTTP, Safari/iPad, records and Sync OPEN. **PWA release HOLD.**

## 1. HISTORY / PROBLEM → PRINCIPLE

AppCache's opaque lifecycle motivated programmable Service Workers, but an offline application now crosses at least four distinct caches/state layers: (1) HTTP private/shared/CDN caches governed by RFC 9111, (2) explicit same-origin Service Worker Cache API storage controlled by JavaScript, (3) installed Service Worker script registration/update/control, and (4) IndexedDB/Sembast owner records and backup. A fifth mechanism, browser back/forward cache (bfcache), stores page state rather than an HTTP response. Conflating these mechanisms can cause false claims: “no-store disables offline,” “no-store guarantees fresh installed code,” “Cache API presence proves owner-data durability,” or “a 304 reauthorizes queued operations.” None follows.

**Principle:** evaluate freshness, code identity, offline readiness, version pinning, user-data preservation, and authority independently. Never change cache policy solely to improve a synthetic score or assume a browser/OS feature from one implementation.

## 2. SOURCE — exact source and authoritative platform evidence

- The five canonical Web Manager operating files, recent commits and research 427/430 were checked. Latest committed Web Manager head is `6ba4f1d`; 428–430 were local evidence in preceding checkpoints, not assumed GitHub commits. `STATUS.md` still contains a 2026-10-09 catch-all Hosting rewrite claim that **does not match** current LogMate source.
- [LogMate firebase.json](https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/firebase.json) sets one `hosting.headers` rule `source: "**"`, `Cache-Control: no-cache, no-store, must-revalidate`, and `hosting.public: build/web`. It excludes `**/.*` and contains three explicit Auth rewrites, **not** a catch-all.
- [LogMate web/flutter_bootstrap.js](https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/web/flutter_bootstrap.js) registers `logmate_service_worker.js` with `updateViaCache: 'none'`, requests `registration.update()`, and does not block first paint on registration. This is **source intent**, not proof of installed runtime behavior.
- [LogMate tool/pwa_precache.dart](https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/tool/pwa_precache.dart) generates Worker code that downloads each Shell/font/notice resource using `fetch(new Request(item.path, {cache:'no-store', credentials:'same-origin'}))`, checks byte length and SHA-256, then calls `cache.put(item.path, response)`. It verifies cached bytes again before serving and uses separate versioned Shell/font caches. Worker activation does not automatically delete old caches. This is source-level inspection, not current built Worker validation.
- [RFC 9111 §5.2.2](https://www.rfc-editor.org/rfc/rfc9111.html) defines `no-store` for HTTP caches, `no-cache` as mandatory revalidation before reuse, and `must-revalidate` as a stale-response restriction. Under the current combined directive, `no-store` dominates the ordinary HTTP-storage decision; it does **not** prove a Service Worker is installed or prohibit explicit Cache API application logic.
- [MDN Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache) explicitly states that the Cache API does not honor HTTP caching headers. Its entries are application-managed, versioned and quota/eviction subject. [MDN Request.cache](https://developer.mozilla.org/en-US/docs/Web/API/Request/cache) distinguishes a fetch's HTTP cache mode `no-store` from a subsequent explicit `Cache.put`.
- [MDN updateViaCache](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache) specifies `none` bypasses the HTTP cache for Worker script **and imports** on update checks, not for all app resources. [MDN registration.update](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update) describes an update attempt, not guaranteed immediate activation or release promotion.
- [Firebase Hosting cache behavior](https://firebase.google.com/docs/hosting/manage-cache) documents CDN and browser cache behavior; Hosting deploy invalidates cached static content on its CDN. Exact served headers/bytes and real cache revalidation are still untested for LogMate.
- [Chrome bfcache no-store change](https://developer.chrome.com/docs/web-platform/bfcache-ccns) documents conditional bfcache eligibility for `no-store` pages beginning in the 2025 rollout. **Do not assert `no-store` universally disables bfcache in current Chromium**, and do not project Chrome policy onto Safari.
- [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) (2023, version-qualified) explicitly distinguishes Cache API/IndexedDB quota from HTTP cache and documents eviction/persistence heuristics. Quota maxima are not guaranteed retention; physical managed-iPad and current iPadOS behavior are CHANGE WATCH.

## 3. SYNTHESIS — twelve connected judgments

1. **HTTP response:** the current wildcard `no-store` is a source-confirmed policy for Hosting static responses; the actual deployed response is not observed. It prevents normal HTTP cache storage, not all possible browser or script-managed persistence.
2. **Explicit offline storage:** Worker `cache.put` can deliberately store a verified response despite its `no-store` HTTP header. The application owns invalidation, integrity and data classification; a security-sensitive personalized response must not be placed into a shared Shell cache.
3. **Fetch mode:** `Request.cache='no-store'` bypasses the ordinary HTTP cache for the download; it does not undo the following explicit `cache.put`. Therefore a source-level `no-store` + `cache.put` pair is not an inherent contradiction.
4. **Install transaction:** initial offline readiness requires successful fetch, verification, Cache API writes and Worker lifecycle control. No header can guarantee this under quota failure, network interruption, storage eviction or management policy.
5. **Worker update:** `updateViaCache:'none'` requests fresh Worker script/import retrieval; it does not force old tabs to relinquish control or force an unverified candidate into service. The Worker deliberately avoids `skipWaiting`.
6. **Version pin:** HTTP freshness and Worker script currentness do not establish old-client Shell byte identity. Only exact client-to-build assignment, verified Cache API response, URL alias handling and actual lifecycle tests can do so.
7. **Uncontrolled first visit:** bootstrap starts independently of Worker registration. A page without an active controller may load its Shell over the network; after offline transition, it may not be runnable until the install/cache path succeeds. No generic “always offline” claim.
8. **Resource cost:** the wildcard `no-store` removes ordinary HTTP cache reuse opportunities for static JS/WASM/fonts on uncontrolled or non-intercepted requests. **No measured bandwidth, latency or energy impact is available**; cache-hit and transfer analysis must be captured in real browser/network traces.
9. **Immutable candidates:** the font directory contains a version-derived ID, but `main.dart.js`, `flutter_bootstrap.js` and Worker filenames are stable. A long `immutable` policy is unsafe for stable executable URLs without an independent content-addressed path/deployment-retention contract. Versioned fonts could be candidates only after exact URL immutability, old-version availability, Hosting behavior and cache-pressure consequences are proven.
10. **bfcache:** it is distinct from HTTP and Cache API. Chrome's conditional `no-store` handling changed; Safari and managed-device behavior require their own observation. A bfcache restore may resume an old page without a network validation; use explicit currentness checks before sensitive remote actions.
11. **Owner data:** HTTP `no-store` is not a data-deletion, privacy, backup or durable-record policy. Cache API and IndexedDB may persist independently; deleting Shell caches or changing headers must not destroy flight records, unsynced operations or `.lbk` backups. Storage eviction still makes independent backup necessary.
12. **Authority:** `304 Not Modified`, a verified SHA-256, a current Worker or an offline-ready badge cannot prove current user authorization, successful Sync acknowledgement, valid schema migration or remote convergence. Preserve D006's operation/ACK/conflict boundary.

## 4. VALIDATION — what actually ran, and what did not

An **independent localhost Chromium 144 / Playwright probe** was implemented to serve `Cache-Control: no-cache, no-store, must-revalidate` on an HTML page, Worker and asset; the Worker would explicitly `cache.put` the asset during install, and the browser would request it after going offline. Chromium launched, but its first navigation to `http://127.0.0.1:<port>/` returned **`net::ERR_BLOCKED_BY_ADMINISTRATOR`**. Therefore the experiment is **NON-EXECUTION**: it neither proves nor disproves Chrome's Cache API behavior. The script and JSON failure result are retained locally. This is not a LogMate defect or a passed browser test.

**Required execution matrix, not yet PASS:** (a) current exact NORMAL artifact; (b) Firebase Emulator and preview/live response headers, ETag/304, status/MIME/byte identity; (c) first visit, controlled visit, offline restart, Worker update waiting/activation, old/new clients, URL aliases, quota failure, cache eviction; (d) Chromium and Safari tab versus installed Home Screen; (e) bfcache restore/currentness; (f) disposable record save/reopen, unsynced edits, independent `.lbk` export/restore; (g) managed-iPad MDM/storage envelope. Record actual HTTP cache versus Cache API hits separately, not a single “cached” Boolean.

**Proposed negative controls:** missing Worker registration; response `no-store` but successful Cache API storage; Cache API cleared with HTTP cache retained; HTTP cache cleared with Cache API retained; changed stable JS URL bytes while old client remains; `304` with stale organizational authority; bfcache restore with revoked remote session; quota exhaustion mid-install; unavailable old font URL after redeploy; loss of Cache Storage without deletion of owner records; HTTP 200 HTML fallback for missing JS; Firebase reserved/Auth path bypass.

## 5. MINTTAP DECISION — bounded and reversible

**Current decision: KEEP the existing Hosting cache header unchanged pending current-build runtime evidence; do not blanket-change to `immutable` or claim `no-store` breaks offline.** The wildcard policy is conservative for HTTP caching but may impose measurable costs outside Worker control. Consider a **future class-based policy** only after exact release identity and runtime tests:
- stable HTML/bootstrap/Worker/sidecar: conservative revalidation or no-store as appropriate, never blindly long-lived immutable;
- truly content-addressed static assets: consider long-lived immutable **only if URL and retention invariants hold**;
- Auth/session-sensitive responses: no-store/private rules and no unintended Cache API admission;
- unknown routes: explicit 404/route policy, not silent app-Shell fallback;
- user records: never infer durability from HTTP cache policy; independently test IndexedDB/Sembast and backup.

This is an Engineering/Operations review proposal, **not a shipped configuration**. Existing PWA G1–G6 remain unapproved. The high-value next step remains obtaining and executing the exact NORMAL build/Hosting/browser evidence; additional mock HTTP-cache models would not promote any gate.

## 6. Five-track comparative allocation and transfer

| Track | Stage 8 evidence/gap | Allocation |
|---|---|---|
| **E — primary** | Source policy known; current Hosting/runtime, release custody and data durability unproven | Own header classes, release/rollback identity, Cache API trust and safe data separation. |
| **A — prerequisite** | HTTP/Worker mechanics established; exact Chrome/Safari lifecycle/cache observations missing | Own HTTP cache vs Cache API vs SW update/control vs bfcache distinctions. |
| **C — validation** | Independent HTTP fixture evidence exists (430); real Chromium attempt blocked; physical Safari/performance/AT missing | Own actual cache-hit, transfer, update/offline/bfcache/device evidence, not synthetic score promotion. |
| **B — UX transfer** | Offline/recovery semantics designed, human/AT validation absent | Own “downloaded”, “offline ready”, “repair needed”, “locally saved”, “Sync acknowledged” distinctions and non-destructive recovery. |
| **D — discovery transfer** | Source policy known; live crawl/install/acquisition evidence absent | Own stable URL/404/canonical implications, privacy-minimal measurements and verified public feature claims. |

**TRANSFER VALIDATION:** WebKit storage policy and D006 replication principles inform the acceptance matrix but do not supply product runtime PASS. Design Studio W121 requires exact execution rather than more speculative manifests. Marketing 438 retains PWA ads OFF. No other specialist's discipline was duplicated.

**CONTRADICTION:** `no-store` and explicit Cache API storage can coexist; “HTTP no-store means no offline cache” is false as a platform-level claim. Conversely, a working Cache API does not guarantee durable owner records. `STATUS.md`'s old catch-all Hosting statement is superseded by current `firebase.json`. Chrome bfcache changes make categorical “no-store disables bfcache” assertions outdated.

## 7. OPEN / DEPENDENCY / CHANGE WATCH / STOP CHECK

**OPEN:** current NORMAL archive, exact source-to-deploy custody, Firebase response policy and CDN behavior, browser Cache API experiment, current Chromium/Safari worker update and bfcache, managed iPad, actual flight records, `.lbk` restore, Sync and remote authority. **Production validation OPEN; PWA release HOLD.**

**DEPENDENCY:** Software Engineering owns product CI/build/source changes and actual runtime; Web Manager owns web-specific header/Worker/Hosting admission. Product repo was read-only. Design Studio W121, Engineering D006 and Marketing 438 were read as bounded transfers.

**CHANGE WATCH:** RFC 9111/Service Worker, Firebase Hosting cache/header policy, Chrome bfcache `no-store` behavior and enterprise overrides, Safari/WebKit storage/eviction and iPadOS installed-context policy, Flutter generated bootstrap, GitHub artifact handling.

**Adjacent-question check:** The next high-value question is exact Firebase/Chrome/Safari execution of the sealed NORMAL artifact, not another synthetic header permutation. Security response headers/CSP would be a separate major-domain investigation and cannot be safely “fixed” without current generated runtime evidence.
