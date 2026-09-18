# 128 — PWA Recovery Dependency Drift & Resilience-Budget Governance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 103–127 recovery/assurance chain; Track A origin/Service Worker/client-generation mechanics; Track C destructive regression and change-triggered validation; Software Engineering for concrete topology/IaC/provider automation.

## Purpose

127 established that recovery independence is scenario-relative and depends on the end-to-end dependency graph rather than provider count. 128 addresses the next operational problem: a recovery design can be correct on Monday and silently lose independence after an SSO migration, CI consolidation, registrar change, administrator turnover, provider acquisition, new recovery mailbox, key-custody change or convenience integration.

Central rule:

> **Recovery resilience is a governed, per-capability risk allocation that must be re-evaluated when dependency topology changes; it is not a permanent property earned by one successful drill.**

The objective is not maximum redundancy. It is to preserve enough independently recoverable capability for the consequence and recovery objective while avoiding uncontrolled common-mode concentration and unnecessary multi-provider complexity.

## 1. Five-track balance and allocation

- **A Platform/Browser — dependency supplier:** owns DNS/origin/TLS/navigation/Service Worker/client-generation mechanics. A central dependency change does not imply installed-client convergence.
- **B UX/IA/Content — consumer:** recovery/degraded states must communicate partial capability and uncertainty rather than a binary `online/offline` story.
- **C Quality — high dependency pressure:** owns change-triggered regression, destructive cut-set tests and evidence that a declared alternate still works after topology change.
- **D Search/Analytics — consumer:** measurement/search dependencies may themselves become concentrated and cannot silently become the sole recovery denominator.
- **E Architecture/Security/Operations — highest-risk owner:** owns dependency inventory, concentration decisions, resilience budget, change triggers, exception expiry and provider due diligence.

Allocation remains intentionally E-heavy with A/C as the strongest dependencies.

## 2. SOURCE — resilience decisions are risk decisions, not redundancy contests

NIST CSF 2.0 is outcome- and risk-oriented rather than prescriptive. It is designed for organizations of different sizes and maturity and does not prescribe one implementation for an outcome.

Sources checked 2026-09-18:
- https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-enterprise-risk-management-quick-start-guide

NIST SP 1303 describes integrating cybersecurity risk monitoring, evaluation and adjustment across organizational units and programs. This supports treating dependency concentration as a changing risk posture rather than a one-time architecture checkbox.

**SYNTHESIS:** the correct amount of recovery independence depends on consequence, risk tolerance, recovery objective and lifecycle cost.

Guards:
- `more redundancy ≠ proportionately better resilience`;
- `shared dependency exists ≠ shared dependency is automatically unacceptable`;
- `accepted concentration ≠ unmanaged concentration`.

## 3. SOURCE — supplier resilience and provenance remain due-diligence concerns

NIST SP 800-161 Rev.1 Update 1 treats supply-chain security, resilience, reliability and reduced visibility into suppliers as risk-management concerns. NIST SP 1326, published 2026-07-08, identifies provenance, resilience and supply-chain tiers as due-diligence components.

Sources:
- https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final
- https://www.nist.gov/publications/nist-cybersecurity-supply-chain-management-due-diligence-assessment-quick-start-guide

**TRANSFER VALIDATION:** a dependency graph cannot be frozen. Provider ownership, upstream dependencies, account recovery, control-plane architecture and product terms can change. Where those facts matter to a recovery claim, they remain CHANGE WATCH.

Guard: `vendor relationship unchanged ≠ dependency topology unchanged`.

## 4. SOURCE — redundancy and diversity have costs and can create new risk

NIST SP 800-160 Vol.2 cyber-resiliency material treats redundancy and diversity as useful resiliency techniques but also recognizes that diversity can increase attack surface, lifecycle cost and inconsistency risk. The engineering lesson is that redundancy must be protected and deliberately designed rather than accumulated.

Source family:
- https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final

**SYNTHESIS:** a resilience control can consume security and operational budget while reducing one failure mode. This is why a small app company should not treat active-active multi-cloud as a maturity badge.

Guard: `diversity added ≠ net risk reduced`.

## 5. Resilience budget model

A **resilience budget** is a governance model, not a monetary ledger and not a NIST-defined term. It records how much common-mode concentration is intentionally tolerated for a capability under stated consequences and recovery objectives.

For each essential capability, record:
1. capability and consequence if unavailable/compromised;
2. target recovery objective or bounded manual-recovery expectation;
3. primary path;
4. alternate/manual path;
5. known shared dependencies;
6. accepted concentration/cut set;
7. why that concentration is acceptable;
8. compensating controls;
9. evidence/drill supporting the decision;
10. change triggers that invalidate or reopen the decision;
11. owner/review authority;
12. OPEN/unknown provider facts.

Do **not** reduce this to one numeric `resilience score`. A score can hide whether the same SSO, person, device or registrar is the actual fatal cut set.

Guards:
- `resilience budget ≠ permission to ignore dependencies`;
- `one score ≠ dependency graph`;
- `risk accepted once ≠ topology change pre-accepted`.

## 6. Concentration classes

Useful classes for governance:

### Class 0 — deliberate single path
Low-consequence capability where provider-native recovery and tested backup are enough. No false independence claim is made.

### Class 1 — shared dependency with bounded recovery
Primary and alternate share a dependency, but the consequence and manual recovery window make this acceptable. Example: same operator controls two paths, while an offline recovery package and documented succession path bound operator loss.

### Class 2 — independence required for a named hazard
At least one alternate must survive a stated failure such as hosting loss, IdP lockout or source-host loss. Independence is claimed only for that hazard.

### Class 3 — stronger multi-domain independence
Reserved for high-consequence/irreplaceable or safety-relevant capability where identity, administrative, data-copy and evidence common modes require stronger separation after threat analysis.

These classes are a local synthesis, not a universal industry standard.

**MINTTAP DIRECTION:** select the lowest complexity class that satisfies the actual consequence and recovery requirement. Actual MintTap/LogMate classification is OPEN.

## 7. Change-triggered invalidation

A dependency claim should be marked **STALE / REVALIDATION REQUIRED** when a material change can alter its cut sets. High-value triggers include:
- IdP/SSO federation or consolidation;
- administrator/owner turnover;
- MFA/recovery-device or recovery-mailbox change;
- registrar or DNS migration;
- source repository migration/mirroring change;
- CI/CD centralization or shared runner/secrets introduction;
- hosting/CDN/provider migration;
- provider acquisition or documented upstream/control-plane change;
- KMS/key-custody/secrets migration;
- billing/legal-owner change that affects account recovery;
- backup/export format or encryption change;
- IaC/automation expanded to manage both primary and alternate paths;
- incident-created emergency path converted to permanent use;
- PWA origin/path/scope change affecting Service Worker update/control;
- API/trust-generation retirement affecting stale-client re-entry.

Not every application release requires full recovery re-analysis. Trigger scope should follow the affected dependency claim.

Guards:
- `any code change ≠ full resilience re-certification`;
- `material dependency change ≠ wait for annual review`;
- `change completed successfully ≠ recovery claim preserved`.

## 8. Dependency-diff discipline

For material infrastructure/identity changes, compare **before → after**:
- nodes added/removed;
- edges added/removed;
- authority/credential path changes;
- newly shared dependencies;
- formerly shared dependencies removed;
- recovery path now requiring a failed primary service;
- new automation blast radius;
- new provider/support/account-recovery assumptions;
- evidence path changes;
- installed-PWA implications.

The important output is not `architecture changed`; it is `which prior recovery claims remain valid, become stronger, become weaker, or become unknown`.

Suggested states:
- **VALID — unchanged relevant dependencies**;
- **VALIDATED-AFTER-CHANGE — affected claim retested**;
- **WEAKENED-ACCEPTED — concentration increased and explicitly accepted**;
- **MITIGATION-REQUIRED**;
- **UNKNOWN / PROVIDER FACT OPEN**;
- **STALE — evidence predates material topology change**.

## 9. Resilience-budget consumption

A change **consumes resilience budget** when it increases common-mode exposure or recovery complexity without removing the affected consequence. Examples:
- alternate provider moved behind same SSO;
- separate recovery mailbox moved into primary tenant;
- mirror repository made writable by the same compromised CI token;
- two backup copies encrypted by one unrecoverable online KMS;
- registrar and hosting placed under one account owner/recovery channel;
- manual alternate publication replaced with shared IaC that can delete both environments;
- independent evidence sink moved into production account.

A change can **restore budget** by removing a critical cut set, reducing standing privilege, adding delayed/versioned copies, improving bounded manual recovery or adding a genuinely independent authority path.

No numeric arithmetic is required. The budget is a disciplined statement of tolerated concentration.

Guard: `cost optimization ≠ free resilience consumption`.

## 10. When shared dependencies are acceptable

A shared dependency may be rational when:
- consequence is modest;
- provider-native recovery is independently usable and tested;
- manual recovery fits the objective;
- an offline/versioned export protects irreplaceable data;
- the shared dependency has strong recovery and is not itself the dominant threat;
- removing it would create disproportionate attack surface/operational complexity;
- the concentration is explicit, owned and periodically challenged.

Examples can include one primary hosting provider, one source platform or one CI path for a small public company site when source/export/domain recovery are separately protected and rebuild time is acceptable.

**CONTRADICTION:** `single provider = immature` is rejected as a universal rule.

## 11. When mitigation becomes necessary

Mitigation pressure rises when:
- one dependency can simultaneously destroy production, backup and recovery authority;
- the dependency controls domain + identity + evidence with no external recovery proof;
- irreplaceable local/user data has no usable independent recovery path;
- recovery time exceeds tolerated consequence;
- provider/account suspension can remove every control path;
- compromise can propagate automatically into all replicas;
- one person/device/mailbox is the only organizational recovery root;
- a new shared dependency invalidates a previously required independence claim;
- repeated drills show alternate recovery is not executable.

Mitigation options should target the cut set: separate credentials, delayed/versioned export, independent registrar recovery, alternate administrator, offline recovery package, manual publication path, provider diversity, or stronger evidence separation. Do not default to the most expensive option.

## 12. PWA-specific drift

PWA recovery has two linked but non-identical graphs.

Central changes can affect:
- origin/DNS/TLS;
- Service Worker script publication;
- worker scope/path;
- manifest/install surface;
- API/trust-generation gates;
- storage/sync backend;
- release evidence.

Installed-client state additionally depends on:
- browser/WebKit implementation and policy;
- network opportunity;
- update check;
- install/activate/control lifecycle;
- local cache/schema/data;
- authentication/trust;
- reconciliation/outbox state.

Therefore provider/CI/domain migration may require new central recovery evidence while leaving long-offline installed clients untouched until reconnect.

Guards:
- `central dependency graph updated ≠ installed fleet graph updated`;
- `new origin deployment path validated ≠ old installed worker converged`;
- `provider consolidation accepted ≠ stale-client authorization widened`.

## 13. EFB / LogMate-like application boundary

For a company iPad that may remain offline:
- do not spend central redundancy budget pretending it can force an offline device to update;
- preserve local utility/read/export independently from remote mutation authority where product design allows;
- treat browser storage persistence/eviction, background execution, MDM behavior and direct device-to-device sync as separate runtime validations;
- after central dependency migration, returning clients must still satisfy current server-side trust/API/reconciliation policy;
- a migration that changes origin, Service Worker scope or authentication may create a new product-specific compatibility/recovery requirement and must not be assumed safe from generic PWA knowledge.

Actual managed-iPad/WebKit/MDM/network behavior remains OPEN.

## 14. Track C validation campaign

Change-triggered validation should include at least:
1. move alternate hosting behind the primary SSO and detect independence loss;
2. move recovery mailbox into primary tenant and invalidate identity-recovery claim;
3. rotate administrator and prove recovery material remains usable by authorized successor;
4. migrate registrar and prove domain recovery without hosting account;
5. migrate DNS while registrar remains available;
6. centralize CI and detect shared publication credential;
7. let one IaC role target both primary/alternate and detect blast-radius increase;
8. migrate backup encryption to a shared KMS and test KMS-loss cut set;
9. move evidence sink into production account and detect evidence-independence loss;
10. provider acquisition/upstream change is recorded as UNKNOWN until verified;
11. expire recovery credential and ensure drill fails rather than silently PASSing;
12. remove primary IdP and exercise bounded manual recovery;
13. test source-host loss after repository migration;
14. test provider account suspension after billing/legal-owner change;
15. verify offline recovery package after format/key migration;
16. verify destructive recovery does not broaden application authority;
17. publish clean PWA after CI/provider migration while a test client remains on old worker;
18. prove old worker cannot use obsolete remote mutation generation;
19. preserve local read/export where designed;
20. keep compromise-era outbox quarantined after central migration;
21. dashboard marks affected recovery claim STALE after material dependency change;
22. revalidation clears only the tested claim, not unrelated claims;
23. provider-specific unknown remains OPEN instead of being inferred from vendor branding;
24. a low-consequence shared dependency can be explicitly accepted with owner/review trigger;
25. a high-consequence shared cut set triggers mitigation rather than convenience acceptance;
26. added redundancy does not introduce broader standing privilege unnoticed;
27. removed redundancy updates runbooks and monitoring so dead paths are not reported healthy;
28. annual review catches drift not captured by automation;
29. change review catches drift before the next annual review;
30. post-change negative canary confirms stale credentials/client generations remain denied.

## 15. Automation vs manual governance

Automation can help detect:
- repository/CI/hosting configuration changes;
- identity-provider configuration changes where APIs expose them;
- account/role/credential changes;
- backup job/export failures;
- IaC graph changes;
- domain/DNS changes;
- expired recovery material.

But provider upstream dependencies, support recovery semantics, legal/account ownership and human succession may not be fully machine-readable. Manual due diligence and destructive drills remain necessary.

Guard: `dependency inventory automated ≠ dependency independence proven`.

## 16. Cross-track transfer

### Track A
A owns the mechanics that determine whether origin/Service Worker changes affect installed clients. 128 consumes these mechanics; it does not redefine them.

### Track B
B should define language/states for `service restored`, `client update required`, `sync blocked`, `reconciliation required`, and `recovery status unknown` without implying universal recovery.

### Track C
C owns dependency-diff regression and destructive tests. A successful infrastructure migration is not a recovery PASS until affected claims are revalidated.

### Track D
D should not treat analytics/search telemetry as independent recovery evidence when account/provider consolidation makes it share the failure domain.

## 17. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` was checked on 2026-09-18. It is now **W080 RESET-BASELINE + NAVIGATION CLOSURE**, Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED. It explicitly keeps cross-browser/Safari/Firefox, non-drag reorder/reset-history, persisted configuration, screen-reader, physical-device, field Core Web Vitals, full WCAG and human UX evidence OPEN. This is useful transfer evidence for honest runtime-state communication but does not prove recovery independence.

Software Engineering Studio `progress/STATUS.md` remains **FOUNDATION STUDY UNDERWAY**; no specialist has passed Foundation. Its current evidence deliberately distinguishes bounded SQLite/process/network tests from lower-layer/mobile/runtime claims. This supports the same evidence-boundary discipline, but no implementation evidence is promoted into 128.

Marketing evidence is not required for this gate. Public resilience/availability claims must not exceed operational evidence.

## 18. SOURCE / SYNTHESIS / MINTTAP DECISION / OPEN boundary

**SOURCE:**
- NIST CSF 2.0 and SP 1303 support risk-based monitoring/evaluation/adjustment;
- SP 800-161 Rev.1 Update 1 and SP 1326 support supplier resilience/provenance/tier due diligence;
- SP 800-160 Vol.2 supports deliberate cyber-resiliency engineering and recognizes redundancy/diversity trade-offs.

**SYNTHESIS:** resilience budget, concentration classes, dependency-diff states and trigger list are local operational models derived from those principles and studies 103–127.

**MINTTAP DIRECTION:** prefer explicit bounded concentration + tested recovery over ceremonial provider duplication. Escalate separation where consequence/cut-set analysis justifies it.

**OPEN:** actual MintTap/LogMate provider topology, RTO/RPO, consequence classes, administrators, IdP, registrar/DNS, CI/CD, hosting, evidence sink, backup/key custody, managed-iPad/WebKit/MDM behavior and legal/safety constraints.

**CHANGE WATCH:** provider ownership/upstream architecture, account recovery, identity federation, browser/PWA behavior, MDM policy, export/backup semantics and provider terms.

## 19. PASS gate

Generic PASS requires ability to:
- explain why recovery independence drifts after topology change;
- maintain scenario-relative dependency claims rather than provider counts;
- distinguish intentional bounded concentration from silent common-mode erosion;
- use a resilience-budget model without collapsing it into a fake numeric score;
- define change triggers and dependency-diff states;
- choose proportionate mitigation targeted at the actual cut set;
- separate central PWA recovery from installed-client convergence;
- define destructive post-change validation and preserve unknown provider facts as OPEN.

**Gate result: PASS (generic).** Product/provider/managed-iPad/runtime validation remains OPEN.

## 20. Adjacent high-value question completed before stop

A resilience budget can itself become governance theater if exceptions are accumulated but never retired. Therefore every accepted concentration needs an owner and a **reconsideration trigger**, not merely a review date. If a new dependency makes a previously accepted cut set materially more consequential, the old acceptance cannot be inherited automatically.

Additional guards:
- `waiver still documented ≠ waiver still justified`;
- `review date not reached ≠ material change can wait`;
- `old risk acceptance ≠ acceptance of new dependency graph`;
- `resilience control added ≠ resilience debt retired`.

## Next high-value target

**PWA resilience-debt retirement & recovery-objective evidence governance** — connect tolerated concentration to explicit recovery objectives and consequence; prevent temporary manual bridges, stale alternates and untested recovery paths from accumulating as permanent resilience debt; define when a recovery path should be retired, replaced or re-proven rather than kept alive indefinitely.