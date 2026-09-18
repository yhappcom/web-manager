# 129 — PWA Resilience-Debt Retirement & Recovery-Objective Evidence Governance

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 103–128 recovery/assurance chain; Track A PWA lifecycle/client-generation mechanics; Track C recovery drills and objective evidence; Track B degraded/recovery-state UX; Software Engineering for implementation evidence.

## Purpose

128 established change-sensitive dependency graphs and a local resilience-budget model. 129 addresses the next lifecycle failure: temporary bridges, stale alternate paths, old recovery credentials, compatibility fallbacks and untested runbooks can accumulate because removing them feels less safe than retaining them.

Central rule:

> **A recovery path earns continued existence by serving a current recovery objective with current executable evidence; age, documentation, redundancy count or historical usefulness are not sufficient reasons to retain it.**

This study uses `resilience debt` as a local synthesis, not a NIST term.

## 1. Five-track balance

- **A Platform/Browser — dependency supplier:** Service Worker/client generations, origin continuity, local storage and stale-client behavior determine whether a central recovery path can actually recover an installed PWA.
- **B UX/IA/Content — consumer:** degraded/manual/recovery-only states need truthful capability language; retiring a path must not strand a promised user recovery journey.
- **C Quality — high dependency pressure:** owns recovery-objective timing/data-loss evidence, destructive drills, stale-path failure tests and retirement regression.
- **D Search/Analytics — consumer:** telemetry can help discover path use but absence of events does not prove an alternate is unused, especially for offline populations.
- **E Architecture/Security/Operations — highest-risk owner:** owns objective definition, path inventory, debt classification, retirement/replace/re-prove decisions and residual-risk acceptance.

Allocation remains E-heavy with A/C as principal dependencies.

## 2. SOURCE — recovery objectives are consequence boundaries

NIST SP 800-34 Rev.1 distinguishes Maximum Tolerable Downtime (MTD), Recovery Time Objective (RTO), and Recovery Point Objective (RPO). RTO bounds how long a resource can remain unavailable before unacceptable mission/business impact; RPO identifies the point in time to which data must be recovered after an outage. RTO normally must fit within MTD, while RPO expresses tolerated data loss rather than downtime.

Sources checked 2026-09-18:
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf
- https://csrc.nist.gov/glossary/term/Recovery_Time_Objective
- https://csrc.nist.gov/glossary/term/recovery_point_objective

**SYNTHESIS:** a recovery mechanism should be evaluated against the consequence/objective it exists to satisfy, not against a generic `backup exists` or `failover exists` checkbox.

Guards:
- `recovery path exists ≠ recovery objective met`;
- `restore succeeds eventually ≠ RTO met`;
- `latest backup exists ≠ RPO met`;
- `RTO met ≠ integrity/provenance restored`.

Actual MintTap/LogMate RTO/RPO/MTD values remain **OPEN**.

## 3. SOURCE — recovery paths require exercise and maintenance

NIST contingency-planning guidance treats testing/training/exercises and plan maintenance as part of the contingency lifecycle. NIST SP 1339 (2026-06-17), although written for OT and therefore not directly a web/PWA requirement, reinforces a durable operational principle: backups should be integrated with change management, created regularly, tested, and reviewed during recovery exercises.

Sources:
- https://www.nist.gov/publications/contingency-planning-guide-federal-information-systems
- https://www.nist.gov/publications/ot-backup-quick-start-guide

**TRANSFER VALIDATION:** a documented alternate that has not been exercised after material dependency/schema/key/provider change is stale evidence, not current recovery assurance.

Guard: `runbook retained ≠ recovery path executable`.

## 4. SOURCE — redundancy must be maintained, not accumulated

NIST SP 800-160 Vol.2 Rev.1 states that redundancy can enhance critical-capability availability but redundant resources must be protected; redundancy/diversity can also increase complexity and scalability challenges. The extent of redundancy should be established and maintained through analysis of single points of failure and shared resources.

Source:
- https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final

**SYNTHESIS:** obsolete alternates can become liabilities: standing credentials, old APIs, stale secrets, forgotten DNS, vulnerable software, divergent data formats and false monitoring can increase attack surface while contributing no proven recovery value.

Guards:
- `more alternate paths ≠ more usable resilience`;
- `path retained for safety ≠ path is safe to retain`;
- `resilience control added ≠ resilience debt retired`.

## 5. Local resilience-debt model

A path creates or carries **resilience debt** when it remains part of the declared recovery posture but one or more of these is true:
1. its current recovery objective is unclear;
2. its dependencies materially changed since the last proof;
3. its credentials/keys/software remain live without demonstrated need;
4. its runbook or automation is stale;
5. it cannot meet current RTO/RPO/consequence bounds;
6. it duplicates another path without covering a distinct failure mode;
7. it creates compatibility/security obligations for obsolete client generations;
8. monitoring still reports it healthy despite no executable proof;
9. nobody owns its maintenance/retirement decision;
10. a temporary incident bridge has no expiry or conversion decision.

Debt is not automatically bad. A deliberately tolerated manual path may be cheaper and safer than permanent hot redundancy. The failure is **unpriced, unowned, untested or falsely represented debt**.

## 6. Recovery-path lifecycle states

Use explicit states rather than `enabled/disabled`:
- **CURRENT-PROVEN** — serves a current objective and has current evidence;
- **CURRENT-MANUAL** — deliberately manual but proven within the objective;
- **STALE-REPROVE** — objective remains, evidence invalidated by age/material change;
- **REPLACE** — objective remains but path no longer meets it or has unacceptable risk;
- **RETIRE-CANDIDATE** — no unique current objective/failure mode justifies maintenance;
- **RETIRE-IN-PROGRESS** — authority, credentials, monitoring, docs and dependencies are being removed;
- **RETIRED-VERIFIED** — path cannot silently regain authority and remaining references are reconciled;
- **UNKNOWN** — evidence/dependency facts insufficient.

Guard: `retirement approved ≠ path retired`.

## 7. Keep, re-prove, replace, retire

**Keep** when the path covers a current named failure mode, consequence warrants it, lifecycle cost/risk is proportionate, and evidence is current.

**Re-prove** when the objective and design remain valid but evidence is stale after dependency, key, format, provider, schema, browser or organizational change.

**Replace** when the objective remains but the mechanism no longer meets timing/data-loss/security/provenance constraints or a simpler safer mechanism now covers the same failure mode.

**Retire** when no current objective/failure mode uniquely depends on it, or its residual attack/operational cost exceeds justified resilience value.

Do not retire merely because a path has not been used in production; successful resilience mechanisms may rarely be invoked. Use objective + drill + dependency evidence, not invocation count alone.

Guard: `zero production use ≠ recovery path unnecessary`.

## 8. Recovery-objective evidence packet

For each essential capability/path, maintain a bounded evidence packet:
1. named capability and failure scenario;
2. consequence and MTD/RTO/RPO or explicit bounded manual-recovery expectation where applicable;
3. protected data/authority/provenance requirements;
4. primary and alternate path;
5. dependency/cut-set version;
6. last material change;
7. last destructive or representative exercise;
8. measured restore/rebuild/re-entry duration;
9. measured recoverable data point/data-loss interval where relevant;
10. integrity/provenance validation result;
11. stale/offline-client result where relevant;
12. owner and next change/review trigger;
13. debt state and decision: keep/re-prove/replace/retire;
14. OPEN assumptions.

This is not a demand for universal enterprise BCM tooling.

## 9. RTO/RPO are not complete PWA recovery semantics

For PWA/EFB, central RTO/RPO can miss installed-client realities. Separate at least:
- origin/service availability;
- Service Worker publication;
- installed worker fetch/install/activate/control convergence;
- local data readability/durability;
- authentication/current trust generation;
- queued-operation reconciliation;
- remote mutation authorization;
- provenance/integrity of recovered records.

A server can meet a central RTO while an offline iPad remains on an old worker indefinitely. Conversely, an iPad may retain useful local records while the origin is unavailable.

Guards:
- `origin RTO met ≠ installed-client recovery complete`;
- `central RPO met ≠ device-local unsynced data recovered`;
- `client opens offline ≠ sync/replay authorized`.

## 10. Temporary bridge debt

Incident-created compatibility endpoints, emergency credentials, alternate DNS/origins, manual export/import paths and broad allowlists require an explicit post-incident disposition:
- convert into a supported permanent path with normal controls;
- keep as bounded emergency capability with owner/exercise/expiry triggers;
- replace;
- retire and verify removal.

A bridge that survives because removal is frightening is not evidence of resilience.

Guards:
- `temporary bridge still works ≠ bridge should remain supported`;
- `bridge removal risky ≠ indefinite bridge retention safe`.

## 11. Retirement must remove authority, not history

Retiring a path should address as applicable:
- credentials/tokens/keys;
- DNS/origin/routes;
- API generations and allowlists;
- CI/CD/IaC targets;
- provider accounts/roles;
- monitoring/health checks;
- documentation/runbooks;
- backup schedules and storage cost;
- incident/break-glass references;
- stale-client compatibility assumptions.

Historical evidence may remain for audit/incident provenance. Do not erase history merely to remove runtime authority.

Guards:
- `runtime path retired ≠ historical evidence deleted`;
- `monitor removed ≠ authority removed`;
- `credential revoked ≠ every stale client converged`.

## 12. PWA/EFB retirement boundary

A central obsolete API/worker/recovery bridge can be retired while preserving local read/export for an old offline iPad, provided product-specific design supports it. Retirement must not silently broaden stale-client authority to avoid user-data loss.

Returning clients should encounter explicit states such as `local recovery available`, `update/re-entry required`, `sync blocked`, or `reconciliation required`, rather than an unsafe compatibility bypass.

Actual managed-iPad/WebKit/MDM/storage/background/direct-sync behavior remains **OPEN** and requires runtime evidence.

## 13. Track C validation campaign

High-value tests:
1. restore meets declared RTO under primary-provider loss;
2. recovered data meets declared RPO;
3. integrity/provenance validation is separate from RTO/RPO;
4. stale runbook fails visibly rather than receiving a paper PASS;
5. key/schema/provider change marks evidence STALE;
6. manual path is timed end-to-end, including human handoff;
7. obsolete alternate requires revoked credential and is rejected;
8. retired DNS/API/CI route cannot regain authority;
9. monitoring no longer reports retired path healthy;
10. historical evidence remains readable after runtime retirement;
11. emergency bridge expiry does not strand irreplaceable local data;
12. old PWA retains local read/export where designed;
13. old worker cannot use retired remote mutation generation;
14. clean origin recovery does not falsely mark offline fleet converged;
15. compromise-era outbox remains quarantined after re-entry;
16. recovery path that meets RTO but violates integrity fails the overall gate;
17. recovery path that restores data but misses RPO fails the data objective;
18. duplicate alternate covering no distinct cut set is flagged as retirement candidate;
19. retirement removes standing privilege and provider cost without removing required evidence;
20. replacement path is proven before old path authority is removed where continuity requires overlap;
21. overlap window is bounded and does not become permanent dual authority;
22. rollback of retirement cannot silently reactivate obsolete credentials;
23. owner departure triggers revalidation of manual recovery;
24. telemetry absence is not treated as proof that offline clients/path users do not exist;
25. objective change reopens keep/replace/retire decision;
26. low-consequence path can intentionally remain manual;
27. high-consequence path cannot be kept on paper evidence alone;
28. recovery exercise records actual duration/data point, not only PASS/FAIL;
29. retirement references are removed from incident runbooks;
30. post-retirement negative canary confirms obsolete authority remains denied.

## 14. Cross-track transfer

**Track A:** supplies browser/Service Worker/storage mechanics; 129 does not redefine them.  
**Track B:** owns truthful recovery/degraded-state information requirements, not infrastructure policy.  
**Track C:** owns executable evidence and objective measurement.  
**Track D:** path-use analytics is supporting evidence only; offline populations and failed telemetry prevent absence-of-use claims.

## 15. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-18: **W080 RESET-BASELINE + NAVIGATION CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Cross-browser/Safari/Firefox, persisted configuration, screen-reader, physical-device, field-CWV and human UX remain OPEN. This supports honest state/evidence boundaries but is not recovery-objective proof.

Software Engineering implementation evidence remains a handoff boundary; concrete timing, persistence, crash/power-loss, browser/device and sync claims require project/runtime validation. Marketing does not own recovery objectives; public reliability claims must not exceed operational evidence.

## 16. MINTTAP DIRECTION

For a small app company, prefer a small number of **named, current, proven recovery paths** over a large inventory of nominal alternates. Keep manual recovery when consequence permits it. Retire obsolete runtime authority aggressively but preserve historical evidence and irreplaceable user data. Do not invent production RTO/RPO values before business/product evidence exists.

## 17. OPEN / VALIDATION / CHANGE WATCH

**OPEN:** actual MintTap/LogMate criticality, MTD/RTO/RPO, authoritative local data, backup topology, provider dependencies, managed-iPad behavior, recovery owners, legal/safety constraints and current alternate paths.

**VALIDATION:** product-specific destructive drills, real restore timing, data-loss interval, integrity/provenance checks, stale-client re-entry and retirement negative tests.

**CHANGE WATCH:** NIST contingency/recovery guidance; browser/WebKit PWA behavior; provider recovery semantics; storage/background capabilities; project architecture and dependency topology.

## 18. Persistent guards

`recovery path exists ≠ recovery objective met`.  
`restore succeeds eventually ≠ RTO met`.  
`latest backup exists ≠ RPO met`.  
`RTO met ≠ integrity/provenance restored`.  
`runbook retained ≠ recovery path executable`.  
`more alternate paths ≠ more usable resilience`.  
`path retained for safety ≠ path is safe to retain`.  
`zero production use ≠ recovery path unnecessary`.  
`retirement approved ≠ path retired`.  
`runtime path retired ≠ historical evidence deleted`.  
`origin RTO met ≠ installed-client recovery complete`.  
`central RPO met ≠ device-local unsynced data recovered`.  
`temporary bridge still works ≠ bridge should remain supported`.

## Gate

**PASS (generic).** The Web Manager can now connect recovery mechanisms to explicit consequence/objective evidence, identify resilience debt, distinguish keep/re-prove/replace/retire decisions, and apply the model to PWA/offline-client recovery without inventing production objectives. Product/provider/managed-iPad validation remains OPEN.

## Next high-value adjacent work

**PWA recovery-objective conflict & graceful-degradation governance:** resolve cases where availability RTO, data-integrity/provenance, privacy/security, offline usefulness and stale-client retirement objectives conflict. Define which capabilities may degrade, which must fail closed, and how product UX communicates partial recovery without converting an availability objective into unsafe remote authority.