# 187 — PWA Archive Migration, Algorithm Retirement & Long-Term Evidence Re-attestation Without Authority Laundering

Status: **PASS (generic) / PRODUCT + CRYPTO + ARCHIVE-FORMAT + VERIFIER + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A offline/browser artifact handling; Track B uncertainty/recovery UX; Track C migration/retirement destructive validation; Track D privacy-bounded evidence health.
Dependencies: 183–186 exact-artifact provenance, transparency evidence, historical key succession, archive integrity/verifier isolation/deletion governance.

## Problem
186 established that archives are evidence rather than authority and that historical verifiers must remain isolated from current mutation/admission. The next lifecycle problem is aging: storage formats, canonicalization rules, parsers, signature/hash algorithms, certificates and verifier runtimes can become obsolete before the evidence retention obligation ends. Migration and later assurance material can preserve interpretability and evidence of prior existence, but they can also accidentally launder a weak, unknown or compromised historical claim into apparently fresh trust.

Central rule:

> **Migration and re-attestation may preserve bytes, meaning, provenance and evidence of prior existence; they do not retroactively create trust that the original evidence never had. Preserve the original claim and its validation context, record every transformation as a new provenance event, and keep current authority separate from preservation assurance.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker/Cache Storage/IndexedDB may hold old formats and observations; browser-local migration is not authoritative archive migration.
- **B UX/IA/Content:** consumer. Owns comprehensible states for locally preserved data, historical verification unavailable/renewed, and remote submission paused without presenting re-attestation as original authenticity.
- **C Performance/Accessibility/Quality:** validator. Owns byte/semantic migration, algorithm retirement, downgrade, long-offline and assistive-technology campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Migration/retirement telemetry should be low-cardinality and must not become an identity/flight/evidence dossier.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns preservation lineage, verifier retirement, re-attestation boundaries, restore/convergence and incident governance.

## SOURCE
### RFC 4998 — Evidence Record Syntax
RFC 4998 addresses long-term evidence when hash/public-key algorithms or certificates can become weak/invalid. Its model renews timestamps before critical mechanisms lose assurance and defines evidence records that can be stored separately from archived objects. The transferable principle is that preservation assurance is periodically renewed while preserving evidence of prior existence; renewal does not replace the original object or silently rewrite its history.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

### RFC 4810 — long-term archive service requirements
RFC 4810 explicitly anticipates future validation after original keys or algorithms cease to provide effective protection and requires modifications to archived data/evidence to be detectable. It also warns that a long-term archive should not necessarily supply all trust anchors/policy itself because doing so can make the archive capable of manufacturing apparently valid evidence.

Source: https://www.rfc-editor.org/rfc/rfc4810.html

### RFC 9321 — Signature Validation Token
RFC 9321 defines an informational mechanism in which a trusted authority asserts that a signature was successfully validated under defined procedures at a particular time. This is useful transfer evidence for separating a later validation assertion from the original signature. It is not a mandate for MintTap/LogMate and does not mean a later validator can repair an originally invalid or unknown signature.

Source: https://www.rfc-editor.org/rfc/rfc9321.html

### NIST SP 800-131A Rev.2 and Rev.3 change watch
SP 800-131A Rev.2 remains the current final transition recommendation. Rev.3 is still an Initial Public Draft; NIST's key-management publications page lists it as Draft while Rev.2 remains final. Rev.3 proposes additional retirements and discusses transition toward 128-bit security strength and quantum-resistant algorithms. Algorithm-retirement schedules must therefore be change-watched rather than hard-coded from the draft.

Sources: https://csrc.nist.gov/pubs/sp/800/131/a/r2/final ; https://csrc.nist.gov/pubs/sp/800/131/a/r3/ipd ; https://csrc.nist.gov/Projects/Key-Management/publications

### FIPS 204 — current PQ digital-signature standard
FIPS 204 (ML-DSA) has been final since 2024-08-13. Its existence confirms that post-quantum signature transition is no longer purely hypothetical, but it does **not** establish a MintTap/LogMate requirement to re-sign historical evidence with ML-DSA or define a migration deadline.

Source: https://csrc.nist.gov/pubs/fips/204/final

## SYNTHESIS — four things that must not collapse
Separate at least:
1. **original evidence object** — exact original bytes/object identity where preservation requires them;
2. **original validation context** — algorithms, keys/certificates, canonicalization, policy and verifier version applicable at the historical event;
3. **migration representation** — a later encoding/container/schema produced to remain readable/interoperable;
4. **preservation assurance** — later timestamp, evidence record, validation token, re-attestation or equivalent mechanism that says something about prior evidence at a later time.

Persistent guards:
- `migration readable ≠ migration authentic`;
- `migration semantically equivalent ≠ original signed bytes preserved`;
- `new container valid ≠ original container was valid`;
- `re-attestation valid today ≠ original evidence was trusted then`;
- `later timestamp proves prior existence ≠ later timestamp proves original semantic legitimacy`;
- `signature validated at T2 ≠ signature known valid at T1 unless the validation evidence/policy supports that claim`;
- `new strong algorithm wraps old evidence ≠ old weak signature becomes cryptographically strong retroactively`;
- `algorithm retired for new signing ≠ historical verification forbidden automatically`;
- `historical verification allowed ≠ retired algorithm may return to current signing/admission`;
- `format migration complete online ≠ long-offline fleet migrated`;
- `PWA cache converted ≠ authoritative archive converted`.

## Migration classes
Treat transformations according to what they change:
- **bit-preserving relocation**: same exact bytes, different storage/container location;
- **container migration**: original bytes embedded/wrapped in a newer container;
- **representation migration**: reserialization or schema conversion changes bytes while intending to preserve meaning;
- **semantic migration**: fields/meaning are mapped into a new domain model;
- **assurance augmentation**: timestamp/evidence record/validation assertion is added without pretending to be the original signer.

The farther a migration moves from exact bytes, the more provenance and validation it needs. A semantic migration should preserve the source object or an independently integrity-protected source identity when the original claim may need future verification. If original signatures cover exact bytes/canonicalized representations, reserialization can invalidate direct signature verification even when the user-visible meaning appears unchanged.

## Re-attestation without authority laundering
A preservation service can state a bounded new claim, for example: "At T2, object digest X and historical validation package Y were observed/validated under policy P2." It must not silently restate this as "the original signer freshly signed X at T2" or "X was unquestionably legitimate at T1."

Required distinctions:
- **original signer/authority** vs **later preservation/validation authority**;
- **original event time** vs **later observation/validation time**;
- **original algorithm/policy** vs **later preservation algorithm/policy**;
- **original validity result** vs **later validator's result and confidence**;
- **known compromise/UNKNOWN intervals** vs **clean intervals**.

If the original key is later suspected compromised, a fresh strong timestamp/re-attestation may preserve the fact that a disputed object existed before/after a boundary only to the extent supported by trustworthy time/provenance evidence. It must not erase the compromise-era UNKNOWN established by 185.

## Algorithm retirement and verifier lifecycle
Generic direction:
1. Maintain a versioned registry of algorithms/verifiers/canonicalization contexts used by retained evidence.
2. Distinguish states such as `approved for new protection`, `verify-only historical`, `restricted/sandboxed historical`, and `unsupported/unverifiable` rather than a single enabled boolean.
3. Before retiring a verifier/runtime, inventory retained evidence that still depends on it; `zero recent use ≠ zero retained dependency`.
4. Where justified, add preservation assurance while the old evidence is still verifiable and before an algorithm/runtime crosses the applicable risk threshold.
5. Preserve original evidence and transformation provenance; do not overwrite the only original with the migrated representation.
6. Keep retired algorithms off current signing/admission paths.
7. Treat algorithm/canonicalization/parser migration as separate epochs; changing one does not prove the others migrated.
8. If evidence can no longer be verified, report `UNKNOWN/UNVERIFIABLE` rather than accepting it through a weaker fallback.

**CHANGE WATCH:** NIST SP 800-131A Rev.3 remains draft as of this study; product retirement dates must be rechecked against final/current policy at implementation time.

## Archive migration and PITR
A migrated archive creates at least two histories: the evidence's original history and the archive system's migration history. A restore can regress either. After PITR:
- reconcile against the surviving current migration/retirement/security floor;
- detect restored pre-migration copies and do not automatically re-enable obsolete signing/verifier paths;
- preserve conflict/compromise/deletion records introduced after the restored snapshot;
- do not infer that because an old archive verifies under an old context it is the current authoritative preservation generation.

`PITR restored old verifier ≠ old verifier re-approved`.

## PWA/EFB boundary
Long-offline company iPads can miss several archive/algorithm/verifier generations. Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. obtain current authenticated server security/policy/migration generation;
3. identify local data/evidence format and provenance without executing obsolete authority;
4. use bounded compatibility/migration logic only where current policy permits;
5. retain source identity/source bytes when required for provenance;
6. re-admit queued consequence-bearing operations under current authority after migration/reconciliation;
7. surface local-preserved/remote-pending/verification-uncertain states accessibly.

Do not assume WebKit can run arbitrary historical verifier runtimes, background migrations, or long-duration jobs. Do not make a PWA client the only preservation service. Physical iPadOS/Safari/Home Screen/MDM evidence remains OPEN.

## Privacy and minimization
Long-term preservation can create permanent identity linkage. Re-attestation packages should contain only what the preservation claim requires. Avoid embedding stable device IDs, user/flight/location history, raw analytics or unrelated account metadata merely because the archive is long-lived. A later preservation envelope should not become a universal correlation identifier across otherwise separable records.

## Track C destructive campaign
Define a **256-case generic campaign** spanning:
- exact-byte relocation and digest mismatch;
- reserialization that preserves display but breaks original signature;
- canonicalization drift;
- schema migration loses unknown extension fields;
- semantic mapping changes units/time-zone/identifier meaning;
- migrated container omits original object;
- preservation envelope points to wrong digest;
- re-attestation claims original signer identity incorrectly;
- timestamp/re-attestation issued after known compromise but presented as pre-compromise proof;
- later strong signature launders weak/UNKNOWN historical validity;
- retired algorithm accidentally enabled for new signing;
- trial-and-error verifier downgrade;
- verifier inventory misses cold archive dependency;
- verifier package contains private signing material;
- old parser exploit crosses read-only boundary;
- algorithm registry rollback through PITR;
- pre-migration archive restored and declared current;
- post-restore conflict/deletion evidence disappears;
- long-offline iPad reconnects with N-3 schema/verifier;
- stale SW selects retired migration path;
- IndexedDB source overwritten before migration validation;
- client migration succeeds locally but remote admission semantics changed;
- queue drains before current policy/migration reconciliation;
- background migration assumption fails on iPadOS;
- migration telemetry leaks stable device/user/flight identity;
- screen reader cannot distinguish preserved-local from verified-remote state;
- human operator mistakes re-attested evidence for newly authorized evidence;
- preservation service compromise attempts to become current trust anchor.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Preserve original evidence identity/bytes when future verification depends on them; never overwrite the only original merely to modernize representation.
2. Treat every migration/re-serialization/semantic conversion as a provenance event with explicit source→target relationship.
3. Separate original authority/signature from later preservation authority and later validation assertions.
4. Re-attestation may renew preservation assurance; it must not erase original INVALID/UNKNOWN/compromise state or manufacture original trust.
5. Maintain explicit algorithm/verifier states; retirement from new use does not automatically destroy historical verification, and historical verification never re-enables current signing/admission.
6. Plan algorithm/runtime retirement before dependencies become unverifiable; inventory cold/offline evidence, not just recent runtime use.
7. Keep NIST SP 800-131A Rev.2 as current final transition baseline and Rev.3 as CHANGE WATCH until finalized.
8. Treat FIPS 204/PQC availability as transition evidence, not a product mandate absent actual risk/compliance architecture.
9. Reconcile PITR/restores against surviving current migration/security/deletion/hold floors before declaring archive recovery complete.
10. Preserve unique local PWA/EFB operational data across reconnect/migration; current server authority governs remote consequence after reconciliation.
11. Keep exact product retention, format, algorithms, timestamp/preservation service, verifier runtime, legal/aviation requirements and physical-iPad behavior OPEN until canonical evidence exists.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate needs long-term cryptographic preservation/re-attestation at all: **OPEN**.
- Actual archive formats, canonicalization, schemas and signature/hash algorithms: **Software Engineering/Security dependency**.
- Actual historical-verifier runtime and isolation mechanism: **Software Engineering/Security dependency**.
- Timestamp/evidence-record/SVT/trust-service architecture: **OPEN; no generic mechanism mandated**.
- Retention/legal/aviation evidentiary duration and admissibility requirements: **Privacy/legal/aviation dependency**.
- PQC migration requirement/timeline: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM long-offline migration behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 256-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- NIST SP 800-131A Rev.3 is still draft; re-check status and final transition schedules before implementation.
- NIST SP 800-57 Rev.6 is draft and may change lifecycle guidance.
- PQC standards/transition guidance and implementation maturity are rapidly evolving.
- Long-term evidence standards and trust-service profiles are jurisdiction/use-case dependent.
- Browser/iPadOS storage/background/runtime behavior remains change-sensitive.

## Adjacent next bottleneck
**PWA preservation-service trust, timestamp authority compromise & re-attestation-chain recovery**: determine how later preservation authorities are scoped and replaced without allowing a compromised timestamp/preservation service to rewrite historical chronology, how multi-provider/independent evidence affects survivability without becoming automatic majority authority, and how long-offline clients consume renewed preservation evidence without carrying obsolete trust roots into current admission.