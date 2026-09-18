# 137 — PWA Checkpoint Lifecycle, Crypto Agility & Verifier Migration

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + CRYPTO/KEY + LONG-HORIZON VERIFIER VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 122–126 evidence/key/verifier continuity; 135–136 portable provenance/checkpoint continuity; Track A browser/local-storage lifecycle; Track B truthful migration/recovery UX; Track C old/new verifier and downgrade validation; Software Engineering owns eventual crypto/data implementation.

## Purpose

136 established that checkpoint continuity, freshness and non-equivocation are separate from per-entry authenticity. The adjacent lifecycle problem is that a useful provenance/checkpoint system may outlive a signing key, algorithm, canonicalization rule, serialization format, verifier implementation or trust-root arrangement.

Central rule:

> **Rotate cryptographic and verifier machinery without resetting lineage: bind each historical claim to the exact verifier context that governed it, bind transitions into the continuing lineage, preserve historical verification where justified, and never let historical compatibility silently restore retired write/current-trust authority.**

This study does not choose an algorithm, PQC scheme, KMS/HSM, signature container, key hierarchy or product format.

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** long-offline PWA clients can retain old verifier/application generations; browser update/storage mechanics bound when migration can occur but do not define cryptographic validity.
- **B UX/IA/Content — elevated consumer:** owns truthful states such as historical verification available, current verification unavailable, migration required, current writes blocked.
- **C Quality — high dependency pressure:** owns old/new key/algorithm/canonicalization/verifier matrices, downgrade, interruption and long-offline tests.
- **D Search/Analytics — constrained consumer:** inventory/telemetry can estimate remaining legacy use but cannot certify cryptographic validity or fleet completeness.
- **E Architecture/Security/Operations — highest-risk owner:** owns lifecycle states, transition evidence, anti-downgrade, key compromise response and verifier retirement.

Allocation remains E-heavy with A/C as prerequisite-critical dependencies.

## 2. SOURCE — crypto agility is an operational capability, not an algorithm field

NIST CSWP 39upd1 (final update 2026-06-29) defines crypto agility as capabilities to replace/adapt cryptographic algorithms across protocols, applications, software, hardware, firmware and infrastructure while preserving security and operations. RFC 7696 similarly warns that algorithm identifiers alone do not make migration easy: implementation, deployment and configuration changes are required, and weak algorithms often remain enabled for interoperability.

Sources checked 2026-09-19:
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://www.rfc-editor.org/info/rfc7696/

**SYNTHESIS:** checkpoint agility requires inventory, transition state, deployed verifier capability, retirement policy and evidence—not merely `alg` or `version` fields.

Guards:
- `algorithm identifier present ≠ crypto agility achieved`;
- `new verifier implemented ≠ deployed fleet can verify it`;
- `new signer active ≠ old verifier retired`;
- `migration planned ≠ migration executable`.

**CHANGE WATCH:** NIST CSWP 39upd1 is current 2026 guidance; algorithm-specific recommendations remain separately change-sensitive.

## 3. SOURCE — transition before failure and protect selection from downgrade

RFC 7696 recommends transition before current algorithms weaken to the breaking point and states that algorithm selection/negotiation should be integrity protected because otherwise downgrade attacks become possible. It also warns that too many algorithm alternatives increase complexity and rarely exercised code.

NIST SP 800-131A Rev.2 provides specific federal transition guidance to stronger keys/algorithms and reinforces planning ahead for cryptographic changes. Product-specific algorithm acceptability is not inferred from this federal profile.

Sources:
- https://www.rfc-editor.org/info/rfc7696/
- https://csrc.nist.gov/pubs/sp/800/131/a/r2/final

**MINTTAP DIRECTION:** model verifier/key/algorithm state explicitly and make current acceptance policy authoritative. Never accept a weaker/retired epoch merely because an imported package or stale client requests it.

Guards:
- `supports old algorithm ≠ may use old algorithm for new checkpoints`;
- `historical verification support ≠ current signing support`;
- `client requests legacy verifier ≠ server may downgrade`;
- `more supported algorithms ≠ more secure agility`.

## 4. Separate lifecycle dimensions

Do not collapse these into one `cryptoVersion`:
1. lineage/checkpoint format epoch;
2. canonicalization/serialization epoch;
3. digest/commitment algorithm epoch;
4. signature/MAC algorithm epoch;
5. signing/authentication key epoch;
6. trust-root/credential epoch;
7. verifier implementation/policy epoch;
8. application/API/Service Worker generation;
9. authorization-policy epoch;
10. migration/transition evidence identity.

A key rollover within one algorithm is not the same as an algorithm transition. A verifier implementation update is not automatically a trust-root change. Canonicalization changes can invalidate byte-level commitments even when cryptographic algorithms remain unchanged.

Guards:
- `key rotation ≠ algorithm migration`;
- `algorithm migration ≠ canonicalization migration`;
- `verifier upgrade ≠ trust-root rotation`;
- `application version current ≠ verifier context current`.

## 5. Historical verification and current authority are different

RFC 7696 notes that systems protecting stored data may need to support older algorithms to recover old protected material even when those algorithms are no longer used for new protection. That is a critical distinction for long-lived provenance.

A retired epoch can therefore have states such as:
- **CURRENT-SIGN+VERIFY**;
- **VERIFY-ONLY-HISTORICAL**;
- **QUARANTINED-VERIFY** (special isolated verifier/evidence path);
- **UNVERIFIABLE**;
- **REVOKED/COMPROMISED-CONTEXT**;
- **RETIRED-REMOVED**.

Historical verification never implies permission to create new checkpoints, accept remote mutations or re-establish current authorization.

Guards:
- `old signature verifies ≠ old algorithm approved for new signatures`;
- `historical key known ≠ historical private key retained`;
- `historical verifier retained ≠ exposed to untrusted live traffic`;
- `historical authenticity PASS ≠ current authorization PASS`.

## 6. Transition must preserve lineage rather than start an unrelated chain

A planned transition should produce evidence that binds the old trusted lineage state to the new verifier context. Conceptually this may require a transition checkpoint/record binding:
- lineage/subject;
- predecessor/current old head;
- new checkpoint/verifier-format epoch;
- new algorithm/key/trust context identifiers;
- transition policy/reason;
- effective boundary;
- sufficient old/new authentication evidence for the threat model;
- successor head or activation state.

Exact double-signing/cross-signing is architecture-specific and not mandated here. DNSSEC rollover literature demonstrates a reusable operational lesson: overlapping old/new material can be required so validators continue to validate during propagation; removal must wait until transition conditions are satisfied. RFC 7583 is DNSSEC-specific and is used only as a transfer pattern.

Guards:
- `new chain starts validly ≠ continuity from old chain proven`;
- `same subject identifier ≠ same authenticated lineage`;
- `old head copied into new format ≠ transition authenticated`;
- `dual evidence useful ≠ dual-sign every object forever`.

## 7. Anti-downgrade and anti-rollback across verifier epochs

The verifier must distinguish historical interpretation from current acceptance. Inputs should not choose arbitrary legacy policy. Relevant context may include lineage, declared epoch, algorithm/key identifiers, protected transition relation, current minimum accepted epoch and historical-only status.

COSE RFC 9052 provides a useful transfer lesson: ambiguity between implicit and explicit algorithms must be prevented, and applications should bind algorithm/key/context deliberately. This is not a requirement to use COSE.

Source:
- https://www.rfc-editor.org/rfc/rfc9052.html

Guards:
- `format says epoch 3 ≠ verifier may ignore current minimum epoch`;
- `cryptographically valid legacy object ≠ current-policy acceptable object`;
- `fallback succeeded ≠ downgrade safe`;
- `unknown algorithm ≠ try every installed verifier`.

## 8. Compromise is not ordinary rotation

Planned rotation and suspected compromise require different claims. If an old private key may have been compromised, a later object carrying a valid old-key signature does not by itself establish that it predates compromise. Historical validation may require trusted timing/checkpoint/anchor evidence that existed before compromise, depending on consequence and architecture.

Long-term signature literature such as RFC 5126 describes archival validation/time-stamping patterns intended to preserve validation as keys/algorithms age. It is legacy informational evidence, not a product mandate.

Source:
- https://www.rfc-editor.org/info/rfc5126/

Guards:
- `old signature mathematically valid ≠ signature predates key compromise`;
- `key revoked now ≠ every historical signature automatically false`;
- `key compromise suspected ≠ ordinary rollover procedure sufficient`;
- `re-sign old content now ≠ original historical authenticity restored`.

## 9. Canonicalization and format agility

Cryptographic continuity depends on what bytes/structure were committed. Changing JSON/CBOR encoding, normalization, field ordering, number representation, Unicode handling, omitted/default fields or compaction rules can alter commitments without changing business semantics.

Preserve the exact historical verification context or an authenticated transformation that explicitly maps old commitment to new representation. Never silently deserialize/re-serialize and call the new digest the original digest.

Guards:
- `same semantic record ≠ same committed bytes`;
- `parser can read old format ≠ verifier can reproduce old commitment`;
- `re-serialization succeeds ≠ original signature preserved`;
- `migration re-hashed data ≠ original checkpoint revalidated`.

## 10. Verifier migration and isolation

A long-lived system may need an old verifier after the main runtime no longer wants old crypto/parser code. Options are architecture-specific, but assurance requirements include:
- historical verifier is version-pinned/identified;
- its accepted input scope is bounded;
- it cannot issue current authority or silently mutate current state;
- results state which epoch/property was verified;
- legacy parser/crypto attack surface is isolated proportionally to risk;
- verifier dependencies/build provenance remain recoverable enough for the retention horizon.

Guards:
- `legacy verifier available ≠ legacy verifier belongs in primary request path`;
- `containerized verifier ≠ verifier trustworthy`;
- `old verifier output PASS ≠ current verifier policy PASS`;
- `source code archived ≠ executable verifier recoverable`.

## 11. Inventory and retirement evidence

RFC 7696 recommends measurement to determine whether implemented algorithms remain in use; unused algorithms should be candidates for removal/deprecation. For PWA fleets, telemetry is incomplete evidence because offline/managed clients may be unseen.

Track D may report observed algorithm/key/verifier generations, but retirement must account for unknown denominator, offline compatibility horizon, retained exports/backups and legal/recovery requirements.

Guards:
- `zero observed legacy use ≠ zero legacy artifacts exist`;
- `online fleet migrated ≠ offline fleet migrated`;
- `telemetry says 100% ≠ every export/backup re-verifiable`;
- `retirement deadline reached ≠ delete historical verification context blindly`.

## 12. PWA/EFB application boundary

A company-iPad PWA can remain offline across multiple signer/verifier/application generations. On reconnect:
- do not require old local data to pretend it was produced under the current epoch;
- verify old material under its historical context if that context remains supported;
- compare lineage/checkpoint transition evidence;
- migrate representation only with explicit transformation provenance;
- require current authorization/policy before remote mutation;
- permit safe local read/export recovery where feasible even when current remote writes are blocked;
- never assume Service Worker update atomically migrates verifier code, IndexedDB schema, keys and queued operations.

Guards:
- `old offline record valid historically ≠ auto-publishable now`;
- `Service Worker updated ≠ crypto/verifier migration complete`;
- `new verifier downloaded ≠ old data migrated`;
- `managed-iPad reconnect ≠ transition path validated`.

Actual WebKit/managed-device crypto APIs, key custody, storage, update and restore behavior remain OPEN.

## 13. UX boundary

Expose consequences rather than cryptographic internals. Candidate states:
- history verified under an older supported epoch;
- current verification requires migration;
- historical data remains readable/exportable but remote write is blocked;
- verifier context unavailable, so authenticity cannot currently be established;
- historical evidence affected by compromised/retired credentials;
- migration completed and continuity verified to a named checkpoint.

Never collapse `historically verified`, `currently authorized`, `latest`, `migrated`, `safe to sync` or `complete` into one green state.

Design Studio W088 is Stage 3 PRACTICE / NOT PASSED; persistence/offline/Sync, Safari/Firefox, screen-reader, physical-device/IME and human UX remain OPEN. No PWA migration UX PASS transfers.

## 14. Privacy and minimization boundary

Crypto agility does not justify indefinite retention of sensitive payloads or private keys. Preserve the minimum verifier context/evidence needed for declared historical claims and applicable retention requirements. Public verification material, algorithm identifiers and transition metadata may have different retention needs from private signing keys and full business payloads.

Guards:
- `historical verification needed ≠ retain historical private signing key`;
- `crypto inventory needed ≠ log sensitive payloads`;
- `key destroyed ≠ public verification evidence must be destroyed`;
- `privacy deletion ≠ fabricate continuity for removed content`.

## 15. Track C validation campaign

1. planned key rotation, same algorithm → old and new checkpoints verify in correct epochs;
2. algorithm migration with authenticated transition → lineage remains connected;
3. new chain without transition evidence → no continuity claim;
4. stale client requests retired algorithm for new write → reject current authority;
5. historical object under verify-only epoch → historical PASS, no new signing;
6. unknown algorithm identifier → fail boundedly, no algorithm guessing;
7. explicit/implicit algorithm ambiguity → reject according to declared context;
8. legacy verifier returns PASS on current-policy-forbidden object → historical-only result;
9. old key compromised after anchored checkpoint → distinguish pre/post-compromise evidence scope;
10. compromise time unknown → do not invent historical validity boundary;
11. re-sign historical content with new key → new attestation, not original signature;
12. canonicalization v1→v2 same semantics/different bytes → original commitment not silently replaced;
13. old parser unavailable → UNVERIFIABLE, not migrated by guess;
14. old parser available but unsafe → isolated historical path, no primary-path exposure;
15. verifier binary exists but dependency/runtime missing → recoverability failure;
16. current signer rotates while offline client queues old-epoch operation → historical intent preserved; current admission separate;
17. Service Worker update interrupted mid-verifier migration → mixed generation detected;
18. IndexedDB migration succeeds but verifier bundle stale → no false current PASS;
19. verifier updates but DB canonicalization marker stale → quarantine/migrate explicitly;
20. rollback application to version accepting retired epoch → server/current policy still rejects downgrade;
21. import old signed export after retirement → historical verification if supported; current admission separate;
22. export package omits verifier/algorithm epoch → incomplete verification context;
23. duplicate transition record → idempotent recognition;
24. same transition identity/different successor context → reject/quarantine;
25. transition checkpoint valid but stale relative to newer trusted head → historical, not current;
26. telemetry sees no legacy clients while offline export remains → retirement inventory catches artifact class;
27. historical public key retained, private key destroyed → historical verification remains possible where scheme/context permits;
28. current private key lost → recovery/rotation path must not rewrite old lineage;
29. accessible migration/recovery UX distinguishes historical verification from sync authority;
30. physical Safari/iPadOS long-offline old→new verifier/key/format migration remains required before product PASS.

## 16. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W088 IME + CONTEXTUAL UNDO SERVED-RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/IME, field-CWV, full-WCAG and human UX remain OPEN.

Software Engineering remains a bounded implementation dependency. Web Manager does not select algorithms, KMS/HSM, signature container, canonical serialization, key hierarchy or verifier deployment topology.

## 17. MINTTAP DIRECTION

For consequence-bearing PWA provenance/checkpoints, require explicit lifecycle metadata and transition evidence. Keep current signing/admission policy separate from historical verification. Bind algorithm/key/canonicalization/verifier epochs to lineage; make downgrade impossible through client-supplied legacy preference; preserve old verification context only for a declared retention/recovery purpose; isolate legacy verifier attack surface; and test long-offline old→new transitions before claiming product readiness.

Do not introduce crypto machinery merely because the model permits it. The minimum sufficient design depends on actual LogMate/MintTap data consequence, retention, threat model and implementation evidence.

## 18. OPEN / next bottleneck

Production OPEN: actual provenance/checkpoint format, canonicalization, algorithm/key hierarchy, signing custody, verifier topology, compromise/revocation semantics, long-term retention, PWA key/storage APIs, managed-iPad behavior, fleet compatibility horizon and destructive migration evidence.

Highest-value adjacent work: **PWA cryptographic compromise recovery, historical-validity windows & trust re-establishment** — determine how to scope evidence when a signing/verifier key or trust root is suspected compromised, how to avoid falsely invalidating all history or falsely trusting post-compromise artifacts, and how new trust can be established without an attacker-controlled old root authorizing its own successor.