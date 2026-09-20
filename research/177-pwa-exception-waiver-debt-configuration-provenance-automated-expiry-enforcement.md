# 177 — PWA Exception/Waiver Debt, Configuration Provenance & Automated Expiry Enforcement

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A runtime/config state; Track B exception/degraded UX semantics; Track C destructive expiry/rollback validation; Track D privacy-bounded governance telemetry.
Dependencies: 173–176 distributed security-state convergence, fail-safe degradation, observability, SLO/brownout/recovery-proof governance.

## Why this study exists
176 established that a temporary security-affecting exception is a governed risk record, not an undocumented toggle. The next failure mode is exception debt: temporary relaxations survive their incident, get copied across regions, return through rollback/PITR, renew by default, or become an alternate authorization plane.

Central rule:

> **An exception is a bounded, provenance-bearing grant to deviate from a named invariant for a named scope and time. Expiry must remove future admission authority by default; renewal is a new decision, not extension by inertia. Historical evidence may remain without remaining executable authority.**

## Five-track balance
- **A Platform/Browser:** supplier. Cache/SW/IndexedDB possession, wall-clock state and old configuration are observations, not proof that an exception is current.
- **B UX/IA/Content:** owns clear user/operator semantics when an operation is paused because an exception expired or currentness cannot be established; does not expose internal waiver identifiers as user-facing jargon.
- **C Performance/Accessibility/Quality:** owns destructive tests for expiry, skew, rollback, region divergence, renewal races, reconnect and accessible recovery states.
- **D Search/Analytics:** bounded consumer. Exception metrics must not become durable per-user incident/identity dossiers.
- **E Security/Operations:** **bottleneck/owner**. Owns exception schema, authority, provenance, propagation, expiry/revocation, renewal, rollback resistance, debt retirement and audit separation.

## SOURCE
### NIST SP 800-53 Rev. 5 / Release 5.2.0
NIST's current control catalog remains risk-based and customizable, integrating access control, configuration/change control, assessment, audit, contingency and risk-management concerns. Release 5.2.0 was issued August 27, 2025.
Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

Transfer: configuration and control deviations require governance and assessment context; the catalog does not create a product-specific waiver duration or approval hierarchy for MintTap/LogMate.

### NIST SP 800-53A Rev. 5 / Release 5.2.0
NIST provides customizable assessment procedures aligned to risk tolerance and lifecycle assessment of security/privacy controls.
Source: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

Transfer: an exception cannot be considered safe merely because it exists in configuration; effectiveness and closure require evidence.

### NIST CSF 2.0 / SP 1302 / SP 1303
CSF 2.0 emphasizes GOVERN, and NIST's Tier/ERM guidance treats cybersecurity risk management as an organizational process subject to monitoring, evaluation and adjustment.
Sources:
- https://www.nist.gov/cyberframework
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-quick-start-guide-using-csf-tiers
- https://www.nist.gov/publications/nist-cybersecurity-framework-20-enterprise-risk-management-quick-start-guide

Transfer: temporary deviations are explicit risk-governance decisions; renewal-by-default is inconsistent with evidence-led monitoring and adjustment.

### OWASP — secrets/configuration lifecycle transfer
OWASP's Secrets Management guidance distinguishes rotation, revocation and expiration and recommends defined expiration where possible. OWASP Top 10:2025 Security Misconfiguration recommends repeatable/automated hardening and automated verification of configuration/settings.
Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/

Transfer: expiry/revocation should be enforceable lifecycle state rather than prose-only process. This does not mean a waiver is a secret; the transferable principle is bounded executable state with automated verification.

## SYNTHESIS — exception record is not the exception authority itself
Separate at least:
1. **risk/governance record** — why deviation was considered, owner, evidence, residual risk;
2. **authorized exception object** — machine-consumable bounded grant;
3. **distribution state** — which controlled enforcement domains have admitted the object;
4. **runtime enforcement state** — whether a request actually used the exception;
5. **historical audit evidence** — what existed/was used and when;
6. **debt/closure state** — remediation, expiry/revocation, reconciliation and retirement.

A ticket, wiki page, database row or signed object alone is not proof of runtime effect. Conversely, a runtime toggle without provenance is not an acceptable governed exception.

Persistent guards:
- `exception recorded ≠ exception authorized`;
- `exception authorized ≠ every region admitted it`;
- `exception distributed ≠ request used it`;
- `exception expired ≠ historical record deleted`;
- `historical record retained ≠ exception still executable`;
- `renewal requested ≠ renewal approved`;
- `same scope renewed ≠ same exception generation`;
- `PITR restored old exception ≠ exception reactivated`;
- `client clock says valid ≠ server authority says valid`;
- `cached exception present ≠ offline client may self-authorize consequence`;
- `exception registry available ≠ registry may bypass primary authorization policy`;
- `compensating control configured ≠ compensating control effective`;
- `exception count low ≠ exception debt low`.

## Generic exception object
Where an exception is technically enforceable, generic minimum semantics are:
- immutable exception identifier plus monotonic generation/version;
- named invariant/control being deviated from;
- exact capability/consequence scope and environment boundary;
- actor/tenant/resource scope only where necessary;
- authorized issuer/approver class and approval provenance;
- reason class and bounded evidence references, not unrestricted sensitive prose;
- `not-before` where needed and **hard `expires-at`**;
- explicit revocation state/path;
- compensating-control references and required validation state;
- current security/policy floor against which it was approved;
- creation/approval/renewal lineage;
- post-expiry reconciliation/closure requirement.

No universal duration, approver role or numeric threshold is asserted. Those require actual product/security/legal/BIA evidence.

## Automated expiry — deny future exception use by default
Expiry should be enforced in the consequence-bearing admission path, not only by a scheduler that later cleans up a flag.

Generic behavior:
1. admission checks current authoritative time/currentness and exception generation;
2. after hard expiry, the exception cannot authorize new consequence-bearing operations;
3. asynchronous cleanup may remove stale config later, but cleanup is not the security boundary;
4. queued work authored while the exception was valid is re-evaluated at commit/admission time unless product evidence proves a different safe transaction contract;
5. inability to establish current exception validity does not convert stale cached exception state into evergreen authority.

Clock handling is an implementation dependency. Generic research does not prescribe a particular time service. Browser/device wall clock is insufficient as the sole authority for remote consequence admission.

## Renewal is a new risk decision
Do not mutate `expires-at` indefinitely on the same object. Renewal should create a new generation linked to the prior exception and require current evidence, current approver authority, current policy floor, scope review, compensating-control review and a new hard expiry.

Metrics should expose repeated renewal/debt without making renewal automatic. Repeated renewal is a signal to remediate architecture/policy or explicitly accept a durable policy change through the normal policy process; it is not itself evidence that the exception is safe.

## Revocation and emergency closure
Revocation can precede scheduled expiry. Emergency revocation must advance a current security floor/generation so that region restore, stale caches and PITR cannot silently reactivate the grant. Revocation affects future executable authority; historical audit evidence remains subject to its own retention policy.

## Rollback/PITR resistance
A restored region may contain an exception that was valid at backup time but has since expired/revoked. Therefore:
- restore completion does not reopen exception-based admission;
- enforcement compares restored state against a surviving/current authority floor;
- stale exception generations are quarantined/reconciled before consequence-bearing traffic reopens;
- rollback of application/configuration must not roll back the independent expiry/revocation floor below the accepted current generation.

Exact persistence/replication design belongs to Software Engineering/provider validation.

## Multi-region propagation and partial failure
Exception creation, revocation and expiry are distributed security-state transitions. Track separately: authorization, publication, regional admission, actual enforcement and convergence evidence.

A region that cannot establish current exception state is `UNKNOWN`, not implicitly valid. A partial rollout must not be hidden behind a global `exception active` boolean.

## PWA / managed-iPad transfer
A PWA may cache UX/config projections, but a company iPad must not use a cached server exception as an offline bearer authorization credential for remote consequence-bearing work.

For LogMate-like long-offline operation:
- preserve unique local flight/logbook records and drafts;
- label remote submission/authority as pending when currentness cannot be established;
- on reconnect, obtain current server authority/exception generation before queued operations are admitted;
- an exception that expired while the iPad was offline stays expired even if old SW/IndexedDB state says otherwise;
- Service Worker update and exception reconciliation are separate;
- physical Safari/Home Screen/MDM behavior remains OPEN.

## Exception registry must not become a second authorization plane
The registry may supply a bounded exception object to the primary admission policy, but it must not independently answer broad `allow` questions outside that policy. Avoid generic `bypass=true`, wildcard scope, permanent no-expiry objects, and support/operator tooling that can mint effective exceptions without the normal approval boundary.

## Privacy/minimization
Exception records can accumulate incident narratives, identities, legal notes and operational history. Prefer bounded reason classes, evidence references and capability/scope/generation metadata. Separate privileged incident/legal material from routine runtime exception state. Do not make raw flight data, federation claims, tokens or stable device fingerprints routine exception dimensions.

Historical retention and deletion periods remain OPEN pending actual legal/security/audit requirements.

## Exception debt
Debt is not just count. Useful bounded signals include:
- active exceptions by invariant/capability/risk class;
- age and time-to-expiry distribution;
- renewal generation/count;
- scope breadth;
- compensating-control validation status;
- regions not converged/current;
- expired/revoked objects still observed in runtime/config stores;
- closure/remediation backlog.

Avoid stable per-user profiling unless necessary for the governed purpose.

## UX transfer — Track B
Users/operators should see task semantics: `saved locally`, `submission paused`, `temporary access no longer available`, `rechecking permission`, `review required`. They should not need to understand exception IDs, policy generations or federation internals. State must be accessible without color-only treatment and validated with screen reader/human evidence.

## MINTTAP DECISION — generic governance
1. Model exceptions as bounded provenance-bearing generations, never undocumented toggles.
2. Require hard expiry for technically enforceable temporary exceptions; no generic permanent exception is pre-approved.
3. Enforce expiry in the admission path; cleanup jobs are secondary hygiene.
4. Treat renewal as a new risk decision/generation, not silent date extension.
5. Preserve historical audit evidence separately from executable authority.
6. Make revocation/expiry rollback-resistant relative to restore/PITR and stale regional state.
7. Treat region/client currentness as explicit; `UNKNOWN` cannot silently become valid.
8. Keep the exception registry subordinate to primary authorization/admission policy.
9. Preserve unique offline PWA data while refusing stale exception authority for remote consequences.
10. Minimize exception telemetry/content and separate privileged incident/legal evidence.
11. Numeric durations, approver classes, retention, debt thresholds and product-specific permissible deviations remain OPEN.

## VALIDATION — 176-case destructive campaign
Families: no-expiry exception; scheduler failure after expiry; admission path ignores expiry; clock skew/time rollback; renewal without reapproval; concurrent renewal/revocation; approver authority revoked; wildcard scope; tenant/resource overbreadth; compensating-control failure; expired exception used by queued operation; region misses revoke; split-view active/expired; CDN/config cache stale; PITR resurrects expired exception; backup restore before current floor; app rollback; SW/IndexedDB stale projection; long-offline iPad; reconnect after multiple exception generations; client clock tampering; telemetry gap; exception registry outage; registry compromise; support impersonation; unauthorized minting; audit record deletion vs runtime state; privacy-heavy free text; cardinality explosion; Shared iPad/account switch; inaccessible status; screen-reader/human misunderstanding; repeated renewal normalization; debt dashboard green while scope broad; emergency revoke during provider outage; progressive recovery with stale region.

Generic campaign definition is PASS. Product/runtime/device/human execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** 176 supplies explicit exception governance and security-floor precedence; 173–175 supply distributed convergence, rollback and observability boundaries.
- **TRANSFER VALIDATION:** NIST CSF 2.0/ERM supports explicit monitored risk governance; SP 800-53/53A supports lifecycle control/assessment discipline.
- **TRANSFER VALIDATION:** OWASP lifecycle/configuration guidance supports automated expiration/revocation/verification as transferable engineering hygiene without treating it as a product-specific normative waiver schema.
- **CONTRADICTION:** `the cleanup cron will remove it eventually, so expiry is safe` is rejected.
- **CONTRADICTION:** `the same exception was approved last week, so extending it is administrative` is rejected.
- **CONTRADICTION:** `PITR restored the flag, therefore the exception is active again` is rejected.
- **CONTRADICTION:** `the offline PWA cached the exception, therefore queued consequences remain authorized` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH
OPEN: actual MintTap/LogMate permissible exception classes, invariants, approver hierarchy, legal/safety constraints, duration/renewal limits, policy/config technology, authoritative time/currentness mechanism, multi-region topology, provider restore behavior, runtime admission path, queue semantics, telemetry/retention, managed-iPad/Safari behavior and human/AT evidence.

DEPENDENCY — Software Engineering: implement signed/authenticated provenance as appropriate to the real threat model, monotonic generation/current-floor checks, admission-path expiry/revocation, safe renewal, region convergence, rollback/PITR resistance, queue re-admission and runtime evidence. Do not infer a cryptographic format from this generic requirement.

DEPENDENCY — Design Studio: validate accessible degraded/expired/recheck/review semantics. Current Web Design status remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human evidence remain OPEN.

CHANGE WATCH: NIST controls/CSF guidance, OWASP guidance, provider configuration/restore behavior and Safari/iPadOS PWA behavior.

## Gate
**177 PASS (generic).** Web Manager can now model temporary exceptions as bounded provenance-bearing generations; separate risk record, executable grant, distribution, enforcement and audit; require admission-path expiry and new-decision renewal; prevent rollback/PITR/cached-client resurrection; measure exception debt without making the registry a privacy dossier; and preserve offline-first local utility without converting stale exceptions into authority.

Next adjacent bottleneck: **PWA exception-compensating-control assurance, break-glass authority & two-person/independent approval boundaries** — determine how a temporary deviation remains bounded when its compensating control fails, when emergency break-glass is justified, how approval independence should be modeled without inventing product roles, and how offline/partial-region conditions avoid turning emergency authority into a permanent bypass.