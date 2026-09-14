# 005 — Domain, Hosting & Security Baseline for `minttap.app`

Status: **FOUNDATION / SOURCE-GROUNDED BASELINE**  
Date: 2026-09-14  
Scope: MintTap company website and app-launch infrastructure hosted under `minttap.app`

## Question

What domain, hosting, transport, security-header, deployment, caching and app↔web verification requirements must `minttap.app` satisfy before a hosting/CDN stack is selected?

The objective is not to select a vendor prematurely. The objective is to define a **provider-independent production contract** so later hosting decisions can be evaluated against real Apple/Android launch requirements and modern web-security practice.

---

## SOURCE — TLS 1.0 and TLS 1.1 are deprecated

IETF BCP 195 / RFC 8996 formally deprecates TLS 1.0 and TLS 1.1 and states implementations MUST NOT negotiate them. TLS 1.2 is the minimum modern baseline; TLS 1.3 supersedes TLS 1.2 and should be enabled where supported.

Source:
- https://www.rfc-editor.org/info/rfc8996/

### MINTTAP DECISION

Production `minttap.app` infrastructure must:

- serve the site exclusively over HTTPS;
- support TLS 1.2 at minimum;
- enable TLS 1.3 when the provider supports it;
- not permit TLS 1.0 or TLS 1.1;
- use automatically renewable, publicly trusted certificates;
- monitor certificate issuance/renewal failure before expiry becomes user-visible.

This is a hosting-selection gate, not an optional optimization.

---

## SOURCE — HSTS can enforce secure transport after HTTPS is proven stable

RFC 6797 defines HTTP Strict Transport Security (HSTS), allowing a site to declare that user agents should interact with it only through secure connections.

Source:
- https://www.rfc-editor.org/info/rfc6797/

### SYNTHESIS

HSTS is valuable only after HTTPS coverage is operationally reliable. Premature use of `includeSubDomains` or preload can turn a forgotten/insecure subdomain into an outage rather than a graceful fallback.

### MINTTAP DECISION

Adopt HSTS in stages:

1. establish complete HTTPS behavior for the production hostname;
2. confirm there are no production HTTP-only dependencies;
3. enable `Strict-Transport-Security` on the apex site;
4. add `includeSubDomains` only after every MintTap-controlled subdomain is known to be HTTPS-ready;
5. treat browser preload as a later irreversible/high-cost operational decision rather than a Foundation default.

`http://minttap.app/...` should redirect to the canonical HTTPS origin for ordinary pages.

---

## SOURCE — Apple associated-domain files have special hosting requirements

Apple's current Associated Domains documentation states that the `apple-app-site-association` file:

- is named exactly `apple-app-site-association` with no extension;
- should be placed under `https://<fully-qualified-domain>/.well-known/apple-app-site-association`;
- must be hosted over HTTPS with a valid certificate;
- must be served without redirects;
- must be available independently on every associated hostname/subdomain declared by the app.

Apple also notes that on iOS 14+ and macOS 11+ associated-domain files are obtained through an Apple-managed CDN that may fetch the latest version from the origin.

Sources:
- https://developer.apple.com/documentation/Xcode/supporting-associated-domains
- https://developer.apple.com/documentation/technotes/tn3155-debugging-universal-links
- https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.developer.associated-domains

Older but still useful Apple guidance also documents a 128 KB uncompressed AASA size limit for apps running iOS 9.3.1+.

Source:
- https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html

### MINTTAP DECISION

The production hosting layer must support this exact endpoint without framework/page redirects:

`https://minttap.app/.well-known/apple-app-site-association`

If MintTap later associates `www.minttap.app`, `support.minttap.app`, or another hostname with an app, each declared hostname must be treated as an independent verification surface.

Do not rely on an apex→www or www→apex redirect to satisfy AASA hosting.

AASA changes are release-critical infrastructure changes and require post-deploy device verification because Apple-side CDN caching can delay or complicate propagation.

---

## SOURCE — Android Digital Asset Links also require exact, redirect-free hosting

Android Developers currently requires the Digital Asset Links statement list at:

`https://<domain>/.well-known/assetlinks.json`

The documentation specifies:

- HTTPS access is required;
- `Content-Type` must be `application/json`;
- the resource must be accessible without 301 or 302 redirects;
- every host used for App Links must publish its own file.

Source:
- https://developer.android.com/training/app-links/configure-assetlinks

### MINTTAP DECISION

The production stack must be able to serve:

`https://minttap.app/.well-known/assetlinks.json`

as a direct HTTP 200 JSON response, with no canonical-host or trailing-path redirect in front of it.

Android signing-certificate fingerprints are security-sensitive configuration data but are not secrets. They must be derived from the correct production signing configuration and reviewed whenever signing or package identity changes.

---

## MINTTAP DECISION — `.well-known` is a privileged operational surface

Treat these machine-readable files differently from normal marketing pages:

- exact filename/path;
- direct 200 response;
- correct MIME type;
- HTTPS only;
- no login/authentication;
- no HTML fallback;
- no SPA catch-all rewrite;
- no automatic locale redirect;
- no apex↔www redirect at the requested host;
- explicit cache policy;
- synthetic monitoring;
- release-linked ownership and review.

At minimum the deployment pipeline must validate:

- `/.well-known/apple-app-site-association` when used;
- `/.well-known/assetlinks.json` when used;
- `/app-ads.txt` when advertising verification is used.

A host that cannot serve these resources precisely is not acceptable for MintTap app-launch infrastructure.

---

## SOURCE — HTTP caching is explicit protocol behavior

RFC 9111 defines HTTP cache behavior and `Cache-Control`. Cache freshness and revalidation can materially change how quickly updated site content or verification resources become visible.

Source:
- https://www.rfc-editor.org/rfc/rfc9111.html

### MINTTAP DECISION — cache classes

Do not use one global cache rule for every object. Use content classes.

### Class A — fingerprinted immutable assets

Examples:
- `/assets/app.8f3a1.js`
- hashed CSS/fonts/images.

Policy direction:
- long cache lifetime;
- immutable only when the URL changes when bytes change.

### Class B — HTML/product/policy/support pages

Policy direction:
- shorter explicit freshness or revalidation;
- must update predictably after a release;
- stale content must not persist for long periods after privacy/support changes.

### Class C — verification and association files

Examples:
- AASA;
- `assetlinks.json`;
- `app-ads.txt`.

Policy direction:
- explicit conservative cache behavior;
- avoid accidental multi-day CDN/browser persistence unless a provider-specific validation proves it safe;
- purge/invalidate CDN cache during updates when supported;
- verify origin and edge response after every change.

Exact TTL values remain an implementation decision after the hosting provider and change frequency are known.

---

## SOURCE — redirect semantics are standardized but platform verification may forbid them

RFC 9110 defines HTTP redirect status codes such as 301, 302, 307 and 308.

Source:
- https://www.rfc-editor.org/rfc/rfc9110.html

### MINTTAP DECISION

For normal human-facing routes:

- choose one canonical production origin;
- redirect alternate scheme/hostname forms deliberately;
- use permanent redirects for deliberate durable URL moves;
- preserve a redirect map when app or policy URLs are renamed.

For Apple/Android association files:

- platform-specific no-redirect rules override the ordinary canonicalization strategy;
- the file must exist directly at each declared hostname.

Provisional canonical origin:

`https://minttap.app/`

`www.minttap.app` should not become a second independent content origin unless a later requirement justifies it. If provisioned, the normal web surface may redirect to the apex, but `.well-known` files must be served directly on `www` if that hostname is ever declared to Apple/Android.

---

## SOURCE — CSP and core response headers reduce browser attack surface

MDN's current web-security guidance recommends HTTPS and Content Security Policy (CSP), including strict CSP where practical. A strict CSP can restrict executable scripts, disable legacy object embeds, constrain base URLs, control framing and upgrade insecure subresource requests.

Relevant current guidance:
- https://developer.mozilla.org/en-US/docs/Web/Security
- https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP

OWASP's HTTP Headers Cheat Sheet recommends, among other controls:

- correctly configured `Content-Type`;
- `X-Content-Type-Options: nosniff`;
- explicit `Referrer-Policy`, with `strict-origin-when-cross-origin` as a practical baseline.

Source:
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

### MINTTAP DECISION — initial browser security-header baseline

The final policy must be validated against the actual implementation, but production should target:

- `Strict-Transport-Security` after HTTPS readiness;
- `Content-Security-Policy`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: strict-origin-when-cross-origin` or a stricter policy if product requirements permit;
- an explicit `Permissions-Policy` that disables browser capabilities not needed by the site.

CSP direction:

- begin deployment using `Content-Security-Policy-Report-Only` where necessary;
- move to enforcement after legitimate sources are known;
- prefer nonce/hash-based script control where the implementation permits it;
- target `object-src 'none'` unless a real requirement exists;
- constrain `base-uri` (`'none'` or `'self'` depending on implementation);
- target `frame-ancestors 'none'` unless legitimate embedding is required;
- constrain `form-action` to intended submission origins;
- do not solve analytics/marketing integration problems by globally adding broad `unsafe-inline` or wildcard sources without review.

The exact CSP cannot be finalized until the web framework, analytics and third-party integrations are selected.

---

## SOURCE — Permissions Policy can disable powerful browser features

Permissions Policy controls whether specified origins may use features such as camera, microphone, geolocation and other browser capabilities.

Source:
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Permissions_Policy

### MINTTAP DECISION

For a normal company/app-support website, sensitive browser capabilities should default to unavailable unless a concrete feature needs them.

If a future MintTap web app legitimately requires camera, microphone, clipboard or other capabilities, enable only the required capability and origin after threat/UX review.

---

## SOURCE — DNSSEC protects authenticity/integrity of DNS data

ICANN explains that DNSSEC adds cryptographic signatures so validating resolvers can detect forged or modified DNS data.

Source:
- https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en

### MINTTAP DECISION

DNSSEC is a **recommended production control**, not yet a hard launch blocker.

Before enabling it:

- confirm registrar and authoritative DNS provider support;
- confirm DS/key rollover operational procedures;
- ensure ownership is clear, because a broken DNSSEC chain can make the domain unreachable for validating resolvers.

The future hosting/DNS evaluation should prefer providers with mature managed DNSSEC support.

---

## SOURCE — CAA can restrict certificate issuance authorities

RFC 8659 defines Certification Authority Authorization (CAA) DNS records, allowing the domain holder to state which CAs are authorized to issue certificates for a domain.

Source:
- https://www.rfc-editor.org/info/rfc8659/

### MINTTAP DECISION

Use CAA after the certificate/hosting provider is known and issuance flows are understood. Do not create an overly restrictive record before confirming all legitimate certificate issuers needed by the selected CDN/hosting platform.

CAA becomes part of the certificate-change checklist.

---

## SOURCE — deployment credentials must not live in source code

OWASP guidance for CI/CD and secrets management recommends that deployment/API credentials not be hardcoded in repositories, and that CI/CD credentials use least privilege, auditing and rotation.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html

### MINTTAP DECISION

`web-manager` may contain public verification material and infrastructure documentation, but must not contain private keys, cloud credentials, deploy tokens, secret API keys or account-recovery secrets.

Production deployment credentials belong in an appropriate CI/CD secrets facility or dedicated secret manager with least privilege.

Public-by-design files such as AASA, `assetlinks.json`, public signing fingerprints and `app-ads.txt` are configuration, not secrets.

---

## Hosting / CDN provider acceptance gate

A candidate production platform must satisfy all of the following before selection.

### Domain and TLS

- custom apex domain `minttap.app`;
- controllable `www` behavior;
- valid automatic certificates;
- automated renewal;
- TLS 1.2+;
- TLS 1.3 support preferred;
- forced HTTPS for ordinary routes;
- ability to emit HSTS.

### Exact-path hosting

- arbitrary static files at root and `.well-known`;
- extensionless AASA file;
- correct JSON MIME for `assetlinks.json`;
- direct 200 responses without redirects;
- ability to bypass SPA/router catch-all behavior.

### HTTP control

- custom response headers;
- CSP support;
- cache-control per route/content class;
- redirects and status-code control;
- custom 404/5xx behavior;
- CDN cache purge/invalidation or predictable revalidation.

### Deployment operations

- atomic or otherwise safe deployment;
- rollback to a known-good version;
- preview/staging support preferred;
- production deployment history;
- restricted deployment permissions;
- CI/CD compatibility;
- secret management integration.

### Observability

- uptime checks or easy external monitoring;
- TLS/certificate monitoring;
- access/error logs when needed;
- ability to detect 4xx/5xx regressions;
- synthetic checks for privacy/support/account-deletion and association files.

### Business continuity

- domain registration must remain separate from ephemeral developer accounts where practical;
- ownership/recovery credentials must not depend on a single person's device/account;
- DNS and hosting configuration must be documented sufficiently to migrate providers;
- backup/export of site source/content must exist independently of the hosting provider.

---

## Provisional MintTap production topology

This is an architecture direction, not a vendor choice.

```text
Registrar
   │
   ├── domain ownership / renewal protection
   │
Authoritative DNS
   │
   ├── A/AAAA or CNAME/ALIAS as provider requires
   ├── DNSSEC (recommended when operationally ready)
   └── CAA (after CA/provider selection)
   │
HTTPS edge / CDN / hosting
   │
   ├── https://minttap.app/
   ├── /apps/...
   ├── /support/...
   ├── /privacy/...
   ├── /.well-known/apple-app-site-association
   ├── /.well-known/assetlinks.json
   └── /app-ads.txt
   │
Versioned deployment source
   │
   └── reviewed CI/CD → production → post-deploy validation
```

The apex hostname is the default canonical public origin unless a future technical or product requirement changes that decision.

---

## Production validation checklist

### Transport

- [ ] `https://minttap.app` presents a valid trusted certificate.
- [ ] TLS 1.0/1.1 are unavailable.
- [ ] TLS 1.2 works; TLS 1.3 works when provider supports it.
- [ ] ordinary HTTP requests redirect to HTTPS.
- [ ] HSTS behavior is intentionally configured.

### Canonicalization

- [ ] apex/www behavior is intentional.
- [ ] alternate public URLs have deliberate redirect behavior.
- [ ] required policy/support URLs return expected final status.
- [ ] retired public routes have an explicit redirect/deprecation decision.

### Apple

- [ ] AASA endpoint returns 200 directly.
- [ ] no redirect occurs.
- [ ] file is syntactically valid JSON.
- [ ] app identifiers and paths match the production app.
- [ ] actual Universal Link behavior is tested on a device.

### Android

- [ ] `assetlinks.json` returns 200 directly.
- [ ] `Content-Type: application/json`.
- [ ] no redirect occurs.
- [ ] package name and production signing fingerprints are correct.
- [ ] Android App Links verification is tested with production-like build/signing.

### Headers

- [ ] CSP is deployed and validated.
- [ ] framing policy is explicit.
- [ ] `X-Content-Type-Options: nosniff`.
- [ ] explicit Referrer Policy.
- [ ] Permissions Policy reviewed against actual browser features.
- [ ] HSTS applied only at the intended scope.

### Cache/deploy

- [ ] versioned static assets can be cached safely.
- [ ] HTML/policy/support changes propagate predictably.
- [ ] verification-file changes can be invalidated/revalidated.
- [ ] rollback has been tested.
- [ ] post-deploy synthetic checks exist for launch-critical URLs.

### Secrets and ownership

- [ ] no production secret is committed to the web repository.
- [ ] deployment credentials are least-privileged.
- [ ] domain renewal/registrar access has recovery controls.
- [ ] configuration is documented enough to rebuild/migrate the site.

---

## DESIGN STUDIO RELATED DOMAIN CHECK

### Web Design

Relevant because security policy affects actual implementation and third-party resource loading. CSP, native browser behavior, performance and production validation are Web Design integration concerns.

### Layout / Interaction

Security and operational errors create user-facing states: broken support/deletion pages, form failures, stale content and link-routing failures need explicit recovery and feedback behavior.

### Typography / Type

Font-hosting choices affect CSP, cross-origin requests, performance and fallback behavior. Prefer designs that remain robust if a third-party font resource fails.

### Color

No direct security dependency at this stage, but browser/system rendering and forced-color accessibility remain relevant when security/error/status surfaces are later designed.

### Handoff opportunity

When the Design Studio Web specialist begins browser implementation research, MintTap can provide a real project validation context for CSP constraints, `.well-known` resources, cache behavior, deep-link routing and production-header design.

---

## OPEN

- Production hosting/CDN vendor has not been selected.
- Registrar and authoritative DNS providers are not yet documented here.
- Current DNSSEC state of `minttap.app` has not been audited.
- Current certificate issuer and renewal path have not been audited.
- Whether `www.minttap.app` should be provisioned is not yet finalized.
- Universal Link and Android App Link route sets are not yet defined.
- No final CSP can be written before implementation dependencies/analytics are known.
- No final cache TTLs can be specified before deployment architecture and change frequency are known.
- Monitoring/incident-response provider and alert owner remain undefined.

---

## CHANGE WATCH

Re-check before production launch and after major infrastructure changes:

- Apple Associated Domains/AASA hosting requirements;
- Android Digital Asset Links requirements;
- TLS BCP updates;
- browser security-header support/standards;
- selected CDN/host certificate and redirect behavior;
- selected provider behavior for extensionless and `.well-known` files;
- any migration affecting DNS, certificate issuance, caching or canonical hostnames.

---

## Foundation conclusion

`minttap.app` is not merely a collection of HTML pages. It is also part of the trust boundary connecting MintTap's public identity, Apple/Android applications, support/privacy obligations and domain ownership.

Therefore hosting must be selected against a **production contract**, not convenience alone.

The minimum architecture direction is:

**stable domain ownership → managed authoritative DNS → modern TLS/HTTPS edge → precise route/header/cache control → versioned deployment → monitored required URLs → reversible releases**.

Provider selection comes after this baseline, not before it.
