# 307 — LogMate PWA Email-Auth Abuse-Control Layering & Release Gate

Status: **PASS (generic/source contract) / PRODUCT CONFIG + RUNTIME VALIDATION OPEN**  
Date: 2026-10-03  
Owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: **A, B, C, D**  
Consumes: **306**

## SOURCE

Canonical Web Manager `main` begins this checkpoint at `f3d7b7a6d0bfb8749cdab1d8c286d286eac84bab`. Canonical LogMate `main` is `31ecf70f5446d49cf6eb8b566e270ac273b37d61`; the relevant auth refinement remains `dbc2a5ddc67318479428fcc4103b2a3c73b275f5`.

306 established the email-identifier privacy boundary. Current Google Identity Platform documentation adds an adjacent but distinct boundary: email-enumeration protection removes several account-existence disclosures, but invalid sign-up still returns `EMAIL_EXISTS`. Google therefore recommends separate sign-up abuse controls. Firebase's security checklist separately recommends tightening Identity Toolkit quotas against brute force.

Identity Platform's reCAPTCHA Enterprise integration is another independent control plane. For email/password authentication it supports OFF, AUDIT and ENFORCE states. In ENFORCE, supported requests without a reCAPTCHA token are rejected; Google recommends AUDIT first and migration of clients before ENFORCE.

Primary references checked 2026-10-03:
- https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
- https://firebase.google.com/support/guides/security-checklist
- https://docs.cloud.google.com/identity-platform/docs/recaptcha-enterprise
- https://docs.cloud.google.com/identity-platform/docs/recaptcha-troubleshooting

## SYNTHESIS

Email privacy and automated-abuse resistance are separate security properties.

Guards:
- `enumeration protection enabled != every auth endpoint non-enumerating`;
- `enumeration protection PASS != brute-force resistance PASS`;
- `generic password-reset response != sign-up disclosure eliminated`;
- `reCAPTCHA configured != reCAPTCHA enforced`;
- `AUDIT telemetry exists != abusive request blocked`;
- `ENFORCE enabled != every deployed client compatible`;
- `bot rejection PASS != legitimate Safari/Home-Screen/managed-iPad client PASS`;
- `Firebase default/recommendation != LogMate production configuration verified`;
- `App Check/reCAPTCHA terminology != one interchangeable control`.

The last guard matters operationally: Identity Platform reCAPTCHA bot protection, Firebase App Check, endpoint quotas/rate controls and email-enumeration protection must be inventoried independently. Their objectives and failure modes overlap but are not equivalent.

## MINTTAP DECISION

Preserve 306's direction: do not weaken enumeration protection to recover historical account-mode discovery.

Before any LogMate email/password release is promoted, require a configuration evidence packet that independently identifies:
1. email/password provider and intended self-registration policy;
2. enumeration-protection state;
3. Identity Platform reCAPTCHA email/password state (OFF/AUDIT/ENFORCE), threshold/rules and supported client SDK path;
4. Firebase App Check registration/enforcement, if used, without treating it as proof of item 3;
5. Identity Toolkit quota/rate controls;
6. any backend/blocking-function admission policy;
7. privacy-minimized auth/security telemetry.

Unknown configuration remains OPEN; generic platform defaults never become product PASS evidence.

## PWA / EFB APPLICATION

A company-iPad PWA creates a two-sided release risk. Weak abuse controls can expose authentication endpoints; overly aggressive enforcement can strand legitimate users after a long offline interval, WebKit/Home-Screen lifecycle change, token/config refresh, network transition or managed-network restriction.

Therefore release admission requires both **security effectiveness** and **legitimate-client survivability**. Do not infer either from desktop Chromium alone.

Track A owns browser/PWA token/config/lifecycle mechanics and Safari-vs-Chromium evidence. Track B owns non-disclosing, recoverable user states when authentication is rejected or temporarily unavailable. Track C owns contradiction/failure tests and false-rejection evidence. Track D owns privacy-minimized security measurement and must not turn raw email/account existence into an analytics dimension. Track E owns configuration, abuse-control layering and release admission.

## VALIDATION

### V0 — configuration evidence
Capture actual project configuration for the seven items above, with environment/project identity and observation date. Distinguish Firebase Auth, Identity Platform reCAPTCHA and App Check controls.

### V1 — privacy matrix
Using controlled existing/nonexistent accounts, compare sign-in, password reset, verification/resend and any reachable sign-up flow. Record HTTP/SDK outcome class, visible copy/state and telemetry category. Do not use uncontrolled real-user addresses.

### V2 — abuse-control matrix
For supported test environments exercise valid, missing, expired/invalid or otherwise rejected bot/attestation evidence where the platform permits deterministic testing. Confirm AUDIT does not masquerade as enforcement. Exercise quota/rate boundaries without destructive production load.

### V3 — legitimate-client survivability
Repeat supported auth journeys across clean load, persisted session, reload, Service-Worker-controlled state, offline start then rejoin, token/config refresh and browser restart. Failure must remain recoverable and must not silently mutate local ledger authority.

### V4 — browser/device promotion
Chromium is evidence only for Chromium. Promote separately through Safari browser, installed Home-Screen Web App, physical iPad, then representative managed-company-iPad/network conditions.

### V5 — rollout/rollback
Before ENFORCE or stricter threshold/quota rollout, require audit/compatibility evidence, staged activation, observability and rollback criteria. Verify rollback does not require disabling enumeration protection or exposing account existence.

## TRANSFER VALIDATION / CONTRADICTIONS

- 306 privacy PASS transfers only to disclosure requirements, not abuse-resistance PASS.
- A reCAPTCHA ENFORCE result that blocks the representative EFB client is a release contradiction even if bot blocking works.
- A usable EFB client that reveals account existence is also a release contradiction.
- Security telemetry that requires raw email as a general analytics key contradicts Track D minimization; use purpose-bound security evidence instead.
- Product self-registration reachability remains a separate source/runtime fact. Presence of create-account code alone does not establish a supported public journey.

## CHANGE WATCH

Identity Platform/Firebase authentication, reCAPTCHA Enterprise integration, App Check Authentication support, WebKit PWA lifecycle and SDK compatibility are change-sensitive. Recheck authoritative documentation before production enforcement changes.

## OPEN

Actual LogMate Firebase/Identity Platform project configuration; intended public self-registration policy; deployed App Check/reCAPTCHA/quota controls; runtime disclosure behavior; abuse/false-positive evidence; Safari/Home-Screen/physical-iPad/managed-iPad evidence; production telemetry; production release/rollback validation.
