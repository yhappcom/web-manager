# 241 — PWA Repair-Approval Credential Compromise, Delegation/Succession & Governance-Root Recovery

Status: **PASS (generic) / PRODUCT + GOVERNANCE + IDENTITY + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A trust-generation/runtime evidence; Track B recovery/delegation UX; Track C destructive validation; Track D governance-transition observability.  
Dependencies: 223–240, especially recovery custody/bootstrap, rotation/succession, monotonic admission floors, topology repair, repair authorization and governance-policy currentness.

## Problem
240 made topology repair a governed versioned transition. The adjacent failure is compromise or succession of the governance authority itself. An approver credential can be stolen while the human remains legitimate; a role can be transferred while old sessions/recovery paths remain live; a delegate can exceed scope; a pending proposal can straddle an authority change; or enough governance-root authority can be compromised that ordinary in-band succession is no longer trustworthy. Long-offline PWA clients can then return with a valid but obsolete governance generation.

Central rule: **governance identity, credential, role, delegation, quorum and root are separate lifecycle objects. Rotation must retire latent predecessor reach, delegation is least-scope and non-transitive unless explicitly authorized, pending approvals are bound to governance generation, and suspected root/quorum compromise cannot be healed merely by letting that same compromised authority certify its successor. Offline clients authenticate successor lineage or enter bootstrap recovery; they never use stale local governance to roll the system backward.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Supplies client trust/governance generation, session/token state and stale acceptance observations; browser possession does not prove current governance authority.
- **B UX/IA/Content:** high dependency pressure. Owns clear `CREDENTIAL-SUSPECT`, `DELEGATION-EXPIRED`, `APPROVAL-STALE`, `GOVERNANCE-RECOVERY`, `BOOTSTRAP-REQUIRED` and data-preserving recovery states; consumes Design Studio evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight succession/delegation/root-recovery destructive cases; campaign expands **680 → 688 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures credential/delegation age, approval invalidation, succession latency and emergency recovery use; telemetry cannot establish authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns credential/role lifecycle, delegation semantics, governance generation, quorum/root recovery, pending-proposal invalidation and recovery closure.

## SOURCE

### NIST SP 800-57 Part 1 Rev.5 — key lifecycle, compromise and recovery
NIST SP 800-57 Part 1 Rev.5 remains the current final general key-management recommendation. It covers authorization, authentication, key recovery, compromise, trust anchors and key lifecycle. NIST's key-management project lists Rev.5 as final while Rev.6 remains an Initial Public Draft.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/Projects/Key-Management/Key-Management-Guidelines
- https://csrc.nist.gov/glossary/term/key_recovery

**TRANSFER VALIDATION:** cryptographic-key lifecycle is bounded precedent for governance signing/recovery credentials where cryptography is actually used. It does not define MintTap's personnel roles, quorum or provider recovery topology.

### NIST IR 8587 — token/assertion protection and lifecycle
NIST finalized IR 8587 on 2026-09-15. It addresses protection of identity tokens/assertions against forgery, theft and misuse, including architectural, key-management, token-verification and lifecycle controls for SSO, federation, APIs and workload access.

Sources:
- https://csrc.nist.gov/news/2026/protecting-tokens-and-assertions-nist-ir-8587
- https://csrc.nist.gov/pubs/ir/8587/final

**TRANSFER VALIDATION:** this strengthens the requirement to treat approver sessions/tokens/assertions as revocable lifecycle objects rather than equating account ownership with current authority. Exact MintTap identity architecture remains OPEN.

### TUF — delegation and root compromise recovery precedent
TUF permits delegated roles to delegate full or partial target trust. Its compromise guidance says compromised role keys are revoked/replaced through Root, while compromise of a threshold of Root keys requires Root metadata to be re-issued out of band.

Sources:
- https://theupdateframework.io/docs/faq/
- https://theupdateframework.io/spec/

**TRANSFER VALIDATION:** TUF is update-security precedent, not the MintTap governance protocol. We transfer scoped delegation, threshold-root distinction and out-of-band recovery principle, not its exact metadata model.

## SYNTHESIS 1 — separate person, account, credential, role and governance authority
A legitimate employee can have a stolen token; a valid account can hold an obsolete role; a role can be current while one recovery credential is compromised. Model at least:
- human/service principal identity;
- account/federated identity;
- active credential/session/token/assertion;
- governance role and scope;
- delegation grant;
- governance-policy/root generation.

Persistent guards: `person still employed ≠ credential uncompromised`; `account enabled ≠ approval role current`; `signature valid ≠ signer currently authorized`.

## SYNTHESIS 2 — credential compromise requires consequence fencing, not merely password reset
When an approval credential is suspected stolen, invalidate or fence consequence-bearing sessions/tokens/assertions and approval capability according to actual architecture. Rotate/recover credentials and inspect approvals produced during the suspect interval. Do not assume changing a password invalidates all provider sessions, API tokens, workload identities, recovery paths or cached assertions.

A credential incident does not automatically prove the human approver malicious. Preserve attribution uncertainty while constraining the compromised capability.

## SYNTHESIS 3 — succession must retire predecessor reach, including latent recovery
Changing the role directory from Alice to Bob is insufficient if Alice retains PAM recovery, hardware token, provider-admin recovery, delegated grant, API credential or long-lived session that can still approve repair.

Succession closure requires successor establishment plus predecessor negative retirement at the relevant consequence boundary. `role assignment changed ≠ predecessor authority extinct`.

## SYNTHESIS 4 — delegation is scoped authority, not identity cloning
A delegation records delegator authority generation, delegate, exact action/resource/consequence scope, validity interval/conditions, re-delegation permission and revocation/currentness state. Delegated authority cannot exceed the delegator's current scope and should not become transitively re-delegable by implication.

`delegate can approve X ≠ delegate inherits all approver powers`; `delegation exists ≠ re-delegation allowed`; `parent authority revoked ≠ child delegation remains automatically valid`.

## SYNTHESIS 5 — composition must be evaluated at the consequence, not grant count
Two narrow delegations can combine into a dangerous effective capability even if each appears safe alone—for example one grant permits topology proposal and another permits emergency publication. Evaluate effective privilege and shared recovery/admin dependencies across composed grants.

Do not infer separation from different role labels when one principal or one recovery plane can exercise both.

## SYNTHESIS 6 — pending approvals bind to governance generation
A proposal approved under governance G7 must not silently publish after transition to G8 if the approver set, threshold, delegation, recovery topology or credential trust materially changed. Re-evaluate or re-approve under the current governance generation.

A factual proposal can remain useful evidence even when its authorization becomes stale. `approval stale ≠ proposal factually false`; `proposal factually sound ≠ stale approval publishable`.

## SYNTHESIS 7 — ordinary root rotation and compromised-root recovery are different ceremonies
If the current governance root/quorum remains trusted, it may authorize a planned successor under defined rotation rules. If enough root/quorum authority is suspected compromised to satisfy the normal transition threshold, allowing that same authority to certify its successor creates attacker-controlled continuity.

The recovery basis must be independent of the suspected cut: e.g. separately governed offline recovery authority, pre-established recovery threshold or other product-specific bootstrap mechanism. The exact mechanism is OPEN and must be threat-modelled before implementation.

Persistent guard: `predecessor can normally rotate successor ≠ compromised predecessor may self-heal`.

## SYNTHESIS 8 — loss of quorum is not permission to lower quorum silently
If required approvers are unavailable or credentials are irrecoverably lost, availability pressure does not redefine the normal threshold. Use a separately defined recovery/emergency basis, record assurance debt and re-establish normal governance before treating the state as ordinary.

`quorum unavailable ≠ smaller quorum satisfied`; `emergency recovery succeeded ≠ normal governance restored`.

## SYNTHESIS 9 — successor governance requires monotonic currentness
Governance root/policy generations need anti-rollback state just like topology generations. A valid old G7 signature must not override G9 merely because its cryptography still verifies. Intentional policy rollback is a new successor generation whose content restores a prior policy, not resurrection of the old generation.

Restore/PITR and disaster-recovery environments must reacquire the current governance floor before consequence-bearing publication.

## SYNTHESIS 10 — offline PWA clients consume governance lineage; they do not hold governance authority
A LogMate-like iPad may leave under G7 and return under G11. Preserve unique flight/logbook data and stale governance/trust evidence. Quarantine consequence-bearing replay, authenticate the supported successor lineage or enter `BOOTSTRAP-REQUIRED`, migrate worker/schema/policy as needed, then re-admit operations under current policy.

A stale device can reveal that an obsolete credential/root is still accepted, reopening a server/fleet claim. It cannot vote G7 back into force. Physical iPadOS/WebKit/MDM behavior remains OPEN.

## SYNTHESIS 11 — governance recovery closure needs independent negative evidence
After succession or root recovery, validate that retired credentials, sessions, delegations, recovery routes and old governance generations cannot produce current consequence. Where possible, the only oracle should not be controlled by the exact identity/admin plane suspected compromised.

Positive successor acceptance is insufficient without negative predecessor rejection for high-consequence transitions.

## SYNTHESIS 12 — retention must preserve why authority changed without preserving live authority
Retain minimum non-secret lineage: governance generations, role/delegation identifiers, scopes, approvals, revocations, incident/recovery reason, successor relation and validation evidence. Do not retain private signing material merely to preserve historical auditability.

Historical verification support and current signing/approval authority remain separate.

## MINTTAP DECISION
For future MintTap/LogMate repair governance, treat approver identity as a layered lifecycle: principal → credential/session → role → delegation → governance generation. Credential compromise fences consequence capability and triggers review of approvals in the suspect interval. Succession requires successor establishment and negative retirement of predecessor reach, including latent recovery/session paths.

Delegation is explicit, scoped, time/currentness bound and non-transitive unless expressly permitted. Pending approvals are bound to governance generation and are re-evaluated after material succession. Planned root rotation may use trusted predecessor authority; suspected threshold/root compromise requires a separately governed recovery/bootstrap basis rather than self-certification by the compromised predecessor.

This is generic direction, not a claim that MintTap or LogMate currently implements such governance.

## DEPENDENCY / TRANSFER
- **Track A:** expose exact session/token/trust/governance generation and stale acceptance; do not infer global authority from one browser/device.
- **Track B:** design understandable credential-suspect, delegation-expired, approval-stale and bootstrap/recovery states without destructive data loss.
- **Track C:** own credential/session retirement, delegation composition, stale approval, root-compromise and offline-client destructive tests.
- **Track D:** observe transition latency/concentration without deciding authority.
- **Software Engineering:** typed authority/delegation state, token/session revocation, generation binding, threshold/recovery implementation and fault injection are implementation handoffs after product authorization.

## CONTRADICTION / FAILURE MODES
1. **Password-reset theater:** stolen long-lived session/API token still approves after password reset.
2. **Latent predecessor:** former approver removed from role list but PAM/provider recovery still restores approval capability.
3. **Delegation widening:** narrow delegate silently gains all parent privileges or re-delegates without authorization.
4. **Composition escalation:** individually narrow grants combine into propose+approve/publish consequence.
5. **Stale pending approval:** G7-approved proposal publishes after G8 governance change without re-evaluation.
6. **Compromised-root self-heal:** suspected threshold root signs its own successor and system calls continuity restored.
7. **Quorum-collapse convenience:** unavailable approver causes normal threshold to be silently lowered.
8. **Offline-client governance rollback:** authentic stale iPad state revives G7 or is erased to hide stale-authority evidence.

## Track C destructive additions — 680 → 688 defined cases
Add eight cases corresponding to the failure modes above. Required oracle behavior:
- revoke/fence all relevant consequence-bearing credentials, not only passwords;
- prove predecessor negative retirement across recovery/admin paths;
- enforce delegation scope/re-delegation/currentness;
- evaluate composed effective privilege;
- bind approval to current governance generation;
- require independent recovery basis when normal root/quorum is suspected compromised;
- reject silent quorum reduction;
- preserve offline unique data/evidence while rejecting governance rollback.

**VALIDATION:** these are **defined cases**, not execution PASS. Actual product identity provider, PAM/provider recovery, governance signing/quorum, MDM, physical iPad/iPadOS/WebKit and runtime execution remain OPEN.

## OPEN
- Actual MintTap/LogMate identity provider, session/token types, approver roles, delegations and recovery topology are unknown.
- Actual governance root/quorum and whether cryptographic threshold signing is appropriate are unknown.
- Actual emergency/loss-of-quorum recovery basis is unknown.
- Actual token/session revocation propagation and provider/PAM recovery behavior are unknown.
- Physical iPadOS/WebKit/MDM stale-governance/bootstrap behavior remains unvalidated.
- Legal/aviation/safety requirements may impose stronger separation, retention or ceremony requirements.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev.5 remains current final; Rev.6 Initial Public Draft remains change watch.
- NIST IR 8587 was finalized 2026-09-15 and is now current token/assertion protection guidance relevant to identity lifecycle.
- TUF remains useful bounded precedent for delegation/root compromise recovery, not a MintTap protocol dependency.
- Identity-provider, PAM, provider, MDM and browser/OS behavior remain implementation-specific and require current validation.

## Gate judgment
**PASS (generic).** The adjacent competency is closed when Web Manager can separate principal/credential/role/delegation/root; fence compromised approval credentials; rotate roles without latent predecessor reach; constrain delegation and composed privilege; invalidate stale approvals across governance succession; distinguish planned rotation from compromised-root recovery; reject silent quorum collapse; and safely rejoin long-offline PWA clients without governance rollback or local-data destruction.

Production certification is not claimed.