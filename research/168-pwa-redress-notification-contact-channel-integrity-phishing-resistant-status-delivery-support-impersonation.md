# 168 — PWA Redress Notification, Contact-Channel Integrity, Phishing-Resistant Status Delivery & Support Impersonation

Status: **PASS (generic) / PRODUCT + IDP + CONTACT-PROVIDER + LEGAL + HUMAN/AT + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track B notification/status UX; Track C accessibility/phishing/abuse validation; Track A Web Push/SW/offline mechanics; Track D aggregate delivery measurement.  
Dependencies: 094 account recovery, 166 explainability/redress, 167 identity/authorization/anti-abuse.

## Why this study exists

167 establishes that redress access is capability-scoped authorization. The adjacent failure is to let a delivery channel become authority: email/SMS/push can leak a sensitive decision on a lock screen, a link can become a bearer credential, a compromised mailbox/phone can silently become the only recovery path, or a support impersonator can use a plausible status message to steal authenticators/recovery evidence.

Central rule:

> **A notification is a hint that authoritative state may have changed, not the authoritative state, identity proof, adjudication result, or mutation credential. Deliver the minimum useful signal over the channel, resolve sensitive status in an authenticated first-party context, and keep channel recovery independent from policy adjudication.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns Web Push subscription/permission, Service Worker delivery, notification activation, offline/stale delivery and platform differences.
- **B UX/IA/Content:** very high dependency pressure. Owns low-disclosure copy, first-party status center, channel-change warnings, repudiation route and accessible fallback.
- **C Quality/Accessibility:** high dependency pressure. Owns lock-screen disclosure, phishing simulation, spoof resistance, stale notification, keyboard/AT and multi-channel failure validation.
- **D Search/Analytics:** bounded consumer. Delivery/failure/repudiation aggregates may be measured; notification payloads, contact identifiers and case reason must not become marketing identity graphs.
- **E Security/Operations:** **bottleneck/owner**. Owns notification-vs-authority separation, channel binding/currentness, support impersonation containment, token scope, provider compromise and incident response.

## SOURCE

### NIST SP 800-63B-4 — independent account notifications

Current final SP 800-63B-4 requires notifications for consequential authenticator/account events such as authenticator binding and account recovery. Account notifications are sent to notification addresses stored in the subscriber account; CSPs must support at least two notification addresses and recovery notifications include instructions/contact information for repudiation. Binding an authenticator requires notification by a mechanism independent of the binding transaction. NIST also explicitly says cross-endpoint authenticator binding codes must not be communicated over insecure channels such as email.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/events/
- https://pages.nist.gov/800-63-4/sp800-63b.html

Transfer: independent notification is valuable fraud detection, but a notification address is not automatically an authenticator or adjudication authority.

### OWASP Forgot Password — side channel and token hygiene

OWASP recommends consistent reset-request responses, side-channel delivery, cryptographically random/sufficiently long/single-use/expiring tokens, HTTPS trusted-domain reset URLs, referrer-leak protection, brute-force protection, and a notification after password reset. It also warns against locking an account merely because a reset was requested.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html

Transfer: if a redress workflow ever uses a link/token, possession can establish only the explicitly designed limited capability; it must not silently grant full case/account authority. Prefer authenticated first-party status navigation where a bearer token is unnecessary.

### Apple/WebKit — iOS/iPadOS Web Push is platform-visible and permissioned

Apple documents standards-based Web Push for Home Screen web apps on iOS/iPadOS 16.4+, using Push API, Notifications API and service workers. Permission requires direct user interaction. Notifications appear on the Lock Screen and Notification Center. Apple documents TTL/offline delivery behavior; a push may be stored and delivered later. Safari requires received push to result in a visible notification under the classic model. WebKit also documents badging and user-controlled notification settings.

Sources:
- https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/

CHANGE WATCH: WebKit Declarative Web Push changes implementation mechanics on newer Apple platforms. It does not change the authority rule that push content is a notification surface, not canonical case state.

### W3C WCAG status-message transfer

W3C WCAG technique ARIA22 shows `role=status` as one method for exposing in-page status updates to assistive technology without moving focus. This is an accessibility technique, not a security channel.

Source: https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA22.html

## SYNTHESIS — separate six objects

Do not collapse these into `contact verified` or `notification sent`:

1. **Notification destination** — where a signal can be sent.
2. **Destination validation/currentness** — whether the destination was previously validated and is still an allowed notification address.
3. **Delivery event** — provider acceptance/delivery attempt; not proof the intended human read it.
4. **Notification content** — minimum signal safe for the channel/lock screen.
5. **Status authority** — authenticated first-party case state and explanation.
6. **Mutation/adjudication authority** — separate capability authorization from 167/166.

Persistent guards:
- `notification delivered ≠ intended person read it`;
- `mailbox/phone possession ≠ full redress authority`;
- `validated contact once ≠ contact current forever`;
- `push subscription present ≠ device/person currently trusted`;
- `notification link clicked ≠ claimant authenticated`;
- `status deep link ≠ bearer mutation authority`;
- `support message plausible ≠ support authentic`;
- `provider accepted message ≠ end-user delivery proven`;
- `old notification authentic ≠ current case state`;
- `notification permission granted ≠ sensitive lock-screen disclosure consent`;
- `channel unavailable ≠ redress right extinguished`.

## Notification content: signal, then resolve securely

Default external-channel content should minimize sensitive case detail. A safe generic pattern is semantic, not prescribed copy: `There is an update to a request. Open the official app/site directly to review it.` Avoid putting sensitive policy reason, identity evidence, aviation/employment/health/financial detail, recovery secret, or consequence-bearing instruction in lock-screen/email subject/SMS preview unless product/legal evidence explicitly requires it.

A notification may carry an opaque non-secret routing reference. Opening it should land in a first-party context that still checks current entitlement/session. If the user is not currently entitled, authenticate/recover there. Do not let knowledge of case ID, push payload, email address or notification URL bypass 167.

Where a one-time bearer link is genuinely required, scope it narrowly, expire it, make it single-use/replay-resistant, bind it to the intended operation where feasible, prevent referrer/log leakage, and require additional current authorization before high-consequence mutation. Actual token architecture is an engineering handoff, not assumed here.

## Contact-channel change and compromise

Changing a notification address is itself security-sensitive because it can blind the legitimate user to future recovery/adjudication events. Generic governance:
- authorize the change at consequence-appropriate assurance;
- validate the new destination;
- notify surviving prior destination(s) when appropriate and safe;
- do not make a newly supplied destination during an ATO complaint automatically authoritative;
- preserve a repudiation/recovery route if an attacker changes the primary channel;
- model destination generation/currentness so delayed notifications to an old address cannot act as current authority.

If all normal channels are unavailable/compromised, fall back to the independent recovery/proofing route from 167. The support channel can facilitate recovery but cannot self-authorize a new destination and adjudicate the underlying policy case in one unchecked step.

## Support impersonation containment

Support/social engineering is a protocol-boundary problem, not just user education. The official system should make genuine support behavior structurally distinguishable:
- publish stable first-party support entry points;
- never ask users to disclose passwords, recovery codes, passkeys/private keys or authenticator-binding secrets to support;
- do not ask users to approve an unsolicited MFA/passkey/authenticator action merely to `verify` support contact;
- let suspicious recipients independently navigate to the official app/site rather than requiring trust in a message link or caller-provided number;
- separate support identity from adjudication/mutation authority;
- record consequential support-assisted changes and independently notify where appropriate;
- rate-limit and review support-assisted recovery abuse without making support persuasion an identity factor.

A message saying `call this number now` can itself be attacker-controlled. For high-risk events, prefer an independently discoverable official route and in-product status.

## PWA / iPadOS / offline implications

Web Push is useful but cannot be assumed available or timely. On iOS/iPadOS it is for Home Screen web apps and requires user permission/direct interaction; the OS controls display and users can disable notifications. Lock-screen visibility creates privacy risk. Push services can retain messages for later delivery according to TTL, so an authentic notification can be stale by the time an offline iPad reconnects.

Therefore:
1. do not require push to preserve access to a redress case;
2. push payload contains no current mutation authority;
3. notification click resolves current server authority outside cached Service Worker state;
4. stale notification after case correction/closure displays current status, not cached message truth;
5. locally preserved unsynced flight data remains independent from notification/session failure;
6. badge count is attention state, not evidence of case count/currentness;
7. multiple Home Screen installs/subscriptions must not be assumed to map 1:1 to a person or managed device;
8. actual managed-iPad notification policy, Focus/lock-screen behavior, MDM restrictions and WebKit version remain OPEN.

## MINTTAP DECISION — generic governance

1. External notification channels carry minimal signals; authoritative sensitive status lives in an authenticated first-party status surface.
2. A notification URL/case reference is not authorization. Avoid bearer authority where ordinary authenticated navigation suffices.
3. Treat contact destinations as lifecycle-managed security objects with validation, generation/currentness, change notification and compromise/recovery handling.
4. Maintain at least conceptual channel redundancy for high-consequence recovery; exact product channel requirements remain OPEN.
5. Support cannot request secrets or turn a persuasive interaction into identity, delegation or adjudication authority.
6. Provide an independently discoverable official route for suspicious notifications/support contact.
7. Push/email/SMS delivery telemetry is operational evidence only; it does not prove the intended human received/read the message.
8. PWA push is optional attention delivery, never the sole redress/status/recovery path; stale/offline delivery must resolve current state.
9. Minimize notification/analytics payloads and lock-screen disclosure. Do not replicate privileged case reasons into delivery providers unnecessarily.
10. Keep actual channels, templates, providers, tokens, IdP, managed-iPad policies, legal notice requirements and human phishing evidence OPEN until verified.

## VALIDATION — 104-case destructive campaign

1 minimal email subject; 2 minimal SMS; 3 minimal push lock-screen text; 4 no sensitive reason in preview; 5 no identity document data; 6 no recovery secret; 7 no bearer mutation credential; 8 opaque routing reference; 9 reference alone grants nothing; 10 unauth click requires entitlement; 11 cross-account deep link denied; 12 old case link resolves current state; 13 corrected case supersedes old notification; 14 closed case handles old click; 15 single-use token replay denied if token used; 16 token expiry; 17 brute force; 18 referrer leakage; 19 server logs do not retain secrets; 20 trusted origin construction; 21 host-header injection test; 22 phishing domain lookalike; 23 support asks for password — policy rejects; 24 support asks recovery code — rejects; 25 support asks unsolicited MFA approval — rejects; 26 caller-provided number not sole verification route; 27 independently navigated official support route; 28 support authenticated; 29 support cannot adjudicate by default; 30 support-assisted mutation independently logged/notified; 31 old email compromised; 32 old phone recycled; 33 new destination validation; 34 old destination notified when safe; 35 attacker changes contact; 36 victim has repudiation path; 37 all channels unavailable; 38 independent recovery path; 39 newly supplied channel not instantly trusted in ATO case; 40 multiple destinations; 41 one destination bounces; 42 provider outage; 43 provider delayed delivery; 44 provider duplicate delivery; 45 provider ACK without user receipt; 46 provider compromise; 47 template injection; 48 header injection; 49 notification flooding; 50 per-account throttling; 51 shared fleet/IP not globally blocked; 52 unsubscribe/permission revoked; 53 push permission denied; 54 push permission later removed; 55 iPad offline; 56 TTL expires; 57 stale push delivered later; 58 current server state wins; 59 SW stale; 60 SW cannot mint authority; 61 notificationclick with old client; 62 IndexedDB old case state; 63 current authority revalidated; 64 multiple Home Screen installs; 65 subscription rotation; 66 device lost/revoked; 67 old subscription cannot mutate; 68 Focus suppresses visibility; 69 lock-screen preview hidden; 70 notification absent but in-app status accessible; 71 badge stale; 72 badge not authority; 73 keyboard status navigation; 74 screen-reader status announcement; 75 focus not stolen by routine update; 76 zoom/reflow; 77 text spacing; 78 reduced motion; 79 forced colors; 80 plain-language phishing warning; 81 localization does not reveal extra data; 82 RTL layout; 83 email client strips styling; 84 SMS truncation; 85 push truncation; 86 offline status page retains local draft; 87 unique unsynced flight data preserved; 88 channel failure does not delete draft; 89 contact-change race; 90 concurrent channel updates; 91 stale PITR restores old contact; 92 current contact generation wins; 93 export contains old notification ref; 94 import does not restore authority; 95 analytics records delivery class not sensitive reason; 96 marketing profile does not ingest case payload; 97 retention of provider delivery logs bounded; 98 repudiation creates new review event not silent rollback; 99 legal-required notice conflict escalated; 100 managed-device notification restriction OPEN; 101 independent Safari/iPad test OPEN; 102 screen-reader/human phishing test OPEN; 103 actual provider/IdP/token implementation OPEN; 104 actual MintTap/LogMate legal/product model OPEN.

## OPEN / CHANGE WATCH

OPEN: actual MintTap/LogMate login/account model; notification channels/providers/templates; email/SMS ownership validation; Web Push use; token/deep-link design; IdP/session behavior; support workflow; managed-iPad/MDM notification policy; Focus/lock-screen configuration; jurisdiction-specific mandatory notices; human phishing/usability evidence; physical Safari/iPad behavior.

CHANGE WATCH: NIST SP 800-63 Rev.4 errata/implementation resources; Apple/WebKit Web Push and Declarative Web Push behavior; Push/Notifications/Badging standards; provider anti-phishing/security features; browser URL/deep-link behavior.

## Adjacent next question

The next high-value Stage-8/PWA boundary is **redress case confidentiality across delegated/representative access, shared/managed devices and support collaboration**: notification integrity still leaves the problem of who may see which explanation/evidence when a representative, employer-managed device, shared endpoint or support operator participates, without turning device ownership/support access into subject authority or leaking unrelated case history.