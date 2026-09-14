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
- `029-http-foundations-history-semantics-evolution.md` — historical/problem/semantic foundation;
- `029a-http-message-anatomy-field-model-framing.md` — detailed message/framing support block retained from the earlier fine-grained cadence;
- `029-http-deep-study-integrated-semantics-caching-negotiation-intermediaries.md` — integrated methods/status/representation/negotiation/cache/intermediary/HTTP2/HTTP3 study;
- `029-http-operational-diagnosis-range-state-boundaries-competency.md` — range requests, cookie/auth boundaries, standardized cache/proxy diagnostics, browser evidence interpretation, living-registry awareness and final Stage 1 competency review.

HTTP Stage 1 competency now covers:
- historical design pressures;
- semantics vs version-specific framing/transport;
- methods/statuses/redirect behavior;
- resource vs representation;
- media types, codings and negotiation;
- caching, validators and conditional requests;
- intermediaries/CDNs/proxies;
- HTTP/1.1, HTTP/2, HTTP/3 and QUIC relationships at Web Manager depth;
- range/partial transfer;
- cookies and authentication as HTTP-boundary concepts;
- operational diagnosis using browser/network/cache/proxy evidence;
- current IANA registry awareness, including the 2026 standardized `QUERY` method.

HTTP will be revisited later in Stage 6/7/8/9/11 for advanced SEO, performance, security/privacy, analytics and operations depth.

## Current curriculum position

**Stage 1 — Web Foundations.**

Next major domain:
- HTTPS / TLS / certificates / browser trust.

This next domain should be studied as one broad integrated professional subject rather than as a chain of micro-reports.

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

No Design Studio handoff was required to close the HTTP Stage 1 core because the work remained protocol/operations foundation. Reconnect when visual/interaction/performance-sensitive browser behavior becomes material.