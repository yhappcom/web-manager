# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–150 — **PASS at recorded generic gates.**  
151 PWA Policy Rollout Cohort Integrity, Cross-Generation Transaction Consistency & Split-Policy Convergence — **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + TRANSACTION/POLICY-RUNTIME VALIDATION OPEN**.

## 151 checkpoint
- Consistency is split into request, logical-transaction, rollout-cohort and fleet-convergence scopes; they are not interchangeable.
- Consequence-bearing multi-step operations require an explicit cross-generation rule: PINNED, REVALIDATE-FORWARD or ABORT/RESTART. Request-by-request mixing cannot cherry-pick permissions from incompatible generations.
- A pinned generation is not immortal authority: security revocation/trust retirement can invalidate an in-flight transaction.
- Final execution should bind transaction identity/significant data, authorization state, accepted policy/evaluator generation lineage, trust context and expiry/consumption state.
- Retry/idempotency preserves operation identity; it is not a fresh authorization opportunity. ACK loss after commit reconciles the durable result rather than re-executing under a newly permissive generation.
- Cohort assignment is authority-bearing when it changes authorization and therefore cannot be client-selected. Stable bucketing does not preserve a retired policy.
- Managed authorization services may be eventually consistent; control-plane update acknowledgement does not prove all evaluators have converged.
- Policy generation, server evaluator, document/app, Service Worker, local schema and physical-iPad runtime/trust epochs remain separate state.
- Long-offline PWA convergence is forward-only for server authority: preserve local data, revalidate queued mutations, and never reactivate legacy server policy merely for compatibility.

## Persistent guards added by 151
`same account ≠ same rollout cohort everywhere`.  
`same cohort ≠ same policy observed by every evaluator at the same instant`.  
`request A permitted under G1 + request B permitted under G2 ≠ transaction permitted`.  
`idempotency key reused ≠ authorization may be re-evaluated under arbitrary generation`.  
`retry under newer policy ≠ new user intent`.  
`provider update acknowledged ≠ all authorization replicas converged`.  
`Service Worker updated ≠ document/runtime/policy generation converged`.  
`legacy client supported ≠ legacy policy still authoritative`.  
`client reports generation ≠ server trusts generation`.  
`compatibility bridge ≠ downgrade channel`.  
`pinned generation ≠ immortal authority`.  
`offline queue created under G1 ≠ remote execution authorized under G1 forever`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; owns exact document/SW/storage/browser generation and activation/control mechanics, not authorization generation.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful local-saved/sync-gated/revalidation/restart/manual-recovery states without implying data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns policy-propagation, multi-step transaction, retry/ACK-loss, multi-device split-cohort and stale-runtime fault injection.
- **D Search/Discovery/Analytics:** constrained supporting consumer; may aggregate privacy-aware cohort/generation diagnostics but cannot assign cohort, clear gates or prove convergence from missing telemetry.
- **E Architecture/Security/Operations:** highest-risk owner; 151 closes generic cohort authority, cross-generation transaction semantics, provider-consistency boundary and split-policy convergence judgment.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W100 SERVED ERROR-PREVENTION TRANSACTION PROVENANCE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, non-drag reorder/I087 runtime, persisted configuration, screen-reader, physical-device/input, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, account/device identity, trust-floor storage, reset/rebootstrap authority, server-side idempotency, approval/succession workflow, runtime authority inventory, evidence/exception/dependency graph, event retention/reconciliation, monitoring SLOs, policy engine/composition/precedence, recovery bootstrap, policy-generation rollout/shadow evaluation/cohort assignment, cross-generation transaction semantics, provider consistency, backup/restore and managed-device integration remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API/policy versions; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; conflict/merge/correction policy; provenance/integrity/compaction/export/import; checkpoint/crypto/key/trust hierarchy; compromise/revocation/recovery; trust-floor/reset/succession/inventory/drills; evidence freshness/exception/dependency graph; event source/retention/cursor/reconciliation; monitoring lag/gap objectives; consequence classes; warning/hard gates; capability taxonomy; policy-combination semantics and precedence; prerequisite/recovery graph; independent bootstrap/recovery plane; policy-generation transition/rollback; shadow/diff coverage; rollout cohort integrity; cross-generation transaction boundaries; in-flight policy leases; provider propagation/consistency; Service Worker trust; actual RTO/RPO/MTD; and real physical-device/security/privacy/legal validation.

## Next learning mode
Highest-value adjacent generic work is **PWA policy-generation retirement, in-flight lease bounding & compatibility-horizon governance**: decide when predecessor authority can be retired after split rollout, how long in-flight transactions may legitimately remain bound to an older generation, how emergency revocation overrides those leases, and how long-offline PWA support horizons can expire without either deleting local data or preserving indefinite downgrade authority.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–151 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/backup/compromise/recovery/evidence/event/SLO/gating/policy-runtime validation remains OPEN.
- Reporting remains coarse/checkpoint-based.