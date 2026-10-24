# 512 — Stage 8 PWA NORMAL ZIP archive transport oracle, falsifiers, and GitHub artifact format drift

Date: 2026-10-24 (Asia/Seoul). **Applied Stage 8 Security / Privacy / Trust — ACTIVE.** Primary owner **E Web Architecture/Security/Operations**; C independent validation and A archive/platform dependency; B/D downstream consumers. **SOURCE / SYNTHESIS / BOUNDED EXECUTABLE VALIDATION**, not production certification. This is a substantive implementation of part of [511](511_stage8_pwa_ci_artifact_transport_promotion_authority_and_recovery_gate_20261024.md), extending [509](509_stage8_pwa_release_artifact_custody_disk_gate_and_deployment_handoff_20261024.md) and [510](510_stage8_pwa_served_byte_custody_http_representation_and_release_evidence_20261024.md).

## 1. Canonical refresh, specialist pressure and provenance [SOURCE / DEPENDENCY]

At run start Web Manager latest main was ecaeb7f7079fc96e0bdb47233b3590a3bc90fbe8; read AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md, relevant 509–511, recent commits. Read-only product LogMate main was 27f926aa6ea1e032dfa9affc598e8e41131eb092, including the exact .github/workflows/data001-pwa-artifact-validation.yml. Design Studio progress/WEB_STATUS.md W121 remains Stage 3 PRACTICE with runtime/AT/human OPEN. Software Engineering Studio Q006 independently proves log-preserving pipelines can mask a failed primary oracle unless the verdict propagates. Marketing Manager STATUS.md (2026-10-24 16:31 KST) keeps LogMate-specific production/marketing evidence conditional; no marketing promotion is implied.

Five-track assessment: **E critical** because a correctly built NORMAL tree is not yet independently transported or authorized; **C critical transfer** because T01–T12 need a real fatal byte oracle; **A high** because ZIP/archive transport is not Service Worker cache or browser storage; **B moderate** because 'downloaded' must not become 'offline ready'; **D moderate** because release/installation claims cannot be inferred from artifact evidence. Primary effort E+C with A mechanics; B/D consume the distinctions. Generic Stage 1–12 competency PASS does not close applied Stage 8 product gates.

## 2. Historical failure → principle → current official behavior [SOURCE / SYNTHESIS / CHANGE WATCH]

Artifact download is not a release trust boundary by itself. GitHub's 2025-03-18 changelog explicitly says an artifact digest mismatch produces a **warning** and does not fail the workflow; its current official tutorial still describes the warning behavior. A zero-exit download therefore cannot be treated as a fail-closed G2 verdict.

Official sources checked 2026-10-24:
- GitHub 2025-03-18 artifact digest announcement: https://github.blog/changelog/2025-03-18-github-actions-now-supports-a-digest-for-validating-your-artifacts-at-runtime/
- GitHub current artifact upload action: https://github.com/actions/upload-artifact — artifact-id, artifact-url, artifact-digest, archive/hidden-file settings, retention and permission semantics.
- GitHub current artifact tutorial: https://docs.github.com/en/actions/tutorials/store-and-share-data
- **GitHub 2026-02-26 format change:** https://github.blog/changelog/2026-02-26-github-actions-now-supports-uploading-and-downloading-non-zipped-artifacts/ — v7 upload with archive:false and compatible v8 download permit a non-ZIP artifact; older uploads and normal archive:true remain ZIP. **Do not assume every future artifact is a ZIP.** The new verifier deliberately accepts **ZIP only** and fails for non-ZIP, requiring a separately specified transport verifier if Engineering selects archive:false.
- Python standard library ZIP model: https://docs.python.org/3/library/zipfile.html — member metadata, CRC/ZIP reader and extraction safety considerations.

Current product source: NORMAL builds to build/web-normal and is verified in the PWA workflow, but the success artifact upload names/contains Acceptance build/web. Default firebase.json Hosting public remains build/web. No NORMAL archive has been supplied and no deploy is evidenced. The new tool is a **research/handoff**, not a product workflow modification.

**Trust distinction:** (a) uploaded ZIP SHA, (b) external schema-1 receipt SHA, (c) receipt's canonical logical full-tree SHA, (d) Worker SHA, (e) HTTPS response SHA identify different objects. None is a substitute for organizational source/run/artifact approval. The tool consumes an independently pinned ZIP digest and receipt digest, but cannot independently prove who pinned them.

## 3. Implemented ZIP oracle [VALIDATION]

New read-only tool: [research/handoffs/pwa_archive_transport_gate.py](handoffs/pwa_archive_transport_gate.py). Tests: [research/handoffs/test_pwa_archive_transport_gate.py](handoffs/test_pwa_archive_transport_gate.py).

The tool requires an exact ZIP path, schema-1 NORMAL receipt, **independent ZIP SHA-256 pin**, **independent receipt SHA-256 pin**, and exact source commit SHA. It:
1. Rejects symlink inputs, invalid pins, Acceptance receipts, wrong source SHA, invalid receipt inventory/Worker/manifest/tree hashes and missing critical release files.
2. Rejects absolute/drive/parent/backslash/percent-encoded/Unicode non-NFC/control-character/trailing-dot-or-space paths, duplicate and casefold-colliding names, file-as-parent conflicts, symlink/special ZIP entries, encrypted or unsupported compression, unexpected or missing files.
3. Bounds archive/receipt size, file count, individual and cumulative decompressed bytes, and compression ratio. It **does not extract** ZIP entries; streams each member to SHA-256 while ZIP CRC checks remain active.
4. Requires the exact ZIP file inventory, byte counts and hashes to equal the external 509 receipt, including hidden paths if present. It checks independent Worker and manifest digests against the receipt.
5. Returns only **ARCHIVE_BYTES_MATCH_UNVERIFIED** (or exits nonzero with HOLD), never a release, deployment, browser, backup, or product PASS.

**Local executable evidence (2026-10-24):** Python 3.13 standard-library unittest **28/28 PASS** plus syntax compilation PASS. Tests include NORMAL positive, hidden-file preservation, wrong pins/source, Acceptance rejection, modified/missing/extra file, duplicate/casefold/parent-path collisions, traversal/absolute/backslash/encoded traversal/Unicode normalization, symlink, high expansion ratio, malformed tree/Worker/size/required entries, directory entry, oversized receipt, non-ZIP and invalid pin. Exact committed Python blob SHA **7073e6959eaeeb0814f23b2b23e6648ae6e61307** and test blob SHA **66ae6b8c1fa17d5e2ab50da9389d1d7603e75374** were independently matched to the local executed files. **This is a synthetic archive-oracle test, not a real LogMate 880-file archive test, GitHub Actions execution, or G2 product PASS.**

Example for an Engineering-controlled **ZIP** artifact only (the pins must be sourced from independently trusted release/run records, not read from the same untrusted archive):

~~~sh
python3 research/handoffs/pwa_archive_transport_gate.py \
  --archive <downloaded-normal-archive.zip> \
  --archive-sha256 <independent-archive-64hex> \
  --receipt <normal-receipt.json> \
  --receipt-sha256 <independent-receipt-64hex> \
  --source-sha <exact-40hex-source> \
  --out <archive-evidence.json>
~~~

The result is deliberately **not** G2 closure by itself. Engineering must also re-run 509's semantic disk verification on an independently extracted/staged tree, tie artifact ID/run ID/attempt to a trusted release record, and preserve the final nonzero semantic verdict through all CI logging and matrix aggregation (Q006). The 509 tool checks Worker embedded manifest, 724 fonts/148 notices, marker polarity and Firebase root; the ZIP tool only checks that archive bytes equal the **pinned** receipt.

## 4. Failure-mode reasoning and adversarial interpretation [CONTRADICTION / MINTTAP DECISION CANDIDATE]

| Tempting inference | Correct boundary |
| --- | --- |
| Download action succeeded, so archive is safe | Warning-only digest behavior; independent fatal check required. |
| Archive ZIP digest matches, so all files are correct | Digest of the *approved* archive must be trusted, and full-tree receipt independently checked. |
| Full-tree ZIP check proves 509 semantic validation | No: an internally consistent but malicious/invalid receipt can be pinned; rerun 509 and verify approval provenance. |
| Same source SHA means NORMAL | Source SHA is not build-flag polarity; explicit receipt kind and 509 marker check required. |
| Hidden file missing is harmless | Hidden-file exclusion is action-dependent; exact receipt mismatch must HOLD unless approved exclusion is explicit. |
| ZIP reader can safely extract arbitrary members | This tool never extracts; a separate staging extractor must independently enforce safe paths/modes and reverify output. |
| Valid archive means authorized deploy | G3 approval binds source, artifact ID, run/attempt, receipt pin, target project/site/channel and validity window. |
| Valid archive means safe rollback | Worker/client/schema/data lineage may have advanced; unique local data cannot be deleted for a green shell. |
| ZIP tool supports future non-ZIP artifact upload | It intentionally does not; v7 archive:false is a CHANGE WATCH and requires a different verifier. |
| All local tests pass, so managed iPad is ready | Browser lifecycle, 37-store restore, storage pressure, MDM Web Clip and physical iPad are separate OPEN gates. |

**Limitations:** ZIP size/ratio limits are a conservative project research policy and can reject legitimate unusually compressible assets; any adjustment requires measured artifact evidence, not an unreviewed bypass. The tool does not parse every ZIP extra field or attest action-run identity, inspect signed provenance, check zip-to-filesystem extraction, guarantee TOCTOU-free immutable inputs, establish release authorization, run 509 semantic checks, deploy, probe Hosting or execute browser/MDM. It currently rejects literal percent characters in ZIP filenames as ambiguous; this may require an explicit policy if real NORMAL assets use such names. ZIP casefold rejection is intentionally stricter than case-sensitive Linux. Source SHA CLI input is an assertion without independent CI provenance.

**Proposed decision, not approved product policy:** Keep NORMAL/Acceptance physically separate; freeze and externally pin the 509 receipt, upload NORMAL as its own immutable archive with exact artifact ID/run/attempt, verify downloaded ZIP with this fatal oracle, safely stage and rerun 509, require G3 target-specific authorization, then execute 510 hosted-byte and G5 Worker/37-store/iPad gates. Never promote a successful G2 byte check into G3–G5 automatically.

## 5. Transfer, operational judgment, next major boundary [TRANSFER VALIDATION / DEPENDENCY / OPEN]

- **E owner:** source/artifact/receipt pin independence, run ID/attempt and target approval, archival retention, non-ZIP format policy, recovery/rollback; approval cannot be delegated to the archive itself.
- **C validator:** 28 synthetic adversarial controls, exact blob identity and fatal exit; Engineering Q006 owns workflow-level verdict propagation, artifact acquisition and real product execution.
- **A supplier:** ZIP transport bytes differ from CacheStorage, Worker version and browser-controlled navigation; W01–W28 remain unexecuted in real browser.
- **B consumer:** UI must not label G2 archive match as offline ready, restored, synchronized or backed up; Design Studio W121 runtime/human/AT evidence remains OPEN.
- **D challenger:** install/acquisition/ad metrics and PWA continuity claims must not treat archive custody as an installed active user; avoid flight-data telemetry and preserve Marketing's HOLD.
- **CHANGE WATCH:** GitHub upload v7 archive:false / download v8, action versions and artifact retention, GitHub digest warning behavior, Firebase deployment input, WebKit/MDM policies.

**Adjacent-value check:** The 511 specification's highest-value missing executable dependency was a fail-closed G2 archive-byte oracle; implemented, adversarially tested and checked against committed blobs. Also resolved the new non-ZIP artifact-format contradiction from 2026 official GitHub documentation. Further promotion requires a **real NORMAL archive, independent approved pins and exact GitHub run/artifact metadata**, plus separate 509 post-staging, 510 HTTPS, 508 Worker, 506 37-store/R03–R04 and 507 managed-iPad execution. **Applied Stage 8 ACTIVE; Production validation OPEN; PWA release HOLD.** Product/peer repositories remain read-only.
