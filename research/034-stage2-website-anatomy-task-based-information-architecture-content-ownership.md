# 034 — Stage 2 Website Anatomy, Task-Based Information Architecture & Content Ownership

Status: **STAGE 2 FOUNDATION / PRACTITIONER CHECKPOINT**
Research date: 2026-09-15
Scope: public company/app website architecture for a developer shipping Apple and Android apps under `minttap.app`.

## Why this block exists

Studies 002 and 026 already established two useful directions:

- MintTap should have durable app identities and a company-first, app-centered URL model rather than unrelated one-off landing pages;
- website planning should distinguish visitor intents such as discover, evaluate, act, support and governance.

Repeating those conclusions would add little value. This block therefore advances the problem one level:

> How do we turn intent categories and a provisional sitemap into an information architecture that remains findable, operable, maintainable and truthful as apps, policies, support content and markets grow?

The key addition is a **task → destination → page system → ownership/lifecycle** model. IA is treated not as a navigation menu exercise but as an operating system for public product information.

---

## 1. SOURCE — public app-company websites are not optional decoration around the stores

### Apple App Store Connect

Apple's current App Store Connect reference defines a **Support URL** as required platform-version information. Apple says it is the URL of the support website provided for users and that it must lead to actual contact information as required by local law so users can reach the developer about app issues, feedback and feature requests. Apple separately defines an optional **Marketing URL** as the website where users can get more information about the app.

Source checked 2026-09-15:
- Apple Developer — Platform version information: https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information

Apple also requires a **Privacy Policy URL** for all apps in App Store Connect.

Source checked 2026-09-15:
- Apple Developer — App privacy reference: https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy

### Google Play

Google Play Console's account-information guidance says developers can provide a website in Store listing contact details, with the contact information appearing on the app's Google Play listing. Google Play's User Data policy further requires an accessible external web resource for account deletion when account deletion requirements apply, in addition to the in-app deletion option.

Sources checked 2026-09-15:
- Google Play Console Help — developer account information: https://support.google.com/googleplay/android-developer/answer/13634081
- Google Play Console Help — User Data policy: https://support.google.com/googleplay/android-developer/answer/10144311

### SYNTHESIS

For an Apple/Android app developer, the public website is not merely a marketing microsite. It can act simultaneously as:

1. product explanation and acquisition support;
2. required or store-linked support destination;
3. privacy and user-control destination;
4. developer identity/contact surface;
5. canonical public location for information that must survive app versions and store interfaces.

This makes IA an operational concern. If support, privacy or account-control destinations become ambiguous, stale or app-mismatched, the problem can affect store compliance and user trust, not only usability.

---

## 2. First-principles model: information architecture starts with user questions, not the organization chart

A company can describe itself internally through departments, products, engineering teams, legal ownership and release pipelines. Visitors generally arrive with a different mental problem:

- What is this app?
- Does it solve my problem?
- Is it available on my device?
- How do I download it?
- How much does it cost?
- How is my data handled?
- I already use it; how do I fix something?
- How do I delete my account or data?
- Who operates this product and how do I contact them?

### SYNTHESIS — the primary IA unit is the user task

A durable architecture should be designed by mapping:

`audience/context → intent → task/question → destination → content object → owner → lifecycle`

rather than:

`company department → page`.

Internal ownership still matters, but it belongs to the governance model behind the page rather than being the main principle exposed to users.

### Failure mode: organization-chart IA

A site can be logically tidy internally and still force visitors to understand MintTap's internal structure before finding help. Examples include placing account deletion under “Compliance,” product help under “Operations,” or store-download links under “Distribution.”

Those labels may be meaningful inside the company but have weak information scent for ordinary users.

---

## 3. SOURCE — orientation and findability require more than one navigation menu

W3C WAI guidance recommends clear and consistent navigation, descriptive titles/headings/labels, orientation cues such as clear headings or breadcrumbs, and more than one method of finding pages where appropriate. WCAG 2.2 also contains requirements around consistent navigation/help in sets of pages.

Sources checked 2026-09-15:
- W3C WAI — Designing for Web Accessibility: https://www.w3.org/WAI/tips/designing/
- W3C WAI — Interaction: navigating and finding: https://www.w3.org/WAI/people-use-web/tools-techniques/navigation/
- W3C WAI — Accessibility Principles: https://www.w3.org/WAI/fundamentals/accessibility-principles/
- W3C WAI — What's New in WCAG 2.2 / Consistent Help: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/

Google Search's current breadcrumb guidance similarly describes breadcrumbs as communicating a page's position in site hierarchy and helping users explore upward. Importantly, Google recommends breadcrumbs that represent a typical **user path** rather than mechanically mirroring URL structure.

Source checked 2026-09-15:
- Google Search Central — Breadcrumb structured data: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

### SYNTHESIS — IA has several simultaneous views

Do not reduce IA to the primary header navigation. A mature site exposes structure through multiple coordinated mechanisms:

- canonical URLs;
- global navigation;
- contextual/local navigation;
- page titles and headings;
- breadcrumbs where useful;
- meaningful internal links;
- footer/utility navigation;
- search or sitemap when content volume justifies it;
- store/deep links that arrive directly at lower-level pages.

These views can differ in presentation while describing one coherent content system.

---

## 4. Website anatomy for an app company: page systems, not a bag of pages

### SYNTHESIS

For MintTap-like companies, page types should be defined by recurring user jobs and content contracts. A useful conceptual anatomy is:

### A. Company / portfolio system

Purpose:
- establish developer identity;
- explain the portfolio at an appropriate level;
- route visitors to individual products;
- provide stable company/contact/governance context.

Possible objects:
- homepage;
- apps/product index;
- about/company page only when substantive content exists;
- contact/company support routing.

### B. App identity system

Purpose:
- give each app a stable public identity;
- explain its value, availability and evidence;
- route to the correct store/platform;
- connect product, support and governance information.

Possible objects:
- canonical app landing page;
- platform/store actions;
- feature/evidence sections or supporting pages when content volume warrants them;
- release/documentation surfaces later if the product needs them.

### C. Support / self-service system

Purpose:
- help existing users resolve problems;
- provide reliable contact/escalation;
- keep app context intact.

Possible objects:
- support hub;
- app-specific support hub;
- task/topic articles;
- contact or escalation path;
- service-status page later if operational complexity justifies it.

### D. Governance / user-control system

Purpose:
- expose legally/policy-required information;
- let users exercise privacy/account/data choices;
- clearly state scope and responsible product/entity.

Possible objects:
- privacy policy;
- terms where applicable;
- account/data deletion resource;
- privacy choices/data request resource;
- notices required by jurisdiction or product behavior.

### E. Machine/infrastructure system

Purpose:
- satisfy platform/protocol integrations rather than ordinary browsing.

Examples from prior studies:
- `/.well-known/assetlinks.json`;
- `apple-app-site-association`;
- `app-ads.txt` when applicable;
- sitemap/robots and other machine-consumed files.

### Operational rule

Do not force every URL into global navigation. **The content tree, user navigation and machine endpoint space are related but not identical.**

---

## 5. The app is the primary context boundary for product-specific information

Study 002 correctly established app identity as first-class. This block strengthens that decision by connecting it to store-linked responsibilities.

Apple's privacy information is answered at the app level in App Store Connect, and Apple requires app support/privacy destinations. Google Play account deletion policy says external deletion resources should clearly reference the app/service.

### SYNTHESIS

When a fact or control differs by app, the app context must remain obvious across the complete path.

For example:

`Store listing → MintTap app page/support/deletion destination → task completion`

should not force a user to land on a generic company page and re-identify which product they use.

### MINTTAP DIRECTION

Retain the durable app namespace proposed in Study 002:

```text
/apps/<app-slug>/
```

with app-owned destinations beneath it when scope is truly app-specific.

However, URL nesting is not mandatory merely because content relates to an app. The controlling question is **scope and lifecycle**, not aesthetic consistency.

Examples:
- a company-wide privacy policy can remain `/privacy/` if it genuinely governs all apps and clearly expresses scope;
- app-specific deletion instructions can live under the app identity where that avoids ambiguity;
- a global support hub can route into app-specific support systems.

---

## 6. Information hierarchy: primary, secondary and assurance tasks

A frequent IA mistake is to treat every important company requirement as equally prominent in the primary navigation.

### SYNTHESIS — three task classes

For most public app pages, tasks can be separated as:

1. **Primary task** — the main reason the page exists, e.g. understand/download the app or solve a support problem;
2. **Secondary task** — related but less frequent actions, e.g. compare features, contact support, inspect details;
3. **Assurance/governance task** — privacy, terms, developer identity, data choices, account deletion, legal/support proof.

Assurance tasks must remain findable and accessible, but “important” does not automatically mean “top-level global navigation item.”

### Example

A privacy policy can be mission-critical and store-required while still belonging in a consistent footer/utility/governance pathway rather than taking equal visual priority with Apps or Support in the global header.

### Constraint

If policy, law, user research or task frequency demonstrates that a governance action must be more prominent, prominence should change. The classification is a design/IA starting model, not a way to hide required information.

---

## 7. Navigation depth: optimize decision cost, not raw click count

“Everything should be one click away” is not a useful universal rule. A flat site with many unrelated choices can be harder to scan than a slightly deeper structure with strong grouping and labels.

### SYNTHESIS

The better objective is:

- understandable categories;
- strong information scent;
- predictable location;
- low ambiguity at each decision point;
- direct deep links for external/store/support entry points;
- no dead-end page that forces return to the homepage to change context.

### MINTTAP DIRECTION

For a small portfolio, keep the **global** navigation shallow while allowing the **content system** to deepen under individual apps/support areas as volume grows.

This preserves a simple first impression without flattening future support/documentation into one giant page.

---

## 8. Labels and taxonomy: use user-recognizable nouns and tasks

### SOURCE

W3C accessibility guidance emphasizes descriptive titles, headings, labels and link text because these may be encountered out of context.

### SYNTHESIS

Navigation labels should make the destination predictable without requiring surrounding marketing copy.

Prefer stable task/domain words such as:
- Apps;
- Support;
- Privacy;
- Delete account / Account deletion;
- Contact.

Avoid relying on vague branded labels such as:
- Explore;
- Discover more;
- Resources;
- Center;
- Experience;

unless user evidence shows those terms are understood and the destination is obvious.

### Taxonomy rule

Classification should use the attribute users need for the decision at that point. Examples:
- support grouped by app when product context is the first question;
- articles grouped by task/topic after app context is known;
- platform (iOS/Android) introduced only when instructions actually diverge.

Do not expose implementation categories merely because they exist in engineering.

---

## 9. Support IA should preserve context and escalation

A support system has two jobs that are often confused:

1. self-service resolution;
2. escalation to a human/contact mechanism when self-service fails.

Apple's required Support URL explicitly ties the support website to contactability for app issues, feedback and feature requests.

### SYNTHESIS

A support architecture should therefore be able to answer:

- Which app?
- What task/problem?
- Which environment/platform if relevant?
- What self-service information exists?
- What happens if it does not work?

### Failure modes

- one generic email address with no app context;
- app-specific FAQ pages with no route back to support hub;
- dead articles without escalation/contact;
- different labels for the same help mechanism on different pages;
- support pages whose ownership disappears after launch.

### DESIGN STUDIO dependency

Web Design/Interaction should later validate whether users can maintain orientation while moving company → app → support topic → escalation on desktop, mobile, keyboard and touch flows.

---

## 10. Content ownership is part of IA

A sitemap without owners and update triggers is incomplete for an app company.

### SYNTHESIS — every production content object needs operational metadata

At minimum, major content objects should have:

- **scope** — company-wide, app-specific, market-specific, platform-specific;
- **canonical source** — where the factual truth comes from;
- **owner** — role responsible for correctness;
- **approver** — where separate review is required;
- **review/update trigger** — release, policy change, data-flow change, pricing change, support change, jurisdiction change;
- **store dependencies** — App Store/Play Console fields pointing to this URL or repeating its claims;
- **localization status**;
- **retirement/redirect rule**.

This extends earlier Product Truth and release-governance studies into visitor-facing IA.

### Example content contract

`/apps/<app>/support/`

- scope: app-specific;
- source of truth: current shipped app behavior + support operating policy;
- owner: product/support role;
- triggers: feature removal/addition, account flow change, contact mechanism change, store metadata change;
- dependent surfaces: Apple Support URL, Google Play developer/support links where used;
- validation: links, contact path, mobile/keyboard access, correct app identity.

### Key principle

**IA defines not only where information lives, but also which public statement is authoritative when multiple surfaces repeat it.**

---

## 11. Store ↔ website continuity must be modeled as edges, not duplicated pages

Apple and Google store pages are separate public surfaces with their own metadata models. The website should not blindly duplicate them.

### SYNTHESIS

Model the relationship as explicit edges:

`acquisition source → store or web landing → app identity → support/governance → store/action`

Each edge has a user expectation and factual consistency requirement.

Examples:
- App Store Support URL should land in relevant support context;
- Privacy Policy URL should resolve directly to the governing policy, not a homepage that requires hunting;
- Google external account deletion URL should lead to a resource that clearly identifies the app/service and explains or performs the deletion process;
- website download CTA should resolve to the correct platform/store and not silently send users to an unavailable product.

### MINTTAP DIRECTION

Maintain explicit **external-entry contracts** for every store-linked website URL. Treat those URLs as public APIs: stable, testable and backward-compatible unless a deliberate redirect/migration is performed.

---

## 12. Multi-app growth: separate stable architecture from temporary portfolio size

Study 002 proposed `/apps/<app>/` even when the portfolio is small. That remains a strong direction because it allows growth without changing canonical identity.

### SYNTHESIS

Growth pressure typically appears in three places:

1. **portfolio discovery** — more apps make a homepage-only card list insufficient;
2. **support volume** — app-specific troubleshooting diverges;
3. **governance scope** — privacy/account/legal obligations may differ by product or market.

The architecture should therefore scale by **adding depth inside stable contexts**, not by repeatedly redesigning top-level categories.

### Anti-pattern

Do not create new top-level navigation items for every new app. That makes global navigation track portfolio count and eventually collapses under growth/localization.

---

## 13. Localization changes content systems, not just strings

Study 007 already covers localization architecture, so this block does not duplicate it. The Stage 2 implication is narrower:

### SYNTHESIS

IA decisions must identify which structures are language-neutral and which labels/content are locale-specific.

Validate:
- longer Korean/English/other-language navigation labels;
- different legal or support content by jurisdiction;
- locale-specific store destinations;
- translated content ownership/freshness;
- whether direct external links arrive at the correct locale without trapping users.

A taxonomy that works only because English labels are short is not production-ready.

---

## 14. Search/discovery implications without turning Stage 2 into SEO study

The dedicated SEO stage remains later. Stage 2 only needs the architectural prerequisite.

### SOURCE

Google Search's breadcrumb guidance recognizes a page as part of a hierarchy and explicitly allows breadcrumb paths to represent typical user paths rather than literal URL nesting.

### SYNTHESIS

Important product/support/governance pages should have:
- unique stable URLs;
- meaningful internal links;
- descriptive titles/headings;
- explicit parent/context relationships where useful;
- no requirement to execute an obscure UI sequence before the page can be addressed.

This benefits humans, accessibility and later search work simultaneously.

---

## 15. Stage 2 operating model — Task/Destination Matrix

Before designing a sitemap for a real MintTap release, construct a matrix such as:

| Audience/context | Intent/task | Canonical destination | Scope | Primary owner | External dependency |
| --- | --- | --- | --- | --- | --- |
| Prospective user | Understand app | App landing page | App | Product/content | Store listing/message continuity |
| Prospective user | Install app | Store action from app page | App/platform | Product/release | App Store / Google Play URL |
| Existing user | Get help | App support hub | App | Support/product | Apple Support URL where used |
| Existing user | Contact developer | Support/contact path | Company/app | Support | Store contact metadata |
| User/data subject | Understand data use | Governing privacy policy | Company/app | Privacy/legal/product | Apple privacy URL / Play policy |
| Account holder | Delete account | External deletion resource | App | Product/privacy/support | Google Play account deletion policy when applicable |
| Visitor | Identify developer | Company/contact surface | Company | Company owner | Store developer identity/contact |

The final rows depend on the real product. The matrix is a planning method, not a claim that every MintTap app currently needs every destination.

---

## 16. Failure diagnosis for IA

When a user “cannot find something,” avoid treating it as a generic navigation problem. Diagnose the earliest broken contract:

1. **Missing content** — no destination exists.
2. **Scope ambiguity** — destination exists but user cannot tell which app/policy it applies to.
3. **Label failure** — destination exists but link/category name does not predict it.
4. **Placement failure** — link exists in an implausible context.
5. **orientation failure** — user reaches a page but cannot understand location or move upward/sideways.
6. **external-entry failure** — store/search/deep link lands at the wrong level/context.
7. **lifecycle failure** — page was correct but became stale after product/policy change.
8. **responsive/accessibility failure** — architecture exists logically but a user cannot operate it under keyboard, zoom, screen reader, narrow viewport or localized content conditions.

This classification allows different fixes rather than reflexively redesigning the menu.

---

## 17. MINTTAP DIRECTION — provisional Stage 2 architecture rules

Until real project evidence overrides them:

1. Organize public information around user tasks and stable app identities, not internal departments.
2. Keep the global navigation smaller than the complete content tree.
3. Preserve a durable `/apps/<app>/` identity for each shipped app.
4. Treat Support, Privacy and account/data controls as first-class destinations even when they are utility/governance navigation rather than global-primary items.
5. Use global hubs to route into app-specific contexts rather than forcing either one giant generic page or disconnected silos.
6. Give every store-linked URL an explicit owner, scope and stability contract.
7. Model external entry from App Store, Google Play, search and direct links; do not assume homepage-first navigation.
8. Define page **types/contracts** before individual page layouts.
9. Record content ownership and change triggers as part of IA.
10. Validate navigation/wayfinding under mobile, keyboard, zoom, screen-reader and localization stress before calling the architecture production-ready.

These are architecture defaults, not a frozen MintTap sitemap.

---

## 18. OPEN — facts required before converting this into MintTap's actual sitemap

- actual app inventory and which products are currently public;
- whether MintTap is the legal/developer-facing brand on each store listing;
- current Apple Support URLs, Marketing URLs and Privacy Policy URLs;
- current Google Play developer website/contact/privacy/account-deletion URLs;
- which apps allow account creation;
- actual data-policy scope by app;
- support channels, staffing and escalation model;
- primary markets/languages;
- product naming/slugs;
- pricing/account/subscription distinctions;
- planned docs/release notes/status pages;
- measured visitor/acquisition/task evidence.

Do not infer these from generic patterns.

---

## 19. VALIDATION — what a real MintTap IA review must test

Before launch or major restructuring:

1. Create the task/destination matrix from real product/store facts.
2. Verify every Apple/Google website URL lands directly in the intended context.
3. Test direct entry to lower-level pages; do not test only homepage journeys.
4. Test app switching and route back to portfolio/support hub.
5. Test current-location cues and heading hierarchy.
6. Test keyboard operation and visible focus.
7. Test at narrow viewport and at least 200% zoom/reflow conditions.
8. Stress labels with supported languages and realistic long app names/content.
9. Check orphan/dead-end pages and broken internal links.
10. Review each content object's owner and update triggers against the release process.
11. Re-test after app/store/privacy/account-flow changes, because IA correctness can decay without layout changes.

---

## 20. DESIGN STUDIO dependency / handoff

Design Studio global status and `progress/WEB_STATUS.md` were re-read on 2026-09-15. Web Design is still Stage 1 / Foundation not yet baselined, but its declared scope directly includes IA, navigation, wayfinding, page hierarchy, responsive systems and browser validation.

### Incoming dependency from Design Studio

When Web Design establishes its baseline, MintTap will need reusable evidence for:
- global vs local navigation patterns;
- orientation/current-location treatments;
- responsive navigation behavior;
- content hierarchy/scan flow;
- page-template/component application;
- browser/keyboard/touch validation.

Layout research also explicitly treats perceptual grouping, hierarchy, responsive recomposition, regions and spatial ownership as canonical spatial questions. These are relevant when the logical IA is turned into visual page systems.

### Outgoing handoff from Web Manager

Future MintTap Web Design work should receive:
- task/destination matrix rather than only a sitemap;
- page-type/content contracts;
- primary/secondary/assurance task hierarchy;
- direct-entry/store-link requirements;
- app-context preservation rules;
- content owner/lifecycle constraints;
- required support/privacy/account-control findability;
- localization and accessibility stress cases.

Web Design should challenge the IA if actual page composition or navigation validation exposes weak grouping, labels or hierarchy. That feedback should return to Web Manager rather than being patched only through visual styling.

No Design Studio canonical file was edited.

---

## 21. Integrated competency checkpoint

This block passes if the Web Manager can:

- distinguish sitemap, URL structure, global navigation, contextual navigation and page hierarchy;
- derive page systems from tasks rather than internal departments;
- explain why app identity is a durable context boundary;
- decide whether content should be company-wide vs app-specific based on scope/lifecycle rather than visual symmetry;
- explain why a required support/privacy/deletion URL is an operational contract, not merely a link;
- keep global navigation shallow without flattening all content;
- diagnose missing content vs labeling vs placement vs orientation vs lifecycle failures;
- attach ownership/update triggers to public content;
- preserve direct-entry and store↔website continuity;
- identify which MintTap facts remain unknown rather than fabricating a sitemap.

**Checkpoint result: PASS at Stage 2 foundation/practitioner level for website anatomy and IA operating model.**

---

## Next highest-value Stage 2 block

Proceed to **content modeling, content hierarchy and lifecycle for app-company pages/support/governance** rather than immediately designing MintTap's final sitemap.

Highest-value questions:
- what constitutes a reusable content object vs page-specific prose;
- claim/evidence structure for product pages;
- support article models and escalation metadata;
- policy/governance scope/versioning;
- content freshness and review triggers;
- duplication vs canonical reuse across website and stores;
- how page templates consume content without making all apps look semantically identical.

This will connect earlier Product Truth/release-governance studies to the new Stage 2 IA model without repeating them.