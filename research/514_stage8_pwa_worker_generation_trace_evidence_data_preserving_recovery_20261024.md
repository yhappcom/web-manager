# 514 — Stage 8 PWA Worker Generation, Trace Evidence Admission and Data-Preserving Recovery

Date: 2026-10-24 KST
Status: **SOURCE/SYNTHESIS + Chrome synthetic 17/17 executed / LogMate W-031 iPadOS Safari Simulator ACCEPTANCE HARNESS PARTIAL (product-recorded) / NORMAL + physical/managed EFB OPEN / Production validation OPEN / PWA release HOLD**
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

The next fixture revision adds an explicit Service Worker MessageChannel version response and keeps **two independently verified v2-controlled tabs** alive during v3 installation. This ensures that a v2 asset being present is not mistaken for the current controller identity. Exact [GitHub Actions run 40625336045](https://github.com/yhappcom/web-manager/actions/runs/40625336045), job 122608779318, tested checkout **a066d6038aff7d05cb000da1d1a2354c9d0e1d6c** with SHA-pinned checkout/setup-python/upload-artifact actions, Python 3.13.16, Playwright 1.57.0 and Chrome 155.0.8059.39: **SW01–SW15 plus SW10B/SW10C = 17/17 browser assertions PASS, zero failures; bounded verdict BOUNDED_SYNTHETIC_CHROMIUM_PASS.** The intentionally unsafe mixed v2 document/v3 asset path was observed, then v3 reload reconciled; synthetic IndexedDB persisted across graceful Chrome process reopen and the test's Worker updates. The failing v4 install had a separately counted v4 script fetch and left the v3 shell/IndexedDB intact. A sanitized JSON evidence ZIP was uploaded as **artifact 12789092775** for this exact run; do not substitute earlier 16-case artifacts across commits.

**What the correction teaches:** Worker lifecycle tests must bind the **actual controller generation of each live client** before asserting waiting/activation semantics. A page displaying cached v2 HTML or receiving a v2 asset alone is not sufficient. The first failed run at SW07 and the pinned-run disappearance of waiting are not grounds to weaken the oracle to a green status; they motivated new independent version identification and two-client admission. This is a substantive A/C→E transfer, not a change to product policy.

**Final evidence gate:** Applied Stage 8 ACTIVE; **synthetic actual Chrome 17/17 PASS** at a066d603; actual LogMate NORMAL/Worker/client map, 37-store Sembast restore, HTTPS host, Safari/iPadOS Home Screen/MDM Web Clip and native-mobile Sync **OPEN**; PWA release **HOLD**. The next useful work requires real product build/runtime and managed-device evidence, not additional generic synthetic Worker iterations.


## 13. 2026-10-28 — LogMate W-031 iPadOS Safari Simulator product-evidence transfer and NORMAL release differential [SOURCE / VALIDATION / CONTRADICTION / TRANSFER VALIDATION]

### A. Provenance and exact source continuity [SOURCE]

This checkpoint independently **reads** existing product-recorded simulator evidence and exact product source blobs. It does not execute a new browser, build or physical-device test. Earlier blanket wording that LogMate has no browser runtime evidence is too broad: there is **bounded LogMate ACCEPTANCE HARNESS Safari Simulator evidence**, not NORMAL production validation.

- Read-only product HEAD: [LogMate main d3bc214](https://github.com/yhappcom/logmate/commit/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f). W-031 PWA artifact source: **7caaee998251602e72159eeebda61f701bdea270**; later follow-up execution: **d346694ea17a57a093ede203a94c70aa98738f7f**. A later documentation/Native merge is not a new PWA build.
- Evidence: [W-031 narrative](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-simulator-preacceptance-2026-10-27.md), [initial structured runtime](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-simulator-2026-10-27/runtime-summary.json) blob **9fae1dccc8c69b7e1bee2831ebee8419574c0968**, and [Safari follow-up JSON](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-safari-followup-2026-10-27/results.json) blob **0f04987eb71742222166d5fe0dcc520afd8f2be2**. These are product-reported observations, not newly independently executed results.
- GitHub blob SHA comparison between artifact-source ref and current product HEAD: **tool/pwa_precache.dart** 90a67954af618a4e18199fa92555491c56167c17; **web/flutter_bootstrap.js** a70625e8bda32aafd5dd23822c017d05229f0e63; **web/manifest.json** 8225e76fe032e792c30b0f22efa1f7cafab68119; **lib/debug/persistence_acceptance_harness.dart** 226a6ccce2aca8dc38bc21622359050b925b89da. All four source blobs match across refs; this does NOT prove full tree/dependencies, generated artifacts or NORMAL entrypoint are unchanged.
- Recorded PWA ACCEPTANCE artifact: **appBuildId 2b515d6c9cf282b2a42b186f45c7b5ea**, **databaseCapability 17**, **API version 2**, **main.dart.js SHA-256 46d9015b61e097713349b9c5bc463e33a3188f65471c6b1d56f646d368dbff76**. Environment: iPad Pro 11-inch M5 Simulator, iPadOS 26.1 build 23B86, Safari 26.1, origin http://127.0.0.1:49331. Acceptance entrypoint bypasses SessionGate and uses an unbound synthetic Flight; it is not a matching-Firebase-UID product test.
- Source bootstrap registers the owned /logmate_service_worker.js with updateViaCache none. Generated Worker maintains verified versions, deliberately avoids automatic skipWaiting and cache deletion. Therefore §12's **intentionally forced** Chrome mixed-version counterexample is not proof that LogMate takes the same path. The cross-generation control-cache race described in §3 remains a conditional hypothesis, not a W-031 observation.

### B. What is observed vs what is still OPEN [VALIDATION / CONTRADICTION]

| Evidence layer | W-031 observation | Narrow admissible conclusion |
| --- | --- | --- |
| Build | make build-pwa-acceptance exited 0; generated Worker/font/shell checks | Acceptance artifact build only; NORMAL build and deployed HTTPS bytes OPEN |
| Safari runtime | Actual iPadOS 26.1 Simulator Safari tab opened loopback harness | Simulator Safari tab, not physical managed EFB |
| Worker activation | WebDriver ready initially activating; later statechange to activated; registration scope and script observed | WebDriver-context activation PASS; ready alone is not activation |
| Client control | WebDriver root reload observed active controller /logmate_service_worker.js | WebDriver context PASS; ordinary Safari-tab controller and first-claim late asset G02 OPEN |
| Storage | Ordinary Safari raw 21 Sembast entries retained across process reopen; WebDriver context independently 15→19 entries and same-session stable read | Two separate context-specific fixture observations; not 37-store NORMAL restore |
| Offline | Test-owned loopback server stopped, curl failed, Safari terminated/reopened root showing cached fixture | Origin-unavailable cached relaunch only; not airplane mode, OS reboot or offline authenticated edit |
| UI and accessibility | WebDriver click intercepted, semantic text empty, unusable UI screenshot | UI/AT/interaction NOT VERIFIED despite Worker and IndexedDB observations |
| Home Screen | Share sheet appeared, installation action unavailable to automation | Installed PWA NOT VERIFIED; no Safari→Home Screen data transfer claim |
| Managed Web Clip | No MDM profile, airline policy, full-screen Web Clip or physical EFB involved | NOT RUN |
| Owner/Sync | SessionGate bypass, unbound fixture, no verified Firebase UID or remote server | Auth/Owner/Manual Sync/Receipt/Cursor NOT RUN |
| Data recovery | Local process restart, not backup→loss→restore or reprovision | Bounded same-origin persistence, not independent recovery or indefinite durability |
| Native | Separate acceptance-flavor iOS/Android Simulator process-persistence evidence; Production default compile-only | Native harness does not transfer to installed PWA or production Sync |

**Independent-oracle warning:** ordinary Safari read-only 21-entry hash **a06c90de776388addc77ddbbf2e585897f5ef7ec208fe024206063d3f3796470** and WebDriver context 19-entry hash **730c2c1363bbec2109a516d7656db4457ebcbd73d5775e31205d31b87761e424** arise from different storage contexts and hashing procedures. Their inequality does not show corruption; their separate persistence does not show Home Screen data sharing. Raw Sembast entries are not the count of LogMate's 37 logical stores or Flights.

### C. Platform standard and managed-iPad policy boundary [SOURCE / CHANGE WATCH]

- [WebKit Safari 26.0, 2025-09-15](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/): Home Screen entry on iOS/iPadOS 26 can open as a web app without a manifest or Service Worker. This is entry behavior, not offline support or airline MDM permission.
- [WebKit Safari 17.2, 2023-12-11](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/): newly created Home Screen web apps may copy login cookies, but no other local storage; later website data is not shared. Cookie/session continuity, ledger migration and current Owner authority require separate evidence.
- [WebKit storage policy, 2023-08-10](https://webkit.org/blog/14403/updates-to-storage-policy/): IndexedDB, Cache Storage and Service Worker storage face quota and eviction conditions; a local write or persist grant is not backup.
- [Apple WebClip payload](https://developer.apple.com/documentation/DeviceManagement/WebClip?language=swift) and [Apple deployment guide](https://support.apple.com/en-gb/guide/deployment/depbc7c7808/web): managed com.apple.webClip.managed and FullScreen are distinct provisioning controls; neither guarantees airline permission, PWA data migration or unattended Sync.
- W-031 WebDriver reported secureContext true for loopback. That is NOT evidence for production HTTPS host, TLS/CSP, deployed Worker scope, Firebase authenticated endpoint or storage continuity across origin change.

### D. Next integrated product acceptance, with negative controls [MINTTAP DIRECTION / DEPENDENCY / OPEN]

1. **NORMAL artifact custody (E/A/C):** Engineering-owned clean NORMAL Flutter Web build, locked dependency graph, generated Worker SHA separate from shell appBuildId, manifest, asset digest/count, served HTTPS inventory, base href and acceptance-marker negative control. W-031 Acceptance appBuildId is not a NORMAL release identity.
2. **First-control and update (A/C/E):** On exact NORMAL build, first network page → Worker install/claim → late same-origin shell/unknown asset → controlled root reload; capture controller generation, clientId/resultingClientId, mapping, response status and digest. Add old/new Worker write barriers, waiting/activation and failed-update independent control-cache oracle; never clear IndexedDB or Cache Storage to make a test pass.
3. **Context migration (A/E/C):** On disposable iPad profile, seed a non-sensitive known record/operation nonce in Safari, then separately create Home Screen app and policy-approved MDM Web Clip. In each context independently inventory origin, install identity, cookies, IndexedDB store list/nonce, Worker controller, offline cold launch, storage quota and verified restore. Assume no data copy; if absent, use explicit product-authorized import while retaining old data.
4. **Ledger/authority (E/C; Engineering implementation owner):** matching verified UID, locked/wrong Owner, 37-store whole-ledger LBK restore, stable identity/revision/tombstone/outbox/cursor, repeated-restore collisions, offline edit/reopen and current Owner check. Local commit, pending Sync, server receipt and convergence must be distinct oracles.
5. **Failure and recovery (E/A/C):** On disposable data with independent backup, distinguish origin-down from all-network-down, failed Worker install, quota pressure, corruption, OS reboot, app deletion, reprovision, token expiry and Owner transfer. Only policy-approved foreground Manual Sync may be tested; do not infer hotspot or unattended background communication.
6. **UX and claims (B/D):** Design Studio W121 owns human/AT validation of Saved locally, Backup verified, Pending Manual Sync, Owner verification required and Offline shell ready. Marketing D8 retains public claim HOLD; privacy-minimal measurement must not collapse icon, cold offline, restored ledger, receipt and convergence into one install metric.

### E. Five-track allocation and exit judgment [SYNTHESIS / TRANSFER VALIDATION]

| Track | Evidence maturity and gap | Responsibility |
| --- | --- | --- |
| E primary | Synthetic Chrome and Firebase security evidence mature; NORMAL release identity, authenticated data custody and managed EFB not validated | Security/release authority, data-preserving recovery, context transition |
| A dependency | Product Worker source verified and W-031 Safari harness controller observed; first-claim, Home Screen and MDM still OPEN | Browser mechanics, Worker generations and OS/browser separation |
| C independent oracle | Chrome 17/17 and product-recorded Safari harness are different scopes; WebDriver UI oracle failed | Exact artifact, store, response, accessibility and failure-negative evidence |
| B consumer | Design Studio Web Stage 3 PRACTICE / W121 human/AT OPEN | Truthful offline/update/restore/denial states, not speculative visual PASS |
| D consumer | Marketing D8 product-claim HOLD | Separate install, offline, backup, owner, receipt and convergence measurement |

**Gate:** Applied Stage 8 ACTIVE · **Chrome synthetic 17/17 PASS** at exact prior ref · **LogMate Safari Simulator ACCEPTANCE HARNESS PARTIAL** (product-recorded) · **Production validation OPEN · PWA release HOLD**. This run adds SOURCE/TRANSFER reconciliation only; no new browser execution, NORMAL product validation or peer-repository changes.

**Adjacent-value check:** Another generic Worker synthetic variation has lower information gain than the exact NORMAL artifact, 37-store runtime and physical/managed iPad. Stop at this substantive source-evidence checkpoint rather than manufacture filler.


## 14. 2026-10-28 — Cross-generation control-catalogue concurrency: Chrome falsification harness [SOURCE / SYNTHESIS / VALIDATION / OPEN]

### Why this is a different failure class

The ordinary Service Worker update lifecycle allows a new Worker to **install while the previous Worker still controls an open tab**. This is not `skipWaiting()` and not the mixed-document problem from §12. The two Worker global scopes may both access origin-shared Cache Storage. A JavaScript promise queue scoped to **one** Worker global does not establish a cross-generation atomic read/modify/write. Primary references: [Service Workers specification](https://w3c.github.io/ServiceWorker/) (lifecycle and event lifetime), [MDN Service Worker lifecycle](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) (new installing/waiting Worker coexists with old active controller), [MDN Cache interface](https://developer.mozilla.org/en-US/docs/Web/API/Cache) (origin-shared Request/Response storage, application-owned update policy). These sources describe the mechanism; they do not certify any LogMate defect.

### Exact product-source review [SOURCE / CONDITIONAL CONTRADICTION]

Read-only `yhappcom/logmate@d3bc214fe9b4b7bf84702f898b4e6993a4127e2f`, `tool/pwa_precache.dart` blob `90a67954af618a4e18199fa92555491c56167c17`, generated Worker template lines 382–646:

- Lines 388–389 store a shared `logmate-offline-control-v2` JSON catalogue; lines 413–423 read and overwrite the whole object.
- Lines 425–441 explicitly acknowledge CacheStorage has no compare-and-swap and use `controlMutation`, a Promise queue **local to the current Worker global**. This protects concurrent handlers *within that global*; no inter-generation lock or transaction is visible in these source lines.
- Lines 545–560 allow the installing candidate to write the shared catalogue before activation; lines 602–643 allow the old active Worker to update client-build assignments on navigation. Thus overlapping mutation windows are **source-plausible**, but exact timing, subsequent repair and reachable impact on LogMate are not established.
- The design deliberately does **not** use `skipWaiting()` or automatic cache deletion, and verifies served asset bytes against manifest digests. Those are genuine safeguards; they do not themselves make the shared JSON update atomic across Worker generations.
- A lost `candidateBuildId` or `clientBuilds` entry would be a **control metadata** problem, not proof of Flight/IndexedDB data loss. The generated Worker returns a 503 repair/reload response when no valid build mapping exists; do not relabel that as a destructive data incident.

### Independent actual-browser diagnostic [VALIDATION — SYNTHETIC, CI EXECUTION SEPARATE]

A disposable [Chrome research fixture](handoffs/pwa_cross_generation_cache_control_probe.py) and [SHA-pinned CI workflow](../.github/workflows/stage8_pwa_cross_generation_cache_control.yml) model the **same architectural pattern**, not the proprietary/product Worker source. The test deliberately holds a v1 event after reading a shared CacheStorage JSON snapshot, installs a v2 Worker which writes a new candidate to that JSON key while v1 still controls the page, then releases v1 to write its stale snapshot. Independent page-context CacheStorage reads check both intermediate and final states.

| Case | Independent assertion | Limit |
| --- | --- | --- |
| CG01 | Sequential read/modify/write retains both fields | Control only; not concurrency |
| CG02 | v2 waiting Worker can write shared metadata while v1 controls a tab | Synthetic Worker; not LogMate |
| CG03 | Delayed v1 write can erase v2 candidate from shared JSON | Demonstrates mechanism, not product exploit |
| CG04 | Distinct immutable per-version keys survive this particular overwrite | Does **not** prove atomic current-version pointer |
| CG05 | v2 remains waiting; no forced activation is needed | Not a Safari/iPadOS result |

**Failure-first evidence:** [initial hosted run 40636043414](https://github.com/yhappcom/web-manager/actions/runs/40636043414) reached Chrome but failed because the test installed its page message listener *before* a navigation and then tried to read the vanished `window.events` array. This is a **test-oracle lifecycle defect**, not a Worker/CacheStorage counterexample. The corrected fixture rebinds its listener after reload; [follow-up run 40636099341](https://github.com/yhappcom/web-manager/actions/runs/40636099341) must be checked for its own exact-ref result before promoting any CG01–CG05 PASS claim. The local execution container blocked loopback Chrome navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`), so no local-browser PASS is claimed.

### Product-grade acceptance and possible remediation [MINTTAP DIRECTION / DEPENDENCY / OPEN]

**Engineering implementation owner; Web Manager only supplies the web-specific failure model.** On an authorized exact LogMate NORMAL artifact, instrument Worker vN/vN+1 with two barrier points around `readControl` and `writeControl`; keep one vN-controlled client alive, install vN+1 and independently read the shared catalogue before and after releasing vN. Repeat with vN+1 install failure, browser restart, offline re-entry and Safari Home Screen (separately from a managed Web Clip). Assert *both* old client→build mapping and candidate/current/previous version identities, actual SHA-verified shell bytes, 503 repair states, untouched IndexedDB and recoverable LBK. No global cache clear or hidden data reset is an acceptable test repair.

Potential architecture choices, **not approved product changes**: (1) immutable version-specific manifest/control records plus a separately protected pointer; (2) IndexedDB `readwrite` transaction for shared mutable control state with exact Safari/Chrome tests; (3) a single authoritative activation-phase writer with carefully defined waiting-worker staging and recovery. Each needs failure-injection for crash, quota, old clients and schema compatibility; merely moving the same JSON to a different cache name is not a transaction.

**Five-track handoff:** **E** owns cross-generation release integrity, atomic control authority and non-destructive rollback/recovery; **A** owns Worker lifecycle, storage semantics and Chrome↔WebKit differences; **C** owns exact browser race barriers, independent state/asset oracles and negative controls; **B** consumes Design Studio W121 for accessible 503/reload/restore without claiming data loss; **D** consumes Marketing D8 claim HOLD and must not count an installed icon or Worker activation as offline-safe readiness. Engineering owns code changes and exact 37-store restore; no peer repository is modified.

**Gate remains:** Stage 8 ACTIVE · LogMate NORMAL product race **OPEN** · Safari Home Screen/managed EFB **OPEN** · Production validation OPEN · PWA release HOLD. The synthetic Chrome result, even if green, cannot advance product release.


### Exact hosted result, 2026-10-28 14:07 KST [VALIDATION — EXECUTED SYNTHETIC CHROME]

[GitHub Actions run 40636099341](https://github.com/yhappcom/web-manager/actions/runs/40636099341), job **122643306893**, checked out **168d1c36e1d0e3f9f25792309b5185028271681a**, completed **SUCCESS**. Ubuntu 24.04, Python 3.13.16, Playwright 1.57.0, Google Chrome **155.0.8059.39**; Python compile PASS, **CG01–CG05 5/5 PASS** in actual headless Chrome. Exact [JSON evidence artifact 12793726973](https://github.com/yhappcom/web-manager/actions/runs/40636099341/artifacts/12793726973) preserved. The independent page-context oracle observed `during={oldAssignments:[],candidate:"v2"}` followed by `after={oldAssignments:["old-tab"],candidate:null}`, while the v2 Worker was **waiting**, not forcibly activated. This demonstrates a real Chrome cross-generation shared CacheStorage **lost-update mechanism in the synthetic fixture**. It does **not** show that LogMate's actual Worker has hit the race, that its data is lost, or that the Safari/managed EFB behavior is identical.

The failed first CI [40636043414](https://github.com/yhappcom/web-manager/actions/runs/40636043414) remains in the evidence chain as a **page-global test harness error**, corrected by rebinding the message listener after reload. Do not retroactively label it a product defect or a passing run. The follow-up success is exact to the test commit above; this documentation commit itself does not rerun the browser.

**Operational priority:** The prior §13 next-target plan now has a more precise NORMAL release sub-gate: **two Worker generations must preserve both old-client assignments and candidate metadata under barrier-controlled overlapping updates**. This is higher information gain than another generic sequential Worker update test. It does not displace the higher-level 37-store backup/restore, verified Owner and physical managed-iPad blockers. **Stage 8 ACTIVE · synthetic Chrome CG 5/5 PASS · LogMate NORMAL cross-generation validation OPEN · Production validation OPEN · PWA release HOLD.**


## 15. 2026-10-28 — Cross-generation control-state remediation boundary: IndexedDB isolation is conditional, not an offline-release proof [SOURCE / SYNTHESIS / TRANSFER VALIDATION / OPEN]

### 15.1 Problem and precise dependency
§14's exact [Chrome CG01–CG05](https://github.com/yhappcom/web-manager/actions/runs/40636099341) demonstrates that *one shared CacheStorage JSON catalogue* can lose a v2 waiting-Worker candidate when v1's delayed read/modify/write overwrites the key. A per-Worker `controlMutation` Promise does not coordinate distinct Worker globals. The next question is **which alternative provides an actual cross-context transaction boundary without accidentally claiming that it also makes CacheStorage asset installation, client control or user data durable**.

**Primary standards checked 2026-10-28:** [W3C IndexedDB 3.0](https://w3c.github.io/IndexedDB/) says overlapping-scope `readwrite` transactions cannot execute concurrently and later transactions observe earlier committed changes; [MDN IDBTransaction](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction) documents the active-task/request-callback lifetime, abort, complete and Worker availability. [Service Workers specification](https://w3c.github.io/ServiceWorker/) defines install/waitUntil, waiting/active overlap and event-lifetime limits. [MDN Cache](https://developer.mozilla.org/en-US/docs/Web/API/Cache) exposes match/put/delete, **not** a cross-key compare-and-swap or IndexedDB-coupled transaction. These standards establish **conditional primitives**, not a LogMate implementation decision or WebKit runtime result.

### 15.2 Candidate architectures and falsification [SYNTHESIS / MINTTAP DIRECTION, NOT APPROVED PRODUCT POLICY]

| Candidate | What it can protect | What it does not protect / failure condition | Required oracle |
| --- | --- | --- | --- |
| A. Keep shared CacheStorage JSON plus Worker-global Promise | Sequential mutations *within one live Worker global* | Old active and new installing Worker; worker termination; stale read/overwrite; other same-origin contexts | Reproduce §14 barrier with actual NORMAL source and independently inspect all catalogue fields |
| B. Immutable per-build records in CacheStorage, separately promoted pointer | Version-specific manifest identity against overwrite of *another* key | Atomicity of shared pointer; missing/corrupt cache bytes; deletion/eviction; old-client assignment; rollback authority | Two generations, pointer collision, absent asset, interrupted install, old-client navigation and 503 repair |
| C. IndexedDB single `readwrite` transaction scoped to shared control store | A **read and conditional write both performed inside the same overlapping-scope transaction** across contexts | Reading outside transaction then blindly writing; asynchronous network/CacheStorage operations inside IDB transaction; IDB↔CacheStorage atomicity; quota/eviction; schema migration | Two independent contexts, stale-pre-read negative control, explicit abort, CacheStorage missing-asset negative control; then real vN/vN+1 |
| D. Activation-only authoritative writer plus immutable waiting-candidate staging | May reduce concurrent writes to one phase if *all* mutation routes respect the protocol | Old Worker navigation assignment and new Worker install still overlap unless segregated; activation crash; stale or incomplete candidate; no automatic client migration proof | Enumerate every write path; barrier old navigation vs new install/activation; power/quota and rollback failures |

**Operational judgment:** C is a promising *conditional* serialization mechanism, not an approved patch. A correct IDB implementation must open one `readwrite` transaction, issue `get`, compute the mutation and issue `put` **within the transaction's active request callback**, then treat `oncomplete` as the commit oracle. Moving only `put` into a transaction while retaining a pretransaction `get` reproduces lost update. Do not `await fetch()`, CacheStorage `put`, hash verification or other unrelated tasks in an open IDB transaction: the transaction may become inactive, and even a successful IDB commit cannot atomically commit the separate CacheStorage asset bytes. Use staged immutable assets, verify exact bytes, then publish a guarded pointer; on failure retain the old runnable generation and surface a non-destructive repair state. This is a design candidate requiring product Engineering approval and runtime tests.

### 15.3 Research-only actual-browser probe [VALIDATION — EXECUTION STATUS MUST BE CHECKED]

Added [two-tab Chrome fixture](handoffs/pwa_idb_control_transaction_probe.py) and [pinned hosted workflow](../.github/workflows/stage8_pwa_idb_control_transaction.yml). It does **not** run LogMate Worker code. The test uses two same-origin *Window* globals, not two Worker generations; this isolates the IndexedDB/CacheStorage primitives before the more expensive actual Worker-generation transfer.

| Case | Independent expected observation | Inference limit |
| --- | --- | --- |
| ID01 | Two tabs read the same origin-scoped IDB control record | Not EFB Home Screen storage partition equivalence |
| ID02 | Two `readwrite` read+modify+put transactions preserve old assignment **and** candidate | Attempts may serialize; not a forced simultaneous transaction interleaving or product Worker proof |
| ID03 | **UNSAFE negative control:** two stale reads *outside* transactions followed by whole-object `put` lose the earlier assignment | Passing means unsafe baseline reproduced, not security certification |
| ID04 | Explicit abort of a transaction leaves prior committed record unchanged | Not browser/process power-loss durability |
| ID05 | IDB pointer can reference a candidate with **no** corresponding CacheStorage asset | Demonstrates missing cross-API atomicity, not a defect in LogMate's existing SHA verifier |
| ID06 | After a separate CacheStorage `put`, another tab can independently read the staged bytes | Ordering illustration only; not manifest hash, promotion or rollback proof |

**First-failure record:** [CI 40641524052](https://github.com/yhappcom/web-manager/actions/runs/40641524052) reached real Chrome and completed ID01–ID03, then failed at ID04 because the fixture's `tx.onerror` rejected the Playwright promise with `null` during an intentionally explicit abort, before the `onabort` oracle could resolve. This is a **test harness error**, not evidence of IDB rollback failure or a LogMate defect. [Correction 7e8fa4e](https://github.com/yhappcom/web-manager/commit/7e8fa4e960bec52fa1e638d72368837e563a2c12) distinguishes the deliberate abort from unexpected transaction errors. **Do not claim ID01–ID06 PASS at the corrected ref without its completed hosted logs.** Local container Chrome navigation was blocked by administrator, so local browser PASS is unavailable.

### 15.4 Exact LogMate source transfer [SOURCE / DEPENDENCY]
Read-only `yhappcom/logmate@d3bc214f`, `tool/pwa_precache.dart` blob `90a67954`, generated Worker template. The real code uses a shared CacheStorage JSON (`CONTROL_CACHE`/`CONTROL_KEY`), `readControl`→`writeControl`, Worker-local `controlMutation`, and writes in **install**, **activate**, **message** and **fetch navigation** paths. In `activate`, `updateControl(async control => promoteInControl(...))` may await `inspect` while holding only the *global-local* queue. No cross-generation lock/transaction is visible in those source lines. The code also has significant safeguards: per-build SHA-verified responses, no `skipWaiting`, no automatic old-cache deletion, and 503 repair rather than serving an unverified newer shell. This is **source-derived plausibility**, not an observed production race.

**Proposed exact NORMAL acceptance matrix (Engineering-owned):** (1) old client vN still controlled while vN+1 waiting installs; (2) barrier around *actual* `readControl`/`writeControl` in both generations; (3) independently assert old `clientBuilds` plus current/previous/candidate/versions, exact manifest hashes and old-client asset bytes; (4) restart/aborted install, 503/reload/repair, IDB data untouched; (5) quota and storage eviction, cold offline re-entry and user-exported LBK; (6) Safari 26 Home Screen and managed Web Clip separately on approved physical iPad; (7) no silent `skipWaiting`, no cache clearing, no forced automatic Sync or UTC LWW policy changes. A successful two-tab *Window* fixture is only a prerequisite to this product/Worker test.

### 15.5 Five-track allocation, peer evidence and gate [TRANSFER VALIDATION / OPEN]
- **E — owner, highest bottleneck:** cross-generation release authority, transaction/asset publication boundaries, secure recovery, storage custody, deploy/rollback. Reuse this analysis as the single control-state owner.
- **A — dependency:** standards and Chromium-vs-WebKit Worker/IDB lifecycle. A same-origin two-tab result does not establish installed Safari Home Screen or MDM Web Clip storage partition or event lifetime.
- **C — independent validation:** keep failing CI provenance, explicit unsafe negative control, exact SHA/environment, byte-level asset/IDB oracles, real Worker barrier and physical-device tests. No score or synthetic PASS is product PASS.
- **B — consumer:** Design Studio [W121 Stage 3 PRACTICE](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) informs accessible offline/update/503/backup recovery flows; it is not runtime certification. Distinguish control metadata repair from Flight loss.
- **D — consumer:** Marketing [D8 HOLD](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) prevents public claims of installed/offline-safe/automatic Sync or EFB approval. Analytics must not equate Worker activation, IDB pointer, cached bytes, local saved data, backup and server-applied cursor.

**Software Engineering owns** implementation, 37-store LBK/Apply+Cursor and real artifact tests; Web Manager supplies web failure model and acceptance conditions. **LogMate approved Manual Delta Sync contract remains unchanged**; no automatic background sync inference. **Gate:** Stage 8 ACTIVE; previous synthetic Chrome CG01–CG05 5/5 PASS; new IDB fixture corrected-run result pending; actual LogMate NORMAL, authenticated Owner, 37-store restore, Safari Home Screen, managed EFB and production validation **OPEN**; PWA release **HOLD**.


### 15.6 Exact hosted execution: two-tab primitive + two actual Worker generations [VALIDATION — EXECUTED SYNTHETIC CHROME]

**Successful exact run:** [GitHub Actions 40641718043](https://github.com/yhappcom/web-manager/actions/runs/40641718043), job `122661145717`, tested checkout `541f082cf38861fd0a2d3303ed815e8c2e6dbac2`, completed **SUCCESS** 2026-10-28 06:05 UTC (15:05 KST). Ubuntu 24.04, Python 3.13.16, Playwright 1.57.0, Google Chrome **155.0.8059.39**. Python compile and both actual-browser scripts passed: **ID01–ID06 6/6** (two independent Window globals) and **WG01–WG05 5/5** (one v1 *active* Service Worker and one v2 *installed/waiting* Service Worker). [Artifact 12795234275](https://github.com/yhappcom/web-manager/actions/runs/40641718043/artifacts/12795234275) contains both bounded JSON outputs. The workflow is pinned and read-only, with no LogMate or Firebase secrets.

**Independent observations:** ID02 retained `oldAssignments=['old-tab']` and `candidate='v2'` with each read+put inside a single `readwrite` transaction. ID03 **intentionally** performed stale reads before separate transactions and lost the old assignment. ID04 explicit abort left the previous committed state. ID05 deliberately published `candidate='v4'` in IDB without any `/asset-v4` CacheStorage entry; ID06 independently read the staged asset after it was written. WG01–WG05 directly crossed the Worker-generation boundary: v1 controlled an open page and waited at a message barrier; v2 installed, wrote `candidate='v2'` through IDB and remained waiting; releasing v1 caused its later IDB transaction to read the current state and retain **both** `oldAssignments=['old-tab']` and `candidate='v2'`. This is a real browser contrast with §14's **synthetic CacheStorage lost update**, not a LogMate product result.

**First failure preserved:** [run 40641524052](https://github.com/yhappcom/web-manager/actions/runs/40641524052) failed because the explicit-abort test harness rejected `null` from `tx.onerror` before `tx.onabort`; [corrected run 40641592719](https://github.com/yhappcom/web-manager/actions/runs/40641592719) independently passed ID01–ID06 6/6. Final run 40641718043 repeated ID01–ID06 and added the **actual two-generation Worker** WG01–WG05, all passing. Neither failed test nor correction is a LogMate incident.

**Crucial limit:** WG04 tests *a particular ordering* (v2 transaction completes before v1 transaction starts), not a forced simultaneous IDB transaction conflict. The standards provide overlapping-scope serialization; further barrier/stress, Safari/WebKit and actual NORMAL Worker transfer are still needed. No cache-asset hash, install interruption, browser crash, storage eviction, migration, real LBK, Owner or server Sync is tested here. `readwrite` isolation does **not** make CacheStorage writes and IDB pointer publication one atomic transaction. This supports a **candidate engineering direction**, not a product change authorization.

**Decision/gate:** E's web release-control alternative now has a bounded **actual cross-generation Chrome transfer PASS**, beyond two-tab simulation. A/C own Safari/WebKit and actual NORMAL reproduction; B's repair/reload/backup UX and D's claim HOLD remain unchanged. Software Engineering owns real code and exact 37-store recovery. **Stage 8 ACTIVE · Chrome synthetic CacheStorage lost-update CG 5/5 PASS · Chrome synthetic IDB two-tab ID 6/6 PASS · Chrome synthetic actual two-generation Worker WG 5/5 PASS · LogMate NORMAL / Safari Home Screen / managed EFB / production validation OPEN · PWA release HOLD.**
