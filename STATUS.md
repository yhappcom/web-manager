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

### 029 — HTTP historical/semantic foundation
`research/029-http-foundations-history-semantics-evolution.md`

**Deep foundation history/semantics block complete; HTTP itself is NOT complete.**

Established the historical path from early Web/HTTP through HTTP/1.0, 1.1, 2 and 3; durable semantics vs protocol expression; safe/idempotent/cacheable separation; status/field semantics; first cache model; and transport/framing evolution.

### 029A — HTTP Message Anatomy, Field Model & Framing
`research/029a-http-message-anatomy-field-model-framing.md`

**DEEP FOUNDATION SUB-BLOCK COMPLETE; HTTP domain remains ACTIVE.**

New understanding established:
- conceptual HTTP message semantics must be separated from HTTP/1.1 textual wire syntax;
- modern message model includes control data, header fields, optional content and optional trailer fields;
- HTTP/1.1 uses request/status start-lines, field lines, an empty-line boundary and message-body-length rules;
- HTTP/2 and HTTP/3 carry control data through pseudo-header fields rather than literal HTTP/1.x start-lines;
- HTTP fields are behavioral metadata, not merely descriptive labels;
- field semantics can affect routing, cache, negotiation, authentication, conditional requests and intermediary behavior even when content bytes are unchanged;
- `Content-Type`, `Content-Encoding`, `Content-Length` and `Transfer-Encoding` answer different protocol questions;
- persistent HTTP/1.1 connections made reliable message framing essential because connection close could no longer delimit every response;
- chunked transfer coding historically enables unknown-length/dynamic HTTP/1.1 content to be transmitted without closing the reusable connection;
- HTTP/2 represents messages with frames on multiplexed streams; HTTP/3 represents HTTP with frames carried on QUIC streams;
- HTTP/2/3 lowercase field requirements illustrate semantic identity vs stricter wire representation;
- HTTP/1.1 body-length precedence is security-significant; conflicting `Transfer-Encoding` and `Content-Length` can signal ambiguous parsing/request-smuggling risk;
- framing disagreement between front-end intermediary and origin is a parser differential across a trust boundary;
- one browser→edge→origin transaction can use different HTTP versions on different hops;
- browser DevTools is an interpreted browser-observed representation, not proof of exact on-wire byte syntax.

Primary sources: RFC 9110, RFC 9112, RFC 9113 and RFC 9114.

No live MintTap test was needed; actual edge/origin protocol topology remains a project fact.

## HTTP deep-study queue

Completed deep sub-blocks:
1. 029 — history / design pressure / semantic model / protocol evolution.
2. 029A — message anatomy / fields / content vs framing / HTTP/1.1 vs 2 vs 3 / framing-security bridge.

Next:

3. **029B — Methods & Status Semantics in Depth**
   - why methods exist as semantic verbs;
   - GET/HEAD/POST/PUT/DELETE/OPTIONS/CONNECT/TRACE distinctions;
   - safe/idempotent/cacheable matrices and retry consequences;
   - status code classes as machine semantics;
   - important 1xx/2xx/3xx/4xx/5xx codes;
   - redirect history and 301/302 method ambiguity;
   - 303 vs 307 vs 308;
   - 401 vs 403, 404 vs 410, 409 vs 422, 429 vs 503;
   - retryability must not be inferred from class alone;
   - UI copy vs protocol status separation.

Then:
4. 029C — Representations & content negotiation.
5. 029D — Caching & conditional requests.
6. 029E — Intermediaries & protocol evolution mechanics.
7. 029F — Operational diagnosis.

Do **not** move to TLS until the HTTP domain is integrated.

## Competency requirement

HTTP is not complete until the Web Manager can reconstruct its evolution, distinguish semantics from framing/transport, reason about methods/retries/statuses, explain representation selection and cache behavior, identify intermediary effects, and diagnose representative exchanges from evidence.

029A adds the requirement to explain why framing is a security boundary and why DevTools views must not be confused with literal HTTP/2/3 wire syntax.

## Design Studio relationship

No Design Studio handoff required for 029A; this remains protocol/infrastructure foundation. Later browser/design/performance work will consume specialist evidence where appropriate.

## Next action

Continue directly with **029B — HTTP Methods & Status Semantics in Depth**. Maintain the slower deep-study tempo: include historical rationale, semantic contracts, failure/retry implications, redirect evolution and operational judgment. Do not treat a method/status catalog as sufficient learning.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- HTTP remains **ACTIVE / NOT COMPLETE**.
- 029 and 029A are completed HTTP sub-blocks.
- Current next sub-block: **029B**.
