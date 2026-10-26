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


---

## 2026-10-27 Stage 8 integrated continuation — managed-EFB federated OAuth operation, session and local-ledger admission [SOURCE / SYNTHESIS / TRANSFER VALIDATION]

**Scope and evidence level.** This section extends the reserved-`/__` routing gate rather than repeating it. LogMate product source read-only at **`main@26d2d7cf2c20c55026c6f84b838dcb6442f7a3f1`**, `lib/auth/provider_auth_engine.dart@ae9fa89cb1becaf41d6d92159186922e7b0ba1fa`, `lib/auth/auth_engine.dart@fcc23dcff1af779b5c2747dad34b2f4e19cda2c6`, `lib/firebase_options.dart@4374020a221d88460e61b15291e403f103722802`, `web/flutter_bootstrap.js@a70625e8bda32aafd5dd23822c017d05229f0e63`, `firebase.json@9ac0972e26749215c4a718360c66315c6caf3cc8`, `pubspec.lock@746ef9de51b1096fb1d64784d098ae188abdbd43`, `test/auth/provider_auth_owner_completion_test.dart@36704b03360ba6e32574c26abae921acc49b016b`, `test/auth/firebase_web_auth_domain_test.dart@bbbcd13fb1a85e059a06507140ebf2957f7a2372`, and `docs/operations/federated-auth-providers.md@a8756232298b24885290fd2e1437d6e98c141c7a`. Lockfile: **firebase_auth 6.7.0 / firebase_auth_web 6.3.0**. No runtime provider credentials, OAuth console, NORMAL archive, actual WebKit/Safari/MDM or production session were exercised.

### A. Why a separate operation gate is needed [HISTORY / DESIGN PRINCIPLE / STANDARD]

Federated sign-in is not one browser action. Initial authentication, **recent-login reauthentication**, provider account **linking**, and **unlinking** have different consequences; they must not be inferred from a successful Google account chooser. The OAuth provider window/redirect, Firebase helper, returned credential, current UID, owner-ledger admission and server-currentness are distinct transitions. Firebase's web auth methods expose popup/redirect operations, whereas FlutterFire documents native `WithProvider` and web `WithPopup`/`WithRedirect` branches. The choice is an API/platform contract, not a visual-button preference.

Authoritative sources inspected 2026-10-27:
- Firebase/FlutterFire federated auth, including explicit web-vs-native Apple **link** and **reauthenticate** branches: https://firebase.google.com/docs/auth/flutter/federated-auth
- FlutterFire upstream source/documentation: https://github.com/firebase/flutterfire/blob/main/docs/auth/federated-auth.md
- Dart `User.linkWithProvider` API: **native flow; on web use linkWithPopup or linkWithRedirect**: https://pub.dev/documentation/firebase_auth/latest/firebase_auth/User/linkWithProvider.html
- Firebase Apple Web authentication, recent login, popup and redirect: https://firebase.google.com/docs/auth/web/apple
- Firebase web redirect/third-party-storage guidance: https://firebase.google.com/docs/auth/web/redirect-best-practices
- Firebase auth-state persistence (LOCAL / SESSION / NONE, origin scoped): https://firebase.google.com/docs/auth/web/auth-state-persistence
- Firebase reserved Hosting namespace: https://firebase.google.com/docs/hosting/reserved-urls
- WebKit Safari 17.2 Home Screen cookie-copy and independent storage caveat: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/
- WebKit Safari 26 Home Screen presentation change: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- Apple managed Web Clip: https://support.apple.com/en-gb/guide/deployment/depbc7c7808/web

These are **current documentation snapshots**, not a verified implementation trace of the exact locked FlutterFire 6.7.0/6.3.0 plugin binaries. Exact version behavior remains a Software Engineering execution question.

### B. Current product operation matrix [SOURCE / CONTRADICTION]

| Operation | Google on Web | Apple on Web | Native branch | Verdict |
| --- | --- | --- | --- | --- |
| Authenticate | `signInWithPopup(GoogleAuthProvider)` | `signInWithPopup(AppleAuthProvider)` | Google SDK credential / Apple `signInWithProvider` | Source branch matches documented web popup pattern; **real success OPEN** |
| Reauthenticate | `user.reauthenticateWithPopup(GoogleAuthProvider)` | **`user.reauthenticateWithProvider(AppleAuthProvider)`** | Apple `reauthenticateWithProvider` | **Web Apple branch diverges from FlutterFire documented `reauthenticateWithPopup`** |
| Link | `user.linkWithPopup(GoogleAuthProvider)` | **`user.linkWithProvider(AppleAuthProvider)`** | Apple `linkWithProvider` | **Web Apple branch contradicts explicit native-flow API guidance** |
| Unlink | `user.unlink(providerId)` | same | same | Source checks current UID, supported provider count and observed removal; backend/provider runtime **OPEN** |

The two bold Apple Web paths are **source-confirmed documentation/implementation mismatches**, not an observed production failure. Do not infer `UnsupportedError`, failed account deletion, compromised UID, or data loss without running the exact locked web plugin. The `_runApple` reauthenticate/link branches use `auth.currentUser!` without the explicit no-user check present in the Google Web path; if absent, a caught exception is normalized to generic `ProviderAuthFailure`. This is a **source-level diagnostic/UX ambiguity**, not a verified reachable user incident.

**Reachability limit:** current `OpeningScreen` calls `authenticate` for Apple/Google; `SettingsScreen` exposes no provider link/reauth action. The account-deletion coordinator defines a separate `DeletionReauthenticationPort`; its actual adapter wiring to this provider engine was not established. Thus the mismatched methods are **potential future/integration paths**, not proven currently exercised product workflows. Operations docs describe client sign-in/link/unlink as implemented but explicitly keep real provider cross-surface runtime NOT VERIFIED. Widget tests use a fake `ProviderAuthEngine` and prove welcome routing/feedback, not Firebase popup, Apple link/reauth, Safari storage or server acceptance.

### C. Popup vs redirect is a controlled trade-off, not an automatic fix [SYNTHESIS / FAILURE MODES]

1. **Popup** avoids a full-page navigation and Firebase explicitly offers it as an alternative when redirect's cross-origin iframe storage is blocked. It can itself be blocked or behave differently on mobile/managed browsers. A popup opening/account chooser is **not** a returned Firebase credential.
2. **Redirect** is documented and sometimes preferred on mobile, but Firebase requires an appropriate same-origin/custom-domain helper setup under third-party storage restrictions. Changing from popup to redirect is **not** a safe blind fallback: it changes page lifecycle and requires explicit result recovery, pending operation identity, UID continuity and unique local data preservation.
3. **Hosting `/__`** is Firebase-reserved; the root-scoped PWA Worker must not intercept the helper or substitute cached shell. This was established in §312 and remains an independent gate even if the popup appears.
4. **Safari tab, installed Home Screen, MDM Web Clip** may have different presentation, session and storage contexts. WebKit's 17.2 cookie-copy-at-creation is not an IndexedDB, CacheStorage, Sembast, local outbox or Auth-state migration guarantee. A sign-in success in Safari tab does not certify a separate installed container.
5. **Offline:** a locally admitted pilot may continue permitted offline logbook work under product policy; the OAuth provider and Firebase helper require connectivity. No offline provider authentication, automatic mobile→PWA identity transfer or background refresh is implied.
6. **Auth state ≠ owner/data authority:** a restored local Firebase session is not fresh remote acceptance; provider credential success does not authorize access to another UID's local ledger; successful local flight save does not prove remote Sync. Retain independent UID binding, local ledger readback and external backup evidence before any recovery or session reset.
7. **Shared/managed device:** Firebase Web's default persistent session may be unsuitable for shared-device policy; switching to SESSION/NONE also changes user friction and restart behavior. Actual managed-device policy, owner authentication and storage deletion/retention remain UNKNOWN. No blanket change to persistence is approved here.

### D. Threat, failure and observability boundaries [SECURITY / OPERATIONAL JUDGMENT]

A popup-blocked, user-cancelled, provider-disabled, unauthorized-domain, helper-route-intercepted, network-indeterminate, stale-session, wrong-UID and server-rejected event must be distinguished. Product `ProviderAuthOutcome` already maps several codes, but an unclassified exception becomes `ProviderAuthFailure`; the UI must not imply cancellation or server revocation from that generic outcome. For reauthentication/linking, record before/after UID and provider-set equality using **privacy-minimal derived diagnostics**, not tokens, email addresses, OAuth codes, full account identifiers or flight data.

A browser/OS restriction is not proof of an app vulnerability. Conversely a source-correct API choice does not certify popups under iPadOS Home Screen/MDM policy. Neither a successful account chooser nor `authDomain` config may promote product PWA admission. If the platform prevents the selected OAuth flow, prefer an explicit unsupported/retry path with local-data preservation rather than clearing Sembast/CacheStorage or inventing automatic device sync.

### E. High-information-gain executable acceptance matrix [VALIDATION DESIGN / OPEN]

Reuse LogMate AUTH-E7 and existing Web Manager 312/504/519/520, W-031/W-036; **Engineering owns code and browser harness**. Each result must record exact source SHA, locked package versions, NORMAL artifact hash, HTTPS origin/response, Worker/controller generation, browser/OS/MDM envelope, initial UID/ledger state, expected/observed outcome and independent oracle; classify NOT RUN / PASS / FAIL / UNKNOWN.

| Case | Stimulus | Independent oracle / negative control |
| --- | --- | --- |
| FA01 | Google initial popup in clean Chromium | helper network path, Firebase UID returned, owner gate; account chooser alone insufficient |
| FA02 | Apple initial popup in clean Chromium | same, with Apple provider enabled/config independently observed |
| FA03 | Google/Apple popup in Safari tab | actual popup/navigation, credential result and error taxonomy |
| FA04 | Google/Apple in installed iPadOS Home Screen | independent installed-container auth/session result, not Safari-tab transfer |
| FA05 | Managed Web Clip with employer-approved policy | actual launch/popup permission and return, no MDM assumption |
| FA06 | Apple **link** on Web exact locked plugin | compare `linkWithProvider` observed result against documented `linkWithPopup` positive control |
| FA07 | Apple **reauthenticate** on Web exact locked plugin | compare `reauthenticateWithProvider` against documented web positive control; same UID |
| FA08 | Google link/reauth Web | popup positive/negative, before/after UID and provider set |
| FA09 | No `currentUser` then Apple/Google link/reauth | expected invalid-session semantics; distinguish generic exception |
| FA10 | Popup blocked, dismissed, delayed, repeated | separate unavailable/cancelled/unknown; no unauthorized owner completion |
| FA11 | `/__` helper under old/new controlling Workers | actual HTTPS helper bytes/status, never Flutter shell/cache |
| FA12 | Third-party-storage restricted + optional redirect prototype | same-origin helper and redirect result, no silent fallback or lost pending state |
| FA13 | Offline and network interruption mid-auth | no fabricated success/revocation; local edits and export remain intact |
| FA14 | Existing auth session in Safari vs newly installed Home Screen | separate auth state, origin/partition, Sembast and backup inventory |
| FA15 | Wrong UID, collision, stale remote authority | fail owner gate without deleting/migrating unique local ledger |
| FA16 | Restart, Worker update, schema transition during auth | pending auth operation/UID state resolved safely; independent ledger + external backup readback |

**Negative controls:** popup opens but no Firebase credential; Firebase credential returns but owner UID mismatch; `/__` returns application shell; session disappears but ledger survives; session survives but local storage is absent; successful login without verified external backup. These must produce **different** verdicts, not one “auth works” PASS.

### F. Five-track allocation and release decision [DEPENDENCY / TRANSFER VALIDATION / MINTTAP DECISION]

- **E primary (highest consequence):** operation authority, custom-domain/helper trust, owner UID, account recovery and managed-device session/data custody. Source/docs mature; exact provider/device proof OPEN.
- **A major prerequisite:** web-vs-native API dispatch, popup/redirect browsing context, first-party helper/Worker scope, Home Screen partition and lifecycle. Current docs/source mature; exact locked-plugin and Safari execution OPEN.
- **C major validation:** 16-case negative/positive matrix and independent 37-store/external-LBK readback; fake-widget and CI PASS are not provider/browser PASS.
- **B bounded transfer:** Design Studio W121/IP recovery semantics. “Popup blocked,” “session unknown,” “owner mismatch,” “offline local access” and “provider reauthentication required” must be distinguishable without implying flight loss.
- **D bounded transfer:** Marketing Manager D8–D10 launch claims HOLD. Web analytics distinguishes click, popup/helper, Firebase accepted, owner bound and repeat local task; avoid raw UID/email/flight telemetry. No acquisition-primer duplication.
- **Software Engineering:** owns exact firebase_auth_web 6.3.0 dispatch audit, executable provider harness and any patch; Web Manager records web release requirements only.

**MINTTAP DIRECTION (not product code approval):** classify the two Apple Web `WithProvider` paths as **implementation review required before feature activation**. Keep existing Apple/Google initial sign-in as **source-implemented but runtime OPEN**; do not approve a redirect replacement without storage/Worker/UID and data-preserving restart tests. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**

**CHANGE WATCH:** Firebase/FlutterFire plugin upgrades, Firebase auth helper/redirect guidance, Apple/WebKit popup/Home Screen/MDM policies, Login/Account deletion wiring, worker `/__` routing and browser storage. **Adjacent-question check:** initial vs reauth vs link vs unlink; web/native dispatch; user-gesture/popup failure; redirect/third-party storage; custom helper/Worker; session/UID/ledger split; Safari/Home Screen/MDM; offline/restart; privacy-minimal diagnostics; negative/positive runtime oracles. Further abstract mock assertions would not resolve the exact-plugin/browser blocker; stop at the meaningful source/standards checkpoint. No peer/product edits.

## 2026-10-27 Stage 8 continuation — cross-tab Auth state, durable owner lock and direct repository authority [SOURCE / SYNTHESIS / TRANSFER VALIDATION / OPEN]

**New, distinct question:** The preceding federated-auth section establishes web/native OAuth API selection. This continuation asks a different security question: *when an already-running browser tab has a LogMate repository handle, which state transition actually prevents it from viewing or mutating a UID-owned ledger after another tab signs out or changes Firebase identity?* This is particularly relevant to shared iPads and multi-tab Chromium, but must not be conflated with WebKit Home Screen storage partitions or an observed data leak.

### 1. Standards/platform and product authority, pinned [HISTORY / SOURCE]

A browser's **authentication persistence** and a product's **durable local authorization lock** are separate mechanisms. Firebase's official Web Auth persistence documentation (checked 2026-10-27) states that browser default is normally LOCAL, that LOCAL auth state is synchronized among tabs on the same origin, and that SESSION/NONE have different tab semantics. Changing persistence also changes existing saved auth state; a successful sign-out in one LOCAL tab may propagate auth state to its sibling tab. **This is Firebase JS/Web documentation, not a captured trace of the locked FlutterFire plugin or a promise across WebKit standalone containers.** Source: https://firebase.google.com/docs/auth/web/auth-state-persistence

WebKit Safari 17.2 states that a new Home Screen web app copies **cookies only** at creation when login state uses cookies, not IndexedDB/localStorage; afterwards website data is separate from Safari. Therefore a same-origin Safari tab and installed Home Screen app are **not equivalent to two tabs sharing one Firebase persistence store**. Do not claim a Firebase Web session is cookie-backed or automatically copied to a LogMate Home Screen app. Source: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ . Managed Web Clip/MDM context remains an independent physical-device question (520).

Current LogMate product authority is **account-required**, with Firebase UID the owner, an explicit sign-out that **durably locks the ledger before Firebase sign-out**, matching-UID reauthentication for unlock, and separate remote-currentness validation. This is confirmed in read-only `docs/specs/startup-and-auth-entry-spec.md@3e1f4b60` and `docs/specs/local-first-manual-delta-sync-contract.md@2240fc1b` (the latter approves Manual Delta Sync **as a contract, not an implemented remote feature**). A restored session, an unlocked local owner, a UI route and a remote Sync receipt are different authorities.

Product source pinned **LogMate main@26d2d7cf2c20c55026c6f84b838dcb6442f7a3f1**:
- `lib/app/session_gate.dart@5bcd6bf2089ef1bf10aae1aaa3950f6795624a66`: startup resolves an owner-aware decision; foreground `didChangeAppLifecycleState(resumed)` schedules remote validation; inspected SessionGate has **no `authStateChanges` / `idTokenChanges` / `userChanges` subscription**. It can retain `LocalLedgerAccessAllowed` and a `HomeScreen`/repository handle until an explicit local action, lifecycle event, or another established reroute. This is an inspected-component statement, **not** a complete application-wide listener inventory or observed stale UI.
- `lib/application/logbook/local_ledger_auth_access_service.dart@a6e74cd15eb9c24ead33c36994f026671eba387e`: passive auth observation reads `currentUser`; no auth-change subscription in this service; explicit sign-out delegates to the owner-aware coordinator.
- `lib/application/logbook/local_ledger_access_coordinator.dart@3fd1bb719d9a5c5b156d112b67431deac6ede9db`: **positive controls** — `signOutExplicitly` writes `lockForExplicitSignOut()` before invoking Firebase sign-out; account-required startup returns authentication-required for signed-out, and owner mismatch for different UID.
- `lib/auth/auth_engine.dart@fcc23dcff1af779b5c2747dad34b2f4e19cda2c6` and `lib/auth/provider_auth_engine.dart@ae9fa89cb1becaf41d6d92159186922e7b0ba1fa`: inspected engines use `FirebaseAuth.instance` and do not themselves set explicit Web persistence. **Repository-wide absence of another persistence override has not been established.**
- `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb` and `lib/repository/logbook/logbook_repository.dart@9d256d5b152744624aeaae0fdb39c55847d1b67e`: repository exposes direct record read and CRUD methods. Exact `create` (around line 2136), `update` (2189), `delete` (2245), `restore` (2302) run Sembast transactions and update revision/outbox/data-generation **without an explicit `_requireUnlockedBoundOwner` or `_readOwnerAccess` in those method bodies**. Direct `readActiveRecords` (2089) and `readActive` (2127) likewise have no owner check in their bodies. Their helper `_requireUnusedMutationIds` checks uniqueness, and `_advanceLedgerDataGeneration` advances a counter; neither is an owner check. `LocalMutationIdentity` in `repository_types.dart@eeb25e16` contains revision ID, operation ID and accepted UTC, **not owner UID**.
- **Positive comparison:** `createFlightEntryDraft` and `updateFlightEntryDraft` explicitly call `_requireUnlockedBoundOwner`; `exportWholeLedgerBackup` checks a matching unlocked `verifiedOwnerUid`; `_commitLedgerMutation` conditionally checks owner based on the plan. This means **not all repository paths are unguarded**. The direct primitive methods' absence of a guard is a real *source-level boundary inconsistency*, not proof that the current Home UI uses them after sign-out.

### 2. Exact failure model and limits [SYNTHESIS / SECURITY / CONTRADICTION]

**Conditional same-partition two-tab sequence:** Tab A and B have a matching owner and local DB; B has already mounted Home. A invokes explicit Sign out; A durably locks the shared owner store and Firebase LOCAL auth may propagate signed-out state to B. If B stays foreground without an auth-state-triggered re-evaluation, its **rendered route may remain stale**. If B invokes a direct repository primitive that does not check the durable lock, its call does not enforce the product's explicit-sign-out invariant at that method boundary. A stale B may also read via the direct `readActive*` methods. **No such two-tab Dart/browser execution was performed; no production disclosure, unauthorized flight edit, exploit or user incident is asserted.** Whether B actually invokes those APIs, and whether higher-level callers revalidate authority, is OPEN.

**Different-UID variant:** A later Firebase LOCAL account switch in a sibling tab is not by itself authority to rebind the existing ledger. The account-required startup resolver has a mismatch guard, but an already-mounted view requires a fresh gate decision. Remote UID acceptance, local UID binding and each record operation must not be collapsed into one “signed in” flag.

**Offline/installed variant:** a temporarily unreachable Firebase service is **not** permission to destroy or lock an established unlocked offline ledger. A separate Safari/Home Screen or second installed copy may not share either Auth persistence or Sembast data with the browser tab; an MDM Web Clip may have additional restrictions. No automatic cross-container lock propagation, session continuity or data transfer can be inferred. Conversely, `signOut` in one separate container must not be advertised as a verified global device wipe.

**Threat-model limit:** malicious JavaScript with same-origin execution could often access origin IndexedDB directly; a repository guard is not a substitute for CSP/XSS defense, OS access controls or encryption. The narrower value here is **correctness of app-internal local owner/explicit-sign-out policy under stale tabs, async events and retained repository handles**. A UI reroute alone is not sufficient evidence that every data entry point enforces the lock. Do not propose clearing CacheStorage/IndexedDB or the 37-store ledger to “fix” a stale UI; this would violate recovery/data-preservation requirements.

### 3. Bounded static audit and discriminating runtime packet [VALIDATION / OPEN]

A **15/15 source-text assertion audit** against the exact blobs above checked: lock-before-Firebase-sign-out, account-required signed-out/mismatched-UID decisions, lifecycle resume handling, absence of auth-state subscription in the two inspected coordinator components, owner guards on two draft methods, absence of owner checks in four direct record CRUD and two direct read bodies, outbox write in direct create, and no owner UID in `LocalMutationIdentity`. This is a **static source audit only**: no Dart analyzer, Sembast execution, Chrome/Safari browser test, FlutterFire cross-tab observation or physical EFB acceptance. Textual assertions can miss indirect authorization elsewhere; the helpers used by the four direct methods were separately inspected for the narrower claim.

**Engineering/QA packet (extend existing W-031/W-036/W-012 and 312/504/519/520; no duplicate product test framework):**

| Case | Stimulus / negative control | Required independent oracle |
| --- | --- | --- |
| AT01 | Exact NORMAL Chromium, same-origin tabs A/B, verified UID A, both foreground | Firebase persistence type actually observed, both tab session states and owner metadata |
| AT02 | A explicit sign-out while B remains foreground | Durable owner lock precedes Auth clear; B route/action availability transitions without needing tab focus |
| AT03 | B direct `readActiveRecords` and `readActive` after AT02 | Distinguish method-level access, higher-level gate and UI exposure; no raw flight logs in telemetry |
| AT04 | B direct `create/update/delete/restore` after AT02 using disposable seeded records | Owner lock must prevent unauthorized mutation; independently compare record/revision/outbox/data-generation before/after |
| AT05 | B draft create/update and LBK export after AT02 | Positive guard controls reject; no partial write/export |
| AT06 | A switches UID A→B while B tab remains mounted | No A-ledger read/mutation or owner rebinding by B; no accidental new-owner claim |
| AT07 | LOCAL versus SESSION/NONE persistence (test-only configurations) | Actual plugin cross-tab behavior; no assumption that a mode switch is safe |
| AT08 | Offline loss of remote authority with already-unlocked UID A | Local approved access preserved, no false sign-out, no remote Sync success |
| AT09 | Same-owner explicit reauth after lock | UID equality, unlock, existing records and pending operations preserved |
| AT10 | Safari tab→Home Screen install and second installed copy | Independent Auth and IndexedDB inventories; cookie-only copy when applicable, no assumed ledger migration |
| AT11 | Representative managed EFB Web Clip | Exact OS/MDM/persistence policy, restart and lock/restore behavior; no background sync assumption |
| AT12 | Worker update or `clients.claim` during A/B sign-out | Controller/route state and data authority independently recorded; no 503 mistaken for security lock |
| AT13 | In-flight write racing A's durable lock | Transaction ordering and before/after record+outbox evidence; no partial commit or silent loss |
| AT14 | A owner deletion or owner B reuse on isolated fixture | Reuse existing W-030 F-01 and Marketing D9 owner-retirement oracles; not “all 37 stores must be empty” |
| AT15 | Export .lbk before lock, restore to clean matching UID | File provenance, restore readback, replica and Sync-hold semantics; never assume sign-out = backup |
| AT16 | Instrumented keyboard/screen-reader focus after external auth change | Accessible, truthful “signed out / offline / owner mismatch / local data preserved” state; no fake data-loss copy |

For each: **NOT RUN / PASS / FAIL / UNKNOWN** at exact commit, locked plugin, NORMAL artifact, origin, browser/OS/MDM, initial UID/owner/lock, fixture and oracle. Tests must prove both positive behavior and **negative control** (locked state rejects direct read/mutation as product policy requires), without relying on a route screenshot or Firebase sign-out alone. Test-only UID pseudonyms and aggregate counters are acceptable; never capture real Firebase tokens, full UID, flight entries or OAuth codes in analytics.

### 4. Five-track allocation and operational judgment [TRANSFER VALIDATION / MINTTAP DIRECTION / CHANGE WATCH]

**E (primary bottleneck):** distinguish Firebase session persistence, durable owner lock, per-operation authorization and remote Sync authority; recommend an **Engineering design review** of direct repository primitives and stale-session invalidation, not a speculative production hotfix. **A (dependency):** Firebase LOCAL tab synchronization vs WebKit independent Home Screen/MDM contexts, Worker control and lifecycle. **C (critical evidence):** AT01–AT16 real browser and locked-owner/37-store/backup oracles; static 15/15 is diagnostic only. **B (bounded transfer):** consume Design Studio `progress/WEB_STATUS.md` W121 (Stage 3 PRACTICE), use accurate lock/recovery/owner-mismatch UX, do not claim screen-reader PASS. **D (bounded transfer):** Marketing Manager D8/D9/D10 keeps offline/Sync/erasure/ads claims HOLD; measurement must distinguish signed-out state, local lock, server revocation, installed copy and recovery without recording personal ledger data. Software Engineering Studio `methods/VALIDATION_STANDARD.md` owns executable test/oracle methodology; product Engineering owns implementation.

**MINTTAP DIRECTION (research-level, not code approval):** A durable explicit-sign-out lock should be enforced at the appropriate *actual data access boundary* as well as reflected in UI routing; a previously opened tab must not be treated as newly authorized solely because it still displays Home. Evaluate whether direct repository CRUD/read primitives are intentionally privileged internal APIs and whether every production caller has a guard, before selecting a fix. Do not infer production exploitation or automatic multi-tab data exposure from source alone. Maintain **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD**.

**CHANGE WATCH:** Firebase JS/FlutterFire exact LOCAL cross-tab behavior and persistence overrides; WebKit iOS/iPadOS Home Screen partition and MDM; LogMate `SessionGate` auth listeners, direct repository CRUD/read callers, lock semantics, schema/backup and approved Manual Delta Sync implementation. **Adjacent-question stop check:** reconciled default LOCAL, shared-tab sign-out, stale UI, direct read/write methods, positive guard controls, account switch, offline, installed partitions, Worker update, data recovery, privacy and cross-track claims. Next information-gain step is **actual Dart repository locked-owner negative test and two-tab browser execution**, not additional abstract mock variants. No peer/product repo writes.
