# 130 — PWA Recovery-Objective Conflict & Graceful-Degradation Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + SAFETY/LEGAL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 083–129 PWA/recovery/assurance chain; Track A Service Worker/offline/client-generation mechanics; Track B partial-state UX; Track C destructive/degraded-mode validation; Track D measurement caveats; Software Engineering for implementation evidence.

## Purpose

129 tied recovery paths to named recovery objectives and executable evidence. The next failure is objective conflict: restoring availability quickly can conflict with integrity, provenance, privacy, current authorization, stale-client retirement or safe reconciliation.

Central rule:

> **Recovery is capability-specific. Restore the safest useful subset that can be justified now; do not convert an availability objective into unproven authority.**

`graceful degradation` here means preserving bounded useful capability under adverse conditions while making unavailable/unsafe capability explicit. It does not mean silently weakening security.

## 1. Five-track balance

- **A Platform/Browser — dependency supplier:** origin availability, Service Worker control, Cache Storage/IndexedDB state, navigation and online/offline transitions determine what a client can actually do.
- **B UX/IA/Content — high-value consumer:** partial recovery must be represented as capability state, with clear local/remote, read/write, queued/synced and recovery/reconciliation distinctions.
- **C Quality — high dependency pressure:** owns degraded-mode functional/accessibility tests, negative authorization oracles, transition tests and recovery-objective timing.
- **D Search/Analytics — supporting consumer:** telemetry may measure recovery-state exposure and completion but cannot prove offline population convergence or authorization correctness.
- **E Architecture/Security/Operations — highest-risk owner:** owns objective precedence, capability partitioning, fail-closed boundaries, degraded-mode authority and normalization criteria.

Allocation remains E-heavy, with B/C receiving more transfer pressure than in 129 because partial recovery becomes a user-visible state machine.

## 2. SOURCE — resilience permits degraded operation, but preserves essential capability

NIST defines information-system resilience as the ability to continue operating under adverse conditions, even in a degraded/debilitated state, while maintaining essential operational capabilities, and to recover to an effective operational posture consistent with mission needs.

Sources checked 2026-09-18:
- https://csrc.nist.gov/glossary/term/information_system_resilience
- https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final

**SYNTHESIS:** degradation is legitimate only when the remaining capability is explicitly bounded and still satisfies the essential property being claimed. A degraded state that restores a UI by bypassing integrity or authorization is not automatically resilient.

Guards:
- `degraded operation ≠ weakened authority by default`;
- `screen available ≠ capability safely recovered`;
- `essential local utility preserved ≠ remote mutation authority restored`.

## 3. SOURCE — RTO/RPO do not settle conflicting properties

NIST SP 800-34 Rev.1 defines RTO as the maximum recovery-phase duration before unacceptable mission/business impact and RPO as the data point to which recovery is required. These are important consequence boundaries but do not themselves prove integrity, provenance, confidentiality or current authorization.

Sources:
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf
- https://csrc.nist.gov/glossary/term/Recovery_Time_Objective
- https://csrc.nist.gov/glossary/term/recovery_point_objective

**SYNTHESIS:** when an RTO can be met only by bypassing a current trust/API/reconciliation requirement, the correct response is not to redefine `available` as `authorized`. Record the objective conflict and recover a narrower capability if possible.

Guards:
- `RTO pressure ≠ authorization bypass justification`;
- `RPO met ≠ recovered records trusted`;
- `availability restored ≠ integrity restored ≠ authority restored`.

Actual MintTap/LogMate consequence priorities remain **OPEN**.

## 4. Capability decomposition before fail-open/fail-closed decisions

Do not classify the whole PWA as simply `up/down` or `fail-open/fail-closed`. Decompose capabilities such as:
1. launch/render cached shell;
2. read locally stored records;
3. search/filter local records;
4. create local draft/record;
5. edit/delete local authoritative data;
6. export/recovery copy;
7. authenticate/re-establish current session;
8. fetch current policy/schema/app generation;
9. enqueue an operation locally;
10. transmit queued operations;
11. reconcile conflicts/provenance;
12. mutate remote authoritative state;
13. destructive remote operation/account action;
14. import/restore data;
15. install/activate a new worker/client generation.

Each capability gets its own prerequisites and degraded-state policy.

Guard: `application available ≠ every capability available`.

## 5. Generic precedence model

When objectives conflict, evaluate in this order rather than applying a universal availability-first rule:

1. **Irreplaceable human/user data preservation** — avoid destructive cleanup merely to normalize software state.
2. **Safety/legal consequence if known** — product-specific and OPEN until authoritative evidence exists.
3. **Integrity/provenance** — do not silently convert uncertain data into trusted authoritative data.
4. **Current authorization/confidentiality/privacy** — do not restore remote authority through stale credentials/client generation merely to meet RTO.
5. **Bounded local usefulness** — preserve read/export or local capture where product design can do so safely.
6. **Remote availability/convenience** — restore after required trust/reconciliation gates.

This is a generic decision order, not a claim about aviation regulatory priority or actual LogMate safety classification.

## 6. Fail-closed, degrade, and fail-visible

Three different responses are useful:

### Fail closed
Use where an unverified action could create remote authority, destructive mutation, privacy disclosure, trust-generation rollback or provenance corruption. Examples: stale client remote write, revoked credential replay, destructive account action, unreconciled compromise-era outbox.

### Degrade safely
Use where useful capability can remain without granting the unsafe property. Examples: local read/search; recovery export; local draft/capture explicitly marked unsynced; cached help/instructions; view-only historical data where confidentiality requirements are still met.

### Fail visibly
A capability may be unavailable, but the system must expose the boundary rather than masquerade as normal. Examples: `sync blocked — re-entry required`, `local only`, `reconciliation required`, `remote status unknown`.

Guards:
- `fail closed ≠ make all local data inaccessible`;
- `graceful degradation ≠ silent stale behavior`;
- `error hidden ≠ graceful recovery`.

## 7. PWA/browser mechanics constrain graceful degradation

The current W3C Service Workers Candidate Recommendation Draft (2026-08-12) retains the event-driven worker model, install/activate lifecycle and fetch interception used for offline-enabled applications. A worker can be terminated when it has no event to handle; therefore product correctness cannot assume a continuously running background process.

Source checked 2026-09-18:
- https://www.w3.org/TR/service-workers/

**TRACK A TRANSFER:** degraded-mode guarantees must be based on durable state and explicit lifecycle transitions, not on an assumed resident background daemon. Offline shell/read capability and later remote reconciliation are separate claims.

**CHANGE WATCH:** browser/WebKit implementation and OS policy remain platform-specific; managed-iPad background/update behavior is not inferred from the standard.

## 8. EFB/LogMate-like state model

A useful generic state model is capability-oriented rather than one global connectivity badge:

- **LOCAL-READY:** locally validated data/functions available; no remote-state claim.
- **LOCAL-UNSYNCED:** local work exists that has not received remote acknowledgement.
- **REMOTE-UNREACHABLE:** origin/API unavailable; local capability may continue.
- **REENTRY-REQUIRED:** network exists but client/session/trust generation is not current enough for remote authority.
- **RECONCILIATION-REQUIRED:** queued/local data exists but cannot safely mutate remote state until conflict/provenance checks complete.
- **REMOTE-READ-ONLY:** current remote reads may be allowed while writes remain blocked, if product architecture validates this distinction.
- **NORMAL:** current trust, supported client/API generation and required reconciliation gates satisfied.
- **UNKNOWN:** evidence insufficient; do not map UNKNOWN to NORMAL.

These are generic design states, not confirmed LogMate implementation states.

## 9. Queuing is not synchronization

A degraded client may accept local work, but the UI and data model must distinguish:
- saved locally;
- queued for later;
- transmitted;
- acknowledged remotely;
- reconciled;
- authoritative/current.

A local queue should not create an implicit promise that every operation will later be replayed. Operations may become invalid after credential expiry, schema change, conflict, incident containment or client retirement.

Guards:
- `queued ≠ sent ≠ acknowledged ≠ reconciled`;
- `captured offline ≠ guaranteed future remote mutation`;
- `network returns ≠ queue replay automatically safe`.

## 10. Update/recovery conflict

Fast recovery may tempt forced Service Worker activation, cache purge or schema migration. Those actions can conflict with local data preservation or an in-progress user task.

Generic direction:
- separate executable/cache cleanup from irreplaceable domain-data deletion;
- treat schema migration as a data operation with compatibility/recovery evidence;
- do not claim installed-client convergence because a clean worker is published;
- where old clients retain local recovery value, block unsupported remote authority rather than destroy local records solely to enforce software currency.

Guards:
- `new worker available ≠ safe immediate activation for every client`;
- `cache cleanup ≠ domain-data cleanup`;
- `client unsupported for remote write ≠ client data should be destroyed`.

## 11. UX truthfulness requirements — Track B transfer

Partial recovery should communicate **what works, what does not, why at a useful level, and what happens to user work**. Avoid generic `Online`, `Synced`, `Recovered`, or green-health language when only one layer is healthy.

For consequential states, expose distinctions such as:
- local vs remote;
- saved vs synced;
- read vs write;
- current vs stale/unknown;
- automatic retry vs user action required;
- recoverable/exportable vs authoritative.

Accessibility requirements apply to degraded states too: state must not depend on color alone; focus/order and status announcements require runtime validation. Design Studio W080 remains Stage 3 PRACTICE / NOT PASSED, so no human/AT/browser PASS is transferred.

## 12. Recovery normalization gate

Do not exit degraded mode merely because network/API health returns. NORMAL requires the claims relevant to the capability, potentially including:
1. current supported client/worker generation;
2. current session/credential/trust generation;
3. policy/schema compatibility;
4. local-data migration success where required;
5. queued-operation classification;
6. conflict/provenance reconciliation;
7. remote negative authorization canary for stale/revoked paths;
8. user-visible state transition consistency;
9. no remaining emergency bypass that silently broadens authority.

Guard: `network healthy ≠ degraded mode exit criteria satisfied`.

## 13. Track C validation campaign

1. origin outage preserves declared local read capability;
2. offline launch does not imply remote freshness;
3. local save is visibly distinct from remote acknowledgement;
4. reconnect does not auto-replay quarantined operations;
5. stale client is denied remote write while local recovery remains available where designed;
6. revoked credential remains denied under RTO pressure;
7. remote read-only mode cannot mutate through alternate endpoints;
8. destructive operations fail closed when authority is uncertain;
9. UNKNOWN state never renders as NORMAL;
10. queued operation invalidated by schema change fails visibly;
11. conflict requires reconciliation rather than last-writer surprise;
12. Service Worker update does not erase domain data;
13. failed migration preserves recoverable pre-migration data;
14. clean origin does not mark offline clients converged;
15. local-only state survives worker restart/termination assumptions;
16. degraded state is keyboard reachable and non-color-only;
17. status transition is exposed to assistive technology in product validation;
18. recovery export works without granting remote mutation;
19. sync resumes only after current trust/API gate;
20. compromise-era outbox remains quarantined after fresh login;
21. RTO measurement records which capabilities recovered, not only `app up`;
22. RPO measurement separates central and device-local unsynced data;
23. telemetry outage does not erase degraded-state population from risk register;
24. forced worker activation cannot bypass migration prerequisite;
25. rollback cannot reactivate retired remote authority;
26. emergency availability bypass expires without converting to permanent authority;
27. local storage failure is distinct from network outage;
28. authentication recovery is distinct from data/provenance recovery;
29. recovery normalization requires negative stale-path tests;
30. partial-recovery messaging matches actual capability matrix.

## 14. Track D measurement boundary

Useful metrics may include time spent in degraded states, transition success/failure, queue age, reconciliation outcomes and recovery completion by capability. But analytics absence is weak evidence for offline/blocked clients, and measurement code itself can fail during incidents.

Guards:
- `no degraded-state events ≠ no degraded clients`;
- `dashboard green ≠ capability matrix normal`.

## 15. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-18: **W080 RESET-BASELINE + NAVIGATION CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Its current evidence reinforces explicit state/provenance and accessibility payload requirements, but cross-browser/Safari/Firefox, persisted configuration, screen-reader, physical-device, field-CWV and human UX evidence remain OPEN.

Software Engineering owns implementation mechanics for persistence, state machines, synchronization and tests. Web Manager supplies web/PWA capability and assurance requirements; implementation evidence must be returned before product claims are promoted. Marketing may consume reliability language only after operational evidence supports it.

## 16. MINTTAP DIRECTION

For PWA/EFB-like products, define recovery objectives per capability rather than one global uptime target. Prefer **local usefulness + explicit unsynced/recovery state + fail-closed remote authority** over either extreme of `everything disabled offline` or `everything replayed when network returns`.

Do not invent actual LogMate safety, regulatory, MDM, storage or sync guarantees. Those remain product/runtime validation questions.

## 17. OPEN / VALIDATION / CHANGE WATCH

**OPEN:** actual critical capabilities, safety/legal consequence, authoritative data model, allowed offline edits, conflict policy, local encryption/session behavior, managed-iPad/WebKit/MDM behavior, supported worker/API generations, user-data durability and actual RTO/RPO/MTD.

**VALIDATION:** physical iPad/WebKit lifecycle; storage/eviction; worker update/activation; offline capture/read/export; reconnect/reconciliation; stale-client denial; accessibility of partial states; destructive recovery drills.

**CHANGE WATCH:** W3C Service Workers; WebKit/iOS/iPadOS PWA capability; Chromium-specific PWA behavior; browser storage/background policy; project architecture; applicable aviation/company policy.

## 18. Persistent guards

`degraded operation ≠ weakened authority by default`.  
`screen available ≠ capability safely recovered`.  
`application available ≠ every capability available`.  
`RTO pressure ≠ authorization bypass justification`.  
`availability restored ≠ integrity restored ≠ authority restored`.  
`fail closed ≠ make all local data inaccessible`.  
`graceful degradation ≠ silent stale behavior`.  
`queued ≠ sent ≠ acknowledged ≠ reconciled`.  
`network returns ≠ queue replay automatically safe`.  
`new worker available ≠ safe immediate activation for every client`.  
`client unsupported for remote write ≠ client data should be destroyed`.  
`network healthy ≠ degraded mode exit criteria satisfied`.  
`UNKNOWN ≠ NORMAL`.

## Gate

**PASS (generic).** The Web Manager can now resolve recovery-objective conflicts by capability, distinguish fail-closed from safe degradation and visible failure, define PWA partial-recovery states, and prevent availability targets from silently restoring stale remote authority. Product/managed-iPad/safety/legal validation remains OPEN.

## Next high-value adjacent work

**PWA degraded-mode convergence & split-brain reconciliation governance:** determine how independently degraded clients rejoin after long offline periods without treating last-writer-wins, fresh login, network restoration or newest timestamp as sufficient conflict resolution; separate domain-record conflict, operation identity/idempotency, provenance, tombstones/deletion and user-mediated reconciliation while keeping direct device-to-device assumptions OPEN.