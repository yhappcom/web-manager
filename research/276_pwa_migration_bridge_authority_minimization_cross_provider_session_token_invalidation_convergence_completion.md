# 276 — PWA Migration-Bridge Authority Minimization, Cross-Provider Session/Token Invalidation & Convergence-Completion Proof

Status: **PASS (generic) / PRODUCT + IDP + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/session/offline rejoin mechanics; Track B truthful migration/recovery UX; Track C destructive validation; Track D bounded convergence diagnostics.  
Dependencies: 260–275 dependency/topology/re-entry/revocation/rotation/recovery/custody/provider-org migration governance.

## Problem

275 established that old/new custody or provider control planes can overlap without becoming co-equal authority. The next failure surface is the temporary migration bridge itself plus credentials that survive outside the visible migration path: browser sessions, refresh/access tokens, cookies, background credentials, service accounts, queued offline requests, recovery/admin sessions and provider-local grants.

A bridge that can translate or admit both generations can accidentally become a transitive super-authority. A migration can also appear complete while old credentials remain capable of producing material effects. Conversely, requiring every offline client to be online simultaneously can make safe closure impossible.

Central rule: **migration bridges must be consequence-bounded, generation-bounded, non-transitive and retireable; credential invalidation must be proved at consequence-bearing boundaries rather than inferred from one provider's logout UI; convergence completion means stale authority can no longer create material effects without current re-admission, not that every historical client is simultaneously online.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns browser cookie/session, Service Worker, storage and offline-return mechanics. Runtime state can retain stale credentials but cannot decide organizational authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `signed out/re-authentication required`, `records preserved`, `sync temporarily limited`, `migration complete centrally`, and `this device still requires re-admission` states.
- **C Performance/Accessibility/Quality:** destructive campaign expands **960 → 968 defined cases**. Execution, physical-device, AT and representative-human PASS remain OPEN.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures stale-generation attempts, invalidation/rejection outcomes, unknown/offline tail and bridge use; telemetry does not grant authority or prove absence merely from zero events.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns bridge authority bounds, cross-provider invalidation, stale-session containment, convergence closure, retirement and rollback resistance.

## SOURCE

### RFC 7009 — OAuth 2.0 Token Revocation

RFC 7009 defines a revocation mechanism for access and refresh tokens. A revocation request invalidates the token and, where applicable, other tokens based on the same authorization grant and the grant itself. The RFC also recognizes propagation delay between authorization and resource servers.

Source: https://www.rfc-editor.org/rfc/rfc7009

**TRANSFER VALIDATION:** OAuth revocation is a concrete protocol precedent for grant-linked invalidation and distributed propagation. It does not prove MintTap/LogMate uses OAuth or define the product's session topology.

### RFC 9700 — Best Current Practice for OAuth 2.0 Security

RFC 9700 describes refresh-token replay defenses, including refresh-token rotation or sender-constrained refresh tokens for public clients, and notes that authorization servers may revoke refresh tokens after security events such as logout or password change. Rotation can expose replay by invalidating the active refresh token when an invalidated predecessor is reused.

Source: https://www.rfc-editor.org/rfc/rfc9700.html

**TRANSFER VALIDATION:** this supports lineage-aware token invalidation and replay detection. It is not a requirement that every PWA adopt one specific OAuth token design.

### OpenID Connect Back-Channel Logout 1.0

OIDC Back-Channel Logout defines direct OP→RP logout communication. It is more independent of an active browser tab than front-channel logout, but the RP must implement application-specific termination of its local sessions and the back-channel endpoint must be reachable. A signed logout token identifies the relevant subject/session.

Source: https://openid.net/specs/openid-connect-backchannel-1_0.html

**TRANSFER VALIDATION:** logout signaling and local-session termination are distinct steps. A delivered logout event is not proof that every downstream/local credential or offline client has been neutralized.

### NIST SP 800-63B-4 — session management

NIST SP 800-63B-4 treats authenticated-session continuity as possession of a session secret and requires session termination at applicable timeout boundaries, with periodic reauthentication. Session lifetime depends on assurance, endpoint and application context.

Source: https://pages.nist.gov/800-63-4/sp800-63b.html

**TRANSFER VALIDATION:** this is bounded session-management precedent, not a universal MintTap/LogMate AAL determination or product timeout prescription.

## SYNTHESIS 1 — a migration bridge is a capability, not a new root

A bridge may temporarily translate identities, validate predecessor artifacts, map old provider subjects to new subjects, or permit bounded recovery. It must not silently gain every privilege held by both sides.

A useful bridge contract records:
- source generation/provider;
- destination generation/provider;
- allowed consequence classes;
- accepted artifact/session/token types;
- translation/revalidation rules;
- non-transitivity rule;
- start and expiry/retirement conditions;
- audit/provenance requirements;
- rollback/compromise response.

Guards:
- `bridge can read old + new ≠ bridge may authorize old + new`;
- `bridge can translate identity ≠ bridge can mint unrestricted authority`;
- `temporary bridge ≠ third permanent control plane`.

## SYNTHESIS 2 — bridge transitivity is an escalation hazard

If G7→G8 bridge output can be fed into G8→G9 as if it were native G8 authority, a chain of temporary bridges can launder obsolete authority forward indefinitely. Successor admission should distinguish native-current evidence from translated/historical evidence and require explicit revalidation for material consequences.

Guards:
- `A→B accepted ≠ A→B→C automatically accepted`;
- `translated identity ≠ native current authority`;
- `bridge output parseable by successor ≠ successor admission proven`.

## SYNTHESIS 3 — logout, token revocation and session invalidation are different surfaces

A user-visible logout can clear one browser state while refresh tokens, server sessions, other browser/device sessions, background credentials or provider grants remain active. Conversely, central token revocation may leave local offline data and UI state intact.

Therefore migration invalidation inventory should distinguish at least:
- browser/RP session cookie or equivalent;
- authorization-server session;
- access token;
- refresh token / grant family;
- device-bound or sender-constrained credential where used;
- background/service credential;
- recovery/admin session;
- queued operation carrying historical authorization context.

Guards:
- `logout UI completed ≠ all credentials invalidated`;
- `refresh token revoked ≠ already-issued access token impossible everywhere`;
- `IdP session ended ≠ RP/server session ended`;
- `local cookie cleared ≠ background credential retired`.

Actual product credential inventory remains OPEN.

## SYNTHESIS 4 — cross-provider invalidation needs a graph, not a single API call

During provider migration, old and new IdPs/control planes may each know only part of the credential graph. A revocation call to provider B cannot be assumed to invalidate provider A sessions; provider A logout cannot be assumed to terminate application-local sessions or independently issued background credentials.

Model invalidation as edges from authority/grant/session roots to derived credentials and material acceptance points. Closure asks whether obsolete roots can still reach a material effect.

Guard: `revoked at provider B ≠ unreachable through provider A`.

## SYNTHESIS 5 — authoritative rejection is the safety boundary for disconnected clients

Long-offline clients cannot reliably receive immediate logout/revocation events. Push, MDM, Service Worker update and back-channel events are useful accelerators where supported, but they cannot be the sole safety boundary for a device that is offline.

For material remote effects, the authoritative online boundary must reject obsolete generation/session/grant context or require current re-admission when the request eventually arrives.

Guards:
- `revocation event sent ≠ offline client received it`;
- `offline client still displays signed-in state ≠ server effect authorized`;
- `Service Worker updated ≠ credential graph invalidated`.

## SYNTHESIS 6 — invalidation should preserve unique offline data

Credential invalidation and local-data destruction are separate operations. A returning EFB-like PWA may contain irreplaceable flight/logbook records created while an old session was locally present. Reauthentication failure or obsolete authority should fence remote mutation/replay while preserving recoverable records and provenance according to product/domain policy.

Guards:
- `session invalid ≠ local record invalid`;
- `old token rejected ≠ queued payload deleted`;
- `re-auth required ≠ destructive sign-out`.

## SYNTHESIS 7 — completion is consequence closure, not fleet simultaneity

Migration can be centrally complete while some devices remain offline if obsolete authority is unable to create new material effects without current re-admission. Completion therefore needs a bounded definition such as:
1. successor authority/provider admitted;
2. current credential issuance works;
3. obsolete credential roots are revoked/retired where controllable;
4. material acceptance boundaries reject obsolete authority;
5. bridge cannot mint or transitively extend obsolete authority;
6. bridge retirement is effective at material boundaries;
7. backup/PITR cannot restore obsolete authority as current;
8. late clients rejoin through current admission/revalidation;
9. unknown/offline tail is measured and operationally bounded rather than declared nonexistent.

Guard: `100% devices online ≠ required for central closure`; equally, `99% migrated ≠ safe closure by itself`.

## SYNTHESIS 8 — zero stale events is weak negative evidence

No observed old-provider traffic may mean migration succeeded, or that old clients are offline, telemetry is incomplete, the bridge is unused, or a path is uninstrumented. Closure needs active negative tests and topology evidence at material boundaries, not silence alone.

Guards:
- `zero old-token events ≠ zero old tokens exist`;
- `dashboard quiet ≠ stale path impossible`;
- `telemetry coverage unknown ≠ convergence proven`.

## SYNTHESIS 9 — bridge retirement needs positive and negative proof

Deleting bridge configuration from a repository or disabling one endpoint is insufficient if cached jobs, old deployments, admin tools or recovery paths can still invoke equivalent authority.

Closure should demonstrate:
- successor/current path positive proof;
- bridge/predecessor negative proof at material boundaries;
- no ungoverned fallback that recreates bridge authority;
- rollback/PITR does not reactivate the bridge as current;
- historical bridge provenance remains verifiable where needed.

Guard: `bridge config removed ≠ bridge authority retired`.

## SYNTHESIS 10 — session/token currentness is not wall-clock freshness alone

An unexpired token can be obsolete because its grant, provider generation, subject mapping, custody generation or organizational authority has been retired. Conversely, an expired credential does not imply its historical actions or local data should be erased.

Guards:
- `token exp in future ≠ current migration authority`;
- `token expired ≠ historical provenance invalid`;
- `recently refreshed ≠ refreshed under current organizational generation`.

## SYNTHESIS 11 — partial convergence requires explicit UNKNOWN handling

If some credential/bridge acceptance surfaces cannot yet be verified, do not silently classify them NORMAL. Scope UNKNOWN to affected consequences and preserve safe capabilities. A migration may remain operationally usable in a bounded mode while high-consequence effects wait for stronger proof.

Guard: `UNKNOWN tail ≠ NORMAL tail`; `UNKNOWN high-consequence path ≠ destroy all local capability`.

## SYNTHESIS 12 — rollback must not resurrect bridge or token authority

PITR can restore old session tables, token-family state, provider mappings, bridge configuration or allowlists. Recovery must reconcile restored state against a current anti-rollback authority reference or governed rebootstrap.

Guards:
- `session DB restored consistently ≠ sessions current`;
- `bridge allowlist restored ≠ bridge reauthorized`;
- `old refresh family cryptographically valid ≠ current grant admitted`.

## Integrated EFB / LogMate-like scenario

Hypothetical only; production facts remain OPEN.

A company iPad remains offline across provider/custody migration G7→G8. It retains a G7 browser/app session, old refresh context, Service Worker, queued writes and unique flight records. A temporary bridge exists for bounded G7→G8 identity reconciliation.

Safe generic sequence:
1. preserve unique records, queue bytes and provenance before destructive auth cleanup;
2. treat local `signed in` display as historical/local state, not remote authorization;
3. on reconnect, obtain current G8 bootstrap/admission evidence through the admitted path;
4. reject or quarantine obsolete G7 remote-effect credentials at authoritative boundaries;
5. use the bridge only for its declared identity/recovery scope, not to mint unrestricted G8 authority;
6. revalidate each queued material operation under current policy/schema/identity rather than replaying because it was once authorized;
7. issue current sessions/tokens only after current admission;
8. prove obsolete G7 and bridge authority cannot create material effects;
9. preserve historical verification/provenance as needed;
10. retire the bridge without requiring the iPad to have been online at the exact retirement moment; a later return must enter through the current rejoin path.

This does **not** establish that LogMate uses OAuth/OIDC, direct PWA↔native sync, background execution, MDM or any specific provider.

## Track B transfer — truthful UX states

Useful semantic states include:
- local records preserved;
- sign-in/re-authentication required before sync or remote mutation;
- migration/recovery in progress;
- this device uses an obsolete session and must rejoin;
- some remote actions temporarily unavailable;
- migration complete centrally but this device still requires current admission.

Avoid language implying `your data is corrupt` merely because authorization is stale, and avoid `fully synced/current` until authoritative acknowledgement/currentness is known.

## Track D transfer — bounded measurement

Useful diagnostics can include:
- attempts by provider/generation/credential family;
- obsolete-authority rejection outcomes;
- bridge invocation by declared scope;
- current re-admission success/failure;
- offline/unknown tail size and age where privacy-appropriate;
- post-retirement bridge/predecessor attempts;
- acceptance-boundary coverage.

Telemetry cannot elect authority, and absence of events cannot prove absence of dormant/offline credentials.

## Track C destructive campaign — 960 → 968 defined cases

Add eight cases:
1. **bridge-transitive-super-authority** — G7→G8 bridge output is accepted as native G8 input to G9 without revalidation; must fail.
2. **logout-UI-equals-global-revocation** — browser logout succeeds while old refresh/server/background credentials still produce effects; migration closure must fail.
3. **new-provider-only-revocation** — provider B revokes sessions but provider A stale grant remains accepted; must fail.
4. **offline-client-revocation-delivery-theater** — migration relies on push/SW/MDM delivery to an offline iPad without authoritative server rejection; must fail.
5. **bridge-config-delete-retirement-theater** — repository config removed while admin/background path retains bridge-equivalent authority; must fail.
6. **zero-events-equals-convergence** — no stale telemetry is treated as proof despite unknown offline tail; must fail.
7. **PITR-token-bridge-resurrection** — restore reactivates obsolete token family/bridge allowlist as current; must fail.
8. **auth-cleanup-deletes-unique-data** — stale session cleanup destroys irreplaceable offline records/queue provenance; must fail.

These are **defined destructive cases**, not executed PASS.

## MINTTAP DECISION / DIRECTION

At the generic Web Manager level:
- temporary migration bridges are least-authority, explicit-scope, non-transitive and retireable;
- provider/session/token invalidation is modeled as a graph across all material acceptance surfaces;
- logout or one-provider revocation is never promoted to global invalidation without evidence;
- long-offline clients are handled through authoritative rejection plus current re-admission, not assumed push delivery;
- unique offline data is preserved independently of authorization currentness;
- convergence closure is consequence-based and can coexist with a bounded unknown/offline tail if stale authority cannot create material effects;
- bridge retirement requires successor positive proof plus bridge/predecessor negative proof and rollback resistance.

## OPEN

Production validation remains OPEN for:
- actual MintTap/LogMate authentication/session/token/provider architecture;
- OAuth/OIDC/Firebase or other provider use and exact revocation semantics;
- browser cookie/session persistence and installed-PWA behavior;
- physical iOS/iPadOS/WebKit and managed-device behavior;
- background/service/recovery/admin credential inventory;
- authoritative API/resource-server rejection behavior;
- direct PWA↔native synchronization and device identity;
- offline queue authorization/reconciliation semantics;
- bridge existence, scope, implementation and retirement;
- provider/org migration topology and currentness reference;
- PITR/backup session/token reconciliation;
- privacy/legal/aviation obligations;
- physical-device, AT and representative-human validation.

## DEPENDENCY / external specialist evidence

Design Studio Web remains Stage 3 PRACTICE / NOT PASSED at W121; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Web Manager consumes its state-model/UX evidence without claiming visual/interaction PASS.

Software Engineering Studio remains FOUNDATION STUDY UNDERWAY with no specialist Foundation PASS. M006 Safari Service Worker evidence is bounded transfer evidence only; installed PWA, fresh-origin-down cold start, physical iOS/iPadOS and canonical-product runtime remain OPEN. Implementation-level session/token/provider validation belongs with product/engineering evidence when available.

## CHANGE WATCH

- OAuth/OIDC provider behavior and vendor-specific revocation/logout semantics are implementation-specific and may change.
- Browser/iOS/iPadOS installed-PWA session/storage/background behavior remains platform/version-specific.
- Managed-device/MDM capabilities remain enrollment/OS/vendor-specific.
- NIST identity guidance versions and provider security guidance should be rechecked when product authentication architecture is selected.

## Gate

**PASS (generic)** for migration-bridge minimization, cross-provider invalidation reasoning and consequence-based convergence-completion judgment.

Not a production certification. No MintTap/LogMate provider, token, session, PWA, managed-iPad or runtime behavior is inferred.

## Next high-value target

**277 — credential-lineage inventory completeness, orphaned authorization discovery & post-migration dormant-path eradication**: determine how to prove that hidden service credentials, legacy refresh families, forgotten admin/recovery sessions, old endpoints and uninstrumented acceptance paths have been discovered after migration; how to distinguish `not observed` from `not possible`; and how to retire dormant authorization paths without destroying historical evidence or unique offline data.