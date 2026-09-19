# 161 — PWA Closure-Evidence Key/Trust Compromise, Verifier Migration & Long-Horizon Proof Survivability

Status: **PASS (generic) / PRODUCT + KEY/TRUST + VERIFIER + LONG-HORIZON + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 137 checkpoint lifecycle/crypto agility; 160 closure-evidence retention/verifier independence; Track A long-offline SW/cache/storage behavior; Track B truthful historical/current-confidence UX; Track C destructive migration/compromise validation; Track D inventory/diagnostic telemetry only; Software Engineering owns eventual crypto/verifier implementation.

## Why this study exists

160 made closure a versioned, independently verifiable claim. The next failure is long-horizon trust decay: the evidence-signing key, verifier credential, trust root, hash/signature algorithm, canonicalization rule or verifier implementation may rotate, expire, become unsupported or be suspected compromised while the closure evidence must remain interpretable.

The security objective is not to keep every old credential alive. It is to preserve bounded historical proof while preventing historical compatibility from becoming present authority, and to avoid laundering evidence whose trustworthy time boundary cannot actually be established.

Central rule:

> **Historical proof survivability requires preserved verification context plus authenticated migration lineage; compromise requires an evidence-validity boundary, not ordinary rotation; and no migration may turn retired historical verification into current signing, admission or closure authority.**

## Five-track balance

- **A Platform/Browser — high dependency supplier:** a long-offline PWA can retain old verifier code, cached trust metadata, canonicalization versions and closure claims across several server generations. Browser state does not establish current trust.
- **B UX/IA/Content — elevated consumer:** owns truthful states such as `HISTORICALLY VERIFIED`, `TRUST CONTEXT RETIRED`, `COMPROMISE WINDOW UNCERTAIN`, `REVALIDATION REQUIRED`, and `CURRENTLY VERIFIED` without collapsing them into one green success state.
- **C Performance/Accessibility/Quality — high dependency pressure:** owns migration, compromise-window, rollback, mixed-generation, evidence-loss and accessible-state tests.
- **D Search/Discovery/Analytics — constrained diagnostic consumer:** inventory/telemetry can reveal observed legacy generations but cannot prove every offline/exported artifact has migrated or that a historical signature predates compromise.
- **E Architecture/Security/Operations — highest-risk owner:** owns key/trust lifecycle, compromise scoping, migration lineage, anti-downgrade and long-horizon verifier survivability.

Allocation remains E-heavy with A/C as critical dependencies. This extends rather than duplicates 137: 137 established generic checkpoint agility; 161 applies the model specifically to closure evidence, compromise timing and retained proof.

## SOURCE

### NIST CSWP 39upd1 — crypto agility is an operational capability

NIST CSWP 39upd1, final 2026-06-29, defines crypto agility as capabilities to replace/adapt cryptographic algorithms across protocols, applications, software, hardware, firmware and infrastructure while preserving security and ongoing operations. The earlier CSWP 39 is withdrawn/superseded by upd1.

Source: https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final

**SYNTHESIS:** closure-proof agility is not an `alg` field. It requires inventory, transition state, deployed verifier capability, retirement rules, recovery evidence and explicit acceptance policy.

### NIST SP 800-57 Part 1 Rev.5 — key lifecycle/archive baseline

SP 800-57 Part 1 Rev.5 remains the final NIST key-management baseline. It distinguishes key lifecycle functions including archival/recovery and requires protection of archived key information. The NIST key-management publication index currently lists Rev.6 as draft, so Rev.6 is CHANGE WATCH rather than a final baseline.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/Projects/Key-Management/publications

**TRANSFER VALIDATION:** long-horizon verification may require retained verification information, but this does not justify retaining historical private signing keys merely because old signatures must remain verifiable.

### RFC 5280 — compromise time can differ from revocation processing time

RFC 5280 defines `invalidityDate` as the date a private key is known or suspected to have been compromised or a certificate otherwise became invalid; this may precede the CRL `revocationDate`, which records when the CA processed the revocation.

Source: https://www.rfc-editor.org/rfc/rfc5280.html

**TRANSFER VALIDATION:** `revocation published at T2` does not prove all signatures before T2 are trustworthy. Where consequence requires historical validity, distinguish compromise/invalidity knowledge from administrative revocation processing.

### RFC 3161 — trusted time as a building block, not automatic truth

RFC 3161 defines a time-stamp protocol providing evidence that a datum existed before a particular time and gives an example in which a signature time-stamp can help determine whether a signature predates certificate revocation. Verification still requires checking the timestamp token, its binding to the signature, certificate validity and relevant revocation information.

Source: https://www.rfc-editor.org/rfc/rfc3161.html

**TRANSFER VALIDATION, NOT PRODUCT PRESCRIPTION:** independently trustworthy temporal evidence can help bound historical claims. MintTap/LogMate is not thereby required to deploy RFC 3161/TSA infrastructure.

## SYNTHESIS — separate six lifecycle dimensions

Do not collapse long-horizon proof into one `cryptoVersion`. Track at least:
1. closure/evidence lineage generation;
2. canonicalization/serialization generation;
3. digest/commitment algorithm generation;
4. signature/authentication algorithm and signing-key generation;
5. trust-root/verifier-policy generation;
6. verifier implementation/runtime generation.

Application/API/Service Worker and authorization-policy generations remain separate additional dimensions.

Persistent guards:
- `key rotation ≠ algorithm migration`;
- `algorithm migration ≠ canonicalization migration`;
- `verifier upgrade ≠ trust-root rotation`;
- `signature mathematically valid ≠ signature trusted for the claimed historical interval`;
- `certificate revoked at T2 ≠ compromise began at T2`;
- `historical verification support ≠ current signing authority`;
- `old public verification material retained ≠ old private authority retained`;
- `new signature over old evidence ≠ original historical authenticity recreated`;
- `timestamp present ≠ timestamp independently trustworthy`;
- `migration completed online ≠ every offline/exported artifact migrated`.

## Planned rotation and compromise are different protocols

### Planned rotation

A planned transition can preserve continuity by binding the accepted predecessor closure/evidence head to the successor verifier context. Conceptually the transition record may commit to predecessor head, successor verifier/trust context, effective boundary, transition reason/policy and sufficient old/new authentication evidence for the threat model.

Exact cross-signing, double-signing or timestamp mechanisms are implementation-specific and are not mandated.

### Suspected or confirmed compromise

Compromise invalidates the assumption that a valid old-key signature necessarily came from the legitimate signer. Historical evidence must be classified relative to the strongest defensible boundary:
- **PRE-COMPROMISE-ANCHORED** — independent evidence supports existence before the bounded compromise interval;
- **SUSPECT-WINDOW** — signature verifies mathematically but trustworthy creation time cannot be bounded outside the compromise window;
- **POST-COMPROMISE/REJECTED** — evidence is known to fall after the invalidity boundary or otherwise fails current policy;
- **UNVERIFIABLE** — required historical verifier/trust context no longer exists or cannot be safely reconstructed.

Do not invent a precise compromise timestamp from detection time, revocation processing time, first malicious observation or operator memory.

`compromise discovered at T3 ≠ compromise began at T3`.

## Trust re-establishment must not launder suspect history

After compromise, a new key/root/verifier generation may establish future authority. It cannot retroactively make suspect old evidence trustworthy simply by re-signing it.

A migration can truthfully attest:
- the bytes/claim were observed during recovery;
- the historical object mathematically verifies under its old context;
- independent pre-compromise evidence exists, if actually established;
- the object was imported into the new lineage at a named recovery generation.

It must not claim the new signature proves the old signer legitimately created the historical claim at the purported old time.

Guards:
- `re-signing succeeds ≠ historical legitimacy restored`;
- `new trust root accepts import ≠ old compromise ambiguity erased`;
- `recovery operator approved ≠ historical signer intent proven`.

## Long-horizon proof package

For consequence-bearing retained closure evidence, survivability may require enough context to reconstruct the historical verification question without retaining live authority. Conceptually preserve or identify:
- closure/evidence claim and lineage generation;
- exact committed representation or reproducible canonicalization version;
- digest/signature algorithm identifiers and parameters where required;
- historical public verification material/certificate chain or stable retrieval references where justified;
- verifier/trust-policy generation and status;
- transition/retirement/compromise lineage;
- trusted temporal/anchor evidence when the threat model depends on historical timing;
- current disposition (`VERIFY-ONLY`, `SUSPECT`, `SUPERSEDED`, `UNVERIFIABLE`);
- privacy/retention metadata.

Exact schema remains OPEN. Private signing keys and bearer recovery credentials are not part of a generic proof package.

## Algorithm and canonicalization migration

When an old algorithm or representation approaches retirement, migration must preserve two different statements:
1. **historical statement:** what was originally committed/signed and under which context;
2. **migration statement:** what a later trusted process observed/transformed and how the successor representation relates to the original.

Never silently deserialize, normalize and re-sign a new representation as though it were the original object. If a transformation is necessary, retain authenticated transformation provenance and enough old context to substantiate the relationship for the required retention horizon.

If the old algorithm is no longer considered secure enough for the claim's consequence, merely retaining an old verifier does not solve the assurance problem. The system may need an earlier independently protected anchor, migration before deprecation, or an explicit downgrade of confidence to `UNVERIFIABLE/SUSPECT`.

## Verifier migration and isolation

Historical verification code can become attack surface. If retained:
- identify/version-pin the verifier and its dependencies;
- bound accepted input and purpose;
- isolate it from current signing/admission paths proportionally to risk;
- make outputs property-specific (`historical signature verifies`, not generic `safe`);
- prevent legacy input from selecting weaker current acceptance policy;
- retain enough build/runtime provenance to recover the verifier where the retention objective requires it.

`source code archived ≠ verifier executable` and `legacy verifier executable ≠ safe to expose to untrusted live traffic`.

A retired verifier may be used in a quarantined historical path without becoming a current authority oracle.

## PWA / Service Worker / managed-iPad application

A LogMate-like company iPad can remain offline across multiple closure-key, verifier, canonicalization and Service Worker generations.

On reconnect:
- treat local closure/evidence generation as historical input, not current trust;
- fetch/establish current server trust policy independently of cached UI state;
- verify historical material under the correct old context only if that context remains supported;
- apply compromise-window classification before presenting old closure as trustworthy;
- preserve unique local flight data even if its old closure proof becomes `SUSPECT` or `UNVERIFIABLE`;
- require current authorization before remote mutation;
- record representation migration as a new transformation event rather than rewriting original provenance;
- never assume Service Worker activation atomically migrates IndexedDB, verifier bundles, keys, queued operations and trust policy.

Actual WebKit/managed-iPad crypto APIs, key custody, storage eviction, update, backup/restore and MDM behavior remain OPEN.

## UX boundary

Track B should expose consequence, not cryptographic ceremony. Required conceptual distinctions include:
- **CURRENTLY VERIFIED** — current lineage/trust policy supports the claim;
- **HISTORICALLY VERIFIED** — valid only under a named retired historical context;
- **REVALIDATION REQUIRED** — currentness/trust transition not yet established;
- **COMPROMISE WINDOW UNCERTAIN** — mathematical verification exists but historical legitimacy cannot be safely bounded;
- **UNVERIFIABLE** — required context is unavailable/unsafe;
- **SUPERSEDED/REOPENED** — historically authentic but no longer current.

Do not use color alone or the word `verified` without scope. Accessibility/human validation remains OPEN.

## Privacy and retention boundary

Long-horizon verification does not justify indefinite payload or private-key retention. Separate:
- public verification context and non-secret transition metadata;
- sensitive evidence content required for a declared retention purpose;
- private signing/recovery material;
- diagnostic telemetry.

Retain the minimum necessary for the declared proof and applicable obligations. Destroying a private signing key after its authorized lifecycle can coexist with retaining public verification evidence. Product/legal retention decisions remain OPEN.

## MINTTAP DECISION — minimal generic model

1. Preserve closure evidence under explicit key/algorithm/canonicalization/trust/verifier generations rather than one opaque crypto version.
2. Treat planned rotation and compromise as different protocols.
3. On compromise, classify historical evidence against a defensible validity interval; never equate detection or revocation-processing time with compromise start.
4. Re-signing/migrating old evidence creates a new attestation/transformation event and never recreates original historical legitimacy.
5. Preserve historical verification where justified without retaining historical current-signing/admission authority.
6. Protect migration lineage against downgrade/rollback; old verifier support is verify-only or quarantined when retired.
7. Preserve enough representation/verifier context for the declared retention horizon, but do not hoard private keys, bearer secrets or unnecessary payloads.
8. Long-offline PWA state may carry old evidence but cannot select current server trust policy or resurrect retired authority.
9. Unique local user/flight data remains preservable/exportable even when historical closure confidence degrades.
10. Do not claim product PASS until actual keys/trust roots, verifier topology, compromise semantics, long-horizon retention, Service Worker and managed-iPad behavior are tested.

## VALIDATION — 76-case compromise/migration campaign

1 planned key rotation; 2 continuity preserved; 3 planned trust-root rotation; 4 predecessor→successor binding verified; 5 algorithm migration; 6 old/new verifier overlap bounded; 7 canonicalization v1→v2; 8 original bytes/commitment preserved; 9 transform provenance recorded; 10 silent reserialization rejected; 11 old signature verifies under retired key; 12 historical-only result; 13 retired key requested for new closure; 14 reject; 15 key compromise detected; 16 revoke current authority; 17 detection time differs from suspected invalidity time; 18 preserve uncertainty; 19 pre-compromise independent anchor exists; 20 classify bounded historical claim; 21 no trustworthy timing evidence; 22 mark suspect rather than invent boundary; 23 post-compromise old-key signature; 24 reject current/historical legitimacy per policy; 25 re-sign suspect object with new key; 26 new attestation does not launder old legitimacy; 27 valid RFC3161-like trusted timestamp before revocation where architecture uses one; 28 verify binding/status policy; 29 untrusted local device timestamp; 30 do not use as compromise proof; 31 historical certificate expired; 32 distinguish expiry from historical verification policy; 33 CRL revocationDate later than invalidityDate; 34 use correct semantics; 35 old public key retained/private key destroyed; 36 historical verification remains possible where context permits; 37 old private key accidentally restored from backup; 38 quarantine/destroy and do not restore authority; 39 legacy verifier source archived but runtime missing; 40 recoverability failure surfaced; 41 legacy verifier executable but vulnerable parser; 42 isolate/quarantine; 43 client supplies legacy algorithm preference; 44 current server policy rejects downgrade; 45 old verifier returns PASS for current-policy-forbidden claim; 46 property-specific historical result only; 47 verifier implementation rotates without key rotation; 48 verifier generation recorded; 49 trust policy changes without algorithm change; 50 current acceptance follows policy generation; 51 evidence package omits canonicalization version; 52 incomplete/unverifiable; 53 evidence package omits trust generation; 54 no generic PASS; 55 old hash/algorithm no longer adequate for consequence; 56 downgrade confidence or rely on prior stronger anchor if proven; 57 migration occurs before retirement; 58 successor commitment binds predecessor evidence; 59 migration after suspected compromise; 60 do not infer old legitimacy; 61 backup restores old trust root; 62 monotonic current trust floor rejects resurrection; 63 stale Service Worker caches old verifier/policy; 64 reconnect obtains current trust before authority; 65 IndexedDB retains old closure and unique flight data; 66 preserve data while reclassifying proof; 67 Service Worker update interrupted mid-migration; 68 mixed generation detected; 69 offline queue signed/authorized under retired context; 70 historical intent preserved/current admission rechecked; 71 export/import across verifier generations; 72 preserve original context plus import provenance; 73 accessible UX distinguishes current/historical/suspect/unverifiable without color alone; 74 screen-reader wording avoids generic `verified`; 75 physical managed-iPad long-offline multi-generation migration; 76 remains OPEN until runtime evidence exists.

## CONTRADICTION / failure-mode analysis

### Re-signing theater
A new trusted key can sign a statement that old bytes were observed. It cannot prove a compromised old signer legitimately created them years earlier.

### Revocation-time theater
Administrative revocation processing is not necessarily the compromise start. Using it as an exact historical cutoff can launder suspect signatures.

### Compatibility-as-authority
Keeping an old verifier for archival evidence is useful; allowing old artifacts to select current acceptance policy turns compatibility into downgrade authority.

### Archive-without-executability
Source, certificates and algorithm identifiers can survive while the actual verifier/runtime/dependencies disappear. Long-horizon proof needs recoverable verification capability, not file accumulation alone.

### Timestamp theater
A local or self-asserted signing time is not independent temporal evidence. Even trusted timestamp systems require their own trust/status validation.

### PWA migration theater
A new Service Worker being active does not prove old IndexedDB data, verifier context, queued operations and trust state migrated atomically.

## OPEN

Production facts remain OPEN: actual closure/evidence signature scheme, key hierarchy/custody, trust roots, verifier topology, canonicalization, timestamp/anchor mechanism if any, compromise detection/invalidation semantics, algorithm transition policy, retention horizon, backup/PITR behavior, KMS/HSM, Service Worker integration, WebKit/managed-iPad behavior and legal/privacy requirements.

NIST SP 800-57 Part 1 Rev.6 and SP 800-131A Rev.3 remain draft in the current NIST publication index and are **CHANGE WATCH**. CSWP 39upd1 is the current final crypto-agility source checked for this study.

## Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-20: **W110 NON-DRAG REORDER PRODUCTION TRANSFER; Stage 3 PRACTICE / NOT PASSED**. No W110 runtime execution, independent-browser/native PASS, physical-device PASS, field Core Web Vitals, full WCAG conformance, screen-reader or human UX PASS is claimed. No production PWA crypto/migration UX PASS transfers.

Software Engineering remains a bounded implementation dependency. Web Manager does not select algorithms, KMS/HSM, signature containers, key hierarchy, timestamp service, canonical serialization or verifier deployment topology without product/runtime evidence.

## Checkpoint / next bottleneck

161 closes the generic closure-evidence compromise/migration/long-horizon-survivability model. The highest-value adjacent bottleneck is **closure-evidence destruction, legal/privacy deletion vs cryptographic lineage continuity, and proof-minimizing redaction**: determine how to satisfy deletion/minimization obligations without fabricating history, how to retain non-secret continuity commitments after permitted payload destruction, and how exports/backups/offline PWAs represent intentionally unavailable evidence without treating deletion as corruption or silently resurrecting deleted content.