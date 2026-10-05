# 316 — LogMate PWA Dedup/Receipt Retention, TTL Deletion & Long-Offline Replay Gate

Status: **PASS (generic/platform) / production validation OPEN**
Evidence date: 2026-10-06
Primary owner: **Track E — Web Architecture, Security & Operations**
Dependency: 315 foreground convergence / UNKNOWN-commit / stable-operation identity.

## SOURCE

Cloud Firestore TTL expiration is not immediate physical deletion. Expired documents can remain visible until deletion, normally within 24 hours. TTL deletions are not transactional, equal-expiry documents need not disappear together or in expiry order, and deleting a parent by TTL does not delete subcollections.

- https://firebase.google.com/docs/firestore/ttl

Firestore transactions atomically apply successful writes and provide serializable isolation, but transaction functions can be retried after contention and may execute more than once.

- https://firebase.google.com/docs/firestore/manage-data/transactions
- https://firebase.google.com/docs/firestore/transaction-data-contention

RFC 9110 explains that idempotent semantics matter when communication fails before a response is read because the original request may already have succeeded.

- https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods

## SYNTHESIS

Dedup/receipt retention is part of Sync correctness, not merely database cleanup. Separate:

1. **replay horizon** — how long a supported stale client/backup can present an old operation;
2. **admission-memory horizon** — how long the authority can recognize its prior outcome;
3. **physical-deletion horizon** — when retained metadata is actually erased.

Guards:
- `TTL configured ≠ deletion completed`;
- `TTL expired ≠ document absent`;
- `TTL expiration ≠ atomic protocol retirement`;
- `dedup record absent ≠ operation never committed`;
- `receipt deleted ≠ stale replay safe`;
- `supported replay horizon > admission-memory horizon ≠ replay-safe`;
- `replay safety ≠ retain full flight payload forever`.

Inside the supported horizon, replay of one stable operation identity must resolve to the prior authoritative outcome without a second material effect. Beyond authoritative memory, a dedup miss must not silently become new intent. The product contract needs an explicit fence: reconciliation/bootstrap, stale-operation rejection/quarantine, retained lineage evidence, or explicit adjudication.

## PRIVACY / DELETION

Replay safety does not automatically justify indefinite flight-payload retention. Separate minimum protocol evidence—operation identity, required subject binding, contradiction evidence, outcome/receipt, reconciliation reference and expiry metadata—from full operational payload where possible.

Account deletion is a replay boundary: a stale iPad or restored backup must not silently recreate deleted remote data or authority. Exact retention fields/durations and legal/aviation obligations remain OPEN.

## BACKUP / MIGRATION

A backup can preserve operation identities longer than an ordinary device lifecycle. Therefore replay-horizon analysis includes old-backup restore, device replacement and protocol/schema migration.

Guards:
- `backup restored ≠ operation becomes new`;
- `old schema parseable ≠ old operation admissible`;
- `protocol migration ≠ dedup lineage reset`;
- `device replacement ≠ authorization continuity proven`.

## CROSS-TRACK TRANSFER

Track A owns retry/lifecycle mechanics. Track B needs a “Needs verification” recovery state rather than falsely calling UNKNOWN/stale operations failed. Track C extends 315 fault injection across retention boundaries. Track D may observe stale-replay/receipt-age/TTL-delay classes without collecting flight payload. Track E owns replay horizon, admission memory, deletion/privacy and stale-return adjudication.

## VALIDATION

Retain 315 cases 1–28 and add:
29. replay just before admission-memory expiry;
30. replay after expiry eligibility but before physical deletion;
31. replay after physical dedup deletion;
32. partial deletion among equal-expiry receipts;
33. deletion order differs from operation order;
34. parent receipt deleted while subordinate evidence remains;
35. old backup restored inside supported horizon;
36. old backup restored beyond supported horizon;
37. account deleted then stale iPad reconnects;
38. superficially similar account recreated but old operation does not inherit authority;
39. protocol/schema migration with old pending operations;
40. payload deletion while permitted minimum anti-replay evidence remains, or an alternate explicit fence if that evidence must also be erased.

## MINTTAP DECISION

For LogMate-like PWA/EFB Sync, retention is a correctness-and-privacy contract. Do not choose a duration until supported offline/restore horizons, deletion obligations, actual Sync schema and authoritative admission semantics exist. Firestore TTL may implement cleanup; it cannot define correctness by itself.

## OPEN

Canonical LogMate `main` remains `059d643f080781cce71f1bd00ccef659a446de8c`. No production Sync admission/dedup/receipt/reconciliation/retention contract is currently evidenced. Physical Safari/Home-Screen and representative managed-EFB validation remain OPEN.

## Gate

**PASS generic. NO production PASS.**
