# 195 — PWA Reconstitution Activation Authorization, Break-Glass Abuse Resistance & Post-Recovery Privilege Extinction

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A reconnect/cache/storage mechanics; Track B recovery-state UX; Track C destructive validation; Track D privacy-bounded security telemetry.
Dependencies: 183–194.

## Problem
194 bounded reconstitution authority as exceptional, generational and retireable. The adjacent risk is activation: a dormant recovery capability can become a permanent bypass if routine operators, compromised IdP sessions, stale offline material, or availability pressure can activate it; conversely, recovery can be impossible if activation depends exclusively on the same control plane or identity system that has failed.

Central rule: **possession of break-glass material, operator privilege, or evidence of outage is not itself authorization to reconstitute. Activation is a separately governed, incident-bound state transition. Post-recovery closure requires positive proof that exceptional privilege can no longer authorize consequence-bearing actions; hiding a control, ending an incident ticket, or rotating one credential is insufficient.**

## Five-track balance
- A Platform/Browser: browser/SW/Cache Storage/IndexedDB may preserve local work and observations; none can activate server recovery authority.
- B UX/IA/Content: owns clear semantics for recovery unavailable, activation pending, activated/bounded, successor admitted, privilege-extinction pending and normal authority restored.
- C Quality: owns destructive activation/bypass/extinction tests; execution, physical-device, AT and human evidence remain OPEN.
- D Search/Analytics: receives only coarse recovery-state telemetry; analytics cannot authorize activation and must not become an operator/device dossier.
- E Architecture/Security/Operations: **highest-risk owner**; owns activation preconditions, exceptional scope, separation from ordinary IAM and verifiable privilege extinction.

## SOURCE
### NIST SP 800-53 Rev.5 — emergency accounts and least privilege
NIST SP 800-53 Rev.5 AC-2 distinguishes temporary/emergency accounts and AC-2(2) requires automated removal or disabling after an organization-defined period. The broader control set associates privileged access with additional scrutiny and least privilege/separation of duties. Transfer: exceptional access should be bounded and removed/disabled rather than left indefinitely enabled. NIST does not prescribe MintTap recovery roles, quorum, cryptography or exact ceremony.
Sources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final ; https://csrc.nist.gov/glossary/term/least_privilege

### NIST CSF 2.0 — authorization governance
CSF 2.0 PR.AA-05 states that access permissions, entitlements and authorizations are defined in policy, managed, enforced and reviewed, incorporating least privilege and separation of duties. Transfer: emergency recovery must remain governed authorization, not an undocumented bypass.
Source: https://csrc.nist.gov/projects/cybersecurity-framework/filters

### NIST SP 800-63B-4 — recovery is distinct from routine authentication
The current SP 800-63B-4 (July 2025) treats account recovery as a distinct process, permits risk-analysed application-specific recovery methods, requires recovery notifications, and invalidates used saved recovery codes. Transfer: recovery credentials/processes can be separately governed, one-time/bounded and observable. This is subscriber-account recovery guidance, not a direct specification for infrastructure reconstitution.
Source: https://pages.nist.gov/800-63-4/sp800-63b.html

## SYNTHESIS — activation is a security transition, not credential use
Separate:
1. dormant recovery capability — material exists but cannot perform ordinary privileged actions;
2. incident eligibility — evidence shows normal authority/control plane cannot safely complete recovery;
3. activation authorization — applicable recovery policy authorizes a bounded incident/scope;
4. activated capability — exceptional operations are technically enabled only for that scope/generation;
5. reconstitution admission — exact successor policy/key/head is admitted;
6. successor normal authority — routine governance resumes;
7. privilege extinction — exceptional capability is technically incapable of future consequence-bearing use under the retired generation;
8. historical evidence — activation/admission/extinction evidence retained according to policy without retaining standing authority.

Persistent guards:
- `break-glass material exists ≠ break-glass activation authorized`;
- `operator is administrator ≠ operator may reconstitute authority`;
- `outage detected ≠ security incident eligibility established`;
- `IdP session valid ≠ recovery actor independently trustworthy`;
- `multiple approvals ≠ independent authorization domains`;
- `activation approved ≠ arbitrary recovery action authorized`;
- `incident closed ≠ exceptional privilege extinct`;
- `credential rotated ≠ all recovery capability extinct`;
- `UI control hidden ≠ authorization path disabled`;
- `audit says disabled ≠ negative execution test proves disabled`.

## Activation authorization model
A generic activation record should bind, without inventing product-specific fields: incident/recovery identifier; last supportable policy/currentness floor; reason normal authority cannot safely recover; exact recovery-authority generation; bounded operations/resources; activation start/expiry or equivalent termination condition; unresolved compromise/UNKNOWN intervals; deletion/hold/security constraints; evidence/approvals required by the then-current recovery policy; and the expected successor normal authority/floor.

Exact actor count, threshold, identity provider, hardware, escrow, cryptography and provider topology remain OPEN. Do not convert `separation of duties` into an arbitrary 2-of-3 rule without a product threat model.

### Independence from failed ordinary IAM
Activation cannot depend exclusively on an ordinary IdP/control plane whose integrity or availability is the incident being recovered from. Conversely, an offline recovery secret cannot by itself become unrestricted authority. The design requirement is an independently survivable authorization path whose trust basis is explicitly scoped and whose compromise does not silently inherit all ordinary production authority.

A compromised ordinary administrator/session must not be able to promote itself into reconstitution authority. A compromised recovery authority must not solely bless its successor. These are distinct compromise domains even if a future implementation shares infrastructure.

## Break-glass abuse resistance
Failure modes include:
- routine administrator discovers/uses dormant recovery credential;
- compromised IdP session invokes recovery API;
- stale incident token or expired activation is replayed;
- activation policy is rolled back by PITR;
- attacker fabricates availability failure to trigger weaker controls;
- recovery actor expands scope after activation;
- activation endpoint remains usable after successor admission;
- nominally separate approvers share the same compromised IAM/recovery domain;
- operator uses old offline credential after policy/key succession;
- region that missed retirement continues accepting recovery authority.

Therefore availability urgency may shorten operational latency but must not silently lower the authenticated security/currentness floor. If required activation evidence is unavailable, consequence-bearing recovery remains frozen or explicitly degraded rather than guessed current.

## Post-recovery privilege extinction
Extinction is stronger than logical closure. A generic extinction proof should test all applicable authorization paths, not only the normal UI:
1. successor normal policy/key/currentness floor is admitted and independently persisted;
2. recovery generation is marked retired/resealed under surviving current policy;
3. online sessions/tokens/capabilities derived from exceptional activation are invalidated or expire as designed;
4. cached regional authorization state is refreshed and rejects the retired recovery generation;
5. PITR/backup restoration cannot resurrect it as current because surviving anti-rollback state rejects the old generation;
6. old activation endpoints/actions reject positive replay attempts;
7. alternate/admin/API/background paths reject the same retired capability;
8. any private/secret material scheduled for destruction is handled under the applicable key/media policy while bounded historical verification evidence remains separate;
9. monitoring verifies no accepted exceptional operations after retirement, without treating absence of observed use as sole proof;
10. a recovery drill includes a **negative authorization oracle** demonstrating that retired exceptional privilege cannot perform consequence-bearing actions.

`no successful use observed` is not equivalent to `use is impossible under enforced policy`.

## PWA / EFB boundary
A company iPad/PWA must never hold generic server reconstitution authority merely because it may be offline during a disaster. Cached recovery notices, policy documents, Service Worker assets, IndexedDB records or old operator sessions are observations/local state only.

For a long-offline iPad returning after break-glass recovery:
1. preserve unique local flight/logbook records;
2. treat cached policy/key/activation state as historical observation;
3. obtain current authenticated successor policy/currentness/recovery generation;
4. detect that exceptional generation R is retired and refuse any queued operation whose authority depended on R;
5. distinguish remote-acknowledged records from local-only work;
6. resubmit local-only work under current normal authority with idempotency/provenance controls;
7. re-admit consequence-bearing queues only after current authorization and lineage reconciliation.

No assumption is made that iPadOS/Safari/Home Screen can execute background recovery, maintain persistent secrets indefinitely, or perform unattended device-to-device synchronization. Those remain runtime CHANGE WATCH/VALIDATION.

## UX/accessibility transfer
Do not expose a generic `Break Glass` affordance to ordinary users/operators without the applicable authorization context. Recovery UI should distinguish: activation unavailable; eligibility under investigation; activation authorization pending; exceptional authority active with bounded scope; successor authority admitted; privilege extinction pending; normal authority restored; local data safe/remote action paused.

Do not label the system simply `recovered` while exceptional privilege remains active. State must not rely on color alone and must survive screen-reader/keyboard/zoom/reflow testing. Design Studio remains canonical for reusable interaction/human validation.

## Privacy / analytics transfer
Activation evidence may identify security staff, devices, locations, incidents and customer/flight context. Security/audit systems may require justified evidence, but product analytics should receive low-cardinality state/timing outcomes rather than raw credentials, approval artifacts or stable operator/device histories. Analytics is never an activation oracle.

## Track C destructive campaign
Define a **320-case generic campaign**, extending 194's 312 cases with: ordinary admin invoking dormant recovery path; compromised IdP session activating recovery; expired activation replay; PITR restoring active break-glass state; scope escalation after valid activation; successor admitted while recovery API remains effective; one region retaining retired recovery generation; old offline credential replay after succession; negative-extinction oracle omitted; and long-offline PWA queue signed/authorized under retired exceptional state.

Campaign definition is not execution.

## TRANSFER VALIDATION / CONTRADICTION
- TRANSFER VALIDATION: NIST AC-2/AC-6 support bounded emergency access, additional scrutiny and least privilege; they do not define MintTap reconstitution topology or quorum.
- TRANSFER VALIDATION: NIST CSF PR.AA-05 supports governed/reviewed authorization and separation of duties; it does not imply a numeric threshold.
- TRANSFER VALIDATION: SP 800-63B-4 supports recovery as a distinct, risk-governed lifecycle with notifications and one-time recovery-code invalidation; infrastructure reconstitution remains a different problem.
- CONTRADICTION: an always-online emergency credential with unrestricted production privilege is operational convenience, not bounded break-glass recovery.
- CONTRADICTION: ending an incident while exceptional authorization remains technically effective leaves a standing bypass.
- CONTRADICTION: forcing recovery through the same compromised IdP/control plane defeats the independence sought by exceptional recovery.

## MINTTAP DECISION / DIRECTION
1. Treat reconstitution activation as a separate authenticated state transition, not possession/use of a magic credential.
2. Keep activation bounded to incident, recovery-authority generation, scope and termination conditions.
3. Do not let routine administrators or ordinary IdP sessions self-promote into reconstitution authority.
4. Do not invent a numeric quorum before actual threat model, actor topology and failure domains are known.
5. Require successor normal policy/currentness admission before declaring authority recovery complete.
6. Require positive negative-testing evidence that retired exceptional privilege no longer works across API/region/session/PITR paths.
7. Never put generic server break-glass authority on an offline PWA/EFB client; preserve local data and rebootstrap forward instead.
8. Keep exact roles, providers, credentials, thresholds, crypto, managed-iPad behavior, legal/aviation obligations and product UI OPEN.

## OPEN / DEPENDENCY / VALIDATION
OPEN: actual MintTap/LogMate IAM and recovery topology; reconstitution actors/roles; independent activation evidence; exact break-glass credentials; provider emergency controls; policy/key hierarchy; token/session invalidation; regional caches; backup/PITR interaction; managed-iPad/WebKit behavior; privacy/legal/aviation retention; operator/AT comprehension.

DEPENDENCY: Software Engineering owns concrete activation state machine, credential/session invalidation, regional enforcement, backup/PITR anti-resurrection, negative authorization tests and executable fault injection. Design Studio owns reusable recovery-state interaction and human/AT validation.

VALIDATION: execute 320-case campaign; compromise ordinary IdP/admin while preserving recovery path; compromise recovery path while preserving normal authority; replay expired/retired activation material; PITR to active break-glass state after retirement; prove every region/API rejects retired recovery generation; test long-offline physical iPad/Safari/Home Screen; validate privacy/accessibility/operator comprehension.

## CHANGE WATCH
NIST SP 800-53 5.x control updates; NIST SP 800-63-4 errata/updates; provider emergency-access/IAM semantics; WebKit/iPadOS PWA storage/session/background behavior; Design Studio/Software Engineering runtime evidence.

## Gate
**PASS (generic).** Web Manager can distinguish dormant capability, incident eligibility, activation authorization, activated exceptional scope, successor admission and privilege extinction; constrain break-glass recovery without inventing arbitrary quorum; require independence from failed ordinary IAM; and define negative evidence needed to prove post-recovery exceptional privilege is actually extinct. Production certification remains OPEN.