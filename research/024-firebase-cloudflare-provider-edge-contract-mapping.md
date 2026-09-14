# 024 — Firebase Hosting vs Cloudflare Provider-Edge Contract Mapping

Status: **PRACTICE / DOCUMENTED PROVIDER MAPPING + LOCAL CONTRACT VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can Firebase Hosting and Cloudflare Workers + Static Assets each satisfy MintTap's provider-neutral 023 workflow contract without allowing provider-specific defaults to weaken preview isolation, exact artifact promotion, rollback, credential scope, static routing, or release verification?

This study does **not** select a provider and does **not** perform a live deploy. Provider accounts/domain authority remain unavailable.

---

## RELATED DOMAIN CHECK

Latest Design Studio Web status still has no substantive `W###`; Web Design remains at `W001` next. Therefore this block is implementation/release infrastructure research, not a visual-design decision.

Future browser validation must consume the exact provider behavior documented here, especially:
- canonical URL/trailing-slash behavior;
- custom 404 behavior;
- cache/security headers;
- preview URL indexing/access;
- localized paths and machine endpoints;
- rollback verification.

No visual style is prescribed.

---

# SOURCE — Firebase Hosting

Primary sources checked 2026-09-14:
- https://firebase.google.com/docs/hosting/manage-hosting-resources
- https://firebase.google.com/docs/hosting/full-config
- https://firebase.google.com/docs/hosting/github-integration
- https://firebase.google.com/docs/cli
- https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines

Verified facts:

1. A Firebase Hosting site has a permanent `live` channel and optional preview channels with their own temporary URLs.
2. A deployed channel release points to a specific version; release metadata records who deployed and when.
3. Preview channels are currently documented as **beta**. They expire by default after 7 days and can be configured up to 30 days.
4. `firebase hosting:clone` can clone an already deployed version from one channel to another. Within the same site, both releases can point to the **same version ID**. Firebase explicitly presents preview→live cloning as a use case for going live with exactly tested content.
5. The live channel can be rolled back to a previous version. Rollback creates a new release serving the same previous version identifier.
6. Release retention is configurable per channel; releases beyond the retained count have content scheduled for deletion.
7. Firebase CLI recommends **Application Default Credentials (ADC)** for CI. Legacy `FIREBASE_TOKEN` is documented as less secure and no longer recommended.
8. Google Cloud supports GitHub Actions OIDC → Workload Identity Federation → short-lived Google credentials, avoiding long-lived service-account keys.
9. Firebase Hosting GitHub integration can create PR preview channels and optionally deploy live after merge, but preview URLs still interact with the real backend resources of the Firebase project.
10. `firebase.json` controls redirects, rewrites, headers, public directory and custom 404 behavior. Redirects have higher precedence than exact static content; exact static content precedes rewrites.
11. Static Hosting redeploys invalidate Firebase CDN cached static content. Cache behavior can be changed with response headers.

### SYNTHESIS — Firebase mapping to 023

Firebase Hosting supports a strong **test exact version → promote exact version** model through preview channels plus `hosting:clone`.

For MintTap, this is preferable to rebuilding the same commit for production because the production release can reference the exact Hosting version that was reviewed.

`firebase deploy --only hosting` should therefore be treated as **version creation**, not automatically as final production promotion in the preferred controlled path.

### MINTTAP DECISION — Firebase credential mode

Preferred future GitHub Actions path:

`GitHub OIDC → Google Cloud Workload Identity Federation → ADC → Firebase CLI`

Do not use a long-lived service-account JSON key or legacy `FIREBASE_TOKEN` as the preferred production baseline.

This path still requires live proof that the exact Firebase CLI operations used by MintTap accept the resulting federated ADC with the intended minimum IAM roles.

---

# SOURCE — Cloudflare Workers + Static Assets

Primary sources checked 2026-09-14:
- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/static-assets/headers/
- https://developers.cloudflare.com/workers/static-assets/redirects/
- https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/
- https://developers.cloudflare.com/workers/versions-and-deployments/
- https://developers.cloudflare.com/workers/versions-and-deployments/preview-urls/
- https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/
- https://developers.cloudflare.com/workers/wrangler/commands/workers/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/
- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/

Verified facts:

1. Workers Static Assets deploys Worker code and static assets as one Worker version.
2. A Worker **version** captures bundled code, static assets, bindings and compatibility settings. External storage state such as KV/R2/D1/Durable Objects is not versioned with it.
3. `wrangler versions upload` creates a version **without deploying it immediately**.
4. `wrangler versions deploy --version-id ...` can later deploy a previously created version, so upload/preview and production promotion can be separated.
5. Versioned preview URLs are generated for uploaded versions when previews are enabled. Preview URLs are public by default; Cloudflare Access can be used to require sign-in.
6. Workers Builds uses `wrangler versions upload` by default for non-production branches and `wrangler deploy` for production branches.
7. External GitHub Actions deployment documentation currently uses a **Cloudflare API token + account ID**, and recommends scoping the token to required account/zone resources.
8. A rollback creates a new deployment pointing at the selected previous version. Rollback is available only among the 100 most recently published versions.
9. Rollback does not roll back external bound resources, and can fail when required bound resources were deleted or certain Durable Object lifecycle changes occurred.
10. `_headers` controls static-asset response headers. Default static asset response behavior includes `Cache-Control: public, max-age=0, must-revalidate` in the documented case and ETag support.
11. `_redirects` controls static redirects/proxying, with documented limits and feature gaps. Redirects are processed before `_headers`.
12. `assets.html_handling` controls canonical `.html` / trailing-slash behavior.
13. Custom 404/static-site behavior is supported through static asset routing configuration.

### SYNTHESIS — Cloudflare mapping to 023

Cloudflare can also implement the required **upload exact version → validate preview → deploy that exact version ID** flow.

For MintTap, `wrangler deploy` should **not** be the default trusted-build command because it couples version creation and 100% production deployment. The preferred controlled path is:

`wrangler versions upload`
→ capture version ID + preview URL
→ validate
→ release manifest ALLOW
→ `wrangler versions deploy --version-id <approved version>`

### MINTTAP DECISION — Cloudflare credential mode

The currently evidenced external-CI baseline is a **scoped Cloudflare API token** stored only in the deploy/rollback trust zone.

No official Cloudflare Workers external GitHub deployment documentation located in this block established a GitHub OIDC → short-lived Cloudflare deploy credential flow equivalent to Google Cloud WIF. Therefore MintTap must not claim OIDC deploy credentials for Cloudflare until directly documented and validated.

---

# PROVIDER COMPARISON

| Control | Firebase Hosting | Cloudflare Workers + Static Assets |
| --- | --- | --- |
| Isolated preview | Preview channels | Version preview URLs / versions upload |
| Preview maturity | Preview channels documented beta | Version previews documented production feature |
| Exact tested artifact promotion | `hosting:clone`; same-site clone can retain same version ID | `versions deploy --version-id` |
| Production deploy default | `firebase deploy` to live if targeting live | `wrangler deploy` creates + immediately deploys |
| Preferred MintTap production path | clone approved version to live | deploy approved uploaded version ID |
| Rollback | new release pointing at previous version | new deployment pointing at previous version |
| Retention | configurable release retention per channel | rollback scope limited to 100 recent published versions |
| CI auth documented by provider | Firebase CLI recommends ADC | API token + account ID |
| Short-lived GitHub identity option | Google Cloud WIF + GitHub OIDC can provide ADC | not established in official Workers external-CI docs checked |
| Static headers | `firebase.json` headers | `_headers` |
| Static redirects | `firebase.json` redirects | `_redirects` |
| Rewrite support | strong Hosting rewrite model | `_redirects` proxying plus Worker/static routing; not feature-equivalent |
| URL canonicalization | explicit config / content rules | `assets.html_handling` |
| Dynamic state rollback | not universally implied; pinned Functions/Cloud Run have specific behavior | external KV/R2/D1/DO state not rolled back |
| Custom domain dependency | provider setup required | Workers custom domain requires Cloudflare-managed nameservers per current migration docs |

---

# MINTTAP DECISION — common provider-edge contract

A provider is acceptable for the POC only if all of these remain true:

1. Preview is isolated from production traffic.
2. Production promotion is separate from preview creation.
3. The **exact reviewed provider version** can be promoted without source rebuild.
4. Rollback can re-point traffic to a prior retained provider version without rebuilding current source.
5. Rollback retention is explicitly bounded and monitored.
6. Static security/cache headers can be configured and independently verified.
7. Redirect/canonical URL behavior is explicit and independently verified.
8. Custom 404 behavior is explicit.
9. Deployment credentials exist only in the DEPLOY/ROLLBACK zone.
10. Dynamic/external state is **not assumed** to roll back with static/Worker version.
11. Provider version ID and MintTap artifact digest are both recorded in the release manifest.
12. Live account/domain behavior is required before production PASS.

---

# LOCAL PRACTICE VALIDATION

Added:
- `tools/validate_provider_edge_contract.py`
- `control/tests/provider_edge_contract_cases.json`

The synthetic validator encodes the minimum 023→provider acceptance contract and rejects configurations that:
- couple preview directly to production;
- cannot promote the exact reviewed version;
- require rebuild-only rollback;
- omit static header control;
- use unsupported credential classes;
- assume unlimited rollback retention;
- falsely assume dynamic state rolls back;
- omit live-provider validation.

Controlled result:

**11 / 11 expected outcomes matched.**

This is a local policy validation only. It does not prove provider APIs, IAM, custom domain, preview URL, version promotion or rollback on real accounts.

---

# IMPORTANT DIFFERENCES FOR THE LIVE POC

## Firebase

Must verify:
- GitHub OIDC/WIF-created ADC works with the exact Firebase CLI Hosting operations;
- minimum IAM roles required for preview deploy, version clone, live promotion and rollback;
- preview channel behavior under the selected production Firebase project;
- whether preview should use a separate backend project because preview URLs may interact with real backend resources;
- exact release-retention setting and storage consequences;
- headers/redirects/404/machine-file response behavior at `web.app` and custom `minttap.app`.

## Cloudflare

Must verify:
- minimum API-token permissions for versions upload, versions deploy, rollback and custom domain/routes;
- whether a separate preview Worker/account/environment is needed for stricter isolation;
- preview URL public/private policy and Cloudflare Access behavior;
- exact version-ID capture and manifest binding;
- rollback behavior when bindings change;
- custom domain/nameserver implications for `minttap.app`;
- `_headers`, `_redirects`, HTML handling and 404 behavior on the actual Worker/custom domain.

---

# DESIGN STUDIO HANDOFF

Future Web Design/browser validation should not treat provider behavior as invisible infrastructure.

The POC must visibly test:
- Korean/English canonical URLs and trailing-slash normalization;
- no accidental indexation of preview URLs;
- 404 presentation and recovery;
- security/cache headers on HTML, assets and machine endpoints;
- `/.well-known/apple-app-site-association`, `/.well-known/assetlinks.json`, `/app-ads.txt`;
- responsive/layout/type/color/accessibility behavior after the real provider's routing and caching rules apply.

Provider choice does not define visual design. It can, however, change URL, preview, routing, cache and error-page behavior that Web Design must validate.

---

# OPEN / CHANGE WATCH

- Firebase preview channels are documented beta as of 2026-09-14.
- Cloudflare Workers Builds/API-token behavior and Static Assets routing capabilities continue to evolve.
- Cloudflare external-CI short-lived OIDC-equivalent deployment auth remains OPEN.
- Firebase Hosting exact IAM role set for WIF-driven CLI operations remains LIVE VALIDATION.
- `minttap.app` DNS authority/provider state is not yet available.
- Neither provider has been production-tested with MintTap content.
- Current deterministic JSON hashing is still not RFC 8785 JCS-conformance proven.

## Highest-value next block

Prepare the **identical provider POC corpus + assertion runner** locally, without provider accounts:
- localized `/ko/` and `/en/` pages;
- support/privacy/app routes;
- exact machine files;
- 404;
- redirects/canonicalization;
- cache/security headers;
- sitemap/robots;
- release artifact digest manifest;
- provider-neutral HTTP assertion specification.

This will make the eventual Firebase vs Cloudflare live POC an execution task rather than another design/research task.
