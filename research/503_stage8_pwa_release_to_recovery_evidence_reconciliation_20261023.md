# 503 — Stage 8 PWA Release-to-Recovery Evidence Reconciliation and Execution Gate

**Checkpoint:** 2026-10-23 KST. **Canonical read:** `yhappcom/web-manager/main@bcb96dd7a308d928aca29c86f8c01ea7bd8ad7e3`. **Product read-only:** `yhappcom/logmate/main@59cd171176c58b598a4db55d128ffd21d406e862`. **Owner:** Track E; A/C critical dependencies; B/D transfer. **Verdict:** Stage 8 source/standards synthesis; current production validation OPEN; PWA release HOLD. No new Flutter, Dart, browser, Safari, MDM or production test was executed in this checkpoint.

## Purpose and source hierarchy

Canonical Web Manager studies 427, 431, 437, 460 and 480 establish the normal-artifact, Worker/cache and bounded whole-ledger recovery principles. The later 493–502 investigations were retained in conversation-local files but not committed to this repository. This integrated checkpoint records only source-supported additions, resolves conflicting evidence tiers and consolidates the actionable execution gate; it does **not** retroactively certify those local reports or turn synthetic models into production evidence. Current pinned source overrides stale STATUS assertions (notably the old Firebase catch-all rewrite and old Flutter pin).

Read at run start: AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md, current 480 and 427/324/460; recent commits. Cross-repository transfer: Design Studio W121 (exact runtime before further manifests), Engineering D006 (logical operation vs delivery/apply/ACK), Marketing 438 (first-release PWA ads HOLD). Other repositories were read-only.

## History/problem → principle → standard → implementation → failure → judgment

AppCache's opaque update semantics gave way to programmable Service Workers; this improves offline control but creates separate source, build, archive, hosted-byte, Worker, cache, ledger and recovery identities. The required chain is:

`pinned source/workflow → NORMAL build tree → exact file inventory and Worker/sidecar consistency → archived/downloaded bytes → Hosting-served bytes → installed/controlling Worker → IndexedDB owner-ledger preservation → independent external backup/restore → separately authorized Manual Sync`.

Every arrow requires its own oracle. SHA-256 proves agreement with a selected reference, not the reference's authority; a manifest checksum is not an author signature. HTTP caching and Cache API caching are distinct; active Worker and local durable ledger are distinct. An accepted backup is not an activated ledger, nor does it authorize remote replay.

Primary normative/platform references: W3C Service Workers https://www.w3.org/TR/service-workers/ ; WebKit storage policy https://webkit.org/blog/14403/updates-to-storage-policy/ ; GitHub upload-artifact behavior https://github.com/actions/upload-artifact ; GitHub artifact digest behavior https://github.blog/changelog/2025-03-18-github-actions-now-supports-a-digest-for-validating-your-artifacts-at-runtime/ ; Firebase Hosting configuration https://firebase.google.com/docs/hosting/full-config and reserved URLs https://firebase.google.com/docs/hosting/reserved-urls . OS/MDM/storage/attestation support remains CHANGE WATCH; standards do not establish company-iPad policy.

## SOURCE — current LogMate main, inspected 2026-10-23

1. `.github/workflows/data001-pwa-artifact-validation.yml` uses Flutter **3.47.5**, builds NORMAL to `build/web-normal`, then development Acceptance to `build/web`, uploads **only Acceptance**, and has no automatic `main` push trigger. Manual dispatch exists. This is a source-level custody gap, not proof of a wrong deployment.
2. `firebase.json` uses `hosting.public=build/web`, dotfile ignore `**/.*`, and three explicit `/auth` rewrites. It has **no catch-all SPA rewrite**. Hosting-served bytes and Firebase `/__` helper routing have not been tested here.
3. `tool/verify_pwa_artifact.dart` checks manifest-listed files' size and SHA-256, 724 font entries, 148 notices and Worker/bootstrap markers. It does not explicitly enforce decoded relative path confinement, reject duplicate/aliased file paths, compare complete Worker-embedded and sidecar manifests, or prove complete archive file-set closure. This is a static coverage observation, **not** a demonstrated exploit or corrupt build. Actual Dart negative tests remain OPEN.
4. `web/flutter_bootstrap.js` registers project-owned Worker with `updateViaCache:'none'`, starts precache and guarded promotion without gating first paint. App bootstrap is not an offline-readiness acknowledgement.
5. `.github/workflows/data001-browser-persistence-validation.yml` still pins Flutter **3.38.7** and triggers automatically only for `feature/data001-domain`; `pubspec.yaml` requires Dart **^3.12.0**. This is a source-level SDK/trigger mismatch requiring Engineering correction, not a recorded execution failure.
6. B1 whole-ledger backup/restore is scoped to 30 registered Sembast stores; source inspection of the fresh-staging gate identified 12 explicitly empty-checked stores and 18 not individually empty-checked (some have separate semantic checks). Rejection-with-preservation across all 30 and cross-tab transaction behavior require **real** Dart/browser tests. The fixed Web DB opener `logmate_ledger` and Repository reuse mean staging commit does not by itself switch the active app DB.
7. WebKit's separate Safari vs Home Screen storage contexts, origin eviction and managed-device policy must be validated per OS/display/MDM envelope. No unattended native↔PWA device sync, persistent storage, background execution or independent iPad backup is assumed.

Pinned source links: https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/.github/workflows/data001-pwa-artifact-validation.yml ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/.github/workflows/data001-browser-persistence-validation.yml ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/tool/verify_pwa_artifact.dart ; https://github.com/yhappcom/logmate/blob/59cd171176c58b598a4db55d128ffd21d406e862/firebase.json .

## VALIDATION — separate actual execution, model and non-execution

| Evidence | Exact scope | Verdict and limit |
|---|---|---|
| Core Product Validation 39881725421, 2026-10-23, main `59cd1711` | macOS Flutter/Dart host suite | **798 PASS / 4 Welcome Golden FAIL / 1 SKIP**; Core quality gate is NOT green. |
| Eight B1 tests within that host suite | checksum/format, owner/staging, rollback, replica identity, file I/O, key checks | **8 host PASS**, not browser IndexedDB or managed iPad. |
| Welcome Golden diagnostic images | portrait/focus/landscape/200% text | 25/25/25/57 changed pixels; common small raster delta is observed but root cause OPEN; do not silently update baselines. |
| Chrome IndexedDB run 39086764619, 2026-10-18 | different exact source ref, browser record close/reopen | **1 Chrome PASS historical**, not current-main B1 whole-ledger or browser-process restart. |
| Current main Core `sembast_web_reopen_test.dart` | browser-only conditional test under macOS host runner | **SKIP**; neither browser PASS nor browser FAIL. |
| Local 491/492/495 matrices | 50 + 16 + 24 proposed scenarios | **90 NOT_EXECUTED**; not managed-iPad proof. |
| Local 493/494 sentinel tests and 500/501 reference models | proposals/synthetic Python checks | **NOT_EXECUTED in Dart/product**; not runtime vulnerability proof. |

Actions references: https://github.com/yhappcom/logmate/actions/runs/39881725421 and https://github.com/yhappcom/logmate/actions/runs/39086764619 . The later non-main Core run 39882327653 cannot be promoted to current main.

## MINTTAP DECISION — executable Engineering handoff (proposal only)

**G0 exact provenance:** pin main SHA, lockfile, Flutter/Dart, approved font archive, workflow revision and all gate outcomes. Preserve Core Golden failures.

**G1 isolated NORMAL:** build `BUILD_WEB_OUTPUT=build/web-normal make build-pwa`; explicitly archive NORMAL, not the Acceptance `build/web`; verify absence of development acceptance marker.

**G2 fail-closed file closure:** actual Dart negative tests for decoded traversal, symlink escape, duplicate/aliased paths, hidden/missing/extra members, mutated Worker with unchanged markers, Worker-sidecar mismatch; exact expected inventory and hash for all resources, including Worker. Distinguish code-hardening requirement from demonstrated exploit.

**G3 immutable custody:** upload NORMAL under an unambiguous immutable artifact name, record source/job/digest, download into a clean job, re-enumerate file set and hashes; explicit failure on mismatch, not warning-only. Confirm attestation availability for the actual repository/account before making it mandatory.

**G4 Hosting:** select approved NORMAL output explicitly, test served bytes, response codes/MIME/headers, missing static 404 and Firebase `/__` plus `/auth` boundaries. Reject HTML-200 for missing JS/WASM/font.

**G5 browser/data:** current-main Chrome Sembast Web reopen and B1 whole-ledger export/import; 30-store preexisting sentinel rejection and rollback; tab concurrency, offline Worker install/update, interruption, quota and unique unsynced outbox preservation. Keep Cache API and IndexedDB test oracles separate.

**G6 physical iPad:** Safari tab vs installed Home Screen vs managed Web Clip/Shared iPad separately; record OS/MDM, display mode, storage identity, Files destination, interruption and independent restore. No browser-to-fleet promotion.

**G7 owner/Sync/UX:** preserve SessionGate/owner verification, distinguish `file decoded`, `staging committed`, `active ledger reopened`, `external backup independently verified`, `remote ACK`; Manual Sync requires explicit user action/current authority/idempotency/reconciliation. PWA advertising remains separately gated.

**G8 adjudication:** each observation carries exact source SHA, NORMAL archive digest, scenario, environment, outcome and `PASS/FAIL/NOT_EXECUTED/BLOCKED`. UNKNOWN never becomes PASS. Release remains HOLD until applicable G0–G8 execution evidence is complete.

## Five-track balance / dependency / contradiction

| Track | Relative maturity and pressure | Role in this bundle |
|---|---|---|
| **E primary** | Stage 8 source-depth high; missing archive/Hosting/restore/MDM execution; highest consequence | Own release custody, security, data survival and HOLD. |
| **A prerequisite** | Worker/storage standards mature; current browser/iPad behavior OPEN | Own scope, update, Cache API vs IndexedDB and storage-context mechanics. |
| **C execution** | Real host and historical Chrome evidence, current Golden FAIL and browser/device OPEN | Own exact-source failure diagnosis, runtime/AT/performance/negative oracles. |
| **B transfer** | Restore-state requirements mature; human/AT execution OPEN | Own honest first-run/update/recovery labels; consume Design Studio W121. |
| **D transfer** | Generic discovery/analytics mature; field install/usage OPEN | Own privacy-minimized evidence and public-claim restraint; consume Marketing 438. |

**TRANSFER VALIDATION:** Design Studio W121 https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md explicitly prioritizes execution over more manifests. Engineering D006 https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md separates operation/delivery/apply/ACK. Marketing 438 https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md recommends initial PWA ad exclusion; not a policy prohibition for all PWAs.

**CONTRADICTION:** `manifest hash match ≠ authenticated release`; `archive present ≠ normal release`; `worker active ≠ offline-ready ≠ owner data durable`; `host B1 PASS ≠ browser B1 PASS`; `historical Chrome PASS ≠ current-main Chrome PASS`; `staging commit ≠ active DB cutover`; `local restore ≠ remote Sync authority`; `browser PASS ≠ managed-iPad PASS`.

**OPEN:** actual NORMAL archive/served bytes, Dart negatives, current-main Chrome/Safari B1, Golden cause, physical/managed iPad and Files custody, Sync backend, legal/privacy/aviation obligations. **DEPENDENCY:** Engineering implementation/execution, Design Studio visual/AT, Marketing ad policy, fleet MDM administrators. **CHANGE WATCH:** Flutter, GitHub artifact/attestation behavior, WebKit storage/installation, Firebase Hosting and OS policy. **STOP RULE:** further synthetic micro-models do not close G0–G8; next high-value action is actual Engineering execution, not another paper checklist.
