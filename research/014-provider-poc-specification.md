# 014 — Provider POC Specification: Firebase Hosting vs Cloudflare Workers

Status: **FOUNDATION SPECIFICATION / NOT YET EXECUTED**  
Research date: **2026-09-14**  
Candidates: **Firebase Hosting** vs **Cloudflare Workers + Static Assets**

## Question

What exact, reproducible proof-of-concept should MintTap run so provider selection is based on observed production-contract behavior rather than documentation comparison or preference?

Study 012 established the provider shortlist. This study defines the **same test artifact, same HTTP contract, same browser/accessibility checks and same rollback exercise** for both candidates.

No provider is selected by this document.

---

## RELATED DOMAIN CHECK

### Existing Web Manager evidence

The POC must exercise:
- Study 002 — stable multi-app IA;
- Study 003 — Privacy / Support / Account Deletion;
- Study 005 — exact machine endpoints, headers, redirects, caching, TLS;
- Study 006 — accessibility baseline;
- Study 007 — Korean/English locale URLs;
- Studies 008–009 — canonical/hreflang/search/social metadata;
- Study 011 — preview, release, rollback, monitoring;
- Study 013 — legal surfaces and provider/data-location review boundaries.

### Design Studio Web

Current Web Design status remains Foundation / `W001` not yet established. Therefore the POC intentionally uses a **minimal neutral visual specimen** rather than pretending to be the final MintTap design.

The POC is an implementation/validation fixture that future Web Design can restyle while retaining the tested contracts.

### Type / Layout / Interaction / Color

The POC must be suitable for later cross-specialist transfer validation:
- Korean/English wrapping/fallback;
- 320 CSS px / 200% text enlargement;
- focus/order/navigation;
- semantic state/contrast;
- legal/support long copy.

---

# 1. POC PRINCIPLE — SAME BUILD ARTIFACT FIRST

## MINTTAP DECISION

Provider comparison is invalid if Firebase and Cloudflare run materially different application stacks.

The first POC must use one provider-neutral static build artifact. Provider-specific files/configuration may control hosting behavior, but the HTML/CSS/content corpus must be identical.

Preferred shape:

```text
poc/
  source-or-fixture/
  dist/                    # identical deployable static output
    index.html
    ko/
      index.html
      apps/
        example/
          index.html
          support/index.html
          privacy/index.html
          account-deletion/index.html
    en/
      index.html
      apps/
        example/
          index.html
          support/index.html
          privacy/index.html
          account-deletion/index.html
    .well-known/
      apple-app-site-association
      assetlinks.json
    app-ads.txt
    robots.txt
    sitemap.xml
    404.html
    assets/
      site.<content-hash>.css
      sample-app.<content-hash>.svg
```

Provider-specific configuration lives outside the content tree or is excluded from artifact-equivalence hashing where unavoidable.

### VALIDATION

Compute a deterministic manifest for all common `dist/` files:
- relative path;
- byte length;
- SHA-256.

Both providers must receive the same common-file manifest.

---

# 2. TEST DATA MUST BE SYNTHETIC

## MINTTAP DECISION

The POC must contain **no real user data, real account identifiers, real legal-person data not already approved for public use, real publisher IDs or production signing fingerprints unless explicitly authorized for a live verification test**.

Use obvious placeholders such as:
- `TEAMID.com.example.minttap.poc`;
- fake SHA-256 fingerprint;
- `pub-0000000000000000`;
- sample support email like `support@example.invalid` in non-public/local artifacts.

### Reason

The POC tests hosting behavior, not production legal/store association.

A later **production association validation** must replace placeholders and rerun the relevant assertions.

---

# 3. HUMAN-FACING FIXTURE

## Required pages

### Root

`/`
- neutral language entry/POC index only;
- links to `/ko/` and `/en/`;
- no automatic IP/language redirect.

This avoids prematurely deciding Study 007's final root strategy.

### Localized home

`/ko/`
`/en/`

Must contain:
- correct `<html lang>`;
- one clear `<main>`;
- logical H1;
- link to localized app page;
- language-switch link to equivalent page;
- footer links to localized support/privacy example routes.

### Localized app page

`/ko/apps/example/`
`/en/apps/example/`

Must exercise:
- title/meta description;
- self canonical;
- reciprocal hreflang;
- Open Graph title/description/url/image;
- one screenshot/evidence placeholder;
- one store CTA placeholder link;
- links to Support / Privacy / Account Deletion;
- visible qualification/limitation text;
- semantic headings.

### Support

Must include:
- FAQ headings;
- contact route placeholder;
- success/error status specimen that can be exposed semantically;
- long Korean/English strings for reflow stress.

### Privacy

Must include:
- long-form sections;
- in-page heading structure;
- processor/retention example table or definition list;
- rights-request link placeholder;
- no legal claim that the sample text is production-compliant.

### Account deletion

Must include:
- scope explanation;
- irreversible consequence sample;
- Cancel and Continue/Delete sample controls;
- safe initial focus behavior if dialog specimen is used;
- no real deletion backend.

---

# 4. MACHINE ENDPOINT CONTRACT

## AASA

Path:
`/.well-known/apple-app-site-association`

Current Apple guidance requires:
- HTTPS with valid certificate;
- exact no-extension file;
- no redirects;
- valid AASA JSON for the intended associated-domain service.

Apple's current associated-domain documentation states no redirect and explains that Apple-managed CDN fetches the file; devices check updates approximately weekly after installation. Archived Apple universal-link guidance specifies JSON / `application/json` for modern iOS.

Primary sources:
- https://developer.apple.com/documentation/xcode/supporting-associated-domains
- https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links
- https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html

### POC assertions

- `AASA-01`: HTTPS GET returns `200`.
- `AASA-02`: redirect count = `0`.
- `AASA-03`: body parses as JSON.
- `AASA-04`: `Content-Type` is `application/json` in the POC contract.
- `AASA-05`: random User-Agent still receives `200` body, not bot block.
- `AASA-06`: body byte hash equals common fixture.

## Android Digital Asset Links

Path:
`/.well-known/assetlinks.json`

Android's current documentation explicitly requires:
- HTTPS;
- `Content-Type: application/json`;
- no redirect;
- public access.

Primary source:
- https://developer.android.com/training/app-links/configure-assetlinks

### POC assertions

- `DAL-01`: HTTPS GET returns `200`.
- `DAL-02`: `Content-Type` starts with `application/json`.
- `DAL-03`: redirect count = `0`.
- `DAL-04`: body parses as JSON array.
- `DAL-05`: file reachable by generic crawler User-Agent.
- `DAL-06`: body byte hash equals fixture.

## app-ads.txt

Path:
`/app-ads.txt`

Current AdMob guidance:
- file lives at developer website root;
- crawler must receive HTTP `200`;
- file must remain crawlable;
- AdMob also attempts HTTP and HTTPS retrieval and warns that HTTPS 40X can purge previously crawled entries.

Primary sources:
- https://support.google.com/admob/answer/9363762
- https://support.google.com/admob/answer/9679128
- https://developers.google.com/admob/android/next-gen/app-ads

### POC assertions

- `ADS-01`: HTTPS request returns `200`.
- `ADS-02`: body is UTF-8 plain text and contains only synthetic sample rows.
- `ADS-03`: `Google-adstxt` is not blocked by robots rules.
- `ADS-04`: HTTP behavior is documented; if global HTTP→HTTPS redirect is used, final HTTPS response must be `200` and provider behavior must be recorded.
- `ADS-05`: root path is not rewritten to HTML/app shell.

---

# 5. HTTP / URL NORMALIZATION CONTRACT

## Canonical host direction

POC custom-domain phase uses:
`https://minttap.app` only **when authorized to connect the real domain**.

Before then, use candidate-owned test hostnames and treat custom-domain assertions as pending.

Do not alter production DNS merely to run a documentation-level POC.

## Redirect fixture

Create one explicit retired route:
`/old-app/` → `/en/apps/example/` using `301`.

Assertions:
- `REDIR-01`: exactly one redirect;
- `REDIR-02`: correct `Location`;
- `REDIR-03`: destination `200`;
- `REDIR-04`: machine endpoints do not inherit this or any catch-all redirect.

## Trailing slash

The POC must choose one deterministic page convention and test it identically.

Foundation direction for fixture:
- directory-style human page URLs end with `/`;
- exact machine-file URLs do not gain `/`.

Assertions:
- `URL-01`: canonical HTML uses chosen slash form;
- `URL-02`: alternate form behavior is recorded (redirect or provider-native behavior);
- `URL-03`: sitemap/internal links use final canonical form;
- `URL-04`: `.well-known` files never receive slash normalization redirect.

---

# 6. RESPONSE HEADER CONTRACT

## Security baseline

For human HTML responses, POC target headers include:
- `X-Content-Type-Options: nosniff`;
- explicit `Referrer-Policy`;
- explicit `Permissions-Policy`;
- a deliberately minimal test `Content-Security-Policy` compatible with the static fixture;
- HSTS only in the **custom-domain production-like stage**, not blindly on temporary vendor preview hosts.

CSP is not considered production-final from the POC; the goal is to prove provider control and detect provider-specific conflict.

## Cache classes

### HTML / legal / metadata
Target:
`Cache-Control: public, max-age=0, must-revalidate`
or a semantically equivalent conservative policy documented per provider.

### Fingerprinted static assets
Target:
`Cache-Control: public, max-age=31536000, immutable`

### Machine association files
Use deliberately short/revalidation-friendly caching during POC so corrections can propagate. Exact production TTL remains OPEN because Apple CDN/device propagation and app-release cadence must be considered.

Assertions:
- `HDR-01`: HTML gets intended security headers.
- `HDR-02`: hashed CSS gets immutable cache policy.
- `HDR-03`: AASA/DAL get explicit suitable content type and cache behavior.
- `HDR-04`: 404 response gets deliberate cache policy.
- `HDR-05`: provider does not silently replace/remove required headers.

---

# 7. SEARCH / LOCALIZATION ASSERTIONS

For both `/ko/...` and `/en/...`:

- `SEO-01`: HTTP `200`.
- `SEO-02`: correct `<html lang>`.
- `SEO-03`: unique localized `<title>`.
- `SEO-04`: localized meta description.
- `SEO-05`: self-canonical equals final current URL.
- `SEO-06`: reciprocal `hreflang="ko"` and `hreflang="en"` point to equivalents.
- `SEO-07`: optional x-default is used only on the neutral root fixture if implemented.
- `SEO-08`: no production-intended page carries `noindex`.
- `SEO-09`: sitemap contains final canonical locale URLs only.
- `SEO-10`: robots does not accidentally block app/support/privacy/account-control pages.
- `SEO-11`: Open Graph `og:url` equals canonical.
- `SEO-12`: Open Graph image is reachable by public HTTPS GET.

## Preview-host rule

Preview/vendor subdomains should not compete with production URLs in search.

POC must demonstrate a provider-specific preview anti-indexing mechanism, e.g. `X-Robots-Tag: noindex` or equivalent preview-only configuration.

- `PREVIEW-SEO-01`: preview HTML returns explicit noindex directive/header.
- `PREVIEW-SEO-02`: production fixture does not inherit preview noindex.

---

# 8. 404 / ERROR CONTRACT

Unknown human route:
`/ko/not-a-real-page/`

Assertions:
- `ERR-01`: returns actual HTTP `404`, not soft-404 `200`.
- `ERR-02`: custom 404 content renders correctly.
- `ERR-03`: 404 has usable navigation back to localized home/apps.
- `ERR-04`: 404 page has no misleading canonical to itself as if valid content.
- `ERR-05`: no SPA fallback converts arbitrary missing routes to app `index.html` with status `200`.

Unknown machine file:
`/.well-known/not-real.json`

- `ERR-06`: returns real `404`; not rewritten to HTML.

---

# 9. ACCESSIBILITY / BROWSER SMOKE MATRIX

The POC is not a full WCAG audit, but must create a stable baseline.

## Manual minimum

For Korean and English app/support/privacy/account-deletion pages:

- `A11Y-01`: keyboard reaches all interactive elements.
- `A11Y-02`: no keyboard trap.
- `A11Y-03`: visible focus.
- `A11Y-04`: logical focus/order matches reading/task order.
- `A11Y-05`: 200% text enlargement without lost controls/content.
- `A11Y-06`: 320 CSS px-equivalent viewport without two-dimensional page scrolling except justified content.
- `A11Y-07`: headings/landmarks retain coherent structure.
- `A11Y-08`: language switch preserves equivalent page where fixture supports it.
- `A11Y-09`: account-delete destructive control remains distinguishable and safely ordered.
- `A11Y-10`: legal/privacy long strings and tables/lists reflow without clipping.

## Automated support

Run an automated accessibility scanner and HTML validation where practical, but scanner success is not PASS by itself per Study 006.

---

# 10. RELEASE / PREVIEW / ROLLBACK EXPERIMENT

## Baseline deployment V1

Deploy fixture with marker:
`POC_VERSION=V1`

Run all deterministic HTTP/search/a11y smoke assertions.

## Preview V2

Change:
- visible POC version marker to V2;
- one page heading;
- one hashed CSS asset;
- one harmless redirect target or metadata value.

Deploy to provider preview/staging mechanism.

Assertions:
- `REL-01`: preview has unique URL/version identity.
- `REL-02`: preview carries noindex protection.
- `REL-03`: live V1 remains unchanged.
- `REL-04`: preview uses same machine endpoint behavior where provider feature allows meaningful test.

## Promote V2

Deploy/promote V2 live.

- `REL-05`: live reports V2.
- `REL-06`: smoke assertions pass after promotion.
- `REL-07`: deployment/release history identifies V2.

## Rollback

Rollback live to V1 using provider-native release/version mechanism, not a new manual rebuild if a native rollback exists.

- `RB-01`: live reports V1 after rollback.
- `RB-02`: previous static asset hash is restored consistently.
- `RB-03`: machine endpoints match V1.
- `RB-04`: headers/redirect config also matches V1.
- `RB-05`: rollback event/version is visible in deployment history.
- `RB-06`: post-rollback smoke suite passes.

### Why this matters

A rollback that restores HTML but not routing/headers/machine files does not meet MintTap's operational contract.

---

# 11. PROVIDER-SPECIFIC OBSERVATIONS TO RECORD

## Firebase Hosting

Current official behavior relevant to the POC:
- custom domain + managed SSL + CDN;
- `firebase.json` controls redirects, rewrites and custom headers;
- redirect rules precede exact static content, then rewrites, so broad redirect rules must be tested carefully;
- preview channels provide separate temporary URLs/config/content;
- versions/releases are tracked and live channel can be rolled back to a prior version;
- channel/version cloning can promote an already-tested exact version.

Primary sources:
- https://firebase.google.com/docs/hosting/custom-domain
- https://firebase.google.com/docs/hosting/full-config
- https://firebase.google.com/docs/hosting/manage-hosting-resources

### Firebase-specific POC notes

Record:
- exact `firebase.json` rule ordering;
- whether extensionless AASA MIME needs explicit header rule;
- preview URL noindex mechanism;
- whether version clone is preferable to rebuild for QA→live promotion;
- custom-domain certificate/DNS provisioning behavior;
- rollback time and whether config+content both restore.

## Cloudflare Workers + Static Assets

Current official behavior relevant to the POC:
- `_headers` and `_redirects` apply to static asset responses;
- they do **not** automatically apply to Worker-generated responses;
- static assets get default `Cache-Control: public, max-age=0, must-revalidate` unless overridden;
- redirects execute before headers;
- Worker versions include bundled code, static assets, bindings/configuration and deployments can be rolled back;
- Workers Custom Domains require nameservers managed by Cloudflare;
- explicit HTML handling / not-found behavior can affect slash/404 semantics.

Primary sources:
- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/static-assets/headers/
- https://developers.cloudflare.com/workers/static-assets/redirects/
- https://developers.cloudflare.com/workers/versions-and-deployments/
- https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/

### Cloudflare-specific POC notes

Record:
- pure static-assets-only configuration first;
- whether Worker code is actually necessary;
- exact `html_handling` and `not_found_handling` choice;
- `_headers` / `_redirects` behavior for extensionless AASA and `.well-known`;
- workers.dev preview/noindex behavior;
- authoritative DNS migration implications separately from static behavior;
- rollback behavior when no external KV/D1/R2 state exists.

---

# 12. AUTOMATED ASSERTION HARNESS — REQUIRED OUTPUT

## MINTTAP DECISION

POC results must be machine-comparable.

Create one provider-neutral smoke harness that accepts a base URL, for example:

```text
verify-site --base-url https://candidate.example
```

The harness should emit structured output such as JSON/JUnit plus human-readable summary.

Minimum result fields:
- assertion ID;
- URL;
- request method;
- expected status;
- observed status;
- redirect chain;
- expected/observed Content-Type;
- selected headers;
- body hash or parser result where relevant;
- PASS / FAIL / WARN;
- timestamp;
- provider/deployment identifier.

### Suggested implementation classes

1. HTTP contract tests — `curl`/Python/Node HTTP client.
2. HTML parser tests — title/canonical/hreflang/meta/OG/lang.
3. JSON/text parsers — AASA/DAL/app-ads/sitemap/robots.
4. Browser smoke — Playwright or equivalent for focus/reflow/screenshots.
5. Accessibility support — axe-core or equivalent plus required manual checklist.

Do not couple the harness to Firebase CLI or Wrangler except for deploy/rollback orchestration wrappers. Verification logic must remain provider-neutral.

---

# 13. SCORING AFTER POC

Documentation-based Study 012 scores become **prior estimates** only.

After POC, score each provider using measured evidence.

## Evidence-adjusted categories

| Category | Evidence from POC |
| --- | --- |
| Operational simplicity | number/complexity of config files, commands, manual console steps, DNS coupling |
| HTTP/routing control | machine endpoint/header/redirect assertions |
| Preview safety | noindex isolation, config parity, shareability |
| Rollback integrity | V2→V1 time and RB assertions |
| Static fit | no unnecessary runtime/Worker/Function requirement |
| Dynamic escape hatch | architecture evaluation only; no need to build unused APIs |
| Observability | deploy/version/log visibility during experiment |
| Domain/DNS flexibility | custom-domain setup consequences |
| CI/Git fit | ability to reproducibly deploy exact artifact |
| Cost predictability | current plan/limits at implementation time, not guessed now |
| Legal/provider review | data-location/subprocessor/admin-log implications when production data flows are known |

## Selection rule

A provider cannot win solely by weighted score if it fails a hard gate.

Any failed hard gate must be:
- fixed and re-tested;
- explicitly accepted with a documented alternative control; or
- treated as provider disqualification.

---

# 14. POC PASS GATE

A candidate reaches **POC PASS** only when:

1. common artifact hash manifest matches expected fixture;
2. all machine-endpoint hard assertions pass;
3. no provider-induced redirect/SPA fallback corrupts verification files;
4. security/cache/header rules behave as specified;
5. Korean/English canonical/hreflang/search/social output passes;
6. custom 404 is a real 404;
7. preview is safely noindex and isolated;
8. deploy/promotion/rollback cycle restores content + routing + headers + machine files;
9. baseline accessibility smoke passes;
10. provider-specific operational/DNS/legal dependencies are documented;
11. assertion harness results are saved with deployment identifiers;
12. unresolved differences are classified rather than hidden.

POC PASS is **not production PASS**. Production still requires real domain, real app identifiers, real legal content, actual Design Studio Web validation, real devices/store associations and operational monitoring.

---

# 15. HANDOFFS TO DESIGN STUDIO

## Web Design

The POC gives Web Design a deterministic browser substrate. Once W### evidence exists, it can replace neutral visual styling while preserving:
- tested route structure;
- semantic templates;
- locale behavior;
- metadata;
- focus/accessibility contracts;
- machine endpoint isolation.

## Typography / Type

Use `/ko/` and `/en/` fixtures for:
- Latin/Korean fallback;
- legal/support long strings;
- 320px / 200% reflow;
- numeric/contact strings;
- fallback/loading behavior in actual browsers.

## Layout / Interaction

Use app/support/privacy/delete fixtures for:
- responsive recomposition;
- language switching;
- focus order;
- destructive flow semantics;
- status/error/recovery;
- navigation orientation.

## Color

Use real browser pages for:
- contrast/focus/state validation;
- forced colors/system settings;
- semantic destructive/success/warning roles;
- screenshot framing and surface hierarchy.

---

# OPEN

- exact SSG/build tool for fixture;
- whether initial POC may connect real `minttap.app` or must remain vendor-host only;
- Firebase/Cloudflare organization accounts and permissions;
- DNS migration authority;
- current provider plan/cost limits;
- monitoring tool used during POC;
- actual browser/device matrix beyond baseline Chromium/WebKit/Firefox if selected;
- real production AASA/DAL identifiers/fingerprints;
- whether app-ads.txt is active for current MintTap apps;
- legal/provider data-location assessment once production analytics/forms/user data exist.

## Foundation conclusion

Provider selection should now proceed through one reproducible experiment:

**one static corpus → two hosting implementations → one provider-neutral assertion harness → preview/promote/rollback cycle → browser/accessibility transfer checks → evidence-adjusted scoring.**

This turns Firebase-vs-Cloudflare from an opinion into a falsifiable engineering/operations decision.