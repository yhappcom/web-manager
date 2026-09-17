# 118 — PWA Containment-Policy Rollback & Emergency-Gate Lifecycle

Status: **PASS (generic) / PRODUCT RUNTIME + MANAGED-IPAD + INCIDENT-DRILL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 098 stale-client revocation; 104 forward-only release governance; 111 recovery-authority continuity; 112 recovery-authority abuse resistance; 116 active-compromise containment; 117 partial/offline fleet containment; Track A auth/Service Worker/reconnect mechanics; Track C adversarial validation; Software Engineering for exact implementation evidence.

## Purpose

117 established that incident containment for a partially offline PWA fleet must be defined by authoritative enforcement rather than assumed client convergence. The adjacent risk is the end of containment. Incident-only API-generation blocks, credential freezes, quarantine gates, replay suppression, emergency accounts and temporary trust restrictions can themselves become unsafe if they are removed too early, rolled back as a bundle, or left active indefinitely.

This study defines a generic lifecycle for relaxing emergency controls without silently restoring stale authority or turning incident exceptions into permanent hidden administration paths. It is not a claim about current MintTap or LogMate implementation.

## 1. Five-track balance

- **A Platform/Browser:** dependency supplier for session/token lifetime, Service Worker update/control, cached executable state and reconnect behavior. A browser cannot be assumed to learn that an emergency policy ended while offline.
- **B UX/IA/Content:** consumes explicit states such as `contained`, `locally usable`, `remote mutation blocked`, `re-entry required`, `reconciled`, `normal authority restored`; it must not collapse policy relaxation into a generic `back online` message.
- **C Quality:** owns staged rollback, stale-client, replay, accessibility and failure-injection validation.
- **D Discovery/Analytics:** owns evidence about observed policy adoption and rollback outcomes, while preserving denominator uncertainty and avoiding sensitive incident telemetry.
- **E Architecture/Security/Operations:** highest-risk owner; defines emergency-control ownership, expiry, rollback prerequisites, staged relaxation and closure evidence.

E remains the bottleneck. A supplies mechanics; C supplies proof.

## 2. SOURCE — incident recovery is risk management, not simply restoration of the previous state

NIST SP 800-61 Rev. 3, finalized April 2025, integrates incident response into cybersecurity risk management and treats response/recovery as organizational risk-management activities rather than a narrow sequence of technical cleanup actions.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

**SYNTHESIS:** incident closure should restore an explicitly acceptable operating state, not mechanically recreate every pre-incident privilege, compatibility path or trust assumption.

Guards:
- `incident pressure ended ≠ pre-incident policy automatically safe`;
- `service restored ≠ emergency controls ready for removal`;
- `return to normal ≠ return to old trust generation`.

## 3. SOURCE — emergency authority is temporary by design

NIST SP 800-53 Rev. 5.1 describes emergency and temporary accounts as short-term mechanisms. AC-02(02) calls for automatic removal or disabling of temporary and emergency accounts after an organization-defined period. NIST's least-privilege principle restricts entities to the minimum resources and authorizations necessary for their function.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-53 Rev. 5.1 OSCAL-derived control catalog, AC-02 / AC-02(02)
- https://csrc.nist.gov/glossary/term/least_privilege

**TRANSFER VALIDATION:** an incident-only API bypass, emergency admin path or temporary trust exception should have explicit owner, scope, activation evidence and retirement condition. This does not require MintTap to implement NIST controls verbatim.

Guards:
- `emergency control useful once ≠ standing privilege justified`;
- `rarely used ≠ temporary`;
- `documented emergency account ≠ automatically expired emergency account`.

## 4. Emergency gates need identities, not anonymous configuration toggles

A future product/control plane should be able to distinguish incident controls by purpose and authority, for example:
- compromised credential-generation deny;
- stale API/protocol mutation deny;
- replay suppression;
- client/trust-generation quarantine;
- destructive-operation freeze;
- emergency read/export allowance;
- temporary administrative/recovery authority.

Each control should have, where architecture permits: stable control identity, incident/reason reference, scope, owner/approver, activation time, expected expiry/review time, enforcement points, rollback prerequisites and closure evidence.

**SYNTHESIS:** a boolean `incidentMode=false` is too coarse if several independent security boundaries were changed.

Guards:
- `one incident ≠ one reversible switch`;
- `configuration reverted ≠ all enforcement points reverted coherently`;
- `temporary control disabled ≠ old authority should be restored`.

## 5. Rollback is usually forward transition, not historical configuration restore

Prior study 104 established forward-only release governance. The same principle applies to incident policy. If credentials, keys, trust generations, API contracts or compromise-era operations changed during containment, restoring an old configuration snapshot can revive revoked authority.

A safer generic model is:
`pre-incident state → containment state → recovered/new trust state → staged normal state`.

The final state can resemble ordinary operation while still retaining post-incident key generations, revoked credentials, retired APIs and reconciliation decisions.

Guards:
- `policy rollback ≠ configuration snapshot rollback`;
- `normal service restored ≠ revoked credential revived`;
- `old API compatibility desired ≠ old mutation authority restored`;
- `old trust state historically valid ≠ currently authorized`.

## 6. Relax controls independently by capability

Emergency controls should not be removed as an all-or-nothing bundle. A staged sequence can preserve safer capabilities while evidence accumulates:
1. keep destructive mutation blocked;
2. allow authenticated read where current authority is proven;
3. allow local export/recovery without remote mutation;
4. allow current-generation non-destructive writes after re-entry checks;
5. allow queued-operation reconciliation rather than automatic replay;
6. restore high-impact/destructive operations only after stronger closure evidence;
7. retire emergency administrative paths separately.

Exact sequencing is product-specific and OPEN.

**MINTTAP DIRECTION:** define rollback per capability/authority plane, not per UI mode.

Guards:
- `read safe ≠ write safe ≠ destructive operation safe`;
- `current client generation ≠ compromise-era outbox trusted`;
- `sync re-enabled ≠ replay authorized`.

## 7. Long-offline clients must cross the current gate, not the gate that existed when they disconnected

An offline client may miss both containment and rollback announcements. When it reconnects, the authoritative boundary should evaluate current credential/session validity, client/trust/API/schema generation, account/device status and unresolved reconciliation requirements.

The client should not receive a special shortcut merely because the emergency block has been globally relaxed.

**SYNTHESIS:** rollback must preserve fail-closed re-entry for clients that never demonstrated remediation.

Guards:
- `global emergency block removed ≠ every stale client re-authorized`;
- `client never observed during incident ≠ client presumed clean after incident`;
- `incident closed centrally ≠ unknown client state resolved`.

## 8. OAuth/session relaxation must not mint indefinite post-incident authority

RFC 9700, the January 2025 OAuth 2.0 Security BCP, recommends restricted token privilege and replay-resistant refresh-token handling; for public clients, refresh tokens must be sender-constrained or rotated. RFC 10017, published August 2026 for browser-based applications, additionally requires rotation or sender constraint and requires a maximum lifetime or inactivity expiration for refresh tokens.

Sources checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc9700.html
- https://www.rfc-editor.org/rfc/rfc10017.html
- https://www.rfc-editor.org/rfc/rfc7009.html

**TRANSFER VALIDATION:** if a product uses OAuth-like bearer/session authority, ending a credential freeze should not resurrect compromise-era refresh/session state. Exact auth architecture is OPEN.

Guards:
- `credential freeze removed ≠ frozen credential valid again`;
- `new login succeeds ≠ old refresh chain should resume`;
- `token endpoint healthy ≠ pre-incident grants trustworthy`.

## 9. Replay suppression needs its own retirement gate

Queued offline operations are particularly dangerous at rollback. They may have been created before compromise, during hostile-origin exposure, during containment, or after local remediation. Network reconnection and sync availability do not establish provenance.

A generic rollback path should classify pending operations by operation identity, trust/client generation, creation context where evidenced, server acknowledgement history and reconciliation status. Unknown operations remain unknown rather than becoming valid because emergency replay suppression ended.

Guards:
- `replay suppression removed ≠ preserved outbox safe to flush`;
- `operation old ≠ operation malicious`; `operation old ≠ operation trustworthy`;
- `idempotency prevents duplicate effect ≠ operation intent legitimate`.

## 10. Service Worker/client update policy also needs staged re-entry

A repaired origin and a relaxed API gate do not prove a stale installed PWA has clean executable state. Service Worker update/control semantics remain client-local and opportunity-dependent. Therefore high-risk remote mutation can remain gated on current release/trust evidence even after ordinary web traffic is restored.

Sources retained from 117:
- https://www.w3.org/TR/service-workers/
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update

Guards:
- `origin normal ≠ stale worker trusted`;
- `emergency API block removed for current clients ≠ stale worker entitled to same authority`;
- `update available ≠ update activated/controlling`.

## 11. Expiry is a safety net, not the whole retirement process

Automatic expiry is valuable for emergency privilege, but blind expiry can also remove a control while the underlying incident condition persists. Therefore distinguish:
- **privilege expiry:** emergency authority should fail closed unless deliberately renewed;
- **containment-control review:** a deny/quarantine may remain until explicit safety prerequisites are met;
- **renewal:** should create fresh decision evidence rather than silently extending forever.

**SYNTHESIS:** some emergency *privileges* should auto-expire; some emergency *restrictions* should require explicit safe relaxation. Treating both identically is unsafe.

Guards:
- `automatic expiry good for emergency privilege ≠ every containment deny should auto-expire`;
- `control still active ≠ control forgotten if review evidence exists`;
- `repeated renewal ≠ temporary in substance`.

## 12. Rollback prerequisites should be evidence-bearing

Depending on the control, rollback evidence may include:
- compromised credentials/keys rotated and old generations rejected;
- authoritative resource/API enforcement tested;
- hostile deployment path removed;
- current release/trust generation admitted;
- current clients pass re-entry tests;
- compromise-era operations classified/reconciled;
- rollback canary succeeds without reviving stale authority;
- independent monitoring shows expected denials/accepts;
- emergency account/session/API token retirement is verified;
- residual unknown clients remain explicitly unknown and fail closed on return.

No universal numeric threshold is invented.

Guard: `incident ticket closed ≠ rollback prerequisites satisfied`.

## 13. Canary relaxation is safer than fleet-wide simultaneous rollback

Where architecture supports staged policy, first relax a narrow population or operation class, observe both positive and negative behavior, then expand. A canary must test not only that legitimate current clients work, but that stale/revoked/unknown clients remain blocked.

**SYNTHESIS:** rollback validation needs negative controls.

Guards:
- `current client succeeds ≠ stale client remains denied`;
- `no errors after rollback ≠ security invariant preserved`;
- `availability canary PASS ≠ authorization canary PASS`.

## 14. Emergency control debt must be tracked after service restoration

Incident pressure creates temporary routes, allowlists, feature flags, credentials, provider exceptions, manual runbooks and telemetry. Service restoration can make these invisible operational debt.

A closure inventory should reconcile:
- every emergency control activated;
- current state and owner;
- whether it was retired, converted into a deliberate permanent control, or remains temporarily active;
- credentials/tokens/sessions created during incident;
- temporary logging/telemetry and its retention/privacy disposition;
- temporary DNS/provider/support arrangements;
- client-side recovery modes and support instructions.

Guards:
- `incident over ≠ incident-created authority gone`;
- `feature flag off ≠ supporting credential/token removed`;
- `temporary telemetry useful ≠ indefinite retention justified`.

## 15. Track B transfer — user/operator state must match actual authority

Rollback UX should distinguish at least:
- local records available;
- remote access restricted;
- re-authentication/recovery required;
- update required before sync;
- pending records preserved but replay blocked;
- reconciliation required;
- normal sync restored.

Avoid messages such as `Everything is back to normal` when unknown/stale clients or unreconciled operations remain.

Guard: `service banner removed ≠ every user/device state normal`.

## 16. Track D transfer — rollback telemetry is evidence, not the authority source

Useful observations may include current-generation accepts, stale-generation denies, quarantine counts, reconciliation outcomes and emergency-control activation/retirement events. Telemetry should not itself decide authorization, and absence of stale-client events does not prove absence of stale clients.

Privacy minimization from 114–117 remains in force.

Guards:
- `telemetry says current ≠ authorization boundary may trust telemetry instead of current policy`;
- `zero stale denials observed ≠ zero stale clients exist`.

## 17. Track C validation campaign

Future exact implementation evidence should include at least:
1. emergency API deny activated then selectively relaxed;
2. stale client reconnect after global relaxation;
3. revoked credential remains rejected after rollback;
4. old refresh/session chain cannot resume;
5. new authenticated session can operate at intended scope;
6. read restored while destructive write remains blocked;
7. local export works while remote mutation remains blocked;
8. current client with clean empty outbox;
9. current client with compromise-era outbox;
10. stale client with queued operations;
11. unknown client reappearing after incident closure;
12. clean Service Worker current client;
13. waiting worker during rollback;
14. stale worker against relaxed origin;
15. trust-generation mismatch;
16. schema/API-generation mismatch;
17. account/device disabled during incident remains disabled;
18. emergency account auto-expiry;
19. emergency account explicit early retirement;
20. emergency restriction requiring explicit review rather than auto-expiry;
21. accidental control expiry while incident condition persists;
22. renewal produces new approval/evidence;
23. repeated renewal is detected as emergency-control debt;
24. canary current client succeeds;
25. canary stale/revoked client remains denied;
26. rollback failure re-enters containment without data loss;
27. accessibility of restricted/recovery/reconciliation states;
28. locale and enlarged-text stress;
29. telemetry records outcomes without sensitive domain payload;
30. managed-iPad client offline through containment and rollback, then re-enters through current gate;
31. server/resource replicas receive rollback consistently;
32. emergency credentials/tokens removed after closure;
33. temporary incident telemetry retention cleanup;
34. rollback audit can reconstruct who changed which gate and why;
35. recovery import remains available where normal sync remains unsupported.

No product PASS exists until exact runtime evidence is captured.

## 18. EFB / LogMate-like judgment

A company iPad may remain offline across the entire incident and only reconnect after headquarters considers the incident closed. Therefore the PWA cannot infer safety from wall-clock incident closure. Its next remote mutation must satisfy the *current* re-entry policy.

Local records should remain preservable/readable/exportable where safe even when the device is stale. Emergency policy rollback should restore remote capability progressively without requiring destructive local reset unless exact evidence shows it is necessary.

Guards:
- `incident closed before device reconnects ≠ device skipped recovery`;
- `managed iPad ≠ centrally reachable during incident`;
- `rollback complete for observed fleet ≠ unknown offline EFB automatically trusted`.

## 19. Operational lifecycle model

Use the following generic lifecycle:

`DEFINE → ACTIVATE → VERIFY ENFORCEMENT → REVIEW/RENEW → SATISFY ROLLBACK PREREQUISITES → CANARY RELAX → EXPAND RELAXATION → RECONCILE → RETIRE EMERGENCY AUTHORITY → VERIFY ABSENCE/RESIDUAL UNKNOWN → POST-INCIDENT REVIEW`.

For every step, distinguish configuration intent from observed enforcement.

## 20. OPEN

Exact product evidence remains required for:
- actual emergency controls/feature flags/accounts;
- auth/session/token architecture and refresh-chain semantics;
- API generation/capability gates;
- Service Worker release/update policy;
- client/trust/schema generations;
- operation IDs/outbox/replay behavior;
- rollback orchestration across replicas/CDN/auth/resource servers;
- emergency privilege expiry and renewal;
- control inventory/audit ownership;
- telemetry/privacy/retention;
- managed-iPad reachability and re-entry behavior;
- incident severity/risk thresholds and approver roles.

## 21. VALIDATION / gate result

**PASS (generic).** The Web Manager can now distinguish rollback from historical configuration restore; separate emergency privilege expiry from containment-restriction relaxation; stage authority restoration by capability; preserve fail-closed re-entry for long-offline clients; and define evidence-bearing retirement of incident-only controls.

Production, managed-iPad and incident-drill validation remain OPEN.

## 22. CHANGE WATCH

Recheck when NIST incident-response/account-management guidance materially changes; browser-based OAuth BCP changes; Service Worker lifecycle/update semantics change; managed-iPad policy changes; or product auth/API/trust/incident-control architecture becomes known.

## 23. Next adjacent target

The next highest-value adjacent risk is **post-incident trust normalization and residual-risk acceptance**: after emergency controls are retired, how to define a defensible new baseline, document residual unknown clients/data, distinguish accepted risk from unresolved incident work, and prevent temporary post-incident assumptions from silently becoming the next permanent trust model.