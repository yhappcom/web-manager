# 278 — PWA Acceptance-Boundary Topology Attestation, Hidden-Bypass Discovery & Continuous Dormant-Authority Regression Control

Status: **PASS (generic) / PRODUCT + BACKEND + DEPLOYMENT + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime surfaces; Track B truthful degraded/rejoin UX; Track C destructive/regression validation; Track D topology/coverage diagnostics.  
Dependencies: 260–277 dependency completeness, topology discovery, authority/custody migration, bridge retirement, credential-lineage inventory and dormant-path eradication.

## Problem

277 established that credential inventory is a lineage-and-acceptance graph rather than a token table. That graph can be correct at one checkpoint and silently become incomplete after a route, worker, replica, provider, recovery path, compatibility deployment or rollback changes. A one-time clean inventory therefore decays unless topology change itself is governed and challenged.

Central rule: **acceptance-boundary completeness is a continuously maintained assurance claim over consequence-bearing effectors, not a static diagram. Material topology change must either update the attested boundary set or be contained until its authority semantics are classified. Discovery, telemetry and documentation are complementary evidence; none may silently elect authority.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns origin/scope, Service Worker control, browser navigation/storage/session mechanics and late-client behavior. Browser runtime observations cannot prove backend boundary completeness.
- **B UX/IA/Content:** high dependency pressure. Owns truthful `local data preserved`, `re-authentication required`, `sync temporarily limited`, `device requires rejoin` and recovery states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** destructive campaign expands **976 → 984 defined cases**. Execution, physical-device, AT and representative-human PASS remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Owns source reconciliation, coverage/drift diagnostics, unknown-boundary alerts and stale-path probe evidence; telemetry remains evidence, not authority.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns material-boundary definition, topology attestation, change coupling, hidden-bypass discovery, quarantine/retirement and rollback-resistant regression control.

## SOURCE

### NIST SP 800-53 Rev. 5.1 — CM-8 System Component Inventory

CM-8 requires an inventory that accurately reflects the system, includes all components within scope, uses sufficient tracking granularity and is reviewed/updated. CM-8(1) requires inventory updates as part of installations, removals and system updates; automated mechanisms may help maintain an up-to-date, complete and accurate inventory.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** this supports coupling inventory maintenance to topology change rather than relying only on periodic rediscovery. It does not define MintTap/LogMate acceptance boundaries or require a particular CMDB/scanner.

### NIST SP 800-137 / RMF Monitor — continuous monitoring

NIST's RMF Monitor step calls for ongoing situational awareness, ongoing assessment of control effectiveness, analysis of monitoring outputs and response. SP 800-137A separately treats both effectiveness and completeness of an information-security continuous-monitoring program as assessment concerns.

Sources: https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step and https://csrc.nist.gov/pubs/sp/800/137/a/final

**TRANSFER VALIDATION:** this supports treating topology assurance as a maintained control with completeness as well as effectiveness. It does not mean every system must poll every component continuously.

### OWASP API Security Top 10 2023 — API9 Improper Inventory Management

OWASP API9 describes old API versions, forgotten endpoints, exposed non-production hosts and outdated inventory/documentation as attack-surface risks. It recommends inventorying API hosts, versions, integrated services and endpoint characteristics, and incorporating documentation generation into CI/CD.

Source: https://api-security.owasp.org/editions/2023/en/0xa9-improper-inventory-management/

**TRANSFER VALIDATION:** this is concrete web/API precedent that deployed topology and documentation can diverge and that legacy/beta paths matter. OWASP guidance is not proof of the actual MintTap/LogMate deployment topology.

## SYNTHESIS 1 — acceptance boundary means material effect, not merely network endpoint

A boundary belongs in the attested set when it can directly or indirectly create a material consequence: mutate authoritative state, publish/finalize data, grant/recover authority, execute queued work, invoke privileged downstream action, or bypass a current admission decision.

Possible classes include API/resource-server routes, job consumers, background workers, admin/recovery interfaces, compatibility endpoints, webhook consumers, privileged server actions and provider control-plane paths. Static content routes are not automatically equivalent.

Guards:
- `route exists ≠ material acceptance boundary`;
- `not public ≠ non-consequence-bearing`;
- `internal worker ≠ outside authorization topology`.

## SYNTHESIS 2 — topology attestation is scoped and versioned

A useful attestation binds at least a defined environment/scope, material consequence classes, discovered boundary set, relevant deployment/configuration generation, evidence sources, known exclusions/UNKNOWNs and validation time/window. A bare statement such as `all endpoints covered` has no stable meaning if deployment state changes underneath it.

Guards:
- `inventory signed ≠ inventory current`;
- `topology hash unchanged ≠ runtime topology unchanged unless the hash covers the relevant sources`;
- `production covered ≠ staging/compatibility path cannot reach production effects`.

## SYNTHESIS 3 — change must invalidate or extend the completeness claim

Installations, removals and system updates are exactly where inventory drift can be introduced. For material systems, deployment/change governance should therefore produce one of three outcomes:
1. known boundary change is incorporated into the attested topology and required controls/tests;
2. change is classified non-material with reviewable rationale;
3. boundary semantics are UNKNOWN and the path is contained from high-consequence effects until resolved.

A successful deploy cannot inherit the prior completeness claim merely because the application health check is green.

Guards:
- `deploy healthy ≠ authorization topology unchanged`;
- `change approved ≠ boundary classification complete`;
- `route removed from source ≠ deployed route retired`.

## SYNTHESIS 4 — discovery must be multi-perspective

No single discovery source proves topology completeness. Useful perspectives can include:
- declared routes/API specifications;
- gateway/load-balancer/reverse-proxy configuration;
- deployment manifests and service/job inventories;
- runtime request/job telemetry;
- identity/provider clients and service principals;
- secret/service-account/KMS inventories;
- network/DNS/service discovery where applicable;
- admin/recovery runbooks and interfaces;
- backup/PITR/rollback manifests;
- active probes for retired/UNKNOWN generations.

Differences between perspectives are findings, not noise to normalize away.

Guard: `multiple inventory feeds ≠ independent evidence if they share one source of truth`.

## SYNTHESIS 5 — hidden bypasses are often semantic, not invisible

A route may be fully inventoried yet still bypass the intended authority path because it omits a middleware layer, trusts a legacy header, uses a service credential with broader scope, executes through a background queue, or calls a privileged downstream service directly. Topology completeness therefore needs **acceptance semantics**, not only endpoint enumeration.

Guards:
- `endpoint inventoried ≠ authorization path verified`;
- `same backend function ≠ same admission controls`;
- `gateway protected ≠ direct/internal invocation protected`.

## SYNTHESIS 6 — negative probes need consequence-aware coverage

A retired credential/generation should be challenged at representative material boundaries, especially privileged, compatibility, background and recovery paths. Testing every URL is neither necessary nor sufficient; equivalence classes must be justified by shared enforcement, deployment and consequence semantics.

If two routes are assumed equivalent because they share middleware, that shared middleware relationship becomes part of the assurance evidence.

Guards:
- `one predecessor rejection ≠ fleet-wide/path-wide retirement`;
- `same code repository ≠ same deployed enforcement`;
- `HTTP rejection ≠ queued/background rejection`.

## SYNTHESIS 7 — continuous control means event-driven plus periodic challenge, not constant polling

Useful regression control combines:
- change-triggered inventory/attestation updates;
- scheduled reconciliation across independent-enough sources;
- bounded active negative probes;
- alerts on unknown/new material boundaries;
- rollback/PITR exercises;
- incident-triggered re-attestation after compromise or topology uncertainty.

Polling frequency alone is not assurance. A deployment event that creates a bypass five minutes after a daily scan can matter immediately.

Guard: `frequent scan ≠ change-coupled control`.

## SYNTHESIS 8 — UNKNOWN boundary semantics must not silently become NORMAL

A newly discovered worker, endpoint or provider path may not immediately be classifiable. The safe generic state is explicit UNKNOWN with consequence-proportionate containment, not automatic admission and not destructive shutdown of unrelated safe capabilities.

High-consequence mutation/publication may be fenced while preserve/read/export/recovery functions remain available where independently safe.

Guards:
- `unknown path ≠ malicious path`;
- `unknown path ≠ trusted path`;
- `security uncertainty ≠ delete unique user data`.

## SYNTHESIS 9 — PWA runtime topology and server authority topology remain separate

Service Worker scope/control, Cache Storage, IndexedDB, navigation routes and local sessions are important Track A surfaces, but they do not enumerate API/job/admin acceptance boundaries. Conversely, a server-side topology attestation does not prove the installed/offline PWA is current.

A stale Service Worker may expose an old client route or queue format without possessing current remote authority. A current worker may still call a forgotten compatibility endpoint if application routing or configuration permits it.

Guards:
- `Service Worker route map complete ≠ backend topology complete`;
- `worker current ≠ endpoint current`;
- `endpoint retired centrally ≠ offline queue safely replayable`.

## SYNTHESIS 10 — long-offline EFB clients are latent callers, not hidden server boundaries

A disconnected company iPad can retain old URLs, queued operations, local credentials and cached code. It is part of the caller/unknown-tail population, not proof that an old server boundary still exists. Central closure can remain valid if current authoritative boundaries reject obsolete/UNKNOWN authority and removed boundaries cannot be resurrected by rollback.

On reconnect, the client needs current admission and operation-level reconciliation; unique flight/logbook records and provenance remain preserved.

Guards:
- `late client knows old endpoint ≠ old endpoint still exists`;
- `old endpoint returns 404 ≠ queued operation semantically reconciled`;
- `offline caller remains ≠ central migration can never close`.

## SYNTHESIS 11 — rollback and restore are topology mutation events

PITR, disaster recovery, blue/green rollback or provider restoration can reintroduce old routes, workers, allowlists, credentials or middleware. Restore success must therefore invalidate or re-evaluate topology/currentness attestations before obsolete authority can regain material effect.

Guards:
- `restore matches backup ≠ restore matches current authorization topology`;
- `rollback approved ≠ retired boundary may return`;
- `configuration restored ≠ predecessor acceptance remains forbidden`.

## SYNTHESIS 12 — telemetry proves observations, not impossibility

Track D should measure boundary-source coverage, new/unknown boundary age, predecessor/UNKNOWN attempts, rejection outcomes, deployment-to-attestation lag, negative-probe coverage and reconciliation contradictions. But zero observed bypass traffic cannot prove a dormant path cannot accept authority.

Useful assurance asks both:
- **effectiveness:** do known controls reject what they should?;
- **completeness:** have material paths and monitoring blind spots been bounded well enough for the claim?

Guards:
- `zero bypass events ≠ zero bypass capability`;
- `100% instrumented known boundaries ≠ 100% material topology known`;
- `monitoring healthy ≠ monitoring complete`.

## Integrated EFB / LogMate-like scenario

Hypothetical only; production facts remain OPEN.

G8 migration is declared centrally closed. A later deployment introduces a compatibility worker for an older queue format. The worker is absent from the API gateway route list but can invoke a privileged internal mutation service. Separately, a company iPad has been offline for six weeks with G7 queued operations.

Safe generic sequence:
1. preserve the iPad's unique records, queue bytes and provenance;
2. treat the new worker deployment as a topology-attestation invalidation/extension event;
3. discover the worker through deployment/job inventory even though API-route inventory is unchanged;
4. classify its privileged downstream call as a material acceptance boundary;
5. contain high-consequence effects while admission semantics are UNKNOWN;
6. verify the worker enforces current G8 identity/policy/schema/operation rules or redesign it so authority is checked at an authoritative downstream boundary;
7. actively prove G7/UNKNOWN operations cannot create material effects through the worker or direct internal service;
8. update the attested boundary graph and regression probes;
9. on iPad reconnect, perform current admission and operation-level reconciliation rather than blind replay;
10. exercise rollback/PITR so the pre-fix worker or G7 acceptance cannot resurrect.

This does **not** establish LogMate's actual queue, backend, provider, MDM, PWA or internal-service architecture.

## Track B transfer — truthful UX under topology uncertainty

Topology uncertainty should not be surfaced as invented technical detail. User-facing states can truthfully communicate `local records preserved`, `sync temporarily limited`, `sign in again before sync`, or `this device must rejoin before remote changes` where product evidence supports those states. Do not claim `all access removed`, `fully synchronized` or `fully current` from topology telemetry alone.

## Track D transfer — coverage diagnostics without authority laundering

Track D should correlate declared/deployed/runtime/provider/recovery sources, expose contradictions and age UNKNOWN boundaries. Coverage denominators must name their source set. A dashboard may report `18/18 known material boundaries probed` while separately retaining `topology completeness: bounded, one unresolved deployment source`; it must not collapse these into `100% secure`.

## Track C destructive campaign — 976 → 984 defined cases

Add eight cases:
1. **deploy-adds-unattested-worker** — a new background consumer can mutate authoritative state but the prior topology attestation remains green; must fail.
2. **gateway-inventory-equals-boundary-inventory** — all public routes are inventoried while an internal/admin path accepts stale authority; must fail.
3. **endpoint-enumerated-but-middleware-bypassed** — route is known but skips the current admission control; must fail.
4. **daily-scan-misses-immediate-bypass** — a material bypass exists between periodic scans and can execute before discovery; must fail.
5. **telemetry-silence-equals-no-capability** — dormant recovery path has no events but accepts predecessor authority when challenged; must fail.
6. **PITR-resurrects-retired-boundary** — restore brings back an old route/worker/allowlist that can create effects; must fail.
7. **worker-current-equals-server-topology-current** — current Service Worker is treated as proof that backend acceptance topology is current; must fail.
8. **offline-iPad-blind-replay-through-new-worker** — late G7 queue bypasses current admission through a compatibility worker; must fail.

These are **defined destructive cases**, not executed PASS.

## MINTTAP DECISION / DIRECTION

At generic Web Manager level:
- maintain acceptance topology as a versioned assurance object tied to material consequence, environment and deployment/configuration state;
- couple material deployments, removals, restores and rollbacks to topology re-attestation or explicit non-material classification;
- discover boundaries from multiple perspectives rather than relying on gateway/API documentation alone;
- model semantic bypasses, background jobs, admin/recovery and privileged internal calls as first-class candidates;
- use explicit UNKNOWN plus consequence-proportionate containment when boundary semantics are unresolved;
- require predecessor/UNKNOWN negative proof at representative material boundaries before retirement/closure claims;
- preserve historical evidence and unique offline user data independently from current authority;
- treat long-offline PWA clients as latent callers requiring current re-admission, not as reasons to keep obsolete authority alive;
- treat PITR/rollback as topology/currentness mutation requiring reconciliation;
- keep telemetry as evidence with declared coverage, never as an authority oracle.

## OPEN

Production validation remains OPEN for:
- actual MintTap/LogMate route, API, job, worker, admin/recovery, webhook and internal-service topology;
- gateway/CDN/origin/provider and environment boundaries;
- actual auth/session/token/service-credential enforcement placement;
- deployment manifests, route generation and CI/CD change controls;
- runtime/service-discovery and telemetry coverage;
- compatibility/legacy endpoint inventory and retirement behavior;
- Service Worker routes, offline queues and reconnect behavior on real iOS/iPadOS;
- managed-iPad/MDM/ADE/provider behavior;
- backup/PITR/rollback topology resurrection behavior;
- physical-device, AT, security/privacy, human and domain/legal/aviation validation.

## VALIDATION

Generic gate PASS requires the Web Manager to be able to:
1. distinguish endpoint inventory from consequence-bearing acceptance topology;
2. explain why completeness is a maintained/versioned assurance claim;
3. couple topology mutation to re-attestation or containment;
4. reconcile declared, deployed, runtime, provider and recovery evidence without treating one source as omniscient;
5. identify semantic bypasses that endpoint enumeration alone misses;
6. design consequence-aware predecessor/UNKNOWN negative tests;
7. separate PWA client/runtime state from server authority topology;
8. preserve unique offline data while fencing stale authority;
9. treat rollback/PITR as topology mutation;
10. distinguish monitoring effectiveness from monitoring completeness.

Result: **PASS (generic).** Product/runtime claims remain OPEN.

## CHANGE WATCH

- NIST SP 800-53/CM-8 and related continuous-monitoring guidance revisions;
- OWASP API Security Top 10 inventory-management revisions;
- browser/WebKit/Chromium Service Worker and storage lifecycle changes;
- provider/gateway/serverless/job-platform discovery and rollback behavior relevant to future canonical product architecture.

## Next highest-value adjacent work

**279 — topology-attestation provenance, change-event authenticity & poisoned-discovery resistance**: determine how deployment/inventory events and discovery feeds are authenticated, how compromised CI/CD or telemetry cannot self-attest a malicious hidden path as legitimate, how contradictory topology sources are preserved and adjudicated, and how long-offline/rollback recovery consumes a trustworthy topology lineage without turning the attestation system itself into a new super-root.