# 116 — PWA Active-Compromise Containment vs Evidence Preservation

Status: **PASS (generic) / PRODUCT RUNTIME + MANAGED-IPAD + INCIDENT-LEGAL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 113 hostile-origin compromise scoping; 114 compromise-era integrity/provenance; 115 evidence-preserving acquisition; Track A Service Worker/storage/network mechanics; Track C adversarial validation; Software Engineering for implementation/tooling evidence.

## Purpose

115 established that observing or acquiring an offline PWA can mutate evidence. The adjacent incident-response problem is harder: **when compromise may still be active, preservation itself can conflict with containment.** Keeping a suspect EFB isolated may preserve local worker/cache/storage/outbox evidence, while delaying credential revocation, trust-root replacement, server-side session invalidation, deployment rollback, DNS/provider containment or fleet protection can increase harm.

This study establishes a generic risk-based ordering. It is not a product runbook and does not assert the exact MintTap/LogMate auth, storage, sync, managed-iPad, provider or legal architecture.

## 1. Five-track balance

- **A Platform/Browser:** supplies mechanics for connectivity transitions, Service Worker execution/update, local persistence, session use and replay triggers.
- **B UX/IA/Content:** consumes explicit states such as isolated, evidence-preserved, authority-revoked, recovery-required and replay-blocked; it must not imply that a device is safe merely because it is offline.
- **C Quality:** owns containment-order campaigns, including race conditions, partial connectivity, failed revocation, stale clients, acquisition-induced mutations and data-loss checks.
- **D Discovery/Analytics:** independent remote telemetry may help scope active abuse, but collection expansion during an incident must remain purpose-limited and privacy-reviewed.
- **E Architecture/Security/Operations:** highest-risk owner; owns containment priority, evidence-sacrifice decisions, remote authority revocation, recovery handoff and incident decision records.

E remains the bottleneck. A and C are the strongest dependencies.

## 2. SOURCE — containment exists to limit continuing harm

NIST SP 800-61 Rev.3 (final April 2025) integrates incident response into CSF 2.0 and gives containment/eradication/recovery high priority. Its containment guidance supports both automated containment and manual handler-selected containment; eradication includes eliminating persistence/entry points and disabling breached accounts. Recovery then restores normal operation from clean state and may include credential changes and tighter controls.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf

**SYNTHESIS:** preservation is subordinate to the incident-response objective of limiting ongoing harm when the two genuinely conflict. Evidence value remains a decision input, not a reason to knowingly leave dangerous authority active.

Guards:
- `evidence preservation valuable ≠ active compromise may continue for evidence convenience`;
- `containment action destructive to evidence ≠ containment action unjustified`;
- `incident evidence incomplete after containment ≠ containment failed`.

## 3. SOURCE — real guidance explicitly recognizes evidence-loss trade-offs

CISA's current StopRansomware response guidance says to determine impacted systems and immediately isolate them. It also notes that powering down a device can destroy volatile evidence and should be used when network disconnection is not possible. CISA recommends snapshots/log collection where practical, but the sequence remains containment-oriented.

Source checked 2026-09-18:
- https://www.cisa.gov/stopransomware/ransomware-guide

NIST SP 800-86 similarly discusses disconnecting network connectivity to prevent remote modification while acknowledging that forensic acquisition and containment can disrupt operations. It is an IT-forensics guide, not legal advice, and its 2006 publication date means platform-specific mechanics require current validation.

Source:
- https://csrc.nist.gov/pubs/sp/800/86/final

**TRANSFER VALIDATION:** PWA containment should make the same trade-off explicit. If a suspect installed client can still exercise valid credentials, replay queued operations, receive hostile origin code or influence other devices, the preservation plan must not delay remote containment without a documented reason.

## 4. Separate client containment from authority containment

A critical PWA distinction is that taking one EFB offline does not necessarily contain the compromised authority that enabled the incident.

Conceptual containment planes:
1. **client connectivity** — isolate a suspect device from networks where safe and feasible;
2. **session/token authority** — revoke/expire compromised sessions, refresh tokens or device credentials where architecture supports it;
3. **account/role authority** — disable breached accounts or narrow privileges;
4. **deployment/origin authority** — stop hostile release paths, restore trusted origin content and deployment credentials;
5. **domain/DNS/provider authority** — contain registrar/DNS/CDN/cloud takeover where applicable;
6. **trust/signing generation** — revoke or supersede compromised trust roots/keys under the product's recovery design;
7. **sync/API authority** — reject stale/compromised client generations and block unsafe replay;
8. **fleet communication** — protect other clients without requiring the suspect device to reconnect first.

Guards:
- `suspect client offline ≠ compromised account/session revoked`;
- `one device isolated ≠ fleet contained`;
- `origin restored ≠ stolen deployment credential revoked`;
- `network isolation ≠ remote authority containment`.

## 5. Containment-before-acquisition decision gate

Before delaying a containment action for acquisition, classify the threatened harm.

**Immediate containment normally dominates** when credible evidence indicates continuing ability to:
- mutate/delete authoritative remote data;
- issue or replay high-impact operations;
- spread hostile code to other clients;
- use compromised credentials or provider/control-plane authority;
- exfiltrate sensitive data;
- destroy backups/audit evidence;
- defeat future recovery by rotating or deleting trust/ownership controls.

**Short acquisition-first handling may be defensible** only when the threat is bounded enough that delay does not materially increase harm and the evidence is unusually perishable/irreplaceable. The exact threshold is product-specific and should be predefined where possible.

Guard: `evidence is perishable ≠ every containment action should wait`.

## 6. Prefer remote containment that preserves the suspect client's local state

Where architecture permits, first choose containment that reduces attacker authority without touching irreplaceable local data. Examples at the generic level include server-side session/token invalidation, disabling compromised accounts, blocking unsafe API generations, revoking deployment credentials, freezing destructive operations, or restoring origin control.

This can preserve the suspect device for later acquisition while limiting external harm. But whether a specific action actually preserves client evidence is implementation-dependent.

Guards:
- `remote revocation ≠ local evidence mutated zero`; client behavior on later reconnect remains OPEN;
- `API blocked ≠ local outbox erased`;
- `origin fixed ≠ suspect client's worker/cache/session state preserved or clean`.

## 7. Evidence sacrifice must be explicit, bounded and recorded

Sometimes safe containment requires an action that changes or destroys evidence: power-off, credential reset, remote wipe, site-data clearing, forced update, worker unregister, key destruction or emergency account disablement.

When this occurs, the incident record should capture:
- threatened harm and urgency;
- evidence expected to be altered/lost;
- alternatives considered and why insufficient;
- actor/authority approving the action;
- exact containment action and time-source confidence;
- independent evidence preserved beforehand, if feasible;
- post-action state and remaining uncertainty.

**SYNTHESIS:** an evidence-sacrifice record does not restore lost evidence; it preserves decision provenance and prevents later overclaiming.

Guards:
- `documented evidence loss ≠ evidence recovered`;
- `containment justified ≠ pre-containment state reconstructed with certainty`;
- `operator followed runbook ≠ action was optimal for this incident`.

## 8. Irreplaceable offline-authoritative data changes the containment shape

For an EFB-like PWA where local records may be the only authoritative copy, indiscriminate remote wipe or site-data clearing can convert a security incident into permanent data loss. Therefore executable/authority containment should be separated from domain-data destruction whenever possible.

Preferred generic shape:
`freeze unsafe authority → isolate client if needed → preserve independent evidence → preserve local domain artifact when feasible → replace/rebootstrap executable/trust plane → reconcile record provenance → authorize replay`.

This does **not** mean local data is trusted merely because it is preserved.

Guards:
- `containment urgent ≠ wipe is automatically the safest containment`;
- `local record irreplaceable ≠ compromised executable authority must remain active`;
- `local record preserved ≠ local record verified`.

## 9. Reconnection is a containment transition, not just a recovery step

After remote containment, reconnecting a quarantined client can trigger:
- session/token refresh failure or replacement;
- worker/application update;
- queued-operation replay attempts;
- remote acknowledgement changes;
- schema/trust migration;
- telemetry and incident indicators;
- attacker-controlled logic if containment was incomplete.

Therefore reconnect should occur under an explicit trust/recovery gate, not simply because the network is available.

Guards:
- `remote containment complete ≠ reconnect safe`;
- `reconnect required for update ≠ replay should be enabled simultaneously`;
- `client receives clean code ≠ compromise-era data provenance resolved`.

## 10. Product incident decision matrix

A future product runbook should classify at least:

| Condition | Generic priority |
|---|---|
| Active remote destructive authority | contain authority immediately; preserve evidence opportunistically |
| Suspect device can spread/issue operations | isolate client and revoke remote authority |
| Device offline, no active external authority, unique local evidence | preserve/acquire before destructive local remediation when feasible |
| Hostile origin/deployment still live | contain origin/deployment/fleet exposure before client-forensic convenience |
| Credential theft suspected | revoke/rotate according to authority scope; record evidence effects |
| Only evidence is local and containment requires destructive action | explicitly approve/document evidence sacrifice; preserve any independent evidence first |
| Reconnect needed for remediation | separate update/trust recovery from replay/data authorization |

This is a decision scaffold, not a universal incident script.

## 11. Track B transfer — truthful containment/recovery UX

User/operator states should distinguish:
- `isolated`;
- `network available but sync blocked`;
- `credentials/session revoked`;
- `update/recovery required`;
- `records preserved but unverified`;
- `reconciliation required`;
- `replay authorized`.

Do not collapse these into a single `offline`, `safe`, or `synced` label.

## 12. Track C validation campaign

Minimum future implementation/runtime campaign:
1. isolate while worker is active;
2. isolate with queued outbox;
3. server revoke while client remains offline;
4. reconnect after revoke;
5. reconnect with waiting worker;
6. origin rollback with stale client;
7. API generation block with preserved outbox;
8. credential rotation without deleting local records;
9. forced update with authoritative local data;
10. failed update while replay blocked;
11. remote account disable with offline unlock state;
12. partial network/captive connectivity;
13. incident telemetry unavailable;
14. compromised deployment credential revoked;
15. domain/DNS authority restored but stale worker retained;
16. acquisition-first delay with bounded threat;
17. immediate containment causing known evidence loss;
18. evidence-sacrifice record completeness;
19. local-data export before destructive remediation;
20. export failure without enabling sync;
21. interrupted trust rebootstrap;
22. replay attempt before reconciliation;
23. stale session rejection after long offline period;
24. multiple devices with mixed trust generations;
25. managed-iPad policy preventing desired isolation/export action;
26. accessibility of containment/recovery states;
27. localization of high-risk warnings without semantic drift;
28. privacy-minimized incident logging;
29. clean-device fleet protection while suspect client stays offline;
30. recovery confirmation without falsely claiming historical cleanliness.

No PASS is claimed until exact target runtime/product evidence exists.

## 13. Track D transfer — telemetry is supporting evidence, not permission for emergency overcollection

An incident can justify heightened observation, but telemetry should remain purpose-bound. Existing server/deployment/authentication/audit evidence may be more valuable than adding broad client payload capture during the event. Any emergency expansion should have explicit scope, retention and post-incident rollback.

Guards:
- `incident response need ≠ unlimited telemetry collection authority`;
- `more telemetry ≠ more reliable provenance`.

## 14. EFB / LogMate-like operational judgment

For the company-iPad scenario, the safest generic principle is not `preserve first` or `contain first` in isolation. It is:

**stop continuing authority harm first when credible; preserve irreplaceable data/evidence through the least-destructive path that does not materially prolong that harm.**

Unknowns remain decisive: exact iPadOS/WebKit/MDM network controls, whether the PWA can be inspected/exported without launch, actual auth/token model, server revocation semantics, whether local records are authoritative, background execution, sync triggers and organizational/legal requirements.

## 15. MINTTAP DIRECTION

Until product evidence exists:
- treat containment and acquisition as separate but coordinated gates;
- design remote authority containment so it does not require deleting local authoritative data;
- block replay independently from local read/export/recovery;
- preserve independent remote evidence before reconnect where practical;
- require explicit approval/record when containment sacrifices evidence;
- do not let legal-forensic aspirations delay action against credible continuing harm;
- do not claim a contained client is clean or its records verified.

## 16. OPEN

Product-specific validation remains OPEN for:
- actual auth/session/token/device credential architecture;
- revocation latency and offline behavior;
- authoritative local-data classes;
- worker/cache/update/replay triggers;
- server-side freeze/hold/idempotency controls;
- deployment/origin/provider containment paths;
- managed-iPad MDM/network controls;
- export/acquisition path and its mutations;
- legal/disciplinary evidence requirements;
- incident authority/approval roles;
- fleet communication and clean-client protection.

## 17. CHANGE WATCH

Recheck when:
- NIST/CISA incident-response guidance materially changes;
- WebKit/iPadOS managed-web-app behavior changes;
- Service Worker/background/network capability changes;
- the product chooses its auth/sync/backup architecture;
- managed-iPad/MDM constraints become known;
- legal or organizational incident requirements are defined.

## 18. Gate

**116 PASS (generic).** The Web Manager can now distinguish evidence preservation from containment, separate client isolation from remote authority containment, choose a risk-based ordering, document deliberate evidence sacrifice, preserve irreplaceable local data without keeping unsafe authority active, and hand exact runtime/tooling validation to the appropriate specialists.

Production/device/legal validation remains OPEN.