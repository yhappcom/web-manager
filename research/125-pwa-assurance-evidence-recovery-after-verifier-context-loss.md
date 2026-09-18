# 125 — PWA Assurance Evidence Recovery After Verifier/Context Loss

Status: **PASS (generic) / PRODUCT RECOVERY + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 122–124 assurance independence/freshness/retention chain; Track C recovery-verifier regression; Track A PWA generation identity; Software Engineering for actual backup/parser/verifier implementation.

## Purpose

124 established that historical assurance may outlive active signing authority only when enough verification context survives. 125 addresses the next failure: retained evidence bytes still exist, but some verification key, trust anchor, certificate/status material, schema interpreter, protected-sink index, epoch-transition record or verifier implementation has been lost or corrupted.

The central rule is conservative reconstruction: recover only claims supported by surviving independent evidence. A new verifier, new key, migrated schema or operator assertion cannot manufacture missing historical trust.

## 1. Five-track balance

- **A Platform/Browser:** supplies historical Service Worker/client/release/trust-generation semantics. It cannot infer a missing generation transition from the current worker alone.
- **B UX/IA/Content:** consumes `VERIFIED / PARTIALLY RECONSTRUCTED / UNVERIFIABLE / UNKNOWN / INVALID`; unavailable proof must not be rendered as a historical PASS.
- **C Quality:** high dependency pressure; owns destructive recovery drills, parser/verifier compatibility fixtures and negative tests proving missing context fails closed.
- **D Search/Analytics:** owns denominator/window semantics; evidence/context loss must not silently remove historical failures from aggregates.
- **E Architecture/Security/Operations:** highest-risk owner; owns recovery sources, trust bootstrap, reconstruction confidence and residual uncertainty.

## 2. SOURCE — key recovery is recovery from backups/archives, not invention

NIST SP 800-57 Part 1 Rev.5 treats key management as a lifecycle including backup, archive, compromise and key recovery. NIST defines key recovery as mechanisms/processes allowing authorized entities to retrieve or reconstruct keys and other key information from key backups or archives.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/key_recovery

**SYNTHESIS:** legitimate recovery starts from an independently preserved recovery source. Generating a replacement key with the same label is replacement, not recovery of the historical verification identity.

Guards:
- `replacement key ≠ recovered historical key`;
- `same key ID label ≠ same cryptographic key`;
- `new trust anchor installed ≠ old trust path reconstructed`.

**CHANGE WATCH:** NIST SP 800-57 Part 1 Rev.6 is an Initial Public Draft dated 2025-12-05; Rev.5 remains the final baseline used here.

## 3. SOURCE — trust anchors are assumptions that require authentic integrity

NIST defines a trust anchor as an authoritative entity/public key whose trust is assumed rather than derived; the validation process depends on the authenticity and integrity of the trust anchor.

Source:
- https://csrc.nist.gov/glossary/term/trust_anchor

**SYNTHESIS:** if the historical trust anchor is lost, downloading a similarly named certificate from an uncontrolled location does not restore the original trust decision. Recovery needs an authenticated independent copy or another evidence path that was already bound to the historical context.

Guards:
- `certificate found later ≠ historical trust anchor authenticated`;
- `public key mathematically verifies signature ≠ historical trust policy reconstructed`.

## 4. SOURCE — verification data is part of the evidence system

RFC 4998 requires preservation of data needed to verify archive timestamps, including certificates and revocation/status information where applicable, and allows evidence records to contain validation information such as trust anchors, certificates, revocation information and policy details.

Source:
- https://www.rfc-editor.org/rfc/rfc4998.html

**TRANSFER VALIDATION:** ordinary MintTap/LogMate assurance does not require ERS. The transferable lesson is that verification context is not disposable metadata when the historical claim depends on it.

Guard: `evidence object retained ≠ verification context retained`.

## 5. SOURCE — recovery should return to a known state; audit evidence benefits from separate failure domains

NIST SP 800-53 recovery guidance requires recovery/reconstitution to a known state after disruption/compromise/failure. AU-9's separate-system audit-backup pattern exists so compromise of the audited component does not also destroy its audit records.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST RMF assessment material for CP-10/AU-9.

**SYNTHESIS:** recovery evidence should not depend exclusively on the failed verifier/control plane. Independent protected copies can improve reconstructability, but separate storage alone does not prove semantics or authenticity.

Guards:
- `backup exists ≠ recoverable verifier context`;
- `separate copy exists ≠ independent trustworthy copy`;
- `system restored ≠ historical assurance restored`.

## 6. Claim-recovery lattice

Do not force binary PASS/FAIL after context loss. Use at least:

1. **VERIFIED** — original claim can be verified under sufficiently reconstructed historical context.
2. **PARTIALLY RECONSTRUCTED** — bounded subclaims survive, but one or more dimensions such as policy, ordering or population continuity remain unknown.
3. **UNVERIFIABLE** — evidence bytes may exist but required authenticity/semantic context is unavailable.
4. **UNKNOWN/GAP** — expected evidence/context is missing or the observation interval cannot be reconstructed.
5. **INVALID** — surviving evidence positively fails the applicable verification rule.

`UNVERIFIABLE` is not `INVALID`; neither is a PASS.

Guards:
- `cannot verify ≠ proven false`;
- `cannot disprove ≠ verified true`;
- `partial reconstruction ≠ full historical PASS`.

## 7. Recovery-source hierarchy

Potential recovery sources, strongest only when independently authenticated and applicable:
- protected backup/archive of verification keys/certificates/trust anchors;
- independently protected sink containing original bytes, receipt/order and immutable identifiers;
- signed/timestamped epoch-transition manifests created before loss;
- reproducible schema/canonicalization specification plus retained golden fixtures;
- independently archived deployment/configuration/release manifests;
- secondary logs/witnesses that can support bounded facts;
- operator notes only as contextual evidence, never cryptographic replacement.

No single hierarchy position guarantees trust; provenance and common-mode failure matter.

## 8. Loss-class analysis

### Verification public key/certificate lost
If an authenticated backup or immutable reference resolves the exact historical key, verification can resume. If only a newly generated key or unauthenticated copy exists, the old signature claim is `UNVERIFIABLE`.

### Trust anchor/policy context lost
A leaf signature may still verify mathematically while the historical authorization/path policy cannot be established. Preserve the narrower cryptographic fact but downgrade the authorization claim.

### Schema/canonicalization interpreter lost
Raw bytes plus a normative historical schema/specification and fixtures may permit a clean-room verifier. If field meaning or canonicalization cannot be reconstructed without guessing, do not reinterpret the record under today's schema.

### Protected-sink index/order lost
Individual signatures may remain authentic while continuity, completeness and ordering become unknown. Rebuilding an index from surviving records does not prove that missing records never existed.

### Epoch-transition record lost
Evidence before and after the gap may each verify, but predecessor/successor continuity is not established. A current operator mapping cannot retroactively create the missing transition.

### Verifier implementation lost
A replacement verifier can be implemented from preserved specifications/fixtures and cross-checked against retained known-good/known-bad vectors. Reimplementing code is not re-signing evidence.

## 9. Re-signing and migration boundary

After context loss, a new authority may sign a recovery package stating what it observed. That signature authenticates the **new recovery statement**, not the lost historical producer claim.

Useful recovery package fields:
- source artifacts/digests;
- missing context explicitly enumerated;
- recovered context and provenance;
- reconstruction method/tool/version;
- verified subclaims;
- unresolved/unsupported subclaims;
- recovery authority/time;
- links to independent witnesses;
- explicit non-promotion to current authorization.

Guards:
- `re-signed old bytes ≠ old signature trust restored`;
- `new recovery statement authentic ≠ historical producer claim authentic`;
- `format converted successfully ≠ missing semantics reconstructed`.

## 10. Recovery must not reactivate obsolete authority

Historical verification material can be restored into an isolated verifier without re-enabling retired signing keys, obsolete API generations, stale sessions or old Service Worker authority.

**MINTTAP DIRECTION:** separate recovery-verifier trust stores from active production authorization stores wherever the architecture warrants historical verification. Exact architecture is OPEN.

Guards:
- `historical key recovered for verification ≠ key reactivated for signing`;
- `historical trust path reconstructed ≠ old client authorized now`.

## 11. PWA / Service Worker application

Suppose historical records say iPad D used worker W12, API A7 and trust epoch T4, but the W12 verification key and W12→W13 transition manifest are lost.

Possible bounded outcomes:
- independent sink + authenticated key backup can restore W12 evidence verification;
- current W13 state does not prove D ever installed W12 or completed W12→W13 transition;
- a fresh W13 login cannot repair uncertainty about compromise-era W12 outbox provenance;
- local domain records may remain useful while provenance is `PARTIALLY RECONSTRUCTED` or `UNVERIFIABLE`;
- remote mutation re-entry still uses current W13/A8/T5-style gates, never recovered historical PASS alone.

Guards:
- `current worker known ≠ historical worker chain known`;
- `fresh login succeeds ≠ historical outbox provenance repaired`.

## 12. EFB / LogMate-like judgment

For long-offline company iPads, verifier-context loss can outlive several client generations. Product design should avoid making irreplaceable flight-record readability depend on a single online historical verifier, while also avoiding local self-attestation as authority.

Generic direction:
- preserve domain records separately from assurance metadata;
- retain enough provenance identifiers to avoid semantic laundering during restore;
- fail historical trust claims to explicit uncertainty when context is unavailable;
- permit local read/export/recovery where policy allows without granting remote mutation;
- validate current re-entry independently of historical verification recovery.

Exact aviation record/legal requirements, MDM/WebKit behavior and product data model remain OPEN.

## 13. Track C destructive recovery campaign

Future bounded implementation evidence should test at least:
1. delete active verifier while retaining authenticated verification-key backup;
2. restore exact historical public key and verify known fixture;
3. substitute same-label/different key and require failure;
4. remove trust anchor but retain leaf certificate/signature;
5. recover authenticated trust anchor from independent archive;
6. remove historical policy constraints and downgrade authorization claim;
7. delete parser executable but retain schema + golden vectors;
8. clean-room parser reproduces known-good/known-bad results;
9. remove canonicalization rule and require `UNVERIFIABLE` rather than guessing;
10. lose sink index while retaining signed records;
11. reconstruct discoverable records but mark completeness unknown;
12. lose one epoch transition while both adjacent epochs verify;
13. reject fabricated predecessor mapping;
14. corrupt verification-context backup and detect integrity failure;
15. primary and secondary copies disagree;
16. recovery authority signs reconstruction package without re-signing historical claim;
17. recovered verification key cannot sign production evidence;
18. current API rejects obsolete client despite historical verification recovery;
19. long-offline PWA returns across unreconstructed epoch gap;
20. local read/export remains available while remote mutation is denied;
21. compromise-era outbox remains quarantined;
22. evidence aggregation excludes `UNKNOWN` from PASS denominator rather than treating it as success;
23. UI labels historical `UNVERIFIABLE` distinctly from `INVALID`;
24. recovery drill works without original producer service;
25. recovery drill documents unrecoverable subclaims instead of filling them from operator memory.

## 14. Cross-repository transfer

### Design Studio
Latest canonical Web status checked 2026-09-18 is W077, Stage 3 PRACTICE / NOT PASSED. W077 captures before/after semantic identity, focus, scroll, geometry, accessibility state and status payload around reorder mutation. Transfer: richer scenario provenance increases future interpretability, but does not prove security evidence recovery. Cross-browser/Safari/Firefox, non-drag reorder, persistence, screen-reader, physical-device, field-CWV and human UX remain OPEN.

### Software Engineering
Latest global status remains Foundation IN STUDY. D005 now provides bounded real application-process crash/restart SQLite evidence while explicitly refusing to promote it to OS/power-loss/mobile durability. Transfer: recovery claims must preserve the failure boundary. Actual verifier backups, clean-room parser tests, key isolation and corruption injection belong to Software Engineering when a concrete implementation exists; none is promoted to PWA runtime proof.

### Marketing
No material canonical evidence changes this boundary.

## 15. Operational recovery record

For each context-loss incident record:
- historical claim/evidence class;
- lost/corrupted context component;
- expected source of truth and retention policy;
- surviving independent copies and provenance;
- common-mode failure analysis;
- reconstruction method/tool/version;
- claims VERIFIED vs PARTIALLY RECONSTRUCTED vs UNVERIFIABLE vs UNKNOWN vs INVALID;
- whether completeness/ordering/continuity remain unknown;
- current authorization impact;
- remediation to prevent recurrence;
- next destructive recovery drill.

## 16. PASS gate

Generic PASS requires ability to:
- distinguish recovery from replacement and re-signing;
- separate mathematical signature verification from historical trust/policy reconstruction;
- degrade claims conservatively when key/trust/schema/index/epoch context is missing;
- recover bounded facts from independent authenticated sources without inventing continuity;
- rebuild verifier tooling from preserved specifications/fixtures without laundering semantics;
- keep historical verification recovery isolated from current production authorization;
- apply the model to long-offline PWA/EFB records and outbox provenance;
- specify destructive recovery tests and explicit uncertainty states.

**Gate result: PASS (generic).** Product/runtime/managed-iPad/key/trust/schema/sink recovery evidence remains OPEN.

## 17. Adjacent question completed before stop

The immediate adjacent question is whether reconstructability itself should be periodically proven. Answer: yes, for assurance classes whose historical verification matters. A retention drill that only checks file existence is insufficient; a destructive or isolated restore should prove that a future verifier can reconstruct the intended bounded claim from retained context without original producer authority. This is folded into Track C rather than creating a separate micro-study.

## Next high-value target

**Assurance recovery authority & provenance after disaster/organizational loss**: when the people, accounts, cloud tenant, repository or provider that authenticated recovery context are themselves unavailable or compromised, determine how bootstrap authority is re-established without circularly trusting the replacement environment. Coordinate with prior organizational-survivability/break-glass work and avoid prescribing enterprise PKI/escrow unless consequence justifies it.