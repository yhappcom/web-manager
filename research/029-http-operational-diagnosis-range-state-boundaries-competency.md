# 029 — HTTP Operational Diagnosis, Range/State Boundaries & Competency Review

Status: **INTEGRATED HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED; ADVANCED REINTEGRATION DEFERRED TO LATER STAGES**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Purpose

This study closes the current HTTP learning cycle at the level required for Stage 1. It does **not** claim that every HTTP extension, browser quirk, CDN feature or security attack has been mastered. Instead, it tests whether the Web Manager now has a coherent model strong enough to explain and diagnose ordinary real-world HTTP behavior before moving to HTTPS/TLS.

This block integrates several remaining subjects that were deliberately not split into separate micro-studies:

- partial/range transfer;
- cookies and HTTP authentication only at the boundary level needed to understand HTTP state;
- standardized cache/proxy diagnostic metadata;
- browser network-monitor interpretation;
- operational failure scenarios;
- current protocol-registry awareness;
- final HTTP competency assessment.

The depth rule remains: future performance, security, privacy, browser-runtime and operations stages will revisit HTTP at higher levels rather than pretending this one Stage 1 checkpoint is permanent completion of the entire protocol family.

---

## 1. Range requests: a representation does not always need to be transferred in full

### SOURCE
RFC 9110 defines range requests and the `Range` request field. If a range is valid, supported and satisfiable for the selected representation, a server can respond with `206 Partial Content`. If the requested range is unsatisfiable, `416 Range Not Satisfiable` is appropriate.

`If-Range` allows a client to combine a range request with a validator so that a partial transfer is only used when the representation still matches the client's validator; otherwise the server sends the full selected representation.

### FOUNDATION
A normal GET asks for a representation. A range request asks for only part of that selected representation.

This exists because transferring a complete representation can be wasteful or unnecessary. Large media, resumable downloads and clients that need only a byte region benefit from partial transfer.

A simplified conceptual flow is:

`GET full representation → 200`

versus

`GET + Range → 206 + Content-Range`

when the range can be satisfied.

### Important distinctions

- `206` is successful partial transfer, not an error.
- `416` means the requested range cannot be satisfied; it is not equivalent to 404.
- `Range` is evaluated against the **selected representation**, so representation selection and validators still matter.
- Partial transfer is an HTTP semantic feature; it should not be confused with HTTP/2 or HTTP/3 framing into DATA frames.

### Web Manager relevance

For a future MintTap site, ordinary HTML pages may rarely require range logic, but large videos, downloadable manuals, app assets or support files might. The operational requirement is not to force range support everywhere; it is to recognize a 206/416 exchange correctly and avoid diagnosing it as truncated content merely because fewer bytes were transferred.

Primary source:
- RFC 9110 — HTTP Semantics, Sections 14 and 15.3.7 / 15.5.17: https://www.rfc-editor.org/rfc/rfc9110.html

---

## 2. HTTP is stateless, but cookies can layer application state over it

### SOURCE
RFC 6265 defines the `Set-Cookie` response field and `Cookie` request field. It explicitly describes cookies as a way for servers to maintain stateful sessions over the mostly stateless HTTP protocol.

As of 2026-09-14, RFC 6265 remains the published RFC, while `draft-ietf-httpbis-rfc6265bis-22` has been approved by the IESG and is in the RFC Editor publication queue. The draft must therefore be treated as **work in progress / publication-pending**, not silently substituted for the current published RFC.

### FOUNDATION
The important boundary model is:

1. HTTP itself does not require conversational server state between messages.
2. A server can send state metadata with `Set-Cookie`.
3. The user agent stores applicable cookie state according to cookie rules.
4. Later requests can include applicable cookie name/value pairs in `Cookie`.
5. The application can associate those values with server-side or client-relevant state.

Therefore:

`HTTP statelessness ≠ application has no state`

and

`cookie ≠ server-side session itself`

A cookie might contain a session identifier, a preference, or other application-defined state. The server decides what the value means.

### Security/privacy boundary

Cookie attributes such as `Secure` and `HttpOnly` change handling constraints, but their detailed threat model belongs in Stage 8 Security/Privacy. At this stage the required understanding is that cookies are browser-managed state carried through HTTP fields and can materially affect caching, personalization and cross-request behavior.

### CHANGE WATCH
The cookie specification is actively evolving. Current production decisions should re-check the finalized RFC that emerges from rfc6265bis rather than relying indefinitely on 2011-era RFC 6265 alone.

Sources:
- RFC 6265: https://www.rfc-editor.org/rfc/rfc6265.html
- IETF Datatracker, rfc6265bis status: https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/

---

## 3. HTTP authentication is also a semantic layer, not identical to login UI

### SOURCE
RFC 9110 defines HTTP authentication as a challenge/response framework. A `401 Unauthorized` response from an origin server includes `WWW-Authenticate` challenge information; a client can respond with `Authorization` credentials. Proxy authentication has parallel `407`, `Proxy-Authenticate`, and `Proxy-Authorization` semantics.

### FOUNDATION
This gives a second important boundary:

`HTTP authentication framework ≠ every website login system`

Many web applications use HTML forms, cookies, bearer tokens, federated identity or application-specific flows. They can still use HTTP, but not every login screen is an implementation of RFC 9110's challenge/response authentication mechanism.

Similarly:

- `401` has authentication-challenge semantics;
- `403` means the server understood the request but refuses it;
- a site should not choose between them merely based on which English label sounds better.

### Operational significance

If a browser or API client receives 401, inspect `WWW-Authenticate` and the authentication context. If it receives 403, do not automatically assume re-entering the same credentials will help.

Detailed OAuth/OIDC, token lifecycle, CSRF and session-security analysis belongs later in Stage 8.

Primary source:
- RFC 9110, Section 11 and status Sections 15.5.2–15.5.4: https://www.rfc-editor.org/rfc/rfc9110.html

---

## 4. Standardized cache diagnostics: `Cache-Status`

### SOURCE
RFC 9211 defines the `Cache-Status` response field so caches can explain how they handled a request using standardized syntax rather than only vendor-specific debugging headers.

It can communicate information such as:
- whether a cache satisfied the request (`hit`);
- why a request was forwarded (`fwd`);
- the next-hop status (`fwd-status`);
- remaining freshness lifetime (`ttl`);
- whether the response was stored (`stored`);
- whether requests were collapsed (`collapsed`);
- cache-key information (`key`) where exposed.

A response can contain multiple cache entries, representing a chain of caches.

### FOUNDATION
This reinforces the idea that “from cache” is not one binary state. A cache can:
- hit directly;
- forward because of miss/staleness/policy;
- validate;
- store or decline to store;
- participate as one cache in a multi-cache chain.

### Operational rule

When `Cache-Status` is present, treat it as useful protocol evidence. When it is absent, do **not** conclude that no cache exists: deployment of the field is optional.

Primary source:
- RFC 9211 — The Cache-Status HTTP Response Header Field: https://www.rfc-editor.org/rfc/rfc9211.html

---

## 5. Standardized intermediary diagnostics: `Proxy-Status`

### SOURCE
RFC 9209 defines `Proxy-Status` to convey how an intermediary handled a response, including errors. Registered error types include DNS resolution failures, connection refusal/termination, TLS errors, HTTP request errors, destination unavailability and other next-hop failures.

The current IANA Proxy-Status registry provides standardized parameters such as `error`, `next-hop`, `next-protocol` and `received-status`.

### FOUNDATION
This gives a concrete way to refine the earlier hop-aware model.

A browser seeing `502 Bad Gateway` knows an intermediary/gateway failed to obtain a valid upstream response, but `Proxy-Status` can provide more specific evidence about *why*—for example DNS failure, connection refusal or TLS certificate error on the intermediary→upstream hop.

### Operational rule

Do not infer that a user-facing `502` means the public TLS connection to the browser failed. The browser can have a completely valid HTTPS/HTTP exchange with the edge while the edge encounters a different failure on its next hop.

Primary sources:
- RFC 9209 — The Proxy-Status HTTP Response Header Field: https://www.rfc-editor.org/rfc/rfc9209.html
- IANA Proxy-Status registry: https://www.iana.org/assignments/http-proxy-status

---

## 6. Browser Network tools are evidence views, not the network itself

### SOURCE
Firefox's official Network Monitor documentation exposes request/response headers, cookies, cache data, timings, security details, request payloads and stack traces. The Timings view distinguishes phases such as DNS resolution, connection, sending, waiting and receiving. The Cache tab can show cached-resource metadata. The Security tab shows secure-connection details.

### SYNTHESIS
Browser Network tools should be treated as a **diagnostic interpretation layer**:

- excellent for browser-observed request/response semantics;
- excellent for correlating status, fields, initiator and timing;
- not identical to a raw packet capture;
- not proof of every upstream hop hidden behind a CDN/reverse proxy;
- capable of showing normalized/presented header information rather than literal HTTP/2/3 wire frames.

### Evidence hierarchy for ordinary Web Manager diagnosis

A useful escalation model is:

1. **Network panel** — what did this browser request and observe?
2. **response fields/status** — what semantic outcome and metadata were returned?
3. **cache/proxy diagnostic fields** — did an intermediary explain its handling?
4. **server/CDN logs** — what did the edge/origin observe?
5. **packet/protocol-level evidence** — only when exact wire/framing/transport behavior matters.

This prevents two opposite errors: treating DevTools as infallible packet truth, or ignoring it and jumping prematurely into low-level tracing.

Implementation reference:
- Firefox Network Monitor request details: https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/request_details/

---

## 7. A practical diagnostic matrix

The following scenarios test whether HTTP knowledge transfers into operational reasoning.

### Scenario A — Beautiful branded “not found” page returns 200

Observed:
- user sees “Page not found”;
- HTTP status = 200.

Diagnosis:
- content and HTTP semantics disagree;
- this is not fixed merely by improving the visual error page;
- status should reflect the actual resource outcome (normally 404, or 410 when intentionally gone and known permanent).

Cross-domain consequences:
- monitoring can misclassify failures as success;
- crawlers can receive misleading semantics;
- analytics can overcount successful content delivery.

### Scenario B — Browser gets 304 and shows full page

Observed:
- network response status = 304;
- browser still renders full content.

Diagnosis:
- 304 does not carry a normal new representation body;
- the browser/cache reuses a previously stored representation after successful validation.

Do not call this a redirect.

### Scenario C — Same URL returns Korean to one client and English to another

Possible evidence:
- `Accept-Language` differs;
- server performs proactive negotiation;
- response `Vary: Accept-Language` is present.

Diagnosis:
- one resource identifier may yield multiple selected representations;
- cache correctness requires variation to be reflected in matching;
- SEO/UX/localization architecture still needs separate evidence before deciding whether header negotiation is the right public-site design.

### Scenario D — Browser-facing protocol is HTTP/3; origin logs HTTP/1.1

Diagnosis:
- no contradiction is required;
- an edge/CDN can terminate HTTP/3 and make a separate HTTP/1.1 upstream connection;
- diagnose per hop rather than assigning one protocol version to “the site.”

### Scenario E — 502 plus `Proxy-Status` indicates DNS error

Diagnosis:
- public DNS for the user-facing hostname may be working perfectly;
- an intermediary failed resolving a **next-hop** hostname;
- this is an upstream/intermediary DNS problem, not automatically the same DNS layer the browser used.

### Scenario F — 503 with `Retry-After`

Diagnosis:
- service is temporarily unavailable and is communicating a suggested retry delay;
- repeated immediate retry can worsen overload;
- compare with 429, which specifically communicates excessive request rate from the client/requesting party under its specification.

### Scenario G — media download returns 206

Diagnosis:
- do not assume corruption/truncation;
- inspect `Range` request and `Content-Range` response semantics;
- 206 can be the intended successful result.

### Scenario H — login page returns 403

Diagnosis:
- 403 means refusal, not “please authenticate” by definition;
- if the server is using HTTP authentication and needs credentials, 401 plus `WWW-Authenticate` has specific semantics;
- application login UX may use a different model, so inspect actual authentication architecture rather than mapping status solely to screen wording.

---

## 8. Status-code and method registries are living protocol infrastructure

### SOURCE
IANA maintains authoritative HTTP method, status and field registries referenced by the IETF specifications.

The method registry was updated on 2026-06-17 and now includes `QUERY`, standardized by RFC 10008. `QUERY` is registered as safe and idempotent.

### Why this matters

A foundational course often teaches only GET/HEAD/POST/PUT/DELETE/PATCH/OPTIONS. That is useful but should not produce the false belief that the method set is permanently closed.

HTTP is extensible. The authoritative registry, not a memorized tutorial list, is the correct source when encountering an unfamiliar method.

### CHANGE WATCH
Protocol expertise requires knowing which knowledge is durable and which requires registry/specification lookup. New standardized methods, fields and status codes can appear without creating a new HTTP major version.

Sources:
- IANA HTTP Method Registry: https://www.iana.org/assignments/http-methods
- RFC 10008 — The HTTP QUERY Method: https://www.rfc-editor.org/rfc/rfc10008.html
- IANA HTTP Field Name Registry: https://www.iana.org/assignments/http-fields

---

## 9. Failure-layer reasoning after the HTTP studies

The Web Manager should now diagnose an ordinary public-web failure through the following chain:

`URL/resource intent`
→ `DNS resolution`
→ `transport/TLS establishment` (next dedicated topic)
→ `HTTP request method + target + fields`
→ `intermediary/cache path`
→ `response status + fields`
→ `selected representation/content`
→ `browser parsing/runtime/rendering`
→ `user-visible interaction`

Each arrow is a boundary where a different class of failure can occur.

A correct diagnosis avoids category errors such as:
- blaming DNS for a 504 generated by a gateway after successful client connection;
- blaming JavaScript for a stale shared-cache response before the new JS ever arrives;
- blaming HTTP because the returned HTML is semantically inaccessible despite transport success;
- blaming the origin when an edge cache is serving the response without contacting it;
- assuming the browser's h3 connection means the origin hop is h3.

---

## 10. HTTP competency review

### A. First-principles explanation — PASS

Can explain:
- why HTTP emerged with the Web;
- why raw document retrieval evolved into structured message semantics;
- why resource and representation are different;
- why methods and statuses form machine-readable semantic contracts;
- why caching and intermediaries became architectural rather than optional curiosities.

### B. Vocabulary and layer separation — PASS

Can distinguish:
- resource vs representation;
- status vs UI message;
- content type vs content coding vs transfer framing vs header compression;
- safe vs idempotent vs cacheable;
- freshness vs validation;
- private vs shared cache;
- browser→edge vs edge→origin protocol hop;
- HTTP semantics vs HTTP/1.1/2/3 wire expression;
- HTTP statelessness vs application session state.

### C. Representative diagnosis — PASS at Stage 1 scope

Can reason about:
- soft-404/200 mismatch;
- redirect method behavior;
- 304 validation/reuse;
- cache hit/miss/validation distinctions;
- 502/503/504 intermediary outcomes;
- negotiated variants and `Vary`;
- 206 partial responses;
- authentication-status boundaries;
- proxy/cache diagnostic metadata.

### D. Alternative comparison — PASS at Stage 1 scope

Can compare:
- 301/302/303/307/308 based on permanence and method handling;
- 404 vs 410;
- 401 vs 403;
- 429 vs 503;
- fresh caching vs validation;
- explicit locale URL architecture vs request-header negotiation as an HTTP-related trade-off without claiming HTTP alone decides the architecture;
- HTTP/1.1 vs HTTP/2 vs HTTP/3 at semantic/framing/transport level.

### E. Specialist/unknown boundaries — PASS

Recognizes that Stage 1 HTTP competence does **not** replace later specialist study of:
- TLS/certificates;
- CORS/same-origin browser security;
- cookie security/privacy and SameSite details;
- OAuth/OIDC/session security;
- CDN vendor-specific cache controls;
- performance measurement and congestion behavior;
- search-engine-specific redirect/indexing behavior;
- accessibility of actual document structure;
- offensive HTTP request-smuggling exploitation.

### F. MintTap application — PASS at principle level

Can define future requirements without inventing current production facts:
- correct status semantics;
- deliberate redirects;
- resource-class cache policy;
- validators where useful;
- correct variation for negotiated content;
- hop-aware CDN diagnosis;
- protocol-version-aware performance analysis;
- evidence collection from browser/network/edge/origin layers.

### G. Evidence quality — PASS

Primary authority now includes:
- RFC 9110 — semantics;
- RFC 9111 — caching;
- RFC 9112 — HTTP/1.1;
- RFC 9113 — HTTP/2;
- RFC 9114 — HTTP/3;
- RFC 9000 — QUIC transport;
- RFC 9204 — QPACK;
- RFC 9205 — building applications with HTTP;
- RFC 9209 — Proxy-Status;
- RFC 9211 — Cache-Status;
- RFC 6265 plus publication-state tracking for rfc6265bis;
- IANA HTTP registries;
- WHATWG Fetch for browser fetch/redirect/cache processing where browser-platform behavior matters;
- browser-vendor DevTools documentation as implementation evidence, not protocol authority.

---

## 11. Stage decision

### SYNTHESIS
The HTTP subject is now sufficiently integrated to close the **Stage 1 HTTP core** and move to HTTPS/TLS.

This decision does **not** mean HTTP is finished forever. Later curriculum stages will reopen it at higher depth:

- Stage 6 — redirect/crawl/canonical/discovery effects;
- Stage 7 — caching, compression, prioritization, connection reuse and performance measurement;
- Stage 8 — cookies, authentication, origin policy, request smuggling, security headers and privacy;
- Stage 9 — measurement/instrumentation semantics;
- Stage 11 — CDN, proxy, deployment and operations.

The correct model is **spiral learning**: establish a sound core now, then revisit with stronger adjacent knowledge.

---

## 12. MintTap operating rules retained from the HTTP domain

### MINTTAP DIRECTION
For future `minttap.app` work:

1. Treat HTTP semantics as part of product quality, not backend trivia.
2. Return machine-correct statuses even when branded error UI is polished.
3. Choose redirect codes by permanence **and** intended method behavior.
4. Define cache policy by resource class; never apply one universal cache recipe blindly.
5. Treat `no-cache`, `no-store`, validators and freshness as distinct tools.
6. Ensure negotiated variants and shared caches cannot mix incompatible representations.
7. Diagnose CDN/proxy paths per hop.
8. Treat HTTP/2/3 as transport/expression changes around shared semantics, not as different application models.
9. Use browser Network evidence first for user-observed behavior, then escalate to cache/proxy/server/protocol evidence as needed.
10. Re-check IANA registries and living/browser standards when an unfamiliar HTTP element appears.

### OPEN
Current real `minttap.app` facts remain unverified in this curriculum block:
- actual browser-facing HTTP version distribution;
- CDN/reverse-proxy topology;
- origin protocol version;
- cache-control/validator strategy;
- redirect inventory;
- cookie/auth use;
- range support;
- `Cache-Status` / `Proxy-Status` exposure.

These should be inspected only when a live-site project or operational audit calls for them.

### DESIGN STUDIO DEPENDENCY
No Design Studio handoff is required from this block. The work is protocol/operations foundation. Later browser performance, responsive loading, error-state UX and web-design implementation studies should cross-reference the Web Design specialist when visual/interaction decisions become material.

---

## Source set

Current/primary:
- RFC 9110 — HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.html
- RFC 9111 — HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111.html
- RFC 9112 — HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112.html
- RFC 9113 — HTTP/2: https://www.rfc-editor.org/rfc/rfc9113.html
- RFC 9114 — HTTP/3: https://www.rfc-editor.org/rfc/rfc9114.html
- RFC 9000 — QUIC: https://www.rfc-editor.org/rfc/rfc9000.html
- RFC 9204 — QPACK: https://www.rfc-editor.org/rfc/rfc9204.html
- RFC 9205 — Building Protocols with HTTP: https://www.rfc-editor.org/rfc/rfc9205.html
- RFC 9209 — Proxy-Status: https://www.rfc-editor.org/rfc/rfc9209.html
- RFC 9211 — Cache-Status: https://www.rfc-editor.org/rfc/rfc9211.html
- RFC 6265 — HTTP State Management Mechanism: https://www.rfc-editor.org/rfc/rfc6265.html
- IETF Datatracker — rfc6265bis: https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/
- IANA HTTP Method Registry: https://www.iana.org/assignments/http-methods
- IANA HTTP Field Name Registry: https://www.iana.org/assignments/http-fields
- IANA Proxy-Status Registry: https://www.iana.org/assignments/http-proxy-status
- RFC 10008 — The HTTP QUERY Method: https://www.rfc-editor.org/rfc/rfc10008.html
- WHATWG Fetch Living Standard: https://fetch.spec.whatwg.org/

Implementation-oriented secondary evidence:
- Firefox Network Monitor request details: https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/request_details/

## Evidence classification

- `SOURCE`: standards, registries and browser-vendor documentation explicitly cited above.
- `SYNTHESIS`: diagnostic hierarchy, scenario reasoning, and decision that Stage 1 HTTP competency is sufficient to advance.
- `MINTTAP DIRECTION`: protocol-semantic operating rules for future MintTap web work.
- `OPEN`: current live `minttap.app` HTTP/CDN/cache/auth topology is not inferred.
- `DEPENDENCY`: no current Design Studio dependency.
- `VALIDATION`: live-site headers/network traces are required when evaluating a real deployment.
- `CHANGE WATCH`: cookie-standard publication, IANA method/field/status registries, WHATWG Fetch behavior, and browser tooling behavior can evolve.