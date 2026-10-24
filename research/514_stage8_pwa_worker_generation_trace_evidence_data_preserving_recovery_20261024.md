# 514 — Stage 8 PWA Worker Generation, Trace Evidence Admission and Data-Preserving Recovery

Date: 2026-10-24 KST
Status: **SOURCE/SYNTHESIS + executable V8-adjudication model (24/24 synthetic cases) / PRODUCT BROWSER EXECUTION OPEN / Production validation OPEN / PWA release HOLD**
Canonical owner: **Track E — Web Architecture, Security & Operations**; Track A supplies browser lifecycle mechanics, Track C independently owns trace fidelity and test execution; B/D consume conclusions without duplicating E.

## 0. Canonical source refresh, scope and evidence boundary [SOURCE]
At run start read `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, studies 508 and 513, and latest Web Manager commits. Prior Web Manager HEAD was `5b92e85a424426b4646ca5d166cf98ef30466113`. Inspected read-only LogMate `main@27f926aa6ea1e032dfa9affc598e8e41131eb092` and exact `tool/pwa_precache.dart` blob `90a67954af618a4e18199fa92555491c56167c17`. Consulted Design Studio `case-studies/logmate/DESIGN_SYNTHESIS_GATE_20260919.md`, `progress/WEB_STATUS.md` (Stage 3 PRACTICE, W121 runtime/human/AT OPEN), Software Engineering Studio research index (Q006 semantic CI exit-status evidence and S007 auth/session boundary), and Marketing Manager STATUS (LogMate offline/PWA claims and ads not production-validated). These repositories were read-only.

**Important boundary:** This is a cross-generation *observation and evidence-admission* design. The earlier 508 read/modify/put counterexample and 513 first-claim probe remain canonical. This study neither reproduces a LogMate browser failure nor proves a correction, build, deployment, data loss, Safari capability, EFB policy or Sync.

## 1. Curriculum allocation and why this bottleneck [SYNTHESIS / DEPENDENCY]
Generic roadmap Stage 8 security/privacy/trust prerequisites have extensive prior coverage, but applied product evidence is weaker. Allocation by stage/gate, maturity, risk, relative depth and dependency pressure:

| Track | Relevant depth and current gap | Role in this bundle |
|---|---|---|
| A Platform/Browser | Service Worker install/wait/activate/claim, clientId/resultingClientId and CacheStorage fundamentals documented; **real two-generation trace OPEN** | Supply exact event/lifecycle/fetch semantics and browser-versus-OS distinctions. |
| B UX/IA/Content | Offline/update/reload task states defined; exact interruption, assistive-tech and managed-device comprehension OPEN | Consume precise readiness/error distinctions; no speculative UI promotion. |
| C Performance/Accessibility/Quality | 513 fail-closed probe tests, but loopback Chromium blocked and no exact NORMAL execution | Own independent response-hash, interception, negative controls and runner-failure taxonomy. |
| D Search/Analytics | Web acquisition and privacy measurement foundations mature; no real installed-PWA attribution | Consume sanitized aggregate verdicts only; prohibit unsupported install/offline claims. |
| E Security/Operations | 509–512 archive→host custody modeled; **Worker generation and repair/data authority unresolved** | Primary owner; integrate trace, release authority and data-preserving incident response. |

E receives the main allocation, A/C supply immediate prerequisites. This is not a sixth PWA specialist and does not repeat generic archive or typography primers.

## 2. Historical problem → principle → standard [SOURCE / SYNTHESIS]
AppCache's document-coupled update model was replaced by programmable Service Workers. That split is powerful but introduces separate *document*, *controller*, *worker generation*, *cache version*, *release artifact*, *data schema*, *storage partition* and *backup authority* lifetimes. No single READY boolean represents all eight.

- W3C Service Workers: https://w3c.github.io/ServiceWorker/ — lifecycle, fetch event client identity and claim semantics. Treat normative algorithm text separately from browser behavior.
- MDN Clients.claim (checked 2026-10-24): https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim — claim can control already network-loaded pages without retroactively intercepting the initial navigation.
- MDN Cache.put (checked 2026-10-24): https://developer.mozilla.org/en-US/docs/Web/API/Cache/put — same-key put replaces the prior cached response. CacheStorage is not a multi-writer compare-and-swap database.
- MDN Cache interface: https://developer.mozilla.org/en-US/docs/Web/API/Cache — app owns cache maintenance; HTTP cache-control does not govern Cache API retention.
- WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/ — origin quota/eviction and standalone policy; do not transplant Chrome persistence results to managed iPad.
- Playwright Chromium Service Worker instrumentation: https://playwright.dev/python/docs/service-workers — test API scope, not an iPadOS promise.

**Principle:** A worker can control a document without that document having been navigated under that worker. A Worker-local Promise queue cannot serialize two distinct Worker globals. A cached asset being valid does not establish a particular client is mapped to the correct version.

## 3. Exact LogMate implementation and source-grounded counterexamples [SOURCE / CONTRADICTION]
In `tool/pwa_precache.dart`, generated Worker uses `CONTROL_CACHE='logmate-offline-control-v2'` and `CONTROL_KEY='/__logmate_offline_control_v2.json'`. `readControl()` loads JSON or returns `emptyControl()`; malformed JSON is silently treated as empty. `writeControl()` uses `Cache.put`. `updateControl()` serializes with a Promise **inside this worker**, not across generations. `rememberManifest()` mutates shared `versions` and `candidateBuildId`.

During `activate`, the Worker updates the catalogue, then calls `clients.claim()`; it deliberately avoids `skipWaiting()` and automatic cache deletion. On intercepted root navigation, `clientId` and `resultingClientId` are mapped to `currentBuildId`. For later non-navigation same-origin GETs, the Worker looks up `clientBuilds[event.clientId]`. An unmapped request returns explicit 503 *before* checking whether the path is a known shell/font asset. For mapped requests it verifies exact cached bytes before serving.

**Conditional counterexample A — first claim:** the initial page was loaded by network, then claimed; its subsequent script/font request can lack a `clientBuilds` entry. `controller !== null` and candidate READY do not prove routability. A controlled root reload is a positive control, not proof of a repaired first page.

**Conditional counterexample B — two generations:** old active Worker and new installing Worker each read the same catalogue before either writes. Their separate Promise queues cannot prevent last-writer replacement of the other's client mapping or candidate metadata. No `skipWaiting()` limits activation behavior but does not by itself prove installing/active writes cannot overlap. Exact occurrence, ordering and impact are **OPEN**.

**Conditional counterexample C — repair by deletion:** clearing CacheStorage/IndexedDB to resolve a Worker error may destroy the offline shell and/or flight ledger; that is not an acceptable diagnostic or recovery shortcut. This study does **not** assert that the observed control-cache defect already caused flight-data loss.

**Conditional counterexample D — same appBuildId:** the shell-derived appBuildId excludes the generated Worker script. Two Worker implementations may therefore share the shell ID. Independent Worker SHA is required in runtime evidence and release inventory.

## 4. Independent trace evidence: no false-green promotion [VALIDATION / SYNTHESIS]
A new reusable, **research-only** fail-closed admission oracle lives at `research/handoffs/pwa_worker_trace_evidence_gate.js`. It takes a JSON trace from an independently instrumented Engineering runner. It does **not** drive a browser, obtain hashes, or authenticate the submitter. The runner must independently bind source commit, NORMAL release-tree SHA-256, Worker SHA-256, expected index/JS hashes, exact Chromium version, disposable profile, and local-loopback versus HTTPS origin. Producer assertions are not independent attestation.

Runtime phases in required order:
1. first network navigation;
2. late asset fetch on newly claimed page;
3. controlled navigation;
4. controlled asset fetch;
5. offline navigation;
6. offline asset fetch;
7. new browser process with same profile, offline navigation;
8. offline asset fetch after process reopen.

For each phase capture status, MIME, **actual response-body SHA-256**, whether controlled, independently observed Worker interception where controlled, enforced offline state and process epoch. The first navigation must be uncontrolled; later phases must be controlled by the expected Worker SHA. Explicit offline transport negative controls are required for both offline phases. A 200 HTML rewrite cannot pass as JavaScript; 200 with wrong bytes cannot pass; a controller claim without fetch interception cannot pass. Missing, malformed or environment-blocked evidence is **INCOMPLETE**, not PASS.

The verdict `BOUNDED_CHROMIUM_TRACE_PASS` means only that a supplied trace satisfies this oracle. It is not a verified actual Chromium run, release approval, independent telemetry attestation, accessibility test, physical iPad proof, 37-store restore, or native Sync evidence.

**False-green adversarial controls:** wrong browser family, bool-as-status, missing phase, process not restarted, claimed but unintercepted fetch, wrong Worker SHA, offline not enforced, absent offline negative control, unexpected MIME and hash mismatch. Each must fail closed.

## 5. Two-generation race observation protocol [VALIDATION / DEPENDENCY]
Use two **different Worker script hashes** and two different build IDs. Preserve a live old-version page while the new Worker installs. A test-only instrumented build may introduce barriers **after each generation reads the same catalogue revision but before either writes**. This must be a disposable test origin/profile with no user data. Record the old/new reads, revisions, writes, worker identities and a separate final catalogue readback *after both writes settle*.

Two controlled write orders must be tested:
- old write → new write: verify old live client's version mapping survives;
- new write → old write: verify new candidate/verified manifest survives.

The oracle requires both reads before either write, same initial revision, independently captured final readback, live old client and independently verified candidate. It returns `CATALOGUE_LOST_UPDATE_OBSERVED` if either required postcondition is absent; `BOUNDED_RACE_PRESERVATION_OBSERVED` only when both survive. An unforced ordinary update is **INCOMPLETE_INTERLEAVING**, not evidence of cross-worker serialization.

**Limits:** a synthetic trace can be fabricated. Even a real passing forced interleaving does not prove every timing schedule, WebKit parity, quota behavior, client lifecycle or durable ledger preservation. The existing 508 model demonstrates possible lost updates, not a browser reproduction. This oracle validates trace structure, not independent evidence acquisition.

## 6. Failure diagnosis, data-safe containment and remediation alternatives [MINTTAP DECISION CANDIDATE / OPEN]
Decision candidate: **Never repair an offline Worker 503 by deleting origin storage, silently reassigning an unknown client to the newest shell, activating an unverified candidate or claiming Sync/backup success.** Freeze destructive maintenance, preserve owner data and pending outbox, capture sanitized diagnostic state, then offer a controlled reload only when a proven compatible shell is available. Preserve distinction between Worker control, route assignment, cached bytes, local database durability and external backup.

Evaluate alternatives with explicit negative controls:
- **Defer first `clients.claim()`** until a controlled navigation or handshake establishes a safe client route; assess first-install UX latency and compatibility with existing pages.
- **Authenticated-by-context client→build handshake** using a page's known bootstrap version; same-origin messaging alone is not release authority and a stale page must not request arbitrary build assignment.
- **Immutable per-build catalogue + transactional pointer** with IndexedDB transactions and generation/fencing; verify upgrade from legacy v2 writer before assuming new lock prevents old writes.
- **Versioned immutable cache metadata with client-local mapping** avoiding one cross-generation mutable JSON; ensure live-client cleanup and process-reopen behavior.

Do not select a patch without source-level caller audit, repeated real-browser interleavings, schema/backup preservation and rollback exercises. No code change is authorized in LogMate by this study.

## 7. Engineering execution packet: twelve linked proof obligations [VALIDATION]
| Gate | Positive and negative evidence |
| --- | --- |
| G01 | Pin exact source SHA, NORMAL tree/Worker SHA, manifest and browser build; reject wrong Acceptance marker or unsigned self-assertion as release authority. |
| G02 | First network page then `clients.claim()`; late shell/unknown same-origin request; capture client IDs and 503/200 without inferring ledger loss. |
| G03 | Controlled root reload; prove client→build mapping and response hashes, not only status. |
| G04 | Offline reload and new-process offline reopen with same profile; independent network-negative controls. |
| G05 | Old/new Worker read barrier and both write orders; independently read final catalogue; reject no-overlap as PASS. |
| G06 | Worker-only change with identical shell appBuildId; distinguish Worker generation from shell identity. |
| G07 | Interrupted activation and corrupt/missing catalogue; preserve prior runnable shell; no silent empty-state promotion. |
| G08 | 1/100/5000 navigation cycles, closed-client pruning and quota/eviction; avoid deleting in-flight client mappings. |
| G09 | Exact NORMAL archive 509/512, served-byte 510 and separate release approval; never deploy Acceptance by default root. |
| G10 | Populated 37-store browser restore with R03/R04 collision, negative rollback and no invented Receipt/ACK; verify actual record semantics. |
| G11 | Safari tab, user Home Screen, managed Web Clip/full-screen as separate physical iPad/MDM cohorts with real backup/restore. |
| G12 | Accessibility of reload/offline/recovery states and privacy-minimal diagnostic/analytics claims; representative users and screen readers remain OPEN. |

Evidence taxonomy: `SOURCE` = exact generator/CI source; `MODEL` = synthetic interleaving; `TRACE ADMITTED` = independent instrumented test input passing oracle; `RUNTIME OBSERVED` = actual browser execution with provenance; `RELEASE APPROVED` = independently authorized artifact/host; `PRODUCT VALIDATED` = relevant data/MDM/runtime acceptance. These labels must not collapse.

## 8. Cross-track transfer and contradictions [TRANSFER VALIDATION / CONTRADICTION]
- **A→E:** `clients.claim()` does not retroactively process the original navigation; `Cache.put` is not a cross-worker transaction. Chromium observations do not imply WebKit behavior.
- **C→E:** a CI job green or synthetic trace admitted does not prove actual interception, exact response bytes, independent release authority or end-to-end data survival. Q006 requires semantic failures to propagate to job exit status.
- **E→B/Design Studio:** `READY` should be scoped to *candidate cached bytes*, not user-safe offline operation. A reload instruction must be recoverable, reversible where possible, and not claim data loss. W121 and CD127 exact-runtime/human gates remain OPEN.
- **E→D/Marketing:** log sanitized error class, browser cohort, build/Worker hash prefix only when needed and privacy-eligible; do not log flight records, credentials, client IDs, or detailed device lineage to general analytics. No EFB offline/auto-sync promotional claim before physical and architecture evidence.
- **Software Engineering transfer:** general code test quality, CI exit propagation and schema migration implementation belong to Engineering; this document supplies web-specific failure oracles, not a product patch.
- **Potential contradiction:** waiting Worker policy reduces uncontrolled takeover but does not prove no concurrent installer write. A single Worker-local lock and a shared JSON Cache key are not an origin-wide serialization guarantee.

## 9. Executed tests, limitations and evidence maturity [VALIDATION]
The **exact code sent to GitHub** was evaluated in the V8 connector runtime with 24 synthetic cases: 13 runtime trace cases and 11 race cases after additional false-green controls; **24/24 expected verdicts**. The gate uses strict integer status, SHA shape, browser family, explicit interception, process epoch, offline negative controls and independent final catalogue readback flags. These flags remain trace assertions, not cryptographic provenance. No Node binary, Playwright browser, LogMate build, Firebase host or physical iPad was executed in this run. The prior 513 Chromium navigation attempt was blocked by `ERR_BLOCKED_BY_ADMINISTRATOR`; no new successful browser observation supersedes it.

**Important caveat:** even `BOUNDED_CHROMIUM_TRACE_PASS` from this file is a classification of provided JSON, not proof the runner collected the JSON honestly. Require Engineering-controlled capture, archived raw test logs, independent receipt, source SHA and runner/CI provenance. Do not use this oracle alone as a release gate.

## 10. Decisions, change watch, adjacent-value check and next meaningful gate [MINTTAP DECISION / OPEN / CHANGE WATCH]
**Decision:** Keep applied Stage 8 ACTIVE, E primary, A/C dependencies; **Production validation OPEN / PWA release HOLD**. No new product bug or data-loss incident is declared. LogMate and specialist repositories remain unchanged.

**OPEN:** actual NORMAL G1→G2 archive, independent release approval, served HTTPS bytes, real Chromium first claim and two-Worker forced interleaving, real browser-process restart, populated 37-store semantic restore/R03–R04, Safari/iPadOS/managed EFB install and storage, native-mobile Sync feasibility, human/accessibility evidence.

**CHANGE WATCH:** Service Worker standard and Chrome/WebKit lifecycle differences, Cache API storage/eviction, browser runner and Playwright capabilities, generated Worker/source hashes, Flutter/SDK build provenance, GitHub artifact formats and CI action versions, Apple managed Web Clip and Home Screen storage policy.

**Adjacent-value check:** The next adjacent high-information-gain step is no longer another model-only primer; it is Engineering-controlled **real two-generation browser instrumentation and actual NORMAL archive**. Additional synthetic cases without new failure semantics would add little value. Stop at this meaningful evidence boundary rather than fabricate product validation.
