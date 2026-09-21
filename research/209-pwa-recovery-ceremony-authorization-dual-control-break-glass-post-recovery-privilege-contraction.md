# 209 — PWA Recovery-Ceremony Authorization, Dual-Control Break-Glass Abuse & Post-Recovery Privilege Contraction

Status: **PASS (generic) / PRODUCT + CEREMONY + IDENTITY/PAM + MANAGED-IPAD + RUNTIME + SECURITY/LEGAL + HUMAN VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A platform/identity mechanics; Track B recovery UX; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–208, especially 205–208.

## Problem
208 established that recovery-anchor custody, organizational identity/admin access, provisioning-provider availability and client/data survivability are separate properties. The next failure mode is procedural authority: after custody/provider loss, who may declare an emergency, invoke break-glass capability, approve a trust-changing recovery ceremony, and terminate the extraordinary authority afterward?

Central rule: **emergency pressure can justify a pre-governed exceptional path, but cannot silently create permanent authority, collapse separation of duties, or turn one surviving administrator/support operator/identity plane into a constitutional trust-reset root. Break-glass authority must be explicitly admitted, scoped, observable, bounded where technically possible, and followed by provable privilege contraction.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Authentication/session/browser/PWA mechanics transport emergency access but do not decide who constitutionally authorizes recovery.
- **B UX/IA/Content:** very high dependency pressure. Must distinguish `RECOVERY REQUESTED`, `APPROVAL INCOMPLETE`, `BREAK-GLASS ACTIVE`, `LOCAL DATA PRESERVED`, `REMOTE MUTATION RESTRICTED`, `NORMAL CONTROL RESTORED`, and `PRIVILEGE CONTRACTION INCOMPLETE` without implying that urgency bypasses policy.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **432 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Audit/telemetry can reveal ceremony use and drift but cannot authorize it or prove privilege extinction alone.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns ceremony initiation/approval, separation of duties, emergency capability, authority scope, revocation/contraction and recovery evidence.

## SOURCE

### NIST SP 800-53 Rev.5 — emergency/temporary accounts, separation of duties and least privilege
NIST SP 800-53 Rev.5 states that temporary and emergency accounts are intended for short-term use; emergency accounts may be rapidly activated in crisis situations and may bypass normal account-authorization processes. It also states that emergency/temporary accounts should be disabled or deactivated when no longer required. AC-5 and AC-6 provide the broader separation-of-duties and least-privilege control families.

Sources:
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
- https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page

**TRANSFER VALIDATION:** emergency access may legitimately have a different activation path, but exceptional activation does not imply permanent privilege. NIST does not prescribe MintTap's approver count, recovery-anchor topology or exact ceremony.

### CISA — break-glass, multi-user coordination, logging and least privilege
CISA cloud-use guidance recommends strong least privilege for administrative functions, separation of duties so one account does not have complete administrative access, emergency “Break Glass” accounts for cloud recovery, consideration of coordination by multiple agency users to enable access, and extensive logging/auditing of administrative activity. CISA Microsoft Entra/Azure AD security guidance also recommends finer-grained privileged roles, avoiding permanent active highly privileged assignments, approval for Global Administrator activation, and alerts for highly privileged assignments.

Sources:
- https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf
- https://www.cisa.gov/sites/default/files/2023-12/Azure%20Active%20Directory%20SCB_12.20.2023.pdf

**TRANSFER VALIDATION:** dual/multi-party activation, just-in-time privilege, alerts and audit are strong operational precedents. Vendor-specific Azure controls are not MintTap architecture.

### TUF — threshold root and out-of-band recovery precedent
TUF uses threshold root authority and offline-root principles. If fewer than threshold root keys are compromised, normal root rotation can replace them; if a threshold is compromised, root metadata must be re-issued out of band. TUF also compartmentalizes trust rather than granting every role equal authority.

Sources:
- https://theupdateframework.io/docs/faq/
- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/docs/metadata/

**TRANSFER VALIDATION:** threshold and compartmentalized authority are useful precedents for preventing a single emergency actor from becoming a universal trust-reset root. TUF is not adopted as MintTap's recovery protocol.

## SYNTHESIS 1 — recovery request, authorization and execution are separate states
A support ticket, outage declaration, monitoring alarm or surviving administrator request can initiate recovery without itself authorizing trust-changing action.

Model at least:
1. incident/recovery trigger observed;
2. recovery request opened;
3. scope and affected authority identified;
4. required approver/ceremony policy selected;
5. authorization threshold satisfied;
6. exceptional capability activated;
7. bounded recovery action executed;
8. current normal authority re-established;
9. exceptional capability revoked/contracted;
10. residual privilege/extinction checked.

`recovery requested ≠ recovery authorized`; `recovery authorized ≠ unrestricted administrator`.

## SYNTHESIS 2 — dual control is an anti-unilateral-reset property, not a magic number
The useful property is that no single ordinary administrator/support operator/compromised identity plane can unilaterally perform the high-consequence trust reset being protected. Exact quorum, roles and independence are product/security decisions.

Two nominal approvers controlled by one IdP/admin/recovery path may still be one failure domain. Independence must consider identity, device/key custody, organizational role, recovery channel and administrative control.

`two approvals ≠ two independent authorities`.

## SYNTHESIS 3 — unavailable approvers do not silently lower the policy
A crisis in which one or more expected approvers are unavailable is precisely when pressure to weaken policy is strongest. Unavailability must lead to a pre-governed alternate ceremony/reconstitution path, reduced capability, or blocked high-consequence recovery—not an undocumented threshold reduction.

`approver unavailable ≠ threshold obsolete`; `business urgency ≠ authority to rewrite recovery policy`.

If exceptional reconstitution changes the policy itself, that change must be explicit and separately evidenced rather than represented as satisfaction of the old quorum.

## SYNTHESIS 4 — break-glass privilege should be capability-scoped
Emergency authority should be no broader than required for the recovery objective. Distinguish capabilities such as:
- restore access to the recovery control plane;
- admit a successor custodian/provider;
- rotate/revoke a specific credential/anchor;
- quarantine a stale region/client cohort;
- inspect recovery evidence;
- preserve/export unique data;
- resume consequence-bearing remote mutation.

Possessing one capability does not imply the others. In particular, data-preservation access should not automatically confer trust-reset or remote-mutation authority.

`break-glass active ≠ all privileges active`.

## SYNTHESIS 5 — time bounds help, but trusted-time uncertainty must not create silent extension
Where technically supported, emergency privilege should have explicit expiry/lease semantics and renewal should require fresh authorization. But 201–204 established that local/client wall clocks and degraded time sources may be uncertain. Therefore expiry is only as trustworthy as its admitted time/currentness basis.

A time-bound grant whose expiry cannot currently be proven should not silently become indefinite. Consequence-bearing actions may need current server-side revalidation or quarantine while local data preservation remains available.

`expiry configured ≠ expiry enforced`; `clock uncertainty ≠ emergency lease extension`.

## SYNTHESIS 6 — audit is necessary but cannot authorize the action it records
Ceremony records should preserve request identity, scope, approver identities/roles, policy generation, evidence considered, activated capabilities, start/end/currentness basis, operations performed, revocations and post-recovery checks. Logs should be protected from the same emergency authority where feasible.

However, telemetry/log presence is observation, not authorization. A compromised administrator cannot legitimize an unauthorized trust reset by producing a complete audit trail.

`fully logged ≠ authorized`; `audit event emitted ≠ privilege extinct`.

## SYNTHESIS 7 — recovery completion and privilege contraction are separate gates
Restoring normal service does not prove emergency authority is gone. Post-recovery contraction must address:
- temporary/emergency accounts;
- temporary role assignments/eligibility;
- session/token/refresh-token residue;
- temporary credentials/certificates/keys;
- temporary firewall/network/provider exceptions;
- MDM/IdP/PAM assignments;
- emergency recovery packages/media;
- stale region/PITR copies;
- long-offline PWA/client state.

`normal service restored ≠ break-glass authority revoked`; `revocation requested ≠ revocation converged`.

## SYNTHESIS 8 — contraction needs positive normal-authority and negative emergency-authority proof
A scoped recovery can claim `CONTRACTED` only when normal/current authority succeeds where expected and retired emergency authority fails at enumerated consequence-bearing enforcement points. This extends the positive/negative oracle model from 199–208.

If an old emergency credential cannot be enumerated or tested, classify the residual state as `UNKNOWN`, not extinct.

## SYNTHESIS 9 — long-offline PWA clients may miss the entire emergency epoch
A LogMate/EFB-like iPad can be offline before break-glass activation and reconnect only after normal control is restored. It should not need to replay every emergency ceremony to preserve unique local records, but it must not use cached pre-emergency or emergency-era authority as current remote authority.

On reconnect:
1. preserve unique local data;
2. obtain current authenticated authority/security/recovery generation;
3. quarantine stale session/token/management assumptions;
4. re-admit queued consequence-bearing operations under current authority;
5. retain historical uncertainty where the original authorization time cannot be proven.

`client missed emergency epoch ≠ client may remain on pre-emergency authority`.

## SYNTHESIS 10 — break-glass must not become the normal operating path
If emergency privilege is routinely used because normal IAM/MDM/provider workflows are inconvenient, the exceptional path has become de facto production authority without normal controls. Track D telemetry may detect frequency/duration anomalies, but governance must define when repeated use triggers architecture correction.

`rare-account label ≠ rare use`; `break-glass convenience use ≠ valid emergency`.

## Track C destructive campaign — 432 cases total
Add eight cases to the 424-case campaign:
1. one surviving Global/MDM administrator invokes permanent trust reset alone — reject unless pre-governed policy explicitly admits that authority;
2. two approvers exist but both depend on the same compromised IdP/admin plane — do not count nominal multiplicity as independent dual control;
3. required approver unavailable during outage — do not silently lower threshold; use admitted alternate ceremony/degraded mode or block high-consequence action;
4. break-glass grant scoped to provider migration is used to authorize unrelated data export or remote mutation — capability boundary rejects escalation;
5. emergency lease expiry occurs while client/local clock is uncertain — no silent indefinite extension; current server-side evidence required for consequence-bearing use;
6. service is restored but temporary admin role/session/token remains valid — recovery remains `PRIVILEGE CONTRACTION INCOMPLETE`;
7. PITR restores an emergency account/role after contraction — current floor and negative oracle reject resurrection;
8. long-offline company iPad misses the entire emergency epoch and returns with unique records — preserve data, bootstrap current authority, reject pre/emergency stale authority, re-admit queue.

Campaign status: **DEFINED, NOT EXECUTED**.

## Cross-track transfer / contradiction
### A → E
Browser/session/PWA and enterprise identity mechanics constrain activation, expiry and residual sessions, but they do not define recovery constitutional authority.

### E → B
Recovery UX must expose that local data preservation can continue while remote authority is restricted. Do not use reassuring “recovered” language until emergency privilege contraction is complete at the relevant scope.

### E → C
C receives unilateral-reset, correlated-approver, unavailable-approver, scope-escalation, expiry/currentness, residual-session, PITR-resurrection and long-offline-client cases.

### E → D
D may measure break-glass activation count, duration, scope, residual assignments and convergence, but analytics cannot authorize activation or declare extinction by itself.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. This artifact defines state semantics and authority boundaries, not visual treatment. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage. Exact PAM/IdP/MDM/session/token implementation, physical iPad/Safari behavior, secure audit pipeline, runtime expiry and negative-oracle execution remain implementation evidence.

## MINTTAP DECISION / DIRECTION
1. Separate recovery initiation, authorization, exceptional-capability activation, execution, normalization and privilege contraction.
2. Do not allow a single ordinary administrator/support operator or one compromised identity plane to become an implicit permanent trust-reset root.
3. Treat dual/multi-control as failure-domain separation, not merely a count of approvals; exact quorum/topology remains OPEN.
4. Keep break-glass capability least-privileged and purpose-scoped; data preservation, provider migration, trust reset and remote mutation are distinct capabilities.
5. Prefer explicit expiry/currentness and fresh authorization for emergency privilege where implementable; never let time uncertainty silently extend it.
6. Preserve independent-enough audit evidence, but never treat logging as authorization.
7. Make post-recovery privilege contraction a separate gate requiring positive current-authority and negative emergency-authority evidence.
8. Preserve LogMate-like unique local data across emergency epochs and re-admit remote work only under current authority.
9. Keep actual MintTap/LogMate approver policy, PAM/IdP/MDM topology, emergency accounts, quorum, time source, audit architecture and legal/aviation obligations OPEN.

## OPEN / VALIDATION
- actual recovery-ceremony approver roles, quorum and independence;
- actual emergency account/PAM/IdP/MDM capability and lifecycle;
- exact token/session/certificate revocation semantics and convergence;
- trusted-time/currentness basis for emergency leases;
- audit-log isolation, retention and recovery accessibility;
- physical iPad/Safari/PWA behavior across emergency/recovery epochs;
- product-specific data-preservation versus remote-mutation capability map;
- security/privacy/legal/aviation/safety and human validation.

## CHANGE WATCH
- Cloud identity/PAM vendor behavior and emergency-account recommendations are implementation-specific and change-sensitive.
- CISA cloud/Azure guidance is operational precedent, not a MintTap provider decision.
- TUF remains a bounded threshold/recovery precedent, not MintTap architecture.
- NIST SP 800-53 Rev.5 remains the control baseline used for generic emergency-account/separation-of-duties reasoning; implementation profiles must be rechecked at design time.

## VALIDATION / GATE
**PASS (generic).** The Web Manager can now separate recovery request from authorization and execution; reason about dual control as independence rather than approval count; resist emergency threshold weakening; scope break-glass capabilities; preserve audit without confusing it with authorization; and require post-recovery privilege contraction with positive/negative enforcement evidence. Product/runtime validation remains OPEN.

## Next highest-value adjacent question
**210 — recovery-ceremony evidence integrity, approver impersonation/coercion & audit-survivability under control-plane compromise.** Determine how ceremony authorization evidence remains trustworthy when IdP/PAM/admin/logging planes are themselves suspect; how to distinguish approver identity from authorization intent and resist replay/coercion/substitution; how independent-enough evidence survives provider/control-plane loss; and how long-offline clients avoid treating ceremony artifacts as current authority.