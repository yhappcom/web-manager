# 513 — Stage 8 PWA first-claim, offline navigation and Chromium process-reopen evidence boundary

Date: 2026-10-24 KST  
Status: **SOURCE + SYNTHESIS + executable diagnostic handoff / synthetic verdict tests PASS / Chromium navigation BLOCKED by environment / PRODUCT VALIDATION OPEN / PWA RELEASE HOLD**  
Owner: **Track E (trust and release adjudication)**; prerequisite supplier **A**; independent runtime oracle **C**; consumers **B/D**.

## 1. Canonical refresh and why this is the next bottleneck [SOURCE / DEPENDENCY]

Run-start `yhappcom/web-manager main@25ba36b7d295d81d2d13dc4c5e608064958e92d0`: read `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, relevant 508, 511, 512, latest commits and the non-deploying G1→G2 workflow proposal. Generic curriculum Stages 1–12 have historical competency PASS; **applied Stage 8 Security/Privacy/Trust remains active**. Latest LogMate `main@27f926aa6ea1e032dfa9affc598e8e41131eb092` was read-only; reviewed `tool/pwa_precache.dart`, `web/flutter_bootstrap.js`, `firebase.json`. Read Design Studio `progress/WEB_STATUS.md` (W121 runtime/AT/human gate OPEN), `progress/CONTENT_STATUS.md` (CD127 exact-runtime state semantics OPEN), Design Synthesis Gate, Software Engineering `research/README.md` (M006 bounded Safari/Chromium and Q006 exit-verdict transfer) and Marketing `STATUS.md` (LogMate EFB/offline/Sync promotional claims HOLD). All peer/product repositories read-only.

Five-track allocation: E remains highest-risk because offline readiness can be misrepresented as release/backup authority; A is the immediate blocking platform prerequisite (first claimed document, fetch event client ID, controlled navigation, persistent profile); C is the high-value executable evidence supplier. B consumes truthful readiness/error language; D consumes privacy-limited status and may not treat a local test as acquisition/install proof. This allocation intentionally does not repeat E's 509–512 archive primers or Design Studio's UI expertise.

## 2. Platform first principles → standard → observed implementation [SOURCE / SYNTHESIS]

**Historical problem.** AppCache mixed document cache policy and lifecycle and was replaced by service-worker-controlled fetch/CacheStorage approaches; these enable programmable offline behavior but create independent registration, worker, cache, document and persistent-data lifetimes. A downloaded shell is not necessarily the shell assigned to a currently running document.

**Standard mechanics.** A first page commonly loads from network before service-worker registration. A worker can then install, activate and call `clients.claim()`, which controls already-open in-scope pages without retroactively processing their original navigation. `FetchEvent.clientId` names the initiating client; `resultingClientId` names a reserved resulting document for navigations. The standard does not promise an application's custom `clientBuilds` mapping. The mapping is LogMate application state, not browser authority.

**Exact LogMate source path.** The bootstrap registers `logmate_service_worker.js` and does not block Flutter first paint. The generated Worker verifies shell/font/notice candidates and writes `currentBuildId` into `logmate-offline-control-v2`, calls `self.clients.claim()` in activation, and binds `clientBuilds[event.clientId/resultingClientId]` only for intercepted root navigations. Later non-navigation shell/font requests read `control.clientBuilds[event.clientId]`; an unassigned ID returns explicit HTTP **503** with a reload-required message. A network-loaded page claimed *after* its navigation can therefore be controlled yet unmapped. This is a source-compatible conditional failure; it does **not** prove any real page experienced the failure. Root reload is a positive control because it can bind the new document. Blindly defaulting unassigned clients to the latest candidate is unsafe: it could mix old-document and new-build bytes.

**Different predicates:** (i) candidate cache byte verification, (ii) catalogue/Worker generation coherence, (iii) particular client→build routing, (iv) cold offline navigation, (v) browser-process-reopen durability, (vi) application ledger/37-store restore, and (vii) independently approved/hosted release are distinct. `READY`, `navigator.serviceWorker.controller`, HTTP 200 and process reopen alone cannot be promoted across these boundaries.

Primary sources reviewed 2026-10-24:
- W3C Service Workers, FetchEvent clientId/resultingClientId and claim: https://w3c.github.io/ServiceWorker/
- MDN Clients.claim: https://developer.mozilla.org/en-US/docs/Web/API/Clients/claim
- Chrome lifecycle explanation: https://web.dev/articles/service-worker-lifecycle
- Playwright Python Service Workers: https://playwright.dev/python/docs/service-workers (service-worker inspection/routing supported in Chromium; not Safari parity).
- Apple/WebKit-specific install/storage behavior remains governed by research 507 and physical managed-device evidence, not by this Chromium probe.

## 3. New executable handoff [VALIDATION / DEPENDENCY]

`research/handoffs/pwa_worker_claim_browser_probe.py` is a **read-only, local, Chromium-only diagnostic**, not a LogMate code patch or deploy workflow. It requires an already-built, separately verified NORMAL directory, operator-asserted exact source SHA and a local Chromium. It serves the directory at an ephemeral `127.0.0.1` origin, uses a disposable persistent Chromium profile, records Worker SHA separately from shell appBuildId, and produces sanitized JSON outside the artifact root. It exercises:

| Case | Controlled transition | Expected bounded evidence |
| --- | --- | --- |
| P01 | first network navigation, worker registration and claim | controller acquired; no claim that initial navigation was intercepted |
| P02 | fetch `main.dart.js` from **same first claimed page** | exact status; 503 is a regression candidate, not inferred ledger loss |
| P03 | controlled root reload and same asset fetch | mapping should allow exact cached version, status 200 |
| P04 | network disabled, same-process root reload and asset fetch | cold navigation and asset should remain available |
| P05 | close Chromium, reopen **same persistent profile** with network disabled, root navigation and asset fetch | process-reopen durability bounded to this local browser/profile |
| P06 | missing evidence or environmental browser block | nonzero and `INCOMPLETE_OR_ERROR` / `EXECUTION_ENVIRONMENT_BLOCKED`, never PASS |
| P07 | asset 503 but other steps succeed | `FIRST_CLAIM_ASSET_FAILURE_OBSERVED`, nonzero |
| P08 | reload/offline/reopen failure | `RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED`, nonzero |
| P09 | all observed statuses 200 | `BOUNDED_CHROMIUM_PATH_PASS` only, not G5 product/release PASS |

Use only a test/disposable profile: no real flight records, credentials, personal data or telemetry. The tool records status, content type, source-SHA assertion and Worker digest, **not response bodies**. A local `http://127.0.0.1` trustworthy-origin exception is **not** an HTTPS Hosting test; test artifacts and browser profile are intentionally isolated. The exact artifact must first pass 509/512 independently and the real served origin later pass 510. No Chrome-specific result transfers to Safari, Home Screen, MDM Web Clip or a company EFB iPad.

Example after Engineering produces a frozen NORMAL artifact (not run against LogMate here):

```sh
python3 research/handoffs/pwa_worker_claim_browser_probe.py \
  --root /path/to/verified/build/web-normal \
  --source-sha <exact-40-hex-LogMate-commit> \
  --chromium /path/to/chromium \
  --out /tmp/logmate-first-claim-evidence.json
```

`--source-sha` is an operator assertion, **not an attestation**. A green probe does not establish artifact provenance, user-data durability, actual Firebase Hosting, accessibility, installability, iPadOS policy or native-mobile Sync.

## 4. Actual execution, bounded failure and oracle reliability [VALIDATION / CONTRADICTION]

**Executed 2026-10-24:** Python 3.13.5 syntax compilation passed; **11/11 deterministic classification-oracle unit tests PASS**. The tests distinguish initial 503/404, controlled reload 503, offline failure, process-reopen failure, missing observation, malformed status and complete 200-only bounded PASS. A disposable HTML/JS/Service Worker fixture was constructed to exercise the browser path without claiming product parity.

**Browser attempt:** local Chromium **144.0.7559.96** launched under Playwright, but the first loopback navigation returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Retried with explicit no-proxy/bypass arguments; the environment still blocked navigation. The evidence verdict is **EXECUTION_ENVIRONMENT_BLOCKED**, not a first-claim failure, not a Chrome runtime PASS and not a product regression. The fixture reproduces only the relevant client-mapping algorithm, not the full LogMate generated Worker. No real NORMAL artifact was available locally. This is a genuine environment/evidence blocker for runtime, not a reason to manufacture a PASS.

**Known limits of the handoff:** The probe currently observes statuses rather than proving each response's cryptographic cache identity, does not capture exact network-versus-Worker response provenance for every subrequest, cannot force every Worker activation interleaving, and does not test second-generation lost-update or corrupt-catalogue cases. It assumes the supplied NORMAL build registers the worker and that root navigation is its supported route. It does not validate an already populated profile with unique ledger data or verify persistence after browser storage eviction. The test helper imports Playwright and requires Engineering to pin versions and re-run its own CI/runner semantics (Q006).

## 5. Cross-track transfers and adversarial judgment [TRANSFER VALIDATION / CONTRADICTION]

- **A — platform supplier:** `clients.claim()` changes controller status, not historical navigation provenance; fetch-event client identity is distinct from application mapping; browser process restart is distinct from tab reload. Service-worker routing is not a cross-generation atomic catalogue.
- **C — quality oracle:** separate incomplete/block/failure/partial success; preserve exact source/build/Worker/browser identity; run P01–P09 on real NORMAL, repeat to characterize timing and add network/service-worker provenance. A browser automation timeout or policy block must never count as product failure or PASS.
- **E — security/operations owner:** do not repair a 503 by clearing origin storage or deleting user data; maintain release HOLD until independently approved G0–G4 and real G5 runtime/data evidence. No unverified cache fallback to a newer shell for an older document.
- **B — UX/IA consumer:** distinguish 'page needs reload' from 'flight data lost'; distinguish shell READY from 'offline safe'; any user-directed reload/reinstall must preserve local edits/outbox and present recoverable state. Design Studio W121/CD127 exact-runtime/AT/human gate remains OPEN.
- **D — discovery/analytics consumer:** aggregate only sanitized failure classes, Worker generation and test cohort, not flight records; avoid claims of 'offline available on company iPad' or seamless unattended sync. Marketing D8/D10 remain HOLD.

**Counterexamples:** worker `activated` while first claimed client unassigned; candidate `READY` while fetch 503; controlled reload works while cold process reopen fails; Chromium local PASS while Safari MDM Web Clip cannot persist storage; archive/host bytes match while Worker/client map fails; worker repair succeeds while local 37-store restore fails. Each breaks a tempting transitive success inference.

## 6. Decision, next execution and stop condition [MINTTAP DECISION CANDIDATE / OPEN / CHANGE WATCH]

**Proposed acceptance rule (not approved product policy):** classify every first-install run separately from update and long-offline rejoin; preserve local data; require bounded positive and negative evidence at every source→archive→host→runtime→ledger boundary. Treat any missing/blocked evidence as UNKNOWN and keep release HOLD.

**OPEN:** real NORMAL build and independent receipt, usable Chromium test runner with loopback permission, repeated P01–P05 product observations, two-Worker shared-catalogue W01–W28 interleavings, exact 37-store semantic restore and R03/R04, browser storage-pressure/eviction, real hosted origin, physical Safari/iPadOS/Home Screen/MDM Web Clip, and native-mobile Sync. **CHANGE WATCH:** W3C Service Worker lifecycle, Chrome/Playwright service-worker diagnostics, WebKit client/installation/storage policy, Flutter bootstrap and generated Worker SHA, LogMate main and release workflow action versions.

**Adjacent-value check:** after the 511/512 CI proposal, the highest-value different dependency was an executable browser first-claim/process-reopen diagnostic; completed with fail-closed verdict tests and an attempted physical Chromium run. Further proof requires a permissive browser runner and exact product NORMAL build, a materially different environment boundary. No production validation gate changed. **Applied Stage 8 ACTIVE / Track E bottleneck / Production validation OPEN / PWA release HOLD.**
