# 104 — PWA Offline-First Recovery Objectives, Exposure Budgets & Long-Offline Operations

Status: **PASS (generic) / PRODUCT THRESHOLDS + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 074 durability/sync boundaries; 091 long-offline compatibility; 098 stale-client revocation; 100 reset/rebootstrap; 101 mixed-epoch recovery; 103 backup assurance; Track A browser/storage mechanics; Track B truthful recovery states; Track C failure validation; Track D privacy-safe operational measurement; Software Engineering D003/D005/D006/Q003/Q005/F006.

## Purpose

103 established what evidence is needed to say that a backup is fresh, complete and recoverable. This study asks the next operational question: how should an offline-first, device-authoritative PWA define recovery objectives and tolerable failure exposure without blindly copying server-centric RPO/RTO or ordinary availability error budgets?

This is a generic requirements model. It does **not** choose MintTap/LogMate thresholds, promise automatic backup, or certify a managed-iPad runtime.

---

## 1. Track allocation and bottleneck

- **A Platform/Browser — dependency supplier.** Storage, lifecycle, connectivity and background constraints bound what can be measured/automated.
- **B UX/IA/Content — consumer.** Converts evidence into truthful states such as locally safe, externally unprotected, sync backlog, recovery compatibility unknown and recovery action required.
- **C Performance/Accessibility/Quality — major validation consumer.** Tests objective measurement under interruption, long-offline, wrong clocks, partial recovery and degraded UX.
- **D Search/Discovery/Analytics — bounded measurement consumer.** Recovery-health signals are operational reliability evidence, not acquisition analytics; sensitive content stays excluded.
- **E Architecture/Security/Operations — primary owner.** Owns objective semantics, risk budgets, alert/action policy and recovery governance.

**Allocation:** E remains the highest-risk owner. C receives substantial transfer. A foundations are dependencies. Do not duplicate Software Engineering's implementation/concurrency work.

---

## 2. SOURCE — traditional RPO/RTO are business-impact objectives

NIST SP 800-34 Rev. 1 defines:
- **RPO** as the point in time to which data must be recovered after an outage;
- **RTO** as the maximum recovery-phase duration before mission/business impact becomes unacceptable.

Sources:
- https://csrc.nist.gov/glossary/term/recovery_point_objective
- https://csrc.nist.gov/glossary/term/recovery_time_objective
- https://doi.org/10.6028/NIST.SP.800-34r1

NIST's contingency guidance ties RPO/RTO to business-impact analysis rather than technology convenience. NIST SP 800-55 Vol. 1 (2024) further emphasizes selecting, testing and validating measures and considering data quality/uncertainty.

Source: https://csrc.nist.gov/pubs/sp/800/55/v1/final

**SYNTHESIS:** RPO/RTO remain useful concepts, but a device-authoritative offline PWA has several independent exposure frontiers that one server-style timestamp cannot represent.

**Guards:**
- `RPO defined ≠ every authoritative local change externally protected`;
- `RTO met ≠ restored state trustworthy/current/reconciled`;
- `service reachable ≠ user's authoritative offline data recoverable`.

---

## 3. Why server-centric RPO is insufficient for an offline-first PWA

In a server-primary system, a recovery point is often expressed as elapsed time behind a durable server-side backup. In an offline-first PWA, the newest authoritative state may exist only on one device for an intentionally long period.

The relevant exposure is therefore not merely `now - backupTimestamp`. It includes at least:
1. committed local state not represented by the latest evidenced recoverable artifact;
2. pending logical operations not durably represented elsewhere;
3. attachments/dependencies not included in the recovery set;
4. trust/key/schema/protocol state required to interpret/reconcile the recovered records;
5. externally protected state whose current reader/key path has not recently passed a restore drill.

**SYNTHESIS:** define recovery-point-like exposure against a logical authoritative frontier first; time is an optional risk dimension, not the identity of the frontier.

**Guards:**
- `backup age ≠ data-loss exposure`;
- `record count delta ≠ semantic recovery exposure`;
- `sync backlog ≠ backup backlog`;
- `zero sync backlog ≠ zero local recovery exposure`.

---

## 4. Recovery objective vector

A future product should evaluate a vector rather than one green recovery score.

### 4.1 Local durable-save objective
Question: after the UI reports a record saved, what committed local frontier can survive ordinary app/navigation interruption under the product contract?

This is not an external backup claim.

### 4.2 External-protection objective
Question: how far has the latest authoritative local frontier advanced beyond the newest **evidenced recoverable external** frontier?

Possible indicators can include logical generations/operations and, secondarily, elapsed exposure time. Exact representation is implementation-owned.

### 4.3 Restore-readiness objective
Question: how old is the latest restore-drill evidence that still applies to the current build/format/key/platform support envelope?

### 4.4 Recovery-duration objective
Question: once legitimate recovery begins, how long until required local functions and records are restored to a validated usable state?

Do not stop timing merely because a file decrypted or the shell opened. If the product promise includes reconciliation before safe sync, that phase needs its own objective.

### 4.5 Sync-convergence objective
Question: once connectivity and current trust return, what backlog remains and how long/what work is required before local/remote state reaches the product's defined reconciled condition?

This is distinct from local recovery.

### 4.6 Long-offline survivability objective
Question: for how long can the product remain offline while still preserving required local tasks and retaining a **supported path** to eventual trust/protocol/schema reconciliation?

Do not express this as a promise until release/API/key-retention policies and target-device behavior support it.

### 4.7 Trust-revalidation objective
Question: after reconnect/reset/recovery, how quickly can the client establish current authorization/trust before remote replay or sensitive bridges resume?

**Guard:** `one recovery objective ≠ local durability + external protection + restore readiness + sync convergence + trust revalidation`.

---

## 5. Failure budgets are multi-dimensional, not permission to lose records

Google SRE defines an error budget for a service objective as the allowable miss rate (`1 - SLO`) and uses it to govern reliability/change trade-offs.

Sources:
- https://sre.google/sre-book/introduction/
- https://sre.google/workbook/error-budget-policy/

**TRANSFER VALIDATION:** the governance principle is useful: reliability targets should be explicit, user/product-driven, measured, and connected to action when exceeded.

**CONTRADICTION / LIMIT:** an ordinary request-availability error budget is not a safe template for irreplaceable user records. A product must not interpret a percentage budget as permission to permanently lose some users' authoritative data.

For offline-first recovery, use **exposure/failure budgets** as bounded operational tolerances around objectives, for example:
- proportion of active authoritative frontiers whose external-protection evidence is beyond the product threshold;
- restore drills outside their support/recency envelope;
- supported artifacts failing restore validation;
- reconnect episodes that cannot establish current trust/reconciliation within the defined operational envelope;
- releases that invalidate recovery compatibility without a tested migration/recovery path.

Exact denominators, windows and thresholds are product/risk decisions and remain OPEN.

**Guards:**
- `error budget concept useful ≠ data-loss percentage acceptable`;
- `budget not exhausted ≠ individual user's irreplaceable data safe`;
- `aggregate reliability green ≠ tail recovery failure acceptable`.

---

## 6. Objective breach classes and actions

A metric is useful only if breach semantics lead to a bounded action. Candidate generic classes:

- **Local durability breach:** stop making stronger save/durability claims; preserve evidence; prioritize data-path repair.
- **External-protection lag breach:** surface truthful protection state; trigger/offer supported backup path where feasible; do not imply server sync fixes it.
- **Restore-readiness breach:** block claims such as "restore tested" for the invalidated envelope; schedule fixture/target restore validation.
- **Compatibility horizon breach:** do not force destructive upgrade/replay; preserve records/outbox and require migration/recovery path.
- **Trust-revalidation breach:** keep remote replay/bridge capability paused while retaining local authoritative data.
- **Sync-convergence breach:** preserve stable logical identities and ambiguity evidence; do not convert timeout/transport failure into blind duplicate replay.

**SYNTHESIS:** failure budgets should govern engineering/operational response, not silently redefine user data as expendable.

---

## 7. Long-offline operation changes the denominator

A company EFB may be intentionally disconnected. Therefore `device offline` is not automatically an availability failure.

Measure the user's promised capability:
- Can required local records be created/read/edited?
- Is the local committed frontier intact?
- Is external-protection exposure truthfully represented?
- Can the client later revalidate current trust/protocol/schema without destructive reset?

If the product explicitly promises an online-only function, lack of connectivity can make that function unavailable without implying the local logbook is failed.

**Guards:**
- `offline ≠ app unavailable`;
- `online ≠ sync authorized`;
- `local task available ≠ externally protected`;
- `long offline supported ≠ indefinite stale-client compatibility guaranteed`.

---

## 8. Time, clocks and logical frontiers

Elapsed time remains useful for business-risk windows, restore duration and operational alerting. It should not be the sole proof of capture order or authoritative freshness.

Device clocks can be wrong; offline devices may not have a trusted current time; analytics arrival time can lag or reorder events. Therefore:
- use logical/committed frontiers for ordering and inclusion where correctness depends on it;
- use elapsed/wall time as a separate exposure dimension with explicit clock uncertainty;
- do not infer capture inclusion from `backupTimestamp > editTimestamp` alone.

**Guard:** `wall-clock newer ≠ logically includes all earlier-looking authoritative changes`.

---

## 9. Tail risk and cohort segmentation

Averages can hide the exact users most at risk: long-offline EFBs, managed devices with Files/iCloud restrictions, old supported builds, users with large attachment sets, or clients that missed several release generations.

NIST SP 800-55 Vol. 1 emphasizes measure quality, analysis and uncertainty; Google SRE similarly notes that heterogeneous workloads can require separate objectives.

**SYNTHESIS:** recovery evidence should be segmented by risk-relevant support envelope, not user identity or sensitive content.

Potential bounded cohorts:
- platform/browser/OS support class;
- managed vs unmanaged device where product policy distinguishes them;
- backup format/schema generation;
- recovery-key path class;
- offline-duration bucket;
- artifact size/attachment complexity bucket where operationally relevant.

Privacy review is mandatory before production collection.

**Guard:** `healthy average ≠ vulnerable cohort healthy`.

---

## 10. B truthful-state handoff

Do not collapse recovery objectives into a single reassuring badge. Truth conditions can distinguish:
- **Saved on this device** — local commit evidence only;
- **External protection current** — latest required authoritative frontier is covered under the product-defined evidence contract;
- **External protection behind** — newer authoritative local state exists;
- **Recovery path tested** — applicable restore drill remains inside its support envelope;
- **Recovery path needs verification** — relevant build/format/key/platform change invalidated prior evidence;
- **Sync pending** — remote convergence incomplete, without implying local data loss;
- **Sync authorization required** — local data remains but remote replay is not currently authorized.

Exact copy/interaction remains Design Studio/Content owned.

---

## 11. C validation bundle

Future implementation evidence should cover at least:
1. one authoritative edit after latest external backup;
2. many edits while intentionally offline;
3. zero sync backlog but stale external backup;
4. current external backup but large sync backlog;
5. old restore drill invalidated by schema/key change;
6. restore succeeds locally but trust revalidation blocks sync;
7. reconnect with lost acknowledgement and ambiguous remote apply state;
8. wrong device clock while logical freshness remains correct;
9. long-offline supported client crossing several releases;
10. managed-device external-destination restriction;
11. accessibility of protection-lag/recovery-required states;
12. telemetry loss/reordering without false correctness claims;
13. aggregate metric green while one risk cohort fails;
14. recovery objective breach during release rollout;
15. restoration timing separated from reconciliation timing;
16. local task continuity during server outage;
17. server healthy while device-only authoritative data remains unprotected externally;
18. backup/restore process interruption at each assurance boundary;
19. stale policy/credential requiring revalidation before replay;
20. evidence that no records/keys/tokens/filenames are exported into reliability telemetry.

Consume Software Engineering Q003/D006/F006 for ordering/ambiguity methodology; these are not themselves PWA runtime proof.

---

## 12. D measurement/privacy boundary

Recovery-health telemetry is operational assurance. It should answer bounded questions without replicating user data.

Prefer state classes, support-envelope identifiers, coarse lag/offline buckets and outcome classes. Avoid raw records, filenames, paths, keys/tokens, memo text, exact travel/investment content and unnecessary stable cross-device identifiers.

Client-side reports are useful but can be delayed, absent, replayed or stale. Absence of a breach event is not evidence of health for an offline device.

**Guards:**
- `no telemetry received ≠ objective met`;
- `client reported healthy ≠ external custody independently verified`;
- `measurement convenience ≠ permission to collect sensitive recovery metadata`.

---

## 13. MINTTAP / LogMate bounded direction

For a LogMate-like EFB, future recovery objectives should be expressed around the user's latest committed authoritative local flight records and the product's actual external-protection/recovery contract, not server uptime alone. Intentional offline operation must not itself count as failure if required local tasks remain within contract.

For MintTap, no authoritative production data/recovery model was inspected in this run. Do not transfer EFB thresholds or data-authority assumptions to MintTap merely because both are company products.

Do **not** set numeric RPO/RTO/SLO/error-budget values until product impact, data authority, target-device constraints, supported offline duration, backup destination and restore evidence are known.

---

## 14. CHANGE WATCH

Re-evaluate when materially relevant:
- authoritative local/server data ownership changes;
- backup destination/background/file APIs or managed-iPad policy change;
- supported offline/client compatibility window changes;
- schema/protocol/key/trust rotation policy changes;
- restore-drill support envelope changes;
- telemetry/privacy/legal policy changes;
- target-browser storage/lifecycle behavior changes.

---

## 15. Gate result

**PASS (generic).** Web Manager can now distinguish traditional RPO/RTO from device-authoritative offline exposure; define a multi-dimensional recovery-objective vector; adapt error-budget governance without treating user data loss as spendable; separate local continuity, external protection, restore readiness, sync convergence and trust revalidation; and define privacy-bounded measurement/validation requirements.

**OPEN:** every numeric threshold; exact authoritative frontier representation; product-specific data-loss tolerance; backup automation/destination; target managed-iPad runtime; actual restore/reconnect timings; exact telemetry implementation; production SLO/budget policy.

**Next high-value boundary:** recovery-objective breach escalation and release/change governance — specifically how schema/key/service-worker/API releases should consume or freeze recovery-risk budget, how compatibility/restore evidence gates rollout, and how to roll back code without rolling back user data/trust state. This should consume release/supply-chain evidence from 089/092 and Software Engineering rather than create a generic CI/CD primer.