# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–140 — **PASS at recorded generic gates.**  
141 PWA Recovery-Authority Abuse Resistance, Quorum & Emergency Reset Governance — **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + RESET-IMPLEMENTATION + INCIDENT-DRILL VALIDATION OPEN**.

## 141 checkpoint
- Recovery authority is itself an attack surface; a universal reset credential can nullify earlier anti-rollback controls.
- Least privilege, separation of duties, MFA and quorum are distinct controls. Two approvals are useful only when independent enough for the relevant compromise model.
- No universal two-person rule is imposed. Threshold/independence scales with consequence; a small company should use minimal sufficient independence rather than enterprise ceremony.
- Recovery authorization binds exact subject, lineage/device/account, permitted effect, policy/authority generation, expiry/consumption and resulting state.
- Recovery execution is server-authoritative and idempotent; retry/ACK ambiguity must not produce duplicate or broader resets.
- Break-glass is bounded emergency authority, not permanent super-admin power. Activation, use, expiry/revocation and post-emergency normalization are separate lifecycle gates.
- Recovery operators should not receive arbitrary `setTrustEpoch(any)` power; prefer bounded current-safe rebootstrap semantics.
- Recovery provenance/audit is distinct from analytics and should survive operator abuse strongly enough for the threat model without copying unnecessary user payload.
- Offline PWA/EFB clients preserve local data but cannot approve a server trust-floor reset from stale Service Worker/cache/UI state.

## Persistent guards added by 141
`authenticated administrator ≠ authorized reset`.  
`admin role ≠ recovery role ≠ audit role`.  
`two named approvers ≠ independent approval`.  
`different accounts ≠ different failure domains`.  
`quorum count high ≠ quorum independent`.  
`MFA on one admin ≠ separation of duties`.  
`approval valid ≠ approval valid for this subject/effect`.  
`retry ≠ new recovery intent`.  
`ACK missing ≠ recovery not applied`.  
`client says approved ≠ server authorization state approved`.  
`break-glass exists ≠ break-glass always enabled`.  
`emergency bypasses normal workflow ≠ emergency bypasses all policy`.  
`service restored ≠ emergency authority retired`.  
`separate email addresses ≠ independent channels`.  
`can recover availability ≠ can select historical security state`.  
`recovery authority ≠ root-signing authority`.  
`recovery logged ≠ log independently trustworthy`.  
`analytics event emitted ≠ recovery provenance durable`.  
`offline user confirmed reset ≠ server recovery authorized`.  
`local data preserved ≠ remote mutation authorized`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; browser/PWA state can preserve request/context but cannot establish organizational quorum or server recovery authority.
- **B UX/IA/Content:** elevated dependency pressure; owns pending-approval, expired/revoked, emergency-limited, normalization-pending and local-preserved states.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns single-channel compromise, replay, duplicate/ACK, approver-loss, stale-policy, restart and physical-device destructive matrices.
- **D Search/Discovery/Analytics:** constrained supporting consumer; recovery telemetry cannot prove authorization legitimacy, approval independence or fleet completeness.
- **E Architecture/Security/Operations:** highest-risk owner; 141 closes generic recovery-authority abuse, consequence-scaled quorum/independence, break-glass and emergency lifecycle boundaries.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W091 SERVED POINTER-CANCELLATION CLOSURE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/input, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, account/device identity, trust-floor storage, reset/rebootstrap authority, server-side idempotency, approval workflow, backup/restore and managed-device integration remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; base/server revision model; conflict/merge/correction policy; provenance schema/integrity/transaction scope; compaction policy; export/import/package format; lineage topology; checkpoint/range/parent model; canonicalization; encryption/signature/MAC algorithms; key/trust-root hierarchy and custody; verifier topology and historical retention; algorithm/key/verifier transition format; compromise detection source and earliest plausible compromise; revocation/containment semantics; successor/recovery authority and independence; trust-policy metadata/snapshot format; minimum accepted trust-floor fields/storage/persistence; reset/rebootstrap authorization and abuse controls; recovery request/approval/execution model; approver identities and independence; break-glass credential/channel/custody; emergency expiry/normalization; first-bootstrap vs replacement-device classification; lost-device revocation; timestamp/anchor/witness evidence; browser file/share APIs; backup destination and rollback semantics; operation receipt/dedup semantics; rejected-operation retention; tombstone semantics; privacy/legal/aviation/investment retention; audit access; analytics/logging separation; inbound cursor/batch atomicity; backup/restore; Service Worker trust; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; safety/legal constraints; and real migration/reconciliation/export/import/fork/crypto-transition/compromise/re-entry/reset/device-loss/emergency drills.

## Next learning mode
Highest-value adjacent generic work is **PWA recovery-authority continuity under organizational loss, credential unavailability & succession governance**: verify that abuse-resistant recovery still works when an owner/approver leaves or is unavailable, an identity provider fails, emergency credentials age out, or company custody changes—without weakening quorum ad hoc or creating a permanent master-key loophole. Reconcile with study 126 rather than duplicating organizational-loss foundations.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–141 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/anchor/backup/compromise/re-entry/reset/recovery-authority validation remains OPEN.
- Reporting remains coarse/checkpoint-based.