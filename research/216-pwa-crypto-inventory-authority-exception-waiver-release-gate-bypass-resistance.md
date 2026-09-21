# 216 — PWA Crypto-Inventory Authority, Exception/Waiver Lifecycle & Release-Gate Bypass Resistance

Status: **PASS (generic) / PRODUCT + AUTHORITY + RELEASE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A platform capability evidence; Track B exception/recovery-state communication; Track C release/destructive validation; Track D exception/drift observation.  
Dependencies: 117–125, 171–215 and the earlier authority/currentness/recovery/provenance chain.

## Problem
215 made cryptographic inventory a versioned evidence product and retirement a bounded negative claim. The adjacent failure mode is governance: an accurate inventory can still be made unsafe if an operator can relabel `UNKNOWN`, `RETIRED` or `REJECTED` crypto as acceptable, issue an open-ended waiver, bypass a release gate during an incident, or replay an old approval after rollback/provider migration/offline return.

Central rule: **inventory evidence describes what is known; acceptance policy decides what may be consequence-bearing; exception authority may temporarily alter a bounded policy outcome but must not silently rewrite inventory facts, retirement history or the durable security floor. Emergency bypass is a governed debt-creating transition with mandatory evidence and re-convergence, not an alternate permanent release path.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Provides actual capability/support/failure evidence for TLS/WebCrypto/WebKit/Service Worker/update and managed-device boundaries. Platform inability may justify a business decision to block/degrade a path; it does not authorize a cryptographic downgrade.
- **B UX/IA/Content:** very high dependency pressure. Must distinguish `blocked`, `temporary exception active`, `data preserved / sync blocked`, `migration required`, `exception expired` and `current` without presenting unsafe downgrade as a user preference.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **488 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures waiver age, bypass frequency, scope, unresolved debt, policy drift and reconvergence evidence; metrics do not grant exceptions.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns policy authority, exception semantics, emergency release gates, anti-rollback, revocation and closure evidence.

## SOURCE

### NIST CSF 2.0 — risk acceptance belongs to explicit governance
NIST CSF 2.0 is a current final risk-management framework. Its Govern function makes organizational context, risk-management strategy, roles/responsibilities, policy and oversight explicit parts of cybersecurity outcomes. NIST's ERM quick-start guide likewise connects cybersecurity risk monitoring, evaluation and adjustment to enterprise risk management rather than treating operational exceptions as local implementation details.

Sources:
- https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-enterprise-risk-management-quick-start-guide

**TRANSFER VALIDATION:** these sources support explicit accountability and risk-acceptance governance. They do not define a MintTap waiver schema, approver set, severity matrix or expiry period.

### NIST CSWP 39upd1 — crypto agility preserves security and operations
NIST CSWP 39upd1, finalized/updated 2026-06-29, defines crypto agility as the capability to replace/adapt cryptographic algorithms across protocols, applications, software, hardware, firmware and infrastructure while preserving security and ongoing operations. It emphasizes environment-specific strategies and trade-offs rather than universal fallback.

Sources:
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://www.nist.gov/publications/considerations-achieving-crypto-agility-strategies-and-practices-0

**TRANSFER VALIDATION:** emergency compatibility pressure does not turn agility into `accept anything supported`. Policy still needs controlled transition and explicit risk ownership.

### NCCoE Migration to PQC — discovery and interoperability are distinct workstreams
The current NCCoE Migration to PQC project separates cryptographic discovery/visibility from interoperability testing. Discovery is intended to establish where/how cryptography is used; interoperability testing identifies compatibility problems in controlled environments before migration.

Source:
- https://www.nccoe.nist.gov/applied-cryptography/migration-to-pqc

**TRANSFER VALIDATION:** a compatibility failure is evidence to resolve, not itself authorization to weaken an acceptance floor. Inventory/discovery and policy exception remain different planes.

## SYNTHESIS 1 — separate fact authority, policy authority and exception authority
Use three distinct concepts:
1. **inventory/fact authority** — may assert evidence-backed observations such as algorithm/provider/key/path/status and uncertainty;
2. **acceptance-policy authority** — may define which cryptographic states are permitted for a purpose/generation;
3. **exception authority** — may authorize a narrowly scoped temporary deviation under predefined governance.

An inventory editor must not gain policy authority merely by changing a classification field. A policy approver must not erase evidence that an old dependency still exists. An exception approver must not convert a temporary waiver into historical proof that the waived state was compliant.

`inventory classification changed ≠ underlying crypto changed`; `inventory editor ≠ acceptance authority`; `exception approved ≠ baseline rewritten`.

## SYNTHESIS 2 — UNKNOWN is not an approval category
`UNKNOWN` means evidence is insufficient. It is not a softer spelling of `ACCEPTED`.

When a release depends on unknown cryptography, valid outcomes include investigation, containment, capability restriction, data-preserving block, or an explicitly governed temporary exception if organizational policy permits. The exception record must preserve the unknown rather than relabel it away.

`unknown accepted temporarily ≠ unknown resolved`; `business urgency ≠ evidence`; `no known exploit ≠ acceptable cryptographic assurance`.

## SYNTHESIS 3 — a waiver is a scoped capability lease, not a global downgrade
A useful crypto exception/waiver should bind at least:
- immutable exception/decision identity and policy generation;
- exact subject: product/service/build/provider/device cohort/path;
- exact cryptographic condition being waived;
- consequence-bearing capabilities allowed and explicitly disallowed;
- rationale and evidence references;
- risk owner and authorization evidence;
- issue/start context and expiry/termination conditions;
- compensating controls where meaningful;
- observation/alert requirements;
- migration/remediation owner and closure criterion;
- supersession/revocation lineage;
- emergency vs planned-exception class.

Do not make a universal expiry duration here; product risk and organizational policy must determine it. But absence of a meaningful termination condition is a governance defect.

`waiver exists ≠ all uses waived`; `same algorithm ≠ same exception scope`; `temporary exception ≠ temporary truth`.

## SYNTHESIS 4 — exception expiry must fail closed for consequence-bearing authority while preserving unique data
When a waiver expires or is revoked, a stale client/provider/build must not continue remote mutation merely because it once had a valid exception. For an offline-first PWA/EFB, expiration should not destroy unique local records. Preserve data, quarantine stale authority, obtain current policy, then re-admit operations.

If current verification cannot execute, the safe generic state is `data preserved / consequence-bearing sync blocked`, not automatic reactivation of the expired waiver.

`waiver valid when queued ≠ waiver valid when replayed`; `offline during expiry ≠ expiry suspended`; `data preservation ≠ authority preservation`.

## SYNTHESIS 5 — emergency release bypass must create evidence and debt atomically
An emergency release may need to proceed while a normal assurance gate is unavailable. A bypass mechanism should not be an undocumented switch. At minimum, the release/bypass record should bind:
- exact artifact/build and environment;
- failed/unavailable gate and why it could not complete;
- emergency authorization and scope;
- checks that did execute and their evidence;
- explicitly unverified properties;
- allowed rollout/capability boundary;
- monitoring/containment conditions;
- rollback/kill conditions;
- mandatory post-release validation and owner;
- re-convergence/closure state.

Where technically feasible, creation of the bypass and creation of the debt/evidence record should be one governed transition so `release succeeded but exception record disappeared` is not a normal state.

`emergency release ≠ normal PASS`; `gate unavailable ≠ gate failed ≠ gate unnecessary`; `artifact deployed ≠ bypass debt closed`.

## SYNTHESIS 6 — break-glass must not bypass the authority model that governs break-glass
A dangerous design gives one operational administrator the ability to both declare an emergency and permanently lower cryptographic policy. Reuse the prior recovery-ceremony principle: emergency capability should be purpose-scoped, independently authorized where required by risk, observable, revocable and followed by privilege contraction.

If the normal identity/control plane is itself suspect, approvals that depend entirely on that same failure domain cannot be treated as independent evidence merely because two accounts clicked approve.

`two approvals ≠ two independent authorities`; `admin role ≠ permanent crypto-policy authority`; `break-glass opened ≠ baseline changed`.

## SYNTHESIS 7 — rollback/PITR must not resurrect expired waivers
Exception state has a currentness dimension. An authentic database backup may contain a waiver that was valid at backup time but expired or was revoked later. PITR must not make it current again.

Preserve a durable policy/exception floor outside the rollbackable application state where required by the architecture, or require post-restore reconciliation against current authority before consequence-bearing operation resumes.

Historical exception records remain evidence; they do not regain authority.

`authentic old waiver ≠ current waiver`; `PITR restored approval ≠ approval reactivated`; `clock moved backward ≠ expiry moved backward`.

## SYNTHESIS 8 — provider migration does not transfer waivers by implication
A waiver scoped to provider/configuration P1 is not automatically valid for P2. Migration may change cryptographic implementation, negotiation, certificate/key custody, control plane and observability. Re-evaluate the exact risk proposition.

Conversely, moving providers does not prove the waived dependency is gone. Old provider paths, DNS, credentials, backups, profiles or dormant recovery configuration may remain reachable.

`provider migrated ≠ exception migrated`; `provider migrated ≠ old exception closed`; `same service purpose ≠ same failure domain`.

## SYNTHESIS 9 — release gates need bypass resistance at more than the UI
A release UI that says `blocked` is insufficient if alternate APIs, CI credentials, manual provider consoles, rollback paths, region-specific deployers or restore procedures can publish an artifact that bypasses the same policy.

Model enforcement points explicitly and test them. The strongest useful retirement/exception claim is scoped: under policy generation G, known consequence-bearing issuance/deployment/admission paths E1..En reject the prohibited state, with enumerated unknowns/tails.

`UI gate blocks ≠ deployment path blocked`; `CI policy PASS ≠ provider console constrained`; `one region rejects ≠ fleet rejects`.

## SYNTHESIS 10 — exception telemetry measures governance health, not permission
Useful observations include:
- active/expired/revoked exceptions by consequence class;
- age and remaining validity;
- repeated renewal count;
- emergency bypass frequency and cause;
- release percentage using bypass;
- unresolved UNKNOWN dependencies under exception;
- time to post-release validation and closure;
- provider/region/client cohorts still depending on a waiver;
- attempts to use expired/retired policy;
- long-offline devices returning after exception expiry.

High exception frequency is a signal of architecture/process debt; zero observed violations is not proof that bypass paths do not exist.

`dashboard green ≠ waiver safe`; `zero expired-use events ≠ expired path extinct`; `exception count low ≠ exception risk low`.

## SYNTHESIS 11 — repeated renewal is a different risk from one bounded exception
A waiver repeatedly renewed without material new evidence can become a de facto baseline while retaining the weaker scrutiny of an exception. Treat renewal as a new decision that references predecessor history, accumulated exposure, failed remediation commitments and changed environment.

Do not reset `age` by issuing a new identifier. Track cumulative exception lineage.

`new waiver ID ≠ new risk`; `renewed ≠ remediated`; `no incident during waiver ≠ risk disproven`.

## SYNTHESIS 12 — long-offline company iPad is the anti-replay test
Consider an EFB-like iPad that went offline while waiver W allowed legacy crypto L, missed W expiry and policy generations G+1/G+2, and returns with unique flight/logbook records plus old Service Worker/session/policy state.

Generic handling:
1. preserve unique local data before destructive remediation;
2. treat W and L as historical context, not current authority;
3. obtain authenticated current policy and exception lineage;
4. quarantine stale session/Service Worker/credential assumptions as required;
5. re-evaluate queued operations under current policy;
6. migrate/transform only where semantics and provenance can be preserved;
7. block consequence-bearing sync if current verification cannot be satisfied;
8. never reopen W merely because the device was unreachable during expiry.

This makes offline fleet tails a direct validation of exception anti-rollback semantics.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. keep inventory facts, acceptance policy and exception authority as separate governed planes;
2. never use `UNKNOWN` as an implicit accepted state;
3. model waivers as scoped, versioned, revocable capability leases with explicit termination and remediation lineage;
4. preserve baseline and retirement history when an exception is granted;
5. make emergency release bypass evidence-producing and debt-creating, with mandatory re-convergence;
6. require purpose-scoped break-glass and post-emergency privilege contraction rather than a universal bypass administrator;
7. protect exception currentness against PITR/clock rollback/stale replica replay;
8. re-evaluate exceptions across provider/control-plane migration rather than transferring them implicitly;
9. enumerate and test release/admission enforcement points beyond the primary UI/CI path;
10. use telemetry to detect exception debt/drift, not to grant permission;
11. treat repeated renewal as cumulative risk history;
12. for long-offline PWA/iPad return, preserve unique data but enforce current policy before consequence-bearing sync.

These are generic governance directions, not claims about current MintTap or LogMate implementation.

## Cross-track transfer
### Track A — DEPENDENCY / TRANSFER
Provide current browser/platform capability evidence that explains why an exception is requested, including exact Safari/WebKit/iPadOS/WebCrypto/Service Worker behavior where execution evidence exists. Capability absence is input to governance, not acceptance authority. Rapidly changing support remains CHANGE WATCH.

### Track B — DEPENDENCY
Consume Design Studio interaction evidence for clear `blocked`, `temporary exception`, `migration required`, `expired`, `data preserved / sync blocked` and recovery states. Avoid user-facing `continue insecurely` controls that bypass server policy. Physical-device and human comprehension validation remain OPEN.

### Track C — VALIDATION
Destructive campaign grows **480 → 488 defined cases**:
1. inventory editor changes `UNKNOWN` to `ACCEPTED` without acceptance-policy authority;
2. waiver for export verification is replayed to authorize current sync admission;
3. waiver W expires while an iPad is offline, then queued work replays under W on reconnect;
4. PITR restores authentic but revoked W and one region resumes acceptance;
5. emergency release bypass deploys artifact but the mandatory debt/evidence record is absent;
6. primary CI gate blocks retired crypto while provider console/manual deployment path still permits it;
7. provider P1 waiver is silently copied to materially different P2 during migration;
8. repeatedly renewed waiver receives new IDs so cumulative age/exposure disappears.

Execution, actual release controls, policy store, clock/currentness source, provider consoles, regional enforcement, managed iPad/Safari and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure exception age/lineage, renewal count, bypass frequency, failed-gate reason, closure latency, unresolved unknowns, expired-policy attempts, enforcement-point coverage and offline-tail return. Keep metrics observational; analytics must not become an exception authorization oracle.

## Persistent guards added through 216
- `inventory classification changed ≠ underlying crypto changed`;
- `inventory editor ≠ acceptance authority`;
- `exception approved ≠ baseline rewritten`;
- `unknown accepted temporarily ≠ unknown resolved`;
- `business urgency ≠ evidence`;
- `no known exploit ≠ acceptable cryptographic assurance`;
- `waiver exists ≠ all uses waived`;
- `same algorithm ≠ same exception scope`;
- `temporary exception ≠ temporary truth`;
- `waiver valid when queued ≠ waiver valid when replayed`;
- `offline during expiry ≠ expiry suspended`;
- `emergency release ≠ normal PASS`;
- `gate unavailable ≠ gate failed ≠ gate unnecessary`;
- `artifact deployed ≠ bypass debt closed`;
- `two approvals ≠ two independent authorities`;
- `admin role ≠ permanent crypto-policy authority`;
- `authentic old waiver ≠ current waiver`;
- `PITR restored approval ≠ approval reactivated`;
- `clock moved backward ≠ expiry moved backward`;
- `provider migrated ≠ exception migrated`;
- `provider migrated ≠ old exception closed`;
- `UI gate blocks ≠ deployment path blocked`;
- `CI policy PASS ≠ provider console constrained`;
- `one region rejects ≠ fleet rejects`;
- `dashboard green ≠ waiver safe`;
- `zero expired-use events ≠ expired path extinct`;
- `new waiver ID ≠ new risk`;
- `renewed ≠ remediated`;
- `no incident during waiver ≠ risk disproven`;
- `data preservation ≠ authority preservation`.

## OPEN
- actual MintTap/LogMate inventory, acceptance-policy and exception-authority schema;
- actual approvers, separation-of-duty/failure-domain requirements and organizational risk tolerance;
- actual exception duration/termination rules, compensating controls and renewal policy;
- actual CI/CD/provider/manual/rollback/region/PITR enforcement points;
- actual emergency-release/break-glass mechanisms and evidence atomicity;
- actual clock/currentness source and anti-rollback implementation;
- actual provider migration and residual old-provider paths;
- actual long-offline iPad fleet, WebKit/PWA crypto capability and queue re-admission behavior;
- actual legal/aviation/privacy/safety constraints on accepting cryptographic exceptions;
- physical-device/runtime, security and human-state validation.

## CHANGE WATCH
- NIST CSF governance/risk-management resources;
- NIST CSWP 39upd1 and subsequent crypto-agility guidance;
- NCCoE Migration to PQC discovery/interoperability outputs;
- NIST PQC transition/algorithm guidance;
- browser/WebCrypto/WebKit/server/provider crypto capability and defaults;
- provider release-policy/attestation/managed-device capabilities.

## Gate result
**216 PASS (generic).** The Web Manager can now separate inventory facts from acceptance and exception authority; model crypto waivers as bounded capability leases; preserve baseline/currentness across expiry, rollback and provider migration; govern emergency release bypass as evidence-producing debt; and test bypass resistance across consequence-bearing enforcement points.

Production validation remains OPEN.

## Next highest-value adjacent question
**217 — exception-authority succession, delegated-policy composition & waiver-conflict resolution across distributed enforcement.** Determine how exception authority itself rotates or is delegated without expanding scope; how global, product, provider, regional and device policies compose when they disagree; how two individually valid waivers are prevented from combining into an unintended broader permission; and how split-brain enforcement converges after authority/policy succession without accepting the most permissive branch.