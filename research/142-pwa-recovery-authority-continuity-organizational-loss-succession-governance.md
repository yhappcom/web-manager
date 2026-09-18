# 142 — PWA Recovery-Authority Continuity Under Organizational Loss, Credential Unavailability & Succession Governance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + CUSTODY + SUCCESSION-DRILL VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A browser/PWA state boundaries; Track B recovery-state UX; Track C destructive continuity validation; prior studies 111–141, especially 126 and 141.

## Why this study exists

Study 141 closed the generic abuse-resistance boundary: recovery authority must not become a universal master reset, quorum must be sufficiently independent for the threat model, and break-glass must be bounded. That creates a second problem: a recovery system that is safe only while specific people, credentials, identity providers and custody arrangements remain available is not operationally complete.

This study does **not** repeat organizational-loss foundations from 126. It applies them to the newer trust-floor, anti-rollback, compromise-recovery and emergency-reset model from 137–141.

## SOURCE

### NIST key-management continuity
NIST SP 800-57 Part 1 Rev.5 treats availability, backup, archive and key recovery as key-management concerns. Its recovery guidance distinguishes recovery of stored/reconstructed keying material and notes that not every key should be backed up; where continuity can be achieved by re-keying, avoiding backup may reduce compromise exposure. It also states that public signature-verification keys may need archival retention for historical verification, while private signature-key backup is generally undesirable and, when justified, requires highly secure recovery and prompt replacement.

Primary sources:
- NIST SP 800-57 Part 1 Rev.5, final (2020): https://doi.org/10.6028/NIST.SP.800-57pt1r5
- NIST SP 800-57 Part 1 Rev.6 is still an Initial Public Draft (2025-12-05); treat changes as **CHANGE WATCH**, not final authority.

### NIST contingency planning
NIST contingency-planning guidance describes coordinated plans, procedures and technical measures for recovery after disruption, including alternate equipment, alternate processing and alternate locations. NIST SP 800-100 further describes recovery teams with primary and alternate personnel so procedures do not depend on one unavailable individual.

Primary sources:
- NIST CSRC contingency-planning topic / SP 800-34 lineage: https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning
- NIST SP 800-100: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-100.pdf

### Identity assurance is not authority succession
CISA recommends MFA, especially for administrative access, and prefers stronger/phishing-resistant factors where available. This is authentication-hardening evidence, not evidence that one identity channel should own organizational recovery.

Source: https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/require-multifactor-authentication

## SYNTHESIS — failure model

Recovery continuity can fail without an attacker:
1. owner/approver departure, death, incapacity or long absence;
2. loss/destruction/expiry of a recovery credential;
3. IdP, email, password-manager, registrar or cloud-account outage;
4. all approvers sharing one unavailable or compromised failure domain;
5. custody transfer during company sale/reorganization;
6. emergency material existing but being unreadable, undocumented or unverifiable;
7. old personnel retaining authority after succession;
8. quorum becoming impossible after one member leaves;
9. an emergency workaround silently weakening trust-floor/anti-rollback policy;
10. historical verification material being lost while current authority is successfully rotated.

The central distinction is:

`recovery authority secure today ≠ recovery authority survivable tomorrow`.

Security and availability are coupled but not interchangeable. Increasing copies/holders can improve availability while increasing compromise surface; minimizing holders can reduce exposure while creating organizational single points of failure.

## SYNTHESIS — authority classes must remain separate

Do not collapse these into one credential or role:
- ordinary administrative authority;
- account/identity recovery;
- deployment authority;
- current signing/trust authority;
- trust-floor reset/rebootstrap authority;
- emergency/break-glass authority;
- historical verification custody;
- provenance/audit custody.

A successor who can operate the company does not automatically need the ability to forge historical signatures or arbitrarily select an older security epoch.

Persistent guards:
- `organizational successor ≠ cryptographic successor until authorized transition completes`;
- `employment ended ≠ authority automatically revoked everywhere`;
- `new owner authenticated ≠ old recovery authority safely retired`;
- `MFA available ≠ organizational continuity achieved`;
- `backup credential exists ≠ backup credential usable`;
- `credential usable ≠ credential currently authorized`;
- `same IdP for all approvers ≠ independent recovery path`;
- `two custodians ≠ two failure domains`;
- `quorum policy documented ≠ quorum achievable after personnel loss`;
- `availability emergency ≠ authorization to lower historical trust floor`;
- `current authority rotated ≠ historical verifier material preserved`;
- `custody transferred ≠ provenance continuity proven`.

## MINTTAP DECISION — minimal sufficient succession model

Do not impose enterprise-scale ceremony on a small app company. Instead, recovery design should satisfy four properties proportional to consequence:

1. **No irreplaceable human singleton** — every consequence-bearing recovery procedure has an authorized succession path that does not require one specific person's continued availability.
2. **No universal online master credential** — continuity must not be purchased by creating a permanently active credential that bypasses all earlier controls.
3. **Independent-enough custody** — high-consequence recovery material/approval paths should not all share the same likely failure domain.
4. **Tested succession, not paper succession** — an alternate must demonstrate that the recovery path can be executed without silently broadening authority.

The preferred pattern is bounded successor capability: authorize transition to the current safe trust/recovery state, not arbitrary `setEpoch(any)` or unrestricted historical signing.

## MINTTAP DECISION — succession transaction

Treat organizational succession as an explicit security transaction rather than an HR note:

`Nominate successor → verify independent authority → bind exact capability/scope → activate successor → verify usable recovery path → revoke/retire predecessor authority → preserve historical verification context → record provenance → test post-transition recovery`.

The transition needs a stable operation identity so retries after ambiguous acknowledgement do not create multiple successors or broader authority.

For planned departure, overlap may be appropriate long enough to validate the successor, but overlap must be bounded and deliberately retired. For unplanned loss, use the pre-established recovery path; do not invent a lower-security path during the incident.

## Credential unavailability vs compromise

These are different states.

- **Unavailable but not suspected compromised:** continuity may use an approved alternate/recovery mechanism.
- **Possibly compromised:** recovering the same credential can restore availability while preserving attacker capability; replacement/rotation and affected-window analysis are required.
- **Unknown:** do not silently classify as safe merely because compromise cannot be proven.

NIST SP 800-57 supports this distinction in key recovery: when compromise is suspected, replacement should follow recovery as soon as practical.

## IdP/provider outage

An IdP outage is not permission to bypass server-side recovery authorization. Conversely, if every recovery approver, audit viewer and emergency credential depends on the same IdP, the architecture has a correlated availability dependency.

A small company should inventory whether high-consequence recovery depends on the same:
- identity provider;
- email domain/provider;
- password manager;
- primary device;
- cloud/root account;
- DNS/registrar account;
- physical custody location.

The goal is not maximum provider diversity. It is to identify whether a plausible single failure defeats the required recovery objective.

## Emergency credential aging

Emergency material can decay even without compromise: algorithms retire, formats change, hardware tokens fail, people forget procedures, contact data changes, or a credential expires.

Therefore emergency continuity needs lifecycle checks:
- existence/inventory;
- validity/expiry;
- decryptability/readability;
- verifier/tool availability;
- custody/contact currency;
- authorization scope;
- revocation/rotation status;
- rehearsal evidence.

`sealed credential present ≠ executable recovery path`.

Do not repeatedly exercise a live high-value secret when a safer verification method can prove custody/readiness; exact implementation remains a Software Engineering/security design dependency.

## Historical verification during succession

Current signing authority and historical verification material have different continuity requirements. A company can rotate current signing/recovery authority while retaining old public verification material and provenance necessary to verify historical records.

Do not give a successor obsolete private signing power merely to retain historical verification capability.

`historical verification continuity ≠ historical signing authority continuity`.

## PWA / EFB application

A long-offline company iPad may return after organizational authority changed several times. The device cannot infer legitimate organizational succession from:
- a new Service Worker;
- a new account session;
- a different support contact;
- a locally cached policy;
- the fact that the company still controls the domain.

On reconnect, local irreplaceable records remain preservable, but remote mutation authority waits for current trust/recovery policy convergence. Old personnel/device credentials must not regain authority merely because the device missed revocation while offline.

`offline during succession ≠ grandfathered old authority`.

The product-specific mechanism remains OPEN until actual LogMate identity, backend, device and managed-iPad architecture exists.

## Track transfers

### Track A — Platform & Browser
Browser state may retain cached identity/policy material across personnel transitions, but cannot establish organizational succession. Service Worker/cache freshness and organizational authority freshness remain separate.

### Track B — UX / IA
Recovery UI needs explicit states such as `SUCCESSION-PENDING`, `PREDECESSOR-REVOKED`, `ALTERNATE-UNAVAILABLE`, `EMERGENCY-LIMITED`, `LOCAL-DATA-PRESERVED / REMOTE-WRITE-BLOCKED`. Avoid presenting an unavailable approver as a generic network error.

### Track C — Quality
Own destructive succession/recovery drills. A documented alternate without a successful independent drill is not PASS.

### Track D — Analytics
Telemetry may reveal recovery attempts/duration but cannot prove custody independence, legitimacy of succession, or absence of dormant predecessor authority.

### Track E — Owner
Own authority topology, custody, succession, revocation, correlated-provider dependencies, break-glass lifecycle and incident normalization.

## VALIDATION — destructive campaign

Product validation should eventually cover at least these classes:
1. sole owner unavailable;
2. one quorum member departs;
3. quorum member departs without revocation;
4. predecessor account still authenticates after handoff;
5. successor activation ACK lost;
6. duplicate succession request;
7. same request ID with changed successor/scope;
8. IdP outage during recovery;
9. email-provider outage;
10. password-manager loss;
11. primary hardware token destroyed;
12. alternate token expired;
13. all recovery factors at one physical location lost;
14. emergency material unreadable;
15. emergency verifier/tool obsolete;
16. planned ownership transfer;
17. abrupt organizational loss;
18. successor tries arbitrary trust-floor rollback;
19. old recovery package replayed after succession;
20. stale Service Worker shows predecessor as active;
21. stale cached policy after authority rotation;
22. long-offline iPad reconnects after multiple successions;
23. old device credential attempts mutation;
24. current signing key rotated while historical verification remains required;
25. predecessor private material discovered after departure;
26. compromise suspected during credential recovery;
27. audit/provenance store unavailable during succession;
28. partial successor activation before crash;
29. successor active but predecessor revocation failed;
30. full continuity drill from organizational loss through normalization.

## OPEN

No production claim is made about MintTap or LogMate identity provider, admin model, corporate ownership, number of personnel, custody arrangement, key hierarchy, recovery credentials, device identity, backend authorization, managed-iPad policy or legal/aviation retention obligations. Those require canonical project/runtime evidence.

## CHANGE WATCH

- NIST SP 800-57 Part 1 Rev.6 remains draft as of this study; re-evaluate when final.
- Browser/WebKit storage and managed-device behavior remain separately change-sensitive but do not replace organizational authority evidence.
- Identity-provider emergency-access features are provider-specific and must be validated if a provider is selected.

## Gate result

**PASS (generic).** The Web Manager can now distinguish abuse-resistant recovery from survivable recovery; model planned/unplanned succession; separate unavailability from compromise; preserve historical verification without obsolete signing authority; identify correlated organizational/provider failure domains; and define destructive continuity drills without inventing MintTap production facts.

Production and managed-EFB validation remain **OPEN**.

## Next highest-value adjacent question

**PWA recovery-authority inventory, dormant-access detection & periodic survivability drills.** Succession policy can still decay silently if dormant predecessor credentials, untested alternates, expired emergency material or correlated provider dependencies accumulate. The next work should turn continuity into measurable assurance without converting a small-company process into heavyweight compliance theater.