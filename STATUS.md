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
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

HTTP competency now covers history/semantics, messages, method/status contracts, representations/content negotiation, caching/conditional requests, intermediaries, HTTP/1.1–3/QUIC relationships, range/state/auth boundaries and evidence-led operational diagnosis.

HTTP remains scheduled for spiral reintegration in later SEO/performance/security/analytics/operations stages.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`research/030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Competency established:
- confidentiality, integrity and authentication as distinct secure-channel goals;
- plaintext HTTP threat model at Web Manager depth;
- SSL → TLS evolution and why legacy versions were retired;
- current TLS 1.3 authority: **RFC 9846 (July 2026), which obsoletes RFC 8446**;
- TLS 1.2 → 1.3 simplification/security rationale;
- handshake vs record protocol;
- asymmetric authentication/key establishment vs symmetric traffic protection;
- X.509 certificate/public/private-key roles;
- root/intermediate/leaf and certification-path reasoning;
- trust anchors as relying-party/browser policy rather than a universal Internet list;
- RFC 9525 SAN-based service identity and obsolete Common Name matching;
- SNI purpose and its distinction from HTTP Host/:authority;
- ALPN and application-protocol selection;
- HSTS vs redirect and preload bootstrap behavior;
- **`.app` TLD HSTS preload** implications: HTTPS is a first-deploy prerequisite for `minttap.app`;
- certificate expiry, clock, hostname, chain, trust-policy, CT and protocol failure categories;
- Certificate Transparency/browser root-program policy as additional modern Web PKI layers;
- edge/CDN TLS and origin TLS as separate connections/security boundaries;
- certificate revocation vs expiration;
- TLS confidentiality limits and metadata boundaries;
- 0-RTT replay caveat and its cross-layer relationship to HTTP method semantics;
- operational diagnosis from URL/DNS/network → TLS negotiation → certificate/service identity → browser policy → ALPN/HTTP → edge-origin hop.

### Important current-policy findings

Authoritative sources checked on 2026-09-14:
- RFC 9846 is now the current TLS 1.3 specification (published July 2026), replacing RFC 8446.
- CA/Browser Forum TLS Baseline Requirements v2.3.0 dated 2026-09-07 limit publicly trusted subscriber certificates issued from 2026-03-15 through 2027-03-14 to **200 days**; the adopted schedule moves to 100 days in 2027 and 47 days in 2029.
- Chrome Root Program Policy v1.8 (2026-02-05) and Mozilla Root Store Policy v3.1 (effective 2026-07-01) continue tightening public Web PKI lifecycle/automation/root-program requirements.
- Google Registry confirms `.app` is included in the HSTS preload list.

These are `CHANGE WATCH` items for implementation time.

## Stage decision

TLS/HTTPS is **closed only for Stage 1 progression**. It will be reopened in:
- Stage 7 — connection/setup performance where material;
- Stage 8 — advanced web security/privacy, HSTS/ECH/cookies/auth/security headers;
- Stage 11 — certificate automation, CDN/origin termination, monitoring, incidents and provider architecture.

## Next major domain

Proceed to **HTML / CSS / JavaScript / DOM / Accessibility Tree — Browser Document & Runtime Foundations**.

The integrated study should cover, from first principles:
- why the Web needed a document language, presentation system and programmable behavior layer;
- HTML parsing and tree construction at conceptual level;
- semantic elements vs visual appearance;
- DOM as browser representation/API rather than the original source text itself;
- CSS cascade/inheritance/box/layout concepts and why separation from markup emerged;
- JavaScript runtime/event model at conceptual level;
- parser-blocking/deferred/module script relationships only to the depth needed for Stage 1;
- DOM mutation and dynamic pages;
- accessibility tree relationship to DOM/semantics, without incorrectly treating it as a direct copy of DOM;
- search engine/assistive technology consumption basics;
- malformed HTML error recovery and browser interoperability concepts;
- progressive enhancement / native semantics as architectural ideas;
- failure diagnosis across HTML/CSS/JS rather than calling every visible defect a “frontend bug.”

Do not split this into micro-reports. Reach a meaningful integrated browser/document checkpoint before reporting.

## Design Studio relationship

The completed TLS block remained primarily network/security foundation, so no immediate Design Studio handoff was necessary.

The next HTML/CSS/JS/DOM/accessibility-tree block creates direct overlap with the Design Studio Web specialist's expected frontend literacy and accessibility implementation scope. Before closing that block, inspect current Web Design progress again and record any reusable implementation/design boundary findings. Do not edit Design Studio specialist canonical files without authorization.

## Important unknown MintTap facts

Do not infer current production state from generic research. Real project work must verify:
- actual `minttap.app` DNS/hosting/CDN topology;
- current public certificate issuer/chain/SAN inventory;
- TLS/ALPN configuration;
- actual renewal/monitoring ownership;
- edge→origin transport/trust model;
- real HTML/CSS/JS stack, framework, rendering strategy and accessibility implementation when the website project starts.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- HTTP Stage 1 core competency is complete.
- HTTPS/TLS/Certificate/Browser Trust Stage 1 core competency is complete.
- Current next major study: **HTML / CSS / JavaScript / DOM / Accessibility Tree foundations**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.