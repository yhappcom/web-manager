# 170 — PWA Delegation Lifecycle Recovery, Authority Conflict & Offline Reconciliation

Status: **PASS (generic) / PRODUCT + IDP + DELEGATION + EMPLOYMENT/ORG + MDM + LEGAL + HUMAN/AT + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A session/SW/storage/reconnect mechanics; Track B acting-for/conflict/recovery UX; Track C destructive authorization/accessibility/device validation; Track D privacy-bounded aggregate measurement.  
Dependencies: 167 identity/recovery; 168 notification/contact integrity; 169 delegated-case confidentiality.

## Why this study exists

169 established that confidentiality follows a current subject–case–capability–purpose relationship rather than device ownership or a coarse representative role. The next failure is temporal: a subject or delegate can recover an account; employment or organization membership can end; multiple delegates can issue incompatible requests; a delegation can be revoked then renewed; and a managed iPad can remain offline across several authority generations.

Central rule:

> **Recover identity without silently recovering stale delegation. Re-establish current relationship authority separately, arbitrate conflicting consequence-bearing actions against authoritative generations, and preserve unique local operational data even when remote mutation authority is lost.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Session cookies, WebAuthn/passkeys, SW/cache/IndexedDB and reconnect behavior can carry stale state but cannot establish current human/organizational delegation.
- **B UX/IA/Content:** very high dependency pressure. Must expose who is acting for whom, current/pending/revoked relationship state, conflicts and safe recovery without requiring users to understand generations or cryptographic terminology.
- **C Quality/Accessibility:** high dependency pressure. Owns destructive recovery/revocation/race/offline/device/AT tests and verifies that stale UI cannot become authority.
- **D Search/Analytics:** bounded consumer. May measure aggregate recovery/conflict quality but must not build durable representative/employment graphs from case telemetry.
- **E Security/Operations:** **bottleneck/owner**. Owns authority generations, recovery boundaries, conflict arbitration, revocation/renewal semantics, organizational change and reconciliation governance.

## SOURCE

### NIST SP 800-63B-4 — authenticator lifecycle, recovery and session separation

The final SP 800-63B-4 (published 2025-08-26) treats authentication as proof that a claimant controls authenticators bound to a subscriber account, and separately covers authenticator event management, recovery and session management. It also requires redress mechanisms to be findable and usable. A successful account recovery can therefore restore account authentication capability; it does not by itself prove that every external relationship or delegated business authority formerly attached to that account is still current.

NIST also distinguishes session secrets from authenticators and requires reauthentication/session lifecycle controls. This supports invalidating or re-evaluating consequence-bearing sessions after material recovery/authority changes rather than treating a recovered account as continuity of every prior session.

Source: https://pages.nist.gov/800-63-4/sp800-63b.html

### W3C WebAuthn Level 3 — scoped strong authentication, not business delegation

Web Authentication Level 3 became a W3C Recommendation on 2026-08-25. WebAuthn public-key credentials are scoped to a relying party and allow strong authentication with user-agent mediation and user consent. This is evidence about authentication capability, not proof of employment, guardianship, representative status, case scope or current delegation.

Source: https://www.w3.org/TR/webauthn-3/

### OWASP Session Management — lifecycle events require session control

OWASP session guidance treats authentication/session state as security-sensitive lifecycle state and recommends invalidating/renewing session identifiers around privilege changes and other material transitions. Transfer: a delegation/recovery generation change must not leave an old browser session as an unreviewed bridge to superseded authority.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

### Apple Shared iPad / managed-device evidence — device lifecycle and user lifecycle are distinct

Apple documents Shared iPad as a multiuser deployment with per-user protected storage; Temporary Session data is deleted when the guest signs out. Apple also documents device-management modes where the device itself, rather than a named user, is the managed object. Therefore company ownership, supervision, MDM enrollment or persistence of an on-device account cannot be promoted into current LogMate representative authority.

Sources:
- https://support.apple.com/guide/security/secd99f373ef/web
- https://support.apple.com/guide/deployment/depa60247ff8/1/web/1.0

TRANSFER VALIDATION: these Apple facts bound device/user separation only. Actual Safari/Home Screen storage, Shared iPad, MDM, account-switch and LogMate behavior remain OPEN until physical product evidence exists.

## SYNTHESIS — separate six generations

A durable model should not collapse these into one `user version`:

1. **Identity/account generation** — who can currently authenticate as the account.
2. **Authenticator/session generation** — which authenticators and sessions remain accepted after recovery or compromise.
3. **Relationship/delegation generation** — whether actor A may currently act for subject S, for what scope and capability.
4. **Organization/employment generation** — current organizational relationship where product/legal policy makes it relevant.
5. **Case/decision generation** — current case state and consequence-bearing decision lineage.
6. **Device/offline-state generation** — what a particular client last observed; never authoritative merely because it is locally newer by clock.

Persistent guards:
- `account recovered ≠ delegation recovered`;
- `authenticator rebound ≠ representative relationship renewed`;
- `employment active once ≠ employment active now`;
- `same email ≠ same authority generation`;
- `same Managed Apple Account ≠ same LogMate delegation`;
- `device still managed ≠ user still authorized`;
- `revoked then renewed ≠ old grant resurrected`;
- `renewal ≠ revocation cancellation`; renewal creates a new generation;
- `multiple valid delegates ≠ every combination of their actions is semantically compatible`;
- `offline action authored while authorized ≠ action still authorized at commit time`;
- `later device timestamp ≠ later authoritative intent`;
- `queued mutation preserved ≠ queued mutation executable`;
- `remote authority lost ≠ unique local operational data should be destroyed`.

## Account recovery — restore authentication, then re-evaluate delegation

Recovery should be capability-specific. A recovered subject account may regain access to its own current case surface after the required authentication/recovery checks. A recovered representative account must not silently reacquire all pre-recovery delegations merely because its account identifier is unchanged.

For sensitive consequence-bearing delegation, evaluate current relationship evidence and product/legal policy after recovery. If a representative account was compromised, surviving sessions/authenticators and pending delegated operations may need revocation or step-up/review. Do not let a compromised pre-recovery session approve its own successor authority.

A recovery event should create a new authentication/session generation. Whether existing delegations survive, suspend pending review or terminate is a product/legal policy decision; generic research does not invent that answer. The invariant is that the decision is explicit and current, not accidental inheritance.

## Organization/employment change

Employment, airline assignment, contractor status, guardian status or organizational membership can be inputs to delegation only where the actual product/legal authority says so. An IdP/MDM assertion that a person is a current employee can be useful evidence but is not automatically authority over a subject's case.

When a relevant organizational relationship ends:
1. stop deriving new authority from the stale relationship;
2. evaluate existing delegations according to their actual authority basis rather than deleting them blindly;
3. invalidate consequence-bearing queued actions that require the ended relationship unless independently authorized;
4. preserve audit/provenance and unique operational data;
5. prevent PITR/import/offline clients from restoring the superseded relationship generation.

## Revocation, renewal and re-delegation

Revocation is forward-looking termination of a grant generation. Renewal or re-delegation creates a new grant with new provenance/currentness, even if subject, delegate and scope appear identical. This prevents old invitations, cached tokens, exports or offline queues from becoming valid again merely because the same person later receives similar authority.

Use stable relationship identity only for history/correlation where justified; use generation-specific authorization for current decisions.

## Multiple delegates and authority conflict

Multiple delegates can each be valid yet issue incompatible actions. Authentication and authorization answer whether each actor could submit; they do not decide which business consequence wins.

Classify operations before conflict policy:
- **commutative/non-consequential** — e.g. add a non-conflicting note where product policy permits;
- **replaceable draft** — can preserve branches and require explicit selection;
- **consequence-bearing but compensable** — requires authoritative ordering and correction provenance;
- **irreversible/high consequence** — do not auto-resolve by last-write-wins or client timestamp.

If two authorized delegates submit conflicting consequence-bearing actions, route through current case/policy generation and the product's adjudication rule. Preserve both provenance records. `first received`, `last received`, `latest timestamp` and `highest device clock` are not generic semantic authority rules.

## Offline PWA / managed-iPad reconciliation

A long-offline PWA may reconnect after identity recovery, delegate revocation, employment change and re-delegation have all occurred.

Required generic behavior:
1. local drafts and unique flight/logbook records remain readable/exportable according to local product policy even if remote authority cannot be established;
2. cached delegation/session/case state is historical observation, not current authority;
3. reconnect obtains current server authority floor outside stale SW-controlled business state before consequence-bearing replay;
4. every queued delegated mutation carries enough provenance to identify actor, subject/case, delegation generation and operation identity;
5. if its delegation generation is superseded, quarantine/preserve the draft rather than silently replaying or silently deleting it;
6. re-delegation to the same actor does not make an old queued action valid automatically; explicit re-authorization/re-submission may be required;
7. Service Worker update, connectivity restoration or MDM presence does not itself reauthorize the queue;
8. device clock ordering is diagnostic only unless the domain explicitly defines it as authority;
9. duplicate reconnect/retry remains idempotent but idempotency does not resolve semantic conflict;
10. no generic assumption is made that iPadOS permits unattended background reconciliation; capability remains platform/product validation.

## Recovery/conflict UX requirements — Track B transfer

Users should see plain-language relationship state such as `Acting for …`, `Access ended`, `Access needs review`, `Draft saved locally — permission must be checked before submission`, and conflict choices where human adjudication is required. Avoid exposing internal generation IDs as the primary explanation.

Recovery must not create a dead end where the only way to challenge a revoked/incorrect relationship is through the revoked relationship itself. Conversely, alternate redress must not bypass identity/authorization controls established in 167.

For shared devices, sign-out/account switch must clear or hide sensitive case projections from the next user to the extent the product/platform controls them, while data-destruction policy for unique operational records remains separately governed.

## MINTTAP DECISION — generic governance

1. Treat identity recovery, session recovery, delegation recovery and organization/employment state as separate authorities.
2. Material recovery/relationship changes create new generations; do not mutate history to make continuity appear unbroken.
3. A recovered representative account does not automatically inherit every old delegation.
4. Revocation remains historical fact; renewal/re-delegation creates a new grant generation.
5. Authorize consequence-bearing operations against current server-side relationship/case/policy state, not cached PWA state or device clock.
6. Preserve stale/offline drafts for review where safe; do not auto-execute them after authority changes.
7. Preserve unique local operational data independently from remote mutation authority.
8. Multiple valid delegates require domain conflict policy; last-write-wins is not a generic authority rule.
9. Organization/MDM/IdP signals are inputs only where actual product/legal policy grants them meaning.
10. Actual LogMate representative/employer/airline/MDM authority and legal consequences remain OPEN.

## VALIDATION — 120-case destructive campaign

1 subject recovery clean; 2 representative recovery clean; 3 representative recovery after ATO; 4 old password/session denied; 5 old authenticator revoked; 6 surviving authenticator policy; 7 recovery code replay; 8 recovery notification; 9 subject recovery does not mint representative authority; 10 representative recovery does not mint delegation; 11 delegation survives only if explicit policy says so; 12 suspended delegation review; 13 expired delegation; 14 revoked delegation; 15 renewed delegation new generation; 16 old invitation replay; 17 old bearer link replay; 18 old export import; 19 PITR old delegation; 20 current authority floor wins; 21 same email reassigned; 22 renamed account; 23 merged identity; 24 split identity; 25 IdP account recreated; 26 Managed Apple Account recreated; 27 employee leaves; 28 employee rehired; 29 contractor ends; 30 organization transfer; 31 airline/tenant transfer; 32 MDM device reassigned; 33 device remains managed after user authority ends; 34 user remains authorized after device replacement; 35 lost device; 36 recovered device; 37 remote wipe OPEN; 38 Shared iPad account switch; 39 Temporary Session; 40 multiple representatives independent; 41 two representatives submit same idempotency key; 42 two different operations; 43 conflicting withdraw/appeal; 44 conflicting correction choices; 45 simultaneous revoke/submit; 46 simultaneous renew/submit; 47 subject revokes while delegate offline; 48 delegate reconnect after revoke; 49 same delegate reauthorized later; 50 old queue remains invalid; 51 explicit resubmission under new grant; 52 old draft preserved; 53 old draft clearly marked; 54 unique flight data preserved; 55 remote mutation blocked; 56 remote read scope changed; 57 cached explanation stale; 58 cached case stale; 59 stale SW; 60 stale IndexedDB; 61 Cache Storage; 62 browser history; 63 BFCache; 64 localStorage if used; 65 stale notification; 66 offline cold start; 67 long-offline multi-generation jump; 68 reconnect current authority fetch; 69 authority endpoint unavailable; 70 fail closed for mutation; 71 local data remains accessible/exportable; 72 duplicate reconnect; 73 retry after timeout; 74 ACK lost; 75 commit unknown; 76 idempotency does not mask conflict; 77 client clock ahead; 78 client clock behind; 79 device timezone change; 80 server clock issue; 81 policy generation change; 82 case generation change; 83 schema/API generation change; 84 relationship generation omitted from queue; 85 tampered relationship generation; 86 cross-account IDOR; 87 cross-tenant delegate; 88 support cannot renew delegation silently; 89 support cannot adjudicate silently; 90 emergency support expires; 91 legal/guardian authority OPEN; 92 deceased/incapacitated subject OPEN; 93 employment-law authority OPEN; 94 aviation retention/authority OPEN; 95 conflicting jurisdiction OPEN; 96 notification channel compromised; 97 contact channel changed during recovery; 98 phishing-resistant auth where required; 99 WebAuthn credential sync does not imply delegation sync; 100 passkey removed; 101 passkey added post-recovery; 102 session fixation; 103 privilege/session renewal; 104 CSRF on revoke/renew; 105 XSS attempts stale queue execution; 106 CSP/containment interaction; 107 audit provenance complete; 108 analytics excludes relationship graph payload; 109 logs minimize PII; 110 keyboard recovery flow; 111 screen-reader acting-for state; 112 focus after conflict; 113 zoom/reflow; 114 plain-language stale-draft warning; 115 localization; 116 RTL; 117 physical Safari/iPadOS OPEN; 118 Shared iPad/MDM physical OPEN; 119 actual LogMate roles/data model OPEN; 120 legal/security/privacy/human review OPEN.

## CONTRADICTIONS / failure modes resolved

- **Recovery continuity fallacy:** same account identifier after recovery does not prove same relationship authority.
- **Rehire resurrection:** rehiring/re-adding a person must not reactivate old revoked grants by identifier equality.
- **Offline authorship fallacy:** action authored while authorized is not automatically authorized when later submitted.
- **MDM authority inflation:** organization control of a device does not imply authority over every human case visible through it.
- **LWW authority bug:** latest timestamp cannot decide high-consequence representative conflicts generically.
- **Destructive containment bug:** loss of remote authority must not automatically destroy the only local operational record.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate account/tenant/delegation/employment model; authority basis; airline/company roles; IdP; passkey/authenticator model; MDM/Shared iPad policy; offline queue schema; local authoritative flight-data semantics; server conflict policy; legal/aviation requirements; physical Safari/Home Screen behavior; background execution; human/AT evidence.

DEPENDENCY: Software Engineering owns implementation architecture and executable authorization/session/queue/reconciliation tests. Its current M006 evidence proves bounded generic Chromium SW offline/restart/update/offline-cold-start behavior, not Safari/iPadOS/EFB or LogMate. Design Studio owns reusable acting-for/conflict/recovery interaction patterns; current Web status remains Stage 3 PRACTICE, not production PASS.

CHANGE WATCH: NIST 800-63-4 errata/updates; WebAuthn Level 3/4 evolution and browser support; Apple Shared iPad/Managed Apple Account/MDM behavior; Safari/WebKit PWA storage/session/background behavior; applicable employment/representative/privacy/aviation law.

## Adjacent next question

The next high-value boundary is **delegation provenance portability and cross-system federation**: if representative authority originates in an employer/airline/IdP or another service, determine how to consume assertions without converting transient organizational claims into permanent local authority, how revocation/currentness propagates across provider outages or migrations, and how offline PWA state remains usable without treating cached federation assertions as evergreen authorization.