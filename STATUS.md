# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED WEB CURRICULUM / AUTONOMOUS CONTINUATION ENABLED**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The Web Manager builds professional knowledge for planning, evaluating, launching, operating and improving MintTap's company/app websites. GitHub is canonical long-term memory; chat is temporary working context.

Canonical curriculum: `LEARNING_ROADMAP.md`.

Existing studies 001–026 remain valid prior evidence, but missing prerequisites are now filled sequentially from first principles. Major topics mature through `FOUNDATION → PRACTITIONER → ADVANCED → EXPERT JUDGMENT`.

## Current curriculum position

**Stage 1 — Web Foundations**

### 027 — COMPLETE
`research/027-web-foundations-internet-web-client-server-url-origin.md`

Foundation established:
- Internet and Web are not synonyms: Internet is networking infrastructure; the Web is a service/system built on it;
- HTTP client/server are roles, not reliable synonyms for physical user/server machines;
- resource identity and returned representation are distinct from backend implementation;
- meaningful public URLs should not be designed as accidental mirrors of framework/server internals;
- URL components have distinct functions: scheme, host, port, path, query and fragment;
- for HTTP(S), origin identity is based on scheme + host + port;
- `http://minttap.app`, `https://minttap.app`, `https://www.minttap.app` and a non-default-port variant are distinct origins;
- origin is security-significant because browser same-origin controls use it as an isolation boundary;
- a page-load failure must first be separated into URL, DNS, network, TLS, HTTP, origin/application, representation or browser/runtime layers rather than generically called a server problem.

Primary evidence: IETF RFC 9110 HTTP Semantics and WHATWG URL Living Standard, supplemented by MDN instructional/security references.

No implementation experiment was necessary for 027 because the block establishes standards-based conceptual foundations.

## Stage 1 learning chain

Completed:
- **027** Internet / Web / Client–Server / URL / Origin.

Next:
- **028** DNS / Domains / Resolution / Hosting Path;
- **029** HTTP Request/Response / Methods / Status / Headers / Cache;
- **030** HTTPS / TLS / Certificates / Browser Trust;
- **031** HTML / CSS / JavaScript / DOM / Accessibility Tree;
- **032** Static/Dynamic / SSR/CSR/SSG / State / Storage / Navigation;
- **033** Stage 1 Integration & Competency Review.

Do not skip to later-stage IA/conversion/provider work until the Stage 1 integration review is satisfactory unless a live MintTap project requires an exception.

## 027 competency checkpoint

Before Stage 1 is ultimately closed, the Web Manager must retain the ability to explain:
1. Internet vs Web;
2. client/server as roles;
3. resource vs representation vs implementation;
4. URL component anatomy;
5. host/domain/origin distinctions;
6. why scheme/host/port differences matter;
7. why origin is a security boundary;
8. why website failure diagnosis requires layer separation.

## Existing prior strengths retained

Studies 001–026 provide useful prior coverage in app-launch requirements, multi-app IA, privacy/support/deletion, store↔website consistency, accessibility, localization, SEO, security/hosting, Product Truth, legal-trigger modeling, provider/release governance and visitor-facing strategy. They will be reintegrated at the appropriate curriculum stages rather than driving the sequence.

## Design Studio relationship

No Design Studio handoff was required for 027 because it is protocol/platform foundation. Web Manager continues to use `yhappcom/design-studio` as canonical reusable expertise for Type/Color/Layout-Interaction/Web Design when later stages become visual/interaction-specific.

## Retained but deferred implementation work

Firebase Hosting / Cloudflare Workers research, synthetic POC artifacts and release-governance tooling remain retained as prior knowledge. No additional provider POC/deployment work is part of the general curriculum until Stage 11 or a live project requires it.

## Important unknown MintTap facts

Real project decisions still require evidence for company/legal identity, real app inventory, audience research, acquisition channels, pricing/account model, store assets, verified trust signals, analytics baseline, data flows/legal applicability and actual Apple/Android identifiers. Do not invent these from generic patterns.

## Next action

Proceed to **028 — DNS, Domains, Resolution and Hosting Path** from first principles: namespace/hierarchy, labels/FQDN, resolver vs authoritative DNS, root/TLD/authoritative delegation, A/AAAA/CNAME and relevant record concepts, caching/TTL, DNS vs URL/origin, and how `minttap.app` resolution relates—but is not identical—to hosting.

## Persistence state

- `LEARNING_ROADMAP.md` is the canonical curriculum.
- `research/README.md` indexes staged learning.
- `027` is the first completed sequential Stage 1 study.
- Current next study: **028**.
- This file is the current operational checkpoint.
