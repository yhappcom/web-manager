# 153 — PWA Policy-Retirement Proof, Orphaned-Lease Detection & Tombstone/Anti-Resurrection Governance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + REPLICA/BACKUP-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 145 evidence graph/invalidation; 146 event authenticity/reconciliation; 147 retention/gap reconstruction; 149 policy composition; 151 cross-generation consistency; 152 retirement/lease horizons; Track A runtime/SW/storage generations; Track B truthful recovery UX; Track C restore/replica/orphan destructive validation; Track D aggregate diagnostics only.

## Why this study exists

152 defines when predecessor policy G1 should stop authorizing and how already-admitted work can drain under bounded leases. That is necessary but not sufficient. A stale replica, restored backup, orphaned lease record, missing retirement marker, or client-carried predecessor material can reintroduce state that looks locally valid after G1 is supposed to be gone.

The problem is therefore not merely deletion. It is **anti-resurrection**: later state must not be able to erase the security fact that an older authority epoch was retired or revoked.

## SOURCE

### OWASP — invalidation must be authoritative server-side
OWASP Session Management and Web Security Testing guidance require expired/logged-out sessions to be invalidated server-side and specifically test that replaying a previous identifier cannot restore access. Transfer lesson: removing client material is insufficient if an older authoritative copy can still accept it.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/07-Testing_Session_Timeout/
- https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/06-Session_Management_Testing/06-Testing_for_Logout_Functionality/

### OWASP — transaction authorization belongs on the server
OWASP Transaction Authorization guidance requires authorization and the selected authorization method to be enforced server-side. Client-controlled data must not disable or alter the authorization decision.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html

### etcd — deletion is represented as a tombstone within a generation
The etcd MVCC data model records monotonically increasing store revisions. Deleting a key generates a tombstone ending that key generation. Compaction can later remove old generations/history. This is useful structural transfer evidence: a deletion/retirement fact has lifecycle and retention semantics, and compaction can remove historical proof if the application needs that proof longer.

Sources:
- https://etcd.io/docs/v3.6/learning/data_model/
- https://etcd.io/docs/v3.5/op-guide/maintenance/

### etcd — replica divergence needs explicit detection
etcd documents initial and periodic corruption checks that compare member state and raise an alarm on mismatch. Transfer lesson: assuming replicas agree is weaker than explicitly reconciling/verifying them.

Source: https://etcd.io/docs/v3.6/op-guide/data_corruption/

### Kubernetes — deletion can require finalization before disappearance
Kubernetes finalizers keep an object in terminating state until declared cleanup conditions are completed. This is transfer evidence for a two-phase retirement concept: `retirement requested` and `retirement finalized` need not be the same fact.

Source: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/

## SYNTHESIS — retirement is a monotonic security fact

A useful generic model distinguishes:

1. **RETIREMENT-INTENT RECORDED** — G1 is no longer eligible for arbitrary new authority according to rollout policy.
2. **DRAINING / REVOKING** — bounded leases are being completed, expired or invalidated.
3. **RETIREMENT-FINALIZABLE** — declared authoritative lease/replica/provider checks are satisfied for the stated scope.
4. **RETIRED-FINALIZED** — G1 cannot authorize within the declared authoritative scope.
5. **HISTORICAL-VERIFICATION-ONLY** — retained G1 evidence can be interpreted but cannot become execution authority.

For security-sensitive retirement, a later restore must merge against a **retirement floor** or equivalent current authority epoch rather than replacing current state wholesale with older state.

Persistent guards:
- `row deleted ≠ authority retired`;
- `retirement flag absent ≠ predecessor active`;
- `backup older than retirement ≠ permission to roll authority back`;
- `lease record exists ≠ lease admissible`;
- `lease missing from one index ≠ lease consumed everywhere`;
- `replica caught up ≠ every offline client observed`;
- `fleet-zero unobserved ≠ retirement unprovable`;
- `tombstone retained ≠ full historical payload retained`;
- `tombstone compacted ≠ retirement may be forgotten`;
- `historical verifier retained ≠ historical authority restored`.

## Retirement floor / anti-resurrection state

The exact implementation is product/provider-specific, but the semantic state should bind enough information to reject stale predecessor authority. A generic retirement fact may include:
- policy/trust generation identifier;
- successor/current authority generation or minimum accepted epoch;
- retirement/revocation reason class;
- effective server-authoritative revision/epoch;
- whether ordinary drain or emergency revocation applies;
- finalization state and evidence references;
- provenance/authentication of the retirement transition;
- retention/compaction rules for the minimal anti-resurrection fact.

This fact is not necessarily a literal database tombstone. `tombstone` here denotes durable negative authority state. The implementation may be an epoch floor, revocation set, append-only transition, provider-native disable state, or another authenticated mechanism.

### Monotonic merge rule

When current state and restored/stale state disagree, security-retirement state must not use naive last-write-wins or backup-wins semantics. A restore older than the retirement floor may recover historical data, but cannot lower the current accepted authority epoch.

A safe conceptual merge is:
- preserve recoverable historical/business data;
- preserve current retirement/revocation floor;
- revalidate surviving leases against current floor;
- reject predecessor execution authority below the floor;
- record uncertainty when the authoritative floor itself cannot be established.

`newer backup timestamp ≠ newer authority state`; authority ordering comes from authenticated policy/trust lineage, not file mtime or device clock.

## Orphaned-lease detection

An **orphaned lease** is a lease-like authority record whose expected owning transaction, principal/device context, policy generation, revocation epoch, completion state or authoritative index relationship cannot be reconciled.

Examples:
- lease exists but transaction record is absent;
- transaction says completed but lease still appears executable;
- lease references retired G1 and lacks a current bounded exception;
- lease restored from backup after its consumption/expiry marker;
- one replica retains the lease while authoritative state marks it revoked;
- lease is syntactically valid but its trust/device epoch is no longer current;
- duplicate lease identities disagree on payload fingerprint or completion.

Default generic treatment for consequence-bearing remote mutation: **orphaned/ambiguous authority is not a permit**. Preserve evidence for diagnosis; do not silently delete the only evidence of the inconsistency before reconciliation.

## Finalization and proof scope

A claim such as `G1 RETIRED` must name its scope. Perfect observation of every offline PWA is neither necessary nor generally possible. The stronger useful claim is about **authoritative execution paths**.

A generic retirement proof can establish that, for a declared capability/environment:
1. current authoritative evaluators reject new G1 authorization;
2. current authority floor/revocation state cannot be lowered by ordinary restore/replica convergence;
3. all server-recognized G1 leases in the declared authoritative stores are completed, expired, revoked, or non-executable;
4. replica/provider reconciliation has no unresolved authoritative divergence for that scope;
5. recovery/bootstrap does not reactivate G1;
6. historical parsers/verifiers cannot execute G1 authority;
7. stale/offline clients must re-enter through current server authority before remote mutation.

This does **not** prove every physical device has deleted G1 bytes. It proves retained bytes cannot obtain G1 remote authority through the declared current execution path.

Useful assurance states:
- `RETIREMENT-PROVEN-FOR-DECLARED-AUTHORITY-SCOPE`;
- `RETIREMENT-PROVEN-WITH-BOUNDED-EXCEPTION`;
- `RETIREMENT-REVALIDATION-REQUIRED`;
- `RETIREMENT-BLOCKED-BY-DIVERGENCE`;
- `RETIREMENT-UNKNOWN`.

## Replica and backup reconciliation

### Stale replica
A replica below the retirement floor may serve historical/read-only data only if architecture explicitly permits it. It must not independently authorize G1 mutation. Rejoining it requires reconciliation against current authority state before authority-bearing service.

### Backup restore
A backup is evidence/data, not an authorization time machine. Restore procedure must separate:
- business/local data restoration;
- policy/authority state restoration;
- current retirement/revocation floor;
- current secrets/keys/trust roots;
- lease consumption/completion state.

If a full-state backup predates G1 retirement, blindly replacing current authorization state can resurrect G1. Recovery must reapply or independently recover the current security floor before consequence-bearing traffic resumes.

### Compaction
Compaction may legitimately remove old payload/history. It must not remove the **only surviving information required to prevent predecessor resurrection** unless equivalent stronger current state supersedes it. This is a retention-design issue, not an argument for retaining every event forever.

## PWA / Service Worker / EFB application

A long-offline company iPad may still hold:
- old document/app bytes;
- old Service Worker/cache;
- local IndexedDB records and queued operations;
- old account/session artifacts;
- old policy/generation labels.

None of these prove current G1 server authority. On reconnect:
1. preserve irreplaceable local data and provenance before destructive migration;
2. establish current server authority/retirement floor through authenticated current channels;
3. reconcile queued operation identities and any claimed leases;
4. treat below-floor predecessor authority as non-executable even if cached UI says otherwise;
5. distinguish already-committed remote operations from genuinely pending local intent;
6. migrate/revalidate forward where supported;
7. otherwise expose `LOCAL DATA PRESERVED / REMOTE AUTHORITY RETIRED / RECOVERY REQUIRED` rather than deleting data or restoring G1.

A Service Worker update, cache deletion, reinstall, or Home Screen removal may change local runtime state but is not the authoritative retirement proof. Conversely, an old SW remaining on disk does not mean G1 remains remotely executable.

Actual Safari/WebKit/MDM storage/update behavior on company iPad remains OPEN.

## Cross-track integration

### Track A — Platform & Browser
Own exact SW/cache/IndexedDB lifecycle and browser storage facts. Transfer: local stale bytes and server authority are separate; browser deletion is not the canonical retirement mechanism.

### Track B — UX / IA / Content
Own truthful recovery states: local data preserved, authorization retired, sync blocked, revalidation/manual recovery required. Do not imply `update app` alone restores authority.

### Track C — Performance / Accessibility / Quality
Own restore/replica/orphan fault injection and accessible degraded/recovery UX. Verify that destructive cleanup is not required to reach a safe state.

### Track D — Search / Discovery / Analytics
May aggregate privacy-minimized generation/orphan/restore diagnostics. Absence of G1 telemetry cannot prove fleet-zero and analytics cannot be the retirement oracle.

### Track E — Owner
Own retirement floor, finalization, authoritative reconciliation, orphan policy, backup anti-resurrection and evidence sufficient for retirement claims.

## MINTTAP DECISION — minimal sufficient generic model

If this class of system is implemented:
1. represent retirement/revocation as durable negative authority state, not only deletion of positive G1 records;
2. make the security retirement floor monotonic under ordinary replica/backup convergence;
3. do not allow stale backup/replica/client timestamps to lower accepted policy/trust generation;
4. bind leases to transaction/payload/principal-device/trust/policy/expiry/revocation/completion state and reconcile all of those before execution;
5. classify unresolved lease inconsistency as non-permit for consequence-bearing mutation;
6. separate retirement proof of authoritative execution paths from impossible claims that every offline client erased old bytes;
7. keep historical verification/parsing separate from execution authority;
8. ensure compaction does not erase the only anti-resurrection state;
9. preserve local EFB data while requiring current authority for remote mutation;
10. require product/provider/managed-device evidence before choosing physical schema, retention, quorum or timing values.

## VALIDATION — 44-case destructive campaign

1. normal G1→G2 retirement; 2. new G1 authorization rejected after floor; 3. bounded G1 lease drains before finalization; 4. expired lease cannot delay retirement; 5. revoked lease cannot delay/restore G1; 6. lease exists without transaction; 7. transaction completed but lease executable flag stale; 8. transaction absent after partial restore; 9. duplicate lease IDs same payload; 10. duplicate lease IDs conflicting payload; 11. lease references old trust epoch; 12. lease references deleted principal/device; 13. replica misses retirement event; 14. replica rejoins below floor; 15. replica divergence alarm/reconciliation; 16. stale read replica cannot authorize; 17. backup before retirement restored; 18. backup after retirement restored; 19. mixed backup where business data newer but security state older; 20. restore loses lease-consumption marker; 21. restore loses retirement marker but external/current floor survives; 22. all local retirement records lost and authority floor cannot be established → UNKNOWN/no permit; 23. compaction removes historical G1 payload but keeps sufficient anti-resurrection state; 24. unsafe compaction proposal detected; 25. historical verifier parses G1 without execution; 26. recovery/bootstrap cannot lower floor; 27. rollback deployment cannot lower floor; 28. operator attempts manual G1 re-enable without authorized transition; 29. forged retirement marker; 30. forged unretire marker; 31. delayed provider replication; 32. split-brain retirement observations; 33. current server rejects stale client-carried G1 lease; 34. old SW + old cache + valid local data reconnect; 35. old SW + forged client clock; 36. old IndexedDB queue includes already-committed operation; 37. queue includes denied predecessor operation; 38. local export remains possible where product policy permits; 39. accessible UX explains preservation vs authority retirement; 40. analytics reports zero G1 but offline device later returns safely; 41. manual recovery imports old data without old authority; 42. physical managed-iPad behavior remains OPEN; 43. backup restore + stale replica + orphaned lease combined; 44. adversarial restore cannot convert historical G1 bytes into current remote mutation authority.

## CONTRADICTION / failure-mode analysis

### Delete-row theater
Deleting `policy=G1` or lease rows can destroy evidence while leaving another replica/backup capable of restoring them.

### Tombstone theater
A tombstone is useful only if its semantics, authenticity, retention and merge precedence are defined. A boolean `retired=true` in the same rollback-prone snapshot is not automatically anti-resurrection.

### Fleet-zero theater
No observed G1 device/telemetry is not proof every offline client is gone. Retirement should be proven at authoritative execution paths instead.

### Backup-success theater
A successful restore that silently restores old authorization is a security failure even if availability metrics are green.

### Garbage-collection theater
Compaction reduces storage; it does not decide which minimal security facts remain necessary to prevent rollback/resurrection.

## OPEN

Actual MintTap/LogMate policy store, database/replication model, provider consistency, lease schema/indexes, backup format, restore sequence, trust/authority epoch store, compaction/retention, Service Worker strategy, local schema/provenance, recovery/import path, account/device identity, managed-iPad behavior, aviation/legal retention and consequence classes remain unknown. No product quorum, retention duration, database primitive or provider guarantee is asserted.

## CHANGE WATCH

- Authorization/session invalidation guidance and selected provider consistency/restore semantics.
- Browser/WebKit storage, SW and Home Screen behavior for EFB claims.
- Database/provider backup, PITR, replica and compaction behavior selected by implementation.
- Any change to policy/trust generation, lease topology, restore tooling or recovery authority requires refreshing anti-resurrection fixtures.

## Gate result

**PASS (generic).** The Web Manager can now distinguish deletion from durable retirement, define a monotonic authority floor, detect orphaned/ambiguous predecessor leases, reconcile stale replicas/backups without resurrecting retired authority, and state a retirement proof at the authoritative execution-path scope without claiming impossible observation of every offline client.

Product/provider/managed-iPad/replica/backup runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA retirement-state disaster recovery, authority-floor escrow & catastrophic control-plane loss.** Anti-resurrection now depends on a trustworthy current retirement floor. The next risk is catastrophic loss of the primary policy/authority store itself: determine how the minimum accepted authority epoch/revocation state can be independently recovered without turning the escrow/recovery copy into a second live authorization oracle, and how to distinguish a legitimately old recovery package from a rollback attack.