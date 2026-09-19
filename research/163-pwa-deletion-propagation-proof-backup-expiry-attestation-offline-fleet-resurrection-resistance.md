# 163 — PWA Deletion Propagation Proof, Backup-Expiry Attestation & Offline-Fleet Resurrection Resistance

Status: **PASS (generic) / PRODUCT + LEGAL + PROVIDER + BACKUP + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 135 provenance transfer; 159 bounded closure proof; 162 deletion/redaction lineage; Track A SW/Cache/IndexedDB/storage semantics; Track B truthful scope/status UX; Track C destructive convergence/restore/device testing; Track D search/analytics derived-copy minimization.

## Why this study exists

162 separated payload destruction from lineage continuity. The next failure is overclaiming deletion after one authoritative row disappears while replicas, indexes, analytics, backups, exports, queues or offline PWAs still hold copies.

Central rule:

> **Deletion completion is a bounded, scoped claim over declared control domains and current generations; it is not proof that every copy everywhere has ceased to exist. Resurrection resistance requires current deletion authority to dominate stale data whenever old backups, exports, queues or offline devices re-enter an authoritative path.**

## Five-track balance

- **A Platform/Browser — critical dependency:** browser storage is per-origin and may include IndexedDB, Cache API, OPFS and other state. Persistence/eviction is browser policy, not fleet deletion evidence. Service-worker cache cleanup is not IndexedDB or export cleanup.
- **B UX/IA/Content — elevated consumer:** user/operator wording must distinguish scoped completion, pending convergence, backup expiry pending, unmanaged-copy unknown and reconnect conflict.
- **C Performance/Accessibility/Quality — high pressure:** owns destructive propagation, restore, stale-export/import, queue and long-offline reconnect campaigns; verifies that safety states remain accessible and do not deadlock data recovery.
- **D Search/Discovery/Analytics — constrained consumer:** derived indexes/events must participate in deletion policy without turning telemetry into a privacy-rich global subject inventory.
- **E Architecture/Security/Operations — highest-risk owner:** owns deletion scope, generation/floor semantics, backup expiry, restore gates, propagation evidence and resurrection resistance.

Allocation remains E-heavy with A/C dependencies. Legal scope and actual provider capabilities remain OPEN.

## SOURCE

### Current browser storage reality

MDN documents that browser origins can hold data in IndexedDB, Cache API, OPFS, Web Storage and cookies, with browser-specific quotas and eviction. Best-effort storage can be evicted; persistent storage changes eviction behavior but is not backup. WebKit documents that Home Screen web apps use browser-app-class origin quota on current iOS/iPadOS/macOS generations and that eviction can occur under storage pressure or other policy conditions.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Caching

**TRANSFER VALIDATION:** browser storage APIs describe local persistence/eviction mechanics. They do not provide a server-visible proof that every device copy has been deleted. A Service Worker `activate` cleanup can remove named caches, but it is not evidence that IndexedDB, OPFS, downloads or user exports were removed.

### Backup erasure and restore safety

The UK ICO states that valid erasure can require steps covering backup systems; where immediate overwrite is not feasible, backup data may remain until scheduled replacement provided it is put beyond ordinary use and not used for another purpose. The guidance explicitly requires clarity about what happens to backup copies. This is jurisdiction-specific evidence, not a MintTap legal conclusion.

Source:
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/

The EDPB's 2025 coordinated-enforcement work on right to erasure highlights backup deletion as a practical challenge. Its 2026 report/annex notes the importance of procedures that preserve erasure after restoration from backups, including identifying erased records so restored operational systems do not silently resurrect them.

Sources:
- https://www.edpb.europa.eu/news/edpb-identifies-challenges-hindering-the-full-implementation-of-the-right-to-erasure_en
- https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf
- https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_annex_en.pdf

**TRANSFER VALIDATION:** the durable systems lesson is restore-time deletion reconciliation and honest backup lifecycle claims. Exact legal obligations depend on jurisdiction, role, purpose, exemptions and product facts.

## SYNTHESIS — deletion completion needs a declared scope

A deletion claim should identify at least:
1. **subject/record/effect scope** without retaining unnecessary identifying payload;
2. **controlled storage classes** — primary, replicas, caches, indexes, analytics/log projections, backups, managed device state, exports if controlled;
3. **deletion generation/floor** that dominates earlier versions;
4. **propagation state** per relevant class;
5. **backup horizon/expiry state**;
6. **unobservable or unmanaged domains** explicitly excluded from the claim;
7. **evidence time/currentness** and evidence source;
8. **re-entry rules** for stale data.

Persistent guards:
- `primary delete ACK ≠ deletion convergence`;
- `all observed replicas clean ≠ all possible copies erased`;
- `telemetry reports zero stale copies ≠ cryptographic proof of universal absence`;
- `backup expired by schedule ≠ backup destruction attested`;
- `backup destruction attested ≠ unmanaged export destroyed`;
- `device offline ≠ deletion failed within server-controlled scope`;
- `device reconnects with old bytes ≠ old bytes become current`;
- `old export authentic ≠ import authorized to resurrect deleted lineage`;
- `cache cleared ≠ IndexedDB cleared ≠ export cleared`;
- `storage persisted ≠ storage backed up`;
- `storage evicted ≠ governed deletion completed`.

## Bounded deletion proof

Do not create a global table containing every person's sensitive data merely to prove deletion. Prefer a proof surface based on minimum operational metadata, for example:
- opaque deletion lineage/generation;
- storage-class or processor identifier at the minimum useful granularity;
- observed state: `PENDING`, `CONVERGED`, `EXPIRED/DESTROYED`, `BEYOND-USE`, `UNKNOWN`, `OUTSIDE-CONTROL`;
- observation/attestation generation and time;
- verifier/source class;
- failure/exception class without copied sensitive payload;
- successor/current deletion floor.

The exact schema is OPEN. A proof inventory itself is personal/security-sensitive if stable identifiers permit correlation, enumeration or reconstruction. Access, retention and aggregation therefore require their own minimization policy.

### Negative proof limit

Absence is difficult to prove globally. A defensible claim is normally:

`Within declared controlled domains D, under generation G and evidence horizon H, required stores report/verify the deletion invariant; domains U are unobservable/outside control and are not included.`

This is stronger and more truthful than `deleted everywhere`.

## Propagation model

Deletion propagation is not one distributed transaction. Derived systems may have different semantics and latency.

Generic states:
`REQUESTED → AUTHORITATIVE-DELETED → PROPAGATING → CONTROLLED-DOMAINS-CONVERGED → BACKUP-EXPIRY-PENDING → SCOPED-COMPLETE`

Side states:
`HOLD`, `FAILED`, `UNKNOWN`, `OUTSIDE-CONTROL`, `REOPENED/RESURRECTION-BLOCKED`.

A system may reach controlled-domain convergence while immutable/append-only backup generations remain inside a governed expiry window. The UI/audit claim must say so rather than collapsing both to `complete`.

## Backup expiry attestation

A retention schedule predicts when a backup should age out; it does not prove that it did.

Evidence strength can range from:
1. policy/configuration evidence that defines retention;
2. provider inventory showing relevant recovery points no longer ordinarily selectable;
3. provider deletion/expiry event or API evidence;
4. cryptographic-erase evidence where validated key topology applies;
5. independent restore challenge demonstrating that a pre-deletion generation cannot re-enter normal service without current deletion reconciliation.

No generic level is automatically sufficient for MintTap. Provider semantics, legal requirements and risk determine the needed assurance.

### Restore gate

A pre-deletion backup may remain valid for disaster recovery while being unsafe as current application truth. Before ordinary traffic:
- recover current deletion/retention floor from a non-rollback-prone authority;
- compare restored record generations against that floor;
- quarantine/suppress payloads that are intentionally unavailable;
- rebuild derived indexes/projections from the reconciled state;
- prevent old queues/jobs from republishing stale payload;
- record reconciliation evidence.

`restore completed ≠ service safe to reopen`.

## Offline fleet and resurrection resistance

### Controlled managed device

If product/MDM/runtime evidence eventually establishes a managed-device deletion channel, it can participate in the declared controlled domain. Until validated, do not claim it.

### Long-offline PWA

A company iPad can miss multiple deletion generations. On reconnect:
1. preserve unique local user/flight data pending authority classification;
2. fetch current deletion/retention authority independently of cached SW/UI state;
3. compare local lineage/generation with current server floor;
4. block automatic upload of stale remotely-deleted lineage;
5. distinguish stale replica from unique unsynced local record;
6. require explicit reconciliation where classification is ambiguous;
7. update local projections/cache only after safe classification;
8. retain minimum non-sensitive evidence of the conflict/outcome.

A stale Service Worker, IndexedDB row or offline queue is data, not authority.

### Old exports/imports

Exports are a major resurrection path. An old package can be authentic and complete for its creation time yet conflict with a later deletion generation. Import must therefore validate current server retention/deletion state before admitting records into an authoritative namespace. Historical inspection/recovery can be separate from ordinary mutation authority.

`package integrity PASS ≠ resurrection authority PASS`.

## Search, analytics and observability boundary

Track D can expose aggregate propagation health such as stale-generation counts by storage class, but subject-level deletion telemetry should not become a new permanent cross-system identity graph. Prefer:
- bounded operational identifiers;
- short retention where possible;
- aggregate counters for fleet health;
- restricted detailed evidence only where needed for reconciliation/audit;
- no deleted payload in metrics dimensions or logs.

`observability sufficient for operations ≠ retain a privacy-rich global inventory`.

## UX truthfulness

Suggested semantic states, not final UI copy:
- **Deletion in progress** — controlled stores are still converging.
- **Server-controlled deletion complete** — declared online/control-plane stores satisfy the invariant; unmanaged copies are not claimed.
- **Backup expiry pending** — ordinary access is blocked but protected recovery generations remain within policy.
- **Backup expiry verified** — evidence supports expiry/destruction under the declared provider/control scope.
- **Offline device status unknown** — device has not reconnected; no universal device-erasure claim.
- **Local copy conflicts with remote deletion** — reconciliation is required; no automatic upload/destruction.

Accessibility requires state changes to be exposed through semantics/status messaging, not color alone. Human validation remains OPEN.

## MINTTAP DECISION — generic governance

1. Define deletion completion as a scoped invariant over declared controlled domains, not universal absence.
2. Carry a monotonic deletion/retention generation or equivalent authoritative floor that stale backups, exports, queues and devices cannot override.
3. Separate online controlled-domain convergence from backup expiry/destruction and unmanaged-copy status.
4. Treat backup schedules as expectations; obtain evidence appropriate to the risk before claiming expiry/destruction.
5. Gate restore/reopen on current deletion-floor reconciliation; do not let PITR become a deletion time machine.
6. Require imports and reconnecting offline clients to compare against current deletion authority before republishing old lineage.
7. Preserve unique local data when authority is ambiguous; block remote mutation rather than destructively guessing.
8. Minimize deletion-proof telemetry so proof infrastructure does not become a new personal-data inventory.
9. Never infer managed-iPad fleet deletion, MDM reachability or browser-storage destruction without runtime evidence.
10. Keep jurisdiction-specific erasure/retention conclusions OPEN for legal review.

## VALIDATION — 88-case destructive propagation/resurrection campaign

1 primary delete accepted; 2 primary read denied; 3 replica stale; 4 detect; 5 replica converges; 6 prove generation; 7 CDN/app cache stale; 8 invalidate; 9 search index stale; 10 purge/rebuild; 11 analytics event retained; 12 apply declared policy; 13 support export stale; 14 classify control scope; 15 security log contains payload; 16 minimization defect; 17 deletion proof store contains raw identifier; 18 privacy defect; 19 opaque proof id still globally linkable; 20 reassess; 21 propagation worker ACK lost; 22 reconcile before retry; 23 duplicate deletion command; 24 idempotent result; 25 delayed projection rebuild; 26 no premature complete; 27 one processor unavailable; 28 state UNKNOWN/PENDING; 29 processor returns after floor advanced; 30 stale data suppressed; 31 backup schedule says expired; 32 inventory still exposes recovery point; 33 do not attest destruction; 34 provider expiry event received; 35 verify scope/currentness; 36 immutable backup cannot selective-delete; 37 beyond-use/expiry policy represented honestly; 38 restore pre-delete snapshot; 39 current floor reapplied; 40 stale payload quarantined; 41 old search index restored; 42 rebuild after reconciliation; 43 old async job restored; 44 block stale publish; 45 PITR rolls proof DB back too; 46 recover deletion floor independently; 47 deletion-floor store unavailable; 48 do not reopen ordinary service with unknown authority; 49 cryptographic erase claimed; 50 wrapped key survives; 51 claim fails; 52 plaintext projection survives; 53 claim fails; 54 managed iPad online; 55 runtime deletion channel remains product OPEN; 56 iPad offline through deletion; 57 server scope can converge without claiming device erased; 58 reconnect with stale remote row; 59 block auto-upload; 60 reconnect with unique unsynced flight row; 61 preserve pending classification; 62 mixed local DB contains both; 63 classify per lineage; 64 stale SW serves old payload; 65 current authority overrides UI cache; 66 Cache API cleared; 67 IndexedDB still contains row; 68 no false device-deletion claim; 69 browser evicts origin; 70 do not record governed deletion from eviction alone; 71 persistence granted; 72 do not call backup; 73 user export predates deletion; 74 import as historical package only until current check; 75 import tries ordinary mutation; 76 reject stale lineage; 77 package re-signed recently; 78 recent signature does not make payload current; 79 device clock ahead; 80 do not order authority by local clock; 81 proof telemetry aggregate zero; 82 inject hidden stale store and verify aggregate cannot certify universal absence; 83 accessible pending/complete/unknown states; 84 no color-only status; 85 screen-reader announcement remains OPEN until observed; 86 physical managed-iPad multi-generation reconnect remains OPEN; 87 provider backup expiry/destruction semantics remain OPEN; 88 legal/product deletion scope remains OPEN.

## CONTRADICTION / failure modes

### Universal-erasure theater
A dashboard showing zero known stale replicas proves only what its instrumentation observes. Unknown exports, unmanaged devices or uninstrumented processors remain outside the claim.

### Privacy-rich deletion ledger
A central ledger containing permanent subject identifiers and every processor touched can become more privacy-sensitive than the data it was designed to help erase. Proof minimization applies to the deletion system itself.

### Backup-expiry theater
A configured 30-day retention setting is not evidence that every old recovery object disappeared on day 30. Provider semantics, holds, replication and failure need evidence.

### Restore resurrection
A technically successful PITR can violate current retention authority. Current deletion floors must dominate restored historical state before service reopen.

### Offline-fleet false failure / false success
An unreachable iPad neither proves fleet deletion failed nor proves it succeeded. Scope the server claim and reconcile the device when it returns.

### Browser-eviction confusion
Browser eviction can destroy local data without an application deletion event. Conversely persistent storage can retain local data longer. Neither behavior proves governed server/fleet deletion.

## OPEN / DEPENDENCY

- Actual MintTap/LogMate legal deletion and aviation-record retention obligations: OPEN.
- Actual local-vs-server authority for flight records: OPEN.
- Actual provider DB/replica/cache/search/analytics/log/backup topology and deletion APIs: OPEN.
- Actual backup retention, legal holds, object-lock/immutability and destruction attestations: OPEN.
- Actual deletion-floor schema and rollback-resistant storage: OPEN.
- Actual Service Worker/IndexedDB/Cache/OPFS/export schema: OPEN.
- Actual managed-iPad MDM reachability and data-clearing semantics: OPEN.
- Actual import/export package and stale-lineage admission behavior: OPEN.
- Actual telemetry identifiers/retention/privacy assessment: OPEN.
- Actual screen-reader/human UX validation: OPEN.

## CHANGE WATCH

- Browser/WebKit storage quota, persistence and eviction policy.
- Managed Web App/MDM capabilities on supported iPadOS versions.
- Provider backup/PITR deletion and immutable-retention capabilities.
- EDPB/ICO and applicable Korean/other jurisdiction guidance on erasure/backups.
- Any product decision that changes whether local EFB data is authoritative, replicated or merely cached.

## Gate result

**PASS (generic).** Web Manager can now distinguish deletion intent, controlled-domain convergence, backup expiry, unmanaged-copy uncertainty and resurrection resistance; can design bounded evidence without claiming universal absence; and can apply the model to PWA restore/import/offline reconnect scenarios.

Production PASS remains OPEN.

## Next highest-value target

**PWA deletion authority conflict, retention/legal hold precedence & cross-jurisdiction policy convergence.** The next adjacent problem is when deletion intent conflicts with retention/aviation/legal hold or multiple policy domains: determine how authority is represented without embedding legal conclusions in client code, how offline clients learn a current hold/deletion outcome, how a released hold creates a new deletion generation, and how policy disagreement avoids both premature destruction and indefinite silent retention.