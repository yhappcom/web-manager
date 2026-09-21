# 212 — PWA Evidence-Chain Migration under Cryptographic Deprecation, Trust-Anchor Expiry & Long-Horizon Re-attestation

Status: **PASS (generic) / PRODUCT + CRYPTO-POLICY + EVIDENCE-SCHEMA + PKI/TSA + VERIFIER + RETENTION/LEGAL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A crypto/runtime mechanics; Track B evidence-state communication; Track C destructive assurance; Track D bounded migration observation.  
Dependencies: 137, 200–211, especially 211.

## Problem
211 separated current evidence signing from historical verification and preserved uncertainty around compromise. The adjacent failure is cryptographic aging itself: a signature/hash/timestamp/trust anchor that was acceptable when evidence was created can later become deprecated, disallowed for new protection, expire, lose implementation support, or become too weak for the remaining retention horizon.

Central rule: **long-horizon preservation extends evidence about the original object; it must not rewrite original provenance or pretend a new signature was the original event. Migration must occur while enough of the predecessor chain remains trustworthy to authenticate the transition.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. WebCrypto/browser support can determine where a verifier can run, but platform API availability does not define whether historical evidence is admissible.
- **B UX/IA/Content:** high dependency pressure. Surfaces must distinguish original verification, preservation/migration verification, current cryptographic acceptability and uncertainty.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **456 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can measure migration coverage, legacy tails and verifier failures; cannot declare a chain trustworthy.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns cryptographic transition policy, preservation-chain lineage, anchor/verifier retirement and anti-downgrade boundaries.

## SOURCE

### NIST SP 800-131A Rev.2 — algorithm transition and legacy use
NIST SP 800-131A Rev.2 remains the current final publication page baseline for transitions to stronger algorithms/key lengths. NIST distinguishes applying new cryptographic protection from processing already-protected information; historical/legacy verification can remain a distinct use even when an algorithm is no longer acceptable for new protection.

Sources:
- https://csrc.nist.gov/pubs/sp/800/131/a/r2/final
- https://www.nist.gov/news-events/news/2023/06/nist-withdraw-special-publication-800-67-revision-2

**TRANSFER VALIDATION:** this supports separating `allowed for new signatures` from `needed to verify old objects`. It does not define MintTap algorithms, dates or legal retention.

### CHANGE WATCH — SP 800-131A Rev.3
NIST published an Initial Public Draft of SP 800-131A Rev.3 on 2024-10-21, including proposed transitions for SHA-1/224-bit hashes, DSA and future 128-bit/quantum-resistant transitions. The final baseline used here remains Rev.2 until NIST publishes a superseding final.

Source:
- https://www.nist.gov/news-events/news/2024/10/transitioning-use-cryptographic-algorithms-and-key-lengths-comment-nist-sp

### NIST SHA-1 transition — preservation can outlive new-protection approval
NIST's SHA-1 transition notice says SHA-1 is being removed from applying cryptographic protection, while acknowledging that SHA-1 may still be needed to handle information protected before the termination date. This is a concrete precedent for keeping historical processing separate from current creation policy.

Source:
- https://www.nist.gov/news-events/news/2022/12/nist-transitioning-away-sha-1-all-applications

### RFC 4998 — Evidence Record Syntax and cryptographic renewal
RFC 4998 is a Standards Track long-term archive precedent. It explicitly addresses evidence retained for decades while algorithms/certificates age. It defines timestamp renewal and hash-tree renewal, requiring renewal before the mechanisms protecting the latest archive timestamp lose security. When the hash protecting the archived data/tree itself weakens, renewal must cover the archived data/evidence rather than merely wrapping an old timestamp.

Source:
- https://www.rfc-editor.org/rfc/rfc4998.html

**TRANSFER VALIDATION:** ERS is not selected as the MintTap format. Its durable principle is that preservation is a chain of later evidence over earlier evidence/data, with the transition performed before the predecessor protection becomes untrustworthy.

### NIST SP 800-57 Part 1 Rev.5 — verification horizon differs from signing horizon
The current final NIST SP 800-57 Part 1 Rev.5 supports longer-lived public signature-verification use than private signing use and recognizes timestamping as one way to support historical verification.

Source:
- https://www.nist.gov/publications/recommendation-key-management-part-1-general-1

## SYNTHESIS 1 — distinguish four clocks
For long-horizon evidence, keep separate:
1. original event/evidence creation time;
2. predecessor cryptographic-policy acceptability interval;
3. preservation/migration/re-attestation time;
4. current verification time.

A 2032 preservation wrapper around a 2026 artifact does not make the original event a 2032 event. Conversely, successful current verification does not prove the predecessor algorithm was acceptable indefinitely.

`re-attested now ≠ originally signed now`; `verifies now ≠ predecessor acceptable now for new protection`.

## SYNTHESIS 2 — preservation adds lineage; it does not replace provenance
A migration object should bind the original immutable evidence (or an authenticated digest/tree commitment), predecessor verification context, migration policy/generation, successor algorithm/anchor context and migration time/evidence. Preserve the original signature/object separately where retention permits.

Do not silently normalize or reserialize the original and call the successor signature the original provenance.

`new wrapper valid ≠ old provenance rewritten`; `same semantics ≠ same signed bytes`.

## SYNTHESIS 3 — migrate before predecessor trust is lost
The strongest generic preservation case is a transition created while the predecessor chain can still be verified under the policy applicable to that transition. A later strong signature over an object after the old algorithm is already practically forgeable cannot by itself prove that the wrapped object existed before the break.

RFC 4998's renewal-before-weakness rule is the central precedent.

`strong successor signature ≠ proof predecessor was still trustworthy at migration`; `migration after break ≠ retroactive preservation`.

If the migration boundary cannot be established, classify the chain `WINDOW-UNCERTAIN/UNVERIFIABLE` rather than manufacturing continuity.

## SYNTHESIS 4 — timestamp renewal and data/hash renewal solve different failures
If the aging problem is the timestamp/signature public-key algorithm, a later preservation timestamp/attestation over the existing evidence may be sufficient in a given design. If the digest binding the original object is itself no longer collision-resistant enough for the policy, merely wrapping the weak digest can preserve ambiguity; the original data/evidence may need to be re-bound under a stronger digest while retaining the old chain.

`new timestamp ≠ hash migration`; `strong signature over weak ambiguous digest ≠ strong object binding`.

## SYNTHESIS 5 — trust-anchor expiry is not identical to compromise
Certificate/trust-anchor expiration, policy deprecation, algorithm weakness, key compromise and verifier removal have different effects. Expiry can be a planned lifecycle boundary; compromise can invalidate trust over an uncertain interval; algorithm weakness can change the feasibility of forgery; implementation removal can make verification unavailable without proving the old evidence false.

Do not collapse them into `invalid`.

Useful states include `HISTORICAL-VERIFIED`, `PRESERVATION-VERIFIED`, `LEGACY-VERIFY-ONLY`, `MIGRATION-DUE`, `WINDOW-UNCERTAIN`, `UNVERIFIABLE`, `POST-COMPROMISE-UNTRUSTED`.

## SYNTHESIS 6 — anchor succession needs authenticated lineage and purpose separation
A successor preservation anchor must be authenticated by a transition path that was valid at the relevant time or by an explicit reconstitution path when ordinary succession is no longer trustworthy. Merely presenting a newer certificate/root is not continuity.

Historical trust-anchor material can remain in an isolated verifier bundle without being admitted as current session/recovery/signing authority.

`anchor expired ≠ history erased`; `old anchor retained ≠ old anchor current`; `new anchor newer ≠ successor authorized`.

## SYNTHESIS 7 — re-attestation is evidence about evidence
A preservation service may state that it verified an old chain under policy P at time T and bind that verified object into a new cryptographic envelope. That statement is a new event with its own signer, policy, timestamp, custody and compromise lifecycle.

It should not claim stronger historical facts than it actually observed. If it did not independently establish pre-compromise timing, it cannot convert `WINDOW-UNCERTAIN` to `PRE-COMPROMISE-VERIFIED` by re-signing.

`re-attestation preserves a claim ≠ re-attestation upgrades an unsupported claim`.

## SYNTHESIS 8 — algorithm deprecation requires an inventory and deadline, not emergency fallback
Long-horizon evidence needs a crypto-agility inventory covering algorithms, key sizes, hash-tree/digest roles, timestamp/TSA algorithms, trust anchors, canonicalization/verifier versions and retained evidence populations. A change watch must identify a migration deadline with enough margin to complete and validate renewal before predecessor protection becomes unacceptable.

`algorithm deprecated ≠ immediate historical deletion`; `deadline known ≠ migration complete`; `online fleet migrated ≠ archive migrated`.

## SYNTHESIS 9 — obsolete verifier retirement is a two-sided gate
Removing vulnerable legacy verifier code reduces attack surface, but deleting it before all required evidence is migrated or independently verifiable can destroy historical capability. Decommission only when evidence inventory and negative-oracle checks show no required unmigrated population, or when an isolated replacement verifier/preservation chain is proven.

Legacy verification should be read-only, purpose-scoped, sandboxed/isolated as appropriate and excluded from current request/authentication/recovery paths.

`legacy verifier removed ≠ legacy evidence preserved`; `legacy verifier retained ≠ expose it to production traffic`.

## SYNTHESIS 10 — long-offline PWA does not need to carry the preservation authority plane
A LogMate/EFB-like iPad can return after multiple evidence-algorithm/anchor migrations. Unique local records should be preserved first. Current synchronization authorization should come from current authority. Historical evidence can be uploaded/preserved and evaluated by the appropriate server/investigator verifier plane.

Do not make old TSA/root/verifier keys synchronization credentials merely because local records contain old signatures.

`client carries old evidence ≠ client carries current authority`; `cannot locally verify old archive chain ≠ delete local operational data`.

## SYNTHESIS 11 — migration atomicity matters
For a preservation batch, `new wrapper written` and `old evidence retained` are separate durability facts. A crash between them can leave an orphaned wrapper or destroy the only predecessor evidence if destructive replacement was attempted.

Prefer append/preserve semantics until successor verification and durable replication are proven. Record migration identity, source object commitment, successor object identity and completion state.

`migration job success ≠ every object migrated`; `new evidence durable ≠ predecessor evidence safely retired`.

## SYNTHESIS 12 — legal/admissibility claims remain external
RFC/NIST cryptographic preservation principles do not define aviation, employment, tax, investment or court admissibility. Product retention horizons and required preservation procedures remain legal/domain dependencies.

`long-term cryptographic verification ≠ legal admissibility`; `technical preservation horizon ≠ mandated retention horizon`.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. maintain separate policy for new cryptographic protection and historical verification;
2. preserve original evidence/provenance and add migration/re-attestation lineage rather than overwriting it;
3. initiate preservation before predecessor algorithms/anchors become untrustworthy, with explicit margin and completion evidence;
4. distinguish signature/timestamp renewal from hash/object rebinding when the underlying digest itself weakens;
5. retain read-only historical verification context without retaining old private signing/recovery authority merely for verification;
6. make re-attestation claims no stronger than the predecessor evidence actually supported;
7. inventory crypto dependencies and retained evidence populations so deprecation deadlines are actionable;
8. decommission legacy verifier code only after required populations are migrated or independently verifiable;
9. make preservation migration crash-safe and provenance-preserving;
10. keep long-offline PWA synchronization dependent on current authority, not preservation keys;
11. preserve explicit `UNKNOWN/UNCERTAIN/UNVERIFIABLE` states instead of manufacturing continuity;
12. do not select a product algorithm, TSA, PKI, archive format or retention horizon from generic research alone.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
When implementation begins, validate exact WebCrypto/WebKit/browser support for current algorithms and any client-side verifier. Browser support is an execution constraint, not the constitutional definition of historical validity.

### Track B — DEPENDENCY
Evidence UI must distinguish original evidence, later preservation evidence, migration due/complete, historical verify-only and uncertainty. Consume Design Studio interaction/accessibility evidence; do not reduce this to a green `signature valid` badge.

### Track C — VALIDATION
Destructive campaign grows **448 → 456 defined cases**:
1. predecessor signature algorithm becomes disallowed for new signatures while old evidence remains legacy-verifiable;
2. preservation wrapper is created before predecessor deprecation, then predecessor verifier is removed;
3. attacker creates a strong new wrapper only after the predecessor algorithm is practically broken and claims continuity;
4. timestamp public-key algorithm ages while object hash remains strong: timestamp renewal path;
5. object/hash-tree digest becomes weak: simple timestamp renewal is incorrectly used instead of rebinding data/evidence;
6. old trust anchor expires normally versus is later suspected compromised; system must produce different evidence states;
7. migration crashes after successor wrapper write but before durable predecessor/evidence-link commit;
8. long-offline iPad returns after two crypto/anchor migrations with unique local records and old evidence receipts.

Execution, physical iPad/Safari, real PKI/TSA/KMS, migration tooling, legal/aviation and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure migration inventory coverage, deadline risk, verifier failure rates, unmigrated legacy tails and preservation completion. Analytics cannot decide whether a predecessor chain was trustworthy at migration time.

## Persistent guards added through 212
- `allowed for historical verification ≠ allowed for new protection`;
- `re-attested now ≠ originally signed now`;
- `new wrapper valid ≠ old provenance rewritten`;
- `migration after break ≠ retroactive preservation`;
- `new timestamp ≠ hash migration`;
- `strong signature over weak ambiguous digest ≠ strong object binding`;
- `anchor expired ≠ history erased`;
- `new anchor newer ≠ successor authorized`;
- `re-attestation preserves a claim ≠ re-attestation upgrades an unsupported claim`;
- `algorithm deprecated ≠ historical evidence deleted`;
- `deadline known ≠ migration complete`;
- `legacy verifier removed ≠ legacy evidence preserved`;
- `migration job success ≠ every object migrated`;
- `client carries old evidence ≠ client carries current authority`;
- `long-term cryptographic verification ≠ legal admissibility`.

## OPEN
- actual MintTap/LogMate evidence algorithms, key sizes, trust anchors, TSA/checkpoint topology and crypto-policy dates;
- actual evidence schema/canonicalization and migration wrapper format;
- inventory of retained evidence and required horizon;
- migration atomicity/storage implementation;
- independent verifier and legacy-verifier isolation;
- legal/aviation/privacy retention/admissibility requirements;
- physical iPad/Safari/PWA behavior;
- real algorithm/anchor migration drills and human evidence-state comprehension.

## CHANGE WATCH
- NIST SP 800-131A Rev.3 progression beyond Initial Public Draft;
- NIST SHA-1 transition through the announced 2030 termination target;
- NIST post-quantum/128-bit transition guidance that changes preservation horizons;
- IETF/ETSI long-term validation/preservation standards relevant to evidence renewal;
- browser/WebCrypto removal/addition of algorithms needed by implementation.

## Gate result
**212 PASS (generic).** The Web Manager can now separate current cryptographic acceptability from historical verification, preserve original provenance through cryptographic renewal, distinguish timestamp renewal from hash/object rebinding, require migration before predecessor trust is lost, and retire obsolete verification capability without silently destroying required history.

Production validation remains OPEN.

## Next highest-value adjacent question
**213 — post-quantum preservation planning, hybrid-transition semantics & harvest-now-forge-later risk for long-lived evidence.** Determine which long-retained authenticity claims need migration before classical signature security materially degrades, how hybrid/classical+PQC evidence should express AND/OR acceptance semantics without downgrade ambiguity, how to preserve predecessor lineage through PQ migration, and how offline/erased clients converge without carrying obsolete cryptographic authority.