# 127 — PWA Recovery-of-Recovery Dependency Assurance & Correlated Provider Failure

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 103–126 recovery/assurance chain; Track A origin/Service Worker boundaries; Track C destructive common-mode drills; Software Engineering for concrete provider topology and automation.

## Purpose

126 established that replacement infrastructure cannot self-attest into organizational authority. 127 asks the next question: when several recovery paths appear independent, do they actually survive the same failure?

Central rule:

> **Recovery independence is a property of the end-to-end dependency graph under a stated failure scenario, not a count of accounts, copies, regions, vendors, or named recovery paths.**

A second repository, cloud account, recovery mailbox or provider can improve availability while contributing little recovery independence if both paths depend on the same identity tenant, administrator, device, billing/legal account, DNS authority, credential store, network path or recovery procedure.

## 1. Five-track balance and allocation

- **A Platform/Browser — dependency supplier:** owns origin/DNS/TLS/navigation/Service Worker/client-generation mechanics. Browser-side stale state is a separate failure domain from central provider recovery.
- **B UX/IA/Content — consumer:** degraded/recovery states must not imply universal recovery merely because one service path is reachable.
- **C Quality — high dependency pressure:** owns common-mode destructive drills, dependency-removal tests and recovery-path negative oracles.
- **D Search/Analytics — consumer:** analytics/search evidence can disappear with a provider or shared identity plane and must not be assumed to be an independent historical denominator.
- **E Architecture/Security/Operations — highest-risk owner:** owns dependency graph, common-mode analysis, recovery-path cut sets, provider concentration and proportionate redundancy decisions.

Allocation remains intentionally E-heavy; A/C are the high-value dependencies.

## 2. SOURCE — alternate capability must address common hazards, not merely exist

NIST SP 800-34 Rev.1 contingency guidance treats alternate processing capability as useful only when it can resume essential functions and notes separation from hazards affecting the primary site. NIST contingency-planning material frames recovery as coordinated plans, procedures and technical measures rather than a backup-copy count.

Sources checked 2026-09-18:
- https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
- https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning

**SYNTHESIS:** alternate capacity that shares the failed dependency is not an effective alternate for that scenario.

Guards:
- `alternate path exists ≠ alternate path survives the same hazard`;
- `two regions ≠ two provider control planes`;
- `two provider accounts ≠ two identity domains`.

## 3. SOURCE — supply-chain resilience requires visibility into dependencies

NIST SP 800-161 Rev.1 Update 1 addresses reduced visibility into how third-party products/services are developed, integrated and operated, and explicitly treats resilience/reliability as supply-chain concerns. The 2026 NIST SP 1326 Due Diligence Quick-Start Guide identifies provenance, resilience and supply-chain tiers as due-diligence components.

Sources:
- https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final
- https://www.nist.gov/publications/nist-cybersecurity-supply-chain-management-due-diligence-assessment-quick-start-guide

**TRANSFER VALIDATION:** web recovery design should model not only direct providers but dependencies that make recovery possible: identity, registrar, DNS, source, CI/CD, hosting/CDN, evidence sink, recovery communication, key custody, payment/legal ownership and operator devices.

Guard: `different vendor name ≠ independent supply-chain failure domain`.

## 4. Dependency graph model

Model a recovery system as capabilities and dependencies, not a flat vendor inventory.

Useful capability nodes include:
- prove organizational/operator identity;
- access registrar/domain control;
- change authoritative DNS;
- obtain/renew TLS/origin credentials where applicable;
- access source repository;
- verify source/release provenance;
- execute CI/build/release;
- publish origin/static assets/Service Worker;
- access hosting/CDN control plane;
- read independent evidence/incident history;
- recover/decrypt backup;
- rotate application credentials/keys;
- restore API/data plane;
- communicate recovery instructions;
- authorize stale-client re-entry and outbox reconciliation.

Dependency nodes can include:
- SSO/identity tenant;
- authenticator/recovery device;
- recovery mailbox/phone;
- administrator/person/role;
- provider parent account or organization;
- registrar/reseller;
- DNS provider;
- source host;
- CI/CD provider;
- artifact registry;
- hosting/CDN provider;
- cloud project/account;
- key/KMS/secrets service;
- billing/payment/legal contact;
- network/ISP/VPN path;
- evidence/log sink;
- offline recovery package.

**MINTTAP DIRECTION:** map dependencies by capability and failure scenario before purchasing duplication. Actual MintTap provider graph is OPEN.

## 5. Common-mode classes

At minimum test these common modes:
1. identity tenant disabled/compromised;
2. primary administrator unavailable;
3. operator device/authenticator lost;
4. recovery mailbox compromised;
5. provider-wide control-plane outage;
6. provider account suspension/billing/legal lock;
7. registrar/domain-control loss;
8. DNS-provider loss;
9. source-host loss;
10. CI/CD or artifact-signing compromise;
11. hosting/CDN loss;
12. KMS/secrets loss;
13. evidence sink lost with production account;
14. network/geographic disruption;
15. software supply-chain compromise affecting both primary and recovery tooling;
16. malicious/erroneous operator action propagated to replicas.

Guards:
- `replicated data ≠ independent administration`;
- `independent administration ≠ independent data copy`;
- `multi-region ≠ multi-provider`;
- `multi-provider ≠ independent identity/recovery`;
- `offline copy ≠ usable recovery path unless decrypt/verify/operate dependencies survive`.

## 6. Recovery-path cut-set reasoning

For each essential recovery capability, ask what smallest set of failed dependencies makes every viable recovery path fail. This is practical cut-set reasoning; no formal graph solver is required for small systems.

Example generic path:
`operator → SSO → repository → CI → hosting → origin`.

Nominal alternate:
`operator → same SSO → mirror repository → alternate hosting → origin`.

The alternate removes one hosting dependency but still collapses under SSO/operator failure. It is therefore independent for a hosting outage, not for identity compromise.

**SYNTHESIS:** independence is scenario-relative.

Guards:
- `path B differs from path A ≠ path B is independent for every threat`;
- `one shared dependency ≠ always unacceptable`; consequence and recoverability determine whether it is an unacceptable cut set.

## 7. Correlation beyond provider identity

Hidden correlation can exist through:
- same upstream cloud behind nominally different services;
- same SSO/SAML/OIDC tenant;
- same email domain/mailbox used for recovery;
- same password manager/device/authenticator;
- same single human owner;
- same DNS/registrar parent account;
- same billing card/legal entity contact;
- same CI token or secrets store;
- same IaC pipeline that can delete both environments;
- same destructive automation or compromised dependency;
- same network/VPN needed to reach both control planes.

Not every hidden correlation is knowable from public provider documentation. Unknown upstream dependencies remain **OPEN**, not assumed independent.

## 8. Independence dimensions

Assess at least:
- **administrative independence** — different authority/credential path;
- **identity independence** — recovery does not require the failed IdP/session;
- **provider/control-plane independence**;
- **data-copy independence**;
- **geographic/network independence** where relevant;
- **software/toolchain independence** where compromise propagation matters;
- **human-role independence** where one unavailable person is a critical cut set;
- **temporal independence** — corruption/deletion does not immediately propagate to every copy;
- **evidence independence** — recovery proof is not stored solely inside the disputed environment.

No single score should collapse these dimensions into a false `independent=true` label.

## 9. Bounded manual recovery can beat full duplication

Full active-active multi-provider duplication is not automatically the best control. It can add:
- configuration divergence;
- larger attack surface;
- more credentials and standing privilege;
- harder data consistency;
- more expensive testing;
- false confidence if identity/control remains shared.

For a small app-company website/PWA, a stronger pattern may be:
- one primary production platform;
- independently protected domain/registrar recovery;
- source/release/export backup outside the production failure domain;
- independently protected identity/recovery credentials;
- documented manual rebuild path;
- bounded offline recovery material;
- destructive recovery drills;
- explicit RTO/RPO/consequence acceptance.

**MINTTAP DIRECTION:** choose redundancy only after identifying the failure it must survive. Exact architecture is OPEN.

Guard: `resilience required ≠ active-active multi-cloud required`.

## 10. PWA-specific recovery graph

Central recovery and installed-client recovery have different graphs.

Central graph may include:
`registrar/DNS → hosting/origin → release artifact → Service Worker publication → API/data plane`.

Installed PWA graph additionally depends on:
`device availability → browser/WebKit policy → network opportunity → update check → worker install/activate/control → local schema/data → current authentication/trust → reconciliation`.

Therefore a provider-independent clean origin still does not prove installed-client convergence.

Guards:
- `provider failover succeeds ≠ installed PWA updated`;
- `origin continuity ≠ client-generation continuity`;
- `alternate hosting serves same URL ≠ stale worker/local data automatically reconciled`.

## 11. EFB / LogMate-like scenario

For company iPads that may remain offline:
- central provider redundancy cannot make an offline device fetch an update;
- local record availability may survive central/provider failure if browser storage survives, but persistence/eviction/backup remain separate product validations;
- direct unattended device-to-device synchronization is not inferred from provider independence;
- reconnect remains the authority boundary: current server-side trust/API/reconciliation policy must decide remote mutation;
- an alternate origin must not weaken stale-client gates merely to accelerate recovery;
- recovery communication should distinguish `central service restored` from `this iPad is current/reconciled`.

Exact managed-iPad/WebKit/MDM/network behavior remains OPEN.

## 12. Provider due-diligence questions

Before declaring two paths independent, obtain current evidence for applicable questions:
- Is service B hosted/control-planed by provider A or the same upstream?
- Can the same IdP/account administrator reset both?
- Are recovery emails/phones shared?
- Can one organization-owner role delete/transfer both?
- Are domain, DNS and hosting in one parent account?
- Can one CI credential publish to both?
- Are backups immutable/versioned or does deletion propagate?
- Is there an export format usable without the failed provider?
- What account-suspension and tenant-recovery paths exist?
- Can support recovery proceed without the primary SSO?
- What evidence proves account/domain ownership?
- Are provider status/API/control-plane dependencies shared?

Provider-specific answers are CHANGE WATCH and must be verified when providers are selected.

## 13. Track C destructive common-mode campaign

Implementation validation should include at least:
1. disable primary SSO and attempt every recovery path;
2. remove original administrator;
3. lose primary authenticator and recovery mailbox separately and together;
4. suspend primary cloud account while domain control survives;
5. lose registrar while hosting survives;
6. lose DNS provider while registrar survives;
7. lose source host while independently retained release/source export survives;
8. lose CI/CD while manual bounded publication path is tested;
9. compromise CI credential and prove alternate path does not reuse it;
10. lose hosting while alternate/manual rebuild works;
11. lose evidence sink and prove production logs are not the sole recovery proof;
12. delete/corrupt primary data and test delayed/versioned copy;
13. malicious IaC deletion targets both nominal environments and test detects correlation;
14. same SSO controls two providers and both paths correctly fail the identity-independence claim;
15. same administrator controls all recovery factors and test identifies person cut set;
16. independent registrar recovery works without hosting account;
17. provider support path cannot silently grant broader application authority;
18. clean alternate origin publishes while offline PWA remains stale;
19. returning stale PWA is denied obsolete remote mutation;
20. local read/export remains available where designed;
21. compromise-era outbox remains quarantined after provider failover;
22. recovery dashboard reports partial recovery rather than universal green;
23. dependency inventory detects a newly introduced shared IdP/provider;
24. annual/periodic drill detects expired recovery credentials;
25. drill proves a supposedly offline recovery package can actually be decrypted and interpreted;
26. wrong recovery key does not get replaced by a newly generated key and called restored;
27. alternate path meets the stated recovery objective under the tested scenario;
28. alternate path failure is recorded as evidence, not waived into PASS;
29. emergency credentials created for provider failover are retired;
30. post-recovery negative canary proves stale credentials/client generations remain denied.

## 14. Assurance tiers

- **Low consequence:** identify obvious single-person/single-account failures; tested provider recovery + independent credential backup may suffice.
- **Moderate consequence:** dependency graph across identity/domain/source/hosting/data/evidence; at least one tested recovery path for high-value common modes; versioned/exportable backups and separate recovery credentials.
- **High consequence/irreplaceable or safety-relevant data:** stronger administrative/provider/evidence independence, explicit cut-set analysis, destructive drills and potentially offline/multi-party custody after threat analysis.

These are generic decision tiers, not MintTap prescriptions.

## 15. Cross-track transfer

### Track A
A owns DNS/origin/browser/Service Worker mechanics. 127 consumes these to show that central failover and installed-client convergence are different recovery graphs.

### Track B
Recovery UI/content should expose partial/degraded states: origin restored, sync unavailable, client stale, reconciliation required, historical evidence uncertain. Do not collapse these into `online`.

### Track C
Owns destructive common-mode tests and must record both successful recovery and claims disproved by the drill.

### Track D
Analytics/search telemetry is not an independent denominator if it shares the failed provider/account. Historical gaps must remain explicit.

## 16. Cross-repository boundary

Design Studio evidence remains a consumer/transfer source for recovery/degraded-state communication; it does not prove provider independence. The latest Web Manager canonical record marks Web Design Stage 3 PRACTICE / NOT PASSED, W077, with cross-browser/device/human evidence still open.

Concrete provider topology, credential separation, backup export/rebuild tooling and destructive automation belong to Software Engineering/project implementation when available. No implementation evidence is promoted into this generic gate.

Marketing evidence does not change the recovery dependency boundary; public availability claims must not exceed operational evidence.

## 17. SOURCE / SYNTHESIS / CHANGE WATCH boundary

Primary/current sources used:
- NIST SP 800-34 Rev.1 contingency planning and alternate processing separation;
- NIST SP 800-161 Rev.1 Update 1 C-SCRM;
- NIST SP 1326 (published 2026-07-08) supplier due-diligence framework emphasizing provenance, resilience and supply-chain tiers;
- NIST contingency-planning topic material.

These sources support generic resilience/dependency principles. They do not establish any actual MintTap provider topology, provider SLA, upstream dependency, account-recovery feature or managed-iPad behavior.

**CHANGE WATCH:** provider ownership/upstream infrastructure, account/tenant recovery, export/backup, control-plane behavior, browser/WebKit/MDM capabilities and provider terms can change.

## 18. PASS gate

Generic PASS requires ability to:
- model recovery as an end-to-end dependency graph;
- distinguish redundancy from scenario-specific independence;
- identify identity/person/device/provider/toolchain common modes;
- reason about small recovery-path cut sets;
- separate central provider recovery from installed-PWA recovery;
- choose bounded manual recovery when it is more proportionate than active-active duplication;
- define provider due-diligence questions and destructive common-mode drills;
- preserve unknown dependency facts as OPEN.

**Gate result: PASS (generic).** Product/provider/managed-iPad/runtime validation remains OPEN.

## 19. Adjacent high-value question completed before stop

A dependency graph can become stale even when every listed recovery path once passed. New SSO federation, repository migration, CDN consolidation, billing-account changes, CI centralization or administrator turnover can silently introduce a new common-mode cut set. Therefore dependency assurance requires **change-triggered re-evaluation**, not only annual documentation review. Material provider/identity/domain/CI/key-custody changes should invalidate affected independence claims until re-checked.

Guards:
- `recovery drill passed once ≠ dependency graph still current`;
- `provider migration completed ≠ recovery independence preserved`;
- `new convenience SSO ≠ harmless to recovery separation`.

## Next high-value target

**PWA recovery dependency drift & resilience-budget governance** — maintain dependency-graph freshness as providers/SSO/CI/domain/key custody evolve; define which new shared dependencies consume an intentional resilience budget, which require mitigation, and how to avoid both silent concentration and unjustified multi-provider complexity.