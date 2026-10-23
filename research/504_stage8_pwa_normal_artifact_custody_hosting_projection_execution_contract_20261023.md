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
