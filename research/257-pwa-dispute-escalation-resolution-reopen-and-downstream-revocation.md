# 257 — PWA Dispute-Escalation Authority, Resolution Expiry/Reopen Policy & Downstream Projection Revocation

Status: **PASS (generic) / PRODUCT + DOMAIN-AUTHORITY + DATA-MODEL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A delivery/cache/Service Worker mechanics; Track B dispute/revocation UX; Track C destructive propagation validation; Track D downstream measurement.  
Dependencies: 074, 117–136, 171–256, especially authority scope, current-policy admission, branch convergence, recovered-data conflict handling and correction-chain provenance.

## Problem
256 established that conflict detection is not conflict closure and that a resolution is itself a provenance-bearing, revisioned decision. The next failure boundary appears after a resolution exists or a dispute remains open: escalation can accidentally inflate authority; a previously valid resolution can become inapplicable without becoming historically false; downstream consumers can retain a superseded projection; and a long-offline PWA can reconnect after multiple reversals with only stale local state.

Central rule: **escalation changes the decision path, not the meaning of every role. Resolution expiry/reopen changes current applicability, not historical provenance. Downstream revocation is a versioned convergence problem: every consequence-bearing consumer must be able to distinguish the projection it previously accepted from the successor/revocation state and must not require destructive full reset merely to regain currentness.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns HTTP cache invalidation/revalidation, Service Worker delivery/retry, Web Push capability and offline transport facts. Delivery mechanics do not prove revocation receipt or semantic application.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `DISPUTED`, `ESCALATED`, `RESOLVED`, `REOPENED`, `SUPERSEDED`, `REVOKED-DOWNSTREAM`, `STALE-LOCAL` and `CURRENT` states without false finality or destructive recovery.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **808 → 816 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. Measures dispute age, escalation class, reopen/reversal, projection generation, downstream acknowledgement and stale-recipient inventory separately. Telemetry cannot elect authority or prove semantic convergence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns escalation scope, resolution applicability, reopen/reversal provenance, downstream invalidation contract, convergence floors and closure evidence.

## SOURCE

### NIST SP 800-53 Release 5.2.0 — separation of duties and least privilege
NIST SP 800-53 AC-5 requires documented separation of duties and access authorizations that support it; AC-6 requires least privilege. These are bounded precedents for preventing an escalation mechanism from turning a reviewer/support/admin role into universal domain authority.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

**TRANSFER VALIDATION:** strong governance precedent for scoped roles and privilege. It does not define LogMate aviation/logbook authority.

### W3C PROV — revision and invalidation are explicit relations
PROV defines revision and invalidation rather than requiring historical overwrite. Invalidation marks the point after which an entity is no longer available for use; revision links a revised entity to its predecessor.

Sources:
- https://www.w3.org/ns/prov
- https://www.w3.org/TR/prov-o/

**TRANSFER VALIDATION:** bounded provenance precedent for `resolution A → invalidation/reopen → resolution B`. PROV does not define product-specific dispute rules.

### RFC 9111 — cache invalidation is local, not global revocation proof
RFC 9111 requires relevant caches to invalidate stored responses after successful unsafe requests, but explicitly notes that this does not guarantee all appropriate responses are invalidated globally; only caches traversed by the request are directly affected.

Source:
- https://www.rfc-editor.org/rfc/rfc9111.html#name-invalidating-stored-responses

**TRANSFER VALIDATION:** critical precedent for separating origin mutation/cache invalidation from downstream fleet convergence. `origin corrected ≠ every cache/client corrected`.

### WebKit — Web Push is available to iOS/iPadOS Home Screen web apps, but is permission/platform state
WebKit documents Web Push for Home Screen web apps on iOS/iPadOS and user-controlled notification permissions. Current WebKit also documents Declarative Web Push on iOS/iPadOS 18.4. These capabilities can accelerate notification of a correction/revocation but cannot be treated as a mandatory reliable acknowledgement channel.

Sources:
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- https://webkit.org/blog/16535/meet-declarative-web-push/

**CHANGE WATCH:** browser/OS capability and policy remain version-specific. Push support or successful send is not proof that an offline EFB received/applied the semantic revocation.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Software Engineering Studio remains Foundation-in-study with no specialist Foundation PASS; its bounded Safari lifecycle evidence does not establish product dispute/revocation semantics. Product runtime validation therefore remains OPEN.

## SYNTHESIS 1 — escalation authority must be consequence-scoped
Escalation should identify:
- dispute identity and subject scope;
- current unresolved consequence(s);
- escalation trigger/reason;
- eligible reviewing role or authority source;
- powers granted at that escalation level;
- powers explicitly not granted;
- validity interval/expiry if temporary;
- predecessor decision state;
- evidence required for closure;
- appeal/reopen route where applicable.

A support operator who may route a dispute is not thereby authorized to settle it. A security administrator who can quarantine a record is not thereby authorized to determine aviation/logbook truth. A supervisor authorized for one organization/crew/time range is not automatically authorized globally.

Guards: `escalated ≠ universally privileged`; `can route ≠ can resolve`; `can quarantine ≠ can rewrite`; `admin role ≠ domain authority`.

## SYNTHESIS 2 — escalation must not erase separation of duties
Where consequence warrants separation, proposal, evidence review, approval and publication can remain distinct. Escalation may select a higher authorized role or a defined quorum, but must not silently collapse all stages into one actor merely because a deadline elapsed.

Emergency handling can temporarily narrow consequences (for example, hold export/publication) without manufacturing a semantic winner.

Guards: `deadline exceeded ≠ reviewer becomes approver`; `incident urgency ≠ provenance optional`; `temporary containment ≠ final correction`.

## SYNTHESIS 3 — distinguish resolution expiry from resolution falsity
A resolution can cease to govern because:
- its explicit validity interval ended;
- its authority scope ended;
- successor policy requires reconsideration;
- new evidence triggers reopen;
- an appeal/reversal is accepted;
- a dependent premise was invalidated.

That does not mean the earlier resolution was fraudulent or never valid. Preserve the historical decision and record why it stopped governing.

Guards: `expired ≠ false`; `reopened ≠ never resolved`; `superseded ≠ deleted`; `current inapplicable ≠ historical evidence worthless`.

## SYNTHESIS 4 — reopening is a new governed transition
Do not mutate `RESOLVED` back to `DISPUTED` without provenance. A reopen event should cite:
- prior resolution;
- reopening actor/authority;
- trigger/new evidence;
- affected consequence scope;
- policy generation;
- resulting provisional state;
- whether prior downstream projection must be revoked.

This yields a chain such as:
`D7 DISPUTED → R8 RESOLVED → O9 PUBLISHED → X10 REOPENED → V11 DOWNSTREAM-REVOKED → R12 RESOLVED`.

The current projection can point to R12 while preserving R8/O9/V11 as historical facts.

## SYNTHESIS 5 — downstream publication creates a revocation obligation
Once a resolved projection is exported, synced, cached, indexed, rendered into a report or consumed by another device, a later reversal creates a downstream convergence problem.

Maintain enough state to identify at least:
- projection/version admitted by recipient;
- subject logical record/revision;
- successor/revocation generation;
- reason class without overexposing sensitive dispute payload;
- consequence scope;
- acknowledgement/application state where available;
- minimum acceptable projection floor.

Guard: `source corrected ≠ downstream corrected`; `revocation emitted ≠ revocation applied`.

## SYNTHESIS 6 — invalidation is not global merely because origin/cache changed
RFC 9111's cache semantics make the limitation explicit: state-changing requests invalidate affected traversed caches, not every copy everywhere. Application exports, offline IndexedDB copies, screenshots/files, native sync replicas and reports may sit outside HTTP cache invalidation entirely.

Therefore separate:
1. canonical source reversal;
2. HTTP/CDN cache invalidation;
3. connected-client update;
4. offline-client pending revocation;
5. exported/third-party artifact remediation;
6. human/organizational notification where required.

Guard: `cache invalidated ≠ replica invalidated`; `200/204 mutation success ≠ fleet convergence`.

## SYNTHESIS 7 — push is a hint/transport, not revocation authority or receipt proof
Web Push can notify supported Home Screen web apps, but user permission, OS delivery, installation state and connectivity vary. A push payload must not itself become semantic authority merely because it arrived through a platform push channel.

A safe pattern is: push/wakeup hint → authenticated current-state fetch when possible → monotonic lineage/floor check → local application → durable acknowledgement. Offline clients retain pending debt until they can perform the authenticated transition.

Guards: `push sent ≠ push received`; `push received ≠ state applied`; `notification permission ≠ background convergence guarantee`; `push payload ≠ canonical truth`.

## SYNTHESIS 8 — offline recipients need monotonic revocation floors
A long-offline PWA can reconnect with projection P8 after canonical history reached P12 and revoked P8. The client should not be forced to erase unique local data. It should instead:
1. preserve local unique records/provenance;
2. obtain current authenticated bootstrap/policy;
3. compare local projection/checkpoint to current minimum floor;
4. mark affected local projection `STALE/REVOKED-PENDING`;
5. fetch/reconcile successor chain;
6. revalidate queued operations against current lineage;
7. admit/publish only current-authorized state;
8. preserve historical P8 as provenance where policy permits.

Guard: `projection obsolete ≠ local unique data disposable`.

## SYNTHESIS 9 — downstream revocation must be idempotent and replay-safe
Recipients can receive the same revocation multiple times or receive successor state before an older revocation message. Revocation application therefore needs stable subject/projection identity and generation/predecessor rules.

Examples:
- receiving `revoke P8 because P12 supersedes` twice must not create two domain effects;
- receiving stale `revoke P8 → P10` after P12 is current must not roll back to P10;
- restoring a backup containing P8 must not clear the durable minimum floor that already requires P12.

Guards: `duplicate revocation ≠ duplicate effect`; `older revocation received later ≠ rollback authorized`; `backup restored ≠ revocation forgotten`.

## SYNTHESIS 10 — partial downstream convergence is explicit debt
Track each material recipient class rather than claiming closure from the online majority. Useful states include:
- `CURRENT-ACKNOWLEDGED`;
- `CURRENT-INFERRED` only where inference is explicitly justified;
- `REVOKED-PENDING`;
- `OFFLINE/UNKNOWN`;
- `EXPORT-OUTSIDE-CONTROL`;
- `RECIPIENT-RETIRED` with evidence;
- `REMEDIATION-REQUIRED`.

Closure criteria depend on consequence. A low-risk display cache and a regulatory/export artifact need not share the same threshold. Unknown recipients are not silently dropped from the denominator.

Guard: `online recipients current ≠ all downstream consequences remediated`.

## SYNTHESIS 11 — revocation scope should minimize privacy leakage
A revocation signal need not expose the full dispute narrative. Where possible, send stable record/projection identity, successor generation, action required and bounded reason class; fetch sensitive details only after current authorization.

This preserves Track E security/privacy and Track D measurement boundaries: analytics may count stale/revoked classes and latency without becoming a duplicate store of sensitive correction evidence.

Guard: `revocation needs routing identity ≠ analytics needs dispute payload`.

## SYNTHESIS 12 — consequence-specific publication states avoid false finality
A record may be:
- locally readable;
- blocked from final export;
- allowed in a provisional internal view;
- excluded from public/search projection;
- pending supervisor/domain review;
- superseded but retained historically.

Do not compress these into one boolean `valid`. Track B must present consequence and uncertainty clearly; Track D must not index/measure provisional content as settled truth; Track E defines policy; Track C validates leakage boundaries.

## SYNTHESIS 13 — Service Worker update is not a semantic revocation mechanism
A new Service Worker can change code/cache behavior, but it does not prove that every controlled/uncontrolled client, IndexedDB record, export or native peer applied a domain correction. `skipWaiting()`/controller replacement cannot stand in for record-level revocation acknowledgement.

Guard: `Service Worker current ≠ projection current`; `cache version advanced ≠ data revocation applied`.

## SYNTHESIS 14 — reopening must not permit authority replay
A historically valid reviewer whose authority ended cannot use the existence of the old resolution to reopen/resolve a new dispute unless current policy still grants that power. Conversely, a current reviewer must not rewrite historical authorship/approval.

Bind reopen/resolution events to current authority generation and scope while retaining predecessor authority evidence.

Guards: `resolved by me before ≠ may resolve now`; `current approver ≠ historical approver`.

## SYNTHESIS 15 — revocation closure needs positive and negative evidence
A robust closure test should show both:
- successor/current projection is accepted; and
- predecessor/revoked projection is rejected or quarantined at the relevant consequence boundary.

For offline/recovery paths, also test backup restore, stale Service Worker/cache, delayed message order and queued mutation replay.

Guard: `successor visible ≠ predecessor impossible to republish`.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. model escalation as scope-limited authority, never role inflation;
2. preserve resolution/reopen/reversal as immutable provenance transitions;
3. separate historical validity from current applicability;
4. version downstream projections and maintain monotonic acceptance floors;
5. treat revocation delivery, receipt, semantic application and acknowledgement as distinct states;
6. keep offline/unknown recipients as explicit convergence debt;
7. use push/cache/SW mechanisms only as transport/acceleration, never authority proof;
8. recover stale offline clients by preserving unique data and reconciling lineage, not destructive reset;
9. require replay/rollback-safe revocation handling across restore/rejoin;
10. require negative predecessor-rejection evidence before claiming consequence-level closure.

These are generic architecture decisions. Actual LogMate/MintTap roles, correction authority, aviation/legal consequences, backend transactions, export formats and MDM/PWA runtime behavior remain OPEN.

## EFB / LogMate-like application case
Assume an iPad Home Screen PWA accepted projection P8 while online, then remained offline. Server-side dispute resolution later produced P9, published it, reopened it after new evidence, revoked P9 and settled on P12. The iPad returns with unique unsynced flight data plus queued operations based on P8.

Safe sequence:
1. preserve unique local data and local provenance;
2. isolate outbound consequence-bearing mutation until current authority is known;
3. authenticate current bootstrap/policy and projection floor;
4. learn that P8/P9 are superseded/revoked without deleting their historical evidence;
5. reconcile P8→P12 lineage and schema/data migrations;
6. rebase/revalidate each queued operation against P12;
7. classify conflicts rather than timestamp-electing a winner;
8. admit current-authorized records/operations;
9. record durable revocation/currentness acknowledgement;
10. test restart/restore/offline relapse so P8/P9 cannot become publishable again.

Push may shorten discovery when supported and permitted, but the architecture cannot require a push to have been delivered while the device was offline.

## Track B transfer — UX state contract
A future product UI should distinguish at least:
- unresolved dispute from resolved state;
- resolved from reopened;
- historical/superseded from current;
- locally readable from final/exportable;
- sync waiting from authority review waiting;
- stale local projection from data-loss error.

Do not use a generic red error that pressures users to delete/re-enter unique records. Exact language, interaction, screen-reader behavior and representative-human comprehension require Design Studio/runtime validation.

## Track D transfer — measurement contract
Measure separately:
- disputes opened/escalated/resolved/reopened;
- resolution age and reopen latency;
- projection generations issued;
- revocations emitted/delivered/applied/acknowledged where observable;
- offline/unknown recipient inventory;
- predecessor rejection failures;
- export/remediation classes.

Do not use analytics arrival order, majority count or notification delivery as semantic authority evidence. Minimize sensitive dispute payload in telemetry.

## Track C destructive campaign — 808 → 816 defined cases
Add eight generic destructive cases:
1. **Escalation role inflation:** routing/support role becomes universal resolver after timeout → reject.
2. **Expiry-as-history deletion:** expired resolution is erased and predecessor provenance disappears → reject.
3. **Origin-corrected global-convergence theater:** canonical record changes and system declares every recipient current without downstream evidence → reject.
4. **Push-delivery authority theater:** successful push send/delivery is treated as semantic revocation acknowledgement → reject.
5. **Service-Worker-version revocation theater:** new SW/cache version is treated as proof all local records/exports applied revocation → reject.
6. **Delayed-revocation rollback:** client at P12 receives old P8→P10 revocation and rolls back to P10 → reject.
7. **Backup revocation amnesia:** restore resurrects P8 as publishable despite durable floor P12 → reject.
8. **Offline-tail destructive convergence:** returning iPad is wiped because its projection is stale even though it contains unique unsynced data → reject.

**VALIDATION:** 816 cases are defined, not executed. Physical-device, AT, human, backend and product runtime PASS is not claimed.

## OPEN
- actual product/domain escalation hierarchy and authority matrix;
- legal/aviation requirements for correction, appeal, export and notification;
- actual logical-record/projection/revocation identifiers;
- backend transaction/outbox/event-stream semantics;
- recipient registry and acknowledgement durability;
- actual Service Worker/IndexedDB/cache/update behavior;
- installed Home Screen PWA and managed-iPad push/background behavior;
- export/report remediation capability;
- native-mobile ↔ PWA sync topology;
- privacy classification for dispute/revocation payloads;
- screen-reader, human comprehension and physical-device validation.

## DEPENDENCY / HANDOFF
- **Software Engineering:** implementation-level outbox/idempotency/precondition/replay-ledger and projection-floor validation when canonical product source/runtime is available.
- **Design Studio Web:** dispute/reopen/revocation/stale-local UX and accessibility validation; current W121 gate remains NOT PASSED.
- **Marketing:** no ownership transfer. Public/support messaging may consume final verified incident/correction facts but must not define technical/domain authority.

## CHANGE WATCH
- WebKit/iOS/iPadOS Web Push, Home Screen web-app and background behavior;
- Service Worker lifecycle/cache behavior across Safari/WebKit versions;
- NIST 800-53 minor releases;
- product/legal/aviation rules if/when canonical evidence becomes available.

## Gate assessment
**PASS (generic).** The Web Manager can distinguish escalation from authority inflation; historical validity from current applicability; origin/cache mutation from downstream convergence; notification from acknowledgement; and stale offline projection from disposable local data. It can specify a replay/rollback-safe downstream revocation model and destructive validation campaign while preserving product/runtime unknowns.

## Next high-value target
**258 — revocation-delivery ledger durability, acknowledgement forgery resistance & export-remediation closure.** Study how to prove which recipients actually applied a revocation without trusting self-reported currentness; preserve delivery/application evidence across backup/restore and device reincarnation; handle recipients outside organizational control; and close export/report remediation without pretending immutable external copies can be remotely deleted.