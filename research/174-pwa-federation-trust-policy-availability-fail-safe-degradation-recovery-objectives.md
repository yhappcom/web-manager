# 174 — PWA Federation Trust-Policy Availability, Fail-Safe Degradation & Recovery Objectives

Status: **PASS (generic) / PRODUCT + FEDERATION + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + SLA/BIA + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A browser/network/SW/offline mechanics; Track B degraded-state UX; Track C resilience/accessibility validation; Track D privacy-bounded availability telemetry.  
Dependency: 171–173 federation evidence, trust metadata/currentness, distribution/rollback/convergence.

## Why this study exists

173 established that trust-policy publication and convergence are distributed security-state transitions. The adjacent failure boundary is availability: current authority can become temporarily unverifiable because an IdP, federation resolver, control plane, region, DNS/TLS dependency or network path is unavailable. An offline-first PWA must remain useful without converting stale trust into indefinite mutation authority.

Central rule:

> **Degrade by consequence, not by one global online/offline switch. Preserve local user data and low-risk local work; require current authority for consequence-bearing remote effects; define recovery objectives per capability from business impact rather than inventing one universal SLA.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Distinguishes transport reachability, HTTP 503/504/Retry-After, Service Worker/cache/storage possession, browser offline state and reconnect. None proves federation currentness.
- **B UX/IA/Content:** owns understandable capability-specific degraded states: local work available, remote submission paused, access check unavailable, retry/review path, preserved drafts.
- **C Quality/Accessibility:** owns dependency-outage, retry-storm, stale-authority, partial-recovery, long-offline and AT/human destructive campaigns.
- **D Search/Analytics:** bounded consumer. Availability/convergence telemetry must not become a per-user federation graph.
- **E Security/Operations:** **bottleneck/owner**. Owns consequence classes, fail-safe admission, dependency isolation, recovery-objective semantics and reopen criteria.

## SOURCE

### NIST SP 800-34 Rev.1 — contingency planning

NIST defines contingency planning as coordinated plans, procedures and technical measures for recovery after disruption. It defines Recovery Time Objective (RTO) as the time system components can remain in recovery before mission/business impact becomes unacceptable, and Recovery Point Objective (RPO) as the point in time to which data must be recovered after an outage.

Sources:
- https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
- https://csrc.nist.gov/glossary/term/Recovery_Time_Objective
- https://csrc.nist.gov/glossary/term/recovery_point_objective

Transfer: recovery objectives follow mission/business impact. They are not properties that can be copied generically from another PWA or provider.

### RFC 9110 — HTTP Semantics

HTTP 503 means the server is temporarily unable to handle a request and may provide `Retry-After`; 504 means a gateway/proxy did not receive a timely upstream response. These are transport/service signals, not proof that an authorization decision should be reused from stale state.

Source: https://www.rfc-editor.org/rfc/rfc9110.html

Transfer: an authorization dependency outage can be represented as temporary service limitation, but HTTP status alone does not decide which product capabilities may safely continue.

### OpenID Federation 1.0 — Final

Trust-chain establishment requires entity identifiers, locally trusted anchors/keys, sufficient Entity Statements and independent validation of candidate trust chains. A resolver can be used as a trusted third party, making its availability and integrity an explicit dependency when chosen.

Source: https://openid.net/specs/openid-federation-1_0.html

Transfer: resolver/provider outage is a dependency failure; it does not transform previously cached federation evidence into timeless authority.

## SYNTHESIS — availability is consequence-specific

Do not collapse these states:
1. **transport availability** — can the client reach any server path?;
2. **application availability** — can the app shell/local workflow run?;
3. **data availability** — are local/remote records readable?;
4. **identity availability** — can authentication/current session be established?;
5. **trust-currentness availability** — can current issuer/anchor/policy status be established?;
6. **authorization availability** — can a current decision be made for this operation?;
7. **mutation availability** — can a consequence-bearing remote effect safely commit?;
8. **recovery evidence** — can operators prove dependencies and enforcement have recovered sufficiently to reopen capability classes?

Persistent guards:
- `network reachable ≠ authority reachable`;
- `IdP reachable ≠ federation currentness established`;
- `cached token valid-looking ≠ current mutation authority`;
- `resolver unavailable ≠ cached trust becomes evergreen`;
- `authorization unavailable ≠ local data unavailable`;
- `remote mutation paused ≠ local draft must be blocked`;
- `503 received ≠ safe to replay automatically later`;
- `Retry-After elapsed ≠ authority restored`;
- `dependency recovered ≠ queued operations still authorized`;
- `region healthy ≠ all authorization dependencies healthy`;
- `RTO ≠ RPO ≠ revocation/convergence objective`;
- `service restored ≠ security floor reconciled`.

## Capability degradation matrix

Generic consequence classes, not product promises:

| Capability class | Current authority unavailable | Generic direction |
|---|---|---|
| local app shell/help | no remote consequence | continue when locally available |
| unique local record/draft creation | local-only, user-preserving | continue and clearly mark unsynced |
| local read/export of already-authorized user data | bounded confidentiality risk | preserve where local authorization/session policy permits; product validation OPEN |
| remote refresh/read | server-side disclosure | require current server admission appropriate to sensitivity |
| queued sync with merge effects | remote mutation | hold until current authority and conflict state are re-evaluated |
| delegation/role/policy change | high-consequence authority mutation | fail safe / pause |
| destructive delete or irreversible external effect | high consequence | require current authoritative decision; never infer from stale client state |

This is a design taxonomy, not a MintTap/LogMate implementation claim.

## Stale-read versus stale-authority budgets

A useful offline application can tolerate some stale **content** while being intolerant of stale **authority**. Treat them as separate budgets.

- Content staleness may be acceptable for local reference/drafts depending on domain semantics.
- Authority staleness determines whether a new remote consequence may be admitted.
- Revocation/compromise events can collapse the acceptable authority-staleness window even if content remains useful.
- No generic duration is selected here. Actual bounds require product consequence, legal/aviation obligations, provider behavior and BIA evidence.

## Retry, overload and recovery storms

A dependency recovery can fail again if every browser/region retries immediately. Generic requirements:
- respect server-directed retry information where applicable;
- use bounded backoff/jitter in implementation rather than tight polling;
- keep local work usable while remote authority remains unavailable;
- make queued work idempotent/reconciliation-aware before retry;
- do not treat timer expiry as proof of restored authority;
- prioritize current trust/policy reconciliation before draining stale consequence-bearing queues.

Exact retry algorithms belong to Software Engineering and require runtime validation.

## Recovery objectives — do not invent one SLA

Separate at least:
- **service RTO:** how long a capability can remain unavailable before unacceptable mission/business impact;
- **data RPO:** how much committed data loss is tolerable after recovery;
- **authority-currentness objective:** how stale trust/authorization evidence may be for a given consequence;
- **emergency revocation propagation objective:** how quickly a compromised issuer/anchor/policy must cease being accepted across controlled enforcement domains;
- **reconciliation objective:** how quickly restored regions/clients/queues must be checked against the current floor;
- **local-data durability objective:** how long unique offline data must remain recoverable despite remote outage.

These objectives can conflict. Faster availability must not silently relax a security floor; stricter authority freshness must not destroy unique local records. Actual numeric objectives remain OPEN pending BIA/product/provider evidence.

## Recovery/reopen sequence

For a failed federation/control-plane dependency:
1. preserve unique local/offline data and incident evidence;
2. restore transport/dependency reachability;
3. establish current authoritative policy/security floor independent of restored snapshots;
4. verify issuer/anchor/key/status dependencies at the required currentness;
5. verify regional enforcement at/above the floor;
6. reopen capability classes progressively by consequence;
7. re-evaluate queued operations against current actor/delegation/policy/conflict state;
8. quarantine operations no longer admissible; preserve user data/drafts;
9. observe retry/load behavior and rollback signals;
10. claim recovery only for the bounded controlled domain actually evidenced.

`dependency endpoint returned 200 ≠ safe to reopen all mutations`.

## PWA / managed-iPad transfer

A long-offline Home Screen PWA may remain valuable while federation services are unavailable. Generic direction:
- app shell and already-local user work may remain available where browser storage survives;
- new local flight/logbook drafts should not depend on live federation merely to exist;
- remote sync/delegation/authority-changing operations wait for current server-side admission;
- cached token, SW, IndexedDB projection or MDM ownership does not create evergreen authority;
- reconnect first preserves unique local data, then establishes current authority, then reconciles queued effects;
- no generic claim is made about iPadOS background execution, persistence, MDM policy, connectivity or Safari/Home Screen behavior. Physical validation remains OPEN.

## UX transfer — Track B

Expose consequences, not topology. Useful semantic states include:
- `You can keep working on this device. Changes are not synced yet.`
- `Access cannot be checked right now. Submission is paused.`
- `Your saved records are still available on this device.`
- `Connection is back. Access is being checked before saved changes are submitted.`

Avoid misleading `You're offline` when transport is online but authority dependencies are unavailable. Avoid countdowns unless backed by authoritative recovery information.

## Privacy/analytics transfer — Track D

Availability evidence should prefer dependency/capability/region/generation aggregates. Do not log raw federation tokens, claims or long-lived per-user outage histories merely to measure uptime. Security diagnostics remain purpose-bound and retention-limited.

## MINTTAP DECISION — generic governance

1. Degrade by capability/consequence, not one global online/offline boolean.
2. Preserve unique local PWA data and low-risk local work during authority outages.
3. Do not convert cached federation/session/policy state into indefinite remote mutation authority.
4. Separate content-staleness tolerance from authority-staleness tolerance.
5. Treat emergency revocation currentness as stricter than ordinary provider outage when consequence requires it.
6. Define RTO/RPO/currentness/revocation/reconciliation/durability objectives separately from BIA/product evidence.
7. Recover security floor and enforcement evidence before reopening consequence-bearing mutations.
8. Re-evaluate queued work after recovery; timer expiry or connectivity return does not authorize replay.
9. Keep degraded/recovery UX accessible and consequence-oriented.
10. Actual numeric SLAs, provider topology, MintTap/LogMate authority model, managed-iPad behavior and physical runtime remain OPEN.

## VALIDATION — 152-case destructive campaign

Families include: IdP outage; federation resolver outage; trust-anchor/status endpoint outage; control-plane outage; one-region/majority-region outage; DNS/TLS failure; 502/503/504; Retry-After absent/present/malformed; overload/retry storm; exponential-backoff implementation failure; provider recovery then relapse; partial dependency recovery; stale cached token; stale JWKS/metadata/policy; emergency revoke during outage; revoke status unreachable; split-view recovery; PITR/backup rollback; region healthy with stale downstream dependency; false-green health check; service 200 before authority reconciliation; local shell available/remote auth unavailable; local draft/read/export; queued sync; destructive mutation; role/delegation change; unique flight record; storage pressure/eviction; stale SW/current data and current SW/stale authority; long-offline cold start; multiple missed generations; reconnect during outage; connectivity flap; clock skew; duplicate/lost ACK; idempotent replay; conflict after recovery; account/delegation revoked while offline; actor reauthorized under new generation; old queue not auto-executed; Shared iPad/user switch; managed-device state; accessible degraded status; keyboard/screen-reader recovery; reduced motion/non-color-only communication; human comprehension; privacy-minimized telemetry; BIA/RTO/RPO mismatch; emergency propagation objective breach; reconciliation objective breach; incident reconstruction.

Generic campaign definition is PASS. Product/provider/browser/device execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION

- **TRANSFER VALIDATION:** 173's monotonic security floor remains mandatory after availability recovery; restore/reachability cannot lower it.
- **TRANSFER VALIDATION:** NIST contingency-planning concepts support consequence/business-impact-derived recovery objectives, not arbitrary generic SLA numbers.
- **TRANSFER VALIDATION:** RFC 9110 provides temporary-unavailability/retry semantics but not authorization reuse semantics.
- **CONTRADICTION:** `IdP/resolver down, therefore keep accepting the last known federation authority indefinitely` is rejected.
- **CONTRADICTION:** `authorization dependency down, therefore disable local drafting/export and risk losing unique offline work` is rejected as a generic default.
- **CONTRADICTION:** `provider recovered, therefore drain every queued mutation immediately` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate capability consequences; BIA; numeric RTO/RPO/MTD/currentness/revocation/reconciliation objectives; provider/IdP/resolver topology and SLAs; policy/key/status caching; queue semantics; offline authorization; managed-iPad/MDM; physical Safari/Home Screen; aviation/legal requirements; human/AT evidence.

DEPENDENCY — Software Engineering: circuit breaking, backoff/jitter, dependency isolation, durable queue, idempotency, current-floor probes and progressive reopen require implementation/runtime evidence.

DEPENDENCY — Design Studio: consume accessible degraded/recovery-state interaction evidence; do not invent visual styling here. Current Design Studio Web status remains Stage 3 PRACTICE / NOT PASSED pending exact runtime, physical-device/PWA, screen-reader and human evidence.

CHANGE WATCH: OpenID Federation/provider availability semantics; Safari/iPadOS PWA storage/background behavior; provider-specific outage/retry/status behavior; relevant contingency/security guidance.

## Gate

**174 PASS (generic).** The Web Manager can now separate application/data/identity/trust/authorization/mutation availability; preserve offline-first utility without stale-authority fail-open; distinguish content-staleness from authority-staleness; define consequence-specific degradation and recovery/reopen ordering; and formulate recovery objectives without inventing production SLAs.

Next adjacent bottleneck: **federation dependency isolation, cascading-failure containment & degraded-mode observability** — determine how authorization/provider failures propagate through web/API/CDN/queue dependencies, how to prevent retry/queue storms and false-green health, and how to prove which degraded capability classes remain safe without privacy-heavy telemetry.