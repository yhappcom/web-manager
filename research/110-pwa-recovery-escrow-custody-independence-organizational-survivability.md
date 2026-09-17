# 110 — PWA Recovery Escrow Custody, Independence & Organizational Survivability

Status: **PASS (generic) / PRODUCT CUSTODY + DISASTER-DRILL VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 101–109 recovery/provenance/longevity chain; Track C drill/fixity evidence; Track A access/runtime constraints; Software Engineering exact artifact/tooling; Design Studio recovery-state UX.

## Purpose

109 established that long-lived recovery requires a non-secret representation contract, historical fixtures/oracles and enough toolchain knowledge to reconstruct a safe current converter. That package can still fail catastrophically if its only copy, integrity evidence, access path and institutional knowledge share the same failure domain as production.

This study asks a narrower question: **what must survive organizational and control-plane loss for recovery knowledge to remain usable and trustworthy without turning escrow into a new repository of production secrets or personal data?**

This is generic architecture. It does not infer MintTap/LogMate providers, IAM topology, personnel, legal retention duties or backup format.

## 1. Track balance

- **A Platform/Browser:** dependency supplier for actual export/import and target-runtime accessibility. Browser storage is not organizationally independent custody.
- **B UX/IA/Content:** consumes truthful states such as escrow unavailable, authenticity unverified, authority unavailable, reconstruction pending and recovered.
- **C Quality:** owns independent-copy readability/fixity, loss-of-primary-domain drills and reconstruction evidence.
- **D Discovery/Analytics:** no observed escrow use is not evidence that custody is unnecessary; escrow access telemetry must avoid exposing artifact/user metadata.
- **E Architecture/Security/Operations:** highest-risk owner; owns failure-domain mapping, custody, authority succession, disaster procedures and survivability gates.

E remains the bottleneck. The problem is now institutional rather than parser-mechanical.

## 2. SOURCE — alternate storage is about common-hazard separation

NIST SP 800-34 Rev. 1 / CP-6 guidance requires an alternate storage site and explicitly describes geographic separation so the alternate site is not susceptible to the same hazards as the primary site. It also requires considering accessibility problems during area-wide disruption and mitigation such as another alternate copy or physical retrieval.

Sources:
- https://csrc.nist.gov/topics/security-and-privacy/security-programs-and-operations/contingency-planning
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf

**SYNTHESIS:** geographic separation is one instance of a broader failure-domain principle. For a web/PWA recovery escrow, two logical copies are not meaningfully independent if the same compromised GitHub organization, cloud tenant, SSO/IdP, root administrator, billing account, deletion workflow or encryption-key authority can destroy or make both inaccessible.

Guards:
- `two copies ≠ two independent failure domains`;
- `different repository ≠ different IAM/control-plane failure domain`;
- `different region ≠ different provider/account failure domain`;
- `different cloud provider ≠ independent custody if one IdP/admin path controls both`.

## 3. SOURCE — offline/segmented backups and tested restoration reduce common-mode compromise

CISA's current #StopRansomware guidance recommends offline encrypted backups, regular availability/integrity testing, and cautions that accessible backups can be deleted or encrypted by ransomware. It also suggests considering multi-cloud to avoid vendor lock-in and emphasizes least privilege/separation of duties for administrative access.

Source:
- https://www.cisa.gov/stopransomware/ransomware-guide

**TRANSFER VALIDATION:** format-spec escrow is not ordinary production backup data, but the same common-mode lesson applies. A custody copy that production automation can overwrite/delete during normal operation is weak evidence against production-account compromise.

**MINTTAP DIRECTION:** design at least one recovery-knowledge custody path whose destructive authority is not continuously reachable from the ordinary production deployment path. Exact medium/provider is a product/operations decision.

Guards:
- `encrypted copy ≠ deletion-resistant copy`;
- `immutable setting configured ≠ independent recovery authority proven`;
- `provider durability SLA ≠ organizational survivability`;
- `production admin can reach escrow ≠ escrow independent from production-admin compromise`.

## 4. Independence must be modeled as a vector

Do not label a copy simply `independent=true`. Evaluate independence across at least:

1. **storage/provider** — same service/account/region or genuinely separate custody;
2. **identity** — same SSO/IdP/root account/recovery email/phone or separate recovery path;
3. **authorization** — same person/service can delete all copies or destructive actions require independent authority;
4. **key/trust** — same key store/signing root needed to authenticate/decrypt every copy or independently recoverable verification/recovery material exists;
5. **network/control plane** — ordinary production automation can mutate escrow or not;
6. **billing/legal ownership** — one billing failure, domain loss, contract termination or company-account lockout disables all paths or not;
7. **personnel knowledge** — only one maintainer knows location/procedure or documented succession exists;
8. **format/tooling** — all copies require the same obsolete service/tool or 109 reconstruction knowledge is self-contained enough to move;
9. **physical/geographic hazard** where physical media or facilities matter;
10. **incident correlation** — compromise mechanism likely to affect all copies simultaneously.

**MINTTAP DIRECTION:** maintain a failure-domain matrix rather than counting copies.

Guard: `copy count ≠ independence score`.

## 5. Escrow contents and escrow authority are separate

109 keeps production secrets and live user records out of format-spec escrow by default. 110 strengthens that separation.

A useful preservation package may contain:
- product-owned format specifications/data dictionaries;
- synthetic/minimized fixtures and independent semantic oracles;
- significant-property and migration-invariant definitions;
- inventory/digests and provenance references;
- public verification keys/certificates or trust-history metadata where legitimately needed to verify historical evidence;
- dependency/toolchain/SBOM references;
- reconstruction and disaster procedures;
- custody inventory and authority contacts/roles.

It should not become a convenience bundle of:
- production DEKs/KEKs;
- live signing/private keys;
- session/refresh tokens;
- reusable device/pairing credentials;
- real user backup payloads or personal flight records without a separately justified retention regime;
- master credentials that unlock all custody copies.

Guards:
- `escrow survives production loss ≠ escrow should contain production authority`;
- `verification material retained ≠ signing authority retained`;
- `organizational survivability ≠ secret aggregation`.

## 6. Key recovery and key custody are purpose-specific

NIST SP 800-57 Part 1 Rev. 5 treats key recovery as mechanisms/processes allowing authorized entities to retrieve or reconstruct keying material from backup/archive. It emphasizes that recoverability depends on key purpose; for example, decryption material may need recovery for as long as protected data must be decrypted, while private signature-key backup is generally undesirable and, when justified, requires highly secure recovery and prompt replacement after recovery.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/key_recovery

A Revision 6 initial public draft was published 2025-12-05; until finalized, Rev. 5 remains the current final reference. **CHANGE WATCH:** key-management guidance and approved algorithms evolve.

**SYNTHESIS:** do not invent one universal `escrow key`. Separate:
- historical authenticity verification;
- encrypted-user-backup decryption/recovery, if product policy requires it;
- current release signing;
- current trust-policy signing;
- escrow-package authenticity;
- custody-access authentication.

Their recovery/retention rules may differ.

Guards:
- `one key can technically unlock several functions ≠ one key should govern several authorities`;
- `decryption key recoverable ≠ signing key should be recoverable`;
- `key backup exists ≠ authorized key-recovery procedure works`.

## 7. No single-person institutional dependency

A technically complete escrow can still fail if one employee is the only person who knows where it is, how to authenticate it, how to regain access or how to reconstruct the converter.

Generic succession evidence should include:
- role-based ownership rather than a person's memory as the canonical locator;
- at least one documented alternate authorized role/path for critical recovery functions;
- joiner/mover/leaver updates to custody and recovery authority;
- emergency contact/ownership records that remain available when primary collaboration systems are down;
- procedure versioning and review after personnel/provider changes;
- exercises involving someone other than the original author.

This does **not** imply every action must use a specific quorum. NIST controls include examples such as dual authorization for destructive backup actions and NIST key-management literature defines split knowledge, but exact quorum/dual-control policy is product-risk dependent.

Guards:
- `documented procedure ≠ successor can execute procedure`;
- `two named people ≠ independent authority if both depend on the same unavailable IdP`;
- `founder/admin available today ≠ organizational recovery path established`.

## 8. Authenticity must survive custody migration

Fixity answers whether bytes changed; authenticity answers whether the package is the governed package and its history is acceptable. Long-lived custody may move between providers/accounts/media, so authenticity cannot rely solely on mutable metadata inside the original storage account.

A generic evidence chain can bind:

`escrow generation × inventory/digests × specification/corpus/oracle revisions × provenance references × custody event × reviewer/authority record × verification material × drill result`.

When custody moves:
1. verify source inventory/fixity/authenticity before transfer;
2. transfer through a controlled path;
3. verify destination inventory/fixity;
4. record custody transition and authority change;
5. test destination readability/accessibility;
6. preserve previous evidence until the new custody path is independently validated;
7. retire old access according to policy rather than assuming migration itself revoked it.

Guards:
- `checksum matches after migration ≠ custody history authenticated`;
- `new provider copy readable ≠ old destructive authority revoked`;
- `old account closed ≠ all old credentials/tokens harmless`.

## 9. Disaster drill must remove the primary trust domain

A normal restore drill performed while GitHub, primary cloud, corporate SSO and original maintainers are all available does not prove organizational survivability.

A stronger drill deliberately declares selected primary dependencies unavailable/compromised. Example scenario:

`primary GitHub org unavailable + production cloud tenant unavailable + ordinary corporate SSO unavailable + original converter executable prohibited`.

The exercise should demonstrate, within the product-defined support envelope:
1. locate the independent escrow copy from an alternate procedure;
2. establish legitimate human/organizational authority without the unavailable primary identity path;
3. verify escrow authenticity/fixity using surviving evidence;
4. recover documentation/corpus/oracles without production secrets;
5. reconstruct a converter using 109 and admit it through 108 provenance/dependency controls;
6. restore a synthetic historical artifact and prove semantic oracle preservation;
7. preserve quarantine/no-credential-revival/reconciliation guards from 101–108;
8. document every hidden dependency that had to be reintroduced.

**VALIDATION:** any dependency unexpectedly needed during the drill is evidence that the failure-domain model was incomplete.

Guards:
- `backup restore drill PASS ≠ organizational-loss drill PASS`;
- `independent copy exists ≠ independent access/authentication works`;
- `escrow readable ≠ converter reconstructable`.

## 10. Destructive authority deserves stronger treatment than read authority

NIST SP 800-53 Rev. 5 CP-9 includes a control enhancement for dual authorization for deletion/destruction of organization-defined backup information. This is government-control guidance, not a universal MintTap requirement, but it validates the principle that destructive authority can warrant stronger separation than ordinary read/test access.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**MINTTAP DIRECTION:** when product evidence exists, explicitly classify who/what may read, append a new generation, replace current custody, delete historical generations, rotate authenticity/recovery material and declare a format retired. Avoid one broad administrator permission where narrower roles are practical.

Guard: `authorized to read/reconstruct ≠ authorized to destroy all recovery evidence`.

## 11. Provider and account loss are different from provider outage

Operational planning must distinguish:
- temporary service outage;
- region failure;
- tenant/account suspension or compromise;
- billing/contract failure;
- domain/SSO loss;
- provider shutdown/product retirement;
- malicious deletion by an authorized account;
- legal/organizational transfer or company dissolution.

Multi-region replication can help the first classes while doing little for account-wide compromise. Multi-provider copies can still share identity, billing, personnel or key failure domains.

**MINTTAP DIRECTION:** select custody diversity against named hazards, not the label `multi-cloud`.

Guard: `multi-region ≠ multi-account ≠ multi-provider ≠ multi-authority`.

## 12. Privacy and minimization remain constraints on survivability

The easiest escrow to preserve forever is also the easiest to over-retain. Long retention multiplies breach, discovery, access-control and stale-data risk.

Default hierarchy:
1. preserve product-owned non-secret representation knowledge;
2. preserve synthetic/minimized fixtures;
3. preserve integrity/provenance/custody metadata that does not expose users;
4. preserve production user artifacts only under a separately defined product/legal recovery requirement and access/retention policy.

Do not use real user backups merely to make an organizational-loss drill realistic.

Guard: `more durable escrow ≠ more data should be escrowed`.

## 13. Track C validation campaign

Exact-product validation should include at least:
1. map storage/provider/identity/admin/key/billing/personnel/network failure domains;
2. prove at least one governed copy is outside the ordinary production destructive path if product risk requires it;
3. simulate loss of primary repository/cloud/SSO separately and in a combined scenario;
4. locate escrow without relying on original maintainer memory;
5. verify independent-copy inventory/fixity;
6. verify authenticity without relying solely on metadata in the failed primary account;
7. prove destination readability after custody migration;
8. prove old access is revoked/contained after migration;
9. prove production secrets and personal user data are absent from format-spec escrow by default;
10. verify synthetic cryptographic fixtures remain usable;
11. verify required decryption/recovery material, if any, follows its own governed recovery policy;
12. verify current signing/private authority is not casually recoverable from preservation escrow;
13. exercise personnel succession with a non-author procedure executor;
14. exercise joiner/mover/leaver authority changes;
15. exercise provider/account/billing/domain-loss contacts and ownership evidence;
16. reconstruct a converter without original executable using independent custody material;
17. admit reconstructed artifact through 108 provenance/dependency policy;
18. preserve 101 reconciliation/no-blind-replay behavior;
19. record hidden dependencies discovered by the drill and update the failure-domain matrix;
20. repeat after material custody/IAM/provider/key/personnel/format changes.

No generic frequency or retention number is set here; product risk and obligations must determine thresholds.

## 14. Design Studio transfer

Canonical Design Studio `progress/WEB_STATUS.md` checked 2026-09-17: Web Design is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED. W061 defines a GitHub Actions execution bridge, but first artifact-bearing run remains OPEN. No Safari/WebKit, screen-reader, physical-device or field-runtime PASS transfers.

**DEPENDENCY:** Web Manager supplies truthful recovery states and organizational-unavailability conditions. Design Studio owns reusable interaction evidence for unavailable/verification-required/reconstruction-pending/recovery-complete states once executable product evidence exists.

## 15. Software Engineering transfer

Canonical Software Engineering Studio `progress/STATUS.md` checked 2026-09-17: every specialist remains Foundation IN STUDY. Its Data/Quality/Architecture evidence provides reusable invariant, restore, reconciliation and generated-failure methods; no exact product escrow implementation or disaster-reconstruction proof transfers.

**DEPENDENCY:** Software Engineering owns exact package/build/converter/IAM integration and executable disaster harness. Web Manager owns web/PWA recovery trust requirements, custody failure-domain model and evidence required before a survivability claim.

## 16. EFB/LogMate bounded application

A LogMate-like managed-iPad PWA may hold irreplaceable offline flight records, so future recovery knowledge can matter after the original app/toolchain/team changes. Generic direction:

`independent non-secret format escrow + separate user-backup/key policy + failure-domain matrix + alternate organizational authority + no-primary-domain reconstruction drill`.

Do not infer that a company iPad can access a chosen escrow provider during normal operation; the escrow is primarily an organizational recovery capability, not an unattended device-to-device sync mechanism. Exact MDM/network/Files/iCloud/provider policy remains OPEN.

MintTap production architecture and data criticality were not inspected; equivalent requirements are not inferred.

## 17. CHANGE WATCH

Re-check when:
- NIST SP 800-57 Rev. 6 becomes final or key-management recommendations materially change;
- escrow/provider/IAM/billing/domain ownership changes;
- company personnel/authority model changes;
- format/spec/corpus generation changes;
- cryptographic verification/recovery algorithms change;
- legal/contractual retention or data-residency obligations change;
- a disaster/reconstruction drill exposes a common dependency.

## 18. Gate

**PASS (generic)** because this study establishes:
- common-mode/failure-domain reasoning beyond copy count;
- custody independence across storage, identity, authorization, key, network, billing, personnel and tooling dimensions;
- strict separation of preservation knowledge from production secrets/live authority;
- purpose-specific key-recovery boundaries;
- personnel succession and destructive-authority separation principles;
- custody-migration authenticity requirements;
- a no-primary-trust-domain reconstruction drill;
- 20 exact-product validation cases and cross-repository ownership boundaries.

**OPEN:** exact providers/accounts/regions, IAM/SSO/root recovery, billing/domain ownership, custody media, quorum/dual-control policy, key hierarchy/recovery, retention/residency/legal requirements, escrow inventory, actual format/corpus, disaster drill, converter reconstruction, managed-iPad/browser/runtime and product security/privacy/accessibility evidence.

## Persistent guards added by 110

`two copies ≠ two independent failure domains`.  
`different repository ≠ different IAM/control-plane failure domain`.  
`different region ≠ different provider/account failure domain`.  
`copy count ≠ independence score`.  
`encrypted copy ≠ deletion-resistant copy`.  
`provider durability SLA ≠ organizational survivability`.  
`escrow survives production loss ≠ escrow should contain production authority`.  
`verification material retained ≠ signing authority retained`.  
`decryption key recoverable ≠ signing key should be recoverable`.  
`documented procedure ≠ successor can execute procedure`.  
`checksum matches after migration ≠ custody history authenticated`.  
`backup restore drill PASS ≠ organizational-loss drill PASS`.  
`independent copy exists ≠ independent access/authentication works`.  
`authorized to read/reconstruct ≠ authorized to destroy all recovery evidence`.  
`multi-region ≠ multi-account ≠ multi-provider ≠ multi-authority`.  
`more durable escrow ≠ more data should be escrowed`.
