# 112 — PWA Recovery Authority Abuse Resistance & Dual-Use Incident Governance

Status: **PASS (generic) / PRODUCT PROVIDER + RECOVERY-CEREMONY VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 093 offline authorization/session boundaries; 099 trust-policy authenticity/anti-rollback; 100 trusted-state reset/rebootstrap; 101 mixed-epoch recovery; 105 release governance; 110 escrow independence; 111 recovery-authority continuity; Track A domain/TLS/origin mechanics; Track C adversarial drills; Software Engineering exact IAM/provider implementation.

## Purpose

111 established how legitimate organizational authority can be rebuilt after identity, domain, signing or control-plane loss. The adjacent security problem is dual use: **the same exceptional process that saves the organization can be invoked by an attacker who impersonates the owner, compromises a recovery factor, manipulates provider support, or abuses emergency privilege.**

Recovery therefore needs abuse resistance, not merely availability. This study defines generic controls and evidence boundaries. It does not prescribe MintTap's registrar, IdP, quorum, delay, recovery factors or provider workflow; those remain OPEN until exact product/provider evidence exists.

## 1. Track balance

- **A Platform/Browser:** supplies domain/DNS/TLS/origin mechanics. A browser accepting a recovered HTTPS origin does not prove the recovery ceremony was legitimate.
- **B UX/IA/Content:** consumes truthful high-risk states: recovery requested, independently reviewing, restricted recovery mode, change pending, disputed/repudiated, trust re-established, replay blocked.
- **C Quality:** owns adversarial recovery-request, notification, cancellation, stale-factor, provider-support and post-recovery persistence drills.
- **D Discovery/Analytics:** domain takeover can alter search/acquisition surfaces; telemetry must not expose recovery factors, timing windows or exploitable emergency state.
- **E Architecture/Security/Operations:** highest-risk owner; owns recovery ceremony, authority separation, high-risk action staging, independent observation, containment and repudiation response.

E remains the bottleneck. A remains a dependency supplier; C has high transfer pressure because this topic is only useful when tested against hostile ceremonies rather than happy paths.

## 2. SOURCE — recovery is a known weak point and human assistance creates social-engineering risk

NIST SP 800-63B-4 states that authenticator recovery is a weak point in many authentication mechanisms and explicitly notes social-engineering risk where recovery is human-assisted. It also requires application-specific alternative recovery methods to be risk-analyzed and documented.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/security/
- https://pages.nist.gov/800-63-4/sp800-63b.html#account-recovery
- NIST publication date: 2025-08-01.

**SYNTHESIS:** provider support or a human operator is not an inherently stronger root of trust than automation. Human discretion can resolve cases that automation cannot, but also creates impersonation, urgency, persuasion and procedural-bypass attack paths.

Guards:
- `human-assisted recovery ≠ high-assurance recovery`;
- `support agent accepted claimant ≠ organization independently authorized destructive change`;
- `recovery path available ≠ recovery path abuse-resistant`;
- `more fallback methods ≠ monotonically safer recovery`.

## 3. SOURCE — notification is detection evidence, not authorization

NIST SP 800-63B-4 requires account-recovery notifications and requires clear instructions for repudiating the event. It also requires multiple notification addresses for subscriber accounts under its scope.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/events/
- https://pages.nist.gov/800-63-4/sp800-63b.html#account-notifications

**TRANSFER VALIDATION:** organizational recovery is not subscriber-account recovery, but the security principle transfers: an exceptional authority transition should create evidence visible outside the initiating path and should provide a route to challenge a fraudulent event.

**CONTRADICTION:** notification is not a substitute for pre-action authorization. If an attacker can instantly replace a domain/trust root and only then notify the victim, detection may arrive after irreversible damage.

Guards:
- `notification delivered ≠ action authorized`;
- `notification sent ≠ notification independently observable`;
- `notification after destructive change ≠ preventive control`;
- `repudiation path documented ≠ repudiation can reverse every action`.

## 4. Independent observation must not collapse into the recovery path

A recovery event can be observed through channels that are not controlled solely by the same actor/path performing the change. Examples may include an alternate-domain contact, separately administered audit sink, registrar notification, independent security contact, or offline organizational record. Exact mechanisms are product/provider decisions.

A useful generic property is **non-self-attestation**: the emergency actor should not be the only source asserting that its own activation and high-risk actions were legitimate.

Failure examples:
- registrar recovery and all alerts use email hosted on the hijacked domain;
- emergency admin can silently rewrite the audit destination before rotating trust roots;
- recovery requester can change the recovery phone number and immediately use it to approve the same ceremony;
- provider support ticket is the only retained evidence that support itself followed the required procedure.

Guards:
- `audit record exists ≠ audit record independent of the actor being audited`;
- `different notification address ≠ independent channel if both are controlled by one compromised IdP`;
- `recovery factor updated ≠ newly updated factor should immediately approve the same high-risk recovery`.

## 5. High-risk recovery actions should be staged by reversibility and blast radius

Do not model recovery as one atomic `restore everything` action. Classify actions by consequence:

1. **observe/preserve** — read state, preserve logs/artifacts/local data;
2. **contain** — disable deployment, revoke suspicious sessions, block replay, restrict writes;
3. **recover narrow control** — regain limited provider/domain/IAM inspection authority;
4. **prepare replacement authority** — create candidate key/trust generation or ownership change without broad activation;
5. **activate high-impact change** — DNS delegation, registrar ownership, root/trust/signing replacement, destructive credential invalidation;
6. **reconcile** — classify stale clients/data and authorize safe migration/replay;
7. **retire emergency authority**.

Where provider/product capabilities permit, higher-impact and less-reversible actions deserve stronger evidence than observation/containment. This does not mandate a universal delay, quorum or number of approvers.

Guards:
- `authorized to inspect ≠ authorized to replace trust root`;
- `authorized to contain ≠ authorized to destroy recovery evidence`;
- `recovery claimant verified ≠ every recovery action has equal risk`;
- `speed is valuable during incident ≠ every irreversible step should be immediate`.

## 6. Delay is a security tool only when paired with observation and containment

A cooling-off or hold period can create time for an owner to detect and dispute a fraudulent high-risk request, but delay alone is not security. It can also harm legitimate incident response, especially when an attacker already controls production.

**MINTTAP DIRECTION:** if an exact provider supports holds/locks/manual review, evaluate them per action class:
- can the hold be bypassed by the same compromised factor?
- are independent notifications emitted during the hold?
- can the organization contain ongoing harm while the destructive action remains pending?
- what happens when the incident is active compromise rather than simple credential loss?

No generic hold duration is set.

Guards:
- `waiting period exists ≠ attacker cannot wait`;
- `fast recovery ≠ safe recovery`;
- `slow recovery ≠ safe recovery`;
- `hold protects ownership transfer ≠ hold contains already-compromised sessions/code`.

## 7. Domain recovery demonstrates why provider policy is part of the threat model

NCSC registrar guidance (published 2025-03-27) recommends MFA, revocable API tokens, change notifications and audit logs, and explicitly recommends protecting notification methods and considering an email address on a different domain from the managed domain. ICANN documents registrar/client transfer locks and notes that unauthorized transfer remediation depends materially on registrar procedures; ICANN itself cannot simply return every lost domain.

Sources:
- https://www.ncsc.gov.uk/collection/security-practice-domain-registrars/make-strong-security-available
- https://www.icann.org/resources/pages/locked-2013-05-03-en
- https://www.icann.org/resources/pages/lost-domain-names
- https://www.icann.org/resources/pages/unauthorized-2013-05-03-en

**SYNTHESIS:** provider support is both a recovery dependency and an attack surface. Exact registrar lock, registry lock, ownership evidence, support escalation, transfer policy and notification behavior must be inventoried rather than inferred.

Guards:
- `registrar MFA enabled ≠ support-assisted takeover impossible`;
- `domain locked ≠ all DNS/account changes impossible`;
- `provider support exists ≠ provider can restore every authority`;
- `ICANN policy exists ≠ ICANN can directly reverse every hijack`.

## 8. Recovery factors need independence and lifecycle rules

NIST SP 800-63B-4 requires stronger combinations for higher-assurance account recovery and warns against leveraging one authentication factor to obtain a different factor. NCSC's 2026 messaging-app warning illustrates the operational reality that attackers actively seek login and account-recovery codes through impersonation/social engineering.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b.html#account-recovery
- https://pages.nist.gov/800-63-4/sp800-63b/security/
- https://www.ncsc.gov.uk/news/ncsc-warns-of-messaging-app-targeting

**TRANSFER VALIDATION:** exact MintTap organizational recovery is outside NIST subscriber AAL requirements, but factor independence remains a useful design test.

Examples of false independence:
- two email addresses recovered through the same compromised mailbox/IdP;
- SMS and voice to the same compromised phone account;
- two administrators whose password resets both depend on the same lost domain;
- offline recovery code stored only in the same cloud account it is intended to recover.

Guards:
- `two factors ≠ two independent failure domains`;
- `different delivery channel ≠ independent recovery authority`;
- `factor possession ≠ current organizational role`;
- `old recovery factor historically valid ≠ factor currently authorized`.

## 9. Repudiation has limits; design before irreversible actions

A legitimate owner may challenge a recovery event after receiving an alert. The system should preserve evidence sufficient to determine what was requested, by which asserted claimant, through which provider/path, what was approved, which authority generation changed, and what sessions/clients remained active.

However, repudiation cannot guarantee reversal:
- an attacker may already have exfiltrated secrets/data;
- hostile origin code may already have reached clients;
- an old trust root may have signed malicious artifacts;
- domain transfer may require provider/legal procedures;
- destructive key deletion may make old data unrecoverable.

Therefore the strongest control is often **preventing premature irreversible authority changes**, not promising perfect rollback afterward.

Guards:
- `event repudiated ≠ compromise effects automatically reversed`;
- `control plane restored ≠ exfiltrated secrets recalled`;
- `malicious key revoked ≠ previously delivered hostile artifact disappeared`;
- `audit complete ≠ rollback technically possible`.

## 10. Recovery evidence must bind action, authority generation and artifact identity

A high-risk recovery record should conceptually bind:
- recovery event/case identity;
- asserted claimant and organizational-role evidence class;
- surviving recovery factors/channels used;
- provider/support case or machine-verifiable event reference where available;
- pre-recovery authority generation/state;
- requested action and scope;
- independent observation/notification evidence;
- approvals/holds required by exact policy;
- resulting authority generation;
- keys/artifacts/configuration identities where relevant;
- sessions/tokens/clients contained or still OPEN;
- closure/expiry evidence.

Do not put recovery secrets, private keys, raw identity documents or unnecessary PII into ordinary telemetry.

Guard: `case number exists ≠ exact destructive action and resulting authority are evidenced`.

## 11. PWA-specific consequence: a fraudulent recovery can persist beyond server remediation

If an attacker obtains domain/deployment authority and serves hostile PWA code, affected clients may retain Service Worker, Cache Storage, IndexedDB, sessions or attacker-written trust metadata after server-side ownership is recovered. Conversely, long-offline clients may have missed the hostile interval entirely.

Therefore incident scope cannot be inferred from current origin state alone. Use the 111 sequence:

`origin/control recovery → client generation classification → trust revalidation → safe update/migration → local-data preservation → reconciliation → replay authorization`.

Additional guard: **do not tell every client to wipe local state solely because a control-plane recovery occurred.** Irreplaceable local records may be the only good copy. Quarantine authority and preserve data until provenance/trust/reconciliation determine safe treatment.

Guards:
- `fraudulent recovery reversed at provider ≠ installed hostile state eradicated`;
- `client was offline during incident ≠ client trust state automatically current`;
- `wipe removes hostile cache ≠ wipe is acceptable if it destroys authoritative local records`.

## 12. Dual-use incident governance matrix

For exact implementation, maintain a matrix for each high-risk authority action:

| Action | Legitimate emergency need | Abuse path | Independent evidence | Reversibility | Containment while pending | Closure evidence |
| --- | --- | --- | --- | --- | --- | --- |
| IdP/admin recovery | regain admin control | impersonated owner/support social engineering | OPEN exact provider | varies | restrict privileges/sessions | ordinary role rebound |
| registrar ownership/transfer | recover domain | hijack/unauthorized transfer | OPEN registrar/registry | provider-dependent | lock/hold where supported | ownership + audit verified |
| DNS change | restore routing | redirect users | independent config/audit where available | generally reversible but effects persist | freeze unrelated changes | intended delegation verified |
| signing/trust-root replacement | recover update authority | attacker establishes permanent root | out-of-band authority evidence | difficult after distribution | candidate generation/quarantine | old root contained + new policy bound |
| destructive credential/key retirement | eradicate compromise | attacker causes lockout/data loss | stronger exact-policy evidence | may be irreversible | revoke use before destroy where feasible | recovery/readability proven |
| stale-client replay enablement | restore sync | attacker/stale client replays invalid ops | trust + reconciliation evidence | remote side effects may not roll back | keep replay blocked | acknowledgement/reconciliation complete |

This matrix is a decision framework, not a product configuration.

## 13. Track C adversarial validation campaign

Exact-product/provider validation should include at least:
1. attacker possesses one valid recovery factor but not current organizational role;
2. attacker compromises the primary mailbox and requests registrar recovery;
3. attacker socially engineers provider support with plausible historical information;
4. legitimate recovery occurs while the primary IdP is unavailable;
5. recovery request changes a notification address and immediately tries to use it;
6. independent notification channel is unavailable;
7. victim repudiates before a high-risk action executes;
8. victim repudiates after an irreversible action executes;
9. emergency actor attempts to rewrite/disable its audit destination;
10. emergency actor attempts broader authority than the declared recovery scope;
11. old revoked recovery factor appears in escrow/backup;
12. registrar lock/hold blocks a legitimate emergency action;
13. compromised production remains active while a recovery hold is pending;
14. attacker gains domain/deployment authority and serves hostile Service Worker code;
15. server recovery succeeds but one client retains hostile/stale installed state;
16. long-offline clean client reconnects after the incident;
17. stale client attempts replay before trust/reconciliation passes;
18. recovery closure leaves temporary sessions/tokens/admin privileges active;
19. successor operator executes the ceremony without original designer knowledge;
20. telemetry/audit review proves no recovery secret or unnecessary sensitive identity evidence leaked.

No PASS is inferred until exact provider and target-runtime evidence exists.

## 14. Cross-repository transfer

### Design Studio
Canonical `progress/WEB_STATUS.md` checked 2026-09-18: Web Design remains **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. W063 observed a real MintTap CI run whose analyzer failed before widget/browser stages; the harness was repaired, but the repaired run remains OPEN. Recovery-state UX must not be claimed accessible or cross-browser until product evidence exists.

### Software Engineering Studio
Canonical `progress/STATUS.md` checked 2026-09-18: every specialist remains **Foundation IN STUDY**. Systems S002 supplies a useful least-privilege reasoning chain and executable bounded-authority example, but explicitly does not constitute Android/iOS/Flutter/product security evidence. Web Manager consumes the principle without duplicating implementation research.

## 15. MINTTAP / LogMate-like direction

For a future exact EFB/PWA design:
- keep emergency authority separate from ordinary daily administration;
- inventory registrar, DNS, IdP, hosting, source/build, signing/trust and notification recovery procedures independently;
- treat provider-support recovery as a security-sensitive trust bridge;
- preserve at least one observation/notification route that does not trivially share the failed authority where feasible;
- stage high-impact recovery actions by blast radius/reversibility;
- do not allow a newly changed recovery channel to self-approve the same ceremony without exact risk justification;
- preserve local authoritative records while quarantining stale/uncertain authority;
- bind recovery evidence to authority generations and exact artifacts/configuration;
- remove emergency privilege and review sessions/tokens/recovery contacts after closure.

Exact quorum, factors, delay, provider choice, legal evidence, key ceremony and managed-iPad behavior remain OPEN.

## 16. Durable synthesis

A robust recovery design must answer two different questions:
1. **Can the rightful organization regain authority when ordinary control fails?** — 111 continuity.
2. **Can an attacker use that same exceptional path to become the apparent rightful organization?** — 112 abuse resistance.

Availability-only recovery fails the second question. Security-only refusal to recover fails the first. Expert judgment requires a staged, evidenced authority transition whose exceptional power is independently observable, bounded by action risk, resistant to circular/self-approval, compatible with repudiation where technically possible, and explicitly retired after ordinary authority returns.

Persistent guards added by 112:
- `recovery path available ≠ recovery path abuse-resistant`;
- `human-assisted recovery ≠ high-assurance recovery`;
- `support agent accepted claimant ≠ organization independently authorized destructive change`;
- `notification delivered ≠ action authorized`;
- `notification after destructive change ≠ preventive control`;
- `audit record exists ≠ audit record independent of the actor being audited`;
- `authorized to inspect ≠ authorized to replace trust root`;
- `waiting period exists ≠ attacker cannot wait`;
- `registrar MFA enabled ≠ support-assisted takeover impossible`;
- `two factors ≠ two independent failure domains`;
- `event repudiated ≠ compromise effects automatically reversed`;
- `case number exists ≠ exact destructive action and resulting authority are evidenced`;
- `fraudulent recovery reversed at provider ≠ installed hostile state eradicated`;
- `wipe removes hostile cache ≠ wipe is acceptable if it destroys authoritative local records`.

## 17. OPEN / CHANGE WATCH

**OPEN**
- actual MintTap/LogMate IdP, registrar, registry, DNS, hosting, source/build, signing/trust topology;
- exact provider support/ownership-verification procedures;
- exact independent notification/audit channels;
- recovery-factor independence and custody;
- hold/lock/quorum/destructive-action policy;
- legal/organizational ownership evidence;
- target managed-iPad hostile/stale Service Worker recovery evidence;
- exact repudiation/cancellation capabilities and limits;
- exact recovery telemetry/privacy review.

**CHANGE WATCH**
- NIST SP 800-63-4 family and errata;
- registrar/registry transfer, lock and recovery policy;
- provider account-recovery/support procedures;
- browser/OS installed-PWA reset/update behavior;
- managed-device policy affecting recovery/notification channels.

## Next adjacent boundary

112 closes the generic dual-use recovery-ceremony prerequisite. If exact implementation evidence remains unavailable, the next highest-value adjacent boundary is **compromise scoping and trust re-entry after hostile origin/service-worker exposure**: determine which clients/artifacts/data/trust generations can be considered clean after domain/deployment takeover, without using indiscriminate local-data wipe as a substitute for provenance and reconciliation.