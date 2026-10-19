# 426 — Stage 8 PWA Current-Head Evidence Custody, Source Drift and Release Admission

**Checkpoint:** 2026-10-20 07:10 KST. **Canonical start:** Web Manager main 090aed2c79b0e22bb1c561f6246abeb64da4bbf8. **Read-only product:** LogMate main 6101666530cb706a042ac82614c840af441895b1. **Owner:** E; A/C prerequisite owners, B/D transfers. **Gate:** SOURCE + bounded metadata/model VALIDATION; **current normal PWA, served Hosting bytes, real browser, owner-data restore and managed iPad OPEN; release HOLD**.

## 1. HISTORY / PROBLEM / PRINCIPLE

The preceding studies 415–425 established archived-worker and acceptance-archive risks and a six-gate release admission model. A distinct problem remains: **release evidence decays while source changes**. A green historical build, its uploaded archive, a current source tree, and an installed browser are not one identity. GitHub Actions artifact retention creates a custody deadline; source changes after the run create a reproducibility/currentness boundary. AppCache's opaque caching history motivated programmable Service Workers, but neither programmable install nor an immutable CI artifact proves that the **current** release was built, uploaded, served, installed, and recovered with user data intact.

**Design principle:** every admission claim names an exact source SHA, build mode, toolchain, output digest, workflow/run, artifact custody status, deployment target, observed runtime and owner-data scope. Historical negative evidence is retained without being promoted to a current production incident. Absence of executable evidence is BLOCKED/UNKNOWN, not a product FAIL.

## 2. SOURCE — current canonical repository and independent primary documentation

- Web Manager governance: AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md and studies 324, 415, 420, 421, 424; locally preserved 425 is a non-canonical handoff until committed.
- LogMate exact current source: https://github.com/yhappcom/logmate/tree/6101666530cb706a042ac82614c840af441895b1 ; PWA workflow: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/.github/workflows/data001-pwa-artifact-validation.yml ; Makefile; tool/pwa_precache.dart; tool/verify_pwa_artifact.dart; firebase.json. Product repository remained READ ONLY.
- Actual historical PWA run: https://github.com/yhappcom/logmate/actions/runs/38341345115 ; run artifact ID 11786039584, GitHub-reported digest sha256:d267bf9a4e8c30b1e40cf8133bdee3acf3e1dfa9cb3937da7b4d009da0180160. The digest identifies the uploaded archive, **not** an independently authenticated current normal build.
- GitHub Actions upload-artifact documentation: https://github.com/actions/upload-artifact — hidden files excluded by default, include-hidden-files must be deliberate; artifact digest and retention metadata are available. Do not enable blanket hidden uploads without a secret inventory.
- W3C Service Workers: https://www.w3.org/TR/service-workers/ ; WHATWG Storage: https://storage.spec.whatwg.org/ ; WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/ ; Firebase reserved URLs: https://firebase.google.com/docs/hosting/reserved-urls ; Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config ; Flutter Web FAQ: https://docs.flutter.dev/platform-integration/web/faq .
- Safari 26.0: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ — iOS/iPadOS Home Screen “Open as Web App” can be toggled off. This is an OS/version-specific CHANGE WATCH, not managed Web Clip acceptance.
- Design Studio W121: https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md ; Engineering D006: https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md ; Marketing 438: https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md . Their expertise is consumed, not re-authored.

## 3. SOURCE / VALIDATION — fresh GitHub run, artifact and source-drift evidence

At the observed checkpoint, LogMate main was 61016665 (committed 2026-10-17 23:45:46 UTC). The latest observed PWA-specific workflow run was 38341345115 at **2026-10-13 03:21:45 UTC**, for source fcff3372, conclusion SUCCESS. Its job steps explicitly report both “Build and verify normal PWA marker isolation” and “Build and verify canonical EFB acceptance artifact” SUCCESS. The **normal build was written to build/web-normal but not uploaded**; the uploaded artifact is the development-only Acceptance build in build/web, with LOGMATE_PERSISTENCE_ACCEPTANCE=true. This is a positive historical CI step observation, not a downloadable current normal release artifact.

The GitHub compare endpoint from that run SHA to current main reports **45 commits ahead, 0 behind, 62 changed files**, including the PWA workflow, tool/pwa_precache.dart, tool/precache_flutter_web.dart, tool/verify_pwa_artifact.dart and the local database capability codec. Therefore even a fully closed old archive cannot stand in for current-head build identity. This does **not** prove the changed files introduce a defect.

Artifact 11786039584 was reported **expired=false** at inspection, created 2026-10-13 03:25:26 UTC, expiry **2026-10-20 03:25:22 UTC (12:25:22 KST)**, size 37,783,048 bytes, seven-day retention. Its recorded digest matches the preserved historical archive studied in 415–425. That archive was previously audited at 951/952 manifest-required files because a hidden .last_build_id was missing; this is **historical Acceptance package FAIL**, not current production FAIL. GitHub metadata alone does not prove the artifact remains downloadable at every later instant. The connector did not supply binary download; no new archive custody or normal-build digest is claimed.

The current workflow's push branches are feature/data001-domain and integration/stage7-stage-d-pwa-20261012; main is not included in that automatic trigger, although workflow_dispatch is available. The latest successful PWA run is therefore not an automatic main release certification. The source verifier checks manifest resource hashes and marker strings but not complete Worker-embedded-manifest/sidecar/bootstrap semantic parity; this was already identified in 423 and is not re-proved here. Firebase Hosting ignores **/.*; GitHub upload-artifact defaults to excluding hidden files. Neither blanket hidden upload nor silent removal of a required manifest item is an approved fix.

## 4. VALIDATION — independent evidence-custody admission model

A standalone Python standard-library metadata policy evaluator was executed against a recorded GitHub response snapshot, plus **17/17 deterministic unit tests PASS**. It rejects historical green as current green, acceptance-mode as normal-mode, wrong-source and wrong-workflow artifacts, missing digest, expired artifact, absent post-upload package, and metadata-only promotion to deployed/browser GO. The real snapshot yields:
- NO_EXACT_HEAD_SUCCESSFUL_PWA_RUN;
- NO_CURRENT_NORMAL_POST_UPLOAD_ARTIFACT;
- HISTORICAL_ARTIFACT_EXPIRING_WITHIN_24H (as of 07:10 KST);
- HISTORICAL_PACKAGE_CLOSURE_FAIL_RETAINED;
- G1 current normal build BLOCKED, G2 post-upload closure BLOCKED, overall HOLD.

**Limits:** the 17 tests validate the *admission model*, not Flutter, Dart, Firebase, WebKit, Chromium, iPad, synchronization, user records or actual release. The snapshot is a bounded observed dataset, not a live GitHub monitoring service. The evaluator deliberately cannot output product GO from metadata alone. It should not be mistaken for the full six-gate admission model in 425.

## 5. SYNTHESIS — eight connected release-evidence questions

1. **Currentness:** a green historical run is meaningful historical evidence but cannot certify a head 45 commits later.
2. **Build vs package:** a successful normal-build CI step does not produce a recoverable normal archive if the workflow uploads only the Acceptance output.
3. **Archive custody:** an artifact digest and expiry timestamp support provenance/retention decisions, not served-byte parity or post-expiry recoverability.
4. **Hidden resources:** excluding a generated hidden marker during upload and Hosting can break a Worker manifest; globally enabling hidden uploads can expose secrets. Fix resource classification and re-generate the entire manifest/Worker consistently.
5. **Verifier authority:** byte hashing against a mutable sidecar is not independent release provenance; Worker-embedded manifest, bootstrap, version pinning and server responses require explicit cross-checks.
6. **Runtime scope:** a downloaded archive does not establish Worker install/control, update, offline re-entry or managed-iPad behavior. Safari tab, Home Screen web app and managed Web Clip are distinct evidence contexts.
7. **Data custody:** Cache Storage repair is not Sembast/IndexedDB durability, independent .lbk restore, outbox survival, Sync ACK or native-device convergence. Do not use origin-wide clear as routine recovery.
8. **Public/marketing truth:** no offline/install/sync/advertising claim is promoted from historical CI or synthetic Worker evidence; Marketing's initial PWA ad-free/HOLD recommendation remains separate from platform capability.

## 6. MINTTAP DECISION — conditional Engineering handoff, NOT SHIPPED

**First executable checkpoint: source-pinned normal build + post-upload closure.** Engineering should run normal make build-pwa on an approved SHA and toolchain, retain the normal output as a distinct artifact, record its SHA-256, re-download the uploaded archive and verify every required file, Worker/sidecar/bootstrap parity, executable URL identity, archive root and secret inventory. Do not change LogMate from Web Manager. Keep Acceptance artifact and normal release in different namespaces and prohibit promotion of Acceptance mode.

**Second checkpoint: same-digest Hosting closure.** Test Firebase Emulator and a disposable preview/staging deployment with exact served bytes, MIME, headers, 404 on missing static files, /__ reserved Auth paths and encoded executable aliases. Emulator PASS is not deployed PASS.

**Third checkpoint: actual browser and owner-data survival.** Run Chromium and WebKit fresh/upgrade/offline/repair cases; preserve unsynced records and independent backup before fault injection. Then perform destructive .lbk restore on disposable data, followed by representative physical managed-iPad validation with actual policy envelope. Do not assume unattended device-to-device sync or iPad background execution.

**Custody policy:** keep compact immutable provenance (source SHA, toolchain, workflow/run, build mode, manifest and archive digests, verified response digests, test oracle, environment, date, expiry, evidence class) for each candidate; retain the exact binary until all runtime gates requiring it complete; do not store credentials, flight records or sensitive analytics in public CI artifacts. Define a retention/rebuild plan before artifact expiry; a later rebuild, even from the same SHA, is a *new* artifact requiring its own digest and proof. The old Acceptance artifact's imminent expiry is an evidence-custody warning, not a release blocker for a current normal build that does not yet exist.

## 7. Five-track maturity and transfers

| Track | Evidence maturity / risk | Ownership in this checkpoint |
| --- | --- | --- |
| E | Highest live risk: source→CI→archive→Hosting custody gap, rollback/data preservation | **Primary**: release admission, expiry/retention, artifact identity, secure deployment and recovery gates |
| A | Strong standards/source/archived Worker models; current Chromium/WebKit mechanics OPEN | Supplies Worker scope/update, URL, Cache Storage and Safari installed-context distinction |
| C | Model tests and negative oracles mature; current runtime/AT/device validation OPEN | Owns post-upload byte oracle, CI failure propagation, browser/quality/performance and negative controls |
| B | Update/offline/recovery content states specified; actual usability/AT evidence OPEN | Defines truthful stale-build, old-version-usable, backup-required and recovery UI, consuming W121 |
| D | Web discovery/measurement competence established; installed-PWA acquisition and continuity unmeasured | Keeps claims/analytics privacy-minimal; does not conflate CI artifact with installed active users |

**TRANSFER VALIDATION:** W121 prioritizes exact runtime evidence over another pre-runtime manifest; Engineering D006 distinguishes local save, remote ACK and convergence; Marketing 438 keeps PWA ads excluded in the first release. **CONTRADICTION:** STATUS.md and research/README.md are materially stale relative to persisted 420/421/424. Their correction is governance hygiene, not product validation.

## 8. OPEN / DEPENDENCY / CHANGE WATCH / STOP RULE

**OPEN:** exact current normal PWA build and upload; upload/re-download SHA closure; Firebase Emulator and served-byte parity; real Chromium/WebKit Worker lifecycle and repair; current data-capability-16 records/outbox; independent .lbk restore; actual physical managed-iPad enrollment/MDM/installation/storage/offline envelope; native↔PWA Sync authority and transport; accessibility/human testing. **DEPENDENCY:** Engineering owns build, CI, verifier changes and runtime execution. Web Manager owns requirements and evidence admission. **CHANGE WATCH:** GitHub artifact action defaults/retention, Firebase Hosting/Reserved URLs, Flutter-generated bootstrap/Worker, WebKit storage and Home Screen behavior, OS/MDM policy, W3C Service Worker and WHATWG Storage.

**Stop rule:** additional historical Worker micro-variants have lower value than current normal build custody. Reopen generic research only for a materially new upstream standard/platform fact, new source contradiction, or a test result that changes the release boundary. **Stage 8 stays active; Track E bottleneck; product/runtime/managed-iPad validation OPEN; PWA release HOLD.**
