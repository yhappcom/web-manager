# 511 — Stage 8 PWA CI artifact transport, release-promotion authority and recovery gate

Date: 2026-10-24 (Asia/Seoul)  
Evidence status: **SOURCE / INTEGRATED SPECIFICATION; NOT PRODUCT EXECUTION**  
Owner: **Track E (Web Architecture, Security & Operations)**; Track A platform dependency, Track C independent oracle, B/D consumers.  
Canonical predecessor: [509](509_stage8_pwa_release_artifact_custody_disk_gate_and_deployment_handoff_20261024.md) disk receipt and [510](510_stage8_pwa_served_byte_custody_http_representation_and_release_evidence_20261024.md) served HTTP bytes. This study closes the *design of the missing transport/promotion stage*, not its execution.

## 1. Run-start provenance and allocation [SOURCE / DEPENDENCY]

Web Manager `main@c94126a965b6d00d454edfce3a0e3f5f37425a2b` was read with `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, 509–510 and recent commits. LogMate was read-only at latest observed `main@27f926aa6ea1e032dfa9affc598e8e41131eb092`: `.github/workflows/data001-pwa-artifact-validation.yml`, `data001-browser-persistence-validation.yml`, `core-product-validation.yml`, `Makefile`, `firebase.json`. Design Studio W121 and `progress/WEB_STATUS.md`, Engineering Q006/M006/D006 and Marketing Manager `STATUS.md` (2026-10-24 15:30 KST) were read as bounded transfers. No peer/product writes.

Current curriculum: general Stages 1–12 historically PASS as competency, **applied Stage 8 Security/Privacy/Trust ACTIVE**. Relative pressure: **E critical** (no independently approved NORMAL release archive/transport/promotion path); **C critical dependency** (false-green CI verdict and extraction/host evidence); **A high dependency** (Worker generation/cache/first-claim mechanics); **B moderate consumer** (truthful update/offline/restore state); **D moderate challenger** (no unproven installation/sync/ads claims). Work concentrated on E/C, not equal distribution. No new generic HTTP or security primer is needed.

## 2. History → mechanism → standards → implementation [SOURCE / SYNTHESIS]

A reproducible build and a green CI job are *not* a deployable release: intermediate packaging, artifact transport, receipt authorization, environment approval, selected Hosting root, actual served representation, browser runtime and user-data preservation are separate trust boundaries. Immutable workflow artifacts prevent mutation *of that uploaded artifact object* but do not prove which directory was uploaded, whether the correct run was downloaded, whether the archive extraction reproduced all expected paths, whether a publisher chose the NORMAL directory, or whether an origin serves it.

Authoritative current sources checked 2026-10-24:
- GitHub official artifact tutorial: https://docs.github.com/en/actions/tutorials/store-and-share-data — upload emits SHA-256 artifact digest; download checks it; **historical 2025 warning-only behavior is version-scoped; see §9 for the official 2026 `download-artifact@v8` default `digest-mismatch: error` correction**.
- GitHub March 18 2025 changelog: https://github.blog/changelog/2025-03-18-github-actions-now-supports-a-digest-for-validating-your-artifacts-at-runtime/ — explicitly says a mismatch does **not** fail the workflow; do not silently rely on automatic step success.
- GitHub upload-artifact official README: https://github.com/actions/upload-artifact — v4 artifacts immutable; upload may omit hidden files by default; archive transport and extracted file tree are distinct; retention and deletion are lifecycle limits.
- GitHub attest official docs: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations and https://github.com/actions/attest — provenance needs verified workflow identity/subject; public repo generally eligible, private/internal depends on plan. **A signed attestation is not release approval or served-byte proof.**
- Firebase Hosting config: https://firebase.google.com/docs/hosting/full-config — `public` selects deployed directory; reserved paths, redirects, exact static, rewrites and 404 follow documented precedence; `ignore` can change uploaded tree.
- Firebase CLI: https://firebase.google.com/docs/cli — `firebase deploy --only hosting` narrows service scope; hooks and deploy target/configuration remain operator-specific. No deployment was initiated.
- Engineering Q006 canonical: `yhappcom/software-engineering-studio/research/quality/Q006_ci_pipeline_exit_status_oracle_integrity.md` — output/log preservation does not guarantee producer exit propagation; reusable-workflow/matrix outputs require explicit semantic reduction.

### Exact LogMate source observations

`data001-pwa-artifact-validation.yml` builds NORMAL with `BUILD_WEB_OUTPUT=build/web-normal make build-pwa`, then builds Acceptance with `make build-pwa-acceptance` to default `build/web`. The **only successful artifact upload** is `logmate-efb-pwa-acceptance-${{ github.sha }}` with `path: build/web`; failed diagnostic upload also points to `build/web`. NORMAL is verified in its build job but **not uploaded or frozen for independent downstream promotion**. Comment explicitly forbids Acceptance production promotion. `firebase.json` currently sets Hosting `public: build/web` and global `Cache-Control: no-cache, no-store, must-revalidate`; auth-specific rewrites are present. A normal `firebase deploy` from this checked-in configuration would therefore select the Acceptance-default directory **if it existed at deploy time**; there is **no evidence that this deploy occurred**. Browser persistence workflow push filter is only `feature/data001-domain`; PWA workflow push filter excludes `main`; Core workflow is dispatch-only. Exact current-head automatic release certification is not established. These are workflow-source observations, not production incident claims.

### Important correction / contradiction

`upload-artifact` digest identifies the **uploaded archive object**, while 509's full-tree receipt identifies **logical extracted files**, and 510's HTTP gate identifies **served representations**. The three SHA-256 values need not be numerically equal. Matching an archive digest does not imply a safe extraction, correct release type, trusted source run or host equality. Conversely, a correctly extracted tree can have a different ZIP digest because ZIP metadata/compression differ. Do not equate or substitute these digests.

## 3. Release evidence state machine [MINTTAP DECISION CANDIDATE]

The following is a proposed Web Manager acceptance contract, **not an approved LogMate deployment policy**:

| Gate | Evidence required | Allowed conclusion | Forbidden promotion |
| --- | --- | --- | --- |
| G0 SOURCE | exact 40-hex commit, branch/ref, workflow SHA, toolchain, dependency lock, expected NORMAL kind | reproducible identity inputs known | not 'built' |
| G1 DISK | 509 full-tree receipt, independent Worker SHA, marker polarity, exact NORMAL root, external pinned receipt | `DISK_ONLY_PASS` | not 'archived' |
| G2 ARCHIVE | unique immutable artifact ID, run ID/attempt, upload archive digest, successful download, safe extraction, **re-run 509 verification against independent receipt** | `ARCHIVE_RESTORED_MATCH` | not 'approved' or 'hosted' |
| G3 AUTHORITY | authorized release decision tied to exact source+receipt+artifact ID and intended Firebase project/site/channel; independent signer/approval identity and non-replay window | `PROMOTION_AUTHORIZED` for specific target | not 'deployed' |
| G4 HOST | selected Hosting public root verified as NORMAL, deploy result identity, 510 critical+all-tree served-byte and header/route negative controls | `HOST_BYTES_MATCH` at measured origin/time | not 'offline ready' |
| G5 RUNTIME | exact browser Worker install/claim/update/overlap, cold offline, process restart, populated 37-store semantic restore/R03–R04, policy-matched physical iPad | bounded device/product PASS only for exercised cohorts | not universal fleet/sync/backup guarantee |

All transitions fail closed on `UNKNOWN`, `MISMATCH`, absent evidence, mismatched target, changed source/ref, changed Worker, expired artifact or missing approval. **No automatic deployment** from a successful test. Approval must name the exact immutable artifact, not just a mutable branch name. G3 and G4 are independent: a correct approved artifact can be served incorrectly, and exact served bytes can be unauthorized.

## 4. Archive and promotion falsifiers [VALIDATION / CONTRADICTION]

The Engineering handoff should implement the following as independently observed positive and negative controls; these are **specified, NOT_EXECUTED** here.

| ID | Fault / control | Required verdict |
| --- | --- | --- |
| T01 | NORMAL archive downloaded from pinned run/artifact ID; full-tree receipt independently matches | G2 candidate PASS |
| T02 | Acceptance archive has same source SHA but wrong kind | HOLD |
| T03 | Artifact name matches, but ID or run attempt differs | HOLD |
| T04 | Download action reports digest mismatch warning yet step exits zero | explicit HOLD; never use step success alone |
| T05 | ZIP digest matches but an extracted file differs from 509 receipt | HOLD |
| T06 | Same files but omitted hidden file / ignore pattern differs | full-tree HOLD or explicit approved exclusion manifest |
| T07 | ZIP has `../`, absolute path, backslash normalization ambiguity, duplicate normalized path or case-fold collision | reject before extraction |
| T08 | ZIP symlink/hardlink/device entry, unexpected permission semantics | reject or approved safe canonicalization |
| T09 | Oversized expansion, extreme compression ratio, too many entries, excessive total bytes | bounded extraction reject |
| T10 | Archive contains unexpected extra or missing file | HOLD |
| T11 | Receipt and archive both altered together; independent receipt pin unchanged | HOLD |
| T12 | Receipt and independently pinned digest both replaced by same actor | **cannot certify**; separate approval trust domain required |
| T13 | Correct archive, `firebase.json` still selects `build/web` | HOLD for NORMAL |
| T14 | Correct archive, explicit NORMAL staging path, but `ignore` removes an expected file | G4 HOLD |
| T15 | Correct archive, `/auth` route rewrite regresses to shell or missing file | route negative control HOLD |
| T16 | Host serves 200 HTML for JS due to rewrite or stale CDN | G4 HOLD |
| T17 | Same shell/appBuildId, changed Worker bytes | independent Worker digest HOLD |
| T18 | Upload+download both green, but required semantic test failed inside a logged pipeline | Q006 semantic HOLD |
| T19 | Approved production project/site differs from actual Firebase target/channel | HOLD |
| T20 | Artifact expired/deleted, only release summary remains | archive custody OPEN, not reconstructable PASS |
| T21 | Release rollback restores old shell while schema/data advanced | preserve unique ledger; compatibility/recovery gate before reactivation |
| T22 | Two workers share catalogue and initial claimed client has no build mapping | 508 W01–W28 browser OPEN, not host/transport PASS |
| T23 | Browser offline cold-start succeeds but IndexedDB restore fails | product data gate HOLD |
| T24 | Chrome PASS but managed MDM Web Clip differs from user-installed Home Screen context | iPad-specific gate OPEN |

**Threat boundaries:** accidental wrong artifact, compromised build runner, malicious source, mutable branch ref, approval replay, wrong Firebase project, stale CDN, archive extraction attacks, unsafe emergency rollback, and organizational loss. A hash detects change only when the expected hash and its approval authority are independently trustworthy. Archive retention is not an independent durable user-data backup.

## 5. Engineering-owned CI implementation contract [DEPENDENCY / VALIDATION]

This is a **design-level handoff**, not a copy-paste deployed workflow. The existing PWA workflow must not silently become a deploy workflow. Suggested order:

1. Keep NORMAL and Acceptance jobs/artifacts physically separate. Build NORMAL with pinned source/Flutter and a clean output root; run product verifier; run 509 freeze and independently pin its receipt in a controlled release record. Record exact run/attempt and action SHAs. Acceptance is explicitly non-deployable.
2. Upload **NORMAL** under a kind-specific name with `if-no-files-found: error`; preserve artifact ID, URL and archive digest. Upload receipt separately, without treating its co-location as independent approval. Retention policy and external long-term custody must be explicit.
3. In an isolated downstream verification job, download by exact **artifact ID and run**, not a mutable latest/name guess. Capture GitHub's digest warning as **non-authoritative** and enforce a separate fatal archive/tree verification. Before extracting an untrusted ZIP, apply T07–T09; after extraction, re-run 509 against independently pinned receipt and compare expected source/Worker/manifest and full file inventory.
4. Require an explicit human/release-controller authorization naming source SHA, artifact ID, receipt digest, target Firebase project/site/channel, approval generation, allowed window and rollback predecessor. Enforce GitHub environment controls if actually configured/available; verify repo plan, required-reviewer rules and self-review settings rather than assuming them.
5. Stage the **verified NORMAL** tree into a deployment-only directory and use an explicitly reviewed Firebase Hosting configuration whose `public` equals it. Preserve and review auth rewrites, headers and ignore rules. Never deploy the checked-in `build/web` by default after the Acceptance job. Restrict deployment identity to the intended target and Hosting-only scope. Use least-privilege credentials/OIDC where supported; do not introduce secrets into artifacts.
6. Re-check full-tree receipt **after final staging**, then deploy only on authorized execution. Record release ID, target and CLI/config digest. Independently fetch the exact origin with 510 critical and all-tree oracles (including auth route and missing static negative controls), with separate region/cache variants when required.
7. Execute 508 Worker W01–W28, 506 restore R01–R12, 507 iPad I01–I16 on exact product/runtime populations before any production-readiness promotion. A failed later gate must not retroactively turn an earlier G1/G2 success into G5 PASS.

**CI false-green guard:** an exit-zero download step with a digest warning is **not** a release verdict. A downstream step must explicitly compare the independently trusted receipt with the extracted tree and exit nonzero on any mismatch. Any pipeline, matrix, reusable-workflow output or `continue-on-error` must be assessed against Engineering Q006; the aggregated semantic verdict must control the final job status. Diagnostic artifact upload may use `if: failure()`/equivalent but must not mask the primary failure.

**No production change made:** no workflow, Firebase config, LogMate source, secrets, deployment, GitHub environment or marketing release status was modified in this study.

## 6. Incident and rollback judgment [SYNTHESIS / MINTTAP DECISION CANDIDATE]

If G4 fails after a deploy, quarantine promotion and preserve the exact bad/good archive receipts, deploy ID, observed served bytes, cache headers and affected client cohort. Reverting Hosting to a previously served shell may not revert IndexedDB schema, local record lineage or Worker control. Do not delete CacheStorage/IndexedDB as a generic recovery action, force `skipWaiting`/claim to hide mismatches, or label data loss 'fixed' because the landing page renders. Define rollback compatibility against the latest local data schema and old/new Worker clients; require user-visible backup/recovery state when uncertainty remains. Incident response should avoid leaking flight records into telemetry and preserve forensic hashes, not raw private ledgers.

For managed EFB iPad, distinguish Safari tab, user Home Screen Web App, MDM Web Clip and full-screen Web Clip. None inherits another population's PASS; installation icon, storage persistence, background Sync, hotspot use and automatic cross-device transport remain independent OPEN questions.

## 7. Cross-track transfer and source freshness [TRANSFER VALIDATION / CHANGE WATCH]

- **E canonical owner:** exact NORMAL release identity, approval authority, target isolation, artifact lifecycle, incident/rollback and recovery.
- **A supplier:** Service Worker first-claim and multi-generation catalogue behavior (508), origin/HTTP cache semantics; a correct archive cannot prove controlled client readiness.
- **C supplier:** T01–T24 fail-closed tests, archive extraction oracle, hosted-response and physical-device evidence, and Engineering Q006 semantic verdict propagation. W121 warns against further pre-runtime UI manifests when execution is the blocker.
- **B consumer:** separate UI states for download available, installed, current client routable, offline content cached, local ledger saved, independently backed up and remote Sync ACK. No automatic 'Offline ready' claim based on G1–G4.
- **D consumer:** do not count installation/activation/sync or advertise seamless offline EFB behavior until G5 evidence; analytics must avoid pilot/flight payloads. Marketing Manager's LogMate pilot/ads remain HOLD, not overridden by this web release research.
- **Engineering boundary:** Engineering owns concrete workflow patch, archive verifier implementation, Firebase Emulator/real host, Dart/Flutter/Chrome and device execution; Web Manager supplies acceptance and falsifiers, not another generic CI discipline.
- **CHANGE WATCH:** GitHub artifact action versions/digest behavior, artifact retention/visibility/attestation eligibility, Firebase CLI/Hosting config/ignore precedence, WebKit/iPadOS/MDM install/storage policy, deployment approval entitlements.

## 8. Meaningful checkpoint / next context boundary [OPEN]

**Established from current source:** NORMAL is built/verified but not archived; Acceptance is the only success artifact; default Hosting public root selects `build/web`; main-branch automatic PWA/browser execution coverage is incomplete; GitHub artifact download digest mismatch currently warns rather than guaranteeing fatal job status. **Not established:** an actual misdeployment, compromised archive, executed transport test, approved NORMAL receipt, real hosted LogMate origin, real Worker overlap, 37-store browser restore, managed-iPad result or production incident.

Next evidence must be Engineering-controlled **G1→G2 exact NORMAL archive round trip with T01–T12 and fatal semantic verdict**, then G3 authorized deploy-input/target evidence and G4 actual hosted bytes. G5 Worker/restore/iPad is independently required. If no exact artifact and approved target exist, stop model expansion and request runtime evidence rather than manufacture synthetic PASS.

**End-of-run adjacent-value check:** 509 left archive custody unverified; 510 established hosted-byte oracle but not the missing intermediate authority/transport step. This run reconciled GitHub's non-fatal digest warning, actual LogMate CI and Firebase roots, 24 falsifiers, approval authority, rollback and cross-track handoff. The next useful step requires new Engineering artifact/runtime evidence or an implementation-owner change; another static restatement cannot promote the gate.


## 9. 2026-10-24 integrated G1→G2 implementation handoff and GitHub action-version correction [SOURCE / CONTRADICTION / VALIDATION]

**Canonical refresh:** Web Manager pre-run `main@94a3a5135c7d3c7f975557f22cde21ca9cdb37b5`; required governance/roadmap/status/index, 509–512 and recent commits read. LogMate read-only `main@27f926aa6ea1e032dfa9affc598e8e41131eb092`, exact PWA workflow, Makefile and firebase.json rechecked. Design Studio `progress/WEB_STATUS.md` W121 Stage 3 PRACTICE/runtime OPEN; Engineering Q006 hosted Bash verdict propagation; Marketing Manager LogMate offline/ads/launch HOLD consumed as bounded transfers. No product/peer modification.

### 9.1 Version-sensitive correction, not a timeless warning rule [SOURCE / CHANGE WATCH / CONTRADICTION]

Prior §2 and studies 511–512 correctly describe **GitHub's 2025-03-18 documented warning-only artifact digest mismatch behavior**, but that statement must now be **version scoped**. The official `actions/download-artifact` `v4/action.yml` has no `digest-mismatch` input, while the official **`v8/action.yml` explicitly exposes `digest-mismatch: error` as the default**, with `ignore|info|warn|error` alternatives. Current `v8` README documents `artifact-ids`, `skip-decompress`, and non-ZIP support; `upload-artifact@v7` documents `archive:false`. Source inspected 2026-10-24:
- https://github.com/actions/download-artifact/blob/v4/action.yml
- https://github.com/actions/download-artifact/blob/v8/action.yml
- https://github.com/actions/download-artifact/blob/main/README.md
- https://github.com/actions/upload-artifact/blob/v4/action.yml
- https://github.com/actions/upload-artifact/blob/v7/action.yml
- https://github.blog/changelog/2025-03-18-github-actions-now-supports-a-digest-for-validating-your-artifacts-at-runtime/

**Operational rule:** a generic claim that *every* GitHub artifact download digest mismatch is warning-only is now incorrect. For v8 default `error`, the action is documented to fail on digest mismatch. This does **not** establish an independent expected digest, semantic file-tree equivalence, release authority, or served-byte proof. A workflow that explicitly sets `digest-mismatch: warn` also cannot use step success as a release verdict. Pin the action SHA/version and verify actual runner behavior; do not extrapolate v8 semantics backwards to v4 or forwards indefinitely.

| Transport | Artifact referent | Native behavior / risk | Web Manager rule |
| --- | --- | --- | --- |
| upload-artifact@v4 + download-artifact@v4 | GitHub-created ZIP wrapper | Historical warning-only digest behavior; normal download unwraps files | Separate fatal inner ZIP + receipt + 509 semantic gate |
| upload-artifact@v7 `archive:false` + download-artifact@v8 | Single raw artifact | Format differs; v8 supports non-ZIP; digest mismatch default `error` | 512 ZIP-only verifier rejects raw input until separately validated |
| upload-artifact@v4 ZIP wrapper containing explicit `normal.zip` file | Wrapper ZIP plus **independent inner NORMAL ZIP** | Wrapper digest and inner ZIP SHA need not match; v4 extracts inner file | Pin and audit inner ZIP; preserve wrapper artifact ID/digest as distinct metadata |
| download-artifact@v8 with `digest-mismatch: error` | Action-managed downloaded artifact | Fatal action mismatch is useful but insufficient for G2/G3 | Still run 512 and 509 against independently trusted release receipt |

### 9.2 Substantive CI handoff [MINTTAP DECISION CANDIDATE / DEPENDENCY]

New non-deploying, **170-line** Engineering proposal: [`handoffs/pwa_normal_release_ci_PROPOSAL.yml`](handoffs/pwa_normal_release_ci_PROPOSAL.yml). It is **not installed under LogMate `.github/workflows`**, is **not executable there without Engineering integration**, and never deploys.

1. `normal-build` uses exact `github.sha`, Flutter 3.47.5/Dart SDK check, approved Stage C font hash, lockfile and Dart formatting gates, then `BUILD_WEB_OUTPUT=build/web-normal make build-pwa`. It does **not** build Acceptance. This preserves the actual product's NORMAL build command rather than inventing a different Flutter pipeline.
2. Run 509 `freeze` to produce the external-to-tree receipt; package the **entire receipt inventory including dotfiles** as one explicit stored `normal.zip`. ZIP members have fixed timestamps and ordinary-file modes. Run 512's inner ZIP byte oracle before upload. Record `sourceSha`, inner ZIP SHA, receipt SHA and separate GitHub wrapper artifact IDs/digests.
3. Upload inner ZIP and receipt as **two v4 artifacts**, each with `if-no-files-found: error`; artifact names bind `run_id/run_attempt`. A new `normal-roundtrip` job downloads **by artifact ID**, not mutable name or latest successful run.
4. Enforce independent fatal `sha256sum --check` on the *inner* ZIP and receipt using build-job outputs, then 512 ZIP/receipt/source/full-tree validation; safely stage archive members; check ZIP hash again; re-run 509 `verify` on the staged NORMAL tree. Bash uses `set -euo pipefail` so the semantic failure cannot be hidden by logging, consistent with Engineering Q006.
5. Explicit result is **`G2_PRODUCER_SCOPED_TRANSPORT_AND_SEMANTIC_MATCH`**. Both pins originate from the build job, so this is **producer-scoped round-trip evidence only**, not independent approval or adversarial builder compromise protection. GitHub wrapper digests are recorded separately and not equated with inner ZIP or logical tree hashes.
6. No `firebase deploy`, no Hosting target, no privileged token, no production secret, no G3 approval, no G4 served-byte or G5 runtime claims. Production integration requires Engineering review of action SHAs, runner support, file modes, archive size, CI execution and product-specific requirements.

**Evidence / limitations:** The exact YAML was parsed with PyYAML, passed **11/11 static structural assertions**, and its embedded package/staging Python snippets completed a synthetic **880-file ZIP round trip** with byte-for-byte restored-file checks. The isolated snippet test used a *stub* `safe_path` import, **not execution of the actual 512 oracle or 509 semantic verifier**; the historical separate 509/512 synthetic suites are 19/19 and 28/28. The exact proposed YAML was committed and independently checked against the locally executed file's Git blob `92f2fd5a28ee1350b2f7ce5326161da3d8f4b668`. **GitHub-hosted Actions, real LogMate NORMAL build, actual artifact upload/download, 509+512 end-to-end execution, independent receipt pin, real Chrome, hosted origin and managed iPad were NOT_EXECUTED.**

### 9.3 Cross-boundary negative/positive campaign [VALIDATION / TRANSFER VALIDATION]

| ID | Scenario | Expected evidence / verdict |
| --- | --- | --- |
| U01 | Real NORMAL build; 509 freeze; inner ZIP contains all 880+ expected entries and any extra unlisted assets | G1 candidate; 512 exact full inventory; no Acceptance marker |
| U02 | Acceptance main.dart.js or wrong `kind` enters NORMAL packaging | fatal HOLD at 509/512 |
| U03 | Hidden resource omitted by upload globs | fatal HOLD; inner ZIP packaging must preserve it |
| U04 | Correct wrapper digest, changed inner ZIP file | fatal 512/509 HOLD |
| U05 | Inner ZIP digest correct but receipt source SHA, worker or manifest differs | fatal 512/509 HOLD |
| U06 | Artifact name matches but immutable artifact ID/run/attempt differs | reject promotion context; ID and run must be bound by Engineering |
| U07 | Download action exits zero despite warning; semantic oracle returns nonzero | final job nonzero; Q006 transfer |
| U08 | ZIP extraction path/symlink/case collision or modified ZIP during staging | reject before 509; preserve evidence, no deployment |
| U09 | Archive and receipt modified together and build-job output pins replaced | **producer-scoped comparison cannot detect same-authority compromise**; G3 independent authority OPEN |
| U10 | GitHub v8 default `error` vs explicit `warn` negative controls | verify actual action-version behavior; do not infer v4 from v8 |
| U11 | NORMAL archive G2 passes while Firebase `public=build/web` still selects Acceptance root | G3/G4 HOLD; no deployment |
| U12 | G2 passes but Worker first claim, 37-store restore or MDM iPad fails | G5 HOLD; local data preservation and truthful UX required |

**Cross-track allocation:** E owns producer/approval separation, target custody and rollback; C owns U01–U12 fatal oracles, provenance and Q006 transfer; A supplies v4/v8 archive behavior and Worker/runtime boundaries; B consumes separate local saved/offline/update/backup/remote-ACK states (Design Studio owns visual system); D must not advertise EFB offline/sync or count installed PWA without G5. Engineering owns any actual workflow patch, runner execution and release authority.

### 9.4 Stop boundary and next high-information-gain proof [OPEN]

This cycle resolves a genuine adjacent dependency: the previously independent 509 disk and 512 ZIP oracles now have a concrete non-deploying two-job NORMAL round-trip integration proposal, while action-version digest behavior is corrected. **Next evidence is an Engineering-owned actual NORMAL G1→G2 run with exact artifact IDs, independent 509/512 and source SHA; then an out-of-band trusted G3 release approval and G4 host comparison, followed by 508 Worker, 506 restore and 507 managed-iPad G5.** The proposal is not a production workflow and is not approval to deploy. Stage 8 applied Security/Privacy/Trust remains ACTIVE; Production validation OPEN; PWA release HOLD.
