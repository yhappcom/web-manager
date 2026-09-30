# 301 — LogMate PWA Firebase Auth Popup, Offline Authority & Rejoin Validation Contract

Status: **PASS (engineering-evidence integration) / PHYSICAL-IPAD + MANAGED-IPAD + PROVIDER-CONSOLE + OFFLINE-REJOIN VALIDATION OPEN**  
Date: 2026-09-30  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: **A Platform/Browser**, **B UX/IA**, **C Quality/Validation**  
Consumer: **D Search/Discovery/Analytics** for observation only

## Why this gate exists

300 established that connectivity is evidence rather than synchronization authority. Canonical LogMate engineering evidence now resolves part of a previously OPEN product topology: LogMate V1 requires a Firebase account; Firebase UID is owner authority; temporary network/token failure must not be interpreted as sign-out; an established unlocked owner may continue offline local use; and the PWA Google entry invokes Firebase Auth `GoogleAuthProvider` popup execution.

This is enough to stop treating authentication as wholly hypothetical, but not enough to claim production PWA authentication acceptance. The exact Firebase/Google console configuration, physical iPad popup behavior, installed-PWA behavior, persistence/reload behavior, reauthentication after offline use, and managed-device policy remain OPEN.

## SOURCE — canonical Software Engineering evidence

Canonical LogMate `MASTER.md` (2026-09-28) establishes:

- Firebase account required for V1;
- Firebase UID is the sole owner authority;
- startup routing distinguishes signed-out, verified matching UID, wrong UID, deletion lock and setup state;
- transient network/token failure is not sign-out and does not revoke established unlocked-owner offline local use;
- explicit sign-out performs local lock before Firebase sign-out;
- PWA Google uses the shared LogMate peer shell and starts Firebase Auth `GoogleAuthProvider` popup execution;
- real-provider browser/device acceptance and Firebase/Google console operational acceptance remain OPEN.

Commit `75870c1d7c61c75e33628a38bca9dac4df6effcb` is canonical evidence for the popup execution decision. Commit `75a0e8363e16dd177cfdf16d2c32d09f58e55712` adds the PWA Google client-ID metadata to `web/index.html`; configuration presence is not provider acceptance.

Canonical LogMate presentation architecture also establishes PWA as the sole Web-family product target, with Tablet/EFB as the primary supported Web-family surface. Browser-tab execution remains a supported install/auth/recovery/fallback/validation path but is not a separate product UI.

## SOURCE — Firebase / Web platform

Firebase documents both popup and redirect Google sign-in. Its current Google sign-in documentation says redirect is preferred on mobile devices. Firebase's redirect best-practices documentation also states that popup can avoid the cross-origin third-party-storage issue affecting redirect flows, while warning that popup can be blocked by devices/platforms and can be less smooth on mobile.

Sources:
- https://firebase.google.com/docs/auth/web/google-signin
- https://firebase.google.com/docs/auth/web/redirect-best-practices

Firebase documents browser Auth persistence dependencies including IndexedDB, localStorage and sessionStorage in its web Auth initialization model. The actual Flutter/Firebase adapter and selected persistence behavior must be verified from implementation/runtime evidence rather than inferred from generic Firebase defaults.

Source:
- https://firebase.google.com/docs/auth/web/custom-dependencies

Web popup creation is gated by transient user activation. A provider popup must remain causally attached to a qualifying user action; delayed/asynchronous indirection can lose the activation window or be blocked.

Source:
- https://developer.mozilla.org/en-US/docs/Web/API/Window/open
- https://developer.mozilla.org/en-US/docs/Glossary/Transient_activation

## SYNTHESIS

### 1. Owner authority, browser Auth persistence and local ledger access are separate

Use separate states:

- **A0 — no resolved Firebase identity**
- **A1 — provider interaction initiated**
- **A2 — Firebase identity resolved**
- **A3 — verified UID accepted**
- **A4 — UID matches durable ledger owner**
- **A5 — local ledger unlocked for this application session**
- **A6 — remote token/session currently accepted**
- **A7 — operation-specific remote authorization accepted**

An established A4/A5 state may remain locally useful during a transient loss of A6 if the product contract explicitly permits it. Loss of network must not synthesize A0. Conversely, a cached local UI or persisted Firebase session must not silently establish A4/A5 without the LogMate startup/owner checks.

### 2. Popup success is not product readiness

`signInWithPopup` resolving is provider/Firebase authentication evidence. Product readiness still requires verification, UID-owner matching, deletion-lock checks and setup state.

`popup success ≠ ledger authority established`.

### 3. Popup failure classes must not collapse into sign-out

At minimum distinguish:

- popup blocked / no user activation;
- user cancellation;
- provider/network failure;
- Firebase configuration/authorized-domain failure;
- credential/account mismatch;
- successful Firebase authentication followed by LogMate wrong-UID rejection;
- already-established owner going temporarily offline.

These have different recovery and data-exposure consequences.

### 4. Mobile popup is an explicit validation risk

Firebase currently prefers redirect on mobile, while LogMate canonically selects popup for PWA Google. That is not a contradiction requiring immediate redesign: Firebase supports popup. It is a **TRANSFER VALIDATION** requirement. The selected popup flow must pass exact installed-PWA and Safari/iPadOS tests before release. A desktop/Chrome popup PASS is non-transitive.

### 5. Redirect is not a free fallback

If future validation motivates redirect, Firebase documents third-party-storage restrictions affecting redirect flows on Safari 16.1+ and other browsers unless an approved hosting/auth-domain strategy is used. Therefore a popup failure must not trigger an unreviewed redirect fallback.

### 6. Offline local authority must be bounded

The current product decision allows an established unlocked owner to keep using local data during transient network/token failure. This requires:

- durable evidence of the accepted owner binding;
- fail-closed wrong-UID handling on identity resolution;
- no remote-confirmation claims while N5–N8 from gate 300 are absent;
- reauthentication/re-adjudication before remote operations when required;
- explicit lock semantics on user sign-out/deletion.

Offline capability is not anonymous/account-free mode.

## MINTTAP DECISION

For LogMate-like PWA validation:

1. Treat the canonical Firebase UID/owner contract as actual engineering evidence, not generic PWA speculation.
2. Keep PWA Google popup as the current product implementation choice; do not promote it to release PASS until exact Safari/iPadOS installed-PWA evidence exists.
3. Preserve user-gesture causality from the visible `Continue with Google` action to popup invocation.
4. Never map network/token failure to signed-out state when a previously accepted owner remains locally authorized by the product contract.
5. Never map provider/Firebase sign-in success directly to ledger visibility; complete verification/UID-owner/lock routing first.
6. Do not add redirect fallback without validating Firebase auth-domain/hosting requirements and Safari storage restrictions.
7. Keep auth persistence mechanism, console provider enablement, authorized domains, exact redirect/popup behavior and managed-iPad policy as runtime evidence, not assumptions.
8. Combine this gate with 300 for reconnect: local owner access can survive transient connectivity loss while remote authorization/convergence remains independently unproven.

## HARD GUARDS

- `popup opened ≠ authenticated`
- `authenticated ≠ verified owner`
- `Firebase UID resolved ≠ ledger UID matched`
- `provider success ≠ ledger unlocked`
- `network failure ≠ signed out`
- `persisted Firebase session ≠ LogMate owner gate bypassed`
- `offline local access ≠ remote authorization`
- `Google client ID present ≠ provider configured/accepted`
- `desktop popup PASS ≠ iPad installed-PWA PASS`
- `Safari-tab PASS ≠ Home-Screen PWA PASS`
- `popup failure ≠ redirect fallback safe`
- `redirect supported ≠ third-party-storage constraints resolved`

## DEPENDENCY / TRANSFER

**Track A** owns popup/user-activation/browser-context mechanics and Safari/Home-Screen differences.  
**Track E** owns identity/owner/trust/session/re-auth/sign-out boundaries.  
**Track B** owns recovery semantics and must distinguish cancel, blocked popup, reauthentication, wrong account and offline continuation without false reassurance.  
**Track C** owns physical browser/device and destructive/session-transition validation.  
**Track D** may measure auth funnel outcomes but telemetry must not become owner authority.  
**Software Engineering** remains canonical for actual Firebase adapter, owner gate and local-lock implementation.

## VALIDATION — deterministic campaign

At minimum test:

1. Direct user tap opens Google popup.
2. Popup invocation after async delay loses user activation.
3. Browser blocks popup.
4. User cancels provider flow.
5. Provider network failure before Firebase identity resolution.
6. Firebase provider disabled/misconfigured.
7. Unauthorized domain/configuration failure.
8. Successful Google auth + verified matching UID.
9. Successful Google auth + wrong UID.
10. Successful auth + unverified account state where applicable.
11. Existing unlocked owner loses network.
12. Existing unlocked owner experiences token refresh failure.
13. App reload offline with durable owner evidence.
14. App reload offline without sufficient owner evidence.
15. Explicit sign-out while offline: local lock occurs before remote sign-out completion.
16. Reconnect after offline local mutations with expired token.
17. Reconnect after credential revocation.
18. Reauth succeeds but queued operation is no longer authorized.
19. Server commit + ACK loss after reauth.
20. Safari browser-tab popup on physical iPad.
21. installed Home-Screen PWA popup on physical iPad.
22. PWA resumed after provider popup/context switch.
23. managed company iPad with Safari/popup/content restrictions.
24. Google provider popup from portrait and landscape EFB presentation.
25. keyboard/VoiceOver activation preserves valid user-activation path.
26. popup error status is programmatically exposed without leaking sensitive account-existence detail.
27. Chrome/desktop PASS incorrectly promoted to iPad Safari.
28. browser-tab PASS incorrectly promoted to installed PWA.
29. popup failure triggers unreviewed redirect fallback.
30. redirect experiment without same-domain/authDomain mitigation on affected Safari.

All are **DEFINED / NOT EXECUTED** unless an exact existing LogMate evidence artifact is explicitly correlated later.

## Validation ladder

- **V0:** canonical auth/owner state topology + provider/config inventory.
- **V1:** deterministic adapter/startup-gate tests with popup/cancel/network/wrong-UID/reload/rejoin injection.
- **V2:** exact Safari/WebKit/iPadOS browser-tab evidence.
- **V3:** exact installed Home-Screen PWA on physical unmanaged iPad.
- **V4:** representative managed company iPad with actual MDM/browser/network policy.
- **V5:** real Firebase/Google provider configuration and account lifecycle.
- **V6:** offline mutation → reauth → remote acknowledgement/convergence with actual sync topology.
- **V7:** keyboard/VoiceOver/human recovery comprehension.

PASS is non-transitive.

## CONTRADICTION / TRANSFER VALIDATION

Firebase's current documentation prefers redirect on mobile. LogMate currently selects popup for PWA Google. Because Firebase also officially supports popup, this is not evidence that LogMate is wrong; it creates a target-specific acceptance obligation. The decision remains acceptable only if exact physical iPad/PWA evidence demonstrates reliable popup execution and recovery.

## CHANGE WATCH

- Firebase popup/redirect guidance and browser storage mitigations.
- Safari/WebKit popup and installed-web-app context behavior.
- Firebase Auth persistence behavior used by the actual Flutter web adapter.
- Google/Firebase provider-console and authorized-domain configuration.
- MDM/Safari/content-filter policy affecting provider windows.

## OPEN

- Exact deployed Firebase Auth provider configuration.
- Exact authorized domains/authDomain/hosting topology.
- Exact web Auth persistence selected by the current Flutter/Firebase adapter.
- Physical Safari/iPad popup behavior.
- Installed-PWA popup/resume behavior.
- Managed-iPad popup/content-filter behavior.
- Actual Sync/outbox/ACK/reconciliation topology.
- Real-provider accessibility and recovery acceptance.

## Integrated competency

The relevant question is no longer “can a PWA authenticate with Google?” Canonical engineering evidence says LogMate does use Firebase UID authority and a Google popup path. The operational question is:

> Can the exact iPad PWA preserve the distinction between provider interaction, Firebase identity, verified ledger ownership, offline local authority and remote authorization across popup blocking, network loss, reload, reauthentication and reconnect—without exposing the wrong ledger or falsely claiming remote success?

Until V3–V6 evidence exists, release acceptance remains OPEN.
