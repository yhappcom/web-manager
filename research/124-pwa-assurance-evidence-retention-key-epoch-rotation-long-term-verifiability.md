# 124 — PWA Assurance Evidence Retention, Key/Epoch Rotation & Long-Term Verifiability

Status: **PASS (generic) / PRODUCT RETENTION + KEY/ORACLE + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 114–123 provenance/incident/assurance chain; Track A PWA generation/state mechanics; Track C evidence-format/verification regression; Track D observation-window/retention interpretation; Software Engineering for exact key/evidence implementation.

## Purpose

123 established that assurance evidence must be authentic, fresh, live, sufficiently covered and continuity-aware. A further failure appears over longer periods: evidence that was valid when created can become unverifiable or misleading after key/certificate rotation, revocation, algorithm retirement, evidence pruning, format migration, oracle epoch reset, or loss of verification context.

This study separates **historical verifiability** from **current authorization** and deliberately avoids promoting ordinary PWA monitoring into a legal non-repudiation or long-term archival-signature system without a demonstrated requirement.

## 1. Five-track balance

- **A Platform/Browser:** supplies Service Worker/client/release/trust generation semantics. Historical worker evidence does not make an old worker current.
- **B UX/IA/Content:** consumes historical/current/unknown evidence states; archived PASS must not be rendered as a current security state.
- **C Quality:** owns verification regression across key/epoch/format migration, pruning and retained fixtures.
- **D Search/Analytics:** owns retention-window and denominator semantics; absence after expiry is not evidence that an event never occurred.
- **E Architecture/Security/Operations:** highest-risk owner; owns evidence lifecycle, verification context, rotation/compromise semantics and proportional archival design.

E remains the bottleneck. C has high dependency pressure because a retention policy without a future verification drill is only a storage claim.

## 2. SOURCE — key management is lifecycle management

NIST SP 800-57 Part 1 Rev. 5 provides general key-management guidance covering cryptographic keying material, protection requirements, key-management functions, backup/archive, compromise and trust anchors.

Source checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

**SYNTHESIS:** assurance evidence can outlive the key's active signing/production period. Rotation should stop or change active authority without necessarily destroying the verification material required to interpret historical evidence.

Guards:
- `signing key retired ≠ historical evidence automatically unverifiable`;
- `verification material retained ≠ signing authority retained`;
- `key rotated ≠ old evidence becomes current under the new key`.

## 3. SOURCE — certificate validity and historical proof are different questions

RFC 5280 defines certificate validity intervals and PKIX path validation. RFC 3161 shows a distinct historical pattern: a trusted timestamp can establish that signed material existed at a time that falls within the signer's certificate validity period.

Sources:
- https://www.rfc-editor.org/rfc/rfc5280.html
- https://www.rfc-editor.org/rfc/rfc3161.html

**SYNTHESIS:** verifying an old evidence object years later is not always equivalent to asking whether its certificate is valid *now*. The claim may require reconstructing the relevant historical validation context. Exact PKI policy is product-specific and remains OPEN.

Guards:
- `certificate expired now ≠ signature necessarily invalid when produced`;
- `certificate once valid ≠ historical claim automatically trustworthy forever`;
- `historical signature valid ≠ producer currently authorized`.

## 4. SOURCE — long-term evidence needs verification context and renewal when cryptography ages

RFC 4998 Evidence Record Syntax addresses long-term proof where signatures, hashes, certificates or timestamp mechanisms can weaken or expire. It preserves verification data such as certificates/revocation information and defines renewal chains so evidence can be re-protected before older mechanisms become inadequate.

Source:
- https://www.rfc-editor.org/rfc/rfc4998.html

**TRANSFER VALIDATION:** RFC 4998 targets long-term non-repudiation/existence evidence. MintTap/LogMate ordinary operational assurance does **not** thereby require ERS, Merkle archival, TSA renewal or non-repudiation infrastructure. The transferable principle is narrower: if a historical claim must remain verifiable beyond the life of its original cryptographic mechanism, preserve enough validation context and renew protection before the old mechanism becomes inadequate.

Guards:
- `long retention ≠ long-term cryptographic verifiability`;
- `historical verifiability required ≠ RFC 4998 implementation required`;
- `cryptographic renewal ≠ re-authorizing historical producer`.

## 5. SOURCE — retention means retrievable and interpretable, not merely stored

NIST SP 800-53 Rev. 5 AU-11 requires audit-record retention according to organizational retention needs; its long-term retrieval enhancement explicitly addresses access/readability over years, including conversion to newer formats, retaining reading capability and retaining documentation needed to interpret records. AU-9 addresses protection of audit information.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** `blob still exists` is weaker than `evidence remains retrievable, parseable, interpretable and verifiable`.

Guards:
- `retained bytes ≠ retrievable evidence`;
- `retrievable evidence ≠ interpretable evidence`;
- `interpretable evidence ≠ cryptographically verifiable evidence`.

## 6. Evidence lifecycle model

For each assurance class distinguish:
1. **production** — oracle creates evidence under an active producer identity/key/epoch;
2. **ingest** — protected sink records evidence, receipt/order and provenance;
3. **active verification** — current operations use it within a defined freshness window;
4. **historical retention** — evidence is no longer current authorization input but remains useful for audit, incident reconstruction, trend/decision provenance or required records;
5. **migration/renewal** — format, storage or cryptographic protection changes while preserving provenance;
6. **expiry/disposition** — evidence and associated verification context are removed according to policy, subject to holds/requirements;
7. **verification drill** — retained evidence is periodically or event-triggeredly proved readable and interpretable under the intended future verifier.

A lifecycle state transition must not silently promote historical evidence back into active authorization.

## 7. Key rotation vs key compromise

Routine rotation and compromise are not equivalent.

### Routine rotation
- old producer key stops creating new evidence at an identified boundary;
- new evidence binds to a new key/epoch;
- historical verification material may remain available as required;
- verifier rejects use of old epoch as current evidence after the cutover.

### Suspected/confirmed compromise
- historical evidence signed before discovery is not automatically known forged and not automatically known trustworthy;
- affected time/sequence scope must be investigated;
- independent sink receipt/order, challenge history, timestamps and other witnesses may narrow what remains supportable;
- evidence created after likely compromise under that key may need quarantine or lower confidence;
- rotating the key prevents future use but does not retroactively repair uncertain history.

Guards:
- `key compromised now ≠ every historical record proven forged`;
- `key compromised now ≠ every historical record remains trustworthy`;
- `new key deployed ≠ uncertain old interval repaired`.

## 8. Epoch semantics

An **epoch** is a bounded operational identity domain, not merely a counter. It can bind producer identity, key, policy/config generation, evidence schema and sequence namespace.

A reset/redeploy must not silently restart sequence `1` under an indistinguishable epoch. A new epoch should have an explicit predecessor/transition record when continuity matters.

Useful generic fields:
- oracle/control identity;
- epoch ID;
- key/certificate or verification-key identifier;
- policy/configuration/release identity;
- schema/version;
- sequence range;
- activation/retirement event;
- predecessor epoch;
- reason: routine rotation, migration, incident recovery, rollback, replacement;
- verification-context locator/digest.

Guards:
- `sequence monotonic within epoch ≠ continuity across epoch transition`;
- `epoch reset authorized ≠ previous gap erased`;
- `same key ≠ same policy epoch`;
- `same epoch label ≠ same cryptographic authority unless bound`.

## 9. Historical authenticity vs current authorization

Historical evidence answers questions such as:
- what did oracle O report about control C under generation G at time/order T?
- was that report received by protected sink S before a later incident?
- can its signature/MAC/provenance still be verified under the historical context?

Current authorization asks a different question:
- may this client/key/worker/API generation perform this operation **now**?

No historical PASS, however well preserved, grants current remote mutation authority.

Persistent guard: `historically authentic ≠ currently authorized`.

## 10. Retention classes should follow claim value

Do not retain all evidence forever. A generic tiering model:

- **Ephemeral operational health:** enough history for current freshness/gap diagnosis; short retention can be appropriate.
- **Security-control assurance:** retain enough to investigate control drift, exceptions, incidents and corrective-action recurrence over the risk horizon.
- **Incident/legal/regulatory evidence:** retention and custody follow applicable organizational/legal requirements; specialist/legal ownership is required.
- **Irreplaceable domain-data provenance:** may need retention aligned to the domain record's lifecycle, but privacy/data-minimization and recovery design remain separate decisions.

**MINTTAP DIRECTION:** define retention by claim/use, not by storage cheapness. Exact periods are OPEN; do not invent them.

## 11. Verification-context bundle

Where historical cryptographic verification matters, preserve enough context to reconstruct the intended claim, proportionate to risk:
- original evidence bytes or canonical representation;
- schema/version and canonicalization rules;
- producer/oracle identity and epoch;
- verification public key/certificate or resolvable immutable reference;
- relevant chain/trust-anchor/policy information where applicable;
- revocation/status/timestamp evidence where the chosen historical-validation model requires it;
- algorithm identifiers and parameters;
- protected sink receipt/order/provenance;
- control/configuration/release identity;
- migration/renewal records;
- parser/verifier specification or executable test fixture sufficient to detect semantic drift.

Private signing keys are not required merely to verify historical signatures and should not be retained just for verification.

Guard: `historical verification need ≠ retain historical signing capability`.

## 12. Format migration without semantic laundering

Long retention can outlive storage formats, schemas and tooling. Migration must preserve:
- immutable source or cryptographically bound source representation where required;
- old→new transformation identity/version;
- field mapping and dropped/derived fields;
- original evidence digest;
- migrated evidence digest;
- verification result before/after migration;
- unsupported semantics explicitly marked rather than guessed.

A successful parser conversion is not proof that evidentiary meaning was preserved.

Guards:
- `format migrated ≠ semantics preserved`;
- `schema readable ≠ historical policy meaning reconstructed`;
- `new signature on migrated record ≠ original producer re-signed new semantics`.

## 13. Pruning and deletion semantics

Evidence retention must distinguish:
- expected expiry under policy;
- storage loss/corruption;
- unauthorized deletion;
- legal/incident hold;
- privacy-driven deletion/minimization;
- cryptographic context loss.

After expected expiry, absence should be represented as `NOT RETAINED BY POLICY`, not `NO EVENT`. If evidence expected to exist is missing, assurance becomes `GAP/UNKNOWN` for the historical claim.

Guards:
- `evidence absent after retention expiry ≠ event never occurred`;
- `evidence deleted by policy ≠ evidence disproved`;
- `expected retained evidence missing ≠ historical assurance PASS`.

## 14. Append-only/transparency transfer boundary

RFC 9162 Certificate Transparency v2 shows a useful pattern: append-only Merkle logs plus consistency/inclusion proofs allow monitors to detect inconsistent views or missing promised entries. This is a specialized certificate ecosystem, not a prescription for MintTap telemetry.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** for very high-impact assurance where deletion/fork detection matters, append/consistency evidence can reduce trust in one mutable database. But an append-only structure does not make a lying producer truthful, does not create freshness, and does not justify collecting sensitive user data.

Guards:
- `append-only log ≠ truthful producer`;
- `inclusion proven ≠ event semantics correct`;
- `tamper-evident retention useful ≠ public transparency log required`.

## 15. PWA / Service Worker application

Historical evidence may record:
- origin served worker generation W12;
- device D fetched/activated W12;
- W12 controlled client C;
- local schema/trust generation was S8/T4;
- remote API admitted generation A7;
- outbox reconciliation result R.

After W13/A8/T5 is current, retained W12/A7/T4 evidence remains historical. It must not make a returning offline iPad current. Conversely, retiring W12's signing/attestation key must not force deletion of historical incident evidence if that evidence still has a justified retention purpose.

Guards:
- `old worker evidence verifiable ≠ old worker supported`;
- `old API evidence retained ≠ old API generation re-enabled`;
- `client history preserved ≠ client re-entry authorized`.

## 16. EFB / LogMate-like operating judgment

For a company iPad that can remain offline for long periods:
- local domain records can outlive multiple assurance/key epochs;
- record provenance should preserve relevant historical generation identities without requiring the device to possess retired signing authority;
- reconnect evaluates current server-side trust/API/reconciliation gates, not historical PASS age alone;
- compromise-era provenance uncertainty remains explicit even after key rotation;
- backup/export/restore retention is a separate domain-data lifecycle from operational assurance-log retention;
- exact managed-iPad/WebKit/MDM, key storage, export and legal record requirements remain OPEN.

This keeps offline usefulness compatible with strict re-entry while avoiding permanent retention of dangerous authority.

## 17. Track C adversarial validation campaign

Future product evidence should include at least:
1. verify evidence before routine key rotation;
2. verify same historical evidence after rotation;
3. reject old key for new/current evidence;
4. certificate expires after evidence creation;
5. historical verification with preserved required context;
6. missing certificate/verification key;
7. revoked/compromised key with evidence before suspected compromise;
8. evidence during uncertain compromise interval;
9. evidence after compromise but before rotation;
10. new epoch with explicit predecessor;
11. unauthorized epoch reset;
12. sequence restart under same epoch rejected;
13. rollback restores old key/config but not old authorization;
14. schema migration preserves original digest;
15. schema migration drops a security-relevant field;
16. parser unavailable years later;
17. retained fixture catches parser semantic drift;
18. evidence pruned exactly by policy;
19. evidence unexpectedly missing before expiry;
20. legal/incident hold prevents ordinary pruning where applicable;
21. privacy deletion does not leave false `NO EVENT` semantics;
22. old PASS displayed only as historical;
23. current authorization rejects historical PASS;
24. Service Worker W12 evidence retained while W13 required;
25. long-offline client returns across multiple epochs;
26. remote API generation retired while local read/export remains possible;
27. compromise-era outbox remains quarantined after new login/key;
28. verification context itself corrupted;
29. independent sink and producer retention disagree;
30. storage migration retains provenance/order;
31. append-only proof detects fork/deletion where implemented;
32. cryptographic algorithm retirement triggers planned migration/renewal where required;
33. verifier distinguishes `UNVERIFIABLE` from `INVALID`;
34. historical evidence access respects privacy/least privilege;
35. restoration drill reconstructs claim without original producer service.

## 18. Cross-repository transfer

### Design Studio
Latest canonical Web status is W076, Stage 3 PRACTICE / NOT PASSED. W076 strengthens scenario-level browser evidence provenance and explicitly prevents source/widget/build evidence from being promoted to browser/cross-browser PASS. Transfer: provenance-bearing evidence should retain enough environment/scenario identity to remain interpretable. It is not security-retention proof.

### Software Engineering
Implementation-level key rotation, schema migration, immutable evidence representation and verifier compatibility belong with Software Engineering once an actual architecture exists. Existing bounded engineering evidence must not be promoted to PWA runtime proof.

### Marketing
No material canonical Marketing evidence changes this security/retention boundary; no duplication is warranted.

## 19. Operational judgment matrix

For each retained assurance class record:
- claim/use and consequence;
- active freshness window;
- historical retention purpose;
- owner/authorized readers;
- retention/disposition trigger;
- hold requirements if any;
- evidence format/schema;
- producer key/epoch identity;
- historical verification context required;
- compromise/revocation interpretation rule;
- migration/renewal trigger;
- verification drill cadence/event trigger;
- privacy/minimization constraints;
- failure state when evidence/context is unavailable;
- explicit statement that historical evidence does not grant current authorization.

## 20. PASS gate

Generic PASS requires ability to:
- separate historical verifiability from current authorization;
- explain routine rotation vs compromise effects on retained evidence;
- preserve verification context without retaining obsolete signing authority;
- distinguish retention, readability, interpretability and cryptographic verifiability;
- govern epoch transition, sequence continuity and format migration;
- represent expected pruning differently from unexplained loss;
- understand long-term timestamp/renewal and append-only techniques without over-prescribing them;
- apply the model to Service Worker/client/API generations and long-offline EFB re-entry;
- keep exact product retention periods, PKI/key architecture, managed-iPad behavior and legal requirements OPEN.

**Assessment: PASS (generic).**

## Persistent guards added by 124

- `signing key retired ≠ historical evidence automatically unverifiable`;
- `verification material retained ≠ signing authority retained`;
- `key rotated ≠ old evidence becomes current under the new key`;
- `certificate expired now ≠ signature necessarily invalid when produced`;
- `historical signature valid ≠ producer currently authorized`;
- `long retention ≠ long-term cryptographic verifiability`;
- `retained bytes ≠ retrievable evidence`;
- `retrievable evidence ≠ interpretable evidence`;
- `key compromised now ≠ every historical record proven forged`;
- `key compromised now ≠ every historical record remains trustworthy`;
- `new key deployed ≠ uncertain old interval repaired`;
- `sequence monotonic within epoch ≠ continuity across epoch transition`;
- `historical verification need ≠ retain historical signing capability`;
- `format migrated ≠ semantics preserved`;
- `evidence absent after retention expiry ≠ event never occurred`;
- `expected retained evidence missing ≠ historical assurance PASS`;
- `append-only log ≠ truthful producer`;
- `old worker evidence verifiable ≠ old worker supported`;
- `old API evidence retained ≠ old API generation re-enabled`;
- `client history preserved ≠ client re-entry authorized`.

## OPEN / CHANGE WATCH

**OPEN:** actual MintTap/LogMate evidence classes and retention periods; legal/regulatory/safety record requirements; PKI/signing/MAC architecture; oracle keys and custody; certificate/revocation/timestamp model; protected evidence sink; schema/canonicalization; key compromise history; epoch authority; archival format; deletion/hold policy; privacy classification; managed-iPad/WebKit/MDM behavior; exact backup/export provenance.

**CHANGE WATCH:** NIST cryptographic/key-management revisions; algorithm-transition guidance; browser/WebKit storage and managed-device behavior; applicable record-retention/privacy law; standards used by any future chosen signing/timestamp/archive architecture.

## Next high-value target

The adjacent bottleneck is **assurance evidence recovery after verifier/context loss**: if verification keys, trust anchors, schema interpreters, sink indexes or epoch-transition records are lost/corrupted, determine which historical claims can be reconstructed from independent copies and which must become `UNVERIFIABLE/UNKNOWN`, without fabricating trust through re-signing or migration.