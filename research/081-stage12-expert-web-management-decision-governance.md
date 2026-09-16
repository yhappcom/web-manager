# 081 — Stage 12: Expert Web Management Decision Governance

Status: **PASS — Stage 12 integrated block 1**  
Date: 2026-09-16

## Purpose
Stage 12 changes the unit of competence from knowing a web discipline to governing ambiguous multi-disciplinary decisions. The Web Manager must preserve evidence boundaries, expose uncertainty, allocate decision rights, and keep decisions reversible where uncertainty is high.

## Integrated model
`decision trigger → decision owner → affected user/business tasks → constraints/non-negotiables → alternatives → evidence + confidence → uncertainty/unknowns → risk/impact → reversibility → cross-specialist conflicts → decision → validation/guardrails → review trigger → retirement/supersession`

## 1. Decision records are not meeting minutes
An Architecture/Decision Record should preserve the decision problem, context, considered alternatives, evidence, assumptions, trade-offs, owner, date, validation conditions, and supersession trigger. A decision can be rational when made and later become wrong because evidence, platform behavior, cost, product scope, or regulation changed. Therefore records must preserve *why*, not only *what*.

### Decision Record Contract
- ID / status: proposed, accepted, rejected, superseded, retired;
- decision owner and required specialist reviewers;
- user/business task affected;
- constraints and non-negotiables;
- alternatives considered, including “do nothing” where valid;
- evidence references and freshness;
- confidence: high / medium / low with reason, never an unexplained score;
- unknowns and assumptions;
- downside/failure modes;
- reversibility and switching cost;
- chosen option and explicit trade-offs;
- validation/guardrail evidence required;
- review/supersession trigger.

**SYNTHESIS:** ADR quantity is not governance quality. A record without alternatives, uncertainty and review triggers becomes decision archaeology rather than a control system.

## 2. Evidence confidence and uncertainty
Separate:
`fact → bounded observation → inference → forecast → preference → decision`.

Confidence is determined by relevance to the actual population/environment, authority of source, recency where behavior changes, directness, reproducibility and contradictory evidence. “More sources” is not automatically stronger evidence when all repeat the same upstream claim.

### Evidence Confidence Record
For material decisions record:
- claim;
- evidence type: standard/platform documentation, production observation, experiment, user research, analytics, specialist judgment, precedent;
- applicable environment/population;
- freshness/change-watch status;
- limitations/missingness;
- contradictions;
- confidence and what evidence would change it.

**SOURCE:** NIST RMF separates preparation, assessment, authorization and continuous monitoring; its authorization step explicitly assigns a senior official accountability for deciding whether residual security/privacy risk is acceptable. This supports separating technical evidence from the authority to accept risk rather than allowing the implementer to silently accept it.

## 3. Reversible vs difficult-to-reverse decisions
Decision speed should depend on downside, uncertainty and reversibility rather than prestige or technical novelty.

### Reversibility frame
- easily reversible: low migration/data/user continuity cost; can use bounded experiments and short review cycles;
- costly reversible: migration or user/support/search disruption exists; require stronger evidence and exit plan;
- effectively irreversible/high-consequence: data loss, public URL destruction, privacy/security exposure, contractual/regulatory commitments, unsupported client lockout; require explicit owner, stronger validation and recovery/exit design before execution.

**SYNTHESIS:** uncertainty alone is not a reason to delay. High uncertainty + cheap reversibility often favors a bounded experiment; high uncertainty + severe/irreversible downside favors evidence gathering and staged commitment.

## 4. Specialist conflict resolution
The Web Manager does not average specialist opinions. Convert disagreement into a shared decision object.

Example conflict:
- Marketing wants additional third-party measurement;
- Performance sees runtime cost;
- Privacy sees collection/sharing risk;
- Design sees consent/UI cost;
- Engineering sees implementation/maintenance cost.

Resolution sequence:
`shared objective → non-negotiable constraints → evidence per discipline → affected populations/tasks → guardrails → alternatives → residual trade-off → accountable owner decision → validation`.

A specialist may own evidence without owning the final portfolio decision. Legal/security/privacy risk acceptance must not be silently delegated to the person implementing the feature.

## 5. Governance is a lifecycle, not a launch gate
W3C's Accessibility Maturity Model explicitly frames accessibility as organizational policies/processes/outcomes that can be assessed, gaps identified, and improvement tracked. It is informative guidance rather than a normative conformance standard. This supports treating accessibility as recurring governance rather than a one-time audit. WCAG conformance remains a separate technical claim.

The same governance pattern applies to privacy, security and analytics:
`policy/requirement → ownership → design/build controls → evidence → release gate → monitoring → incident/feedback → improvement`.

### Governance boundary guards
- WCAG conformance ≠ accessibility maturity;
- security control present ≠ residual risk accepted;
- privacy notice present ≠ collection justified;
- analytics event present ≠ decision-quality evidence;
- design review passed ≠ browser/device/runtime validation;
- launch gate passed ≠ continuing governance.

## 6. Debt as future constraint
Debt is not limited to code.

Maintain four linked classes:
1. technical debt — architecture, dependency, build, test, migration, compatibility;
2. content debt — stale claims, duplicated truth, screenshots, support docs, localization;
3. operational debt — missing runbooks, untested restore, unclear ownership, alert gaps, manual release steps;
4. governance debt — undocumented risk acceptance, stale ADRs, missing evidence lineage, unresolved specialist boundaries.

### Debt Record
Record origin, affected tasks/surfaces, consequence of leaving it, interest mechanism (how cost/risk compounds), dependency/blocker, remediation/retirement trigger, owner.

**SYNTHESIS:** “debt count” is a weak portfolio metric. Prioritize by user harm/risk, compounding cost, dependency pressure and reversibility.

## 7. Migration/replatforming judgment
Replatforming is justified by a requirement/risk/cost mismatch, not by framework fashion.

Evaluate:
`current constraints → required future capability → migration benefit → transition risk → URL/search continuity → data/schema compatibility → accessibility/performance/security regression → operational capability → dual-run/rollback path → TCO`.

Migration is a temporary distributed system: old/new routes, caches, search indexes, clients, schemas, content and analytics may coexist. A successful code deploy is not a successful migration.

### Migration Decision Gate
Require:
- explicit problem current platform cannot reasonably solve;
- alternative including incremental remediation;
- inventory of URLs/data/integrations/identity/analytics;
- compatibility and migration map;
- rollback/forward-fix boundaries;
- acceptance criteria by user task;
- monitoring and post-migration review;
- decommission conditions.

## 8. Total cost of ownership
TCO must include more than provider price:
`provider spend + engineering time + specialist skill scarcity + release/incident burden + observability/security/compliance work + support/content operations + migration/exit cost + expected failure/recovery cost`.

Cheap infrastructure can be expensive if it increases operational toil or makes recovery uncertain. Managed services can create lock-in yet still be rational when they materially reduce complexity and risk. The correct question is whether dependency and exit cost are understood and acceptable.

## 9. Durable principle vs temporary platform behavior
Classify guidance:
- durable principle: e.g. minimize single points of irreversible data loss;
- current standard: stable normative behavior;
- current platform implementation/policy: CHANGE WATCH;
- project observation: bounded to artifact/device/environment;
- hypothesis: requires validation.

This prevents a current Safari/Chromium/App Store behavior from becoming a permanent company rule.

## 10. MintTap / LogMate bounded applications
### MintTap
Actual production architecture remains OPEN. Before changing `minttap.app`, use the Decision Record Contract to distinguish portfolio IA/product truth requirements from provider/framework preferences. Store/web claims, analytics, support and product release truth should retain explicit owners and evidence lineage.

### LogMate / EFB PWA
The direct-PWA/sync problem is high-consequence because irreplaceable flight records, offline use and managed-device constraints interact. Therefore generic PWA support tables cannot authorize the architecture. Required evidence remains exact-artifact + target-device validation, data durability/recovery, protocol compatibility and bounded transport tests. Direct unattended device-to-device sync remains OPEN until implementation evidence establishes it.

The recent white-screen preview artifact is failure evidence for that artifact path, not proof that Safari/IndexedDB/product logic is categorically unsuitable. This is an example of expert evidence bounding.

## 11. Expert Web Decision Packet
For consequential changes produce one packet rather than scattered specialist conclusions:
1. decision statement and owner;
2. affected tasks/populations/surfaces;
3. constraints/non-negotiables;
4. alternatives;
5. evidence-confidence table;
6. contradictions/unknowns;
7. reversibility/TCO/risk;
8. specialist handoffs and dissent;
9. selected decision with trade-offs;
10. release/validation/rollback criteria;
11. review and supersession trigger.

## 12. Failure modes
- HiPPO/preference presented as evidence;
- consensus mistaken for correctness;
- ADR written after implementation to rationalize a choice;
- legal/security/privacy risk silently accepted by engineering;
- accessibility reduced to a launch checklist;
- analytics optimization overriding guardrails;
- framework/provider novelty used as migration justification;
- sunk cost used to preserve a failing architecture;
- reversible experiment treated as permanent policy;
- temporary platform behavior fossilized into company doctrine;
- production observation generalized beyond its artifact/device/population.

## Stage 12 competency checkpoint 1
PASS at integrated-block level if the Web Manager can:
- structure an ambiguous cross-specialist decision;
- distinguish evidence from inference/preference;
- make uncertainty and contradiction explicit;
- assign risk acceptance/decision ownership;
- reason about reversibility and TCO;
- govern technical/content/operational/governance debt;
- plan migration as a lifecycle rather than a deploy;
- preserve durable principles while marking changing platform behavior;
- define validation and supersession conditions.

## OPEN for Stage 12 closure
A second integrated block should stress-test this system with portfolio scenarios: multi-app ownership and escalation, localization at scale, accessibility/security/privacy/analytics governance conflicts, postmortem learning, competitor/precedent analysis, platform evolution/change-watch, organizational ownership and a final expert gate. Stage 12 is therefore **ACTIVE, not closed**.

## Sources
- NIST Risk Management Framework and Authorize Step, accessed 2026-09-16.
- W3C Accessibility Maturity Model, Note dated 2025-11-04, accessed 2026-09-16.
- W3C WCAG 2 Overview and WCAG 3 status pages, accessed 2026-09-16.
- OWASP Threat Modeling project guidance, accessed 2026-09-16.
