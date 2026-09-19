# 151 — PWA Policy Rollout Cohort Integrity, Cross-Generation Transaction Consistency & Split-Policy Convergence

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + TRANSACTION/POLICY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 149 policy composition/deadlock; 150 rollout/shadow/diff; Track A SW/runtime-generation mechanics; Track B truthful revalidation/convergence UX; Track C cross-generation destructive validation; Track D aggregate rollout diagnostics only.

## Why this study exists

150 made candidate rollout bounded and observable. Partial rollout creates a harder problem: one logical operation can span requests, devices, retries, workers and policy-store replicas while different policy generations are authoritative in different places. A client can also remain offline across several generations. Without explicit invariants, a sequence of individually permitted steps can become a cross-generation privilege escalation or a half-authorized transaction.

The objective is to preserve authorization meaning across a logical transaction, prevent client-selected downgrade, tolerate provider propagation lag without pretending it is atomic, and converge long-offline PWAs without converting legacy compatibility into authority.

## SOURCE

### Authorization is a server-side transaction property
OWASP Transaction Authorization requires authorization to be enforced server-side, transaction data to be protected against modification, allowed state transitions to be controlled, and a final execution gate to verify that the transaction was properly authorized. It explicitly calls out TOCTOU and downgrade risks when authorization methods or transaction data change.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html

### Managed authorization state can be eventually consistent
Amazon Verified Permissions documents eventual consistency: a new or changed policy-store element can take seconds to propagate. Policy-template changes are reflected in linked-policy authorization decisions within those eventual-consistency constraints. This is concrete evidence that a managed authorization service must not be assumed to switch every evaluator atomically at one instant.

Sources:
- https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_CreatePolicyStore.html
- https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyTemplate.html

### Retry identity does not by itself define authorization semantics
The current IETF HTTPAPI Idempotency-Key draft defines a unique key/fingerprint pattern so a resource can recognize retries of the same non-idempotent request. It is useful transfer evidence for retry identity, but it does not define a product's authorization-generation or multi-step transaction semantics.

Source: https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07

### Service Worker generations can overlap with document generations
The Service Worker lifecycle normally lets an old worker continue controlling open pages while a new worker waits; `skipWaiting()` can activate a waiting worker immediately, and `clients.claim()` can make an active worker control existing clients. This means application/document/SW generation transitions must not be equated with one atomic server-policy transition.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting
- https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim

## SYNTHESIS — distinguish four consistency scopes

Do not ask for a vague `consistent rollout`. Separate:

1. **REQUEST CONSISTENCY** — one authorization decision is evaluated against a well-identified authoritative policy/evaluator context.
2. **LOGICAL-TRANSACTION CONSISTENCY** — all consequence-bearing steps of one transaction obey an explicit generation rule and cannot combine permissions from incompatible generations.
3. **COHORT CONSISTENCY** — rollout assignment is authenticated/server-controlled where it changes authority; a principal/device cannot self-select a weaker cohort.
4. **FLEET CONVERGENCE** — supported clients eventually revalidate onto an accepted policy/runtime generation; unsupported stale clients retain bounded local data access where appropriate but do not gain legacy remote authority.

Persistent guards:
- `same account ≠ same rollout cohort everywhere`;
- `same cohort ≠ same policy observed by every evaluator at the same instant`;
- `request A permitted under G1 + request B permitted under G2 ≠ transaction permitted`;
- `idempotency key reused ≠ authorization may be re-evaluated under arbitrary generation`;
- `retry under newer policy ≠ new user intent`;
- `provider update acknowledged ≠ all authorization replicas converged`;
- `Service Worker updated ≠ document/runtime/policy generation converged`;
- `legacy client supported ≠ legacy policy still authoritative`;
- `client reports generation ≠ server trusts generation`;
- `compatibility bridge ≠ downgrade channel`.

## Cross-generation transaction rule

A consequence-bearing logical transaction needs a server-recognized transaction identity and a policy-generation rule. Generic safe choices include:

- **PINNED** — transaction begins under authoritative generation G and all authorization-bearing steps remain under G until completion/expiry, but only while G remains explicitly valid for that transaction class.
- **REVALIDATE-FORWARD** — when policy advances, the transaction is re-evaluated under the newer generation before the next consequence-bearing step; prior authorization cannot simply be carried forward.
- **ABORT/RESTART** — if semantics changed incompatibly or predecessor authority was revoked, preserve user data where possible and restart authorization under the current generation.

There is no universal best choice. A security revocation must be able to invalidate an otherwise pinned transaction. Therefore `pinned generation ≠ immortal authority`.

Never allow a transaction to cherry-pick each step from whichever generation is more permissive. The final execution gate should bind at minimum transaction identity, significant transaction data/fingerprint, authorization state, policy/evaluator generation or accepted generation lineage, relevant authority/trust epoch, and expiry/consumption state.

## Retry and idempotency semantics

A retry should preserve operation identity. If the first attempt committed but its response was lost, re-evaluating the same idempotency key as a fresh operation under a newer policy can create contradictory outcomes. Generic rule:

- completed operation → return/reconcile the durable result;
- in-flight operation → do not execute a second independent effect;
- uncommitted operation after material policy change → follow the transaction's PINNED/REVALIDATE/ABORT rule;
- same idempotency key + different significant payload → reject as identity misuse.

`ACK missing ≠ commit missing`; `retry ≠ new authorization opportunity`.

## Cohort integrity

If cohort membership changes authorization, cohort assignment is authority-bearing state. It should be derived or admitted server-side from authenticated rollout state. Client hints may help diagnostics but cannot select a weaker policy generation.

Avoid sticky-cohort assumptions that outlive a security retirement. A stable account hash can make rollout deterministic, but it is not by itself an authorization proof and must not force use of a retired generation.

Multi-device accounts require explicit semantics. Device A in candidate rollout and long-offline device B on an older runtime can coexist, but server authorization for each operation remains based on accepted server policy state, not on whichever device reports the older generation.

## Eventual-consistency boundary

A provider may acknowledge a policy update before every authorization path observes it. Therefore rollout orchestration should not infer global convergence from a successful control-plane write.

Where generation observability exists, record the evaluator/policy generation that actually determined the decision. Where it does not, treat exact convergence as OPEN and avoid claims that depend on atomic cutover.

For authority-critical transitions such as revocation, trust-floor increase or recovery restriction, use product/provider mechanisms that can enforce the required safety property; if the provider cannot supply sufficient semantics, keep the affected capability gated or use a separately controlled enforcement boundary rather than inventing consistency.

## Split-policy detection and convergence

Useful states:
- **PREDECESSOR-AUTHORITATIVE**;
- **CANDIDATE-SHADOW**;
- **BOUNDED-SPLIT-AUTHORITY** — expected partial rollout with explicit cohort scope;
- **CONVERGING** — candidate authoritative for intended scope but observed runtime/evaluator lag remains;
- **UNEXPECTED-SPLIT** — decisions/generations outside declared rollout topology;
- **RETIREMENT-PENDING** — predecessor accepted only for bounded in-flight/compatibility cases;
- **CURRENT** — intended authoritative generation reached for stated scope;
- **UNOBSERVABLE** — provider/runtime cannot establish required generation fact.

Convergence is not merely `latest config deployed`. It requires retirement rules for predecessor authority and explicit treatment of in-flight transactions, retries, offline clients and recovery paths.

## PWA / Service Worker / EFB application

For a long-offline company iPad, keep distinct:
- cached document/app generation;
- controlling Service Worker generation;
- local data/schema generation;
- server API generation;
- server authorization-policy generation;
- account/device trust epoch.

On reconnect:
1. preserve local irreplaceable data before destructive migration;
2. discover/revalidate current server compatibility and authority rather than trusting the client-reported policy generation;
3. do not replay queued remote mutations merely because they were locally valid under an old policy;
4. bind queued operation identity/payload/provenance so retry/reconciliation cannot silently become a new intent;
5. if current policy permits revalidation, converge forward;
6. if predecessor was retired for security, do not reactivate it as a compatibility shortcut;
7. if no safe automated bridge exists, keep local read/export and enter truthful manual recovery where product semantics permit.

`offline queue created under G1 ≠ remote execution authorized under G1 forever`.

Actual Safari/WebKit/MDM/background/storage behavior remains OPEN until physical/project evidence exists.

## Cross-track transfer

### Track A — Platform & Browser
Own observable document/SW/storage/browser generation mechanics and exact activation/control facts. Do not infer authorization generation from SW generation.

### Track B — UX / IA
Own truthful states for `local changes preserved`, `revalidation required`, `sync paused`, `operation already completed`, `transaction must be restarted`, and `manual recovery required`. Avoid wording that implies local deletion when only remote authority is gated.

### Track C — Performance / Accessibility / Quality
Own fault injection across policy propagation lag, multi-request transactions, retries/ACK loss, two-device split cohorts, stale SW/document combinations and accessible recovery/restart states.

### Track D — Search / Discovery / Analytics
May measure rollout/cohort/generation diagnostics with privacy minimization. Analytics cannot assign authoritative cohort, clear a gate or prove fleet convergence from absence of old-generation telemetry.

### Track E — Owner
Own cohort authority, transaction-generation semantics, predecessor retirement, provider-consistency assumptions, cross-generation execution gates and recovery compatibility policy.

## MINTTAP DECISION — minimal sufficient model

If implemented for MintTap/LogMate-like systems:
1. make policy/evaluator generation explicit where the chosen architecture exposes it;
2. make rollout cohort server-controlled when it affects authorization;
3. give consequence-bearing multi-step operations a server-recognized transaction/operation identity;
4. choose PINNED, REVALIDATE-FORWARD or ABORT/RESTART semantics per operation class instead of accidental request-by-request mixing;
5. let security revocation override obsolete pinned authority;
6. bind final execution to transaction data, authorization state and accepted generation/trust context;
7. treat retries as the same operation, not a fresh chance to obtain a more permissive generation;
8. never infer provider-wide convergence from a control-plane acknowledgement;
9. converge offline PWA clients forward without allowing them to select legacy server policy;
10. preserve local data while gating unsafe remote mutation when convergence cannot yet be established.

No production engine, consistency SLA, transaction schema, cohort algorithm, compatibility horizon or WebKit behavior is asserted.

## VALIDATION — 42-case campaign

1. same-generation single request; 2. same-generation multi-step transaction; 3. G1 begin/G2 execute with PINNED allowed; 4. G1 begin/G2 execute with revocation overriding pin; 5. REVALIDATE-FORWARD permit; 6. REVALIDATE-FORWARD deny; 7. incompatible change forces ABORT/RESTART; 8. step A G1 permit + step B G2 permit cannot cherry-pick incompatible semantics; 9. final execution detects changed significant payload; 10. transaction expiry; 11. authorization consumption/replay rejection; 12. ACK loss after commit returns durable result; 13. retry before commit does not duplicate effect; 14. same idempotency key/different payload rejected; 15. retry after policy change follows transaction rule; 16. client-forged predecessor generation ignored; 17. client-forged cohort ignored; 18. stable cohort cannot preserve retired generation; 19. account with two devices in different rollout states cannot combine privileges; 20. provider control-plane ACK precedes evaluator convergence; 21. expected split remains within declared cohort; 22. unexpected evaluator generation detected; 23. predecessor retirement waits only for explicitly bounded valid in-flight cases; 24. predecessor security retirement aborts unsafe in-flight case; 25. policy rollback cannot resurrect retired trust epoch; 26. stale SW + current document; 27. current SW + stale document; 28. `skipWaiting`/`clients.claim` transition does not grant server authority; 29. offline queue G1 reconnects at G3 and revalidates; 30. queued operation denied at G3 preserves local record/provenance; 31. old operation already committed remotely reconciles without duplicate; 32. local clock manipulation cannot select generation; 33. stale backup cannot restore cohort authority; 34. analytics absence of G1 does not prove G1 fleet zero; 35. provider generation unobservable produces bounded UNKNOWN rather than false CURRENT; 36. manual recovery path remains accessible when automatic convergence fails; 37. accessible UX distinguishes saved-local from synced-remote; 38. two simultaneous devices retry same logical operation safely; 39. policy-language/runtime generation change included in transaction compatibility; 40. recovery/reset transaction cannot cross generations without explicit rule; 41. full bounded rollout converges while long-offline iPad remains data-preserving/gated; 42. adversarial sequence combines forged cohort + retry + policy propagation lag + stale SW and fails without privilege expansion or duplicate mutation.

## CONTRADICTION / failure-mode analysis

### Sticky-cohort theater
A deterministic rollout bucket can improve repeatability but is not permission to keep using a retired policy.

### Atomic-rollout theater
A successful policy update API call does not prove every evaluator changed simultaneously when the provider documents eventual consistency.

### Request-by-request authorization theater
Every request can be individually authorized while the overall multi-step transaction violates an invariant.

### Retry theater
Idempotency prevents duplicate effects only if operation identity and durable result semantics are actually enforced; it does not solve authorization-generation drift by itself.

### PWA-generation theater
A new Service Worker does not prove the document, data schema, server API, policy or trust epoch all converged.

### Compatibility theater
Keeping old clients usable must not mean allowing clients to choose old authorization policy.

## OPEN

Actual MintTap/LogMate authorization engine, provider consistency semantics, policy/evaluator generation observability, transaction boundaries, operation/idempotency model, rollout cohorts, device/account identity, queued mutation format, SW strategy, compatibility horizon and managed-iPad behavior remain unknown. Production semantics are not claimed.

## CHANGE WATCH

- Managed authorization-provider consistency/propagation behavior must be verified against the chosen service and can change.
- The IETF Idempotency-Key specification remains an Internet-Draft as of the cited 2025 draft; do not treat draft details as a final RFC contract.
- Service Worker lifecycle/browser behavior requires current Track A evidence and physical Safari/WebKit validation for EFB claims.
- Policy-language/runtime upgrades and product transaction topology changes require refreshing cross-generation fixtures.

## Gate result

**PASS (generic).** The Web Manager can now distinguish request, transaction, cohort and fleet consistency; prevent client-controlled generation downgrade; define explicit cross-generation transaction rules; account for provider propagation lag; and converge long-offline PWA clients without converting legacy compatibility into remote authority.

Product/provider/managed-iPad/transaction-policy runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA policy-generation retirement, in-flight lease bounding & compatibility-horizon governance.** Once split-policy rollout can converge safely, the next bottleneck is deciding when predecessor authority may be retired, how long bounded in-flight transactions can legitimately survive, how emergency revocation overrides leases, and how compatibility/support horizons are communicated and enforced without turning expiry into data loss or indefinite downgrade support.