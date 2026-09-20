# 189 — PWA Preservation-Policy Continuity, Trust-Service Exit/Portability & Cross-Provider Re-anchoring

Status: **PASS (generic) / PRODUCT + PROVIDER + LEGAL + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A browser/offline convergence; Track B provider-migration and uncertainty UX; Track C destructive validation; Track D privacy-bounded migration telemetry.
Dependencies: 183–188 exact-artifact lineage, transparency, archive integrity, historical verifier isolation, algorithm retirement, bounded re-attestation and TSA/preservation compromise recovery.

## Problem
188 established that preservation/timestamp services are bounded evidence providers and that compromise creates an evidence-backed uncertainty interval. The adjacent problem is ordinary or forced provider exit. A preservation service may terminate, be replaced, become commercially unavailable, change policy, or transfer obligations. Historical evidence must remain interpretable and portable without allowing the successor provider to silently redefine the predecessor's validation policy, chronology or trust status.

Central rule:

> **Provider migration transfers objects, evidence, applicable historical policy/context and continuity obligations; it does not transfer the predecessor's power to mint new history, nor does successor acceptance retroactively re-authorize predecessor evidence.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Cached provider roots/status/tokens/SW/IndexedDB are observations; reconnect must converge to current server provider/policy generation without promoting stale roots to current authority.
- **B UX/IA/Content:** high-pressure consumer. Owns understandable distinctions among provider changed, historical evidence preserved, historical verification uncertain, local work preserved and remote submission paused.
- **C Performance/Accessibility/Quality:** validator. Owns exit/transfer, split-provider, stale-client, restore, privacy and AT/human campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Migration telemetry must not contain raw evidence or stable user/device/flight dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns exit planning, transfer completeness, historical-policy continuity, successor admission, decommissioning and cross-provider recovery.

## SOURCE
### RFC 4810 — Long-Term Archive Service Requirements
RFC 4810 §4.6 explicitly requires transfer of archived data objects, associated evidence and evidence records from one archive service to another. Evidence records must be able to span multiple providers without losing evidentiary value. The rationale covers both provider cessation and voluntary provider change.

Source: https://www.rfc-editor.org/rfc/rfc4810.html

### RFC 4998 — Evidence Record Syntax
RFC 4998 defines timestamp/hash-tree renewal so long-term evidence can survive weakening algorithms and expiring timestamp credentials. Renewal preserves prior evidence through a time-ordered chain; it does not redefine the semantics or original authority of the preserved object.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

### RFC 3161 — Time-Stamp Protocol
RFC 3161 distinguishes ordinary TSA retirement/cessation from key compromise. For non-compromise revocation reasons such as cessationOfOperation, tokens generated before the revocation time can remain valid under the protocol's stated conditions. Token verification also includes policy acceptability and certificate status; therefore historical interpretation requires the applicable context, not merely token bytes.

Source: https://www.rfc-editor.org/rfc/rfc3161.html

### RFC 3628 — TSA policy/termination precedent
RFC 3628 requires a terminating TSA to minimize disruption, notify affected parties, transfer obligations for event/audit archives to a reliable party, maintain or transfer public-key/certificate availability, destroy TSU private keys and state termination arrangements in its practices. It is Informational and not a universal product mandate, but it provides a useful separation among verification continuity, private signing capability and operational transfer.

Source: https://www.rfc-editor.org/rfc/rfc3628.html

### ETSI TS 119 511 V1.2.1 — preservation-service policy evidence
ETSI TS 119 511 states that where preservation evidence policy cannot be inferred from context it should be included in the preservation evidence and cryptographically protected; it also binds signature-preservation processing to the supported signature-validation policy. This supports carrying exact policy/profile identity across provider migration rather than assuming the successor's current policy describes historical validation.

Source: https://www.etsi.org/deliver/etsi_ts/119500_119599/119511/01.02.01_60/ts_119511v010201p.pdf

### Current EU qualified-trust-service termination precedent
Commission Implementing Regulation (EU) 2025/2530 requires qualified trust service providers to maintain service-specific termination plans, address anticipated/unanticipated and partial/complete termination, keep relevant records accessible/usable, safeguard subscribers, support alternative-provider arrangements where applicable, and prevent further qualified outputs from being created using the terminated provider's signature/seal creation data. Regulation (EU) No 910/2014 as amended also requires relevant information to remain accessible as necessary after provider activities cease for evidence and service continuity.

These are jurisdiction-specific legal requirements for EU qualified trust services, **not a generic MintTap/LogMate mandate**. They are useful current operational precedent for termination planning and portability.

Sources: https://eur-lex.europa.eu/eli/reg_impl/2025/2530/oj ; https://eur-lex.europa.eu/eli/reg/2014/910/2024-05-20/eng

## SYNTHESIS — what must travel and what must not
A defensible migration package may need distinct layers:
1. original preserved object/evidence identity;
2. original signatures/timestamp/evidence records;
3. predecessor provider/service/policy/profile identity;
4. historical trust anchors and certificate/status material required for verification;
5. applicable algorithm/canonicalization/verifier context;
6. audit/incident/compromise/cessation metadata relevant to interpretation;
7. deletion/retention/legal-hold state where applicable;
8. transfer manifest/provenance and completeness evidence;
9. successor receipt/admission result;
10. later successor renewal/re-attestation as a **new** preservation assertion;
11. current server admission/security generation, kept separate from historical preservation context.

Do **not** transfer predecessor private signing authority merely because verification continuity is required. Historical public verification material and old policy may remain necessary while predecessor private keys/signing capability are destroyed or disabled.

Persistent guards:
- `provider exit complete ≠ historical evidence disposable`;
- `historical evidence portable ≠ predecessor signing authority portable`;
- `successor accepted package ≠ predecessor evidence retroactively re-authorized`;
- `successor re-attested package ≠ original chronology rewritten`;
- `same evidence bytes ≠ same validation policy context`;
- `same policy name ≠ same policy version/semantics`;
- `public verifier retained ≠ obsolete provider may issue new outputs`;
- `termination ≠ compromise`;
- `provider unavailable ≠ historical evidence invalid by default`;
- `transfer structurally complete ≠ transfer semantically complete`;
- `archive export succeeded ≠ all status/audit/policy dependencies exported`;
- `old provider root verifies history ≠ old provider root belongs on current admission path`;
- `client cached old root ≠ provider migration rolled back`.

## Provider lifecycle states must remain distinct
At minimum distinguish:
- planned provider replacement;
- provider cessation without compromise;
- unanticipated provider failure/bankruptcy;
- partial service termination;
- complete termination;
- provider/key compromise;
- policy/profile retirement;
- algorithm/key migration;
- legal/organizational succession.

These states can overlap but are not interchangeable. Ordinary cessation may preserve validity of earlier evidence under the applicable historical policy, while compromise can create an UNKNOWN interval. A successor provider cannot collapse those states into a single `migrated=true` flag.

## Cross-provider re-anchoring
Generic safe sequence:
1. freeze the exact predecessor service/policy generation and define the migration scope;
2. export original objects plus evidence, policy/profile identifiers, verification/status/audit dependencies and known incident/cessation metadata;
3. independently verify package identity and transfer completeness before predecessor shutdown where possible;
4. establish the successor provider/service/policy as a **new current preservation generation** through current authorized governance;
5. bind successor renewal/re-attestation to the exact predecessor evidence/package identity and explicitly preserve predecessor validity/UNKNOWN/INVALID state;
6. publish transfer lineage and successor generation without claiming the successor authored predecessor chronology;
7. reconcile archives/regions/clients to the new current preservation generation;
8. remove predecessor signing capability from current issuance/admission paths while retaining bounded historical verification material as required;
9. verify that PITR, caches and old clients cannot reactivate predecessor issuance/current trust;
10. retain migration/termination evidence for the governed period and validate restore/recovery.

A successor can preserve continuity **from** predecessor evidence. It cannot create trustworthy evidence **about a time before its own trustworthy observation** unless that conclusion is supported by the predecessor chain and applicable policy.

## Policy continuity
Provider portability is not only data portability. Historical validation can depend on policy OIDs/identifiers, profile versions, certificate/status semantics, algorithm-suitability policy, canonicalization, trust-anchor state and audit evidence.

Migration therefore needs immutable or otherwise authenticated references to the historical policy context. If the exact policy cannot be recovered, affected evidence may remain parseable but its historical validation result can become `UNKNOWN`.

`successor implements equivalent controls` is not enough to assert `successor reproduces predecessor historical policy` unless equivalence is actually evidenced.

## Exit planning and decommissioning
Exit readiness should be designed before provider failure. Generic requirements include:
- documented export format and dependency inventory;
- ability to verify export completeness independently of the departing provider;
- retained public verification/status material for historical evidence where required;
- successor/import compatibility tests;
- decommissioning that prevents new outputs under terminated provider keys;
- handling of audit/incident records and privacy/retention obligations;
- tested recovery when the provider disappears without a cooperative export window.

A commercial backup/export checkbox is not evidence of portability until a representative transfer and verification path is exercised.

## PWA/EFB boundary
A long-offline company iPad can miss the entire provider migration. It may return with predecessor certificates, timestamp tokens, preservation envelopes, cached status and an obsolete Service Worker.

Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. classify cached provider material as historical observation only;
3. obtain current authenticated server security/preservation/provider generation;
4. reconcile any predecessor evidence against server-known transfer lineage, cessation/compromise state and current historical-verification policy;
5. migrate local metadata only when needed for compatibility; do not rewrite original evidence bytes/chronology merely to match the new provider;
6. keep predecessor verification material isolated from current remote-admission/signing capability;
7. re-admit queued consequence-bearing operations under current server authority after reconciliation.

Do not assume background provider migration, certificate/status refresh or renewal can execute while an iPadOS Home Screen app is suspended/offline. Physical Safari/Home Screen/MDM evidence remains OPEN.

## Privacy and minimization
Provider exit can tempt bulk replication of raw archives to multiple vendors. Portability does not justify uncontrolled duplication. Transfer scope, temporary staging copies, provider logs, stable identifiers, retention expiry and deletion verification must remain governed.

Migration telemetry should prefer low-cardinality state such as migration generation, package class/count, verification outcome and error class. Raw flight/user/location evidence should not become analytics payload merely because a migration is being monitored.

## Track C destructive campaign
Define a **272-case generic campaign** extending the 264-case baseline with:
- planned provider exit with clean predecessor state;
- abrupt provider bankruptcy/no export window;
- partial vs complete termination confusion;
- predecessor policy/profile omitted from export;
- status/CRL/OCSP/audit dependencies unavailable after exit;
- successor silently applies its current policy to predecessor history;
- same policy label but changed semantics;
- transfer manifest omits an evidence segment;
- package bytes preserved but canonicalization/verifier context lost;
- successor re-attestation launders predecessor UNKNOWN/INVALID;
- predecessor private signing key remains usable after termination;
- predecessor public verifier incorrectly removed;
- PITR resurrects predecessor as current provider;
- region A uses successor while region B still issues through predecessor;
- stale CDN/SW/IndexedDB republishes predecessor currentness;
- long-offline iPad returns after multiple provider/policy generations;
- queue drains before provider/security reconciliation;
- uncooperative provider export differs from documented format;
- migration staging copy violates retention/deletion policy;
- provider-to-provider transfer leaks stable user/device/flight identity;
- screen reader/human operator cannot distinguish `provider changed` from `historical evidence invalid`;
- operational urgency pressures acceptance of incomplete migration package.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat preservation-provider exit as a planned lifecycle state, not only an incident response problem.
2. Require portability of original evidence **and its applicable historical validation context**, not only object bytes.
3. Keep predecessor historical verification capability separate from predecessor current signing/admission capability.
4. Establish successor service/policy as a new preservation generation; never let successor acceptance or re-attestation rewrite predecessor chronology or validity state.
5. Distinguish ordinary cessation, unanticipated failure and compromise; preserve UNKNOWN intervals where evidence requires them.
6. Require transfer provenance/completeness evidence and test representative cross-provider restore/import before relying on portability claims.
7. Reconcile PITR/regions/caches/clients against the current provider/security floor before reopening consequence-bearing work.
8. Preserve unique local PWA/EFB data during provider migration; stale cached roots/tokens are observations only.
9. Minimize migration copies and telemetry; portability is not permission for indefinite multi-provider duplication.
10. Keep exact MintTap/LogMate provider choice, legal profile, evidence duration, algorithms, policy identifiers, transfer format and managed-iPad behavior OPEN until project/runtime evidence exists.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate requires any external preservation/TSA provider: **OPEN**.
- Actual provider/service/policy/profile and legal/aviation evidentiary obligations: **OPEN / legal + product dependency**.
- Exact portable package/schema/canonicalization/verifier and import tooling: **Software Engineering dependency**.
- Ability to independently verify provider export completeness: **OPEN**.
- Cross-provider compatibility and re-attestation semantics: **OPEN / provider + crypto + legal dependency**.
- Historical certificate/status/audit availability after provider exit: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM long-offline behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 272-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- Trust-service termination/portability requirements vary by jurisdiction and profile. EU qualified-trust-service requirements are current legal precedent, not a universal rule.
- Commission Implementing Regulation (EU) 2025/2530 is a current 2025 termination-plan requirement for EU qualified trust services; implementation/legal applicability must be checked at project time.
- ETSI preservation profiles and trust-service standards evolve; exact current version/profile must be checked before implementation.
- Browser/iPadOS background, storage and certificate/status behavior remains change-sensitive.
- PQC and algorithm-suitability transitions can force provider/policy migration independently of commercial provider exit.

## Adjacent next bottleneck
**PWA preservation portability proof, escrow/continuity-provider independence & uncooperative-provider failure recovery**: determine how to prove an export is actually sufficient before the incumbent disappears, how independent escrow/continuity custody avoids sharing the incumbent's failure domain, how to recover when provider APIs/records vanish abruptly, and how offline fleets converge without turning escrow copies or old trust roots into current authority.