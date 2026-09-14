# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

Build professional Web Manager judgment from first principles through advanced cross-domain reasoning. GitHub is canonical memory; chat is temporary context.

Canonical curriculum: `LEARNING_ROADMAP.md`.

### Depth rule now in force
Large subjects are not completed by one survey file. Study follows:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment`

A topic remains active until it can be explained, diagnosed and applied—not merely defined.

## Current position — Stage 1 / HTTP domain ACTIVE

### 027 — Web/Internet/URL/Origin
**FOUNDATION LAYER COMPLETE**, retained for later reintegration.

### 028 — DNS/Domain/Resolution
**FOUNDATION LAYER COMPLETE**, retained for later practitioner/advanced reintegration.

### 029 — HTTP
`research/029-http-foundations-history-semantics-evolution.md`

**Deep foundation history/semantics block complete; HTTP itself is NOT complete.**

New understanding established:
- HTTP arose as the transfer/interchange protocol of the early distributed hypertext Web alongside identifiers and HTML;
- HTTP/0.9's radical simplicity was useful initially but lacked the metadata/negotiation machinery demanded by a growing Web;
- HTTP/1.0 documented richer request/response messages and typed representations;
- growth introduced proxies, caching, virtual hosting and connection-cost pressures that exposed HTTP/1.0 limitations;
- HTTP/1.1 made persistent connections a core scaling/performance behavior;
- modern standards deliberately separate durable HTTP semantics (RFC 9110) from caching (9111), HTTP/1.1 messaging (9112), HTTP/2 expression (9113) and HTTP/3-over-QUIC expression (9114);
- HTTP/2 and HTTP/3 should be understood as evolving expressions/transports of the same core application semantics rather than unrelated protocols;
- stateless HTTP does not prohibit application sessions/state;
- safe, idempotent and cacheable are separate semantic properties;
- destructive behavior behind GET violates safe-method semantics and can be triggered by automated retrieval/prefetch/crawling;
- status codes are machine/protocol semantics, not user-facing error copy;
- HTTP fields can materially alter browser/cache/CDN/intermediary behavior without changing HTML bytes;
- HTTP caching reuses response messages/representations and is distinct from DNS caching;
- freshness and validation are distinct; ETag/Last-Modified can support conditional validation and 304 reuse;
- `no-cache` is not synonymous with `no-store`;
- `Vary` participates in cache matching when representation selection depends on request fields;
- HTTP/2 multiplexes streams over TCP and compresses fields, but TCP loss can still stall multiple active transactions;
- HTTP/3 maps HTTP semantics over QUIC, moving multiplexing/reliability behavior into a stream-aware transport.

Primary sources: W3C Web history/early HTTP records; RFC 1945; RFC 9110, 9111, 9112, 9113, 9114. Historical RFC 2616 is used only for evolution context, not as current normative authority.

## HTTP deep-study queue

Do **not** move to TLS yet. Continue:

1. **029A — Message anatomy & field model**
   - request/response components;
   - HTTP/1.1 start lines vs HTTP/2/3 framing/pseudo-fields;
   - field model and combination;
   - content vs framing;
   - Content-Type/Length/Transfer-Encoding/trailers;
   - malformed/ambiguous message security implications.

2. **029B — Methods & status semantics in depth**
   - method-by-method semantics;
   - safe/idempotent/cacheable reasoning;
   - redirects and historical 301/302 ambiguity vs 303/307/308;
   - important 2xx/3xx/4xx/5xx codes;
   - retry implications.

3. **029C — Representations & content negotiation**
   - media types, charset/encoding distinctions;
   - Accept families, Content-Encoding, Vary;
   - representation selection and ranges.

4. **029D — Caching & conditional requests**
   - cache keys/private/shared caches;
   - freshness/age/directives;
   - validators/ETag/Last-Modified;
   - conditional precedence/304;
   - stale rules;
   - browser/CDN cache interactions;
   - immutable vs mutable resource strategies.

5. **029E — Intermediaries & protocol evolution mechanics**
   - proxy/reverse proxy/gateway/CDN;
   - persistence/pipelining history;
   - HTTP/2 frames/streams/HPACK;
   - TCP HOL effects;
   - HTTP/3/QUIC/QPACK;
   - negotiation/discovery concepts.

6. **029F — Operational diagnosis**
   - browser Network evidence;
   - request/response inspection;
   - redirect/cache/intermediary diagnosis;
   - representative failures;
   - performance-waterfall foundations.

Only after these are integrated should dedicated TLS study begin.

## Competency requirement

HTTP is not complete until the Web Manager can:
- reconstruct why each major protocol generation exists;
- distinguish semantics from framing/transport;
- reason about method safety/idempotence/retry;
- interpret important statuses/fields;
- explain representation selection and caching;
- identify intermediary effects;
- diagnose representative exchanges from evidence;
- connect HTTP choices to SEO, performance, security, privacy, accessibility and UX without conflating layers.

## Existing prior strengths retained

Studies 001–026 remain prior evidence across launch requirements, IA, privacy/support, accessibility, localization, SEO, security, hosting, legal and release governance. They will be reintegrated at the appropriate curriculum stages.

## Design Studio relationship

No Design Studio handoff is required for the current protocol-history block. Later browser/design/performance studies will consume Design Studio evidence where visual or interaction decisions matter.

## Next action

Continue directly with **029A — HTTP Message Anatomy & Field Model**. Preserve the slower deep-study tempo and historical/design rationale rather than rushing to the next numbered domain.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` records the deep-domain rule.
- `029-http-foundations-history-semantics-evolution.md` is the current completed HTTP sub-block.
- HTTP remains **ACTIVE / NOT COMPLETE**.
