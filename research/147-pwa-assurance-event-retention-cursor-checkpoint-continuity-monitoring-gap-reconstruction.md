# 147 — PWA Assurance-Event Retention, Cursor/Checkpoint Continuity & Monitoring-Gap Reconstruction

Status: **PASS (generic) / PRODUCT + PROVIDER-RETENTION + CURSOR + EVENT-STORE + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 143–146; Track A runtime/SW/device-generation observability; Track C loss/replay/restore validation; Track B uncertainty UX; Track D bounded monitoring-health telemetry.

## Why this study exists

146 established authenticated change-event admission and current-state reconciliation. It deliberately left one harder question open: after retention expiry, cursor loss, compaction, backup restore or a long monitoring outage, what interval can the system honestly claim was observed?

A local `lastProcessedEvent` value can prove only what its source semantics and durable processing protocol actually support. A successful current-state poll can recover **now** without reconstructing every transition that happened while monitoring was blind. The objective is therefore not fictional perfect history; it is explicit **coverage provenance, gap detection, bounded reconstruction and consequence-aware revalidation**.

## SOURCE

### Long-term event/log evidence requires retention, accessible formats and transfer-integrity checks
NIST SP 800-92 §5.4 requires log retention to follow organizational requirements, warns that long-lived archives can become unreadable when formats/software disappear, recommends periodic archive-format review/migration, and calls for integrity verification when logs are transferred. This supports treating retention, readability and transfer integrity as separate properties rather than assuming an archived blob proves monitoring continuity.

Source: https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.pdf

### Continuous monitoring is ongoing visibility, not a stored-cursor claim
NIST SP 800-137 frames information-security continuous monitoring as ongoing visibility into assets, threats/vulnerabilities and control effectiveness sufficient to support risk response. A monitoring outage therefore degrades visibility even if a local cursor remains intact.

Source: https://doi.org/10.6028/NIST.SP.800-137

### Event ordering metadata is scoped to the producer/source semantics
The CloudEvents Sequence extension defines ordering only within the scope of a unique event `source`; its sequence value is producer-defined. It recommends monotonically increasing/contiguous values but does not turn arbitrary event systems into gap-free durable logs. This is transfer evidence for the rule that a cursor/sequence can support completeness only when the upstream contract actually guarantees the needed properties.

Source: https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/sequence.md

### Durable buffering reduces loss but does not create unlimited retention
OpenTelemetry Collector resiliency documentation distinguishes in-memory queues, persistent/WAL-backed queues and external message queues, and explicitly describes loss conditions including queue overflow, retry exhaustion and storage failure. This is operational transfer evidence: durable local processing state improves crash recovery but does not prove upstream completeness or infinite catch-up.

Source: https://opentelemetry.io/docs/collector/resiliency/

## SYNTHESIS — five different continuity claims

Do not collapse these:

1. **SOURCE RETENTION** — the upstream source still exposes historical events for an interval.
2. **SOURCE ORDER/COVERAGE** — source semantics let a consumer determine whether positions between two boundaries are complete.
3. **LOCAL INGESTION** — the local system durably received/admitted events.
4. **LOCAL PROCESSING** — admitted events were idempotently processed into dependency transitions.
5. **CURRENT-STATE OBSERVATION** — reconciliation can verify the dependency state now.

Persistent guards:
- `cursor stored ≠ source history retained`;
- `cursor advanced ≠ every source event received`;
- `sequence ordered ≠ sequence gap-free`;
- `contiguous-looking IDs ≠ completeness guaranteed`;
- `event archive present ≠ archive readable ≠ archive integrity verified`;
- `local event store complete ≠ upstream source complete`;
- `current state recovered ≠ intermediate transitions reconstructed`;
- `backup restored ≠ monitoring coverage restored`;
- `compaction successful ≠ discarded evidence reconstructable`;
- `no known gap ≠ proven continuous coverage`.

## Coverage ledger, not one global cursor

A future implementation should represent monitoring coverage by **source/dependency stream and interval**, not a single global `lastEventId`.

Minimal conceptual record:

`sourceId | dependencyScope | sourceEpoch | startBoundary | endBoundary | boundarySemantics | sourceGuarantee | localCheckpoint | coverageState | observedGap | archiveRef/digest | reconciliationRef | provenance`

`sourceEpoch` matters because provider resets/migrations may make the same cursor namespace incomparable across epochs.

### Coverage states

Use explicit states such as:
- **PROVEN-CONTIGUOUS** — source contract plus verified boundaries support completeness for the interval;
- **OBSERVED-NONCONTIGUOUS** — events were observed but source semantics cannot prove no omissions;
- **GAP-KNOWN** — loss/outage/retention expiry establishes missing coverage;
- **CURRENT-STATE-RECOVERED / HISTORY-GAPPED** — reconciliation establishes now but not all transitions;
- **RECONSTRUCTED-BOUNDED** — some transitions are recovered from independent durable evidence, with limits recorded;
- **UNOBSERVABLE** — neither retained history nor current state can presently be verified;
- **SUPERSEDED** — an old source epoch no longer governs current monitoring but remains historical evidence.

Do not render OBSERVED-NONCONTIGUOUS as green continuous coverage.

## Cursor semantics must come from the source contract

A cursor can mean very different things: opaque pagination token, offset, monotonically increasing sequence, timestamp boundary, stream position or provider-specific continuation token. Before using one for completeness, verify:

1. scope: account/tenant/resource/partition/source;
2. ordering guarantee;
3. uniqueness guarantee;
4. whether positions are contiguous or sparse;
5. retention horizon and expiry behavior;
6. replay/redelivery semantics;
7. cursor invalidation/reset behavior;
8. snapshot/consistency behavior while paginating;
9. whether deleted/compacted events leave detectable gaps;
10. provider migration/version semantics.

If unknown, treat the cursor as a **resume hint**, not completeness proof.

`resume token ≠ audit checkpoint`.

## Durable processing checkpoint

Where source semantics support it, checkpoint advancement should be coupled to durable local admission/processing semantics strongly enough that a crash cannot silently skip work.

Conceptual order:
1. fetch/receive source event range;
2. authenticate and semantically admit under 146;
3. durably record event/provenance;
4. apply idempotent dependency transition and 145 targeted propagation;
5. durably record processing result;
6. advance local source checkpoint only to the highest boundary justified by the source contract.

A checkpoint ahead of durable processing can create a silent skip after restart. A checkpoint behind processing is usually recoverable through idempotent replay but may increase duplicate work.

`checkpoint persisted ≠ effects persisted`.
`effects persisted ≠ checkpoint persisted`.

The exact atomicity mechanism is implementation-specific and remains a Software Engineering handoff.

## Retention expiry and long outage

When the consumer resumes after the source's recoverable history window:

1. preserve the last proven coverage boundary;
2. record a **known monitoring gap** from that boundary to the earliest defensible recovered boundary;
3. reconcile current provider/runtime state under 146;
4. use independently retained artifacts only for transitions they actually evidence;
5. apply 145 invalidation from the earliest defensible uncertainty/change window;
6. revalidate consequence-bearing claims affected by the unknown interval;
7. never invent intermediate events merely to make the timeline continuous.

If the final state equals the pre-gap state, do not infer that no transient security-relevant change occurred.

`same state before/after gap ≠ no transition occurred during gap`.

## Compaction and archive checkpoints

Compaction may be justified for cost/privacy/operability, but it changes what can later be proven. Before discarding raw events, preserve only the minimum evidence required by the assurance claim, potentially including:
- covered source/epoch and interval boundaries;
- source guarantee used;
- event-count/range metadata where meaningful;
- digest/checkpoint of the retained archive/range;
- admitted dependency transitions and provenance;
- known gaps/contradictions/exceptions;
- format/schema/verifier context required to read retained evidence.

A digest of discarded events proves integrity only relative to content that can still be obtained/verified; it does not reconstruct deleted payloads.

`archive digest retained ≠ archived events recoverable`.

NIST SP 800-92's warning about future readability applies: retained evidence that cannot be parsed years later is weak operational evidence.

## Backup restore and checkpoint rollback

Restoring an older event-store backup can roll local cursors, processing state and coverage metadata backward. Do not simply trust restored `lastProcessed` as current.

Recovery pattern:
- identify backup generation and last independently known coverage/checkpoint;
- compare restored source epoch/cursor against current source semantics;
- replay retained upstream history if still available and idempotent;
- reconcile current state;
- mark any unrecoverable interval explicitly gapped;
- prevent a stale backup from lowering anti-rollback/trust floors established by 139–140.

`backup internally consistent ≠ backup current`.

## PWA / EFB application

A long-offline company iPad is not itself proof of server monitoring continuity. Separate at least:
- server/provider assurance-event coverage;
- served application/runtime release history;
- Service Worker activation/control observed on that device;
- local data/operation history on the iPad;
- MDM/WebKit/device-policy observations when actually available.

If an iPad reconnects after multiple server monitoring gaps, local flight records remain preservable. Remote mutation authority can remain gated until relevant current trust state is reconciled. Do not demand that the iPad reconstruct server events it could never observe.

`device offline interval ≠ server monitoring gap`.
`server monitoring gap ≠ local data loss`.
`server event archive complete ≠ device activation history complete`.

## Cross-track transfer

### Track A — Platform & Browser
Own observable Service Worker/runtime/storage/device generation semantics. A page/SW-local version marker is scoped device evidence, not a provider event cursor.

### Track B — UX / IA
Consume `history gapped`, `current state recovered`, `revalidation required` and `remote authority gated` states. Avoid user-facing claims such as “fully verified” when only current state is known.

### Track C — Quality
Own cursor reset, retention expiry, replay, duplicate, partial processing, backup restore, compaction/readability and gap-reconstruction tests. Preserve scenario IDs and provenance.

### Track D — Search / Analytics
Monitoring-health metrics may expose lag, oldest retained boundary, queue depth and gap duration. Analytics remains diagnostic, not a completeness oracle.

### Track E — Owner
Own source-contract interpretation, coverage ledger, retention/compaction policy, gap classification, reconciliation consequences and assurance claims.

## MINTTAP DECISION — minimal viable pattern

Do not build an enterprise event-sourcing platform. If product implementation requires this capability, preserve the smallest set that prevents false confidence:
1. source-specific cursor/retention contract;
2. durable source/dependency coverage boundaries;
3. idempotent event admission/processing;
4. explicit source epoch/reset handling;
5. known-gap and unknown-coverage states;
6. reconciliation after outage/retention loss;
7. targeted assurance invalidation/revalidation;
8. compaction/archive provenance and readability requirements;
9. backup-restore reconciliation;
10. separate server/provider coverage from physical PWA/device evidence.

Retention duration is product/provider/legal/risk dependent. No universal MintTap number is set here.

## VALIDATION — 30-case campaign

1. ordered contiguous source resumes without gap; 2. opaque cursor treated only as resume token; 3. sparse sequence not misclassified as missing events; 4. guaranteed contiguous sequence detects one missing position; 5. duplicate delivery after resume is idempotent; 6. out-of-order delivery preserves correct boundary semantics; 7. cursor expires inside retention window; 8. retention expires during outage; 9. source resets cursor namespace and increments source epoch; 10. provider silently changes cursor semantics and CHANGE WATCH catches contract drift; 11. local event persisted but checkpoint write fails; 12. checkpoint persisted before effect and destructive test exposes skip risk; 13. effect persisted but ACK/checkpoint fails and replay remains idempotent; 14. queue overflow produces explicit coverage degradation; 15. current-state reconciliation after gap succeeds but history remains gapped; 16. pre/post state equal across gap does not assert no transient change; 17. independent deployment evidence reconstructs only one bounded transition; 18. contradictory archive/provider evidence remains open; 19. compaction preserves required boundary/provenance; 20. compacted archive digest exists but payload unavailable and recoverability is not claimed; 21. archived format becomes unreadable and revalidation flags evidence degradation; 22. archive transfer integrity mismatch is detected; 23. stale backup rolls cursor backward and retained upstream history is replayed safely; 24. stale backup plus expired upstream retention creates explicit gap; 25. stale backup cannot lower trust floor; 26. long-offline iPad reconnect is not confused with server monitoring gap; 27. server event coverage does not claim SW activation on physical iPad; 28. source/API outage plus local collector restart tests persistent-queue limits; 29. two partitions/sources never compare unrelated cursors; 30. end-to-end outage → retention expiry → current-state recovery → targeted revalidation leaves no false continuous-green interval.

## CONTRADICTION / failure-mode analysis

### Cursor theater
A sophisticated cursor table cannot prove more than the upstream source guarantees. Opaque continuation tokens are not automatically audit checkpoints.

### Retention theater
Keeping events for a long time is not useful if integrity, provenance or future readability is missing.

### Reconciliation theater
Current-state recovery closes operational uncertainty about now; it cannot manufacture an unknown transition history.

### Backup theater
A restored database can be transactionally valid while being security-obsolete.

### Compaction theater
A compact summary can preserve selected claims, not all facts that raw events once contained.

## OPEN

Actual MintTap/LogMate providers, retention windows, cursor/sequence semantics, event partitions, source epochs, archive formats, event volume, legal/privacy retention requirements, event-store architecture, transaction boundaries, backup generations, independent reconstruction evidence, MDM/device observability and physical-iPad behavior are unknown. No production PASS is claimed.

## CHANGE WATCH

- Provider cursor, replay, webhook/event retention and pagination semantics are provider-specific and can change; verify selected provider documentation at implementation time.
- CloudEvents Sequence is an extension and its semantics remain source-scoped; do not infer provider guarantees merely from field presence.
- OpenTelemetry is transfer evidence for buffering/loss mechanics, not a MintTap architecture requirement.
- NIST SP 800-92 is durable log-management guidance but old; use it for retention/integrity/readability principles, not current product-specific retention periods.
- Browser/WebKit/MDM observability remains platform/version sensitive.

## Gate result

**PASS (generic).** The Web Manager can now distinguish source retention/order guarantees, local ingestion/processing checkpoints and current-state reconciliation; model monitoring coverage by source/epoch/interval; reconstruct only what evidence supports; preserve explicit gaps; and prevent stale backups/compaction from creating false continuity.

Production/provider/managed-EFB runtime assurance remains **OPEN**.

## Next highest-value adjacent question

**PWA assurance coverage SLOs, lag/gap severity & consequence-based escalation.** Once coverage can be represented honestly, the next bottleneck is deciding when delayed monitoring, an unrecoverable gap or an unobservable dependency is merely degraded telemetry versus a condition that must block release/recovery/remote mutation. The decision should be consequence- and dependency-class based rather than one universal timeout.