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

Integrated coverage includes build/request/client rendering boundaries; SSR/CSR/SSG/hybrid strategies; hydration; progressive enhancement; browser/runtime/history/cookie/Web Storage/server-state boundaries; RFC 10025 cookie authority; cross-document vs same-document navigation; SPA vs rendering-strategy distinctions; Back/Forward; bfcache; native forms; CDN/edge/static/render/client responsibility boundaries; and rendering/state/navigation failure diagnosis.

### 033 — Stage 1 End-to-End Integration & Competency Review
`033-stage1-end-to-end-integration-competency-review.md`

**STAGE 1 INTEGRATION GATE PASSED.**

The review reconstructs the full path from URL interpretation through DNS, TLS, HTTP/intermediaries/cache, rendering boundaries, HTML→DOM, CSS/resource/layout processing, JavaScript/Web APIs, application state, navigation/history/bfcache and accessibility exposure. It tests representative failures by responsible layer rather than by vague symptom labels and establishes cross-layer invariants such as `DNS success ≠ TLS success`, `HTTP 200 ≠ correct representation`, and `visual correctness ≠ accessibility correctness`.

Primary/current evidence rechecked 2026-09-15 includes WHATWG URL/HTML Living Standards, IETF RFC 9110, IETF RFC 9846, and W3C accessibility mapping guidance. Production MintTap infrastructure facts remain explicitly open until verified in a live project.

## Current curriculum position

**Stage 1 — Web Foundations: COMPLETE at the intended foundation/practitioner curriculum level.**

Next major stage:
- **Stage 2 — Website Anatomy / Content / Information Architecture.**

The first Stage 2 integrated block should establish, from first principles, how a company that develops Apple/Android apps should structure a public website around visitor intent rather than internal organization. It should cover website purpose and archetypes, audience/intent/task modeling, page types, information hierarchy, navigation/wayfinding, labels/taxonomy, app-vs-company-vs-support/governance surfaces, content ownership/lifecycle and one-app→multi-app growth implications.

Existing 002 and 026 should be revisited only where they add validation or advanced synthesis; they should not substitute for a proper Stage 2 first-principles baseline.

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

Studies 031–033 create an outgoing Web Design handoff covering native semantics, DOM/visual/focus-order divergence, accessibility-tree non-equivalence, script/hydration timing, same-document vs cross-document navigation, Back/Forward expectations, deep-link behavior, loading/error/partial states, bfcache restoration, native forms and progressive enhancement. The Stage 1 integration review adds an explicit requirement that future Web Design treat URL/history/navigation/accessibility behavior as product constraints rather than merely implementation details.

Design Studio Web remains pre-baseline in its own canonical status; Web Manager does not edit Design Studio canonical files without authorization.