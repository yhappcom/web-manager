# 262 — PWA Dependency-Surface Inventory Drift, Discovery-Control Failure & Completeness-Proof Independence

Status: **PASS (generic) / PRODUCT + DATA-MODEL + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime discovery mechanics; Track B uncertainty/challenge UX; Track C destructive validation; Track D bounded drift/coverage measurement.  
Dependencies: 122–130, 161, 198–200, 241–261, especially assurance independence, hidden-edge discovery, consequence-scoped completeness and reauthorization-proof expiry.

## Problem
261 established that a dependency graph can be internally consistent yet incomplete, and that completeness is a consequence-scoped assurance claim. The next failure boundary is recursive: the inventory and discovery controls used to justify completeness can themselves be stale, incomplete, misconfigured, compromised, unavailable, or controlled by the same producer whose omissions they are supposed to detect.

A producer that declares its own consumers, emits the only telemetry about those consumers, and signs the resulting completeness proof can create a perfectly self-consistent false world. Conversely, demanding organizationally separate tooling for every low-risk inventory claim would create cost without proportionate assurance.

Central rule: **completeness confidence depends not only on what the inventory says, but on how inventory evidence is produced, challenged, reconciled and kept current. High-consequence closure must not rely solely on a producer-controlled self-description of its own dependency surface. Independence is risk-proportionate and evidence-path-specific, not a universal requirement for separate vendors or teams.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns what browser caches, Service Workers, storage, navigation, installed-PWA/runtime state and network observations can reveal—and what they cannot reveal when offline or uninstrumented.
- **B UX/IA/Content:** high dependency pressure. Owns truthful states such as `inventory stale`, `coverage challenged`, `drift unresolved`, `safe to inspect`, and `publication blocked`; human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **848 → 856 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer/challenger. May compare declared and observed topology and measure drift debt, but analytics silence cannot prove absence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns inventory provenance, drift reconciliation, discovery-control failure handling, risk-proportionate challenge independence and closure policy.

## SOURCE

### NIST SP 800-53 Rev. 5 / Release 5.2.0 — inventory must be updated and maintained
CM-8 System Component Inventory requires an inventory of system components. CM-8(1) addresses updating inventory during installation/removal/system updates; CM-8(2) addresses automated mechanisms to maintain currency, completeness, accuracy and availability; CM-8(3) addresses automated detection of unauthorized components. The discussion explicitly recognizes that some components, such as inactive virtual machines, can be difficult to observe.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final  
Source PDF: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

**TRANSFER VALIDATION:** bounded precedent that inventory is a maintained control subject to update and discovery failure, not a timeless declaration. It does not define a LogMate dependency graph or PWA topology.

### NIST SP 800-53A Rev. 5 — assessment can require independence and multiple evidence methods
CA-2(1) calls for independent assessors/assessment teams where the organization-defined level of independence requires it. NIST explains that independence is about impartiality and freedom from conflicts involving development, operation, sustainment, management or effectiveness determination. SP 800-53A assessment methods include examine, interview and test rather than treating one system's self-report as the only evidence channel.

Source: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** supports risk-proportionate independent challenge and evidence diversity. It does not imply that every web inventory needs a third-party auditor or separate vendor.

### NIST SP 800-137 — continuous monitoring and discovery can expose unauthorized components
NIST SP 800-137 discusses configuration/network management technologies that support host discovery, inventory, change control and continuous monitoring, including discovery of unauthorized hardware/software. It also treats continuous monitoring as broader than a one-time inventory snapshot.

Source: https://csrc.nist.gov/pubs/sp/800/137/final

**TRANSFER VALIDATION:** supports ongoing declared-vs-observed comparison. It does not prove that automated monitoring sees offline, manual or external dependencies.

### NIST CSF 2.0 — governance, inventories and data flows remain maintained risk-management outcomes
CSF 2.0 applies broadly to organizations and emphasizes governance and supply-chain risk. Its asset-management outcomes include managed hardware/software/services, authorized network communications/data flows, supplier services and data/metadata inventories. NIST's August 2026 final SP 1347 further emphasizes applying informative references with continuing evaluation rather than treating a mapping as self-validating.

Sources: https://www.nist.gov/cyberframework  
https://csrc.nist.gov/News/2026/csf-2-0-informative-references-qsg

**TRANSFER VALIDATION:** supports lifecycle maintenance and cross-reference of evidence. It does not establish product-specific completeness.

## SYNTHESIS 1 — inventory is evidence, not reality
A declared dependency-surface inventory is one observation of topology. It can be stale or wrong even if its schema is valid and its signature verifies.

Guard: `inventory signed ≠ inventory complete`; `inventory current timestamp ≠ topology current`.

## SYNTHESIS 2 — model inventory provenance and control health
For consequence-bearing completeness, record at least inventory generation, producer, collection method, collection scope, source systems, last successful observation, expected update trigger/frequency, known blind spots, control-health state and reconciliation/challenge evidence.

A discovery agent that stopped reporting yesterday must not silently produce today's `complete` result from cached state.

Guard: `collector healthy yesterday ≠ collector healthy now`; `last successful scan ≠ current scan`.

## SYNTHESIS 3 — detect declared-vs-observed topology drift
Compare declared architecture/configuration against independent-enough observations where practical: DNS/CDN/configuration state, runtime request destinations, queue/job registries, export registries, storage/backup manifests, MDM/fleet inventory, operator records and bounded browser/device observations.

Contradictions are not automatically attacks; they are drift evidence requiring classification.

Guard: `declared topology ≠ observed topology`; `drift detected ≠ compromise proven`.

## SYNTHESIS 4 — producer self-description cannot be the sole high-consequence completeness proof
If producer P owns the consumer registry, emits the only discovery telemetry, and approves its own completeness proof, one omission or compromise can defeat all three layers. For material closure, introduce an independent-enough challenge path whose failure domain is not identical to the claim being tested.

This can be another internal role/system, a separately derived inventory, bounded runtime observation, configuration reconciliation, or independent assessment. It need not always be a different vendor.

Guard: `producer says all consumers known ≠ all consumers known`; `different dashboard ≠ independent evidence`.

## SYNTHESIS 5 — independence is dimensional, not binary
Assess independence across relevant dimensions: data source, collection mechanism, credential/authority, administration, deployment/update path, storage, reviewer/approver, and failure/compromise domain. Two tools querying the same compromised registry with the same credential are correlated even if their logos differ.

Guard: `two tools ≠ two independent observations`; `different vendor ≠ independent data source`.

## SYNTHESIS 6 — discovery controls themselves need failure states
A completeness engine must distinguish at least `CURRENT`, `STALE`, `PARTIAL`, `FAILED`, `CONTRADICTED`, `UNKNOWN` and `UNDER-CHALLENGE` for discovery evidence. Collector failure is not an empty result.

Guard: `discovery failed ≠ zero dependencies`; `timeout ≠ clean inventory`.

## SYNTHESIS 7 — inventory updates must follow topology-changing events
Relevant triggers can include deployment/configuration change, new worker/queue/export/integration, CDN/routing change, Service Worker/cache strategy change, backup/restore topology change, MDM/fleet lifecycle change, support/manual workflow change, schema/policy migration and newly discovered hidden edges.

Periodic scans remain useful but cannot substitute for event-triggered reconciliation.

Guard: `scheduled scan not due ≠ topology unchanged`; `change deployed ≠ inventory updated`.

## SYNTHESIS 8 — change-control success does not prove discovery-control success
A deployment may be approved and technically successful while inventory hooks fail, or an emergency manual path may bypass normal configuration management. Closure therefore checks both topology change and evidence that the inventory/discovery model absorbed the change.

Guard: `change approved ≠ dependency inventory reconciled`; `deployment green ≠ discovery green`.

## SYNTHESIS 9 — offline/long-tail devices create asymmetric visibility
A company iPad offline for weeks cannot be assumed absent because central discovery sees no active session. Its local Cache Storage, IndexedDB, queued operations, installed PWA generation and unique data may be invisible to central telemetry.

Central inventory should preserve an `offline/unknown` fleet tail until governed retirement/disposition or bounded rejoin evidence exists.

Guard: `centrally unobserved ≠ locally empty`; `offline device ≠ nonexistent consumer`.

## SYNTHESIS 10 — challenge paths must survive the primary discovery mechanism's compromise
If the main registry or collector is suspected compromised, recomputing completeness from the same source is circular. Preserve enough independent-enough evidence—configuration history, signed change records, alternate inventories, bounded endpoint attestations, export/queue records, backup manifests or human-controlled records as appropriate—to reconstruct or challenge the claim.

Guard: `re-ran compromised collector ≠ independent revalidation`.

## SYNTHESIS 11 — challenge evidence can itself be incomplete
An independent challenger is not omniscient. Record its scope, blind spots and freshness. Independence increases confidence; it does not convert bounded evidence into universal proof.

Guard: `independent assessment ≠ universal completeness`; `challenger found no drift ≠ no hidden edge anywhere`.

## SYNTHESIS 12 — disagreement is a first-class assurance state
When declared inventory and observed topology disagree, preserve both observations and the reconciliation decision. Do not silently force observed data into the declared model or discard observations as noise merely because canonical documentation differs.

Guard: `canonical document ≠ automatically correct observation`; `runtime observation ≠ automatically authorized topology`.

## SYNTHESIS 13 — manual and external paths need proportionate challenge
Some dependencies cannot be discovered by code scanning or telemetry: printed reports, emailed files, support spreadsheets, ad-hoc exports and third-party handoffs. For material consequences, challenge can include recipient/export registries, ticket evidence, operator interview, sampled reconciliation and acknowledgement evidence.

Guard: `machine inventory complete ≠ operational inventory complete`.

## SYNTHESIS 14 — telemetry is useful for contradiction, weak for absence
Track D can use analytics/network observations to identify an undeclared consumer or unexpected route. But privacy blocking, offline operation, failed instrumentation and manual paths make silence ambiguous.

Guard: `observed event can reveal drift`; `no event cannot universally prove no drift`.

## SYNTHESIS 15 — completeness proof should carry challenge lineage
A high-consequence closure proof should bind the consequence, inventory generation, discovery-control health, enumerated surfaces, declared/observed reconciliation result, challenger/evidence path, unresolved blind spots, policy/authority/topology generations and invalidation triggers.

A successor challenge supersedes current applicability without deleting historical proof.

Guard: `proof exists ≠ proof independently challenged`; `challenge superseded ≠ historical challenge erased`.

## SYNTHESIS 16 — avoid assurance monoculture
Do not create one inventory service whose outage/compromise simultaneously erases the dependency graph, collector health, challenge evidence and closure history. Independence can be modest but should preserve the ability to detect or reconstruct material contradiction.

Guard: `centralized convenience ≠ acceptable common-mode assurance`.

## SYNTHESIS 17 — PWA browser mechanics are discovery surfaces, not fleet authority
Service Worker registrations, Cache Storage, IndexedDB and page/session telemetry can expose local state when reachable. They cannot prove every installed/offline PWA state across iOS/iPadOS or other browsers, and a current Service Worker does not prove current dependency inventory.

Guard: `Service Worker observed current ≠ local dependency state complete`; `browser inventory ≠ fleet inventory`.

## SYNTHESIS 18 — product facts remain OPEN
This study does not assert that MintTap/LogMate uses a specific MDM, CDN, worker queue, export service, backup platform, telemetry stack, inventory collector, independent assessor or proof format. Those are validation targets against canonical implementation/runtime evidence.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. treat dependency inventories as provenance-bearing evidence with explicit control-health state;
2. compare declared topology with independent-enough observed evidence for material consequences;
3. prevent a producer-controlled self-description from being the sole high-consequence completeness proof;
4. evaluate independence across data source, credentials, administration, deployment, storage and reviewer—not vendor count;
5. distinguish collector failure/staleness/partial coverage from an empty inventory;
6. reconcile inventory on material topology-changing events as well as periodic review;
7. preserve offline/unknown fleet tails rather than converting telemetry silence into absence;
8. retain contradiction/reconciliation provenance instead of overwriting history;
9. bind completeness proofs to challenge lineage, discovery-control health and known blind spots;
10. preserve a recovery/challenge path that does not depend entirely on the discovery mechanism being challenged.

## EFB / LogMate-like application case
Assume server inventory G21 says all P12-era consumers are fenced, but a company iPad has been offline for 45 days. The main discovery collector D1 and topology registry R1 are administered by the same service account. A separate export registry shows an undeclared historical handoff, and the returning iPad contains a browser-local retry queue unknown to R1.

Safe generic sequence:
1. preserve unique local records/provenance and the retry queue without executing it;
2. mark G21 completeness `CONTRADICTED/UNDER-CHALLENGE`, not historically nonexistent;
3. preserve D1/R1 outputs and collector-health evidence;
4. add the export handoff and local queue as discovered topology evidence with discovery time/provenance;
5. determine whether D1/R1 share a compromise/failure domain and avoid circular revalidation from them alone;
6. reconcile against independent-enough configuration/export/device evidence within the consequence scope;
7. fence only affected mutation/publication paths while keeping unique data inspectable/recoverable;
8. revalidate/rebase queued operations under current authority/schema/policy;
9. issue successor completeness evidence bound to the corrected inventory and challenge lineage;
10. keep unobserved offline/manual/external surfaces explicit as residual assurance debt.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
849. **Producer self-certification theater** — producer registry, collector and closure proof all derive from one self-controlled source; no challenge path. Expected: fail.
850. **Collector-failure-as-empty** — discovery agent times out and system records zero dependencies/current completeness. Expected: fail.
851. **Different-dashboard independence theater** — two dashboards query the same compromised registry with the same credential and are counted as independent observations. Expected: fail.
852. **Approved-change inventory lag** — new worker/export path deploys successfully but completeness proof remains valid against pre-change inventory. Expected: fail.
853. **Offline-tail erasure** — 45-day-silent iPad disappears from consumer inventory without authorized retirement/disposition. Expected: fail.
854. **Circular compromise revalidation** — suspected discovery registry is cleared solely by rerunning its own collector. Expected: fail.
855. **Canonical-doc contradiction suppression** — observed undeclared consumer is discarded because architecture documentation says it cannot exist. Expected: fail.
856. **Independent-challenger omniscience** — bounded independent assessment finds no drift and system upgrades claim to universal completeness despite explicit blind spots. Expected: fail.

**VALIDATION:** these are defined destructive cases only. Execution PASS is not claimed.

## OPEN / VALIDATION
Production validation remains OPEN for:
- actual dependency-surface inventory and ownership;
- actual inventory/discovery collector(s), credentials and failure domains;
- topology/change event sources and reconciliation automation;
- actual browser/PWA local stores, Service Worker/cache/update behavior and long-offline fleet visibility;
- MDM/ADE/Apple Business/device-incarnation topology;
- queue/job/export/integration/manual workflow surfaces;
- backup/PITR/restore inventory behavior;
- completeness-proof/challenge format and storage;
- authority for contradiction resolution and closure;
- physical iOS/iPadOS/installed-PWA runtime;
- accessibility and representative-human understanding of uncertainty/challenge states;
- security/privacy/legal/aviation/domain requirements.

## CHANGE WATCH
- NIST SP 800-53 / 800-53A releases and assessment guidance;
- NIST CSF 2.0 implementation/informative-reference guidance;
- Apple/WebKit iOS/iPadOS PWA lifecycle, storage and managed-device behavior;
- browser storage/Service Worker capability changes;
- canonical product architecture, MDM, backend, export, backup and workflow changes.

## Gate assessment
**PASS (generic).** The Web Manager can distinguish inventory from reality; model discovery-control health; detect declared-vs-observed drift; require risk-proportionate independent-enough challenge; reason about correlated evidence/failure domains; preserve offline tails; handle discovery-control compromise without circular self-clear; and scope challenge evidence without claiming universal completeness.

No product/runtime/security/legal/aviation/physical-device PASS is implied.

## Next high-value target
**263 — topology-change authorization, shadow-consumer admission & discovery-to-governance closure.** Study how newly discovered consumers become authorized/owned inventory entries rather than merely observed nodes; distinguish legitimate emergency/manual paths from shadow dependencies; require ownership, consequence classification and retirement rules before a discovered edge is normalized into current topology; and prevent the discovery system itself from silently authorizing what it observes.