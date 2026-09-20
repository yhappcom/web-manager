# 172 — PWA Federation Trust Metadata Currentness, Split-View & Successor-Anchor Governance

Status: **PASS (generic) / PRODUCT + FEDERATION + IDP + TRUST-ANCHOR + MANAGED-IPAD + PROVIDER + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A discovery/HTTPS/JWKS/SW/cache mechanics; Track B trust-currentness/degraded-state UX; Track C destructive metadata/key/split-view/offline validation; Track D privacy-bounded federation diagnostics.  
Dependency: 171 delegation provenance portability and cross-system federation.

## Why this study exists

171 established that federation assertions are bounded evidence, not evergreen local delegation. The adjacent bottleneck is how a relying system knows **which federation configuration itself is current and trustworthy**. A correctly signed token can still be evaluated against stale, substituted or split-view metadata; a provider migration can preserve identity while changing issuer/trust topology; an offline PWA can retain an internally consistent but obsolete trust view.

Central rule:

> **Federation metadata, keys, trust chains and local trust-anchor configuration are versioned security state, not passive discovery conveniences. Validate identity and provenance of metadata, bind it to the expected issuer/resource and local trust policy, preserve freshness/transition evidence, and never let a cached or self-consistent offline trust view silently become current authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns HTTPS fetch, redirect/origin, HTTP cache, browser storage, Service Worker and reconnect mechanics. Network success or cache hit is not trust-currentness proof.
- **B UX/IA/Content:** high dependency pressure. Must express `organization sign-in unavailable`, `trust information needs refresh`, `saved work remains available`, and `submission requires review` without exposing federation internals.
- **C Quality/Accessibility:** high dependency pressure. Owns metadata substitution, stale JWKS, key rotation, split-view, migration, rollback, cache/SW/offline and accessible degraded-state tests.
- **D Search/Analytics:** bounded consumer. Security diagnostics may measure aggregate trust-refresh outcomes, but issuer/entity identifiers and federation graphs must not become acquisition/user tracking identifiers.
- **E Security/Operations:** **bottleneck/owner**. Owns trust anchors, metadata provenance/currentness, issuer/resource binding, key transition, federation-policy evaluation, migration and compromise recovery.

## SOURCE

### RFC 8414 — OAuth 2.0 Authorization Server Metadata

RFC 8414 defines HTTPS authorization-server metadata and requires the returned `issuer` value to be identical to the issuer identifier used to construct the metadata request; if not identical, the metadata **must not be used**. It defines `jwks_uri` as the HTTPS location for keys used to validate authorization-server signatures and permits signed metadata.

Source: https://www.rfc-editor.org/rfc/rfc8414.html

Operational transfer: discovery is not `fetch arbitrary JSON and trust endpoints`. Issuer binding is a security invariant. Endpoint/key metadata that does not bind to the expected issuer cannot be accepted merely because TLS succeeded.

### RFC 9728 — OAuth 2.0 Protected Resource Metadata

RFC 9728 defines protected-resource metadata including the resource identifier and authorization servers associated with that resource.

Source: https://www.rfc-editor.org/rfc/rfc9728.html

Operational transfer: authorization-server trust and protected-resource identity are distinct bindings. A valid authorization server is not automatically appropriate for every resource.

### OpenID Federation 1.0 — Final, 2026-02-17

OpenID Federation 1.0 is an OpenID Final Specification. It models federation entities, signed Entity Statements, trust anchors and trust chains. A federation entity is trusted through a chain from the entity to a locally trusted anchor; Entity Statements carry issuance/expiry and metadata/policy information.

Source: https://openid.net/specs/openid-federation-1_0.html

Operational transfer: a cryptographically valid leaf self-statement is not sufficient to establish federation membership. Trust is evaluated through an accepted chain and local trust anchor/policy.

### OpenID Federation for OpenID Connect 1.1 — Final, 2026-05-05

The OpenID Foundation published OpenID Federation for OpenID Connect 1.1 as Final in May 2026.

Source: https://openid.net/specs/openid-federation-connect-1_1.html

CHANGE WATCH: OpenID Federation is current and comparatively new. Product adoption, ecosystem interoperability and provider-specific behavior require implementation evidence rather than standards-only assumptions.

### NIST SP 800-63C-4 — federation and assertions

NIST SP 800-63C-4 is the current NIST federation guideline (published 2025-08-01, superseding SP 800-63C). It treats federation as interaction across separately administered relying parties and credential service providers and supports multiple CSPs per RP.

Source: https://csrc.nist.gov/pubs/sp/800/63/c/4/final

Transfer: federation is explicitly cross-administrative. Local systems need explicit trust configuration and cannot assume an external provider's administrative state is identical to local authorization state.

## SYNTHESIS — distinguish five trust objects

Do not collapse:

1. **Entity/issuer identity** — which external system is speaking.
2. **Metadata document** — endpoints, keys, capabilities and policy material observed at a point in time.
3. **Trust chain** — evidence linking an entity through intermediates to an accepted anchor where federation uses chains.
4. **Local trust-anchor/policy generation** — which anchors, issuers, claim classes and transition rules the local product currently accepts.
5. **Local authorization/delegation generation** — what the product currently permits for a subject/case/capability.

Persistent guards:

- `HTTPS fetch succeeded ≠ metadata semantically trusted`;
- `metadata signature valid ≠ expected issuer bound`;
- `issuer bound ≠ resource bound`;
- `JWKS fetched ≠ key current`;
- `key ID matches ≠ key lineage trusted`;
- `leaf self-statement valid ≠ federation membership proven`;
- `trust chain validates ≠ local policy accepts this chain`;
- `one valid chain ≠ no competing valid chain exists`;
- `metadata cached ≠ metadata current`;
- `cache revalidated ≠ federation relationship semantically current`;
- `provider reachable ≠ provider uncompromised`;
- `provider unavailable ≠ stale metadata becomes current`;
- `same issuer URL ≠ same uncompromised trust generation`;
- `same organization ≠ same federation entity identifier`;
- `new anchor available ≠ old anchor may authorize its own replacement after compromise`;
- `offline trust view internally consistent ≠ online authority current`.

## Metadata retrieval is a security operation

Treat metadata retrieval as controlled trust-state acquisition:

1. start from a locally authorized issuer/entity/resource identifier or an explicitly governed discovery path;
2. require secure transport where the protocol requires it;
3. validate exact issuer/resource binding and redirect/origin rules appropriate to the protocol;
4. validate signatures/chains/policies where applicable;
5. enforce local algorithm/key/policy requirements;
6. record freshness/expiry and the local trust-policy generation used for evaluation;
7. cache only with explicit bounded semantics;
8. on refresh failure, distinguish `stale/unknown` from `revoked/false`;
9. do not let untrusted metadata choose an unrestricted next fetch target without SSRF/network-boundary controls in server-side implementations;
10. keep browser/PWA clients from becoming the sole root of trust for consequence-bearing server authorization.

The exact implementation topology belongs to Software Engineering. This study owns the web/federation trust requirements.

## Key rotation and JWKS currentness

Normal key rotation is not compromise recovery.

A safe model must tolerate an overlap where old and new verification keys coexist long enough for valid in-flight artifacts, while preventing indefinite acceptance of retired keys. Cache lifetime, token/assertion lifetime, provider rotation procedure and local verifier behavior must be compatible.

Failure modes:
- new signing key appears before consumers can fetch it;
- stale JWKS causes false rejection;
- old key remains accepted after intended retirement;
- `kid` collision or key substitution selects the wrong key;
- cached metadata points to obsolete endpoints/keys;
- rollback restores a previously valid but retired JWKS/trust-policy generation;
- compromise is misclassified as routine rotation and the compromised authority blesses its successor.

MINTTAP DECISION: do not invent a generic key-overlap duration. It is provider/protocol/product dependent and must be validated against actual token/assertion lifetimes and operational contracts.

## Split-view and equivocation

A federation provider, intermediary, cache, proxy or compromised control plane can expose different valid-looking metadata/trust views to different consumers. Cryptographic validity of each view does not by itself establish non-equivocation.

Operational requirements:
- preserve enough metadata generation/provenance to correlate authorization incidents;
- detect impossible or unauthorized regressions in local trust-policy generation;
- treat materially different concurrent trust views as an incident/reconciliation condition, not last-write-wins;
- do not infer maliciousness solely from divergence: rollout, cache propagation and provider migration can also create transient differences;
- define authoritative resolution outside a possibly compromised cached client view.

`split view detected ≠ attacker proven`; `no split view observed ≠ equivocation impossible`.

## Successor-anchor governance

Planned trust-anchor migration and compromised-anchor recovery are distinct.

### Planned migration
- establish the successor anchor through approved governance;
- define overlap and retirement boundaries;
- preserve historical verification provenance;
- create a new local trust-policy generation;
- reconcile cached/offline clients against the new floor;
- retire old authority for new trust decisions after the approved boundary.

### Compromise
A compromised old anchor cannot be the sole authority that authorizes its successor. Successor trust must come from a surviving independent recovery/governance path. Historical artifacts may need compromise-window classification rather than blanket validity or blanket invalidity.

This consumes 161/165 compromise-recovery principles rather than rewriting them.

## Provider migration and entity continuity

Provider A → B migration can change issuer identifiers, endpoints, keys, subject identifiers and trust anchors. Do not solve this by aliasing A and B globally.

Separate questions:
- Is B a trusted new provider/entity?
- Is subject X under A linked to subject Y under B?
- Does the same local delegation continue?
- Which pending/offline operations were authored under A-era authority?
- Which historical decisions must remain verifiable under A-era metadata?

Each answer can differ. Migration creates new trust/mapping generations even when user-facing organization identity appears unchanged.

## PWA / managed-iPad offline transfer

A long-offline Home Screen PWA may hold stale:
- Service Worker code;
- issuer/entity metadata projections;
- JWKS-derived verification state;
- browser session/token projections;
- local delegation/case state;
- unique flight records/drafts;
- queued consequence-bearing operations.

Reconnect discipline:
1. preserve unique local operational data first;
2. do not use stale local trust metadata as the sole authority to validate current remote mutation rights;
3. obtain current server-side trust/authority floor through a path that does not depend on stale business-state assumptions;
4. refresh federation evidence according to current server policy;
5. compare trust, issuer, delegation, case and queued-operation generations;
6. execute only operations explicitly admitted by current authority;
7. quarantine/preserve non-admitted drafts/operations for review rather than silently deleting them;
8. update Service Worker/app shell independently from semantic authority reconciliation.

No generic claim is made that iPadOS will refresh federation metadata, JWKS, tokens or Service Worker in the background. Physical Safari/Home Screen/MDM behavior remains OPEN.

## UX transfer — Track B

Primary UX should describe user consequences, not protocol internals:

- `Your organization sign-in information needs to be refreshed.`
- `Your saved records are still available on this device.`
- `Submission is paused until access can be checked.`
- `Your organization's sign-in service is temporarily unavailable.`
- `Access changed since this device was last online.`

Do not expose raw issuer URLs, key IDs, trust-chain paths or provider topology unless an authorized support/operator diagnostic surface requires them.

## Privacy / analytics transfer — Track D

Federation diagnostics can become a cross-organization identity graph. Keep operational measurements aggregate/purpose-bounded where possible. Do not use issuer/entity IDs, employee identifiers, pairwise subject mappings or trust-chain topology as marketing/acquisition identifiers.

`security telemetry useful ≠ security telemetry exempt from minimization`.

## MINTTAP DECISION — generic governance

1. Treat federation metadata/trust configuration as versioned security state.
2. Bind metadata to expected issuer/resource and current local trust policy; TLS alone is insufficient.
3. Separate metadata/key freshness from semantic relationship/delegation currentness.
4. Cache federation trust material only with bounded semantics; stale cache is historical observation, not evergreen authority.
5. Distinguish normal key rotation, provider migration and compromise recovery.
6. A compromised authority cannot be the sole source of successor trust.
7. Treat materially inconsistent concurrent trust views as reconciliation/incident conditions rather than last-write-wins.
8. Preserve unique offline PWA data while re-establishing current trust before consequence-bearing replay.
9. Keep trust/federation diagnostics out of acquisition identity graphs.
10. Actual MintTap/LogMate federation, issuer, JWKS, trust-anchor, provider, MDM and physical-iPad facts remain OPEN.

## VALIDATION — 136-case destructive campaign

1 correct issuer metadata; 2 issuer mismatch; 3 scheme downgrade; 4 redirect to unexpected origin; 5 metadata 404; 6 malformed JSON; 7 oversized metadata; 8 duplicate fields; 9 unknown fields; 10 signed metadata valid; 11 signed metadata invalid; 12 signed/plain conflict; 13 stale signed metadata; 14 wrong signer; 15 expected issuer changed; 16 resource mismatch; 17 unexpected authorization server; 18 endpoint substitution; 19 jwks_uri substitution; 20 JWKS unavailable; 21 malformed JWKS; 22 empty JWKS; 23 duplicate kid; 24 unknown kid; 25 wrong alg; 26 prohibited alg; 27 new key before cache refresh; 28 old key overlap; 29 old key retirement; 30 old key accepted too long; 31 key removed too early; 32 rotation during outage; 33 rotation during offline period; 34 compromise misclassified as rotation; 35 key rollback; 36 metadata rollback; 37 local trust-policy rollback; 38 cache-control stale; 39 intermediary stale cache; 40 browser cache stale; 41 Service Worker stale; 42 IndexedDB stale projection; 43 PITR restores old metadata; 44 backup restores old trust config; 45 config deployment partial; 46 multi-region propagation lag; 47 split-view metadata; 48 split-view JWKS; 49 split-view trust chain; 50 split-view local policy; 51 divergent but legitimate rollout; 52 divergence after compromise; 53 one valid chain; 54 two valid chains; 55 invalid intermediate; 56 expired Entity Statement; 57 future iat/clock skew; 58 missing trust anchor; 59 wrong trust anchor; 60 retired trust anchor; 61 anchor planned migration; 62 anchor overlap; 63 anchor retirement; 64 anchor compromise; 65 compromised anchor blesses successor; 66 independent successor recovery; 67 historical artifact under old anchor; 68 compromise-window ambiguity; 69 provider A→B migration; 70 same email under B; 71 changed subject ID; 72 subject collision; 73 old token under B; 74 old queue under B; 75 old local delegation under B; 76 explicit new mapping generation; 77 migration rollback; 78 rollback after compromise; 79 broker normal; 80 broker outage; 81 broker compromise; 82 broker strips provenance; 83 broker changes upstream; 84 provider DNS outage; 85 provider TLS failure; 86 provider metadata outage; 87 JWKS-only outage; 88 partial recovery; 89 stale provider replica; 90 currentness unknown; 91 fail-open attempt; 92 bounded degraded read; 93 high-consequence mutation blocked; 94 unique local record readable; 95 unique local export preserved; 96 offline cold start; 97 long-offline iPad; 98 reconnect same generation; 99 reconnect one-generation jump; 100 reconnect multi-generation jump; 101 stale SW + current server; 102 current SW + stale semantic state; 103 metadata refresh before authority floor; 104 authority floor before metadata refresh; 105 queued operation authorized then revoked; 106 re-delegated same actor; 107 old queue remains non-executable; 108 explicit resubmission; 109 duplicate reconnect; 110 lost ACK; 111 retry after trust change; 112 account recovery plus provider migration; 113 MDM still active/user revoked; 114 device ownership change; 115 Shared iPad user switch; 116 Temporary Session; 117 notification stale provider state; 118 support sees raw issuer data; 119 user UI leaks issuer topology; 120 analytics captures subject mapping; 121 analytics captures issuer graph; 122 logs capture bearer token; 123 logs capture full JWKS unnecessarily; 124 incident evidence minimized; 125 metadata endpoint SSRF attempt in server fetcher; 126 private-network target; 127 redirect loop; 128 DNS rebinding consideration; 129 accessibility of degraded-state notice; 130 keyboard recovery path; 131 screen-reader status; 132 reduced-motion/no visual-only trust status; 133 Safari physical-device run; 134 managed Home Screen run; 135 provider contract/currentness validation; 136 human comprehension of stale-vs-revoked state.

Generic campaign definition is PASS. Execution against actual product/provider/browser/device remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION

- **TRANSFER VALIDATION:** 171's `federation evidence ≠ local authority` remains valid and is strengthened: the evidence's metadata/trust context itself has currentness and lineage.
- **TRANSFER VALIDATION:** 161/165 successor-trust rule applies to federation anchors/providers: compromised old authority cannot self-authorize recovery.
- **TRANSFER VALIDATION:** 170's offline queue rule remains: authored-while-authorized does not imply authorized-at-commit.
- **CONTRADICTION:** `JWKS endpoint reachable, therefore trust healthy` is rejected. Reachability, authenticity, freshness, issuer binding and semantic authorization are distinct.
- **CONTRADICTION:** `OpenID Federation trust chain valid, therefore LogMate delegation valid` is rejected. Federation membership/trust is upstream evidence; local case authority remains a separate decision.

## OPEN / DEPENDENCY / CHANGE WATCH

### OPEN
- actual MintTap/LogMate identity/federation architecture;
- actual airline/employer/IdP federation contracts and claim authority;
- actual issuer/JWKS/metadata cache behavior;
- actual local trust-anchor/recovery governance;
- actual managed-iPad Safari/Home Screen behavior;
- actual legal/aviation implications of delegated authority;
- physical browser/device/AT/human validation.

### DEPENDENCY
- Software Engineering: implementation-level metadata/JWKS cache, SSRF, token and trust-store design when a real architecture exists;
- Design Studio: accessible degraded/currentness/review-required presentation;
- provider/security/legal owners: authoritative currentness/revocation and successor-trust contracts.

### CHANGE WATCH
- OpenID Federation ecosystem/provider adoption and interoperability;
- OAuth/OIDC metadata/security BCP evolution;
- Safari/iPadOS PWA lifecycle and background behavior;
- NIST digital-identity guidance updates.

## Next adjacent bottleneck

**Federation trust-policy distribution, rollback resistance & multi-region/offline convergence**: determine how local trust-policy generations reach servers and long-offline PWA clients without split-brain authorization, how emergency revoke/anchor changes propagate under partial outage, and how to prove convergence without making client cache state an authority oracle.