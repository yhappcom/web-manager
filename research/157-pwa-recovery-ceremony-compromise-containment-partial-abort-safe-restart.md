# 157 — PWA Recovery-Ceremony Compromise Containment, Partial Abort & Safe Restart

Status: **PASS (generic) / PRODUCT + ORGANIZATION + IDENTITY + PROVIDER + MANAGED-IPAD + CEREMONY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 154 authority-floor disaster recovery; 155 custody/succession; 156 ceremony target/human-factor binding; Track A browser/session/SW mechanics; Track B abort/restart UX; Track C destructive validation; Track D diagnostics only.

## Why this study exists

156 made a recovery ceremony target-bound, participant-bound and non-replayable. A remaining high-risk case is discovery of compromise or contradiction **after** some approvals, shares, temporary credentials or recovery-side effects already exist. A naive restart can accidentally carry predecessor approvals forward, leave temporary authority executable, destroy evidence, or permanently lock the organization out.

The objective is to make abort a first-class security transition: contain the compromised attempt, preserve evidence without preserving executable authority, invalidate predecessor approvals, reconcile side effects, and start a new ceremony only from a fresh authoritative generation.

## SOURCE

### NIST SP 800-61 Rev. 3 — incident response is integrated risk management
NIST finalized SP 800-61 Rev. 3 in April 2025 and superseded Rev. 2. The current model integrates incident response with CSF 2.0 risk management across organizational operations rather than treating response/recovery as an isolated technical sequence.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

Transfer: a compromised recovery attempt is itself an incident state requiring containment and governed recovery, not merely a failed form submission.

### NIST SP 800-53 Rev. 5 — recovery/reconstitution returns to known state and retires interim capability
NIST's current SP 800-53 Rev. 5 family includes contingency and incident-response controls. NIST's reconstitution definition explicitly includes deactivation of interim capabilities used during recovery, assessment of restored capability, reestablishment of continuous monitoring and potential reauthorization.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/glossary/term/reconstitution

Transfer: a ceremony cannot be considered safely closed merely because the intended service is responding. Temporary recovery authority must be retired and the resulting state reassessed.

### OWASP Transaction Authorization — restart after failed authorization; enforce ordered state and final gate
OWASP's Transaction Authorization Cheat Sheet requires controlled sequential state transitions, operation-unique authorization, bounded validity and a final authorization check tied to execution. It also states that after a configured number of failed authorization attempts, the entire transaction-authorization process should restart.

Source:
- https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html

Transfer: recovery approvals are not timeless credentials. Restart creates a new authorization attempt; old approvals cannot be silently imported into it.

### OWASP security-relevant transition testing
OWASP Web Security Testing guidance for security-relevant feature transitions warns that stale assertions captured before a kill switch/transition must not remain trusted and that partial rollout can create inconsistent enforcement.

Source:
- https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/15-Feature_Flag_Security_Bypass/

Transfer: abort state must be authoritative across evaluators; a stale node/client must not continue executing ceremony N after ceremony N is aborted.

## SYNTHESIS — abort is a monotonic authority transition

A ceremony should have explicit states such as:

`CREATED → VERIFYING → PARTIALLY-APPROVED → EXECUTING → RECONCILING → CLOSED`

with terminal/non-forward states such as:

`DENIED`, `EXPIRED`, `ABORTED-SUSPECTED-COMPROMISE`, `ABORTED-CONTRADICTION`, `ABORTED-TECHNICAL-INTEGRITY`, `QUARANTINED`.

Exact implementation is product-specific. The generic invariant is stronger:

> Once an authoritative ceremony generation enters an abort/terminal state, predecessor approvals and temporary authority from that generation must never regain execution authority through retry, cache, replica lag, restore, client replay or a later ceremony.

Persistent guards:
- `abort recorded ≠ partial authority neutralized`;
- `new ceremony created ≠ old ceremony contained`;
- `old approval authentic ≠ old approval executable after abort`;
- `same incident ≠ same ceremony generation`;
- `same target/package ≠ approval carry-over permitted`;
- `temporary credential revoked ≠ all derived sessions/tokens neutralized`;
- `rollback attempted ≠ side effects reversed`;
- `evidence preserved ≠ executable credential preserved`;
- `service restored ≠ recovery ceremony safely closed`;
- `client UI says aborted ≠ server authority aborted`.

## Abort triggers and consequence classes

Abort is appropriate when continued authorization confidence is materially broken, for example:
- participant/custodian compromise or suspected impersonation;
- target/environment/package/checkpoint contradiction;
- custody/succession generation mismatch;
- approval transcript or integrity failure;
- discovery that a supposedly independent verification path shares the compromised failure domain;
- unexpected temporary authority, derived token or execution outside the declared consequence;
- authoritative state disagreement that cannot be safely reconciled in-place.

A recoverable transport/UI failure is not automatically a compromise abort. The system should distinguish retryable technical failure from loss of authorization confidence so operators do not normalize unnecessary restarts or, worse, treat compromise as an ordinary retry.

## The abort barrier

A safe abort has four logically separate obligations.

### 1. Stop new consequential effects
The authoritative server/control plane rejects further approvals, share admission, temporary-authority minting and consequential execution for the aborted ceremony generation. UI disablement is only presentation.

### 2. Revoke or quarantine partial authority
Inventory temporary credentials, leases, sessions, tokens, role grants, generated keys, recovery channels and other derived authority. Revoke/rotate or quarantine according to consequence. If revocation completeness cannot yet be established, authority remains UNKNOWN/contained rather than assumed clean.

### 3. Reconcile already-created effects
Some operations are irreversible or externally visible. Do not model abort as database rollback unless atomic rollback is actually proven. Classify each effect as:
- not committed;
- committed and reversible;
- committed and compensatable;
- committed and irreversible;
- state unknown pending reconciliation.

For authority-changing operations, uncertainty does not become permit.

### 4. Preserve forensic evidence safely
Retain enough non-secret evidence to reconstruct who/what/when/which generation and which side effects occurred. Quarantine does not mean retaining reusable shares, bearer tokens or approval credentials in logs.

## Approval invalidation and no carry-over

A restart is a **new ceremony generation** with a new identifier/nonce and fresh currentness checks. It may reference the same incident and target for continuity, but old approvals are historical evidence only.

A participant who approved ceremony N must approve N+1 again if their role is still required. This prevents:
- laundering an attacker-influenced approval into a clean attempt;
- combining partial quorums across generations;
- replaying an approval after target/package changes;
- bypassing a newly learned compromise fact.

The restart may reuse non-authoritative investigation facts after validation. It must not reuse executable authorization artifacts.

## Partial side effects: transaction semantics over rollback theater

Recovery can cross systems that do not share one atomic transaction. Therefore `abort` does not imply `everything returned to the exact prior state`.

A safe model uses an effect ledger keyed to ceremony generation and operation identity. Before restart, consequence-bearing effects are reconciled to an explicit state. Compensation creates new provenance; it does not erase the original event.

If a temporary key was used to sign or authorize an irreversible external action before abort, revoking the key stops future authority but cannot pretend the prior action never happened. Investigation and downstream containment remain necessary.

## Safe restart preconditions

Generic restart requires evidence that:
1. predecessor ceremony is terminal and rejected by authoritative execution paths;
2. known temporary/derived authority is retired, quarantined or explicitly bounded;
3. unresolved side effects are identified and cannot silently execute under the new generation;
4. current custody/succession/authority floor is re-established;
5. the triggering contradiction/compromise is resolved or isolated enough for the declared consequence;
6. participants and verification channels are freshly evaluated;
7. a new ceremony generation/nonce is created;
8. predecessor approvals/shares/tokens are non-executable;
9. monitoring/audit can distinguish N from N+1;
10. the new attempt does not weaken policy merely to escape the failed attempt.

If these cannot be established, the system remains in containment/manual recovery rather than creating a permissive restart loop.

## Avoid permanent lockout

Fail-closed behavior can itself create a recovery deadlock. The solution is not to reactivate the compromised ceremony. The recovery architecture should have an independently governed path to establish a **new** clean generation from the surviving authority floor/custody model.

This preserves two properties simultaneously:
- predecessor authority cannot resurrect;
- legitimate recovery remains possible after containment.

If no independent clean-start path exists, that is an architecture defect to surface in exercises rather than a reason to carry old approvals forward.

## Replica, cache and backup behavior

Abort is authority-bearing negative state. It must survive:
- evaluator/replica lag;
- application rollback;
- backup/PITR restore;
- stale browser/PWA cache;
- old Service Worker control;
- delayed offline queue replay.

A stale replica that still believes ceremony N is executable must not be an alternate authorization oracle. Anti-resurrection/authority-floor rules from 153–154 apply.

## PWA / Service Worker / managed-iPad application

For a LogMate/EFB-like PWA:
- an offline/stale Service Worker may continue rendering ceremony-N UI, but cannot make N authoritative after server-side abort;
- cached `approved` state is never sufficient for consequential server mutation;
- queued ceremony-N approval/mutation messages reconnecting later are rejected as historical/aborted generation, not upgraded to N+1;
- unique local flight data remains preservable/exportable during ceremony containment;
- local operational data should not be deleted merely because organizational recovery failed;
- reconnect must separate data reconciliation from recovery-authority reconciliation;
- a physical iPad containing evidence/data is not automatically a clean recovery endpoint or participant.

Actual WebKit/MDM/background/network behavior remains OPEN until runtime validation.

## Cross-track integration

### Track A — Platform & Browser
Owns exact browser/SW/cache/session/WebAuthn behavior. Transfer: local UI/session state cannot override authoritative abort generation; browser persistence must be tested for stale replay paths.

### Track B — UX / IA / Content
Owns truthful `ABORTING`, `ABORTED`, `QUARANTINED`, `RESTART REQUIRED`, `MANUAL RECOVERY REQUIRED` states. The interface must not show success while derived authority is unresolved and must preserve a safe path for local-data export where permitted.

### Track C — Performance / Accessibility / Quality
Owns destructive validation across replica lag, retry storms, accessibility, interrupted network, stale SW, delayed queue replay and partial external effects. Tests must prove negative authorization after abort, not merely absence of a button.

### Track D — Search / Discovery / Analytics
May detect abnormal restart/abort rates and help incident diagnostics. Telemetry cannot establish that derived authority is fully revoked or that a restart is legitimate.

### Track E — Owner
Owns abort semantics, containment barrier, effect reconciliation, generation invalidation, safe restart prerequisites and anti-resurrection governance.

## MINTTAP DECISION — minimal sufficient generic model

If consequential recovery ceremonies exist:
1. model abort as authoritative monotonic state, not UI cancellation;
2. bind every approval/effect to a unique ceremony generation;
3. invalidate all predecessor approvals on abort; never merge quorum across generations;
4. inventory and neutralize/quarantine derived temporary authority before declaring clean restart;
5. reconcile partial effects explicitly; do not claim rollback where distributed atomicity is absent;
6. preserve forensic provenance without retaining reusable recovery secrets;
7. restart only as a new generation with fresh target/package/currentness/participant verification;
8. make stale replicas, backups, Service Workers and offline queues unable to resurrect aborted authority;
9. preserve irreplaceable local PWA/iPad data independently of ceremony authority;
10. require post-abort and post-restart negative authorization tests for predecessor/emergency artifacts.

## VALIDATION — 60-case compromise/abort/restart campaign

1. abort before any approval; 2. abort after one approval; 3. abort one short of quorum; 4. abort immediately after quorum; 5. abort during temporary-token mint; 6. abort after token minted; 7. abort after token used once; 8. abort after reversible effect; 9. abort after irreversible external effect; 10. participant compromise discovered; 11. participant merely unavailable; 12. target mismatch; 13. package mismatch; 14. stale authority floor; 15. transcript tamper; 16. correlated OOB channel discovered; 17. false-positive suspicion resolved; 18. transport failure remains retryable; 19. client says abort but server never receives it; 20. server aborts while client offline; 21. stale replica accepts N; 22. replica catches up; 23. app rollback predates abort; 24. PITR restore predates abort; 25. anti-resurrection floor rejects N; 26. old approval replay; 27. old share replay; 28. old bearer token replay; 29. old session-derived authority replay; 30. old signed assertion replay; 31. N approval submitted to N+1; 32. same participant freshly approves N+1; 33. partial quorum from N combined with N+1; 34. rejected; 35. restart uses same incident but new generation; 36. restart changes package; 37. restart changes target; 38. restart changes custody generation; 39. unresolved side effect blocks automatic restart; 40. compensating action recorded as new provenance; 41. irreversible effect preserved for investigation; 42. derived key rotated; 43. emergency role removed; 44. temporary session revoked; 45. negative test proves N fails; 46. N+1 succeeds only with fresh approvals; 47. audit distinguishes N/N+1; 48. audit contains no reusable secret; 49. telemetry unavailable but authority still fails closed; 50. stale SW renders N; 51. server rejects N; 52. offline queue replays N; 53. queue is quarantined/not upgraded; 54. local flight data remains exportable where policy permits; 55. local data not mistaken for authority evidence; 56. keyboard/zoom/reflow/AT exposes abort/restart truth; 57. repeated aborts trigger investigation rather than weaker policy; 58. no clean-start path reveals architectural deadlock; 59. independently governed clean-start path establishes new generation; 60. full exercise demonstrates predecessor authority cannot resurrect while legitimate recovery remains possible.

## CONTRADICTION / failure-mode analysis

### UI-cancel theater
Disabling the button or showing `Cancelled` does not revoke server-side or derived authority.

### Database-rollback theater
Distributed recovery side effects may already be externally committed. Compensation and provenance are often required; pretending atomic rollback occurred destroys evidence and can hide residual authority.

### Fresh-ID theater
Creating N+1 is not safe if N tokens/approvals still execute. Generation freshness and predecessor containment are separate obligations.

### Approval-reuse convenience
Carrying `already approved` participants into N+1 weakens the purpose of abort and can launder compromised approvals across attempts.

### Delete-the-evidence containment
Deleting all N records can remove forensic truth without neutralizing authority that escaped elsewhere. Evidence preservation and credential neutralization are separate.

### Fail-closed-forever
A system that can only recover by reactivating the compromised generation has not designed a survivable recovery path. Clean-start authority must be independent enough to preserve anti-resurrection without permanent lockout.

## OPEN

Product/runtime evidence is required for:
- actual ceremony and effect schemas;
- authoritative abort/terminal-state storage and replication semantics;
- temporary credentials/roles/leases/tokens and revocation topology;
- cross-service transaction/compensation boundaries;
- actual identity/custody/succession providers;
- backup/PITR restore interaction with abort state;
- audit retention/redaction/key management;
- Service Worker/offline queue implementation;
- managed-iPad/WebKit/MDM behavior;
- accessibility/human performance under incident stress;
- legal/employment/aviation constraints.

No production PASS is claimed.

## CHANGE WATCH

- NIST SP 800-61 Rev. 3 remains the current final incident-response baseline as of 2026-09-19 and supersedes Rev. 2.
- NIST SP 800-53 Rev. 5 received Release 5.2.0 updates in August 2025; track subsequent control/catalog revisions.
- OWASP transaction/testing guidance is implementation guidance, not a substitute for product-specific authorization proof.
- Browser/WebKit/MDM/offline behavior requires current runtime evidence.

## Gate result

**PASS (generic).** The model now covers compromise discovery during an in-progress recovery ceremony, monotonic abort, partial-authority quarantine/revocation, effect reconciliation, evidence preservation, approval non-carry-over, anti-resurrection and independently governed safe restart. Production validation remains OPEN.

## Next highest-value adjacent target

**PWA recovery-ceremony effect reconciliation, compensation authority & irreversible-side-effect governance**: deepen the case where ceremony N already changed external systems before abort. Determine who may authorize compensation, how to prevent compensation from becoming a second unbounded emergency authority, how to preserve causality across original/compensating actions, and when an irreversible effect must be accepted/contained rather than falsely 'rolled back'.