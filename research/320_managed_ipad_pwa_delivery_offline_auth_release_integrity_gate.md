# 320 — Managed-iPad PWA Delivery, Offline Durability, Auth Isolation & Release Integrity

**Gate:** PASS for generic/source-bounded integration only; **normal LogMate release build, served browser, Firebase/Auth, Safari/Home Screen, physical managed iPad, recovery and production validation OPEN**.
**Evidence date:** 2026-10-09 (Asia/Seoul). **Canonical Web Manager source:** `yhappcom/web-manager@fc2c4a0f4e0b5b57f545ceea849fffcb4fd41f55`. **Product source:** `yhappcom/logmate@7f359193dd0a378fb7ca047267ceaa0aae8ddcfd`, declared `1.0.0+1`; this is **main, not proven deployed production**.
**Owner:** Track E (architecture/security/operations). Track A supplies browser/origin/storage/Service Worker mechanics; B owns install/offline/recovery task semantics; C owns independent verification/accessibility; D owns search/measurement/privacy boundaries. Web Manager coordinates, not a sixth specialist. **Dependencies:** 290–293, 308–312, 315–319. The full exploratory working dossier is not a substitute for canonical, independently validated product evidence.

## HISTORY / PROBLEM → DESIGN PRINCIPLE

An icon on a company iPad is not proof of offline function. AppCache's declarative cache model failed to give robust programmable request/update control; modern Service Workers and Cache Storage permit explicit behavior but shift correctness, update, integrity and eviction responsibilities to the application. Separate **permission to distribute → exact launch context → HTTPS/origin → worker scope/control → shell asset integrity → local transaction → storage durability → export/restore → network path → current server admission → receipt/convergence**. Each arrow is an independent evidence boundary. A Web Clip, Safari tab, manually installed Home Screen app, Shared iPad named session and Shared iPad temporary session are not interchangeable.

## SOURCE — authoritative, version-scoped

1. Apple Web Clips payload and restrictions: https://support.apple.com/guide/deployment/web-clips-payload-settings-depbc7c7808/web and https://support.apple.com/guide/deployment/restrictions-for-iphone-and-ipad-devices-dep0f7dd3d8/web . Web Clip/full-screen/Safari restrictions require exact policy inspection; `com.apple.webapp` allow/deny matters.
2. Apple Shared iPad security/deployment: https://support.apple.com/guide/security/shared-ipad-security-secd99f373ef/web and https://support.apple.com/guide/deployment/shared-ipad-dep9a34c2ba2/web . Temporary-session logout deletes session-local state; quota/eviction and named-session rules differ.
3. WebKit Safari 17.2 Home Screen behavior: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ . Cookie transfer at installation does **not** imply transfer of IndexedDB/other local storage. Do not generalize this manual-install finding to an untested MDM Web Clip.
4. WebKit Safari 26 Home Screen changes: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ . Launch/install affordance is not offline cache proof or MDM override.
5. W3C Web App Manifest: https://www.w3.org/TR/appmanifest/ ; Service Workers: https://w3c.github.io/ServiceWorker/ . Manifest `id` identifies an app, while worker control is defined by registration/scope; neither proves durable data or OS permission.
6. MDN storage/eviction: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria . `persisted()` is not backup or tested restoration.
7. Firebase Hosting reserved namespace: https://firebase.google.com/docs/hosting/reserved-urls . Firebase reserves `/__`; PWA navigation fallback MUST exclude it, independently of Hosting rewrite behavior.
8. Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config ; Flutter Web FAQ: https://docs.flutter.dev/platform-integration/web/faq . A catch-all SPA rewrite can return HTML 200 for a missing JS/WASM/font resource. Flutter documents an exclusion/real-404 pattern and notes newer Flutter no longer provides a managed caching worker by default.
9. Firebase Hosting preview and version clone: https://firebase.google.com/docs/hosting/test-preview-deploy and https://firebase.google.com/docs/hosting/manage-hosting-resources . Preview URL is not a private access boundary; backend coupling must be explicitly fenced. Clone can preserve tested Hosting content/config, not installed-client state.
10. HTTP caching: https://www.rfc-editor.org/rfc/rfc9111 ; Cache Storage: https://developer.mozilla.org/en-US/docs/Web/API/Cache . HTTP freshness, Cache Storage entries, installed worker versions, local DB and remote authority are separate state machines.
11. Firebase Authentication web persistence and Flutter user state: https://firebase.google.com/docs/auth/web/auth-state-persistence and https://firebase.google.com/docs/auth/flutter/manage-users . Authentication initialization, cross-tab change, locally owned data and remote authority require explicit identity-bound gating.
12. Firebase restore-in-place: https://firebase.google.com/docs/firestore/restore-in-place . Old offline writes can return to a restored database under the same ID; account retirement and current admission must survive the rollback failure domain.

## CANONICAL LOGMATE SOURCE CONTRACT — verified at the pinned main ref

- `firebase.json` (`dfa9aa132acca6f69ea032b838bdbb0640e08bbf`) serves `build/web`, rewrites `/auth`, `/auth/`, `/auth/action` to `/auth/action/index.html`, then uses a `** → /index.html` fallback. It applies `Cache-Control: no-cache, no-store, must-revalidate` globally. There is **no explicit missing-asset exclusion**. Existing static files may be served correctly; absent compiled resources may receive HTML fallback. This is a **source-derived failure possibility, not an observed deployed response**.
- `web/manifest.json` (`8225e76fe032e792c30b0f22efa1f7cafab68119`) uses `start_url: "."`, `display: standalone`, `orientation: portrait-primary`, but no explicit `id` or `scope`. Future start-path changes can alter default app identity; portrait-only preference must be tested against tablet/EFB landscape requirements. Multiple installations are not automatically one IndexedDB ledger.
- `pubspec.yaml` (`6f4844c113cf4bb3ad8738b9b65423d7346903f8`) requires Dart `^3.12.0`, declares local Roboto/RobotoMono fonts, but not `NotoSansKR-wght.ttf`. `tool/verify_pwa_artifact.dart` (`83382ee7ffbd99103f959b7741763a14fbf2db05`) explicitly requires that CJK fallback. **Verifier/build contract mismatch**, unless an independently documented build injection supplies it.
- `.github/workflows/data001-pwa-artifact-validation.yml` (`0db21694ac330ab1e1142a36531364791b610a7e`) pins Flutter 3.38.7 and its automatic push trigger to `feature/data001-domain`; `core-product-validation.yml` pins Flutter 3.47.5 but is manual. The older PWA job toolchain does not satisfy the current Dart floor; no inspected automatic `main` normal-release PWA gate closes this.
- `Makefile` (`87b588874923afa829203269368f1b907101035f`) defines `build-pwa` and acceptance-harness `build-pwa-acceptance`. `tool/precache_flutter_web.dart` (`9661005786b72546b81479ec764f6ffd0c434f24`) expects the **legacy generated `RESOURCES`/`CORE` worker format**, rewrites query handling to strip **all** query strings and adds `ignoreSearch: true` to one cache lookup. This is not a generic modern Flutter worker migration. Exact generated bytes and sensitive-route exclusion remain unverified. `verify_pwa_artifact.dart` verifies file presence/markers, not live served response digest, MIME, auth exclusion or physical offline function.
- `web/auth/action/index.html` is a dedicated account-action document. Reset/verification links can contain action-bearing query parameters. Do not cache, normalize or substitute app shell for these URLs. Firebase `/__/*` helpers are a separate reserved server namespace, not protected merely by custom `authDomain`.
- Existing `SessionGate` / Sembast code merits implementation-level tests for **current authenticated UID = authorized local owner UID** across initial restoration, A→B cross-tab switch, overlapping asynchronous completions, partial owner initialization and offline reopen. Static execution-order counterexamples are hypotheses; no runtime data exposure has been demonstrated. Local owner transactions supply some positive protection and must not be ignored.
- Existing account-deletion page and shipped Settings route were contradictory at the 319 source checkpoint; revalidate against exact released product. Neither a public instruction nor Firebase identity deletion proves all active, derived, nested, backup and offline domains erased.

## SYNTHESIS / CONTRADICTION — independent planes

**C1 — installation:** App Store restriction ≠ Safari restriction ≠ Web Clip permission. Apple guidance about Safari hidden/full-screen Web Clip and guidance about disabling Use Safari may concern distinct settings; the exact OS/MDM payload and physical observation are required. No universal launch conclusion.

**C2 — storage:** Safari-origin IndexedDB ≠ Home Screen installed storage ≠ managed Web Clip storage ≠ Shared iPad session state. Storage persistence grant ≠ backup; cache shell availability ≠ unique flight-record durability. A temporary Shared iPad session is unsuitable as the **sole** store of irreplaceable unsynced records absent an independent verified recovery path.

**C3 — caching:** HTTP `no-store` is a browser/intermediary cache instruction; it is not evidence that an explicit Service Worker Cache Storage implementation is correct, complete or absent. Global no-store is a deliberate conservative freshness setting, but may increase repeat network cost and is not a substitute for an explicit asset-specific versioning/update plan. `200 OK` or `response.ok` does not prove correct JS/WASM/font content. Worker control, HTTP response, Cache Storage, app data and server admission require separate oracles.

**C4 — identity:** Manifest app ID ≠ worker scope ≠ origin ≠ Firebase UID ≠ Sembast ledger owner. Default manifest ID may change with start URL; installed contexts can diverge. Auth initialization/currentUser checks and cross-tab changes require a single latest identity-bound decision. A stale async result cannot reopen an older owner's view.

**C5 — release:** source SHA ≠ build SHA ≠ preview Hosting version ≠ live bytes ≠ installed worker/cache version ≠ local schema version. A preview URL is a different origin and cannot prove production-origin IndexedDB continuity. Preview can contact live backend resources unless fenced. Hosting rollback does not restore local data or legitimate predecessor remote authority.

**C6 — sync:** local saved ≠ queued ≠ sent ≠ remote accepted ≠ reconciled ≠ backed up. Online transition does not authorize old operations after account deletion, credential revocation or PITR. Direct unattended iPad↔native background sync/hotspot/discovery is **OPEN**, not a supported design assumption.

## MINTTAP DECISION — release acceptance ladder (proposed, not certified)

| Gate | Independent evidence required | Current disposition |
| --- | --- | --- |
| G0 Source/toolchain | exact main/release SHA, lockfile, compatible Flutter/Dart, normal vs acceptance mode, complete asset/route inventory | OPEN: PWA workflow toolchain mismatch |
| G1 Build | normal `build-pwa` exact output, CJK/local fonts, CanvasKit, own Service Worker, artifact path+SHA256+type+size | OPEN: font and legacy worker assumptions |
| G2 Hosting emulator | real positive app/auth/`/__` responses and negative missing JS/WASM/font/worker/manifest = 404, not HTML 200 | OPEN: catch-all rewrite |
| G3 Preview | isolated backend/test accounts, exact response status/MIME/body digest, OAuth redirect and public URL exposure controls | OPEN |
| G4 Live promotion | same tested Hosting version or explicit byte equivalence; served live critical file hashes and rollback plan | OPEN |
| G5 Browser/runtime | active/waiting worker, legacy registration retirement, cache hashes, online→offline cold start, upgrade/rollback while edits pending | OPEN |
| G6 Local data/authority | UID/ledger-owner match, IndexedDB/outbox preservation, export/restore, current remote admission after rejoin/deletion | OPEN |
| G7 Managed fleet | exact iPadOS/hardware/MDM/Shared iPad profile, policy/launch/storage pressure/logout/OS upgrade and physical offline rejoin | OPEN |

**No gate G0–G7 is promoted to LogMate product PASS here.** Gate ownership: E sets release/security invariants, A specifies platform behavior, C supplies independent executable oracles, B provides truthful accessible states, D separates preview/live acquisition metrics. Software Engineering owns code/CI/Firebase emulator and Flutter integration tests; Design Studio owns reusable interaction/visual decisions; Marketing owns release/feature claims.

## VALIDATION — falsifiable suite (designed; not runtime executed)

**M01–M24 fleet matrix:** App Store vs Safari/Web Clip restrictions, `com.apple.webapp` allow/deny, full-screen, content filter/proxy/TLS, first install/cold offline, process kill, pressure/eviction, Safari↔installed separation, remove/redeploy, named/temporary Shared iPad logout, long-offline queued return, PITR/import, accessibility/AT, OS/MDM update.

**Auth/owner cases:** auth initial null→restored UID, A→B and A→B→A cross-tab changes, overlapping async completion, remote reject, network loss, local owner transaction partial failure, error message claiming no mutation, protected Home reentry and current-UID check. Existing widget tests with injected startup decisions do not prove live Firebase/Sembast behavior.

**Hosting/worker negative cases:** missing JS/WASM/font returns real 404; correct MIME and digest; auth action query survives; Firebase `/__` bypasses worker; unknown extensionless path fails closed; `ignoreSearch` cannot collapse sensitive actions; old controller and new controller coexist safely; waiting update preserves unsynced local edits; rollback retains current server authority.

**MODEL-ONLY RESULT:** Local deterministic route-classifier `pwa_release_route_contract_model_20261009.py` evaluated **18/18 assertions PASS** on 2026-10-09. This proves only that the *proposed path classifier* matches its cases; it does not execute Firebase Hosting rules, Service Worker, OAuth, iPad or real product. It is **not** G2 or G5 evidence.

## TRANSFER VALIDATION / RELATED DOMAIN CHECK

- Design Studio `research/web/W103-logmate-synthesis-runtime-transfer-and-evidence-promotion-gate.md` and `W117-candidate05-production-promotion-packet.md`: static render, Flutter widget, served browser, independent engine, reflow/forced colors, screen reader, physical iPad and representative human are different evidence tiers; Web Stage 3 remains PRACTICE/NOT PASS.
- Software Engineering Studio `research/systems/S007_logmate_auth_onboarding_integrated_product_contract_2026-09-24.md` and `research/README.md`: product Auth/owner/deletion implementation belongs there and in LogMate; Web Manager transfers web-specific trust/routing/installation acceptance, not implementation code ownership.
- Marketing Manager current status and claim governance: no offline, secure synchronization, account deletion, device support or installability claim is promoted from source/model-only evidence.
- Track D: preview analytics are not live acquisition, Service Worker registration is not proof of install/retention, and auth action query/UID/flight payload must not enter analytics.

## OPEN / CHANGE WATCH / NEXT CHECKPOINT

**OPEN:** 320 physical fleet policy contradiction, exact compatible Flutter build, CJK font, custom worker ownership, reserved auth namespace, missing-asset 404, served digests, preview backend isolation, install identity, Safari/Web Clip local separation, offline persistence/export, owner-auth races, rejoin/idempotency, deletion/recovery and real screen-reader/human tests. Production validation remains OPEN. **CHANGE WATCH:** Flutter worker retirement/build toolchain, Firebase Hosting rewrites/preview/clone, W3C worker/manifest, WebKit install/storage/MDM behavior and Auth provider redirects.

**Next major checkpoint:** establish an exact current-head **normal (non-acceptance) PWA build** with compatible toolchain, owned worker and complete offline fonts; run Hosting Emulator negative routing and served-byte tests; then preview/live exact-version promotion and independent Safari/managed-iPad data-preserving execution. Do not treat a local model or source audit as production PASS.
