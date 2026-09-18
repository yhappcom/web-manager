# 141 — PWA Recovery-Authority Abuse Resistance, Quorum & Emergency Reset Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + RESET-IMPLEMENTATION + INCIDENT-DRILL VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 099–102 trusted-state reset/rebootstrap; 111 recovery-authority continuity/abuse resistance; 117–121 emergency/corrective-control lifecycle; 138–140 compromise/re-entry/trust-floor recovery; Track B recovery UX; Track C destructive validation; Software Engineering owns implementation.

## Purpose

140 established that trust-floor loss is evidence loss, not rollback authorization, and that reset/rebootstrap is a high-consequence authority. The adjacent risk is that the recovery authority itself becomes the easiest path around the trust model.

Central rule:

> **Recovery authority must be narrower than ordinary super-admin power, consequence-scaled, independently authorized enough for the threat model, replay-safe, auditable, time/scope bounded, and unable to silently convert emergency availability into permanent rollback authority.**

This study does not prescribe a particular IAM vendor, threshold-signature scheme, hardware token, MDM product, or fixed number of approvers.

## 1. Five-track balance

- **A Platform/Browser — dependency supplier:** browser/PWA state cannot itself establish organizational quorum or independent recovery authority; stale Service Worker/cache/client state must not bypass server-side recovery authorization.
- **B UX/IA/Content — elevated consumer:** owns truthful pending-approval, emergency-limited, expired/rejected, local-preserved and post-reset-review states without implying success before durable authorization.
- **C Quality — high pressure:** owns single-channel compromise, replay, partial approval, approver loss, stale policy, clock, restart, duplicate request and emergency-expiry matrices.
- **D Search/Analytics — constrained consumer:** telemetry can measure observed recovery events but cannot serve as authorization, quorum evidence or fleet completeness proof.
- **E Architecture/Security/Operations — highest-risk owner:** owns authority decomposition, separation of duties, consequence-based threshold, break-glass scope, provenance, expiry/revocation and post-emergency normalization.

Allocation remains E-heavy because a universal recovery credential can nullify 099–140.

## 2. SOURCE — separation of duties and least privilege address authorized-abuse risk

NIST SP 800-53 Rev. 5 AC-5 defines separation of duties to reduce abuse of authorized privileges and malicious activity without collusion; AC-6 requires least privilege. NIST describes the control catalog as tailorable to mission/business needs and risk rather than a universal fixed ceremony.

Sources checked 2026-09-19:
- https://csrc.nist.gov/pubs/sp/800/53/r5/final
- https://csrc.nist.gov/glossary/term/least_privilege

OWASP Secure Product Design likewise treats least privilege and separation of duties as design principles; the Authorization guidance recommends deny-by-default and explicit justification of granted access.

Sources checked 2026-09-19:
- https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

**SYNTHESIS:** a recovery operator who can request, approve, execute, erase evidence and select arbitrary historical trust state is a concentrated failure domain. Separation should follow consequence and organization size, not ritual.

Guards:
- `authenticated administrator ≠ authorized reset`;
- `admin role ≠ recovery role ≠ audit role`;
- `least privilege ≠ merely fewer UI buttons`;
- `two named approvers ≠ independent approval`;
- `different accounts ≠ different failure domains`.

## 3. Threshold/quorum is consequence-based, not universally mandatory

A fixed two-person rule is not a Web/PWA standard. The correct question is whether one compromised channel can cause an unacceptable consequence.

Generic tiers:
- **Low consequence:** ordinary account/session recovery that cannot lower system trust or resurrect revoked authority may use normal product authorization.
- **Elevated consequence:** device replacement or trust rebootstrap that restores remote mutation should require stronger, context-bound evidence and explicit provenance.
- **Critical consequence:** lowering a remembered trust floor, replacing a compromised root/recovery authority, overriding containment, or re-authorizing a revoked lineage should require independent-enough approval/threshold or an equivalently strong recovery mechanism justified by threat model.

For a small app company, independence can be achieved by separating credentials/channels or pre-provisioned recovery material; it need not imply a large enterprise committee.

Guards:
- `quorum count high ≠ quorum independent`;
- `independence required ≠ many employees required`;
- `small company ≠ single credential should control everything`;
- `MFA on one admin ≠ separation of duties`.

## 4. Recovery request, approval and execution are distinct objects

Model a recovery as a context-bound authorization transaction rather than an informal instruction.

Minimum semantic dimensions, product-dependent:
- recovery request ID / logical operation ID;
- subject/account/device/product/lineage;
- reason/classification;
- current known floor and requested target floor/recovery epoch;
- authority generation/policy version;
- requester and approval evidence;
- creation, expiry and consumption state;
- permitted effects and explicit prohibitions;
- resulting authoritative floor/revision;
- provenance/audit reference.

The approval must bind to the exact consequence. A signature/approval for device replacement must not be reusable to lower a global trust root.

Guards:
- `approval valid ≠ approval valid for this subject/effect`;
- `request authenticated ≠ target floor authorized`;
- `request ID unique ≠ request semantically safe`;
- `same user + same device ≠ same recovery transaction`.

## 5. Replay, duplicate delivery and ambiguous acknowledgement

Recovery is a high-consequence distributed operation and inherits earlier idempotency/ACK lessons. Retrying after network loss must not create a second reset or consume a second emergency grant.

Generic state machine:
`REQUESTED → APPROVAL-PENDING → AUTHORIZED → EXECUTION-PENDING → APPLIED-DURABLE → ACKNOWLEDGED → CLOSED`, with `REJECTED`, `EXPIRED`, `REVOKED`, `AMBIGUOUS/REVERIFY` branches.

Durable logical operation identity and resulting state are required before success is reported. Server-side authorization remains authoritative; client state or stale Service Worker UI cannot manufacture approval.

OWASP Transaction Authorization explicitly requires authorization to be enforced server-side and resistant to client parameter tampering.

Source checked 2026-09-19: https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html

Guards:
- `retry ≠ new recovery intent`;
- `ACK missing ≠ recovery not applied`;
- `approval token present ≠ token unused/current`;
- `client says approved ≠ server authorization state approved`;
- `duplicate request blocked ≠ conflicting request resolved`.

## 6. Break-glass is bounded emergency authority, not a permanent superuser

NIST SP 800-53 treats emergency accounts as short-term crisis mechanisms that may bypass normal activation and should be disabled when no longer required. CISA cloud guidance recommends strongly protected emergency accounts, consideration of multiple-user coordination, extensive logging/auditing and attention to whether administrators can suppress alerts/logs.

Sources checked 2026-09-19:
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
- https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

**TRANSFER VALIDATION:** emergency recovery may legitimately bypass ordinary workflow, but the bypass itself needs bounded authority, evidence and lifecycle.

Generic constraints:
- explicit emergency reason and scope;
- minimum effects necessary to restore safe service/data access;
- short validity/one-time consumption where feasible;
- independent notification/evidence path where threat model warrants;
- inability to silently erase its own provenance;
- post-use credential/authority rotation where relevant;
- mandatory normalization/review after emergency state ends.

Guards:
- `break-glass exists ≠ break-glass always enabled`;
- `emergency bypasses normal workflow ≠ emergency bypasses all policy`;
- `service restored ≠ emergency authority retired`;
- `emergency credential secret ≠ emergency use unobservable`.

## 7. Approval independence is about correlated compromise

Two approvals add little if both depend on the same compromised mailbox, password manager, device, IdP session, signing root or support console. Independence is threat-model-relative.

Ask:
1. Which failure/attacker caused the reset need?
2. Which credentials/channels approve it?
3. Can that attacker control all of them through one compromise?
4. Can one approver alter audit evidence or policy after approval?
5. Does the emergency path depend on the same unavailable infrastructure it is meant to recover?

**MINTTAP DIRECTION:** use the minimum independent recovery factors/channels necessary for the consequence. Avoid both a universal master credential and unnecessary enterprise ceremony.

Guards:
- `separate email addresses ≠ independent channels`;
- `different vendors ≠ independent if same root account controls both`;
- `offline recovery material ≠ safe if copied into ordinary online secrets store`;
- `quorum reached ≠ underlying policy current`.

## 8. Recovery authority must not choose arbitrary history

140 preferred recovery that establishes a current/bounded-safe state. 141 strengthens that boundary: ordinary recovery operators should not receive a free-form `setTrustEpoch(any)` capability.

Safer generic semantics are declarative/bounded, e.g. authorize this subject to rebootstrap to the currently approved recovery epoch, or authorize this replacement device under current successor trust. The server/policy engine determines the allowed target.

Guards:
- `can recover availability ≠ can select historical security state`;
- `operator knows desired epoch ≠ operator should supply authoritative epoch`;
- `support override ≠ policy override`;
- `recovery authority ≠ root-signing authority`.

## 9. Recovery provenance and audit independence

Recovery provenance should record enough to answer who/what authorized which consequence under which policy, without turning logs into a shadow copy of sensitive user data.

Where feasible, the actor executing a reset should not be able to silently destroy the only evidence of that reset. This follows the same independence logic as earlier provenance/checkpoint studies.

Privacy/data-minimization still applies: record identifiers, policy/authority generation, result, timing/evidence references and reason class where sufficient; do not automatically retain full flight/investment payloads.

Guards:
- `recovery logged ≠ log independently trustworthy`;
- `audit record complete ≠ business payload must be copied`;
- `analytics event emitted ≠ recovery provenance durable`;
- `no alert received ≠ no recovery occurred`.

## 10. Emergency lifecycle: activation → use → containment → normalization

An emergency reset is incomplete until elevated authority is retired and the system returns to a defined normal state.

Generic lifecycle:
1. classify incident/recovery need;
2. authorize bounded emergency capability;
3. activate for defined subject/scope;
4. execute idempotently;
5. durably establish resulting floor/authority;
6. revoke/consume/expire emergency capability;
7. rotate affected credentials where needed;
8. reconcile offline devices/data under current policy;
9. review provenance and exceptions;
10. close only when ordinary controls are restored or explicit residual risk is accepted.

Guards:
- `reset applied ≠ incident closed`;
- `credential expired ≠ every session/grant revoked`;
- `ordinary service available ≠ ordinary trust normalized`;
- `postmortem written ≠ corrective control verified`.

## 11. PWA/EFB boundary

A company iPad PWA may be offline during the entire emergency. It must not be expected to participate in live quorum or receive immediate revocation. On reconnect it should receive authenticated current recovery/trust state and enter re-entry/reconciliation before remote mutation authority is restored.

A stale Service Worker, cached support page, local clock or offline UI cannot approve a trust-floor reset. Irreplaceable local flight records remain preservable/readable/exportable where product semantics allow while remote write remains blocked.

Guards:
- `offline user confirmed reset ≠ server recovery authorized`;
- `cached emergency page available ≠ emergency capability current`;
- `PWA reinstalled ≠ emergency reset consumed`;
- `managed iPad ≠ organizational recovery quorum available`;
- `local data preserved ≠ remote mutation authorized`.

## 12. Track B UX handoff

Required semantic states include:
- recovery request awaiting additional approval;
- approval expired/revoked; local data unchanged;
- emergency access active for a limited purpose;
- reset applied but synchronization remains blocked pending trust normalization;
- this device cannot complete recovery offline;
- recovery failed without deleting local records.

Do not expose quorum mechanics as false reassurance. `Two approvals received` is not a user-facing security guarantee if the product has not validated independence.

Design Studio Web at run start is **W091 / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, Safari/Firefox, screen reader, physical-device/input and human UX remain OPEN; no recovery-UX PASS transfers.

## 13. Track D measurement boundary

Privacy-minimized telemetry may measure observed recovery request volume, approval latency, rejection/expiry classes, emergency-duration and normalization completion. It cannot prove authorization legitimacy, approver independence, offline fleet completeness or absence of unobserved recovery attempts.

Guards:
- `two approval events observed ≠ two independent approvals`;
- `zero emergency events observed ≠ emergency path cannot be abused`;
- `recovery success metric high ≠ recovery policy secure`.

## 14. Destructive validation campaign — Track C handoff

1. single support credential compromised → cannot unilaterally lower critical floor;
2. single admin credential compromised → scoped authority enforced;
3. two approvers share same compromised IdP session → independence assumption fails visibly;
4. requester also attempts self-approval where policy forbids → reject;
5. approval for device A replayed for device B → reject;
6. approval for account X replayed for Y → reject;
7. approval for replacement reused for root rollback → reject;
8. valid request duplicated → idempotent;
9. same request ID/different payload → reject/conflict;
10. approval expires before execution → no reset;
11. approval revoked before execution → no reset;
12. execution commits, ACK lost → retry returns prior result without second reset;
13. crash after approval before execution → recover pending state safely;
14. crash after effect before provenance publication → detect/repair without duplicate effect;
15. emergency credential copied into ordinary secrets store → threat model flags correlated failure;
16. break-glass used while ordinary admin path works → policy/alert path exercised;
17. break-glass remains active after recovery → normalization gate fails;
18. emergency actor attempts to erase only audit trail → evidence control blocks/detects;
19. stale Service Worker displays old approved request → server denies if no longer current;
20. Cache Storage replays old emergency package → freshness/consumption checks reject;
21. device clock rollback extends local expiry → server/current trusted policy wins;
22. device clock forward causes false expiry → safe retry/reverification, no downgrade;
23. offline iPad requests reset → local preservation only until server authorization;
24. lost device reconnects after replacement reset → current revocation/re-entry policy applies;
25. replacement approved but old device not revoked → separate containment remains OPEN/visible;
26. one approver unavailable → no silent quorum weakening; invoke explicit alternate emergency policy if defined;
27. recovery policy version changes mid-request → re-evaluate or invalidate under defined semantics;
28. recovery authority generation revoked → outstanding grants cannot silently survive;
29. telemetry/log pipeline unavailable → authorization still secure; evidence-gap state explicit;
30. physical Safari/Home Screen termination/restart during recovery → no UI-only success; durable server/floor state determines result.

No product PASS is claimed until actual implementation/runtime evidence exists.

## 15. Integrated operational judgment

A practical small-company design should optimize for **minimal sufficient independence**, not maximal ceremony. The default should be no universal online master reset credential. High-consequence recovery should bind exact subject/effect, require stronger or independent-enough authorization, execute idempotently server-side, preserve durable provenance, expire/consume emergency capability and force normalization.

The exact threshold is a product risk decision. A two-person quorum is not automatically required; conversely, one person's ordinary admin session is not automatically sufficient merely because the organization is small.

## 16. OPEN / DEPENDENCY / CHANGE WATCH

### OPEN — product/runtime
- actual MintTap/LogMate account/device/role model;
- actual trust-floor and recovery-authority representation;
- available admin/support identities and independent credential channels;
- actual managed-iPad/MDM recovery controls;
- server-side idempotency/transaction/provenance implementation;
- lost-device revocation and replacement semantics;
- legal/aviation/investment requirements for emergency access/audit;
- physical Safari/Home Screen interruption behavior;
- real incident and recovery drills.

### DEPENDENCY
Software Engineering owns implementation and executable failure-injection. Security/legal review is required if real recovery controls protect regulated/safety-sensitive records. Design Studio owns reusable interaction design; Web Manager supplies state/consequence requirements.

### CHANGE WATCH
- NIST SP 800-53 and digital-identity guidance revisions;
- CISA privileged/emergency-access guidance;
- WebKit storage/PWA lifecycle behavior;
- actual platform/provider IAM/MDM capabilities if selected.

## 17. Gate

Generic PASS requires ability to:
1. explain why recovery authority is itself an attack surface;
2. distinguish least privilege, separation of duties, MFA and quorum/independence;
3. scale threshold to consequence rather than impose a universal number;
4. bind recovery authorization to exact subject/effect/policy;
5. make recovery replay-safe/idempotent and server-authoritative;
6. constrain break-glass by scope/time/provenance and retire it after use;
7. identify correlated approval failure domains;
8. preserve local PWA/EFB data while remote authority is blocked;
9. keep analytics/audit/authorization evidence distinct;
10. state product/runtime unknowns without inventing implementation facts.

**Result: PASS (generic). Production validation remains OPEN.**

## Next highest-value target

**PWA recovery-authority continuity under organizational loss, credential unavailability & succession governance**: test whether the abuse-resistant controls introduced here can still recover when an owner/approver is unavailable, an identity provider fails, the company changes personnel, or emergency credentials age out—without weakening quorum ad hoc or creating a permanent master-key loophole. Reconcile with earlier 126 organizational-loss recovery work rather than duplicating it.