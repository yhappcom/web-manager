# 263 — PWA Topology-Change Authorization, Shadow-Consumer Admission & Discovery-to-Governance Closure

Status: **PASS (generic) / PRODUCT + DATA-MODEL + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/discovery mechanics; Track B uncertainty/exception UX; Track C destructive validation; Track D bounded drift measurement.  
Dependencies: 241–262, especially topology recovery, hidden-edge discovery, consequence-scoped completeness, inventory drift and independent challenge.

## Problem
262 established that inventories and discovery controls are evidence rather than reality. The next boundary is governance: discovery can reveal a previously unknown consumer, route, queue, export path, offline device or manual handoff, but observation does not answer whether that node is authorized, who owns it, what consequences it may carry, how long it may exist, or how it retires.

A dangerous system can normalize every observed dependency into the canonical topology and thereby let discovery become an authorization oracle. The opposite failure is to destroy or disconnect every undeclared dependency immediately, potentially losing unique offline data or interrupting a legitimate emergency path before classification.

Central rule: **discovery creates a governance obligation, not authority. A newly observed dependency remains classified and bounded until an authorized decision establishes ownership, allowed consequences, lifecycle and retirement/review rules. Observation, use, historical success and emergency necessity are evidence; none independently grants durable topology membership.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Identifies browser/PWA surfaces that can appear dynamically or remain offline; runtime presence does not authorize them.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `unclassified`, `quarantined`, `temporary exception`, `safe to inspect`, `mutation blocked` and `retirement pending` states; human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **856 → 864 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer. Can reveal shadow consumers and measure exception age/drift, but cannot convert observed traffic into authorization.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns admission, exception, ownership, consequence classification, lifecycle, review and retirement governance.

## SOURCE

### NIST SP 800-53 Rev. 5 / Release 5.2.0 — configuration changes require controlled authorization
CM-3 Configuration Change Control requires changes to be reviewed/approved, documented, and controlled. CM-3(1) includes mechanisms to document proposed changes, notify approval authorities, prohibit changes until required approvals are received, document completed changes and notify designated personnel. CM-4 addresses impact analysis; CM-5 addresses restrictions on who may make changes.

Sources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final  
https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

**TRANSFER VALIDATION:** bounded precedent that discovered or proposed topology change should not self-authorize merely because it exists. It does not define a LogMate consumer-admission workflow.

### NIST SP 800-53 CM-8 — inventory and unauthorized-component detection are distinct from authorization
CM-8 requires maintained component inventories; enhancements address automated maintenance and detection of unauthorized components. The control family separates knowing what exists from deciding what is permitted.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** supports `observed component ≠ authorized component`. It does not imply every web/PWA dependency is literally a CM-8 system component.

### NIST CSF 2.0 — authorized flows and lifecycle management
CSF 2.0 ID.AM includes maintained inventories of systems/services, representations of authorized internal/external network communications and data flows, supplier services, prioritization by criticality/impact, and lifecycle management.

Source: https://www.nist.gov/cyberframework

**TRANSFER VALIDATION:** supports explicit authorized-flow and lifecycle distinctions. It does not prescribe product-specific topology admission.

### NIST configuration-control definition
NIST defines configuration control as controlling modifications before, during and after implementation to protect against improper modification.

Source: https://csrc.nist.gov/glossary/term/configuration_control

**TRANSFER VALIDATION:** reinforces that after-the-fact discovery still requires governance; successful execution is not retroactive approval.

## SYNTHESIS 1 — discovery and authorization are separate state machines
A newly observed node/edge should enter a state such as `DISCOVERED-UNCLASSIFIED`, not `CURRENT-AUTHORIZED`.

Possible governance states include:
`DISCOVERED-UNCLASSIFIED → QUARANTINED/INSPECTABLE → TEMPORARY-EXCEPTION or PROPOSED-ADMISSION → AUTHORIZED-CURRENT → RETIREMENT-PENDING → RETIRED`, with `REJECTED`, `UNKNOWN-OWNER`, `UNDER-REVIEW` and `EMERGENCY-BOUNDED` branches as needed.

Guard: `observed ≠ authorized`; `inventory entry created ≠ topology admission approved`.

## SYNTHESIS 2 — require ownership before normalization
A durable dependency needs an accountable owner or explicitly governed shared ownership. Discovery system, runtime producer and current operator are not automatically the owner.

Minimum admission evidence should identify the dependency/edge, owner, business/operational purpose, consequence class, data/authority handled, source/destination boundary, expected lifecycle, review triggers, retirement path and approval provenance.

Guard: `someone uses it ≠ someone owns it`; `operator ≠ accountable owner`.

## SYNTHESIS 3 — classify consequence before granting capability
Admission should be scoped to what the consumer may do: read/display, cache, queue, mutate, publish, export, authenticate, attest, acknowledge, recover or administer. A consumer admitted for read-only recovery does not thereby gain mutation or publication authority.

Guard: `authorized consumer ≠ authorized for every consequence`; `read admission ≠ write admission`.

## SYNTHESIS 4 — shadow dependency is not synonymous with malicious dependency
An undeclared consumer may be accidental, obsolete, emergency-created, manually operated, forgotten after migration, or malicious. Discovery alone cannot elect the explanation.

Preserve evidence and classify before destructive action unless immediate containment is required by risk.

Guard: `shadow ≠ malicious`; `unauthorized ≠ disposable data`.

## SYNTHESIS 5 — emergency use creates debt, not permanent precedent
An emergency/manual path may need bounded use before normal approval completes. Its exception should bind purpose, scope, consequence, authorized actor, start, expiry/review trigger, compensating controls, evidence requirements and exit/normalization path.

Repeated successful emergency use must not silently convert it into permanent topology.

Guard: `emergency allowed once ≠ permanently admitted`; `worked during incident ≠ normal architecture approved`.

## SYNTHESIS 6 — historical success is weak authorization evidence
A queue/export/integration that has run successfully for months may prove existence and operational reliance, but not that it was approved or remains appropriate.

When discovered, preserve historical evidence and classify current risk. Do not backdate authorization to first observed use unless authoritative historical approval evidence actually exists.

Guard: `historically used ≠ historically authorized`; `no incident observed ≠ acceptable risk proven`.

## SYNTHESIS 7 — discovery systems cannot approve what they discover
Collector D may propose a candidate inventory entry and attach evidence, but the same observation should not automatically set `AUTHORIZED-CURRENT` for material consequences.

For high-consequence paths, admission authority should be distinct enough from discovery that compromise or misconfiguration of the collector cannot manufacture approved topology.

Guard: `discovery evidence ≠ approval evidence`; `collector can see ≠ collector can authorize`.

## SYNTHESIS 8 — admission must update both declared topology and completeness assumptions
Once a shadow consumer is legitimately admitted, update the declared topology, consequence map, dependency graph, inventory/discovery coverage, closure prerequisites, backup/recovery assumptions and relevant tests. Admission is incomplete if the architecture record changes but assurance machinery still reasons about the old graph.

Guard: `approved ≠ assurance graph updated`; `topology document updated ≠ closure proof updated`.

## SYNTHESIS 9 — rejection needs safe disposition
Rejected consumers require a disposition appropriate to their consequence: block future execution, revoke credentials/routes, preserve unique data/provenance, migrate needed records, notify affected owners/recipients, remove stale configuration and prove retirement where controllable.

Immediate deletion is not the universal answer.

Guard: `rejected dependency ≠ erase everything`; `path disabled ≠ unique data safely dispositioned`.

## SYNTHESIS 10 — retirement is part of admission design
Every durable admitted dependency should have retirement/review rules at admission time: owner departure, product retirement, credential expiry, replacement, inactivity threshold as review trigger, policy/schema incompatibility, provider termination or explicit end date where appropriate.

Telemetry silence alone remains insufficient retirement evidence.

Guard: `admitted once ≠ immortal`; `inactive ≠ retired`.

## SYNTHESIS 11 — offline PWA/EFB consumers need asymmetric containment
A returning company iPad may reveal an undeclared local queue or old installed-PWA consumer. Preserve unique local flight/logbook data and provenance, but fence obsolete mutation/publication authority until the consumer and queued operations are classified under current policy.

The device can be `safe to inspect/recover` while `not authorized to mutate/publish`.

Guard: `safe to inspect ≠ safe to execute`; `offline history present ≠ current topology member`.

## SYNTHESIS 12 — browser/service-worker discovery remains evidence only
Service Worker registration, Cache Storage, IndexedDB or network observations may reveal a local consumer. A Service Worker becoming active does not constitute organizational admission, and a manifest-installed PWA does not automatically become a trusted enterprise participant.

Guard: `Service Worker active ≠ consumer authorized`; `PWA installed ≠ organizationally admitted`.

## SYNTHESIS 13 — manual/external consumers need the same governance semantics
Email exports, spreadsheets, printed reports, support tools and third-party handoffs may not be machine-addressable topology nodes, but material dependencies still need owner, consequence, retention/remediation and retirement rules proportionate to risk.

Guard: `manual path ≠ governance-free path`; `external recipient ≠ controllable runtime consumer`.

## SYNTHESIS 14 — admission authority is consequence-scoped
A person/team permitted to approve a low-risk analytics sink may not be permitted to approve a recovery-authority bridge or safety-relevant export path. Approval authority should follow consequence and policy rather than organizational convenience.

Guard: `can approve one topology class ≠ can approve all topology classes`.

## SYNTHESIS 15 — topology change requires post-admission validation
After admission, verify the intended constraints actually hold: credentials/scopes, routes, storage, queue behavior, failure isolation, observability, retirement hooks and predecessor rejection as applicable. Paper approval is not runtime proof.

Guard: `change approved ≠ change safely realized`; `configuration intended ≠ runtime behavior proven`.

## SYNTHESIS 16 — contradiction after admission reopens governance
If later observation shows the admitted consumer has broader behavior than approved, preserve the original admission and create a new contradiction/review event. Do not silently expand the approved scope to match reality.

Guard: `runtime drift ≠ automatic scope expansion`.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. separate discovery, classification, admission, operation, review and retirement states;
2. never let discovery automatically authorize a newly observed consumer;
3. require accountable ownership, purpose, consequence class, allowed capability, lifecycle and retirement rules before durable admission;
4. treat emergency/manual paths as bounded exceptions with expiry/review and normalization/removal obligations;
5. preserve unique data/provenance while fencing unauthorized mutation/publication paths;
6. scope admission authority to consequence rather than giving topology-wide approval power;
7. update dependency/completeness/closure assumptions when a consumer is admitted or rejected;
8. validate runtime constraints after approval and reopen governance on contradiction;
9. retain historical use separately from historical authorization;
10. keep product/backend/MDM/domain/legal implementation facts OPEN until canonical evidence exists.

## EFB / LogMate-like application case
Assume a 45-day-offline company iPad returns with unique flight records and a browser-local retry queue Q9 that is absent from the declared topology. Q9 has successfully sent records in the past, but no admission record is found.

Safe generic sequence:
1. preserve Q9 contents and unique records/provenance without executing the queue;
2. classify Q9 as `DISCOVERED-UNCLASSIFIED/UNDER-REVIEW`, not automatically malicious or current;
3. fence mutation/publication while allowing bounded inspection/recovery;
4. search for historical approval, owner and purpose evidence without inventing authorization from prior success;
5. classify consequence, credentials, data handled and current compatibility;
6. if emergency access is necessary, issue a bounded exception with expiry/review and compensating controls rather than permanent admission;
7. if durable admission is justified, establish current owner, scope, authority, lifecycle and retirement contract and update the dependency/completeness model;
8. revalidate/rebase individual queued operations under current policy before execution;
9. if rejected, migrate/preserve needed data and prove the obsolete path is fenced/retired where controllable;
10. retain the discovery/admission/rejection provenance for future completeness and incident analysis.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
857. **Discovery-authorizes-itself** — collector finds an undeclared consumer and automatically marks it current/authorized. Expected: fail.
858. **Historical-success laundering** — months of successful execution are treated as proof of historical/current approval. Expected: fail.
859. **Emergency-path permanence** — incident-created export/queue remains indefinitely after emergency without expiry/review/normalization. Expected: fail.
860. **Ownerless admission** — material consumer is admitted without accountable ownership or retirement responsibility. Expected: fail.
861. **Read-to-write authority expansion** — consumer approved for inspection/recovery silently gains mutation/publication authority. Expected: fail.
862. **Shadow-equals-malicious destruction** — undeclared offline consumer triggers deletion of unique local records before classification/recovery. Expected: fail.
863. **Approval-with-stale-assurance-graph** — consumer is legitimately approved but completeness/closure machinery continues to use predecessor topology. Expected: fail.
864. **Runtime-drift scope laundering** — post-admission observation shows broader behavior and system silently expands approved scope to match. Expected: fail.

**VALIDATION:** these are defined destructive cases only. Execution PASS is not claimed.

## OPEN / VALIDATION
- Actual MintTap/LogMate topology, queues, workers, exports, MDM, fleet, Service Worker, backend and manual workflows remain OPEN.
- Actual admission authorities and aviation/safety/legal consequence classes remain OPEN.
- Physical iOS/iPadOS installed-PWA and managed-EFB behavior remains OPEN.
- Emergency-path operational UX, screen-reader and representative-human validation remains OPEN.
- Exact retirement, migration and unique-data preservation mechanisms remain OPEN.

## CHANGE WATCH
- NIST SP 800-53 release updates and configuration-management guidance.
- Apple/WebKit installed-PWA, storage, service-worker and managed-device behavior.
- Actual project topology, MDM/enrollment, auth/session, sync and export architecture when canonical implementation evidence becomes available.

## Next high-value target
**264 — emergency topology exception expiry, normalization/removal proof & exception-debt concentration.** Determine how temporary shadow-consumer admissions expire without destructive data loss, how repeated exceptions reveal architectural debt, how successor normal paths prove predecessor emergency routes are fenced, and how exception concentration/common-mode dependence changes risk even when each exception is individually bounded.