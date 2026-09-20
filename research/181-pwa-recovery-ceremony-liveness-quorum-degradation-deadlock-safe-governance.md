# 181 — PWA Recovery-Ceremony Liveness, Quorum Degradation & Deadlock-Safe Governance

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + ORGANIZATIONAL + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A reconnect/session/offline-state mechanics; Track B recovery-pending/degraded UX; Track C destructive liveness validation; Track D privacy-bounded readiness telemetry.
Dependencies: 176–180 brownout/exception governance, break-glass assurance, trust reconstitution, recovery-root survivability and organizational succession.

## Problem
180 established that recovery must survive personnel/provider/organizational loss without converting continuity into unilateral takeover. The adjacent failure is deadlock: a ceremony may be secure on paper yet impossible to complete because required participants, providers, evidence or communication channels are unavailable.

The unsafe shortcut is to interpret elapsed time or business pressure as permission to reduce authority requirements ad hoc. The opposite failure is permanent lockout because the only recovery policy assumes every original participant survives.

Central rule:

> **Recovery liveness must be designed before disruption as a governed set of alternate paths and eligibility transitions. Timeout, outage duration, backlog or operational urgency may trigger escalation/reassessment, but do not themselves create authority or lower an approval threshold. A degraded quorum is legitimate only when a pre-authorized/current policy independently defines how eligibility changes and preserves the intended independence/failure-domain constraints.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser timers, cached policy, local clocks, Service Worker/IndexedDB state and reconnect cannot decide quorum legitimacy. Preserve local work while server authority is unresolved.
- **B UX/IA/Content:** high-pressure consumer. Distinguish `recovery pending`, `additional authority unavailable`, `local work preserved`, `remote privileged action paused`, `recovery path changed under current policy`, and `current authority restored` without exposing sensitive topology.
- **C Performance/Accessibility/Quality:** high-pressure validator. Test participant loss, delayed/duplicate approvals, policy-version races, provider partitions, inaccessible ceremony UI, long-offline clients and false liveness.
- **D Search/Discovery/Analytics:** bounded consumer. Aggregate ceremony readiness/liveness without retaining unnecessary custodian identity, approval graph, secret location or incident dossier data.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns liveness invariants, alternate recovery paths, quorum-policy generations, deadlock handling, escalation boundaries, anti-takeover controls and convergence proof.

## SOURCE
### NIST SP 800-34 Rev. 1 — personnel unavailability and alternate teams
NIST contingency guidance explicitly anticipates that disruptions can make personnel unavailable. It recommends teams large enough to remain viable, alternates for team leaders, and where necessary trained personnel from another geographic area or contractors/vendors. It also treats recovery/reconstitution and testing as planned capabilities rather than improvised incident-time shortcuts.
Sources:
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf
- https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning

**TRANSFER VALIDATION:** this supports preplanned alternate staffing and exercises. It does not prescribe a cryptographic or organizational quorum for MintTap/LogMate.

### NIST SP 800-53 Rev. 5 / Release 5.2.0 — contingency, separation and controlled change
The current SP 800-53 family includes contingency planning/training/testing and access-control/separation-of-duties concepts. Recovery governance must remain a controlled policy decision rather than an incident-time bypass.
Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**BOUNDARY:** control catalogs establish objectives; they do not supply a product-specific `k-of-n`, custodian roster or emergency threshold.

### CISA cloud emergency-access guidance
CISA recommends least privilege, separation of duties, protected break-glass accounts, consideration of coordination among multiple users, and extensive logging/auditing while recognizing that privileged administrators may interfere with evidence.
Source: https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

**TRANSFER VALIDATION:** emergency availability and multi-party coordination are compatible, but availability pressure is not evidence that one actor may redefine the recovery policy.

## SYNTHESIS — liveness is not authority weakening
Keep separate:
1. **availability of participants/resources** — who/what can respond now;
2. **eligibility** — who/what current policy permits to participate;
3. **threshold/quorum rule** — what combination is sufficient;
4. **independence constraint** — whether participants actually span required failure/authority domains;
5. **escalation state** — whether an alternate pre-authorized path may be evaluated;
6. **successor policy generation** — a governed policy change, not an ad hoc threshold edit;
7. **runtime admission** — whether the new authority is actually enforced;
8. **client observation** — never the oracle for quorum legitimacy.

Persistent guards:
- `quorum unavailable ≠ quorum may be lowered`;
- `timeout elapsed ≠ authority expanded`;
- `business urgency ≠ approval independence waived`;
- `two approvals ≠ two independent failure domains`;
- `alternate custodian exists ≠ alternate custodian currently eligible`;
- `policy administrator reachable ≠ administrator may self-authorize recovery`;
- `old policy cached ≠ old policy executable`;
- `ceremony making progress ≠ successor authority legitimate`;
- `deadlock avoided ≠ takeover resistance preserved`;
- `remote recovery blocked ≠ local operational work must be destroyed`.

## Deadlock-safe governance model
A robust recovery design should pre-establish **alternate paths**, not an incident-time `lower threshold` button. Generic forms may include alternate eligible classes, independent recovery authorities, organizational succession procedures, provider-independent evidence or separately governed policy-reconstitution paths. This study deliberately does not prescribe the mechanism.

Requirements:
- enumerate credible participant/provider/site/identity loss combinations before production reliance;
- define which loss combinations remain recoverable and which intentionally require manual/legal/security intervention;
- ensure an alternate path has its own current eligibility and independence checks;
- prevent the same actor from declaring deadlock, changing the threshold, approving itself and exercising the resulting authority unless that concentration is explicitly accepted by real governance;
- bind every ceremony to a policy generation/currentness floor;
- preserve UNKNOWN when current policy/roster/independence cannot be established;
- make policy changes forward-moving generations with rollback/PITR resistance;
- test exhaustion cases where no legitimate quorum exists. Safe non-completion is preferable to silent unilateral takeover.

## Timeout and escalation semantics
Timeout is an operational signal, not an authorization primitive.

A timeout may:
- page/escalate to another already-authorized recovery path;
- request fresh evidence/currentness;
- mark a ceremony stalled;
- activate a separately governed continuity process;
- change user-visible degraded-state messaging.

A timeout must not by itself:
- add an approver;
- reduce a threshold;
- waive independence;
- reactivate an expired/revoked participant;
- convert cached/offline approval into current approval;
- authorize queue drain.

If prolonged disruption requires a policy change, treat it as a **new policy/recovery generation** with its own authority, evidence, distribution, expiry/review and post-event validation.

## Partial quorum and participant replacement
Participant replacement is an eligibility transition, not identity substitution.

- same job title/email alias/device does not inherit predecessor approval;
- replacement must be established under current policy;
- approvals from a superseded participant are re-evaluated according to actual ceremony semantics rather than blindly counted;
- duplicate/replayed approvals do not increase independence;
- a participant who changes failure domain mid-ceremony may require re-evaluation;
- stale roster or provider directory data is evidence input, not authority truth.

No generic numeric quorum is selected. The correct threshold depends on actual consequences, organization, cryptographic design, provider topology and legal obligations.

## Policy-change deadlock
A special circular failure occurs when the only authority allowed to change recovery policy is the unavailable quorum itself.

Generic resolution principle: **policy-reconstitution authority must be designed as a separate governed continuity capability if the organization requires survival of quorum loss.** It cannot be improvised after the quorum is lost. This may intentionally be harder/slower than ordinary recovery.

If no such path was pre-established, the generic safe result is not to invent one. Preserve local/read/export capability where safe, suspend privileged remote consequences, and escalate to real organizational/security/legal decision-making.

## PWA / EFB transfer
For a LogMate-like company-iPad PWA:
- offline flight/logbook records and drafts remain locally useful while recovery quorum is unresolved;
- cached Service Worker/IndexedDB/cookies cannot vote, lower a threshold or prove current recovery policy;
- a client clock timeout cannot activate emergency authority;
- reconnect must obtain current server security/recovery generation before privileged queue drain;
- queued work authored while an old quorum was valid is not grandfathered if authority changed before commit;
- application/SW/schema update and authority reconstitution remain separate state machines;
- no generic claim is made that iPadOS background execution, push, MDM, Shared iPad or hotspot/network behavior can propagate quorum changes. Physical Safari/Home Screen/managed-device validation remains OPEN.

## UX transfer — Track B
Required user/operator semantics:
- `Recovery is still in progress; remote privileged actions are paused.`
- `Your local work remains saved on this device.`
- `Additional authorized recovery participation is required.`
- `A current recovery path has been established; pending actions will be checked before submission.`

Do not expose exact custodian counts, identities, secret locations or failure topology to ordinary users. Do not use a countdown implying that authority automatically weakens at zero. Accessibility, screen-reader, focus, non-color status and representative-human comprehension remain OPEN.

## Track C destructive campaign
Define a **208-case generic campaign** across:
- one/two/multiple required participants unavailable;
- primary and alternate leader unavailable;
- alternate exists but eligibility expired;
- participant replaced mid-ceremony;
- same alias/new human confusion;
- two accounts controlled by one human/admin/IdP;
- quorum met numerically but independence lost;
- delayed, duplicated and replayed approvals;
- approval arrives after revocation;
- timeout before/after approval;
- operator repeatedly extends timeout;
- policy administrator self-adds;
- policy-change authority shares failed quorum;
- stale roster and stale policy generation;
- policy rollback/PITR resurrects easier threshold;
- split-region quorum policy;
- provider/IdP/evidence-store outage combinations;
- false-green liveness dashboard;
- ceremony progresses under wrong generation;
- successor authority created but not enforced everywhere;
- long-offline iPad crosses policy generations;
- client clock skew/tampering;
- stale SW/IndexedDB displays obsolete recovery state;
- reconnect queue drains before current authority;
- local flight data deleted because remote recovery is blocked;
- inaccessible recovery status/action;
- screen-reader ambiguity;
- human mistakes timeout for automatic authorization;
- recovery succeeds but alternate capacity is not replenished/retested.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat recovery liveness and authorization strength as separate requirements.
2. Pre-establish alternate recovery paths where continuity requires them; do not improvise threshold reduction during an incident.
3. Treat timeout as escalation/reassessment evidence only, never as authority creation.
4. Bind ceremony, roster, threshold and independence rules to current policy generations with rollback resistance.
5. Evaluate quorum legitimacy by current eligibility and failure-domain independence, not raw approval count.
6. Treat participant replacement as a new eligibility event; do not inherit predecessor approvals/credentials automatically.
7. Separate recovery-policy reconstitution from ordinary recovery when survival of quorum loss is required.
8. Permit safe non-completion when no legitimate recovery path exists rather than silently enabling unilateral takeover.
9. Preserve unique local PWA/EFB work during deadlock while consequence-bearing remote operations remain paused.
10. Re-admit queued operations only after current server authority is established.
11. Keep telemetry privacy-bounded and avoid exposing recovery topology.
12. Do not select product quorum numbers, timeout durations or implementation mechanisms without canonical product/security/organizational evidence.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate recovery roles, quorum, provider, IdP, legal entity, policy administrator and consequence classes: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad/offline runtime: **OPEN**.
- Exact server-side admission, policy-generation, clock/currentness, queue and rollback implementation: **Software Engineering/security dependency**.
- Legal/aviation/investment requirements for organizational succession or record submission: **OPEN**.
- Screen-reader/representative-human recovery comprehension: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## Adjacent next target
Highest-value adjacent Stage-8/PWA question: **recovery-policy reconstitution authority, governance-key rotation & constitutional change control** — how the rules that define quorum/eligibility can themselves evolve, recover from compromise or organizational change, and resist both permanent deadlock and self-authorized weakening across multi-region/offline clients.