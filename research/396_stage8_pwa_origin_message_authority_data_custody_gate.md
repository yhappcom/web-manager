# 396 — Stage 8 PWA Origin Trust, Worker Message Authority and Managed-Context Data Custody

**Checkpoint:** 2026-10-17 Asia/Seoul. **Canonical intake:** `yhappcom/web-manager/main@47857fc1b53953be73b7d442bc43821d4aae9906`. **Read-only product source:** `yhappcom/logmate/main@241fdb50ad0458913cfae2cf583864b8d96cde94`. **Gate:** SOURCE/SYNTHESIS and 20/20 pinned-source assertions PASS only; actual built Worker/Hosting/Chromium/Safari/managed-iPad/runtime/data/sync evidence OPEN; PWA release HOLD. **Owner:** E; A owns browser scope/control/message mechanics, C negative execution, B recovery/install UX, D discovery/privacy-safe observability. Web Manager coordinates.

## HISTORY / PROBLEM → PRINCIPLE → STANDARD

AppCache's declarative model could not safely express modern update/offline policy; programmable Service Workers introduced distinct **registration scope, client control, fetch interception, message command, Cache Storage and release authorization** boundaries. A handler returning without `respondWith` only declines to substitute a fetch response; it does **not** move the page outside the Service Worker registration's scope or create a new web security origin. Path-based routing is not an origin-isolation boundary.

**SOURCE, consulted 2026-10-17:**
- W3C Service Workers Candidate Recommendation Draft (2026-09-17): https://www.w3.org/TR/service-workers/ — registration/control/fetch/message are separate mechanisms; the draft is not uniform platform support proof.
- MDN ServiceWorkerRegistration: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration — active Worker controls in-scope clients.
- MDN ServiceWorkerGlobalScope message: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/message_event — pages can message active Workers; message dispatch is separate from fetch response substitution.
- MDN ServiceWorkerGlobalScope fetch: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/fetch_event — `respondWith` determines response substitution.
- MDN ServiceWorkerContainer.getRegistration: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/getRegistration — in-scope registration can be discovered by a same-origin client.
- WHATWG Storage https://storage.spec.whatwg.org/ and WebKit storage policy (2023-08-10) https://webkit.org/blog/14403/updates-to-storage-policy/ — origin/bucket/quota/eviction and persistence are not independent backup.
- WebKit Safari 17.2 https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ and Apple managed Web Clips https://support.apple.com/guide/deployment/depbc7c7808/web — installed-context storage and MDM launch affordances require separate device evidence.

## SOURCE — pinned current LogMate (not production)

- `web/index.html` (Flutter base-href placeholder) and `web/flutter_bootstrap.js@a70625e8bda32aafd5dd23822c017d05229f0e63`: registers `logmate_service_worker.js` with `scope: logmateBaseUrl.pathname`, `updateViaCache: 'none'`. If the generated build base is `/`, the resulting registration scope covers `/auth/action`, `/about`, `/support`, `/privacy`, `/terms` and the app root. **Generated exact base and actual control must still be observed.**
- `tool/pwa_precache.dart@90a67954af618a4e18199fa92555491c56167c17` generates the Worker. `fetch` bypasses `auth`, `auth/`, and Firebase `__/` by returning without `respondWith`; navigation shell substitution is root-only. This is a positive **fetch-routing** restriction, **not** a page isolation or message-authorization rule.
- The same Worker has an `message` listener dispatching `GET_STATUS`, `VERIFY_CACHE`, `START_PRECACHE`, `REPAIR_CACHE`, `PROMOTE_VERIFIED_CANDIDATE`, and `ROLLBACK_TO_PREVIOUS` based on `api` and `type`; no explicit `event.source` URL/client-role check or per-command resource budget is visible. Promotion rechecks verified bytes, and rollback explicitly replies `NOT_ROLLED_BACK`; do **not** describe rollback as remotely executable or promotion as bypassing verification.
- `web/auth/action/index.html@39d06a633ab7bee719b3401bc3ac744f8ba175d0` executes Firebase `gstatic` ES modules and reads `oobCode` from the URL. The page contains **no** `navigator.serviceWorker` call. There is no evidence of a malicious script or actual message abuse. A future compromised/injected same-origin script is the conditional threat.
- `firebase.json@9ac0972e26749215c4a718360c66315c6caf3cc8` has global HTTP no-store and three Auth rewrites; no explicit CSP or Referrer-Policy. **Actual served headers remain unobserved.** Four inspected public pages (about/support/terms/privacy) contain no `<script>` tag. A static page today is not a permanent guarantee against future third-party additions.
- `web/manifest.json@8225e76fe032e792c30b0f22efa1f7cafab68119` has `start_url: "."` and `display: "standalone"`, but no explicit `id` or `scope`; manifest identity is not Worker scope and neither migrates IndexedDB.
- `research/324_stage8_pwa_release_evidence_ci_route_policy_20261011.md` remains the canonical release-evidence integration. Historical branch and current main differ; earlier generic/source studies are not evidence of current production behavior.

## SYNTHESIS — four non-equivalent boundaries

**B1. Fetch bypass != scope exclusion.** A root-scope Worker can still control an Auth page even if its `fetch` handler does not intercept Auth navigation. A controlled page can reach its controller; an in-scope same-origin page may also obtain a registration/active Worker handle. Test actual browser behavior, do not infer it solely from the template.

**B2. Scope exclusion != origin isolation.** A page on the same origin can use the origin's IndexedDB and Cache Storage according to web security rules regardless of its URL path. Script loaded from `gstatic` as an ES module runs with the embedding document's page authority, not with an isolated `gstatic` storage principal. This is a **trust exposure**, not proof Firebase's modules are unsafe or that LogMate data were accessed.

**B3. Message acceptance != remote release authority.** API version checks are protocol compatibility checks, not user/role/route admission. The Worker does verify candidate integrity before promotion and currently fails rollback closed. A compromised same-origin script could still trigger expensive verification/repair or promotion of an already verified candidate, affecting operational availability/timing. No cross-origin unauthenticated exploit, bypass of digest checks, user-data deletion, or incident is established.

**B4. Same origin != same installed storage container.** Safari tab vs Home Screen app may have separate local data despite a common domain; MDM Web Clip and Shared iPad require policy-specific testing. Origin separation can reduce future public marketing/third-party-script exposure, but moving the **offline PWA origin** is a data-custody migration, not a harmless DNS change. The same Firebase UID, icon or manifest ID does not copy an unsynced ledger.

## MINTTAP DECISION (proposed, not shipped)

1. **Preserve the current PWA origin** until a tested owner-bound, lossless export/import or server-confirmed reconciliation proves unique offline records survive. Do not delete/reinstall, clear site data, rotate the PWA origin or treat MDM redeployment as routine repair.
2. **Evaluate a separate public marketing origin** if advertising/analytics/third-party JS is introduced. Keep the sensitive Auth action and Firebase redirect compatibility in a dedicated review; do not casually move Auth endpoints or assume cross-origin session/redirect continuity. Marketing research 438 currently proposes an ad-free PWA; this is a proposal, not proof no future third-party code will exist.
3. **Engineering-owned Worker message hardening:** classify read-only status vs expensive verify/repair vs release-changing promotion. Validate message schema, source client URL/context where feasible, bound/coalesce expensive work, protect concurrent control-catalogue updates, and require verified candidate/release/data-compatibility evidence. Source URL validation is defense in depth, **not** a cure for same-origin XSS. Avoid a secret embedded in client JS as a purported authorization root.
4. **Auth action confidentiality:** evaluate `Referrer-Policy: no-referrer`, no-secret URL telemetry, safe URL cleanup before optional subresource loads, and CSP appropriate to actual Firebase module/connect flows; do not deploy untested restrictive headers. This follows the prior local study 392 but remains a live-header/browser validation question.
5. **Keep deployment authority and data custody independent:** SHA-256 verified body != trusted MIME/CSP; Worker activated != all clients upgraded; local save != server ACK; installed icon != offline durability; managed Web Clip != App Store-native persistence guarantees.

## VALIDATION — source assertions, adversarial matrix and evidence tiers

**Executed 2026-10-17:** 20/20 pinned-source assertions PASS, covering bootstrap scope/update settings, Worker Auth/`/__` fetch bypass, message API/commands, rollback fail-closed, lack of explicit sender-route check, Auth script/query, absence of Auth-page Worker calls, Hosting header omissions, manifest fields, and four public pages without script tags. **This is source text inspection, not a browser/Worker exploit or security penetration test.**

**T0 source gate:** preserve exact SHA/blobs, generated Worker/base href, final Firebase Hosting config, Auth HTML and any public third-party script inventory. Negative: stale branch/main or source/built mismatch.

**T1 disposable-origin browser gate:** in Chromium and Safari, register the exact Worker and navigate root, `/auth/action?mode=resetPassword&oobCode=FAKE`, `/privacy`, `/__`. For each record `controller`, matching registration, fetch intercept/network status, response headers and sanitized message response. Verify whether an Auth/public page can send a harmless `GET_STATUS` despite fetch bypass. Never use real codes or production user records.

**T2 command abuse and update gate:** on a **disposable** origin, issue bounded parallel `VERIFY_CACHE`/repair requests, measure CPU/time, memory, catalog mutation, quota and candidate promotion; include old/new Worker overlap and blocked/missing font. Negative: unbounded work, version mixing, stale control write, corrupt cached response, unsynced data deletion. Do not send repair/promotion messages to production.

**T3 sensitive-route/header gate:** inspect actual HTTPS `Referer`, CSP, MIME, missing JS/WASM/font 404, Firebase reserved namespace, action A/B query isolation and Worker control. Redact all query tokens.

**T4 custody/device gate:** use disposable owner-bound v14/v15 records and outbox in Safari tab, Home Screen and actual managed Web Clip separately; test offline cold start, long dormancy, storage pressure, MDM restrictions, app removal/reinstall, export/import, interrupted restore and remote ACK. Temporary Shared iPad sessions must not be the only repository of unique records. Physical iPad and independent restore are mandatory before promotion.

**Evidence tiers:** source/model -> exact normal artifact -> served HTTPS -> Chromium/Safari browser -> physical iPad per install mode -> managed fleet + actual backend/Sync. Never promote between tiers without an executed oracle. The previous 0/55 current-product browser/device matrix remains **NOT_EXECUTED**; no new release PASS.

## CROSS-TRACK / SPECIALIST TRANSFER

- **E (primary bottleneck):** origin boundary, message authority, Auth confidentiality, release/update and data-custody risk.
- **A (prerequisite):** scope/control/fetch/message distinctions, Cache Storage/IndexedDB partition and browser/OS divergence.
- **C (execution debt):** independent browser and physical-device negative tests, resource-budget and integrity/semantic recovery oracles. Software Engineering Q006 shows structural reopen != semantic recovery in a bounded SQLite crash test, not LogMate PWA PASS.
- **B (UX dependency):** distinguish local saved/queued/remote ACK, install-context migration, verified export/restore and update/repair blocked states; Design Studio W120/W121 Stage 3 remains PRACTICE/NOT PASSED, with exact runtime evidence prioritized.
- **D (privacy/discovery):** keep public SEO surfaces separate from app shell and action codes; no UID/oobCode/flight payload in analytics, and no install/offline/Sync claim from source/model evidence. Marketing 438 PWA-ad-free is conditional architecture, not installed enforcement.
- **CONTRADICTION:** the earlier 324's legacy Worker/catch-all Hosting descriptions were pinned to older product refs; current main uses a project-owned Worker and only explicit Auth rewrites. Historical analysis is retained, not silently overwritten.
- **CHANGE WATCH:** W3C Service Workers draft; Chromium/WebKit message/control behavior; WebKit installed storage/eviction; iPadOS/MDM/Shared iPad; Firebase Hosting/Auth; manifest install identity.

**Adjacency check:** scope, message authority, same-origin script exposure, Auth token confidentiality, public-origin strategy, installed storage custody and test execution are now integrated. More source-only microtests cannot certify the actual compiled Worker or managed-iPad safety. **Next checkpoint:** exact current-main normal artifact + disposable HTTPS Chromium/Safari + physical managed iPad + owner-data survival/remote authority evidence. **Production validation OPEN; deployment HOLD.**

**Canonical sync:** This integrated artifact consolidates a new cross-boundary finding and references previous working studies 385–395 without pretending their local files are on main. Do not increment a PASS label solely because this file is committed.
