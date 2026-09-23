# 261 — PWA Dependency-Graph Completeness Assurance, Hidden-Edge Discovery & Reauthorization-Proof Expiry

Status: **PASS (generic) / PRODUCT + DATA-MODEL + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/cache/Service Worker mechanics; Track B uncertainty/reverification UX; Track C destructive validation; Track D bounded coverage/debt measurement.  
Dependencies: 122–130, 161, 198–200, 241–260, especially assurance-debt governance, revocation/downstream remediation, credential compromise, dependency reconstruction and bounded reauthorization.

## Problem
260 established how to reconstruct a compromise blast radius from typed consequence-bearing dependencies. The next failure boundary is epistemic: a graph can be internally consistent yet incomplete. A closure engine can traverse every recorded edge and still miss a PDF export, stale HTTP cache, background job, manual spreadsheet, browser-local queue, old Service Worker path, third-party handoff or operator procedure that actually consumed the disputed state.

The opposite failure is to demand impossible proof that no hidden dependency exists anywhere. That converts assurance into paralysis and encourages fake completeness claims.

Central rule: **dependency completeness is consequence-scoped assurance, not a universal boolean. Closure requires an explicit coverage basis for the relevant consequence, known unknowns, negative discovery evidence across enumerated dependency surfaces, and freshness of both the graph and the reauthorization proof. A previously sound proof expires when material policy, topology, schema, authority or workflow assumptions change.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns HTTP cache, browser storage, Service Worker, navigation, offline queue and runtime mechanics that create hidden technical copies/paths. It does not decide semantic consequence.
- **B UX/IA/Content:** high dependency pressure. Owns truthful `coverage incomplete`, `reverification required`, `safe to read but not publish`, recovery and manual-handoff states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **840 → 848 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. May measure discovered surfaces, stale proof debt and convergence latency; absence of telemetry cannot prove absence of a dependency.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns completeness claims, discovery inventory, proof assumptions, invalidation triggers, bounded expiry and closure policy.

## SOURCE

### NIST CSF 2.0 — inventories, flows and lifecycle are maintained
NIST CSF 2.0 identifies asset management outcomes including inventories of managed hardware, software/services/systems, authorized network communications and data flows, supplier-provided services, designated data/metadata, and lifecycle management. CSF 2.0 is an outcome framework rather than a product graph specification.

Source: https://www.nist.gov/cyberframework  
Source PDF: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf

**TRANSFER VALIDATION:** supports systematic inventory/flow coverage as a prerequisite to risk reasoning. It does not prove that a LogMate-like dependency graph is complete.

### NIST SP 800-53 Rev. 5 — continuous monitoring, change control, impact analysis and inventory are distinct controls
NIST SP 800-53 includes CA-7 Continuous Monitoring and configuration-management controls including CM-3 Configuration Change Control, CM-4 Security Impact Analysis and CM-8 System Component Inventory. Its change-control guidance includes documenting proposed/completed changes and auditing changes before and after implementation.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** bounded precedent that inventory alone is insufficient; changes and their impact require continuing assessment. It does not prescribe this study's graph schema or proof-expiry algorithm.

### NIST SP 800-61 Rev. 3 — incident response is integrated across cybersecurity risk management
NIST finalized SP 800-61 Rev. 3 in April 2025 and integrates incident response with broader cybersecurity risk-management activities to improve preparation, detection, response and recovery.

Source: https://csrc.nist.gov/pubs/sp/800/61/r3/final

**TRANSFER VALIDATION:** supports continuing impact/recovery reasoning across operational boundaries rather than one-time credential revocation. It does not define product dependency completeness.

### RFC 9111 — HTTP invalidation is local to caches on the request path
RFC 9111 requires certain cache invalidation after successful unsafe requests but explicitly notes that this does not guarantee all appropriate responses are invalidated globally; only caches traversed by the state-changing request are necessarily affected. It also distinguishes cache freshness/revalidation from user-agent history/display behavior.

Source: https://www.rfc-editor.org/rfc/rfc9111.html

**TRANSFER VALIDATION:** direct evidence that a canonical-source mutation cannot establish global-copy convergence. HTTP caches are one hidden-edge class, not the whole dependency problem.

## SYNTHESIS 1 — completeness is scoped to a consequence and observation boundary
Do not store `graph_complete=true` as a universal property. A graph can be sufficient to decide whether current sync publication is allowed while insufficient to claim every historical PDF recipient has been remediated.

A useful completeness claim binds at least:
- consequence/action being authorized;
- subject/projection/record scope;
- graph generation;
- policy/verifier/authority generation;
- enumerated dependency surfaces;
- discovery methods/evidence;
- unresolved unknowns/exceptions;
- proof time and invalidation triggers.

Guard: `graph traversed completely ≠ real dependency universe complete`; `complete for sync ≠ complete for external remediation`.

## SYNTHESIS 2 — maintain a dependency-surface inventory before claiming coverage
Hidden-edge discovery should enumerate where state can leave or outlive the canonical path. Generic classes include:
1. canonical database/event/provenance stores;
2. server caches, CDN/edge caches and derived materializations;
3. browser HTTP cache, Cache Storage, IndexedDB/local storage and Service Worker-controlled resources;
4. offline mutation/retry queues and background processing queues;
5. scheduled jobs, workers, outboxes, dead-letter/retry stores and delayed tasks;
6. exports, reports, email attachments, downloaded files and print artifacts;
7. APIs/webhooks/integrations and third-party imports;
8. backups, snapshots, PITR, restore environments and disaster-recovery copies;
9. manual workflows, spreadsheets, support/admin tools and operator runbooks;
10. device reincarnations, long-offline clients and retired-but-returnable fleet tails.

This is a discovery taxonomy, not a claim that MintTap/LogMate currently implements each surface.

Guard: `inventory item absent ≠ dependency absent`; `surface known ≠ every edge on surface known`.

## SYNTHESIS 3 — use multiple discovery channels; no single telemetry source is authoritative
Compare architecture/configuration inventory, code/config references, queue/job definitions, data-flow documentation, export registries, audit/provenance records, backup topology, operator procedures and bounded runtime observations. Contradictions become investigation input.

Analytics may reveal an unexpected consumer but silence is not proof of non-use, especially for offline iPads, blocked telemetry, manual exports or retired clients.

Guard: `zero telemetry ≠ zero dependency`; `no recent request ≠ no durable copy`.

## SYNTHESIS 4 — hidden edges are discovered evidence, not retroactive history invention
When investigation finds that C12 also depended on manual export workflow M3, add a graph-correction event recording discovery evidence and discovery time. Do not rewrite the historical graph to imply M3 was always known.

Guard: `edge discovered later ≠ edge created later`; `current graph knowledge ≠ historical operator knowledge`.

## SYNTHESIS 5 — absence evidence requires an explicit search space
A negative result is meaningful only relative to a defined surface and method: e.g. "no active outbox/dead-letter job references projection P12 in enumerated queue stores at generation J7." It does not mean "no hidden dependency exists anywhere."

A closure proof should therefore carry coverage assertions and residual unknowns rather than an unqualified absence claim.

Guard: `not found in searched stores ≠ nonexistent globally`; `negative query PASS ≠ complete architecture inventory`.

## SYNTHESIS 6 — completeness debt blocks only consequences that require the missing assurance
Unknown external-recipient remediation may block `ALL-RECIPIENTS-REMEDIATED` but need not destroy unique local flight data or necessarily block unrelated read-only access. Missing queue provenance may block mutation replay while allowing evidence inspection.

Guard: `one unknown edge ≠ whole product unusable`; `unknown consequence dependency ≠ safe to publish`.

## SYNTHESIS 7 — reauthorization proof has an assumption set, not timeless validity
A successor proof can be sound under graph G20, policy P20, verifier V9, schema S8, authority epoch K5 and topology T7. It must be reconsidered when a material assumption changes.

Potential invalidation triggers include:
- policy or consequence-scope change;
- authority/credential compromise, rotation or role change;
- verifier/oracle/corpus generation change;
- schema/semantic migration;
- new export/integration/background-job path;
- cache/Service Worker/storage topology change;
- backup/restore/re-enrollment path change;
- newly discovered hidden edge or contradiction;
- product workflow change that creates a new consequence;
- evidence expiry required by governing policy.

Guard: `reauthorized once ≠ authorized forever`; `proof cryptographically valid ≠ proof assumptions still current`.

## SYNTHESIS 8 — prefer event/assumption-triggered expiry over arbitrary TTL-only expiry
A time interval can force periodic review, but age alone is a weak semantic model. A five-minute-old proof can be stale after a material topology/policy change; a much older proof may remain historically valid for its original claim even though it is no longer sufficient for a new consequence.

Use time-based expiry where policy/risk requires it, but bind proof currentness to material assumption generations and change events.

Guard: `young proof ≠ current proof`; `old proof ≠ historically false`.

## SYNTHESIS 9 — topology generation must include non-code operational paths
A deployment hash or Service Worker version cannot represent manual support workflow, CDN rule, queue consumer, export destination or MDM/backup topology. Completeness proof should reference a broader operational topology generation or equivalent set of versioned assumptions.

Guard: `same app build ≠ same dependency topology`; `same Service Worker ≠ same operational graph`.

## SYNTHESIS 10 — caches are consumers/copies, not semantic authority
RFC 9111 demonstrates why source correction cannot imply global cache invalidation. For PWA reasoning, browser Cache Storage and Service Worker caches are additionally application-controlled stores with their own lifecycle. A cached projection can remain readable while current publication authority has changed.

Do not infer semantic currentness from cache freshness alone.

Guard: `HTTP fresh ≠ semantically current`; `cached copy reachable ≠ publishable truth`.

## SYNTHESIS 11 — background jobs require authorization at execution, not only enqueue
A queued job may have been valid when created but execute after policy/authority/projection changes. Dependency completeness must include delayed execution paths, and consequence-bearing jobs should re-check the current prerequisites appropriate to the operation rather than treating enqueue-time authorization as eternal.

Guard: `authorized when queued ≠ authorized when executed`; `job retry ≠ reauthorization`.

## SYNTHESIS 12 — backups and restore environments can resurrect hidden edges
A graph can be complete for live stores yet incomplete after restoring an old snapshot containing stale queues, caches, exports or acknowledgement state. Restore validation must reconcile the restored dependency/proof generation with current policy/topology before consequence-bearing replay.

Guard: `backup restored ≠ dependency graph current`; `PITR success ≠ stale side effects safe to replay`.

## SYNTHESIS 13 — manual workflows need evidence without pretending humans are deterministic services
Operator procedures can create consequence-bearing copies/decisions. Model the controlled handoff, role, artifact, acknowledgement and exception where needed; do not infer exact execution merely because a runbook exists.

Guard: `procedure documented ≠ procedure executed`; `ticket closed ≠ downstream state proven`.

## SYNTHESIS 14 — closure proof is a recomputable evidence bundle
For a material consequence, closure should be derivable from current prerequisites plus a scoped completeness assertion. If a hidden edge is later discovered, retain the old closure as historical evidence, mark its assurance basis superseded/contradicted as appropriate, and recompute a successor closure.

Guard: `closure was reasonable then ≠ closure remains current now`; `new hidden edge ≠ delete old decision history`.

## SYNTHESIS 15 — negative predecessor tests extend to newly discovered surfaces
260 required proving controllable compromised predecessor paths are rejected. If 261 discovers a forgotten worker or offline replay endpoint, that surface joins the predecessor-rejection campaign before current closure can rely on its extinction.

Guard: `known predecessor paths blocked ≠ newly discovered path blocked`.

## SYNTHESIS 16 — product facts remain OPEN
This study does not assert that MintTap/LogMate has CDN caches, a particular Service Worker cache strategy, background sync, outboxes, dead-letter queues, webhooks, MDM, specific backup tooling, signed proofs or the listed manual workflows. They are discovery classes to test against canonical implementation evidence later.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. replace universal graph-completeness booleans with consequence-scoped completeness assertions;
2. maintain a versioned dependency-surface inventory spanning technical, offline, export, backup and manual paths;
3. combine multiple discovery channels and preserve contradictions/unknowns as assurance debt;
4. record newly discovered hidden edges as graph-correction provenance;
5. make negative evidence explicit about the searched surface/method;
6. block only consequences requiring unresolved assurance rather than destroying unrelated data/capability;
7. bind reauthorization proofs to graph/policy/verifier/schema/authority/topology assumptions;
8. invalidate/review proofs on material assumption changes, with TTL as a supplementary policy tool rather than the sole freshness mechanism;
9. include delayed jobs and restore paths in current-authorization checks;
10. recompute closure and predecessor-rejection evidence when a new dependency surface appears.

## EFB / LogMate-like application case
Assume a company iPad returns after a long offline interval with unique records and a P12 projection. Server-side investigation previously reauthorized P12→P20 and closed the incident under graph G20. Later, an old export worker W3 and a browser-local retry queue are discovered; both can still consume P12-era material.

Safe generic sequence:
1. preserve the iPad's unique records/provenance and old queue state;
2. do not treat G20 closure as timeless—record W3/queue discovery as graph correction G21;
3. classify whether W3 and each queued operation materially depend on revoked P12/K4 authority;
4. fence consequence-bearing replay while keeping unique data readable/recoverable;
5. inspect current worker/queue stores plus restore/dead-letter paths within the defined coverage boundary;
6. prove obsolete P12/K4 inputs are rejected on W3/current replay path where controllable;
7. revalidate/rebase only operations that remain legitimate under current policy/authority/schema;
8. issue successor completeness/reauthorization evidence bound to G21 and current topology/policy generations;
9. leave unsearched external/manual surfaces as explicit residual debt rather than claiming universal eradication;
10. do not factory-reset the iPad merely because the old graph was incomplete.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
841. **Recorded-graph completeness theater** — all stored edges traverse successfully, so system claims no hidden dependencies without surface inventory. Expected: fail.
842. **Telemetry-silence absence proof** — zero analytics events is treated as proof that no offline/manual/export consumer exists. Expected: fail.
843. **TTL-only proof freshness** — reauthorization remains current until 24h TTL despite material policy/topology change at minute 2. Expected: fail.
844. **Build-hash topology collapse** — unchanged app/Service Worker build is treated as proof that CDN/job/manual/export topology is unchanged. Expected: fail.
845. **Enqueue-time eternal authority** — delayed job executes under obsolete authority because it was valid when queued. Expected: fail.
846. **Restore hidden-edge resurrection** — PITR restores stale queue/cache state and replay occurs without graph/current-policy reconciliation. Expected: fail.
847. **Runbook-equals-execution** — documented remediation procedure or closed ticket is treated as proof that downstream recipient state changed. Expected: fail.
848. **New-edge closure inertia** — newly discovered consequence-bearing edge is added to graph but prior closure remains current without recomputation/predecessor rejection. Expected: fail.

**VALIDATION:** these are defined destructive cases, not executed PASS.

## Cross-track transfer
- **A → E:** cache/storage/Service Worker/navigation/queue mechanics enumerate technical persistence and replay surfaces; E decides consequence relevance and completeness policy.
- **E → B:** UX must represent incomplete coverage/reverification without false finality or destructive recovery; Design Studio owns reusable interaction validation.
- **E → C:** validation must inject hidden edges, topology changes, restore resurrection and stale proofs, including negative predecessor tests.
- **E → D:** measurement can quantify inventory coverage, unknown-edge debt and proof age/change-trigger latency; it cannot convert telemetry absence into dependency absence.

## External specialist boundary
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED** with physical-device/PWA, screen-reader and representative-human UX evidence OPEN. Software Engineering Studio remains **FOUNDATION STUDY UNDERWAY / no specialist Foundation PASS**; Safari Service Worker and generic offline-attestation evidence remain bounded transfer evidence only. Installed PWA, fresh-origin-down Safari cold start, physical iOS/iPadOS and canonical-product runtime remain OPEN. No external gate is promoted here.

## OPEN / VALIDATION
- actual MintTap/LogMate dependency-surface inventory and topology generation;
- actual Service Worker/cache/storage strategy and installed-PWA behavior;
- actual background jobs/outboxes/dead-letter/retry stores and execution-time authorization;
- actual export/report/email/webhook/integration destinations and recipient registry;
- actual backup/PITR/restore topology and stale-side-effect reconciliation;
- actual manual support/admin/aviation workflows and authority;
- exact policy for proof expiry/review triggers;
- physical managed-iPad/iPadOS/WebKit/MDM runtime;
- AT/human/security/incident-response validation.

## Gate result
**PASS (generic).** The Web Manager can now distinguish graph consistency from graph completeness, define consequence-scoped completeness evidence, systematically search hidden dependency surfaces, preserve negative-evidence boundaries, and expire/recompute reauthorization proof when material assumptions change without rewriting historical evidence or destroying unique offline data.

Production validation remains OPEN.

## Next high-value target
**262 — dependency-surface inventory drift, discovery-control failure & completeness-proof independence.** Study how the mechanism that inventories hidden dependencies can itself fail or be compromised; prevent a producer from self-certifying that all of its consumers are known; detect drift between declared and observed topology; and preserve an independent-enough completeness challenge path for long-offline PWA/EFB operations.