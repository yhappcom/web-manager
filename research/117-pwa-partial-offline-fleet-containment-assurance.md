# 117 — PWA Partial/Offline Fleet Containment Assurance

Status: **PASS (generic) / PRODUCT RUNTIME + MANAGED-IPAD + FLEET TELEMETRY VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 091 long-offline compatibility; 098 stale-client revocation; 113 hostile-origin compromise scoping; 116 active-compromise containment; Track A Service Worker/session/network mechanics; Track C adversarial validation; Software Engineering for implementation evidence.

## Purpose

116 separated local client isolation from remote authority containment. The adjacent fleet problem is convergence: a company may revoke credentials, block an API generation, repair origin/deployment authority and publish a clean Service Worker while some installed PWAs remain offline for days or months. This study defines what containment can and cannot mean before every client reconnects.

This is generic web/PWA security knowledge, not a claim about current MintTap or LogMate authentication, API, Service Worker, fleet-management or managed-iPad implementation.

## 1. Five-track balance

- **A Platform/Browser:** owns the mechanics that explain why offline clients do not automatically receive worker/application changes and why later navigation/reconnect can trigger update/control transitions.
- **B UX/IA/Content:** consumes explicit states such as `locally usable`, `remote authority expired`, `reconnect required`, `update required`, `sync blocked`, `reconciliation required` and `replay authorized`.
- **C Quality:** owns long-offline, mixed-generation, revocation-latency, reconnect and replay validation.
- **D Discovery/Analytics:** telemetry can establish observed convergence, not universal fleet absence; measurement denominators and blind spots must be explicit.
- **E Architecture/Security/Operations:** highest-risk owner; defines containment invariants that are enforceable server/control-plane-side even when clients are unreachable.

E remains the bottleneck. A supplies the browser mechanics; C supplies the proof campaign.

## 2. SOURCE — revocation is a server-side security decision, but distributed propagation can lag

RFC 7009 defines OAuth token revocation and says invalidation is intended to take effect immediately, while explicitly recognizing practical propagation delay between servers. It also explains the architectural difference between self-contained access tokens and server-referenced tokens: immediate revocation properties depend on system design, and short-lived access tokens can bound exposure when immediate access-token revocation is unavailable.

Source checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc7009.html

**SYNTHESIS:** a revocation command being accepted is not equivalent to every enforcement point already rejecting the credential.

Guards:
- `revocation requested ≠ revocation globally enforced`;
- `revocation endpoint returned success ≠ every resource server observed the new state`;
- `client offline ≠ stolen credential unusable elsewhere`.

## 3. SOURCE — current OAuth BCP favors bounded, replay-resistant authority

RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) recommends sender-constrained access tokens where appropriate, refresh-token replay defenses for public clients, risk-based refresh-token issuance and inactivity expiration. It notes that sender constraint is weakened if attacker-controlled browser code can access both token and key material.

Sources checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc9700.html
- https://www.rfc-editor.org/info/bcp240/

RFC 10017, OAuth 2.0 for Browser-Based Applications (published August 2026), further emphasizes reducing token authority through shorter lifetimes, narrower scopes and resource restriction, while warning that sender-constrained tokens do not solve browser-only client security limitations.

Source checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc10017.html

**TRANSFER VALIDATION:** PWA fleet containment should rely on server-enforced bounded authority rather than assuming an unreachable browser client will voluntarily receive a revocation message. Exact OAuth adoption is product-specific and OPEN.

Guards:
- `sender-constrained token ≠ compromised same-origin/browser client harmless`;
- `short token lifetime ≠ offline client safely converged`;
- `refresh token rotated ≠ all compromise-era authority resolved`.

## 4. SOURCE — a Service Worker update requires a future update opportunity

The current Service Workers specification defines `ServiceWorkerRegistration.update()` as an update job. MDN documents that an update fetches the worker script and installs a changed worker; lifecycle guidance also shows that a newly installed worker may wait while an old worker controls existing pages.

Sources checked 2026-09-18:
- https://www.w3.org/TR/service-workers/
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update
- https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers

**SYNTHESIS:** publishing clean origin code cannot retroactively modify an unreachable installed PWA. The security design must therefore distinguish server-side containment from client-side remediation/convergence.

Guards:
- `clean worker published ≠ offline client fetched it`;
- `new worker fetched ≠ activated ≠ controlling every client`;
- `origin repaired ≠ long-offline executable state remediated`.

## 5. Containment must be defined as enforceable invariants, not fleet freshness

For a partially offline fleet, useful containment assertions are those enforceable without contacting every client. Depending on architecture, examples may include:
1. compromised credentials/generations are rejected at authoritative server boundaries;
2. stale API/protocol generations cannot perform unsafe remote mutations;
3. compromised deployment credentials cannot publish new trusted origin code;
4. restored domain/origin serves only an admitted release generation;
5. compromise-era queued operations are not automatically accepted merely because a client reconnects;
6. old trust generations cannot silently regain remote authority after reappearance.

These are design targets, not claims that MintTap/LogMate already implement them.

**MINTTAP DIRECTION:** define incident containment by remote invariants first, then measure client convergence separately.

Guard: `fleet not converged ≠ remote containment necessarily failed`; conversely `remote containment PASS ≠ client remediation complete`.

## 6. Three separate assurance questions

### A. Authority containment
Can an unseen stale client still exercise dangerous remote authority?

### B. Exposure containment
Can an unseen client still fetch hostile code or can the attacker still publish it?

### C. Client remediation
Has a particular installed client actually received clean code/trust state and reconciled its local data/operations?

A strong incident model records these separately.

Guards:
- `authority contained ≠ client clean`;
- `hostile deployment removed ≠ previously exposed client remediated`;
- `client remediated ≠ compromise-era operations trustworthy`.

## 7. Offline clients require fail-closed remote re-entry, not remote control while offline

An unreachable PWA cannot be forced to process a new server policy while it remains offline. The controllable boundary is what happens when it next seeks remote authority.

A generic safe re-entry gate can evaluate, where applicable:
- client/app/release generation;
- trust/key generation;
- credential/session validity;
- API/schema/protocol compatibility;
- server-side account/device status;
- pending operation generation and idempotency/provenance;
- whether mandatory recovery/update/reconciliation is outstanding.

The local app may remain readable/exportable while remote mutation is denied.

Guards:
- `cannot remotely update offline client ≠ must remotely trust it on return`;
- `local read allowed ≠ remote mutation allowed`;
- `reconnect observed ≠ replay authorized`.

## 8. Telemetry cannot prove universal convergence without a defensible denominator

Fleet telemetry naturally overrepresents devices that reconnect. Long-offline, powered-down, uninstalled, network-restricted or telemetry-disabled clients may be absent.

Therefore useful metrics distinguish:
- known enrolled/registered clients, if such a registry exists;
- observed active clients in a defined interval;
- clients proven on current trust/release generation;
- clients rejected/quarantined on re-entry;
- clients whose status is unknown;
- retired/decommissioned clients with evidence supporting retirement.

**CONTRADICTION:** `100% of observed clients current` is not equivalent to `100% of fleet current` unless the fleet denominator itself is independently authoritative and current.

Guards:
- `zero observed stale clients ≠ zero stale clients`;
- `no reconnect after incident ≠ device decommissioned`;
- `telemetry silence ≠ containment evidence`;
- `known inventory complete once ≠ inventory remains complete forever`.

## 9. Negative evidence must be scoped

A useful containment report states what was actually tested or observed. Examples:
- resource servers reject a revoked credential generation under controlled tests;
- an old API generation receives a deterministic denial;
- an offline test client reconnects after N days and is quarantined before replay;
- a stale worker cannot regain privileged remote operation before required update/recovery.

These prove bounded properties. They do not prove that no unknown client exists.

**SYNTHESIS:** absence claims require an authoritative population boundary; enforcement claims require adversarial tests at the enforcement boundary.

## 10. Mixed-generation fleet is a normal incident state

During recovery, clients may simultaneously be:
- current and never exposed;
- current after remediation;
- stale but remotely constrained;
- stale and never yet observed after incident;
- preserved/quarantined for evidence;
- unsupported for normal sync but still entitled to local export/recovery;
- decommissioned with independent evidence.

The system should not collapse these into `updated/not updated`.

Track B transfer: operator UX should avoid labels such as `all safe` when the actual state is `remote unsafe generations blocked; 17 clients observed remediated; 3 enrolled clients not yet re-observed`, if such inventory exists.

## 11. API-generation blocking is stronger than UI messaging but needs semantic scope

If old clients can still call a backward-compatible endpoint that performs high-impact mutation, publishing an `update required` screen is not containment. Enforcement belongs at the authoritative operation boundary.

A generation gate should be scoped by capability: local read/export/recovery may remain available while unsafe remote mutation/replay is denied. Prior research 105–107 already separates normal sync retirement from recovery compatibility.

Guards:
- `update-required UI shown ≠ stale API authority blocked`;
- `old sync denied ≠ old local records should be deleted`;
- `protocol version accepted ≠ every operation class authorized`.

## 12. Revocation latency is an explicit security parameter

A future product architecture should identify maximum credible windows for:
- access-token validity after incident decision;
- refresh/session revocation propagation;
- CDN/API/auth cache propagation;
- deployment credential rotation;
- DNS/provider control recovery;
- stale API-generation enforcement;
- client-side update observation after reconnect.

No numeric target is invented here. The important distinction is that each plane has a different convergence mechanism and evidence source.

Guard: `one revocation SLA ≠ all containment planes share that SLA`.

## 13. Track C validation campaign

Future implementation/runtime evidence should include at least:
1. client offline before incident and reconnecting after access-token expiry;
2. refresh/session revoked while client offline;
3. revoked credential presented to every resource-server path;
4. propagation-delay measurement across replicas/regions if applicable;
5. old API generation attempting read vs write vs destructive mutation;
6. old API generation with queued outbox;
7. stale client reconnect with automatic replay disabled;
8. stale worker plus clean origin;
9. waiting worker and mixed open clients;
10. compromised deployment credential rotation;
11. restored origin with old cached shell;
12. trust-generation mismatch;
13. schema-generation mismatch;
14. device/account disabled while client offline;
15. client absent beyond ordinary telemetry window;
16. inventory-known but telemetry-silent client;
17. client removed/uninstalled without explicit server deregistration;
18. decommission evidence path;
19. captive/partial connectivity during re-entry;
20. managed-iPad network/MDM restriction;
21. local read/export while sync blocked;
22. recovery import while normal sync unsupported;
23. quarantine UX with accessibility/locale stress;
24. server-side rejection telemetry without sensitive payload logging;
25. emergency API-generation block rollback after incident;
26. false-positive stale classification and safe recovery;
27. attacker replaying stolen bearer token from another host;
28. sender-constrained token where both browser code and key material are compromised;
29. current client with compromise-era outbox;
30. unknown client reappearing after a long retention interval.

No product PASS exists until exact runtime evidence is captured.

## 14. EFB / LogMate-like judgment

For a company iPad that may stay offline during flight or for extended periods, containment cannot depend on background push, unattended execution or immediate policy delivery unless exact managed-iPad evidence proves those mechanisms. A safer generic architecture assumes an offline client may remain unchanged and makes its next remote authority request pass through current server-side gates.

This preserves offline usefulness while preventing `offline-capable` from becoming `indefinitely trusted for remote mutation`.

Guards:
- `offline usefulness ≠ indefinite remote authority`;
- `background capability unavailable ≠ containment impossible`;
- `managed fleet ≠ every device continuously reachable`.

## 15. D telemetry/privacy transfer

Containment assurance needs enough metadata to distinguish generations and outcomes, but an incident is not a license to mirror flight records or user content into telemetry. Prefer narrowly scoped identifiers/generation/outcome evidence where product architecture supports it, with retention and access controls.

Guard: `fleet assurance requires denominator/evidence ≠ collect all domain data`.

## 16. Operational decision record

A containment-convergence report should distinguish:
- **issued:** security decision made;
- **enforced:** authoritative boundary tested/verified;
- **observed:** particular clients seen under the new policy;
- **remediated:** particular clients proven on clean executable/trust state;
- **reconciled:** compromise-era data/operations reviewed;
- **unknown:** clients/population not yet evidenced.

This vocabulary prevents management reporting from promoting a control-plane action into a fleet-wide fact.

## 17. OPEN

Exact product evidence remains required for:
- client/fleet identity and authoritative denominator;
- auth/session/token architecture and revocation semantics;
- API generation/version gates;
- server/resource topology and cache/replication propagation;
- Service Worker update/activation policy;
- device/account disable semantics;
- trust/key generations;
- operation IDs/idempotency/outbox behavior;
- managed-iPad reachability/MDM/network policy;
- telemetry availability, privacy and retention;
- decommission/retirement evidence;
- actual maximum offline interval and support policy.

## 18. VALIDATION / gate result

**PASS (generic).** The Web Manager can now distinguish containment issuance, enforcement, observed fleet convergence, client remediation and reconciliation; explain why long-offline PWAs defeat telemetry-only assurance; and define fail-closed remote re-entry without requiring destructive local cleanup.

Production, managed-iPad and exact fleet validation remain OPEN.

## 19. CHANGE WATCH

Recheck when browser Service Worker lifecycle/update behavior materially changes; when browser-based OAuth guidance changes; when managed-iPad background/network policy changes; or when product auth/API/trust architecture becomes known.

## 20. Next adjacent target

The remaining adjacent risk is **containment-policy rollback and emergency-gate lifecycle**: once an incident-only API-generation block, credential freeze, quarantine or trust gate is introduced, how to remove or relax it without silently re-authorizing stale clients, replaying preserved operations, or leaving emergency controls permanently active.