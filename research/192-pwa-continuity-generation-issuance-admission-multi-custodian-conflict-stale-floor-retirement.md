# 192 — PWA Continuity-Generation Issuance/Admission, Multi-Custodian Conflict Resolution & Stale-Floor Retirement

Status: **PASS (generic) / PRODUCT + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A reconnect/cache mechanics; Track B conflict/degraded-state UX; Track C destructive validation; Track D privacy-bounded convergence telemetry.
Dependencies: 183–191 exact-artifact lineage, transparency, archive/preservation integrity, portability/escrow independence, custody compromise, package freshness and anti-rollback.

## Problem
191 established that continuity custody is an evidence/survivability plane and that integrity, authenticity, completeness, set consistency, freshness and current authority are distinct. The next bottleneck is governance of the continuity-generation head itself: how a candidate generation becomes admitted, how competing independently authentic heads are handled, and how obsolete anti-rollback floors are retired without silently reopening downgrade paths.

Central rule:

> **Issuance creates a candidate continuity generation; admission makes that exact candidate acceptable under the current continuity policy. Custodian signatures, numerical recency and copy counts are evidence inputs, not admission authority. Conflicting valid-looking heads suspend automatic advancement until lineage and policy resolve the conflict.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. HTTP/SW/Cache Storage/IndexedDB can preserve generation observations but browser caches, client clocks and local maxima cannot issue or admit continuity heads.
- **B UX/IA/Content:** high-pressure consumer. Owns distinguishable semantics for candidate issued, admitted, superseded, stale-floor retirement pending, conflict detected, reconciliation required and remote consequence-bearing work paused.
- **C Performance/Accessibility/Quality:** validator. Owns fork, race, rollback, stale-floor retirement, long-offline and operator/AT campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Measures convergence/conflict states without turning generation observations into stable-device or flight/user dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns issuance/admission separation, exact-generation lineage, conflict containment, floor lifecycle and recovery governance.

## SOURCE
### The Update Framework — trusted metadata transition precedent
TUF separates root, targets, snapshot and timestamp roles. Root metadata defines trusted keys and signature thresholds for roles; snapshot metadata binds repository metadata versions; timestamp metadata identifies a current snapshot and has freshness semantics. The specification's root update procedure requires sequential version progression and treats lower versions as rollback. This is software-update precedent, not a continuity/preservation standard.

Sources:
- https://theupdateframework.io/spec/
- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/overview/

### RFC 9162 — conflicting-view evidence precedent
RFC 9162 (Certificate Transparency v2.0, December 2021; obsoletes RFC 6962) uses signed tree heads and Merkle consistency/inclusion evidence. It explicitly recognizes conflicting views as log misbehavior and notes that multiple clients comparing signed tree heads ('gossip') can detect append-only violations; the RFC does not define gossip as a complete universal protocol. Transfer is limited to the principle that independently valid-looking signed heads can constitute conflict evidence rather than a vote for whichever head is newer or more numerous.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

### NIST SP 800-53 Rev.5 — governed change/backup precedent
NIST SP 800-53 Rev.5 remains a current security/privacy control catalog (with later 5.x updates). Configuration/change and contingency controls support governed change, protected backup and tested recovery. Transfer only the governance principle: security-significant state transitions and recovery information require controlled authorization and validation; NIST does not prescribe a MintTap continuity-generation quorum.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

## SYNTHESIS — issuance, admission, observation and enforcement are different states
A generic continuity lifecycle should distinguish at least:
1. **prepared** — exact package/set exists and validation can run;
2. **issued** — an authorized issuer has created a signed candidate generation;
3. **observed** — one or more custodians/monitors/clients have retained evidence of it;
4. **admitted** — current continuity policy accepts the exact candidate as the new head/floor;
5. **distributed** — required custody/observation domains have received it;
6. **effective for recovery** — recovery logic may use it subject to current security/policy/deletion/hold constraints;
7. **superseded/retired** — no longer current but retained as bounded historical evidence where required.

Persistent guards:
- `generation issued ≠ generation admitted`;
- `generation admitted ≠ every custodian converged`;
- `custodian signed head ≠ head authorized`;
- `highest generation number ≠ legitimate successor`;
- `latest wall-clock timestamp ≠ legitimate successor`;
- `most copies agree ≠ authority established`;
- `threshold signatures valid ≠ semantic transition authorized unless the applicable policy says so`;
- `conflict detected ≠ choose majority branch`;
- `old floor inconvenient ≠ old floor safely retireable`;
- `floor retired ≠ historical evidence deleted`;
- `client forgot old floor ≠ system floor lowered`;
- `PITR restored old admission registry ≠ old registry current`.

## Candidate generation issuance
A candidate generation should bind, subject to implementation design:
- exact package/manifest identity;
- predecessor admitted head or explicit reconstitution lineage;
- continuity policy generation under which issuance occurred;
- applicable provider/key/schema/verifier/security generations;
- declared completeness scope;
- retention/deletion/hold constraints relevant to recovery;
- issuer identity/role evidence and cryptographic context;
- bounded creation evidence without relying on mutable wall-clock ordering alone.

Issuance does not itself advance the anti-rollback floor. This prevents a compromised or premature issuer from converting every signed candidate into current recovery authority.

## Admission ceremony
Generic admission should validate the exact candidate rather than a mutable alias such as `latest`:
1. verify artifact/set identity and completeness;
2. verify authenticated predecessor or explicit recovery/reconstitution transition;
3. verify issuer/role/key/policy generation is allowed for this transition;
4. reject known rollback, freeze or splice conditions;
5. compare against surviving higher security/policy/provider/deletion/hold/continuity floors;
6. evaluate known conflicting heads/incident markers;
7. record an immutable/bounded admission decision tied to the exact candidate and applicable policy generation;
8. only then advance the current continuity floor;
9. distribute/observe the admitted state and measure convergence separately.

Exact quorum/threshold, key hierarchy and operator ceremony remain product/crypto OPEN. TUF threshold-role precedent demonstrates separation of roles and thresholds but does not supply MintTap numbers.

## Multi-custodian conflict resolution
A conflict exists when independently retained evidence supports incompatible successor claims from the same admitted predecessor or otherwise incompatible current heads.

Do **not** resolve by:
- largest generation number;
- newest wall-clock timestamp;
- majority of copies/custodians;
- fastest responding provider;
- client-local highest cached generation;
- 'last writer wins'.

Generic response:
1. preserve all conflicting heads/packages/receipts/checkpoints;
2. freeze automatic continuity-floor advancement and consequence-bearing recovery admission that depends on the disputed lineage;
3. identify common admitted ancestor and exact divergence point;
4. verify each branch against the policy/key/provider/security state applicable at issuance and admission time;
5. inspect whether one branch lacks valid admission, violates predecessor/set binding, crosses a compromise/retirement boundary, or conflicts with surviving higher-order policy/security evidence;
6. if evidence uniquely establishes the legitimate branch, reconstitute current head with an explicit conflict-resolution record;
7. if not, retain UNKNOWN/incident state rather than manufacture an ordering;
8. never erase the losing/conflicting signed evidence merely because operations resume.

RFC 9162 supports the detection principle: conflicting signed views are evidence to investigate, not a majority-election mechanism.

## Stale-floor retirement
Anti-rollback floors cannot grow forever without lifecycle management: old algorithms, keys, providers, storage, policy formats and client generations eventually become obsolete. But deleting the floor is equivalent to deleting part of downgrade memory unless a successor floor safely dominates it.

Generic retirement conditions:
- a newer admitted floor has authenticated continuity from, or explicit governed reconstitution over, the retiring floor;
- the successor floor carries enough lineage/evidence to reject artifacts that were already stale under the old floor;
- required historical verification material is retained separately from current admission authority;
- deletion/hold/incident constraints are reconciled;
- offline-client compatibility policy is explicit; unsupported stale clients are contained rather than causing server floor rollback;
- restore/PITR procedures know the successor floor independently of a mutable application database;
- retirement is itself auditable and cannot be performed solely by a compromised custodian whose rollback resistance it weakens.

Retirement should therefore be modeled as **floor succession**, not `delete old version check`.

## Floor compaction without rollback-memory loss
Long-lived systems may compact old floor records. Safe compaction conceptually preserves enough authenticated summary to prove that the current floor dominates retired generations and to identify relevant compromise/UNKNOWN boundaries. It must not convert a history of `G admitted → G+1 disputed → G+2 reconstituted` into a false simple chain `G → G+2` that hides the disputed interval.

Exact accumulator/checkpoint/manifest mechanism remains implementation OPEN. No blockchain requirement is inferred.

## Race and partial-admission states
Important races include:
- G+1 issued while G+2 is being prepared;
- two issuers produce distinct G+1 candidates from G;
- admission commits but distribution to one custodian fails;
- custodian receives candidate before admission record;
- region A admits G+1 while region B still enforces G;
- PITR restores an admission registry from before G+1;
- deletion/hold state advances between issuance and admission.

These are distributed-state conditions, not reasons to collapse issuance/admission/distribution into one flag. A partially distributed admitted generation can be current while a custodian is stale; a merely issued candidate cannot become current because many custodians saw it.

## PWA / EFB boundary
A long-offline company iPad can return with cached continuity floor G while server has admitted G+n and may have retired intermediate verifier/provider material.

Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. treat cached floor/head/checkpoint/provider material as historical observation;
3. obtain current authenticated server security/policy/continuity state;
4. determine whether client crossed retired/compromised/UNKNOWN generations;
5. migrate/interpret local records through supported compatibility paths without lowering server floor;
6. reconcile acknowledged remote history separately from local-only work;
7. submit local-only work under current authority;
8. re-admit queued consequence-bearing operations only after current authorization and lineage reconciliation.

A stale PWA that cannot verify the current continuity generation may need degraded/local-only operation or supported upgrade/rebootstrap. It must not demand that the server re-enable a retired floor merely to regain compatibility. Physical Safari/Home Screen/managed-iPad behavior remains OPEN.

## UX / accessibility transfer
Recovery/admin UI must distinguish:
- candidate generation created;
- candidate validation complete;
- generation admitted/current;
- distribution/convergence incomplete;
- conflicting heads detected;
- automatic advancement paused;
- stale floor retirement pending/complete;
- client compatibility too old for current floor;
- local data safe while remote submission is paused.

Do not label a signed or replicated candidate simply `current`. Do not require users to infer authority from version numbers, timestamps or color. Exact interaction design and representative human/AT validation remain Design Studio-owned/OPEN.

## Privacy / telemetry boundary
Useful low-cardinality telemetry may include admitted generation class, convergence lag bucket, conflict state, floor-retirement state and compatibility class. Avoid raw evidence packages, stable device identifiers, exact flight/user/location histories and unnecessary long-term per-device generation trails. Security evidence retention and product analytics remain separate systems.

## Track C destructive campaign
Define a **296-case generic campaign**, extending 191's 288-case baseline with at least these adjacent cases:
- validly signed but never-admitted G+1 replicated to every custodian;
- two distinct validly issued G+1 candidates from the same G;
- minority custodian holds the only legitimately admitted head while majority holds an issued-only branch;
- attacker increments generation number without valid predecessor/admission;
- wall-clock manipulation makes unauthorized branch look newer;
- admission succeeds but one region/custodian remains at G;
- PITR restores pre-admission registry and tries to retire G+1;
- old floor is deleted before successor anti-rollback memory is independently durable;
- compromised custodian initiates floor retirement to enable rollback;
- long-offline iPad returns with a locally higher-looking but never-admitted generation;
- stale Service Worker interprets `issued` as `current` and drains queue;
- screen reader/operator cannot distinguish `signed`, `admitted`, `distributed` and `current` states;
- two custodians agree because both share the same compromised admission feed;
- conflict evidence is garbage-collected after operational recovery;
- G+2 reconstitution hides a G+1 UNKNOWN/compromise interval;
- client compatibility pressure causes server to reactivate retired verifier/currentness floor.

Campaign definition is not execution. Physical-device/browser/provider/crypto/AT/human evidence remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** TUF demonstrates durable separation of trusted-role policy, threshold signatures, version progression, snapshot/set binding and freshness. Transfer the separation, not TUF's software-update architecture wholesale.
- **TRANSFER VALIDATION:** RFC 9162 demonstrates that conflicting signed heads can be durable misbehavior/conflict evidence and that cross-observer comparison is useful; it does not create a majority-vote authority rule.
- **TRANSFER VALIDATION:** NIST SP 800-53 supports governed security-significant change and tested/protected recovery information without prescribing product-specific continuity thresholds.
- **CONTRADICTION:** `more custodians agree` is not a substitute for authenticated admission lineage when custodians can share an upstream failure domain.
- **CONTRADICTION:** retiring old compatibility material by lowering the server floor defeats anti-rollback; stale clients are compatibility problems, not authority sources.

## MINTTAP DECISION / DIRECTION
For generic Web Manager/PWA guidance:
1. separate continuity issuance, admission, distribution, observation and recovery effectiveness;
2. bind admission to exact package/set identity plus authenticated predecessor/reconstitution lineage;
3. do not make generation integers, wall clocks, custodian signatures or copy counts into currentness authority;
4. treat incompatible valid-looking heads as incident/conflict evidence and suspend automatic advancement until resolved;
5. retire stale floors only through authenticated successor-floor transition that preserves rollback memory and relevant UNKNOWN/compromise history;
6. keep historical verifier/evidence retention separate from current admission capability;
7. never lower current server floor to accommodate long-offline PWA clients; preserve their unique local data and use supported migration/rebootstrap;
8. keep concrete topology, quorum, algorithms, retention periods and UI mechanics OPEN pending implementation/provider/legal evidence.

## OPEN / DEPENDENCY / VALIDATION
OPEN:
- actual MintTap/LogMate continuity issuer/admission topology and policy;
- exact package/head/checkpoint schema, signatures, thresholds and floor persistence;
- actual region/provider/custodian convergence behavior;
- actual backup/PITR/deletion/hold integration;
- managed-iPad/WebKit compatibility/rebootstrap behavior;
- legal/aviation constraints on retained conflict/history evidence;
- representative human/AT comprehension.

DEPENDENCY:
- Software Engineering owns concrete admission transactions, manifest/checkpoint formats, verifier isolation, persistent floor storage, restore/rebootstrap mechanics and test harnesses when product/runtime evidence exists.
- Design Studio owns reusable recovery/conflict/currentness interaction design and human validation.

VALIDATION:
- execute the 296-case destructive campaign against real architecture;
- simulate split issuance, partial regional admission, custodian disagreement and PITR rollback;
- verify floor retirement across backup restore and long-offline client return;
- verify physical iPad/Safari/Home Screen and accessibility behavior;
- verify privacy/retention behavior for conflict and convergence evidence.

## CHANGE WATCH
- TUF specification and reference implementation security guidance;
- RFC/transparency ecosystem developments around gossip/witnessing;
- NIST contingency/configuration guidance;
- provider object-lock/versioning/checkpoint semantics;
- WebKit/iPadOS PWA storage/update/background/rebootstrap behavior.

## Gate
**PASS (generic).** Web Manager can separate continuity-generation issuance from admission/distribution, diagnose multi-custodian conflicts without majority-authority shortcuts, and specify stale-floor succession/retirement that preserves rollback memory while keeping long-offline PWA clients non-authoritative.

Production certification remains OPEN.