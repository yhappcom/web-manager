# 245 — PWA Convergence-Proof Verifier Compromise, Archive Migration & Historical-Evidence Continuity

Status: **PASS (generic) / PRODUCT + ARCHIVE + VERIFIER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A verifier/currentness mechanics; Track B recovery UX; Track C destructive validation; Track D privacy-minimized evidence continuity.  
Dependencies: 137, 171–214, 223–244, especially verifier migration, crypto compromise recovery, proof retention, witness compromise and stale-checkpoint non-authority.

## Problem
244 made convergence proofs finite historical assurance packages. The adjacent failure is verifier decay: a proof may outlive the key, certificate chain, canonicalization algorithm, parser, schema, hash/signature algorithm or software used to assess it. Migration can preserve assessability, but careless re-signing can falsely make an old witness statement appear newly authored, erase the original bytes, or turn a successor archive attestation into retroactive trust.

Central rule: **preserve the original evidence object and its historical verification context; append successor preservation evidence that attests to continuity, not a replacement statement pretending to be the original. A new signature can authenticate a new archival assertion about old evidence, but cannot recreate the old signer’s act, repair an already-compromised historical signature, or make stale evidence current authority.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns client-visible verifier generation, bootstrap/currentness and byte-preserving local evidence mechanics. Browser/PWA support for an old verifier is not authority to use it for new current operations.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `HISTORICAL-ONLY`, `VERIFIER-UNAVAILABLE`, `REVALIDATION-REQUIRED` and `BOOTSTRAP-REQUIRED` states while preserving unique data; reusable interaction doctrine remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight destructive cases; campaign expands **712 → 720 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure migration coverage and verifier-generation tails with privacy minimization; telemetry cannot establish historical authenticity or current authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns archive/verifier migration, compromise-window reasoning, continuity attestations, retirement and long-horizon validation.

## SOURCE

### RFC 4998 — Evidence Record Syntax and renewal
RFC 4998 defines evidence records for long-term proof of data existence/integrity. It explicitly addresses weakening hash/public-key algorithms and invalid certificates, requires preservation of verification material, and defines timestamp/hash-tree renewal so newer archive timestamps cover prior evidence before the prior mechanism becomes unsuitable.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

**TRANSFER VALIDATION:** strong bounded precedent for append-only preservation evidence and proactive cryptographic renewal. ERS is not adopted as the MintTap/LogMate archive protocol, and its non-repudiation goals are broader/different from our convergence-proof claims.

### NIST FIPS 186-5 — signatures authenticate signatory and detect modification
FIPS 186-5 defines digital-signature algorithms and the security properties of detecting unauthorized modification and authenticating the signatory.

Source: https://csrc.nist.gov/pubs/fips/186-5/final

**TRANSFER VALIDATION:** supports keeping signer identity and signed bytes distinct from later archival assertions. It does not define long-term evidence migration policy.

### NIST SP 800-102 — digital-signature timeliness remains relevant CHANGE WATCH
NIST’s cryptographic publication review notes SP 800-102 addresses timestamps for establishing when a digital signature was generated. NIST requested public review in November 2024; current reliance should therefore be freshness-checked rather than treated as timeless.

Source: https://www.nist.gov/news-events/news/2024/11/nist-requests-public-comments-sp-800-102-recommendation-digital-signature

**CHANGE WATCH:** use only as bounded timeliness precedent; do not infer a MintTap timestamping architecture.

## SYNTHESIS 1 — original statement and preservation statement are different objects
If witness W signed object O at T1, an archive service signing O again at T5 does not mean W signed O at T5. Preserve at least: original bytes/encoding, original signature and signer/verifier generation, historical validation inputs, successor preservation attestation, migration event/provenance, and the relation between them.

Persistent guards: `archive re-signed ≠ original statement re-signed`; `new archival signature valid ≠ old signer acted again`; `successor attestation ≠ retroactive authorship`.

## SYNTHESIS 2 — migration must preserve identity of the thing being evidenced
A format migration may produce semantically equivalent content while changing committed bytes. If the original signature bound exact bytes, replacing them with normalized/re-serialized bytes destroys the original verification target. Preserve the original signed representation or an evidence chain that unambiguously binds the migration to it.

`same semantic record ≠ same signed bytes`; `parseable successor format ≠ original signature preserved`.

## SYNTHESIS 3 — proactive renewal differs from post-compromise rescue
If a verifier/signing/timestamp mechanism is approaching retirement but is still trustworthy, successor preservation evidence can be created while the old proof is still assessable. If the old private key or verifier trust basis may already have been compromised, simply re-signing the old object does not establish that it existed before compromise.

Classify migration as `PLANNED-RENEWAL`, `POST-COMPROMISE-REVALIDATION`, or `UNVERIFIABLE`, with explicit compromise/uncertainty windows.

`renewed before weakness ≠ re-signed after unknown compromise`; `new strong signature ≠ old evidence repaired`.

## SYNTHESIS 4 — verifier retirement is asymmetric
Historical verification support may need to outlive current signing/admission support. An isolated legacy verifier can remain available for bounded historical assessment while the current request path rejects legacy algorithms for new authority-bearing objects.

`historical verification needed ≠ legacy signing allowed`; `legacy verifier retained ≠ legacy verifier belongs in primary request path`.

## SYNTHESIS 5 — preserve verification context, not only algorithms
Long-horizon verification can depend on schema version, canonicalization rules, certificate/revocation material, trust-root generation, policy effective at the claimed time, parser semantics and verifier implementation assumptions. An algorithm identifier alone is insufficient.

A generic preservation package should record the minimum context needed to reproduce the historical assessment and the successor migration chain without retaining unrelated user telemetry.

`algorithm known ≠ historical verification reproducible`; `hash matches ≠ canonicalization semantics known`.

## SYNTHESIS 6 — migration provenance must itself be versioned and non-destructive
Do not overwrite `proof-v1` with `proof-v2`. Append a migration record binding source object identifier/hash, exact source representation, migration reason, source/target schema and verifier generations, transformation (if any), preservation attestation, operator/service provenance, validation result and unresolved limitations.

A later verifier compromise can then reopen only migrations/proofs that materially depended on it.

## SYNTHESIS 7 — archival attestations are evidence, never governance roots
A preservation service can attest that it observed/bound an object at a time under a defined mechanism. That does not grant it authority to select the canonical recovery branch, approve sync, or override current server admission floors.

`archive says object existed ≠ object currently authorized`; `archive continuity PASS ≠ governance currentness PASS`.

## SYNTHESIS 8 — verifier compromise has claim and time boundaries
If verifier V3 is compromised, determine which proof generations, observation intervals, migrations and closure claims depended materially on V3. Do not invalidate unrelated V2 evidence or automatically trust V4 re-signing. Where pre-compromise timing cannot be established, classify the affected evidence as potentially affected/unverifiable and seek independent successor evidence.

`verifier compromised now ≠ every historical proof false`; `signature verifies now ≠ signature predates compromise`.

## SYNTHESIS 9 — archive migration needs negative tests
A migration PASS needs more than successful parsing. Test that altered original bytes fail where byte identity matters; unsupported/retired verifier generations cannot create new current authority; missing migration links are detected; downgrade to a weaker verifier is rejected; and an archival attestation cannot authorize consequence-bearing operations.

## SYNTHESIS 10 — long-offline PWA evidence crosses verifier generations through lineage, not fallback
A LogMate-like iPad may return carrying G12 proof objects while current verifier generation is G19. Preserve the local original evidence and unique flight/logbook data. Obtain current supported bootstrap/currentness, verify any supported historical chain in a bounded verifier path, compare lineage for rollback/fork contradictions, migrate data/schema as required, and re-admit queued operations under current authority.

If G12 cannot be safely verified, remain `VERIFIER-UNAVAILABLE`/`BOOTSTRAP-REQUIRED`; do not reset the device merely to remove the incompatibility, and do not enable G12 as a current-authority fallback.

## SYNTHESIS 11 — migration coverage is not proof validity
Track D may report the proportion of retained packages migrated to V4, but `100% migrated` means only coverage under the migration definition. It does not prove every original witness statement was historically valid, every migration preserved semantics, or every offline artifact has returned.

## SYNTHESIS 12 — privacy minimization survives verifier migration
Migration is not permission to unpack and retain more user content than the proof claim requires. Where evidence can be renewed over hashes/commitments and minimal provenance, avoid copying unrelated payloads into a new archive. Product/aviation records may have separate retention obligations; keep those grounds distinct.

## MINTTAP DECISION
For future MintTap/LogMate evidence preservation, use append-only/versioned historical-evidence continuity: retain original signed/committed representations and their historical verifier context; add successor archival attestations/migration records without rewriting authorship; distinguish proactive renewal from post-compromise revalidation; isolate legacy historical verification from current authority paths; and require current bootstrap/re-admission for returning PWA clients regardless of historical proof validity.

This is generic direction, not a claim that current MintTap/LogMate implements such an archive.

## DEPENDENCY / TRANSFER
- **Track A:** expose verifier/currentness generations and byte-preserving evidence behavior; never promote verifier fallback into current authority.
- **Track B:** communicate historical-only/unverifiable/bootstrap-required states without destructive-reset coercion.
- **Track C:** execute migration, downgrade, byte-substitution and archival-authority destructive tests.
- **Track D:** measure migration coverage/missing tails with explicit denominator and privacy minimization.
- **Track E:** own compromise windows, archival attestation semantics, verifier retirement and migration governance.
- **Software Engineering:** exact archive schema, canonicalization, parser isolation, verifier implementation and physical-device migration tests remain implementation handoff territory.

## TRACK C DESTRUCTIVE CAMPAIGN ADDITIONS — 712 → 720 DEFINED CASES
1. **Re-signing authorship laundering:** successor archive signature is displayed as if the original witness signed again — FAIL.
2. **Re-serialization substitution:** original signed bytes are discarded after semantic conversion and historical verification is still claimed — FAIL.
3. **Post-compromise rescue laundering:** old key may already be compromised; strong new signature alone marks old proof trusted — FAIL.
4. **Legacy-verifier authority fallback:** historical verifier is re-enabled in current admission path so stale objects can authorize mutation — FAIL.
5. **Context-loss migration:** algorithms remain known but schema/canonicalization/trust context is lost while durable verification is claimed — FAIL.
6. **Broken-chain migration:** proof-v2 exists without authenticated binding to exact proof-v1/migration provenance — FAIL.
7. **Archive-authority promotion:** valid preservation attestation is accepted as governance/current sync authority — FAIL.
8. **Offline-iPad verifier downgrade:** returning iPad forces current service to accept G12 authority because G19 cannot interpret its old package — FAIL.

These are **defined cases only**. Execution PASS is not claimed.

## VALIDATION
Generic gate passes because the model now distinguishes original authorship from archival attestation; proactive renewal from post-compromise rescue; byte identity from semantic equivalence; historical verification from current authority; and verifier migration from destructive reset/downgrade. It also defines cross-track transfer and destructive counterexamples.

Production validation remains OPEN for actual archive/proof schema, signing/timestamp/verifier stack, canonicalization, key/trust generations, provider/archive independence, migration tooling, retention obligations, current bootstrap/admission protocol, physical iPadOS/WebKit behavior and human/AT recovery UX.

## OPEN
- Actual MintTap/LogMate archive/evidence schema and verifier generations.
- Exact cryptographic algorithms, keys, trust roots and canonicalization in production.
- Whether any trusted timestamp/archive service exists or is required.
- Legal/aviation/product retention and evidentiary requirements.
- Exact long-offline currentness/bootstrap and operation re-admission protocol.
- Physical iPadOS/WebKit/MDM migration and storage behavior.
- Archive migration/restore drills and parser/verifier isolation.

## CHANGE WATCH
- NIST cryptographic guidance, especially SP 800-102 review status and SP 800-57 evolution.
- Algorithm/key-size suitability and post-quantum transition guidance.
- Browser/OS/MDM storage and PWA lifecycle behavior.
- Applicable legal/aviation evidence and retention requirements.

## NEXT
Highest-value adjacent work: **246 — preservation-service compromise, migration-chain fork/splice resistance & verifier-supply-chain reproducibility**. Determine how to detect a compromised archive/migration service that issues conflicting successor attestations, how to prevent valid migration segments from being spliced into a false continuity chain, and how to preserve enough reproducible verifier/toolchain evidence without freezing vulnerable executables into the primary trust path.