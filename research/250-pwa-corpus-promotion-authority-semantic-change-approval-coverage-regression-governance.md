# 250 — PWA Corpus-Promotion Authority, Semantic-Change Approval & Coverage-Regression Governance

Status: **PASS (generic) / PRODUCT + GOVERNANCE + CORPUS + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A platform/runtime generation evidence; Track B recovery/status UX; Track C regression/coverage validation; Track D governance metrics with explicit denominators.  
Dependencies: 137, 171–249, especially authority/currentness, exception/emergency lifecycle, oracle provenance, corpus evolution, retirement/replay resistance and semantic coverage drift.

## Problem
249 established that an oracle corpus is generation-bound and that a newer or larger corpus is not automatically stronger. The adjacent governance risk is **who may make a corpus current, what exactly that approval means, and how semantic or coverage weakening is prevented from being laundered as ordinary test maintenance**.

A test maintainer can legitimately repair a fixture without having authority to redefine security semantics. A security/policy owner can approve a semantic rule without having authority to fabricate evidence that the implementation satisfies it. A release operator can deploy an approved corpus without being entitled to promote an unreviewed corpus. Emergency test changes can be necessary, but an emergency path that silently becomes the normal semantic-authority path defeats the governance model.

Central rule: **separate corpus authorship, semantic authority, evidence review, promotion and release enforcement; bind promotion to an explicit semantic/coverage delta and current approval policy; treat justified coverage reduction as visible assurance debt rather than a green-suite optimization; and never let a newer artifact, emergency patch or long-offline client choose the current corpus by freshness alone.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Provides browser/runtime/parser/canonicalization generation changes and distinguishes implementation observation from normative/product semantics.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `CORPUS-PENDING`, `REVALIDATION-REQUIRED`, `COVERAGE-DEGRADED`, `EMERGENCY-CORPUS`, `HISTORICAL-ONLY` and `BOOTSTRAP-REQUIRED` states without destructive reset or false reassurance.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns semantic delta review, coverage-regression evidence and destructive validation. Campaign expands **752 → 760 defined cases**; defined cases are not execution PASS.
- **D Search/Discovery/Analytics:** bounded consumer. May report promotion latency, coverage deltas, exception age and unresolved partitions, but metrics cannot elect semantic truth or approve a generation.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns promotion authority, role separation, currentness, emergency governance, release enforcement and assurance-debt closure.

## SOURCE

### NIST SP 800-128 — security-focused configuration change control
NIST SP 800-128 describes configuration change control as a documented process covering proposal, justification, implementation, test/evaluation, review and disposition. It explicitly includes emergency/unscheduled changes and says responsibilities and authorities for each step should be articulated. It also states that security-impact analysis should preferably occur before approval/implementation, and should also be performed for emergency changes and after implementation to identify unanticipated effects.

Source: https://doi.org/10.6028/NIST.SP.800-128  
Freshness checked: 2026-09-23; NIST page updated 2025-02-19.

**TRANSFER VALIDATION:** bounded governance precedent. A MintTap oracle corpus is not itself a NIST system configuration item, but promotion of a security-relevant corpus has analogous proposal/approval/test/review/change-record requirements.

### NIST SP 800-53 Rev.5 / Release 5.2.0 — configuration change control
Current NIST SP 800-53 Release 5.2.0 retains CM-3 change-control concepts: document proposed changes, notify designated approval authorities, prohibit changes until required approvals are received, document completed changes, retain records and monitor/review change-control activity. CM-4 separately addresses security-impact analysis.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

**TRANSFER VALIDATION:** bounded control-governance precedent only; this does not prescribe MintTap staffing or a specific approval threshold.

### web-platform-tests — review and expectation metadata
Current WPT review guidance asks reviewers to verify that a test passes and fails when it should, tests what it claims, and that the specification supports the expected behavior. WPT expectation metadata can also be generated from observed run results and can be conditional on environment properties.

Sources:
- https://web-platform-tests.org/reviewing-tests/checklist.html
- https://web-platform-tests.org/tools/wptrunner/docs/expectation.html

**SYNTHESIS:** observed results can legitimately inform harness metadata, but a mechanism that updates expectations from runs is not authority to redefine product security semantics. For MintTap, observed browser behavior and normative/product expected behavior remain separate evidence classes.

### Current cross-repository evidence boundary
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED** with physical-device/PWA, screen-reader and representative-human UX evidence OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**; bounded exact-fixture macOS Safari Service Worker registration→control→V1→V2 update/controller replacement→fresh-WebDriver V2 control recovery is PASS, while origin-down fresh cold-start, installed PWA, physical iOS/iPadOS/EFB and canonical-product runtime remain OPEN.

Sources: `yhappcom/design-studio/progress/WEB_STATUS.md`; `yhappcom/software-engineering-studio/progress/STATUS.md`, checked 2026-09-23.

**DEPENDENCY:** generic corpus governance does not upgrade runtime, human or physical-device gates.

## SYNTHESIS 1 — distinguish corpus roles and authorities
At minimum distinguish:
1. **author/editor** — proposes vectors, fixtures or metadata;
2. **semantic owner** — owns the normative/product policy claim being tested;
3. **evidence reviewer** — evaluates provenance, rationale, independence and delta;
4. **promotion authority** — designates a corpus generation as eligible for a named gate/scope;
5. **release/gate enforcer** — enforces the approved generation/floor in CI/runtime/recovery paths.

One person or system may hold multiple roles in a small organization, but the roles must remain conceptually distinct so correlated authority is visible.

Guards: `can edit tests ≠ can redefine semantics`; `can approve semantics ≠ can fabricate validation evidence`; `can deploy corpus ≠ can promote corpus`; `repository write ≠ current-oracle authority`.

## SYNTHESIS 2 — promotion is a scoped authorization, not a timestamp
A promotion record should identify the corpus generation, applicable semantic/policy/schema/parser/runtime generations, operation/consequence scope, required predecessor or floor, known gaps, approval basis and effective interval where relevant.

A newer commit, artifact timestamp or successful build is not promotion.

Guards: `newer corpus ≠ current corpus`; `merged ≠ promoted`; `artifact published ≠ gate-authorized`; `latest timestamp ≠ highest authority`.

## SYNTHESIS 3 — classify changes before approval
Not every corpus edit carries the same consequence. Separate at least:
- editorial/non-semantic metadata correction;
- fixture implementation repair with unchanged semantic claim;
- added coverage for an existing claim;
- expected-result change due to clarified/corrected semantics;
- policy/security semantic change;
- retirement/removal reducing executable coverage;
- parser/canonicalization/verifier generation change;
- emergency temporary override.

Classification determines required review. A maintainer must not label an expected-result reversal as an editorial fix to bypass semantic authority.

Guard: `small diff ≠ low semantic impact`; `test-only change ≠ non-production change`.

## SYNTHESIS 4 — expectation changes need independent semantic basis
If `ACCEPT` becomes `REJECT`, or vice versa, promotion requires a rationale grounded in the applicable normative/product policy basis, not merely the current implementation result. WPT's review checklist usefully separates “what the test does” from whether the specification backs the expectation.

**MINTTAP DIRECTION:** preserve old generation-bound expectation, append the new expectation, identify why applicability changed, and require semantic-owner review for consequence-bearing reversals.

Guards: `implementation now passes ≠ expectation should become PASS`; `browser observation changed ≠ security policy changed`.

## SYNTHESIS 5 — promotion requires semantic and coverage delta review
Before G20 becomes current, compare it with the currently authorized generation across:
- added/removed/retired vectors;
- changed expected claims;
- semantic partition denominator/model changes;
- sequence/lifecycle coverage changes;
- provenance/generator/reviewer changes;
- new platform/runtime conditions;
- unresolved disagreements and OPEN partitions;
- historical closures depending on altered expectations.

A green run after deleting the only test for a critical partition is a governance failure, not an improvement.

Guards: `green after delta ≠ safe delta`; `failure count down ≠ assurance up`.

## SYNTHESIS 6 — coverage regression can be accepted only as explicit debt
Some coverage loss may be justified: broken infrastructure, obsolete platform, privacy/legal retention constraints, urgent incident response or a superseded feature. If accepted, record the missing claim/partition, consequence, rationale, compensating control if any, owner, expiry/review trigger and restoration/retirement condition.

Do not silently change the denominator so the percentage stays green.

Guards: `approved regression ≠ no regression`; `temporary waiver ≠ permanent baseline`; `coverage denominator changed ≠ debt disappeared`.

## SYNTHESIS 7 — emergency corpus changes need bounded authority
Emergency hotfixes may need accelerated approval, but must still identify scope, semantic claim, provenance, effective generation, expiry/review trigger and post-event validation. Emergency authority should not automatically gain permission to rewrite historical expectations or become the normal promotion path.

After stabilization, either promote a normally reviewed successor or retire the emergency generation; preserve the emergency interval in history.

Guards: `emergency accepted ≠ normal baseline approved`; `incident ended ≠ emergency corpus retired`; `post-event green ≠ emergency governance debt closed`.

## SYNTHESIS 8 — approval currentness matters
A corpus approved under approval policy P7 is not automatically authorized after governance moves to P9 if the change affects relevant authority, threshold, delegation or failure-domain assumptions. Pending promotion should bind to its approval-policy generation and be re-evaluated when material governance changes occur.

Guard: `approved once ≠ approved under every successor governance generation`.

## SYNTHESIS 9 — separation of duties is failure-domain reasoning, not headcount theater
Two approvals are not independent if both derive from the same compromised account, shared recovery path, same unreviewed fixture generator or same semantic misconception. Conversely, not every low-risk editorial change needs heavyweight dual control.

**MINTTAP DIRECTION:** choose review independence and threshold according to consequence and credible failure modes; do not prescribe a universal `2-of-N` without product governance evidence.

Guards: `two clicks ≠ two independent approvals`; `different usernames ≠ different failure domains`.

## SYNTHESIS 10 — gate enforcement must fail closed on unknown generation
Release/recovery tooling should know which corpus generation or minimum floor is authorized for the gate. If the requested corpus is newer but unpromoted, older and retired, or cannot be mapped to current approval state, the consequence-bearing gate should not silently choose “latest available.”

Useful states include `CORPUS-PENDING`, `CORPUS-STALE`, `CORPUS-UNAUTHORIZED`, `COVERAGE-DEGRADED`, `EMERGENCY-CORPUS`, `HISTORICAL-ONLY`, `REVALIDATION-REQUIRED`.

Guard: `unknown currentness ≠ choose newest`.

## SYNTHESIS 11 — automation may enforce promotion policy but must not invent semantic authority
Automation can verify signatures/digests, generation floors, required approvals, delta manifests, expiry and coverage thresholds. It cannot determine that a disputed semantic expectation is correct merely because all automated checks agree.

Guard: `policy engine says approvals present ≠ semantic claim correct`.

## SYNTHESIS 12 — long-offline PWA must distinguish artifact freshness from authority
A company iPad may return carrying G12 corpus evidence while the server exposes a newly built G20 corpus artifact. Neither fact alone establishes current authority. The client/recovery path must obtain current governance/bootstrap evidence identifying the authorized corpus/policy generation, preserve G12 historical evidence, migrate data separately and re-admit queued operations under the current authorized semantic gate.

Guards: `newer downloaded corpus ≠ authorized corpus`; `cached signed corpus ≠ current corpus`; `historical PASS ≠ current operation admitted`.

## SYNTHESIS 13 — PWA update mechanics do not solve corpus governance
A Service Worker can fetch/cache a newer app shell or test artifact, but browser update mechanics do not establish product semantic authority. `skipWaiting()`, controller replacement or successful cache population cannot be treated as corpus promotion.

Track A owns lifecycle mechanics; Track E owns promotion/currentness; Track C validates the resulting sequences.

Guard: `Service Worker activated ≠ semantic corpus promoted`.

## SYNTHESIS 14 — analytics observes governance; it does not govern
Track D may report time-to-promotion, percentage of partitions covered, waiver age, emergency-generation duration, stale-client tails and promotion failures. These indicators can trigger review. Thresholds alone cannot approve semantic changes, choose between disputed expectations or close assurance debt.

Guard: `governance KPI green ≠ semantic gate passed`.

## MINTTAP DECISION / DIRECTION
Generic policy only; actual staffing, thresholds and product implementation remain OPEN.

1. Treat oracle-corpus promotion as an explicit, scoped authorization distinct from authoring, merge, build and deployment.
2. Classify corpus changes by semantic consequence before choosing review depth.
3. Require independent semantic rationale for consequence-bearing expectation changes; preserve historical assertions.
4. Require promotion delta review covering semantic partitions, sequence coverage, provenance and known gaps.
5. Make accepted coverage regression explicit assurance debt with owner, scope and closure condition; never hide it by denominator manipulation.
6. Bound emergency corpus authority by scope/time and require post-event review plus normal successor/retirement.
7. Bind promotion approvals to governance generation/currentness; stale approvals do not silently survive material authority changes.
8. Fail closed for consequence-bearing gates when corpus authorization/currentness is unknown; do not auto-select newest.
9. Keep Service Worker/update mechanics separate from semantic corpus authority.
10. Long-offline PWA rejoin preserves historical evidence but obtains current bootstrap and operation-level re-admission under the currently authorized corpus/policy generation.

## Track C destructive oracle additions — 752 → 760 defined cases
These are **defined tests, not executed PASS**.

1. **Maintainer semantic escalation** — test editor changes `REJECT` to `ACCEPT` and merges without semantic-owner review. Expected: not promotable for consequence-bearing gate.
2. **Newest-artifact auto-promotion** — gate selects highest timestamp/version despite missing promotion record. Expected: fail closed / `CORPUS-PENDING`.
3. **Green-by-coverage-removal** — sole critical partition test is removed and suite turns green. Expected: coverage regression/debt blocks ordinary promotion unless explicitly accepted.
4. **Denominator laundering** — removed partition is also removed from metric denominator without governance record. Expected: preserve prior model/delta and flag regression.
5. **Stale-approval replay** — G20 was approved under P7, but approval topology materially changes to P9 before publication. Expected: revalidation required.
6. **Emergency permanence** — incident hotfix corpus remains current after emergency expiry because it is passing. Expected: retire or normally promote reviewed successor; debt remains until closure.
7. **Correlated dual approval** — two approvers share the same compromised identity/recovery/fixture failure domain. Expected: independence claim fails where required by consequence model.
8. **Offline-iPad newest-corpus laundering** — returning device downloads a newer unpromoted corpus and uses it to admit queued sync. Expected: current governance/bootstrap determines authorized corpus; preserve evidence and re-admit operations.

Campaign total: **760 defined cases**. Execution, physical-device, AT and human validation remain OPEN.

## VALIDATION ladder
Generic reasoning PASS requires:
- authoritative/bounded change-control and test-review precedents;
- explicit role/authority separation;
- scoped promotion/currentness model;
- semantic/coverage delta and regression-debt model;
- emergency lifecycle and stale-approval handling;
- long-offline PWA transfer analysis;
- destructive cases defined.

Product/runtime PASS additionally requires actual:
- corpus repository/registry and promotion mechanism;
- semantic/policy owners and approval topology;
- executed delta manifests and coverage models;
- enforced corpus generation/floor at release/recovery/admission gates;
- emergency/waiver lifecycle evidence;
- actual LogMate/MintTap Service Worker, sync, auth, schema and data-model evidence;
- physical iPadOS/WebKit/MDM validation where in scope.

## OPEN
- Actual MintTap/LogMate corpus promotion authority, semantic-owner map, CI/release gate and exception process are unknown.
- No universal approval count or separation-of-duties threshold is prescribed without product consequence/failure-domain evidence.
- Physical iPadOS/WebKit/MDM PWA lifecycle/storage/sync behavior remains unverified.
- Production legal/aviation/safety obligations and retention requirements remain unknown.

## CHANGE WATCH
- NIST SP 800-53/800-128 updates affecting configuration/change-control precedents.
- WPT review/expectation tooling and browser/OS PWA behavior.
- Actual product policy/spec/schema/verifier generations once canonical evidence exists.

## Gate
**250 generic PASS.** This closes the generic promotion-authority / semantic-change / coverage-regression governance block. It does not certify a production corpus, CI gate, PWA, managed iPad or product runtime.

## Next highest-value adjacent work
**251 — corpus-promotion record integrity, approval-artifact anti-replay & gate-policy split-brain resistance:** determine how promotion records themselves are authenticated/versioned/revoked; how CI, recovery service and long-offline PWA avoid accepting different “current” corpus generations; how approval artifacts are prevented from replay across scope/generation; and how a promotion-control-plane compromise is contained without rewriting historical corpus evidence.