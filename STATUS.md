# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–139 — **PASS at recorded generic gates.**  
140 PWA Trust-Floor Persistence, Reset Authorization & Device-Loss Recovery — **PASS (generic) / PRODUCT + MANAGED-IPAD + ACCOUNT/DEVICE + RESET-AUTHORITY + PHYSICAL-DEVICE VALIDATION OPEN**.

## 140 checkpoint
- Loss of local monotonic state is evidence loss, not rollback authorization. Missing state must not silently become epoch zero.
- WHATWG persistent storage and WebKit persistent mode reduce user-agent eviction risk; they are not immutable device-lifetime anti-rollback roots.
- First bootstrap, known-account/new-device, known-device/floor-missing, backup restore and device-loss/replacement are distinct recovery cases.
- Reset/rebootstrap is a high-consequence authorization event. It needs evidence independent enough from the failure/compromise that caused floor loss.
- Account authentication, device lineage, trust-floor recovery, data restoration and remote mutation authorization remain separate claims.
- A restored backup may preserve irreplaceable records while carrying stale trust metadata; data admission and authority restoration therefore use separate paths.
- Prefer recovery authority that establishes a bounded current-safe state rather than arbitrary permission to select an old epoch.
- Floor acceptance must become durable before remote authority is reported restored; partial persistence/restart ambiguity requires re-verification.
- Preserve local read/export and provenance when rebootstrap fails; do not trade irreplaceable data for silent downgrade.

## Persistent guards added by 140
`persisted() == true ≠ trust floor cannot be deleted`.  
`Home Screen PWA storage ≠ hardware monotonic storage`.  
`eviction-resistant ≠ rollback-resistant`.  
`trusted metadata missing ≠ first install proven`.  
`fresh installation bits ≠ fresh trust bootstrap`.  
`local state missing ≠ reset authorized`.  
`user can delete site data ≠ user intended security downgrade`.  
`same account authenticated ≠ old device floor reconstructed`.  
`reset authority exists ≠ arbitrary rollback authority exists`.  
`same user ≠ same device`.  
`backup restored ≠ security state current`.  
`replacement device trusted ≠ lost device revoked`.  
`account recovery PASS ≠ trust-floor recovery PASS`.  
`trust-floor recovery PASS ≠ account authorization PASS`.  
`backup authentic ≠ backup current`.  
`restore completed ≠ remote authority restored`.  
`candidate verified ≠ floor durable`.  
`floor durable ≠ policy effects complete`.  
`trust state unrecoverable now ≠ local data disposable`.  
`new installation event ≠ first-ever bootstrap`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; browser persistence/eviction/storage isolation constrain floor retention but do not provide immutable rollback protection.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful local-preserved, previous-state-unavailable, re-verification-required, restore-blocked and replacement-device states.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns eviction/delete/reinstall/backup/new-device/interrupted-reset and physical-device destructive matrices.
- **D Search/Discovery/Analytics:** constrained supporting consumer; recovery telemetry cannot reconstruct missing trust state, authenticate reset authority or prove fleet completeness.
- **E Architecture/Security/Operations:** highest-risk owner; 140 closes generic trust-floor loss, reset authorization, backup/device-loss and rebootstrap boundaries.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W090 SERVED POINTER-REORDER TRANSFER CLOSURE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/input, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, account/device identity, trust-floor storage, reset/rebootstrap authority, backup/restore and managed-device integration remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; base/server revision model; conflict/merge/correction policy; provenance schema/integrity/transaction scope; compaction policy; export/import/package format; lineage topology; checkpoint/range/parent model; canonicalization; encryption/signature/MAC algorithms; key/trust-root hierarchy and custody; verifier topology and historical retention; algorithm/key/verifier transition format; compromise detection source and earliest plausible compromise; revocation/containment semantics; successor/recovery authority and independence; trust-policy metadata/snapshot format; minimum accepted trust-floor fields/storage/persistence; reset/rebootstrap authorization and abuse controls; first-bootstrap vs replacement-device classification; lost-device revocation; timestamp/anchor/witness evidence; browser file/share APIs; backup destination and rollback semantics; operation receipt/dedup semantics; rejected-operation retention; tombstone semantics; privacy/legal/aviation/investment retention; audit access; analytics/logging separation; inbound cursor/batch atomicity; backup/restore; Service Worker trust; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; safety/legal constraints; and real migration/reconciliation/export/import/fork/crypto-transition/compromise/re-entry/reset/device-loss drills.

## Next learning mode
Highest-value adjacent generic work is **PWA recovery-authority abuse resistance, quorum/independence & emergency reset governance**: once reset is a high-consequence authority, determine how to prevent a single compromised support/admin/account channel from abusing it; integrate separation of duties, threshold/quorum where consequence warrants it, break-glass constraints, replay/idempotency, recovery-event provenance and emergency lifecycle without imposing unnecessary enterprise ceremony on a small app company.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–140 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/anchor/backup/compromise/re-entry/reset validation remains OPEN.
- Reporting remains coarse/checkpoint-based.