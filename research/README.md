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

Integrated coverage:
- confidentiality, integrity and authentication as distinct TLS goals;
- SSL → TLS history and TLS 1.0/1.1 deprecation;
- current TLS 1.3 authority moved from RFC 8446 to **RFC 9846 in July 2026**;
- TLS 1.2 → 1.3 design changes, handshake and record roles;
- asymmetric authentication/key establishment vs symmetric traffic protection;
- X.509 root/intermediate/leaf and certification-path mental model;
- trust anchors as relying-party policy, not a universal Internet list;
- RFC 9525 SAN/service-identity verification and obsolete CN matching;
- SNI and ALPN roles and their protocol-layer boundaries;
- HSTS and preload behavior;
- `minttap.app` consequence of the `.app` TLD being HSTS preloaded;
- certificate expiration, revocation, chain, clock, hostname and trust-policy failure classes;
- Certificate Transparency and browser/root-program policy as modern Web PKI layers;
- CDN edge TLS vs origin TLS as separate connections/security boundaries;
- current CA/B certificate-lifetime reduction schedule and the resulting need for automation;
- integrated TLS failure diagnosis before HTTP/application analysis.

Current policy-sensitive findings include CA/Browser Forum TLS BR v2.3.0 (7 Sep 2026), which limits publicly trusted subscriber certificates issued from 15 Mar 2026 through 14 Mar 2027 to 200 days and already schedules further reductions to 100 days in 2027 and 47 days in 2029.

TLS/Web PKI will be revisited in Stage 8 and Stage 11 for advanced security/privacy and operations depth.

### 031 — Browser Document & Runtime Foundations
`031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Integrated coverage:
- why HTML, CSS and JavaScript evolved as separate but interacting layers;
- WHATWG HTML parsing: tokenization/tree construction into the runtime DOM;
- source HTML vs parsed/mutated DOM;
- semantic HTML vs visual appearance;
- DOM as browser object/tree/event model rather than source text;
- CSS cascade/inheritance as value-resolution systems distinct from layout;
- DOM order vs generated boxes/visual order distinctions;
- ECMAScript language vs browser Web APIs;
- script blocking/`defer`/`async`/module timing at Stage 1 depth;
- DOM event targets and propagation concepts;
- native element semantics/interaction as browser-platform capabilities;
- accessibility API exposure and why the accessibility representation is not a direct DOM clone;
- accessible name/role/state concepts and ARIA's limits;
- layered diagnosis across delivery, parser/DOM, cascade, layout, JS runtime, events and accessibility exposure;
- progressive-enhancement/native-first reasoning for resilient public app-company pages;
- explicit handoff boundaries with Design Studio Web Design.

Current standards/evidence checked 2026-09-14 include WHATWG HTML/DOM Living Standards, TC39 ECMAScript, W3C CSS modules, Core-AAM 1.2 and HTML-AAM 1.0 drafts, and W3C APG guidance.

This domain will be reopened later for deeper responsive CSS/layout, accessibility, browser-runtime performance and framework/component implementation.

## Current curriculum position

**Stage 1 — Web Foundations.**

Next major domain:
- **application/rendering/state/navigation foundations**: static vs dynamic, SSR/CSR/SSG, hydration, browser/server state boundaries, cookies/Web Storage/session concepts, forms/navigation/history, CDN/edge/hosting vocabulary integration, followed by Stage 1 end-to-end competency review.

The next domain should again be studied as one broad integrated professional subject rather than a chain of micro-reports.

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

No immediate Design Studio handoff was required to close HTTP or TLS foundations. Study 031 now creates an explicit outgoing handoff for future Web Design work: native semantics, DOM/visual/focus-order divergence, accessibility-tree non-equivalence, native-vs-custom control costs, cascade-vs-layout diagnosis and script-timing consequences should be integrated when Design Studio begins real web implementation/design validation. Web Manager does not edit Design Studio canonical files without authorization.