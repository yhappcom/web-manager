# 208 — PWA Recovery-Anchor Custody Succession, Organizational/Provider Loss & Bootstrap Survivability

Status: **PASS (generic) / PRODUCT + RECOVERY-CUSTODY + APPLE-BUSINESS/MDM + MANAGED-IPAD + RUNTIME + SECURITY/LEGAL + HUMAN VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A platform/provisioning mechanics; Track B recovery UX; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–207, especially 205–207.

## Problem
207 separated recovery-anchor authorization from WebPKI/CDN/MDM/support/bootstrap distribution. The adjacent survivability problem is organizational: recovery authority may be cryptographically intact while its custodians, company identity/admin plane, MDM tenant/provider, Apple Business access, enrollment integration, PKI, or ordinary control plane becomes unavailable. A design that survives key compromise but cannot survive loss of the people/provider/account needed to use the key is not operationally recoverable.

Central rule: **custody survivability, provider survivability, bootstrap distribution and recovery authorization are distinct properties. Preserve enough independently governed recovery capability to reconstitute current authority without making an always-online provider/admin plane a super-root, and never interpret provider outage or personnel loss as permission to weaken the admitted recovery policy.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Apple enrollment/management and PWA/browser mechanisms constrain how managed iPads can be reprovisioned, but do not define constitutional recovery authority.
- **B UX/IA/Content:** high dependency pressure. Must distinguish `MANAGEMENT MIGRATION REQUIRED`, `RECOVERY CUSTODY UNAVAILABLE`, `LOCAL DATA PRESERVED`, `REMOTE AUTHORITY QUARANTINED`, `RE-ENROLLMENT REQUIRED`, and `RECOVERY BLOCKED` without implying data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **424 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Inventory/migration/adoption telemetry can reveal drift but cannot elect replacement custodians/providers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns custody succession, provider/control-plane loss, survivability topology, recovery ceremony and extinction/convergence evidence.

## SOURCE

### Apple — current device-management migration capability
Apple Platform Deployment, published 2026-09-17, documents migration of managed devices to another device-management service for supported devices. Current requirements include iOS/iPadOS/macOS 26 or later and Automated Device Enrollment for the main organization-owned path. Apple documents migration deadlines, reenrollment, preservation of managed apps/data in specified conditions, and notes unsupported cases such as Shared iPad. Apple also documents planning work: inventory dependencies such as IdP, PKI, network, app distribution, access management, monitoring, asset management, APNs and Apple Business/School Manager; recreate enrollment/configuration; test; then migrate.

Sources:
- https://support.apple.com/guide/deployment/dep4acb2aa44/web
- https://support.apple.com/guide/deployment/plan-your-device-management-migration-depa5bf97586/1/web/1.0

**TRANSFER VALIDATION:** provider migration is a real current Apple platform capability for qualifying deployments, and Apple explicitly treats migration as dependency-rich operational work. This does not establish LogMate enrollment mode, iPadOS version, provider, supervision, Apple Business access or eligibility.

### Apple — loss of old management-service access is not equivalent to zero residual state
Apple's current migration guidance states that if the organization cannot access the old device-management service, it cannot perform some old-service cleanup such as unassigning volume-purchased apps; assignments can remain while old content-token access eventually expires. This is direct precedent that provider/admin loss can leave residual assignments/state and therefore requires explicit extinction/reconciliation rather than assuming disappearance.

Source:
- https://support.apple.com/guide/deployment/dep4acb2aa44/web

### Apple — Automated Device Enrollment and supervision
Apple documents Automated Device Enrollment for organization-owned devices and automatic supervision for supported iPadOS devices enrolled through that path. Apple Business device assignment/reassignment requires appropriately privileged organizational roles.

Sources:
- https://support.apple.com/guide/deployment/about-device-supervision-dep1d89f0bff/1/web/1.0
- https://support.apple.com/guide/business/assign-reassign-or-unassign-devices-axmf500c0851/1/web/1

**TRANSFER VALIDATION:** Apple Business/School Manager and management-service assignment can be decisive provisioning dependencies. They are not automatically recovery anchors.

### TUF — offline threshold root precedent
The current TUF specification index exposes v1.0.36. TUF's root design uses threshold trust and recommends keeping root private keys offline; if fewer than threshold keys are compromised, normal rotation can revoke them, while threshold compromise requires out-of-band recovery. TUF also emphasizes separation of signing roles and keys.

Sources:
- https://theupdateframework.github.io/specification/
- https://theupdateframework.io/docs/faq/
- https://theupdateframework.io/docs/security/

**TRANSFER VALIDATION:** offline/threshold custody and role separation are strong survivability precedents. TUF is not adopted as MintTap architecture, and exact threshold/custodian count remains OPEN.

### NIST key-management baseline
NIST SP 800-57 Part 1 Rev.5 remains the current final general key-management baseline. Rev.6 remains an Initial Public Draft as of this checkpoint.

Sources:
- https://www.nist.gov/publications/recommendation-key-managementpart-1-general
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

**CHANGE WATCH:** Rev.6 is not promoted to final guidance.

## SYNTHESIS 1 — cryptographic availability is not organizational recoverability
A recovery anchor may remain mathematically valid while no authorized living custodian can access/use it, the organizational account needed to provision clients is lost, or the provider tenant/control plane is unavailable.

Model separately:
1. anchor/key material availability;
2. authorized custodian availability;
3. recovery-policy/quorum availability;
4. company identity/admin-plane availability;
5. provisioning-provider availability;
6. Apple/enterprise enrollment dependency availability;
7. distribution-path availability;
8. client/data survivability.

`key still exists ≠ organization can lawfully/operationally exercise it`.

## SYNTHESIS 2 — custody succession must be authorized before emergency pressure
Personnel departure, incapacity or organizational restructuring should not force an improvised trust reset. Normal custody succession should be a governed policy transition with predecessor authorization where still trustworthy, successor acceptance, inventory transfer, access removal, evidence of old-custodian extinction where possible, and independent recovery if ordinary authority is lost.

`employee left ≠ key retired`; `new employee has copy ≠ custody succession complete`.

Unknown copies/material remain UNKNOWN.

## SYNTHESIS 3 — avoid an always-online super-root
Making the same always-online company IdP/admin account/MDM tenant capable of both routine provisioning and ultimate recovery collapses failure domains. High-consequence recovery authority should be sufficiently isolated from routine compromise paths; availability can be supplied through threshold/offline/escrowed or otherwise separately governed mechanisms without claiming one universal pattern.

`high availability ≠ keep ultimate recovery authority online`.

Exact custody topology is product/security architecture evidence.

## SYNTHESIS 4 — provider migration is survivability, not authority succession
Changing MDM provider or tenant can preserve device-management capability while recovery-anchor policy remains unchanged. Conversely, anchor succession can occur without MDM migration.

Apple's current iOS/iPadOS 26 migration capability is operationally important but has eligibility and state-preservation conditions. Therefore:

`MDM migration complete ≠ recovery authority migrated`; `recovery anchor current ≠ MDM migration complete`.

## SYNTHESIS 5 — loss of the old provider can leave residual authority/state
Old provider loss may prevent cleanup. Old app assignments, profiles, credentials, declarations, certificates or cached client state may persist according to their own lifecycles. The system must classify them and enforce current server admission rather than assuming provider disappearance destroyed them.

`old provider unreachable ≠ old provider state extinct`.

This extends 207's old-media rule to SaaS/control-plane residue.

## SYNTHESIS 6 — migration dependency inventory is a recovery artifact
Apple's current migration guidance explicitly calls for documenting IdP, PKI, network, app distribution, access management, monitoring, asset management and Apple-service integrations before migration. Generic recovery planning should similarly maintain a dependency graph identifying which dependencies are required for:
- routine management;
- anchor custody/signing;
- zero-state bootstrap;
- provider migration;
- device identity/re-enrollment;
- server-side admission;
- old-authority extinction.

A recovery path that depends on the failed provider/account is not independent merely because it has a different runbook.

## SYNTHESIS 7 — bootstrap survivability needs at least one admitted path outside the failed ordinary path
If normal provisioning and one recovery distribution path are unavailable, a new/erased/long-offline device can recover only if another pre-governed bootstrap basis/path remains usable. That path may be organizational provisioning, controlled offline ceremony/media, another independently governed service, or another product-specific mechanism. No generic mechanism is mandated.

The fallback must not silently weaken anchor policy or accept the newest-looking material.

`primary provisioning unavailable ≠ fallback may redefine trust`.

## SYNTHESIS 8 — provider/organization recovery requires positive and negative evidence
Recovery success needs both:
- positive: successor custodians/provider/bootstrap path can establish current authority and legitimate clients can re-enroll/re-admit;
- negative: former custodians/provider/tenant/bootstrap material cannot exercise current consequence-bearing authority at scoped enforcement points.

If old-provider cleanup cannot be performed, server-side negative admission evidence becomes even more important.

## SYNTHESIS 9 — LogMate/EFB data survivability remains independent
For a company iPad caught across MDM/provider/custodian loss:
1. preserve unique local flight/logbook data where safely possible;
2. do not erase merely to satisfy a management migration unless data durability has been independently established;
3. quarantine stale management/session/anchor assumptions from remote authority;
4. establish current recovery/bootstrap basis;
5. re-enroll/reprovision where platform/product policy requires;
6. re-evaluate device/session identity and queued mutations under current authority;
7. reconcile data without rewriting uncertain historical authorization.

Apple's current migration support can preserve managed apps/data in specified conditions, but that capability is not assumed for LogMate until target-device/runtime evidence exists.

## SYNTHESIS 10 — custody drills must include organizational/provider loss, not only key restore
A successful key backup/restore drill does not prove that the organization can recover after losing the MDM tenant, Apple Business administrator, IdP administrator, custodian personnel or provider account. Assurance must exercise the dependency graph at the intended scope.

`key restore PASS ≠ organizational/provider-loss recovery PASS`.

## Track C destructive campaign — 424 cases total
Add eight cases to the 416-case campaign:
1. anchor key intact but all authorized custodians unavailable — do not silently appoint a new custodian; invoke governed succession/reconstitution;
2. former custodian retains an unknown copy after role departure — current admission rejects former authority; copy remains UNKNOWN until evidenced otherwise;
3. MDM tenant/provider unavailable while Apple Business organizational access survives — migrate/reprovision only through admitted organizational policy; do not change recovery anchor implicitly;
4. Apple Business/admin-plane access lost while MDM provider remains reachable — routine provider access cannot self-promote into ultimate recovery authority;
5. old MDM unavailable during migration and residual app/profile/credential state remains — classify residue and prove server-side extinction rather than assuming cleanup;
6. normal MDM provisioning and primary recovery CDN both unavailable — alternate pre-governed bootstrap path may restore current basis without lowering anchor policy;
7. PITR restores former provider/custodian mapping after migration — current floor rejects resurrection and positive/negative oracles detect divergence;
8. long-offline company iPad returns after custodian + MDM migration with unique records — preserve data, bootstrap current authority, re-enroll/re-admit, retain historical uncertainty.

Campaign status: **DEFINED, NOT EXECUTED**.

## Cross-track transfer / contradiction
### A → E
Apple management migration and enrollment mechanisms are platform capabilities with explicit version/enrollment constraints. They transport/re-establish management state; they do not decide constitutional recovery authority.

### E → B
Recovery UX/content must not instruct users to erase/re-enroll as the first response when unique local operational data may exist. Distinguish management migration from data recovery and authority recovery.

### E → C
C receives personnel-loss, provider-loss, Apple-admin loss, residual-state, dual-channel outage, PITR and long-offline migration cases.

### E → D
Provider/device migration telemetry is useful for inventory and convergence only; it cannot authorize custodian/provider succession.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. This study defines recovery states and sequencing, not visual treatment; physical-device/PWA, screen-reader and human evidence remain OPEN.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage. Exact iPadOS/MDM migration behavior, secure custody implementation, local-data preservation, restore/reinstall, provider APIs and authorization-oracle execution remain implementation/runtime evidence.

## MINTTAP DECISION / DIRECTION
1. Treat recovery-anchor custody succession as governed security-policy succession, separate from provider migration and ordinary personnel administration.
2. Maintain an explicit dependency/failure-domain map for anchor custody, organizational identity/admin, MDM/Apple enrollment, PKI, distribution, backup/PITR and server admission.
3. Do not make an always-online MDM/IdP/company-admin plane the implicit ultimate recovery root merely for convenience.
4. Pre-govern at least one survivable bootstrap basis/path outside any ordinary provisioning path whose failure is in scope; do not lower anchor policy during outage.
5. Treat old-provider/custodian residue as potentially extant until scoped extinction evidence exists; provider disappearance is not deletion.
6. Separate MDM migration success from recovery-anchor succession and from PWA/local-data durability.
7. For LogMate-like iPads, preserve unique local data before destructive management recovery and re-admit remote work only under current authority.
8. Keep actual MintTap/LogMate custody, Apple Business/MDM topology, enrollment eligibility, thresholds, cryptography and recovery ceremony OPEN.

## OPEN / VALIDATION
- actual recovery-anchor custody/threshold and personnel succession policy;
- actual Apple Business/School Manager use, roles and recoverability;
- actual company-iPad ownership, supervision, Automated Device Enrollment and iPadOS version;
- actual MDM provider/tenant, migration support and admin/recovery topology;
- actual alternate bootstrap path and independence from routine control planes;
- old-provider/profile/certificate/app-assignment extinction behavior;
- PWA local-data durability during migration/re-enrollment/erase;
- physical iPad/Safari/MDM/provider, security/privacy, safety/legal/aviation, AT and human validation.

## CHANGE WATCH
- Apple management migration behavior is version/enrollment dependent. Current Apple Platform Deployment pages published 2026-09-17 document iOS/iPadOS/macOS 26+ migration conditions; re-check target OS/provider before implementation.
- TUF and NIST remain transfer precedents, not MintTap architecture.
- NIST SP 800-57 Rev.6 remains an Initial Public Draft at this checkpoint.

## VALIDATION / GATE
**PASS (generic).** The Web Manager can now separate cryptographic anchor availability from organizational custody survivability, distinguish provider migration from authority succession, reason about residual state after provider loss, require a pre-governed alternate bootstrap basis without creating an always-online super-root, and preserve offline operational data across management recovery. Product/runtime validation remains OPEN.

## Next highest-value adjacent question
**209 — recovery-ceremony authorization, dual-control break-glass abuse & post-recovery privilege contraction.** Determine how exceptional custody/provider-loss recovery is initiated and approved without allowing one surviving administrator, support operator or compromised identity plane to invoke a permanent trust reset; how emergency authority is scoped/time-bounded/audited; how recovery completes when some approvers are unavailable; and how temporary break-glass privilege is provably removed after normal control is restored.