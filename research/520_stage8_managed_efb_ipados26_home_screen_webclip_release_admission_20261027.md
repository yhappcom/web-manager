# 520 — Stage 8 managed-EFB PWA admission: iPadOS 26 Home Screen, managed Web Clips, offline and release custody

Date: **2026-10-27**. State: **SOURCE + SYNTHESIS + product-source transfer / generic platform decision gate; actual NORMAL artifact, HTTPS, browser, managed-device and ledger validation OPEN**. Owner: **E Web Architecture, Security & Operations**, with **A** platform prerequisites, **C** acceptance evidence, **B** task/recovery semantics, **D** claim/measurement controls. This is a **major cross-track domain integration**, not a sixth PWA track or an implementation change.

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
