# 069 — Stage 7: Performance Budgets, Measurement Toolchain & Release Regression Governance

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER**

## Purpose
066 established browser-work mechanics, 067 bounded Core Web Vitals as observations, and 068 mapped delivery/resource causes. This block turns those concepts into an operating system for preventing regressions without inventing universal byte or score targets.

## SOURCE — authoritative evidence

### Web Performance APIs are an evidence substrate, not one score
The W3C Web Performance Working Group maintains distinct specifications including Navigation Timing, Resource Timing, Performance Timeline, User Timing, Server Timing, Paint Timing, Event Timing, LCP and Long Animation Frames. Their publication maturity differs. Source checked 2026-09-16: https://www.w3.org/webperf/ and https://www.w3.org/groups/wg/webperf/publications/

Resource Timing exposes detailed timing information for document resources. User Timing provides application-defined high-resolution marks/measures, allowing product-specific milestones that browser-generic metrics cannot know. Specification maturity/version must be recorded rather than treating all APIs as a timeless bundle.

### Performance budgets are constraints, not universal constants
Google/web.dev material documents budget mechanisms such as resource-size/count budgets and historical example budgets. Those examples are not MintTap requirements and are not copied as targets here. A budget must derive from a page/task contract and representative environment, then be validated against real evidence.

## SYNTHESIS — what a performance budget actually is
A useful budget is a **pre-declared boundary on an evidence-bearing performance variable whose regression would threaten an important user task**.

Therefore:

`budget != optimization wish != Lighthouse score != arbitrary industry number`

A budget may constrain:
- task-relative milestone/readiness;
- LCP/INP/CLS field or controlled-lab behavior;
- critical-path request count/bytes;
- critical JS execution/main-thread work;
- image/font/third-party cost;
- regression delta against a known baseline.

The correct unit depends on the causal risk.

## Page-family model
MintTap should not assume one budget for every URL. Future production evidence should classify at least representative Company, Product, Support and Governance families, and any materially different campaign/status/account surface if they actually exist.

For each family record:
1. primary user task;
2. Primary Readiness Contract;
3. representative content/data state;
4. representative viewport/device/network/navigation contexts;
5. critical resources and third parties;
6. baseline field/lab evidence;
7. metric/resource regression boundaries;
8. exceptions and expiry/review owner.

A privacy page and screenshot-heavy product page can have different resource profiles while both remaining acceptable for their tasks.

## Measurement hierarchy
Use complementary evidence rather than a single dashboard:

### Layer A — deterministic/static release checks
Examples: unexpected asset growth, number of third-party origins, missing intrinsic media geometry, newly introduced blocking dependencies. Good for fast regression detection; weak for real-user experience.

### Layer B — controlled browser/lab runs
Use representative routes/states and repeatable conditions to inspect waterfall, initiator chain, CPU/main-thread work, LCP candidate, interaction latency phases, shifts and task milestones. Good for causal debugging; not population evidence.

### Layer C — production field/RUM
Observe actual heterogeneous users, navigation/cache/device/network distributions and page families. Good for population outcome; aggregates alone do not reveal root cause.

### Layer D — task/business evidence
Confirm whether the page became usable and the intended task remained achievable. Performance metrics cannot prove comprehension, accessibility, correctness or conversion causality.

Operating loop:
`baseline → declared budget → pre-release deterministic/lab regression → release → field observation → segmented anomaly → causal trace → bounded fix → regression test → field re-observation`

## Release-gate discipline
A release gate should block on **material, reproducible regression against a justified contract**, not any small score movement.

Before blocking, preserve:
- route/page family and build/release identity;
- tool/browser/version;
- run conditions and number of runs;
- baseline distribution, not only one run;
- absolute value and delta;
- candidate/interaction/shift/resource cause where known;
- primary-task impact hypothesis;
- whether the regression is deterministic, lab-only, field-only or cross-evidence.

Do not gate production on one noisy Lighthouse run or a universal score of 100.

## Variance and false precision
Performance measurements vary because of scheduling, cache state, network, device, server, content and browser conditions. Consequently:
- preserve distributions/repeated runs where feasible;
- compare like with like;
- distinguish cold/warm and normal/bfcache navigation;
- do not report millisecond-level precision as product certainty when the environment is variable;
- use regression ranges/tolerances only after baseline variance is known.

## Budget hierarchy
A practical hierarchy is:

1. **Task invariant** — primary content/action must remain available and correct.
2. **User-experience budget** — task milestone and relevant LCP/INP/CLS evidence.
3. **Causal budget** — critical JS/media/font/third-party/request/dependency constraints.
4. **Diagnostic guardrail** — bundle/resource counts and automated audit signals.

Lower layers support higher ones. Passing a byte budget cannot override a failed primary task; failing a generic audit does not automatically prove user harm.

## Exceptions governance
A budget exception must record:
- reason and user/product value;
- affected page family;
- measured cost;
- alternatives considered;
- compensating mitigation;
- owner;
- review/expiry trigger.

This prevents permanent performance debt from entering through undocumented launch exceptions.

## App-company specific judgment
For a company publishing Apple/Android apps, common web additions such as product screenshots/video, store badges, analytics, consent tooling, support widgets and campaign scripts should enter the Resource Criticality Matrix before becoming default dependencies on every page.

A product demonstration can justify cost on a Product page while being unnecessary on Governance/Support pages. Shared global bundles/third-party tags can silently impose that cost across the entire site; page-family measurement is therefore required.

## Relationship to accessibility/design/content
Performance interventions must not create false wins by removing meaningful labels, reducing text legibility, breaking zoom/reflow, hiding required content, delaying consequential feedback or replacing accessible controls with lighter but inferior custom behavior.

Performance is a constraint within product quality, not permission to trade away correctness/accessibility without evidence and explicit decision.

## Design Studio dependency / handoff
Latest `yhappcom/design-studio/progress/WEB_STATUS.md` checked 2026-09-16. W018 now provides bounded Chromium evidence separating first frame, data visibility and task readiness and demonstrates reserved vs unreserved async geometry. It explicitly does **not** establish production LCP/INP/CLS or human perceived speed.

Handoff for future live-project/runtime work:
- Web Design: expose representative page-family/task milestones and geometry states; retain W018 direct geometry diagnostics when CLS instrumentation is silent; do not turn W018 millisecond values into targets.
- Type: production font family/weight/script decisions require measured delivery/fallback/layout evidence before a budget is finalized.
- Layout/Interaction: async reservation and task continuity are part of readiness/stability budgets.
- Media/visual fidelity: compression/resizing decisions require visual-quality review where product proof is affected.
- Content Design/UX remain user-managed; hand off only when performance gating changes content priority, pending/error language or task flow.

No Design Studio canonical file is edited.

## OPEN — MintTap production facts
Do not invent budgets until these are verified:
- actual page/route families and primary tasks;
- frontend/rendering/hydration architecture;
- hosting/CDN/origin/cache/compression behavior;
- production image/video/font/JS/CSS/third-party inventory;
- representative user device/network/geography distribution;
- production RUM/CrUX availability and privacy constraints;
- baseline repeated lab runs and field distributions;
- release/CI system capable of enforcing checks;
- acceptable product-specific trade-offs and owners.

## VALIDATION — future production gate
A MintTap performance budget becomes production-valid only after:
1. representative page family/task is defined;
2. baseline variance is measured;
3. budget is tied to a user/task or causal risk;
4. automated/lab check is reproducible;
5. accessibility/correctness/design invariants are retained;
6. release identity is traceable;
7. field evidence is reviewed after deployment;
8. exceptions have owner and review trigger.

## Competency gate
PASS if the Web Manager can:
- explain why a performance budget is not a universal byte/score target;
- choose task, UX, causal and diagnostic budgets appropriately;
- distinguish deterministic, lab, field and task evidence;
- design a regression gate without treating one noisy run as truth;
- preserve measurement context/version/baseline variance;
- govern exceptions and cross-domain quality constraints;
- refuse to invent MintTap targets before production evidence exists.

Result: **PASS**.

## Next highest-value block
070 — **Stage 7 Integration: Performance Diagnostic & Release Operating System**. Integrate 066–069 across representative failure scenarios, test the Stage 7 foundation/practitioner gate, and close Stage 7 only if causal diagnosis, evidence selection and governance transfer coherently.