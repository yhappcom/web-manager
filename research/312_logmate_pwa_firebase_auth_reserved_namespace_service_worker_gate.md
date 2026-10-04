# 312 — LogMate PWA Firebase Auth Reserved-Namespace & Service-Worker Isolation Gate

Status: **PASS (generic/platform + canonical-source contract) / EXACT BUILT-WORKER + DEPLOYED OAUTH + SAFARI/HOME-SCREEN + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Evidence date: 2026-10-04  
Curriculum: Stage 8 Security / Privacy / Trust continuous expert application  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A Service Worker/browser mechanics; Track C runtime/failure validation; Track B auth/recovery UX; Track D auth funnel/diagnostic measurement

## Why this checkpoint exists

LogMate now configures the Web Firebase Auth `authDomain` as `logmate.minttap.app`, and the Google/Apple operational record configures the OAuth return path as:

`https://logmate.minttap.app/__/auth/handler`

That is directionally aligned with Firebase custom-domain guidance. It also creates a PWA-specific release dependency that must not be missed: Firebase Hosting reserves the `/__` namespace for Firebase services, including OAuth auth helpers, while LogMate's offline PWA uses a root-scoped Service Worker model. A Service Worker can intercept navigation and subresource requests within its scope before Hosting handles them.

Firebase explicitly warns PWA authors not to intercept the reserved `/__` namespace and says navigation fallbacks must exclude it.

Therefore a valid custom-domain OAuth configuration is not sufficient evidence that Google/Apple sign-in works in the installed/offline-capable PWA. The exact shipped Service Worker must preserve Firebase's reserved namespace.

## Canonical LogMate evidence read this run

Latest LogMate `main` at run time includes commits through `e408be3b5ec604547d44f0606b84f1d969c56f7f`.

Canonical source establishes:

- `DefaultFirebaseOptions.web.authDomain == 'logmate.minttap.app'`.
- `firebase.json` serves `build/web`, has explicit `/auth` email-action rewrites, and otherwise has a catch-all app rewrite.
- `docs/operations/federated-auth-providers.md` records Google custom-domain origin/redirect and Apple custom-domain/return URL as CONFIGURED, while provider runtime remains NOT VERIFIED.
- The current PWA build/verifier contract still requires `build/web/flutter_service_worker.js` and the full-precache/query-safe post-processing markers.
- The exact generated worker bytes for the current LogMate head were not available in repository source during this run, so its `/__` handling is **OPEN**, not inferred.

The recent OAuth/public-page/configuration commits are configuration/source evidence. They do not constitute deployed PWA/provider acceptance.

## Authoritative platform evidence

### SOURCE — Firebase Hosting reserved namespace

Firebase Hosting reserves URLs beginning with `/__`. Firebase Authentication uses that namespace to serve special HTML/JavaScript that completes provider OAuth flows.

Firebase's PWA guidance is explicit: if a Service Worker uses navigation fallback, fallbacks for `/__` must be disabled, and requests in that namespace should not be intercepted by the Service Worker.

Source: https://firebase.google.com/docs/hosting/reserved-urls

### SOURCE — Firebase custom authDomain

Firebase documents custom-domain OAuth for Google and Apple by:

1. connecting the custom domain to Firebase Hosting;
2. adding the custom domain to Firebase Authentication authorized domains;
3. registering the custom-domain `/__/auth/handler` with the provider;
4. setting Firebase `authDomain` to that custom domain.

Sources:
- https://firebase.google.com/docs/auth/web/google-signin
- https://firebase.google.com/docs/auth/web/apple
- https://firebase.google.com/docs/auth/web/redirect-best-practices

Firebase also documents that redirect auth can fail when the helper domain is cross-origin and browser third-party storage is blocked; using the app/custom domain is one supported strategy. This is a browser-storage reason for same-origin auth helper routing, not evidence that the PWA Service Worker is safe.

### SOURCE — Apple web return URLs

Apple requires registered web return URLs to be absolute and include scheme, host and path, and the web service must be associated through a Services ID.

Source: https://developer.apple.com/documentation/signinwithapple/configuring-your-environment-for-sign-in-with-apple

### SOURCE — Service Worker interception

A Service Worker registration scope defines the URLs it can control. Fetch events include page-navigation and subresource requests, and a worker may satisfy them using `respondWith()`.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/scope
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/fetch_event
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers

## Core synthesis

### 1. Same-origin auth routing solves one problem and creates another release dependency

Using `logmate.minttap.app` as `authDomain` can remove the cross-origin helper-storage boundary described by Firebase and presents the product domain during provider authentication.

But it places Firebase auth-helper traffic under the same origin as the PWA. A root-scoped Service Worker can therefore become part of the authentication request path.

So:

`custom authDomain configured ≠ OAuth helper reachable through installed PWA`

### 2. Hosting rewrite correctness and Service Worker correctness are separate

Firebase Hosting owns `/__` as a reserved namespace. Even if Hosting serves `/__/auth/handler` correctly, a controlling Service Worker can intercept a navigation before the request reaches Hosting.

So:

`Firebase Hosting reserved route correct ≠ controlled-client navigation reaches Hosting`

and:

`firebase.json correct ≠ Service Worker bypass correct`

### 3. Auth-helper bypass is a security and availability invariant, not a caching preference

The Service Worker must not synthesize the Flutter app shell, return a stale cached response, or otherwise take authority over `/__` requests.

The minimum owned-worker rule is conceptually:

- detect same-origin path beginning `/__/`;
- do not answer it from the application cache;
- do not apply navigation fallback;
- allow the request to proceed to the network/Hosting path according to the browser's normal fetch behavior.

Exact implementation belongs to Software Engineering and must be tested; Web Manager owns the invariant.

### 4. Offline authentication and offline application use are distinct

An EFB PWA can remain useful offline using already-authorized local product state while a new federated OAuth transaction is unavailable because the provider/Firebase helper requires network access.

Therefore:

`PWA works offline ≠ federated sign-in works offline`

and:

`offline local access policy ≠ permission to fabricate/refresh provider authentication`

Auth/session/offline-authorization policy remains a separate Stage-8 boundary.

### 5. Existing controlled clients matter

A user may already have an older Service Worker controlling an open Safari/Home-Screen client when a new OAuth configuration or worker version is deployed. Release validation must cover the existing-controller path, not only a clean install.

This connects directly to the prior mixed-generation gates:

`new Hosting config deployed ≠ installed fleet uses safe worker behavior`

`new worker installed ≠ existing document/controller generation aligned`

### 6. Legacy provider routes are compatibility state, not proof of fallback safety

LogMate's operations document deliberately retains legacy `firebaseapp.com` provider routes. That may be useful during migration, but runtime code currently points Web Firebase Auth to `logmate.minttap.app`.

Retaining a legacy redirect in provider configuration does not prove that Firebase Auth will automatically fail over to it if the custom-domain helper is intercepted or unavailable.

No automatic fallback is assumed.

## Cross-track ownership and transfer

### Track E — owner

Own:
- auth-domain/Hosting/provider routing trust boundary;
- reserved-namespace isolation requirement;
- release/rollback compatibility;
- auth-helper availability and incident diagnosis;
- prohibition on treating a Service Worker fallback as an auth handler.

### Track A — dependency supplier

Own reusable mechanics:
- Service Worker registration scope;
- fetch/navigation interception;
- controlled-client lifecycle;
- browser storage/redirect behavior.

Transfer: root-scope control means `/__` must be explicitly outside application fallback authority.

### Track C — validation consumer

Required runtime matrix:
- clean browser tab;
- previously controlled browser tab;
- installed/Home-Screen PWA;
- N worker controlling document while N+1 is waiting/active;
- online provider success/cancel/error;
- `/__/auth/handler` direct navigation;
- popup flow;
- redirect flow if supported/used;
- offline attempt and network restoration;
- stale-worker rollback;
- Safari/iPadOS and Chromium diagnostic runs.

Record exact document/controller/worker generation and actual response URL/content for `/__/auth/handler`.

### Track B — UX dependency

Do not collapse:
- local EFB access;
- Firebase session present;
- provider reauthentication required;
- provider popup/redirect unavailable;
- network unavailable;
- auth-helper routing failure.

A locally usable offline logbook must not falsely claim federated sign-in success.

### Track D — measurement dependency

Auth analytics must distinguish at least:
- provider flow started;
- popup/redirect opened;
- helper returned;
- Firebase credential accepted;
- owner/session gate completed.

Do not use page navigation to `/__/auth/handler` as a successful-sign-in metric.

## Release invariants

1. `/__` is Firebase-reserved and outside application navigation-fallback authority.
2. No executable application cache may satisfy `/__/auth/*`.
3. A PWA release verifier should fail if the owned Service Worker does not encode/test this exclusion.
4. Current Flutter-generated worker acceptance remains OPEN until exact built bytes demonstrate the exclusion.
5. Custom `authDomain`, Firebase authorized-domain configuration, provider return URL, Hosting reserved route and Service Worker bypass are five separate checks.
6. Popup success does not waive redirect/helper-route testing because both rely on provider/helper infrastructure and platform behavior can differ.
7. Offline product usability does not imply offline provider authentication.
8. Legacy `firebaseapp.com` registration is not an automatic runtime fallback contract.
9. Clean-install PASS does not waive existing-controller/mixed-generation testing.
10. Provider console CONFIGURED does not become VERIFIED until real served-origin runtime evidence exists.

## Deterministic validation plan

### V0 — exact artifact inspection

From the exact release candidate:
- preserve `flutter_bootstrap.js`;
- preserve `flutter_service_worker.js`;
- record worker script URL and registration scope;
- locate navigation-request logic;
- prove what happens for `https://logmate.minttap.app/__/auth/handler`;
- fail if it can return Flutter `index.html` or application cache content.

### V1 — Hosting route baseline without controlling worker

On a clean profile:
- request `/__/auth/handler` directly;
- confirm Firebase helper content/behavior, not Flutter shell;
- record status/headers/final URL;
- exercise Google and Apple configured return paths separately.

### V2 — controlled-client isolation

Install/activate the release worker, then repeat V1 from:
- controlled browser tab;
- reopened tab;
- Home-Screen PWA where supported.

The response must remain Firebase helper behavior.

### V3 — mixed generation

Hold an N-controlled document open while deploying N+1. Repeat provider start/return before and after controller transition. No generation may capture `/__` with application fallback/cache.

### V4 — network/offline failure

Attempt provider auth while offline and during network interruption. Expected behavior is explicit auth unavailability/recovery, not cached fake success. Restore network and verify a fresh provider/helper exchange.

### V5 — rollback

Roll back application/worker generation while retaining provider configuration. Verify both current and rollback-supported worker generations preserve `/__` isolation.

### V6 — platform ladder

Chromium is diagnostic only. Required product evidence remains:
Safari tab → iPadOS Home Screen → physical iPad → representative managed iPad/EFB.

## MINTTAP / LogMate decision

Treat Firebase's `/__` namespace as **non-cacheable, non-fallback application-external control traffic** in the LogMate PWA architecture.

When LogMate moves from Flutter-generated Service Worker patching to an owned worker, the `/__` bypass must be a first-class source rule, verifier assertion and runtime acceptance fixture.

Until the exact current generated worker is inspected, current custom-domain Google/Apple PWA runtime remains **OPEN / NOT VERIFIED** even though source/configuration is CONFIGURED.

## CHANGE WATCH

Recheck when any of these change:
- Flutter Web Service Worker generation/retirement behavior;
- Firebase Auth helper/custom-domain guidance;
- Firebase Hosting reserved namespace behavior;
- Safari/WebKit storage partitioning or popup/redirect behavior;
- Google/Apple OAuth return-domain requirements;
- LogMate Service Worker scope or navigation strategy;
- LogMate `authDomain`, Hosting domain or provider redirect URLs.

## Next highest-value work

1. Build the exact current LogMate normal/acceptance PWA artifact and inspect generated worker navigation handling for `/__`.
2. Add `/__` isolation to the future LogMate-owned-worker contract before cutover.
3. Add semantic verifier checks that reject application fallback/cache authority over Firebase reserved URLs.
4. Execute custom-domain Google/Apple runtime acceptance through a controlled PWA client.
5. Then return to local-mutation ambiguous-completion work with the auth/session boundary now separated from Service Worker routing.

Production validation remains OPEN until real served-origin and physical/runtime evidence exists.
