# 218 — PWA Distributed Policy-Currentness Witnesses, Enforcement Convergence & Stale-Authority Extinction

Status: **PASS (generic) / PRODUCT + POLICY-ENGINE + DISTRIBUTED-ENFORCEMENT + RECOVERY + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline-state mechanics; Track B reconciliation-state communication; Track C destructive/distributed validation; Track D convergence observation.  
Dependencies: 117–137, 171–217 and earlier authority/currentness/recovery/provenance work.

## Problem
217 made policy composition explicit and required distributed convergence evidence before claiming predecessor authority or waiver extinction. The adjacent problem is epistemic: a central policy store can be current while one or more enforcement points still enforce an older authentic generation. Conversely, a dashboard can report apparent convergence while an unobserved provider console, recovery path, restored region, MDM/bootstrap path or long-offline client can still exercise stale authority.

Central rule: **policy currentness is a property that must be evidenced at consequence-bearing enforcement boundaries, not inferred from publication; convergence claims must be scoped to a known enforcement set and an observation interval; unreachable tails remain explicit unknowns; and predecessor authority is extinct only for a stated consequence/scope when both positive current-policy evidence and negative stale-authority tests support that claim.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Service Worker/cache/storage/offline mechanics explain why a client can retain stale policy material, but cached state does not establish current authority.
- **B UX/IA/Content:** very high dependency pressure. Must distinguish offline-usable, reconciliation-required, sync-blocked, stale-policy, recovery-in-progress and current states without presenting security downgrade as a preference.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands from 496 to **504 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures generation skew, witness age, unreachable-tail duration, rejected predecessor attempts, convergence latency and resurrection events. Telemetry cannot create currentness.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns currentness floor, enforcement-set inventory, witness semantics, partition/recovery behavior, extinction claims and admission after rejoin.

## SOURCE

### NIST SP 800-207 — decision and enforcement are distinct logical functions
NIST SP 800-207 defines zero-trust architecture around explicit policy decision and policy enforcement rather than implicit trust based on network location. A Policy Enforcement Point carries out access decisions at the protected resource boundary.

Sources:
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://csrc.nist.gov/glossary/term/policy_enforcement_point

**TRANSFER VALIDATION:** a current decision/control plane does not prove that every enforcement point has consumed or is enforcing the current decision. This is a bounded architectural transfer, not a claim that MintTap must implement NIST ZTA components literally.

### NIST SP 800-207A — distributed application enforcement requires policy plus runtime enforcement infrastructure
NIST SP 800-207A addresses granular application-level policy enforcement across multi-location/multi-cloud environments and explicitly discusses gateways, proxies and identity infrastructure that enforce policies independent of service location.

Source:
- https://csrc.nist.gov/pubs/sp/800/207/a/final

**TRANSFER VALIDATION:** distributed policy is not complete at policy publication; enforcement components and their runtime state matter.

### NIST SP 1800-35 — current final implementation evidence separates PEP operation and monitoring
NIST SP 1800-35 was published final on 2025-06-10. Its zero-trust implementations use Policy Enforcement Points to enable, monitor and terminate connections according to policy decisions and demonstrate distributed enterprise enforcement patterns.

Sources:
- https://www.nccoe.nist.gov/publications/practice-guide/implementing-zero-trust-architecture-nist-sp-1800-35-practice-guide-6
- https://www.nist.gov/publications/implementing-zero-trust-architecture-high-level-document

**TRANSFER VALIDATION:** monitoring an enforcement point is useful evidence of behavior, but observation remains distinct from authority.

### NIST SP 800-53 / 800-53A — control existence and control assurance are different questions
NIST SP 800-53 provides security/privacy controls; SP 800-53A provides assessment procedures and explicitly frames assessment as evidence supporting confidence that controls operate as intended.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** configured policy is not equivalent to assessed effective enforcement. MintTap-specific assessment procedures remain OPEN.

## SYNTHESIS 1 — separate publication, distribution, consumption and enforcement
For a policy generation G, distinguish at least:
1. **AUTHORED** — policy exists in an authoritative source;
2. **PUBLISHED** — G is the current authenticated publication for its namespace;
3. **DISTRIBUTED** — G reached a target endpoint/channel;
4. **CONSUMED** — the endpoint parsed/accepted G as current;
5. **ENFORCING** — consequence-bearing decisions are actually governed by G-or-later;
6. **OBSERVED** — evidence confirms enforcement behavior within a stated interval.

A success at an earlier layer does not imply later layers.

`policy authored ≠ policy published`; `published ≠ distributed`; `distributed ≠ consumed`; `consumed ≠ enforcing`; `enforcing once ≠ continuously current`.

## SYNTHESIS 2 — define the enforcement set before claiming convergence
A convergence claim needs a denominator. Potential consequence-bearing enforcement points can include:
- primary server/API admission;
- regional gateways and replicas;
- CI/release gate and deployment API;
- provider/admin console paths capable of bypassing CI;
- recovery and break-glass tooling;
- KMS/PKI/signing policy boundaries;
- MDM/bootstrap/provisioning path;
- scheduled/background jobs;
- export/import or backup/restore admission;
- Service Worker/client-side gate where it has real consequence;
- reconnecting offline clients only to the extent they can initiate consequence-bearing remote work.

The exact MintTap/LogMate set is **OPEN**. An inventory is itself evidence and can be incomplete.

`known enforcement set converged ≠ every possible path converged`; `inventory complete claim ≠ universal absence of shadow enforcement`.

## SYNTHESIS 3 — currentness witness is evidence, not authority
A useful enforcement witness can bind:
- enforcement-point identity and failure domain;
- policy namespace;
- accepted policy/authority generation;
- composition/evaluator version;
- predecessor/waiver revocation floor;
- observation time or monotonic sequence where meaningful;
- tested consequence/capability;
- result and evidence provenance;
- witness issuer/collector and freshness bounds.

A witness does not grant authority. It reports evidence about an enforcement state.

`witness says G12 ≠ witness may authorize G12`; `signed witness ≠ truthful witness`; `fresh witness ≠ complete fleet evidence`.

## SYNTHESIS 4 — prefer monotonic authority/currentness floors over wall-clock recency
Wall clocks can skew, roll back or be unavailable offline. Where architecture permits, currentness should rely on authenticated monotonic generations/epochs or equivalent lineage rather than `latest timestamp wins`.

A durable floor can state that generation < G12 or predecessor authority E1 is no longer admissible for a namespace/capability. Restored application data may contain older objects, but those objects cannot lower the floor.

`newer timestamp ≠ current authority`; `PITR restored G9 ≠ floor returned to G9`; `clock unavailable ≠ retired authority current`.

Exact storage and anti-rollback mechanism remain implementation OPEN.

## SYNTHESIS 5 — convergence is bounded, not absolute
A defensible statement is scoped, for example:

> For enforcement set S known at inventory revision I, all reachable consequence-bearing points have demonstrated G12-or-later enforcement and predecessor rejection during interval T; points U1/U2 are unreachable and remain UNKNOWN with remote mutation disabled until re-admission.

Do not state `fleet converged` if the denominator or unreachable tail is unknown.

`all observed current ≠ all existent current`; `no stale attempt observed ≠ no stale authority exists`; `unreachable ≠ compliant`.

## SYNTHESIS 6 — unreachable tails need a return-to-service contract
A partitioned region, powered-off recovery appliance or long-offline iPad can miss multiple policy generations. When it returns:
1. preserve unique data/evidence first;
2. do not accept its cached policy as proof of currentness;
3. authenticate current authority/currentness floor;
4. update/migrate evaluator semantics if required;
5. test predecessor/expired-waiver rejection;
6. re-admit consequence-bearing capabilities only after required checks;
7. preserve evidence about stale operations attempted or accepted before reconciliation.

`device returned ≠ device re-admitted`; `network reachable ≠ policy current`; `data preserved ≠ mutation authorized`.

## SYNTHESIS 7 — partition availability must not manufacture local policy sovereignty
Offline-first PWA utility can continue for local data entry/read workflows where product policy permits. It does not imply that a disconnected client can extend an expired waiver, invent a successor policy or permanently authorize queued remote mutations.

If current policy is unavailable, the product can preserve local work and expose a bounded `reconciliation required / sync blocked` state rather than silently selecting the cached permissive branch.

`offline utility ≠ offline authority sovereignty`; `cached permit ≠ renewable permit`; `central unavailable ≠ stale policy promoted`.

## SYNTHESIS 8 — stale-authority extinction is a scoped negative claim
Do not claim an old authority is globally nonexistent. Historical artifacts may legitimately remain for verification/audit. Instead define extinction in consequence terms, e.g.:

> E1 is no longer accepted to authorize new remote mutation for namespace N across known enforcement set S at current floor G12.

Evidence bundle can include:
- current policy/authority publication;
- known enforcement-set inventory;
- positive G12 acceptance tests;
- negative E1/expired-waiver tests;
- region/provider/recovery-path tests;
- PITR restore/rejoin tests;
- observation for predecessor attempts;
- explicit unreachable/unknown tails;
- historical-verifier isolation evidence.

`retired authority artifact exists ≠ retired authority consequence-bearing`; `negative tests pass ≠ universal absence proven`.

## SYNTHESIS 9 — PITR/recovery needs a rejoin gate
A restored region may have internally consistent G9 policy, old delegation rows and old waiver objects. Before it can serve consequence-bearing requests, it must reconcile against a currentness source/floor outside the rolled-back failure domain or another independently governed recovery basis.

If currentness cannot be established, serve only explicitly safe degraded capabilities; preserve data and block sensitive mutation.

`restore complete ≠ region admitted`; `database consistency ≠ authority currentness`; `old policy verifies ≠ old policy admissible`.

## SYNTHESIS 10 — observation needs anti-equivocation and identity binding
A fleet dashboard can be misleading if two endpoints share an identity, a stale endpoint reports for another, or the collector accepts replayed witness data. Evidence should bind endpoint identity, generation, evaluator semantics and freshness, and should detect duplicate/conflicting endpoint identity where practical.

Do not let the same policy plane be the only source that both declares G current and certifies every enforcement point is current without independent validation where risk warrants it.

`dashboard green ≠ independent enforcement proof`; `endpoint authenticated ≠ report fresh`; `one witness identity ≠ one physical/logical enforcement instance`.

## SYNTHESIS 11 — convergence SLOs are operational objectives, not authorization rules
It can be useful to measure propagation/convergence latency, stale-generation attempt rate and unreachable-tail age. But an SLO such as `99.9% within 5 minutes` does not authorize the remaining 0.1% to use retired authority.

For high-consequence revocation, policy can require capability restriction until a point proves the current floor. Availability trade-offs must be explicit rather than hidden inside the SLO.

`SLO met ≠ every endpoint safe`; `within propagation budget ≠ stale authority authorized`; `availability target ≠ security exception`.

## SYNTHESIS 12 — policy/evaluator upgrades require semantic convergence
A point can report policy G12 while still running an evaluator/combiner whose semantics differ from the one G12 assumes. Currentness witness therefore may need to bind both policy generation and evaluator/composition version.

`same G ≠ same decision semantics`; `policy synchronized ≠ evaluator synchronized`; `binary deployed ≠ policy migration complete`.

## SYNTHESIS 13 — rollback and kill-path evidence should be asymmetric
Rollback of application code/data is common; rollback of security floors should require separate explicit authorization. A recovery action may restore an older application build while preserving a newer authority floor.

Likewise, a kill/revocation path should be testable even when normal distribution is impaired. This does not require a particular vendor architecture; it establishes a requirement to avoid coupling all revocation authority to the exact failure domain being recovered.

`app rollback ≠ security-floor rollback`; `recovery needs old binary ≠ recovery needs old authority`.

## SYNTHESIS 14 — long-offline LogMate/EFB scenario
For a company iPad that remains offline across G9→G12:
- local flight/logbook data remains usable/preserved according to local product rules;
- old Service Worker/cache/policy/waiver is historical context;
- reconnect does not immediately replay queued consequence-bearing operations;
- client first obtains authenticated current authority/policy and required evaluator/schema migrations;
- stale operations are classified and re-admitted, transformed or blocked under current rules;
- inability to complete current verification leaves `data preserved / sync blocked`, not data deletion or server-floor downgrade.

No assumption is made here that iPadOS permits unattended background convergence, durable storage, direct device-to-device sync or a particular MDM flow. Those remain runtime OPEN.

## Generic currentness/convergence evidence contract
For a material policy/authority change retain enough evidence to answer:
- what namespace/capability changed;
- predecessor and successor generation/authority;
- which enforcement-set inventory revision is the denominator;
- which points are reachable/current/stale/unreachable/unknown;
- what each point actually enforces, not merely what it downloaded;
- evaluator/composition version;
- negative predecessor/expired-waiver result;
- observation/witness freshness;
- partition/recovery/PITR rejoin state;
- unresolved tails and imposed restrictions;
- closure criteria and who can declare closure.

This is a generic knowledge template, not a MintTap production schema.

## Track C destructive campaign — 496 → 504 defined cases
Add:
1. **Published-not-enforced:** central store is G12; one regional gateway still enforces G11 permit.
2. **False convergence denominator:** dashboard reports 100% because an unregistered provider-console path is absent from inventory.
3. **Replayed witness:** stale signed `G12 current` witness is replayed after endpoint rollback to G10.
4. **PITR resurrection:** restored region contains G9 + predecessor authority and serves before currentness rejoin.
5. **Evaluator skew:** all points report G12 but one old combiner interprets Indeterminate as Permit.
6. **Partitioned tail:** unreachable region misses waiver revocation; return-to-service must reject old waiver before mutation.
7. **Long-offline iPad:** client returns after multiple generations with unique data and queued old-waiver mutation; preserve data, obtain current policy, re-admit queue.
8. **Historical-verifier confusion:** retired E1 public verification material remains for audit and is mistakenly wired into current issuance/admission path.

These are **defined cases, not executed PASS evidence**.

## Cross-track transfer
### Track A
Own exact Service Worker/cache/storage/network mechanics and browser/OS capability evidence. Do not infer current authority from a cached policy or successful fetch.

### Track B
Own comprehensible states for `offline usable`, `policy reconciliation required`, `sync blocked`, `recovery rejoin`, `current` and `historical-only`. Do not provide a user-facing security downgrade control unless explicitly authorized by policy.

### Track C
Execute partition, rollback, PITR, provider-console, evaluator-skew, stale-witness and physical-device return matrices when implementation exists. Validate that blocked/recovery states remain accessible and understandable.

### Track D
Measure generation skew, witness freshness, convergence latency, unreachable-tail age, predecessor attempts and resurrection incidents. Observation cannot itself mark a point current.

### Design Studio dependency
Canonical Design Studio Web remains W121, Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. No reconciliation UI is promoted here as validated design.

### Software Engineering dependency
Implementation-level policy store, anti-rollback floor, witness format, endpoint identity, evaluator versioning, distributed consistency, test harness and release integration belong to Software Engineering when canonical evidence exists. This study defines web-security/operations requirements and failure oracles, not implementation PASS.

## MINTTAP DECISION / DIRECTION
For future MintTap/LogMate-like implementation requirements:
1. never equate central policy publication with distributed enforcement;
2. inventory the consequence-bearing enforcement set and version that inventory;
3. make convergence claims scoped to that known set, generation and observation interval;
4. treat unreachable tails as UNKNOWN and require a rejoin contract before sensitive capability resumes;
5. use authenticated monotonic authority/currentness lineage where feasible rather than wall-clock recency alone;
6. preserve application/data rollback capability without automatically rolling back the security floor;
7. prove stale-authority extinction with bounded positive-current + negative-predecessor evidence, not absolute absence claims;
8. bind evaluator/composition semantics into currentness evidence when semantic drift can change decisions;
9. preserve unique offline data first while requiring current-policy re-admission for consequence-bearing sync;
10. keep exact MintTap/LogMate enforcement topology, witness mechanism, SLOs and iPad behavior OPEN until canonical runtime evidence exists.

## Persistent guards added
- `policy authored ≠ policy published`;
- `published ≠ distributed`;
- `distributed ≠ consumed`;
- `consumed ≠ enforcing`;
- `enforcing once ≠ continuously current`;
- `known enforcement set converged ≠ every possible path converged`;
- `witness says current ≠ witness grants authority`;
- `signed witness ≠ truthful witness`;
- `fresh witness ≠ complete fleet evidence`;
- `newer timestamp ≠ current authority`;
- `all observed current ≠ all existent current`;
- `unreachable ≠ compliant`;
- `device returned ≠ device re-admitted`;
- `offline utility ≠ offline authority sovereignty`;
- `retired authority artifact exists ≠ retired authority consequence-bearing`;
- `restore complete ≠ region admitted`;
- `database consistency ≠ authority currentness`;
- `dashboard green ≠ independent enforcement proof`;
- `SLO met ≠ every endpoint safe`;
- `same policy generation ≠ same evaluator semantics`;
- `app rollback ≠ security-floor rollback`.

## OPEN / VALIDATION
Still OPEN until product/runtime evidence exists:
- actual enforcement-set inventory and shadow paths;
- currentness-floor persistence and anti-rollback implementation;
- endpoint/witness identity and replay resistance;
- policy/evaluator distribution mechanics;
- provider-console/recovery/MDM/PITR enforcement;
- convergence objectives and availability trade-offs;
- physical iPad/WebKit/Service Worker behavior;
- long-offline queue re-admission semantics;
- human/accessibility validation of reconciliation states;
- legal/aviation/safety consequences of blocked or delayed synchronization.

## Gate
**218 PASS (generic).** The Web Manager can now distinguish policy publication from effective enforcement; define a bounded enforcement-set denominator; construct scoped currentness/convergence evidence; handle unreachable tails and recovery rejoin without permissive merge; and define stale-authority extinction without claiming universal absence.

Production validation remains OPEN.

## Next high-value target
**219 — currentness-witness trust, collector compromise, equivocation/fork detection & independent convergence attestation.** 218 assumes useful witnesses can be produced. The next adjacent risk is that the witness/collector plane itself lies, forks views between operators, replays a once-valid fleet state, or shares the same compromise domain as policy publication. Study independent corroboration, witness succession/revocation, anti-equivocation, partial observability and recovery when the convergence evidence plane is itself suspect.