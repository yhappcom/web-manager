# 236 — PWA Contradiction Intake Authenticity, Adversarial False-Reopen Resistance & Evidence-Poisoning Containment

Status: **PASS (generic) / PRODUCT + INTAKE + TRIAGE + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A client/runtime evidence; Track B containment/revalidation UX; Track C destructive validation; Track D intake observability.  
Dependencies: 223–235 dependency/currentness, proof lineage, recovery/destruction and closure/contradiction handling.

## Problem
235 established that later contradiction is appended rather than rewriting history, and that affected claims are reopened by dependency blast radius. The next attack surface is the contradiction intake itself. A contradiction may arrive from an unauthenticated user, stale PWA client, provider alert, support channel, monitoring system, audit export, incident responder or attacker. Treating every report as authority lets an attacker force perpetual containment; dismissing untrusted reports lets genuine residual authority, stale verifiers or restore paths remain hidden. A compromised intake/triage plane can also suppress, rewrite, duplicate or fabricate evidence.

Central rule: **contradiction intake accepts potentially valuable untrusted evidence without granting the reporter authority. Preserve the submitted artifact and provenance separately from the claim it alleges; score consequence and corroboration rather than reporter prestige alone; use bounded reversible containment when plausible consequence crosses a defined threshold; rate-limit work and duplicate amplification without discarding unique high-consequence evidence; and require independent/current authority paths for adjudication and re-closure.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser/Service Worker/storage observations can be authentic client-local facts while remaining insufficient to establish server authority or fleet-wide state.
- **B UX/IA/Content:** high dependency pressure. Owns understandable RECEIVED / UNVERIFIED / CORROBORATING / CONTAINED / DISMISSED-AS-DUPLICATE / REOPENED states without implying accusation or certainty.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight intake-poisoning/false-reopen/suppression destructive cases; campaign expands **640 → 648 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures intake volume, duplicate rate, corroboration latency, containment duration, suppression/recovery signals and queue health; metrics cannot adjudicate truth.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns provenance capture, triage trust boundaries, consequence-based containment, false-report DoS resistance, suppression detection and independent adjudication.

## SOURCE

### NIST SP 800-61 Rev.3 — incident response is an integrated risk-management capability
NIST finalized SP 800-61 Rev.3 in April 2025, superseding Rev.2. It integrates incident response into CSF 2.0 and emphasizes preparation, detection, response and recovery as organization-wide risk-management activities rather than a single alert-processing step.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://doi.org/10.6028/NIST.SP.800-61r3

**TRANSFER VALIDATION:** contradiction intake is narrower than general incident response, but the durable principle transfers: detection input is not itself final adjudication; response needs prepared roles, prioritization, analysis, containment and recovery.

### NIST SP 800-53 / audit-information protection — evidence channels require integrity protection
NIST control families distinguish monitoring/detection from protection of audit information. This supports keeping telemetry/reporting, evidence preservation and authority enforcement as separate planes rather than letting an intake database become the source of current authorization.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** `report stored ≠ report true`; `audit protected ≠ underlying event legitimate`; `monitoring alert ≠ authority decision`.

### CISA reporting model — receive, triage and analyze reports rather than assuming every submission is verified
CISA's cyber-event reporting guidance explicitly describes receiving reports and then triaging/analyzing them, with follow-up for additional information where needed. This is a bounded operational precedent for separating intake from adjudication.

Source:
- https://www.cisa.gov/sites/default/files/publications/Sharing_Cyber_Event_Information_Fact_Sheet_FINAL_v4.pdf

## SYNTHESIS 1 — reporter authenticity, artifact authenticity and allegation truth are different claims
For every intake preserve separately:
1. **reporter identity/provenance** — known account, anonymous channel, provider principal, device identity, support case, etc.;
2. **artifact integrity/authenticity** — exact bytes, signature/hash, capture method, device/provider object identifiers, timestamp source and chain of custody where available;
3. **semantic allegation** — what closure/currentness claim the reporter says the artifact contradicts;
4. **current consequence reachability** — whether the alleged condition can plausibly reach a current verifier, threshold, restore/rejoin path or consequence boundary.

An anonymous report may contain authentic high-value evidence. A strongly authenticated employee may be mistaken. `reporter authenticated ≠ allegation true`; `reporter anonymous ≠ evidence worthless`; `artifact authentic ≠ interpretation correct`.

## SYNTHESIS 2 — intake creates a candidate contradiction, not an automatic reopen authority
Receipt should create a versioned candidate evidence object in a non-authoritative intake plane. It may trigger triage and bounded containment, but cannot directly mutate admission floors, recovery roots or closure truth solely because an intake row says `critical`.

State model: `RECEIVED → PRESERVED → UNVERIFIED/CORROBORATING → {DUPLICATE, NON-MATERIAL, CONTRADICTION-CONFIRMED, INCONCLUSIVE}` with independent consequence state `{NORMAL, PRECAUTIONARY-CONTAINMENT, REOPENED/CONTAINED, REVALIDATING}`.

`report received ≠ contradiction confirmed`; `contradiction plausible ≠ attacker proven`; `intake severity field ≠ authority decision`.

## SYNTHESIS 3 — consequence can justify containment before provenance is complete
False-report resistance must not become an excuse to ignore high-consequence evidence. If an artifact plausibly demonstrates that a retired recovery share can satisfy a current threshold, a stale verifier accepts a predecessor, or a restore path can rejoin with obsolete authority, use the least destructive reversible containment that blocks that consequence while preserving evidence and unique data.

Containment threshold should combine consequence magnitude, reachability, evidence specificity, corroboration and reversibility. Reporter reputation is only one input.

`unverified ≠ harmless`; `containment ≠ final adjudication`; `precautionary fence ≠ declaration of compromise`.

## SYNTHESIS 4 — false-reopen floods are a control-plane DoS threat
An attacker can submit thousands of syntactically distinct reports to consume analysts or repeatedly trigger expensive containment. Defenses include:
- content/provenance-aware deduplication;
- per-source and global rate controls on processing, not blind evidence deletion;
- queue isolation by consequence class;
- bounded automated checks for exact object/generation references;
- cost escalation only as evidence becomes more specific/corroborated;
- preserving a compact immutable receipt for dropped/duplicate submissions where justified;
- emergency capacity controls that do not lower current authority floors.

Never let `number of reports` substitute for independent corroboration. `1000 duplicate allegations ≠ 1000 independent witnesses`; `rate-limited processing ≠ evidence may be silently discarded`.

## SYNTHESIS 5 — deduplication must preserve genuinely new evidence
Two reports can allege the same contradiction while carrying different artifacts, generations or provenance. Deduplicate work at the allegation/signature level while retaining unique evidence edges. Conversely, attackers can mutate irrelevant bytes to defeat naive hash-only deduplication.

Use semantic keys such as affected claim/object/generation/provider event/device lineage plus artifact digest and provenance. `same text ≠ same evidence`; `different hash ≠ independent contradiction`.

## SYNTHESIS 6 — intake/triage compromise requires an independent suppression-detection path
If the intake service can delete a report before any independent trace exists, compromise can hide genuine contradiction. High-consequence channels should produce a minimal external receipt/checkpoint or independent audit event containing non-secret metadata sufficient to prove submission occurrence and detect disappearance, without making that receipt an authority oracle.

Periodically reconcile ingress counts/IDs/checkpoints with triage outcomes and evidence-store objects. A missing report triggers evidence-integrity investigation; it does not prove the allegation itself.

`submission receipt ≠ allegation true`; `no triage record ≠ no report existed`; `independent receipt ≠ second authority root`.

## SYNTHESIS 7 — corroboration should cross failure domains where consequence warrants it
Corroboration is strongest when it crosses the suspected failure domain: provider event plus application negative oracle; stale-client artifact plus current server verifier behavior; backup manifest plus isolated restore test; HSM inventory plus independently governed audit export. Two observations from the same compromised admin plane may add little independence.

`two alerts ≠ two independent observations`; `different dashboard ≠ different failure domain`.

## SYNTHESIS 8 — false-positive history cannot permanently discredit a source
A device/user/source that previously produced false or stale reports may later surface the only real contradiction. Reputation may affect triage cost/priority but must not become a permanent truth veto for specific high-consequence evidence. Exact object/generation evidence can override low source reputation and trigger bounded corroboration.

`prior false positive ≠ future evidence impossible`; `trusted source ≠ future evidence automatically true`.

## SYNTHESIS 9 — long-offline PWA/iPad return is an intake event with data-preservation priority
A LogMate-like iPad returning after months may expose old worker/trust metadata, queued operations, local exports or stale verifier behavior. Treat the device state as preserved candidate contradiction evidence. Do not let the returning device directly reopen server authority, and do not wipe it merely because it is noisy or stale.

Preserve unique flight/logbook data first; isolate consequence-bearing replay; record client lineage, worker/controller/storage state and current bootstrap result where available; then corroborate against current server/admission state. Physical iPad/WebKit behavior remains OPEN until execution evidence exists.

## SYNTHESIS 10 — analytics detects abuse and suppression but does not decide truth
Track D can measure submission volume, unique-artifact ratio, dedup ratio, queue age, corroboration latency, containment time, source diversity, missing-receipt discrepancies and reopened-claim outcomes. These support capacity and drift diagnosis. They cannot auto-dismiss low-frequency reports, auto-confirm high-volume reports or auto-close after quiet periods.

`low frequency ≠ low consequence`; `high volume ≠ truth`; `queue drained ≠ contradiction resolved`.

## SYNTHESIS 11 — triage personnel and automation need bounded privileges
Triage must be able to preserve evidence, request corroboration and invoke pre-authorized reversible containment for defined high-consequence classes, but should not possess unrestricted recovery-root rotation, threshold reduction or destructive data authority merely for convenience. Exceptional escalation follows the existing governed emergency/recovery authority model.

`can contain ≠ can redefine trust`; `analyst admin ≠ recovery authority`.

## SYNTHESIS 12 — adjudication and re-closure remain successor-proof operations
A confirmed contradiction reopens the affected closure/dependencies under 235. A false/non-material report is closed with rationale and retained provenance sufficient for audit/abuse analysis. Re-closure after a real contradiction requires successor evidence and negative oracles; deleting or banning the reporter is irrelevant to technical closure.

`report dismissed ≠ artifact erased`; `reporter malicious ≠ every artifact false`; `reporter banned ≠ contradiction resolved`.

## MINTTAP DECISION / DIRECTION
1. Treat contradiction intake as an untrusted evidence-ingress plane, never as current authority.
2. Separate reporter provenance, artifact authenticity, semantic allegation and current consequence reachability.
3. Preserve exact candidate evidence before transformation where feasible; assign immutable intake identity and provenance links.
4. Use consequence-based, reversible containment before full attribution when plausible current authority impact is high.
5. Resist false-reopen DoS with semantic deduplication, bounded queues/rate controls and staged corroboration; never use report count as witness quorum.
6. Preserve unique evidence even when reports deduplicate operationally.
7. Maintain an independent minimal submission/checkpoint path for high-consequence intake so triage compromise cannot silently erase every trace.
8. Corroborate across failure domains when consequence warrants it.
9. Keep triage privilege bounded; analysts/automation may not redefine trust roots or lower floors as a shortcut.
10. For long-offline PWA/iPad returns, preserve unique user data and stale-tail evidence before bootstrap/re-admission; do not wipe to simplify triage.
11. Metrics support abuse/suppression detection and capacity management only; they never adjudicate truth or authority.
12. Confirmed contradiction and re-closure continue through dependency-scoped successor-proof governance from 235.

## DEPENDENCY / TRANSFER
- **Track A:** supplies exact browser/Service Worker/storage/client-lineage semantics for interpreting stale-client evidence. New bounded Software Engineering Safari service-worker lifecycle evidence is useful transfer evidence but does not establish iOS/iPadOS/EFB behavior.
- **Track B / Design Studio:** consumes explicit RECEIVED, UNVERIFIED, CORROBORATING, PRECAUTIONARY-CONTAINMENT, REOPENED, DISMISSED-AS-DUPLICATE and REVALIDATING states. Design Studio remains Stage 3 PRACTICE / NOT PASSED; human/AT/device validation remains OPEN.
- **Track C:** owns execution of poisoning, flood, suppression, dedup and long-offline destructive cases when implementation exists.
- **Track D:** observes intake health and abuse patterns but cannot vote reports into truth.
- **Software Engineering:** exact intake schema, queue, immutable receipt/checkpoint, semantic dedup, privilege boundaries and test harness are implementation handoffs. Current Studio evidence remains Foundation-stage and bounded.

## Track C destructive additions — 640 → 648 defined cases
1. **Single-report authority promotion:** unauthenticated intake row marked critical directly lowers/changes current admission state → fail authority separation.
2. **False-reopen flood:** thousands of duplicate reports repeatedly trigger global shutdown without corroboration or bounded containment → fail DoS resistance.
3. **Blind rate-limit loss:** rate limiter silently discards the one report carrying a unique current-threshold key artifact → fail evidence preservation.
4. **Hash-only dedup evasion:** irrelevant-byte mutations create unlimited independent cases and analyst work → fail semantic dedup.
5. **Over-dedup evidence loss:** same allegation from two genuinely independent failure domains is collapsed and second artifact/provenance discarded → fail corroboration preservation.
6. **Compromised triage suppression:** intake service deletes a genuine high-consequence report and no independent receipt/checkpoint reveals the disappearance → fail suppression detection.
7. **Reputation truth veto:** historically noisy device returns with exact current-generation contradiction but is auto-dismissed solely from reputation → fail consequence-led triage.
8. **Long-offline iPad destructive triage:** returning iPad is wiped to stop noisy contradiction reports before unique flight/logbook data and stale-tail evidence are preserved → fail data-preserving intake.

These are **defined cases, not execution PASS**.

## VALIDATION
Generic PASS requires the Web Manager to distinguish report provenance from artifact authenticity and allegation truth; accept untrusted reports without promoting them to authority; contain plausible high-consequence conditions without declaring attribution; resist false-reopen floods without deleting unique evidence; detect intake suppression through an independent bounded trace; preserve cross-failure-domain corroboration; and apply the model to long-offline PWA/iPad evidence without claiming unexecuted product behavior.

Production validation remains OPEN for actual MintTap/LogMate intake channels, provider alert APIs, support workflows, queue/retention topology, triage IAM, audit/checkpoint independence, dependency graph, current authority/floor integration, physical iPad/WebKit behavior and human operational performance.

## CHANGE WATCH
- NIST SP 800-61 Rev.3 is current final as of 2026-09-23; it superseded Rev.2 on 2025-04-03.
- Provider incident/audit/reporting APIs and retention semantics remain provider-specific CHANGE WATCH.
- Browser/iOS/iPadOS PWA capability and managed-device behavior remain CHANGE WATCH and require physical/runtime validation for product claims.

## Gate result
**PASS (generic).** Track E remains the highest-risk owner. The next adjacent high-value question is **237 — corroboration-graph independence, contradiction quorum & coordinated evidence-fabrication resistance**: prevent multiple reports, dashboards or provider views controlled by one failure domain from masquerading as independent corroboration; define when one high-specificity artifact can outweigh many weak observations; and preserve availability without turning contradiction handling into simplistic majority voting.