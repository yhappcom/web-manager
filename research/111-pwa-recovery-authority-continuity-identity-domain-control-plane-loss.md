# 111 — PWA Recovery Authority Continuity Under Identity, Domain & Control-Plane Loss

Status: **PASS (generic) / PRODUCT AUTHORITY-TOPOLOGY + EMERGENCY-DRILL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 093 offline authorization/session boundaries; 099 trust-policy authenticity/anti-rollback; 100 trusted-state reset/rebootstrap; 101 mixed-epoch recovery; 105 release/change governance; 106 retirement; 108 provenance; 110 custody/organizational survivability; Track A DNS/TLS/browser trust mechanics; Track C recovery drills; Software Engineering exact IAM/key/provider implementation.

## Purpose

110 established that recovery knowledge must survive loss of the ordinary repository/cloud/SSO/control plane. That still leaves a harder problem: **who is authorized to rebuild control after the identity system, domain account, DNS authority, signing/trust authority or ordinary administrative plane is unavailable or suspected compromised?**

A recovery path that depends entirely on the failed authority cannot recover. A permanent super-admin credential that bypasses the failed authority can recover, but also creates a standing path that defeats ordinary least privilege and anti-rollback. This study defines a generic authority-continuity model between those extremes.

This is not a MintTap/LogMate provider design. Exact registrar, DNS host, IdP, cloud tenant, certificate, signing key, passkey, recovery contact, legal ownership evidence and personnel are OPEN until product evidence exists.

## 1. Track balance

- **A Platform/Browser:** supplies DNS, TLS, origin, certificate and browser trust mechanics. Browser acceptance of a domain/TLS endpoint does not establish organizational recovery legitimacy.
- **B UX/IA/Content:** consumes truthful states such as identity unavailable, ownership verification pending, emergency authority active, trust re-established, local-only/quarantine and replay blocked.
- **C Quality:** owns destructive-failure drills, stale-authority rejection, notification/audit evidence, recovery-path expiry and post-recovery containment tests.
- **D Discovery/Analytics:** domain/control-plane incidents affect search, links and acquisition, but public recovery telemetry must not disclose recovery factors or emergency authority state in exploitable detail.
- **E Architecture/Security/Operations:** highest-risk owner; owns authority graph, recovery eligibility, emergency privilege lifecycle, trust-root transition and provider/domain recovery runbooks.

E remains the bottleneck. A is a prerequisite supplier because domain/TLS/DNS are part of the web trust path, not proof of organizational identity.

## 2. SOURCE — account recovery is not ordinary authentication

NIST SP 800-63B-4 distinguishes account recovery from ordinary authentication. Recovery is invoked when required authenticators are lost and can use saved/issued recovery codes, recovery contacts or repeated identity proofing. Recovery causes notification, and alternative application-specific recovery methods are to be risk-analyzed and documented.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/events/
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/
- https://www.nist.gov/publications/nist-sp-800-63-4-digital-identity-guidelines

**TRANSFER VALIDATION:** organizational control-plane recovery is not identical to subscriber account recovery, but the distinction is valuable: a recovery ceremony is a separate high-risk state transition, not merely a weaker login form.

**SYNTHESIS:** do not model `emergency login` as an ordinary administrator session with a special password. Model recovery as an explicit authority transition with separate eligibility evidence, restricted powers, notification/audit, expiry and post-recovery re-binding.

Guards:
- `recovery succeeded ≠ ordinary authentication occurred`;
- `possession of one recovery factor ≠ full organizational authority proven`;
- `can regain account access ≠ may rotate every trust root immediately`;
- `emergency authority available ≠ emergency authority should be continuously active`.

## 3. SOURCE — emergency accounts are exceptional and short-lived

NIST SP 800-53 Rev. 5 describes emergency accounts as crisis-response accounts that may bypass normal account-authorization processes because rapid activation is needed. It separately calls for automated removal/disablement of temporary and emergency accounts after an organization-defined period. Least privilege restricts entities to the minimum resources and authorizations necessary.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/glossary/term/least_privilege

**SYNTHESIS:** an emergency recovery capability may need a different activation path from ordinary SSO, but that does not justify permanent unrestricted privilege.

**MINTTAP DIRECTION:** when exact systems exist, separate at least:
1. recovery eligibility/identity evidence;
2. emergency activation authority;
3. provider/domain ownership recovery;
4. trust/key rotation authority;
5. data recovery/reconstruction authority;
6. destructive retirement authority.

Do not collapse them into one `break-glass admin` unless exact risk analysis proves that unavoidable.

Guards:
- `break-glass exists ≠ standing super-admin justified`;
- `normal SSO unavailable ≠ all authorization controls may be bypassed`;
- `emergency privilege activated ≠ privilege should survive incident closure`;
- `account of last resort ≠ ordinary daily admin account`.

## 4. Authority continuity is a graph, not one root credential

Model recovery dependencies explicitly. A generic authority graph can include:

- legal/organizational ownership evidence;
- human recovery roles;
- primary IdP/SSO;
- alternate authentication/recovery factors;
- registrar account and registry procedures;
- DNS hosting/control;
- cloud/hosting control plane;
- source/build/deployment authority;
- certificate/TLS automation;
- release signing/trust-policy verification;
- backup/escrow custody;
- billing/contact/recovery channels;
- notification/audit channels.

For each edge ask: **if node X is compromised or unavailable, can X itself authorize the only recovery path for X?** If yes, the path may be circular.

Examples of weak cycles:
- registrar password reset goes only to email hosted on the lost domain;
- cloud recovery email depends on the same corporate IdP that is unavailable;
- escrow access requires the same GitHub organization that escrow is meant to survive;
- new trust-policy key can be authorized only by the compromised old key;
- emergency administrator can silently rewrite the audit destination it is meant to notify.

**MINTTAP DIRECTION:** maintain an authority/failure graph in addition to 110's failure-domain matrix.

Guards:
- `documented recovery path ≠ non-circular recovery path`;
- `separate account name ≠ separate recovery authority`;
- `different factor ≠ independent factor if both recover through the same compromised channel`.

## 5. Domain ownership is a security authority, not branding metadata

A domain registrar compromise can change registration or delegation and redirect users. Current domain-owner guidance recommends MFA, registrar/client locking, registry locking where justified, current contact details and rapid registrar/registry escalation after hijacking. Registry-level locking can add an out-of-band authorization layer beyond ordinary registrar-account changes.

Sources:
- https://www.cyber.gov.au/business-government/protecting-devices-systems/hardening-systems-applications/network-hardening/domain-name-system-security-for-domain-owners
- https://www.ncsc.gov.uk/collection/security-practice-domain-registrars/make-strong-security-available
- https://www.icann.org/resources/pages/lost-domain-names

**SYNTHESIS:** recovery planning must distinguish:
1. DNS host compromise;
2. registrar-account compromise;
3. registrant/ownership dispute or account loss;
4. registry-level restriction/recovery;
5. expiration/billing failure;
6. domain irrecoverability.

Changing DNS at a hosting provider does not recover a lost registrar account. Recovering a registrar account does not prove that previously served code, sessions or trust state remained uncompromised.

Guards:
- `DNS restored ≠ registrar ownership restored`;
- `registrar access restored ≠ prior DNS answers trustworthy`;
- `domain resolves correctly now ≠ clients were never exposed to hostile origin content`;
- `domain possession ≠ release-signing authority`;
- `domain recovery ≠ session/token recovery`.

## 6. DNSSEC illustrates trust-anchor continuity and its hard limit

RFC 5011 defines automated, authenticated and authorized DNSSEC trust-anchor updates using an already trusted anchor. It explicitly does not solve initial trust-anchor configuration, and if all trust-anchor keys at a trust point are compromised, manual or other out-of-band update is required. RFC 4986 separately recognizes emergency/non-scheduled trust-anchor rollover and revocation.

Sources:
- https://www.rfc-editor.org/rfc/rfc5011
- https://www.rfc-editor.org/rfc/rfc4986

**TRANSFER VALIDATION:** PWA/application trust-policy signing is not DNSSEC, but the security principle transfers: an in-band rollover mechanism can preserve continuity while at least one accepted trust root remains trustworthy; total root compromise requires an independently governed rebootstrap path.

Guards:
- `old root can sign new root ≠ safe recovery if old root is compromised`;
- `automated rollover works normally ≠ total-root-compromise recovery solved`;
- `out-of-band recovery required ≠ any out-of-band assertion should be trusted`.

## 7. Recovery must preserve anti-rollback

A dangerous recovery design restores availability by accepting any historically valid credential, key, policy or backup. That can revive authority deliberately revoked before the incident.

Generic recovery inputs therefore need freshness/epoch context such as:
- last known accepted trust generation;
- revoked/retired key identifiers;
- schema/protocol generation;
- account/device revocation state;
- custody/provenance evidence;
- recovery event identity;
- explicit replacement generation.

**MINTTAP DIRECTION:** emergency rebootstrap may establish a *new* trust generation, but should not silently reset the system to `trust generation 0` or resurrect old credentials merely because they are present in escrow.

Guards:
- `historically authentic ≠ currently authorized`;
- `old key available ≠ old key may be reactivated`;
- `backup predates compromise ≠ backup contains current revocation state`;
- `emergency reset ≠ anti-rollback reset`.

## 8. Separate identity proof from authorization scope

NIST SP 800-63A-4 defines identity proofing as evidence-based establishment that an applicant corresponds to a real-world identity. NIST SP 800-63C-4 defines federation between separately administered parties. Neither implies that proving a person's identity grants every organizational privilege.

Sources:
- https://www.nist.gov/publications/nist-sp-800-63a-4digital-identity-guidelines-identity-proofing-and-enrollment
- https://www.nist.gov/publications/nist-sp-800-63c-4digital-identity-guidelines-federation-and-assertions

**SYNTHESIS:** during organizational recovery, distinguish:
- **who is this person/entity?**
- **does this person currently represent the organization?**
- **which recovery action may they perform?**
- **what independent evidence/provider process supports that authority?**
- **when does that authority expire?**

A former employee can still prove their identity. That does not make their former organizational authority current.

Guards:
- `human identity proven ≠ current organizational role proven`;
- `organizational role proven ≠ unrestricted technical authority`;
- `provider support accepted claimant ≠ every downstream trust root should accept claimant automatically`.

## 9. Recovery ceremony should be staged, not atomic

A generic high-assurance sequence is:

1. **declare incident scope** — unavailable vs suspected compromised nodes;
2. **freeze dangerous automation** where possible — deployment, key rotation, destructive cleanup, blind sync replay;
3. **preserve evidence** — logs, current DNS/registrar state, artifact identities, escrow generations, local user data;
4. **establish recovery claimant/organizational authority** through surviving independent evidence;
5. **recover the narrowest control plane first** — enough to inspect and contain, not immediately enough to rewrite everything;
6. **establish a new authority generation** for compromised identity/signing/trust components;
7. **invalidate/contain old authority** according to provider/system capabilities;
8. **restore domain/DNS/TLS/deployment paths** with explicit provenance;
9. **reconcile stale/offline clients and data** using 101/106 rules;
10. **notify/audit** recovery events through surviving channels;
11. **expire emergency authority** and re-bind ordinary least-privilege identities;
12. **post-recovery drill/review** hidden dependencies and unauthorized persistence.

This sequence is conceptual. Exact order can change when a provider imposes dependencies.

Guards:
- `control regained ≠ compromise eradicated`;
- `new admin created ≠ old admin/session/token invalidated`;
- `new signing key active ≠ old signatures/clients safely retired`;
- `website serving again ≠ offline clients safe to replay`.

## 10. PWA-specific consequence: domain/control recovery does not repair installed state

An installed PWA may retain Service Worker, Cache Storage, IndexedDB, local records, sessions and trust metadata across a server-side incident. A recovered origin can therefore meet clients holding different generations of code/data/trust.

Generic rule:

`origin recovery → client generation classification → trust revalidation → safe update/migration → local-data preservation → reconciliation → replay authorization`.

Do not assume a recovered domain can force every long-offline client to update immediately. Do not erase local authoritative records merely because their client generation is unsupported.

Guards:
- `origin recovered ≠ installed PWA recovered`;
- `TLS valid again ≠ cached worker/data trustworthy`;
- `network reachable ≠ stale client authorized to replay`;
- `unsupported client ≠ local records should be destroyed`.

## 11. Recovery notifications and audit are part of authority assurance

NIST SP 800-63B-4 requires account-recovery notifications and notification for important authenticator events. SP 800-53/PAM guidance emphasizes monitoring privileged-account use.

**TRANSFER VALIDATION:** organizational recovery should produce independently reviewable evidence of activation, actions, new authority generation and closure. Where practical, at least one notification/audit path should not be writable solely by the same emergency authority being observed.

Do not log recovery secrets, private keys, recovery codes or sensitive user data.

Guards:
- `recovery action logged locally ≠ independent audit evidence preserved`;
- `notification sent through compromised domain ≠ recipient necessarily received trustworthy notice`;
- `more recovery logging ≠ more assurance if logs expose recovery factors`.

## 12. Provider support is a dependency, not an invisible root of trust

Registrar, registry, cloud, source-control and identity providers each have their own account-recovery and ownership-verification procedures. They can be essential when internal credentials are lost, but provider support introduces policy, personnel and evidence dependencies outside application code.

**MINTTAP DIRECTION:** for each critical provider record:
- ownership evidence required;
- supported recovery contacts/channels;
- whether those contacts depend on the lost domain/IdP;
- lock/hold/manual-review behavior;
- expected restrictions on high-risk changes;
- how compromise is reported;
- what audit/case evidence is retained;
- what cannot be recovered by support.

Do not invent a provider recovery SLA or assume a support agent can restore a domain/account.

Guard: `provider has support ≠ provider can restore every lost authority`.

## 13. Emergency authority must have an exit path

Recovery is incomplete until exceptional authority is removed or reduced. Closure should consider:
- disable/remove temporary emergency accounts;
- rotate temporary authenticators/secrets;
- revoke superseded sessions/tokens/API keys;
- replace compromised recovery contacts;
- re-establish normal SSO/role assignments;
- review registrar/DNS/cloud/build/signing privileges;
- bind the new trust generation into normal update policy;
- review audit evidence;
- update 110 failure-domain and 111 authority graphs;
- rerun recovery drills after material changes.

Guard: `incident closed ≠ emergency privilege automatically disappeared`.

## 14. Track C validation campaign

Exact-product validation should include at least:
1. draw the complete authority/recovery graph;
2. identify circular recovery dependencies;
3. simulate primary IdP unavailable but not compromised;
4. simulate primary IdP compromised;
5. simulate registrar account unavailable;
6. simulate registrar account compromised with malicious DNS change;
7. simulate DNS host compromise without registrar loss;
8. simulate source-control/cloud control-plane loss;
9. simulate release/trust signing-key compromise;
10. prove recovery claimant identity does not automatically grant unrestricted scope;
11. prove emergency authority has bounded actions and lifecycle;
12. prove emergency activation and closure are auditable;
13. prove recovery notifications through an alternate channel where product policy requires it;
14. prove old sessions/tokens/admin paths are invalidated or explicitly quarantined;
15. prove historical revoked trust/key generations cannot be reintroduced by stale backup;
16. prove new trust generation is accepted through a documented rebootstrap ceremony;
17. prove long-offline PWA local records survive while replay remains blocked until trust/reconciliation pass;
18. prove domain/DNS restoration does not count as installed-client convergence;
19. prove emergency authority can be disabled after normal least-privilege administration returns;
20. repeat with a successor operator rather than the original designer.

No generic quorum, timeout, RTO, number of recovery factors or provider choice is set here. Those require product risk and provider evidence.

## 15. Design Studio transfer

Canonical Design Studio `progress/WEB_STATUS.md` checked 2026-09-18: Web Design remains **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. W062 implements a MintTap CI bridge, but its first artifact-bearing execution remains OPEN. No Safari/WebKit, screen-reader, physical-device, field-CWV or human UX PASS transfers.

**DEPENDENCY:** Web Manager supplies truthful security/recovery states and action restrictions. Design Studio owns reusable interaction evidence for emergency/offline/recovery UX once executable product evidence exists.

## 16. Software Engineering transfer

Canonical Software Engineering Studio `progress/STATUS.md` checked 2026-09-18: all specialists remain **Foundation IN STUDY**. Existing data/quality/systems evidence supports invariant, failure-generation, artifact/provenance and reconciliation methods, but no exact MintTap/LogMate IAM, registrar, DNS, signing, trust-rebootstrap or emergency-account implementation transfers.

**DEPENDENCY:** Software Engineering owns exact implementation, executable IAM/key/provider integration and failure harness. Web Manager owns web/PWA authority-continuity requirements and evidence gates.

## 17. EFB/LogMate bounded application

For a LogMate-like managed-iPad PWA holding irreplaceable offline records, organizational control-plane loss must not convert into device-data destruction. A bounded recovery posture is:

`preserve local authoritative records → block trust-sensitive remote replay when authority is uncertain → recover organizational/domain/trust authority independently → establish new trust generation → classify stale client → migrate/update safely → reconcile → authorize replay`.

This does not prove that managed iPad background execution, direct device sync, Files/iCloud access or unattended trust refresh is available. Those remain target-device/MDM CHANGE WATCH and validation items.

MintTap production data criticality and authentication architecture were not inspected; equivalent product controls are not inferred.

## 18. CHANGE WATCH

Re-check when:
- registrar/registry/DNS provider or domain ownership changes;
- IdP/SSO/recovery-contact policy changes;
- NIST SP 800-63 or SP 800-53 guidance materially changes;
- signing/trust/bootstrap design changes;
- DNSSEC/trust-anchor operational standards change;
- a provider changes account/domain recovery procedures;
- emergency drill exposes a circular dependency;
- PWA runtime/managed-device policy changes affect recovery communication.

## 19. Gate

**PASS (generic)** because the study now establishes a source-grounded authority-continuity model across identity recovery, emergency privilege, domain/registrar control, trust-anchor transition, anti-rollback, PWA stale-client containment, audit and post-recovery privilege removal.

**PRODUCT VALIDATION OPEN:** exact authority graph, provider procedures, registrar/DNS/IdP/cloud topology, recovery factors, key/trust generations, emergency privileges, notification/audit independence and target-device recovery behavior.

## 20. Next high-value boundary

The next adjacent bottleneck is **recovery-authority abuse resistance and dual-use incident governance**: distinguish legitimate emergency recovery from an attacker invoking the same process, including recovery-request authentication, social-engineering/provider-support risk, delayed/high-risk actions, independent observation, repudiation/rollback limits and evidence needed before destructive trust-root/domain/account changes. This should deepen 111 rather than create a permanent bypass bureaucracy.