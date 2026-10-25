# 519 — Stage 8 PWA Browser Runtime Admission: CSP, Worker, Auth, Offline and Managed iPad

Date: **2026-10-25 (Asia/Seoul)**  
State: **SOURCE + SYNTHESIS + EXECUTION CONTRACT + FAILED ENVIRONMENT ENTRY; NO PRODUCT/REAL-BROWSER PASS**  
Canonical Web Manager start: `main@3bddc55235e7d4139f17af19c5950d9183aa1438`.  
Owner: **E Security/Operations**, with **A Browser/Platform** and **C Quality/Independent Oracles** as critical suppliers; **B UX/IA** and **D Discovery/Measurement** consume the evidence. This is a materially different runtime-admission domain after 517/518's hosted synthetic CI proof, not another CSP header primer.

## 1. Why this stage and what the prior evidence does NOT prove [SOURCE / SYNTHESIS]

Research [517](517_stage8_pwa_served_header_evidence_admission_20261025.md) owns route/CSP expectation and sanitized evidence admission. [518 §11](518_stage8_pwa_approved_https_capture_and_browser_admission_contract_20261025.md) establishes **hosted Node 22.16.0 synthetic 41/41 collector + 41/41 gate PASS** at run `40136992197`, tested executable head `93f156118df73324df0fb1d2bc4799418b4de690`. The latest start commit is documentation-only downstream of that executable identity. Those tests establish a research tool's bounded behavior, not an actual server, CSP enforcement, worker lifecycle, authenticated LogMate session or EFB device.

**Problem:** browser policy is a *runtime decision* on actual responses and scripts. A textually approved CSP can permit dangerous script execution; a Report-Only header can report without blocking; a page may have the intended CSP while a worker executes under a different policy; an installed old worker may continue serving a cached document; a desktop browser result cannot establish a Home Screen app's data container or MDM policy. The next gate needs **independent positive and deliberately failing runtime controls**, plus source/artifact/host and state provenance.

**MINTTAP DECISION:** promote no PWA release/security/offline/storage claim from 517/518 synthetic PASS. The minimal progression is:
`APPROVED_PRODUCT_ARTIFACT → APPROVED_HTTPS_CAPTURE → CHROMIUM_RUNTIME_NEGATIVE+POSITIVE → APPLE_SAFARI_RUNTIME → PHYSICAL_MANAGED_IPAD → DATA_CUSTODY/RESTORE → RELEASE_AUTHORITY`.
These are distinct evidence tiers; success is not transitive. An explicitly approved test plan is a prerequisite, not an assertion that a deployment exists.

## 2. Current primary platform and tool facts [SOURCE / CHANGE WATCH]

Sources rechecked **2026-10-25**:
1. W3C CSP Level 3, https://www.w3.org/TR/CSP/ — enforced and Report-Only policies differ; each delivered enforced policy applies; worker execution and fetch integration require actual browser checks. `script-src` or `default-src` shape alone is not a complete security guarantee.
2. MDN `SecurityPolicyViolationEvent.disposition`, https://developer.mozilla.org/en-US/docs/Web/API/SecurityPolicyViolationEvent/disposition — `enforce` means blocked, `report` means observed; event delivery is corroboration, not a substitute for actual script execution/absence.
3. MDN `worker-src`, https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/worker-src — worker script loading policy fallback `worker-src → child-src → script-src → default-src`. The worker's own fetched-resource policy must be inspected on its own response.
4. Service Workers, https://w3c.github.io/ServiceWorker/ ; MDN controller, https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controller — registration/installation/activation and *document control* are distinct; do not infer a controlled document merely from an active registration.
5. web.dev update lifecycle, https://web.dev/learn/pwa/update — a waiting worker avoids uncontrolled old/new version overlap; `skipWaiting()` and `clients.claim()` can cause a mixed-generation client and must not be adopted uncritically for a durable ledger.
6. Playwright service-worker documentation, https://playwright.dev/docs/service-workers and https://playwright.dev/python/docs/service-workers — Playwright's **service-worker instrumentation APIs are Chromium-only**. Playwright WebKit engine testing is **not Safari.app**, **not iPadOS Home Screen**, and does not establish native Safari SW instrumentation. In-page browser API observations may be useful but must be classified separately.
7. Firebase Hosting configuration, https://firebase.google.com/docs/hosting/full-config — custom headers match the **initial URL before rewrite**; aliases must be observed independently. A source `firebase.json` is not a live header capture.
8. WebKit Safari 26, https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ — iOS/iPadOS 26 Home Screen defaults to opening added sites as web apps, with an option to disable; this is **not** proof of a managed device's permission to create/use one.
9. WebKit Safari 17.2, https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ — cookies can be copied at Home Screen web-app creation, but **other local storage is not copied**; data containers are not automatically shared after installation.
10. WebKit storage policy, https://webkit.org/blog/14403/updates-to-storage-policy/ — quota and origin eviction are distinct from durable export/restore. StorageManager estimates do not guarantee persistence.
11. Apple supervised device restrictions, https://support.apple.com/en-ca/guide/deployment/dep6b5ae23e9/web — a policy disabling Safari also prevents Web Clips. Apple managed data flow, https://support.apple.com/en-ae/guide/deployment/depaa73a4973/web — Managed Open In can restrict document transfer; do not infer Files/export success from an unmanaged iPad.
12. Apple content filtering, https://support.apple.com/en-ca/guide/deployment/dep1129ff8d2/web — organization DNS/proxy/filtering can independently affect origin reachability.
13. Software Engineering Studio `progress/STATUS.md`: M006 bounded macOS Safari lifecycle transfer and Q006 CI-verdict controls do not establish exact LogMate iPad execution. Design Studio `progress/WEB_STATUS.md` / CD127 requires actual visible↔accessible↔action semantics; Marketing Manager `STATUS.md` D8/D10 keeps unverified PWA/export/sync and advertising claims on HOLD.

**CONTRADICTION:** “WebKit engine automation PASS” must not be labeled “Safari/iPad PASS”; “Home Screen web-app option exists” must not be labeled “company iPad installable”; “Safari login worked” must not be labeled “Home Screen local ledger migrated”; “worker active” must not be labeled “this document controlled”; “network restored” must not be labeled “Manual Delta Sync completed”.

## 3. LogMate product boundary refreshed read-only [SOURCE / DEPENDENCY]

LogMate latest observed `main@4101ec7380796300f68fa60dbc7e5b6061f00080`; `AGENTS.md` says `MASTER.md` is the only current product-state authority, while code is implementation evidence. `MASTER.md` confirms **Firebase UID account-required** Apple/Google/Email+Password entry, with previously unlocked verified owner retaining defensible local offline use through temporary network/token failure. `docs/specs/local-first-manual-delta-sync-contract.md` confirms **user-initiated Manual Delta Sync** as the approved design, **production sync NOT IMPLEMENTED**, with whole-ledger `.lbk` export/import preferred for device migration. Do not revive historical account-free or automatic unattended P2P-sync assumptions.

Checked-in `firebase.json@9ac0972e26749215c4a718360c66315c6caf3cc8` has catch-all Cache-Control and rewrites for `/auth`, `/auth/`, `/auth/action`; it does **not** itself declare CSP/Referrer-Policy. `web/auth/action/index.html@39d06a633ab7bee719b3401bc3ac744f8ba175d0` contains an inline module importing Firebase JS modules from `www.gstatic.com` and reads action-link `oobCode` from the URL. The correct CSP requires an independently inventoried runtime dependency graph and safe handling of token-bearing URLs. A checked-in `web/logmate_service_worker.js` path was **not found** at this head; generated output must be obtained from the **exact approved build**, not inferred from a nonexistent source path or earlier generated snapshot.

**OPEN:** exact NORMAL archive and hashes, preview origin, deployed CSP/header values, Firebase provider setup, worker generated bytes/scope, real external `.lbk` file save/reopen/37-store restore, and actual managed EFB policy. No LogMate files were modified.

## 4. Admission and falsification matrix [MINTTAP DECISION — PROPOSED TEST CONTRACT]

Every case records: `caseId, exact source SHA, approved build artifact SHA, deployed origin, environment tier, OS/browser version, install/container mode, management-policy envelope, fixture identifier, setup/preconditions, action, expected oracle, observed result, negative-control result, PASS/FAIL/UNKNOWN, sanitized evidence locator`. A case with missing prerequisite or unexecuted negative control is **UNKNOWN**, not PASS. Each browser/environment must run its own fixture and its own verdict; do not aggregate a union of partial passes into one platform PASS.

| IDs | Scenario / positive and negative oracle | Tier required |
| --- | --- | --- |
| R01–R02 | Exact approved NORMAL source/build/served response SHA and TLS chain; reject mismatched body, unexpected redirect, unapproved host or ignored TLS error. | Independent HTTPS |
| R03–R04 | Each initial URL `/`, `/index.html`, `/auth`, `/auth/`, `/auth/action`, `/auth/action/index.html`, worker script and provider-reserved `/__/...` observed separately; no HTML masquerading as JS. | Independent HTTPS |
| R05–R06 | **Enforce** CSP: allowed first-party boot code executes, deliberately injected disallowed inline/external DOM script does **not** execute; `securitypolicyviolation` `disposition=enforce` corroborates. | Chromium + Safari |
| R07–R08 | **Report-Only**: deliberately disallowed script **does** execute, report event `disposition=report`; do not mislabel a report as a block. | Chromium + Safari |
| R09–R10 | Multiple enforced CSP headers are jointly restrictive; worker script fetch/execution policy assessed independently of document CSP; negative attempt must be observed. | Chromium + Safari |
| R11–R12 | Auth action links: valid/expired/invalid/fake-code/network cases, safe referrer and URL/report/log handling; no real codes in CI, HAR, telemetry or GitHub. Provider `/__/...` classified separately. | Approved disposable Auth environment |
| R13–R14 | Worker registration, `installing/waiting/active`, `controller` and `controllerchange` distinguished; positive controlled app navigation and negative excluded auth navigation. | Chromium; native Safari independently |
| R15–R16 | Cold first visit vs warm controlled revisit; origin-down offline app reopen **after a truly controlled client**; excluded auth route must not silently render cached Home. | Chromium; Safari; installed iPad |
| R17–R18 | Two worker generations, waiting/activation, old/new document overlap and rollback; preserve unique ledger/draft data across update/reload/failed migration, no origin-wide clearing as default recovery. | Chromium; Safari; installed iPad |
| R19–R20 | IndexedDB and Cache Storage persistence are tested separately across close/relaunch/storage pressure; `persisted()` and `estimate()` are diagnostics, not a backup receipt. | Physical iPad + other target devices |
| R21–R22 | External `.lbk` saved, reopened from independent Files location, validated, restored to a new DB and compared for **all 37 stores**; missing/duplicate/corrupt/wrong-owner cases fail safely. | Real file/restore workflow; managed iPad separately |
| R23–R24 | Managed iPad: Safari/Web Clip allowance, web filtering/proxy, Home Screen creation, launch, managed/unmanaged Files destinations, offline after restart, update, storage survival; distinguish from unmanaged device. | Representative supervised/MDM iPad |
| R25–R26 | Manual Sync UI states `local saved`, `queued`, `remote receipt`, `applied`, `conflict` mapped to actual authority; no automatic unattended sync/advertising claims inferred. | Exact implemented product + independent receipts |
| R27–R28 | Keyboard/focus/ARIA/live region on auth-expiry/offline/update/restore, responsive layout, navigation recovery; real accessible name/role/state compared with actual action and result. | Runtime + assistive tech + representative human |
| R29–R30 | Acquisition/analytics only query-free privacy-eligible events; no action-link code, pilot records or unapproved third-party script. Unsupported PWA/ads/offline marketing claims remain HOLD. | Product/Marketing approval |

**Oracle rules:** a negative script must be created as a real DOM `<script>` or network resource under the document CSP. `page.evaluate('window.flag=true')` is automation-controlled JS and **is not evidence of script permission**. Assert both **absence of the forbidden effect** and **presence of a permitted baseline effect**; collect a sanitized violation disposition as corroboration. For Worker, assert `navigator.serviceWorker.controller` after navigation; `registration.active` alone is insufficient. For offline, do not confuse a page still held in memory with a cold/reopened app; explicitly log whether the server was stopped, browser network disabled, profile persisted, and whether the app was newly launched.

**False-green controls:** report-only accidentally labeled enforce; missing violation event interpreted as a pass; baseline script failing yet negative also blocked; blocked Worker registration misread as offline success; stale cached HTML counted as fresh server response; test runner `ignoreHTTPSerrors` counted as TLS PASS; fake success from fixture-derived expectation; product data lost during cleanup; Safari-WebKit automation counted as managed iPad; 37-store count without independent reopen; backend receipt equated with local apply; manually selected test route not matching Firebase rewrite alias.

## 5. Execution packet, independence and security custody [VALIDATION PLAN / OPEN]

1. **Product owner / Engineering:** approve exact NORMAL build/archive digest, origin and disposable test accounts/records. Freeze independent expected response/body hashes before capture. No actual user email action tokens or flight records.
2. **E/C:** run 518's read-only collector against the approved **publicly reachable** test origin with DNS/TLS validation, pinned route inventory and fail-closed verdict; keep response/header/body evidence separate from expected policy approval. Never use loopback/private IP exceptions in the production collector.
3. **A/C:** in Chromium, execute R05–R18 with a clean browser profile, controlled vs uncontrolled page, positive and negative CSP probes, worker registration/scope and two-version rollback; attach exact version, hashes, time and sanitized screenshots/console summaries. Do not promote to Safari.
4. **A/C:** run equivalent tests in **actual macOS Safari** using its supported browser automation and/or human-run protocol. A Playwright WebKit engine result is a separate supplemental tier. Physical iPadOS Safari and Home Screen are additional tiers, not inherited passes.
5. **E/B/C:** run managed-iPad envelope and `.lbk` file-custody/recovery with disposable synthetic ledger. Validate source/destination ownership, policy-controlled Files transfer and independent reopen; use explicit human/AT state evidence. No destructive reset without separate protected backup.
6. **D:** only after real product capability exists, evaluate privacy-safe discovery/install/analytics continuity and claim approval. Never add a third-party ad tag to obtain a measurement signal during security acceptance.
7. **E release authority:** preserve a machine-readable FAIL/UNKNOWN/PASS per case and tier; independently review contradictions. No `GO` from green CI or a screenshot. On failure, HOLD and preserve unique local data before attempting recovery.

**Suggested browser harness shape (NOT YET EXECUTED):** local disposable HTTPS server returns different enforce/report-only/multi-policy headers; permitted external bootstrap installs `securitypolicyviolation` listener; real DOM-inserted script is the negative control; separate root-scoped worker fixture caches only app navigation and bypasses auth/provider paths; a clean profile is used for each variant. The harness must be isolated from product endpoints, secrets and pilots. Test-only self-signed TLS bypass must be labeled **LOCAL SYNTHETIC / TLS NOT VERIFIED**. Do not wire an unverified harness into product release CI as a trusted oracle.

### Actual execution-environment attempt (2026-10-25) [VALIDATION / BLOCKER]

A disposable local HTTPS Python/Playwright fixture was constructed and **attempted**, not promoted. `python playwright` was importable; Node 22.16.0 and system Chromium 144.0.7559.96 were present. Default Playwright browser binaries were missing; explicitly launched system Chromium reached browser startup, but local HTTPS navigation to `127.0.0.1` failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR` **before the first CSP probe**. Playwright WebKit's required binary was absent. No policy bypass or unapproved external endpoint was attempted. Thus **0/0 CSP/Worker browser cases executed**, **not 0/4 FAIL** and **not a Chromium/WebKit product result**. The local uncommitted prototype is **not** accepted as a validated test tool. A controlled runner with approved localhost/fixture networking and installed browser binaries is required; this is a **test-environment blocker**, separate from missing approved product artifact/preview.

## 6. Cross-track pressure, transfer and operational judgment [DEPENDENCY / TRANSFER VALIDATION / CONTRADICTION]

| Track | Evidence maturity / pressure | Allocation and ownership |
| --- | --- | --- |
| **E — Security/Operations** | Stage 8 highest-risk; hosted synthetic proof exists, real response/artifact/MDM custody absent. | **Primary:** release admission, origin/TLS, worker/update incident/backup boundaries and authority. |
| **A — Platform/Browser** | CSP/Service Worker foundation sound; exact Chromium/Safari runtime and OS capability unresolved. | **High:** lifecycle, scope/control, policy interpretation, Home Screen vs browser context. |
| **C — Quality/Accessibility** | Hosted 41+41 research tests PASS; independent browser negative controls, AT and physical iPad absent. | **High:** discriminating runtime oracle, tier isolation, failure diagnostics and data-safe stress. |
| **B — UX/IA/Content** | Design Studio W121/CD127 static semantic work saturated; actual accessible state/action evidence absent. | **Transfer:** specify observable saved/queued/offline/expired/recovery messages only against real implementation. |
| **D — Search/Analytics** | Marketing D8/D10 public claim and ads HOLD; no production attribution/consent evidence. | **Transfer:** privacy-safe measurement and claim truth after implementation, not another acquisition primer. |

**CONTRADICTIONS:** Safari 26's Home Screen default does not override MDM restrictions. Safari's creation-time cookie copy is not IndexedDB/Cache Storage migration. `Service Worker active` is not `controller present`. A report-only violation is not blocked execution. HTTPS collector PASS is not browser CSP PASS. An account-required Firebase UID contract does not prove network availability while offline, and the approved Manual Delta Sync contract does not mean Sync implementation exists. A WebKit engine run cannot be promoted to native Safari or supervised iPad.

**CHANGE WATCH:** W3C CSP3 and worker policies, Playwright engine instrumentation, Chromium/WebKit browser releases, Safari 26 Home Screen behavior, WebKit quota/eviction, Apple MDM Safari/Web Clip/Managed Open In policies, Firebase Hosting aliases, generated Flutter worker, LogMate account and Manual Delta Sync implementation, approved product/CI artifacts.

## 7. Checkpoint and next high-information-gain boundary [OPEN]

The adjacent question after 518's hosted CI success was **what evidence can actually distinguish effective CSP/Worker/Auth/offline behavior from false green?** This bundle completed primary-standard and product-authority reconciliation, 30 case IDs, positive/negative oracle design, WebKit-vs-Safari tier separation, Apple managed-device restrictions and a bounded browser-environment attempt. The next valuable step **cannot be promoted here** without a working authorized browser runner and independently approved NORMAL HTTPS product artifact. No additional speculative CSP policy string, third-party ad tag, product edit or duplicate Design/Marketing/Engineering research is justified.

**Gate:** **Stage 8 ACTIVE · hosted synthetic research-tool 41+41 PASS · browser/runtime admission NOT EXECUTED · Production validation OPEN · PWA release HOLD.**


## 8. Executable local Chromium CSP negative-control bridge (2026-10-25) [SOURCE / VALIDATION / OPEN]

**Problem and decision.** R05–R10 previously specified actual browser execution oracles, but the attempted disposable Playwright runner was blocked before the first probe. Repeating a header-only comparator would not reduce this gap. A new **Web Manager-only** executable lab and least-privilege hosted workflow now exercise the *browser's actual DOM-script execution* on a disposable loopback fixture, not the product endpoint. This is a **lower-tier prerequisite** to approved HTTPS/product/Safari testing, not a substitute for them.

**Committed implementation:**
- `research/handoffs/pwa_chromium_csp_runtime_lab.mjs` — Node 22 standard-library HTTP server bound to `127.0.0.1`, per-case fresh Chromium profile, headless DOM capture, bounded subprocess, no user secrets, no third-party network, no product endpoint, sanitized PASS/FAIL/UNKNOWN case output.
- `research/handoffs/test_pwa_chromium_csp_runtime_lab.mjs` — six Node test groups covering positive/negative oracles, malformed/missing results and fixture policy-header separation.
- `.github/workflows/pwa_chromium_csp_runtime_research.yml` — `ubuntu-24.04`, Node 22.16.0, full-SHA-pinned checkout/setup-node, read-only permissions, exact-triggering-revision checkout, unit and real Chromium phases. Only research files/workflow trigger push; manual dispatch also available. Workflow uses installed Chrome/Chromium and makes no deployment or product mutation.

**Four runtime cases (actual DOM `<script>`, not `page.evaluate`):**

| Case | Positive oracle | Negative / distinction oracle | Failure meaning |
| --- | --- | --- | --- |
| `enforce` | Same-origin external bootstrap and allowed script execute | Disallowed inline script does **not** execute; `securitypolicyviolation.disposition=enforce` observed | Allowed baseline fails, inline runs or enforcement evidence absent |
| `report` | External bootstrap and inline script **both execute** | `disposition=report` observed; report-only must not be mislabeled as blocking | Inline blocked or report evidence absent |
| `multi` | Same-origin baseline executes | Two separately emitted enforced CSP headers jointly restrict inline execution even though one header allows it | Treating later header as an override |
| `unrestricted` | Both external and inline scripts execute | No CSP violation event | An environment-wide script block or fabricated negative success |

**Admission discipline.** The allowed baseline must succeed in each case, and the negative behavior must be observed. Missing result/PENDING is **UNKNOWN**, not PASS. Mixed `enforce`+`report` dispositions are **FAIL**, not a partial match to the expected policy; two additional negative assertions were added to the same six-group suite. A violation event corroborates execution evidence but cannot replace it. The browser test is bound to **loopback HTTP**, which browsers treat as a potentially trustworthy development origin for relevant APIs; this is expressly **NOT TLS CERTIFICATE VERIFIED**, not deployed HTTPS, and not a CSP test on LogMate's real scripts. Headless Chrome is a Chromium-tier laboratory result only; neither Safari.app nor managed iPad is inferred. The `--no-sandbox` browser flag is confined to this disposable CI/lab process and is not an endorsed product runtime setting.

**Observed evidence and limitations.** A locally assembled first implementation's six Node oracle/fixture groups passed **6/6** under Node 22.16.0. The same local environment's Chromium 144 attempt produced **four UNKNOWN / CHROME_TIMEOUT**, with no completed DOM probe; earlier 519 Playwright attempt independently returned `ERR_BLOCKED_BY_ADMINISTRATOR`. These are **test-environment non-executions**, not evidence that CSP failed in Chromium or that the product is vulnerable. The GitHub-committed module is a separately written equivalent implementation: its exact hosted unit/browser result is **OPEN until an identified GitHub Actions run and log are inspected**. Commit existence and a YAML trigger do not establish CI execution or success.

**Sources rechecked 2026-10-25:** W3C CSP Level 3 https://www.w3.org/TR/CSP/ ; Chrome Headless CLI https://developer.chrome.com/docs/chromium/headless ; Chrome DevTools/Headless source https://github.com/GoogleChrome/developer.chrome.com/blob/main/site/en/articles/new-headless/index.md ; Playwright Service Workers https://playwright.dev/docs/service-workers ; GitHub runner image https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md . Browser/runtime version and runner image are CHANGE WATCH.

**Five-track ownership and transfer.** **E** owns the enforce/report-only release-trust distinction and tier admission; **A** owns Chromium CSP/runtime mechanics and the separation from Safari/Worker contexts; **C** owns the executable negative-control and fail-closed result contract; **B** consumes Design Studio W120/CD127 for eventual visible/accessible/action truth; **D** consumes Marketing D8/D10 to prohibit claims of verified offline/security/sync or web-ad readiness. No generic Design/Marketing/Engineering primer was duplicated and no external repository was changed.

**Adjacent question checked:** Can this lab close R11–R30, auth token leakage, Worker control, source→NORMAL artifact→host provenance, 37-store external restore or managed-iPad readiness? **No.** Those require different runtime fixtures, approved product bytes and device/provider evidence. Extending the local CSP fixture to pretend otherwise would create a false green. **Gate remains Stage 8 ACTIVE / synthetic research CI previously 41+41 PASS / new Chromium lab hosted result OPEN / product browser admission OPEN / Production validation OPEN / PWA release HOLD.**
