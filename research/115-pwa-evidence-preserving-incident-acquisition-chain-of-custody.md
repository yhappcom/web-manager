# 115 — PWA Evidence-Preserving Incident Acquisition & Chain-of-Custody Boundary

Status: **PASS (generic) / PRODUCT TOOLING + MANAGED-IPAD + LEGAL-FORENSIC VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 103 backup assurance; 110 independent custody; 113 hostile-origin compromise scoping; 114 compromise-era integrity/provenance; Track A Service Worker/storage mechanics; Track C incident validation; Software Engineering Data/Quality/Systems for implementation evidence.

## Purpose

114 established that compromise-era records may be preserved yet unverifiable. This study closes the next generic question: **how should an offline PWA client be observed/acquired when opening, reconnecting, updating, exporting or debugging it can itself mutate Service Worker, cache, IndexedDB, outbox, session or acknowledgement evidence?**

This is incident-response guidance, not a legal-forensic procedure. Exact MintTap/LogMate storage layout, export path, managed-iPad policy, MDM controls, browser inspection capability, legal jurisdiction and admissibility requirements remain OPEN.

## 1. Five-track balance

- **A Platform/Browser:** supplies mutation mechanics: service workers can start independently; developer tools can inspect but may also expose mutation controls; browser/application state is distributed across worker, Cache Storage, IndexedDB, cookies/session and remote state.
- **B UX/IA/Content:** consumes truthful acquisition/recovery states and must not label an ordinary export as a forensic image or an incident snapshot as a verified clean backup.
- **C Quality:** owns acquisition-before-remediation campaigns, repeatability, mutation detection and target-engine/device validation.
- **D Discovery/Analytics:** remote telemetry can corroborate server-observed chronology but must not be silently altered/expanded to copy sensitive domain payloads.
- **E Architecture/Security/Operations:** highest-risk owner; owns acquisition order, preservation, custody metadata, separation of incident-response evidence from formal forensic claims and recovery handoff.

E remains the bottleneck; A and C are the strongest dependencies.

## 2. SOURCE — current incident response is risk-management integrated; forensic acquisition remains a distinct discipline

NIST SP 800-61 Rev.3, finalized April 2025, supersedes Rev.2 and integrates incident response across CSF 2.0 risk-management activities. NIST still lists forensics as part of its Incident Response project resources. NIST SP 800-86 remains the dedicated practical forensic guide and explicitly describes an IT/incident-response view rather than law-enforcement procedure.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://csrc.nist.gov/projects/incident-response
- https://csrc.nist.gov/pubs/sp/800/86/final

**SYNTHESIS:** an operational incident snapshot can be highly useful without satisfying formal evidentiary requirements. Conversely, calling an export a `forensic image` does not make it one.

Guards:
- `incident evidence useful ≠ formal forensic evidence established`;
- `application export ≠ forensic image`;
- `chain-of-custody notes exist ≠ legal admissibility established`.

## 3. SOURCE — acquisition order must account for value, volatility and acquisition side effects

SP 800-86 recommends a standard collection process: identify data sources, develop an acquisition plan, acquire data and verify integrity. It says acquisition priority should consider likely value, volatility and effort, and that a decision about legal/disciplinary evidence preservation should be made before collection where applicable. It also warns that collection itself can alter a system and emphasizes preserving volatile data appropriately.

Source:
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-86.pdf

**TRANSFER VALIDATION:** classic OS volatility ordering cannot be copied mechanically into a browser PWA. PWA evidence has different mutation triggers: launching the app can start a worker; network restoration can trigger fetch/sync/application logic; a new navigation can cause update checks; application export code can write metadata; browser tools may expose edit/delete/clear controls.

Guards:
- `most volatile first ≠ blindly open the PWA first`;
- `read-only intent ≠ acquisition path is non-mutating`;
- `device powered on ≠ application state static`.

## 4. Browser/PWA acquisition is a state-transition problem

Before touching a suspect offline PWA, conceptually inventory possible evidence planes:
1. device/OS/browser/Home Screen app identity and version;
2. network state and known connectivity transitions;
3. service-worker registration/active/waiting generation where observable;
4. cached executable/resource generations;
5. IndexedDB/local storage/cookie/session state;
6. local record and attachment stores;
7. outbox/pending operation state;
8. local acknowledgement/reconciliation metadata;
9. remote server/audit/telemetry state already outside the client;
10. backup/export artifacts that predate the incident;
11. trust/key/schema/application generations.

The acquisition plan should state which observation can trigger which mutation before it is executed.

Guard: `state observed after interaction ≠ state that existed before interaction`.

## 5. SOURCE — browser developer tools are inspection tools, not inherently non-destructive forensic acquisition

Apple's current Safari Developer Features documentation says macOS Safari can inspect webpages, Home Screen web apps and service workers on connected iOS/iPadOS devices. Web Inspector exposes resources, network activity and storage including IndexedDB. Service workers are separately inspectable and may be short-lived; automatic inspection can be configured for newly launched workers.

Chrome's Application panel likewise exposes manifests, service workers, Cache Storage and IndexedDB, but the same tools can update workers, edit/delete IndexedDB values and clear site data.

Sources checked 2026-09-18:
- https://developer.apple.com/documentation/safari-developer-tools
- https://developer.apple.com/documentation/safari-developer-tools/develop-menu
- https://developer.apple.com/documentation/safari-developer-tools/web-inspector
- https://developer.chrome.com/docs/devtools/application
- https://developer.chrome.com/docs/devtools/storage/indexeddb

**SYNTHESIS:** DevTools/Web Inspector can provide diagnostic visibility but must not be treated as a write-blocked acquisition environment. Exact act-of-inspection side effects and export capabilities require engine/version/device validation.

Guards:
- `inspectable ≠ non-mutating`;
- `DevTools visible ≠ forensic acquisition supported`;
- `service worker listed ≠ complete historical worker evidence preserved`;
- `storage panel shows data ≠ byte-complete storage image acquired`.

## 6. Preserve remote evidence before reconnecting the client where possible

If server-side acknowledgement, audit, deployment, DNS/CDN, authentication or telemetry evidence already exists independently, preserve/export its relevant incident window before reconnecting the suspect client where practical. Reconnection can generate new requests, refresh sessions, receive new worker/application code, reconcile outbox state or change server-side timestamps/status.

This does not mean remote evidence is automatically authoritative for local user intent; 114's provenance boundaries remain.

Guards:
- `remote evidence preserved ≠ local evidence preserved`;
- `server chronology ≠ client action chronology`;
- `reconnect for diagnosis ≠ neutral observation`.

## 7. Generic acquisition ladder for an offline-authoritative PWA

A defensible operational sequence is:

1. **Declare incident scope and preservation objective.** Decide whether the goal is operational diagnosis/recovery or whether formal legal/disciplinary evidence may be required. Escalate legal/forensic requirements before destructive handling.
2. **Record external facts first.** Device identity, OS/browser/app mode/version if visible without launching the app, current connectivity, time source, physical/custody state and operator.
3. **Prevent avoidable network transitions.** Do not reconnect merely to make inspection easier until remote evidence is preserved and mutation risks are understood. Exact airplane-mode/MDM handling is product/device specific.
4. **Preserve independent remote evidence.** Server receipts, audit records, deployment identities, trust/revocation state and incident windows where available.
5. **Choose the least-mutating supported local observation path.** Prefer platform-supported inspection/export that has been validated not to trigger unacceptable state transitions for the exact runtime. If no such path exists, record that limitation rather than claiming pristine acquisition.
6. **Capture original artifact/state before normalization.** If the application has a validated export/backup path, preserve the original output and separately record that invoking export may itself mutate application metadata unless tested otherwise.
7. **Compute integrity identifiers after acquisition.** Hash/capture metadata for copied artifacts; retain originals read-only in incident storage where operationally possible. A digest detects later byte changes; it does not prove pre-acquisition authenticity.
8. **Document every state-changing action.** Launch, unlock, inspector attach, network enable, worker update, export, restart, cache/storage operation, credential rotation and replay/reconciliation must be recorded.
9. **Analyze copies, not the sole irreplaceable artifact.** Keep recovery experiments and parser/converter work away from the only preserved copy.
10. **Separate acquisition from remediation.** Do not clear cache/storage, unregister worker, rotate local trust state or replay outbox until the required preservation checkpoint is complete.
11. **Re-enter recovery under 113/114.** Restore executable/trust authority, classify record provenance and reconcile operations without silently relabeling acquired uncertainty as clean.

## 8. Integrity metadata is necessary but bounded

For each acquired artifact/snapshot, useful operational metadata includes:
- acquisition identifier;
- source device/application/origin identity as actually observed;
- acquisition operator/tool/version;
- start/end time and time-source confidence;
- connectivity state;
- source state before/after known interaction;
- exact method/commands/UI path where reproducibility matters;
- cryptographic digest of the acquired bytes;
- storage location/access history;
- known limitations or mutations introduced by acquisition.

Guards:
- `hash matches ≠ source was trustworthy`;
- `hash matches ≠ acquisition was complete`;
- `timestamp recorded ≠ timestamp trusted`;
- `tool produced output ≠ tool validated for this artifact/runtime`.

## 9. Chain of custody: use the term narrowly

NIST's digital-forensics glossary describes strict digital forensics as preserving integrity and maintaining a strict chain of custody, with validated/repeatable methods and possibly judicial use. SP 800-86 says formal chain of custody should be followed when evidence may be used in legal or internal disciplinary proceedings and advises consulting management/legal counsel for applicable law.

Sources:
- https://csrc.nist.gov/glossary/term/digital_forensics
- https://csrc.nist.gov/pubs/sp/800/86/final

**MINTTAP DIRECTION:** ordinary Web Manager incident records should use terms such as `incident acquisition record`, `preservation log`, `artifact digest` and `custody/access record` unless a qualified process has actually established formal chain of custody.

Guard: `preservation log ≠ formal chain of custody`.

## 10. Irreplaceable user data changes the remediation order

For an EFB-like PWA, destructive browser cleanup may remove the only copy of legitimate flight records. Security response therefore cannot default to `clear all site data` before acquisition. Conversely, preserving bytes does not authorize them for replay.

Default generic ordering:

`preserve → classify → replace executable/authority plane → validate trust → reconcile data/operations → authorize replay → retire incident artifacts according to policy`.

Guards:
- `malicious executable state present ≠ user data should be destroyed`;
- `user data preserved ≠ user data safe to replay`;
- `cleanup succeeded ≠ evidence preservation succeeded`.

## 11. Track B — truthful incident/recovery UX

Candidate operator/user states:
- device isolated for preservation;
- records preserved, integrity not yet verified;
- export captured, acquisition may have changed metadata;
- remote state preserved separately;
- executable state not yet trusted;
- reconciliation required;
- records available for review/export but automatic sync blocked;
- recovery completed with unresolved historical uncertainty.

Do not use `forensic backup`, `verified original`, `clean device` or `fully recovered` without evidence supporting those exact claims.

## 12. Track C — acquisition validation campaign

Product validation should include at least:
1. launch while offline and detect whether any DB metadata changes;
2. launch while online and observe worker/update/sync mutations;
3. inspector attach without launching visible UI where supported;
4. inspector attach causing service-worker launch;
5. application export with before/after storage diff;
6. backup/export interrupted mid-write;
7. browser restart before acquisition;
8. OS restart before acquisition;
9. network restored before remote evidence capture;
10. stale outbox auto-replay on reconnect;
11. worker update check on navigation;
12. waiting worker activation during acquisition;
13. session/token refresh on reconnect;
14. server acknowledgement arrives during acquisition;
15. Cache Storage mutation during app launch;
16. IndexedDB version migration triggered by new code;
17. storage-pressure/eviction event;
18. acquisition copy hash verification;
19. analysis performed only on duplicate artifact;
20. malformed/hostile record safely inspected without executing content;
21. incident log records operator/tool/time/connectivity/action;
22. local and remote clocks disagree;
23. repeated acquisition demonstrates expected/non-expected differences;
24. Chromium diagnostic path;
25. independent engine path;
26. Safari/WebKit Home Screen path on target physical iPad;
27. managed-iPad policy permits/blocks Web Inspector or export;
28. accessibility of incident/recovery states;
29. privacy review proves no unnecessary sensitive duplication;
30. remediation cannot begin before preservation gate unless an explicit containment exception is recorded.

No runtime PASS is inferred.

## 13. Cross-repository transfer

### Design Studio
Canonical `progress/WEB_STATUS.md` checked 2026-09-18: Web Design remains **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. W067 defines a repair-to-browser closure ladder after real widget failures. Incident/recovery state labels above are requirements only; no browser/Safari/AT/device UX PASS transfers.

### Software Engineering Studio
Canonical `progress/STATUS.md` checked 2026-09-18: all specialists remain **Foundation IN STUDY**. Systems S005 supplies artifact/release identity discipline but not PWA acquisition tooling. Exact storage snapshot/export implementation, immutable-copy handling, parser isolation, operation replay and mobile/browser acquisition tools remain engineering handoffs.

## 14. CHANGE WATCH

- NIST SP 800-61 Rev.3 is current final as of 2026-09-18; it superseded Rev.2 in April 2025.
- SP 800-86 remains useful but dates to 2006; apply its collection/integrity/custody principles, not stale platform-specific procedures.
- Safari/Web Inspector and Chromium DevTools capabilities are version-sensitive.
- Managed-device inspection/export policy can differ from consumer-device capability and requires exact MDM/device validation.
- Legal/disciplinary evidence requirements are jurisdiction and organization specific; Web Manager generic guidance is not legal advice.

## 15. Durable synthesis

A suspect offline PWA is not a passive file. It is a distributed state machine whose **observation can cause state transitions**. Incident acquisition therefore requires an explicit mutation model before interaction, preservation of already-independent remote evidence, least-mutating validated local acquisition, artifact integrity metadata, separation of originals from analysis copies, and a hard boundary between acquisition and remediation.

Persistent guards:
- `incident evidence useful ≠ formal forensic evidence established`;
- `application export ≠ forensic image`;
- `most volatile first ≠ blindly open the PWA first`;
- `read-only intent ≠ acquisition path is non-mutating`;
- `state observed after interaction ≠ state that existed before interaction`;
- `inspectable ≠ non-mutating`;
- `DevTools visible ≠ forensic acquisition supported`;
- `reconnect for diagnosis ≠ neutral observation`;
- `hash matches ≠ source was trustworthy or acquisition complete`;
- `preservation log ≠ formal chain of custody`;
- `malicious executable state present ≠ user data should be destroyed`;
- `user data preserved ≠ user data safe to replay`;
- `cleanup succeeded ≠ evidence preservation succeeded`.

## 16. OPEN / next boundary

Product/runtime OPEN:
- exact managed-iPad/WebKit/Home Screen acquisition and inspection path;
- whether company MDM permits Web Inspector, Files/share/export or device backup;
- whether launching/exporting the actual PWA mutates IndexedDB/outbox/worker metadata;
- exact local storage schema, attachment storage and export format;
- server/audit/deployment evidence sources and retention;
- legal/disciplinary evidence requirements and qualified forensic process;
- validated acquisition toolchain and repeatability.

Highest-value adjacent generic boundary: **incident containment vs evidence preservation under active compromise** — when continuing network isolation preserves evidence but delays credential/trust revocation or remote containment, define decision gates for destructive/remote containment actions, document evidence sacrificed, and prevent evidence-preservation goals from prolonging active harm.