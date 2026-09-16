# Web Manager Specialist Track Operating Model

Status: **ACTIVE**  
Established: 2026-09-16

## Purpose

`yhappcom/web-manager` remains one canonical Web Manager knowledge base, but learning is now organized as five cooperating specialist tracks plus one coordinating Web Manager role. The purpose is to develop genuine depth without fragmenting the organization into isolated repositories or duplicating the same research.

The 12-stage `LEARNING_ROADMAP.md` remains the vertical beginner→expert curriculum. The specialist tracks are the horizontal expertise model. A stage can involve several tracks, and a track can deepen across many stages.

## Coordinator — Web Manager

The Web Manager is not a sixth specialist. It coordinates the five tracks, compares maturity and evidence gaps, allocates learning effort, integrates conclusions for app-company website decisions, manages cross-domain dependencies, and decides when a curriculum gate has sufficient evidence.

The coordinator must not force equal research volume. Work is allocated according to prerequisite gaps, risk, transfer value, evidence maturity, live-project relevance and dependency pressure.

## Track A — Web Platform & Browser

Owns reusable knowledge of how the Web itself works:
- Internet/Web boundary, URL/origin/host/resource models;
- DNS, HTTP, HTTPS/TLS and protocol evolution;
- browser architecture and navigation lifecycle;
- HTML/CSS/JavaScript platform mechanics;
- DOM and browser runtime;
- cookies, storage, sessions, cache and service workers;
- same-origin/CORS platform mechanics;
- HTTP/1.1, HTTP/2, HTTP/3, TCP/QUIC relationships;
- proxy/CDN/intermediary behavior at the platform layer;
- browser/network evidence interpretation.

This track supplies foundational mechanics to Security, Performance, Search and Operations rather than those tracks relearning the protocol from zero.

## Track B — Web UX, IA & Content Architecture

Owns web-specific information and task structure:
- website purpose, audience, intents and journeys;
- information architecture, taxonomy and navigation;
- page systems and content hierarchy;
- support/privacy/legal/product/company surface relationships;
- responsive information hierarchy and wayfinding;
- forms, states, task continuity and web interaction requirements;
- content models, lifecycle and localization structure;
- app↔web information continuity.

Design Studio remains canonical for reusable visual/interaction design expertise. This track translates product/site needs into web structure and requirements and consumes Design Studio evidence rather than duplicating Type, Color, Layout/Interaction or general design research.

## Track C — Web Performance, Accessibility & Quality

Owns evidence-led web quality:
- loading/rendering/runtime performance;
- Core Web Vitals and task-readiness evidence;
- resource priority, media/font/JS/CSS cost and third-party cost;
- performance budgets and regression governance;
- semantic/accessibility implementation requirements;
- keyboard/focus/reflow/zoom/preferences/assistive-technology concerns;
- cross-browser/device compatibility;
- quality validation, failure diagnosis and regression evidence.

Accessibility and performance remain distinct quality dimensions even though they share runtime and release evidence. Neither may be reduced to a single automated score.

## Track D — Search, Discovery & Analytics

Owns discoverability and measurement:
- crawling, indexing and search diagnostics;
- canonicalization, redirects, sitemap/robots and structured data;
- international discovery/hreflang;
- social preview and app-store↔web discovery continuity;
- Search Console and search evidence;
- analytics/event/funnel design;
- attribution limitations and privacy-aware measurement;
- experimentation, validity, segmentation and decision thresholds;
- evidence-led content/site improvement.

Marketing Manager owns broader acquisition/market/community strategy. This track owns web/search/measurement mechanics and hands evidence across the boundary when relevant.

## Track E — Web Architecture, Security & Operations

Owns reliable and defensible operation:
- hosting/runtime architecture and deployment models;
- CDN/edge/origin topology and DNS operations;
- security threat models and browser/server trust boundaries;
- XSS/CSRF/injection/clickjacking concepts and mitigations;
- CSP/security headers/auth/session boundaries where relevant;
- privacy, cookies/storage/data minimization and third-party risk;
- dependency/supply-chain and secret/deployment risk;
- environments, CI/CD, monitoring, incidents and rollback;
- migrations, redirects, backup/versioning and lifecycle operations;
- provider trade-offs, portability, cost and lock-in.

Software Engineering / Code Specialist, when available, owns general implementation/code/software-engineering expertise. This track owns web-architecture and web-operations requirements and exchanges implementation evidence rather than absorbing the software-engineering discipline.

## Cross-track operating rule

One track is the canonical owner of a reusable finding. Other tracks consume it through `DEPENDENCY`, `TRANSFER VALIDATION`, `CONTRADICTION` or integration analysis. They do not independently repeat the same foundation unless replication is necessary to resolve uncertainty.

Example: Platform & Browser establishes HTTP caching semantics. Performance applies those semantics to latency/resource reuse; Search applies status/redirect/cache behavior to crawler outcomes; Architecture/Operations applies it to CDN/origin policy. Those tracks should not each write a new HTTP primer.

## Balanced learning loop

At the start of each autonomous learning run, the Web Manager compares all five tracks using:
1. current curriculum stage and gate;
2. missing foundational prerequisites;
3. evidence maturity: SOURCE → SYNTHESIS → diagnostic/application ability → validation/transfer evidence;
4. cross-track dependency pressure;
5. live-project relevance and risk;
6. depth relative to adjacent tracks.

The highest-value bottleneck receives the largest share of the run. Other tracks may receive integration/transfer work when it materially improves the same learning bundle. Equal work allocation is explicitly not required.

## Work-volume and cadence rule

The hourly automation is a scheduling cadence, not a one-hour-sized syllabus unit. Each run should use the available execution window productively and continue through logically adjacent work rather than stopping after one easy subtopic.

A normal run should aim for a **substantial integrated bundle** equivalent to roughly 8–12 former micro-study blocks when the subject permits. This is a scope heuristic, not a quota. Quality and evidence take priority over artificial volume.

Before ending a run, ask:
- Is there another directly adjacent high-value question that can be responsibly completed now?
- Can the current evidence be integrated or stress-tested rather than merely summarized?
- Is a track waiting on a dependency that can be resolved in this same run?
- Would stopping now create an avoidable idle gap before the next hourly trigger?

Continue when the answer is yes and tool/runtime limits permit. Stop when a meaningful checkpoint is reached, evidence becomes blocked, the next work requires materially different context, or execution limits make continuation unsafe.

Do not manufacture filler to consume time. Minimizing idle space means increasing useful integrated work per run, not padding research.

## Persistence/reporting rule

Prefer domain-level or stage-level integrated research over many tiny files. Persist meaningful specialist ownership/dependencies in the research artifact and keep `STATUS.md` concise.

User-facing reporting should summarize substantial checkpoints only. The automation may run hourly without producing a user-visible micro-report every hour.

## External specialist relationships

- **Design Studio** → reusable visual/interaction/design expertise.
- **Marketing Manager** → market, acquisition, community and promotion expertise.
- **Software Engineering / Code Specialist** → general implementation, code quality, testing and software architecture expertise.
- **Web specialist tracks** → web-medium-specific platform, structure, quality, discovery and operations expertise.
- **Web Manager** → integrates these into website strategy, requirements, evidence and operational decisions.

Cross-repository work must respect each repository's canonical ownership and handoff rules.