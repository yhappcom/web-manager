# 152 — PWA Policy-Generation Retirement, In-Flight Lease Bounding & Compatibility-Horizon Governance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + TRANSACTION/POLICY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 149 policy composition/deadlock; 150 rollout/shadow/diff; 151 cohort/transaction/split-policy convergence; Track A SW/runtime lifecycle; Track B expiry/recovery UX; Track C lease/retirement fault injection; Track D aggregate retirement diagnostics only.

## Why this study exists

151 prevents cross-generation cherry-picking during partial rollout. The remaining authority problem is temporal: once G2 is authoritative, when may G1 stop authorizing new work, how long may already-started G1 work finish, what events must kill that allowance immediately, and what happens to a PWA that returns after the compatibility horizon has ended?

A predecessor policy that never retires becomes a downgrade surface. A predecessor that disappears without bounded transition semantics can strand legitimate in-flight work or force destructive handling of offline local data. The objective is therefore **bounded authority retirement without data destruction**.

## SOURCE

### Current NIST session guidance separates continuing state from indefinite authority
NIST SP 800-63B-4 (current revision, published 2025) requires periodic reauthentication and defines definite overall/inactivity timeouts by assurance level. It also distinguishes authentication/session continuity from access tokens that may outlive the subscriber's authenticated session. Transfer lesson: possession of previously valid continuity material is not indefinite proof of present authority.

Source: https://pages.nist.gov/800-63-4/sp800-63b.html

### OWASP requires server-side timeout enforcement
OWASP Session Management guidance requires server-side invalidation on session expiry; the testing guide warns against client-controlled timeout enforcement. This is directly transferable to policy-generation leases: client clocks, cached flags or stale workers must not extend server authority.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/07-Testing_Session_Timeout

### Service Worker activation can change client control independently of server policy retirement
`skipWaiting()` can force a waiting worker active; `clients.claim()` can immediately control in-scope clients. These are browser runtime transitions, not server authorization retirement semantics.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting
- https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim

### iOS/iPadOS Home Screen web apps are real WebKit application contexts, but product guarantees remain separate
WebKit documents Home Screen web apps and Service Worker-backed offline capability. This establishes platform capability, not MintTap/LogMate storage durability, lease, background execution or managed-EFB guarantees.

Sources:
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- https://webkit.org/blog/16993/news-from-wwdc25-web-technology-coming-this-fall-in-safari-26-beta/

## SYNTHESIS — retirement is a lifecycle, not a delete

Separate at least these states:

1. **CURRENT** — generation may authorize new and existing work for its declared scope.
2. **SUCCESSOR-AUTHORITATIVE / PREDECESSOR-DRAINING** — predecessor may not start arbitrary new authority-bearing work; explicitly admitted in-flight work may continue under a bounded lease.
3. **COMPATIBILITY-ONLY** — predecessor representations/protocols may still be parsed or migrated, but predecessor policy no longer grants remote authority.
4. **RETIRED** — predecessor cannot authorize new or in-flight remote mutation.
5. **REVOKED** — emergency/security retirement invalidates otherwise-live leases according to consequence policy.
6. **HISTORICAL-VERIFICATION-ONLY** — old generation metadata/evidence can remain interpretable without being executable authority.

Persistent guards:
- `generation supported ≠ generation authoritative`;
- `generation parseable ≠ generation executable`;
- `transaction started under G1 ≠ G1 may authorize forever`;
- `lease unexpired ≠ revocation cannot override it`;
- `client clock before expiry ≠ server lease valid`;
- `compatibility horizon ≠ authority horizon`;
- `local data older than horizon ≠ local data should be deleted`;
- `old Service Worker active ≠ old policy active`;
- `offline duration long ≠ grandfathered remote authority`;
- `retired policy metadata retained ≠ retired policy reactivated`.

## In-flight lease model

A policy-generation lease is a **server-recognized bounded exception for an already-admitted logical transaction**, not a general extension of G1.

A useful generic lease binds:
- transaction/operation identity;
- principal/account and, where relevant, device/trust context;
- accepted predecessor generation and evaluator lineage;
- significant transaction data/fingerprint;
- operation class/capability;
- admission time and authoritative expiry/maximum lifetime;
- current revocation/trust epoch;
- consumed/completed/aborted state;
- any successor-generation compatibility condition.

Lease time is enforced by authoritative server/provider state, not client time. Retries preserve the same lease/operation identity; they do not mint a fresh lease or reset expiry.

A lease may permit completion of an already-authorized operation while forbidding new G1 operations. Therefore `G1 lease exists ≠ G1 remains generally authoritative`.

## Retirement criteria

Do not choose one universal number. A predecessor can move from DRAINING to RETIRED when the declared retirement conditions are satisfied, which may include:
- no admissible new transactions under G1;
- bounded in-flight leases have completed, expired or been explicitly aborted;
- successor recovery/bootstrap path is independently usable;
- provider/evaluator convergence is sufficient for the affected consequence class;
- compatibility handling for retained local data does not require restoring G1 authority;
- rollback policy does not resurrect a security-retired trust epoch;
- required evidence/audit/provenance remains interpretable after execution authority ends.

Calendar duration is one input, not the definition of safety. Product-specific values remain OPEN.

## Emergency revocation

Security compromise, stolen authority, trust-root retirement or a discovered policy flaw can require immediate predecessor invalidation. Emergency revocation therefore has precedence over ordinary drain leases when the consequence model says continued execution is unsafe.

The result may be operationally unpleasant but must be explicit:
- preserve user-entered/local irreplaceable data;
- abort or gate remote consequence-bearing execution;
- record why the lease became invalid;
- require current-generation revalidation/restart or manual recovery;
- never silently reinterpret the old authorization as a new one.

`availability loss caused by revocation ≠ justification to restore compromised authority`.

## Compatibility horizon governance

Separate three horizons:

1. **AUTHORITY HORIZON** — last point at which a generation can authorize remote consequence-bearing work.
2. **AUTOMATED COMPATIBILITY HORIZON** — last point at which supported software can automatically migrate/revalidate old local state.
3. **DATA RECOVERY/EXPORT HORIZON** — how long retained local data can still be read/exported/recovered, subject to actual format and storage durability.

These horizons need not be equal. In particular, data recovery may outlive remote authority. This is the central EFB/PWA safety property: **expiry of server compatibility must not be modeled as permission to erase local flight data**.

Past the automated compatibility horizon, a long-offline device may enter `LOCAL-DATA-PRESERVED / REMOTE-AUTHORITY-EXPIRED / MANUAL-RECOVERY-REQUIRED`. Whether manual recovery exists and what it can authorize is product-specific and remains OPEN.

## PWA / Service Worker / managed-iPad application

For a long-offline iPad, keep separate:
- app/document generation;
- controlling Service Worker generation;
- local schema/data/provenance generation;
- server API compatibility generation;
- policy generation;
- transaction lease generation/expiry;
- account/device trust epoch.

On reconnect after G1 retirement:
1. preserve local data before destructive migration;
2. discover current server authority/compatibility without trusting client-reported generation or clock;
3. reconcile operation identities to avoid duplicate execution;
4. reject expired/revoked G1 remote authority even if the old SW remains active;
5. if an admitted unexpired lease is still valid and not revoked, finish only the bounded operation it names;
6. otherwise revalidate forward, migrate, restart authorization, or enter manual recovery;
7. never reinstall/re-enable G1 server policy merely because the device was offline.

Service Worker `skipWaiting()`/`clients.claim()` may alter which worker controls a page, but cannot mint/extend a server transaction lease or reverse policy retirement.

Actual WebKit/MDM/background/storage persistence behavior on company iPad remains OPEN pending physical/project evidence.

## Cross-track transfer

### Track A — Platform & Browser
Own exact SW/document/cache/storage generation and activation/control facts. Validate that runtime transitions cannot be confused with server lease extension.

### Track B — UX / IA / Content
Own truthful states such as `local data preserved`, `sync authorization expired`, `revalidation required`, `transaction expired`, `update required`, and `manual recovery required`. Avoid destructive or misleading wording.

### Track C — Performance / Accessibility / Quality
Own time-boundary, clock-skew, delayed retry, revocation-race, stale-SW, long-offline and accessible recovery testing.

### Track D — Search / Discovery / Analytics
May measure privacy-minimized generation/lease retirement diagnostics. Telemetry absence cannot prove all G1 leases/fleet members are gone and analytics cannot extend authority.

### Track E — Owner
Own authority horizon, lease admission/expiry/revocation, predecessor retirement, compatibility governance and recovery boundary.

## MINTTAP DECISION — minimal sufficient model

If implemented for MintTap/LogMate-like systems:
1. distinguish generation support, parsing, automated migration and authorization;
2. stop G1 from admitting new authority-bearing work before or at successor cutover according to declared rollout policy;
3. represent any surviving G1 transaction as a server-bound lease with operation identity, payload fingerprint, scope, expiry and revocation epoch;
4. do not renew a lease merely because a retry arrives;
5. let emergency security revocation override ordinary lease completion where consequence requires it;
6. retire execution authority without deleting historical evidence needed to explain prior decisions;
7. separate authority, automated compatibility and data-recovery horizons;
8. after compatibility expiry, preserve local irreplaceable data while gating remote mutation;
9. never let client clock, SW version or offline duration select/extend legacy authority;
10. require real product/provider/device evidence before setting actual durations or claiming managed-iPad behavior.

## VALIDATION — 40-case campaign

1. G1 new work allowed before retirement; 2. new G1 work denied once draining starts; 3. admitted G1 transaction completes within lease; 4. lease expiry before final effect; 5. retry does not renew lease; 6. same lease/different payload rejected; 7. completed operation retry returns durable result; 8. duplicate final execution rejected; 9. client clock rollback cannot extend lease; 10. client clock jump cannot force server expiry; 11. server/provider clock-boundary behavior; 12. emergency revocation kills unsafe live lease; 13. low-consequence lease allowed to drain when policy explicitly permits; 14. revoked trust epoch invalidates predecessor lease; 15. policy rollback cannot resurrect retired G1; 16. stale backup cannot restore lease authority; 17. historical G1 evidence remains readable after retirement; 18. compatibility parser accepts G1 data without granting G1 authority; 19. automatic migration succeeds after authority retirement; 20. automatic migration failure preserves source data; 21. device reconnects just before compatibility horizon; 22. reconnects just after horizon; 23. long-offline queue contains already-committed operation; 24. long-offline queue contains now-denied operation; 25. mixed G1/G2 local records preserve provenance; 26. stale SW controls current page but cannot extend G1 lease; 27. current SW with stale document cannot extend G1; 28. `skipWaiting` transition during lease; 29. `clients.claim` transition during lease; 30. account has two devices, only one has valid bounded lease; 31. forged lease identifier; 32. stolen but revoked lease; 33. provider evaluator lag during retirement; 34. recovery/bootstrap remains available after G1 retirement; 35. recovery path does not reactivate G1; 36. local read/export remains available where product policy permits; 37. accessible UX distinguishes local preservation from remote expiry; 38. analytics missing G1 traffic does not prove retirement complete; 39. physical managed-iPad case remains OPEN rather than inferred; 40. adversarial stale-SW + forged clock + retry + revoked G1 lease produces no privilege expansion or data deletion.

## CONTRADICTION / failure-mode analysis

### Grace-period theater
A fixed grace period is not sufficient if it can be reset by retry, ignores revocation or admits new G1 work.

### Compatibility theater
Keeping a decoder/migrator for G1 does not require keeping G1 authorization active.

### Fleet-zero theater
No observed G1 telemetry does not prove every offline client or lease is gone.

### Update theater
A current Service Worker does not prove policy/trust/transaction convergence; an old worker does not entitle the client to old authority.

### Safety-through-deletion theater
Deleting old local data avoids compatibility work but is not a valid substitute for authority governance where the data may be irreplaceable.

## OPEN

Actual MintTap/LogMate operation classes, consequence model, transaction boundaries, lease store, provider consistency, clock authority, policy engine, account/device identity, SW strategy, schema/API support window, compatibility horizon, local-data criticality, managed-iPad storage behavior, recovery/export implementation and legal/aviation retention requirements remain unknown. No production duration or guarantee is asserted.

## CHANGE WATCH

- NIST SP 800-63B-4 is the current revision; do not reuse superseded 63-3 timeout values as current requirements.
- Browser/WebKit SW lifecycle and Home Screen behavior require current platform evidence and physical validation for EFB claims.
- Authorization-provider consistency/lease semantics must be verified against the selected provider.
- Any change to operation topology, trust epochs, migration format or recovery policy requires refreshing retirement fixtures.

## Gate result

**PASS (generic).** The Web Manager can now distinguish predecessor drain from indefinite legacy authority, bound in-flight authorization as revocable server-side leases, separate authority/compatibility/data-recovery horizons, and expire long-offline PWA support without converting expiry into local-data deletion or downgrade authority.

Product/provider/managed-iPad/transaction-policy runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA policy-retirement proof, orphaned-lease detection & tombstone/anti-resurrection governance.** After defining bounded retirement, the next risk is proving that predecessor authority is actually gone: stale replicas, restored backups, orphaned leases or deleted retirement markers can resurrect G1. The next study should define durable retirement/tombstone state, reconciliation across replicas/backups, orphan detection and evidence sufficient to claim authority retirement without requiring impossible fleet-perfect observation.