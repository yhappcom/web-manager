# 070 — Stage 7 Integration: Performance Diagnostic & Release Operating System

Date: 2026-09-16
Status: **PASS — FOUNDATION/PRACTITIONER INTEGRATION GATE**

## Purpose
Integrate 066–069 into one repeatable operating model for diagnosing and governing web performance for an Apple/Android app company website without collapsing performance into a score, file size, or single Core Web Vital.

## Evidence labels
- **SOURCE** — directly established by authoritative standards/platform documentation.
- **SYNTHESIS** — transferable conclusion derived from the source model.
- **MINTTAP DIRECTION** — recommended operating direction; not a claim about current production implementation.
- **OPEN** — unknown until actual `minttap.app` evidence exists.
- **DEPENDENCY** — evidence/work required from another domain.
- **VALIDATION** — production/browser/field test required.
- **CHANGE WATCH** — browser/tool/spec behavior that can evolve.

## Authoritative source check — 2026-09-16
Primary references rechecked for this integration:
- W3C Web Performance Working Group and current publications: https://www.w3.org/webperf/ and https://www.w3.org/groups/wg/webperf/publications/
- W3C Resource Timing: https://www.w3.org/TR/resource-timing/
- W3C Largest Contentful Paint: https://www.w3.org/TR/largest-contentful-paint/
- web.dev bfcache performance-measurement guidance: https://web.dev/articles/bfcache

**SOURCE:** Web performance observability is deliberately distributed across multiple timing/observation specifications: navigation, resources, user timing, paint, event timing, LCP, long tasks/animation frames and related APIs. These specifications also have different maturity states. A single synthetic score is therefore not the underlying standards model.

**CHANGE WATCH:** exact Core Web Vitals definitions, thresholds, browser implementations, report aggregation and specification maturity are versioned/current behavior, not timeless laws.

---

# 1. Integrated mental model

`user task → navigation context → delivery → resource discovery/dependency → parse/style/layout/paint/main-thread work → visible/operable readiness → metric observation → causal evidence → intervention → regression gate → release → field/task re-observation`

The critical separation is:

`experience symptom ≠ metric ≠ browser phase ≠ resource cause ≠ fix ≠ release decision`

A professional diagnosis must preserve those layers.

## Three contracts retained

### Primary Readiness Contract
For each page family/task:
- primary content that must become understandable;
- primary action that must become operable;
- dependencies that gate those outcomes;
- secondary work that can safely be deferred;
- pending/error feedback that prevents false readiness.

### Performance Evidence Contract
Preserve:
- route/page family/task;
- navigation/cache/bfcache context;
- field vs lab provenance and population;
- metric values plus LCP candidate, representative INP interaction/latency phases and CLS shift sources where available;
- lower-level navigation/resource/main-thread/render evidence;
- release/change identity;
- intervention and re-observation.

### Resource Criticality Matrix
For each meaningful resource/dependency:
- primary-task necessity;
- discovery timing and initiator;
- network criticality;
- CPU/decode/render cost;
- layout-stability risk;
- cache reuse;
- safe deferrability;
- evidence supporting the classification.

---

# 2. Diagnostic operating procedure

## Step A — State the user-visible symptom
Examples:
- product proof appears late;
- page looks ready but primary CTA does not respond promptly;
- support content shifts while the user is reading;
- repeat navigation is unexpectedly slow;
- a release worsened field performance for a page family.

Do not begin with “improve Lighthouse.”

## Step B — Preserve context before changing code
Record:
- route/page family and primary task;
- release/build identity;
- browser/device/network profile;
- cold/warm/cache/bfcache/navigation state;
- lab or field source;
- measurement/tool version;
- timestamp and relevant experiment flags.

Without context, before/after comparisons can become false evidence.

## Step C — Use the metric as a symptom locator, not diagnosis
- poor LCP → identify actual candidate and its discovery/transfer/render chain;
- poor INP → identify representative interaction, then separate input delay, processing and presentation/render delay;
- poor CLS → identify actual shift source/session window and geometry dependency;
- good CWV but poor task readiness → investigate readiness contract, app/data/script/state dependencies instead of declaring performance solved.

## Step D — Map to browser phase and causal dependency
Ask in order:
1. Was document/server/navigation delivery late?
2. Was the critical resource discovered late?
3. Was priority/dependency ordering wrong?
4. Was transfer/cache/compression the bottleneck?
5. Was decode/font/style/layout/paint expensive?
6. Was JS/main-thread work blocking interaction?
7. Did third-party work contend for network/main-thread/rendering?
8. Did async content lack geometry/state continuity?

## Step E — Apply the narrowest justified intervention
Examples:
- fix discovery rather than globally preload everything;
- correct image source/dimensions rather than blindly compress every image;
- reduce/sequence execution rather than treating cached JS as free;
- reserve geometry rather than hiding legitimate async content;
- remove/defer an unnecessary third party rather than degrade primary content fidelity;
- change font delivery only with Type/fidelity/layout evidence.

## Step F — Reproduce and regress
A candidate fix must be tested against:
- the original symptom/context;
- primary task correctness;
- accessibility;
- visual/content fidelity;
- representative responsive/localized states;
- adjacent performance dimensions.

A faster but incorrect, inaccessible or misleading page is a failed intervention.

## Step G — Release gate
Use the hierarchy:

`task invariant → user-experience budget → causal budget → diagnostic guardrail`

Block when a material reproducible regression threatens a justified contract. Do not block merely because one noisy score moved slightly.

## Step H — Field re-observation
After release:
- wait for appropriate field evidence;
- segment by relevant page family/population/context;
- compare with release/change identity;
- verify downstream task evidence where available;
- keep lab reproduction available for causal follow-up.

---

# 3. Representative competency scenarios

## Scenario 1 — Product hero screenshot becomes the LCP problem
Evidence path:
`LCP regression → candidate = hero media → late discovery? wrong source? transfer? decode? paint?`

Bad response: compress every image and preload all hero variants.

Correct response: inspect candidate, responsive source selection, intrinsic dimensions, discovery/priority, transfer and decode; change only the causal layer. Preserve product-proof fidelity.

## Scenario 2 — Page visually loads quickly but Store CTA feels frozen
Evidence path:
`Primary Readiness failure + interaction evidence → input delay / handler processing / presentation delay → main-thread/third-party/hydration cause`

Bad response: declare success because LCP is good.

Correct response: treat operability separately from visual readiness and inspect the actual interaction path.

## Scenario 3 — Support article shifts after font/media/async insertion
Evidence path:
`CLS/direct geometry → shift source → missing reserved geometry/font metric change/late content insertion`

Bad response: remove useful support content to improve score.

Correct response: preserve content and fix geometry/delivery/state continuity.

## Scenario 4 — One Lighthouse run regresses after a release
Evidence path:
`single run → baseline variance/tool context → repeated controlled evidence → causal trace → field corroboration if material`

Bad response: emergency rollback based only on one synthetic score.

Correct response: apply the predeclared regression contract and reproduce material change.

## Scenario 5 — Repeat navigation is fast while first visit is slow
Evidence path:
`navigation/cache state → Resource Timing/cache behavior → cold critical path`

Bad response: average cold and warm runs and report one number.

Correct response: preserve navigation/cache populations separately. bfcache restores are also a distinct lifecycle context; current web.dev guidance notes that CrUX-style Core Web Vitals collection treats bfcache restores as separate page visits.

---

# 4. Performance release operating record

For a real release, retain one record containing:
- release/build/commit;
- changed page families/tasks;
- expected performance effect;
- Primary Readiness Contract affected;
- baseline contexts and variance;
- deterministic/static checks;
- controlled browser/lab results;
- trace/resource evidence;
- budget/gate result;
- accessibility/correctness/fidelity result;
- exception owner/rationale/expiry if any;
- deployment timestamp;
- field/RUM re-observation window/result;
- downstream task observation;
- follow-up decision.

This creates an auditable chain from change to user consequence rather than a screenshot of a score.

---

# 5. Design Studio handoff

Latest `progress/WEB_STATUS.md` checked 2026-09-16:
- Web Design is now **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE**;
- W021 has an integrated executable specimen, but actual browser execution is still the next step;
- real HTTP/network, cross-browser, screen-reader, physical-device, field-performance and human-UX evidence remain OPEN.

**DEPENDENCY — Web Design:** when W021 or later integrated browser/runtime work is executed, preserve task/readiness milestones and geometry evidence, but do not promote local specimen timings to production performance targets.

**DEPENDENCY — Type:** production font family/weight/script requirements and visual suitability come from Type; Web/engineering should return actual font discovery/transfer/fallback/layout evidence.

**DEPENDENCY — Layout/Interaction:** async geometry, primary-action continuity and truthful pending/outcome states must survive performance interventions.

**DEPENDENCY — visual/media design:** image/video optimization that changes product proof requires fidelity review, not byte-only approval.

**DEPENDENCY — Content Design/UX:** user-managed specialists receive evidence only when performance work changes information priority/loading language or when observed readiness/interaction problems materially affect task comprehension/completion.

No Design Studio canonical file is edited by this study.

---

# 6. MintTap OPEN / VALIDATION

No production performance claim is made. Still OPEN:
- actual `minttap.app` route/page-family/task inventory;
- framework/rendering/hydration architecture;
- hosting/CDN/origin topology;
- HTTP/cache/compression headers;
- resource waterfall and dependency graph;
- production media/font/JS/CSS/third-party inventory;
- service-worker/cache behavior;
- actual device/network/navigation population;
- field/RUM Core Web Vitals and task evidence;
- baseline variance and CI/release tooling;
- justified numeric budgets and regression thresholds.

**VALIDATION:** these must be measured from the real implementation before MintTap-specific budgets or performance claims are approved.

---

# 7. Stage 7 competency gate

PASS criteria:
1. Explain browser performance from navigation through task readiness rather than one load duration.
2. Explain what LCP/INP/CLS observe and what they do not prove.
3. Separate field population evidence from controlled lab/trace evidence.
4. Trace a metric/task symptom to browser phase and causal resource/dependency.
5. Distinguish bytes, discovery, transfer, CPU/decode/render, layout and task cost.
6. Select bounded interventions instead of generic optimization checklists.
7. Define task/page-family budgets without inventing unsupported universal numbers.
8. Preserve baseline variance, context and release identity.
9. Gate material reproducible regressions without sacrificing accessibility/correctness/fidelity.
10. Re-observe production field/task outcomes after release.
11. Identify Design Studio and implementation dependencies without fabricating evidence.

Result: **PASS — FOUNDATION/PRACTITIONER.**

Stage 7 is complete at the intended curriculum level. Production `minttap.app` performance remains OPEN until real implementation and field evidence exist.

## Next curriculum move
Proceed to **Stage 8 — Security / Privacy / Trust**, beginning from first principles rather than jumping directly to CSP/header configuration.