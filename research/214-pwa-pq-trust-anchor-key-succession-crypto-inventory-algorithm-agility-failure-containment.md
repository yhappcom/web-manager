# 214 — PWA PQ Trust-Anchor/Key Succession, Crypto-Inventory Completeness & Algorithm-Agility Failure Containment

Status: **PASS (generic) / PRODUCT + CRYPTO-INVENTORY + PQ-KEY/ANCHOR + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A crypto/runtime mechanics; Track B recovery/update communication; Track C destructive assurance; Track D inventory/migration observation.  
Dependencies: 137, 205–213 and the earlier authority/currentness/recovery chain.

## Problem
213 established that PQ transition is a policy/lineage transition rather than an algorithm-name swap. The adjacent operational failure is harder: what happens after a PQ key, trust anchor, provider implementation or PQ algorithm family itself becomes suspect, while retired classical paths still exist for historical verification or compatibility?

Central rule: **crypto agility is the ability to replace cryptographic mechanisms while preserving security and operations; it is not permission to accept every mechanism ever supported. Failure containment therefore requires authenticated successor policy, explicit acceptance floors, complete-enough cryptographic inventory and bounded legacy verification.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/WebCrypto/WebKit/server/provider support determines executable migration paths but cannot authorize downgrade.
- **B UX/IA/Content:** high dependency pressure. Must distinguish current, migration-required, legacy-verify-only, quarantined and unknown crypto states without implying that fallback equals recovery.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **472 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can measure inventory coverage, unknowns, legacy tails and fallback events; telemetry cannot prove inventory completeness or cryptographic validity.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns successor authority, algorithm/key failure containment, inventory governance, downgrade boundaries and retirement.

## SOURCE

### NIST CSWP 39upd1 — current crypto-agility baseline
NIST CSWP 39upd1, *Considerations for Achieving Crypto Agility: Strategies and Practices*, is final as of 2026-06-29 and supersedes the original CSWP 39. NIST defines crypto agility as capabilities needed to replace/adapt cryptographic algorithms in protocols, applications, software, hardware, firmware and infrastructures while preserving security and ongoing operations. It emphasizes environment-specific mechanisms, challenges and trade-offs rather than a universal switch.

Sources:
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://csrc.nist.gov/Projects/crypto-agility/publications

**TRANSFER VALIDATION:** this supports designing replaceability and operational transition. It does not authorize legacy fallback, choose MintTap algorithms, or establish product runtime support.

### NCCoE Migration to PQC — discovery/inventory is a first-class workstream
NCCoE's Migration to Post-Quantum Cryptography project separates cryptographic discovery from interoperability. The discovery workstream evaluates inventory tools to identify where/how cryptography protects important data and systems and to support risk/prioritization. Interoperability work tests PQ implementations in controlled non-production environments.

Sources:
- https://www.nccoe.nist.gov/applied-cryptography/migration-to-pqc
- https://pages.nist.gov/nccoe-migration-post-quantum-cryptography/

**TRANSFER VALIDATION:** inventory is not paperwork after migration; it is a prerequisite for knowing what must migrate and for finding hidden quantum-vulnerable dependencies. Automated discovery is useful but not proof of completeness.

### NIST's HQC selection illustrates algorithm-family contingency, bounded to KEMs
NIST selected HQC in 2025 as a future backup KEM based on different mathematics from ML-KEM, explicitly citing the value of a second line of defense if a weakness were found in ML-KEM. This is KEM/encryption evidence, not a direct signature-policy rule.

Source:
- https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption

**TRANSFER VALIDATION:** diversity can reduce common-mode cryptanalytic dependency. It does not imply that deploying two algorithms automatically creates safe failover, nor that HQC is relevant to signature succession.

## SYNTHESIS 1 — separate key compromise, anchor compromise, implementation defect and algorithm-family failure
These incidents have different blast radii:
- one private key compromise may require key succession within the same algorithm/policy;
- trust-anchor compromise can invalidate a wider authorization root and may require reconstitution rather than ordinary succession;
- provider/library implementation failure may affect keys/operations produced by that implementation without proving the underlying algorithm broken;
- cryptanalytic failure of an algorithm family can invalidate every acceptance path relying on that family for the affected purpose.

Do not collapse all four into `crypto failure`.

`key compromised ≠ algorithm broken`; `provider defect ≠ mathematical break`; `anchor compromised ≠ ordinary leaf rotation`.

## SYNTHESIS 2 — successor authority cannot be derived solely from the failed mechanism
If PQ anchor P1 is merely scheduled for rotation and remains trusted, authenticated P1→P2 succession can be ordinary. If P1 is compromised beyond its authorized threshold, P1 alone cannot prove that P2 is the legitimate successor; that re-enters the independent recovery/reconstitution model from 205–208.

Likewise, if algorithm A is cryptanalytically broken for the relevant claim, an A-signed statement saying `trust algorithm B` cannot by itself restore confidence. Successor trust needs an independent still-supportable path or pre-established transition lineage.

`failed authority signs successor ≠ successor trusted`; `newer key ≠ legitimate successor`.

## SYNTHESIS 3 — retired classical authority remains historical, not an emergency fallback
PQ failure creates pressure to re-enable an older classical verifier/key because it is familiar and available. That is unsafe once the classical path has been retired from current authority. Historical verification support may remain, but it must not become a current signing/bootstrap/recovery path merely because the PQ path is degraded.

`PQ incident ≠ classical authority restored`; `legacy verifier available ≠ legacy authority available`.

## SYNTHESIS 4 — crypto agility requires an acceptance matrix, not a bag of algorithms
For each object/purpose/generation, define which algorithm/key/anchor combinations are:
- REQUIRED CURRENT;
- TRANSITION-ACCEPTABLE;
- HISTORICAL VERIFY-ONLY;
- QUARANTINED;
- RETIRED/REJECTED;
- UNKNOWN.

The matrix must be versioned and authenticated. Supporting a parser or verifier for an old algorithm does not imply acceptance for new objects. Multi-algorithm code without explicit policy expands downgrade surface.

`algorithm supported ≠ algorithm accepted`; `parser available ≠ authority available`; `agility ≠ universal fallback`.

## SYNTHESIS 5 — inventory completeness is a claim with evidence, not a binary fact
A useful crypto inventory spans at least:
1. public endpoints/TLS and certificates;
2. API/service-to-service cryptography;
3. application signatures/tokens/session artifacts;
4. package/build/update signing and CI/CD;
5. TSA/checkpoints/transparency/evidence preservation;
6. database/storage/backup/export encryption and signatures;
7. KMS/HSM/secret-manager keys and aliases;
8. mobile/PWA/browser/local persisted crypto state;
9. MDM/enterprise provisioning/bootstrap certificates and profiles;
10. third-party SaaS/provider cryptography and transitive dependencies;
11. offline media, disaster-recovery material and historical verifier bundles;
12. source/config/schema/protocol algorithm identifiers and implicit defaults.

Completeness requires reconciling multiple evidence planes. A scanner sees only what its vantage point exposes.

`scan complete ≠ inventory complete`; `CMDB entry exists ≠ cryptographic dependency observed`; `no telemetry ≠ no dependency`.

## SYNTHESIS 6 — use positive and negative inventory evidence
Positive evidence identifies observed crypto use. Negative evidence is equally important during retirement: search source/config, provider inventories, certificate/key stores, artifact formats, backups, offline packages and runtime telemetry for prohibited algorithms/anchors; then test representative flows that must reject them.

Zero observed use is useful only with known coverage and retention windows. Unknown/offline fleets and dormant recovery paths remain explicit tails.

`zero observed legacy use ≠ zero legacy artifacts`; `retirement policy written ≠ retired path extinct`.

## SYNTHESIS 7 — algorithm identifiers and negotiability can become downgrade surfaces
Protocols/libraries often need negotiation or multiple algorithms during transition. The peer, attacker, stale policy or compatibility shim must not be allowed to select a weaker retired path outside authenticated policy. Unknown/unsupported algorithms should fail according to policy rather than silently choosing a familiar predecessor.

`negotiation succeeded ≠ strongest authorized policy used`; `unsupported current algorithm ≠ permission to choose legacy`.

## SYNTHESIS 8 — diversity helps only when failure domains are actually diverse
Two algorithms implemented by the same provider/library, rooted in the same administrative plane, updated through the same supply chain and accepted under the same stale policy can share operational failure modes even if their mathematics differ. Conversely, excessive diversity increases code, test, parser, key-management and incident complexity.

Use diversity to address a named common-mode risk, not as a count metric.

`two algorithms ≠ two independent failure domains`; `more crypto options ≠ more resilience`.

## SYNTHESIS 9 — inventory must bind purpose and consequence
An algorithm name alone is insufficient. Inventory records should bind at least asset/object class, cryptographic purpose, algorithm/parameters, key/anchor identity, provider/library, location, owner, generation/policy, data/evidence horizon, offline/backup presence, current acceptance state and migration dependency.

The same algorithm may be acceptable for historical verification while forbidden for new signatures. Purpose/context determines urgency and retirement semantics.

`same algorithm ≠ same migration priority`; `same key technology ≠ same consequence`.

## SYNTHESIS 10 — long-offline PWA convergence must not reopen retired crypto
A LogMate/EFB-like iPad may return carrying old classical policy C1, hybrid H2, or an early PQ key P1 after the service has moved to P3 because of compromise/deprecation. Preserve unique local flight/logbook data first. Do not treat its cached crypto state, Service Worker, session or receipt as current authority. Obtain current authenticated policy through the surviving bootstrap/recovery basis and re-admit queued work.

If the device cannot verify current policy, degrade remote mutation rather than lowering the server floor. Export/data-preservation paths may remain available if safely scoped.

`offline device stranded ≠ retired crypto reauthorized`; `data rescue ≠ trust downgrade`.

## SYNTHESIS 11 — containment needs a kill path and a recovery path
For each current cryptographic authority, pre-plan:
- detection/alert source;
- scope assessment;
- ability to stop new issuance/signing/acceptance;
- verifier policy update and propagation;
- successor/reconstitution authority;
- handling of in-flight/offline objects;
- historical evidence classification;
- negative tests proving retired path rejection;
- rollback/PITR behavior;
- post-incident inventory reconciliation.

A kill switch without successor trust creates outage; successor support without a reliable kill path leaves the failed authority alive.

`new algorithm deployed ≠ failed algorithm contained`.

## SYNTHESIS 12 — provider/API abstraction can improve replaceability but can also hide dependencies
Central crypto APIs/providers can reduce application-specific coupling, but they can obscure actual algorithms, defaults, key custody or provider-specific semantics. An abstraction layer is useful only if inventory can still answer what was used, where, for what purpose and under which policy.

`crypto API abstraction ≠ crypto inventory`; `provider portability ≠ trust portability`.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. adopt NIST CSWP 39upd1 as the current general crypto-agility precedent, while keeping product choices OPEN;
2. distinguish key, trust-anchor, implementation/provider and algorithm-family failure before selecting recovery action;
3. never let a compromised/broken predecessor alone authorize its successor;
4. never restore retired classical current authority merely because a PQ path fails;
5. maintain a versioned acceptance matrix separating current, transition, historical-verify-only, quarantined, retired and unknown states;
6. build cryptographic inventory from multiple evidence planes and record coverage/unknowns rather than claiming absolute completeness from one scanner;
7. inventory purpose, key/anchor/provider, policy generation, retention horizon, offline/backup presence and migration dependency—not just algorithm names;
8. treat negotiation/fallback as authenticated policy, not library convenience;
9. require positive successor operation plus negative proof that retired/failed paths are rejected in consequence-bearing domains;
10. keep long-offline PWA data preservation separate from current crypto authority;
11. pre-plan containment and recovery for every current cryptographic authority;
12. use algorithm/provider diversity only against named common-mode risks and account for added operational complexity.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
Implementation validation must inventory actual browser/WebKit/WebCrypto/server libraries, algorithm negotiation behavior, certificate/PKI support, provider APIs and persisted client state. API availability does not define authorization policy.

### Track B — DEPENDENCY
Recovery/update UX must communicate `current`, `migration required`, `historical verify-only`, `quarantined`, `unsupported current crypto` and `data preserved but sync blocked` without offering a user-facing insecure fallback. Consume Design Studio evidence for accessible recovery/state communication.

### Track C — VALIDATION
Destructive campaign grows **464 → 472 defined cases**:
1. P1 private key compromise with valid P2 ordinary succession available;
2. P1 trust anchor compromised and attacker self-signs P2;
3. PQ algorithm A is deprecated/broken while legacy classical C remains installed as historical verifier;
4. current verifier lacks algorithm B and silently negotiates retired A/C;
5. inventory scanner reports clean while dormant backup/export/TSA path still emits retired algorithm;
6. two PQ algorithms share one compromised provider/update supply chain despite mathematical diversity;
7. PITR restores old acceptance matrix and re-enables retired algorithm after containment;
8. long-offline iPad returns with unique data plus P1 authority after P1 compromise/P3 current floor.

Execution, physical iPad/Safari, actual libraries/providers, inventory tools, PKI/KMS/TSA, schema/performance and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure discovered assets, coverage by inventory method, unknown/unowned crypto, current/legacy algorithm use, fallback/negotiation events, policy-generation lag, dormant-path exercise results and offline-fleet tails. Telemetry cannot prove cryptographic safety or absolute completeness.

## Persistent guards added through 214
- `key compromised ≠ algorithm broken`;
- `provider defect ≠ mathematical break`;
- `anchor compromised ≠ ordinary leaf rotation`;
- `failed authority signs successor ≠ successor trusted`;
- `newer key ≠ legitimate successor`;
- `PQ incident ≠ classical authority restored`;
- `legacy verifier available ≠ legacy authority available`;
- `algorithm supported ≠ algorithm accepted`;
- `parser available ≠ authority available`;
- `agility ≠ universal fallback`;
- `scan complete ≠ inventory complete`;
- `CMDB entry exists ≠ cryptographic dependency observed`;
- `no telemetry ≠ no dependency`;
- `retirement policy written ≠ retired path extinct`;
- `negotiation succeeded ≠ strongest authorized policy used`;
- `unsupported current algorithm ≠ permission to choose legacy`;
- `two algorithms ≠ two independent failure domains`;
- `more crypto options ≠ more resilience`;
- `same algorithm ≠ same migration priority`;
- `offline device stranded ≠ retired crypto reauthorized`;
- `data rescue ≠ trust downgrade`;
- `new algorithm deployed ≠ failed algorithm contained`;
- `crypto API abstraction ≠ crypto inventory`;
- `provider portability ≠ trust portability`.

## OPEN
- actual MintTap/LogMate cryptographic inventory, owners and coverage;
- actual algorithms/parameters, key sizes, anchors, PKI/KMS/HSM/TSA/checkpoint/update-signing topology;
- actual crypto providers/libraries and common-mode failure domains;
- actual acceptance/negotiation/fallback policy and enforcement points;
- actual offline/backup/export/recovery/historical-verifier crypto tails;
- browser/WebKit/managed-iPad algorithm/provider support;
- containment propagation time, PITR/rollback behavior and negative extinction evidence;
- legal/aviation/privacy retention and cryptographic admissibility requirements;
- physical-device/runtime and human recovery-state validation.

## CHANGE WATCH
- NIST CSWP 39upd1 revisions and future crypto-agility maturity guidance;
- NCCoE Migration to PQC discovery/inventory practice outputs;
- NIST PQC standards, additional signature/KEM standardization and cryptanalytic updates;
- NIST IR 8547 transition-plan progression;
- IETF hybrid/composite and protocol algorithm-negotiation specifications;
- browser/WebCrypto/WebKit/server/provider PQ support and defaults.

## Gate result
**214 PASS (generic).** The Web Manager can now separate PQ key/anchor/provider/algorithm failure classes, require independent successor authority when predecessor trust fails, keep retired classical paths historical-only, model algorithm acceptance explicitly, treat crypto inventory completeness as multi-plane evidence with known unknowns, and contain algorithm-agility fallback risk while preserving long-offline PWA data.

Production validation remains OPEN.

## Next highest-value adjacent question
**215 — cryptographic inventory attestation, shadow-crypto discovery & retirement-proof governance.** Determine how inventory claims themselves are versioned/attested, how unmanaged libraries/scripts/SaaS/offline artifacts and implicit platform cryptography are discovered, how inventory drift becomes a release/incident signal, and what evidence is sufficient to claim that a retired algorithm/anchor is no longer consequence-bearing without pretending absolute absence can be proven.