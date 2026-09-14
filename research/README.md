# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve professional judgment for a real MintTap website/app launch, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Curriculum model

The canonical curriculum is `../LEARNING_ROADMAP.md`.

Learning proceeds systematically from beginner fundamentals to advanced/expert judgment. Existing studies are retained as prior evidence but do not allow missing prerequisites to be skipped.

Major stages:
1. Web Foundations;
2. Website Anatomy / Content / IA;
3. UX & Interaction Foundations;
4. Web Design Literacy;
5. Accessibility;
6. Search / Discovery / Content Quality;
7. Performance / Browser Runtime;
8. Security / Privacy / Trust;
9. Analytics / Experimentation;
10. App-Company Web Strategy / Growth;
11. Web Operations / Platform Architecture;
12. Advanced / Expert Web Management.

Each major topic should mature through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved or not yet validated.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed prior studies 001–026

Studies 001–026 remain retained as prior knowledge spanning launch requirements, IA, privacy/support, content consistency, security, accessibility, localization, SEO, marketing, legal triggers, provider evaluation, release governance and app-company strategy. They are **prior knowledge, not the curriculum order going forward**.

See Git history and the individual files for canonical detail.

## Sequential curriculum studies

- `027-web-foundations-internet-web-client-server-url-origin.md` — **FOUNDATION COMPLETE**. Establishes Internet ≠ Web; client/server as protocol roles; resource vs representation; URL components; host/domain/origin distinctions; scheme+host+port origin identity; same-origin security significance; first-pass navigation flow; and failure-layer diagnosis.
- `028-web-foundations-dns-domain-resolution-hosting-path.md` — **FOUNDATION COMPLETE**. Establishes DNS as a distributed hierarchical typed naming system; root/TLD/domain hierarchy; domain vs zone vs host; delegation; recursive resolver vs authoritative server; recursive vs iterative resolution; root hints; A/AAAA/NS/CNAME/MX/TXT/SOA concepts; TTL/cache and negative caching; registrar/registry/DNS/hosting role separation; and DNS failure-layer diagnosis.

## Current curriculum position

**Stage 1 — Web Foundations**.

027–028 are complete. Next:
- `029` — HTTP request/response, methods, status codes, headers and cache basics;
- `030` — HTTPS, TLS, certificates and browser trust basics;
- `031` — HTML, CSS, JavaScript, DOM and accessibility tree;
- `032` — static/dynamic, SSR/CSR/SSG, browser state/storage/navigation;
- `033` — Stage 1 integration and competency review.

The purpose of revisiting apparently familiar subjects is to establish a complete first-principles mental model rather than relying on isolated advanced knowledge.

## Study quality standard

A substantial study should normally include:
- precise definitions and vocabulary;
- first-principles explanation;
- authoritative or high-quality evidence;
- examples and counterexamples;
- common misconceptions;
- failure modes;
- MintTap relevance;
- boundaries between durable principles and changeable platform behavior;
- a competency/application check when useful.

Implementation experiments are used only when necessary to answer a material factual question. POC work is not the default learning path.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web strategy, platform knowledge, content/IA, measurement and operations stay here first.

Web Manager should become design-literate enough to brief, critique and validate web work, while Design Studio remains the reusable authority for Type, Color, Layout/Interaction and Web Design expertise.
