# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-18

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–133 — **PASS at recorded generic gates.**  
134 PWA Provenance Publication Atomicity & Partial-History Recovery — **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + BACKEND VALIDATION OPEN**.

## 134 checkpoint
- Transaction atomicity has scope: two sequential writes or two systems do not become one atomic commit because one function/request coordinates them.
- Define the authoritative acceptance unit before publication order. Where consequence requires it, business effect + minimal provenance + operation receipt/dedup state should become durable together under one authoritative transaction when architecture permits.
- Asynchronous derivatives may use a durable publication intent/outbox; committed intent is not proof of downstream application.
- Projection committed/provenance missing, provenance claim/effect missing, ACK lost after valid commit, and cursor outrunning effects are distinct failure states.
- Current projection generally cannot reconstruct lost authorship, rejected branches, transformer/policy version or correction history. Missing history remains explicit rather than inferred.
- Partial-history states distinguish COMPLETE-VERIFIED, EFFECT-VERIFIED/HISTORY-INCOMPLETE, HISTORY-CLAIM/EFFECT-UNVERIFIED, REPAIR-PENDING, REPAIRED-WITH-PROVENANCE and UNVERIFIABLE.
- Local IndexedDB atomicity cannot atomically commit a future remote server effect; long-offline PWA reconnect therefore needs durable logical operation identity and explicit remote acceptance/reconciliation state.

## Persistent guards added by 134
`two writes in one function ≠ one atomic commit`.  
`transactional locally ≠ transactional across browser/server`.  
`projection durable ≠ provenance durable`.  
`history missing ≠ effect absent`.  
`provenance entry exists ≠ business effect committed`.  
`outbox committed ≠ downstream applied`.  
`downstream applied ≠ client received ACK`.  
`current projection ≠ invertible history`.  
`projection rebuildable from history ≠ history rebuildable from projection`.  
`repair created provenance ≠ original provenance recovered`.  
`local transaction committed ≠ remote transaction committed`.  
`queue item removed ≠ authoritative receipt preserved`.  
`atomic provenance required ≠ duplicate full sensitive payload per revision`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; IndexedDB transaction mechanics bound local atomicity, but browser/server publication remains separate.
- **B UX/IA/Content:** high dependency pressure; owns truthful saved/queued/accepted/history-incomplete/repair-required explanations.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns crash-point, split-publication, duplicate/retry, rebuild and repair oracles.
- **D Search/Discovery/Analytics:** constrained supporting consumer; telemetry may observe publication failures but is neither commit record nor business provenance.
- **E Architecture/Security/Operations:** highest-risk owner; 134 closes generic acceptance-unit, publication-atomicity and partial-history-recovery boundaries.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W085 CAUSAL-UNDO SERVED-RUNTIME CLOSURE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering Data is **Stage 1 IN STUDY / NOT YET PASSED**. D005 supplies bounded SQLite crash/capacity evidence; D006 supplies commit-before-ACK, deduplication and cursor/effect atomicity evidence including an exact-ref LogMate pre-implementation invariant. Real mobile/backend, Flutter, storage and multi-writer evidence remain OPEN. Web Manager consumes these without duplicating implementation ownership.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation identity; base/server revision model; conflict/merge/correction policy; provenance schema/integrity/transaction scope; outbox/publication mechanism; operation receipt/dedup semantics; rejected-operation retention; tombstone semantics; privacy/legal/aviation/investment retention; audit access; analytics/logging separation; inbound cursor/batch atomicity; encryption/key hierarchy; backup/restore; Service Worker trust; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; safety/legal constraints; and real migration/reconciliation/destructive-recovery drills.

## Next learning mode
Highest-value adjacent generic work is **PWA provenance integrity under compaction/export/import and cross-device transfer**: determine how bounded lineage remains attributable and non-misleading when history is compacted, exported for backup/device migration, imported into a new trust context, or merged with another device lineage; separate chain continuity from content availability and current authorization.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–134 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend validation remains OPEN.
- Reporting remains coarse/checkpoint-based.