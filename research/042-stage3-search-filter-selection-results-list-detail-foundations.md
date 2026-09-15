# 042 — Stage 3 Search, Filtering, Selection, Results & List/Detail Interaction Foundations

Status: **FOUNDATION/PRACTITIONER CHECKPOINT — PASS**  
Research date: 2026-09-15  
Scope: on-site retrieval and result interaction for `minttap.app`; **not SEO/search-engine discovery**.

## Why this block exists

Stage 2 established information architecture, findability and direct-entry contracts. Studies 039–041 established interaction state, task/journey and form/transaction mechanics. The unresolved prerequisite is retrieval inside a growing app-company website: how a user locates an app, support topic, known issue or document when browse navigation alone is insufficient.

This block does **not** assume MintTap needs site search at launch. Search is additional product complexity and must be justified by corpus size, retrieval tasks and evidence.

## RELATED DOMAIN CHECK

Latest `yhappcom/design-studio/progress/WEB_STATUS.md` checked 2026-09-15. Web Design now has W001–W003; W003 defines responsive recomposition as `task → relationship → stress signal → owner → adaptation → invariant → validation`, but measured browser execution remains open. Web Foundation remains NOT PASSED and complete task surfaces including search/filter/list-detail remain a gap. This makes 042 a useful incoming state/task contract rather than duplicate visual research.

No Design Studio canonical file is edited here.

---

# 1. SOURCE — search is a semantic control and region, but semantics do not design the retrieval system

WHATWG HTML defines `input type=search` for search-field input and defines form submission behavior, including GET-form query serialization. WAI-ARIA defines a `search` landmark for a region containing search functionality; WAI examples note that multiple search landmarks need distinguishable labels.

Primary sources checked 2026-09-15:
- WHATWG HTML Living Standard — forms/input/search: https://html.spec.whatwg.org/multipage/input.html#text-(type=text)-state-and-search-state-(type=search)
- WHATWG HTML Living Standard — form submission: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#form-submission-2
- WAI-ARIA 1.2 — search role: https://www.w3.org/TR/wai-aria-1.2/#search
- WAI ARIA Practices — Search Landmark: https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/examples/search.html

### SYNTHESIS

A semantically correct search box does not establish:
- what corpus is searched;
- query interpretation;
- ranking;
- filters;
- result identity;
- loading/error/empty states;
- URL/history behavior;
- selection continuity.

Therefore search must be modeled as a retrieval system, not an input component.

---

# 2. FOUNDATIONAL MODEL — browse, search, filter, sort and ranking are different operations

### SYNTHESIS

- **Browse/navigation**: traverse a known information structure.
- **Search**: express an information need and retrieve candidate objects from a corpus.
- **Filter**: constrain an existing candidate set by explicit attributes/conditions.
- **Sort**: reorder a set by a declared comparison key/direction.
- **Ranking**: order candidates by a relevance/utility function that may not be directly controlled by the user.

Combining all five under a generic “search” state makes behavior, analytics and recovery ambiguous.

### MINTTAP DIRECTION

If future support content is small and well-taxonomized, prefer browse/direct links. Add search only when known-item retrieval, corpus scale, task diversity or observed failures justify its operational cost.

**Search does not repair missing content or weak IA.**

---

# 3. Query state is not one string

### SYNTHESIS

A useful state model separates:

`draft query → submitted query → scope → active filters → sort/rank mode → retrieval status → result set → selected item → list position/context`

Draft and submitted query must be distinguishable. If a user edits the field after results are returned, the interface should not imply that the visible results already correspond to the unsubmitted draft unless retrieval actually updates immediately.

Immediate search is a different contract: debounce/cancellation, stale-response protection and status exposure become material.

### Failure example

Request A for `sync` begins. User changes query to `backup`, request B begins, B returns first, then A returns later and overwrites the result list. The pixels may look normal but the visible result set no longer corresponds to current query state.

### REQUIRED IMPLEMENTATION CONTRACT

Associate responses with the query/request state that produced them; stale responses must not silently become authoritative current results.

---

# 4. Filters need explicit cardinality and application semantics

A filter is not merely a checkbox drawer.

For each filter specify:
- attribute and scope;
- single vs multiple selection;
- OR/AND semantics within and across groups;
- whether counts represent current or unfiltered corpus;
- immediate vs explicit Apply;
- reset/clear semantics;
- zero-result prevention or recovery;
- persistence/history behavior.

### SYNTHESIS

**Immediate apply** reduces a separate commit action but can produce repeated network work, focus/position instability and difficult mobile panel behavior. **Explicit apply** batches decisions but creates draft-vs-applied state. Neither is universally superior.

Selected constraints must remain visible enough that a user can explain why the result set changed and can remove constraints without reconstructing hidden state.

---

# 5. URL/history/shareability are retrieval-state decisions

WHATWG form GET submission serializes form data into the URL query. The URL Standard defines URL query/search parameters. Browser session history can represent navigable state; History API behavior is separate from URL serialization.

Primary sources checked 2026-09-15:
- WHATWG HTML form submission: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#form-submission-2
- WHATWG URL Standard: https://url.spec.whatwg.org/
- HTML Living Standard — session history/navigation: https://html.spec.whatwg.org/multipage/nav-history-apis.html

### SYNTHESIS

When retrieval state is safe and meaningful to expose, URL representation can support reload, bookmark, share, direct entry and Back/Forward continuity. It is not necessary to serialize every transient UI state.

### PRIVACY LIMIT

Do not place sensitive or private search terms into URLs merely for convenience. URLs can surface through browser history, copied links, logs, analytics/referrers and other infrastructure. URL-state policy must therefore classify the information before serialization.

### MINTTAP DIRECTION

Public app/support taxonomy, query and non-sensitive filters are candidates for canonical URL state if search is introduced. Private account/support-case queries are not automatically candidates.

---

# 6. Results need identity, evidence and destination promise

A result row/card should expose enough information to distinguish candidates and predict the destination.

Possible object-specific signals:
- title/name;
- app/product scope;
- content type;
- concise contextual excerpt;
- platform/version applicability where decision-critical;
- current/retired/known-issue status where relevant.

### SYNTHESIS

Do not show metadata because it exists. Show the minimum evidence needed to choose correctly among plausible candidates.

Result presentation is therefore coupled to Stage 2 content-object identity and scope. Search cannot compensate for ambiguous titles or app context.

---

# 7. Loading, empty, no-result, partial, stale and error are different states

### REQUIRED STATE TAXONOMY

`idle / loading / success-with-results / success-empty / partial / stale / known-error / canceled / outcome-unknown`

Key distinction:

**0 results ≠ retrieval failure.**

A successful query with no matching objects is evidence about the corpus/query. A failed request says the system does not currently know the answer.

No-result causes may include:
- query mismatch;
- filter overconstraint;
- wrong scope;
- genuine content absence;
- index/content synchronization lag.

Recovery should correspond to the cause when known: clear a constraint, broaden scope, revise query, browse taxonomy, or escalate to support. Never fabricate “no results” from a backend failure.

---

# 8. Dynamic result changes need an accessibility notification strategy

WCAG 2.2 Success Criterion 4.1.3 requires status messages to be programmatically determinable so assistive technology can present them without receiving focus. WAI ARIA practices provide live-region mechanisms, but live regions are not a mandate to announce every mutation.

Primary sources checked 2026-09-15:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/#status-messages
- Understanding SC 4.1.3: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- WAI-ARIA 1.2 live regions: https://www.w3.org/TR/wai-aria-1.2/#dfn-live-region

### SYNTHESIS

For dynamic retrieval, identify which changes are status information useful to the task (for example result count after a submitted query/filter) and expose them without automatically moving focus. Avoid chatty announcements for every keystroke or intermediate mutation.

Keyboard focus, visible selection and AT announcement are separate channels; one must not be used as a substitute for the others.

---

# 9. List → detail → Back is a continuity contract

Stage 1/039 and Design Studio Interaction evidence already establish history/focus restoration concerns. 042 applies them to retrieval.

### SYNTHESIS

After selecting a result, inspecting detail and returning, preserve enough context to continue the task:
- submitted query;
- scope;
- filters;
- sort/rank mode;
- meaningful list position;
- prior selection/focus target where appropriate.

Reload/share may intentionally preserve a smaller subset than same-session Back. These are different continuity levels and should be specified rather than assumed.

### FAILURE

Returning from an article to a reset search page forces the user to reconstruct both query and location. This is not merely inconvenience; it breaks the retrieval task state.

---

# 10. Suggestions/autocomplete are a separate retrieval surface

Suggestions may represent query completions, popular searches, exact entities, recent queries or direct destinations. These have different sources and privacy implications.

### SYNTHESIS

Do not add autocomplete merely because search inputs commonly have it. Specify:
- suggestion source;
- whether it predicts a query or is itself a destination;
- keyboard/touch behavior;
- active-option semantics;
- cancellation/loading/error behavior;
- history/personalization privacy;
- localization/tokenization limits.

If suggestions are not materially useful, ordinary search submission is simpler and more robust.

---

# 11. Responsive retrieval is recomposition, not feature removal

### DEPENDENCY — Design Studio Web W003

W003's current model is reusable:

`task → relationship → stress signal → owner → adaptation → invariant → validation`

For retrieval, invariants may include:
- current query/scope remains visible or recoverable;
- active filters remain inspectable/removable;
- result identity remains sufficient to choose;
- list/detail return preserves context;
- essential actions do not require hover;
- focus/source/task order remains coherent.

A narrow viewport may move filters into a disclosure/sheet, but hiding the existence of active filters or changing their semantics is not harmless recomposition.

### VALIDATION

Design Studio W003 has an executable browser harness but measured results are currently OPEN. Do not cite W003 as production browser proof.

---

# 12. Ranking and sorting require truthfulness

### SYNTHESIS

A user-selected sort should describe its key accurately (`Newest`, `A–Z`, etc.). A relevance ranking can combine multiple signals, but labels must not imply an objective ordering the system does not implement.

If sponsored/promoted results ever exist, commercial placement must not masquerade as organic relevance. This is a future policy/ethics dependency, not a current MintTap fact.

### OPEN

No verified MintTap requirement currently establishes site search, ranking, personalization, sponsorship or search analytics.

---

# 13. Retrieval Contract — reusable project artifact

For a material search/filter/list-detail surface, specify:

1. user information need and entry context;
2. corpus and content-object types;
3. whether browse alone is sufficient;
4. searchable fields and scope;
5. draft vs submitted query behavior;
6. suggestion model if any;
7. filter groups, cardinality and AND/OR semantics;
8. immediate vs explicit filter application;
9. sorting vs ranking model;
10. selected-filter visibility/reset behavior;
11. URL/history/share/bookmark/privacy policy;
12. result identity/evidence/destination promise;
13. pagination/load-more/infinite model if needed;
14. idle/loading/results/empty/partial/stale/error/canceled states;
15. no-result cause/recovery model;
16. stale-response/concurrency protection;
17. list/detail selection, focus and position continuity;
18. keyboard/touch/hover-independent behavior;
19. status-message/AT exposure strategy;
20. responsive/localization/long-content stress;
21. analytics/privacy requirements;
22. human validation required for findability/usability claims.

---

# 14. Failure taxonomy

Diagnose before redesigning:

- **corpus failure** — needed content/object is absent;
- **scope failure** — user searches the wrong/unclear corpus;
- **query-state failure** — draft/submitted/current result state disagree;
- **ranking failure** — plausible target exists but is buried/misordered;
- **filter-model failure** — constraints/cardinality/AND-OR semantics mismatch expectation;
- **hidden-constraint failure** — active filters are not apparent;
- **concurrency failure** — stale response replaces current results;
- **state-classification failure** — empty is shown for error, stale as current, etc.;
- **result-identity failure** — candidates cannot be distinguished;
- **continuity failure** — detail/Back/reset loses retrieval context;
- **URL/privacy failure** — sensitive state leaks or shareable state cannot be reproduced;
- **accessibility failure** — focus, semantics or dynamic status exposure breaks the task;
- **responsive failure** — narrow layout removes or obscures retrieval state;
- **localization failure** — tokenization, labels, wrapping or result evidence fails in target language.

---

# 15. MintTap applicability

### VERIFIED FACT

MintTap is an Apple/Android app company operating `minttap.app`; the repository does not currently establish a production corpus large enough to justify site search.

### MINTTAP DECISION

Do **not** make launch-time site search a default requirement. Begin with Stage 2 task-based IA, app-specific support routing, meaningful labels and direct-entry URLs. Introduce retrieval UI when real content volume/tasks justify it.

If introduced, public support retrieval should preserve app scope and avoid making users re-identify an app already known from the entry path.

### OPEN

Need project evidence for:
- number/growth rate of apps and support articles;
- known-item vs exploratory retrieval frequency;
- support search terms and zero-result patterns;
- Korean/English tokenization and synonym needs;
- backend/index technology and freshness guarantees;
- whether search analytics are acceptable under privacy policy;
- pagination/large-result requirements;
- authenticated/private support search.

---

# 16. Design Studio handoff

## Web Design

Incoming contract for future complete task-surface practice:
- distinguish query/filter/sort/rank states visually and behaviorally;
- preserve active constraints across responsive recomposition;
- validate narrow widths, long KO/EN content, real browser zoom and keyboard behavior;
- validate filter disclosures without hiding current state;
- validate result-list/detail return and focus restoration;
- test dynamic result count/status without inappropriate focus theft;
- test hover-independent essential actions and touch target behavior.

W003 currently supports the adaptation-ownership framework but not measured production proof.

## Layout / Interaction

Challenge:
- immediate vs explicit apply trade-offs;
- stale-response cancellation/reconciliation;
- list/detail history/focus restoration;
- selection continuity after mutation;
- partial/stale/outcome-unknown representation.

## Type / Color

When retrieval surfaces become real, validate long bilingual result titles/metadata, dense scanning, semantic state distinction, forced colors and delivered-font fallback without destroying result comparability.

No Design Studio canonical file was edited.

---

# 17. Competency check

A practitioner checkpoint is satisfied if the Web Manager can:

- explain why search/filter/sort/ranking are not synonyms;
- decide when search is unjustified;
- model query and retrieval state explicitly;
- diagnose stale-response and hidden-filter failures;
- distinguish zero results from system failure;
- define URL/history/privacy boundaries;
- preserve list/detail task continuity;
- specify accessible dynamic status behavior without indiscriminate focus movement;
- hand a state/task contract to Web Design without prematurely prescribing one visual layout.

**Checkpoint result: PASS at foundation/practitioner level.**

This does not establish production search quality, ranking relevance, browser/device parity or human usability. Those require implementation and user evidence.

---

# Highest-value next block

Proceed to **Responsive Web Interaction, Input Modality & Cross-Device Continuity**.

Reason: W003 now provides a Design Studio responsive recomposition model, while Web Manager Stage 3 has state/task/form/retrieval contracts. The next unresolved prerequisite is how those contracts survive touch, pointer, keyboard, hover/no-hover, coarse/fine pointer, virtual keyboard, orientation/viewport changes, zoom/reflow and cross-device/browser contexts without equating viewport width with input capability.
