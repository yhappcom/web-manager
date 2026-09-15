# 058 — Stage 5 Integration: Accessibility Conformance, Complete-Process Evidence & App-Company Competency Review

Date: 2026-09-16  
Stage: 5 — Accessibility  
Gate target: FOUNDATION / PRACTITIONER INTEGRATION

## Purpose

Integrate 051–057 into one operational accessibility model for an Apple/Android app company website. This is not a new checklist and does not claim that `minttap.app` currently conforms to WCAG. The question is whether the Web Manager now has a coherent method to scope, diagnose, specify, validate and accurately report accessibility across Company, Product, Support and Governance/account-control work.

Integrated model:

`user goal → functional need/barrier → page/process scope → semantic exposure → operability/focus → transaction/recovery → dynamic application state → adaptation/user preference → media equivalence → accessibility-supported implementation → complete-process evidence → bounded conformance statement → lifecycle regression control`

---

## 1. SOURCE — conformance is broader than passing individual success criteria

WCAG 2.2 is the normative baseline used in this stage. Its five conformance requirements are: conformance level, full pages, complete processes, only accessibility-supported ways of using technologies, and non-interference. A responsive page's automatically presented variations are included in the full-page requirement. If a page belongs to a sequence required to accomplish an activity, all pages in that complete process must conform at the claimed level.

Primary source checked 2026-09-16:
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Understanding Conformance: https://www.w3.org/WAI/WCAG22/Understanding/conformance

### SYNTHESIS

`criterion pass != component conformance != page conformance != process conformance != site-wide claim`.

The seven Stage 5 contracts therefore cannot be treated as independent checklists. They are evidence lenses that converge on the same page/process scope.

### FAILURE MODE

A product page with valid headings, keyboard-operable controls and good contrast can still fail a claimed complete process if its linked account-deletion confirmation step is inaccessible. Likewise, an accessible desktop variation does not rescue a nonconforming automatically presented narrow responsive variation.

---

## 2. SOURCE — current evaluation methodology supports scoped, representative evaluation but does not replace WCAG

W3C published WCAG Evaluation Methodology (WCAG-EM) 2.0 as a Group Note on 2026-07-23. It now applies to digital products, including websites and mobile applications. Its process is: define evaluation scope, explore the product, select a representative sample, evaluate that sample, and report findings. It explicitly does not add to or replace WCAG requirements and does not replace accessibility quality assurance throughout development.

Primary sources checked 2026-09-16:
- W3C WCAG-EM 2.0: https://www.w3.org/TR/wcag-em-2/
- W3C WCAG-EM Overview: https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/

### SYNTHESIS

Representative sampling is an evaluation strategy, not permission to ignore known variants, states or complete-process steps. Sampling must be informed by product exploration: templates, key functionality, content types, states, technologies and processes.

For MintTap this means page-family sampling should deliberately cover structurally different risk surfaces rather than simply choosing a few URLs.

---

## 3. Integrated page/process-family model

### Company / Home

Primary accessibility risks are orientation, hierarchy, navigation, product identification, responsive adaptation, non-text meaning and any animated/promotional media. Apply 051 barrier mapping, 052 semantics, 053 operability, 056 adaptation and 057 media where present. If navigation or disclosures are dynamic, add 055.

Evidence question: can users with different input, vision, hearing and cognitive needs understand what MintTap is, identify available products and reach the intended next destination without losing meaning or control?

### Product / App

Product pages combine information architecture with product evidence. Apply all relevant semantic, focus, responsive, media and state contracts, while preserving 048/057 provenance truth between website claims, screenshots/video and shipped app behavior.

Evidence question: can the user understand the app's purpose/features and follow the intended store/support/privacy path without an inaccessible representation or interaction becoming the only usable route?

### Support

Support is a retrieval and recovery environment. Search, filters, disclosures, dynamic results, forms, errors and status messages may combine. Apply 052–056 together; 057 applies to tutorial media.

Evidence question: can a user find, understand and complete a recovery/support task, including no-results, invalid input, pending/failure and success states, without relying on pointer-only, color-only, visual-only or transient-only information?

### Governance / Account control

This is the highest complete-process risk family because privacy choices, account deletion, authentication, verification and consequential changes can span several steps and possibly third-party boundaries. Apply 052 semantics, 053 focus/input, 054 transaction/authentication/error prevention, 055 dialogs/status/state and 056 timing/re-authentication continuity as one process contract.

Evidence question: can the user enter the process, authenticate using an accessible path, understand consequences, correct mistakes, complete/cancel the action and receive durable confirmation without accessibility failure at any required step?

### SYNTHESIS

The correct accessibility unit is selected by the user's required activity, not by repository component boundaries. A reusable component can be individually sound yet participate in an inaccessible process because focus destination, status exposure, timing, content relationship or recovery is wrong at integration level.

---

## 4. Seven contracts now form one evidence system

1. **Accessibility Evidence Contract (051)** owns scope, barriers, evidence classes and claim boundaries.
2. **Semantic Accessibility Contract (052)** owns role/name/description/state/property and native-vs-ARIA decisions.
3. **Operability / Focus Contract (053)** owns keyboard/pointer paths, focus movement/visibility/restoration and modality-independent task access.
4. **Accessible Transaction Contract (054)** owns labels/instructions, errors, async status, authentication, redundant entry, consequential-action safeguards and completion.
5. **Accessible Application-State Contract (055)** owns synchronization of visible, semantic, focus, selection/active and announcement state in dynamic UI.
6. **Adaptation / User-Preference Accessibility Contract (056)** owns enlargement, zoom/reflow, text-spacing, orientation, motion, timing and preference resilience.
7. **Product-Demo Media Accessibility Contract (057)** owns media classification, captions/description/equivalence, player operability and product-media provenance.

### SYNTHESIS — contract composition rule

Contracts are additive where the same task crosses domains. They must not produce contradictory ownership. Example: a modal account-deletion confirmation uses 052 for semantics, 053 for focus/keyboard, 054 for consequential-action safeguards, 055 for modal state and return focus, and 056 if session expiry or motion is involved. The test object is still one task state machine.

---

## 5. Evidence ladder and claim discipline

A defensible MintTap accessibility evaluation should distinguish:

`source/code/static inspection → automated rules → browser/manual interaction → computed accessibility representation → keyboard/pointer/user-preference stress → representative AT/device execution → complete-process execution → disability-informed human evaluation → scoped conformance reporting`

### SOURCE

W3C ACT Rules are informative test rules, not the normative basis for WCAG conformance. WCAG-EM recommends a structured evaluation process and recommends involving users with disabilities to address real-life experience.

Primary sources:
- https://www.w3.org/WAI/standards-guidelines/act/rules/about/
- https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/

### SYNTHESIS

Automation is useful for repeatable detectable failures and regression gates; it cannot prove semantic appropriateness, task comprehensibility, caption quality, useful focus placement or real-world usability. Conversely, a successful human task trial does not by itself establish every normative WCAG criterion.

### MINTTAP DIRECTION

Use two parallel statements in real work:
- **conformance evidence** — criterion/scope-specific technical evidence;
- **experience evidence** — whether people can actually understand and complete the intended task.

Do not collapse them into one score.

---

## 6. Accessibility-supported technology and support matrix

### SOURCE

WCAG conformance requires that only accessibility-supported ways of using technologies are relied upon to satisfy success criteria. Accessibility support depends on user-agent and assistive-technology support rather than syntax alone.

### SYNTHESIS

A source-correct ARIA pattern is not automatically a production-supported pattern. A real project needs a declared browser/OS/AT/input support matrix tied to actual users and product policy, then representative execution against that matrix.

### OPEN

The actual `minttap.app` frontend stack, browser support policy, AT matrix, native/custom controls and third-party widgets are unknown. Production accessibility support cannot be inferred from Design Studio exercises or generic standards compatibility.

---

## 7. Conformance reporting is a scoped claim, not a marketing adjective

### SOURCE

WCAG 2.2 conformance claims are optional. If made, the standard specifies required claim components including date, WCAG version/URI, level and concise description of the pages covered.

### SYNTHESIS

Avoid unbounded phrases such as “MintTap is WCAG compliant” unless scope and evidence actually justify them. Prefer explicit statements of target, evaluated scope, date, known limitations and feedback route when a real evaluation exists.

WCAG-EM 2.0 is useful for organizing an evaluation/report but is a supporting Group Note, not a replacement normative standard.

### CHANGE WATCH

WCAG 3.0 is under development and must not be represented as the current stable replacement for WCAG 2.2. Recheck standards status before future formal claims.

---

## 8. Lifecycle and regression governance

Accessibility is invalidated by ordinary product change: new components, altered responsive breakpoints, authentication changes, third-party embeds, copy/localization growth, app-demo replacement, router/dialog behavior, design-token changes and new motion.

### MINTTAP DIRECTION

For each release affecting web UI/content, classify changes against the seven contracts and decide the minimum regression evidence required. High-risk changes include:
- new custom interactive controls;
- authentication/account/deletion process changes;
- modal/composite/dynamic-state changes;
- responsive shell/navigation changes;
- session/OTP timing changes;
- media/player/provider changes;
- third-party widgets required for a task.

Accessibility review belongs in definition/design/development/release, not only pre-launch audit. WCAG-EM itself explicitly says evaluation does not replace lifecycle QA.

---

## 9. Design Studio dependencies / handoffs

Latest `progress/WEB_STATUS.md` checked 2026-09-16: Web Design Stage 1 PASS / Stage 2 PRACTICE, NOT PASSED. W014 establishes the source-grounded native-vs-custom button contract but runtime execution remains open. W006 integrated task-state runtime, W011 icon runtime, actual browser-UI zoom, true HTTP direct-entry/reload and broader browser/device/AT/human evidence remain open.

### Web Design

For live MintTap work, execute representative integrated slices rather than isolated visual components: navigation + disclosure/composite + form/error/status + modal + responsive/zoom state where applicable. Preserve computed semantics, keyboard/focus behavior and state synchronization evidence. Do not promote W012/W013 exercise evidence into MintTap production evidence.

### Layout / Interaction

Receive complete task/state models and adaptation invariants. Validate focus destinations, modal/background behavior, responsive state migration and recovery paths as interaction architecture, not only layout.

### Type

Receive actual KO/EN/mixed production strings. Validate enlargement, spacing, wrapping, error/status text and media captions in shipped contexts.

### Color

Receive semantic state inventory. Validate focus/control/text/non-text contrast and forced/user-environment behavior without using color as the sole state channel.

### Web Manager retains

Evaluation scope, WCAG level classification, complete-process boundaries, accessibility-supported technology assumptions, cross-contract integration, product/support/governance task inventory, evidence sufficiency, conformance-claim wording and lifecycle governance.

No Design Studio canonical file is edited by Web Manager.

---

## 10. OPEN — real MintTap evidence still required

Stage 5 learning completion does **not** establish production accessibility. Still unknown/unvalidated:
- actual page/process/component inventory and source implementation;
- supported browser/OS/AT/input matrix;
- computed accessibility tree and native/custom-control behavior;
- keyboard, touch, speech-input and screen-magnifier task execution;
- 200% text enlargement, actual browser zoom, 320 CSS-px-equivalent reflow and spacing overrides;
- forms, errors, live status, dialogs/composites, authentication/MFA/session/OTP/deletion complete processes;
- third-party process boundaries;
- real media/player/caption/description inventory;
- KO/EN production content stress;
- disability-informed human evaluation;
- jurisdiction-specific legal obligations and accessibility statement/feedback ownership.

These must remain OPEN until evidence exists.

---

## 11. Stage 5 competency gate

Foundation/Practitioner competency requires the Web Manager to be able to:
- start from disability-related functional barriers rather than checklist order;
- distinguish normative WCAG requirements from techniques, APG patterns, ACT rules and evaluation methodology;
- scope full pages, responsive variations and complete processes correctly;
- diagnose semantic, operability, transaction, dynamic-state, adaptation and media failures as interacting systems;
- prefer native semantics and understand the reconstruction burden of custom controls;
- distinguish automated, browser, AT/device, process and human evidence;
- define accessibility-supported technology assumptions rather than assuming source syntax proves support;
- construct a representative evaluation plan across Company, Product, Support and Governance/account-control families;
- report evidence and limitations without overstating conformance;
- route design execution to the appropriate Design Studio specialist while retaining scope and evidence governance;
- preserve accessibility through release/regression lifecycle.

**Result: PASS — Stage 5 Accessibility Foundation/Practitioner integration gate.**

No missing prerequisite requires extending Stage 5 before curriculum progression. Advanced accessibility remains intentionally reopenable later for production audits, legal jurisdiction analysis, detailed AT matrices and expert remediation.

## Next

Proceed to **Stage 6 — Search / Discovery / Content Quality**. Highest-value opening block: **059 — Search & Discovery Foundations: Crawling, Indexing, Rendering, Canonicalization and App-Company Findability**. Start from how search engines discover and represent web resources before studying keyword tactics, structured data or growth optimization.