# 176 — PWA Degraded-Mode SLO, Error-Budget, Brownout Admission & Recovery-Proof Governance

Status: **PASS (generic) / PRODUCT + BIA + SLO + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A platform/runtime state; Track B degraded/recovery UX semantics; Track C SLI/SLO and destructive validation; Track D privacy-bounded measurement.  
Dependencies: 173–175 trust-policy convergence, consequence-specific availability, dependency isolation and degraded-mode observability.

## Why this study exists

175 established that dependency failure must be isolated and that generic green health cannot prove authorization safety. The next governance failure is incentive inversion: an availability SLO or exhausted error budget can pressure operators to reopen a capability before current security authority is established, or a temporary brownout exception can quietly become normal operating policy.

Central rule:

> **Reliability objectives measure whether intended capability is delivered; they do not authorize bypassing security floors. Brownout and recovery are explicit capability-admission states whose opening and closing require evidence, ownership, expiry and review.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Owns observable browser/network/SW/storage states and reminds consumers that online/offline or cached/not-cached is not an authorization state.
- **B UX/IA/Content:** owns user-facing semantics for preserved local work, paused submission, degraded remote read, recovery checking and review-required states; does not expose infrastructure jargon as the primary explanation.
- **C Performance/Accessibility/Quality:** owns SLI fitness, denominator/failure-class critique, burn-rate interpretation, brownout/recovery destructive testing and accessible state communication.
- **D Search/Analytics:** bounded consumer. Reliability measurement must not turn outage/SLO telemetry into durable identity, acquisition or behavioral profiles.
- **E Security/Operations:** **bottleneck/owner**. Owns consequence-class objectives, error-budget governance, security-floor precedence, brownout admission, exception lifecycle and recovery-proof requirements.

## SOURCE

### Google SRE — SLOs and error budgets

Google SRE defines an SLO as a target value or range for a service-level indicator and recommends beginning from what users care about rather than what is easiest to measure. It explicitly treats target selection as a product/business decision, not a purely technical one. Error budgets are derived from the SLO and are used to balance reliability with change velocity.

Sources:
- https://sre.google/sre-book/service-level-objectives/
- https://sre.google/workbook/implementing-slos/
- https://sre.google/sre-book/embracing-risk/

Transfer: generic Web Manager research can define objective structure and governance but cannot invent MintTap/LogMate percentages or windows without actual user-impact/BIA evidence.

### Google SRE — example error-budget policy

Google's published example policy halts ordinary changes when the error budget is exhausted while still allowing urgent security fixes and reliability work. It also treats an error-budget policy as an agreed decision mechanism rather than a punishment.

Source: https://sre.google/workbook/error-budget-policy/

Transfer: availability pressure must not suppress security correction. A spent availability budget is not authority to fail open stale federation or authorization state.

### NIST Cybersecurity Framework 2.0 / ERM integration

NIST CSF 2.0 added explicit `GOVERN` emphasis and frames cybersecurity as enterprise risk that must be prioritized and communicated alongside other organizational risks. NIST SP 1303 connects CSF outcomes to enterprise risk monitoring, evaluation and adjustment.

Sources:
- https://www.nist.gov/cyberframework
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-enterprise-risk-management-quick-start-guide

Transfer: a temporary reliability/security tradeoff requires explicit risk ownership and governance; it must not emerge implicitly from an availability dashboard.

### NIST SP 800-53 Rev. 5 / Release 5.2.0

NIST's current control catalog remains the risk-based control baseline. Availability, monitoring, contingency, incident and security-control requirements coexist; availability is not a blanket override for access-control or integrity requirements.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### RFC 9110 — 503 / Retry-After

HTTP 503 represents temporary inability to handle a request, and `Retry-After` can suggest when a client should retry. It does not prove that an authorization dependency or security floor is current after that delay.

Source: https://www.rfc-editor.org/rfc/rfc9110.html

## SYNTHESIS — SLOs are consequence-specific, not one uptime number

A PWA with offline utility has materially different capability classes. A single site-uptime SLO can hide both useful local continuity and unsafe remote admission.

Generic objective families should be separated at least into:
1. **local-preservation objective** — can unique local work be saved/recovered/exported where product policy permits?;
2. **read-availability objective** — can authorized remote information be retrieved?;
3. **mutation-admission objective** — can consequence-bearing operations receive current authoritative admission?;
4. **authority-currentness objective** — is the security/policy floor current enough for the consequence class?;
5. **reconciliation objective** — after outage/reconnect, does queued work converge without stale-authority replay or silent loss?;
6. **recovery-proof objective** — after reopening, is actual consequence-path admission current across the controlled enforcement domain?;
7. **accessibility objective** — can users perceive and operate degraded/recovery states without color-only, pointer-only or inaccessible authentication/recovery paths?

These objectives can share evidence, but they are not interchangeable.

Persistent guards:
- `SLO met ≠ security floor met`;
- `error budget remaining ≠ permission to weaken authorization`;
- `error budget exhausted ≠ permission to bypass a failed dependency`;
- `availability restored ≠ consequence admission safe`;
- `brownout active ≠ incident resolved`;
- `temporary exception approved ≠ permanent policy changed`;
- `exception expired ≠ system automatically safe`;
- `low burn rate ≠ current authority proven`;
- `503 ended ≠ currentness restored`;
- `queue draining ≠ recovery proven`;
- `client success telemetry ≠ controlled-domain enforcement proof`;
- `local work preserved ≠ remote mutation available`.

## Error-budget semantics with security floors

An error budget is a reliability-management mechanism. It answers how much failure against an agreed SLO is tolerable over a window and can govern release/change priorities. It does **not** answer whether an actor is authorized, a trust anchor is current, or stale federation evidence may be accepted.

Generic precedence:
1. legal/safety/product hard constraints where verified;
2. current security/authority floor for the consequence class;
3. data-integrity and unique-local-data preservation requirements;
4. capability-specific reliability objectives/error budgets;
5. feature/change velocity.

This ordering is not a claim about unknown LogMate aviation obligations; those remain OPEN. It is a governance rule that a reliability metric cannot silently redefine an authorization invariant.

If an SLO is impossible to meet without bypassing a security invariant, the response is to revisit architecture, dependency resilience, product expectations or the SLO—not to redefine stale authority as success.

## Brownout as explicit capability admission

`Brownout` here means an intentional temporary reduction in capability to preserve safer/more important functions under dependency or capacity stress. It is not a standards term and must not be confused with authorization.

A brownout declaration should identify:
- affected capability classes;
- consequence level and what remains allowed/paused;
- trigger evidence and reason class;
- security-floor generation/currentness requirement;
- owner/approver appropriate to risk;
- start time and bounded review/expiry point;
- rollback/reopen criteria;
- user-visible semantic state;
- observability/evidence requirements;
- queued-work treatment;
- post-event review when material.

Examples of generic brownout behavior:
- preserve app shell/help/local draft while remote mutation is paused;
- preserve current-authority and reconciliation capacity while shedding analytics/background refresh;
- allow low-risk static/read surfaces only if their disclosure policy does not require unavailable current admission;
- quarantine stale queued consequences rather than count automatic replay as availability success.

## Temporary exception governance

A security-affecting exception must not be represented merely as `brownout=false` or an undocumented operator toggle. At minimum, model:
- invariant being relaxed, if relaxation is even permissible;
- exact scope/capability/tenant or environment boundary where applicable;
- reason and evidence;
- accountable approver;
- start and hard expiry/review time;
- compensating controls;
- telemetry/validation;
- revocation path;
- residual-risk record;
- post-expiry reconciliation.

**MINTTAP DECISION:** generic Web Manager guidance does not pre-authorize stale-authority exceptions. For remote consequence-bearing operations, current authoritative admission remains the default requirement. Any real exception requires product/security/legal/operational evidence and explicit approval in the actual system context.

## Recovery-proof governance

Reopening a capability requires more than endpoint recovery or an improving SLO. Generic recovery proof should progress through:
1. transport/dependency reachability;
2. current security-floor/trust-policy acquisition;
3. region/service admission of that floor;
4. actual authorization/enforcement checks for the capability class;
5. queue/reconciliation validation against current actor/delegation/policy/schema state;
6. bounded progressive reopen;
7. relapse detection and ability to re-enter brownout;
8. evidence that user-visible state matches actual capability;
9. explicit closure or continued exception ownership.

No universal numeric threshold is asserted. Actual reopening thresholds depend on topology, consequence, traffic, BIA/SLO and product evidence.

## SLI design failure modes

### Easy-to-measure denominator

Counting all HTTP 2xx responses can label a static shell healthy while submission is unavailable. Conversely, counting deliberately paused high-consequence mutations as ordinary server failures can obscure that the system is preserving security correctly.

Direction: define SLIs around intended user/capability outcomes and preserve reason classes. Do not game the denominator by excluding inconvenient failures without governance.

### Security-preserving refusal counted as success

A blocked stale-authority mutation is security-correct but not necessarily reliability-successful from the user's task perspective.

Direction: preserve two dimensions: `admission correctness` and `task availability`. A secure refusal can PASS the former and MISS the latter. This prevents pressure to convert secure refusal into unsafe success.

### Local continuity hidden by remote outage

An offline-first PWA can remain valuable while remote sync is unavailable.

Direction: local preservation/draft utility and remote sync/admission need separate indicators.

### Error-budget gaming through brownout

Disabling a failing feature can improve aggregate success ratios while materially reducing product utility.

Direction: brownout duration/scope is itself evidence and should not disappear from reliability reporting. SLO definitions must state whether intentionally unavailable capability counts against the relevant objective.

### Unknown telemetry treated as success

Monitoring outage or sampling gaps can create an artificially healthy budget.

Direction: `UNKNOWN` remains explicit. Error-budget arithmetic must document missing-evidence handling; generic research does not prescribe one universal formula.

## PWA / managed-iPad transfer

For a LogMate-like company iPad scenario:
- offline local save can remain available even while federation/current-authority SLO is missing;
- local continuity must not be counted as proof that sync or delegated remote mutation is available;
- reconnect does not immediately consume queued work merely to improve availability metrics;
- Service Worker/app-shell success is not a mutation-admission SLI;
- physical iPad/Safari/Home Screen storage, background, network-transition and MDM behavior remain OPEN;
- unique unsynced flight/logbook data should not be destroyed because a remote reliability/security objective is missed;
- actual aviation consequence classes and acceptable objectives require canonical product/legal evidence.

## UX transfer — Track B

Brownout/recovery UX should communicate what the user can do now and what remains pending, not a numeric SLO or internal dependency graph. Required semantic distinctions include:
- local work saved vs not yet synchronized;
- remote submission paused vs failed permanently;
- connection restored vs submission still being rechecked;
- queued item awaiting authority/conflict review;
- capability reopened vs some operations still restricted.

State changes must be perceivable without color alone and validated for keyboard/screen-reader/human comprehension. Design Studio remains canonical for reusable visual/interaction treatment.

## D / privacy transfer

SLO and brownout telemetry should prefer capability, reason class, region/service, generation, aggregate latency/error/backlog and bounded recovery-state dimensions. Do not make per-user outage history, raw federation claims, tokens, flight payloads or stable device fingerprints routine reliability dimensions. Incident evidence requiring more detail belongs to a separate purpose/access/retention regime.

## MINTTAP DECISION — generic governance

1. Define SLOs by user-relevant capability/consequence class, not one site uptime number.
2. Keep security-floor/current-authority invariants outside the error-budget spending mechanism; error budgets cannot authorize stale trust.
3. Preserve separate indicators for admission correctness and user task availability.
4. Treat intentional brownout as a first-class operational state with scope, owner, evidence, expiry/review, UX and reopen criteria.
5. Do not hide brownout scope/duration by denominator manipulation.
6. Treat temporary security-affecting exceptions as explicit governed risk records, not undocumented toggles; no generic stale-authority exception is pre-approved.
7. Reopen consequence-bearing capability only after current floor, enforcement and reconciliation evidence—not merely endpoint health or improving SLO.
8. Preserve `UNKNOWN` when evidence is absent/lagging; do not silently count it healthy.
9. Keep local PWA data-preservation utility separate from remote authorization availability.
10. Numeric SLOs, error budgets, burn thresholds, exception authority and recovery thresholds remain OPEN until actual BIA/product/provider/runtime evidence exists.

## VALIDATION — 168-case destructive campaign

Families include: incorrect SLI denominator; static-shell green/submit red; local-save green/sync red; secure stale-authority refusal; refusal miscounted as success/failure; error-budget exhaustion; security fix during freeze; brownout entry/exit race; operator toggle without expiry; expired exception still active; compensating control failure; stale policy/JWKS/issuer; partial-region recovery; false-green synthetic probe; telemetry outage/lag/sampling; unknown counted healthy; deliberate capability shedding hidden from SLO; queue depth improvement with invalid work; retry/reconnect storm; progressive reopen relapse; PITR rollback; stale SW/IndexedDB; long-offline iPad; Shared iPad/account switch; inaccessible status/recovery UI; color-only state; screen-reader announcement; user misunderstanding; incident close with active exception; exception renewal normalization; audit/provenance loss; privacy-heavy reliability telemetry; security-floor generation mismatch; provider recovery without local enforcement; physical Safari/Home Screen/MDM transfer.

Generic campaign definition is PASS. Product/runtime/device/human execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION

- **TRANSFER VALIDATION:** 174 consequence-specific availability supplies the capability classes; 175 isolation/observability supplies the evidence boundary.
- **TRANSFER VALIDATION:** Google SRE supports SLO/error-budget use as an agreed reliability/change decision mechanism and explicitly permits security fixes when an example policy freezes ordinary changes.
- **TRANSFER VALIDATION:** NIST CSF 2.0 governance supports treating cybersecurity tradeoffs as explicit organizational risk decisions rather than hidden availability optimizations.
- **CONTRADICTION:** `we are missing the availability SLO, therefore accept stale authorization` is rejected.
- **CONTRADICTION:** `brownout improved the success ratio, therefore reliability improved` is rejected unless reduced capability is represented in the objective.
- **CONTRADICTION:** `exception was approved once, therefore it is part of normal policy` is rejected.
- **CONTRADICTION:** `endpoint recovered and burn rate fell, therefore queued consequences may drain` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate BIA, user-critical journeys, capability consequence classes, SLI definitions, numeric SLOs/windows/error budgets/burn thresholds, SLA obligations, provider dependencies, exception authority, security floors, telemetry completeness, region topology, queue semantics, managed-iPad/MDM, Safari/Home Screen runtime, aviation/legal requirements and human/AT evidence.

DEPENDENCY — Software Engineering: instrument consequence-specific SLIs; implement brownout/admission gates, expiry-safe configuration, current-floor checks, progressive reopen, queue quarantine/re-admission and relapse controls; provide runtime evidence rather than generic pattern claims.

DEPENDENCY — Design Studio: consume degraded/recovery semantic requirements and validate accessible user comprehension. Current Web Design evidence remains Stage 3 PRACTICE / NOT PASSED with physical-device/PWA, screen-reader and human evidence OPEN.

CHANGE WATCH: NIST control/CSF guidance; provider/federation behavior; Safari/iPadOS PWA runtime; SRE practices are engineering guidance rather than Web standards and must not be misrepresented as normative requirements.

## Gate

**176 PASS (generic).** The Web Manager can now distinguish reliability objectives from authorization invariants; structure capability-specific SLO/error-budget semantics without inventing product numbers; model brownout and exceptions as governed states; detect denominator/error-budget gaming; and require evidence-based progressive reopening that preserves offline-first local utility without normalizing stale-authority fail-open.

Next adjacent bottleneck: **PWA exception/waiver debt, configuration provenance & automated expiry enforcement** — determine how temporary brownout/security exceptions are represented, signed/authorized, propagated, expired and audited across regions/offline clients without turning the exception registry into either a permanent bypass catalog or a privacy-heavy dossier.