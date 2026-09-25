# 286 — PWA Recovery-Ceremony Evidence Durability, Anti-Equivocation & Post-Recovery Normalization

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-25  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B recovery UX; Track C destructive validation; Track D recovery diagnostics.  
Dependencies: 266–285 authority/currentness, anti-rollback, mixed-generation adjudication, stale-client rebootstrap and predecessor-consequence closure.

## Problem

285 established that a long-offline PWA must preserve unique local data while re-establishing current organizational bootstrap, runtime and operation admission separately. The adjacent Stage 8 problem is catastrophic recovery: the ordinary authority or publication path may be compromised or restored from stale state, while clients, mirrors or operators can observe conflicting successor claims.

Central rule: **recovery is not complete when a successor works. A defensible recovery needs durable evidence of the succession decision, resistance to equivocation, explicit predecessor rejection, and a governed transition from emergency authority back to normal operations.**

## Five-track balance

- **A Platform/Browser:** prerequisite supplier. Browser secure transport, Service Worker update/control and local storage can transport/cache recovery material but cannot elect organizational authority.
- **B UX/IA/Content:** consumer. Must expose task truth such as local-data-preserved, revalidation-required and remote-confirmation-pending without asking ordinary users to adjudicate trust roots.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1040 → 1048 defined cases**; runtime/device/AT/human execution remains OPEN.
- **D Search/Discovery/Analytics:** challenger. Can observe recovery convergence and contradictory lineage evidence; telemetry cannot elect authority.
- **E Architecture/Security/Operations:** bottleneck owner. Owns recovery evidence, witness independence, predecessor extinction, emergency-authority retirement and normalization.

## SOURCE

### NIST SP 800-184 — recovery is a planned, tested and improved discipline

NIST SP 800-184 provides strategic and tactical guidance for recovery planning, playbooks, testing and continual improvement after cybersecurity events.

Source:
- https://doi.org/10.6028/NIST.SP.800-184

**TRANSFER VALIDATION:** recovery is not merely restoration of bytes or service availability. Product-specific recovery authority, quorum and acceptance criteria remain OPEN.

### RFC 9162 — append-only evidence can still face split views

Certificate Transparency defines inclusion/consistency auditing and explicitly recognizes a misbehaving log presenting different conflicting Merkle-tree views to different parties. Detecting this class requires comparison of observed signed tree heads; the RFC describes gossip as an active research area rather than a complete protocol.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** one internally consistent recovery history does not by itself prove that every observer received the same organizational successor history.

### Sigstore/TUF — trust-root distribution and independent holders are bounded precedents

Sigstore documents a trust root established by a public root-key ceremony with rotating keyholders from different organizations/institutions and distributes verification material through TUF. Cosign starts from an embedded TUF root and retrieves updated trusted verification material.

Sources:
- https://docs.sigstore.dev/about/security/
- https://docs.sigstore.dev/cosign/system_config/installation/

**TRANSFER VALIDATION:** MintTap/LogMate is not assumed to use Sigstore or TUF. The reusable lesson is that succession evidence, threshold approval, distribution and verification are separate questions, and nominal key count is not proof of failure-domain independence.

## SYNTHESIS 1 — succession evidence is a security artifact

A catastrophic-recovery decision should leave durable evidence sufficient for an authorized verifier to determine at least:
1. predecessor/current lineage being replaced;
2. successor identity/generation;
3. bounded reason/recovery event identity;
4. approval/ceremony evidence appropriate to the threat model;
5. effective transition constraints;
6. predecessor rejection/retirement requirements.

The exact schema, cryptography and retention are product-specific and OPEN.

Guards:
- `successor reachable ≠ succession proven`;
- `new key exists ≠ new key legitimately appointed`;
- `incident ticket exists ≠ cryptographic/organizational succession evidence`.

## SYNTHESIS 2 — evidence must outlive the path it is judging

If the only record proving recovery is stored behind the same account, provider, backup set and administrative path whose compromise triggered recovery, that evidence may disappear or rollback with the failed domain.

Independence is threat-relative:
- separate database under the same recovery account may not be independent;
- separate provider under the same identity/recovery control may not be independent;
- multiple keys held by one operator/workstation are not automatically independent.

Guard: `multiple copies ≠ independent witnesses`.

## SYNTHESIS 3 — transparency and authority election are different

Append-only/transparency evidence can make contradiction or history mutation detectable. It does not decide which of two conflicting organizational successor claims is legitimate.

RFC 9162's split-view model is the bounded precedent: locally valid signed history can coexist with conflicting views until observations are compared.

Guards:
- `append-only proof ≠ organizational legitimacy`;
- `one consistent view ≠ globally unique view`;
- `highest epoch ≠ legitimate successor`.

## SYNTHESIS 4 — anti-equivocation needs comparison across relevant failure domains

A recovery architecture should identify which observers/witnesses can compare successor claims and which compromise domains could cause them to collude or rollback together.

The goal is not universal consensus. The goal is sufficient evidence for the declared threat model that conflicting successor claims cannot silently become NORMAL at material boundaries.

When legitimate lineage cannot be established, consequence-bearing remote effects remain `UNKNOWN/contained`.

## SYNTHESIS 5 — emergency authority must have an exit

Emergency recovery authority can become a permanent bypass if it is never retired. Normalization therefore requires explicit closure:
1. establish legitimate successor;
2. restore normal admission/publication paths;
3. migrate required runtime/clients;
4. verify predecessor and emergency bypass rejection at material boundaries;
5. retire/restrict emergency credentials and procedures;
6. preserve recovery evidence for the required horizon;
7. continue contradiction monitoring appropriate to the system.

Guard: `incident resolved ≠ emergency authority retired`.

## SYNTHESIS 6 — normalization is consequence-specific

A system may restore read/local-capture/export before destructive or publication effects. Returning the UI or origin to service does not justify restoring every authority simultaneously.

Guard: `site available ≠ all remote consequences normalized`.

## SYNTHESIS 7 — long-offline PWA is a recovery consumer, not an authority elector

A dormant iPad may return with:
- unique local records;
- old runtime/Service Worker;
- old session/policy/bootstrap material;
- queued intents;
- historical evidence of a prior lineage.

Those facts can be valuable for preservation and reconciliation. They do not authorize the client to choose between conflicting server successor claims.

Generic sequence:
1. preserve unique local records, queue and provenance;
2. classify cached trust/runtime/session state as potentially stale;
3. obtain legitimate current bootstrap through the recovery model;
4. adopt required runtime/schema changes;
5. obtain current admission;
6. map queued intents to current consequence semantics;
7. reconcile ambiguous prior effects;
8. execute only after current material-boundary authorization.

## SYNTHESIS 8 — client generation cannot repair organizational ambiguity

A client showing a numerically higher cached epoch does not make it current. Conversely, a recovered server showing a lower generation must not erase newer unique client data merely because its restored authority database is older.

Guards:
- `higher client epoch ≠ server authority`;
- `restored server epoch ≠ unique local data obsolete`;
- `runtime update ≠ organizational recovery complete`.

## SYNTHESIS 9 — telemetry is contradiction evidence, not quorum

Track D may measure:
- successor bootstrap adoption;
- predecessor rejection;
- emergency-path use;
- dormant-client return;
- contradictory generation observations;
- reconnect→current-admission latency.

But traffic majority, recency or silence cannot appoint authority.

Guards:
- `majority observation ≠ legitimate succession`;
- `zero predecessor traffic ≠ predecessor extinct`.

## SYNTHESIS 10 — recovery evidence needs privacy/minimization governance

Durable evidence should preserve what is necessary to prove succession and detect contradiction without retaining unrelated sensitive payload indefinitely. Exact identifiers, hashes, signatures, operator records, retention horizon and legal requirements remain product-specific.

Guard: `durable evidence ≠ retain all incident data forever`.

## SYNTHESIS 11 — post-recovery validation must include negative evidence

Success-path checks are insufficient. Closure requires tests that predecessor and emergency authorities fail at every material path that could still create consequences: API, background worker, compatibility bridge, admin/recovery path and stale-client rejoin.

Guard: `successor works ≠ predecessor powerless`.

## SYNTHESIS 12 — PWA/browser mechanics remain subordinate to recovery authority

HTTPS, Service Worker update, Cache Storage, IndexedDB, Home Screen installation and push can transport or retain recovery-related material. None independently establishes organizational legitimacy.

Platform-specific iOS/iPadOS background, MDM/ADE, persistence and install behavior remain CHANGE WATCH and require device/runtime evidence.

## MINTTAP DECISION / DIRECTION

1. Treat catastrophic-recovery succession evidence as a first-class security artifact.
2. Define witness/quorum independence by failure domain, not count.
3. Do not use highest-version, newest timestamp, traffic majority or client preference to elect organizational authority.
4. Keep transparency/append-only evidence separate from legitimacy decisions.
5. Preserve unique offline PWA data before runtime/trust repair.
6. Require an explicit emergency-authority retirement and normalization phase.
7. Close recovery with negative predecessor/emergency-path evidence, not successor success alone.
8. Keep product implementation, retention periods, quorum, managed-iPad behavior and production PASS OPEN until verified.

## DEPENDENCY / TRANSFER

- **A → E/C:** secure transport, Service Worker lifecycle and storage constrain delivery/adoption but do not elect authority.
- **E → B:** recovery/currentness states become user task-truth requirements; Design Studio owns reusable interaction treatment.
- **E → C:** C receives anti-equivocation, emergency-retirement and stale-client invariants for destructive validation.
- **E → D:** D measures convergence/contradictions but cannot appoint authority.
- **Software Engineering:** implementation of lineage records, witness/quorum mechanics, durable evidence, fault injection and recovery tooling remains engineering evidence.
- **Design Studio:** no physical-device PWA, screen-reader or representative-human evidence observed in the latest canonical commits that promotes this gate.

## Track C destructive additions — defined, not executed

1041. **Successor-reachability theater:** a reachable successor endpoint is treated as proof of legitimate succession.  
1042. **Correlated-witness quorum:** several approvals/copies share the same compromise or recovery domain but are counted as independent.  
1043. **Highest-epoch election:** conflicting valid-looking lineages are resolved solely by the largest version/epoch.  
1044. **Transparency-equals-authority:** append-only consistency is treated as proof of organizational legitimacy.  
1045. **Emergency-bypass permanence:** incident path remains capable of material effects after normal service is restored.  
1046. **Dormant-client election:** an offline PWA's cached generation is allowed to choose organizational authority.  
1047. **Recovered-server data destruction:** stale restored authority causes newer unique local records to be erased before reconciliation.  
1048. **Successor-only closure:** successor path passes while predecessor/emergency/admin/compatibility path still creates material effects.

Execution, physical-device, AT and representative-human PASS are not claimed.

## OPEN

Actual MintTap/LogMate authority topology, quorum/witness model, recovery identities, providers, backups, bootstrap lineage, auth/session/token model, Service Worker behavior, managed-iPad/MDM/ADE configuration, storage, queue/schema, consequence classes, retention, legal/aviation/safety requirements and human/accessibility behavior remain OPEN.

## CHANGE WATCH

- iOS/iPadOS/WebKit installed-web-app, Service Worker, storage, background and managed-device behavior.
- TUF/Sigstore operational trust-root practices.
- Transparency/gossip/anti-equivocation mechanisms and standards.

## VALIDATION

Generic gate passes because the model now distinguishes restoration, succession legitimacy, durable recovery evidence, anti-equivocation, witness independence, emergency-authority retirement, stale-client preservation and negative predecessor closure.

Production validation remains OPEN until real runtime/backend/managed-iPad/AT/human evidence exists.

## Next high-value target

**287 — recovery evidence retention, witness compromise/rotation, emergency-credential lifecycle and normalization drills.** Determine how recovery evidence remains verifiable as witnesses/keys/operators rotate or become compromised, how old emergency credentials become provably unusable, and how recurring drills validate the complete normalization path without manufacturing production claims.
