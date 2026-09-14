# 001 — App Launch Website Foundations

Checked: 2026-09-14
Scope: MintTap company/developer website for iOS App Store and Google Play launches.

## Research question

What must `minttap.app` be capable of providing before it can reliably support Apple and Android app launches, and what belongs to the website manager rather than the app itself?

## RELATED DESIGN STUDIO CHECK

Design Studio governance and Web Design status were reviewed before this study.

Reusable conclusions:
- Web work must integrate Type, Color, Layout/Interaction rather than act as a final styling pass.
- Real browser/device validation matters; static design alone is insufficient.
- Project-specific decisions belong in the project repository and should not silently become universal Design Studio rules.
- Research volume is not a success metric; the test is whether the finding changes or improves a real product decision.

Canonical dependency: `yhappcom/design-studio`, especially `AGENTS.md`, `progress/WEB_STATUS.md`, `research/web/README.md`, `coordination/COLLABORATION_PROTOCOL.md`, and `methods/PROJECT_ENGAGEMENT.md`.

## SOURCE — Apple App Store

### Privacy policy
Apple App Store Connect states that a Privacy Policy URL linking to the company's privacy policy is required for all apps. App privacy declarations must also accurately represent data practices, including relevant third-party partners.

Sources:
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy
- https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy

### Support URL
Apple's platform-version metadata requires a Support URL. Apple states that the URL must lead to actual contact information so users can reach the developer regarding issues, feedback and feature requests.

Source:
- https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information

### Marketing URL
Apple provides a Marketing URL field for a website where users can learn more about the app. This is distinct from the Support URL.

Source:
- https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information

### Account deletion
If an app supports account creation, Apple requires account deletion to be available within the app. This is primarily an app requirement, but the website manager must keep privacy/data-control documentation synchronized with it.

Sources:
- https://developer.apple.com/app-store/review/guidelines/
- https://developer.apple.com/support/offering-account-deletion-in-your-app

### Korea-specific developer information
Apple collects and displays specified developer identification information for developers based in South Korea. This is App Store compliance data rather than a substitute for the website's support/legal surfaces.

Source:
- https://developer.apple.com/kr/help/app-store-connect/manage-compliance-information/manage-korea-compliance-information

## SOURCE — Google Play

### Privacy policy and Data safety
Google Play requires published apps to complete the Data safety form. Even apps that do not collect user data must complete the form and provide a privacy-policy link. Google policy also requires a comprehensive privacy policy accessible in the app and linked in Play Console.

Sources:
- https://support.google.com/googleplay/android-developer/answer/10787469
- https://support.google.com/googleplay/android-developer/answer/10144311

### Support/contact presence
Google Play requires a contact email for the store listing and strongly recommends a website for user support. Google recommends web-based FAQ/help content and clear additional contact options.

Sources:
- https://support.google.com/googleplay/android-developer/answer/9859152
- https://support.google.com/googleplay/android-developer/answer/113477

### External account-deletion resource
If an app allows account creation, Google Play requires users to be able to request account deletion both inside the app and outside the app through a designated web resource. The external URL is entered in Play Console.

Source:
- https://support.google.com/googleplay/android-developer/answer/10144311

## SOURCE — App ↔ website trust files

### Apple associated domains / Universal Links
Apple uses an `apple-app-site-association` file hosted on the HTTPS website together with the app's Associated Domains entitlement. Depending on supported services it can underpin Universal Links and other associated-domain features.

Sources:
- https://developer.apple.com/documentation/Xcode/supporting-associated-domains
- https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html

### Android App Links
Android verified App Links require a Digital Asset Links file named `assetlinks.json` at `https://<domain>/.well-known/assetlinks.json`. Google documentation requires HTTPS, `application/json`, and no redirects for verification. Android 15+ can also use the file for dynamic App Link rules.

Sources:
- https://developer.android.com/training/app-links/configure-assetlinks
- https://developer.android.com/training/app-links/about

## SOURCE — Advertising verification

Google AdMob documents `app-ads.txt` as not mandatory but highly recommended. It must be publicly crawlable and published at the root of the developer website used in the app listing when used for authorized-seller verification.

Source:
- https://developers.google.com/admob/android/next-gen/app-ads

## SYNTHESIS — What `minttap.app` must become

`minttap.app` should be treated as operational launch infrastructure, not merely a promotional landing page. A durable baseline should support:

1. company/developer identity;
2. per-app product/marketing information;
3. user support and contact;
4. privacy policy and data-practice communication;
5. account/data-control web routes when applicable;
6. store download destinations;
7. app↔domain association files when deep linking/associated-domain features are used;
8. advertising verification files when monetization requires them;
9. localization, accessibility and responsive presentation;
10. release-time validation, broken-link monitoring and policy-change review.

## SYNTHESIS — Required separation of concerns

Do not collapse all store-facing URLs into one generic page.

A professional site architecture should preserve distinct user intents:
- marketing/product understanding;
- support/contact;
- privacy/data practices;
- account/data controls;
- legal terms/notices;
- machine-readable verification files.

Pages may share navigation and visual design, but their purpose, ownership and change triggers differ.

## MINTTAP DECISION — Foundation operating direction

Before production design begins, Web Manager will build requirements and knowledge in layers:

1. platform/store compliance surfaces;
2. company/product information architecture;
3. privacy/support/account-control content model;
4. domain/hosting/security and machine-readable verification;
5. Design Studio integration for typography, color, layout, interaction and responsive behavior;
6. localization/accessibility/SEO;
7. release operations and monitoring.

## OPEN

The following cannot be finalized from platform research alone:

- which MintTap apps require account deletion pages;
- exact personal/user/device data handled by each app;
- third-party SDKs and processors;
- final support email/phone/address and legal entity details;
- advertising networks and publisher IDs;
- Universal/App Link route map;
- launch jurisdictions and resulting legal obligations;
- hosting/CDN/DNS architecture.

## VALIDATION

At release time, policy-sensitive findings in this study must be rechecked against current Apple/Google documentation. URLs must be tested as public, HTTPS, non-broken resources, and machine-readable association files must be validated from real target devices/platform tooling.

## HANDOFF TO DESIGN STUDIO

Future MintTap implementation may provide real-browser transfer evidence for:
- Type: font loading, fallback, localization, zoom and text growth;
- Color: browser/device/theme and accessibility behavior;
- Layout/Interaction: responsive recomposition, navigation, focus, input and async state behavior;
- Web Design: complete production page-system validation.

Such findings remain MintTap-specific here until there is enough evidence to justify reusable transfer back to Design Studio.
