# 126 — PWA Assurance Recovery Authority & Provenance After Organizational Loss

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 103–125 recovery/organizational-survivability/assurance chain; Track A PWA authority boundaries; Track C destructive organizational-loss drills; Software Engineering for concrete provider/bootstrap implementation.

## Purpose

125 established conservative recovery when evidence survives but verifier context is lost. 126 addresses the harder common-mode failure: the people, administrator accounts, cloud tenant, repository, provider identity, domain-control path, or organizational records that authenticated the recovery context are themselves unavailable or compromised.

The central problem is bootstrap circularity. A replacement environment cannot prove its own authority merely by being the environment that was successfully rebuilt. Recovery authority must derive from surviving provenance that is sufficiently independent of the failed authority domain, or the claim must remain explicitly uncertain.

Central rule:

> **Recovery restores authority only from surviving, independently attributable authority/provenance; replacement infrastructure, possession, successful login, or operational continuity cannot manufacture the missing organizational trust root.**

## 1. Five-track balance and allocation

- **A Platform/Browser — dependency supplier:** maps origin/domain/TLS/Service Worker/client-generation boundaries. A recovered origin does not establish installed-PWA or historical organizational authority.
- **B UX/IA/Content — consumer:** recovery and degraded-trust states must distinguish service availability, local record availability, current remote authority, and unresolved organizational provenance.
- **C Quality — high dependency pressure:** owns destructive drills in which original administrators/providers/tenant/repository are unavailable, plus negative tests against circular bootstrap.
- **D Search/Analytics — consumer:** recovered analytics/search surfaces cannot silently redefine historical denominators, incident windows or ownership provenance.
- **E Architecture/Security/Operations — highest-risk owner:** owns bootstrap authority, succession, alternate failure domains, provider recovery, reconstitution and residual uncertainty.

Allocation remains intentionally E-heavy. Track A and C are the highest-value dependencies; B/D consume the resulting state model rather than duplicating security foundations.

## 2. SOURCE — contingency planning is organizational, not merely backup restoration

NIST describes contingency planning as coordinated plans, procedures and technical measures for recovering systems, operations and data after disruption. NIST SP 800-53 CP-2 requires contingency plans to identify essential functions, recovery objectives, roles/responsibilities and assigned individuals, maintain essential functions despite disruption/compromise/failure, and support eventual restoration without deterioration of planned safeguards. CP-7 additionally treats alternate processing capability and separation from common threats as explicit concerns.

Sources checked 2026-09-18:
- https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** organizational recovery is not proven by `backup restored`. Personnel authority, provider access, trust provenance, processing capability and security controls can fail together.

Guards:
- `data backup survived ≠ recovery authority survived`;
- `system rebuilt ≠ organization re-authorized`;
- `service reachable ≠ recovered service trustworthy`.

## 3. SOURCE — alternate capability must reduce common-mode failure

SP 800-53 CP-7(1) requires alternate processing sites to be sufficiently separated from the primary site to reduce susceptibility to the same threats; CP-7 also addresses accessibility and preparation. The principle is risk-based separation rather than merely making another copy.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** a second cloud account controlled by the same compromised SSO, same recovery mailbox and same administrators is not automatically an independent recovery authority. Likewise, a repository mirror whose credentials derive from the same failed identity plane may add availability but little bootstrap independence.

Guards:
- `second account ≠ second authority domain`;
- `second provider copy ≠ independent recovery provenance`;
- `geographic separation ≠ identity/control-plane separation`.

## 4. SOURCE — account recovery and identity proofing are different from authorization

NIST SP 800-63B-4 (final July 2025) governs authenticator management; SP 800-63A-4 governs identity proofing. NIST defines account recovery as regaining ownership of a subscriber account and its associated information/privileges. Authentication establishes confidence in a claimant/subscriber relationship; application authorization remains a separate decision.

Sources:
- https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- https://csrc.nist.gov/pubs/sp/800/63/a/4/final
- https://csrc.nist.gov/glossary/term/account_recovery

**SYNTHESIS:** provider account recovery can restore control of a provider account, but that fact alone does not prove every historical organizational role, signing authority, deployment authorization or data-provenance claim that depended on the lost environment.

Guards:
- `provider account recovered ≠ all historical authority recovered`;
- `identity re-proved ≠ old authorization graph reconstructed`;
- `new administrator authenticated ≠ new administrator inherits every old privilege`.

## 5. Bootstrap-authority source classes

Potential sources should be evaluated by provenance and common-mode independence, not by convenience:

1. **Pre-disaster organizational authority records** — approved role/succession records, recovery contacts, sealed/offline recovery instructions or comparable records whose provenance survived.
2. **Independent identity/recovery channel** — a provider recovery process capable of re-establishing an accountable organizational identity without depending solely on the failed tenant/session.
3. **Independent cryptographic/provenance material** — retained trust anchors, verification keys, signed manifests, protected evidence sinks or recovery packages already bound to the pre-disaster organization.
4. **Independent infrastructure control evidence** — domain/registrar/provider control recovered through a separately governed path.
5. **Multiple bounded witnesses** — useful to corroborate facts when no single witness is authoritative; agreement does not automatically recreate a missing root of authority.
6. **Current operator assertion** — contextual evidence only when it is not independently anchored.

No item is universally required. Consequence determines the assurance level.

Guard: `possession of surviving artifact ≠ authority to redefine its meaning`.

## 6. Recovery authority is capability-scoped

A recovered actor may be authorized to perform one recovery action without receiving universal production authority. Useful capability separation includes:
- read historical evidence;
- decrypt a recovery package;
- verify historical signatures;
- recover provider/tenant access;
- restore DNS/origin service;
- publish a recovery build;
- rotate credentials;
- re-enable ordinary remote writes;
- authorize destructive mutation;
- reconcile compromise-era queued operations.

**MINTTAP DIRECTION:** bootstrap authority should be least-privilege and staged where consequence warrants it. Exact roles are OPEN.

Guards:
- `authority to recover ≠ authority to operate indefinitely`;
- `authority to decrypt backup ≠ authority to publish production`;
- `authority to restore origin ≠ authority to accept stale client writes`.

## 7. Avoid circular recovery

Circular patterns that do not independently establish authority include:
- the new tenant declares itself successor because it contains a copied configuration;
- a new signing key signs a statement saying it is the historical key's successor without a surviving predecessor binding;
- a restored repository contains a file naming the current operator as recovery owner, but repository provenance itself is the disputed fact;
- a compromised mailbox receives the recovery link that is then used to prove the mailbox was trustworthy;
- the rebuilt origin serves a manifest claiming the rebuilt origin is authoritative;
- a stale PWA self-reports that its cached trust state should bootstrap the new server.

Guards:
- `replacement environment self-attests ≠ bootstrap provenance established`;
- `new key signs succession claim ≠ predecessor authorized succession`;
- `restored repository says owner X ≠ repository provenance independently verified`.

## 8. Succession without the original person

A resilient recovery model must not require one irreplaceable individual forever. Conversely, the absence of that person does not justify granting whoever remains universal access.

Generic pattern:
1. predefine role-based rather than person-only recovery responsibility where practical;
2. preserve an independent record of succession/recovery policy;
3. require enough surviving authority factors/witnesses for the consequence level;
4. issue new bounded recovery credentials rather than revive departed/lost credentials;
5. record the transition and retire emergency authority after normalization;
6. preserve unresolved historical claims as uncertainty rather than filling gaps from memory.

This is governance direction, not a prescription for quorum size or legal corporate authority. Actual MintTap ownership, staffing and succession facts are OPEN.

Guards:
- `single founder unavailable ≠ recovery impossible by definition`;
- `remaining operator available ≠ universal successor by default`.

## 9. Emergency/break-glass authority remains temporary

SP 800-53 account-management guidance treats emergency and temporary accounts as short-term mechanisms and includes automatic removal/disablement after an organization-defined period. 118 already established that emergency privilege and containment deny controls have different expiry semantics.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** organizational-loss recovery may require emergency authority, but bootstrap success should create a new normal authority graph rather than leave recovery credentials as permanent hidden superuser access.

Guards:
- `break-glass used successfully ≠ break-glass becomes normal administration`;
- `recovery complete ≠ emergency credential safely retained active`.

## 10. Recovery of domain/origin does not recover installed PWA state

Track A transfer:
- control of DNS/hosting/origin can be re-established centrally;
- installed PWAs may remain offline with old Service Workers, caches, local data, sessions and queued operations;
- a clean origin cannot retroactively prove what an offline client executed during the organizational-loss interval;
- reconnect can be used as a re-entry boundary under current server-side trust/API/reconciliation policy.

Therefore:
- `domain recovered ≠ installed PWA recovered`;
- `clean origin online ≠ offline fleet converged`;
- `new Service Worker published ≠ stale client fetched/activated it`;
- `organizational authority recovered ≠ compromise-era outbox authorized`.

## 11. EFB / LogMate-like consequence model

For a company iPad that may remain offline while central organizational authority is being rebuilt:
- preserve local flight records independently of central availability where product/legal policy allows;
- do not require the offline PWA to continuously prove organizational liveness;
- do not let cached client trust bootstrap replacement server authority;
- on reconnect, separate local read/export/recovery from remote mutation;
- require current server-side re-entry and reconciliation before accepting stale queued writes;
- retain explicit provenance uncertainty for records created during an unresolved authority interval.

Exact aviation/legal requirements, WebKit/MDM behavior, local-authoritative-data model and sync implementation remain OPEN.

## 12. Provider-recovery boundary

A provider may offer its own account/tenant recovery procedure. That is evidence about provider account control under the provider's rules, not automatically evidence about:
- historical application signing keys;
- prior deployment approvals;
- corporate/legal succession;
- old data authorship;
- offline-client state;
- compromise-era operation intent.

**MINTTAP DIRECTION:** record which claim each provider recovery step actually establishes. Do not promote provider support success into universal organizational trust.

Guard: `support ticket resolved ≠ historical provenance restored`.

## 13. Minimum recovery-provenance record

For consequential recovery, preserve at least the applicable subset of:
- recovery event/incident identity;
- failed authority domains and suspected common mode;
- surviving authority/provenance sources;
- source independence rationale;
- actor/role and authentication/proofing path;
- capability granted and explicit exclusions;
- keys/accounts/tenants/domains/repositories restored or replaced;
- predecessor/successor bindings that are verified vs unknown;
- emergency credentials and retirement condition;
- PWA/origin/client generations affected;
- data/outbox trust state;
- independent verifier/challenge results;
- unresolved historical claims;
- normalization and review evidence.

This record authenticates the recovery decision only to the strength of its own provenance; it does not repair missing predecessor evidence.

## 14. Track C destructive organizational-loss campaign

Future implementation validation should include at least:
1. primary administrator unavailable;
2. primary authenticator set lost;
3. primary SSO tenant inaccessible;
4. recovery mailbox compromised;
5. repository inaccessible while provider account survives;
6. provider account inaccessible while independent repository/evidence archive survives;
7. DNS/registrar access lost;
8. origin provider lost while domain control survives;
9. same SSO controls both primary and supposed alternate provider;
10. independently governed alternate recovery path succeeds;
11. new key attempts unsigned/unbound predecessor succession and is rejected;
12. restored repository attempts self-authentication and is rejected;
13. recovery actor receives read-only historical-verifier capability only;
14. separate actor/process authorizes production publication where required;
15. emergency account expires/retires after normalization;
16. stale emergency credential cannot operate later;
17. recovered domain serves clean origin while offline PWA remains stale;
18. stale PWA cannot bootstrap replacement server trust;
19. returning client passes current re-entry gate but old outbox remains quarantined;
20. local read/export survives central authority outage where designed;
21. two nominal backup accounts share one common-mode identity failure and test detects non-independence;
22. conflicting recovery witnesses produce explicit uncertainty rather than majority-by-convenience;
23. provider support recovery restores account but does not promote historical signing claim;
24. historical evidence remains `UNVERIFIABLE` when predecessor binding is absent;
25. recovery package records unsupported claims explicitly;
26. destructive drill can proceed without the original individual;
27. drill cannot proceed when the required independent provenance was intentionally removed;
28. dashboard does not report recovered/green solely because service is reachable;
29. negative canary proves old credentials/client generation remain denied;
30. post-recovery review proves break-glass authority is gone.

## 15. Assurance tiering — avoid enterprise PKI/escrow by default

Not every app-company website requires elaborate offline quorum, HSM escrow or public transparency infrastructure. Scale controls to consequence:

- **Low consequence:** independently protected recovery codes/authenticators + documented provider recovery + tested restore may be sufficient.
- **Moderate consequence:** separate administrative/recovery identities, protected recovery records, role succession, provider/domain separation and destructive drills may be warranted.
- **High consequence / irreplaceable or safety-relevant data:** stronger independent custody, multi-party or offline authority, dedicated cryptographic recovery and formal exercises may be justified after explicit threat/consequence analysis.

These are decision tiers, not MintTap production prescriptions.

Guard: `organizational survivability required ≠ enterprise PKI required`.

## 16. Cross-repository transfer

### Design Studio
Canonical Web Design status checked 2026-09-18: **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**, W077. Its before/after semantic/focus/scroll/geometry/accessibility provenance reinforces the value of explicit runtime identity, but provides no organizational-recovery authority evidence. Cross-browser/Safari/Firefox, non-drag reorder, persistence, screen-reader, physical-device, field-CWV and human UX remain OPEN.

### Software Engineering
Concrete tenant/provider recovery automation, credential isolation, key custody, recovery package tooling and destructive tests belong with Software Engineering when implementation exists. No implementation evidence is promoted here. Current Web Manager canonical evidence records Software Engineering as Foundation IN STUDY.

### Marketing
No marketing evidence changes the security/authority boundary; public recovery/trust messaging must not claim stronger continuity than operational evidence supports.

## 17. SOURCE/SYNTHESIS boundary and CHANGE WATCH

Primary standards used:
- NIST SP 800-53 Rev.5 current release information and CP/AC control model;
- NIST contingency-planning guidance;
- NIST SP 800-63A-4 and 800-63B-4 final publications (July 2025).

These sources establish general control/identity principles. They do **not** establish MintTap's provider recovery features, staffing, legal succession, actual domain ownership, MDM policy or production architecture.

**CHANGE WATCH:** provider-specific account/tenant/domain recovery procedures are operationally changeable and must be verified from the actual selected providers before project decisions.

## 18. PASS gate

Generic PASS requires ability to:
- distinguish system/data restoration from organizational-authority recovery;
- identify circular bootstrap and common-mode identity/control-plane failure;
- evaluate recovery sources by provenance and independence;
- separate identity/account recovery from application authorization and historical provenance;
- scope recovery authority by capability and retire emergency authority;
- preserve explicit uncertainty when predecessor/succession evidence is missing;
- separate recovered origin from installed-PWA/fleet recovery;
- apply fail-closed reconnect/reconciliation to long-offline EFB-like clients;
- specify destructive organizational-loss tests;
- scale assurance to consequence rather than prescribing enterprise PKI by default.

**Gate result: PASS (generic).** Product/provider/organizational/legal/managed-iPad runtime validation remains OPEN.

## 19. Adjacent high-value question completed before stop

The next adjacent question is whether successful bootstrap is enough to declare the replacement authority normal. Answer: no. Bootstrap establishes bounded recovery authority; normalization requires a newly documented authority graph, retirement of emergency credentials, current negative authorization probes, provider/domain/repository inventory reconciliation, and explicit treatment of unresolved predecessor claims. This is incorporated here rather than split into a micro-study.

## Next high-value target

**PWA recovery-of-recovery dependency assurance / correlated provider failure:** determine how to map and test hidden shared dependencies across identity provider, registrar/DNS, source repository, CI/CD, hosting/CDN, evidence sink, recovery mailbox/device and key custody so that nominally independent recovery paths do not collapse under one SSO/provider/person/device failure. Keep the analysis consequence-based and avoid demanding full multi-provider duplication where bounded manual recovery is sufficient.