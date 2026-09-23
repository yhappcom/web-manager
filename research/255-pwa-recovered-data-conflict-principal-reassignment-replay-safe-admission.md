# 255 — PWA Recovered-Data Conflict Authority, Principal Reassignment & Duplicate/Replay-Safe Admission

Status: **PASS (generic) / PRODUCT + DATA-MODEL + IDENTITY + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A retry/offline transport mechanics; Track B conflict/reassignment UX; Track C destructive duplicate/replay validation; Track D recovery/dedup measurement.  
Dependencies: 074, 131–136, 171–254, especially conflict/reconciliation, provenance, current admission, incarnation identity and recovered-data ownership transfer.

## Problem
254 established that recovered old-incarnation data crosses into a current system through quarantine, attribution/ownership resolution and current-policy admission without reviving old authority or rewriting authorship. The adjacent problem is harder: recovered data can overlap or conflict with records already admitted remotely; a pilot/account may have been reassigned; schema/incarnation migrations may change representation; and the same recovery package may be retried by several operators or successor incarnations.

Central rule: **transport retry suppression, record identity, semantic duplicate detection, conflict resolution, principal reassignment and admission authority are separate concerns. A recovered package must be safely replayable without silently duplicating domain effects, while conflicts and ownership changes remain explicit governed decisions rather than timestamp/device/account shortcuts.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns retry/offline request mechanics, Service Worker/background limitations and local storage facts. HTTP retry semantics do not decide domain duplicates or conflict winners.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `DUPLICATE`, `POSSIBLE-DUPLICATE`, `CONFLICT`, `REASSIGNMENT-PENDING`, `ADMITTED`, `REJECTED` and `MANUAL-REVIEW` states, preserving user-visible history and recovery options.
- **C Performance/Accessibility/Quality:** high dependency pressure. Campaign expands **792 → 800 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. Measures package attempts, unique packages, unique records, duplicate/conflict classes and disposition separately. Analytics cannot elect conflict winners or ownership.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns stable identities, replay ledger/floors, provenance-preserving reassignment, conflict authority, admission atomicity and closure.

## SOURCE

### RFC 9110 — transport idempotency is request semantics, not business-record identity
RFC 9110 defines an idempotent method as one whose intended server effect for multiple identical requests is the same as for one request. It explicitly allows logging/revision side effects and explains why idempotent requests can be retried after connection failure.

Source:
- https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods

**TRANSFER VALIDATION:** useful precedent for separating safe retry behavior from domain-level duplicate/conflict semantics. A LogMate recovery/import API is not automatically idempotent merely because HTTP offers idempotent methods.

### RFC 9449 — replay identifiers are scoped proof evidence, not domain identity
DPoP requires a unique `jti` for each proof and describes server-side replay detection. It also warns that proof/nonce enforcement can affect retry behavior even for otherwise idempotent resource requests.

Source:
- https://www.rfc-editor.org/rfc/rfc9449.html

**TRANSFER VALIDATION:** bounded precedent for nonce/replay-state design. A proof identifier can stop reuse of one authorization proof but does not identify a flight/logbook record, resolve a semantic duplicate or determine which conflicting record is correct.

### NIST SP 800-63B-4 — authenticator binding/recovery preserves account lifecycle distinctions
Current NIST SP 800-63B-4 requires lifecycle management of authenticator bindings and describes account recovery as a distinct process after which new authenticators can be bound. It requires records of authenticators bound to subscriber accounts and explicit invalidation when bindings should end.

Source:
- https://pages.nist.gov/800-63-4/sp800-63b.html

**TRANSFER VALIDATION:** bounded precedent for separating principal/account continuity from authenticator/device continuity. It does not define LogMate crew reassignment, record ownership or aviation record semantics.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED** with physical-device/PWA, screen-reader and representative-human UX evidence OPEN. Product conflict/reassignment UI cannot be promoted without those validation classes. Software Engineering evidence remains bounded transfer evidence; product data-model/admission implementation is OPEN.

## SYNTHESIS 1 — use distinct identifiers for distinct questions
At minimum distinguish:
- `recovery_package_id` — immutable identity of one preserved recovery package/version;
- `package_attempt_id` — one submission/retry attempt;
- `source_record_id` — source-system identity if trustworthy and stable;
- `logical_record_id` — product/domain identity across representation/schema/incarnation changes where the domain can define it;
- `record_revision_id` — one immutable revision/content state;
- `admission_id` — one current-policy admission decision/effect;
- `principal_assignment_id` — one governed assignment interval/relationship.

One UUID/hash should not be overloaded to answer all of these.

Guards: `request ID ≠ record ID`; `package ID ≠ record ID`; `content hash ≠ semantic identity`; `same source ID ≠ same current authority`.

## SYNTHESIS 2 — exact duplicate and semantic duplicate are different
An exact byte-identical record can often be detected by immutable content/provenance identity. A semantic duplicate may be represented differently after schema migration, normalization, timezone correction or source-system export. Conversely, two records with similar date/flight/route/time fields may be legitimate distinct events.

Use deterministic domain keys only when the domain contract proves they are unique enough for the consequence. Otherwise classify `POSSIBLE-DUPLICATE` and retain evidence for review.

Guards: `same hash ⇒ same committed bytes`, not necessarily `same domain event`; `same composite fields ≠ guaranteed duplicate`; `different bytes ≠ different event`.

## SYNTHESIS 3 — deduplication is not conflict resolution
Two records can refer to the same logical event while carrying different revisions or claims. Dedup answers whether they belong to one identity set; conflict resolution decides which projection/correction relationship is admitted. Do not discard the losing evidence merely because one projection wins.

Guard: `duplicate detected ≠ conflict resolved`; `projection winner ≠ losing evidence disposable`.

## SYNTHESIS 4 — conflict authority is consequence-specific
Do not elect a winner by newest device clock, newest import time, currently logged-in user, newest incarnation or server-arrival order. Resolution may require domain rules, authoritative upstream evidence, current principal confirmation, supervisor/organizational approval, or a correction workflow depending on consequence.

A generic system should support `CONFLICT-UNRESOLVED` rather than fabricate certainty.

Guards: `latest timestamp ≠ latest authoritative intent`; `current user ≠ conflict authority`; `server copy ≠ automatically correct`.

## SYNTHESIS 5 — principal reassignment must be an event, not an authorship rewrite
If a record historically belonged to principal P12 but organizational policy now requires it to be managed under P20, preserve original authorship/creation attribution and add an explicit reassignment/custody/entitlement event with actor, authority, reason, effective scope/time and predecessor relation.

Reassignment may change who can manage or view a record; it does not retroactively make P20 the original author.

Guards: `reassigned to P20 ≠ authored by P20`; `account merge ≠ history rewrite`; `current entitlement ≠ historical authorship`.

## SYNTHESIS 6 — replay-safe package admission needs durable consumed-state
A recovery package may be submitted twice because the first response was lost, an operator retries, another successor incarnation discovers the same export, or an attacker replays it. Keep a durable package/admission ledger keyed by a stable package identity plus relevant generation/scope. A repeated submission should return/reconstruct the existing disposition where safe, not create a second domain effect.

Do not rely only on short-lived HTTP nonce state: long-offline recovery replay can occur far beyond a request-level replay window.

Guards: `request replay blocked ≠ package replay blocked`; `response missing ≠ admission missing`; `retry ≠ second admission`.

## SYNTHESIS 7 — replay ledger itself needs provenance and lifecycle
A consumed-package marker that can be lost during restore, migration or compaction can reopen replay. Preserve replay/dedup state with backup/migration semantics appropriate to the consequence, or derive it from durable admitted provenance. If the ledger is reconstructed, record the reconstruction basis and uncertainty.

Guard: `data restored ≠ replay state restored`; `projection restored ≠ admission history restored`.

## SYNTHESIS 8 — package-level idempotency is not enough
One package can contain multiple records with mixed dispositions: duplicate, conflict, accepted, rejected, ownership-pending. If processing crashes midway, retry must not duplicate already committed records or silently skip uncommitted ones. Persist per-record disposition or use an atomic boundary that the actual backend can guarantee.

Do not claim cross-browser/server atomicity from a local transaction.

Guards: `package accepted ≠ every record admitted`; `transactional locally ≠ transactional across browser/server`; `all-or-nothing desired ≠ all-or-nothing implemented`.

## SYNTHESIS 9 — migrations need identity-preserving mappings
Schema migration may alter serialization and derived fields. Preserve explicit mapping from source record/revision to successor logical record/revision rather than recalculating identity from mutable display fields after every migration.

Where no stable logical identity can be proven, preserve uncertainty and use a duplicate-candidate relation rather than inventing one.

Guard: `schema migrated ≠ identity preserved`; `normalized fields equal ≠ lineage proven`.

## SYNTHESIS 10 — corrections should be append/relate, not silent overwrite
For safety/audit-sensitive records, a conflict resolution that changes a value should preserve the superseded claim and correction provenance where product/legal policy requires it. The current projection may show one value while historical evidence retains both claims and the resolution event.

Guard: `current projection singular ≠ history singular`; `correction accepted ≠ original never existed`.

## SYNTHESIS 11 — current authorization applies to the operation being performed
Historical data may be authentic and attributable, yet current authorization must govern import, reassignment, correction, merge and publication independently. An operator allowed to recover bytes may not be allowed to reassign a pilot or resolve a material conflict.

Guard: `recovery permission ≠ reassignment permission ≠ conflict-resolution permission ≠ publish permission`.

## SYNTHESIS 12 — offline PWA queues require operation identity, not timestamp ordering
A long-offline PWA can queue creates/corrections while remote state evolves. Give queued operations stable identities and predecessor/base context sufficient for the domain to detect stale/conflicting intent. Do not use client wall-clock order as universal conflict authority.

Guard: `queue order ≠ global semantic order`; `client timestamp later ≠ current authority later`.

## SYNTHESIS 13 — Service Worker retry is transport machinery only
A Service Worker may retry a failed request or replay an offline queue when connectivity returns. It must not independently decide that a recovery package is new, that a record is duplicate, or that a conflict can be auto-merged. Those decisions belong to durable current admission semantics.

Guard: `Service Worker retry succeeded ≠ exactly-once domain effect proven`; `background replay ≠ conflict resolution`.

## SYNTHESIS 14 — measurement must retain the denominator and disposition classes
Track D should distinguish submission attempts from unique packages and unique logical records. Report duplicates, possible duplicates, conflicts, ownership-pending, accepted, rejected and unresolved separately. A falling accepted count can reflect better deduplication rather than failure; a low conflict count can reflect over-aggressive silent merging.

Guard: `fewer imported rows ≠ data loss proven`; `zero conflicts observed ≠ conflict detector complete`.

## SYNTHESIS 15 — closure needs negative replay and authority tests
A correct admission path must show more than successful first import:
- identical package replay does not create another domain effect;
- replay through another successor incarnation/operator does not bypass consumed state;
- changed package with reused friendly ID is not silently treated as the old package;
- same semantic candidate with different bytes reaches dedup/conflict policy;
- old principal cannot resolve/reassign after authority ended;
- current principal cannot rewrite old authorship;
- stale offline correction cannot overwrite a newer authoritative correction by timestamp alone;
- restore/recovery does not forget consumed-package state.

Guard: `first import PASS ≠ replay/conflict closure PASS`.

## PWA / LogMate-like EFB application
For a retired/offline company iPad recovery where the server already contains overlapping logbook records:

1. **Preserve package and source provenance:** freeze an immutable recovery package identity/version; do not normalize away original evidence before comparison.
2. **Establish current authority independently:** current bootstrap identifies which operator/principal may recover, reassign, resolve conflicts and admit records.
3. **Check package replay before effects:** consult durable consumed/admission state; retry returns prior disposition when appropriate.
4. **Classify records:** exact duplicate, semantic duplicate candidate, non-conflicting new record, conflicting revision, ownership/reassignment pending, invalid/unverifiable.
5. **Resolve identity before winner:** establish logical-record relationship where evidence permits; do not use current user/device/time as the identity key.
6. **Apply consequence-specific conflict authority:** preserve both claims until the applicable domain rule/authorized actor resolves them.
7. **Record reassignment separately:** if pilot/account responsibility changes, retain original authorship and add explicit assignment/transfer provenance.
8. **Admit per record/operation:** preserve admission/rejection/conflict decisions and migration mappings under current policy.
9. **Test replay across restart/restore/incarnation:** prove duplicate package/record effects cannot reappear after Service Worker retry, backend restart or recovery-state restore.

**OPEN:** actual LogMate flight-record identity, duplicate key, revision/correction semantics, pilot/account reassignment rules, authoritative conflict sources, backend transaction/idempotency design, recovery-package format and legal/aviation retention requirements are unknown until canonical product/runtime evidence exists.

## Track C destructive additions — 792 → 800
Add eight defined cases:
1. **Request-ID/domain-ID collapse:** one HTTP idempotency/retry token is treated as permanent flight-record identity.
2. **Composite-key false merge:** same date/flight/route/time fields silently collapse two legitimate domain events.
3. **Timestamp conflict election:** latest device/import timestamp silently wins a recovered/current conflict.
4. **Principal-reassignment authorship rewrite:** reassigned record is rewritten as originally authored by the successor principal.
5. **Cross-incarnation package replay:** the same recovery package is admitted again through a different successor device/operator.
6. **Lost replay ledger after restore:** data restore succeeds but consumed-package state is absent, enabling duplicate effects.
7. **Partial-package retry duplication:** crash after partial admission causes already committed records to be admitted again on retry.
8. **Service-Worker exactly-once theater:** successful offline queue replay is treated as proof of exactly-once domain admission without durable server evidence.

**VALIDATION:** defined destructive oracles only; not executed product tests. Campaign total: **800 defined cases; execution PASS not claimed**.

## MINTTAP DECISION / generic operating direction
- Separate package/attempt/logical-record/revision/admission/principal-assignment identities.
- Treat transport idempotency and proof replay defense as necessary but insufficient for domain duplicate/conflict safety.
- Preserve exact and semantic duplicate classes; do not force uncertain candidates into automatic merge.
- Make conflict authority consequence-specific and allow explicit unresolved states.
- Model principal reassignment as a provenance event; never rewrite historical authorship for convenience.
- Maintain durable package/record admission state across retries, migrations, backup/restore and successor incarnations.
- Preserve per-record dispositions when package processing can be partial.
- Keep Service Worker/background retry mechanics subordinate to server/domain admission semantics.
- Keep actual product identity/conflict/reassignment/transaction rules OPEN until canonical evidence exists.

## OPEN / DEPENDENCY / VALIDATION
- **OPEN:** LogMate/MintTap production record IDs, composite keys, schema/revision model, recovery package IDs and dedup retention.
- **OPEN:** actual principal/pilot/account reassignment authority and aviation/legal correction obligations.
- **OPEN:** backend transaction/idempotency/replay-ledger implementation and restore behavior.
- **OPEN:** physical iPadOS/WebKit installed-PWA offline queue/retry behavior for the actual product.
- **DEPENDENCY:** Software Engineering should validate implementation-level idempotency, transaction boundaries, replay-state durability and crash/retry behavior when canonical product code exists.
- **DEPENDENCY:** Design Studio owns reusable conflict/recovery interaction patterns; Web Manager supplies required states/consequences.
- **VALIDATION:** execute exact duplicate, semantic duplicate, conflict, partial failure, replay-after-restore and cross-incarnation replay tests against the real backend/PWA.
- **CHANGE WATCH:** browser background/offline capabilities and managed-iPad behavior remain platform/version specific.

## Gate
**255 PASS (generic).** The Web Manager can distinguish transport retry/idempotency from domain duplicate/conflict semantics; model stable package/record/revision/admission/assignment identities; preserve authorship through reassignment; prevent package replay across retries/incarnations/restores; and define data-preserving conflict admission for long-offline PWA recovery. Product/data-model/backend/managed-iPad/legal/aviation/runtime validation remains OPEN.

## Next highest-value target
**256 — conflict-resolution provenance, correction-chain convergence & multi-authority dispute closure:** determine how multiple legitimate correction/assignment authorities produce auditable resolution without silent last-write-wins; how correction chains remain convergent across long-offline branches; how a later authoritative reversal supersedes rather than erases an earlier resolution; and how unresolved disputes remain usable/readable without becoming silently publishable current truth.