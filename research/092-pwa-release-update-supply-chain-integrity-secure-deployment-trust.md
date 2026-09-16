# 092 — PWA Release/Update Supply-Chain Integrity & Secure Deployment Trust

Status: **PASS (generic security/operations contract) / PRODUCT IMPLEMENTATION VALIDATION OPEN**  
Date: 2026-09-17

## Purpose
091 established how long-offline clients coexist and retire safely. 092 asks the preceding trust question: **what if the update itself is malicious, unauthorized, stale, or built from compromised inputs?** Track E owns release trust and containment; A supplies service-worker/browser mechanics; C consumes integrity evidence into release gates; B consumes truthful security/recovery states; D consumes minimized rollout evidence without becoming a security oracle.

## Integrated model
`source authority → reviewed change → dependency resolution → isolated build → artifact/provenance identity → authorized promotion → origin/CDN publication → service-worker update fetch → controlled activation → runtime policy → monitoring → credential rotation/incident recovery`.

Security must cover every authority transition. HTTPS protects transport to the origin; it does not prove that the origin, CI/CD pipeline, dependency graph, deployment credential, or published artifact is trustworthy.

Guard: `HTTPS delivered ≠ intended artifact delivered ≠ authorized artifact built ≠ dependency graph uncompromised`.

## SOURCE — Service Worker is a high-impact execution/update boundary
MDN documents `ServiceWorkerContainer.register()` as secure-context only and explicitly treats `scriptURL` as an injection sink. A registered worker can intercept requests within its scope and return fresh, cached, new, or modified responses. MDN recommends constraining worker script locations with CSP `worker-src` (falling back to `script-src`/`default-src`) and, where Trusted Types is enforced, using `TrustedScriptURL` rather than unconstrained strings.

Service-worker registration persists beyond individual page objects. Updates fetch the worker script and install a new worker when the fetched script differs byte-for-byte from the incumbent. `updateViaCache` controls whether HTTP cache participates for worker scripts/imports; it does **not** authenticate who was authorized to publish the bytes.

**SYNTHESIS:** a compromised worker publication path has durable blast radius because the browser deliberately grants the worker request-interception authority over its scope and preserves registration across visits.

Guard: `service-worker byte change detected ≠ legitimate release authorized`.

## SOURCE — Worker CSP is its own response policy
MDN CSP documentation states that workers generally are not governed by the CSP of the document that created them. To apply CSP to a worker, the worker script response itself needs an appropriate `Content-Security-Policy` header (with limited special cases such as globally unique URLs).

**SYNTHESIS:** a strong page CSP cannot be assumed to secure code execution inside the service worker. Page policy and worker-response policy are separate enforcement surfaces and must be reviewed separately.

Guard: `page CSP strong ≠ service-worker CSP strong`.

## SOURCE — CI/CD and dependency systems are security boundaries
OWASP Top 10:2025 A03 classifies software supply-chain failures as a primary application risk and recommends hardening repositories/build systems, restricting IAM, protecting CI/CD changes, preserving provenance/signatures/timestamps for artifacts, promoting immutable artifacts rather than rebuilding independently per environment, maintaining SBOM/component visibility, and using staged/canary deployment rather than updating every system simultaneously.

OWASP Cornucopia CLD5 models malicious build/deployment injection through unprotected variables or pipeline configuration and emphasizes that pipelines often possess production deployment authority. It recommends dedicated secret management, short-lived credentials, protected/reviewed pipeline changes, restricted production-trigger paths and audit logging.

OWASP Dependency-Track illustrates the operational SBOM model: produce an inventory, continuously analyze components against vulnerability/policy intelligence, govern policy and respond over the application lifecycle.

**SYNTHESIS:** supply-chain security is not `run dependency scanner`. The trust graph includes source control, workflow definitions, build runners, package registries, dependency locks, generated artifacts, deployment identity, CDN/origin configuration and emergency recovery authority.

## 1. Threat model by trust transition

### Source/review threats
- compromised maintainer account;
- malicious or mistaken source change;
- workflow/configuration change hidden inside ordinary product work;
- bypassed review/branch controls;
- generated/binary artifact not traceable to reviewed source.

### Dependency/build threats
- malicious dependency/version takeover;
- lockfile drift or unreviewed transitive change;
- compromised package registry or build tool;
- compromised runner/action/plugin;
- secrets exposed to untrusted build context;
- non-reproducible or environment-dependent output that breaks provenance comparison.

### Publication threats
- stolen long-lived deployment credential;
- wrong environment/branch published;
- mutable artifact replaced after approval;
- origin/CDN/storage write compromise;
- cache retaining an unsafe generation after origin repair;
- DNS/account/provider compromise outside application source control.

### Browser/update threats
- unsafe worker scope;
- dynamic/untrusted worker URL construction;
- page policy assumed to cover worker policy;
- activation before data/schema compatibility is known;
- long-offline client skipping directly across compromised/repaired generations;
- incident response that clears authoritative local records to remove bad caches.

## 2. Release trust record
For every production-capable PWA release preserve a machine-correlatable record of:
- source commit/revision;
- reviewed workflow/configuration revision;
- dependency lock/SBOM identity;
- build invocation and trusted builder identity;
- immutable artifact digest;
- environment/configuration identity excluding secret values;
- deployment actor/workload identity;
- target origin/environment;
- publication timestamp;
- worker/shell/schema/protocol generations;
- promotion/approval evidence;
- rollback/forward-fix compatibility statement;
- acceptance evidence IDs;
- incident/revocation status.

The record should allow answering: **which reviewed source and dependency set produced the exact bytes that this origin was authorized to serve?**

Guard: `commit SHA known ≠ deployed bytes proven`.

## 3. Build once, promote the same artifact
Where architecture permits, prefer producing an immutable release artifact once and promoting the same identified bytes across acceptance/staging/production rather than rebuilding independently for each environment. Environment-specific runtime configuration must be designed so it does not silently convert promotion into a different untracked executable artifact.

Benefits:
- stronger source→artifact→production correlation;
- smaller environment drift surface;
- incident comparison can use exact digests;
- acceptance evidence can attach to the promoted artifact rather than merely a branch name.

**OPEN:** exact LogMate/MintTap hosting/build architecture is not verified here; this is a governance requirement, not an assertion that current projects support artifact promotion unchanged.

## 4. Deployment identity and least authority
Production deployment should not rely on broadly reusable, long-lived credentials where short-lived workload identity is available. Separate at minimum:
- source contribution authority;
- workflow modification authority;
- build execution authority;
- artifact publication authority;
- production configuration authority;
- DNS/domain authority;
- emergency revocation/rotation authority.

A single compromised developer token should not automatically imply production publication + DNS takeover + secret disclosure.

Required controls are implementation/provider-specific and belong to Software Engineering/operations validation. The Web Manager requirement is **bounded, auditable, revocable deployment authority with no unnecessary credential reuse**.

## 5. Service-worker publication contract
Because a worker can control many clients and persist across visits:
1. worker script URL is fixed or selected from a tightly controlled allowlist; never user-controlled;
2. registration scope is deliberately minimal for the product requirement;
3. `Service-Worker-Allowed` is not broadened casually;
4. worker script response has explicit CSP appropriate to worker execution;
5. page CSP separately constrains worker creation with `worker-src` where applicable;
6. Trusted Types/`TrustedScriptURL` is evaluated where dynamic script URL sinks exist and browser/product support makes it appropriate;
7. worker and imported-code update/cache policy is explicit (`updateViaCache` semantics understood rather than assumed);
8. activation follows 088–091 compatibility/data-preservation gates;
9. release identity is observable without exposing user payloads;
10. emergency repair accounts for already-installed offline workers that cannot receive remote containment.

## 6. CSP and Trusted Types boundaries
CSP reduces classes of unauthorized code/resource execution when correctly designed, but it is not artifact provenance and cannot rescue a legitimately authorized-but-compromised deployment pipeline.

Trusted Types addresses DOM/script injection sinks by forcing values through approved policies; it does not prove dependency provenance, protect a stolen production deploy credential, or authenticate the semantic intent of a service-worker release.

Therefore:
`CSP/Trusted Types → runtime injection containment layer`
`provenance/review/deploy IAM → release authorization layer`
`worker lifecycle/compatibility → update safety layer`
`backup/outbox/recovery → data survival layer`.

No one layer substitutes for the others.

## 7. Third-party code and CDN policy
For an offline-capable PWA, third-party runtime dependencies expand both availability and trust boundaries. Prefer minimizing code that must execute from third-party origins at runtime, especially inside the worker path. If a dependency is required, decide whether it is:
- vendored/bundled into the immutable application artifact;
- fetched from a third party at runtime;
- allowed in page context only;
- allowed in worker context;
- essential offline or optional enhancement.

A CDN improves delivery but does not create trust. If the CDN/origin publication account is compromised, valid HTTPS can deliver malicious content. Recovery therefore needs provider-account security, deployment auditability, origin/CDN purge/revalidation procedure and exact artifact comparison.

Guard: `valid certificate ≠ trustworthy publisher state`.

## 8. Dependency/SBOM lifecycle
Maintain enough component identity to answer after release:
- which direct/transitive versions were included;
- which release generations contain a newly disclosed vulnerable component;
- whether the vulnerable component is reachable/executable in page/worker/build-only context;
- whether remediation requires rebuild, configuration change or no product action;
- which offline clients may still hold the affected generation.

SBOM/inventory is evidence infrastructure, not an automatic risk verdict. Vulnerability severity, exploitability, runtime reachability, browser sandbox/context and product data exposure still require judgment.

## 9. Compromised-update incident model
If a malicious/unauthorized release may have reached production:

### Immediate priorities
`stop further publication → preserve evidence → identify exact artifact/digest/time window → revoke/rotate compromised credentials → restrict smallest unsafe server capability → publish verified repair through an independently re-established trust path → preserve authoritative local records/outbox → reconcile affected clients`.

Do not make `clear website data` the default containment action: a client may hold the only unsynchronized authoritative record.

### Determine blast radius
- was the bad artifact published or merely built?
- did worker script bytes change?
- which scope did the worker control?
- was activation reached or only waiting/installing?
- which network/API credentials or data could executing code access?
- could the malicious worker modify cached shell/API responses or exfiltrate local data while online?
- which installed clients were offline and therefore never fetched the bad generation?
- which clients fetched it but later went offline?
- did server-side capability containment limit harm?

### Recovery invariant
A repaired origin is insufficient. Installed clients may retain a previously activated worker/cache. Recovery evidence must show the intended clean generation controls the client **and** authoritative user data/outbox survived and reconciles correctly.

Guard: `origin repaired ≠ installed fleet clean`.

## 10. Credential/key rotation
Rotation plans must distinguish:
- source-control/user credentials;
- CI workload/deploy credentials;
- hosting/CDN/provider credentials;
- API/backend credentials;
- TLS/domain/DNS account authority;
- application/session/token keys where relevant;
- local-data encryption/recovery keys if the product introduces them.

Rotating one class does not invalidate the others. Rotation also needs a recovery authority that is not dependent on the same compromised credential path.

**OPEN:** no MintTap/LogMate credential topology is asserted by this research.

## 11. Staged release as security containment
091 established staged rollout for compatibility diversity. 092 adds a security reason: limiting initial exposure can reduce blast radius from an authorized-but-defective or compromised release. However, installed/offline PWAs complicate percentage-based rollout because update fetch timing is client-driven and silent clients are not represented in current traffic.

Therefore release gates should combine:
- exact artifact identity;
- limited initial publication/promotion where infrastructure permits;
- anomaly/security monitoring;
- generation-diverse compatibility fixtures;
- capability-scoped server containment;
- explicit decision to expand rollout;
- ability to identify/repair installed worker generations.

Guard: `canary origin traffic clean ≠ long-offline installed fleet safe`.

## 12. Cross-track transfer
### Track A — Platform/Browser
Owns service-worker registration/scope/update/cache mechanics. Transfer: security decisions must distinguish browser update mechanics from authorization/provenance. Browser byte comparison detects change, not legitimacy.

### Track B — UX/IA/Content
Consumes incident states: update paused, security repair available, local records preserved, sync temporarily restricted, recovery required. Wording must avoid false claims such as “secure now” before client-generation/data invariants are verified. Visual/interaction execution remains Design Studio-owned.

### Track C — Performance/Accessibility/Quality
Adds release-security oracles: exact artifact digest, worker generation, clean-update path, offline-return repair, no destructive recovery, accessible incident/recovery state. Security headers/scanners are supporting evidence, not the whole release gate.

### Track D — Search/Discovery/Analytics
Consumes minimized release-generation/incident evidence. Analytics cannot certify compromise absence because offline/silent clients do not report and security telemetry may intentionally omit sensitive detail.

### Track E — Architecture/Security/Operations
Remains owner. 092 closes generic trust boundaries from source through installed worker and incident recovery. Exact CI/hosting/IAM/product validation remains OPEN.

## 13. Cross-repository transfer
### Design Studio
Latest Web status checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W043 temporal provenance runtime is ready but execution OPEN. Transfer: security/update/recovery messaging needs trustworthy chronology and authority/freshness semantics, but no Safari/cross-browser/AT/physical-device/human-UX PASS is inferred.

### Software Engineering Studio
Latest repository evidence checked 2026-09-17: Foundation IN STUDY; D005 recovery/publication evidence remains the newest relevant executable block. Transfer: artifact publication/integrity and semantic recovery are separate. 092 requires Software Engineering to validate actual source→build→artifact→deploy provenance, credential boundaries, dependency locks/SBOM, and repair/rotation procedures rather than Web Manager inventing implementation details.

## 14. Five-track balance after 092
- **A:** strong; worker mechanics are sufficient for this decision layer, with browser/WebKit details CHANGE WATCH.
- **B:** strong generic state architecture; security incident wording/interaction needs product + Design Studio validation.
- **C:** strong generic release/fault architecture; exact security/recovery tests on Safari/managed iPad remain OPEN.
- **D:** not the bottleneck; consumes bounded release/incident measurement and silent-client caveats.
- **E:** received the dominant allocation because release trust was the highest-risk unresolved generic bottleneck. Generic supply-chain/update-integrity governance now reaches PASS; implementation evidence is the next dependency.

## MINTTAP / LOGMATE DIRECTION
For any PWA carrying irreplaceable user data, treat the update channel as privileged code deployment. Require traceability from reviewed source/dependency set to immutable artifact and authorized production publication; constrain worker scope/execution policy; preserve exact release identity; and design compromised-update recovery that does not destroy unsynchronized local records.

This is a direction/acceptance contract, not a claim that current MintTap or LogMate infrastructure already satisfies it.

## OPEN / VALIDATION
- actual GitHub branch/ruleset/review enforcement for product repositories;
- actual CI runner/action trust model and dependency pinning;
- actual SBOM/provenance/signing mechanism;
- actual hosting/CDN/origin and production deploy identity;
- actual secret/workload-identity model;
- CSP/Trusted Types feasibility against real Flutter/PWA output;
- worker-response CSP and registration scope on exact product artifact;
- provider/DNS emergency recovery authority;
- credential/key rotation drill;
- compromised-worker clean-repair behavior on physical managed iPad;
- AT-accessible incident/recovery UX;
- privacy/legal approval for security diagnostics and retention.

## CHANGE WATCH
- Service Worker specification/WebKit implementation;
- CSP Level 3 and Trusted Types browser support/behavior;
- OWASP supply-chain guidance and ecosystem attack patterns;
- provider/GitHub workload identity, provenance and artifact-attestation capabilities;
- actual product build/deployment architecture once implementation exists.

## Competency checkpoint
**PASS at generic expert security/operations level.** Web Manager can distinguish transport security from release authorization, reason about service-worker-specific trust, define source→artifact→deployment evidence, separate CSP/Trusted Types from provenance, design narrow incident containment, and specify non-destructive compromised-update recovery. Product/production certification remains OPEN.

## Sources
- MDN, `ServiceWorkerContainer.register()`, current page accessed 2026-09-17.
- MDN, `ServiceWorkerRegistration.updateViaCache`, current page accessed 2026-09-17.
- MDN, `ServiceWorkerRegistration.update()`, current page accessed 2026-09-17.
- MDN, `Content-Security-Policy (CSP) header`, worker CSP section, current page accessed 2026-09-17.
- OWASP Top 10:2025, A03 Software Supply Chain Failures, accessed 2026-09-17.
- OWASP Cornucopia CLD5, CI/CD build/deployment variable compromise scenario, accessed 2026-09-17.
- OWASP Dependency-Track project overview, accessed 2026-09-17.
- `yhappcom/design-studio` `progress/WEB_STATUS.md`, checked 2026-09-17.
- `yhappcom/software-engineering-studio` latest D005-related repository evidence, checked 2026-09-17.