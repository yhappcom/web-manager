# 148 — PWA Assurance Coverage SLOs, Lag/Gap Severity & Consequence-Based Escalation

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + CONSEQUENCE-POLICY VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 143–147; Track A runtime/SW/device observability; Track B degraded-state UX; Track C fault-injection and release evidence; Track D monitoring-health telemetry.

## Why this study exists

147 established honest monitoring-coverage provenance: source retention, source order/coverage, local ingestion, local processing and current-state observation are separate claims, and a retention/outage gap must remain explicit when history cannot be reconstructed. The next operational question is harder: **what should the product do when coverage is late, gapped or unobservable?**

A universal timeout such as “older than 15 minutes = block everything” is attractive but unsound. Different dependencies change at different rates and carry different consequences. An analytics feed can be stale without making a security-sensitive remote mutation unsafe; uncertainty about a trust-root/recovery-authority transition can be a direct authorization problem. Conversely, “monitoring is degraded” must not automatically become a global outage.

The goal is a small-company-compatible model that connects monitoring quality to consequence-bearing decisions without inventing production thresholds before actual topology, threat, safety, legal and product requirements are known.

## SOURCE

### Monitoring frequency is risk- and volatility-dependent, not universal
NIST SP 800-137 §3.2.2 says organizations determine monitoring/assessment frequencies for individual metrics and controls. Relevant considerations include control volatility and how monitoring information is used. The publication's purpose is ongoing visibility and timely risk response aligned with organizational risk tolerance.

Source: https://doi.org/10.6028/NIST.SP.800-137

### Continuous monitoring supports risk decisions
NIST's current RMF Monitor guidance states that monitoring maintains ongoing situational awareness of system/organization security and privacy posture, with monitoring output analyzed and responded to. CSF 2.0 likewise provides outcomes for understanding, assessing, prioritizing and communicating cybersecurity risk rather than prescribing one implementation threshold.

Sources:
- https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step
- https://doi.org/10.6028/NIST.CSWP.29

### Risk response should reflect mission/consequence, not alert arrival order
NIST SP 800-61 Rev. 3 (final April 2025) integrates incident response with CSF 2.0 risk management. It supersedes Rev. 2; older Rev. 2 prioritization material is useful historical context but is not the current normative source. CISA's incident-management resource guidance also describes event priority as informing impact, response timeframe, response type and escalation.

Sources:
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://www.cisa.gov/sites/default/files/c3vp/crr_resources_guides/CRR_Resource_Guide-IM.pdf

### Small organizations still benefit from high-risk alerting without enterprise ceremony
CISA's small/medium-business logging guidance recommends selecting useful logs, centralizing where practical, monitoring regularly and setting alerts for high-risk events. This is transfer evidence that a small company can use consequence-focused monitoring without building a large SOC.

Source: https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/use-logging-on-business-systems

## SYNTHESIS — separate objectives that are often collapsed

Do not use one number called “monitoring SLO.” Separate at least:

1. **OBSERVATION LAG OBJECTIVE** — how stale the newest defensible observation may become for a dependency/claim.
2. **INGESTION/PROCESSING LAG OBJECTIVE** — how long authenticated source information may remain unapplied locally.
3. **COVERAGE CONTINUITY OBJECTIVE** — whether the relevant interval must be proven contiguous, merely observed, or may tolerate bounded gaps.
4. **GAP RECOVERY OBJECTIVE** — how quickly a known gap must be replayed, reconciled or escalated.
5. **UNOBSERVABILITY TOLERANCE** — how long/under what circumstances a dependency may remain unverifiable before authority is reduced.
6. **DECISION FRESHNESS REQUIREMENT** — maximum evidence age/coverage class acceptable for a particular consequence-bearing action.

Persistent guards:
- `monitoring SLO met ≠ dependency safe`;
- `monitoring SLO missed ≠ incident proven`;
- `lag low ≠ coverage complete`;
- `coverage contiguous ≠ observation fresh`;
- `current state fresh ≠ gap history reconstructed`;
- `telemetry delayed ≠ product unavailable`;
- `security evidence stale ≠ local data must be deleted`;
- `one timeout ≠ one risk class`;
- `high alert severity ≠ high business consequence in every context`;
- `analytics freshness ≠ authorization freshness`.

## Consequence classes before time thresholds

A future implementation should first classify **what decision depends on the evidence**, then choose lag/gap objectives. Generic classes:

### Class 0 — Diagnostic / non-authoritative
Examples: dashboards, aggregate usage analytics, non-security trend reporting.

Coverage degradation normally affects confidence/diagnostics, not product authority. Mark telemetry degraded; do not block unrelated product operations.

### Class 1 — Operational quality
Examples: rollout-health evidence, cache/update convergence observations, non-authoritative runtime-quality monitoring.

Degradation can pause rollout expansion or require manual review, while already-safe local use may continue.

### Class 2 — Security/recovery supporting evidence
Examples: dependency inventory, recovery-readiness observations, provider configuration evidence that supports but does not alone authorize a sensitive action.

Staleness/gaps can require revalidation or an independent observation before release/recovery progression.

### Class 3 — Authority-critical evidence
Examples: current trust root/policy epoch, recovery-authority/revocation state, compromise containment state, evidence required to authorize remote mutation after long offline operation.

Unknown or materially stale state can be a **fail-closed authority condition** for the affected capability. It is not necessarily a whole-app outage: preserve local read/export/data where product semantics permit.

These are generic reasoning classes, not final MintTap/LogMate labels. Actual mapping remains OPEN.

## Severity is multidimensional

Do not derive escalation from lag duration alone. Evaluate:

`severity = f(consequence, evidence role, coverage state, lag, gap recoverability, dependency volatility, independent observation, blast radius, active threat/incident context, reversibility)`

This is a reasoning model, not a formula to implement literally.

A short gap in authority-critical compromise/revocation evidence can matter more than a long delay in analytics. A long gap in a stable low-consequence dependency can remain degraded rather than blocked if independent current-state evidence is sufficient for the intended decision.

### Coverage states from 147 mapped to operational meaning

- **PROVEN-CONTIGUOUS + fresh enough for decision** → no coverage-based restriction.
- **OBSERVED-NONCONTIGUOUS** → usable only for decisions whose assurance requirement does not require completeness.
- **GAP-KNOWN** → apply consequence-specific gating; current-state reconciliation does not erase the gap.
- **CURRENT-STATE-RECOVERED / HISTORY-GAPPED** → may restore decisions requiring only current state; must not restore decisions whose safety depends on absence/knowledge of intermediate transitions.
- **RECONSTRUCTED-BOUNDED** → authorize only within the reconstructed claim/scope.
- **UNOBSERVABLE** → authority-critical decisions remain blocked or require an explicitly independent approved path.

`current state recovered ≠ every decision may resume`.

## Escalation ladder — capability-scoped, not global

A small organization can use a compact ladder:

1. **NORMAL** — objective satisfied for the decision scope.
2. **DEGRADED / VISIBLE** — lag/gap exists but does not yet invalidate the intended decision; expose internally and preserve provenance.
3. **REVALIDATION REQUIRED** — automated evidence is insufficient; obtain current/independent evidence before a consequence-bearing transition.
4. **CAPABILITY GATED** — block the affected release/recovery/remote-mutation capability while preserving unrelated safe functions.
5. **INCIDENT / BREAK-GLASS GOVERNANCE** — evidence loss is correlated with compromise, contradictory authority state, or another incident criterion; use the established bounded emergency lifecycle rather than silently widening permissions.

Escalation must be reversible only through evidence that satisfies the affected decision's requirement. “Alert acknowledged” is not evidence restoration.

`operator saw alert ≠ assurance restored`.
`manual override ≠ uncertainty resolved`.

## Time budgets: no invented MintTap numbers

SP 800-137 supports differentiated monitoring frequencies based on volatility/risk. Therefore this study does **not** set 5-minute, 1-hour, 24-hour or other production thresholds.

At implementation time, each consequential dependency/claim should record:
- decision/capability protected;
- consequence if stale/incorrect;
- expected volatility/change mechanism;
- source retention/replay window;
- normal observation and processing latency;
- independent observation availability;
- acceptable evidence/coverage state for each action;
- warning threshold and hard-gate condition where justified;
- owner and escalation path;
- test evidence and change invalidators.

Thresholds should fit inside source retention/replay constraints when catch-up is required. An SLO that permits more lag than the provider's recoverable history without explicitly accepting a gap is internally inconsistent.

## Error budgets are not authorization budgets

SRE-style error-budget language can help operationally track monitoring reliability, but **unused budget must not be treated as permission to ignore an authority-critical gap**. Ten harmless analytics delays do not offset one unknown recovery-authority transition.

Useful distinction:
- aggregate reliability budget → service/monitoring engineering planning;
- per-decision evidence requirement → authorization/security gate.

`monthly availability target met ≠ this sensitive decision has current evidence`.

## PWA / EFB application

For a long-offline company iPad, distinguish at least four clocks/scopes:

1. server/provider security-state observation lag;
2. served release/Service Worker publication state;
3. actual device Service Worker/runtime activation state;
4. local operation/data lineage and last successful trust/sync reconciliation.

Do not compare them as if they were one global freshness timestamp.

Example generic reasoning:
- stale analytics → no reason to block offline flight-record entry;
- uncertain rollout telemetry → may pause rollout expansion, not erase local records;
- unknown current trust/revocation state after a long offline interval → preserve local records/read/export, but remote mutation/sync authority may remain gated until current authority evidence is re-established;
- server monitoring is healthy → still does not prove a physical iPad activated the current Service Worker.

`server monitoring green ≠ device trust current`.
`device runtime stale ≠ server monitoring failed`.

Actual EFB safety, aviation, company-MDM and operational requirements remain outside this generic PASS until verified.

## Cross-track transfer

### Track A — Platform & Browser
Own exact browser/Service Worker/storage/device observation semantics. Supply which runtime facts can be observed and with what lifecycle limitations; do not invent server security consequence policy.

### Track B — UX / IA
Own truthful degraded-state communication requirements. “Offline,” “sync paused,” “verification required,” and “service unavailable” are not interchangeable. User messaging must describe capability state without claiming security facts the evidence does not support.

### Track C — Performance / Accessibility / Quality
Own lag/gap fault injection, boundary testing and provenance. Validate warning→revalidation→gate→recovery transitions, including accessibility of critical degraded-state messaging. Do not reduce PASS to alert firing.

### Track D — Search / Discovery / Analytics
Own diagnostic monitoring-health metrics and measurement continuity. Analytics may report lag/gap/denominator health but is not an authorization oracle.

### Track E — Owner
Own consequence classification, decision freshness requirements, coverage-state policy, escalation/gating, exception/break-glass linkage and operational review.

## MINTTAP DECISION — minimal sufficient policy model

Do not build a large SRE/SOC platform for a small app company. If implementation requires this capability, preserve the minimum structure:

1. identify consequence-bearing decisions/capabilities;
2. map each to required dependency/evidence scope;
3. record acceptable coverage state and freshness requirement;
4. monitor source/processing lag and known gaps separately;
5. make escalation capability-scoped;
6. distinguish warning, revalidation and hard gate;
7. keep authority-critical unknowns from being averaged away by healthy low-risk telemetry;
8. preserve local irreplaceable data during remote-authority gating;
9. test recovery from lag/gap and verify gates actually clear only on sufficient evidence;
10. revisit policy when dependency volatility, provider retention, product consequence or platform behavior changes.

No production threshold or actual MintTap/LogMate consequence mapping is asserted here.

## VALIDATION — 32-case campaign

1. analytics lag exceeds warning threshold and does not block unrelated product use; 2. authority-critical observation becomes stale and affected remote mutation gates; 3. low lag with known source gap does not render continuous green; 4. contiguous history with stale current observation triggers freshness action; 5. current-state reconciliation closes a decision requiring only current state; 6. same reconciliation does not close a decision requiring transition history; 7. source retention window is shorter than configured catch-up tolerance and policy validation rejects configuration; 8. ingestion healthy but processing backlog grows; 9. source healthy but local collector unavailable; 10. local monitoring healthy while source itself is unobservable; 11. warning threshold crossed then self-recovers with provenance; 12. hard gate clears only after sufficient evidence; 13. alert acknowledgement alone cannot clear gate; 14. manual override enters bounded exception/break-glass path; 15. exception expires while evidence remains stale; 16. two low-risk degraded feeds do not automatically equal one critical failure; 17. correlated loss of two authority-critical observers escalates more strongly than one; 18. independent current observation reduces uncertainty only for claims it actually supports; 19. active compromise context tightens escalation for affected evidence; 20. normal operation does not borrow unused aggregate error budget to accept critical uncertainty; 21. rollback/revocation state unknown after long offline interval gates remote authority but preserves local data; 22. server monitoring green does not mark physical iPad SW current; 23. physical iPad stale does not falsely mark provider monitoring failed; 24. rollout-health evidence stale pauses expansion without forcing rollback absent other evidence; 25. provider cursor reset creates coverage classification before SLO evaluation; 26. backup restore rolls monitoring state backward and does not inherit old green status; 27. monitoring clock skew does not silently extend authorization freshness; 28. accessibility test verifies critical gated-state status and recovery action are perceivable/operable; 29. dashboard aggregation cannot hide one Class-3 UNKNOWN behind many Class-0 greens; 30. policy generation change invalidates obsolete thresholds/mappings; 31. source semantics change triggers CHANGE WATCH/revalidation; 32. end-to-end long outage → retention gap → current-state recovery → consequence-specific revalidation/gating leaves no false global green or unnecessary global outage.

## CONTRADICTION / failure-mode analysis

### Universal-timeout theater
One threshold is easy to operate but conflates low-consequence telemetry with authority-critical evidence and ignores volatility/retention.

### Alert-severity theater
A vendor's “critical” alert label is not automatically the product's consequence classification. Product decisions need their own mapping.

### Fail-open availability theater
Keeping every operation available during authority uncertainty can turn monitoring failure into an authorization bypass.

### Fail-closed-everything theater
Blocking the entire PWA for any telemetry gap harms availability and can endanger irreplaceable offline data workflows without improving the affected trust decision.

### Error-budget theater
Aggregate monthly reliability can look healthy while the single evidence stream required for a sensitive decision is stale exactly when needed.

### Dashboard-green theater
A green monitoring service says its pipeline is healthy; it does not by itself prove upstream completeness, device convergence or security-state correctness.

## OPEN

Actual MintTap/LogMate consequence classes, protected operations, source/provider topology, normal lag distributions, retention/replay windows, incident criteria, safety/legal requirements, release process, MDM/WebKit observability, offline-edit semantics, remote-mutation boundaries, staffing/on-call model and acceptable thresholds are unknown. No production SLO, blocking rule or EFB safety conclusion is claimed.

## CHANGE WATCH

- Provider retention/cursor/replay guarantees can change and directly constrain feasible gap-recovery objectives.
- Browser/WebKit/MDM observation capabilities remain version/platform dependent.
- NIST SP 800-137 remains the current final ISCM publication found in this review; its principles are durable, but implementation should re-check for revisions.
- NIST SP 800-61 Rev. 3 is the current final incident-response publication as of this study; older Rev. 2 prioritization details should not be cited as current normative guidance.
- CISA operational guidance is useful transfer evidence, not a MintTap-specific SLO prescription.

## Gate result

**PASS (generic).** The Web Manager can now distinguish lag, continuity, recoverability, unobservability and decision freshness; derive escalation from consequence/evidence role rather than a universal timeout; preserve capability-scoped fail-closed behavior without turning every telemetry defect into a whole-app outage; and keep aggregate monitoring reliability separate from per-decision authorization evidence.

Production/provider/managed-EFB SLOs and thresholds remain **OPEN**.

## Next highest-value adjacent question

**PWA assurance policy composition, conflicting gates & degraded-mode deadlock avoidance.** Once multiple evidence streams can independently gate release, recovery and remote mutation, the next bottleneck is composition: avoid a weaker policy accidentally overriding a stronger gate, detect contradictory prerequisites, prevent circular revalidation dependencies, and provide a bounded recovery path when two individually reasonable gates would otherwise deadlock the system.