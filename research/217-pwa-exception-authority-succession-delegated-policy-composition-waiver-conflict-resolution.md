# 217 — PWA Exception-Authority Succession, Delegated-Policy Composition & Waiver-Conflict Resolution

Status: **PASS (generic) / PRODUCT + POLICY-ENGINE + DISTRIBUTED-ENFORCEMENT + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A capability/currentness evidence; Track B policy-state communication; Track C destructive/distributed validation; Track D drift/conflict observation.  
Dependencies: 117–126, 171–216 and earlier authority/currentness/recovery/provenance work.

## Problem
216 separated inventory fact authority, acceptance-policy authority and exception authority, then modeled a waiver as a scoped, revocable capability lease. The adjacent failure mode is composition. A system can have individually valid global, product, provider, regional and device policies plus individually valid waivers, yet their combination can accidentally authorize more than any issuer intended. Authority rotation or delegation can also create overlapping issuers, and network partitions can leave enforcement points with different valid-looking policy branches.

Central rule: **delegation must be monotonic in authority unless a separately governed higher authority explicitly changes the ceiling; policy composition must be explicit and deterministic; individually valid waivers must not union into an unintended broader permit; and split-brain convergence must not select a branch merely because it is newer or more permissive.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/WebKit/Service Worker/device capability facts constrain whether a policy can execute, but capability support does not choose policy precedence or grant an exception.
- **B UX/IA/Content:** very high dependency pressure. Must represent current, blocked, temporary exception, conflict/indeterminate, migration-required and data-preserved/sync-blocked states without exposing a user-selectable security downgrade.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands from 488 to **496 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures policy-version skew, stale enforcement points, waiver overlap, delegation depth, conflict frequency and convergence latency; observation cannot resolve authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns authority ceilings, delegation/succession semantics, policy composition, anti-rollback, distributed enforcement and conflict closure.

## SOURCE

### NIST CSF 2.0 — governance establishes roles, responsibilities and policy accountability
NIST CSF 2.0 is a final framework and explicitly elevates cybersecurity governance. Its Govern function treats organizational context, risk-management strategy, roles/responsibilities, policy and oversight as cybersecurity outcomes. It does not prescribe a MintTap policy-combining algorithm or delegation schema.

Sources:
- https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- https://csrc.nist.gov/pubs/sp/1303/final

**TRANSFER VALIDATION:** distributed crypto exceptions remain governed risk decisions even when policy is enforced automatically. Automation does not erase accountability.

### NIST least privilege — delegated authority should not exceed task need
NIST defines least privilege as restricting users/processes to the minimum authorizations and resources necessary for assigned functions.

Source:
- https://csrc.nist.gov/glossary/term/least_privilege

**TRANSFER VALIDATION:** least privilege supports bounded delegation, but does not by itself define how global/product/provider/device policy must compose.

### OASIS XACML 3.0 — policy combination is a first-class semantic choice
OASIS XACML 3.0 defines explicit policy/rule combining algorithms including deny-overrides, permit-overrides, first-applicable and only-one-applicable, with explicit handling of Indeterminate/NotApplicable states. This demonstrates that combining valid policies is itself an authorization-semantic decision, not an implementation detail.

Source:
- https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html

**TRANSFER VALIDATION:** XACML is precedent for explicit composition semantics. MintTap is not required to implement XACML, and generic `deny-overrides` is not automatically correct for every business policy. The important transfer is that precedence, uncertainty and conflict behavior must be deliberate and testable.

## SYNTHESIS 1 — separate authority ceiling from delegated authority
A delegation should bind at least:
- issuer authority identity and generation;
- delegate identity;
- exact policy namespace/domain;
- subject/resource/device/provider/product scope;
- permitted decision types and capabilities;
- maximum exception severity/risk class if applicable;
- delegation start/expiry/revocation conditions;
- whether subdelegation is forbidden or bounded;
- evidence/audit obligations;
- successor/revocation lineage.

A delegate cannot create authority it was not granted. If authority A can waive only provider P for read-only capability C, A cannot delegate authority to waive every provider or remote mutation.

`delegated authority ≠ parent authority copied`; `can issue waiver ≠ can change baseline`; `can delegate ≠ can subdelegate without limit`.

## SYNTHESIS 2 — succession and delegation are different transitions
**Delegation** permits another authority to act within a bounded ceiling while the issuer may remain active. **Succession** changes which authority is current for a namespace or role. Treating succession as merely adding another delegate can leave predecessor and successor simultaneously able to issue current waivers indefinitely.

A succession record should bind predecessor, successor, affected authority namespace, effective generation, predecessor retirement/restriction, outstanding delegation treatment, outstanding waiver treatment and anti-rollback/currentness evidence.

`successor active ≠ predecessor extinct`; `new approver exists ≠ old approver retired`; `authority rotated ≠ old delegations automatically safe`.

## SYNTHESIS 3 — policy layers need explicit domains and precedence
Potential policy layers include:
1. organization/global security floor;
2. product/service policy;
3. provider/deployment policy;
4. region/environment policy;
5. managed-device/cohort policy;
6. session/request currentness/admission state;
7. scoped exception/waiver overlays.

Do not assume that narrower always means stronger or that later always wins. A device-specific policy may impose an extra restriction; a provider waiver may relax only one provider condition; a global floor may be non-waivable by lower authorities.

The effective decision must be derived from an explicit composition contract, not object merge order, database timestamp, UI order or whichever replica answers first.

`more specific ≠ more authoritative`; `newer ≠ more authoritative`; `last writer ≠ policy winner`.

## SYNTHESIS 4 — individually valid waivers must not union into unintended permission
Consider two valid waivers:
- W1: provider P may use legacy algorithm L for **read-only export**;
- W2: device cohort D may perform **remote mutation** under current algorithm C.

A naive union could produce `provider P + cohort D + legacy L + remote mutation`, which neither waiver authorized. Evaluate each requested consequence-bearing operation against a waiver whose own scope covers the entire deviation, or against an explicitly authorized composition rule.

A useful model is intersection-oriented: an operation must satisfy the baseline plus every non-waived applicable restriction; each waiver removes only its named restriction for its named subject/capability/context. Do not synthesize a new super-waiver by unioning partial permissions.

`W1 valid + W2 valid ≠ W1∪W2 authorized`; `two narrow exceptions ≠ one broad exception`; `same request matches both ≠ combined privileges intended`.

## SYNTHESIS 5 — unknown/indeterminate composition must not silently become permit
Distributed policy evaluation can fail because a policy is unavailable, unverifiable, stale, syntactically invalid, semantically unsupported or outside the evaluator's known generation. These are not equivalent to `NotApplicable`.

For consequence-bearing crypto/recovery authority, an indeterminate required restriction should not disappear merely because another policy returns Permit. Preserve an explicit `INDETERMINATE/BLOCKED` state unless the composition contract deliberately and safely defines another result.

XACML's explicit treatment of Indeterminate is useful precedent: errors and non-applicability are semantically meaningful states rather than implicit permit.

`policy unavailable ≠ policy not applicable`; `cannot evaluate restriction ≠ restriction absent`; `one permit ≠ uncertainty erased`.

## SYNTHESIS 6 — exception-authority rotation must define outstanding waiver fate
When exception authority E1 is replaced by E2, existing E1 waivers need an explicit rule. Plausible outcomes include:
- remain valid until their original bounded expiry under a current policy that recognizes E1 historical issuance;
- require E2 revalidation before further consequence-bearing use;
- become suspended immediately for a compromise-driven rotation;
- remain historical evidence only.

Do not infer the rule from signature validity alone. A cryptographically authentic E1 waiver can be historically valid yet no longer current-policy acceptable.

`old waiver verifies ≠ old waiver currently admissible`; `authority succession ≠ blanket waiver renewal`; `re-signing ≠ risk re-acceptance`.

## SYNTHESIS 7 — compromise succession differs from planned succession
If E1 rotates normally while trustworthy, E1 may participate in authentic successor lineage under the governing policy. If E1 is compromised, E1 cannot be trusted to authorize an unrestricted E2 successor or to bless attacker-issued waivers as part of migration.

Reuse the recovery-anchor principle from earlier studies: compromise recovery must rely on a separately governed recovery basis/threshold, and post-compromise waivers may need uncertainty classification by issuance window.

`planned rotation ≠ compromise recovery`; `compromised issuer signed successor ≠ successor trusted`; `signature valid ≠ issuance authorized`.

## SYNTHESIS 8 — split-brain policy branches require authority/currentness reconciliation, not permissive merge
Suppose region R1 has policy generation G10 revoking waiver W while R2 is partitioned on authentic G9 where W remains active. Both objects can verify cryptographically. On reconnection, do not choose:
- the branch with the newest wall-clock timestamp;
- the branch with more successful operations;
- the branch that is more permissive;
- a union of both branches.

Reconcile using authenticated policy-generation/lineage/currentness rules. Preserve evidence of operations accepted under stale R2, classify them by consequence and current policy, and require remediation/re-admission where needed.

`authentic branch ≠ current branch`; `split-brain resolved ≠ stale actions retroactively authorized`; `availability history ≠ authority history`.

## SYNTHESIS 9 — distributed enforcement needs a convergence floor
An authority change is not complete merely because the policy store has G11. Consequence-bearing enforcement points may include CI, deployment API, provider console, regional gateway, server admission layer, recovery tooling, MDM/bootstrap path and reconnecting offline clients.

Define a bounded convergence claim such as: known enforcement set E1..En has observed or proven G11-or-later and rejects predecessor authority/expired waivers, with enumerated unreachable/unknown tails. Unreachable tails remain OPEN and may require capability restriction when they return.

`policy published ≠ policy enforced`; `central store current ≠ fleet current`; `one region converged ≠ enforcement converged`.

## SYNTHESIS 10 — rollback/PITR must restore data without restoring retired authority
A PITR snapshot can contain valid old policy, delegation and waiver objects. Restoring them as database rows is not equivalent to reactivating them. Before consequence-bearing operation, reconcile restored state against a durable current authority/policy floor that is not silently rolled back with the application snapshot.

If currentness cannot be established, preserve unique data and block sensitive mutation rather than selecting the restored permissive branch.

`PITR restored delegation ≠ delegation reactivated`; `restored waiver row ≠ current waiver`; `rollback availability ≠ rollback authority`.

## SYNTHESIS 11 — PWA/offline client policy is cached evidence, not autonomous exception authority
A long-offline iPad may hold:
- an old Service Worker;
- cached baseline policy;
- a once-valid waiver;
- queued operations created while that waiver was active;
- local records that must not be lost.

On reconnect, preserve unique records first. Do not let cached W authorize replay merely because the operation was queued during W. Obtain current authenticated policy/authority generation and evaluate consequence-bearing operations under current admission rules, preserving historical context about when/why the operation was created.

A user-facing state may be `data preserved / policy reconciliation required / sync blocked`; this is preferable to silent downgrade or data deletion.

`cached waiver ≠ local policy sovereignty`; `queued under valid W ≠ replay authorized now`; `offline utility ≠ offline permanent exception authority`.

## SYNTHESIS 12 — policy composition itself is versioned security logic
Changing `deny-overrides`-like semantics to `permit-overrides`-like semantics, changing specificity precedence, or changing how Indeterminate is handled can alter authorization without changing any individual policy object. Therefore composition-engine version/semantics belong in policy evidence and migration testing.

For durable decisions retain enough context to answer which policy set, composition semantics, authority generation and evaluator version produced the decision.

`same policies + different combiner ≠ same authorization`; `policy bytes unchanged ≠ security semantics unchanged`; `engine upgrade ≠ policy-neutral by default`.

## Delegation/waiver composition contract — generic template
For each consequence-bearing decision, bind or derive:
- request/operation identity and purpose;
- subject/product/provider/region/device/environment;
- baseline policy generation;
- applicable policy namespaces and authenticated versions;
- composition algorithm/version;
- exception authority generation;
- candidate waiver IDs and complete scopes;
- currentness/revocation/expiry evidence;
- final decision: PERMIT / DENY / INDETERMINATE-BLOCKED;
- obligations/compensating controls where applicable;
- evidence references and evaluator identity/version.

This is a knowledge template, not a MintTap production schema.

## Conflict classes
Distinguish at least:
- **restriction conflict:** one applicable policy permits, another denies;
- **scope overlap:** multiple waivers match parts of one request;
- **authority conflict:** predecessor/successor or two delegates both claim current authority;
- **generation conflict:** authentic policy branches disagree on currentness;
- **semantic conflict:** evaluator/composition versions produce different outcomes;
- **availability conflict:** required policy cannot be fetched/evaluated;
- **evidence conflict:** policy store says one state while enforcement observation shows another.

Do not normalize all of these to a generic `policy error`; remediation differs.

## Track C destructive campaign — 488 → 496 defined cases
Add:
1. **Partial-waiver union:** W1 allows legacy crypto for export; W2 allows mutation for current crypto; engine incorrectly permits legacy mutation.
2. **Delegation expansion:** delegate authorized for provider P issues global waiver; must reject beyond ceiling.
3. **Predecessor resurrection:** E1 retired, PITR restores E1 and an unexpired historical waiver; current authority must not reactivate.
4. **Compromised succession:** compromised E1 signs E2 and broad waiver; ordinary succession path must not establish trust.
5. **Regional split-brain:** R1 has G11 revoke, R2 has G10 permit; convergence must not select permissive branch or union histories.
6. **Indeterminate disappearance:** required device policy cannot be evaluated while provider policy permits; sensitive operation must not silently permit.
7. **Combiner drift:** same policies evaluated by old/new composition engines yield different decisions; release/convergence evidence must detect semantic divergence.
8. **Long-offline iPad:** device queued operation under W at G9, returns at G12 after W expiry and authority succession; preserve data, reject stale authority, re-admit only under current policy.

These are **defined cases, not executed PASS evidence**.

## Cross-track transfer
### Track A
Provide exact browser/WebKit/server/provider capability and cached-state behavior. Do not infer policy authority from capability support.

### Track B
Own comprehensible states for policy conflict, expired exception and data-preserved/sync-blocked conditions. Do not expose a `use old security anyway` preference when policy does not authorize it.

### Track C
Execute composition, rollback, region-skew, evaluator-version and offline-return matrices when implementation exists. Include accessibility/clarity validation for blocked/recovery states.

### Track D
Measure policy skew, stale generation attempts, overlapping-waiver matches, rejected predecessor authority, convergence latency and unresolved tails. Telemetry is evidence, not authorization.

### Design Studio dependency
Canonical Design Studio Web remains W121, Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and human UX evidence remain OPEN. No UI pattern is promoted here as validated reusable design.

### Software Engineering dependency
Implementation-level policy engine, canonical serialization, evaluator versioning, distributed consistency, tests and release integration belong to Software Engineering when canonical evidence is available. This study defines web-security/operations requirements and failure oracles, not implementation PASS.

## MINTTAP DECISION / DIRECTION
For future MintTap/LogMate-like implementation requirements:
1. treat exception authority as a bounded namespace/capability, not generic admin privilege;
2. distinguish delegation from succession and planned rotation from compromise recovery;
3. make policy composition semantics explicit, versioned and testable;
4. do not union partial waivers into broader permission;
5. keep required-policy uncertainty as blocked/indeterminate for consequence-bearing operations unless an explicitly governed rule says otherwise;
6. reconcile split-brain using authenticated authority/currentness lineage, not permissiveness or wall-clock recency;
7. require distributed convergence evidence before claiming predecessor authority/waiver extinction;
8. preserve unique offline data while re-admitting queued operations under current policy;
9. keep production thresholds, authority topology and exact policy engine OPEN until project evidence exists.

## Persistent guards added
- `delegated authority ≠ parent authority copied`;
- `can issue waiver ≠ can change baseline`;
- `can delegate ≠ can subdelegate without limit`;
- `successor active ≠ predecessor extinct`;
- `new approver exists ≠ old approver retired`;
- `more specific ≠ more authoritative`;
- `newer ≠ more authoritative`;
- `last writer ≠ policy winner`;
- `W1 valid + W2 valid ≠ W1∪W2 authorized`;
- `two narrow exceptions ≠ one broad exception`;
- `policy unavailable ≠ policy not applicable`;
- `cannot evaluate restriction ≠ restriction absent`;
- `old waiver verifies ≠ old waiver currently admissible`;
- `authority succession ≠ blanket waiver renewal`;
- `planned rotation ≠ compromise recovery`;
- `authentic branch ≠ current branch`;
- `split-brain resolved ≠ stale actions retroactively authorized`;
- `policy published ≠ policy enforced`;
- `central store current ≠ fleet current`;
- `PITR restored delegation ≠ delegation reactivated`;
- `cached waiver ≠ local policy sovereignty`;
- `queued under valid W ≠ replay authorized now`;
- `same policies + different combiner ≠ same authorization`;
- `engine upgrade ≠ policy-neutral by default`.

## OPEN / VALIDATION
Production validation remains OPEN for:
- actual MintTap/LogMate policy/exception authority topology;
- global/product/provider/region/device policy layers and precedence;
- delegation/subdelegation model;
- waiver composition semantics;
- policy/evaluator store and anti-rollback mechanism;
- region/provider/control-plane consistency model;
- enforcement-point inventory and convergence oracle;
- exact iPadOS/WebKit/PWA cached-policy behavior;
- implementation test results, physical devices, AT and human validation;
- legal/aviation/safety obligations that may constrain exception authority.

## CHANGE WATCH
- NIST CSF/ERM governance guidance and crypto-agility guidance;
- policy-engine/authorization standards used by any eventual implementation;
- WebKit/iPadOS/PWA lifecycle and managed-device behavior;
- provider/MDM/release-control capabilities that affect enforcement/convergence.

## Gate
**217 PASS (generic).** The Web Manager can distinguish delegation/succession/compromise recovery; model explicit policy composition and indeterminate states; prevent accidental waiver union; reason about split-brain and distributed convergence; and preserve offline-first data without preserving stale exception authority.

Production/device/policy-engine/runtime certification remains OPEN.

## Next highest-value adjacent target
**218 — distributed policy-currentness witnesses, enforcement convergence proofs & stale-authority extinction under partition/recovery.** Determine how to establish bounded evidence that known enforcement points have consumed a current policy/authority floor, how to handle unreachable tails without claiming universal convergence, how recovery/PITR/region rejoin proves it did not resurrect predecessor authority, and how long-offline PWA clients obtain current policy without turning central availability into a requirement for local data preservation.