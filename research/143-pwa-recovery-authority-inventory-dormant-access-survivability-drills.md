# 143 — PWA Recovery-Authority Inventory, Dormant-Access Detection & Periodic Survivability Drills

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + IDENTITY/ADMIN + CUSTODY + DRILL VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A PWA/browser-state boundaries; Track B recovery-state UX; Track C destructive validation; Track D bounded telemetry; studies 126–142, especially 141–142.

## Why this study exists

Study 142 established that recovery authority must survive organizational loss without becoming a universal master credential. That guarantee decays unless the organization can detect dormant predecessor authority, orphaned service/recovery identities, unusable alternates, correlated failure domains and emergency material that exists on paper but no longer works.

This study turns recovery continuity into a **measurable assurance cycle**. It deliberately does not impose an enterprise compliance program on a small app company.

## SOURCE

### Account/access review and dormant authority
CISA hardening guidance recommends removing unnecessary accounts, periodically reviewing accounts to verify continued need, applying least privilege and monitoring accounts in use. CISA ransomware guidance specifically recommends quarterly audits of user/admin accounts for inactive or unauthorized accounts; that cadence is context-specific guidance, not a universal MintTap requirement.

Sources:
- CISA Enhanced Visibility and Hardening Guidance: https://www.cisa.gov/resources-tools/resources/enhanced-visibility-and-hardening-guidance-communications-infrastructure
- CISA #StopRansomware Guide: https://www.cisa.gov/stopransomware/ransomware-guide

OWASP NHI Top 10 (2025) identifies improper offboarding of non-human identities as a risk when applications are deprecated, owners depart, or credentials remain accessible after personnel departure. This is particularly relevant because recovery authority may live in service accounts, deploy keys, API credentials, CI identities or automation rather than only human admin accounts.

Source: https://owasp.org/www-project-non-human-identities-top-10/2025/1-improper-offboarding/

### Exercise, maintenance and evidence
NIST SP 800-34 Rev.1 treats contingency-plan testing/exercises and maintenance as lifecycle activities. Exercises can expose personnel-availability failures; results and lessons should be documented and incorporated into plan updates. The guide says plans should be reviewed for accuracy/completeness at least annually or after significant changes, while some elements such as contact lists may require more frequent review. This is federal-system guidance and is transferred as a lifecycle principle, not adopted as MintTap compliance or cadence.

Source: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf

NIST SP 800-84 provides a general test/training/exercise framework intended to prepare personnel, exercise plans and test systems. NIST SP 1339 (2026) reinforces a modern operational pattern in the backup domain: integrate recovery assets into change management, test them, and review them during recovery exercises. These support the principle that possession/documentation is weaker evidence than executable recovery.

Sources:
- NIST SP 800-84: https://csrc.nist.gov/pubs/sp/800/84/final
- NIST SP 1339, published 2026-06-17: https://doi.org/10.6028/NIST.SP.1339

## SYNTHESIS — assurance is not inventory alone

An inventory answers **what should exist**. Assurance asks whether the listed authority is still legitimate, sufficiently independent, technically usable and capable of producing the bounded recovery outcome.

Persistent guards:
- `credential inventoried ≠ credential currently authorized`;
- `credential currently authorized ≠ credential usable`;
- `credential usable ≠ recovery path survivable`;
- `account inactive ≠ account harmless`;
- `no recent login ≠ authority revoked`;
- `employee account removed ≠ service/recovery identities removed`;
- `owner field populated ≠ owner still accountable`;
- `two recovery paths listed ≠ two independent failure domains`;
- `drill completed ≠ recovery outcome correct`;
- `one successful drill ≠ future survivability guaranteed`;
- `telemetry silent ≠ dormant authority absent`.

## SYNTHESIS — recovery-authority inventory model

For each consequence-bearing recovery capability, inventory the minimum facts needed to reason about it without storing secrets in the inventory itself:

- stable authority/capability identifier;
- authority class: ordinary admin, deployment, identity recovery, trust-floor reset/rebootstrap, emergency/break-glass, signing/trust, historical verifier/provenance custody;
- bounded scope/effect;
- accountable current owner/custodian and successor path;
- authentication/credential class without secret material;
- provider/failure-domain dependencies: IdP, email, password manager, cloud/root, registrar/DNS, device, physical custody;
- creation/activation and intended expiry/rotation state;
- last authorization review;
- last safe readiness evidence;
- predecessor/supersession/revocation relationship;
- whether current use should be online, dormant, sealed or verify-only;
- evidence/provenance pointer for the last review/drill.

The inventory must not become a credential vault or a second authorization source. Runtime authorization remains authoritative.

`inventory says revoked ≠ runtime authority revoked` and `runtime revoked ≠ stale inventory harmless`.

## Dormant-access detection

Dormancy is a diagnostic signal, not a revocation rule. A rarely used emergency credential can be legitimately dormant, while a predecessor service account can be dangerously dormant.

Classify at least:
1. **EXPECTED-DORMANT** — bounded emergency/recovery material intentionally unused but periodically verified;
2. **ACTIVE-EXPECTED** — ordinary authority with justified recent use;
3. **INACTIVE-REVIEW** — authority still enabled but use/need is unclear;
4. **ORPHANED** — owner/custodian no longer valid or no successor exists;
5. **SUPERSEDED-STILL-ACTIVE** — replacement exists but predecessor still authorizes;
6. **UNUSABLE-ALTERNATE** — listed recovery path cannot currently execute;
7. **CORRELATED-DEPENDENCY** — nominally separate paths share a critical failure domain;
8. **UNKNOWN** — evidence is insufficient.

Do not auto-delete solely because an account is old or unused. Consequence-bearing removal needs dependency analysis so dormant-access cleanup does not destroy the only recovery path.

## MINTTAP DECISION — small-company assurance loop

Use a compact event-driven + periodic loop rather than heavyweight certification:

`Inventory → reconcile against runtime/provider reality → flag drift → review consequence/dependency → revoke/repair/rotate → exercise bounded path → record result → retire stale evidence → repeat after meaningful change`.

Trigger review after material events such as personnel departure, provider/IdP change, domain/registrar change, device/custody loss, recovery-policy change, key/trust transition, incident, failed recovery attempt, or architecture migration. A calendar cadence is a backstop, not the sole freshness mechanism.

No universal quarterly/monthly MintTap cadence is asserted. CISA's quarterly example and NIST's annual/change-driven guidance demonstrate that cadence is risk/context dependent. Product cadence remains OPEN until actual authority topology and consequence are known.

## Survivability drill ladder

Avoid jumping directly to dangerous live resets. Evidence should escalate by consequence:

1. **Inventory reconciliation** — verify listed principals/capabilities against actual provider/runtime state.
2. **Readiness inspection** — verify contacts, custody, expiry, tools, formats and successor availability without exposing secrets unnecessarily.
3. **Tabletop dependency loss** — simulate owner/IdP/email/device/provider loss and identify correlated blockers.
4. **Non-destructive authentication/capability proof** — where implementation safely permits, prove the alternate can authenticate or produce a bounded test artifact without changing production trust state.
5. **Isolated recovery exercise** — exercise recovery in a staging/isolated environment with production-equivalent policy where meaningful.
6. **Controlled production recovery drill** — only when consequence and architecture justify it, with rollback/containment and explicit authorization.

A lower rung cannot prove all properties of a higher rung. Conversely, repeatedly invoking live emergency credentials merely to generate evidence can increase exposure.

`tabletop PASS ≠ credential usable`; `credential usable ≠ production recovery safe`; `staging PASS ≠ managed-iPad PASS`.

## Drill quality and success criteria

A drill is not PASS merely because service becomes available. Evaluate separately:
- legitimate authority used;
- intended quorum/independence preserved;
- no unauthorized trust-floor rollback;
- exact bounded recovery effect achieved;
- predecessor/dormant authority remains revoked;
- local irreplaceable data preserved where required;
- remote mutation remains blocked until trust convergence;
- provenance/audit evidence survives;
- emergency capability is retired/normalized after use;
- recovery time and blockers are measured without turning the metric into a false SLA;
- discovered drift is assigned and actually retired.

## Track transfers

### Track A — Platform & Browser
Browser/Service Worker/Cache/IndexedDB state can retain stale authority presentation or local data after organizational changes. It cannot prove that a recovery principal is still authorized. Site-data deletion or PWA reinstall can also remove local evidence, so the browser must not be the sole authority inventory.

### Track B — UX / IA
Own explicit user/operator states: `RECOVERY-REVIEW-REQUIRED`, `ALTERNATE-UNAVAILABLE`, `AUTHORITY-SUPERSEDED`, `LOCAL-DATA-PRESERVED / REMOTE-WRITE-BLOCKED`, and `RECOVERY-COMPLETE / NORMALIZATION-PENDING`. Avoid generic “sync failed” messaging when the actual blocker is authority assurance.

### Track C — Quality
Own reproducible scenario IDs, evidence capture, negative tests and drill repeatability. A drill should test the failure mode, not merely rehearse the happy path. Physical Safari/managed-iPad evidence remains required for EFB claims.

### Track D — Analytics
Telemetry may identify use/non-use, failures and recovery duration but is supporting evidence only. Analytics cannot prove absence of an uninstrumented credential, custody independence, legitimacy of a successor or complete revocation. Avoid copying sensitive recovery payloads into analytics.

### Track E — Owner
Own inventory semantics, runtime reconciliation, authority drift, revocation, dependency topology, drill ladder, exception lifecycle and normalization.

## PWA / EFB application

A company iPad can remain offline across personnel, key, policy and provider changes. On reconnect:
- do not treat cached recovery UI/policy as authority evidence;
- do not treat old device credential silence as revocation evidence;
- preserve irreplaceable local records;
- classify current trust/recovery authority before remote mutation;
- require current server-side authorization and anti-rollback policy convergence;
- include stale Service Worker/cache and device replacement in drills.

No assumption is made that a managed company iPad can execute unattended background sync, retain storage indefinitely, use a particular file/share API, or communicate directly with a native phone. Those remain product/platform validation questions.

## VALIDATION — 30-case campaign

1. predecessor human account still active after departure; 2. predecessor API/service credential remains active; 3. orphaned service account; 4. emergency account intentionally dormant; 5. emergency credential expired; 6. hardware token unreadable/unavailable; 7. successor contact stale; 8. inventory says revoked but runtime still accepts; 9. runtime revoked but inventory says active; 10. same IdP failure disables both approvers; 11. same email domain disables both recovery channels; 12. same password manager contains all alternates; 13. all physical custody at one lost location; 14. registrar/DNS dependency omitted; 15. cloud-root dependency omitted; 16. drill owner unavailable; 17. tabletop passes but credential authentication fails; 18. staging passes but production policy differs; 19. recovery succeeds by unauthorized trust-floor downgrade; 20. recovery succeeds but predecessor remains active; 21. recovery succeeds but audit/provenance missing; 22. emergency path remains enabled after drill; 23. ACK loss causes duplicate recovery attempt; 24. same operation ID with changed scope; 25. stale Service Worker shows old recovery authority; 26. stale cache after current server revocation; 27. long-offline iPad reconnects after multiple successions; 28. local data preserved while remote write blocked; 29. site-data clear/reinstall removes local assurance state; 30. full organizational-loss drill through normalization and drift retirement.

## OPEN

Actual MintTap/LogMate account model, personnel count, identity provider, cloud/registrar, service accounts, recovery credentials, custody, key hierarchy, managed-iPad policy, server authorization, runtime inventory APIs, telemetry, drill environment, legal/aviation obligations and acceptable recovery objectives are unknown. No production PASS is claimed.

## CHANGE WATCH

- Provider-specific dormant-account, emergency-access and audit APIs change and must be validated after provider selection.
- Managed iPad/WebKit storage and lifecycle behavior remains separately change-sensitive.
- Security guidance cadence examples must not become timeless universal rules.

## Gate result

**PASS (generic).** The Web Manager can now distinguish inventory from runtime authority, classify dormant/orphaned/superseded recovery access, detect correlated continuity drift, define a proportionate survivability-drill ladder, and interpret drill evidence without equating paperwork or telemetry with executable recovery.

Production, managed-EFB and real organizational validation remain **OPEN**.

## Next highest-value adjacent question

**PWA recovery-assurance evidence freshness, exception debt & false-confidence control.** The next bottleneck is how to prevent an old successful drill, waived dormant credential, or stale inventory attestation from remaining green indefinitely; how evidence expires; how exceptions accumulate/retire; and how dashboards avoid converting incomplete evidence into false assurance.