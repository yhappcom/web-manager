# 190 — PWA Preservation Portability Proof, Escrow Independence & Uncooperative-Provider Recovery

Status: **PASS (generic) / PRODUCT + PROVIDER + LEGAL + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A offline/reconnect mechanics; Track B degraded/recovery UX; Track C destructive validation; Track D privacy-bounded continuity telemetry.
Dependencies: 183–189 exact-artifact lineage, transparency, archive integrity, historical verifier isolation, preservation compromise, provider exit and cross-provider re-anchoring.

## Problem
189 established that provider exit must transfer evidence plus applicable historical validation context. The adjacent risk is false portability: a provider may expose an export API or secondary copy that appears adequate until the incumbent disappears, after which policy/status/audit/verifier dependencies, credentials, keys, formats or operational knowledge prove unavailable. A nominal escrow may also share the incumbent's identity, cloud, KMS, administrator or recovery failure domain.

Central rule:

> **Portability is a demonstrated recovery capability, not an export feature. An escrow/continuity copy is independent only to the extent that the recovery path and evidence needed to use it survive failure of the incumbent's relevant failure domains.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser caches, IndexedDB, Service Worker state and offline tokens can preserve observations/data but are neither escrow nor current provider authority.
- **B UX/IA/Content:** high-pressure consumer. Owns clear states for local work preserved, provider unavailable, historical verification incomplete/unknown, recovery in progress and remote submission paused.
- **C Performance/Accessibility/Quality:** validator. Owns destructive loss-of-provider, loss-of-dependency, correlated-escrow, restore and long-offline-client campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Continuity telemetry must not turn recovery copies into user/device/flight tracking datasets.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns portability proof, continuity custody, independent recovery, uncooperative-provider failure and reconstitution boundaries.

## SOURCE
### RFC 4810 — Long-Term Archive Service Requirements
RFC 4810 requires transfer of archived data objects, evidence and evidence records between services and requires evidence records to span multiple providers without losing evidentiary value. It also warns that an archive service should not necessarily be trusted to supply every element required for proof; for example, allowing the archive itself to supply trust anchors can enable forgery. Evidence records can require certificates, revocation information, trust anchors, policy details and role information.

Source: https://www.rfc-editor.org/rfc/rfc4810.html

### NIST SP 800-53 Rev.5 — contingency/backup separation and testing
The current control catalog distinguishes contingency testing, alternate storage, alternate processing, backup reliability/integrity testing, test restoration, separate storage for critical information, transfer to alternate storage and redundant secondary systems. The important transferable principle is that a second copy and a tested recovery capability are separate properties; separation and accessibility matter.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### CISA #StopRansomware recovery guidance
CISA recommends offline encrypted backups of critical data and regular availability/integrity testing in disaster-recovery scenarios, explicitly because accessible backups can be discovered and destroyed by the same incident. This is ransomware guidance, not a preservation-service standard, but it is strong operational precedent for correlated-failure analysis and tested restore.

Source: https://www.cisa.gov/stopransomware/ransomware-guide

## SYNTHESIS — portability proof is stronger than export proof
A defensible portability proof needs at least four distinct demonstrations:
1. **package completeness** — exact objects/evidence plus policy/profile/status/audit/verifier/canonicalization/retention metadata needed by the declared historical validation scope are present or independently obtainable;
2. **independent custody** — the recovery package and its access path do not rely solely on the failed incumbent's account, IdP, DNS, KMS, support channel, administrator, billing state, region or control plane;
3. **independent interpretability** — enough authenticated format/schema/policy/verifier context survives to interpret the package without asking the failed provider to explain proprietary semantics;
4. **executed recovery** — a representative package has actually been restored/imported and its expected integrity/history results reproduced under a separately controlled recovery environment.

Persistent guards:
- `export API exists ≠ portability proven`;
- `export downloaded ≠ export complete`;
- `second copy exists ≠ independent recovery path exists`;
- `different bucket/account ≠ different failure domain`;
- `different provider name ≠ independent identity/KMS/admin/recovery domain`;
- `escrow readable ≠ escrow authentic/complete`;
- `restore parses ≠ historical validation reproduced`;
- `restore succeeds once ≠ ongoing portability remains proven`;
- `provider unavailable ≠ escrow becomes current authority`;
- `escrow has historical roots ≠ roots belong on current admission path`;
- `provider API unavailable ≠ unique local operational data should be destroyed`.

## Failure-domain independence matrix
Continuity custody should be evaluated across explicit dimensions rather than a binary `independent=true` flag:
- organization/legal entity and contract termination;
- cloud/provider/control plane and region;
- identity provider, MFA/recovery and privileged administrators;
- DNS/domain/email dependency;
- KMS/HSM/key-wrapping/recovery path;
- storage account and deletion authority;
- build/export tooling and proprietary runtime;
- policy/schema/verifier documentation source;
- audit/status/revocation evidence source;
- network path and operational site;
- personnel/custodian succession;
- billing/payment suspension;
- incident blast radius and backup deletion credentials.

Independence is claim-specific. A copy may survive storage loss while remaining dependent on the same IdP or decryption KMS. Do not convert partial independence into global independence.

## Portability proof ceremony
Generic sequence:
1. freeze the declared provider/service/policy generation and recovery scope;
2. generate an export and a manifest that identifies exact package objects and required external dependencies;
3. copy the package to continuity custody under independently governed access;
4. verify object identity/integrity and authenticated provenance outside the incumbent's ordinary control plane;
5. remove incumbent API/network availability from the test path;
6. recover required schemas/policies/status/audit/verifier context from the continuity package or independently retained authoritative sources;
7. restore/import a representative sample into an isolated successor/recovery environment;
8. reproduce expected historical verification outcomes, including known UNKNOWN/INVALID cases rather than only happy-path valid records;
9. demonstrate that predecessor private issuance/current-admission authority is absent;
10. record gaps, recovery duration, dependency failures and the exact proof scope;
11. repeat after material provider/schema/policy/key/export changes.

A checksum of the exported ZIP proves neither semantic completeness nor recoverability.

## Uncooperative-provider failure recovery
When the provider disappears without a cooperative export window:
- freeze claims about the last known provider generation; do not invent a clean cessation boundary;
- preserve independently held packages, manifests, receipts, public verification/status/policy material and prior test evidence;
- classify missing intervals/dependencies as `UNKNOWN` where they cannot be reconstructed from authenticated independent evidence;
- establish any successor preservation service as a new generation through current governance;
- import only evidence whose provenance and interpretation can be bounded;
- retain gaps explicitly; successor re-attestation cannot manufacture missing predecessor audit/status/history;
- prevent restored/PITR configuration from re-enabling predecessor signing or current admission;
- keep local PWA/EFB records available while remote consequence-bearing operations wait for current admission.

`provider failure` is not permission to lower evidence standards silently. Availability pressure may justify degraded service, not historical fabrication.

## Escrow is custody, not authority
Escrow/continuity storage may hold historical public verification material, encrypted evidence packages, policy/profile snapshots, manifests and recovery tooling. It should not automatically hold live predecessor issuance authority. If decryption or import requires secrets, those secrets need their own survivability and separation analysis.

A continuity provider that shares the incumbent's privileged administrator, KMS recovery account or deletion authority can be operationally correlated even if data is stored in a different region/vendor product.

## PWA / EFB boundary
A company iPad may be offline during provider collapse and return with records that never reached remote preservation, plus old provider tokens/roots and stale Service Worker/IndexedDB state.

Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. treat cached provider material as historical observation only;
3. obtain current authenticated server security/preservation generation when connectivity exists;
4. distinguish records previously acknowledged by the old provider from local-only/unacknowledged work;
5. reconcile acknowledged historical evidence against independently recovered lineage; retain UNKNOWN where dependencies are missing;
6. submit local-only work under current provider/current server authority rather than attempting to mint predecessor history;
7. re-admit queued consequence-bearing operations only after current authorization and reconciliation.

Do not assume suspended iPadOS Home Screen apps can perform continuity export, escrow refresh, background re-attestation or unattended peer-to-peer recovery. Physical Safari/Home Screen/MDM evidence remains OPEN.

## Privacy boundary
Independent continuity does not justify indiscriminate replication. Escrow packages, manifests and recovery telemetry should minimize raw user/device/flight/location identifiers and should inherit retention/deletion/legal-hold governance. Temporary restore environments and test copies require explicit cleanup/retention handling.

## Track C destructive campaign
Define a **280-case generic campaign** extending the 272-case baseline with:
- export API reports success but omits policy/profile dependency;
- package hash valid but manifest omits an evidence segment;
- escrow shares incumbent IdP/MFA recovery;
- escrow uses separate cloud but same KMS/wrapping root;
- separate region shares account-level deletion authority;
- provider disappears before final export;
- proprietary verifier unavailable after provider failure;
- independent package restores but known UNKNOWN case becomes falsely VALID;
- recovery environment can accidentally use predecessor private issuance key;
- PITR restores old provider as current;
- continuity copy is stale across policy/key generation;
- billing suspension disables both incumbent and escrow access;
- DNS/email loss blocks both recovery paths;
- custodian departure makes escrow unreadable;
- long-offline iPad returns with predecessor-only acknowledgements;
- local-only iPad records are mistaken for predecessor-preserved records;
- queue drains before current provider/security reconciliation;
- recovery telemetry leaks stable user/device/flight identity;
- screen-reader/operator cannot distinguish `provider unavailable` from `local data lost`;
- urgency pressures acceptance of an untested export as proven recovery.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat portability as a periodically demonstrated recovery capability, not a contractual/export checkbox.
2. Require a dependency manifest and independent restore/import exercise for representative evidence, including UNKNOWN/INVALID fixtures.
3. Model continuity independence per failure domain; do not infer it from provider count, region count or copy count.
4. Keep escrow custody separate from current signing/admission authority.
5. Preserve enough authenticated policy/schema/status/audit/verifier context to recover without incumbent cooperation where the declared evidence scope requires it.
6. On abrupt provider loss, preserve uncertainty rather than allowing a successor to fabricate missing history.
7. Re-test portability after material format/policy/key/provider/recovery-path changes.
8. Keep recovery/test copies and telemetry privacy-bounded and lifecycle-governed.
9. Preserve unique offline PWA/EFB data; reconcile it under current authority after reconnect rather than treating stale provider material as authority.
10. Keep exact MintTap/LogMate provider, escrow topology, evidence duration, recovery objective, package format and managed-iPad behavior OPEN until project/runtime evidence exists.

## TRANSFER VALIDATION / CONTRADICTION
- NIST/CISA backup separation and restore-testing principles transfer to the **operational survivability** question, but they do not by themselves prove cryptographic/evidentiary portability.
- RFC 4810's warning that an archive should not necessarily supply all trust material contradicts architectures in which the incumbent is the sole source of both evidence and the trust context required to validate that evidence.
- Software Engineering Studio remains Foundation-in-study; implementation details for exact export/import, verifier isolation and restore tooling are a dependency, not something Web Manager claims as executed product evidence.
- Design Studio Web remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate requires an external preservation/TSA service: **OPEN**.
- Exact provider/escrow/continuity topology and legal/aviation evidence obligations: **OPEN**.
- Exact export schema, canonicalization, verifier runtime, decryption/key hierarchy and import tooling: **Software Engineering dependency**.
- Actual independent recovery domains and provider contractual export behavior: **OPEN / provider validation**.
- Representative restore from a real provider export with incumbent access removed: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM long-offline behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 280-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- Provider export APIs, trust-service profiles, status/revocation availability and contractual exit behavior can change.
- Browser/iPadOS storage/background behavior remains change-sensitive.
- PQC/algorithm transitions may change package/verifier dependencies and trigger new portability tests.
- Jurisdiction-specific retention/termination requirements must be checked at project time.

## Adjacent next bottleneck
**PWA continuity-custody compromise, escrow poisoning & recovery-package freshness/anti-rollback**: determine how independently held recovery packages prove freshness/completeness across generations, how poisoned or rolled-back escrow is detected without making the incumbent the sole oracle, how recovery custody is rotated after compromise, and how long-offline clients converge without treating an escrow snapshot as current authority.