# 518 — Stage 8 PWA Approved HTTPS Capture, Release Verdict Propagation and Browser Admission

Date: **2026-10-25 (Asia/Seoul)**  
State: **SOURCE + PRIMARY STANDARD + CROSS-TRACK SYNTHESIS + EXECUTABLE SYNTHETIC CAPTURE 30/30; LIVE HTTPS / BROWSER / MANAGED-IPAD / PRODUCT VALIDATION OPEN**  
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

It performs sequential **GET** requests against an exact HTTPS origin; no credentials, cookies, query strings, POSTs, automatic redirect following or body retention. DNS lookup rejects private/reserved destinations, certificate verification stays enabled, body hashing is streamed and size-bounded (32 MiB per route), selected raw header instances are retained, and Set-Cookie/Location are excluded from output. Encoded bodies are rejected. The CLI runs 517's semantic gate and writes with exclusive creation (mode 0600) **only after** SERVED_HEADER_CONSISTENT_UNVERIFIED; failures exit nonzero with fixed diagnostic codes. A capture remains **unattested** even if consistent. This collector is a research handoff, not a production CI deployment change.

**Local synthetic test evidence:** Node v22.16.0; running the test file with node --test yielded **30/30 PASS** on injected transport responses. Positive fixture checks three-route capture and header redaction; negative cases include origin/URL/route/hash/policy/schema, redirects, oversized responses, invalid headers, compressed body, DNS address classification and failure-message redaction. **No real HTTPS endpoint was contacted and the combined CLI→517 gate has not been executed against a real capture.**

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
| **C** | Synthetic 509–517 oracles mature; exact hosted and browser PASS missing | Owns 30 falsifications, negative controls, CI exit propagation and provenance transfer. |
| **B** | Static Design Studio content saturated before runtime | Consumes W120/CD127 for visible↔accessible↔actual auth/offline/recovery parity. |
| **D** | Marketing D8/D10 release/ads evidence HOLD | No action-code telemetry, no web ad rollout or verified-security/offline marketing claim. |

Read-only canonical transfers: Design Studio progress/WEB_STATUS.md, research/web/120-cross-concept-executable-stress-packet.md and research/content/127-pre-runtime-saturation-and-semantic-evidence-stop-rule.md; Software Engineering Studio progress/QUALITY_STATUS.md Q006 verdict semantics; Marketing Manager STATUS.md D8/D10. These disciplines are not duplicated. No LogMate/Design/Engineering/Marketing files changed.

## 5. Limits, evidence blockers and next meaningful boundary [OPEN / CHANGE WATCH]

- **OPEN:** independently approved preview origin, real NORMAL archive and body-hash plan, actual TLS response, unaltered capture custody, verified DNS/HTTP negative cases on real network, deployed CSP and Firebase Auth, Chromium/WebKit enforced-policy negative tests, old/new Worker session, 37-store external restore and managed iPad/MDM.
- **CHANGE WATCH:** Firebase pre-rewrite header matching and reserved namespaces, Node HTTPS/header handling, W3C CSP and browser enforcement, WebKit Home Screen behavior, storage quota/eviction, CI action version/verdict propagation and Flutter/Firebase module graph.
- **CONTRADICTION:** a 200 status + expected header strings cannot certify actual script blocking; a syntactically valid capture cannot certify approved deployment; a browser-only PASS cannot certify managed-EFB data durability. Reject all such promotions.
- **Adjacent-value checkpoint:** the 517 evidence-oracle gap was closed to the **synthetic read-only collector** layer and stress-tested with 30 cases. Next material work requires approved HTTPS host and independently pinned NORMAL bytes; additional ungrounded synthetic variants have lower information gain. **Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD.**
