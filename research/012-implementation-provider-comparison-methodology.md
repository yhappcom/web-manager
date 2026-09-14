# 012 — Implementation / Hosting Provider Comparison Methodology

Status: **FOUNDATION STUDY / PRELIMINARY CANDIDATE ASSESSMENT; NO FINAL PROVIDER SELECTED**  
Research date: **2026-09-14**

## Question

What implementation and hosting architecture best fits `minttap.app` now that the product, compliance, localization, SEO, accessibility, marketing and operational requirements from Studies 002–011 are known?

The goal is not to choose a fashionable framework. The goal is to select the smallest production architecture that satisfies MintTap's real contracts and remains easy to validate, roll back and operate.

---

## RELATED DOMAIN CHECK

### Existing Web Manager evidence

The provider must satisfy all relevant prior requirements, especially:
- Study 002: durable multi-app URL hierarchy;
- Study 003: public Privacy/Support/Deletion surfaces;
- Study 005: exact `.well-known` routing, HTTPS, headers, caching, security and rollback;
- Study 006: semantic/accessibility production requirements;
- Study 007: locale-specific URLs;
- Studies 008–009: canonical/search/social output;
- Study 011: deployment validation, monitoring and operational continuity.

### Design Studio

Web Design remains responsible for actual browser/page validation and has not yet established a substantive W### baseline. Therefore this study selects an **implementation architecture envelope**, not a visual system or final component framework.

Type/Layout/Color dependencies remain implementation validation inputs after a real site exists.

---

# Architecture principle — static-first unless a user task requires server execution

## SYNTHESIS

Current planned public surfaces are primarily:
- company/app information;
- screenshots and product evidence;
- support/help;
- privacy/terms;
- account-deletion instructions or entry points;
- store links;
- machine-readable verification files;
- sitemap/robots/metadata.

These are overwhelmingly publish/read workloads. They do not inherently require server-side rendering, a database-backed CMS, a persistent application server or runtime JavaScript.

### MINTTAP DECISION

Default architecture direction:

**Git-versioned content/data → build-time generation/static files → global HTTPS/CDN hosting → small isolated serverless/API functions only when a real workflow requires them.**

Examples of future functions that may justify dynamic execution:
- authenticated account-deletion request submission;
- support/contact form with abuse controls;
- App Store Connect webhook receiver;
- internal monitoring/operations endpoints.

Those functions do not require the entire public website to become dynamically rendered.

### Why this matters

Static-first reduces:
- runtime failure modes;
- server attack surface;
- dependency on database availability;
- cache invalidation complexity;
- framework/runtime upgrade pressure on legal/support pages;
- difficulty serving exact machine files;
- rollback uncertainty.

It also improves determinism for:
- canonical/hreflang/meta generation;
- accessibility test fixtures;
- screenshot/content review;
- deployment diffing;
- exact response/file validation.

This is a MintTap project judgment, not a universal rule for websites.

---

# Provider hard gates

A candidate cannot advance if it cannot support all applicable hard gates.

## G1 — domain / TLS
- `minttap.app` apex custom domain;
- managed valid TLS;
- stable production hostname;
- deliberate `www`/alternate-host redirect policy.

## G2 — exact machine endpoints
Must be able to directly serve:
- `/.well-known/apple-app-site-association`;
- `/.well-known/assetlinks.json`;
- `/app-ads.txt` when used;
with exact path/status/content-type/cache behavior and no unintended canonical-host redirect on hosts used for app association.

## G3 — response control
- custom security/cache/content-type headers;
- route-specific rules;
- redirects and rewrites without interfering with machine endpoints.

## G4 — release safety
- preview/test deployment;
- immutable or traceable versions;
- fast rollback to known-good deployment;
- Git/CI-compatible deployment.

## G5 — static/search/localization correctness
- arbitrary static HTML/files;
- locale path structure (`/ko`, `/en`);
- custom 404;
- sitemap/robots;
- canonical/hreflang/JSON-LD/Open Graph generation;
- no forced SPA fallback across all routes unless explicitly configured.

## G6 — operational capability
- deploy/log/history visibility;
- monitoring integration or inspectable HTTP behavior;
- access/role continuity;
- secrets outside repository for any dynamic functions.

---

# Weighted comparison criteria

After hard gates pass, score candidates 0–5 on:

| Area | Weight | Meaning |
| --- | ---: | --- |
| Operational simplicity | 20 | few moving parts, deterministic deploy/rollback |
| Exact HTTP/routing control | 15 | machine endpoints, headers, redirects, caching |
| Preview + rollback | 15 | safe review and fast recovery |
| Static-first fit | 10 | efficient uncomplicated static publishing |
| Dynamic escape hatch | 10 | optional forms/webhooks/API without replatforming whole site |
| Observability/integration | 10 | logs, deployment history, monitoring hooks |
| Domain/DNS flexibility | 10 | custom apex, migration flexibility, provider lock implications |
| Git/CI workflow | 5 | reviewable content and automated deploys |
| Cost predictability | 5 | early-stage sustainable baseline; re-evaluate with real traffic |

Weights are MintTap Foundation defaults and may change when real site traffic/dynamic needs exist.

---

# Candidate A — Firebase Hosting

## SOURCE

Firebase Hosting provides:
- static asset hosting on a global CDN;
- SSL by default;
- custom domains with managed certificate provisioning/reprovisioning;
- custom headers, caching, redirects and rewrites;
- custom 404 pages;
- preview channels / GitHub preview workflows;
- release history and rollback to previous versions;
- optional rewrites to Cloud Functions or Cloud Run for dynamic behavior.

Primary sources:
- https://firebase.google.com/docs/hosting
- https://firebase.google.com/docs/hosting/custom-domain
- https://firebase.google.com/docs/hosting/full-config
- https://firebase.google.com/docs/hosting/manage-hosting-resources
- https://firebase.google.com/docs/hosting/use-cases

## FIT

Strengths for MintTap:
- very direct fit for static-first public site;
- exact file and route configuration available in `firebase.json`;
- preview channels + rollback align well with Study 011;
- dynamic functions can remain isolated;
- managed TLS/CDN reduces infrastructure burden.

Watch items:
- preview URLs are public if known and must be treated as non-secret;
- rewrite/rule ordering requires explicit tests around `.well-known` paths;
- full-stack framework helpers can create Functions/runtime complexity that MintTap may not need.

### Preliminary score direction

**Strong Foundation candidate.**

Do not choose Firebase App Hosting merely because it is newer; App Hosting/full-stack runtime should be justified by an actual SSR/server requirement.

---

# Candidate B — Cloudflare Workers + Static Assets

## SOURCE

Cloudflare now states that Workers supports most Pages use cases with a broader feature set and recommends new projects start with Workers. Workers Static Assets supports static HTML/assets, `_headers` and `_redirects`, Worker code as an optional dynamic layer, versioned deployments and rollback.

Cloudflare Workers custom domains issue certificates and DNS records automatically within a Cloudflare zone. Cloudflare's migration documentation notes that Workers custom domains require nameservers managed by Cloudflare.

Primary sources:
- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/static-assets/headers/
- https://developers.cloudflare.com/workers/static-assets/redirects/
- https://developers.cloudflare.com/workers/versions-and-deployments/
- https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/

## FIT

Strengths:
- excellent exact HTTP/cache/header/routing control;
- static assets and dynamic edge logic can be deployed as one controlled unit;
- strong version/rollback model;
- suitable for future lightweight forms/webhooks/edge behavior.

Watch items:
- adopting Workers custom domain means `minttap.app` DNS/nameservers move into Cloudflare control;
- more platform primitives and Worker behavior create more operational surface than plain static Firebase Hosting;
- if Worker code handles routes, `_headers`/`_redirects` behavior differs from pure static asset handling and must be tested explicitly.

### Preliminary score direction

**Strong candidate where DNS/control/edge flexibility is valued.**

It may be more capability than MintTap needs for a first static company site.

---

# Candidate C — Vercel

## SOURCE

Vercel supports custom domains, managed SSL verification, custom response headers/configuration, Git-triggered deployments, deployment inspection and production rollback. Rollback occurs at routing level and can rapidly restore an earlier deployment.

Primary sources:
- https://vercel.com/docs/domains/set-up-custom-domain
- https://vercel.com/docs/headers
- https://vercel.com/docs/deployments/overview
- https://vercel.com/docs/deployments/rollback-production-deployment

## FIT

Strengths:
- strong preview/deploy workflow;
- excellent fit if MintTap later explicitly selects Next.js or another Vercel-optimized framework;
- custom domains, headers and rollback satisfy core hosting gates.

Watch items:
- platform value is strongest when using framework/runtime features MintTap has not yet shown it needs;
- Vercel recommends `www` as the primary domain for maximum routing flexibility, while MintTap's current canonical direction is apex `https://minttap.app/`; apex is supported, but final host choice must remain a MintTap decision rather than inherit provider preference;
- avoid adopting framework/runtime complexity solely to justify the hosting provider.

### Preliminary score direction

**Technically capable, but not currently the clearest minimal-fit winner.**

Promote if future web design/content requirements justify Next.js/SSR/server rendering or Vercel-specific workflows.

---

# Candidate D — Netlify

## SOURCE

Netlify supports custom response headers through `_headers` or `netlify.toml`, redirects/rewrites, deployment contexts, custom-domain routing and atomic deployment rollback by republishing a previous successful deploy.

Primary sources:
- https://docs.netlify.com/manage/routing/headers/
- https://docs.netlify.com/manage/routing/redirects/overview/
- https://docs.netlify.com/manage/deploys/manage-deploys-overview/

## FIT

Strengths:
- mature static-site deployment model;
- strong file/config-based headers and redirects;
- simple instantaneous rollback to retained atomic deployments;
- suitable for Git-backed static generation.

Watch items:
- headers on function/SSR responses need to be returned by those functions rather than relying only on `_headers`;
- Pretty URLs / routing defaults must be validated against MintTap's exact canonical slash policy and `.well-known` machine routes;
- currently no unique MintTap requirement makes Netlify clearly superior to Firebase Hosting or Cloudflare Workers.

### Preliminary score direction

**Viable, but presently secondary unless its workflow/cost/team fit becomes materially better.**

---

# Preliminary comparison

Scores are **Foundation judgments**, not benchmark results. `5 = strongest fit`, `3 = adequate`, `1 = material concern`.

| Criterion | Firebase Hosting | Cloudflare Workers | Vercel | Netlify |
| --- | ---: | ---: | ---: | ---: |
| Operational simplicity | 5 | 3 | 4 | 4 |
| Exact HTTP/routing control | 4 | 5 | 4 | 4 |
| Preview + rollback | 5 | 5 | 5 | 5 |
| Static-first fit | 5 | 5 | 4 | 5 |
| Dynamic escape hatch | 4 | 5 | 5 | 4 |
| Observability/integration | 4 | 5 | 5 | 4 |
| Domain/DNS flexibility | 4 | 3 | 4 | 4 |
| Git/CI workflow | 5 | 4 | 5 | 5 |
| Cost predictability | 4* | 4* | 3* | 3* |

`*` Cost scores are intentionally low-confidence and must be recalculated from current plans/traffic when implementation begins. Pricing is a CHANGE WATCH item.

Using the Foundation weights above, Firebase Hosting and Cloudflare Workers form the strongest current shortlist. This table is not permission to skip a proof-of-concept.

---

# Framework / content architecture decision

## MINTTAP DECISION — content source should be Git-reviewable

For Foundation implementation, company/app/legal/support content should be representable as version-controlled content/configuration rather than requiring a proprietary visual CMS as the sole canonical source.

Reasons:
- Product Truth / Claim / Locale review can be diffed;
- policy pages have history;
- deployment revision can be linked to content revision;
- rollback includes content/config;
- structured data and metadata can be generated from the same records.

A CMS may later be added as an authoring interface if it preserves review/version guarantees.

## MINTTAP DECISION — prefer SSG/static output over universal SSR by default

Framework category priority:
1. static HTML / lightweight static site generator;
2. static-capable component framework/SSG if richer components justify it;
3. SSR/full-stack framework only after a concrete server-rendering requirement exists.

Do not select Next.js, Nuxt, Remix or another full-stack framework solely because it is popular or because a hosting vendor optimizes for it.

### Required static-generator capabilities

- localized route generation;
- content collections/data validation;
- accessible semantic templates;
- per-page metadata/canonical/hreflang/JSON-LD/Open Graph;
- deterministic sitemap/robots output;
- raw static files in `.well-known` and root;
- build-time broken-link/schema checks;
- minimal client JavaScript for informational pages;
- straightforward unit/browser/a11y testing.

Exact generator selection remains OPEN until Design Studio/Web page requirements and authoring workflow are known.

---

# Provider proof-of-concept gate

Before selecting production hosting, build the same minimal specimen on the top two candidates.

Required specimen:
- `/ko/` + `/en/` home;
- one `/apps/example/` app page in both locales;
- Privacy + Support + Account Deletion pages;
- `/.well-known/apple-app-site-association`;
- `/.well-known/assetlinks.json`;
- `/app-ads.txt` sample;
- `robots.txt`, `sitemap.xml`;
- custom 404;
- security headers;
- canonical/hreflang/Open Graph;
- one controlled redirect;
- preview deployment;
- rollback test.

Test assertions:
- exact status/content-type/redirect rules;
- no machine endpoint accidentally redirected;
- apex/custom-domain behavior;
- staging/preview noindex protection;
- deploy → smoke validation;
- rollback → smoke validation;
- Korean/English static route integrity;
- accessibility smoke test.

Only after this transfer test should a provider become **SELECTED**.

---

# Current recommendation

## Preferred architecture

**Static-first, Git-versioned, CDN-hosted site with isolated dynamic functions only when required.**

## Provider shortlist

1. **Firebase Hosting** — current simplest strong fit.
2. **Cloudflare Workers + Static Assets** — strongest control/flexibility alternative, with Cloudflare DNS ownership as a deliberate trade-off.

Keep Vercel and Netlify as viable alternatives. Do not discard them permanently; re-evaluate if framework/team/runtime requirements change.

## NOT YET DECIDED

- final provider;
- static site generator/framework;
- CMS;
- monitoring vendor;
- dynamic-form/webhook backend;
- DNS registrar/authoritative provider;
- analytics stack.

---

# HANDOFFS TO DESIGN STUDIO

## Web Design

Before framework selection, provide concrete requirements for:
- page/component complexity;
- interactive galleries/forms/navigation;
- responsive states;
- animation/runtime behavior;
- whether any page genuinely needs server rendering.

Web Design findings may change the framework category but should not silently override the operational hard gates.

## Type / Layout / Color

The provider POC will create the first real-browser MintTap specimen suitable for:
- Korean/English fallback/wrapping;
- 320px/200% stress;
- focus/navigation states;
- real surface/contrast/theme checks.

This is an opportunity for cross-specialist transfer validation.

---

# OPEN / CHANGE WATCH

- current provider plan/pricing/limits at implementation time;
- exact log retention/observability needs;
- organization/team access controls on chosen provider plan;
- actual DNS ownership strategy;
- exact dynamic workflows;
- selected SSG/framework and dependency maintenance burden;
- whether production analytics/cookie consent changes static architecture requirements;
- vendor product direction (for example Cloudflare's shift from Pages toward Workers);
- Design Studio Web requirements once W### work exists.

## Foundation conclusion

MintTap should **not** start website implementation by selecting a framework and then bending requirements around it.

The decision sequence is:

**Studies 002–011 contracts → static/dynamic boundary → provider hard gates → weighted shortlist → identical POC on top candidates → browser/ops/design validation → provider/framework selection.**

At current evidence level, **static-first + Firebase Hosting or Cloudflare Workers** is the highest-confidence implementation envelope, with Firebase Hosting currently the simpler default and Cloudflare Workers the higher-control alternative.