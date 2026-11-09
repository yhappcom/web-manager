# Stage 8 — accessible PWA recovery and owner-custody trust
Date: 2026-11-10 KST. Evidence class: SOURCE + SYNTHESIS + proposed VALIDATION; **no LogMate runtime/device PASS**. Stage 8 ACTIVE / production OPEN / PWA release HOLD.

**Owner:** C owns accessibility and quality test oracles; E owns identity, deletion, storage and backup security; A owns browser and service-worker mechanics; B owns recovery journeys and copy; D owns consent-safe measurement and truthful public claims. Coordinator is not a sixth track. This cross-track application complements [PWA Architecture Master](PWA_ARCHITECTURE_MASTER.md), [Evidence Register](EVIDENCE_VALIDATION_REGISTER.md), [Product Application](MINTTAP_PRODUCT_APPLICATION.md), [research 529](../529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) and [research 530](../530_stage8_pwa_install_identity_origin_migration_efb_custody_20261030.md), rather than rewriting their foundations.

## SOURCE and historical problem
Service workers make an offline shell possible, not an atomic guarantee of accessible task completion, durable local storage, current owner authority, independent backup or remote Sync. A user can see a functioning form while network, IDB quota, worker activation, session or deletion authorization is failing. Accessible recovery is a data-safety requirement when unsynced flight records exist.

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) provides 2.1.1 Keyboard, 2.4.3 Focus Order, 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured (Minimum), 3.3.1 Error Identification, 3.3.3 Error Suggestion, 4.1.3 Status Messages and 2.2.1 Timing Adjustable. [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) gives patterns, not automatic conformance; [ARIA22 status technique](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22) addresses announcements without moving focus. [MDN Navigator.onLine](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine) cautions that connection indication is unreliable as reachability proof. [MDN controller](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controller) distinguishes controlled clients from registered workers; [MDN persistence](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist) does not certify independent backup. Browser/OS behavior is CHANGE WATCH.

## SYNTHESIS: six distinct evidence and message states
| State | Permitted user-facing statement | Prohibited inference |
| --- | --- | --- |
| Input captured | Editing is in progress | Saved to IndexedDB |
| Local transaction committed | Saved on this device/container | Independent Files or cloud backup |
| Export generated | Export prepared | File saved in Files and reopened |
| Independent Files readback | Backup file verified by readback | Fresh-container restoration works |
| Remote receipt verified | Specific records accepted remotely | All pending records synchronized |
| Fresh-container restore verified | Tested restore of specified version and owner | Future eviction/MDM changes harmless |

**CONTRADICTION:** “offline ready” from icon installation, cached HTML or worker registration conflicts with separate shell-completeness, ledger and owner-custody evidence. “Synced” from an online indicator or queued request conflicts with actual server receipt. “Backup complete” from a generated blob conflicts with independent file custody.

## E-owned security invariants
E1: Retry, refresh, history restore and accessibility shortcuts must not bypass owner/epoch/deletion admission. E2: A deleted owner’s old tab must not regain write access through a focus return, bfcache or pending update. E3: Recovery instructions must not casually recommend Clear-Site-Data or deleting browser data when unsynced records lack verified independent custody. E4: Screen-reader announcements, logs and analytics must not expose action-link tokens, backup secrets or another owner's data. E5: Worker reload/update must not discard unsaved edits or silently cross incompatible schema. E6: Offline account deletion instructions must never claim remote deletion succeeded. These are requirements, not observed LogMate defects.

## B task states, C accessibility oracles and A platform dependencies
| Failure case | Recovery UX and accessible oracle | Required safety evidence |
| --- | --- | --- |
| First-install offline cache incomplete | Text status, actionable keyboard/VoiceOver retry, no false ready state | Worker control and complete shell inventory |
| Network loss during edit | One status update; keep focus and input; distinguish local save vs pending sync | IDB commit and outbox independently measured |
| Quota/transaction failure | Specific failure and non-destructive next step; no success toast | Negative local-commit oracle, no destructive purge |
| Waiting V2 with V1 editor | Defer update safely; cancel and resume; focus not trapped | No unsaved state loss, schema compatibility |
| Restored A tab after A deletion/B login | Revalidate before privileged action; accessible denial | A write blocked at transaction boundary |
| Session expires offline | Explain network-required sign-in vs locally available records | No fabricated server-auth renewal |
| Files export or restore failure | Separate generated/saved/readback/restore states; actionable error | Fresh-container owner/schema/record checks |
| iPad rotation/split view/200% text | Controls and focus remain visible; VoiceOver and keyboard usable | No orientation-driven mutation |
| Public deletion/support route offline | Cached help distinguished from remote action | No claimed deletion receipt |
| Repeated network flaps | Rate-limit announcements; preserve current task focus | Sync receipt verified by owner and epoch |

**TRANSFER VALIDATION:** Design Studio [WEB_STATUS](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) owns focus visuals and interaction design; Web Manager owns runtime/task acceptance. Marketing owns acquisition strategy and must not promote offline/sync/backup capability without actual product acceptance. No Design Studio gate was independently validated here.

## VALIDATION RA01–RA20: DEFINED NOT RUN
Use disposable A/B synthetic records, exact pinned NORMAL served build, separate acceptance build when needed, worker V1/V2, and authorized physical managed iPad. Preserve worker controller, cache catalogue, IDB transaction, focus trace, accessibility tree, VoiceOver output, network/console errors, owner/epoch, remote receipts and independently reopened Files hashes. Never run destructive tests on operational EFB.

RA01 online install; RA02 first cold offline launch; RA03 interrupted precache; RA04 waiting worker with active editor; RA05 update deferral with unsaved edits; RA06 quota failure before commit; RA07 optimistic success before failed transaction; RA08 reconnect flap; RA09 remote receipt failure; RA10 expired session; RA11 deleted A owner in background tab; RA12 A bfcache restoration after B sign-in; RA13 denied retry-save; RA14 Files save failure; RA15 generated export without readback; RA16 fresh-container wrong-owner/wrong-schema restore; RA17 Safari tab vs Home Screen vs permitted managed Web Clip; RA18 split-view, rotation, 200% text and keyboard; RA19 VoiceOver focus/order/error recovery walkthrough; RA20 sensitive sentinel absence from announcements, URLs, referrers and telemetry. Report **NOT RUN / BLOCKED / mechanism-only / exact product PASS / exact product FAIL** separately.

## MINTTAP DECISION / OPEN / DEPENDENCY / CHANGE WATCH
**Proposed requirement only:** accessible, independently truthful status for local save, pending Sync, remote receipt, backup, offline shell, authentication and deletion; non-destructive recovery and user-controlled safe update. Do not assume background sync, Files permissions, direct peer transfer or managed Web Clip support. **OPEN:** actual LogMate UI/VoiceOver, served worker, 37-store deletion parity, old-writer denial, Files custody and MDM permission. **DEPENDENCY:** Engineering source/runtime and authorized device; Design Studio focus specification; owner-approved release truth. **CHANGE WATCH:** WCAG guidance, WebKit installed-container behavior, Chrome lifecycle, MDM restrictions. **Gate remains Stage 8 ACTIVE / production OPEN / PWA HOLD.**
