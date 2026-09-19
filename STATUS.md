# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–148 — **PASS at recorded generic gates.**  
149 PWA Assurance Policy Composition, Conflicting Gates & Degraded-Mode Deadlock Avoidance — **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + POLICY-RUNTIME VALIDATION OPEN**.

## 149 checkpoint
- Assurance requirements compose per protected capability through typed mandatory prerequisites; independent subsystems do not race to set one global `allowed` boolean.
- Authority-critical `UNKNOWN/INDETERMINATE` is non-permissive, but unrelated diagnostic degradation does not become a whole-app outage.
- Within a policy generation, ordinary degraded transitions are monotonic toward equal/narrower authority; authority can increase only through recognized fresh evidence, reconciliation, approved recovery, policy transition or bounded emergency authorization.
- Policy precedence is semantic and explicit. A weaker fallback cannot silently erase containment/revocation/trust restrictions; exceptions are bounded typed authorizations rather than global overrides.
- Prerequisite graphs are checked for circular recovery dependencies. A strongly connected blocked set requires an independently authorized bootstrap/recovery entry edge or must stop at explicit manual recovery rather than dropping a prerequisite ad hoc.
- PWA/Service Worker local state remains separate from server-side remote-mutation authority. Local read/export/data preservation can remain available while remote sync/recovery authority is gated.
- Policy-composition semantics are versioned security state; candidate generation, evidence applicability, exception migration, rollback and offline-device compatibility require explicit transition semantics.

## Persistent guards added by 149
`one policy permits ≠ capability permitted`.  
`one policy restricts capability X ≠ whole app unavailable`.  
`weaker fallback policy ≠ override of stronger mandatory gate`.  
`UNKNOWN ≠ PERMIT` for authority-critical decisions.  
`policy evaluation order ≠ policy precedence`.  
`UI enabled ≠ server authority granted`.  
`offline local capability ≠ remote mutation authority`.  
`recovery path exists ≠ normal gate bypassed`.  
`break-glass authorized ≠ all controls disabled`.  
`cycle detected ≠ safe to drop one prerequisite`.  
`network online ≠ prerequisite graph resolved`.  
`Service Worker activated ≠ recovery authority current`.  
`new policy deployed ≠ old device evaluated under new policy`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; owns exact observable SW/browser/WebKit/storage/runtime generation semantics and supplies facts without defining authorization precedence.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful LOCAL-AVAILABLE / SYNC-GATED / REVALIDATION / RECOVERY-ONLY / MANUAL-RECOVERY states without implying data loss or false security certainty.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns policy-composition/cycle fixtures, fault injection, generation-transition tests and accessible recovery/degraded-state evidence.
- **D Search/Discovery/Analytics:** constrained supporting consumer; may diagnose gate frequency/recovery duration but cannot clear gates or serve as authorization oracle.
- **E Architecture/Security/Operations:** highest-risk owner; 149 closes generic policy-composition, precedence and deadlock-avoidance judgment.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W098 SERVED UNSAVED-EXIT + LIFECYCLE TRANSFER; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, non-drag reorder/exit-lifecycle runtime, persisted configuration, screen-reader, physical-device/input, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, account/device identity, trust-floor storage, reset/rebootstrap authority, server-side idempotency, approval/succession workflow, runtime authority inventory, evidence/exception/dependency graph, event retention/reconciliation, monitoring SLOs, policy engine/composition/precedence, recovery bootstrap, policy-generation rollout, backup/restore and managed-device integration remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API/policy versions; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; conflict/merge/correction policy; provenance/integrity/compaction/export/import; checkpoint/crypto/key/trust hierarchy; compromise/revocation/recovery; trust-floor/reset/succession/inventory/drills; evidence freshness/exception/dependency graph; event source/retention/cursor/reconciliation; monitoring lag/gap objectives; consequence classes; warning/hard gates; capability taxonomy; policy-combination semantics and precedence; prerequisite/recovery graph; independent bootstrap/recovery plane; policy-generation transition/rollback; Service Worker trust; actual RTO/RPO/MTD; and real physical-device/security/privacy/legal validation.

## Next learning mode
Highest-value adjacent generic work is **PWA policy-graph rollout safety, shadow evaluation & decision-diff validation**: determine how a candidate policy generation can be evaluated against representative/current decision contexts without making shadow output authoritative, detect dangerous permit expansion and recovery-path regressions, and roll out/rollback policy semantics while stale offline clients and observability gaps remain explicit.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–149 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/backup/compromise/recovery/evidence/event/SLO/gating/policy-runtime validation remains OPEN.
- Reporting remains coarse/checkpoint-based.