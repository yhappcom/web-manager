# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-18

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–131 — **PASS at recorded generic gates.**  
132 PWA Reconciliation Policy Evolution & Schema/Version Conflict Governance — **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL VALIDATION OPEN**.

## 132 checkpoint
- Syntactic migration can make old data readable; it does not make old intent semantically valid or currently authorized.
- Separate storage schema, domain/record schema, operation format, validation-policy epoch, authorization/trust epoch, conflict-policy epoch, API generation, application/worker generation, base revision and migration provenance.
- Compatibility is directional/relational: read-compatible, write-compatible, parseable, lossless and semantically equivalent are different claims.
- IndexedDB `versionchange` can atomically change local structure but does not prove semantic migration of queued operations.
- Service Worker activation/control can overlap application/storage generations; `skipWaiting()`/`clients.claim()` are not atomic whole-application migrations.
- Preserve original operation/provenance and transform to a candidate current operation. If semantic equivalence cannot be demonstrated, reject/quarantine/recover rather than silently rewriting user intent.
- Current authorization, base revision and current domain invariants remain admission gates after migration.
- Rejected obsolete operations can remain valuable user data; remote mutation retirement and read/export/recovery are separate capabilities.

## Persistent guards added by 132
`syntactic migration ≠ semantic re-authorization`.  
`schema structurally current ≠ record semantically current`.  
`parseable ≠ lossless ≠ same domain meaning`.  
`backward-readable ≠ backward-writable`.  
`new worker active ≠ every client/data schema migrated`.  
`skipWaiting + claim ≠ atomic application migration`.  
`operation translated ≠ operation valid against current base`.  
`migration function success ≠ semantic equivalence proven`.  
`default inserted ≠ user chose default`.  
`valid under old policy ≠ valid under current policy`.  
`historical record grandfathered ≠ obsolete mutation authority grandfathered`.  
`old conflict policy recorded ≠ old conflict policy remains executable`.  
`version marker advanced ≠ every semantic migration completed`.  
`operation rejected ≠ user data should be silently deleted`.  
`old data recoverable ≠ old writer supported`.

## Five-track state
- **A Platform/Browser:** high dependency supplier for IndexedDB versionchange and Service Worker/client-generation overlap; browser structural migration does not define domain semantics.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful migration/review/rejected/recovered/authoritative states and non-destructive correction/recovery UX.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns interrupted migration, mixed-generation, old-reader/new-writer, stale-policy replay, unknown-field-loss and recovery oracles.
- **D Search/Discovery/Analytics:** supporting evidence only; version telemetry can diagnose but missing offline clients prevent fleet-compatibility inference.
- **E Architecture/Security/Operations:** highest-risk owner; 132 closes generic schema/policy evolution and stale-operation admission governance.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W083 DYNAMIC FOCUS-REMOVAL RUNTIME CLOSURE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering Data is **Stage 1 IN STUDY / NOT YET PASSED**. D003 establishes relational reader/writer/schema compatibility and split-publication migration hazards; D006 supplies bounded replication/idempotency/cursor evidence. Real mobile/backend, Flutter, migration and multi-writer product evidence remain OPEN. Web Manager consumes these without duplicating implementation ownership.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation identity; base/server revision model; conflict/merge policy; rejected-operation retention; dedup/tombstone semantics; inbound cursor/batch atomicity; encryption/key hierarchy; backup/restore; Service Worker trust; record provenance; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; safety/legal constraints; and real migration/reconciliation/destructive-recovery drills.

## Next learning mode
Highest-value adjacent generic work is **PWA reconciliation auditability & user-correction provenance**: determine how automated migration, conflict resolution and later user correction preserve an explainable chain from original local intent to authoritative current state without defaulting to heavyweight event sourcing; cover correction vs mutation, provenance compaction, privacy/minimization, retention and user-visible explanation boundaries.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–132 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model validation remains OPEN.
- Reporting remains coarse/checkpoint-based.