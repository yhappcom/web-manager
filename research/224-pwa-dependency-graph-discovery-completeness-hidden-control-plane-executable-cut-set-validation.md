# 224 — PWA Dependency-Graph Discovery Completeness, Hidden-Control-Plane Detection & Executable Cut-Set Validation

Status: **PASS (generic) / PRODUCT + DISCOVERY-PIPELINE + PROVIDER + RECOVERY + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline mechanics; Track B degraded/recovery UX; Track C executable validation; Track D coverage/drift telemetry.  
Dependencies: 117–137, 171–223, especially 215 inventory attestation, 218–223 distributed currentness, assurance debt and dependency-graph partial reauthorization.

## Problem
223 made partial reauthorization depend on a typed, claim-specific dependency graph and a proven unaffected trust cut. The next failure mode is circular: if the graph is built only from the architecture/configuration source that omitted the dangerous path, graph traversal will confidently prove the wrong cut. Hidden provider consoles, break-glass credentials, CI/update roots, DNS/registrar authority, recovery/PITR paths, MDM, legacy APIs, Service Worker routes, SaaS delegation and human emergency authority can remain consequence-bearing even when absent from the declared diagram.

Central rule: **dependency completeness is not an absolute Boolean. Build material graph edges from independent discovery planes, preserve source/provenance and explicit unknown coverage, challenge declared cuts with positive and negative executable tests, and scope every completeness claim to a capability, edge class, environment and observation interval. A graph cannot prove its own completeness merely by containing everything its generator knew to ask for.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Browser route/control scope, Service Worker fetch/update behavior, storage/session state and reconnect paths are discovery targets; browser APIs do not establish policy authority.
- **B UX/IA/Content:** very high dependency pressure. Must communicate UNKNOWN/RESTRICTED/PARTIALLY-READMITTED states without converting discovery uncertainty into a global failure claim.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **544 → 552 defined cases**; executable cut validation remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can quantify source coverage, stale-edge rate, orphan observations and validation outcomes; telemetry cannot prove complete discovery or authorize recovery.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns discovery-source reconciliation, hidden-control-plane challenge, edge provenance, coverage semantics and executable trust-cut validation.

## SOURCE

### NIST SP 800-53 / SP 800-53A — inventory, monitoring and assessment are distinct evidence activities
NIST SP 800-53 Rev.5 includes configuration-management and continuous-monitoring controls such as system component inventory and monitoring; SP 800-53A Rev.5 supplies assessment procedures. The useful precedent is that declared inventory/control state and evidence that controls are implemented/effective are separate concerns.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** these controls do not define a MintTap dependency graph or completeness algorithm. They support requiring inventory/monitoring/assessment evidence instead of treating a design document as executable proof.

### NIST SP 800-70 Rev.5 — machine-readable/executable configuration evidence and unauthorized-change detection
NIST SP 800-70 Rev.5 (May 2026) describes security configuration checklists that can be machine-readable/executable, verify configuration and identify unauthorized configuration changes.

Source:
- https://doi.org/10.6028/NIST.SP.800-70r5

**TRANSFER VALIDATION:** a configuration checklist is one discovery/validation plane, not a complete authority/dependency inventory. Runtime, provider-admin and recovery paths can exist outside the checklist's modeled surface.

### NIST NCCoE asset-management project — incomplete inventory impairs risk understanding
NCCoE's June 25, 2026 initial public draft project description for OT asset management explicitly notes that incomplete inventories impair understanding of cybersecurity risk and proposes automated/manual discovery, inventory, configuration and change-management approaches.

Source:
- https://csrc.nist.gov/pubs/pd/2026/06/25/asset-management-as-a-foundation-for-ot-cybersecur/ipd

**CHANGE WATCH / TRANSFER VALIDATION:** this is an initial public draft and OT-focused. It is useful only as current precedent that multiple discovery methods and lifecycle change management matter; it is not a Web/PWA dependency-graph standard.

### CISA Log4Shell guidance — multiple methods and broad asset scope
CISA/FBI/NSA partner guidance for Log4Shell directs organizations to inventory affected assets, including cloud assets, and to verify mitigations with more than one method where possible.

Source:
- https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a

**TRANSFER VALIDATION:** vulnerability discovery is not equivalent to authority-path discovery. The reusable principle is independent-method reconciliation and explicit tracking of known/suspected assets.

### NIST IR 8613 — multi-cloud control is structurally difficult
NIST IR 8613 Initial Public Draft (August 21, 2026) identifies security/compliance challenges amplified across autonomous cloud silos.

Source:
- https://csrc.nist.gov/pubs/ir/8613/ipd

**CHANGE WATCH / TRANSFER VALIDATION:** this is a draft, not a MintTap architecture rule. It reinforces that provider/region multiplicity can increase control-plane discovery and consistency problems rather than proving independence.

## SYNTHESIS 1 — use independent discovery planes, not one authoritative-looking source
Build candidate nodes/edges from several evidence planes:
1. declared architecture/IaC/configuration and policy;
2. cloud/provider IAM, organization/project/account and admin configuration;
3. DNS/registrar/certificate/key/signing/update configuration;
4. CI/CD/deployment/package provenance;
5. runtime request/authorization/service-call observations;
6. audit/security/change logs;
7. recovery/PITR/backup/runbook and break-glass procedures;
8. endpoint/browser/Service Worker/MDM configuration and observed behavior;
9. SaaS/vendor delegation and supplier evidence;
10. manual challenge/interview only as attributed evidence, never as silent truth.

No plane is universally superior. Reconciliation asks why an edge appears in one source but not another.

`IaC declared ≠ all control paths declared`; `runtime observed ≠ dormant recovery path absent`; `audit log silent ≠ authority absent`; `provider inventory present ≠ application consequence modeled`.

## SYNTHESIS 2 — classify observations as declared, observed, inferred or unknown
Every material edge should carry provenance and epistemic state. Useful classes:
- **DECLARED** — configuration/specification says the edge exists;
- **OBSERVED** — runtime/control-plane evidence demonstrates it;
- **INFERRED** — evidence supports a bounded relationship but direct execution is unavailable;
- **CONTRADICTED** — sources disagree materially;
- **UNKNOWN** — required edge class/scope has insufficient evidence.

Freshness attaches to the evidence source and claim, not merely the graph file.

`declared + observed agreement > declared alone`, but `two agreeing sources ≠ complete universe`; `fresh source ≠ complete source`; `inferred edge ≠ executed edge`.

## SYNTHESIS 3 — discover hidden control planes by consequence-oriented challenge
Start from a capability and ask who/what can change its code, authorization, routing, data, identity, evidence or recovery state. Then search for alternate administrative paths rather than only request-flow dependencies.

High-value challenge classes include cloud root/org roles, provider consoles/APIs, DNS/registrar, certificate issuance, CI secrets, signing/KMS/HSM admin, package registries, feature flags, policy stores/evaluators, support/admin tools, MDM, backup/PITR, break-glass accounts, scheduled jobs, legacy endpoints, Service Worker/update channels and third-party SaaS delegation.

An edge is material when compromise/uncertainty can change the assurance claim under test.

`not on request path ≠ not consequence-bearing`; `read-only UI ≠ read-only control plane`; `dormant path ≠ extinct path`; `manual path ≠ outside system security`.

## SYNTHESIS 4 — quantify coverage without claiming impossible absolute completeness
Do not report “100% dependency complete” without a closed, defensible denominator. Instead report scoped coverage such as:
- required edge classes assessed / required edge classes defined for capability C;
- known enforcement/admin/recovery surfaces reconciled / current versioned denominator;
- orphan observations not mapped to graph;
- declared edges lacking observation where observation is feasible;
- observed edges lacking declared owner/provenance;
- UNKNOWN/CONTRADICTED material edges;
- age/change generation of each evidence source.

A useful result is `CUT VALIDATED FOR CLAIM C UNDER SCOPE S AT GENERATION G; unknown tail U remains outside/inside consequence boundary`, not `graph complete`.

`100% of known denominator ≠ absolute completeness`; `zero orphan today ≠ no hidden path`; `coverage metric ≠ authority`.

## SYNTHESIS 5 — executable cut-set validation requires positive and negative oracles
For proposed unaffected capability C and trust cut K:

**Positive tests:** current authorized identity/policy/code path can perform the allowed operation; required current policy/evaluator/signing generations are observed; data/provenance semantics remain valid.

**Negative tests:** retired/stale credentials, old policy, old Service Worker/legacy route, recovery snapshot, provider-console bypass, break-glass path or affected shared root cannot authorize/mutate C beyond the permitted scope.

Test the alternate path itself where feasible. A successful primary path does not exercise rejection at the bypass path.

`positive PASS ≠ negative-path PASS`; `negative test at gateway ≠ negative test at provider/recovery path`; `test harness cannot reach path ≠ path rejected`.

## SYNTHESIS 6 — validate recovery and rollback as graph mutation events
PITR, backup restore, failover, region recreation and disaster recovery can resurrect nodes/edges that production discovery had retired. Treat recovery as a graph transition requiring re-discovery/reconciliation before consequence-bearing rejoin.

The validation oracle is not merely “service works after restore.” It includes current authority floor, current dependency graph generation, extinct-path rejection and evidence-plane continuity.

`restore succeeded ≠ graph current`; `configuration restored ≠ retired authority still retired`; `region healthy ≠ region re-admitted`.

## SYNTHESIS 7 — PWA/offline clients create dormant edges that online telemetry undercounts
A long-offline PWA can retain cached code, Service Worker routing, credentials/session artifacts, local schema, queued operations and old endpoint knowledge. These edges may be invisible to current server runtime until reconnect.

Do not count “no calls to legacy endpoint” as extinction while an offline cohort capable of invoking it remains unresolved. On reconnect, preserve unique local data, update/reconcile code/policy/schema as required, then execute negative/positive admission tests for consequence-bearing queued operations.

`zero online legacy calls ≠ zero dormant legacy clients`; `Service Worker update offered ≠ update installed`; `client reconnect ≠ dormant edge extinct`.

Exact iPadOS/WebKit storage/background/update behavior remains runtime evidence, not inferred here.

## SYNTHESIS 8 — contradictions are discovery output, not noise to normalize away
If provider IAM says principal P can mutate resource R but IaC says no such path exists, preserve CONTRADICTED and investigate. If runtime shows an edge not in the declared graph, create an orphan observation rather than silently attaching it to the nearest expected node.

Contradiction can widen a blast radius until resolved. It must not be averaged away by more green sources.

`source disagreement ≠ majority vote`; `unexpected edge ≠ telemetry defect by default`; `orphan observation ≠ safe to ignore`.

## SYNTHESIS 9 — discovery pipelines themselves have authority and failure domains
Collectors/scanners need access and can be compromised, scoped incorrectly or lag behind changes. Record collector identity, permissions, source scope, collection generation and failure state. Where a high-consequence cut depends on discovery, use independent corroboration or direct challenge from a different failure domain.

This inherits 219–220 witness rules: evidence origin/integrity does not prove truth, completeness or independence.

`scanner authenticated ≠ scan complete`; `collector success ≠ source scope complete`; `two scanners sharing API/credential ≠ two independent discovery planes`.

## SYNTHESIS 10 — executable validation must be safe, reversible and consequence-scoped
Negative tests should not require destructive production compromise. Prefer controlled fixtures, staging mirrors, provider policy simulators where authoritative, read-only enumeration, canary identities/resources, bounded rejection probes and recovery drills with explicit rollback/evidence capture.

For claims that cannot be tested safely, retain INFERRED/OPEN rather than manufacturing PASS. Product safety/legal/aviation boundaries may require specialist approval before active tests.

`untestable safely ≠ assumed safe`; `simulation PASS ≠ production enforcement PASS`; `staging topology similar ≠ production topology identical`.

## MINTTAP DECISION / DIRECTION
1. Build dependency graphs by reconciling independent declared/configuration, provider/control-plane, runtime, audit, recovery and endpoint evidence planes.
2. Attach provenance, generation/freshness and DECLARED/OBSERVED/INFERRED/CONTRADICTED/UNKNOWN state to material edges.
3. Search explicitly for hidden administrative, update, recovery, break-glass and offline-client paths; do not restrict discovery to primary request flow.
4. Express completeness only against a versioned scoped denominator and publish unknown/orphan/contradicted tails.
5. Require positive allowed-operation and negative stale/bypass/recovery rejection tests for a high-consequence unaffected trust cut where safe/feasible.
6. Treat PITR/failover/recovery and long-offline reconnect as graph reconciliation events.
7. Preserve contradictions as assurance debt until resolved; never majority-vote them away.
8. Treat discovery collectors as evidence-plane components with their own scope/failure domains.
9. Use safe, reversible validation; retain OPEN where production-equivalent testing is unavailable.
10. Keep these generic directions separate from actual MintTap/LogMate topology until canonical runtime/project evidence exists.

## OPEN / DEPENDENCY
- Actual MintTap/LogMate discovery sources, graph schema, denominator and edge provenance: **OPEN**.
- Provider/IAM/DNS/CI/signing/policy/recovery/admin/break-glass topology: **OPEN**.
- Exact legacy/bypass endpoint and Service Worker/update paths: **OPEN**.
- Managed-iPad/iPadOS/WebKit/MDM offline cohort and update behavior: **Track A + Software Engineering runtime dependency**.
- Product-safe active test authorization and aviation/legal/safety constraints: **OPEN**.
- Capability-specific degraded/recovery UX: **Track B consuming Design Studio; physical/human/AT validation OPEN**.

## Track C destructive campaign — 544 → 552 defined cases
Add:
1. **IaC monoculture false completeness:** graph is generated only from IaC and misses a manually created provider-admin path.
2. **Runtime-only false extinction:** zero observed traffic to a legacy endpoint is treated as extinction while dormant recovery/offline clients can still invoke it.
3. **Scanner-scope omission:** discovery job succeeds but its credential cannot enumerate organization/root-level IAM, hiding a shared authority edge.
4. **Orphan normalization:** unexpected runtime/control-plane observation is automatically mapped to an expected node and the hidden edge disappears.
5. **Positive-only cut validation:** current path succeeds, but stale credential through provider/recovery bypass is never rejection-tested.
6. **PITR graph resurrection:** restore brings back retired policy/endpoint/configuration while current graph artifact remains unchanged and falsely green.
7. **Correlated discovery planes:** two scanners appear independent but use the same provider API/credential and share the same blind spot.
8. **Long-offline iPad dormant edge:** online fleet shows zero legacy use; returning device has stale Service Worker/endpoint knowledge and queued writes. Preserve unique data, reject stale authority, reconcile graph/current policy, then re-admit per operation.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** browser/Service Worker/offline mechanics supply discoverable edges and mixed-epoch behavior; exact Safari/iPadOS behavior remains execution evidence.
- **Track B:** uncertainty must be communicated by capability/state rather than a global “secure/unsafe” label.
- **Track C:** executable positive/negative cut tests, recovery drills and physical-device/browser validation are required before product PASS.
- **Track D:** coverage/orphan/drift metrics diagnose the graph but cannot prove completeness or authorize a capability.
- **Design Studio:** Web remains W121 / Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/iPadOS/EFB and canonical-product runtime remain OPEN.

## Persistent guards added
`IaC declared ≠ all control paths declared`; `runtime observed ≠ dormant recovery path absent`; `audit log silent ≠ authority absent`; `provider inventory present ≠ application consequence modeled`; `fresh source ≠ complete source`; `not on request path ≠ not consequence-bearing`; `dormant path ≠ extinct path`; `manual path ≠ outside system security`; `100% of known denominator ≠ absolute completeness`; `zero orphan today ≠ no hidden path`; `positive PASS ≠ negative-path PASS`; `test harness cannot reach path ≠ path rejected`; `restore succeeded ≠ graph current`; `zero online legacy calls ≠ zero dormant legacy clients`; `Service Worker update offered ≠ update installed`; `source disagreement ≠ majority vote`; `scanner authenticated ≠ scan complete`; `collector success ≠ source scope complete`; `untestable safely ≠ assumed safe`; `simulation PASS ≠ production enforcement PASS`.

## Gate result
**224 PASS (generic).** The knowledge gate closes because multi-plane graph discovery, edge provenance/state, hidden-control-plane challenge, scoped coverage semantics, positive/negative executable cut validation, recovery/offline graph mutation, contradiction handling and discovery-plane failure boundaries now have explicit evidence rules and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**225 — dependency-graph drift detection, change-triggered revalidation & stale-proof expiry**: determine which architecture/provider/IAM/CI/recovery/Service Worker changes invalidate prior cut proofs, how evidence TTL should be claim/change based rather than arbitrary time alone, how to avoid both permanent re-testing and stale-proof reuse, and how long-offline clients are admitted when the server's dependency proof generation has advanced multiple times.