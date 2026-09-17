# 119 — PWA Post-Incident Trust Normalization & Residual-Risk Acceptance

Status: **PASS (generic) / PRODUCT RUNTIME + MANAGED-IPAD + RISK-OWNER VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 113 hostile-origin compromise scope; 114 compromise-era integrity/provenance; 116 active-compromise containment; 117 partial/offline fleet containment; 118 containment rollback/emergency-gate lifecycle; Track A browser/session/Service Worker mechanics; Track C adversarial validation; Software Engineering for exact implementation evidence.

## Purpose

118 established that ending containment is a forward transition into a new trust baseline rather than restoration of an old configuration snapshot. The adjacent problem is governance after that transition: when may the organization call the new state normal, which remaining uncertainties are acceptable residual risk, which are still unfinished incident work, and how can long-offline clients or unverifiable data remain explicitly unknown without either blocking the entire fleet forever or being silently promoted to trusted?

This study defines that generic boundary. It does not claim that MintTap or LogMate currently implements any described control, inventory, risk register, authorization gate or managed-iPad behavior.

## 1. Five-track balance

- **A Platform/Browser:** dependency supplier. Offline browser state, Service Worker generations, local storage and session state do not become current because an organizational incident is declared closed.
- **B UX/IA/Content:** consumes durable post-incident states such as `normal`, `restricted`, `re-entry required`, `unreconciled`, `unknown`, and `retired`; user-facing language must not overstate certainty.
- **C Quality:** owns negative controls, stale/unknown-client tests, re-entry regression and evidence that accepted risk does not bypass technical invariants.
- **D Discovery/Analytics:** owns observation/denominator discipline. Telemetry can monitor residual risk but cannot silently convert absence of observations into proof of fleet convergence.
- **E Architecture/Security/Operations:** highest-risk owner. Defines baseline normalization, residual-risk records, acceptance authority, review triggers and closure boundaries.

E remains the bottleneck; A supplies mechanics and C supplies proof. D supplies monitoring evidence without becoming an authorization source.

## 2. SOURCE — incident response belongs inside ongoing cybersecurity risk management

NIST SP 800-61 Rev. 3, finalized April 2025, explicitly integrates incident response into the NIST Cybersecurity Framework 2.0 risk-management lifecycle rather than treating recovery as an isolated cleanup phase.

Sources checked 2026-09-18:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

NIST CSF 2.0, published February 2024, frames cybersecurity outcomes across Govern, Identify, Protect, Detect, Respond and Recover and emphasizes governance of cybersecurity as enterprise risk.

Sources:
- https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- https://www.nist.gov/cyberframework

**SYNTHESIS:** incident closure is not the end of risk management. The recovered system becomes the next current risk posture, which must remain observable and governable.

Guards:
- `incident closed ≠ residual risk disappeared`;
- `service normalized ≠ uncertainty eliminated`;
- `recovery completed ≠ risk-management lifecycle ended`.

## 3. SOURCE — acceptance is an intentional risk response, not a synonym for unfinished work

NIST's current risk-response glossary defines risk response as accepting, avoiding, mitigating, sharing or transferring risk. NIST IR 8286B Update 1 (February 2025) describes selecting responses in light of enterprise objectives and recording risk priorities/response information in cybersecurity risk registers. It states that residual risks remain part of risk aggregation, correlation and communication rather than disappearing after a response decision.

Sources checked 2026-09-18:
- https://csrc.nist.gov/glossary/term/risk_response
- https://csrc.nist.gov/pubs/ir/8286/b/upd1/final
- https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8286B-upd1.pdf

NIST IR 8286 Rev. 1 (December 2025) reinforces that senior leaders need a clear view of cybersecurity risk posture and that system/organization risk decisions should be informed by enterprise objectives.

Source:
- https://csrc.nist.gov/pubs/ir/8286/r1/final

**SYNTHESIS:** `accepted` must represent an intentional, attributable response to a defined risk. A missing fix, missing test, unknown owner or forgotten emergency control is not transformed into accepted risk by age or by incident closure.

Guards:
- `known unresolved item ≠ accepted risk`;
- `no planned fix ≠ risk accepted`;
- `incident ticket closed ≠ risk owner accepted residual exposure`;
- `risk accepted ≠ risk erased from monitoring`.

## 4. Distinguish four post-incident classes

A useful normalization model separates at least:

1. **Resolved/validated** — the relevant trust/security invariant has evidence sufficient for its defined gate.
2. **Accepted residual risk** — a specific remaining risk is understood well enough for an authorized owner to accept it within applicable appetite/tolerance and obligations, with review triggers.
3. **Open remediation/validation work** — the organization intends to reduce or verify the risk and has not completed that work.
4. **Unknown/unclassifiable state** — evidence is insufficient to estimate or classify the client/data/operation confidently; this is not automatically equivalent to either compromised or safe.

**MINTTAP DIRECTION:** preserve these classes explicitly in future incident/risk governance rather than using one `closed/open` flag.

Guards:
- `unknown ≠ accepted`;
- `unknown ≠ known compromised`;
- `unknown ≠ safe by default`;
- `mitigation planned ≠ mitigation completed`;
- `validation pending ≠ residual risk formally accepted`.

## 5. A new normal baseline is an explicit current-state contract

The normalized baseline should describe the authority and compatibility state that is allowed *now*, not merely document that emergency controls were removed. Depending on future architecture, this can include:
- current release/client generation eligible for remote authority;
- current trust/key/credential generations and explicitly retired generations;
- current API/schema/protocol generations and capability gates;
- current Service Worker/update expectations;
- current session/authentication/re-entry requirements;
- local data classes that may remain readable/exportable while remote mutation is restricted;
- outbox/replay reconciliation requirements;
- emergency controls that are retired versus deliberately converted into permanent controls;
- unresolved client/data populations and their fail-closed behavior.

**SYNTHESIS:** normalization is a versioned trust contract, not the absence of an incident banner.

Guards:
- `emergency controls removed ≠ baseline defined`;
- `baseline documented ≠ baseline enforced`;
- `baseline enforced for observed clients ≠ unknown offline clients converged`.

## 6. Risk acceptance needs a decision object, not a vague statement

A defensible residual-risk record should be capable of answering, proportionately to risk:
- what exact risk scenario remains;
- what assets/users/operations are in scope;
- what evidence supports likelihood/impact and what uncertainty remains;
- which mitigations are already in force;
- why further mitigation/avoidance/transfer is not currently selected;
- who owns the risk and who has authority to accept it;
- what duration/review date or reconsideration triggers apply;
- what monitoring or negative canaries remain;
- what would invalidate the acceptance decision;
- what regulatory, contractual, safety or policy constraints limit acceptance.

NIST IR 8286A Rev. 1 (December 2025) emphasizes documenting risk scenarios, likelihood/impact and risk appetite/tolerance context in risk registers. NIST IR 8286C Rev. 1 describes integrating cybersecurity risk-register information into governance oversight and the enterprise risk portfolio.

Sources:
- https://csrc.nist.gov/pubs/ir/8286/a/r1/final
- https://csrc.nist.gov/pubs/ir/8286/c/r1/final

**TRANSFER VALIDATION:** exact MintTap approval roles and thresholds are organizational facts and remain OPEN. Do not invent a CISO, board, quorum or numeric threshold.

Guard: `risk record exists ≠ correct authority accepted it`.

## 7. Acceptance must not authorize a known-invalid technical state

Risk acceptance is governance over exposure; it should not be used as a technical bypass that makes revoked credentials, obsolete trust roots, hostile workers or unreconciled operations valid again.

Example: an organization might accept the business risk that some long-offline devices remain unobserved for a period, while still requiring those devices to pass the current fail-closed re-entry gate when they return. The accepted risk is the uncertainty/availability/support exposure, not permission for stale authority to mutate remote state.

**SYNTHESIS:** preserve security invariants while accepting bounded uncertainty around them.

Guards:
- `residual risk accepted ≠ revoked credential authorized`;
- `fleet uncertainty accepted ≠ stale client remote mutation allowed`;
- `availability risk accepted ≠ anti-rollback disabled`;
- `business accepts uncertainty ≠ protocol should fail open`.

## 8. Long-offline EFB clients can remain unknown after organizational normalization

A company iPad can remain offline through compromise, containment, rollback and organizational closure. Its absence from telemetry does not prove its state. The central service can nevertheless normalize for current clients while preserving an explicit unknown population whose next remote interaction must satisfy current re-entry policy.

A generic state model is:
`known-current` / `known-restricted` / `known-revoked` / `unknown-offline` / `retired-with-evidence`.

Exact fleet identity and inventory architecture are OPEN.

Guards:
- `organization normalized ≠ every device normalized`;
- `unknown-offline client ≠ blocker to all current clients if remote authority remains fail-closed`;
- `device absent from telemetry ≠ retired`;
- `risk accepted for unknown population ≠ unknown device pre-authorized on return`.

## 9. Compromise-era data may remain useful while integrity remains uncertain

Studies 113–115 established that same-origin compromise can make local data integrity unverifiable and that indiscriminate wipe may destroy irreplaceable flight records. Post-incident normalization therefore must allow a durable state in which data is preserved for read/export/reconciliation while its provenance is unresolved.

Possible generic classifications:
- verified against independent evidence;
- reconciled by explicit user/operator review;
- preserved but unverified;
- known conflicting;
- rejected/quarantined;
- authoritative remote acknowledgement available.

Exact LogMate record model is OPEN.

Guards:
- `data preserved ≠ data trusted`;
- `data useful for recovery ≠ data safe for automatic replay`;
- `risk accepted around unverifiable data ≠ provenance magically established`.

## 10. Temporary recovery assumptions must not silently become permanent policy

Incident pressure can produce assumptions such as:
- a temporary allowlist is “good enough”;
- a support-assisted identity path is trusted;
- a compatibility bridge remains necessary;
- an emergency export path is exempt from normal validation;
- additional telemetry is retained indefinitely;
- a stale API remains writable for “just a little longer.”

118 requires emergency-control retirement. 119 adds a normalization question for every survivor: is it intentionally promoted to permanent policy, with ordinary owner/threat/privacy/validation review, or is it unresolved incident debt?

Guards:
- `survived incident closure ≠ approved permanent architecture`;
- `temporary exception repeatedly renewed ≠ normalized control`;
- `useful during recovery ≠ justified during steady state`.

## 11. Acceptance has a time dimension and reconsideration triggers

NIST SP 1303 describes integration of cybersecurity risk monitoring, evaluation and adjustment into enterprise risk management. NIST IR 8286B similarly treats response and monitoring as ongoing risk activities.

Sources:
- https://csrc.nist.gov/pubs/sp/1303/final
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-enterprise-risk-management-quick-start-guide

A residual-risk decision should therefore be revisited when material assumptions change. Potential triggers include:
- a previously unknown client reconnects;
- new evidence changes compromise scope;
- a new browser/OS behavior changes the control boundary;
- a key/API/schema generation is retired;
- monitoring detects a negative canary failure;
- business impact or data criticality changes;
- a temporary mitigation becomes unavailable;
- regulatory/contractual requirements change.

No universal review interval is invented.

Guards:
- `accepted once ≠ accepted forever`;
- `review date reached ≠ automatic re-acceptance`;
- `no new incident ≠ assumptions unchanged`.

## 12. Track D transfer — monitoring cannot manufacture certainty

Post-incident telemetry can track current-generation accepts, stale-generation denies, re-entry outcomes, reconciliation results and reappearance of unknown clients. But telemetry sees what reports. Long-offline devices remain denominator uncertainty unless a separate authoritative inventory/decommission source exists.

**TRANSFER VALIDATION:** monitoring informs review; it is not the authorization boundary.

Guards:
- `zero stale events ≠ zero stale clients`;
- `no alert ≠ residual risk retired`;
- `telemetry coverage high ≠ fleet denominator complete`.

Privacy minimization from 114–118 remains in force; incident monitoring is not authority for indefinite collection of flight-record payloads or unrelated user data.

## 13. Track B transfer — UX must communicate capability, not organizational paperwork

A user/operator should receive actionable state rather than internal labels such as `risk accepted`. Relevant UX distinctions can include:
- records available locally;
- sync temporarily restricted;
- update/re-authentication required;
- pending records preserved but not yet reconciled;
- some records require review;
- normal remote operation restored.

**SYNTHESIS:** an internal risk-acceptance decision does not make uncertainty disappear from a user workflow when that uncertainty materially affects capability or data confidence.

Guards:
- `risk accepted internally ≠ user impact absent`;
- `incident closed internally ≠ “everything is normal” message accurate for every device`.

## 14. Track C validation campaign

Future exact implementation evidence should cover at least:
1. current clean client after normalization;
2. revoked credential remains rejected after normalization;
3. stale trust generation remains rejected;
4. stale API generation remains blocked for mutation;
5. current read succeeds while prohibited destructive action fails;
6. unknown-offline client reconnects after incident closure;
7. unknown client cannot inherit old session authority;
8. unknown client can preserve/export local records where policy permits;
9. current update/re-auth path restores intended authority;
10. stale Service Worker cannot bypass server-side generation gate;
11. compromise-era outbox remains suppressed until reconciliation;
12. reconciled operation is admitted once with expected semantics;
13. rejected operation remains quarantined;
14. preserved-unverified data is not labeled verified;
15. risk acceptance record does not alter authorization decision code path;
16. emergency account remains retired;
17. temporary feature flag remains retired or is explicitly promoted through ordinary governance;
18. expired risk acceptance triggers review rather than automatic renewal;
19. material new evidence triggers reassessment;
20. negative canary catches stale-client acceptance regression;
21. monitoring outage does not cause fail-open authorization;
22. zero observed stale clients does not automatically close unknown inventory;
23. retired device requires retirement evidence;
24. rollback to old configuration does not revive old trust state;
25. browser storage survives normal update without losing authoritative local records;
26. recovery path preserves local data while executable state is replaced;
27. accessibility of restricted/re-entry/reconciliation states;
28. enlarged text/reflow/localization do not hide critical restriction state;
29. privacy review confirms residual-risk telemetry is minimized;
30. managed-iPad client offline through entire incident rejoins through current gate;
31. incident closure report can distinguish accepted risk from open remediation;
32. risk owner/approval evidence is attributable;
33. acceptance review trigger is observable/auditable;
34. current baseline version can be reconstructed from configuration/evidence;
35. a deliberately permanent former-emergency control receives ordinary architecture/security ownership rather than remaining anonymous incident debt.

No product PASS exists until exact runtime and organizational evidence is captured.

## 15. Operational normalization model

Use the generic sequence:

`RECOVER → VERIFY CURRENT ENFORCEMENT → DEFINE NEW BASELINE → CLASSIFY RESIDUAL ITEMS → KEEP OPEN WORK OPEN → FORMALLY ACCEPT ONLY ELIGIBLE RESIDUAL RISK → RETIRE/PROMOTE EMERGENCY CONTROLS → MONITOR CURRENT + UNKNOWN POPULATIONS → REASSESS ON TRIGGER`.

The key discipline is that each transition preserves uncertainty instead of laundering it into `normal`.

## 16. EFB / LogMate-like judgment

For an offline-first flight-log PWA, the safest generic post-incident posture is not necessarily “all devices clean before service resumes.” That may be impossible to prove for devices that remain offline. A stronger architecture can normalize central service for current verified clients while retaining fail-closed remote authority for unknown/stale clients and preserving their local records for later recovery/reconciliation.

This requires exact product architecture to validate. In particular, direct unattended device-to-device synchronization, background execution, managed-iPad reachability, storage persistence and re-entry behavior remain OPEN and must not be inferred from generic web standards.

## 17. OPEN

Exact product/organizational evidence remains required for:
- actual post-incident baseline representation;
- risk appetite/tolerance and authorized risk-owner roles;
- risk register/decision-record process;
- client/fleet identity and authoritative denominator;
- device retirement/decommission evidence;
- auth/session/token and trust-generation architecture;
- API/schema/protocol capability gates;
- Service Worker update/re-entry behavior;
- local record provenance/integrity model;
- outbox/operation IDs/reconciliation semantics;
- emergency-control inventory and permanent-promotion process;
- telemetry coverage/privacy/retention;
- managed-iPad OS/WebKit/MDM behavior;
- legal, contractual, aviation or safety constraints that may make some risks non-acceptable regardless of technical preference.

## 18. CHANGE WATCH

- NIST CSF/IR 8286 guidance can evolve; sources were checked 2026-09-18.
- Browser/WebKit/Chromium storage, Service Worker and installed-web-app behavior remains version-sensitive.
- Managed-iPad MDM and enterprise policy is product/organization-specific and requires current evidence.
- Authentication/session provider semantics and deployment/control-plane behavior are implementation-sensitive.

## 19. VALIDATION / gate result

**PASS (generic).** The Web Manager can now distinguish a new post-incident trust baseline from mere emergency-control removal; distinguish accepted residual risk from unfinished remediation and unknown state; preserve fail-closed authority for long-offline clients while allowing central normalization; keep unverifiable local data useful without falsely promoting integrity; and define risk acceptance as an attributable, reviewable governance decision rather than a technical bypass.

Production, managed-iPad, organization-specific risk acceptance, legal/safety and incident-drill validation remain OPEN.

## 20. Next adjacent bottleneck

The highest-value adjacent generic boundary is **post-incident learning → control-baseline change governance**: decide when a lesson learned should alter permanent architecture/control requirements, how to avoid overfitting the entire platform to one incident, how to supersede old assumptions/ADRs without rewriting history, and how to verify that corrective actions actually reduce recurrence risk rather than merely produce documentation.