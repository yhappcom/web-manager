# 297 — PWA Recovery-Root Topology Handoff & Executable Evidence Contract

Status: **PASS (generic research/handoff gate) / PRODUCT + RUNTIME + MANAGED-IPAD EXECUTION OPEN**  
Date: 2026-09-29  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Validation owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: Track A browser/storage/Service Worker mechanics; Track B recovery-state UX; Track D observation only; Software Engineering supplies implementation facts.

## Purpose

Study 296 made contradictory historical evidence claim-specific and failure-domain-aware. The next bottleneck is not another abstract recovery model. It is the handoff from generic PWA security knowledge to falsifiable product/runtime validation without inventing LogMate or MintTap production facts.

This study defines the minimum **Recovery Topology Record (RTR)** and deterministic V1 fixture required before claims such as “native is a backup”, “server is authoritative”, “MDM can recover the PWA”, “reinstall is safe”, or “sync restored the record” may be promoted.

It does **not** assert that MintTap or LogMate currently uses any particular IdP, backend, MDM, export format, sync protocol, storage schema, key hierarchy, acknowledgement model or Service Worker strategy.

## Track allocation

- **E owns** authority roots, recovery boundaries, destructive-action authority, dependency/failure domains and operational closure.
- **C owns** executable destructive/failure fixtures and non-transitive validation tiers.
- **A supplies** browser origin/storage/Service Worker mechanics and platform-version boundaries.
- **B consumes** states such as local-only, queued, recovery-required, conflict, rejected and remotely confirmed; it does not redefine authority.
- **D observes** attempts, acknowledgements, contradictions and recovery outcomes; telemetry does not elect authority.

Current bottleneck order: **E → C → A**. B/D receive transfer work only.

## SOURCE

### WebKit storage policy

WebKit documents that, starting with Safari 17 / iOS 17 / iPadOS 17, browser-app origin quota is up to 60% of total disk and overall quota up to 80%. A standalone Home Screen web app receives the same quota class as when opened in a browser app. WebKit normally evicts data by origin under storage pressure/overall-quota pressure. Persistent mode can affect eviction eligibility, but it is not a backup or independent recovery copy.

Source: https://webkit.org/blog/14403/updates-to-storage-policy/

**TRANSFER:** IndexedDB, Cache Storage and other same-origin stores must not be counted as independent recovery roots merely because they are separate APIs.

### W3C Service Workers

The current published Service Workers document is a Candidate Recommendation Draft dated 2026-09-17. Service workers are event-driven workers with registration/lifecycle/update semantics. Runtime generation/currentness remains distinct from data lineage, organizational authority and recovery completeness.

Source: https://www.w3.org/TR/service-workers/  
History: https://www.w3.org/standards/history/service-workers/

**CHANGE WATCH:** browser implementation behavior and platform policy require version-specific validation.

### NIST SP 800-63B-4 account recovery

NIST treats account recovery as a controlled authenticator-lifecycle event, distinguishes recovery from ordinary authentication, defines recovery methods, and requires recovery notifications. This is used only as a cross-domain security precedent: recovery authority deserves explicit controls and evidence rather than being inferred from ordinary login success.

Source: https://pages.nist.gov/800-63-4/sp800-63b/events/

This does not assert that MintTap/LogMate targets a NIST AAL or uses these recovery methods.

## SYNTHESIS — Recovery Topology Record (RTR)

Before product-specific recovery claims, inventory only nodes and edges that are evidenced to exist.

### Node classes

Record, where applicable:

1. account / identity provider;
2. recovery channels and recovery contacts/codes;
3. PWA installation and browser profile/origin;
4. Service Worker registration/generation;
5. protected local stores;
6. reconstructible local stores/cache;
7. operation/outbox and acknowledgement state;
8. native-mobile peer;
9. server/API boundary;
10. authoritative remote store, if one is actually designated;
11. export artifact and import/restore mechanism;
12. key/credential/recovery roots;
13. MDM/device-management control plane;
14. administrator/support/emergency authority;
15. telemetry/diagnostic observers.

Unknown nodes remain **OPEN**. Generic architecture patterns must not fill them in.

### Edge fields

For every material edge record:

- direction: read / mutate / reconcile / recover / revoke;
- credential or authority root used;
- exact meaning of acknowledgement;
- offline behavior;
- currentness source;
- retry/idempotency behavior;
- revocation/retirement path;
- schema/semantic generation;
- whether the edge can create material effects after predecessor authority is revoked;
- correlation dimensions from study 296: K/A/S/C/P/N/O/D.

### Hard guards

`multiple paths ≠ multiple independent recovery roots`  
`same user ≠ same device lineage`  
`native peer exists ≠ native peer is complete/current backup`  
`server reachable ≠ server has acknowledged all local consequences`  
`export exists ≠ restore is executable`  
`reinstall succeeds ≠ unique local data recovered`  
`MDM enrolled ≠ PWA data backup/restore behavior known`  
`Service Worker current ≠ data/schema/authority current`  
`same-origin stores ≠ independent whole-origin recovery copies`.

## Recovery-root independence is claim-specific

Independence is evaluated for a specific **claim × threat × consequence**, not assigned globally.

A nominally separate native peer and server may still share:
- one account/recovery root;
- one privileged administrator;
- one tenant/control plane;
- one compromised sync/export lineage;
- one parser/canonicalizer defect;
- one incomplete acknowledgement horizon.

Therefore copy/path count is not an assurance metric by itself.

## Weakest-path and predecessor-negative rules

A strong normal authentication path does not compensate for a materially weaker recovery path that can reconstitute the same sensitive authority.

After recovery:

`successor works ≠ predecessor powerless`.

Closure requires evidence that predecessor sessions, refresh/grant families, offline credentials, queued operations, compatibility adapters, admin paths and recovery paths can no longer create obsolete material effects at the boundaries where they matter.

This is a generic security rule. Product-specific token families and revocation semantics remain OPEN.

## Required Software Engineering handoff

Before V1 product fixtures can be instantiated, obtain canonical implementation evidence for the subset that exists:

- identity/recovery methods and authority roots;
- session/token/credential storage and revocation;
- protected vs reconstructible local stores;
- record and operation identity;
- durable transaction boundary and what UI “Saved” means;
- outbox/queue state machine;
- exact remote acknowledgement stages;
- tombstone/dedup/provenance semantics;
- conflict/convergence policy;
- export contents, omissions and import path;
- schema/version migration;
- native-peer role and authority;
- server/API/store authority;
- MDM wipe/re-enrol/backup/restore behavior;
- destructive reset/reinstall scope.

Absence of this evidence blocks product-specific promotion; it does not imply the feature is absent.

## V1 executable fixture contract

Once the relevant topology exists, C should instantiate deterministic fixtures for at least:

1. UI attempts “Saved” before durable local commit.
2. Durable local commit survives restart with stable operation identity.
3. Remote commit succeeds but ACK is lost; retry must not create duplicate consequence.
4. Remote/native candidate omits a local-only tail but appears healthy.
5. Tombstone omission resurrects deleted material.
6. Dedup/provenance omission allows replay or duplicate consequence.
7. Same-origin second store is destroyed with the primary origin.
8. Export is byte-present but cannot be imported/reconciled.
9. Schema skew makes an old copy parseable but semantically unsafe.
10. Successor session works while predecessor credential can still mutate.
11. Recovery/reset destroys evidence before inventory/preservation.
12. Reinstall restores shell but not unique local work.
13. MDM policy changes storage/network/recovery assumptions.
14. Foreground reconnection succeeds but queued work remains unresolved.
15. Telemetry says success while consequence reconciliation fails.
16. Recovery source and primary share the failure domain being tested.

Every fixture records expected consequence, required evidence, PASS/FAIL/UNKNOWN and which claim is permitted afterward.

## Validation ladder

- **V0 — static/model:** RTR structure, invariants, threat/consequence mapping.
- **V1 — deterministic fixture:** controlled roots/tokens/stores/queues/export/import/failure injection.
- **V2 — exact browser/build:** named browser/OS/app build.
- **V3 — physical unmanaged device:** lifecycle, termination, storage pressure, update/rejoin.
- **V4 — representative managed iPad/EFB:** actual management/network/trust/restriction envelope.
- **V5 — representative PWA↔native↔server topology:** real acknowledgement, convergence, restore, revocation and rollback boundaries.

PASS is non-transitive. V1 does not imply V2; physical unmanaged evidence does not imply managed-EFB evidence.

## EFB / LogMate-like transfer

For a company iPad PWA expected to remain useful offline, the following remain separate questions:

- Can the shell launch offline?
- Can unique work be durably admitted locally?
- Can the browser retain that data under the target lifecycle/storage conditions?
- Can a native peer be discovered and authenticated?
- Can transfer occur on the actual network/hotspot/MDM policy?
- Does transfer mean receipt, durable commit, reconciliation or authoritative acknowledgement?
- Can the system recover after origin loss?
- Is any recovery source independent of the failure being tested?
- Can predecessor authority be proven unable to create stale effects?

Do not assume unattended background device-to-device sync, hotspot reachability, storage persistence, MDM backup, or cross-device communication.

## CONTRADICTION / TRANSFER VALIDATION

- WebKit generic quota/eviction evidence is sufficient to reject “separate same-origin APIs are independent backups”; it is insufficient to predict survival on a particular managed iPad.
- Service Worker standards establish lifecycle mechanics; they do not establish organizational/data currentness.
- NIST account-recovery controls support treating recovery as a separate authority transition; they do not define this product’s authentication architecture.
- Software Engineering evidence may satisfy an RTR field only when it describes the actual implementation boundary. Design or marketing intent does not promote runtime facts.

## MINTTAP DECISION

1. Stop extending generic recovery theory when the next claim depends on actual topology.
2. Require an RTR before product-specific backup/sync/recovery assurance claims.
3. Count independence by relevant failure domains, not copy/vendor/path count.
4. Prefer V1 executable contradiction/failure fixtures as soon as Software Engineering exposes sufficient topology.
5. Keep production validation OPEN through the required physical/managed/topology tiers.
6. Preserve PWA as a cross-track specialization rather than a sixth track.

## OPEN

- Actual MintTap/LogMate identity, session, storage, schema, sync, export, native, server and MDM topology.
- Exact “Saved”, “Synced”, “Backed up” and “Recovered” product semantics.
- Target iPad/iPadOS/WebKit/MDM/network envelope.
- Actual acknowledgement and convergence semantics.
- Actual destructive recovery/reset/reinstall behavior.
- Physical-device, managed-device, accessibility and human validation.

## CHANGE WATCH

- W3C Service Workers publication/implementation changes.
- WebKit/iOS/iPadOS storage, persistence, eviction and Home Screen behavior.
- Apple managed-device/MDM policy and deployment behavior.
- Identity/recovery standards where used as security precedent.

## Gate result

**PASS (generic handoff gate).**

Study 296’s correlation model can now be handed to implementation validation without inventing product topology. The next high-value move is not another generic recovery primer: obtain canonical implementation facts, instantiate the RTR, then execute V1 fixtures. If those facts remain unavailable, reallocate learning to another unresolved Stage 8/PWA prerequisite rather than manufacturing product assumptions.
