# 057 — Media Accessibility, Captions, Transcripts, Audio Description & Product-Demo Communication

Date: 2026-09-16  
Stage: 5 — Accessibility  
Checkpoint target: FOUNDATION / PRACTITIONER

## Why this block exists

MintTap is an Apple/Android app company. Product pages, launch pages and support may eventually use app-preview videos, tutorials, demonstrations, webinars or audio. Study 048 already established static screenshot/product-evidence truth. This block does not repeat image accessibility; it establishes the additional obligations created when meaning unfolds over time.

Core model:

`communication purpose → media class → information channels → information required for task/comprehension → synchronized equivalent(s) → player/control operability → product-evidence truth → localization/lifecycle → complete-media validation`

---

## 1. SOURCE — WCAG time-based media is channel- and media-type-specific

WCAG 2.2 Guideline 1.2 does not impose one universal “add a transcript” rule. Relevant requirements depend on whether media is prerecorded/live, audio-only/video-only/synchronized, and the target conformance level.

For prerecorded synchronized video with meaningful audio:
- SC 1.2.2 Captions (Prerecorded) is Level A;
- SC 1.2.3 Audio Description or Media Alternative (Prerecorded) is Level A;
- SC 1.2.5 Audio Description (Prerecorded) is Level AA.

For live synchronized media, SC 1.2.4 Captions (Live) is Level AA.

For prerecorded audio-only, an alternative for time-based media is required by SC 1.2.1 at Level A. For prerecorded video-only, SC 1.2.1 requires an alternative for time-based media or an audio track presenting equivalent information.

Primary sources checked 2026-09-16:
- W3C WCAG 2.2 / ACT criterion index: https://www.w3.org/WAI/standards-guidelines/act/rules/
- W3C WAI Planning Audio and Video Media: https://www.w3.org/WAI/media/av/planning/
- W3C WAI Captions/Subtitles: https://www.w3.org/WAI/media/av/captions/
- W3C WAI Transcripts: https://www.w3.org/WAI/media/av/transcripts/
- W3C WAI Description of Visual Information: https://www.w3.org/WAI/media/av/description/

### SYNTHESIS

`caption != transcript != audio description != media alternative`.

They solve different channel-loss problems. Captions synchronize important speech/sound with video. A transcript provides a non-time-bound text representation. Audio description makes important visual information available through audio. A descriptive transcript/media alternative can combine auditory and visual information in text, but at AA a prerecorded synchronized video's visual information still falls under SC 1.2.5 audio-description requirements unless the visual information is already conveyed in the main audio or the content qualifies for the media-alternative exception.

### FAILURE MODE

A page saying “Transcript available” does not by itself prove that a prerecorded synchronized product demo meets AA media requirements.

---

## 2. SOURCE — captions must carry meaningful audio, not merely speech-shaped text

W3C describes captions as synchronized text for speech and other sounds needed to understand content. Caption quality includes synchronization, speaker identification where needed, punctuation/capitalization and important non-speech sounds. WAI's Easy Checks explicitly warns that merely having auto-generated captions is not sufficient evidence of adequate captions.

Primary sources:
- https://www.w3.org/WAI/media/av/captions/
- https://www.w3.org/WAI/test-evaluate/easy-checks/captions/

### SYNTHESIS

Caption validation has at least four dimensions:

`availability → semantic completeness → temporal synchronization → readability/presentation`.

Automatic speech recognition may be a production aid, but “captions generated” is not a quality gate. Product names, ticker symbols, finance terminology, UI labels and proper nouns are especially plausible transcription failure points for MintTap media and require review if such media exists.

### OPEN

No production MintTap video/audio inventory, caption workflow, target languages or player is established in this repository. Do not infer one.

---

## 3. SOURCE — visual information can be integrated into the main narration

W3C explains that audio description communicates important visual information that is otherwise unavailable through the main audio. It also notes that if important visual information is already provided in the main audio, separate description may not be necessary. Planning accessible media before production can therefore reduce later description work by having speakers naturally verbalize relevant visual information.

Primary source:
- https://www.w3.org/WAI/media/av/description/

### SYNTHESIS — accessible-by-script production

For an app demonstration, narration such as “Tap Tax Adjustment, then choose the 2025 Final ROC year” carries materially more accessible information than “Tap here, then choose this.” If the script names controls, states, values and changes that matter, accessibility is designed into the source communication instead of being bolted on after editing.

This does **not** justify narrating every decorative pixel. The contract is the information necessary to understand the demonstration and task.

### MINTTAP DIRECTION

If product-demo media is created, write the accessibility information-channel plan at storyboard/script time, before recording. Mark each important fact as available through audio, visual, captions and/or descriptive equivalent. Any fact available through only one sensory channel needs deliberate review.

---

## 4. Transcript is useful beyond minimum conformance, but normative level must remain precise

WAI's current media guidance distinguishes WCAG requirements from user benefits beyond WCAG. For prerecorded video with audio, captions are Level A; a transcript of the whole synchronized presentation is useful but is not simply a substitute for all AA requirements. For prerecorded audio-only, the transcript/media alternative is Level A.

Primary source:
- https://www.w3.org/WAI/media/av/transcripts/

### SYNTHESIS

A transcript can improve scanning, search, translation, quotation, low-bandwidth access and comprehension. Those are strong content-strategy benefits, but Web Manager must not relabel an optional improvement as a normative requirement or relabel a normative requirement as optional.

This distinction also matters for Stage 6: a well-structured transcript can create useful indexable text, but SEO benefit is secondary to communicating an equivalent accurately.

---

## 5. Media player accessibility is separate from media-content alternatives

W3C's media planning guidance explicitly identifies media-player functionality as an additional accessibility concern and points to other WCAG requirements such as Pause/Stop/Hide and Audio Control.

Primary source:
- https://www.w3.org/WAI/media/av/planning/

### SYNTHESIS

`accessible media content != accessible media player`.

A perfectly captioned video can still be unusable if keyboard users cannot operate play/pause/captions, focus is invisible, controls disappear unpredictably, labels are absent, or autoplay/audio behavior violates user control. Conversely, an operable player does not repair missing captions or visual equivalents.

### DEPENDENCY

Reuse 052 Semantic Accessibility Contract, 053 Operability/Focus Contract, 055 Application-State Contract and 056 motion/timing/user-preference contract when a real player is selected. Do not create a custom player merely to satisfy visual branding unless native/provider controls are demonstrably insufficient and the reconstruction cost is justified.

---

## 6. Product demonstration remains product evidence

048 established:

`website claim ↔ website screenshot/demo ↔ shipped app behavior ↔ store representation`.

Time-based media adds temporal truth risks:
- editing away prerequisite steps or latency;
- compositing states that cannot occur in sequence;
- narration claiming behavior not shown or shipped;
- showing obsolete UI after an app release;
- captions/transcripts preserving old terminology after the video changes;
- localization where spoken/captioned UI labels no longer match the localized app.

### MINTTAP DIRECTION — extend Product Evidence Ledger

For time-based product media add:
- source app/build/platform/locale;
- capture and edit dates;
- actual capture vs simulation/composite classification;
- claims/tasks demonstrated;
- narration language;
- caption languages and review status;
- transcript/descriptive-equivalent version;
- audio-description strategy (integrated narration / separate track/version / other conforming approach);
- player/provider;
- poster frame;
- store-asset relationship;
- retirement trigger and owner.

A video update and its caption/transcript/descriptive equivalent are one versioned communication unit.

---

## 7. SOURCE / CHANGE WATCH — Apple app-preview facts are store policy/format facts, not web accessibility conformance

Apple currently describes app previews as optional assets that visually communicate the app experience. App Store Connect currently permits up to three previews per supported device size/language, and current preview specifications specify 15–30 seconds, supported formats/resolutions and audio parameters. Localization fallback can cause another language's preview to appear when a locale-specific preview is absent.

Primary sources checked 2026-09-16:
- Apple — Upload app previews and screenshots: https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots
- Apple — App preview specifications: https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications

Apple also has a separate App Accessibility framework for developers to indicate app accessibility support; its captions evaluation criteria concern accessibility inside the app. That should not be confused with proving WCAG conformance of minttap.app media.

Primary source:
- Apple — Captions evaluation criteria: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/captions-evaluation-criteria

### SYNTHESIS

`store asset acceptance != website accessibility conformance` and `native-app accessibility declaration != website accessibility evidence`.

Store requirements are CHANGE WATCH items. Web accessibility claims remain scoped to the actual web content/process and applicable conformance target.

---

## 8. Product-Demo Media Accessibility Contract

For each media item, record:

| Field | Required question |
| --- | --- |
| purpose/task | What user question or task does the media support? |
| media class | prerecorded/live; audio-only/video-only/synchronized? |
| target conformance | Which WCAG level/scope is being claimed? |
| auditory information | What meaning exists only in speech/sound? |
| visual information | What meaning exists only visually? |
| captions | required? language(s)? human-reviewed? synchronized? important sounds/speakers represented? |
| transcript/media alternative | required or supplementary? does it carry the necessary auditory/visual information? |
| audio description | required? already integrated in main narration? separate mechanism needed? |
| player | keyboard/focus/name/state/control behavior? caption/description controls? |
| autoplay/motion/timing | which 056 obligations/preferences apply? |
| evidence truth | source build/platform/locale and edit/composite boundary? |
| localization | narration/caption/transcript/UI terminology alignment? |
| lifecycle | what change invalidates video or equivalents? |
| validation | content review + browser/input/AT/device + complete-media/task evidence? |

---

## 9. Validation ladder

Do not call media production-ready from file presence alone.

1. **Inventory/classification** — identify media type and information channels.
2. **Normative mapping** — map applicable WCAG A/AA obligations without conflating optional enhancements.
3. **Content review** — verify captions, transcript/equivalent and description against the actual media.
4. **Temporal review** — verify caption synchronization and that edits do not break meaning.
5. **Player/browser review** — keyboard, focus, labels/states, captions/description controls, zoom/reflow where applicable.
6. **AT/device review** — representative supported browser/OS/AT/input combinations.
7. **Task/evidence review** — confirm the user can obtain the intended product/support information and that the demo remains truthful to the shipped app.
8. **Human review** — disability-informed evaluation where material; automated checks do not establish semantic quality of captions or description.

---

## 10. Design Studio dependencies / handoffs

### Web Design
When media enters a real page, validate player hierarchy, visible controls, keyboard/focus behavior, captions/description discoverability, narrow-width/reflow behavior and poster-frame communication. Do not treat a branded custom player as inherently superior to native/provider controls.

### Layout / Interaction
Define media-control placement and responsive adaptation without hiding essential controls. If a demo is embedded in a carousel/modal/transient layer, preserve the 053/055 focus/state contracts and 056 motion/timing obligations.

### Type
Validate caption/subtitle legibility and KO/EN/mixed-script behavior in the actual delivery environment. Do not infer readable caption typography from static mockups.

### Color
Validate caption/control contrast and user-environment behavior; do not use color alone for play state, selected track, error or other meaning.

### Web Manager retains
Media classification, WCAG level mapping, information-equivalence requirements, product-evidence provenance/lifecycle, store-vs-web claim boundaries and complete-media validation scope.

No Design Studio canonical file is edited by Web Manager.

---

## 11. OPEN / project facts required later

Unknown until actual MintTap implementation/content inventory is inspected:
- whether minttap.app uses any audio/video at all;
- whether product previews are self-hosted, embedded or store-only;
- player/provider and accessibility behavior;
- autoplay/muted-loop behavior;
- caption/transcript/description availability and languages;
- whether tutorials demonstrate consequential financial/tax workflows;
- app-build/media provenance and retirement workflow;
- supported browser/OS/AT/device matrix;
- legal/regulatory accessibility obligations beyond a chosen WCAG target.

Do not manufacture these facts.

---

## 12. Competency check

PASS at FOUNDATION/PRACTITIONER checkpoint if Web Manager can:
- classify media before choosing an accessibility technique;
- distinguish captions, transcripts, audio description and media alternatives;
- state the relevant A/AA distinction without turning optional enhancements into requirements;
- explain why transcript-only does not generally prove AA conformance for synchronized prerecorded video;
- plan accessible narration before recording;
- separate player accessibility from content-alternative accessibility;
- preserve product-evidence truth across video, captions, transcript and app versions;
- define a reproducible validation ladder and Design Studio handoff.

**Result: PASS.**

## Next

Proceed to **058 — Stage 5 Integration: Accessibility Conformance, Complete-Process Evidence & App-Company Competency Review**, unless a new prerequisite gap is found while integrating 051–057. The integration must test whether the seven contracts operate coherently across Company, Product, Support and Governance/account-control page/process families, and must keep production conformance claims OPEN until real implementation evidence exists.