# 517 — Stage 8 PWA Served-Header Evidence Admission: Auth Aliases, Worker Policy and False-Green Controls

Date: **2026-10-25 (Asia/Seoul)**  
State: **SOURCE + PRIMARY STANDARD REVIEW + SYNTHETIC EVIDENCE GATE 26/26 EXPECTED; NO HOSTED/CHROME/SAFARI/PRODUCT PASS**  
Canonical start: Web Manager `main@7d12f92c46d39cfd247227c0f2e956463107381e`. LogMate inspected read-only at `main@4101ec7380796300f68fa60dbc7e5b6061f00080`; Hosting blob `9ac0972e26749215c4a718360c66315c6caf3cc8`.  
Owner: **Track E**, with A browser semantics, C independent evidence admission, B recovery UX and D privacy/claims. Reuses 516; does not create another CSP primer.

## 1. What changed from 516 [SOURCE / SYNTHESIS]

516 established the shared-origin execution risk and identified that the current checked-in `firebase.json` has only a catch-all Cache-Control rule; it does **not** establish absent headers on a live host. It also verified the generated Worker bypass for `auth/` and `__/`, not origin isolation.

This continuation answers the adjacent operational question: **what exactly would count as defensible evidence that all auth aliases, root and Worker receive the intended response policy, without mistaking a green log or a report-only policy for enforcement?** A new fail-closed, non-network [served-header evidence gate](handoffs/pwa_served_header_evidence_gate.js) accepts two independently supplied JSON documents: an approved expectation and a captured-response envelope. It compares provenance identifiers, an exact enumerated route set, HTTPS response identity, body SHA-256, status, no-redirect contract, Content-Type, policy mode and exact expected header arrays.

**Result:** 26 deterministic cases exercised in V8; **26/26 expected classifications**, including the positive synthetic fixture. The output success token is intentionally `SERVED_HEADER_CONSISTENT_UNVERIFIED`, **not** `CSP_ENFORCED`, `HOST_PASS` or `RELEASE_GO`. No actual HTTPS requests were made, and the capture envelope is not cryptographically authenticated.

## 2. History/problem → standard → operational implication [SOURCE]

- **History/problem:** HTTP response headers are evaluated by the browser on the response actually received, not on a developer's intended deployment file. Hosting rewrites, aliases, CDN/intermediary layers and installed Service Workers can make source-level configuration diverge from runtime behavior. A CI command returning 0 can also conceal a failed semantic oracle if exit status is lost through a pipeline (Engineering Q006).
- **Firebase Hosting:** custom headers match the **initial request URL before rewrite**. Therefore `/auth`, `/auth/`, `/auth/action` and `/auth/action/index.html` must be probed independently even when they render the same underlying HTML. Provider-reserved `/__/...` responses are a distinct inventory item; do not assume project headers or normal Hosting rules govern them.
- **CSP Level 3:** `Content-Security-Policy-Report-Only` observes violations; it does not enforce the proposed policy. Multiple enforced policies combine restrictively, so a single permissive-looking policy cannot cancel a stricter second policy. `worker-src` fallback order is `worker-src → child-src → script-src → default-src`; `script-src-elem` is not the fallback. `frame-ancestors` has no `default-src` fallback and cannot be delivered through a meta CSP. Worker global policies ordinarily come from the **Worker script response**, not merely its parent document's header.
- **HTTP/identity:** a status 200 with `text/html` at a JavaScript Worker path is not valid JavaScript evidence. Header names are case-insensitive, but duplicate header fields can be significant, particularly multiple CSP policies; a collector must preserve raw field instances instead of flattening them into a single last-value map.
- **Privacy:** `oobCode` in action-link query strings is sensitive. Do not store raw action links, query tokens, authorization headers, cookies or pilot records in test captures, reports or GitHub artifacts. The gate requires query-free exact route URLs and emits only fixed error codes.

Primary sources reviewed 2026-10-25:
- W3C CSP Level 3: https://www.w3.org/TR/CSP/
- Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config
- MDN CSP policy, multiple headers and Worker response distinction: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
- MDN CSP guide/report-only: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- MDN Referrer-Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy

## 3. Route-by-route proposed acceptance contract [MINTTAP DECISION / PROPOSED, NOT DEPLOYED]

| Route cohort | Independently observed evidence | Required independent browser exercise |
| --- | --- | --- |
| `/`, `/index.html`, Flutter boot scripts | exact NORMAL artifact/body, final MIME, configured CSP/Referrer-Policy, `nosniff` candidate; all allowed module/connection origins inventoried | Flutter boot, runtime imports, auth, offline first-load/reload, forced disallowed inline/external script |
| `/auth`, `/auth/`, `/auth/action`, `/auth/action/index.html` | each **initial URL** and its final representation, redirect chain, effective response headers and body; explicit report-only vs enforcement | verification/reset, invalid/expired code, network error, referrer observation using fake code, keyboard/focus/AT |
| `/logmate_service_worker.js` | independent Worker script response CSP, JS MIME, SHA, scope and cache behavior | registration, claim, reserved-route bypass, two Worker generations, offline reopen, data-preserving recovery |
| `/__/...` | provider-reserved path classification and actual response without asserting project-controlled header coverage | auth helper/redirect compatibility and Worker non-interception |
| Future third-party tag/ad | **not currently approved**; no implicit policy allowance | security/privacy/Marketing/Engineering approval before any production tag execution |

**Policy profiles are not interchangeable.** A source baseline may record `observe` (no enforced CSP) truthfully. A proposed preview may demand `report`, then a later **separate** preview may demand `enforce`. The gate compares whichever **approved external expectation** is supplied. It must never generate an expectation from the same response it is judging, nor label report-only as blocked execution. Do not copy a speculative `script-src` into production without the exact Flutter/Firebase module graph and negative runtime tests.

## 4. Executable gate design and adversarial falsification [VALIDATION]

File: `research/handoffs/pwa_served_header_evidence_gate.js`.

CLI when Node is available: `node pwa_served_header_evidence_gate.js --self-test` or `node pwa_served_header_evidence_gate.js approved-expectation.json sanitized-capture.json`. Exit 0 only for **syntactic/semantic evidence consistency**; exit 2 for mismatches. CI must preserve exit status across `tee` and workflow output boundaries (Engineering Q006). No network request, no secret, no real action link, no browser execution and no GitHub API credential is required for the synthetic suite.

**26 cases, 26 expected:** positive fixture; wrong source SHA; wrong artifact SHA; wrong origin; missing alias; extra route; duplicate route; non-HTTPS transport; POST instead of GET; 302; redirect; URL query; foreign origin; wrong body SHA; zero bytes; boolean bytes; HTML masquerading as Worker JS; missing enforced CSP; missing report-only CSP; wrong Referrer-Policy; missing `nosniff`; duplicate required singleton; CRLF in header; null headers; schema mismatch; wrong route URL. The fixture includes root, four auth aliases and Worker.

**Admitted evidence class:** `SERVED_HEADER_CONSISTENT_UNVERIFIED` means the **two supplied JSON objects agree under this narrow schema**. It does **not** mean:
- the collector made real HTTPS requests or the responses came from an approved server;
- the expectation was independently approved, signed or pinned to an actual NORMAL archive;
- the body hash was independently calculated rather than copied into the capture;
- CSP was parsed or enforced correctly by Chromium/WebKit;
- a blocked-script negative control actually failed in a browser;
- Firebase Auth, PWA offline, 37-store data, iPad/MDM or production passed.

The gate intentionally does **not** implement Firebase glob matching, CSP directive parsing, redirects or a browser. These remain source/provider/runtime responsibilities. It rejects any observed redirects by default: an approved redirecting alias would require a reviewed schema and separate trust chain, not silently relaxed evidence. The fixture's example policy strings and `preview.example.test` origin are **synthetic**, not recommended deployment headers.

## 5. Five-track pressure comparison and transfer [DEPENDENCY / TRANSFER VALIDATION]

| Track | Stage/gate and relative depth | Work allocation |
| --- | --- | --- |
| **E — Security/Operations** | Stage 8 applied; shared-origin code authority, approval/served-header distinction and incident rollback are highest risk. | **Primary**: route trust matrix, release/incident boundaries, external approval evidence. |
| **A — Platform/Browser** | CSP fallback/Worker lifecycle foundations established; actual Chromium/WebKit behavior and EFB policy remain OPEN. | Supplies standards semantics and browser route/control cases. |
| **C — Quality/Accessibility** | 509–514 synthetic oracles exist; no real NORMAL/host/managed-device PASS. | Co-owner of independent capture, false-green controls, negative runtime tests and CI verdict propagation. |
| **B — UX/IA/Content** | Design Studio Web W121/CD127 says static evidence saturated; exact visible/a11y state still OPEN. | Defines honest auth-expiry/offline/recovery state and prevents false “verified” messages. |
| **D — Discovery/Analytics** | Marketing D8/D10 and 437/438 show PWA release/ads claims HOLD. | No action-link query telemetry, web ads or “secure/offline-ready” claims without runtime evidence. |

Read-only specialist transfer: Design Studio `progress/WEB_STATUS.md` and `research/content/127-pre-runtime-saturation-and-semantic-evidence-stop-rule.md`; Engineering Q006 pipeline verdict and M006 bounded macOS Safari transfer; Marketing Manager current D8/D10. Do not rewrite these domains' canonical findings.

## 6. Release/incident state machine and next execution [SYNTHESIS / OPEN]

`SOURCE_CONFIG_OBSERVED` → `EXPECTED_POLICY_APPROVED` → `HTTPS_CAPTURE_AUTHENTICATED` → `SERVED_HEADERS_CONSISTENT_UNVERIFIED` → `BROWSER_NEGATIVE_ENFORCEMENT_PASS` → `AUTH_AND_OFFLINE_RUNTIME_PASS` → `MANAGED_IPAD_POLICY_PASS` → independently approved release decision.

The stages are **not** automatically promoted. An offline Worker can serve an old document even after the server header changes; a rollback can restore executable authority unexpectedly; a policy incident must not trigger origin-wide storage deletion or invalidate the only local flight ledger. Preserve 515 external-backup custody, 506 R03/R04 semantic restoration and 513–514 two-generation Worker proof as separate gates.

**Engineering execution packet:** use approved disposable HTTPS preview and exact NORMAL archive, independently freeze expectation/body hashes and source/run/attempt identity, collect sanitized raw response headers for each alias and Worker, run the gate with fail-closed exit propagation, then run real Chromium/Safari positive and deliberately blocked script probes, Auth flows, offline/reopen and managed-iPad policy matrix. Record OS/browser/MDM envelope and screenshots/a11y states without credentials. `/__/...` must be separately classified as provider-reserved; do not mark it passing from app-owned fixture. On failure, block release and retain diagnostic hashes and sanitized failure codes.

**CHANGE WATCH:** Firebase Hosting initial-URL header matching, CSP Level 3 implementations/Trusted Types, Firebase SDK module graph, Flutter generated Worker, Apple WebKit/Home Screen/MDM and GitHub Actions CI verdict behavior. Recheck at actual deployment date.

**Adjacent-value check:** after 516, this run completed the executable source-to-served admission model, 26 adversarial false-green controls, standards contradiction analysis and A–E handoff. The next decisive proof is a **materially different environment boundary**: approved HTTPS and real browser/device execution. No LogMate, Design, Engineering or Marketing repository was modified.

**Gate:** **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**