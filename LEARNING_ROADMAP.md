# MintTap Web Manager — Beginner-to-Advanced Learning Roadmap

Status: **ACTIVE CURRICULUM**
Established: 2026-09-14

## Purpose

This roadmap defines how the MintTap Web Manager builds professional web knowledge from first principles to advanced judgment.

The objective is not to race through topics or maximize research-file count. The objective is to develop a reliable mental model of the web, then progressively learn how to plan, evaluate, launch, operate and improve websites for a company that develops Apple and Android apps.

Existing studies 001–026 are retained as valid evidence. They are treated as partial prior coverage, not proof that every prerequisite has been learned in sequence. When a foundational gap exists, the Web Manager may deliberately revisit a topic at a more elementary level.

## Learning rule

For each major topic, progress through four layers:

1. **FOUNDATION — What is it?**
   - vocabulary, concepts, actors, layers, standards and basic mechanics;
   - explainable without assuming specialist knowledge.
2. **PRACTITIONER — How is it used?**
   - common patterns, trade-offs, failure modes and implementation implications;
   - ability to evaluate ordinary real sites.
3. **ADVANCED — How do systems interact?**
   - cross-domain effects, measurement, architecture, governance and optimization;
   - ability to compare alternatives under constraints.
4. **EXPERT JUDGMENT — What should MintTap do and why?**
   - evidence quality, business/product fit, risk, lifecycle effects and second-order consequences;
   - ability to make and defend project-specific decisions without pattern-copying.

A topic is not considered learned merely because a checklist or implementation exists.

---

# Stage 1 — Web Foundations

Goal: understand the web itself before specializing in websites.

Study areas:
- Internet vs Web; client/server model;
- browser, server, origin, host, URL, URI and resource;
- DNS resolution and domain hierarchy;
- HTTP request/response model;
- methods, status codes and headers;
- HTTPS, TLS and certificates at conceptual level;
- HTML as document structure;
- CSS as presentation/layout system;
- JavaScript as behavior/runtime layer;
- DOM and accessibility tree concept;
- static vs dynamic sites;
- server-side vs client-side rendering at conceptual level;
- cookies, local storage, sessions and cache basics;
- CDN and edge basics;
- browser navigation/history;
- forms and basic user input flow;
- hosting/deployment vocabulary;
- how search engines and assistive technologies consume web documents at a basic level.

Exit capability:
- explain what happens from entering `minttap.app` to seeing and interacting with a page;
- distinguish document, network, browser, server, storage and hosting concerns;
- identify which layer owns a basic web problem.

---

# Stage 2 — Website Anatomy, Content & Information Architecture

Goal: understand what a website is made of from the user and information perspective.

Study areas:
- website purpose and audience;
- page types and site archetypes;
- content hierarchy;
- headings and document outline;
- navigation systems;
- global/local/contextual/footer navigation;
- labels, taxonomy and terminology;
- information scent;
- wayfinding;
- search and browse behavior;
- shallow vs deep IA;
- single-product vs multi-product company sites;
- app detail pages;
- company/about/support/privacy/legal surfaces;
- support and self-service IA;
- content lifecycle and ownership;
- content models and structured content;
- localization effects on IA and content structure.

Exit capability:
- produce and critique a sitemap and navigation model;
- explain why content belongs on a particular page and in a particular order;
- design an IA that can grow from one MintTap app to many.

---

# Stage 3 — User Experience & Interaction Foundations

Goal: understand how people perceive, navigate and act on websites.

Study areas:
- user goals, tasks and journeys;
- discoverability and affordance;
- feedback and system status;
- consistency and expectation;
- cognitive load;
- recognition vs recall;
- progressive disclosure;
- error prevention and recovery;
- forms and validation;
- keyboard, pointer and touch interaction;
- focus management;
- responsive vs adaptive behavior;
- mobile constraints;
- empty/loading/error/partial states;
- trust and uncertainty reduction;
- ethical persuasion and dark-pattern avoidance;
- conversion paths and friction.

Exit capability:
- critique whether a user can understand, navigate and complete a task;
- distinguish visual attractiveness from usability;
- write interaction and state requirements for Design Studio/engineering.

---

# Stage 4 — Web Design Literacy

Goal: become able to judge web-specific design quality while using Design Studio as the reusable design authority.

Study areas:
- visual hierarchy;
- composition and spacing;
- grid and alignment;
- typography on the web;
- font loading/fallback implications;
- color and contrast in browser contexts;
- imagery, screenshots and product demonstration;
- responsive composition;
- design systems and component systems;
- native vs custom controls;
- design tokens;
- page templates;
- consistency vs local optimization;
- content density;
- scan paths;
- motion and feedback when justified;
- web-specific application of Type/Color/Layout-Interaction research.

Exit capability:
- give a structured critique of a web design;
- distinguish brand preference from usability/accessibility evidence;
- provide a high-quality design brief without inventing a universal MintTap style.

---

# Stage 5 — Accessibility & Inclusive Web

Goal: understand accessibility as a property of structure, content and interaction, not a final compliance check.

Study areas:
- disability and assistive-technology basics;
- semantic HTML;
- accessible names/roles/states;
- keyboard operation;
- focus order and focus visibility;
- landmarks and headings;
- forms/errors/instructions;
- contrast and non-color communication;
- zoom, reflow and text spacing;
- reduced motion and user preferences;
- images and alternatives;
- accessible status messages;
- mobile/touch accessibility;
- WCAG structure and conformance model;
- automated vs manual testing;
- accessibility statements and organizational practice.

Exit capability:
- identify common accessibility defects and their user impact;
- distinguish WCAG criteria from broader usability quality;
- define an accessibility validation plan.

---

# Stage 6 — Search, Discovery & Web Content Quality

Goal: understand how public web information is discovered, interpreted and represented.

Study areas:
- crawling, indexing and ranking concepts;
- robots.txt and sitemap;
- canonicalization;
- redirects and duplicate content;
- metadata/title/description;
- structured data;
- hreflang and international SEO;
- internal linking;
- content quality and intent alignment;
- information architecture effects on discovery;
- Open Graph/social preview concepts;
- app-store/web message continuity;
- app links/universal links from the user journey perspective;
- Search Console and diagnostics.

Exit capability:
- diagnose basic crawl/index/discovery problems;
- plan app/company pages that are understandable to both users and machines;
- avoid treating SEO as keyword stuffing.

---

# Stage 7 — Web Performance & Browser Runtime

Goal: understand why sites feel fast or slow and how design/content/engineering decisions interact.

Study areas:
- navigation lifecycle;
- critical rendering path;
- HTML/CSS/JS loading;
- render-blocking resources;
- images/fonts/media;
- caching;
- compression;
- lazy loading;
- CDN/edge delivery;
- Core Web Vitals;
- LCP/INP/CLS mechanics;
- lab vs field data;
- performance budgets;
- third-party scripts;
- perceived performance;
- performance-accessibility-conversion relationships.

Exit capability:
- identify likely performance causes rather than only symptoms;
- judge whether a visual/marketing decision has runtime cost;
- define measurable performance targets and validation methods.

---

# Stage 8 — Security, Privacy & Trust

Goal: understand the risk surface of a public app-company website.

Study areas:
- threat-model basics;
- HTTPS/TLS;
- same-origin concept;
- cookies and browser security boundaries;
- common web attack concepts: XSS, CSRF, injection, clickjacking;
- security headers and CSP concepts;
- authentication/session basics where applicable;
- secrets and deployment credentials;
- dependency/supply-chain risks;
- privacy by design;
- analytics/advertising consent implications;
- data minimization;
- trust signals vs deceptive trust theater;
- security/privacy communication to users;
- support abuse/phishing considerations.

Exit capability:
- recognize ordinary website security/privacy risks;
- know when specialist security/legal review is required;
- evaluate trust claims against evidence.

---

# Stage 9 — Analytics, Experimentation & Evidence-Led Improvement

Goal: learn how to improve a website using evidence rather than taste.

Study areas:
- business goal → user behavior → metric mapping;
- acquisition/conversion/support metrics;
- events and funnels;
- attribution limits;
- privacy-aware measurement;
- qualitative vs quantitative evidence;
- search analytics;
- support-query analysis;
- usability testing;
- A/B testing fundamentals;
- experiment validity and guardrails;
- vanity metrics;
- segmentation;
- cohort concepts;
- decision thresholds;
- instrumentation governance.

Exit capability:
- define a measurement plan before launch;
- distinguish signal from noise;
- recommend changes with an explicit evidence chain.

---

# Stage 10 — App-Company Web Strategy & Growth

Goal: integrate web knowledge into the specific needs of an Apple/Android app company.

Study areas:
- company site vs product site vs campaign site;
- one-app → multi-app growth;
- app launch lifecycle;
- prelaunch/launch/postlaunch web needs;
- store listing ↔ website continuity;
- product screenshots/demos/proof;
- pricing/subscription explanation;
- support/release-note/status architecture;
- account deletion and governance surfaces;
- deep linking and app acquisition;
- email/news/update surfaces where justified;
- developer/company credibility;
- international expansion;
- product retirement and URL lifecycle;
- cross-product navigation and brand architecture.

Exit capability:
- create a complete web strategy for a new MintTap app;
- identify what should live at company, app, support or store level;
- plan for future portfolio growth rather than a one-off launch page.

---

# Stage 11 — Web Operations & Platform Architecture

Goal: understand reliable operation without turning general study into an infrastructure project.

Study areas:
- hosting models;
- static generation, SSR, CSR and hybrid architecture;
- CDN/edge models;
- DNS operations;
- deployment environments;
- preview/staging/production;
- CI/CD concepts;
- observability and monitoring;
- uptime and incident response;
- redirects and URL migrations;
- backups/versioning/rollback;
- dependency/update management;
- provider trade-offs;
- cost, lock-in and portability;
- change management and release governance.

Exit capability:
- compare architecture/provider choices using project requirements;
- define operational safeguards;
- know when implementation validation is required without making POC work the curriculum itself.

---

# Stage 12 — Advanced / Expert Web Management

Goal: develop cross-disciplinary judgment for ambiguous real projects.

Study areas:
- portfolio-level web governance;
- design/content/engineering/legal/marketing coordination;
- architecture decision records;
- evidence confidence and uncertainty management;
- technical debt and content debt;
- large-scale localization governance;
- accessibility governance;
- privacy/security governance;
- analytics governance;
- web platform evolution;
- migration and replatforming strategy;
- brand/product architecture under growth;
- total cost of ownership;
- organizational ownership models;
- failure postmortems;
- systematic competitor/precedent analysis;
- distinguishing durable web principles from temporary industry fashion.

Exit capability:
- act as the web owner for a multi-product app company;
- integrate business, user, design, technical, policy and operational evidence;
- make explicit trade-offs and challenge weak assumptions;
- know which decisions can be made internally and which require specialists or real-world validation.

---

## Cross-cutting study method

Every stage should use a mixture of:
- authoritative standards/platform documentation;
- established usability/accessibility/security research;
- current browser/platform evidence where freshness matters;
- real website examples and counterexamples;
- failure-mode analysis;
- Design Studio evidence where visual/interaction questions overlap;
- small implementation experiments only when they answer a factual question that reading cannot settle.

Do not infer a rule from one attractive website.
Do not treat current trends as principles without evidence.
Do not confuse implementation familiarity with Web Manager expertise.

## Assessment model

At the end of each stage, the Web Manager should be able to:
1. explain the concepts from first principles;
2. correctly use the vocabulary;
3. diagnose representative problems;
4. compare plausible alternatives;
5. identify unknowns and specialist boundaries;
6. apply the knowledge to a hypothetical MintTap app-company scenario;
7. cite authoritative or high-quality evidence for material claims.

If these cannot be done, the stage is not complete even if research files exist.

## Current position

Existing 001–026 research gives meaningful partial credit across Stages 2, 5, 6, 8, 10 and 11, with especially strong prior work in launch requirements, governance, privacy/support architecture, SEO/localization/accessibility baselines and technical operations.

However, the curriculum will now deliberately return to **Stage 1 Web Foundations** and fill missing first-principles knowledge before continuing upward in sequence. Earlier advanced studies remain retained and will later be revisited from the stronger conceptual foundation.
