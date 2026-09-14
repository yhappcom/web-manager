# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

Build professional Web Manager judgment from first principles through advanced cross-domain reasoning. GitHub is canonical memory; chat is temporary context.

Canonical curriculum: `LEARNING_ROADMAP.md`.

## Learning cadence rule

Depth remains high, but reporting/file granularity is intentionally coarse.

Do not create/report one artifact for every small concept. Study multiple related sub-blocks internally, then persist/report one coherent professional knowledge unit. The target is **more learning per checkpoint, fewer checkpoints**.

Large subjects follow:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

A Stage 1 core can close once the domain can be explained, diagnosed and applied at the curriculum's required level. It is then deliberately reopened in later stages for advanced security, performance, browser, SEO or operations depth.

## Current position — Stage 1 Web Foundations

### 027 — Web/Internet/URL/Origin
**FOUNDATION LAYER COMPLETE**, retained for later reintegration.

### 028 — DNS/Domain/Resolution
**FOUNDATION LAYER COMPLETE**, retained for later practitioner/advanced reintegration.

### 029 — HTTP
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED**

Integrated artifacts:
- `research/029-http-foundations-history-semantics-evolution.md` — historical/problem/semantic foundation;
- `research/029a-http-message-anatomy-field-model-framing.md` — earlier message/framing deep block, retained as supporting detail;
- `research/029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md` — integrated semantics/caching/negotiation/intermediary/protocol evolution checkpoint;
- `research/029-http-operational-diagnosis-range-state-boundaries-competency.md` — operational diagnosis, range/state boundaries, registry change-awareness and final Stage 1 competency review.

HTTP competency now includes:
- origin/history and why the protocol evolved;
- semantics vs wire/framing/transport distinction;
- resource vs representation;
- request/response message model;
- method contracts, safe/idempotent/cacheable distinctions and retry implications;
- status semantics and redirect history/method behavior;
- representation metadata, media type, content coding and negotiation;
- `Vary` and cache matching;
- HTTP cache storage/matching/freshness/stale/validation/reuse lifecycle;
- private vs shared caches;
- validators and conditional requests/304;
- intermediary/proxy/CDN path reasoning;
- HTTP/1.1 vs HTTP/2 vs HTTP/3 mechanics at Web Manager depth;
- QUIC/QPACK design implications at the level necessary to understand HTTP/3;
- range requests and 206/416 interpretation;
- cookies as state layered over stateless HTTP;
- HTTP authentication boundary vs application login systems;
- standardized `Cache-Status` and `Proxy-Status` diagnostic evidence;
- browser Network tools as evidence views rather than literal packet truth;
- operational failure-layer diagnosis;
- awareness that IANA HTTP registries evolve (including the 2026 `QUERY` method standardized by RFC 10008).

Primary evidence includes RFC 9110/9111/9112/9113/9114, RFC 9000, RFC 9204/9205/9209/9211, RFC 6265 plus publication tracking for rfc6265bis, WHATWG Fetch and IANA HTTP registries.

### Stage decision

HTTP is **closed only for Stage 1 core progression**. It remains scheduled for spiral reintegration in later stages:
- Stage 6 — redirects/crawl/discovery;
- Stage 7 — caching/compression/prioritization/performance;
- Stage 8 — cookies/auth/origin/security/privacy/request-smuggling;
- Stage 9 — measurement/instrumentation;
- Stage 11 — CDN/proxy/deployment/operations.

This prevents both extremes: rushing onward with a shallow glossary, or never advancing because one protocol has effectively unlimited specialist depth.

## Next major domain

Proceed to **HTTPS / TLS / Certificates / Browser Trust**.

The study should again use a coarse integrated cadence and begin from first principles/history:
- what problem plaintext HTTP creates;
- confidentiality, integrity and peer authentication as distinct goals;
- SSL history and transition to TLS;
- TLS handshake mental model;
- symmetric vs asymmetric cryptography roles at conceptual Web Manager depth;
- certificates, public keys, signatures and certification paths;
- CA / root store / intermediate / leaf roles;
- hostname verification and SAN;
- SNI and ALPN where they connect to web operation;
- TLS 1.2 → TLS 1.3 evolution and why the handshake changed;
- HSTS and `.app` preload relevance later in the block;
- expiry, revocation limitations, clock errors, chain errors and browser trust failures;
- TLS termination at CDN/edge vs separate origin TLS;
- browser security evidence and operational diagnosis.

Do not split this into micro-reports. Reach a meaningful HTTPS/TLS checkpoint before reporting.

## Design Studio relationship

No Design Studio handoff was required for the completed HTTP protocol block. The latest Design Studio Web specialist remains at its own Foundation baseline stage. Web Manager should reconnect when browser performance, loading UX, responsive behavior, error-state design or implementation-visible constraints become material.

## Important unknown MintTap facts

Do not infer current production state from generic research. Real project work must verify:
- actual `minttap.app` DNS/hosting/CDN topology;
- browser-facing and origin-facing HTTP versions;
- real cache/validator policy;
- redirect inventory;
- cookie/auth use;
- current TLS certificate chain, issuer, renewal, HSTS and edge/origin termination model.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- HTTP Stage 1 core competency is complete.
- Current next major study: **HTTPS / TLS / Certificates / Browser Trust**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.