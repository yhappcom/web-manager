# 136 — PWA Provenance Fork Detection, Checkpoint Anchoring & Anti-Splicing Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + CRYPTO/KEY + EXTERNAL-ANCHOR VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 122–126 evidence/key/verifier continuity; 131–135 reconciliation/provenance/portable transfer; Track A storage/offline mechanics; Track B truthful fork/gap UX; Track C omission/reorder/splice/fork validation; Software Engineering owns eventual data-structure/crypto implementation.

## Purpose

135 established that export/import/compaction are provenance transformations. The next failure class is subtler: every retained event or segment may be individually authentic while the presented history omits a valid segment, reorders segments, splices material from another branch, rolls back to an older head, or presents different valid-looking heads to different verifiers.

Central rule:

> **Per-item authenticity is not sequence integrity. Bind sequence position/parentage and scoped checkpoints strongly enough to detect omission, reordering, rollback and branch splicing for the consequence being protected; treat semantic legitimacy and current authorization as separate from cryptographic continuity.**

This study does **not** select Merkle trees, blockchain, Certificate Transparency, SCITT, Sigstore, a signing algorithm, a database, or a LogMate format. Those systems provide reusable assurance concepts and counterexamples.

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** local storage, lifecycle and offline duration determine which checkpoints/heads can survive and when a client can compare them. Browser storage is not an independent anchor.
- **B UX/IA/Content — elevated consumer:** owns truthful `history verified / branch detected / checkpoint stale / detail unavailable / review required` states without implying that cryptographic continuity means business correctness.
- **C Quality — high dependency pressure:** owns deletion/reorder/splice/rollback/equivocation and restart/export/import test oracles.
- **D Search/Analytics — constrained consumer:** telemetry can expose fleet/head divergence but cannot itself certify continuity unless it is part of the explicitly trusted evidence design.
- **E Architecture/Security/Operations — highest-risk owner:** owns sequence-integrity claims, anchor independence, verifier context, anti-rollback/fork response and cost/complexity proportionality.

Allocation remains E-heavy; A/C are prerequisite-critical and B is material because fork/gap states affect recovery decisions.

## 2. SOURCE — inclusion and consistency prove different things

RFC 9162 Certificate Transparency v2 defines Merkle inclusion proofs and Merkle consistency proofs separately. Inclusion proves that a leaf is included in a particular tree head. A consistency proof proves that a newer tree extends a previously advertised tree without changing the earlier prefix. RFC 9162 also requires auditing append-only behavior and consistency of the view presented to query sources.

Sources checked 2026-09-19:
- https://www.rfc-editor.org/rfc/rfc9162.html
- https://www.rfc-editor.org/info/rfc9162/

**SYNTHESIS:** an item proving membership under one checkpoint does not establish that no prior item was omitted from a different claimed scope, that the checkpoint is the newest trusted head, or that all verifiers saw one history.

Guards:
- `entry signature valid ≠ sequence intact`;
- `inclusion proven ≠ append-only continuity proven`;
- `checkpoint valid ≠ checkpoint fresh`;
- `one valid head ≠ no competing valid-looking head`.

## 3. SOURCE — transparency separates append-only from non-equivocation

RFC 9943 (SCITT Architecture, June 2026) defines append-only and non-equivocation as distinct VDS security requirements. Append-only means the statement sequence cannot be modified, deleted or reordered; non-equivocation means there is no fork and relying parties see a sequence consistent with receipts they have verified. It also notes that transparency does not prevent a dishonest issuer from making false statements; it makes statements auditable/accountable.

Sources checked 2026-09-19:
- https://www.rfc-editor.org/info/rfc9943/
- https://www.ietf.org/ietf-ftp/rfc/rfc9943.html

**SYNTHESIS:** cryptographic sequence continuity is not semantic truth. A perfectly append-only chain can faithfully preserve a bad, unauthorized or later-corrected operation.

Guards:
- `append-only PASS ≠ semantic legitimacy PASS`;
- `non-equivocation PASS ≠ statement accuracy PASS`;
- `historically registered ≠ currently authorized`;
- `cryptographically continuous ≠ conflict-free`.

**CHANGE WATCH:** RFC 9943 is newly published in June 2026. It is conceptual/standards evidence, not a MintTap/LogMate architecture mandate.

## 4. Threat model: individually valid pieces can compose a false history

Distinguish at least these attacks/failures:
1. **omission** — valid event/segment is absent from the presented package;
2. **reordering** — valid events are presented in an order not committed by the lineage;
3. **rollback** — an older authentic checkpoint/head is presented as current;
4. **prefix truncation** — a valid older prefix is presented while later history is hidden;
5. **suffix truncation** — package ends before its declared/current expected head;
6. **branch splice** — valid segment from lineage B is inserted into lineage A without a legitimate merge/admission event;
7. **fork/equivocation** — different relying parties receive incompatible successor heads;
8. **checkpoint substitution** — valid checkpoint from another subject/device/epoch is used against the wrong history;
9. **compaction-boundary splice** — a compacted checkpoint is connected to a later segment whose declared predecessor/range does not actually match;
10. **re-export laundering** — imported material is re-exported in a way that erases original branch/import transformation identity.

Per-record signatures/hashes alone do not rule these out.

## 5. Sequence binding: minimum conceptual requirements

A provenance segment/checkpoint intended to support continuity should bind enough context to make accidental or malicious substitution detectable. Depending on actual architecture, relevant fields may include:
- lineage/subject identifier and namespace;
- checkpoint/segment identity;
- covered revision/range/count;
- predecessor checkpoint/head or parent relation;
- content commitment/root/digest for the declared scope;
- schema/canonicalization/integrity format version;
- compaction/redaction declaration where applicable;
- producer/verifier/key epoch where cryptographic authentication is used;
- branch/merge/admission identity when multiple lineages legitimately converge.

This is a requirements model, not a wire format.

Guards:
- `hash chain exists ≠ lineage context bound`;
- `same digest algorithm ≠ same history namespace`;
- `valid parent hash ≠ current head known`;
- `branch merged structurally ≠ merge semantically admitted`.

## 6. Checkpoints and anchors are not the same thing

A **checkpoint** is a compact commitment to a lineage state/range. An **anchor** is a copy/attestation of a checkpoint held in a context whose failure/rewriting assumptions differ enough to help detect rollback or equivocation.

If the current mutable database stores both history and its only checkpoint, compromise of that database may rewrite both consistently. Likewise, an IndexedDB record containing a head does not independently anchor another record in the same origin/storage failure domain.

Guards:
- `checkpoint stored ≠ independently anchored`;
- `history + checkpoint in same mutable failure domain ≠ rollback-resistant evidence`;
- `second copy ≠ independent anchor`;
- `external anchor ≠ globally trusted anchor`.

Anchor independence is threat-specific, not binary. A server-side checkpoint may be independent of browser-local corruption while still sharing organization/key/provider risk.

## 7. Freshness and anti-rollback

A valid old checkpoint is still cryptographically valid. A verifier therefore needs a freshness/continuity basis appropriate to the claim, such as a previously retained trusted head, an independently retained anchor, a monotonic revision known from another trusted context, or a current service comparison. The exact mechanism is product-specific.

Never infer freshness from signature validity alone.

Guards:
- `authentic old head ≠ current head`;
- `rollback detected ≠ missing content reconstructed`;
- `newer timestamp ≠ descendant checkpoint`;
- `higher local counter ≠ globally authoritative revision`.

This extends the 123–125 freshness/verifier-context work into portable provenance.

## 8. Fork/equivocation detection needs comparison, not merely verification

RFC 9162 explicitly notes that checking whether all entities received a consistent log view requires sharing/comparing log responses. A verifier that only sees one internally valid fork cannot prove another fork does not exist.

**SYNTHESIS:** non-equivocation assurance requires some comparison domain: prior trusted state, independent observer/anchor, another device/server view, auditor/witness, or another architecture-specific mechanism. There is no generic proof of `no unseen fork anywhere` from one isolated package.

Guards:
- `one branch verifies ≠ no fork exists`;
- `two heads individually authenticate ≠ heads are mutually consistent`;
- `offline verifier sees no conflict ≠ ecosystem non-equivocation proven`.

For long-offline EFB clients this means a device may verify its local lineage while still being unable to know whether a newer or competing server/device branch exists until a comparison opportunity occurs.

## 9. Anti-splicing across compaction/export/import epochs

Compaction and transfer create new derived artifacts. To prevent valid segments being rearranged into a false chain:
- bind compacted checkpoint to the exact source lineage/range it summarizes;
- bind post-compaction continuation to that checkpoint/declared predecessor;
- preserve export/import transformation identity;
- preserve branch identity until reconciliation/admission;
- do not let destination reserialization erase source lineage;
- reject/quarantine same checkpoint/segment identity with different committed content;
- represent missing intermediate detail as unavailable rather than manufacturing a seamless narrative.

Guards:
- `valid segment A + valid segment B ≠ valid A→B transition`;
- `compaction checkpoint matches root ≠ omitted semantics recoverable`;
- `imported branch accepted ≠ original branch erased`;
- `re-exported successfully ≠ lineage laundering prevented`.

## 10. Legitimate forks are not automatically attacks

Offline-first products can legitimately create divergent device branches. A fork detector must not classify every divergence as malicious equivocation. Distinguish:
- expected offline branch divergence;
- server-side authoritative history fork that should not exist;
- stale prefix/rollback;
- duplicate/replayed branch;
- explicit merge/admission result;
- unknown relationship due to missing lineage evidence.

The response depends on domain policy. Preserve both branches and route to reconciliation when semantic conflict cannot be safely automated.

Guard: `fork detected ≠ attacker proven`; `legitimate branch ≠ automatically authoritative merge`.

## 11. Do not jump to blockchain or public transparency infrastructure

Certificate Transparency, SCITT and Sigstore demonstrate strong append-only/non-equivocation patterns, but their scale/threat model does not imply a small app company needs a public transparency log, blockchain, consensus cluster or multi-party witness network.

A proportional design may use, for example, bounded per-record revision/precondition controls plus periodic scoped checkpoints retained in a sufficiently independent recovery/evidence context. Whether that is enough depends on consequence, adversary capability, legal/safety requirements, recovery objectives and implementation cost.

Guards:
- `fork resistance required ≠ blockchain required`;
- `checkpointing useful ≠ public transparency service required`;
- `stronger cryptography ≠ better system if verifier/key/operations fail`;
- `more witnesses ≠ proportionately better assurance`.

## 12. SOURCE — receipts and consistency proofs remain proof-scoped

RFC 9942 defines COSE Receipts for verifiable data structures and includes consistency-proof support for RFC9162_SHA256. Verification first checks the receipt signature and then the consistency proof; a valid signature over an invalid consistency proof is not a valid consistency result.

Source checked 2026-09-19:
- https://www.rfc-editor.org/info/rfc9942/

**TRANSFER VALIDATION:** this supports the broader Web Manager rule that evidence dimensions must be composed, not collapsed. Signature authenticity and sequence-consistency proof are distinct checks.

Guard: `signed proof object ≠ embedded proof valid`.

## 13. PWA/EFB application boundary

For a company-iPad PWA:
- local IndexedDB may retain a lineage head/checkpoint, but that head shares browser-storage durability risk;
- an offline device can validate local parent/sequence relations without proving that no newer remote branch exists;
- reconnect should compare current server/admission state before granting remote mutation authority;
- export should bind its declared source head/range and preserve any known branch/gap state;
- import must not collapse destination and source heads before reconciliation;
- an old authentic export may be valuable recovery evidence while being stale for current remote writes;
- Service Worker update generation and data-lineage head are separate state dimensions.

Guards:
- `local head verifies ≠ remote head known`;
- `Service Worker current ≠ data lineage current`;
- `data lineage current ≠ remote authorization current`;
- `offline branch valid ≠ safe to auto-publish`.

Actual managed-iPad/WebKit storage, file handling, device policy and server comparison remain OPEN.

## 14. UX boundary

Track B/Design Studio should expose consequences, not cryptographic jargon. Useful states may include:
- history continuity verified to checkpoint X;
- checkpoint is older than current known state;
- another branch/history exists;
- some detail is unavailable but retained checkpoint still verifies its declared range;
- imported history requires reconciliation;
- source/history cannot be verified;
- local data remains readable/exportable while remote write is blocked.

Never display `secure`, `complete`, `latest`, `synced` or `verified` without naming the property actually established.

Design Studio W087 supplies current served-runtime evidence about contextual command routing and branch ownership, but persistence/offline/Sync, Safari/Firefox, screen reader, physical-device and human UX remain OPEN. No PWA fork/recovery UX PASS transfers.

## 15. Privacy/minimization boundary

Anti-splicing does not require retaining every historical payload indefinitely. Checkpoints can preserve scoped commitments while retention policy removes unnecessary detail, but the system must downgrade claims when removed detail prevents semantic audit. Avoid external anchors that unnecessarily expose user/flight/investment content; an anchor may only need a scoped commitment plus non-sensitive context, depending on threat model.

Guards:
- `external commitment ≠ externalize sensitive payload`;
- `privacy compaction ≠ pretend full audit detail remains`;
- `minimal anchor ≠ sufficient anchor until threat model validated`.

## 16. Track C destructive validation campaign

1. delete one middle event while retaining surrounding signed events → sequence failure/gap;
2. reorder two valid events → parent/range/sequence failure;
3. present authentic older head as current → rollback/staleness detected when comparison evidence exists;
4. truncate suffix but claim current complete package → declared-scope/head mismatch;
5. export an explicitly historical prefix → valid historical package, not falsely current;
6. splice valid segment from lineage B into A → lineage/predecessor mismatch;
7. splice same-subject but incompatible branch → branch conflict, no silent merge;
8. same checkpoint ID/different committed root → reject/quarantine;
9. valid checkpoint from another device/subject → namespace mismatch;
10. valid checkpoint from retired epoch → historical verification may pass; freshness/current authority separate;
11. current mutable DB and same-DB checkpoint both rolled back → local-only verification cannot claim independent detection;
12. independent retained newer checkpoint + rolled-back DB → rollback detectable;
13. two individually signed incompatible heads → fork/equivocation state;
14. isolated verifier receives only fork A → cannot claim global non-equivocation;
15. later comparison exposes fork B → preserve evidence and block unsafe convergence;
16. legitimate offline device divergence → classify branch, not attacker;
17. branch merge with explicit reconciliation/admission → new merge provenance retained;
18. branch concatenation without merge event → reject;
19. compaction checkpoint + continuation with wrong predecessor → reject/quarantine;
20. compacted detail unavailable → continuity claim remains scoped, detail not reconstructed;
21. export/import/re-export → original source lineage and transformations survive;
22. re-export strips import transformation → provenance integrity failure;
23. duplicate checkpoint/package replay → idempotent recognition;
24. signature valid but consistency proof invalid → overall consistency verification fails;
25. verifier lacks historical key/context → UNVERIFIABLE, not false PASS;
26. anchor provider unavailable → local data may remain usable; independent freshness claim unavailable;
27. external anchor compromised but local history intact → do not let anchor alone rewrite semantic state;
28. analytics reports all clients on same head while sampled cryptographic comparison disagrees → telemetry cannot override evidence;
29. accessible branch/reconciliation UX preserves semantic focus and clearly separates local-read from remote-write authority;
30. physical Safari/iPadOS restart/eviction/export/import/reconnect plus server-head comparison remains required before product PASS.

## 17. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W087 CONTEXTUAL UNDO ROUTING SERVED-RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device, field-CWV, full-WCAG and human UX remain OPEN.

Software Engineering implementation evidence remains a bounded dependency. Web Manager does not choose hash-chain/Merkle/VDS/signature/checkpoint storage or sync implementation here.

## 18. MINTTAP DIRECTION

For PWA/EFB-like products with consequence-bearing offline data, require provenance continuity claims to be explicitly scoped. Preserve lineage/parentage/range across compaction/export/import; distinguish membership, sequence continuity, freshness, non-equivocation, semantic legitimacy and current authorization; use threat-proportionate independent checkpoint anchoring where rollback/fork detection warrants it; and do not infer a need for blockchain/public transparency infrastructure without product risk evidence.

No production provenance scheme, external anchor, cryptographic key model, server architecture or LogMate behavior is inferred.

## 19. OPEN / DEPENDENCY / CHANGE WATCH

**OPEN:** actual consequence classes; authoritative lineage topology; whether server history is single-linear or branch-aware; checkpoint cadence; namespace; canonicalization; crypto/key hierarchy; independent anchor requirement/provider; offline comparison horizon; merge/admission policy; retention/privacy/legal/aviation requirements; managed-iPad persistence/export; physical fork/recovery drills.

**DEPENDENCY:** Software Engineering owns executable data-structure/transaction/crypto implementation once product truth exists. Track C owns destructive/runtime verification. Track B/Design Studio own concrete branch/gap/recovery UX.

**CHANGE WATCH:** RFC 9942/9943 were published June 2026 and should be watched for implementation/errata/ecosystem maturation. Browser/WebKit managed-device behavior remains runtime evidence, not inferred from transparency standards.

## 20. Gate

**PASS (generic).** The Web Manager can distinguish item authenticity from sequence integrity; inclusion from consistency; append-only from non-equivocation; checkpoint from independent anchor; authentic old state from current state; legitimate offline branches from server equivocation; and cryptographic continuity from semantic legitimacy/current authorization. The manager can define anti-omission/reorder/splice requirements and a proportional validation campaign without prematurely selecting heavyweight infrastructure.

Product, managed-iPad, data-model, cryptographic/key, external-anchor and destructive-runtime validation remain OPEN.

## 21. Adjacent high-value question completed in this run

The immediate adjacent question — whether anti-splicing necessarily requires blockchain/public transparency infrastructure — is closed generically: **no**. The required mechanism is threat- and consequence-dependent. Public transparency/witnessing is one design family; scoped checkpoints plus sufficiently independent retention/comparison may be adequate for smaller threat models, but adequacy cannot be certified until product consequences, adversary model, authority topology and recovery objectives are known.

## 22. Next highest-value adjacent work

**PWA checkpoint lifecycle, key/algorithm agility & verifier migration without lineage reset**: determine how checkpoint/signature algorithms, keys, canonicalization and verifier formats can rotate over years without turning every rotation into a new unconnected history, while preserving historical verification and preventing downgrade/rollback to retired verifier epochs.