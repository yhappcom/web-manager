# 509 — Stage 8 LogMate PWA release-artifact custody: independent disk gate, adversarial fixtures, and deployment handoff

Date: 2026-10-24 (Asia/Seoul). Owner: Track E Web Architecture/Security/Operations; Track A/C supply platform and independent quality oracles. Evidence status: **DISK-ONLY VALIDATION / PRODUCT RUNTIME OPEN**. This is a substantial continuation of 508 §§6–10, not a new generic PWA primer.

## 1. Canonical refresh and curriculum allocation [SOURCE / DEPENDENCY]

Re-read Web Manager main at start **f8431d7a7e6ff879054f234b78e7950294f8fbbe**: AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research/README, 508 and latest commit. LogMate read-only latest main **27f926aa6ea1e032dfa9affc598e8e41131eb092** (PR #22 roadmap reconciliation, docs only); inspected tool/pwa_precache.dart, tool/verify_pwa_artifact.dart, Makefile, web/flutter_bootstrap.js and firebase.json. Design Studio latest **534fadba3ebaeaa25fb53c075f9f60772c6da41c** and progress/WEB_STATUS.md: W121 Stage 3 PRACTICE, exact runtime/AT/human evidence OPEN. Marketing Manager STATUS (2026-10-24 13:35 KST) keeps LogMate launch pilot and advertising HOLD; Software Engineering Studio research/README records M006 bounded Chromium/macOS Safari transfer and D006 interruption, not actual LogMate release acceptance.

Priority comparison: **E highest** (release identity and custody; possible Acceptance publication); **A high dependency** (Worker/CacheStorage and first-claim client routing from 508); **C high execution pressure** (artifact/origin/device oracles); **B consumer** (truthful offline/update/recovery states, no unsupported 'ready'); **D challenger** (no promotion/measurement of an unverified install/Sync). E owns this reusable gate; A/C/B/D consume its outcomes without duplicating source/standards primers.

## 2. History → principle → current implementation [SOURCE / SYNTHESIS]

A release is not merely source code or a shell hash: build tools, post-build transforms, Worker generation, packaging, deployment selection and served bytes form a custody chain. CacheStorage may retain multiple Worker generations; Cache.put overwrites a matching entry, so an in-memory Worker lock is not cross-generation atomicity (508). A shell-derived appBuildId can stay unchanged when the generated Worker changes. A generic 'CI green' or an archive's digest alone cannot prove which bytes were served.

LogMate source-specific facts:
- tool/pwa_precache.dart enumerates shell, 724 font records and 148 font notices, calculates appBuildId from JSON-encoded shell records, and generates the Worker with embedded OFFLINE_MANIFEST.
- tool/verify_pwa_artifact.dart validates manifest-listed size/SHA-256, bootstrap/Worker string invariants and a DATA-001 marker in main.dart.js. It does not inventory every unlisted file, create a frozen full-tree receipt or authenticate later hosting.
- Existing CI research 508 observed NORMAL at build/web-normal, Acceptance at build/web, and firebase.json hosting.public = build/web. This is a **configuration mismatch hazard**, not evidence of actual deployment or exposure.
- Latest LogMate PR #22 modifies roadmap documents only. This does not constitute a new runtime or deploy PASS.

Authoritative primary sources checked 2026-10-24:
- Firebase Hosting config / public directory: https://firebase.google.com/docs/hosting/full-config
- GitHub upload-artifact digest, immutability, retention and path behavior: https://github.com/actions/upload-artifact
- GitHub artifact attestation and plan/visibility constraints: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- MDN Cache.put overwrite behavior: https://developer.mozilla.org/en-US/docs/Web/API/Cache/put
- W3C Service Worker lifecycle/clients: https://w3c.github.io/ServiceWorker/

## 3. Independent executable gate delivered [VALIDATION / Track E+C]

New standalone Python handoff:
- research/handoffs/pwa_release_custody_gate.py
- research/handoffs/test_pwa_release_custody_gate.py

The gate requires an explicit immutable-looking 40-character source SHA, NORMAL/Acceptance kind and an external receipt path. It:
1. inventories **all** files (including unlisted extras) with SHA-256/size, rejecting symlinks and nonfiles;
2. validates required entrypoints, manifest schema/API, 724 fonts, 148 notices, 144 OFL notices, safe URL-decoded paths, duplicate records and per-file digests;
3. independently recomputes shell-derived appBuildId and compares the Worker's embedded manifest with the deployed offline manifest;
4. checks bootstrap fontSetId and the DATA-001 marker polarity across text assets (NORMAL forbids it; Acceptance requires it in main.dart.js);
5. freezes a deterministic full-tree digest, independent Worker digest, manifest digest, source SHA and complete file inventory in an **external** JSON receipt; refuses to overwrite that receipt;
6. on verify, recomputes and compares the entire receipt; optionally rejects a Firebase Hosting public root that differs from the verified artifact root.

Example for a future Engineering-controlled, **already-built** NORMAL artifact:

    python3 research/handoffs/pwa_release_custody_gate.py freeze \
      --root build/web-normal --kind normal --source-sha <40-hex-exact-commit> \
      --receipt ../normal-release-receipt.json
    python3 research/handoffs/pwa_release_custody_gate.py verify \
      --root build/web-normal --kind normal --source-sha <same-commit> \
      --receipt ../normal-release-receipt.json --firebase-config firebase.json

With the currently observed firebase.json pointing to build/web, the second command should **HOLD** for a NORMAL build at build/web-normal. This is intentional; do not 'fix' it by silently selecting Acceptance output. Engineering must supply an explicit deployment config/root and independently inspect the exact publish input. The tool does not deploy.

**Execution actually performed:** Python 3 unittest on synthetic generated fixtures with 724 font and 148 notice records: **15/15 PASS**, including freeze/verify positive, Worker-only drift, unlisted file drift, marker leak/missing, manifest corruption/path traversal, file/root symlinks, receipt overwrite/location, Worker-manifest divergence, source SHA validation, and Firebase root mismatch/match. The positive fixture contained **880** files. This is a *test of the verifier*, not a test of LogMate's generated PWA. Syntax compilation passed. No Flutter build, actual NORMAL archive, Firebase publish, browser, Safari or managed-iPad run occurred.

## 4. Threat model, negative controls and limits [CONTRADICTION / OPEN]

| Incorrect inference | Falsifier / boundary |
| --- | --- |
| Shell appBuildId matches, so Worker matches | Worker-only edit changes Worker SHA/full-tree digest while appBuildId can stay the same. |
| Manifest listed assets verify, so release tree is identical | Unlisted extra/missing file changes the independent full-tree receipt. |
| A NORMAL verification means the Hosting root is NORMAL | Optional firebase.json public-path equality must be checked against the exact artifact root; source currently points to Acceptance output. |
| CI artifact upload digest means hosted bytes match | Upload digest identifies an artifact, not deployment selection or served origin bytes. |
| A matching JSON receipt proves an authorized release | Receipt is **not signed or independently trusted**; a malicious actor able to replace both receipt and artifact can forge consistency. |
| 15 synthetic tests PASS means product release PASS | Product build, archive download, hosted response, Worker runtime and managed iPad remain OPEN. |
| Disk bytes match, so browser CacheStorage/IDB data is durable | Different failure domains; process restart, storage pressure/eviction, backup/restore and Sync authority need separate oracles. |
| Firebase public directory equality means actual served bytes match | Firebase ignore rules, transforms, deploy permissions, preview channels, caching, rewrites, CDN and network fetch still require independent verification. |

Limitations of the current handoff: no signed attestation, GitHub source-tree lookup, source/toolchain verification, race-free filesystem snapshot, archive integrity, permission metadata, Firebase ignore-rule evaluation, deployed URL fetching, browser execution, rollback authorization or semantic 37-store restore. A caller-supplied source SHA is an assertion until matched against a trusted build run. A generated manifest that has been maliciously rewritten together with all assets before freeze can be internally consistent; approval must anchor the receipt to an independent CI/run identity. Tool output is intentionally named **DISK_ONLY_PASS**, never 'release PASS'.

## 5. Operational release custody protocol [MINTTAP DECISION / VALIDATION]

**Proposed protocol, not an approved LogMate patch:**
1. Build NORMAL and Acceptance in physically distinct directories with a fixed source SHA/toolchain and separate CI jobs or isolated workspaces. Assert marker polarity using the product verifier.
2. Freeze NORMAL with this independent gate. Preserve external receipt plus exact toolchain/CI run identity and artifact digest. Pin receipt in an independent approved release record; use attestation/signature where supported, checking GitHub plan and repository visibility first.
3. Upload/archive NORMAL explicitly with error-on-missing, verify after download/extraction using the same pinned receipt, and ensure no later job rewrites its directory. Acceptance remains non-deployable.
4. Use an explicit Firebase config whose public root equals that verified NORMAL directory. Verify the publish input after final staging and before deploy; fail closed on root drift, marker presence, file drift or missing approval.
5. Fetch independently from the deployed HTTPS origin: Worker, bootstrap, offline manifest, root navigation and selected critical assets. Record URL, status, content type, cache policy, bytes/SHA-256, time, deployment identity and route exclusions; do not confuse an auth rewrite with an offline shell.
6. Only then run exact-browser first-install/claim, old/new Worker overlap, offline cold start, real browser-process restart and data-preserving update; proceed to populated 37-store backup/restore and policy-matched managed iPad. Retain previous runnable shell and unique local data during rollback or recovery.

This separates **source equivalence → disk custody → archived custody → deploy-input custody → served-byte custody → browser execution → data/managed-device acceptance**. No level automatically promotes to the next.

## 6. Five-track transfer, decisions and next boundary [TRANSFER VALIDATION / DEPENDENCY]

- **E owner:** release-root correctness, independently anchored receipt, artifact provenance, deployment approvals, recovery/rollback/incident controls. No product release promotion.
- **A:** verify Worker embedded manifest/version semantics and browser cache/control behavior against exact Worker digest; old/new Worker coexistence remains unresolved.
- **C:** own CI invocation, negative controls, downloaded-archive and served-byte independent oracles; attach exact source/build/OS/browser/toolchain/run identity.
- **B:** only display 'offline ready' when this client is routable and relevant local data is preserved; distinguish release availability from offline readiness and remote Sync.
- **D:** launch/install/advertising claims and analytics funnels remain conditional on actual hosted and device evidence; avoid collecting flight records in telemetry.
- **Design Studio W121:** design/AT/human gates remain open; Web Manager does not replace UI specialist judgment.
- **Engineering D006/M006:** implement/execute project-specific CI, Flutter/Worker/IDB and device tests; bounded generic transfer is not product acceptance.
- **Marketing:** no unsupported seamless offline/Sync or PWA advertising claims.

**Current gate:** Stage 8 applied Security/Privacy/Trust ACTIVE, E highest bottleneck with A/C urgent. **Production validation OPEN / PWA release HOLD.** Adjacent high-value work completed here: source-to-artifact identity distinction, independent full-tree/Worker digest, normal-vs-acceptance marker polarity, manifest traversal/duplicate controls, Firebase root equality, synthetic positive/negative execution, release protocol and cross-track transfer. The next materially different checkpoint requires an actual generated NORMAL artifact and independent archive/host/browser evidence, not another model-only test. Product/Design Studio/Marketing/Engineering repositories were read-only.
