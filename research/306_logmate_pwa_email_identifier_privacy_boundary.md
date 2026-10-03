# 306 — LogMate PWA Email-Identifier Privacy Boundary

Status: **PASS (source/contract diagnosis) / PRODUCT CONFIG + RUNTIME VALIDATION OPEN**
Date: 2026-10-03
Owner: **Track E — Web Architecture, Security & Operations**
Dependencies: **A, B, C, D**
Consumes: **304, 305**

## SOURCE
Canonical LogMate main is `31ecf70f5446d49cf6eb8b566e270ac273b37d61`. Commit `dbc2a5ddc67318479428fcc4103b2a3c73b275f5` refines email authentication. Its `EmailAccountModeResolver` comment records that `firebase_auth 6.7.0` no longer provides the former client-side `fetchSignInMethodsForEmail()` lookup, so production account-mode resolution needs an explicit product/backend decision. Until then, accountMode is a compatibility fallback and no visible Sign in/Create account selector is exposed on the email page.

Google Identity Platform recommends email-enumeration protection for all projects. Projects created on or after 2023-09-15 have it enabled by default. With protection enabled, sign-in-method discovery does not reveal methods for a supplied email. Firebase Flutter/Web documentation says the former identifier-first differentiation pattern based on that method is disabled by this protection and recommends against disabling the protection.

Primary references checked 2026-10-03:
- https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
- https://firebase.google.com/docs/auth/flutter/email-link-auth
- https://firebase.google.com/docs/auth/web/email-link-auth

## SYNTHESIS
The missing client lookup is a privacy/security boundary, not merely an SDK inconvenience.

Guards:
- identifier-first UX desired != pre-auth account-existence lookup justified;
- SDK lookup unavailable != public replacement lookup required;
- generic recovery response != unusable UX;
- Firebase newer-project default != LogMate production setting verified;
- source comment recognizes the boundary != runtime behavior proven.

## MINTTAP DECISION
Preserve email-enumeration protection as the default direction. Do not disable it merely to restore historical sign-in-method discovery. Do not infer the actual LogMate Firebase setting until it is directly verified.

If identifier-first UX remains desired, the next step should not depend on revealing account existence before authentication. Product/Design owns exact interaction; Software Engineering owns implementation; Web Manager owns privacy requirements and PWA/browser validation.

## VALIDATION
V0: verify the actual Firebase setting; inventory client/server account-mode discovery; inspect auth telemetry fields.
V1: paired existing/nonexistent-address tests across identifier entry, sign-in, reset, verification/resend and account creation; compare visible state and error taxonomy.
V2: repeat with clean/persisted/offline Service-Worker-controlled PWA states; verify cached account-mode state does not survive sign-out/user handoff.
V3: Safari and Home-Screen Web App separately, then physical and representative managed iPad.

## TRACK TRANSFERS
A owns browser cache/session mechanics. B owns usable non-disclosing recovery journeys. C owns paired contradiction and cross-browser/device tests. D uses privacy-minimized measurement. E owns configuration evidence, disclosure boundary and release admission.

## CORRECTION
The 2026-10-02 LogMate auth commit does not establish the previously reported provider-UID-continuity change. The security-relevant source evidence visible in that commit is the added Firebase cancellation-code mapping and the explicit account-mode resolver comment. UID continuity may be a useful generic invariant, but it must not be attributed to this commit without direct canonical source evidence.

## OPEN
Actual LogMate Firebase enumeration-protection setting; any production account-mode resolver; deployed behavior; telemetry schema; PWA cache/session interaction; Safari/Home-Screen and managed-iPad evidence.
