# 253 — PWA Convergence-Debt Expiry, Device-Retirement Authority & Stale-Tail Resurrection Resistance

Status: **PASS (generic) / PRODUCT + MDM + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/storage/Service Worker mechanics; Track B retirement/rejoin UX; Track C destructive retirement/resurrection validation; Track D fleet denominator/debt measurement.  
Dependencies: 137, 171–252, especially anti-rollback, device/fleet currentness, recovery bootstrap, policy distribution, consumer checkpoints and partial-fleet convergence debt.

## Problem
252 made partial-fleet convergence an explicit assurance state rather than treating active-online clients as the whole fleet. The next question is when a stale/offline device may legitimately leave the convergence denominator, who has authority to retire it, and what happens if a supposedly retired device later reappears carrying unique local data plus obsolete policy/checkpoint state.

Central rule: **silence is not retirement, inventory disappearance is not destruction, and retirement is not proof that a device can never return. A consequence-bearing fleet needs explicit retirement authority and evidence; a returning retired device is treated as a new rejoin/recovery event whose unique data is preserved while its old authority remains retired.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Explains browser storage, cached Service Worker/app-shell persistence, local data survival and reset/reinstall boundaries. These mechanics do not decide organizational retirement.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `DEVICE-RETIRED`, `REJOIN-REQUIRED`, `AUTHORITY-RETIRED`, `DATA-RECOVERY-PENDING`, and `RESURRECTED-STALE-TAIL` states without destructive reset or false “all synced” messaging.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns lost/offline/retired/reappearing-device sequences. Campaign expands **776 → 784 defined cases**; defined cases are not execution PASS.
- **D Search/Discovery/Analytics:** bounded consumer. Measures active/stale/unknown/retired/resurrected populations with explicit denominator transitions and reason codes; telemetry cannot authorize retirement.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns retirement authority, revocation/containment, evidence, convergence-debt expiry, resurrection handling and closure.

## SOURCE

### NIST SP 800-124 Rev. 2 — mobile-device lifecycle includes disposal
NIST SP 800-124 Rev. 2 (May 2023) provides enterprise guidance for deployment, use and disposal of mobile devices across the mobile-device lifecycle, including centralized device management.

Sources:
- https://csrc.nist.gov/pubs/sp/800/124/r2/final
- https://www.nist.gov/news-events/news/2023/05/guidelines-managing-security-mobile-devices-enterprise-nist-publishes-sp

**TRANSFER VALIDATION:** this establishes lifecycle/disposal as a managed security concern; it does not prescribe MintTap/LogMate retirement protocol or prove a specific device was disposed.

### Apple Business — release is an administrative lifecycle action, not disappearance
Current Apple Business documentation says devices may be released when sold, lost or irreparable; released devices remain visible in the device listing, cannot be assigned to a device-management service, and should be erased/restored. Apple also documents who or what service released a device and the release date. A released device can later be added back through supported enrollment paths.

Source:
- https://support.apple.com/en-ca/guide/business/axmec4d28461/1/web/1

**TRANSFER VALIDATION:** this is strong current Apple-platform evidence that managed-device retirement/release is an explicit administrative lifecycle event with provenance, and that reappearance/re-enrollment is possible. It is not evidence that LogMate currently uses Apple Business Manager or any specific MDM.

### Apple Managed Lost Mode / remote wipe — lost, locked and erased are distinct states
Apple documents Managed Lost Mode for supervised iPhone/iPad and remote wipe as separate device-management actions. A wipe command is acknowledged and then performed when the device can receive it; therefore “wipe requested” and “wipe completed/acknowledged” must not be conflated.

Sources:
- https://support.apple.com/en-ca/guide/security/secc46f3562c/web
- https://support.apple.com/en-au/guide/deployment/depb980a0be4/web

**TRANSFER VALIDATION:** platform-specific evidence only. It supports explicit state/evidence separation, not a generic guarantee that every MDM/provider exposes equivalent acknowledgement semantics.

### Apple Return to Service — reset/re-enrollment can be an explicit transition
Apple documents Return to Service as an erase followed by automated re-enrollment/configuration for supported managed devices. This reinforces that erasure, organizational assignment, enrollment and operational readiness are separate lifecycle steps.

Source:
- https://support.apple.com/en-eg/guide/deployment/dep17cb455a0/web

**CHANGE WATCH:** Apple platform versions, MDM commands and enrollment behavior are platform/provider-specific and must be rechecked for the actual managed-iPad environment.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**; physical-device/PWA, screen-reader and representative-human evidence remain OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**. Exact-fixture macOS Safari Service Worker registration→control→V1→V2 update/controller replacement→fresh-WebDriver V2 control recovery is bounded PASS, while installed-PWA/ordinary-profile persistence, physical iOS/iPadOS/EFB and canonical-product runtime remain OPEN.

**DEPENDENCY:** generic retirement/rejoin reasoning cannot upgrade those runtime/design gates.

## SYNTHESIS 1 — fleet membership is governed state, not a telemetry side effect
A device leaving telemetry does not establish that it has been sold, destroyed, wiped, de-authorized or removed from organizational control. Offline travel, power loss, network isolation, broken MDM enrollment, app uninstall and telemetry failure can all produce silence.

Guards: `telemetry silence ≠ retirement`; `last seen expired ≠ device destroyed`; `MDM unreachable ≠ device no longer exists`.

## SYNTHESIS 2 — retirement authority must be explicit
For consequence-bearing fleet accounting, retirement should be an authorized lifecycle decision bound to device identity and reason, not an analytics cleanup rule. Record at least:
1. stable device/installation identity sufficient for the relevant system;
2. retirement reason/class;
3. authorizing actor/control plane and governance generation;
4. effective time/generation;
5. expected authority revocation/containment actions;
6. data/evidence disposition expectation;
7. whether physical custody/destruction/wipe is known, requested, acknowledged or unknown;
8. resurrection/rejoin rule.

Guard: `inventory row deleted ≠ device retired`.

## SYNTHESIS 3 — denominator exit and authority retirement are related but not identical
A device may leave a rollout denominator because it is formally retired from the managed population, yet old credentials/tokens/cached policy may still exist until revoked/expired/contained. Conversely, authority may be revoked immediately while unique local data still requires later recovery.

Therefore model at least:
- fleet-membership state;
- authority state;
- custody/disposal state;
- unique-data recovery state;
- policy/checkpoint generation.

Guard: `retired from fleet ≠ all authority cryptographically gone`; `authority revoked ≠ local data erased`.

## SYNTHESIS 4 — debt expiry requires disposition, not elapsed time
Convergence debt cannot auto-close because a device has been offline for 30/90/365 days. A time threshold may trigger review/escalation, but closure requires an authorized disposition such as verified rejoin/convergence, formal retirement with containment, or another explicitly governed outcome.

Guards: `debt age exceeded ≠ debt closed`; `SLA expired ≠ stale tail harmless`.

## SYNTHESIS 5 — lost-device handling preserves uncertainty
A lost device may be placed into a contained/lost state before physical disposition is known. If remote wipe is requested but no completion evidence exists, record `WIPE-REQUESTED/UNCONFIRMED`, not `ERASED`. If policy permits denominator retirement while physical state remains unknown, the residual authority/data risk remains separately visible.

Guards: `wipe command sent ≠ wipe completed`; `lost ≠ destroyed`; `released from management ≠ sanitized`.

## SYNTHESIS 6 — administrative release is not data-destruction evidence
Apple Business explicitly separates release from the organization and erase/restore. Generalize the distinction: removing a device from MDM/inventory or releasing ownership control cannot be used as evidence that browser storage, IndexedDB, Cache Storage, Service Worker state, credentials or unique local records were erased.

Guard: `management release ≠ storage sanitization`.

## SYNTHESIS 7 — a retired device can legitimately reappear
Apple documents supported ways to add a released device back. More generally, a lost device may be recovered or an offline device may reconnect after administrative retirement. The system must therefore resist **stale-tail resurrection**: old policy/checkpoint/credential state cannot regain current authority merely because the physical device is again present.

Guard: `device returned ≠ authority restored`.

## SYNTHESIS 8 — resurrection is a recovery/rejoin event, not rollback
A returning retired device enters `RESURRECTED-STALE-TAIL` / `REJOIN-REQUIRED`. Preserve unique data and historical evidence first. Establish current organizational/device authority through a current bootstrap path; check retirement/revocation history and policy lineage; migrate data/schema as required; then re-admit queued operations individually under current policy.

Do not reactivate the retired credential merely to make sync easier. Do not lower the fleet policy floor to the device's remembered generation.

Guards: `physical possession ≠ current credential validity`; `old device identity recognized ≠ old authority re-enabled`; `successful local unlock ≠ sync authorization`.

## SYNTHESIS 9 — same hardware may be a new administrative incarnation
After erase/re-enrollment/reassignment, the same serial-number hardware may represent a new management enrollment, user assignment, key set, application installation or policy epoch. Preserve hardware identity where operationally necessary, but do not splice old and new authority merely because the serial number matches.

Guard: `same hardware ≠ same administrative incarnation`.

## SYNTHESIS 10 — unique offline data and obsolete authority must be separated
For an EFB/LogMate-like PWA, a returning iPad may contain irreplaceable flight/logbook records created while offline. The safe default is not “wipe because retired” and not “trust because data is valuable.” Preserve/export/recover unique data and provenance while keeping stale authority isolated.

Guard: `data valuable ≠ data automatically trusted`; `authority obsolete ≠ data disposable`.

## SYNTHESIS 11 — retirement records need historical durability
If a retired device later returns, the system needs enough retained retirement/revocation history to know that the old authority was intentionally closed. Deleting the retirement record with the inventory row creates a resurrection vulnerability.

Retain privacy-minimized lineage: device/incarnation identifier, retirement generation/reason, authority disposition, relevant timestamps/approvals and successor/rejoin relation where required. Do not retain unrelated behavioral telemetry merely to prove retirement.

Guard: `asset removed from active inventory ≠ retirement evidence may be deleted`.

## SYNTHESIS 12 — rejoin must not silently rewrite historical retirement
If device D was correctly retired at G20 and later re-enrolled at G25, preserve both facts. Do not mutate the old record to imply uninterrupted active membership. The new incarnation references the historical one through an explicit rejoin/successor relation.

Guard: `re-enrolled now ≠ was never retired`.

## SYNTHESIS 13 — denominator governance needs reason-coded transitions
Track D may report populations such as ACTIVE-CURRENT, ACTIVE-STALE, OFFLINE-UNKNOWN, LOST-CONTAINED, RETIRED, RESURRECTED-REJOIN, and DISPOSED-VERIFIED. Movement out of the active convergence denominator requires a reason-coded authorized transition. Reporting should preserve the excluded-retired count separately rather than making the denominator shrink invisibly.

Guards: `smaller denominator ≠ better convergence`; `100% of remaining active ≠ 100% of historical fleet`.

## SYNTHESIS 14 — retirement authority itself is a security boundary
An attacker who can retire devices can hide stale or compromised endpoints from convergence metrics and possibly trigger destructive workflows. Retirement/release permissions therefore require least privilege, auditability and recovery/contradiction handling appropriate to consequence.

Apple Business documentation explicitly identifies authorized roles/services that can release devices, providing bounded platform precedent for treating release authority as privileged governance.

Guard: `authorized to view inventory ≠ authorized to retire`; `MDM integration present ≠ MDM should have release authority by default`.

## SYNTHESIS 15 — closure requires negative resurrection tests
A retirement control is not proven by showing that an active device disappears from a dashboard. Test that:
- retired credential/policy cannot mutate/sync;
- stale cached Service Worker/app shell cannot restore authority;
- clearing/reinstalling local state cannot bypass retirement history;
- a returning device preserves unique data without regaining obsolete authority;
- re-enrollment creates/links the correct successor incarnation;
- convergence metrics do not silently erase retired/resurrected tails.

Guard: `retirement recorded ≠ resurrection resisted`.

## PWA / LogMate-like EFB application
For a company iPad that may remain offline for long periods:

1. **While active/offline:** preserve local unique flight/logbook data, provenance and last accepted policy/checkpoint; do not infer retirement from missed telemetry.
2. **If lost/unreachable:** contain/revoke what can be contained; distinguish requested actions from acknowledged completion; keep physical/data state UNKNOWN where evidence is absent.
3. **If formally retired:** record authorized retirement and denominator transition; retire current authority according to system design; preserve necessary historical lineage.
4. **If later recovered:** do not wipe first merely to simplify management if unique data may exist. Isolate network mutation, preserve/export evidence/data, establish current bootstrap and retirement history, then evaluate migration/re-admission.
5. **If returned to service for a new user/incarnation:** old unique data recovery and new enrollment are separate workflows. Same hardware does not splice old user/device authority into the new incarnation.
6. **If no unique data exists and sanitization is required:** follow the actual platform/organizational sanitization workflow; generic PWA research does not claim that Apple release/unenrollment alone sanitizes browser/app storage.

**OPEN:** actual LogMate device identity, enrollment/MDM, data ownership, backup/export, offline-auth, key/token, revocation, sanitization and rejoin semantics are unknown until canonical product/runtime evidence exists.

## Track C destructive additions — 776 → 784
Add eight defined cases:
1. **Telemetry-silence retirement laundering:** inactive device auto-removed from denominator with no authorized disposition.
2. **MDM-disappearance = sanitized:** unenrolled/released device treated as erased despite no wipe evidence.
3. **Wipe-request = wipe-complete:** remote command submission closes residual-data risk before acknowledgement/evidence.
4. **Debt-timeout auto-closure:** stale tail disappears after N days without retirement/rejoin evidence.
5. **Retirement-record deletion:** active inventory cleanup also removes revocation/retirement lineage; returned device regains old authority.
6. **Same-serial authority splice:** re-enrolled hardware inherits old credentials/policy because serial number matches.
7. **Resurrection rollback:** recovered iPad's cached policy/checkpoint lowers current fleet floor to permit sync.
8. **Destructive resurrection recovery:** returned retired iPad with unique offline logbook data is wiped before preservation because management state is stale.

**VALIDATION:** these are defined destructive oracles, not executed product tests. Campaign total: **784 defined cases; execution PASS not claimed**.

## MINTTAP DECISION / generic operating direction
- Treat device retirement as an explicit authorized lifecycle transition, not a telemetry timeout.
- Separate fleet membership, authority, custody/sanitization and unique-data recovery state.
- Allow time thresholds to trigger review, never automatic assurance-debt closure.
- Preserve retirement/revocation lineage long enough to resist stale-tail resurrection.
- On reappearance, preserve unique data first and recover current authority independently; never reactivate obsolete authority merely to sync.
- Treat same hardware after re-enrollment as potentially a new administrative incarnation.
- Keep physical managed-iPad/MDM behavior and product-specific retirement semantics OPEN until executed evidence exists.

## OPEN / DEPENDENCY / CHANGE WATCH
- **OPEN:** actual MintTap/LogMate fleet membership model, device identifiers/incarnations, MDM/ADE/Apple Business usage, retirement roles, wipe acknowledgement, credential revocation, data recovery, backup/export and rejoin semantics.
- **OPEN:** physical iPadOS/WebKit PWA behavior and installed/Home-Screen PWA persistence across actual organizational reset/re-enrollment flows.
- **DEPENDENCY:** Software Engineering owns implementation-level device identity, data migration, sync and test harnesses when product source/runtime authorization exists.
- **DEPENDENCY:** Design Studio owns reusable recovery/status interaction quality; Web Manager supplies web/PWA state requirements.
- **CHANGE WATCH:** Apple Business/MDM commands, Return to Service, iPadOS versions and enrollment behavior are platform/provider-specific and current documentation must be rechecked before implementation.

## Gate result
**253 PASS (generic).** The Web Manager can now distinguish silence, loss, retirement, release, wipe, sanitization, authority revocation and re-enrollment; govern convergence-debt denominator exit without timeout laundering; and reason about stale-tail resurrection while preserving unique offline PWA data. Product/MDM/physical-iPad/runtime validation remains OPEN.

## Next high-value target
**254 — device-incarnation identity, re-enrollment lineage & recovered-data ownership transfer.** Determine how to bind same-hardware/new-enrollment incarnations without serial-number authority splicing; how recovered offline data from a retired user/device is quarantined, attributed and transferred; how key/token/device identifiers rotate across erase/re-enrollment; and how rejoin evidence proves continuity where intended without granting old authority to the new incarnation.