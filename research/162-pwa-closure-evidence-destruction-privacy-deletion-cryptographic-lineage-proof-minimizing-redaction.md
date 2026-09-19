# 162 — PWA Closure-Evidence Destruction, Privacy Deletion, Cryptographic Lineage & Proof-Minimizing Redaction

Status: **PASS (generic) / PRODUCT + LEGAL + STORAGE + BACKUP + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 135 provenance compaction/export/import; 160 closure-evidence retention; 161 long-horizon verifier survivability; Track A browser/SW/IndexedDB/cache persistence; Track B truthful deletion/unavailability UX; Track C destructive deletion/restore validation; Track D telemetry minimization; legal/privacy specialist review for jurisdiction-specific obligations.

## Why this study exists

161 established how closure evidence can remain verifiable across key/trust/verifier change. The adjacent risk is the opposite lifecycle pressure: sensitive payloads may need to be minimized or intentionally destroyed while a non-fabricated historical lineage still needs to show that an event existed, was closed, later redacted, or became intentionally unavailable.

The objective is not to preserve every payload forever and not to make deletion invisible. It is to separate content availability from historical/provenance continuity without leaving a supposedly harmless commitment that still functions as a practical identifier or dictionary oracle.

Central rule:

> **Intentional deletion should destroy the data whose continued availability is no longer justified while preserving only the minimum non-secret lineage needed for the declared proof; deletion state must itself be provenance, and retained commitments must be assessed as potentially identifying data rather than assumed anonymous.**

## Five-track balance

- **A Platform/Browser — critical dependency supplier:** owns what SW caches, Cache Storage, IndexedDB, browser-managed storage, downloads/exports and offline queues can retain; browser deletion is not proof of server/backup/device-fleet deletion.
- **B UX/IA/Content — elevated consumer:** owns truthful distinctions among `AVAILABLE`, `REDACTED`, `INTENTIONALLY UNAVAILABLE`, `RETENTION HOLD`, `MISSING/UNKNOWN`, `CORRUPT` and `REVALIDATION REQUIRED` without exposing sensitive reason text.
- **C Performance/Accessibility/Quality — high dependency pressure:** owns destructive deletion, restore, stale-cache/export, offline-device and accessible-state validation.
- **D Search/Discovery/Analytics — constrained consumer:** must not recreate deleted content through analytics/search indexes, event payloads or diagnostic dimensions; aggregate telemetry can diagnose deletion propagation but cannot certify it.
- **E Architecture/Security/Operations — highest-risk owner:** owns retention/deletion state, cryptographic erasure boundary, backup/replica propagation, commitment privacy, anti-resurrection and proof-minimization governance.

Allocation remains E-heavy with A/C as critical dependencies. Product-specific legal deletion requirements are OPEN and must not be inferred from generic security/privacy research.

## SOURCE

### NIST SP 800-88 Rev.2 — current media-sanitization baseline

NIST SP 800-88 Rev.2 was published September 2025 and supersedes Rev.1. NIST defines sanitization as rendering access to target data on media infeasible for a given level of effort. Rev.2 explicitly includes cryptographic erase and emphasizes enterprise sanitization programs, validation and modern logical/cloud storage contexts.

Sources:
- https://csrc.nist.gov/pubs/sp/800/88/r2/final
- https://csrc.nist.gov/news/2025/guidelines-for-media-sanitization-rev-2

**TRANSFER VALIDATION:** application deletion and media sanitization are not identical. The useful transfer is that `delete command accepted` is not sufficient assurance; sanitization effectiveness and all relevant copies/key hierarchy matter. Cryptographic erase depends on correct key scope and sanitization, including derived/wrapped/unwrapped copies.

### NIST de-identification guidance — transformation does not eliminate re-identification risk by assertion

NIST IR 8053 and NIST's later de-identification guidance emphasize that de-identification reduces privacy risk but some de-identified data can be re-identified; organizations should evaluate disclosure risk rather than treating a transformation label as proof of anonymity.

Sources:
- https://csrc.nist.gov/pubs/ir/8053/final
- https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance

**TRANSFER VALIDATION:** a hash/commitment derived from deleted content is not automatically privacy-neutral. Low-entropy or guessable domains can permit dictionary confirmation; linkable stable commitments can themselves become identifiers.

### EDPB Guidelines 01/2025 — pseudonymised data can remain personal data

The EDPB's Guidelines 01/2025 on Pseudonymisation (public-consultation version, adopted 16 January 2025) state that pseudonymised data that can be linked back to an individual using additional information remains personal data. This is useful privacy evidence but is not a MintTap legal conclusion; jurisdiction/product applicability requires legal review.

Source: https://www.edpb.europa.eu/public-consultations/guidelines-012025-on-pseudonymisation_en

**CHANGE WATCH:** this cited version is consultation-stage guidance; monitor final status before treating it as final EDPB guidance.

## SYNTHESIS — deletion has several independent dimensions

Do not collapse deletion into one boolean. At minimum distinguish:
1. **logical availability** — may normal application/API paths retrieve the payload?
2. **authoritative retention state** — retained, scheduled, held, redacted, destroyed, or unknown;
3. **replica/cache/search/analytics propagation** — have derived operational copies converged?
4. **backup/recovery availability** — can older protected copies still be restored under policy?
5. **cryptographic recoverability** — do any relevant keys/wrapping/derived/unwrapped copies still make ciphertext recoverable?
6. **offline/exported copies** — user-controlled or managed-device copies may exist outside server deletion control;
7. **lineage/proof residue** — what minimum event metadata or commitment intentionally remains?

Persistent guards:
- `row deleted ≠ data destroyed`;
- `application delete succeeded ≠ backups sanitized`;
- `ciphertext retained + key destroyed ≠ cryptographic erase proven unless key scope/copies are validated`;
- `hash retained ≠ content anonymous`;
- `salted hash ≠ automatically non-identifying`;
- `payload unavailable ≠ event never existed`;
- `tombstone retained ≠ payload retained`;
- `tombstone present ≠ deletion propagated everywhere`;
- `offline copy exists ≠ server deletion failed` when that copy is outside the declared server-control scope;
- `offline copy exists ≠ safe to silently republish deleted server data`;
- `backup exists ≠ ordinary application may resurrect intentionally deleted data`;
- `INTENTIONALLY UNAVAILABLE ≠ CORRUPT ≠ NOT YET SYNCED`.

## Proof-minimizing deletion model

A consequence-bearing historical record may need to preserve that a closure/deletion transition occurred without retaining the sensitive payload. A minimal generic lineage can conceptually include:
- opaque record/effect lineage identifier where justified;
- predecessor lineage/head reference;
- deletion/redaction event generation;
- coarse reason/policy class, avoiding sensitive free text;
- effective/observed deletion state;
- verifier/trust generation needed to authenticate the transition;
- commitment only when it serves a declared proof and passes privacy/threat review;
- retention/hold metadata where necessary;
- successor lineage/head reference.

The exact schema is OPEN. Do not retain a digest merely because cryptographic provenance is desirable. Ask what claim the digest proves and whether that claim can be achieved with less linkable material.

### Commitment privacy

A plain unsalted hash can reveal deleted low-entropy content by trial enumeration. A salt may frustrate precomputation but does not make a small candidate space safe if the salt is available with the commitment. A secret-keyed commitment/HMAC can change the attack model but introduces key retention/custody and can itself become a correlation service. Randomized commitments can reduce linkability but complicate verification.

Therefore:
- classify the candidate payload entropy and attacker knowledge;
- avoid committing directly to predictable identifiers, statuses, dates or small enums where dictionary confirmation matters;
- avoid global stable commitments that create unnecessary cross-record linkability;
- separate proof keys from live authorization/signing authority;
- expire/destroy proof material when the declared proof horizon ends;
- treat commitment design as a product/security/privacy decision, not a generic recipe.

`cryptographically strong hash ≠ privacy-safe commitment`.

## Deletion as provenance, not history rewriting

Do not erase an event from the lineage and reconnect predecessor directly to successor as though the deleted content never existed. Instead, where historical continuity is justified, record a new authenticated transition that states the prior payload is intentionally unavailable under the current retention state.

The deletion transition must not contain enough copied sensitive fields to defeat deletion. Historical verification should answer bounded questions such as:
- did an authenticated lineage transition occur?
- is the payload intentionally unavailable rather than silently missing?
- which later lineage supersedes it?

It need not answer `what exactly was the deleted sensitive payload?` unless an applicable retained-evidence purpose explicitly requires that content.

## Backup/PITR and anti-resurrection

Backups complicate deletion because availability/recovery objectives and deletion obligations can conflict. Generic governance:
- record deletion intent/current retention state outside any single rollback-prone application row;
- after PITR/restore, reconcile restored data against the current deletion/retention floor before ordinary serving;
- prevent a pre-deletion backup from making intentionally unavailable content current again merely because the restored snapshot is internally consistent;
- define whether protected backup copies age out, are selectively purged, or are inaccessible except controlled disaster recovery according to actual legal/product policy;
- test that restore workflows re-apply current deletion state before reopening normal access.

Exact backup deletion obligations and provider capabilities remain OPEN.

## Cryptographic erase boundary

Cryptographic erase can be useful when data is encrypted under sufficiently scoped keys and destroying the relevant key material renders target data infeasible to recover. It is not a magic application-level delete primitive.

Before relying on CE, validate:
- target data/key scope;
- shared-key blast radius;
- wrapped/derived keys and hierarchy;
- cached/unwrapped key copies;
- backup/escrow/recovery key copies;
- provider implementation/assurance;
- plaintext replicas, exports, logs, search indexes and analytics copies outside the encrypted target.

If one key protects many records, destroying it to delete one record can violate availability; if the key is retained for other records, CE did not delete the target ciphertext. Product key topology remains OPEN.

## PWA / Service Worker / managed-iPad application

A LogMate-like company iPad can remain offline across a server-side deletion or redaction event. Generic safe behavior:
- preserve unique local flight/user data unless product/legal policy establishes authority to destroy it;
- mark server deletion state as unknown while offline rather than inventing convergence;
- on reconnect, obtain current retention/authority state independently of cached UI/SW state;
- never let a stale SW or offline queue silently republish server-intentionally-deleted content;
- distinguish local-only user data from a stale replica of remotely deleted data;
- require explicit reconciliation when the device contains content whose server lineage is now `INTENTIONALLY UNAVAILABLE`;
- preserve non-sensitive lineage needed to explain the conflict without exposing deleted payload in logs/UI;
- treat downloaded/exported user-controlled copies as a separate control domain.

Actual WebKit storage eviction, managed-iPad/MDM deletion capability, file/export custody and product data authority remain OPEN.

## UX boundary

Track B should expose meaningful availability states without implying legal conclusions:
- **AVAILABLE** — content is currently retrievable under current authority;
- **INTENTIONALLY UNAVAILABLE** — current lineage records deliberate removal/unavailability;
- **REDACTED** — only a permitted subset remains;
- **RETENTION HOLD** — destruction is currently blocked by an applicable governed hold (product/legal semantics OPEN);
- **MISSING / SYNC UNKNOWN** — absence is not yet explained by authoritative deletion evidence;
- **CORRUPT / UNVERIFIABLE** — expected evidence cannot be validated;
- **LOCAL COPY / REMOTE STATUS CHANGED** — offline/local content exists but remote lineage changed.

Do not collapse these to `Deleted` if the system cannot prove the claimed scope. Do not expose sensitive deletion reasons unnecessarily. Accessibility/human validation remains OPEN.

## Analytics/search/log boundary

Deletion propagation must include derived systems proportionally to their role. Search indexes, analytics events, support exports and security logs are separate stores with separate purposes; deleting primary payload does not automatically remove them. Conversely, security/audit retention does not justify copying full sensitive payload into logs.

Track D can measure observed propagation and stale-generation counts, but telemetry must not recreate the deleted payload or become a stable cross-context identifier without a justified purpose.

## MINTTAP DECISION — minimal generic model

1. Model content availability, retention state, replica propagation, backup recoverability, cryptographic recoverability, offline/export copies and lineage residue separately.
2. Make intentional deletion/redaction a versioned provenance transition; do not rewrite history to pretend the event never existed.
3. Retain only the minimum lineage needed for a declared proof purpose; commitments are optional, not mandatory.
4. Treat hashes/commitments as potentially identifying/linkable; assess dictionary and correlation attacks before retention.
5. Do not use application deletion success as evidence of sanitization or backup/offline-fleet convergence.
6. Reconcile PITR/backup restores against the current deletion/retention floor before serving restored content.
7. Use cryptographic erase only when key scope, hierarchy, copies and provider behavior are validated; CE does not cover plaintext/derived copies elsewhere.
8. Long-offline PWA/device data must not silently resurrect intentionally unavailable server content, but unique local data should not be destroyed absent verified product/legal authority.
9. UX must distinguish intentional unavailability from corruption/missing sync and disclose only the minimum reason necessary.
10. Product/legal/provider/device PASS remains OPEN until actual retention obligations, storage topology, backups, keys, SW/device behavior and deletion propagation are tested.

## VALIDATION — 80-case destructive deletion/redaction campaign

1 primary row delete; 2 API no longer returns payload; 3 stale replica still has payload; 4 detect incomplete propagation; 5 cache still has payload; 6 invalidate/reconcile; 7 search index still has content; 8 derived deletion path; 9 analytics event contains full payload; 10 privacy defect; 11 security log contains bearer/sensitive payload; 12 minimize/redact; 13 tombstone retained without payload; 14 lineage remains continuous; 15 tombstone accidentally copies sensitive field; 16 reject; 17 plain hash of low-entropy value retained; 18 dictionary recovery succeeds in test; 19 classify unsafe; 20 salted low-entropy hash; 21 online guessing still feasible; 22 do not claim anonymity; 23 keyed commitment used; 24 key custody/purpose tested; 25 proof key compromised; 26 reassess privacy/linkability; 27 randomized commitment; 28 verifier relation preserved where required; 29 deletion event omitted from exported history; 30 detect continuity gap; 31 export represents INTENTIONALLY UNAVAILABLE; 32 no deleted payload included; 33 pre-deletion backup restored; 34 current deletion floor reapplied; 35 restore attempts to serve deleted payload; 36 block before normal traffic; 37 backup copy ages out under declared policy; 38 verify destruction/expiry evidence; 39 backup cannot selectively purge; 40 limitation documented rather than hidden; 41 CE with per-record key; 42 destroy all relevant key copies; 43 wrapped key survives; 44 CE not proven; 45 unwrapped key in volatile/runtime store; 46 sanitize/reset path tested; 47 shared key protects many records; 48 reject per-record CE claim; 49 plaintext search projection survives CE; 50 deletion incomplete; 51 provider reports key destroyed; 52 independent/contractual assurance requirement remains scoped; 53 user export predates deletion; 54 classify outside server-control scope; 55 import old export after deletion; 56 do not silently resurrect current remote state; 57 stale SW serves deleted payload; 58 reconnect/current state invalidates authority; 59 IndexedDB retains stale remote replica; 60 reconcile before upload; 61 IndexedDB holds unique unsynced flight data; 62 preserve pending authority decision; 63 device offline during deletion; 64 show remote status unknown; 65 reconnect receives INTENTIONALLY UNAVAILABLE marker; 66 distinguish from corruption; 67 local device clock wrong; 68 do not infer deletion ordering from it; 69 SW update clears cache but not IndexedDB; 70 detect mixed storage state; 71 app reinstall clears browser storage; 72 do not call this server deletion proof; 73 retention hold active; 74 deletion executor blocked with auditable state; 75 hold released; 76 new deletion generation required; 77 screen reader announces redacted/unavailable without generic error; 78 color-independent differentiation; 79 physical managed-iPad multi-generation delete/reconnect; 80 remains OPEN until runtime evidence exists.

## CONTRADICTION / failure-mode analysis

### Hash-as-anonymization theater
A strong digest can still confirm guesses in a small domain and can provide stable linkability. Cryptographic collision resistance does not imply privacy anonymity.

### Tombstone bloat
A deletion marker that copies the old payload to make audit easy defeats minimization. Preserve state/provenance, not a shadow payload.

### Backup time machine
A pre-deletion backup can be valid disaster-recovery data and simultaneously unsafe to expose as current application state. Restore must reconcile current deletion floors.

### Cryptographic-erase theater
Destroying one named key is insufficient when wrapped, derived, cached or escrow copies survive, or when plaintext projections exist elsewhere.

### Offline-device false convergence
The server cannot honestly claim every device/export is erased merely because authoritative server stores converged. Scope the claim to controlled domains and separately govern reconnect/resurrection.

## OPEN / DEPENDENCY

- Actual MintTap/LogMate retention/deletion/legal obligations: OPEN; requires product/legal evidence.
- Actual data authority for local flight records and whether server may order device-side destruction: OPEN.
- Actual DB/replica/search/analytics/log/backup/PITR topology: OPEN.
- Actual encryption/key hierarchy, CE capability, KMS/HSM/provider assurance: OPEN.
- Actual Service Worker/IndexedDB/cache/export schema and managed-iPad/MDM behavior: OPEN.
- Actual deletion propagation SLO, retention holds and backup expiry policy: OPEN.
- Design Studio human/accessibility validation for deletion/reconciliation states: OPEN.
- Software Engineering implementation/schema/runtime validation: OPEN.

## CHANGE WATCH

- NIST SP 800-88 Rev.2 is current final baseline as of 2026-09-20; monitor NIST FAQ/errata and provider-specific CE assurance changes.
- EDPB Guidelines 01/2025 source used here is consultation-stage; monitor for final adoption/version changes.
- Browser/WebKit storage, eviction and managed-device capabilities remain platform-sensitive and require current device validation.
- Applicable privacy/deletion law and platform/provider policy are jurisdiction/product-specific and must be refreshed when product facts exist.

## Gate decision

**PASS (generic).** The Web Manager can now distinguish payload destruction from provenance continuity, reason about commitment privacy, backup/PITR anti-resurrection, cryptographic erase boundaries and long-offline PWA deletion conflicts without inventing product/legal facts. Production certification remains OPEN.

## Next highest-value adjacent work

**PWA deletion propagation proof, backup expiry attestations & offline-fleet resurrection resistance.** The next bottleneck is proving bounded deletion convergence across replicas/search/analytics/backups and reconnecting offline clients without turning deletion telemetry or attestation into a privacy-rich global inventory. Study should define evidence scopes, negative/positive proof limits, restore-time deletion floors, stale-export/import handling, and what can truthfully be claimed when unmanaged copies are unobservable.