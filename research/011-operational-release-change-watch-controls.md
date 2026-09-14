# 011 — Operational Release & Change-Watch Controls

Status: **FOUNDATION STUDY / OPERATING MODEL ESTABLISHED; AUTOMATION NOT YET IMPLEMENTED**  
Research date: **2026-09-14**

## Question

How should MintTap operate `minttap.app` after launch so store-policy changes, broken required URLs, app↔web verification failures, stale privacy/support/marketing content, indexing mistakes and expired evidence are detected before they become app-review, user-trust or distribution problems?

This study establishes the operational control model. It does not claim production PASS because no hosting/provider, monitoring stack, live app inventory or real release pipeline has yet been implemented.

---

## RELATED DOMAIN CHECK

### Existing Web Manager evidence

- Study 003 established privacy/support/account-deletion surfaces and the App Data Contract.
- Study 004 established Product Truth, Screenshot Evidence Set and Content Release Manifest.
- Study 005 established hosting/security/verification-file requirements.
- Study 007 established Locale Matrix and Localization Manifest.
- Studies 008–009 established search/social operational state.
- Study 010 established Claim Registry and content/claim invalidation triggers.

This study does not repeat those contracts. It connects them into one release/freshness control loop.

### Design Studio

- **Web Design** remains the production validation owner for actual pages/browser behavior. Its current status is still Foundation / no substantive W### baseline.
- **Layout / Interaction** now has controlled evidence for errors, pending states, recovery and interruption. Those principles transfer to any user-facing maintenance/error/account-control state, but monitoring itself remains Web Manager operations.
- Type/Color become relevant when operational fallbacks, banners or maintenance/error states are rendered in production.

---

# SOURCE — platform policies are moving targets

Apple revised its App Review Guidelines on **2026-06-08** and its current guideline page records that date as the last update. Apple also maintains an Upcoming Requirements page for submission/SDK and other time-bound requirements.

Primary sources:
- https://developer.apple.com/news/?id=a233fmpw
- https://developer.apple.com/app-store/review/guidelines/
- https://developer.apple.com/news/upcoming-requirements/

Google Play explicitly states that Developer Program Policies are regularly updated and maintains both a current **Policy Deadlines** table and a historical Policy Archive. As of this research date the deadlines page includes a **2026-09-30** Play Console requirement and later 2027 policy deadlines.

Primary sources:
- https://support.google.com/googleplay/android-developer/table/12921780
- https://support.google.com/googleplay/android-developer/answer/13386702
- https://support.google.com/googleplay/android-developer/announcements/13412212

### SYNTHESIS

A release checklist that contains policy text copied once into a repository will decay.

MintTap needs to separately record:
1. what rule currently applies;
2. when it was last checked;
3. when a new rule was announced;
4. its effective/deadline date;
5. which apps/surfaces are affected;
6. who owns remediation;
7. whether production has been revalidated.

### MINTTAP DECISION — Policy Change Register

Maintain a **Policy Change Register** with at least:
- platform/source;
- source URL;
- announcement date;
- effective/deadline date;
- affected app(s);
- affected product/data/content/infrastructure surface;
- impact assessment;
- owner;
- required action;
- release/blocking severity;
- verification evidence;
- status (`NEW`, `ASSESSED`, `ACTION REQUIRED`, `VERIFIED`, `NOT APPLICABLE`, `SUPERSEDED`);
- last checked date.

Do not silently overwrite old policy records. Preserve the historical decision trail.

---

# SOURCE — Google Play supports policy communication to organizational recipients

Google Play Console supports **email recipients** who can receive policy communications without being granted Play Console access. Google recommends adding recipients to all relevant topics and prefers groups so notifications continue when employees change.

Primary source:
- https://support.google.com/googleplay/android-developer/answer/15771712

### MINTTAP DECISION

Policy notifications must not depend on one person's inbox.

When organizational email infrastructure exists:
- create a durable distribution/group address for app-store policy/operations;
- subscribe it to Google Play **Policy** communications;
- document at least two responsible humans/roles behind the group;
- review membership/access periodically.

Until a group exists, this remains an OPEN operational dependency.

---

# SOURCE — Apple app-status changes can be event driven

App Store Connect supports webhooks for changes including build-upload status, beta-build status and app-version status. A webhook is configured with a secret that the receiving server uses to verify authenticity. Apple also exposes app/submission statuses and status history in App Store Connect.

Primary sources:
- https://developer.apple.com/help/app-store-connect/manage-your-team/manage-webhooks
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-and-submission-statuses
- https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/view-app-status-history

### MINTTAP DECISION

When MintTap has a production operations backend, prefer App Store Connect webhooks for relevant status transitions instead of depending only on manual polling.

Operational requirements:
- verify webhook authenticity using the configured secret;
- persist event ID, event type and receipt/result;
- make processing idempotent;
- alert on repeated delivery failures;
- periodically send/test a webhook to prove the integration still works;
- keep manual App Store Connect status/history inspection as a fallback.

Webhooks are app-scoped; ownership and routing must be documented per app.

---

# SOURCE — Apple associated-domain updates have propagation delay

Apple states that the associated-domains CDN requests an `apple-app-site-association` file for a domain within **24 hours**, and devices check for updates approximately **once per week after app installation**.

Primary source:
- https://developer.apple.com/documentation/Xcode/supporting-associated-domains

### MINTTAP DECISION

AASA operational health has two different states:

1. **origin health** — is MintTap serving the correct direct HTTPS file now?
2. **ecosystem convergence** — have Apple CDN/devices refreshed the new association yet?

A successful origin check does **not** prove immediate client convergence.

When materially changing AASA routes/app IDs:
- deploy before the app release when possible;
- validate direct production response first;
- test on representative devices/install states;
- avoid same-minute website + app rollout assumptions;
- record the effective association-file revision in the Content Release Manifest.

---

# SOURCE — Android App Links are verifiable and dynamic rules are periodically refreshed

Android fetches `https://<host>/.well-known/assetlinks.json` for App Links verification. Android's official tooling supports forced re-verification and inspection of per-domain verification state. On Android 15+ with Google services, Dynamic App Link rules can be periodically re-fetched from `assetlinks.json`.

Primary sources:
- https://developer.android.com/training/app-links/verify-applinks
- https://developer.android.com/training/app-links/test-applinks
- https://developer.android.com/training/app-links/configure-assetlinks

### MINTTAP DECISION

A valid HTTP response alone is insufficient for an App Links change.

For every release/change involving Android App Links:
- verify direct HTTPS `200`;
- verify `Content-Type: application/json`;
- verify no redirect;
- verify package name and signing fingerprint against the actual release configuration;
- use Digital Asset Links / Android tooling to confirm association;
- on a test device, force re-verification when appropriate and confirm state = `verified`;
- test at least one intended URL end-to-end.

Dynamic rules are treated as live production configuration and therefore require the same change-review discipline as application routing.

---

# SOURCE — app-ads.txt external reflection is not immediate

Google AdMob states that `app-ads.txt` changes may take several days to appear in AdMob, and for apps with low ad-request volume can take up to a month. Google also requires the file to remain crawlable, return `200`, and not be blocked by robots.

Primary sources:
- https://support.google.com/admob/answer/9679128
- https://developers.google.com/admob/android/next-gen/app-ads

### MINTTAP DECISION

Monitor two separate states:
- **origin correctness** — current file is reachable and correct;
- **AdMob/exchange recognition** — external systems have refreshed it.

Do not roll back a correct file merely because AdMob has not reflected the change immediately. Record the change timestamp and expected propagation window first.

---

# SOURCE — Google Search itself publishes a change feed

Google Search Central maintains a documentation update log and publishes an RSS feed for changes. Supported search features can be added, changed or removed; for example, documentation entries in 2026 include structured-data feature changes/removals.

Primary source:
- https://developers.google.com/search/updates

### MINTTAP DECISION

Search behavior is a **CHANGE WATCH** domain rather than a static SEO configuration.

Subscribe the operations workflow to the Search Central update feed when implementation begins. Only changes relevant to MintTap's actual schema/crawl/indexing setup create action items.

---

# OPERATIONAL CONTROL MODEL

## 1. Operational Surface Registry

Maintain one registry of every production-critical public/machine surface.

Minimum fields:
- surface ID;
- app / company scope;
- URL or external console object;
- surface class;
- owner;
- expected HTTP/status/content behavior;
- upstream truth source;
- monitoring method;
- monitoring cadence;
- last successful validation;
- next required review;
- severity if failed;
- remediation/runbook link.

### Initial surface classes

**A — Launch / policy critical**
- app privacy URLs;
- app support URLs;
- account-deletion URLs when required;
- official App Store / Google Play destinations;
- AASA / `assetlinks.json` when used;
- production DNS/HTTPS/certificate path.

**B — Revenue / distribution critical when applicable**
- `app-ads.txt`;
- subscription/pricing disclosures;
- campaign/download destinations.

**C — Discovery / trust critical**
- canonical app pages;
- sitemap/robots/canonical/hreflang;
- Search Console property;
- social-preview metadata/assets;
- company/contact pages.

**D — Evidence freshness**
- Screenshot Evidence Set;
- Claim Registry;
- Localization Manifest;
- Product Truth/App Data Contract revisions.

---

## 2. Risk-based monitoring layers

### Layer 1 — deploy-time validation

Every production deployment affecting web content/configuration runs deterministic checks before and immediately after deploy.

Minimum checks where applicable:
- critical URLs return intended status;
- final host/HTTPS/canonical redirects correct;
- Privacy/Support/Deletion pages render;
- store CTA destinations are correct;
- AASA and `assetlinks.json` direct response requirements pass;
- `app-ads.txt` origin response passes;
- no staging `noindex`/robots rules leaked;
- canonical/hreflang/sitemap production host is correct;
- essential accessibility smoke checks pass;
- changed claims/screenshots/locales have approved upstream evidence.

A deploy cannot be declared successful solely because the hosting platform reports `SUCCESS`.

### Layer 2 — continuous/scheduled synthetic health

Initial MintTap operating direction:
- critical public URLs and machine endpoints: automated recurring health checks, **hourly or better** when a monitoring service is available;
- DNS/TLS/certificate validity: automated warning before expiry/failure;
- store CTA destination availability: daily or release-triggered check;
- sitemap/robots/canonical host sanity: daily after launch, then tune based on change frequency/noise.

These are **MINTTAP operating defaults**, not platform-mandated intervals. Adjust when real reliability data and operating capacity exist.

### Layer 3 — event-driven watches

Examples:
- App Store Connect webhook app/build/version status;
- Google Play policy email/group notifications;
- Search documentation RSS;
- CI/CD deployment event;
- application release/version change;
- SDK/data-processing/auth/ads provider change;
- screenshot or marketing-claim source invalidation.

An event creates an assessment task; it does not automatically imply that every website surface must change.

### Layer 4 — human freshness review

Automated HTTP checks cannot decide whether a page is still truthful.

Recommended initial review rhythm:
- **before every app/store release:** full affected-app Content Release Manifest review;
- **weekly:** policy/deadline/announcement inbox and open policy actions;
- **monthly:** screenshots, Claim Registry expiry, Privacy/Support instructions, store links, locale parity, search/social metadata, broken-link report;
- **quarterly:** account/access ownership, webhook recipients/secrets, Search Console access, registrar/DNS/hosting ownership, monitoring escalation paths and recovery contacts.

These intervals are MintTap governance defaults and should later be tuned from actual release frequency and risk.

---

# RELEASE GATE MODEL

## PRE-RELEASE

For each affected app/version:

1. Product Truth revision approved.
2. App Data Contract reviewed for SDK/data/auth/ads changes.
3. Claim Registry identifies added/changed/invalidated claims.
4. Screenshot Evidence Set reviewed against the actual release build.
5. Locale Matrix / Localization Manifest marks all affected translations current or explicitly unavailable.
6. Privacy/Support/Account Deletion impact assessed.
7. Store metadata and website content impact assessed.
8. AASA/App Links impact assessed.
9. Pricing/subscription/store availability facts verified.
10. Content Release Manifest has an owner for every required change.

## RELEASE-BLOCKING VALIDATION

A release/web publication is blocked when an applicable critical condition is unresolved, including:
- broken required Privacy/Support/Deletion URL;
- material privacy/data disclosure mismatch;
- wrong store destination;
- unsupported/stale payment or availability claim;
- unshipped feature represented as current;
- AASA/App Links verification broken for a release depending on those routes;
- production DNS/TLS/host failure;
- inaccessible launch-critical account/support flow;
- wrong locale/product canonical relationship;
- app UI locale support falsely represented;
- critical screenshot/claim proven stale or misleading.

Search indexing delay, social-card cache delay and app-ads external crawler propagation are **not automatically release blockers** when the production origin is correct and the platform's propagation delay is understood/documented. They may become blockers for a specific campaign/contract that explicitly depends on them.

## POST-RELEASE

Do not close the release at upload time.

Verify:
- App Store / Google Play live product destination after actual publication;
- website CTA reaches live correct listing;
- production app page, support, privacy and deletion surfaces still match released behavior;
- deep links on representative iOS/Android devices when changed;
- production search metadata/canonical/locale output;
- key social preview when campaign/public announcement depends on it;
- monitoring alerts and webhook receivers remain healthy.

Apple notes that an approved app can take up to 24 hours to appear across selected storefronts, so publication confirmation and review-approval are separate operational states.

Primary source:
- https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/overview-of-publishing-your-app-on-the-app-store

---

# INCIDENT SEVERITY

## P0 — USER / DISTRIBUTION CRITICAL

Examples:
- domain/HTTPS outage;
- Privacy/Support/Deletion required URL unavailable during review/release;
- wrong app/store destination causing install failure or material user harm;
- account deletion workflow falsely claims deletion while backend does not perform it;
- material privacy mismatch;
- deep-link verification failure that breaks a core launched user flow.

Action direction: immediate ownership/escalation; freeze related release/content changes until understood.

## P1 — HIGH

Examples:
- stale material price/subscription claim;
- misleading screenshot/claim discovered after publication;
- one locale materially contradicts Product Truth;
- app-ads origin broken for monetized app;
- sitemap/canonical/noindex error materially affecting app pages;
- webhook/policy notification path broken with no fallback owner.

## P2 — NORMAL

Examples:
- non-critical social-preview image stale;
- minor search snippet/title quality issue;
- non-material support article stale while correct current help route remains available.

Severity is based on user/distribution/policy impact, not visual prominence.

---

# FRESHNESS / INVALIDATION GRAPH

Operational state should be dependency-driven rather than calendar-only.

Examples:

**App release changes feature**  
→ Product Truth revision  
→ Claim Registry affected claims stale  
→ Screenshot Evidence Set affected assets stale  
→ website/store/localization/social content review  
→ Content Release Manifest tasks

**SDK / processor changes data flow**  
→ App Data Contract revision  
→ Apple App Privacy / Google Data safety / web privacy review  
→ localized privacy surfaces stale until reviewed

**signing certificate / package / domain changes**  
→ `assetlinks.json` / AASA review  
→ deep-link verification tests  
→ release gate

**store availability/price changes**  
→ Product Truth revision  
→ website CTA / pricing copy / structured data / social campaign review

**policy announcement**  
→ Policy Change Register  
→ affected-app assessment  
→ remediation task or NOT APPLICABLE evidence

---

# MINIMUM AUTOMATION CONTRACT

When implementation begins, monitoring/tooling should be capable of producing machine-readable results for:

- URL/status/redirect assertions;
- TLS/certificate expiry;
- expected content type/body signature for machine files;
- canonical/noindex/hreflang/sitemap sanity;
- store-link HTTP/destination sanity;
- broken internal links;
- deployment revision → validation result association.

Human review remains required for:
- truthfulness of feature/value claims;
- privacy/data meaning;
- screenshot representativeness;
- locale equivalence;
- accessibility beyond automated smoke checks;
- policy applicability;
- user-facing support/account-deletion correctness.

Automation should reduce forgotten checks, not manufacture false PASS states.

---

# OWNERSHIP / BUS FACTOR

No launch-critical operational capability should exist only in one person's account or memory.

Required continuity records when production exists:
- domain registrar owner/recovery;
- DNS/CDN/hosting owner and backup admin;
- Apple Developer / App Store Connect operational roles;
- Google Play Console owner/admin + policy recipients;
- Search Console owners;
- monitoring alert recipients;
- CI/CD credential recovery/rotation procedure;
- support/privacy/contact inbox ownership;
- escalation contact for P0/P1 incidents.

Secrets themselves do **not** belong in this repository. Record ownership/process, not secret values.

---

# CHANGE WATCH SOURCES

Maintain an explicit watch list rather than relying on memory.

## Apple
- App Review Guidelines + revision date;
- Apple Developer News guideline-change announcements;
- Upcoming Requirements;
- App Store Connect status/webhook events;
- Associated Domains documentation when deep linking is used.

## Google Play / Android
- Play Policy Announcements;
- Policy Deadlines;
- Policy Archive;
- Play Console policy email recipients;
- Android App Links documentation if links are used;
- Target API / Play Console requirements applicable to active apps.

## Web / Search / Ads
- Google Search documentation update feed;
- structured-data docs used by MintTap;
- AdMob app-ads.txt status/guidance when monetization is used;
- relevant browser/web standards/security changes when they materially alter the production contract.

A watched source changing is not itself a task-completion signal. It triggers relevance assessment.

---

# HANDOFFS TO DESIGN STUDIO

## Web Design

When production implementation exists, validate user-facing operational states such as:
- 404 / retired app / temporarily unavailable;
- support/contact failure;
- account-deletion pending/success/failure;
- store unavailable in a user's region;
- maintenance/degraded service notice;
- localized fallback behavior.

These states must preserve the normal hierarchy, accessibility, trustworthy content and recovery routes.

## Layout / Interaction

Use existing error/recovery/focus evidence when designing maintenance, submission, account-control and retry states. Operational incident severity does not dictate user-interface composition automatically; interaction should communicate state and recovery accurately.

## Typography / Type

Operational banners, legal notices and support/error strings are future Korean/English long-text/fallback/reflow stress cases.

## Color

P0/P1 severity in internal operations must not be mapped mechanically to user-facing red/orange UI. User-facing semantic state still requires Color + Interaction validation.

---

# OPEN ITEMS

- production monitoring/vendor/tool selection;
- exact CI/CD pipeline and where validation runs;
- internal machine-readable schemas for Surface Registry, Policy Change Register and Content Release Manifest;
- company/group email addresses for policy/alerts;
- App Store Connect webhook receiver/backend;
- Google Play operational API/automation beyond policy-email/deadline monitoring;
- live app inventory and real deep-link host matrix;
- actual monetization/app-ads.txt use;
- alert escalation SLA and on-call expectations;
- jurisdiction-specific legal monitoring once launch markets are defined;
- provider status-page watches after hosting/CDN vendors are chosen.

---

# Foundation conclusion

MintTap website operations should run as a **continuous verification system**, not a static set of pages.

The control loop is:

**event/policy/release/change → impact assessment → upstream truth revision → affected surface invalidation → pre-release validation → production publication → post-release verification → scheduled freshness review → preserved evidence/history.**

The highest-value next research area is now **implementation/provider comparison methodology** unless jurisdiction/market/legal facts become available first. That comparison should score real hosting/CMS/framework options against the contracts established in Studies 002–011 rather than choose technology by popularity.