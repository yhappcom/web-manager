# 271 — PWA Revocation-Source Key/Authority Rotation, Dual-Control Transition & Partition-Safe Successor Adoption

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime persistence and update boundaries; Track B truthful migration/revalidation UX; Track C destructive validation; Track D bounded adoption/lag diagnostics.  
Dependencies: 260–270 dependency, topology, re-entry, composite-proof, revocation-distribution and anti-rollback governance.

## Problem

270 established that revocation distribution is evidence transport rather than self-authenticating truth. The next boundary is rotation of the authority that produces that truth. A planned R1→R2 transition must let current clients adopt R2 without ambiguous permanent dual authority. A compromise transition is harder: if R1 itself may be hostile, R1 alone cannot safely define R2. Meanwhile long-offline clients may know only R1 and must not be stranded forever or allowed to make R1 current again merely because they reconnect late.

Central rule: **planned rollover and compromise recovery are different trust problems. A successor authority must be admitted through a transition path whose assurance remains valid under the stated compromise model; overlap is bounded migration state, not permanent co-equal truth. Clients advance monotonically through authenticated lineage or a governed rebootstrap, preserve historical evidence, and never let an old/partitioned authority roll current state backward. Unique data remains distinct from authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns exact Service Worker/client persistence, storage, secure transport and late-client update mechanics. Browser update state cannot establish authority succession.
- **B UX/IA/Content:** high dependency pressure. Owns truthful states such as `successor pending`, `revalidation required`, `limited/recovery-only`, and preserved-offline-data messaging without presenting migration as data loss.
- **C Performance/Accessibility/Quality:** destructive campaign expands **920 → 928 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures R2 adoption, R1 sightings, partition/unknown tail, failed lineage checks and predecessor rejection. Telemetry cannot elect R2.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns successor admission, compromise-safe transition, overlap limits, anti-rollback lineage, retirement and rebootstrap governance.

## SOURCE

### NIST SP 800-57 Part 1 Rev. 5 — compromise changes key state and requires revocation/replacement

NIST SP 800-57 Part 1 Rev. 5 states that a key/key pair transitions from active to compromised when relevant integrity/confidentiality becomes suspect, and that compromised keying material is revoked. It distinguishes compromise from ordinary deactivation/replacement and records/notifies the transition where other entities know the key.

Source: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**TRANSFER VALIDATION:** this is key-management guidance, not a PWA authorization protocol. The bounded precedent is that suspected compromise changes what the old key may safely authorize; ordinary rollover assumptions cannot simply be reused.

### RFC 4986 / RFC 6024 — rollover must recover from compromise without degrading trust

RFC 4986 requires trust-anchor rollover mechanisms to support add/delete/replace operations, recovery from a configured trust-anchor compromise when another uncompromised anchor remains, and non-degrading trust during rollover. RFC 6024 separately requires trust-anchor management to support compromise/loss recovery and recognizes bootstrap/out-of-band establishment of management trust.

Sources:  
https://www.rfc-editor.org/rfc/rfc4986  
https://www.rfc-editor.org/rfc/rfc6024

**TRANSFER VALIDATION:** DNSSEC/PKI trust anchors are not product revocation authorities. Their useful precedent is that successor admission, compromise recovery and bootstrap are explicit security operations rather than ordinary data synchronization.

### RFC 5011 — an existing trusted key can introduce a successor, but compromised-current-key risk is explicit

RFC 5011 defines automated DNSSEC trust-anchor update behavior. It explicitly identifies the risk that compromise of an existing key could let an attacker introduce malicious new trust material, and provides hold-down/revocation behavior intended to constrain that problem.

Source: https://www.rfc-editor.org/rfc/rfc5011

**TRANSFER VALIDATION:** do not copy RFC 5011 timers or DNSKEY semantics into PWA design. The bounded lesson is that `old key signed new key` is not universally sufficient under a compromise threat model.

### RFC 9691 — planned successor staging uses reciprocal predecessor/successor evidence and an acceptance interval

RFC 9691 defines RPKI Trust Anchor Key objects. For planned rollover, the current authority can publish a successor, the successor publishes the predecessor relation, relying parties verify both sides, and an acceptance timer precedes production transition. The RFC also notes that clients initialized at different points may temporarily use different keys and that previous keys may need to remain available during migration.

Source: https://www.rfc-editor.org/rfc/rfc9691

**TRANSFER VALIDATION:** RPKI TAK is a specific protocol. The reusable precedent is planned staged succession, reciprocal lineage checking, bounded overlap and explicit late-client considerations—not the 30-day timer itself.

### The Update Framework — root rotation requires continuity under both predecessor and successor trust sets

TUF root metadata identifies authorized keys and thresholds. During root update, version N+1 must be signed by the threshold required by trusted root N and by the threshold required by N+1, and clients retrieve intermediate root versions in sequence. TUF also rejects rollback of root versions.

Source: https://theupdateframework.github.io/specification/v1.0.26/

**TRANSFER VALIDATION:** TUF is software-update security, not a MintTap/LogMate revocation protocol. Its useful precedent is explicit predecessor/successor continuity, threshold-aware migration and sequential anti-rollback lineage.

## SYNTHESIS 1 — planned rotation and compromise rotation are different transitions

For a planned R1→R2 rotation where R1 is still trusted, R1 participation can be meaningful evidence. If R1 is suspected compromised, a transition authorized only by R1 inherits the compromise.

Guards:
- `R1 signed R2 ≠ R2 trustworthy when R1 is compromised`;
- `planned rollover procedure ≠ compromise-recovery procedure`;
- `new key material ≠ new trust root established`.

## SYNTHESIS 2 — successor admission needs a trust path valid under the compromise model

Generic successor evidence may include an uncompromised pre-established recovery authority, threshold/quorum that survives the stated compromise, independently protected management authority, or governed out-of-band rebootstrap. Exact mechanism is product-specific.

Do not invent independence: two approvers or keys in one compromised control plane may remain one failure domain.

Guards:
- `two signatures ≠ two independent authorities`;
- `different key IDs ≠ different compromise domains`;
- `recovery channel exists ≠ recovery channel uncompromised`.

## SYNTHESIS 3 — dual-control transition means bounded cross-authorization, not permanent co-equal truth

During migration, R1 and R2 may coexist for continuity, but the system needs explicit transition state: predecessor, successor, scope, generation, start, acceptance/adoption criteria, retirement trigger and compromise status. Coexistence without precedence creates split authority.

Guards:
- `both accepted during migration ≠ both permanently authoritative`;
- `dual-control ≠ whichever response arrives first wins`;
- `overlap improves continuity ≠ overlap has no attack cost`.

## SYNTHESIS 4 — successor proof should bind lineage, scope and consequence

A generic transition object/evidence should bind at least predecessor identity, successor identity, authority/scope, relevant consequence, transition generation/epoch, policy/verifier context and provenance. A successor authorized for one scope does not silently inherit every R1 capability.

Guards:
- `successor for scope A ≠ successor for scope B`;
- `revocation authority successor ≠ universal application administrator`;
- `key rotation ≠ policy rotation unless explicitly bound`.

## SYNTHESIS 5 — anti-rollback applies to authority lineage itself

Once a client/server has established R2 as current for scope S at generation G2, later receipt or restoration of authentic R1 evidence cannot make R1 current again absent a separately governed forward transition.

Guards:
- `authentic predecessor ≠ current predecessor`;
- `old authority reachable again ≠ authority rollback permitted`;
- `PITR restored R1 state ≠ R1 reauthorized`.

## SYNTHESIS 6 — partition-safe adoption cannot depend on simultaneous fleet migration

A distributed fleet will not transition atomically. Some clients may know R2 while long-offline clients know only R1. Safety comes from current authoritative execution boundaries and explicit requalification, not an assumption that every client has received the transition.

A useful generic split is:
- central/current systems: R2 current, R1 rejected for affected high-consequence operations after retirement criteria;
- known transitional clients: bounded migration behavior;
- unknown/offline tail: data may remain valuable, but high-consequence authority is not inherited on return.

Guards:
- `fleet not converged ≠ R2 cannot become current centrally`;
- `central R2 current ≠ offline client already R2-qualified`;
- `offline client missed rollover ≠ offline data invalid`.

## SYNTHESIS 7 — acceptance/adoption windows are evidence windows, not magic safety timers

RFC 9691 provides a protocol-specific 30-day acceptance timer; TUF uses sequential signed root versions. A product should not cargo-cult either value/mechanism. The generic need is enough bounded evidence to test successor availability/lineage and detect contradiction before relying on it, while preserving a compromise path that can move faster when old authority is unsafe.

Guards:
- `timer expired ≠ successor safe`;
- `timer not expired ≠ emergency compromise recovery forbidden`;
- `elapsed time ≠ independent validation`.

## SYNTHESIS 8 — compromise may require breaking continuity rather than preserving malicious continuity

If R1 is actively compromised, maximizing uninterrupted acceptance of R1 can be worse than temporarily degrading high-consequence operations. Recovery policy must be consequence-aware: preserve/read/recovery may remain available while mutation/publication requiring current authority is fenced until R2 is established.

Guards:
- `availability preserved ≠ trust preserved`;
- `continuity at all costs ≠ safe rollover`;
- `high-consequence fenced ≠ unique data destroyed`.

## SYNTHESIS 9 — predecessor retirement needs authoritative rejection proof

R2 becoming current is not sufficient. Retirement needs evidence that R1 can no longer exercise the retired consequence at authoritative boundaries, including API/job/manual/recovery paths as applicable. Historical R1 evidence remains retained for audit/provenance.

Guards:
- `R2 works ≠ R1 retired`;
- `R1 key deleted in one store ≠ R1 rejected everywhere material`;
- `predecessor historically retained ≠ predecessor currently authorized`.

## SYNTHESIS 10 — late/offline clients rejoin by forward lineage reconciliation

A long-offline iPad that knows R1 should not jump directly to arbitrary latest Rn solely from network response, nor should it insist on R1 forever. Rejoin should establish an authenticated lineage from a still-valid trust/recovery basis or use governed rebootstrap when lineage cannot be safely proven.

Generic flow:
1. preserve unique data, queue payloads and old transition evidence;
2. classify R1 as historical/current/compromised/unknown for the relevant scope;
3. prevent inherited high-consequence replay;
4. obtain successor lineage/current checkpoint through a valid trust path;
5. verify anti-rollback generation and applicable policy/schema/incarnation;
6. reconcile queued operations individually;
7. prove obsolete R1 consequence rejection;
8. create a current successor composite decision;
9. retain historical lineage and unresolved-tail evidence.

## SYNTHESIS 11 — missing intermediate transitions are not automatically fatal, but need a defined proof path

TUF deliberately validates intermediate root versions; other systems may use a checkpoint or recovery authority capable of proving a later successor directly. The architecture must specify which skips are valid. A client cannot infer that R5 supersedes R1 merely because R5 has a larger number or a newer timestamp.

Guards:
- `higher generation label ≠ valid lineage`;
- `latest endpoint response ≠ safely skippable intermediate authority`;
- `cannot prove lineage ≠ delete local records`.

## SYNTHESIS 12 — forked successor claims require quarantine, not first-writer/majority transport election

If R1 lineage appears to nominate R2 while another authenticated recovery path nominates R3, preserve both. Determine whether one path is invalid under the compromise model or whether governance has genuinely forked. High-consequence operations remain bounded until a current authority is established.

Guard: `two authentic successor claims ≠ one may be chosen by arrival order`.

## SYNTHESIS 13 — browser/PWA runtime state is orthogonal to authority rotation

A Service Worker update can deliver code that understands R2, but code deployment does not establish R2's organizational authority. Conversely, a stale worker can be blocked by server-side rejection of R1.

Guards:
- `worker supports R2 ≠ R2 authorized`;
- `worker still knows R1 ≠ server must accept R1`;
- `app shell updated ≠ authority lineage migrated`.

## SYNTHESIS 14 — telemetry measures adoption but cannot elect the successor

Useful observations include R2-qualified cohort, R1 request sightings, unknown/offline tail, failed lineage checks, predecessor rejection counts, rebootstrap count and contradictory successor claims. A dashboard showing 99% R2 adoption cannot turn R2 into authority if admission proof is invalid; nor does a 1% offline tail automatically keep R1 authoritative centrally.

Guard: `adoption percentage ≠ authority election`.

## SYNTHESIS 15 — rollback/recovery must preserve the authority transition boundary

Backup/PITR restoring application state from before R2 adoption must not silently restore R1 as current. Recovery needs a current anti-rollback reference outside the restored failure domain or governed rebootstrap. Conversely, historical R1 evidence should remain readable for provenance.

Guards:
- `restore before rotation ≠ undo rotation`;
- `historical verification key retained ≠ current signing authority retained`.

## SYNTHESIS 16 — generic rotation contract

For a material R1→R2 transition:
1. identify whether rotation is planned, suspected-compromise or confirmed-compromise;
2. preserve R1 history and current compromise evidence;
3. define authority/scope/consequence and transition generation;
4. select a successor-admission path valid under that compromise model;
5. establish R2 identity/key and protect its activation path;
6. where safe, establish predecessor↔successor lineage/cross-evidence and bounded adoption period;
7. prevent ambiguous co-equal authority by defining precedence and retirement criteria;
8. validate R2 behavior and current policy/verifier compatibility;
9. advance central authority monotonically;
10. fence/reject R1 for retired consequences at authoritative boundaries;
11. requalify late/offline clients and queued operations on return;
12. preserve unique data independently of authority status;
13. maintain rollback-resistant transition evidence outside restored failure domains;
14. monitor adoption/unknown tail without using telemetry as authority;
15. retain historical R1 evidence but not R1 current authority;
16. escalate contradictions/forks to governed recovery rather than transport majority vote.

This is a reasoning contract, not a mandated cryptographic architecture.

## Track C destructive campaign additions — 920 → 928

1. **compromised-R1-self-successor:** suspected-compromised R1 alone signs R2 and system treats R2 as clean. Expected: successor admission requires a path valid under the compromise model.
2. **permanent-dual-authority:** R1 and R2 remain co-equal indefinitely after migration. Expected: bounded transition and explicit predecessor retirement.
3. **timer-equals-trust:** acceptance interval expires despite failed successor lineage test. Expected: elapsed time cannot substitute for validation.
4. **late-client-R1-resurrection:** offline iPad reconnects with authentic R1 and rolls central/current state backward. Expected: preserve data; reject authority rollback; requalify forward.
5. **R2-success-only-retirement:** R2 positive test passes while R1 is still accepted by a background/manual path. Expected: predecessor rejection proof required.
6. **multi-key-independence-theater:** R1 and recovery key are separate IDs but share one compromised control plane. Expected: failure-domain analysis prevents false independence.
7. **PITR-pre-rotation-resurrection:** backup restore returns R1 to current state. Expected: external/current anti-rollback reference or governed rebootstrap preserves R2 boundary.
8. **worker-upgrade-authority-theater:** Service Worker understands R2 and UI declares migration complete without semantic successor proof. Expected: runtime deployment remains orthogonal to authority admission.

These are defined cases, not executed product evidence.

## EFB / LogMate-like application case

Scenario: a company iPad was offline before R1→R2 rotation. Central systems later suspect R1 compromise, establish R2 through a recovery path not solely controlled by R1, and retire R1 for publication/sync authority. The iPad returns with unique flight/logbook records, R1-era transition evidence, an old Service Worker and queued operations.

Generic safe handling:
1. preserve local records, queue payloads and R1 provenance;
2. do not let old worker/network success imply R1 currentness;
3. block inherited publication/sync authority while allowing policy-permitted preservation/recovery;
4. obtain current R2 lineage/checkpoint via a valid trust/rebootstrap path;
5. update runtime/schema only as separate prerequisites;
6. reconcile each queued operation under current identity/policy/schema/authority;
7. reject obsolete R1 authorization at authoritative server/operation boundaries;
8. create successor decision evidence for operations that still qualify;
9. retain R1 historical evidence without allowing it to vote current authority backward.

**OPEN:** actual LogMate identity model, backend, PWA storage, MDM/ADE topology, offline duration, sync protocol, domain authority, legal/aviation requirements and physical iPad/WebKit behavior are unverified.

## Cross-track transfer

### Track A
Own exact browser lifecycle/storage/update mechanics. Consume only the requirement that runtime state cannot self-certify semantic authority succession.

### Track B
Design states that distinguish preserved local data from unavailable current authority, and planned migration from revalidation/recovery. Human/AT validation remains OPEN.

### Track C
Execute the 928-case campaign only when real implementation/runtime evidence exists; defined cases are not PASS evidence.

### Track D
Measure migration/adoption/failure/unknown-tail evidence. Do not turn cohort percentage, channel majority or analytics events into successor authorization.

### Track E
Own the successor-admission compromise model, transition lineage, overlap, predecessor retirement, rebootstrap and anti-rollback recovery.

## MINTTAP DECISION / DIRECTION

For future PWA/web architecture work:
- model authority rotation explicitly rather than replacing a key/config value in place;
- distinguish planned rollover from compromise recovery;
- require successor-admission evidence whose trust assumptions survive the stated compromise;
- keep dual-authority overlap bounded and consequence/scope-specific;
- make authority lineage anti-rollback and recovery-aware;
- reject obsolete predecessor authority at execution boundaries after retirement;
- preserve unique offline data independently from execution authority;
- requalify long-offline clients rather than inheriting central NORMAL;
- treat Service Worker/browser update state as runtime evidence only;
- keep actual product thresholds, cryptographic design and managed-iPad behavior OPEN pending canonical implementation evidence.

## VALIDATION

Generic gate PASS requires ability to explain and diagnose:
- why ordinary rollover and compromise recovery differ;
- why a compromised predecessor cannot be sole trust basis for a clean successor;
- how bounded overlap differs from permanent dual authority;
- how anti-rollback lineage applies to authority rotation;
- how late/offline clients can rejoin without resurrecting R1 or losing unique data;
- why successor positive tests do not prove predecessor retirement;
- why browser/Service Worker state and telemetry do not establish authority succession;
- why backup restore needs to preserve the transition boundary.

This artifact satisfies that **generic reasoning gate only**. No production implementation, physical-device, cryptographic construction, MDM, domain-authority or legal/aviation PASS is claimed.

## CHANGE WATCH

Re-check when:
- NIST key-management guidance changes materially;
- TUF root-rotation semantics/specification changes;
- relevant IETF trust-anchor rollover guidance changes;
- Apple/WebKit/managed-device behavior changes in a way that affects bootstrap/recovery transport;
- canonical MintTap/LogMate implementation defines real authority/key/MDM/offline-sync topology.

## Next highest-value bottleneck

**272 — successor-authority compromise during overlap, cross-signature contamination & emergency trust-reset convergence**: determine how to recover when R2 is compromised before R1 retirement, when predecessor/successor cross-evidence becomes contaminated, or when neither in-band authority can safely certify the next state; define bounded trust-reset/rebootstrap, evidence preservation, long-offline rejoin and predecessor/successor rejection without destructive data reset.