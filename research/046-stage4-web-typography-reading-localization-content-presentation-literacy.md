# 046 — Stage 4: Web Typography, Reading, Localization & Content Presentation Literacy

Date: 2026-09-15  
Stage: 4 — Web Design Literacy  
Checkpoint target: Foundation / Practitioner  
Scope: Web Manager judgment for `minttap.app`; not typeface authorship

## Why this block now

045 established the boundary between task/content obligations and specialist visual authorship. The next highest-value gap is runtime reading behavior: a company site for Apple/Android apps must present product, support, policy, account and data text reliably across Korean/English, responsive widths, font loading/fallback and user text adaptation.

This block deliberately does **not** repeat Design Studio Type construction research. It translates current Type evidence and Web standards into a Web Manager review/briefing contract.

## Core model

`content role → semantic/language structure → typographic role → font selection/fallback → shaping/line breaking → measure/wrapping → responsive/text adaptation → reading/navigation → browser/human validation`

Typography on the Web is not a static mockup property. The rendered result is produced at runtime from document language, available/downloaded fonts, glyph coverage, font matching, shaping/line-breaking rules, CSS, viewport and user overrides.

---

# 1. Language is document semantics, not decoration

**SOURCE** — WHATWG HTML defines `lang` as the primary language of an element's contents and text-bearing attributes; it inherits from the parent when omitted. User agents may use language for font selection, pronunciation, dictionaries and form-control UI. The root `html` language is therefore machine-consumable structure, not merely metadata.

Source: https://html.spec.whatwg.org/multipage/dom.html#the-lang-and-xml:lang-attributes

**SOURCE** — WCAG 2.2 SC 3.1.1 requires the default human language of each page to be programmatically determinable. W3C notes consequences including screen-reader pronunciation and visual rendering.

Source: https://www.w3.org/WAI/WCAG22/Understanding/language-of-page

**SYNTHESIS** — A Korean page with English product names, ticker symbols, store labels or quoted English may require explicit language-of-parts treatment where pronunciation/text processing materially changes. Do not assume visual script recognition substitutes for language semantics.

**MINTTAP DECISION** — Every localized page contract must name its default language and identify meaningful language switches. The website must not infer page language from font family, URL appearance or visible script alone.

**OPEN** — MintTap's supported locales, locale URL strategy and translation workflow are not yet verified.

---

# 2. Font declaration does not prove rendered font

**SOURCE** — CSS Fonts Level 4 defines `font-family` as a prioritized list. The user agent iterates through families until it finds an available face containing the needed glyph; installed fallback can follow when no specified family matches. Downloadable fonts introduce loading, fallback and swap/failure behavior.

Source: https://www.w3.org/TR/css-fonts-4/

**SOURCE** — CSS Fonts Level 4 also defines metric override descriptors such as `ascent-override`, `descent-override` and `line-gap-override`, explicitly illustrating their use to reduce layout movement when switching from fallback to a web font.

**SYNTHESIS** — `font-family: BrandFont` is an instruction, not evidence that every glyph is rendered by BrandFont. Mixed Korean/Latin content can cross font boundaries because coverage and cluster matching participate in selection.

**SYNTHESIS** — Font-loading failure can become a layout and task problem: substitute metrics can alter heading wraps, card height, CTA position, navigation density and cumulative page geometry.

**MINTTAP DECISION** — Web typography review must test intended-font, fallback and delayed/failed-font conditions for task-critical text. A screenshot taken after a successful font load is insufficient evidence.

**DEPENDENCY — Design Studio Type** — Current canonical Type status is Stage 1 PASS. T016 and related work provide controlled webfont loading/fallback evidence; exact production Korean/complex-script, Safari/Firefox/native and human reading remain later validation, not assumed proof.

---

# 3. Korean and English do not share one universal wrapping rule

**SOURCE** — CSS Text Level 3 states that soft-wrap opportunities depend on content language/writing system and CSS. It explicitly documents two Korean styles: `word-break: normal` can break between consecutive Hangul/Hanja, while `word-break: keep-all` suppresses those intra-word opportunities and behaves more like space-separated English text.

Source: https://www.w3.org/TR/css-text-3/#line-breaking

**SYNTHESIS** — Choosing `keep-all` globally because it appears visually cleaner can create avoidable overflow or poor narrow-screen composition; choosing unrestricted syllable breaking globally can damage phrase grouping. The right behavior depends on content role, measure and actual Korean copy.

**MINTTAP DECISION** — Korean line-breaking is a content/runtime decision to validate with real headings, support instructions, policy paragraphs, CTA labels and mixed Latin/ticker strings. No universal `word-break` rule is adopted for all MintTap text.

**VALIDATION** — Stress strings must include long Korean headings, Korean+English app names, URLs/emails, version strings, ticker/data tokens and unspaced/long Latin sequences. Test narrow widths and enlarged text, not only desktop marketing copy.

---

# 4. Reading hierarchy has four distinct layers

For review, separate:

1. **document hierarchy** — sections and relationships in the content model;
2. **semantic heading structure** — actual heading/landmark semantics;
3. **visual hierarchy** — size, weight, spacing, contrast and placement;
4. **reading/navigation utility** — whether a user can scan, locate, resume and understand the material.

**SYNTHESIS** — A visually large line that is not structurally a heading and a semantically correct heading that is visually indistinguishable from body text are different failures. Neither is repaired merely by changing font size.

**MINTTAP DECISION** — Support and governance/policy pages prioritize stable reading/navigation structure over marketing compactness. Marketing pages may use stronger display hierarchy, but not at the expense of semantic order or task prerequisites.

---

# 5. Do not turn readability guidance into fake universal constants

**SOURCE** — WCAG 2.2 SC 1.4.8 (AAA) includes a mechanism for blocks of text to reach no more than 80 characters/glyphs (40 for CJK), among several user-adjustable presentation conditions. It does **not** establish that every authored paragraph at every breakpoint must be exactly that width.

Source: https://www.w3.org/TR/WCAG22/#visual-presentation

**SYNTHESIS** — The familiar idea of a single ideal line length cannot be treated as a universal MintTap token. Script, glyph metrics, font size, content type, viewport and user adaptation all affect reading conditions.

**MINTTAP DECISION** — Evaluate text measure by task and failure: excessive eye travel, difficult line tracking, pathological short wrapping, isolated labels, broken comparisons and loss of hierarchy. Use actual KO/EN content rather than a fixed character-count doctrine.

---

# 6. User text adaptation is a resilience requirement

**SOURCE** — WCAG 2.2 SC 1.4.12 Text Spacing requires no loss of content or functionality when supported text properties are overridden to specified line, paragraph, letter and word spacing values. W3C explicitly says authors are not required to use those values by default; the requirement is adaptation without loss.

Source: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing

**SOURCE** — WCAG 2.2 also includes Resize Text and Reflow requirements at Level AA. These are accessibility requirements, not claims that a particular visual design is readable or aesthetically successful.

Source: https://www.w3.org/TR/WCAG22/#resize-text  
Source: https://www.w3.org/TR/WCAG22/#reflow

**SYNTHESIS** — Fixed-height labels/cards/navigation that work only at authored metrics are fragile. Text growth should generally cause recomposition or container growth rather than clipping, overlap or inaccessible horizontal reading.

**MINTTAP DECISION** — The Web Manager's design brief must include enlarged-text and text-spacing stress conditions for navigation, CTA, support, forms, policy content and data labels. Passing these structural checks does not prove human readability.

---

# 7. Localization is a layout and evidence problem, not string substitution

Localization can change:

- label and heading length;
- phrase boundaries and line-break opportunities;
- font/glyph fallback;
- line-box metrics;
- numeric/date/currency presentation;
- navigation density;
- CTA width;
- legal/support wording and information density.

**SYNTHESIS** — A layout that tolerates English expansion does not thereby prove Korean behavior, and vice versa. Translation-length heuristics are useful for early stress only; final validation requires actual localized content.

**MINTTAP DECISION** — Page contracts must carry localization stress strings and content-role constraints before Design Studio authors final composition. Do not solve overflow by silently abbreviating policy/support meaning.

**OPEN** — Actual MintTap terminology glossary, localization vendor/process, legal translations and app/store naming conventions remain unverified.

---

# 8. Operational and numeric text needs role-specific treatment

A company/app site can contain version numbers, dates, percentages, prices/subscriptions, tickers, platform names and support identifiers.

**SYNTHESIS** — Numeric typography should follow the comparison task. Tabular figures can help aligned comparisons, but applying them to all prose numbers is unnecessary. Monospace is likewise not automatically appropriate for technical data.

**MINTTAP DECISION** — The Web Manager specifies where stable numeric comparison/alignment is a requirement; Type/Web specialists choose the exact OpenType/font treatment. Product claims and financial examples must remain truthful content first, typographic styling second.

---

# 9. Failure taxonomy for Web Manager review

Use this diagnostic chain instead of saying "the typography feels wrong":

`content/semantic failure → language-tag failure → font availability/coverage failure → fallback/metric failure → shaping/line-break failure → measure/wrapping failure → hierarchy/grouping failure → responsive/text-adaptation failure → task/reading consequence`

Examples:

- heading wraps badly only during webfont fallback → font metric/loading + composition issue;
- Korean phrase breaks at undesirable syllable boundaries → language/line-breaking/content-role issue;
- support heading looks prominent but is not a heading → semantic issue;
- text clips at user spacing override → resilience/layout issue;
- policy text is technically conforming but users cannot locate a section → information/reading-navigation issue requiring human/task evidence, not a font-size guess.

---

# 10. Web Typography / Reading Contract

For any substantial MintTap page, record:

| Field | Required question |
| --- | --- |
| content roles | heading, body, instruction, label, metadata, data, code/identifier, legal/support? |
| semantic structure | what document/heading relationships must survive presentation? |
| default language | what valid language tag represents the page? |
| language changes | which meaningful parts switch language? |
| font source | system/local/downloaded; what can fail or be unavailable? |
| fallback contract | what families/scripts/metrics must remain usable? |
| mixed-script condition | KO/EN/numeric/symbol combinations to test? |
| line-breaking policy | what behavior is intentional for each content role? |
| measure/wrapping stress | longest realistic strings and narrow conditions? |
| numeric role | prose, identifier or comparison-critical data? |
| user adaptation | resize/reflow/text-spacing conditions? |
| responsive invariant | what hierarchy/relationship must survive recomposition? |
| browser matrix | which engines/devices need actual evidence? |
| human question | what reading/scan/comprehension claim requires users rather than inspection? |

This contract layers on 045's Visual/Web Design Review Contract and the Stage 2/3 Page/Task/Interaction contracts.

---

# 11. Design Studio dependencies and handoffs

## Type

**HANDOFF** — Provide exact KO/EN corpus, product font candidates, declared weights, fallback stack, loading strategy and comparison-critical numeric roles. Request actual glyph coverage, fallback seam, metric/wrapping and feature validation. Do not ask Type to invent content hierarchy.

Latest specialist status checked 2026-09-15: Type Stage 1 PASS; Stage 2 entry audit next (`T020`). Production Korean/complex-script/cross-browser/native/human evidence remains explicitly open.

## Web Design

**HANDOFF** — Web Design must consume the contract in complete responsive page/task surfaces, including localization growth, font loading/failure, text adaptation and browser execution.

Latest specialist status checked 2026-09-15: Web Stage 1 PASS; Stage 2 entry accepted/not passed (`W010`); next explicit content gap is W011 iconography/non-text signals. This supersedes the stale coordinator global summary.

## Layout / Interaction

**HANDOFF** — Challenge fixed-height/fixed-cell ownership, grouping and responsive recomposition when text grows or fallback metrics change. Preserve focus/task/state continuity when typography causes geometry change.

## Color

**HANDOFF** — Validate text/surface hierarchy and contrast with actual fonts/weights/sizes and states; color must not compensate for weak semantic hierarchy.

No Design Studio canonical file is edited by this study.

---

# 12. Verified facts vs synthesis vs open questions

## Verified/source-grounded

- HTML `lang` represents content language and can affect processing/rendering.
- WCAG requires programmatically determinable page language at Level A.
- CSS font matching is a prioritized runtime process with glyph coverage and fallback.
- downloadable fonts have loading/fallback behavior; metric overrides exist.
- CSS line-breaking opportunities depend on language/writing system; Korean has documented `normal` and `keep-all` behaviors.
- WCAG Text Spacing is an adaptation/no-loss requirement, not a mandate to author those exact spacing values.

## Synthesis / professional judgment

- typography failures should be diagnosed as a chain from semantics/language through runtime font/line behavior to task consequence;
- localization is a composition/runtime stress condition, not merely translation;
- line length should be evaluated by role/failure and actual scripts rather than a universal magic number;
- fallback/loading tests belong in acceptance criteria for task-critical text.

## Open / requires project evidence

- MintTap production font families and weights;
- exact Korean/English locale set and URL/content model;
- actual support/privacy/product corpus;
- final browser/device support matrix;
- final app/store terminology and screenshots;
- human reading, scan, comprehension and preference evidence.

---

# 13. Competency check

Checkpoint passes only if the Web Manager can:

1. explain why CSS font declaration is not proof of rendered glyph/font;
2. distinguish language semantics, font fallback, line breaking, wrapping and layout failures;
3. explain Korean `normal` vs `keep-all` without turning either into a universal rule;
4. distinguish WCAG adaptation requirements from readability/user evidence;
5. review headings/body/support/policy/data text across KO/EN and narrow/enlarged conditions;
6. write a Web Typography / Reading Contract and route specialist work correctly;
7. state what remains unverified rather than inventing MintTap production facts.

**CHECKPOINT: PASS — FOUNDATION/PRACTITIONER.**

The next Stage 4 block should address **Web Color, Surfaces, State & Brand Application Literacy**, reusing Design Studio Color evidence and focusing on actual browser/page application rather than repeating color science.
