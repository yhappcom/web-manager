# 182 — PWA Recovery-Policy Reconstitution, Governance-Key Rotation & Constitutional Change Control

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + ORGANIZATIONAL + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A policy/currentness/reconnect mechanics; Track B constitutional-change/degraded-state UX; Track C destructive change-control validation; Track D privacy-bounded policy-generation telemetry.
Dependencies: 176–181 brownout/exception governance, break-glass assurance, trust reconstitution, organizational succession, ceremony liveness and deadlock-safe governance.

## Problem
181 established that ordinary recovery cannot safely solve loss of the authority that defines recovery itself. The adjacent problem is constitutional: who may change the rules that define eligible recovery actors, quorum/independence constraints, successor trust, emergency powers and policy-reconstitution authority?

A mutable recovery policy controlled by the same administrator or failed quorum it governs creates self-authorization. An immutable policy creates permanent deadlock under legitimate organizational succession, compromise or cryptographic transition.

Central rule:

> **Recovery-policy change is a higher-order authority transition, not an ordinary configuration edit. The authority that proposes, approves, signs/publishes, admits and exercises a successor constitutional policy must be separated enough that a compromised current administrator, failed quorum or obsolete governance key cannot unilaterally weaken its own successor rules. Planned rotation and compromise reconstitution are distinct ceremonies; policy generations move forward and stale/offline clients never become constitutional oracles.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. HTTP/cache/SW/IndexedDB/session/currentness mechanics explain how stale policy can persist, but browser state cannot authorize a constitutional transition.
- **B UX/IA/Content:** high-pressure consumer. Must distinguish ordinary recovery, constitutional-policy change pending, local work preserved, privileged submission paused, successor policy admitted and queued work awaiting re-admission without exposing governance topology.
- **C Performance/Accessibility/Quality:** high-pressure validator. Owns rollback, split-view, partial rollout, dual-generation, key-transition, inaccessible ceremony and long-offline-client destructive cases.
- **D Search/Discovery/Analytics:** bounded consumer. Observe policy generation/admission/convergence with low-cardinality telemetry; never publish custodian graphs, key material, approval topology or incident dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns constitutional authority boundaries, governance-key lifecycle, change control, anti-self-authorization, compromise transition, rollback resistance and enforcement proof.

## SOURCE
### NIST SP 800-53 Rev. 5 / Release 5.2.0 — controlled system change
CM-5 requires defined, documented, approved and enforced access restrictions for changes. CM-5(4) provides dual authorization as an available control enhancement for selected changes; CM-3/related controls cover controlled configuration change and post-change review/verification. These controls support treating security-significant policy mutation as governed change rather than ordinary administrator convenience.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** NIST does not prescribe a MintTap/LogMate constitutional quorum or mandate dual authorization for this product. It supports the generic requirement that security-significant changes have explicit authorization, accountability and verification.

### NIST SP 800-57 Part 1 Rev. 5 — key lifecycle and compromise
Current final Part 1 Rev. 5 provides general key-management guidance covering key lifecycle, compromise, recovery, trust anchors, metadata and protection requirements. Governance-signing/recovery keys therefore require lifecycle treatment distinct from the policy semantics they authenticate.

Source: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**CHANGE WATCH:** SP 800-57 Part 1 Rev. 6 remains an Initial Public Draft published 2025-12-05; its comment period closed 2026-02-05. It includes new quantum-resistant algorithms and revised keying-material guidance but is not the final authority used here.
Source: https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

### NIST SP 800-57 Part 2 Rev. 1 — organizational key-management policy
Part 2 identifies policy, planning, Key Management Specification and Key Management Practice Statement requirements for organizations. This supports treating governance-key ownership and lifecycle as an organizational policy problem, not only a cryptographic API problem.
Source: https://doi.org/10.6028/NIST.SP.800-57pt2r1

### NIST SP 800-131A Rev. 2 — planned cryptographic transition
NIST explicitly treats transitions to stronger algorithms/key lengths as planned lifecycle work. This supports separating routine/planned governance-key or algorithm migration from emergency compromise reconstitution.
Source: https://doi.org/10.6028/NIST.SP.800-131Ar2

## SYNTHESIS — constitutional state is not ordinary configuration
Keep separate:
1. **policy semantics** — eligibility, quorum, independence, emergency/recovery rules;
2. **policy generation** — monotonic identity/version of those semantics;
3. **governance authority** — who may authorize a successor generation;
4. **governance key/material** — cryptographic means used to authenticate approved policy artifacts;
5. **publication** — successor artifact becomes available;
6. **regional admission** — a region accepts the generation as eligible for enforcement;
7. **runtime enforcement** — consequence paths actually enforce it;
8. **client observation** — never constitutional authority;
9. **historical verification** — ability to verify old decisions without granting old policy current authority.

Persistent guards:
- `policy administrator can edit file ≠ administrator may redefine its own authority`;
- `current quorum approves successor ≠ successor is legitimate after current quorum compromise`;
- `new governance key generated ≠ successor policy authorized`;
- `new key signed by old key ≠ safe transition if old key is compromised`;
- `dual signatures present ≠ approval domains independent`;
- `policy published ≠ every region enforces it`;
- `region admits successor ≠ old sessions/queues automatically inherit it`;
- `historical policy verifies ≠ historical policy remains executable`;
- `rollback restored signed old policy ≠ constitutional rollback authorized`;
- `client cached newer policy ≠ client is authority oracle`;
- `offline client missed generations ≠ intermediate weak policy may be replayed`;
- `algorithm/key rotation ≠ semantic policy change`;
- `semantic policy change ≠ cryptographic migration required`;
- `organizational successor exists ≠ predecessor governance credential inherited`.

## Constitutional change classes
Treat at least these as different change classes:

### 1. Ordinary non-constitutional configuration
Does not change who may create/approve/recover privileged authority. It remains subject to normal configuration controls.

### 2. Planned constitutional policy change
Examples: approved organizational restructuring, new eligible role class, revised independence requirement, retirement of a recovery provider. Requires explicit successor-generation authorization and validation before enforcement.

### 3. Planned governance-key rotation / crypto migration
Policy semantics may remain identical while authenticating key/algorithm changes. Maintain authenticated lineage and an overlap/transition design appropriate to the actual implementation. Do not infer a generic overlap duration.

### 4. Compromise reconstitution
If current governance authority/key may be compromised, it cannot be the sole basis for trusting its successor. Use surviving independent recovery/reconstitution authority established outside the compromised failure domain. Planned rotation rules are insufficient evidence by themselves.

### 5. Organizational/legal succession
A successor organization or custodian becomes eligible through a new governed event; possession of predecessor domains, billing accounts, devices or credentials is not constitutional proof.

## Anti-self-authorization boundary
The system must not allow one actor/failure domain to perform the full chain `declare constitutional need → change eligibility/threshold → approve change → publish/sign → admit → exercise newly created privilege` unless real product governance explicitly accepts that concentration with evidence.

Generic design requirements:
- separate policy-authoring convenience from authorization to create a successor generation;
- bind approvals to the exact policy artifact/generation or canonical digest, not a mutable label;
- verify approver eligibility and independence under the correct governing generation;
- prevent a policy from silently redefining the rules used to validate its own creation;
- make constitutional transitions auditable without turning logs into a second authority plane;
- preserve an independently governed compromise path where continuity requirements demand survival of governance-key/current-policy compromise;
- fail to `UNKNOWN/PAUSED` rather than infer legitimacy when governing lineage cannot be established.

## Governance-key rotation
A governance key authenticates an approved policy artifact; it does not create policy legitimacy by itself.

Planned rotation:
- establish new key/material under current legitimate governance;
- bind new key to a forward policy/key generation;
- provide enough verifier transition for controlled enforcement domains;
- retire old signing authority for new policy artifacts while retaining only the historical verification capability actually required;
- prove regional enforcement/currentness before relying on the successor generation.

Compromise:
- freeze reliance on the suspect key for new constitutional authority;
- do not accept `old compromised key signs new key` as sole successor proof;
- reconstitute through surviving independent authority/evidence;
- invalidate/re-evaluate old sessions, pending ceremonies and queued privileged operations according to actual semantics;
- reconcile restored regions/PITR against the surviving forward security floor.

No product key type, HSM, threshold signature, quorum number or cryptoperiod is selected here.

## Policy generation, rollback and split view
Constitutional policy must be forward-moving at the authority layer. A backup, cache or valid historical signature cannot lower the current generation.

Required generic properties:
- authoritative generation/currentness floor independent of client caches;
- detection/reconciliation of regions enforcing different generations;
- no automatic rollback to an older easier quorum after deployment/PITR;
- no queue admission merely because an operation was authored under an older policy;
- historical artifacts remain distinguishable from current executable policy;
- split view is an incident/reconciliation condition, not automatic proof of attack;
- enforcement proof is scoped to controlled server/region domains rather than impossible claims that every offline client is current.

## PWA / EFB transfer
For a LogMate-like company-iPad PWA:
- local flight/logbook records and drafts remain usable while constitutional authority is unresolved;
- Service Worker, Cache Storage, IndexedDB, cookies and client clocks may retain old policy observations but cannot authorize or veto a successor constitutional generation;
- a long-offline iPad may skip multiple policy/key generations; reconnect should obtain the current server security/policy floor rather than replay every historical generation as executable state;
- queued privileged work is re-admitted under current server authority before remote consequence;
- application/SW/schema migration, data reconciliation, authentication/session recovery and constitutional-policy migration are separate state machines;
- no claim is made that iPadOS background execution, push, MDM, Shared iPad or direct device-to-device communication can distribute policy. Physical Safari/Home Screen/managed-device validation remains OPEN.

## UX transfer — Track B
Required semantics include:
- `Security governance is being restored; privileged remote actions are paused.`
- `Your local work remains saved on this device.`
- `A current governance policy has been established; pending actions will be checked before submission.`

Do not expose quorum thresholds, custodian identities, key identifiers or recovery topology to ordinary users. Do not imply that app update completion means governance recovery completion. Accessibility, focus, screen-reader, non-color state and human comprehension remain OPEN.

## Track C destructive campaign
Define a **216-case generic campaign** spanning:
- policy administrator self-authorizes broader policy power;
- current quorum lowers its own threshold;
- compromised quorum signs weaker successor;
- compromised governance key signs successor key;
- planned rotation incorrectly treated as compromise recovery;
- compromise recovery incorrectly treated as routine rotation;
- same human controls two nominal approval identities;
- same IdP/admin controls nominally independent approvers;
- approval binds mutable policy name rather than exact artifact;
- policy artifact changes after approval;
- valid signature on unauthorized policy;
- new key generated but not authorized;
- old key remains able to sign new policy after retirement;
- historical verifier accidentally admits old policy as current;
- region A admits G+1 while region B enforces G;
- rollback/PITR restores easier G-1;
- CDN/cache serves old signed policy;
- telemetry reports new generation while enforcement remains old;
- governance/evidence plane outage yields false green;
- organizational successor inherits predecessor credential;
- provider/domain/billing ownership mistaken for governance authority;
- long-offline iPad skips generations;
- stale SW/IndexedDB shows obsolete constitutional state;
- client clock/currentness tampering;
- queued operation authored under G drains under G+2 without re-admission;
- local operational data deleted because governance is unresolved;
- inaccessible constitutional-recovery status;
- screen-reader ambiguity;
- human mistakes app update for security-policy recovery;
- recovery succeeds but old key/session/pending ceremony remains executable.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat recovery-policy change as higher-order constitutional authority, not ordinary configuration.
2. Separate policy semantics, policy generation, governance authority, governance key, publication, admission and enforcement.
3. Prevent the current administrator/failed quorum/compromised root from unilaterally authorizing weaker successor rules.
4. Bind approval to the exact successor artifact/generation and validate approver eligibility/independence under the correct governing policy.
5. Separate planned key/algorithm rotation from compromise reconstitution.
6. Require independent surviving authority/evidence when the current governance root is compromised.
7. Make constitutional generations forward-moving and rollback/PITR resistant at the authority layer.
8. Preserve historical verification without granting historical policy current execution authority.
9. Treat multi-region split view as a reconciliation/incident state and prove actual enforcement before reopening consequence paths.
10. Preserve unique local PWA/EFB work while constitutional authority is unresolved; re-admit remote queued consequences under current server authority.
11. Keep policy-generation telemetry privacy-bounded and non-authoritative.
12. Do not select product quorum, key type, HSM, algorithm, cryptoperiod, overlap window or legal succession mechanism without canonical evidence.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate policy administrator, constitutional authority, quorum, recovery root, provider/IdP, key architecture and legal entity: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad/offline runtime: **OPEN**.
- Exact policy canonicalization/signature, key storage, server admission, generation/currentness, queue, rollback and multi-region implementation: **Software Engineering/security dependency**.
- Legal/aviation/investment obligations and organizational succession: **OPEN**.
- Screen-reader/representative-human comprehension: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev. 5 remains the current final baseline used here.
- Rev. 6 is still an Initial Public Draft as of this study; track its finalization and resulting PQC/key-management changes.
- Browser/iPadOS capability support remains separately change-sensitive; no constitutional authority is delegated to client capability behavior.

## Adjacent next target
Highest-value adjacent Stage-8/PWA question: **constitutional-policy supply-chain authenticity, build/publish separation & transparency/equivocation evidence** — how an approved policy becomes an exact deployable artifact without CI/CD, signing, CDN or operator substitution; how multiple regions/observers detect competing valid-looking policy artifacts; and how PWA/offline clients consume current policy observations without becoming trust anchors.