# 322 — Stage 8 PWA Security-Header Side Effects, Irreplaceable Local Data & Authentication Interoperability

**Checkpoint:** 2026-10-10 Asia/Seoul. **Owner:** Track E (web security/operations); A owns browser origin, fetch, Service Worker and storage mechanics; C owns executable negative oracles; B owns user-visible hold/recovery semantics; D owns privacy-preserving reporting. Web Manager coordinates, not a sixth specialist.
**Gate:** PASS — generic standards + source-bounded risk diagnosis; **no LogMate production/header change, browser execution, current-head normal PWA build, physical Safari/MDM, loss incident, or restoration PASS is claimed**.
**Canonical refs inspected:** Web Manager `main@2cd71c37cc8d513ca0c9ebf6033e222c3853a0f3` (AGENTS, SPECIALIST_TRACKS, LEARNING_ROADMAP, STATUS, research index, 320–321); LogMate `main@827a7deed162bf525313c6b4b9d244e56828a1c1`; Design Studio W103/W117; Engineering S007; Marketing Manager STATUS (2026-10-10).

## 1. HISTORY / PROBLEM → DESIGN PRINCIPLE

Security response headers are often treated as harmless, additive hardening. That assumption fails for offline-first PWAs: some headers are **imperative state-changing instructions**, others change browsing-context relationships or produce diagnostic telemetry. The same origin can host an offline ledger, login/action page, and Service Worker; a response to one route can affect storage and sessions used by another route. The most severe failure mode is a well-intentioned worker recovery or logout change that removes the only unsynchronized local records. Conversely, withholding all containment after a genuine origin compromise can preserve malicious persistence. The design principle is **consequence-scoped response-header governance**, not "always add all security headers."

Keep four separate questions: (1) Does the header protect confidentiality/integrity? (2) Can it mutate local state or disable required Auth/OAuth paths? (3) Does it work in the exact browser/install context? (4) Can the app recover unique local records and safely reestablish authority? A header is not a verified recovery plan.

## 2. SOURCE — primary and current platform evidence (reviewed 2026-10-10)

- W3C Clear Site Data editor's draft (10 Nov 2023, work in progress): https://w3c.github.io/webappsec-clear-site-data/ . `Clear-Site-Data: "storage"` targets origin DOM storage including IndexedDB and Service Worker registrations; `"cookies"` affects cookies at a broader registered-domain boundary; `"cache"` targets caches; `"*"` is deliberately forward-extensible. The 2017 published WD is older; do not call this a final Recommendation.
- MDN Clear-Site-Data (last modified 2025-11-21): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data . It explicitly lists IndexedDB deletion and Service Worker unregistration under `"storage"`, distinguishes `"cache"`, and cautions that directive/browser support varies.
- Chrome/Workbox "Removing buggy service workers" (last updated 2021-10-20): https://developer.chrome.com/docs/workbox/remove-buggy-service-workers . A no-fetch-handler replacement Worker at the **same script URL** is a recovery option; Chrome expressly warns that `Clear-Site-Data: "storage"` also clears IndexedDB/localStorage/sessionStorage and is not universally supported. The document's statement that "damage isn't permanent" concerns fixing buggy Worker behavior, **not** recovery of unsynced user data.
- WebKit Safari 18.4 release (2025-03-31): https://webkit.org/blog/16574/webkit-features-in-safari-18-4/ . WebKit documents first-party cookie clearing introduced in Safari 17.0, partitioned-cookie clearing in 18.4, and removal of `executionContexts` support in Safari 18.4. This is **not evidence of Safari parity for every Clear-Site-Data directive**, Home Screen partition, or managed Web Clip.
- Firebase Hosting configuration: https://firebase.google.com/docs/hosting/full-config . Custom-header patterns match the **initial request URL before rewrites**; matching rules apply in defined order. A header on `/auth/action/index.html` alone does not establish that `/auth`, `/auth/`, `/auth/action` receive it.
- W3C CSP Level 3 Working Draft (2026-09-16): https://www.w3.org/TR/CSP3/ ; MDN Reporting API: https://developer.mozilla.org/en-US/docs/Web/API/CSPViolationReport . Report-only can send document URL/report fields containing query capabilities; treat collector ingestion and observability as a separate sensitive-data path, not solved by Referrer-Policy alone.
- MDN COOP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy ; Firebase Google sign-in: https://firebase.google.com/docs/auth/web/google-signin . `same-origin` may sever opener/popup references; `same-origin-allow-popups` is a conditional compatibility pattern, **not a universal safe OAuth fix**. Firebase documents popup and redirect variants, with redirect preferred on mobile.
- RFC 9111 HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111 ; Service Worker: https://w3c.github.io/ServiceWorker/ . `Cache-Control: no-store` is not `Clear-Site-Data`; HTTP cache, Cache Storage, local IndexedDB and remote authority are independent.

## 3. SOURCE — pinned LogMate facts and explicit non-facts

- `firebase.json` blob `dfa9aa132acca6f69ea032b838bdbb0640e08bbf`: global `Cache-Control: no-cache, no-store, must-revalidate`; three auth aliases rewritten to `/auth/action/index.html`, then catch-all SPA fallback. **No `Clear-Site-Data`, COOP, CSP, Referrer-Policy or nosniff custom header is declared in this pinned file.** This is **not** evidence of all actual CDN/proxy/live response headers.
- `web/auth/action/index.html` blob `39d06a633ab7bee719b3401bc3ac744f8ba175d0`: dedicated account action page; `<meta name="robots" content="noindex">` is already present. Firebase action URL parsing and auto-apply distinctions are owned by study 321; do not repeat its primer.
- `research/320` establishes that Sembast Web stores local ledger data in an IndexedDB-backed context and that a logical capability-v15 marker is **not** necessarily a physical IndexedDB schema version. Local records, Custom definitions/values, baseline, drafts, receipts and pending outbox may be uniquely valuable; no production durability claim follows from this.
- Engineering S007 requires Firebase UID owner authority and fail-closed identity mismatch/recovery. Signing out or account-link failure is not authorization to destroy a different owner's offline ledger.
- No current source evidence indicates LogMate actually deploys a destructive header or has suffered local data loss. This study defines a **future-release/incident negative guard**.

## 4. SYNTHESIS — seven independent security/control planes

**P1 Response-route scope:** Firebase headers apply to the original URL. Auth aliases, exact file path, `/__` reserved helpers, SPA shell, missing assets and Service Worker script require separate response captures. A path-level "security hardening" change can have origin-wide consequences even when only one route receives the header.

**P2 State-destructive instructions:** `Clear-Site-Data: "storage"` can delete the IndexedDB-backed ledger and unregister Workers; `"*"` is wider. A server's successful 200 response does not make this safe. No response header can determine whether a device has unsynced flights; a remote operator cannot infer safe deletion from server ACK count or login state alone.

**P3 Session vs data:** Sign-out may require revoking session/credential access while preserving locally owned unsynced records in a quarantined, non-disclosed state. Preservation is not authorization to reopen under a different UID. Account deletion may require erasure but must use a verified, policy-governed data-domain and offline-return contract (318–319), not accidental blanket clearing.

**P4 Worker incident containment:** Replacing a buggy Worker with a no-op Worker at the same URL can neutralize fetch interception without issuing origin-wide storage erasure. However `skipWaiting()`, forced navigation, active edits, old tabs, cached shell and offline re-entry still need testing. A compromised origin is a different threat: a no-op Worker alone may not reestablish trust; incident authority and data-provenance handling remain OPEN.

**P5 OAuth browsing contexts:** Applying strict COOP globally may disrupt popup-based Auth; choosing a weaker COOP solely to make tests green may sacrifice isolation. Determine actual product flow, browser/OS, helper route and opener needs; test both popup and redirect where applicable. A generic CSP copied onto the Flutter shell or Firebase `/__` can similarly break resources/Auth.

**P6 Diagnostic confidentiality:** CSP Report-Only reports, server access logs and same-origin referrers may contain `oobCode` URLs. Sanitization must precede collector storage/forwarding; sampling after ingestion is insufficient. Disabling all reporting is not the only option: exclude capability-bearing routes from raw external reporting or deploy a trusted pre-ingest scrubber with sentinel tests.

**P7 Rollback asymmetry:** Restoring old Hosting bytes or a worker cannot reverse client-side IndexedDB deletion. Preview-origin data survival does not establish production-origin survival. Backups require independent, executable recovery with owner/provenance checks, not only "persistent" storage or a stale device snapshot.

## 5. MINTTAP DECISION — proposed response-header governance (NOT SHIPPED)

| Header / change | Intended benefit | High-value failure to prevent | Release stance |
| --- | --- | --- | --- |
| `Referrer-Policy: no-referrer` on action aliases | Prevent Referer propagation | Missing alias, late JS-only mitigation | Candidate; capture all entry responses before promotion |
| `Cache-Control: no-store` on action | Avoid HTTP caching | Mistakenly interpreted as IndexedDB erasure or Worker isolation | Candidate; verify actual response and Worker route |
| CSP enforce/report-only | Reduce injection / observe violations | OAuth/SDK breakage; `oobCode` in reports | Route-scoped, privacy-safe, executable compatibility gate |
| `X-Content-Type-Options: nosniff` | Enforce resource MIME boundaries | HTML-200 fallback makes missing JS/WASM fail | Pair with real 404/MIME/digest negative tests |
| COOP / COEP | Isolation and cross-origin controls | Popup Auth / external resources break | Do not apply blindly; exact Auth/browser matrix |
| `Clear-Site-Data: "cookies"` | Session-cookie cleanup | Registered-domain collateral session effects | Require owner/provider/domain audit; not automatic on action GET |
| `Clear-Site-Data: "cache"` | Browser cache invalidation | Unintended offline availability regression | Prefer explicit versioned asset/Worker strategy; test |
| `Clear-Site-Data: "storage"` or `"*"` | Emergency client purge | Irrecoverable unsynced IndexedDB ledger/outbox loss | **HOLD / prohibited as routine auth, logout, worker-fix or deployment header** until approved destruction/recovery protocol |
| no-op replacement Worker | Disable buggy interception | Forced reload loses draft or leaves data inaccessible | Conditional incident tool; same URL, safe-edit hold, data inventory |
| global HTTP no-store | Conservative freshness | Mistaken as complete offline strategy | Keep separate from Cache Storage and release asset inventory |

A security incident may justify destructive containment, but only through an explicitly approved incident playbook with a documented consequence decision, scope, alternative preservation, and residual risk. "Prohibited as routine" does **not** mean an unconditional ban during verified compromise.

## 6. VALIDATION — independent negative matrix (DESIGNED, NOT EXECUTED)

**H01–H06 route/header:** capture exact `/auth`, `/auth/`, `/auth/action?mode=...&oobCode=SENTINEL`, `/auth/action/index.html`, `/__/*` and `/` responses; assert intended Referrer/CSP/no-store/COOP and **absence of unintended Clear-Site-Data**. Verify header matching before rewrite and no accidental SPA HTML on absent JS/WASM/font.

**H07–H12 destructive consequences:** with synthetic **disposable** IndexedDB ledger + outbox fixture, apply no header, `"cache"`, `"cookies"`, `"storage"`, `"*"`, and malformed/unsupported directive. Measure actual per-engine storage, Worker registration, cookie and navigation effects; never run destructive tests against a real user profile. An observed browser that ignores a directive does not make its global deployment safe for browsers that implement it.

**H13–H18 update/incident:** old Worker → no-op same URL; old Worker → no-op changed URL; active edit during `skipWaiting`/reload; offline before and after remediation; rollback to old Hosting bytes; rejoin after account retirement. Assert local owner/outbox/provenance retained or explicitly safe-held; remote admission remains current.

**H19–H24 auth/reporting/device:** Firebase Auth Emulator popup and redirect with strict/compatible COOP; CSP Report-Only sentinel query capture and **pre-ingest** redaction; CSP enforce SDK/font/WASM compatibility; Safari tab vs Home Screen vs managed Web Clip; named vs temporary Shared iPad session; accessibility of "local preserved / session revoked / remote not acknowledged" states. Do not infer iPadOS policy from desktop Safari.

**Oracle classes:** SOURCE static config, HOSTING emulator, SERVED response, BROWSER runtime, REAL local mutation/reopen, PHYSICAL device/MDM, INCIDENT recovery drill. None is transitive to the next. Mark PASS/FAIL/UNKNOWN per class and attach source SHA, build hash, Hosting version, browser/OS/display mode, storage partition, worker version, fixture ID, and sanitized trace.

**No H01–H24 executable PASS is claimed.** The current product source shows no Clear-Site-Data configuration; this is a release-prevention and incident-readiness research result, not a production finding.

## 7. TRANSFER VALIDATION / CONTRADICTION / five-track balance

- **E highest-risk bottleneck:** security header scope, incident authority, irreversible-data risk, rollback and no-destructive-default release governance. Own this reusable finding.
- **A critical prerequisite:** browser support is per directive/engine/OS; Service Worker control and origin storage partitioning must be observed. Chrome guidance cannot certify WebKit, and WebKit cookie support cannot certify its IndexedDB clearing.
- **C challenger:** run header/route negative tests with disposable stores; demonstrate **absence of data loss** under ordinary auth/update, and safe incident handling. A static header snapshot is not an executable ledger-preservation test.
- **B transfer:** distinguish signed-out, owner mismatch, locally preserved, sync unacknowledged, update blocked, recovery required and genuinely deleted. Design Studio W103/W117 remains PRACTICE; no physical/AT promotion.
- **D transfer:** no action code, UID, raw flight data or full auth URL in CSP reports, analytics or diagnostic dashboards. Marketing owns outward offline/security claims and must HOLD without exact device/runtime evidence.
- **Engineering S007:** identity/onboarding product contract and implementation/test harness remain Engineering/LogMate-owned. Web Manager supplies header-level requirements only.
- **CONTRADICTION resolved:** `"storage"` is sometimes recommended as an emergency Worker reset, but in an offline ledger origin it can destroy the very data that must survive remediation. The advice is context-dependent, not universally safe.
- **CONTRADICTION unresolved:** WebKit/Safari support for each directive and storage partition under managed Web Clip remains OS-policy/device specific; no universal behavior claimed.

## 8. OPEN / DEPENDENCY / CHANGE WATCH / NEXT

**OPEN:** exact normal PWA build and deployed bytes; actual auth/Hosting response headers; current Worker control; Auth Emulator OAuth behavior; safe reporting ingestion; cross-engine Clear-Site-Data behavior; v14→v15 offline ledger/outbox preservation; recovery export/restore; physical managed iPad/Shared iPad; production incident and deletion authority. **Production validation OPEN.**

**DEPENDENCY:** Engineering supplies a current-head normal build and disposable owner-bound IndexedDB fixtures; Hosting/Auth Emulator access; Web Manager C validates H01–H24; managed-device operator supplies MDM/iPad evidence. No production state mutation is authorized by this research.

**CHANGE WATCH:** W3C Clear-Site-Data draft and CSP3; Chromium Worker remediation guidance; Safari/WebKit per-directive support (including 18.4 `executionContexts` removal); Firebase Hosting header/rewrite rules and Auth popup/redirect SDK; Flutter worker ownership; iPadOS Home Screen/MDM storage behavior.

**Before-close adjacency check:** this bundle integrated the earlier CSP-reporting privacy risk, new destructive-header/incident consequence, browser-specific behavior, Auth COOP compatibility, rollback asymmetry and 24 falsifiable tests. Additional generic primers would not close H01–H24. Next high-value work requires exact artifact and disposable runtime/physical-device evidence.
