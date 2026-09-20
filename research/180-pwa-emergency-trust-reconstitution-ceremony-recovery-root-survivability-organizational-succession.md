# 180 — PWA Emergency Trust-Reconstitution Ceremony, Recovery-Root Survivability & Organizational Succession

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + PROVIDER + ORGANIZATIONAL + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A browser/session/offline-state boundaries; Track B recovery/succession UX and safe task continuity; Track C ceremony/destructive continuity validation; Track D privacy-bounded recovery telemetry.
Dependencies: 173–179 distributed security-floor convergence, fail-safe degradation, exception/break-glass governance, emergency compromise and trust reconstitution.

## Why this study exists
179 established that a compromised emergency/recovery root cannot be the sole authority that blesses its successor. The adjacent continuity problem is harder: what happens when the original custodians, provider, organization, legal entity, identity system, site, or combinations of them are unavailable rather than merely compromised?

A recovery mechanism that is cryptographically strong but depends on one employee, one provider account, one office, one IdP, one legal identity, or undocumented institutional memory is not demonstrably survivable. Conversely, making recovery universally available to avoid orphaning creates unilateral-takeover risk.

Central rule:

> **Emergency trust reconstitution must survive loss of expected custodians without turning survivability into unilateral takeover. Recovery authority is a governed, pre-established and tested continuity capability whose custody, independence, succession, evidence and expiry are separate from ordinary production authority. Organizational succession transfers eligibility to participate in a new trust decision; it does not automatically transfer old emergency credentials, sessions or offline authority.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser storage, sessions, SW/cache/IndexedDB, device clocks and reconnect state can preserve local work and stale observations, but cannot establish organizational succession or successor recovery authority.
- **B UX/IA/Content:** high dependency consumer. Owns safe semantics for unavailable custodian/provider, recovery pending, local-work preservation, privileged submission pause, new organizational authority verification and explicit re-admission without exposing recovery topology.
- **C Performance/Accessibility/Quality:** high dependency validator. Owns destructive ceremony exercises across personnel/provider/site loss, quorum loss, stale regions, PITR, offline devices, inaccessible recovery workflows and representative-human comprehension.
- **D Search/Discovery/Analytics:** bounded consumer. Recovery/succession evidence is not acquisition analytics. Aggregate readiness can be measured without creating durable per-person recovery dossiers or publishing sensitive custody topology.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns recovery-root failure domains, custody continuity, ceremony state machine, succession boundaries, anti-orphaning/anti-takeover controls, independent evidence, regional convergence and closure.

## SOURCE
### NIST SP 800-34 Rev. 1 — contingency planning and reconstitution
NIST contingency-planning guidance treats recovery as a coordinated strategy spanning plans, procedures, technical measures, alternate equipment/processing/location and testing. SP 800-34 Rev. 1 also states that plans must be maintained to reflect organizational structure and policies, and its exercise model includes full recovery/reconstitution to a known state.
Source: https://csrc.nist.gov/Topics/Security-and-Privacy/security-programs-and-operations/contingency-planning
Source: https://www.nist.gov/publications/contingency-planning-guide-federal-information-systems
Source: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf

**TRANSFER VALIDATION:** contingency planning is broader than emergency cryptographic authority, but it directly supports the requirement that recovery roles, procedures, alternate resources and exercises remain current when personnel or organizational structure changes.

### NIST SP 800-53 Rev. 5 — alternate processing and separation from common threats
Current NIST control guidance for alternate processing sites emphasizes sufficient separation from the primary site to reduce susceptibility to the same threats and coordination for transfer/assignment of personnel.
Source: https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

**TRANSFER VALIDATION:** geographic/site separation is not itself recovery-root independence. The reusable principle is failure-domain separation: nominally separate recovery resources that share the same identity, administrator, provider or legal dependency may still fail together.

### NIST SP 800-57 Part 1 Rev. 5 — key-management lifecycle
NIST SP 800-57 Part 1 Rev. 5 is the current final general key-management recommendation. It covers key management, compromise, backup, recovery and trust anchors. NIST also defines split knowledge as dividing key knowledge into shares such that fewer than the required shares reveal no key information.
Source: https://www.nist.gov/publications/recommendation-key-management-part-1-general-1
Source: https://csrc.nist.gov/glossary/term/split_knowledge

**CHANGE WATCH:** NIST published SP 800-57 Part 1 Rev. 6 as an Initial Public Draft on 2025-12-05; the public comment period closed 2026-02-05. It is not promoted here over Rev. 5 as final guidance.
Source: https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

**BOUNDARY:** split knowledge is a cryptographic mechanism, not proof of organizational independence. Multiple shares held by identities controlled through one compromised IdP, one administrator, one provider recovery path or one person are not automatically independent.

### CISA cloud emergency-access guidance
CISA cloud guidance recommends least privilege, separation of duties, well-protected emergency `Break Glass` accounts, consideration of coordination among multiple users, extensive logging/auditing, and recognition that privileged administrators may be able to interfere with alerts/logs.
Source: https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

**TRANSFER VALIDATION:** this supports bounded multi-party emergency access and independent evidence, but does not prescribe MintTap/LogMate custody, quorum, legal succession or recovery-root implementation.

## SYNTHESIS — survivability is not credential redundancy
Keep these dimensions distinct:
1. **credential/material survivability** — required secret/key/material remains recoverable;
2. **custodian survivability** — authorized participants remain reachable/replaceable;
3. **identity survivability** — successor participants can be independently identified/authenticated;
4. **organizational survivability** — the organization or legitimate successor can establish authority after personnel/legal/provider change;
5. **provider survivability** — recovery does not silently depend on one provider/account/support channel;
6. **site/device survivability** — loss of office/device/facility does not destroy the only recovery path;
7. **evidence survivability** — recovery can be audited even if production/evidence systems are impaired;
8. **policy survivability** — the ceremony and eligibility rules remain interpretable and current;
9. **runtime convergence** — successor authority actually reaches enforcement points;
10. **offline-fleet convergence** — stale clients cannot import obsolete emergency authority on reconnect.

Persistent guards:
- `backup recovery material exists ≠ recovery ceremony executable`;
- `multiple custodians named ≠ custodians independent`;
- `multiple shares exist ≠ failure domains independent`;
- `custodian reachable ≠ custodian currently eligible`;
- `employee successor appointed ≠ old credential inherited`;
- `legal/entity successor exists ≠ technical authority automatically transferred`;
- `provider account recovered ≠ organizational authority re-established`;
- `quorum met ≠ quorum legitimate after roster/policy change`;
- `recovery succeeded once ≠ recovery path remains current`;
- `ceremony completed ≠ every region/client converged`;
- `offline client retained old recovery artifact ≠ successor authority accepts it`;
- `local data preserved ≠ old privileged authority preserved`.

## Recovery-root survivability model
A recovery root is not necessarily one cryptographic key. It is the minimum governed set of authority/evidence required to establish a new trusted emergency generation when ordinary authority is unavailable or compromised.

Generic requirements:
- identify the actual failure domains on which recovery depends: people, identity provider, cloud/provider, administrator, device, site, legal entity, communications channel, evidence store and time/currentness source;
- avoid claiming independence merely because components have different names;
- ensure loss of one expected custodian does not necessarily orphan recovery when the product's real risk model requires continuity;
- ensure one surviving actor cannot silently redefine eligibility, policy and successor authority alone unless that unilateral risk has been explicitly accepted by the real organization;
- keep recovery material/capability outside the ordinary privileged path when shared compromise would defeat its purpose;
- preserve enough independently verifiable evidence to explain which recovery basis survived and why it was accepted.

This study does not prescribe `k-of-n`, HSMs, paper shares, vaults, hardware keys, provider escrow or any named custody mechanism. Those are implementation decisions requiring Software Engineering/security/organizational evidence.

## Ceremony as a state machine, not a runbook checkbox
Generic ceremony states:
1. **trigger/declare** — establish why ordinary/emergency authority is unavailable, lost or suspected compromised;
2. **scope** — identify affected authority generations/failure domains and preserve UNKNOWN explicitly;
3. **freeze inherited privilege** — prevent stale emergency authority from remaining executable merely because succession is underway;
4. **establish surviving recovery basis** — verify currently eligible recovery participants/evidence outside the failed domain;
5. **verify ceremony policy/currentness** — ensure the procedure/roster itself has not been superseded, rolled back or maliciously changed;
6. **authorize successor generation** — create a new authority generation without inheriting old sessions/tokens/queues;
7. **publish/admit** — distribute successor floor to regions/enforcement dependencies;
8. **invalidate/reconcile** — reject superseded authority and re-admit pending consequences under current policy;
9. **prove enforcement** — test actual consequence paths, not only configuration publication;
10. **progressive reopen** — restore privileged capabilities where current proof exists;
11. **close/review** — retain bounded evidence, repair depleted recovery capacity, update custody/rosters and test the new state.

`ceremony documented ≠ ceremony executable`; exercises must falsify assumptions.

## Custody transfer and personnel succession
Personnel changes create two symmetric hazards:
- **orphaning:** all effective recovery authority leaves with a departed/unavailable custodian;
- **silent inheritance:** a replacement automatically receives predecessor secrets, sessions or authority without a new eligibility decision.

Generic direction:
- succession changes eligibility/custody through an explicit new event/generation;
- predecessor artifacts are revoked/retired/reconciled according to their actual role;
- replacement identity is established independently of merely possessing predecessor material;
- roster/policy administration is not automatically the same capability as exercising emergency recovery;
- departed personnel must not remain a hidden dependency through personal email/phone/device/provider account;
- emergency continuity plans must be reviewed when material organizational/personnel changes occur, not only on a calendar.

## Organizational and legal-entity succession
A merger, acquisition, spin-off, dissolution, provider transfer, insolvency or other legal/organizational transition cannot be reduced to `rename tenant`.

Generic model:
- **historical organization identity** and **current successor eligibility** are distinct;
- old authority may remain necessary for historical verification without remaining valid for new privileged actions;
- successor eligibility requires an independently governed basis appropriate to the real organization/legal context;
- technical systems must not infer legal succession from domain ownership, billing access, MDM ownership or possession of old devices alone;
- if no legitimate successor can be established, the safe state may be preserved local/read/export capability with privileged remote mutation unavailable rather than unilateral takeover.

Legal requirements are OPEN; this study does not decide corporate/aviation/investment-law succession.

## Provider loss and support-channel recovery
Provider support can be part of a recovery dependency but must not be assumed to be an independent organizational authority.

Failure cases:
- provider account inaccessible because the same IdP failed;
- provider support authenticates through the same compromised email/domain;
- billing ownership is mistaken for application authority;
- provider migration exports data but not recovery provenance;
- provider outage makes a hosted vault/quorum simultaneously unavailable;
- support agent/social-engineering path can reset the very controls meant to resist unilateral takeover.

MINTTAP DIRECTION: provider recovery evidence may contribute to reconstitution, but `provider restored account access ≠ local emergency authority restored`.

## Independent recovery evidence
A ceremony should produce evidence sufficient to answer, at minimum:
- what authority/failure domain was unavailable or suspected;
- which recovery policy/generation governed the ceremony;
- which eligibility classes participated, without unnecessarily exposing secrets;
- what independent evidence established their current eligibility;
- what successor generation was created;
- which inherited sessions/tokens/queues/artifacts were invalidated or quarantined;
- which regions/enforcement paths admitted the successor floor;
- what remains UNKNOWN/OPEN;
- when depleted recovery capacity was replenished and retested.

Evidence must be privacy-bounded. Do not create a permanent dossier of personal recovery history, raw identity documents, secret material, flight payloads or unnecessary device identifiers simply to prove continuity.

## PWA / managed-iPad transfer
A LogMate-like PWA can remain useful during organizational/emergency succession without acting as a recovery root.

- Preserve unique local flight/logbook records and drafts through recovery/succession.
- Service Worker, Cache Storage, IndexedDB, cookies and installed-app state may retain historical UI/data observations but cannot prove successor organizational authority.
- A company-owned/supervised iPad does not establish who inherited organizational emergency authority.
- An offline iPad that misses custodian/root succession must not grandfather obsolete emergency credentials on reconnect.
- Reconnect order: preserve local data → establish current server security/recovery generation → reconcile identity/delegation/organizational state → re-admit queued consequence-bearing operations → update application/SW/schema as separately required.
- Old queued work may remain useful evidence/draft content; it is not automatically authorized for submission by the successor organization.
- No generic claim is made that push, background execution, MDM, Shared iPad or device ownership reliably propagates succession/revocation. Physical Safari/Home Screen/managed-device validation remains OPEN.

## UX transfer — Track B
Required semantic distinctions include:
- `Recovery authority is being re-established; privileged submission is paused.`
- `Your work remains saved on this device.`
- `Your organization/account has changed; pending actions must be checked before submission.`
- `Access has been re-established on the server; pending actions are being re-evaluated.`

Do not expose custodian names, share counts, provider recovery topology or secret-bearing ceremony details to ordinary users. Do not state `recovery complete` solely because login or app shell works. Accessible status, keyboard/focus, non-color signaling, screen-reader and representative-human validation remain OPEN.

## Quality / destructive validation — Track C
Define a **200-case generic destructive campaign** across these families:
- sole custodian unavailable/deceased/departed;
- two custodians share one IdP/admin/provider;
- quorum loses one member during ceremony;
- stale roster admits departed employee;
- replacement employee receives predecessor device;
- replacement has same email alias but different identity;
- malicious insider attempts unilateral succession;
- roster administrator self-adds and exercises recovery;
- provider support resets account through compromised email;
- provider outage plus IdP outage;
- office/site loss destroys co-located recovery material;
- nominal offsite copy shares same cloud tenant;
- lost recovery device;
- inaccessible hardware/secret share;
- split-knowledge shares corrupted/mismatched;
- ceremony policy rollback/PITR;
- stale printed/offline procedure;
- old legal entity dissolved;
- merger/acquisition with ambiguous technical owner;
- domain/billing/MDM ownership falsely treated as authority;
- provider migration loses provenance;
- successor root established but old sessions survive;
- one region accepts predecessor root;
- split-view successor generations;
- audit/evidence store unavailable;
- recovery evidence tampered;
- false-green ceremony dashboard;
- time/currentness ambiguity;
- long-offline iPad crosses multiple succession generations;
- stale SW/IndexedDB presents obsolete privileged state;
- queued operation authored under predecessor authority;
- reconnect drains queue before current generation check;
- Shared iPad account switch;
- local flight data wrongly deleted during authority reset;
- inaccessible recovery UI;
- screen-reader status ambiguity;
- human operator mistakes login recovery for authority recovery;
- ceremony completes but depleted backup custody is never replenished;
- exercise passes once then roster/provider dependency drifts.

Campaign definition PASS; runtime/product/device/human execution OPEN.

## MINTTAP DECISION — generic governance
1. Treat recovery-root survivability as continuity of governed authority/evidence, not merely duplicate credentials.
2. Model people, IdP, provider, administrator, site/device, legal entity, evidence store and policy/currentness as possible correlated failure domains.
3. Prevent both orphaned recovery and unilateral takeover; do not infer independence from account/share count alone.
4. Make succession an explicit new eligibility/custody event; do not inherit predecessor sessions, credentials or emergency generation automatically.
5. Keep legal/organizational succession separate from domain, billing, MDM and device ownership.
6. Treat provider account recovery as input evidence, not automatic local emergency-authority restoration.
7. Run recovery as a versioned state machine with freeze, surviving-basis verification, successor generation, invalidation, convergence, enforcement proof and closure.
8. Preserve independently verifiable, privacy-minimized ceremony evidence and explicit UNKNOWN states.
9. Require exercises that include personnel/provider/site loss and return to a known secure state; documentation alone is not evidence of executability.
10. Preserve unique offline local data while remote privileged authority is suspended/reconstituted.
11. On reconnect, current server authority precedes privileged queue drain; stale PWA state cannot import predecessor authority.
12. Do not invent MintTap/LogMate quorum, recovery material, corporate successor, provider behavior, legal obligations or physical-iPad behavior.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** 179 supplies the non-self-blessing successor rule and separates credential, approval-policy, evidence and regional recovery.
- **TRANSFER VALIDATION:** NIST contingency guidance supports maintained roles/responsibilities, alternate recovery resources, exercises and reconstitution to a known state.
- **TRANSFER VALIDATION:** NIST key-management guidance supports treating key recovery/trust anchors as lifecycle/security concerns; split knowledge is one possible mechanism, not an organizational-independence proof.
- **TRANSFER VALIDATION:** CISA supports least privilege, separation of duties, multi-user coordination consideration and extensive emergency administrative logging.
- **CONTRADICTION:** `we have three shares, therefore three independent recovery authorities exist` is rejected.
- **CONTRADICTION:** `the replacement employee inherited the laptop/account, therefore inherited emergency authority` is rejected.
- **CONTRADICTION:** `the provider restored our tenant, therefore organizational authority is restored` is rejected.
- **CONTRADICTION:** `the acquiring company owns the domain/billing account, therefore every old privileged operation is authorized` is rejected.
- **CONTRADICTION:** `the offline iPad still has the old emergency state, therefore it may submit under the predecessor generation` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH
OPEN: actual MintTap/LogMate organizational/legal structure; personnel roles; recovery roots/custodians/quorum; provider/IdP/vault/support dependencies; key/secret material; identity proofing; successor-entity rules; region/control-plane topology; session/token invalidation; authoritative time; evidence/audit storage; BIA/continuity objectives; legal/aviation/investment requirements; managed-iPad/Safari/MDM/Shared-iPad behavior; accessibility and human ceremony evidence.

DEPENDENCY — Software Engineering: current studio evidence is Foundation-stage and must validate concrete ceremony state, generation binding, credential/session invalidation, anti-replay, queue re-admission, provider integration, rollback/PITR resistance and exact PWA/runtime behavior before product PASS. Existing Chromium evidence does not transfer to Safari/iPadOS/EFB.

DEPENDENCY — Design Studio: Web Specialist remains Stage 3 PRACTICE / NOT PASSED at W121; exact runtime, physical-device/PWA, screen-reader and representative-human evidence remain OPEN. Recovery/succession UX cannot be promoted from generic semantics alone.

CHANGE WATCH: NIST SP 800-57 Rev. 6 progression beyond Initial Public Draft; NIST contingency/key-management guidance; CISA privileged/emergency-access guidance; provider recovery mechanisms; Safari/iPadOS PWA/MDM behavior; relevant legal/organizational succession requirements.

## Gate
**180 PASS (generic).** Web Manager can now model recovery-root survivability across personnel/provider/site/organizational loss; distinguish credential redundancy from independent recovery authority; model succession as a new governed eligibility/custody event; reject automatic inheritance via device/domain/billing/provider ownership; specify a reconstitution ceremony state machine with independent evidence and destructive exercises; and preserve local PWA work while obsolete privileged authority is prevented from crossing organizational generations.

Next adjacent bottleneck: **PWA recovery-ceremony liveness, quorum degradation & deadlock-safe governance** — determine how a recovery process avoids permanent lockout when required participants/resources are unavailable without adding an emergency shortcut that collapses independence; how quorum/policy changes are authorized during prolonged disruption; how timeout/escalation differs from authority weakening; and how offline clients remain useful while recovery liveness is unresolved.