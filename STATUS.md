# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–146 — **PASS at recorded generic gates.**  
147 PWA Assurance-Event Retention, Cursor/Checkpoint Continuity & Monitoring-Gap Reconstruction — **PASS (generic) / PRODUCT + PROVIDER-RETENTION + CURSOR + EVENT-STORE + MANAGED-IPAD VALIDATION OPEN**.

## 147 checkpoint
- Monitoring continuity is decomposed into source retention, source order/coverage guarantees, local ingestion, local processing and current-state observation; none implies the next.
- Coverage is modeled by source/dependency stream, source epoch and interval rather than one global cursor.
- A cursor is completeness evidence only when the upstream source contract actually supplies the required scope/order/contiguity/retention semantics; otherwise it is a resume hint.
- Retention expiry or long outage creates an explicit monitoring gap. Current-state reconciliation can recover `now` without inventing intermediate transitions.
- Durable processing checkpoints must not advance beyond justified durable admission/effects; exact transaction mechanics remain an implementation handoff.
- Compaction/archive policy preserves claim-relevant boundaries, provenance, integrity and future readability while acknowledging discarded detail cannot be reconstructed from a digest alone.
- Backup restore is a rollback event for monitoring state: restored cursors/checkpoints require source replay/reconciliation and cannot lower established trust floors.
- For PWA/EFB, server/provider monitoring coverage, served runtime, Service Worker/device activation and local iPad history remain separate evidence scopes.

## Persistent guards added by 147
`cursor stored ≠ source history retained`.  
`cursor advanced ≠ every source event received`.  
`sequence ordered ≠ sequence gap-free`.  
`contiguous-looking IDs ≠ completeness guaranteed`.  
`resume token ≠ audit checkpoint`.  
`local event store complete ≠ upstream source complete`.  
`checkpoint persisted ≠ effects persisted`.  
`current state recovered ≠ intermediate transitions reconstructed`.  
`same state before/after gap ≠ no transition occurred during gap`.  
`backup restored ≠ monitoring coverage restored`.  
`compaction successful ≠ discarded evidence reconstructable`.  
`archive digest retained ≠ archived events recoverable`.  
`no known gap ≠ proven continuous coverage`.  
`server event archive complete ≠ device activation history complete`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; owns exact observable SW/browser/WebKit/storage/runtime generation semantics and keeps device activation evidence separate from server event history.
- **B UX/IA/Content:** elevated dependency pressure; consumes history-gapped/current-state-recovered/revalidation-required states without false “fully verified” claims.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns cursor reset, retention expiry, replay, partial-processing, archive-readability, backup-restore and gap-reconstruction test provenance.
- **D Search/Discovery/Analytics:** constrained supporting consumer; monitoring-health telemetry can expose lag/gap/retention health but cannot prove source completeness.
- **E Architecture/Security/Operations:** highest-risk owner; 147 closes generic retention/cursor/checkpoint/compaction/restore gap-reconstruction judgment.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W096 SERVED SCROLL-ANCHOR + FOCUS TRANSFER; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/input, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, account/device identity, trust-floor storage, reset/rebootstrap authority, server-side idempotency, approval/succession workflow, runtime authority inventory, dormant-access detection, evidence/exception store, dependency graph/change-event sources, provider APIs/webhook verification, event retention/cursor/source-epoch semantics, event-store/checkpoint transactions, archive/compaction, reconciliation implementation, backup/restore and managed-device integration remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; base/server revision model; conflict/merge/correction policy; provenance schema/integrity/transaction scope; compaction policy; export/import/package format; lineage topology; checkpoint/range/parent model; canonicalization; encryption/signature/MAC algorithms; key/trust-root hierarchy and custody; verifier topology and historical retention; algorithm/key/verifier transition format; compromise detection/revocation; successor/recovery authority and independence; trust-policy metadata; trust-floor storage; reset/rebootstrap authorization; recovery request/approval/execution model; organizational succession; predecessor revocation; recovery-authority inventory; dormant/orphaned/service identities; provider/failure-domain mapping; alternate/recovery credential custody and aging; IdP/provider outage behavior; break-glass lifecycle; drill environment/cadence/evidence; evidence validity envelopes; exception workflow/debt; assurance aggregation; assurance dependency graph/typed edges; change-event authenticity/source semantics/retention/cursors/source epochs; event-store checkpoint/compaction/archive semantics; reconciliation APIs/authority/independent observers; first-bootstrap vs replacement-device classification; lost-device revocation; timestamp/anchor/witness evidence; browser file/share APIs; backup semantics; operation receipt/dedup; tombstones; retention obligations; audit/analytics separation; inbound cursor atomicity; Service Worker trust; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; and real recovery/succession/survivability drills.

## Next learning mode
Highest-value adjacent generic work is **PWA assurance coverage SLOs, lag/gap severity & consequence-based escalation**: determine when delayed monitoring, unrecoverable gaps or unobservable dependencies are degraded telemetry versus conditions that must block release/recovery/remote mutation, using dependency consequence and evidence class rather than a universal timeout.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–147 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/anchor/backup/compromise/re-entry/reset/recovery-authority/succession/inventory/drill/evidence-freshness/exception/dependency-graph/event-source/retention/cursor/checkpoint/reconciliation runtime validation remains OPEN.
- Reporting remains coarse/checkpoint-based.