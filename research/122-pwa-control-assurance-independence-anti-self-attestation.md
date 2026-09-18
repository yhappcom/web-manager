# 122 — PWA Control-Assurance Independence & Anti-Self-Attestation

Status: **PASS (generic) / PRODUCT RUNTIME + ASSURANCE-OWNER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 117–121 containment/baseline/exception chain; Track A browser/PWA enforcement mechanics; Track C assessment and negative-probe evidence; Track D denominator/telemetry discipline; Software Engineering for exact enforcement and observability implementation.

## Purpose

121 separated approved baseline, declared configuration, effective enforcement and observed population. The adjacent assurance problem is circular evidence: the same control plane can enforce a rule and report that the rule is healthy. A compromised, misconfigured or bypassed component may therefore produce a plausible green signal while the forbidden path remains available.

This study defines proportionate assurance independence. It does **not** require full duplication of every control. It asks which claims need evidence outside the failure/authority domain that could make the claim false, and which lower-risk claims can reasonably rely on self-observation plus periodic independent challenge.

## 1. Five-track balance

- **A Platform/Browser:** identifies the real enforcement point and browser/PWA state that can diverge from server/control-plane declarations.
- **B UX/IA/Content:** consumes restricted/degraded states; assurance uncertainty must not be presented to users as verified normality where the distinction matters.
- **C Quality:** owns examine/interview/test evidence, negative probes, independent runtime checks, provenance and oracle quality.
- **D Search/Analytics:** owns denominator and observation-bias discipline; telemetry from only admitted/current clients cannot prove excluded populations are safe.
- **E Architecture/Security/Operations:** highest-risk owner; defines assurance claim, threat/failure domain, required independence, escalation and closure.

E remains the bottleneck. C receives increased dependency pressure because an assurance claim needs a credible oracle, not merely more telemetry.

## 2. SOURCE — assurance is distinct from control functionality

NIST SP 800-53 Rev.5 explicitly treats security/privacy from both functionality and assurance perspectives: the mechanism can provide a function while assurance measures confidence that the capability is actually provided. NIST SP 800-53A Rev.5 provides assessment methodology, and NIST defines assessment methods as **examine, interview and test**.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final
- https://csrc.nist.gov/glossary/term/assessment_method

**SYNTHESIS:** configuration declaration is an assessment object, not automatically the truth of runtime enforcement. A high-value claim should be challenged by behavior/evidence capable of falsifying it.

Guards:
- `control exists ≠ control effectiveness assured`;
- `control reports healthy ≠ forbidden path is impossible`;
- `configuration evidence ≠ behavioral evidence`;
- `more telemetry from one authority domain ≠ independent assurance`.

## 3. SOURCE — assessor independence is risk-proportionate, not synonymous with an external auditor

NIST SP 800-53 CA-2(1) describes independent assessors as impartial and free from actual/perceived conflicts concerning development, operation, sustainment, management or determination of control effectiveness. It also states that independence can be achieved inside an organization; when structure is small, independent expert review of assessment results can improve completeness, accuracy, integrity and reliability. The required level is risk-based.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** independence is a property of the evidence/assessment relationship, not a requirement to buy a duplicate external platform. A small app company can use separation of role, failure domain, credential, data source or active probe according to consequence.

Guards:
- `independent assurance ≠ external vendor required`;
- `different dashboard ≠ independent evidence`;
- `different team ≠ independent evidence if both consume the same corruptible source`;
- `same team ≠ zero assurance if the test independently exercises the mechanism and produces protected evidence`.

## 4. SOURCE — protect audit evidence from the system being audited

NIST SP 800-53 AU-9 requires protection of audit information/tools from unauthorized access, modification and deletion. AU-9(2) specifically describes storing audit records on a physically different system/component because compromise of the audited system should not automatically compromise its audit records.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** assurance evidence should not always share the exact compromise domain of the control it is intended to validate. This does not mean every log must be physically separate; it means high-consequence claims need an evidence path whose failure is not perfectly correlated with the enforcement failure being tested.

Guards:
- `local audit says deny ≠ request was independently denied`;
- `record + log controlled by same compromised authority ≠ two witnesses`;
- `separate storage ≠ independent truth if the same producer can fabricate both before export`.

## 5. SOURCE — continuous monitoring must address effectiveness

NIST SP 800-137 defines ISCM as providing visibility into the effectiveness of deployed controls and ongoing assurance aligned with risk tolerance. SP 800-137A assesses the completeness/effectiveness of the monitoring program itself.

Sources:
- https://csrc.nist.gov/pubs/sp/800/137/final
- https://csrc.nist.gov/pubs/sp/800/137/a/final

**SYNTHESIS:** monitoring cannot become recursively trusted merely because it is continuous. For critical claims, periodically assess the monitor/oracle and preserve a path to discover that the monitoring system itself is blind, stale or misleading.

Guards:
- `continuous monitoring ≠ continuously correct monitoring`;
- `monitor green ≠ monitor coverage complete`;
- `detector deployed ≠ detector capable of seeing the failure mode`.

## 6. Assurance independence dimensions

Do not reduce independence to one binary label. Evaluate at least:

1. **authority independence** — can the enforcement administrator alter the assurance result?
2. **credential independence** — does the probe use a distinct credential/path from the control administrator?
3. **execution-path independence** — does evidence traverse the actual protected path rather than only query configuration state?
4. **data-source independence** — is the evidence produced by a source outside the same mutable state?
5. **failure-domain independence** — would one provider/component compromise defeat both control and oracle?
6. **temporal independence** — can a brief bypass occur between periodic checks?
7. **population independence** — does observation include stale/unknown/exception populations rather than only successful current clients?
8. **human/organizational independence** — can the same actor silently approve, implement and attest a high-risk deviation?

No single dimension is sufficient for every claim.

## 7. Proportionate assurance tiers

Use consequence and plausible common-mode failure to choose assurance strength.

### Tier 0 — declaration only
Suitable only for low-consequence inventory/status claims. Configuration/provider declaration may be enough for operational convenience, not security proof.

### Tier 1 — self-observation + behavioral test
Control telemetry plus a negative test that exercises the real path. Useful for ordinary regression assurance where compromise of the control plane is not the assumed threat.

### Tier 2 — independently sourced behavioral evidence
Separate probe/credential/evidence sink challenges the actual enforcement path. Appropriate for high-impact authorization, stale-client denial, destructive-operation gates and exception boundaries.

### Tier 3 — stronger separation / independent assessment
Independent reviewer/team, protected evidence repository, separate administrative domain or external observation when compromise/common-mode risk justifies it.

**MINTTAP DIRECTION:** do not default all controls to Tier 3. Escalate independence with impact, reversibility, attacker/control-plane overlap, history of drift, exception complexity and difficulty detecting silent failure.

Guard: `higher assurance ≠ maximum duplication everywhere`.

## 8. Negative probes are especially valuable for authorization claims

A positive probe showing that a current client can write proves availability of an allowed path. It does not prove stale/revoked/unknown clients are denied.

For a PWA/EFB mutation gate, useful independent challenges include:
- current trust/API generation succeeds;
- stale generation fails;
- revoked credential fails;
- expired exception fails;
- adjacent capability outside a narrow waiver fails;
- unreconciled outbox replay fails;
- destructive operation remains denied when only ordinary write is allowed;
- long-offline re-entry cannot resurrect obsolete authority.

Guards:
- `allowed path succeeds ≠ forbidden path denied`;
- `negative probe configured ≠ negative probe executed`;
- `probe receives deny ≠ production population universally denied`.

## 9. Oracle independence vs authorization mechanism

A canary/probe must not become the thing that authorizes production. Otherwise a broken canary can either grant access or make the test circular.

Separate:
- **policy/enforcement mechanism** — decides/blocks production requests;
- **probe identity/input** — intentionally exercises expected allow/deny cases;
- **oracle** — evaluates actual outcome against expectation;
- **evidence sink** — preserves result/provenance;
- **alert/decision path** — reacts to mismatch.

Guard: `canary proves gate ≠ canary should be the gate`.

## 10. Common-mode failure analysis

Two observations are not independent if the same failure can falsify both. Examples:
- application dashboard and audit log both read the same policy database;
- provider console and exported report are generated by the same provider control plane;
- application deny telemetry and test harness both trust the same mocked middleware;
- two admin accounts are recoverable through the same compromised identity domain;
- client and server both accept the same obsolete trust generation because a shared configuration bundle drifted.

**SYNTHESIS:** count independent failure domains, not dashboards, files or copies.

Guard: `two evidence artifacts ≠ two independent evidence sources`.

## 11. PWA / Service Worker assurance cases

Service Worker state creates a useful separation between server declaration and installed-client reality.

A server may truthfully report that only clean `sw.js` is deployed while an offline client still runs an older/hostile worker generation. Conversely, a client may report its local generation while remote API policy correctly denies obsolete authority.

Therefore distinguish assurance claims:
1. clean worker is currently served;
2. update endpoint/network path serves expected bytes/headers;
3. a given client fetched/installed/activated the worker;
4. the worker controls the relevant client;
5. local cache/data generations are expected;
6. remote mutation authority is current;
7. fleet denominator has converged.

No one signal proves all seven.

Guards:
- `server serves clean worker ≠ installed client clean`;
- `client reports current worker ≠ remote authorization current`;
- `remote authorization current ≠ local executable/data state clean`.

## 12. EFB / LogMate-like assurance model

For an offline-first company iPad, the strongest practical invariant is not “every client is continuously observable.” That is incompatible with legitimate long-offline operation.

A more defensible generic direction is:
- local records remain usable/recoverable according to product policy while offline;
- remote mutation authority is checked at re-entry against current server-side trust/API/reconciliation policy;
- a stale/unknown client cannot self-attest its way around that gate;
- high-impact server-side gates have independent negative probes or equivalent challenge evidence;
- fleet convergence claims require a real denominator, not only active-client telemetry;
- managed-iPad/WebKit behavior remains separately validated.

Actual LogMate auth, API, storage, sync, Service Worker and MDM architecture remain **OPEN**.

## 13. Exception/waiver assurance

121's exception object needs assurance that actual runtime scope matches approved scope. For higher-risk exceptions, use evidence that can detect:
- waiver affects more subjects than registry states;
- expiry/revocation flag changed but enforcement did not;
- nested exceptions compose into forbidden authority;
- provider/edge policy bypasses application expectation;
- monitoring outage suppresses detection;
- rollback revives an obsolete exception.

A waiver owner should not be the sole source of proof that the waiver is correctly bounded when the consequence is high.

Guard: `exception owner attests bounded ≠ runtime scope independently bounded`.

## 14. Privacy and availability constraints

Independent assurance is not permission to duplicate sensitive user data into multiple telemetry systems. Prefer minimal probe identities, synthetic records, operation IDs/generations and bounded outcome metadata where they can answer the assurance question.

Likewise, an external probe should not create a destructive production side effect merely to prove the destructive path is blocked. Use safe test tenants/resources, preconditions, dry-run semantics or equivalent engineering mechanisms where available.

Guards:
- `independent telemetry ≠ duplicate all user data`;
- `security test valuable ≠ destructive production probe justified`.

## 15. Track C validation campaign

Future product evidence should cover at least:
1. baseline configuration identity can be reconstructed;
2. effective enforcement is behaviorally challenged;
3. current client allowed-path succeeds;
4. stale client forbidden mutation fails;
5. revoked credential fails;
6. expired exception fails;
7. adjacent capability outside waiver fails;
8. destructive path remains denied;
9. outbox replay gate is independently challenged;
10. negative probe is not authorization mechanism;
11. probe credential cannot administer the gate;
12. gate administrator cannot silently rewrite protected probe history where stronger independence is required;
13. provider declaration is cross-checked against actual request behavior;
14. monitoring outage is detectable;
15. stale monitor data cannot appear current without freshness provenance;
16. denominator includes known offline/retired/unknown states;
17. common-mode failure between control and oracle is documented;
18. Service Worker served/fetched/activated/controlling states remain separate;
19. local client self-report is not sole proof of remote authority;
20. server self-report is not sole proof of local remediation;
21. exception composition is challenged;
22. rollback cannot silently disable probe;
23. incident/emergency mode cannot suppress all independent evidence without detection;
24. evidence timestamps/source identities are reconstructable;
25. privacy minimization is verified;
26. synthetic probe data cannot contaminate real user records;
27. availability/performance cost of probes is measured;
28. keyboard/screen-reader/reflow states preserve restricted-state meaning where user-facing;
29. exact Safari/WebKit/managed-iPad behavior is tested where relevant;
30. independent reviewer can reproduce the claim from preserved evidence for high-risk controls.

## 16. Cross-repository transfer

### Design Studio
Canonical Web Design is Stage 3 PRACTICE / NOT PASSED. W074 has executed Chrome product-auth evidence for several LogMate scenarios, but the workflow remains red due to a malformed test command, unrelated stale test/API drift and genuine legacy-layout 200% overflows; no independent browser/Safari/device/human UX PASS is claimed. This is a useful evidence-provenance transfer: per-scenario executed evidence is stronger than inheriting a job-level label, but it is not security assurance for Web Manager controls.

### Software Engineering
Exact feature/configuration enforcement, probe implementation, auth/API generations, Service Worker release identity and protected telemetry are Engineering-owned. Existing capability-contract work is useful transfer evidence, not direct runtime proof. Current exact implementation remains OPEN.

## 17. Operational judgment — minimal independent evidence matrix

For each high-value control claim record:
- **claim** — e.g. stale generation cannot mutate;
- **enforcement point** — actual component/path;
- **self evidence** — config/log/health signal;
- **plausible common-mode failure** — how enforcement and self-report could fail together;
- **independent challenge** — probe/observer/reviewer capable of falsification;
- **evidence sink/provenance** — where result survives relevant compromise;
- **coverage/denominator** — what population/time the evidence actually supports;
- **assurance tier** — why this degree of independence is proportionate;
- **OPEN** — exact facts not yet proven.

This matrix prevents both extremes: trusting a green dashboard as proof and demanding a duplicate infrastructure for every low-risk control.

## 18. PASS gate

Generic PASS requires ability to:
- distinguish functionality from assurance;
- explain why self-attestation can become circular;
- select risk-proportionate independence rather than universal duplication;
- identify common-mode failure across apparently separate evidence;
- design negative behavioral probes that do not become authorization mechanisms;
- separate server, Service Worker, local-data, remote-authority and fleet-convergence claims;
- preserve privacy/availability while increasing assurance;
- keep product/runtime claims OPEN without exact evidence.

**Assessment: PASS (generic).**

## Persistent guards added by 122

- `control exists ≠ control effectiveness assured`;
- `control reports healthy ≠ forbidden path is impossible`;
- `configuration evidence ≠ behavioral evidence`;
- `more telemetry from one authority domain ≠ independent assurance`;
- `independent assurance ≠ external vendor required`;
- `different dashboard ≠ independent evidence`;
- `continuous monitoring ≠ continuously correct monitoring`;
- `monitor green ≠ monitor coverage complete`;
- `allowed path succeeds ≠ forbidden path denied`;
- `negative probe configured ≠ negative probe executed`;
- `canary proves gate ≠ canary should be the gate`;
- `two evidence artifacts ≠ two independent evidence sources`;
- `server serves clean worker ≠ installed client clean`;
- `client reports current worker ≠ remote authorization current`;
- `exception owner attests bounded ≠ runtime scope independently bounded`;
- `higher assurance ≠ maximum duplication everywhere`.

## OPEN / next boundary

Actual MintTap/LogMate control topology, assurance owners, probe identities, evidence repositories, auth/API/trust generations, provider boundaries, Service Worker/client state, managed-iPad behavior, privacy/legal constraints and production telemetry remain OPEN.

The highest-value adjacent generic boundary is **assurance-oracle compromise, stale evidence and freshness/replay resistance**: independent evidence is still weak if an attacker can replay an old PASS, suppress failed probes, backdate health, or keep a stale signed snapshot looking current. The next study should distinguish authenticity, freshness, liveness, coverage and continuity of assurance evidence without assuming an unavailable perfect trusted clock.