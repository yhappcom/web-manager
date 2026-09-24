# 277 — PWA Credential-Lineage Inventory Completeness, Orphaned Authorization Discovery & Post-Migration Dormant-Path Eradication

Status: **PASS (generic) / PRODUCT + IDP + PROVIDER + BACKEND + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline credential surfaces; Track B truthful recovery/rejoin UX; Track C destructive validation; Track D discovery/coverage diagnostics.  
Dependencies: 260–276 dependency completeness, topology discovery, revocation, authority/custody migration, bridge minimization, credential invalidation and convergence governance.

## Problem

276 established that migration closure is consequence closure rather than fleet simultaneity. That closure is unsafe if the credential and acceptance inventory is incomplete. Dormant refresh families, service credentials, forgotten admin/recovery sessions, old endpoints, background workers, replicas, compatibility routes or offline clients can remain capable of producing effects even when the visible migration path is clean.

Central rule: **credential inventory completeness is a bounded assurance claim over credential roots, derivation lineage and material acceptance boundaries; silence is not proof of absence, and dormant authority is retired only when it cannot create material effects without current admission. Historical evidence and unique offline data remain distinct from current authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns cookies/session artifacts, Service Worker/cache/storage state, offline return and browser-held credential mechanics. Browser enumeration cannot prove backend inventory completeness.
- **B UX/IA/Content:** high dependency pressure. Owns truthful `re-authentication required`, `local records preserved`, `old access retired`, `device still requires rejoin` states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** destructive campaign expands **968 → 976 defined cases**. Execution, physical-device, AT and representative-human PASS remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Owns coverage diagnostics, stale-path probes, inventory reconciliation and unknown-tail measurement; telemetry is evidence, not authority.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns credential-lineage model, completeness claim, orphan discovery, acceptance-boundary proof, dormant-path retirement and rollback resistance.

## SOURCE

### RFC 7009 — OAuth 2.0 Token Revocation

RFC 7009 defines revocation of access and refresh tokens and states that revocation can, where applicable, invalidate other tokens based on the same authorization grant and the grant itself. It explicitly motivates cleanup of abandoned grants that users may otherwise be unaware of.

Source: https://www.rfc-editor.org/rfc/rfc7009

**TRANSFER VALIDATION:** this is concrete precedent that an authorization artifact belongs to a wider grant lineage and abandoned authorization matters. It does not prove MintTap/LogMate uses OAuth or that RFC 7009 can enumerate every product credential.

### RFC 9700 — OAuth 2.0 Security Best Current Practice

RFC 9700 requires replay defense for refresh tokens issued to public clients through sender constraint or refresh-token rotation. Rotation retains relationship information so reuse of an invalidated predecessor can expose compromise; refresh tokens remain bound to the authorized scope/resource servers.

Source: https://www.rfc-editor.org/rfc/rfc9700.html

**TRANSFER VALIDATION:** lineage retention and audience/scope restriction are useful precedents for discovering and containing derived credentials. They do not establish the product token design.

### NIST SP 800-63B-4 — independent IdP/RP session state

NIST SP 800-63B-4 states that IdP and RP sessions are managed independently and that termination at one does not inherently terminate the other. It also treats session continuity and reauthentication as explicit lifecycle concerns.

Source: https://pages.nist.gov/800-63-4/sp800-63b.html

**TRANSFER VALIDATION:** this supports treating credential/session inventory as multiple independent surfaces rather than one `logged in` flag. No product AAL or timeout is inferred.

### RFC 9770 — revoked-token notification for intermittently connected devices

RFC 9770 addresses revocation notification in an ACE environment where intermittently connected devices can hold relatively long-lived access tokens and therefore need updated revocation information.

Source: https://www.rfc-editor.org/rfc/rfc9770.html

**TRANSFER VALIDATION:** this is bounded precedent that intermittent connectivity complicates revocation/currentness. ACE/CoAP mechanisms are not MintTap/LogMate defaults.

## SYNTHESIS 1 — inventory is a graph, not a token table

A defensible inventory distinguishes:
- authority/grant/session roots;
- derived access/refresh/session artifacts;
- browser cookies and local session handles;
- service/background credentials;
- admin/recovery credentials and sessions;
- device/incarnation bindings where used;
- migration/compatibility bridge artifacts;
- queued operations carrying historical authorization context;
- material acceptance boundaries: API, resource server, job worker, admin/recovery path, compatibility endpoint and equivalent effectors.

A credential row without derivation and acceptance edges cannot establish whether retirement is complete.

Guards:
- `token table complete ≠ authorization graph complete`;
- `known issuers enumerated ≠ all acceptance paths enumerated`;
- `credential not in UI ≠ credential not authoritative`.

## SYNTHESIS 2 — completeness needs independent discovery channels

Self-reported inventory from the same provider/control plane being migrated is useful but insufficient for high-consequence closure. Discovery should reconcile, where applicable and available:
1. configured issuers/providers and registered clients;
2. application/backend acceptance code and policy configuration;
3. runtime logs/telemetry at material boundaries;
4. secret/KMS/service-account inventory;
5. job/worker/deployment topology;
6. admin/recovery interfaces;
7. historical issuance/revocation records;
8. active negative probes for retired generations;
9. backup/PITR and compatibility configuration that can restore old acceptance.

No single channel is universally authoritative. Correlation and blind spots must be explicit.

Guards:
- `provider export complete ≠ application acceptance inventory complete`;
- `code search clean ≠ runtime topology clean`;
- `runtime quiet ≠ dormant path impossible`.

## SYNTHESIS 3 — absence of observation and impossibility are different claims

A stale credential may be unobserved because its owner is offline, the path is rarely used, telemetry is missing, the credential is dormant until incident recovery, or an old endpoint is outside current dashboards. Zero events is therefore weak negative evidence.

Stronger closure combines topology evidence with negative acceptance tests and current-policy enforcement at material boundaries.

Guards:
- `not observed ≠ does not exist`;
- `does not currently execute ≠ cannot execute`;
- `zero stale traffic ≠ zero stale authority`.

## SYNTHESIS 4 — orphan means lineage or owner is unresolved, not automatically malicious

An orphan can be a credential whose issuing grant, owner, device, service, provider generation, purpose or acceptance boundary cannot be resolved. Unknown provenance is itself a risk state, but it does not justify destroying user data or historical evidence.

For consequence-bearing authority, unresolved lineage should not be silently classified current. It should be quarantined, re-attributed/re-admitted, or retired according to product policy.

Guards:
- `orphaned credential ≠ trusted current credential`;
- `orphaned authorization ≠ orphaned user data`;
- `unknown owner ≠ safe to replay`.

## SYNTHESIS 5 — dormant credentials can be more dangerous than noisy stale credentials

A noisy predecessor is likely to trigger telemetry and rejection evidence. A dormant admin token, recovery session, service account or compatibility endpoint may survive until a rare incident and then bypass the normal path. Discovery priority should therefore weight consequence and privilege, not only frequency.

Useful risk dimensions include consequence class, privilege breadth, issuer/provider generation, last verified use, owner/current custodian, audience, derivation root, acceptance surface, observability and retirement evidence.

Guard: `rarely used ≠ low consequence`.

## SYNTHESIS 6 — acceptance-boundary enumeration is the closure anchor

Credential inventory can never be proved merely by listing every byte that might exist on disconnected devices. A more useful bounded claim asks whether any obsolete credential can reach a material acceptance boundary and create an effect without current re-admission.

This shifts proof toward:
- complete-enough material-boundary topology;
- current admission policy at those boundaries;
- predecessor/unknown rejection tests;
- removal of ungoverned bypass/fallback paths;
- rollback resistance.

Guard: `unknown offline credential may exist ≠ central migration can never close`; equally, `central migration declared closed ≠ every boundary is fenced`.

## SYNTHESIS 7 — refresh-family lineage is a concrete model, not a universal inventory

RFC 9700 refresh rotation shows why predecessor/successor relationship retention matters: replay of an invalidated predecessor can reveal that a family is compromised. The general lesson is to preserve enough lineage to reason about derived authority and revocation blast radius.

Do not overgeneralize OAuth family semantics to browser cookies, service credentials or recovery sessions. Each artifact class needs its own lineage/currentness model.

Guard: `refresh-family modeled ≠ all credential classes modeled`.

## SYNTHESIS 8 — session inventory crosses IdP and RP boundaries

NIST SP 800-63B-4 explicitly separates IdP and RP sessions. Consequently, a provider migration inventory that only enumerates IdP sessions can miss RP/server sessions, application cookies and downstream service authorization.

Guards:
- `IdP inventory complete ≠ RP inventory complete`;
- `IdP logout complete ≠ downstream session inventory empty`.

## SYNTHESIS 9 — long-offline PWA state is an unknown-tail class, not an exception to authority

A company iPad may retain a browser/app session, IndexedDB data, Service Worker state, queued operations and possibly provider artifacts while offline. Its local state cannot be centrally enumerated in real time.

The safe model does not require magical remote deletion. Instead:
- preserve unique local records/provenance;
- treat stale local signed-in state as non-authoritative for remote effects;
- require current rejoin/admission on reconnect;
- reject obsolete/unknown authority at online material boundaries;
- reconcile queued operations under current policy/schema/identity.

Guards:
- `offline state unenumerable ≠ offline state pre-authorized`;
- `local credential still present ≠ remote effect permitted`;
- `cannot remotely erase ≠ cannot safely contain`.

## SYNTHESIS 10 — dormant-path eradication is consequence retirement, not artifact deletion

A stale token can remain in a historical log or offline device while being harmless if every material boundary rejects it. Conversely, deleting a token row is meaningless if a fallback route, service credential or restored snapshot recreates equivalent authority.

Closure therefore needs current-effect negative proof, not merely storage deletion.

Guards:
- `artifact deleted ≠ authority eradicated`;
- `historical verifier retained ≠ current authority retained`;
- `credential bytes preserved for evidence ≠ credential admitted`.

## SYNTHESIS 11 — PITR and rollback are inventory multipliers

Backups can restore retired clients, sessions, token-family state, allowlists, old endpoint configuration or service credentials. Inventory must include resurrection sources, not just live state.

A restore must reconcile against current external/anti-rollback authority before obsolete credentials or acceptance rules regain current consequence.

Guards:
- `live inventory clean ≠ restore inventory safe`;
- `backup authentic ≠ restored authorization current`.

## SYNTHESIS 12 — telemetry completeness is itself an assurance claim

Track D can measure issuance, stale attempts, rejection, bridge use and unknown-tail age, but metrics need coverage metadata. `100% of observed endpoints` is meaningless if endpoint discovery is incomplete.

Useful diagnostics distinguish:
- known material boundaries covered;
- known boundaries not instrumented;
- suspected/unknown topology;
- stale credential attempts and rejection outcomes;
- orphan discovery source and disposition;
- dormant privileged paths exercised by scheduled negative tests.

Guard: `dashboard coverage 100% ≠ topology coverage 100%`.

## SYNTHESIS 13 — discovery must not become a new authority oracle

Inventory scanners, telemetry collectors and secret-discovery systems can be compromised, stale or incomplete. Their findings inform challenge and remediation but do not themselves elect current authority.

High-consequence closure should correlate independent-enough evidence and retain contradiction states rather than majority-voting them away.

Guard: `scanner says absent ≠ cryptographic/organizational retirement proven`.

## SYNTHESIS 14 — retirement has a lifecycle

A dormant path moves through states such as:
1. discovered/suspected;
2. lineage/owner/scope resolved or marked UNKNOWN;
3. consequence fenced;
4. current replacement/rejoin path proven where needed;
5. predecessor negative test passed at material boundaries;
6. configuration/secret/session cleanup performed;
7. rollback/PITR resurrection test passed;
8. historical provenance retained as required;
9. monitoring/watch period bounded by risk rather than treated as proof by silence.

No single deletion step substitutes for this lifecycle.

## Integrated EFB / LogMate-like scenario

Hypothetical only; production facts remain OPEN.

After G7→G8 provider/custody migration, central dashboards show no G7 traffic. One company iPad has been offline for six weeks. A forgotten compatibility endpoint and a dormant maintenance credential also existed during G7.

Safe generic sequence:
1. preserve unique iPad records, queue bytes and provenance;
2. inventory credential roots, derivation classes and material acceptance boundaries independently of the visible login UI;
3. discover compatibility/admin/background/recovery paths and reconcile them with deployment/runtime topology;
4. classify the offline iPad as an unknown tail, not current authority and not data loss;
5. require current G8 admission before material remote effects;
6. actively prove G7/unknown credentials fail at material boundaries, including compatibility/admin/background paths;
7. on iPad reconnect, reconcile queued operations under current identity/policy/schema rather than auto-replay;
8. retire dormant paths while preserving historical verification material;
9. test PITR/restore so G7 acceptance cannot resurrect;
10. retain residual UNKNOWN explicitly if a material boundary cannot yet be verified.

This does **not** establish LogMate's actual IdP, token, service-account, MDM, direct-device-sync or backend architecture.

## Track B transfer — truthful UX

Useful states include `local records preserved`, `sign in again before sync`, `this device has not completed migration`, `some remote actions are temporarily unavailable`, and `old access retired`. Avoid claiming `all sessions removed` or `fully current` unless the relevant scope is actually proven.

## Track D transfer — discovery without authority laundering

Track D should maintain coverage-oriented diagnostics rather than vanity counts. Measure inventory sources, boundary coverage, stale/orphan attempts, rejection results, unknown/offline cohorts and dormant privileged-path tests. Analytics never turns silence into authority.

## Track C destructive campaign — 968 → 976 defined cases

Add eight cases:
1. **provider-export-equals-complete-inventory** — provider lists no old tokens while RP/server session still creates effects; must fail.
2. **zero-traffic-equals-no-dormant-authority** — forgotten admin credential is unused during observation then succeeds; must fail.
3. **code-search-equals-runtime-topology** — source tree is clean while old deployed worker/endpoint accepts stale authority; must fail.
4. **orphan-cleanup-deletes-user-data** — unresolved credential cleanup destroys unique offline records/provenance; must fail.
5. **refresh-family-equals-all-credentials** — OAuth family is retired while service/recovery credential remains accepted; must fail.
6. **dashboard-100-percent-coverage-theater** — all instrumented endpoints are green but one material uninstrumented compatibility path exists; must fail.
7. **PITR-recreates-dormant-path** — restore reactivates retired session/allowlist/service credential; must fail.
8. **offline-iPad-local-session-authority** — late device presents stale local session and queued writes that bypass current re-admission; must fail.

These are **defined destructive cases**, not executed PASS.

## MINTTAP DECISION / DIRECTION

At generic Web Manager level:
- model credential currentness as lineage plus material acceptance reachability, not one token/session table;
- use multiple discovery channels and expose coverage/UNKNOWN explicitly;
- treat orphaned authority as unresolved risk without conflating it with user-data validity;
- prioritize dormant privileged paths by consequence, not event frequency;
- anchor closure at authoritative material boundaries with predecessor/unknown negative proof;
- preserve historical evidence and unique offline data while retiring current consequence;
- include backup/PITR and compatibility paths in inventory/resurrection testing;
- do not infer actual MintTap/LogMate OAuth, IdP, MDM, provider or backend topology without canonical/runtime evidence.

## OPEN / VALIDATION

Production validation remains OPEN for actual credential classes and issuers; Firebase/Apple/Google/email auth behavior if used; RP/backend session topology; access/refresh/grant semantics; service/background/admin/recovery credentials; endpoint/job/deployment topology; managed-iPad local persistence; revocation propagation; offline-return behavior; backup/PITR; and material-boundary negative tests.

Physical iOS/iPadOS installed-PWA validation, Safari/WebKit runtime validation, screen-reader/representative-human UX validation and canonical-product runtime evidence remain OPEN.

## CHANGE WATCH

- OAuth/OIDC and NIST digital-identity guidance changes;
- Apple/WebKit/iOS/iPadOS PWA session/storage/background behavior;
- provider-specific session/revocation/export capabilities once actual providers are established;
- Software Engineering canonical auth/session/runtime findings when promoted beyond foundation evidence.

## Gate

**277 PASS (generic).** The Web Manager can now reason about credential-lineage inventory completeness, orphaned authorization discovery, dormant privileged paths, acceptance-boundary closure, offline unknown tails and rollback-safe retirement without claiming product implementation evidence.

Next highest-value adjacent work: **278 — acceptance-boundary topology attestation, hidden-bypass discovery & continuous dormant-authority regression control**: prove the set of consequence-bearing boundaries remains complete as deployments/routes/jobs evolve, detect newly introduced bypasses or reactivated legacy paths, and prevent a one-time clean inventory from decaying into false closure.