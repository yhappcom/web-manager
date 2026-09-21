# 196 — PWA Recovery-Authorization Evidence Survivability, Emergency-Identity Independence & Break-Glass Drill Assurance

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A browser/PWA reconnect and cached-state boundaries; Track B recovery/drill state semantics; Track C assurance/destructive validation; Track D privacy-bounded security telemetry.
Dependencies: 183–195.

## Problem
195 separated dormant recovery capability, incident eligibility, activation authorization, bounded exceptional capability, successor admission and privilege extinction. The adjacent problem is assurance: the organization must still be able to prove who/what authorized exceptional recovery when ordinary IAM, audit or control-plane services are unavailable or compromised; emergency identity must survive relevant normal-IAM failures without becoming a permanent shadow-admin plane; and recurring drills must prove both recovery availability and post-use extinction without routinely exercising unrestricted live bypasses or exposing live recovery secrets.

Central rule: **recovery evidence, emergency identity and drill evidence are three distinct assurance objects. A drill that proves login availability does not prove authorization legitimacy, evidence survivability, bounded scope, or post-use privilege extinction. Independence must be evaluated by failure domain, not by account name or storage location.**

## Five-track balance
- **A Platform/Browser:** browser/SW/Cache Storage/IndexedDB may retain local observations and user work, but cached recovery evidence or a prior drill result is not an activation/currentness oracle.
- **B UX/IA/Content:** owns clear distinctions among drill/simulation, real incident, evidence unavailable, emergency identity unavailable, exceptional authority active, extinction pending and normal restored. Design Studio remains canonical for interaction/human validation.
- **C Performance/Accessibility/Quality:** owns executable drills, fault injection, evidence-recovery checks and negative post-extinction oracles. Physical-device, Safari/iPadOS, AT and representative-human evidence remain OPEN.
- **D Search/Discovery/Analytics:** consumes only coarse drill/recovery outcomes. Product analytics must not store recovery secrets, raw approval artifacts or stable security-staff dossiers and cannot be an authorization source.
- **E Architecture/Security/Operations:** **highest-risk owner**; owns evidence survivability, emergency-identity failure-domain analysis, drill safety, activation proof and extinction proof.

## SOURCE

### NIST SP 800-53 Rev.5 / Release 5.2.0 — controls and assurance are distinct
NIST SP 800-53 Rev.5 remains the current control catalog; Release 5.2.0 was issued 2025-08-27. Its contingency-planning, access-control, audit, incident-response and assessment families provide a current generic precedent for governed emergency access, contingency capability, evidence and assurance. The catalog explicitly distinguishes control functionality from assurance/confidence in that capability.
Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### NIST SP 800-53A Rev.5 — assessment must establish operating outcome
SP 800-53A Rev.5 remains the current assessment methodology; its Release 5.2.0 was also issued 2025-08-27. It treats assessment as determining whether controls are implemented correctly, operate as intended and produce the desired outcome, rather than merely checking documentation.
Source: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

### NIST SP 800-61 Rev.3 — current incident-response baseline
NIST finalized SP 800-61 Rev.3 on 2025-04-03, superseding Rev.2. It integrates incident response across CSF 2.0 risk management and emphasizes preparation, response and recovery as organizational capabilities. Transfer: break-glass evidence and drills belong to a maintained incident/recovery capability, not an isolated credential ceremony.
Source: https://csrc.nist.gov/pubs/sp/800/61/r3/final

### NIST SP 800-84 — test/training/exercise precedent
SP 800-84 remains a final NIST guide for designing, conducting and evaluating test, training and exercise events for IT plans/capabilities. It is old (2006), so use it as a durable TT&E-method precedent rather than current identity-platform guidance.
Source: https://csrc.nist.gov/pubs/sp/800/84/final

### Microsoft Entra emergency-access guidance — current vendor-specific operational precedent
Current Microsoft guidance for Entra emergency access recommends cloud-only emergency accounts independent of federated identity providers, different phishing-resistant authentication from normal admin paths, credentials/devices in separate secure locations, monitoring of all use, and functionality validation at least every 90 days. It also recommends that devices used for emergency access have multiple network paths without a common failure mode. This is **Microsoft Entra-specific**, not a universal MintTap topology or numeric account requirement.
Source: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access

## SYNTHESIS 1 — recovery authorization evidence needs an independent-enough survival path
A real activation may occur precisely when normal identity, logging or control-plane services cannot be trusted. Therefore the recovery evidence chain cannot rely exclusively on those same services.

Separate at minimum:
1. **incident eligibility evidence** — why normal authority cannot safely perform recovery;
2. **authorization evidence** — what then-current recovery policy authorized which actors/capabilities/scope;
3. **activation evidence** — which exceptional generation actually became effective, where and when according to trusted evidence available to the system;
4. **action evidence** — what consequence-bearing recovery actions were accepted;
5. **successor-admission evidence** — exact normal authority/policy/currentness floor admitted after recovery;
6. **extinction evidence** — positive negative tests showing the exceptional generation no longer works;
7. **historical verification context** — enough policy/key/verifier context to interpret those records later without retaining standing recovery authority.

Persistent guards:
- `recovery log exists ≠ recovery authorization proven`;
- `ordinary audit unavailable ≠ recovery may be unaudited`;
- `evidence copied elsewhere ≠ evidence failure-domain independent`;
- `evidence immutable ≠ evidence complete or current`;
- `emergency account exists ≠ emergency identity independent`;
- `different IdP tenant/account ≠ independent recovery path`;
- `break-glass login succeeds ≠ reconstitution authorization is legitimate`;
- `drill PASS ≠ live incident PASS`;
- `tabletop PASS ≠ credential retrieval PASS ≠ activation PASS ≠ extinction PASS`;
- `secret not exposed during drill ≠ live secret recoverable`;
- `live secret used during every drill ≠ good assurance practice`.

### Evidence survivability without a new authority oracle
An independently retained activation record may prove what was observed/authorized under a known policy, but the evidence store must not gain unilateral power to issue new recovery authority. Evidence survivability and authority issuance remain separate.

If ordinary audit is compromised, surviving evidence should permit later reconstruction of the bounded transition. If no trustworthy evidence survives for a consequence-bearing interval, that interval remains UNKNOWN rather than being reconstructed from operator memory or a successor system's later assertion.

## SYNTHESIS 2 — emergency identity independence is a failure-domain property
An emergency identity path should be evaluated against the failures it is intended to survive. Potential correlation includes:
- same federation/SSO dependency;
- same IdP administration/recovery hierarchy;
- same MFA/push/SMS/telephony dependency;
- same employee-owned device;
- same password manager/vault/KMS;
- same workstation/device-compliance policy;
- same DNS/network/provider dependency;
- same privileged administrators/custodians;
- same billing/organization recovery channel;
- same automated account-cleanup/expiration process;
- same monitoring/evidence sink.

A path may be independent for one failure and correlated for another. `independent` therefore requires an explicit failure-domain statement, not a boolean label.

### Independence must not create permanent shadow administration
Survivability does not justify an unrestricted parallel admin plane. Generic direction:
- emergency identity is not used for ordinary administration;
- its normal-state capability is dormant or narrowly constrained according to the actual platform design;
- use is high-signal and monitored;
- custody/authorized-user lists are governed;
- the path is tested without normalizing daily use;
- after real activation, successor normal authority is established and exceptional privilege is extinguished under 195's negative oracle;
- historical evidence is retained separately from reusable authority material.

Exact account count, threshold, FIDO2/PKI choice, hardware, provider, vault, secret-sharing scheme and personnel model remain OPEN.

## SYNTHESIS 3 — drill assurance is layered, not one binary test
A mature drill program should avoid two symmetric failures: **paper recovery** that has never been executable, and **routine live bypass** that turns emergency access into normal administration.

Use progressively stronger evidence classes:

### Layer 0 — inventory and dependency review
Verify documented recovery actors, policy generation, custody, contact/role changes, failure domains, provider dependencies, evidence sinks, expiry/cleanup risks and expected successor/extinction process.

### Layer 1 — tabletop / decision drill
Exercise incident eligibility, authorization decision, scope, UNKNOWN handling, communication and stop conditions without activating production privilege. Useful for process comprehension; does not prove credentials or enforcement.

### Layer 2 — retrieval/authentication readiness
Prove authorized personnel can retrieve the required emergency material/device and reach the intended authentication path under representative dependency failures. Prefer a provider-supported validation method or isolated target when possible. This does not by itself prove production reconstitution scope or extinction.

### Layer 3 — bounded technical exercise
In a safe environment or explicitly bounded production-safe operation, verify the intended exceptional authorization path, evidence capture, monitoring and scope enforcement. Avoid unnecessary access to customer/flight data and avoid changing real authority merely to demonstrate the ceremony.

### Layer 4 — extinction/anti-resurrection exercise
After the bounded activation/exercise, prove the retired exceptional capability fails across applicable API/session/region/background/PITR paths and that successor currentness state survives rollback attempts.

### Layer 5 — compound-failure exercise
Periodically inject the failures the emergency path is meant to survive: normal IdP/federation unavailable, primary audit unavailable, one custodian unavailable, one network path unavailable, stale regional state, or recovery evidence sink loss. Do not infer compound resilience from isolated happy-path tests.

A single vendor recommendation such as a 90-day emergency-account validation interval is a provider-specific operational precedent, **not a universal MintTap drill cadence**. MintTap cadence remains threat/risk/provider/product specific and OPEN.

## Drill safety and evidence hygiene
A drill should bind a unique drill identifier and be unmistakably distinguishable from a real incident. Generic safeguards:
- declare simulation vs real incident in the authorization/evidence record;
- predefine allowed targets/actions and stop conditions;
- use least-sensitive fixtures/safe resources where possible;
- do not copy recovery secrets into tickets, analytics, screenshots or chat;
- monitor for unexpected real-world side effects;
- preserve evidence needed to assess the control while minimizing personnel/device/customer data;
- rotate/reseal material if the exercise meaningfully exposed it under the applicable policy;
- conduct post-exercise review and corrective action;
- require a negative post-exercise oracle when exceptional capability was actually activated.

`successful exercise` means the stated oracle was satisfied; it must not be generalized beyond the environment, generation, provider behavior and failure injection actually tested.

## PWA / EFB boundary
A company iPad/PWA is a recovery **subject/client**, not generic server emergency identity or evidence authority.

For a long-offline iPad returning after a drill or real recovery:
1. preserve unique local flight/logbook records before destructive migration;
2. distinguish drill metadata from real recovery generations;
3. treat cached policy/key/evidence/SW/IndexedDB state as historical observation;
4. obtain current authenticated server policy/currentness/recovery state;
5. refuse queued consequence-bearing work that depended on a retired exceptional generation;
6. reconcile acknowledged history vs local-only work;
7. resubmit local-only work under current normal authority;
8. keep client-local recovery telemetry from becoming a server activation oracle.

A drill must not assume Safari/iPadOS background execution, persistent storage, unattended sync, direct device-to-device transport or MDM behavior. Those remain separate runtime VALIDATION/CHANGE WATCH items.

## UX / accessibility transfer
Track B should specify distinct user/operator states for **drill**, **real incident**, **authorization unavailable**, **evidence unavailable**, **exceptional scope active**, **extinction pending**, and **normal restored**. A drill banner alone is insufficient if the underlying authority is live; semantics must reflect actual enforcement state. Status must not depend on color alone and requires keyboard, zoom/reflow, screen-reader and representative-human validation before product PASS.

## Privacy / analytics transfer
Recovery drills can expose staff identity, custody locations, device identifiers, network paths and operational weakness. Security evidence may justify some of this data; ordinary product analytics generally should not. Track D receives low-cardinality outcomes/timing only where useful. Drill evidence must not become an employee-surveillance or flight/customer dossier by default.

## Track C destructive campaign
Define a **328-case generic campaign**, extending 195's 320 cases with at least these adjacent classes:
- normal IdP unavailable while emergency identity still secretly depends on its MFA/recovery path;
- emergency credential stored separately but vault/KMS/admin recovery is shared;
- primary audit unavailable and recovery evidence silently disappears;
- recovery evidence survives but can itself authorize new activation;
- tabletop PASS while live credential retrieval fails;
- authentication PASS while activation scope enforcement fails;
- drill uses production bypass and leaves privilege effective afterward;
- long-offline PWA confuses drill generation with real/current recovery state;
- one network path and one custodian fail simultaneously;
- personnel change leaves former custodian with effective emergency material;
- monitoring is disabled by the same incident being drilled;
- PITR restores pre-drill or active exceptional state after extinction.

Campaign definition is not execution.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** NIST 800-53/53A support separating control existence from assurance that it operates correctly and achieves the intended outcome; they do not prescribe MintTap recovery identities or drill cadence.
- **TRANSFER VALIDATION:** NIST 800-61r3 supports maintained incident-response/recovery capability and organizational learning; it does not define break-glass cryptography or quorum.
- **TRANSFER VALIDATION:** NIST 800-84 supports structured test/training/exercise design and evaluation; because it is a 2006 publication, it is not current identity-platform guidance.
- **TRANSFER VALIDATION:** Microsoft Entra guidance provides a current concrete precedent for emergency identities independent of federation, separate authentication/custody, monitoring and regular drills; it is vendor-specific and cannot be promoted to universal architecture.
- **CONTRADICTION:** a second account in the same failed identity/recovery domain is not meaningful independence for that failure.
- **CONTRADICTION:** a quarterly successful login that never tests evidence survival or privilege extinction is not end-to-end recovery assurance.
- **CONTRADICTION:** repeatedly using unrestricted production break-glass privilege merely to prove it works can normalize the bypass and expand exposure.

## MINTTAP DECISION / DIRECTION
1. Treat recovery authorization evidence, emergency identity and drill evidence as separate assurance objects.
2. Require recovery evidence to survive relevant ordinary IAM/audit/control-plane loss in an independent-enough failure domain without becoming a new issuance authority.
3. Evaluate emergency-identity independence against explicit failure domains; do not infer it from account/provider labels.
4. Prevent emergency identity from becoming routine shadow administration.
5. Use layered drills: inventory/dependency, tabletop, retrieval/auth readiness, bounded technical activation where justified, extinction/anti-resurrection, and compound-failure exercises.
6. Do not adopt a universal drill frequency or numeric quorum from generic/vendor precedent; derive it from the actual product/provider/threat model.
7. Every drill that activates exceptional privilege must include post-use negative authorization/extinction evidence.
8. Keep PWA/EFB clients outside server break-glass authority; preserve local data and rebootstrap forward.

## OPEN / DEPENDENCY / VALIDATION
**OPEN:** actual MintTap/LogMate IAM/federation/provider topology; emergency identities; custody/vault/KMS/network failure domains; recovery evidence store; actor/threshold policy; provider-supported safe validation methods; session/token invalidation; regional authorization cache; drill cadence; physical iPad/WebKit behavior; MDM; privacy/legal/aviation requirements; human/AT comprehension.

**DEPENDENCY — Software Engineering:** concrete recovery/evidence state machine, provider/IAM integration, token/session invalidation, regional enforcement, PITR anti-resurrection, fault injection and negative authorization tests. Current Software Engineering Studio Foundation evidence does not close iOS/Safari/EFB or product runtime.

**DEPENDENCY — Design Studio:** recovery/drill status semantics, accessible high-risk interaction and representative-human/AT validation. Current Web Specialist Stage 3 remains PRACTICE/NOT PASSED.

**VALIDATION:** execute 328-case campaign; remove normal federation/IdP path; remove primary audit sink; make one custodian and one network path unavailable; verify evidence still survives; verify emergency path cannot perform ordinary work outside authorized scope; activate only in bounded exercise where justified; prove extinction across API/session/region/PITR; test long-offline physical iPad/Safari/Home Screen; perform privacy and human/AT review.

## CHANGE WATCH
NIST SP 800-53/53A 5.x releases; NIST SP 800-61r3 errata/resources; NIST SP 800-84 status/replacement; Microsoft Entra and other selected provider emergency-access semantics; WebKit/iPadOS PWA storage/session/background behavior; Design Studio and Software Engineering runtime evidence.

## Gate
**PASS (generic).** Web Manager can separate recovery-evidence survivability, emergency-identity independence and drill assurance; reason about hidden shared failure domains; design layered drills that avoid both paper-only recovery and normalized unrestricted bypass; and require post-use extinction evidence. Production certification remains OPEN.