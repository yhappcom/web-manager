# 288 — PWA Recovery Validation Matrix and Evidence Contract

Status: **PASS (generic) / IMPLEMENTATION + PHYSICAL-IPAD + MANAGED-IPAD + AT + HUMAN + PRODUCT VALIDATION OPEN**  
Date: 2026-09-26  
Primary owner: **Track C — Web Performance, Accessibility & Quality**  
Security dependency: **Track E — Web Architecture, Security & Operations**  
Dependencies: 285–287.

## Purpose

287 established recovery, evidence-retention and normalization requirements. This checkpoint converts those requirements into a repeatable validation model. The goal is not a healthy final screen alone. A valid recovery experiment must preserve enough evidence to reconstruct the initial state, controlled disruption, transition, material outcome, recovery, retirement checks and normalization.

Central guard: **healthy final state does not prove a safe transition.**

## SOURCE

### NIST SP 800-115

NIST SP 800-115 describes technical security assessment as planning and conducting tests/examinations, analyzing findings and developing mitigation, while accounting for the benefits and limitations of assessment techniques.

Sources:
- https://csrc.nist.gov/pubs/sp/800/115/final
- https://www.nist.gov/publications/guide-information-security-testing-and-assessment

Transfer: recovery validation should define scope, assumptions, expected results and evidence before execution. NIST does not define this PWA-specific matrix.

### W3C Service Workers

The W3C publication history records a Service Workers Candidate Recommendation Draft dated 2026-09-17 after multiple 2026 drafts.

Sources:
- https://www.w3.org/TR/service-workers/
- https://www.w3.org/standards/history/service-workers/

**CHANGE WATCH:** lifecycle/update details and browser implementations remain active platform evidence.

### WebKit inspection evidence

WebKit documents remote inspection of Safari pages and Home Screen websites on connected iOS devices. Safari 26 adds automatic inspection and pausing for newly running Service Workers associated with an app or Home Screen Web App.

Sources:
- https://webkit.org/web-inspector/enabling-web-inspector/
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

Transfer: these capabilities improve physical-device observability; they do not prove background execution, storage durability, update timing or recovery correctness.

## Five-track allocation

- **A Platform/Browser:** supplies Service Worker/controller/cache/storage and platform-lifecycle observables.
- **B UX/IA/Content:** consumes truthful local-saved, offline, queued, revalidation, conflict and remotely-confirmed state requirements.
- **C Quality:** primary owner; defines repeatable scenarios, evidence tiers and verdict rules.
- **D Analytics:** consumes privacy-aware correlation and convergence observations without treating telemetry silence as proof.
- **E Security/Operations:** supplies authority/currentness and normalization invariants.

## Validation model

Each scenario declares before execution:
1. precondition and relevant generation state;
2. expected allowed local capabilities;
3. expected prohibited material outcomes;
4. authoritative decision boundary;
5. expected user-visible state;
6. required positive and negative evidence;
7. data-integrity evidence;
8. cleanup/normalization condition.

Guards:
- `no crash ≠ PASS`;
- `observed outcome ≠ predeclared expected outcome`;
- `healthy final screen ≠ safe transition proven`.

## Multidimensional PWA state

A single `appVersion` is insufficient. Capture as applicable:
- Service Worker registration/scope/script identity;
- installing/waiting/active and actual controller generation;
- Cache Storage generation;
- application-data schema generation;
- verifier/bootstrap/policy generation;
- session/admission generation;
- local queue/provenance generation;
- backend acceptance/policy generation.

Not every scenario requires every field, but omission is deliberate and documented.

Guards:
- `worker current ≠ controller current`;
- `worker current ≠ cache current`;
- `worker current ≠ schema/verifier/session current`;
- `single version label ≠ reconstructable recovery state`.

## Verdict model

Use three values:

- **PASS:** all mandatory positive/negative evidence exists, invariants hold and normalization completes.
- **FAIL:** a declared invariant is violated, a prohibited material outcome occurs, required unique data is lost, obsolete authority succeeds, or the user-visible state is materially false.
- **UNKNOWN:** mandatory evidence is missing or ambiguous, observation fails, or instrumentation materially changes the condition under study.

Guards:
- `no observed failure ≠ PASS`;
- `missing evidence ≠ success`;
- `instrumented success ≠ uninstrumented equivalence proven`.

## Evidence bundle

Record as applicable:
- scenario and harness version;
- validation tier, device, OS/browser/WebKit version;
- sanitized precondition state vector;
- declared expected results/invariants;
- controlled-disruption start/stop and provenance;
- transition ordering;
- privacy-safe correlation identifiers;
- relevant page/worker/browser/backend observations;
- local-data/queue integrity summary;
- user-visible recovery state;
- successor-positive and predecessor-negative evidence;
- cleanup/normalization result;
- ambiguity/UNKNOWN reason.

Evidence collection follows data minimization and must not unnecessarily retain sensitive user records or authentication material.

Guard: `more telemetry ≠ stronger evidence`.

## Validation tiers

- **T0:** model/static review.
- **T1:** deterministic desktop/browser automation.
- **T2:** Safari/WebKit desktop and/or simulator evidence where applicable.
- **T3:** physical target iPad/iPadOS Home Screen PWA.
- **T4:** actual managed/company iPad configuration when relevant.
- **T5:** representative-human plus assistive-technology validation.

Lower-tier success does not certify a higher tier.

Guards:
- `desktop PASS ≠ Safari/iPad PASS`;
- `simulator PASS ≠ physical-iPad PASS`;
- `physical-iPad PASS ≠ managed-fleet PASS`;
- `technical PASS ≠ human/AT PASS`.

## Minimum scenario matrix H01–H10

**H01 — old controller / new deployment.** Keep a known old controller while a successor exists. Observe controller/currentness separately and verify that material outcomes obey current authoritative rules.

**H02 — new worker / stale cache.** Compose a known successor runtime with a predecessor cache set. Verify that unsafe combinations are migrated, rejected or contained according to the declared compatibility rule.

**H03 — generation skew.** Exercise known runtime/schema/verifier/session generation mismatch. Parse compatibility must not silently restore obsolete authority.

**H04 — long-offline rejoin with unique local data.** Rejoin a dormant client holding unique records, provenance and queued intent. Preserve unique data before destructive repair, establish current admission and re-adjudicate queued material effects.

**H05 — predecessor retirement.** After successor establishment, validate representative material boundaries so obsolete recovery/currentness material cannot create predecessor effects.

**H06 — queued work across policy transition.** Delay an operation across a policy change. Queue admission is not assumed to be permanent authorization; execution uses current adjudication or an explicitly governed bounded snapshot rule.

**H07 — interrupted migration/restart.** Interrupt a known migration at selected boundaries. Verify no silent partial-success state, unique-data loss, duplicate material effect or weaker rollback authority.

**H08 — migration horizon exceeded.** Use a client older than the supported migration horizon while preserving unique data. Unsupported authority is not admitted merely to recover the data; preservation/reconciliation and re-provisioning remain distinct concerns.

**H09 — contradictory recovery/currentness evidence.** Present conflicting valid-looking claims. Do not elect authority by highest epoch, newest timestamp or traffic majority; contain material consequence until legitimate authority is established.

**H10 — observation failure.** Remove one mandatory evidence channel. If the missing evidence is necessary to adjudicate the case, the expected verdict is UNKNOWN rather than PASS.

## Determinism boundary

Repeatability applies to fixture identity, initial state, controlled disruption and expected invariants. Browser scheduling, Service Worker timing and OS lifecycle may remain nondeterministic. Use observable conditions and bounded waits rather than pretending platform scheduling is guaranteed.

Guard: `repeatable setup ≠ deterministic browser scheduler`.

## Physical-iPad boundary

T1/T2 provide inexpensive coverage but cannot establish target-iPad behavior. T3 is required before target-iPad lifecycle/update/storage/rejoin claims. WebKit inspection improves evidence capture, but debugging or pausing can itself perturb timing and that limitation must be recorded.

Guard: `debugger-observed behavior ≠ debugger-free timing equivalence`.

## Software Engineering handoff

Web Manager owns scenario semantics, web/PWA invariants, required browser/platform observations, verdict semantics and validation tiers.

Software Engineering owns implementation choices for fixtures, test interfaces, browser/device runners, backend correlation, snapshot/restore tooling, CI/device-lab orchestration and safe logging.

No product implementation is inferred here.

## MINTTAP DECISION / DIRECTION

1. Use PASS/FAIL/UNKNOWN for recovery evidence.
2. Declare expected invariants before controlled disruption.
3. Model PWA state as multiple generations rather than one app version.
4. Maintain H01–H10 as the minimum generic recovery matrix.
5. Require T3 evidence before target-iPad behavioral claims; keep T4/T5 separate.
6. Preserve unique offline data before destructive trust/runtime repair.
7. Require positive successor and negative predecessor evidence for retirement.
8. Keep evidence privacy-minimized.
9. Hand implementation mechanics to Software Engineering.
10. Keep actual MintTap/LogMate architecture and runtime facts OPEN until verified.

## Track C destructive additions — defined, not executed

1057. **Single-version blindness:** one app version hides controller/cache/schema/verifier/session skew.  
1058. **Expectation-after-observation:** expected result is invented only after the run.  
1059. **Final-state theater:** healthy final UI masks an unsafe intermediate outcome or data loss.  
1060. **Foreground-only retirement:** one foreground boundary rejects obsolete authority while another material path remains capable.  
1061. **Evidence overcollection:** validation records unnecessary sensitive authentication/user material.  
1062. **Destructive-repair data loss:** stale client is reset before unique local data/provenance is preserved.  
1063. **Tier-promotion error:** desktop/simulator evidence is reported as physical/managed-iPad evidence.  
1064. **Missing-evidence PASS:** mandatory observation is absent but the case is recorded as successful instead of UNKNOWN.

Execution, physical-device, managed-device, AT and representative-human PASS are not claimed.

## OPEN

Actual MintTap/LogMate worker/cache/schema/verifier/session generations; auth/provider topology; material acceptance boundaries; queue/sync semantics; migration horizon; unique-record schema; MDM/ADE/company-iPad configuration; browser/device matrix; background behavior; storage durability; test environment; fixtures; validation interfaces; evidence implementation; legal/aviation/safety requirements; and human/AT behavior remain OPEN.

## VALIDATION

Generic gate passes because the recovery model is now falsifiable and repeatable: it has predeclared expectations, multidimensional PWA state, explicit evidence requirements, three-valued verdicts, non-transitive validation tiers, a minimum scenario matrix and a bounded engineering handoff.

Production validation remains OPEN until implemented and executed against real target browser/backend/device/managed-device/human conditions.

## Next high-value target

**289 — deterministic offline/rejoin fixture identities, validation-control protocol and Software Engineering handoff package.** Define minimum fixture identities, generation probes, correlation contract, cleanup/reset invariants and physical-iPad runbook needed to implement H01–H10 without allowing test-only mechanisms to become production authority.
