# 083 — Change Watch: PWA Storage Durability & Service-Worker Standards, 2026-09

Status: **PASS — continuous expert maintenance checkpoint**  
Date: 2026-09-16
Primary owners: **A Platform/Browser + E Architecture/Security/Operations**  
Consumers: B offline/recovery UX; C resilience/validation; D installed-PWA measurement boundaries.

## Trigger
The sequential curriculum is complete. This maintenance cycle selected PWA durability because it is high-consequence for the LogMate/EFB-like scenario and current standards/platform evidence has materially changed or clarified since older PWA guidance.

## 1. Service Workers remain active standards work
**SOURCE:** W3C publication history shows Service Workers received repeated Candidate Recommendation Draft publications through **2026-08-12**. Therefore the service-worker model is mature enough to be a core platform primitive, but the specification is still actively maintained rather than frozen.

**CHANGE WATCH:** Do not fossilize one browser's worker-update behavior or an old tutorial into permanent company policy. Preserve the durable lifecycle/control model, while re-checking implementation-specific edge cases before consequential releases.

## 2. Storage persistence is request/state, not a backup guarantee
**SOURCE:** StorageManager `persist()` requests persistent storage and returns whether persistence was granted; the user agent may decline according to browser-specific rules. `persisted()` reports current persistence state. `estimate()` reports approximate origin usage/quota. These APIs require a secure context where applicable.

**SYNTHESIS:**
`storage API available ≠ persistence granted ≠ data independently backed up`.

Persistent mode can reduce automatic eviction risk, but it does not create another copy, validate data integrity, export data, synchronize another device, or prove recovery after browser/app/device loss.

## 3. WebKit's modern quota model materially supersedes old fixed-quota folklore
**SOURCE:** WebKit's Safari 17 storage-policy update states that browser-app overall quota may reach up to 80% of disk and other apps up to 20%; standalone Home Screen Web Apps receive the same origin/overall quota treatment as browser use. WebKit also states that origins in persistent mode are exempt from eviction under its quota mechanism.

**CONTRADICTION:** Old guidance such as a universal WebKit 50 MiB Cache API ceiling is historical implementation evidence, not a current general Safari rule. The 2018 WebKit service-worker article is valuable history but must not be used as 2026 quota policy.

**CHANGE WATCH:** Exact quotas and eviction heuristics are browser policy and can change. Product acceptance must not encode a fixed quota number unless verified for the supported fleet.

## 4. Eviction remains a product risk
**SOURCE:** Current WebKit storage policy documents eviction when overall quota is exceeded, the system is under storage pressure, or inactivity/tracking-prevention policy applies. MDN likewise distinguishes best-effort from persistent storage and documents storage-pressure/browser-limit/proactive eviction behavior.

**SYNTHESIS:** For replaceable HTTP resources, eviction can often be repaired by refetch. For irreplaceable local pilot records, eviction is a data-loss event unless an independent recovery copy exists.

Therefore classify PWA storage by data class:
- **reconstructible shell/assets** → cache policy can accept eviction;
- **reconstructible remote data** → local cache may be disposable if server authority is healthy;
- **pending local operations/outbox** → must survive expected offline window or have explicit recovery semantics;
- **irreplaceable user-authored records** → local browser storage alone is insufficient as the only recovery copy.

## 5. Durability acceptance contract
For a high-consequence offline PWA, acceptance should separately verify:
1. secure origin and exact accepted artifact provenance;
2. IndexedDB/schema open + migration behavior;
3. persistence request/status where supported and meaningful;
4. storage usage/quota observation as diagnostic evidence, not capacity promise;
5. offline create/edit/read after process termination and device restart where product requires it;
6. behavior after worker/cache update while local data exists;
7. long-offline skipped-version migration;
8. outbox idempotency/reconciliation after connectivity returns;
9. independent backup/export/remote-copy path for irreplaceable data;
10. tested restore onto a clean/new environment;
11. explicit user-visible recovery state when durability/sync/backup cannot be confirmed.

**VALIDATION:** Generic standards documentation can establish API semantics. It cannot establish managed-iPad policy, actual persistence grant, storage pressure behavior, long-offline survival, or product recovery. Those require exact-device/artifact tests owned by Product + Software Engineering.

## 6. EFB/LogMate transfer
**TRANSFER VALIDATION:** Existing Web Manager guards remain correct and gain stronger current evidence:
`local save ≠ persistent storage ≠ sync queued ≠ remote acknowledgement ≠ backup ≠ tested restore`.

For a company-managed iPad, do not promise "your logbook is safely stored offline" solely because IndexedDB works or `persisted()` is true. A defensible product claim needs a defined supported offline interval, independent recovery path, and physical managed-device evidence.

The previously observed white-screen preview artifact remains bounded failure evidence for that artifact path. It does not establish storage eviction as the cause.

## 7. Cross-track consequences
### A Platform/Browser
Own current service-worker/storage semantics and browser-policy change-watch.

### B UX/IA/Content
Offline UX should distinguish **saved locally**, **sync pending**, **synced**, **backup/recovery verified**, and **storage/recovery warning** where product risk warrants it. Avoid a single ambiguous "Saved" state if it masks materially different durability states.

### C Performance/Accessibility/Quality
Eviction/refetch performance and offline recovery are resilience tests, not only performance tests. Physical Safari/iPad, process termination, storage pressure where safely reproducible, update-with-local-data and accessibility of recovery states belong in product validation.

### D Search/Discovery/Analytics
Analytics arrival cannot prove local durability or synchronization. Offline events may arrive late or never; occurrence time and ingestion time remain distinct.

### E Architecture/Security/Operations
Persistence is one layer in a durability architecture. Independent backup/restore, schema/version compatibility, incident recovery, privacy of exported/backed-up records and device-loss handling remain separate controls.

## 8. Operational decision rule
For high-value local data, choose architecture by required recovery guarantee rather than by storage quota size:
`data criticality → acceptable loss window → offline requirement → local persistence → remote/independent copy opportunity → conflict/reconciliation → restore path → tested recovery evidence`.

A larger quota reduces capacity pressure; it does not solve the recovery problem.

## 9. OPEN
- managed company iPad exact OS/WebKit/MDM storage policy;
- whether Home Screen installation is permitted and retained by company policy;
- actual `navigator.storage.persist()` behavior on target fleet;
- LogMate canonical data schema/migration and outbox implementation;
- independent backup destination and restore UX;
- storage-pressure and long-inactivity behavior on the actual EFB fleet;
- direct unattended PWA↔native transport remains separately OPEN.

## Sources checked 2026-09-16
- W3C Service Workers publication history — latest listed Candidate Recommendation Draft 2026-08-12.
- WebKit, *Updates to Storage Policy* — modern Safari/WebKit quota and eviction model.
- WebKit, *WebKit Features in Safari 17.0* — Storage API and quota-policy implementation context.
- MDN, `StorageManager.persist()`, `persisted()`, `estimate()` and storage quotas/eviction criteria — cross-browser API semantics and diagnostic guidance.
- WebKit, *Workers at Your Service* (2018) — retained only as historical evidence; old fixed Cache API quota must not be generalized to current Safari.

## Maintenance result
No production certification is claimed. This cycle materially updates the PWA durability evidence base and identifies an important historical-knowledge trap: **old WebKit fixed-quota guidance must not be reused as current Safari storage policy**.