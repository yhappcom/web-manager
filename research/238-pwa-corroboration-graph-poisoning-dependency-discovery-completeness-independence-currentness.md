# 238 — PWA Corroboration-Graph Poisoning, Dependency-Discovery Completeness & Independence-Proof Currentness

Status: **PASS (generic) / PRODUCT + GRAPH-PROVENANCE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/client evidence; Track B uncertainty/containment UX; Track C destructive validation; Track D graph-observability diagnostics.  
Dependencies: 223–237, especially hidden-dependency discovery, drift/revalidation, contradiction intake and claim-scoped corroboration independence.

## Problem
237 established that corroboration is a claim-scoped dependency graph rather than a report count. That reasoning is unsafe if the graph itself is stale, incomplete or attacker-curated. A compromised control plane can omit a shared IAM recovery path, a provider migration can silently merge formerly independent collectors, an MDM rollout can make separate iPads consume one trust package, or inventory discovery can simply miss a dependency. The result is false `CROSS-DOMAIN` assurance even though every visible witness shares the same hidden failure domain.

Central rule: **independence is a time-bounded claim over a versioned, provenance-bearing dependency snapshot and an explicit discovery scope. Absence of a shared edge is not proof that no shared edge exists. Graph completeness is never assumed from self-attestation; material decisions must state discovery coverage, blind spots and freshness, and must fail toward `INSUFFICIENT-INDEPENDENCE` or narrow reversible containment when an unmodeled dependency could change the consequence judgment.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Supplies concrete browser/device/Service Worker/cache/storage/MDM relationships and distinguishes client-local observations from server/provider evidence. Browser surfaces cannot prove management-domain independence.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `GRAPH-CURRENT`, `GRAPH-STALE`, `DISCOVERY-INCOMPLETE`, `DEPENDENCY-CONFLICT`, `INSUFFICIENT-INDEPENDENCE` and precautionary-containment states without presenting an inventory count as certainty.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight graph-poisoning/discovery-currentness destructive cases; campaign expands **656 → 664 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures graph age, discovery coverage, unresolved edges, source concentration and revalidation latency. Telemetry cannot certify completeness or independence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns graph provenance, discovery scope, versioning, revalidation triggers, poisoning resistance and consequence policy under incomplete discovery.

## SOURCE

### NIST SP 800-61 Rev.3 — correlation is analysis input, not graph truth
NIST SP 800-61 Rev.3 is current final incident-response guidance, published April 2025. DE.AE-03 calls for correlating information from multiple sources, while potentially adverse events remain subject to analysis.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://doi.org/10.6028/NIST.SP.800-61r3

**TRANSFER VALIDATION:** correlation can reveal relationships only to the extent that collection and dependency knowledge are adequate. The standard does not justify treating an asset/dependency graph as complete merely because it contains multiple sources.

### NIST SP 800-18 Rev.2 — system plans include environment, components and internal/external data flows
NIST finalized SP 800-18 Rev.2 on 2026-06-30. NIST describes system plans as centralized references for system components, internal/external environments and data flows, with machine-readable data supporting lifecycle risk decisions.

Sources:
- https://csrc.nist.gov/News/2026/nist-releases-sp-800-18r2
- https://csrc.nist.gov/projects/risk-management

**TRANSFER VALIDATION:** lifecycle system/dependency representation is useful precedent for keeping graph context current. It does not prove that any one inventory source has discovered every operational or administrative dependency.

### CISA 2025 asset-inventory guidance — discovery and monitoring are continuing activities
CISA and partners' 2025 asset-inventory guidance emphasizes maintaining asset inventories, prioritizing critical assets and systems, understanding redundancy/operation under compromise, and monitoring for emerging conditions.

Source:
- https://www.cisa.gov/sites/default/files/2025-08/joint-guide-foundations-for-OT-cybersecurity-asset-inventory-guidance_508c.pdf

**TRANSFER VALIDATION:** this is bounded inventory precedent, not a MintTap topology prescription. It supports treating discovery as continuing evidence rather than a one-time enumeration.

## SYNTHESIS 1 — graph completeness is a scoped claim, never an implicit boolean
A dependency graph can only be called complete relative to a declared scope: affected capability, consequence boundary, failure hypothesis, dependency classes, environment and observation horizon. `all known dependencies mapped` is not equivalent to `all dependencies mapped`.

For a material independence decision record at least:
1. claim/capability and consequence boundary;
2. graph snapshot/version and creation time;
3. discovery methods/sources used;
4. dependency classes searched (identity, admin, provider, deployment, key/recovery, MDM, collector/parser, clock, storage, network where relevant);
5. known blind spots and inaccessible sources;
6. material changes since last validation;
7. independent observations/negative controls used to challenge the graph;
8. resulting assurance state and expiry/revalidation condition.

Persistent guard: `edge absent ≠ dependency absent`.

## SYNTHESIS 2 — self-attesting discovery cannot prove its own failure-domain independence
If the same provider-admin API supplies the dependency inventory, the evidence event and the statement that no shared admin dependency exists, compromise of that plane can curate all three. The graph needs cross-plane discovery where consequence warrants it: configuration/IaC, IAM/PAM/recovery, provider/account topology, audit exports, deployment metadata, MDM/trust distribution, runtime negative tests and organizational custody records as applicable.

No source is automatically privileged as universal truth. Differences become reconciliation work rather than `source A wins`.

Persistent guard: `inventory source authoritative for its objects ≠ inventory source complete for the trust cut`.

## SYNTHESIS 3 — graph poisoning includes omission, insertion and semantic relabeling
Poisoning is not limited to deleting an edge. An attacker or drift can:
- omit a shared dependency;
- invent a fake independent provider/path;
- split one principal into several aliases;
- merge distinct generations under one friendly name;
- relabel an administrative dependency as mere telemetry;
- alter timestamps/currentness;
- suppress a dependency-change event;
- retain a retired edge as if it were current, causing needless global containment.

Graph integrity therefore requires provenance for nodes/edges and semantic identity, not merely a hash of serialized graph bytes.

## SYNTHESIS 4 — independence proof is versioned and expires on relevant change
A prior `CROSS-DOMAIN` conclusion is bound to the dependency snapshot that supported it. Revalidate when a material dependency changes, including IAM federation/recovery, provider/account ownership, HSM/KMS/vault administration, CI/CD, collector/parser, audit export, MDM/trust package, service-worker release path, DNS/CDN/origin control or organizational custody where relevant.

Time alone can also make evidence stale when the environment is change-prone or discovery coverage ages beyond the decision's risk tolerance. Do not invent one universal TTL; define revalidation by consequence and observed change cadence.

Persistent guards: `historical graph PASS ≠ current graph PASS`; `no recorded change ≠ no change occurred`.

## SYNTHESIS 5 — missing change events are themselves a dependency risk
A graph that depends entirely on change notifications can remain falsely green if the notifier is compromised or misconfigured. Periodic or event-driven reconciliation must compare declared state with independently observable state where practical. Examples include IaC vs provider enumeration, IAM policy vs actual recovery/admin reach, MDM declaration vs device-received trust generation, and deployment registry vs runtime artifact identity.

`change feed quiet ≠ dependency stable`.

## SYNTHESIS 6 — discovery completeness and graph integrity are different assurance dimensions
A graph can be tamper-evident yet incomplete; it can be comprehensive at one instant yet later stale. Track separately:
- **integrity/provenance** — was recorded graph evidence altered or spoofed?;
- **coverage** — what dependency classes/surfaces were actually searched?;
- **currentness** — does the snapshot still represent the decision environment?;
- **semantic correctness** — do nodes/edges mean what policy assumes?;
- **independence conclusion** — does the resulting graph separate the relevant failure cut?

One green dimension cannot launder another red/unknown dimension.

## SYNTHESIS 7 — uncertainty must be consequence-partitioned
Incomplete discovery does not imply global shutdown. If local capture/read/export is demonstrably outside the uncertain trust cut, it may remain available. But an operation whose authorization depends on the allegedly independent witnesses cannot treat `unknown shared dependency` as `independent` merely for availability.

State model:
- `GRAPH-CURRENT` — scope and discovery evidence current enough for the stated claim;
- `GRAPH-STALE` — prior graph exists but material freshness is insufficient;
- `DISCOVERY-INCOMPLETE` — required dependency classes/sources are missing;
- `DEPENDENCY-CONFLICT` — sources disagree materially;
- `INSUFFICIENT-INDEPENDENCE` — graph cannot establish separation for the relevant failure hypothesis;
- `PRECAUTIONARY-CONTAINMENT` — narrow reversible restriction while high-consequence uncertainty is resolved.

## SYNTHESIS 8 — direct consequence tests can challenge a graph but cannot prove universal completeness
Suppose the graph says two verifier paths are independent. A fault injection or negative test that simultaneously breaks both can reveal a hidden shared dependency and should reopen the independence claim. Conversely, successful independent-looking tests do not prove no hidden shared dependency exists outside tested hypotheses.

Use runtime/destructive tests as contradiction generators against topology assumptions, not as magical completeness certificates.

## SYNTHESIS 9 — PWA/EFB management dependencies are easy to hide behind physical-device diversity
For a LogMate-like fleet, ten physical iPads can still share one MDM tenant, one pushed trust package, one identity-recovery plane, one app/PWA origin, one service-worker release artifact and one backend admission service. Physical diversity therefore does not establish trust-path diversity.

A graph should distinguish at least device-local state from management/trust distribution and server authority. Safari page, Service Worker and IndexedDB observations on one iPad remain client-local; separate iPads sharing the suspected MDM/trust dependency remain correlated for that hypothesis.

Exact iPadOS/WebKit/MDM behavior remains **OPEN** until physical runtime evidence exists. Unique flight/logbook data remains preservation-first under graph uncertainty.

## SYNTHESIS 10 — stale offline clients need graph-epoch-aware intake, not retroactive trust
A long-offline iPad may return carrying evidence created under an older dependency graph. Preserve the artifact and its graph/authority epoch. Do not reinterpret it as if produced under today's topology. Conversely, a stale client can reveal that a supposedly retired dependency remained reachable and therefore reopen a current independence/retirement claim.

`artifact fresh to device ≠ graph current to fleet`.

## SYNTHESIS 11 — graph provenance must not become a new authorization root
Signing/versioning a graph can protect provenance, but an authenticated graph still only states what was recorded. Authorization/admission remains governed by current authority/floor/policy. A signed stale or incomplete graph cannot grant consequence rights.

Persistent guard: `graph authentic ≠ graph complete ≠ graph current ≠ operation authorized`.

## SYNTHESIS 12 — graph compaction must preserve decision lineage
Long-running systems cannot necessarily retain every raw topology observation forever. Compaction may preserve checkpoints/summaries, but material decisions must retain enough provenance to explain which graph version, discovery scope, blind spots and dependency cut justified the decision and what later event reopened or superseded it.

Do not compact away the only evidence that two witnesses shared an administration plane at decision time.

## MINTTAP DECISION
For future MintTap/LogMate contradiction and recovery decisions, treat corroboration independence as a **versioned, claim-scoped assurance product**. Never infer independence from missing edges, report multiplicity or physical-device count. Material records should bind the decision to graph version, discovery coverage, known blind spots, failure hypothesis, consequence cut and revalidation trigger.

When required discovery is incomplete, label the result explicitly rather than synthesizing a complete graph. High-consequence uncertainty may trigger narrow reversible containment; unrelated capability may continue only when its trust cut is demonstrably independent.

This is generic architecture/security guidance, not a claim that MintTap or LogMate currently implements such a graph.

## DEPENDENCY / TRANSFER
- **Track A:** supply exact browser/device/runtime facts and distinguish device-local state from MDM/server/provider authority. Do not claim iPad independence from browser evidence alone.
- **Track B:** represent stale/incomplete/conflicting graph states and preserve user data/tasks during precautionary containment; consume Design Studio interaction evidence rather than inventing visual rules.
- **Track C:** own destructive tests that falsify hidden-independence assumptions and validate accessible degraded-state behavior.
- **Track D:** observe graph age/coverage/concentration/revalidation latency but never turn telemetry into completeness or authority.
- **Software Engineering:** implementation-level graph schema, collectors, reconciliation, tests and runtime fault injection become appropriate only with canonical product/source authorization.

## CONTRADICTION / FAILURE MODES
1. **Hidden IAM recovery edge:** two provider paths appear independent but one SSO/PAM recovery administrator controls both.
2. **Curated provider graph:** compromised provider-admin plane omits its own shared dependency and self-attests independence.
3. **Stale graph after migration:** collector B moves behind collector A's pipeline while old `CROSS-DOMAIN` decision remains green.
4. **Suppressed change event:** notification channel fails; no revalidation occurs despite dependency merge.
5. **Alias laundering:** one principal appears as multiple independent nodes through account/region aliases.
6. **Integrity-only false assurance:** signed graph is authentic but discovery never covered MDM or recovery paths.
7. **Managed-iPad physical-count laundering:** ten iPads are counted as independent although all receive the same suspect trust package.
8. **Offline stale-epoch reinterpretation:** artifact generated under graph G12 is evaluated as if generated under current G19.

## Track C destructive additions — 656 → 664 defined cases
Add eight defined cases corresponding to the failure modes above. Required oracle behavior:
- expose or conservatively classify hidden/shared dependency rather than count apparent witnesses;
- downgrade stale/incomplete graph assurance without deleting preserved evidence;
- keep affected consequence bounded while preserving unrelated demonstrably independent capability;
- retain unique offline client data;
- require revalidation after material topology change;
- never promote graph authenticity into authority.

**VALIDATION:** these are **defined cases**, not execution PASS. Physical iPad/iPadOS/WebKit/MDM, provider, graph-collector and product runtime validation remain OPEN.

## OPEN
- Actual MintTap/LogMate dependency graph/schema, collector inventory and graph provenance are unknown.
- Actual provider/IAM/PAM/KMS/HSM/vault/CI/CD/MDM failure domains are unknown.
- Exact revalidation triggers/SLAs and acceptable discovery blind spots require product risk/consequence evidence.
- Physical iPadOS/WebKit/MDM topology and stale-client behavior remain unvalidated.
- Legal/aviation/safety obligations may impose stronger retention/validation requirements and remain specialist/product evidence questions.

## CHANGE WATCH
- NIST SP 800-18 Rev.2 is final as of 2026-06-30; use it as current system-planning precedent.
- NIST SP 800-61 Rev.3 remains current final incident-response guidance as of this study.
- Provider inventory/audit/organization/identity and MDM APIs remain provider-specific and change-sensitive.
- Browser/OS PWA behavior remains platform-specific; physical iPadOS validation remains required before product claims.

## Gate judgment
**PASS (generic).** The adjacent generic competency is closed when Web Manager can explain why an authenticated graph can still be incomplete/stale, scope completeness claims, resist omission/insertion/alias poisoning, version independence conclusions, detect missing change-event risk, consequence-partition uncertainty and apply the model to long-offline managed-iPad PWA evidence without inventing production facts.

Production certification is not claimed.