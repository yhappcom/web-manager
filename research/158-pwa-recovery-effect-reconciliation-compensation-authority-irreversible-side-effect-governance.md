# 158 — PWA Recovery Effect Reconciliation, Compensation Authority & Irreversible-Side-Effect Governance

Status: **PASS (generic) / PRODUCT + PROVIDER + IDENTITY + MANAGED-IPAD + EFFECT-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 153 anti-resurrection; 154 disaster recovery; 155 custody; 156 ceremony binding; 157 abort/safe restart; Track A browser/SW/session mechanics; Track B truthful recovery UX; Track C destructive validation; Track D diagnostics only.

## Why this study exists

157 established that abort is not distributed rollback. The remaining high-value failure mode is what happens when ceremony N already changed one or more external systems before compromise/contradiction is discovered. A temporary role may have been granted, a key rotated, a provider configuration changed, a notification sent, a remote record mutated, or an irreversible action accepted by another authority domain.

The objective is to govern those effects without inventing rollback, without turning compensation into a second unbounded emergency authority, and without erasing causal evidence.

## SOURCE

### NIST SP 800-61 Rev. 3 — containment/recovery remain risk-managed incident work
NIST SP 800-61 Rev. 3 (final April 2025) integrates incident response with CSF 2.0 risk management. Recovery is not evidence that every pre-incident state can or should be recreated; organizations must restore operations while managing residual risk and learning from the event.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

Transfer: after an aborted recovery ceremony, effect reconciliation is an incident-recovery obligation. Restoring service does not prove that escaped authority or external effects have been neutralized.

### OWASP Transaction Authorization — authorization must be operation-specific and execution-bound
OWASP Transaction Authorization guidance requires authorization to be server-side, tied to the specific operation/data, time-bounded and checked at execution rather than treated as a reusable general approval.

Source:
- https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html

Transfer: a compensation command must have its own bounded authorization. The fact that an original recovery action was authorized does not create indefinite authority to perform any purported inverse later.

### Microsoft Azure Architecture Center — compensation is application-specific, may fail and does not necessarily restore the original state
Microsoft's current Compensating Transaction pattern states that distributed/eventually-consistent operations often cannot simply restore an old snapshot because concurrent work may have occurred. Compensation is application-specific, should retain enough information to undo effects, must be observable, may itself fail, and retryable compensation steps should be idempotent. It explicitly notes that compensation need not run in exact reverse order and that some operations are irreversible or require human decision.

Source (current page updated 2026-04-21):
- https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction

Transfer: compensation is a new governed forward action that seeks an acceptable state; it is not historical deletion or proof of exact rollback.

### AWS Prescriptive Guidance — saga compensation has isolation and observability limits
AWS Saga guidance describes compensation across local transactions, requires idempotency for repeated execution, notes that sagas lack transaction isolation, and recommends semantic locking where concurrent orchestration can expose stale data. It also emphasizes observability as participants increase.

Source:
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html

Transfer: compensation races with legitimate concurrent work and cannot assume the state observed at the original action still exists.

## SYNTHESIS — an effect is not a row; it is a consequence with authority and causality

For recovery governance, each consequence-bearing effect should be classified at least conceptually by:
- **effect identity** — stable operation/effect identifier;
- **ceremony generation** — which recovery attempt caused it;
- **target/authority domain** — local policy store, IdP, KMS, provider, remote API, human/legal process, etc.;
- **requested consequence** and **observed consequence**;
- **commit certainty** — not committed / committed / unknown;
- **reversibility class** — reversible / compensatable / irreversible / unknown;
- **current-state dependency** — what changed since the original effect;
- **compensation relation** — if any, a new action causally linked to the original;
- **authorization generation** for the compensation itself;
- **verification evidence** showing the resulting state.

Persistent guards:
- `abort recorded ≠ external effect reconciled`;
- `inverse API exists ≠ original effect safely reversible`;
- `compensation requested ≠ compensation authorized`;
- `compensation authorized ≠ compensation succeeded`;
- `compensation succeeded ≠ exact pre-effect state restored`;
- `retryable ≠ safe under changed state`;
- `idempotent command ≠ semantically valid compensation`;
- `same operator ≠ same authority for compensation`;
- `original approval ≠ compensation approval`;
- `rollback label ≠ rollback semantics`;
- `irreversible ≠ ignore`; `irreversible ≠ automatically catastrophic`;
- `local UI reconciled ≠ provider state reconciled`.

## Effect taxonomy

### 1. Uncommitted
Evidence establishes that the effect did not cross its authoritative commit boundary. No compensation is needed, but retry/replay must still be prevented if the ceremony is aborted.

### 2. Reversible
The target system provides a trustworthy inverse whose preconditions remain valid and whose application restores the relevant invariant without overwriting legitimate concurrent changes. Even here, the inverse is a new operation with its own authorization and audit trail.

### 3. Compensatable
Exact reversal is impossible or undesirable, but a new domain action can bring the system to an acceptable state. Example abstractions: revoke a grant rather than erase its historical issuance; rotate a key rather than recreate the old key; issue a correction rather than delete an already-observed event.

### 4. Irreversible
The effect cannot be undone in the relevant authority domain. Examples can include already-consumed external actions, disclosure, human communication, or signed/accepted external records. The response becomes containment, downstream notification/correction, residual-risk decision and provenance preservation rather than rollback theater.

### 5. Unknown
Commit/result cannot yet be established. For authority-changing operations, UNKNOWN is not treated as either success or safe absence. Reconciliation precedes permissive restart where consequence requires it.

## Compensation is a new authority-bearing transaction

A compensation operation should be bound to:
- the original effect identity and ceremony generation;
- a declared compensation type and bounded target;
- current target state/preconditions;
- current authority/custody/policy generation;
- an idempotency/retry identity where retries are possible;
- an expiry/currentness window where appropriate;
- explicit result verification.

The generic rule is:

> Compensation authority is derived from current governed recovery policy, not inherited from the compromised/original ceremony.

This prevents a dangerous pattern where `N was once allowed to create role X` is interpreted as `anyone handling N may later change role X however needed`.

## Prevent compensation from becoming a second emergency superuser

Compensation should be capability-scoped. A grant-revocation compensation may revoke the specific escaped grant; it should not imply general identity administration. A key-rotation compensation may retire a specific compromised key; it should not imply unrestricted KMS administration.

Where practical, authorization should distinguish:
- **investigate/reconcile** — read evidence/current state;
- **propose compensation** — construct intended bounded action;
- **authorize compensation** — approve declared consequence;
- **execute compensation** — perform only that action;
- **verify result** — independently confirm target state.

Exact organizational role count is product-specific; semantic separation is the reusable requirement.

## Causality and the effect ledger

Never overwrite the original effect with `reverted=true` as the only history. Preserve a causal chain such as:

`ceremony N → effect E1 → abort A1 → reconciliation R1 → compensation proposal C1 → authorization CA1 → compensation effect E2 → verification V1`

If E2 later fails or requires another correction, append that lineage. The projection may show `contained` or `compensated`, but the provenance must not imply E1 never happened.

This supports incident reconstruction, retry safety, provider dispute resolution and anti-resurrection checks.

## Concurrency and changed-state safety

Between E1 and compensation, legitimate actors may change the target. Therefore compensation must not blindly write the old snapshot back.

Before execution, validate current state and relevant version/precondition. Outcomes may include:
- expected state: execute declared compensation;
- already compensated: return/reconcile the existing result without duplicate side effect;
- changed but safely compensatable: require a newly evaluated compensation plan;
- conflicting legitimate work: quarantine/manual decision;
- target state unknown: do not guess.

Semantic locks/version checks can reduce races, but they do not replace current authorization or domain judgment.

## Retry and idempotency

A compensation workflow can fail midway. Durable progress and stable operation identity are required so a retry does not create another independent effect. Idempotency is necessary for many retryable steps but insufficient by itself: the target state may have changed, the authorization may have expired, or the compensation plan may no longer be semantically valid.

Therefore:
- retry uses the same compensation operation identity where it is truly the same operation;
- retry does not renew expired authority automatically;
- a changed compensation plan receives a new identity/authorization;
- an ACK loss is reconciled before issuing another side effect;
- provider `unknown` responses remain unknown until authoritative reconciliation.

## Irreversible-side-effect governance

An irreversible effect changes the goal from reversal to bounded containment and residual-risk management. The workflow should identify:
1. what cannot be undone;
2. what downstream authority/data/users may have relied on it;
3. what future authority can still be stopped;
4. what correction/notification/annotation is possible;
5. what evidence must remain;
6. who may accept residual risk or require escalation;
7. whether safe restart is blocked until a consequence-specific condition is met.

Do not use the label `compensated` merely because an operator acknowledged the incident. Acceptance and compensation are different states.

## Safe restart interaction

157's clean restart prerequisites now gain an effect-specific condition: a new ceremony must not silently proceed across an unresolved consequential effect when that effect can change the safety/meaning of the new attempt.

A restart may proceed with an irreversible residual effect only when current governance explicitly determines that:
- future authority is contained;
- the residual consequence is known enough for the next operation;
- required correction/notification/escalation has occurred or is independently tracked;
- the new ceremony does not pretend the residual effect disappeared.

This is consequence-scoped, not a universal requirement that every historical inconsistency be solved before any recovery work can continue.

## PWA / Service Worker / managed-iPad application

For a LogMate/EFB-like PWA:
- an offline queue containing ceremony-N compensation commands cannot execute merely because it was authored before abort;
- cached UI showing `reverted` cannot establish provider/server reconciliation;
- stale Service Worker code cannot broaden compensation authority;
- reconnect should distinguish local operational-data reconciliation from organizational recovery-effect reconciliation;
- unique local flight data remains preservable/exportable even if remote compensation is blocked;
- an irreversible remote sync or disclosure cannot be made reversible by deleting the local browser record;
- local correction records should preserve provenance rather than silently rewriting the history of what was previously synchronized.

Actual WebKit/MDM/background/network behavior remains OPEN until physical/runtime evidence exists.

## Cross-track integration

### Track A — Platform & Browser
Owns exact SW/cache/offline queue/session mechanics. Transfer: local retries and cached state cannot manufacture current compensation authority or provider reconciliation.

### Track B — UX / IA / Content
Owns truthful states such as `RECONCILING`, `COMPENSATION REQUIRED`, `COMPENSATION IN PROGRESS`, `COMPENSATED`, `IRREVERSIBLE — CONTAINED`, `UNKNOWN — MANUAL REVIEW`, and data-preservation/export paths. Do not present `Undone` unless the declared invariant was actually restored.

### Track C — Performance / Accessibility / Quality
Owns destructive testing across duplicate delivery, ACK loss, concurrency, stale SW, inaccessible incident UX, provider timeout and partial compensation. Quality evidence must verify authoritative target state, not only successful API/UI completion.

### Track D — Search / Discovery / Analytics
Telemetry can correlate effect/compensation rates and detect anomalous loops. Analytics cannot authorize compensation or establish provider truth.

### Track E — Owner
Owns effect taxonomy, compensation authority, causal ledger, irreversible-effect containment, restart gating and residual-risk boundaries.

## MINTTAP DECISION — minimal sufficient generic model

If consequential recovery effects exist:
1. give each effect durable identity and bind it to ceremony generation/target/consequence;
2. classify commit certainty and reversibility explicitly;
3. treat compensation as a new current-policy-authorized operation, never inherited emergency authority;
4. capability-scope compensation and separate investigation/proposal/authorization/execution/verification semantics where consequence warrants it;
5. preserve original→abort→compensation causal lineage rather than deleting/overwriting history;
6. validate current target state before compensation; do not restore stale snapshots over concurrent legitimate work;
7. make retry identity stable and reconcile ACK/result uncertainty before duplicate execution;
8. treat irreversible effects with containment/correction/residual-risk governance, not fake rollback;
9. prevent stale Service Workers/offline queues from replaying compensation or broadening authority;
10. preserve irreplaceable local PWA/iPad data independently of remote recovery-effect authority.

## VALIDATION — 64-case reconciliation/compensation campaign

1. abort before effect commit; 2. commit known; 3. commit unknown; 4. provider timeout before ACK; 5. ACK lost after commit; 6. duplicate compensation delivery; 7. idempotent duplicate; 8. non-idempotent downstream API; 9. current state unchanged; 10. legitimate concurrent state change; 11. attacker state change; 12. stale snapshot inverse attempted; 13. version/precondition rejects it; 14. reversible effect succeeds; 15. reversible inverse fails; 16. compensatable effect succeeds; 17. compensation partially succeeds; 18. compensation itself times out; 19. compensation result unknown; 20. retry same operation ID; 21. retry after authority expiry; 22. changed plan gets new authorization; 23. original approval presented as compensation authority; 24. reject; 25. old ceremony token presented; 26. reject; 27. broad admin role requested for narrow compensation; 28. reject/escalate; 29. investigate role cannot execute; 30. proposer cannot silently broaden consequence; 31. effect ledger links E1→C1→E2; 32. projection cannot erase E1; 33. provider says already compensated; 34. reconcile without duplicate action; 35. provider disagrees with local projection; 36. provider truth remains unresolved; 37. irreversible external disclosure; 38. future access contained; 39. correction/notification tracked; 40. irreversible signed external event; 41. historical event retained; 42. residual risk accepted by proper authority; 43. operator acknowledgement alone not compensation; 44. compensation races with restart; 45. consequence gate blocks unsafe restart; 46. unrelated low-risk residual does not globally deadlock recovery; 47. stale replica reissues C1; 48. dedupe/revocation rejects; 49. PITR restore predates compensation; 50. causal floor prevents resurrection; 51. stale SW shows `reverted`; 52. server/provider remains unresolved; 53. offline queue replays old compensation; 54. rejected/quarantined; 55. offline local flight data remains available; 56. local deletion cannot undo remote disclosure; 57. correction preserves provenance; 58. keyboard/focus/zoom/AT exposes true state; 59. telemetry missing but authority remains bounded; 60. audit contains no bearer recovery secret; 61. compensation worker crashes and resumes; 62. manual intervention path preserves identity/causality; 63. negative test proves original/emergency authority cannot execute new compensation; 64. end-to-end drill proves contained irreversible effect plus safe clean restart without rollback theater.

## CONTRADICTION / failure-mode analysis

### Inverse-API theater
An endpoint named `undo`, `delete` or `revoke` does not prove semantic reversal. Concurrent work, external observation or downstream derivation may make the original consequence non-reversible.

### Compensation-superuser
Granting a broad emergency administrator role because compensation is difficult creates a second recovery authority larger than the original consequence.

### Snapshot rollback
Writing the old snapshot over current state can destroy legitimate concurrent work and create a new incident.

### Idempotency theater
An idempotency key prevents some duplicate effects; it does not prove that the command is still authorized or semantically correct under current state.

### History erasure
Replacing E1 with `reverted` hides what happened and weakens forensics, dispute handling and anti-resurrection reasoning.

### Irreversible-equals-hopeless
Irreversibility does not mean no useful response exists. Future authority can often be stopped, downstream consumers corrected/notified, provenance retained and residual risk explicitly governed.

### Global fail-closed
One unresolved low-consequence effect should not automatically freeze unrelated local data preservation or every recovery capability. Gating follows consequence and dependency, not panic.

## OPEN

Product/runtime evidence is required for:
- actual external side-effect inventory and provider APIs;
- which effects are truly reversible, compensatable or irreversible;
- operation/effect/idempotency schema;
- authorization roles and compensation policy;
- provider commit/ACK/reconciliation semantics;
- concurrency/version/semantic-lock support;
- audit/provenance storage and retention;
- actual LogMate local/remote correction and sync model;
- Service Worker/offline queue behavior;
- managed-iPad/WebKit/MDM behavior;
- legal/employment/aviation consequences of irreversible actions.

No production PASS is claimed.

## CHANGE WATCH

- NIST SP 800-61 Rev. 3 remains the current final incident-response baseline as of 2026-09-19.
- Microsoft Azure Architecture Center's Compensating Transaction page is current as of 2026-04-21; architecture guidance may evolve.
- AWS saga guidance is implementation guidance and does not establish MintTap/LogMate provider semantics.
- OWASP transaction authorization guidance informs authorization design but does not substitute for product-specific proof.
- Browser/WebKit/MDM/offline behavior remains runtime-sensitive.

## Gate result

**PASS (generic).** The model now covers effect identity, commit certainty, reversibility classification, bounded compensation authority, current-state/concurrency validation, retry/idempotency limits, causal provenance, irreversible-side-effect containment and PWA stale-client boundaries. Production validation remains OPEN.

## Next highest-value adjacent target

**PWA recovery-effect closure proof, downstream dependency reconciliation & residual-risk acceptance expiry**: define when an effect may legitimately move from `RECONCILING` to `CLOSED`, how downstream systems/consumers that observed an escaped effect are enumerated and reconciled, how evidence proves containment rather than merely local success, and how temporary residual-risk acceptance expires/revalidates instead of becoming permanent silent debt.