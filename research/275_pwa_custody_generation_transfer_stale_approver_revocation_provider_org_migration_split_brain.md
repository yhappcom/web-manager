# 275 — PWA Custody-Generation Transfer, Stale-Approver Revocation & Provider/Org Migration Split-Brain

Status: **PASS (generic) / PRODUCT + PERSONNEL + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline rejoin mechanics; Track B truthful migration/recovery UX; Track C destructive validation; Track D bounded migration diagnostics.  
Dependencies: 260–274 dependency/topology/re-entry/revocation/rotation/emergency-reset/recovery-root/custody-succession governance.

## Problem

274 established that recovery authority is a custody/dependency graph and that succession is an authority transition rather than a credential handoff. The adjacent failure occurs during overlap: old and new custodian sets, provider tenants, identity/control planes, legal organizations, or recovery workflows may coexist long enough that each side can appear locally valid. If both can independently declare themselves current, the organization has created an authority split-brain.

Central rule: **custody migration must converge on one current organizational authority generation without allowing old or new sides to self-elect merely because their credentials still work. Historical verification and unique offline data may survive the transition; consequence-bearing approval authority must be generation-scoped, explicitly admitted, and revocable.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Long-offline clients can retain old provider endpoints, Service Workers, sessions, caches and custody metadata; runtime reachability cannot elect an organizational generation.
- **B UX/IA/Content:** high dependency pressure. Migration UX must distinguish `records preserved`, `old approval no longer current`, `organizational migration incomplete`, `remote effects limited`, and `new authority established` without implying corruption.
- **C Performance/Accessibility/Quality:** destructive campaign expands **952 → 960 defined cases**. Execution, physical-device, AT and human PASS remain OPEN.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures old/new authority attempts, migration-tail size, provider/control-plane reachability, rejection evidence and unknown/offline cohorts; telemetry cannot choose the winner.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns custody-generation lineage, stale-approver revocation, migration admission, provider/org split-brain resolution, negative proof and rollback resistance.

## SOURCE

### NIST SP 800-57 Part 1 Rev. 5 — authorization-key lifecycle and replacement are explicit transitions

NIST key-management guidance treats key lifecycle state and replacement as explicit transitions. Active authorization/signature material does not remain valid for new protection indefinitely merely because verification material may remain useful for processing historical protected information. The transition is recorded, and replacement/deactivation/destruction semantics differ by key purpose.

Source: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**TRANSFER VALIDATION:** custody generations are broader organizational authority objects, not merely cryptographic keys. The reusable principle is explicit lifecycle/currentness: historical verification can outlive current consequence-bearing authority.

**CHANGE WATCH:** SP 800-57 Part 1 Rev. 6 remains an Initial Public Draft dated 2025-12-05; Rev. 5 remains final at this checkpoint.

### NIST SP 800-57 Part 2 Rev. 1 — institutional key management requires policy, roles and planning

NIST Part 2 addresses institutional key-management policy, practice statements, planning and centralized/decentralized structures. Organizational migration therefore cannot be reduced to copying key bytes or provider configuration.

Source: https://doi.org/10.6028/NIST.SP.800-57pt2r1

**TRANSFER VALIDATION:** this supports explicit organizational authority and role transition, not any specific MintTap/LogMate quorum or provider architecture.

### NIST SP 800-53 Rev. 5 AC-2/PS family — personnel/account transitions require account-state changes

NIST access-control/personnel controls treat transfer/termination and account management as lifecycle events; emergency/temporary/shared account handling and disabling conditions are not equivalent to leaving credentials valid indefinitely.

Source: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

**TRANSFER VALIDATION:** federal controls are not a universal PWA implementation prescription. The reusable principle is that role/personnel transition changes current authorization even if credentials technically continue to authenticate.

### RFC 6781 — trust-anchor rollover has overlap and ordering constraints

DNSSEC operational guidance shows that trust-anchor/key rollover is a staged transition with explicit introduction, overlap, revocation/removal ordering and distant-cache concerns. Old and new material can coexist temporarily without being permanently co-equal.

Source: https://www.rfc-editor.org/rfc/rfc6781

**TRANSFER VALIDATION:** DNSSEC timers/protocol are not PWA defaults. The reusable principle is that overlap needs lineage, precedence and retirement semantics, especially when clients can remain stale.

## SYNTHESIS 1 — generation is an authority claim, not a timestamp

Define a custody generation (or equivalent currentness object) as the organizationally admitted set of approvers/custodians, relevant provider/control-plane identity, recovery scope, consequence limits, predecessor relationship and admission evidence. A larger integer or later wall clock alone cannot establish it.

Guards:
- `newer timestamp ≠ current custody authority`;
- `higher generation number ≠ legitimate successor`;
- `provider says migration complete ≠ organizational authority transferred`.

## SYNTHESIS 2 — overlap is permitted; co-equal self-election is not

Migration may require old and new sets to coexist. During overlap, the system must know which consequences each generation may authorize and under what transition policy. Both sets remaining technically functional does not make both authoritative for all consequences.

Guards:
- `both credentials work ≠ both generations current`;
- `overlap required ≠ permanent dual authority`;
- `first responder ≠ authoritative responder`.

## SYNTHESIS 3 — successor admission must come from a trust path that survives the modeled failure

The new generation cannot establish legitimacy solely by asserting that it is new. Depending on the transition, admission may derive from the still-trusted predecessor plus independently governed organizational evidence, a pre-established recovery authority, or governed rebootstrap. If the predecessor is compromised, predecessor-only approval is insufficient.

Guards:
- `new side self-declares current ≠ successor admitted`;
- `old side signs successor ≠ sufficient when old side is compromised`;
- `migration API success ≠ authority admission proof`.

Actual MintTap/LogMate admission mechanism remains OPEN.

## SYNTHESIS 4 — stale approver revocation needs negative proof at material boundaries

Removing a person from the new roster is not enough if old credentials, provider sessions, admin APIs, background jobs or recovery paths still accept that person. Retirement requires evidence that obsolete approvers cannot produce material effects through consequence-bearing boundaries.

Guards:
- `removed from roster ≠ authority rejected`;
- `credential expired in one IdP ≠ all old sessions revoked`;
- `new quorum works ≠ old quorum harmless`.

Historical signatures may remain verifiable for provenance without preserving current approval authority.

## SYNTHESIS 5 — provider migration can create two control planes with different truths

During HSM/KMS/IdP/cloud-tenant migration, old and new providers may each hold valid-looking identities, keys, sessions and policy. Treat this as a topology/currentness problem. Provider reachability or successful signing does not choose the organizational winner.

Guards:
- `provider A reachable ≠ A current`;
- `provider B signs successfully ≠ B admitted`;
- `two healthy tenants ≠ one coherent authority`.

Migration design should establish a current organizational reference outside the ambiguity it is trying to resolve, or use governed rebootstrap if none survives.

## SYNTHESIS 6 — organizational migration and provider migration are separable axes

A legal/entity/team transition can occur without a provider move, and a provider move can occur without organizational authority change. Collapsing both into one flag hides partial completion and can accidentally transfer emergency mandate.

Guards:
- `tenant migrated ≠ organization reauthorized`;
- `organization reauthorized ≠ provider path proven`;
- `same human in both tenants ≠ same authority generation`.

## SYNTHESIS 7 — rollback resistance applies to custody state

PITR, backup restore, replica lag or offline clients can reintroduce an authentic but obsolete roster/provider generation. Currentness must survive those rollback paths. Restored historical state can be evidence; it must not automatically regain consequence-bearing authority.

Guards:
- `backup internally consistent ≠ custody current`;
- `old roster authentic ≠ old roster authorized now`;
- `PITR restored old tenant mapping ≠ old tenant reactivated`.

## SYNTHESIS 8 — long-offline clients are migration tails, not voters

An installed PWA can preserve old Service Worker code, endpoint configuration, sessions, queue payloads and custody metadata. On return it must not elect the old generation or force central rollback. Preserve unique records/provenance, fence stale high-consequence replay, obtain current generation evidence and reconcile queued operations individually.

Guards:
- `offline client arrives with old authority ≠ old authority resurrected`;
- `offline record created under old generation ≠ record deleted`;
- `old queue authentic ≠ current execution authorized`.

## SYNTHESIS 9 — split-brain detection is not split-brain resolution

Telemetry may detect simultaneous old/new approvals, mismatched provider generations or unexpected stale sessions. It cannot decide which side is legitimate. Resolution requires authority lineage/admission evidence and consequence-aware fencing.

Guards:
- `split-brain observed ≠ majority side wins`;
- `more events from new provider ≠ new provider authoritative`;
- `dashboard green on one side ≠ global convergence`.

## SYNTHESIS 10 — migration completion requires successor positive proof and predecessor negative proof

A meaningful closure bundle includes: successor generation admitted; required current quorum/provider path works; stale approvers rejected at material boundaries; obsolete provider/control-plane effects rejected or tightly bounded; backup/PITR cannot restore current authority backward; and long-offline clients rejoin through current admission rather than inheritance.

Guard: `new path PASS ≠ migration PASS`.

## SYNTHESIS 11 — partial convergence can support bounded operation

Not every client/provider replica must converge simultaneously before any operation resumes. Central authority can admit the new generation while stale clients remain offline, provided stale consequence-bearing paths are authoritatively fenced and safe preservation/read/recovery remains available. This avoids both unsafe dual authority and unnecessary destruction/total outage.

Guard: `fleet not converged ≠ all data/work must stop`; `bounded operation ≠ stale authority accepted`.

## SYNTHESIS 12 — emergency migration shortcuts create normalization debt

If business continuity requires a temporary bridge between old/new control planes, the bridge is an exception with scope, expiry, monitoring, independent review and retirement proof. It must not silently become the permanent authority architecture.

Guards:
- `temporary bridge works ≠ permanent architecture approved`;
- `migration finished operationally ≠ bridge retired`;
- `bridge unused recently ≠ bridge cannot authorize`.

## PWA / LogMate-like EFB application case

Scenario: recovery custody moves from organization/provider generation G7 to G8. Some custodians changed, the IdP/HSM tenant is being migrated, and a company iPad returns after six weeks offline with unique flight records, G7-era sessions, cached endpoints and queued operations.

Safe generic sequence:
1. preserve unique local records, queue payloads and provenance before authority cleanup;
2. establish whether G7 remains trusted enough to participate in planned transition or is itself suspect;
3. validate G8 admission through the appropriate surviving organizational trust path rather than G8 self-election;
4. bind G8 to the current custodian/quorum/provider/control-plane scope and transition lineage;
5. fence G7 high-consequence effects at authoritative server/admin/recovery boundaries while retaining historical verification where needed;
6. invalidate or revalidate stale approver sessions/tokens according to current policy; do not rely on roster deletion alone;
7. reconcile provider/org migration axes separately so a tenant move does not silently transfer emergency mandate;
8. treat the returning iPad as a stale migration tail: preserve data, obtain current bootstrap/generation, reconcile runtime/schema/session/device state, and revalidate queued operations individually;
9. prove G8 positive operation and G7 negative rejection, including backup/PITR and manual/admin paths;
10. retire temporary migration bridges and record residual exceptions before declaring convergence.

This is a generic architecture pattern. It does **not** establish that LogMate uses a particular HSM, KMS, IdP, quorum, MDM, provider, tenant or aviation-security architecture.

## Cross-track transfer

### Track A — Platform/Browser
**DEPENDENCY:** Service Worker/IndexedDB/Cache Storage/session persistence can preserve obsolete endpoints and generation metadata. Browser freshness does not establish custody currentness. Runtime migration and authority migration are separate gates.

### Track B — UX/IA/Content
**TRANSFER VALIDATION:** distinguish `records safe`, `remote approval temporarily limited`, `organization/provider migration in progress`, `old approval no longer current`, and `recovery restored`. Avoid telling users that preserved offline records are corrupt merely because authority changed. Human/AT validation remains OPEN.

### Track C — Quality / destructive campaign
Add eight defined cases:
1. **Old/new self-election split-brain** — both generations claim current; neither wins from local assertion alone.
2. **Roster-only stale-approver removal** — former approver disappears from UI but old session/admin path still works; migration remains open.
3. **Provider-signing-equals-authority theater** — new HSM/KMS signs successfully before organizational admission; do not promote.
4. **Tenant-transfer mandate laundering** — cloud/IdP tenant move succeeds and emergency mandate is silently inherited; reject.
5. **PITR custody rollback** — restore revives G7 roster/provider mapping after G8 admission; current authority must remain G8 or enter governed recovery, not roll back automatically.
6. **Offline-iPad G7 resurrection** — returning PWA presents authentic G7 metadata/queue; preserve records but reject stale authority inheritance.
7. **Successor-only migration PASS** — G8 works while G7 admin/background path still produces effects; migration gate remains open.
8. **Temporary-bridge permanence** — migration bridge remains consequence-bearing after declared completion; require explicit retirement/review.

Campaign total: **960 defined cases**. This is definition coverage, not execution PASS.

### Track D — Discovery/Analytics
**DEPENDENCY:** measure old/new generation attempts, stale-approver use, provider reachability, rejection outcomes, migration-tail size, bridge use and unknown/offline cohorts. Telemetry is challenger evidence; it cannot elect a generation or transfer organizational mandate.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate-like web/PWA requirements:
- represent custody/provider/org authority with explicit currentness/generation or equivalent lineage evidence rather than wall-clock recency;
- permit planned overlap only with explicit consequence scope, predecessor/successor relation and retirement criteria;
- revoke stale approvers at material effect boundaries, not only in rosters;
- keep provider migration and organizational-authority migration as separate state dimensions;
- preserve historical verification and unique offline data while denying obsolete current authority;
- require successor positive proof plus predecessor negative proof before declaring migration closed;
- make backup/PITR and long-offline rejoin anti-rollback obligations part of migration design;
- treat temporary cross-provider/control-plane bridges as bounded exceptions with retirement proof;
- do not infer actual MintTap/LogMate personnel, provider, HSM, MDM or legal topology without canonical production evidence.

## OPEN

Product-specific validation remains OPEN for actual custodian roster/quorum, provider/IdP/HSM/KMS topology, tenant/org migration semantics, legal mandate, session/token revocation, backend/admin/manual/background boundaries, generation storage and anti-rollback reference, backup/PITR, managed-iPad/WebKit behavior, long-offline queue semantics, physical-device/AT/human testing, and aviation/investment/security/privacy obligations.

## VALIDATION / gate

**275 PASS (generic)** because the study now distinguishes overlap from co-equal authority, provider migration from organizational migration, successor admission from self-election, stale-approver roster removal from consequence revocation, detection from resolution, and historical/offline preservation from current authority. Production/runtime validation remains OPEN.

## Adjacent next target

**276 — migration-bridge authority minimization, cross-provider session/token invalidation & convergence-completion proof.** Determine how a temporary bridge can support migration without becoming a transitive super-authority; how old/new IdP/provider sessions, refresh tokens and background credentials are invalidated across partial convergence; and what evidence closes migration when long-offline clients may return later.