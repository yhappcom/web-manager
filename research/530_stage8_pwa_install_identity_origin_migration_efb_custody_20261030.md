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


---

## 15. History restoration is a fourth PWA state plane [HISTORY / PRINCIPLE / SOURCE — 2026-10-31]

**Problem:** An offline-first PWA already separates (1) the HTTP cache, (2) explicit Service Worker Cache Storage and (3) IndexedDB/local ledger. A fourth plane is **back/forward cache (bfcache)**: a browser may freeze and later restore an entire *document and JavaScript heap* rather than run a new navigation, Worker fetch, Flutter bootstrap or cold-start owner check. This is not a second copy of the database, a Service Worker cache hit or a normal SPA route transition. A fifth independent plane is an already-running background tab or installed Web App instance. These distinctions matter when owner A signs out, deletion starts, or owner B authenticates elsewhere.

- **[SOURCE, WHATWG HTML](https://html.spec.whatwg.org/multipage/nav-history-apis.html):** \`PageTransitionEvent.persisted\` distinguishes a newly loaded document from one reused through session history; \`pagehide.persisted=true\` is only an *intention* to preserve, not proof of subsequent restoration.
- **[SOURCE, web.dev](https://web.dev/articles/bfcache):** \`pageshow.persisted=true\` is the positive restore observation; the old JS heap can resume without rerunning startup. \`freeze\`/\`resume\` events are Chromium-specific and not a cross-engine replacement for \`pageshow\`. Browser history restoration is not the same as Flutter Navigator's in-document route history.
- **[SOURCE, MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/pageshow_event) / [Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API):** \`pageshow\`, \`pagehide\` and \`visibilitychange\` describe different transitions. A hidden tab becoming visible does not necessarily navigate or trigger \`pageshow\`; a mobile foreground transition does not guarantee network reachability.

**Operational invariant:** after any history restore or foreground transition, *cached view identity*, *current authenticated identity*, *durable local owner/deletion phase*, *remote authority*, and *write eligibility* are distinct checks. An event listener alone is not authorization; all mutations need an authoritative admission guard. Conversely, a transient offline remote validation failure should not automatically destroy an approved offline owner's ledger. These are constraints for Engineering's contract, not authorization to change it.

## 16. \`no-store\` is not a universal history/privacy lock [SOURCE / CHANGE WATCH]

The pinned [LogMate \`firebase.json\`](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/firebase.json) has one \`**\` Hosting header rule: \`Cache-Control: no-cache, no-store, must-revalidate\`. It is a *source configuration*, not a measurement of a particular deployed response. The meanings of these cache systems must not be collapsed:

| Plane | What the broad header establishes | What it does **not** establish |
| --- | --- | --- |
| Browser/shared **HTTP cache** | \`no-store\` instructs compliant HTTP caches not to store the response; \`no-cache\` alone would permit storage with revalidation | Existing cache eviction, offline shell readiness, IndexedDB erasure |
| Explicit **Cache API / Service Worker** | Nothing about a Worker application's own \`Cache.put\` admission by itself | A no-store response is necessarily absent from named Cache Storage; Worker code must enforce sensitive-route exclusions |
| **bfcache** document/heap | May affect eligibility in browser-specific ways | All engines always discard a \`no-store\` document or always re-run app startup |
| **IndexedDB** / app local state | No account-erasure guarantee | All 37 LogMate stores cleared, backup removed, old tab invalidated |
| External **Files** backup | No impact on an independently saved file | Backup deletion or custody verified |

**[SOURCE, Chrome, updated 2025-09-09](https://developer.chrome.com/docs/web-platform/bfcache-ccns):** Chrome progressively enabled bfcache for \`Cache-Control: no-store\` documents when safe, with exclusions for changes in cookies/authentication, certain live connections and sensitive no-store subresource requests, plus a shorter three-minute timeout. This is **conditional Chrome behavior**, not proof that any LogMate page will enter bfcache. The [Chrome Enterprise policy](https://chromeenterprise.google/policies/allow-back-forward-cache-for-cache-control-no-store-page-enabled/) can change this outcome on managed Chrome. Other browsers, including WebKit, need independent evidence; do not backport Chrome's policy.

**[SOURCE, MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)** describes HTTP cache directives; the [W3C Service Worker explainer](https://github.com/w3c/ServiceWorker/blob/main/explainer.md) explicitly says Cache API freshness headers are ignored. [LogMate's project-owned generated Worker](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/tool/pwa_precache.dart) deliberately fetches shell assets and stores verified bytes in Cache Storage (already owned by integrated research 528). This is **not a contradiction**: HTTP cache bypass and explicit offline caching are separate operations.

**MINTTAP DIRECTION:** do not loosen headers to chase a speculative bfcache score, nor claim the existing blanket \`no-store\` proves sensitive information cannot be revisited. Test per-route served headers, Worker inventory and actual history restoration before a security/performance trade-off. Auth-action bearer-code \`Referrer-Policy\` remains a *separate* 527 issue.

## 17. Exact LogMate lifecycle and ownership call graph [SOURCE / STATIC REVIEW]

Read-only pin, LogMate \`main@9cc0cd432a317d5dfebbe90e318fb219e53e024a\`:

1. [\`web/index.html\`](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/index.html) loads \`flutter_bootstrap.js\` after \`<base href="$FLUTTER_BASE_HREF">\`. The [bootstrap](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/web/flutter_bootstrap.js) registers \`logmate_service_worker.js\` at base-path scope with \`updateViaCache:'none'\`; it handles Worker \`controllerchange\`, not a top-level \`pageshow\`/visibility-to-owner authorization handshake in that file.
2. [\`SessionGate\`](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/app/session_gate.dart#L97-L155) runs \`_resolveStartup(...)\` in \`initState\`. Its \`didChangeAppLifecycleState(resumed)\` branch, **when startup has already resolved and its decision requires remote validation**, calls \`_runBackgroundRemoteSessionValidation()\`; it does **not** directly rerun \`_startupResolver()\` or explicitly reread the durable account-deletion phase in that branch.
3. [\`AccountDeletionCoordinator\`](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/application/account_deletion_coordinator.dart) and [repository](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/repository/logbook/sembast_logbook_repository.dart#L1007-L1125) implement a multi-step deletion saga and local phase. Earlier 529 RW §§76–83 already identified the separate local mutation guard question; do not duplicate or promote it to a runtime incident.
4. [\`AccountDeletionLockedScreen\`](https://github.com/yhappcom/logmate/blob/9cc0cd432a317d5dfebbe90e318fb219e53e024a/lib/screens/session_recovery_screens.dart) displays a deletion lock when the startup resolver returns that decision. It is not evidence that a *different, already-rendered document* has been invalidated.

**Precise source-level gap:** the inspected bootstrap and resumed SessionGate branch do not demonstrate a cross-document history-restore → local deletion-phase recheck → immediate sensitive-view suppression protocol. Flutter's own lifecycle mapping, Firebase Auth callbacks, other widgets and actual compiled browser behavior may add protections; absence of a \`pageshow\` listener in this one file does **not** prove data exposure. An owner deletion in one installed WebKit container also does not by itself update a separate Safari container. **OPEN:** full app-wide lifecycle search, exact compiled Web execution and cross-container owner tests.

## 18. Reproduction model: what would actually constitute a privacy failure [SYNTHESIS / CONTRADICTION]

Distinguish **stale pixels**, **stale in-memory objects**, **live read access**, **write access** and **foreign-owner disclosure**. They are not equivalent:

| Sequence / branch | Possible observation | Security conclusion without execution |
| --- | --- | --- |
| A page navigates away and later receives \`pageshow.persisted=true\` | Previous A DOM/heap may be restored before app revalidation | Conditional sensitive-view window; **not proven LogMate** |
| A signs out in *same* document and returns via Flutter Navigator | Soft navigation; no bfcache required | Must test app's own state guard; bfcache theory alone irrelevant |
| A deletes account in tab 1; tab 2 remains open | Tab 2 can retain its prior Flutter state unless coordinated | 529 RW admission/owner-check tests; no automatic cross-tab proof |
| A is deleted in Safari tab; separate Home Screen app exists | Separate WebKit storage/credential containers can diverge | No automatic all-container erasure; remote authority and local custody must be tested |
| Old view displays stale A data but all reads/writes reject | Residual display privacy issue possible | Not the same as ongoing data mutation or B receiving A records |
| B logs in on a genuinely new independent origin/container | No A local database inherited merely by equal product branding | Does not prove old A container erased |
| Offline page resumes with A still legitimate | Remote verification may be unavailable | Must preserve safe offline access while preventing owner/phase mismatch |

**Failure oracle:** a test must capture the exact owner/phase at navigation and restore, the first rendered frame before/after the gate, redacted canary visibility, read/write rejection and remote validation outcome. No real pilot data, auth token, user UID or credential in diagnostic logs. Merely observing \`pageshow.persisted=true\` is not a product failure.

## 19. Browser/OS matrix and capability boundaries [SOURCE / CHANGE WATCH]

- **WHATWG / general Web:** \`pageshow.persisted\`, \`pagehide\` and visibility semantics are platform concepts. Browser bfcache admission/eviction and event timing differ. A Service Worker registration cannot guarantee that history restore triggers its \`fetch\` handler.
- **Chromium:** Chrome's 2025 no-store bfcache change makes relying on no-store for logout erasure invalid as a universal rule. Chrome's eviction on cookie/auth changes is conditional, and Firebase session state may not correspond to a same-origin cookie change. Do not assert that this specific app is eligible without a real run.
- **Safari/WebKit:** the [WebKit 17.2 cookie-copy statement](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/) says no other local storage is copied and later app/browser data are not shared. [Safari 26 Home Screen behavior](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) broadens app-style launches, not cross-container revocation. Whether Safari's page cache retains a particular no-store LogMate route on iPadOS 26 is **OPEN**.
- **Managed EFB:** MDM may restrict install, file movement, browser access or enterprise settings; none are inferable from an ordinary Safari lab. A no-store response, cookie copy or icon does not grant an airline-approved offline logbook.

## 20. Exact acceptance packet — HR01–HR22 [VALIDATION DEFINED / NOT RUN]

Use disposable synthetic A/B accounts and flight canaries, approved test backend, exact compiled Web commit/artifact hash, actual served HTTPS headers, browser/OS/MDM version, manifest and Worker hashes, isolated profiles and redacted trace. Classify **NOT RUN / NON-EXECUTION / FAIL PRODUCT / PASS PRODUCT / PASS DEVICE-MDM**.

| ID | Test | Required observation / negative control |
| --- | --- | --- |
| HR01 | Exact served \`/\`, \`/auth/action\`, static font, SW, manifest | Real \`Cache-Control\`, \`Referrer-Policy\`, \`Vary\` and Worker scope; source config alone insufficient |
| HR02 | Cold A startup online | First frame owner/phase gate; no stale data before decision |
| HR03 | A navigates away and back in same browser | \`pageshow.persisted\`, network/Worker fetch, Flutter startup invocation and owner guard distinguished |
| HR04 | No-store vs no-cache in **isolated synthetic** page | bfcache eligibility and HTTP-cache behavior separately measured, no production header change |
| HR05 | A signs out in another tab while original A view is hidden | First frame on return, owner state, read/write denial, stale pixels |
| HR06 | A deletion begins in tab 1; tab 2 foregrounds | Phase recheck and write barrier; reuse 529 RW01–RW14 |
| HR07 | A deletion completes; browser Back | No actionable A view, no A canary exposure; record history eligibility |
| HR08 | A deletion completes; tab 2 remains visible | Cross-tab notification vs durable guard; no assumption that event alone revokes writes |
| HR09 | A deletion completes; B attempts normal startup | 529 completed-marker/37-store P0 oracles, no premature B PASS |
| HR10 | B startup on independent clean profile | Control that rejects false inherited-A claims |
| HR11 | Offline A legitimate foreground restore | No destructive remote-auth failure; local owner/phase consistency |
| HR12 | Offline A after local deletion lock | No A write; recoverable status, no false completion |
| HR13 | Frozen document vs background tab \`visibilitychange\` | Separate event paths; no reliance on one event firing universally |
| HR14 | Flutter Navigator soft back | Do not misclassify as bfcache; in-app route guards checked |
| HR15 | Worker update during history navigation | Controller, shell/schema version, old client and cache consistency; reuse 528 |
| HR16 | Auth Action one-time code Back/Forward | Code not re-exposed or logged; AA01–AA14 route/header oracles |
| HR17 | Two same-origin installed Home Screen copies | Separate owner/Replica/IDB and old-view status |
| HR18 | Safari tab ↔ Home Screen app | Cookie copy vs independent local storage; deletion not presumed global |
| HR19 | Managed Web Clip vs Safari | Actual airline MDM policy, history/offline/Files constraints |
| HR20 | VoiceOver/large text on restored locked state | Sensitive view suppressed, focus/announcement accurate, recovery discoverable |
| HR21 | Analytics on \`pageshow.persisted\` | Privacy-safe page-view de-duplication, no UID/flight content or token |
| HR22 | bfcache disabled / blocked by policy | Ordinary reload control still enforces owner/deletion gates |

**Ordering:** HR05–HR09 are P0 **only after Engineering's existing 529 exact A/B/37-store fixture is available**. HR01/HR03/HR04/HR13/HR15 are platform and quality dependencies; HR17–HR20 require actual iPad/MDM. This packet is a targeted extension, not a replacement for 529 WP/RC/RW or 530 II cases.

## 21. B/C/D transfer and operating trade-offs [DEPENDENCY / TRANSFER VALIDATION]

- **A owns:** HTML history events, browser cache vs Cache API, Safari/Chromium lifecycle, first/second installed container distinctions. No duplicate HTTP primer.
- **E owns:** security decision that no-store, Worker install and initial Firebase auth do not independently revoke old-page authority; cross-context owner/deletion lifecycle, served header policy and incident response. Engineering S007 owns implementation and tests.
- **B owns:** first-frame suppression, truthful “signed out / deletion pending / deleted / offline” task states, recovery navigation; Design Studio W121 owns visual/accessibility interaction execution evidence, not another pre-runtime design manifest.
- **C owns:** exact browser matrix, bfcache eligibility, first-frame trace, foreground/offline interruption, VoiceOver and cross-platform PASS provenance. An isolated synthetic Chrome PASS cannot promote exact LogMate.
- **D owns:** privacy-aware \`pageshow\` measurement, avoiding duplicate SPA route/page-view counting; Marketing D9 owns public claims. No install/backup/deletion claims until actual oracles pass.

**Performance tension:** blanket no-store can increase repeat network cost, yet bfcache restoration may avoid a reload in eligible Chromium; allowing history restoration can preserve stale UI. Optimizing hit rate is subordinate to owner/deletion safety. **Analytics tension:** a bfcache restore may not run ordinary initial pageview JS; blindly firing an additional pageview for every Flutter soft navigation double counts. Define the semantic event contract before instrumentation.

## 22. Attempted independent browser lab and evidence integrity [VALIDATION / NON-EXECUTION]

On 2026-10-31 an isolated Python HTTP server + Playwright attempted three synthetic Chrome history cases (\`no-store\`, \`no-cache\`, ordinary cache) in container Chromium **144.0.7559.96**. Navigation to \`http://127.0.0.1:<ephemeral>/no-store\` failed with **\`net::ERR_BLOCKED_BY_ADMINISTRATOR\` before the test page loaded**. No \`pageshow\`, network trace, bfcache eligibility or HTTP-cache result was produced. This is **NON-EXECUTION / environment policy**, not a browser defect, LogMate FAIL, or proof of either cache behavior. Do not count it as a passed synthetic test.

An approved HTTPS test origin or CI runner that permits test navigation is required for HR03/HR04. A successful synthetic browser run would remain LAB evidence, not an exact compiled LogMate or managed iPad result.

## 23. Falsification and release decision [CONTRADICTION / OPEN]

This finding narrows or disappears if exact product execution demonstrates that an already-rendered A view is suppressed and its reads/writes rejected on **every** history/foreground/cross-tab transition before owner-invalid pixels or operations become observable, including when offline. It strengthens if an old A view survives a verified deletion, displays a redacted synthetic canary or admits a write; classify display, read, write and cross-owner results separately.

**Do not prescribe** unconditional reload on every foreground event, global \`Clear-Site-Data\`, forced \`skipWaiting\`, broad Worker cache removal, a new \`id\`/origin, or blanket auth denial when offline. Each can disrupt legitimate offline pilot data or old-client schema compatibility. Any proposed fix needs Engineering ownership, offline-first policy, migration/rollback and cross-engine proof.

## 24. Adjacent high-value questions checked [SYNTHESIS / OPEN]

This bundle integrated history restoration, HTTP/Cache API/bfcache boundaries, current Chrome no-store change, exact LogMate bootstrap and SessionGate resume branch, cross-tab owner lifecycle, installed WebKit containers, managed EFB, UX/AT, analytics and falsifiable release oracles. **Next adjacent step cannot responsibly be promoted without an approved executable origin and exact Engineering 529 fixture**. Further source-only rewording would add less information than HR05–HR09 execution. No LogMate, Design Studio, Marketing or Engineering repository changes.

## 25. Gate and handoff [MINTTAP DIRECTION / CHANGE WATCH]

**Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.** Highest bottleneck remains **529 account A terminal deletion / 37-store parity / B startup / RW/RC write admission**; history restoration is a new **cross-track validation dimension**, not a substitute for it. Then independently retained Files backup, Safari Home Screen/managed Web Clip custody and physical offline operation. Recheck Chrome bfcache/no-store eligibility, Safari 26.x behavior and MDM policy at actual release; never infer production state from an old source pin.


## 26–34. Service-worker update and offline rollback custody: source-grounded cross-track checkpoint (2026-10-31)

**Evidence boundary:** SOURCE = read-only LogMate `main` `web/flutter_bootstrap.js` and `tool/pwa_precache.dart` inspected 2026-10-31. The generated `logmate_service_worker.js` is **not a source-tree file**; its JS template is emitted by `_workerSource(manifest)` in the Dart generator. Therefore source conclusions are about generation logic, **not** proof of served build bytes or installed-worker behavior. Prior 529 deletion parity and 530 history tests remain unexecuted.

### 26. Historical failure and explicit ownership [HISTORY / PRINCIPLE / A]
AppCache bundled application-shell update and offline caching into an opaque declarative mechanism with confusing update timing. Service workers separate registration, install, waiting, activate, control and fetch handling, but create their own multi-version and multi-client consistency problem. The safety target is **verified executable shell + compatible local data + recoverable owner state**, not merely “new worker active.” Standard: [W3C Service Workers](https://www.w3.org/TR/service-workers/); platform lifecycle explanation: [web.dev lifecycle](https://web.dev/articles/service-worker-lifecycle). Treat WebKit lifecycle behavior as independently testable, not a Chromium guarantee.

### 27. Exact LogMate update admission [SOURCE / A+E]
The bootstrap registers the generated worker at a base-path-derived scope, `updateViaCache:'none'`, calls `registration.update()`, and posts `START_PRECACHE` to waiting/active/controller. It does **not** await registration before starting the Flutter engine. It posts `PROMOTE_VERIFIED_CANDIDATE` on `ready` and `controllerchange` (controllerchange listener uses `once:true`). The generator emits an install path that hashes shell/fonts/notices, a waiting-worker strategy with **no `skipWaiting()`**, an activate path with `clients.claim()`, and an explicit verified-candidate promotion path. It intentionally does **not** clean up old caches; rollback message currently returns `NOT_ROLLED_BACK`. These are deliberate guardrails, not proof of end-to-end atomic update.

### 28. Three independent authorities [SYNTHESIS / E]
(A) The worker's verified `appBuildId` and cache catalogue certify bytes of an offline package; (B) `databaseCapability` in the generated manifest is a build-time declared compatibility marker; (C) actual open local database schema, dirty edits, owner/deletion phase and Sync outbox are runtime facts. Neither A nor B alone proves C. A verified previous shell may be **incompatible with a newly migrated DB**. Accordingly the existing fail-closed `ROLLBACK_TO_PREVIOUS` behavior is appropriate absent a separately validated downgrade protocol. The `clients.claim()` call is not equivalent to a product-level session/owner reauthorization.

### 29. Update consistency matrix [DEPENDENCY / A→E/C]
- **Old tab + waiting new worker:** old tab may continue with old JS while candidate cache downloads; no `skipWaiting` reduces involuntary controller replacement, but old-tab mutation authority must still be checked at repository write time.
- **All old clients closed:** waiting worker can activate; verify that the first new navigation receives a self-consistent app shell and that DB migration/owner guard succeeds before write admission.
- **Failed candidate digest:** existing verified shell should remain available; test both online and offline navigation and observe actual `currentBuildId`.
- **Storage pressure mid-download:** retained previous versions and 724 font resources increase quota pressure; no claim of eviction or exact storage footprint without measured bytes/OS data.
- **Interrupted install/activate:** verify cache catalogue, shell response and local DB separately after force close/reopen; `event.waitUntil` does not guarantee persistence against process termination.
- **Old browser tab + account A deletion in another context:** a valid cached shell is not an authorization token; a stale owner view must fail transaction-time writes irrespective of update state.

### 30. Fetch/cache and credential separation [SECURITY / E]
The generator's `download()` uses `fetch(new Request(item.path,{cache:'no-store',credentials:'same-origin'}))`, checks HTTP status, exact byte count and SHA-256, and stores verified responses. This is **resource integrity** for enumerated shell artifacts, not a general guarantee about auth endpoints, all navigations, user-data backup or response privacy. Need to verify actual fetch routing for non-GET, cross-origin, auth action URLs, deep links, range requests and offline errors against the generated output. Cache Storage and IndexedDB have different purposes; neither should be treated as an independent export. Explicit cache retention needs a measured, consent-aware maintenance strategy that never deletes user records to make room for fonts.

### 31. EFB operational fault model [TRANSFER VALIDATION / B+C+E]
For a managed company iPad, test separately: Home Screen launch allowed by MDM; worker install/activation; first full precache; offline relaunch; old/new shell consistency; Files export/readback permission; IndexedDB durability after OS pressure; screen rotation and VoiceOver recovery. Airplane mode is not equivalent to disabling every local network path. Native↔PWA unattended synchronization remains **OPEN**: no inference from Service Worker background capability, `clients.claim`, push or background sync to direct device-to-device transport. Avoid a UI promise of “automatic sync” before device/network/policy evidence.

### 32. Acceptance packet SW01–SW16 [VALIDATION DEFINED, NOT RUN]
| IDs | Scenario / oracle | Ownership |
|---|---|---|
| SW01–02 | Fresh HTTPS install and complete verified shell; offline cold launch with no network | A/C |
| SW03–04 | Old controlled tab open while new worker waits; close last tab then activate, observe version and DB schema | A/E |
| SW05–06 | Tamper/truncate one shell/font asset; candidate rejected, old verified shell still usable | A/C |
| SW07–08 | Kill browser during precache and during activation; reopen with catalogue, byte and DB consistency checks | A/E |
| SW09–10 | Quota exhaustion with retained caches; no unconsented IndexedDB or backup erasure | C/E |
| SW11–12 | Auth/deletion during old tab and history restore; repository writes rejected after deletion intent | E/B |
| SW13–14 | Deliberate schema incompatibility; rollback request fails closed, safe user recovery copy available | E/B |
| SW15–16 | Safari Home Screen + managed EFB and Chromium independent results; Files export/reopen/restore | A/C/E |

**Required artifacts:** exact source SHA, built worker/manifest hashes, served HTTPS headers, browser+OS build, installation mode, controlled client count, SW state transitions, current/previous build IDs, DB capability/schema and owner-phase canaries, sanitized console/Network trace, export checksum, and operator-observed Files reopen. No simulated model can close the production gate.

### 33. Cross-track ownership and release judgment [MINTTAP DECISION / DEPENDENCY]
Track A owns lifecycle/fetch/installation facts. Track E owns version/DB/owner security and deployment/rollback release gates. Track C owns offline resilience, quota, accessibility and device matrix. Track B owns explicit “update pending / safely close / export first / recover” states, consuming Design Studio interaction evidence. Track D owns privacy-minimized install/update/offline-success telemetry, not acquisition promises; Marketing D9 retains product-claim HOLD. Software Engineering S007 owns executable product tests and implementation decisions. **Do not elevate a green SW digest check into user-data durability or release PASS.**

### 34. Contradiction and next-adjacent-question audit [CONTRADICTION / OPEN / CHANGE WATCH]
**Resolved:** “No `skipWaiting` means updates never activate” is false: normal waiting activation after old clients release is possible. “`clients.claim()` proves old owner invalidation” is false. “No cache cleanup guarantees safe rollback” is false because cached bytes do not establish schema compatibility. “Generated worker file missing from source means offline worker missing in build” is false: generator emits it. **OPEN:** inspect and execute the *generated* worker from an exact production-equivalent build, including fetch-routing and catalogue concurrency, before claiming runtime correctness. Browser/OS support and MDM policy remain CHANGE WATCH. The adjacent high-value work is now executable product acceptance, not another speculative static-only SW primer. Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD unchanged.


### 35. Exact artifact-build provenance and the two distinct test binaries [SOURCE / ENGINEERING DEPENDENCY; 2026-10-31]

Re-read current LogMate [Makefile](https://github.com/yhappcom/logmate/blob/main/Makefile) (blob `42485938e7bcbad6e473b047bf01690954ccbbc3`), [bootstrap](https://github.com/yhappcom/logmate/blob/main/web/flutter_bootstrap.js) (blob `a70625e8bda32aafd5dd23822c017d05229f0e63`) and [worker generator](https://github.com/yhappcom/logmate/blob/main/tool/pwa_precache.dart) (blob `90a67954af618a4e18199fa92555491c56167c17`). The actual project defines **two different build contracts**:

- `make build-pwa`: `flutter build web --output build/web --pwa-strategy=none --no-web-resources-cdn --no-wasm-dry-run`, then `dart run tool/precache_flutter_web.dart --build-root build/web`, then `dart run tool/verify_pwa_artifact.dart --build-root build/web`.
- `make build-pwa-acceptance`: same chain, but Flutter receives `--dart-define=LOGMATE_PERSISTENCE_ACCEPTANCE=true`, and verification requires `--require-acceptance-harness`.

**SYNTHESIS:** A test on the acceptance-harness build cannot by itself establish the identical runtime behavior of the ordinary release build. The compile-time flag may change the attack surface or execution path. Conversely, release build testing alone may lack safe seeded-data instrumentation. Both must have separate artifact SHA, source commit, command transcript and served HTTPS deployment identity; a source-only worker inspection is not an artifact test. **OPEN:** no output artifact or device run was produced in this Web Manager cycle.

### 36. Bootstrap sequencing as an observable race, not an assumed defect [SOURCE / FAILURE MODEL]

The bootstrap launches `registerLogMateOfflineWorker()` asynchronously and immediately starts the Flutter engine. It does **not** await registration, worker activation, candidate precache or controller assignment before app startup. Its `navigator.serviceWorker.ready` handler posts `PROMOTE_VERIFIED_CANDIDATE` and `START_PRECACHE`; its one-shot `controllerchange` listener repeats these. The source intentionally avoids a blanket first-paint dependency on offline readiness.

**CONTRADICTION:** “The first screen rendered” is not evidence that a cold offline relaunch will work. Equally, “worker not yet controlling the first page” does not prove an implementation bug: the app can run online before offline preparation completes. A first-install test must distinguish **app rendered**, **registration exists**, **worker active/controlling**, **complete cache verified**, **network removed**, and **fresh process offline relaunch**. Record all six separately, and never silently label the first as the last.

### 37. Two-build acceptance and controlled failure-injection sequence [VALIDATION DEFINED NOT RUN]

1. **Reproducibility gate:** pin LogMate commit and toolchain, build ordinary and acceptance artifacts separately, retain each generated `logmate_service_worker.js`, offline manifest, verification output and SHA-256; reject unpinned mutable test URLs.
2. **Served-asset gate:** serve each build over HTTPS from isolated test origins, capture final response headers and SW registration scope; compare served worker and manifest bytes to built artifacts. A local `file://` run cannot validate this.
3. **First-install gate:** on clean profile record all six readiness stages in §36. Disconnect network only after separately observing complete verified precache, then terminate and relaunch; verify owner-safe task readiness, not merely an icon or shell pixels.
4. **Two-version gate:** keep old controlled client open, deploy version B, observe waiting/activation and client-build mapping, then close/reopen. Capture old/new JS, manifest and DB capability. Never infer DB rollback safety from retained cache bytes.
5. **Fault gate:** independently corrupt shell and font entries, exhaust quota, interrupt precache, interrupt browser process, and retry; distinguish expected fail-closed 503, successful verified old shell, and a user-visible recovery route. Do not clear IndexedDB to make an asset test pass.
6. **Owner gate:** seed all 37 stores with synthetic owner-A canaries in Engineering-approved harness; test deletion intent, old tab, bfcache, fresh startup B and write denial with exact repository calls. Only then extend to installed Safari and managed EFB. The normal release artifact still needs noninstrumented regression evidence.
7. **Files custody gate:** export an independent file, close browser, reopen it from the actual Files destination, validate checksum/owner/37-store completeness and restore on an empty permitted target. In-app “export success” is not external custody proof.
8. **Evidence gate:** classify `PASS`, `FAIL`, `NON-EXECUTION`, `NOT RUN` separately for Chromium, Safari tab, Safari Home Screen and managed iPad. Preserve negative controls and anonymized traces; avoid pilot or crew data.

**MINTTAP DECISION:** keep PWA release HOLD. Do not change `skipWaiting`, Cache Storage retention, `id`, hosting headers or schema rollback policy on static theory. These are Engineering-owned implementation choices pending exact-runtime evidence.

### 38. Cross-track bottleneck reallocation and stop decision [DEPENDENCY / TRANSFER VALIDATION]

Track **E** remains P0 for owner deletion, 37-store parity and durable independent backup; **A** owns the precise registration/activation/fetch/installed-container semantics in §§35–37. **C** owns the six-stage readiness oracle, quota interruption and accessibility/physical-device evidence; **B** consumes Design Studio W121 for honest offline-ready/update/recovery states; **D** consumes Marketing D9's product-claim HOLD and requires privacy-minimized, version-attributed success measurement rather than an install count. Software Engineering owns exact builds and source modifications. This transfer does not assert Design Studio Stage 3 PASS or product execution.

**Adjacent-question audit:** source commands and asynchronous bootstrap ordering were resolved here. The next question—whether the *generated served worker* actually meets the six readiness and two-version oracles—cannot be resolved by another source-only primer. It requires an Engineering-approved build/HTTPS/browser execution environment. Existing Native W-012 PASS remains valid only for its native scope; browser, Files and managed EFB remain OPEN. Stage 8 ACTIVE / Production validation OPEN / PWA release HOLD.
