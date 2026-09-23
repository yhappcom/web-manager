# 246 — PWA Preservation-Service Compromise, Migration-Chain Fork/Splice Resistance & Verifier-Supply-Chain Reproducibility

Status: **PASS (generic) / PRODUCT + ARCHIVE + VERIFIER + SUPPLY-CHAIN + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A verifier/runtime mechanics; Track B recovery states; Track C destructive validation; Track D privacy-minimized coverage.  
Dependencies: 137, 171–214, 223–245, especially provenance anti-splicing, archive migration, verifier compromise and historical-evidence continuity.

## Problem
245 separated original historical statements from later preservation attestations. The adjacent risk is that the preservation/migration service itself becomes compromised, issues conflicting successor attestations, or emits individually valid migration segments that can be recombined into a false continuity path. A second risk is verifier reproducibility: future investigators may need to reproduce an old verification decision without trusting an opaque binary, package registry, mutable container tag or vulnerable executable as current authority.

Central rule: **preservation continuity is a path claim, not a bag of valid segments. Every successor attestation must bind the exact predecessor identity, transformation/context, branch/generation and intended successor. Reproducibility evidence must identify the verifier/toolchain and inputs sufficiently to reconstruct or independently re-evaluate the historical decision, while keeping legacy execution isolated from current authority paths.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns byte identity, verifier/runtime generation and current bootstrap boundaries; a browser capable of running legacy code does not make that code trusted.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `ARCHIVE-CONFLICT`, `CHAIN-INCOMPLETE`, `VERIFIER-REBUILD-REQUIRED`, `HISTORICAL-ONLY` and `BOOTSTRAP-REQUIRED` states without destructive reset.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive cases; campaign expands **720 → 728 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure chain/migration/verifier coverage with explicit denominator and privacy minimization; coverage cannot establish authenticity or current authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns preservation-service compromise blast radius, path continuity, fork/splice resistance, verifier provenance and isolation.

## SOURCE

### RFC 4998 — Evidence Record Syntax
RFC 4998 treats long-term evidence as ordered Archive Timestamp chains/sequences, requires verification material to be preserved, and renews evidence before older cryptographic mechanisms become unsuitable. It also notes correlated risk across timestamp authorities/algorithms and recommends redundant evidence using different algorithms/TSAs as a mitigation.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

**TRANSFER VALIDATION:** bounded precedent for ordered renewal, predecessor coverage and preserving verification material. ERS is not adopted as MintTap/LogMate protocol, and a central archive service is not assumed trustworthy merely because RFC 4998 discusses one.

### SLSA v1.0 — provenance authenticity, trust boundary and build-platform identity
SLSA v1.0 requires consumers at relevant levels to authenticate provenance and identify the build platform/entities that must be trusted; provenance accuracy depends on generation inside the identified control plane rather than tenant-controlled build steps. It recommends signing approaches that improve compromise detection/remediation, including transparency logs or timestamping where appropriate.

Source: https://slsa.dev/spec/v1.0/requirements

**TRANSFER VALIDATION:** bounded precedent for verifier/build provenance and trust-boundary identification. SLSA is not an archive format and does not by itself prove historical semantic correctness.

### Software Engineering Studio — current bounded implementation evidence
Canonical Software Engineering status on 2026-09-23 remains Foundation IN STUDY with no specialist PASS. Its M006 Safari Service Worker lifecycle evidence was explicitly reopened after a false-green oracle; the repaired regression remained pending at inspection time. This reinforces the distinction between a reproducible tool invocation/workflow and a semantically valid oracle.

Source: `yhappcom/software-engineering-studio/progress/STATUS.md` (2026-09-23).

**TRANSFER VALIDATION:** implementation evidence remains bounded; no Safari/iPadOS/product PASS is promoted here.

## SYNTHESIS 1 — preservation-service signatures do not make the service an unquestionable history oracle
If archive service P issues successor attestations A→B and later appears compromised, scope which objects, generations, time windows and claims depended materially on P. Do not invalidate unrelated evidence automatically, but do not let P self-clear by issuing a new statement that its older output was correct.

Guards: `preservation signature valid ≠ preservation service uncompromised`; `service says history is intact ≠ independent continuity proof`.

## SYNTHESIS 2 — migration continuity is an ordered path claim
Each migration edge should bind at least predecessor object/generation/hash, successor object/generation/hash, transformation identifier and version, verifier/canonicalization context, policy/reason, time evidence where used, and service/operator provenance. Verification must establish an allowed path from the original object to the candidate successor.

`valid edge A→B + valid edge C→D ≠ valid A→D continuity`.

## SYNTHESIS 3 — splice resistance requires transition binding, not segment validity
An attacker may collect legitimate edges from different histories and concatenate them. Segment signatures can all verify while the composite history is false. Reject a path when predecessor/successor identities, branch identifiers, transformation semantics or policy generations do not connect exactly.

`all segment signatures valid ≠ chain continuity valid`; `same friendly record ID ≠ same predecessor object`.

## SYNTHESIS 4 — conflicting successor attestations create a fork, not a timestamp race
If P signs A→B and A→C, do not choose B merely because its timestamp is newer, more clients saw it, or its signature algorithm is stronger. Preserve both, determine whether multi-successor issuance was permitted, examine consequence/branch semantics, and classify unresolved divergence as `ARCHIVE-CONFLICT`.

`newer preservation attestation ≠ canonical successor`; `stronger signature ≠ correct branch`.

## SYNTHESIS 5 — archive-service compromise recovery needs an independent successor basis
A compromised preservation service should not unilaterally authorize its own replacement or re-sign all history into a clean-looking new chain. Successor preservation evidence needs an independently justified trust basis and must retain the old service's affected/unknown interval rather than rewriting it away.

`new archive provider imported everything ≠ old uncertainty erased`.

## SYNTHESIS 6 — verifier reproducibility is more than keeping an executable
Long-term re-evaluation may depend on source revision, build configuration, compiler/runtime, dependencies, platform assumptions, schema, canonicalization, trust inputs, test vectors and the exact oracle/decision procedure. A binary hash identifies bytes but does not explain how they were produced or whether their semantic behavior is trustworthy.

`binary retained ≠ verifier reproducible`; `rebuild succeeds ≠ rebuild semantically equivalent`.

## SYNTHESIS 7 — prefer reconstructable/verifiable environments over permanent legacy execution authority
Preserve source/provenance/dependency identities and, where justified, hermetic or reproducible build evidence so a historical verifier can be reconstructed or cross-checked. If an exact legacy binary/container is retained, quarantine it as evidence/tooling: no production credentials, no current signing keys, no implicit network trust and no current admission authority.

`legacy image retained ≠ legacy image trusted`; `historical tool runnable ≠ historical tool safe on production network`.

## SYNTHESIS 8 — reproducible builds improve confidence but do not prove semantic correctness
Independent rebuilds that match an expected artifact can strengthen the claim that source/configuration produced those bytes. They do not prove the verifier implements the intended historical policy, has no vulnerability, or used a valid oracle. Software Engineering's reopened Safari lifecycle evidence is a concrete reminder that workflow/tool execution and semantic evidence are separate.

`reproducible bytes ≠ correct verifier semantics`; `workflow green ≠ oracle valid`.

## SYNTHESIS 9 — toolchain provenance itself has dependencies and currentness
Compiler, package manager, base image, registry, CI builder and provenance signer can share failure domains. Preserve identities/digests/provenance where material, but do not recursively claim universal certainty. Record blind spots and distinguish `REPRODUCED`, `REBUILT-NONIDENTICAL`, `UNREPRODUCIBLE`, and `SEMANTICS-UNVALIDATED`.

## SYNTHESIS 10 — independent implementations can test semantics without becoming a majority vote
Where a legacy verifier can be specified sufficiently, a separately implemented verifier or test-vector suite may expose parser/canonicalization/toolchain defects. Agreement increases confidence only within the tested claim; disagreement triggers investigation. Two implementations copied from the same flawed parser are not necessarily independent.

## SYNTHESIS 11 — PWA/offline evidence must never depend on executing a stale verifier in the primary app path
A long-offline LogMate-like iPad may return with G12 evidence whose original verifier is no longer shipped. Preserve the bytes/data, bootstrap to current authority, and route historical assessment through a bounded verifier/reconstruction service. Do not sideload an obsolete verifier into the current Service Worker/app shell merely to make sync proceed.

Order: preserve unique flight/logbook data and original evidence → current bootstrap → historical lineage assessment in isolated path → fork/splice checks → schema/data migration → operation-by-operation current re-admission.

## SYNTHESIS 12 — retention and privacy boundaries remain intact
Verifier reproducibility does not justify retaining arbitrary user payloads or entire historical developer machines. Preserve the minimum artifacts/context required for the claim, plus separately justified product/aviation records. Dependency manifests/provenance may be retained without copying unrelated browsing, analytics or device content.

## MINTTAP DECISION
For future MintTap/LogMate historical-evidence preservation, treat archive/migration output as a versioned path with exact predecessor/successor binding and explicit fork detection. A preservation service cannot self-certify through compromise. Preserve verifier source/build/provenance/context sufficiently for bounded reconstruction or independent re-evaluation, but isolate legacy tooling from current authority, credentials and production admission paths. Reproducibility strengthens supply-chain understanding; it never substitutes for semantic oracle validation.

This is generic direction, not a claim that current MintTap/LogMate implements such infrastructure.

## DEPENDENCY / TRANSFER
- **Track A:** expose exact byte/verifier/runtime generations and current bootstrap mechanics.
- **Track B:** communicate archive-conflict/chain-incomplete/verifier-rebuild states without coercive reset.
- **Track C:** execute fork/splice, rebuild, isolation and semantic-oracle destructive tests.
- **Track D:** measure migration/rebuild coverage and missing tails with explicit denominator/privacy limits.
- **Track E:** own preservation-service compromise, successor trust, chain semantics and legacy-tool isolation.
- **Software Engineering:** exact reproducible/hermetic build design, sandboxing, parser implementation and test harnesses remain implementation handoff territory.

## TRACK C DESTRUCTIVE CAMPAIGN ADDITIONS — 720 → 728
1. **Preservation self-clear:** compromised P signs a statement declaring all prior P output safe; expected: self-attestation cannot close compromise uncertainty.
2. **Valid-edge splice:** valid A→B and C→D segments are concatenated as A→D; expected: predecessor/successor transition mismatch rejects path.
3. **Friendly-ID splice:** two histories share a display ID but differ in committed object identity; expected: friendly identifier cannot bridge chains.
4. **Dual-successor laundering:** P signs A→B and A→C; expected: no newest/majority auto-election; enter `ARCHIVE-CONFLICT` unless policy proves both legitimate.
5. **Clean-provider rewrite:** successor archive re-signs imported history and drops old compromise interval; expected: uncertainty/provenance survives migration.
6. **Binary-only reproducibility:** retained verifier binary exists but source/build/dependencies/context are absent; expected: do not claim reproducibility.
7. **Reproducible-wrong oracle:** independent rebuild matches bytes while known semantic test vector fails; expected: reproducibility cannot promote semantic PASS.
8. **Offline-iPad legacy verifier downgrade:** returning iPad can sync only if obsolete verifier is restored to primary path; expected: preserve data, isolate historical verification, require current bootstrap/re-admission.

These are **defined cases, not executed PASS evidence**.

## VALIDATION
Generic gate PASS requires ability to diagnose preservation-service compromise without blanket invalidation/self-clear, reject chain splicing despite individually valid signatures, preserve fork evidence, distinguish archive migration from current authority, specify reproducible-verifier evidence without trusting legacy executables, and keep returning PWA data safe without verifier downgrade.

Production validation remains OPEN for actual archive providers, schema/canonicalization, verifier source/build graph, signing/timestamp services, trust roots, CI/build provenance, parser sandbox, managed iPad/iPadOS/WebKit/MDM, Service Worker/update/storage behavior and LogMate data/rejoin semantics.

## CHANGE WATCH
- SLSA/provenance specifications and tooling evolve; verify current version before implementation.
- Cryptographic/timestamp/archive guidance and algorithm suitability change over time.
- Browser/iOS/iPadOS PWA behavior remains platform-specific and must be physically validated.

## OPEN
Highest-value adjacent question: **247 — verifier-reconstruction sandbox integrity, historical dependency acquisition & semantic differential validation**: how to obtain/build retired dependencies without trusting mutable registries, execute vulnerable historical verifiers without granting them current credentials/network authority, and use independent test vectors/differential implementations to distinguish reproducible bytes from reproduced historical semantics.