# 213 — PWA Post-Quantum Preservation Planning, Hybrid-Transition Semantics & Harvest-Now-Forge-Later Risk

Status: **PASS (generic) / PRODUCT + CRYPTO-INVENTORY + PQ-POLICY + HYBRID-FORMAT + PKI/TSA + VERIFIER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A crypto/runtime mechanics; Track B evidence-state communication; Track C destructive assurance; Track D bounded migration observation.  
Dependencies: 137, 211–212 and the earlier authority/currentness/recovery chain.

## Problem
212 established that long-lived evidence must migrate before predecessor protection becomes untrustworthy. The adjacent question is quantum transition: classical public-key signatures that are acceptable today can become forgeable if cryptographically relevant quantum computers arrive during the evidence retention horizon. Long-lived authenticity therefore needs a planning horizon based on exposure/retention/migration time rather than waiting for a classical algorithm to fail in production.

Central rule: **post-quantum migration is a policy and lineage transition, not an algorithm-name swap. Hybrid/dual-stack periods require explicit acceptance semantics, downgrade resistance and preservation of the predecessor evidence chain.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/WebCrypto/WebKit support constrains client-side implementation; lack of API support does not decide evidence validity.
- **B UX/IA/Content:** high dependency pressure. Must distinguish classical-only, hybrid/dual, PQ-current, legacy-verify-only, migration-due and uncertainty without implying unsupported safety claims.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **464 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can observe inventory/migration coverage and downgrade/fallback events, not declare cryptographic validity.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns transition policy, acceptance semantics, lineage, anti-downgrade, crypto inventory and retirement boundaries.

## SOURCE

### NIST finalized PQC standards
NIST finalized FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA) on 2024-08-13. FIPS 204 defines ML-DSA for digital signatures; NIST describes ML-DSA as believed secure against adversaries with a large-scale quantum computer. NIST's PQC project page, updated 2026-08-05, states that organizations should begin migration and identifies 2035 as the planned removal horizon for quantum-vulnerable algorithms under the draft transition plan, with high-risk systems moving earlier.

Sources:
- https://csrc.nist.gov/pubs/fips/204/final
- https://csrc.nist.gov/Projects/post-quantum-cryptography/publications
- https://csrc.nist.gov/projects/post-quantum-cryptography

**TRANSFER VALIDATION:** finalized algorithms make migration planning concrete. They do not select MintTap/LogMate algorithms, key sizes, PKI, certificate format, browser implementation or deadline.

### NIST IR 8547 — transition plan remains draft
NIST IR 8547, *Transition to Post-Quantum Cryptography Standards*, remains an Initial Public Draft dated 2024-11-12. It describes migration away from quantum-vulnerable digital-signature and key-establishment schemes. Its public-comment period is closed, but it has not become a final publication as of this run.

Source:
- https://csrc.nist.gov/pubs/ir/8547/ipd

**CHANGE WATCH:** do not promote draft dates into a MintTap production deadline without final/current policy and inventory evidence.

### NIST 2026 PIV working drafts — dual-stack precedent
On 2026-06-12 NIST published preliminary PIV working drafts for PQC. The proposed approach is dual-stack: preserve existing classical PIV keys/data objects while adding PQC key references, certificate containers and data objects to support backward compatibility and incremental deployment.

Source:
- https://www.nist.gov/news-events/news/2026/06/working-drafts-post-quantum-cryptography-updates-piv-standards

**TRANSFER VALIDATION:** dual-stack is a useful migration precedent, not a MintTap architecture decision and not proof that `classical OR PQ` acceptance is safe for every security claim.

### IETF hybrid signatures are active work, not settled universal semantics
Current September 2026 IETF Internet-Drafts include JOSE/COSE PQ/T composite signatures combining ML-DSA with ECDSA or EdDSA, and CFRG work on strongly-unforgeable hybrid signature constructions. These are work in progress and may change.

Sources:
- https://www.ietf.org/ietf-ftp/internet-drafts/draft-ietf-jose-pq-composite-sigs-04.html
- https://www.ietf.org/ietf-ftp/internet-drafts/draft-prabel-cfrg-suf-hybrid-sigs-02.html

**CHANGE WATCH:** serialization and construction details remain draft. Do not freeze a product format from an Internet-Draft.

## SYNTHESIS 1 — separate confidentiality harvest-now-decrypt-later from authenticity harvest-now-forge-later
Encrypted data can be captured now and decrypted later if its confidentiality horizon extends beyond the arrival of a capable quantum adversary. Signed evidence has a different risk: old authentic objects can remain available, while a future attacker may gain the ability to forge classical signatures that appear compatible with historical objects unless trustworthy timing/preservation lineage establishes that the evidence existed before the break.

For long-lived evidence, the planning question is not merely `is classical signature secure today?`; it is `will the authenticity claim remain distinguishable from a future forgery for its required horizon?`.

`harvest-now-decrypt-later ≠ harvest-now-forge-later`; `signature verifies mathematically later ≠ historical provenance remains trustworthy later`.

## SYNTHESIS 2 — use horizon arithmetic as a planning model, not a quantum-date prediction
Inventory each evidence class by at least: creation/signing algorithm; expected authenticity/retention horizon; time needed to discover inventory; design/build/deploy migration; offline-fleet convergence; archive re-attestation; validation margin; and consequence if forgery becomes plausible.

A generic migration trigger should leave enough time to complete preservation before predecessor trust becomes questionable. Do not invent a quantum-computer arrival date. Use authoritative transition policy plus product retention/exposure and migration lead time.

`unknown quantum date ≠ permission to defer inventory`; `2035 policy horizon ≠ every evidence class may wait until 2035`.

## SYNTHESIS 3 — hybrid acceptance semantics must be explicit
A package carrying classical C and PQ P components can implement materially different policies:
- **AND:** require C and P;
- **OR:** accept either C or P;
- **policy-by-epoch:** require a defined combination for a specific transition generation;
- **preservation lineage:** accept historical C only when authenticated preservation evidence binds it into a later PQ-capable chain.

These are not interchangeable. If a verifier silently falls back from `C AND P` to `C OR P`, the PQ component can become decorative and classical compromise can still authorize the object.

`two signatures present ≠ two signatures required`; `hybrid format ≠ hybrid security`; `algorithm agility ≠ fallback permission`.

## SYNTHESIS 4 — AND is not automatically the universal answer
Requiring both components can preserve security when one component remains secure, depending on the exact construction and verification semantics, but it also creates availability/compatibility dependencies and can complicate long-offline migration. OR semantics may be appropriate only for explicitly scoped compatibility states and can preserve the weakest accepted path as an attack path.

Therefore acceptance belongs to a versioned policy bound to object type, generation and purpose. Do not infer security from the word `hybrid` alone.

## SYNTHESIS 5 — bind component identity, policy and message context
A transition object must unambiguously bind the same intended evidence/object, component algorithm identifiers/parameters, key/anchor identities, transition policy/generation, purpose/domain and predecessor lineage. Independent signatures over subtly different serialization/context can create substitution ambiguity.

Current IETF hybrid-signature work itself illustrates that composition details matter; generic concatenation is not a sufficient architecture specification.

`C verifies + P verifies ≠ both authenticated the same semantic statement`; `same display text ≠ same signed bytes/context`.

## SYNTHESIS 6 — downgrade resistance spans verifier, policy and distribution
An attacker may strip the PQ component, present an older classical-only policy, route to a stale verifier, exploit unsupported-algorithm fallback, or target an offline client that never learned the PQ-required epoch. Anti-downgrade therefore needs authenticated policy lineage and currentness, not merely an `alg` field.

Once an enforcement domain has admitted a PQ-required generation, an authentic older classical-only generation must not silently regain current authority.

`PQ unsupported locally ≠ classical fallback authorized`; `old object authentic ≠ old acceptance policy current`.

## SYNTHESIS 7 — preservation migration can protect old classical evidence without rewriting it
For historical classical evidence that must outlive the classical security horizon, retain the original bytes/signature and create authenticated preservation evidence while the classical chain remains supportable. The successor PQ-capable layer attests to the predecessor evidence and migration context; it does not claim the original event was PQ-signed.

This carries forward 212's RFC 4998 principle: migration after predecessor break cannot retroactively create continuity.

`PQ re-attested ≠ originally PQ-signed`; `PQ wrapper valid ≠ classical compromise window erased`.

## SYNTHESIS 8 — PQ migration has implementation and performance consequences but those do not set trust policy
PQC signatures/keys/certificates can change artifact size, parsing, storage, bandwidth, verification cost, cache behavior, schema limits and browser/server library compatibility. These require Track A/C and Software Engineering execution evidence. Performance pressure must not silently weaken acceptance semantics.

`larger/slower ≠ unsafe`; `fast fallback ≠ authorized fallback`.

## SYNTHESIS 9 — long-offline PWA convergence remains current-authority-first
A LogMate/EFB-like iPad may leave during classical-only epoch C1 and return after hybrid H2 and PQ-required P3. Preserve unique local flight/logbook data first. Treat its classical signatures/receipts as historical evidence, not current synchronization authority. Obtain current authenticated policy/authority, isolate stale session/Service Worker/security assumptions, and re-admit queued mutations under current rules.

The client need not execute every missed crypto epoch merely to preserve data, but the server must not lower the current floor to accommodate it.

`offline client lacks PQ support ≠ server restores classical authority`; `data preservation ≠ authority preservation`.

## SYNTHESIS 10 — erased/new clients are bootstrap-policy problems
A zero-state client has no durable local floor with which to reject a classical-only downgrade. Its bootstrap basis must authenticate the current transition policy or an authorized lineage to it. This remains the recovery/bootstrap problem from 206–208; PQ does not remove the need for an initial trust basis.

`PQC algorithm present ≠ bootstrap authentic`; `newest-looking PQ package ≠ authorized current policy`.

## SYNTHESIS 11 — inventory before migration
The useful first production step is not mass algorithm replacement. Build a cryptographic inventory identifying signatures, KEMs/encryption, TLS dependencies, certificates, TSA/checkpoints, package/update signing, backup/export evidence, retained historical evidence, browser/client verifier support, libraries/providers and offline-fleet tails. Classify by confidentiality/authenticity horizon and consequence.

Without inventory, a nominal PQ rollout can leave hidden classical authority paths.

`primary API migrated ≠ cryptographic estate migrated`; `online fleet PQ-capable ≠ archive/offline fleet transition complete`.

## SYNTHESIS 12 — standards maturity must remain visible
FIPS 203/204/205 are final. NIST IR 8547 is draft. The 2026 PIV PQC materials are preliminary working drafts. Current IETF hybrid-signature formats/constructions cited here are Internet-Drafts. Product decisions must preserve these maturity distinctions.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. begin/maintain a crypto inventory now for any long-lived authenticity/confidentiality claim; do not wait for a quantum-date prediction;
2. treat FIPS 203/204/205 as final standards evidence but do not select algorithms or product formats without product requirements and implementation validation;
3. model authenticity horizon separately from confidentiality horizon;
4. preserve original classical evidence and add authenticated PQ-capable preservation lineage rather than rewriting provenance;
5. make hybrid/dual-stack acceptance semantics explicit, versioned and purpose-scoped; never infer them from component presence;
6. bind transition policy, component identities, exact object/context and predecessor lineage;
7. make fallback/downgrade a policy decision, never an automatic response to unsupported PQ algorithms;
8. prevent stale classical-only policy/verifiers from regaining current authority after a PQ-required floor is admitted;
9. keep offline PWA data preservation separate from current crypto authority and re-admit queued work after current-policy bootstrap;
10. treat NIST transition drafts and IETF hybrid drafts as CHANGE WATCH, not frozen MintTap specifications;
11. validate size/performance/schema/library/browser effects before production rollout without allowing performance pressure to weaken trust semantics;
12. preserve `UNKNOWN/UNCERTAIN/LEGACY-VERIFY-ONLY` states where continuity cannot be established.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
Validate exact browser/WebKit/WebCrypto/library support only when implementation work begins. Server-side or isolated verifier support may be required; browser API absence does not define cryptographic invalidity.

### Track B — DEPENDENCY
Future UX must communicate `classical historical`, `hybrid transition`, `PQ current`, `migration due`, `legacy verify-only` and uncertainty without promising quantum safety from a badge. Consume Design Studio interaction/accessibility evidence.

### Track C — VALIDATION
Destructive campaign grows **456 → 464 defined cases**:
1. object carries C+P but verifier accepts C alone after P stripping;
2. authenticated stale classical-only policy is replayed after PQ-required floor;
3. C and P signatures verify but bind different canonicalized/contextual statements;
4. verifier/library lacks PQ support and silently falls back to classical;
5. PQ preservation wrapper is created only after predecessor classical protection becomes untrustworthy;
6. migration inventory misses TSA/checkpoint/update-signing classical authority path;
7. long-offline iPad returns C1-only after H2/P3 with unique local records;
8. erased/zero-state iPad is offered authentic old classical bootstrap plus current PQ bootstrap.

Execution, physical iPad/Safari, actual PQ libraries/providers, schema/size/performance, PKI/TSA, product crypto inventory and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure inventory coverage, classical-only tails, hybrid/PQ adoption, fallback/downgrade events, verifier failures, archive migration coverage and offline-fleet lag. Telemetry cannot decide cryptographic validity.

## Persistent guards added through 213
- `harvest-now-decrypt-later ≠ harvest-now-forge-later`;
- `unknown quantum date ≠ permission to defer inventory`;
- `2035 policy horizon ≠ every evidence class may wait until 2035`;
- `two signatures present ≠ two signatures required`;
- `hybrid format ≠ hybrid security`;
- `algorithm agility ≠ fallback permission`;
- `C verifies + P verifies ≠ both authenticated the same semantic statement`;
- `PQ unsupported locally ≠ classical fallback authorized`;
- `old object authentic ≠ old acceptance policy current`;
- `PQ re-attested ≠ originally PQ-signed`;
- `PQ wrapper valid ≠ classical compromise window erased`;
- `offline client lacks PQ support ≠ server restores classical authority`;
- `PQC algorithm present ≠ bootstrap authentic`;
- `primary API migrated ≠ cryptographic estate migrated`;
- `online fleet PQ-capable ≠ archive/offline fleet transition complete`.

## OPEN
- actual MintTap/LogMate cryptographic inventory and required confidentiality/authenticity horizons;
- actual algorithms, key sizes, certificates, TSA/checkpoint/update-signing and trust-anchor topology;
- actual hybrid/dual-stack/PQ transition policy and serialization;
- browser/WebKit/server/library/provider support and performance;
- evidence schema/canonicalization and preservation format;
- managed-iPad/offline-fleet convergence behavior;
- legal/aviation/privacy retention/admissibility requirements;
- physical-device/runtime and human evidence-state validation.

## CHANGE WATCH
- NIST IR 8547 progression beyond Initial Public Draft and any revised transition dates;
- NIST PQC standards errata/revisions and additional signature/KEM standardization;
- 2026 PIV PQC working drafts becoming formal drafts/final guidance;
- IETF JOSE/COSE/SSH/hybrid-signature drafts and final RFC semantics;
- browser/WebCrypto/platform PQ algorithm support;
- authoritative quantum-risk and government transition guidance.

## Gate result
**213 PASS (generic).** The Web Manager can now distinguish confidentiality and authenticity quantum-transition risks, plan long-lived evidence migration without predicting a quantum date, define hybrid acceptance as explicit policy rather than component presence, preserve predecessor provenance through PQ re-attestation, resist classical downgrade, and keep offline PWA convergence dependent on current authority.

Production validation remains OPEN.

## Next highest-value adjacent question
**214 — PQ trust-anchor/key succession, crypto-inventory completeness & algorithm-agility failure containment.** Determine how PQ key/anchor compromise or algorithm-specific cryptanalytic failure can be contained without collapsing back to retired classical authority; how to prove inventory completeness across hidden signing/TSA/update/export paths; and how a multi-algorithm transition avoids making every supported legacy algorithm a permanent fallback attack surface.