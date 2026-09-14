# 025 — Identical Provider POC Corpus + Provider-Neutral HTTP Assertion Runner

Status: **PRACTICE / LOCAL PROVIDER-NEUTRAL HTTP CONTRACT VALIDATION COMPLETED**  
Research date: 2026-09-14

## Purpose

Studies 023–024 established a four-zone release workflow and mapped Firebase Hosting and Cloudflare Workers + Static Assets onto it. The remaining pre-account gap was practical: both providers need to receive the **same deployable bytes** and be judged by the **same externally observable HTTP contract**. Otherwise a provider comparison can accidentally compare different sites or different test criteria.

This study creates that neutral test layer. It intentionally uses synthetic app identifiers and synthetic privacy/support copy. It is not a MintTap production website and must not be interpreted as real product, legal, advertising, App Store or Play Store truth.

## SOURCE — authoritative constraints used by the corpus

### Apple associated domains

Apple's current Supporting Associated Domains documentation requires an `apple-app-site-association` file in `/.well-known/`, served over HTTPS with a valid certificate and **without redirects**. Apple's Universal Links guidance documents JSON / `application/json` for modern deployments. Apple TN3155 recommends directly inspecting the HTTP response and treats 301/302 on the AASA fetch as unsupported.

Sources:
- https://developer.apple.com/documentation/xcode/supporting-associated-domains
- https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links
- https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html

### Android App Links

Android's current App Links documentation requires `https://<domain>/.well-known/assetlinks.json`, `Content-Type: application/json`, HTTPS, and **no 301/302 redirects**. Package name and SHA-256 signing certificate fingerprints are part of the association record.

Source:
- https://developer.android.com/training/app-links/configure-assetlinks

### Search canonicalization / robots

Google Search documents redirects, sitemap membership and `rel="canonical"` as canonicalization signals, while making clear that a declared canonical is a hint rather than an absolute command. Google's Robots Exclusion Protocol documentation requires `robots.txt` at the site top level and supports an absolute `Sitemap:` URL.

Sources:
- https://developers.google.com/search/docs/crawling-indexing/canonicalization
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec

### Provider behavior retained from 024

Firebase Hosting and Cloudflare Static Assets expose different configuration mechanisms, but both can express custom headers, redirects/canonical URL behavior and custom 404 handling. Cloudflare documents `_headers`, `_redirects`, `assets.html_handling` and `not_found_handling`; Firebase uses `firebase.json` Hosting configuration.

Sources:
- https://firebase.google.com/docs/hosting/full-config
- https://developers.cloudflare.com/workers/static-assets/headers/
- https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/
- https://developers.cloudflare.com/workers/static-assets/routing/static-site-generation/

## SYNTHESIS

A provider POC should not ask whether Firebase and Cloudflare expose the same configuration syntax. It should ask whether the same release artifact produces the same required **observable response semantics**.

The neutral contract therefore measures:
- status code;
- redirect destination;
- `Content-Type`;
- cache policy;
- required security headers;
- canonical URL declaration;
- language declaration;
- machine-file direct accessibility;
- valid JSON for association files;
- preview indexation protection;
- real 404 status + body;
- artifact byte integrity.

This separates **what MintTap requires** from **how a provider is configured**.

## MINTTAP DECISION — deterministic synthetic corpus

`tools/build_poc_corpus.py` deterministically generates a provider-neutral site containing:

- `/ko/`
- `/en/`
- `/ko/apps/example/`
- `/en/apps/example/`
- localized support pages;
- localized privacy pages;
- `/.well-known/apple-app-site-association`;
- `/.well-known/assetlinks.json`;
- `/app-ads.txt`;
- `/robots.txt`;
- `/sitemap.xml`;
- `/404.html`.

The `example` app and all identifiers are explicitly synthetic. Real Team ID, bundle ID, Android package name, signing certificate, ad-system records and legal copy remain OPEN product facts.

The generator emits a non-public release artifact manifest containing:
- every relative file path;
- byte count;
- per-file SHA-256;
- aggregate `artifact_digest` computed from the ordered path + file-digest set.

The manifest itself is not included in the deployable corpus, avoiding a self-referential digest.

## MINTTAP DECISION — one HTTP contract, two environment profiles

`control/poc/http_contract.json` defines a provider-neutral external contract.

### Production profile

HTML must:
- return `200` at canonical trailing-slash routes;
- declare the exact `https://minttap.app/...` canonical URL;
- use the expected `lang`;
- return the defined cache policy;
- expose the required CSP, `X-Content-Type-Options` and `Referrer-Policy` values.

Canonical non-slash aliases must redirect to their slash form.

Machine files must:
- be directly reachable;
- return their expected MIME type;
- use the machine-file cache policy;
- return parseable JSON for AASA and Asset Links.

An unknown route must return a true `404`, not a soft-404 `200`.

### Preview profile

The corpus bytes stay identical. Preview isolation is an edge/deployment responsibility. In addition to the production content checks, preview HTML must expose:

`X-Robots-Tag: noindex`

The current local reference adds `nofollow` as well, but the normative assertion is `noindex`.

This design prevents preview-specific HTML mutation from producing a different artifact than production.

## MINTTAP DECISION — assertion runner

`tools/poc_http_assert.py` accepts any HTTP origin:

```text
python tools/poc_http_assert.py \
  --base-url <provider-preview-or-production-origin> \
  --profile preview|production
```

The same tool is intended for:
- local reference validation;
- Firebase preview channel;
- Firebase live channel;
- Cloudflare version preview URL;
- Cloudflare production custom domain.

Provider adapters may change configuration syntax, credentials and version identifiers. They may **not** silently change the test contract.

## VALIDATION — controlled local proof

Command:

```text
python tools/poc_http_assert.py --self-test
```

Result: **8 / 8 expected outcomes matched.**

Cases:
1. clean production reference → PASS;
2. clean preview reference with `noindex` → PASS;
3. preview missing `noindex` → detected FAIL;
4. `assetlinks.json` served with wrong MIME type → detected FAIL;
5. required CSP removed → detected FAIL;
6. localized page canonical points to wrong URL → detected FAIL;
7. unchanged corpus matches artifact manifest → PASS;
8. post-build mutation of `en/index.html` → digest verification detects FAIL.

Generated controlled corpus: **14 files**.

Observed deterministic artifact digest for the current synthetic fixture:

`sha256:3476b92117ff46aebe44721505f81d9b679b81237234a5e99449f92d03717f7f`

This digest is evidence for the current fixture only. Any intentional corpus change must generate a new digest.

## Important design boundary

The local reference server proves the **runner and contract**, not Firebase or Cloudflare behavior. It deliberately emulates the expected externally visible behavior so positive and negative detection can be checked before provider accounts exist.

Provider PASS requires deploying the generated bytes and running the same assertions against real provider URLs.

## OPEN / VALIDATION REQUIRED

Before production confidence:
- replace all synthetic AASA and Asset Links identifiers with real app facts;
- decide whether `app-ads.txt` is applicable and populate only verified advertising records;
- verify exact response MIME/redirect/cache behavior on Firebase preview + live;
- verify the same on Cloudflare preview + production;
- verify machine files over real HTTPS and custom domain;
- verify preview URLs cannot be indexed and, where appropriate, cannot expose production backends;
- test `minttap.app` DNS/custom-domain behavior;
- add live TLS/certificate/HSTS assertions once HTTPS endpoints exist;
- decide production CSP after actual scripts/fonts/analytics are known;
- validate sitemap/canonical/hreflang against real app inventory;
- verify 404 behavior and canonical redirects in real browsers and Search Console after launch.

## Design Studio dependency / handoff

Latest checked Web Design status still has no substantive `W###`. No visual style is prescribed here.

Future Web Design / Layout-Interaction transfer should use the live POC to test:
- localized navigation and route recovery;
- true 404 comprehension and recovery action;
- canonical redirect behavior during keyboard/history navigation;
- Korean/English text growth and reflow;
- machine endpoints remaining invisible to visual page composition while still operationally correct;
- preview/staging state being distinguishable in internal review interfaces without relying on color alone.

The HTTP corpus is infrastructure/test evidence. Production page hierarchy, typography, color and interaction remain Design Studio-owned design questions.

## Outcome

025 closes the provider-neutral pre-deployment test gap. The next high-value work is no longer another abstract hosting comparison: it is to prepare provider-specific deployment adapters/configuration for this exact corpus, then execute the live Firebase vs Cloudflare POC when account/domain authority is available.
