# 105 — PWA Recovery-Risk Release Governance, Rollout Gates & Forward-Only State

Status: **PASS (generic) / PRODUCT RELEASE POLICY + TARGET-RUNTIME VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 089/092 release and installed-client evidence as indexed; 091 long-offline compatibility; 098 revocation; 099 trust-policy authenticity; 100–104 recovery chain/objectives; Track A service-worker lifecycle; Track B truthful update/recovery UX; Track C fault/recovery validation; Track D privacy-bounded rollout evidence; Software Engineering Q006/D003/D005/D006/Q003.

## Purpose

104 established that recovery objectives are a vector and that failure/exposure budgets govern action rather than permission to lose irreplaceable records. This study asks the next operational question: **when must a release be slowed, frozen, or rejected because it weakens recoverability, and what does rollback mean when code can move backward but user data, schema, trust state, or remote effects may already have moved forward?**

This is a generic governance model. It does not define MintTap/LogMate numeric thresholds, CI implementation, deployment provider, database migration framework, or managed-iPad runtime behavior.

---

## 1. Track allocation and bottleneck

- **A Platform/Browser — critical dependency supplier.** Service-worker waiting/activation/control, cache coexistence and installed-client update lag constrain release semantics.
- **B UX/IA/Content — consumer.** Owns truthful states for update available/required, local records preserved, sync paused, recovery required and unsupported-client boundaries.
- **C Performance/Accessibility/Quality — major validation consumer.** Owns release/recovery fault campaigns, exact-artifact evidence, accessibility of degraded states and regression sensitivity.
- **D Search/Discovery/Analytics — bounded consumer.** Rollout health measurement must not mistake missing long-offline telemetry for success or leak recovery metadata.
- **E Architecture/Security/Operations — primary owner.** Owns release gates, exposure-budget escalation, compatibility horizons, emergency stop/containment and rollback/recovery policy.

**Allocation:** E remains the highest-risk bottleneck; A and C are the strongest dependencies. Do not duplicate generic CI/CD or database implementation theory owned by Software Engineering.

---

## 2. SOURCE — controlled deployment is a reliability control

CISA/FBI/ACSC's *Safe Software Deployment* guidance recommends controlled deployment, including canary/small-scale rollout, monitoring before wider release, gradual expansion and an automatic breaker or emergency stop capability during incidents. It also recognizes that some customers intentionally remain on N-1/N-2 releases.

Source: https://www.cisa.gov/sites/default/files/2024-10/safe-software-deployment-how-software-manufacturers-can-ensure-reliability-for-customers-508c.pdf

NIST's current DevSecOps reference model says release teams gather evidence that changes passed needed tests and operations validates production readiness and rollback procedures. NIST SSDF remains the higher-level secure-development framework; its current 2025 initial public draft revision is change-sensitive and is not treated as final normative policy.

Sources:
- https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- https://csrc.nist.gov/projects/ssdf
- https://csrc.nist.gov/pubs/sp/800/218/r1/ipd

**SYNTHESIS:** release is not merely artifact publication. It is a controlled expansion of exposure whose velocity should depend on evidence and whose stop conditions must be defined before the incident.

**Guards:**
- `build passed ≠ rollout safe`;
- `artifact published ≠ installed fleet converged`;
- `canary healthy ≠ long-offline cohort compatible`;
- `rollback procedure exists ≠ user state can safely move backward`.

---

## 3. PWA release state is distributed across code, worker, caches and durable user state

The Service Worker lifecycle deliberately permits an updated worker to install and wait while the old worker continues controlling existing clients. A new worker normally activates after old controlled pages close; `skipWaiting()` can force earlier activation and `clients.claim()` can take control of existing clients. Service-worker registrations also persist beyond individual page objects.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting

web.dev warns that immediate activation can mix a new worker with pages/resources expecting the old version; old caches also need explicit cleanup. Chrome/Workbox guidance specifically warns that `skipWaiting` can break lazy-loaded uniquely-versioned resources if activation purges resources still expected by the current page.

Sources:
- https://web.dev/articles/service-worker-mindset
- https://developer.chrome.com/docs/workbox/modules/workbox-core

**SYNTHESIS:** a PWA release has multiple simultaneous generations: document/app shell, service worker, caches, database/schema, trust/policy, API/protocol and outbox/remote effects. A release gate must reason about supported combinations, not merely a single semantic version.

**Guards:**
- `new worker installed ≠ new worker controlling every client`;
- `new worker active ≠ every open document built for that worker`;
- `code version N ≠ cache/schema/trust/API generation N`;
- `origin deploy complete ≠ installed-client migration complete`.

---

## 4. Release-risk budget: change consumes evidence margin, not user records

104 adapted error-budget thinking into recovery exposure. A release should consume a **recovery-risk budget** when it changes a component required to preserve, interpret, recover or reconcile authoritative local data.

High-risk change classes include:
1. schema/data-model migration;
2. encryption/key hierarchy or recovery-key change;
3. service-worker/cache/update strategy;
4. backup/export/import format;
5. trust-policy/protocol generation;
6. sync/outbox/idempotency semantics;
7. API retirement or server compatibility window;
8. origin/storage partitioning or identity boundary;
9. browser/OS support floor affecting recovery capability.

The budget is not a numeric permission to lose data. It is a governance signal controlling rollout velocity and evidence requirements.

**MINTTAP DIRECTION (generic company rule):** the more a release changes recovery-critical generations simultaneously, the stronger the pre-release compatibility/restore evidence and the smaller the initial exposure should be. Exact thresholds remain OPEN.

**Guards:**
- `small code diff ≠ small recovery risk`;
- `feature flag off ≠ migrated local state rolled back`;
- `release success rate high ≠ recovery-critical cohort safe`.

---

## 5. Minimum release-gate evidence for recovery-critical changes

A recovery-critical release should not progress solely on unit/build success. Generic evidence gates are:

### Gate A — exact-artifact identity
Bind evidence to build/worker/schema/protocol/key-policy identifiers and target support envelope. Avoid accepting stale evidence from a different artifact.

### Gate B — forward migration
Prove supported predecessor states can migrate to the candidate without losing authoritative records, outbox identity, tombstones, trust metadata or required recovery information.

### Gate C — interruption/fault recovery
Inject failure before mutation, during migration, after local apply/before acknowledgement, and after acknowledgement where applicable. Use an independent semantic oracle.

### Gate D — backup/restore compatibility
Restore applicable old and new artifacts into isolated candidates; validate integrity/provenance, keys, reader/schema/domain semantics and reconciliation before publication.

### Gate E — mixed-generation compatibility
Exercise supported combinations of old document/new worker, new document/old worker where possible, old client/new API, old backup/new reader, pending outbox/new protocol and long-offline N-k client/current authority.

### Gate F — degraded/recovery UX
Confirm the user can still access authoritative local records and understand update required, sync paused, recovery required or unsupported-client states without destructive coercion; validate keyboard/zoom/AT/browser behavior in the applicable product harness.

### Gate G — rollout observability and breaker
Define rollout cohorts, independent success/failure oracles, privacy-bounded signals, stop criteria and containment action before expansion.

### Gate H — recovery from rollback decision
Demonstrate what happens if the candidate code is withdrawn after some clients have already advanced durable state.

**DEPENDENCY:** Software Engineering Q006 supplies the reusable method `fault point → recovery action → independent terminal-state oracle → regression sensitivity`; D003/D005/D006 supply schema/restore/replay semantics. These are methodology dependencies, not PWA runtime PASS.

---

## 6. Forward-only durable state: rollback code, not blindly data

A central failure mode is assuming deployment rollback means all system state can return to the previous release.

After release N+1, a client may already have:
- migrated DB/schema;
- rewritten encrypted records or keys;
- advanced trust/protocol generation;
- emitted operations accepted remotely;
- created records only representable by the new model;
- rotated backup format;
- deleted/retired old cache resources.

Returning origin code to N does not undo those effects and may make N unable to read them.

**SYNTHESIS:** durable user/trust state should generally be treated as **forward-moving** unless an explicit, tested, lossless reverse migration exists. Operational rollback therefore often means **code containment + compatibility bridge + forward repair**, not destructive state reversal.

**Guards:**
- `code rollback ≠ schema rollback`;
- `code rollback ≠ key/trust rollback`;
- `code rollback ≠ remote side effect rollback`;
- `old binary restored ≠ old state representation restored`;
- `down migration implemented ≠ down migration lossless`.

**MINTTAP DIRECTION:** prefer additive/backward-compatible or expand→migrate→contract transitions for recovery-critical data where practical; do not require old code to read a state generation it was never designed to understand unless that compatibility is explicitly tested.

---

## 7. Roll-forward vs rollback decision model

When a release breaches a recovery objective, candidate actions are distinct:

1. **Pause expansion** — stop exposing additional clients while collecting evidence.
2. **Disable optional feature path** — only if the flag does not pretend already-migrated state reverted.
3. **Keep new reader, disable new writer** — useful where newly written state is risky but reverting reader compatibility would strand data.
4. **Compatibility bridge** — keep server/API/reader support for both generations while clients converge.
5. **Forward repair** — deploy N+2 that understands already-advanced state and fixes the defect.
6. **Code rollback** — safe only when the old code's compatibility with already-advanced durable state is demonstrated.
7. **Quarantine sync/bridge** — preserve local records/outbox while preventing unsafe remote effects.
8. **Emergency trust/security containment** — may justify faster worker activation or capability disablement, but still must preserve authoritative local data where possible.

**Operational judgment:** for a PWA with durable offline records, roll-forward repair is often safer than blind rollback once state migration has escaped into the fleet. This is a conditional design principle, not a universal prohibition on rollback.

---

## 8. Service-worker activation is itself a release-governance decision

Default waiting behavior reduces mixed-version takeover risk but delays fixes until old clients release control. `skipWaiting()` accelerates activation but can create a new-worker/old-page combination; `clients.claim()` further expands immediate control.

**MINTTAP DIRECTION:** do not use unconditional `skipWaiting()+clients.claim()` merely to make deployment appear instant. Activation policy should depend on compatibility evidence and severity.

Generic policy classes:
- **routine compatible release:** permit normal waiting/user-coordinated activation;
- **breaking shell/worker relationship:** require a controlled reload/update UX after local work is safely committed;
- **urgent security containment:** accelerated activation may be justified, but validate that it cannot destroy unsaved/authoritative local state or strand recovery paths;
- **bad worker incident:** publish a correcting worker under the existing registration path; deleting/renaming the worker file alone does not remove already registered workers.

Source: https://web.dev/learn/pwa/update

**Guards:**
- `faster activation ≠ safer recovery`;
- `security urgency ≠ permission to destroy unsynced local records`;
- `worker file removed from origin ≠ installed worker removed from clients`.

---

## 9. Long-offline clients make rollout completion an evidence problem

CISA's N-1/N-2 consideration maps strongly to offline PWAs, but a long-offline EFB can miss many generations, not merely one. Server/API/key/trust retirement must therefore be governed by the declared compatibility horizon and recovery path.

A rollout dashboard that sees only connected clients has survivorship bias. A silent old client may reappear later with authoritative records and an outbox.

**SYNTHESIS:** rollout completion requires a definition such as “all observed eligible clients converged plus the declared stale-client recovery/retirement policy is in force”; it cannot mean “no errors from currently online clients.”

**Guards:**
- `no old-client telemetry ≠ no old clients exist`;
- `connected fleet converged ≠ long-offline fleet recoverable`;
- `API retirement date reached ≠ stale authoritative records expendable`.

---

## 10. Breach escalation matrix

Generic escalation classes:

| Evidence/breach | Default action |
| --- | --- |
| build/test evidence stale or not bound to exact artifact | do not promote |
| candidate restore fails for supported artifact | freeze rollout; preserve artifact; diagnose |
| migration loses/duplicates authoritative semantics | reject candidate; no exposure expansion |
| canary shows recovery-objective breach | trip breaker/pause expansion |
| worker/page mixed-generation incompatibility | stop forced activation; preserve old resources/compatibility |
| API/protocol rejects supported long-offline client | restore compatibility bridge or quarantine replay while preserving local data |
| trust/security compromise | contain authority/bridge; accelerate trusted repair only with data-preservation checks |
| already-migrated state unreadable by rollback build | do not blind rollback; deploy compatible reader/forward repair |
| telemetry absent for offline cohort | mark evidence unknown, not healthy |

Exact automation and thresholds are implementation/product decisions.

---

## 11. C validation campaign

Future implementation evidence should cover at least:
1. N→N+1 schema migration then origin code rollback;
2. N+1 write creates state N cannot represent;
3. failure halfway through migration;
4. local migration succeeds, remote acknowledgement lost;
5. new worker waiting while old page edits authoritative state;
6. forced `skipWaiting` while old page lazy-loads old resource;
7. cache cleanup deletes resource still needed by controlled old page;
8. correcting worker after bad worker already controls clients;
9. long-offline N-k client reconnects after API retirement;
10. old backup restored under new reader after rollout;
11. new backup attempted under rollback build;
12. key/trust generation advances before release rollback;
13. canary cohort green while managed/offline cohort unobserved;
14. breaker pauses expansion while already-exposed clients continue recovery;
15. feature flag disabled after irreversible state write;
16. accessibility of update-required/sync-paused/recovery-required states;
17. exact artifact/build/worker/schema identity attached to evidence;
18. privacy review of rollout/recovery telemetry;
19. malicious/buggy release recovery without deleting authoritative local records;
20. regression mutant that makes rollback path silently discard a new-generation field and must be killed by semantic oracle.

---

## 12. B truthful update/recovery states

User-facing state must distinguish:
- update available;
- update downloaded/waiting;
- restart/reload required;
- update required before sync/online action;
- records saved locally;
- sync paused for compatibility/security;
- recovery/repair in progress;
- current version unsupported but records retained/export/recovery path available, when true.

Do not say “rolled back successfully” merely because old UI code is serving. Success depends on durable state readability and recovery objectives.

Exact copy/interaction remains Design Studio/Content owned.

---

## 13. D measurement and release evidence

Rollout telemetry should prefer non-sensitive release/support-envelope identifiers and outcome classes. It must not export records, backup filenames, keys/tokens or sensitive domain content.

Useful bounded dimensions include build/worker/schema/protocol generation, coarse platform/support class, migration outcome, restore-compatibility outcome and recovery-state class. Stable user/device identifiers require separate necessity/privacy review.

**Guard:** `release telemetry convenient ≠ recovery metadata collection justified`.

---

## 14. MINTTAP / LogMate bounded direction

For a LogMate-like device-authoritative EFB, a release that changes schema, key/recovery, worker/cache, sync protocol or API compatibility should be treated as recovery-critical until exact evidence proves otherwise. Local authoritative flight records/outbox should survive rollout freeze, code rollback decision and trust revalidation.

For MintTap, this run did not inspect the production application's actual data authority, schema, service worker, deployment or backup architecture. Do not transfer EFB assumptions to MintTap production.

No numeric canary percentage, rollout interval, support horizon, recovery budget or mandatory-update deadline is selected here.

---

## 15. CHANGE WATCH

Re-evaluate when materially relevant:
- Service Worker lifecycle/update behavior or browser support changes;
- iOS/iPadOS Home Screen lifecycle/managed-device policy changes;
- schema/key/trust/API compatibility policy changes;
- backup/restore support envelope changes;
- release tooling/provenance model changes;
- CISA/NIST deployment guidance materially changes;
- exact product data-authority or long-offline requirements change.

---

## 16. Gate result

**PASS (generic).** Web Manager can now connect recovery objectives to release/change governance; distinguish artifact publication, worker activation, fleet convergence and durable-state migration; define evidence-gated rollout/breaker semantics; and explain why code rollback must not imply blind rollback of user data/schema/key/trust/remote effects.

**OPEN:** exact MintTap/LogMate release topology; product thresholds; canary cohorts; mandatory-update policy; service-worker activation strategy; migration tooling; compatibility horizon; target managed-iPad runtime; production restore/migration/rollback drills; security review; accessible user-state validation.

**Next high-value boundary:** release compatibility contracts and retirement proof — define how long old readers/writers/API/protocol/key generations remain supported, what evidence permits contract/field/API removal, and how a long-offline authoritative client is retired without converting “unsupported” into silent data loss. This should consume 091/105 and Software Engineering compatibility/migration evidence rather than duplicate API-versioning primers.