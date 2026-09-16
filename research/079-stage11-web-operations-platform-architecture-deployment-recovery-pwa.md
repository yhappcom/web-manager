# 079 — Stage 11 Web Operations & Platform Architecture: Deployment, Recovery & PWA Lifecycle

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER INTEGRATED CHECKPOINT**
Primary owner: **E Web Architecture, Security & Operations**
Consumers: A Platform/Browser; C Performance/Accessibility/Quality; D Search/Discovery/Analytics; B UX/IA/Content; Software Engineering.

## Purpose
Build the first integrated Stage 11 operating model from requirements through hosting/rendering topology, environments, deployment, cache invalidation, observability, rollback/recovery and provider portability. PWA/service-worker clients are a major application case because origin deployment and client activation are separate state transitions. No MintTap production architecture is inferred.

## SOURCE — authoritative evidence rechecked 2026-09-16
- Firebase Hosting documentation: local emulation, temporary preview channels, live deployment and version cloning are separate operations. Google recommends a separate Firebase project for testing/development to protect production resources from accidental changes. Preview URLs are public to anyone who knows them and normally interact with real backend resources unless pinned/emulated behavior is deliberately configured.
- Firebase Hosting management documentation: live Hosting retains previous releases so a live channel can be rolled back to a previously served version. Cloning a tested preview version to live can preserve the exact Hosting version/content/config that was reviewed.
- Firebase App Hosting documentation: rollback can restore an existing previous container image without rebuilding, or rebuild an earlier commit against current configuration. These are operationally different rollback semantics.
- Cloudflare Cache documentation: cache invalidation can be targeted by URL/tag/hostname/prefix or broad. Cloudflare recommends targeted single-file purge over purge-everything; broad purge can sharply increase origin load. Custom cache keys alter what must be identified for correct purge.
- W3C Service Workers current publication: service workers are event-driven workers with an independently managed lifecycle. Secure Contexts defines the trustworthy-environment model used by powerful web capabilities.
- MDN Service Worker documentation, aligned to the specification: a changed worker can install in the background and remain waiting while an old worker controls existing pages. `skipWaiting()` and `clients.claim()` can accelerate takeover but change compatibility risk; activation is not equivalent to every open client having reloaded into a coherent new application generation.
- WebKit current Safari release material continues to ship/fix service-worker behavior, confirming browser/runtime behavior is a CHANGE WATCH and Safari/iPadOS must be validated rather than inferred from Chromium.

## 1. First-principles architecture model
Architecture is not provider selection. Begin with required behavior and failure tolerance:

`user/task requirements → content/runtime state → rendering/execution model → origin/backend dependencies → edge/CDN/cache → DNS/TLS → deployment/version state → client/browser state → observation → recovery`

A provider is one implementation of parts of this chain.

### Required separations
- static content ≠ dynamic computation;
- build artifact ≠ deployed release;
- deployment success ≠ healthy release;
- origin version ≠ edge-cache version ≠ service-worker version ≠ open-client version;
- rollback of web bytes ≠ rollback of database/schema/user data;
- preview environment ≠ production-equivalent environment;
- cache purge ≠ application rollback;
- monitoring signal ≠ root cause;
- backup ≠ rollback ≠ disaster recovery;
- provider convenience ≠ portability.

## 2. Rendering/hosting choice is requirements-led
Evaluate static generation/static hosting, SSR/server rendering, CSR/client rendering and hybrid models by:
- freshness and personalization requirements;
- public crawlable content needs;
- authenticated/user-specific state;
- latency and geographic distribution;
- runtime/backend dependency;
- failure mode and offline behavior;
- deployment/rollback complexity;
- security surface;
- cost and operational ownership.

**SYNTHESIS:** an app-company marketing/support site can often have a different architecture from an offline-capable PWA product. Sharing a domain or design system does not require sharing runtime architecture.

**MINTTAP DIRECTION:** do not select Firebase Hosting, App Hosting, Cloudflare, SSR or another stack until actual `minttap.app` route/runtime requirements are inspected. Existing Firebase familiarity is not sufficient architectural evidence.

## 3. Environment topology and release lineage
Minimum conceptual states:
`local/dev → review/preview → production`.

Environment separation must consider not just frontend URL but backend/database/storage/auth/analytics and secrets. A preview frontend pointed at production data is not a harmless sandbox.

Create an **Environment Contract** with:
- environment purpose;
- deploy source/ref;
- frontend origin;
- backend/data targets;
- authentication identity/tenant;
- secrets/config source;
- analytics destination;
- external integrations;
- test-data policy;
- access policy;
- retention/expiration;
- promotion rule.

Create a **Release Lineage Record**:
`source commit → build/toolchain → immutable artifact/version → environment → deployment/release ID → config/schema dependencies → validation evidence → promotion/rollback relation`.

A release that cannot be traced to source, artifact and config is operationally weak even if it works now.

## 4. Deployment atomicity and compatibility
A release may update several independently cached/deployed components. Treat compatibility as a matrix rather than assuming synchronized replacement.

Examples:
- HTML N referencing hashed JS N while old HTML remains cached;
- new JS calling API N+1 while API N still serves some traffic;
- new service worker serving old cached shell;
- old offline PWA returning after several releases;
- new client opening an older IndexedDB schema;
- rollback frontend encountering forward-migrated persistent data.

Use a **Deployment Compatibility Window**:
- current release;
- previous supported client generations;
- API compatibility range;
- schema compatibility range;
- cache generations;
- service-worker generations;
- required forward/backward compatibility;
- expiry/removal condition.

**CONTRADICTION:** “deploy all components together” is not proof of atomic user-visible deployment. DNS, CDN, browser cache, service workers, open tabs, offline clients and rollout systems create distributed state.

## 5. Cache architecture and invalidation
Caching is a correctness system as well as a performance system.

Classify each resource:
1. immutable/versioned asset — long reuse is normally safe when URL changes with content;
2. mutable shell/document — freshness and revalidation matter;
3. API/data response — user/data semantics determine cacheability;
4. service-worker-controlled response — browser HTTP cache and Cache Storage/service-worker policy are separate layers.

Create a **Cache Ownership Map**:
`resource → cache layer → key → freshness rule → invalidation mechanism → owner → validation signal`.

Prefer content-addressed/hashed immutable assets where appropriate, bounded freshness for mutable documents, and targeted invalidation. Broad purge is an emergency/control option, not a substitute for correct cache design.

A purge can also increase origin load; therefore cache recovery must include origin-capacity consequences.

## 6. PWA release topology
PWA deployment adds a client-managed execution/cache generation:

`origin release N+1 → worker update check → installing → waiting → activating → controlling client → client reload/navigation → cache/schema compatibility`.

The browser may keep worker N controlling existing clients while N+1 waits. Forcing `skipWaiting()`/`clients.claim()` can reduce waiting but can also create a page loaded with N assets/state suddenly controlled by N+1 fetch behavior. Therefore immediate takeover is a compatibility decision, not a generic best practice.

### Safe update contract
Define:
- how update availability is detected;
- whether activation is automatic, user-confirmed or task-boundary-triggered;
- what happens to unsaved local work;
- worker/cache version compatibility;
- IndexedDB/schema migration order;
- outbox/sync protocol compatibility;
- stale-client minimum supported version;
- recovery when an offline client skips multiple releases;
- behavior when network disappears mid-update;
- observability that does not become product-state authority.

For an EFB-like managed iPad, assume neither background update nor prompt timing nor storage persistence nor unattended synchronization until physical Safari/Home Screen validation exists.

## 7. Rollback is multi-layer recovery
Define separately:
- **release rollback**: serve previous known web artifact;
- **configuration rollback**: restore previous config/secrets/routing policy where possible;
- **cache recovery**: invalidate/repopulate bad cached objects;
- **application forward-fix**: deploy a new version compatible with state already changed;
- **data recovery**: restore/reconcile persistent data from a defined recovery mechanism;
- **service-worker recovery**: replace or neutralize a bad worker/cache generation.

A previous frontend artifact may be unsafe after irreversible database/schema migration. Hence “rollback button exists” ≠ “system is safely rollbackable.”

Create a **Recovery Decision Record**:
`incident scope → affected layers/population → current persistent-state compatibility → rollback candidate → forward-fix candidate → cache action → data action → validation → communication → post-incident evidence`.

## 8. Observability model
Observe user-visible outcomes and causal layers:
- DNS/TLS/HTTP availability;
- edge/origin status and latency;
- deploy/version identity;
- browser errors and failed resources;
- Core Web Vitals/task readiness where applicable;
- API/backend health;
- service-worker registration/version/update failures;
- offline/cache failures;
- sync/outbox/reconciliation state for product telemetry, while never treating analytics delivery as sync truth;
- support/user reports.

Every signal needs population, time window, version/environment and known missingness. A dashboard without release lineage cannot reliably answer “what changed?”

## 9. Incident and rollback gate
A practical sequence:
`detect → scope → identify release/config/environment → stabilize → choose rollback/forward-fix/cache/data action → verify critical tasks → communicate bounded facts → monitor → preserve evidence → postmortem/action`.

Do not purge caches, unregister workers, roll back backend or restore data reflexively. Each action changes evidence and can enlarge impact.

## 10. Dependency/update governance
Track runtime/framework/build/deployment dependencies by:
- owner and purpose;
- current version/source;
- security/update channel;
- compatibility constraints;
- browser/platform dependency;
- build reproducibility;
- removal/replaceability;
- validation required before update.

Software Engineering owns implementation/code dependency practice. Web Operations owns production-web requirements, release evidence and failure/recovery implications.

## 11. Provider evaluation without premature commitment
Compare providers against requirements using:
- static/dynamic/runtime support;
- custom domains/TLS;
- CDN/cache controls;
- preview/environment model;
- deployment atomicity/version retention;
- rollback semantics;
- observability/log access;
- security controls;
- data/runtime locality requirements;
- automation/API/IaC support;
- pricing at expected traffic and failure bursts;
- exportability/artifact portability;
- proprietary configuration/data coupling;
- operational complexity and team skill.

Create a **Portability Ledger**:
`capability → standard/portable layer → provider-specific dependency → exit cost → migration evidence/mitigation`.

Lock-in is not automatically bad. It becomes a risk when convenience is accepted without understanding replacement cost or operational dependency.

## 12. Failure diagnostics
### A. New deploy is live but some users still see old UI
Do not immediately redeploy. Identify document cache, CDN edge, browser HTTP cache, service-worker controller, open-client generation and rollout population.

### B. Rollback succeeds in Hosting but PWA remains broken
Old/bad worker or Cache Storage may still control clients, or persistent schema changed. Origin rollback is only one layer.

### C. Preview passed but production fails
Check environment contract: backend targets, secrets, origin/CORS, production cache/CDN, auth, analytics/consent and traffic characteristics may differ.

### D. Purge-everything fixes stale content but origin latency spikes
The cache action created a thundering refill/origin-load problem. Replace emergency broad purge with targeted invalidation and capacity-aware recovery.

### E. Offline iPad returns after months and cannot sync
Treat as skipped-version compatibility and data reconciliation, not “network failure.” Validate worker/client/schema/outbox/protocol versions and provide bounded recovery/export path.

## 13. Cross-track transfers
- **A Platform/Browser:** owns HTTP/browser/cache/service-worker mechanics consumed here.
- **B UX/IA/Content:** update/offline/maintenance/recovery states need truthful user communication and task-safe interruption points.
- **C Quality:** release gates need performance/accessibility/cross-browser/device regression evidence; production validation remains OPEN.
- **D Search/Analytics:** migrations, status codes, canonical URLs and instrumentation need release lineage; analytics cannot certify deployment correctness.
- **Design Studio:** update/error/offline/recovery UI requirements transfer without Web Manager inventing visual solutions.
- **Software Engineering:** actual CI/CD, schema migration, API compatibility, service-worker code, sync protocol and automated tests require implementation evidence.

## 14. MintTap / LogMate facts still OPEN
- actual framework/rendering model;
- Firebase Hosting/App Hosting or other provider usage;
- DNS/CDN/origin topology;
- preview/staging/production separation;
- CI/CD and branch/release policy;
- cache headers/keys/purge controls;
- service-worker code/update strategy;
- IndexedDB/schema migration strategy;
- observability/logging/alerts;
- rollback/data recovery capability;
- dependency inventory;
- backup/RPO/RTO requirements;
- EFB physical iPad behavior and management restrictions.

## 15. PROJECT TRANSFER — LogMate EFB offline preview regression and artifact provenance

**Evidence date:** 2026-09-16.  
**Product authority:** `yhappcom/logmate`; Web Manager does not own the product fix or current product PASS/FAIL state.

A current LogMate EFB Safari acceptance attempt exposed a reusable operations failure class: the tested preview artifact was created through a direct generic Flutter Web build path while the product repository already contained a canonical PWA build path with additional offline requirements. The direct preview rendered online but produced a white screen on physical EFB Safari after termination and offline re-entry. Historical LogMate POC evidence had already recorded similar white-screen iterations and a successful offline path using CDN-free web resources, bundled local fonts, full generated-resource precache, fresh preview origin, and actual readable first-frame validation.

The current product source separately shows a first-frame-safe startup pattern (`runApp()` before asynchronous Firebase restoration), so the historical pre-first-frame Firebase-blocking failure should be compared but not assumed to be the current cause. The failed preview remains valid evidence **for that exact artifact and scenario**; root cause remains OPEN until the canonical product PWA build/deploy path is reproduced.

### Transfer classification
- historical POC white-screen evidence: **TRANSFER CANDIDATE**, not current-product PASS;
- current direct-build EFB white screen: **VALIDATION FAILURE for the tested artifact**;
- generic attribution to IndexedDB, Safari support, or LogMate application logic: **NOT ESTABLISHED**;
- canonical PWA rebuild on a fresh origin: **REQUIRED next isolation step** before speculative product-code changes.

### Reusable Web Operations rule — canonical artifact provenance
For PWA/offline acceptance, a source commit is insufficient identity. Record:

`source ref → canonical build target/command → toolchain/lock → required build flags → post-build service-worker/asset transforms → artifact/deployment ID → fresh/reused origin → browser/device/OS → observed first-frame/data result`.

If a repository defines required offline build/post-build steps, a direct framework build that bypasses them is a **different artifact class**. Its failure must not be promoted to a failure of the canonical PWA path until reproduced there.

### PWA acceptance guard
Before physical offline acceptance:
1. verify the artifact was produced by the canonical PWA target or a proven equivalent;
2. verify required local renderer/font/static assets are present and no prohibited runtime CDN dependency remains;
3. verify the generated service worker contains the intended precache/navigation behavior after all post-build transforms;
4. use a fresh or explicitly version-isolated preview origin when stale worker/cache state would confound the result;
5. validate the **actual readable application first frame**, not merely HTML DOM, runtime bootstrap, worker activation or cache presence;
6. only after shell/readability PASS, evaluate IndexedDB/data persistence and higher-level task behavior;
7. preserve failed artifacts and their provenance rather than erasing them after a later PASS.

### Handoff — Web Manager → Software Engineering / LogMate
Software Engineering should convert this from a human-memory rule into executable build/release checks where practical: canonical build target enforcement, artifact provenance capture, post-build worker/asset assertions, prohibited remote-runtime dependency checks, and offline fresh-navigation regression coverage. LogMate remains the authority for exact commands, code, CI and physical EFB acceptance evidence.

## 16. Competency gate
PASS this checkpoint if Web Manager can:
1. derive architecture from requirements instead of provider preference;
2. separate origin/edge/browser/service-worker/client/data versions;
3. define environment and release lineage;
4. diagnose cache invalidation by layer/key/owner;
5. distinguish rollback, cache recovery, forward-fix and data recovery;
6. reason about PWA waiting/activation and mixed-version compatibility;
7. define observability with version/population/missingness context;
8. evaluate provider convenience against portability/exit cost;
9. identify implementation evidence that belongs to Software Engineering;
10. keep all MintTap production claims OPEN until runtime evidence exists.

**Result: PASS — Stage 11 first integrated foundation/practitioner checkpoint.**

## Next adjacent work
Continue Stage 11 with **operational reliability and architecture stress testing**: DNS/domain/TLS operations, origin/CDN failure domains, CI/CD promotion and secret/config governance, monitoring/SLO/incident evidence, backup/RPO/RTO/disaster recovery, dependency/supply-chain release operations, and provider portability/cost scenarios. Deepen PWA recovery with bad-worker kill/recovery patterns, schema migrations, stale offline clients and physical Safari/iPad validation requirements before Stage 11 closure. Carry the LogMate artifact-provenance incident into future release-gate examples so canonical PWA build equivalence is tested rather than assumed.
