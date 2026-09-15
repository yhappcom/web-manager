# 051 — Accessibility Foundations: Disability, Barriers, Standards, Conformance & App-Company Web Responsibility

Date: 2026-09-15  
Stage: 5 — Accessibility  
Checkpoint: FOUNDATION/PRACTITIONER PASS

## Why this block exists

Accessibility must begin with people, functional needs and barriers rather than a mechanical WCAG checklist. This block establishes the mental model needed before studying individual implementation domains.

## 1. SOURCE — accessibility is about barriers across diverse abilities

W3C WAI's current Diverse Abilities and Barriers guidance emphasizes diversity across auditory, cognitive/learning, physical, speech and visual abilities, and also age-related, multiple, changing, temporary and situational limitations. It explicitly recommends considering broad functional needs rather than relying only on medical categories.

Primary source: https://www.w3.org/WAI/people-use-web/abilities-barriers/ (updated 2024-06-25; checked 2026-09-15).

### SYNTHESIS

The useful unit for Web Manager diagnosis is not `disability label → special version`; it is:

`user goal → functional need → environment/tool → encountered barrier → consequence → accessible path → validation`.

A barrier is relational: a design/implementation assumption becomes disabling when it conflicts with a person's way of perceiving, understanding or operating the interface.

Examples:
- icon-only control + no accessible name → meaning may be unavailable to non-visual interaction;
- pointer-only interaction → task unavailable to keyboard/switch users;
- color-only error indication → state unavailable where color distinction is insufficient;
- rigid zoom/reflow → low-vision enlargement can destroy task continuity;
- complex/unpredictable instructions → cognitive burden can prevent task completion;
- unlabeled media → information unavailable through another sensory channel.

Do not infer that one technique serves every person within a disability category.

## 2. SOURCE — accessibility, usability and inclusion overlap but are not synonyms

WAI distinguishes accessibility (equal perception, understanding, navigation, interaction and contribution for people with disabilities), usability (effectiveness, efficiency and satisfaction), and broader inclusion. WAI also warns that general usability work may fail to address disability-specific needs.

Primary source: https://www.w3.org/WAI/fundamentals/accessibility-usability-inclusion/ (checked 2026-09-15).

### SYNTHESIS

Passing a general usability test does not prove accessibility. Passing technical accessibility checks does not prove efficient or satisfying use. The Web Manager therefore needs separate evidence ledgers for:

1. normative conformance evidence;
2. implementation/browser/AT behavior;
3. human task accessibility/usability evidence.

These may support each other but cannot be substituted for one another.

## 3. SOURCE — accessibility is a system, not only page markup

WAI's Accessibility Principles explains that accessible web use depends on interacting components including web content, user agents, assistive technologies and authoring tools. Different input modalities and assistive technologies change how content is perceived and operated.

Primary source: https://www.w3.org/WAI/fundamentals/accessibility-principles/ (checked 2026-09-15).

### SYNTHESIS

A correct DOM pattern is necessary in many cases but does not by itself establish production accessibility. The evidence chain is:

`author semantics/behavior → browser accessibility model → user agent/AT support → user configuration/input modality → actual task outcome`.

This explains why earlier Web Manager studies correctly kept browser/device/AT/human proof OPEN even after structural review.

## 4. SOURCE — WCAG 2.2 structure and normative status

WCAG 2.2 is a W3C Recommendation. W3C advises use of WCAG 2.2 to maximize future applicability. Its success criteria are organized under four principles: Perceivable, Operable, Understandable and Robust, with A, AA and AAA conformance levels.

Primary normative source: https://www.w3.org/TR/WCAG22/ (checked 2026-09-15).

### Important standards literacy

WCAG's normative success criteria and conformance requirements determine conformance. Understanding documents, Techniques, examples and notes are informative unless the normative specification says otherwise.

**MINTTAP DIRECTION:** use WCAG 2.2 as the current technical baseline for new `minttap.app` web work unless a verified jurisdiction/client requirement specifies another target. This is a project engineering baseline, not a legal conclusion.

**CHANGE WATCH:** WCAG 3 remains a Working Draft, not a replacement conformance standard for MintTap production claims at this time.

## 5. SOURCE — conformance is stronger than “we checked some criteria”

WCAG 2.2 section 5 establishes five conformance requirements:

1. a conformance level is met in full;
2. conformance applies to full pages;
3. all pages in a complete process must conform at the claimed level;
4. only accessibility-supported ways of using technologies may be relied on;
5. non-accessibility-supported/non-conforming technology must not interfere with the rest of the page.

A responsive page's automatically presented screen-size variations are included in the full-page requirement. Conformance claims are optional, but if made they have required components including date, WCAG version/URI, level, scope and relied-upon technologies.

Primary sources:
- https://www.w3.org/TR/WCAG22/#conformance
- https://www.w3.org/WAI/WCAG22/Understanding/conformance

### SYNTHESIS — conformance scope is architectural

For an app-company website, accessibility cannot be certified by polishing a landing-page hero while excluding the support form, privacy/account-control flow, responsive variant or other required step in the same process.

This directly connects Stage 3's complete-task model to Stage 5:

`accessible control ≠ accessible page ≠ accessible process ≠ accessible product experience`.

A complete process such as an account-control request must be evaluated from entry through completion/recovery, not only at the first page.

## 6. Accessibility responsibility for an Apple/Android app company

### SYNTHESIS

The website has multiple accessibility responsibilities even when the native app is a separate product:

- **Company/discovery:** product identity, navigation and app-store path must remain perceivable and operable.
- **Product evidence:** screenshots, demos and claims need meaningful alternatives/context where necessary; imagery cannot become the only carrier of essential product information.
- **Support:** instructions, search/retrieval, contact/escalation and forms must support varied perception/input/cognition.
- **Governance/account control:** privacy, deletion or other consequential controls require accessible complete processes and clear error/recovery behavior.
- **Cross-channel continuity:** the web must not create an accessibility dead end between website, store and app-support surfaces.

These are operational responsibilities inferred from web task architecture plus WCAG's full-page/complete-process model. They do not assert that every native-app requirement is governed by WCAG in every jurisdiction.

## 7. Barrier map — reusable foundation

| Functional dimension | Common web barrier mechanism | Typical task consequence | Evidence needed |
| --- | --- | --- | --- |
| visual perception | low contrast, color-only meaning, clipped zoom/reflow, inaccessible imagery | information/state unavailable | computed/manual checks + browser/user-mode validation |
| auditory perception | audio-only information, missing captions/transcript | content unavailable | media alternative review + playback validation |
| motor/dexterity | keyboard trap, pointer/drag dependence, small targets, timing | action impossible/error-prone | keyboard/pointer/input execution |
| speech/input modality | visible label differs from programmatic name | voice activation ambiguity/failure | accessible-name/visible-label inspection + AT/input validation |
| cognitive/learning | unpredictable changes, unclear instructions/errors, excessive complexity | orientation/completion failure | structural review + human task evidence |
| non-visual navigation | weak semantics/name-role-state/focus order | structure/action/state unavailable | accessibility-tree/keyboard/AT execution |
| photosensitivity/vestibular | flashing or unavoidable motion | physical harm/disorientation | content/runtime review + user preference behavior |

This table is a diagnostic map, not a substitute for WCAG success-criterion evaluation.

## 8. SOURCE — automated tools cannot determine accessibility

W3C WAI states that evaluation tools can quickly identify potential issues and automate some checks, but cannot check all accessibility aspects; human judgment is required and tools can produce false or misleading results. WAI explicitly states that tools cannot determine accessibility by themselves.

Primary sources:
- https://www.w3.org/WAI/test-evaluate/tools/selecting/
- https://www.w3.org/WAI/test-evaluate/

ACT Rules are informative testing rules and are not themselves required for WCAG/ARIA conformance.

Primary source: https://www.w3.org/WAI/standards-guidelines/act/rules/

### MINTTAP DIRECTION — evidence ladder

Do not report `automated scan passed` as `accessible` or `WCAG conformant`.

Use an evidence ladder:

`static/automated detection → manual structural review → keyboard/input execution → browser/accessibility-tree inspection → representative AT execution → responsive/user-preference execution → complete-process evaluation → human disability-informed evaluation`.

Not every release requires every possible AT/device combination, but the selected matrix and residual uncertainty must be explicit.

## 9. Evaluation lifecycle

WAI recommends evaluating accessibility early and throughout design/development rather than leaving it to a final audit. WCAG-EM provides a methodology for conformance evaluation and can apply to websites, mobile applications and kiosks, but accessibility should be integrated throughout the lifecycle.

Primary sources:
- https://www.w3.org/WAI/test-evaluate/
- https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/

### SYNTHESIS

MintTap's correct lifecycle is:

`requirements/task modeling → semantic/content/design contracts → implementation → continuous automated/manual checks → runtime/AT validation → representative process audit → release evidence → feedback/remediation`.

Accessibility defects discovered in production should feed back into reusable component/content contracts rather than be patched only on one page.

## 10. Accessibility Evidence Contract

For each important MintTap web page/process, record:

1. page/process identity and user goal;
2. accessibility scope and intended conformance baseline;
3. functional needs/barriers considered;
4. content/semantic requirements;
5. keyboard/input/focus requirements;
6. visual/non-text/media requirements;
7. responsive/zoom/user-preference requirements;
8. status/error/recovery requirements;
9. technologies relied upon;
10. automated/static evidence;
11. manual browser evidence;
12. AT/input/device evidence;
13. complete-process evidence;
14. human-evaluation evidence, if available;
15. known exceptions/open risks;
16. owner, date/build and retest trigger;
17. whether any public conformance/accessibility statement is authorized.

This contract prevents `checklist PASS` from being promoted into a stronger claim than the evidence supports.

## 11. Design Studio dependencies / handoffs

Latest Web Design specialist status checked 2026-09-15: Stage 1 PASS; Stage 2 PRACTICE / NOT PASSED. W012/W013 provide Chromium responsive/navigation runtime transfer, while native/custom control semantics, integrated task-state execution, icon runtime, broader browser/device/AT and human evidence remain OPEN.

### Outgoing handoff

- **Web Design:** execute semantics/focus/keyboard/state behavior in actual components and page processes; preserve the difference between visual behavior and accessibility-tree/interaction behavior.
- **Layout/Interaction:** map complete-task state transitions, focus restoration, error/recovery and alternative input paths.
- **Type:** validate reading/wrapping under zoom, text spacing, fallback and actual KO/EN content; typography hierarchy must not be the sole structural carrier.
- **Color:** validate text/non-text contrast and ensure required meaning survives non-color/user-color environments.

Web Manager owns accessibility scope, page/process requirements, evidence claims, cross-channel task continuity and release/governance boundaries. Specialist PASS statuses must not be interpreted as MintTap production accessibility evidence.

## 12. OPEN questions — deliberately unresolved

- actual MintTap page/process inventory and which surfaces will exist at launch;
- target conformance level required by company policy or applicable law;
- jurisdictions and legal accessibility obligations;
- target browser/OS/AT/input support matrix;
- real frontend/component implementation and third-party widgets;
- actual media, support, account/deletion and privacy-control flows;
- whether native apps will receive a coordinated accessibility program and which standards/legal regimes govern them;
- disability-informed human evaluation participants and release cadence;
- public accessibility statement/feedback channel ownership.

These require project or legal/operational evidence; they are not inferred here.

## 13. Competency check

PASS at Foundation/Practitioner level if Web Manager can:

- explain accessibility through functional needs and barriers rather than disability stereotypes;
- distinguish accessibility, usability and inclusion;
- explain WCAG principles, success criteria, levels and normative/informative material;
- explain all five WCAG 2.2 conformance requirements and why responsive variants/complete processes matter;
- distinguish automated findings, technical conformance evidence, AT behavior and human task accessibility;
- diagnose barriers across semantics, input, focus, visual presentation, non-text content, cognition and responsive behavior;
- scope an app-company web accessibility review without claiming facts about MintTap that are not verified;
- create an Accessibility Evidence Contract and hand implementation-specific work to Design Studio without treating specialist exercises as production proof.

**Result: PASS.**

## Next highest-value block

052 — **Semantic Structure, Native HTML, Accessible Names/Roles/States & ARIA Boundary**.

Reason: after establishing people/barriers/conformance, the next prerequisite is understanding how authored HTML becomes programmatic structure and controls for browsers/assistive technologies, why native semantics are the baseline, when ARIA is needed, and how misuse creates accessibility failures. This should connect directly to Design Studio Web W005/W011 runtime gaps rather than duplicate generic HTML study.
