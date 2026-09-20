# 191 — PWA Continuity-Custody Compromise, Escrow Poisoning & Recovery-Package Freshness/Anti-Rollback

Status: **PASS (generic) / PRODUCT + PROVIDER + CRYPTO + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A offline/reconnect mechanics; Track B degraded/recovery UX; Track C destructive validation; Track D privacy-bounded continuity telemetry.
Dependencies: 183–190 exact-artifact lineage, transparency, archive/preservation integrity, provider exit, portability proof, escrow independence and uncooperative-provider recovery.

## Problem
190 established that portability is demonstrated recovery rather than an export feature. The adjacent failure is more adversarial: an independently held continuity package can itself be stale, rolled back, selectively truncated, poisoned, replaced, or made unavailable by compromise of its custodian. Independence from the incumbent therefore does not prove correctness or freshness of the continuity copy.

Central rule:

> **Continuity custody is a survivability/evidence plane, not a current-authority plane. A recovery package is usable only within an authenticated lineage and freshness scope that survives both incumbent and custodian failure; possession, readability or immutability alone does not establish currentness.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. HTTP/cache/SW/IndexedDB and client clocks can retain observations but cannot determine recovery-package currentness.
- **B UX/IA/Content:** high-pressure consumer. Owns distinguishable states for local work preserved, recovery package stale/uncertain, reconciliation required, and remote consequence-bearing work paused.
- **C Performance/Accessibility/Quality:** validator. Owns rollback, poison, split-custody, expiry, long-offline and operator/AT campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Freshness telemetry must avoid raw evidence and stable user/device/flight dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns continuity generation, authenticated lineage, anti-rollback, custody compromise/reconstitution and recovery admission boundaries.

## SOURCE
### The Update Framework — rollback/freeze design precedent
TUF separates signed roles and metadata. Snapshot metadata binds versions/hashes of repository metadata so an attacker cannot safely mix files from different repository states; timestamp metadata binds the current snapshot, is frequently renewed, and expires quickly. TUF documentation states that clients can reject metadata older than previously observed metadata. This is software-update precedent, not a preservation-service standard, but it supplies a strong reusable distinction between integrity, consistent-set binding, freshness and rollback/freeze resistance.

Sources:
- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/faq/

### CISA #StopRansomware recovery guidance
CISA recommends offline encrypted backups, regular availability/integrity testing, delete protection/object lock where supported, versioning, and recovery onto clean systems. The transferable principle is that copies must survive correlated compromise and be tested; immutability alone does not prove that the immutable object was the right generation before it was locked.

Source: https://www.cisa.gov/stopransomware/ransomware-guide

## SYNTHESIS — integrity, completeness, freshness and authority are separate
A continuity package can be:
1. byte-integrity-valid but stale;
2. authentic for generation G but incomplete for G;
3. complete/authentic for G but superseded by G+1;
4. current-looking but poisoned before signing/custody;
5. current and authentic as historical recovery evidence but still not current business/admission authority.

Persistent guards:
- `escrow immutable ≠ escrow correct`;
- `escrow authentic ≠ escrow fresh`;
- `escrow fresh ≠ escrow complete`;
- `highest local version ≠ globally current version`;
- `newest client timestamp ≠ authoritative freshness`;
- `package generation number present ≠ generation number trustworthy`;
- `custodian signed receipt ≠ package semantics authorized`;
- `two custody copies agree ≠ two independent failure domains agree`;
- `old package is last surviving copy ≠ old package becomes current authority`;
- `restore from G succeeds ≠ G may overwrite surviving G+1 state`;
- `immutability enabled ≠ poisoning before lock impossible`;
- `custody reconstituted ≠ compromise-era package becomes known-good`.

## Authenticated continuity-generation model
A generic package should be interpretable against an authenticated lineage rather than a naked integer or wall-clock timestamp. The lineage may need, subject to product/crypto design:
- exact package/artifact identity and manifest digest;
- continuity generation/epoch;
- predecessor identity or authenticated transition evidence;
- applicable provider/policy/key/schema/verifier generations;
- creation/admission evidence and declared completeness scope;
- retention/hold/deletion state relevant to restore;
- independent receipt/checkpoint evidence where available;
- compromise/retirement markers and UNKNOWN intervals.

The package must not be considered fresh merely because a mutable manifest says `generation=latest` or because its filesystem/object timestamp is newest.

## Anti-rollback without making the incumbent sole oracle
The incumbent cannot be the only source of `latest` because 190 specifically requires survival of incumbent disappearance. Conversely, the escrow custodian cannot be the only freshness oracle because this study assumes custodian compromise.

Generic strategy:
1. bind each accepted continuity generation to authenticated package identity and predecessor/currentness evidence;
2. retain bounded independent observations/checkpoints outside the ordinary incumbent and custody mutation path where feasible;
3. compare candidate restore generation against every surviving authenticated higher security/policy/provider/deletion/hold floor;
4. treat contradictory valid-looking heads as conflict/incident evidence, not as a majority vote;
5. never lower a surviving floor solely because an older package is the only readable package;
6. after restore, reconcile rather than blindly replace any independently surviving newer state.

This is analogous to TUF's separation of snapshot consistency and timestamp freshness, but it is not a claim that TUF itself is the correct preservation architecture.

## Freeze, rollback and mix-and-match failures
Three failure classes must be distinguished:
- **rollback:** attacker substitutes an older authentic package or metadata generation;
- **freeze:** attacker prevents observation of newer generations so an old generation continues to appear current;
- **mix-and-match/splicing:** individually authentic components from different generations are assembled into a package that never existed as an admitted whole.

A single package hash can detect post-package mutation but cannot prove that the package was the latest admitted package. Per-object signatures can still permit splicing unless a signed manifest/snapshot-like object binds the intended set and applicable versions together.

## Custody compromise and reconstitution
When continuity custody is suspected compromised:
1. stop treating that custody domain as fresh evidence producer;
2. preserve existing packages, receipts, logs and conflicting heads as incident evidence;
3. identify the earliest defensible compromise boundary; if unavailable, widen UNKNOWN rather than invent precision;
4. compare independently retained package identities/checkpoints and surviving provider/security/policy floors;
5. reconstitute custody under a new generation and independently governed credentials/keys/deletion path;
6. import only packages whose provenance and scope can be bounded;
7. preserve compromise-era uncertainty explicitly;
8. do not let the compromised custodian solely sign its own successor as trusted;
9. rerun incumbent-independent restore/validation before calling portability recovered.

Credential/key rotation alone does not prove custody reconstitution if poisoned packages or rolled-back manifests survive.

## Poisoning before immutability
Object lock/WORM/immutable storage is valuable against later overwrite/deletion, but a malicious or compromised export pipeline can deposit poisoned content before the retention lock applies. Therefore package admission needs semantic/completeness validation and exact manifest binding before or as part of continuity acceptance. `WORM` is a mutation property, not provenance.

## PITR / restore anti-rollback
A point-in-time restore may resurrect:
- an older continuity-generation registry;
- retired provider/key/policy state;
- already-satisfied deletion/hold states;
- an old package marked `current`;
- obsolete custodian credentials;
- monitor state from before a conflict.

Restored state must reconcile against surviving external/current floors. A database that is internally self-consistent after PITR is not thereby current.

## PWA / EFB boundary
A long-offline company iPad can return carrying local records plus cached provider roots, package/checkpoint observations, Service Worker code and IndexedDB state from generation G while server/custody has advanced to G+n.

Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. classify cached continuity/provider material as historical observation only;
3. obtain current authenticated server security/preservation/continuity generation when connectivity exists;
4. detect whether the client skipped provider/custody/security generations;
5. reconcile acknowledged historical records against the recovered authoritative lineage;
6. keep missing/compromise-era evidence UNKNOWN where necessary;
7. submit local-only work under current authority rather than manufacturing predecessor acknowledgements;
8. re-admit queued consequence-bearing operations only after current authorization/reconciliation.

Do not use the iPad wall clock, highest cached integer, Service Worker cache age or `navigator.onLine` as authority/currentness evidence. Physical Safari/Home Screen/managed-iPad behavior remains OPEN.

## UX / accessibility transfer
Recovery UI must not collapse these into one generic `backup available` state:
- local data preserved;
- continuity package found;
- package integrity verified;
- package freshness unresolved;
- package conflict detected;
- historical verification incomplete;
- recovery/reconciliation in progress;
- remote submission paused.

Status must remain perceivable without color alone and must not encourage an operator to choose `newest-looking` package by timestamp. Exact interaction design remains Design Studio-owned and human/AT validation remains OPEN.

## Privacy / telemetry boundary
Freshness/checkpoint telemetry should prefer low-cardinality generation/digest/status evidence over raw flight/user/device payloads. Independent observations should not become stable-device tracking beacons. Recovery copies, temporary restore environments and conflict evidence remain subject to retention/deletion/legal-hold governance.

## Track C destructive campaign
Define a **288-case generic campaign**, extending 190's 280-case baseline with at least these adjacent cases:
- immutable custody contains a package poisoned before lock;
- authentic G replaces G+2 after custody credential compromise;
- manifest generation is edited while object digests remain valid;
- individually authentic objects from G/G+1 are spliced into a never-admitted package;
- timestamp/clock manipulation makes stale package appear newest;
- incumbent unavailable and custodian falsely asserts `latest`;
- two nominally independent custodians share compromised IdP/KMS/deletion authority;
- PITR resurrects old continuity registry/current marker;
- deletion/hold floor regresses with package restore;
- custodian key rotation leaves poisoned package set untouched;
- freeze attack suppresses observation of newer continuity generations;
- conflict monitor is unavailable during split custody;
- long-offline iPad returns with higher-looking local generation but stale authority;
- stale Service Worker drains queue before currentness reconciliation;
- local-only records are overwritten by older remote restore;
- screen-reader/operator cannot distinguish `package verified` from `package current`;
- urgency causes selection by newest wall-clock timestamp;
- recovery telemetry leaks stable device/flight identity.

Campaign definition is not execution. Physical device, browser, provider, crypto, AT and representative-human evidence remain OPEN.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** TUF demonstrates a mature security design that treats signed integrity, consistent snapshot binding, metadata versioning and expiration/freshness as distinct defenses. Transfer only the security distinction, not the software-update architecture wholesale.
- **TRANSFER VALIDATION:** CISA backup guidance reinforces offline/immutable/versioned/tested recovery and correlated-failure resistance.
- **CONTRADICTION:** `immutable backup` language must not be interpreted as proof of semantic correctness, freshness or provenance; poisoning can precede immutability.
- **CONTRADICTION:** multiple copies do not create a vote-based authority system.

## MINTTAP DECISION / DIRECTION
For generic Web Manager/PWA guidance:
1. treat continuity custody as evidence/survivability, never current authority by possession;
2. model continuity generation and exact package identity separately from wall-clock time;
3. require authenticated set binding to prevent mix-and-match recovery packages;
4. preserve independent higher-floor observations/checkpoints where practical so incumbent and custodian are not sole freshness oracles;
5. reconcile PITR/restore against surviving current security/policy/provider/deletion/hold floors;
6. reconstitute custody after compromise rather than merely rotating credentials;
7. preserve unique offline local operational data even while remote consequence-bearing work remains paused;
8. keep product-specific topology, algorithms, key hierarchy, quorum and retention choices OPEN until implementation/provider/legal evidence exists.

## OPEN / DEPENDENCY / VALIDATION
OPEN:
- actual MintTap/LogMate continuity provider/custodian topology;
- exact package/manifest/schema/key/signature/checkpoint design;
- actual provider export and immutability semantics;
- managed-iPad/WebKit offline storage/update/reconnect behavior;
- legal/aviation retention and deletion constraints;
- actual backup/PITR/restore and queue behavior;
- representative human/AT recovery comprehension.

DEPENDENCY:
- Software Engineering owns implementation of package manifests, parsers, verifier isolation, storage/key hierarchy, restore mechanics and test harnesses when product source/runtime becomes available.
- Design Studio owns reusable recovery-state interaction/visual design and human validation.

VALIDATION:
- execute the 288-case destructive campaign on real provider/runtime architecture;
- perform incumbent-independent and custodian-compromise restore drills;
- verify physical iPad/Safari/Home Screen behavior and accessibility;
- verify deletion/hold/privacy behavior across recovery copies.

## CHANGE WATCH
- TUF specification/metadata guidance and implementation security guidance;
- CISA/NIST backup/recovery guidance;
- provider-specific immutable/object-lock/versioning semantics;
- WebKit/iPadOS PWA storage/background/update behavior.

## Gate
**PASS (generic).** Web Manager can distinguish package integrity, authenticity, completeness, freshness, set consistency and current authority; diagnose rollback/freeze/mix-and-match and custody poisoning; specify compromise/reconstitution and PWA convergence boundaries without inventing product facts.

Production certification remains OPEN.