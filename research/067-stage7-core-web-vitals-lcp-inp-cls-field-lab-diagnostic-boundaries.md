# 067 — Stage 7: Core Web Vitals from First Principles — LCP, INP, CLS, Field/Lab Evidence & Diagnostic Boundaries

Date: 2026-09-16  
State: **PASS — FOUNDATION/PRACTITIONER**

## Why this block now
066 established the browser-work model before metrics. 067 now asks what current Core Web Vitals actually observe, what their windows/aggregation omit, and how a Web Manager should move from a metric symptom back to browser-phase evidence without score chasing.

## Source set — authoritative/current
- W3C Web Performance Working Group publications: https://www.w3.org/groups/wg/webperf/publications/
- W3C Largest Contentful Paint, Working Draft 13 July 2026: https://www.w3.org/TR/largest-contentful-paint/
- W3C Paint Timing: https://www.w3.org/TR/paint-timing/
- W3C Event Timing API: https://www.w3.org/TR/event-timing/
- Google/web.dev Core Web Vitals and metric guidance: https://web.dev/articles/vitals
- Google/web.dev LCP: https://web.dev/articles/lcp
- Google/web.dev INP: https://web.dev/articles/inp
- Google/web.dev CLS: https://web.dev/articles/cls
- Google/web.dev bfcache: https://web.dev/articles/bfcache

Metric definitions, thresholds, Chrome/CrUX reporting behavior and draft specifications are **CHANGE WATCH**. Rechecked 2026-09-16.

---

## 1. First-principles model

`browser/user experience → bounded observable event/timing stream → metric algorithm/window → per-visit value → population distribution → reporting threshold/classification → diagnostic hypothesis → lower-level evidence → intervention → re-measurement`

A metric is an observation model, not the experience itself.

Standing distinction:

`user experience ≠ Web Vital ≠ PerformanceEntry ≠ lab score ≠ field distribution ≠ root cause`

Core Web Vitals deliberately summarize three useful dimensions: loading/rendering prominence (LCP), interaction responsiveness (INP), and unexpected visual instability (CLS). They do not measure every dimension of readiness, accessibility, correctness, trust, task completion or perceived quality.

---

## 2. SOURCE — LCP observes a heuristic largest-content paint, not “page fully loaded”

The W3C Largest Contentful Paint Working Draft defines an API for monitoring the largest paint triggered by an eligible element. The specification explicitly describes LCP as heuristic and lists limitations. Candidate tracking changes as larger eligible content appears and terminates on certain trusted scroll/input behavior. The API is document-load based and does not itself reset for bfcache restoration or same-document history navigation.

Paint Timing is the lower-level foundation for paint timestamps. It distinguishes rendering-related timing from arbitrary notions such as network completion or application readiness.

### SYNTHESIS
LCP answers approximately: **when did the largest eligible content candidate in the initial viewport/loading episode get painted?** It does not establish:
- all resources loaded;
- primary CTA operable;
- hydration/data state complete;
- correct content;
- task completion readiness;
- absence of later shifts;
- good interaction latency.

Therefore `good LCP → page is fast` is an overclaim.

### Diagnostic decomposition
When LCP is poor, inspect causal stages rather than changing the largest element blindly:
`navigation/server delay → discovery delay → resource transfer → decode/font/render dependency → style/layout/paint → candidate behavior`.

This connects directly to 066.

---

## 3. SOURCE — INP is interaction-to-next-paint evidence, not generic JavaScript speed

Event Timing provides timing information for user interactions. Current Core Web Vitals guidance uses Interaction to Next Paint (INP) as the responsiveness vital. INP evaluates interaction latency over the page visit rather than only initial load.

An interaction can include input delay before handlers run, event-handler processing, and presentation delay before the next paint. These phases may have different causes.

### SYNTHESIS
A poor INP is a symptom of delayed visual response to interaction, not proof that “JavaScript is slow.” Possible causal families include:
- main-thread work already occupying the event loop before the event is handled;
- expensive event-handler work;
- synchronous rendering/style/layout work;
- large DOM/render work before presentation;
- third-party work or unrelated tasks competing for the main thread.

The correct diagnostic question is: **which portion of the interaction latency is large, and what work occupied it?**

### Boundary
A good INP does not prove that:
- every interaction is semantically correct;
- navigation/result is useful;
- accessibility is good;
- animation is smooth;
- network-backed async completion is fast after the immediate next paint.

---

## 4. SOURCE — CLS measures unexpected layout instability through layout-shift evidence

CLS aggregates layout-shift evidence using the Layout Instability model and session-window logic in current web performance guidance. User-initiated/expected shifts are treated differently from unexpected shifts.

### SYNTHESIS
CLS is not a measure of “how much the layout changed” in a visual-diff sense. It is a bounded metric for unexpected instability affecting visible content.

Common causal families include:
- images/media/embeds without reserved geometry;
- late-inserted content;
- font/style changes that alter geometry;
- async components whose final size was not anticipated;
- responsive/component behavior that displaces existing content.

### Boundary
A good CLS does not prove good layout design. A stable but unusable layout can score well. Conversely, an intentional transition may involve movement without representing the same user-harm model as an unexpected shift.

---

## 5. Current thresholds are operational classifications, not natural laws

Google's current Core Web Vitals guidance evaluates page/visit populations using percentile-based field distributions and classifies current LCP, INP and CLS values with published good/needs-improvement/poor boundaries. These boundaries and reporting implementation are platform guidance, not timeless W3C laws.

### MINTTAP DIRECTION
Record threshold/version/source date in performance governance. Never bake a threshold into architectural truth as though browsers or human perception are defined by that number.

Use thresholds as release/monitoring signals only after page-family/task requirements are understood.

---

## 6. Field evidence and lab evidence answer different questions

### SOURCE/SYNTHESIS
Field/RUM/CrUX-like evidence observes real visits across heterogeneous devices, networks, caches, navigation histories and user behavior, but aggregation can obscure causal detail and low-traffic niche sites may have sparse/no public field data.

Lab runs offer controlled reproducibility and detailed traces, but one device/network/scripted journey is not a population claim. Some metrics are also difficult or impossible to represent faithfully without real interaction distributions.

### Operating distinction
- **Field:** `What did a real population experience under observed conditions?`
- **Lab/trace:** `Under this controlled condition, what browser work caused this result?`

Use them together:
`field symptom/segment → reproducible lab hypothesis → trace/root cause → bounded fix → lab regression check → field re-observation`.

Never replace missing field evidence with a Lighthouse run and call it “real-user performance.”

---

## 7. Population aggregation can hide minority failure

A percentile/report classification summarizes a distribution. It does not mean every visit met the threshold. Device, network, geography, page family, navigation type, cache state and user path can form materially different populations.

### MINTTAP DIRECTION
When sufficient traffic exists, segment before interpreting:
- page family/route;
- device class;
- geography/locale where relevant;
- navigation type;
- app-launch/support/governance task context;
- release/change window.

Do not create tiny segments that destroy statistical usefulness; preserve sample-size/evidence limitations.

---

## 8. Lifecycle/window semantics matter

The LCP Working Draft explicitly notes document-load limitations for bfcache restoration and same-document history navigations. Current web.dev guidance notes that CrUX-style tools treat bfcache restores as separate page visits and describes special handling/approximation for LCP, INP and CLS. The web-vitals library supports bfcache restores in its reporting.

### SYNTHESIS
A Web Manager must know **what counts as a visit/window** before comparing numbers. SPA/same-document navigation, bfcache, prerender/background-tab behavior and long-lived sessions can make naive metric collection semantically wrong even when the arithmetic is correct.

### CHANGE WATCH
Metric lifecycle handling is implementation/tool-sensitive. Validate the measurement library/report definition used by the actual MintTap stack.

---

## 9. Core Web Vitals are not the Primary Readiness Contract

066 established task-relative readiness. 067 preserves that distinction.

Example: a product page may paint a large hero quickly (good LCP), remain visually stable (good CLS), and respond quickly to a button press (good INP), while the button's required destination/data is wrong or the important support information is absent.

Conversely, a page can have a mediocre metric because of a noncritical visual asset while the user's primary support task is already usable.

### MINTTAP DIRECTION
Keep two joined but separate records:
1. **Primary Readiness Contract** — what content/action must be available for the page's real task;
2. **Performance Evidence Contract** — LCP/INP/CLS plus causal timings/traces and population context.

Do not let Core Web Vitals replace task requirements.

---

## 10. Performance Evidence Contract

For each representative page family/release, record:

| Field | Purpose |
| --- | --- |
| route/page family + locale | comparison identity |
| primary user task/readiness contract | experience target |
| measurement source/tool/version | evidence provenance |
| field vs lab | evidence class |
| observation window/date | temporal context |
| sample/population | denominator |
| device/network/navigation context | segmentation |
| LCP value/distribution + candidate | loading symptom |
| INP value/distribution + interaction | responsiveness symptom |
| CLS value/distribution + shift sources | stability symptom |
| lower-level timing/trace evidence | causal investigation |
| release/change identity | intervention join |
| hypothesis | synthesis, not fact |
| intervention | bounded change |
| regression result | controlled validation |
| field re-observation | population outcome |
| unresolved limitations | prevents overclaim |

Evidence labels remain `SOURCE/OBSERVED`, `SYNTHESIS`, `OPEN`, `VALIDATION`, `CHANGE WATCH`.

---

## 11. Failure patterns to reject

1. **Score chasing:** optimize a composite/tool score without tracing the user symptom.
2. **Metric substitution:** claim LCP means full readiness, INP means all interactions are good, or CLS means good layout.
3. **Single-run certainty:** generalize one lab run to production population.
4. **Field-only diagnosis:** infer root cause directly from a percentile.
5. **Threshold absolutism:** treat current Google boundaries as universal human laws.
6. **Unsegmented aggregation:** ignore route/device/navigation differences.
7. **Optimization externality:** improve one metric by damaging accessibility, content priority, image legibility, task continuity or maintainability.
8. **Measurement drift:** compare data whose metric/tool/lifecycle definitions changed without annotation.

---

## 12. Design Studio dependency / handoff

Latest `design-studio/progress/WEB_STATUS.md` checked 2026-09-16: Web Stage 1 PASS / Stage 2 PRACTICE NOT PASSED; W017 Chromium transfer 12/12; real Fetch/DOM/network and true HTTP navigation remain OPEN/BLOCKED; W007 request/paint/readiness/stability measurement remains an explicit gap.

### Web Design handoff
When W007/runtime measurement becomes executable, record candidate/interaction/shift evidence rather than only final scores:
- actual LCP candidate and its discovery/render dependency;
- representative INP interaction and input/processing/presentation breakdown where tooling permits;
- layout-shift sources/session context;
- navigation/cache/bfcache context;
- Primary Readiness Contract alongside the vitals.

### Type handoff
Font loading/substitution can affect paint timing and geometry. Actual shipped fonts, fallback and layout effects remain production validation, not an inferred font rule.

### Layout/Interaction handoff
Reserve geometry for async/media states where appropriate and test that pending→resolved transitions do not unexpectedly displace task-critical content. For responsiveness, preserve immediate truthful feedback without faking completion.

### Content Design / UX
User-managed. Hand off evidence if performance prioritization changes information order/loading messages or if real interaction/shift evidence suggests task-orientation harm. Metrics alone do not establish a content/UX defect.

No Design Studio canonical file is edited.

---

## 13. OPEN MintTap facts
- actual production route/page-family inventory;
- rendering/hydration architecture;
- field Core Web Vitals availability/traffic sufficiency;
- RUM/analytics instrumentation and privacy constraints;
- actual LCP candidates by route;
- actual INP interaction distribution and causal phases;
- actual layout-shift sources;
- navigation/bfcache/SPA behavior;
- device/network/user population;
- performance tool/library versions;
- performance release thresholds/budgets;
- actual Primary Readiness Contracts.

Do not fabricate production scores or causes.

---

## 14. Competency check
PASS at FOUNDATION/PRACTITIONER if Web Manager can:
1. explain LCP, INP and CLS as bounded observation models rather than generic speed scores;
2. state important lifecycle/heuristic limitations;
3. move from each metric symptom to plausible browser-phase causal families without claiming causality prematurely;
4. distinguish field population evidence from controlled lab/trace evidence;
5. preserve percentile/sample/segment context;
6. keep current thresholds and tooling behavior on change watch;
7. join Core Web Vitals to, but not replace, task-relative readiness;
8. define a traceable measurement→hypothesis→intervention→re-observation workflow.

**Result: PASS.**

## Next highest-value block
068 — **Performance Causality: Network/Server/Resource Prioritization, Caching/Compression, Images/Fonts/JavaScript & Third-Party Cost.**

066 explains browser phases and 067 explains the user-centric symptoms. 068 should now study the major causal resource/delivery families and trade-offs before building budgets or running an integration gate.