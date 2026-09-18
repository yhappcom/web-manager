# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-19

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts.

## Continuous expert maintenance
083–138 — **PASS at recorded generic gates.**  
139 PWA Compromise-Era Trust-Policy Distribution & Offline Re-entry Authenticity — **PASS (generic) / PRODUCT + MANAGED-IPAD + TRUST-METADATA + RECOVERY-PATH + PHYSICAL-DEVICE VALIDATION OPEN**.

## 139 checkpoint
- Re-entry is not `fetch latest and trust it`: authenticate successor trust, enforce a monotonic minimum accepted trust/policy floor, verify coherent policy state, then restore remote authority.
- Current TUF v1.0.36 is used as transfer evidence for rollback/freeze/mix-and-match/key-compromise defenses, not as a MintTap implementation mandate.
- Policy authenticity, freshness, monotonicity and cross-object consistency are separate claims.
- A compromised root/authority cannot safely be the sole authority for its successor; threshold-root compromise requires sufficiently independent rebootstrap for the declared threat model.
- Service Worker and Cache Storage are runtime/transport state, not trust-freshness oracles. Updating a worker does not automatically update author-managed caches.
- Loss/restoration of browser-local trust-floor state must not silently become epoch zero. Missing prior floor means `UNKNOWN/REENTRY-REQUIRED` until independently authenticated bootstrap succeeds.
- Preserve irreplaceable local data/read/export while consequence-bearing remote mutation remains blocked if current trust cannot be established.
- Policy publication needs a coherent snapshot/receipt boundary; individually authentic root/revocation/compatibility objects can still form an invalid mix-and-match state.

## Persistent guards added by 139
`HTTPS fetch succeeded ≠ trust policy is current`.  
`policy signature valid ≠ policy is fresh`.  
`fresh-looking timestamp ≠ trusted monotonic progress`.  
`newer version number ≠ legitimate successor`.  
`all files individually valid ≠ files belong to one legitimate policy snapshot`.  
`old root signs new root ≠ safe recovery after threshold compromise`.  
`new Service Worker fetched from origin ≠ compromise-era trust reset proven`.  
`local state restored ≠ trust floor may roll back`.  
`app reinstalled ≠ compromise history erased`.  
`not expired according to device clock ≠ globally fresh`.  
`cannot update trust policy ≠ accept old policy`.  
`availability pressure ≠ rollback authorization`.  
`Service Worker current ≠ cached trust policy current`.  
`cache cleared ≠ trusted floor safely reset`.  
`recovery package authentic ≠ recovery package current`.  
`no local floor found ≠ floor was zero`.  
`same account login ≠ same prior device trust state recovered`.  
`objects individually authentic ≠ combined state authorized`.  
`100% of observed online clients updated ≠ 100% of fleet updated`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; Service Worker update/control, Cache Storage and long-offline lifecycle constrain re-entry but do not establish trust freshness.
- **B UX/IA/Content:** elevated dependency pressure; owns truthful local-preserved, trust-update-required, sync-blocked, re-entry-failed and affected-record-review states.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns rollback/freeze/mix-and-match, stale cache/worker, reinstall/restore, clock and physical-device destructive matrices.
- **D Search/Discovery/Analytics:** constrained supporting consumer; observed generation/adoption telemetry cannot authenticate client trust state or establish fleet completeness.
- **E Architecture/Security/Operations:** highest-risk owner; 139 closes generic successor-policy distribution, monotonic floor and offline re-entry authenticity boundaries.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W089 KEYBOARD-LAYOUT SHORTCUT SERVED-RUNTIME CLOSURE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/layout/IME, field-CWV, full-WCAG and human UX evidence remain OPEN.

Software Engineering Data `progress/DATA_STATUS.md` is **Stage 1 IN STUDY / NOT YET PASSED**. D005/D006 supply bounded durability/sync/cursor evidence; actual LogMate persistence/Sync, Flutter/mobile transfer, key storage, trust-policy publication and re-entry implementation remain OPEN.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence. This includes managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; authentication/session/offline authorization; local authoritative data; actual schema/operation/API versions; validation/authorization/conflict-policy epochs; compatibility horizon; allowed offline edits/deletes; record/operation/device identity; base/server revision model; conflict/merge/correction policy; provenance schema/integrity/transaction scope; compaction policy; export/import/package format; lineage topology; checkpoint/range/parent model; canonicalization; encryption/signature/MAC algorithms; key/trust-root hierarchy and custody; verifier topology and historical retention; algorithm/key/verifier transition format; compromise detection source and earliest plausible compromise; revocation/containment semantics; successor/recovery authority and independence; trust-policy metadata/snapshot format; minimum accepted trust-floor persistence; reset/rebootstrap authorization; timestamp/anchor/witness evidence; browser file/share APIs; backup destination; operation receipt/dedup semantics; rejected-operation retention; tombstone semantics; privacy/legal/aviation/investment retention; audit access; analytics/logging separation; inbound cursor/batch atomicity; backup/restore; Service Worker trust; fleet denominator; API-generation enforcement; actual RTO/RPO/MTD; safety/legal constraints; and real migration/reconciliation/export/import/fork/crypto-transition/compromise/re-entry drills.

## Next learning mode
Highest-value adjacent generic work is **PWA trust-floor persistence, reset authorization & device-loss recovery without rollback loopholes**: determine how to recover when local monotonic trust state is deleted, evicted, restored from an old backup or absent on a replacement device without treating loss of state as permission to downgrade. Integrate independent reset authority, browser-storage limitations, recovery packages, account/device identity boundaries and physical-device validation.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–139 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/provider/data-model/backend/crypto/anchor/backup/compromise/re-entry validation remains OPEN.
- Reporting remains coarse/checkpoint-based.