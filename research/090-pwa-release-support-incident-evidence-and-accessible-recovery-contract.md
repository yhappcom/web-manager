# 090 — PWA Release, Support & Incident Evidence + Accessible Recovery Contract

Status: **PASS (generic governance/acceptance contract) / TARGET-DEVICE & AT EXECUTION OPEN**  
Date: 2026-09-17

## Purpose
Extend 089 from test architecture into the operational boundary where a release is accepted, a user reports failure, support gathers evidence, an incident is diagnosed, and degraded/recovery states remain accessible. The highest-value bottleneck is now the Track C ↔ E boundary, consuming Track A Safari/WebKit diagnostics and Track B truthful-state semantics.

## Integrated model
`release lineage → pre-release invariant evidence → exact-artifact/device acceptance → rollout → privacy-minimized health evidence → user-visible degraded state → support diagnostic capture → incident correlation → recovery/forward-fix → post-recovery invariant check → retained evidence/postmortem`

## SOURCE — Safari/iPad inspection boundary
WebKit's current Web Inspector reference (updated 2025-03-19) documents remote inspection of Safari pages and websites added to the iOS Home Screen when Web Inspector is enabled on the iOS device and the inspecting Mac. A cable or Xcode-configured wireless debugging path is required. Apple Safari Developer Tools also documents Web Inspector for webpages, service workers and Home Screen web apps, and Safari WebDriver for browser automation.

**SYNTHESIS:** Safari/Home-Screen diagnostic capability exists generically, but this does not prove that the company's managed EFB configuration permits enabling Web Inspector, pairing to an authorized Mac, wireless inspection, diagnostic export, or support access. Those remain target-device/MDM acceptance questions.

Guard: `Safari diagnostic capability documented ≠ managed-EFB diagnostic workflow permitted`.

## SOURCE — accessible status and recovery communication
W3C WAI's current accessibility-responsibility material maps WCAG 2.2 SC 4.1.3 status-message work to UX/front-end ownership: status/toast-like changes should be programmatically exposed so assistive technology can announce them without moving focus. WCAG conformance remains distinct from product usability and target-device AT execution.

**SYNTHESIS:** PWA state truth such as local-save completion, sync pending/completed, update readiness, conflict, offline fallback and recovery completion cannot rely only on color, transient animation or an unannounced toast. Important state changes need persistent discoverability where the consequence remains relevant, and programmatic status semantics where an announcement is appropriate. Focus should move only when the user must act in a new interaction context, not merely because background state changed.

## SOURCE — diagnostic minimization and log security
OWASP Logging guidance states that logs should normally exclude or sanitize session identifiers, access tokens, sensitive personal data, passwords, secrets and other data beyond the logging system's authorization; logging itself needs confidentiality, integrity and availability controls. OWASP Session Management recommends correlation without recording raw session IDs, for example by using a salted hash when session correlation is required.

**SYNTHESIS:** a PWA support bundle is a security/privacy product surface. It is not exempt from minimization because it is 'diagnostic'. Flight-record payloads, crew names, routes, tokens, cookies and encryption keys are not justified merely to diagnose worker/cache/schema/navigation state.

## 1. Release acceptance packet
A release that changes worker/cache/schema/sync/offline/auth/recovery behavior should retain one acceptance packet:
- exact source commit and immutable build/release identifier;
- worker/shell/local-schema/protocol generations;
- environment/config class without secrets;
- migration compatibility window and unsupported generation pairs;
- selected 089 fault cases and results;
- accessibility/degraded-state assertions;
- browser/engine/device evidence tier and exact conditions;
- target managed-iPad result when a managed-EFB claim is made;
- rollback/forward-fix boundary, including whether older code can open newer state;
- known limitations/OPEN items;
- approver/decision record and evidence links.

Guard: `release deployed ≠ release accepted ≠ product recovery validated`.

## 2. Support diagnostic bundle — user-safe contract
Default bundle should prefer structural state:
- diagnostic bundle schema version;
- app/build ID;
- worker lifecycle + generation;
- shell/cache generation and cache inventory categories/counts, not cached payloads;
- local DB schema generation;
- outbox count and state categories, not mutation payloads;
- last local-save / sync-attempt / remote-ack timestamps only when justified;
- navigation outcome/source class;
- storage persistence state/quota estimate when available;
- migration/recovery result codes;
- browser/OS/container/network class;
- feature/capability detection relevant to the incident;
- ephemeral diagnostic correlation ID;
- redaction/minimization version.

Default exclusion:
- flight-record content;
- crew/passenger names;
- route/registration details unless separately and explicitly justified for a specific incident;
- raw session IDs/cookies/access or refresh tokens;
- credentials/keys/secrets;
- unrestricted URLs/query strings that can carry personal data;
- full IndexedDB/Cache dumps.

If payload-level evidence is ever required, it needs an explicit escalation path, user/organizational authorization where applicable, narrow scope, retention limit and access control. Do not silently expand normal telemetry.

## 3. Correlation without identity leakage
Separate:
`release identity ≠ device identity ≠ user/account identity ≠ session identity ≠ diagnostic-run identity`.

Use the least stable identifier that answers the diagnostic question. A one-run correlation ID is preferable for worker/cache/recovery investigation when cross-session identity is unnecessary. If account/session correlation is genuinely required, define a reviewed pseudonymous correlation method rather than logging raw session credentials.

## 4. Supportability as release quality
A release can be functionally correct in the happy path yet operationally unsafe if support cannot distinguish:
- local-only vs acknowledged data;
- old worker vs new worker control;
- schema mismatch vs network failure;
- reconstructible-cache loss vs authoritative-record loss;
- migration blocked vs migration corrupted;
- offline client vs telemetry pipeline failure.

Therefore consequential PWA releases need diagnostic observability sufficient to classify failure without requiring destructive actions such as clearing all site data.

Guard: `cannot diagnose ≠ user should clear storage`.

## 5. Accessible degraded-state contract
Canonical state semantics consumed from Track B:
- saved on this device;
- waiting to sync;
- sync attempt in progress;
- remotely acknowledged/reconciled;
- conflict/review required;
- offline but task available;
- offline and task unavailable;
- update available/deferred;
- update required before a task can continue;
- migration/recovery in progress;
- recovery completed;
- recovery blocked / support required;
- backup current / backup overdue / backup not verified.

Track C acceptance requirements:
- state is not color-only;
- persistent consequential states remain discoverable after transient announcements disappear;
- programmatic status semantics are used for appropriate dynamic changes;
- background status updates do not steal focus;
- actionable blocking recovery surfaces have a logical heading, focus order and keyboard/touch operability;
- timeout/retry messaging does not falsely claim remote acknowledgement;
- screen-reader/zoom/reflow/contrast/reduced-motion checks are included at the appropriate evidence tier;
- exact Safari/iPad + assistive-technology behavior remains OPEN until executed.

## 6. Incident evidence lifecycle
Incident flow:
`detect/report → freeze release/device/environment identity → preserve local authoritative data/outbox → collect minimized diagnostic state → classify failure domain → reproduce at appropriate evidence tier → choose rollback/forward-fix/recovery → verify data invariants → communicate truthful state → retain evidence → postmortem/change-watch`.

Never begin by clearing storage or reinstalling when unsynchronized authoritative records may exist. First preserve/recover evidence and data according to the 085/088 recovery contracts.

## 7. Telemetry blind spots
An offline, crashed, storage-corrupted or worker-broken client may be unable to emit telemetry. Therefore:
- server-side silence is not success;
- missing client events need an explicit `unknown/not observed` interpretation;
- support/user reports and exact-device inspection are independent evidence channels;
- health dashboards must not use reporting-client denominator alone to certify durability.

## 8. Cross-track ownership
- **A Platform/Browser:** owns Safari/WebKit inspection mechanics, worker/storage/network semantics and capability CHANGE WATCH.
- **B UX/IA/Content:** owns truthful state taxonomy, action hierarchy and durable help/recovery information architecture.
- **C Quality:** owns accessible degraded-state assertions, evidence tiers and release acceptance oracles.
- **D Search/Analytics:** may consume aggregate structural health signals; cannot infer healthy silent clients or expand collection without governance.
- **E Architecture/Security/Operations:** owns diagnostic access/retention, incident workflow, release lineage, rollback/forward-fix and support escalation.

Web Manager coordinates the packet and prevents one discipline's convenience from overriding data safety/privacy/accessibility.

## 9. Design Studio transfer
Current Design Studio Web status is Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED. W040 durable audit-reconstruction contract is ready but execution is OPEN; no Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS exists. Therefore Design Studio can own the visual/interaction realization of these recovery states, but Web Manager retains the truthful-state/accessibility acceptance contract and must not infer runtime validation.

## 10. Software Engineering transfer
Software Engineering Studio remains Foundation-level. Its D003 executable evidence shows that schema migration success and cross-version application compatibility are distinct and that transaction boundaries can prevent some partial-publication states without proving mobile/distributed compatibility. Transfer to PWA release acceptance: worker/build generation and persisted schema generation are separate identities; rollback must explicitly test whether an older artifact can safely open newer persisted state.

Required implementation evidence:
- diagnostic bundle generator + redaction tests;
- fixtures proving raw tokens/record payloads are excluded;
- release packet generation tied to exact artifact;
- interrupted migration and rollback-release matrices;
- target Safari/Home Screen inspection on authorized physical iPad;
- exact managed-EFB check for whether inspection/pairing/export is permitted;
- AT/physical-device degraded-state execution when environment permits.

## 11. OPEN / VALIDATION
- exact managed EFB MDM policy for Safari Web Inspector and device pairing;
- whether support staff can lawfully/operationally obtain diagnostic bundles from the company device;
- actual LogMate diagnostic/telemetry implementation and data classification;
- retention/access/consent or other privacy requirements for production diagnostics;
- exact Safari/Home Screen screen-reader behavior for state announcements;
- exact rollback compatibility across future LogMate persisted schemas;
- actual production incident ownership/escalation.

## CHANGE WATCH
- Safari/WebKit Web Inspector and Home Screen debugging behavior;
- Service Worker/WebKit fixes;
- WCAG/WAI implementation guidance;
- platform/MDM restrictions affecting inspection, export and diagnostics;
- privacy/security requirements applicable to actual deployment jurisdictions and organizational policy.

## Competency checkpoint
PASS at generic governance level. The Web Manager can now connect 089 test evidence to release acceptance, privacy-safe support diagnostics, accessible degraded/recovery state requirements and incident evidence preservation. Product certification remains OPEN until exact artifact + managed iPad + AT/security/privacy/operational evidence exists.

## Sources
- WebKit, `Enabling Web Inspector`, updated 2025-03-19, accessed 2026-09-17.
- Apple Developer, Safari Developer Tools — Web Inspector / Develop menu, accessed 2026-09-17.
- W3C WAI, Tasks Involved in Accessibility — Dynamic Interactions, updated 2025-07-24, accessed 2026-09-17.
- OWASP Logging Cheat Sheet / Session Management Cheat Sheet, accessed 2026-09-17.
- `yhappcom/design-studio` `progress/WEB_STATUS.md`, checked 2026-09-17.
- `yhappcom/software-engineering-studio` `progress/STATUS.md`, checked 2026-09-17.