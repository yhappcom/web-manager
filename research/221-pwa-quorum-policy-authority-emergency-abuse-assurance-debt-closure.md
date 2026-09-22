# 221 — PWA Quorum-Policy Authority, Emergency-Mode Abuse Resistance & Assurance-Debt Closure

Status: **PASS (generic) / PRODUCT + AUTHORITY + QUORUM-POLICY + EMERGENCY-OPERATIONS + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A offline/runtime mechanics; Track B emergency/recovery UX; Track C destructive validation; Track D debt/assurance telemetry.  
Dependencies: 117–137, 171–220 and prior authority/currentness/recovery/evidence work.

## Problem
220 established that quorum is claim-specific policy and emergency reduced-assurance operation is a bounded capability mode, not a numerical quorum bypass. The adjacent risk is governance recursion: during an incident, the same actor that cannot satisfy the current assurance rule may try to weaken that rule, activate the weakened rule, and then use the newly-created authority to declare itself normal.

Central rule: **an assurance requirement must not be weakened merely by the actor or evidence path whose inability to satisfy that requirement is the reason for weakening it. Emergency activation, emergency-policy authorship, execution and closure are distinct authorities. Normal service is not restored until temporary authority and assurance debt are demonstrably retired.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Cached policy, offline clocks, Service Worker/update state and reconnect timing affect activation/expiry evidence but do not author emergency authority.
- **B UX/IA/Content:** very high dependency pressure. Owns comprehensible `NORMAL`, `DEGRADED`, `EMERGENCY-RESTRICTED`, `RECOVERY-PENDING`, and `DATA-PRESERVED / SYNC-BLOCKED` states while consuming Design Studio evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **520 → 528 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures emergency duration, activation reason, debt age, residual temporary authority and closure evidence; telemetry cannot authorize entry or closure.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns quorum-policy authority, separation of emergency roles, anti-self-authorization, capability ceilings, expiry/revocation and closure proof.

## SOURCE

### NIST CSF 2.0 — cybersecurity risk decisions require governance
NIST CSF 2.0 adds the Govern function and treats cybersecurity risk strategy, expectations, policy, roles, responsibilities and authorities as organizational governance concerns rather than purely technical runtime decisions.

Sources:
- https://doi.org/10.6028/NIST.CSWP.29
- https://www.nist.gov/cyberframework

**TRANSFER VALIDATION:** CSF 2.0 does not prescribe MintTap quorum or emergency roles. It supports the bounded conclusion that risk acceptance and authority-changing policy belong to explicit governance rather than being inferred from an outage.

### NIST SP 800-61 Rev.3 — recovery has authorization, criteria and explicit return-to-normal work
SP 800-61 Rev.3, final April 2025, integrates incident response with CSF 2.0. Its recovery guidance calls for plans to identify recovery actions and required authorizations; recovery actions are selected/scoped/prioritized; restored assets are checked before production use; normal operating status is confirmed; and the end of recovery is declared based on criteria with incident documentation completed.

Sources:
- https://doi.org/10.6028/NIST.SP.800-61r3
- https://csrc.nist.gov/pubs/sp/800/61/r3/final

**TRANSFER VALIDATION:** this is strong precedent for separating emergency action from recovery closure. It does not define MintTap's exact closure quorum or capability set.

### NIST SP 800-53 Rev.5 / SP 800-53A Rev.5 — emergency/temporary authority has lifecycle and assessment evidence
AC-2(2) provides for automated removal or disabling of temporary and emergency accounts after an organization-defined period. SP 800-53A supplies assessment objects including configuration, system-generated account lists and audit records.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** emergency accounts are not identical to MintTap reduced-assurance modes. The reusable principle is that temporary emergency authority requires explicit lifecycle termination and evidence; it should not remain indefinitely because an administrator forgets to close it.

### CISA TIC 3.0 cloud guidance — emergency administration uses least privilege, separation and extensive logging
CISA guidance recommends least privilege for administrative functions, separation of duties so one account does not hold complete cloud administration, carefully protected break-glass accounts, consideration of multiple users for enabling access, and extensive logging/auditing.

Source:
- https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

**TRANSFER VALIDATION:** this is cloud administrative guidance, not a MintTap PWA protocol. It is useful precedent for separation, bounded emergency access and evidence capture.

## SYNTHESIS 1 — policy authorship, activation, execution and closure are different authorities
Separate at least four roles/capabilities:
1. **policy author** — defines quorum/diversity/emergency capability ceilings;
2. **activator** — declares that pre-authorized emergency entry conditions are met;
3. **executor** — performs only capabilities admitted by that mode;
4. **closure authority/assessor** — verifies recovery and retires temporary authority/debt.

One human may hold more than one role in a small organization, but the security model must not silently collapse the roles. Where independence is required, it must be explicit and evidence-backed.

`can activate ≠ can rewrite policy`; `can execute ≠ can expand capability`; `can restore service ≠ can declare assurance restored`.

## SYNTHESIS 2 — quorum policy cannot self-weaken through the failed quorum
Suppose Q12 requires independent corroboration from A+B. If B is unavailable, A cannot use the fact that Q12 is unsatisfied to author Q13=`A alone is enough`, activate Q13, and then claim Q13's own rule proves the change valid. That is recursive self-authorization.

A legitimate emergency transition must derive from authority that was already valid independently of the missing assurance: e.g. pre-authorized bounded emergency policy, separately governed recovery authority, or another authenticated authority lineage whose validity does not depend on the failed condition.

`cannot satisfy Q ≠ may rewrite Q`; `new policy signed ≠ signer authorized to lower its own acceptance rule`.

## SYNTHESIS 3 — emergency authority has a capability ceiling, not an editable blank check
Emergency mode should identify an immutable or separately governed maximum capability envelope. Incident operators may choose a subset within that envelope; they must not add new authority merely because the incident is severe.

For an offline-first PWA, a plausible generic ceiling may preserve local record creation/read-only trusted data while keeping authority changes, destructive reconciliation, trust reset and high-consequence remote mutation prohibited. Exact product capabilities remain OPEN.

`emergency declared ≠ all controls optional`; `availability pressure ≠ authority expansion`.

## SYNTHESIS 4 — expiry is necessary but not sufficient
Time-bounded emergency authority reduces persistence risk, but wall-clock expiry alone is weak when clocks, partitions, cached policy, rollback or long-offline devices exist. Bind temporary authority to authenticated policy/security generation and revocation/termination lineage where architecture permits.

After expiry, queued work created during the emergency is not grandfathered automatically. It is re-admitted against current policy.

`queued while valid ≠ replay valid later`; `offline during expiry ≠ expiry suspended`; `clock says expired ≠ every enforcement point has extinguished authority`.

## SYNTHESIS 5 — assurance debt is an explicit evidence object
Emergency operation creates debt even if no known harmful action occurred. Track at least:
- missing/relaxed assurance and reason;
- affected capability, region/cohort and time/generation window;
- temporary credentials/policies/accounts/waivers introduced;
- actions executed and queued under reduced assurance;
- contradictions/unknown tails;
- compensating controls and monitoring;
- remediation/validation owner;
- closure criteria and evidence.

Do not reduce debt to a ticket marked `resolved`.

`incident closed ≠ assurance debt closed`; `service green ≠ temporary authority extinct`.

## SYNTHESIS 6 — closure requires positive recovery evidence and negative temporary-authority evidence
Return to NORMAL should require evidence that normal prerequisites are restored **and** temporary/stale paths no longer authorize consequence-bearing work. A generic closure bundle should include:
1. current quorum/diversity and policy/evaluator generation;
2. contradiction/unknown-tail disposition;
3. restored enforcement-set convergence;
4. disabled/revoked/expired emergency accounts, waivers, keys or modes;
5. negative tests showing retired emergency/predecessor authority is rejected;
6. review/re-admission of queued emergency operations;
7. PITR/recovery rejoin evidence;
8. incident/recovery record and residual-risk decision.

`positive normal-path PASS ≠ emergency-path extinction PASS`; `emergency flag false ≠ emergency credential unusable`.

## SYNTHESIS 7 — closure authority cannot erase evidence debt by declaration
A closure approver may accept documented residual risk, but cannot convert UNKNOWN evidence into historical PASS. If a period cannot be independently reconstructed, retain that uncertainty in the incident/evidence record.

`risk accepted ≠ evidence recovered`; `closure approved ≠ missing history reconstructed`.

## SYNTHESIS 8 — emergency mode persistence itself is a security signal
Long-running emergency state increases exposure to normalization of deviance. Define escalation/change-watch thresholds for duration, repeated activation, widening scope, failed closure tests and reactivation shortly after closure. These signals trigger governance review; they do not themselves change authority.

`emergency lasted longer ≠ emergency automatically broadens`; `frequent emergency use ≠ make exception baseline silently`.

## SYNTHESIS 9 — rollback and recovery must not resurrect closed emergency authority
PITR or regional rollback may restore rows/configuration that say emergency mode is active. Current security-generation/termination evidence must dominate stale restored state. A restored environment remains behind a rejoin gate until it proves current policy and rejection of retired emergency authority.

`restored emergency row ≠ emergency re-authorized`; `backup contains credential ≠ credential current`.

## SYNTHESIS 10 — long-offline PWA preserves data but not expired emergency sovereignty
A LogMate-like iPad can remain offline across emergency activation and closure. On reconnect, preserve unique flight/logbook data first. Cached emergency policy, Service Worker state, local clock or old credential is historical context, not current authority. Re-acquire current authenticated policy/security generation, migrate schema/evaluator as required, and re-admit queued consequence-bearing work.

`device missed closure ≠ emergency remains valid on device`; `local unique data preserved ≠ queued remote mutation authorized`.

## MINTTAP DECISION / DIRECTION
1. Model quorum-policy authorship, emergency activation, execution and closure as separate authorities even if an eventual small-team implementation maps multiple roles to one person.
2. Prohibit recursive self-authorization: failure to satisfy a quorum never by itself authorizes weakening that quorum.
3. Treat emergency operation as a pre-authorized capability ceiling with explicit scope, termination and evidence obligations.
4. Treat emergency operation as creating **assurance debt** that survives service restoration until closure evidence is complete.
5. Require both positive restored-assurance evidence and negative extinction evidence for temporary authority before declaring NORMAL.
6. Preserve uncertainty rather than rewriting it as PASS during risk acceptance or incident closure.
7. Preserve unique offline PWA data while re-admitting consequence-bearing work under current authority after emergency closure.

These are generic directions, not claims about current MintTap/LogMate architecture.

## OPEN / DEPENDENCY
- Exact MintTap/LogMate policy-author/activator/executor/closure roles: **OPEN**.
- Exact quorum policy, emergency capability ceiling, maximum duration and closure criteria: **OPEN**.
- Actual provider IAM/break-glass/recovery topology and audit independence: **OPEN**.
- Exact iPadOS/WebKit/MDM/offline clock/background/storage behavior: **Track A + Software Engineering runtime dependency**.
- Emergency/degraded operator and pilot UX: **Track B consuming Design Studio; human/accessibility validation OPEN**.
- Legal/aviation/safety requirements for emergency/offline EFB operation: **OPEN**.

## Track C destructive campaign — 520 → 528 defined cases
Add:
1. **Recursive self-weakening:** sole surviving collector changes `2 independent` to `1` and uses its own vote to validate the change.
2. **Activator becomes author:** incident commander may activate pre-authorized emergency mode but edits its capability ceiling to permit authority reset.
3. **Executor broadens scope:** regional operator copies a region-scoped emergency credential into global provider administration.
4. **Expired queue replay:** mutation queued during valid emergency mode executes after closure without current re-admission.
5. **UI-only closure:** dashboard flag returns NORMAL while break-glass credential and provider-console path still work.
6. **PITR resurrection:** restored policy database reactivates an already-closed emergency mode/credential.
7. **Debt laundering:** incident is closed while one contradictory witness and an unreachable enforcement tail remain recorded as ordinary green.
8. **Long-offline iPad misses full emergency lifecycle:** unique local data survives, but cached emergency authority cannot resume consequence-bearing sync after reconnect.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** offline clocks/cache/Service Worker state can explain stale emergency state but cannot prolong authority.
- **Track B:** emergency/recovery UX must expose restricted capability and pending work without presenting a user-controlled security bypass.
- **Track C:** extinction, rollback, queued-work and role-separation claims require executable tests; reading is not runtime PASS.
- **Track D:** analytics can expose duration/debt/repeated activation but cannot close debt or grant emergency authority.
- **Design Studio:** Web remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/iPadOS/EFB and canonical-product runtime remain OPEN.

## Persistent guards added
`can activate ≠ can rewrite policy`; `can execute ≠ can expand capability`; `can restore service ≠ can declare assurance restored`; `cannot satisfy Q ≠ may rewrite Q`; `new policy signed ≠ signer authorized to lower its own acceptance rule`; `emergency declared ≠ all controls optional`; `queued while valid ≠ replay valid later`; `offline during expiry ≠ expiry suspended`; `incident closed ≠ assurance debt closed`; `service green ≠ temporary authority extinct`; `positive normal-path PASS ≠ emergency-path extinction PASS`; `risk accepted ≠ evidence recovered`; `restored emergency row ≠ emergency re-authorized`; `device missed closure ≠ emergency remains valid on device`.

## Gate result
**221 PASS (generic).** The knowledge gate closes because policy-authority separation, anti-self-authorization, emergency capability ceilings, expiry semantics, assurance-debt modeling, positive/negative closure evidence, rollback resistance and long-offline PWA consequences now have explicit evidence boundaries and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**222 — assurance-debt ledger integrity, closure-evidence independence & post-emergency regression governance**: determine how assurance debt itself remains complete/tamper-evident across incident pressure, how closure evidence avoids being produced solely by the same compromised/exception authority, how unresolved debt blocks only the capabilities it actually affects, and how repeated emergency activation becomes a corrective-control/regression signal without silently normalizing reduced assurance.