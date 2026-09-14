# 029A — HTTP Message Anatomy, Field Model & Framing

Status: **DEEP FOUNDATION SUB-BLOCK COMPLETE — HTTP DOMAIN STILL ACTIVE**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations / HTTP deep study

## Why this study exists

Knowing that HTTP uses requests and responses is not enough. A Web Manager must understand which parts describe *meaning*, which parts are merely a version-specific wire representation, and how recipients know where one message/content region ends. This distinction explains otherwise confusing differences between HTTP/1.1, HTTP/2 and HTTP/3 and exposes why malformed framing can become a security boundary failure rather than a cosmetic syntax error.

The central question is:

> What is an HTTP message conceptually, and how is that conceptual message serialized differently by each major protocol version?

## 1. Historical design pressure: from a tiny request to structured messages

Early HTTP could be extremely simple because the original Web problem was correspondingly narrow: identify a document and retrieve it. As HTTP evolved, clients and servers needed metadata about representations, status, negotiation, caching, routing and connection behavior. The protocol therefore acquired structured control data and fields around content.

The important historical lesson is not that modern HTTP has 'more headers'. It is that a growing distributed system needed a richer **message model**, while later protocol generations discovered that the original textual serialization was not the only or best way to carry that model.

## 2. Semantic message model vs wire syntax

### SOURCE — RFC 9110

Modern HTTP semantics are deliberately separated from version-specific messaging. RFC 9110 describes messages in terms of control data, header fields, content and optional trailer fields. HTTP/1.1 carries control data in a first line; HTTP/2 and HTTP/3 express equivalent control information with pseudo-header fields.

### FOUNDATION

Conceptually, an HTTP request/response can contain:

1. **control data** — e.g. request method/target information or response status;
2. **header section** — fields that modify, describe or provide metadata about the message, representation, request or response;
3. **content** — optional sequence of bytes associated with the message semantics;
4. **trailer section** — optional fields sent after content where the protocol permits them.

Do not equate this conceptual model with the familiar HTTP/1.1 text shape.

### Key distinction

`HTTP semantics ≠ HTTP/1.1 textual serialization`

This is one of the most important ideas in the entire HTTP domain.

## 3. HTTP/1.1 message anatomy

### SOURCE — RFC 9112

HTTP/1.1 serializes a message as:

`start-line + CRLF`
`zero or more field-lines + CRLF`
`empty line (CRLF)`
`optional message-body`

A request uses a **request-line**; a response uses a **status-line**.

Illustrative request:

```text
GET /apps/example HTTP/1.1
Host: minttap.app
Accept: text/html

```

Illustrative response:

```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1234

[1234 bytes ...]
```

The examples explain serialization, not a MintTap production configuration.

### Why the empty line matters

HTTP/1.1's empty line terminates the header section. After that boundary, subsequent octets may be message body/content according to the message-body-length rules. A parser therefore cannot safely treat an HTTP/1.1 exchange as arbitrary lines of text.

## 4. Request-line and status-line are HTTP/1.x expressions, not universal HTTP concepts

In HTTP/1.1, the request-line carries method, request-target and protocol version. The response status-line carries protocol version, status code and reason phrase.

But HTTP/2 and HTTP/3 do not preserve this literal textual start-line. They carry control data in pseudo-header fields.

Typical request control data becomes conceptually represented by fields such as:
- `:method`
- `:scheme`
- `:authority`
- `:path`

A response carries `:status`.

### Consequence

A browser DevTools panel might present a convenient 'request headers' view that resembles HTTP/1 syntax even when the network protocol is HTTP/2 or HTTP/3. The UI representation must not be mistaken for literal bytes on the wire.

## 5. HTTP fields: more than 'headers containing text'

### SOURCE — RFC 9110

HTTP fields are extensible key/value metadata. A field line consists conceptually of a field name and field value. Field definitions establish syntax and semantics, including whether multiple field lines can be combined and how recipients interpret them.

### FOUNDATION

A field can influence very different layers of HTTP behavior. Examples include:
- representation metadata: `Content-Type`;
- representation coding: `Content-Encoding`;
- caching: `Cache-Control`, `ETag`, `Vary`;
- redirects: `Location` in appropriate responses;
- authentication: `Authorization`, `WWW-Authenticate`;
- conditional requests: `If-None-Match`, `If-Modified-Since`;
- routing/authority in HTTP/1.1: `Host`;
- connection-specific behavior in HTTP/1.1: fields such as `Connection`.

Therefore 'the HTML is identical' does not imply two responses behave identically. Their field metadata may produce different cache, browser, security or intermediary behavior.

## 6. Field name case and protocol generation

HTTP field names are case-insensitive semantically. However, HTTP/2 and HTTP/3 impose lowercase encoding requirements and treat uppercase field names as malformed.

This is a useful example of the semantics/wire distinction: semantic identity can be case-insensitive while a particular wire protocol imposes a stricter serialized form.

## 7. Content is not the same thing as message framing

A common beginner model is:

`headers + body`

That is useful initially but insufficient.

The protocol must answer two different questions:

1. **What bytes are the message's content/representation?**
2. **How does the recipient determine message/content boundaries on this connection/stream?**

These are not identical questions.

`Content-Type` describes media type of content/representation metadata. It does not delimit an HTTP/1.1 message.

`Content-Length` can participate in HTTP/1.1 message framing by declaring an expected number of octets in applicable cases. It is not a media-type declaration.

`Transfer-Encoding` is a message-transfer mechanism specific to HTTP/1.1 framing; it is not the same concept as `Content-Encoding`.

## 8. Content-Length: simple-looking, security-significant

### SOURCE — RFC 9112

HTTP/1.1 has an ordered algorithm for determining message body length. Some responses cannot contain a message body regardless of fields; successful CONNECT has tunnel semantics; and combinations such as both `Transfer-Encoding` and `Content-Length` are dangerous enough that the specification warns they can indicate request smuggling or response splitting and ought to be handled as errors.

### FOUNDATION

`Content-Length: 1234` means the applicable message framing expects 1234 octets of content/message body under the protocol rules. It does **not** mean:
- there are 1234 characters;
- the resource is always 1234 bytes in every representation;
- this value alone overrides all other body-length rules.

The surrounding message semantics and framing precedence still matter.

## 9. Transfer-Encoding and chunked history

Persistent HTTP/1.1 connections created a practical problem: if the connection remains open for reuse and the sender does not know the content length in advance, connection close can no longer serve as the normal boundary marker for every response.

HTTP/1.1 therefore supports transfer codings; `chunked` framing allows content to be sent in chunks with explicit chunk lengths and an end marker. This permits streaming a dynamically generated body without knowing its final size before transmission.

### Critical distinction

- `Transfer-Encoding` describes transfer framing/coding between HTTP/1.1 message participants;
- `Content-Encoding` describes a coding applied to representation/content, such as compression, and is representation metadata.

They solve different problems.

HTTP/2 and HTTP/3 prohibit HTTP/1.x connection-specific transfer-coding machinery such as ordinary `Transfer-Encoding` use because their binary framing/stream structures provide message boundaries differently.

## 10. Why HTTP/2 changed the representation

HTTP/1.x textual framing was workable but increasingly costly/awkward for multiplexed modern traffic. HTTP/2 retains HTTP semantics while representing messages as frames on streams.

### SOURCE — RFC 9113

HTTP/2 carries field sections in HEADERS/related frames and message data in DATA frames. Control data is expressed with pseudo-header fields. A stream gives the protocol an explicit structural context unavailable in the same form in HTTP/1.1's sequential textual message parsing.

### FOUNDATION

Instead of thinking:

`one giant textual request followed by one giant textual response`

think:

`connection → multiple logical streams → frames belonging to each stream`

This enables multiplexing while preserving HTTP request/response semantics.

## 11. Why HTTP/3 changes the transport again

### SOURCE — RFC 9114

HTTP/3 carries HTTP over QUIC. Requests use client-initiated bidirectional QUIC streams; HTTP/3 frames have explicit type and length; HEADERS frames carry QPACK-encoded field sections and DATA frames carry content bytes. HTTP/3 also uses pseudo-header control data.

### FOUNDATION

The conceptual message survives again:

`request/response semantics + fields + content`

but the wire machinery is now:

`QUIC connection → streams → HTTP/3 frames`

This reinforces the durable lesson:

> Learn HTTP's semantic message model first; learn each protocol generation's framing as an implementation of that model.

## 12. Trailers: why fields can appear after content

A trailer section allows certain fields to be sent after content. This can be useful when a field value cannot be known until content has been generated or processed.

Trailers are constrained: not every field is meaningful or safe as a trailer, and recipients/intermediaries may impose version-specific handling rules. A Web Manager should therefore recognize trailers as part of the HTTP model without assuming arbitrary header fields can simply be moved after content.

## 13. Ambiguous framing becomes a security problem

### SOURCE — RFC 9112

HTTP/1.1 explicitly identifies request smuggling risk when different recipients parse message boundaries differently. `Transfer-Encoding` plus `Content-Length`, malformed transfer codings, duplicate/conflicting lengths and inconsistent parsing can create disagreement between a front-end intermediary and a back-end server.

### Mechanism

Imagine:

`client → CDN/reverse proxy → application server`

If the front end concludes request A ends at byte X, while the back end concludes it ends at byte Y, bytes between X and Y can be interpreted as part of another request by one component but not the other.

This is not merely 'invalid syntax'. It is a **parser differential across a trust boundary**.

### Web Manager implication

When architecture introduces proxies, CDNs, gateways or load balancers, protocol parsing consistency is part of security. Correct HTTP normalization and rejecting ambiguous messages matter even when application code itself appears safe.

## 14. Content-Length vs transfer framing vs compression

Keep these questions separate:

| Question | Concept/example |
|---|---|
| What kind of representation is this? | `Content-Type: text/html` |
| Has the representation/content been encoded? | `Content-Encoding: gzip` |
| How is HTTP/1.1 transfer/message framing expressed? | `Content-Length` or applicable `Transfer-Encoding` rules |
| How does HTTP/2 separate units? | frames/streams |
| How does HTTP/3 separate units? | HTTP/3 frames on QUIC streams |

The exact relationship between selected representation, content coding and message content length will be expanded in 029C.

## 15. Intermediaries can translate protocol versions

A request does not necessarily travel end-to-end using one HTTP version. A browser might communicate with an edge using HTTP/3 while the edge communicates upstream using HTTP/2 or HTTP/1.1.

RFC 9110 notes that intermediaries update the protocol version according to the connection being used; `Via` can communicate upstream protocol information.

Therefore:

`browser says h3` does not prove `edge → origin` also used HTTP/3.

This becomes important later for performance and request-smuggling diagnosis.

## 16. Browser DevTools is an interpretation layer

DevTools is essential evidence, but it is not a packet capture. Browser UI commonly normalizes fields and presents pseudo-header/control information in human-readable sections.

Operational rule:
- use DevTools to understand browser-observed requests/responses;
- do not infer exact on-wire byte syntax solely from the visual header panel;
- use protocol/network-level evidence when exact framing matters.

## 17. MintTap application

For a future `minttap.app` deployment, Web Manager should be able to ask:

- Which HTTP version does the browser negotiate with the public edge?
- Does a CDN/reverse proxy translate the request before origin?
- Are response metadata and content semantics correct independently of HTML appearance?
- Is dynamic content emitted with framing appropriate to the protocol stack?
- Are ambiguous HTTP/1.1 requests rejected at trust boundaries?
- Are application developers incorrectly treating `Content-Type`, `Content-Encoding`, `Content-Length` and transfer framing as interchangeable concepts?

No live MintTap configuration is inferred here.

## 18. Common misconceptions corrected

1. **'HTTP messages are always plain text.'** False. HTTP/1.x has textual message syntax; HTTP/2 and HTTP/3 use binary framing.
2. **'Headers are just descriptive labels.'** False. Fields can alter routing, caching, negotiation, authentication and security behavior.
3. **'Content-Length tells the type of content.'** False. It concerns length/framing; media type is a different concept.
4. **'Transfer-Encoding gzip and Content-Encoding gzip are basically the same.'** False. Transfer coding and representation/content coding have different semantics.
5. **'HTTP/2 is just HTTP/1.1 with compression.'** False. It changes framing and multiplexing while preserving core semantics.
6. **'If Chrome shows header-like text, those exact lines were transmitted.'** Not necessarily, especially for HTTP/2/3.
7. **'Malformed Content-Length is merely a broken response.'** Parser disagreement can create request-smuggling/security consequences.

## 19. Diagnostic exercise

Scenario: a public CDN accepts a request and forwards it to an origin. Logs disagree about where one HTTP/1.1 request ends.

Correct first reasoning path:
1. identify HTTP versions on each hop;
2. inspect whether an intermediary translated protocols;
3. inspect `Content-Length` / `Transfer-Encoding` and framing rules;
4. determine whether components parsed the same boundary;
5. reject/normalize ambiguity rather than assuming application routing is the root cause.

This is a protocol-framing problem until evidence proves otherwise.

## 20. Competency checkpoint for 029A

Before considering this sub-block retained, Web Manager should be able to explain:

1. Why HTTP semantics and HTTP/1.1 wire syntax are not the same thing.
2. The conceptual components of an HTTP message.
3. The HTTP/1.1 start-line/header/body serialization.
4. Why HTTP/2/3 use pseudo-header control data instead of literal start-lines.
5. Why `Content-Type`, `Content-Encoding`, `Content-Length` and `Transfer-Encoding` answer different questions.
6. Why persistent connections made explicit framing important.
7. How HTTP/2 streams/frames differ structurally from HTTP/1.1 parsing.
8. How HTTP/3 frames map onto QUIC streams.
9. Why ambiguous HTTP/1.1 framing can become request smuggling.
10. Why DevTools is useful evidence but not proof of exact wire bytes.

## 21. Boundaries / what remains active

029A does not complete HTTP. Still required:
- method/status semantics and redirects;
- representation selection/content negotiation;
- deep cache/conditional model;
- intermediary behavior and HTTP/2/3 mechanics;
- operational evidence diagnosis.

Request-smuggling mechanics are introduced only to explain why framing precision matters. Offensive exploitation procedures are outside this learning objective.

## Sources

Primary/current standards:
- IETF RFC 9110 — HTTP Semantics, 2022: https://www.rfc-editor.org/rfc/rfc9110.html
- IETF RFC 9112 — HTTP/1.1, 2022: https://www.rfc-editor.org/rfc/rfc9112.html
- IETF RFC 9113 — HTTP/2, 2022: https://www.rfc-editor.org/rfc/rfc9113.html
- IETF RFC 9114 — HTTP/3, 2022: https://www.rfc-editor.org/rfc/rfc9114.html

Historical context is inherited from `029-http-foundations-history-semantics-evolution.md` and its early-Web / HTTP/0.9 / 1.0 / 1.1 source trail.

## Evidence classification

- `SOURCE`: current message/field/framing rules from RFC 9110/9112/9113/9114.
- `SYNTHESIS`: semantics-vs-wire mental model, DevTools interpretation warning, and cross-hop protocol translation reasoning.
- `MINTTAP DECISION`: future MintTap web operations should diagnose HTTP per hop and treat metadata/framing correctness independently from visible page content.
- `OPEN`: actual MintTap edge/origin HTTP versions and intermediary topology remain project facts.
- `DEPENDENCY`: none from Design Studio for this protocol block.
- `VALIDATION`: no live POC required; exact production framing should be inspected only when a real deployment/incident needs it.
- `CHANGE WATCH`: HTTP extension fields and implementation behavior evolve; core RFC 9110-family model remains the current standards baseline for this study.