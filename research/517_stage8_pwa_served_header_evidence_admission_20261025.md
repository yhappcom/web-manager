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

## 7. Enforced-policy presence false-green and independently pinned CSP expectation (2026-10-25) [SOURCE / CONTRADICTION / VALIDATION]

### Falsified assurance and causal mechanism

An audit of the exact pre-change 517 gate (blob c5d52d52571f8c68588109139c060da98beeff0b) found that `policy: enforce` only checked whether an array named `Content-Security-Policy` had at least one member. It did not require an independently expected CSP value, nonempty policy text or a recognized directive capable of constraining behavior. Executing that exact committed gate in V8 returned `SERVED_HEADER_CONSISTENT_UNVERIFIED` for each of: an empty enforced header, whitespace-only text, and `report-uri /csp-report` with no enforcement directive. These are **confirmed evidence-oracle false greens**, not a demonstrated LogMate deployment failure.

History/problem → principle → standard: CSP is a directive-list policy delivered by HTTP; merely receiving a header field is not equivalent to a browser enforcing an effective restriction. `report-uri` routes reports and does not independently restrict script execution. W3C CSP Level 3 separates policy parsing, enforced policies and report-only delivery. MDN documents directive semantics and distinct reporting behavior. Current primary references checked 2026-10-25:
- W3C CSP Level 3 Working Draft (2026-09-16): https://www.w3.org/TR/CSP3/
- MDN CSP guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config

### Corrected admission contract [MINTTAP DECISION — research-tool boundary only]

1. For each route with `policy: enforce`, an independently approved plan must explicitly pin a `content-security-policy` array. For `policy: report`, it must pin `content-security-policy-report-only`; these classes are not interchangeable. `observe` retains the existing observation-only semantics.
2. A pinned array must be nonempty; every value must contain non-whitespace text; at least one must name a recognized security-relevant CSP directive (e.g., `default-src`, `script-src`, `worker-src`, `object-src`, `base-uri`, `frame-ancestors`, `connect-src`, `form-action`, `sandbox`, `upgrade-insecure-requests` or `require-trusted-types-for`). A report-only transport directive by itself does not satisfy this minimal policy-shape gate.
3. The existing 517 gate still compares all pinned header instances exactly against received evidence. Empty, unpinned, whitespace, report-uri-only and unknown-directive cases now return `REJECT` with `POLICY_UNPINNED_OR_EMPTY`. This is a **necessary admission guard**, not a CSP parser, browser interpretation proof, a recommendation of a universal policy string, or a guarantee that an independently pinned policy is secure.
4. The 518 HTTPS collector now reuses the **same 517-owned `hasPinnedPolicy` function** during plan preflight and refuses invalid plans with `ROUTE_POLICY_PLAN` **before starting any network request**. This avoids duplicating policy semantics between collector and verifier and prevents wasted/unauthorized probing on structurally invalid plans.
5. The 517 self-test fixture now explicitly pins enforced and report-only policy values on all relevant routes. The 518 collector test fixture is aligned; three new Node top-level negative controls check that missing enforce/report expectations and empty/report-uri-only values do not reach the transport.

### Reproduction and verification [VALIDATION — bounded]

| Evidence tier | Exact outcome | Not proven |
| --- | --- | --- |
| Before fix, exact 517 committed blob | 3/3 false-green values (`''`, whitespace, report-uri-only) admitted | Browser CSP behavior |
| After fix, exact 517 committed blob | 33/33 deterministic V8 self-test outcomes; 7 new policy-oracle negative controls | Hosted Node execution |
| After fix, exact 518 collector blob | 4/4 isolated V8 preflight cases (1 approved, 3 rejected) using mocked Node modules | Real Node HTTPS transport |
| After fix, committed JS files | 3/3 V8 syntax compilation | Full 40-case Node test suite |
| CI | Workflow watches the changed files; expected 40 collector top-level tests and 33 gate self-tests | Run ID, exact hosted conclusion and logs OPEN |

New code identities at this checkpoint: gate blob `9685a7b7daecab5f3be2e7c6361825112cd0e007`; collector blob `c0b485301bfbd8b60bc43d54a617310415f3a10d`; Node test blob `036090c8836101aa6d997fb56a4cfa557911a4a8`. The V8 collector preflight check used a mock URL/net/Node module shim, so it is **not** an exact Node transport or CLI run. Do not claim hosted 40/40 or real HTTPS PASS.

### Five-track dependency, residual failure modes and operational judgment [DEPENDENCY / TRANSFER VALIDATION]

| Track | Gate pressure and bounded contribution |
| --- | --- |
| E — primary | Stage 8 release-trust bottleneck: owns independently approved policy expectation, CSP evidence-admission and no-false-green gate. |
| A — dependency | Owns W3C/browser enforced vs report-only and Worker-global policy semantics. Actual Chromium/WebKit execution still OPEN. |
| C — challenger | Owns 33 deterministic gate controls, 40 expected Node collector controls, CI failure propagation and negative browser probes; no hosted verdict claimed. |
| B — transfer | Design Studio W120/CD127 requires actual visible↔accessible↔action truth for Auth/offline/recovery; do not translate gate PASS into UI reassurance. |
| D — transfer | Marketing D8/D10 retains PWA/ads claim HOLD; telemetry must not collect Auth action-code URLs or represent policy consistency as security certification. |

Residual contradictions: an explicitly pinned but permissive CSP can still pass text equality; a recognized directive name does not guarantee meaningful browser enforcement; multiple policies, fallback directives, inline module behavior, Worker script policy and Safari differences require browser tests. An independently supplied plan can be self-approved unless Engineering/release authority pins it outside the collector's writable domain. DNS/TLS capture custody, NORMAL artifact→served body identity, browser policy enforcement, 37-store external restore and managed-iPad/MDM remain distinct OPEN gates. No policy change is prescribed to LogMate `firebase.json` without exact Auth/Flutter runtime compatibility evidence.

**Adjacent-value checkpoint:** a confirmed false-green in the current release-evidence oracle was reproduced, its source-level admission path corrected in both verifier and collector, and new negative cases added without changing LogMate or other specialist repositories. Further promotion requires the actual hosted 40-case/33-case results, an independently approved NORMAL preview and Chromium/Safari/managed-iPad runtime evidence. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**

## 8. Canonical-route and sanitized-evidence false-green correction (2026-10-25) [SOURCE / CONTRADICTION / VALIDATION]

### 8.1 Causal audit — the verifier was broader than the capture client

At run start the canonical `main@f0d77953` governance, tracks, roadmap, status/index, 517/518, exact JS/CI files and recent commits were read. Design Studio W120/CD127, Engineering Q006 and Marketing D8/D10 were inspected read-only. The highest-value Stage 8 bottleneck remained **E evidence admission / privacy**, with A URL mechanics and C independent negative controls; B/D consume transfer findings.

The existing 517 gate accepted plan route `/auth/../action` even though the 518 collector refused dot-segment routes. It also accepted an evidence response with additional `Set-Cookie: session=SECRET` and `Authorization: Bearer SECRET` headers, even though the collector intentionally stripped them. An exact committed-gate V8 reproduction returned `SERVED_HEADER_CONSISTENT_UNVERIFIED` for a plan/response containing both the dot-segment route and those extra credential-bearing fields. A separate `https://foo.internal/` envelope also passed the *consistency-only* gate; the collector's origin/network policy remains intentionally stricter. These are **research evidence-admission false greens**, not proof that LogMate exposed credentials or that an HTTPS request to a prohibited host occurred.

**SOURCE:** RFC 3986 §5.2.4 and §6.2.2.3 (dot-segment removal), https://www.rfc-editor.org/rfc/rfc3986 ; WHATWG URL Standard (URL path parsing and canonicalization), https://url.spec.whatwg.org/ ; W3C CSP Level 3 Working Draft 2026-09-16, https://www.w3.org/TR/CSP/ ; GitHub Actions push/path semantics, https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows . Sources checked 2026-10-25.

**SYNTHESIS:** exact equality between two *untrusted* evidence envelopes does not imply a canonical route, sanitized evidence, a trustworthy collector, or browser CSP enforcement. The 517 JSON gate is an independently usable comparator; therefore its admissible route/header vocabulary cannot rely solely on a caller having used 518 first. URI normalization can make a visually different path resolve to a different route, and preserving authentication response fields in research artifacts violates the collector's stated minimization objective.

### 8.2 Bounded correction [MINTTAP DECISION]

- 517 now owns `safeEvidenceRoute` and a shared `SAFE_CAPTURE_HEADERS` allowlist plus `admissibleEvidenceHeader` / `sensitiveEvidenceValue` predicates. The gate rejects dot-segment and protocol-relative plan paths, excessively long routes, non-allowlisted plan/response headers, control characters and the existing explicitly recognized action-token patterns even when the plan itself pins the same unsafe value. Both *planned* and *observed* header arrays are validated.
- 518 imports these predicates instead of maintaining a second route/allowed-header vocabulary. Its collector still **drops** non-allowlisted raw headers, preserving the intended sanitized capture format. Explicitly sensitive values in allowed fields fail with `SENSITIVE_HEADER`, preserving the existing negative-test contract; other invalid allowed fields fail closed.
- The gate's `SERVED_HEADER_CONSISTENT_UNVERIFIED` verdict remains deliberately weak: it is neither proof of a real TLS exchange nor proof that a policy blocks a script. The 517 gate does **not** become a network-target authorization service; 518 retains separate HTTPS origin, DNS/IP, TLS and egress controls. Syntactically valid `.test` fixtures remain usable in offline gate self-tests.

### 8.3 Adversarial evidence [VALIDATION]

Eight new deterministic 517 self-test negatives cover dot-segment traversal, protocol-relative path, extra cookie, extra authorization, extra unknown header, planned cookie, planned CSP containing `oobCode`, and NUL in an otherwise allowlisted header. The exact **committed** 517 gate was re-fetched and executed in V8: **41/41 deterministic self-test outcomes; baseline `SERVED_HEADER_CONSISTENT_UNVERIFIED`; zero failures.** Prior pre-fix false-green reproduction was also executed against the earlier committed gate. The 518 collector suite adds one **collector→gate** end-to-end synthetic case distinguishing enforce and report-only responses, with explicit cookie redaction and a negative mutation. **Expected Node top-level collector tests: 41; exact Node suite/hosted GitHub Actions conclusion NOT VERIFIED.** These are code-level oracles, not a live HTTPS capture or Chromium/Safari test.

| Distinction | What this checkpoint proves | What remains OPEN |
| --- | --- | --- |
| Route admission | 517 and 518 now share conservative dot-segment/protocol-relative rejection | Actual Hosting rewrite/redirect/alias behavior |
| Evidence minimization | 517 refuses credential-bearing/unknown evidence headers; 518 filters raw response headers | Complete sensitive-data taxonomy, encoded/double-encoded tokens, actual log/artifact custody |
| CSP plan consistency | 517 pinned-policy requirement remains; expected/observed header comparison preserved | Actual browser-enforced CSP, multiple policy interaction, third-party SDK/Auth compatibility |
| CI | Code changed in workflow-watched paths | Exact run ID, Node 41/41, gate 41/41 hosted steps and final conclusion |
| PWA product | No LogMate changes | NORMAL artifact/HTTPS, Worker, 37-store external restore, managed iPad/MDM |

### 8.4 Cross-track transfer, counterexamples and operational judgment [DEPENDENCY / TRANSFER VALIDATION / OPEN]

- **E owner:** evidence minimization, approved origin, collector/gate custody and release decision remain independent. A sanitized JSON object can still be fabricated; do not promote comparator PASS into attested collection.
- **A supplier:** URI dot segments and browser URL normalization are distinct from literal plan-string equality. Safari, Chromium, Firebase Hosting and Worker route behavior still require exact deployed tests.
- **C challenger:** new eight-case falsification plus one cross-component collector→gate synthetic case. Hosted Node and actual browser negative-control execution remain OPEN; a configured workflow is not a run.
- **B transfer:** Design Studio W120/CD127 still requires exact visible↔accessible↔actual-action semantics for Auth/offline/restore; no reassurance string may imply verified security from JSON gate output.
- **D transfer:** Marketing D8/D10 still prohibits unverified PWA/offline/advertising claims and Auth action-code analytics. Reject leaking sensitive response values into telemetry or diagnostics.

**CONTRADICTION:** rejecting known token patterns is not a complete DLP engine; whitelisting headers does not prove that all permitted values are non-sensitive. A valid CSP containing only `img-src` can be textually consistent without proving script blocking; script execution requires independent positive/negative browser probes. A current HTTPS response does not prove an old installed Worker has relinquished control. No synthetic result establishes 37-store durability or managed EFB installability.

**Adjacent-value check:** after reproducing the independent-gate false green, the run completed shared-predicate integration, additional negative controls, collector→gate cross-check design and specialist transfer without another generic CSP primer. The next meaningful boundary is exact Node/hosted execution and independently approved NORMAL HTTPS/browser/device evidence. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**
