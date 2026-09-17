# 108 — PWA Recovery-Bridge Provenance, Dependency/Supply-Chain Closure & Recoverability-Preserving Replacement

Status: **PASS (generic) / PRODUCT BUILD + DEPENDENCY + HISTORICAL-CORPUS VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 092 release supply-chain; 099 trust-policy authenticity; 101–107 recovery/provenance/release/retirement/bridge chain; Track A browser/runtime mechanics; Track C validation/regression evidence; Software Engineering implementation evidence; Design Studio W059 runtime closure boundary.

## Purpose

107 minimized legacy recovery authority, but the remaining narrow parser/converter is now security-critical recovery infrastructure. This study defines the evidence required to trust that bridge, its dependencies and its replacement process without silently stranding historical user data.

This is not a package-manager tutorial, SBOM implementation guide or product-specific cryptographic design. Exact MintTap/LogMate parser libraries, CI builders, dependency graph, signing service and historical backup corpus remain unknown.

## 1. Track balance

- **A Platform/Browser:** supplies runtime and artifact-loading boundaries. Browser execution does not prove build provenance or dependency identity.
- **B UX/IA/Content:** consumes truthful states when recovery is temporarily disabled, converter replacement is required, or artifact generation is recognized but not currently safe to process.
- **C Quality:** owns historical-corpus semantic oracles, old→new converter equivalence, malformed/adversarial mutants and exact-artifact regression evidence.
- **D Discovery/Analytics:** vulnerability/bridge telemetry can prioritize work but cannot prove absence of dormant old artifacts or safe retirement.
- **E Architecture/Security/Operations:** highest-risk owner; owns provenance admission, dependency inventory/vulnerability state, release identity, replacement governance and recovery continuity.

Allocation remains E-heavy. A narrow bridge concentrates rather than removes trust: fewer components remain, but failure or compromise of those components can affect irreplaceable recovery data.

## 2. SOURCE — provenance says how an artifact was produced, not whether it is safe

SLSA 1.2 defines provenance as verifiable information tracing an artifact through the build process to its source and records builder identity, build definition/parameters and known resolved dependencies. Its build requirements distinguish artifact identity, provenance authenticity, builder trust and provenance completeness. SLSA also explicitly treats the builder as a trust boundary.

Sources:
- https://slsa.dev/spec/v1.2/provenance
- https://slsa.dev/spec/v1.2/build-provenance
- https://slsa.dev/spec/v1.2/build-requirements

**SYNTHESIS:** a recovery converter should be admitted as an exact artifact, not merely as “version 3.2” or a repository commit. Useful evidence binds the shipped artifact digest to an accepted builder, source revision/build definition and dependency resolution evidence.

But provenance is not a vulnerability scanner, semantic proof or benevolence proof. SLSA's dependency work explicitly notes that verified upstream provenance does not prove an upstream dependency is non-malicious; downstream admission policy still decides whether the evidence is acceptable.

Guards:
- `artifact hash known ≠ artifact provenance verified`;
- `provenance verified ≠ builder acceptable`;
- `builder acceptable ≠ dependency set safe`;
- `dependency provenance verified ≠ dependency non-malicious`;
- `converter built from expected source ≠ converter preserves historical semantics`.

## 3. Provenance consumer policy is part of the trust chain

A signed attestation is useful only if the verifier knows which signer-builder combinations are acceptable and checks that the attested subject digest is the artifact actually being used. SLSA's model separates signer and builder identity for this reason.

Generic recovery-bridge admission therefore needs:
1. exact converter/parser artifact digest;
2. authenticated provenance;
3. accepted signer + builder identity/policy;
4. expected source revision/build definition;
5. known build parameters that affect recovery semantics;
6. dependency identity/resolution evidence to the degree available;
7. vulnerability/advisory evaluation;
8. historical semantic regression evidence;
9. current recovery-policy authorization.

Guard: `attestation signature valid ≠ attested artifact authorized for recovery`.

## 4. Dependency inventory is necessary but not sufficient

The 2025 multinational CISA-led SBOM guidance states that SBOM value comes from consumption: component data should be mapped to vulnerability databases, advisories, supply-chain risk and end-of-life/support information, and that this risk changes over time. It also notes VEX as contextual evidence for vulnerability applicability.

Source:
- https://www.cisa.gov/sites/default/files/2025-09/joint-guidance-a-shared-vision-of-software-bill-of-materials-for-cybersecurity_508c.pdf

OpenSSF's current OSPS Baseline (v2026.08.28) requires standardized dependency-management tooling where available; its baseline also treats signed/hash-accounted release assets and dependency-management policy as security controls.

Sources:
- https://baseline.openssf.org/versions/2026-08-28
- https://baseline.openssf.org/

**SYNTHESIS:** a bridge register from 107 should grow a supply-chain facet: direct/transitive dependency identity where tooling can establish it, version/source, lock/resolution state, known advisories/CVEs, applicability decision and replacement status.

Guards:
- `SBOM generated ≠ SBOM consumed`;
- `component listed ≠ vulnerability applicability known`;
- `no CVE currently known ≠ component safe`;
- `VEX says not affected ≠ future versions/advisories irrelevant`;
- `dependency pinned ≠ dependency trustworthy`.

## 5. Vulnerability evidence is time-varying

CISA's Known Exploited Vulnerabilities catalog exists specifically because evidence of active exploitation changes operational priority. A converter that passed release review can later become unsafe because a parser/decompression/transitive dependency acquires a relevant advisory or exploitation evidence.

Source:
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**CHANGE WATCH:** dependency/advisory/KEV state is not frozen at build time. Recovery bridges may be rarely invoked, so ordinary runtime usage does not remove the need for periodic vulnerability reassessment while the recovery contract remains supported.

Guard: `release-time dependency review PASS ≠ bridge safe for its entire recovery lifetime`.

## 6. Exact artifact and exact corpus must meet

107 required a historical regression corpus. 108 adds a stronger closure rule: supply-chain evidence and semantic recovery evidence must refer to the same converter artifact.

A useful evidence tuple is conceptually:

`converter artifact digest × builder/provenance identity × dependency resolution × corpus version/digest × expected semantic oracle × test environment × result`

This prevents a common evidence gap where one binary has provenance, another binary was tested, and a third is shipped.

Guards:
- `source tests passed ≠ shipped artifact tested`;
- `converter version label same ≠ artifact bytes same`;
- `corpus passed once ≠ replacement artifact passed`;
- `test corpus exists ≠ corpus provenance/coverage known`.

## 7. Historical corpus is security/recovery evidence, not production data by default

The corpus should represent every promised historical generation and boundary case needed to establish recoverability. It should include synthetic/minimized fixtures where possible, expected normalized output and malformed/adversarial mutants. Real user backups should not become a casually copied regression corpus merely because they are useful examples.

**MINTTAP DIRECTION:** separate:
- format-specification fixtures;
- synthetic historical-valid fixtures;
- malformed/adversarial mutants;
- sanitized incident reproductions where approved;
- any exceptional real-data fixture under explicit privacy/security governance.

The corpus itself needs version/digest/ownership and expected-output provenance so a changed oracle cannot silently redefine “PASS.”

Guards:
- `old backup available ≠ acceptable test fixture`;
- `fixture parses ≠ fixture represents all promised generations`;
- `oracle changed ≠ prior PASS still comparable`.

## 8. Replacement without recoverability regression

When a parser/converter dependency is vulnerable, abandoned or incompatible, replacement should not be “upgrade package and hope.” Generic replacement sequence:

1. freeze or narrow unsafe bridge exposure if risk requires it;
2. preserve opaque historical artifacts and current live state;
3. inventory affected format generations and dependency paths;
4. build replacement under current accepted provenance/build policy;
5. run the complete historical-valid corpus plus malformed/adversarial corpus;
6. compare normalized semantic output against independent expected oracles, not only old-parser output;
7. run migration/reconciliation tests through current canonical representation;
8. verify no old credential/session/trust authority is revived;
9. test interruption/resource exhaustion and unsupported-generation containment;
10. canary/limited-enable the replacement where architecture permits;
11. retain rollback of converter code only when forward state remains readable/recoverable;
12. retire vulnerable implementation after replacement evidence passes, while retaining opaque artifacts/recovery obligation as required.

**CONTRADICTION resolved:** exact output equality with a vulnerable old parser is not always the oracle because the old parser may contain semantic defects. Use a current domain oracle plus reviewed historical compatibility expectations.

Guards:
- `new parser accepts same bytes ≠ same domain meaning preserved`;
- `old and new parser outputs match ≠ output is correct`;
- `dependency upgraded ≠ historical recoverability preserved`;
- `vulnerable bridge disabled ≠ opaque user artifact should be deleted`.

## 9. Fail closed on authority, preserve data on uncertainty

If provenance, dependency admission or semantic regression evidence fails, the safe generic action is to withhold privileged recovery publication/replay, not erase the candidate artifact.

Useful degraded states include:
- artifact preserved / converter temporarily unavailable;
- recognized generation / current converter not authorized;
- conversion quarantined / semantic review required;
- records converted / reconciliation pending;
- local recovery accepted / remote replay not authorized.

This extends the existing rule: `security uncertainty may remove authority without removing user data`.

## 10. C — validation campaign

Exact-product evidence should include at least:
1. provenance subject digest matches shipped converter;
2. wrong artifact with valid unrelated attestation is rejected;
3. valid signature from unaccepted builder is rejected;
4. changed build parameter affecting parser semantics is detected;
5. dependency resolution differs from approved set and is surfaced;
6. direct/transitive vulnerable dependency is mapped to bridge reachability/applicability;
7. unsupported/abandoned dependency triggers replacement path;
8. every promised historical format generation has a positive fixture;
9. boundary/malformed/adversarial corpus remains bounded;
10. corpus/oracle version and digest are recorded;
11. replacement parser preserves independent domain oracle;
12. replacement does not restore old credentials/trust/session material;
13. already-applied outbox operations are not blindly replayed;
14. interruption during conversion preserves opaque artifact and live state;
15. converter rollback cannot strand forward-migrated current state;
16. vulnerability discovered after release can disable authority without deleting data;
17. diagnostics identify artifact/parser/dependency/corpus identities without logging user record contents/secrets;
18. Safari/WebKit managed-iPad import/recovery behavior remains separately validated;
19. recovery/error/quarantine states remain keyboard/zoom/screen-reader operable;
20. old bridge removal occurs only after replacement + retirement evidence closes.

## 11. Design Studio transfer

Canonical Design Studio `progress/WEB_STATUS.md` checked 2026-09-17: Stage 1 PASS, Stage 2 PASS, Stage 3 PRACTICE/NOT PASSED. W059 is a deterministic runtime-closure runbook, but execution is blocked and no browser/Safari/screen-reader/physical-device PASS is claimed.

**DEPENDENCY:** Web Manager supplies truthful recovery/provenance states; Design Studio owns reusable interaction/render evidence. No runtime PASS transfers from W059.

## 12. Software Engineering transfer

Canonical Software Engineering Studio checked 2026-09-17: every specialist remains Foundation IN STUDY. Existing A003/D003/D005/D006/Q003/Q005/Q006 evidence supplies contract-evolution, recovery, reconciliation and fault/regression methods, but no exact PWA converter/build provenance proof.

**DEPENDENCY:** Software Engineering should own exact parser/converter implementation, dependency graph/build tooling and executable replacement tests. Web Manager owns the web/PWA recovery trust contract and evidence required before enabling that implementation.

## 13. EFB/LogMate bounded application

For a LogMate-like managed-iPad PWA, a historical backup may remain the only copy of irreplaceable records. Therefore a supply-chain incident in the converter must not turn into destructive “unsupported file” handling. Generic preference:

`preserve opaque artifact → remove unsafe converter authority → establish patched/replacement exact-artifact provenance → run historical semantic corpus → quarantine conversion → reconcile → authorize current representation/replay`.

Exact backup formats, CI/build service, dependency set, iPad import path, MDM constraints and production sync architecture remain OPEN.

MintTap production architecture was not inspected; no EFB data-authority model is inferred for it.

## 14. Gate

**PASS (generic)** because this study establishes:
- the difference among artifact identity, provenance authenticity, builder trust, dependency inventory/vulnerability state and semantic recovery correctness;
- a provenance/admission contract for security-critical recovery converters;
- supply-chain extension of the bridge debt register;
- exact-artifact × exact-corpus evidence binding;
- privacy-bounded historical regression-corpus governance;
- a recoverability-preserving vulnerable dependency/parser replacement sequence;
- a 20-case validation campaign and cross-repository handoff boundary.

**OPEN:** exact product converter/parser artifacts, CI builder/signer, dependency/SBOM/VEX state, historical corpus, privacy approval, vulnerability policy, runtime isolation and managed-iPad/browser evidence.

## Next high-value boundary

**Recovery corpus longevity and format-spec escrow:** provenance can establish what converter was built, but a long-lived recovery promise also depends on retaining enough non-secret format semantics, fixtures, keys/authority procedures and toolchain knowledge to reconstruct a safe converter after the original dependency/toolchain disappears. Study how to preserve recovery knowledge without preserving vulnerable executables or secrets, and how to prove a future clean-room/current-toolchain converter still implements the historical contract.