# 508 — Stage 8 LogMate PWA cross-generation control catalogue and release-artifact custody

Date: 2026-10-24 (Asia/Seoul)
Evidence class: SOURCE / SYNTHESIS / MINTTAP DECISION / OPEN / DEPENDENCY / VALIDATION / CHANGE WATCH / TRANSFER VALIDATION / CONTRADICTION
Primary owner: Track E (release trust, storage/control governance); Track A (Service Worker/Cache API mechanics) and C (falsification) are critical suppliers. B and D consume verified outcomes. Web Manager coordinates, not a sixth track.
Repository boundary: Web Manager may be edited; LogMate, Design Studio, Software Engineering Studio and Marketing Manager are READ-ONLY.

## 1. Canonical refresh, why this is the highest-value next bundle [SOURCE]

Read Web Manager AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md, studies 505–507, and recent commits. Reviewed Design Studio W121, Engineering D006 and M006 Safari cold-start transfer, Marketing 438. LogMate latest observed main is b64938efe38cea0ca5ad0dd2604321c4b780e6d8, which adds/updates only two evidence documents after 97a9a661. Source files inspected: tool/pwa_precache.dart, tool/precache_flutter_web.dart, tool/verify_pwa_artifact.dart, web/flutter_bootstrap.js, web/index.html, web/manifest.json, Makefile, firebase.json, test/tool/pwa_precache_test.dart, and the PWA/browser workflows. Product implementation remains unchanged by this study.

**Priority comparison.** E remains the strongest release bottleneck: source-level recovery-hold collision (506), unverified managed iPad data custody (507), and now the Worker catalogue/release artifact boundary. A supplies the concrete lifecycle and Cache API semantics; C needs an actual two-worker/hosted-bundle oracle. B already has recovery-state IA but no exact-device human/AT proof (W121); D has no approved web advertising or real deployment measurement (Marketing 438). Spending another cycle on generic install primers would not change the gate. This bundle instead tests three adjacent production-relevant assumptions: a per-worker lock protects a shared catalogue; a shell hash identifies the entire release; and a passing PWA Acceptance CI job supplies a safe deployable NORMAL artifact.

## 2. History/problem → platform rule → present implementation [SOURCE / SYNTHESIS]

Service Workers replaced AppCache's brittle declarative update model with event-scoped install, waiting, activate, fetch and explicit Cache Storage. The update model permits a new installing Worker to prepare assets while an older active Worker continues to serve clients; the new Worker does not normally activate while the old Worker controls clients. W3C Service Worker explainer explicitly describes installation while the old version is still in control. Cache API put() overwrites a matching entry; Cache Storage does not expose a cross-worker compare-and-swap or a multi-operation transaction for the JSON catalogue.

Primary references checked 2026-10-24:
- W3C Service Worker explainer: https://github.com/w3c/ServiceWorker/blob/main/explainer.md
- W3C Service Worker standard: https://w3c.github.io/ServiceWorker/
- MDN Cache put: https://developer.mozilla.org/en-US/docs/Web/API/Cache/put
- MDN Cache API: https://developer.mozilla.org/en-US/docs/Web/API/Cache
- MDN Clients.matchAll: https://developer.mozilla.org/en-US/docs/Web/API/Clients/matchAll
- MDN ServiceWorkerContainer.register, scope and updateViaCache: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
- WebKit storage policy: https://webkit.org/blog/14403/updates-to-storage-policy/

**Exact LogMate source facts.** tool/pwa_precache.dart generates the Worker with one shared CacheStorage key, 'logmate-offline-control-v2' / '/__logmate_offline_control_v2.json'. Its readControl -> change -> writeControl operation uses an in-memory 'controlMutation' Promise chain inside a single Worker instance. The installing Worker writes candidate/version metadata in install/precache; the active Worker writes 'clientBuilds' mappings on navigation. web/flutter_bootstrap.js registers the owned Worker with scope based on document.baseURI and updateViaCache 'none'. The Worker deliberately avoids skipWaiting and verifies cached response bytes before serving them. These are useful controls, but they do not establish cross-generation atomicity.

## 3. New conditional risk: two Worker generations share one mutable JSON record [SOURCE / CONTRADICTION / OPEN]

**Counterexample, no invented runtime claim.** Let control record C contain current v1 and no client assignment or v2 candidate. The old active Worker and new installing Worker each read C. The old Worker adds client X -> v1. The installing Worker adds v2 manifest/candidate. Both serialize their own local mutation queue correctly, but the queues are separate JavaScript globals. If the new Worker puts its stale snapshot last, client X's mapping disappears. If the old Worker puts its stale snapshot last, v2's candidate/manifest update disappears. A later install write may repair the candidate, but does not guarantee the lost client mapping is restored; a later old-worker write can likewise overwrite a completed candidate update. The exact interleaving and user-visible effects require real browser evidence.

**Bounded executable model:** research/handoffs/sw_control_catalogue_race_model.js uses Node 22 stdlib to exercise both commit orders, a hypothetical globally serialized reference, and 5,000 closed-client IDs. Executed locally with 'node --test': **4/4 PASS**. These passes prove only that the source-compatible read/modify/put shape permits a lost-update interleaving; they are not evidence that Chrome/Safari actually scheduled it, that LogMate has lost data, or that the proposed reference architecture is production-ready.

**Risk interpretation:** losing a live client's build mapping can make a later shell/font request return the Worker's explicit 503 'Offline version is not assigned; reload required.' Losing candidate metadata can disrupt readiness/promotion bookkeeping. Neither outcome alone proves ledger loss, because Sembast/IndexedDB is a separate store; the operational risk is an avoidable failed/offline update or recovery path. Do not call this a reproduced production defect.

**Critical distinction:** a Promise lock protects one event loop/Worker instance, not the origin-wide CacheStorage record across active and installing Worker generations. The source comment accurately says 'in this worker'; treating it as a cross-worker guarantee would be a false transfer.

## 4. Adjacent state-lifecycle risk: unbounded clientBuilds catalogue [SOURCE / SYNTHESIS / OPEN]

The generated Worker assigns both clientId and resultingClientId on root navigation, writes them to control.clientBuilds, and has no observed deletion/pruning path in the inspected generator. New navigations/process lifecycles can therefore leave historical client IDs in a persistent JSON object. The bounded model demonstrates linear key growth; it does not establish an actual storage quota or failure threshold. A physical iPad's long-offline/dormancy workload makes this worth testing, especially because CacheStorage persistence and eviction are separate from app-ledger custody.

**Design guard:** prune only with a proved live-client set and an explicit grace/race policy. MDN Clients.matchAll({includeUncontrolled:true}) is a possible observation primitive, not a proof that an in-flight navigation cannot be removed. A naive 'delete all IDs not returned now' can break subresource assignment while a client transitions. Treat client identity and build assignment as short-lived runtime routing state, not remote Sync authority or backup evidence.

## 5. Adjacent identity risk: appBuildId does not identify Worker generation [SOURCE / CONTRADICTION]

In buildOfflineArtifact(), appBuildId is the first 32 hex characters of SHA-256 over the JSON shell-file description. The shell description deliberately excludes the generated Worker and generated offline manifest; the Worker is written afterward. The catalogue indexes versions by appBuildId. Thus a Worker-generator-only change with identical shell bytes can change the Worker script while retaining appBuildId. The same label then does not uniquely describe the Worker semantics, even if all cached shell files remain byte-correct.

This is an identity/granularity limitation, not a demonstrated runtime break. A separate Worker-generation identifier and an independently archived full-release digest should be recorded without creating a circular hash dependency between Worker source and embedded manifest. Reusing appBuildId as an all-artifact supply-chain identity is not justified.

## 6. New release custody risk: NORMAL output and default Hosting root diverge [SOURCE / MINTTAP DECISION]

The PWA CI workflow first runs 'BUILD_WEB_OUTPUT=build/web-normal make build-pwa' and validates a NORMAL build with the development harness absent. It then runs 'make build-pwa-acceptance' into default 'build/web' and uploads only that Acceptance directory. The checked-in firebase.json Hosting public root is also 'build/web'. Therefore the CI workspace's final default Hosting root contains the development-only Acceptance build, not the earlier NORMAL build. A deployment from that workspace/root without an explicit separate gate could publish the wrong artifact. **No actual Firebase deployment, credential, production exposure, or incident was observed.** The workflow does not contain a deploy step; this is a source-level configuration hazard.

The verifier correctly checks that the acceptance marker is absent in NORMAL and present when required for Acceptance. It validates manifest-listed shell/font/notice bytes and Worker string-level invariants. It does not prove that the NORMAL directory is archived, that a later deploy uses it, that hosted bytes match the validated archive, or that an iPad installed/ran them.

**Provisional release rule:** a deployable NORMAL artifact must be separately archived with source SHA, toolchain, post-build transforms, manifest/Worker/full-tree digest, marker-absence verdict and release approval. Acceptance output must be isolated from the deployment root. A deployment gate must inspect the exact bytes it publishes, then independently fetch and compare served Worker/bootstrap/manifest and critical shell assets; route/auth exclusions and offline behavior remain separate runtime tests. Do not automatically change LogMate Hosting/CI from this research repository.

## 7. Exact CI provenance correction: stronger evidence, still not release proof [SOURCE / TRANSFER VALIDATION]

The newly merged LogMate docs/evidence/pr16-pr17-post-f1-integration-review-20261024.md reports all six workflows successful on integration SHA 95250e55acfb0789595475a8947ec1bff45d04df. GitHub Actions run metadata independently confirms:
- Core 40045831745 — success
- Browser 40045834556 — success
- Checkpoint 40045837170 — success
- iOS Build 40045839712 — success
- PWA Acceptance 40045842917 — success
- Repository Fast 40045845781 — success

All six are attached to 95250e55 (2026-10-24 00:36 UTC). Git tree SHA for 95250e55 and PR #16 merge 97a9a661 is **identical: 1f2554df612060a753e321f9d76f059d40f970e8**. Later main b64938e changes only two evidence docs. Therefore the prior shorthand 'no browser validation of the merged code' is too broad: the same source tree has six successful integration workflows, including Chrome and PWA packaging. This does **not** turn those checks into exact-b649-head CI, real browser-process restart, 37-store populated Chrome restore, Worker concurrency, NORMAL artifact custody, Safari/Home Screen, MDM iPad or authenticated remote Sync validation. Preserve both the improved source-tree evidence and its boundaries.

## 8. Engineering-owned falsification and remediation packet [VALIDATION / DEPENDENCY]

| ID | Required independent observation / negative control |
| --- | --- |
| W01 | Two exact generated Worker versions, same origin/scope; old active client remains open during new install; record both Worker script hashes and client IDs. |
| W02 | Controlled delay between control-cache read and put in old active/new installing contexts; force both write orders; detect lost candidate or client mapping. |
| W03 | Candidate verified and waiting while old client loads a late font/script; no cross-build bytes or unexpected 503. |
| W04 | Kill/restart Worker during install and after control write; reconcile catalogue with actual version caches and clients. |
| W05 | Same shell bytes but changed Worker logic; prove whether appBuildId aliasing affects readiness/rollback/diagnostics. |
| W06 | 1/100/5,000 navigation/reopen cycles; observe control size, stale IDs, quota and safe pruning with in-flight requests. |
| W07 | First install with clients.claim and previously uncontrolled page; test late subresources and truthful reload-required UX. |
| W08 | Missing/corrupted cached byte, partial candidate, interrupted download, storage pressure: preserve prior runnable shell and ledger. |
| W09 | Concurrent same-origin page/cache mutation negative test; do not equate same-origin access with authenticated release authority. |
| W10 | NORMAL and Acceptance separately build/verify; assert unique directories, compile-time marker polarity, no accidental overwrite. |
| W11 | Archive NORMAL exact bytes, source SHA, SDK, font archive, full tree digest, Worker/manifest digest; independently verify downloaded artifact. |
| W12 | Host only NORMAL via explicit deploy root; fetch served bytes, content types, HTTPS/Worker scope, auth routes and cache policy. |
| W13 | Old/new JS with capability-v16/v17 Sembast and verified owner state; no stale mutation or hidden 503 before backup. |
| W14 | 37-store populated LBK restore including R03/R04 collision and R05/R11 controls; no fabricated Receipt/ACK. |
| W15 | Safari tab, user Home Screen and managed Web Clip/full-screen as separate exact-build, storage/MDM populations (507 I01–I16). |
| W16 | Physical device offline cold-start, process restart, cache loss, owner-lock/export/recovery and native-mobile rejoin with explicit consent. |

**Candidate engineering options, not approved patches:** (a) use an atomic IndexedDB transaction for a single catalogue record with version/currentness checks and crash/fault tests; (b) remove the cross-generation shared mutable record by storing immutable per-build manifests and separate client routing records, with a carefully defined activation/retirement reconciliation protocol; (c) designate a single lifecycle owner for pointer mutations and avoid writes by an installing Worker to active-client routing state. None is automatically safe; IDB atomicity is local only, activation races remain, and no design may delete the last runnable version or unique ledger data to repair a catalogue.

**Do not promote** a synthetic model PASS, a source-tree-equivalent CI PASS, a Worker registered state, a 724-font integrity check, or a hosted icon into offline/backup/Sync release certification. The release decision requires exact artifact + hosted/runtime + device + data custody evidence.

## 9. Five-track integration, contradiction register and decision [TRANSFER VALIDATION]

- **E (owner, highest pressure):** release directory isolation, immutable artifact custody, Worker catalogue trust/currentness, safe rollback, backup before repair and incident containment. Owns the no-release decision.
- **A (platform prerequisite):** active/installing Worker overlap, Cache API overwrite, browser client IDs, scope, control and Safari/WebKit differences. The platform does not provide a cross-worker lock for this JSON record.
- **C (high execution pressure):** W01–W16 with source/tree/artifact/run/device provenance and fail-closed negative controls; Design Studio W121's exact-runtime/AT/human stop rule applies.
- **B (consumer):** distinguish 'offline version not assigned; reload required' from data loss, and 'local saved / backup verified / remote ACK' from each other. No destructive reload or reinstall prompt without unique-data preservation evidence.
- **D (consumer/challenger):** privacy-minimized counts for Worker generation, update/503/recovery outcome, no record payloads; Marketing 438's conditional PWA ad-free and no unsupported seamless-Sync claim remain in force.

**CONTRADICTIONS resolved:** 'per-worker serialized' is not 'cross-generation atomic'; 'shell digest' is not 'Worker/release digest'; 'PWA CI green' is not 'NORMAL hosted artifact proven'; 'same-tree integration green' is useful evidence but not exact-main/managed-device acceptance; 'a 503 means ledger loss' is unproven.

**OPEN:** real concurrent Worker interleaving and impact, browser client ID lifecycle/pruning, actual artifact generation hashes, deploy process/permissions, exact hosted origin, true source-to-host custody, R03/R04 compiled behavior, full 37-store Chrome restore, physical Safari/iPad/MDM and authenticated server Receipt. No production facts are inferred.

**CHANGE WATCH:** WebKit Worker scheduling and storage policy; Chromium/Chrome Worker lifecycle; Flutter-generated bootstrap; LogMate source and CI workflow SHA; iPadOS/MDM launch and partition policy; browser quota; future server Sync/Receipt design.

**Decision / stop check:** Stage 8 applied Security/Privacy/Trust remains active, Track E primary bottleneck, A/C urgent dependencies. Production validation **OPEN**; PWA release **HOLD**. The adjacent high-value questions in this cycle were completed together: actual Worker control algorithm, independent lost-update counterexample, unbounded client IDs, build-ID granularity, NORMAL/Acceptance Hosting root, and corrected six-workflow source-tree provenance. The next materially different gate is Engineering's exact Worker/browser and artifact/Hosting execution (W01–W12) combined with R03/R04 and 37-store restore, then policy-envelope-matched managed iPad. No product or other specialist repository was modified.
