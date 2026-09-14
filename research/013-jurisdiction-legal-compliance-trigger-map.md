# 013 — Jurisdiction-Specific Legal / Compliance Trigger Map

Status: **FOUNDATION STUDY / LEGAL APPLICABILITY REMAINS CONDITIONAL**  
Research date: **2026-09-14**  
Scope: `minttap.app` company/app/privacy/support/account-control web surfaces and their relationship to MintTap mobile apps.

## Question

How should MintTap decide which jurisdiction-specific legal/compliance web obligations apply without inventing facts about the company's legal entity, launch markets, users, data practices, payment model, age audience or third-party processors?

This study is a **trigger map and operational design input**, not legal advice and not a final legal determination. Final applicability must be re-evaluated against the actual MintTap legal entity, launch countries/states, app audience, direct-sales model, data flows and then reviewed by qualified counsel when the consequence is material.

---

## RELATED DOMAIN CHECK

### Existing Web Manager studies

- Study 003 already established App Data Contract + per-app Privacy/Support/Account Deletion surfaces.
- Study 004 established Product Truth and store↔web factual synchronization.
- Study 006 established WCAG 2.2 AA internal accessibility target.
- Study 007 established Korean/English locale architecture.
- Study 010 established Claim Registry and truthful marketing.
- Study 011 established Policy Change Register and continuous freshness controls.

### Design Studio

Legal/compliance requirements often become design requirements rather than separate footer documents:
- Web Design: page structure, disclosure placement, forms and implementation validation;
- Layout/Interaction: rights-request flows, consent/withdrawal, error/recovery and destructive controls;
- Typography: long legal/support content, Korean/English readability and reflow;
- Color: focus, status, destructive/disabled states and non-color-dependent meaning.

No Design Studio evidence is treated as legal authority.

---

# OPERATING MODEL — LEGAL TRIGGER REGISTRY

## MINTTAP DECISION

Do not maintain a single binary field such as `GDPR = yes/no` or `CCPA = yes/no` without underlying facts.

Create a **Legal Trigger Registry** with at least:

- jurisdiction;
- statute/regulation/policy;
- trigger facts;
- current applicability state: `APPLIES / DOES NOT APPLY / CONDITIONAL / UNKNOWN`;
- relevant app(s) / web surface(s);
- required user-facing notice/control if triggered;
- required backend/process behavior if triggered;
- source URL and source/effective date;
- factual dependencies still missing;
- responsible owner;
- legal-review requirement;
- last verification date;
- next review / change-watch trigger.

A legal/compliance obligation may not be marked `APPLIES` merely because users can technically access `minttap.app` from that jurisdiction.

---

# KOREA — PERSONAL INFORMATION PROTECTION ACT (PIPA)

## SOURCE — privacy policy contents

The current Korean Personal Information Protection Act, effective 2026-09-11, Article 30 requires a personal information controller to establish and disclose a privacy policy. Article 30 lists required areas including processing purpose, retention period, third-party provision where applicable, destruction procedures/methods, outsourcing where applicable, data-subject/legal-representative rights and exercise methods, privacy-officer/contact information, automatic collection devices where applicable, and other matters prescribed by decree.

Primary source:
- https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1029331583

PIPC also publishes a privacy-policy drafting guide; the current repository should use current law as authority and the PIPC guide as implementation guidance, rechecking for newer editions at production time.

Guidance source:
- https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=D010030020&nttId=11134

### MINTTAP DECISION

If MintTap is a PIPA-regulated personal-information controller for an app/site, the Korean privacy page cannot be a generic App Store template. Its contents must be generated/reviewed against the **App Data Contract**.

The policy should explicitly map actual:
- purposes;
- categories and retention;
- processors/outsourcing;
- third-party provision;
- deletion/destruction;
- user rights/contact routes;
- cookies/SDK/device or similar automatic collection behavior where applicable;
- overseas processing/transfer where applicable.

### BLOCKER

Do not publish a Korean privacy policy that says an SDK/vendor/data category is absent when the actual release uses it.

---

## SOURCE — rights request methods must be public and not harder than collection

PIPA Article 38(4) requires controllers to establish concrete methods/procedures for rights requests and make them publicly known; the method/procedure may not be more difficult than the method/procedure used to collect the personal information. Article 38 also addresses objections to refusals. Articles 35–37 establish rights such as access, correction/deletion, suspension of processing and withdrawal of consent subject to statutory conditions/exceptions.

Primary sources:
- https://www.law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029331309
- https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=283839

### SYNTHESIS

A privacy policy that merely names rights while providing an impractical or hidden exercise route is operationally insufficient.

### MINTTAP DECISION

Study 003's account/data-control architecture must support the broader concept of **data-subject rights routing**, not only store-mandated account deletion.

Potential public route model after actual requirements are known:
- per-app privacy page explains rights;
- stable privacy/support contact or request surface;
- authenticated in-app route where identity-sensitive operations require it;
- web route where legally/store-required or operationally useful;
- documented verification, response and objection process behind the user-facing surface.

Do not ask for more identity evidence than reasonably necessary to verify a rights request.

---

## SOURCE — privacy officer responsibility

PIPA Article 31 requires designation of a privacy officer subject to statutory exceptions/threshold rules; where an exception permits no separate designation, the owner/representative becomes the privacy officer under Article 31(2). The Act was amended in 2026 to introduce additional governance requirements for controllers meeting future/decree-defined scale criteria.

Primary sources:
- https://law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0031&lsiSeq=283839&urlMode=lsScJoRltInfoR
- https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029563011

### OPEN

MintTap's legal entity, employee/revenue/data scale and resulting exact CPO governance requirements are not recorded. Do not invent a named privacy officer/contact yet.

---

## SOURCE — overseas transfer is a separate trigger

PIPA Article 28-8 governs transfer of personal information outside Korea, including provision, processing outsourcing and storage. The statute provides several lawful routes; where transfer is based on consent, Article 28-8(2) specifies information that must be given in advance, including data categories, country/time/method, recipient/contact, purpose/retention and refusal consequences. The statute also permits certain contract-performance outsourcing/storage routes when required information is disclosed in the privacy policy or otherwise notified as specified.

Primary sources:
- https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029331899
- https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029334953

### MINTTAP DECISION

Provider selection must include a **data-location / cross-border-processing review** separately from website hosting performance.

Firebase, Cloudflare, analytics, ads, authentication, support systems or other vendors must not be treated as legally interchangeable merely because they all support HTTPS.

For every vendor that receives/stores/processes personal information record:
- legal entity / recipient;
- purpose;
- data categories;
- processing/storage country or region where determinable;
- retention/deletion terms;
- contractual role;
- applicable transfer basis;
- required disclosure/notice/consent status.

This becomes a dependency of the App Data Contract and provider POC/selection.

---

# KOREA — E-COMMERCE / DIRECT SALES

## SOURCE — direct online selling creates seller-information obligations

Korea's Act on the Consumer Protection in Electronic Commerce, Article 13, requires a mail-order seller advertising for the purpose of receiving an offer/order to provide specified identity information, including business name/representative, address/phone/email and mail-order-sales report information. Article 13(2) requires transaction-condition disclosures before contract formation.

Primary source (effective 2026-07-21):
- https://www.law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1027062829

### MINTTAP DECISION

Do **not** automatically add a Korean e-commerce-business footer to `minttap.app` merely because apps can be purchased in App Store / Google Play.

First classify the transaction model:

1. `STORE-ONLY ACQUISITION` — website only explains app and links to Apple/Google stores;
2. `WEB DIRECT SALE / SUBSCRIPTION` — MintTap accepts an order/payment/contract on `minttap.app`;
3. `HYBRID` — some direct web transaction plus store distribution.

If direct web contracting/selling is introduced, perform a dedicated Korean electronic-commerce legal review before launch and add the required business/transaction disclosures and cancellation/refund processes as applicable.

### BLOCKER

Do not add direct checkout/subscription to the website as an implementation detail without re-opening the Legal Trigger Registry.

---

# UNITED STATES — FEDERAL BASELINE (FTC)

## SOURCE — truth-in-advertising and privacy promises apply to mobile-app marketing

FTC business guidance for app developers states that representations about app capabilities on a website, app store or in the app must be truthful; objective claims require support. It also advises developers to disclose material information clearly/conspicuously, accurately explain data practices, honor privacy/security promises and maintain reasonable data security.

Primary FTC guidance:
- https://www.ftc.gov/business-guidance/resources/marketing-your-mobile-app-get-it-right-start
- https://www.ftc.gov/business-guidance/resources/app-developers-start-security

### SYNTHESIS

The U.S. federal baseline is not equivalent to “every app must publish one federally prescribed privacy-policy template.” Instead, FTC risk is strongly tied to actual representations, omissions, security practices and specialized rules.

### MINTTAP DECISION

Study 010's **Claim Registry** and Study 003's **App Data Contract** are also U.S. consumer-protection controls:
- no unsupported functionality/performance/security claims;
- no privacy promise that contradicts SDK/backend behavior;
- no buried material qualification;
- no changing a material data practice by silently editing the policy where additional notice/consent is legally required.

“Secure”, “private”, “anonymous”, “we never share”, and similar absolute statements are high-risk Claim Registry entries and require precise technical/legal support.

---

# UNITED STATES — COPPA

## SOURCE — trigger

The FTC's COPPA Rule applies to operators of commercial websites/online services directed to children under 13 that collect personal information, and to general-audience operators with actual knowledge they are collecting personal information from a child under 13. The FTC explicitly includes mobile apps within online services.

Primary sources:
- https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions

COPPA requirements include privacy notices, verifiable parental consent subject to exceptions, parental access/deletion/control, security and retention/deletion rules.

### MINTTAP DECISION

Every app's Product Truth Record should have an **Audience / Age Trigger** section:
- intended audience;
- whether child-directed factors exist;
- whether date-of-birth/age information is collected;
- whether MintTap can gain actual knowledge of an under-13 user;
- SDK/ad/analytics behavior for child users;
- store age classifications vs actual audience design.

Do not solve COPPA by adding a sentence “not intended for children under 13” if the actual product, marketing or collected age information indicates otherwise.

### CHANGE WATCH

COPPA remains actively evolving. The FTC updated the COPPA Rule in 2025 and issued a 2026 policy statement concerning certain age-verification technologies. Recheck current rule/guidance before any child/mixed-audience product launch.

Current FTC pages:
- https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children

---

# UNITED STATES — CALIFORNIA CCPA

## SOURCE — threshold-based application

The California Privacy Protection Agency states that the CCPA applies to a for-profit business that collects/controls processing of California consumers' personal information, does business in California, and meets at least one threshold. As of the 2025 CPI adjustment, the gross-revenue threshold is $26.625 million; alternative triggers include buying/selling/sharing personal information of 100,000 or more California consumers/households or deriving 50% or more annual revenue from selling/sharing California consumers' personal information.

Primary sources:
- https://cppa.ca.gov/faq
- https://cppa.ca.gov/regulations/cpi_adjustment.html

### SOURCE — web notice consequences when applicable

CPPA materials state that businesses subject to CCPA must provide a privacy policy and Notice at Collection; notices have content, language, readability and accessibility requirements. CPPA's FAQ also states covered businesses are required to post a privacy-policy link using the word “privacy” on their homepage and other webpages.

Primary sources:
- https://cppa.ca.gov/pdf/general_notices.pdf
- https://cppa.ca.gov/faq

### MINTTAP DECISION

Do not mark CCPA `APPLIES` merely because a Californian can download an app.

Record and periodically recompute:
- entity for-profit status;
- California business nexus;
- annual gross revenue threshold;
- California consumer/household processing count;
- whether personal information is sold/shared as defined by CCPA;
- percent of revenue from sale/sharing;
- service-provider/contractor relationships and exemptions.

If triggered, the website/app must implement the applicable privacy notice and rights mechanisms rather than merely renaming the Korean privacy policy “California Privacy Policy.”

### CHANGE WATCH

California rules continue to change. New CCPA regulations became effective 2026-01-01, including risk-assessment, cybersecurity-audit and automated-decisionmaking requirements for certain covered businesses/processing, with different compliance dates.

Current source:
- https://cppa.ca.gov/regulations/ccpa_updates.html

---

# UNITED STATES — OTHER STATES

## OPEN / CHANGE WATCH

This Foundation study does **not** claim California is the only U.S. state privacy regime.

Before launching materially into U.S. markets, build a current state-law inventory using:
- actual states targeted/served;
- business/data-volume thresholds;
- sale/share/targeted-advertising definitions;
- sensitive-data processing;
- consumer rights/appeal requirements;
- universal opt-out signals where required;
- child/teen rules;
- notice language/accessibility requirements.

Do not copy CCPA controls into every state and assume compliance.

---

# EUROPEAN UNION — CONDITIONAL WATCH

## SOURCE — territorial trigger

GDPR Article 3 applies not only to EU establishments but also, under specified conditions, to non-EU controllers/processors processing personal data of people in the EU where processing relates to offering goods/services to them or monitoring their behavior in the EU.

Article 13 specifies information that must be provided when personal data are collected directly, including controller identity/contact, purposes/legal basis, recipients and international-transfer information, plus additional transparency items.

Primary source:
- https://eur-lex.europa.eu/eli/reg/2016/679/

### MINTTAP DECISION

Do not treat the fact that `minttap.app` is globally reachable as sufficient evidence that GDPR applies.

Re-open EU legal review if product strategy shows indicators such as:
- intentional EU market availability/marketing/localization;
- EU-directed goods/services;
- EU user accounts and commercial activity;
- analytics/advertising or other behavior monitoring of users in the EU;
- EU establishment/representative/processor relationship.

EU cookie/ePrivacy consent, transfer mechanisms, representative/DPO and member-state-specific obligations require a separate review when this trigger becomes real.

---

# TERMS OF SERVICE / LEGAL PAGE ARCHITECTURE

## SYNTHESIS

There is no evidence from this study that every MintTap informational app page requires a generic “Terms of Service” page merely because it exists on the web.

Terms become material when they define an actual contract/service relationship, account conditions, direct website transactions/subscriptions, user-generated content, licensing or other product-specific obligations.

### MINTTAP DECISION

Do not generate generic legal boilerplate just to make the footer look complete.

`/terms/` remains conditional until the actual service/transaction/account contract requires it. App Store/Google Play platform terms do not automatically substitute for MintTap-specific terms where MintTap has its own contractual obligations.

---

# JURISDICTION / TRIGGER MATRIX — FOUNDATION

| Area | Trigger facts | Web consequence if triggered | Current state |
| --- | --- | --- | --- |
| Korea PIPA privacy policy | MintTap is regulated controller processing PI | Korean privacy policy matched to actual data contract | CONDITIONAL — entity/data facts incomplete |
| Korea PIPA rights | processing subject to PIPA | public rights methods + operational request handling | CONDITIONAL |
| Korea overseas transfer | personal information transferred/provided/outsourced/stored abroad | transfer basis + disclosure/notice/consent as applicable | CONDITIONAL; high relevance to cloud vendor choice |
| Korea e-commerce | MintTap accepts direct web order/contract/payment | seller identity + transaction-condition/cancellation/refund review | NOT YET TRIGGERED by known website plan |
| U.S. FTC | commercial app/marketing/data/security representations | truthful claims, clear material disclosures, honored privacy/security promises | RELEVANT BASELINE for U.S. activity |
| U.S. COPPA | child-directed under-13 service or actual knowledge | COPPA notice/consent/parent rights/security/retention controls | UNKNOWN — audience facts required |
| California CCPA | CA nexus + for-profit/controller + statutory threshold | privacy/collection notices + rights/opt-outs etc. | UNKNOWN — threshold facts required |
| Other U.S. states | state-specific scope thresholds/triggers | state-specific notices/rights/opt-outs | OPEN / launch-time inventory required |
| EU GDPR | EU establishment or Art. 3(2) goods/services/monitoring trigger | GDPR transparency/rights/basis/transfers etc. | CONDITIONAL — do not infer from global accessibility |

---

# PRODUCT / RELEASE DATA REQUIRED BEFORE LEGAL PASS

Before a real MintTap app/page can receive legal-compliance signoff, collect:

## Entity / market
- exact contracting/publishing legal entity;
- registered/public business contact data;
- countries/states intentionally launched/marketed;
- whether website accepts direct orders/payments/subscriptions;
- store seller-of-record / merchant-of-record model where applicable.

## Audience
- intended age audience;
- child/teen-directed characteristics;
- age collection/verification;
- educational/family use cases if any.

## Data
- exact data categories;
- sensitive/financial/geolocation/health/child data;
- SDKs/processors;
- purposes and legal/operational basis;
- retention/deletion;
- sale/share/targeted-ad implications;
- processing/storage countries;
- direct vs inferred/third-party data collection.

## Rights / operations
- identity verification method for requests;
- request channels;
- response/appeal workflow;
- deletion/account closure relation;
- support/privacy inbox ownership;
- legal preservation exceptions;
- incident/breach escalation.

---

# INTEGRATION WITH EXISTING CONTROL ARTIFACTS

## App Data Contract additions

Add fields for:
- controller/entity;
- jurisdiction/market coverage;
- processor location/cross-border transfer;
- sensitive-data class;
- audience/age trigger;
- sale/share/targeted-ad classifications where relevant;
- legal retention requirements/exceptions;
- rights supported and backend implementation path.

## Product Truth Record additions

Add:
- intended public markets;
- direct-sale model;
- intended audience age class;
- terms/subscription model;
- account relationship and deletion scope.

## Content Release Manifest additions

For every release check whether changes affect:
- data collection/use/share/retention;
- SDK/vendor/country;
- age audience;
- price/payment/direct sale;
- automated decision/profiling behavior;
- rights/deletion workflow;
- legal/entity/contact data;
- market availability.

Any such change invalidates relevant privacy/legal review state.

## Policy Change Register additions

Watch at minimum:
- Korean PIPA / Enforcement Decree / PIPC guidance;
- Korean e-commerce law if direct selling becomes relevant;
- FTC privacy/security/advertising/COPPA updates;
- CPPA CCPA regulations/threshold updates;
- other U.S. state regimes once U.S. market scope is active;
- GDPR/EU guidance once EU trigger is active.

---

# DESIGN STUDIO HANDOFFS

## Web Design

Legal/compliance content creates page-system requirements:
- privacy notices need readable structure, in-page navigation where long, stable anchors when useful and mobile readability;
- Notice at Collection / just-in-time disclosures may need contextual placement near collection points rather than footer-only presentation;
- rights requests require accessible form/state/error/success design;
- direct-sale disclosures, if introduced, must be visible before contract action.

## Layout / Interaction

High-value validation targets:
- withdrawal/delete/rights flows must be understandable and reversible where legally/semantically appropriate;
- destructive account/data actions require clear scope and confirmation;
- denial/partial fulfillment needs explanation and an objection/appeal path where required;
- material limitations cannot be hidden behind low-salience disclosure patterns.

## Typography

Legal/support text is a strong Korean/English long-copy stress case:
- headings and hierarchy;
- long processor/transfer names;
- phone/email/addresses;
- line wrapping and zoom;
- date/retention expressions;
- tables/lists under narrow reflow.

## Color

Legal rights and consent cannot depend on color-only distinction. Error, warning, destructive, success and current-choice states must retain semantic clarity under high contrast/forced colors.

---

# RELEASE BLOCKERS ADDED BY THIS STUDY

When an applicable jurisdiction trigger is established, blockers include:

- publishing a privacy policy that materially contradicts actual processing;
- missing/false controller or required contact information;
- missing public rights-request method when legally required;
- rights-request path materially harder than the collection path where Korean PIPA Article 38 applies;
- undisclosed/unreviewed overseas transfer where Korean PIPA requirements apply;
- introducing direct web commerce without reopening seller/transaction obligations;
- child-directed/known-under-13 collection without completed COPPA review where relevant;
- marking CCPA compliance complete without verifying scope thresholds and current regulations;
- making privacy/security claims unsupported by operational reality;
- copying one jurisdiction's privacy template and presenting it as universally compliant.

---

# CHANGE WATCH

This study is intentionally date-sensitive.

Recheck legal sources:
- before first production launch;
- when MintTap legal entity changes;
- when a new country/state is intentionally targeted;
- when account/data/SDK/analytics/ads/payment/age behavior changes;
- when a website direct-sale flow is introduced;
- on a periodic compliance review cadence;
- whenever Policy Change Register receives a relevant update.

---

# OPEN / DEPENDENCIES

Still unknown:
- MintTap legal entity and place of establishment;
- contracting entity per app/store;
- final intended launch countries/states;
- direct web payment/subscription plan;
- exact app audience/age classifications;
- actual App Data Contracts per app;
- exact cloud/SDK processor countries;
- whether targeted advertising/sale/share categories are used;
- company revenue/user/California-volume thresholds;
- EU targeting/monitoring facts;
- legal counsel/reviewer and final signoff process.

These unknowns prevent legal PASS but do **not** block the Foundation architecture.

## Foundation conclusion

MintTap should manage legal web compliance as a **fact-driven trigger system**, not a universal pile of Privacy/Terms/Cookie boilerplate.

The operating chain is:

**Entity + market + audience + transaction model + App Data Contract → Legal Trigger Registry → required public notice/control → backend operational process → release validation → policy/fact change watch.**

That structure minimizes both under-compliance and unnecessary legal/UI clutter.