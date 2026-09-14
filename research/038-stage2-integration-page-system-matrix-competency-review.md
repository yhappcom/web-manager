# 038 — Stage 2 Integration: Company/App/Support/Governance Page-System Matrix & Competency Review

Status: **STAGE 2 INTEGRATION GATE — PASS AT FOUNDATION/PRACTITIONER LEVEL**
Research date: 2026-09-15
Scope: public MintTap company/app website architecture under `minttap.app`, integrating Studies 034–037 without re-teaching them.

## Why this block exists

Studies 034–037 separately established:

- task-based website anatomy and ownership;
- canonical content objects and lifecycle;
- navigation/wayfinding/findability;
- page contracts, intra-page hierarchy and recovery states.

The remaining Stage 2 question is not whether each model is individually plausible. It is whether they remain coherent when a real visitor enters from an app store, search engine, shared deep link or stale URL and must complete a task without first understanding MintTap's internal organization.

This study therefore acts as a **system integration gate**.

It tests the chain:

`entry context → identity/orientation → destination promise → canonical content → task completion → escalation/recovery → lifecycle`.

A Stage 2 failure exists whenever one link breaks even if every individual page looks reasonable in isolation.

---

# 1. RELATED DOMAIN CHECK

## Web Manager evidence reused

- 034 — Website Anatomy, Task-Based IA & Content Ownership;
- 035 — Content Modeling, Hierarchy, Lifecycle & Cross-Channel Truth;
- 036 — Navigation, Wayfinding & Findability;
- 037 — Page Systems, Content Hierarchy & Scan/Comprehension Architecture.

This gate deliberately avoids re-describing those models. Repetition is used only where needed to validate an end-to-end scenario.

## Design Studio evidence checked

Latest Design Studio status checked 2026-09-15:

- Web Design remains Stage 1 Foundation / **NOT YET BASELINED** with no substantive `W###` evidence;
- Layout/Interaction remains Stage 1 Foundation / CRITIQUE in studied modules;
- Layout L002 rejects universal sparse/whitespace rules and treats density as task-dependent;
- current Layout/Interaction evidence explicitly requires real-browser multilingual, enlarged-text, keyboard/focus/status and failure/recovery validation before stronger claims.

Relevant files:

- `yhappcom/design-studio/progress/STATUS.md`;
- `yhappcom/design-studio/progress/WEB_STATUS.md`;
- `yhappcom/design-studio/progress/LAYOUT_STATUS.md`;
- `yhappcom/design-studio/research/layout/L002-whitespace-density-spatial-rhythm.md`.

### DEPENDENCY

This Stage 2 gate proves **information architecture and page-system coherence**, not final visual usability. Web Design must later validate the resulting contracts in complete responsive browser compositions. No Design Studio canonical file is edited by Web Manager.

---

# 2. SOURCE REVALIDATION — external store entry is an operational contract

## Apple

Current App Store Connect documentation states that:

- Support URL is a required platform-version property and may be localized;
- it points to the support website and must lead to actual contact information as required by applicable local law so users can reach the developer about app issues, feedback and feature requests;
- Privacy Policy URL is required for all apps;
- User Privacy Choices URL is optional and may point to public controls such as access, deletion or modification of user data.

Primary sources checked 2026-09-15:

- https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
- https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy

## Google Play

Current Google Play guidance states that if an app enables account creation, users must have:

- an in-app deletion path; and
- a web resource from which they can request account and associated-data deletion.

Google further states that the external resource must function, be relevant in scope, prominently expose the deletion pathway, and reference the app or developer name as shown on the Play listing. It must not require the user to reinstall the app merely to submit the request.

Primary sources checked 2026-09-15:

- https://support.google.com/googleplay/android-developer/answer/13327111
- https://support.google.com/googleplay/android-developer/answer/10144311

### SYNTHESIS

A store-linked web URL is not merely a navigation convenience. It is a **versioned external entry contract** whose destination must continue to identify the correct product, expose the promised task and remain operational after site restructuring.

This validates 034–037's use of direct-entry testing and lifecycle/redirect rules.

---

# 3. SOURCE REVALIDATION — structure must survive non-visual and constrained presentation

W3C/WAI current guidance establishes that meaningful page structure uses headings, page regions and relationships that can be programmatically determined. WCAG-related guidance also requires descriptive page titles/headings and meaningful navigation/focus order. Reflow guidance requires content at narrow equivalent viewport widths to remain available without loss of information or functionality except where two-dimensional presentation is essential.

Primary sources checked 2026-09-15:

- https://www.w3.org/WAI/tutorials/page-structure/
- https://www.w3.org/WAI/tutorials/page-structure/regions/
- https://www.w3.org/WAI/tips/writing/
- https://www.w3.org/WAI/standards-guidelines/wcag/new-in-21/#1410-reflow-aa

### SYNTHESIS

Stage 2 architecture cannot depend on desktop geometry alone. A task path fails structurally if app identity, prerequisites, action or recovery disappear or become ambiguously reordered under narrow width, text enlargement, keyboard navigation or assistive-technology structure.

---

# 4. INTEGRATED PAGE-SYSTEM MATRIX

The matrix below is the minimum structural contract for a multi-app company website. It is deliberately semantic rather than visual.

| Page system | Typical external/internal entry | Identity/orientation requirement | Primary task | Canonical content objects | Required onward/recovery paths | Lifecycle trigger |
| --- | --- | --- | --- | --- | --- | --- |
| Company / portfolio | direct domain, search, shared link | MintTap/company identity and current portfolio scope | understand developer / select app | Company, App summaries | app detail, support, governance | app launch/retirement, company identity change |
| App detail | store marketing URL, search, portfolio, shared link | app name + MintTap/developer context | evaluate app / reach correct store | App, Feature, Claim, Store Destination | support, privacy, platform action | release, pricing, availability, claim change |
| Support hub | Apple Support URL, app, search | app context or clear app selector | locate help | Support Topic, escalation/contact | article, app, contact/escalation | feature/support/contact change |
| Support article | search, shared link, support hub | app + task/problem identity | resolve problem | Support Article, scope, version/platform conditions | related help, escalation, app context | behavior/version/process change |
| Privacy / policy | store privacy URL, footer, search | responsible entity + app/service scope | understand policy | Policy Document, scope/version/effective date | privacy choices/contact where applicable | data practice, legal/entity, market change |
| Account control / deletion | Play listing, app, privacy, search | app/service identity before destructive action | request/complete account-data action | Account-Control Procedure, retention exceptions | confirmation, support/escalation, privacy | account/auth/data-retention flow change |
| Release / known issue | direct shared/search link, support/app | app + affected version/status | determine current behavior/status | Release Change, Known Issue | workaround/support/app | release, issue resolution/status change |
| Error / retired / unavailable | stale link, bad route, removed content | explain what resource/state failed | recover without losing context | retirement/replacement metadata | replacement, parent context, support | URL/content retirement or service state |

### MINTTAP DECISION

Treat this matrix as a **pre-design content/navigation contract**, not as a mandatory menu layout or one-template page system.

---

# 5. SCENARIO GATE A — App Store / Google Play / search → app detail → support/privacy

## Expected chain

`external listing/search → correct app identity → app detail → relevant support/privacy task`.

### PASS conditions

1. The destination identifies the app without requiring homepage context.
2. Store-derived claims remain materially consistent with canonical product truth.
3. Support and privacy links retain app/service scope where scope differs by product.
4. Platform/store actions do not silently route to an unavailable or different product.
5. A visitor can move from app evaluation to support/governance without returning to the homepage.
6. Renaming or restructuring preserves old store-linked URLs through deliberate migration/redirect behavior.

### Counterexample

A Support URL lands on `/` with a generic “Contact us” link and no app context.

The site may technically contain support information, but the **external-entry contract fails** because the user must reconstruct product context.

### RESULT

**PASS as an architectural model.** Production validation remains dependent on actual MintTap store URLs and app inventory.

---

# 6. SCENARIO GATE B — direct support article → resolution → escalation

## Expected chain

`search/shared deep link → app/task identity → scope/conditions → resolution → failure branch → escalation`.

### PASS conditions

1. H1/page title makes the task/problem recognizable out of context.
2. App identity and platform/version scope appear before instructions when material.
3. Required prerequisites appear before the action that depends on them.
4. Failure/exception branches are not hidden behind unrelated marketing content.
5. Escalation remains reachable if self-service fails.
6. Related links preserve the same app/support context.

### Failure diagnosis

If instructions are correct but the user cannot tell which app/version they apply to, the failure is **scope/identity**, not article prose.

If the article resolves the common case but offers no path when it fails, the failure is **support-system recovery**, not navigation depth.

### RESULT

**PASS as an integrated contract.** Human comprehension/usability evidence remains OPEN.

---

# 7. SCENARIO GATE C — privacy / account-control direct entry

## Expected chain

`store/search/app → correct policy/control scope → user understands consequences → action/request → confirmation/recovery`.

### PASS conditions

1. Direct entry identifies the responsible app/service and operator scope.
2. Privacy policy and account-control procedure are distinct objects even when cross-linked.
3. Destructive or consequential action is not disguised as a generic navigation item.
4. Google Play deletion-resource conditions can be satisfied without requiring app reinstallation where the account-deletion requirement applies.
5. Any retained-data exception is sourced from actual policy/legal requirements, not invented by web copy.
6. Completion and failure states provide clear next steps.

### OPEN

Whether any current MintTap app creates user accounts is unknown. Therefore no app-specific deletion URL structure is finalized in this study.

### RESULT

**PASS conditionally.** The architecture supports the requirement; applicability is project-specific.

---

# 8. SCENARIO GATE D — release / known-issue direct entry

## Expected chain

`search/shared/support link → app identity → affected version/status → current evidence → workaround/action → resolution state`.

### PASS conditions

- known issue and release note are separate content objects;
- status and affected scope are explicit;
- resolved content is not silently deleted if existing links have ongoing value;
- retirement routes to a replacement, resolution note or durable parent context;
- support escalation remains available when the workaround fails.

### SYNTHESIS

A known-issue page is operational content, not a blog post. Its usefulness depends on status/scope freshness and lifecycle, not publication date alone.

### RESULT

**PASS.** Actual publication thresholds remain OPEN until MintTap support volume and incident model are known.

---

# 9. SCENARIO GATE E — missing, retired, unavailable or no-result resource

These states must not collapse into one generic error template.

## Required distinctions

- **404 / unknown URL** — resource not found;
- **retired** — resource existed but is intentionally withdrawn or replaced;
- **temporarily unavailable** — task/resource is expected to return;
- **unsupported** — request/context is understood but not supported;
- **empty** — valid destination currently has no items;
- **no result** — retrieval/search completed but found no match.

### PASS conditions

Each state answers, where applicable:

1. What happened?
2. Is the user's data/action safe or unchanged?
3. Is the condition temporary, permanent or unknown?
4. What can the user do next?
5. Can app/task context be preserved rather than dumping the user at home?

### RESULT

**PASS.** 037's differentiated state model integrates cleanly with 034 ownership/lifecycle and 036 recovery/findability.

---

# 10. SCENARIO GATE F — Korean/English + narrow width + enlarged text/reflow

This is an architecture stress test, not a visual-polish test.

### Required invariants

Across language expansion and constrained presentation:

- app/service identity remains available;
- page purpose and H1 remain understandable;
- prerequisite information remains before dependent action where sequence matters;
- navigation labels do not become vague merely to fit;
- destructive/governance actions remain distinguishable;
- repeated navigation can still be bypassed/understood structurally;
- visual reorder must not produce a contradictory DOM/focus/reading sequence;
- information needed for comparison is not hidden solely to make a mobile composition appear sparse.

### Design Studio transfer

L002 supports the last point: density is task-dependent, and more whitespace is not a universal performance improvement. Web Design must test real text, wrapping, zoom/reflow and browser behavior instead of satisfying this gate with rectangle wireframes.

### RESULT

**PASS as semantic requirements; NOT a production UI pass.** Real browser/device/human validation remains a Design Studio/Web implementation dependency.

---

# 11. DIRECT-ENTRY COMPETENCY TEST

Every critical public destination should be testable with the homepage removed from the user's history.

For a direct URL opened in a fresh context, the reviewer should be able to answer:

1. Which company/app/service is this?
2. What is this page for?
3. What scope/version/platform does it apply to, if material?
4. What must I know before acting?
5. What is the primary action or resolution?
6. What happens if the action does not work?
7. Where can I move next without losing context?

### PASS rule

A critical destination does not pass merely because all seven answers exist somewhere on the site. The answers must be discoverable **from the destination and its immediate structural context**.

---

# 12. HEADING / LANDMARK / MEANINGFUL-ORDER GATE

For each critical destination, validate independently:

- document/page title;
- H1/page promise;
- heading-only outline;
- main/navigation/other relevant regions;
- repeated-navigation bypass mechanism where implemented;
- link purpose;
- DOM/reading sequence;
- keyboard focus sequence when interactive controls exist.

### SYNTHESIS

Visual hierarchy may reinforce this structure but cannot substitute for it. Conversely, semantically valid headings do not prove that visual priority or human comprehension is good. These are separate evidence layers.

---

# 13. END-TO-END FAILURE TAXONOMY

An integrated Stage 2 failure should now be classified before redesign:

1. **entry-contract failure** — store/search/shared link lands in wrong or insufficient context;
2. **identity/scope failure** — user cannot determine app/service/version applicability;
3. **truth failure** — public surfaces conflict materially;
4. **destination failure** — task has no stable destination;
5. **label/scent failure** — path exists but destination cannot be predicted;
6. **hierarchy/sequence failure** — prerequisite, evidence or action order is misleading;
7. **recovery failure** — task breaks and context/escalation is lost;
8. **lifecycle failure** — stale/retired content remains authoritative or links break after change;
9. **localization/reflow failure** — meaning is shortened, hidden or reordered under constrained presentation;
10. **semantic-exposure failure** — headings/regions/order/focus do not preserve intended structure.

This taxonomy prevents one class of problem from being cosmetically patched as another.

---

# 14. STAGE 2 COMPETENCY REVIEW

The Web Manager should now be able to do the following without beginning with a visual mockup:

- derive public destinations from real user/store/support/governance tasks;
- distinguish content objects from pages/components/channel fields;
- preserve app/service scope across external deep links;
- identify canonical truth and lifecycle ownership;
- separate global, local, utility and direct-entry navigation responsibilities;
- define Page Contracts by task and context;
- distinguish browsing hierarchy from visit history;
- classify findability and comprehension failures before changing layout;
- design recovery contracts for retired/error/unavailable/no-result states;
- specify structural invariants for localization, narrow widths and enlarged text;
- hand Design Studio semantic/behavioral requirements without dictating unsupported visual solutions.

### COMPETENCY RESULT

**PASS — Stage 2 Foundation/Practitioner integration gate satisfied.**

No unresolved prerequisite was found that requires another Stage 2 foundation block before progressing to Stage 3 UX & Interaction Foundations.

This does **not** mean Stage 2 is complete at advanced/expert depth. It should reopen later when real MintTap audience evidence, analytics, content volume, search behavior, localization, support operations and production browser testing exist.

---

# 15. MINTTAP PROJECT HANDOFF PACKAGE

Before future website design begins, Web Manager should supply Design Studio/Web Design with:

1. audience/context → task → destination matrix;
2. app/company/support/governance scope boundaries;
3. canonical content objects and truth owners;
4. external store/search/shared-link entry contracts;
5. global/local/utility navigation responsibilities;
6. critical-destination direct-entry tests;
7. Page Contracts including prerequisite/action/recovery relationships;
8. heading/region/meaningful-order requirements;
9. disclosure and simultaneous-comparison constraints;
10. Korean/English long-string and stale-translation cases;
11. narrow-width + enlarged-text/reflow cases;
12. differentiated error/retired/unavailable/unsupported/empty/no-result states;
13. DOM/visual/focus/accessibility-order validation requirements;
14. content owner/change-trigger/retirement metadata.

Design Studio should return any structural contradiction to Web Manager rather than solving it silently through visual styling.

---

# 16. OPEN QUESTIONS — deliberately not invented

Real MintTap implementation still requires verified answers for:

- current app inventory and launch order;
- actual Apple/Google store-linked URLs;
- which apps create accounts;
- company/legal/developer identity exposed in each market;
- support escalation channels and operating owner;
- supported languages/markets;
- actual acquisition sources and user task frequencies;
- pricing/subscription/account models;
- real content volume and whether site search is justified;
- framework/hosting/runtime constraints;
- human usability/comprehension results.

These are inputs to a project instance of the architecture, not reasons to delay the curriculum.

---

# 17. CHANGE WATCH

Re-check before production or store submission:

- Apple App Store Connect Support/Privacy URL requirements;
- Google Play User Data/account-deletion requirements;
- WCAG/WAI normative/current implementation guidance relevant to the target conformance level;
- actual Design Studio Web evidence once `W###` studies and browser validations exist.

---

# 18. NEXT CURRICULUM MOVE

Advance to **Stage 3 — UX & Interaction Foundations**.

The first Stage 3 block should start from first principles rather than UI-pattern catalogues:

`user goal → action possibility/affordance → system state → feedback → error/prevention/recovery → continuity across interruption`.

Highest-value early topics include:

- usability and interaction as task-state systems;
- affordance/signifier/constraint/feedback distinctions;
- state, mode, visibility and system-status communication;
- errors, validation, prevention, reversibility and recovery;
- forms and consequential actions;
- interruption, pending/async states and continuity;
- mouse/touch/keyboard/mixed-input equivalence;
- applying, not duplicating, Design Studio Interaction evidence.

The boundary is explicit: Stage 3 should study user action and state transitions. It should not reopen Stage 2 merely to redesign page layouts.