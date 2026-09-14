# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve a real MintTap decision, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Evidence labels

Use as appropriate:

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved question.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail that requires later re-checking.

## Completed studies

### 001 — App Launch Website Foundations
`001-app-launch-website-foundations.md`

Establishes the website's role in Apple/Google app launch operations: privacy, support, account deletion, app↔web association, advertising verification and release-time revalidation.

### 002 — Multi-App Company Website Information Architecture
`002-multi-app-information-architecture.md`

Establishes the scalable company/app/support/governance hierarchy, canonical per-app paths, URL rules, navigation baseline, accessibility/wayfinding consequences and app-page search/structured-data direction.

### 003 — Privacy, Support & Account-Deletion Content Architecture
`003-privacy-support-account-deletion-architecture.md`

Establishes Apple/Google policy-backed per-app privacy, support and account-deletion surfaces; required content models; a shared internal App Data Contract; release consistency triggers; and validation gates. It deliberately separates platform policy from later jurisdiction-specific legal analysis.

### 004 — App Store / Google Play ↔ Website Content Synchronization
`004-store-website-content-synchronization.md`

Establishes a Product Truth Record, channel-specific copy model, screenshot evidence set, Content Release Manifest, localization synchronization, ownership boundaries and discrepancy severity so store metadata and `minttap.app` remain factually aligned without requiring identical wording.

### 005 — Domain, Hosting & Security Baseline
`005-domain-hosting-security-baseline.md`

Defines a provider-independent production contract for `minttap.app`: modern TLS/HTTPS, staged HSTS, redirect strategy, exact Apple/Android association-file hosting, cache classes, browser security-header direction, DNSSEC/CAA, deployment/secrets requirements, observability and hosting/CDN acceptance gates.

### 006 — Accessibility Production Baseline
`006-accessibility-production-baseline.md`

Adopts WCAG 2.2 AA as MintTap's internal production baseline and defines semantic structure, landmarks/headings, native controls, keyboard/focus behavior, 320px-equivalent reflow, 200% text enlargement, pointer-target floors, form/error/status behavior, language metadata and automated/manual/assistive-technology validation gates for launch-critical web surfaces.

### 007 — Localization Architecture
`007-localization-architecture.md`

Establishes Korean/English-first localization architecture with locale-specific URLs, HTML language declarations, reciprocal hreflang, self-canonical locale pages, a Locale Matrix and Localization Manifest, website/store/app-locale separation, translation invalidation triggers, language-switcher behavior and release gates. It explicitly leaves real Korean/English typography/browser proof open for Design Studio and production validation.

## Current research queue

See root `STATUS.md` for the authoritative next-work queue. Current high-value areas include:

1. SEO/social/structured-data/crawlability;
2. company/app marketing content model;
3. operational release and change-watch controls;
4. jurisdiction-specific legal/compliance web requirements when launch regions and app data practices are known;
5. implementation/provider selection after the evidence baseline is mature enough to compare real options;
6. real browser Korean/English typography, localization and accessibility transfer validation when production implementation exists.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web decisions and production findings stay here first.

Relevant Design Studio domains:
- Typography / Type Design;
- Color;
- Layout / Spatial & Interaction;
- Web Design.

When MintTap production work confirms, limits or contradicts a reusable Design Studio claim, record the MintTap evidence here and hand it back to the appropriate specialist when justified.
