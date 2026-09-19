# 167 — PWA Redress Identity, Authorization & Anti-Abuse Without Exclusion

Status: **PASS (generic) / PRODUCT + IDENTITY-PROVIDER + LEGAL + HUMAN/AT + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track B redress UX; Track C accessibility/abuse validation; Track A session/offline/currentness mechanics; Track D aggregate abuse/workflow measurement.  
Dependencies: 093 session/offline authorization, 094 account/device/key recovery, 111 recovery authority abuse resistance, 155–166 recovery/policy/redress lineage.

## Why this study exists

166 establishes that consequential policy decisions need usable explanation and correction paths. The adjacent security failure is to make the redress path either too weak or too strong: an account-takeover attacker/support impersonator/bot can enumerate or mutate sensitive policy state, or legitimate users are excluded because the redress system demands excessive identity evidence, inaccessible cognitive tests, unavailable devices, or impossible recovery credentials.

Central rule:

> **Redress access is a consequence-scoped authorization problem, not a universal demand for maximum identity proofing. Authenticate/prove only enough for the requested redress capability, minimize disclosed identity attributes, keep enumeration/automation resistance separate from adjudication authority, and preserve an accessible recovery path when ordinary authenticators are unavailable.**

## Five-track balance and allocation

- **A Platform/Browser:** dependency supplier. Owns browser session/authenticator/SW/offline mechanics; cached session or device possession alone does not establish current redress authority.
- **B UX/IA/Content:** high dependency pressure. Owns discoverable challenge/recovery path, progressive proofing, non-leaky status, representative flows and accessible fallback semantics.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns abuse, enumeration, lockout, CAPTCHA/cognitive burden, password-manager/paste, keyboard/AT, stale-session and offline-device tests.
- **D Search/Discovery/Analytics:** bounded consumer. May measure aggregate abuse/failure/abandonment but cannot become identity evidence, adjudication authority or a subject-level fraud dossier.
- **E Architecture/Security/Operations:** **bottleneck/owner**. Owns capability-scoped authorization, assurance escalation, anti-enumeration, throttling/anti-automation, representative delegation boundaries, recovery, privacy minimization and incident separation.

## SOURCE

### NIST SP 800-63 Revision 4 — current final digital identity baseline

NIST finalized SP 800-63 Revision 4 in July/August 2025. SP 800-63-4 frames digital identity risk management as selection of usable, privacy-enhancing security and anti-fraud controls and explicitly includes risks introduced by the identity system itself. SP 800-63A-4 requires redress mechanisms for identity-proofing failures/difficulties and compromised-account recovery to be easy to find/use and assessed for efficacy.

Sources:
- https://pages.nist.gov/800-63-4/
- https://pages.nist.gov/800-63-4/sp800-63.html
- https://pages.nist.gov/800-63-4/sp800-63a/ial-general/

NIST 63A-4 also requires privacy risk assessment and limits processing to the minimum personal information needed for proofing/fraud/authorization purposes. Its privacy guidance warns that unsuccessful proofing should provide a remedy without disclosing failure specifics that would help fraudulent applicants learn which personal facts are correct.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63a/privacy/
- https://pages.nist.gov/800-63-4/sp800-63a/proofing/

### NIST SP 800-63B-4 — authentication and abuse controls

63B-4 requires rate limiting for relevant low-entropy authenticators, recognizes additional bot/risk controls, and warns that controls should reduce the chance an attacker can lock out a legitimate claimant. It defines phishing resistance as a protocol property rather than user vigilance; manual OTP/OOB entry is not phishing-resistant. Physical-authenticator loss/compromise requires a mechanism to invalidate it.

Sources:
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/
- https://pages.nist.gov/800-63-4/sp800-63b.html

### W3C WCAG 2.2 — authentication must not create avoidable cognitive exclusion

WCAG 2.2 SC 3.3.8 Accessible Authentication (Minimum), Level AA, disallows requiring a cognitive-function test in an authentication step unless an allowed exception/alternative/mechanism exists. W3C explicitly cites password-manager support and copy/paste as mechanisms; its understanding guidance says account recovery/change paths also need a non-cognitive-test method. WebAuthn/device authentication is given as an accessible pattern. SC 3.3.9 strengthens this at AAA.

Sources:
- https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum
- https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html

### OWASP authentication transfer evidence

OWASP Authentication Cheat Sheet recommends generic authentication/recovery responses so differences in account existence/lock state do not create an enumeration oracle. This is security guidance, not a requirement to make post-authenticated redress explanations vague.

Source:
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

## SYNTHESIS — separate five questions

Do not collapse these into one `identity verified` boolean:

1. **Subject resolution** — which account/record/decision is being challenged?
2. **Claimant authentication/proofing** — what evidence says this actor is entitled to act for that subject?
3. **Capability authorization** — may this actor view an explanation, submit a contest, upload evidence, change identity/account data, or authorize a consequence-bearing mutation?
4. **Abuse/fraud confidence** — is this request automated, enumerative, coerced, socially engineered or otherwise suspicious?
5. **Adjudication authority** — who/what may decide the challenged policy outcome?

Persistent guards:
- `authenticated account ≠ authority over every redress capability`;
- `identity proofed once ≠ current session authorized for high-consequence mutation`;
- `device possession ≠ person identity ≠ representative authority`;
- `support agent authenticated ≠ support agent may adjudicate`;
- `fraud score high ≠ claimant proven fraudulent`;
- `rate limited ≠ redress right extinguished`;
- `bot challenge passed ≠ identity proven`;
- `CAPTCHA passed ≠ authorization granted`;
- `generic pre-auth response ≠ vague post-auth explanation required`;
- `more identity evidence ≠ proportionately safer`;
- `offline session authentic historically ≠ current redress authority`.

## Capability ladder — proof proportionate to consequence

Generic capability classes, not product enums:

- **Public/discovery:** find redress/recovery instructions without authentication.
- **Low-disclosure intake:** initiate a request using an opaque reference or contact route without revealing whether a sensitive subject/policy record exists.
- **Authenticated explanation:** inspect a scoped explanation for a decision already associated with the authenticated subject.
- **Contest submission:** challenge that decision and attach bounded evidence.
- **Sensitive identity correction / representative binding:** stronger proof may be needed because the operation changes attributes or delegates authority.
- **Consequence-bearing disposition:** deletion/retention/authority changes remain under the policy/adjudication controls from 164–166; claimant authentication never substitutes for adjudication.

Do not choose an assurance level by habit. Start with harm if the wrong actor receives/changes the specific capability, then select the least burdensome evidence that mitigates that risk. Actual MintTap/LogMate assurance requirements remain OPEN.

## Anti-enumeration and useful explanation are compatible

Before entitlement is established, responses should avoid confirming sensitive account/decision existence through prose, status code, timing, email behavior or redirect differences. After entitlement is established, 166's meaningful explanation requirement applies.

`generic pre-auth response` is therefore an information-boundary control, not a justification for telling a legitimate authenticated user nothing.

Where asynchronous intake is used, request identifiers should be opaque and non-enumerable. A request lookup should require current entitlement; knowing an ID is not authorization.

## Anti-automation without denial-of-redress

Use layered controls rather than a single punitive CAPTCHA:
- rate limits by capability and risk, not only global IP;
- progressive delay/backoff where appropriate;
- replay/idempotency controls;
- bot/automation signals as risk evidence, not identity truth;
- abuse review for high-impact patterns;
- protected alternate channel when automated controls block a legitimate claimant;
- avoid permanent lockout from an attacker intentionally exhausting retry limits.

Do not treat IP/geolocation/device fingerprint as stable identity. Shared networks, VPNs, accessibility tooling and managed fleets make them weak or correlated signals.

## Accessibility and inclusion

Authentication/redress cannot rely on memory puzzles, transcription barriers or inaccessible CAPTCHA as the only path. Preserve password-manager/autofill/paste support and an alternative that does not require the same unavailable authenticator when recovery is the purpose.

A secure fallback can still require meaningful evidence; accessibility does not mean bypassing authorization. Conversely, security does not justify a workflow that only a fully sighted, dexterous user with a remembered secret and second device can complete.

Track B should make escalation explicit: what additional evidence is requested, why it is needed, whether it is optional/mandatory, and what alternative path exists. Do not collect identity documents merely because a challenge is unusual.

## Representative / support boundary

A user may act through an authorized representative in some real contexts, but exact legal/product rules are OPEN. Generic architecture must distinguish:
- subject identity;
- representative identity;
- evidence of delegation/authority;
- scope and expiry of delegation;
- support/operator role;
- adjudicator role.

Support must not create delegation by editing a role field after a persuasive phone call. Representative authority should be scoped, reviewable and revocable; it should not silently become account ownership.

## Recovery and account takeover

Redress is especially sensitive when the complaint itself is `my account/authenticator was compromised`. Requiring the compromised session/authenticator as the only proof creates a dead end; automatically trusting a new email/phone supplied during the complaint creates an ATO path.

Recovery should:
1. separate contactability from identity/authority;
2. use surviving evidence/independent recovery controls proportionate to consequence;
3. invalidate/restrict compromised authenticators where established;
4. avoid exposing which evidence failed to an unauthenticated claimant;
5. create a new authority/session generation after recovery rather than reviving stale sessions;
6. preserve the ability to contest without letting the recovery channel adjudicate the policy decision.

## PWA / long-offline iPad

A company iPad can possess an old authenticated session, cached explanation and locally drafted contest while offline. That state can support local continuity but not current remote authority.

On reconnect:
1. preserve unique unsynced flight/user data;
2. authenticate/revalidate current session/authority outside cached SW state;
3. do not auto-submit consequence-bearing operations merely because they were queued under an old session;
4. a locally drafted contest may sync as a request after current admission checks;
5. if account/device trust was revoked while offline, quarantine remote mutation while keeping export/recovery available;
6. do not infer identity from MDM/device ownership unless actual product/MDM evidence establishes that contract;
7. do not require online-only redress UI to read/preserve local data needed to formulate a later challenge.

## Track D transfer — measure abuse without building a fraud dossier

Useful aggregate metrics can include challenge success/failure bands, abandonment, retry/lockout rates, recovery-channel usage, suspected automation rate and resolution latency. Avoid analytics as canonical identity evidence. Do not permanently join detailed adjudication evidence, device fingerprints and sensitive reason histories into a marketing/analytics profile.

## MINTTAP DECISION — generic governance

1. Model redress authorization per capability/consequence; do not use one universal `verified` flag.
2. Use the least identity proof necessary for the requested capability and perform privacy risk assessment before collecting additional evidence.
3. Separate pre-entitlement anti-enumeration from post-entitlement meaningful explanation.
4. Layer throttling/automation controls and preserve an accessible alternate path; attacker-induced lockout must not silently extinguish redress.
5. Support password managers/autofill/paste and avoid cognitive-function tests as the sole authentication/recovery path.
6. Keep support, representative delegation, identity recovery and adjudication as separate authorities.
7. A compromised-account complaint needs an independent recovery route; do not require the compromised authenticator as the only route or trust a newly supplied contact channel automatically.
8. Cached/offline PWA sessions and device possession never establish current remote redress authority; preserve unique local data during revalidation.
9. Keep fraud/abuse telemetry purpose-limited and aggregate where possible; do not make analytics the identity or policy authority.
10. Keep actual assurance levels, IdP/authenticator choices, representative rules, legal rights, MDM contracts and physical-device behavior OPEN until canonical product/runtime/legal evidence exists.

## VALIDATION — 96-case destructive identity/redress campaign

1 public redress route discoverable; 2 no account existence leak; 3 no decision existence leak; 4 equivalent status behavior; 5 timing discrepancy checked; 6 opaque request ID; 7 ID alone grants nothing; 8 authenticated user sees own scoped explanation; 9 cross-account IDOR denied; 10 old session rejected where currentness required; 11 low-risk intake avoids excess proof; 12 high-consequence action escalates; 13 escalation reason explained; 14 unnecessary document not collected; 15 proof data retention bounded; 16 privacy notice accurate; 17 password manager works; 18 autofill works; 19 paste works; 20 no sole memory puzzle; 21 no sole transcription challenge; 22 CAPTCHA alternative exists; 23 keyboard complete; 24 screen-reader labels/status; 25 zoom/reflow; 26 text spacing; 27 touch target; 28 timeout warning/recovery; 29 duplicate submit idempotent; 30 ACK lost; 31 retry does not duplicate contest; 32 per-account throttling; 33 per-network throttling does not block shared fleet; 34 attacker cannot permanent-lock victim; 35 backoff bounded; 36 automation signal not identity truth; 37 VPN does not prove fraud; 38 geolocation does not prove identity; 39 device fingerprint not sole identity; 40 bot challenge pass not authorization; 41 rate limit hit; 42 alternate legitimate path; 43 support can explain; 44 support cannot adjudicate; 45 support cannot bind representative informally; 46 representative identity separate; 47 delegation evidence scoped; 48 delegation expiry; 49 delegation revoke; 50 representative cannot become owner silently; 51 compromised account reported; 52 compromised authenticator not sole recovery route; 53 new email not automatically trusted; 54 surviving evidence evaluated; 55 compromised authenticator invalidated when established; 56 stale sessions retired; 57 recovery creates new generation; 58 recovery does not adjudicate underlying contest; 59 phishing-resistant path where consequence warrants; 60 manual OTP not mislabeled phishing-resistant; 61 push fatigue/rate considered; 62 failed attempts rate-limited; 63 successful auth resets appropriate retry state; 64 pre-auth failure detail minimized; 65 post-auth explanation remains meaningful; 66 identity provider unavailable; 67 local data still readable/exportable as authorized; 68 redress draft preserved; 69 offline iPad holds old session; 70 reconnect revalidates; 71 revoked device cannot remote-mutate; 72 device ownership not assumed person identity; 73 stale SW cannot mint authority; 74 IndexedDB auth state not authority floor; 75 queued contest requires admission; 76 queued deletion/disposition not auto-run; 77 unique unsynced flight data preserved; 78 service worker update does not equal auth refresh; 79 clock skew not identity proof; 80 PITR restores old session; 81 current revocation floor wins; 82 export contains old request token; 83 import cannot resurrect session; 84 analytics measures aggregate failures; 85 analytics not canonical identity; 86 sensitive evidence excluded from marketing profile; 87 fraud flag appeal/review path where applicable; 88 high risk score does not mark person fraudulent as fact; 89 abuse incident separated from policy adjudication; 90 third-party IdP compromise path; 91 representative/support compromise path; 92 forced-colors/reduced-motion applicable states; 93 independent browser validation OPEN; 94 physical Safari/iPad OPEN; 95 screen-reader/human validation OPEN; 96 actual MintTap/LogMate legal/product/identity model OPEN.

## OPEN / CHANGE WATCH

OPEN: actual MintTap/LogMate account model; whether LogMate PWA has login; IdP/CSP; authenticators/passkeys; session lifetime; assurance levels; representative/delegation needs; support roles; MDM/device identity contract; rate/anti-bot provider; identity-document handling; jurisdiction-specific redress identity rules; offline contest schema; physical iPad/WebKit behavior; AT/human evidence.

CHANGE WATCH: NIST SP 800-63 Rev.4 implementation/conformance resources; WCAG/WAI authentication techniques; browser/passkey/WebAuthn platform behavior; provider anti-bot behavior and accessibility.

## Adjacent next question

After identity/authorization/anti-abuse is bounded, the next high-value Stage-8/PWA question is **redress notification/contact-channel integrity, phishing-resistant status delivery & support-channel impersonation containment**: how to tell a claimant that a review/status/correction exists without leaking sensitive decision state through email/SMS/push, allowing spoofed support messages to steal recovery credentials, or making an unavailable/compromised contact channel the only path back to the case.