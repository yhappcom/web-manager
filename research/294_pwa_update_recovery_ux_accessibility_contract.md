# 294 — PWA Update, Recovery-State UX & Accessibility Validation Contract

Status: **PASS (generic evidence/contract) / REPRESENTATIVE PHYSICAL MANAGED-IPAD + AT + HUMAN VALIDATION OPEN**  
Date: 2026-09-27  
Primary owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: Track A service-worker/runtime mechanics; Track B state/task architecture; Track E authority/recovery semantics from 290–293. Track D consumes privacy-minimized diagnostics only.

## Scope
This study converts the lifecycle, managed-device, offline-authority and cross-device boundaries in 290–293 into a user-observable and accessibility-testable recovery contract. It does not select LogMate authentication, synchronization transport, schema, MDM vendor or visual design.

## SOURCE
- W3C WCAG 2.2 is a Recommendation. SC 4.1.3 requires status messages to be programmatically determinable so assistive technology can present them without receiving focus. WCAG 2.2 also adds Focus Not Obscured (Minimum).
- Service Worker lifecycle separates install/waiting/activation/control. `skipWaiting()` can request immediate activation; `Clients.claim()` lets an active worker control in-scope clients immediately. These mechanics do not establish application-data/schema/queue correctness.
- WebKit documents remote inspection of iOS/iPadOS Safari pages and Home Screen web apps. Debugger-assisted behavior therefore needs an instrumentation-off replay before representative promotion.
- Safari 26 documentation says users can add any site to the Home Screen; a manifest is no longer an installability prerequisite on that platform. This is platform behavior, not proof of offline durability or product readiness.

## SYNTHESIS — consequence states must remain distinct
Do not collapse the following into one Online/Saved/Synced boolean:
1. **Saved locally** — unique work is durably represented in the current local evidence envelope.
2. **Pending** — local work exists but remote consequence is unresolved.
3. **Needs connection** — required destination is not presently reachable.
4. **Needs reauthentication/current admission** — identity/session evidence is insufficient for the requested remote consequence.
5. **Needs re-pairing/peer approval** — cross-device peer authority is unresolved.
6. **Update available** — newer runtime material exists; current work is not thereby invalid.
7. **Update required before remote action** — current runtime/schema cannot safely execute a material remote consequence.
8. **Conflict requires review** — competing valid work cannot be safely auto-converged.
9. **Rejected/quarantined** — current policy/admission rejects the remote effect while preserving explainable local provenance where defensible.
10. **Remotely confirmed** — current remote authority accepted the effect and the product has evidence appropriate to its convergence contract.

`local save ≠ remote acknowledgement ≠ semantic convergence`.

## Update-safety ladder U1–U10
U1 update discovered; U2 update acquired/worker installed; U3 waiting/activation state known; U4 expected client control established; U5 application/schema migration completed; U6 unique data, provenance and queued payload integrity established; U7 current session/grant/peer authority established; U8 queued operations re-adjudicated under current semantics; U9 visual and programmatic state truthfully represents consequence; U10 rollback/recovery path preserves unique work and does not resurrect obsolete authority.

No earlier rung promotes a later rung. In particular:
- `worker installed ≠ product safely updated`;
- `skipWaiting() succeeded ≠ schema migration safe`;
- `clients.claim() succeeded ≠ queued work compatible`;
- `page refreshed ≠ unique work preserved`.

## Accessibility/recovery contract
- Routine background update/rejoin must not steal focus.
- A consequential blocking recovery step may move focus only when task continuation requires it, with deterministic focus placement and a return/continuation path.
- Focused controls must remain perceivable and not be obscured by author-created recovery banners/dialogs.
- Important non-focus status changes must be programmatically determinable; do not rely on visual text, color, animation or toast timing alone.
- Coalesce repetitive connectivity/retry noise. A live region is not a packet/event log.
- Persistent consequential states such as pending, rejected, conflict and update-required must remain discoverable after transient announcements disappear.
- Reduced-motion preference must not remove meaning or required controls; animation is never the sole carrier of sync/update consequence.
- Reauthentication must not imply replay-all. After authority changes, queued material operations return through 292 re-adjudication.
- Clear-site-data/reinstall is not a default repair while unique local work may exist.

## Representative validation matrix A0–A12
A0 baseline/reset and synthetic unique-data fixture; record OS/WebKit/build/launch context/management envelope.  
A1 offline local capture and relaunch; prove semantic record preservation.  
A2 connectivity flapping; prove announcement coalescing and no focus theft.  
A3 selective endpoint failure; distinguish shell reachability from auth/API/sync reachability.  
A4 session/admission expiry or revocation using the actual product mechanism; preserve local work and require current admission.  
A5 worker update with old client present; record installed/waiting/active/controller states.  
A6 schema/runtime transition with queued old-generation work; prove migration plus current consequence mapping.  
A7 deterministic conflict; verify persistent visual/programmatic conflict state and non-destructive resolution.  
A8 peer replacement/revocation/re-pairing where cross-device sync exists; predecessor authority must not resurrect.  
A9 interruption/background/process termination/relaunch; preserve task and local provenance within the supported envelope.  
A10 reduced-motion and zoom/reflow/keyboard checks for the recovery path.  
A11 VoiceOver plus external-keyboard task run on representative physical iPad; verify state comprehension, focus order, status exposure and recovery completion.  
A12 instrumentation-off replay of critical paths; debugger-attached PASS cannot alone become representative PASS.

Every case records PASS/FAIL/UNKNOWN. UNKNOWN never promotes to PASS.

## Track C destructive additions — DEFINED / NOT EXECUTED
1121. Binary-sync-label composition.  
1122. Installed-worker→updated-product promotion.  
1123. Background-status focus theft.  
1124. Consequential state exists only as ephemeral toast.  
1125. Live-region storm from connectivity/retry churn.  
1126. Color-only consequence distinction.  
1127. Motion-required comprehension.  
1128. Forced-refresh/update causes unique-local-data loss.  
1129. Reauthentication triggers replay-all without current re-adjudication.  
1130. Clear-data/reinstall used as default repair despite unique local work.  
1131. ACK rendered as converged/confirmed without the product convergence proof.  
1132. Blocking recovery dialog has no deterministic return/continuation path.  
1133. UNKNOWN rendered or announced as success/current.  
1134. Single-AT or debugger-assisted result promoted to representative fleet PASS.

## TRANSFER VALIDATION / CONTRADICTION
- Track A owns worker/controller mechanics; this artifact consumes them without turning lifecycle APIs into migration policy.
- Track B owns information/task architecture and should consume the consequence-state vocabulary without prescribing a visual system.
- Track E owns current authority, policy and recovery semantics; UX labels cannot create authority.
- Track D may measure coarse recovery outcomes, but analytics events are not authority, acknowledgement or convergence evidence.
- Design Studio should later translate these semantic states into visual/interaction treatments; Web Manager does not prescribe a universal component.
- Software Engineering should implement deterministic fixtures/harnesses only after concrete product runtime/auth/sync architecture is known.

## MINTTAP DECISION / DIRECTION
For any company PWA that can hold unique offline work, prioritize truthful recoverable state over seamless-looking state. Do not hide unresolved authority, conflict or update requirements behind a generic success indicator. Do not force destructive repair before preserving/exporting unique work where technically defensible.

For the LogMate-like EFB scenario, representative validation requires a physical managed iPad and the actual launch context, with VoiceOver/external-keyboard and instrumentation-off critical-path replay. Generic Safari, simulator, desktop, unmanaged iPad or automated accessibility results are prerequisites, not production certification.

## OPEN / VALIDATION
Actual LogMate/MintTap runtime, auth/session model, schema, queue, cross-device transport, MDM policy, Home Screen deployment, AT behavior and human task comprehension remain **OPEN**. No production PASS is claimed.

## CHANGE WATCH
Recheck WCAG/WAI guidance, WebKit Home Screen behavior, Service Worker lifecycle implementation differences and iOS/iPadOS accessibility/runtime behavior before product commitment or after material OS/WebKit policy changes.
