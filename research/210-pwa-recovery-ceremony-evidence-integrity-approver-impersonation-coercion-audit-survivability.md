# 210 — PWA Recovery-Ceremony Evidence Integrity, Approver Impersonation/Coercion & Audit Survivability

Status: **PASS (generic) / PRODUCT + CEREMONY + IDENTITY/PAM + AUDIT + MANAGED-IPAD + RUNTIME + SECURITY/LEGAL + HUMAN VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A identity/browser mechanics; Track B ceremony/recovery UX; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–209, especially 205–209.

## Problem
209 separated recovery request, ceremony authorization, exceptional-capability activation, execution, normalization and privilege contraction. The adjacent failure is evidentiary: the IdP/PAM/admin/logging plane that says “Alice approved recovery X” may itself be compromised, relayed, replayed, substituted, coerced or restored from stale state.

Central rule: **an authenticated approver identity is not by itself evidence that the approver knowingly authorized this exact recovery action under the current policy; an audit record is not trustworthy merely because it exists; and ceremony evidence must survive the failure domains whose recovery it is intended to govern.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. WebAuthn/phishing-resistant authentication, origin/session binding and browser security can strengthen approver authentication but cannot prove organizational authority or absence of coercion.
- **B UX/IA/Content:** very high dependency pressure. Approval surfaces must expose target, scope, consequence, policy generation and exceptional nature sufficiently to support deliberate action; Design Studio owns reusable interaction expertise.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **440 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Analytics/telemetry may detect anomalies but are neither authorization evidence nor an independent audit archive by default.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns evidence binding, replay/substitution resistance, audit isolation/survivability, evidentiary states and recovery admission.

## SOURCE

### NIST SP 800-63B-4 — phishing resistance and authentication intent
Current NIST SP 800-63B-4 distinguishes phishing resistance from authentication intent. Phishing-resistant protocols bind authenticator output to the verifier/channel or verifier name; authentication intent requires explicit claimant intervention for each authentication/reauthentication request.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/
- https://pages.nist.gov/800-63-4/sp800-63b.html

**TRANSFER VALIDATION:** phishing-resistant authentication and explicit user action are useful prerequisites for high-consequence approver authentication. They do not prove that the human understood the requested recovery scope, possessed current organizational authority, or acted without coercion.

### NIST SP 800-53 Rev.5 — audit protection, separation of duties and least privilege
SP 800-53 Rev.5 provides control families for audit/accountability, protection of audit information, separation of duties and least privilege. This supports treating evidence storage/administration as a security boundary rather than assuming the same emergency administrator should be able both to exercise privilege and rewrite the record of that exercise.

Source:
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

**TRANSFER VALIDATION:** independent-enough audit administration and protected audit information are useful generic control precedents. NIST does not prescribe MintTap's ceremony evidence format or storage topology.

### RFC 9162 — append-only consistency and equivocation limits
Certificate Transparency v2 uses Merkle consistency/inclusion proofs to make append-only history auditable. It also explicitly notes that a misbehaving log can show inconsistent views to different clients and that consistency of views must be checked across query sources.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** append-only/consistency evidence is a useful model for detecting deletion, rollback and inconsistent audit views. CT is not MintTap's audit design and a transparent record does not make an unauthorized statement authorized.

### RFC 9943 — transparency records accountability, not issuer honesty
RFC 9943 defines signed statements and transparency receipts over verifiable data structures and explicitly states that transparency does not prevent dishonest or compromised issuers; it makes their statements available for scrutiny/accountability.

Source:
- https://www.rfc-editor.org/rfc/rfc9943.html

**TRANSFER VALIDATION:** a signed/registered ceremony statement can improve provenance and auditability without proving that the signer was legitimate or the decision correct.

## SYNTHESIS 1 — identity, intent, authority and decision content are separate
A defensible approval needs separate answers to at least:
1. **Who authenticated?**
2. **Did that authenticator demonstrate fresh user action/intent?**
3. **Was that identity currently authorized for this ceremony role?**
4. **What exact action did the person approve?**
5. **Was the approval attached to the current request/policy/recovery generation?**
6. **Did the required independent approval policy actually converge before execution?**

`identity authenticated ≠ ceremony authorized`; `authentication intent ≠ recovery intent`; `recovery intent ≠ informed authorization`.

## SYNTHESIS 2 — approval evidence must bind the consequence-bearing statement
A generic “Approve” event or reusable MFA success is too weak for a high-consequence trust reset. Evidence should bind, at the appropriate implementation layer, the recovery request identifier, target authority/resource, requested capability, scope, policy/recovery generation, approver identity/role, relevant evidence digest, freshness/challenge context and decision.

The purpose is to make substitution visible: an approval for “preserve local data” must not be replayable as approval for “replace recovery anchor,” and an approval for Region A must not silently authorize all regions.

`approved a session ≠ approved every action in the session`; `approved request X ≠ approved modified request X′`.

Exact cryptographic encoding is an implementation/security-design dependency, not decided here.

## SYNTHESIS 3 — phishing resistance narrows impersonation risk but does not solve compromised endpoints or authority
Verifier-bound cryptographic authentication can prevent common credential-relay/phishing paths. It does not prove that:
- the approver endpoint/UI is uncompromised;
- the displayed recovery scope matches the server-side action;
- the approver still holds the required organizational role;
- the policy generation is current;
- the approver is acting voluntarily.

Therefore WebAuthn/passkey/PIV-like authentication may strengthen an approver path but must not be promoted into a complete ceremony oracle.

`phishing-resistant authentication PASS ≠ ceremony-integrity PASS`.

## SYNTHESIS 4 — replay resistance needs current ceremony context, not merely a timestamp
A signed approval can remain cryptographically valid after its intended ceremony is retired. Reuse must be constrained by request identity, current policy/recovery generation, target/scope and one-time or otherwise freshness-bound challenge semantics where appropriate.

Local wall-clock timestamps are insufficient because prior work established rollback/time uncertainty. A stale but authentic approval from ceremony R must not authorize R+1 merely because its signature still verifies.

`signature valid ≠ approval current`; `timestamp present ≠ replay impossible`; `old approval authentic ≠ old authority current`.

## SYNTHESIS 5 — substitution resistance requires end-to-end comparison
If the UI displays one request while the enforcement plane executes another, strong authentication only authenticates approval of the wrong representation. The approval representation and the executed operation need a verifiable relationship.

Validation should be able to detect changes in target, privilege/capability, affected cohort/region, successor anchor/policy, destructive side effects and expiry/currentness assumptions between approval and execution.

`secure approval UI ≠ secure execution binding`.

## SYNTHESIS 6 — coercion is not solved by cryptographic authentication
A valid cryptographic action can be made by a real authorized person under coercion, social pressure or deceptive organizational context. Generic technical evidence cannot prove free human consent.

Do not claim “not coerced” from MFA, biometric use, physical presence, camera evidence or audit completeness. Where coercion risk materially matters, governance may use independent approvers, role separation, delayed/high-friction execution, escalation/duress procedures or post-event review, but exact controls require organizational/security/legal validation.

`real approver ≠ voluntary approver`; `user presence ≠ informed consent`; `two signatures ≠ no coercion`.

## SYNTHESIS 7 — audit plane must not share all failure modes with the authority it audits
If the same emergency administrator can execute a trust reset, delete/replace its audit trail, restore a pre-event database and control every independent copy, the audit record cannot provide strong survivability evidence.

Evaluate audit independence across:
- identity/admin authority;
- write/delete privilege;
- storage/backup/PITR;
- signing/key custody;
- provider/account ownership;
- region/network path;
- deployment/configuration plane;
- monitoring/verification path.

Independence is a failure-domain property, not a vendor-count property.

`separate log bucket ≠ independent audit plane`; `different provider ≠ independent administration`.

## SYNTHESIS 8 — append-only/transparency mechanisms improve tamper evidence, not authorization
Append-only logs, signed checkpoints, receipts or consistency proofs can make deletion/rollback/equivocation easier to detect. They do not establish that the underlying recovery was authorized. A compromised approver can sign a false/unauthorized statement; a transparency service can faithfully preserve it.

`tamper-evident ≠ authorized`; `transparent ≠ truthful`; `receipt verifies ≠ ceremony legitimate`.

This preserves the earlier provenance distinction between integrity, authenticity, completeness and semantic legitimacy.

## SYNTHESIS 9 — audit survivability needs recovery semantics
After IdP/PAM/provider/control-plane compromise or PITR, ceremony evidence should be classifiable rather than flattened into “logs available/unavailable.” Useful states include:
- `CURRENT-VERIFIED` — lineage/currentness and integrity established;
- `HISTORICAL-VERIFIED` — authentic historical evidence, not current authority;
- `PARTIAL` — known missing interval/field/source;
- `FORKED` — incompatible valid-looking views exist;
- `UNVERIFIABLE` — evidence exists but required verification context is absent;
- `UNKNOWN` — absence/completeness cannot be established.

`log restored ≠ audit history complete`; `cannot verify ≠ proven false`; `one consistent copy ≠ no competing copy`.

## SYNTHESIS 10 — ceremony evidence should outlive ordinary control-plane loss without becoming a super-root
Evidence survivability does not require the audit system to authorize recovery. The audit plane should be able to preserve/check statements without gaining power to issue successor anchors, lower quorum or resume consequence-bearing mutation.

This preserves separation between **authorization plane** and **evidence plane**.

`can prove what happened ≠ can authorize what happens next`.

## SYNTHESIS 11 — long-offline PWA clients consume current authority, not ceremony artifacts
A LogMate/EFB-like iPad may miss the entire ceremony and reconnect after normal control is restored. It should not be required to understand raw approver evidence to preserve unique records, and a cached/downloaded ceremony receipt must not itself authorize remote mutation.

Reconnect order remains:
1. preserve unique local records;
2. obtain current authenticated authority/security/recovery generation;
3. quarantine stale session/Service Worker/management assumptions;
4. re-admit queued consequence-bearing operations under current authority;
5. preserve historical uncertainty where original authorization cannot be proven.

`ceremony artifact present ≠ client authority current`; `audit receipt ≠ synchronization credential`.

## SYNTHESIS 12 — evidence privacy/minimization remains a separate constraint
High-integrity audit does not justify retaining every recovery payload, personal attribute, biometric or sensitive local record. Preserve the minimum evidence needed to establish decision provenance, scope, policy/currentness and post-recovery contraction, with retention/access governed separately.

`auditability required ≠ retain every payload forever`.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. treat approver authentication, authentication intent, organizational authority, recovery intent and execution binding as separate properties;
2. require high-consequence approval evidence to bind exact request/scope/capability/current policy context rather than reusable generic MFA success;
3. do not infer absence of coercion from technical authentication evidence;
4. protect ceremony evidence from the same emergency privilege/failure domain where feasible and explicitly record residual correlation;
5. use append-only/transparency concepts only as integrity/accountability mechanisms, never as authorization oracles;
6. preserve explicit `PARTIAL`, `FORKED`, `UNVERIFIABLE` and `UNKNOWN` evidence states;
7. keep audit/evidence authority unable to mint recovery authority merely because it survived;
8. keep long-offline PWA recovery dependent on current server authority, not replayed ceremony artifacts;
9. preserve unique local operational data before trust repair/destructive client remediation.

No product-specific authenticator, PAM, audit vendor, threshold, cryptographic envelope, retention period or MDM topology is selected.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
Supply exact browser/WebAuthn/session/origin and managed-iPad authentication mechanics. Do not infer constitutional recovery authority from browser authentication success.

### Track B — DEPENDENCY
Define comprehensible ceremony states and approval representations that expose target/scope/consequence/currentness. Consume Design Studio interaction evidence; do not duplicate reusable interaction-design research.

### Track C — VALIDATION
Destructive campaign grows **432 → 440 defined cases**:
1. phished/replayed approver credential attempts modified recovery request;
2. phishing-resistant approver authenticates but compromised UI substitutes target before execution;
3. authentic approval from ceremony R is replayed into R+1;
4. same approver identity has lost organizational role but IdP credential remains valid;
5. two valid approver signatures originate from one compromised administrative/failure domain;
6. audit DB and PAM are restored to pre-ceremony PITR while independent checkpoint indicates later history;
7. primary audit store shows one view while surviving verifier/monitor holds an incompatible valid-looking view;
8. long-offline iPad reconnects carrying cached ceremony receipt and stale pre-recovery session.

Execution, physical iPad/Safari, IdP/PAM, secure-audit, AT and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Telemetry may detect unusual approver frequency, repeated recovery use, duration or missing events. It is observation only; analytics cannot prove authorization, voluntary intent, evidence completeness or privilege extinction.

## Persistent guards added through 210
- `identity authenticated ≠ ceremony authorized`;
- `authentication intent ≠ recovery intent`;
- `recovery intent ≠ informed authorization`;
- `phishing-resistant authentication PASS ≠ ceremony-integrity PASS`;
- `approved request X ≠ approved modified request X′`;
- `signature valid ≠ approval current`;
- `timestamp present ≠ replay impossible`;
- `secure approval UI ≠ secure execution binding`;
- `real approver ≠ voluntary approver`;
- `user presence ≠ informed consent`;
- `two signatures ≠ no coercion`;
- `separate log bucket ≠ independent audit plane`;
- `tamper-evident ≠ authorized`;
- `transparent ≠ truthful`;
- `receipt verifies ≠ ceremony legitimate`;
- `log restored ≠ audit history complete`;
- `can prove what happened ≠ can authorize what happens next`;
- `ceremony artifact present ≠ client authority current`;
- `audit receipt ≠ synchronization credential`.

## OPEN
- actual MintTap/LogMate approver roles, quorum and failure-domain independence;
- exact IdP/PAM/authenticator/WebAuthn/MDM implementation;
- trusted-display/transaction-confirmation feasibility;
- audit store/signing/checkpoint/monitor topology;
- evidence retention/privacy/legal/aviation requirements;
- coercion/duress organizational procedure;
- physical iPad/Safari/PWA behavior and runtime tests;
- exact ceremony/execution binding representation;
- independent recovery/audit drills and human validation.

## CHANGE WATCH
- NIST SP 800-63-4 authentication/phishing-resistance guidance;
- WebAuthn/browser/platform authenticator behavior;
- NIST/CISA privileged-access and audit guidance;
- transparency-log standards and operational practice;
- Apple managed-device identity/provisioning behavior where used.

## Gate result
**210 PASS (generic).** The Web Manager can now distinguish approver identity, authentication intent, recovery authorization intent, action binding, replay/substitution resistance, coercion limits, audit integrity, audit survivability and transparency/accountability without turning any one into a universal oracle.

Production validation remains OPEN.

## Next highest-value adjacent question
**211 — recovery-evidence retention/key succession, verifier survivability & post-compromise evidentiary admissibility.** Determine how ceremony evidence remains verifiable after audit-signing key rotation/compromise, provider migration, verifier/software retirement and long retention; how to preserve historical verification without letting retired evidence keys authorize new recovery; how to classify evidence around uncertain compromise windows; and how restored/offline clients consume only current authority while investigators retain historical evidence.