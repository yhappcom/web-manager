# 321 — Stage 8 PWA Auth-Action URL Capability, Referrer Boundary & Release Evidence Gate

**Evidence checkpoint:** 2026-10-10 (Asia/Seoul). **Owner:** Track E; Track A owns browser/referrer/worker mechanics, C owns independent executable oracles, B owns user-facing action/recovery states, D owns privacy-minimized measurement. Web Manager coordinates, not a sixth specialist.
**Gate:** PASS for generic standards and pinned-source diagnosis ONLY. **Live action-code exposure, current-head normal PWA build, Firebase Auth E2E, Safari/managed-iPad, production validation: OPEN.**
**Canonical baseline:** yhappcom/web-manager main b045366b9d6ccfcfa5947e63efcc3f623a7bccda (AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md, 318–320 and recent commits checked). **Product baseline:** yhappcom/logmate main 827a7deed162bf525313c6b4b9d244e56828a1c1 (not asserted deployed). Design Studio W103/W117, Engineering S007/M006 and Marketing status consumed as bounded transfer.

## HISTORY / PROBLEM → PRINCIPLE → STANDARD

Firebase action URLs contain a one-time out-of-band code in the query. The initial document GET and the subsequent JavaScript SDK mutation are separate events; a GET-only link checker is not the same as a JavaScript-executing visitor. A page's same-origin subresource requests, address/history, server access logs, analytics, caches and error reports are independent places where URL capabilities might propagate. Treat the code as a secret capability until redeemed/expired, without claiming any observed leak.

**SOURCE (primary/current, checked 2026-10-10):**
- Firebase custom action handler: https://firebase.google.com/docs/auth/custom-email-handler — verifyEmail, recoverEmail, resetPassword, one-time oobCode, continueUrl, lang, API-key rotation caveat; provider examples can automatically apply verify/recover codes.
- Referrer Policy standard: https://www.w3.org/TR/referrer-policy/ ; MDN current behavior: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy — default strict-origin-when-cross-origin sends the full path/query for same-origin subresource requests, but only origin for HTTPS cross-origin requests.
- Firebase Hosting custom headers/rewrites: https://firebase.google.com/docs/hosting/full-config ; Firebase reserved URLs: https://firebase.google.com/docs/hosting/reserved-urls .
- OWASP Forgot Password Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html — token URL/referrer protection; OWASP advice is defense-in-depth, not product incident evidence.
- Service Worker specification: https://w3c.github.io/ServiceWorker/ ; Flutter Web FAQ: https://docs.flutter.dev/platform-integration/web/faq ; Apple/WebKit Home Screen version-scoped evidence in research/320.

## SOURCE — pinned LogMate implementation and current CI provenance

1. web/auth/action/index.html blob 39d06a633ab7bee719b3401bc3ac744f8ba175d0 parses location.search mode/oobCode, imports Firebase JS 11.10.0 from gstatic, calls start() at load. verifyEmail and recoverEmail immediately call applyActionCode; resetPassword first calls verifyPasswordResetCode, then confirmPasswordReset only after explicit password form submit. There is no source-level referrer meta, URL scrubbing with history.replaceState, or page-specific CSP meta. This does not prove a link scanner executes JS.
2. firebase.json blob dfa9aa132acca6f69ea032b838bdbb0640e08bbf sets only global Cache-Control: no-cache, no-store, must-revalidate; /auth/action has a dedicated rewrite followed by ** catch-all. No explicit Referrer-Policy/CSP/nosniff or missing-static 404 exclusion appears in this pinned config. Deployed headers may differ: current-run live revalidation was unavailable.
3. .github/workflows/data001-pwa-artifact-validation.yml blob 0db21694ac330ab1e1142a36531364791b610a7e pins Flutter 3.38.7, push branch feature/data001-domain, and builds only make build-pwa-acceptance. Makefile blob 87b588874923afa829203269368f1b907101035f separately defines normal build-pwa. Core Product Validation blob 15e06583a51b20c7e5c80653877262a0c3e63b80 pins Flutter 3.47.5 but is workflow_dispatch. This is a release-evidence coverage gap, not proof a current build failed.
4. GitHub Actions read-only listing checked 2026-10-10: latest 20 visible LogMate runs were created no later than 2026-10-07 and had head SHAs different from current main 827a7dee. The most recent listed Core Product Validation run 37610113951 failed at SHA 1106e9ee; its failure cannot be attributed to current main without logs/commit lineage. No current-main normal PWA acceptance run was evidenced by that listing.
5. tool/precache_flutter_web.dart blob 9661005786b72546b81479ec764f6ffd0c434f24 expects legacy RESOURCES/CORE worker and applies ignoreSearch; tool/verify_pwa_artifact.dart blob 83382ee7ffbd99103f959b7741763a14fbf2db05 checks marker/resource presence, not live action-route isolation, browser referer or offline data preservation.

## SYNTHESIS / CONTRADICTION

**R1 — same-origin token propagation:** without an explicit referrer policy, modern default behavior permits a same-origin image/font/static request to carry the action page's full query as Referer. The source has same-origin favicon/font links. Whether those exact requests were sent with an actual code, whether the hosting access logs retain Referer, or whether anyone received the code is UNKNOWN. The external gstatic import must NOT be alleged to receive the full query under the default cross-origin policy.
**R2 — temporal ordering:** a JavaScript history.replaceState after module imports/asset fetches cannot retroactively prevent earlier Referer headers or erase the initial document GET from server logs. A response-level Referrer-Policy: no-referrer on the action document protects requests before JS; early URL cleanup can further reduce history/screenshot/support exposure but requires preserving the code in memory for the pending SDK call. Logging must independently redact the initial request URI and sensitive query parameters.
**R3 — automatic action:** Firebase examples themselves auto-apply verify/recover; this is not by itself a violation. A JS-executing link visitor could invoke the action without a human click; real scanner behavior, Firebase code reuse/expiry and product risk require isolated emulator/test accounts. A GET-only crawler cannot invoke applyActionCode simply by fetching HTML.
**R4 — worker/cache:** never cache action-code documents, normalize action-code query strings, replay action SDK requests from offline queues or rewrite /__ Firebase reserved routes to an app shell. A Worker with no fetch handler is not evidence that other clients or installed contexts have no Worker.
**R5 — evidence chain:** successful artifact markers, a historical CI run, an icon/manifest and a 200 HTTP response do not prove exact-current-head normal build, deployed bytes, installed worker, data durability or authorization. Existing research/320 release gates G0–G7 remain OPEN for production.

## MINTTAP DECISION — proposed engineering handoff (not shipped)

- For /auth/action and its resolved HTML route: explicit Referrer-Policy: no-referrer; Cache-Control: no-store; noindex; query/code redaction in request/access/analytics/CSP-error/support telemetry; route-scoped CSP evaluated first in Report-Only with privacy-safe reporting and actual Firebase module/connect dependencies.
- Do not apply a global restrictive CSP blindly to Flutter WASM, Firebase OAuth helper /__, or gstatic-loaded inline-module action code. Enforce only after exact browser/SDK tests.
- Separate online-web and offline-EFB-PWA release contracts. Require current-head normal build provenance, exact served bytes/status/MIME/digest, static negative 404, Worker control and update coexistence, local owner/outbox/schema preservation, and independent managed-iPad acceptance.
- Avoid changing the product or deleting user state as part of research; Engineering owns implementation. This document is a requirements/evidence handoff.

## VALIDATION — falsifiable matrix and honest evidence tier

**Static/source confirmed:** auto-apply for verify/recover vs form-submit reset; no explicit auth-action referrer header/meta; catch-all Hosting rewrite; CI trigger/toolchain/acceptance-mode gap. **Not confirmed:** real code leakage, link scanner execution, deployed auth success, current-head build failure, managed-device behavior.

**Proposed executable cases (OPEN):**
1. Synthetic action URL with a nonsecret sentinel: capture same-origin Referer under default, no-referrer and origin-only policies; compare a header delivered before resources with late history.replaceState. Verify initial document request URI still contains sentinel and access logs redact it.
2. Auth Emulator test accounts: GET-only scanner, JS-capable visitor, duplicate tabs, verifyEmail, recoverEmail, resetPassword, expired/used codes, network interruption and localized/continueUrl variants. Require current state and error UX evidence, not just SDK promise resolution.
3. Hosting Emulator: dedicated action route and /__ helper, real 404 for absent JS/WASM/CSS/fonts, correct MIME/nosniff, valid SPA navigation, CSP Report-Only then enforced; test redirects/trailing slashes and resource referrers.
4. Exact normal PWA artifact: build SHA/toolchain/asset inventory; clean vs upgraded worker; offline reopen and pending edits; local UID/owner and v14→v15 preservation; no token caching, no /__ interception; iPad Safari vs Home Screen vs MDM Web Clip separate.

**Execution blocker this run:** a locally hosted synthetic Chromium/Playwright loopback fixture was prepared, but page navigation returned net::ERR_BLOCKED_BY_ADMINISTRATOR. It is NOT a browser PASS or product FAIL. Source/spec reasoning remains the only new referrer evidence; do not bypass environment policy.

## CROSS-TRACK ALLOCATION / TRANSFER VALIDATION

- E highest-risk bottleneck: action capability confidentiality, route headers, CI/release attestation, rollback, account-deletion authority.
- A prerequisite: referrer default/scope, Service Worker navigation and Cache Storage, installed Safari storage identity; standard ≠ Chromium ≠ WebKit ≠ MDM policy.
- C execution dependency: independent browser + Hosting/Auth Emulator, negative oracles and physical iPad; no inferred runtime PASS.
- B: verify/recover/reset state clarity, expired/used/temporary failure and no destructive local-reset instruction; Design Studio W103/W117 are PRACTICE, not product promotion.
- D: no oobCode/full URL/UID/flight data in analytics; no public offline/install/sync claims without exact artifact/device evidence; Marketing retains broader claims ownership.
- Engineering S007 retains product identity/onboarding/owner semantics and implementation ownership; Web Manager does not duplicate SDK coding discipline.

## OPEN / DEPENDENCY / CHANGE WATCH / NEXT CHECKPOINT

OPEN: actual Hosting header rollout, live Referer traces, authorized Firebase emulator action semantics, link-inspection actor behavior, CSP module/connect compatibility, current-head CI, exact PWA artifact, Safari/MDM, offline record preservation and native Sync. CHANGE WATCH: Firebase email handler/SDK, Hosting reserved URLs, Chromium/WebKit referrer policies, Flutter Worker lifecycle and iPadOS Home Screen/MDM behavior. **Production validation remains OPEN.**

**Before-close adjacency check:** source CI and auth-route analysis was completed in the same bundle. Further meaningful progress requires permitted browser/Hosting/Auth Emulator access and Engineering-owned normal PWA artifact; no additional generic primer would close those gates.
