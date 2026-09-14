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
- Internet vs Web;
- client/server as protocol roles;
- resource vs representation vs backend implementation;
- URL anatomy;
- host/domain/origin distinctions;
- origin as scheme + host + port security boundary;
- page-load failure layer separation.

Primary evidence: IETF RFC 9110 and WHATWG URL Living Standard.

### 028 — COMPLETE
`research/028-web-foundations-dns-domain-resolution-hosting-path.md`

Foundation established:
- DNS is a distributed, hierarchical, typed naming system rather than merely a domain→IP lookup table;
- the namespace is a tree rooted at `.`, with TLD delegation below the root;
- domain, DNS zone and URL host are related but distinct concepts;
- authority is distributed through delegation and referrals;
- recursive resolvers and authoritative servers perform different roles;
- recursive service may answer from cache or pursue resolution, while iterative resolution follows referrals toward authority;
- root hints provide a bootstrap path for recursive resolver operation;
- A, AAAA, NS, CNAME, MX, TXT and SOA records represent different kinds of DNS data;
- an A/AAAA result does not reveal the complete web-hosting topology;
- TTL controls DNS cache lifetime, not a universal exact "propagation time";
- negative answers may also be cached;
- registrar, TLD registry, authoritative DNS operator and hosting provider are separate roles even when one vendor bundles them;
- nameserver delegation changes have a broader potential blast radius than changing one ordinary web record;
- successful DNS resolution does not prove TLS, HTTP, application or browser health.

Primary evidence: RFC 1034, RFC 1035, current DNS terminology RFC 9499, RFC 3596 / STD 88 for AAAA, and IANA root-zone/root-hints material.

No live `minttap.app` DNS inspection was performed or required for this foundation block; actual registrar, delegation, DNSSEC, authoritative provider and record inventory remain real-project facts to verify separately.

## Stage 1 learning chain

Completed:
- **027** Internet / Web / Client–Server / URL / Origin;
- **028** DNS / Domains / Resolution / Hosting Path.

Next:
- **029** HTTP Request/Response / Methods / Status / Headers / Cache;
- **030** HTTPS / TLS / Certificates / Browser Trust;
- **031** HTML / CSS / JavaScript / DOM / Accessibility Tree;
- **032** Static/Dynamic / SSR/CSR/SSG / State / Storage / Navigation;
- **033** Stage 1 Integration & Competency Review.

Do not skip to later-stage IA/conversion/provider work until the Stage 1 integration review is satisfactory unless a live MintTap project requires an exception.

## Stage 1 competency accumulation

Before Stage 1 is closed, the Web Manager must retain the ability to explain and diagnose:

From 027:
1. Internet vs Web;
2. client/server as roles;
3. resource vs representation vs implementation;
4. URL component anatomy;
5. host/domain/origin distinctions;
6. why origin is a security boundary.

From 028:
7. DNS namespace hierarchy and delegation;
8. domain vs zone vs host;
9. recursive resolver vs authoritative server;
10. root/TLD/authoritative resolution path;
11. A/AAAA/NS/CNAME record concepts;
12. TTL/caching and why observed DNS changes are not instant everywhere;
13. registration vs delegation vs authoritative zone data vs hosting;
14. why DNS success/failure must be separated from downstream TLS/HTTP/application behavior.

## Existing prior strengths retained

Studies 001–026 provide useful prior coverage in app-launch requirements, multi-app IA, privacy/support/deletion, store↔website consistency, accessibility, localization, SEO, security/hosting, Product Truth, legal-trigger modeling, provider/release governance and visitor-facing strategy. They will be reintegrated at the appropriate curriculum stages rather than driving the sequence.

## Design Studio relationship

No Design Studio handoff was required for 027–028 because they are protocol/infrastructure foundations. Web Manager continues to use `yhappcom/design-studio` as canonical reusable expertise for Type/Color/Layout-Interaction/Web Design when later stages become visual/interaction-specific.

## Retained but deferred implementation work

Firebase Hosting / Cloudflare Workers research, synthetic POC artifacts and release-governance tooling remain retained as prior knowledge. No additional provider POC/deployment work is part of the general curriculum until Stage 11 or a live project requires it.

## Important unknown MintTap facts

Real project decisions still require evidence for company/legal identity, real app inventory, audience research, acquisition channels, pricing/account model, store assets, verified trust signals, analytics baseline, data flows/legal applicability and actual Apple/Android identifiers. DNS-specific real facts also remain unknown here: current registrar, `.app` delegation details, authoritative DNS provider, record inventory, DNSSEC state and actual hosting mapping.

Do not invent these from generic patterns.

## Next action

Proceed to **029 — HTTP Request/Response, Methods, Status Codes, Headers and Caching Basics** from first principles. Build the model of what an HTTP message represents after the client has a path to the target authority: request method/target/fields/content, response status/fields/content, safe/idempotent semantics, major status-code classes, redirects, content negotiation/media type basics, and HTTP caching distinct from DNS caching.

## Persistence state

- `LEARNING_ROADMAP.md` is the canonical curriculum.
- `research/README.md` indexes staged learning.
- `027` and `028` are complete sequential Stage 1 studies.
- Current next study: **029**.
- This file is the current operational checkpoint.
