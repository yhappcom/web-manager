# 256 — PWA Conflict-Resolution Provenance, Correction-Chain Convergence & Multi-Authority Dispute Closure

Status: **PASS (generic) / PRODUCT + DOMAIN-AUTHORITY + DATA-MODEL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A conditional-request/offline transport mechanics; Track B dispute/correction UX; Track C destructive convergence validation; Track D conflict/correction measurement.  
Dependencies: 074, 131–136, 171–255, especially correction provenance, branch convergence, current admission, incarnation identity, recovered-data conflict authority and replay-safe admission.

## Problem
255 separated retry, package replay, record identity, semantic duplicate detection, conflict resolution and principal reassignment. The next failure boundary appears after a conflict is correctly detected: several legitimate authorities can issue different corrections; an offline branch can contain a correction based on an old projection; a later authoritative reversal can invalidate an earlier resolution; and a dispute can remain unresolved while the product still needs a readable, non-destructive state.

Central rule: **conflict detection is not conflict closure. A resolution must itself be a provenance-bearing, scope-limited, revisioned decision with explicit predecessors, authority basis and consequence. Later corrections or reversals supersede rather than erase prior decisions. Concurrent/offline branches may converge structurally without being semantically safe to publish.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns HTTP validators/preconditions, Service Worker queue/retry mechanics and local browser state. Conditional requests can prevent blind overwrite but cannot elect semantic truth.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `CURRENT`, `SUPERSEDED`, `DISPUTED`, `PENDING-REVIEW`, `CORRECTION-ACCEPTED`, `REVERSAL-ACCEPTED` and recovery states without presenting unresolved data as settled truth.
- **C Performance/Accessibility/Quality:** high dependency pressure. Campaign expands **800 → 808 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. Measures conflict families, correction attempts, authority classes, resolution latency, reopen/reversal and unresolved inventory separately. Analytics cannot elect winners.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns correction lineage, authority scope, optimistic-concurrency/admission boundaries, dispute state, supersession/reversal and convergence closure.

## SOURCE

### RFC 9110 — HTTP preconditions prevent blind lost updates, not semantic conflict
RFC 9110 defines conditional requests and requires `If-Match` to be evaluated before state-changing operations when present. A failed `If-Match` normally yields `412 Precondition Failed`. This protects a mutation from silently applying to a representation different from the one on which it was based.

Source:
- https://www.rfc-editor.org/rfc/rfc9110.html#name-preconditions
- https://www.rfc-editor.org/rfc/rfc9110.html#field.if-match

**TRANSFER VALIDATION:** strong bounded precedent for base-revision checks. It does not determine which of two domain corrections is substantively correct.

### RFC 6585 — a server may require conditional mutation
RFC 6585 defines `428 Precondition Required`, typically to avoid the lost-update problem by requiring clients to submit conditional requests.

Source:
- https://www.rfc-editor.org/rfc/rfc6585.html#section-3

**TRANSFER VALIDATION:** a useful protocol control for forcing clients to declare a base state. The RFC explicitly notes that clients cannot assume 428 alone prevents conflicts; domain-level resolution remains separate.

### RFC 6902 — patch preconditions and atomic patch application are representation controls
RFC 6902 defines JSON Patch as an ordered sequence of operations and includes a `test` operation. When used with HTTP PATCH, failed operations cause the patch not to be deemed successful; the RFC also shows `If-Match` in examples.

Source:
- https://www.rfc-editor.org/rfc/rfc6902.html

**TRANSFER VALIDATION:** useful for expressing explicit base/value assumptions and avoiding partial representation mutation. A successful patch is not evidence that the corrected value had domain authority.

### W3C PROV — revision and invalidation are explicit provenance relations
W3C PROV defines `wasRevisionOf` as a derivation where the resulting entity is a revised version of an original, and models invalidation as the point after which an entity is no longer available for use. It also supports attribution and qualified provenance relations.

Source:
- https://www.w3.org/ns/prov
- https://www.w3.org/TR/prov-o/

**TRANSFER VALIDATION:** bounded provenance precedent for retaining predecessor/revision/invalidation relationships rather than rewriting history. PROV does not define aviation/logbook conflict authority.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**. Physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN, so conflict/dispute UI cannot be promoted from generic reasoning alone. Software Engineering implementation evidence remains bounded transfer evidence; actual product correction/admission code and data model are OPEN.

## SYNTHESIS 1 — make the resolution an immutable domain event
Do not overwrite a conflicting record with only the chosen value. A resolution event should identify at least:
- conflict/dispute identity;
- subject logical record and affected field/scope;
- predecessor revision(s) or branch heads considered;
- proposed/accepted correction revision;
- resolving actor/principal and authority basis;
- policy/domain-rule generation used;
- decision time plus trustworthy server/admission ordering where relevant;
- reason/evidence references;
- consequence scope (`display`, `publish`, `sync`, `export`, `regulatory`, etc.);
- successor/supersession relation when later changed.

Guard: `value chosen ≠ resolution provenance captured`; `current projection ≠ complete resolution history`.

## SYNTHESIS 2 — distinguish authorship, correction proposal, approval and publication
One actor can author an original record, another can propose a correction, another can approve it, and the system can later publish a projection. These roles are not interchangeable.

A current user who can edit a local field is not automatically authorized to close a safety/legal dispute. Conversely, a reviewer who can approve a correction does not become the original author.

Guards: `correction author ≠ original author`; `proposal permission ≠ approval permission`; `approval ≠ publication`; `publication ≠ historical authorship`.

## SYNTHESIS 3 — base revision is part of correction intent
A correction should carry the revision/head against which it was authored. If the server has moved to another head, the operation is stale even if its payload is syntactically valid.

HTTP `If-Match`/ETag or an application-level predecessor revision can enforce this boundary. A stale operation should enter rebase/conflict evaluation rather than silently overwrite the newer state.

Guards: `request valid ≠ base current`; `ETag mismatch ≠ correction false`; `precondition failure ≠ safe to retry unchanged`.

## SYNTHESIS 4 — transport concurrency control does not resolve domain authority
Optimistic locking can prove that two clients did not blindly overwrite each other. It cannot prove which correction is correct. A server that accepts the first `If-Match` mutation and rejects the second has serialized writes, not resolved the semantic dispute.

Guard: `first conditional write wins ≠ semantic winner`; `412 returned ≠ conflict resolved`.

## SYNTHESIS 5 — concurrent correction branches form a relation, not a timestamp race
If offline branch A corrects `R7 → R8A` while remote branch B corrects `R7 → R8B`, preserve both branch relations. Device clock, upload order and branch discovery order cannot by themselves choose a winner.

Where both changes are independent and the domain contract proves they commute, a merged successor can cite both predecessors. Where they overlap or authority is uncertain, keep an explicit dispute.

Guards: `later upload ≠ later authoritative intent`; `two valid branches ≠ one auto-mergeable branch`; `mergeable fields ≠ mergeable domain meaning`.

## SYNTHESIS 6 — CRDT-style structural convergence is not enough for authority-sensitive records
A data structure can deterministically converge to the same state on all replicas while still choosing a domain-invalid result. Last-writer-wins, max timestamp, lexical actor ID or deterministic tie-breaker can provide convergence but not substantive authority.

Use automatic merge only for fields/operations whose domain semantics establish commutativity or an acceptable deterministic resolution. Consequence-bearing corrections require the applicable authority rule.

Guards: `replicas converge ≠ semantic conflict resolved`; `deterministic winner ≠ authorized winner`; `eventual consistency ≠ eventual correctness`.

## SYNTHESIS 7 — later reversal supersedes; it does not erase the earlier resolution
A legitimate resolution can later be reversed because new authoritative evidence appears, an earlier decision is found wrong, or policy permits appeal. Preserve:
`claim(s) → dispute → resolution A → reversal/reopen → resolution B`.

The current projection may point to B while historical evidence retains A and why A ceased to govern.

Guards: `reversed ≠ never happened`; `superseded ≠ deleted`; `current truth projection ≠ immutable historical truth claim`.

## SYNTHESIS 8 — authority is scoped by action, subject and interval
An actor may be authorized to correct one record class, one crew assignment, one organization or one time interval but not another. Store enough scope to prevent a valid old approval from being replayed onto another conflict.

A resolution made while authority was valid can remain historical evidence after that authority ends; ending authority does not automatically invalidate past valid decisions. New decisions require current authority.

Guards: `historically authorized ≠ currently authorized`; `authority for record A ≠ authority for record B`; `authority ended ≠ past decision erased`.

## SYNTHESIS 9 — multi-authority disagreement needs explicit dispute state
When two legitimate authorities issue incompatible decisions and no higher/defined tie-break rule is proven, do not fabricate a winner. Maintain `DISPUTED` / `ESCALATION-REQUIRED` with both signed/attributed claims and the applicable scope.

The product can remain usable by separating consequences. For example, a record can remain locally readable while mutation, sync publication, export-as-final or regulatory projection is held. Exact consequence policy is product/domain-specific and OPEN.

Guards: `readable ≠ publishable`; `preserved ≠ admitted`; `unresolved ≠ false`; `two approvals ≠ consensus`.

## SYNTHESIS 10 — closure requires a defined authority path, not majority voting
Do not resolve a domain dispute by counting devices, replicas, users or signatures unless the governing domain explicitly defines a quorum. Multiple approvals can share one failure domain or lack authority for the consequence.

A closure rule should identify the authorized role/rule, evidence required, predecessor dispute state, successor projection and negative conditions that must no longer be accepted.

Guard: `more signatures ≠ more authority`; `replica majority ≠ domain quorum`; `consensus algorithm ≠ business/legal authority`.

## SYNTHESIS 11 — preserve rejected and superseded corrections for audit without re-admitting them
Rejected/stale/superseded corrections can be important provenance. Retain them according to privacy/retention policy with a disposition that prevents them from silently returning through restore, offline replay or import.

Replay/dedup state must therefore cover correction/resolution events as well as base records.

Guards: `rejected correction retained ≠ correction active`; `history retained ≠ replay permitted`; `backup restore ≠ superseded correction current again`.

## SYNTHESIS 12 — correction-chain compaction must retain proof of supersession
If long histories are compacted for performance, preserve enough durable lineage/checkpoint evidence to show which revisions and resolutions were superseded, why the current projection is current, and what unresolved branches remain. A compacted projection alone cannot prove conflict closure.

Guard: `projection compacted ≠ dispute history disposable`; `current row restored ≠ correction chain restored`.

## SYNTHESIS 13 — offline PWA rejoin must revalidate each queued correction against current lineage
A Service Worker or app queue can preserve a correction while offline, but on rejoin the server must evaluate its base revision, operation identity, current authority, policy/schema generation and existing dispute state. Queue order or client timestamp cannot establish global semantic order.

If the operation is stale but potentially valid, preserve it as a proposal/conflict input rather than dropping it or auto-applying it.

Guards: `offline queue preserved ≠ correction still admissible`; `Service Worker replay order ≠ correction authority order`; `network restored ≠ dispute resolved`.

## SYNTHESIS 14 — unresolved disputes need a safe projection contract
A system may need to render a record while a conflict remains open. The projection contract should state whether the UI shows last-admitted value, both claims, a neutral placeholder or a warning, and which downstream actions are disabled. Do not let a single convenient display value become silently interpreted as final truth by export, sync or analytics.

Track B must make the state understandable and accessible; Track D must measure unresolved inventory without treating the displayed fallback as a resolved outcome.

Guard: `displayed value ≠ resolved value`; `fallback projection ≠ publishable truth`.

## SYNTHESIS 15 — correction-chain closure needs negative tests
A closure claim requires evidence that:
- a stale correction based on an old predecessor cannot overwrite the current head;
- the same correction/resolution event cannot be replayed after restart/restore;
- a superseded resolution cannot become current via offline import;
- an expired/reassigned authority cannot close a new dispute;
- a current authority cannot rewrite historical authorship;
- a later reversal preserves prior resolution provenance;
- competing branch heads cannot be silently collapsed by timestamp/order;
- unresolved state cannot leak into final/publish/export surfaces as resolved truth.

Guard: `current projection correct once ≠ correction-chain closure PASS`.

## PWA / LogMate-like EFB application
For a company iPad that was offline while remote corrections occurred:

1. **Preserve local operation/provenance:** retain the queued correction, its base logical revision, source incarnation/principal and original evidence.
2. **Establish current authority:** refresh current bootstrap, principal assignment and correction/publish scopes independently of the old Service Worker/session.
3. **Compare lineage before mutation:** detect whether the base revision is still current or whether remote correction branches now exist.
4. **Classify the operation:** current/non-conflicting, stale-but-rebasable, concurrent-branch conflict, authority-ended, duplicate/replayed, unverifiable.
5. **Do not timestamp-elect:** device wall clock, queue order and reconnect order cannot choose the correction winner.
6. **Apply consequence-specific authority:** only a domain-proven rule/actor may close the dispute; otherwise retain `DISPUTED`/`PENDING-REVIEW`.
7. **Record resolution as a new provenance event:** reference all considered predecessor branches and authority/evidence basis.
8. **Preserve reversal path:** later authoritative evidence creates a successor reversal/resolution; it does not delete the earlier decision.
9. **Project safely:** local readability can continue where allowed while final sync/export/publication is gated by dispute state.
10. **Test restart/restore/rejoin:** prove stale/superseded correction events cannot resurrect after Service Worker restart, app reinstall/recovery, backend restore or successor-device import.

**OPEN:** actual LogMate flight/logbook correction authority, crew/operator roles, authoritative upstream sources, legal/aviation amendment requirements, field-level mergeability, backend conditional-update model, revision identifiers, offline queue schema and final-export semantics remain unknown until canonical product/runtime evidence exists.

## Track C destructive additions — 800 → 808
Add eight defined cases:
1. **First-conditional-write semantic election:** the first successful `If-Match` write is treated as proof that its correction is substantively correct.
2. **Timestamp branch collapse:** concurrent offline/remote correction branches are silently collapsed using device or arrival time.
3. **Deterministic-convergence authority laundering:** CRDT/LWW convergence is treated as domain conflict resolution without authority semantics.
4. **Resolution overwrite:** later reversal replaces the earlier resolution record, destroying supersession provenance.
5. **Expired-authority replay:** a historically valid correction approval is replayed to close a new/current dispute after authority ended.
6. **Restore resurrects superseded correction:** backup restores data but loses resolution/replay state, making an old correction current again.
7. **Service-Worker queue-order election:** offline replay order decides which competing correction becomes current.
8. **Unresolved-to-final leakage:** a fallback/readable projection from a disputed record is exported/synced/published as settled truth.

**VALIDATION:** defined destructive oracles only; not executed product tests. Campaign total: **808 defined cases; execution PASS not claimed**.

## MINTTAP DECISION / generic operating direction
- Model correction proposals, approvals, resolutions, reversals and publication as separate provenance-bearing events where consequences require it.
- Require an explicit predecessor/base revision for consequence-bearing corrections; use transport/application preconditions to reject blind stale mutation.
- Treat conditional requests as concurrency controls, never as semantic conflict authority.
- Preserve concurrent correction branches until domain semantics prove a safe merge or authorized resolution.
- Do not use LWW/timestamps/replica majority as generic authority rules.
- Preserve superseded/reversed decisions and their authority/evidence basis; current projection may be singular while history remains plural.
- Make unresolved disputes first-class and separate readable state from publishable/final state.
- Revalidate long-offline queued corrections against current lineage, authority and policy before admission.
- Keep actual product correction authority, merge rules, legal/aviation obligations and runtime behavior OPEN until canonical evidence exists.

## OPEN / DEPENDENCY / VALIDATION
- **OPEN:** actual LogMate/MintTap revision/correction/dispute schema and authoritative correction sources.
- **OPEN:** actual role/crew/operator authority hierarchy, escalation/quorum rules and legal/aviation correction obligations.
- **OPEN:** backend ETag/precondition/transaction model, correction replay ledger and restore semantics.
- **OPEN:** which record fields, if any, are safely commutative/auto-mergeable.
- **OPEN:** physical iPadOS/WebKit installed-PWA queue/rejoin/restart behavior for the actual product.
- **DEPENDENCY:** Track A supplies browser/HTTP/Service Worker mechanics only; it cannot define domain truth.
- **DEPENDENCY:** Track B must validate disputed/corrected/superseded UX with AT and representative humans before product promotion.
- **DEPENDENCY:** Software Engineering must validate implementation-level transaction, precondition, lineage and replay behavior when canonical product code/runtime is available.
- **VALIDATION:** execute Track C destructive campaign against real schema/backend/managed-iPad runtime before any production PASS.
- **CHANGE WATCH:** browser/PWA background/retry behavior and platform policy remain version-specific; HTTP standards cited here are protocol precedents, not product-domain authority definitions.

## Adjacent checkpoint
The next highest-value generic question is **257 — dispute-escalation authority, resolution expiry/reopen policy & downstream projection revocation**: determine how unresolved disputes escalate without role inflation; when a previously valid resolution may expire or be reopened; how downstream exports/analytics/sync recipients learn that an earlier projection was superseded or revoked; and how offline recipients reconcile a correction/reversal without destructive full reset.