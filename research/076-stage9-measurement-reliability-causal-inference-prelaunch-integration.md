# 076 — Stage 9 Measurement Reliability, Causal Inference & Pre-Launch Integration

Date: 2026-09-16
State: **PASS — STAGE 9 FOUNDATION/PRACTITIONER INTEGRATION GATE**
Primary owner: **Track D — Search, Discovery & Analytics**
Consumers: B task semantics; C quality guardrails; E privacy/operations; A browser/PWA lifecycle.

## Purpose
Close Stage 9 at the intended foundation/practitioner level by proving that Web Manager can distinguish measurement from reality, diagnose missing/biased data, design bounded experiments, and define a pre-launch measurement plan before a vendor dashboard exists. PWA offline/install/sync remains a stress case, not a reason to redefine product truth around telemetry.

## Source basis and freshness
Authoritative material rechecked 2026-09-16:
- NIST/SEMATECH e-Handbook of Statistical Methods — experimental objectives, randomized designs, blocking/confounding, replication, statistical vs practical significance.
- Google Analytics Help / Developers — GA4 data-quality indicators, sampling/thresholding, observed vs modeled consent data, consent-mode behavior, Measurement Protocol timestamps/late-event constraints.
- W3C Privacy Principles — measurement can often be performed through aggregation without exposing individual contribution.

Vendor limits, consent-mode eligibility, report behavior, browser/platform observability and Measurement Protocol constraints are **CHANGE WATCH**. Statistical principles and evidence separations below are durable.

## 1. Integrated evidence model

`decision → target population/task → product truth → observable signal → collection mechanism → missingness/selection → transformation/modeling → metric/uncertainty → alternative explanations → causal design if needed → guardrails → decision → intervention → re-observation`

The central rule is:

`reality ≠ observable population ≠ collected data ≠ processed report ≠ modeled estimate ≠ causal effect`

A trustworthy dashboard therefore requires an evidence lineage, not merely a correct chart.

## 2. Measurement reliability is a system property
A metric can fail even when its arithmetic is correct. Reliability requires at least:
- stable semantic definition;
- known eligible denominator;
- trigger correctness;
- versioned schema;
- delivery expectations;
- duplicate/late-event policy;
- known consent/blocking/offline gaps;
- transformation/reporting knowledge;
- anomaly/reconciliation checks;
- release linkage.

### Reliability failure classes
1. **Semantic drift** — same event name changes meaning across releases.
2. **Coverage loss** — route, locale, browser or consent class stops reporting.
3. **Duplicate delivery** — retry/replay inflates counts.
4. **Late/out-of-order delivery** — occurrence time and ingestion time diverge.
5. **Eligibility drift** — denominator population changes while metric name stays constant.
6. **Transformation drift** — vendor report/model/sampling/threshold behavior changes.
7. **Identity discontinuity** — cookie/device/session boundaries change user/session counts.
8. **Instrumentation interference** — telemetry adds runtime/privacy cost or fails the task it observes.

**SOURCE:** GA4 exposes a data-quality indicator because reports/explorations can involve sampling, thresholding or other quality states. GA4 also distinguishes observed and modeled data under consent-mode behavior. These are concrete examples of why report output cannot be treated as raw ground truth.

**SYNTHESIS:** every decision-relevant metric should carry a `measurement status`: semantics/version, coverage, missingness, modeled/sampled/thresholded state where applicable, and known incidents.

## 3. Missingness is not automatically random
Observed users may differ systematically from unobserved users because of:
- consent choice;
- content blockers;
- browser/platform capability;
- offline duration;
- failed scripts/network requests;
- geographic/jurisdictional configuration;
- authentication state;
- app/web/cross-device handoff;
- release/version bugs.

Therefore:
`observed conversion rate ≠ population conversion rate` unless the observation process supports that inference.

**SOURCE:** Google documents behavioral modeling specifically because consent denial creates unobserved behavior; modeled and observed data are distinguishable concepts and modeling has eligibility requirements.

**CONTRADICTION:** “We have 100% of the events visible in this report” does not mean “we observed 100% of real users/tasks.” Report completeness is conditional on what entered that measurement system.

### Missingness register
For every major metric document:
- who can be observed;
- who may be absent;
- why absence may correlate with behavior;
- whether vendor modeling is present;
- whether conclusions change if missing users behave differently;
- which independent evidence can bound the uncertainty.

## 4. Late, duplicate and offline telemetry
PWA makes delivery semantics explicit.

Product truth from 073–074 remains:
`local save → durable outbox → transport → remote apply → acknowledgement → reconciliation/conflict`.

Analytics is a separate observer.

Rules:
- preserve event occurrence time separately from ingestion time where justified;
- define whether repeated event IDs are deduplicated analytically;
- never infer sync correctness from analytics arrival order;
- never make product acknowledgement depend on analytics acknowledgement;
- long-offline events may fall outside vendor backfill/join windows;
- dashboards should identify data-freshness windows before declaring a regression.

**SOURCE / CHANGE WATCH:** GA4 Measurement Protocol currently documents timestamp precedence and constraints for backdated events, including special processing limits for events intended to join client-collected data. This is a vendor constraint, not a universal PWA rule.

## 5. Attribution and identity discontinuity
Attribution is an evidence model under partial observation. It can be disrupted by:
- cross-device web→store→app journeys;
- browser privacy/storage boundaries;
- consent;
- direct/bookmark/revisit behavior;
- campaign parameter loss;
- store reporting boundaries;
- modeled data;
- different identity scopes.

Do not merge web analytics, Search Console, App Store/Play reporting and app analytics into a fictitious universal user history unless an actual permitted identity/measurement architecture establishes the join.

Useful output is instead an **evidence mosaic**:
`search exposure evidence + web landing evidence + outbound store handoff evidence + store acquisition evidence + app activation evidence`, each with its own denominator and uncertainty.

Marketing receives channel evidence with these limits; it owns acquisition strategy.

## 6. Causal inference: when observation is insufficient
A pre/post metric change can be explained by treatment plus:
- seasonality/time;
- traffic mix;
- simultaneous release changes;
- external events;
- regression to the mean;
- instrumentation changes;
- novelty/learning;
- platform/browser changes.

A causal claim therefore requires a design that makes competing explanations less plausible.

### Randomization
**SOURCE:** NIST describes completely randomized designs as random assignment of factor levels to experimental units. Randomization reduces systematic allocation bias and supports defensible comparison under the design.

For web experiments specify:
- experimental unit: user/session/device/page-view/etc.;
- stable assignment boundary;
- treatment/control eligibility;
- exposure event distinct from assignment;
- contamination/crossover risk;
- primary outcome and guardrails;
- analysis population.

Assignment without actual exposure answers a different question from treatment-on-exposed analysis. Do not silently swap them.

### Blocking/stratification
**SOURCE:** NIST explains blocking as controlling important nuisance factors, with randomization addressing remaining nuisance variation.

Web translation: locale/platform/page-family can sometimes be pre-specified blocking/stratification dimensions when they are known to materially affect outcomes. Do not discover dozens of segments after the result and select the favorable one.

### Replication and repeated evidence
One successful experiment is bounded evidence for the tested population, implementation and period. Replication across releases/surfaces can test robustness. It does not create a timeless universal law.

## 7. Statistical vs practical significance
**SOURCE:** NIST explicitly distinguishes statistical significance from practical/engineering significance; sample size affects detectability.

Web Manager decision contract:
- effect estimate, not only p-value;
- uncertainty interval where appropriate;
- minimum practically meaningful change defined before interpretation where feasible;
- guardrail effects;
- implementation/reversal cost;
- evidence quality and missingness.

`statistically detectable ≠ worth shipping`

and

`not statistically significant ≠ proven equal`.

## 8. Experiment validity checklist
Before trusting an A/B result, diagnose:
1. objective/hypothesis was pre-specified;
2. randomization unit matches interference/identity reality;
3. assignment ratio and eligibility are correct;
4. exposure logging is valid;
5. instrumentation definitions stayed stable;
6. control/treatment differ only in intended ways where feasible;
7. sample-ratio mismatch is investigated;
8. novelty/seasonality/release overlap is considered;
9. repeated peeking/stopping policy is controlled;
10. multiplicity from many metrics/variants is acknowledged;
11. primary outcome and guardrails are both reviewed;
12. effect is practically meaningful;
13. result is scoped to the tested population/time/version.

High-risk security/privacy/accessibility changes are not made acceptable merely because conversion improves.

## 9. When not to A/B test
Do not default to experimentation when:
- correctness has a known defect;
- accessibility/security/privacy requirement already determines the fix;
- traffic is too low for useful discrimination and qualitative evidence is more efficient;
- treatment creates unacceptable irreversible risk;
- randomization is infeasible or contamination dominates;
- the question is descriptive/diagnostic rather than causal.

For niche apps such as MintTap/LogMate, low traffic can make careful task observation, support/search evidence, release cohorts and deterministic quality tests more useful than endless underpowered experiments.

## 10. Pre-launch measurement plan
A website should launch with a measurement contract, not “analytics installed.”

### Layer 1 — Decisions
For each page family define likely decisions:
- Company: can visitors understand publisher identity and reach product/support surfaces?
- Product: can qualified visitors understand value/evidence and reach the correct store?
- Support: can users find and complete a support task without avoidable escalation?
- Governance: can users locate privacy/account-deletion/legal information?
- PWA: can supported users understand install/offline/update/sync state without telemetry becoming correctness infrastructure?

These are generic page-family contracts, not claims about current `minttap.app` routes.

### Layer 2 — Minimal evidence
For each decision define:
- outcome;
- diagnostics;
- guardrails;
- eligibility/denominator;
- context dimensions that change decisions;
- qualitative companion evidence.

### Layer 3 — Event contracts
Specify exact event semantics, parameters, privacy purpose, retention, schema version, duplicate/late behavior and QA before code implementation.

### Layer 4 — Validation
Pre-production:
- static/schema review;
- browser trigger verification;
- network/delivery verification where permitted;
- consent-state matrix;
- locale/route/browser matrix;
- offline/reconnect matrix for PWA telemetry;
- accessibility/performance impact;
- report reconciliation.

Post-launch:
- freshness/volume anomaly monitoring;
- release annotations;
- data-quality/modeling/sampling checks;
- periodic registry audit;
- removal of unused telemetry.

## 11. Analytics Evidence Registry — extended fields
075 established the registry. Add:
- eligible population/denominator;
- expected missingness classes;
- occurrence-time vs ingestion-time policy;
- duplicate/replay policy;
- observed vs modeled/sampled/thresholded state;
- identity/session scope;
- independent reconciliation source;
- practical decision threshold;
- active incident/degradation status.

This turns instrumentation governance into measurement lineage.

## 12. PWA transfer validation
Scenario: standalone PWA appears to have lower `sync_acknowledged` rate than browser mode.

Invalid conclusion: “installed PWA sync is less reliable.”

Required diagnostic chain:
1. verify same product acknowledgement semantics/version;
2. compare eligible populations and offline duration;
3. distinguish actual product acknowledgement from telemetry delivery;
4. inspect occurrence vs ingestion time;
5. check browser/display-mode/OS version mix;
6. check missing consent/blocking/telemetry availability;
7. use product sync correctness evidence from Engineering;
8. only then form a bounded reliability hypothesis.

**TRANSFER VALIDATION:** 073–074 product-state semantics prevent analytics from becoming source of truth.

**DEPENDENCY — Software Engineering:** production event emission, durable queue/retry implementation, identifiers, sync correctness logs and target-device evidence belong to implementation validation. Software Engineering Studio currently remains Foundation IN STUDY and explicitly separates source-of-truth/durability and validation evidence; Web Manager should hand over measurement contracts, not prescribe implementation architecture without evidence.

## 13. Cross-track transfers
### A — Platform/Browser
Own lifecycle/session/storage/offline mechanics used to interpret event delivery and identity discontinuity.

### B — UX/IA/Content
Own task/eligibility semantics. Funnel evidence can identify a transition needing investigation but cannot invent user motive.

### C — Performance/Accessibility/Quality
Own guardrails and instrumentation runtime validation. Telemetry itself is a third-party/runtime cost when applicable.

### E — Architecture/Security/Operations
Own consent/data-flow/retention/processor/incident boundaries. Measurement degradation should be observable as an operational condition.

### Design Studio
Analytics may identify candidate comprehension/interaction failures. Design Studio remains owner of reusable design/interaction diagnosis; current Web evidence is not equivalent to human/cross-browser/AT production validation.

### Marketing
Receives search/acquisition/outbound evidence plus attribution/missingness boundaries; does not receive a fabricated “true channel” from partial web data.

## 14. Diagnostic competency exercises
### A — Conversion drops after release
Check release/instrumentation version, eligible denominator, traffic mix, data freshness/quality, runtime errors, store-link correctness and independent evidence before UX redesign.

### B — GA report and raw/business count disagree
Determine scope, identity, time zone, late data, sampling/thresholding/modeling, filters, event definition and duplicate policy. Do not average the disagreement away.

### C — A/B treatment +4% CTA, support errors +15%
Do not declare a winner from the primary metric alone. Validate assignment/exposure, uncertainty and practical magnitude, then apply pre-defined guardrails and investigate mechanism.

### D — Search traffic rises, app installs unchanged
Search exposure, web visits, store handoff and store acquisition are different measurement systems. Locate the first evidence-supported transition before attributing cause.

### E — Offline PWA telemetry arrives two days later
Use occurrence time and vendor constraints; do not rewrite product chronology from ingestion order. If the vendor cannot accept/process the delay reliably, record measurement missingness rather than altering product sync behavior.

## 15. Stage 9 competency gate
Roadmap exit requirements:
1. **Define a measurement plan before launch** — PASS: decision/page-family → outcome/diagnostic/guardrail → minimal event contracts → privacy → QA/operations.
2. **Distinguish signal from noise** — PASS: semantics, denominator, missingness, data-quality states, segmentation, practical vs statistical significance, alternative explanations.
3. **Recommend changes with explicit evidence chain** — PASS: observation → uncertainty/alternatives → causal design where required → guardrails → risk-weighted decision → re-observation.

Additional demonstrated capability:
- diagnose modeled/sampled/thresholded/late/duplicate data boundaries;
- separate attribution from causal history;
- specify randomization/blocking/validity requirements without overclaiming;
- preserve PWA product-state truth;
- hand implementation/design/marketing questions to their canonical owners.

**Result: STAGE 9 PASS — FOUNDATION/PRACTITIONER.**

This is transferable competence, not production validation of `minttap.app`.

## 16. Production OPEN register
Still unknown:
- actual `minttap.app` analytics vendor/property/tagging;
- consent mode/CMP/legal basis and jurisdictions;
- event schema/metric definitions;
- route/page-family inventory and denominators;
- web→store attribution implementation;
- traffic volumes/data-quality behavior;
- raw export/warehouse/reconciliation capability;
- experiment assignment infrastructure;
- PWA telemetry/runtime behavior;
- actual user/support/search baselines.

No production recommendation may pretend these facts are known.

## 17. Next major target
With Stages 1–9 complete at foundation/practitioner level, the next vertical gap is **Stage 10 — App-Company Web Strategy & Growth**. Integrate company/product/support/governance surfaces, one-app→multi-app architecture, launch lifecycle, store↔web continuity, deep linking, release/status/support, international growth and product retirement. PWA remains an elevated cross-track specialization and should be used where it materially affects app-company strategy, without duplicating Marketing ownership.