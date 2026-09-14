# 032 — Application / Rendering / State / Navigation Foundations

Status: **STAGE 1 CORE — FOUNDATION/PRACTITIONER CHECKPOINT COMPLETE**
Research date: 2026-09-15
Curriculum: Stage 1 — Web Foundations

## Purpose

This study closes the remaining broad prerequisite between browser document/runtime foundations and the Stage 1 end-to-end integration review.

The goal is not to learn one framework. It is to build a framework-neutral mental model for:

- static vs dynamic delivery;
- build-time, request-time and client-time rendering;
- SSR, CSR, static generation and hybrid rendering;
- hydration and progressive enhancement;
- browser/server/application state boundaries;
- cookies, Web Storage and server-side sessions;
- cross-document vs same-document navigation;
- session history and back/forward restoration;
- forms and native submission;
- CDN/edge/hosting relationships;
- failure diagnosis and project trade-offs.

The Web Manager should be able to determine **where content is produced, where state lives, what survives navigation, and which layer owns a failure** without assuming a framework implementation.

---

## 1. The key mental model: three different times at which a page can be produced

### SOURCE
MDN defines server-side rendering (SSR) as generating HTML on the server and sending it to the client, while client-side rendering (CSR) generates HTML content in the browser using JavaScript. MDN also notes these approaches are not mutually exclusive.

MDN describes static-site generation as producing static files ahead of requests. web.dev distinguishes server-side rendering, client-side rendering, prerendering/static rendering and hydration.

### SYNTHESIS
A clearer framework-neutral model is to ask **when and where the representation is produced**:

1. **Build time** — HTML/files are generated before a user request.
2. **Request time** — server/edge logic generates a response for the current request.
3. **Client time** — browser JavaScript creates or changes DOM after delivery.

A single modern site can use all three.

This is more durable than memorizing framework labels because frameworks frequently combine rendering modes.

---

## 2. Static vs dynamic is not the same distinction as interactive vs non-interactive

### SOURCE
MDN's SSG description characterizes static sites as pre-generated files without request-time server-side logic for page generation. Static assets can be delivered from a CDN.

### FOUNDATION
A page can be **statically generated but highly interactive** after JavaScript loads.

Conversely, a server can dynamically generate a mostly non-interactive HTML document.

Therefore:

- `static` primarily describes when/how the delivered representation is produced;
- `interactive` describes runtime behavior available to the user;
- these dimensions are independent.

### Common misconception
"Static site" does not mean "plain HTML with no JavaScript."

---

## 3. SSR, CSR and SSG are strategies, not mutually exclusive site identities

### SOURCE
MDN explicitly notes SSR and CSR can be combined in one application. web.dev documents mixed rendering and hydration approaches.

### FOUNDATION

**SSR**
- server generates HTML for a request;
- browser receives meaningful document content before client rendering is necessarily complete.

**CSR**
- browser JavaScript produces or substantially constructs displayed DOM/content;
- the initially delivered HTML can be minimal.

**SSG / static generation**
- output is generated before request time;
- deployment can often distribute immutable/static files through CDN infrastructure.

### SYNTHESIS
Real systems are frequently hybrid:

- marketing pages may be static;
- support search may call APIs dynamically;
- account pages may use request-time rendering;
- components may hydrate and continue client-side interaction;
- some later navigations may be same-document/client-routed.

The Web Manager should identify rendering **per route and per component where necessary**, rather than assigning one simplistic label to the whole domain.

---

## 4. Hydration: visible HTML and interactive application state are not the same milestone

### SOURCE
web.dev defines hydration as running client-side scripts that attach application state/interactivity to server-rendered HTML.

### FOUNDATION
A server-rendered page can be visible before its JavaScript-driven components are ready to respond.

This creates an important distinction:

`content visible` ≠ `application interactive`

### Failure mode
A user sees a button but taps before the relevant JavaScript has loaded/executed. The control appears ready, but the intended client behavior has not been activated yet.

### SYNTHESIS
This is one reason native HTML behavior and progressive enhancement remain valuable for public website functions. Native links/forms can preserve useful baseline behavior even if enhancement code is delayed or fails.

This does not mean every site must avoid hydration. It means hydration cost and failure behavior are architecture/UX considerations rather than invisible implementation details.

---

## 5. Progressive enhancement and hydration solve different problems

### FOUNDATION
Hydration typically starts with server-rendered markup and activates application logic on the client.

Progressive enhancement starts from a functional baseline and layers optional richer capabilities on top.

They can coexist.

### SYNTHESIS
For MintTap public/company surfaces, resilience should be evaluated by asking:

- Can core navigation work without client routing?
- Can essential forms submit through native browser mechanisms where appropriate?
- Is core informational content present in delivered HTML?
- What happens when enhancement JavaScript is slow or fails?

This is a provisional architecture quality criterion, not a decision that MintTap must use a specific framework or rendering mode.

---

## 6. State has multiple locations and lifetimes

A phrase such as "the website stores state" is too vague.

A useful Stage 1 taxonomy is:

1. **DOM/runtime state** — current objects/variables in an active document/runtime;
2. **session history state** — navigation-related state associated with history entries;
3. **Web Storage** — client-side key/value storage exposed by browser APIs;
4. **cookies** — HTTP state tokens stored by the user agent and conditionally attached to requests;
5. **server-side application/session state** — application data retained on infrastructure and associated with a user/session identifier;
6. **persistent backend data** — durable application/database records.

Each has different scope, lifetime, security, privacy and synchronization characteristics.

---

## 7. Cookies: HTTP is mostly stateless, but cookies allow state continuity

### SOURCE — RFC 10025
RFC 10025, published July 2026, is the current IETF Standards Track specification for cookies and **obsoletes RFC 6265**.

It defines `Set-Cookie` and `Cookie` fields. A server can send state to a user agent, which may return eligible cookies on later requests. The RFC explicitly frames cookies as a way to maintain stateful sessions over the mostly stateless HTTP protocol.

### FOUNDATION
A cookie is not automatically "the session."

It can contain:
- a session identifier;
- a preference;
- another application-defined token/value.

The actual account/session data may remain on the server.

### Important scope distinction
Cookie delivery is governed by rules including host/domain, path, expiry, Secure, HttpOnly and SameSite behavior.

### Security/privacy boundary
RFC 10025 explicitly records historical security/privacy weaknesses and ambient-authority concerns. Those topics belong to later Stage 8 depth, but the Stage 1 lesson is:

> cookies are transport-attached state with security/privacy semantics, not a generic browser database.

### CHANGE WATCH corrected
Prior repository notes that treated RFC 6265bis as pending are now outdated. **RFC 10025 is published and normative as of July 2026.**

---

## 8. Web Storage: localStorage and sessionStorage are not cookie substitutes

### SOURCE — WHATWG HTML
The HTML Standard defines Web Storage mechanisms including `sessionStorage` and `localStorage`.

The standard explains that session storage is associated with a browsing context/tab-like session, while local storage supports data that persists beyond a single session and across windows under its storage-key/origin rules.

### FOUNDATION
Unlike cookies, Web Storage values are generally accessed through browser script APIs and are not automatically attached to every HTTP request.

Therefore cookies and Web Storage have different network, security and privacy consequences.

### Common misconception
"localStorage is a newer cookie" is false.

They differ in transport behavior, API exposure, scope and threat model.

---

## 9. Server-side sessions: identifier and state can be separated

### SYNTHESIS
A common application pattern is:

`browser holds session identifier → request carries identifier → server looks up session state`

In this pattern the cookie is not the entire session database. It is an association mechanism.

This explains why clearing one cookie can appear to "log out" a user while server-side records still exist.

### OPEN
MintTap's future website/account architecture is unknown. Do not assume that MintTap uses or needs server-side sessions until real account/auth requirements exist.

---

## 10. Navigation is a browser/document lifecycle operation, not merely changing the address bar

### SOURCE — WHATWG HTML
The HTML Standard's navigation/session-history model describes a navigable presenting an active `Document`, navigation to another URL, fetching/creating a new document for cross-document navigation, session-history entries and traversal through them.

It also permits multiple contiguous session-history entries to share one document state, including same-document navigations such as History API state changes or fragment navigation.

### FOUNDATION
Two broad categories matter:

**Cross-document navigation**
- typically produces/activates a different `Document`;
- may involve network retrieval, parsing and new runtime lifecycle.

**Same-document navigation**
- can update URL/history without creating an entirely new document;
- examples include fragment/history-state operations and many SPA routing patterns.

### Operational consequence
A URL change does not prove a new HTML document was fetched.

Likewise, no visible full-page reload does not mean browser history/navigation semantics disappeared.

---

## 11. SPA is a document-lifecycle pattern, not synonymous with CSR

### SOURCE
MDN describes a single-page application (SPA) as loading one web document and updating that document through JavaScript APIs for later views.

MDN also notes SPAs do not inherently require pure CSR; modern frameworks can combine SPA navigation with SSR.

### FOUNDATION
Separate these concepts:

- **SPA vs multi-page** concerns document/navigation lifecycle;
- **SSR vs CSR vs SSG** concerns where/when content is rendered.

They are independent axes.

### Common misconception
"SSR means multi-page and CSR means SPA" is false.

---

## 12. Browser history is user-facing application architecture

### SOURCE — WHATWG HTML
The HTML Standard defines session history entries, traversal, push/replace behavior and same-document navigation semantics.

### FOUNDATION
The Back/Forward buttons are part of the browser's navigation contract with the user.

Client-side routing that visually changes pages without creating coherent history entries can break expected user behavior.

### SYNTHESIS
For a Web Manager, correct application navigation means more than displaying the correct component. URL, document state, focus/announcement behavior, scroll restoration and Back/Forward expectations can all matter.

Detailed focus/accessibility behavior belongs to later stages, but architecture must not treat browser history as optional decoration.

---

## 13. bfcache is different from HTTP cache

### SOURCE
MDN documents the browser back/forward cache (bfcache) as retaining a snapshot of a page, including JavaScript heap/runtime state, for rapid history traversal.

This differs from HTTP cache, which stores reusable HTTP responses.

### FOUNDATION
Keep three distinct caching concepts separate:

- **DNS cache** — naming answers;
- **HTTP cache** — HTTP responses/representations;
- **bfcache** — a browser page/document/runtime snapshot for history traversal.

### Diagnostic consequence
Returning with Back and seeing old runtime/UI state does not necessarily mean the browser performed a fresh HTTP request or reused an ordinary HTTP cache response.

This distinction will matter in Stage 7 performance/runtime diagnosis.

---

## 14. Forms are a built-in Web application mechanism, not merely framework components

### SOURCE — WHATWG HTML
The HTML Standard defines forms, controls, validation and submission. Its introductory guidance explicitly notes that many forms can send data to a server without client-side scripting, while JavaScript can augment the experience.

### FOUNDATION
A native form establishes:

- named controls;
- user input collection;
- constraint validation behavior;
- submission method/action semantics;
- encoding rules;
- browser navigation/submission behavior.

JavaScript can intercept or enhance this flow, but it does not create the concept of form submission.

### SYNTHESIS
For public MintTap support/contact/search/account surfaces, the architecture should deliberately decide whether JavaScript enhancement is necessary rather than assuming all forms must be client-only components.

This improves resilience and makes failure modes easier to reason about.

---

## 15. Rendering architecture changes failure shape

### Framework-neutral diagnosis

**Build-time/static failure**
- stale generated content;
- wrong artifact deployed;
- route/file absent;
- build did not include expected data.

**Request-time/server rendering failure**
- request reaches render service but data/template execution fails;
- 5xx/timeouts;
- personalization or locale generation wrong.

**Client-rendering failure**
- HTML arrives but JS bundle fails to load/execute;
- runtime exception prevents content/component creation;
- API fetch fails after shell is visible.

**Hydration mismatch/failure**
- server HTML appears but client assumptions differ;
- events/components fail to activate or client replaces unexpected markup.

**Navigation/history failure**
- view changes but URL/history is wrong;
- deep URL works client-side but direct server request 404s because hosting fallback/routing is misconfigured.

**State failure**
- cookie not sent because scope/policy excludes it;
- storage missing/cleared;
- stale client state disagrees with server state;
- server session expires while UI still looks authenticated.

The correct first question is not "Which framework is broken?" but "At what production/state/navigation boundary did expected behavior stop?"

---

## 16. CDN/edge/hosting relationship

### SYNTHESIS from HTTP/TLS/rendering studies
A public path may look like:

`browser → DNS → TLS edge → CDN/cache/edge logic → static artifact or render service/origin → response → browser runtime`

A CDN is not synonymous with static hosting. Modern edge/CDN platforms can cache static resources, proxy requests, execute logic and route to dynamic origins.

Likewise, a site using SSR does not imply every request reaches one traditional application server.

### Web Manager rule
Architecture diagrams should separately identify:

- authoritative DNS;
- public TLS termination;
- CDN/cache/edge layer;
- static artifact storage;
- request-time rendering/application service;
- APIs/data stores;
- browser client runtime.

Combining several roles in one vendor does not eliminate the conceptual boundaries.

---

## 17. Rendering choice is a multidimensional trade-off

No rendering mode is universally superior.

A professional evaluation should consider:

- content change frequency;
- personalization;
- number/predictability of URLs;
- interaction complexity;
- time until meaningful content is available;
- JavaScript required before interaction;
- crawl/social-preview requirements;
- accessibility/resilience;
- cacheability/CDN reuse;
- backend cost/latency;
- deployment complexity;
- operational failure modes;
- localization/content workflow.

### MintTap provisional synthesis
For an app-company website whose primary public surfaces are likely product information, downloads/store links, support, privacy/legal, help and release information, static or server-rendered HTML should normally be considered before defaulting to a client-only shell.

This is **not yet a MintTap architecture decision** because actual product requirements, account features and content workflows remain unknown.

---

## 18. Search/accessibility/performance implications without premature optimization

### SYNTHESIS
Rendering architecture influences later specialist domains:

**Search/discovery**
- URL stability and content availability matter;
- client routing/deep links must map coherently to retrievable destinations.

**Accessibility**
- initial semantics, focus handling and announcements can be affected by client-side navigation/hydration;
- native functionality can offer stronger baseline behavior.

**Performance**
- static/SSR can improve early content availability but does not guarantee low JavaScript cost;
- CSR can avoid some server rendering cost but can add client/network dependency waterfalls;
- hydration can improve initial content while still imposing client execution cost.

**Operations**
- static output has different invalidation/deploy failure modes from per-request rendering;
- hybrid systems require observability across both server and browser.

These are directional relationships. Detailed optimization belongs to later curriculum stages.

---

## 19. Representative diagnosis exercises

### Case A — content visible, button dead for two seconds
Likely investigation:
1. confirm server/static HTML contains the visible control;
2. inspect JavaScript loading/execution;
3. determine whether hydration/event activation is pending or failed;
4. assess whether native baseline behavior should exist.

Do not call this a "server-rendering failure" merely because SSR was used.

### Case B — navigation works inside site, direct URL refresh gives 404
Likely investigation:
1. determine whether routing is same-document/client-side;
2. request the deep URL directly from hosting/edge;
3. verify server/static route generation or rewrite/fallback behavior;
4. verify correct HTTP status instead of masking all unknown routes with 200 shell responses.

### Case C — user presses Back and sees old form values instantly
Possible explanation includes bfcache restoration rather than HTTP cache reuse or refetch.

### Case D — user appears logged out after navigation
Investigate separately:
- cookie eligibility/scope;
- session expiration/server lookup;
- client-state representation;
- network response/auth status.

Do not assume one UI state proves the authentication/session layer state.

---

## 20. Competency checkpoint

This Stage 1 block is retained when the Web Manager can explain:

1. build-time vs request-time vs client-time content production;
2. why static/dynamic and interactive/non-interactive are separate axes;
3. SSR, CSR and SSG without tying them to a specific framework;
4. hydration and the gap between visible and interactive content;
5. SPA vs rendering-strategy distinctions;
6. cookie vs Web Storage vs server-session state;
7. why RFC 10025 supersedes RFC 6265;
8. cross-document vs same-document navigation;
9. browser session history as part of UX/application correctness;
10. bfcache vs HTTP cache vs DNS cache;
11. native form submission as a browser capability;
12. how hosting/CDN/edge/render-service/client layers combine;
13. how rendering/state/navigation choices alter failure modes;
14. why MintTap architecture must be selected from real product requirements rather than fashion/framework defaults.

Checkpoint result: **PASS at Stage 1 foundation/practitioner level.**

---

## 21. MintTap direction vs unknowns

### MINTTAP DIRECTION
For future public `minttap.app` work:
- model rendering per route rather than label the entire domain casually;
- preserve durable URL/deep-link behavior regardless of client navigation;
- prefer meaningful delivered HTML for core public information unless requirements justify otherwise;
- treat hydration/client JS as an enhancement/runtime dependency with observable failure modes;
- distinguish browser storage, cookies and server state explicitly in architecture diagrams;
- preserve native browser navigation/form behavior where it improves resilience and accessibility;
- diagram CDN/edge/origin/client responsibilities separately even when one provider implements several.

### OPEN
Real project decisions still require:
- product/app inventory and page types;
- whether website login/account functionality exists;
- personalization requirements;
- localization/content update workflow;
- support-search/data requirements;
- framework/build system;
- hosting/CDN platform;
- offline/PWA need;
- analytics/third-party runtime dependencies;
- SEO/social-preview requirements per route.

No rendering framework or hosting provider is selected by this research.

---

## 22. Design Studio dependency / handoff

### DEPENDENCY
Design Studio Web Design remains the reusable owner for how page/navigation/state patterns should look and behave across responsive layouts and interaction modes.

### Outgoing handoff from this study
When Design Studio Web begins substantive research/project work, it should explicitly account for:

1. visible content vs hydrated/interactable state;
2. same-document navigation vs cross-document navigation and Back/Forward expectations;
3. route/deep-link behavior as a design constraint, not only engineering configuration;
4. loading/partial/error states that differ by server vs client data/render boundaries;
5. bfcache restoration as a possible return-navigation state;
6. native form/navigation capability as a baseline before custom interception;
7. storage/session expiry or disagreement as a source of UI state transitions;
8. progressive enhancement and resilience when designing app-company public surfaces.

No Design Studio canonical file is edited from Web Manager.

---

## Sources

Primary/current standards:
- WHATWG HTML Living Standard — navigation/session history, forms, Web Storage: https://html.spec.whatwg.org/
- IETF RFC 10025 — Cookies: HTTP State Management Mechanism, July 2026, obsoletes RFC 6265: https://www.rfc-editor.org/rfc/rfc10025.html

High-quality implementation/concept references:
- MDN — Server-side rendering (SSR): https://developer.mozilla.org/en-US/docs/Glossary/SSR
- MDN — Client-side rendering (CSR): https://developer.mozilla.org/en-US/docs/Glossary/CSR
- MDN — Static site generator (SSG): https://developer.mozilla.org/en-US/docs/Glossary/SSG
- MDN — Single-page application (SPA): https://developer.mozilla.org/en-US/docs/Glossary/SPA
- MDN — bfcache: https://developer.mozilla.org/en-US/docs/Glossary/bfcache
- web.dev — Rendering on the Web: https://web.dev/articles/rendering-on-the-web

## Evidence classification

- `SOURCE`: WHATWG navigation/history/forms/Web Storage behavior; RFC 10025 cookie semantics; rendering terminology supported by MDN/web.dev.
- `SYNTHESIS`: build/request/client-time model; rendering/state failure taxonomy; CDN-edge-render-client decomposition; route-level architecture reasoning.
- `MINTTAP DIRECTION`: meaningful public HTML, durable routes, explicit state boundaries, native/progressive baseline where appropriate.
- `OPEN`: actual rendering framework, account/session requirements, hosting topology, page inventory, localization/data/runtime needs.
- `DEPENDENCY`: Design Studio Web must later integrate navigation/state/loading/resilience constraints into actual design behavior.
- `VALIDATION`: real MintTap project should test direct deep links, JS-disabled/degraded behavior where relevant, Back/Forward, state expiry, form behavior, hydration/runtime failures and edge/origin routing.
- `CHANGE WATCH`: browser implementation details and storage/privacy restrictions; cookie standard authority updated to RFC 10025 in July 2026.