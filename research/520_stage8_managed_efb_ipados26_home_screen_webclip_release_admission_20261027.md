# 520 — Stage 8 managed-EFB PWA admission: iPadOS 26 Home Screen, managed Web Clips, offline and release custody

Date: **2026-10-27**. State: **SOURCE + SYNTHESIS + product-source transfer / generic platform decision gate; exact NORMAL/HTTPS/installed/managed-device validation OPEN; bounded iPadOS Safari Simulator harness evidence now observed**. Owner: **E Web Architecture, Security & Operations**, with **A** platform prerequisites, **C** acceptance evidence, **B** task/recovery semantics, **D** claim/measurement controls. This is a **major cross-track domain integration**, not a sixth PWA track or an implementation change.

## 1. Evidence boundary and why this domain matters [SOURCE / HISTORY / OPEN]

The company has a plausible EFB scenario: a LogMate-like offline-first PWA on a company iPad where ordinary App Store installation may be unavailable. **The particular employer's enrollment, OS version, allowed browser, Web Clip policy, storage partition, connectivity, aviation obligations and PWA permissions have NOT been observed.** Neither Home Screen icon appearance nor an MDM-managed Web Clip proves Service Worker control, cached executable bytes, IndexedDB durability, independent backup, or native-mobile Sync.

Prior Web Manager research 504/508/515/519 establishes a product release HOLD, exact NORMAL artifact custody gap and conditional source-level Worker risks. This study resolves a **distinct distribution/admission question**: what can be concluded from current iPadOS Home Screen and Apple-managed Web Clip capability, and what independent evidence is still necessary for a defensible EFB deployment?

Historical problem: AppCache coupled declarative caching to opaque browser behavior and lacked the fine-grained programmable lifecycle needed for resilient updates. Service Workers separated registration/install/activate/control and programmable FetchEvent/CacheStorage from **OS-level app presentation**. The modern OS can expose an app-like window without establishing offline readiness. The distinction is now especially material on iOS/iPadOS 26.

Primary sources, inspected **2026-10-27**:
- W3C Service Workers Candidate Recommendation Draft **2026-09-17**: https://www.w3.org/TR/service-workers/
- web.dev Service Worker lifecycle/update (Chromium-oriented explanatory implementation guidance): https://web.dev/learn/pwa/service-workers and https://web.dev/learn/pwa/update
- WebKit, **Safari 26.0**, “Every site can be a web app on iOS and iPadOS”: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- WebKit, iOS/iPadOS **16.4** Web Push, manifest ID, third-party Add to Home Screen and Shared iPad condition: https://webkit.org/blog/13878/
- WebKit, **17.2** Home Screen cookie-copy behavior and independent post-install storage: https://webkit.org/blog/14787/webkit-features-in-safari-17-2/
- WebKit, storage quota/eviction policy (Safari **17+**, OS-version scoped): https://webkit.org/blog/14403/updates-to-storage-policy/
- WebKit, first-party Home Screen vs Safari ITP behavior: https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
- Apple Platform Deployment, **Web Clips device-management payload**: https://support.apple.com/en-gb/guide/deployment/depbc7c7808/web
- Apple Device Management WebClip schema: https://developer.apple.com/documentation/devicemanagement/webclip
- Apple Home Screen Layout IconItem: https://developer.apple.com/documentation/devicemanagement/homescreenlayout/iconitem
- Software Engineering Studio canonical validation contract: https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md and https://github.com/yhappcom/software-engineering-studio/blob/main/coordination/CROSS_REPO_COLLABORATION.md

## 2. New platform distinction: icon ≠ offline PWA [SOURCE / SYNTHESIS / CHANGE WATCH]

**Safari 26 / iOS 26 / iPadOS 26:** WebKit states that by default **any website** added to the Home Screen opens as a web app, and the user may instead turn off **Open as Web App** to create a browser bookmark. A manifest and Service Worker are **not prerequisites** for this Home Screen presentation. The site may still benefit from a manifest and Worker; absence of a manifest does not preclude the icon/app-like window. This is an **Apple/WebKit OS presentation policy**, not a new W3C guarantee of offline operation or an assertion about every enterprise configuration.

**Earlier versions:** WebKit's 16.4 description ties standalone Home Screen behavior to appropriate manifest/display or Apple meta configuration, and documents third-party browser Add to Home Screen constraints (including Shared iPad caveats). **Do not back-port the iPadOS 26 UI default to 16.x/17.x/18.x devices** or assume a company's iPad is on 26. On 17.2+ WebKit describes cookie copying at creation, **not IndexedDB/CacheStorage copying**, and post-creation storage isolation. Cookie/session continuity is not logbook-data continuity.

**Managed Web Clips are another distribution path.** Apple documents an MDM Web Clip payload with URL, label, optional nonremovable status and **Full screen**. Apple also documents managed Home Screen layout. An MDM administrator may be able to deliver a Web Clip without an App Store binary, but actual enrollment, Safari restriction, Web Clip installation and FullScreen policy require **organization/device proof**. Apple's documentation explicitly cautions that MDM vendors implement settings differently. A Web Clip is **not** evidence that the company's iPad allows user-installed Home Screen PWAs or that an app can run unattended in the background.

**CONTRADICTION resolved:** “The iPad shows a LogMate icon / opens fullscreen” and “LogMate is installed, offline-capable and durable” are **not equivalent statements**. Under iPadOS 26 the first can be true for an ordinary website with no Service Worker at all; under managed Web Clips it can be true because MDM placed an icon. This is a semantic false-positive risk for release acceptance and Marketing claims, **not a demonstrated LogMate defect**.

## 3. Independent predicates and trust boundaries [SYNTHESIS / OPERATIONAL JUDGMENT]

An EFB-ready PWA requires independent evidence for each predicate, not one broad “installed” result:

| Predicate | Evidence needed | False-positive example |
| --- | --- | --- |
| **P1 distribution** | exact OS/browser/MDM profile and whether Home Screen/managed Web Clip action is permitted | icon delivered by MDM |
| **P2 presentation** | actual standalone/fullscreen launch and route/URL | Safari 26 web-app window without SW |
| **P3 registration** | secure context, exact origin/scope, registered Worker script digest/state | manifest present |
| **P4 control** | page controller identity, first-control/reload and old/new coexistence | registration.ready but unassigned claimed client |
| **P5 executable offline** | retained NORMAL bytes; airplane-mode cold start; verified shell/font/notice; no 503 | a prior online page still in memory |
| **P6 local data** | owned IndexedDB/Sembast store inventory and readback across termination/restart | UI “Saved” after an in-memory write |
| **P7 recoverability** | external export/readback, clean destination restore and provenance/owner checks | backup file name exists |
| **P8 update safety** | exact OLD/NEW Worker and shell identity, atomic admission, fault injection and rollback policy | candidate READY or appBuildId alone |
| **P9 remote authority** | explicit online auth/rejoin, queue review, conflict and Manual Sync acknowledgment | network online indicator |
| **P10 operational custody** | approved build→archive→Hosting served bytes/headers→device→incident record | successful CI build only |

Neither P1 nor P2 entails P3–P10. P3 does not entail P4. P5 does not entail P6/P7. P6 does not entail P9. **Security consequence:** the release authority must not be elected by a presentation-layer affordance or self-reported Worker status.

The 2018-era generic Service Worker “persistent background processing” language does not promise an always-running daemon, unrestricted sync, or unattended peer-to-peer transport. A service worker is event-driven and may be terminated. Separate any Web Push/Badging support from direct device Sync and managed-network permissions. For this product, **offline-first local usage + explicit, authenticated, data-preserving transfer/Sync when supported** remains a *design direction*, not a validated cross-device architecture.

## 4. Exact LogMate source transfer, pinned and bounded [SOURCE / TRANSFER VALIDATION]

Read-only GitHub source at LogMate **main@26d2d7cf2c20c55026c6f84b838dcb6442f7a3f1**, reviewed 2026-10-27:
- `web/manifest.json@8225e76f`: `start_url: "."`, `display: "standalone"`, app name/icons; **no explicit manifest `id`**. This does not disqualify Safari 26 Home Screen presentation. Manifest identity and origin/storage identity are distinct. The absence of `id` requires an identity/upgrade test, not an unsupported claim that installation fails.
- `web/flutter_bootstrap.js@a70625e8`: secure-context check and `navigator.serviceWorker.register` with explicit scope and `updateViaCache:'none'`; registration errors are logged, and Flutter app startup is deliberately **not gated on Worker registration**. A successfully displayed app may therefore have **no working offline Worker**. This is a source-confirmed separation, not an observed device failure.
- `tool/pwa_precache.dart@90a67954`: install caches candidate shell; activate calls `clients.claim()`; Worker control and version catalogue logic are independent of Home Screen presentation. Prior **519 §§26–34** conditionally identify warm-start verification amplification, mutable metadata/headers, incomplete shell repair, first-claim unassigned 503, two-Worker catalogue lost updates, failed-install residue, shell/Worker release-ID mismatch, and waiting-Worker message promotion. These remain **source/model risks**, not real iPad incidents.
- `tool/verify_pwa_artifact.dart@b3993279`: validates many asset invariants and development Acceptance exclusion, but §519 documents gaps in independently approved whole-release identity; no current NORMAL artifact downloaded or actual Dart negative test claimed here.
- `firebase.json@9ac0972e`: `hosting.public=build/web` and Cache-Control policy. Exact production domain, redirects, served headers and whether any approved NORMAL bytes were deployed are **UNKNOWN**. Historical GitHub CI evidence in 504: NORMAL build verified in CI but **not retained** as the downloadable release archive; development Acceptance archive must not be substituted.

**Identity consequence:** Home Screen name/icon, manifest identity, origin, storage partition, Worker registration, `appBuildId`, Worker script digest, authenticated account, device lineage and backup identity are **different identifiers**. They must not be collapsed into “same app.” Changing hostname or installing a separate Home Screen copy does not transfer IndexedDB flight records; WebKit 17.2 describes cookie copying only at installation, not general storage migration. Existing §515 origin-host migration rules and §504/519 release gates remain authoritative.

## 5. Platform and management matrix [SOURCE / OPEN / CHANGE WATCH]

| Dimension | W3C/WHATWG layer | Chromium/browser implementation | Apple/WebKit/iPadOS | Enterprise EFB policy |
| --- | --- | --- | --- | --- |
| Home Screen icon/standalone | Web App Manifest provides metadata, not offline proof | Chromium install UX/criteria implementation-specific | iPadOS 26 default web-app window for any added site; user can choose bookmark | User add may be blocked; MDM Web Clip may be provided |
| Worker registration | HTTPS secure-context, origin/scope/lifecycle | exact Chrome version/runtime needed | Safari/Home Screen and OS version must be tested independently | Safari/Web Clip restrictions and enrollment unknown |
| Offline shell | FetchEvent/CacheStorage plus app-specific caching | actual controller and retained bytes required | same principle, different lifecycle/quota/eviction behavior | offline restart and managed app execution must be witnessed |
| Data durability | Storage API is not backup guarantee | persistence/eviction/quota implementation-specific | WebKit 17+ quota and eviction, Home Screen distinct context; 17.2 cookie copy only | profile wipe, OS updates, Shared iPad and reset behavior unknown |
| Background/push/sync | distinct APIs with distinct support and permission | platform/version-specific | WebKit 16.4 Home Screen Web Push support ≠ arbitrary background peer sync | network, notifications, managed policies may restrict |
| Identity/transfer | origin/storage-key and manifest ID differ | installation may create distinct app context | separate Home Screen installs possible; name + manifest ID used for Focus identity | managed Web Clip payload URL/name do not prove ledger continuity |

Do not infer current EFB OS/version or managed Safari policy from public Apple feature announcements. **CHANGE WATCH:** iPadOS 26+ Home Screen toggle, WebKit storage rules, Web Clip FullScreen behavior, Shared iPad limitations, Safari app restrictions, Chrome install heuristics and exact product bootstrap/manifest/Hosting changes.

## 6. Consequence-ranked failure and acceptance architecture [SYNTHESIS / DEPENDENCY / VALIDATION DESIGN]

**Priority 0 — irreversible-data/release authority:** obtain the **approved, independently retained NORMAL** archive with full hashes and Acceptance-marker negative proof; bind build source, toolchain, Worker digest, offline manifest, `appBuildId`, Hosting projection and actual served HTTPS bytes/headers. Confirm an independent 37-store (or current exact product store inventory) export/readback and clean-device restore before any destructive update/clear/host migration. This is the dominant Track E/C bottleneck, not a reason to invent more synthetic Worker tests.

**Priority 1 — distribution and first-control:** collect two distinct installation paths on each eligible device: user Add to Home Screen **and**, if the employer permits, managed Web Clip. Record OS build, Safari/WebKit version, enrollment/Shared iPad state, MDM payload/FullScreen restrictions, source URL/origin and whether a browser bookmark was chosen. Record registration, active/waiting/controller identity, Worker script digest, `navigator.serviceWorker.controller` before/after initial load, reload and cold start. Distinguish no Worker, registered but uncontrolled, claimed-unassigned, controlled-and-ready and offline-verified states.

**Priority 2 — lifecycle and interrupted operations:** use retained OLD/NEW NORMAL artifacts to run the existing 519 §31/§32/§34 negative controls: two-Worker catalogue interleavings, install rejection residue, waiting Worker message, stale client, cache/metadata corruption, 503 and repair behavior, version-only Worker change. Never use production flight records as destructive test fixtures. Browser trace and OS execution, not V8 mock PASS, decide runtime acceptance.

**Priority 3 — offline task and recovery semantics:** airplane-mode cold launch, long offline edits, browser process termination, device reboot, storage pressure and reinstall/host-change. Preserve provenance and unique edits. For failure, show *local saved*, *backup verified*, *update waiting*, *repair required*, *remote sync pending*, *remote acknowledged* as different states. Design Studio owns copy/interaction; Engineering owns implementation; Web Manager owns web task-state requirements.

**Priority 4 — acquisition/measurement:** do not claim “installable on all airline EFB iPads,” “works offline,” “automatically syncs with native,” “never loses records,” “ads supported in PWA,” or “background sync” from icon/manifest/source evidence. If telemetry is permitted, capture only sanitized build/OS/controller/route/failure class and aggregate timing; no UID, flight contents, auth codes, or raw client IDs.

## 7. Reusable real-device validation packet (not executed) [VALIDATION / OPEN]

Use the existing LogMate W-012/013/014/030/031/036 and Web Manager 504/508/515/519; **do not open duplicate product test projects**. Each case requires exact artifact/ref/OS/browser/MDM, prestate, independent oracle, observed result, negative control and evidence limit.

| ID | Stimulus and required discriminating evidence |
| --- | --- |
| EF01 | iPadOS 26 Safari Add to Home Screen with Open as Web App **on**; prove presentation, then separately Worker registration/control and cold offline. |
| EF02 | Same OS, toggle **off**; confirm browser bookmark is not misclassified as installed standalone PWA. |
| EF03 | Pre-26 compatible iPadOS branch; do not transfer iPadOS 26 default behavior; record actual manifest/meta and user UI. |
| EF04 | Managed Web Clip FullScreen vs ordinary user-installed icon; capture actual MDM payload and allowed browser, not just icon. |
| EF05 | Managed Safari restricted/hidden or Shared iPad path; document whether installation, launch and offline use are permitted. |
| EF06 | Valid standalone launch with deliberately absent/rejected Worker; app presentation must **not** be scored offline PASS. |
| EF07 | Worker registered but first page uncontrolled / `clients.claim` transition; capture requests and any 503 before reload. |
| EF08 | Retained NORMAL OLD→NEW update with waiting Worker and explicit/implicit message paths; trace controller and bytes. |
| EF09 | CacheStorage shell missing, metadata missing, font missing and partial failed install; verify no unsafe newer-byte fallback or data wipe. |
| EF10 | Offline cold start after device reboot and WebKit process termination, not merely an already-loaded screen. |
| EF11 | Separate Safari tab, Home Screen app and second Home Screen copy; test data isolation without assuming shared IndexedDB. |
| EF12 | Local flight edit + export/readback + clean destination 37-store restore; verify unique edits and source provenance. |
| EF13 | Storage pressure, eviction, OS/profile removal and managed re-enrollment (isolated test device); prove recoverability from independent backup. |
| EF14 | Offline→online rejoin and explicit Manual Sync; prove authentication, conflict review and remote ACK separately from connectivity. |
| EF15 | Actual HTTPS root/auth/policy routes, headers, Worker scope, manifest/start URL and custom/default host; no action-code logging. |
| EF16 | Accessibility/UX: text scaling, focus, screen reader, offline/update/error wording and safe user choice on representative iPad. |

Verdicts: **NOT RUN / PASS / FAIL / UNKNOWN / NOT APPLICABLE**, with reason. A green icon, a source audit, a V8 mock, an emulator and a real managed iPad are different evidence tiers. An MDM “not allowed” result is a **deployment constraint**, not automatically a browser standards defect. A source-conditional 503 without a real request trace is not an observed field failure.

## 8. Five-track maturity and transfer [DEPENDENCY / TRANSFER VALIDATION / CONTRADICTION]

- **E — primary/highest consequence:** OS distribution and MDM policy cannot elect release authority; approved NORMAL artifact, served HTTPS trust, Worker update/rollback, independent backup and incident/recovery custody are the bottleneck. Generic knowledge strong, product admission **OPEN**.
- **A — high dependency:** W3C Worker registration/control/lifecycle, manifest identity vs origin, WebKit 26 Home Screen presentation and Web Clip distinctions; physical OS-specific execution **OPEN**.
- **C — high dependency:** evidence ladder and EF01–EF16 negative controls; source/model/CI pass must not become device, accessibility, resilience or data-durability PASS. Design Studio Web W121 is Stage 3 PRACTICE, not AT/human acceptance.
- **B — bounded transfer:** Design Studio `progress/WEB_STATUS.md` W121 and Content/Interaction evidence own truthful install/update/offline/recovery labels; web task structure separates distribution, local edit, backup and remote acknowledgment.
- **D — bounded transfer:** Marketing Manager `STATUS.md` D8–D10 maintains LogMate PWA/offline/sync/ads/Store-claim HOLD; web measurement must not infer successful offline operation from Home Screen installs.
- **Engineering:** Software Engineering Studio `methods/VALIDATION_STANDARD.md` and `coordination/CROSS_REPO_COLLABORATION.md` supply artifact→runtime and independent-oracle methodology. LogMate/product Engineering owns executable browser/MDM/ledger harness and code changes. Web Manager does not alter peer/product repositories.

## 9. MintTap direction, open questions and stop check [MINTTAP DECISION / OPEN / CHANGE WATCH]

**MINTTAP DIRECTION (research-level, not product approval):** Keep EFB PWA distribution **conditional on the employer/device**, with **separate user Home Screen and MDM Web Clip paths**. Accept neither as proof of offline readiness. Use a per-platform release-admission chain: **NORMAL archive → approved HTTPS served bytes → OS/MDM launch path → Worker control → offline cold start → owned ledger readback → independent backup/restore → data-preserving update/rejoin**. The absence of App Store installation need not rule out Web Clips or Home Screen web apps in principle, but **neither path is verified on the actual employer device**.

**OPEN:** actual managed EFB fleet and OS versions; MDM restrictions and Web Clip payload; Safari/Home Screen installation; exact current NORMAL artifact and HTTPS deployment; 37-store backup/restore; multi-origin and multiple Home Screen copies; offline/online, Sync, auth, storage eviction, update and physical-device/human/AT validation. No production vulnerability, data loss, enterprise installation authorization, advertising viability or unattended Sync asserted.

**Adjacent-question check completed:** (i) Safari 26 presentation vs older Safari, (ii) user-installed vs managed Web Clip, (iii) manifest ID vs origin/storage identity, (iv) secure-context Worker vs app startup, (v) lifecycle/first-control and waiting versions, (vi) storage eviction/cookie-copy, (vii) data export/recovery, (viii) Sync authority, (ix) Hosting/CI artifact chain, (x) UX/claims/measurement, (xi) MDM/Shared iPad restrictions, and (xii) independent executable oracle design. Further abstract scenarios have lower information gain than **real NORMAL archive + actual device/MDM/runtime evidence**. Stop at this substantive domain checkpoint; do not manufacture a micro-test. **Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD**. No LogMate/Design Studio/Marketing/Engineering writes.


---

## 10. Applied Safari Simulator evidence promotion — W-031, 2026-10-27 [SOURCE / VALIDATION / TRANSFER VALIDATION]

**Why this is a material checkpoint:** The prior 520 admission matrix had no actual iPadOS Safari runtime. Canonical LogMate now contains **real iPadOS 26.1 Simulator Safari tab and Safari WebDriver observations**, but **only for a purpose-built synthetic PWA harness**, not the NORMAL authenticated app, installed Home Screen web app, or managed company iPad. This promotes a **narrow platform/runtime subclaim** from OPEN to bounded PASS; it does not change the release gate.

### 10.1 Exact source, artifact and evidence custody

- Product authority: LogMate \`MASTER.md\`; execution evidence: \`docs/evidence/w031-simulator-preacceptance-2026-10-27.md\`, \`docs/evidence/w031-simulator-2026-10-27/runtime-summary.json\`, \`docs/evidence/w031-safari-followup-2026-10-27/results.json\`, and W-031 card. Read-only main checked 2026-10-27 at \`6180fd80c1b084bd4347534c0770fe425f707768\`. Direct GitHub compare \`7caaee998251602e72159eeebda61f701bdea270...6180fd80c1b084bd4347534c0770fe425f707768\` returned **8 commits, 17 changed paths, all documentation/evidence**, no lib/test/web/tool/lockfile modifications. This preserves code identity for the recorded harness, not a new execution at HEAD.
- Original build/source SHA: \`7caaee998251602e72159eeebda61f701bdea270\`. Follow-up execution HEAD: \`d346694ea17a57a093ede203a94c70aa98738f7f\`, with no relevant product source changes as recorded. PWA acceptance appBuildId \`2b515d6c9cf282b2a42b186f45c7b5ea\`, \`main.dart.js\` SHA-256 \`46d9015b61e097713349b9c5bc463e33a3188f65471c6b1d56f646d368dbff76\`. This is a **PWA acceptance/harness artifact** and not a verified NORMAL release archive.
- Device/runtime: iPad Pro 11-inch M5 **Simulator**, iPadOS **26.1 / 23B86**, Safari **26.1**; loopback \`http://127.0.0.1:49331\`. Local Mac host and Safari WebDriver test sessions; not physical iPad, not enterprise enrollment/MDM, not a production HTTPS hostname.
- Exact observed product scope: \`LOGMATE_PERSISTENCE_ACCEPTANCE=true\` bypasses SessionGate and uses a **synthetic unbound owner**. It writes one synthetic Flight with known revision/outbox/page data. It is **not** verified Firebase UID, full Add/Edit/Custom UI, account deletion, LBK export/restore or Manual Sync acceptance.

### 10.2 Claims that now have bounded runtime evidence

| Claim / environment | Observed oracle | Verdict and exact limit |
| --- | --- | --- |
| iPadOS Safari normal tab can run synthetic PWA harness | Safari launched at fresh loopback origin, synthetic Flight \`ACCEPT1\` / revision / pending operation / page shown | **PASS — Safari Simulator harness**, not full product |
| IndexedDB state survives Safari process restart in that normal tab | Same-origin \`logmate_ledger\` database/version2 and read-only raw 21-row hash before/after \`a06c90de776388addc77ddbbf2e585897f5ef7ec208fe024206063d3f3796470\` | **PASS — this simulator/origin/data class**, not storage pressure, origin migration or device loss |
| Cached shell/record can relaunch while test origin server unavailable | Task-owned loopback server stopped; curl exit7; Safari terminated/reopened at root without create flag; synthetic record still shown | **PASS — origin-unavailable relaunch only**; not full network isolation, fresh offline edit, remote Auth or A0–A3 |
| Worker activation in Safari WebDriver context | \`navigator.serviceWorker.ready\` initially returned \`activating\`; explicit statechange observed \`activated\` | **PASS — automation context only** |
| Current document controlled by worker | After navigation/reload, \`navigator.serviceWorker.controller\` script \`/logmate_service_worker.js\`, state \`activated\` | **PASS — automation context only**; do not infer control in the normal Safari tab |
| Secure context on HTTP loopback | \`isSecureContext === true\` in WebDriver | **PASS — loopback potentially trustworthy**; **NOT** TLS, certificate chain or approved HTTPS deployment |
| Synthetic DB survives navigation in WebDriver session | \`entry\` rows 15 before fixture, 19 after; independent \`getAllKeys/getAll\` SHA-256 \`730c2c1363bbec2109a516d7656db4457ebcbd73d5775e31205d31b87761e424\` before/after root re-navigation | **PASS — same automation session/navigation**, not Safari process restart or persistent user data |
| WebDriver UI interaction / accessible content | native accessibility element click returned HTTP400 \`click intercepted\`; DOM text empty, screenshot blank | **INCONCLUSIVE for UI**; no product rendering/accessibility PASS or established product defect |
| Home Screen install / installed storage | Share sheet appeared; installation control inaccessible to automation; no installation | **NOT RUN / NOT VERIFIED** |
| Native iOS/Android app runtime | Builds succeeded, but native artifacts retained production Firebase initialization paths; existing Android app present | **NOT RUN by safety decision**; no native runtime PASS |

### 10.3 New cross-domain diagnostic — WebDriver storage isolation is *expected*, not a PWA partition experiment [SOURCE / CONTRADICTION]

WebKit's primary explanation of iOS Safari WebDriver explicitly states that automation windows have **separate tabs, preferences and persistent storage**, start clean, and their session state is destroyed when the session ends: https://webkit.org/blog/9395/webdriver-is-coming-to-safari-in-ios-13/ (2019-07-08; rechecked 2026-10-27). Apple Safari WebDriver: https://developer.apple.com/documentation/webkit/testing-with-webdriver-in-safari . This directly explains why the normal Safari tab's raw **21-row** store and the WebDriver session's **15→19-row** store must **not** be compared as one database, and why the automation session cannot prove Home Screen PWA storage separation. Different hash methods (raw SQLite bytes vs browser \`getAllKeys/getAll\` JSON) also prohibit direct digest equality comparisons.

**Negative-control rule:** \`Safari normal tab ≠ Safari WebDriver profile ≠ installed Home Screen web app ≠ managed Web Clip\`. Cross-context copying, cookies, origin storage, and independent file recovery each require their own explicit fixture/observations. Do not claim that a blank WebDriver frame is a user-facing blank-screen defect while the normal Safari tab still displays the fixture; investigate render/AX/automation independently.

W3C Secure Contexts treats \`127.0.0.0/8\` as potentially trustworthy, explaining loopback \`isSecureContext=true\` without HTTPS: https://www.w3.org/TR/secure-contexts/ . W3C Service Workers requires secure-context clients but separates registration, activation and current client control: https://www.w3.org/TR/service-workers/ . These standards support interpreting the observations, not a production TLS/Service Worker policy pass. WebKit storage quota/eviction remains independent: https://webkit.org/blog/14403/updates-to-storage-policy/ .

### 10.4 Why installed-PWA/MDM and native safety remain blocked [DEPENDENCY / OPEN]

1. **Installation:** WebDriver is web-content automation, not general-purpose iPad OS UI automation; WebKit documents suppression of system-level actions. Share sheet appearance and an AX/coordinate automation failure do not show lack of platform install support. Need authorized manual or suitable system-level installed-app test, with app identity, launch mode, storage origin and independent readback.
2. **Managed EFB:** The simulator lacks actual supervision/MDM restrictions, enterprise Web Clip payload, managed network path, Open In file custody, device storage pressure and physical lifecycle. No transfer of Safari Simulator PASS to a company EFB.
3. **Authentication:** Harness bypasses Firebase SessionGate. Real verified UID/owner locking, sign-out across contexts, session expiry and provider redirect/popup are untested. The normal Safari synthetic fixture is not real user data.
4. **Offline:** Origin-server outage is weaker than physical network disablement and cannot prove Auth token/remote Sync behavior or an offline edit. Run controlled online→offline→cold-start→edit→restart→rejoin tests with independent record/operation oracle and actual Manual Sync only.
5. **Native Firebase:** Resolved \`firebase_core 4.15.0\` iOS plugin may auto-configure bundled production options during registration; Android merged manifest has \`FirebaseInitProvider\`. Native artifacts were deliberately not installed/launched. A test entrypoint that does not call Firebase in Dart does not prove the native binary is Firebase-isolated. Product Engineering must separately authorize/verify isolated build resources and package identity.
6. **Data safety:** No W-012 37-store LBK restore, W-013 actual external file I/O, W-014 device migration, account deletion, multi-tab replay, storage eviction, rollback or native↔PWA reconciliation was executed. Their existing gates remain OPEN.

### 10.5 Integrated next acceptance campaign, prioritized by information gain [MINTTAP DECISION / VALIDATION PLAN]

**Campaign S1 — exact artifact and reproducibility (Engineering owner, E/C challenge).** Preserve source/build/served hashes, WebDriver capability payload, test origin, fixture seed, fresh profile and oracle. Distinguish harness from NORMAL; capture actual response headers and SW/controller. Positive and negative: wrong artifact, missing worker, uncontrolled initial navigation, worker activating, origin unavailable, cache removed, deliberate fixture mismatch. PASS/FAIL/UNKNOWN per case.

**Campaign S2 — genuine installed Home Screen (A/C/E).** On approved unmanaged physical iPad first, install via user-visible OS path, record manifest identity, launch display mode, fresh DB and cookies, independent file/record sentinel, close/relaunch, origin outage, update and uninstall/reinstall. Do not use WebDriver's temporary store as the pre-install source; protect unique data before destructive tests.

**Campaign S3 — actual managed EFB (E/A/C).** Repeat only after the employer/device policy envelope is documented: supervision/MDM, Safari/Web Clip restrictions, network/proxy/TLS, Files managed/unmanaged destination, permitted app actions, lifecycle and support. A managed Web Clip is a separate installation class and must not inherit unmanaged Home Screen verdicts.

**Campaign S4 — authenticated data and recovery (Engineering + E/C/B).** Verified UID, owner lock, synthetic records with independent IDs, offline mutation/restart, explicit Manual Sync/ACK, export-to-external-file and clean 37-store restore, cancellation/blocked file share, wrong owner and partial failure; require no loss or silent cross-owner import. Reconcile LBK source-cut/currentness and Sync \`unbound/unverified\` semantics from 298/319/521; never infer backup from IndexedDB persistence.

**Campaign S5 — truthful user/measurement transfer (B/D).** Design Studio W121/CD127 retains visual/AX/human gates; do not write "Offline Ready", "Installed", "Backed Up" or "Synced" from harness-only observations. Marketing D8–D10 public PWA/ads claims remain HOLD. Measure each distinct installation/runtime context without flight content, UID, token or identifying payload.

### 10.6 Five-track depth/gate assessment and adjacent-question stop check

- **E primary:** generic Stage 8 high maturity; release-admission/MDM/Auth/backup authority remains the bottleneck. **No production promotion.**
- **A strong source + new bounded simulator runtime:** loopback secure context, worker activation and client control demonstrated in one automation context; installation, OS policy and cross-container behavior remain OPEN.
- **C high pressure:** genuine Safari Simulator harness observations now exist; independent oracles and normal-tab restart hash are useful, but WebDriver AX/render failure, full UI/AT, physical/managed and data-loss negatives remain OPEN.
- **B consumer:** actual UI state and accessible action outcome are missing; Design Studio Stage 3 PRACTICE/W121 and CD127 remain the owners of visual/semantic validation.
- **D consumer/challenger:** observed harness operation is not a public PWA capability claim, install conversion, Store readiness, ad eligibility or user success. Marketing owns promotion policy; Web Manager owns web measurement mechanics.

**Meaningful gate update:** \`Applied Stage 8 ACTIVE · Safari 26.1 Simulator synthetic harness PARTIAL PASS · NORMAL/HTTPS/installed/managed/product data validation OPEN · PWA release HOLD\`. This is stronger evidence than the previous source-only claim but much narrower than an EFB admission. **Adjacent questions checked:** WebDriver profile isolation, loopback secure-context interpretation, worker activation vs control, browser-process restart vs same-session navigation, normal-tab vs automation hash, origin-outage vs network-offline, native Firebase prelaunch and product Work W-012/013/014 sequencing. Further progress requires authorized actual installed/physical/managed/runtime or executable product harness evidence rather than more abstract scenarios. No peer/product repo changes.


---

## 11. Applied cross-target evidence: isolated Native acceptance is not installed-PWA or native↔PWA admission (2026-10-27) [SOURCE / VALIDATION / TRANSFER VALIDATION / CONTRADICTION]

### 11.1 Why this continuation is necessary

The prior §10 established real **iPadOS Safari Simulator** runtime evidence for a **synthetic PWA**. Since that checkpoint, LogMate main acquired a materially different class of evidence: **isolated iOS and Android Native acceptance builds, actual Simulator/Emulator repository reopen observations, and fail-closed native-startup checks**. This is worth admitting into the same release-evidence matrix because it resolves a *native execution safety prerequisite* for eventual PWA↔native recovery/synchronization experiments. It **does not** turn the PWA, installed Home Screen, managed Web Clip, backup, or cross-device sync gates green.

Canonical read-only product comparison, checked 2026-10-27: LogMate \`6180fd80c1b084bd4347534c0770fe425f707768\` → latest \`d3bc214fe9b4b7bf84702f898b4e6993a4127e2f\`, **eight commits ahead**. The 50+ changed paths include native build configuration, acceptance-specific iOS/Android entry points, Dart acceptance guard, focused tests, and execution evidence. Unlike the earlier §10 source-only documentation continuation, **this delta changes product test infrastructure**; it must not be described as docs-only. Source/test observations below are pinned to the recorded execution SHAs, **not a claim that all tests were re-executed at latest main**.

Primary product records:
- [W-031 simulator pre-acceptance and Native follow-up](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-simulator-preacceptance-2026-10-27.md).
- [Initial isolated Native results](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-native-isolation-2026-10-27/results.json) and [subsequent fail-closed results](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/evidence/w031-native-failclosed-2026-10-27/results.json).
- Exact [Dart guarded entrypoint](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/lib/main_l2c_persistence_harness.dart), [iOS native guard](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/ios/Runner/AppDelegate.swift), [Android isolated launcher](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/android/app/src/acceptance/kotlin/app/minttap/logmate/AcceptanceActivity.kt), [artifact verifier](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/tool/verify_native_acceptance.py), [negative startup tests](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/test/debug/native_acceptance_entry_test.dart).

### 11.2 Foundations: distinguish four independent identities [SOURCE / HISTORY / SYNTHESIS]

An OS-installed Native app's **bundle/application ID and app container** are not a web **origin**, and neither is a Firebase UID. A browser's Service Worker registration/CacheStorage/IndexedDB live within its web storage context; a Native app's local repository is governed by its OS package/container. Same human, similar Flutter UI and matching synthetic record fields do not create a shared physical database, common session, or transport channel. A separate acceptance bundle ID deliberately creates a **different** Native app identity and storage boundary.

Relevant authoritative sources, checked 2026-10-27:
- [Apple CFBundleIdentifier](https://developer.apple.com/documentation/BundleResources/Information-Property-List/CFBundleIdentifier) — bundle identity, not web origin.
- [Android manifest and application ID](https://developer.android.com/guide/topics/manifest/manifest-element) — unique app identity, default distinct UID, and a different ID is not an in-place update/data migration.
- [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests) — integration execution scope and platform-specific test runners; a successful build is not an executed user journey.
- [WebKit Safari 17.2 web-app cookie copying](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/) — only cookies can be copied at Home Screen installation; other local website storage is not copied and subsequent storage is separate.
- [WebKit Safari 26.0 Home Screen behavior](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) — user-facing web-app presentation is not an offline or data-transfer guarantee.
- [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) — quota/eviction remain distinct from successful process relaunch.

**Operational rule:** establish an explicit, authenticated and authorized *transfer protocol* (file export/import or a separately validated network/sync mechanism) before claiming that a Native record can appear in the PWA or vice versa. Matching Dart repository models are a potential compatibility input, not transfer proof.

### 11.3 What the new execution evidence actually proves [VALIDATION]

| Boundary | Recorded positive observation | Scope and remaining unknown |
| --- | --- | --- |
| Artifact isolation | Acceptance identity \`app.minttap.logmate.acceptance\` on both platforms; iOS bundle excludes GoogleService-Info.plist/OAuth keys; Android package excludes FirebaseInitProvider/Google Services resources; production artifacts rejected by acceptance checker | **PASS for inspected artifacts**, not proof of all runtime network effects, physical devices or production authentication |
| Native startup admission | Dart compile-time \`LOGMATE_NATIVE_ACCEPTANCE\` guard, typed MethodChannel handshake requiring exact ID, \`firebaseApps=0\`, \`firebaseOptionsPresent=false\`; iOS native preconditions and selective plugin registration; Android selective JNI plugin registration and Firebase observation | Guarded test route is **source-supported**; no automatic implication for normal Production entrypoint or PWA |
| Negative guard matrix | Final fail-closed tests: flags omitted **19**, false **19**, true-focused **39**, all completed successfully (total **77 executions**, including repeated helper checks); missing/invalid handshake cases reject before UI/repository access in mocked tests | **PASS for bounded focused tests**; 77 is not 77 independent product journeys, and mocked guard checks are not an OS isolation audit |
| iOS actual Native persistence | iOS 26.1 iPhone Simulator acceptance app: prior real UI Save-button fixture retained; newer acceptance build reopened same synthetic owner/record and matched stable record/revision/totals/pending data after process termination/relaunch | **PASS for bounded iOS Simulator repository re-entry**; later build did not repeat Save click; not physical device, Firebase, complete UI E2E, OS reboot or 37-store LBK |
| Android actual Native persistence | Android 16/API36 read-only Emulator: separate acceptance UID from existing production UID, synthetic record written through guarded local debugger harness; force-stop/cold-start reread matched fixture | **PASS for bounded Emulator repository re-entry**, **not UI Save-button PASS**; read-only AVD overlay cannot establish data survival across VM shutdown |
| Production defaults | Normal iOS release/no-codesign and Android debug builds compiled; default production identities/plugins preserved; checker rejected production binaries for acceptance installation | **BUILD / negative-artifact PASS only**; production binaries were **not installed/launched** |
| Safari synthetic PWA | Prior §10 iPadOS 26.1 normal Safari tab and separate WebDriver profile have bounded offline/restart/IndexedDB/Worker evidence | **Different platform and different data stores**; no Native↔PWA communication or installed PWA proof |

The final fail-closed result file reports source SHA \`67d8cc4c642cf7de9995d659474a0bfbcea8470e\` for its compile/test steps. The initial Native isolation evidence was recorded on earlier source revisions, including \`af481d6c...\` iOS and \`db9cab11...\` Android. Preserve those execution identities and the product document's correction history; do not retrospectively relabel all observations as one immutable binary.

### 11.4 Security trust-boundary critique and counterexamples [SYNTHESIS / CONTRADICTION]

1. **Compile-time flag ≠ isolation by itself.** A Dart-only test entrypoint was previously insufficient because the native plugin registrant could initialize bundled Firebase settings before Dart ran. The newer acceptance target addresses that through separate OS identity, resource exclusion, native plugin registration and runtime handshake. Its correctness still depends on the *built artifact* matching the inspected configuration.
2. **No Firebase apps at startup ≠ no network ever.** It is a narrow initialization observation; it does not prove absence of all future SDK/network operations, permissions, telemetry or platform calls. A full network/credential trace would be a different oracle.
3. **Production artifact rejected by test checker ≠ production app unusable.** This is an intentional safety negative control. Production builds compiled; neither a production Firebase run nor a production app defect follows.
4. **Native repository persistence ≠ web IndexedDB persistence.** Both may use Sembast-like domain records but have different storage engines, OS identities, failure modes, migrations and backup custody.
5. **Same fixture after process restart ≠ storage durability across OS eviction/restore.** Physical storage pressure, device reprovisioning, browser website-data deletion, reinstall and migration are distinct.
6. **Acceptance package cannot stand in for production package data migration.** Android explicitly treats a changed app ID as a different app. iOS bundle identity is also independent. A clean acceptance container is *safer for testing* but does not prove production user-data preservation during upgrade.
7. **Synthetic unbound owner ≠ authenticated Firebase UID.** Owner lock, logout, token refresh, account deletion, cross-owner transfer and Sync authorization remain unexecuted.
8. **A normal browser tab ≠ installed Home Screen ≠ managed Web Clip.** Safari WebDriver's temporary profile is yet another context; §10's distinct 21-row/19-row oracles must remain distinct.
9. **Installed PWA presentation ≠ device-to-device Sync.** No discovered peer, approved transport, credential binding, conflict resolution, background execution or convergence is established by the Native or Safari fixture.
10. **77 green focused test executions ≠ full CI release certification.** Product record explicitly says full Flutter suite and GitHub CI were not run for the final Native checkpoint; the two production binaries were compiled but not launched.

### 11.5 Transfer to the EFB/PWA release admission matrix [MINTTAP DECISION / DEPENDENCY]

**New bounded promotion:** a dedicated *Native test-environment safety and synthetic local-reopen* subgate can now cite executed iOS/Android Simulator/Emulator evidence. This is a prerequisite for safe future dual-endpoint testing, not the same as PWA validation. The previous Safari synthetic partial PASS is unchanged. **No composite PWA release promotion.**

| Claim requested | Evidence tier now | Required independent next proof |
| --- | --- | --- |
| Safe isolated Native synthetic test endpoints | Source + artifact checks + bounded Native runtime **PARTIAL PASS** | Exact approved binary/hash, platform network/Firebase observation, repeated cold starts and negative fixture tests |
| Safari normal-tab synthetic offline/local state | §10 Simulator **PARTIAL PASS** | Real authenticated NORMAL PWA, cold offline edits, independent data hashes, actual HTTPS |
| Installed Home Screen / managed Web Clip | **OPEN** | Manual install/launch, storage partition/eviction, management payload, offline/restart and file destination |
| Native↔PWA record transfer / unattended Sync | **OPEN** | Explicit transport/file path, UID/peer authority, idempotent transfer, conflict/ACK and failure/rejoin observations |
| Full 37-store LBK save/readback/restore | **OPEN** | W-012 repository restore → W-013 external file UX → W-014 device transfer; independent source-cut and owner checks |
| Service Worker OLD/NEW update safety | §519 synthetic hosted Chromium **PASS only for fixture** | Exact NORMAL two-generation Worker, cached HTML/JS, 37-store data, rollback/restart/invalid-message negative controls |
| Production release / EFB readiness | **HOLD** | Source→artifact→served bytes/headers→browser/managed device→authenticated data→recovery and support custody |

**Negative decision:** do not use Native acceptance package data to assert that a production Native user can hand records to Safari, Home Screen PWA, or managed EFB iPad. In fact, deliberate isolation means the acceptance data is in a separate Native container. A future migration/sync test must explicitly create and verify a transfer artifact or channel.

### 11.6 Falsifiable integrated acceptance packet N1–N16 [VALIDATION PLAN / DEPENDENCY]

These are **proposed tests, NOT RUN here**. They extend §10 S1–S5 and 298/319/519/521 without introducing another generic primer.

| ID | Independent oracle / positive + negative control | Owner |
| --- | --- | --- |
| N1 | Pin final test source, binary digest, build flavor, native ID, signed entitlement/manifest and launch PID; wrong artifact must be rejected | Engineering / E |
| N2 | On Native startup observe zero Firebase apps and no packaged production options; inject invalid handshake and verify no repository access | Engineering / C |
| N3 | Capture redacted network destinations during acceptance; distinguish no observed Firebase traffic from a universal network-isolation claim | E / C |
| N4 | Repeat iOS process-restart repository readback with exact IDs/revisions/pending operations; corrupt one expected value and require FAIL | C |
| N5 | Repeat Android force-stop readback, then separately reboot a **disposable** AVD and check persistence; preserve base production package | C |
| N6 | Assert production build cannot be installed by acceptance runner; production default build remains buildable without acceptance contamination | Engineering / E |
| N7 | Re-run §10 Safari normal-tab origin outage and process restart on pinned harness; no cross-profile DB/hash comparison | A / C |
| N8 | On approved physical iPad manually install Home Screen app and test independent post-install origin/cookie/IndexedDB/CacheStorage fixtures | A / C |
| N9 | On representative managed EFB, document MDM Web Clip policy, permitted file destination and network/TLS; denial must not be reported as browser lack of support | E / A |
| N10 | Verify Native→PWA transfer via an explicit authorized file or transport, exact record/revision identity, wrong-owner rejection and duplicate replay | Engineering / E |
| N11 | Verify PWA→Native transfer independently; simulate interrupted transfer, retry, conflict and acknowledgement without duplicate totals | Engineering / C |
| N12 | Separate online/offline/edit/restart/rejoin/Manual Sync; no background/unattended claim without observed execution opportunity and network path | A / E |
| N13 | Save actual LBK to external file, read it independently, restore 37 stores into empty same-UID destination and reject stale/wrong-owner assumptions | Engineering / E |
| N14 | Combine a waiting NEW Worker and OLD-controlled client with actual NORMAL shell/JS and nonempty synthetic ledger; preserve data on rollback | A / C / E |
| N15 | Accessible UI state must distinguish "local saved", "backup file verified", "sync acknowledged", "offline ready" and "unknown"; human/AT proof separate | B / Design Studio |
| N16 | Instrument install/transfer/recovery outcomes with privacy-minimized event categories only; exclude UID, flight payload, credentials and private record IDs | D / Marketing |

**Failure-handling rule:** a negative control that does not actually execute is **NOT RUN**, not PASS. Record source/artifact/environment/oracle identity, observed result and contradiction separately. Avoid destructive reset of unique pilot data and avoid production Firebase activation for synthetic testing.

### 11.7 Five-track allocation and specialist boundary [TRANSFER VALIDATION]

- **E — primary Stage 8 bottleneck:** admission of isolated Native test endpoints, credential/trust boundaries, deployment identity, data custody and rollback. Native isolation reduces *test risk*, not production security proof.
- **A — platform dependency:** browser origin, Safari profile/Home Screen/Web Clip and Worker control mechanics. Native OS package/container is a different authority and should not be described as browser storage.
- **C — high validation pressure:** independently check test fixture, process-restart and negative control semantics; Native 77/77 focused execution and Safari harness are separate verdict classes.
- **B — consuming Design Studio W121/CD127:** user-facing local-save/recovery/offline state accuracy and accessible action verification; Design Studio Stage 3 runtime/AT gate still OPEN.
- **D — consuming Marketing D8–D10:** no public claim that PWA↔Native Sync, managed-EFB readiness, file backup, offline editing or ad serving is complete. Track D owns privacy-minimized web measurement mechanics, not promotion strategy.
- **Software Engineering Studio:** canonical general mobile build/test and executable test semantics (M006/Q006); Web Manager owns *web/PWA transfer and release-admission requirements*. Engineering's current progress/STATUS remains Stage 1 foundations, and this product result is not an automatic Studio curriculum gate change.

### 11.8 Meaningful checkpoint and adjacent-question check

Completed in one integrated continuation: (1) exact product HEAD delta, (2) Native build identity, (3) iOS plugin/Firebase boundary, (4) Android plugin/Firebase boundary, (5) compile-time vs runtime fail-closed guards, (6) 77-run test semantic accounting, (7) actual iOS reopen, (8) actual Android reopen and ephemeral overlay limit, (9) production default negative-control interpretation, (10) Safari profile/installed separation, (11) native↔PWA transfer/backup dependency, and (12) cross-track acceptance oracles. **Next useful evidence is an actual authorized dual-endpoint transfer/installed PWA/managed-device run, not additional speculative transfer diagrams.**

**Gate:** Applied Stage 8 ACTIVE · isolated Native Simulator/Emulator synthetic local-reopen PARTIAL PASS · Safari Simulator synthetic PWA PARTIAL PASS · installed/NORMAL/managed-EFB/native↔PWA transfer/37-store LBK/production validation OPEN · PWA release HOLD. No product or peer repository changes.
