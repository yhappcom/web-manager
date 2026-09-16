# 075 — Stage 9 Analytics, Measurement & Experimentation Evidence Foundations

Date: 2026-09-16
State: **PASS — FOUNDATION/PRACTITIONER INTEGRATED CHECKPOINT**
Primary owner: **Track D — Search, Discovery & Analytics**
Consumers: B task semantics; C quality guardrails; E privacy/operations; A browser lifecycle/PWA delivery.

## Purpose
Build an evidence system for improving an app-company website without confusing telemetry with product truth, correlation with causation, attribution with historical fact, or an experiment result with universal truth. PWA install/offline/synchronization is used as a major application case because 073–074 established durable product-state semantics that analytics must observe rather than redefine.

## Source basis / CHANGE WATCH
Current authoritative material rechecked 2026-09-16:
- Google Analytics Help / Developer documentation: events and event parameters; parameters add contextual data to interactions and feed report dimensions/metrics. GA attribution has user-, session- and event-scoped traffic dimensions; event-scoped key-event attribution depends on the selected attribution model.
- W3C Privacy Principles: measurement should avoid unnecessary personal data; aggregation can satisfy measurement use cases while obscuring individual contribution.
- W3C Web Performance Working Group: Navigation/Resource/User/Event Timing and related APIs are separate observation surfaces; User Timing can instrument application-specific milestones but exposes timing information to scripts on the same page.

Vendor report names/defaults and browser measurement capabilities are **CHANGE WATCH**. The durable concepts below do not depend on GA4 specifically.

## 1. First-principles measurement chain

`decision to make → user/business question → task/state semantics → observable evidence → privacy/minimization gate → event/metric contract → delivery/quality checks → aggregation/segment → interpretation → alternative explanations → decision threshold → intervention → re-observation`

**SYNTHESIS:** telemetry is useful only when it is connected to a decision and has known semantics. Logging everything first and deciding later creates privacy cost, ambiguous metrics and instrumentation debt.

Critical separations:
- product state ≠ analytics event;
- event occurrence ≠ unique user;
- event count ≠ successful task;
- funnel drop-off ≠ proven UX cause;
- correlation ≠ causal effect;
- attribution model ≠ historical ground truth;
- dashboard change ≠ product change;
- statistically detectable ≠ practically valuable;
- experiment win ≠ permission to ignore accessibility/security/performance guardrails.

## 2. Metric architecture: outcome, diagnostic and guardrail
A useful measurement plan begins with a decision, then separates:
1. **Outcome metric** — evidence closest to the desired task/business result.
2. **Diagnostic metrics** — help explain where/why the outcome moved.
3. **Guardrails** — must not materially regress while optimizing the outcome (accessibility, reliability, privacy, performance, support burden, error/conflict rate, etc.).
4. **Context dimensions** — page family, locale, acquisition surface, browser/display mode, app/site version, network/offline state when justified and privacy-safe.

Avoid composite scores that hide trade-offs unless their construction and interpretation are explicit.

## 3. Event semantics and instrumentation contract
Before implementation, each material event should have a contract:
- decision/question served;
- event name and semantic definition;
- exact trigger boundary;
- success/failure/state meaning;
- allowed parameters and cardinality;
- source surface/version;
- whether duplicate delivery is possible and how analysis treats it;
- offline queue behavior if any;
- privacy purpose, minimization and retention owner;
- validation method;
- known blind spots.

**SOURCE:** GA events can carry event parameters that provide context and later populate dimensions/metrics. This is a vendor implementation of a broader event+context model, not the definition of the product state itself.

### Example: Store CTA
Bad: `button_click`.
Better semantic layers, only if justified:
- `store_cta_exposed` — CTA genuinely eligible/visible under a defined rule;
- `store_cta_activated` — user activation occurred;
- outbound handoff evidence — browser/navigation evidence if observable;
- actual store install — **not inferable from web click alone** unless a separate supported attribution system establishes it.

## 4. Funnels are state models, not just charts
A funnel must specify eligibility and denominator. Example:
`qualified product-page entry → meaningful product proof exposure → store CTA activation → observable outbound handoff`

A visitor who never had an eligible CTA should not automatically be counted as the same failure state as a visitor who saw it and declined it.

Funnels may be ordered, unordered, session-bounded or cross-session; the chosen model changes the answer. Document it.

**CONTRADICTION:** “60% drop at step X means step X caused the problem” is invalid. The chart locates an observed transition; causal diagnosis requires additional evidence.

## 5. Segmentation and cohorts
Segment only on dimensions that can change a decision. Useful classes can include page family, locale, acquisition source class, browser/platform, new/returning, release/version, and PWA display mode where reliably observable.

Cohorts answer longitudinal questions for a defined entry condition/time rather than mixing all users. Examples: users first arriving during a release period; users whose first observed qualified visit used a given locale.

Risks:
- tiny cells create noise and privacy risk;
- post-treatment segmentation can bias experiment interpretation;
- high-cardinality IDs/URLs can leak data and make reports unusable;
- Simpson's paradox can make aggregate and segment trends disagree.

## 6. Attribution boundaries
**SOURCE:** Google Analytics distinguishes user-, session- and event-scoped traffic-source dimensions; event-scoped key-event credit depends on the selected attribution model.

**SYNTHESIS:** attribution is a model for assigning credit under observable data and rules, not a replay of a person's private causal journey.

Therefore:
- do not call last-click/data-driven/model output “the true source”;
- keep web search evidence, App Store/Play acquisition evidence and web analytics as distinct observation systems;
- campaign parameters can support channel analysis but cannot prove why a person chose the app;
- privacy controls, browser restrictions, cross-device transitions and unobserved offline activity create missingness.

Marketing owns channel strategy; Track D owns measurement mechanics and evidence limits.

## 7. Privacy-aware analytics
Stage 8 transfers directly:
`purpose → minimum evidence → collection → processing/sharing → retention → deletion/withdrawal implications → user communication`

**SOURCE:** W3C Privacy Principles explicitly note that measurement often can use aggregation so an individual's contribution is obscured.

Rules:
- do not collect personal data merely because a tool can;
- avoid raw free-text/search/support payloads unless a justified purpose and handling model exists;
- prefer coarse categories over identifiers where the decision permits;
- avoid sensitive or unnecessary event parameters;
- document third-party processor/transfer implications before deployment;
- analytics absence due to consent/blocking/offline must not break the product.

`secure telemetry ≠ justified telemetry` and `consented telemetry ≠ unlimited telemetry`.

## 8. PWA measurement state machine
073–074 established product truth. Analytics may observe these states but must not own them:
`browser visit → install/Home-Screen opportunity (if observable) → standalone launch → local task → local durable save → queued sync → transport attempt → remote acknowledgement → reconciliation/conflict`

Critical rules:
- `local_save` must be emitted only after the actual local transaction boundary succeeds, if such telemetry is justified;
- `sync_queued` is not `sync_success`;
- transport attempt is not acknowledgement;
- acknowledgement is not independent backup;
- analytics delivery failure must never roll back or block a product transaction;
- analytics retry duplicates must not be confused with product outbox retries;
- offline telemetry may arrive later and out of wall-clock ingestion order; preserve event occurrence time/version where justified;
- if analytics is unavailable, synchronization correctness remains unchanged.

### Install measurement boundary
Do not assume every platform exposes the same install prompt/install-complete event. Safari/iOS/iPadOS and Chromium install models differ and are CHANGE WATCH. Measure only events actually supported/validated on the target platform. Standalone/display-mode observation is not automatically proof of a newly completed installation.

## 9. Performance and analytics interaction
Track C owns runtime quality. Analytics scripts are themselves runtime dependencies and third-party/privacy costs. Measurement should not materially degrade the task it measures.

W3C Performance/User Timing provides browser/application timing observations, but those timings are not business events by themselves. Join them only when the question warrants it.

Possible analysis chain:
`qualified task population → performance context → task outcome`
not:
`LCP improved → conversion was caused to improve` without causal evidence.

## 10. Qualitative + quantitative evidence
Quantitative evidence answers how often/where a pattern is observed. Qualitative evidence can explain comprehension, expectation, failure mechanism and user language.

Use together:
- analytics/search/support data identifies candidate problems;
- usability observation/support evidence identifies mechanisms;
- controlled experiments can test bounded causal changes where appropriate;
- accessibility/performance/security evidence supplies non-negotiable guardrails.

Do not manufacture user motives from telemetry.

## 11. Experimentation foundations
A valid experiment begins before exposure:
1. decision/problem statement;
2. hypothesis and causal mechanism;
3. treatment/control definition;
4. randomization unit;
5. primary outcome and guardrails;
6. eligibility/population;
7. exposure logging contract;
8. sample-size/power or decision rule appropriate to method;
9. stopping rule/duration;
10. analysis plan, segmentation policy and failure criteria.

Major failure modes:
- peeking/stopping when significance appears;
- testing many metrics/variants then reporting only favorable ones;
- sample-ratio mismatch or broken assignment;
- contamination between control/treatment;
- novelty/seasonality/release confounding;
- changing instrumentation mid-test;
- interpreting non-significance as proof of equality;
- treating statistical significance as practical importance;
- optimizing a local conversion while degrading trust/accessibility/performance/support outcomes.

**SYNTHESIS:** an A/B test is a causal instrument under assumptions, not a general truth machine.

## 12. Decision thresholds and evidence confidence
Every recommendation should state:
- observed effect/pattern;
- population/time window/version;
- uncertainty/missingness;
- plausible alternatives;
- guardrail status;
- reversibility/risk of intervention;
- what evidence would change the decision.

Use lower evidence thresholds for cheap/reversible changes and higher thresholds for irreversible, privacy-sensitive, security-sensitive or high-cost changes. This is risk-weighted judgment, not a universal numeric rule.

## 13. Instrumentation governance
Maintain an **Analytics Evidence Registry**:
- metric/event owner;
- decision served;
- semantic contract/version;
- collection surfaces;
- parameters/cardinality;
- privacy/retention basis;
- release introduced/changed/removed;
- QA status;
- known missingness/duplication;
- downstream reports/experiments;
- deprecation date.

Schema/version changes should be release-managed. Never silently redefine a metric while comparing pre/post periods.

Validation layers:
1. static/schema validation;
2. controlled browser/app event trigger test;
3. network/delivery inspection where permitted;
4. vendor debug/realtime observation where applicable;
5. warehouse/report reconciliation if available;
6. production anomaly monitoring.

## 14. Diagnostic exercises
### A. Product-page CTA falls 20%
Do not redesign immediately. Check denominator/eligibility, instrumentation version, traffic/locale/device mix, page/runtime changes, store-link correctness and data missingness. Then obtain qualitative or controlled evidence for the suspected mechanism.

### B. PWA shows fewer sync-success events
First distinguish product acknowledgements from analytics delivery. Inspect product sync correctness logs/state, offline duration/version/platform mix and telemetry queue behavior. Never infer lost flight records from analytics alone.

### C. Campaign traffic converts poorly
Attribution identifies an observed acquisition classification, not motive. Compare landing/task fit and eligible population, then hand channel-message questions to Marketing with evidence boundaries.

### D. Experiment improves CTA activation but increases support errors
Outcome improvement does not automatically win. Guardrails are part of the decision contract; investigate the mechanism and practical trade-off.

## 15. Cross-track transfers
### Track B
Owns task/state semantics and eligibility definitions. Analytics must not invent user-task meaning from DOM clicks. B consumes funnel evidence to identify where deeper UX/content investigation is warranted.

### Track C
Owns performance/accessibility/quality guardrails and validates telemetry runtime cost. Automated conversion gains do not override accessibility correctness or field-quality regressions.

### Track A
Owns browser lifecycle, storage/offline and PWA mechanics. D consumes lifecycle evidence when defining session/visit/display-mode/offline event semantics.

### Track E
Owns privacy/security/operations. D must hand over data flows, processors, retention, consent/storage and telemetry failure/incident implications.

### Marketing
Receives web/search/acquisition observations with attribution limitations. Marketing strategy is not duplicated here.

### Design Studio
If analytics identifies a candidate comprehension/navigation problem, provide the observed population/task transition and uncertainty, not a prescriptive visual fix. Human/UX validation remains separate.

## 16. MintTap / project facts still OPEN
Do not infer:
- whether `minttap.app` currently has any analytics tag/property;
- vendor/property IDs, consent configuration or retention;
- production event schema/funnels;
- web→App Store/Play attribution setup;
- actual traffic/populations/conversion baselines;
- PWA install/display-mode/offline telemetry;
- actual LogMate/EFB PWA implementation;
- warehouse/export/experiment platform;
- legal basis/consent requirements for actual jurisdictions/data flows.

These require runtime/project evidence and, where appropriate, legal/privacy specialist review.

## 17. Competency gate
PASS at foundation/practitioner if Web Manager can:
1. map a decision to task semantics, outcomes, diagnostics and guardrails;
2. specify event trigger/parameter/privacy/quality contracts before implementation;
3. diagnose funnel changes without causal overclaim;
4. distinguish attribution model output from causal truth;
5. integrate privacy/minimization and instrumentation governance;
6. preserve PWA product-state truth under offline/delayed/duplicate telemetry;
7. combine quantitative, qualitative and experiment evidence appropriately;
8. identify experiment validity failures and guardrails;
9. make risk-weighted recommendations with explicit uncertainty;
10. hand evidence to Marketing/Design/Engineering without duplicating their disciplines.

**Result: PASS — FOUNDATION/PRACTITIONER integrated checkpoint.**

## Next adjacent work
Stage 9 is not yet closed. Highest-value next block should deepen **causal inference/experimentation validity, measurement reliability, attribution/missingness, and pre-launch measurement planning**, then perform a Stage 9 integration gate. PWA remains a cross-track application case; target-device/runtime validation stays OPEN.