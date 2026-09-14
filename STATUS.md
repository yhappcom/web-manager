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

Competency covers history/semantics, message framing, methods/statuses, representations/content negotiation, caching/conditional requests, intermediaries, HTTP/1.1–3/QUIC relationships, range/state/auth boundaries and evidence-led diagnosis.

### 030 — HTTPS / TLS / Certificates / Browser Trust
`research/030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Competency covers secure-channel goals, SSL→TLS evolution, current TLS 1.3 authority (RFC 9846), handshake/record reasoning, symmetric vs asymmetric roles, X.509 chain/trust anchors, SAN identity verification, SNI/ALPN, HSTS/preload, `.app` implications, CT/root-policy layers, edge/origin TLS separation and operational failure diagnosis.

Policy-sensitive findings remain `CHANGE WATCH`, including public certificate lifetime rules and browser root-program requirements.

### 031 — HTML / CSS / JavaScript / DOM / Accessibility Tree
`research/031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Competency established:
- historical reason for separating document structure, presentation and programmability;
- HTML parser/tokenization/tree-construction mental model;
- source HTML vs runtime DOM distinction;
- semantic HTML vs visual appearance;
- DOM as browser object/tree/event model rather than source text;
- CSS cascade/inheritance/value resolution distinct from layout;
- DOM order vs generated boxes/visual order distinctions;
- ECMAScript language vs browser Web APIs;
- parser-blocking/`defer`/`async`/module timing at conceptual level;
- DOM event targets/propagation basics;
- native-element behavior/semantics as browser-platform capabilities;
- accessibility API mapping and why accessibility representation is not a DOM clone;
- accessible name/role/state concepts and ARIA limits;
- layered diagnosis across source/delivery, parsing/DOM, cascade, layout, runtime, events and accessibility exposure;
- progressive-enhancement/native-first reasoning for public app-company pages.

Primary/current evidence checked 2026-09-14: WHATWG HTML and DOM Living Standards, TC39 ECMAScript, W3C CSS modules, Core-AAM/HTML-AAM and W3C APG.

## Design Studio relationship — outgoing handoff now material

Design Studio Web Design remains at **Stage 1 Foundation / not yet baselined**. Its canonical scope explicitly includes semantic HTML, CSS cascade/layout, DOM/events/focus, accessibility implementation and browser validation.

Study 031 establishes several reusable constraints for future Design Studio Web work:
1. native HTML semantics can be visually customized without discarding browser behavior;
2. DOM order, visual order and focus/accessibility order can diverge;
3. replacing native controls with custom widgets transfers keyboard/focus/accessibility implementation burden to the project;
4. accessibility API exposure is not a raw DOM copy, so screenshot/DOM-only QA is insufficient;
5. CSS cascade failure and layout failure are different diagnostic classes;
6. script loading/runtime timing can affect when content/interaction becomes available.

These findings are recorded in Web Manager as an outgoing handoff. No Design Studio canonical file was edited.

## Next major domain

Proceed to **Application / Rendering / State / Navigation Foundations** as the remaining broad Stage 1 prerequisite block before final integration.

Integrated scope:
- static vs dynamic website meanings;
- server-side rendering, client-side rendering and static generation at conceptual level;
- hydration and why server-rendered HTML can still require client runtime activation;
- browser/server/application state boundaries;
- cookie vs Web Storage vs server-session concepts;
- browser navigation/history basics;
- forms and basic input submission flow;
- URL/navigation implications for public content;
- CDN/edge/hosting/deployment vocabulary integration;
- framework-neutral failure diagnosis;
- relationship to SEO, accessibility, performance, offline behavior and operations without prematurely entering later stages.

After that block, perform a **Stage 1 end-to-end competency review**: explain the entire path from entering `minttap.app` through DNS, TLS, HTTP, parsing, styling, runtime interaction, state/navigation and accessibility exposure, and identify the responsible layer for representative failures.

## Important unknown MintTap facts

Do not infer production implementation from generic research. Real project work must verify:
- actual `minttap.app` DNS/hosting/CDN topology;
- real framework/build system;
- rendering strategy (static/SSR/CSR/hybrid);
- component architecture;
- browser/device support matrix;
- cookie/storage/session usage;
- localization implementation;
- analytics/third-party runtime dependencies;
- accessibility testing stack;
- deployment/monitoring ownership.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- HTTP Stage 1 core competency complete.
- HTTPS/TLS/Certificate/Browser Trust Stage 1 core competency complete.
- Browser Document & Runtime Foundations Stage 1 core competency complete.
- Current next major study: **Application / Rendering / State / Navigation Foundations**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.