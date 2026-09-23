# 266 — PWA Exception-Budget Breach Response, Compensating-Control Decay & Contingency Exit-Proof Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/fencing mechanics; Track B degraded/recovery UX; Track C destructive validation; Track D bounded debt/control-health measurement.  
Dependencies: 117–121 exception/waiver lifecycle, 127–130 resilience/degraded mode, 249–265 policy/distribution/dependency/topology/exception governance.

## Problem

265 established consequence-aware exception-debt budgets, renewal-authority separation and forced architecture-review triggers. The next failure boundary is what happens after the accepted envelope is breached, or when the controls that justified an exception stop providing comparable protection.

Two symmetric failures are dangerous. A breach can be treated as a panic switch and destroy unique offline data or abruptly remove recovery capability. Or it can become a dashboard warning that changes nothing, allowing temporary authority and residual-risk acceptance to persist indefinitely. Likewise, a compensating control can remain documented while topology, credentials, browser/runtime behavior, operator coverage or discovery assumptions have changed enough that the control no longer compensates.

Central rule: **budget breach is a governance state requiring consequence-aware containment, reassessment and explicit disposition—not automatic destructive shutdown and not implicit continuation. Compensating controls are current only while their assumptions, coverage and effectiveness remain current. A contingency exit is credible only when the successor path and predecessor retirement/recovery behavior are evidenced, including offline/unknown tails.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Owns whether Service Worker/cache/queue/runtime paths can actually be fenced, whether stale clients can still execute predecessor operations, and what browser/platform state survives offline/rejoin. Runtime state cannot accept risk.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `budget breach`, `degraded`, `recovery-only`, `renewal blocked`, `control stale`, `exit verification pending` and safe-data-recovery states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **880 → 888 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer. Measures debt envelope, control-health signals, exit-path exercises, predecessor traffic and unknown/offline tail. Metrics may trigger reassessment but cannot grant authority or prove retirement.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns breach-response semantics, compensating-control applicability, residual-risk disposition, exit-proof criteria and re-entry governance.

## SOURCE

### NIST SP 800-53B — compensating controls require rationale, comparable protection and accepted residual risk

NIST SP 800-53B describes compensating controls as alternatives used when baseline controls are tailored out by necessity while protection is still required. It states that compensating controls should provide equivalent or comparable protection, require rationale, and require assessment and acceptance of the associated security/privacy risk. It also notes that technology-based compensating controls may be temporary until the system is updated.

Source: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53B.pdf

**TRANSFER VALIDATION:** supports treating compensating controls as evidence-bearing risk treatments whose continued adequacy matters. It does not prescribe a MintTap/LogMate exception score, degradation ladder or PWA exit workflow.

### NIST SP 800-137 / RMF Monitor — control effectiveness and risk posture require ongoing visibility

SP 800-137 frames continuous monitoring as visibility into assets, threats/vulnerabilities and deployed-control effectiveness, providing ongoing assurance that controls remain aligned with organizational risk tolerance and information for timely response when controls are inadequate. The RMF Monitor step similarly calls for monitoring the environment, ongoing assessment of control effectiveness, analysis/response to monitoring output and ongoing authorization based on current evidence.

Sources: https://csrc.nist.gov/pubs/sp/800/137/final  
https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step

**TRANSFER VALIDATION:** supports control-decay detection and current-risk reassessment. It does not imply continuous telemetry can observe every long-offline PWA client.

### NIST CSF 2.0 / SP 1303 — governance includes monitoring, evaluation and adjustment

CSF 2.0 emphasizes governance and risk-informed decisions; SP 1303 describes integrating risk monitoring, evaluation and adjustment across organizational units/programs.

Sources: https://www.nist.gov/cyberframework  
https://csrc.nist.gov/pubs/sp/1303/final

**TRANSFER VALIDATION:** supports escalating a breached exception envelope into explicit risk-governance decisions rather than treating the metric as self-executing authority.

## SYNTHESIS 1 — breach is a state transition, not a kill command

When the accepted debt envelope is exceeded, the system should enter a governed breach state. The response depends on consequence: new high-consequence mutation/publication may be blocked or require stronger authorization; read/recovery/export-for-preservation may remain available where necessary to prevent data loss or preserve evidence.

Guards:
- `budget breached ≠ delete data`;
- `budget breached ≠ all capabilities forbidden`;
- `budget breached ≠ existing authority silently continues`.

A breach should force reassessment/disposition, not encode the disposition itself.

## SYNTHESIS 2 — use consequence-aware degradation rather than binary availability

A useful response ladder can distinguish capabilities such as:
1. ordinary read/view;
2. local capture preserving unique data/provenance;
3. recovery/export-for-preservation;
4. queued mutation;
5. remote synchronization;
6. publication/finalization;
7. administrative/recovery-authority actions.

Higher-consequence capabilities can be fenced first while lower-consequence preservation functions remain available. The exact ladder is product/domain specific and remains OPEN.

Guard: `degraded mode ≠ data-loss mode`.

## SYNTHESIS 3 — compensating controls have an applicability contract

A compensating control is not merely a named checkbox. Its evidence should identify at least:
- the risk/control gap it compensates for;
- consequence/capability scope;
- assumptions about topology, identity, credentials, runtime and operators;
- expected protection/effect;
- observation/validation method;
- review/expiry triggers;
- dependencies/failure domains;
- residual risk and accountable authority.

If those assumptions materially change, applicability must be reassessed even before nominal expiry.

Guard: `control documented ≠ control currently compensating`.

## SYNTHESIS 4 — control decay includes silent semantic decay

A control can remain technically alive while no longer reducing the intended risk. Examples include:
- a server rejection rule that no longer covers a newly admitted API route;
- a manual review that still occurs but no longer sees offline-tail operations;
- a credential fence that excludes a new device incarnation scheme;
- a telemetry alert that misses Service Worker/local queue execution;
- a recovery procedure whose required operator/provider dependency has changed;
- a rate/approval control whose consequence classification has changed.

Guard: `control running ≠ control effective for current topology`.

## SYNTHESIS 5 — positive health signals do not erase blind spots

A dashboard can show 100% health for the surfaces it observes while long-offline clients, shadow consumers or manual/export paths remain outside coverage. Control-health evidence must retain coverage scope and known unknowns.

Guards:
- `green control dashboard ≠ complete control coverage`;
- `no alert ≠ no control decay`;
- `online fleet protected ≠ offline fleet protected`.

## SYNTHESIS 6 — breach response needs explicit authority and provenance

Actions taken because a budget was breached should identify:
- breached envelope/dimension;
- affected consequence scope;
- current evidence and uncertainty;
- immediate containment/degradation;
- preserved capabilities/data;
- decision authority;
- reassessment deadline/trigger;
- architecture-review or residual-risk path;
- exit/re-entry criteria.

A metric engine can detect breach but should not silently grant itself authority to delete, renew, normalize or accept residual risk.

Guard: `metric detects breach ≠ metric authorizes disposition`.

## SYNTHESIS 7 — residual-risk acceptance is bounded successor evidence

If operation must continue beyond the accepted envelope, continuation requires explicit current residual-risk acceptance appropriate to consequence. That acceptance should bind scope, assumptions, compensating controls, owner, review/expiry trigger and normalization/exit obligation.

It should not mutate the original budget to make the breach disappear.

Guards:
- `risk accepted ≠ risk eliminated`;
- `acceptance recorded ≠ exception normalized`;
- `budget redrawn after breach ≠ breach resolved`.

## SYNTHESIS 8 — repeated acceptance can itself become architecture debt

If every breach is followed by a new acceptance without improving the normal architecture, predecessor retirement or exit evidence, governance has become a normalization-avoidance loop. Recurring acceptance should raise architecture-review pressure rather than automatically creating precedent.

Guard: `accepted repeatedly ≠ acceptable permanently`.

## SYNTHESIS 9 — exit plans are hypotheses until exercised

A document saying “migrate to N2” is not exit proof. A credible exit requires evidence proportionate to consequence that:
- successor path is admitted/current;
- required data/provenance can move or remain safely accessible;
- queued operations have disposition/revalidation rules;
- predecessor new consequence-bearing use is fenced;
- rollback/recovery behavior is understood;
- offline/unknown tails have rejoin/retirement handling;
- current users/operators can execute the procedure;
- the path has been exercised at the relevant boundary where feasible.

Guard: `exit plan exists ≠ exit path works`.

## SYNTHESIS 10 — exit proof is scoped, not universal

A server-side migration drill can prove server-side transition without proving installed/long-offline PWA behavior. A Chromium test does not prove iPadOS Home Screen behavior. A managed-device procedure does not prove every unmanaged/export recipient path.

Guard: `one exit drill PASS ≠ fleet-wide exit proven`.

## SYNTHESIS 11 — failed exit exercise should update authority decisions

If an exit drill reveals that predecessor fencing, data recovery or successor admission does not work, the failure is governance evidence. It should update debt, control applicability and risk decisions rather than being hidden as “test environment only” without analysis.

Guard: `exit drill failed ≠ exit obligation unchanged`.

## SYNTHESIS 12 — exit success requires predecessor disposition, not just successor success

As established in 264, successor availability is only half of normalization. Exit closure must also address old credentials/routes/queues/caches/offline clients and any residual recovery-only path. Some predecessor state may remain intentionally readable for evidence/recovery while mutation authority is retired.

Guard: `successor current ≠ predecessor harmless`.

## SYNTHESIS 13 — re-entry after breach needs current evidence

Returning from degraded/breach state to ordinary operation should require evidence that the breached condition has been dispositioned: debt reduced or explicitly re-accepted, controls current, successor/predecessor state reconciled and required review completed. Merely dropping below a numeric threshold due to ticket closure is insufficient.

Guard: `metric below threshold ≠ safe re-entry proven`.

## SYNTHESIS 14 — offline PWA capture and authority should remain separable

For an EFB/LogMate-like iPad, a budget breach or stale compensating control should not force destruction of unique flight/logbook data. Where domain policy permits, local capture/preservation may remain available while remote mutation/publication is fenced pending current bootstrap and revalidation.

Guards:
- `capture preserved ≠ publication authorized`;
- `sync blocked ≠ local unique data should be erased`.

Product/aviation/legal semantics remain OPEN.

## SYNTHESIS 15 — Service Worker/cache cleanup is not exit proof

Unregistering a Service Worker or clearing Cache Storage on an observed client may reduce a runtime surface but does not prove server rejection of obsolete operations, removal from offline devices or closure of manual/export paths.

Guard: `client cleanup PASS ≠ contingency exit PASS`.

## SYNTHESIS 16 — control decay should propagate into dependent closure claims

If closure C12 depended on compensating control X and X is later found inapplicable for the relevant interval/scope, C12 requires dependency-aware reassessment. Do not automatically invalidate unrelated closures, but do not leave transitive claims untouched merely because their direct record did not change.

Guard: `control decayed ≠ dependent closure remains current by default`.

## SYNTHESIS 17 — containment itself can create new risk

Blocking synchronization can increase divergence and offline-tail debt; disabling recovery can threaten data availability; emergency manual handling can create new provenance gaps. Breach response must therefore assess second-order risk rather than assume “more restrictive” is always safer.

Guard: `more restrictive ≠ lower total risk in every consequence dimension`.

## SYNTHESIS 18 — contingency exit is a lifecycle, not a date

A target date is useful but not sufficient. Exit lifecycle should include `PLANNED → READY-FOR-EXERCISE → EXERCISED/PARTIAL/FAILED → CUTOVER-AUTHORIZED → CUTOVER-IN-PROGRESS → PREDECESSOR-FENCED → RESIDUAL-RECOVERY-ONLY/RETIRED → CLOSED`, with contradiction/reopen paths.

Guard: `exit date reached ≠ exit completed`.

## Cross-track transfer

### Track A — Platform/Browser
Provide evidence for which browser/runtime surfaces remain executable after degradation or cutover: Service Worker control, Cache Storage/IndexedDB, queued requests, navigation/offline behavior and server rejection. Do not infer governance authority from runtime freshness.

### Track B — UX/IA/Content
Distinguish “data preserved locally”, “sync blocked”, “recovery available”, “publication blocked”, “control review required” and “safe to resume” states. Avoid generic “offline/error” copy that hides authority or data-preservation semantics. Human/AT validation remains OPEN.

### Track C — Quality
Add negative/destructive cases below and require restart/restore/rejoin variants where relevant. No runtime PASS is claimed by this research.

### Track D — Discovery/Analytics
Measure breach dimensions, control-health evidence age/coverage, exit-drill recency/results, predecessor traffic and offline/unknown tail. Analytics may challenge a claim but cannot accept risk or authorize re-entry.

## Track C destructive campaign — +8 defined cases

881. **Budget-breach destructive cleanup** — breach causes deletion/reset of unique offline data instead of consequence-aware fencing. Expected: preserve data/provenance; fence authority as needed.
882. **Dashboard-green control laundering** — observed control health is treated as complete effectiveness despite an unobserved offline/shadow surface. Expected: coverage scope/unknowns remain explicit.
883. **Nominal-expiry-only control freshness** — compensating control remains current after material topology/policy change because review date has not arrived. Expected: material assumption change triggers reassessment.
884. **Risk-acceptance budget erasure** — accepted breach is implemented by moving the threshold/score until dashboard becomes green. Expected: historical breach and successor acceptance remain distinct evidence.
885. **Exit-plan paper PASS** — unexercised migration document is treated as exit proof. Expected: exercised/scoped evidence required proportionate to consequence.
886. **Successor-only exit closure** — N2 works, but E1 route/credential/queue/offline-tail remains executable. Expected: predecessor disposition required.
887. **Ticket-count re-entry** — closed tickets drop metric below threshold and ordinary authority resumes without control/closure reconciliation. Expected: explicit current re-entry evidence.
888. **Client-cleanup exit theater** — observed Service Worker/cache cleanup is treated as fleet/server/manual-path retirement. Expected: consequence-scoped server/authority and offline-tail evidence required.

Campaign total: **888 defined cases**. Definition is not execution; physical-device, AT, human and product runtime validation remain OPEN.

## EFB / LogMate-like application case

Scenario: a company iPad has been offline for weeks while exception debt exceeds the accepted envelope. The normal sync path N2 is available, but an emergency predecessor E1 and its compensating server review control X were previously used. A new API route means X no longer covers every E1 consequence.

Generic safe sequence:
1. preserve local unique records, queue and provenance;
2. classify X as potentially stale for the uncovered route rather than declaring all historical evidence false;
3. fence new high-consequence E1 operations at an authority boundary that does not depend only on observed-client cleanup;
4. retain recovery/read capability needed to avoid data loss where policy permits;
5. perform current bootstrap/identity/authority verification;
6. reconcile queued operations individually against N2/current policy;
7. exercise successor data/provenance recovery and predecessor rejection;
8. account for other offline/unknown devices rather than treating the returning iPad as the fleet;
9. create current residual-risk/normalization evidence for any intentionally retained recovery-only path;
10. re-enter ordinary operation only after the breach/control/exit obligations have current disposition.

This is a generic architecture pattern, not a claim about actual LogMate implementation, MDM, iPadOS behavior, aviation requirements or backend semantics.

## MINTTAP DECISION / DIRECTION

For future product-specific governance, prefer:
- consequence-aware breach states rather than destructive global shutdown;
- preservation of unique local data/provenance while mutation/publication authority can be fenced separately;
- compensating-control records with explicit assumptions, coverage and review triggers;
- residual-risk acceptance as successor evidence rather than threshold rewriting;
- exit proof that covers successor readiness **and** predecessor disposition;
- offline/unknown tails as explicit obligations;
- re-entry based on current evidence, not dashboard arithmetic alone.

Do not set numeric thresholds, capability classes, approval roles or legal/safety policy until canonical product/domain evidence exists.

## OPEN

- Actual MintTap/LogMate exception budgets and risk tolerance.
- Actual managed-iPad/MDM/ADE topology and iPadOS/WebKit behavior.
- Which local capture/recovery capabilities are legally/operationally permissible when remote authority is fenced.
- Actual Service Worker/cache/IndexedDB/queue/backend rejection semantics.
- Actual compensating controls, their effectiveness evidence and ownership.
- Actual exit/rollback procedures, backup/restore and offline-tail inventory.
- Aviation/legal/privacy/safety requirements.
- Physical-device, screen-reader, representative-human and exact-product runtime evidence.

## CHANGE WATCH

- Apple/WebKit/iOS/iPadOS PWA lifecycle/storage/background behavior.
- Managed-device enrollment/restore/Return-to-Service behavior.
- NIST RMF/CSF/800-53 family revisions affecting risk/control terminology.
- Product topology, authority model, consequence classification and offline policy.

## Persistent guards added

- `budget breached ≠ delete data`;
- `budget breached ≠ all capabilities forbidden`;
- `degraded mode ≠ data-loss mode`;
- `control documented ≠ control currently compensating`;
- `control running ≠ control effective for current topology`;
- `green control dashboard ≠ complete control coverage`;
- `metric detects breach ≠ metric authorizes disposition`;
- `risk accepted ≠ risk eliminated`;
- `acceptance recorded ≠ exception normalized`;
- `accepted repeatedly ≠ acceptable permanently`;
- `exit plan exists ≠ exit path works`;
- `one exit drill PASS ≠ fleet-wide exit proven`;
- `successor current ≠ predecessor harmless`;
- `metric below threshold ≠ safe re-entry proven`;
- `capture preserved ≠ publication authorized`;
- `client cleanup PASS ≠ contingency exit PASS`;
- `more restrictive ≠ lower total risk in every consequence dimension`;
- `exit date reached ≠ exit completed`.

## Gate result

**PASS (generic).** The Web Manager can now distinguish exception-budget breach from destructive shutdown; reason about consequence-aware degradation; model compensating-control applicability and decay; prevent residual-risk acceptance from laundering debt; require scoped, exercised contingency-exit evidence; and preserve offline unique data while fencing stale authority. Product implementation and runtime validation remain OPEN.

## Next high-value target

**267 — degraded-authority recovery ordering, control-restoration proof & safe re-entry under partial fleet convergence.** Determine ordering when multiple controls recover at different times; prevent one restored control from reopening high-consequence authority while others remain stale; define evidence for safe staged re-entry; and handle long-offline devices that return after central re-entry without allowing obsolete authority or destructive reset.