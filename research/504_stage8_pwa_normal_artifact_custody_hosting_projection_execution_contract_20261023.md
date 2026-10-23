# 504 — Stage 8 NORMAL PWA Custody, Hosting Projection and Browser Execution Contract

**Date:** 2026-10-23 KST. **Owner:** E (release security and operations), A/C mandatory dependencies; B/D transfer. **Canonical starting point:** Web Manager `main@6bc353550f13934da67d6e597fb271dbf0dbdf4f`, study 503. **Read-only product:** LogMate `main@59cd171176c58b598a4db55d128ffd21d406e862`. **Verdict:** SOURCE + operational SYNTHESIS + implementation-ready *proposal*, NOT an executed patch, deployed artifact, or product PASS. Stage 8 / Production validation OPEN / PWA release HOLD.

## Why this checkpoint is distinct from 503

Study 503 established G0–G8 gates. This study resolves the adjacent *implementation handoff*: which build is retained, which bytes are eligible for Hosting, how an independent consumer can detect a missing/extra file, how to avoid a false PASS from GitHub's warning-only artifact digest, how to resume existing browser tests, and which counterexamples falsify each handoff. It deliberately does not create another synthetic reference model or re-label earlier host tests as iPad validation.

### 1. History / problem / standard / operational principle [SOURCE + SYNTHESIS]

AppCache-era opaque update and current Service Worker update semantics make “build succeeded” an insufficient release identity. Service Worker registration is scope-bound, secure-context-bound and update-sensitive. `updateViaCache: 'none'` controls HTTP-cache consultation for Worker script/import updates, **not** the Cache API, IndexedDB durability, content release authority or physical-device storage. `registration.update()` attempts a Worker update; it is not proof of a verified offline candidate, active controller or safe ledger migration.

GitHub Actions artifact `upload-artifact` produces an artifact SHA-256 digest; the official `download-artifact` digest mismatch is reported as a **warning**, not a fail-closed release oracle. Upload v4 excludes hidden paths by default. Firebase Hosting deploys the `hosting.public` tree subject to `hosting.ignore`, and response precedence is reserved `/__`, redirects, exact static, rewrites, then 404. These are *three different projections*: build tree, uploaded archive members and Hosting-served files. Equality cannot be assumed merely because all three operations succeed.

**Sources checked 2026-10-23:** GitHub https://docs.github.com/en/actions/tutorials/store-and-share-data ; upload action https://github.com/actions/upload-artifact ; Firebase https://firebase.google.com/docs/hosting/full-config ; W3C https://www.w3.org/TR/service-workers/ ; MDN https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register and https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/updateViaCache ; WebKit https://webkit.org/blog/14403/updates-to-storage-policy/ . GitHub action versions, Apple policy and browser capability are CHANGE WATCH.

### 2. Current pinned LogMate evidence [SOURCE]

- `Makefile`: `BUILD_WEB_OUTPUT ?= build/web`; NORMAL = `flutter build web --output ... --pwa-strategy=none --no-web-resources-cdn --no-wasm-dry-run` followed by `tool/precache_flutter_web.dart` and `tool/verify_pwa_artifact.dart`. Acceptance adds `--dart-define=LOGMATE_PERSISTENCE_ACCEPTANCE=true` and `--require-acceptance-harness`.
- `.github/workflows/data001-pwa-artifact-validation.yml`: Flutter 3.47.5; NORMAL built into `build/web-normal`, then Acceptance into `build/web`. Only Acceptance `build/web` is uploaded; workflow has manual dispatch but no `main` push trigger. `firebase.json` currently selects `build/web` and ignores `**/.*`; three `/auth` rewrites, no catch-all SPA rewrite.
- `.github/workflows/data001-browser-persistence-validation.yml`: Flutter 3.38.7, automatic push only on `feature/data001-domain`; project `pubspec.yaml` requires Dart `^3.12.0`. Current-main browser validation cannot be inferred from historical different-ref Chrome 1/1 PASS.
- `test/repository/logbook/sembast_web_reopen_test_browser.dart`: real browser fixture opens uniquely named Sembast Web DB; create/delete/restore and close/reopen assertions cover revisions, page, previous totals, pending operations. It does **not** assert B1 whole-ledger .lbk import/export, browser process restart, installed Safari context or physical managed iPad.
- `tool/verify_pwa_artifact.dart`: checks required files, sidecar record size/SHA-256, 724 fonts, 148 notices, bootstrap/Worker string markers and Acceptance flag isolation. It does not independently enforce file-set closure, decoded path confinement/symlink safety, duplicate record paths, full Worker-sidecar agreement or full Worker-byte identity. This is a source-level test-coverage gap, not proof of an exploitable defect.
- `web/flutter_bootstrap.js`: registers owned Worker with `updateViaCache:'none'`, starts guarded precache and promotion, does not block first paint. An app launch or controller event is not an offline-ready receipt.

**Exact source:** https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/Makefile ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/.github/workflows/data001-pwa-artifact-validation.yml ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/.github/workflows/data001-browser-persistence-validation.yml ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/firebase.json .

### 3. Recommended Engineering change sequence [MINTTAP DECISION — PROPOSAL, NOT APPROVED IMPLEMENTATION]

**Phase 0 — provenance and quality:** checkout a pinned source SHA, use Flutter 3.47.5 or an explicitly approved compatible toolchain, verify `pubspec.lock` unchanged and Stage C font archive checksum; record exact workflow revision, Dart/Flutter, runner OS, build flags and Core CI failures. Do not silently baseline-update four failing Golden tests or call Core green.

**Phase 1 — clean NORMAL construction:** build NORMAL in an isolated clean directory/workspace; verify normal harness *absent* with existing Dart verifier. Do not build Acceptance into the same directory or copy Acceptance output over NORMAL. Preserve an inventory of *all* regular files with normalized relative paths, byte lengths and SHA-256, including `logmate_service_worker.js`, `logmate-offline-manifest.json`, `index.html`, `main.dart.js`, font assets and license notices. Reject symlinks and path escape; do not accept duplicate normalized names or case-fold collisions where a target filesystem may fold case. Reject missing or unexpected files against an explicit release inventory policy. A cryptographic inventory alone does not prove the signer/runner's authority.

**Phase 2 — archive custody:** upload NORMAL under a distinct `logmate-pwa-normal-<sourceSHA>-<runID>` name with `if-no-files-found:error`; preserve upload artifact ID and digest and an independently generated content inventory. Explicitly audit hidden files: because upload-artifact v4 omits hidden files by default and Firebase `**/.*` ignores them, *fail* if a required deployed resource would be silently omitted; do not globally enable hidden-file upload without a secret-leak audit. In a fresh downstream job, download by exact artifact name/ID; independently re-enumerate members and compare sorted path/length/hash tuples to the signed/controlled pre-upload inventory. Exit nonzero on mismatch regardless of GitHub's built-in warning behavior. Require a trustworthy reference inventory delivered through the job dependency or a separately authenticated artifact, not an untrusted manifest bundled with the bytes it judges.

**Phase 3 — deployment projection:** compare the approved NORMAL inventory with the actual `firebase.json` deploy projection. `hosting.public=build/web` means an unmodified deployment from repository root would read Acceptance output after the current validation workflow, *not* `build/web-normal`. **This is a configuration hazard, not evidence a deployment occurred.** In a clean deploy job stage the verified NORMAL files into a dedicated directory and point an explicit validated Hosting config to that directory, or change the config under reviewed change control; never implicitly reuse `build/web`. Reject an unintended difference between approved archive files and Hosting-selected files, accounting explicitly for ignore rules. Keep production credentials and deploy permissions out of the build/test job; do not auto-deploy on the basis of this study.

**Phase 4 — serve and lifecycle:** test Hosting Emulator then an approved non-production preview for expected JS/WASM/WOFF2/Worker/manifest MIME, bytes, status and headers; unknown static path must return 404 rather than HTML-200. Test `/auth`, `/auth/action`, Firebase reserved `/__/*` independently. Verify Worker scope/control and actual offline resource reads after first install and upgrade with two open clients, interrupted precache, offline reload, rollback, and preservation of unsynced IndexedDB data. Do not promote a Worker update by `skipWaiting` without product-specific data safety review.

**Phase 5 — local data and owner:** run current-main Chrome test with a compatible Flutter/Dart SDK, then extend Engineering-owned browser tests to B1 .lbk full-ledger import/export and 30-store preservation after rejected restore, transaction callback retry/concurrency and reopen. Physical Safari tab, Home Screen, managed Web Clip and Shared iPad are separate test envelopes; record iPadOS, MDM, display mode, storage identity and independently accessible backup. Manual Sync requires current owner authority and independent remote ACK; local restore is not remote convergence.

### 4. Minimal reviewable CI change plan [DEPENDENCY — Engineering]

Prefer **two jobs**: (A) build-and-upload NORMAL with no deploy credentials; (B) independent download-and-verify with no product source rebuild, followed only later by an explicitly approved deployment stage. Keep Acceptance upload as a *separate development artifact*, with unambiguous name and no deployment eligibility. Align browser workflow SDK and trigger to approved current-main verification; avoid widening production deployment triggers accidentally. A workflow patch must be reviewed for the actual action version, permissions, artifact retention and release promotion authority. No patch is applied to LogMate by Web Manager.

### 5. Falsifiable counterexamples and oracles [VALIDATION]

| Case | Required observation | Verdict until run |
|---|---|---|
| NORMAL compiled without Acceptance marker | Existing Dart verifier succeeds; Acceptance-only marker absent | NOT_EXECUTED |
| Acceptance bytes mislabeled NORMAL | Independent build identity/harness check fails | NOT_EXECUTED |
| Hidden required file omitted by archive | inventory difference produces nonzero exit | NOT_EXECUTED |
| Extra or duplicate archive member | closure/uniqueness check fails | NOT_EXECUTED |
| Traversal, encoded traversal, symlink escape | Dart verifier rejects before reading outside root | NOT_EXECUTED |
| Worker byte changed while markers retained | complete-file digest check fails | NOT_EXECUTED |
| Sidecar manifest differs from embedded Worker data | semantic or byte-equivalence check fails | NOT_EXECUTED |
| GitHub digest mismatch only warns | independent release gate still fails | NOT_EXECUTED |
| Firebase public points to Acceptance directory | release promotion rejects wrong source tree | NOT_EXECUTED |
| Missing static JS route | HTTP 404, never HTML-200 fallback | NOT_EXECUTED |
| Worker update interrupted; old tab open | no false offline-ready; no lost unique local record | NOT_EXECUTED |
| Browser B1 restore rejected with preexisting data | all 30 registered stores unchanged; no side effects | NOT_EXECUTED |
| Safari tab vs installed app | storage identity measured, no assumed sharing | NOT_EXECUTED |
| Managed iPad backup lost/evicted | independent export + restore demonstrated or gate FAIL | NOT_EXECUTED |

**Execution packet schema:** `{sourceSHA, workflowSHA, jobRunId, artifactId, artifactDigest, contentInventoryDigest, releaseMode, FlutterVersion, DartVersion, hostingConfigDigest, testEnvironment, OS/browser/MDM, scenario, observedResult, evidenceLocation, verdict}`. Distinguish PASS / FAIL / NOT_EXECUTED / BLOCKED. Never promote UNKNOWN or source-only reasoning to runtime PASS. Do not collect real flight records or sensitive owner identifiers in public CI artifacts.

### 6. Five-track ownership and transfer

| Track | Gate/depth/dependency pressure | Single-owner contribution |
|---|---|---|
| **E** | Stage 8 highest consequence; source mature, actual release custody and restore OPEN | Own phase 0–3 trust boundary, rollback, data survival, release HOLD |
| **A** | Standards/source mature; platform differences and current-main browser execution OPEN | Own Worker/HTTP-cache/Cache API/IndexedDB scope, activation and storage context mechanics |
| **C** | Historical host/Chrome evidence but current Core 4 FAIL, browser/iPad execution OPEN | Own negative tests, exact-source runtime oracles, accessibility/performance evidence |
| **B** | Recovery task-state requirements mature; human/AT validation OPEN | Own local-save, backup verified, installed, offline-ready, active-ledger, remote-ACK labels; consume Design Studio W121 |
| **D** | Generic web discovery/analytics mature; install/acquisition field proof OPEN | Own privacy-minimized provenance and honest PWA capability/advertising claims; consume Marketing 438 |

**TRANSFER VALIDATION:** Design Studio W121 (https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md) also rejects further paper manifests before exact runtime; Engineering D006 (https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md) distinguishes delivery/apply/ACK and retries; Marketing 438 (https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md) conditionally recommends initial PWA ad exclusion. No design, software-engineering or marketing ownership is reassigned here.

### 7. Contradictions, risks, change watch and stop rule

**CONTRADICTION:** `uploaded artifact digest exists` ≠ `digest mismatch fails deployment`; `uploaded files` ≠ `build tree` ≠ `Hosting-selected tree`; `same manifest SHA` ≠ `authorized publisher`; `NORMAL built` ≠ `NORMAL uploaded`; `normal verifier passed` ≠ `Worker bytes match sidecar`; `Worker registered` ≠ `offline-ready`; `Chrome reopen PASS` ≠ `B1 whole-ledger/iPad PASS`.

**OPEN:** real CI patch/approval, NORMAL archive, independent downstream consumer, Hosting preview/served bytes, negative Dart tests, current-main browser B1, physical managed iPad, full recovery and Sync backend. **CHANGE WATCH:** GitHub artifact action versions/digest semantics/hidden file defaults, Flutter web output, Firebase Hosting ignore/rewrite semantics, WebKit quotas/installation/eviction, iPadOS and MDM.

**Decision:** retain Stage 8, Track E bottleneck, Production validation OPEN, PWA release HOLD. The next meaningful checkpoint is **actual Engineering execution and exact artifact evidence**. More standalone synthetic studies should not be generated unless a new concrete contradiction changes the execution contract.


---

## 2026-10-23 source contradiction addendum — cross-generation Worker catalogue writer isolation (Track E owner, Track A dependency)

**Evidence boundary:** inspected exact LogMate `main@59cd171176c58b598a4db55d128ffd21d406e862` `tool/pwa_precache.dart` generated-worker template (lines approximately 380–690), `web/flutter_bootstrap.js`, and `test/tool/pwa_precache_test.dart`. No deployed worker, physical device or two-generation browser interleaving was executed. This is a **source-level concurrency risk requiring a falsifying browser test**, not a proven user-data loss incident or security exploit. It is a concrete source contradiction worth adding to 504 rather than a new micro-study.

### SOURCE — shared storage, separate execution contexts

- Worker template sets `CONTROL_CACHE = 'logmate-offline-control-v2'` and `CONTROL_KEY = '/__logmate_offline_control_v2.json'`. `readControl()` reads one JSON response; `writeControl()` overwrites it via `cache.put`. `updateControl(change)` chains operations on a module-global `let controlMutation = Promise.resolve()` and performs **read → change → write**.
- Active worker `fetch` uses `updateControl` to write `clientBuilds[clientId]` on root navigation; installing/waiting successor worker `install` and `precacheCandidate` also use `updateControl` to write `versions`, `candidateBuildId`, `verified` and sometimes `currentBuildId`. `web/flutter_bootstrap.js` explicitly selects `registration.waiting || registration.active || controller` for `START_PRECACHE`, so a waiting worker can receive a message while the previous worker serves clients.
- Each ServiceWorkerGlobalScope has its **own** JavaScript module-global promise. It is not an origin-wide mutex. Both generations can access the same named Cache Storage; Cache API `put` is not an atomic multi-operation compare-and-swap transaction for the JSON catalogue. The source comment promising serialization of `every control catalogue mutation in this worker` is valid only within that worker context; it does not establish cross-generation serializability.
- The existing Dart test checks for string markers (`controlMutation`, `updateControl`, two client IDs) but has no actual old-active/new-installing/waiting execution or stale-write oracle.

**Primary/platform sources checked 2026-10-23:** W3C Service Workers specification https://www.w3.org/TR/service-workers/ (lifecycle, Cache/CacheStorage); web.dev https://web.dev/articles/service-worker-lifecycle (successor installation alongside active predecessor, waiting, update safety); MDN https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage (shared worker/window cache namespace) and https://developer.mozilla.org/en-US/docs/Web/API/Cache (application-controlled updates). Platform behavior on exact Safari/iPadOS is CHANGE WATCH; no claim of a browser bug is made.

### SYNTHESIS — minimal falsifiable lost-update interleaving

Let persisted catalogue `C0` contain current build `A` and an existing `clientBuilds` map. Two **distinct worker globals** have separate `controlMutation` queues. (1) Old active worker begins root navigation and reads `C0`. (2) New installing worker reads `C0` to remember candidate `B`. (3) Old worker writes `C0 + clientBuilds[newClient]=A`. (4) New worker writes `C0 + versions[B], candidateBuildId=B` from its stale snapshot. The client assignment disappears. Reverse write order can instead discard candidate metadata. No individual `cache.put` needs to be corrupt for the whole-object update to be lost. `fetch` later consults `clientBuilds[event.clientId]`; missing assignment can produce a 503 for an otherwise verified shell asset. This is a *possible schedule*, not an observed production trace.

**Second adjacent boundary:** the same `updateControl` overwrites the JSON even when a callback merely returns `false`; a rejected `PROMOTE_VERIFIED_CANDIDATE` does not inherently prevent a stale whole-object write. `appBuildId` is derived from shell records rather than full Worker bytes (501), so catalogue ownership and release identity are distinct requirements. Do not assume `no skipWaiting` prevents old-active/new-installing shared-cache writes; waiting protects control takeover, not all storage mutations.

### MINTTAP DECISION — Engineering contract, not an authorized LogMate patch

**Do not declare Worker update / offline-ready gate PASS based on 504 custody alone.** Add a cross-generation catalogue-integrity gate to the same Engineering execution packet. Prefer architecture review of **immutable candidate records plus a single active-owner promotion path**, or a dedicated IndexedDB transactional catalogue with an explicit generation/epoch and rejection of stale authority. Merely adding another in-memory promise, retrying `cache.put`, or relying on `skipWaiting` is not a sufficient fix. An IndexedDB design must separately consider transactions, storage eviction, schema migration, and existing LogMate ledger isolation; no backend or app-data change is proposed by this study.

### VALIDATION — real browser oracles (all NOT_EXECUTED)

1. **Old-active/new-installing:** pause the successor immediately after its `readControl`, perform old-worker root navigation, then release successor write. Catalogue must retain both candidate and client assignment; correct versioned shell fetch must not return 503.
2. **Reverse order:** pause active navigation write, allow successor catalogue write, then release active write; both records must survive. Capture exact Worker script digests and Cache Storage snapshot before/after.
3. **Waiting worker message:** with old tab open, send `START_PRECACHE` to `registration.waiting` while old tab navigates/reloads; no lost `currentBuildId`, `versions`, `clientBuilds`, and no premature activation.
4. **Rejected promotion and interrupted install:** exercise rejected `PROMOTE_VERIFIED_CANDIDATE`, install failure, retry and restart; previous verified shell must remain reachable, and catalogue must not lose newer entries.
5. **Safari/Home Screen/managed iPad:** repeat only after Chromium test harness establishes deterministic reproduction. Each is an independent environment; do not infer shared Safari/Home Screen storage or managed Web Clip behavior.

A PASS needs an **actual** pinned-source, pinned-browser two-generation run with recorded read/write interleaving and invariant checks, not merely the source comment, a mock single-global promise, or a green static generator test. For a FAIL, preserve a sanitized catalogue diff, worker versions, event/client IDs, and the exact 503 response without exporting flight/identity data.

### Five-track transfer / dependency / contradiction

- **E (owner):** shared catalogue authority, atomicity and update rollback; highest release consequence.
- **A:** Service Worker lifecycle, distinct globals, Cache Storage scope and cross-browser semantics; owns generic mechanics only.
- **C:** implement deterministic browser interleaving, test failure localization and offline asset oracles; Golden/Core CI debt remains independent.
- **B:** never display offline-ready or safely-updated solely from registration/candidate status; maintain recoverable/repair-required states and screen-reader accessible instructions; consume Design Studio W121.
- **D:** do not count an install/update event as durable offline readiness or publish offline capability claims without an actual read-after-update proof; consume Marketing 438 PWA-ad-exclusion boundary.

**CONTRADICTION:** `serialized within one worker` ≠ `serialized across old-active/new-installing/waiting workers`; `Cache.put succeeded` ≠ `read-modify-write was atomic`; `no skipWaiting` ≠ `no shared-state overlap`. **OPEN:** exact Chromium/Safari reproduction, severity/frequency, production use of this path, remediation, managed-device execution. **Gate:** Stage 8 / Track E bottleneck / production validation OPEN / PWA release HOLD; this is an added Engineering blocker, not a runtime defect verdict.

**VALIDATION ATTEMPT (2026-10-23):** Prepared a local Playwright/Chromium two-worker read–write interleaving probe and attempted to open its loopback test origin. The browser returned `net::ERR_BLOCKED_BY_ADMINISTRATOR` before any Service Worker registration or Cache Storage scenario ran. **Verdict: BLOCKED / NOT_EXECUTED**, not a reproduced browser failure. No attempt was made to bypass the environment restriction. Engineering must run this class of test in an approved browser environment.


---

## 2026-10-23 architecture decision addendum — V2→V3 Worker catalogue migration under an uncooperative predecessor

**Owner:** Track E; A provides browser primitives, C owns falsification, B/D consume transfer. **Source pins:** Web Manager \`main@abc7b75c16a4b1aa433f97b22528ec55bf0cde73\` before this addendum; read-only LogMate \`main@59cd171176c58b598a4db55d128ffd21d406e862\` (unchanged on recheck 2026-10-23). **Classification:** SOURCE + SYNTHESIS + MINTTAP DECISION (Engineering architecture *recommendation*) + OPEN; **no runtime PASS, product patch or release promotion**.

### A. The actual upgrade problem is not just choosing a mutex [SOURCE / CONTRADICTION]

The shipped V2 worker has a module-local \`controlMutation\` queue and a shared Cache Storage JSON document, \`logmate-offline-control-v2 /__logmate_offline_control_v2.json\`. Its \`install\`, \`precacheCandidate\`, \`activate\`, \`PROMOTE_VERIFIED_CANDIDATE\` and root-navigation \`fetch\` paths can all perform \`readControl → mutate → cache.put\`. The bootstrap intentionally sends \`START_PRECACHE\` to \`registration.waiting\` while an old active worker can still own tabs. The old V2 binary cannot be retroactively taught a new Web Lock name or an IndexedDB protocol.

**Consequential distinction:** a new V3 worker that simply wraps its own V2 Cache writes in \`navigator.locks.request()\` **does not serialize** with the still-active V2 worker, which never takes that lock. Likewise, moving only the successor's control writes to IndexedDB while continuing to read and write the legacy V2 JSON cannot establish cross-generation transaction isolation. A mixed-protocol migration is a distinct hazard from the final steady-state design.

The current \`status()\` computes candidate \`READY\` from shell/font/notice byte checks; it does not prove that \`currentBuildId\` and a requesting client's \`clientBuilds\` assignment still form a usable route. A candidate-ready status can therefore coexist with a missing client assignment and a later 503. The existing test \`test/tool/pwa_precache_test.dart\` asserts strings, not cross-global scheduling. The earlier Playwright loopback attempt failed before registration (\`ERR_BLOCKED_BY_ADMINISTRATOR\`): **BLOCKED / NOT_EXECUTED**. Do not describe the schedule as an observed bug.

**Platform SOURCE (checked 2026-10-23):** Service Workers registration has separate installing/waiting/active workers, and waiting is not a general storage mutex (https://w3c.github.io/ServiceWorker/ ; https://web.dev/articles/service-worker-lifecycle/). The Web Locks draft coordinates *cooperating* agents sharing a storage bucket, not actors that never request the lock (https://w3c.github.io/web-locks/). IndexedDB overlapping \`readwrite\` transaction scopes serialize, but its transaction does not atomically include Cache Storage (https://w3c.github.io/IndexedDB/). MDN documents worker IndexedDB and the event-loop-sensitive transaction lifetime (https://developer.mozilla.org/en-US/docs/Web/API/WorkerGlobalScope/indexedDB ; https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB).

### B. Compare viable repairs before implementation [SYNTHESIS / OPERATIONAL JUDGMENT]

| Design | What it can establish | Where it fails or remains conditional | Decision |
|---|---|---|---|
| More in-memory Promise queues | Serializes callbacks within one live Worker global | Old/new globals and worker restarts do not share the queue | **Reject as sole fix** |
| Web Lock around legacy Cache JSON RMW | Cross-agent exclusion **if every writer cooperates** and the same storage bucket is used | Already-deployed V2 does not take the lock; lock availability and Home Screen/managed context must be tested; no atomicity with unrelated Cache/IDB operations | **Optional later optimization, not V2 migration fix** |
| Separate immutable candidate/build records plus activation-owned control pointer | Installing successor can stage/verify without touching V2's mutable control document; old controller remains intact | Requires precise promotion/recovery protocol; mutable pointer still needs one writer or transaction; Cache eviction can invalidate staged bytes | **Required migration boundary** |
| Dedicated V3 IndexedDB control database, single overlapping \`readwrite\` scope for mutable pointers/assignments | Browser-provided cross-context serialization and atomic control-record changes among **V3 participants** | Cannot enlist V2; IDB schema upgrade may block; no transaction spans IDB and Cache API; storage eviction/abort remains possible | **Preferred steady-state control store, conditional on runtime tests** |
| Per-client/per-version Cache keys without a shared JSON document | Reduces overwrite collision and can make immutable data append-only | Multi-key promotion, stale assignments, garbage collection, crash recovery and ownership remain unsolved | **Useful subpattern, not complete protocol** |
| Server as sole release-authority oracle | Can authorize remote promotion/release policy while online | EFB must still work offline; server cannot serialize two offline browser Workers or prove local bytes survived eviction | **Remote policy boundary only** |

**MINTTAP DECISION — recommendation to Engineering, not an approved code change:** prefer **V3 staged immutable per-release assets + no legacy V2 control writes before successor activation + a dedicated V3 IndexedDB transactional control store after controlled handover**. Keep the existing verified-byte-on-every-response guard and old-version caches until positive compatibility/restore evidence. Avoid new \`skipWaiting\` or opportunistic cache deletion. A Web Lock can supplement cooperating future clients but must not be the migration's correctness foundation.

### C. Migration phases and invariants [DEPENDENCY / MINTTAP DECISION]

**M0 — pin provenance and define release identity.** Record source SHA, full Worker script digest, sidecar manifest digest, release inventory digest, database capability/schema and font set. The existing \`appBuildId\` hashes shell records, not the entire Worker/release; it is not a sufficient unique key for a Worker-protocol migration. Require explicit compatibility between old stored manifest and new V3 decoder, without equating an asset hash with publisher authorization.

**M1 — install/wait stage without mutating legacy shared control.** The successor may populate uniquely named candidate caches, verify all required bytes and store a *candidate-scoped* immutable descriptor. It must not call V2 \`rememberManifest\`/\`updateControl\` against \`logmate-offline-control-v2\` while V2 controls any client. A waiting-worker \`START_PRECACHE\` must remain safe and idempotent under this rule; sending the legacy API 1 bridge must not silently reintroduce a V2 control write. If staging fails or is interrupted, installation fails or remains unpromoted and the predecessor continues serving its own verified bytes.

**M2 — handover after old-client control ends, not on mere candidate readiness.** At activation, read the *latest* V2 state as historical input, validate required existing verified shell/manifest, and initialize V3 control in one short IndexedDB \`readwrite\` transaction. This is a proposed handover protocol, **not** a proof that every browser has already drained every predecessor event: test old in-flight \`waitUntil\` and client lifecycle on exact targets. Do not overwrite the legacy document; retain it for rollback diagnosis until explicitly governed retirement. If the V3 DB cannot open, its upgrade is blocked, or its transaction aborts, do not announce \`READY\` or erase V2 caches. Surface a recoverable hold/failure rather than falling back to an unverified newer shell.

**M3 — atomic control mutation only, with assets verified outside it.** V3 stores candidate descriptor, verified state, current/previous pointer and client assignments in a transactional control schema. Overlapping \`readwrite\` scopes serialize all V3 writers. Do not \`await fetch()\`, \`cache.match()\`, digest computation, UI work or arbitrary Promise chains *inside* an IndexedDB transaction: it may become inactive before the subsequent write. Perform expensive verification before the transaction; then commit a short, deterministic mutation referencing immutable candidate identity. Because Cache Storage and IndexedDB cannot share a transaction, a committed pointer must be rechecked against actual verified bytes on serving/restart; missing or changed bytes produce repair/hold, not a cross-version network fallback. Use \`complete\`/abort/error outcomes as transaction evidence, not merely individual request success.

**M4 — restart, failure and rollback.** On fresh Worker global, reconstruct state from V3 persisted records and independently verify referenced cache bytes. Handle IDB \`onblocked\`, \`versionchange\`, quota/eviction and interrupted activation explicitly. A \`strict\` durability hint, where supported, does **not** establish an independent backup or immunity from browser storage eviction; IndexedDB's durability options are browser hints, not EFB data-preservation guarantees (https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction). Maintain existing fail-closed rollback: the current V2 worker replies \`NOT_ROLLED_BACK\` because it lacks independent ledger/outbox/auth/schema compatibility proof. Do not use an old control pointer to authorize a remote Sync or resurrect obsolete account/session authority.

**M5 — retire only after negative predecessor evidence.** Once a V3 Worker is active and tested, require evidence that no V2 path can still create a mutable V2 control effect relevant to the active release. An absence of V2 traffic or a successful V3 install alone is not proof of retirement. Cleanup of old caches, V2 catalogue and obsolete per-client mappings is a separate consequence-bearing maintenance operation with rollback and data-survival tests.

**Safety properties:** (I1) a failed successor cannot destroy the predecessor's runnable verified shell; (I2) every served asset belongs to the build assigned to that request's controlled client and passes current byte verification; (I3) candidate promotion cannot discard an existing live client assignment or predecessor metadata; (I4) a control transaction cannot certify Cache API bytes it did not verify; (I5) local offline-readiness, local ledger durability, independent backup and remote Sync ACK are distinct claims. **Liveness property:** after an approved, fully verified update and controlled handover, a reloaded eligible client can obtain a valid assigned shell without a spurious 503; a safe hold is preferable to a false READY when storage is missing.

### D. Exact Engineering test packet — discriminate protocols, not count fixtures [VALIDATION / OPEN]

Run on an **approved** browser runner against a pinned NORMAL artifact and actual generated V2→V3 Worker scripts. This is a targeted integrated suite, not a new collection of synthetic pass labels.

1. **Legacy coexistence:** keep V2 active with two open tabs; install V3; force V2 root-navigation assignment before/after V3 candidate stage. Assert the V2 JSON is unchanged by V3 during waiting, old tab assets still verify, and V3 candidate data is isolated. Exercise \`START_PRECACHE\` to waiting V3.
2. **Handover/transaction:** close V2-controlled clients, allow V3 activation, interleave two V3 control writers and inspect the committed transaction and client mappings. Verify candidate/current/previous pointers and a real root+subresource fetch, not only \`GET_STATUS READY\`.
3. **Negative install and crash:** interrupt a font or shell download, terminate a Worker during staging, abort IDB transaction, block an IDB version upgrade, and simulate missing/corrupt Cache Storage bytes. Previous verified shell must remain or an explicit repair/hold must be shown; no silent newer-network mix.
4. **Release/identity and auth:** change Worker bytes while retaining shell \`appBuildId\`; change sidecar only; test wrong publisher/inventory; request \`/auth\`, \`/auth/action\`, \`/__/*\` and an unknown static path. Assert release identity is unambiguous and auth/reserved paths bypass offline interception.
5. **Recovery and user-state:** close/reopen browser, restart worker, preserve B1 30-store local ledger and unsynced outbox; separately export/restore \`.lbk\`; test Safari tab vs Home Screen, then *actual* managed iPad policy/device. A Chrome PASS cannot stand in for those contexts. Record sanitized worker/manifest SHA, OS/browser, active/waiting state, transaction completion/abort, catalogue before/after and HTTP outcomes. Do not upload real flight/owner records.

**Exit oracle:** both directions of legacy interleaving plus V3 concurrent writes PASS; no V2 shared mutation by waiting successor; no lost client assignment; offline root and subresources read from the intended verified build after restart; previous verified version survives interrupted update; Core CI debt remains separately visible. Until then: **NOT_EXECUTED / Production validation OPEN / PWA release HOLD**.

### E. Cross-track transfer, confidence and change watch

- **E (canonical owner):** transition protocol, publisher/release identity, current-pointer authority, anti-rollback, failure-domain/backup separation. This design is a proposal, not an authorized LogMate patch.
- **A (dependency):** standards-level worker lifecycle, storage-bucket partitioning, Web Locks cooperation, IndexedDB transaction lifetime and Cache API independence. No assumption that Safari tab, installed Home Screen and managed Web Clip share the same storage bucket.
- **C (transfer validation):** executable two-generation Chromium/Safari fault injection, offline fetch/503 and state oracles; Core Golden 4 FAIL remains independent.
- **B (Design Studio W121 transfer):** distinguish “candidate files downloaded”, “offline verified for this device/context”, “update waiting”, “repair required”, “local record saved” and “remote ACK”. Require screen-reader and human state-comprehension validation; no new visual design authority claimed.
- **D (Marketing 438 transfer):** install/update events and \`GET_STATUS READY\` are not durable-offline, installed-iPad or cross-device Sync proof. PWA ad exclusion remains the current conditional Marketing direction; avoid invasive analytics of flight records.

**CONTRADICTION:** \`new Worker uses a lock\` ≠ \`old Worker cooperates\`; \`IndexedDB commit atomic\` ≠ \`Cache Storage + IDB commit atomic\`; \`READY candidate\` ≠ \`client route is usable\`; \`new release identity\` ≠ \`publisher authorized\`; \`installed\` ≠ \`independent backup\`. **CHANGE WATCH:** IndexedDB transaction/durability browser behavior, Web Locks Worker/partition behavior, WebKit installed-PWA storage and MDM policy, Service Worker lifecycle implementation. **STOP RULE:** this resolves the adjacent architecture choice at SOURCE/SYNTHESIS level; do not add further paper fixtures. Next evidence must be Engineering's real V2→V3 runner and NORMAL artifact custody chain.


---

## 2026-10-23 cross-resource storage-pressure addendum — Worker update versus owner-ledger durability (E owner; A/C dependencies)

**Why this is a material adjacent contradiction:** The preceding V2→V3 migration design focuses on catalogue atomicity and retaining old verified shell bytes. It does **not** establish that those bytes, the browser's Cache Storage, and the user's Sembast Web / IndexedDB ledger survive the same storage-pressure event. This addendum is one integrated extension of 504, not a new synthetic test series.

### SOURCE — pinned product mechanics and current platform boundary

- Exact LogMate `main@59cd171176c58b598a4db55d128ffd21d406e862`, `tool/pwa_precache.dart` generated Worker: `shellCache(manifest)` uses `logmate-shell-${manifest.appBuildId}`; `fontCache(manifest)` uses `logmate-fonts-${manifest.fontSetId}`; `cacheGroup` independently writes each missing item with `cache.put`; `install` writes the candidate shell, then candidate metadata, then fonts/notices. On failed installation, there is no compensating deletion of partially written candidate caches. `activate` deliberately performs **no cache cleanup**, and old/failed candidates remain pending an explicit policy. These are code facts, not observed resource usage or a confirmed failure.
- WHATWG Storage Standard (living standard updated **2026-10-19**), https://storage.spec.whatwg.org/ : Cache API, IndexedDB and Service Worker registrations are local storage endpoints in the platform storage model; `estimate()` provides **estimates**, `persist()` requests persistent storage. Persistent storage is not an external backup.
- WebKit's documented storage policy (2023, checked **2026-10-23**), https://webkit.org/blog/14403/updates-to-storage-policy/ : Cache API and IndexedDB are within website-storage policy. Reaching an **origin quota** may cause a new write to fail with `QuotaExceededError`; separately, **overall quota/storage pressure/inactivity** can cause eviction, normally of the *entire origin*. Persistent mode can exclude an origin from automatic eviction under documented conditions; it is requested and heuristically granted, not automatically guaranteed by installation.
- MDN's maintained browser-comparison guide (updated 2026-01-05), https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria : quota/write failure and origin eviction are different mechanisms; when an origin is evicted, **both Cache API and IndexedDB data** can be removed. `navigator.storage.estimate()` values are approximate and not an admission guarantee. `navigator.storage.persist()` is a window-context request, not a Service Worker API (https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist).
- WebKit Safari 26.0 release (2025-09-15), https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ : on iOS/iPadOS 26, adding to Home Screen defaults to Web App, but users may disable “Open as Web App”; a Home Screen icon alone cannot certify the installed storage context. Managed Web Clips, Shared iPad and MDM policies remain separately unverified.

### SYNTHESIS — two failure mechanisms that must not be conflated

**F1: write rejection.** If a candidate shell/font write reaches the origin quota, a `cache.put` may reject; the candidate installation should fail, leaving the predecessor as controller. But writes already committed to the candidate cache are not part of a multi-file transaction and may remain. An interrupted or failed update can therefore consume storage even though no new Worker was activated. The current `no automatic deletion` policy avoids unsafe eviction of old shell versions by app code, but cannot guarantee an upper bound on candidate-cache growth.

**F2: origin-wide eviction.** When the browser chooses an eligible best-effort origin for eviction due to broader storage pressure or policy, the loss boundary is not just an expendable shell cache: the same storage origin can lose **Cache Storage, IndexedDB ledger/outbox, and Service Worker registration**. Retaining prior shell versions in code does not defend against this. It would be incorrect to claim that installing a new Worker *necessarily* causes eviction or that an individual `QuotaExceededError` immediately deletes the ledger; both require runtime/OS evidence.

The approximate footprint is `Σ distinct retained shell-build bytes + Σ distinct font-set bytes + control/partial-candidate bytes + owner ledger/outbox + browser overhead`. The exact footprint and eviction eligibility for a company-managed iPad are **UNKNOWN**. No 724-font total-byte size or real device headroom is asserted from the manifest entry count.

### MINTTAP DECISION — bounded release and recovery contract, proposed only

1. **Owner data outranks shell retention.** Do not optimize a verified-shell availability gate by making a false owner-data durability claim. An offline-ready shell is not a tested local-ledger survival guarantee, and a persistent-storage grant is not a portable backup.
2. **Measure separately, do not promise.** In each exact Safari tab, Home Screen Web App and managed-device context, record `navigator.storage.persisted()`, the result of any explicitly approved `persist()` request from the **page**, and `estimate()` before/after staged updates. Permission may be denied and estimates are not hard reservations. No automatic user-facing "safe storage" badge follows from these readings.
3. **No unbounded or blind cleanup.** Add a release-scoped cache inventory and a bounded, auditable retirement policy. Cleanup must first prove that a shell is no longer assigned to a live/returning client and that rollback/recovery constraints are satisfied. Never delete owner IndexedDB stores, unsynced outbox or an unverified user's only backup to reclaim space. Do not simply purge all old shell caches on `activate`.
4. **Staging and headroom admission.** Treat candidate bytes, partially downloaded fonts and notices as quota consumers; fail the update safely on `QuotaExceededError`, preserve diagnostic evidence and provide explicit repair/export options. Preflight estimates can advise but cannot certify that all writes will succeed. Recovery needs an independently restorable `.lbk` copy outside the same browser origin/failure domain, with privacy and ownership controls reviewed by Engineering.
5. **Do not conflate contexts or platforms.** Chrome's persistence policy, Safari-tab state, iPadOS Home Screen storage and a managed Web Clip are separate evidence envelopes. Neither Safari 26 install UX nor the WebKit published maximum quota certifies company-device storage policy or future OS behavior.

### VALIDATION — targeted Engineering-owned runtime oracles (all OPEN)

- **P1: failed staged update.** With a pinned NORMAL build and a preserved owner-ledger sentinel, force one mid-shell and one mid-font `cache.put` failure; verify install rejection, predecessor fetch availability, partial-cache inventory and owner ledger unchanged. Repeat across two failed updates to detect unbounded residue.
- **P2: pressure versus quota.** Separately exercise origin quota rejection and OS/browser-managed storage-pressure eviction in an approved test environment. Record which failure actually occurred; do not report quota rejection as an eviction test. A forced browser-site-data deletion is a destructive-loss *recovery* test, not proof of natural eviction frequency.
- **P3: grant/denial and restart.** Measure `persisted()` before/after a user-context persistence request, denial behavior, Worker restart, browser restart and dormancy. Reopen actual IndexedDB data and independently restore a backup if storage disappears. A persistent grant does not waive restore testing.
- **P4: retention/rollback.** With old and new clients, verify candidate staging and cache retirement never delete a still-assigned shell; after controlled retirement verify bounded cache growth and no stale-build 503. This composes with the V2→V3 catalogue-interleaving test, not a substitute for it.
- **P5: EFB envelope.** Repeat relevant scenarios on a real iPad under recorded iPadOS, supervision/MDM/Web Clip policy, available storage, install mode, network restrictions and backup destination. Chrome or unmanaged Safari results cannot promote this gate.

**DEPENDENCY / TRANSFER VALIDATION:** E owns release/data-loss consequences and retention authority; A supplies Storage Standard and WebKit bucket/quota semantics; C executes failure injection and device tests; B consumes Design Studio W121 to label "update downloaded", "offline verified", "backup verified" and "restore required" separately; D limits analytics to sanitized aggregate bytes/verdicts and avoids recording flight data, device identifiers or overstated install/durability claims. Software Engineering D006 retains sync/ACK and actual ledger implementation ownership. Marketing 438's conditional initial PWA ad exclusion is unaffected.

**CONTRADICTION:** `previous shell retained in Cache Storage` ≠ `previous shell guaranteed on device`; `Worker install rejected` ≠ `partial writes rolled back`; `QuotaExceededError` ≠ `origin evicted`; `persistent mode granted` ≠ `independent backup`; `Home Screen icon` ≠ `known storage context`. **CHANGE WATCH:** WebKit/Chromium eviction policy, persistence heuristics, iPadOS and MDM policy, font/shell release footprint, storage-pressure behavior. **GATE:** SOURCE/SYNTHESIS complete for this failure boundary; P1–P5 NOT_EXECUTED, Production validation OPEN, PWA release HOLD. Next useful evidence is actual Engineering/browser/device execution; no more standalone synthetic storage studies.
