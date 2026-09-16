# 066 — Stage 7: Web Performance Foundations — Navigation Lifecycle, Critical Rendering Path, Resource Loading, Main-Thread/Rendering Work & Perceived Readiness

Date: 2026-09-16  
State: **PASS — FOUNDATION/PRACTITIONER**

## Why this block now
Stages 1–6 established how a public app-company resource is addressed, delivered, understood, used and discovered. Stage 7 begins by learning what the browser must actually do between navigation and a page becoming visually and interactively useful. Core Web Vitals and optimization recipes are deliberately deferred until these mechanics are understood.

## Authoritative source set
- WHATWG HTML Living Standard — parsing, scripting, styling/render-blocking and event loops: https://html.spec.whatwg.org/
- W3C Web Performance Working Group / specifications: https://www.w3.org/webperf/
- W3C standards status index, Web Performance deliverables: https://www.w3.org/TR/
- MDN, *Populating the page: how browsers work*: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work
- MDN, *Critical rendering path*: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path
- MDN, *Navigation and resource timings*: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Navigation_and_resource_timings

Specification status is CHANGE WATCH. W3C currently lists Navigation Timing Level 2 as a Draft Standard (25 February 2026), Performance Timeline as a Candidate Standard (21 May 2025), while High Resolution Time Level 2 is a W3C Standard. Do not collapse every Web Performance API into one maturity level.

---

## 1. First-principles performance model

`navigation intent → URL/network setup → request → response bytes → HTML parsing → resource discovery/fetch → DOM/CSSOM/script work → render-tree/style/layout → paint/composite → visible content → event-loop/main-thread availability → useful interaction → later stability`

Performance is not one duration and “page loaded” is not one universal event.

### Standing distinction
`server response ≠ HTML received ≠ DOM parsed ≠ first pixels ≠ important content visible ≠ page visually stable ≠ main thread available ≠ task ready ≠ load event`

A professional diagnosis must identify which stage is late and which user-visible consequence follows.

---

## 2. SOURCE — navigation timing and resource timing observe different scopes
W3C Web Performance APIs and MDN distinguish navigation timing for the document navigation from resource timing for resources requested by or during the page. Navigation can include redirect, DNS, connection/TLS, request and response phases; resource entries expose analogous detailed fetch timing for individual resources.

### SYNTHESIS
A slow page cannot be diagnosed from total elapsed time alone. Delay may be caused by connection/setup, server/response timing, critical-resource discovery, transfer, parsing/scripting, rendering or post-render main-thread contention.

### Failure mode
“Hosting is slow” based solely on a late visual result. A fast HTML response can still lead to late useful content because the browser discovers a critical image/font/script late or spends substantial time executing/rendering afterward.

---

## 3. SOURCE — HTML is processed incrementally; resource relationships affect the critical path
Browsers parse HTML into a DOM while discovering external resources. CSS contributes to the CSSOM/styling model; scripts can alter the DOM and can interact with parser/script-blocking stylesheet rules. WHATWG defines explicit parser-blocking/script-blocking and render-blocking mechanisms rather than a simplistic rule that “all CSS blocks everything” or “all JavaScript blocks rendering.”

### SYNTHESIS
Performance depends on **dependency structure and discovery order**, not only aggregate bytes.

A smaller resource discovered late can be more consequential than a larger non-critical resource loaded after useful content. Resource priority, dependency depth and when the browser learns that a resource exists are therefore first-class diagnostic concepts.

### Vocabulary discipline
- **parser blocking:** parsing progress is blocked by a pending script condition;
- **script blocking stylesheet:** styling dependency can delay parser-executed script availability/execution;
- **render blocking:** document rendering is held by defined render-blocking elements/conditions;
- **network blocking:** an informal phrase unless the exact queue/connection/resource mechanism is specified.

Do not use these interchangeably.

---

## 4. SOURCE — critical rendering path converts document inputs into pixels
MDN describes the critical rendering path as the steps that transform HTML, CSS and JavaScript into pixels, including DOM, CSSOM, render-tree/style work, layout and paint. Browser rendering further involves compositing where appropriate.

### SYNTHESIS
A useful conceptual split is:
1. **acquire** — obtain document/resources;
2. **construct** — parse and construct browser representations;
3. **compute** — style/layout and script-dependent state;
4. **draw** — paint/composite;
5. **remain available** — leave enough event-loop/main-thread capacity for interaction and subsequent rendering.

Optimization should target the actual critical dependency, not mechanically minimize every file.

---

## 5. Main thread and event-loop availability
WHATWG defines event loops as the coordination mechanism for events, user interaction, scripts, rendering and networking-related tasks. The specification cautions that event loops do not map one-to-one to implementation threads, so “the event loop is the main thread” is an oversimplification.

MDN's browser-performance model nevertheless emphasizes that substantial scripting/rendering work competes for main-thread availability in ordinary page interaction.

### SYNTHESIS
A page may **look loaded but feel unavailable** when long synchronous work prevents timely handling of input or rendering updates.

This is the bridge from load performance to responsiveness. Stage 7 will later connect it to Event Timing, long tasks/long animation frames and INP; those metrics are not used here as substitutes for the underlying model.

---

## 6. Readiness is task-relative
No single browser lifecycle event proves that the user can complete the primary task.

Examples:
- DOMContentLoaded can occur while an important image or late application state is unavailable;
- `load` can wait for resources that do not matter to the primary task;
- first paint can occur before meaningful product content;
- a visually complete page can remain interaction-constrained by main-thread work;
- a page can become usable before every below-fold resource has loaded.

### MINTTAP DIRECTION
For a future Company/Product/Support/Governance route, define a **Primary Readiness Contract** rather than “must finish loading fast”:
- what primary content must be visible;
- what primary action must be operable;
- which resource/state dependencies gate those outcomes;
- what can load later without blocking the task;
- what visible feedback is required while dependencies remain pending.

This will later connect to objective metrics without equating the metric with the user task.

---

## 7. Resource criticality is contextual
A resource is not globally “critical” because of its file type.

Potentially task/paint-critical resources can include:
- CSS needed for initial layout/readability;
- the actual above-fold product/hero image if it conveys primary content;
- a web font if the chosen strategy makes readable text depend on it;
- JavaScript required for a primary interactive control;
- data required to render the primary state.

Potentially deferrable resources can include below-fold media, secondary analytics/marketing features, non-immediate widgets or route-specific code not needed for the current task.

### Failure mode
Apply `lazy`, `async`, `defer`, preload or prefetch as universal “speed flags.” Each changes discovery/execution/priority semantics and must be justified by the dependency graph. Premature or excessive hints can compete with genuinely critical resources.

---

## 8. Performance causality map

| Symptom | Candidate causal layer | Evidence needed later |
| --- | --- | --- |
| document starts late | redirect/DNS/connection/TLS/request/server | Navigation Timing + network trace |
| HTML arrives but blank/unstyled state persists | CSS/script/render-blocking/dependency discovery | waterfall + parser/render evidence |
| primary image appears late | discovery/priority/transfer/decode/render | resource timing + LCP candidate trace |
| text shifts after font/media arrives | intrinsic sizing/font/layout dependency | layout-shift + font/media trace |
| page looks ready but clicks lag | long JS/rendering task/main-thread contention | performance trace + Event Timing/INP later |
| later scroll/animation janks | repeated style/layout/paint/script work | frame/main-thread trace |

This table is diagnostic scaffolding, not proof. Every row remains hypothesis until measured.

---

## 9. Measurement architecture — observe layers before optimizing
The Performance Timeline family exists so browser events can be represented as timestamped performance entries. Navigation Timing and Resource Timing provide structured evidence for document/resource phases; later Stage 7 blocks will add paint/LCP/event/layout-shift/field-vs-lab evidence.

### SYNTHESIS
Use a layered evidence chain:
`user symptom → browser phase hypothesis → appropriate timing/trace → causal dependency → bounded intervention → re-measurement`.

Do not use:
`Lighthouse score → random optimization checklist`.

---

## 10. Design/content/engineering are performance inputs
Performance is cross-disciplinary:
- large product screenshots/video change transfer/decode/render cost;
- typography decisions affect font requests, fallback and layout stability;
- responsive composition affects which media/assets are needed;
- animation/interaction patterns affect main-thread/render work;
- third-party marketing/analytics can add network and script work;
- content quantity and structure can affect DOM/media size;
- engineering architecture controls bundling, rendering, caching and resource discovery.

### MINTTAP DIRECTION
Web Manager owns the **performance requirement/evidence contract**, not every implementation detail. Design Studio and engineering receive causal constraints rather than generic instructions such as “make images smaller” or “use fewer fonts.”

---

## 11. Design Studio dependency / handoff
Latest `design-studio/progress/WEB_STATUS.md` checked 2026-09-16: Web Stage 1 PASS / Stage 2 PRACTICE NOT PASSED. W017 completed icon/non-text Chromium transfer 12/12 after preserved failure/revision evidence. Real Fetch/DOM/network transfer and true HTTP navigation remain OPEN because the current environment blocked network navigation. W007 request/paint/readiness/stability measurement is explicitly listed as a remaining Web gap.

### Web Design handoff
066 gives W007 a clearer evidence boundary. Future performance practice should distinguish:
- request/navigation phases;
- resource discovery/transfer;
- parser/render blocking;
- style/layout/paint/composite;
- main-thread availability;
- task-relative readiness;
- later stability.

A deterministic visual specimen or successful Chromium assertion does not establish field performance.

### Type handoff
When production typography is selected, validate actual font file count/weight/subsetting/fallback/load behavior and resulting layout/readiness; do not infer performance from typeface aesthetics.

### Layout/Interaction handoff
Preserve primary task/action availability while media, secondary data or noncritical modules are pending. Skeleton/loading treatment must not create false readiness or avoidable layout instability.

### Content Design / UX handoff
These remain user-managed. If a performance intervention changes information priority, loading labels, perceived readiness or task continuity, record evidence for handoff rather than treating performance as purely engineering.

No Design Studio canonical file is edited here.

---

## 12. OPEN MintTap facts
- actual `minttap.app` frontend/rendering/deployment architecture;
- production HTTP/navigation timing;
- route/resource waterfall and cache behavior;
- JS/CSS bundle and dependency graph;
- production image/video/font inventory;
- third-party scripts;
- service-worker behavior, if any;
- primary task/readiness definition by page family;
- field performance data and supported device/network population;
- actual Core Web Vitals;
- performance budget or release gates.

No production performance claim is permitted until these are observed.

---

## 13. Competency check
PASS at FOUNDATION/PRACTITIONER if Web Manager can:
1. separate navigation/network, parsing/resource discovery, rendering and responsiveness phases;
2. explain why total bytes alone do not determine readiness;
3. distinguish parser-, script- and render-blocking concepts;
4. explain DOM/CSSOM/style/layout/paint/composite at the level needed for diagnosis;
5. explain why lifecycle events and visual appearance do not prove task readiness;
6. form a causal hypothesis and select evidence rather than applying generic optimization recipes;
7. identify Design/Content/Engineering dependencies without assigning performance to one discipline.

**Result: PASS.**

## Next highest-value block
067 — **Core Web Vitals from First Principles: LCP, INP, CLS, Metric Windows, Field vs Lab Evidence & Diagnostic Boundaries.**

Now that browser work and readiness phases are established, study what the current user-centric metrics actually observe, what they omit, how field/lab evidence differs, and how to diagnose causes without score chasing.