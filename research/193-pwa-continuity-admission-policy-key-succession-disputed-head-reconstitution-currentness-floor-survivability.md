# 193 — PWA Continuity-Admission Policy/Key Succession, Disputed-Head Reconstitution & Independent Currentness-Floor Survivability

Status: **PASS (generic) / PRODUCT + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A reconnect/cache/storage mechanics; Track B recovery/currentness UX; Track C destructive validation; Track D privacy-bounded recovery telemetry.
Dependencies: 183–192.

## Problem
192 separated continuity-generation issuance from admission and established that competing valid-looking heads are conflict evidence rather than a majority election. The adjacent bottleneck is higher-order: the policy and keys that authorize admission themselves evolve, and ordinary application/control-plane state may be lost exactly when recovery needs anti-rollback memory most.

Central rule: **A continuity head is current only under an authenticated current admission-policy lineage. Policy/key succession is itself a governed higher-order transition. If disputed history cannot be uniquely resolved, recovery establishes a new explicit reconstitution generation from surviving higher-order evidence without rewriting the disputed interval. Currentness-floor survivability must outlive ordinary control-plane loss without turning custody copies, clients or stale keys into authority.**

## Five-track balance
- A Platform/Browser: browser/SW/Cache Storage/IndexedDB retain observations but do not define currentness.
- B UX/IA/Content: owns policy-transition, dispute, reconstitution, local-safe/remote-paused semantics.
- C Quality: extends destructive validation through policy/key rotation, control-plane loss and long-offline return.
- D Analytics: recovery telemetry is not an authority vote and must remain privacy bounded.
- E Architecture/Security/Operations: **highest-risk owner**; owns policy lineage, key succession, reconstitution and floor survivability.

## SOURCE
### TUF trusted-root succession precedent
The Update Framework root metadata defines trusted keys and thresholds. Root update is sequential and validated against previously trusted root plus successor requirements. Transfer: changing trust-policy/key material is itself an authenticated transition, not an ordinary payload update. TUF is software-update precedent, not a preservation standard.
Sources: https://theupdateframework.io/spec/ ; https://theupdateframework.io/docs/metadata/

### NIST key lifecycle precedent
NIST SP 800-57 Part 1 Rev.5 remains the final general key-management recommendation. It distinguishes key lifecycle states and requires suspected compromise to be handled as compromise with recorded transition/revocation. SP 800-57 Part 1 Rev.6 is an Initial Public Draft dated 2025-12-05 and is CHANGE WATCH only.
Sources: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final ; https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

### RFC 9162 conflicting-view precedent
RFC 9162 recognizes conflicting authenticated tree views as misbehavior evidence and cross-observer comparison as useful detection. It does not define majority authority. Transfer: preserve conflicts through recovery.
Source: https://www.rfc-editor.org/rfc/rfc9162.html

### NIST SP 800-53 recovery/change precedent
SP 800-53 Rev.5 remains a current control catalog; NIST issued Release 5.2.0 on 2025-08-27. Transfer governed change and protected/tested recovery principles only; no MintTap-specific quorum is inferred.
Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

## SYNTHESIS — three lineages
Distinguish:
1. continuity-content lineage — packages/heads and predecessors;
2. admission-policy lineage — which policy generation defines admission;
3. admission-key/role lineage — key/role material permitted by that policy.

Persistent guards:
- `head valid under old policy ≠ head admissible under current policy`;
- `new policy published ≠ new policy admitted/current`;
- `new key exists ≠ new key authorized for admission`;
- `old key verifies history ≠ old key may authorize a new transition`;
- `policy/key rotation complete in primary DB ≠ rollback resistance survives DB loss`;
- `surviving custody copy/client maximum ≠ currentness authority`;
- `reconstitution resumes service ≠ disputed history resolved`;
- `new clean head ≠ disputed/UNKNOWN interval erased`.

## Admission-policy succession
Admission policy is higher-order security state. A successor should bind predecessor policy generation or explicit reconstitution lineage, exact policy identity, allowed roles/key generations, transition rules, retirement boundaries, incident markers and exact admitted generation.

Generic ceremony: prepare exact successor; validate semantics/dependencies; authorize under still-current predecessor higher-order authority unless compromised; validate successor constraints; commit authenticated predecessor→successor record; advance independently survivable policy/currentness floor; measure distribution separately; retire predecessor current-admission capability while retaining bounded historical verification material where needed.

A stale policy restored by PITR must not admit a head rejected by the successor policy.

## Key succession and compromise
Planned rotation and compromise replacement differ. Planned rotation may use authenticated overlap according to policy. A compromised admission key cannot solely authenticate its own successor; reconstitution needs surviving higher-order evidence outside the compromised failure domain. Unbounded compromise intervals remain UNKNOWN. Historical verification does not restore old/compromised keys to current admission capability.

## Dual-policy hazards
Explicitly model P admitted centrally while a region enforces P-1; head H accepted under P but rejected under P-1; P published but not admitted; K+1 distributed before policy authorizes it; independent floor still P-1; PITR restores P-1. Do not accept whichever policy/head looks locally newest.

## Disputed-head reconstitution when no branch wins
If no branch can be uniquely proven legitimate: preserve conflicts; identify last supportable common admitted ancestor; mark divergence UNKNOWN; establish surviving higher-order authority outside the disputed domain; issue an explicit reconstitution policy generation referencing ancestor and unresolved interval; create a reconstituted continuity generation rather than false clean succession; bind current security/deletion/hold/provider constraints; independently persist new floor; resume consequence-bearing recovery only after exact admission; retain historical conflict evidence under valid retention/privacy rules.

Reconstitution is a forward recovery statement and cannot convert historical UNKNOWN to VALID.

## Independent currentness-floor survivability
The ordinary application/control-plane database cannot be the sole anti-rollback memory. A survivable floor should retain authenticated current continuity generation, current admission-policy generation, relevant key/role generation IDs, enough succession binding to reject known stale states, compromise/UNKNOWN/reconstitution markers, applicable deletion/hold/security floors and integrity/authenticity/freshness context.

Independence is failure-domain-specific. A second database under the same IAM/KMS/admin/deletion domain may not survive the intended failure. The floor is rollback memory/evidence, not unilateral business authority; it cannot mint arbitrary new heads.

After primary control-plane loss: freeze consequence-bearing admission; collect independently retained floor/policy/head evidence; preserve conflicts; determine the strongest mutually consistent lower bound supported by valid succession evidence; reconcile higher-order policy/security/deletion/hold evidence; restore uniquely established lineage or enter explicit reconstitution; only then repopulate ordinary control-plane state. Exact quorum/crypto mechanism remains OPEN.

## PWA / EFB boundary
For a company iPad returning after continuity and policy/key generations changed: preserve unique local flight/logbook records; treat cached head/policy/key/SW/IndexedDB as historical observation; obtain current authenticated server state; identify retired/compromised/disputed/reconstituted crossings; update/rebootstrap supported verifier material without lowering server floor; reconcile acknowledged remote history separately from local-only work; submit local-only records under current authority; re-admit consequence-bearing queue only after current authorization/lineage reconciliation. Offline clients never become the sole current-policy floor.

Physical Safari/Home Screen/managed-iPad behavior remains OPEN.

## UX/accessibility and privacy transfer
Recovery UI must distinguish successor policy prepared/published/admitted, key transition pending/current/compromised, regional convergence incomplete, lineage disputed, historical UNKNOWN, reconstitution admitted, floor recovered/reconciled, and local-data-safe/remote-paused. Avoid generic `secure`, `verified`, `latest` and color-only semantics. Human/AT validation remains Design Studio-owned/OPEN.

Telemetry may use coarse policy-generation class, floor-recovery state, convergence bucket and dispute/reconstitution state. Avoid raw evidence payloads, stable device identity and user/flight/location dossiers in analytics.

## Track C destructive campaign
Define a **304-case generic campaign**, extending 192's 296 cases with: stale P-1 PITR admitting H-1; K+1 distributed before authorization; compromised K signing its successor; central P vs regional P-1; independent floor stuck P-1; primary DB and correlated backup rollback while independent floor survives; stale authentic independent floor vs newer valid primary state; incompatible independent policy floors; irreconcilable continuity branches; reconstitution laundering UNKNOWN; floor compaction deleting compromise marker; long-offline iPad presenting never-admitted old-policy head; stale SW treating publication as admission; regional recovery restoring retired key authorization; deletion/hold floor advancing during policy-store outage; operator/AT confusion among published/admitted/reconstituted/UNKNOWN.

Campaign definition is not execution.

## TRANSFER VALIDATION / CONTRADICTION
- TRANSFER VALIDATION: TUF supports authenticated trust-policy/key succession, not wholesale preservation architecture.
- TRANSFER VALIDATION: NIST key lifecycle supports explicit active/deactivated/compromised states, not MintTap ceremonies.
- TRANSFER VALIDATION: RFC 9162 supports retaining conflicting authenticated views, not majority voting.
- TRANSFER VALIDATION: SP 800-53 supports governed change and protected/tested recovery information.
- CONTRADICTION: stale policy does not become current because PITR restored an era when it was current.
- CONTRADICTION: independent storage that can unilaterally mint current heads has become authority and needs separate governance.

## MINTTAP DECISION / DIRECTION
1. Model content, admission-policy and admission-key lineages separately.
2. Make policy/key succession an authenticated higher-order transition with independent anti-rollback memory.
3. Never let compromised admission material solely bless its successor.
4. Preserve disputed/UNKNOWN history through explicit reconstitution.
5. Keep authenticated currentness floor outside ordinary control-plane failure domain, bounded to rollback evidence rather than unilateral authority.
6. Reconcile floor/policy/head evidence before reopening consequence-bearing recovery.
7. Keep long-offline PWA clients non-authoritative while preserving unique local data and rebootstrap paths.
8. Keep topology, thresholds, keys, storage, retention and operator ceremony OPEN pending implementation/provider/legal evidence.

## OPEN / DEPENDENCY / VALIDATION
OPEN: actual MintTap/LogMate policy/key hierarchy; independent floor topology; reconstitution authority; schemas/crypto binding; backup/PITR/deletion/hold integration; managed-iPad behavior; legal/aviation retention; human/AT comprehension.

DEPENDENCY: Software Engineering owns concrete transactions, key/policy persistence, floor implementation, recovery tooling and executable tests. Design Studio owns reusable recovery/currentness/dispute interaction and human validation.

VALIDATION: execute 304-case campaign; simulate planned/compromised policy-key succession; destroy/rollback primary control plane while retaining independent floors; exercise irreconcilable dual-head reconstitution; verify long-offline physical iPad/Safari/Home Screen; verify privacy/accessibility/operator comprehension.

## CHANGE WATCH
TUF root semantics; NIST SP 800-57 Rev.6 draft and SP 800-131A Rev.3 status; SP 800-53 5.x; transparency/witness ecosystem; provider independent-custody semantics; WebKit/iPadOS PWA recovery behavior.

## Gate
**PASS (generic).** Web Manager can separate continuity-content, admission-policy and key lineages; govern policy/key succession without stale-policy rollback; preserve unresolved history through explicit reconstitution; and specify an independently survivable currentness floor that remains rollback evidence rather than a new sole authority. Production certification remains OPEN.