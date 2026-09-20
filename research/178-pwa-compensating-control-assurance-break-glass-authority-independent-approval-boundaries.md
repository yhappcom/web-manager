# 178 — PWA Compensating-Control Assurance, Break-Glass Authority & Independent Approval Boundaries

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A runtime/currentness mechanics; Track B emergency/degraded UX semantics; Track C destructive assurance and recovery validation; Track D privacy-bounded emergency-use telemetry.
Dependencies: 173–177 distributed security-state convergence, fail-safe degradation, recovery proof, exception provenance/expiry/debt.

## Why this study exists
177 made temporary exceptions bounded, provenance-bearing generations with admission-path expiry. The adjacent failure is subtler: an exception can remain formally valid while the compensating control that justified it has failed, or an emergency path can become a standing bypass because one operator can create, approve, exercise and conceal it.

Central rule:

> **An exception is not safe merely because its compensating control was configured at approval time. Consequence-bearing use requires the control assurance state demanded by the exception contract. Break-glass authority is a separately bounded emergency capability, not an administrator-shaped universal bypass; independence must prevent one failure/actor from silently minting, exercising and erasing exceptional authority.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Browser cache, Service Worker, IndexedDB, device clock and connectivity state can report observations but cannot establish current break-glass or compensating-control authority.
- **B UX/IA/Content:** owns comprehensible semantics such as `emergency access in use`, `submission paused`, `saved locally`, `additional approval required`, `emergency access ended`, without exposing sensitive internal control topology.
- **C Performance/Accessibility/Quality:** owns destructive validation of control failure, approval races, partial-region state, expiry, PITR, reconnect, logging failure, accessibility and human comprehension.
- **D Search/Analytics:** bounded consumer. Emergency-use metrics are security/operations evidence, not acquisition analytics; avoid durable per-person privileged-activity profiles unless governed necessity exists.
- **E Security/Operations:** **bottleneck/owner**. Owns exception assurance contract, break-glass scope, independent approval/separation, emergency activation, expiry/revocation, post-use review, evidence independence and rollback resistance.

## SOURCE
### NIST SP 800-53 Rev. 5 / current control catalog
NIST AC-5 requires organizations to identify duties requiring separation and define access authorizations supporting that separation. Its discussion states that separation of duties reduces abuse of authorized privileges and risk of malevolent activity without collusion. AC-6 requires least privilege for users and processes. NIST also distinguishes control functionality from assurance — confidence that the capability actually provides the intended protection.
Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

Transfer: independence and least privilege are risk controls, not a universal mandate that every emergency action needs exactly two named humans. The concrete duties, quorum and exceptions require product/risk evidence.

### CISA — emergency administrative access transfer
CISA TIC 3.0 cloud guidance says agencies should strongly apply least privilege to administrative functions, consider separation of duties so no single account has complete administrative access, and consider emergency `Break Glass` global-administrator accounts. It further recommends strong protection, possible coordination of multiple users to enable access, extensive logging/auditing, anomalous-activity detection, and consideration of whether administrators can disable alerts/logs.
Source: https://www.cisa.gov/sites/default/files/2023-05/tic_3.0_cloud_use_case_508c.pdf

Transfer: emergency access can be legitimate, but its custody, enablement, observation and evidence path should not collapse into the same unilateral authority. This federal-cloud guidance is evidence for a design principle, not a product-specific MintTap/LogMate role model.

### OWASP Top 10:2025 — Broken Access Control
OWASP continues to place Broken Access Control at A01 and recommends deny-by-default, reusable server-side access-control mechanisms, business-limit enforcement, logging of access-control failures and testing access control in unit/integration coverage.
Source: https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

Transfer: exceptional access remains access control. A UI-only emergency switch, client-side bypass or untested alternate route is not acceptable simply because it is called break-glass.

## SYNTHESIS — compensating control has an assurance lifecycle
Separate:
1. **control requirement** — what risk reduction the exception relies on;
2. **control implementation** — concrete mechanism/provider/configuration;
3. **control observation** — telemetry/test/attestation showing state;
4. **control assurance decision** — whether evidence satisfies the exception's required assurance at this consequence/time;
5. **exception admission** — whether the exceptional path may actually authorize the request;
6. **post-use evidence** — what happened and whether residual risk/closure changed.

Persistent guards:
- `compensating control configured ≠ compensating control effective`;
- `control health endpoint green ≠ control assurance sufficient`;
- `control effective yesterday ≠ control current now`;
- `exception unexpired ≠ exception usable after required control failure`;
- `break-glass account exists ≠ emergency use authorized`;
- `emergency declared ≠ unlimited capability granted`;
- `operator authenticated ≠ operator may self-approve emergency authority`;
- `two approvals recorded ≠ approvals independent`;
- `approval independent ≠ runtime use independently observed`;
- `emergency access ended ≠ post-use review complete`;
- `logs exist ≠ operator could not suppress them`;
- `PITR restored emergency config ≠ emergency authority reactivated`;
- `offline client cached emergency state ≠ remote consequence authorized`.

## Compensating-control contract
A security-affecting exception should identify the controls whose continued effectiveness is material to the deviation. Generic contract fields may include:
- named control objective and bounded mechanism/reference;
- required assurance state for each consequence class;
- evidence source and freshness/currentness semantics;
- failure/UNKNOWN behavior;
- independence expectations where correlated failure would defeat both primary and compensating control;
- validation owner and evidence retention boundary;
- effect of control degradation on exception admission;
- hard expiry/revocation and closure path.

Do not prescribe one universal health-check interval or numeric threshold. Those require actual threat model, BIA, provider/runtime evidence and consequence classification.

### Fail-safe relation
If a compensating control is a condition of the exception, its material failure or inability to establish required current assurance means the exception cannot silently continue as if the condition still held. Depending on the real risk model this can pause only the affected exceptional capability rather than the entire PWA.

Unique local data preservation remains separate: local flight/logbook records and drafts may remain usable while exceptional remote consequence authority is unavailable.

## Break-glass is a separate emergency capability
Break-glass is justified only for a defined class of emergencies where the normal privileged/control path is unavailable or itself unsafe and where refusing all emergency action would create greater governed harm.

Generic properties:
- distinct from routine administrator/session authority;
- narrow target/capability/environment scope;
- explicit emergency reason/evidence class;
- strong authentication appropriate to the actual threat model;
- bounded activation and hard expiry;
- server-side admission and deny-by-default outside scope;
- no implicit inheritance to unrelated tenants/cases/data;
- independent activation/approval where the risk requires it;
- protected, independently useful audit evidence;
- immediate or bounded post-use review and credential/capability reset where appropriate;
- emergency generation cannot become a normal-role grant by persistence or renewal inertia.

No generic claim is made that a standing shared password, one global administrator, or exactly two human approvers is the correct implementation.

## Independent approval and separation boundaries
Independence is about failure/authority domains, not merely headcount.

Two clicks are not independent if:
- the same actor controls both identities;
- one compromised IdP/session can impersonate both approvers;
- the requester can alter the approval policy or approver set;
- both approvals depend on the same compromised administrative plane;
- the emergency operator can erase/alter the only audit evidence;
- an automated approver merely reflects requester-controlled input.

Generic separation questions:
1. Who requests exceptional authority?
2. Who can approve/activate it?
3. Who can change the approval policy/approver set?
4. Who exercises the capability?
5. Who observes/audits use?
6. Who can revoke/terminate it?
7. Who performs post-use review/closure?

The real product may combine some duties after risk analysis. Web Manager does not invent employee roles or a fixed quorum.

## Emergency when the approval plane is unavailable
The hardest case is a real emergency plus loss/compromise of the normal approval plane. Do not solve this by declaring any surviving administrator authoritative.

A viable design needs a pre-established recovery/emergency authority model whose trust roots and custody survive the failure it is intended to address. If no trustworthy current authority can be established, consequence-bearing remote action may remain blocked even though local preservation/read/export capabilities continue.

Any single-person emergency route, if a real product ultimately requires one, is a separately accepted high-risk design with narrow scope, hard expiry, independent evidence and mandatory post-use review — not a generic recommendation from this study.

## Evidence independence and anti-concealment
Break-glass use is high-value evidence. The operator should not be able to rely on emergency privilege to silently destroy the sole evidence of that same use.

Generic direction:
- security-relevant activation/use/termination events are captured outside the narrow mutable domain where practical;
- audit unavailability is explicit `UNKNOWN`, not `clean`;
- evidence minimization still applies — record capability, generation, reason class, approval/use/termination and outcome metadata rather than unnecessary user payloads;
- evidence protection does not imply immutable retention forever; retention/deletion remain governed separately.

## Multi-region, rollback and PITR
Break-glass activation/revocation is distributed security state. Track authorization, publication, regional admission, actual enforcement and convergence separately.

- A region missing activation must not invent it from another region's client cache.
- A region missing revocation/expiry must not keep emergency authority indefinitely.
- PITR/rollback cannot resurrect an ended emergency generation.
- Recovery must reconcile against a surviving current emergency/security floor before consequence-bearing traffic reopens.
- Split-view emergency state is an incident/reconciliation condition, not evidence that either client observation is globally authoritative.

## PWA / managed-iPad transfer
A LogMate-like company iPad can remain useful during emergency-control outages without becoming an emergency authorization oracle.

- Preserve unique local flight/logbook records and drafts.
- A cached emergency banner/config/exception in SW or IndexedDB is presentation/observation state only.
- Offline-authored work under a then-valid emergency state is re-admitted against current server authority at commit time unless a product-specific transaction contract proves otherwise.
- If break-glass expires/revokes while the iPad is offline, reconnect does not revive it.
- Service Worker update, emergency-policy reconciliation and data/schema reconciliation are separate.
- Do not assume iPadOS background execution, push delivery, MDM state or device ownership can maintain or prove emergency authority. Physical Safari/Home Screen/MDM validation remains OPEN.

## UX transfer — Track B
Emergency/degraded states must communicate task consequence rather than internal security jargon. Candidate semantics include:
- `Saved on this device — submission is paused`;
- `Additional approval is required before this action can be submitted`;
- `Emergency access is active for this operation` where disclosure is safe and useful;
- `Emergency access has ended — rechecking permission`;
- `Your local records are preserved`.

Avoid fear-heavy banners that imply data loss when only remote authority is paused. Do not reveal sensitive approver identities/control topology unnecessarily. Status must not rely on color alone; screen-reader and human validation remain OPEN.

## MINTTAP DECISION — generic governance
1. Treat compensating-control effectiveness as a runtime assurance dependency when the exception contract requires it; configuration presence alone is insufficient.
2. Represent break-glass as a separate, narrow, expiring emergency capability, not a universal administrator bypass.
3. Keep request, approval/activation, exercise, policy administration, observation/audit, revocation and review conceptually separable; combine duties only with explicit real-world risk evidence.
4. Judge independence by authority/failure domains, not merely number of clicks or accounts.
5. Require server-side consequence admission; client/PWA state cannot self-authorize emergency remote effects.
6. Preserve unique offline local data when emergency authority is unavailable or ended.
7. Make emergency expiry/revocation rollback/PITR-resistant relative to surviving current security state.
8. Treat audit/telemetry loss as UNKNOWN and protect emergency-use evidence from unilateral concealment where the threat model requires it.
9. Require bounded post-use review/closure; emergency termination is not closure by itself.
10. Do not invent product roles, quorum, durations, control thresholds, credential form, legal permissions or aviation authority. These remain OPEN.

## VALIDATION — 184-case destructive campaign
Families: exception active/control failed; control stale/UNKNOWN; false-green health; correlated primary+compensating failure; emergency without qualifying incident; routine admin invokes break-glass; requester self-approves; same actor controls two identities; compromised IdP impersonates quorum; approver-set mutation race; approval after expiry; revoke/use race; region misses activation; region misses revoke; split-view emergency generation; operator suppresses audit; audit pipeline outage; evidence tampering; credential copied/shared; emergency token replay; overbroad tenant/resource scope; wildcard capability; privilege inheritance; session survives emergency expiry; queue authored during emergency then committed after revoke; PITR resurrects emergency config; app/config rollback; stale CDN/cache; stale SW/IndexedDB; long-offline iPad; reconnect after multiple generations; client clock rollback; MDM/device ownership mistaken for human authority; Shared iPad account switch; push delayed/missed; control provider outage; approval-plane outage; emergency recovery-root compromise; post-use review skipped; emergency credential not reset; repeated break-glass normalization; privacy-heavy logs; high-cardinality identity telemetry; inaccessible status; color-only warning; screen-reader/human misunderstanding; unique local data wrongly deleted; progressive recovery opens stale region.

Generic campaign definition is PASS. Product/runtime/device/human execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** 177 supplies bounded exception generations, hard expiry, rollback resistance and debt governance; 173–176 supply distributed convergence, fail-safe degradation, observability and recovery proof.
- **TRANSFER VALIDATION:** NIST AC-5/AC-6 support separation of duties and least privilege; NIST's functionality/assurance distinction supports testing whether a compensating control is effective rather than merely configured.
- **TRANSFER VALIDATION:** CISA cloud guidance explicitly recognizes protected emergency `Break Glass` accounts, possible multi-user coordination, extensive audit and the risk that administrators can disable alert/log evidence.
- **TRANSFER VALIDATION:** OWASP Broken Access Control supports server-side deny-by-default and testing of alternate privileged paths.
- **CONTRADICTION:** `the compensating control was enabled when approved, so the exception remains safe until expiry` is rejected.
- **CONTRADICTION:** `two approvals exist, therefore separation of duties is proven` is rejected.
- **CONTRADICTION:** `emergency means the administrator may bypass every policy` is rejected.
- **CONTRADICTION:** `the operator's own log says nothing bad happened, therefore break-glass use is clean` is rejected.
- **CONTRADICTION:** `the offline PWA saw emergency access before disconnect, therefore queued consequences remain authorized` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH
OPEN: actual MintTap/LogMate emergency classes, consequence taxonomy, control objectives, compensating controls, approver/administrator/reviewer roles, independence/quorum requirements, identity provider and recovery roots, credential technology, activation/expiry/revocation durations, legal/aviation constraints, multi-region topology, authoritative time/currentness, audit stack/retention, provider restore behavior, managed-iPad/Safari/MDM runtime behavior and human/AT evidence.

DEPENDENCY — Software Engineering: once real architecture exists, validate policy-enforced narrow emergency capability, control-assurance inputs, independent approval domains where required, session termination, anti-replay, expiry/revocation, evidence protection, regional convergence, rollback/PITR resistance and queue re-admission. This study does not prescribe a specific cryptographic/token/workflow implementation.

DEPENDENCY — Design Studio: validate accessible local-preservation, approval-required, emergency-active/ended and recheck semantics. Current Web Design evidence remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and representative-human evidence remain OPEN.

CHANGE WATCH: NIST control catalog/assessment guidance, CISA emergency-access guidance, OWASP access-control guidance, provider privileged-access capabilities and Safari/iPadOS PWA/MDM behavior.

## Gate
**178 PASS (generic).** Web Manager can now distinguish compensating-control configuration from assurance, make exception admission conditional on required current assurance, model break-glass as a bounded emergency capability, assess approval independence by authority/failure domains rather than headcount, protect post-use evidence/closure, prevent region/PITR/offline-client persistence from turning emergency authority into a standing bypass, and preserve offline-first local utility without stale remote consequence authority.

Next adjacent bottleneck: **PWA emergency-authority compromise, break-glass credential recovery & trust reconstitution** — determine what happens when the emergency path or one of its approval/recovery roots is itself compromised; how to revoke and rebuild emergency authority without trusting the compromised root to bless its successor; how sessions/regions/offline clients converge after emergency-root rotation; and how local operational data remains preservable while privileged trust is being reconstituted.