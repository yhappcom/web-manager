# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Each major topic matures through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

**Depth correction:** a large domain is no longer marked complete after one short survey. Study should follow `history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment`. A topic can remain active across multiple research blocks.

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

- `027-web-foundations-internet-web-client-server-url-origin.md` — **FOUNDATION LAYER COMPLETE**. Internet ≠ Web; client/server roles; resource vs representation; URL; host/domain/origin; origin security significance; failure-layer model.
- `028-web-foundations-dns-domain-resolution-hosting-path.md` — **FOUNDATION LAYER COMPLETE**. DNS hierarchy/delegation; resolver/authority; records; TTL/cache; registration/delegation/hosting separation; DNS failure diagnosis.
- `029-http-foundations-history-semantics-evolution.md` — **HTTP DEEP STUDY ACTIVE — FOUNDATION HISTORY/SEMANTICS BLOCK COMPLETE**. Traces HTTP from early Web/HTTP/0.9 through 1.0/1.1/2/3; separates durable semantics from version-specific framing/transport; introduces statelessness, safe/idempotent/cacheable semantics, status/field meaning, caching/freshness/validation, intermediaries and version-evolution design pressures.

## Current curriculum position

**Stage 1 — Web Foundations / HTTP domain active.**

Do not move directly to TLS merely because the first HTTP file exists. Required HTTP continuation:
- **029A** message anatomy and field model;
- **029B** methods and status semantics in depth;
- **029C** representations, media types and content negotiation;
- **029D** caching and conditional requests in depth;
- **029E** intermediaries, persistent connections, HTTP/2 and HTTP/3 mechanics;
- **029F** operational diagnosis using representative HTTP exchanges/network evidence.

Then continue dedicated TLS/browser foundation blocks. Numbering may be normalized later; conceptual completeness matters more than file count.

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
