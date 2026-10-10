# 323 — Stage 8 Service Worker Script Trust, Update-Cache Semantics & Offline Recovery Gate

**Evidence checkpoint:** 2026-10-11 (Asia/Seoul). **Primary owner:** Track E — web security, release/incident governance. **Track A:** browser Service Worker, CSP and HTTP/cache mechanics. **Track C:** independent executable quality and negative oracles. **Track B:** update/hold/recovery states. **Track D:** privacy-minimized diagnostics and release-claim discipline. Web Manager coordinates, not a sixth specialist.

**Gate:** **PASS — generic standards + pinned source diagnosis only.** **OPEN:** exact current-head normal PWA build, generated bootstrap/worker, HTTP responses, browser CSP/update behavior, migration/restore, installed Safari, MDM Web Clip, physical iPad and production. No shipped change or incident is inferred.

**Canonical refs checked:** Web Manager `main@c10bbc17f0e826435e63692e8abf47b931ee6444`, including AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research index and 318–322; LogMate `main@827a7deed162bf525313c6b4b9d244e56828a1c1`; Design Studio W103/W117 (runtime transfer **OPEN**), Engineering S007 (UID owner authority; product runtime **OPEN**), Marketing STATUS (2026-10-09; public claims require separate evidence). This is a web-specific handoff, not an Engineering implementation decision.

## 1. HISTORY / PROBLEM → PRINCIPLE

AppCache's declarative application cache could trap applications in difficult-to-recover stale states. Service Workers make request interception and offline resources programmable, but thereby create a persistent, privileged origin component. A Worker that is trusted to answer navigation requests can preserve availability and can also perpetuate a bad shell or intercept sensitive same-origin routes. Its script delivery, script update, activation, Cache Storage and local user-data durability are **different state machines**.

**Principle:** a PWA release is not trusted merely because its Worker registered, its page CSP passed, its cache contains files, or its offline screen rendered. Establish **script provenance → registration authority → Worker execution policy → versioned resource integrity → safe activation → local-data preservation → current remote admission** independently. During compromise, distinguish fixing fetch interception from restoring origin trust or reconstructing unique offline data.

## 2. SOURCE — primary standards and scoped implementation evidence (checked 2026-10-11)

1. **W3C Service Workers Nightly, Candidate Recommendation Draft dated 2026-09-17:** https://www.w3.org/TR/service-workers/ . §6.1 secure contexts; §6.2 CSP of the Worker **script response**; §6.3 origin/importScripts; §6.5 path restriction **not a hard security boundary**; §6.6 JavaScript MIME; Update algorithm checks main-script bytes and, for classic imported scripts, also compares stored vs fetched import bodies; update-via-cache modes affect network/cache behavior. This is a CR **draft**, not a final W3C Recommendation; implementation transfer remains separate.
2. **W3C CSP Level 3 Working Draft (2026-09-16):** https://www.w3.org/TR/CSP3/ . `worker-src` governs Worker/Service Worker script fetches from the registering document, with specified directive fallbacks. A document policy restricting registration is not the Worker execution policy.
3. **MDN `ServiceWorkerContainer.register()`:** https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register . Same-origin and secure-context constraints, scope/path, JavaScript MIME, `type`, `updateViaCache`, and the scriptURL injection sink/Trusted Types considerations. **The API has no `integrity` registration option.**
4. **MDN `ServiceWorkerRegistration.updateViaCache`:** https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache . `imports` (default) bypasses the HTTP cache for main Worker update checks but may consult it for imported scripts; `all` may consult for both; `none` bypasses for both. This option does **not** control ordinary app-resource Cache Storage or prove fresh authorization.
5. **MDN CSP workers:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy . Workers generally do **not** inherit the parent document CSP; serve CSP on the Worker script response for Worker execution restrictions.
6. **Chrome Workbox precaching:** https://developer.chrome.com/docs/workbox/modules/workbox-precaching . Workbox can attach optional `integrity` to precache-manifest entries, causing integrity verification for those resource fetches. **Workbox precache integrity is not an automatic browser-level SRI check for the registered Worker script.** Chrome-specific documentation, not a Safari guarantee.
7. **Chrome Workbox Worker remediation:** https://developer.chrome.com/docs/workbox/remove-buggy-service-workers . A same-script-URL no-fetch-handler replacement can remove buggy interception. `Clear-Site-Data: "storage"` is a dangerous alternative for origins with unique IndexedDB data (see 322).
8. **Firebase Hosting:** https://firebase.google.com/docs/hosting/full-config and https://firebase.google.com/docs/hosting/reserved-urls . Header rules apply to the **original request path before rewrite**. Firebase `/__` reserved helpers and auth flows must not be swallowed by SPA/Worker navigation fallback. Hosting source configuration is not evidence of actual served headers.

**CHANGE WATCH / old-source conflict:** The historical W3C Service Worker explainer at https://github.com/w3c/ServiceWorker/blob/main/explainer.md says imported scripts are not checked in an update. The **2026-09-17 CRD Update algorithm explicitly compares classic imported-script bytes** (§ Update, after main-script comparison). Treat the older explainer as stale for this claim; do not infer that all browser/OS versions implement the latest algorithm identically. Test `updateViaCache` and imported-script changes on each target engine.

## 3. SOURCE — pinned LogMate implementation facts and non-facts

**Read-only exact blobs at LogMate `827a7dee`:**
- `firebase.json` `dfa9aa132acca6f69ea032b838bdbb0640e08bbf`: one global `Cache-Control: no-cache, no-store, must-revalidate`, three `/auth` aliases, then `**` SPA rewrite. No configured CSP, `Referrer-Policy`, `Clear-Site-Data`, or path-specific Worker CSP. This does **not** establish actual live headers, proxy/CDN behavior or incident.
- `tool/precache_flutter_web.dart` `9661005786b72546b81479ec764f6ffd0c434f24`: expects legacy generated `RESOURCES` and `CORE`, converts `?v=` query handling into all-query stripping and injects `ignoreSearch: true` into one cache match. This postprocessor does **not** contain an explicit `/auth` or `/__` route guard. **Absence of a guard in this patch script alone does not prove the final generated Worker intercepts these paths**; the exact built Worker must be inspected and exercised.
- `tool/verify_pwa_artifact.dart` `83382ee7ffbd99103f959b7741763a14fbf2db05`: verifies legacy Worker markers, required resource strings, local fonts/CanvasKit and acceptance-harness isolation; does **not** verify served Worker CSP, `updateViaCache`, import integrity, actual Cache Storage bytes, offline navigation, owner-bound records or safe upgrade.
- `web/index.html` `01be77585ac40bf11e80777177a4ab08e4885671`: loads generated `flutter_bootstrap.js`. The generated bootstrap is **not present** in `web/` source; registration behavior must be measured on the exact built/served artifact, not invented from template HTML.
- `.github/workflows/data001-pwa-artifact-validation.yml` `0db21694ac330ab1e1142a36531364791b610a7e`: feature-branch-triggered acceptance build, Flutter 3.38.7, `make build-pwa-acceptance`; not a current-`main` normal-PWA release gate. `pubspec.yaml` requires Dart `^3.12.0`; this toolchain mismatch remains a source-level concern, not an observed fresh CI failure.

**Static assertion run:** 18/18 expected source assertions matched across the five blobs above (global no-store, catch-all, absent declared headers, legacy Worker dependence, query rewriting, absent patch-script route guards, marker-only verifier, generated bootstrap reference, feature-only acceptance CI). **Evidence tier: SOURCE only.** The assertions were not a browser test, build PASS, deployed response capture, safety proof or physical-device result.

## 4. SYNTHESIS — six non-substitutable trust planes

**T1 — registration eligibility vs executable bytes.** HTTPS/same-origin and valid JavaScript MIME are necessary for Worker registration. Document `worker-src 'self'` can constrain *where* registration loads from, but does not authenticate a particular revision of same-origin script bytes. Restrict scriptURL construction; avoid untrusted dynamic paths. `Service-Worker-Allowed` can expand scope, but scope/path is not a tenant or data-security boundary. A Worker with root scope can control app documents even if it cannot read the DOM directly.

**T2 — two CSP enforcement contexts.** The registering document's CSP `worker-src` controls whether a Worker can be created; the Worker **script response's** CSP constrains execution inside that Worker. Applying CSP only to `/index.html` or only to `/auth/action` is not proof that the Worker script receives a safe policy. Conversely, applying a global CSP without checking Firebase SDK/Auth and Flutter resources can break the app. Require route-specific captured responses and functional tests, not a blanket copied header.

**T3 — update freshness vs cache/data integrity.** `updateViaCache` selects how HTTP cache participates in Worker script/import update checks. It does not control app-resource Cache Storage, IndexedDB, remote authority or backup. Byte-difference update detection does not prove bytes came from the approved release. Content-hashed filenames, pinned build inventories and optional Workbox precache integrity protect different parts of the chain. A passing `Cache.addAll()` does not certify correct JS/WASM/font content or app execution (see 320–321).

**T4 — mixed generations and activation.** A new Worker may wait while old controlled clients remain. `skipWaiting()` and `clients.claim()` can shorten overlap but cannot prove that in-flight edits, Sembast owner-bound records, draft/outbox or schema migration are safe. Browser Worker activation ≠ data migration transaction ≠ remote policy admission. A release gate must test old-client→new-client, offline during install, interruption during migration, multi-tab overlap and rollbacks separately.

**T5 — Auth/helper routing.** A root-scope Worker can see in-scope navigations. The *final* fetch strategy must explicitly avoid caching or substituting shell HTML for action-bearing `/auth` links, Firebase `/__` helpers, account-specific endpoints, credentials and authorization-bearing responses. Preserve full query identity for sensitive URLs. Avoid global `ignoreSearch` or query-stripping outside a bounded immutable static-resource allowlist. **Do not infer actual interception from the current postprocessor alone.**

**T6 — incident containment and data survival.** A same-URL no-op replacement Worker may restore network fetch behavior but does not automatically prove origin trust after malicious hosting/dependency compromise. A destructive `Clear-Site-Data` reset may erase the sole unsynchronized ledger. A rollback to old Hosting bytes cannot reconstruct deleted IndexedDB or undo server-side account retirement. Separate (a) stop malicious interception, (b) establish approved script/release provenance, (c) quarantine unique local data with UID/provenance, (d) revalidate remote admission and (e) demonstrate actual restoration. An offline iPad may remain on an old Worker until connectivity/launch; never promise unattended convergence.

## 5. MINTTAP DECISION — proposed Worker release/incident contract (NOT SHIPPED)

**Release-preflight hold:** require an Engineering-owned **normal** PWA build from pinned source/toolchain, including generated bootstrap/Worker and all imports, SHA-256 inventory, resource MIME/size, explicit route policy, manifest, and local font/CanvasKit. Test Worker script request response status/MIME/CSP, document `worker-src`, declared registration scope/`updateViaCache`, imported-script version changes, cache asset digests and static-resource negative 404. Record source SHA, build hash, Hosting version, browser/OS, display mode, storage partition and prior Worker version.

**Promotion hold:** require disposable owner-bound IndexedDB fixtures, clean and upgraded registrations, saved edits/outbox, offline cold re-entry, expired action URL, Firebase `/__` helper behavior, schema migration interruption, safe update UX, and post-rejoin remote authority/receipt evidence. Promote one evidence class at a time. Browser-level pass on Chromium cannot certify WebKit, Safari tab cannot certify Home Screen, and Home Screen cannot certify MDM Web Clip/Shared iPad.

**Incident decision:** default to *non-destructive containment* when possible; do not use `Clear-Site-Data: "storage"` or `"*"` for routine logout, deploy or Worker fix. Verified compromise may justify exceptional destruction only with explicit incident authority, consequence analysis and tested owner-safe preservation/recovery path. Preserve unique local records without treating them as remotely authorized. A physical EFB device's offline usefulness and PWA↔native sync require independent evidence.

## 6. VALIDATION — falsifiable execution matrix (DESIGNED, NOT EXECUTED)

| ID | Independent test / failure oracle | Required evidence |
| --- | --- | --- |
| W01 | Normal exact build vs acceptance build, toolchain, no harness leakage | source/build/lockfile SHA, compiler and artifact |
| W02 | Missing Worker script and HTML-200 fallback | actual 404 or registration fails safely; no false install |
| W03 | Wrong Worker MIME or redirect | registration rejects; no app-shell masquerade |
| W04 | Document CSP `worker-src` denies unauthorized script URL | real registration error, no new Worker |
| W05 | Worker-script response CSP denies unauthorized import/fetch | real Worker policy behavior; Auth and offline still work |
| W06 | Header matching on `/flutter_service_worker.js`, `/auth` aliases and `/__` | served response capture per original URL |
| W07 | `updateViaCache: imports/all/none` under controlled HTTP cache | actual registration value and network trace |
| W08 | Change only classic imported-script bytes | new Worker observed or explicit engine contradiction |
| W09 | Change only main Worker bytes | waiting/active version provenance |
| W10 | Same URL, altered bytes / stale CDN response | block promotion on unapproved hash, independent of HTTP 200 |
| W11 | Missing JS/WASM/font with SPA rewrite | real 404, MIME/digest negative oracle |
| W12 | Full offline shell from exact artifact | restart and task operation, not screenshot alone |
| W13 | Root-scope Worker navigation to action URL with sentinel `oobCode` | no cached shell/token/query normalization; no raw diagnostic leak |
| W14 | Firebase `/__` Auth helper under Worker control | network helper works, not intercepted or cached |
| W15 | Old/new tabs and `skipWaiting` during dirty edit | draft/outbox/owner data intact; explicit user hold |
| W16 | Interrupted v14→v15 migration and offline re-open | same owner, full data, no unauthorized mutation |
| W17 | Same-URL no-op Worker recovery vs changed URL | fetch interception stops without unintended DB loss |
| W18 | Deliberate `Clear-Site-Data` on disposable test origin | per-engine storage/Worker/cookie effects; never real ledger |
| W19 | Account retired while iPad offline then reconnects | local quarantine preserved; obsolete remote effects denied |
| W20 | Chromium vs Safari tab vs Home Screen vs managed Web Clip | independent verdicts, not assumed parity |
| W21 | PWA↔native sync with network interruptions | distinct discovery, authentication, queue, ACK, convergence evidence |
| W22 | Privacy and accessibility of update/recovery states | no token/full URL/flight data in telemetry; keyboard/AT and locale checks |

**Verdicts:** `PASS/FAIL/UNKNOWN/BLOCKED` **per case and evidence tier** (SOURCE, BUILD, HOSTING, BROWSER, DATA MUTATION, PHYSICAL DEVICE, INCIDENT). Never aggregate a source-level pass into runtime/production PASS. Negative tests use synthetic action codes and disposable test accounts/origins only. No W01–W22 runtime PASS is claimed.

## 7. CROSS-TRACK TRANSFER / CONTRADICTION / depth allocation

- **E (primary bottleneck, highest allocation):** owns two-CSP-context release policy, approved Worker script/import provenance, incident authority, rollback and data-preserving remediation. Generic understanding now advanced; production/Engineering evidence remains the gate.
- **A (high prerequisite pressure):** owns scope, registration, `updateViaCache`, HTTP cache vs Cache Storage, import-update semantics, Safari/WebKit/OS differences. **CONTRADICTION resolved at source tier:** old explainer's "imports not checked" vs 2026 CRD imported-script comparison. **OPEN:** exact browser transfer.
- **C (highest execution pressure):** owns W01–W22 independent negative oracles; no source marker or Chromium-only result can certify offline integrity, accessibility or managed iPad.
- **B (transfer):** signed-out vs offline-usable, update waiting vs forced, locally saved vs remotely acknowledged, recovery required vs data erased. Consume Design Studio W103/W117 runtime ladder; no visual-only promotion.
- **D (transfer):** capture only sanitized release/Worker/route/version evidence, never auth query capabilities, UID or flight records. Search/indexing must distinguish public web documents from private installed PWA state; Marketing owns outward claims.
- **Engineering S007 (dependency):** owns product UID authority, Firebase/Auth implementation, exact Flutter build and migration harness. Web Manager owns the web-specific acceptance contract, not code changes to LogMate.

## 8. OPEN / DEPENDENCY / CHANGE WATCH / ADJACENCY CHECK

**OPEN:** generated bootstrap registration, `updateViaCache`, actual Worker imports and CSP, served header matrix, offline cache bytes, current-head normal build, Auth/Hosting emulator, physical iPad/MDM storage and recovery, native synchronization, privacy-safe telemetry, production incident validation. Product-specific decisions beyond the pinned source are not inferred.

**DEPENDENCY:** Engineering supplies a pinned normal build and disposable UID-bound v14/v15 fixtures; Hosting/Auth emulator and independent browser/physical iPad operators supply real traces. Do not mutate production users or deploy security headers based on this research.

**CHANGE WATCH:** W3C Service Workers CRD (2026-09-17), CSP3 (2026-09-16), imported-script update behavior across Chromium/WebKit versions, Flutter's Worker-generation behavior, Firebase Hosting header/rewrite rules, WebKit iPadOS Home Screen/MDM policy, Workbox integrity semantics.

**Before-close adjacent question check:** The adjacent distinction between `worker-src` and Worker response CSP, imported-script update freshness, source postprocessor's absent route exclusions, Workbox SRI boundaries, non-destructive incident recovery, and W01–W22 has been integrated here. The next information-gain step is **an exact normal PWA artifact plus executable negative tests**, not another primer. Stage 8 product/production validation remains OPEN.
