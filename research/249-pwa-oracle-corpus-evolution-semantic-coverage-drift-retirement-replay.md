# 249 — PWA Oracle-Corpus Evolution, Semantic-Coverage Drift & Retirement/Replay Resistance

Status: **PASS (generic) / PRODUCT + CORPUS-GENERATION + SPEC/POLICY + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A versioned platform/parser semantics; Track B stale-evidence/recovery UX; Track C coverage/regression validation; Track D denominator-aware coverage measurement.  
Dependencies: 137, 171–214, 223–248, especially verifier migration, historical evidence continuity, verifier reconstruction, oracle provenance and common-mode failure.

## Problem
248 established that a golden corpus is provenance-bearing evidence rather than truth by label. The adjacent failure is **time**. A corpus can be authentic, correctly derived and useful for generation G12 yet become incomplete, misleading or actively unsafe after a specification, canonicalization rule, parser, trust policy, schema, threat model or product operation changes. Conversely, retiring a vector from current conformance does not erase its historical evidentiary value.

Central rule: **bind every oracle claim to the semantic generation it tests; measure coverage over explicit semantic partitions rather than case count; append/supersede instead of silently rewriting; distinguish historical applicability from current admissibility; and require current bootstrap plus operation-level re-admission when long-offline PWA evidence crosses corpus generations.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns exact browser/runtime/parser/canonicalization generations and identifies platform behavior changes that alter vector applicability.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `CORPUS-STALE`, `EXPECTATION-RETIRED`, `SEMANTIC-GAP`, `HISTORICAL-ONLY`, `REVALIDATION-REQUIRED` and `BOOTSTRAP-REQUIRED` states without destructive reset.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns semantic partition coverage and destructive regression. Campaign expands **744 → 752 defined cases**; defined cases are not execution PASS.
- **D Search/Discovery/Analytics:** bounded consumer. May measure coverage by semantic partition/generation with explicit denominators; raw vector count and pass percentage cannot establish assurance.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns corpus lifecycle, promotion/retirement, replay resistance, policy/spec binding and current-authority isolation.

## SOURCE

### W3C CSS test-suite lifecycle
W3C's CSS test-suite page distinguishes Final, Release Candidate, Beta, Alpha, Pre-Alpha and **Obsolete** suites. It also preserves dated versions while a `current` URL points to the latest dated suite. This is a useful standards-testing precedent for separating historical test artifacts from current recommended conformance evidence.

Source: https://www.w3.org/Style/CSS/Test/  
Freshness checked: 2026-09-23; page updated 2025-10-02.

**TRANSFER VALIDATION:** bounded lifecycle/versioning precedent only. CSS test-suite governance is not adopted as MintTap's corpus protocol.

### W3C Test Metadata
The W3C Test Metadata Note treats tests as units associated with metadata such as status, context and specification relationship. The note is old (2005), so it is used only for the durable principle that test artifacts need contextual metadata rather than being context-free files.

Source: https://www.w3.org/TR/test-metadata/

**CHANGE WATCH:** historical W3C QA guidance, not a current normative Web standard.

### web-platform-tests expectation metadata
Current WPT runner documentation records expected outcomes at test/subtest granularity and permits expectations to depend on run information such as OS/version/processor. This is useful evidence that expected outcomes are contextual, not timeless properties of a filename.

Source: https://web-platform-tests.org/tools/wptrunner/docs/expectation.html  
Freshness checked: 2026-09-23.

**TRANSFER VALIDATION:** bounded test-harness precedent; browser expectation metadata does not define MintTap security semantics.

### NIST — input-space and combinatorial coverage
NIST's coverage work explicitly distinguishes the number of tests from how much relevant input/configuration space is covered. `Input Space Coverage Matters` warns that even full structural coverage can miss rare untested inputs. NISTIR 7878 defines combinatorial coverage measures for arbitrary test sets, and 2025 work extends coverage reasoning to event sequences.

Sources:
- https://www.nist.gov/publications/input-space-coverage-matters
- https://www.nist.gov/publications/combinatorial-coverage-measurement
- https://www.nist.gov/publications/ensuring-reliability-through-combinatorial-sequence-coverage

**TRANSFER VALIDATION:** bounded coverage-measurement precedent. MintTap does not infer that t-way coverage alone proves security, PWA correctness or semantic conformance.

### Current cross-repository evidence boundary
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**; exact-fixture macOS Safari Service Worker registration→control→V1→V2 update/controller replacement→fresh-WebDriver V2 control recovery is bounded PASS, while origin-down fresh cold-start, installed PWA and physical iOS/iPadOS/EFB remain OPEN.

Sources: `yhappcom/design-studio/progress/WEB_STATUS.md`; `yhappcom/software-engineering-studio/progress/STATUS.md` (checked 2026-09-23).

**DEPENDENCY:** generic corpus-lifecycle reasoning does not upgrade those runtime/human/device gates.

## SYNTHESIS 1 — corpus applicability is generation-bound
A vector needs more than identity and expected result. Bind it, where relevant, to specification/policy generation, schema, canonicalization/parser/verifier generation, operation class and threat/assurance purpose. The same bytes can be a valid historical oracle under G12 and an obsolete current oracle under G19.

Guards: `vector authentic ≠ vector currently applicable`; `historically correct expectation ≠ current-policy expectation`; `same input bytes ≠ same semantic generation`.

## SYNTHESIS 2 — evolution has several independent axes
Do not use one `corpus_version` to hide distinct changes. Track at least:
1. normative/specification semantics;
2. schema/data-model semantics;
3. canonicalization/serialization semantics;
4. parser/verifier implementation generation;
5. trust/admission/security policy;
6. operation/consequence class;
7. platform/runtime behavior where relevant;
8. corpus/vector generation and provenance.

A parser upgrade can require regression without changing policy; a policy change can invalidate an old expected admission outcome while parsing remains identical.

Guard: `implementation generation change ≠ semantic rule change`; `semantic rule change ≠ bytes necessarily change`.

## SYNTHESIS 3 — append/supersede; do not rewrite historical expectations
If a G12 vector expected `ACCEPT` but G19 policy correctly expects `REJECT`, preserve the G12 assertion and add the G19 assertion with its rationale and supersession/applicability relation. Replacing the old expected field destroys the ability to reproduce historical behavior and can launder past results.

Guards: `expectation changed ≠ old expectation was always wrong`; `current correction ≠ historical rewrite`.

## SYNTHESIS 4 — retirement has scope and reason
Retirement is not deletion. Record why a vector is retired: specification feature removed, policy superseded, duplicate/redundant, oracle disputed, generator compromised, platform no longer supported, privacy/legal retention expiry, or replacement by stronger evidence. Distinguish `RETIRED-CURRENT` from `INVALID-HISTORICAL`.

Guards: `retired from current suite ≠ historically invalid`; `historically retained ≠ eligible for current admission`.

## SYNTHESIS 5 — prevent retired-vector replay
A test runner or recovery tool must not accept an obsolete corpus merely because its digest/signature is valid. Bind execution/closure to an allowed corpus generation or policy floor. If a job requests a retired generation for historical reconstruction, label the result `HISTORICAL-ONLY` and isolate it from current release/admission gates.

Guards: `corpus signature valid ≠ corpus generation current`; `old suite passes ≠ current gate passes`; `historical verifier mode ≠ current admission mode`.

## SYNTHESIS 6 — coverage is a map over claims, not a case counter
`752 tests` says nothing about whether critical semantic partitions are covered. Maintain a claim/partition matrix appropriate to the format and threat model: valid/invalid/malformed, boundary lengths, duplicate/order behavior, generation/predecessor substitution, canonicalization variants, signature mutation, stale/current policy, migration boundaries, offline/rejoin transitions and consequence-bearing operation classes.

Use explicit denominators where the partition is enumerable. Where it is not, state the model and blind spots rather than inventing a percentage.

Guards: `more cases ≠ more semantic coverage`; `100% tests passing ≠ 100% semantics covered`; `coverage percentage without denominator/model ≠ assurance`.

## SYNTHESIS 7 — coverage can drift while test count increases
Adding many cases to already dense partitions can raise corpus size while newly introduced semantic partitions remain empty. A new schema field, policy state or sequence transition changes the coverage model denominator. Therefore compare coverage across generations only after normalizing to the relevant semantic model.

Guard: `case-count growth ≠ coverage growth`; `same percentage under changed model ≠ same assurance`.

## SYNTHESIS 8 — sequence coverage matters for PWA lifecycle claims
PWA correctness often depends on transitions, not isolated states: worker V1 controls → V2 installs → activation/controllerchange → restart; offline queue → policy generation changes → reconnect → migration → re-admission. NIST's sequence-coverage work is a useful precedent that event combinations can expose failures missed by state-only coverage.

**MINTTAP DIRECTION:** Track C should model consequence-bearing lifecycle sequences explicitly; do not infer sequence assurance from individual-state vectors.

Guard: `each state tested ≠ transition sequence tested`.

## SYNTHESIS 9 — corpus promotion requires delta analysis
Before making generation G20 current, identify added/removed/retired vectors, changed expected claims, new semantic partitions, unresolved disagreements, provenance changes and whether previously closed claims depend on altered expectations. A green G20 run without this delta can hide a weakened suite.

Guard: `new corpus green ≠ new corpus at least as strong`; `fewer failures ≠ improved correctness`.

## SYNTHESIS 10 — negative-space inventory is part of coverage
Record known untested/unknown partitions, not just covered ones. This is especially important when platform capability differs across Chromium, Safari/WebKit, installed PWA, ordinary tab and managed iPad. Unknown physical-device behavior cannot be represented as a passing generic vector.

Guard: `not failing in corpus ≠ covered`; `unsupported test environment ≠ product PASS`.

## SYNTHESIS 11 — platform change watch can trigger corpus revalidation
When WebKit/Chromium/OS behavior materially changes a relied-on PWA capability, first determine whether the semantic requirement changed, the implementation behavior changed, or only the environment changed. Revalidate affected partitions and do not silently mutate expected results merely to match the newest browser.

Guard: `browser changed ≠ expected security semantics should change`; `new observed behavior ≠ new normative truth`.

## SYNTHESIS 12 — long-offline PWA evidence crosses generations as evidence, not authority
For a company iPad leaving at G12 and returning at G19, preserve the G12 corpus/verifier context needed to interpret historical evidence. Do not execute G12 as the current admission oracle. Establish current bootstrap, map historical claims to current semantics, identify retired/changed expectations, migrate data/schema separately, then re-admit queued operations under G19 policy.

Guards: `G12 corpus retained ≠ G12 authority retained`; `historical PASS ≠ queued operation currently admissible`.

## SYNTHESIS 13 — corpus pruning must preserve evidentiary continuity
Performance pressure may justify removing redundant executable vectors from the hot CI set, but retain enough metadata/provenance/supersession lineage to explain what was tested historically and why coverage is still claimed. A smaller smoke suite and a larger authoritative corpus may coexist if their scopes are explicit.

Guard: `removed from hot CI ≠ erased from evidence lineage`; `fast suite PASS ≠ full corpus PASS`.

## SYNTHESIS 14 — analytics cannot turn coverage into truth
Track D may report partition coverage, stale-vector incidence, disagreement rates, retirement reasons and unknown tails. These are governance/quality indicators. They cannot determine semantic truth, choose between disputed oracles, or promote a corpus generation by threshold alone.

Guard: `coverage KPI met ≠ semantic gate passed`.

## MINTTAP DECISION / DIRECTION
Generic policy only; product implementation remains OPEN.

1. Version corpus applicability across spec/policy/schema/canonicalization/verifier/runtime dimensions where material.
2. Preserve old expected claims and append/supersede; never silently rewrite historical semantics.
3. Separate current conformance/admission suites from historical reconstruction suites.
4. Bind current gates to an allowed corpus/policy floor and reject silent retired-generation replay.
5. Measure claim/partition/sequence coverage with explicit denominators/models; never use raw test count as assurance.
6. Require corpus-generation delta analysis before promotion.
7. Preserve known gaps and unsupported environments as OPEN, especially physical iPadOS/WebKit/EFB.
8. Long-offline PWA rejoin uses historical corpus only to interpret evidence; current bootstrap and operation-level re-admission remain mandatory.

## Track C destructive oracle additions — 744 → 752 defined cases
These are **defined tests, not executed PASS**.

1. **Authentic-retired replay** — signed G12 corpus is supplied to a G19 release gate. Expected: reject as current oracle; historical mode only.
2. **Silent expectation rewrite** — G12 `ACCEPT` is overwritten by G19 `REJECT`. Expected: preserve both generation-bound assertions and supersession.
3. **Case-count laundering** — thousands of duplicate/easy vectors are added while a new critical semantic partition remains empty. Expected: no coverage uplift for missing partition.
4. **Denominator drift** — coverage remains reported as 95% after new policy states expand the model. Expected: recompute against G19 model; preserve old metric context.
5. **State-only lifecycle claim** — install, activate, offline and reconnect states pass individually but transition ordering is untested. Expected: sequence assurance remains OPEN.
6. **Green-by-retirement** — failing high-value vector is retired without justified scope/replacement and suite turns green. Expected: gate remains blocked/review required.
7. **Browser-observation rewrite** — new Safari behavior causes expected security result to be changed without normative/policy analysis. Expected: contradiction/change-watch, not silent oracle mutation.
8. **Offline-iPad corpus downgrade** — returning G12 iPad causes current Service Worker/sync path to load G12 corpus for admission. Expected: preserve historical evidence; current bootstrap/migration/re-admission required.

Campaign total: **752 defined cases**. Execution, physical-device, AT and human validation remain OPEN.

## VALIDATION ladder
Generic reasoning PASS requires:
- authoritative/bounded evidence for test-suite lifecycle/context and coverage principles;
- explicit generation/applicability model;
- retirement/replay controls;
- semantic partition and sequence-coverage model;
- long-offline PWA transfer analysis;
- destructive cases defined.

Product/runtime PASS additionally requires actual:
- corpus inventory/generations and promotion history;
- spec/policy/schema/canonicalization/verifier mappings;
- executed partition/sequence coverage with semantic artifacts;
- replay/retirement negative tests;
- browser/device matrices including physical iPadOS/WebKit where in scope;
- actual LogMate/MintTap data, sync, auth and release-gate evidence.

## OPEN
- Actual MintTap/LogMate corpus generations, oracle inventory, schema/policy/verifier generations and CI gate behavior are unknown.
- Physical iPadOS/WebKit/MDM PWA lifecycle/storage/sync behavior remains unverified.
- No claim is made that NIST combinatorial coverage alone is sufficient for semantic/security conformance.
- No production corpus retention period or legal/aviation obligation is inferred.

## CHANGE WATCH
- Web-platform-tests/browser expectation behavior and browser/OS PWA behavior.
- Any normative specification/policy used by actual product verifiers.
- NIST/W3C testing guidance where current operational recommendations evolve.

## Gate
**PASS (generic).** The Web Manager can distinguish corpus authenticity from current applicability; model semantic and sequence coverage rather than case count; preserve historical expectations while preventing retired-generation replay; govern corpus promotion/retirement; and apply the model to long-offline PWA rejoin without restoring stale authority. Product/device/runtime validation remains OPEN.

## Next highest-value adjacent question
**250 — corpus-promotion authority, semantic-change approval & coverage-regression governance:** determine who may declare a corpus generation current; how normative/spec/policy changes are authorized without allowing test maintainers to redefine product security semantics; how coverage regressions and justified retirement exceptions are approved; how emergency corpus hotfixes accrue/retire assurance debt; and how long-offline clients distinguish current corpus authority from merely newer test artifacts.