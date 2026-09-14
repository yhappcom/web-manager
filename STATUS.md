# MintTap Web Manager Status

Operating state: **ACTIVE — FOUNDATION RESEARCH**
Last sync: 2026-09-14
Domain: `minttap.app`
Platforms: iOS / App Store, Android / Google Play

## Mission state

The web manager has been appointed as the owner of MintTap's company website content and app-launch web requirements. Production site work has not yet been assigned; current priority is building a reliable professional foundation.

## Completed foundation work

- Confirmed Design Studio governance and the Web Design specialist's integration role.
- Confirmed that MintTap-specific website decisions belong here while reusable design research remains in `yhappcom/design-studio`.
- Opened the first app-launch website research block covering Apple, Google Play, app↔web association, support/privacy/account deletion, and advertising verification.

## Current maturity

Stage: **Foundation**
State: **IN STUDY**

Reading alone does not constitute completion. Store-policy findings require source tracking and later launch-time revalidation.

## Initial requirement map

### Launch-critical / policy-facing
- Company/product website on `minttap.app`.
- Public privacy policy URL.
- Apple Support URL with real contact information.
- Google Play support/contact website presence.
- External account-deletion web resource for Google Play when an app allows account creation.
- Privacy disclosures synchronized with Apple App Privacy and Google Play Data safety declarations.

### Platform/domain infrastructure when used
- Apple `apple-app-site-association` for Universal Links / associated domains.
- Android `/.well-known/assetlinks.json` for verified App Links.
- Root `app-ads.txt` when app advertising inventory requires it; not universally mandatory, but strongly recommended by Google AdMob.

### Company/product web surfaces to study and design
- Home/company identity.
- Per-app product/marketing pages.
- Support/help/FAQ.
- Contact.
- Privacy.
- Terms/legal notices where applicable.
- Account/data controls where applicable.
- App Store / Google Play download destinations.
- Localization and accessibility.
- SEO/search previews/social metadata.
- Release/update/freshness ownership.

## Important open items

- Exact MintTap legal entity/public contact details are not yet established in this repository.
- Exact app inventory and which apps create accounts are not yet mapped here.
- Exact analytics, advertising SDKs, authentication providers, data collection and third-party processors are not yet mapped.
- Hosting/CDN/SSL/DNS implementation has not yet been selected or audited.
- Universal/App Link routes are not yet defined.
- `app-ads.txt` publisher/vendor lines cannot be finalized until monetization vendors and IDs are known.
- Jurisdiction-specific legal pages beyond store/platform requirements need separate legal/compliance review when launch regions are fixed.

## Next research queue

1. Website information architecture for a multi-app developer/company site.
2. Privacy/support/account-deletion page content architecture and consistency controls.
3. Apple/Google store metadata ↔ website content synchronization.
4. Domain/hosting/security baseline for `minttap.app`.
5. Accessibility, localization, responsive content and design integration with Design Studio.
6. SEO, social sharing, structured data and crawlability for app/company pages.
7. Operational checklist for release, policy change watch and broken-link/verification monitoring.
