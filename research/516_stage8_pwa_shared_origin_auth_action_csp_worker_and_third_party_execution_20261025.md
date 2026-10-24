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
