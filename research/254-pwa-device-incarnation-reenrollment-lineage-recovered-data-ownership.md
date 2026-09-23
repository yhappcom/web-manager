# 254 — PWA Device-Incarnation Identity, Re-enrollment Lineage & Recovered-Data Ownership Transfer

Status: **PASS (generic) / PRODUCT + MDM + MANAGED-IPAD + DATA-OWNERSHIP + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/storage/enrollment mechanics; Track B recovery/transfer UX; Track C destructive incarnation/transfer validation; Track D incarnation-aware fleet measurement.  
Dependencies: 137, 171–253, especially identity/currentness, retirement/resurrection, recovery bootstrap, anti-rollback, provenance and unique-data preservation.

## Problem
253 established that same hardware after erase/re-enrollment may be a new administrative incarnation, and that a returning retired device can carry valuable data without carrying current authority. The adjacent problem is to define what identifies an incarnation, how old and new incarnations may be linked without authority splicing, and how recovered offline data is attributed and transferred when the old user/device authority is retired.

Central rule: **hardware continuity, enrollment continuity, authority continuity and data continuity are separate claims. Prove only the continuity needed for the operation. A new enrollment gets new current authority; recovered historical data crosses the boundary through provenance-preserving quarantine/admission, not by reviving the old incarnation.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns browser storage/Service Worker persistence/reset behavior and platform enrollment/key mechanics. It can establish what bytes/keys may survive or be destroyed, not organizational ownership.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `OLD-INCARNATION`, `NEW-INCARNATION`, `RECOVERED-DATA-QUARANTINED`, `ATTRIBUTION-UNRESOLVED`, `TRANSFER-APPROVAL-REQUIRED` and `ADMITTED-HISTORICAL-DATA` states without presenting old authority as restored.
- **C Performance/Accessibility/Quality:** high dependency pressure. Campaign expands **784 → 792 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. Counts administrative incarnations separately from physical assets and preserves reason-coded predecessor/successor transitions. Analytics cannot elect identity or ownership.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns incarnation binding, authority/key rotation, quarantine, provenance-preserving data transfer, re-admission and closure.

## SOURCE

### Apple Managed Device Attestation — hardware identity and enrollment-bound keys are distinct evidence
Apple documents Managed Device Attestation for supported Apple devices. An ACME enrollment can create a hardware-bound private key in the Secure Enclave and allow a relying CA/service to validate device properties. Apple also states that hardware-bound keys are removed by erase/restore and must be recreated; DeviceInformation attestation keys are reused for the lifetime of the enrollment. A fresh attestation can be requested with a nonce.

Sources:
- https://support.apple.com/en-gb/guide/deployment/dep28afbde6a/1/web/1.0
- https://support.apple.com/en-ie/guide/security/sec97eb9e2f2/web
- https://support.apple.com/en-ca/guide/deployment/dep54e5ac1fd/web

**TRANSFER VALIDATION:** this is strong platform precedent for separating durable hardware properties from enrollment/key lifetime. It does not prove that LogMate uses Managed Device Attestation, ACME, a particular MDM, or any device certificate.

### Apple Return to Service — erase and re-enrollment are explicit lifecycle transitions
Apple documents Return to Service as secure erasure followed by enrollment/configuration for the next operational use. Current iOS/iPadOS versions can preserve managed app binaries in supported configurations while securely erasing previous-user data; this does not preserve previous-user authority or user-generated app data.

Source:
- https://support.apple.com/en-sa/guide/deployment/dep17cb455a0/1/web/1.0

**CHANGE WATCH:** Return-to-Service details are OS/version/enrollment specific and must be rechecked for the actual managed-iPad deployment.

### Apple enrollment/data separation — management identity is not restored by backup
Apple documents that device-management enrollment uses certificate identities; removing enrollment removes associated managed configurations/apps, and restoring from backup does not restore device-management enrollment. Account-driven enrollment also uses cryptographic separation of organizational data and destroys relevant separation keys on unenrollment.

Sources:
- https://support.apple.com/guide/deployment/intro-to-device-management-depc0aadd3fe/1/web/1.0
- https://support.apple.com/en-ae/guide/deployment/dep4d9e9cd26/web

**TRANSFER VALIDATION:** platform-specific evidence supporting new-enrollment/new-authority separation; not a generic PWA storage guarantee.

### NIST SP 800-63B-4 — new authenticator binding and invalidation are lifecycle events
Current NIST SP 800-63B treats binding a new authenticator, account recovery and authenticator invalidation as explicit lifecycle operations. Recovery permits new authenticators to be bound after recovery; invalidation removes the binding between an authenticator and subscriber account.

Source:
- https://pages.nist.gov/800-63-4/sp800-63b.html

**TRANSFER VALIDATION:** bounded identity-lifecycle precedent. Device-management enrollment is not identical to subscriber authentication, but the separation between old authenticator invalidation and new authenticator binding is directly useful.

### Cross-repository evidence
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED** with physical-device/PWA, screen-reader and representative-human evidence OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**; bounded Safari Service Worker lifecycle evidence exists, while installed-PWA/physical iOS/iPadOS/EFB and canonical-product runtime remain OPEN.

**DEPENDENCY:** generic incarnation/data-transfer reasoning cannot upgrade those runtime/design gates.

## SYNTHESIS 1 — model physical asset and administrative incarnation separately
A useful model separates at least:
- `physical_asset_id` — hardware/inventory identity where legitimately available;
- `incarnation_id` — one governed enrollment/installation/authority epoch;
- `principal_assignment` — user/crew/organization assignment for that epoch;
- `authority_set` — current certificates/tokens/keys/session bindings;
- `policy/schema generation`;
- predecessor/successor relation with reason.

Serial/UDID/hardware attestation can support a hardware claim in applicable deployments, but **hardware identity is not incarnation identity**.

Guards: `same serial ≠ same incarnation`; `same hardware attested ≠ same enrollment`; `same user ≠ same device authority`.

## SYNTHESIS 2 — re-enrollment creates a new authority epoch
Erase/restore can destroy hardware-bound enrollment keys, and Apple documents new certificate identity enrollment. Therefore a re-enrolled device should not inherit old authority merely because hardware continuity is proven.

Create a successor incarnation with new authority material and current policy/bootstrap. Preserve an explicit predecessor relation only where justified.

Guards: `predecessor known ≠ predecessor authority inherited`; `re-enrolled ≠ reactivated`; `hardware continuity ≠ credential continuity`.

## SYNTHESIS 3 — attestation proves bounded properties, not ownership
Managed Device Attestation can provide strong evidence about device properties and enrollment-bound keys. It does not by itself prove which employee owns a recovered record, that an old user assignment remains valid, or that local PWA data is semantically legitimate.

Guard: `device attested ≠ data ownership proven`; `key hardware-bound ≠ record business-authorized`.

## SYNTHESIS 4 — continuity is claim-specific
Do not collapse continuity into one boolean. A recovery may prove:
1. physical hardware continuity;
2. historical incarnation identity;
3. record provenance/creation continuity;
4. organizational custody continuity;
5. user/principal continuity;
6. current authority continuity.

These can differ. Example: same iPad, same organization, new user, new enrollment, old unique flight records awaiting transfer.

Guard: `some continuity proven ≠ all continuity proven`.

## SYNTHESIS 5 — recovered data crosses an authority boundary through quarantine
When data from a retired incarnation is recovered after the new incarnation exists, do not copy it directly into the current trusted projection. Preserve original bytes/evidence where feasible, identify source incarnation, mark authority/currentness state, and place it in a quarantine/import workflow.

Minimum transfer record should bind:
- source incarnation and known principal/assignment;
- recovery method/time/operator;
- source policy/schema/verifier generation;
- content/provenance identity;
- custody/transformations performed;
- target account/incarnation/domain object;
- approving authority and rationale;
- resulting admission status and successor relation.

Guard: `data copied ≠ data admitted`; `data admitted ≠ old authority restored`.

## SYNTHESIS 6 — attribution and ownership are different questions
A record may be attributable to an old device/incarnation yet its organizational ownership, user entitlement or target account may be unresolved. Preserve provenance while holding `ATTRIBUTION-UNRESOLVED` / `OWNERSHIP-TRANSFER-PENDING` rather than assigning by convenience.

Guard: `source identified ≠ rightful target established`; `same employee name ≠ same account/principal identity`.

## SYNTHESIS 7 — transfer must not rewrite authorship
If historical record R was created under old incarnation I12 and later admitted under I20, the current system may record import/recovery/admission by I20 or an operator, but must not rewrite R as if I20 authored it originally.

Guard: `imported by successor ≠ authored by successor`; `current signature ≠ original authorship`.

## SYNTHESIS 8 — old authority is never the transfer credential
The retired certificate/token/key should not be temporarily re-enabled to authenticate recovered data. Historical signatures/provenance may be verified in a bounded historical path, but current transfer approval comes from current governance/identity.

Guard: `historical verifier support ≠ old credential reactivation`; `recovery convenience ≠ authority rollback`.

## SYNTHESIS 9 — identifier reuse must not collapse incarnations
An MDM/provider/backend may expose stable-looking identifiers. If an identifier can be reused, restored, reissued or scoped differently across enrollment modes, it cannot alone serve as an eternal incarnation key. Bind incarnation identity to explicit lifecycle/generation evidence rather than one friendly identifier.

Guard: `identifier equal ≠ lifecycle equal`; `inventory match ≠ authority lineage proven`.

## SYNTHESIS 10 — privacy constrains identity collection
Apple User Enrollment intentionally withholds some hardware identifiers. Generic design must therefore not require universal serial/UDID collection. Use the minimum identity evidence needed for the deployment and consequence; preserve privacy boundaries between personal and organizational contexts.

Guard: `stronger tracking ≠ stronger governance`; `identifier unavailable ≠ invent fingerprinting workaround`.

## SYNTHESIS 11 — PWA local storage has its own identity boundary
A Home Screen/web PWA's local storage, Service Worker and cached application state are web-origin/browser/OS artifacts, not MDM enrollment authority by themselves. Even if bytes survive some lifecycle path, they do not establish current incarnation identity. Conversely, platform erase/managed-app behavior cannot be assumed to describe Safari/Home-Screen PWA persistence without physical/runtime evidence.

Guards: `local PWA state survives ≠ enrollment survived`; `enrollment renewed ≠ PWA lineage migrated`; `managed-app data behavior ≠ PWA storage behavior`.

## SYNTHESIS 12 — new incarnation should start with a current bootstrap, not an inherited floor guess
The successor incarnation obtains current organizational bootstrap/policy through current trusted channels. Historical checkpoint/policy from the predecessor remains evidence for interpreting recovered data, not a floor that automatically transfers to the successor or a reason to downgrade current policy.

Guard: `old checkpoint present ≠ successor bootstrap complete`.

## SYNTHESIS 13 — data continuity can be preserved without authority continuity
This is the principal LogMate/EFB requirement. Unique offline flight/logbook data may legitimately need to cross from I12 to I20 while I12's credential remains revoked forever. Preserve provenance, migrate schema, resolve conflicts/ownership and admit records under current policy.

Guard: `authority discontinuity ≠ data must be discarded`; `data continuity ≠ authority continuity`.

## SYNTHESIS 14 — authority continuity, where required, needs explicit successor proof
Some deployments may intentionally rotate credentials without changing assignment/incarnation semantics. If so, continuity must be demonstrated by an authorized rotation/binding ceremony or equivalent current control-plane evidence, not inferred from same hardware/account/name.

NIST authenticator lifecycle is useful precedent: binding a replacement authenticator and invalidating the old are explicit events.

Guard: `replacement key exists ≠ successor relation proven`.

## SYNTHESIS 15 — closure needs negative splice tests
A correct successor path should prove both positive continuity and negative separation:
- old credential cannot authenticate current mutation;
- same serial cannot inherit old user assignment automatically;
- restored backup cannot restore enrollment authority;
- recovered records retain old authorship/provenance;
- target admission requires current authorization;
- current incarnation cannot silently rewrite retirement history;
- old local Service Worker/cache cannot elect current identity;
- unresolved ownership does not become default-owner assignment.

Guard: `successor works ≠ predecessor is safely retired`.

## PWA / LogMate-like EFB application
For a retired company iPad recovered with unique offline logbook data and then returned to service:

1. **Freeze destructive action until preservation decision:** if unique data may exist, do not erase merely to simplify re-enrollment.
2. **Quarantine old incarnation:** block old sync/mutation authority; preserve/export local records and provenance using an approved recovery path.
3. **Establish current device/organization state independently:** perform current enrollment/bootstrap/attestation as applicable; create a new incarnation and new current credentials.
4. **Link, do not merge, identities:** record `I12 → I20` successor/rejoin relation where supported by evidence; keep old retirement intact.
5. **Resolve data attribution/ownership:** map recovered records to the correct pilot/account/organizational domain using product/business evidence, not serial number alone.
6. **Verify/migrate:** evaluate historical provenance with bounded historical verifiers, migrate schema/data, retain transformations.
7. **Admit per record/operation:** current policy decides acceptance/conflict/correction; current admission metadata does not replace original authorship.
8. **Close only with negative evidence:** confirm I12 credentials/policy cannot regain mutation authority and I20 cannot silently claim I12 authorship.

**OPEN:** actual LogMate user/account/device/incarnation identifiers, company iPad ownership model, MDM/ADE, PWA storage, export/recovery, data ownership, credential/key rotation and backend admission semantics are unknown until canonical product/runtime evidence exists.

## Track C destructive additions — 784 → 792
Add eight defined cases:
1. **Serial-number authority splice:** new enrollment inherits old credential/assignment because hardware serial matches.
2. **Attestation ownership laundering:** valid device attestation treated as proof that recovered records belong to the current user.
3. **Backup-enrollment resurrection:** restored backup/local state treated as restoring old MDM/PWA authority.
4. **Recovered-data direct admission:** old-incarnation records copied directly into current projection without quarantine/provenance/current policy.
5. **Successor authorship rewrite:** imported historical records rewritten as authored by the new incarnation.
6. **Retired-credential transfer:** old credential temporarily reactivated to authorize import/sync.
7. **Identifier-reuse collapse:** provider-friendly ID equality merges two distinct enrollment epochs.
8. **Unresolved-owner defaulting:** recovered records assigned to the currently logged-in user merely because attribution evidence is incomplete.

**VALIDATION:** these are defined destructive oracles, not executed product tests. Campaign total: **792 defined cases; execution PASS not claimed**.

## MINTTAP DECISION / generic operating direction
- Separate physical asset, administrative incarnation, principal assignment, authority set and data provenance.
- Treat erase/re-enrollment as a new authority epoch unless explicit authorized rotation evidence establishes a narrower continuity claim.
- Never use hardware continuity or attestation alone to prove data ownership/current authorization.
- Recover old-incarnation data through provenance-preserving quarantine and current-policy admission; never revive retired authority to move data.
- Preserve original authorship while recording current recovery/import/admission actions separately.
- Use privacy-minimized identifiers appropriate to the enrollment model; do not compensate for unavailable platform identifiers with covert fingerprinting.
- Keep physical iPadOS/WebKit/PWA persistence, MDM/provider identity semantics and product data-ownership rules OPEN until executed/canonical evidence exists.

## OPEN / DEPENDENCY / CHANGE WATCH
- **OPEN:** actual MintTap/LogMate physical asset IDs, incarnation IDs, user/account/crew assignment, MDM/ADE/Apple Business use, Managed Device Attestation/ACME use, credential/token/key lifecycle, PWA storage identity, recovered-data ownership and import/admission model.
- **OPEN:** physical iPadOS/WebKit Home-Screen PWA behavior across erase/re-enrollment/restore and actual managed-network flows.
- **DEPENDENCY:** Software Engineering owns implementation-level identifier/key/schema/import/sync mechanics when canonical product source/runtime is authorized.
- **DEPENDENCY:** Design Studio owns reusable recovery/transfer interaction quality; Web Manager supplies state and trust-boundary requirements.
- **CHANGE WATCH:** Apple deployment, Managed Device Attestation, Return to Service and enrollment/privacy behavior are platform/version/provider specific.

## Gate result
**254 PASS (generic).** The Web Manager can now separate hardware, administrative incarnation, principal assignment, authority and data continuity; reason about re-enrollment without serial-number authority splicing; and define provenance-preserving recovered-data transfer without reviving retired authority. Product/MDM/managed-iPad/data-ownership/runtime validation remains OPEN.

## Next high-value target
**255 — recovered-data conflict authority, principal reassignment & duplicate/replay-safe admission.** Determine how recovered old-incarnation records interact with already-synced/current records; how principal reassignment is authorized without rewriting authorship; how dedup/identity survives schema/incarnation changes; and how an attacker cannot replay the same recovered package through multiple successor incarnations or recovery operators.