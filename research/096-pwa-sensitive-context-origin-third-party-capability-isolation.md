# 096 — PWA Sensitive-Context Origin, Third-Party Isolation & Capability Minimization

Status: **PASS (generic) / PRODUCT TOPOLOGY + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A origin/Service Worker/storage/CSP mechanics; Track B state and continuity requirements; Track C security/compatibility validation; Track D analytics/discovery requirements; 092 supply-chain trust; 093 authorization/local-data separation; 095 runtime-origin compromise.

## 1. Problem and decision pressure

095 established that encryption at rest does not protect locally unlocked records from hostile code already executing with the application's origin authority. The adjacent architectural question is therefore not merely which scripts are trustworthy, but **which web surfaces should possess the same browser authority at all**.

A multi-surface app company may have:
- public company/product/SEO pages;
- marketing analytics and campaign measurement;
- advertising or affiliate integrations;
- support/chat/feedback widgets;
- authentication/account surfaces;
- an installable PWA with Service Worker control;
- locally authoritative offline records and durable outbox;
- diagnostic/export/recovery functions.

Putting these under one hostname/path tree is operationally simple, but paths are not browser security principals. Conversely, moving every feature to another origin can create authentication, accessibility, navigation, deployment and support complexity. The objective is **least browser authority consistent with product requirements**, not maximal fragmentation.

## 2. SOURCE — platform mechanics

### 2.1 Origin is scheme/host/port, not path

MDN's Same-Origin Policy documentation defines an origin by scheme, host and port. URLs differing only by path remain same-origin. Browser storage such as Web Storage and IndexedDB is separated by origin, not by application route.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy (checked 2026-09-17).

**SYNTHESIS:** `/marketing`, `/support` and `/app` on the same scheme/host/port do not create script/storage security boundaries merely because the application router treats them as different products.

Canonical guard:

`different path ≠ different origin security boundary`.

### 2.2 Service Worker scope is a routing/control boundary, but not a complete origin boundary

Service Workers register against an origin and control clients within registration scope. Default scope follows the worker script directory; `Service-Worker-Allowed` can broaden permitted scope. Registrations persist beyond a single page object's lifetime.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers and https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration (checked 2026-09-17).

**SYNTHESIS:** Narrowing worker scope can reduce accidental control of public routes, but a narrower worker scope does not turn two same-origin paths into mutually distrustful security principals. Same-origin page script/storage relationships remain relevant.

Canonical guard:

`narrow Service Worker scope ≠ independent origin isolation`.

### 2.3 CSP limits resource and connection authority, but policy is response/context specific

`connect-src` constrains destinations reachable through script interfaces including `fetch`, XHR, WebSocket, EventSource and `sendBeacon`. `frame-src` constrains iframe sources; `frame-ancestors` constrains who may embed a document. `default-src` is a fallback for fetch directives. Workers generally require their own CSP response header rather than inheriting the creator document's policy.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src ; https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-src ; https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors ; https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy (checked 2026-09-17).

**SYNTHESIS:** A sensitive PWA can have a materially narrower script/network authority budget than a public marketing page. This is useful even when origins are shared, but it is defense-in-depth rather than a substitute for origin separation where mutual distrust is required.

Canonical guard:

`CSP destination minimization ≠ malicious same-origin code loses all application authority`.

### 2.4 iframe sandbox can reduce embedded authority, with important escape/compatibility constraints

The iframe/CSP sandbox model can remove script, same-origin, navigation, popup and other capabilities unless selectively restored. MDN explicitly warns that same-origin embedded content given both `allow-scripts` and `allow-same-origin` can remove the sandbox attribute, making that configuration ineffective as a same-origin containment mechanism. Content that may be opened outside the sandbox should also be served from a separate origin when damage limitation matters.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe and https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/sandbox (checked 2026-09-17).

Canonical guard:

`sandbox attribute present ≠ embedded third party safely contained`.

### 2.5 Permissions Policy is capability delegation, not code trust

Permissions Policy can control access to selected browser features at a top-level document and in iframes; iframe `allow` can further constrain an individual embedded context.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Permissions_Policy (checked 2026-09-17).

**SYNTHESIS:** Third-party support/media widgets should not automatically inherit camera, microphone, geolocation or other powerful features. Permissions Policy narrows browser-feature authority, but it does not sanitize hostile JS or prevent network exfiltration through otherwise allowed channels.

### 2.6 Cross-origin embedding does not imply zero state relationship

The Storage Access API exists specifically because cross-site embedded content may need user-agent-mediated access to unpartitioned cookies/state that browsers otherwise restrict. Browser behavior differs, and permission activation can be contextual. Partitioned cookies/CHIPS provide a different model in which cookie state is partitioned by top-level site.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API and https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Third-party_cookies/Partitioned_cookies (checked 2026-09-17).

**CHANGE WATCH:** Storage-access prompts, third-party cookie policy, partitioning and browser-specific behavior are active platform areas. Do not encode one browser's current behavior as a permanent product invariant.

Canonical guard:

`cross-origin iframe ≠ no cookie/storage relationship`.

### 2.7 Cross-origin requests can deliberately carry credentials

Fetch request credentials default to `same-origin`; `include` can send credentials cross-origin subject to applicable CORS/cookie rules.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials (checked 2026-09-17).

**SYNTHESIS:** Origin separation reduces ambient same-origin authority, but application architecture can deliberately rebuild cross-origin authority through credentialed APIs, CORS, postMessage, storage-access grants or shared identity systems. These bridges are security contracts and must be explicit.

Canonical guard:

`different origin ≠ no trust bridge`.

### 2.8 SRI addresses unexpected subresource modification, not complete third-party isolation

Subresource Integrity lets a browser verify that a fetched resource matches an expected cryptographic hash and is useful against unexpected modification of externally hosted static resources.

SOURCE: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity (checked 2026-09-17).

**SYNTHESIS:** SRI is useful where compatible immutable external scripts/styles are unavoidable, but it does not constrain an intentionally updated third-party script to a safe capability set, and it does not protect APIs/widgets whose runtime behavior depends on remote code/data outside the hashed resource.

## 3. History/problem → design principle

Traditional brochure sites often treated analytics, ads, support and product JavaScript as peers because little irreplaceable client-side state existed. An offline-first PWA changes the consequence model: the browser origin may now contain authoritative unsynchronized records, cryptographic capabilities, durable outbox and a persistent Service Worker.

Therefore the design principle is:

> **Execution authority should follow data/task sensitivity, not organizational convenience or URL taxonomy.**

The relevant question for every script, frame and endpoint is not only “is this vendor reputable?” but:
1. Must it execute in the sensitive application document?
2. Must it read the application DOM/state?
3. Must it share the application's storage/authentication authority?
4. Must it contact arbitrary destinations?
5. Must it be controlled by the same Service Worker?
6. What breaks if its authority is removed?

## 4. Surface/capability classification

Use a capability inventory before choosing topology.

| Surface | Typical need | Authority that is *not automatically required* |
|---|---|---|
| public company/product pages | crawlable content, store links, public analytics | IndexedDB/outbox, local unlock, PWA record APIs |
| campaign/marketing page | attribution/conversion measurement | authoritative offline record access |
| advertising/affiliate | rendering/click measurement | app storage, auth tokens, broad `connect-src`, Service Worker control |
| support docs | public help/search | unlocked user records |
| support widget/chat | user-initiated support channel | arbitrary DOM/storage access; direct record dump |
| auth/account | identity/session operations | broad marketing script graph |
| sensitive offline PWA | local records, sync, export/recovery | ads/tag managers/support scripts by default |
| diagnostics | structural health evidence | record contents, session secrets, unrestricted network authority |

**MINTTAP DIRECTION:** This is a requirements matrix, not a claim about the current MintTap or LogMate implementation. Exact product surfaces and vendors remain OPEN.

## 5. Architecture patterns and trade-offs

### Pattern A — one origin, one execution graph

Example conceptual topology: `https://example.com/marketing`, `/support`, `/app` with shared script ecosystem.

Benefits:
- simplest routing/deployment/auth continuity;
- minimal cross-origin API/CORS complexity;
- straightforward first-party navigation.

Risks:
- public/marketing dependencies may gain same-origin execution authority in sensitive contexts if loaded there;
- route separation does not isolate storage;
- broad root Service Worker scope can accidentally couple public and application release lifecycles;
- CSP may become a union of every surface's needs, weakening the sensitive surface.

**Operational judgment:** acceptable only if the sensitive application document can maintain a deliberately minimal script/resource/network graph and public dependencies are not loaded into it. Same origin alone is not automatically wrong; **authority sharing is the decision variable**.

### Pattern B — same origin, separated documents/scopes/policies

Use distinct route documents/builds, narrow Service Worker scope and per-response CSP; do not load marketing/ads/support runtime into the sensitive app document.

Benefits:
- less operational complexity than separate origins;
- meaningful reduction in accidental worker/script/network coupling;
- can preserve same-origin auth/API convenience.

Limitations:
- not a strong isolation boundary against same-origin compromise;
- storage remains origin-scoped;
- a vulnerability or intentionally privileged same-origin component may cross route assumptions.

**Operational judgment:** useful defense-in-depth and often a good baseline, but must never be described as origin isolation.

### Pattern C — sensitive application on a separate origin

Conceptual example only: public `www.example.com`, sensitive PWA `app.example.com`. Different hosts create different origins.

Benefits:
- separate DOM/storage/service-worker principals;
- independent CSP and dependency graphs;
- public analytics/advertising compromise does not automatically become same-origin app execution;
- clearer incident containment and release ownership.

Costs:
- authentication/session continuity must be deliberately designed;
- cross-origin API/CORS and redirect/deep-link flows add complexity;
- cookies are not identical to Web Storage origin semantics and require careful domain/SameSite/credential design;
- separate deployment/DNS/certificate/monitoring incident surfaces;
- user-visible origin transitions can affect trust and support.

**MINTTAP DECISION:** Do **not** mandate a separate origin generically. Require a product threat model and exact script/storage/auth topology first. For an offline PWA holding irreplaceable locally authoritative records, separate-origin evaluation is mandatory if public/third-party runtime would otherwise share sensitive execution authority.

### Pattern D — cross-origin sandboxed third-party embed

Useful for support/media/other embedded functionality that does not need application DOM/storage authority.

Benefits:
- stronger isolation than directly loading vendor JS into the top-level sensitive document;
- sandbox and Permissions Policy can remove capabilities;
- CSP `frame-src` can allow only known embed origins.

Risks:
- `postMessage` becomes an explicit bridge requiring strict origin/schema validation;
- Storage Access API/cookie grants can reintroduce state relationships;
- sandbox tokens can accidentally restore excessive capability;
- accessibility, focus, resizing, error recovery and offline behavior require validation;
- vendor may require top-level execution and be incompatible with safe containment.

**Operational judgment:** if a vendor cannot function without broad top-level DOM/storage/network authority, that is a product risk/cost to evaluate, not a reason to silently widen the sensitive PWA's authority.

## 6. Third-party authority budget

For every third-party dependency proposed inside a sensitive PWA, require an authority record:

- business/task necessity;
- execution mode: no JS / static resource / sandboxed frame / top-level script;
- exact origin(s);
- DOM read/write requirement;
- storage/cookie requirement;
- auth/session visibility;
- network destinations;
- browser-feature permissions;
- offline requirement;
- Service Worker interaction;
- update/provenance model;
- retention/data-processing owner;
- failure behavior when blocked/offline;
- accessible fallback;
- removal/incident kill path.

A dependency that cannot justify an authority should not receive it merely because integration is easy.

Canonical guard:

`third-party business value ≠ requirement for sensitive-context execution authority`.

## 7. Analytics and advertising transfer

Track D owns measurement mechanics; Marketing owns acquisition/channel strategy. Track E owns the security boundary.

### TRANSFER VALIDATION
Public acquisition analytics can often be measured on public surfaces without executing the same analytics graph inside the locally authoritative PWA. Installed-PWA continuity may require first-party event design, but continuity is a measurement requirement, not proof that a third-party tag manager must access unlocked records.

For sensitive PWA telemetry:
- prefer first-party, minimized events where feasible;
- event payloads should describe state/outcome, not authoritative record content;
- `connect-src` should enumerate required destinations rather than become an unrestricted exfiltration channel;
- advertising should not be assumed compatible with sensitive/offline execution authority;
- offline queueing of analytics must not compete with or masquerade as authoritative sync/outbox state.

Canonical guards:

`measurement continuity ≠ shared script authority`.

`analytics queue ≠ authoritative application outbox`.

### Advertising-specific caution
The company has an ad-revenue business constraint, but Web Manager must not infer that an EFB PWA can or should host advertising in the sensitive application context. Advertising feasibility, policy, offline behavior and revenue are separate Marketing/platform questions. Security architecture should expose safe integration boundaries rather than predetermine monetization.

## 8. Authentication continuity without ambient authority

If public and sensitive surfaces are separated by origin, do not recreate a de facto shared-origin trust model through overly broad credentials.

Evaluate separately:
- public anonymous navigation;
- authentication initiation/callback;
- app session establishment;
- API credential scope/audience;
- CSRF/CORS/SameSite behavior;
- logout/revocation propagation;
- offline local unlock;
- recovery/export authority.

093 remains canonical for session/offline authorization. This study adds only the topology constraint:

`SSO convenience ≠ every web origin should receive the same session credential`.

## 9. Service Worker topology

A Service Worker should control only the routes/tasks it is responsible for. A root-scoped worker that exists solely for the offline app but also controls marketing/support pages increases coupling:
- public-page failures can become worker incidents;
- marketing deploy cadence can interact with app worker/cache cadence;
- worker compromise has broader surface;
- cache routing mistakes can affect SEO/support navigation.

Conversely, multiple workers/origins add versioning and diagnostics complexity.

**MINTTAP DIRECTION:** For any product PWA, record worker script URL, allowed scope, controlled route set, cache classes, update owner and public-page relationship. Do not choose root scope by default convenience.

Canonical guard:

`PWA installed from site ≠ Service Worker should control the entire site`.

## 10. UX / accessibility transfer

Origin/security separation must not create misleading or inaccessible continuity.

Track B/C requirements:
- users must know when they leave the offline app for public support/account content if task state could be affected;
- opening support must not silently discard unsaved/pending state;
- sandboxed support content needs keyboard/focus/zoom/screen-reader validation;
- blocked third-party content needs an understandable first-party fallback;
- auth redirects must return users to truthful local/sync state rather than implying remote acknowledgement;
- offline mode must not depend on a third-party widget to explain recovery.

Design Studio latest canonical evidence checked 2026-09-17: Web is Stage 3 PRACTICE / NOT PASSED; W047 runtime is ready but execution OPEN. No Safari, screen-reader, physical-device or human-UX PASS is transferable.

## 11. Quality/security validation matrix

Exact-artifact validation should include at least:

1. **Origin inventory** — enumerate every document, worker, frame, script and API origin.
2. **Script graph** — sensitive app with marketing/tag-manager/ad/support scripts absent by default; fail build/release if unauthorized script appears.
3. **Storage boundary** — verify public/embedded origins cannot read sensitive IndexedDB/Web Storage; verify same-origin route assumptions are not treated as isolation.
4. **Worker scope** — confirm controlled URLs and that public routes are/are not controlled exactly as designed.
5. **CSP negative tests** — unexpected script/frame/connect destinations blocked; worker-response CSP independently checked.
6. **Sandbox tests** — remove one restriction at a time only when justified; verify same-origin + scripts escape hazard is not introduced.
7. **Permissions Policy** — camera/microphone/geolocation/etc denied unless required.
8. **Credential tests** — public/third-party origins do not receive app credentials unless explicitly required; CORS/credential policy tested.
9. **postMessage tests** — strict target/source origin and message-schema validation; reject wildcard/unknown sender where authority crosses boundary.
10. **Storage Access tests** — verify behavior when third-party state is blocked, partitioned, granted or denied across target browsers.
11. **Network exfiltration oracle** — hostile test script cannot beacon/fetch to destinations outside intended policy; do not treat CSP alone as proof against all exfiltration.
12. **Offline test** — sensitive core task remains useful when analytics/support/ads are unavailable.
13. **Incident test** — disable/remove a third-party integration without deleting authoritative local data or breaking recovery/export.
14. **Accessibility test** — iframe/fallback/auth transitions with keyboard, focus, reflow and applicable AT.
15. **Target managed iPad** — Safari/Home Screen/MDM behavior separately; no desktop Chromium result upgrades this gate.

## 12. Cross-track balance result

### Track A — Platform/Browser
Strong foundation. Supplies origin, storage, worker scope, iframe/sandbox, CSP and credential mechanics. Current dependency: exact Safari/managed-iPad behavior where browser policy differs.

### Track B — UX/IA/Content
Consumes topology as a continuity constraint. Must design public/support/auth transitions without false save/sync/recovery implications.

### Track C — Performance/Accessibility/Quality
Owns negative tests, third-party failure isolation, accessibility of embeds/fallbacks and target-engine/device evidence. Third-party removal can also improve runtime cost, but security isolation is not justified solely as performance optimization.

### Track D — Search/Discovery/Analytics
Public crawl/discovery surfaces should remain public and do not require unlocked application authority. Measurement continuity must be designed without assuming shared sensitive execution.

### Track E — Architecture/Security/Operations
Highest-value owner. 096 closes the generic topology/capability-minimization prerequisite created by 095. Product decision remains OPEN pending exact origin/script/storage/auth/worker/deployment evidence.

## 13. External specialist dependencies

### Design Studio
Latest `progress/WEB_STATUS.md` checked 2026-09-17: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W047 retention-boundary runtime ready, execution OPEN. Consume interaction/state evidence only; do not claim Safari/AT/physical-device/human UX validation.

### Software Engineering Studio
Latest global status checked 2026-09-17: all specialists remain Foundation IN STUDY. F004 synchronization evidence and D006/S001 remain adjacent but no exact PWA origin/CSP/worker/third-party implementation evidence exists. Engineering handoff should provide an executable origin/script/storage/worker/CSP inventory and target-device test artifact rather than generic architecture prose.

### Marketing
Advertising/acquisition value is an input, not authority ownership. Marketing should state required outcomes/vendors/data; Web Manager/Engineering determine the least-capability web integration that can satisfy them.

## 14. OPEN — product facts not inferred

Do not infer any of the following without repository/runtime evidence:
- current `minttap.app` hostname/origin topology;
- whether LogMate PWA shares a domain with public pages;
- current Service Worker script or scope;
- current analytics, ads, tag manager, support/chat vendors;
- current CSP/Permissions Policy/CORS/cookie configuration;
- current authentication/session origin model;
- whether sensitive local records are encrypted;
- whether any third party can access app DOM/storage;
- whether a separate application origin is operationally acceptable;
- managed-iPad third-party-cookie/storage-access behavior under company policy.

## 15. Integrated competency / decision procedure

Before approving a public/third-party integration near an offline authoritative PWA:

1. classify the data/task sensitivity;
2. identify the minimum capability the integration needs;
3. choose the least-privileged execution mode;
4. decide whether same-origin placement is actually required;
5. minimize worker scope, CSP destinations and browser-feature permissions;
6. make every cross-origin trust bridge explicit;
7. preserve auth/offline/recovery continuity without sharing unnecessary credentials;
8. test blocked/offline/compromised integration failure modes;
9. validate accessibility and target browser/device behavior;
10. preserve incident removal and independent data recovery.

### Final generic judgment

For an offline PWA that may hold irreplaceable locally authoritative records, **public content, marketing, analytics, advertising and support functionality should not automatically inherit the PWA's execution/storage/worker authority**. Path separation is insufficient; CSP/sandbox/Permissions Policy are valuable capability-reduction tools; separate origins provide a stronger browser principal boundary but introduce real authentication/operations/UX costs. The correct topology must be selected from an exact product threat model and executable evidence.

## 16. Next adjacent target

Generic topology mechanics are now sufficient for handoff. Do not repeat same-origin/CSP/iframe primers. Highest-value next work should consume exact product implementation evidence when available. Without it, the next adjacent generic risk is **cross-context communication and explicit trust bridges**: `postMessage`, CORS/credentialed APIs, auth redirects, deep links/universal links and support/export handoffs — how isolation can be accidentally undone by overly broad message origins, credential scope or navigation authority.
