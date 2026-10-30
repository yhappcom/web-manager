# 530 — Stage 8 PWA install identity, origin migration and EFB storage custody (integrated)

Evidence date: **2026-10-30**. Status: **SOURCE / SYNTHESIS / PROJECT TRANSFER / VALIDATION DEFINED NOT RUN / CHANGE WATCH**. Primary owner: **Track A — Web Platform & Browser**, with Track E security/operations dependency; B/C/D consume the platform contract. This is a substantial new platform-and-origin domain, not an implementation request. Canonical Web Manager baseline: main@c2c9d7a25666e8fe8fd62855c19c9de13bbbcc72. LogMate product source: **read-only main@9cc0cd432a317d5dfebbe90e318fb219e53e024a**.

## 1. Why install identity is a security and durability topic [HISTORY / PRINCIPLE]

A Home Screen icon, an installed web app identity, a URL origin, a service-worker registration scope, a browser website-data container, an authenticated Firebase UID, and a local LogMate replica ID are **different identifiers**. They do not become one durable storage authority merely because the same app icon is displayed. Historical AppCache-era assumptions that “saved to Home Screen” implied offline operation were unsound; Service Workers give explicit programmable network control, but even a correctly installed worker does not make browser-managed data immune to quota eviction, app removal, OS policy or separate container state.

The Web App Manifest standard introduced declarative installed-app metadata. The later manifest **id** member separates app identity from a mutable launch URL. Safari's historical Home Screen installation heuristics also evolved. The operational consequence for an offline-first flight logbook is severe: a user may install a perfectly valid icon, then discover an empty *different* storage container, an unavailable offline shell, a different account, or a missing backup. None of those outcomes can be inferred or excluded from the presence of the icon.

**Trust separation:** install identity identifies an app presentation; origin governs web storage/security boundaries; SW scope governs fetch interception; a local owner/replica record governs product data provenance; a remote deletion receipt governs server erasure. Do not use one as a substitute for another.

## 2. Safari/iPadOS 26 changes the installation gate, not the offline gate [SOURCE / CHANGE WATCH]

WebKit's Safari 26.0 announcement explicitly says **iOS 26 and iPadOS 26 default to “Open as Web App” for any website added to Home Screen**; users may turn it off and create a browser bookmark instead. WebKit calls this zero Safari “installability” requirements. This is a **Safari/WebKit OS-platform behavior**, not a W3C requirement, not a guarantee for every older iPadOS release, and not evidence of permission on a managed EFB.

The same primary source says the manifest remains useful for metadata, and Service Workers remain useful for offline experience. Therefore “can add any URL to Home Screen” is **not** equivalent to “LogMate has a verified complete precache,” “can run without network,” “has a durable IndexedDB,” or “is permitted by airline device policy.” Installation, first-run readiness, offline readiness, local-data custody and independent export are five separate gates.

Primary: [WebKit — Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) (checked 2026-10-30). Earlier iOS/iPadOS 16.4 WebKit support for manifest id, multiple installs and Web Push: [WebKit 16.4](https://webkit.org/blog/13878/). Treat OS-version, user toggle and enterprise configuration as CHANGE WATCH.

## 3. Chromium installation is a different capability contract [SOURCE / CONTRADICTION]

Chrome's historical manifest install audits listed name/short_name, 192/512 icons, start_url, display and prefer_related_applications. However Chrome later **removed the fetch-handler Service Worker requirement for installation from its menu** (Android 108 / desktop 112) and deprecated the Lighthouse PWA installability category. It would be wrong to assert “Chrome always requires a fetch-handler SW to install” or to promote an old Lighthouse badge as the product acceptance oracle.

Current Chromium installation UI, install prompts, manifest parsing and OS integration must be observed in the **specific browser/build**. A user-installed site without a working offline worker can still have an icon. Do not generalize Chrome's beforeinstallprompt to Safari or assume a Chrome prompt on iPadOS.

Primary: [Chrome revised installability criteria](https://developer.chrome.com/blog/update-install-criteria); [Chrome manifest guidance](https://developer.chrome.com/docs/lighthouse/pwa/installable-manifest); [web.dev installation](https://web.dev/learn/pwa/installation). Historical requirements are included to explain change, not to claim current universal gates.

## 4. Exact LogMate manifest and bootstrap inventory [SOURCE / READ-ONLY]

Product files independently read at pinned main:
- [web/manifest.json](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/manifest.json), blob **8225e76f**: name, short_name, relative start_url **"."**, display **standalone**, background/theme colors, description, **orientation portrait-primary**, prefer_related_applications false, 192/512 standard and maskable icons. **No explicit id or scope**.
- [web/index.html](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/index.html), blob **01be7758**: Flutter base-href placeholder, manifest link, mobile-web-app-capable, Apple title and apple-touch-icon, async bootstrap. The page is not a verified served build.
- [web/flutter_bootstrap.js](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/flutter_bootstrap.js), blob **a70625e8**: derives worker URL from document.baseURI, registers **logmate_service_worker.js** with scope equal to base pathname and updateViaCache none, asynchronously initiates precache/promotion, **does not block first paint or engine startup**.
- [Makefile](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/Makefile), blob **42485938**: build-pwa disables Flutter-generated worker, then invokes owned precache generation and artifact verification. [tool/pwa_precache.dart](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/tool/pwa_precache.dart), blob **90a67954**, explicitly copies source manifest into build output and requires shell, font and notice inventories.
- [firebase.json](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/firebase.json), blob **9ac0972e**: Hosting public build/web, wildcard no-store, /auth aliases. No deployment host, base path or actual served headers were verified here.

**Positive:** a manifest and project-owned offline build pipeline exist. **OPEN:** whether deployed manifest/worker bytes match source; exact host, path, HTTPS, SW control, installation permission, data persistence and EFB behavior. Do not claim missing id/scope makes the manifest invalid or that portrait preference is necessarily enforced on iPad.

## 5. Computed app identity and scope: why a path migration matters [STANDARD / REPLICATION MODEL]

MDN and web.dev describe the manifest **id** fallback to start_url when id is absent, and the default **scope** as the directory of start_url when scope is absent. Relative start_url resolves against the manifest URL. For LogMate's current "." start_url, a root-hosted manifest would normally resolve to the root path; a subpath-hosted manifest would resolve to that subpath. **The actual deployed base path is unknown.**

A deterministic standard-URL-resolution fixture (Python urllib.parse.urljoin, **not browser installation**) yielded:

| Hypothetical manifest URL | Effective start_url / fallback identity | Inferred scope |
| --- | --- | --- |
| https://example.test/manifest.json | https://example.test/ | https://example.test/ |
| https://example.test/logmate/manifest.json | https://example.test/logmate/ | https://example.test/logmate/ |
| https://example.test/preview/manifest.json | https://example.test/preview/ | https://example.test/preview/ |

All three resolve correctly, but **are different installed identities/scopes**. Moving LogMate between root, /logmate/ and /preview/ without an explicitly stable identity could cause a browser to treat the new manifest as a different app; this is a **conditional migration risk**, not an observed duplicate install. Actual Chromium computed ID should be captured from DevTools before choosing an id. The standard identity fallback does not guarantee all browsers use it identically.

Sources: [MDN id](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/id), [MDN scope](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/scope), [MDN start_url](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/start_url), [Chrome existing-install id migration](https://developer.chrome.com/docs/capabilities/pwa-manifest-id). **Do not add an arbitrary new id** to a deployed app: Chrome explicitly recommends first reading the computed existing ID to preserve continuity.

## 6. Scope, installed presentation, SW control and account isolation [SYNTHESIS / SECURITY]

Manifest scope describes the **installed presentation/navigation context**. Service Worker registration scope describes which controlled pages can have fetches intercepted. The origin is the storage/security principal. These scopes can overlap without being interchangeable. The current bootstrap sets SW scope from the built page base path, while the manifest omits explicit scope. If the base path changes, **both the installed navigation boundary and worker registration may change**, but the effects on existing installed clients, Cache Storage, IndexedDB and offline routing must be measured independently.

An installed app opened at a deep link, a browser tab at the same host, a second Home Screen copy, and a different-origin staging app may have different data custody. An identity label does not authorize automatic transfer of one user's logbook to another installation or native device. The owner-A deletion and 37-store parity concerns in [529](529_stage8_pwa_owner_deletion_backup_mdm_custody_20261030.md) remain the P0 security blocker; changing the manifest cannot repair that repository deletion behavior.

**Counterexample:** if the user installs a new icon and sees an empty logbook, automatically importing a previous container's data based only on matching name/origin would violate owner, replica, provenance and consent boundaries. The recovery flow must authenticate the intended owner and use an explicitly verified independent backup/restore or approved sync contract.

## 7. WebKit installed-container custody: copy-on-install is not live sharing [SOURCE / CHANGE WATCH]

WebKit's Safari 17.2 announcement says iOS/iPadOS Home Screen web-app creation **copies existing login cookies** from the initiating browser when the auth state is cookie-based; **other local storage is not copied**, and website data is **not shared after installation**. This directly contradicts a common assumption that Safari IndexedDB data appears automatically inside a newly installed PWA. It also means “the user is already signed in” is not a reliable substitute for inspecting the actual Firebase persistence mechanism and owner gate.

WebKit 16.4 also explicitly describes **multiple Home Screen installations of the same web app** and a name+manifest-id identity scheme for Focus. Multiple icons cannot be assumed to share a single local ledger, even if the same URL and account name appear. Exact 26.x behavior should be revalidated on a physical device, rather than assuming 17.2 behavior is unchanged.

Primary: [WebKit Safari 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/), [WebKit 16.4](https://webkit.org/blog/13878/). This is a platform-level storage warning, **not** a measured LogMate copy or erasure result.

## 8. Storage quota, persistence, eviction and export are distinct [SOURCE / FAILURE MODES]

WebKit's Storage Policy explains quota versus eviction, origin-wide eviction, StorageManager.estimate/persisted/persist, and that standalone Home Screen web apps use browser-app-class quotas. MDN describes best-effort storage and browser-specific persistence decisions. The existence of a quota estimate or a successful persist request is **not a permanent backup guarantee**; origin-wide eviction, user clearing, app removal, MDM policy and independent installed containers remain distinct failure domains.

The [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) says persistent mode can exempt an origin from browser-managed eviction in the described policy, while [MDN quota guide](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) emphasizes browser-dependent permission and storage-pressure behavior. Neither says a managed iPad permits exporting a .lbk file to a user-controlled Files location. A successful 37-store in-DB backup encode is not an independently saved and reopened external file. Existing [W-012 Native B1](https://github.com/yhappcom/logmate/blob/main/docs/evidence/w012-empty-destination-backup-2026-10-27.md) **70 focused / 900 full PASS, 1 browser-only SKIP** remains a valid bounded Native restore result, not PWA storage or Files custody evidence.

A browser profile with multiple installations may have independent cookies, IndexedDB, Cache Storage and Service Worker registrations. The exact data partition on Safari 26 and a managed EFB must be **observed**, not inferred from URL equality or an app icon.

## 9. Chromium 150 origin migration is an install transfer, not a data transfer [SOURCE / CHANGE WATCH]

Chrome announced **PWA Origin Migration in Chrome 150** for same-site origin changes, using a two-sided association/authorization handshake. The official guide expressly warns that **user data and permissions are not migrated**: LocalStorage, IndexedDB, cookies and notification/geolocation permissions remain origin-bound. This is particularly relevant if LogMate later moves between a Firebase-hosted subdomain and a MintTap domain. A supported icon/OS integration migration is not an owner-authorized ledger migration.

Primary: [Chrome 150 origin migration announcement, 2026-06-03](https://developer.chrome.com/blog/seamless-pwa-origin-migration), [Chrome migration guide](https://developer.chrome.com/docs/modern-web-guidance/guides/pwa/migrate-web-app-origin). **Do not deploy the handshake or force migration now**: exact browser support, manifest id, hosting origins, old-site availability, account authority, data export and rollback have not been approved. Safari/WebKit parity is unproven. The API and policy are fast-changing CHANGE WATCH, not a universal web standard guarantee.

Migration invariant: **app installation continuity ≠ origin storage continuity ≠ local ledger custody continuity ≠ remote account continuity**. A migration runbook must independently preserve or deliberately retire each, and must never silently delete the old local data before a verified backup or approved sync handoff.

## 10. iPad landscape, managed installation and offline task readiness [B/C TRANSFER]

LogMate's manifest currently declares **portrait-primary**. MDN labels manifest orientation as **limited availability** and notes browsers/OS may or may not honor it. For a cockpit iPad that may be used landscape, this is a **compatibility question**: it is not proof the app is forced portrait, and not a reason to change source without an approved responsive design and physical-device result. Test landscape, portrait, split-view/multitasking where permitted, zoom, VoiceOver, large text, SafeArea, keyboard and offline interrupted launch as separate dimensions.

Apple MDM Restrictions include Managed Open In policies such as allowOpenFromManagedToUnmanaged and its inverse. These can affect document movement but **do not by themselves establish** the EFB's actual policy, Home Screen install permission, Files destination, external app availability, hotspot allowance or background sync. An iPad enrolled as Shared iPad has additional historical Add-to-Home-Screen restrictions for third-party browser flows in WebKit 16.4; do not extrapolate them to all 26.x Safari or every airline.

Sources: [MDN orientation](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/orientation), [Apple MDM restrictions](https://developer.apple.com/documentation/devicemanagement/restrictions), [WebKit 16.4](https://webkit.org/blog/13878/). Design Studio [W121](https://github.com/yhappcom/design-studio/blob/main/research/web/121-stage3-evidence-saturation-and-execution-priority-gate.md) already requires exact runtime and AT evidence rather than more speculative visual manifests.

## 11. Operational identity/custody decision matrix [SYNTHESIS / EXPERT JUDGMENT]

| Operation | What may succeed | What must NOT be inferred |
| --- | --- | --- |
| Add to Home Screen on iPadOS 26 | App-like icon/window, user toggle | offline shell verified, installed data durable, airline MDM permits workflow |
| Change start_url without explicit id | New launch path | existing installed identity preserved |
| Add id after previous install | More stable future identity *if computed ID matches* | all existing installations migrate automatically |
| Move to new origin with Chrome 150 handshake | Supported Chromium installation integration migration | IndexedDB/Cache/Firebase session or Files moved; Safari support |
| Copy cookies at Home Screen installation | Cookie-based sign-in may be copied | IndexedDB or local logbook copied, live shared auth |
| Request storage persistence | UA may grant persistent mode | no user/MDM removal, no data loss, no backup required |
| Install same URL twice | Multiple user-visible app icons | same storage container or same local replica |
| Complete local account deletion | Local phase may say completed | all 37 stores erased, all installed containers/server/external Files erased |
| Save backup inside database | Coherent export snapshot design | independent Files save/readback/restore |
| Service Worker installed | Fetch interception possible | complete cache, stable update, first-claim safety, no quota loss |

**MINTTAP DIRECTION (not approved implementation):** freeze the current identity/origin/deployment path until the operator can inventory installed copies and verify custody. Do not change id/start_url/scope/orientation, move origin, add install promotions, force uninstall, or clear browser storage on this research alone.

## 12. Engineering/physical-device falsification packet — II01–II24 [VALIDATION DEFINED NOT RUN]

Use disposable test identities and synthetic flight canaries; capture exact Git source SHA, generated artifact digest, served manifest/worker URL, browser/OS build, installed display mode, data-container ID if observable, owner/replica hashed markers, offline state, File save/readback and MDM configuration **without** personal flight content or real credentials. Positive and negative controls are mandatory.

| ID | Scenario | Required oracle |
| --- | --- | --- |
| II01 | Serve exact approved build at intended HTTPS origin | Manifest and SW fetched from correct URLs; source/build hash recorded |
| II02 | Install from Safari 26/iPadOS 26 with Open as Web App ON | Actual standalone launch observed, not inferred from icon |
| II03 | Same URL with Open as Web App OFF | Bookmark/browser behavior distinguished |
| II04 | Older supported iPadOS/Safari install | Version-specific behavior recorded; no 26 rule backported |
| II05 | Chromium current build install | Current menu/prompt and computed manifest ID captured |
| II06 | Current LogMate manifest without id | Actual computed ID and scope recorded before any edit |
| II07 | Hypothetical root/subpath deployment in isolated lab | ID/scope changes detected; no production migration |
| II08 | Add proposed stable id in disposable lab | Existing installed identity remains the same; rollback possible |
| II09 | Existing install, change start_url in lab | No duplicate install or lost user route after approved identity preservation |
| II10 | New installed Home Screen copy after Safari local canary | Prove whether IDB/cookies are copied/shared separately |
| II11 | Two same-origin Home Screen icons, different labels | Independent container and replica custody measured |
| II12 | Safari tab vs installed app, same verified UID | Explicit local owner, replica, backup inventory, no assumed sharing |
| II13 | Network disconnected before first successful worker install | Truthful not-offline-ready failure; no false readiness |
| II14 | Full verified install then offline restart | Shell, data read and edit behavior; no fabricated network sync |
| II15 | Interrupted update/old+new worker | No mixed shell/DB schema or silent data loss; reuse 528 FC/CW/TR |
| II16 | Quota/eviction and storage persistence | Distinguish granted/denied, user removal, origin data loss and backup |
| II17 | Files export from managed EFB | Actual permitted destination, independent file bytes/readback |
| II18 | Reinstall or new container + import saved file | 37-store owner/replica/Sync trust verified; no implicit transfer |
| II19 | Managed Open In restricted EFB | Explicit deny path and recoverable instructions; no fake success |
| II20 | Landscape/portrait/split view/VoiceOver | No hidden controls or unusable recovery; Design Studio consumes evidence |
| II21 | Delete owner A in installed copy, Safari tab still open | 529 WP/RW/RC cross-container truth; no all-device erasure claim |
| II22 | Chrome 150+ same-site origin migration lab | Installation move separately observed from storage and permissions |
| II23 | Same migration attempt in Safari/WebKit | Explicit unsupported/unknown outcome, no Chromium assumption |
| II24 | Public onboarding/acquisition and installed app telemetry | Privacy-safe counts only; no UID, flight content or installation fingerprint |

**Priority order:** 529 WP01–WP10/WP15 owner deletion and A→B liveness **P0**, then II01/II02/II06/II10–II12/II14/II17–II20 **P1**, then II07–II09/II22–II24 migration **P2**. No new exact LogMate test, browser run or physical EFB run occurred in this study. A test blocked before the runner is NON-EXECUTION, never product FAIL/PASS.

## 13. Cross-track ownership, external transfer and contradiction register [DEPENDENCY / TRANSFER VALIDATION]

- **A — primary owner:** manifest id/start_url/scope, Safari 26 install toggle, Chromium install semantics, Service Worker registration scope, container separation, origin migration platform facts. Evidence: primary sources + exact manifest/JS static; installed runtime OPEN.
- **E — security/operations co-lead:** origin and identity migration release/rollback, independent Files custody, MDM restrictions, privacy/owner trust, stale installed copies. Highest overall Stage 8 P0 remains **529 terminal deletion 29/37**; this PWA domain does not displace it.
- **B — UX/IA consumer:** “install,” “ready offline,” “your local logbook,” “backup saved,” “account deleted” require different task states and recovery copy; Design Studio W121 owns visual/interaction evidence.
- **C — quality verifier:** landscape/AT/offline install/eviction and installed-copy matrix, exact product/device provenance. Existing W-012 Native PASS cannot be transferred to WebKit.
- **D — discovery/analytics consumer:** installed-vs-web acquisition continuity and privacy-safe measurement. Marketing [D9](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) remains release/claim HOLD; no install success or guaranteed offline claim.
- **Engineering:** [S007](https://github.com/yhappcom/software-engineering-studio/blob/main/research/systems/S007_account_deletion_reauthentication_revocation_saga.md) owns owner deletion; [D003](https://github.com/yhappcom/software-engineering-studio/blob/main/research/data/D003_schema_evolution_migration_rollback_compatibility.md) owns schema compatibility; product implementation/test authority remains Engineering. No peer/product repository edits.

**CONTRADICTIONS resolved:** (1) “Safari requires a manifest/SW for app-like installation” is outdated for iPadOS 26; (2) “Chrome always requires fetch SW for installation” is outdated for menu install; (3) “same URL = same installed storage” is false as a general guarantee; (4) “Chrome origin migration moves user data” explicitly contradicted by Chrome docs; (5) “manifest portrait-primary means verified forced portrait on EFB” unsupported; (6) “a successful icon means the offline logbook is ready” unsupported.

## 14. Checkpoint, uncertainty and change watch [OPEN / DECISION]

**New reusable result:** PWA *installation availability* is increasingly permissive (Safari 26; Chromium revised criteria), while **installed identity, container custody, offline readiness and account erasure remain independent operational proofs**. Exact LogMate manifest has relative start_url, no explicit id/scope and portrait-primary; these are migration/compatibility review triggers, not confirmed production defects. The project-owned worker is a positive offline architecture component but is not proven safe on the target managed EFB.

**Unresolved:** actual LogMate hosting origin/base path; whether any iPad installations exist; iPadOS/Safari version; airline MDM and Files restrictions; installed IDB partition; actual cookie/auth behavior; offline readiness; physical landscape; exact Files readback; A→B deletion and all 37 stores; approved origin migration plan. Do not infer these from standards. Recheck Safari 26.x, Chrome origin migration rollout, manifest id handling, Apple Managed Open In and current policy at any release decision.

**Gate:** Stage 8 ACTIVE · PWA release HOLD · Production validation OPEN. Next high-information-gain step is Engineering-approved populated 37-store deletion and B-startup, followed by installed-iPad identity/container and independent Files custody. No filler primer or speculative UI change is warranted until execution evidence changes.
