# 507 — Stage 8: Managed iPad Web Clip vs Home Screen PWA — installation, storage identity, offline custody and Sync authority

Date: 2026-10-24 (Asia/Seoul)  
Evidence status: **SOURCE / SYNTHESIS / MINTTAP DECISION / OPEN / DEPENDENCY / VALIDATION / CHANGE WATCH / TRANSFER VALIDATION / CONTRADICTION**  
Curriculum: **Stage 8 applied Security / Privacy / Trust** (generic sequential Stages 1–12 already completed; not production certification).  
Primary owner: **Track E** (managed deployment, trust, durability, incident/backup lifecycle). Track A owns platform mechanics; C owns device/runtime proof; B and D consume the verified constraints.  
Product boundaries: **Web Manager read/write; LogMate, Design Studio, Software Engineering Studio and Marketing Manager read-only**. No device, production, backend or managed-MDM validation occurred.

## 1. Source and dependency refresh [SOURCE]

At the start of this cycle, reread current `yhappcom/web-manager` `main@52db083ca2632a506d61af9ae25418b2c1a02611` `AGENTS.md`, `SPECIALIST_TRACKS.md`, `LEARNING_ROADMAP.md`, `STATUS.md`, `research/README.md`, current integrated 506 (including §10) and latest commits. Read the applicable Design Studio W121, Engineering D006 and Marketing 438 as **bounded transfers**, not replacements for their owners. LogMate current observed `main@97a9a6613fdd976a7b90ac50b2a8210a894420b5` (PR #16 L-2C and PR #17 Flutter/CI); no new product HEAD or runtime evidence observed in this cycle. Prior 506 source-level 37-store v17 restore and recovery-hold collision remains **OPEN** for compiled execution. Existing 291 managed-iPad policy envelope is an input, not proof that any fleet is configured.

**Why this adjacent research has high information gain:** Earlier 506 concentrated on deterministic recovery-evidence collision and browser CI. A different release blocker is now directly resolvable by primary evidence: **company-managed iPad deployment is not interchangeable with a user-installed Home Screen web app**. The platform's iOS/iPadOS 26 install UI changed; management-delivered Web Clips remain a separate configuration path. Treating those as one installation state could make a supposedly tested offline/backup flow apply to the wrong data container, launch mode or policy. This is a material cross-track Stage-8 trust boundary, not another generic PWA primer.

**Primary source register (reviewed 2026-10-24):**
1. Apple Deployment, *Web Clips device management payload settings* (published 2022-10-24; rechecked): https://support.apple.com/en-gb/guide/deployment/depbc7c7808/web — `com.apple.webClip.managed`, iOS/iPadOS/Shared iPad, URL/label, removable/full-screen options, Safari restricted/hidden interplay, provider-specific implementation caveat.
2. Apple Developer, *HomeScreenLayout* and *IconItem*: https://developer.apple.com/documentation/devicemanagement/homescreenlayout/ and https://developer.apple.com/documentation/devicemanagement/homescreenlayout/iconitem — a Home Screen layout can place a WebClip but **does not create it**; separate WebClip payload is required.
3. WebKit, *WebKit Features in Safari 26.0* (2025 release description): https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ — iOS/iPadOS 26 user Add-to-Home-Screen defaults to **Open as Web App**, with an opt-out; no manifest/Service Worker prerequisite merely to add a website as a web app.
4. Apple iPad User Guide, *Turn a website into an app in Safari on iPad*: https://support.apple.com/en-mide/guide/ipad/ipad8f1f7a29/ipados — user-initiated Add to Home Screen / Open as Web App, device-local icon.
5. WebKit, *WebKit Features in Safari 17.2* (2023-12-11): https://webkit.org/blog/14787/webkit-features-in-safari-17-2/ — when **user** adds Home Screen web app, current login cookies may be copied; **no other local storage is copied**; subsequent website data is not shared. Do not automatically extend this claim to MDM-created Web Clips without a device test.
6. WebKit, *Updates to Storage Policy* (2023-08-10): https://webkit.org/blog/14403/updates-to-storage-policy/ — quota/eviction, `navigator.storage.estimate/persisted/persist`, origin-wide eviction and best-effort defaults; standalone Home Screen web apps receive browser-app quota class but this is not backup or durability certification.
7. WebKit, *Web Push for Web Apps on iOS and iPadOS*: https://webkit.org/blog/13878/ — Home Screen web-app push context; does not establish unattended device-to-device Sync.
8. MDN, *Background Synchronization API*: https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API — **limited availability**, secure context and service-worker dependency. Periodic background sync is also limited/experimental: https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API.
9. MDN, *Using Service Workers* and *Secure Contexts*: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers and https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts — HTTPS/secure-context, Worker registration, lifecycle/cache.
10. Prior project evidence: Web Manager 506 (37-store restore, copied-but-unverified Sync authority), Design Studio W121 (runtime/human/AT proof), Engineering D006 (cursor/apply atomicity), Marketing 438 (conditional ad-free PWA; no false Sync-complete claim).

These documents have different temporal scope. Apple iPadOS 26 user-install behavior is **not retroactively applicable** to an older fleet; WebKit's 2023 storage policy is a platform model, not a 2026 fleet test. All OS/MDM capability combinations are **CHANGE WATCH**.

## 2. History/problem → principle → platform boundary [SYNTHESIS]

Historically a Home Screen icon could be a bookmark opening in a browser, or a standalone web app when declared capable. WebKit states iOS/iPadOS 26 changes **user-initiated** Add to Home Screen so sites open as web apps by default, with a user choice to open as a browser bookmark. This relaxes an *installation presentation gate*, not HTTPS, Worker, Cache, IndexedDB, authentication, durable backup, MDM enrollment or Sync semantics.

An enterprise administrator can instead deploy a **managed Web Clip** configuration profile. Apple documents `Full screen` to open the URL as a web app without URL/search bar and describes the special case where Safari is hidden and restricted. The presence of a managed icon or full-screen launch is **not evidence** that the exact same browser data container, login bootstrap, manifest semantics, push permission, Worker lifecycle or uninstall behavior was exercised as user Add to Home Screen.

**Trust decomposition:**
- **Icon provisioned**: MDM profile exists and a Home Screen entry is visible.
- **Launch mode verified**: Safari tab, user Home Screen web app, or managed Web Clip/full-screen behavior identified on the actual device.
- **Secure origin reachable**: HTTPS and certificate/trust/network restrictions verified for the *actual URL*, redirects, resources and authentication endpoints.
- **Offline shell available**: a successfully installed/controlling Service Worker and complete required cached app shell/assets/routes verified after network removal.
- **Local ledger available**: real application IndexedDB/Sembast state loaded and usable under the *same launch context*.
- **Custody durable**: unique data independently exported and recoverably restored after storage loss or profile/management changes.
- **Remote Sync authorized**: authenticated server Receipt/cursor/convergence verified; neither connectivity nor copied Sync rows suffice.

None of these propositions implies the next. In particular, **`installable` ≠ `installed` ≠ `offline-ready` ≠ `local-data-durable` ≠ `Sync-authorized`**.

## 3. Four deployment/launch paths are separate test populations [SOURCE / MINTTAP DECISION]

| Context | Primary-source basis | What can be claimed now | Must be independently tested |
| --- | --- | --- | --- |
| A. Safari tab on company iPad | Browser Web APIs; MDM may restrict Safari | Web page can run subject to policies; no user-installed standalone inference | HTTPS redirects, authentication, Service Worker control, storage partition, offline navigation, rejoin |
| B. User Add to Home Screen web app | WebKit iOS/iPadOS 26 user UI, Apple iPad guide | On iPadOS 26, user Add to Home Screen defaults to web-app mode with opt-out; earlier OS rules differ | Actual OS/version, user ability to add, manifest/launch URL, storage continuity, cookie transfer, offline data |
| C. MDM-managed Web Clip, full-screen off | Apple Web Clips payload | Admin can provision Web Clip URL/icon, subject to enrollment/provider and Safari restrictions | Whether it opens Safari tab or another context under exact policy; local data partition and auth continuity |
| D. MDM-managed Web Clip, full-screen on | Apple Web Clips payload | Full-screen web-app-like launch is an available configuration; necessary with Safari hidden/restricted per Apple guide | Exact runtime/Worker/storage identity, uninstall/reinstall/profile removal, no URL chrome, navigation/recovery UX, offline restart |

**Contradiction to reject:** “iPadOS 26 lets users add any site as a web app, therefore the airline can deploy the LogMate PWA on managed iPads and it will retain Safari data.” The first clause concerns a user UI capability; the second assumes management permission, delivery, launch identity, data migration and durability. No cited primary source composes these claims.

**MDM profile identity:** The Apple HomeScreenLayout IconItem with `Type=WebClip` references an existing Web Clip URL; it **does not install/create** the Web Clip. A fleet rollout must verify the Web Clip payload and layout separately. If the profile is non-removable, removal may require removing the profile; do not infer whether app data survives that removal.

## 4. Storage identity, initial auth and reinstall: hidden failure modes [SOURCE / SYNTHESIS]

**WebKit 17.2 user-install boundary:** Current cookies may be copied from Safari/browser to a newly created Home Screen web app, including cookie-based login state; IndexedDB, Cache Storage and other local storage **are not copied**. After installation the data stores are not shared. Therefore:
1. A Safari-tab flight entered before Home Screen installation must **not** be assumed to appear in the newly installed app. If LogMate stores unique offline records locally, an explicit, verified export/import or authenticated server Sync is required for migration. In this project, remote Sync remains unverified; use independent backup/restore only after its own validation.
2. Cookie bootstrap is not a fresh authorization grant. Validate cookie scope, SameSite/session expiration, sign-out, offline owner-lock behavior and device/organizational policy before allowing sensitive operations.
3. This cookie-copy statement is specifically for **user-created Home Screen web apps**. Whether a managed Web Clip uses the same bootstrap/partition behavior is **OPEN**; test it rather than silently transferring the rule.
4. Installing, changing, removing or re-provisioning a Web Clip cannot be used as a “safe repair” until preservation of unique offline data has been independently established.

**Storage policy boundary:** WebKit's origin quota is a *ceiling*; `estimate()` is an estimate; `persist()` is heuristically granted or denied. By default origin data is best-effort and can be evicted under storage pressure or quota conditions, commonly origin-wide. A persistent grant is not an independently recoverable backup, and quota headroom does not prove durability. Cache Storage (offline shell) and IndexedDB (ledger) are different logical stores but may share an origin-wide loss event. An installed Home Screen context's quota class does not establish which storage container an MDM Web Clip actually uses.

**Operational ordering for irreplaceable data:** preserve verified export and owner evidence → verify destination/restore semantic oracle and fresh replica → check locked/unverified Sync state → only then consider reinstall/profile removal/clear-data/upgrade repair. A failed export or collision-rejected restore is a **recovery hold**, not an instruction to delete the old app.

## 5. Offline EFB workflow and synchronization boundaries [MINTTAP DECISION / DEPENDENCY]

For a company iPad that may be disconnected in flight:
- **Local capture/read** can be a product goal after exact device and owner-lock testing; do not imply server ACK.
- **Network rejoin** does not prove HTTPS endpoint reachability, current authentication, authorization, stream binding, receipt admission or convergence. Native phone ↔ iPad transfer requires independently verified discovery/transport/security/protocol paths; no unattended peer-to-peer path is assumed.
- **Foreground explicit Sync** is the conservative architecture candidate until a concrete runtime and organizational policy establish background execution opportunity. The MDN Background Sync API is not Baseline; the existence of a Service Worker or Web Push is not a background-Sync SLA.
- **Worker update** changes fetch handling/cached shell generation, not the already-running Dart/JS generation, Sembast capability or server authority. A page can remain stale while a newer Worker activates. Protect local unique data before forced reload and revalidate delayed operations.
- **A Web Clip with no browser URL bar** has special phishing/recovery/diagnostic UX obligations: show trustworthy product identity, origin/help diagnostics where safe, owner/account context, version, local/export/Sync states and a non-destructive recovery route. Design Studio owns the actual accessible presentation; do not display credentials, tokens, UIDs or flight payloads in logs.

**State labels for transfer to B:** `Installed / launch verified`, `Offline shell ready`, `Local saved`, `Export verified`, `Restore rejected—original preserved`, `Restored / owner locked / Sync unverified`, `Queued`, `Server acknowledged`, `Converged`. These are separate claims, not one green status indicator.

## 6. Engineering/device falsification campaign [VALIDATION — NOT EXECUTED]

**Evidence envelope per run:** exact LogMate commit + built artifact SHA-256; origin/redirect chain; manifest/Worker script hashes; iPad model and iPadOS/Safari/WebKit versions; supervised/shared/enrollment class; MDM vendor and policy profile ID/revision (sanitized); Web Clip payload fields including FullScreen/IsRemovable and Safari restrictions; network/VPN/filter/cert envelope; launch context; storage API support/values; test fixture digest and non-sensitive counts; timestamp and observer; expected/actual; rollback/recovery evidence. Never upload real flight data, cookies, UID, bearer tokens or raw personal backups.

| ID | Test / controlled perturbation | Pass criterion (no inference from a different context) |
| --- | --- | --- |
| I01 | iPadOS 26 user Add to Home Screen, Open as Web App on/off | Correct launch classification; opt-out documented; no false claim that manifest/Worker installed |
| I02 | Older iPadOS baseline with same origin | OS-version-specific behavior recorded; no 26-to-old transfer |
| I03 | Managed Web Clip FullScreen=false, Safari allowed | Actual launch context and origin/partition documented |
| I04 | Managed Web Clip FullScreen=true, Safari hidden/restricted | Launch under approved MDM policy or explicit blocked verdict; never assumed |
| I05 | HomeScreenLayout WebClip reference without WebClip payload | No false assumption that layout alone installs the icon |
| I06 | Safari tab seeds synthetic IndexedDB; user installs Home Screen app | No unsupported automatic ledger migration; cookie and non-cookie data inspected separately |
| I07 | Managed Web Clip install with preexisting Safari synthetic data | Actual data-container/bootstrap behavior measured; **no automatic 17.2 user-install extrapolation** |
| I08 | HTTPS redirect/cert/VPN/content-filter policy change while offline | Cached shell vs authentication/remote admission distinguished; safe blocked/recovery state |
| I09 | Fresh launch offline after successful Worker control and cache prime | Required routes/assets/ledger open in exact context; no remote-success claim |
| I10 | Storage pressure, quota exhaustion, persisted() false/true | Recoverable error path, no fabricated durable guarantee; independent backup available |
| I11 | Web Clip profile removal/reinstall and app update | Pre/post local fixture and backup evidence; no destructive repair without export |
| I12 | Browser/process kill, device restart, extended dormancy | Same-context data verified with hashes and semantic oracle; process restart ≠ independent backup |
| I13 | v16→v17 stale page + Worker replacement | Old/new build IDs, guarded mutations, no lost unique records; M01–M12 handoff |
| I14 | 37-store v17 LBK export/restore with source cursor/holds | Semantic 37-store oracle, new replica, locked owner, unbound/unverified Sync; R03/R04 collision control |
| I15 | Wi-Fi/hotspot/VPN reconnect and phone proximity | Transport reachability measured; explicit Sync only; no unattended peer-sync assertion |
| I16 | Keyboard/VoiceOver/reduced motion/zoom, error and restore states | Accessible status/recovery and no hidden success; Design Studio/human/AT proof |

**Negative controls:** an icon visible but no offline shell; Service Worker registered but no controlling client; manifest present but Web Clip opens in Safari; cookie copied but IndexedDB absent; `persisted=true` but independent backup missing; local Outbox eligible but server Receipt absent; remote ACK asserted from restored source Receipt; process-reopen test labeled power-loss durability; management profile removed before verified export. All must prevent production PASS.

**Adjudication tiers:** DOCUMENTED PLATFORM CAPABILITY (Apple/WebKit) → EXACT POLICY/DEVICE CONFIGURATION OBSERVED → EXACT BUILD + LAUNCH CONTEXT RUNTIME OBSERVED → CRASH/LOSS/RESTORE RECOVERY VERIFIED → REPRESENTATIVE MANAGED FLEET + OPERATIONAL SUPPORT VERIFIED. No automatic promotion between tiers. A user-owned iPad result is not a company managed-iPad result; a Safari-tab result is not a Web Clip result.

## 7. Five-track integration and dependency pressure [TRANSFER VALIDATION]

| Track | Maturity / gap | Ownership and next dependency |
| --- | --- | --- |
| **E — primary bottleneck** | Static LogMate 506 trust/reset/collision evidence plus Apple MDM source; no real fleet/restore proof | Own policy envelope, data custody, profile removal/update/incident sequence, no destructive repair, release hold |
| **A — critical prerequisite** | Secure-context/Worker, Safari 26 install UI, Safari 17.2 cookie boundary, WebKit storage policy source | Own launch/storage partition/Worker/browser vs Web Clip mechanics; confirm exact iPadOS 26 and MDM behavior on device |
| **C — high validation pressure** | Existing Chrome L-2C source tests and semantic 37-store contract; no managed iPad run | Own I01–I16 provenance, fault/device/AT tests and negative controls; do not promote source documentation to runtime PASS |
| **B — dependent** | Existing recovery-state IA; Design Studio W121 requires actual human/AT rendering | Own trustworthy task continuity and recovery copy for full-screen no-URL launch, distinct local/export/ACK states |
| **D — dependent/challenger** | No representative deployed analytics or publisher approval | Own privacy-minimized counts for launch context, offline/export/recovery and sync outcome; no tracking SDK or ad injected into protected PWA without separate approval |

**Engineering D006 transfer:** Atomic cursor+apply is required for future inbound Sync; neither it nor Sembast transaction success repairs cross-store recovery-hold key collisions. Engineering owns actual LogMate adapter, test integration, CI and server ACK implementation.  
**Design Studio W121 transfer:** Human/AT/physical-runtime acceptance must use the exact device and launch context, not pre-runtime mockups.  
**Marketing 438 transfer:** A managed offline EFB-like PWA is conditionally ad-free for initial release; installed Web Clip capability is not permission for AdSense, popup ads or a public “seamless Sync” claim.

## 8. Operational decision, change watch and next checkpoint

**MINTTAP DECISION (provisional, evidence-bound):** Treat **managed Web Clip** and **user Home Screen web app** as separate deployable products for testing, support and recovery even if they share URL and web code. A company-managed EFB rollout is not approved merely because iPadOS 26 can display any site as a web app. Choose a candidate MDM delivery mode only after exact organizational policy evidence, storage/owner identity behavior and non-destructive recovery are observed. Until then, foreground/manual Sync and verified independent backup are the conservative architectural assumptions.

**CHANGE WATCH:** iPadOS 26+ Home Screen behavior and user opt-out; MDM vendor's implementation of Web Clip/full-screen/Safari restrictions; Shared iPad policies; cookie bootstrap; storage partition, quota/persistence/eviction; Worker/background API support; network content filters and certificate deployment. Record OS build, MDM profile revision and date with every result. A standards-based web API does not imply the managed policy permits it.

**OPEN:** actual airline/company enrollment/supervision and device policy; Safari restriction; allowed Web Clip payload; deployed origin/cert/network; exact LogMate web build and Worker; current Chrome 37-store restore; v16/v17 two-binary test; R03/R04 collision execution/fix; Web Clip vs user-installed data-container comparison; cookie/owner-lock continuity; physical managed-iPad offline/dormancy/storage/backup recovery; native phone transfer; authenticated server Receipt. No production fact is inferred.

**VALIDATION verdict (2026-10-24):** Primary platform **SOURCE VERIFIED** for documented user-install, Web Clip, storage and background capability boundaries; proposed cross-context non-transfer and I01–I16 are **SYNTHESIS / VALIDATION SPEC**, not executed evidence. **Stage 8 applied security remains active; Track E primary bottleneck, A/C critical dependencies; Production validation OPEN; PWA release HOLD.**

**Adjacent-question checkpoint:** This bundle resolves the otherwise ambiguous managed Web Clip vs user Home Screen installation and storage-transfer claims and supplies an exact 16-case falsification plan. The next materially different question is **runtime evidence**: Engineering-owned R03/R04/R05/R11 and 37-store Chrome execution, then a permitted MDM-enrolled iPad matrix. Additional source-only “PWA installability” primers would not advance the gate.
