# 222 — PWA Assurance-Debt Ledger Integrity, Closure-Evidence Independence & Post-Emergency Regression Governance

Status: **PASS (generic) / PRODUCT + LEDGER + CLOSURE-ASSESSMENT + EMERGENCY-OPERATIONS + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A offline/runtime mechanics; Track B recovery/degraded-state UX; Track C destructive validation; Track D debt/regression telemetry.  
Dependencies: 117–137, 171–221 and prior evidence/currentness/quorum/emergency-authority work.

## Problem
221 established that emergency operation creates assurance debt and that NORMAL requires positive recovery evidence plus negative evidence that temporary authority is extinct. The adjacent failure is that the debt record and closure process can themselves become part of the incident's compromised or exception-bearing failure domain. An operator could omit debt, mutate its scope, produce its own closure evidence, mark unresolved uncertainty `resolved`, or repeatedly invoke emergency mode until reduced assurance becomes the de facto baseline.

Central rule: **assurance debt is a versioned evidence obligation, not a mutable incident checkbox. Its creation, amendment, evidence attachment, risk acceptance and closure must preserve provenance; closure evidence must be sufficiently independent of the authority/failure domain that created the debt; unresolved debt constrains the affected capability without silently laundering uncertainty; repeated emergency use is regression evidence, not implicit normalization.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Offline clocks, cached policy, Service Worker/update state and delayed reconnect affect evidence timing and replay but do not own debt truth.
- **B UX/IA/Content:** very high dependency pressure. Must distinguish `NORMAL`, `DEGRADED`, `RECOVERY-PENDING`, `DATA-PRESERVED / SYNC-BLOCKED`, and unresolved-debt states without turning operator/user UI into an authority bypass.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **528 → 536 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures debt age, recurrence, scope, evidence completeness and regression; analytics cannot create, waive or close debt.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns ledger integrity, provenance, closure independence, scoped blocking, corrective-control escalation and post-emergency governance.

## SOURCE

### NIST SP 800-61 Rev.3 — recovery closure produces documentation and feeds improvement
SP 800-61 Rev.3 is final (2025-04-03). Its recovery recommendations require integrity checks before restored assets return to use, confirmation of normal operating status, criteria-based end of recovery and completion of incident documentation/after-action reporting. NIST's incident-response project also explicitly feeds lessons learned from all CSF functions into Improvement for analysis and prioritization.

Sources:
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://csrc.nist.gov/projects/incident-response

**TRANSFER VALIDATION:** NIST does not define a MintTap assurance-debt ledger. It supports the bounded conclusions that recovery closure is criteria/evidence based, documentation survives the incident, and lessons learned should alter future risk management rather than disappear at service restoration.

### NIST SP 800-53 Rev.5 — audit information itself requires protection
SP 800-53 Rev.5 remains current with later patch releases. The Audit and Accountability family includes audit generation, review, retention and **AU-9 Protection of Audit Information**; related assessment guidance treats evidence and assessment as distinct from the operational control being assessed.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** an assurance-debt ledger is not automatically an AU log. The reusable principle is that evidence about security-relevant actions needs integrity/access protection and assessability; storing a debt row in the same mutable operational database is not by itself strong evidence.

### NIST CSF 2.0 — improvement and governance are continuing risk-management functions
CSF 2.0 treats cybersecurity outcomes as an organization-wide risk-management framework and adds explicit governance. Incident-response guidance built on CSF 2.0 routes lessons learned into Improvement rather than treating an incident as complete once availability returns.

Source:
- https://doi.org/10.6028/NIST.CSWP.29

**TRANSFER VALIDATION:** CSF does not prescribe recurrence thresholds or MintTap corrective controls. It supports treating repeated emergency activation as governance/improvement input rather than silently converting an exception into baseline practice.

## SYNTHESIS 1 — debt is an evidence object with identity and lineage
Each debt item should have a stable identity and preserve at least: creation authority/event; affected capability/scope; missing or relaxed assurance; security/policy generation; time/window evidence; temporary authority introduced; actions executed/queued; contradictions/unknown tails; compensating controls; remediation owner; closure criteria; evidence references; amendments; risk decisions; and terminal state.

Amendments append/supersede; they do not silently rewrite the historical record. A human-readable ticket may project this ledger, but the ticket is not necessarily the authoritative evidence object.

`ticket closed ≠ debt evidence closed`; `row updated ≠ history preserved`; `current projection ≠ complete debt lineage`.

## SYNTHESIS 2 — ledger integrity must survive the incident's failure domain
If the same compromised admin plane can both exercise emergency authority and delete or rewrite its debt evidence, the ledger provides weak assurance. Protect debt evidence with access separation, append/supersession semantics, durable audit/provenance, backups/retention and—where warranted—independent or differently administered evidence copies/checkpoints.

Do not infer that cryptographic signing alone solves completeness: a compromised authorized signer can sign an omission or false closure claim.

`signed debt record ≠ complete debt record`; `tamper-evident entry ≠ omission-resistant ledger`; `backup exists ≠ independent evidence domain`.

## SYNTHESIS 3 — closure evidence needs claim-specific independence
The actor that performed an emergency action may supply evidence, but for material claims it should not be the sole source of assurance that its own temporary authority is extinct or that the affected enforcement path is current. Independence is claim/failure-domain specific: a separate service name is insufficient if it shares credentials, telemetry source, database or admin plane with the emergency actor.

A closure bundle can combine operator evidence with independently sourced negative tests, provider/control-plane evidence, currentness witnesses, recovery/PITR rejoin evidence and review by an authority whose validity does not derive from the emergency exception.

`different approver name ≠ independent evidence`; `operator attests revoked ≠ revoked path tested`; `closure authority independent ≠ every evidence source independent`.

## SYNTHESIS 4 — unresolved debt is capability-scoped, not a global Boolean
Debt should constrain the capability and trust claim it actually affects. If independent evidence for a remote-mutation path remains missing, that need not erase locally preserved flight/logbook data or unrelated read-only capability. Conversely, scoping cannot be abused to label a cross-cutting authority failure as a tiny local debt.

Use an explicit dependency map from debt item → authority/evidence/control → affected capabilities/enforcement set. Scope can narrow only when evidence supports that boundary.

`one debt open ≠ whole product unusable`; `narrow label ≠ narrow blast radius proven`; `data preserved ≠ remote mutation admitted`.

## SYNTHESIS 5 — risk acceptance cannot mutate historical evidence state
An authorized risk owner may accept operation with unresolved debt, but acceptance creates a new governance decision linked to the debt. It does not change `UNKNOWN`, `CONTRADICTED` or `UNVERIFIED` historical evidence into `PASS`.

`risk accepted ≠ debt disproven`; `accepted residual risk ≠ evidence recovered`; `business continuation ≠ historical assurance restored`.

## SYNTHESIS 6 — repeated emergency activation is regression evidence
Track recurrence by cause/control/capability/failure domain, not just raw count. Repeated activation after nominal closure can indicate ineffective corrective control, fragile quorum/witness topology, operational capacity mismatch, dependency concentration, or an emergency mode that has become a shadow normal path.

Define governance triggers for recurrence, cumulative emergency duration, reactivation shortly after closure, repeated use of the same exception authority, widening scope and recurring closure debt. Crossing a trigger causes review/corrective-control work; it does not automatically broaden emergency permission.

`frequent exception ≠ baseline permission`; `incident count low ≠ control healthy`; `same symptom ≠ same root cause`; `repeated closure ≠ corrective control effective`.

## SYNTHESIS 7 — debt closure and corrective-action closure are separate
An individual incident's evidence debt can close while a systemic corrective action remains OPEN. Conversely, a redesign may be deployed while historical debt for an old interval remains UNKNOWN. Preserve both lifecycles.

`incident debt closed ≠ systemic regression fixed`; `new control deployed ≠ historical uncertainty erased`; `corrective ticket closed ≠ recurrence risk validated`.

## SYNTHESIS 8 — post-emergency validation requires regression evidence
Where a corrective control is introduced, validate the exact failure oracle that caused or enabled emergency mode and adjacent bypass paths. A dashboard showing normal metrics is not a regression test. Where physical/browser/provider behavior matters, generic research cannot substitute for runtime evidence.

For PWA cases this can include stale Service Worker/policy rejection, expired emergency credential rejection, queued-work re-admission, PITR rejoin, offline-client reconnect and data-preserving blocked-sync behavior.

`green dashboard ≠ regression PASS`; `code deployed ≠ failure oracle closed`; `emulator/browser automation PASS ≠ physical iPad PASS`.

## SYNTHESIS 9 — offline clients may discover closed debt late
A long-offline iPad can return after debt D was created and closed. Its cached emergency state may itself be an outstanding enforcement tail even if the central incident is closed. Preserve unique local data, acquire current authenticated policy/security generation, reject extinct emergency authority, and re-admit queued consequence-bearing work. If the device cannot prove current admission state, keep sync restricted without relabeling its data as lost or malicious.

`central debt closed ≠ every offline tail converged`; `device was unreachable ≠ device inherited indefinite emergency authority`.

## SYNTHESIS 10 — the debt ledger itself needs recovery and retention semantics
A ledger lost in PITR, provider migration or retention cleanup can make closure unverifiable. Treat its recovery objective, retention, export/migration format, verifier context and deletion authority as part of the evidence system. Retention should be justified by operational/legal/privacy requirements rather than indefinite payload hoarding.

`production restored ≠ debt ledger restored`; `ledger export parseable ≠ provenance preserved`; `retention expiry ≠ permission to erase still-open debt`.

## MINTTAP DECISION / DIRECTION
1. Treat assurance debt as a versioned, provenance-bearing evidence object rather than a mutable incident checkbox.
2. Separate debt creation/amendment, risk acceptance and closure authority; preserve the identity and basis of each transition.
3. Require claim-specific independent corroboration for material closure claims, especially extinction of temporary authority and convergence of previously affected enforcement paths.
4. Map unresolved debt to affected capabilities and dependencies; preserve safe local/offline utility where the debt does not invalidate it, but do not use narrow labels to launder broad authority uncertainty.
5. Keep risk acceptance separate from evidence truth.
6. Treat repeated emergency activation as regression/corrective-control evidence and establish governance triggers rather than silently normalizing reduced assurance.
7. Keep incident-debt closure, systemic corrective-action closure and runtime regression validation as separate states.
8. Include debt-ledger durability/recovery/retention in the evidence architecture.

These are generic directions, not claims about current MintTap/LogMate architecture.

## OPEN / DEPENDENCY
- Actual debt-ledger schema/storage/access/retention/backup/attestation topology: **OPEN**.
- Actual emergency actor, closure assessor, provider IAM and evidence failure domains: **OPEN**.
- Exact capability/dependency map and what unresolved debt should block: **OPEN**.
- Recurrence thresholds/corrective-action governance appropriate to company risk: **OPEN**.
- Exact managed-iPad/iPadOS/WebKit/MDM/offline behavior: **Track A + Software Engineering runtime dependency**.
- Degraded/recovery/debt UX: **Track B consuming Design Studio; human/accessibility validation OPEN**.
- Legal/aviation/safety retention and EFB requirements: **OPEN**.

## Track C destructive campaign — 528 → 536 defined cases
Add:
1. **Debt deletion by emergency actor:** operator exercises break-glass authority and removes the corresponding debt entry before closure review.
2. **Signed omission:** authorized ledger signer produces a valid signed snapshot that omits one unresolved debt item.
3. **Self-produced closure:** emergency operator is sole source for evidence that its own temporary credential no longer works.
4. **False narrow scoping:** global/shared authority uncertainty is relabeled as one regional capability debt to unblock the rest of the fleet.
5. **Risk-acceptance laundering:** risk owner accepts continued operation and system rewrites historical `UNKNOWN` evidence to `PASS`.
6. **Recurring emergency normalization:** same control failure triggers repeated emergency mode; each incident closes independently and no regression/corrective-control escalation occurs.
7. **PITR ledger loss:** service recovery restores operational data but rolls the assurance-debt ledger back before an unresolved item was created.
8. **Long-offline iPad after central closure:** central debt is closed, but returning device still presents cached emergency authority; unique data survives while consequence-bearing sync remains blocked until current re-admission.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** cached state and offline timing explain delayed convergence; they do not change debt truth or authority expiry.
- **Track B:** users/operators need comprehensible restricted/recovery states, but UI labels cannot close debt or create bypass authority.
- **Track C:** ledger integrity, independent closure, PITR survival and recurrence regression require executable evidence; reading is not runtime PASS.
- **Track D:** telemetry can detect recurrence, age and scope patterns but cannot infer authority or rewrite evidence state.
- **Design Studio:** Web remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/iPadOS/EFB and canonical-product runtime remain OPEN.

## Persistent guards added
`ticket closed ≠ debt evidence closed`; `row updated ≠ history preserved`; `signed debt record ≠ complete debt record`; `tamper-evident entry ≠ omission-resistant ledger`; `different approver name ≠ independent evidence`; `operator attests revoked ≠ revoked path tested`; `one debt open ≠ whole product unusable`; `narrow label ≠ narrow blast radius proven`; `risk accepted ≠ debt disproven`; `frequent exception ≠ baseline permission`; `repeated closure ≠ corrective control effective`; `incident debt closed ≠ systemic regression fixed`; `new control deployed ≠ historical uncertainty erased`; `green dashboard ≠ regression PASS`; `central debt closed ≠ every offline tail converged`; `production restored ≠ debt ledger restored`; `retention expiry ≠ permission to erase still-open debt`.

## Gate result
**222 PASS (generic).** The knowledge gate closes because debt identity/lineage, ledger integrity, closure-evidence independence, capability-scoped unresolved debt, risk-acceptance separation, recurrence/regression governance, corrective-action separation, offline-tail handling and ledger recovery/retention now have explicit evidence boundaries and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**223 — assurance-debt dependency graphs, transitive blast-radius proof & safe partial reauthorization**: determine how debt propagates through shared identity/provider/key/policy/evidence dependencies, how to prove that an unaffected capability is genuinely outside the compromised trust path before re-enabling it, and how partial reauthorization avoids both unnecessary global shutdown and unsafe scope laundering across distributed/offline PWA enforcement.