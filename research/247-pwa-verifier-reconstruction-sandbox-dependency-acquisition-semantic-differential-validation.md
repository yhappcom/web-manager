# 247 — PWA Verifier-Reconstruction Sandbox Integrity, Historical Dependency Acquisition & Semantic Differential Validation

Status: **PASS (generic) / PRODUCT + SANDBOX + DEPENDENCY-MIRROR + VERIFIER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A verifier/runtime mechanics; Track B recovery UX/state; Track C destructive validation; Track D privacy-minimized coverage.  
Dependencies: 137, 171–214, 223–246, especially verifier migration, archive continuity, preservation-service compromise and verifier reproducibility.

## Problem
246 established that retaining a verifier binary or reproducing its bytes does not prove historical semantics. The adjacent problem is operational: future investigators may need dependencies that disappeared, were republished, became vulnerable, or exist only in mutable registries; the historical verifier may itself be exploitable; and two implementations may agree only because they inherited the same parser, fixture or specification error.

Central rule: **historical reconstruction is an evidence-analysis activity, not a revival of old authority. Acquire dependencies by immutable identity where possible, quarantine unresolved provenance, execute legacy code with no current credentials/admission authority and minimal network/filesystem capability, then validate semantics against claim-specific independent vectors and implementations. Reproducible bytes, sandbox containment and semantic agreement are separate claims.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns byte/runtime/parser/canonicalization boundaries and current bootstrap mechanics. Browser execution capability never upgrades historical code into current authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `DEPENDENCY-UNRESOLVED`, `RECONSTRUCTION-QUARANTINED`, `SEMANTICS-DIVERGENT`, `HISTORICAL-ONLY` and `BOOTSTRAP-REQUIRED` states without destructive reset.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive cases; campaign expands **728 → 736 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure reconstruction coverage, unresolved dependency tails and differential outcomes with explicit denominators/privacy minimization; counts cannot prove semantic correctness.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns acquisition provenance, sandbox trust boundary, current-authority isolation, semantic differential interpretation and incident-safe reconstruction.

## SOURCE

### NIST SP 800-218 — Secure Software Development Framework 1.1
NIST SP 800-218 remains the current final SSDF (February 2022). It frames secure development as lifecycle practice intended to reduce vulnerabilities, reduce impact of residual vulnerabilities and address root causes. SP 800-218 Rev.1 / SSDF 1.2 remains an Initial Public Draft published 2025-12-17, so changes remain `CHANGE WATCH` rather than current-final authority.

Sources:
- https://csrc.nist.gov/pubs/sp/800/218/final
- https://csrc.nist.gov/pubs/sp/800/218/r1/ipd

**TRANSFER VALIDATION:** useful lifecycle/supply-chain precedent; it does not define a MintTap historical-verifier sandbox.

### NIST SP 800-190 — Application Container Security Guide
NIST SP 800-190 identifies risks from untrusted/stale images, embedded malware/secrets, unbounded network access, insecure runtime configuration, shared kernels and weak administrative separation. It recommends restricting test-team access to test images/hosts and limiting production access.

Source: https://doi.org/10.6028/NIST.SP.800-190

**TRANSFER VALIDATION:** bounded support for least-privilege/isolation. A container alone is not assumed to be a perfect security boundary, especially for deliberately vulnerable legacy code.

### NIST software-supply-chain guidance — retroactive dependency inventories
NIST notes that retroactively generated SBOMs may not reproduce the same dependency list actually used at build time. This is directly relevant to historical verifier reconstruction: a present-day resolver result is not evidence of the historical dependency graph.

Source: https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance-20

### SLSA Build provenance / isolation
SLSA v1.0 requires authenticated provenance at stronger levels, identifies trusted build-platform boundaries, and at Build L3 requires isolation between builds, ephemeral build environments and resistance to cache poisoning. It explicitly states that resolved-dependency completeness is best effort. SLSA also distinguishes isolation from hermeticity; an isolated build may still communicate with external services.

Source: https://slsa.dev/spec/v1.0/requirements

**TRANSFER VALIDATION:** bounded precedent for provenance, ephemeral isolation and cache-poisoning resistance. SLSA does not prove historical verifier semantics.

### SLSA Dependency Track — current draft / CHANGE WATCH
The draft Dependency Track requires dependency ingestion through controlled sources, version pinning plus integrity hashes, and at stronger levels structural blocking of bypass paths and isolation of ingestion/signing infrastructure.

Source: https://slsa.dev/spec/draft/dependency-track

**CHANGE WATCH:** draft material only. Useful direction, not adopted MintTap policy or final standard.

### Software Engineering Studio — bounded current evidence
Canonical Software Engineering status on 2026-09-23 remains Foundation IN STUDY with no specialist PASS. M006 Safari Service Worker lifecycle evidence is still under restart-boundary regression after prior false-green evidence and lifecycle-invalid oracles. This remains a concrete transfer warning: executable/reproducible harness behavior and a valid semantic oracle are independent claims.

Source: `yhappcom/software-engineering-studio/progress/STATUS.md` (2026-09-23).

## SYNTHESIS 1 — historical dependency acquisition must resolve identity, not repeat a mutable locator
A package name/version/URL is a locator claim. A historical dependency should be tied, where evidence permits, to immutable content identity (digest), source revision, signed provenance/attestation, archived package bytes and the build/run context that consumed it. Re-resolving `package@1.2.3` from today's registry can retrieve altered, replaced or policy-repacked content.

Guard: `same package name/version ≠ same historical bytes`; `registry resolves today ≠ historical dependency recovered`.

## SYNTHESIS 2 — lockfiles are evidence, not universal proof of the historical dependency closure
Lockfiles and integrity fields can materially improve reconstruction, but they may omit system libraries, compiler/runtime state, generated tools, mutable URLs, package-manager behavior or dependencies fetched outside the lock mechanism. NIST's warning on retroactive SBOMs and SLSA's best-effort resolved-dependency completeness prevent a false completeness claim.

Guard: `lockfile present ≠ dependency closure complete`; `SBOM generated later ≠ build-time graph recovered`.

## SYNTHESIS 3 — unresolved historical dependencies create an explicit assurance state
If exact bytes cannot be recovered, do not silently substitute the nearest available patch release, distro package or container base. Record `DEPENDENCY-UNRESOLVED` or `REBUILT-NONIDENTICAL`, identify the affected semantic claims, and use independent evidence where available. A substitute may be useful diagnostically but cannot inherit the original identity.

Guard: `compatible replacement ≠ historical dependency`; `build succeeds with substitute ≠ historical reconstruction succeeds`.

## SYNTHESIS 4 — sandboxing is capability removal, not a container label
Potentially vulnerable historical verifier code should run without production credentials, current signing keys, current admission tokens, browser profile secrets or writable production mounts. Default network should be absent; if a test needs network, expose only a purpose-built fixture endpoint. Input artifacts are treated as hostile; outputs are evidence, not commands for current systems.

Guard: `runs in container ≠ safely sandboxed`; `no known exploit ≠ safe for production credentials`; `historical verifier output ≠ current admission decision`.

## SYNTHESIS 5 — sandbox control plane must remain outside the legacy workload
The legacy verifier must not be able to rewrite its own provenance, approve its output, alter the golden vectors, access sandbox signing material or persist into later runs. Ephemeral execution, read-only inputs, independently captured stdout/stderr/result artifacts and destroyed per-run state reduce cross-run influence. If shared caches are used, cache poisoning becomes an explicit failure mode.

Guard: `sandbox started clean ≠ sandbox output trustworthy`; `ephemeral worker ≠ oracle independent`.

## SYNTHESIS 6 — network denial and hermeticity are different claims
A verifier can have no Internet access yet still consume host files, inherited environment variables, shared caches, clocks or kernel behavior. Conversely, a reconstruction may require a bounded fixture service while still preventing arbitrary egress. Record actual capabilities instead of calling every isolated run “hermetic.”

Guard: `offline execution ≠ hermetic execution`; `hermetic build ≠ semantically correct verifier`.

## SYNTHESIS 7 — semantic validation starts from claim-specific test vectors
Vectors should cover known-valid, known-invalid and boundary/malformed inputs for the exact historical claim: parser acceptance, canonicalization, signature verification, chain transition, generation/currentness interpretation and policy decision where relevant. A verifier that passes only positive fixtures can still accept dangerous malformed or stale objects.

Guard: `known-good vector passes ≠ verifier correct`; `parser accepts ≠ policy authorizes`.

## SYNTHESIS 8 — differential implementations are useful only when their failure domains differ
Agreement between legacy verifier V1 and independently implemented V2 increases confidence only if they do not simply share the same parser library, generated code, fixture generator or copied algorithmic defect. Record implementation lineage and dependency overlap. Disagreement is evidence requiring investigation, not a majority vote.

Guard: `two implementations agree ≠ two independent oracles agree`; `implementation majority ≠ semantic truth`.

## SYNTHESIS 9 — differential validation needs negative controls and metamorphic relationships
When no perfect historical oracle exists, use relationships that should remain invariant or should fail: semantically irrelevant representation changes where the historical format permits them; one-bit signature mutation; predecessor/generation substitution; truncation; duplicate-field or ordering cases according to the historical canonicalization rules. These do not replace authoritative vectors but can expose shared false positives.

Guard: `same answer on corpus ≠ same semantics outside corpus`; `differential agreement ≠ completeness`.

## SYNTHESIS 10 — current policy and historical semantics must not be conflated
A reconstructed verifier may correctly establish “this G12 object would have passed G12 rules.” That does not establish “this object is acceptable for G19 mutation.” Historical interpretation feeds provenance/incident analysis; current bootstrap and current admission policy remain separate.

Guard: `historically accepted ≠ currently authorized`; `historical semantics reproduced ≠ current trust restored`.

## SYNTHESIS 11 — long-offline PWA rejoin never depends on legacy execution in the app shell
For a LogMate-like iPad returning with G12 evidence under G19 authority: preserve unique flight/logbook data and original bytes; establish current bootstrap independently; submit historical evidence to an isolated reconstruction/verification path; classify unresolved dependency or semantic divergence explicitly; check lineage/fork/splice; migrate data/schema; then re-admit each queued operation under current policy. Never ship a vulnerable G12 verifier back into the Service Worker merely to make synchronization proceed.

## SYNTHESIS 12 — reconstruction artifacts need privacy and retention boundaries
Historical reconstruction can require package bytes, source, manifests, build metadata, test vectors and evidence objects. It does not justify copying unrelated user data, full developer home directories, browser histories or production secrets into the archive. Minimize fixtures and redact/derive representative data where the semantic claim permits it.

## SYNTHESIS 13 — reconstruction itself needs provenance
Record who/what requested reconstruction, exact input object digests, dependency acquisition sources/digests, sandbox image/runtime identity, capability policy, verifier source/binary identity, vector-suite version, outputs and disposition. This provenance describes the later analysis; it must not be rewritten as original historical provenance.

Guard: `reconstruction provenance ≠ original execution provenance`.

## SYNTHESIS 14 — semantic PASS is bounded by tested dimensions
A verifier can reproduce parser/signature semantics while policy/currentness semantics remain unresolved, or vice versa. Use dimensions such as `BYTES-REPRODUCED`, `DEPENDENCIES-RESOLVED`, `SANDBOX-BOUNDARY-VALIDATED`, `PARSER-SEMANTICS-VALIDATED`, `CRYPTO-SEMANTICS-VALIDATED`, `POLICY-SEMANTICS-VALIDATED`, `SEMANTICS-DIVERGENT`, `UNRESOLVED`. Do not collapse them into one green badge.

## MINTTAP DECISION
For future MintTap/LogMate historical verifier reconstruction, treat registries and locators as acquisition hints, not historical identity. Prefer retained content-addressed artifacts/provenance and record unresolved dependencies explicitly. Execute legacy tooling in a capability-minimized, ephemeral analysis boundary with no current credentials, signing/admission authority or unrestricted network. Establish semantic confidence with claim-specific positive/negative/boundary vectors plus genuinely independent differential implementations where useful. Historical PASS never authorizes current PWA sync/mutation; current bootstrap and operation-level re-admission remain mandatory.

This is generic direction, not a claim that current MintTap/LogMate implements such infrastructure.

## Track C destructive campaign additions — 729–736
1. **Mutable-registry replay:** same package version resolves to different bytes; system must not call it exact historical reconstruction.
2. **Lockfile completeness laundering:** hidden system/runtime dependency differs while lockfile matches; closure claim must remain bounded.
3. **Nearest-version substitution:** missing dependency is replaced with a compatible patch and build succeeds; result must be `REBUILT-NONIDENTICAL`, not historical PASS.
4. **Container-label theater:** legacy verifier runs in a container with production token/network mount; sandbox gate must fail.
5. **Shared-cache poisoning:** run A contaminates cache consumed by run B; ephemeral/isolation oracle must detect or structurally prevent influence.
6. **Shared-parser differential:** two verifiers agree because both use the same flawed parser; independence claim must fail even when output agrees.
7. **Positive-only corpus:** known-good vectors pass but malformed generation/signature mutation is accepted; semantic gate must fail.
8. **Offline-iPad legacy fallback:** stale device can sync only by re-enabling G12 verifier in current app path; preserve data but reject authority downgrade.

**Campaign state:** **736 defined cases; execution PASS is not claimed.**

## DEPENDENCY / TRANSFER
- **Track A:** exact runtime/parser/canonicalization generations and browser execution boundaries.
- **Track B:** non-destructive user/operator states for unresolved dependency, divergent semantics and bootstrap-required recovery.
- **Track C:** execute sandbox escape/capability, cache-poisoning, dependency substitution and semantic differential cases.
- **Track D:** measure reconstruction/unresolved tails with explicit denominators and privacy limits.
- **Track E:** acquisition provenance, sandbox authority isolation and assurance-state composition.
- **Software Engineering:** implementation of hermetic/reproducible build environments, OS/container/VM sandbox hardening, package mirrors and differential harnesses remains implementation handoff territory.

## OPEN
- Actual MintTap/LogMate verifier source/build/dependency graphs and historical package retention.
- Actual package-manager/registry/mirror choices and immutable artifact availability.
- Actual sandbox technology and escape-resistance validation.
- Actual current credentials/network/host mounts exposed to reconstruction workloads.
- Historical parser/canonicalization/crypto/policy vector suites.
- Independent implementation lineage and semantic differential results.
- Physical iOS/iPadOS/EFB PWA rejoin behavior and MDM constraints.
- Legal/aviation retention requirements for reconstruction evidence.

## CHANGE WATCH
- NIST SP 800-218 Rev.1 / SSDF 1.2 remains draft until finalized.
- SLSA Dependency Track is draft; do not treat its current levels as stable policy.
- Container/VM sandbox behavior, package-registry retention guarantees and platform security boundaries are implementation/provider specific.
- Browser/iOS/iPadOS PWA capability remains platform-specific and requires physical-device evidence.

## Gate result
**PASS (generic).** Track E can distinguish historical dependency identity from mutable resolution, specify a capability-minimized reconstruction boundary, separate sandbox containment from semantic correctness, design bounded semantic differential validation, and apply the result to long-offline PWA rejoin without legacy-authority fallback. Product/runtime validation remains OPEN.

## Next high-value adjacent target
**248 — reconstruction-oracle provenance compromise, test-vector custody & differential-common-mode failure:** determine how golden vectors are generated/custodied/versioned, how compromised fixture generators or copied specifications can poison all differential implementations, and how to recover semantic assurance when the oracle corpus itself becomes disputed.