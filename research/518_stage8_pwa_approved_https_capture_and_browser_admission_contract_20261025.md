# 518 — Stage 8 PWA Approved HTTPS Capture, Release Verdict Propagation and Browser Admission

Date: **2026-10-25 (Asia/Seoul)**  
State: **SOURCE + PRIMARY STANDARD + CROSS-TRACK SYNTHESIS + EXECUTABLE SYNTHETIC CAPTURE 32/32; LIVE HTTPS / BROWSER / MANAGED-IPAD / PRODUCT VALIDATION OPEN**  
Canonical starting Web Manager main: ffb9db81fb51e92389914c6c47dd05eafd6c1fc6. LogMate firebase.json blob 9ac0972e26749215c4a718360c66315c6caf3cc8 inspected read-only.  
Primary owner: **Track E** (trust, release/incident and approved endpoint). A supplies HTTP/TLS/CSP/Worker semantics; C independent falsification and verdict propagation; B auth/offline recovery state truth; D privacy-preserving measurement and publisher claims.

## 1. Highest-value bottleneck [SYNTHESIS]

517's 26/26 synthetic verdict oracle was not a collector: it compared two caller-provided JSON objects. The unresolved Stage 8 risk is an evidence-laundering path: a self-reported body SHA, header map or successful CI command can be promoted to “served HTTPS policy passed” without independently fetched representation bytes. The next coherent step is a read-only HTTPS capture tool that hashes received response bytes, preserves duplicate security-header fields, refuses redirects, avoids auth-code query strings and fails closed before it writes an evidence artifact. It does **not** close the separate browser-policy, source→NORMAL archive→host, or managed-iPad gates.

The reviewed LogMate firebase.json configures only catch-all Cache-Control and three auth rewrites, not a source-configured CSP/Referrer-Policy. Do not infer what the deployed server currently serves. The checked-in Worker excludes /auth/ and /__/ from interception; a path bypass does not isolate origin execution authority. Reuse 516/517 instead of creating another CSP primer.

## 2. First principles, standards and live-project meaning [SOURCE / SYNTHESIS]

1. **History/problem:** build file ≠ uploaded artifact ≠ served response ≠ browser-enforced policy. An HTTP 200 can be a rewrite, stale Worker response or HTML served under a JS URL. Hashing received bytes is necessary but not sufficient to establish intended code provenance.
2. **HTTP transport:** use a real HTTPS GET with certificate verification; avoid browser cookie/session context. A network collector is not a browser and cannot observe an installed Worker or enforce CSP. Node rawHeaders preserves duplicate header instances; flattening headers can erase conflicting policies.
3. **Hosting semantics:** Firebase custom headers match the initial URL **before** rewrites; /auth, /auth/, /auth/action and /auth/action/index.html require distinct probes. A Hosting rewrite is not necessarily an HTTP redirect. Provider-reserved /__/ is a separate policy/ownership boundary.
4. **CSP semantics:** Report-Only does not block execution. Multiple enforced policies can compound restrictions. The Worker global's response policy must be checked separately. Do not infer effective script allowance from a single CSP string or vendor allowlist.
5. **Capture confidentiality:** never send a real Firebase oobCode, password reset URL, cookies, Authorization header, flight records or personal query string to a diagnostic collector. Use query-free public route probes; capture only approved policy/representation headers and hashes, never bodies.
6. **Trust independence:** approved expectation must be independently pinned to an exact NORMAL archive and approval identity. A plan generated from the same HTTPS response is a circular oracle. Collector metadata and TLS verification do not cryptographically attest the capture artifact or bind it to GitHub release authority.
7. **Negative controls:** reject malformed path/duplicate route, non-HTTPS or foreign origin, redirect, unexpected body, missing enforced/report header, incorrect MIME, absent nosniff, duplicate singleton header and CI exit-code loss. Requiring clean test exit is separate from verified product PASS.
8. **Update/rollback:** host rollback can restore earlier executable authority; an installed Service Worker may continue serving a cached document with old policies. Treat current server capture and Worker-controlled browser session as different cohorts.
9. **iPadOS installation CHANGE WATCH:** WebKit's Safari 26 announcement says on iOS/iPadOS 26 every Home Screen addition opens as a web app by default, unless the user turns off “Open as Web App.” This is an OS/UI rule, **not** proof that a managed iPad permits installation or that IndexedDB transfers from Safari. Old “manifest required for Safari installability” claims are not universal.
10. **Durability:** WebKit documents origin storage quota, persistence heuristics and eviction. A secure hosted shell cannot substitute for independently verified external backup and 37-store semantic restore. Do not erase origin data as a CSP/Worker repair shortcut.
11. **UX/analytics:** browser-tested auth-expired/offline/restore states must correspond to actual action and accessible name/role/status (Design Studio W120/CD127); exclude action-code query from analytics, referrer, crash capture and CI logs (Marketing D8/D10).
12. **Release judgment:** correct output of synthetic capture tests is **COLLECTOR_TESTED**. Only independently approved endpoint, actual NORMAL archive, authenticated capture custody, 517 gate, real browser negative CSP tests, auth/offline regression, managed policy and data restore can support an eventual release decision.

Primary sources reviewed 2026-10-25:
- Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config
- W3C CSP Level 3: https://www.w3.org/TR/CSP/
- Node HTTP rawHeaders: https://nodejs.org/api/http.html
- Node HTTPS request: https://nodejs.org/api/https.html
- WebKit Safari 26 installation: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/

## 3. New executable capture [VALIDATION]

Files:
- research/handoffs/pwa_https_evidence_collector.js
- research/handoffs/test_pwa_https_evidence_collector.js
- Existing downstream research/handoffs/pwa_served_header_evidence_gate.js (517; **not modified**).

Collector contract: Node.js 22+ (stdlib only); explicit arguments:

    node research/handoffs/pwa_https_evidence_collector.js --plan APPROVED.json --allow-origin https://approved.example.com/ --out sanitized-capture.json

It performs sequential **GET** requests against an exact HTTPS origin; no credentials, cookies, query strings, POSTs, automatic redirect following or body retention. DNS lookup rejects private/reserved destinations, certificate verification stays enabled, body hashing is streamed and size-bounded (32 MiB per route), selected raw header instances are retained, and Set-Cookie/Location are excluded from output. Encoded bodies and action-code/token-like values in approved response headers are rejected; unexpected injected error codes are mapped to fixed failure codes to avoid leaking secrets. The CLI runs 517's semantic gate and writes with exclusive creation (mode 0600) **only after** SERVED_HEADER_CONSISTENT_UNVERIFIED; failures exit nonzero with fixed diagnostic codes. A capture remains **unattested** even if consistent. This collector is a research handoff, not a production CI deployment change.

**Local synthetic test evidence:** Node v22.16.0; running the test file with node --test yielded **32/32 PASS** on injected transport responses. Positive fixture checks three-route capture and header redaction; negative cases include origin/URL/route/hash/policy/schema, redirects, oversized responses, invalid headers, compressed body, DNS address classification and failure-message redaction. **No real HTTPS endpoint was contacted and the combined CLI→517 gate has not been executed against a real capture.**

### CI admission contract [MINTTAP DECISION / PROPOSED]

1. Engineering independently pins source commit, NORMAL archive digest and per-route expected body hashes; approves policy profile and exact endpoint; stores plan outside capture job's writable outputs.
2. CI uses a least-privilege, read-only, approved preview endpoint; pins collector+517 gate code identity; no secrets, tokens or real action links in fixture or log.
3. Node test suite must succeed as a separate step. Capture command must succeed **and** create a new sanitized JSON file. Downstream 517 gate must return exact semantic token; shell pipeline/tee exit status must be preserved. UNKNOWN/skipped job cannot become PASS (Engineering Q006).
4. Reviewer independently checks archive→host body identity and HTTPS collection provenance; a successful comparator alone does not authenticate the capture.
5. Run real Chromium/Safari positive and intentionally blocked script probes, Worker claim/old-generation/offline reopen, Firebase action-link flow with disposable fake tokens and no URL capture, focus/AT and data-preserving recovery. Test iPadOS 26 “Open as Web App” selection and MDM policy as distinct real-device envelopes.
6. Any mismatch or absent result remains **HOLD**; do not auto-deploy, reset local IndexedDB or promote lab test to managed EFB readiness.

## 4. Track balance and external transfers [DEPENDENCY / TRANSFER VALIDATION / CONTRADICTION]

| Track | Gate, depth and pressure | This integrated bundle |
| --- | --- | --- |
| **E** | Stage 8 applied bottleneck; provenance/custody/approval and recovery highest risk | Owns approved origin, collector and release verdict semantics; dominates work. |
| **A** | Browser/HTTP/CSP foundations available; Safari/WebKit/installed Worker reality OPEN | Supplies exact route, raw header and Home Screen vs Safari/MDM distinctions. |
| **C** | Synthetic 509–517 oracles mature; exact hosted and browser PASS missing | Owns 32 falsifications, negative controls, CI exit propagation and provenance transfer. |
| **B** | Static Design Studio content saturated before runtime | Consumes W120/CD127 for visible↔accessible↔actual auth/offline/recovery parity. |
| **D** | Marketing D8/D10 release/ads evidence HOLD | No action-code telemetry, no web ad rollout or verified-security/offline marketing claim. |

Read-only canonical transfers: Design Studio progress/WEB_STATUS.md, research/web/120-cross-concept-executable-stress-packet.md and research/content/127-pre-runtime-saturation-and-semantic-evidence-stop-rule.md; Software Engineering Studio progress/QUALITY_STATUS.md Q006 verdict semantics; Marketing Manager STATUS.md D8/D10. These disciplines are not duplicated. No LogMate/Design/Engineering/Marketing files changed.

## 5. Limits, evidence blockers and next meaningful boundary [OPEN / CHANGE WATCH]

- **OPEN:** independently approved preview origin, real NORMAL archive and body-hash plan, actual TLS response, unaltered capture custody, verified DNS/HTTP negative cases on real network, deployed CSP and Firebase Auth, Chromium/WebKit enforced-policy negative tests, old/new Worker session, 37-store external restore and managed iPad/MDM.
- **CHANGE WATCH:** Firebase pre-rewrite header matching and reserved namespaces, Node HTTPS/header handling, W3C CSP and browser enforcement, WebKit Home Screen behavior, storage quota/eviction, CI action version/verdict propagation and Flutter/Firebase module graph.
- **CONTRADICTION:** a 200 status + expected header strings cannot certify actual script blocking; a syntactically valid capture cannot certify approved deployment; a browser-only PASS cannot certify managed-EFB data durability. Reject all such promotions.
- **Adjacent-value checkpoint:** the 517 evidence-oracle gap was closed to the **synthetic read-only collector** layer and stress-tested with 32 cases. Next material work requires approved HTTPS host and independently pinned NORMAL bytes; additional ungrounded synthetic variants have lower information gain. **Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD.**

## 6. DNS target admission, slow-drip exhaustion and aggregate capture-budget correction (2026-10-25) [SOURCE / CONTRADICTION / VALIDATION]

### Trigger: existing collector's security claims required adversarial falsification

A read-only collector is still an outbound network client. The original 518 implementation relied on textual IPv6 prefix matching and a hand-maintained IPv4 exclusion list. This is not equivalent to the IANA special-purpose registries or normalized address-prefix evaluation. A locally reproduced copy of the **original** `publicIP` predicate returned `true` for four non-general-purpose addresses:

| Counterexample | IANA classification / issue | Old result | Revised expected result |
| --- | --- | --- | --- |
| `2001:0db8::1` | IPv6 documentation prefix, alternative textual spelling of `2001:db8::/32` | incorrectly allowed | reject |
| `3fff::1` | IPv6 documentation prefix `3fff::/20` (RFC 9637) | incorrectly allowed | reject |
| `2001:2::1` | IPv6 benchmarking `2001:2::/48` | incorrectly allowed | reject conservatively |
| `192.88.99.2` | 6a44/retired 6to4 relay special-purpose range | incorrectly allowed | reject conservatively |

This is a **confirmed source-level classifier defect** in the Web Manager research tool, not evidence of an SSRF exploit, real network connection or LogMate product vulnerability. The existing 32-case synthetic suite missed these equivalence classes; a prior green test count was not evidence of complete IP classification.

**Primary sources checked 2026-10-25:**
- IANA IPv4 special-purpose registry: https://www.iana.org/assignments/iana-ipv4-special-registry
- IANA IPv6 special-purpose registry: https://www.iana.org/assignments/iana-ipv6-special-registry
- IANA IPv6 global unicast assignments: https://www.iana.org/assignments/ipv6-unicast-address-assignments
- Node 22 `net.BlockList.addSubnet/check`: https://nodejs.org/api/net.html
- Node DNS lookup/OS resolver behavior: https://nodejs.org/api/dns.html
- Node HTTPS/TLS client behavior: https://nodejs.org/api/https.html

### Correction [MINTTAP DECISION — research handoff, not product]

The collector now uses Node `net.BlockList` parsed-prefix matching instead of textual IPv6 prefix comparison. IPv4 rejects private/shared/loopback/link-local/documentation/benchmarking/multicast/reserved ranges and deprecated 6to4 relay addresses. IPv6 must fall within `2000::/3` and must not match conservative special-purpose exclusions (`2001::/23`, `2001:db8::/32`, `2002::/16`, `3fff::/20`). These exclusions deliberately prefer false negatives over accidentally probing ambiguous addresses. They are **not** a claim that all remaining addresses are reachable or safe in every enterprise network; IANA's registry is a maintained source and additional special-purpose allocations can change.

`dns.lookup(..., {all:true})` now rejects an entire response set if **any** address is malformed, has a mismatched address family, or is nonpublic. It no longer silently selects one public address from a mixed public/private answer set. The selected address is passed through the HTTPS client's lookup callback; TLS certificate verification remains enabled for the requested hostname. An independently approved origin remains mandatory: public-address classification is not authorization to scan arbitrary hosts.

The original `req.setTimeout` only bounded socket inactivity, not a slow-drip transfer that periodically produces data. A separate wall-clock timer now destroys the request on expiry and is cleared on request close/error. A separate 128 MiB **aggregate** capture budget now complements the pre-existing 32 MiB per-response limit; remaining budget is passed into the streaming transport, and a fifth request is not started after four 32 MiB responses exhaust it. Five individually valid 32 MiB responses must fail as a combined collection. Neither change certifies a total CI job deadline; an approved runner must also impose an independent job-level timeout and egress policy.

### Adversarial execution and test boundary [VALIDATION]

- **Observed baseline:** the original classifier admitted all four counterexamples above in a local Node reproduction. This falsifies the former broad `DNS private/reserved rejected` assurance.
- **Isolated corrected-function Node v22.16.0 smoke:** 18 negative and 4 positive IP cases matched expected outcomes (**22/22**); a separate mocked HTTPS request exercised the wall-clock deadline (**1/1**). These are **isolated targeted executions**, not a byte-identical run of the complete GitHub collector.
- **Persisted GitHub source:** collector blob `02eebec22574903f6a89b83125ca56bab35ac4c7`; test blob `a5fde28caa0719b4c2087169dd02c6f255d36c03`. Both fetched again and parsed successfully by V8 (`new Function`, syntax only).
- **Four new top-level Node test cases** added to the existing 32-case suite: (1) special-purpose IPv4/IPv6; (2) mixed/malformed/empty DNS answers; (3) mocked slow-drip deadline; (4) aggregate inventory exhaustion with boundary success. **The updated full 36-case repository suite has NOT been executed** in this run because GitHub connector file bytes were not mounted into the local Node runtime. Do not label it 36/36 PASS. The prior 32/32 PASS belongs to the earlier uncorrected revision only.
- **No real network probes, production DNS, actual HTTPS, deployed CSP, Chromium/Safari or managed iPad tests** were performed. The repaired predicate has not been independently audited against the complete, evolving IANA registry or an enterprise proxy topology.

### Release/operations contract and 12-case negative matrix [DEPENDENCY / TRANSFER VALIDATION]

| Case | Falsifiable expected outcome | Owner |
| --- | --- | --- |
| N01 | Alternate-spelling `2001:0db8::1` rejected | A → E |
| N02 | `3fff::/20` and benchmarking IPv6 rejected | A → E |
| N03 | Deprecated 6to4 relay IPv4 rejected | A → E |
| N04 | Public-only IPv4/IPv6 DNS set allowed to connect, TLS still verified | A / C |
| N05 | Mixed public/private DNS answer fails before connect | E / C |
| N06 | Empty/malformed/address-family mismatch fails closed | E / C |
| N07 | Slow-drip response times out on wall clock despite periodic bytes | E / C |
| N08 | Aggregate body budget fails across routes | E / C |
| N09 | Redirect, encoded body and credential/action-code header rejected | E / C |
| N10 | Approval plan and source/archive hash independently pinned; collector cannot self-approve | E / Engineering |
| N11 | Runner egress/proxy, DNS resolution and TLS endpoint identity independently observed | E / Engineering |
| N12 | Actual browser enforced-CSP negative test plus Auth/Worker/offline/restore still required | A / C / B / D |

**Track allocation:** E remains Stage 8's release/egress/custody bottleneck and owns this correction. A supplies browser/HTTP/DNS normalization semantics, C owns independent negative controls and execution proof, B consumes truthful offline/auth/recovery states from Design Studio W121/CD127, and D continues to reject unproven privacy/security/offline/advertising claims under Marketing D8/D10. Engineering Q006 owns CI verdict/timeout transfer semantics; Web Manager does not replace Engineering implementation review.

### Remaining blockers, operational judgment and adjacent-value check [OPEN / CHANGE WATCH]

The collector still has no independently approved real endpoint, authenticated NORMAL archive/body-hash plan, production DNS/egress trace, real TLS response or browser enforcement evidence. Future work must independently audit full IANA address-class coverage, DNS/proxy and network namespace effects, and verify Node's exact connection/timeout behavior under real CI. A public IP can still be attacker-controlled; a TLS-valid endpoint can still serve unexpected content; an exact hash can still come from an unapproved artifact. These are distinct trust dimensions.

The adjacent-value question **was completed now**: rather than adding another CSP primer, the existing collector was falsified and corrected across address canonicalization, mixed DNS, slow-drip and aggregate resource exhaustion, with explicit synthetic-vs-runtime boundaries. Further release promotion now crosses a materially different evidence boundary (exact Node suite + approved host + actual browser/device). **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.**


## 7. Exact-source hosted regression execution boundary and read-only CI integration (2026-10-25) [SOURCE / VALIDATION / DEPENDENCY]

### Why this checkpoint matters [SYNTHESIS / CONTRADICTION]

Section 6's revised collector and four new regressions were committed but the **full updated 36-case Node suite had not run**. Targeted 22/22 IP and 1/1 timeout checks were not a substitute for exercising the exact repository tests and the 517 gate together. The next useful action is a *non-deploying hosted execution path*, not another isolated PWA primer or another ungrounded security-success claim.

At the beginning of this checkpoint, canonical Web Manager main was `b1213c15fed5964073b6214acb78372f1dffa8eb`. The five-track governance, roadmap, STATUS, index, 517/518, collector/test source and latest commits were read. Design Studio Web Stage 3 W121 still requires real runtime; Engineering Quality Q006 owns fatal verdict propagation; Marketing D8/D10 still hold unproven PWA/advertising claims. Product `MASTER.md` confirms account-required Auth and **user-triggered Manual Delta Sync**, not an automatic unattended PWA↔native sync assumption. These are bounded read-only transfers.

### Persisted executable workflow [MINTTAP DECISION — Web Manager research only]

Added [`pwa_https_evidence_research_tests.yml`](.github/workflows/pwa_https_evidence_research_tests.yml) at repository path `.github/workflows/pwa_https_evidence_research_tests.yml` (link from this research file: `../.github/workflows/pwa_https_evidence_research_tests.yml`). It is intentionally **read-only and non-deploying**, triggered on relevant `main` source/workflow changes and manually via `workflow_dispatch`.

- `permissions: contents: read`, `ubuntu-24.04`, 10-minute job timeout, no secrets, upload, deployment, third-party package install, credential persistence or privileged PR trigger.
- Checkout pinned to reviewed full SHA `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1); Node setup pinned to `actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1` (v7.1.0). Both full commits were fetched from their official GitHub repositories. Pinning code identity does **not** attest all transitive runner/network dependencies or create independent release approval.
- Node runtime requested as exact `22.16.0`, automatic package-manager caching disabled. Shell `set -euo pipefail` precedes three `node --check` commands, the exact committed `node --test research/handoffs/test_pwa_https_evidence_collector.js` suite, and `node research/handoffs/pwa_served_header_evidence_gate.js --self-test`.
- No actual preview origin, HTTP capture, credentials, production action-link, Worker process, or user ledger is involved. This workflow tests **research-tool logic**, not served CSP, real browser security or PWA product readiness.

**Local validation:** workflow YAML parsed successfully, and **14/14 structural assertions PASS** for trigger, permissions, immutable action refs, bounded job, pinned Node, no persisted checkout credentials/cache, fatal shell, expected commands, no deployment and no privileged trigger. This does not prove the GitHub Actions runner can download Node or execute the tests.

**Hosted execution remains OPEN at this checkpoint.** The connector returned empty commit statuses and its commit-workflow-run endpoint only reports PR-triggered runs; those observations cannot establish that a push-triggered job ran, passed, failed, or was disabled. Do not promote 36/36 or 26/26 to hosted PASS without a concrete run ID, job/step conclusion, exact SHA and output.

### Release-evidence admission and failure modes [DEPENDENCY / VALIDATION]

| Boundary | Required evidence | If missing |
| --- | --- | --- |
| Research source | exact commit SHA and collector/gate/test blob identities | UNKNOWN |
| Hosted synthetic suite | run ID, runner/Node identity, `node --test` exit status and full 36-case outcome | NOT EXECUTED / HOLD |
| Hosted 517 gate | same run ID, `--self-test` exit status, 26 expected outcomes | NOT EXECUTED / HOLD |
| Artifact-to-HTTPS | independently approved NORMAL archive and expected body hashes; real TLS response with egress provenance | OPEN |
| Browser enforcement | Chromium + Safari positive and deliberately blocked CSP script tests, Auth aliases and Worker/offline behavior | OPEN |
| Ledger and managed EFB | 37-store external file round trip, same-profile restart, Home Screen and managed-iPad policy envelope | OPEN |

**Track allocation:** E owns execution authority/egress and forbids promotion from green unit tests; C owns exact-run failure propagation and negative controls; A owns Node/HTTP/Worker/browser transfer; B owns truthful accessible offline/auth/recovery messages; D owns no premature acquisition/security/advertising claims. This adds executable proof infrastructure without duplicating Engineering Q006 or Design Studio W121.

**CHANGE WATCH:** action release identity, Node 22 runtime and runner image changes, GitHub Actions enablement/event semantics, IANA address registries, CSP/WebKit/Hosting changes. **Stage 8 applied ACTIVE; Production validation OPEN; PWA release HOLD.** The adjacent valuable task was completed by adding the actual non-deploying CI path and reviewing its negative boundaries; further promotion requires hosted run evidence or an approved actual preview/device, not more synthetic documents.
