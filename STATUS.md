# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-18

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–130 — **PASS at recorded generic gates.**  
131 PWA Degraded-Mode Convergence & Split-Brain Reconciliation Governance — **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL VALIDATION OPEN**.

## 131 checkpoint
- Connectivity recovery is not convergence. Re-entry requires explicit operation identity, version/provenance checks, deletion semantics and conflict policy.
- HTTP idempotency/retry safety and conditional lost-update protection are separate properties; neither substitutes for domain conflict resolution.
- Distinguish record identity, logical operation identity, actor/device, base revision, payload, server receipt/application, resulting authoritative revision, tombstone/deletion identity and replication progress.
- Last-write-wins is a possible policy, not a correctness theorem. Newest timestamp, fresh login or network restoration are insufficient authority signals for provenance-sensitive records.
- Ambiguous ACK requires durable logical-operation identity/deduplication where retry can occur; deduplication alone does not make a stale operation semantically valid.
- Deletion must not be inferred from absence. Long-offline update vs delete requires explicit tombstone/rebootstrap policy to prevent silent resurrection.
- Queue-empty is not a convergence proof; normalization requires every pending logical operation classified and stale/replay/resurrection paths negatively tested.
- Direct iPad↔phone transport remains OPEN; reconciliation semantics are transport-independent requirements.

## Persistent guards added by 131
`connectivity recovery ≠ convergence`.  
`retry-safe ≠ conflict-safe`.  
`ACK missing ≠ commit missing`.  
`retry request new ≠ logical operation new`.  
`deduplicated ≠ semantically conflict-free`.  
`last write wins ≠ latest intent wins`.  
`newest timestamp ≠ most authoritative record`.  
`different fields changed ≠ changes commute safely`.  
`record absent ≠ deletion proven`.  
`delete acknowledged ≠ every offline client observed deletion`.  
`old update arrives ≠ deleted record should resurrect`.  
`fresh login ≠ queued operation fresh`.  
`queue empty ≠ converged`.  
`client caught up ≠ fleet converged`.  
`reconciliation semantics defined ≠ transport capability proven`.

## Five-track state
- **A Platform/Browser:** dependency supplier for offline storage/restart/connectivity and Service Worker mechanics; browser storage does not define domain conflict policy.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful saved/pending/conflict/resolved/authoritative language and user-mediated reconciliation requirements.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns ambiguous-ACK, duplicate, stale-update, delete-resurrection, restart and conflict-UX oracles.
- **D Search/Discovery/Analytics:** supporting evidence only; missing telemetry cannot prove offline population convergence.
- **E Architecture/Security/Operations:** highest-risk owner; 131 closes the generic degraded-client convergence/split-brain governance boundary.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W082 SEMANTIC FOCUS IDENTITY RUNTIME PROVENANCE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Cross-browser/Safari/Firefox, persisted configuration, screen-reader, physical-device, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering Data is **Stage 1 IN STUDY / NOT YET PASSED**. D006 provides bounded executable replication/idempotency/conflict evidence plus exact-ref LogMate inbound cursor atomicity transfer; real mobile/backend, dedup/tombstone retention and multi-writer evidence remain OPEN. Web Manager consumes that evidence without duplicating implementation ownership.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; allowed offline edits/deletes; record/operation identity; base/server revision model; conflict/merge policy; dedup retention; tombstone/deletion semantics; inbound cursor/batch atomicity; encryption/key hierarchy; backup/restore; Service Worker trust; record provenance; fleet denominator; API-generation enforcement; evidence sinks; actual RTO/RPO/MTD; safety/legal constraints; and real reconciliation/destructive-recovery drills.

## Next learning mode
Highest-value adjacent generic work is **PWA reconciliation policy evolution & schema/version conflict governance**: determine how long-offline operations created under older domain schema, validation rules, conflict policy or operation format are handled without treating syntactic migration as semantic re-authorization; preserve rejected operations for recovery and prevent schema upgrades from silently rewriting historical user intent.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–131 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model validation remains OPEN.
- Reporting remains coarse/checkpoint-based.