# 029 — HTTP Deep Study: Semantics, Representations, Caching, Intermediaries & Protocol Evolution

Status: **INTEGRATED DEEP-STUDY CHECKPOINT — HTTP DOMAIN REMAINS ACTIVE FOR OPERATIONAL VALIDATION**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Purpose

This document changes the working cadence from many tiny sub-files to one meaningful professional learning unit. It integrates the prior HTTP history/message work with deeper study of methods, status semantics, representations, negotiation, caching, intermediaries, and HTTP/2–HTTP/3 mechanics.

The goal is not to memorize headers or status-code tables. The goal is to understand HTTP as a semantic contract that remains relatively stable while its wire expression, transport, caching topology and intermediary behavior evolve.

## 1. Durable HTTP mental model

Current HTTP architecture is best understood as layers:

1. **resource identity / target** — what resource or action target is addressed;
2. **request semantics** — method plus fields describing what the client intends;
3. **response semantics** — status plus fields describing the result;
4. **representation** — selected information representing resource state;
5. **caching/validation** — rules for storing, matching, reusing and validating prior responses;
6. **intermediaries** — caches, proxies, gateways and CDNs that may participate between user agent and origin;
7. **version-specific expression** — HTTP/1.1 textual messages, HTTP/2 frames/streams, HTTP/3 frames over QUIC streams;
8. **transport/security substrate** — TCP for HTTP/1.1 and HTTP/2 in normal deployment, QUIC for HTTP/3; TLS is studied separately next.

The central professional rule is: do not infer one layer from another without evidence.

## 2. Methods are semantic contracts

RFC 9110 defines the method token as the primary source of request semantics. Methods are not arbitrary route labels.

Important relationships:
- GET requests transfer of a current selected representation;
- HEAD is GET-like without transferring response content;
- POST asks the target resource to process enclosed content according to that resource's semantics;
- PUT requests creation/replacement of target resource state with supplied representation semantics;
- DELETE requests removal of the association between target URI and current functionality;
- OPTIONS requests communication options;
- CONNECT establishes a tunnel in applicable contexts.

Safe, idempotent and cacheable remain independent properties. Safe semantics permit automated retrieval systems to assume the client did not request destructive state change. Idempotence supports reasoning about retries after uncertain failures, but does not promise identical response bytes.

Operational implication: designing a destructive action behind GET is not merely stylistically poor; it breaks assumptions used by crawlers, prefetchers, link checkers and other automated agents.

## 3. Status codes describe protocol outcomes, not UI language

RFC 9110 defines status classes and individual meanings. A Web Manager must reason about the semantic boundary rather than treating all errors as interchangeable.

Representative distinctions:
- 200: request succeeded; meaning of content depends on method;
- 201: request succeeded and created one or more resources;
- 202: accepted for processing, not proof that processing completed;
- 204: successfully fulfilled with no additional response content;
- 301/308: permanent relocation semantics, but 308 unambiguously preserves method on automatic redirect;
- 302/307: temporary relocation semantics, but 307 unambiguously preserves method;
- 303: directs retrieval of another resource as an indirect response, commonly converting a POST result flow into GET retrieval;
- 304: conditional GET/HEAD indicates a stored representation can be reused; it is not an ordinary redirect to a new URL;
- 401: authentication credentials are required/failed in the HTTP authentication model;
- 403: server understood request but refuses fulfillment;
- 404: target resource not found or server unwilling to disclose existence;
- 410: resource is known to be no longer available and condition is likely permanent;
- 409: request conflicts with current resource state;
- 422: content syntax/media type may be understood but instructions cannot be processed;
- 429: rate limiting is defined outside RFC 9110 but represents too many requests;
- 500: unexpected server condition;
- 502: gateway/proxy received invalid response from inbound server;
- 503: service currently unable to handle request, often temporary;
- 504: gateway/proxy did not receive timely upstream response.

This matters to monitoring, SEO, API behavior and user support. A polished error document with 200 status creates semantic disagreement between human-visible content and machine-visible outcome.

## 4. Redirect history explains today's confusing status family

RFC 9110 records the historical divergence around 301 and 302: early implementations disagreed about whether a redirected POST should remain POST or become GET. Prevailing browser practice converged on method change in common cases. 303 was defined for an explicit indirect GET-style result; 307 and later 308 provide unambiguous method-preserving temporary/permanent redirects.

Historical lesson: protocol oddities often represent compatibility compromises, not arbitrary bad design.

Web Manager judgment:
- choose redirect status based on permanence **and** desired method behavior;
- do not reduce redirect design to “301 permanent, 302 temporary”;
- URL migrations, form submission flows and API redirects require different semantic reasoning.

## 5. Resource and representation are not identical

A resource is the conceptual target identified by a URI. A representation is information intended to reflect a past, current or desired state of that resource.

One resource can have multiple representations, e.g. language, media type or content coding variants. This explains why a URL alone does not always determine the exact bytes returned.

`Content-Type` identifies the media type of the selected representation before content coding. `Content-Encoding` describes codings applied to that representation, commonly compression. They answer different questions.

This reinforces the earlier resource/representation distinction from Study 027.

## 6. Content negotiation is representation selection

RFC 9110 defines proactive/server-driven and reactive negotiation concepts. Clients can express preferences through fields such as Accept, Accept-Encoding and Accept-Language. The server selects a representation according to available variants and its algorithm.

The standard does not prescribe one universal server selection algorithm.

`Vary` is critical when request fields influence representation selection: it tells caches which request fields must participate in matching a stored response.

Consequences:
- content negotiation affects caching;
- very broad variation can reduce cache efficiency;
- preference fields can expose information useful for fingerprinting/privacy analysis;
- explicit locale URLs can simplify discoverability, analytics and cache identity for public localized sites, although HTTP does not require this architecture.

For MintTap, locale architecture should later be decided jointly from SEO, UX, localization and caching evidence rather than from HTTP alone.

## 7. Compression is negotiation plus representation metadata

A browser can advertise supported codings through `Accept-Encoding`; a server can select one and indicate it through `Content-Encoding`. If selected encoding varies by request capability, cache matching needs the corresponding `Vary` dimension.

Do not confuse:
- media type (`Content-Type`);
- content coding/compression (`Content-Encoding`);
- HTTP/1.1 transfer framing (`Transfer-Encoding`);
- HTTP/2 HPACK / HTTP/3 QPACK field compression.

These are four different mechanisms at different layers.

## 8. HTTP caching is a decision system, not a browser “file cache”

RFC 9111 defines caching around stored responses and rules controlling storage/reuse.

A useful state model is:

`storeability → cache key/matching → freshness → stale policy → validation → reuse/replacement`

A cache must first determine whether a response may be stored. On a later request it determines whether a stored response matches. If fresh, it can often reuse it without contacting the origin. If stale, it generally needs validation unless rules permit stale reuse.

Private caches are associated with a user agent; shared caches can serve multiple users, including CDN/proxy caches.

This is separate from DNS caching: DNS reuses naming answers; HTTP caching reuses HTTP responses.

## 9. Freshness and validation solve different problems

Freshness asks whether a stored response is young enough to reuse without checking the origin. Validation asks whether a stored response still corresponds to the current selected representation.

Validators include:
- `ETag` / entity tags;
- `Last-Modified` timestamps.

Conditional request fields include:
- `If-None-Match`;
- `If-Modified-Since`;
- and other precondition fields for state-sensitive operations.

A successful conditional GET/HEAD can produce 304 Not Modified, allowing reuse of stored content while refreshing relevant metadata rather than retransferring the representation.

Professional implication: “served from cache” is not one behavior. A response can be fresh-reused, validated-and-reused, served stale under permitted rules, or replaced.

## 10. Cache-Control names must be learned semantically

`no-cache` does not mean “never store.” It requires successful validation before reuse under its semantics.

`no-store` is the directive intended to prevent storage under the specified rules.

`max-age` provides freshness lifetime. Shared-cache-specific controls such as `s-maxage` can distinguish shared-cache policy from ordinary cache policy.

The naming is historically unintuitive, so operational diagnosis must use standards semantics rather than English intuition.

## 11. Vary is part of cache correctness

RFC 9111 requires caches to account for request fields named by `Vary` when selecting stored responses.

Example conceptual case:
- same URL;
- client A advertises Brotli;
- client B does not;
- server selects different encoded representations.

If cache identity ignores `Accept-Encoding`, the wrong representation could be reused. Correct variation metadata connects negotiation to cache safety.

This same principle applies to other dimensions such as language where header-based negotiation is used.

## 12. Intermediaries make HTTP a path, not merely two endpoints

HTTP supports proxies, gateways, caches and CDNs. An intermediary can terminate one HTTP connection and create another upstream. Consequently:

`browser → edge` and `edge → origin`

can use different HTTP versions and have different connection behavior.

A 502/504 often points directly to an intermediary/upstream relationship rather than to browser rendering. Conversely, a response observed at the browser does not prove the origin application emitted every field unchanged.

Operational diagnosis therefore needs hop-aware evidence.

## 13. HTTP/1.1: persistent connections solved one problem and exposed others

HTTP/1.1 made connection reuse central, reducing repeated connection setup. But one byte-stream connection still requires correct message delimitation and does not provide HTTP/2-style independent multiplexed streams.

Historically, clients opened multiple connections to gain parallelism. Pipelining existed but suffered deployment/practical limitations and did not become the general browser solution that multiplexing later became.

The framing rules studied in 029A become security-critical because intermediaries must agree about where each message ends.

## 14. HTTP/2: multiplex HTTP exchanges over streams

RFC 9113 defines streams as independent bidirectional sequences of frames inside one HTTP/2 connection. Multiple streams can be concurrently open and frames interleaved. HEADERS and DATA frames carry core request/response material; fields are compressed.

This changes the concurrency model substantially compared with HTTP/1.1.

However, HTTP/2 commonly runs over one TCP connection. TCP provides one ordered byte stream. Packet loss requiring TCP recovery can therefore delay progress visible across multiple HTTP/2 streams even though HTTP/2's application framing separates them.

This is the transport-level head-of-line issue that motivated part of HTTP/3's design.

## 15. HTTP/3: QUIC moves stream independence into the transport

RFC 9114 maps HTTP semantics over QUIC. QUIC provides multiple streams with per-stream flow control and reliability properties. Loss affecting one stream need not prevent unrelated streams from progressing merely because transport bytes from another stream are missing.

HTTP/3 therefore should not be described as “HTTP/2 but UDP.” QUIC supplies transport functionality including reliable streams, congestion control and integrated cryptographic handshake properties; HTTP/3 maps HTTP onto that transport.

The durable semantics—methods, statuses, fields, representations—remain recognizable.

## 16. Why QPACK exists instead of simply reusing HPACK

HTTP/2 uses HPACK field compression. HPACK relies on ordering properties compatible with its HTTP/2/TCP environment. QUIC deliberately permits independent streams to progress without total cross-stream ordering.

RFC 9204 explains that reusing HPACK directly would introduce field-section head-of-line blocking. QPACK restructures dynamic table communication with dedicated streams and explicit blocking controls to fit QUIC's transport model.

This is a strong example of cross-layer design: changing transport assumptions can force redesign of an apparently unrelated compression mechanism.

## 17. Performance rules are protocol-generation dependent

Old HTTP/1-era optimization folklore cannot be applied mechanically to HTTP/2/3.

Examples:
- combining every asset into one giant bundle reduced request overhead in older connection models but can hurt caching granularity and loading priorities today;
- excessive domain sharding could increase parallelism under HTTP/1 constraints but can create extra connection/DNS/TLS costs and reduce modern connection reuse;
- request count still matters, but its cost model changes with multiplexing and caching.

Therefore Web Manager optimization should begin from measured network behavior, protocol generation and resource dependency—not inherited folklore.

## 18. HTTP is deliberately extensible

RFC 9110's method, status and field mechanisms allow extensions, while clients/intermediaries need rules for unknown values. RFC 9205 emphasizes using HTTP's existing semantics—links, caching, negotiation, authentication, intermediaries—rather than tunneling an unrelated protocol through superficially HTTP-shaped messages.

Professional implication: APIs and web services should benefit from HTTP semantics rather than treating POST + 200 as a universal envelope for every operation/outcome.

## 19. Cross-domain connections

### SEO
Redirect permanence, 404/410 semantics, cache correctness and representation identity affect crawler interpretation.

### UX
HTTP status is not user copy, but correct semantics supports reliable error handling, navigation and form workflows.

### Accessibility
HTTP cannot make inaccessible HTML accessible, but correct media type, language architecture, redirects and error semantics help user agents receive the intended resource/representation. Accessibility itself remains a document/UI concern studied separately.

### Security
Method semantics, parser consistency, cache variation, authorization metadata and intermediary boundaries affect attack surface. Dedicated security study will go deeper later.

### Privacy
Negotiation headers, personalized caching and shared-cache variation can expose or mix user-specific information if designed incorrectly.

### Performance
Fresh caching, validation, compression, multiplexing and connection reuse can reduce latency/bandwidth; incorrect optimization can negate those benefits.

### Operations
502/504, cache age/validators, protocol version and intermediary headers can identify failure layers more accurately than visible page symptoms alone.

## 20. Failure-diagnosis model

For a future MintTap HTTP problem, diagnose in this order rather than jumping to application code:

1. What URL/resource was targeted?
2. What method and request semantics were used?
3. Which HTTP version is used on the browser-facing hop?
4. Which intermediary/CDN/proxy participates?
5. What status was returned, and by which likely participant?
6. Which fields alter redirect, representation, cache or security behavior?
7. Was the response selected from a cache? Fresh or validated?
8. Did representation negotiation change the returned bytes?
9. Is the visible content consistent with status semantics?
10. Is the problem browser/runtime-level after a semantically valid response, or earlier in HTTP?

This prevents category errors such as treating a stale CDN response as a JavaScript bug or treating a 504 as a DNS failure.

## 21. Common misconceptions now rejected

- HTTP is not synonymous with TCP.
- HTTP/3 is not unreliable merely because QUIC uses UDP as its substrate.
- HTTP/2 and HTTP/3 do not redefine GET/404 semantics from scratch.
- 301/302 are not fully described by “permanent/temporary”; method behavior has historical nuance.
- 304 is not a normal URL redirect.
- 401 does not simply mean “not allowed”; authentication semantics matter.
- 404 does not prove a resource never existed.
- 200 does not prove the page is semantically the intended content.
- one URL can have multiple representations.
- Content-Type, Content-Encoding, Transfer-Encoding and HPACK/QPACK compression are different concepts.
- no-cache does not mean no-store.
- cache reuse does not imply the origin was contacted.
- browser-facing HTTP/3 does not prove the origin hop uses HTTP/3.
- fewer requests is not universally equivalent to faster modern Web performance.

## 22. MintTap judgment established so far

For future `minttap.app` work, Web Manager should require:

- resource URLs with durable meaning rather than provider internals;
- correct HTTP status semantics for real success/error/redirect outcomes;
- deliberate redirect choices based on permanence and method behavior;
- explicit caching strategy by resource class rather than one global header recipe;
- validators for mutable public resources where useful;
- cache-busting/fingerprinted immutable asset strategy to be evaluated in the performance/deployment stage;
- explicit handling of localization/representation variation;
- compression configured with cache variation correctness;
- hop-aware diagnosis when CDN/reverse proxy infrastructure exists;
- protocol-generation-aware performance decisions;
- no production assumptions about current `minttap.app` topology until verified.

These are architectural principles, not a claim about the current live domain.

## 23. Competency checkpoint

The HTTP domain is approaching integrated foundation/practitioner competence when Web Manager can explain without rote lookup:

1. why HTTP methods are semantic contracts;
2. safe vs idempotent vs cacheable;
3. why redirect codes evolved and how method preservation differs;
4. resource vs representation;
5. Content-Type vs Content-Encoding vs transfer framing;
6. how negotiation and Vary interact;
7. cache store/match/freshness/validation/reuse lifecycle;
8. ETag/Last-Modified and 304 logic;
9. private vs shared cache;
10. proxy/gateway/CDN role in a request path;
11. HTTP/1.1 persistence/framing constraints;
12. HTTP/2 stream multiplexing and TCP limitation;
13. HTTP/3/QUIC stream model;
14. why QPACK differs from HPACK;
15. why optimization advice changes across protocol generations;
16. how to separate HTTP evidence from DNS, TLS, application and browser-runtime evidence.

## 24. Remaining work before HTTP is closed

Do not create a long sequence of micro-files. The remaining HTTP work should be integrated into this domain checkpoint:

- inspect representative real HTTP exchanges and browser/network evidence;
- practice redirect/cache/representation/intermediary diagnosis;
- study range requests and resumable/partial transfer at appropriate depth;
- examine cookie/auth interaction only enough to establish HTTP boundaries, leaving security/privacy depth for later stages;
- perform an integrated competency review;
- then consolidate 029/029A/this document if useful rather than preserving unnecessary fragmentation.

## Sources

Primary/current:
- IETF RFC 9110 — HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.html
- IETF RFC 9111 — HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111.html
- IETF RFC 9112 — HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112.html
- IETF RFC 9113 — HTTP/2: https://www.rfc-editor.org/rfc/rfc9113.html
- IETF RFC 9114 — HTTP/3: https://www.rfc-editor.org/rfc/rfc9114.html
- IETF RFC 9204 — QPACK: Field Compression for HTTP/3: https://www.rfc-editor.org/rfc/rfc9204.html
- IETF RFC 9205 / BCP 56 — Building Protocols with HTTP: https://www.rfc-editor.org/rfc/rfc9205.html

Implementation-oriented supplementary reference:
- MDN Web Docs — HTTP Content Negotiation and HTTP header references.

Historical background remains in `029-http-foundations-history-semantics-evolution.md`.

## Evidence classification

- `SOURCE`: protocol semantics/mechanics established by cited IETF standards.
- `SYNTHESIS`: layered mental model, cross-domain connections, optimization implications and diagnostic workflow.
- `MINTTAP DECISION`: future web work must preserve semantic correctness, deliberate caching/redirect/representation policies and hop-aware diagnosis.
- `OPEN`: actual MintTap HTTP/CDN/origin configuration and real network traces.
- `DEPENDENCY`: Design Studio not required for this protocol block; later UX/performance integration will consume its evidence.
- `VALIDATION`: representative network-trace interpretation remains before HTTP domain closure.
- `CHANGE WATCH`: browser deployment behavior, protocol adoption and implementation-specific DevTools behavior.