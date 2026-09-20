# 171 — PWA Delegation Provenance Portability & Cross-System Federation

Status: **PASS (generic) / PRODUCT + FEDERATION + IDP + EMPLOYER/AIRLINE + REVOCATION + MANAGED-IPAD + LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A browser/session/SW/token mechanics; Track B federated-authority/currentness UX; Track C destructive federation/offline/device/accessibility validation; Track D privacy-bounded federation measurement.  
Dependency: 170 delegation lifecycle recovery, authority conflict and offline reconciliation.

## Why this study exists

170 separated account/authenticator, delegation, organization/employment, case and offline-device generations. The adjacent failure is cross-system authority: an employer, airline, IdP, federation broker or other external service may assert identity or attributes, but a local product can accidentally turn a transient external assertion into a permanent local authorization grant.

Central rule:

> **Consume federation as bounded, issuer-specific evidence. Do not convert identity, employment, organization membership or a cached assertion into evergreen local delegation. Establish local authority through an explicit policy mapping, preserve issuer/audience/time/provenance, and re-evaluate consequence-bearing operations against current local authority when freshness or federation continuity is uncertain.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns front/back-channel browser mechanics, redirect/session boundaries, token exposure surfaces, Service Worker/cache/storage behavior and reconnect. Browser possession of an assertion/token is not business authority.
- **B UX/IA/Content:** high dependency pressure. Must distinguish `signed in through`, `organization verified`, `acting for`, `access needs review`, provider unavailable and stale/offline evidence without exposing protocol jargon.
- **C Quality/Accessibility:** high dependency pressure. Owns issuer/audience/replay/expiry/provider-outage/migration/offline destructive tests plus browser/device/AT/human validation.
- **D Search/Analytics:** bounded consumer. Federation identifiers and organization/delegation graphs are not acquisition identifiers; measurement must avoid cross-context identity correlation.
- **E Security/Operations:** **bottleneck/owner**. Owns trust anchors, issuer registration, assertion validation, local authority mapping, revocation/currentness, provider migration, outage behavior and federation compromise response.

## SOURCE

### NIST SP 800-63C-4 — current federation baseline

NIST SP 800-63C-4, published 2025-08-01 and superseding SP 800-63C, is the current NIST federation/assertion guideline. It defines federation as a credential service provider supplying authentication and optionally subscriber attributes to separately administered relying parties. This is identity federation; it does not mean every asserted attribute is automatically local business authorization.

Source: https://www.nist.gov/publications/nist-sp-800-63c-4digital-identity-guidelines-federation-and-assertions

Operational transfer: the RP must know which external party it trusts, for which claims and purpose, at what assurance/currentness, and how those claims map to local policy. `federated authentication succeeded` is therefore an input to local authorization, not a generic delegation grant.

### NIST federation privacy boundary

Federation can expose subscriber attributes across administrative boundaries and create correlation risk. The durable design implication is data minimization: request only attributes needed for the local decision, avoid copying broad upstream identity profiles into local case history, and keep federation telemetry from becoming a durable cross-organization identity graph.

Source: https://csrc.nist.gov/pubs/sp/800/63/c/4/final

### RFC 9700 — OAuth 2.0 Security Best Current Practice

RFC 9700 (BCP 240, January 2025) recommends restricting access-token privileges to the minimum required, audience-restricting tokens to the intended resource server, and using sender-constrained access tokens where appropriate to reduce stolen-token replay. Public-client refresh tokens must be sender-constrained or use refresh-token rotation.

Source: https://www.rfc-editor.org/rfc/rfc9700.html

Transfer: even a correctly issued OAuth access token is bounded by issuer, audience/resource, scope/action, lifetime and token-binding/replay controls. It is not a portable organization-wide delegation certificate.

### RFC 9068 — JWT access-token validation

RFC 9068 requires a resource server receiving a JWT access token to validate issuer, audience, signature and expiration and reject a token whose audience does not identify the current resource server. Authorization claims are inputs that the resource server combines with its own context to decide whether the call is authorized.

Source: https://www.rfc-editor.org/rfc/rfc9068.html

Transfer: signature validity alone is insufficient. A token valid for service A cannot be replayed as authority at service B merely because both belong to the same company or federation.

### RFC 10017 — browser-based OAuth applications

RFC 10017, published in 2026, emphasizes reducing token authority for browser-based applications through short access-token lifetimes, reduced scopes/permissions and single-resource restriction, and warns against unnecessary sensitive claims in OpenID Connect ID Tokens.

Source: https://www.rfc-editor.org/rfc/rfc10017.html

Transfer: a PWA/browser client should not become a long-lived warehouse for broad federation claims merely to avoid future online checks.

## SYNTHESIS — separate assertion, evidence and authority

Do not collapse these objects:

1. **External identity assertion** — issuer says a subject authenticated or has attributes at issuance time.
2. **External relationship evidence** — issuer says a subject currently has some employer/airline/organization relationship, if the issuer is actually authoritative for that fact.
3. **Local authority mapping** — local policy decides whether that evidence permits a local capability over a local subject/case/resource.
4. **Local delegation generation** — explicit local grant/current authority state with provenance and lifecycle.
5. **Browser/session/token state** — transport/runtime mechanism, not semantic authority by itself.
6. **Offline observation** — what a device last knew; historical evidence unless currentness is re-established.

Persistent guards:

- `federated login PASS ≠ local delegation PASS`;
- `identity assertion valid ≠ employment/relationship current`;
- `employment/organization attribute current ≠ authority over every local case`;
- `issuer trusted for authentication ≠ issuer trusted for delegation`;
- `signature valid ≠ issuer appropriate for this claim`;
- `issuer appropriate ≠ claim current enough for this consequence`;
- `audience valid ≠ scope/capability sufficient`;
- `scope present ≠ local policy permits operation`;
- `token cached ≠ authority evergreen`;
- `refresh succeeds ≠ external relationship still semantically valid`;
- `provider unavailable ≠ stale assertion becomes current`;
- `provider migrated ≠ old issuer automatically interchangeable with new issuer`;
- `same email/employee ID ≠ same federated subject lineage`;
- `IdP account disabled ≠ all locally sourced authority necessarily deleted`;
- `IdP account active ≠ all local authority necessarily active`;
- `offline assertion authentic ≠ online mutation authorized now`.

## Trust contract — trust issuers per claim class, not globally

A federation trust configuration needs more than `trusted_idp=true`. Record, conceptually:

- issuer identity and trust anchor/registration provenance;
- expected audience/resource/RP;
- claim classes the issuer is authoritative to assert;
- assurance/currentness requirements by local capability;
- subject identifier semantics and migration rules;
- attribute minimization rules;
- assertion/token lifetime and replay expectations;
- revocation/disable/currentness signal where available;
- provider outage behavior;
- key rotation/compromise procedure;
- provider migration/successor procedure;
- local policy generation that maps evidence to authority.

Example: an enterprise IdP can be trusted to authenticate employee E, but not necessarily to assert that E may act for pilot P's personal logbook case. An airline roster service may know crew assignment but not legal representative status. A device-management service may know a device is supervised but not which human currently has case authority.

## Currentness and revocation

Federation protocols can prove bounded facts at a point in time. They do not create a universal currentness oracle.

For consequence-bearing local operations:
1. validate issuer, audience/resource, signature, expiry and replay requirements;
2. validate that the issuer is trusted for the specific claim class;
3. evaluate currentness appropriate to the consequence and available provider signals;
4. map the evidence through current local policy/delegation generation;
5. authorize the local operation against current case/resource state;
6. preserve enough provenance to explain which external evidence and local policy supported the decision without retaining unnecessary upstream payloads.

Do not extend a short-lived assertion indefinitely by copying its claims into IndexedDB and labeling them `verified`. If local product policy intentionally creates a durable local delegation from an external event, that is a new local authority object with explicit provenance/lifecycle — not continued validity of the old assertion.

## Provider outage — degrade evidence, not truth

Provider outage creates `currentness unavailable`, not `relationship definitely ended` and not `relationship definitely continues`.

Capability-specific behavior:
- public/non-sensitive local content may remain available;
- local drafts and unique operational records remain readable/exportable where local policy permits;
- low-consequence actions may use explicitly defined bounded grace only if product/security policy supports it;
- consequence-bearing remote mutations requiring fresh external authority fail closed or enter review/quarantine;
- stale assertion age and last-known state may be shown as context but not promoted to current authority;
- recovery/redress must not depend solely on the failed provider when that would create an unrecoverable circular dependency.

A grace period, if ever adopted, is a product/security/legal decision with explicit maximum age, capability scope, risk and revocation caveat. Generic research does not invent one.

## Provider migration and successor trust

Migration from IdP A to IdP B is not `replace issuer string`.

Required conceptual steps:
1. establish B independently through approved trust/registration governance;
2. define subject-account linking evidence without relying only on mutable email/employee IDs;
3. preserve A-era provenance for historical decisions;
4. prevent A-era bearer artifacts from becoming valid under B;
5. create new local mapping/delegation generations where current authority continues;
6. reconcile pending/offline operations against the new authority floor;
7. retire A according to explicit overlap/rollback/compromise policy;
8. distinguish planned migration from A compromise — a compromised A cannot be the sole authority that blesses B.

`same person` and `same authority` are separate migration questions.

## Federation broker/proxy boundary

A federation broker can normalize protocols and reduce RP integration complexity, but it becomes a concentrated trust/privacy dependency. Downstream services must not infer that every upstream claim is equally trustworthy merely because the broker emitted a uniform token.

Preserve claim provenance sufficiently to know the authoritative upstream class or broker assurance decision when that matters. At the same time, do not expose unnecessary upstream identity topology to clients or analytics.

Broker compromise/outage and split-view behavior belong in dependency/resilience and incident plans; `one broker` is not `one source of truth` unless governance actually makes it authoritative for the relevant claim.

## PWA / managed-iPad offline model

A long-offline PWA can retain:
- an old browser session;
- old ID/access-token-derived projections;
- local delegation state;
- a stale Service Worker;
- IndexedDB/Cache Storage data;
- locally authored drafts/flight records;
- queued delegated operations.

Generic reconnect sequence for consequence-bearing work:
1. preserve unique local operational data before authority repair;
2. treat cached federation/delegation data as historical observation;
3. establish a current network/trust path outside stale business-state assumptions;
4. obtain current server-side local authority floor;
5. refresh/re-establish external federation evidence only where current policy requires it;
6. validate issuer/audience/currentness and map through current local policy;
7. compare queued operation's delegation/policy/case generations;
8. execute only if current authority explicitly admits it; otherwise quarantine/preserve for review or resubmission;
9. do not let Service Worker update, MDM presence, connectivity or token refresh independently authorize replay.

No assumption is made that iPadOS provides unattended background refresh/sync. Physical Safari/Home Screen/MDM behavior remains OPEN.

## Privacy and identifier portability

Avoid using global email, employee number, airline ID or federation subject as an analytics/acquisition identity unless separately justified. Prefer RP/local identifiers and minimize imported attributes.

Provider migration must not silently create a permanent cross-provider correlation table available to analytics/support. Identity-linking evidence should be access-controlled, purpose-bounded and retained according to actual operational/legal need.

If pairwise/pseudonymous identifiers or broker mappings are used, they reduce some correlation risk but do not make accompanying attributes anonymous.

## UX transfer — Track B

User-facing concepts should be semantic, not protocol-centric:
- `Signed in through your organization`;
- `Organization status verified` only when current evidence supports that exact statement;
- `Acting for [subject]` only when local delegation is current;
- `Permission needs to be checked before this draft can be submitted`;
- `Your organization sign-in service is unavailable. Your saved local records are still available.`;
- `Access changed since this device was last online`;
- `Draft kept — submission requires review`.

Avoid `SSO token expired`, `FAL`, `aud mismatch` and issuer IDs as primary user explanations. Diagnostic detail can exist in support/operator surfaces with appropriate confidentiality.

## MINTTAP DECISION — generic governance

1. Treat federation as bounded evidence transport, not portable evergreen delegation.
2. Trust issuers per claim class and purpose; authentication trust does not imply delegation trust.
3. Validate issuer/audience/signature/time/replay plus local claim-authority mapping before consequence-bearing use.
4. Keep local delegation generation distinct from external assertion/token lifetime.
5. Provider outage yields unknown/stale currentness; do not silently extend authority.
6. Provider migration creates new trust/mapping generations; do not rewrite history or equate mutable identifiers.
7. Preserve unique local PWA operational data even when federation authority is unavailable or revoked.
8. Revalidate queued consequence-bearing operations at commit/reconnect time; cached federation state is not enough.
9. Minimize imported attributes and federation telemetry; do not create a durable cross-provider identity graph without justified need.
10. Actual LogMate employer/airline/IdP/MDM authority, provider contracts, legal consequences and physical iPad behavior remain OPEN.

## VALIDATION — 128-case destructive campaign

1 valid issuer/login; 2 wrong issuer; 3 unknown issuer; 4 compromised issuer; 5 retired issuer; 6 issuer key rotation; 7 stale key cache; 8 wrong audience; 9 multi-audience ambiguity; 10 wrong resource; 11 expired assertion; 12 not-yet-valid/clock skew; 13 replay; 14 duplicate assertion ID; 15 signature failure; 16 alg confusion; 17 malformed claims; 18 missing subject; 19 mutable email as subject; 20 employee-ID reuse; 21 subject merge; 22 subject split; 23 pairwise identifier migration; 24 authentication-only issuer used for employment; 25 employment issuer used for delegation; 26 MDM used as human authority; 27 roster assignment used as legal representation; 28 valid employment + invalid case scope; 29 valid delegation + wrong case; 30 valid scope + prohibited action; 31 scope escalation; 32 stale role claim; 33 stale group claim; 34 stale employment claim; 35 upstream disable; 36 upstream re-enable; 37 local revoke while upstream active; 38 upstream revoke while local grant active; 39 explicit durable local grant policy; 40 accidental durable grant; 41 token copied to IndexedDB; 42 token leaked to Cache Storage; 43 URL/history leakage; 44 logs leak token; 45 analytics leak claims; 46 referrer leakage; 47 XSS token theft; 48 CSRF local action; 49 sender-constrained token path; 50 stolen bearer replay; 51 refresh rotation; 52 refresh replay; 53 provider outage; 54 DNS outage; 55 federation metadata outage; 56 key endpoint outage; 57 currentness endpoint outage; 58 partial provider recovery; 59 stale provider replica; 60 split-view issuer metadata; 61 bounded grace disabled; 62 bounded grace if product policy exists; 63 grace expiry; 64 high-consequence action during outage; 65 local draft during outage; 66 local export during outage; 67 unique flight data preserved; 68 provider A→B planned migration; 69 A compromised during migration; 70 A and B overlap; 71 subject linking mismatch; 72 email collision; 73 employee-ID collision; 74 old A token under B; 75 old A queue after B migration; 76 new B auth + old local delegation; 77 explicit new delegation generation; 78 rollback to A; 79 migration rollback after compromise; 80 broker normal path; 81 broker outage; 82 broker compromise; 83 broker strips provenance; 84 broker overclaims assurance; 85 upstream issuer changed behind broker; 86 privacy overcollection; 87 unnecessary ID-token claims; 88 cross-RP correlation; 89 analytics correlation; 90 support correlation; 91 export contains federation secret; 92 PITR resurrects old issuer trust; 93 backup restores old mapping; 94 config rollback; 95 local policy generation rollback; 96 provider metadata rollback; 97 offline cold start; 98 stale Service Worker; 99 stale IndexedDB; 100 stale Cache Storage; 101 stale session; 102 cached explanation; 103 queued mutation old delegation; 104 reconnect provider unavailable; 105 reconnect local server available/provider down; 106 reconnect provider up/local authority stale; 107 multiple-generation jump; 108 token refresh succeeds but delegation revoked; 109 same actor re-delegated; 110 old queue remains non-executable; 111 explicit resubmission; 112 duplicate reconnect; 113 lost ACK; 114 retry/idempotency; 115 current case conflict; 116 account switch/shared device; 117 MDM reassignment; 118 company iPad still managed after employment ends; 119 notification stale; 120 keyboard federation/recovery flow; 121 screen-reader provider/outage state; 122 focus after failed federation; 123 zoom/reflow; 124 localization/RTL; 125 physical Safari/Home Screen OPEN; 126 actual LogMate federation OPEN; 127 security/privacy/legal/aviation review OPEN; 128 human/AT managed-fleet validation OPEN.

## CONTRADICTIONS / failure modes resolved

- **SSO-authority inflation:** successful organizational sign-in is not authority over every local subject/case.
- **Attribute-authority inflation:** an issuer can truthfully assert employment while being non-authoritative for representative delegation.
- **Cached-claim immortality:** persisting a valid claim does not preserve its currentness forever.
- **Provider-outage fail-open:** inability to refresh currentness does not justify silently extending high-consequence authority.
- **Migration identity collapse:** matching email/employee ID does not prove continuity of federated subject or delegation generation.
- **Broker laundering:** a uniform broker token must not erase material upstream provenance/assurance differences.
- **Offline replay inflation:** reconnect/token refresh does not automatically authorize an old queued delegated action.
- **Federation data-hoarding:** importing broad identity profiles for convenience creates avoidable privacy/correlation risk.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate IdP/CSP/federation/broker; employer/airline authority; local delegation semantics; OIDC/OAuth/SAML use; provider currentness/revocation API; identifier contract; token storage; backend/session architecture; MDM/Shared iPad; offline queue schema; legal/aviation authority; physical Safari/Home Screen behavior; background execution; human/AT evidence.

DEPENDENCY: Software Engineering owns implementation architecture, protocol libraries, token/session storage and executable federation/reconnect tests. Design Studio owns reusable federation/outage/review interaction patterns. Web Manager owns web/PWA trust boundaries, requirements and evidence interpretation.

CHANGE WATCH: NIST SP 800-63C-4 updates/errata; OAuth/OIDC security BCP evolution; RFC 10017 implementation guidance; browser privacy/storage changes; WebKit/iPadOS PWA behavior; enterprise IdP/broker platform behavior; applicable employment/representative/privacy/aviation law.

## Adjacent next question

The next highest-value boundary is **federation compromise, issuer metadata/key recovery & local authority containment**: when an IdP/broker signing key, discovery/metadata endpoint or federation control plane is suspected compromised, determine how to freeze new trust without destroying local unique data, distinguish pre-compromise historical evidence from current authorization, rotate/re-establish issuer trust independently, and reconcile offline clients that may still hold cryptographically valid but no-longer-trusted assertions.