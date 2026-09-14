# 029 — HTTP Foundations: Why HTTP Exists, Semantic Model & Protocol Evolution

Status: **FOUNDATION LAYER — DEEP STUDY, NOT TOPIC-COMPLETE**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Why this block is deliberately larger

The earlier curriculum risked treating HTTP as a glossary of GET/POST, status codes and headers. That is insufficient for professional Web Manager judgment.

HTTP will therefore be studied as a multi-block domain. This first block asks:

1. What problem did HTTP originally solve?
2. Which ideas survived from the early Web into modern HTTP?
3. Which limitations drove HTTP/1.0, HTTP/1.1, HTTP/2 and HTTP/3?
4. What is HTTP semantics, and why must semantics be separated from wire format and transport?
5. Why do safe, idempotent and cacheable semantics matter operationally?
6. How did intermediaries, caching and connection costs shape the protocol?

This file does **not** close HTTP. Later 029 sub-blocks must cover messages/fields, methods/statuses, representations/content negotiation, conditional requests/caching, intermediaries, transport/version mechanics, browser diagnostics and failure analysis.

---

## 1. Historical problem: a distributed hypertext system needed a transfer protocol

### SOURCE
W3C records that Tim Berners-Lee invented the World Wide Web at CERN in 1989, wrote the first Web server (`httpd`) and first browser/editor (`WorldWideWeb`) in 1990, and developed the initial URI, HTTP and HTML specifications as parts of the emerging Web architecture.

RFC 1945 states that HTTP had been used by the World-Wide Web initiative since 1990.

### SYNTHESIS
HTTP should be understood together with the original Web architecture:

- identifiers answer **what target/resource is being referred to?**;
- HTTP answers **how does a user agent interact with that target using standardized request/response semantics?**;
- HTML initially supplied a major hypertext representation format.

This separation is architecturally important. HTTP is not HTML transport only. Modern HTTP transfers JSON, images, fonts, video, API representations and many other media types.

### Durable lesson
The protocol's value is not merely moving bytes. It gives independently implemented clients, servers and intermediaries a shared vocabulary for requests, responses, metadata and resource interaction.

---

## 2. HTTP/0.9: radical simplicity made the first Web possible, but could not scale in expressiveness

### SOURCE
Historical W3C/IETF material describes the earliest HTTP, later called HTTP/0.9, as a very simple protocol for raw data transfer. RFC 1945 retains compatibility discussion for the simple HTTP/0.9 format.

A 1994 IETF HTTP BOF record says HTTP began as a very simple protocol and was extended with MIME-style wrapping, content type/encoding information, negotiation, metadata and basic authentication as the Web's needs expanded.

### FOUNDATION
The early design demonstrates a recurring systems principle:

> A minimal protocol can validate an architecture quickly, but ecosystem growth exposes missing metadata, negotiation, caching, security and performance needs.

The initial Web did not need today's elaborate response metadata because its environment and use cases were far smaller.

### Why history matters
Without this history, HTTP headers can look like arbitrary bureaucracy. Historically, many fields exist because raw document transfer became inadequate once clients needed to know what they received, how to interpret it, whether it changed, whether it could be reused, and how to negotiate behavior.

---

## 3. HTTP/1.0: messages acquire metadata and richer semantics

### SOURCE
RFC 1945 (May 1996) documents common HTTP/1.0 practice. It describes HTTP as an application-level, generic, stateless protocol and describes request/response operation using method, URI, protocol version, metadata and optional content.

The RFC explicitly says typed data representations allow systems to be built independently of the transferred data.

### FOUNDATION
Compared with the earliest simple exchange, HTTP/1.0 formalized a much richer message model:

- request method;
- target URI;
- protocol version;
- request metadata;
- optional request content;
- response status;
- response metadata;
- optional response content.

This is the conceptual ancestor of the modern HTTP message model.

### Important principle — representation typing
A client should not need to infer a response format from file extensions alone. HTTP metadata can describe the representation being transferred.

That principle later connects to `Content-Type`, content negotiation, APIs, accessibility-relevant document handling, caching and security.

---

## 4. Why HTTP/1.0 was not enough

### SOURCE
The HTTP/1.1 historical specification notes several pressures inadequately handled by HTTP/1.0 practice: hierarchical proxies, caching, persistent connections and virtual hosts, as well as inconsistent implementations claiming HTTP/1.0 compatibility.

### SYNTHESIS
As the Web grew, three dimensions changed simultaneously:

1. **Scale** — more users, resources and requests;
2. **Topology** — proxies/caches/intermediaries appeared between clients and origins;
3. **Economics of connections** — repeatedly creating connections for many page resources imposed latency and network cost.

HTTP therefore had to become more explicit about message boundaries, caching, intermediaries, host authority and connection reuse.

This is a recurring Web Manager lesson: protocols evolve not only because of new features but because an architecture that works at small scale behaves differently under large-scale latency, congestion, caching and intermediary conditions.

---

## 5. HTTP/1.1: persistence and scalable Web infrastructure

### SOURCE
Historical HTTP/1.1 specifications made persistent connections the default. Persistent connections reduce repeated connection-opening overhead and can reduce latency and network load.

Current RFC 9112 specifies HTTP/1.1 message syntax, parsing and connection management. It describes HTTP as a stateless application-level protocol.

### FOUNDATION
A Web page rarely consists of one object. It can require HTML, stylesheets, scripts, images, fonts and API requests.

If every object required a new transport connection, setup costs would be repeatedly paid. Persistent connections allow multiple HTTP exchanges to use an established connection under protocol rules.

### Deeper consequence
This is why Web performance cannot be understood by counting file sizes alone. Connection setup, request concurrency, round trips, prioritization, congestion and reuse all affect observed latency.

Those mechanics will be studied in later performance/transport blocks rather than prematurely reduced to one optimization rule.

---

## 6. Modern HTTP separates semantics from version-specific expression

### SOURCE
RFC 9110 defines HTTP semantics. RFC 9112 defines HTTP/1.1 syntax/connection mechanics. RFC 9113 defines HTTP/2 as an optimized expression of HTTP semantics. RFC 9114 maps HTTP semantics over QUIC for HTTP/3.

HTTP/2 introduces binary framing, field compression and concurrent streams on one connection. HTTP/3 maps the same HTTP semantic model over QUIC, whose stream model avoids the TCP-level cross-stream stall problem described by RFC 9114.

### FOUNDATION
This distinction is critical:

**HTTP semantics** answer questions such as:
- what does GET mean?
- what does a 404 mean?
- what does a representation describe?
- is an operation safe or idempotent?
- what does a cache validator mean?

**HTTP version/framing/transport mechanics** answer questions such as:
- how are fields and content encoded on the wire?
- can multiple exchanges progress concurrently?
- how is a connection transported?
- how are streams framed/compressed/flow-controlled?

### SYNTHESIS
HTTP/1.1 → HTTP/2 → HTTP/3 should **not** be learned as three unrelated application protocols.

A better model is:

`durable HTTP semantics` + `evolving message/transport expression`

This explains how a browser can request the same conceptual resource with the same GET semantics while the underlying protocol expression differs substantially.

---

## 7. HTTP is request/response, but not necessarily direct browser→origin

### SOURCE
HTTP specifications model user agents, origin servers and intermediaries. HTTP can pass through proxies, gateways and caches rather than always being a direct two-party path.

### FOUNDATION
The beginner diagram:

`browser → server`

is useful but incomplete.

A more realistic conceptual path can be:

`user agent → intermediary/cache/CDN/proxy → origin infrastructure`

The response observed by a browser might therefore be:
- generated by the origin;
- reused by a cache;
- transformed or routed by infrastructure where allowed/configured;
- rejected before reaching application code.

### Web Manager implication
A response header/status is evidence about the HTTP exchange, but not automatically proof that application code generated it. Diagnosis must identify which participant produced or modified the response.

---

## 8. Stateless semantics: what it does and does not mean

### SOURCE
RFC 9112 calls HTTP a stateless application-level protocol.

### FOUNDATION
"HTTP is stateless" does **not** mean websites cannot have login sessions, carts, preferences or personalized state.

It means the protocol's request/response semantics do not inherently require a server to maintain conversational application state between requests in order for HTTP itself to function.

Application state can be layered through mechanisms such as cookies, authorization credentials, URLs, server-side session stores or client storage.

### Common misconception
`HTTP is stateless → every website interaction is independent and cannot remember users` is false.

A stateless protocol can carry identifiers or credentials that applications use to reconstruct/associate state.

This distinction will matter later for cookies, authentication, privacy and caching.

---

## 9. Method semantics are contracts, not just route names

### SOURCE
RFC 9110 defines method semantics and explicitly distinguishes **safe** and **idempotent** methods.

GET, HEAD, OPTIONS and TRACE are defined as safe. Safe means the client does not request a state-changing effect, even though incidental side effects such as logging can occur.

A method is idempotent when multiple identical requests have the same intended effect on the server as one such request. Safe methods, PUT and DELETE are defined as idempotent.

### FOUNDATION
These properties exist because software needs to reason about what it may do automatically.

Examples:
- crawlers and prefetchers need safe retrieval semantics;
- clients may be able to retry idempotent operations after uncertain connection failure;
- caches need method semantics to determine reuse behavior;
- UI and API design should not hide destructive operations behind a safe GET.

### Critical example
A URL such as:

`GET /account/delete?id=123`

that actually deletes an account violates the intended safe semantics of GET. A crawler, prefetcher or link checker could trigger it merely by following the URL.

### Web Manager implication
HTTP semantics have direct UX, SEO, reliability and security consequences. They are not backend-programmer trivia.

---

## 10. Safe ≠ idempotent ≠ cacheable

These concepts must remain separate.

### Safe
The client does not request a state-changing action.

### Idempotent
Repeating the same request has the same intended server effect as performing it once.

### Cacheable
A response is permitted to be stored/reused according to HTTP caching rules.

### Example reasoning
- GET: safe and idempotent; responses are commonly cacheable subject to rules/metadata.
- PUT: not safe, but idempotent by defined semantics.
- DELETE: not safe, but idempotent by defined semantics even if later responses differ after deletion has already occurred.
- POST: not generally safe or idempotent; some POST responses can nevertheless be cached when explicit requirements are met.

### Common misconception
"Idempotent means the response must be identical every time" is wrong. It concerns the intended effect, not byte-for-byte response equality.

---

## 11. Status codes are protocol semantics, not UI copy

### FOUNDATION
HTTP status codes tell a recipient how to interpret the outcome of the HTTP request. They are not substitutes for user-facing error design.

Classes:
- 1xx — informational;
- 2xx — successful handling;
- 3xx — redirection/further action;
- 4xx — request/client-side class of error semantics;
- 5xx — server-side class of failure semantics.

### Important nuance
"4xx means the human user made a mistake" is an oversimplification. It describes the HTTP request/response condition. A broken link generated by MintTap can lead a user to a 404 even though the user did nothing wrong.

Similarly, a polished branded error page returning HTTP 200 is still semantically problematic for machines because the protocol says success while the content says failure.

This later connects directly to SEO, monitoring and accessibility.

---

## 12. Fields/headers are protocol metadata, not decoration

### FOUNDATION
HTTP fields communicate metadata that affects representation interpretation, caching, negotiation, authorization, conditional requests, redirects, security policy and intermediary behavior.

Examples to be studied in depth later:
- `Content-Type` — representation media type;
- `Content-Length` — representation/message length information in applicable versions/contexts;
- `Location` — redirect/new-resource location semantics in applicable responses;
- `Cache-Control` — cache directives;
- `ETag`, `Last-Modified` — validators/metadata for conditional operations;
- `Accept`, `Accept-Language` — representation preferences;
- `Vary` — which request fields influenced selected representation for cache matching;
- `Authorization` — credentials for HTTP authentication schemes;
- `Cookie` / `Set-Cookie` — state-management extension semantics.

### Web Manager implication
Changing a header can change browser, CDN, crawler and cache behavior even when the HTML bytes are unchanged.

---

## 13. Why HTTP caching exists

### SOURCE
RFC 9111 defines an HTTP cache as a local store of response messages plus the subsystem controlling storage/retrieval/deletion. Its goal is to improve performance by reusing prior responses, reducing response time and network bandwidth.

It distinguishes private and shared caches.

### FOUNDATION
Caching is not simply "save a file for N seconds."

A cache must reason about:
- whether a response may be stored;
- whether the stored response matches the new request;
- whether it is fresh;
- whether stale content may be reused;
- whether it must contact another server to validate it;
- whether the representation varies based on request metadata.

### Freshness vs validation
A fresh response can generally be reused without contacting the origin.

A stale response might be revalidated using validators such as:
- `ETag` with `If-None-Match`;
- `Last-Modified` with `If-Modified-Since`.

If unchanged, a `304 Not Modified` response can allow reuse of the stored representation without retransmitting the full content.

### Important distinction from Study 028
DNS caching and HTTP caching are different systems.

- DNS cache reuses naming-system answers.
- HTTP cache reuses HTTP responses/representations.

A fresh DNS answer does not imply fresh page content, and clearing browser HTTP cache does not necessarily clear upstream DNS caches.

---

## 14. `no-cache` does not mean "do not store"

### SOURCE
Under modern HTTP caching semantics, `no-cache` requires validation before reuse; it is not synonymous with prohibition on storage. `no-store` is the directive used to request that caches not store the response/request content under its defined rules.

### Why this matters
This naming is historically unintuitive and frequently misunderstood.

A Web Manager who reads `Cache-Control: no-cache` as "the browser has no copy" can misdiagnose production behavior.

This will receive deeper treatment in the caching sub-block.

---

## 15. Representation selection and `Vary`

### SOURCE
RFC 9111 requires caches to account for request fields named by `Vary` when determining whether a stored response matches a later request.

### FOUNDATION
One URL can have multiple representations.

For example, a server could select different output based on language preferences. If a cache ignores the dimension that caused the variation, one user's representation could be incorrectly reused for another request.

### MintTap relevance
This is directly relevant to Korean/English architecture. It reinforces an earlier strategic preference for explicit locale URLs where practical: URLs make locale identity clearer to users, crawlers, analytics and caches. Header-based negotiation still has valid uses, but it introduces cache-key and discoverability considerations.

This is a synthesis, not a claim that HTTP requires locale-specific URLs.

---

## 16. HTTP/2: optimize expression without redefining the Web's application semantics

### SOURCE
RFC 9113 says HTTP/2 is an optimized expression of HTTP semantics. It introduces binary framing, concurrent streams/multiplexing and field compression to improve network-resource use and latency.

### Historical problem
HTTP/1.1 had no multiplexing layer. Browsers often used multiple TCP connections to obtain parallelism.

HTTP/2 allows multiple HTTP exchanges as independent streams on one connection.

### Important limitation
Those streams still share TCP transport. RFC 9114 explains that TCP loss recovery can stall all active HTTP/2 transactions when a packet is lost/reordered, even if only one stream's data was directly involved.

This is one motivation for HTTP/3's transport change.

---

## 17. HTTP/3: change the transport foundation, preserve HTTP semantics

### SOURCE
RFC 9114 maps HTTP semantics over QUIC. QUIC provides stream multiplexing, per-stream flow control, low-latency connection establishment and integrated TLS 1.3 security properties.

### FOUNDATION
HTTP/3 is not "HTTP but with different status codes." The application semantics remain recognizably HTTP; the transport/framing mechanics change substantially.

Simplified evolution:

`HTTP/1.x semantics + text-oriented HTTP/1.x messaging over TCP`

→ `same core semantics + HTTP/2 binary streams/multiplexing over TCP`

→ `same core semantics + HTTP/3 framing over QUIC streams`

### Expert-direction lesson
When a new HTTP version appears, first ask:
1. Did application semantics change?
2. Did message representation/framing change?
3. Did transport behavior change?
4. What problem was the change intended to solve?

Do not reduce protocol evolution to a version-number ranking.

---

## 18. A first complete conceptual exchange

After Studies 027–028 and this block, a more mature conceptual page request is:

1. User/browser obtains a URL.
2. Browser parses scheme/host/port/path/query/fragment and determines origin.
3. DNS resolution obtains routing-relevant addressing/service information through resolver/cache/authority mechanisms.
4. A transport/security path is established as appropriate; TLS details are still deferred.
5. The user agent expresses an HTTP request with a method, target and fields, optionally content.
6. Intermediaries may participate.
7. A cache may satisfy the request when HTTP caching semantics allow it; otherwise the request proceeds toward the origin/service.
8. The selected server/intermediary returns a status, fields and optional content representing the outcome.
9. The browser interprets the representation according to metadata such as media type and then invokes later document/runtime behavior.
10. Additional subresource requests repeat HTTP exchanges, potentially reusing connections/caches depending on protocol/version/policy.

This is still intentionally incomplete until TLS, browser rendering and storage studies are completed.

---

## 19. Failure-mode reasoning introduced by HTTP

A user says: "The page is wrong."

After DNS succeeds, candidate HTTP-layer causes now include:
- wrong method semantics;
- redirect loop or wrong redirect target;
- incorrect status code;
- incorrect media type;
- stale cache entry;
- incorrect cache directives;
- cache key / `Vary` mismatch;
- intermediary-generated error;
- origin-generated error;
- representation selected for wrong request conditions;
- conditional request/validator mismatch;
- protocol/version/intermediary incompatibility.

A Web Manager should inspect evidence before attributing the failure to application code.

---

## 20. MintTap provisional operating principles from this block

### SYNTHESIS / MINTTAP DIRECTION
1. Public web endpoints should use HTTP method semantics correctly; destructive state change must not be hidden behind GET.
2. HTTP status and content must agree: error content should not casually return success semantics.
3. Cache policy must be deliberate by resource class rather than one global arbitrary TTL.
4. Versioned immutable assets and mutable HTML/API/governance documents will likely need different cache strategies; exact policy belongs to later applied stages.
5. Locale variation must account for cache behavior; explicit locale URLs remain a strong architectural default, not an HTTP requirement.
6. CDN/hosting responses must be diagnosed as part of an intermediary chain rather than assuming every response originates in app code.
7. HTTP/2 or HTTP/3 availability alone does not prove a fast site. Resource design, caching, server latency, connection conditions and browser work still matter.

---

## 21. Misconceptions to eliminate

- HTTP = HTML delivery. **False.**
- HTTP/3 replaced HTTP semantics with a different application model. **False.**
- Stateless means a website cannot remember a login. **False.**
- GET is harmless because developers usually use it for reading. **Incomplete:** safety is a defined semantic contract and must be respected by the resource implementation.
- Idempotent means identical response bytes. **False.**
- 404 means the user made an error. **False.**
- 200 means the page is semantically correct. **False.** It means HTTP success semantics, not content quality.
- `no-cache` means nothing is stored. **False.**
- DNS cache and browser HTTP cache are the same. **False.**
- HTTP/2 multiplexing means transport loss can never stall unrelated streams. **False over TCP.**
- HTTP/3 automatically makes every website fast. **False.**

---

## 22. Competency checkpoint for this sub-block

Before advancing within HTTP, the Web Manager should be able to explain without memorized slogans:

1. Why did the original Web need HTTP in addition to identifiers and HTML?
2. What limitation of HTTP/0.9 led toward metadata-rich HTTP messages?
3. What growth pressures exposed HTTP/1.0 limitations?
4. Why did persistent connections matter to HTTP/1.1?
5. What is the difference between HTTP semantics and HTTP/1.1, HTTP/2 or HTTP/3 wire/transport expression?
6. Why is HTTP called stateless while websites still maintain sessions?
7. Distinguish safe, idempotent and cacheable.
8. Why is deleting data with GET dangerous beyond style preference?
9. Why can a 200 response still be operationally wrong?
10. What problem does HTTP caching solve?
11. Distinguish freshness from validation.
12. Explain why `no-cache` and `no-store` are not synonyms.
13. Why does `Vary` matter to caches?
14. What did HTTP/2 multiplexing improve?
15. Why can TCP still create cross-stream stalls for HTTP/2?
16. Why did HTTP/3 move HTTP semantics onto QUIC?
17. Why does protocol version alone not determine site performance?

If these cannot be explained, this layer should be revisited.

---

## 23. HTTP domain is NOT complete — required next deep blocks

Rather than immediately moving to TLS, continue HTTP until the following are understood:

### 029A — Message anatomy and field model
- request/response conceptual components;
- HTTP/1.1 start line vs HTTP/2/3 pseudo-fields/framing distinction;
- field syntax/combination;
- content vs message framing;
- Content-Type, Content-Length, Transfer-Encoding;
- trailers;
- malformed/ambiguous message security implications.

### 029B — Methods and status semantics in depth
- GET/HEAD/POST/PUT/DELETE/OPTIONS/PATCH context;
- safe/idempotent/cacheable matrix;
- 1xx–5xx important codes;
- 201/202/204;
- 301/302/303/307/308 historical semantics;
- 304;
- 400/401/403/404/405/409/410/412/415/422/429;
- 500/502/503/504;
- retry implications.

### 029C — Representations and negotiation
- representation metadata/data;
- media types;
- charset/encoding distinction;
- Accept / Accept-Language / Accept-Encoding;
- proactive vs reactive negotiation concepts;
- Content-Encoding;
- Vary;
- range requests.

### 029D — Caching and conditional requests in depth
- cache key;
- private/shared cache;
- freshness lifetime/current age;
- Cache-Control directives;
- heuristic freshness;
- validators;
- strong/weak ETag;
- Last-Modified;
- conditional request precedence;
- 304;
- stale behavior;
- immutable fingerprinted assets vs mutable documents;
- CDN/browser cache interaction.

### 029E — Intermediaries and connection evolution
- proxy/reverse proxy/gateway/CDN concepts;
- Via/Forwarded concepts where relevant;
- HTTP/1.1 persistent connections;
- pipelining historical limitations;
- HTTP/2 framing/streams/HPACK overview;
- TCP head-of-line effects;
- HTTP/3/QUIC/QPACK overview;
- protocol negotiation/discovery at conceptual level.

### 029F — Operational diagnosis
- reading browser Network panels;
- curl-style request/response inspection conceptually;
- redirects;
- cache hit/miss evidence;
- origin vs intermediary clues;
- method/status/header diagnosis;
- representative failure cases;
- performance waterfall interpretation foundations.

Only after these blocks should HTTP be considered sufficiently mature for Stage 1 and the curriculum move to dedicated TLS study.

---

## Sources

Primary / standards / historical:
- W3C, History of the Web: https://www.w3.org/about/history/
- Tim Berners-Lee / W3C, *The World Wide Web: Past, Present and Future*: https://www.w3.org/People/Berners-Lee/9610-IEEE-Computer.html
- W3C archive, HTTP BOF minutes, December 1994: https://lists.w3.org/Archives/Public/ietf-http-wg/1994OctDec/0258.html
- RFC 1945, *Hypertext Transfer Protocol -- HTTP/1.0*, May 1996: https://www.rfc-editor.org/rfc/rfc1945.html
- RFC 9110, *HTTP Semantics*, June 2022: https://www.rfc-editor.org/rfc/rfc9110.html
- RFC 9111, *HTTP Caching*, June 2022: https://www.rfc-editor.org/rfc/rfc9111.html
- RFC 9112, *HTTP/1.1*, June 2022: https://www.rfc-editor.org/rfc/rfc9112.html
- RFC 9113, *HTTP/2*, June 2022: https://www.rfc-editor.org/rfc/rfc9113.html
- RFC 9114, *HTTP/3*, June 2022: https://www.rfc-editor.org/rfc/rfc9114.html
- Historical RFC 2616 / HTTP/1.1 material used only for evolution context; current semantics are taken from the RFC 9110-series.

## Evidence classification

- `SOURCE`: historical chronology and protocol semantics directly supported by W3C/IETF/RFC material above.
- `SYNTHESIS`: historical problem→design-pressure→modern architecture reasoning; HTTP version-learning model; operational layer conclusions.
- `MINTTAP DIRECTION`: method correctness, status/content agreement, deliberate cache classes, intermediary-aware diagnosis and locale/cache awareness.
- `OPEN`: exact MintTap HTTP/CDN/cache policies remain project-specific and require actual architecture/content classes.
- `DEPENDENCY`: no Design Studio dependency for this protocol-history block.
- `VALIDATION`: later 029F should inspect real HTTP exchanges; this block does not claim implementation validation.
- `CHANGE WATCH`: HTTP standards and browser/proxy behavior can evolve; current protocol decisions must check current RFC/browser/provider support.
