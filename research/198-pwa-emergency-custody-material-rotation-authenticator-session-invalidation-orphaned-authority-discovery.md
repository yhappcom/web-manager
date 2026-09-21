# 198 — PWA Emergency-Custody Material Rotation, Authenticator/Session Invalidation & Orphaned-Authority Discovery

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + CRYPTO + PERSONNEL + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A PWA/browser session and offline-state boundaries; Track B personnel/custody state semantics; Track C destructive assurance; Track D privacy-bounded security telemetry.  
Dependencies: 183–197.

## Problem
197 established that emergency-custody succession is an authorization transition: successor readiness and former-custodian extinction are separate oracles. The next failure class is practical extinction. A departed or transferred custodian may have had access through several derived paths at once: an account, hardware/software authenticator, shared or exported secret, active browser/RP session, IdP session, refresh/access token, vault recovery route, provider support/recovery path, device credential, regional authorization cache, automation credential, or copied offline material.

No inventory can normally prove that an undiscovered copy does not exist. Conversely, uncertainty about copies must not force permanent paralysis. The generic security problem is therefore to move from **known material rotation** to **effective authority invalidation**, while explicitly preserving UNKNOWN where an authority path cannot be disproved or bounded.

Central rule: **inventory, rotation, authenticator invalidation, session invalidation and effective authorization extinction are separate properties. A retired custodian is extinct only to the extent that every consequential authorization path is either negatively proven unusable under the current authority model or explicitly bounded UNKNOWN.**

## Five-track balance
- **A Platform/Browser:** supplies browser cookie/session, Service Worker, Cache Storage and IndexedDB mechanics. Local browser state can preserve stale tokens/observations but cannot establish server-side authorization currentness or personnel eligibility.
- **B UX/IA/Content:** owns operator/user semantics for `ROTATION PENDING`, `SESSION INVALIDATION PENDING`, `ORPHANED AUTHORITY SUSPECTED`, `UNKNOWN`, `SUCCESSOR READY`, and `FORMER AUTHORITY EXTINCT`; Design Studio remains canonical for reusable interaction/human evidence.
- **C Performance/Accessibility/Quality:** owns destructive tests across authenticator/session/provider/cache/PITR/offline-client paths. Physical Safari/iPadOS, AT and representative-human execution remain OPEN.
- **D Search/Discovery/Analytics:** consumes coarse security outcomes only. Analytics is not the authoritative authority inventory and must not become a personnel-surveillance dossier.
- **E Architecture/Security/Operations:** **highest-risk owner**; owns authority-derivation inventory, invalidation graph, rotation boundary, negative authorization oracles, orphan discovery and UNKNOWN containment.

## SOURCE

### NIST SP 800-53 Rev.5 / SP 800-53A Rev.5 — account removal and shared-authenticator change are assessable lifecycle controls
SP 800-53 Rev.5 AC-2 links account management to termination/transfer and requires a process for changing shared/group authenticators when individuals are removed. SP 800-53A Rev.5 assessment objectives explicitly test account disable/removal and shared/group authenticator changes. Transfer: personnel change must propagate into effective access mechanisms rather than stop at an HR or directory record.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

### NIST SP 800-63B-4 — authenticator invalidation and session state are distinct
The current final SP 800-63B-4 was published in 2025 and supersedes SP 800-63B. It requires CSPs to promptly invalidate authenticators in specified lifecycle/compromise cases and distinguishes authenticator binding from authenticated sessions. It also states that IdP and RP sessions are independently managed in federation: ending one does not imply that the other ended. Access/refresh tokens can outlive an authentication session.

Sources:
- https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- https://pages.nist.gov/800-63-4/sp800-63b.html
- https://pages.nist.gov/800-63-4/sp800-63b/session/

**TRANSFER VALIDATION:** this directly supports the generic guard `authenticator invalidated ≠ every session invalidated`, and in federated architectures `IdP session terminated ≠ RP session terminated`. It does not prescribe MintTap's provider-specific revocation APIs or emergency-account topology.

## SYNTHESIS 1 — model an authority-derivation graph, not a credential checklist
A useful retirement model starts from the former custodian and follows every known way authority could remain effective.

Representative nodes/edges include:
1. **identity/account** — directory/emergency/provider-local account;
2. **authenticators** — passkey/security key/TOTP/certificate/device-bound credential/recovery code as applicable;
3. **authentication sessions** — IdP session, provider console session, RP/admin application session;
4. **delegated tokens** — access/refresh tokens or equivalent delegated credentials;
5. **shared material** — safe/vault combination, exported key, sealed secret, printed recovery material;
6. **provider recovery** — support, organization owner, billing/domain/email or provider-specific recovery routes;
7. **devices/endpoints** — managed/unmanaged devices with cached session or authenticator material;
8. **regional/control-plane caches** — authorization decisions, policy snapshots, offline verifiers;
9. **automation/non-human authority** — API credentials, CI/CD or service identities that a former custodian could still invoke or mutate;
10. **historical copies** — backup/PITR/export/escrow copies that could resurrect retired bindings.

The graph is architecture-dependent and must not be treated as complete merely because all expected rows are populated.

Persistent guards:
- `inventory complete according to schema ≠ no undiscovered authority exists`;
- `credential rotated ≠ derived sessions/tokens invalidated`;
- `account disabled ≠ provider recovery route disabled`;
- `IdP session terminated ≠ RP session terminated`;
- `device returned ≠ copied secret destroyed`;
- `vault access removed ≠ previously exported material unusable`;
- `region policy updated ≠ every cached authorization decision updated`;
- `primary DB corrected ≠ PITR cannot resurrect retired authority`.

## SYNTHESIS 2 — rotation is strongest when old material loses server-side meaning
Where feasible, extinction should depend on current authoritative verification/admission state rather than confidence that every old byte was physically found and destroyed.

Examples at the generic level:
- remove/revoke the old authenticator binding;
- advance a key/policy/generation so old signed or encrypted authority material cannot authorize current operations;
- invalidate server-side sessions and token families where the architecture supports it;
- rotate shared material after affected personnel leave the authorized set;
- revoke provider-local recovery routes or ownership roles;
- advance regional/currentness floors so stale cached authority is rejected;
- reconcile backups/PITR against the surviving retirement floor before reopening consequence-bearing paths.

This does **not** mean all old data should become unreadable. Historical evidence may need old verifier context. Historical verification and reusable current authority remain separate.

**MINTTAP DIRECTION:** prefer authority designs where personnel retirement can invalidate the *binding or acceptance condition* centrally/cryptographically without relying solely on locating every copied secret. Exact cryptographic/provider implementation remains OPEN.

## SYNTHESIS 3 — sessions require their own extinction campaign
Authenticator rotation does not necessarily terminate sessions already established from that authenticator. NIST's current federation guidance makes the separation especially explicit: IdP and RP sessions are independently managed, and an RP decides whether its reauthentication requirements are met.

A generic session-extinction campaign therefore asks separately:
- Are IdP sessions terminated?
- Are provider-local/admin sessions terminated?
- Are application/RP sessions terminated?
- Are refresh-token or equivalent token families invalidated?
- Can an already-issued access token still perform a consequence-bearing action until expiry?
- Can a regional cache continue to accept a retired session?
- Can a PITR restore old session/refresh-token validity?
- Does a browser/PWA retain a stale secret that the server still accepts?

If a token cannot be actively revoked, residual validity is a bounded risk interval, not instant extinction. Exact provider semantics and maximum residual windows are **OPEN** until verified.

## SYNTHESIS 4 — orphaned-authority discovery is an ongoing assurance problem
An **orphaned authority** is a consequence-bearing path that remains effective after the person/role/material that justified it should have been retired, or whose current owner/justification can no longer be established.

Discovery signals can include, depending on the architecture:
- provider/IAM account and authenticator enumeration;
- session/token inventory where exposed;
- vault/share/recovery-role review;
- device/MDM inventory;
- cloud/provider organization-owner and support-recovery review;
- certificate/key/API credential inventory;
- region/policy generation reconciliation;
- backup/PITR resurrection tests;
- audit evidence showing use by a retired identity/material;
- negative authorization probes using retired fixtures/credentials;
- comparison between HR/role roster, custody roster and effective provider authorization.

But discovery evidence has asymmetric meaning. Finding an orphan proves a defect. Finding none proves only that the exercised discovery surfaces found none.

Persistent guard: **`scan found zero orphaned authorities ≠ orphaned authority impossible`.**

Use an explicit disposition for each material/path:
- **INVALIDATED** — current negative oracle establishes it cannot authorize the scoped action;
- **EXPIRED/BOUNDED** — cannot be actively revoked but residual validity is bounded by verified semantics;
- **HISTORICAL-ONLY** — retained solely to verify history, isolated from current admission;
- **UNKNOWN** — effective authority cannot yet be disproved or bounded;
- **CURRENT** — intentionally authorized under current policy.

Do not collapse UNKNOWN into INVALIDATED for reporting convenience.

## SYNTHESIS 5 — UNKNOWN needs containment, not automatic global shutdown
Unknown copied material is common in real succession scenarios. The response should be proportional to what the unknown material could still authorize.

Generic containment questions:
1. What exact actions could this material perform if it survived?
2. Does current server policy still accept it?
3. Can the acceptance floor/key/binding be advanced without destroying unique data or historical verification?
4. Can high-consequence actions be frozen while lower-risk read/export/local work continues?
5. Is there a bounded expiry after which the material loses meaning?
6. Can independent negative probes reduce UNKNOWN to INVALIDATED?
7. What evidence is required before normal operation resumes?

This preserves the established rule that availability pressure must not lower a security/currentness floor simply to accommodate stale clients or uncertain authority.

## SYNTHESIS 6 — PWA/browser storage is observation/local-work state, not personnel authority
A PWA can retain cookies, IndexedDB state, Cache Storage content, Service Worker code and application records. Exact persistence and browser behavior vary by platform and remain a CHANGE WATCH, especially on iOS/iPadOS.

For the LogMate-like EFB case, a company iPad that was offline during personnel/custody rotation may return with:
- a stale user/custodian label;
- old policy/custody generation;
- an application session or token;
- queued consequence-bearing operations;
- unique unsynchronized flight/logbook records.

Generic convergence sequence:
1. preserve unique local domain records before destructive cleanup;
2. quarantine stale authentication/custody observations from current authority decisions;
3. obtain current authenticated server policy/custody/security generation;
4. let the server evaluate any retained session/token under current policy rather than trusting local age/labels;
5. reauthenticate/rebootstrap when required;
6. separate already-acknowledged history from local-only work;
7. re-admit consequence-bearing queued work under current authority;
8. clear or retire obsolete local authorization artifacts only after unique-data preservation requirements are satisfied.

**MINTTAP DIRECTION:** an offline EFB/PWA must never be used as proof that a former employee remains authorized merely because it has a valid-looking cached session. Likewise, forced logout/data cleanup must not erase unique unsynchronized operational records.

## SYNTHESIS 7 — positive and negative oracles remain independent
Strong succession evidence includes both:
- **positive successor oracle:** authorized successor can retrieve/use the intended emergency path under current policy;
- **negative former-authority oracle:** retired account/authenticator/session/provider-recovery/material cannot perform representative consequence-bearing operations.

Negative testing should cover the architecture's distinct authority surfaces rather than replaying one failed login. A failed old password does not prove an old browser session, refresh token, provider support route or regional cache is dead.

Where destructive testing against real emergency authority is unsafe, use bounded fixtures/staging/provider-supported revocation evidence plus carefully scoped production-negative checks. Reading alone cannot close production validation.

## SYNTHESIS 8 — privacy and personnel boundaries
Orphan discovery can easily become excessive employee surveillance. The security purpose is authority retirement, not behavioral profiling.

Generic minimization direction:
- collect identity/role/material/path/status/generation/time evidence needed to establish authorization state;
- avoid retaining unrelated browsing/content/location history merely because an emergency-access investigation exists;
- separate security/audit evidence from analytics;
- limit custody/evidence access;
- retain historical attribution only as required for interpretation/accountability;
- apply applicable retention/deletion/legal rules rather than inventing indefinite personnel dossiers.

Track D therefore remains a bounded telemetry consumer, not the authority oracle.

## Track C destructive campaign — 344 cases total
Add eight high-value cases to the 336-case campaign:
1. former authenticator invalidated but an RP/admin browser session remains effective;
2. IdP session terminated but provider-local/RP session survives and performs a privileged action;
3. refresh-token family survives account/role retirement and mints a new access token;
4. shared emergency material rotates but a provider support/recovery route still recognizes the former custodian;
5. primary region rejects retired authority while a stale regional authorization cache accepts it;
6. PITR restores a retired authenticator/session binding and consequence-bearing admission resumes before reconciliation;
7. orphan scan reports zero findings while a deliberately seeded hidden fixture remains usable, demonstrating detection-coverage limits;
8. long-offline iPad returns with unique unsynced records plus a stale former-personnel session; data survives while authorization is rejected/rebootstrapped.

Campaign status: **DEFINED, NOT EXECUTED**. Physical iPad/Safari/Home Screen, AT, human UX, provider/IAM and canonical product-runtime validation remain OPEN.

## Cross-track transfer / contradiction checks
### A → E
Browser/session mechanics support stale-state analysis. **CONTRADICTION:** browser-local deletion alone cannot prove server-side session/token invalidation.

### E → B
B should expose pending/UNKNOWN states without implying compromise certainty. `Former authority extinction pending` is not the same as `former employee malicious`.

### E → C
C must test multiple derived authority paths. One failed login is insufficient negative evidence.

### E → D
Security telemetry may indicate invalidation status and anomalous retired-authority use, but analytics must not become admission authority or a shadow personnel dossier.

### Software Engineering dependency
Concrete implementation needs provider/API-specific state machines for account/authenticator/session/token invalidation, generation/floor enforcement, regional convergence, PITR reconciliation and negative authorization tests. Software Engineering Studio remains Foundation-stage; no implementation PASS transfers here.

### Design Studio dependency
Design Studio Web remains Stage 3 PRACTICE / NOT PASSED with physical-device/PWA, screen-reader and representative-human validation OPEN. Reusable UX for forced reauthentication, unique-local-data preservation and authority-UNKNOWN states remains a Design Studio execution dependency.

## OPEN
- actual MintTap/LogMate identity provider and emergency-access topology;
- whether sessions/tokens are stateful, revocable, short-lived or provider-managed;
- actual account/authenticator/session/token/provider-recovery inventory surfaces;
- actual shared-secret/key/vault/device custody model;
- actual regional authorization cache and convergence behavior;
- actual backup/PITR treatment of identity/session state;
- actual managed-iPad/WebKit storage/session behavior;
- actual personnel/HR integration and legal/retention obligations;
- exact cryptographic/key-generation design and hardware custody;
- acceptable residual validity intervals and high-consequence action classification.

## CHANGE WATCH
- NIST SP 800-63B-4 remains the current final authentication/authenticator/session baseline as of this study; provider implementations may differ materially.
- WebKit/iPadOS PWA storage/session/background behavior remains platform-sensitive.
- Provider-specific global sign-out, refresh-token revocation, passkey/security-key removal and support-recovery semantics must be re-verified when a provider is selected or changed.

## Gate judgment
**PASS (generic).** The Web Manager can now distinguish material rotation from effective authority extinction, model authority derivation beyond a credential list, reason about independent authenticator/session/federation/provider-recovery invalidation, discover orphaned authority without treating inventory as proof of absence, preserve UNKNOWN honestly, and apply the model to long-offline PWA/EFB convergence.

This is not production certification. Product/provider/runtime/personnel/crypto/privacy/physical-device/human evidence remains OPEN.

## Next highest-value adjacent work
**PWA orphaned-authority containment expiry, revocation propagation & convergence proof across federated/provider/region boundaries.** Determine how to prove retirement state has propagated far enough across independent RPs/providers/regions; how to handle non-revocable short-lived authority without claiming immediate extinction; how to define convergence evidence without requiring impossible proof of every hidden copy; and how offline PWA clients rejoin after the retirement floor has advanced.