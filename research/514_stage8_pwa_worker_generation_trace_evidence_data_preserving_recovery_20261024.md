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
The **exact code sent to GitHub** was evaluated in the V8 connector runtime with 24 synthetic cases: 15 runtime trace cases and 9 race cases after additional false-green controls; **24/24 expected verdicts**. The gate uses strict integer status, SHA shape, browser family, explicit interception, process epoch, offline negative controls and independent final catalogue readback flags. These flags remain trace assertions, not cryptographic provenance. No Node binary, Playwright browser, LogMate build, Firebase host or physical iPad was executed in this run. The prior 513 Chromium navigation attempt was blocked by `ERR_BLOCKED_BY_ADMINISTRATOR`; no new successful browser observation supersedes it.

**Important caveat:** even `BOUNDED_CHROMIUM_TRACE_PASS` from this file is a classification of provided JSON, not proof the runner collected the JSON honestly. Require Engineering-controlled capture, archived raw test logs, independent receipt, source SHA and runner/CI provenance. Do not use this oracle alone as a release gate.

## 10. Decisions, change watch, adjacent-value check and next meaningful gate [MINTTAP DECISION / OPEN / CHANGE WATCH]
**Decision:** Keep applied Stage 8 ACTIVE, E primary, A/C dependencies; **Production validation OPEN / PWA release HOLD**. No new product bug or data-loss incident is declared. LogMate and specialist repositories remain unchanged.

**OPEN:** actual NORMAL G1→G2 archive, independent release approval, served HTTPS bytes, real Chromium first claim and two-Worker forced interleaving, real browser-process restart, populated 37-store semantic restore/R03–R04, Safari/iPadOS/managed EFB install and storage, native-mobile Sync feasibility, human/accessibility evidence.

**CHANGE WATCH:** Service Worker standard and Chrome/WebKit lifecycle differences, Cache API storage/eviction, browser runner and Playwright capabilities, generated Worker/source hashes, Flutter/SDK build provenance, GitHub artifact formats and CI action versions, Apple managed Web Clip and Home Screen storage policy.

**Adjacent-value check:** The next adjacent high-information-gain step is no longer another model-only primer; it is Engineering-controlled **real two-generation browser instrumentation and actual NORMAL archive**. Additional synthetic cases without new failure semantics would add little value. Stop at this meaningful evidence boundary rather than fabricate product validation.


## 11. 2026-10-28 — Executed Chrome Worker update, offline process-reopen and mixed-generation negative control [SOURCE / VALIDATION / CONTRADICTION]

**Provenance and scope.** The new [disposable Playwright Python browser probe](handoffs/pwa_worker_lifecycle_browser_probe.py) and [GitHub Actions workflow](../.github/workflows/stage8_pwa_worker_lifecycle_browser.yml) exercise a deliberately small **synthetic** Service Worker / CacheStorage / IndexedDB app. It is NOT the LogMate generated Worker, a 37-store Sembast database, a NORMAL build, HTTPS Hosting, Safari, Home Screen app or managed EFB. It uses a temporary browser profile, localhost trustworthy-origin exception, and one invented operation ID; no personal pilot records, real Auth or product data. Exact hosted [run 40625164455](https://github.com/yhappcom/web-manager/actions/runs/40625164455), checkout d48b677ad31c1e3d79cc02a5c299277c30c35160, completed SUCCESS: **16/16 named browser assertions**, Python 3.13.16 / Playwright 1.57.0 / Chrome 155.0.8059.39. A sanitized evidence JSON artifact was uploaded. This does NOT retroactively close 513's actual LogMate first-claim probe or 514's forced two-generation shared-catalogue race.

**Standards and current primary sources, checked 2026-10-28:**
- [W3C Service Workers](https://w3c.github.io/ServiceWorker/): separate registration/Worker/cache lifetimes; Cache API entries are author-managed and do not update merely because Worker code changes.
- [MDN register()](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register) and [updateViaCache](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache): script same-origin/secure-context requirements, HTTP cache policy for Worker script/imports, not CacheStorage or the ledger. Localhost is a development trustworthy-origin exception, not a production HTTPS proof.
- [web.dev lifecycle](https://web.dev/articles/service-worker-lifecycle) and [MDN skipWaiting](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting): waiting workers, old controlled clients, explicit takeover, controllerchange and mixed-version risk.
- [MDN storage quotas/eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria): IndexedDB commit, process reopen and StorageManager persistence observation are not external backup or guaranteed survival through user deletion, quota pressure, device loss or MDM reprovisioning.
- [WebKit Safari 26](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/): Home Screen web-app entry no longer requires a manifest or Worker; File System WritableStream support is not proof of an approved managed Files destination. [WebKit 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/): creation-time cookies can be copied, but not IndexedDB or other local storage.

**Actual browser oracles, grouped by independent failure domain:**

| Domain | Named cases and exact bounded result |
| --- | --- |
| First navigation / control | SW01 first document network/uncontrolled; SW02 later claim intercepts asset but not original navigation; SW03 IndexedDB transaction commits synthetic sentinel; SW04 independent second tab reads it. |
| Waiting and old clients | SW05 v2 cache exists while v1 still serves two controlled clients; SW06 closing only one client leaves v2 waiting; SW07 after releasing old clients and race-aware admission, v2 serves controlled navigation. |
| Offline / process lifecycle | SW08 synthetic cache cleanup preserves IndexedDB; SW09 offline cached navigation succeeds while uncached request fails; SW10 new Chrome process/same profile reopens offline shell and IndexedDB; SW10B explicitly verifies a controlled v2 client before next update. |
| Unsafe takeover / containment | SW11 deliberately forcing v3 activation makes still-open v2 document fetch v3 asset; SW12 IndexedDB sentinel survives; SW13 reload reconciles shell; SW14 intentionally failing v4 install (with independent v4 script-fetch counter) leaves v3 active and ledger intact; SW15 StorageManager status observed without calling it a backup. |

**Failure-first history retained [CONTRADICTION]:**
- [40624878099](https://github.com/yhappcom/web-manager/actions/runs/40624878099): SW01–SW06 PASS, SW07 FAIL; new tab was created immediately after old clients closed.
- [40624950277](https://github.com/yhappcom/web-manager/actions/runs/40624950277): diagnostic showed v1 cached document/asset while both v1 and v2 caches existed. The test had incorrectly assumed instant activation; this is not a product or standards failure.
- [40625029890](https://github.com/yhappcom/web-manager/actions/runs/40625029890): race-aware SW07 and SW08–SW10 passed; v3 waiting-worker message failed because the supposedly old client was not independently established as controlled.
- [40625094451](https://github.com/yhappcom/web-manager/actions/runs/40625094451): added controlled v2 reload, **16/16 PASS**. [40625164455](https://github.com/yhappcom/web-manager/actions/runs/40625164455): required a verified v4 script fetch to avoid a false-green failed-install claim; **16/16 PASS**. Earlier failed runs are fixture scheduling/oracle defects, not LogMate data loss.

**Critical product contrast:** Read-only [LogMate generated-Worker source](https://github.com/yhappcom/logmate/blob/main/tool/pwa_precache.dart) at main d3bc214fe9b4b7bf84702f898b4e6993a4127e2f (file blob 90a67954af618a4e18199fa92555491c56167c17) **does not call skipWaiting and does not automatically delete old caches**. It uses shared CacheStorage control metadata and client-to-build mappings; an unassigned client can receive explicit 503. Synthetic SW08 automatic cache cleanup and SW11 forced takeover are deliberately unsafe contrast cases, NOT claims about LogMate. The actual product's first-claim unmapped-client path, cross-generation catalogue writes, Worker-only change under identical shell ID, populated 37-store recovery and external backup remain runtime OPEN.

**Five-track allocation / transfer:** E owns Worker-script trust, release/rollback and data custody; A supplies lifecycle, scope, fetch, browser/OS semantics; C owns exact-job first-failure and negative controls, but lacks product NORMAL/host/body-hash/device evidence; B consumes Design Studio W121/CD127's truthful offline/reload/recovery states; D consumes Marketing D8's PWA/EFB claim HOLD and must not count synthetic Chrome tests as installation or successful Sync. Engineering M006 owns generic Chromium/Safari validation; this web-specific fixture adds update-mixing and web-release custody, not a duplicate of Engineering's discipline.

**MINTTAP DIRECTION (not product approval):** Avoid forced activation and origin-storage clearing as generic repair shortcuts. Preserve local ledger/outbox while resolving shell update; require independent source→NORMAL→served host→Worker/client→37-store data→external backup→managed EFB evidence. A successful graceful browser restart is not physical crash durability. **Stage 8 ACTIVE · Synthetic Chrome 16/16 PASS at the cited exact ref · Production validation OPEN · PWA release HOLD.**

**Adjacent-value check:** The next useful question requires the **exact LogMate NORMAL build and generated Worker**, then actual client mapping, two-generation catalogue interleavings, source/host bytes, populated 37-store restore and Safari/Home Screen/MDM Web Clip. Another generic synthetic Worker primer would have lower information gain. No peer or product writes.


## 12. Final stricter two-client rerun and exact pinned CI [VALIDATION / CONTRADICTION]

**2026-10-28 03:12 UTC.** The source-only change to pin checkout/setup-python/upload-artifact actions at exact upstream commits was followed by [run 40625208322](https://github.com/yhappcom/web-manager/actions/runs/40625208322), checkout 8b22de2c. It **FAILED** after SW01–SW10B because a waiting v3 worker disappeared before the script could send the forced-activation message. The earlier 16/16 result remains valid for its own exact checkout; it does not prove this update interleaving is deterministic. The failure is a **research-fixture timing/identity oracle** until independently established otherwise, not evidence of a LogMate product defect or an upstream browser defect.

The next fixture revision adds an explicit Service Worker MessageChannel version response and keeps **two independently verified v2-controlled tabs** alive during v3 installation. This ensures that a v2 asset being present is not mistaken for the current controller identity. Exact [GitHub Actions run 40625336045](https://github.com/yhappcom/web-manager/actions/runs/40625336045), job 122608779318, tested checkout **a066d6038aff7d05cb000da1d1a2354c9d0e1d6c** with SHA-pinned checkout/setup-python/upload-artifact actions, Python 3.13.16, Playwright 1.57.0 and Chrome 155.0.8059.39: **SW01–SW15 plus SW10B/SW10C = 17/17 browser assertions PASS, zero failures; bounded verdict BOUNDED_SYNTHETIC_CHROMIUM_PASS.** The intentionally unsafe mixed v2 document/v3 asset path was observed, then v3 reload reconciled; synthetic IndexedDB persisted across graceful Chrome process reopen and the test's Worker updates. The failing v4 install had a separately counted v4 script fetch and left the v3 shell/IndexedDB intact. A sanitized JSON evidence ZIP was uploaded, artifact ID **12789495045 belonged to the earlier 16-case run**, not this exact 17-case run; do not substitute artifact identities across commits.

**What the correction teaches:** Worker lifecycle tests must bind the **actual controller generation of each live client** before asserting waiting/activation semantics. A page displaying cached v2 HTML or receiving a v2 asset alone is not sufficient. The first failed run at SW07 and the pinned-run disappearance of waiting are not grounds to weaken the oracle to a green status; they motivated new independent version identification and two-client admission. This is a substantive A/C→E transfer, not a change to product policy.

**Final evidence gate:** Applied Stage 8 ACTIVE; **synthetic actual Chrome 17/17 PASS** at a066d603; actual LogMate NORMAL/Worker/client map, 37-store Sembast restore, HTTPS host, Safari/iPadOS Home Screen/MDM Web Clip and native-mobile Sync **OPEN**; PWA release **HOLD**. The next useful work requires real product build/runtime and managed-device evidence, not additional generic synthetic Worker iterations.
