# 516 — Stage 8 PWA Shared-Origin Authority: Auth Action, CSP, Worker Bypass and Third-Party Execution

Date: **2026-10-25 (Asia/Seoul)**  
State: **SOURCE AUDIT + CROSS-TRACK SYNTHESIS + PROPOSED SECURITY ACCEPTANCE; NO LIVE HEADER/BROWSER/DEVICE PASS**  
Primary owner: **Track E (Security / Operations)**; Track A owns browser policy mechanics, C independent tests, B recovery/task meaning, D privacy and publisher claims.  
Canonical Web Manager starting HEAD: `80d377f7be40946d1501321382931d0588f8a3bd`. Product inspected **read-only** at LogMate `main@4101ec7380796300f68fa60dbc7e5b6061f00080`. No product policy or source change is authorized by this study.

## 1. Decision and information-gain boundary [SOURCE / SYNTHESIS]

Previous 509–515 work separated release bytes, Service Worker generations, IndexedDB custody and external backup. The adjacent Stage 8 question is **which JavaScript and document responses are permitted to execute with the same origin as the pilot ledger and Firebase account-action flow**, and which route-specific browser policies can narrow that risk without breaking Flutter, authentication or offline recovery.

This is **not** another generic CSP/XSS primer or a claim that LogMate has a known exploit. Web Manager's earlier sensitive-origin work (including the 096 boundary cited by Marketing 438), 321–324 auth/CSP/Worker research and 514/515 recovery research remain reusable. This study adds an exact-current-source **multi-route trust audit**, a verified Worker reserved-route counterexample, the Firebase Hosting pre-rewrite header-matching consequence, and a concrete admission matrix for Engineering.

**Core distinction:** a path excluded from Service Worker interception is not a different web origin. A third-party ES module imported by a same-origin HTML document executes with that document's privileges; origin/IndexedDB access is constrained by the browser's actual storage container, not by the module's download hostname. Neither a trusted vendor label nor a versioned CDN URL constitutes a script sandbox. An attacker or compromised script is a **threat-model scenario**, not an observed vendor compromise.

## 2. Canonical evidence and exact source findings [SOURCE]

| Surface / pinned blob | Direct observation | Limit of observation |
| --- | --- | --- |
| `firebase.json` blob `9ac0972e26749215c4a718360c66315c6caf3cc8` | Hosting `public: build/web`; sole configured `headers` rule matches `**` and sets `Cache-Control: no-cache, no-store, must-revalidate`; rewrites `/auth`, `/auth/`, `/auth/action` to `/auth/action/index.html`. No configured CSP, Referrer-Policy, Permissions-Policy or frame policy in **this source file**. | Actual HTTPS responses may have provider/intermediary headers; no served-byte/header probe performed. This does not establish production header absence. |
| `web/index.html` blob `01be77585ac40bf11e80777177a4ab08e4885671` | Flutter root loads same-origin `flutter_bootstrap.js` with `async`; manifest link; no ad or analytics script in this **template**. | Generated build/Flutter runtime imports and live network activity not audited by this template alone. |
| `web/flutter_bootstrap.js` blob `a70625e8bda32aafd5dd23822c017d05229f0e63` | Project-owned worker registration at base path with `updateViaCache:'none'`; registration deliberately does not gate first paint. | Worker registration success, installed scope, active controller, runtime security policy and offline readiness remain unverified. |
| `web/auth/action/index.html` blob `39d06a633ab7bee719b3401bc3ac744f8ba175d0` | Inline `<script type="module">` imports Firebase SDK modules from `https://www.gstatic.com/firebasejs/11.10.0/...`; reads `mode` and `oobCode` from URL query; supports email action/password reset; inspected UI writes use `textContent` (no `innerHTML` or `eval(` string found in this file). | A fixed versioned module path is not a verified immutable hash. No SDK supply-chain incident, XSS, token leakage or deployed-policy failure observed. |
| `tool/pwa_precache.dart` blob `90a67954af618a4e18199fa92555491c56167c17`, generated Worker source around lines 404–406 and 602–642 | `reserved()` excludes decoded `auth`, `auth/`, and `__/` routes; `fetch` handler checks `reserved(rawRelative)` and returns **before** `event.respondWith`. Non-root navigations also bypass the root-shell rewrite. | This corrects an easy false inference: the present source does **not** show Worker interception of ordinary `/auth/action` navigation. Browser/device enforcement of that bypass still needs exact-build evidence. |
| LogMate `MASTER.md` and approved Manual Delta Sync contract | Account-required Firebase UID is owner authority; Manual Delta Sync is user-initiated, and PWA/native direct unattended Sync is not approved/verified. | A Firebase action-link completion does not prove local ledger ownership transfer, backup, remote receipt or Sync success. |
| Marketing Manager 437/438, latest `STATUS.md` | Native-only Manual-Sync ad is a conditional research candidate; **PWA ad-free by default, web ad rollout HOLD**, no ad provider/publisher authorization asserted. | This study does not approve or implement a new ad placement. |

**Static check performed this run:** inspected the above exact GitHub blobs; source-string inventory found two external Firebase module imports in the auth-action document, no `innerHTML`/`eval(` there, and the Worker reserved-path return before interception. These are bounded source observations, **not** executed tests or security assurance.

## 3. First principles → operational judgment [SOURCE / SYNTHESIS]

1. **Problem/history.** Same-origin scripts share document execution authority; a local-first PWA concentrates valuable offline data and app logic in the browser. CSP was introduced as defense in depth for injection, not as a replacement for encoding, dependency review, authorization or independent backups. The programmable Service Worker adds an independent long-lived fetch/control plane.
2. **Standards.** W3C CSP Level 3 defines `script-src`, `worker-src`, `connect-src`, `frame-src`, `frame-ancestors` and fallback semantics. `script-src-elem` is **not** the `worker-src` fallback. A document's CSP generally does not govern its Worker global: the **Worker script response needs its own CSP**.
3. **Current implementation.** The repository config exposes one catch-all cache header and no source-configured CSP. The root Flutter template and auth action have **different script loading shapes**: same-origin bootstrap vs inline module importing cross-origin Firebase SDK. A single untested global `script-src 'self'` could break auth action; a global `'unsafe-inline'` added solely to make auth work would weaken the ledger surface.
4. **Failure modes.** Remote module compromise or DOM injection on a same-origin document can reach that document's origin-scoped APIs; CSP misconfiguration can break password reset or Flutter startup; Worker policies can be mistakenly assumed inherited; wrong rewrite/header matching can leave aliases unprotected; broad `connect-src` can expand exfiltration destinations; `no-store` does not replace Service Worker cache/IndexedDB controls or external backup.
5. **Cross-domain.** E owns code-execution trust; A owns CSP/Worker/WebKit behavior; C owns live negative controls; B/Design owns accurate action-link errors; D/Marketing owns third-party tag admission and no misleading “secure”/“offline”/ad claims.
6. **Judgment.** **Do not paste a speculative production CSP** into `firebase.json`. First inventory the exact generated NORMAL build and auth module network dependency graph; derive separate route-specific candidate policies; deploy to a disposable authorized preview; exercise allowed and deliberately blocked paths; then stage report-only/enforcement with independent rollback and exact served-header evidence. No destructive origin clearing.

Primary references checked 2026-10-25:
- W3C CSP Level 3: https://www.w3.org/TR/CSP/
- MDN CSP Worker policy and multiple policies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
- MDN XSS/strict CSP: https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS
- Firebase Hosting full configuration, updated **2026-10-21 UTC**: https://firebase.google.com/docs/hosting/full-config
- OWASP Third Party JavaScript Management: https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html

## 4. Shared origin is a security authority boundary, not a pathname boundary [SYNTHESIS / CONTRADICTION]

**Source-positive:** `reserved()` ensures ordinary `/auth` and `/__` fetch paths are passed through to the network rather than rewritten to offline root or cached as an app shell. This avoids one class of stale Worker capture and must be preserved in any refactor.

**Non-implication:** `/auth/action` remains hosted under the same scheme/host/port as the root PWA. A browser executing third-party imported JavaScript within the auth document does not automatically confine that code to the vendor's hostname. If the auth page and ledger are in the **same browser origin and storage container**, hostile same-origin document code may have access to origin-local data unless further architecture/browser isolation prevents it. This is a **conditional threat model**, not a finding that the Firebase SDK reads flight data. iPadOS Safari-tab versus user Home Screen versus managed Web Clip storage containers must be tested independently (507/515).

**Security architecture options (not product decisions):**
- **Option A: keep current shared origin;** minimize executable dependencies, apply audited route-specific CSP and referrer policy, tightly control releases, verify worker bypass and monitor without sensitive telemetry. Lowest migration complexity; same-origin compromise blast radius remains.
- **Option B: isolate sensitive account-action HTML on a separately owned origin;** reduces ambient access to the ledger's origin storage if auth provider/redirect, action-link, email-template, deep-link and return-path contracts all survive. Migration complexity, authentication-domain authorization, user continuity, redirects, link expiry and operational recovery must be tested. Merely choosing another URL **path** or same-origin iframe does not isolate storage.
- **Option C: embed third-party content in a separate-origin sandboxed iframe;** may reduce parent DOM/storage privileges for a genuinely separable third-party surface, but not a drop-in fix for the Firebase action page or a generic ad SDK. `postMessage` must check exact origin/source and schema; sandbox restrictions and navigation/open-in-new-tab behaviors require browser validation.

**Decision status:** do not choose B or C without Engineering/Auth/Product approval. Current source does not prove an urgent migration is required. A source-level CSP/header gap merits **engineering security review**, not a fabricated live vulnerability.

## 5. Route-specific header and script-execution contract [MINTTAP DECISION / PROPOSED / OPEN]

**Policy design contract, not paste-ready config:**

| Response class | Candidate controls to validate | Critical regression and source-dependent allowance |
| --- | --- | --- |
| Root `/`, `/index.html`, Flutter bootstrap and generated JS | CSP `default-src`, `script-src`, `connect-src`, `worker-src`, `object-src`, `base-uri`, `frame-ancestors`; referrer, content type and no-sniff; avoid third-party executable code by default. | Flutter loader/renderer, dynamic imports, Firebase Auth/Identity Toolkit/Firestore endpoints, fonts, WASM/canvas, and offline boot may require narrowly justified exceptions. Determine from exact build and actual network trace. |
| `/auth`, `/auth/`, `/auth/action`, `/auth/action/index.html` | Dedicated document CSP allowing **only reviewed** inline module execution (hash/nonce strategy as technically appropriate), versioned Firebase module dependency graph and required Auth connections; `Referrer-Policy: no-referrer` candidate; anti-framing and safe errors. | A blanket `script-src 'self'` would block the observed cross-origin SDK imports/inline module unless policy is adapted. Verify password reset, email verification, expired/invalid code, offline/network errors, screen reader, redirects and query-token privacy. |
| `/logmate_service_worker.js` and any generated Worker/imported scripts | Worker-script response CSP distinct from document CSP; exact Worker SHA/Content-Type; controlled scope and allowed fetch/connect destinations; cache/version policy. | Parent document policy is not sufficient; Worker lifecycle and offline fallback must remain functional. Test existing/next generation overlap and failure preservation, not only clean install. |
| Public `/privacy`, `/about`, `/account-deletion` | No unexpected script, restrictive CSP where compatible, accurate privacy/support and anti-framing; no personal-data telemetry. | Distinguish public static content from authenticated PWA data; avoid accidentally blocking links/accessible interactions. |
| `/__/...` reserved Firebase routes | Explicitly inventory Firebase reserved endpoints and actual responses; don't assume project-controlled HTML/header config applies to all provider-generated content. | Current Worker bypasses `__/`; verify live reserved routing and don't promote source-only assumptions. |

**Firebase-specific operational detail:** Hosting's `headers` match the **initial request URL before rewrite**; matching rules apply in configured order (official Hosting docs, 2026-10-21). A policy matching only `/auth/action/index.html` cannot be assumed to cover aliases `/auth`, `/auth/`, `/auth/action`. A proposal must enumerate all aliases and independently fetch each effective response. This is a new practical dependency relative to the previous release-byte gates.

**Referrer boundary:** The auth page places `oobCode` in the query. Browser default `strict-origin-when-cross-origin` ordinarily sends only the origin on cross-origin HTTPS subresource requests, **not** the full query, but same-origin requests may carry the full path/query. Thus no leakage is demonstrated. A reviewed `no-referrer` policy is defense in depth; check authentication navigation compatibility, analytics exclusions, server logs and actual redirect chains. Do not log, paste into CI artifacts or report raw action URLs/codes.

**Cache boundary:** `Cache-Control: no-store` governs HTTP caches; it is not proof that IndexedDB, CacheStorage, a previously installed Worker, browser history, or external LBK backups were erased or preserved. Never issue `Clear-Site-Data: storage` or bulk origin deletion as an automatic CSP/Worker incident fix.

## 6. Script integrity, browser compatibility and limitations [SOURCE / CHANGE WATCH]

- **SRI:** Subresource Integrity can bind suitable external `<script>` resources to reviewed bytes; cross-origin SRI requires CORS and a compatible `crossorigin` mode. The current auth page uses inline ES module `import` statements, so a naïve `integrity` attribute on a nonexistent external `<script src>` does not pin the transitive module graph. Review bundling/self-hosting, SDK release integrity and CSP import restrictions with Engineering before selecting an approach.
- **Trusted Types:** `require-trusted-types-for 'script'` can constrain DOM injection sinks where supported, but compatibility and app/library sinks must be measured on **exact Chromium, Safari/WebKit, and managed iPadOS builds**. MDN reports Baseline 2026 support in current versions; this does not mean old EFB OS builds comply. It is not an origin-isolation or third-party-script sandbox.
- **Iframe sandbox:** combining `allow-scripts` and `allow-same-origin` for a same-origin embedded document can defeat sandboxing. A separately owned origin and narrow message contract are necessary if iframe containment is selected.
- **Report-Only:** CSP report-only can expose policy conflicts but reports are not proof of enforcement, absence of XSS or coverage of offline clients. Reports can contain URLs with sensitive query data; use an explicitly approved sanitized endpoint, redact credentials/OOB codes and cap retention. No report collection is authorized here.
- **WebKit/Chromium:** W3C normative policy behavior is not equivalent to browser/OS-specific compatibility or MDM configuration. Physical Safari/Home Screen/managed Web Clip, especially older company-managed versions, remain CHANGE WATCH.

References:
- MDN SRI: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity
- MDN iframe: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
- MDN postMessage: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
- MDN Referrer-Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
- MDN Trusted Types CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for
- MDN Cache-Control: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control

## 7. Ad/analytics cross-track contradiction and authority [TRANSFER VALIDATION / MINTTAP DECISION]

Marketing Manager 437/438 already owns platform monetization eligibility and currently recommends **no PWA web advertising** at release. This study neither duplicates publisher policy nor authorizes ad scripts. It supplies the missing web trust consequence: **adding a third-party top-level script or tag manager to the PWA origin is a code-execution authority change**, not merely a layout or revenue experiment. It may expand access to local flight records and change `connect-src`/offline/recovery behavior. “We don't use logbook data to personalize ads” is a **purpose statement**, not a technical confinement guarantee.

Transfer rule for any future owner-approved web-ad proposal: new origin/trust graph, source and runtime script inventory, vendor update authority, SRI feasibility, frame isolation where supported, storage and outbound-data controls, consent/privacy and offline failure semantics, rollback/revocation, no logbook or UID targeting, and physical managed-iPad eligibility. No ad request may gate local records, backup, restore or authenticated Manual Sync. Native AdMob research remains owned by Marketing and Engineering.

## 8. Adversarial admission campaign (defined, NOT EXECUTED) [VALIDATION / OPEN]

Use disposable accounts, synthetic ledger and fake action codes; never send real `oobCode`, credentials, UID or pilot records into reports or traces.

| Test | Required falsification / independent evidence |
| --- | --- |
| S01–S02 | Capture exact source HEAD, NORMAL artifact tree/Worker hashes and all deployed HTML/JS; fail if Acceptance/stale build is substituted. |
| S03–S04 | Fetch **each** auth alias and root URL over approved HTTPS; record effective CSP, Referrer-Policy, Content-Type, Cache-Control, redirect chain and final body hash; prove headers match initial URL rather than assuming rewrite destination policy. |
| S05–S06 | Root Flutter bootstrap and complete Firebase Auth flows under report-only and then candidate enforcement; fail if allowed modules/connect endpoints are silently blocked. |
| S07–S08 | Intentionally injected disposable inline script and unauthorized external script must be blocked under enforced candidate CSP; a mere report-only warning is NOT PASS. |
| S09–S10 | Worker script response policy, scope, reserved `auth/__` network bypass, first claim and two-generation update; fail if auth navigations become cached root shell or stale 503. |
| S11–S12 | Inspect exact module/network graph and DOM injection sinks; validate SRI/CORS only where actually applicable; negative third-party script replacement must not be promoted as safe. |
| S13–S14 | Fake OOB query + same-origin and cross-origin referrer requests, redirects, logs and CSP reports; assert no raw action code in any external diagnostic channel. |
| S15–S16 | Test wrong-origin/sender/schema `postMessage` and sandbox token misconfiguration in any **future approved** iframe path; not applicable means NOT RUN, not PASS. |
| S17–S18 | Offline cold start and auth action with network unavailable, plus later recovery; ensure no misleading “account verified” and no deletion of local ledger/cache to repair a header issue. |
| S19–S20 | Chrome/Android and Safari tab/Home Screen/actual managed Web Clip with OS/MDM envelope; enforce source→served→runtime evidence separation, and screen-reader/status/keyboard checks. |
| S21–S22 | Inject blocked third-party analytics/ad dependency and simulate vendor outage; core PWA, local record and Manual Sync authority must remain independent. Web ads remain disabled unless separately authorized. |
| S23–S24 | Review incident rollback: restoring old headers cannot silently re-enable unsafe script authority; ensure sanitized telemetry and external LBK recovery survive controlled remediation. |

**Admission verdicts:** `SOURCE_CONFIG_OBSERVED`, `SERVED_HEADER_OBSERVED`, `POLICY_REPORT_ONLY_DIAGNOSTIC`, `ENFORCEMENT_NEGATIVE_TEST_PASS`, `RUNTIME_COMPATIBILITY_PASS`, `DEVICE_POLICY_PASS`, `BLOCKED`, `UNKNOWN`. No roll-up from source config to device or release PASS. A missing live test is **OPEN**, not green.

## 9. Five-track comparison and dependencies [SYNTHESIS / DEPENDENCY]

| Track | Current evidence maturity / risk | Allocation and reusable transfer |
| --- | --- | --- |
| **E Security / Operations** | Highest risk: shared-origin auth action, executable third-party modules, CSP/Worker policy and sensitive local ledger; only source audit now. | **Primary**. Own route policy/trust graph, rollout/rollback, incident and release admission. |
| **A Platform / Browser** | Strong standards/Worker source foundations; browser compatibility, WebKit storage partition and effective header enforcement OPEN. | High dependency. Own exact CSP fallback, Worker response policy, route/storage mechanics. |
| **C Performance / Accessibility / Quality** | Existing 509–514 synthetic oracles and Engineering M006/Q006; no exact LogMate served runtime or managed device PASS. | High dependency. Own independent header/body, positive+negative browser, offline/AT and regression oracles. |
| **B UX / IA / Content** | Design Studio W121/CD127 static evidence saturated; exact runtime/human/AT remains OPEN. | Consume authoritative states; action-code expiry/network failures and “safe offline” copy must not invent successful account recovery. |
| **D Search / Discovery / Analytics** | Marketing 437/438 native candidate and PWA web-ad HOLD; publisher/analytics/runtime eligibility UNKNOWN. | Consume execution boundary; forbid premature web ads, personal-data instrumentation and unsupported security/privacy claims. |

Design Studio Web W121 and Content CD127 explicitly require exact runtime and accessible-state evidence. Engineering Studio M006 supplies bounded browser lifecycle transfer; Q006 warns that CI green may conceal failed semantic oracles. No peer discipline is re-owned here.

## 10. Decision register, contradictions and next checkpoint

**MINTTAP DECISION / proposed security posture (not a product-policy edit):** preserve Worker `auth/__` bypass; keep PWA web ads and tag managers disabled; do not add a universal permissive CSP; require route-specific script and Worker trust review before release; treat action-link query data as sensitive; prohibit automatic origin wipe; demand real served-header and exact-browser negative tests before any security claim.

**OPEN:** production effective headers; exact NORMAL Flutter module/network graph; auth action CSP feasibility; SRI/bundling feasibility; Browser/WebKit/managed-iPad enforcement; whether a separate account-action origin is worthwhile; owner-approved FILE UI and 37-store external restore; actual Firebase Auth/Sync and release evidence.

**CONTRADICTION register:** Worker bypass ≠ separate origin; vendor hostname ≠ vendor-only execution privilege; versioned module URL ≠ content hash; `textContent` source use ≠ universal XSS immunity; source `firebase.json` header absence ≠ live absence; report-only CSP ≠ blocked exploit; global CSP strictness ≠ app compatibility; `no-store` ≠ no IndexedDB; browser tab PASS ≠ managed EFB PASS; ad-purpose privacy text ≠ technical isolation.

**CHANGE WATCH:** W3C CSP/Trusted Types and Chrome/WebKit implementation, Firebase Hosting header/rewrite semantics, Firebase JS SDK module graph, Flutter generated loader/Worker, iPadOS MDM policy, publisher/analytics SDKs. Primary Hosting docs last updated 2026-10-21; sources checked 2026-10-25.

**Adjacent-value check:** This run resolved three connected questions without adding another generic primer: (1) auth action's actual imported-script trust boundary; (2) source-verified Worker reserved-path bypass, correcting a plausible false alarm; (3) Firebase pre-rewrite header matching and differentiated CSP rollout/negative-test admission. The next valuable step requires **Engineering-controlled disposable preview + exact served HTTPS/runtime evidence**, a materially different execution boundary. **Stage 8 applied ACTIVE; Production validation OPEN; PWA release HOLD.** No product/Design/Marketing/Engineering repository modifications.


---

## 2026-10-25 §11 — Action-link bearer-code exposure window and pre-script referrer admission (Track E owner; A/C critical)

**Why revisit this boundary:** §5 already identified the action-code/referrer issue, and §8 defined S13–S14. This addendum resolves a *timing* question that matters to an implementer: **a client-side URL cleanup inside the existing ES module cannot protect requests made before that module body executes**. It is a source-grounded execution contract, not a claim that a real token was leaked. The same-origin URL is a capability-bearing recovery surface; it must not be treated as an ordinary search/analytics landing page.

### Exact current product source, read-only [SOURCE]

Re-read 2026-10-25:
- LogMate `web/auth/action/index.html` blob `39d06a633ab7bee719b3401bc3ac744f8ba175d0`: `new URLSearchParams(window.location.search)` reads `mode` and `oobCode`; `start()` consumes it in `applyActionCode` / `verifyPasswordResetCode`, and the reset form later calls `confirmPasswordReset`. A source scan found **no** `history.replaceState(` and **no** referrer meta policy. `<meta name="robots" content="noindex">` is present. The favicon and Apple-touch-icon links occur **before** the inline `<script type="module">`, whose two Firebase JS imports come from versioned `www.gstatic.com` URLs. This is a bounded source scan, not runtime evidence.
- LogMate `firebase.json` blob `9ac0972e26749215c4a718360c66315c6caf3cc8`: the only source-configured Hosting response header is `Cache-Control: no-cache, no-store, must-revalidate`; **no source-configured Referrer-Policy/CSP**. Three aliases `/auth`, `/auth/`, `/auth/action` rewrite to `/auth/action/index.html`. Effective live headers may differ; no HTTPS capture was performed.
- LogMate `web/flutter_bootstrap.js` blob `a70625e8bda32aafd5dd23822c017d05229f0e63` registers a same-origin scoped Worker; generated Worker source previously reviewed in §2 bypasses `auth/` and `__/` before interception. Bypass is not origin isolation and not proof of effective device behavior.
- Product `MASTER.md` remains authoritative for account-required Firebase UID and current implementation status; this review neither changes owner authority nor assumes production Sync.

**Primary sources rechecked 2026-10-25:**
1. Firebase custom email handlers: https://firebase.google.com/docs/auth/custom-email-handler — Firebase explicitly supplies `mode` and a one-time `oobCode` query parameter; the handler must validate and apply the action.
2. MDN Referrer-Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy — default `strict-origin-when-cross-origin` can send **full path/query to same-origin** requests while sending only the origin to cross-origin HTTPS requests.
3. MDN History.replaceState: https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState — replaces the current history entry's URL; it does not undo the already-sent initial request or earlier resource requests.
4. OWASP Forgot Password: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html — recommends `no-referrer` on password-reset pages carrying URL tokens.
5. Firebase Hosting full configuration: https://firebase.google.com/docs/hosting/full-config — Hosting custom headers match the **initial request URL**, before rewrites; redirect/static/rewrite precedence matters.

### Request chronology and trust-boundary analysis [SYNTHESIS / CONTRADICTION]

| Phase | What is established | What is **not** established |
| --- | --- | --- |
| T0: user opens email action URL | The initial navigation request can contain `oobCode` in its query, as designed by Firebase. This request already reaches the Hosting/server boundary. | URL cleanup cannot retroactively remove it from the initial request, infrastructure traces or email client. Whether logs retain it is UNKNOWN. |
| T1: HTML parser processes `<head>` | The current page lists favicon/touch-icon subresources before the inline module. Under the modern default referrer policy, a **same-origin** subresource request may carry the full action URL, including query, in `Referer`. | No real Chrome/Safari favicon request, header or logging capture exists. Do not report a confirmed leak; browser scheduling differs. |
| T2: module graph loads | Static cross-origin Firebase imports are resolved/fetched before the module body executes. The default modern policy ordinarily sends only the **origin** to those HTTPS cross-origin imports, **not** the query. | Do not falsely accuse `www.gstatic.com` of receiving the token in `Referer`; actual policy, redirects and runtime network trace remain OPEN. |
| T3: module body and async action | The current source reads `oobCode` and uses it for Firebase operations, without replacing the visible URL/history entry. A late `replaceState` would reduce *subsequent* address-bar/history/referrer exposure only. | `noindex`, `Cache-Control: no-store`, Worker bypass and a future `replaceState` are **not** substitutes for a pre-resource referrer policy. |
| T4: success, error, retry, reload | The code may remain in the URL after success or error; the reset flow needs it through the later form submission. | Token reuse/expiry, browser history retention, copy/share, BFCache, reload UX, server-side log scrubbing and MDM browser behavior require separate evidence. |

**Key contradiction:** `strip URL in module body` ≠ `protect pre-module resource referrers`; `cross-origin imports exist` ≠ `cross-origin token leakage`; `noindex` ≠ `token confidentiality`; `no-store` ≠ `history or server-log erasure`; `source header absent` ≠ `live header absent`; `auth path bypassed by Worker` ≠ `separate origin or data container`.

### Bounded operational options — Engineering/Product approval required [MINTTAP DECISION / PROPOSED]

**Preferred defense-in-depth candidate for disposable preview:** apply a **route-scoped `Referrer-Policy: no-referrer` on all four action-document entry URLs** (`/auth`, `/auth/`, `/auth/action`, `/auth/action/index.html`) with initial-URL matching, and verify it on the *served* response. An early HTML `<meta name="referrer" content="no-referrer">` before any subresource is a defense-in-depth candidate if verified; it is not evidence that an HTTP header was delivered. Do not introduce a global policy change without assessing Flutter/Auth integrations.

**Separate, complementary candidate:** parse the one-time code into volatile JS memory and replace the current history URL promptly, preserving only reviewed nonsecret parameters. The existing inline module is too late to be the **sole** mitigation for parser-initiated requests. Test the one-time password-reset form, error/retry, reload and navigation consequences before changing code. Never persist `oobCode` in localStorage, IndexedDB, logs, analytics, exception reports, CI artifacts, screenshots or query-bearing telemetry.

**Control-plane constraint:** a CSP `report-uri`/`report-to` collector and browser error telemetry can themselves contain `documentURL` or source URLs. Redaction must happen before retention/third-party delivery. An authorized diagnostic capture uses a disposable fake/expired code, never a real email action or pilot account. Any server-side request-log filtering needs separate Hosting/provider review; client history cleanup cannot sanitize upstream logs.

### Falsifiable execution packet [VALIDATION / OPEN]

All cases pin exact NORMAL build SHA, approved preview origin, initial URL/alias, response headers, browser/OS, profile/container, source of synthetic token, time, sanitized oracle and PASS/FAIL/UNKNOWN. Never paste full query-bearing URL into a test report.

| ID | Positive + negative control | Required evidence tier |
| --- | --- | --- |
| A01 | Fetch each of four aliases; `no-referrer` present on **each actual response** and absent-policy negative fixture visibly differs. | Approved HTTPS capture; no cached-only response |
| A02 | Same-origin favicon/icon/font request with disposable query; capture actual `Referer`; compare no-policy vs no-referrer. | Real Chromium and native Safari separately |
| A03 | Cross-origin Firebase module request with disposable query; verify only allowed origin/no full query, not presumed third-party leakage. | Actual browser network trace, redacted |
| A04 | Assert first navigation's query still reaches initial server boundary even when `replaceState` runs; verify log-retention/redaction configuration independently. | Authorized Hosting/provider logging review |
| A05 | Test `replaceState` before/after async validation, success/error, browser Back and reload; ensure the one-time code remains available in volatile memory until legitimate form submit, without replay authority. | Exact action handler in disposable Auth environment |
| A06 | Valid/expired/invalid/fake codes and offline/network interruption must show truthful action state and accessible errors, never a false success or local-ledger reset. | Engineering Auth + Track B/C human/AT |
| A07 | CSP enforce/report-only probes cover inline module, transitive Firebase imports and connection endpoints; report-only must not count as blocking. | Chromium and native Safari |
| A08 | Worker scope/exclusion and cached/uncached navigation of each alias; no root-shell substitution or stale offline success. | Product NORMAL browser runtime |
| A09 | Check query absence from CSP reports, analytics, third-party tags, crash reports and CI artifacts using disposable markers; negative injected telemetry must fail. | Approved privacy/observability test |
| A10 | Same-origin storage access and managed iPad tab/Home Screen/Web Clip are classified by actual container/MDM envelope; no inference from desktop Chrome. | Physical managed iPad separately |
| A11 | Test redirect chain and Firebase `/__/...` reserved routes; distinguish provider-managed response policy from project Hosting rules. | Served HTTPS + disposable Auth |
| A12 | After password reset or verification, confirm user can return to the app without interpreting link success as local ledger rebind, external backup or Manual Delta Sync completion. | Product Auth/UX integration |

**C / negative oracle:** each test must prove its intended positive baseline and its deliberately failing control. Missing trace, policy or precondition is UNKNOWN, never PASS. A source scan is not a runtime assertion.

### Five-track allocation and transfer [DEPENDENCY / TRANSFER VALIDATION]

- **E (primary bottleneck):** bearer-code custody, route-specific policy, provider log/redirect boundary, release/incident governance. Own this reusable finding here; no new micro-primer.
- **A:** browser referrer algorithm, parser/module timing, Service Worker control and Safari/Chromium differences. This supplies mechanics rather than a duplicate security policy.
- **C:** independent HTTP/network trace, negative controls, auth regression, accessibility and device validation. No automated WebKit result promoted to Safari.app/managed EFB.
- **B:** Design Studio W121/CD127 requires visible/accessible/action-state parity for reset success, expired code, interrupted connection and return-to-app; URL cleanup must not silently destroy recovery usability.
- **D:** Marketing 438 owns advertising policy; PWA web ads remain excluded by default. Web analytics/search must never capture action codes. `noindex` is a discovery directive, not a security mechanism.
- **Software Engineering D006:** account-action success and a subsequent Manual Delta Sync receipt/apply are separate state transitions. Engineering owns product implementation and the authorized disposable runtime.

**Next major checkpoint:** Engineering-approved disposable HTTPS auth preview and exact NORMAL artifact, then independent alias/header/referrer/CSP/network captures with negative controls. If this execution is unavailable, preserve the source-level risk as **OPEN**, not a production leak claim. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.** No LogMate or peer repository was modified.


## §12 — Auth action route-policy completeness, permanent redirect custody and negative-oracle execution (2026-10-26 KST)

**Owner:** E security/Hosting response policy; A supplies HTTP/URL/browser mechanics; C owns execution and falsification; B/D consume UX/privacy implications. **Scope:** disposable Firebase Hosting Emulator and read-only LogMate source, not deployed HTTPS, real Auth, Safari or EFB. **Current gate:** Stage 8 applied ACTIVE / Production validation OPEN / PWA release HOLD.

### SOURCE — exact product and standards

- Re-read LogMate `web/auth/action/index.html@39d06a633ab7bee719b3401bc3ac744f8ba175d0` and `firebase.json@9ac0972e26749215c4a718360c66315c6caf3cc8` from `main`: the action document reads `mode` and `oobCode` from the query; the Hosting source has global `Cache-Control: no-cache, no-store, must-revalidate` but no explicit `Referrer-Policy`. Three aliases rewrite to the action document; `auth/action/index.html` exists as static content. No production response or disclosure was observed.
- Firebase Hosting primary documentation (rechecked 2026-10-26): https://firebase.google.com/docs/hosting/full-config . Custom response-header rules match the **initial requested URL before rewrites**, and configured redirects/exact static precede rewrites. A header rule matching only `/auth/action/index.html` cannot be assumed to protect a browser request to `/auth` merely because that request is rewritten to that file.
- RFC 9110 §15.4.2: https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4.2 . A `301` is heuristically cacheable **unless** explicit controls or method rules override it. This is a general property, **not evidence that the LogMate redirect was cached**. The product's global `no-store` declaration must be checked on the actual **redirect response**, not inferred from the final 200.
- MDN Referrer-Policy (rechecked 2026-10-26): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy . Default `strict-origin-when-cross-origin` can include the complete action URL/query on same-origin resource requests; `no-referrer` suppresses the `Referer` header but **does not remove the original navigation URL or redirect `Location` query**. OWASP password-reset guidance recommends `no-referrer` for reset pages with URL tokens: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html .
- Existing executed [504 emulator checkpoint](504_stage8_pwa_normal_artifact_custody_hosting_projection_execution_contract_20261023.md) established, on Firebase CLI 15.34.1 synthetic fixtures, that `/auth/action` returns `301 → /auth/action/ → 200 AUTH` with a **non-secret** query preserved. This is an HTTP emulator result, not a Chromium/Safari Referer trace.

### SYNTHESIS — five document-entry paths plus the redirect hop

| Initial request path | Prior synthetic baseline | Why separate policy admission is required |
| --- | --- | --- |
| `/auth` | 200 action HTML through rewrite (no shadow file) | Response-header matching uses `/auth`, not rewrite destination. |
| `/auth/` | 200 action HTML through rewrite | Slash alias is a separate requested path; adding `auth/index.html` changes content. |
| `/auth/action` | 301 to slash path | Redirect response and target response are **two** distinct HTTP-policy/caching observations. |
| `/auth/action/` | 200 action HTML | This is the actual redirect target; it was omitted from the earlier four-path header proposal in §11. |
| `/auth/action/index.html` | 200 exact static action HTML | A destination-only header rule can protect direct static requests but not the other aliases. |

**CORRECTION to §11 proposal:** the earlier “all four action-document entry URLs” wording omitted `/auth/action/`. The **five** requested document paths above require individual admission or a proved equivalent matching expression. In addition, `/auth/action` has an initial **301 hop** whose own headers/cache behavior must be recorded. This is a research-proposal correction, not a product change or production vulnerability finding.

**CONTRADICTIONS to reject:** `final 200 has no-referrer` ≠ `301 had no-referrer/no-store`; `rewrite destination protected` ≠ `all aliases protected`; `header attached` ≠ `query removed from initial request/redirect/provider logs`; `query preserved` ≠ `token leaked to third party`; `no-store configured` ≠ `all intermediaries and browsers demonstrably did not retain the redirect`; `policy applied` ≠ `correct Auth HTML served` (static-shadow counterexample).

### VALIDATION — executable, credential-free negative controls

Extended the **existing** `research/handoffs/test_firebase_hosting_auth_route_emulator.mjs` rather than creating a new micro-lab. The pinned workflow `.github/workflows/pwa_hosting_auth_route_emulator_research.yml` executes on pushes to this harness. Its five synthetic cases are: original baseline without policy; static-shadow baseline; five-alias route-scoped `no-referrer`; policy plus static shadow; and **rewrite-destination-only** policy as an intentional negative control. The script records initial/final status, policy and cache-control headers separately, tests final HTML identity, and logs only Boolean query preservation with a non-secret sentinel. It must not log real `oobCode` or a full query URL.

**Falsifiable acceptance:** every protected alias must serve the intended AUTH sentinel and expose `Referrer-Policy: no-referrer` on the final document; root remains unmodified; baseline has no referrer policy; shadow is still rejected by content identity even if it carries the policy; destination-only policy must not masquerade as protection of rewrite aliases. Redirect-hop header/caching observations remain separately classified and are **not** inferred from the final 200. Source-only or pending Actions code is **not PASS**; exact run ID/conclusion and observed response fields are required before promoting this emulator gate.

### MINTTAP DECISION — bounded proposal / OPEN

For an Engineering-approved disposable preview, evaluate a route-scoped policy covering all **five** initial action-document URLs and test both 301 and 200 responses; do not automatically deploy a global policy or assume that rewriting to a protected destination is sufficient. Check 301 `Cache-Control`, `Location` query preservation, Referrer-Policy, redacted provider/CDN logs, browser history, same-origin icons/fonts, cross-origin module requests, CSP telemetry, real Auth error/retry and accessible return-to-app states. Do not change Firebase Auth handlers or remove `oobCode` before the password-reset form retains a valid in-memory code. A safer canonical email action-link path (avoiding a redirect) is a **candidate**, not an approved migration; email templates, Firebase authorized domains, old-link compatibility and operational rollback require Engineering/Auth ownership.

**TRANSFER VALIDATION:** A supplies actual browser request/referrer semantics; C must reproduce negative controls in real Chromium then native Safari and distinguish initial 301 from final 200; B consumes Design Studio's mandatory semantic/focus/recovery gate, with password-reset completion separate from local ledger/Sync status; D consumes Marketing Manager D8/D10 claim HOLD and forbids query-bearing action links in analytics, campaign attribution or advertising surfaces. Product-specific managed-iPad/MDM/storage and 37-store recovery remain independent OPEN gates.

**CHANGE WATCH:** Firebase CLI/Hosting redirect behavior, Chrome/Safari referrer policy, OS-managed Web Clip container, Firebase email-handler action URL shape and HTTP caching intermediaries. **Next meaningful evidence:** exact hosted emulator result, then an authorized NORMAL artifact + HTTPS response/browser capture; no synthetic HTTP pass may promote production or managed-iPad release.


### §12 executed hosted checkpoint — 2026-10-26 KST [VALIDATION]

The exact GitHub Actions workflow at `8468a86dc9f8d3d4341476b92afbe756ea3eec29` completed **SUCCESS**: [run 40205657315](https://github.com/yhappcom/web-manager/actions/runs/40205657315), job `121205908261`, Node 22.16.0, Firebase CLI 15.34.1, five synthetic cases with independent negative controls. The earlier four-case intermediate [run 40205633796](https://github.com/yhappcom/web-manager/actions/runs/40205633796) also completed SUCCESS but is **not** the final destination-only counterexample source.

**Observed from exact hosted job log, not assumed from source:**

| Fixture | Initial requested path | Initial HTTP | Initial `Referrer-Policy` | Final `Referrer-Policy` | Distinct content/interpretation |
| --- | --- | --- | --- | --- | --- |
| No-policy baseline | `/auth`, `/auth/`, `/auth/action`, `/auth/action/` | 200 / 200 / 301 / 200 | absent | absent | AUTH HTML on final; demonstrates default exposure surface is not a configured header. |
| Five-path protected | all five document paths | 200 except `/auth/action` 301 | `no-referrer` | `no-referrer` | All five final documents AUTH; root policy absent. |
| Protected + static shadow | `/auth/` | 200 | `no-referrer` | `no-referrer` | **SHADOW**, not AUTH: header success alone cannot prove correct routing. |
| Destination-only policy | `/auth/action/index.html` | 200 | `no-referrer` | `no-referrer` | Direct exact static request protected. |
| Destination-only policy | `/auth`, `/auth/`, `/auth/action`, `/auth/action/` | 200 / 200 / 301 / 200 | **absent** | **absent** | Same AUTH bytes via alias do **not** inherit rewrite-destination-only header. |

In the five-path protected fixture, the **initial 301** for `/auth/action` explicitly carried `Referrer-Policy: no-referrer` **and** `Cache-Control: no-cache, no-store, must-revalidate`; the final 200 carried both as well. This closes the **pinned emulator header observation** that §12 previously left unverified. It does **not** prove HTTPS CDN behavior, browser cache retention, absence of upstream request logs, or a real token's secrecy. The non-secret synthetic query remained in the navigation/redirect URL despite the policy, as expected.

**Gate change, strictly bounded:** `synthetic Firebase Hosting route-scoped header / 301 policy / destination-only false-green NEGATIVE PASS`. No LogMate source or live Hosting configuration changed. **Production validation OPEN / PWA release HOLD.** Next material question is real Chromium/Safari same-origin `Referer` behavior and actual approved HTTPS action-link delivery; physical managed iPad/37-store restore remain separate evidence tiers.


**Final fail-closed promotion — 2026-10-26 [VALIDATION]:** Follow-up [hosted run 40205883570](https://github.com/yhappcom/web-manager/actions/runs/40205883570) at exact harness commit `e0a0e1a21405a75a7907958ffd09dd6f15fd0192`, job `121206591637`, completed **SUCCESS**. The research harness now **asserts** (rather than only reports) the initial `/auth/action` 301 `Referrer-Policy: no-referrer`, initial and final `Cache-Control: no-cache, no-store, must-revalidate`, and the negative baseline's absent policy. This makes redirect-hop header regression fail closed in the pinned synthetic emulator. It is not a browser `Referer` trace or evidence of production policy deployment. **Synthetic Hosting gate PASS; Production validation OPEN; PWA release HOLD.**


## §13 — Actual browser `Referer` vs Hosting header: synthetic network evidence program (2026-10-26 KST)

**Owner / gate:** Track E owns the sensitive-action URL security and operational policy. Track A supplies Referrer Policy / Fetch / navigation mechanics; Track C owns the browser-level independent oracles. Track B and D consume state-truth and telemetry constraints. **Stage 8 applied security ACTIVE; product HTTPS, Safari and managed EFB OPEN; PWA release HOLD.** This section builds on §12's executed Firebase Hosting HTTP-emulator gate; it does **not** promote synthetic behavior to product deployment.

### SOURCE — history, standard and exact product boundary

- **Problem/history:** Email verification and password-reset links commonly carry a short-lived bearer-like action value in the URL. An HTML document can cause same-origin resource requests before application JavaScript processes the code. An HTTP response policy, the browser's navigation/referrer computation, URL history mutation and provider logging are distinct mechanisms. The old default `no-referrer-when-downgrade` must not be assumed; current default is `strict-origin-when-cross-origin`.
- **Normative platform:** W3C Referrer Policy living editor's draft https://w3c.github.io/webappsec-referrer-policy/ (document/client policy, default, `no-referrer`, same-origin full URL vs cross-origin origin); WHATWG Fetch living standard https://fetch.spec.whatwg.org/ (request referrer/policy and redirect processing); MDN https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy (current implementation explanation); MDN https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState (history entry mutation, not reversal of a completed network request). Rechecked 2026-10-26.
- **Security guidance:** OWASP Forgot Password Cheat Sheet https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html explicitly recommends a `no-referrer` policy on reset pages; OWASP WSTG https://owasp.github.io/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication/09-Weak_Password_Change_or_Reset_Functionalities likewise treats token-bearing Referer exposure as a test target. Neither proves a LogMate incident.
- **Provider:** Firebase Hosting https://firebase.google.com/docs/hosting/full-config documents header matching on the **original request path** before rewrites. §12's pinned emulator verified five action entry paths and an initial `/auth/action` 301 hop, including route-scoped `no-referrer` and `no-store` negative controls.
- **Product SOURCE, read-only:** `yhappcom/logmate/main:web/auth/action/index.html` contains favicon and Apple Touch Icon references in the head and an `@font-face` same-origin asset; the module later parses `mode`/`oobCode`. `firebase.json` currently has global `Cache-Control: no-cache, no-store, must-revalidate`, three action rewrites, and **no** explicit `Referrer-Policy`. Exact reviewed files are source evidence, not served-response or token-exfiltration evidence. Never record real `oobCode` in the research harness.

### SYNTHESIS — distinct security boundaries and counterexamples

| Boundary | What it can establish | What it cannot establish |
| --- | --- | --- |
| URL initial navigation / 301 `Location` | Whether action parameters reach the document | Whether logs, address bar, history, screenshots, intermediaries or email clients did not retain the query |
| Response `Referrer-Policy: no-referrer` | Suppresses `Referer` on requests made from that protected document | Removes the original URL query, prevents all server-side request logging, or retroactively erases prior requests |
| Default `strict-origin-when-cross-origin` | Same-origin full URL and cross-origin origin-only behavior, under ordinary matching conditions | A blanket statement that all third parties receive the code, or that same-origin paths cannot expose it |
| `history.replaceState` | Changes the current history entry URL after execution | Retroactively changes previously transmitted `Referer` or initial request URL |
| Header applied only to rewrite destination | Can protect a direct request for that destination | Covers `/auth`, `/auth/`, `/auth/action` or `/auth/action/` automatically |
| CSP / Worker exclusions / `no-store` | Constrain distinct execution, interception and HTTP caching surfaces | Substitute for referrer policy, logging minimization, token lifetime/single-use or account-action correctness |
| Browser pass | Demonstrates specific browser/version and local fixture | Product CDN/HTTPS, Safari/WebKit, MDM EFB, external backup or native Sync behavior |

**Important conditional risk:** Under the default policy a same-origin icon/font/script request *can* carry the full action URL as `Referer`, including a code. A third-party module under the default policy usually receives origin-only, not the full code. The relevant confidentiality boundary includes same-origin access logs, resource delivery, monitoring, analytics and any same-origin worker interception. This is a potential exposure path, **not** proof of access by an attacker or Firebase leakage.

**Temporal ordering:** A late `replaceState` call may protect the current address/history and later requests while leaving earlier parser-triggered resources unaffected. A response header is preferable to relying solely on late application JavaScript; a CSP or HTML meta policy has its own delivery timing and must be separately assessed. Removing the query before the application retains its valid action value could break password reset; Auth Engineering must own any migration.

### VALIDATION — independent, fail-closed Chromium request oracle

Added [credential-free Chromium network lab](handoffs/pwa_auth_referrer_chromium_lab.mjs), [17 independent classifier regressions](handoffs/test_pwa_auth_referrer_chromium_lab.mjs) and [pinned hosted workflow](../.github/workflows/pwa_auth_referrer_chromium_research.yml). Node 22.16.0 classifier checks include missing resource requests, wrong same-origin token exposure, unexpected cross-origin full URL, invalid referrer, redirect/query loss, browser timeout and absent DOM completion marker. **Local Node 22.16.0 classifier 17/17 PASS**; the container's local Chromium 144 headless process timed out without reaching the loopback fixture, so **local real-browser evidence is UNKNOWN, not PASS**.

The isolated HTTP fixture exercises six conditions: default policy; `no-referrer`; history cleanup only; combined header and cleanup; a redirect with header on both hop and document; and a redirect with policy only on the final document. It observes early same-origin script, late same-origin script and a separate-port cross-origin script. It records only Boolean `Referer` properties and query-preservation flags, never raw request URLs, `Referer` values or real action codes. All cases require an actual completed Chromium process, expected document marker, **three observed network requests**, and expected header behavior. This is a **loopback HTTP** experiment: neither HTTPS CDN behavior nor Safari support is inferred. The hosted workflow must be judged by its exact run conclusion and job log, not by existence of the script.

**Negative controls / false-green defenses:** A missing resource must not count as `no-referrer` success. A page that failed to load cannot count as a privacy PASS. An expected same-origin code must be observed in the default control, otherwise the policy test is not discriminating. Cross-origin requests are measured separately; `no-referrer` is not conflated with origin-only. A 301 query-preservation check is separate from the final page's resource-request policy. A clean address bar is not proof of clean initial logs.

### Five-track transfer and operational judgment

- **E (owner):** Maintain route-scoped policy admission for five action entry paths **plus** initial 301 hop; require content identity, response status/Location, Cache-Control and Referrer-Policy. Require redacted CDN/Hosting/observability log review, token invalidation/lifetime and recovery/incident handling under Auth owner. Do not silently edit LogMate.
- **A (supplier):** Distinguish initial navigation, redirected navigation, document client policy, same-/cross-origin requests, resource timing, Worker scope and history API; Chrome evidence does not prove Safari/iPadOS.
- **C (challenger):** Browser requests are the oracle, not the HTML policy string alone. Assert a positive control and missing-request failure; then reproduce on approved HTTPS product bytes, Safari and managed iPad with a disposable non-production account. No real code in logs.
- **B (consumer):** Design Studio `DESIGN_SYNTHESIS_GATE_20260919.md` and `INTEGRATION_PRINCIPLES_20260919.md` require truthful pending/error/recovery state, keyboard/focus and semantic equivalence. Account-action success cannot be inferred from `200`, 301 or an accessible-looking screen; verify password-reset completion and expired-link retry separately from flight-data Sync.
- **D (consumer):** Marketing Manager `STATUS.md` D8/D9 keeps PWA/Sync claims and launch visuals HOLD. Do not send query-bearing action URLs to attribution, analytics, advertising, search indexing or support screenshots. A local synthetic browser test is not acquisition/production evidence.
- **Engineering dependency:** Exact NORMAL build custody, approved HTTPS preview, Firebase Auth action link/domain, early token handling and redacted network trace require product/Software Engineering authorization and implementation. Web Manager owns the web-medium acceptance contract, not the Auth implementation.

**MINTTAP DECISION (proposal, not product change):** Prefer response-header protection on **every action entry path**, plus early in-memory capture and safe history cleanup where Auth flow supports it; verify 301 and 200 independently. Do not claim global `no-referrer` is automatically safe for unrelated site analytics. Do not remove query parameters before Firebase action handlers can use them. Treat a direct canonical link that avoids the normalization 301 as an engineering candidate requiring template, authorized-domain, old-link and rollback review.

**OPEN:** Exact hosted Chromium run and request fields; HTTPS CDN response policy, initial access logs, actual token retention, browser history, Safari/Home Screen, managed EFB Web Clip, production action-link UX, NORMAL PWA artifact and 37-store restore. **CHANGE WATCH:** Chromium/Firefox/WebKit Referrer Policy, WHATWG redirect processing, Firebase CLI/Hosting route precedence, iPadOS/MDM constraints. **Release HOLD remains unchanged.**


## §14 — Executed Chrome 155 `Referer` timing / speculative-parser counterexample (2026-10-26 KST) [VALIDATION / CONTRADICTION]

**Final exact hosted execution:** [GitHub Actions run 40210704513](https://github.com/yhappcom/web-manager/actions/runs/40210704513), source `33cbf5c6fc6048d173fa6245f76c3aebf31f44bf`, job `121221102970`, **SUCCESS**. Hosted Node **22.16.0** classifier regressions **19/19 PASS**, actual **Google Chrome 155.0.8059.39** on disposable HTTP loopback **6/6 browser cases PASS**. All six required completed Chrome process, completed fixture DOM and observed same-origin early/parser-late/dynamic-post plus cross-origin script requests; redirect cases additionally required query continuity. No real tokens, accounts, production build or external origin were used.

**Why a negative first attempt mattered:** [Run 40210568736](https://github.com/yhappcom/web-manager/actions/runs/40210568736) at `7c218420` had 17/17 classifier tests PASS but **browser FAIL in cleanup-only**: the supposedly *late* static script still sent the full original URL query in `Referer` after an inline `history.replaceState` call. Treating DOM source order as request initiation order was a **test-model defect**. MDN's [speculative parsing explanation](https://developer.mozilla.org/en-US/docs/Glossary/Speculative_parsing) and Mozilla's [preload-scanner history](https://hacks.mozilla.org/2017/09/building-the-dom-faster-speculative-parsing-async-defer-and-preload/) explain how browsers may request parser-visible resources ahead of a blocking script. The first browser result alone did not prove which initiator won the race.

**Independent causal discriminator:** The revised fixture keeps the parser-visible static `late.js` but adds `post.js` using a parser-blocking `document.write` **after** the inline history cleanup. The latter URL is absent as a fetchable tag from the original HTML byte stream, so it cannot be discovered by the original markup's preload scanner before the cleanup script runs. The revised oracle fails if any expected request is absent, and the 19 classifier tests include missing post-request and wrong post-request `Referer` negatives.

| Chrome 155 synthetic case | Early same-origin contains sentinel | Parser-visible late same-origin contains sentinel | Post-cleanup dynamically written same-origin contains sentinel | Cross-origin request | Verdict |
| --- | --- | --- | --- | --- | --- |
| No policy, no cleanup | yes | yes | yes | origin-only, no sentinel | PASS |
| Response `no-referrer` | no | no | no | absent `Referer` | PASS |
| `replaceState` only | **yes** | **yes** | **no** | origin-only, no sentinel | PASS |
| Response `no-referrer` + cleanup | no | no | no | absent `Referer` | PASS |
| 301 + final 200 both protected | no | no | no | absent `Referer`; synthetic redirect query preserved | PASS |
| 301 without policy, final 200 protected | no | no | no | absent `Referer`; synthetic redirect query preserved | PASS |

**SYNTHESIS / operational consequence:** This experiment supplies an actual Chromium request-level distinction between parser-visible resources and a request constructed only after cleanup. In this version/context, the post-cleanup request omitted the synthetic code while the static later-in-markup script did not. Therefore `replaceState` alone is not a safe pre-resource secrecy control, **even if it is textually placed before a later static resource**. Header-based `no-referrer` prevented `Referer` on all three same-origin and the cross-origin script probes. A protected final document also protected its subresources even where the initial 301 lacked the header, but the 301's own response policy/cache/logging is a **separate requirement**; this does not overturn §12's initial-hop gate.

**Evidence hierarchy:** This is an executed **Chrome 155 synthetic loopback HTTP** result, not a demonstration of a LogMate production leak. The first failed browser run was an incorrect temporal oracle, not evidence of a Chrome privacy regression or an incident. The successful run does not prove exactly which internal Chrome preload initiator fetched `late.js`; a DevTools/CDP initiator and timestamp trace would be needed for that narrower attribution. It also does not prove HTTPS/CDN behavior, Safari/WebKit, Home Screen, managed iPad, action-token invalidation, log retention, PWA update or 37-store durability.

**MINTTAP DECISION (bounded):** Maintain the proposed action-route HTTP `Referrer-Policy: no-referrer` on **all five requested URLs** and initial redirect hop; do not replace it with late JavaScript cleanup. Preserve valid action code in memory before removing the URL where Auth Engineering approves; test actual reset/verification, expired-link recovery, icon/font requests and accessibility. Require exact NORMAL artifact + authorized HTTPS preview + redacted server/browser evidence before product promotion. **Stage 8 synthetic Chromium `Referer` gate PASS; Production validation OPEN; PWA release HOLD.**

**TRANSFER VALIDATION:** A supplies parser/preload and policy mechanics; C retains observed-network positive and negative oracles; E owns response policy, initial access-log exposure and incident boundary; B preserves truthful auth/recovery UI and focus; D forbids token-bearing analytics/marketing links. **CHANGE WATCH:** Chrome/WebKit preload timing and Referrer Policy, Firebase Hosting redirects/headers, OS-managed browser and Web Clip policy. Next major checkpoint should be an **authorized product HTTPS** proof, not more synthetic case inflation.


## §15 — Public account-deletion request versus verified erasure: Store-policy, Auth and managed-PWA admission (2026-10-26 KST)

**Owner and stage:** Track **E** owns privacy/security/operations and the externally reachable deletion-request surface; Track **A** supplies origin/Worker/session/browser-container mechanics; **C** owns independent request-to-completion and negative validation; **B** owns truthful deletion/recovery information architecture using Design Studio evidence; **D** owns web discoverability and Store-link/measurement truth. This is **Stage 8 applied security/privacy/trust**, not an implementation of the Software Engineering S007 saga. LogMate, Design Studio, Marketing and Software Engineering are **read-only**. The account-deletion web page is already present in product source; the old “no web deletion resource” handoff is **outdated as a source-inventory statement**, but public delivery and real erasure remain OPEN.

### 15.1 Historical problem → standards/policy → product-source reality [SOURCE]

Account creation on mobile creates a durable obligation to let a former user request removal even when the app is uninstalled, the device is inaccessible, the account is locked, or a managed EFB forbids the app. This is different from a “sign out” action or deleting the Firebase Auth identity alone. The user-facing request, ownership verification, provider revocation, remote data erasure, local-data disposition and proof of completion are separate events; distributed failure can interrupt between them.

**Primary sources checked 2026-10-26:**
- Google Play, *Understanding Google Play's app account deletion requirements*, https://support.google.com/googleplay/android-developer/answer/13327111 : account-creating apps need an in-app path **and** a functional web resource that lets users request account and associated-data deletion without reinstalling the app. The external method **may be a customer-service email address**, form or direct request link; it must be discoverable, relevant to the app and usable. Store Data safety URL declaration and actual service-provider data deletion are separate obligations. Legitimate retention must be disclosed.
- Apple App Review Guideline **5.1.1(v)**, https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion : an in-app deletion initiation path is required; a support email/call/chat **cannot generally be imposed as the in-app deletion route** except in the stated highly regulated cases. Reauthentication is permitted when proportionate. Manual fulfillment can be acceptable with expected timing and confirmation. Apple-linked accounts require token-revocation consideration. Apple also notes a **conditional** server-to-server notification endpoint requirement for developers based in the Republic of Korea registering a new Services ID; the exact developer/Services-ID facts here are **UNKNOWN**.
- Apple TN3194, https://developer.apple.com/documentation/technotes/tn3194-handling-account-deletions-and-revoking-tokens-for-sign-in-with-apple : revocation, developer-held account-data deletion and credential-revoked notifications are distinct. Lack of an available Apple revocation token does **not** excuse account-data deletion; use the documented fallback/manual provider-disconnection process. Do not assert a successful revocation without provider evidence.
- Firebase Flutter *Manage Users*, https://firebase.google.com/docs/auth/flutter/manage-users : deleting an identity is a security-sensitive action requiring recent sign-in. This API is **not** an oracle for product-data or device-local erasure.
- OWASP *Forgot Password Cheat Sheet*, https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html : account-recovery flows are enumeration/abuse surfaces; use safe messages, rate limiting, single-use secrets where relevant. **Transfer principle only**: deletion request intake must not disclose whether an address exists, accept unauthenticated destructive commands, or send bearer credentials to support.

**Exact LogMate `main@4101ec7380796300f68fa60dbc7e5b6061f00080` source read 2026-10-26:**
- `web/account-deletion/index.html` blob `f8558e921c3f72743189a82d6f9cefe81b6fb193` is an English public **static information/request page** with a canonical URL `https://logmate.minttap.app/account-deletion`, an in-app Settings instruction, a `mailto:support@minttap.app?subject=LogMate%20account%20deletion%20request` route, “do not send password or authentication codes,” intended deletion scope, exported-copy caveat, limited retention and manual completion contact.
- `web/privacy/index.html` blob `ca465aaa281ee929941f31fdb3ba6ae136de7d47` §11 links to `/account-deletion`; `web/about/index.html` and `web/support/index.html` also link to it. This supports **source-level navigation/discoverability**, not public HTTP availability, search indexing, Play Console acceptance or actual mailbox handling.
- `firebase.json` blob `9ac0972e26749215c4a718360c66315c6caf3cc8` declares `build/web` as Hosting public directory and no dedicated deletion-path rewrite. Source presence in `web/` alone does not prove its byte-identical presence in an approved NORMAL archive or served HTTPS response. The generated Worker is reviewed separately in §2 and excludes `auth` and `__/`; **no source-backed assertion that it also bypasses `/account-deletion`** is made. Check exact built Worker/route behavior before relying on fresh public instructions.
- `MASTER.md` §0 and `docs/specs/startup-and-auth-entry-spec.md` prescribe a durable `local lock → same-UID reauth → provider revoke → remote erase → Firebase identity delete → local wipe` saga. The latter explicitly lists **deployed erasure/revocation adapters, Settings confirmation UI and the external resource as OPEN** at its recorded revision; `MASTER.md` later acknowledges that the **static policy/request-channel source exists** while public deployment, manual request operations and remote adapters remain **NOT VERIFIED**. Read latest authority by **scope and date**, not as an invented contradiction that the HTML file is absent.
- `lib/application/account_deletion_coordinator.dart` blob `8e844e888b39d3b5e1648aeb84be26e6582ed60f` defines typed reauth, provider revoke, remote erasure and identity deletion ports and advances durable phases. `test/application/account_deletion_coordinator_test.dart` blob `54dac071bf0cd34a93dd674cff5f5106037079d0` uses **in-memory fake ports** to test same UID, remote failure/resume and UID mismatch. Those tests are **not** evidence of deployed remote erasure, actual provider revocation, public request intake or cross-device deletion.
- Software Engineering Studio `research/systems/S007_account_deletion_reauthentication_revocation_saga.md` (2026-09-24) owns the general saga and provider ordering; it correctly requested a Web Manager public deletion surface. The product now has a **static page**, so the handoff narrows to **operational reachability, verification, service intake and closure evidence**, not building another duplicate page.
- Design Studio `case-studies/logmate/DESIGN_SYNTHESIS_GATE_20260919.md`, Content CD127 and Web W121 require semantic truth and exact-build accessible state/action evidence before visual/wording promotion. Marketing 438's PWA no-ad and unverified capability-claim HOLD remains applicable; no analytics/advertising instrumentation belongs on a sensitive deletion request.

**External verification attempt:** a fresh public GET of `https://logmate.minttap.app/account-deletion` and `/privacy` was **not successfully observed** in this run (web retrieval returned inaccessible; local container DNS resolution was unavailable; an alternate page-fetch provider had no execution capacity). This is **NOT_EXECUTED/UNVERIFIED public reachability**, **not evidence that the public site is down**. No mail was sent and no deletion was requested.

### 15.2 Policy and actual capability are not transitive [SYNTHESIS / CONTRADICTION]

| Claim | Source evidence | What is still required / contradiction |
| --- | --- | --- |
| Google Play external resource exists | Static `/account-deletion` page and explicit email request path | Public HTTPS GET/redirect/body, functioning intake, operator receipt/status and correct Play Console URL **OPEN**. Google permits email as external intake; this is **not** proof the mail arrives or is processed. |
| Apple in-app deletion | Product contract and coordinator + in-memory tests | Actual discoverable Settings UI, same-UID reauth, non-email-only completion path and provider-specific behavior **OPEN**. The Google-acceptable external support email cannot substitute for Apple's ordinary in-app path. |
| Remote data erased | `RemoteAccountErasurePort` interface and fake test | Deployed authorized coordinator, idempotency, data-inventory deletion receipts, service-provider handling and retry after partial failure **OPEN**. |
| Firebase identity deleted | `FirebaseIdentityDeletionPort` interface and fake test | Actual Firebase state and ordering after remote deletion **OPEN**; Auth identity absence alone cannot prove data deletion. |
| Local PWA data erased | Contract and host repository tests | Browser/container-specific execution on Safari tab, Home Screen, Web Clip, native device; offline/revoked-device reachability and external-file limits **OPEN**. |
| Apple provider token revoked | Provider port and Engineering S007 | Real provider flow and revocation/notification evidence **OPEN**. Lack of revocation token does not justify skipping product-data deletion. |
| Completion notification | Static page promises manual confirmation | Actual inbox/queue owner, request ID, verification method, status, fulfillment clock and proof **OPEN**. |
| Public discovery / measurement | Canonical URL and about/privacy/support links in source | Real served 200/redirect, crawler accessibility and Play Console entry **OPEN**; do not record account emails, UIDs, action codes or request-body secrets in analytics. |

**Important contradiction:** The page says “email from the email address associated with your LogMate account.” This may be unavailable or confusing for users whose provider does not expose a usable sending address, including **Sign in with Apple Hide My Email** users, users without the original mailbox, and locked/uninstalled/managed-EFB contexts. It is a **conditional accessibility/recovery risk**, not proof that a particular account cannot request deletion. A support operator must offer **alternate identity verification** without asking for passwords, action-link codes, a full logbook export or automatic trust in the email `From` header. A reply/verification workflow must prevent an attacker from deleting another UID's ledger. Do not promise automatic deletion based solely on an email message.

**Another scope contradiction:** A remote deletion request can erase the service's controlled data but cannot automatically delete a user-owned exported `.lbk` file, printed record or an offline iPad that never reconnects. The static policy correctly discloses exported-copy limits. “Deleted everywhere” would be a false claim; device-local active-store wipe and other-device offline state need explicit product behavior and operator disclosure. A PWA account-deletion page being static and reachable does not guarantee it is current under an installed Worker's offline cache; test both controlled and uncontrolled navigation, with no forced storage clearing.

### 15.3 Request-to-completion operational contract [MINTTAP DECISION / DEPENDENCY]

**Web Manager decision (release admission, not product implementation):** preserve the already-authored public static page as the canonical candidate; **do not create a second deletion microsite**. Do not mark Google Play compliance or Apple App Review readiness PASS until both policy surfaces and operational fulfillment are verified. The external web path is a **request intake**, not a destructive authenticated endpoint; the in-app path is a separately tested, recent-reauthenticated product operation. The same backend deletion coordinator, when implemented, must provide consistent status semantics without trusting arbitrary client-supplied UID/email.

A defensible **minimum manual-intake operating model** needs: (1) independently monitored inbox/queue and designated operator; (2) non-enumerating receipt and opaque request ID; (3) alternate verification when the sender address is not usable, with no credential/flight-record solicitation; (4) explicit verified UID mapping before any destructive step; (5) auditable but data-minimized state changes and idempotent retries; (6) provider-revocation and remote-data inventory with per-system terminal results; (7) a disclosed reasonable completion timeframe and follow-up contact; (8) failure escalation when identity or provider/remote deletion cannot be completed; (9) deletion of request artifacts according to a documented retention policy; (10) final user notification that distinguishes **service-side deletion** from inaccessible/offline device-local data and external copies. Exact timing, retention periods, jurisdiction and operator staffing are **UNKNOWN/product/legal decisions**, not invented SLAs.

**Security ordering:** a web request may be accepted before identity verification; it must **not** directly revoke tokens, delete a Firebase UID or wipe remote ledger from an unauthenticated `mailto:`/form event. An email message's `From` field is not an authentication factor by itself. A claimed Firebase UID from the requester must not become authorization. An ambiguous timeout after deletion initiation requires re-observation of authoritative state before retry, not duplicate irreversible effects. If an in-app deletion begins while offline, a local lock/pending state is **not** a server-accepted deletion receipt; if a managed iPad is never online again, remote deletion cannot prove that its local bytes were wiped. Protect recovery of unrelated owner data from wrong-UID reauth and stale cookies.

### 15.4 Integrated falsification/acceptance matrix [VALIDATION — ALL OPEN unless separately cited]

These are **test contracts, not executed tests**; use synthetic accounts/records, non-production email destinations and approved preview/device environments. Reuse Engineering S007 and existing EFB-C tests rather than duplicating implementation suites.

| Case | Positive and negative independent oracle | Responsible owner |
| --- | --- | --- |
| DEL-W01 public link | Approved NORMAL HTTPS `/account-deletion` plus trailing slash/canonical, 200/redirect/body hash, exact app name and functional mailto/text fallback; wrong HTML/404/offline stale page rejected | E/A/C |
| DEL-W02 navigation | About/Privacy/Support → deletion path by keyboard/touch/AT; meaningful headings and visible request route at 200% zoom/landscape; no only-hover route | B/C |
| DEL-W03 Google Play declaration | Exact Play Console Data safety link opens without app/reinstall, request can be submitted and tracked; app-store name and retention disclosure match | D/E |
| DEL-W04 Apple in-app path | Signed-in Settings deletion entry initiates/continues without mandatory email/support detour for ordinary app; wrong-UID and cancellation non-destructive | B/E/Engineering |
| DEL-W05 mailbox intake | Disposable email accepted, request ID and non-enumerating acknowledgement; mailbox unreachable/undelivered/bounce classified BLOCKED not SUCCESS | E/C |
| DEL-W06 alternate identity | Apple relay/unavailable email/no-mail-client scenario can obtain safe alternate verification; spoofed `From` or wrong UID never triggers erasure | E/Engineering |
| DEL-W07 provider reauth | Recent-auth same UID, stale credential, Apple revocation and provider failure; do not claim provider revoke from fake-port test | Engineering/C |
| DEL-W08 remote erasure | Verified request maps to all UID-associated remote datasets, Sync operational metadata, provider-held data and terminal evidence; ambiguous timeout resumes idempotently | Engineering/E |
| DEL-W09 identity/local order | Remote data outcome and Auth deletion independently checked; local lock immediately hides ledger, local wipe after required stages; process kill/restart resumes | Engineering/C |
| DEL-W10 cross-context PWA | Safari tab/Home Screen/MDM Web Clip on approved test devices: offline stale owner data is not shown as “globally deleted”; same-origin does not imply one storage container | A/C/E |
| DEL-W11 incident/retention | Wrong-account, duplicate request, bounced completion email, legally retained minimal data, export outside origin and stale provider link handled without false completion | E/B |
| DEL-W12 privacy/analytics | No real UID, request email, token, `.lbk` content, action URL or support correspondence in third-party analytics/CSP reports/CI artifacts; negative injected synthetic secret detected | D/E/C |

**Evidence packet:** `{sourceSHA, NORMALDigest, HTTPSOrigin, responseStatusRedirectAndBodyHash, appVersion, platformAndBrowser, deletionRequestClass, verificationVerdict, providerStepClass, remoteEraseReceiptClass, firebaseIdentityVerdict, localContextInventoryClass, contactDeliveryClass, finalVerdict, timestamp, redactedEvidenceLocation}`. **No raw credentials, private account identifiers or actual flight data** in public evidence. An unavailable public host is `UNKNOWN` unless independently verified from an approved network. A static page plus an untested email address is `SOURCE PRESENT / OPERATION OPEN`, never `POLICY PASS`.

### 15.5 Five-track balance, transfer, next meaningful gate [TRANSFER VALIDATION / OPEN / CHANGE WATCH]

- **E — primary bottleneck:** bridge source-present public deletion information to **actually reachable request intake and verified fulfillment**, provider/remote erasure, operator ownership and data-retention disclosure. This is a higher-value Stage 8 privacy/trust blocker than another generic CSP fixture.
- **A — platform dependency:** distinguish static public route/HTTP status, Worker-controlled stale navigation, Firebase Auth session, Apple relay, origin-local data and offline managed-device reachability. No automatic cross-device deletion or shared storage is assumed.
- **C — independent challenger:** execute DEL-W01–12 at the appropriate environment tier, including spoof/wrong UID, unreachable mailbox, process death, offline PWA and all-device claim falsification; do not promote in-memory fake-port PASS.
- **B — Design Studio transfer:** semantic precedence requires “Request received”, “Identity verification needed”, “Deletion in progress”, “Service data deleted” and “Local device cleanup pending” to reflect real, independently observable states. No invented finished UI; exact-build accessible/human validation remains OPEN.
- **D — Marketing/Store transfer:** static discoverability is promising but does not prove Play Console URL acceptance, search indexing, user request completion or compliant claims. Keep PWA ads OFF pending publisher/product authority; never instrument deletion with third-party tags.
- **Software Engineering handoff:** S007 remains canonical for saga implementation and provider adapters. Web Manager supplies public-route, policy, inbox, privacy and browser/managed-EFB acceptance only. Product code and other repositories are unchanged.

**CHANGE WATCH:** Google Play Data safety deletion requirements and accepted web resource methods; Apple 5.1.1(v), Korea-specific Services ID notification rule where applicable, TN3194 revocation, Firebase recent-auth and provider flows, WebKit Home Screen storage, managed EFB policy, actual product deletion UI/backend, and served public URL behavior.

**Checkpoint:** source-level `/account-deletion` already exists; Google permits email as an **external** request method; Apple ordinarily requires a usable **in-app** initiation path and cannot be satisfied by substituting mandatory email. Real site availability, mailbox intake, manual fulfillment, deployed provider/remote erasure and managed-device local cleanup are **OPEN**. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.** **Adjacent-value check:** policy/source contradiction, existing-page reuse, alternative-identity failure mode, 12 end-to-end acceptance contracts and cross-track transfer are complete. Next work requires approved HTTPS + monitored test inbox + Engineering deletion coordinator and physical test-device access; further static copywriting or synthetic counters cannot establish these facts.


### 15.6 Adjacent exact-source Worker check — public deletion navigation is network pass-through [SOURCE / TRANSFER VALIDATION]

After §15's policy/source audit, the directly adjacent question was whether an installed LogMate Worker could turn the public deletion URL into a stale offline app shell. Read-only inspection of `tool/pwa_precache.dart` blob `90a67954af618a4e18199fa92555491c56167c17` resolves the **source-level** question: generated Worker fetch handler lines 602–610 first ignores non-GET/cross-origin requests, then returns for reserved `auth`/`__/` routes, and **returns without `respondWith` for every non-root navigation** (`request.mode === 'navigate' && rawRelative !== ''`). Thus a normal navigation to `/account-deletion` is **not intercepted by this generated Worker as the offline root shell**. This is a **positive source safeguard**, not proof of an actual installed generation, correct served HTML, absence of other network intermediaries or offline availability of the deletion page. A controlled online browser navigation should reach Hosting/network; offline navigation may fail and users need the documented external request route from another device. Keep DEL-W01 and DEL-W10 as real-browser tests. This avoids inventing a Worker interception defect and narrows the release blocker to real HTTPS delivery, intake and deletion execution. No source file changed outside Web Manager.


## §16 — Account-deletion local erasure completeness: 37-store registry versus 29-store wipe (2026-10-26 KST) [SOURCE / SYNTHESIS / CONTRADICTION / VALIDATION / OPEN]

**Meaningful Stage 8 checkpoint.** The prior §15 established that a public request page, a typed deletion coordinator and fake-port tests do not prove data erasure. This continuation resolves a previously unexamined *exact-source* question: does the local terminal wipe actually cover every durable ledger and Sync store? **Track E owns the privacy/destructive-boundary finding; A supplies browser/database mechanics; C owns independent all-store and process-reopen oracles; B and D consume state/disclosure consequences.** LogMate and specialist repositories remain read-only. The finding is source-level, **not** a claim that a real account was deleted or that a physical iPad was tested.

### 16.1 Exact pinned product-source audit and repeatable census [SOURCE / VALIDATION — STATIC]

At LogMate `main@4101ec7380796300f68fa60dbc7e5b6061f00080`, `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb`, compare the `_lbkStoreRegistry` with the explicit `StoreRef.drop(transaction)` list in `wipeLocalUserDataAndCompleteDeletion`. The audit parsed all 37 `_LbkStoreDefinition` names and resolved the 29 wipe-list variables to their declared Sembast store names. The set difference is **8 exact stores**:

| Not explicitly dropped during terminal local wipe | Role / consequence to test |
| --- | --- |
| `logmate_local_replica_v1` | Prior replica identifier may remain across deletion/new owner; test fresh-identity contract. |
| `logmate_sync_state_v1` | Existing Sync status/remote-baseline fields may remain; `ownerUid` is updated indirectly by `_writeOwnerAccess`, **not** a full state reset. |
| `logmate_sync_operation_bindings_v1` | Historical operation-to-remote binding rows remain candidates for residual personal/Sync metadata. |
| `logmate_sync_receipts_v1` | Historical acknowledgement rows remain candidates; not proof of current remote authority. |
| `logmate_sync_applied_identities_v1` | Historical applied-operation identities remain candidates. |
| `logmate_sync_applied_cursor_v1` | Historical cursor rows remain candidates. |
| `logmate_sync_record_heads_v1` | Historical record-head rows remain candidates. |
| `logmate_sync_holds_v1` | Historical recovery/hold rows remain candidates, potentially including embedded source evidence. |

**Control-flow check, not just a textual diff:** `AccountDeletionCoordinator.resume()` requires local lock → same-UID reauth → provider revoke → remote erase → Firebase identity delete → `wipeLocalUserDataAndCompleteDeletion`. The terminal wipe runs in one Sembast transaction and drops **29** named stores, then calls `_initializeFreshDatabase`, then writes `AccountDeletionPhase.completed`. `_initializeFreshDatabase → _writeReadyMigration → _publishCapabilityV7 → _publishCurrentCapability` calls `_ensureLocalReplicaIdentity` and `_ensureSyncState`; both **preserve an existing row** rather than dropping the corresponding store. `_writeOwnerAccess(unbound)` does update the existing Sync state row's `ownerUid` to null; it does not clear its other fields or the six other Sync-history stores. The terminal completion state itself stores `ownerUid` and `requestId` in `logmate_account_deletion_v1`; any necessary post-deletion audit/idempotency retention must be separately justified and bounded. No assertion that every omitted store is nonempty in every user journey is made.

**Precise finding:** the terminal method's *declared erasure coverage is incomplete relative to the product's own 37-store durable inventory*. Where omitted rows exist, the inspected path does not explicitly remove them. This is a **source-confirmed release-blocking validation gap** with a plausible privacy and future rebind risk, not a runtime-reproduced exploit or confirmed production data-loss incident. The existing `test/application/account_deletion_coordinator_test.dart@54dac071bf0cd34a93dd674cff5f5106037079d0` checks three fake-port scenarios, final phase, call order and unbound owner; it **does not** assert all-37 post-wipe raw-store emptiness, Sync sentinels, fresh replica identity or close/reopen/rebind. The existing product CI PASS cannot be promoted to this absent oracle.

**Related prior work / contradiction:** [519 §21](519_stage8_pwa_browser_runtime_csp_worker_auth_and_managed_ipad_admission_20261025.md) found **restore admission** checks only 12 of 37 stores; [519 §22] found **restore** intentionally preserves historical Sync evidence while resetting current destination authority. The new §16 concerns **terminal account deletion**, where retaining former-owner Sync evidence is a different privacy consequence. `restore must preserve provenance` is not a valid reason to assume `account deletion must preserve all Sync rows`. The correct erasure/retention rule is product/legal authority, not an inference from the restore path.

### 16.2 History → platform mechanism → limits → operational judgment [SOURCE / SYNTHESIS / CHANGE WATCH]

A local-first PWA can store meaningful user data beyond its visible flight-record collection: operational receipts, provenance, replica identifiers, pending work, authentication state and browser caches are separate persistence surfaces. A successful app-level transaction can therefore yield an empty visible logbook without establishing erasure of every relevant store. **A UI returning to Welcome, an unbound owner flag, or a completed saga phase is not a whole-store erasure oracle.**

The Sembast `StoreRef.drop(transaction)` list is an **application-database** operation, not deletion of every browser storage container, origin cache, Service Worker registration, Firebase credential, user-owned exported file or disconnected EFB. The browser's `Clear-Site-Data: "storage"` mechanism (W3C working draft / MDN) can request broad origin storage clearing in supporting browsers, including IndexedDB and Service Worker registrations, but it is **not** a drop-in repair: (a) browser/directive support and exact context vary; (b) a server response cannot reach an offline device; (c) broad clearing may erase unique unsynced ledger data or unrelated same-origin user data; (d) it does not delete independently exported `.lbk` files; and (e) Safari tab, Home Screen web app and managed Web Clip cannot be assumed to share one storage container. **Do not add global Clear-Site-Data to `/account-deletion`**, which is a public request-information page and can be visited by a user who has not verified destructive intent.

Primary sources rechecked **2026-10-26**:
- W3C Clear Site Data Working Draft (2017, non-final standard): https://www.w3.org/TR/clear-site-data/ .
- MDN `Clear-Site-Data` (directive scope and browser variation): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data .
- W3C IndexedDB: https://www.w3.org/TR/IndexedDB/ ; transaction semantics do not establish physical erasure of all browser/profile copies.
- WebKit Safari 17.2 Home Screen data-container separation (cookies may copy; other local storage does not): https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ .
- Google Play account deletion requirement: https://support.google.com/googleplay/android-developer/answer/13327111 .
- Apple 5.1.1(v) account deletion: https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion .

**Operational decision, PROPOSED:** Engineering should make the product-owned complete durable-store inventory the terminal wipe acceptance authority, including any later schema stores; preserve only a specifically justified minimal deletion receipt, if any. A single transaction across relevant Sembast stores may provide local atomicity; it does **not** provide remote-provider atomicity, browser-profile-wide erasure, secure physical media sanitization or disconnected-device deletion. Neither a generic `indexedDB.deleteDatabase()` nor `Clear-Site-Data` should be prescribed before verifying preservation of non-deleted users' data, pending offline work and browser/OS support. The approved owner must determine how to handle external backups, legal retention and re-enrollment after deletion.

### 16.3 Product-owned discriminating acceptance packet [VALIDATION / DEPENDENCY — NOT EXECUTED]

Reuse the existing DEL-W07–12 and Engineering S007 saga tests. Add these **specific oracles** rather than another generic Auth primer:

| ID | Exact positive/negative observation needed | Failure if |
| --- | --- | --- |
| DEL-L01 | Before deletion seed all 37 stores with valid distinguishable synthetic records where supported; inventory raw keys/counts and opaque hashes. | Test only checks UI records/owner flag. |
| DEL-L02 | Seed nonempty Sync binding/receipt/applied identity/cursor/head/hold rows with synthetically distinct old-owner references; execute same-UID deletion with fake remote/provider ports. | Any unjustified old-owner Sync row survives terminal completion. |
| DEL-L03 | Compare all 37 raw store snapshots **after** terminal transaction; assert the approved empty/default/retained schema for every store, including replica and Sync state. | Store omitted, unexplained retained key or implicit default accepted as erased. |
| DEL-L04 | Verify `completed` receipt contains only approved minimal metadata with an explicit retention/expiry rule; wrong-UID requests cannot retrieve another user's receipt. | Full UID/request ID retained without documented purpose/controls. |
| DEL-L05 | Close database, reopen through `SembastLogbookRepository.open`, validate canonical state, then bind a **different** synthetic UID and verify no previous Sync authority/provenance leaks or replays. | Reopen fails, old replica identity/Sync status incorrectly persists, or prior receipts are treated as new-owner ACK. |
| DEL-L06 | Inject transaction failure after partial store drops, confirm rollback to the locked pre-wipe state; restart/resume without skipping provider/remote outcome checks. | Partial wipe presented as completed or unique local data silently destroyed. |
| DEL-L07 | Exercise remote erasure timeout/unknown result and provider-revoke failure; keep local lock and verify idempotent re-observation before irreversible retry. | Client phase advances from ambiguous response or deletion claim based on Firebase sign-out. |
| DEL-L08 | Two-tab/process overlap: stale tab/worker attempts write, export, read and rebind during and after deletion; distinguish DB transaction atomicity from cross-tab authority fencing. | Old context recreates stale owner data or emits remote effects. |
| DEL-L09 | Approved HTTPS Chromium, native Safari, Home Screen and managed Web Clip: independently inventory origin IndexedDB, CacheStorage, Worker, Auth/session and local user data before/after **authorized** deletion. | One context's wipe is promoted to other context's PASS. |
| DEL-L10 | Offline device remains disconnected after remote deletion: rejoin under revoked UID, fence remote writes, classify local data honestly, avoid false “deleted everywhere.” | Old offline data automatically regains remote authority or user-facing claim overstates reach. |
| DEL-L11 | Deliberately exercise `Clear-Site-Data` only in isolated synthetic origins; check browser support and negative control that public `/account-deletion` GET never triggers destructive origin clearing. | Visiting public information deletes active data or browser support is assumed. |
| DEL-L12 | Separate independent external `.lbk` file, OS backups and operator/third-party copies from app-controlled stores; verify accurate disclosure and lawful retention decisions. | App-local wipe is represented as deletion of inaccessible copies. |

**Execution tier:** the above is an exact-source **static audit + proposed falsification contract**. No Dart/Sembast runtime, HTTPS product artifact, real provider erasure, Safari, managed-iPad or external-backup execution was performed here. Expected release verdict remains **Stage 8 applied ACTIVE / Production validation OPEN / PWA release HOLD**. This is a higher-information-gain blocker than another synthetic browser header test.

### 16.4 Five-track transfer and adjacent-question decision [TRANSFER VALIDATION / CONTRADICTION / OPEN]

- **E (owner; highest risk):** terminal erasure inventory completeness, minimal deletion receipt, provider/remote erasure custody and privacy claims. Hand off the exact 8-store set to Software Engineering S007/LogMate for implementation-level tests; do not modify their repositories.
- **A (dependency supplier):** Sembast store semantics, IndexedDB storage container and Worker/cache scope; explicitly distinguish browser storage clearing from application-record deletion and managed-OS storage.
- **C (independent quality):** all-37 pre/post raw-store oracles, fault injection, close/reopen, cross-tab and real browser/device tiers; fake-port PASS does not substitute for these.
- **B (Design Studio CD127/W121 transfer):** `Deletion requested`, `Locally locked`, `Remote deletion pending`, `Account deleted` and `Other devices/copies not verified` must map to authoritative outcomes, accessible states and actual implemented actions; no unsupported promise of global deletion.
- **D (Marketing D9 / web discovery):** external Google Play deletion URL, real intake and completion remain OPEN; no UID/email/token/Sync metadata in public analytics or logs; account-deletion compliance/promotion remains HOLD.

**Adjacent-value check:** this audit followed the prior §15 request/fulfillment study into its highest-value destructive local boundary, independently reconciled the earlier 519 restore-vs-delete contradiction, inspected initialization/rebind and tested the existing test-suite's coverage by direct source read. The next material step is **Engineering-owned execution of DEL-L01–L06 with nonempty Sync sentinels**, then authorized NORMAL HTTPS and actual Safari/managed-EFB multi-container behavior. More source-only wording without a runtime oracle would not close the gate.

## §17 — Deletion saga transition authority, terminal-state reuse and identity-first recovery (2026-10-26 KST) [SOURCE / SYNTHESIS / CONTRADICTION / VALIDATION / OPEN]

**Stage 8 applied continuation, not a new study file.** §16 identified eight durable stores omitted by the terminal wipe. The next adjacent high-value question is whether *phase advancement and post-deletion reuse* preserve the same trust boundary. **Track E owns** the destructive-operation authorization and recovery contract; A supplies database/browser-container semantics; C owns independent adversarial validation; B/D consume state-truth and Store-claim consequences. Exact product authority is LogMate `MASTER.md`; the following code observations are pinned to **`yhappcom/logmate main@4101ec7380796300f68fa60dbc7e5b6061f00080`**, **not** a production deployment claim.

### 17.1 Source chain, history and independent static adjudication [SOURCE / VALIDATION — STATIC ONLY]

Read-only source blobs: `lib/application/account_deletion_coordinator.dart@8e844e888b39d3b5e1648aeb84be26e6582ed60f`; `lib/domain/account_deletion_state.dart@499037bd3a50058757f8155d2287e7f301f2eafc`; `lib/repository/logbook/sembast_logbook_repository.dart@d7e4efd4f6dc85220a2f67ca8af956e8abf01aeb`; `test/application/account_deletion_coordinator_test.dart@54dac071bf0cd34a93dd674cff5f5106037079d0`. Reconciled current product `MASTER.md` §0/§13 and `AGENTS.md`; Design Studio synthesis/W121, Marketing D9 and Engineering S007 are **transfer dependencies**, not alternate product authority.

**History/problem → principle:** resumable deletion spans multiple independent systems. A local phase is a durable *record of the coordinator's prior result*, not itself cryptographic evidence that a provider revoked credentials, a remote ledger was erased or Firebase deleted an identity. A single-store transaction cannot make external provider calls atomic. The normal coordinator sequences same-UID reauthentication → provider revoke → remote erasure → Firebase identity deletion → local wipe and advances each phase after its awaited port succeeds. That is a **positive implementation pattern**, but its lower-level repository phase setter has a broader accepted transition graph.

A fresh, read-only V8 source-text analysis of these exact blobs resolved **37/37** store variable names, counted **37 registry entries**, **29** terminal `drop` references, **0 unresolved references**, and exactly the **eight** omitted stores recorded in §16. It independently checked the enum order, repository guard, coordinator ordering, new-owner bind and terminal receipt predicates. A separate abstract evaluation of the **actual source predicate** generated the transition table below. This is a **source-derived static predicate execution**, **not Dart compilation, a Sembast transaction, an external-provider call or a browser/device test**. No product code changed.

### 17.2 Counterexample A: monotonic phase is not verified completion [CONTRADICTION / FAILURE MODE]

`advanceAccountDeletion(ownerUid, requestId, phase)` checks the current stored owner/request and rejects `none`, `completed`, and **backward** transitions (`phase.index < current.phase.index`). It does **not** require the immediately authorized next phase or a result/receipt from the external step. Therefore the repository's public Dart method can **accept a direct request** to record `firebaseIdentityDeleted` from `localLocked` when the same owner/request is supplied. `wipeLocalUserDataAndCompleteDeletion` then checks the stored phase `firebaseIdentityDeleted`, not a provider-issued deletion receipt. **This is a source-level internal API contract gap, not evidence of a remote exploit or that the normal coordinator takes the shortcut.** The normal coordinator calls the phases in order; direct production caller reachability outside it has not been established.

| Recorded phase before `advance` | Accepted requested phases by the source guard (same owner/request) | Security/recovery significance |
| --- | --- | --- |
| `localLocked` | `localLocked`, `reauthenticated`, `providerRevoked`, `remoteDataErased`, `firebaseIdentityDeleted`, `retryableIncomplete` | Four forward skips beyond the immediate step are not excluded; direct terminal precondition can be manufactured inside the app. |
| `reauthenticated` | same, `providerRevoked`, `remoteDataErased`, `firebaseIdentityDeleted`, `retryableIncomplete` | Prior provider/remote/identity outcomes are not independently proven by the repository. |
| `providerRevoked` | same, `remoteDataErased`, `firebaseIdentityDeleted`, `retryableIncomplete` | A direct identity-complete phase can skip remote erasure. |
| `remoteDataErased` | same, `firebaseIdentityDeleted`, `retryableIncomplete` | Identity step still requires a real outcome from its owner. |
| `firebaseIdentityDeleted` | same, `retryableIncomplete` | Moving to `retryableIncomplete` can remove the coordinator's recognized local-wipe branch. |
| `retryableIncomplete` | `retryableIncomplete` only | `resume()` has no branch for this phase; a direct setter call can leave a locked state without automatic progression. |
| `completed` | none | Terminal record is immutable by this setter. |

**Proposed Engineering correction, NOT an approved product patch:** define an explicit legal transition relation, make external-result authority available only through the trusted coordinator/port boundary, and reject arbitrary jumps even if a caller knows UID/request ID. Merely changing `index <` to `index != current + 1` is *not sufficient authorization*: a caller could still fake each adjacent step. Idempotent retries, timeouts, restart and independently checked provider/remote receipts must be designed together. The `requested` and `retryableIncomplete` enum values require an explicit supported recovery interpretation or a documented unreachable-state invariant; do not silently discard historical states.

### 17.3 Counterexample B: completed receipt survives new-owner binding [SOURCE / CONTRADICTION]

The terminal wipe **drops** `logmate_account_deletion_v1`, reinitializes the database, then **writes `completed` with the former `ownerUid` and `requestId`**. `AccountDeletionState.locksNormalAccess` is **false** for `completed`. The public `createOwnedLedger(newUid)` and `bindOwner(newUid)` methods require an unbound owner but **do not inspect or reset** the terminal deletion record. In contrast, `requestAccountDeletion(newUid, newRequest)` rejects every non-`none` record except an *identical* old UID/request pair. Thus the direct repository-API sequence

`delete owner A → completed(A, requestA) → createOwnedLedger(ownerB) → requestAccountDeletion(ownerB, requestB)`

has a **source-level contradictory postcondition**: new owner B may be bound while their deletion request is rejected as “a different account deletion request is already active.” This is **not a demonstrated ordinary UI flow**; startup routing, fresh-profile policy and actual Dart/Sembast reachability require execution. A product decision is also required on whether same-profile reuse is supported or deliberately prohibited. If prohibited, the owner-entry API and user-visible recovery must reject reuse consistently *before* creating a new owner state. If supported, the old completion receipt must not block the new owner's deletion or expose old UID/request metadata. Retention of any minimal receipt must have an explicit purpose, scope, access control and expiry rather than assuming permanent client storage is necessary.

**Additional privacy connection:** `_writeOwnerAccess` updates only `sync_state.ownerUid`; the seven prior Sync history stores are not explicitly dropped (§16). Consequently the owner-B binding counterexample must be combined with the eight-store sentinel and old-owner provenance checks, rather than tested as a pure UI error. No old-owner data disclosure is claimed without runtime evidence.

### 17.4 Counterexample C: remote identity gone, local completion interrupted [SYNTHESIS / DEPENDENCY / OPEN]

The approved `MASTER.md` ordering deliberately places Firebase identity deletion **before** device-local wipe. The coordinator persists `firebaseIdentityDeleted` only after the identity port returns. If the process dies (i) after remote Firebase deletion but before the local phase commit, (ii) after phase commit but before the wipe, or (iii) during a local storage/quota failure, recovery requirements differ. In (i), a subsequent identity-delete call may see “already deleted” and must adjudicate that result without reviving authority or claiming remote success from an exception. In (ii), `resume()` can reach the local-wipe branch *if it is invoked*, but normal authenticated startup might no longer exist. In (iii), the old ledger may remain locally locked while the remote account no longer exists. These are **plausible failure windows, not reproduced product outcomes**. A real service receipt, independent remote state re-observation, offline safe-local cleanup and process-restart entry must be proven; avoid solving this by deleting unique local data before the authorized remote step.

Firebase's current client documentation requires recent sign-in for sensitive deletion; the Firebase Admin API can delete an identity by UID using server authority, but neither proves product-data erasure or client-local cleanup. Primary sources rechecked **2026-10-26**: [Firebase client manage users](https://firebase.google.com/docs/auth/web/manage-users), [Firebase Admin manage users](https://firebase.google.com/docs/auth/admin/manage-users), [Apple App Review 5.1.1(v)](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion), [W3C IndexedDB](https://www.w3.org/TR/IndexedDB/), [MDN IndexedDB transaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction). An IndexedDB transaction `complete` is not a proof of erasure from every profile/device or physical-media sanitization. A browser/server `Clear-Site-Data` header is **not** a substitute for owner-scoped local erasure or an offline-device protocol (§16).

### 17.5 Falsifiable Engineering-owned acceptance extension [VALIDATION — NOT EXECUTED]

Extend **existing** DEL-L01–L12 and DEL-W07–12; do not build a duplicate account-deletion subsystem or pretend a research-model PASS is a product PASS:

1. **DEL-L13 — phase-jump negative:** on a seeded same-UID `localLocked` state, call the public repository method with `firebaseIdentityDeleted` and with `remoteDataErased` without executing provider/remote ports. **Expected desired gate: REJECT, all 37 stores unchanged, no completed state.** Current source guard appears to permit these transitions; **runtime verdict OPEN / likely expected RED**, not an executed failure.
2. **DEL-L14 — terminal-phase dead end:** attempt direct `retryableIncomplete` from `localLocked` and from `firebaseIdentityDeleted`; restart and invoke `resume()`. Require a documented recoverable state, not a silent locked forever or an unverified success.
3. **DEL-L15 — post-completion new UID:** seed eight omitted-store sentinels; complete owner A with fake ports; close/reopen; attempt owner B creation and B deletion. Verify old UID/request receipt isolation, new-owner authority and an explicit supported/rejected reuse policy. The source predicts B request rejection if binding is allowed.
4. **DEL-L16 — identity/local interruption matrix:** fail/crash at identity delete before phase persist, phase persist before wipe, and during wipe; restart with Auth deleted, offline and wrong UID. Assert no unverified remote deletion claim, no unguarded ledger visibility, no lost retry route and no stale remote Sync admission.
5. **DEL-L17 — completed receipt minimization:** enumerate all raw keys/values of `logmate_account_deletion_v1` and seven Sync stores before/after; test allowed retention/expiry and no old-UID exposure to B, logs, support analytics or export. Do not prescribe a receipt lifetime without product/legal approval.
6. **DEL-L18 — two-client/revocation race:** old controlled PWA tab/Service Worker and new owner session share origin; try writes, exports, rebind, cache reads and delayed remote effects across deletion and restart. Distinguish application authorization from storage persistence, cross-tab locks and server-side revocation; repeat in real Safari/Home Screen/managed Web Clip only when permitted.

**Required evidence fields:** `{exactLogMateSHA, DartFlutterSembastVersions, sourceAndRuntimeEnvironment, seeded37StoreDigestClasses, phaseBeforeAfter, invokedPortTrace, providerRemoteReceiptClass, ownerUidClass, requestIdClass, localStoreCensus, processRestartClass, newOwnerOutcome, browserStorageContainer, negativeControlVerdict, redactedEvidenceLocation}`. Synthetic UID/flight records only; no real action tokens or personal ledger in public CI. Explicit `PASS/FAIL/BLOCKED/NOT_EXECUTED` per environment. Static source truth and abstract guard evaluation cannot be promoted to Dart, browser, server, Safari or managed-iPad PASS.

### 17.6 Five-track transfer, release decision and adjacent-value check [MINTTAP DECISION / TRANSFER VALIDATION / CHANGE WATCH]

- **E (dominant bottleneck):** owns phase authority, multi-system failure recovery, old-owner receipt retention, all-store deletion and exact HTTPS/managed-EFB release gate. The product contract mandates a resumable saga; *recorded phase* cannot self-attest external erasure. Keep PWA release **HOLD**.
- **A (foundational dependency):** the Sembast transaction boundary and browser storage context are separate from provider authority. Native app, Safari tab, installed Home Screen app and MDM Web Clip may have different storage/launch paths; no implicit cross-device erasure.
- **C (independent challenger):** execute actual Dart negative phase transitions, interrupted deletion, process reopen and new-UID path before spending effort on more generic synthetic Worker fixtures. Record expected RED separately from observed FAIL and demand an independently checked all-37-store postcondition.
- **B (Design Studio synthesis/CD127/W121):** user-visible `Locally locked`, `Remote deletion verified`, `Local cleanup pending`, `Deletion completed on this device` and `Other offline devices not verified` must map to actual state, preserve keyboard/AT recovery, and never turn a stranded account into a misleading success screen.
- **D (Marketing D9 / Store-truth transfer):** no account-deletion-complete, global-erasure, managed-PWA recovery or Sync claim from source-only tests. Public web request, mailbox operations and Play/Apple in-app paths remain separate OPEN gates. Do not log UID/request IDs or deletion receipts to third-party measurement.
- **Engineering handoff:** S007 owns implementation and provider/remote adapters; D005/D006 own crash/transaction/Sync mechanics. Web Manager supplies these *specific* failure contracts, not a new generic software architecture or edits to LogMate. Marketing D9 has independently confirmed the 29/37 gap; this section adds phase authority and same-profile reuse contradictions without rewriting Marketing's Store research.

**MINTTAP DECISION (proposed admission):** prioritize Engineering **DEL-L13 + DEL-L15 + existing DEL-L02/03** in one actual Sembast test bundle; add interruption and two-client cases next. Do **not** treat strict adjacent-phase checks alone as external verification, nor require deletion of unrelated offline owners' unique data. Product owner must resolve same-profile reuse and minimal terminal receipt policy. Exact approved NORMAL artifact, retained hash, HTTPS/real Auth and physical managed-iPad remain mandatory separate tiers.

**OPEN:** real Dart reproduction and caller reachability, new-owner entry product policy, retained-receipt purpose/expiry, actual provider/remote deletion receipts, interrupted-after-identity-deletion recovery, all-37 seeded store outcomes, browser/MDM contexts, NORMAL custody/HTTPS. **CHANGE WATCH:** Firebase identity deletion semantics/recent sign-in, Apple/Google Store deletion guidance, Sembast/IndexedDB transaction durability, WebKit storage isolation and LogMate schema/phase evolution. **Gate: Stage 8 applied ACTIVE · SOURCE-CONFIRMED INTERNAL CONTRACT CONTRADICTIONS / RUNTIME NOT_EXECUTED · Production validation OPEN · PWA release HOLD.**

**Adjacent-value check:** this bundle went beyond §16's store census into the actual enum/guard, trusted coordinator, post-terminal owner reuse, deletion interruption and cross-track consequences; further speculation about production exploitability would be unsound without real product runtime/port/MDM evidence. Next meaningful boundary is an Engineering-owned exact-source Dart/Sembast negative run, not another research-only synthetic PASS.
