# 313 — LogMate PWA Persistent-Storage Admission, Eviction & EFB Durability Gate

Status: **PASS (generic/platform + canonical-source contract) / PRODUCT IMPLEMENTATION + PHYSICAL/MANAGED-IPAD VALIDATION OPEN**  
Evidence date: 2026-10-05  
Curriculum: Stage 8 Security / Privacy / Trust continuous expert application  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependency owner: **Track A — Web Platform & Browser**  
Consumers: Tracks B/C/D

## Why this checkpoint exists

311 separated executable-cache retirement from unique pilot-log data and identified Storage API persistence as a high-value candidate. This checkpoint resolves the next prerequisite: what persistent storage can actually prove, when it should enter the LogMate EFB durability model, and what evidence it cannot replace.

For a company-iPad PWA that may hold unsynchronized flight records, default best-effort origin storage is an avoidable risk class. But a successful persistence request is not backup, synchronization, data-integrity proof, or managed-device policy proof.

## Canonical evidence read

At run start, Web Manager main was `69f75eea78ba914a46e54512b30aa15e66f0f77f`. Required operating files, 311/312 and recent commits were read. LogMate main was `f4e579c8590e09fb3cb4470ae885001a67890b09`; repository search still found no LogMate source evidence for `navigator.storage.persist()` / `persisted()`. Design Studio's newest commits were roster/parser evidence and supplied no physical-iPad/PWA storage validation.

This absence is **OPEN**, not proof that dependency/runtime code can never request persistence.

## SOURCE — Storage API contract

`StorageManager.persist()` requests persistent storage and resolves to true only when persistence is granted. User agents may accept or reject according to browser-specific rules. `persisted()` observes whether the current storage bucket is persistent. `estimate()` reports approximate origin usage/quota.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persisted
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate

## SOURCE — WebKit/iPadOS policy

WebKit states that Safari 17 and WebKit on iOS/iPadOS 17 added full Storage API support. Origin storage is best-effort by default. Storage-pressure/overall-quota eviction is origin-oriented and normally selects non-persistent origins; persistent mode can exempt an origin from ordinary eviction. Home-Screen web apps use the browser-app origin/overall quota class.

WebKit also documents that Home-Screen web-app first-party data is isolated from Safari for ITP purposes and exempt from ITP's seven-day script-writable-storage removal rule. This is important but narrower than general durability: it does not make Home-Screen data immune to explicit deletion, application bugs, device loss, corruption or all OS/browser lifecycle effects.

Sources:
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://webkit.org/blog/14445/webkit-features-in-safari-17-0/
- https://webkit.org/tracking-prevention/

## SYNTHESIS — five separate durability claims

For LogMate/EFB, keep these independent:

1. **Local write success** — the record/outbox write committed locally.
2. **Persistence mode** — the origin is currently reported persistent.
3. **Storage survival** — data actually survives target lifecycle/storage-pressure scenarios.
4. **Independent recovery** — another failure domain can restore irreplaceable data.
5. **Remote convergence** — server/native peer has acknowledged and reconciled the intended state.

No arrow between these is automatic.

Persistent guards:
- `persist() true ≠ backup`;
- `persist() true ≠ explicit deletion impossible`;
- `persist() true ≠ device loss survivable`;
- `persist() true ≠ IndexedDB/Sembast consistency proven`;
- `persist() true ≠ remote ACK`;
- `Home Screen ITP exemption ≠ general non-eviction guarantee`;
- `large quota ≠ reserved capacity`;
- `estimate() reports quota ≠ future write guaranteed`;
- `Safari evidence ≠ Home-Screen evidence ≠ managed-EFB evidence`.

## MINTTAP / LogMate decision

**DIRECTION:** Treat persistent-storage admission as a first-class durability control candidate for the LogMate PWA, because the product may temporarily hold unique unsynchronized pilot records.

Do not block local capture merely because persistence is not granted. Instead, persistence state should modify durability risk and recovery guidance, while remote authority and synchronization remain separate.

Implementation-level timing and retry policy belong to Software Engineering. Web Manager requires that any implementation be bounded, idempotent in effect, and observable without collecting flight-record payloads.

## Admission model

At a suitable foreground/product-ready point:

1. feature-detect `navigator.storage`;
2. observe `persisted()`;
3. if already persistent, record that state and do not repeatedly request;
4. if not persistent, make one bounded `persist()` request according to product policy;
5. observe `persisted()` again rather than assuming the request result is durable forever;
6. record only coarse diagnostics needed for durability support;
7. continue local operation even if persistence is unavailable/denied, but surface risk according to UX policy when unique unsynchronized records exist.

Do not place `persist()` in a Service Worker: MDN documents that the request method is not available in Web Workers.

## Track transfer

### A — Platform/Browser
Own Storage API semantics, secure-context requirement, quota/eviction mechanics and Safari vs Home-Screen storage-context distinctions.

### B — UX/IA
Keep “saved on this device”, “protected from ordinary browser eviction”, “backed up”, and “synced” distinct. A persistence denial must not be presented as a failed flight-log save when the local write succeeded.

### C — Quality
Validate persistence state before/after request, offline cold start, process termination, OS restart, storage pressure, worker update, cache retirement and origin-reset controls. Verify cache maintenance never erases ledger/outbox.

### D — Analytics
Persistence telemetry is diagnostic, not authority. Useful coarse fields: platform/app context, API available, before/after persistent boolean, request outcome class, approximate usage/quota bucket, local-unsynced-count bucket. Do not send flight-record contents merely to diagnose storage.

### E — Security/Operations
Own durability classification, reset blast radius, backup/restore boundary, incident runbook and managed-EFB evidence gate.

## Validation ladder

**V0 source/artifact:** establish exact local data store identity and whether production code currently calls Storage API.

**V1 disposable browser profiles:** record `persisted()`, `estimate()`, bounded `persist()`, then repeat observations after reload/restart.

**V2 data separation:** create representative local ledger/outbox + executable caches; retire only executable cache generations; prove ledger/outbox unchanged.

**V3 physical iPad:** Safari tab and Home-Screen app separately; termination, reboot, offline cold start, elapsed dormancy and controlled storage pressure.

**V4 loss/recovery:** explicitly clear website data and simulate app removal/device loss. Persistent mode must not be credited as recovery; export/backup/restore evidence is required.

**V5 managed EFB:** repeat under representative MDM/restriction/network/update policy. Management may alter installability, storage cleanup, backup, network and lifecycle conditions; no unmanaged result promotes automatically.

## OPEN

- exact LogMate Sembast/IndexedDB storage identity and migration behavior;
- current runtime persistence request/result;
- product UX for best-effort state with unique unsynced records;
- physical iPad persistence outcomes;
- managed-EFB policy interaction;
- independent backup/restore;
- remote ACK/convergence;
- elapsed-dormancy and real storage-pressure evidence.

## CHANGE WATCH

Revalidate WebKit quota/eviction/persistence policy on material Safari/iPadOS changes. Treat browser grant heuristics and OS/MDM cleanup behavior as implementation policy, not timeless Web-standard guarantees.

## Integrated competency

Persistent storage is a **risk-reduction property of an origin storage bucket**, not a recovery system. For an offline-first EFB, the defensible architecture combines bounded persistence admission, selective executable-cache maintenance, explicit local-unsynced state, independent recovery and separately proven synchronization.
