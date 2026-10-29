# 526 — Stage 8: Offline owner continuity, same-origin ledger confidentiality and remote-rejection custody

Date: 2026-10-29 KST. Primary owner: **Track E — Web Architecture, Security & Operations**. Dependencies: A browser/storage mechanics, B offline/recovery UX, C independent browser/device validation, D privacy/discovery claims. State: **SOURCE + SYNTHESIS + TRANSFER + VALIDATION DESIGN; NO NEW PRODUCT RUNTIME EXECUTION**.

## 1. Problem, exact scope and boundary [SYNTHESIS]

An EFB iPad may need to keep an existing pilot logbook useful without network connectivity, while Firebase authentication can be stale, revoked or temporarily unreachable. At the same time, the entire ledger is stored in browser-managed IndexedDB. Three independent questions must be answered:

1. **Product access:** Does the LogMate app route a user to the ledger after observing the local owner binding and authentication state?
2. **Storage confidentiality:** Can another script executing in the same origin or a person with sufficient local device/profile access read the underlying browser storage regardless of the app's screen gate?
3. **Remote authority:** Can the cloud currently accept the Firebase UID for server operations, and how/when does an offline device learn about revocation?

A PASS on one does not establish the others. A local UID binding is not encryption. A locked Flutter route is not an IndexedDB access-control list. Firebase Auth session persistence is not an offline ledger backup. An online remote rejection cannot retroactively reach an offline device. Conversely, an unavailable server is not proof of rejection. These distinctions are essential for shared or managed EFB devices, account deletion, backup export, PWA installation and privacy copy.

This study extends 523 (Service Worker/CSP/cache), 524 (file custody), 525 (optional peer transport) and 522 (delta/clock). It does not re-study those topics or authorize new LogMate product behavior.

## 2. Historical problem → browser design principle → current standards [SOURCE]

Browsers isolate storage primarily by **origin/storage key**, not by application route, screen, account UID, local sign-out flag or JavaScript module. The W3C [Indexed Database API 3.0](https://w3c.github.io/IndexedDB/) defines opening databases within a storage key; [MDN same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy) explains that same-origin scripts can access the origin's IndexedDB, while scripts from another origin cannot simply read it. The boundary is **origin-wide**. A public support/auth page and the private app at different paths on the same origin are not separate confidentiality principals. This does not assert that the currently tracked public pages execute hostile code.

The [OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html) distinguishes client-side database data from server-authorized access and cautions against assuming IndexedDB confidentiality against script injection or local profile access. A malicious script already running under the app origin is a precondition for the script-based scenario; merely visiting an external site on another origin does not grant access.

[Web Cryptography Level 2](https://www.w3.org/TR/webcrypto/) distinguishes non-extractability of a CryptoKey from guarantees about its persistence, local physical protection and use by hostile scripts. A key that is non-extractable may still be **usable** by code with access to the key object, and browser storage can be deleted. Thus adding Web Crypto without a separate key-unlock and recovery threat model is not an automatic remedy. No LogMate ledger-at-rest encryption implementation or key custody is claimed in this study.

[Firebase Auth web state persistence](https://firebase.google.com/docs/auth/web/auth-state-persistence) documents LOCAL, SESSION and NONE, with default browser persistence when no override is set. This is a **Firebase JavaScript SDK general behavior**, not a measurement of the exact FlutterFire Web build, managed iPad context or LogMate Auth configuration. Do not infer that Safari tab and installed Home Screen PWA share a persisted Firebase session.

[WebKit tracking prevention](https://webkit.org/tracking-prevention/) states that Home Screen web app data is isolated from Safari and exempt from the first-party seven-day ITP deletion cap. [Safari 17.2 release notes](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/) specify a one-time cookie copy at Home Screen creation, **not** copying IndexedDB/localStorage. [Safari 26.0 release notes](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) describe user-controlled “Open as Web App” behavior; an icon or manifest alone does not establish the exact storage container. [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/) still permits quota failures and storage eviction. None of these sources proves a managed airline Web Clip's policy or an actual EFB backup.

## 3. Exact LogMate source and evidence, read-only [SOURCE]

Canonical LogMate **main 9cc0cd432a317d5dfebbe90e318fb219e53e024a**, inspected 2026-10-29. Relevant exact Git blobs:

- lib/repository/logbook/sembast_database_opener_web.dart **87f043d5** opens the Sembast Web database named **logmate_ledger**. The browser adapter uses IndexedDB. This establishes a local origin database surface, **not** proof that a specific malicious script accessed records.
- lib/repository/logbook/local_owner_access_codec.dart **47626ee7** encodes ownerUid and a local lock state (unlocked / lockedByExplicitSignOut) as structured repository metadata. It is an app-level access-state codec, not an encryption key or browser ACL.
- lib/application/logbook/local_ledger_access_coordinator.dart **3fd1bb71**: account-required startup refuses signed-out access; a bound, unlocked matching owner can continue; an explicitly signed-out owner requires reauthentication; a mismatched UID fails closed. Explicit sign-out first persists the local lock, then invokes Firebase sign-out. Local deletion state has its own lock.
- lib/app/session_gate.dart **5bcd6bf2**: for a fresh/unbound ledger, locally restored Firebase UID is remotely checked before binding; remote uncertainty fails closed for new ownership. For an **established** owner, cold-start remote validation has a **1,500 ms** budget, after which local startup may proceed and late result is processed. Resume initiates remote validation if applicable. A temporary network failure or indeterminate result does not revoke established local access; a positive rejection triggers guarded Firebase session clearing and rerouting without local record deletion. If guarded clear itself fails, established local decision can remain in force pending retry. These are explicit source behaviors, not evidence of an exploited flaw.
- lib/auth/auth_engine.dart **fcc23dcf** uses Firebase user.reload() for remote authority, with typed accepted, deleted, disabled, temporary-unreachable, changed and indeterminate outcomes. A stale remote response cannot clear a newer different UID. Do not treat currentUser or Auth listeners alone as fresh remote authorization.
- firebase.json **9ac0972e** serves build/web, declares catch-all Cache-Control no-cache/no-store, and rewrites /auth paths. It does not establish deployed CSP or the real CDN/edge response headers. web/index.html **01be7758**, web/auth/action/index.html **39d06a63** and web/account-deletion/index.html **f8558e92** are distinct routes under the tracked LogMate hosting arrangement. The public deletion page itself contains no active script in the inspected first-party HTML; do not manufacture an XSS claim.
- test/remote_session_gate_test.dart **23dc473b** and test/session_gate_test.dart **7727b338** contain bounded widget tests for network failure, late remote rejection, sign-out and owner mismatch. They are positive source/test artifacts, **not** production EFB, physical theft, browser-profile or exact deployed CSP validation.

The Engineering [S007 remote invalidation study](https://github.com/yhappcom/software-engineering-studio/blob/main/research/systems/S007_remote_session_invalidation_offline_authority_transfer.md) independently established local owner vs remote authority and leaves the post-positive-rejection local-data policy open. Its 2026-09-24 source context predates the current LogMate code; the current code is the stronger source for what is implemented now. The [Engineering Validation Standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) governs executable oracle requirements. The [approved Manual Delta contract](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md) still forbids automatic Push/Pull/Apply; SessionGate remote Auth validation is **not** Manual Sync or the permitted one-time lightweight latestSequence metadata check.

## 4. Authority algebra and operational decision table [SYNTHESIS / TRANSFER VALIDATION]

| Scenario | Locally bound ledger | Remote Firebase authority | Source-grounded app route | Security/data interpretation |
| --- | --- | --- | --- | --- |
| First use, unbound, cached UID, network unreachable | none | unknown | fail closed before creating owner | prevents stale UID from claiming a new ledger |
| Existing bound/unlocked UID, offline | established | unknown | preserve local-first access if Auth observation supports it | cloud freshness unknown; not server-authorized Sync |
| Existing bound/unlocked UID, delayed reload beyond 1.5s | established | pending | startup may proceed, late outcome processed | UI access is not a server acceptance receipt |
| Existing UID, reload network timeout | established | unreachable | preserve local access | never turn transport failure into deletion |
| Existing UID, positive disabled/deleted reload | established | rejected | guarded Auth clear and startup reroute | local data is not automatically erased; cloud denied |
| Positive rejection, guarded Auth clear fails | established | rejected, clear incomplete | local route may remain pending retry | explicit residual exposure/recovery policy question |
| Explicit sign-out | durable local lock | Firebase sign-out requested | require owner reauthentication | UI gate, **not** secure erasure of IndexedDB bytes |
| Different signed-in UID | ledger owned by another UID | mismatch | deny ledger route | prevents normal app-level cross-owner display |
| Same-origin malicious script after injection | any lock state | any | UI gate irrelevant to direct browser storage API | conditional same-origin storage disclosure/tampering risk |
| Safari tab → Home Screen installation | existing Safari container | not inherited by assumption | independent Auth/owner observation required | no implicit IDB transfer; one-time cookie copy is not a ledger copy |
| Storage eviction / app deletion | local data may disappear | unrelated | startup may appear fresh | restore requires separately retained verified .lbk |
| Device remains offline after remote account deletion | old local state | unobserved rejection | remote change cannot be delivered | no promise of instantaneous remote wipe |

**CONTRADICTION AVOIDED:** “remote rejection means immediate data deletion” conflicts with local-first preservation and the absence of a physical channel. “sign out means encrypted data inaccessible to all scripts” conflicts with origin-wide IndexedDB access. “PWA installed means data automatically migrates from Safari” conflicts with WebKit's storage separation. None is an acceptable launch claim.

## 5. Three attacker/failure models, with preconditions [SYNTHESIS]

**Model A — ordinary different user in the application.** The app-level UID comparison and explicit sign-out lock are relevant defenses. Tests should confirm wrong-UID and explicit-lock routes never render a private ledger. This is the narrow positive security property supported by source and widget tests.

**Model B — already-compromised same-origin JavaScript.** A hostile script executing at the LogMate origin can use same-origin browser APIs to inspect or alter origin-owned IndexedDB even if the Flutter app is currently showing a sign-in/locked screen. The route-level UI lock is not an API boundary. A public HTML route being under the same origin matters if it ever becomes an execution entry point; this does **not** prove a current injection vector. Connect to 523's conditional cached-Worker catalogue/CSP trust findings, which describe separate ways an already-compromised origin might retain malicious execution.

**Model C — local device/profile compromise, MDM removal or storage eviction.** Origin isolation does not itself prove confidentiality against someone with browser-profile/device privileges, nor availability after profile wipe. OS hardware protection, passcode, managed app policy and encrypted backups might mitigate some cases, but the specific airline controls are unknown. An unencrypted .lbk export can independently create disclosure risk even when the source PWA is well managed; see 524.

**Conditional cryptography:** If Engineering evaluates encryption at rest, it must define who supplies and protects the decrypt capability, how it survives offline restart, how logout/revocation affects key availability, whether same-origin hostile code can call decrypt, how backup/restore and key loss work, and how 37-store schema migration is made atomic. A non-extractable Web Crypto key alone is insufficient evidence. No new PIN, passkey, hardware-backed key, mandatory online unlock or server escrow policy is approved.

## 6. Architecture alternatives and decision pressure [MINTTAP DIRECTION, NOT PRODUCT APPROVAL]

| Option | Security benefit | Cost / failure / product consequence | Current judgment |
| --- | --- | --- | --- |
| Keep same-origin public + app; harden CSP and all script entry points | avoids migration and routing complexity | public/auth code execution shares origin storage trust; one weak entry may affect ledger | acceptable only after independent deployed CSP, Worker, dependency and origin-script review |
| Separate public support/marketing origin from ledger app origin | browser SOP isolates public-origin scripts from private app IndexedDB | domain/canonical/SEO, Firebase authorized domains, redirects, OAuth, cookie and Service Worker scope, links, hosting, app install, analytics and release complexity | **high-value design alternative to evaluate**, not a change order |
| Add optional short inactivity lock or reauthentication | reduces casual shoulder-surfing/shared-device exposure | may prevent legitimate cockpit offline access, increase recovery failures; UI lock still not encrypted storage | product/Design Studio decision pending threat/user research |
| Encrypt local ledger with independently protected unlock secret | may mitigate some device/profile read scenarios | key loss, offline recovery, Web Crypto script-use limits, performance, migration, backup and 37-store complexity | defer design choice until independent key custody/physical EFB risk proof |
| Server-mediated access for every read | simplifies fresh remote authorization | violates approved offline-first core and cockpit availability | **reject as default** under current LogMate contract |
| Treat remote rejection as destructive local wipe | can remove app-visible data on a connected device | irreversible pilot data loss, no reachability guarantee, deletion saga conflation | **reject as implicit Auth side effect**; deletion coordinator remains separate |

No evidence currently justifies declaring the managed EFB secure or insecure in the field. The most immediately actionable work is **independent source-origin/script policy verification plus exact device/Owner/restore tests**, before choosing costly encryption or origin migration.

## 7. Cross-track integration and transfer [DEPENDENCY / TRANSFER VALIDATION]

- **E primary:** owns origin-wide trust boundary, auth-versus-storage confidentiality, post-rejection policy and release HOLD; consumes Engineering S007 instead of rewriting Firebase internals.
- **A:** owns W3C storage key, WebKit Safari-tab/Home-Screen isolation, Firebase web persistence versus actual FlutterFire, and Service Worker scope. Standards support mechanisms, not physical EFB behavior.
- **B:** owns truthful user states: “Available offline”, “Account status not verified”, “Sign in required”, “Backup not verified” and “Cloud sync not completed” must remain semantically distinct. Design Studio Web W121 is execution-priority and Content Design is not a passed human comprehension gate; no approved final copy is inferred.
- **C:** owns negative controls, independently measured browser storage access, physical Safari/MDM, keyboard/VoiceOver and exact 37-store reopen/readback. Widget tests cannot attest to hostile script isolation.
- **D:** owns privacy/deletion/discovery implications. Marketing D8 product claims remain HOLD; do not advertise “end-to-end encrypted”, “instant remote wipe”, “safe forever offline”, “automatic sync” or “Safari-to-PWA seamless migration”. If app/public origins split, review redirects, canonicals, sitemap, account-deletion discoverability and privacy-aware analytics before deployment.

**RELATED DOMAIN CHECK:** Design Studio progress/WEB_STATUS Stage 3 practice, W121 runtime priority; Marketing main 2026-10-29 19:29 D8/D9 claim HOLD; Engineering S007 and Validation Standard; LogMate main 9cc0cd43. All consumed read-only, no cross-repo modifications.

## 8. Independent acceptance oracles LO01–LO22 [VALIDATION DEFINED — NOT RUN]

Use disposable synthetic 37-store ledgers, authorized Firebase Emulator/Admin identities, a dedicated test domain and device, and exact Git SHA/build/iPadOS/browser/MDM policy. Capture independent source/after hashes and semantic record/Owner/Replica/Outbox/Revision/Cursor state; never log real UID, flight data, credentials, or authentication tokens.

| ID | Independent test, including negative oracle |
| --- | --- |
| LO01 | Exact NORMAL Web build, deployed origin, actual headers, Worker scope and installed-mode provenance; no template-only substitution. |
| LO02 | Fresh/unbound ledger + restored UID + network timeout: no new Owner created, no Home reveal, no data mutation. |
| LO03 | Fresh/unbound ledger + positive same-UID remote acceptance: one Owner binding, duplicate callback idempotent. |
| LO04 | Established matching owner fully offline: Home and record save/read/reopen work without automatic server Push/Pull/Apply. |
| LO05 | Established owner, reload exceeds 1.5s then network failure: local work retained, no false “server verified”. |
| LO06 | Established owner, late positive disabled/deleted response: guarded Auth clear, reroute, no ledger deletion; inspect no stale Home exposure after routing. |
| LO07 | Rejection and guarded Auth clear failure: actual behavior captured and product-approved recovery policy recorded; no silent success. |
| LO08 | UID A stale reload response arrives after sign-in UID B: cannot clear B, rebind A, or reveal A's ledger to B. |
| LO09 | Explicit sign-out with Firebase sign-out failure: local durable lock persists; restart remains gated. |
| LO10 | App-level locked route vs independent same-origin IndexedDB API read in disposable fixture: demonstrate **UI gate is not browser storage ACL**; never use real user data. |
| LO11 | Different-origin fixture attempts same IndexedDB database access: cannot read app origin; distinguish from same-origin path and from browser extensions/profile compromise. |
| LO12 | Public support/auth route script policy, CSP, third-party dependencies, dynamic injection sinks and deployment headers reviewed; no unsupported claim of XSS. |
| LO13 | Worker cache/header tampering synthetic case from 523 repeated with separate ledger-origin access oracle; do not mistake fixture for exact product exploit. |
| LO14 | Safari tab and independently installed Home Screen context: record actual separate IndexedDB/auth/Worker state and one-time cookie behavior, if any. |
| LO15 | Same origin added twice as distinct Home Screen installations and managed Web Clip: test isolation or shared storage with exact OS/MDM; never infer from icons. |
| LO16 | Online Auth disabled/deleted while physical EFB offline: no instant revocation claim; reconnect and verify eventual typed rejection without data wipe. |
| LO17 | On-device passcode/MDM profile removal, app deletion, Web Clip removal and storage eviction in **approved disposable** context: compare data loss and recovery paths. |
| LO18 | Independent .lbk export → Files durable readback → fresh isolated destination same-UID restore: 37-store, new Replica, no cursor/ACK promotion; use 524 BF matrix. |
| LO19 | Encryption design *if proposed*: hostile same-origin script with access to key handles, device loss, offline unlock, key deletion, 37-store migration and backup recovery; no key-security claim from extractable=false alone. |
| LO20 | VoiceOver and interruption UX: distinguish offline-available, remote-unverified, remotely rejected, explicitly signed out and missing backup; no misleading status. |
| LO21 | Account deletion saga versus remote Auth disable: independent local lock, provider revoke, remote erase, local wipe and exported-copy warning; do not conflate. |
| LO22 | Release/privacy claims and origin topology: document security assumptions, exact app/public hosts, Firebase callbacks, CSP, canonical links, MDM evidence and operator recovery drill. |

**Oracle discipline:** tests must record claim → exact build/source → prestate → independently derived expected state → actual observation → verdict → limitations. Source inspection, simulated widget state, and a Chrome fixture each occupy different evidence rungs. No LO test was run in this cycle.

## 9. Operational judgment, explicit OPEN and next major checkpoint

**MINTTAP DIRECTION (research recommendation only):** Preserve approved local-first/offline access and non-destructive data custody. Make local UI gate, same-origin storage confidentiality and remote Firebase authority separate acceptance dimensions. Prioritize deployed-origin CSP/route audit and physical EFB/Owner/backup tests over a premature “encrypt everything” or “force online login” change. If an origin split is considered, Engineering owns deployment/auth changes, Design Studio owns user task states, Marketing owns external claims; Web Manager owns web-origin risk and cross-track requirements.

**OPEN:** actual deployed CSP/edge response headers; all active same-origin script sources; physical managed EFB profile; FlutterFire web persistence in exact installed context; session state across Safari/Home Screen/MDM; post-positive-rejection local data policy; optional at-rest encryption/key custody; backup UX/Files export; actual 37-store product readback; production deletion saga; origin-split feasibility. **CHANGE WATCH:** Safari/iPadOS install modes, WebKit storage eviction, Firebase Auth persistence and reload behavior, Web Crypto key handling, airline MDM restrictions.

**Gate remains:** Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD. This document is a substantive source-level cross-track checkpoint, **not** a new product runtime PASS or release approval. Before closing the study, the adjacent 523/524/525 failure models were cross-checked: cached hostile script → same-origin ledger access; backup exported outside managed origin → independent confidentiality; peer transfer → UID verification and durable apply. Those questions are integrated here; their physical/production tests remain separate and OPEN.
