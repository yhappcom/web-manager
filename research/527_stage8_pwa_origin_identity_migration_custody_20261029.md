# 527 — Stage 8: PWA origin separation, installed-app identity and lossless ledger migration gate

Evidence date: **2026-10-29 KST**. Primary owner: **Track E — Web Architecture, Security & Operations**. Track A owns browser-origin/manifest/Worker mechanics; B owns task continuity; C owns independent migration/device evidence; D owns crawl/measurement continuity. Status: **SOURCE + SYNTHESIS + MINTTAP DIRECTION + TRANSFER VALIDATION + VALIDATION DESIGN; NO PRODUCT MIGRATION OR DEVICE EXECUTION**.

## 1. Problem → principle → operational question [SYNTHESIS]

Study 526 established that an app-level owner lock is not an IndexedDB ACL: public pages and the ledger under one *origin* share the same browser storage principal. Separating public/support/auth surfaces from the private ledger is a plausible defense-in-depth option, but changing the private app's origin is not a harmless DNS or routing change. It can strand the only copy of an offline-first pilot logbook. **Security isolation and recoverability are both release-critical invariants.**

Distinguish four different changes: (1) path-only change on one origin; (2) move only public pages to a new origin while keeping the ledger origin unchanged; (3) move the private ledger to a new origin; (4) Safari-tab → installed Home Screen or MDM Web Clip container change, potentially with the same URL. Only (2) can potentially obtain meaningful public/private script isolation *without moving the ledger's existing origin*; (4) remains a separate container problem even if URL/host is unchanged. None is approved for LogMate.

## 2. Source authority and freshness [SOURCE]

- [MDN Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy), reviewed 2026-10-29: scheme + hostname + port define origin; IndexedDB/Web Storage are origin-separated. Paths are not security principals. Cookies have different domain/path rules, and must not be conflated with IndexedDB.
- [W3C Web Application Manifest Working Draft, 2026-10-26](https://www.w3.org/TR/appmanifest/): `start_url`, `scope`, `id` are distinct. Absent `id`, processed ID defaults to `start_url`; an ID must be same-origin as start URL. A new-origin app cannot simply declare an old-origin identity to inherit installation. Browser implementation and OS installation UI are **CHANGE WATCH**, not universal guarantees.
- [MDN Service Worker guide](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers): Service Worker registration/control/fetch are tied to origin and scope; a redirect does not copy the old registration, CacheStorage or IndexedDB to the destination.
- [WebKit Safari 17.2, 2023-12-11](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/): one-time cookie copying on Home Screen creation; **other local storage is not copied**. [WebKit Safari 26.0, 2025-09-15](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/): Home Screen entries default to web-app mode but users can choose a bookmark. Neither establishes a managed EFB Web Clip's storage identity.
- [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/): quota/eviction remain possible; installed status is not a backup.
- [Firebase redirect best practices](https://firebase.google.com/docs/auth/web/redirect-best-practices), reviewed 2026-10-29: when using custom-domain Firebase Hosting redirect auth, `authDomain`, authorized domains and `/__/auth/handler` may require coordinated changes. This is a **conditional requirement** for the exact provider/SDK flow, not proof that LogMate currently uses redirect sign-in.
- [Google Search Central site move](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes): old/new URL mapping, server redirects and monitoring matter for indexable public pages; SEO migration instructions do **not** migrate private browser data.
- [MDN postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage): explicit cross-origin communication is possible only between connected windows with checked `event.origin` and exact `targetOrigin`; this is not a storage-migration primitive by itself, and a compromised old origin could forge its outgoing data.

## 3. Exact current project source, read-only [SOURCE]

LogMate `main@9cc0cd432a317d5dfebbe90e318fb219e53e024a` checked 2026-10-29:

- `web/manifest.json` blob `8225e76f`: `start_url: "."`, `display: "standalone"`, **no explicit `id` or `scope`**. Under the W3C processing model, the resulting identity/scope depend on the resolved manifest/start URL; **do not infer an installed production app's actual identity** without its served URL and browser evidence.
- `web/index.html` blob `01be7758`: Flutter `<base href="$FLUTTER_BASE_HREF">`, external bootstrap, linked manifest. Build base-href and served root matter for navigation and manifest resolution.
- `firebase.json` blob `9ac0972e`: Hosting serves `build/web`, rewrites `/auth` variants to Auth Action, catch-all no-store header; **no documented origin split, migration bridge or installed-app transfer** in this file. Live DNS, Firebase Hosting aliases, custom domains, CSP and deployed response headers **UNKNOWN**.
- `lib/repository/logbook/sembast_database_opener_web.dart` blob `87f043d5`: browser IndexedDB-backed `logmate_ledger`. Local owner codec `47626ee7`, session gate `5bcd6bf2` and Auth `fcc23dcf` distinguish local owner and remote UID authority. None grants cross-origin IDB read.
- Approved `docs/specs/local-first-manual-delta-sync-contract.md` blob `2240fc1b`: independent local DB/Replica ID, first transfer by `.lbk`, same verified Firebase UID, empty destination, no silent overwrite/merge, later **user-initiated** Manual Delta Sync. P2P remains optional. An origin migration must not silently mint new Operations, change original timestamps or treat cloud Sync as a verified full restore.
- 524: `.lbk` integrity SHA-256 is not encryption/authentication; browser File handoff is not independent Files readback. 526: app UI lock not browser storage ACL. 523: root Worker/public-route and cached-header security gates still OPEN.

**No actual production hostnames, installed app IDs, real EFB policies or data volumes are inferred from repository templates.**

## 4. Architecture alternatives [SYNTHESIS / MINTTAP DIRECTION — NOT APPROVED]

| Alternative | Public/private origin isolation | Ledger continuity | Main failure mode | Judgment |
| --- | --- | --- | --- | --- |
| A. Same origin; public and app separated only by paths | **No** IndexedDB isolation | Existing origin may remain | Public-route script trust shared with ledger; CSP/Worker path interactions | Hardenable interim, not true storage isolation |
| B. Keep current ledger origin, move public/support/marketing pages to another origin | **Yes**, if all untrusted/public executable entry points genuinely leave app origin | Can preserve existing app origin and its local storage in same browser container | Old public URLs, Auth Action, deletion route, Worker scope, SEO and policy links need careful remapping | **Preferred first architecture experiment**, not approval |
| C. Move private ledger to new origin, retain old public origin | Yes | **No automatic IDB/Cache/Worker/session transfer** | Data abandonment, duplicate app installs, broken offline launches | **HOLD until independently verified user-controlled migration and rollback** |
| D. Separate only via subdomain/path alias with shared script deployment or wildcard CORS | Depends on real origin and script supply chain | Depends | Misconfigured CORS, cookies, OAuth or shared JS reintroduces exposure | Reject as isolation claim without exact header/runtime proof |
| E. Safari tab to Home Screen or MDM Web Clip, unchanged origin | URL may match, **container may not** | No assumed IDB transfer | User sees empty ledger, old records still in tab, old app removed | Treat as independent migration requiring backup/readback |

For B, moving the public page off the ledger origin only helps if the old app origin does not continue serving equivalent executable public/auth routes. A public page can remain indexable on a separate origin while authenticated ledger routes are deliberately nonindexable; exact robots/canonical and account-deletion obligations require review. An iframe or shared third-party script loaded *into the app origin* still executes with the app document's privileges unless properly sandboxed; moving a URL alone is not an XSS cure.

## 5. Why 301/302, manifest id, CORS and OAuth are not ledger transport [SYNTHESIS]

- **HTTP redirect:** browser navigates to a new origin. Its old IDB, CacheStorage, service worker and owner lock remain in the old storage key. A permanent redirect can also prevent users from reopening the old offline-capable migration UI; do not deploy before custody proof.
- **Manifest identity:** an `id` describes installation identity, not a browser storage capability. A new-origin `id` is not a same-origin continuation of the old one. No standard automatic ledger copy follows changing `start_url`, `scope` or `id`.
- **CORS:** governs selected cross-origin network response access, not permission to open another origin's IndexedDB. Credentialed CORS and overly broad origins can create a separate server-data risk.
- **Cookies/Firebase:** parent-domain cookies may cross subdomains under explicit Domain rules, but Firebase Web session persistence may use browser storage, and Safari installed containers are independent. An OAuth login success is not proof of restored local ledger. Provider redirect/auth-domain changes require exact flow validation.
- **Cross-window postMessage:** can carry deliberately exported data after a verified handshake, but requires both windows live, precise origin checks, replay protection, size/transaction/error handling, user consent and authenticated Owner binding. It creates a new high-risk data-transfer channel and must not bypass the approved `.lbk` contract.
- **Manual Sync:** only user-initiated deltas, not an implicit full-state bootstrap; it cannot be used to justify silent old-origin deletion or success when no complete server snapshot exists.

## 6. Migration safety invariant [MINTTAP DIRECTION]

Define a synthetic source ledger S and destination D. A proposed migration is eligible only if all hold:

1. **Source custody:** S remains readable, unmodified and independently recoverable until after a verified destination restore and user acknowledgment. A redirect must not destroy access to S before this.
2. **Owner:** verified same Firebase UID; mismatched/unknown owner fails closed without mutating D. Offline status cannot be upgraded to remote-authorized status.
3. **Data completeness:** semantic 37-store records, metadata, Owner, revisions, history, outbox, applied cursors, tombstones, structure, baseline, file attachments (if applicable) and aggregate consistency independently match the approved backup contract. Raw byte equality is not sufficient across schema versions.
4. **Replica semantics:** new independent local DB gets new Replica ID; original Operation IDs, timestamps and stable Record IDs remain unchanged; no accidental new user Commands.
5. **Atomicity:** partial, interrupted or quota-failed restore never leaves an apparently successful usable half-ledger; retries are idempotent and no nonempty destination is overwritten silently.
6. **Independent backup:** user can read exported `.lbk` bytes from an independently retained Files location; same-origin Blob/OPFS is not a backup. A checksum mismatch or unsupported schema blocks restore.
7. **Offline capability:** new installed app's shell and data reopen without network, with no unverified automatic Sync. Old installed app stays recoverable during rollback.
8. **Truthful UX:** `Export prepared`, `File saved/read back`, `Restore validated`, `Destination available offline`, `Cloud synchronized` are separate statuses.
9. **Security:** neither migration bridge nor Auth callback exposes UID/token/flight data in URL, Referer, CSP reports, analytics or public logs; CSP and script authority remain controlled.
10. **Policy:** managed EFB Web Clip, Files provider, MDM Open In, install mode and uninstall policy independently verified on a permitted device.

These are acceptance requirements, not assertions that any existing LogMate build passes them.

## 7. Failure-first scenarios and rollback [SYNTHESIS / VALIDATION]

- **New origin opens as empty ledger:** display recovery state, not onboarding that silently binds a fresh UID and invites conflicting edits. Keep old source and backup intact.
- **Old origin redirects before export:** migration is blocked; restore the old offline-capable path and avoid destructive cache/registration cleanup.
- **Network fails after file export but before new-origin auth:** retain independently saved backup and old ledger; do not imply cloud synchronization.
- **File saved but zero-byte/truncated/corrupted:** readback, schema/digest and semantic checks must fail before destination commit.
- **Old and new apps both used:** independent Replica IDs and user-controlled Manual Sync must preserve immutable Operation IDs; avoid accidental duplicate first transfer into nonempty DB.
- **MDM removes old Web Clip or blocks Files:** do not launch an origin move until a policy-approved transfer and restore path is demonstrated; old device might not be recoverable after removal.
- **Browser storage pressure or WebKit eviction:** never claim installation/persistence API alone is a disaster-recovery strategy.
- **Auth provider redirect breaks on new host:** separate login availability from ledger restore success; rollback without erasing local records.
- **Public page migration causes account-deletion route 404:** D must prove public policy URL availability, redirects, index/canonical and form continuity; do not treat search ranking as data-custody proof.
- **Old Worker controls old public tab:** root Worker may still intercept CSS/GET; validate 523 §22–24 before assuming public-site move solves existing client-control behavior.

**Rollback rule:** preserve both old origin and old installed launch while the new destination is validated; never use automatic old-cache/IDB deletion as a cleanup step. Define a product-approved end-of-support and data-retention policy only after migration is independently complete.

## 8. Five-track allocation and external transfer [DEPENDENCY / TRANSFER VALIDATION]

| Track | Current gate/pressure | Contribution, without duplicating canonical discipline |
| --- | --- | --- |
| **E** | Stage 8 primary bottleneck; high data-loss/security consequence | Own migration trust model, deployment phases, rollback, CSP/Owner/privacy policy, release HOLD |
| **A** | Browser prerequisites essential; standard-source maturity higher than physical evidence | Origin/storage/Worker/manifest semantics; WebKit container and Chromium differences; installation CHANGE WATCH |
| **B** | Recovery UX cannot be designed truthfully until status distinctions are fixed | Task state and non-destructive user journey; consume Design Studio W121 rather than restyling |
| **C** | Independent physical/installed/runtime validation absent | Device/browser/MDM/37-store, interrupted restore, VoiceOver and keyboard test oracles; no score-only pass |
| **D** | Marketing D8/D9 product claim HOLD; SEO transfer pressure | Indexable public URL move, account deletion/support continuity, privacy-safe acquisition measurement; no “seamless transfer” claim |

**RELATED DOMAIN CHECK:** Design Studio `progress/WEB_STATUS.md` Stage 3 PRACTICE/W121 execution priority, no human/physical gate; Engineering `methods/VALIDATION_STANDARD.md` independent claim→oracle chain and S007 remote authority; Marketing `STATUS.md` 2026-10-29 D8 claims HOLD/D9 deferred; LogMate exact approved Manual Delta contract. All read-only. No peer/product repository writes.

## 9. Exact-product acceptance matrix OM01–OM24 [VALIDATION DEFINED — NOT RUN]

Use disposable synthetic full-schema data, an authorized test Firebase project/UID, distinct test origins, explicit browser profile/container provenance and approved MDM device. Record repository SHA, built asset hashes, URLs, Worker registration/control scope, manifest parsed identity, browser/iPadOS version, device policy, and independent pre/post semantic digest. Do not store real pilot records or secrets in CI.

| ID | Independent oracle |
| --- | --- |
| OM01 | Enumerate actual deployed old/new scheme-host-port, served headers, DNS/Hosting and Worker scopes; template alone is not proof. |
| OM02 | Same-origin different paths share IDB; distinct origins cannot directly open old IDB; include negative controls. |
| OM03 | Old origin redirect to new origin does **not** populate new IDB/Cache/Worker; prove no automatic copy. |
| OM04 | Current manifest `start_url "."`/missing `id` resolves to measured old installation identity; record exact served URL. |
| OM05 | Proposed new-origin manifest yields distinct identity/installation under actual Chrome and Safari; no assumed icon continuity. |
| OM06 | Existing installed old app remains offline-launchable during migration; no premature 301/Worker cleanup. |
| OM07 | Old Worker `clients.claim()` and unassigned public GET behavior on real build, including CSS/auth assets. |
| OM08 | Public-only origin split: no app-ledger IDB read from public origin, while app origin retains original data. |
| OM09 | Public/auth scripts and dependencies actually absent from app-origin execution surfaces after split; CSP verified in responses. |
| OM10 | Exact Firebase Apple/Google/email flow per provider on both origins; authorized domains/redirect/continue URI independently checked. |
| OM11 | Safari tab and Home Screen same URL: record separate IDB/Cache/Auth/Worker contexts; no assumed non-cookie transfer. |
| OM12 | Safari 26 web-app versus bookmark toggle and managed Web Clip: classify real container before any restore. |
| OM13 | Independent `.lbk` export → Files saved/readback → digest/schema verification, including no-network and quota stress. |
| OM14 | Same UID + empty new-origin DB restores 37-store semantics, baseline/history/Owner/Outbox/Replica/Cursor correctly. |
| OM15 | Wrong UID/unknown authority/nonempty destination fails closed with source/destination untouched. |
| OM16 | Mid-restore crash, partial write, quota error, corrupt file, unsupported schema: no false success; retry idempotent. |
| OM17 | Old and new origin concurrently used: no duplicate Operation ID or timestamp rewrite; conflict policy explicit. |
| OM18 | After successful restore, new installed PWA relaunches offline with exact saved records and no implicit Push/Pull/Apply. |
| OM19 | Remote disabled/deleted versus transport-unreachable states remain distinct; no automatic local wipe. |
| OM20 | MDM Files/Open In/Web Clip removal policies exercised on real permitted EFB; untested policy remains OPEN. |
| OM21 | Keyboard/VoiceOver, focus and interruption recovery across export, install, restore and rollback. |
| OM22 | Public support/privacy/account-deletion URLs, redirect status, canonicals, sitemap, Search Console continuity independently checked. |
| OM23 | No UID, auth code, backup payload or flight data in URL/referrer/CSP reports/analytics; negative privacy probes. |
| OM24 | Independent post-restore readback and human acceptance; source retained until signed-off rollback window, no automatic deletion. |

No OM test was executed in this study. Browser standards, source inspection and prior synthetic 526 6/6 are **not** OM PASS.

## 10. Decision and next evidence [MINTTAP DIRECTION / OPEN]

**Provisional architecture recommendation:** first evaluate moving *public* surfaces away while **preserving the ledger's existing origin**; do not move the private app's origin as a routine security fix. Before either change, resolve 523's existing Worker/public-route behavior, Auth Action CSP/report privacy and account-deletion route contradiction. For any app-origin move or Safari-tab→installed/managed container transfer, require `.lbk` independent Files custody, same-UID empty-target restore, full-schema semantic readback and physical EFB policy proof. This is a research recommendation, **not** an authorized product architecture change.

**OPEN:** actual served LogMate domain(s), Firebase provider flow/authorized domains, managed EFB MDM and Files policy, installed-app manifest identity, old/new Worker runtime, full-schema migration/backup implementation and independent user acceptance. Engineering owns any code/production test. **Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**

**CHANGE WATCH:** W3C manifest ID/scope WD 2026-10-26; WebKit installed container and Safari26 user toggle; Firebase Auth redirect behavior; browser storage partitioning/eviction; Google indexing moves. Re-check primary sources when an actual deployment proposal or version change arises.


## 11. Applied origin-split preflight: Auth, cookies, routes and synthetic browser falsifiers (2026-10-29)

**Evidence classification:** SOURCE / SYNTHESIS / CONTRADICTION / MINTTAP DIRECTION (provisional) / DEPENDENCY / VALIDATION DESIGN / CHANGE WATCH. **Owner:** E security and operations; A browser/origin mechanics; B task continuity; C browser and physical-device quality; D discovery/canonical/measurement. **No product changes, production tests or approval.**

### 11.1 Exact current LogMate source and route inventory [SOURCE]

Read-only LogMate main **9cc0cd432a317d5dfebbe90e318fb219e53e024a**, checked 2026-10-29:

| Source (Git blob) | Observed source fact | Consequence for proposed public-only split |
| --- | --- | --- |
| firebase.json (9ac0972e) | Single tracked Hosting public root **build/web**, global no-store header, three Auth Action rewrite aliases: /auth, /auth/, /auth/action | No second public host, DNS mapping or deployment is established. Served aliases/headers remain unknown. |
| web/auth/action/index.html (39d06a63) | Inline module/style, Firebase gstatic 11.10.0 imports, **authDomain = logmate.minttap.app**, URL **oobCode** consumption | Auth Action is an authenticated, executable surface, not a generic marketing page. Moving it requires separate provider, action-link, redirect, session and CSP validation. |
| web/about/index.html (947aae88), support (d185fc88), privacy (ca465aaa), terms (2c83da66), account-deletion (f8558e92) | **5/5** selected pages contain hard-coded canonical URLs on https://logmate.minttap.app; navigation, CSS and icons are root-relative | Copying HTML to a new host without rewriting canonical/internal routes and assets can leave wrong discovery targets or broken user tasks. This is a tracked-source census, not a live crawl. |
| web/public.css (755b5c73), web/index.html (01be7758) | Public pages request /public.css; Flutter shell has build-time base href and relative manifest/bootstrap | Public assets must exist on the new host; shell base/entry cannot be silently repointed. |
| web/manifest.json (8225e76f) | Relative start_url "." and no explicit id or scope | Resolved start URL/derived manifest ID can differ after host/base-path changes; actual installed identity still requires browser/device evidence. |
| tool/pwa_precache.dart (90a67954) | Root-scoped Worker generator reserves Auth paths, calls clients.claim and uses client-build mapping for other GETs | Old public tabs and old-host redirects can remain subject to Worker control/asset routing. See 523 §§22–26. |

**Important contradiction:** Option B in §4 can isolate the **five informational pages** without moving the private ledger, but if Auth Action stays on the ledger origin, its Firebase imports still execute in a document with that origin's privileges. This does **not** establish malicious Firebase code, XSS, a ledger read or a product breach. It prevents the broader claim that moving static public pages automatically isolates *all* public/auth executable content. Moving Auth Action too is a materially different authenticated-product migration.

### 11.2 Four distinct security/continuity boundaries [SOURCE / SYNTHESIS]

1. **Origin** (scheme/host/port): IndexedDB, CacheStorage and Service Worker authority are origin-specific; paths are not storage principals. Distinct ports can create distinct script-storage origins, but are not equivalent to production subdomains for every browser feature.
2. **Cookie scope** differs: cookies are host/domain/path scoped and do **not** include port. A host-only cookie does not automatically reach sibling subdomains, but an explicit parent-Domain cookie can. A public/private origin split is **not** sufficient proof of credential-cookie isolation. Audit actual Set-Cookie Domain, Path, SameSite, Secure, HttpOnly, prefix and server CSRF/session policy; do not assume LogMate currently uses a particular cookie.
**Additional same-site counterexample:** two HTTPS sibling subdomains can be **cross-origin but same-site** (scheme + registrable domain). Therefore SameSite=Strict/Lax alone does not prevent every cross-subdomain request or substitute for server-side CSRF/Origin validation. A parent-Domain cookie may be sent to both subdomains, subject to cookie attributes and browser context. This is a standards-derived *conditional* attack-surface requirement, **not** evidence of a LogMate cookie, CSRF vulnerability or live subdomain topology. See [MDN Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy), [MDN Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies) and [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie).

3. **Installed container** differs: WebKit Safari 17.2 documents one-time cookie copying into a new Home Screen web app while other local storage is not copied. A changed origin and a new installed browser container are separate migration axes. MDM Web Clip classification is still open.
4. **Account authority** differs: Firebase sign-in on a new host, verified same UID, successful 37-store restore, independent backup and cloud Sync ACK are separate assertions. An origin handshake is not identity authentication or ledger migration.

Primary sources checked 2026-10-29: [W3C Web Application Manifest](https://www.w3.org/TR/appmanifest/), [MDN Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers), [MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie), [MDN Storage Access API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API), [Firebase redirect best practices](https://firebase.google.com/docs/auth/web/redirect-best-practices), [Google Identity Platform custom handler](https://docs.cloud.google.com/identity-platform/docs/show-custom-domain), [WebKit Safari 17.2](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/). Cookie/partition, manifest installation, provider redirect and WebKit behavior are **CHANGE WATCH**, not universal cross-platform guarantees.

### 11.3 Architecture choices and failure-first judgment [SYNTHESIS / MINTTAP DIRECTION — NOT APPROVED]

| Candidate | Advantage | Residual/new risk | Gate |
| --- | --- | --- | --- |
| B1 — move **five static informational pages only**, keep ledger and Auth Action at original origin | Keeps original local ledger origin; reduces unrelated public-page script exposure if no old executable copies remain | Auth Action/gstatic scripts remain on ledger origin; root Worker and cookie/auth routes need separate hardening; canonical/Store links may break | **Preferred bounded experiment**, not complete Auth isolation |
| B2 — move informational pages **and Auth Action** | More complete document-origin separation | Hard-coded authDomain, action-link destination, /__/auth/handler, authorized domains, popup/redirect and session transfer, CSP/report privacy; unproven cross-origin credential handoff | **HOLD** until Engineering-specific threat model and real provider/browser validation |
| B3 — keep all routes, harden CSP/Worker | Avoids origin/data migration | Same-origin public/private storage authority persists; cached-header/catalogue threats not automatically fixed | Possible containment, not storage isolation |
| C — move private ledger origin | Could isolate if complete | IDB/Cache/Worker/manifest/owner continuity lost unless independent Files backup and same-UID 37-store restore verified | **HOLD** under OM13–OM24 |

Firebase Auth helper routes and the Auth Action rewrite are not interchangeable. Firebase's primary documentation explicitly requires correct authDomain/handler/provider configuration and notes that a plain HTTP 302 is not an equivalent transparent helper proxy. Do not infer that every LogMate platform uses redirect sign-in merely because the Auth Action file contains Firebase imports.

### 11.4 Synthetic Chrome mechanism experiment [VALIDATION — LOCAL NON-EXECUTION / HOSTED OUTCOME OPEN]

Committed [research-only 12-case browser probe](handoffs/pwa_origin_split_browser_probe.py) and [hosted CI](../.github/workflows/stage8_pwa_origin_split.yml) to **Web Manager only**. The fixture creates two HTTP loopback servers with the **same hostname and different ports**, disposable IndexedDB/CacheStorage, a synthetic Worker, redirect, cookie and postMessage handshake. It intentionally contains no LogMate source, pilot data, credentials or Firebase project.

Twelve independent intended observations: old origin seeded; same-origin public path can read synthetic IDB; different origin lacks both IDB and CacheStorage; host cookie is shared across ports despite different origins; cross-origin Worker registration rejects; old Worker controls only old origin; redirect does not transfer IDB; old source survives redirect; exact sender-origin postMessage check rejects a wrong-origin message; a handshake alone does not restore IDB; and relative manifest start URLs resolve separately. This is a **mechanism falsification suite**, not a production migration test.

**Execution truth:** Python 3.13 syntax compilation PASS on draft. Local Chromium navigation to loopback failed at the first request with **ERR_BLOCKED_BY_ADMINISTRATOR**, so **zero local browser cases ran**. Hosted workflow targets Ubuntu 24.04 / Python 3.13 / Playwright 1.57 / installed Chrome; **hosted result not verified at this checkpoint**, so no synthetic 12/12 PASS is claimed. A future hosted PASS requires inspecting exact checkout, job logs, browser observations and artifact. Even then, distinct-port cookie behavior does **not** prove actual HTTPS sibling-subdomain cookies, nor Safari, Home Screen, MDM, LogMate Auth, real 37-store or installed identity.

### 11.5 Existing OM01–OM24 acceptance amendments, not a duplicate test catalogue [VALIDATION / DEPENDENCY]

- **OM01/07:** enumerate exact served old/new origins and root Worker registration/control; test old-host redirects with controlled old tabs, public CSS, auth fonts/icons and unrelated GET.
- **OM08/09:** after a proposed B1 split, enumerate *all remaining executable app-origin documents* (especially Auth Action and Firebase imports), old aliases and CSP. Public-static separation must not be represented as all-script separation.
- **OM10/23:** disposable email verify/reset, Apple/Google popup/redirect/link/reauth, authDomain, provider authorized URLs, initial query, Referer/CSP-report/edge-log custody. A successful HTTP redirect is not successful Auth.
- **OM11–16/20:** distinguish Safari tab, installed Home Screen and managed Web Clip; require independently retained .lbk Files bytes, same-UID empty-destination full 37-store semantic restore, rollback and no silent Sync.
- **OM22:** verify **5/5** canonical tags, root-relative navigation/asset paths, Store/support/privacy/account-deletion URLs, redirects and real Search Console continuity. Do not canonicalize the new host back to the old unintentionally.
- **OM23 cookie negative controls:** host-only vs parent-Domain, HttpOnly/Secure/SameSite, same-site subdomain requests, CSRF/session fixation, logout continuity on **real HTTPS**. Synthetic port test is only a prompt for these oracles.

**RELATED DOMAIN CHECK:** Design Studio progress/WEB_STATUS.md is Stage 3 PRACTICE / W121 runtime gate; do not duplicate visual design. Software Engineering methods/VALIDATION_STANDARD.md requires claim→target→oracle→environment→observation→limit and owns actual product code/build/MDM tests. Marketing STATUS D8 product claims HOLD and D9 deferred; do not advertise seamless migration. All peer/product repositories read-only.

### 11.6 Adjacent-question check and next checkpoint [OPEN / MINTTAP DIRECTION]

The next concrete decision is whether the **five static informational pages** can leave the ledger origin without breaking canonical/Store/deletion/support tasks **while residual Auth Action and Worker authority are separately hardened**. This source-and-browser preflight can advance now; a full Auth Action move is a materially different security/session migration and must not be silently bundled with it. Actual deployed hosts, Firebase provider console, exact NORMAL artifact, Safari/managed EFB, 37-store Files roundtrip and production release authority remain UNKNOWN.

**Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.** No origin split, Firebase config change, product code change, real pilot data or physical-device execution. Next: inspect hosted Chrome job, correct fixture failures if any, then Engineering-approved exact product route/Auth/Worker and physical EFB evidence.
