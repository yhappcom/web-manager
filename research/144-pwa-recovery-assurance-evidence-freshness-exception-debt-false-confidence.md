# 144 — PWA Recovery-Assurance Evidence Freshness, Exception Debt & False-Confidence Control

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + EVIDENCE-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A browser/PWA state; Track B assurance/recovery UX; Track C validation evidence; Track D bounded telemetry; studies 117–143, especially 120–125 and 141–143.

## Why this study exists

143 created a recovery-authority inventory and survivability-drill loop. That loop can still create false confidence when a once-valid drill, attestation, inventory reconciliation or temporary exception remains green after the facts it depended on have changed.

The problem is therefore not merely collecting more evidence. It is preserving an honest relationship between **claim, evidence, scope, freshness, dependencies, exceptions and current decision authority**.

## SOURCE

### Risk information is continuously monitored and adjusted
NIST Cybersecurity Framework 2.0 is outcome-oriented rather than prescriptive and applies across organization sizes. Its Govern/Identify/Improve model treats cybersecurity risk as something understood, assessed, prioritized, communicated and improved rather than certified once forever.

Source: https://doi.org/10.6028/NIST.CSWP.29

NIST SP 1303, the CSF 2.0 Enterprise Risk Management Quick-Start Guide, explicitly frames cybersecurity risk management as monitoring, evaluation and adjustment across organizational units and programs.

Source: https://doi.org/10.6028/NIST.SP.1303

NIST SP 800-53A Rev.5 defines procedures for assessing security/privacy controls. The current CSRC publication notes Release 5.2.0 (2025-08-27), reinforcing that assessment procedures themselves evolve. Assessment evidence therefore has context and method provenance; a historical PASS cannot be detached from the procedure, system state and scope under which it was obtained.

Source: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

NIST ongoing-authorization guidance links continuous monitoring/ongoing assessment to maintaining sufficiently current risk information rather than relying solely on point-in-time authorization.

Source: https://doi.org/10.6028/NIST.CSWP.06032014

### Exceptions must not fail open
OWASP Top 10:2025 A10 covers mishandling exceptional conditions, including fail-open behavior and authorization/state errors under abnormal conditions. It supports the bounded principle used here: missing, expired or contradictory assurance evidence must not silently become an implicit PASS.

Source: https://top10.owasp.org/2025/A10_2025-Mishandling_of_Exceptional_Conditions/

## SYNTHESIS — evidence has a validity envelope

A PASS is not a timeless property of a system. Treat each material assurance item as a claim with a **validity envelope**:

- claim/control/recovery capability being asserted;
- evidence type and provenance;
- subject/system/device/provider scope;
- policy/schema/key/verifier/application generation where material;
- observed/tested environment;
- evidence collection time;
- dependencies assumed during the test;
- method/scenario version;
- unresolved exceptions or compensating controls;
- invalidation triggers;
- revalidation owner/path.

Persistent guards:
- `evidence exists ≠ evidence current`;
- `evidence current ≠ evidence covers this scope`;
- `recent timestamp ≠ strong evidence`;
- `old evidence ≠ automatically false`;
- `old evidence ≠ current assurance`;
- `control unchanged ≠ dependencies unchanged`;
- `dashboard green ≠ uncertainty absent`;
- `exception approved ≠ exception harmless`;
- `temporary exception ≠ permanent architecture`;
- `compensating control documented ≠ compensating control effective`;
- `revalidation scheduled ≠ revalidation completed`.

## Evidence freshness is semantic, not just chronological

Do not define freshness only as `now - testedAt < N days`. Evidence can become stale immediately after a material change and can remain useful longer when its dependencies are stable and the claim is inherently durable.

Use two mechanisms together:

1. **Event invalidation** — personnel/owner change, provider/IdP change, key/trust transition, policy/schema/API change, Service Worker/deployment generation change, custody loss, incident, failed recovery, device/MDM change, browser/platform change relevant to the claim, or architecture migration can invalidate or narrow prior evidence immediately.
2. **Periodic revalidation backstop** — catches silent drift where no explicit change event was recorded.

No universal MintTap expiry interval is asserted. Actual cadence is consequence-, volatility- and evidence-type-dependent and remains OPEN.

### Evidence states

Use explicit states instead of green/red only:

- **CURRENT-VERIFIED** — evidence is within its validity envelope and no known invalidator applies;
- **CURRENT-WITH-EXCEPTION** — evidence remains applicable but an explicitly bounded accepted exception exists;
- **REVALIDATION-DUE** — time/change threshold reached; claim must not silently remain fully green;
- **INVALIDATED-BY-CHANGE** — a known dependency/scope change breaks applicability;
- **CONTRADICTED** — newer evidence conflicts with the prior claim;
- **PARTIAL/BOUNDED** — evidence proves only a subset (e.g. staging, Chromium, online path);
- **UNKNOWN** — evidence insufficient or provenance unavailable;
- **SUPERSEDED** — retained historically but replaced by newer evidence.

`UNKNOWN ≠ PASS` and `REVALIDATION-DUE ≠ FAIL` are both important. The first prevents fail-open; the second prevents false precision.

## Exception debt

An exception is a deliberate departure from the desired control/assurance state. It becomes **exception debt** when temporary risk acceptance persists, multiplies, loses an accountable owner, outlives its rationale, or interacts with other exceptions/dependencies in ways the original approval did not cover.

Minimum exception record, without storing secrets:
- stable exception ID;
- exact control/guard being waived or narrowed;
- bounded scope and consequence;
- rationale and evidence available at acceptance;
- accountable risk owner/approver;
- compensating control if any;
- start and review/expiry condition;
- invalidation/escalation triggers;
- dependency on other exceptions;
- retirement criterion;
- current status/provenance.

### Exception rules

- An expired exception does not convert automatically into approval renewal.
- A missing owner does not mean the exception remains accepted.
- Renewal is a new risk decision using current evidence, not a timestamp extension.
- A compensating control must itself have current evidence.
- Multiple individually tolerable exceptions can create an intolerable combined path; aggregation must examine shared consequences/dependencies.
- Emergency/break-glass exceptions require post-event normalization and explicit retirement.

Persistent guards:
- `exception expired ≠ control fixed`;
- `exception expired ≠ exception still authorized`;
- `exception renewed ≠ original evidence still sufficient`;
- `two accepted exceptions ≠ combined risk accepted`;
- `waiver closed in tracker ≠ runtime deviation removed`;
- `compensating control PASS ≠ original control restored`.

## MINTTAP DECISION — assurance aggregation without false confidence

Do not compute a single opaque “security/recovery score.” A numeric average can allow strong low-consequence evidence to hide one unknown high-consequence recovery path.

Use a compact claim matrix instead:

`Claim | consequence | evidence state | scope | last verified | invalidators | exception state | owner | next action`

Aggregate only to an **honest status vocabulary** such as:
- **ASSURED FOR STATED SCOPE**;
- **ASSURED WITH BOUNDED EXCEPTION**;
- **DEGRADED / REVALIDATION REQUIRED**;
- **BLOCKED BY UNKNOWN OR CONTRADICTION**;
- **NOT ASSESSED FOR THIS ENVIRONMENT**.

High-consequence unknown/contradicted claims must remain visible and must not be averaged away. A product can be operational while recovery assurance is degraded; UI/operations should represent those as different dimensions.

## Cross-track transfers

### Track A — Platform & Browser
A Service Worker update, browser upgrade, site-data clear, PWA reinstall or storage-policy change may invalidate evidence whose scope depended on previous lifecycle/storage behavior. `same URL works ≠ previous PWA recovery evidence still applies`. Physical Safari/iPad claims remain device evidence, not inferred from generic Web standards.

### Track B — UX / IA
Own explicit states such as `RECOVERY ASSURANCE DEGRADED`, `REVALIDATION REQUIRED`, `LOCAL DATA PRESERVED / REMOTE WRITE BLOCKED`, and `EXCEPTION EXPIRES/REVIEW REQUIRED`. Do not expose a generic reassuring green state when material evidence is UNKNOWN or bounded to another environment.

### Track C — Quality
Own evidence provenance, scenario version, environment, repetition and contradiction handling. A newer failing test supersedes neither the historical fact that the old test passed nor the need to diagnose the changed condition. Preserve both and classify the current claim as contradicted/degraded.

### Track D — Analytics
Telemetry can trigger revalidation when failure/use patterns change, but telemetry freshness is not control assurance. Missing events may be instrumentation failure. Do not let analytics become the authority for exceptions, risk acceptance or recovery authorization.

### Track E — Owner
Own validity-envelope semantics, invalidation triggers, exception governance, assurance aggregation, retirement and normalization.

## PWA / EFB application

For a long-offline company iPad:
- a months-old successful reconnect drill does not prove current WebKit/MDM/provider behavior;
- a current server recovery drill does not prove stale Service Worker/cache/IndexedDB behavior on that iPad;
- browser/site-data loss can erase local evidence without authorizing trust rollback;
- an offline device may cross multiple policy/key/succession epochs, invalidating prior “one-epoch reconnect” evidence;
- local irreplaceable records remain preservable while remote mutation stays gated when current assurance is insufficient.

No assumption is made about unattended sync, storage persistence, MDM retention, file/share APIs or direct phone↔iPad transport. Those remain product/platform validation items.

## VALIDATION — 30-case campaign

1. old drill remains green after IdP change; 2. old drill remains green after key rotation; 3. old Safari evidence reused for new iPadOS/WebKit generation without review; 4. Chromium PASS displayed as managed-iPad PASS; 5. staging PASS displayed as production PASS; 6. evidence timestamp recent but scenario omitted the critical failure; 7. evidence old but no known invalidator—classified due, not false; 8. provider change event missing from assurance system; 9. dependency change invalidates two claims transitively; 10. new failure contradicts prior PASS; 11. contradictory evidence hidden by latest-only dashboard; 12. exception expires while runtime deviation remains; 13. exception auto-renews without current risk decision; 14. exception owner departs; 15. compensating control expires before exception; 16. two exceptions combine into trust-floor downgrade path; 17. emergency exception remains active after normalization; 18. waiver tracker closed but provider credential remains enabled; 19. exception rationale references unavailable evidence; 20. revalidation task scheduled but never executed; 21. dashboard averages one critical UNKNOWN with many green low-risk controls; 22. telemetry silent because instrumentation broke; 23. local PWA storage cleared and assurance state disappears; 24. stale Service Worker presents superseded assurance state; 25. long-offline iPad reconnects after multiple invalidating epochs; 26. browser update changes relevant storage/lifecycle behavior; 27. drill method changes and results are incorrectly compared as identical; 28. imported backup restores stale assurance/exception state; 29. current server evidence coexists with unvalidated physical-device path; 30. end-to-end change → invalidation → degraded state → bounded exception if justified → revalidation → exception retirement → normalization.

## OPEN

Actual MintTap/LogMate evidence store, provider topology, identity/admin model, exception workflow, risk owner, alerting, Service Worker/storage implementation, managed-iPad/MDM fleet, browser versions, telemetry, recovery scenario set, consequence classification and acceptable review cadence are unknown. No production PASS is claimed.

## CHANGE WATCH

- Browser/WebKit/Chromium/MDM behavior that underlies a validation claim is change-sensitive.
- NIST/OWASP assessment/security guidance evolves; record source/version rather than treating a citation as timeless.
- Provider audit, credential and recovery APIs require provider-specific validation after selection.

## Gate result

**PASS (generic).** The Web Manager can now distinguish evidence age from semantic freshness, invalidate assurance on dependency change, model temporary exceptions as debt with retirement obligations, preserve contradiction/uncertainty, and aggregate recovery assurance without hiding critical unknowns behind a single score.

Production, managed-EFB and runtime assurance remain **OPEN**.

## Next highest-value adjacent question

**PWA recovery-assurance dependency propagation, evidence graph consistency & transitive invalidation.** The next bottleneck is how one changed root dependency (IdP, key, provider, browser generation, custody path) should invalidate only the claims that actually depended on it—neither leaving stale green claims nor triggering blanket revalidation of everything—and how to detect cycles, orphan evidence and contradictory graph state without building heavyweight GRC infrastructure.