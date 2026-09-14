# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve a real MintTap decision, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved question.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed studies

### 001 — App Launch Website Foundations
`001-app-launch-website-foundations.md`

Apple/Google launch web requirements: privacy, support, account deletion, app↔web association, advertising verification and policy revalidation.

### 002 — Multi-App Company Website Information Architecture
`002-multi-app-information-architecture.md`

Company → apps → app → support/control/governance hierarchy, canonical per-app paths, URL/navigation baseline.

### 003 — Privacy, Support & Account-Deletion Content Architecture
`003-privacy-support-account-deletion-architecture.md`

Per-app privacy/support/account-deletion surfaces, App Data Contract and cross-surface disclosure consistency.

### 004 — App Store / Google Play ↔ Website Content Synchronization
`004-store-website-content-synchronization.md`

Product Truth Record, Screenshot Evidence Set, Content Release Manifest and factual synchronization rules across stores/web.

### 005 — Domain, Hosting & Security Baseline
`005-domain-hosting-security-baseline.md`

Provider-independent HTTPS/TLS, verification-file, caching, security-header, DNS, secret, rollback and monitoring contract.

### 006 — Accessibility Production Baseline
`006-accessibility-production-baseline.md`

WCAG 2.2 AA internal target, semantic structure, keyboard/focus, reflow, text enlargement, forms/status and manual validation gates.

### 007 — Localization Architecture
`007-localization-architecture.md`

Korean/English-first locale URLs, HTML language, reciprocal hreflang, Locale Matrix, Localization Manifest and translation invalidation controls.

### 008 — SEO, Structured Data, Sitemap, Canonical & Crawlability
`008-seo-structured-data-crawlability.md`

Canonical/hreflang, robots/sitemap, crawlability, conservative structured data and Search Console production validation.

### 009 — SEO Independent Verification & Social Preview Metadata
`009-seo-independent-verification-social-preview.md`

Independent check of 008, public/noindex/private classes, robots vs noindex, localized title/description and Product-Truth-governed Open Graph baseline.

### 010 — Company / App Marketing Content Model
`010-company-app-marketing-content-model.md`

Product-Truth-governed marketing, Claim Registry, content hierarchy, evidence/screenshots, trust/store CTA, price/subscription and claim staleness controls.

### 011 — Operational Release & Change-Watch Controls
`011-operational-release-change-watch-controls.md`

Connects Studies 003–010 into a continuous operating loop. Establishes Policy Change Register, Operational Surface Registry, deploy/scheduled/event/human watch layers, pre/post-release gates, P0/P1/P2 incident severity, AASA/App Links/app-ads propagation handling, policy notification continuity, ownership/bus-factor controls and freshness/invalidation dependencies.

## Current research queue

See root `STATUS.md` for the authoritative next-work queue. Highest-value next work is now:

1. implementation/provider comparison methodology and candidate scoring for hosting/CDN/CMS/framework/deployment/monitoring;
2. jurisdiction-specific legal/compliance web requirements once entity, launch regions and actual data practices are known;
3. real-browser Korean/English typography/localization/accessibility/search/social/marketing transfer validation once production implementation exists;
4. app-specific user/market evidence when actual product pages are assigned.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web decisions and production findings stay here first.

Relevant Design Studio domains:
- Typography / Type Design;
- Color;
- Layout / Spatial & Interaction;
- Web Design.

When MintTap production work confirms, limits or contradicts a reusable Design Studio claim, record the MintTap evidence here and hand it back to the appropriate specialist when justified.
