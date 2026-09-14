# 040 — Stage 3 User Goals, Task/Journey Modeling, Cognition, Expectation & Friction Foundations

Status: **STAGE 3 FOUNDATION/PRACTITIONER CHECKPOINT — COMPLETE**  
Research date: 2026-09-15  
Scope: transferable UX judgment for public website and future web-application journeys of a company shipping Apple and Android apps under `minttap.app`.

## Why this block exists

Study 039 established how an individual interaction loop should behave:

`goal → action possibility/signifier → constraint → requested transition → state → feedback → recovery → continuity`

That still leaves a more basic product question unanswered:

> **Should this interaction or step exist at all, and does the sequence help a person complete the real goal without unnecessary memory, uncertainty, interruption, or coercion?**

A flow can have excellent buttons, correct validation and technically sound async state while still fail because:

- the product models an internal company process rather than the user's goal;
- one user task is fragmented across unrelated surfaces;
- users must remember information from previous steps that could be shown again;
- an interruption destroys enough context that resumption becomes guesswork;
- a familiar expectation is violated without useful benefit;
- choice complexity is reduced cosmetically while the underlying decision remains unclear;
- important conditions are hidden until after commitment;
- a protective confirmation is removed as “friction” even though it prevents high-cost mistakes;
- cancellation, privacy or account-control steps are made harder specifically to discourage the user.

This block therefore moves from **interaction correctness** to **task/journey correctness**.

---

# RELATED DOMAIN CHECK

## Web Manager evidence reused

- 034–038 — task-based IA, destination contracts, content hierarchy, navigation/findability and Stage 2 integration;
- 039 — action/state/feedback/error/recovery Interaction Contract.

Stage 2 already established that pages should be task contracts. 040 does not repeat that IA work. It asks whether the **sequence of tasks and decisions** is justified and cognitively supportable.

## Design Studio evidence checked

Current repository state on 2026-09-15:

- `research/interaction/007-interaction-agency-feedback-errors.md` — familiarity, agency, feedback, error recovery and an operational recognition-vs-recall distinction;
- `research/interaction/I001-navigation-history-focus-restoration-interruption.md` — navigation state, resumption, interruption and restoration;
- `progress/LAYOUT_STATUS.md` — Layout/Interaction Stage 1 now **PASS**, Stage 2 entry audit next; human/user-task validation remains explicitly deferred rather than simulated;
- `research/web/W001-web-as-native-medium-history-flexibility-design-contracts.md` — Web as addressable, variable, browser-mediated medium; purpose/user task and direct-entry behavior precede composition;
- `progress/WEB_STATUS.md` — W001 is Practice/Critique; W002 next.

### Transfer choice

**REUSE + PRIMARY-SOURCE VALIDATION + WEB-MANAGER TASK/JOURNEY SYNTHESIS.**

Design Studio owns reusable interaction/design expertise. Web Manager needs a project-level method for deciding which steps, choices, reminders, interruptions and frictions belong in a MintTap web journey and which are implementation or business-process leakage.

---

# 1. SOURCE — human-centred design begins with people, context and their work, not a preselected interface

ISO 9241-210:2019 is the current ISO standard for human-centred design of interactive systems. ISO states that the 2019 edition was reviewed and confirmed in 2025 and remains current. Its scope explicitly includes websites and applications and provides requirements/recommendations for human-centred design activities through the interactive-system life cycle.

Primary source checked 2026-09-15:
- ISO 9241-210:2019 — https://www.iso.org/standard/77520.html

The UK Government Service Standard similarly requires teams to design around user needs and the user's whole problem rather than around technologies, departmental boundaries or preselected solutions. Its service guidance notes that what one team builds is often only part of a larger task and that broken joins between transactions/channels create journey failure.

Primary operational sources checked 2026-09-15:
- GOV.UK Service Standard — Solve a whole problem for users: https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem
- GOV.UK Service Manual — Map and understand a user's whole problem: https://www.gov.uk/service-manual/design/map-a-users-whole-problem
- GOV.UK Service Manual — Learning about users and their needs: https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs

## SYNTHESIS — goal, task, step and control are different layers

Use the following vocabulary:

- **Goal / desired outcome** — what the person ultimately wants to accomplish or know;
- **Task** — a meaningful unit of work necessary to advance that goal;
- **Step** — one part of a task sequence;
- **Action** — an input that requests a state change or navigation;
- **Control** — one interface mechanism through which an action may be expressed;
- **System operation** — internal work performed by the product or backend.

Example:

`Goal: get help for a failed app action`

may contain:

`identify app/context → understand likely issue → try resolution → escalate if unresolved`

It is not naturally:

`open hamburger → click Resources → choose department → fill internal category code → press Submit`.

The second sequence may describe the implementation. It does not prove those steps belong in the user's task.

## MINTTAP DIRECTION

For important flows, start with the user outcome and work inward to the minimum justified task sequence. Do not start with existing forms, database fields, team boundaries or analytics funnel steps.

---

# 2. Journey is an observable task/state sequence, not a marketing diagram

A journey map is useful only when its units correspond to meaningful user work, state, evidence or transitions.

GOV.UK explicitly recommends understanding the larger journey because apparently separate transactions may be one task from the user's perspective. It identifies dead ends, ambiguous transaction choice, duplicated/confusing content and poorly joined online/offline elements as journey problems.

Primary source:
- https://www.gov.uk/service-manual/design/map-a-users-whole-problem

## SYNTHESIS — operational journey model

For Web Manager, model a journey as:

`entry/context`
`→ user goal`
`→ required knowledge/prerequisites`
`→ task 1 / state`
`→ decision or commitment`
`→ task 2 / state`
`→ ...`
`→ goal achieved / unresolved / abandoned`
`→ recovery or escalation`

For every transition record:

1. what the user is trying to achieve;
2. what they must know now;
3. what information the system already knows;
4. what input is truly required from the user;
5. what state changes;
6. what commitment or consequence occurs;
7. what can interrupt the task;
8. what must survive interruption;
9. what failure/recovery path exists.

### Counterexample — funnel-only model

`Landing → CTA → Form → Success`

can be useful for analytics but is not a sufficient UX model. It says nothing about:
- whether the CTA matches the user's goal;
- whether the form asks unnecessary questions;
- whether prerequisites were disclosed before the form;
- whether a failed submit preserves work;
- whether success means a local acknowledgement or actual remote completion;
- whether the user can resume after interruption.

Analytics funnels describe observed/desired transitions. They do not determine which transitions are user-centred.

---

# 3. Critical path: remove unjustified work, not merely screens

## SYNTHESIS

Define the **user critical path** as the smallest sequence of user-visible tasks/decisions required to achieve the intended outcome under the relevant constraints.

This is not necessarily the fewest clicks or fewest pages.

A step is justified when it materially serves one or more of:

- task necessity;
- safety/error prevention;
- legal/policy requirement;
- informed consent/decision;
- authentication/authorization;
- necessary disambiguation;
- required evidence/input;
- recovery or escalation.

A step is suspect when it exists mainly because:

- internal ownership is fragmented;
- a database schema asks for it;
- one channel cannot share data with another;
- analytics prefers another pageview;
- marketing wants another persuasion opportunity;
- legacy workflow is copied without current justification.

### Important correction

**Fewer steps ≠ automatically easier.**

Combining all information and choices into one surface can increase search, comparison and error cost. Splitting a high-consequence decision into review/commit steps can improve control. The professional question is not raw step count but **task cost and reason for each transition**.

---

# 4. SOURCE — working memory is limited, but there is no universal UI item-count rule

Nelson Cowan's 2001 review re-examined short-term-memory capacity and argued for a limited central capacity often around four chunks under constrained conditions. The paper itself is about memory experiments and boundary conditions, not menu design.

Primary research source:
- Cowan N. *The magical number 4 in short-term memory: a reconsideration of mental storage capacity*. Behavioral and Brain Sciences. 2001;24(1):87–114. DOI: 10.1017/S0140525X01003922. PubMed: https://pubmed.ncbi.nlm.nih.gov/11515286/

W3C's Cognitive Accessibility guidance takes a directly applicable design direction: processes should not require users to remember information from previous steps when the information can be provided in the current step; previous-step summaries, orientation and easy traversal can reduce memory dependence.

Primary W3C guidance checked 2026-09-15:
- Ensure Processes Do Not Rely on Memory: https://www.w3.org/WAI/WCAG2/supplemental/objectives/o6-memory/
- Do Not Rely on Users Calculations or Memorizing Information: https://www.w3.org/WAI/WCAG2/supplemental/patterns/o6p05-low-cognition/

## SYNTHESIS — externalize context before reducing content blindly

The valid transfer is:

> Do not make successful task completion depend on remembering transient information when the interface can preserve, repeat or summarize it.

Useful mechanisms include:
- visible current selection;
- prior-step summaries;
- persistent app/account/object identity;
- stable labels;
- visible constraints and prerequisites;
- saved draft/input;
- review screens for consequential submissions;
- breadcrumb/step context where meaningful;
- explicit state/history rather than hidden mode.

### Rejected folklore

Do **not** convert memory research into rules such as:
- show at most four menu items;
- every group must contain 4±1 controls;
- every task must fit on one screen;
- seven items is always acceptable because of Miller's 7±2.

Chunking depends on knowledge, task, encoding and organization. Interface design should reduce unnecessary recall and validate actual task performance rather than enforce a magic count.

---

# 5. Recognition, recall and transfer learning

Design Studio Study 007 already establishes a useful operational distinction:

- recognition-heavy interaction exposes visible choices, labels and context;
- recall-heavy interaction requires hidden gestures, remembered commands, uncommon icon meanings or values from prior steps.

This block does not restudy that distinction. It extends it to **journey architecture**.

## SYNTHESIS

Ask at every step:

- What can the user recognize from the current interface?
- What must they recall from earlier in the journey?
- What domain knowledge must they already possess?
- Can the system supply or preserve that information instead?
- If expert recall is intentionally supported for speed, is a discoverable recognition path still available where the audience requires it?

### MINTTAP example pattern

If a support form already knows the user arrived from `/apps/<app>/support/...`, asking the user to remember and select the app again may be redundant unless there is a genuine need to change context.

If the choice matters, preserve the known value visibly and allow correction rather than hiding it.

## DEPENDENCY

Actual MintTap flows are not yet known, so this remains a design requirement rather than a claim that a current form contains redundant steps.

---

# 6. SOURCE — interruption is a task-state problem, not only a notification problem

W3C Cognitive Accessibility guidance recommends limiting interruptions because interruptions can prevent people with memory or attention impairments from completing tasks.

Primary guidance:
- Limit Interruptions: https://www.w3.org/WAI/WCAG2/supplemental/patterns/o5p01-minimal-interruptions/

Design Studio I001 already models navigation, task state, focus and restoration separately and warns that empirical resumption quality requires user/task testing.

## SYNTHESIS — resumption requires reconstruction cues

When interruption is plausible, preserve enough evidence for the user to answer:

1. Where am I?
2. What was I doing?
3. What has already been completed or committed?
4. What remains?
5. Did anything change while I was away?
6. Can I continue safely from here?

Possible state to preserve separately:
- entered data/draft;
- current step/location;
- selected object/app/account;
- pending remote operation;
- validation/error state;
- filters/search query;
- authoritative data freshness;
- focus/scroll when useful.

### Failure mode

Restoring the same URL while losing the draft or pending-operation truth is not successful resumption. Conversely, blindly restoring stale form state after the authoritative object changed can also be wrong.

039's state/commitment model therefore remains part of the journey contract.

---

# 7. Choice complexity: Hick/Hyman is evidence about uncertainty, not a menu-item law

W. E. Hick's 1952 experiments applied information theory to controlled choice-reaction tasks with different numbers/probabilities of stimulus-response alternatives. Ray Hyman's 1953 work similarly studied stimulus information and reaction time.

Primary sources:
- Hick WE. *On the Rate of Gain of Information*. Quarterly Journal of Experimental Psychology. 1952;4(1):11–26. DOI: 10.1080/17470215208416600
- Hyman R. *Stimulus information as a determinant of reaction time*. Journal of Experimental Psychology. 1953;45(3):188–196. DOI: 10.1037/h0056940. PubMed: https://pubmed.ncbi.nlm.nih.gov/13052851/

A later scholarly review identifies important limitations and moderators including stimulus-response compatibility, practice, very large set sizes and sequential dependencies.

Validation source:
- Proctor RW, Schneider DW. *Hick's law for choice reaction time: A review*. Quarterly Journal of Experimental Psychology. 2018;71(6):1281–1299. DOI: 10.1080/17470218.2017.1322622

## SYNTHESIS

The transferable principle is narrower than common UX folklore:

> Decision time/cost can increase with uncertainty and with poorly structured alternatives, but raw option count alone does not determine usability.

For a MintTap decision surface consider:
- whether alternatives are meaningfully distinct;
- whether one option is clearly dominant for the user's task;
- whether grouping reflects the user's model;
- whether labels make consequences predictable;
- whether choices can be deferred until relevant;
- whether the user needs simultaneous comparison;
- familiarity and practice;
- whether reducing visible options merely hides them behind extra navigation.

### Rejected rule

Do not say “Hick's Law means fewer menu items are always better.” That conclusion is not established by the original experiments.

---

# 8. Progressive disclosure is information timing, not aesthetic cleanup

Stage 2 already established that progressive disclosure exchanges simultaneous visibility for discovery, interaction, memory and state cost.

040 adds a task-sequence test.

## SYNTHESIS — disclose by decision dependency

For each piece of information ask:

- Is it required to decide whether to begin?
- Is it required before entering data?
- Is it required before committing?
- Is it needed only for an exceptional branch?
- Does it need simultaneous comparison with another item?
- Can it safely remain available on demand?

### Preserve early visibility for

- eligibility/prerequisites that could make the task pointless;
- price/material consequence;
- irreversible/destructive consequence;
- privacy/data use material to the decision;
- unsupported platform/account state;
- constraints that would invalidate significant effort;
- comparison-critical facts.

### Good candidates for later/on-demand depth

- advanced explanation after the primary concept is understood;
- troubleshooting branches not relevant to most users;
- implementation detail not needed for the current decision;
- secondary evidence that remains easily discoverable.

### Failure mode

A “clean” flow that asks for ten minutes of information and only then reveals the user is ineligible has lower visual density but worse journey design.

---

# 9. Expectation and consistency: preserve learned contracts, not visual sameness

Apple's familiarity direction, Design Studio Study 007 and Web W001 all converge on a bounded principle: familiar behavior and stable semantic relationships reduce unnecessary relearning, but visual originality is still allowed.

## SYNTHESIS

Users form expectations at several levels:

- **platform** — links navigate, Back traverses history, standard controls behave recognizably;
- **site/product** — the same label and component should normally preserve the same semantic promise;
- **journey** — progress, commitment and recovery should remain coherent across steps;
- **domain** — concepts such as account, app, subscription, support case or privacy choice should retain stable meaning.

Consistency should therefore be evaluated by **transfer of learned meaning**, not by pixel identity.

### Legitimate inconsistency

Different behavior is appropriate when the underlying task or consequence is materially different, provided the difference is communicated.

Example:
- a routine preference toggle can commit immediately;
- deleting an account may require a review/confirmation stage because consequence and reversibility differ.

Forcing visual/behavioral sameness would ignore the task model.

---

# 10. Friction taxonomy — not all friction is bad

“Reduce friction” is insufficient as a UX objective because some friction protects people or makes decisions informed.

## A. Necessary friction

Work inherent to completing the task correctly.

Examples:
- providing information the service genuinely cannot know;
- authenticating before viewing protected data;
- choosing among materially different outcomes.

Goal: make the necessity and requirement clear; do not pretend it can always be removed.

## B. Protective friction

Deliberate effort or pause that reduces meaningful risk.

Examples:
- reviewing an irreversible action;
- re-authentication for a sensitive account operation;
- showing material consequences before commitment;
- preventing accidental destructive input.

Goal: proportional protection based on consequence and reversibility, consistent with Study 039.

## C. Accidental friction

Effort caused by design, architecture or organizational defects rather than the user's goal.

Examples:
- re-entering known information;
- losing a draft after validation failure;
- being sent to the homepage to rediscover support context;
- hidden prerequisites;
- inconsistent terms for the same object;
- duplicated authentication caused by poorly joined systems.

Goal: remove or redesign.

## D. Manipulative / obstructive friction

Effort or interface asymmetry intentionally or materially used to steer users away from a free and informed choice for the operator's benefit.

This is not only an ethics abstraction. It can be regulated.

### SOURCE — FTC

The U.S. Federal Trade Commission's 2022 staff report *Bringing Dark Patterns to Light* describes design practices that can obscure, subvert or impair consumer choice and decision-making. FTC enforcement has also targeted cancellation obstacles and asymmetric processes.

Primary government sources:
- FTC report announcement, 2022-09-15: https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers
- FTC Vonage action, 2022-11-03: https://www.ftc.gov/news-events/news/press-releases/2022/11/ftc-action-against-vonage-results-100-million-customers-trapped-illegal-dark-patterns-junk-fees-when-trying-cancel-service

### SOURCE — EU Digital Services Act

Regulation (EU) 2022/2065 Article 25 prohibits providers of online platforms within its scope from designing/organising/operating interfaces in ways that deceive/manipulate recipients or otherwise materially distort or impair free and informed decisions. The Article explicitly identifies examples for possible guidance including making service termination harder than subscription.

Primary law source checked 2026-09-15:
- EUR-Lex, Regulation (EU) 2022/2065, Article 25: https://eur-lex.europa.eu/eli/reg/2022/2065/oj

## Important legal scope limit

Do **not** infer that every MintTap website/app is an “online platform” within DSA Article 25, or that a particular FTC theory automatically applies. Applicability is a legal question requiring the product/business/jurisdiction facts.

The transferable design rule is independent of that unresolved legal scope:

> Do not intentionally make a user-protective or user-exit choice harder merely because the company prefers the opposite outcome.

## MINTTAP DIRECTION — symmetry test

For paired choices such as:
- subscribe / cancel;
- enable / disable;
- create / delete account;
- consent / withdraw;
- start / stop a recurring service;

compare:
- discoverability;
- number/type of steps;
- language clarity;
- authentication burden;
- waiting/escalation burden;
- consequence disclosure;
- available channel;
- reversibility.

Asymmetry can be justified by risk/security/legal constraints. If so, record that reason. Commercial preference alone is not a UX justification.

---

# 11. Trust and uncertainty are journey variables

A user often pauses not because the control is hard to operate but because the outcome is uncertain.

## SYNTHESIS

At consequential decision points, reduce **relevant uncertainty**, not merely interaction count.

Questions a user may need answered before acting:
- What exactly will happen?
- To which account/app/item?
- Is this immediate or pending?
- Will I lose data?
- Can I reverse it?
- Does it cost money?
- What information will be shared?
- How long will it take?
- What happens if the network fails or I leave?

A short flow that hides these answers can produce more hesitation and error than a slightly longer flow that establishes commitment truth.

### Distinction

Useful assurance is not the same as decorative “trust badges.” Trust-related claims must be truthful and evidence-backed under the content-truth model from Stage 2.

---

# 12. Task/Journey Contract for MintTap

For a consequential or multi-step web journey, add this contract before visual design.

## A. User outcome
- What does the user believe they are trying to accomplish?
- What counts as actual completion?

## B. Entry contexts
- Store, search, direct link, in-app link, homepage, support article, authenticated state?
- What context is already known?

## C. Preconditions
- Eligibility, authentication, app/platform, account state, data needed, policy constraints.
- Which must be shown before meaningful effort begins?

## D. Task sequence
For each task/step:
- purpose;
- user-visible information;
- required input;
- information already known by the system;
- state transition;
- commitment level;
- exit/back behavior;
- recovery.

## E. Cognitive dependency
- What must be recognized?
- What must be recalled?
- What prior information should be repeated/summarized?
- What domain knowledge is assumed?

## F. Decision structure
- alternatives;
- grouping;
- consequence labels;
- simultaneous-comparison need;
- what can be deferred safely.

## G. Interruption/resumption
- what state survives;
- how the user re-orients;
- stale/changed authoritative state handling;
- pending/outcome-unknown handling from 039.

## H. Friction classification
Classify each nontrivial burden as:
- necessary;
- protective;
- accidental;
- potentially manipulative/obstructive.

Record the justification for necessary/protective friction.

## I. Trust/uncertainty
- which material questions must be answered before commitment;
- evidence/source for claims;
- status/commitment truth after action.

## J. Evidence/validation
- standards/policy checks;
- analytics evidence;
- support/contact evidence;
- usability test task;
- target-user comprehension and confidence;
- accessibility/browser/device validation.

---

# 13. Journey failure taxonomy

Use this before proposing UI polish.

## Goal mismatch
The system optimizes an internal process rather than the user's intended outcome.

## Scope fragmentation
One user problem is split across disconnected products/pages/channels without coherent handoff.

## Redundant work
The user repeats information/actions the system already has or could preserve.

## Premature work
The user invests effort before eligibility, constraints or consequence are known.

## Recall dependency
Completion depends unnecessarily on memory of previous steps, values or hidden state.

## Choice-structure failure
Alternatives are ambiguous, poorly grouped, unexpectedly hidden or impossible to compare.

## Expectation-transfer failure
A learned label/pattern changes meaning without a task-based reason.

## Interruption/resumption failure
The user returns without enough state/context to continue safely.

## Commitment uncertainty
The user cannot tell whether the operation is draft, pending, committed, reversible or final.

## Accidental friction
Extra burden comes from product/organization defects rather than task necessity.

## Protective-friction mismatch
A high-risk action is under-protected or a low-risk/reversible action is needlessly blocked.

## Manipulative asymmetry
The interface materially favors the operator's preferred choice by hiding, delaying or burdening an alternative without user-protective justification.

## Evidence failure
A supposed “simplification” is declared better without task/user evidence.

---

# 14. Competency checks

Web Manager should now be able to answer the following without defaulting to pattern folklore.

### Case A — “Can we remove this confirmation to reduce friction?”
Ask consequence, reversibility, likelihood/cost of accidental action and recovery. Friction is not bad merely because it adds one step.

### Case B — “There are eight choices, so Hick's Law says reduce them to five.”
Reject the numerical inference. Analyze uncertainty, familiarity, grouping, labels, frequency, comparison and whether hiding options adds navigation/memory cost.

### Case C — “This wizard has only one question per page, so cognitive load is low.”
Not established. Determine whether users must remember prior answers/context, whether prerequisites are delayed, and whether navigation/resumption preserves state.

### Case D — “The support journey takes six screens; make it three.”
First identify the user goal and purpose of each step. Remove redundant/internal work, but keep justified disambiguation, consequence or recovery steps.

### Case E — “Cancellation has more steps than signup.”
Investigate whether security/legal/consequence differences justify the asymmetry. If not, treat it as a serious UX/ethical risk and potentially a policy/legal issue depending on jurisdiction/service scope.

### Case F — “The analytics funnel converts better after hiding a privacy choice.”
Conversion improvement does not establish UX quality or ethical acceptability. Check informed-choice requirements, regulatory scope, user goal and long-term trust/support consequences before accepting the change.

---

# 15. Measurement boundary

GOV.UK's service guidance recommends combining performance metrics with user research and, for end-to-end journeys, directly testing believable tasks and measuring outcomes such as successful completion, time, abandonment and perceived confidence/difficulty.

Primary operational sources:
- Measuring the success of your service: https://www.gov.uk/service-manual/measuring-success/measuring-the-success-of-your-service
- Usability benchmarking a website or whole service: https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service

## SYNTHESIS

Later MintTap analytics/experimentation work should not define “better journey” as conversion rate alone.

Depending on the flow, relevant measures may include:
- task completion;
- correct outcome, not merely final-page reach;
- abandonment location/reason;
- time/effort;
- repeated input;
- error/recovery;
- support escalation;
- confidence/comprehension;
- cancellation/deletion completion where relevant;
- downstream reversals/refunds/complaints.

### VALIDATION

No current MintTap user journey is claimed to have any particular cognitive or friction problem. Actual judgments require the real flow, analytics/support evidence and human testing.

---

# 16. Durable principles vs change watch

## Durable principles

- Start from user outcome, not control or organization structure.
- Separate goal, task, step, action, control and system operation.
- Model journeys as task/state/commitment sequences.
- Remove unjustified work rather than optimizing raw click count.
- Reduce unnecessary recall by externalizing/preserving context.
- Do not turn working-memory research into fixed item-count rules.
- Treat Hick/Hyman as evidence about choice uncertainty under bounded tasks, not a universal menu formula.
- Time information according to decision dependency.
- Preserve learned semantic contracts unless task differences justify change.
- Distinguish necessary/protective/accidental/manipulative friction.
- Reduce material uncertainty before consequential commitments.
- Conversion metrics cannot by themselves establish usability or ethical quality.

## CHANGE WATCH

Re-check when relevant:
- FTC rulemaking/enforcement affecting subscriptions, cancellation, endorsements or interface practices;
- EU DSA/dark-pattern guidance and actual applicability to the relevant MintTap service;
- Apple/Google policy around account deletion, subscription management, privacy/consent and external web flows;
- W3C cognitive accessibility guidance as it evolves;
- jurisdiction-specific consumer/privacy law.

Do not turn current regulatory examples into timeless universal legal statements.

---

# 17. OPEN / DEPENDENCIES

Real MintTap decisions require verified facts not yet available in the Web Manager record:

- actual high-frequency/high-value user goals;
- real app/site entry channels;
- account creation/authentication/deletion behavior;
- subscription/payment model;
- privacy/data-control journeys;
- support escalation workflow;
- cross-app context sharing;
- which information the web can know from app/store/deep-link context;
- analytics funnel definitions and current drop-off;
- support/contact reasons;
- target users' expertise and accessibility needs;
- interruption patterns across desktop/mobile/app↔web;
- legal jurisdictions and service classifications relevant to manipulative-design rules.

Do not infer these from generic app-company practice.

---

# 18. DESIGN STUDIO HANDOFF

Use **Stage 2 Page Contract + 039 Interaction Contract + 040 Task/Journey Contract** together.

## To Web Design / Layout-Interaction

For future MintTap project work validate:

1. whether each visible step corresponds to a real user task or justified protection;
2. whether known context is preserved rather than re-requested;
3. whether prior-step information needed for the current decision is visible/summarized;
4. whether progressive disclosure follows decision dependency rather than aesthetic minimalism;
5. whether responsive recomposition preserves task sequence and comparison requirements;
6. whether interruption/resumption returns enough task and commitment context;
7. whether familiar labels/controls preserve semantic expectations across pages;
8. whether necessary/protective friction remains proportional and explainable;
9. whether opt-out/cancel/delete/privacy alternatives are not visually or procedurally obstructed without legitimate reason;
10. whether human testing supports claims about comprehension, effort, confidence or task performance.

### Incoming Design Studio evidence reused

- Interaction 007: recognition-vs-recall and familiarity baseline;
- I001: navigation/resumption/restoration contract;
- W001: purpose/task/direct-entry before composition and relationship-over-coordinate Web model;
- current Layout/Interaction Stage 1 PASS does not substitute for live MintTap human testing;
- Web W001 Practice/Critique does not imply Web Foundation or production PASS.

No Design Studio canonical file was edited.

---

# 19. Stage 3 checkpoint verdict

**PASS at the intended foundation/practitioner checkpoint for this integrated block.**

The Web Manager can now distinguish:

- user outcome from implementation steps;
- journey/task architecture from analytics funnels;
- minimum justified work from minimum click count;
- memory limitation evidence from item-count folklore;
- recognition support from required recall;
- choice uncertainty from raw option count;
- progressive disclosure from indiscriminate hiding;
- consistent semantics from visual sameness;
- necessary/protective friction from accidental/manipulative friction;
- task completion from conversion;
- standards/expert synthesis from actual human usability evidence.

This does not establish target-user performance for any real MintTap journey. That remains a project validation gate.

## Highest-value next Stage 3 block

Proceed next to **Forms, Input, Choice, Validation & Multi-Step Transaction Design** as an integrated task system.

Rationale:
- 039 established individual action/state/error/recovery mechanics;
- 040 established goal/task/journey/cognitive/friction architecture;
- forms and multi-step transactions are the first major surface where those two contracts must work together in concrete web interaction;
- MintTap support, contact, privacy/account-control and possible future authenticated flows are likely to depend on these skills;
- this should deepen field semantics, input collection, defaults, validation timing, error-summary/focus behavior, conditional questions, save/resume, review/commit and native-vs-custom controls without drifting into visual styling or backend/provider implementation.
