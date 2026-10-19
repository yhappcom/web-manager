# 420 — Stage 8 PWA Repair Completeness, Deep-Status Cost and Safe Recovery Gate

**Checkpoint:** 2026-10-20 (Asia/Seoul). **Canonical start:** Web Manager `main@69e240a94dd6763bd31adfea17bed430d66b92b5`; **product read-only:** LogMate `main@6101666530cb706a042ac82614c840af441895b1`; Design Studio `main@f03d251c`; Software Engineering `main@20aa7c58`; Marketing `main@b25ee576`. **Primary owner E; A/C critical dependencies, B/D transfer.** **Gate:** source-exact historical Acceptance Worker behavior demonstrated in a bounded Node VM; **current normal PWA, real browser, iPad and production OPEN**. No product files changed, no incident inferred.

## 1. HISTORY / PRINCIPLE / STANDARD

AppCache's brittle declarative update semantics were replaced by programmable Service Workers. Programmability separates (a) install acceptance, (b) runtime verification, (c) missing/corrupt-byte repair, (d) promotion and old-version retention, and (e) authoritative data backup. An install `waitUntil` rejection is not a Cache Storage transaction rollback; a `REPAIR_CACHE` command name is not proof that it repairs every resource family. A cheap UI status query should not be assumed cheap if it performs full cryptographic inventory verification.

**SOURCE (primary, checked 2026-10-20):**
- W3C Service Workers lifecycle, install/activate/message/fetch: https://www.w3.org/TR/service-workers/
- WHATWG Storage bucket/quota concepts: https://storage.spec.whatwg.org/
- WebKit quota/eviction and origin-wide data-loss risk: https://webkit.org/blog/14403/updates-to-storage-policy/
- LogMate source generator `tool/pwa_precache.dart`: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/tool/pwa_precache.dart
- Exact Hosting policy: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/firebase.json
- CI: https://github.com/yhappcom/logmate/blob/6101666530cb706a042ac82614c840af441895b1/.github/workflows/data001-pwa-artifact-validation.yml
- Prior canonical integrated artifact and hidden-resource failure: [415](415_stage8_pwa_ci_uploaded_artifact_hidden_resource_falsification_gate_20261018.md); fetch/route source diagnosis: [324](324_stage8_pwa_release_evidence_ci_route_policy_20261011.md).
- Design Studio W121: https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md
- Engineering M006 browser transfer: https://github.com/yhappcom/software-engineering-studio/blob/main/research/mobile/M006_real_browser_service_worker_transfer.md ; Safari lifecycle: https://github.com/yhappcom/software-engineering-studio/blob/main/research/mobile/M006_safari_service_worker_lifecycle_run4_closure.md ; Q006 CI verdict propagation: https://github.com/yhappcom/software-engineering-studio/blob/main/research/quality/Q006_ci_pipeline_exit_status_oracle_integrity.md
- Marketing 438, PWA ad-free first release and product advertising HOLD: https://github.com/yhappcom/marketing-manager/blob/main/research/438_logmate_one_pass_ad_architecture_and_launch_gates.md

## 2. SOURCE — pinned generator semantics

The owned Worker `install` event downloads Shell via `cacheGroup(shellCache(OFFLINE_MANIFEST), OFFLINE_MANIFEST.shell)`, writes candidate catalogue and invokes `precacheCandidate`. **That routine downloads fonts and font notices only**; it then calls `inspect(OFFLINE_MANIFEST)` over Shell+fonts+notices. `START_PRECACHE` and `REPAIR_CACHE` both invoke `precacheCandidate({promoteInitial:true})`. Thus a corrupt/missing Shell file can be detected, but these message repair paths do not redownload it. `verifiedResponse` independently checks bytes before serving known Shell entries and returns 503 on missing/invalid bytes. Fail-closed serving is not successful repair.

`status()` separately calls `inspect(OFFLINE_MANIFEST)` and `inspect(served)`. If current and candidate share the same build ID, it still hashes the same inventory twice. This is source-level logical work, not evidence of iPad latency.

The pinned `firebase.json` ignores `**/.*`; the CI generates a normal build in `build/web-normal` but uploads the Acceptance build from `build/web`. Historical archive contains 952 required resources, one mandatory hidden `.last_build_id` absent, so current normal artifact/Hosting cannot be certified from that archive.

## 3. VALIDATION — exact archived Worker under Node 22 VM

**Input provenance:** historical `logmate-efb-acceptance-fcff3372.zip` SHA-256 `d267bf9a4e8c30b1e40cf8133bdee3acf3e1dfa9cb3937da7b4d009da0180160`; extracted Worker SHA-256 `4da9ae8bc6797c478946f3e661487c1ff0e547ad21239930a5912b6fa41d083b`; Manifest SHA-256 `3a63d8f0e56790097fc4eb85be9851ac373315e3fb7caae1e3f6d4ddd07dc2da`. The archived Worker JS was **unmodified**; synthetic Cache Storage, filesystem-backed ZIP `fetch`, messages and WebCrypto digest instrumentation were supplied. Historical capability 15 Acceptance, **not current capability 16 normal PWA**.

**Repair-negative and positive controls:**
1. Before repair: Shell **0/80**, fonts **0/724**, notices **0/148** valid.
2. `REPAIR_CACHE` fetched **724 fonts, 148 notices, zero Shell resources**. Afterward: Shell **0/80**, fonts **724/724**, notices **148/148**; returned `REPAIR_REQUIRED`.
3. Corrupt one downloaded font; another `REPAIR_CACHE` fetched **exactly one font**, restoring **724/724**.
4. Populate 79 available Shell files, corrupt `index.html`; `REPAIR_CACHE` fetched **zero Shell resources**, leaving Shell **78/80** valid. `PROMOTE_VERIFIED_CANDIDATE` returned `NOT_PROMOTED`. This preserves fail-closed promotion but does not restore the damaged Shell.
5. With synthetic catalogue `currentBuildId == candidateBuildId`, a `GET_STATUS` call made **1,902 SHA-256 operations over 136,121,178 bytes = 129.82 MiB logical hashing** (79 available Shell + 724 fonts + 148 notices, inspected twice). Node VM observed roughly 1.3–1.7 seconds per call. These are **not browser network usage, quota, energy, Safari timing or product UX results**.

**Eight bounded assertions PASS:** Shell never fetched by repair; all font and notice entries fetched; missing Shell remained; duplicate current/candidate hashing; corrupted font repaired; corrupted Shell not repaired; invalid promotion refused. These are source-specific Node checks, not eight product tests.

**Harness integrity:** initial fake Cache Storage used `Response.clone()` and exposed a consumed-body simulation artifact. The harness was repaired to store immutable bytes and reconstruct Response objects on reads. This is a harness correction, not a LogMate bug. Local evidence bundle contains `repair_status_vm.cjs`, `repair_status_vm_results.json`, exact hashes and a detailed offline report. Reproduction requires the pinned historical archive, extracted into `fixture/`. Browser launch in the current container was blocked with `ERR_BLOCKED_BY_ADMINISTRATOR`: **NON-EXECUTION**.

## 4. SYNTHESIS / OPERATIONAL JUDGMENT — integrated adjacent questions

- **Installation vs repair:** a complete install path does not imply complete post-install repair. Shell and font recovery need independent positive/negative tests.
- **Verification vs repair:** a correct `REPAIR_REQUIRED` diagnosis can coexist with a repair routine unable to fix the problem. Product copy must distinguish these states.
- **Availability vs integrity:** refusing corrupt Shell bytes or invalid promotion protects version isolation, but does not make a damaged active version usable offline.
- **Deep status cost:** the candidate/served double-inspection can be a large repeated workload. Do not implement rapid status polling or infer energy impact without device profiling. A cached READY bit is not a substitute for verifying bytes at the actual response boundary.
- **Storage pressure:** failed installs/repairs can leave bytes; extra retries can contend with IndexedDB/outbox storage. Never use origin-wide clear/reset as routine remediation.
- **Deployment:** the archived hidden marker is a delivery failure; no repair algorithm can retrieve an absent deployment resource. Fix build/upload/Hosting parity before runtime acceptance.
- **Release authority:** a Waiting Worker may verify but must not unilaterally elect the served version; per-Worker Promise serialization does not make a shared catalogue cross-Worker atomic.
- **Browser and EFB boundaries:** synthetic Node behavior, generic Chromium M006 and macOS Safari fixture evidence do not certify current LogMate Flutter build, Home Screen, managed Web Clip, physical iPad or native↔PWA Sync.

## 5. MINTTAP DECISION / ENGINEERING HANDOFF (PROPOSED; NOT SHIPPED)

**D1.** Specify an approved **same-build Shell+font+notice repair** that redownloads missing/corrupt bytes from an immutable verified release inventory, checks size/hash before Cache.put and preserves the last verified version. Test 404, offline, quota, interrupted fetch, corrupt cache and version overlap. Do not fall through to a newer executable asset for an old client.

**D2.** Separate cheap state/metadata query from deliberate deep integrity audit, while preserving byte verification at the fetch response boundary and revoking stale readiness claims when appropriate. Profile status on target iPad before choosing any polling/auto-repair cadence.

**D3.** Keep release promotion tied to actual activation authority and transactionally safe cross-Worker version metadata. Do not assume Cache Storage JSON writes are atomic across Workers. Re-test reserved Firebase `/__` namespace, Auth and unknown executable paths (prior 324/419).

**D4.** Treat `Cache Storage ≠ IndexedDB ≠ verified .lbk backup ≠ remote Sync ACK`. Never delete user records/outbox to fix Worker caches. Verify file handoff by independent reopen/restore and owner/schema/lineage checks. No unattended device-to-device synchronization claim.

**D5.** Release gate: pinned **normal** capability-16 build + uploaded ZIP + Firebase served-byte parity → missing-static/Auth/`/__`/MIME negative oracles → Chromium new/upgrade/offline → Safari tab/Home Screen → physical managed iPad, storage pressure, owner-data mutation/reopen, `.lbk` restore and accessibility. Until then: **PWA release HOLD**.

## 6. TRACK C EXECUTION PACKET (DESIGNED, NOT BROWSER-EXECUTED)

| ID | Falsifiable oracle | Required tier |
| --- | --- | --- |
| R01 | Normal build, uploaded ZIP, Firebase served bytes and hidden-file policy match embedded Manifest | BUILD/HOSTING |
| R02 | Corrupt/remove Shell JS/HTML, repair with same-build bytes, verify hash and offline re-entry | BROWSER |
| R03 | Corrupt font and notice independently, repair without user ledger mutation | BROWSER/DATA |
| R04 | Offline repair failure retains previous runnable Shell and honest retry UX | BROWSER/UX |
| R05 | Quota failure during repair leaves old version and owner data intact | BROWSER/DATA |
| R06 | Profile repeated GET_STATUS/VERIFY_CACHE hashing, CPU, energy and UI responsiveness | BROWSER/PHYSICAL |
| R07 | Two Worker versions and clients concurrently update catalogue without lost mapping/premature promotion | BROWSER |
| R08 | `/__`, `/auth`, unknown executable and manifest routes under assigned/unassigned clients | HOSTING/BROWSER |
| R09 | Safari tab, Home Screen, managed Web Clip, cold start, storage pressure separately | PHYSICAL/MANAGED |
| R10 | Interrupted update then independent `.lbk` export/reopen/restore with pending Operations | DATA/PHYSICAL |
| R11 | Keyboard/screen-reader/zoom recovery states, no ads blocking logbook | UX/AT |
| R12 | Diagnostics exclude UID, flight payload, auth query and backup bytes | PRIVACY |

Each case needs source SHA, artifact digest, served origin, engine/OS/display context and independent positive/negative evidence; PASS/FAIL/UNKNOWN/BLOCKED is **per tier**, never transitive.

## 7. FIVE-TRACK ALLOCATION / TRANSFER / CONTRADICTION

**E** highest-risk owner (repair completeness, release trust, cache/data custody); **C** next execution bottleneck; **A** browser mechanics and digest workload; **B** truthful `SHELL_REPAIR_REQUIRED`, `FONT_REPAIR_IN_PROGRESS`, `OLD_VERSION_USABLE`, `BACKUP_VERIFIED` task states (Design Studio W121); **D** privacy-minimal diagnostics and no unverified offline/install/sync public claims (Marketing 438). This is risk-weighted allocation, not five parallel primers.

**CONTRADICTION:** `REPAIR_CACHE` sounds comprehensive but downloads only fonts/notices; `GET_STATUS` sounds cheap but hashes the full inventory twice when candidate=served. Older `STATUS.md` 2026-10-09 legacy Worker/catch-all rewrite statements were superseded by later pinned LogMate source; they are not current deployment facts.

**OPEN:** exact normal PWA/Hosting/Chromium/WebKit/physical iPad, managed MDM policy, Shell repair implementation, safe cache retirement, IndexedDB/.lbk data recovery, native↔PWA Sync, AT/human evidence. **CHANGE WATCH:** W3C Service Workers, WebKit storage/install policies, Flutter generated bootstrap, Firebase reserved routes, GitHub hidden-file handling.

**Stop check:** Positive font repair, negative Shell repair, invalid promotion, repeated hash cost, storage/data custody, routing, five-track transfer and R01–R12 have been integrated. Another synthetic microtest cannot promote runtime; next major boundary is current normal artifact and real browser/physical iPad. **Stage 8 continues; Production validation OPEN; PWA release HOLD.**
