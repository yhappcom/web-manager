# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**
Last sync: 2026-09-15
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

### 030 — HTTPS / TLS / Certificates / Browser Trust
`research/030-https-tls-certificates-browser-trust-integrated-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 031 — HTML / CSS / JavaScript / DOM / Accessibility Tree
`research/031-browser-document-runtime-html-css-js-dom-accessibility-tree-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

### 032 — Application / Rendering / State / Navigation
`research/032-application-rendering-state-navigation-foundations.md`

**STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT PASSED.**

Competency established:
- build-time, request-time and client-time rendering as separate production points;
- static/dynamic distinct from interactive/non-interactive;
- SSR/CSR/SSG/hybrid strategies without framework dependence;
- hydration and visible-vs-interactive readiness;
- progressive-enhancement reasoning for resilient public surfaces;
- DOM/runtime, session-history, cookie, Web Storage, server-session and persistent backend state boundaries;
- cookie standard authority updated: **RFC 10025 (July 2026) obsoletes RFC 6265**;
- cross-document vs same-document navigation;
- SPA vs rendering-strategy distinction;
- Back/Forward/session history as application correctness;
- bfcache vs HTTP cache vs DNS cache;
- native forms/submission as browser capability;
- CDN/edge/static artifact/render service/client responsibility separation;
- rendering/state/navigation failure diagnosis.

Primary/current evidence checked 2026-09-15: WHATWG HTML Living Standard, IETF RFC 10025, MDN rendering/navigation references and web.dev rendering guidance.

## Design Studio relationship — outgoing handoff expanded

Design Studio Web Design remains at **Stage 1 Foundation / not yet baselined** and explicitly owns web navigation, responsive systems, state presentation, forms, browser-native behavior and accessibility implementation.

Studies 031–032 create reusable constraints for future Web Design work:
1. native semantics can be styled without discarding browser behavior;
2. DOM, visual, focus and accessibility order can diverge;
3. visible server-rendered content can precede hydrated/interactable state;
4. same-document navigation still needs coherent URL/history/Back behavior;
5. deep-link behavior is a product/design constraint, not just routing configuration;
6. server/client boundaries create distinct loading, partial and error states;
7. bfcache can restore prior runtime/page state independently of ordinary HTTP caching;
8. native forms/navigation should be considered before replacing them with client-only behavior;
9. storage/session expiry or disagreement can generate user-visible state transitions;
10. progressive enhancement/resilience should be part of app-company public web design judgment.

These are recorded as outgoing handoff evidence. No Design Studio canonical file was edited.

## Stage 1 remaining gate

The broad prerequisite blocks 027–032 are now established. **Do not start Stage 2 yet.**

Next perform a single end-to-end Stage 1 integration & competency review covering:

1. user enters `https://minttap.app/...`;
2. URL/origin interpretation;
3. DNS resolution/delegation;
4. network/TLS establishment and certificate/service identity;
5. HTTP request/response, intermediaries, cache and status semantics;
6. build/request/client rendering boundary;
7. HTML parsing → DOM;
8. CSS cascade/layout and resource loading;
9. JavaScript/Web API/runtime interaction;
10. state/cookie/storage/session boundaries;
11. navigation/history/bfcache;
12. accessibility exposure;
13. representative failure diagnosis across those layers;
14. identification of any Stage 1 gaps before promotion to Stage 2.

The review must demonstrate connected reasoning, not a glossary recap.

## Important unknown MintTap facts

Do not infer production implementation from generic research. Real project work must verify:
- actual `minttap.app` DNS/hosting/CDN topology;
- real framework/build system;
- rendering strategy by route;
- component architecture;
- browser/device support matrix;
- cookie/storage/session usage;
- whether website authentication/account functionality exists;
- localization implementation;
- analytics/third-party runtime dependencies;
- accessibility testing stack;
- deployment/monitoring ownership.

## Persistence state

- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- Stage 1 cores complete: 027–032.
- Current next major work: **Stage 1 end-to-end integration & competency review**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.