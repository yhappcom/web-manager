# 215 — PWA Cryptographic Inventory Attestation, Shadow-Crypto Discovery & Retirement-Proof Governance

Status: **PASS (generic) / PRODUCT + INVENTORY-TOOLING + RELEASE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/platform discovery; Track B migration/recovery state communication; Track C assurance and destructive validation; Track D inventory/drift observation.  
Dependencies: 137, 205–214 and the earlier authority/currentness/recovery/provenance chain.

## Problem
214 established that crypto inventory completeness is a multi-plane evidence claim rather than the output of one scanner. The adjacent governance problem is stronger: how can an organization trust an inventory snapshot itself, discover cryptography that is unmanaged, dormant, implicit or transitive, detect drift before it silently becomes authority, and make a defensible retirement claim without pretending to prove universal absence?

Central rule: **a cryptographic inventory is a versioned evidence product with provenance, coverage and uncertainty—not a static spreadsheet. Retirement is a consequence-bearing negative claim that requires bounded evidence across known execution and recovery planes, plus explicit residual unknowns.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Owns where browser/WebCrypto/TLS/Service Worker/storage/platform cryptography can be observed and where the platform hides implementation detail. It does not decide acceptance or retirement authority.
- **B UX/IA/Content:** high dependency pressure. Must represent migration-required, blocked, unknown, historical-only and data-preserved/sync-blocked states without inventing insecure compatibility escape hatches.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **480 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Owns coverage/drift/unknown telemetry and observation quality, but telemetry cannot prove cryptographic safety or universal absence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns inventory provenance, attestation scope, drift gates, shadow-crypto governance, retirement evidence and residual-risk classification.

## SOURCE

### NIST CSWP 39upd1 — crypto agility remains controlled replaceability
NIST CSWP 39upd1, *Considerations for Achieving Crypto Agility: Strategies and Practices*, is the current final NIST crypto-agility white paper, updated/finalized 2026-06-29. It defines crypto agility across protocols, applications, software, hardware, firmware and infrastructure and emphasizes environment-specific strategies, mechanisms, trade-offs and maturity rather than a universal switch.

Sources:
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://www.nist.gov/publications/considerations-achieving-crypto-agility-strategies-and-practices-0

**TRANSFER VALIDATION:** inventory/retirement governance is part of enabling replaceability. NIST does not certify MintTap inventory completeness or define a product-specific attestation schema.

### NCCoE Migration to PQC — comprehensive inventory is a maintained risk-management input
NCCoE's current Migration to PQC material separates **Cryptographic Visibility and Risk Management** from **Interoperability and Benchmarking**. Its FAQ defines a cryptographic inventory as a descriptive record of cryptography used across systems, applications, services, devices and data flows and explicitly says the listed discovery tools are not exhaustive. Current examples span edge/TLS scanners, certificate discovery, code analysis and collaborator inventory products.

Sources:
- https://pages.nist.gov/nccoe-migration-post-quantum-cryptography/
- https://www.nccoe.nist.gov/applied-cryptography/migration-to-pqc

The preliminary SP 1800-38B discovery work also states that automated tools should identify cryptography in hardware/software modules, libraries, embedded code, key-management and access-management paths. It remains a **Preliminary Draft**, so its detailed method is supporting evidence rather than final normative guidance.

Source:
- https://www.nccoe.nist.gov/publications/practice-guide/migration-post-quantum-cryptography-nist-sp-1800-38-practice-guide

**TRANSFER VALIDATION:** multiple discovery vantage points are necessary because each tool sees only part of the environment. `tool list available ≠ organization inventory complete`.

### CISA SBOM resources — component transparency is useful but bounded
CISA's SBOM resources treat software-component transparency as a supply-chain capability. SBOM evidence can help identify libraries/packages that may contain cryptographic functionality, but a component inventory does not reveal every runtime algorithm, key, provider default, SaaS behavior, platform primitive or dormant recovery artifact.

Source:
- https://www.cisa.gov/topics/cyber-threats-and-advisories/sbom/sbomresourceslibrary

**CONTRADICTION:** `SBOM complete ≠ cryptographic inventory complete`. SBOM is one evidence plane, not the crypto authority ledger.

## SYNTHESIS 1 — inventory snapshots need provenance and scope
An inventory snapshot should identify at least:
- inventory generation/version and schema;
- collection time/window and applicable environment/release;
- collection methods/tool versions/configurations;
- source repositories/build/artifact identities where relevant;
- observed systems/assets/flows and declared scope exclusions;
- cryptographic purpose, algorithm/parameters, key/anchor/provider/library and acceptance state;
- owner/custodian and consequence-bearing use;
- offline/backup/export/recovery/historical presence;
- evidence references supporting each material assertion;
- known blind spots, stale observations and unresolved conflicts;
- reviewer/approval state for claims that drive migration or retirement.

A signature over a snapshot can protect integrity/authenticity of the snapshot, but cannot make missing discovery coverage true.

`inventory signed ≠ inventory complete`; `snapshot authentic ≠ snapshot accurate`; `snapshot current ≠ all assets observed current`.

## SYNTHESIS 2 — attestation must bind claim, evidence and coverage
Do not attest merely `inventory complete=true`. A useful attestation states a bounded proposition such as: under inventory generation G, methods M1..Mn observed scopes S1..Sk during window W; unresolved unknowns U remain; prohibited crypto P was not observed in covered consequence-bearing paths; specified negative tests rejected P at enforcement points E.

This preserves the difference between:
1. integrity of the inventory artifact;
2. provenance of discovery evidence;
3. coverage of the discovery process;
4. correctness of classification;
5. authorization to declare retirement.

`attested claim ≠ universal fact`; `reviewed inventory ≠ independently replicated inventory`.

## SYNTHESIS 3 — shadow crypto has several distinct origins
Treat `shadow crypto` as cryptography outside the governed inventory/acceptance path, including:
1. developer/library defaults introduced without explicit policy;
2. unmanaged or vendored libraries/scripts/plugins;
3. transitive dependencies and native/FFI modules;
4. SaaS/CDN/identity/payment/analytics/support-provider cryptography;
5. CI/CD, code signing, package registries and update channels;
6. backup/export/import/archive/TSA/checkpoint paths;
7. MDM/profile/certificate/bootstrap and enterprise provisioning;
8. browser/OS/platform cryptography selected implicitly;
9. dormant disaster-recovery/offline media and historical verifier bundles;
10. experimental/test/debug/admin tooling that can cross into production authority.

Not every cryptographic primitive discovered is consequence-bearing. Inventory must bind purpose and authority before prioritization.

`crypto found ≠ current authority`; `not in source tree ≠ not in system`; `not in runtime telemetry ≠ not in recovery path`.

## SYNTHESIS 4 — reconcile evidence planes instead of choosing a favorite scanner
A mature discovery loop compares at least:
- source/dependency/SBOM/CBOM evidence;
- build and artifact inspection;
- config/IaC/policy/secret/KMS/HSM/certificate inventories;
- network/endpoint/protocol observation;
- runtime/API/provider telemetry;
- cloud/SaaS/vendor declarations and contract/config evidence;
- backup/export/archive/recovery/offline-media inventories;
- MDM/device/bootstrap/profile state;
- historical evidence/verifier requirements;
- owner/system declarations.

Disagreement is a finding. Example: source declares library L but runtime never observes it; runtime observes algorithm A but source/config cannot explain it; KMS contains key K with no owner; backup metadata references retired certificate C. These are not noise to normalize away.

`evidence-plane disagreement ≠ choose newest record`; `unowned crypto ≠ harmless crypto`.

## SYNTHESIS 5 — inventory drift should become a release and incident signal
Define material drift separately from routine inventory churn. Examples that should trigger investigation or a release/security gate include:
- new algorithm/provider/key/anchor in a consequence-bearing path;
- reappearance of RETIRED/REJECTED crypto;
- acceptance-matrix change without corresponding inventory generation;
- unknown cryptographic dependency introduced by a build/provider change;
- owner/custodian loss for current authority;
- dormant recovery path no longer exercised within its required evidence horizon;
- production observation inconsistent with approved build/config;
- rollback/PITR restoring older crypto policy or inventory.

The inventory should therefore be compared across release, infrastructure, provider and recovery generations—not refreshed only on an annual calendar.

`inventory updated ≠ drift reviewed`; `release green ≠ crypto drift acceptable`.

## SYNTHESIS 6 — retirement proof is bounded negative evidence, not proof of absolute absence
For a retired algorithm/key/anchor R, define the exact consequence-bearing claim: for example, `R cannot authorize new release signatures, current sync admission, bootstrap, recovery or remote mutation under policy generation G`.

A defensible retirement evidence bundle can include:
- acceptance policy marks R historical-only/rejected;
- current signer/issuer paths cannot emit R for prohibited purposes;
- representative and destructive negative tests submit valid-looking R artifacts and observe rejection;
- source/config/build/provider searches find no current prohibited issuer/acceptor path in covered scope;
- key/certificate/KMS/HSM custody state prevents prohibited current use where applicable;
- deployment/region/PITR/rollback checks preserve the retirement floor;
- offline/recovery/backup tails are enumerated and either migrated, quarantined or explicitly UNKNOWN;
- telemetry shows no prohibited use during a stated observation window, with known coverage;
- long-offline client convergence rejects R as current authority while preserving unique data.

This supports a scoped conclusion. It does **not** prove that no byte containing R exists anywhere.

`retired authority extinct ≠ every historical artifact destroyed`; `zero rejection events ≠ no retired attempts`; `negative test PASS ≠ universal absence proven`.

## SYNTHESIS 7 — historical verification and current authority must remain separable in inventory
Retirement can be successful while a legacy public key, parser, certificate chain or verifier remains intentionally available for historical evidence. Inventory must classify these as historical-verify-only and prove they are not reachable as current issuance/bootstrap/recovery authority.

Deleting every old verifier may destroy evidentiary value; retaining old private signing keys merely for verification is unnecessary and dangerous.

`historical artifact present ≠ retirement failed`; `historical verifier retained ≠ current issuer retained`.

## SYNTHESIS 8 — dormant paths require exercises, not telemetry optimism
A disaster-recovery signer, offline recovery package, export verifier or MDM bootstrap may have no ordinary production telemetry. Its silence cannot prove compliance. Dormant consequence-bearing paths need scheduled or change-triggered exercises with exact artifact/policy generations and negative tests.

Exercise cadence should follow risk/change, not an invented universal interval. Provider migration, crypto-policy change, recovery-authority change, major platform update or long inactivity can all invalidate old evidence.

`dormant ≠ retired`; `unused ≠ safe`; `drill passed once ≠ dormant path still current`.

## SYNTHESIS 9 — browser/PWA implicit crypto creates a special observability boundary
A PWA may depend on TLS/WebPKI, browser storage protection, WebCrypto, platform randomness, OS key stores, push/service infrastructure or managed-device certificates without owning their internal implementation. Inventory should record the **dependency and observable contract**, not invent hidden implementation facts.

For WebKit/iPadOS, exact algorithms/providers/platform behavior remain execution/change-watch evidence. A standards API name is not proof of underlying provider, hardware protection or long-term availability.

`WebCrypto API used ≠ underlying provider known`; `secure context ≠ product crypto inventory complete`; `platform-managed ≠ risk-owner absent`.

## SYNTHESIS 10 — SaaS/provider declarations are evidence, not self-proving truth
Provider documentation, attestations and API inventories can cover cryptography inaccessible to local scanners. They should be versioned against provider/service/config generation and reconciled with observable behavior. A provider's `PQC ready` claim does not prove the exact MintTap flow uses PQC or that all fallback paths are retired.

`vendor attested ≠ tenant configured`; `provider supports PQC ≠ flow uses PQC`; `contract says retired ≠ runtime rejects retired`.

## SYNTHESIS 11 — inventory itself needs anti-rollback and succession
Because inventory drives retirement and migration decisions, an authentic old inventory can be dangerous after policy changes. Preserve inventory generation lineage and reject stale snapshots for current authorization/governance decisions. PITR/restore must not silently reinstate an older acceptance matrix or inventory floor.

Historical snapshots remain useful as evidence; they do not regain current authority.

`authentic inventory ≠ current inventory`; `PITR restored inventory ≠ current policy restored`.

## SYNTHESIS 12 — long-offline EFB/PWA devices are an explicit inventory tail
A company iPad may remain offline across several crypto generations and return carrying unique records plus old Service Worker/session/certificate/policy state. Inventory should classify such devices/fleet tails by last-known policy generation and current reachability without pretending that silence means migration.

On reconnect, preserve unique flight/logbook data first; obtain current authenticated policy; quarantine stale authority; then re-admit queued operations. If current verification cannot execute, block consequence-bearing sync rather than reopening retired crypto.

`fleet inventory says migrated ≠ unreachable device migrated`; `device absent from telemetry ≠ device absent`.

## MINTTAP DECISION / DIRECTION
At generic architecture level:
1. treat crypto inventory as a versioned, provenance-bearing evidence product with scope, methods, coverage and explicit unknowns;
2. attest bounded inventory propositions rather than a Boolean `complete` claim;
3. reconcile source/dependency, build, config, key/cert stores, network/runtime, provider, backup/recovery, MDM/device and historical-verifier evidence planes;
4. treat unexplained disagreement between evidence planes as a finding;
5. classify shadow crypto by purpose and consequence before prioritization;
6. make material crypto drift a release/incident signal when it changes authority, acceptance, provider, key/anchor or retirement state;
7. define retirement as a scoped consequence-bearing negative claim and support it with policy, kill-path, negative-test, regional/PITR, inventory and observation evidence;
8. never equate retirement with destruction of all historical verification material;
9. exercise dormant recovery/offline paths because ordinary telemetry cannot validate them;
10. inventory browser/PWA/platform-managed crypto at the observable dependency/contract level and keep hidden implementation facts OPEN;
11. treat provider attestations as one evidence plane, not product proof;
12. protect inventory generations against rollback and keep long-offline devices as explicit migration tails.

## Track transfers
### Track A — DEPENDENCY / TRANSFER
Map actual observable crypto dependencies at browser, TLS/WebPKI, WebCrypto, Service Worker/update, storage, push and managed-device boundaries. Do not infer hidden WebKit/OS crypto implementation. Exact Safari/iPadOS behavior requires runtime/platform evidence.

### Track B — DEPENDENCY
Consume Design Studio evidence to communicate `migration required`, `unknown`, `historical verify-only`, `blocked current authority`, and `data preserved / sync blocked` states. Do not expose a user choice that downgrades the server security floor.

### Track C — VALIDATION
Destructive campaign grows **472 → 480 defined cases**:
1. signed inventory snapshot omits a consequence-bearing SaaS signer but verifies cryptographically;
2. SBOM/source scan is clean while runtime provider emits retired crypto;
3. runtime telemetry is clean while dormant backup/export path still accepts retired anchor R;
4. release introduces an implicit library/provider default not present in approved inventory generation;
5. valid-looking retired R artifact is submitted after retirement and one region incorrectly accepts it;
6. PITR restores old inventory/acceptance matrix and resurrects R;
7. provider attests PQC/current crypto while tenant configuration still negotiates legacy fallback;
8. long-offline iPad absent from fleet telemetry returns with unique data and retired authority after fleet migration is declared complete.

Execution, physical iPad/Safari, actual providers/libraries, inventory tools, release gates, PKI/KMS/TSA, backup/recovery, schema/performance and human validation remain OPEN.

### Track D — TRANSFER VALIDATION
Measure coverage by discovery plane, unexplained cross-plane conflicts, unowned/unknown crypto, inventory age by asset, material drift events, prohibited-use/rejection events, dormant-path exercise age, provider declaration/config mismatch and unreachable/offline fleet tails. Metrics support governance; they do not prove universal completeness or cryptographic correctness.

## Persistent guards added through 215
- `inventory signed ≠ inventory complete`;
- `snapshot authentic ≠ snapshot accurate`;
- `snapshot current ≠ all assets observed current`;
- `attested claim ≠ universal fact`;
- `reviewed inventory ≠ independently replicated inventory`;
- `SBOM complete ≠ cryptographic inventory complete`;
- `crypto found ≠ current authority`;
- `not in source tree ≠ not in system`;
- `not in runtime telemetry ≠ not in recovery path`;
- `evidence-plane disagreement ≠ choose newest record`;
- `unowned crypto ≠ harmless crypto`;
- `inventory updated ≠ drift reviewed`;
- `release green ≠ crypto drift acceptable`;
- `retired authority extinct ≠ every historical artifact destroyed`;
- `zero rejection events ≠ no retired attempts`;
- `negative test PASS ≠ universal absence proven`;
- `historical artifact present ≠ retirement failed`;
- `historical verifier retained ≠ current issuer retained`;
- `dormant ≠ retired`;
- `unused ≠ safe`;
- `drill passed once ≠ dormant path still current`;
- `WebCrypto API used ≠ underlying provider known`;
- `secure context ≠ product crypto inventory complete`;
- `platform-managed ≠ risk-owner absent`;
- `vendor attested ≠ tenant configured`;
- `provider supports PQC ≠ flow uses PQC`;
- `contract says retired ≠ runtime rejects retired`;
- `authentic inventory ≠ current inventory`;
- `PITR restored inventory ≠ current policy restored`;
- `fleet inventory says migrated ≠ unreachable device migrated`;
- `device absent from telemetry ≠ device absent`.

## OPEN
- actual MintTap/LogMate inventory schema, evidence sources, tooling and owners;
- actual SBOM/CBOM/dependency/build/runtime/provider/KMS/certificate coverage;
- actual shadow-crypto and SaaS/transitive dependency population;
- actual release gates and material-drift thresholds;
- actual retirement claims, negative-test enforcement points and regional/PITR coverage;
- actual offline/backup/export/recovery/historical-verifier inventories;
- actual WebKit/iPadOS/WebCrypto/MDM observable dependencies and provider behavior;
- actual long-offline fleet population and migration-tail handling;
- legal/aviation/privacy evidentiary and retention requirements;
- physical-device/runtime and human recovery/migration-state validation.

## CHANGE WATCH
- NIST CSWP 39upd1 revisions and crypto-agility maturity work;
- NCCoE Migration to PQC cryptographic-visibility/discovery outputs and SP 1800-38 progression beyond preliminary draft;
- CBOM/SBOM standards and government guidance relevant to cryptographic discovery;
- NIST PQC standards/transition guidance and cryptanalytic developments;
- browser/WebCrypto/WebKit/server/provider PQ support and defaults;
- provider cryptographic inventory/attestation capabilities.

## Gate result
**215 PASS (generic).** The Web Manager can now model a crypto inventory as a provenance-bearing, scoped and versioned evidence product; distinguish attestation integrity from completeness; discover/reconcile shadow crypto across multiple evidence planes; turn material inventory drift into governance signals; and build bounded retirement evidence without making an impossible universal-absence claim.

Production validation remains OPEN.

## Next highest-value adjacent question
**216 — crypto-inventory authority, exception/waiver lifecycle & release-gate bypass resistance.** Determine who may classify an unknown/legacy dependency as accepted, how time-bounded crypto exceptions are authorized without becoming permanent downgrade channels, how emergency release bypasses preserve evidence and mandatory re-convergence, and how expired waivers/old approvals are prevented from surviving rollback, provider migration or long-offline client return.