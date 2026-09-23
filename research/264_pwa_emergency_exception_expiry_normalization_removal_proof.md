# 264 — PWA Emergency Topology Exception Expiry, Normalization/Removal Proof & Exception-Debt Concentration

Status: **PASS (generic) / PRODUCT + DATA-MODEL + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/fencing mechanics; Track B expiry/recovery UX; Track C destructive validation; Track D bounded exception-debt measurement.  
Dependencies: 117–121 exception/waiver lifecycle, 127–130 dependency concentration/resilience, 249–263 policy/distribution/dependency/topology governance.

## Problem
263 separated discovery from authorization and made emergency/manual paths bounded exceptions rather than permanent architecture. The next failure boundary is what happens after an exception is granted.

A temporary route can remain technically reachable after its approval expires; repeated individually valid exceptions can accumulate into a de facto shadow architecture; a successor path can be declared normal while the predecessor emergency path still accepts writes; or expiry can trigger destructive cleanup that erases unique offline data before recovery. Each local exception may look controlled while the aggregate system becomes less controlled.

Central rule: **exception expiry ends exceptional authority, not the existence of data or evidence. Normalization requires positive successor evidence plus predecessor fencing/removal evidence appropriate to consequence. Exception debt must be assessed both per exception and in aggregate for common-mode concentration, recurrence and architectural substitution.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns the mechanics by which old Service Workers, caches, queues, routes, credentials and offline clients can remain reachable after policy expiry. Runtime reachability is not authority.
- **B UX/IA/Content:** high dependency pressure. Owns understandable `exception expiring`, `expired/recovery-only`, `normalization pending`, `safe to recover`, `mutation blocked` and `retirement incomplete` states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **864 → 872 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer. Measures exception age, recurrence, overlap, concentration and predecessor traffic, but telemetry silence cannot prove removal.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns expiry semantics, successor normalization, predecessor fencing/removal proof, exception-debt aggregation and risk disposition.

## SOURCE

### NIST SP 800-53 Rev. 5 — emergency changes remain inside configuration change control
CM-3 requires configuration changes to be reviewed, approved, documented and controlled; NIST guidance explicitly includes emergency changes in configuration change control. CM-4 requires security/privacy impact analysis, while CM-5 limits who may make changes.

Sources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final  
https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

**TRANSFER VALIDATION:** emergency status does not create a governance-free lane. This is bounded precedent, not a LogMate-specific exception workflow.

### NIST CSF 2.0 — lifecycle, authorized flows and risk governance
CSF 2.0 provides outcomes for maintaining inventories, representations of authorized communications/data flows, supplier/service dependencies and lifecycle/risk governance.

Source: https://www.nist.gov/cyberframework

**TRANSFER VALIDATION:** supports treating repeated temporary paths and concentrated dependencies as governed risk rather than isolated tickets. CSF does not prescribe this exception-debt model.

### Apple Platform Deployment — Return to Service is an explicit erase/re-enrollment transition
Apple documents Return to Service as a managed erase followed by enrollment/configuration. On iOS/iPadOS 26+ app binaries may be preserved while user-generated app data is securely erased; on current iOS/iPadOS 27 flows enrollment retry and update behavior are version-specific. Apple separately documents restore cases where managed app data may return while enrollment/identity behavior differs by enrollment method and OS version.

Sources: https://support.apple.com/guide/deployment/dep17cb455a0/web  
https://support.apple.com/guide/deployment/depd44f04xc4/1/web/1.0

**TRANSFER VALIDATION:** device lifecycle transitions can preserve some software/data while changing management authority. This reinforces `bits remain/return ≠ old exception authority remains`; it does not prove any current LogMate deployment topology.

## SYNTHESIS 1 — expiry revokes exceptional authority, not data existence
When an exception reaches its expiry/review boundary, its exceptional permission becomes non-current unless a separately authorized extension or successor decision exists. Expiry does not prove the route disappeared and does not authorize deletion of unique data.

Useful states include `EXCEPTION-CURRENT`, `EXPIRING`, `EXPIRED-RECOVERY-ONLY`, `NORMALIZATION-PENDING`, `SUCCESSOR-CURRENT`, `PREDECESSOR-FENCED`, `REMOVAL-PENDING`, `RETIRED`, and `UNKNOWN/CONTRADICTED`.

Guards: `exception expired ≠ path disappeared`; `exception expired ≠ data disposable`; `expiry reached ≠ safe to execute queued work`.

## SYNTHESIS 2 — extension is a new authority decision, not timestamp editing
Extending an exception should create successor approval evidence with current scope, reason, authority, compensating controls, review/expiry and changed assumptions. Editing the original expiry in place destroys evidence about how long exceptional operation actually persisted.

Guards: `expiry extended ≠ original exception never expired`; `renewed exception ≠ permanent admission`.

## SYNTHESIS 3 — normalization needs successor proof and predecessor proof
A normal successor path N2 is not sufficient evidence that emergency path E1 is gone. Closure should distinguish at least:
1. successor admitted/current;
2. intended data/operations migrated or reconciled;
3. new writes to E1 fenced;
4. credentials/routes/scopes retired or bounded as applicable;
5. queued/retry/background work dispositioned;
6. offline/unknown tails governed;
7. predecessor rejection tested where controllable;
8. residual external/manual copies recorded.

Guard: `successor works ≠ predecessor retired`.

## SYNTHESIS 4 — removal proof is consequence-scoped
A low-consequence read-only emergency view may need weaker retirement evidence than a mutation/recovery-authority bridge. Removal proof should match the capability being retired: route rejection, credential revocation, write denial, queue drain/quarantine, configuration removal, old-version rejection, or governed residual state.

Guard: `one retirement check ≠ all capabilities retired`.

## SYNTHESIS 5 — telemetry silence is not removal proof
No observed traffic after cutover can support a retirement assessment but cannot prove an offline client, dormant queue, cached route, external recipient or manual procedure no longer exists.

Use explicit search space and bounded negative evidence. Long-tail unknowns remain visible until governed disposition.

Guard: `zero predecessor traffic ≠ predecessor impossible`.

## SYNTHESIS 6 — preserve unique offline data before fencing destructive paths
For a long-offline PWA/EFB client, authority may expire while unique records remain locally. Recovery should preserve records/provenance first, then fence obsolete mutation/publication, bootstrap current authority and revalidate individual operations.

Guard: `obsolete authority ≠ obsolete data`; `fence writes ≠ erase local store`.

## SYNTHESIS 7 — exception debt is an aggregate risk object
Exception governance fails if each exception is reviewed only in isolation. Maintain an aggregate view by service/path, capability, owner, credential/identity provider, vendor, runtime, data class, consequence, expiry, recurrence and shared failure domain.

Useful signals include count, age, extension count, recurrence interval, overlapping duration, same-root credential dependence, same operator dependence, percentage of critical workflows using exceptions and predecessor-retirement backlog.

These are risk signals, not automatic severity scores.

Guard: `each exception bounded ≠ aggregate exception risk bounded`.

## SYNTHESIS 8 — repeated exceptions can reveal architectural substitution
If the same emergency route is repeatedly reopened, the system may have an unmet normal-path requirement rather than a sequence of unrelated emergencies. Repetition should trigger architecture review, not silent renewal.

Possible dispositions: build/admit a durable normal path, redesign the workflow, accept a documented residual risk under appropriate authority, or retire the capability.

Guard: `repeated temporary need ≠ still temporary by definition`.

## SYNTHESIS 9 — concentration changes risk even when every exception is valid
Ten individually justified exceptions can share one credential issuer, operator, provider, export channel or recovery bridge. A compromise/outage there can invalidate multiple supposedly independent controls simultaneously.

Use the dependency/concentration model from 127–130: different exception IDs do not imply independent failure domains.

Guards: `many exceptions ≠ diversified risk`; `different tickets ≠ different failure domains`.

## SYNTHESIS 10 — exception authority must not self-renew from runtime necessity
A component that would fail when its exception expires cannot use that failure as automatic proof that it should remain authorized. Runtime necessity is evidence of dependency/debt and may justify emergency escalation, but renewal remains an authorized governance decision.

Guard: `service would break ≠ exception auto-renews`.

## SYNTHESIS 11 — predecessor fencing should survive restart/restore/rejoin
A path that appears retired until a browser restart, backup restore, Service Worker activation, old app/PWA rejoin or offline queue replay is not robustly retired.

Negative validation should cover applicable restart/restore/rejoin boundaries and verify that predecessor authority does not resurrect while recoverable data remains recoverable.

Guard: `disabled in current session ≠ retired across lifecycle`.

## SYNTHESIS 12 — Service Worker/cache cleanup is not the authority model
Deleting a Service Worker registration or Cache Storage entry may be part of cleanup, but organizational authorization and server-side acceptance must not depend solely on client cleanup succeeding. An old client can be offline during cleanup.

Guard: `Service Worker removed ≠ old authority impossible`; `cache cleared ≠ server rejects predecessor`.

## SYNTHESIS 13 — manual and external emergency paths need closure semantics too
Emergency spreadsheets, email exports, printed reports, support handoffs or third-party transfers can outlive their exception. Where technical deletion is impossible, closure should record notification/replacement/remediation obligations and residual external-copy state rather than claiming universal erasure.

Guard: `workflow closed ≠ every external copy erased`.

## SYNTHESIS 14 — expiry failure creates explicit debt, not silent grace
If normalization cannot complete by expiry, do not silently treat the exception as current. Record `EXPIRED/UNDER-REVIEW` or an explicitly authorized successor exception. Consequence-bearing operations should follow the approved degraded/recovery policy.

Guard: `missed expiry ≠ implicit grace period`.

## SYNTHESIS 15 — exception debt needs ownership and retirement SLOs, not vanity counts
Raw exception count can be misleading. A useful operational view includes accountable owner, consequence, oldest age, next review, normalization blocker, predecessor-removal status and concentration. Thresholds should be risk-based and product-specific rather than invented generically.

Guard: `exception count down ≠ risk down`.

## SYNTHESIS 16 — closure must preserve history
When E1 is normalized into N2, retain the original exception, extensions, migration/reconciliation, successor admission, predecessor fencing and residual-debt evidence. Do not rewrite E1 as if N2 had always existed.

Guard: `normalized now ≠ originally normal`.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. model exception expiry as authority expiry, not data deletion or path disappearance;
2. make extensions successor governance events rather than editing history;
3. require both positive successor evidence and consequence-scoped predecessor fencing/removal evidence;
4. preserve unique local data/provenance before disabling obsolete mutation/publication;
5. keep offline/unknown fleet tails explicit during retirement;
6. aggregate exception debt by recurrence, age, overlap and common failure domains;
7. escalate repeated exceptions into architecture review instead of indefinite renewal;
8. ensure server/authority-side rejection does not depend solely on Service Worker/cache/client cleanup;
9. validate retirement across applicable restart/restore/rejoin paths;
10. keep product/backend/MDM/domain/legal implementation facts OPEN until canonical evidence exists.

## EFB / LogMate-like application case
Assume emergency queue E1 was temporarily authorized for a company iPad fleet during an outage. Normal queue N2 is later deployed and admitted. One iPad remains offline past E1 expiry with unique flight records and E1 queued operations.

Safe generic sequence:
1. mark E1 authority expired for new consequence-bearing execution; do not infer E1 has disappeared;
2. on returning iPad, preserve unique records, queue contents and provenance before mutation;
3. bootstrap current device/incarnation/session/policy authority independently of E1;
4. classify each E1 queued operation under current policy and N2 identity/dedup/conflict rules;
5. admit/rebase only current-valid operations through N2; quarantine/reject others without deleting unique source records;
6. verify server-side predecessor rejection/fencing for E1 where controllable;
7. inspect applicable Service Worker/cache/IndexedDB/retry surfaces for residual E1 references without treating cleanup as authority proof;
8. update fleet-tail/exception-debt state and retain unknown devices until governed retirement/rejoin;
9. test restart/restore/rejoin paths for E1 resurrection;
10. close E1 only with successor-current plus predecessor-fenced/removal/residual-state evidence appropriate to consequence.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
865. **Expiry-equals-deletion** — exception expiry triggers deletion of unique offline records. Expected: fail.
866. **Successor-only closure** — N2 works, so E1 is marked retired without predecessor rejection/fencing evidence. Expected: fail.
867. **Telemetry-silence retirement** — zero E1 traffic is treated as proof no offline/dormant E1 consumer remains. Expected: fail.
868. **In-place exception extension** — original expiry is overwritten, erasing renewal/debt history. Expected: fail.
869. **Repeated-exception normalization theater** — same emergency path is repeatedly renewed without architecture review. Expected: fail.
870. **Exception-ID diversification theater** — many exception IDs sharing one credential/provider/operator are counted as independent risk. Expected: fail.
871. **Client-cleanup authority theater** — Service Worker/cache cleanup is treated as sufficient proof obsolete authority cannot execute. Expected: fail.
872. **Restore-resurrected predecessor** — backup/restore or rejoin restores E1 execution after retirement while closure remains marked complete. Expected: fail.

**VALIDATION:** these are defined destructive cases only. Execution PASS is not claimed.

## OPEN / VALIDATION
- Actual MintTap/LogMate exception authority, topology, queues, server rejection, MDM, fleet and Service Worker behavior remain OPEN.
- Product-specific expiry/review periods, risk thresholds, retirement SLOs and aviation/safety/legal consequences remain OPEN.
- Physical iOS/iPadOS installed-PWA, managed-device restore/rejoin and long-offline behavior remain OPEN.
- Human/AT comprehension of expiry/recovery-only/normalization states remains OPEN.
- Actual exception-debt concentration and provider/credential/operator common-mode dependencies remain OPEN.

## CHANGE WATCH
- NIST SP 800-53/CSF revisions affecting configuration/risk governance.
- Apple Platform Deployment changes for Return to Service, restore, managed-app preservation and enrollment behavior; current Apple documentation is version/enrollment-specific.
- WebKit/iOS/iPadOS PWA storage, Service Worker and lifecycle behavior.
- Canonical LogMate/MintTap implementation evidence when available.

## Next high-value target
**265 — exception-debt budget, renewal-authority separation & forced architecture-review triggers.** Determine how to govern aggregate temporary-authority debt without arbitrary quotas; prevent the same authority from indefinitely renewing its own exception; define consequence-aware escalation triggers; and distinguish legitimate prolonged contingency from normalization failure while preserving offline recovery paths.