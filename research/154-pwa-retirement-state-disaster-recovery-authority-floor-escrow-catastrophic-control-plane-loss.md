# 154 — PWA Retirement-State Disaster Recovery, Authority-Floor Escrow & Catastrophic Control-Plane Loss

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + CRYPTO/KEY + DISASTER-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 137 crypto/verifier lifecycle; 138 compromise recovery; 153 retirement proof/anti-resurrection; Track A runtime/SW/storage generations; Track B truthful recovery UX; Track C destructive restore validation; Track D diagnostics only.

## Why this study exists

153 makes predecessor retirement depend on a trustworthy current authority floor. That creates a harder failure mode: the primary policy/authority control plane, its replicas, or its current retirement-floor records can be catastrophically lost together. A normal backup may restore business data while being older than one or more revocations/retirements. Blindly treating the newest surviving backup as current authority can resurrect a generation that was intentionally retired.

The objective is therefore not merely `restore the database`. It is to recover enough independently protected security state to establish a **safe lower bound on accepted authority**, then reconstitute current policy deliberately without turning the recovery copy into a second ordinary authorization oracle.

## SOURCE

### NIST SP 800-34 Rev. 1 — contingency recovery uses alternate storage and must be tested
NIST contingency guidance treats recovery as coordinated plans/procedures/technical measures and discusses alternate/offsite storage. Backup methods should reflect availability and integrity requirements, and backup media should be tested for successful retrieval. This supports separating the primary failure domain from recovery material and validating actual restore capability.

Sources:
- https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf

### NIST SP 800-53 family — recovery is reconstitution to a known state, not mere process restart
CP-10 frames recovery/reconstitution as returning a system to a known state after disruption, compromise or failure and includes re-establishing monitoring/authorization activities. Transfer lesson: availability alone is insufficient if recovered authority state is unknown or stale.

Source family:
- https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page

### NIST SP 800-57 Part 1 Rev. 5 — key recovery is deliberate lifecycle functionality
NIST defines key recovery as mechanisms/processes that allow authorized entities to retrieve or reconstruct keys/key information from backup/archive. Rev. 5 discusses backup/archive recovery and split knowledge. It also distinguishes key types: private signature keys generally should not be archived, while recoverability decisions depend on key purpose and consequence.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/key_recovery
- https://csrc.nist.gov/glossary/term/split_knowledge

### NIST SP 800-57 Rev. 6 is draft, not current normative baseline
Revision 6 Initial Public Draft was published 2025-12-05 and its comment period is closed; Rev. 5 remains the final publication used here. Rev. 6 is CHANGE WATCH only.

Source:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

### OWASP Key Management — recoverability and escrow depend on key role
OWASP recommends secure backup for keys required to recover long-term encrypted data and cautions against escrow of digital-signature keys. Transfer lesson: a recovery design must distinguish data-decryption continuity from authority/signing continuity rather than escrow every secret indiscriminately.

Source:
- https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

## SYNTHESIS — three different things must survive disaster

Catastrophic recovery should distinguish at least:

1. **DATA RECOVERY MATERIAL** — business/local records, backups, exports, encrypted payloads.
2. **AUTHORITY-FLOOR RECOVERY MATERIAL** — the minimum authenticated facts needed to prevent predecessor policy/trust/revocation resurrection.
3. **LIVE AUTHORIZATION MATERIAL** — current online policy evaluator state, signing/authorization credentials, sessions and mutable operational controls.

They are not interchangeable.

Persistent guards:
- `backup available ≠ authority floor recoverable`;
- `authority floor recoverable ≠ live authorization restored`;
- `recovery package authentic ≠ recovery package current`;
- `latest surviving package ≠ latest legitimate authority state`;
- `escrow readable ≠ escrow may authorize production`;
- `data decryption key recoverable ≠ signing/authorization key should be escrowed`;
- `disaster declared ≠ every recovery control bypassed`;
- `primary lost ≠ predecessor generation active`;
- `offline client carries old policy ≠ client is recovery oracle`;
- `availability restored ≠ known-safe authority restored`.

## Authority-floor escrow: what it is and what it is not

`Escrow` in this study is a semantic term for independently protected recovery evidence. It does not require a particular vendor, HSM, database, secret-sharing scheme or human process.

A minimum authority-floor recovery package may need to bind, depending on the product:
- system/product/environment identity;
- authority/policy/trust generation namespace;
- minimum accepted generation or equivalent retirement/revocation floor;
- critical revocation/retirement facts not safely derivable from an older backup;
- package sequence/checkpoint identifier;
- creation and effective authority epochs;
- authenticated predecessor/successor lineage reference;
- cryptographic algorithm/key/verifier identifiers needed to verify the package;
- custody/provenance and recovery-policy version;
- expiry/supersession semantics where applicable;
- enough integrity/authenticity evidence to distinguish legitimate recovery state from injected rollback material.

The package should contain **minimum sufficient anti-resurrection state**, not a second full mutable production policy database by default.

## Preventing escrow from becoming a second live authorization oracle

A recovery copy becomes dangerous if normal request paths can consult it as an alternate policy source whenever the primary denies or is unavailable. That creates downgrade and split-brain authority.

Generic separation rule:
- ordinary production evaluators do not fall back to escrow;
- escrow is not a client-selectable policy generation;
- recovery access is a distinct, audited, bounded procedure;
- recovered floor establishes constraints for reconstitution; it does not itself issue arbitrary end-user permits;
- production resumes consequence-bearing mutation only after a new/current authoritative control plane is established under those constraints;
- any temporary recovery capability is explicitly retired after reconstitution.

`primary DENY + escrow older PERMIT` must never mean PERMIT.

## Freshness, rollback and the missing-latest-package problem

An authentic old package can still be unsafe. Catastrophic loss may destroy the newest floor package while leaving an earlier authentic package. Therefore signature/MAC validity alone cannot establish freshness.

Useful recovery states:
- `FLOOR-RECOVERED-CURRENT-WITHIN-DECLARED-EVIDENCE`;
- `FLOOR-RECOVERED-BUT-FRESHNESS-BOUNDED`;
- `RECOVERY-PACKAGE-AUTHENTIC-BUT-POSSIBLY-STALE`;
- `FLOOR-CONTRADICTED`;
- `FLOOR-UNKNOWN`.

If currentness cannot be established, the safe generic action for consequence-bearing remote mutation is not to guess a lower floor. Preserve/recover data, expose degraded/manual recovery, and require stronger reconciliation/authorization before restoring mutation authority.

### Independent anchors and witness evidence

Freshness may be strengthened by independently retained checkpoint/sequence evidence, external custody records, provider-native disable/revocation state, offline protected copies, or other authenticated witnesses. No single mechanism is mandated. The independence claim must be tested: two copies controlled by the same identity/admin/provider failure domain are not automatically independent.

## Key and trust material: do not escrow indiscriminately

NIST key-management guidance makes key recoverability purpose-dependent. OWASP similarly distinguishes encryption-key recovery from signing-key escrow. Generic implications:
- long-term data-decryption keys may need secure recovery when loss would make irreplaceable data unreadable;
- historical verification material may need long retention without retaining historical private signing capability;
- current signing/authorization private keys should not be copied merely because disaster recovery is desired;
- when a lost key may have been compromised, recovery and replacement are distinct concerns;
- split knowledge/multi-party custody can reduce single-custodian exposure for suitable recovery material, but it does not by itself prove package freshness or legitimate recovery authority.

Exact HSM/KMS, quorum, share count and ceremony remain implementation-specific.

## Catastrophic reconstitution sequence

A generic safe sequence is:

1. **Declare/identify control-plane loss** and freeze consequence-bearing authority whose current state cannot be established.
2. **Preserve surviving evidence** before destructive restore or key rotation.
3. **Recover business/local data independently** where possible; do not infer authority from data-backup timestamps.
4. **Recover and authenticate authority-floor material** from the strongest surviving independent sources.
5. **Assess freshness/continuity** and explicitly classify gaps/contradictions.
6. **Reconcile keys/trust**; do not reactivate suspected-compromised signing/authorization material merely to accelerate recovery.
7. **Reconstitute a new authoritative control plane** at or above the recovered floor; ordinary restore cannot lower it.
8. **Revalidate policy, leases, revocations and recovery/bootstrap paths** against the new authority state.
9. **Resume capabilities by consequence**, keeping remote mutation gated where evidence remains UNKNOWN.
10. **Retire temporary recovery authority**, rotate/reseal recovery packages and restore continuous monitoring.

## PWA / Service Worker / EFB application

A long-offline company iPad may survive the server disaster with valid local flight records, old SW/cache, IndexedDB queue and old generation labels. It is useful as a **data/provenance source**, but not automatically as the canonical authority-floor source.

On reconnect after control-plane reconstitution:
- preserve/export irreplaceable local records before destructive migration;
- compare local operation IDs/provenance with recovered server data;
- do not allow the device to lower the recovered server authority floor;
- treat old cached policy/session/lease artifacts as claims requiring current reconciliation;
- permit local read/export/offline work where product policy allows while remote mutation remains gated;
- expose a truthful `DATA PRESERVED / SERVER AUTHORITY RECOVERING OR REVALIDATION REQUIRED` state rather than asking the user to erase data to make the UI look current.

Actual Safari/WebKit/MDM persistence, storage eviction, background execution and managed-EFB recovery behavior remain OPEN.

## Cross-track integration

### Track A — Platform & Browser
Owns exact browser/SW/cache/IndexedDB persistence and what local evidence can survive. Transfer: surviving local bytes can aid data recovery but cannot silently become server authority.

### Track B — UX / IA / Content
Owns degraded recovery communication and non-destructive user paths. Distinguish `data recovered` from `sync/remote authority restored`.

### Track C — Performance / Accessibility / Quality
Owns destructive disaster drills: total policy-store loss, stale escrow, unavailable custody, conflicting witness, old backup + old SW, accessible recovery UI and restore-time evidence capture.

### Track D — Search / Discovery / Analytics
Analytics can help identify impact/population but cannot establish authority-floor currentness. Disaster telemetry may itself be incomplete.

### Track E — Owner
Owns floor semantics, recovery custody, independence, reconstitution ordering, anti-rollback and resumption gates.

## MINTTAP DECISION — minimal sufficient generic model

If this class of authority system is implemented:
1. maintain an independently recoverable **minimum anti-resurrection authority floor**, separate from ordinary business-data backup semantics;
2. do not make the escrow/recovery copy an online fallback policy oracle;
3. authenticate recovery packages and separately evaluate freshness/currentness;
4. never lower authority because the newest surviving backup/package is old;
5. recover data and authority as separate planes, then reconcile;
6. distinguish decryption-key recoverability from signing/authorization-key recovery;
7. preserve historical verification without retaining obsolete execution authority;
8. require explicit recovery procedure/custody and retire temporary recovery capabilities after reconstitution;
9. keep PWA local data recoverable while old local policy/session/SW state remains unable to lower server authority;
10. choose provider, KMS/HSM, quorum, retention, timing and custody only after product/runtime evidence exists.

## VALIDATION — 48-case destructive campaign

1. primary authority store total loss; 2. all ordinary replicas lost; 3. business backup survives but floor escrow does not; 4. floor escrow survives but business backup does not; 5. both survive; 6. authentic current floor package; 7. authentic stale package; 8. forged newer package; 9. two authentic packages disagree; 10. newest package unavailable; 11. sequence gap before disaster; 12. witness says later floor existed; 13. witness unavailable; 14. witness shares same failure domain; 15. provider-native revocation survives; 16. provider state contradicts escrow; 17. old backup attempts to lower floor; 18. restore timestamp newer than floor package; 19. operator chooses old generation for convenience; 20. ordinary evaluator tries escrow fallback; 21. client requests escrow generation; 22. escrow service reachable from public request path; 23. recovery custody unavailable; 24. one custodian compromised; 25. multi-party recovery succeeds; 26. recovered encryption key restores data; 27. recovered suspected-compromised key immediately replaced; 28. historical verifier retained without signing key; 29. missing signing key does not justify old-authority activation; 30. lease table restored without consumption state; 31. revocation table older than floor; 32. retired G1 appears in stale replica; 33. temporary recovery authority not retired; 34. recovery audit evidence missing; 35. monitoring not re-established; 36. old SW + old cache reconnect; 37. offline iPad has records absent from server backup; 38. iPad carries stale lease; 39. iPad carries old policy bytes; 40. local export works while remote mutation gated; 41. destructive reinstall is not required for safe recovery; 42. accessible status distinguishes data vs authority; 43. provider/KMS regional catastrophe; 44. correlated identity/admin loss; 45. backup + escrow encrypted under same lost key; 46. escrow package authentic but verifier unavailable; 47. physical managed-iPad behavior remains OPEN; 48. end-to-end disaster drill restores data and a known non-decreasing authority floor without predecessor resurrection.

## CONTRADICTION / failure-mode analysis

### Backup-is-authority theater
The newest surviving database snapshot can still predate a critical revocation. Backup recency is not authority ordering.

### Escrow-as-secondary-production theater
If normal traffic can consult escrow after a primary denial/outage, escrow has become a second policy plane and downgrade oracle.

### Signature-validity theater
A valid signature proves package authenticity/integrity under the accepted verifier; it does not prove no newer floor existed.

### Multi-copy theater
Several copies protected by the same account/provider/admin/key failure domain do not establish independent recovery.

### Key-escrow-everything theater
Escrowing every private key increases compromise surface and can preserve obsolete signing authority. Recoverability must follow key purpose.

### PWA-device-as-authority theater
An offline device may contain the only copy of valuable business data while still being a stale/compromised authority source. Preserve its data without promoting its cached policy state.

## OPEN

Actual MintTap/LogMate policy store, provider, authority-floor schema, revocation representation, KMS/HSM, trust roots, signing/encryption keys, backup/PITR, independent storage, identity/admin dependencies, custody/quorum, RTO/RPO, lease model, Service Worker strategy, local data authority, import/export/recovery, managed-iPad behavior and legal/aviation retention requirements remain unknown. No concrete quorum, provider, retention duration or cryptographic ceremony is asserted.

## CHANGE WATCH

- NIST SP 800-57 Part 1 Rev. 6 remains draft as of this study; reassess when finalized.
- Selected cloud/database/KMS backup, export, cross-region and disaster-recovery guarantees.
- WebKit/iPadOS storage/SW/managed-device behavior for product claims.
- Any change to trust roots, policy-generation semantics, backup encryption, identity/admin topology or recovery custody requires refreshing disaster fixtures.

## Gate result

**PASS (generic).** The Web Manager can now separate data backup, authority-floor recovery and live authorization; design a non-live escrow role; reason about authentic-but-stale recovery packages; prevent old backup/client state from lowering a recovered authority floor; and define consequence-gated reconstitution after catastrophic control-plane loss.

Product/provider/managed-iPad/crypto-key/disaster-runtime validation remains **OPEN**.

## Next highest-value adjacent question

**PWA recovery-escrow survivability under organizational loss, custody succession & anti-capture governance.** 154 establishes technical recovery separation. The next risk is organizational: recovery material may survive technically while every legitimate custodian/admin is unavailable, or a single surviving insider may capture recovery authority. Determine succession, multi-party custody, emergency replacement and post-recovery re-sealing without creating permanent insider veto/capture or undocumented shadow authority.