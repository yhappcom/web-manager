# 235 — PWA Closure-Proof Retention, Evidence-Store Compromise & Post-Closure Contradiction Handling

Status: **PASS (generic) / PRODUCT + EVIDENCE-STORE + PROVIDER + BACKUP + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A stale-client/runtime boundary; Track B closure/reopened-state UX; Track C destructive validation; Track D evidence observability.  
Dependencies: 160–165 closure-evidence/retention foundations; 211–212 long-horizon evidence migration; 223–234 dependency/currentness, recovery, destruction and resurrection-proof closure.

## Problem
234 made destruction closure provenance-bound and separated provider lifecycle evidence from current-authority negative enforcement. The next failure mode is temporal: closure evidence itself can later be corrupted, deleted, become unverifiable, lose verifier context, or be contradicted by newly discovered residual material, a stale verifier, a restore path or a previously hidden control plane. A naive system either treats old PASS as eternal, or rewrites history and invalidates everything when one later contradiction appears.

Central rule: **a closure proof is a retained historical claim plus a current dependency judgment, not an authority credential and not an eternal truth token. Retain the minimum non-secret evidence needed to verify the historical claim for its required horizon; protect evidence integrity and verifier context without letting the evidence store authorize current consequences; and when new evidence contradicts a closure assumption, preserve the original historical event, reopen only the affected current claim and its transitive dependents, contain current consequence paths, and revalidate before re-closing.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker, browser storage and stale-client state can reveal contradictions to current closure assumptions but remain client-relative historical evidence, not server authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible CLOSED / EVIDENCE-DEGRADED / REOPENED / CONTAINED / REVALIDATING states while consuming Design Studio interaction evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight evidence-loss/contradiction destructive cases; campaign expands **632 → 640 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures evidence age, verification failures, contradiction discoveries and reopen latency; telemetry cannot authorize closure or suppress contradiction.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns retention horizon, evidence integrity, verifier survivability, evidence-store compromise response, claim reopening, dependency blast radius and re-closure governance.

## SOURCE

### NIST SP 800-92 — retention must preserve usable, integrity-checkable evidence
NIST SP 800-92 remains NIST's published Guide to Computer Security Log Management. It treats log management as an infrastructure/process problem spanning generation, transmission, storage, analysis and disposal. Its archive guidance calls for periodically checking whether archived formats risk becoming inaccessible, migrating them when needed, verifying integrity after transfer (for example with message digests), securely storing archival media and destroying logs after the required retention period under sanitization policy.

Sources:
- https://csrc.nist.gov/pubs/sp/800/92/final
- https://doi.org/10.6028/NIST.SP.800-92

**TRANSFER VALIDATION:** closure-proof packages are not ordinary logs, but the durable-evidence principles transfer: retained bytes that cannot be interpreted or integrity-checked at the verification horizon are not useful retained proof.

### NIST SP 800-53 Rev.5 AU-11 — retention period follows verification need, not arbitrary permanence
AU-11 requires audit records to be retained for an organization-defined period consistent with records-retention policy so they remain available for after-the-fact investigation and applicable regulatory/organizational needs. The control does not imply retaining every record forever.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** evidence retention should be derived from the claim's investigation, recovery, legal/operational and supported-client horizon. `important evidence ≠ retain every payload forever`.

### RFC 9162 Certificate Transparency — append-only evidence improves auditability but does not make the log an authority oracle
RFC 9162 uses Merkle trees, signed tree heads, inclusion proofs and consistency proofs to make append-only behavior auditable. It also explicitly notes that inconsistent views can defeat a client that sees only one view; monitors/auditors and cross-view comparison matter. The log detects/records behavior; it does not itself prevent certificate misissuance or decide the business response.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** an append-only or transparency-style evidence store is a useful integrity precedent, not a requirement that MintTap use Certificate Transparency or a blockchain. More importantly, `tamper-evident evidence ≠ current authorization authority` and `one consistent view ≠ no hidden contradictory view`.

## SYNTHESIS 1 — retain claims, not retired capability
A closure package should retain the minimum material necessary to reconstruct what was asserted and why:
- closure claim ID/type/scope;
- exact object/material/generation identifiers and safe fingerprints;
- lifecycle event/receipt identifiers and timestamps;
- successor/admission-floor generation relevant at closure;
- negative-oracle identities/results and environment identifiers;
- residual-copy/restore/reimport disposition;
- evidence-source provenance and integrity digest/reference;
- verifier/schema/algorithm version needed to interpret the package;
- dependencies and their generations at closure;
- retention class/horizon and legal/operational hold where applicable;
- later supersession/reopen/re-close links.

Do not retain private recovery/signing material merely so the old proof can be reproduced. `retain closure proof ≠ retain retired authority capability`.

## SYNTHESIS 2 — retention horizon is claim-specific
There is no generic `forever` or `90 days` answer. Retention is bounded by the longest material verification need among supported restore/PITR windows, stale-client/bootstrap horizons, incident/investigation needs, applicable records obligations, contractual/audit needs and successor-lineage verification needs. When one need expires, data minimization may justify reducing detail while preserving a smaller checkpoint sufficient for the remaining claim.

A shorter provider audit-log window does not automatically define the closure-proof horizon. Conversely, an old proof whose dependent system and supported recovery horizon are extinct need not be retained at full fidelity solely because it once existed.

`provider log retention ≠ closure-proof retention`; `retention expired ≠ historical event becomes false`; `historical value ≠ unlimited payload retention`.

## SYNTHESIS 3 — evidence store is not an authority root
The evidence store may say that authority generation G18 was retired. Current admission must still be enforced by current policy/floor/verifier state, not by granting the evidence database a privileged `allow/deny` capability.

If an attacker can edit the proof store but cannot change the current admission floor, they may damage auditability but should not resurrect G18. If editing the proof store alone can make G18 current, the architecture has accidentally promoted evidence into authority.

`proof-store says CLOSED ≠ operation authorized`; `proof-store compromise ≠ predecessor automatically resurrected`; `evidence availability ≠ enforcement availability`.

## SYNTHESIS 4 — integrity, availability and interpretability are separate evidence properties
A retained package can fail in different ways:
- bytes altered → integrity failure;
- package missing → availability failure;
- signature/hash algorithm or verifier unavailable → verifiability failure;
- schema/canonicalization context lost → interpretability failure;
- provenance binding lost → attribution/scope failure;
- evidence still valid but dependency changed → currentness failure.

These must not collapse into one `proof invalid` flag. Recovery differs: restore a missing replica, migrate verifier context, reconstruct from independent sources, or reopen current claims when dependency assumptions changed.

`bytes intact ≠ proof interpretable`; `signature verifies ≠ proof current`; `evidence missing ≠ historical event disproven`.

## SYNTHESIS 5 — evidence-store compromise requires bounded downgrade
If the evidence store is suspected compromised, freeze/preserve the suspect state, identify the compromise interval and affected namespaces, compare independent provider receipts/audit exports/checkpoints/negative-runtime evidence, and downgrade only claims whose required provenance or integrity can no longer be established. Current consequence enforcement should remain on current floor/policy paths.

Do not automatically accept all old authorities because audit evidence is unavailable; do not silently keep all closure claims green either. Use explicit `EVIDENCE-DEGRADED` or `REOPENED` states according to whether current safety is still independently established.

`evidence compromised ≠ authority compromised automatically`; `authority still fenced ≠ evidence closure still fully proven`.

## SYNTHESIS 6 — contradiction is an append, not a rewrite
Suppose G18 provider destruction was correctly observed and closed, then six months later an exported G18 private-key copy is discovered. The provider destruction event remains historically true. What changes is the residual-copy/universal-erasure claim and any current-authority claim that depended on `no usable G18 copy remains`.

Record the contradiction as a new evidence event linked to the original closure. Preserve both. Reopen affected claims and transitive dependents rather than editing the old receipt into nonexistence.

`later contradiction ≠ erase historical event`; `historical event true ≠ original closure scope still current`; `reopen claim ≠ declare every prior observation fraudulent`.

## SYNTHESIS 7 — reopen by dependency blast radius
Use the closure dependency graph from 223–226. A newly discovered residual copy may reopen:
- material-erasure/residual-copy claim directly;
- current-authority retirement only if the copy can reach a verifier/admission path or satisfy a threshold;
- restore/rejoin closure if the copy exists in a supported recovery artifact;
- unrelated capability closures only when an explicit dependency path exists.

Unknown impact is not proof of no impact: if graph completeness is uncertain across the affected cut, widen containment/revalidation until the boundary is established.

`one contradiction ≠ global invalidation`; `no known dependency ≠ proven independence`; `unknown blast radius ≠ safe unaffected state`.

## SYNTHESIS 8 — containment precedes forensic certainty when consequence is plausible
A contradiction can be ambiguous: an old key copy is found but its provenance is unclear. If it plausibly satisfies a current threshold or can reach a stale verifier, consequence-bearing paths should be fenced while provenance is investigated. Unique local/offline data should remain preserved.

This is not the same as declaring compromise proven. State can be `CONTAINED / REVALIDATING` while attribution remains OPEN.

`contradiction discovered ≠ attacker proven`; `attacker not proven ≠ continue consequence path unchanged`.

## SYNTHESIS 9 — re-closure requires successor evidence, not deletion of the contradiction
Re-closing an affected claim requires evidence that addresses the new fact: for example successor/floor advancement, stale-verifier retirement, threshold change under valid authority, residual-copy containment/destruction where supportable, restore-path negative tests and updated inventory reconciliation. Merely deleting the discovered copy or marking the incident resolved is insufficient if another path can still admit predecessor authority.

Re-closure creates a successor proof generation linked to the reopened claim. It does not mutate the old PASS into a timeless PASS.

`contradiction artifact deleted ≠ contradiction resolved`; `incident closed ≠ closure proof current`; `re-close ≠ rewrite old proof`.

## SYNTHESIS 10 — long-offline PWA clients are contradiction sources, not disposable evidence
A LogMate-like iPad can return after months with a stale worker, old trust metadata, queued operations or a previously unknown local export. That can contradict assumptions about fleet convergence or stale-authority extinction. Preserve unique flight/logbook data first. Quarantine consequence-bearing replay, acquire current trust, inspect the stale tail, then re-admit operations individually.

Do not wipe/reinstall the device to make the contradiction disappear. Browser-local evidence can reopen a fleet-convergence or stale-verifier claim; it still cannot prove or disprove provider physical deletion by itself.

`stale client discovered ≠ local data disposable`; `client reset ≠ contradiction resolved`; `old queued operation authentic ≠ current admission authorized`.

## SYNTHESIS 11 — evidence-store replication is not evidence independence
Two replicas under the same identity/admin/KMS/backup failure domain improve availability but may not improve compromise independence. Stronger closure packages may combine independently controlled provider event exports, application negative-oracle results, immutable/tamper-evident checkpoints and separately governed retention copies, but independence is claim-relative and must be mapped rather than assumed.

`two evidence copies ≠ two independent witnesses`; `WORM/append-only ≠ correct evidence`; `signed evidence ≠ complete evidence`.

## SYNTHESIS 12 — contradiction metrics are operational signals, not adjudicators
Track D may measure reopen count, contradiction age, proof-verification failures, evidence-reconstruction latency, stale-client discoveries and time-to-recontain. These metrics identify drift and operational debt. They must not automatically suppress a contradiction because frequency is low or auto-close a claim because a dashboard is green.

`zero contradiction alerts ≠ no contradiction exists`; `low event rate ≠ low consequence`; `dashboard green ≠ closure authorized`.

## MINTTAP DECISION / DIRECTION
1. Store closure as versioned claim/evidence objects with dependency generations and supersession/reopen links; never as an unqualified eternal boolean.
2. Retain the minimum non-secret proof package for a claim-specific verification horizon derived from restore, stale-client, investigation and applicable obligation needs.
3. Keep current admission authority outside the closure-evidence store. Evidence-store compromise must not itself resurrect retired authority.
4. Preserve verifier/schema/canonicalization context needed to interpret retained proof; integrity-only retention is insufficient.
5. On evidence-store compromise, preserve suspect evidence, reconcile independent sources and downgrade affected claims without inventing certainty.
6. Treat later contradiction as append-only new evidence. Preserve the historical event and reopen affected current claims/dependents rather than rewriting history.
7. Use dependency-graph blast radius; widen containment when independence cannot be established.
8. Contain plausible consequence before attribution is complete, while preserving unique local/offline data.
9. Re-close with a successor proof generation that directly addresses the contradiction and re-runs required negative oracles.
10. Treat long-offline PWA/iPad stale tails as valuable contradiction sources; never wipe unique data to simplify closure evidence.

## DEPENDENCY / TRANSFER
- **Track A:** supplies browser/Service Worker/storage semantics for stale-tail discovery and bootstrap. Client state remains bounded evidence.
- **Track B / Design Studio:** consumes explicit CLOSED, EVIDENCE-DEGRADED, REOPENED, CONTAINED, REVALIDATING and BOOTSTRAP-REQUIRED states. Visual/interaction treatment remains Design Studio-owned.
- **Track C:** owns execution of proof-store corruption, verifier-loss, contradiction/reopen and long-offline destructive cases when implementation exists.
- **Track D:** observes evidence health and contradiction/reopen latency but cannot adjudicate authority.
- **Software Engineering:** exact evidence schema/store, append-only/tamper-evident implementation, verifier migration, restore harness and dependency-graph evaluator remain implementation handoffs. Current Studio evidence does not establish product or physical iPad runtime.

## Track C destructive additions — 632 → 640 defined cases
1. **Proof-store authority promotion:** attacker edits closure row from REOPENED to CLOSED and current admission begins accepting predecessor → fail architecture separation.
2. **Integrity-only archive:** bytes/digest survive but schema/verifier/canonicalization context is gone and proof cannot be interpreted → fail long-horizon verifiability.
3. **Evidence-store compromise blanket resurrection:** audit store compromise causes system to accept every retired authority as fallback → fail bounded downgrade.
4. **Evidence-store compromise false green:** suspect interval affects required proof but UI/control plane leaves closure silently CLOSED → fail evidence semantics.
5. **Residual-copy contradiction rewrite:** exported predecessor key is discovered and original provider-destruction event is deleted/edited rather than linked to a reopened residual-copy claim → fail provenance.
6. **Global invalidation without dependency:** one unrelated closure contradiction disables independent local-capture/read capability despite a proven separate trust cut → fail bounded blast radius.
7. **Contradiction auto-close:** discovered stale verifier is marked resolved after telemetry quiets without negative predecessor test → fail re-closure evidence.
8. **Long-offline iPad evidence destruction:** returning iPad exposes stale authority/queued operations and is wiped before unique data/evidence preservation; closure remains green → fail data-preserving contradiction handling.

These are **defined cases, not execution PASS**.

## VALIDATION
Generic PASS requires the Web Manager to distinguish historical fact from current closure, retention from authority, integrity from interpretability/currentness, and contradiction from historical rewrite; derive claim-specific retention; contain evidence-store compromise without accidental authority fallback; reopen by dependency blast radius; and re-close with successor evidence. This artifact meets that reasoning gate.

Production PASS remains OPEN until exact evidence-store schema/topology, retention policy, verifier migration, provider/audit exports, dependency graph, current admission enforcement, restore/reimport behavior and managed-iPad stale-tail evidence exist.

## OPEN
- Actual MintTap/LogMate closure-evidence store, replicas, IAM/KMS/admin and backup failure domains.
- Exact retention obligations/horizons for product, aviation, investment, incident and provider evidence.
- Exact proof schema, verifier/canonicalization versions, migration and long-horizon re-verification process.
- Exact contradiction intake, dependency-blast-radius evaluator, containment and re-closure workflow.
- Actual provider/audit export independence and evidence-loss recovery capability.
- Physical iPad/Safari/WebKit/MDM stale-tail discovery and data-preserving evidence acquisition.

## CHANGE WATCH
- NIST log-management guidance and SP 800-53 audit/retention controls can evolve; monitor revisions.
- Cryptographic/verifier deprecation can make retained proof uninterpretable unless migration/reattestation is planned.
- Provider audit export/retention and backup semantics are mutable.
- Managed iPad/WebKit storage/update/runtime behavior remains execution-sensitive.

## Gate result
**PASS (generic).** Track E remains highest-risk owner. Track C destructive campaign reaches **640 defined cases**, with execution PASS explicitly unclaimed.

## Adjacent-value check
The next adjacent issue is materially distinct but directly follows the new reopen model: **236 — contradiction intake authenticity, adversarial false-reopen resistance & evidence-poisoning containment**. A malicious actor can manufacture or flood apparent contradictions to force perpetual containment, while a compromised intake/triage plane can suppress real contradictions. This deserves a separate checkpoint because it changes from retained-proof semantics to hostile-input/adjudication semantics.

## Next highest-value target
**236 — contradiction intake authenticity, adversarial false-reopen resistance & evidence-poisoning containment.** Determine how to accept untrusted contradiction reports without letting them directly change authority, how to preserve plausible high-consequence reports while triaging provenance, how to resist denial-of-service through false reopen floods, and how to prevent a compromised intake/triage system from suppressing real residual-copy/stale-verifier/restore-path evidence.