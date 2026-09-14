# Study 003 — Privacy, Support & Account-Deletion Content Architecture

Status: FOUNDATION RESEARCH / PLATFORM POLICY BASELINE
Date: 2026-09-14
Scope: `minttap.app` support for Apple App Store and Google Play app launches

## Question

How should MintTap structure privacy, support and account-deletion web content so that each Apple/Android app has a durable, reviewable and operationally consistent web surface?

This study establishes a platform-policy baseline. It does **not** replace jurisdiction-specific legal review (for example, Korean PIPA, GDPR, CCPA/CPRA or sector-specific law).

## RELATED DESIGN STUDIO CHECK

### Web Design
- Checked: `yhappcom/design-studio/progress/WEB_STATUS.md`.
- Reusable finding: web work must define complete page systems, forms/states, accessibility behavior and browser/device validation, not just static page copy.
- Transfer opportunity: privacy/support/deletion pages will later need real responsive, keyboard, focus, localization and error/recovery validation.

### Accessibility / Layout & Interaction
- Checked: `yhappcom/design-studio/research/004-accessibility-reflow-targets-focus.md`.
- Reusable finding: focus visibility, target geometry, reflow and alternate operation are structural requirements, not late polish.
- Transfer opportunity: destructive account-deletion actions and support forms require explicit focus, confirmation, error/recovery and narrow-width behavior.

### Type / Color
- No MintTap-specific decision is required in this policy/content block. Later production validation must apply the current Type and Color evidence for legal/support reading density, text scaling, contrast, focus and state communication.

## AUTHORITATIVE SOURCES CHECKED

### Apple

1. App Store Review Guidelines — Privacy, 5.1.1 and account sign-in/deletion
   - https://developer.apple.com/app-store/review/guidelines/
2. App Store Connect Help — App privacy
   - https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
3. App Store Connect Help — Platform version information / Support URL
   - https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
4. Apple Developer Support — Offering account deletion in your app
   - https://developer.apple.com/support/offering-account-deletion-in-your-app
5. Apple HIG — Managing accounts
   - https://developer.apple.com/design/human-interface-guidelines/managing-accounts

### Google Play

1. User Data policy
   - https://support.google.com/googleplay/android-developer/answer/10144311
2. Understanding Google Play's app account deletion requirements
   - https://support.google.com/googleplay/android-developer/answer/13327111
3. Data safety section guidance
   - https://support.google.com/googleplay/android-developer/answer/10787469
4. Create and set up your app — contact details
   - https://support.google.com/googleplay/android-developer/answer/9859152
5. How to support your app's users
   - https://support.google.com/googleplay/android-developer/answer/113477

Policy-sensitive findings must be rechecked before each app launch and after material platform-policy changes.

---

## 1. SOURCE — Privacy policy requirements

### Apple

Apple requires a privacy policy URL for all apps in App Store Connect. App Review Guideline 5.1.1 additionally requires an easily accessible privacy-policy link inside the app.

Apple states that the privacy policy must clearly identify:

- what data the app/service collects, if any;
- how the data is collected;
- the purposes for which the data is used;
- third parties that receive/share user data and the expected protection level;
- retention/deletion policies;
- how users can revoke consent and/or request deletion of data.

App Store Connect also provides an optional **User Privacy Choices URL** for a public page where users can learn about and manage privacy choices such as data access, deletion or changes.

### Google Play

Google Play requires every app to provide a privacy-policy link in Play Console and a privacy-policy link or text within the app. This applies even when an app does not collect personal/sensitive user data.

Google's policy requires the privacy policy to include, at minimum:

- developer information and a privacy point of contact or inquiry mechanism;
- the personal/sensitive data accessed, collected, used and shared;
- parties with which such data is shared;
- secure handling procedures;
- retention and deletion policy;
- clear identification as a privacy policy.

The app or developer/entity named on the Play Store listing must appear in the policy. Google further requires the policy URL to be active, publicly accessible, non-geofenced, non-editable by users, and not a PDF.

### SYNTHESIS

A generic company page that vaguely says "we respect privacy" is not sufficient. The policy must be a maintained representation of the actual app and SDK behavior.

A store disclosure and a website privacy policy are different surfaces, but they must describe the same underlying data-processing reality.

---

## 2. MINTTAP DECISION — Separate company website privacy from app privacy

Use two different scopes:

- `/privacy/` — MintTap website/company privacy surface for `minttap.app` itself, when applicable.
- `/apps/<app-slug>/privacy/` — canonical privacy policy for the specific app.

Every released MintTap app gets its own durable app privacy URL even when it collects no user data. A no-collection app should state that fact accurately and still identify scope, developer and contact route.

### Why

- reduces ambiguity when apps use different SDKs, accounts or data types;
- gives App Store / Play Console one clear governing URL per app;
- prevents one app's policy changes from silently changing another app's disclosure;
- makes version/release audits feasible;
- scales better as MintTap adds products.

A combined multi-app policy may be reconsidered later only if app data practices genuinely converge and scope remains unambiguous.

---

## 3. MINTTAP DECISION — Canonical app privacy-page content model

Each `/apps/<app-slug>/privacy/` page should contain the following sections. Items marked PLATFORM are directly motivated by Apple/Google requirements; other items are operational structure.

1. **Policy identity** — PLATFORM
   - title: Privacy Policy;
   - exact app name;
   - MintTap/developer entity identity matching store-facing identity;
   - effective date and last-updated date.

2. **Scope**
   - covered app/platforms;
   - whether the page covers related web services or only the app.

3. **Data inventory** — PLATFORM
   For every relevant data category:
   - data type;
   - source / collection method;
   - whether required or optional where meaningful;
   - purpose of use;
   - whether transmitted off-device;
   - storage/processing context;
   - sharing/recipient category.

4. **Third parties / SDKs / processors** — PLATFORM
   - analytics, advertising, authentication, cloud/service providers and other parties that receive user data;
   - role/purpose of each material party.

5. **Security / secure handling** — GOOGLE PLATFORM
   - high-level handling controls appropriate for public disclosure;
   - do not expose secrets or security-sensitive implementation details.

6. **Retention and deletion** — APPLE + GOOGLE PLATFORM
   - retention logic or periods where known;
   - deletion trigger;
   - exceptions where data must legitimately be retained;
   - link to account/data-control mechanism where applicable.

7. **User choices and controls** — APPLE PLATFORM
   - consent withdrawal/permission control where applicable;
   - account deletion;
   - other access/change/delete controls where provided.

8. **Children / special categories / region supplements**
   - include only if relevant to the app and launch regions;
   - requirements must come from dedicated legal/platform study, not template filler.

9. **Privacy contact** — GOOGLE PLATFORM
   - stable privacy contact or inquiry mechanism.

10. **Changes to the policy**
   - how effective/updated dates are maintained;
   - material-change communication mechanism where legally/operationally required.

### Important rule

Do not write data categories from memory. Build policy content from the app's verified technical data inventory, SDK list and server behavior.

---

## 4. SOURCE — Account deletion requirements

### Apple

Apps that support account creation must let users initiate account deletion within the app. Deactivation/freezing is not a substitute for deleting the account and associated data not legally required to be retained.

If a user must visit a website to finish deletion, the app should link directly to the page that completes the process. For ordinary, non-highly-regulated apps, Apple says the user should not be forced through unnecessary phone/email/customer-service flows.

Reasonable reauthentication and confirmation are allowed, but the process must not be unnecessarily difficult.

Apple also states:

- deletion may be asynchronous/manual if users are told the expected timing and receive completion confirmation;
- Sign in with Apple tokens should be revoked when the account is deleted;
- user-generated content associated with the account is expected to be deleted unless retention is legally required;
- if auto-renewable subscriptions exist, users must understand that billing can continue through Apple and how cancellation is handled.

### Google Play

If an app permits account creation, Google requires both:

- an in-app path to request deletion of the app account and associated data; and
- an external web resource where users can request deletion without being forced to reinstall/use the app.

The web resource must be functional, relevant to account deletion, prominently expose the deletion pathway, and reference the app or developer name as shown on Google Play.

Account deactivation/freezing does not qualify as account deletion. If some data is retained for legitimate reasons such as security, fraud prevention or regulatory compliance, the user must be informed.

---

## 5. MINTTAP DECISION — Dedicated per-app account-deletion resource

For every MintTap app that enables account creation, reserve:

`/apps/<app-slug>/account-deletion/`

This is a first-class durable URL, not a hidden section inside Terms or Privacy.

### Required content model

1. exact app name and MintTap/developer identity;
2. clear heading: account deletion;
3. whether the user can complete deletion on the page or how to initiate the request;
4. authentication / identity-verification steps;
5. what the deletion removes;
6. what data, if any, must be retained and why;
7. expected processing time if not immediate;
8. how completion is confirmed;
9. subscription/billing warning and cancellation route when relevant;
10. support fallback for failures, not as an unnecessary barrier to normal deletion;
11. link back to the governing privacy policy.

### Interaction rule

Account deletion is destructive. The UI must use explicit language, a deliberate confirmation step and clear consequences. It must not use deceptive friction, hidden controls or ambiguous labels such as only "Deactivate" when the policy requirement is deletion.

### Optional Apple privacy-choice mapping

If an app later has several privacy controls, create a broader data/privacy-control page and consider using it as Apple's optional User Privacy Choices URL. The dedicated deletion URL should still remain stable when Google requires it.

---

## 6. SOURCE — Support web requirements

### Apple

The App Store Support URL is required and localizable. Apple says it must lead to actual contact information so users can reach the developer about app problems, general feedback and feature requests; legal address, email and telephone information may be required under local law.

### Google Play

An app support/contact email is required on the Play Store listing. Google also strongly recommends a website and recommends help/FAQ content and additional contact options.

### MINTTAP DECISION — Per-app support page

Use:

`/apps/<app-slug>/support/`

as the preferred Apple Support URL and Google Play website/support destination for that app.

Content model:

1. app identity and short support scope;
2. common help / FAQ links;
3. current high-impact known issue notice only when necessary;
4. contact/support method;
5. feedback / feature-request route if supported;
6. privacy link;
7. account-deletion/data-control link when applicable;
8. company/legal contact information required for the launch region;
9. accessibility/contact alternative where the primary support channel fails.

Company `/support/` acts as a routing hub to app-specific support pages rather than replacing them.

---

## 7. MINTTAP DECISION — One underlying "App Data Contract"

The highest operational risk is not missing prose. It is **inconsistency** between app behavior, website policy, App Store App Privacy and Google Play Data safety.

Each app should therefore have one maintained internal data contract that is the source for all public/privacy disclosures.

Minimum fields:

- canonical app name / slug;
- Apple bundle ID;
- Android package name;
- Apple/Google store-facing developer identity;
- account creation: yes/no;
- guest/automatic account creation: yes/no;
- authentication providers;
- Sign in with Apple usage;
- user data types;
- collection source/method;
- required vs optional collection;
- processing purpose;
- off-device transmission;
- first-party storage/services;
- third-party SDK/processors;
- sharing/recipient categories;
- retention/deletion rules;
- account-deletion implementation and URL;
- subscription/IAP presence;
- support URL/contact;
- privacy URL/contact;
- App Store privacy disclosure owner/date;
- Google Data safety owner/date;
- last technical audit date.

The exact storage format (YAML/JSON/other) will be selected when app inventory integration begins.

---

## 8. CONSISTENCY / RELEASE CONTROL

A privacy-impacting app change must trigger a disclosure review before release.

Triggers include:

- adding/removing an SDK;
- changing analytics or advertising;
- new authentication/account behavior;
- new data field or permission;
- new server-side processing;
- new sharing/processor;
- retention/deletion change;
- subscription/account-deletion interaction change;
- company/developer identity or privacy contact change.

### Release check

For each affected app compare:

1. actual app/client behavior;
2. backend/server behavior;
3. SDK/vendor behavior;
4. app privacy page;
5. in-app privacy link/disclosure;
6. Apple App Privacy answers;
7. Google Data safety answers;
8. account-deletion page/flow;
9. support page/contact information.

No surface should be treated as authoritative in isolation; the technical data contract is the reconciliation source.

---

## 9. VALIDATION GATES BEFORE PRODUCTION PASS

### Privacy URL
- HTTPS and stable canonical URL;
- publicly reachable;
- no login requirement;
- no geo-blocking for Google Play policy;
- HTML/web-readable rather than PDF for Google Play;
- app/developer identity visibly matches store identity;
- link works from app and store metadata;
- mobile/narrow viewport readable;
- language version matches submitted localized metadata where provided.

### Account deletion
- page reachable after app uninstall;
- pathway to request/complete deletion is immediately discoverable;
- no forced app reinstall;
- identity verification works;
- destructive confirmation is understandable;
- retained-data explanation matches real backend behavior;
- processing-time statement is true;
- completion notification works when promised;
- subscription handling is accurate;
- keyboard/focus/error/recovery behavior is validated.

### Support
- support URL returns a useful app-specific page;
- contact route is operational and monitored;
- app name is unambiguous;
- privacy/deletion routes are not broken;
- localized contact/help content is valid where submitted.

---

## 10. OPEN / DEPENDENCIES

- MintTap's exact legal entity and public privacy/support contacts are not yet recorded.
- Current app inventory and account-creation behavior are not yet mapped.
- SDKs, analytics, advertising, authentication and processors are not yet mapped per app.
- Jurisdiction-specific privacy-law requirements still require separate research/legal review.
- Final support response SLA/escalation workflow is not defined.
- Final deletion backend behavior and identity-verification method are app-specific.
- Website hosting architecture is not yet selected, so URL uptime/deployment controls remain unvalidated.

---

## 11. CHANGE WATCH

Recheck before launch and periodically afterward:

- Apple App Review Guidelines 5.1.1;
- Apple App Store Connect App Privacy fields;
- Apple account-deletion guidance;
- Google Play User Data policy;
- Google Play account-deletion web-resource rules;
- Google Play Data safety form requirements;
- store support/contact metadata requirements.

Policy text and Console fields can change independently of this repository.

---

## 12. PROJECT-READINESS RESULT

After this study, Web Manager should be able to answer for a new MintTap app:

- Which privacy/support/deletion URLs are needed?
- Which content is platform-required vs MintTap operational structure?
- Whether the app needs an external deletion resource?
- What fields engineering/product must supply before privacy copy can be considered accurate?
- Which app/store/web surfaces must be reconciled before release?
- What must be revalidated when the app's data behavior changes?

Foundation status remains below PASS until the model is applied to at least one real MintTap app and its technical behavior, store disclosures and website pages are cross-validated.