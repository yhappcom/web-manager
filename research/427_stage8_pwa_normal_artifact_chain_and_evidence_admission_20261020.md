# 427 — Stage 8 PWA Normal-Artifact Release Chain, Controlled Custody and Admission Contract

**Checkpoint:** 2026-10-20 08:10–08:35 KST. **Canonical Web Manager:** main 1476db752f7a0849351940340c10c1dd13648a67. **Read-only LogMate:** main 6101666530cb706a042ac82614c840af441895b1. **Owner:** Track E; Track A/C prerequisites and Track B/D transfers. **Gate:** SOURCE + independent fixture VALIDATION; current normal build/served bytes/browser/managed-iPad/owner-data recovery OPEN. **Release decision: HOLD.**

## 1. HISTORY / PROBLEM / DESIGN PRINCIPLE

AppCache-era opaque application caching did not provide programmable, trustworthy update control; Service Workers make request interception and offline caching explicit, but transfer the burden of update safety to build, delivery, cache identity and recovery contracts. A release is not one object: source tree, compiled normal output, generated sidecar manifest, Worker-embedded manifest, uploaded archive, Firebase-served resources, installed controller and owner data have distinct identities and failure domains. Studies 415–426 diagnosed archived Acceptance worker/cache/URL failure modes and a historical source-drift/custody gap. This checkpoint converts those observations into an executable **normal-artifact custody contract** and an Engineering-ready validation sequence, without repeating the old Worker micro-tests.

**Principle:** reject claims when exact source SHA, build mode, complete file inventory, upload/download bytes, deployment target, actual browser behavior or independent record restore are absent. Never turn an Acceptance artifact into a normal production candidate. Never fix a missing hidden manifest resource by uploading all hidden files without secret review.

## 2. SOURCE — canonical observations and freshness

1. Web Manager AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md and studies 421, 424, 426 were read from main. The older STATUS.md is not evidence of current LogMate deployment.
2. LogMate main source is unchanged from the 426 checkpoint at 6101666530cb706a042ac82614c840af441895b1 (commit date 2026-10-17 23:45:46 UTC). Exact PWA workflow: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/.github/workflows/data001-pwa-artifact-validation.yml ; Makefile; tool/pwa_precache.dart; tool/verify_pwa_artifact.dart; firebase.json.
3. The workflow builds a normal candidate to build/web-normal and validates it in that build directory, then builds development-only Acceptance into build/web and uploads only build/web. Its push branches are feature/data001-domain and integration/stage7-stage-d-pwa-20261012, not main; workflow_dispatch is available. The normal build is **not** retained as a post-upload downloadable artifact.
4. The generator _describeShell recursively includes hidden files except its explicit three generated exclusions and font-fallback directory; the historical archive included .last_build_id in its required manifest, while GitHub upload-artifact defaults to exclude hidden files and firebase.json Hosting ignore includes **/.*. Historical Acceptance archive therefore failed the 951/952 resource closure audit. This is a **historical Acceptance artifact** result, not an observed current normal production failure.
5. tool/verify_pwa_artifact.dart verifies manifest resource sizes/hashes and markers but does not independently compare the complete Worker-embedded manifest to the sidecar or prove bootstrap semantic configuration, deployed bytes, or browser install. These are separate Engineering requirements, not assertions that current normal Dart validation was executed here.
6. GitHub Actions run 38341345115, source fcff3372b3c25a3ae40ea68f5faea3fea023c5c0, 2026-10-13 03:21:45 UTC, was SUCCESS; both normal build and Acceptance build steps succeeded. Its **only** uploaded artifact is Acceptance ID 11786039584, digest sha256:d267bf9a4e8c30b1e40cf8133bdee3acf3e1dfa9cb3937da7b4d009da0180160, expiry 2026-10-20 03:25:22 UTC (12:25:22 KST). At this run's API inspection, expired=false, not a guarantee of future download. The connector does not provide its binary download.
7. A newer real-Chrome IndexedDB test exists: workflow run 39086764619 on 2026-10-18 01:30:50 UTC, exact PR source d1b2f71020d7da4d24e9204e2c43bf6c47d2ec3d, completed SUCCESS including the “IndexedDB reopen in real Chrome” step. This is **real Chrome persistence evidence for that PR SHA**, not current main, Service Worker update, deployed Firebase Hosting or managed iPad. The separate L2C multi-platform run 39090249808 likewise does not certify current main PWA.
8. Current primary platform sources: https://github.com/actions/upload-artifact ; https://docs.github.com/en/actions/tutorials/store-and-share-data ; https://docs.github.com/en/actions/concepts/security/artifact-attestations ; https://firebase.google.com/docs/hosting/full-config ; https://firebase.google.com/docs/hosting/reserved-urls ; https://www.w3.org/TR/service-workers/ ; https://storage.spec.whatwg.org/ ; https://webkit.org/blog/14403/updates-to-storage-policy/ .
9. Specialist transfer evidence: Design Studio W121 https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md ; Software Engineering D006 https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D006_replication_sync_consistency_idempotency_conflicts.md ; Marketing 438 https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md . These are scoped handoffs, not re-authored general expertise.

## 3. SYNTHESIS — ten connected release-chain questions

**Q1 Source and mode:** a successful workflow run must bind to the exact claimed SHA and mode (NORMAL versus ACCEPTANCE); a normal-build step preceding an Acceptance upload is not a normal archive. The compile-time Acceptance harness is a development-only contaminant in any production candidate.

**Q2 Build inventory:** after generating the Worker and sidecar, compute a complete, reviewed build-tree inventory. The manifest is not itself the entire tree: it excludes the generated Worker and sidecar to avoid self-reference. A release descriptor must separately record their SHA-256 and all other delivered files.

**Q3 Hidden resource policy:** current generator/Hosting/upload policies disagree on dotfiles. Either remove the non-deliverable marker from the Shell contract and regenerate all derived identities consistently, or explicitly approve a narrowly scoped deployable file and update both upload and Hosting policies. Do not enable blanket hidden-file upload or weaken the verifier to ignore a required file. A secret inventory is mandatory before relaxing excludes.

**Q4 Byte-level closure:** after upload, download the exact artifact and compare the full file set, lengths and SHA-256 to the sealed pre-upload inventory. GitHub upload-artifact's archive digest is useful custody evidence, but the download action's digest mismatch produces a **warning**, so the release gate must independently fail on missing or altered bytes. Record archive ID/digest and exact build SHA.

**Q5 Signed provenance:** for actual releases, evaluate GitHub artifact attestations and verify them against expected repository, workflow, source SHA and digest; attestation is not proof that code is secure or that Firebase served the same bytes. Availability and plan/visibility requirements must be verified before requiring the feature.

**Q6 Hosting closure:** Firebase Hosting public directory is build/web, while normal CI output is build/web-normal. A deployment candidate must explicitly select the verified normal artifact and never accidentally deploy Acceptance output. Compare deployed static responses, including Content-Type/status/redirect behavior and exact bytes, to the sealed release inventory; reserved Firebase /__ and Auth routes require their own routing tests.

**Q7 URL alias policy:** file inventory equality alone cannot establish that encoded URL aliases or unknown executable paths preserve version pins. Use 424's URL authority contract and actual Firebase Emulator + deployed responses; do not equate local HTTP aliases with Firebase behavior.

**Q8 Browser lifecycle:** Worker install/wait/activate/control, old/new clients, offline restart and failed update require real Chromium and Safari/WebKit runs. Chrome IndexedDB reopening at a different PR SHA proves neither Service Worker control nor current release viability.

**Q9 User-data custody:** Cache Storage/Worker repair is not Sembast/IndexedDB owner-record restoration. Independently verify flight records, unsynced operations, backup export and .lbk import/reopen; distinguish local persistence from remote Sync ACK and conflict reconciliation. Never delete origin records to repair a Shell.

**Q10 Managed iPad:** Safari tab, Home Screen web app, Web Clip, MDM policy, Shared iPad and device backup/eviction are distinct contexts. Generic platform support does not prove unattended sync, background transport, storage persistence or company-EFB installation.

## 4. VALIDATION — independent release-chain fixture auditor

A Python 3.13 standard-library oracle was implemented and executed locally with **15/15 deterministic unit tests PASS**. It accepts an unpacked build, a downloaded ZIP and optionally a static served-byte snapshot; parses schema-v2 manifest Shell/fonts/notices; checks duplicate/traversal/encoded path safety, lengths/hashes, Worker/sidecar existence, full archive file-set and byte parity, served snapshot parity, and rejects unreviewed hidden files anywhere in the build. Negative controls cover missing ZIP member, modified ZIP bytes, changed build resource, hidden required marker, hidden unmanifested secret, duplicate manifest path, encoded traversal, duplicate ZIP member, served mismatch, altered Worker, malformed schema and path safety. Positive controls cover clean fixture, encoded font path and matching served snapshot.

**Independent audit output is not a release GO:** fixtures contain miniature synthetic HTML/JS, not a LogMate build. This oracle does not parse the Worker-embedded manifest, verify a signed attestation, prove CI checkout identity, perform Firebase route/URL alias resolution, install a Service Worker, access real Chrome/Safari, measure iPad runtime or restore owner records. A served directory snapshot is not equivalent to a live Hosting fetch. Do not label this a 15-test product PASS.

Local evidence bundle: release_chain_audit.py, test_release_chain_audit.py, tests.log. The tool intentionally rejects current source's historical .last_build_id hidden-manifest pattern until Engineering resolves the policy, rather than silently auto-excluding it.

## 5. MINTTAP DECISION — PROPOSED Engineering execution contract, NOT SHIPPED

**A. Exact-source controlled build:** manually trigger a dedicated checkpoint for current main SHA; preserve Flutter 3.47.5 and approved Stage C font ZIP digest. Build NORMAL in an isolated output, run the actual Dart verifier, record output inventory and sidecar/Worker/bootstrap consistency. Acceptance may be built separately but is never an eligible release artifact.

**B. Explicit file policy:** define deployable resource classes and disallowed secrets before packaging. Resolve .last_build_id as a generated build-marker classification defect, regenerate Manifest and Worker, and rerun verifier. Preserve security exclusions for unknown dotfiles. Do not upload a whole worktree.

**C. Post-upload independent gate:** upload the reviewed NORMAL directory as a separately named immutable artifact; download that exact ID in a clean job; compare complete bytes and fail closed on any missing/extra/mismatched member. Store a compact provenance record with source SHA, toolchain, mode, archive digest, inventory hash and retention date. Extend retention for actual release evidence only within repository limits; do not assume an expiring diagnostic artifact remains recoverable.

**D. Deployment staging:** take only the verified downloaded NORMAL artifact as the deployment input, never rebuild between verification and deploy. Validate Firebase Emulator routing and /__ reserved namespace, then exact deployed static bytes/headers/routes before promoting any release claim. Do not deploy the dev Acceptance build or infer production status from emulator alone.

**E. Runtime/data admission:** separately execute Chromium, Safari tab, installed Home Screen, physical/managed iPad where permitted, offline/online transitions, old-client pinning, broken Shell repair, rollback rejection, record reopen, independent .lbk backup/restore, and Sync authority. Maintain six independent G1–G6 gate statuses; UNKNOWN/BLOCKED/NON-EXECUTION never auto-promotes to PASS.

**F. Provenance hardening:** GitHub attestation is a candidate addition for release provenance after confirming repository eligibility and permissions; it supplements, never replaces, full byte parity and actual runtime verification. Revalidate on every source SHA or hosting policy change.

## 6. Five-track bottleneck comparison and TRANSFER VALIDATION

| Track | Stage 8 / PWA evidence | Pressure / assignment |
| --- | --- | --- |
| E — Security/Operations | Strong historical source/model; current normal archive, Hosting custody and release trust absent | **PRIMARY BOTTLENECK**. Own exact-head release custody, secret exclusion, attestations, deployment rollback and user-data preservation boundaries. |
| A — Browser/Platform | Strong Worker/cache/source fundamentals; current real controller lifecycle absent | Supply Service Worker URL/control/install/activation and Safari context prerequisites to E/C; do not duplicate release custody. |
| C — Quality/Accessibility | Historical Node VM and PR-specific real Chrome IndexedDB PASS; current normal SW/Hosting/physical device absent | Own exact browser oracles, negative tests, performance, accessible recovery states and evidence labels. |
| B — UX/IA | Recovery/offline UX requirements available; no current device/human validation | Specify non-destructive update, backup and repair messages; transfer to Design Studio W121 execution packet. |
| D — Discovery/Analytics | Privacy-aware claim constraints available; no release-grade install/acquisition telemetry | Forbid unsupported install/offline/sync/ads claims; define privacy-minimal evidence after release is actually verified. |

**CONTRADICTION:** “real Chrome IndexedDB PASS” from PR16 does not contradict “current normal PWA release HOLD”; they test different source, execution scope and product contract. “GitHub artifact digest exists” does not contradict historical 951/952 required-resource mismatch; an intact ZIP can faithfully preserve an incomplete file set. “Build verified” does not imply the uploaded ZIP contains the same build.

## 7. OPEN / DEPENDENCY / CHANGE WATCH

**OPEN:** current-head NORMAL CI execution; downloadable normal artifact; archive after-upload byte closure; Worker-embedded/sidecar/bootstrap semantic parity; actual Firebase Emulator and deployed-byte verification; Chrome/WebKit controlled lifecycle; managed iPad, Web Clip and offline storage; owner-record/.lbk restoration; Sync contract; publisher ads/consent. No new deployment or product repository mutation was performed.

**DEPENDENCY:** Software Engineering owns code and CI changes; Design Studio owns reusable interaction visual quality; Marketing 438 retains PWA ads OFF pending policy/implementation evidence. Web Manager records web-specific admission contracts only.

**CHANGE WATCH:** GitHub upload-artifact major versions, hidden-file behavior and artifact retention; GitHub attestation availability/permissions; Firebase Hosting ignore/rewrites/reserved URLs; Flutter generated bootstrap/Service Worker policy; WebKit Home Screen/storage policy; W3C Service Worker and WHATWG Storage behavior. Source checks are time-bounded to this checkpoint.

**Next meaningful checkpoint:** Engineering produces one exact-head NORMAL PWA artifact with a sealed, post-download-verified inventory; Web Manager/Track C then runs Firebase route/served-byte and actual browser tests. Stop adding historical-worker synthetic variants without new runtime evidence.