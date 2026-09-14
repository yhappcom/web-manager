# Study 004 — App Store / Google Play ↔ Website Content Synchronization

Status: FOUNDATION RESEARCH / RELEASE-OPERATIONS BASELINE
Date: 2026-09-14
Scope: `minttap.app` product pages and Apple App Store / Google Play public metadata

## Question

How should MintTap keep website product content, App Store metadata and Google Play store listings consistent as apps and versions change, without forcing every channel to use identical copy?

## RELATED DESIGN STUDIO CHECK

- Web Design: channel content must become a coherent page system and survive responsive/localized/browser conditions; implementation is not the same as content truth.
- Layout/Interaction: screenshots, release states, support/error messaging and navigation must reflect actual user-visible behavior.
- Type/Color: store/web assets later require cross-channel hierarchy, localization and visual-system validation; this study does not define final visual treatment.

## AUTHORITATIVE SOURCES CHECKED

### Apple
- App Review Guidelines, 2.3 Accurate Metadata
  - https://developer.apple.com/app-store/review/guidelines/
- App Store Connect — Platform version information
  - https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- Required, localizable, and editable properties
  - https://developer.apple.com/help/app-store-connect/reference/app-information/required-localizable-and-editable-properties
- Localize app information
  - https://developer.apple.com/help/app-store-connect/manage-app-information/localize-app-information
- Manage app privacy
  - https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy

### Google Play
- Create and set up your app
  - https://support.google.com/googleplay/android-developer/answer/9859152
- Deceptive Behavior policy
  - https://support.google.com/googleplay/android-developer/answer/17006354
- Best practices for your store listing
  - https://support.google.com/googleplay/android-developer/answer/13393723
- Translate and localize your app
  - https://support.google.com/googleplay/android-developer/answer/9844778
- Data safety guidance
  - https://support.google.com/googleplay/android-developer/answer/10787469

---

## 1. SOURCE — Store metadata must describe the real app

### Apple

App Review Guideline 2.3 says metadata — including privacy information, description, screenshots and previews — must accurately reflect the app's core experience and remain up to date with new versions.

App Store Connect treats screenshots, description, support URL, marketing URL and What's New as version/platform metadata with localization/editability rules. Apple also notes that privacy-policy URL changes release with the next app version.

### Google Play

Google's deception policy requires title, description, icon, screenshots and other metadata to accurately reflect actual functionality. Google explicitly prohibits misleading or impossible feature claims and instructs developers to update the store listing when functionality changes.

Google store listings support localized title, short description, full description and graphic assets. Metadata policy applies to translations as well.

### SYNTHESIS

The required relationship is **truth consistency**, not literal copy equality.

A website, App Store description and Play Store short description serve different constraints and audiences. Their wording may differ, but any factual claim about capability, privacy, account requirements, availability, screenshots, pricing/subscription behavior or support must resolve to the same product reality.

---

## 2. MINTTAP DECISION — Establish a canonical Product Truth Record

Each app needs one internal product-truth record that is upstream of public marketing copy.

Minimum fields:

- canonical app name;
- slug;
- Apple bundle ID;
- Android package name;
- current public version(s);
- supported platforms/devices;
- current release status;
- core product purpose;
- currently shipped user-visible features;
- account/login requirements;
- subscription/IAP/payment behavior;
- region availability where relevant;
- privacy/data-impact summary linked to the App Data Contract from Study 003;
- support URL;
- privacy URL;
- account-deletion URL when applicable;
- canonical store destinations;
- current screenshot/UI evidence set;
- current release notes / change summary;
- known material limitations that affect claims;
- last technical confirmation date;
- confirming product/engineering owner.

The Product Truth Record answers **what is true**. Channel copy answers **how that truth is communicated here**.

---

## 3. MINTTAP DECISION — Three layers of content

### Layer A — Product truth: must match

These facts may not contradict across channels:

- app identity/name;
- core purpose;
- whether a feature actually exists in the released version;
- account/login requirements;
- data/privacy behavior;
- subscription/payment behavior;
- platform/device availability;
- support and data-control destinations;
- user-visible release state.

### Layer B — Channel expression: may differ

These may be written differently while preserving truth:

- headline/tagline;
- feature ordering;
- amount of explanatory detail;
- App Store subtitle vs Play short description vs website hero copy;
- page section hierarchy;
- calls to action;
- SEO-oriented supporting copy;
- localized idiom.

### Layer C — Campaign/promotional content: expires

Examples:

- launch announcements;
- seasonal messaging;
- temporary campaign pages;
- promotional text;
- feature spotlights.

Campaign content must have an owner and expiry/review date. It must never become the accidental source of truth for permanent app capabilities.

---

## 4. MINTTAP DECISION — Claim traceability

Every major product claim used on `minttap.app` should be traceable to one of:

1. shipped functionality in the current public release;
2. a clearly identified currently available service capability;
3. a clearly labeled future/beta/preview state that is allowed for that channel and not presented as already shipped.

### Default MintTap rule

For normal public product pages and store listings, describe **currently available behavior**. Do not use roadmap features as if they already exist.

If preview content is ever used on the company website, it must be unmistakably labeled and must not be reused in store metadata unless the platform's rules and actual reviewed app state support it.

---

## 5. Screenshots and visual claims

### SOURCE

Apple requires screenshots to show what the app looks like on a device and requires metadata to accurately represent the core experience.

Google requires screenshots/images to accurately depict functionality and warns against misleading graphic assets. Google also recommends localized screenshots when screenshots contain text.

### MINTTAP DECISION

Maintain a version-linked **Screenshot Evidence Set** per app.

For each asset record:

- app/version/build source;
- platform/device class;
- locale;
- feature shown;
- whether UI text is live or composited;
- capture date;
- store/web usages;
- replacement trigger.

Website device mockups may frame the screenshot visually, but the depicted in-app state must not invent unavailable functionality.

Replace screenshots when a UI or workflow change makes the old image materially misleading, not merely because pixels differ.

---

## 6. Release synchronization model

Create a **Content Release Manifest** for each material app release.

Minimum manifest:

- app + version;
- release date/status;
- feature additions/removals/behavior changes;
- privacy/data-impact flag;
- account/subscription-impact flag;
- screenshot-impact flag;
- support/FAQ-impact flag;
- website product-copy-impact flag;
- App Store description/What's New impact;
- Google Play listing impact;
- localization impact;
- links requiring change;
- completion status and owner for each surface.

### Release sequence

1. engineering/product confirms release facts;
2. privacy/data changes reconcile through the App Data Contract;
3. Web Manager reviews product-page/support/privacy/deletion impact;
4. store metadata owner reviews Apple/Google listing impact;
5. assets/translations are updated where materially affected;
6. cross-surface consistency check is performed;
7. release occurs under the appropriate platform review/publishing process;
8. post-release public surfaces are verified.

The sequence may overlap operationally, but no copy should be based on unconfirmed implementation assumptions.

---

## 7. Channel field map

### Apple App Store

Track at minimum:

- name;
- subtitle;
- screenshots / app previews;
- promotional text;
- description;
- keywords;
- Support URL;
- Marketing URL;
- What's New;
- privacy policy URL and User Privacy Choices URL where used;
- App Privacy disclosures.

Important platform behavior:

- many properties are localizable;
- editability depends on app/version status;
- privacy URL changes release with the next app version;
- public changes may not appear instantly.

### Google Play

Track at minimum:

- app name;
- short description;
- full description;
- icon / feature graphics / screenshots / video where used;
- support email;
- website/support URL;
- privacy-policy URL;
- Data safety answers;
- account-deletion URL when applicable;
- localized listing variants;
- custom store listings if MintTap later uses them.

### MintTap website

Track at minimum:

- app product-page title/name;
- one-sentence proposition;
- feature list and proof;
- screenshots/media;
- platform/download destinations;
- account/subscription explanation where material;
- support/privacy/account-control links;
- current availability;
- release/update information if shown.

---

## 8. MINTTAP DECISION — Do not make the store listing the website CMS

Store metadata is constrained, review-sensitive and platform-specific. It should not be copied mechanically into the website.

Likewise, website marketing copy should not be pasted blindly into App Store / Play Console fields.

Instead:

**Product Truth Record → channel-specific approved copy → public surfaces**

This prevents:

- stale claims copied from an old store description;
- SEO copy leaking into constrained store fields;
- one platform's terminology becoming inaccurate on the other;
- support/privacy links diverging silently;
- screenshots surviving after their depicted feature changed.

---

## 9. Localization synchronization

### SOURCE

Both Apple and Google support localized store metadata. Google policies apply to translated listings, and localized graphic assets can be supplied. Apple metadata localizations are managed separately from app-binary localization.

### MINTTAP DECISION

Treat every supported locale as a maintained content artifact, not a one-time translation.

For each locale maintain:

- approved app name where localization differs;
- core proposition;
- feature terminology glossary;
- privacy/support/deletion URLs or localized equivalents;
- store descriptions;
- website product copy;
- screenshot text/assets;
- last review date.

When a source-language feature claim changes, all affected locales enter a review state before the change is considered complete.

Machine/automatic translation may be available on platforms but is not MintTap's canonical localized copy without review.

---

## 10. Responsibility model

### Product / Engineering

Owns confirmation of technical product truth:

- shipped capability;
- version/build;
- account/subscription behavior;
- data/SDK/backend behavior;
- technical limitations.

### Web Manager

Owns:

- `minttap.app` product/support/privacy/deletion content;
- website freshness and link integrity;
- Product Truth Record / Content Release Manifest coordination for web-facing facts;
- cross-surface discrepancy detection;
- launch-time web validation;
- escalation when store/web/app facts conflict.

### Store-console owner

Owns publishing Apple/Google metadata unless the Web Manager is separately assigned that console role.

The Web Manager supplies/reviews website-dependent URLs and consistency but must not assume console publication occurred merely because website content is ready.

---

## 11. Release discrepancy severity

### BLOCKER

- privacy/data disclosure mismatch;
- non-existent feature claimed as available;
- broken required support/privacy/deletion URL;
- account/subscription behavior materially misdescribed;
- wrong app/store destination;
- misleading screenshot of core functionality.

### HIGH

- major feature removal still promoted;
- materially stale screenshot/workflow;
- support contact no longer operational;
- one locale makes a materially different claim.

### NORMAL

- non-material wording drift;
- style/ordering difference that does not alter meaning;
- cosmetic UI differences that do not misrepresent interaction or capability.

Not all drift is a bug. **Contradictory product truth is the bug.**

---

## 12. VALIDATION GATES

Before a material release is considered content-synchronized:

- current public build checked against core claims;
- Product Truth Record updated;
- Content Release Manifest completed;
- privacy-impact determination completed;
- Apple and Google metadata reviewed for affected claims;
- website app page reviewed;
- support/privacy/deletion links tested;
- screenshots checked for material accuracy;
- supported locales checked for affected claims;
- store download links verified;
- post-publication pages checked in live storefront/web contexts.

## OPEN

- exact MintTap store-console ownership is not yet documented;
- actual app inventory/version mapping has not yet been imported;
- canonical schema/storage format for Product Truth Record and Content Release Manifest is not selected;
- release-note publishing strategy on `minttap.app` is undecided;
- screenshot production/approval workflow is not defined;
- localization owner/reviewer roles are not defined.

## CHANGE WATCH

Recheck before launches:

- Apple metadata requirements/editability and App Review Guideline 2.3;
- Apple localization and privacy URL release behavior;
- Google Play Metadata/Deceptive Behavior policies;
- Google listing/localization/custom-listing behavior;
- Google Data safety and account deletion fields.

## PROJECT-READINESS RESULT

After this study, Web Manager should be able to distinguish:

- facts that must remain identical in meaning across app/store/web;
- copy that can legitimately vary by channel;
- temporary promotional content that needs expiry controls;
- changes that require a cross-surface release review;
- discrepancies serious enough to block launch.

Foundation status remains below PASS until the process is run against a real MintTap release and post-publication surfaces are verified.