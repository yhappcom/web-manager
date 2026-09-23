# 265 — PWA Exception-Debt Budget, Renewal-Authority Separation & Forced Architecture-Review Triggers

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/fencing mechanics; Track B exception/recovery UX; Track C destructive validation; Track D bounded debt measurement.  
Dependencies: 117–121 exception/waiver lifecycle, 127–130 dependency concentration/resilience, 249–264 policy/distribution/dependency/topology/exception governance.

## Problem
264 established that exception expiry ends exceptional authority rather than deleting data, that normalization requires both successor-current and predecessor-fenced evidence, and that repeated/concentrated exceptions form aggregate architecture debt. The next failure boundary is governance of that debt.

A fixed count such as “no more than five exceptions” is easy to measure but can be dangerously meaningless: one high-consequence recovery bridge may dominate ten low-consequence read-only exceptions. Conversely, a vague “risk-based” process can become permanent discretionary renewal. A useful model must constrain aggregate temporary authority without inventing universal numeric thresholds, prevent self-renewal loops, force architecture review when temporary paths become structural, and preserve legitimate contingency/recovery capability when prolonged exceptional operation is actually necessary.

Central rule: **exception debt is governed by consequence, exposure duration, recurrence, concentration, dependency criticality, normalization evidence and residual uncertainty—not ticket count alone. Renewal is a new authorization decision and should be separated from the actor/path whose continued operation creates the need. Architecture-review triggers are evidence-based escalation conditions, not automatic declarations that an exception is malicious or must be destructively removed.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Owns facts about Service Worker/cache/queue/runtime reachability, offline-tail persistence and whether predecessor paths remain technically executable. Runtime necessity cannot authorize renewal.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `temporary`, `renewal pending`, `expired/recovery-only`, `architecture review required`, `normalization blocked` and `safe data recovery` states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **872 → 880 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer. Measures age, recurrence, overlap, concentration, critical-workflow share, extension count and predecessor traffic; metrics inform governance but do not grant authority or prove absence.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns debt-budget semantics, renewal separation, escalation/architecture-review triggers, contingency-vs-normalization-failure classification and residual-risk disposition.

## SOURCE

### NIST CSF 2.0 / SP 1303 — risk governance is contextual, not a universal ticket quota
NIST CSF 2.0 and SP 1303 frame cybersecurity risk management around organizational context, risk governance and enterprise risk integration. Profiles/Tiers and risk information are intended to support prioritized improvement and management decisions rather than prescribe one universal numeric exception threshold.

Sources: https://www.nist.gov/cyberframework  
https://csrc.nist.gov/pubs/sp/1303/final

**TRANSFER VALIDATION:** supports consequence-aware debt governance and escalation into enterprise/architecture risk decisions. It does not define a PWA exception budget.

### NIST IR 8286A Rev. 1 — risk appetite/tolerance and scenario-based risk analysis
NIST IR 8286A Rev. 1 (December 2025) describes identifying/estimating cybersecurity risk in the context of enterprise risk guidance, appetite and tolerance, using scenario likelihood/impact information to prioritize and communicate risk.

Source: https://csrc.nist.gov/pubs/ir/8286/a/r1/final

**TRANSFER VALIDATION:** supports treating exception debt as risk scenarios with impact/exposure/concentration rather than raw counts. Product-specific thresholds remain OPEN.

### NIST SP 800-53 Rev. 5 / Release 5.2.0 — separation of duties, least privilege and controlled change
AC-5 addresses separation of duties to reduce abuse of authorized privileges; AC-6 addresses least privilege. CM-3/CM-4/CM-5 keep changes, including emergency changes, under review/approval/impact/access control.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** supports separating request/operation from material renewal authorization and preventing exceptional access from silently expanding. It does not require a specific organizational approval matrix.

### NIST SP 800-37 Rev. 2 / ongoing authorization guidance — authorization depends on current risk information
The RMF treats authorization as a risk decision supported by assessment and continuous monitoring rather than a permanent one-time property.

Sources: https://www.nist.gov/publications/risk-management-framework-information-systems-and-organizations-system-life-cycle  
https://www.nist.gov/publications/supplemental-guidance-ongoing-authorization-transitioning-near-real-time-risk

**TRANSFER VALIDATION:** supports reassessing temporary authority when assumptions materially change; it does not make every exception an RMF authorization package.

## SYNTHESIS 1 — budget is a governance envelope, not a universal number
An exception-debt budget should answer whether aggregate temporary authority remains within the organization/product's accepted risk envelope. Useful dimensions include consequence class, capability (read/write/publish/recovery/admin), data sensitivity, exposure duration, recurrence, extension count, critical-workflow dependence, predecessor-removal backlog, offline/unknown fleet tail, concentration/common-mode dependence and uncertainty in discovery/closure evidence.

Guard: `exception count within quota ≠ exception risk within tolerance`.

Do not invent generic weights or thresholds. Product/domain/legal/safety evidence must set them.

## SYNTHESIS 2 — budget consumption should be consequence-aware and explainable
A budget model may use qualitative bands or product-defined quantitative scoring, but every score must remain decomposable into evidence. A high-consequence write/recovery bridge can consume more governance attention than many read-only diagnostic exceptions. Metrics are prioritization aids, not semantic authority.

Guards: `score low ≠ safe`; `score high ≠ malicious`; `metric ≠ authorization`.

## SYNTHESIS 3 — renewal is a new decision, not continuity by default
Renewal creates successor authorization evidence with current scope, assumptions, compensating controls, owner, expiry/review trigger and normalization blocker. If no valid renewal exists at expiry, the prior exception does not silently remain current.

Guards: `renewal requested ≠ renewal granted`; `missed review ≠ implicit extension`; `service dependence ≠ automatic renewal`.

## SYNTHESIS 4 — separate renewal authority from the beneficiary where consequence warrants
The component owner/operator may supply evidence and request continuation, but material exception renewal should not be self-certified solely by the actor whose service would fail if the exception ended. Risk-proportionate separation may be organizational, role-based or workflow-enforced; it need not mean a different company or universal two-person approval.

Guards: `can request ≠ can approve`; `operational owner ≠ sole renewal authority by default`; `separation of duties ≠ mandatory bureaucracy for every low-risk case`.

## SYNTHESIS 5 — repeated renewal is evidence of architecture mismatch
Repeated extensions of the same capability/path, recurring re-creation shortly after closure, or an increasing share of critical workflows relying on exceptions should trigger architecture review. The review asks whether the normal architecture lacks a real requirement, whether the exception should become a deliberately governed normal capability, whether workflow redesign is needed, or whether the capability should be retired.

Guard: `temporary label retained ≠ temporary architecture retained`.

## SYNTHESIS 6 — forced review triggers should be multi-dimensional
Candidate triggers include: repeated renewal; age beyond product-defined tolerance; overlapping exceptions with the same failure domain; critical workflow dependence; rising offline/unknown tail; repeated predecessor resurrection; normalization deadline misses; control/collector contradiction; material policy/topology change; or exception debt exceeding an accepted consequence-aware envelope.

A trigger means **review required**, not automatically `reject`, `delete`, `compromise`, or `production outage`.

Guard: `review trigger fired ≠ destructive shutdown authorized`.

## SYNTHESIS 7 — legitimate prolonged contingency differs from normalization failure by evidence
A long-lived contingency can be legitimate if there is a documented continuing hazard/mission need, bounded capability, current authority, compensating controls, periodic independent-enough review, tested exit/normalization path and explicit residual-risk acceptance. A normalization failure is characterized by stale justification, repeated auto-renewal, missing owner, unchanged temporary rationale despite structural dependence, untested predecessor fencing, or no credible exit plan.

Guard: `long duration ≠ automatically illegitimate`; `documented reason ≠ sufficient current justification`.

## SYNTHESIS 8 — architecture review may normalize, redesign, retain contingency or retire
Forced review has four broad outcomes: (1) admit a durable normal path with full lifecycle/governance; (2) redesign the workflow to remove the dependency; (3) retain a bounded contingency with explicit risk acceptance and stronger review; or (4) retire the capability/path while preserving recoverable data/evidence. The review should not simply rename an exception “normal” to clear the debt dashboard.

Guard: `renamed normal ≠ normalized safely`.

## SYNTHESIS 9 — debt concentration needs common-mode accounting
Exceptions sharing identity provider, credential issuer, cloud/provider, operator, queue, recovery bridge, deployment path, data store or external recipient channel can fail together. Budgeting should expose concentration rather than treat ticket IDs as diversification.

Guard: `budget distributed across tickets ≠ risk distributed across failure domains`.

## SYNTHESIS 10 — budget exhaustion should degrade authority, not erase unique data
If the accepted exception envelope is exceeded, consequence-bearing new operations may need stronger approval, quarantine or degraded/recovery-only mode. Budget exhaustion is not a license to delete unique offline records, clear queues without provenance, or factory-reset devices to make debt disappear.

Guard: `exception budget exceeded ≠ data destruction authorized`.

## SYNTHESIS 11 — offline PWA tails consume uncertainty debt even when silent
A company iPad that has been offline beyond the review horizon may hold obsolete queue/service-worker state and unique records. It should remain an explicit unknown-tail obligation until governed rejoin/retirement/disposition. Silence can increase uncertainty debt; it cannot count as successful normalization.

Guard: `offline silence ≠ zero exception debt`.

## SYNTHESIS 12 — Service Worker/runtime freshness cannot approve exception renewal
A current Service Worker, successful fetch, fresh session or healthy runtime proves technical state only. It cannot establish current organizational authorization or residual-risk acceptance.

Guard: `runtime healthy ≠ exception governance healthy`.

## SYNTHESIS 13 — renewal evidence itself has assumptions and expiry
A renewal decision depends on topology, consequence, compensating controls, discovery coverage, authority and normalization plan. Material changes can invalidate its applicability before its nominal expiry. Conversely, an expired approval remains historical evidence of what was authorized then.

Guard: `renewed until date X ≠ valid under every topology until X`.

## SYNTHESIS 14 — closure metrics need denominator and consequence context
“90% exceptions closed” can be misleading if the remaining 10% carry all recovery/write authority. Report closure by consequence/capability, oldest age, concentration and critical-workflow dependence, not raw percentage alone.

Guard: `closure percentage improved ≠ residual risk improved`.

## SYNTHESIS 15 — architecture-review independence should match consequence
For high-consequence exceptions, the review should be independent enough from the requesting/operating failure domain to challenge assumptions. For low-consequence cases, lightweight role separation may be sufficient. Independence is risk-proportionate, not ceremonial.

Guard: `different approver name ≠ independent review`.

## SYNTHESIS 16 — debt retirement requires evidence, not dashboard deletion
An exception leaves the active debt set only when its authority is expired/withdrawn as intended and its consequence-bearing predecessor path is fenced/removed or explicitly recorded as residual, with data/operations reconciled and relevant offline/external tails dispositioned. Deleting the ticket or changing its label does not retire debt.

Guard: `ticket closed ≠ exception debt retired`.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. govern exception debt with consequence-aware envelopes, not universal ticket quotas;
2. keep product-specific weights/thresholds OPEN until domain evidence exists;
3. make renewal a successor authorization event and prohibit implicit grace;
4. separate material renewal approval from the beneficiary/requester sufficiently for the consequence;
5. force architecture review on recurrence, age, concentration, critical dependence, missed normalization, contradiction or material assumption change;
6. distinguish review trigger from destructive shutdown;
7. allow legitimate prolonged contingency only with current bounded authority, compensating controls, review and credible exit/recovery evidence;
8. preserve unique offline data/provenance when debt is over budget or authority expires;
9. count offline/unknown fleet tails as uncertainty/debt obligations rather than absence;
10. retire debt only with consequence-scoped normalization/removal/residual evidence.

## EFB / LogMate-like application case
Assume emergency sync bridge E1 was created during an outage and has been renewed twice because several company iPads remain intermittently offline. A third renewal request arrives while normal bridge N2 is available for connected devices.

Safe generic sequence:
1. preserve E1 history and current debt/concentration state; do not edit the original approval;
2. identify E1 capability/consequence, dependent workflows, unknown/offline devices and shared credentials/providers;
3. test whether the third request crosses product-defined recurrence/age/critical-dependence review triggers;
4. require architecture review rather than beneficiary self-renewal when the trigger fires;
5. determine whether remaining offline-tail need is a legitimate bounded contingency or evidence that N2/rejoin architecture is incomplete;
6. if temporary continuation is justified, create a successor exception with narrower scope where possible, explicit compensating controls, review/expiry and exit conditions;
7. block obsolete mutation/publication outside that scope while preserving unique flight/logbook records and provenance;
8. on device rejoin, bootstrap current authority and revalidate queued operations individually through current identity/dedup/conflict rules;
9. prove E1 predecessor fencing/removal for devices/workflows that no longer require it; retain unknown tails as debt;
10. close debt only when successor/current-path and predecessor/residual-state evidence support it.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
873. **Raw-count budget theater** — five low-risk exceptions and one recovery-authority exception consume identical budget and produce the same decision. Expected: fail.
874. **Beneficiary self-renewal loop** — E1 operator repeatedly renews E1 solely because expiry would break its service. Expected: fail for material consequence.
875. **Implicit grace after missed review** — expiry passes without decision and E1 remains mutation-authorized. Expected: fail.
876. **Review-trigger equals destructive shutdown** — recurrence trigger immediately deletes unique offline data/queues. Expected: fail.
877. **Rename-to-normal debt laundering** — exception is relabeled normal without lifecycle admission or predecessor/assurance updates. Expected: fail.
878. **Ticket-diversification concentration laundering** — many exceptions sharing one credential/provider are treated as diversified debt. Expected: fail.
879. **Offline-silence budget relief** — unreachable iPads are removed from debt because they emit no telemetry. Expected: fail.
880. **Dashboard-close retirement theater** — exception ticket closes while predecessor route still accepts obsolete writes after restore/rejoin. Expected: fail.

**VALIDATION:** these are defined destructive cases only. Execution PASS is not claimed.

## OPEN / VALIDATION
- Actual MintTap/LogMate exception authority matrix, risk appetite/tolerance, budget dimensions, thresholds and architecture-review roles remain OPEN.
- Actual queue/server rejection, MDM, fleet, Service Worker and managed-iPad behavior remain OPEN.
- Aviation/safety/legal consequences and any required approval separation remain OPEN.
- Physical iOS/iPadOS installed-PWA, long-offline rejoin and restore behavior remain OPEN.
- Human/AT comprehension of renewal-pending, recovery-only and architecture-review-required states remains OPEN.
- Actual provider/credential/operator concentration and critical-workflow dependence remain OPEN.

## CHANGE WATCH
- NIST CSF/RMF/IR 8286/SP 800-53 revisions affecting risk governance, authorization and separation of duties.
- Apple Platform Deployment and WebKit/iOS/iPadOS changes affecting managed-device/PWA lifecycle and offline tails.
- Canonical MintTap/LogMate implementation/domain evidence when available.

## Next high-value target
**266 — exception-budget breach response, compensating-control decay & contingency exit-proof governance.** Determine how to respond when accepted debt is exceeded without destructive cleanup; how compensating controls age or become invalid as topology/policy changes; how to prove a prolonged contingency still has a viable exit path; and how to prevent risk acceptance from becoming a permanent substitute for normalization.