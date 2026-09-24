# 270 — PWA Revocation-Distribution Authenticity, Invalidation-Channel Partition & Anti-Rollback Recovery

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime transport and persistence boundaries; Track B truthful partition/degraded-state UX; Track C destructive validation; Track D bounded lag/coverage diagnostics.  
Dependencies: 260–269 dependency/completeness/topology/re-entry/composite-revocation governance.

## Problem

269 established that cached `NORMAL` decisions remain dependent on current prerequisites and revocation state. The next failure boundary is the revocation distribution mechanism itself. A client, server, worker, replica or operator can receive a forged, replayed, stale, partial or partitioned invalidation view; a channel can be unavailable; and recovery can restore an older status snapshot. Treating any delivered revocation payload as current, or treating channel silence as proof of no revocation, recreates stale authority.

Central rule: **revocation distribution is evidence transport, not self-authenticating truth. Material authorization decisions need authenticated source/scope, freshness/currentness semantics, anti-rollback state and consequence-aware behavior when current revocation status cannot be established. Recovery must converge forward from a trusted current reference or governed rebootstrap; stale replicas, backups and long-offline clients cannot vote authority backward. Unique data remains distinct from execution authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns exact HTTPS/secure-context, Service Worker update/control, Cache Storage and browser persistence mechanics. Browser transport/runtime currentness is not semantic revocation authority.
- **B UX/IA/Content:** high dependency pressure. Must represent `status current`, `currentness unavailable`, `limited/recovery-only`, `revalidation required`, and preserved offline data without falsely claiming global outage or data loss. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** destructive campaign expands **912 → 920 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures distribution lag, channel partition, contradictory views, stale generations and unknown tails; telemetry cannot authenticate or authorize revocation state.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns revocation-source authenticity, currentness contracts, partition policy, anti-rollback recovery and successor requalification.

## SOURCE

### RFC 6960 — signed status, authorized responder and explicit freshness semantics

RFC 6960 defines signed OCSP responses, requires relying parties to establish that the responder is authorized, and distinguishes `thisUpdate`, `nextUpdate`, `producedAt` and `revocationTime`. It says responses whose `nextUpdate` is earlier than local time, or whose `thisUpdate` is later than local time, should be considered unreliable. It also provides `tryLater`, `unauthorized` and `unknown` outcomes rather than treating inability to provide authoritative status as `good`.

Source: https://www.rfc-editor.org/rfc/rfc6960

**TRANSFER VALIDATION:** OCSP is a PKIX protocol, not a MintTap/PWA revocation protocol. Its useful bounded precedent is that status authenticity, responder authority, scope and freshness are separate checks; channel success alone is insufficient.

### RFC 5280 — revocation distribution can lag; monotonic CRL numbers identify supersession

RFC 5280 notes that CRL distribution can delay revocation visibility until relying systems obtain updated information. It defines CRL Number as a monotonically increasing sequence for a given issuer/scope so consumers can determine when one CRL supersedes another; delta CRLs bind to a base CRL and scope. Currentness also depends on `thisUpdate`/`nextUpdate` and applicable scope.

Source: https://www.rfc-editor.org/rfc/rfc5280

**TRANSFER VALIDATION:** CRL numbering is bounded precedent for anti-rollback/currentness reasoning. It does not mandate a numeric counter or PKI-shaped implementation for PWA authorization.

### RFC 10007 — even revocation artifacts need correct signer authorization checks

RFC 10007 (2026) updates RFC 5280 CRL validation to require checking the CRL issuer certificate's `keyUsage` authorization for CRL signing. This reinforces that a cryptographically signed revocation object is not sufficient unless the signer is authorized for that revocation function.

Source: https://www.rfc-editor.org/rfc/rfc10007

**TRANSFER VALIDATION:** use only as a current PKIX precedent for signer-role authorization. It does not define product revocation roles.

### Service Worker update/cache are secure-context runtime mechanisms

Service Worker registration/update and Cache Storage are secure-context browser mechanisms. `ServiceWorkerRegistration.update()` checks for a changed worker script; Cache Storage can persist request/response objects and application code is responsible for cache update policy. These mechanisms can carry or retain stale application state but do not authenticate organizational revocation state.

Sources:  
https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update  
https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache  
https://developer.mozilla.org/en-US/docs/Web/API/Cache

**TRANSFER VALIDATION:** browser secure transport and worker freshness are necessary runtime evidence where applicable, not proof that semantic revocation state is authentic/current.

## SYNTHESIS 1 — distribution transport and revocation truth are separate

A successful HTTPS request, push delivery, websocket message, MDM signal or sync response proves only bounded transport facts. A material revocation view still needs enough evidence to establish:
- authoritative issuer/source;
- source authorization for the claimed scope;
- integrity/authenticity;
- subject/consequence/scope binding;
- freshness/currentness interval or generation;
- supersession/rollback relation;
- applicable policy/verifier context.

Guards:
- `message delivered ≠ revocation authentic`;
- `signature valid ≠ signer authorized for this scope`;
- `HTTPS valid ≠ payload semantically current`;
- `channel healthy ≠ revocation view complete`.

## SYNTHESIS 2 — distinguish forged, replayed, delayed and merely old-but-historical evidence

These are different states. A forged object fails authenticity. A replayed object may be authentic historical evidence but inapplicable now. A delayed object may be current for its source epoch but arrive too late for a high-consequence operation. Do not erase authentic historical evidence merely because it is stale.

Guards:
- `authentic old status ≠ current status`;
- `stale now ≠ historically false`;
- `arrived later ≠ supersedes newer state`.

## SYNTHESIS 3 — currentness requires scope-aware monotonic or anti-rollback relation

A useful generic contract binds revocation state to an authority/scope plus a monotonic or otherwise anti-rollback generation/checkpoint. A lower generation cannot silently replace a higher accepted generation merely because it was restored later or came from another replica.

Exact representation is implementation-specific: counter, signed checkpoint, epoch tuple or another construction may be appropriate.

Guards:
- `newly received ≠ newer`;
- `restore completed ≠ generation current`;
- `replica online ≠ replica authoritative-current`.

## SYNTHESIS 4 — wall-clock freshness alone is insufficient

Timestamps help, but clock skew, offline duration, replay and restored snapshots can defeat timestamp-only reasoning. Currentness should combine authenticated source/scope with relevant validity interval/generation and policy context.

Guards:
- `recent timestamp ≠ current authority`;
- `device clock newer ≠ revocation state newer`;
- `TTL unexpired ≠ no superseding revocation exists`.

## SYNTHESIS 5 — partition is UNKNOWN currentness, not implicit GOOD

If a material revocation channel is unavailable and no still-applicable authenticated currentness evidence exists, the system does not know that nothing was revoked. For affected high-consequence operations, transition to a product-defined degraded/revalidation state rather than silently reusing old `NORMAL`.

This does **not** imply global fail-closed destruction. Lower-consequence local preservation/read/recovery capability can remain available when its prerequisite graph is unaffected.

Guards:
- `channel silent ≠ no revocation`;
- `cannot refresh status ≠ status good`;
- `currentness UNKNOWN ≠ data disposable`;
- `high-consequence blocked ≠ all local capability blocked`.

## SYNTHESIS 6 — fail-open/fail-closed is consequence-specific

A single global network-partition rule is too coarse. Product policy should classify consequences: preservation/read, local capture, recovery export, queued mutation, remote sync, publication/finalization, administrative/recovery authority. The acceptable stale-status window and behavior can differ by consequence and domain obligation.

**OPEN:** actual MintTap/LogMate consequence classification and legal/aviation requirements are unverified.

Guard: `one revocation channel policy ≠ one consequence policy`.

## SYNTHESIS 7 — multiple channels do not automatically provide independent currentness

Push, API polling and dashboard views may all originate from the same registry, signing key, replica or deployment pipeline. Channel diversity can improve availability but not necessarily independence or authenticity.

Guards:
- `three delivery channels ≠ three independent revocation authorities`;
- `different transport ≠ different failure domain`.

## SYNTHESIS 8 — contradictory authenticated views require quarantine/reconciliation, not majority vote

If two apparently authentic sources for the same scope present incompatible current generations, preserve both views and provenance, identify authority/scope/dependency, and prevent affected high-consequence reuse until a current successor is established. A 2-of-3 transport majority is not automatically semantic truth when all three may share a stale root or one legitimate authority has advanced.

Guard: `majority view ≠ authoritative-current view`.

## SYNTHESIS 9 — recovered channels rejoin through forward reconciliation

After a partition, do not copy whichever replica reconnects first over the rest. Rejoin should compare authenticated authority/scope/generation/checkpoint and actual dependency history. A stale replica can receive current state; it must not roll the current authority backward.

Generic pattern:
1. preserve both histories/checkpoints;
2. establish trusted current authority/scope;
3. compare generations/lineage;
4. quarantine contradictions/forks;
5. advance stale replicas to a current successor state;
6. invalidate derived stale decisions;
7. prove authoritative rejection of obsolete generations;
8. resume consequences only after required currentness is established.

## SYNTHESIS 10 — backup/PITR recovery needs an anti-rollback reference outside the restored failure domain

If both application state and revocation generation are restored from the same old backup, internal consistency does not prove currentness. Recovery needs a current reference not rolled back with that snapshot, or a governed rebootstrap when such a reference is unavailable.

Guards:
- `backup internally consistent ≠ authorization current`;
- `revocation DB restored ≠ revocation history complete`;
- `same backup contains decision + generation ≠ anti-rollback`.

## SYNTHESIS 11 — revocation-source compromise requires successor authority, not self-healing by the compromised source

If the revocation signer/registry/verifier itself is suspected compromised, its later `all clear` cannot alone restore trust. Preserve historical evidence, scope affected claims, establish successor authority through a path not solely controlled by the compromised root, then issue successor currentness evidence.

Guards:
- `source says recovered ≠ source trust recovered`;
- `new status signed by compromised root ≠ successor trust established`.

## SYNTHESIS 12 — Service Worker update does not repair a partitioned semantic authority channel

A current worker can fetch or display stale revocation data. Conversely, a stale worker may be prevented from executing a high-consequence operation by a current authoritative server fence. Browser runtime version and semantic revocation currentness are orthogonal inputs.

Guards:
- `worker current ≠ revocation current`;
- `worker stale ≠ stale authority accepted by server`;
- `Cache Storage cleared ≠ revocation partition healed`.

## SYNTHESIS 13 — long-offline clients require currentness requalification on return

A company iPad may hold authentic G17 status and unique records while central authority has advanced to G23. Preserve records and historical status, block inherited high-consequence `NORMAL`, obtain/authenticate current state, reconcile queued operations individually, and create successor decision evidence.

Guards:
- `offline-held authentic status ≠ reconnect authority`;
- `data worth preserving ≠ queued effect worth replaying`.

## SYNTHESIS 14 — revocation distribution observability is not revocation authority

Useful diagnostics include last authenticated generation by scope, distribution lag, contradictory-view count, partition duration, online cohort coverage, late-client sightings and obsolete-generation rejection counts. These metrics expose uncertainty; they do not convert UNKNOWN into GOOD.

Guard: `telemetry says 100% delivered ≠ stale authority impossible`.

## SYNTHESIS 15 — currentness proof must survive manual/admin/export/import paths

A support console or exported status bundle can reintroduce an old authenticated generation. Manual/import admission needs the same source/scope/supersession checks as automated paths.

Guard: `human imported authentic bundle ≠ bundle current`.

## SYNTHESIS 16 — generic partition/recovery contract

For a material revocation distribution failure:
1. preserve current and conflicting evidence/provenance;
2. classify affected consequence and source/scope;
3. determine last authenticated currentness evidence and its applicability;
4. if currentness cannot be established, fence affected high-consequence reuse while preserving unique data/unaffected capabilities;
5. do not treat transport silence, push failure or missing telemetry as GOOD;
6. authenticate recovered source and establish anti-rollback generation/lineage;
7. reconcile replicas/clients forward, not by arrival order or wall-clock alone;
8. invalidate derived decisions that depended on superseded state;
9. reject obsolete generations at authoritative execution boundaries;
10. requalify late/offline clients and queued operations under current policy;
11. retain historical revocation evidence and recovery provenance;
12. record unresolved offline/unknown tail and contradiction debt.

This is a reasoning contract, not a mandated implementation architecture.

## Track C destructive campaign additions — 912 → 920

1. **forged-revocation delivery:** syntactically valid payload from unauthorized signer is accepted. Expected: signer/scope authorization failure prevents semantic use.
2. **authentic-replay rollback:** old signed G17 arrives after G23 and replaces current state. Expected: anti-rollback relation rejects currentness downgrade while retaining history.
3. **partition-means-good:** revocation endpoint unavailable and cached NORMAL continues indefinitely for publication. Expected: consequence-aware UNKNOWN/degraded behavior.
4. **wall-clock-only freshness:** later device timestamp wins over higher authenticated generation. Expected: clock cannot override authority/lineage.
5. **multi-channel independence theater:** push/API/dashboard all green from one stale registry. Expected: shared failure domain remains one evidence root.
6. **PITR revocation rollback:** app and revocation DB restore together to G19 after authority reached G24. Expected: external/current reference or governed rebootstrap blocks rollback.
7. **worker-update partition theater:** new Service Worker activates but revocation source remains partitioned; UI returns NORMAL. Expected: runtime update cannot establish semantic currentness.
8. **late-iPad stale-status replay:** long-offline iPad reconnects with authentic old status and auto-replays high-consequence queue. Expected: preserve data, obtain current state, reconcile operation-by-operation.

These are defined cases, not executed product evidence.

## EFB / LogMate-like application case

Scenario: a company iPad leaves connectivity while holding authenticated revocation generation G17 and unique flight/logbook records. Central authority later reaches G23 after a credential/verifier revocation. During return, the iPad can reach application hosting but the revocation/currentness channel is partitioned; its Service Worker is current and local UI is functional.

Generic safe handling:
1. preserve unique records, queue payloads and historical G17 evidence;
2. do not infer current authority from worker/network health;
3. mark affected high-consequence currentness UNKNOWN when G17 is no longer sufficient under policy;
4. retain allowed preservation/read/recovery capability according to consequence policy;
5. fence auto-replay/publication requiring current revocation state;
6. when the channel recovers, authenticate source/scope and obtain a state that cannot be rolled back below already-established central currentness;
7. reconcile each queued operation against current policy/authority/schema;
8. reject obsolete generation at the authoritative boundary;
9. create successor composite evidence only from compatible current prerequisites;
10. retain unresolved fleet-tail obligations.

**OPEN:** actual LogMate auth/session/backend/MDM/WebKit/queue/data model, direct sync architecture and aviation/legal consequence policy remain unverified.

## Cross-track transfer

### Track A
Own exact HTTPS/secure-context, Service Worker update/control, Cache Storage and browser persistence behavior. Transfer rule: transport/runtime integrity is input evidence only; it cannot establish semantic revocation currentness.

### Track B
Define understandable degraded/revalidation states without falsely claiming data loss or a universal outage. Exact wording, focus behavior, offline recovery flow and AT/human validation remain Design Studio/runtime work.

### Track C
Execute forged/replayed/partitioned/recovery/late-client cases against actual implementation, including server, browser, background job and manual/import paths.

### Track D
Measure distribution lag, contradictory views, last-seen generations, partition duration and unknown tail. Absence of stale sightings is not proof of convergence.

### Track E
Own revocation source/scope authenticity, consequence-aware partition policy, anti-rollback state, replica recovery, authoritative obsolete-generation rejection and successor trust.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate-like PWA work unless stronger product evidence supersedes this generic rule:
- treat revocation distribution as authenticated, scope-bound, freshness/anti-rollback evidence rather than a boolean push event;
- never infer `GOOD` solely from channel silence or delivery success;
- use consequence-aware degraded behavior when currentness cannot be established;
- preserve unique local data independently from high-consequence execution authority;
- prevent lower/older authenticated generations from replacing already-established newer state;
- require forward reconciliation after replica/channel/backup recovery;
- make authoritative execution boundaries reject obsolete generations for material offline-return operations;
- do not use Service Worker/cache/network currentness as semantic revocation proof;
- require successor trust establishment when the revocation source itself is compromised.

## OPEN / VALIDATION

Production validation remains OPEN for:
- actual revocation/status source and signer/authorization model;
- actual generation/checkpoint/epoch representation;
- partition tolerance and consequence-specific stale windows;
- auth/session/token behavior;
- server/gateway/job/manual/import cache and replica topology;
- backup/PITR/reimport anti-rollback reference;
- Service Worker/cache/IndexedDB/queue behavior on target browsers and installed PWA;
- physical iOS/iPadOS/managed-device behavior;
- MDM/ADE/fleet inventory/currentness channels;
- product/domain/aviation/legal authority and degraded-mode policy.

## CHANGE WATCH

- Browser/WebKit Service Worker/storage behavior and installed-PWA lifecycle remain platform/version sensitive.
- PKIX RFCs are bounded security precedents, not a product architecture prescription.
- Authentication/session/provider revocation behavior is provider- and deployment-specific.
- Apple managed-device/PWA behavior remains OS/enrollment/version specific.

## Gate

**270 PASS (generic).** We can distinguish authentic/current revocation evidence from transport success, reason about partition without treating silence as GOOD, prevent rollback during replica/backup/late-client recovery, and preserve unique offline data while fencing stale high-consequence authority.

**Production PASS is not claimed.** Product/runtime/managed-iPad/domain validation remains OPEN.

## Next highest-value target

**271 — revocation-source key/authority rotation, dual-control transition & partition-safe successor adoption:** determine how a system moves from revocation authority R1 to R2 without letting compromised R1 self-authorize its successor, without letting partitioned clients permanently reject legitimate R2, and without accepting ambiguous dual-authority status during long-offline migration.