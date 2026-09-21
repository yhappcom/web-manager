# 194 — PWA Reconstitution-Authority Succession, Independent-Floor Poisoning & Policy-Floor Convergence

Status: **PASS (generic) / PRODUCT + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A reconnect/cache/storage mechanics; Track B recovery/convergence UX; Track C destructive validation; Track D privacy-bounded recovery telemetry.
Dependencies: 183–193.

## Problem
193 established three distinct lineages (continuity content, admission policy, admission key/role), explicit disputed-head reconstitution and an independently survivable currentness floor. The adjacent failure mode is that the machinery used to recover those lineages can itself become a permanent super-root, while independent floors can be stale, poisoned or mutually inconsistent after catastrophic control-plane loss.

Central rule: **Reconstitution authority is an exceptional, scoped recovery capability with its own succession/retirement lifecycle; it is not a timeless root above normal policy. Independent floors are authenticated rollback evidence, not truth by storage count. Catastrophic recovery converges only after conflicting floor evidence is preserved, bounded, reconciled against surviving higher-order evidence and followed by an explicitly admitted successor policy floor. Availability pressure cannot lower that floor.**

## Five-track balance
- A Platform/Browser: browser/SW/Cache Storage/IndexedDB supply observations and preserve local work, but cannot elect a recovery authority or policy floor.
- B UX/IA/Content: owns recovery-paused, evidence-conflict, reconstitution-pending/admitted, region-convergence and local-safe semantics.
- C Quality: owns destructive campaigns for poisoned floors, correlated loss, split recovery and long-offline return.
- D Search/Analytics: consumes coarse recovery/convergence states only; telemetry is neither a vote nor a stable-device dossier.
- E Architecture/Security/Operations: **highest-risk owner**; owns exceptional authority lifecycle, floor reconciliation and catastrophic convergence.

## SOURCE
### TUF compromise-recovery transfer precedent
TUF separates signing responsibilities and uses Root metadata to define trusted keys/thresholds. Its current FAQ states that compromised online-role keys are replaced through Root; if a threshold of Root keys is compromised, Root must be re-issued out of band. Transfer: compromise of ordinary authority and compromise of the higher-order recovery authority are different cases, and recovery may require an independently established trust path. TUF is a software-update framework, not MintTap's recovery architecture.
Sources: https://theupdateframework.io/spec/ ; https://theupdateframework.io/docs/faq/

### RFC 9162 conflict-evidence precedent
RFC 9162 recognizes conflicting authenticated tree views and cross-observer comparison as evidence of misbehavior; it does not define majority authority. Transfer: mutually inconsistent authenticated floors must be preserved as conflict evidence rather than resolved by copy count or newest local timestamp.
Source: https://www.rfc-editor.org/rfc/rfc9162.html

### NIST contingency/reconstitution precedent
NIST SP 800-53 Rev.5 remains current, with Release 5.2.0 issued 2025-08-27. CP controls require contingency planning, restoration priorities, protected recovery information and backup reliability/integrity testing. NIST's glossary defines recovery/reconstitution as restoring functions/capability to fully operational states. Transfer: recovery is governed and tested; surviving copies are not self-authenticating authority.
Sources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final ; https://csrc.nist.gov/glossary/term/recovery_and_reconstitution

### CHANGE WATCH — storage guidance
NIST SP 800-209 Rev.1 is an **Initial Public Draft dated 2026-07-22**; its public-comment period closed 2026-09-08. It is not a final baseline. It is relevant change-watch evidence for modern storage-security, isolation and restoration-assurance guidance only.
Source: https://csrc.nist.gov/pubs/sp/800/209/r1/ipd

## SYNTHESIS — reconstitution authority is not a permanent super-root
Distinguish:
1. normal admission authority — routine policy/head admission;
2. currentness floor — authenticated rollback lower-bound/evidence;
3. reconstitution authority — exceptional capability invoked when normal lineage cannot be uniquely restored;
4. reconstitution record — exact forward recovery statement and evidence bindings;
5. successor normal authority — post-recovery authority that resumes ordinary operation.

Persistent guards:
- `reconstitution authority available ≠ reconstitution authorized now`;
- `reconstitution authority valid once ≠ permanent super-root`;
- `reconstitution completed ≠ reconstitution credential remains active`;
- `independent floor authentic ≠ independent floor current`;
- `two matching floors ≠ two independent failure domains`;
- `highest generation floor ≠ legitimate floor`;
- `floor conflict resolved operationally ≠ historical conflict erased`;
- `region online ≠ region policy-converged`;
- `availability emergency ≠ permission to lower currentness/security floor`.

## Reconstitution-authority lifecycle
A generic lifecycle is: dormant/escrowed → eligibility established → activated for a bounded incident/scope → exact recovery proposal prepared → independent/higher-order evidence checked → reconstitution admitted → successor normal policy/key lineage established → recovery capability retired/resealed → post-event evidence retained under policy.

Activation should bind the incident/recovery scope, applicable last supportable ancestor/floors, unresolved UNKNOWN interval, exact successor policy/head, deletion/hold/security constraints and expiry/retirement conditions. Exact roles, thresholds, crypto and custodians remain OPEN.

The exceptional authority should not remain an always-online signing oracle. If its own trust material is compromised or cannot be uniquely established, it cannot solely bless a successor. A new recovery trust path must come from surviving evidence outside the compromised failure domain. This is analogous only at principle level to TUF's out-of-band Root recovery after threshold compromise.

## Reconstitution-authority succession
Planned succession and compromise succession differ.

Planned succession may overlap old/new recovery material according to an authenticated higher-order policy, with explicit predecessor→successor binding and retirement. Compromise succession cannot rely solely on the compromised authority. Preserve compromise evidence and UNKNOWN interval, establish an independently supportable recovery basis, issue an explicit new recovery-authority generation, and prevent the retired/compromised generation from current recovery use while retaining bounded historical verification material.

A PITR restore that resurrects an old recovery credential must fail against the surviving recovery-authority/currentness floor.

## Independent-floor poisoning model
An independent floor can fail by:
- rollback: authentic but older floor substituted for a newer admitted floor;
- pre-commit poisoning: attacker inserts a false floor before immutable storage locks it;
- splice: fields from different valid generations are recombined;
- omission: compromise/UNKNOWN/deletion/hold marker is dropped;
- fork: two valid-looking successors share a predecessor;
- correlated compromise: nominally separate floor stores share IAM/KMS/admin/deletion/recovery dependencies;
- freshness loss: floor is authentic but no longer proves currentness after an observation gap.

Therefore integrity/authenticity, exact set binding, lineage, freshness, independence and semantic admissibility are separate properties.

## Floor conflict and recovery
When surviving floors disagree:
1. freeze consequence-bearing admission and preserve every conflicting artifact/receipt;
2. verify each floor's bytes/signatures/context without treating verification as currentness;
3. identify common authenticated ancestor and exact divergence;
4. compare policy/key/security/deletion/hold generations and compromise markers;
5. evaluate failure-domain independence rather than copy count;
6. reject known rollback/splice/issued-but-never-admitted candidates;
7. if one lineage is uniquely supportable, admit recovery from that lineage under current higher-order policy;
8. if none is uniquely supportable, preserve divergence as UNKNOWN and invoke explicit reconstitution;
9. write a new independently survivable successor floor only after exact reconstitution admission;
10. retain bounded conflict evidence; do not compact away the UNKNOWN interval.

Neither majority, maximum generation nor latest timestamp is a generic resolver.

## Policy-floor convergence after catastrophic control-plane loss
Convergence is a state machine, not a database restore event:
`control plane lost → consequence-bearing admission frozen → surviving evidence collected → floor conflict classified → normal lineage restored OR explicit reconstitution admitted → successor policy/currentness floor persisted independently → region/service verifier state rebootstrap → regions prove enforcement of successor floor → queued work re-admitted → old recovery capability retired`.

A restored region is not current merely because health checks pass. It must demonstrate it is enforcing the admitted successor policy/key/currentness floor. Regions that cannot do so remain degraded/read-only/local-safe as product requirements permit.

Do not lower the server floor to accommodate a stale region/client. Compatibility/rebootstrap moves stale participants forward or contains them; it does not move authority backward.

## PWA / EFB boundary
For a company iPad that remained offline through catastrophic recovery:
1. preserve unique local flight/logbook records before destructive migration;
2. treat cached policy/head/key/SW/IndexedDB state as historical observation only;
3. obtain current authenticated server recovery/policy/currentness generation;
4. detect skipped compromised/disputed/reconstitution generations;
5. rebootstrap supported verifier/application state without lowering server floor;
6. separate remotely acknowledged records from local-only work;
7. submit local-only work under current authority with idempotency/provenance controls;
8. re-admit consequence-bearing remote queue only after current authorization and lineage reconciliation.

The client clock, cached maximum generation, `navigator.onLine`, stale Service Worker or possession of an old recovery artifact is never a currentness oracle. Physical Safari/Home Screen/managed-iPad behavior remains OPEN.

## UX/accessibility transfer
Recovery UI must distinguish at least: service available but admission frozen; floor conflict detected; reconstitution authority not yet activated; reconstitution pending; successor floor admitted; region convergence incomplete; local data safe; remote actions paused; historical UNKNOWN retained. Avoid `secure`, `fixed`, `latest` or `recovered` without scoped meaning, and never encode these states by color alone. Human/AT validation remains Design Studio-owned and OPEN.

## Privacy / analytics transfer
Recovery evidence can expose device, operator, flight, location and incident history. Analytics should receive coarse recovery generation/state/convergence buckets, not raw signed artifacts or stable fleet/device identifiers unless a separately justified operational/security system requires them. Analytics cannot participate in authority election.

## Track C destructive campaign
Define a **312-case generic campaign**, extending 193's 304 cases with: dormant recovery credential stolen before activation; expired recovery authority replayed; planned R→R+1 succession followed by PITR to R; compromised R solely blessing R+1; authentic-but-stale independent floor; pre-lock poisoned immutable floor; two floors with shared hidden KMS/IAM failure domain; highest-generation malicious floor; floor missing UNKNOWN/deletion/hold marker; mutually inconsistent authentic floors; region restored healthy but enforcing P-1; emergency availability operator lowering floor; stale Service Worker treating reconstitution publication as admission; long-offline iPad presenting retired recovery material; queue drain before region convergence; AT/operator confusion between service-restored and authority-restored.

Campaign definition is not execution.

## TRANSFER VALIDATION / CONTRADICTION
- TRANSFER VALIDATION: TUF supports separation of duties, trusted-root/key succession and out-of-band recovery after higher-order compromise; it does not define MintTap recovery ceremonies.
- TRANSFER VALIDATION: RFC 9162 supports preserving conflicting authenticated views; it does not define floor-election majority.
- TRANSFER VALIDATION: NIST contingency controls support governed/tested recovery and integrity assurance; they do not prescribe MintTap topology or quorum.
- CONTRADICTION: immutable independent storage does not prove that the value written before lock was legitimate.
- CONTRADICTION: a disaster-recovery credential that remains indefinitely empowered after recovery has become a standing super-root and expands blast radius.
- CONTRADICTION: a region that serves traffic successfully is not thereby enforcing the current admitted security/policy floor.

## MINTTAP DECISION / DIRECTION
1. Keep reconstitution authority exceptional, scoped, generational and retireable; do not model a permanent omnipotent recovery key.
2. Give reconstitution authority its own planned/compromise succession and anti-rollback state.
3. Treat independent floors as evidence/lower bounds, never votes or unilateral head-minting authorities.
4. Resolve floor conflicts through lineage/policy/failure-domain evidence; use explicit UNKNOWN + reconstitution when no unique winner exists.
5. Require successor policy/currentness floor admission before regional/queue consequence-bearing recovery.
6. Never lower server authority/floor to recover stale regions or long-offline PWAs.
7. Preserve unique local EFB data while rebootstrap moves clients forward.
8. Keep exact topology, roles, thresholds, cryptography, provider controls, legal/aviation retention and product UI OPEN pending canonical implementation/runtime evidence.

## OPEN / DEPENDENCY / VALIDATION
OPEN: actual MintTap/LogMate reconstitution authority; policy/key hierarchy; independent-floor topology/failure domains; storage/crypto bindings; regional convergence mechanism; queue semantics; backup/PITR/deletion/hold integration; managed-iPad/WebKit behavior; legal/aviation retention; operator/AT comprehension.

DEPENDENCY: Software Engineering owns concrete state machines, transactions, credential storage, floor persistence, regional enforcement proof, recovery tooling and executable fault injection. Design Studio owns reusable recovery/conflict/currentness interaction and human/AT validation.

VALIDATION: execute 312-case campaign; simulate normal and compromised reconstitution-authority succession; poison/rollback multiple nominally independent floors; destroy primary control plane and recover with both uniquely resolvable and irreconcilable floor sets; verify restored regions cannot serve consequence-bearing writes under stale policy; test long-offline physical iPad/Safari/Home Screen; validate privacy/accessibility/operator comprehension.

## CHANGE WATCH
TUF specification/root recovery semantics; NIST SP 800-53 5.x; NIST SP 800-209 Rev.1 draft status; NIST SP 800-57 Rev.6 and SP 800-131A Rev.3 status; transparency/witness ecosystem; provider immutable-storage/independent-custody semantics; WebKit/iPadOS PWA recovery behavior.

## Gate
**PASS (generic).** Web Manager can constrain reconstitution authority so it does not become a permanent super-root, distinguish authentic floors from current/admissible floors, recover from poisoned/conflicting independent floors without majority or generation-number shortcuts, and specify forward policy-floor convergence after catastrophic control-plane loss while keeping stale PWA clients non-authoritative. Production certification remains OPEN.