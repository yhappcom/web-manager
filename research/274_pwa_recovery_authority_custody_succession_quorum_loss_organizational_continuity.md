# 274 — PWA Recovery-Authority Custody Succession, Quorum Loss & Organizational Continuity

Status: **PASS (generic) / PRODUCT + PERSONNEL + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline rejoin mechanics; Track B truthful recovery UX; Track C destructive validation; Track D bounded continuity diagnostics.  
Dependencies: 260–273 dependency/topology/re-entry/revocation/rotation/emergency-reset/recovery-root governance.

## Problem

273 established that a recovery root is itself a high-consequence authority and must survive the actual compromise domain, remain bounded during emergency use, and be retired or returned to controlled standby afterward. The adjacent continuity failure is organizational rather than purely cryptographic: the recovery authority may be technically intact while the people, quorum, provider account, HSM access, identity plane, corporate control or documented procedure needed to use it is no longer available.

Central rule: **recovery authority is not operationally recoverable merely because key material still exists. Continuity requires current, authorized and independently survivable custody plus a tested succession path. Personnel/provider loss must not force the organization to choose between an unrecoverable cold root and a permanently shared/hot super-root.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Long-offline clients can retain obsolete recovery material through organizational transitions; runtime persistence cannot establish successor organizational authority.
- **B UX/IA/Content:** high dependency pressure. Recovery states must distinguish `data preserved`, `recovery authority unavailable`, `organizational reauthorization required`, `limited capability`, and `recovery restored` without claiming data corruption.
- **C Performance/Accessibility/Quality:** destructive campaign expands **944 → 952 defined cases**. Execution, physical-device, AT and human PASS remain OPEN.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures custody health, quorum reachability, stale-custodian attempts, provider dependency and unknown/offline tail; telemetry cannot appoint successor custodians.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns custody topology, succession, quorum-loss handling, provider/personnel concentration, reauthorization and post-transition retirement.

## SOURCE

### NIST SP 800-57 Part 1 Rev. 5 — recovery is a lifecycle function, not possession alone

NIST defines key recovery as mechanisms and processes that allow authorized entities to retrieve or reconstruct keys from backups/archives. Its recovery appendix notes that recovery commonly involves human assistance and that key metadata must be recoverable as well. It also distinguishes inaccessible material from suspected-compromised material and requires prompt replacement after recovery when compromise may have occurred.

Source: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**TRANSFER VALIDATION:** cryptographic key-recovery guidance is not a PWA custody architecture prescription. The reusable point is that authorization, process, metadata and human/organizational capability are part of recovery—not merely the existence of bytes.

**CHANGE WATCH:** SP 800-57 Part 1 Rev. 6 remains an Initial Public Draft dated 2025-12-05; Rev. 5 remains the final publication at this checkpoint.

### NIST split knowledge — availability and unilateral control are different problems

NIST defines split knowledge as dividing a key into shares so that fewer than the required threshold reveal no information about the key. This is useful bounded precedent for separating unilateral custody from reconstructability.

Source: https://csrc.nist.gov/glossary/term/split_knowledge

**TRANSFER VALIDATION:** split knowledge, threshold signatures and organizational multi-party approval are not interchangeable. MintTap/LogMate has no selected mechanism. The reusable principle is that recovery design can avoid one-person unilateral possession while still planning for loss of individual custodians.

### NIST SP 800-57 Part 2 Rev. 1 — institutional key management requires policy, practices and planning

Part 2 identifies institutional key-management concepts, security planning, specifications, policy and practice-statement requirements for centralized and decentralized structures.

Source: https://doi.org/10.6028/NIST.SP.800-57pt2r1

**TRANSFER VALIDATION:** the durable lesson is organizational: custody and recovery need documented roles, procedures and planning that survive personnel/provider change. This does not establish a particular quorum size or provider.

**CHANGE WATCH:** NIST marks Part 2 Rev. 1 as under review as of 2025-07-01.

### CISA cloud guidance — emergency administration should remain protected and may require multiple users

CISA TIC 3.0 cloud guidance describes emergency `break glass` administrator accounts as strongly protected, recommends separation of duties, suggests coordination of multiple users for emergency access, and emphasizes logging/auditing.

Source: https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

**TRANSFER VALIDATION:** this is federal cloud guidance, not a universal PWA design. It supports the bounded principle that emergency access should not collapse into an ordinary single shared credential.

## SYNTHESIS 1 — custody is a graph, not a person name

Recovery availability depends on more than a named custodian. Model at least the authority object, required approvals/shares, authenticators, HSM/provider account, identity/recovery plane, physical or logical storage, procedure, organizational authorization and current successor relationships.

Guards:
- `key exists ≠ recovery available`;
- `custodian listed ≠ custodian reachable ≠ custodian authorized`;
- `two custodians ≠ two independent failure domains`.

## SYNTHESIS 2 — personnel loss and credential compromise are different states

Departure, death, leave, incapacity or loss of employment authority does not prove compromise, but it invalidates assumptions about availability and authorization. Conversely, a still-employed custodian can be compromised. Succession must classify both dimensions separately.

Guards:
- `custodian unavailable ≠ key compromised`;
- `custodian employed ≠ custodian trustworthy/current`;
- `credential works ≠ former custodian still authorized`.

## SYNTHESIS 3 — succession is an authority transition

Replacing Alice with Bob is not merely handing Bob a password/share. The organization must establish Bob's current role/authorization, transfer or regenerate custody according to the mechanism, retire Alice's consequence-bearing access, preserve provenance, and update quorum/recovery metadata.

Guards:
- `credential handoff ≠ authority succession`;
- `new employee added ≠ old employee retired`;
- `same recovery secret copied ≠ clean succession`.

## SYNTHESIS 4 — quorum loss must fail differently from quorum compromise

If a 2-of-3 recovery arrangement loses one custodian but retains a valid 2-of-2 reachable subset, continuity may remain possible. If too few authorized participants remain, the organization has **quorum loss**, not permission to lower the threshold ad hoc. If a participant is suspected compromised, simply counting that participant toward the threshold can be unsafe.

Guards:
- `quorum unavailable ≠ threshold may be silently lowered`;
- `quorum numerically satisfied ≠ quorum trustworthy`;
- `emergency pressure ≠ unilateral authority justified`.

Actual quorum size/mechanism remains product-specific and OPEN.

## SYNTHESIS 5 — do not solve cold-root fragility with a permanent shared hot credential

A shared password stored in routine team tooling may improve apparent availability while destroying attribution, separation, compromise containment and retirement quality. A recovery mechanism should be reachable enough to test and use, but not normalized into daily administration.

Guards:
- `easy to reach ≠ safe to keep hot`;
- `shared credential ≠ resilient quorum`;
- `everyone can recover ≠ organizational continuity`.

## SYNTHESIS 6 — succession needs spare capacity before failure

A quorum that requires every current custodian has no tolerance for ordinary absence. Continuity planning should account for simultaneous leave, termination, regional outage, device loss and provider support delay appropriate to consequence. This does not imply maximal redundancy; it means the recovery objective and failure model must be explicit.

Guard: `quorum works today ≠ quorum survives one expected loss`.

## SYNTHESIS 7 — provider loss is a custody event when the provider is on the trust path

An HSM/KMS/IdP/cloud account can be part of the recovery authority even when key material is nominally separate. Account suspension, provider outage, organization-transfer failure or loss of billing/domain/identity control can make recovery unusable.

Guards:
- `key stored externally ≠ provider-independent recovery`;
- `multi-user provider account ≠ provider-loss tolerance`;
- `backup of key bytes ≠ backup of provider authorization context`.

Provider portability and actual MintTap/LogMate topology remain OPEN.

## SYNTHESIS 8 — corporate-control change requires reauthorization, not inherited superuser status

Acquisition, legal-entity change, ownership transfer or administrative-domain migration can alter who is entitled to exercise emergency authority. Technical continuity must not automatically grant the new operator all old emergency consequences, nor should it destroy historical verification evidence.

Guards:
- `organization renamed/transferred ≠ authority automatically transferred`;
- `provider tenant transferred ≠ emergency mandate transferred`;
- `historical verifier retained ≠ former organization retains current authority`.

Legal/company-specific rules remain OPEN.

## SYNTHESIS 9 — succession records need anti-rollback and provenance

A backup or long-offline client can remember an obsolete custodian set. Current authority should bind custody generation/epoch or equivalent currentness evidence so restored state cannot reinstate a departed custodian or old threshold.

Guards:
- `old quorum metadata authentic ≠ old quorum current`;
- `PITR restores custodian set ≠ custodian set reauthorized`;
- `offline client remembers former custodian ≠ former custodian current`.

## SYNTHESIS 10 — recovery drills must exercise organizational loss, not only cryptography

A drill that proves shares reconstruct or an HSM signs does not prove continuity after a custodian leaves or a provider account is inaccessible. Useful drills can separately challenge custodian unavailability, quorum substitution, provider/account loss, successor appointment, obsolete-custodian rejection and return-to-standby/retirement.

Guards:
- `key reconstruction PASS ≠ succession PASS`;
- `HSM signing PASS ≠ provider-loss recovery PASS`;
- `runbook exists ≠ alternate custodian can execute it`.

## SYNTHESIS 11 — succession must preserve least consequence

A successor custodian should inherit only the recovery role/capability required, not every operational privilege held by a predecessor. Recovery authority and normal administration remain separate even if the same human sometimes occupies both roles.

Guard: `same person ≠ same authority context`.

## SYNTHESIS 12 — no viable quorum means governed rebootstrap, not improvisation

If no authorized trustworthy quorum remains and no pre-established independent succession path survives, the system has lost its recovery authority. The safe response may require bounded service degradation plus governed organizational rebootstrap from evidence outside the failed custody set. Do not manufacture legitimacy by changing policy in the failed plane.

Guards:
- `no quorum ≠ one person may declare quorum`;
- `business urgency ≠ trust basis`;
- `rebootstrap required ≠ delete unique data`.

## SYNTHESIS 13 — PWA/offline clients must not participate in organizational election by stale state

Service Worker, IndexedDB, Cache Storage or an installed PWA can preserve old recovery metadata. They can preserve records and provenance, but cannot appoint a successor custodian or roll the central custody generation backward.

Guards:
- `worker has old recovery object ≠ old custodian reauthorized`;
- `offline data preserved ≠ offline authority current`;
- `client reconnects first ≠ client elects recovery generation`.

## SYNTHESIS 14 — human accessibility matters during recovery without weakening authority

Recovery instructions and states must be operable under stress and accessible to authorized operators, but accessibility/usability improvements must not reveal secret material, collapse separation of duties or create ambiguous destructive actions. Actual human/AT validation remains OPEN.

## SYNTHESIS 15 — custody health is a maintained property

Useful periodic evidence can include authorized custodian roster/currentness, quorum reachability, independent failure-domain review, provider/account access health, succession readiness, obsolete-custodian rejection, drill recency and unresolved exceptions. Telemetry is evidence, not authority.

## PWA / LogMate-like EFB application case

Scenario: emergency authority Q2 requires multiple organizational custodians. One custodian leaves, another is on extended leave, and the cloud/HSM provider account is temporarily inaccessible. A six-week-offline company iPad returns with unique flight records plus Q1/Q2-era recovery metadata.

Safe generic sequence:
1. preserve unique local records, queue payloads and provenance before authority cleanup;
2. classify current custodian availability, authorization and compromise independently;
3. determine whether the current Q2 quorum remains both numerically satisfiable and trustworthy without silently reducing threshold;
4. fence high-consequence recovery/publication if no valid quorum or provider path exists while preserving safe local read/recovery capability;
5. use a pre-established independent succession/provider-loss path if one survives; otherwise invoke governed rebootstrap rather than improvising a shared superuser credential;
6. establish the successor custody generation and current organizational mandate;
7. retire departed/obsolete custodian authority and prove rejection at material recovery/admin boundaries;
8. reconcile current R/current-policy/schema/session/device incarnation and queued operations individually;
9. treat Q1/Q2-era metadata on the iPad as historical evidence, not an election mechanism;
10. return emergency authority to bounded standby and refresh succession/drill evidence.

This is a generic architecture pattern. It is **not** evidence that LogMate uses a particular quorum, HSM, MDM, provider or aviation-security architecture.

## Cross-track transfer

### Track A — Platform/Browser
**DEPENDENCY:** browser persistence can retain obsolete custodian/recovery metadata. Runtime freshness does not prove organizational succession. Preserve IndexedDB/Cache Storage data independently from operation/recovery authorization.

### Track B — UX/IA/Content
**TRANSFER VALIDATION:** recovery UX should distinguish `records safe`, `remote effects paused`, `authorized recovery team unavailable`, `organizational reauthorization required`, and `recovery restored`. Do not expose secret/quorum internals unnecessarily. Human/AT validation remains OPEN.

### Track C — Quality / destructive campaign
Add eight defined cases:
1. **Departed-custodian credential inheritance** — former employee credential still works; current authority must reject it.
2. **Ad-hoc quorum reduction** — 2-of-3 loses two members; operator lowers threshold to 1 without independent authority; fail closed for high consequence.
3. **Shared-hot-secret continuity theater** — team-shared break-glass password restores availability; do not count as resilient quorum/succession.
4. **Provider-account loss** — key bytes exist but HSM/KMS/IdP authorization context is unavailable; recovery availability must remain unproven.
5. **PITR custodian rollback** — backup restores former custodian roster/threshold; anti-rollback currentness must prevent resurrection.
6. **Offline-iPad custodian resurrection** — stale recovery metadata names old custodians; preserve records but reject stale organizational authority.
7. **Crypto-only drill theater** — shares reconstruct successfully but alternate custodian/provider-loss procedure cannot execute; continuity gate remains open.
8. **Corporate-transfer authority inheritance** — tenant/org transfer technically succeeds; emergency mandate must not transfer without governed reauthorization.

Campaign total: **952 defined cases**. This is definition coverage, not execution PASS.

### Track D — Discovery/Analytics
**DEPENDENCY:** observe roster/quorum health, provider reachability, stale-custodian attempts, succession completion and unknown/offline tail. Telemetry cannot appoint custodians, lower quorum or authorize corporate transfer.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate-like web/PWA requirements:
- model recovery custody as an authority/dependency graph, not a named person or secret location;
- distinguish custodian availability, current authorization and compromise;
- pre-plan succession and ordinary custodian loss without making emergency authority permanently hot;
- never silently lower quorum because people/providers are unavailable;
- include provider/IdP/HSM/account-control dependencies in recovery availability;
- bind custody changes to current generation/provenance and prevent PITR/offline rollback;
- preserve unique offline data independently of recovery-authority validity;
- test organizational-loss and successor-rejection paths, not only cryptographic reconstruction;
- keep actual quorum, provider, personnel, legal/aviation and product topology OPEN until canonical evidence exists.

## OPEN

Production validation remains OPEN for actual MintTap/LogMate recovery authority; custodian roles and staffing; quorum/threshold mechanism; HSM/KMS/IdP/provider topology; corporate/legal authority; provider portability; MDM/ADE/managed-iPad behavior; offline/session/sync architecture; backup/PITR anti-rollback reference; human/AT recovery UX; aviation/legal obligations; and runtime rejection of obsolete custodians.

## VALIDATION / gate

**Generic PASS** requires ability to distinguish possession from authorized recoverability, personnel loss from compromise, quorum loss from quorum compromise, succession from credential handoff, provider loss from key loss, and historical custody evidence from current authority; preserve data during authority failure; resist rollback/offline resurrection; and define destructive tests without claiming execution.

**Production PASS remains OPEN** until canonical runtime/project evidence demonstrates the selected custody/succession mechanism and consequence boundaries.

## Next high-value target

**275 — custody-generation transfer, stale-approver revocation & provider/org migration split-brain.** Determine how overlapping old/new custodian sets and provider/control-plane migrations establish one current organizational authority without permitting either stale side to self-elect, while preserving historical evidence and long-offline data.