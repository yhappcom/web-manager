# 068 — Stage 7: Performance Causality — Delivery, Resource Priority, Caching, Media, Fonts, JavaScript & Third-Party Cost

Date: 2026-09-16  
State: **PASS — FOUNDATION/PRACTITIONER**

## Purpose
066 established browser-work phases; 067 established LCP/INP/CLS as bounded observations. This block asks the next causal question: **what delivery/resource decisions create or remove work on the path to primary readiness?**

The goal is not a bag of optimization tricks. It is a causal model that lets Web Manager identify which bytes, dependencies, origins and execution/render costs actually gate a MintTap page task.

## Primary source set
- MDN, Web Performance best practices: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Best_practices
- MDN, HTML performance optimization: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/HTML
- MDN, How browsers work: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work
- MDN, Speculative loading: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Speculative_loading
- MDN, HTTP Priority: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Priority
- MDN, Multimedia/image performance: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Multimedia
- web.dev, Image performance: https://web.dev/learn/performance/image-performance
- web.dev, Optimize web fonts: https://web.dev/learn/performance/optimize-web-fonts
- web.dev, Font best practices: https://web.dev/articles/font-best-practices

Platform/browser implementation details are CHANGE WATCH; source set rechecked 2026-09-16.

---

## 1. First-principles causal model

`origin/server availability → connection/response → HTML discovery → dependency chain → browser priority/scheduling → transfer/decompression → parse/decode/compile → style/layout/paint → main-thread work → primary content/action readiness → later secondary work`

### Standing distinction
`resource bytes ≠ transfer time ≠ discovery time ≠ dependency delay ≠ execution/decode cost ≠ render cost ≠ user-task impact`

A large file may be harmless if deferred outside the task path. A smaller file can be damaging if it is discovered late, blocks a critical dependency, occupies the main thread at interaction time or causes layout instability.

**SYNTHESIS:** optimize the **critical dependency path**, not an undifferentiated page-weight total.

---

## 2. Network/server latency is one component, not the whole explanation

A document cannot expose its dependency graph until the browser receives enough response content to parse/discover it. Cross-origin dependencies may add DNS/connection/TLS work. Later resources may reuse existing connections/caches, so the cost is context-dependent.

`preconnect` can move connection setup earlier for a likely critical cross-origin origin. MDN warns that preconnecting many origins can be counterproductive. Same-origin preconnect normally adds no benefit once the connection exists.

**SYNTHESIS:** a third-party origin has at least two possible costs: connection establishment and the resource/script work it later introduces. Eliminating 5 KB from a first-party CSS file is not automatically more valuable than removing an unnecessary origin handshake plus its execution chain.

**OPEN MINTTAP:** hosting/CDN, TTFB distribution, HTTP protocol, geographic audience and third-party origin graph are unknown.

---

## 3. Discovery and priority: earlier is not universally better

Browsers parse HTML and use preload scanning to discover resources early. Explicit mechanisms such as `preload`, `modulepreload`, `preconnect`, `prefetch` and `fetchpriority` can influence discovery or priority, but they are hints/controls for specific problems, not blanket acceleration switches.

MDN documents that unused preload consumes bandwidth/work and that excessive preconnect can be counterproductive. HTTP Priority/fetch priority expresses relative preference; server/browser scheduling remains implementation-dependent.

### Diagnostic question set
For a suspected critical resource ask:
1. Was it actually required for primary readiness?
2. When did the browser discover it?
3. What initiated it?
4. Was it delayed behind another dependency?
5. What priority did browser/server assign?
6. Did moving it earlier displace something more important?
7. After arrival, was decode/parse/compile/render still the bottleneck?

**SYNTHESIS:** `preload everything` destroys the meaning of priority. Priority is a scarce ordering signal.

---

## 4. Caching and compression solve different costs

Compression reduces transferred representation size; caching can avoid or conditionally validate transfers on later visits. Neither automatically removes parse/decode/execution/render work after a resource is available.

Static immutable versioned assets and frequently changing HTML/API data have different cache semantics and lifecycle risks. A stale resource served quickly can be operationally worse than a fresh resource served slightly slower.

**SYNTHESIS:** cache policy is a correctness + lifecycle decision before it is a speed trick. Performance evidence must distinguish cold, warm/repeat and restored navigation contexts.

**OPEN MINTTAP:** Cache-Control/ETag/versioning/CDN/service-worker policy is unknown.

---

## 5. Images and product media: likely high-value app-company cost family

MDN identifies images/video as major page-weight contributors and recommends delivering appropriately sized media and loading it when needed. Responsive images can avoid sending desktop-sized assets to smaller displays. Explicit dimensions/aspect reservation reduce reflow/layout-shift risk. Priority should favor the primary visible image over secondary carousel/media assets.

Modern formats such as WebP/AVIF can reduce transfer cost depending on content and encoding settings, but no universal compression setting preserves the right quality for every asset. Screenshots containing UI text/sharp edges require visual QA after lossy compression.

### MintTap operating rule
For each screenshot/video classify:
- primary proof / potentially LCP-relevant;
- secondary explanatory media;
- below-fold optional media;
- decorative media.

Do not lazy-load the primary above-fold image merely because `lazy` is generally useful. Do not eagerly fetch an entire screenshot gallery merely because images are product evidence.

**DESIGN STUDIO HANDOFF:** Web/Color/Layout should preserve visual evidence quality and geometry while Web Manager/engineering validate actual responsive source selection, transfer size, discovery priority and layout reservation.

---

## 6. Fonts are a network + text-rendering + geometry system

Web fonts can affect initial text visibility/LCP and later layout stability. Font discovery commonly depends on CSS and whether text using the face exists. Font files also differ by family, weight, style, script coverage and format.

`font-display` changes the rendering/fallback policy; it is not a universal `swap = solved` switch. A fallback with materially different metrics can cause reflow when the web font replaces it. Excess weights/styles/script coverage can create unnecessary transfers.

### SYNTHESIS
Font optimization has four separable questions:
1. **necessity** — which family/weights/scripts are actually required?
2. **discovery/delivery** — when/how is the file found and transferred?
3. **fallback/render policy** — what appears before/without it?
4. **metric compatibility** — what geometry changes when it swaps?

**TYPE HANDOFF:** Type owns typographic suitability and exact production family/weight/script requirements. Web Manager/engineering own measured delivery/discovery/cache/runtime cost. Neither side should optimize independently of the other.

**OPEN MINTTAP:** shipped fonts and Korean/Latin subset strategy are unknown.

---

## 7. CSS: critical style dependency, not merely file size

Stylesheets participate in rendering dependencies and can gate useful paint. CSS can also discover secondary assets such as fonts/background images later than equivalent HTML discovery. Splitting/inlining/deferring CSS can help or harm depending on cache reuse, duplication and actual criticality.

**SYNTHESIS:** “minify CSS” is hygiene, not diagnosis. More important questions are whether primary content needs the stylesheet, whether the stylesheet delays rendering, whether it introduces late dependencies and whether unused page-wide CSS is shipped to every route.

---

## 8. JavaScript has transfer AND CPU/runtime cost

JavaScript cost is not captured by compressed KB alone. A script can require transfer, decompression, parse/compile, execution, framework initialization/hydration, event work and later interaction work. Code splitting can reduce initial work when boundaries align with actual task needs; poor splitting can create long dependency chains or late task blockers.

MDN recommends loading only JavaScript needed by the current page and using appropriate async/defer/module patterns rather than allowing unnecessary parser/render interference.

### Diagnostic split
`download problem? → discovery/priority/bytes/cache`
`startup problem? → parse/compile/execute/init`
`interaction problem? → event handler/synchronous work/render aftermath`
`late feature problem? → chunk discovery/dependency/network`

**SYNTHESIS:** a cached JavaScript bundle can still be expensive because CPU work remains. Conversely, a moderately sized deferred bundle may not affect primary readiness.

**OPEN MINTTAP:** framework, hydration model, route chunks and bundle/runtime costs are unknown.

---

## 9. Third-party code multiplies uncertainty and cost

Analytics, embeds, support widgets, social media, consent systems and marketing tags can add origins, DNS/TLS connections, bytes, execution, DOM mutation, layout changes and privacy/security dependencies. Their availability and behavior are not fully controlled by MintTap.

### Third-Party Cost Record
For every third party record:
- user/business purpose;
- owner;
- routes where required;
- load trigger;
- origins/requests;
- transfer + main-thread/render evidence;
- privacy/consent dependency;
- failure behavior;
- whether primary task depends on it;
- removal/defer/self-host alternative where legally/licensing-wise valid;
- revalidation date.

**SYNTHESIS:** “async” does not mean “free”. It may remove parser blocking while retaining network, CPU, interaction and privacy costs.

---

## 10. Resource Criticality Matrix

Use this before proposing an optimization:

| Resource | Primary task required? | Discovery point | Network criticality | CPU/render criticality | Layout risk | Cache reuse | Deferrable? | Evidence |
|---|---|---|---|---|---|---|---|---|
| document | usually yes | navigation | high | parse | structure | context | no | runtime |
| critical CSS | often | HTML | high | style/layout | yes | high | bounded | trace |
| hero/product image | page-dependent | HTML/CSS | possibly high | decode/paint | yes | medium/high | page-dependent | LCP/trace |
| web font | page-dependent | CSS | medium/high | text/layout | yes | high | policy-dependent | trace/CLS |
| primary JS | architecture-dependent | HTML/module graph | variable | potentially high | indirect | high | bounded | trace/INP |
| secondary media | usually no | page/interaction | low initially | decode/render | yes if unreserved | variable | often yes | waterfall |
| third party | purpose-dependent | tag/script | variable | variable/high | possible | external | often | trace/inventory |

This matrix is a hypothesis scaffold; production measurements decide actual criticality.

---

## 11. Optimization order — causal, not fashionable

Recommended diagnostic sequence:

`identify primary readiness/task → observe candidate/interaction/shift → inspect request/dependency chain → classify network vs CPU/render vs geometry cause → identify owner/resource family → make smallest defensible intervention → check correctness/accessibility/design → lab regression → field re-observation`

Examples:
- Late LCP image because CSS discovers it late → fix discovery/source architecture before blindly compressing every image.
- Good transfer but slow INP → inspect main-thread/event/render work rather than CDN tuning.
- CLS after font swap → investigate fallback metrics/font policy rather than image compression.
- Slow cold load but fast repeat load → inspect server/connection/cache path and preserve context in reporting.

---

## 12. Failure modes rejected

- optimize total KB without identifying the primary task path;
- preload every asset;
- preconnect every third-party origin;
- lazy-load all images including primary visible proof;
- assume AVIF/WebP automatically gives acceptable screenshot quality;
- assume `font-display: swap` eliminates font performance problems;
- call cached JavaScript free;
- call async third-party JavaScript free;
- optimize Lighthouse advice without validating candidate/dependency causality;
- remove product evidence/accessibility semantics merely to improve a metric;
- declare production improvement from one lab run.

---

## 13. Design Studio dependencies / handoffs

Latest known Web Design state remains Stage 1 PASS / Stage 2 PRACTICE NOT PASSED with W007 request/paint/readiness/stability measurement OPEN and real HTTP/network breadth blocked in the current environment.

### Web Design
Future W007/live-project evidence should include waterfall initiator chains, resource priority/discovery, media dimensions/source selection, font discovery/swap, JS/third-party main-thread work and readiness/stability—not just paint timestamps.

### Type
Provide actual chosen families, files, weights, styles, scripts and acceptable fallback behavior. Web Manager returns measured load/layout effects rather than dictating typography from generic speed advice.

### Layout / Interaction
Reserve geometry for async media/content; keep primary actions available while secondary resources load; do not use skeleton/placeholder behavior that falsely implies completion.

### Color / media
Compression/format changes to screenshots and visual product proof require visual fidelity review, especially UI text, fine lines and gradients.

### Content Design / UX
User-managed. Handoff only when deferral/removal/reordering changes information priority, loading/status language or task continuity.

No Design Studio canonical file is edited here.

---

## 14. OPEN MintTap production facts

- hosting/CDN/origin topology and geographic latency;
- HTTP/cache/compression headers and asset versioning;
- actual HTML/CSS/JS framework and hydration model;
- request waterfall and dependency/initiator chains;
- screenshot/image/video inventory, source dimensions and encoding;
- actual font family/files/weights/scripts/subsets/fallbacks;
- third-party/analytics/consent/embed inventory;
- service worker and repeat-navigation behavior;
- field device/network distribution;
- page-family Primary Readiness Contracts;
- production LCP/INP/CLS causal evidence.

No optimization recommendation for `minttap.app` should pretend these are known.

---

## 15. Competency check

PASS at FOUNDATION/PRACTITIONER if Web Manager can:
1. separate bytes, discovery, priority, dependency, CPU/render and task impact;
2. explain why preload/preconnect/priority hints can help or harm;
3. distinguish compression from caching and cold from repeat contexts;
4. diagnose image cost across size/source/discovery/decode/layout dimensions;
5. treat fonts as delivery + rendering + geometry, not just a file download;
6. distinguish JavaScript transfer from execution/interaction cost;
7. inventory third-party cost beyond request size;
8. trace a metric symptom to a bounded causal intervention without sacrificing correctness/accessibility/product evidence.

**Result: PASS.**

## Next highest-value block
069 — **Performance Budgets, Page-Family Targets, Measurement Toolchain & Release Regression Governance.**

066–068 now establish browser work, user-centric observations and causal resource families. The next gap is governance: turn them into page/task-specific budgets and a lab/field/release evidence system before Stage 7 integration.