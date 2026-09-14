# 026 — App-Company Web Strategy, Information Hierarchy & Conversion Path

Status: **FOUNDATION / KNOWLEDGE STUDY**
Research date: 2026-09-14

## Why this study exists

Studies 001–025 built strong launch, policy, security, release and hosting knowledge, but recent work drifted too far toward implementation/POC preparation. The Web Manager's standing objective is broader professional knowledge for planning, evaluating and operating real app-company websites. Implementation experiments are supporting validation only, not the curriculum destination.

This study resets the center of gravity toward the visitor-facing website: what a company/app page must communicate, how information should be ordered, and how the website relates to App Store / Google Play conversion.

## SOURCE — current primary guidance

### Apple: first-contact product communication

Apple's current App Store asset guidance says product assets set expectations before download and should communicate the app's value/story. For product-page headers Apple recommends one clear idea and designing for a first-time visitor. Apple also supports product-page optimization tests and custom product pages for audience-specific acquisition paths.

Sources:
- https://developer.apple.com/app-store/asset-best-practices/
- https://developer.apple.com/help/app-store-connect/create-product-page-optimization-tests/overview-of-product-page-optimization
- https://developer.apple.com/app-store/

### Google Play: value must be clear, concise and accurate

Google Play's current store-listing guidance says users use the listing to learn about an app and decide whether to try it. Descriptions must accurately describe functionality; the short description should summarize the biggest benefits; wording should be succinct and straightforward because users may only read the first few sentences. Store graphics should remain consistent, avoid misleading claims and focus on useful product communication.

Source:
- https://support.google.com/googleplay/android-developer/answer/13393723

### W3C: hierarchy is functional, not merely visual

W3C WAI states that well-structured content improves navigation and orientation. Headings communicate content organization and can provide in-page navigation; clear/consistent navigation, headings, spacing and meaningful link text improve both accessibility and comprehension. Responsive design must consider how information is presented at different viewport sizes rather than merely shrinking a desktop layout.

Sources:
- https://www.w3.org/WAI/tutorials/page-structure/
- https://www.w3.org/WAI/tutorials/page-structure/headings/
- https://www.w3.org/WAI/tips/designing/
- https://www.w3.org/WAI/tips/writing/

### Google web.dev: performance is part of the delivered experience

Current Core Web Vitals measure loading, interaction responsiveness and visual stability. Recommended good thresholds remain LCP <= 2.5 s, INP <= 200 ms and CLS <= 0.1, evaluated at the 75th percentile separately for mobile and desktop. Therefore marketing-page visual ambition has an experiential cost that must be considered during design, not after it.

Source:
- https://web.dev/articles/vitals

## SYNTHESIS — website and store are different stages of one acquisition path

An app-company website should not be treated as a larger copy of the App Store / Play listing. The store listing has platform-defined structure and the final install context. The website has broader jobs:

1. establish who/what the product is;
2. match the visitor's problem or intent to the product;
3. explain differentiated value with enough evidence to reduce uncertainty;
4. let the visitor inspect features, screenshots, trust/support/privacy information when needed;
5. route the visitor to the correct store/product destination with minimal ambiguity;
6. support existing users who arrived for help, privacy, account or company information rather than acquisition.

The site therefore needs explicit **audience × intent × destination** mapping before visual composition.

## MINTTAP DECISION — four visitor intents

Until real product research proves otherwise, future MintTap company/app website planning should explicitly test at least four intent classes rather than assume every visitor is a prospective downloader:

- **DISCOVER** — What is this app/company and is it relevant to me?
- **EVALUATE** — Why should I trust/use it? What exactly does it do?
- **ACT** — Download/open/contact/continue to the appropriate destination.
- **SUPPORT / GOVERNANCE** — Get help, privacy/account-deletion/legal/company information.

These are planning categories, not claims about measured MintTap users. Real analytics/user evidence can change them.

## SYNTHESIS — app landing-page information hierarchy

A reusable default reasoning sequence for a new app page is:

### 1. Identity + value
The opening viewport should allow a first-time visitor to identify the product and its primary value without decoding feature jargon. One clear proposition is preferable to competing headline messages.

### 2. Primary action
The appropriate next action should be visible and unambiguous. For a released consumer app this may be store acquisition; for pre-release, waitlist or information may be appropriate. CTA wording must describe the destination/action, not generic `Learn more` where a more meaningful label exists.

### 3. Product evidence
Use actual product UI, screenshots, demonstrations or factual examples to substantiate the proposition. Website claims remain governed by Product Truth / Claim Registry from earlier studies.

### 4. Differentiated capabilities
Explain a small set of capabilities through user outcomes, not an exhaustive feature inventory. Detailed features can follow after the core proposition is established.

### 5. Trust / uncertainty reduction
Surface the trust evidence relevant to the product: developer identity, privacy/data handling, support, factual endorsements/recognition if verified, platform availability, pricing/account facts where appropriate.

### 6. Secondary paths
Existing-user support, privacy, account deletion, company information and other governance destinations remain findable without competing visually with the primary acquisition task.

### 7. Repeated contextual action
For a long page, repeat the primary action after enough evidence has been provided rather than requiring a return to the hero.

This is a **starting model**, not a mandatory fixed section order. Product/audience/task evidence can justify recomposition.

## MINTTAP DECISION — hierarchy before decoration

Before asking Design Studio for visual styling of a MintTap page, Web Manager should provide:

- page purpose;
- target audience / known evidence;
- visitor intents;
- primary and secondary actions;
- required factual claims and evidence;
- required support/privacy/legal destinations;
- page information hierarchy;
- content that must survive narrow widths and localization;
- store destination(s) and platform conditions;
- performance/accessibility constraints.

Design Studio then owns how that hierarchy is expressed through typography, color, layout, interaction and visual identity.

## MINTTAP DECISION — website/store message continuity

The website and store page do not need identical copy or composition, but they must preserve a recognizable message chain:

**acquisition source → website proposition/evidence → store proposition/assets → installed product reality**.

A visitor should not encounter a materially different promise after moving from website to store. Earlier Product Truth controls remain the factual authority.

## Responsive hierarchy rule

Responsive design is not `desktop page scaled down`. At narrower widths:

- preserve product identity and primary proposition;
- preserve the primary action;
- preserve essential evidence;
- recompose navigation and secondary information according to available space;
- avoid hiding required support/privacy/governance access;
- maintain semantic heading/region structure;
- test Korean/English expansion and text zoom as content conditions, not edge cases.

This rule aligns with W3C's guidance to consider how main information/navigation are presented across viewport sizes.

## Performance as a content/design constraint

Large hero video, autoplay media, excessive web fonts, animation and oversized screenshots may weaken the very first-contact experience they are intended to improve. Future page concepts should identify their likely LCP element, layout-shift risks and interaction cost during design review. Core Web Vitals are not the complete UX, but they are a useful production constraint.

## OPEN — evidence still required before real MintTap page design

- actual MintTap corporate positioning;
- real app inventory and launch state;
- audience/persona or behavioral evidence per app;
- acquisition channels and traffic mix;
- primary conversion definition per app;
- pricing/account model;
- verified trust signals;
- store-page assets and current messaging;
- analytics baseline;
- competitor/alternative context.

Do not invent these from generic app-company patterns.

## DESIGN STUDIO HANDOFF

This study provides **content hierarchy and task requirements**, not a visual template.

Future Web Design work should test:
- whether first-time visitors can identify product/value/action;
- whether hierarchy survives desktop → narrow mobile recomposition;
- whether Korean/English text changes disturb scan order;
- whether app screenshots remain legible and useful rather than decorative;
- whether CTA, support and governance paths remain distinct;
- whether Type/Color/Layout evidence preserves semantic hierarchy without color-only meaning;
- whether visual ambition harms LCP/CLS/interaction.

## CHANGE WATCH

Apple/Google store presentation, marketing asset formats, optimization tools and metadata policy can change. Recheck official platform guidance when a real app launch begins.

## Next knowledge gaps

High-value study should now continue across visitor-facing web expertise rather than provider POC work:

1. app-company / multi-product website IA and navigation decision models;
2. landing-page content strategy, evidence and conversion without manipulative dark patterns;
3. trust architecture for an unknown/small app developer;
4. support/FAQ/self-service information architecture;
5. responsive content hierarchy and mobile-first recomposition;
6. performance-aware marketing design / Core Web Vitals;
7. analytics and measurement framework for company/app sites;
8. systematic precedent/critique method for real app-company websites.
