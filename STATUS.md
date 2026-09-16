# MintTap Web Manager Status

Operating state: **ACTIVE — STRUCTURED BEGINNER→ADVANCED / DEEP-DOMAIN STUDY**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play

## Mission state
Build professional Web Manager judgment from first principles through advanced cross-domain reasoning. GitHub is canonical memory; chat is temporary context. Canonical curriculum: `LEARNING_ROADMAP.md`.

Learning sequence: `history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`.

---

# Stages 1–6
**COMPLETE — FOUNDATION/PRACTITIONER CURRICULUM GATES PASSED.**
- Stage 1 Web Foundations: 027–033.
- Stage 2 Website Anatomy / Content / IA: 034–038.
- Stage 3 UX & Interaction Foundations: 039–044.
- Stage 4 Web Design Literacy: 045–050.
- Stage 5 Accessibility: 051–058.
- Stage 6 Search / Discovery / Content Quality: 059–065.

Production accessibility/search quality remain OPEN pending real `minttap.app` implementation/browser/AT/crawler/store/task evidence.

---

# Stage 7 — Web Performance / Browser Runtime
**ACTIVE — FOUNDATION/PRACTITIONER STUDY.**

066 — **Web Performance Foundations: Navigation Lifecycle, Critical Rendering Path, Resource Loading, Main-Thread/Rendering Work & Perceived Readiness — PASS.**

Established model:
`navigation intent → network/document response → HTML parsing/resource discovery → DOM/CSSOM/script dependencies → style/layout → paint/composite → visible content → main-thread/event-loop availability → task-relative readiness → later stability`.

Retained judgments through 066:
- performance is not one duration and browser `load` is not synonymous with user readiness;
- navigation timing and resource timing observe different scopes;
- total bytes alone do not determine readiness: dependency depth, discovery order, priority and execution/render cost matter;
- parser blocking, script-blocking stylesheet behavior and render blocking are distinct concepts;
- critical rendering work includes document/style construction, style/layout and drawing, with scripts able to alter dependencies/state;
- event loops coordinate script/events/rendering/network-related work but are not specified as one-to-one implementation threads;
- a page can look loaded while synchronous/main-thread work delays interaction;
- resource criticality is task/context-specific, not determined solely by file type;
- performance diagnosis should follow `user symptom → browser-phase hypothesis → timing/trace evidence → causal dependency → bounded intervention → re-measurement` rather than score-driven checklists;
- future page families should define a Primary Readiness Contract: primary visible content, primary operable action, gating dependencies, safely deferrable work and pending feedback;
- production performance claims require actual runtime/field evidence.

Specification maturity is kept explicit: W3C Web Performance deliverables are at different statuses and must not be treated as one timeless API bundle.

Highest-value next block:
067 — **Core Web Vitals from First Principles: LCP, INP, CLS, Metric Windows, Field vs Lab Evidence & Diagnostic Boundaries.**

Study the metrics only after the browser-work model so optimization does not collapse into score chasing.

---

# Design Studio relationship
Latest `design-studio/progress/WEB_STATUS.md` checked 2026-09-16:
- Web Design Stage 1 PASS / Stage 2 PRACTICE NOT PASSED;
- W017 icon/non-text Chromium transfer 12/12 after preserved failure/revision;
- real Fetch/DOM/network and true HTTP navigation remain OPEN/BLOCKED in the current environment;
- W007 request/paint/readiness/stability measurement remains an explicit Web gap.

### Stage 7 handoff
066 gives the W007/runtime handoff a performance-phase contract: distinguish request/navigation, resource discovery/transfer, parser/render blocking, style/layout/paint/composite, main-thread availability, task-relative readiness and later stability. Deterministic visual/browser assertions do not establish field performance.

Type should later validate actual production font files/subsetting/fallback/load/layout effects. Layout/Interaction should preserve primary task availability under pending secondary media/data and avoid false readiness/layout instability. Content Design and UX remain user-managed; Web Manager records evidence handoffs if performance interventions affect information priority, loading language, perceived readiness or task continuity.

No Design Studio canonical file was edited.

---

# Important unknown MintTap facts
Real project decisions still require verified evidence for actual app/page/process inventory, frontend/component library/router, production brand/fonts/components, supported locales, analytics/privacy constraints and accessibility/search production evidence.

Stage 7 additionally requires actual rendering/deployment architecture, HTTP/navigation/resource timing, waterfall/cache behavior, JS/CSS dependency graph, image/video/font inventory, third-party scripts, service-worker behavior, page-family readiness definitions, device/network population, field performance/Core Web Vitals and performance release gates. Do not infer these from generic app-company patterns.

---

# Persistence state
- `LEARNING_ROADMAP.md` remains canonical curriculum.
- `research/README.md` indexes staged learning.
- Stages 1–6: COMPLETE at intended foundation/practitioner level.
- Stage 7: **ACTIVE; 066 PASS.**
- Current next work: **067 — Core Web Vitals from First Principles**.
- Reporting cadence remains coarse: deep internal study, consolidated persistence/reporting.