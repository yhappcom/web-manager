# 120 — PWA Post-Incident Learning → Permanent Control-Baseline Change Governance

Status: **PASS (generic) / PRODUCT RUNTIME + ORGANIZATIONAL CHANGE-OWNER VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 113–119 incident/recovery chain; Track A browser/PWA mechanics; Track C recurrence validation; Software Engineering for implementation/ADR/change evidence.

## Purpose

119 separated normalized state, accepted residual risk, open work and unknown state. The adjacent problem is what to do with incident lessons after normalization: which lessons should become durable architecture/security requirements, how to preserve superseded assumptions without blindly restoring them, how to avoid overfitting one incident, and what evidence is required before a corrective action can be called effective.

This is generic governance. It does not claim MintTap or LogMate currently implements the controls described here.

## 1. Five-track balance

- **A Platform/Browser:** supplies causal mechanics. A browser/PWA behavior should become a permanent requirement only when the causal boundary is understood and remains relevant to supported runtimes.
- **B UX/IA/Content:** consumes permanent restricted/recovery/re-entry states. Incident-specific warnings must not become permanent friction without an enduring user-risk rationale.
- **C Quality:** owns recurrence oracles, negative controls, regression suites and evidence that a corrective action blocks the causal failure path without unacceptable regressions.
- **D Search/Analytics:** supplies monitoring evidence and recurrence signals but cannot prove prevention from silence alone.
- **E Architecture/Security/Operations:** highest-risk owner. Owns lesson classification, durable control promotion, supersession, change governance and closure evidence.

E remains the bottleneck. A supplies causality; C supplies proof.

## 2. SOURCE — incident lessons feed continuous improvement

NIST SP 800-61 Rev.3 (April 2025) integrates incident response into cybersecurity risk management. NIST's current Incident Response project explicitly shows lessons learned from activities across the CSF Functions feeding the **Improvement** category, where lessons are analyzed, prioritized and used to inform all Functions.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://csrc.nist.gov/projects/incident-response
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

**SYNTHESIS:** the output of an incident is not merely a postmortem document. Useful lessons must enter ordinary risk, architecture, engineering, validation and operational governance.

Guards:
- `lesson documented ≠ lesson institutionalized`;
- `incident closed ≠ corrective-action lifecycle closed`;
- `postmortem complete ≠ recurrence risk reduced`.

## 3. SOURCE — root cause should change the development/control system when appropriate

NIST SSDF 1.1 (SP 800-218, February 2022) is the current final SSDF. Its purpose includes addressing root causes of vulnerabilities to prevent future recurrence. The earlier SSDF task formulation explicitly describes reviewing the SDLC and updating it as appropriate to prevent or reduce recurrence of a root cause.

Sources:
- https://csrc.nist.gov/pubs/sp/800/218/final
- https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04232020.pdf (historical task detail; superseded by SP 800-218)

NIST released SSDF 1.2 / SP 800-218r1 as an initial public draft in December 2025; it remains **CHANGE WATCH**, not the final baseline for this study.

Source:
- https://www.nist.gov/news-events/news/2025/12/secure-software-development-framework-ssdf-version-12-available-public

**SYNTHESIS:** fixing one bad artifact is weaker than changing the producing/validating system when the root cause is systemic.

Guards:
- `instance fixed ≠ root cause fixed`;
- `root cause identified ≠ recurrence control implemented`;
- `one regression test added ≠ whole failure class prevented`.

## 4. Corrective-action hierarchy

Classify each lesson before promoting it:

1. **incident-local cleanup** — removes artifacts/authority unique to this event;
2. **implementation defect correction** — fixes a concrete flaw without changing architecture policy;
3. **validation/control strengthening** — adds an oracle, negative test, monitoring invariant, release gate or recovery drill;
4. **durable architecture/security requirement** — changes the steady-state trust, data, update, authorization, recovery or compatibility contract;
5. **organizational/process change** — changes ownership, review, escalation, evidence retention or decision governance;
6. **accepted residual risk / no permanent change** — lesson is understood but a permanent control is not justified.

**MINTTAP DIRECTION:** do not promote every emergency measure to level 4 or 5. Promotion requires causal relevance, proportionality, ownership and validation.

Guards:
- `useful emergency measure ≠ justified permanent control`;
- `incident involved component X ≠ component X requires permanent redesign`;
- `more controls ≠ lower total risk`.

## 5. Avoid single-incident overfitting

A permanent control should address a defensible failure class or durable invariant, not merely replay the exact chronology of one event. Ask:
- what precondition allowed the failure;
- whether the precondition is structural or incidental;
- which other paths share it;
- whether the proposed control blocks the causal mechanism or only the observed symptom;
- whether the control creates availability, accessibility, privacy, recovery or operability regressions;
- whether a simpler invariant covers more variants.

Example: a hostile Service Worker incident does not automatically justify clearing all site data on every recovery. The durable invariant may instead be `untrusted executable/authority state cannot regain remote mutation authority before re-entry validation while irreplaceable domain data is preserved`.

Guards:
- `prevents exact replay ≠ prevents failure class`;
- `stronger restriction ≠ better architecture`;
- `security hardening ≠ permission to destroy authoritative local data`.

## 6. Preserve superseded assumptions and decision history

A changed baseline should record:
- prior assumption/requirement and why it was once accepted;
- incident/evidence that challenged it;
- new causal model;
- superseding decision and scope;
- affected client/trust/API/schema/release generations where relevant;
- migration/compatibility consequences;
- validation oracle;
- remaining uncertainty and review triggers.

Do not silently rewrite history so the old decision appears never to have existed.

**TRANSFER VALIDATION:** Software Engineering Studio A006 independently distinguishes accepted architecture decisions from validation PASS and preserves decision lifecycle evidence. That is compatible with this Web-owned incident/control governance, but exact implementation transfer remains OPEN.

Guards:
- `decision superseded ≠ prior evidence should be erased`;
- `ADR accepted ≠ corrective action effective`;
- `new baseline approved ≠ deployed fleet conforms`.

## 7. SOURCE — flaw remediation belongs inside configuration/change management

NIST SP 800-53 Rev.5 SI-2 requires identifying/reporting/correcting flaws, testing remediation for effectiveness and side effects before installation, and incorporating flaw remediation into configuration management. SP 800-53A Rev.5 assesses flaw-remediation evidence using update test results and installation/change-control records.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf

**SYNTHESIS:** incident-driven changes are still changes. Emergency origin does not exempt permanent controls from ordinary validation, configuration identity and change governance.

Guards:
- `urgent during incident ≠ exempt after incident`;
- `change deployed ≠ side effects acceptable`;
- `configuration changed ≠ intended invariant enforced`.

## 8. Corrective-action closure requires recurrence evidence

A corrective action should have a falsifiable acceptance oracle. Depending on the control, evidence can include:
- the original failure reproduced on a vulnerable fixture or prior generation;
- the same causal path rejected on the corrected generation;
- adjacent variants rejected where the control claims class coverage;
- legitimate current behavior still succeeds;
- stale/offline/unknown clients fail closed where required;
- local authoritative data survives update/recovery where required;
- rollback/recovery does not revive the vulnerable trust generation;
- observability detects violations without becoming the authorization mechanism.

**SYNTHESIS:** closure is evidence that the relevant failure mechanism is constrained, not evidence that a ticket, document or code change exists.

Guards:
- `code merged ≠ corrective action closed`;
- `test exists ≠ test would fail on vulnerable behavior`;
- `positive canary PASS ≠ negative invariant PASS`;
- `no recurrence observed ≠ recurrence prevented`.

## 9. PWA-specific permanent-control candidates

Incident evidence may justify durable requirements around:
- server-side generation/capability gates that stale Service Workers cannot bypass;
- separation of executable/authority state from irreplaceable local domain data;
- explicit client/trust/API/schema generation identity;
- fail-closed re-entry after long offline periods or incident epochs;
- replay suppression/reconciliation before compromise-era outbox admission;
- data-preserving update/recovery paths;
- independent deployment/domain/identity recovery authority;
- worker/update/cache observability sufficient to classify generations;
- tested recovery without indiscriminate site-data destruction.

These are **candidate control classes**, not claims about current LogMate architecture.

## 10. Cross-track contradiction checks

### Track B
A permanent security state must remain understandable and accessible. Do not retain incident-era blocking dialogs or warnings if a quieter capability-state model communicates the enduring restriction accurately.

Guard: `security state permanent ≠ incident alarm UX permanent`.

### Track C
Every promoted control needs both regression and side-effect evidence. Accessibility, localization, offline recovery, data preservation and managed-iPad behavior remain part of quality acceptance where relevant.

### Track D
Telemetry can demonstrate observed violations or trends, but a quiet dashboard cannot prove a failure class is impossible.

Guard: `zero observed recurrence ≠ recurrence control validated`.

### Track A
Browser/OS behavior can change. A permanent requirement should state the invariant separately from the current WebKit/Chromium mechanism, and platform-specific mechanisms remain CHANGE WATCH.

Guard: `durable invariant ≠ immutable browser mechanism`.

## 11. EFB / LogMate-like judgment

For an offline-first flight-log PWA, the most important permanent lesson from a severe client/origin incident may be architectural: **local usefulness and data preservation must not imply indefinite remote authority**. A long-offline iPad can retain records while its next remote mutation is gated by current trust/compatibility/reconciliation requirements.

A corrective action that merely forces all clients online immediately would overfit to a connectivity assumption not yet validated for the managed-EFB environment. Likewise, a blanket wipe may satisfy executable cleanup while violating the product's irreplaceable-data objective.

Exact iPadOS/WebKit/MDM/storage/sync behavior remains OPEN.

## 12. Track C validation campaign

Future product evidence should cover at least:
1. original vulnerable generation demonstrates the causal failure where safely reproducible;
2. corrected generation blocks it;
3. adjacent attack variant is blocked if class coverage is claimed;
4. legitimate current client succeeds;
5. stale Service Worker cannot bypass server gate;
6. long-offline client re-enters through current gate;
7. revoked trust/credential generation remains denied;
8. old configuration rollback does not restore old authority;
9. compromise-era outbox remains suppressed;
10. reconciled operation is admitted exactly as intended;
11. local records survive safe update;
12. local records survive executable-state recovery where required;
13. emergency account/control is absent unless deliberately promoted;
14. promoted control has ordinary owner and change history;
15. negative canary detects reintroduction;
16. monitoring outage does not fail open;
17. accessibility of permanent restricted/re-entry state;
18. localization/reflow does not hide restriction;
19. privacy review covers new telemetry/evidence retention;
20. performance/offline availability regression is measured;
21. managed-iPad behavior is validated on exact supported environment;
22. unsupported/degraded platform outcome is explicit;
23. superseded assumption remains reconstructable;
24. acceptance oracle is tied to exact source/build/deployment/runtime identity;
25. removal of the corrective control causes the regression test to fail or otherwise demonstrates test sensitivity.

No product PASS exists yet.

## 13. Operational governance model

`INCIDENT EVIDENCE → CAUSAL LESSON → CLASSIFY LOCAL VS SYSTEMIC → PROPOSE CONTROL/PROCESS CHANGE → CHECK CROSS-DOMAIN COST → PRESERVE SUPERSEDED DECISION → IMPLEMENT UNDER NORMAL CHANGE GOVERNANCE → PROVE RECURRENCE ORACLE + SIDE-EFFECT ORACLES → DEPLOY/STAGE → VERIFY ENFORCEMENT → RETIRE CORRECTIVE-ACTION ITEM → MONITOR / REASSESS`.

Do not collapse these transitions into `postmortem action item done`.

## 14. CHANGE WATCH

- NIST SSDF 1.2 / SP 800-218r1 is currently draft; recheck finalization before replacing SSDF 1.1 as canonical final guidance.
- Service Worker/update/storage and iOS/iPadOS managed-web behavior remain platform/version sensitive.
- Exact product release, auth, storage, API and fleet mechanisms remain implementation evidence, not generic web facts.

## 15. OPEN

- actual MintTap/LogMate incident history and postmortem process;
- actual change owner/approver roles;
- exact ADR/control-baseline/configuration-management implementation;
- exact recurrence test tooling and runtime identity chain;
- exact Service Worker/update/auth/API/trust/storage/outbox architecture;
- managed-iPad validation;
- legal/safety implications for flight-record preservation and correction;
- risk appetite and criteria for accepting no permanent change.

## 16. Gate assessment

**PASS (generic).** The Web Manager can now distinguish lesson capture from institutional change, incident-local cleanup from durable control promotion, symptom fixes from failure-class controls, supersession from historical erasure, and documentation/code completion from recurrence evidence.

Production/device/organizational validation remains OPEN.