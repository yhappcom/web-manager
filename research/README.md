# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Each major topic matures through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

### Depth and cadence rule

Large domains are not marked complete after one short survey. Study should follow:

`history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`

Depth remains high, but persistence/reporting is intentionally coarse. Several related learning sub-blocks should normally be integrated into one professional knowledge checkpoint instead of generating one file/report per small concept.

A Stage 1 core may close when it can be explained, diagnosed and applied at the level required by the curriculum; the same domain can and should be reopened later for advanced security, performance, SEO, browser or operations depth.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION/DIRECTION` — project-specific choice or provisional direction.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed prior studies 001–026

Studies 001–026 remain retained as prior knowledge spanning launch requirements, IA, privacy/support, content consistency, security, accessibility, localization, SEO, marketing, legal triggers, provider evaluation, release governance and app-company strategy. They are prior knowledge, not the curriculum order going forward.

## Sequential curriculum studies

### 027 — Web / Internet / URL / Origin
`027-web-foundations-internet-web-client-server-url-origin.md`

**FOUNDATION LAYER COMPLETE.** Internet ≠ Web; client/server roles; resource vs representation; URL; host/domain/origin; origin security significance; failure-layer model.

### 028 — DNS / Domain / Resolution
`028-web-foundations-dns-domain-resolution-hosting-path.md`

**FOUNDATION LAYER COMPLETE.** DNS hierarchy/delegation; resolver/authority; records; TTL/cache; registration/delegation/hosting separation; DNS failure diagnosis.

### 029 — HTTP
**STAGE 1 HTTP CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Supporting/integrated artifacts:
- `029-http-foundations-history-semantics-evolution.md`;
- `029a-http-message-anatomy-field-model-framing.md`;
- `029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md`;
- `029-http-operational-diagnosis-range-state-boundaries-competency.md`.

HTTP Stage 1 competency covers history/semantics, methods/statuses, representations and negotiation, caching/validators, intermediaries, HTTP/1.1–3, QUIC relationships, state/auth boundaries and operational diagnosis. It will be reopened in later SEO/performance/security/operations stages.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage includes secure-channel goals; SSL→TLS history; current TLS 1.3 authority; handshake/record reasoning; symmetric/asymmetric roles; X.509 chain/trust anchors; SAN service identity; SNI/ALPN; HSTS/preload; `.app` implications; CT/root-program policy; edge/origin TLS separation; certificate lifetime automation; and failure diagnosis.

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage includes HTML parsing/DOM; semantic HTML; CSS cascade vs layout; ECMAScript vs Web APIs; script timing; events; native controls; accessibility API mapping; DOM/visual/focus-order distinctions; and layered browser-runtime diagnosis.

### 032 — Application / Rendering / State / Navigation Foundations
`032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage:
- build-time vs request-time vs client-time content production;
- static/dynamic vs interactive/non-interactive distinctions;
- SSR, CSR, SSG and hybrid rendering without framework lock-in;
- hydration and visible-vs-interactive readiness;
- progressive-enhancement reasoning;
- browser/runtime, history, cookie, Web Storage and server-state boundaries;
- **RFC 10025 (July 2026) as the current cookie standard, obsoleting RFC 6265**;
- cross-document vs same-document navigation;
- SPA vs rendering-strategy distinctions;
- browser history and Back/Forward as application behavior;
- bfcache vs HTTP cache vs DNS cache;
- native form submission and enhancement;
- CDN/edge/static/render-service/client responsibility boundaries;
- rendering/state/navigation failure diagnosis;
- explicit handoff to Design Studio Web for navigation/state/loading/resilience design.

Primary/current evidence checked 2026-09-15: WHATWG HTML Living Standard, IETF RFC 10025, MDN rendering/navigation references and web.dev rendering guidance.

## Current curriculum position

**Stage 1 — Web Foundations.**

The major prerequisite blocks 027–032 are now established at Stage 1 foundation/practitioner level.

Next major block:
- **Stage 1 end-to-end integration & competency review** — reconstruct the path from entering `minttap.app` through URL/origin, DNS, TLS, HTTP, rendering/document parsing, CSS/JS runtime, state/navigation and accessibility exposure; diagnose representative failures by responsible layer; identify unresolved prerequisite gaps before Stage 2.

Do not advance to Stage 2 until this integration gate is satisfactory.

## Study quality standard

A substantial study should normally include:
- origin/history and the problem being solved where useful;
- precise definitions and vocabulary;
- first-principles mechanics;
- authoritative standards and current implementation evidence;
- examples/counterexamples and common misconceptions;
- failure modes and operational diagnosis;
- relationships to security, performance, accessibility, SEO, UX and operations where relevant;
- MintTap relevance without inventing project facts;
- durable principles vs changeable implementation behavior;
- competency/application checks.

Implementation experiments are used only when necessary to answer a material factual question. POC work is not the default learning path.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first. Web Manager should become design-literate enough to brief, critique and validate work while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.

Studies 031–032 create an outgoing Web Design handoff covering native semantics, DOM/visual/focus-order divergence, accessibility-tree non-equivalence, script/hydration timing, same-document vs cross-document navigation, Back/Forward expectations, deep-link behavior, loading/error/partial states, bfcache restoration, native forms and progressive enhancement. Web Manager does not edit Design Studio canonical files without authorization.