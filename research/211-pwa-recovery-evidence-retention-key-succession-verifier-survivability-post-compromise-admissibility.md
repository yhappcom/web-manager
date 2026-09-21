# 211 — PWA Recovery-Evidence Retention, Key Succession, Verifier Survivability & Post-Compromise Admissibility

Status: **PASS (generic) / PRODUCT + EVIDENCE-SCHEMA + KEY/PKI + VERIFIER + RETENTION/LEGAL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/crypto/runtime mechanics; Track B evidence-state communication; Track C destructive assurance; Track D bounded observation.  
Dependencies: 122–126, 137–210, especially 200–210.

## Problem
210 established that ceremony evidence must survive the authority/control plane it audits without becoming recovery authority. The adjacent problem is long-lived verification: audit-signing keys rotate, become suspected compromised, certificates/revocation data age, providers and verifier software disappear, algorithms are retired, and compromise time may be uncertain.

Central rule: **historical evidence verification is a different capability from current evidence signing and current recovery authorization. Key rotation or provider retirement must not destroy historical verification, but retaining historical verification material must not preserve authority to mint new evidence or recovery decisions.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Exact WebCrypto/browser certificate and verifier support is implementation evidence; browser support must not define constitutional evidence validity.
- **B UX/IA/Content:** high dependency pressure. Investigator/operator surfaces need explicit `verified`, `uncertain-window`, `unverifiable`, `superseded` and `current-authority` distinctions rather than a green/red signature badge.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **448 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Telemetry can reveal verification failures or legacy-use tails but cannot decide evidentiary admissibility.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns retention, verifier/key succession, compromise-window classification, provider independence and authority separation.

## SOURCE

### NIST SP 800-57 Part 1 Rev.5 — signing vs verification cryptoperiod
Current final NIST SP 800-57 Part 1 Rev.5 states that a private signature key can have a shorter cryptoperiod than its corresponding public signature-verification key; the public verification key may remain usable for years as long as signatures need verification. It also describes cryptographic timestamping as a way to support verification of signatures produced during the private key's usage period.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://doi.org/10.6028/NIST.SP.800-57pt1r5

**TRANSFER VALIDATION:** this supports retaining public verification context after current signing authority ends. It does not define MintTap's retention period or prove a historical signature predates compromise.

### RFC 5280 — compromise time and revocation-processing time are distinct
RFC 5280 defines `invalidityDate` as the date on which a private key is known or suspected to have been compromised or a certificate otherwise became invalid; it may precede the CRL revocation date, which is when revocation was processed.

Source:
- https://www.rfc-editor.org/rfc/rfc5280.html

**TRANSFER VALIDATION:** discovery/processing time must not automatically be treated as the compromise boundary. Historical evidence around an uncertain compromise interval requires an explicit uncertainty state.

### RFC 3161 — trusted timestamp as historical-validity evidence, with limits
RFC 3161 defines a timestamp token as proof that a datum existed at a particular time and describes using timestamps to support verification that a signature was made before certificate revocation. It also warns that if the TSA private key itself is compromised, tokens made with that key cannot simply be trusted; audit trails or independent TSA evidence may be needed to discriminate genuine from false backdated tokens.

Source:
- https://www.rfc-editor.org/rfc/rfc3161.html

**TRANSFER VALIDATION:** independent time evidence can narrow a historical-validity question, but a timestamp is another trust dependency with its own key-compromise and retention problem. `timestamped ≠ permanently admissible`.

### CHANGE WATCH — NIST SP 800-57 Rev.6
NIST SP 800-57 Rev.6 remains an **Initial Public Draft** dated 2025-12-05 as of this study. Rev.5 remains the final baseline used here.

Source:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

## SYNTHESIS 1 — split signing authority from historical verification capability
Retiring evidence-signing key K must disable creation of new authoritative evidence under K while retaining enough public/non-secret verification context to validate legitimately historical objects when policy requires.

`signing key retired ≠ verification key deleted`; `historical verification support ≠ current signing support`; `public verification material retained ≠ private signing key should be archived`.

Private signing material should not be retained merely because old evidence needs verification. Exact archival/backup controls are implementation/security dependencies.

## SYNTHESIS 2 — verifier survivability is a package, not a public key
Long-horizon verification can depend on more than a key:
- original evidence bytes or canonical representation;
- algorithm/parameter identifiers;
- public key/certificate/trust-chain material;
- relevant revocation/status evidence and policy context;
- timestamp/checkpoint/lineage evidence where used;
- schema/canonicalization/version semantics;
- verifier implementation/specification and test vectors;
- migration/succession records.

A retained certificate with no parseable original evidence or canonicalization rules may be insufficient. A retained verifier binary with no trustworthy trust context is also insufficient.

`key retained ≠ evidence verifiable`; `bytes retained ≠ semantics recoverable`; `verifier executable ≠ verifier trustworthy`.

## SYNTHESIS 3 — provider migration must preserve evidence portability without making the provider the authority
If a logging/KMS/PKI/provider is replaced, historical evidence should remain independently interpretable enough to avoid a single provider's disappearance silently destroying all verification. Provider-specific receipts may be retained as evidence, but provider availability is not itself the constitutional basis for current recovery authority.

`provider retired ≠ history invalid`; `provider reachable ≠ history admissible`; `export succeeded ≠ independent verification proven`.

## SYNTHESIS 4 — key succession needs lineage, not merely a new key
K→K+1 should preserve which key was authorized for which evidence epoch and purpose. A newer key must not silently re-sign old evidence and thereby manufacture a false historical provenance.

If evidence is migrated/resealed, preserve the distinction between:
- original evidence/signature;
- later migration/attestation wrapper;
- migration time and policy;
- successor verifier context.

`re-signed old bytes ≠ old signature trust restored`; `successor key current ≠ predecessor evidence rewritten`.

## SYNTHESIS 5 — compromise creates evidentiary intervals, not necessarily one global Boolean
Useful generic classification:
- `PRE-COMPROMISE-VERIFIED` — evidence is independently bounded before the credible compromise interval under applicable policy;
- `POST-COMPROMISE-UNTRUSTED` — evidence is at/after a boundary where the signing authority cannot be trusted;
- `WINDOW-UNCERTAIN` — creation time and compromise interval overlap or cannot be independently ordered;
- `HISTORICAL-VERIFIED` — cryptographic/lineage checks pass and current policy accepts the historical context;
- `UNVERIFIABLE` — required verification material/context is absent or obsolete;
- `FORKED/PARTIAL/UNKNOWN` — retain the 210 evidence-integrity states where applicable.

Do not infer that every old artifact is false merely because K was later compromised; equally, do not infer that an old-looking signature predates compromise because its embedded timestamp says so.

`key compromised now ≠ every historical signature forged`; `signature says old date ≠ signature proven pre-compromise`.

## SYNTHESIS 6 — revocation time, invalidity/compromise time and discovery time must remain distinct
Operational systems often know compromise only retrospectively. Preserve at least:
- suspected/known compromise interval;
- discovery time;
- revocation/retirement processing time;
- evidence creation/registration time when independently supported.

Do not backfill false precision. RFC 5280's invalidity-date distinction is a useful precedent, but exact MintTap evidence semantics remain OPEN.

## SYNTHESIS 7 — timestamp evidence is useful only when its own lineage survives
A trusted timestamp can help establish that evidence existed before a key's revocation/compromise boundary. But timestamp authority compromise, stale trust roots, missing status data or unverifiable timestamp algorithms can destroy that inference.

Therefore timestamping may be one independent evidence component, not an eternal truth oracle.

`timestamp verifies ≠ signer uncompromised`; `timestamp authority trusted then ≠ timestamp authority trusted forever`; `two timestamps ≠ independent failure domains`.

## SYNTHESIS 8 — algorithm/verifier retirement requires read-only legacy verification or migration evidence, not silent fallback
When algorithms/canonicalizers/verifier software age out, historical verification may require isolated read-only legacy verification, a preserved specification/test corpus, or an authenticated migration wrapper. Legacy capability must not be exposed as a current signing/recovery path.

A verifier that cannot establish the exact historical semantics should return `UNVERIFIABLE/UNKNOWN`, not normalize the object through a modern serializer and claim equivalent verification.

`legacy verifier available ≠ legacy signer allowed`; `modern parser accepts ≠ historical signature preserved`; `fallback verifies ≠ current policy accepts`.

## SYNTHESIS 9 — evidence retention policy must include verification dependencies
Deleting old public keys, status evidence, canonicalization definitions, checkpoints or migration records before the evidence retention horizon can make nominally retained audit records useless. Conversely, indefinite retention of sensitive payloads is not justified by verification needs.

Retention should separate:
- evidence payload/minimized statement;
- verification context;
- private signing authority;
- public verification material;
- operational analytics.

`audit retained ≠ verification context retained`; `verification context retained ≠ retain every sensitive payload`.

Exact legal/aviation/privacy retention is OPEN.

## SYNTHESIS 10 — current authorization never comes from historical evidence keys
An investigator may need K-old to verify a 2026 ceremony years later. A PWA/client/server must not accept K-old as authority to issue a current session, current recovery package or new evidence.

Key usage/purpose/epoch boundaries should make this separation enforceable.

`historical verifier trusts K-old for old evidence ≠ runtime trusts K-old for new authority`.

## SYNTHESIS 11 — restored and long-offline clients do not need the historical verifier plane to sync safely
A LogMate/EFB-like iPad returning after several evidence-key rotations should preserve unique local records, obtain current authority/security generation, quarantine stale session/Service Worker/management assumptions, and re-admit queued operations under current authority. Historical audit verification can occur server/investigator-side as needed.

Do not ship every retired evidence key as a synchronization credential simply to let the client reconnect.

`client can verify historical receipt ≠ client may mutate remotely`; `old evidence key cached ≠ current authority cached`.

## SYNTHESIS 12 — evidentiary admissibility is policy/context dependent
Cryptographic verification establishes bounded technical properties; legal, regulatory, aviation, employment or incident-response admissibility can require additional chain-of-custody, retention, procedure and jurisdictional evidence. Web Manager must not convert a cryptographic PASS into a legal admissibility claim.

`cryptographically verified ≠ legally admissible`; `audit complete ≠ sufficient for every regulator`.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. separate evidence-signing authority from historical verification capability;
2. retain public/non-secret verification context for the required evidence horizon without retaining retired private signing authority merely for verification;
3. preserve key/verifier/canonicalization/policy lineage across rotation and provider migration;
4. classify evidence around compromise using explicit uncertainty intervals rather than one global valid/invalid bit;
5. treat timestamp/checkpoint evidence as dependencies with their own compromise and retention lifecycle;
6. make legacy verification read-only and purpose-scoped; never use it as a current recovery/session/signing fallback;
7. preserve original evidence separately from later migration/reseal attestations;
8. keep long-offline PWA convergence dependent on current authority, not historical evidence keys;
9. preserve verification dependencies while minimizing sensitive retained payloads;
10. do not claim legal/aviation evidentiary admissibility from generic cryptographic verification.

No product-specific PKI, algorithm, TSA, retention period, KMS/provider, verifier implementation or evidence schema is selected.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
Supply exact browser/WebCrypto/certificate/verifier capability when implementation validation begins. Browser API support is not the definition of evidence validity.

### Track B — DEPENDENCY
Evidence UI should communicate `current authority` separately from `historical verified`, `uncertain window`, `partial`, `forked`, `unverifiable` and `unknown`; consume Design Studio evidence for interaction/accessibility rather than duplicating it.

### Track C — VALIDATION
Destructive campaign grows **440 → 448 defined cases**:
1. evidence-signing K1 rotates normally to K2; K1 private key is unavailable but historical K1 evidence must still verify;
2. K1 is discovered compromised at T3 with credible compromise interval T1–T3; evidence from T2 must remain `WINDOW-UNCERTAIN` rather than silently valid/invalid;
3. attacker backdates new K1-signed evidence to before T1 after compromise;
4. RFC-3161-like timestamp exists but TSA key is later compromised;
5. audit provider is retired; exported evidence lacks one provider-specific verification dependency;
6. canonicalization/verifier v1 is retired and modern parser reserializes bytes differently;
7. PITR restores a server with K1 historical verifier material and mistakenly re-enables K1 as current authority;
8. long-offline iPad reconnects carrying old evidence receipts/keys after K1→K3 while unique local records remain unsynced.

Execution, physical iPad/Safari, real PKI/KMS, verifier migration, retention, legal/aviation and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure verifier failures, legacy-tail volume, provider migration coverage and unknown-state rates if instrumented. Analytics cannot decide whether an artifact is admissible or whether compromise occurred before signing.

## Persistent guards added through 211
- `signing key retired ≠ verification key deleted`;
- `historical verification support ≠ current signing support`;
- `key retained ≠ evidence verifiable`;
- `bytes retained ≠ semantics recoverable`;
- `verifier executable ≠ verifier trustworthy`;
- `provider retired ≠ history invalid`;
- `export succeeded ≠ independent verification proven`;
- `re-signed old bytes ≠ old signature trust restored`;
- `key compromised now ≠ every historical signature forged`;
- `signature says old date ≠ signature proven pre-compromise`;
- `revocation time ≠ compromise time ≠ discovery time`;
- `timestamp verifies ≠ signer uncompromised`;
- `legacy verifier available ≠ legacy signer allowed`;
- `modern parser accepts ≠ historical signature preserved`;
- `audit retained ≠ verification context retained`;
- `historical verifier trusts K-old ≠ runtime trusts K-old for new authority`;
- `cryptographically verified ≠ legally admissible`.

## OPEN
- actual MintTap/LogMate evidence schema, canonicalization and verifier versions;
- audit-signing PKI/KMS/key custody/rotation/revocation implementation;
- trusted timestamp/checkpoint/monitor topology;
- compromise-window investigation procedure;
- provider-export portability and independent verifier tests;
- retention/privacy/legal/aviation requirements;
- physical iPad/Safari/PWA runtime behavior;
- exact legacy-verifier isolation and decommission criteria;
- human/investigator evidence-state comprehension.

## CHANGE WATCH
- NIST SP 800-57 Rev.6 progression beyond Initial Public Draft;
- algorithm/key-management transition guidance;
- PKIX/timestamp/transparency standards relevant to long-term validation;
- browser/WebCrypto/platform verifier behavior where implementation depends on it.

## Gate result
**211 PASS (generic).** The Web Manager can now separate current evidence signing from historical verification, preserve verifier/key/policy lineage across rotation/provider retirement, classify compromise-window uncertainty, and prevent historical evidence capability from becoming current recovery authority.

Production validation remains OPEN.

## Next highest-value adjacent question
**212 — evidence-chain migration under cryptographic deprecation, trust-anchor expiry & long-horizon re-attestation.** Determine how to preserve historical verification when algorithms/trust anchors become unacceptable or unverifiable, how migration/re-attestation can extend evidence life without rewriting original provenance, how to prove the migration happened while the old chain was still trustworthy, and how to retire obsolete verifier code/keys without losing required historical evidence.