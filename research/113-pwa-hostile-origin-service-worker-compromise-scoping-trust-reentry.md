# 113 — PWA Hostile-Origin / Service-Worker Compromise Scoping & Trust Re-entry

Status: **PASS (generic) / PRODUCT RUNTIME + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 089 update/recovery; 093 offline authorization/session boundaries; 097 trust bridges; 098 stale-client containment; 099 trust authenticity/anti-rollback; 100 rebootstrap; 101 mixed-epoch recovery; 111 authority continuity; 112 recovery abuse resistance; Track A Service Worker/origin/storage mechanics; Track C adversarial runtime validation.

## Purpose

112 established that a fraudulent domain/deployment recovery can deliver hostile PWA code and that restoring the provider/domain does not prove installed clients are clean. This study closes the adjacent generic question: **how should compromise scope and trust re-entry be reasoned about after an origin or Service Worker may have been hostile, while preserving irreplaceable offline records?**

This is generic architecture/security judgment. Exact MintTap/LogMate code, worker versions, cache layout, IndexedDB schema, authentication, MDM controls and iPad/WebKit behavior remain OPEN until runtime evidence exists.

## 1. Five-track balance

- **A Platform/Browser:** critical dependency owner for registration lifetime, control scope, update/unregister semantics, Cache Storage and browser-specific behavior.
- **B UX/IA/Content:** consumes truthful states: exposure unknown, local records preserved, network authority quarantined, remediation pending, trust re-established, replay blocked/authorized.
- **C Quality:** high-pressure consumer; owns incident fixtures, mixed-generation clients, offline/online transitions, preservation tests and independent-engine/device evidence.
- **D Discovery/Analytics:** domain takeover may poison acquisition/discovery and incident telemetry; absence of telemetry from offline clients is not non-exposure evidence.
- **E Architecture/Security/Operations:** highest-risk owner; owns compromise scope, evidence classes, quarantine, rebootstrap and re-entry policy.

E remains the bottleneck; A and C are the strongest dependencies. Equal allocation is not justified.

## 2. SOURCE — Service Worker persistence and control outlive a page

The current W3C Service Workers specification requires the user agent to persist registrations until explicitly unregistered. A controlled client has an active worker that can serve its loading and subresources. MDN likewise documents that a registration's lifetime exceeds the JavaScript registration object and that registrations are persistently maintained by the browser.

Sources:
- https://www.w3.org/TR/service-workers/ (current Working Draft, checked 2026-09-18)
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration

**SYNTHESIS:** if hostile code became the active worker for a scope, closing the page or later fixing the server is not evidence that every existing client ceased to be controlled by the hostile generation.

Guards:
- `origin fixed now ≠ every client controlled by clean worker now`;
- `page closed ≠ registration removed`;
- `server artifact replaced ≠ previously active client generation disappeared`.

## 3. SOURCE — update and unregister are mechanisms, not proof of fleet remediation

`ServiceWorkerRegistration.update()` checks the server for a worker update and installs a changed script. `unregister()` requests removal of a registration, while an ongoing worker operation can finish; registration races are also possible. A long-offline client cannot receive a network remediation until it reconnects and actually executes an applicable path.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/unregister
- https://www.w3.org/TR/service-workers/

**SYNTHESIS:** remediation is an observed client-state transition, not a deployment-side intention.

Guards:
- `clean worker published ≠ clean worker fetched ≠ clean worker activated ≠ client revalidated`;
- `unregister requested ≠ every hostile effect removed`;
- `online again ≠ remediation path completed`.

## 4. SOURCE — Cache Storage is separately persistent and application-managed

MDN documents Cache Storage as persistent named caches associated with the current context/origin; applications decide how cache entries are updated. The Cache API's lifetime and retention are browser-dependent.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage
- https://developer.mozilla.org/en-US/docs/Web/API/Cache

**SYNTHESIS:** replacing/unregistering a worker is not by itself proof that attacker-written cached responses, application state, session material or domain records have been classified/remediated.

Guard: `worker registration clean ≠ cache clean ≠ application data clean ≠ trust state clean`.

## 5. Exposure must be modeled as an evidence matrix, not one infected/clean bit

For each client/cohort, distinguish at least:
1. **origin exposure window** — could the client have contacted the hostile origin/deployment?
2. **worker generation** — which installing/waiting/active worker generations are evidenced?
3. **resource generation** — which shell/scripts/assets could have been served or cached?
4. **session/credential exposure** — could hostile same-origin code access or trigger privileged actions?
5. **local-data mutation** — could authoritative records/outbox/trust metadata have been altered?
6. **remote-side effects** — could hostile code have sent operations already accepted remotely?
7. **post-remediation state** — what exact clean artifact/trust generation is now active?

Useful classes are **proven non-exposed**, **potentially exposed**, **exposed with bounded evidence**, **remediated with re-entry evidence**, and **unknown**. Do not collapse `unknown` into clean.

Guards:
- `no observed compromise ≠ proven non-exposure`;
- `offline during part of incident ≠ offline during entire hostile window`;
- `current worker hash clean ≠ historical hostile execution impossible`;
- `telemetry absent ≠ client absent`.

## 6. Non-exposure proof and remediation proof are different

A client can be trusted through two different evidence routes:

### Route A — non-exposure evidence
Evidence must establish that the client could not have executed the hostile generation during the relevant interval, for example through a defensible combination of last-known clean generation, verified offline interval, no hostile worker/resource generation and no later contact before recovery. Exact evidence depends on the implementation and cannot be assumed.

### Route B — remediation evidence
If exposure cannot be excluded, trust re-entry must show containment, current clean artifact/trust activation, classification of persistent state, preservation/reconciliation of local authoritative records, invalidation/rotation of affected authority where required, and replay authorization.

**SYNTHESIS:** Route B does not rewrite history; it proves current safe state after possible exposure.

Guards:
- `remediated ≠ never exposed`;
- `non-exposure not proven ≠ data must be destroyed`;
- `historical exposure proven ≠ every local record malicious`.

## 7. Clear-Site-Data is powerful but too coarse for irreplaceable local records

The W3C Clear Site Data specification was explicitly designed to clear origin-local storage, cookies, workers/service workers and caches after incidents. Current MDN documents `"storage"` as including IndexedDB and Service Worker registrations, while `"cache"` clears cached data. Browser support/details vary and remain CHANGE WATCH.

Sources:
- https://www.w3.org/TR/clear-site-data/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data

**CONTRADICTION / PWA consequence:** a global storage wipe may remove the very authoritative offline records that recovery is meant to protect. A kill-switch suitable for an ordinary site is not automatically suitable for a device-authoritative EFB.

MINTTAP/LogMate-like direction:
- do not make `Clear-Site-Data: "storage"` or equivalent full origin wipe the default incident response for a client that may contain unique records;
- first preserve/export/recover the authoritative data frontier through a current trusted path where technically possible;
- quarantine executable/network authority separately from domain data when the architecture permits;
- exact Safari/iPadOS directive behavior must be tested, not inferred from generic compatibility tables.

Guards:
- `clear site data supported ≠ indiscriminate clearing safe`;
- `security wipe successful ≠ user-data recovery successful`;
- `cache can be discarded ≠ IndexedDB authoritative records can be discarded`.

## 8. Data plane and authority plane require separate treatment

After hostile-origin exposure, classify local state into conceptual planes:
- **executable/resource plane:** worker scripts, cached HTML/JS/CSS/assets;
- **authority plane:** sessions/tokens, device credentials, trust roots/generations, replay authorization, sync capability;
- **domain-data plane:** user-created flight/log records, attachments, local business state;
- **operation plane:** queued/outbox operations and acknowledgement/reconciliation metadata.

Default incident reasoning should be:
`freeze authority/replay → preserve domain data → replace executable plane → rebootstrap/revalidate authority → reconcile operation plane → resume`.

This is a model, not an implementation prescription.

Guards:
- `same origin storage ≠ same security meaning`;
- `attacker could execute same-origin code ≠ every domain record should be deleted`;
- `record preserved ≠ record semantically trusted without reconciliation`.

## 9. Same-origin hostile code creates a difficult integrity boundary

If hostile JavaScript executed with the application's normal same-origin authority while data was unlocked, encryption-at-rest does not prove that records or metadata were unreadable/unmodifiable. Prior studies already guard against treating at-rest encryption as protection from authorized same-origin script.

Therefore preservation must retain uncertainty. Potentially exposed records may require:
- record-level invariants/history where available;
- remote acknowledgement comparison;
- user/domain review for ambiguous mutations;
- append-only or provenance evidence where the exact product supplies it;
- quarantine from automatic replay until reconciliation.

No generic mechanism proves a mutable IndexedDB record was untouched after arbitrary same-origin script execution unless the product has independent integrity evidence.

Guard: `bytes parse correctly ≠ record integrity proven after hostile same-origin execution`.

## 10. Trust re-entry is a monotonic generation transition

A safe generic re-entry sequence is:
1. establish legitimate origin/control-plane authority under 111/112;
2. freeze or narrow remote writes/replay for uncertain clients;
3. identify current recovery artifact/worker/trust generation;
4. preserve irreplaceable local domain data before destructive cleanup where feasible;
5. remove/replace hostile executable/cache generations using exact platform-supported mechanisms;
6. invalidate/rotate compromised session/device/trust authority as required;
7. migrate/rebootstrap to a **new** trusted generation rather than reviving an old compromised one;
8. reconcile local records/outbox with remote acknowledgement/state;
9. authorize replay only after current policy and reconciliation pass;
10. record closure evidence and retire temporary recovery authority.

Guards:
- `old known-good version ≠ currently authorized generation`;
- `rollback to pre-incident code ≠ rollback of compromise effects`;
- `new worker active ≠ old tokens/remote side effects reconciled`;
- `trust re-entry ≠ trust-history erasure`.

## 11. Browser/platform distinctions and CHANGE WATCH

### Web standard
Service Worker registration/control/update/unregister and Clear-Site-Data define generic mechanisms, not product remediation guarantees.

### Chromium
Do not transfer Chrome DevTools/background/update observations into Safari or managed iPad claims without execution evidence.

### Safari/WebKit
WebKit supports Service Workers for Home Screen web apps and continues evolving web-app behavior. WebKit's Safari 26 material states that on iOS/iPadOS 26 any site may be added as a web app, while Service Workers remain optional enhancement. This does not establish MintTap/LogMate installability under company MDM or incident-cleanup semantics.

Sources:
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/

**CHANGE WATCH:** exact iOS/iPadOS/WebKit version, Home Screen data partition, Clear-Site-Data behavior, MDM restrictions, user removal/reset behavior and storage persistence require target-device tests.

Guard: `WebKit feature exists ≠ managed-EFB policy permits/retains it`.

## 12. Track B truthful recovery UX states

A compromised-client recovery flow should not use a binary `safe/unsafe` label when evidence is incomplete. Candidate semantic states include:
- checking incident exposure;
- local records preserved;
- network changes temporarily blocked;
- remediation required;
- rebuilding trusted application components;
- records require reconciliation;
- trust restored, sync still blocked;
- sync/replay authorized;
- manual recovery/export required.

Do not claim data is lost merely because executable state is untrusted, and do not claim data is safe merely because it is visible locally.

## 13. Track C validation campaign

Exact product validation should include at least:
1. client online throughout hostile-origin interval;
2. client offline throughout hostile interval;
3. client connects once during hostile interval then goes offline;
4. hostile worker installed but waiting;
5. hostile worker active and controls an existing client;
6. clean worker published while client remains offline;
7. worker remediated but hostile cache entry remains;
8. cache clean but session/token remains compromised;
9. domain data preserved while executable plane is replaced;
10. global wipe attempted against a device with unsynced authoritative records;
11. hostile script mutates one local record and one outbox operation;
12. remote side effect acknowledged before incident containment;
13. stale outbox tries replay immediately after reconnect;
14. current trust generation rejects stale replay;
15. recovery interrupted between preservation and executable cleanup;
16. recovery interrupted after worker replacement but before reconciliation;
17. long-offline client returns after normal compatibility window;
18. storage pressure/eviction occurs during incident recovery;
19. browser restart occurs at each major transition;
20. Chromium and independent engine behavior compared;
21. Safari/WebKit Home Screen behavior tested on target iPadOS;
22. managed-EFB MDM/network restrictions applied;
23. accessibility of quarantine/recovery states verified;
24. telemetry cannot falsely classify silence as non-exposure;
25. no recovery telemetry leaks local record contents, tokens or secrets.

No runtime PASS is inferred from generic standards.

## 14. Cross-repository transfer

### Design Studio
Canonical `progress/WEB_STATUS.md` checked 2026-09-18: Web Design remains **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. W064's second real CI run still failed in analysis because of an unavailable semantics debug helper; a repaired product commit exists but its run remains OPEN. Recovery/quarantine UI therefore has no product-browser, Safari, screen-reader or physical-device PASS.

### Software Engineering Studio
Canonical `progress/STATUS.md` checked 2026-09-18: every specialist remains **Foundation IN STUDY**. Systems S003 adds bounded profiling evidence; it is not PWA/mobile/runtime security evidence. Exact storage partitioning, migration, worker versioning, cryptographic integrity, sync reconciliation and incident implementation remain Software Engineering handoffs where appropriate.

## 15. MINTTAP / LogMate-like operational judgment

For an offline-first EFB-like PWA, the highest-value principle is **preserve data while revoking uncertain authority**. If a client may contain the only copy of flight records, incident response must avoid equating storage destruction with security recovery.

A future product architecture should make it possible, where feasible, to:
- identify worker/app/trust/schema generations without exposing secrets;
- stop or gate network replay independently of local read/export;
- preserve authoritative records before executable-state destruction;
- distinguish records from executable caches and credentials;
- rebootstrap authority into a new generation;
- reconcile queued operations before remote side effects resume;
- produce evidence that a client was non-exposed or was remediated, rather than merely observing that the server is currently healthy.

Exact feasibility on company-managed iPad remains OPEN.

## 16. Durable synthesis

The correct post-hostile-origin question is not `is the PWA clean now?` but:

**which client generations could have executed hostile authority, which persistent planes could have been affected, what evidence proves non-exposure or current remediation, and can authority be replaced without destroying irreplaceable local data?**

Persistent guards:
- `origin fixed now ≠ every client controlled by clean worker now`;
- `clean worker published ≠ clean worker fetched ≠ clean worker activated ≠ client revalidated`;
- `worker registration clean ≠ cache clean ≠ application data clean ≠ trust state clean`;
- `no observed compromise ≠ proven non-exposure`;
- `remediated ≠ never exposed`;
- `clear site data supported ≠ indiscriminate clearing safe`;
- `same origin storage ≠ same security meaning`;
- `bytes parse correctly ≠ record integrity proven after hostile same-origin execution`;
- `new worker active ≠ old tokens/remote side effects reconciled`;
- `WebKit feature exists ≠ managed-EFB policy permits/retains it`.

## 17. OPEN / next boundary

Product/runtime OPEN:
- exact worker/cache/IndexedDB/session/trust topology;
- exact incident exposure evidence and client-generation identifiers;
- exact record-integrity/provenance capability;
- exact selective preservation/cleanup mechanisms;
- Safari/iPadOS Home Screen and managed-MDM behavior;
- accessible recovery UX;
- remote reconciliation and replay policy.

Highest-value adjacent generic boundary: **compromise-era data integrity and operation provenance**. Once arbitrary same-origin code may have run, preserving local records is necessary but does not prove their integrity. The next study should determine what evidence can distinguish user-authored records, attacker-mutated records, queued operations and remotely acknowledged effects without requiring impossible retrospective certainty, and how to degrade safely when independent integrity evidence never existed.