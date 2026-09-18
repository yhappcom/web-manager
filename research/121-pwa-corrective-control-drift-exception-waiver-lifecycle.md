# 121 — PWA Corrective-Control Drift, Exception & Waiver Lifecycle

Status: **PASS (generic) / PRODUCT RUNTIME + EXCEPTION-OWNER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 117–120 containment/normalization/corrective-control chain; Track A browser/PWA mechanics; Track C runtime conformance and negative-oracle evidence; Software Engineering for exact configuration/feature-flag/policy implementation.

## Purpose

120 established how an incident lesson may become a permanent control baseline. The adjacent failure mode is quieter: a control can be approved, implemented and initially validated, then later become weaker through compatibility exceptions, emergency bypasses, feature flags, stale-client allowances, provider settings, operational workarounds or undocumented configuration changes.

This study defines how to distinguish bounded intentional deviation from silent control erosion and what evidence is required to claim that effective runtime enforcement still matches the approved baseline. It is generic governance; it does not claim MintTap or LogMate implements these mechanisms.

## 1. Five-track balance

- **A Platform/Browser:** supplies the actual enforcement mechanics and identifies where browser/Service Worker/client-version behavior can make a nominally identical policy behave differently.
- **B UX/IA/Content:** consumes degraded/restricted states. A waiver must not be hidden behind misleading “normal” UX when capabilities are intentionally reduced.
- **C Quality:** owns conformance, negative canaries, exception-path tests, expiry tests, configuration identity and regression evidence.
- **D Search/Analytics:** supplies observation of exception population and control outcomes but cannot turn telemetry absence into proof of conformance.
- **E Architecture/Security/Operations:** highest-risk owner. Owns baseline identity, deviation classification, authorization, bounded scope, expiry/review, revocation and reconciliation.

E remains the bottleneck; A explains effective mechanics and C proves whether enforcement actually matches the declared policy.

## 2. SOURCE — a baseline is a controlled reference, not a suggestion

NIST defines a baseline configuration as a documented set of specifications formally reviewed and agreed at a point in time and changeable only through change-control procedures. NIST SP 800-128 describes security-focused configuration management as establishing, controlling, monitoring and assessing configurations to manage security risk while supporting business functionality.

Sources checked 2026-09-18:
- https://csrc.nist.gov/glossary/term/baseline_configuration
- https://www.nist.gov/publications/guide-security-focused-configuration-management-information-systems-0
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-128.pdf

**SYNTHESIS:** a permanent control baseline needs an identity against which effective state can be compared. If an organization cannot state which baseline applies to a client/API/trust/release generation, “drift” is not measurable.

Guards:
- `baseline documented ≠ runtime conforms`;
- `same source revision ≠ same effective security configuration`;
- `configuration exists ≠ configuration is the approved baseline`.

## 3. SOURCE — deviations can be legitimate, but must be identified, documented and approved

NIST SP 800-53 Rev.5 CM-6 requires organizations to establish configuration settings, implement them, identify/document/approve deviations based on operational requirements, and monitor/control changes. SP 800-128 likewise treats recorded deviations from common secure configurations as an expected output and calls for change request/approval, security-impact analysis, testing and post-implementation review.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-128.pdf

**SYNTHESIS:** an exception is not automatically a control failure. The governance failure is an unbounded, unowned, unobserved or silently permanent deviation whose effective risk is no longer represented by the approved baseline.

Guards:
- `deviation exists ≠ control governance failed`;
- `operational need asserted ≠ deviation justified`;
- `exception approved ≠ exception safe indefinitely`;
- `documented exception ≠ effective scope matches documentation`.

## 4. Exception taxonomy

Use distinct classes because they require different evidence and retirement behavior:

1. **compatibility exception** — older client/platform temporarily receives reduced capability or alternate path;
2. **availability exception** — a control is relaxed to preserve critical service under a bounded failure condition;
3. **emergency bypass** — extraordinary authority used during an incident or recovery event;
4. **migration bridge** — old/new protocol, trust, schema or release generations coexist temporarily;
5. **feature-flag/configuration override** — runtime behavior differs from nominal code path by configuration;
6. **provider/edge exception** — CDN, WAF, identity, DNS, hosting or other control-plane setting changes enforcement;
7. **manual operational workaround** — humans perform a step outside the normal automated control path;
8. **accepted permanent deviation** — a deliberate baseline variant, no longer legitimately called “temporary.”

**MINTTAP DIRECTION:** once an exception is intentionally permanent, either incorporate it into an explicit supported baseline/profile with its risk decision or remove it. Do not retain permanent behavior under a fictional temporary-waiver label.

Guard: `temporary label ≠ temporary behavior`.

## 5. Exception object / decision record

A security-relevant exception should be reconstructable with at least:
- exception/control ID;
- baseline/control being deviated from;
- causal operational requirement;
- exact scope: users, clients, API operations, release/trust/schema generations, environment/provider surface;
- capabilities added/removed;
- security/privacy/availability/data-durability impact;
- compensating controls;
- owner and approving authority;
- activation time and evidence;
- expiry or mandatory review trigger;
- revocation/kill path;
- observability and expected denominator;
- tests proving both exception behavior and non-exception isolation;
- closure evidence and residual risk.

Exact MintTap roles and approval hierarchy remain **OPEN**.

## 6. Fail-safe scope: an exception must not become a transitive authority bridge

A compatibility exception for one narrow capability should not silently restore all privileges of an obsolete client. Example: allowing an old EFB to export local records does not imply permission to replay old outbox mutations or perform destructive server operations.

For PWA/EFB, separate capability classes such as:
`local read/export → remote read → ordinary current-generation write → reconciled queued operation → destructive/high-impact mutation`.

Guards:
- `exception for capability A ≠ authorization for capability B`;
- `legacy client supported for recovery ≠ legacy client supported for mutation`;
- `migration bridge exists ≠ old trust generation globally trusted`.

## 7. Feature flags and configuration are part of the security state

A source-code review can show the intended gate while runtime configuration disables or bypasses it. Conversely, a feature flag may be the legitimate delivery mechanism for staged enforcement. Therefore source/build identity alone is insufficient for control-conformance claims.

**SYNTHESIS:** evidence should bind, where applicable, source/build/deployment identity to the effective security-relevant configuration/flag/policy generation and the enforcement point that evaluated it.

Guards:
- `code contains gate ≠ runtime gate enabled`;
- `flag default secure ≠ every environment uses secure value`;
- `deployment succeeded ≠ policy generation converged`;
- `dashboard says enabled ≠ request path enforced it`.

## 8. Exception expiry must fail toward review, not silent privilege continuation

Expiry semantics depend on control type. For a temporary privilege/bypass, automatic expiry to the safer baseline is generally the desired direction when operationally feasible. For a compatibility bridge whose abrupt removal could destroy data availability, expiry may instead force explicit review/re-entry rather than silently continue or destructively cut off local recovery.

**MINTTAP DIRECTION:** no security-relevant temporary exception should become permanent merely because its expiry job failed or nobody revisited it.

Guards:
- `expiry timestamp passed ≠ runtime exception actually disabled`;
- `review overdue ≠ exception implicitly renewed`;
- `automatic expiry ≠ safe for every availability/data-recovery control`.

## 9. SOURCE — continuous monitoring is evidence of control effectiveness, not merely asset visibility

NIST SP 800-137 describes continuous monitoring as providing visibility into assets, threats/vulnerabilities and the effectiveness of deployed controls, supplying information to respond when controls are inadequate. NIST SP 800-128 likewise treats monitoring and assessment as part of security-focused configuration management.

Sources:
- https://csrc.nist.gov/pubs/sp/800/137/final
- https://www.nist.gov/publications/guide-security-focused-configuration-management-information-systems-0

**SYNTHESIS:** exception governance needs evidence of effective enforcement and population, not merely an exception registry. A registry can say “three clients waived” while an implementation bug waives thirty.

Guards:
- `exception registry count ≠ effective waived population`;
- `telemetry quiet ≠ baseline conformance`;
- `control configured ≠ control effective`.

## 10. Denominator discipline for offline fleets

The long-offline PWA problem from 117 applies directly. An exception may be removed centrally while clients that have not reconnected retain old executable/configuration state. Conversely, a server-side fail-closed generation gate can constrain remote authority even when client convergence is incomplete.

Distinguish:
1. exception removed from control plane;
2. server enforcement updated;
3. observed online clients conform;
4. known fleet denominator reconciled;
5. long-offline/unknown clients re-enter through current policy;
6. old local executable/configuration state is remediated where required.

Guards:
- `waiver revoked centrally ≠ every client remediated`;
- `zero observed waived clients ≠ zero waived clients`;
- `offline client stale ≠ server must honor stale exception`.

## 11. Exception nesting and composition

Multiple individually bounded exceptions can compose into an unsafe path. Example: a stale-client compatibility allowance + emergency identity bypass + replay exception may collectively recreate the authority that the permanent control was designed to remove.

Evaluate not only each exception but also:
- shared subject/client population;
- overlapping capability scope;
- common trust/identity generations;
- temporal overlap;
- whether compensating controls depend on each other;
- whether one exception disables the detector for another.

Guard: `each exception individually bounded ≠ combined exception set bounded`.

## 12. Drift detection model

For a security-relevant control, compare four layers:

1. **approved baseline** — what governance says should hold;
2. **declared deployment/configuration state** — what tooling/provider says is configured;
3. **effective enforcement state** — what the actual request/client path does;
4. **observed population/outcomes** — which subjects actually encountered which policy.

A mismatch between layers is evidence to investigate, not automatic proof of compromise.

Useful drift classes:
- approved ≠ declared;
- declared ≠ effective;
- effective ≠ observed due to instrumentation/denominator gaps;
- exception scope ≠ actual affected population;
- expired/revoked exception still effective;
- baseline changed but old exception references obsolete semantics.

## 13. Track C validation campaign

Future product evidence should cover at least:
1. baseline client is allowed exactly intended capabilities;
2. stale client is denied restricted remote mutation;
3. scoped compatibility exception enables only named capability;
4. adjacent capability remains denied;
5. destructive operation remains denied unless separately authorized;
6. exception applies only to named client/release/trust generation;
7. non-exception client cannot inherit it;
8. expiry removes temporary privilege or forces explicit review state;
9. failed expiry automation is detected;
10. revoked exception remains revoked after service restart/deploy rollback;
11. configuration rollback does not revive obsolete exception;
12. feature-flag default and environment override are both tested;
13. provider/edge policy matches application expectation;
14. monitoring outage does not cause fail-open exception behavior;
15. registry population is reconciled with effective enforcement population;
16. nested exceptions are composition-tested;
17. emergency bypass cannot become a standing credential;
18. long-offline client cannot resurrect an expired server-side exception;
19. local read/export remains available where recovery policy requires it;
20. unreconciled outbox remains blocked;
21. exception UX accurately communicates restricted capability;
22. keyboard/screen-reader/reflow/localization preserve restriction/error semantics;
23. privacy review covers exception telemetry and identifiers;
24. performance/availability impact of stricter baseline is measured;
25. exact managed-iPad/WebKit behavior is tested where relevant;
26. negative canary proves forbidden path still fails;
27. canary itself is not the authorization mechanism;
28. exception closure leaves no hidden flag/account/provider rule;
29. accepted permanent deviation is promoted into explicit baseline/profile;
30. exact source/build/deployment/configuration/runtime identity accompanies PASS evidence.

## 14. Cross-repository transfer

### Design Studio
Canonical Web Design is Stage 3 PRACTICE / NOT PASSED. W073 requires diagnostic replication → repaired widget → production Web build → served browser → independent engine before stronger runtime claims. This supports the same evidence discipline: a declared repair or configuration is not runtime conformance. It is not direct security evidence.

### Software Engineering
Software Engineering remains Foundation IN STUDY. M006 explicitly distinguishes installability, offline capability, service-worker execution, storage policy and continuous background execution and requires capability-aware acceptance rather than API-shape assumptions. That transfers well to exception scoping: a waiver should name the capability actually changed. Exact feature-flag/configuration implementation remains Engineering-owned and OPEN.

## 15. EFB / LogMate-like judgment

The most dangerous compatibility waiver is one that converts “old client may preserve/export its local records” into “old client may keep indefinite remote mutation authority.” For an offline-first flight-log PWA, support and authority should remain separable.

A defensible compatibility bridge could preserve local usability and a narrow recovery/export path while the server requires current trust/API/reconciliation state for mutations. Whether LogMate can implement this depends on its actual auth, API, storage, sync and managed-iPad architecture, all currently OPEN.

## 16. PASS gate

Generic PASS requires ability to:
- explain baseline vs deviation vs effective runtime state;
- distinguish intentional bounded exception from silent control erosion;
- scope exceptions by capability, subject/generation and time/review trigger;
- explain feature-flag/provider/configuration drift as part of security state;
- reason about offline fleet denominators and stale exception resurrection;
- detect unsafe composition of individually bounded exceptions;
- define runtime conformance/negative-oracle evidence;
- keep product/runtime claims OPEN without exact evidence.

**Assessment: PASS (generic).**

## Persistent guards added by 121

- `baseline documented ≠ runtime conforms`;
- `same source revision ≠ same effective security configuration`;
- `deviation exists ≠ control governance failed`;
- `operational need asserted ≠ deviation justified`;
- `exception approved ≠ exception safe indefinitely`;
- `documented exception ≠ effective scope matches documentation`;
- `temporary label ≠ temporary behavior`;
- `exception for capability A ≠ authorization for capability B`;
- `code contains gate ≠ runtime gate enabled`;
- `expiry timestamp passed ≠ runtime exception actually disabled`;
- `review overdue ≠ exception implicitly renewed`;
- `exception registry count ≠ effective waived population`;
- `waiver revoked centrally ≠ every client remediated`;
- `each exception individually bounded ≠ combined exception set bounded`.

## OPEN / next boundary

Actual MintTap/LogMate control baselines, feature flags, auth/session/API gates, provider settings, managed-iPad policy, exception owners, risk approvers and runtime telemetry remain OPEN.

The highest-value adjacent generic boundary is **control-assurance independence and anti-self-attestation**: when the same compromised or misconfigured control plane both enforces a security rule and reports that the rule is healthy, determine what independent evidence is needed to detect false conformance without building an impractical duplicate system.