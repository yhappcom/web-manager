# 175 — PWA Federation Dependency Isolation, Cascading-Failure Containment & Degraded-Mode Observability

Status: **PASS (generic) / PRODUCT + FEDERATION + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + SLO/BIA + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track A browser/network/SW mechanics; Track B degraded-state semantics; Track C resilience/accessibility validation; Track D privacy-bounded telemetry.  
Dependency: 171–174 federation, trust-currentness, convergence, availability and recovery-objective work.

## Why this study exists

174 established consequence-specific degradation: local work can remain useful while current remote authority is unavailable. The next failure boundary is propagation. A failing IdP, federation resolver, trust-status service, control plane, region or queue can consume connection pools, worker capacity, retries and operator attention until unrelated capabilities fail too. Conversely, a coarse health dashboard can remain green while the authorization path required by one consequence class is stale or saturated.

Central rule:

> **Contain dependency failure by capability and resource boundary; admit remote consequences only through current authoritative dependencies; prove degraded safety with bounded server-side enforcement evidence rather than client presence or privacy-heavy identity telemetry.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Owns DNS/TLS/HTTP failure semantics, connection/retry behavior, SW/cache/storage possession and reconnect boundaries. Browser reachability does not prove downstream authority health.
- **B UX/IA/Content:** consumes capability state, not infrastructure topology. Distinguishes local work preserved, submission paused, access-check unavailable, recovery/recheck and conflict-review states.
- **C Quality/Accessibility:** owns cascading-failure, false-green, overload, partial-recovery, stale-SW and accessible-degraded-state destructive validation.
- **D Search/Analytics:** bounded consumer. Availability telemetry should use low-cardinality capability/dependency/generation aggregates and must not become a durable user/federation graph.
- **E Security/Operations:** **bottleneck/owner**. Owns failure-domain mapping, isolation requirements, admission gates, degraded-mode observability and progressive recovery evidence.

## SOURCE

### NIST SP 800-53 Rev. 5 / Release 5.2.0

NIST's current control catalog addresses availability, monitoring, incident response and protection against denial-of-service as part of risk-based system controls. SI-4 system monitoring explicitly connects monitoring to continuous monitoring and incident response; its discussion also warns that automated monitoring can create privacy risk when unrelated records are linked.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

Transfer: monitoring is evidence for operational/security decisions, not permission to collect arbitrary identity-rich traces.

### NIST SP 800-160 Vol. 2 Rev. 1 — cyber resiliency

NIST frames cyber resiliency as the capability to anticipate, withstand, recover from and adapt to adverse conditions, stresses, attacks or compromises.

Source: https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final

Transfer: degraded operation is a designed system state. It is not equivalent to silently bypassing a failed security dependency.

### RFC 9110 — HTTP semantics

`Retry-After` tells a user agent how long it ought to wait before a follow-up request; with 503 it indicates expected service unavailability. It is not an authorization-currentness signal.

Source: https://www.rfc-editor.org/rfc/rfc9110.html

Transfer: retry timing and security admission remain separate.

### OpenTelemetry semantic conventions — observability boundary

OpenTelemetry defines common semantic conventions for metrics/traces/logs. Its HTTP metrics require or recommend bounded attributes and explicitly require route templates to be low-cardinality; dynamic URL paths are not substitutes. Some header-derived attributes carry cardinality warnings.

Sources:
- https://opentelemetry.io/docs/concepts/semantic-conventions/
- https://opentelemetry.io/docs/specs/semconv/http/http-metrics/
- https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/

Transfer: operational observability can be useful without embedding raw subject IDs, tokens, claims, case IDs or unbounded URLs into metric dimensions.

## SYNTHESIS — map failure propagation, not just endpoints

A dependency graph for authorization-sensitive web/PWA operation should distinguish at least:
1. DNS/TLS/network path;
2. web/API ingress and resource pools;
3. authentication/IdP path;
4. federation metadata/JWKS/resolver/status path;
5. local policy/authorization decision point;
6. data store and mutation transaction;
7. queue/worker/reconciliation path;
8. control-plane/security-floor distribution;
9. telemetry/health pipeline;
10. local PWA shell/storage/draft path.

A failure can propagate through shared capacity even when there is no direct semantic dependency. Examples: federation timeouts occupy API workers; retrying clients overload ingress; queue replay saturates the same database used by reads; a telemetry exporter blocks application work; a control-plane outage prevents current policy admission while ordinary static content remains healthy.

Persistent guards:
- `dependency endpoint healthy ≠ capability path healthy`;
- `global health green ≠ authorization path current`;
- `one dependency failed ≠ every local capability must fail`;
- `circuit open ≠ authorization granted`;
- `fallback available ≠ fallback semantically equivalent`;
- `retry scheduled ≠ retry authorized`;
- `queue depth falling ≠ stale work admissible`;
- `telemetry absent ≠ system healthy`;
- `client online ≠ server dependency graph healthy`;
- `synthetic probe PASS ≠ user consequence path PASS`;
- `high-cardinality telemetry ≠ better observability`;
- `correlation useful ≠ indefinite identity linkage justified`.

## Dependency-isolation requirements

Generic architecture requirements, not implementation prescriptions:

- **Resource isolation:** high-latency federation/status calls should not be able to consume all capacity required for local/static/read-only or recovery paths.
- **Timeout budget:** downstream waits are bounded; upstream request lifetime cannot expand without limit through nested retries.
- **Retry ownership:** one layer owns a retry policy for a failure path. Browser, API, proxy and worker must not independently multiply retries without an explicit budget.
- **Admission before replay:** recovered transport does not drain consequence-bearing queues until current authority/security floor and conflict state are re-established.
- **Load shedding by consequence:** protect critical reconciliation/recovery and current-authority paths before optional background refresh/analytics.
- **Failure-domain separation:** telemetry/exporter, analytics and nonessential third parties should not be required for core authorization or local-data preservation.
- **Known-state degradation:** when current authority cannot be established, remote consequence classes pause while explicitly safe local capabilities may continue.

Circuit breakers, bulkheads, bounded queues and backoff/jitter are candidate implementation mechanisms. Exact algorithms and thresholds belong to Software Engineering/runtime validation; Web Manager owns the behavioral requirements and failure evidence.

## Cascading-failure patterns

### Retry amplification

A single failed dependency can trigger retries at browser, CDN/proxy, API client, service and worker layers. If each layer retries independently, request volume multiplies during the period of least capacity.

Direction: assign retry responsibility, bound attempts/time, add jitter where implementation warrants it, honor authoritative service hints without treating them as authorization, and stop retrying consequence-bearing work when current admission cannot be established.

### Queue recovery storm

A backlog can become a second outage when a dependency recovers. Queue age and depth do not establish semantic validity. Old work may have crossed delegation, policy, schema or conflict generations.

Direction: progressive drain, current-floor check, idempotency/reconciliation, per-consequence admission and quarantine of no-longer-admissible operations.

### Shared-pool exhaustion

Slow trust/IdP calls can starve unrelated requests when they share worker/connection/thread pools.

Direction: require bounded isolation appropriate to consequence and capacity; exact pool topology remains implementation-specific.

### False-green recovery

An endpoint returning 200 or a generic `/health` passing can coexist with stale JWKS, failed resolver status, old policy generation or a saturated queue.

Direction: health evidence is layered: reachability, dependency readiness, current security-floor generation, enforcement/admission result and backlog/reconciliation state. Do not collapse them into one boolean.

## Degraded-mode observability model

Observe the minimum facts needed to answer operational questions:

| Question | Preferred bounded evidence |
|---|---|
| Is capability X accepting consequences? | capability class + admission state + reason class |
| Is current trust floor enforced? | region/service + policy/security generation + enforcement result |
| Which dependency is blocking admission? | dependency class + bounded failure class |
| Is retry pressure dangerous? | aggregate attempts/rate/latency/rejection/backlog |
| Is recovery converging? | region/service generation distribution + queue age/depth + reconciliation outcomes |
| Is local PWA work preserved? | aggregate save/export/error outcomes where instrumentable; physical-device validation still required |

Avoid by default in ordinary availability metrics: raw access/ID tokens, federation claims, subject identifiers, email/phone, case IDs, flight record payloads, free-text errors, full URLs with user data, stable device fingerprints or indefinite per-user outage histories.

Security incident evidence can require more detail, but it is a separate purpose/retention/access regime from product analytics and ordinary availability dashboards.

## Observability failure modes

- **Telemetry pipeline outage:** absence must render state `UNKNOWN`, not `HEALTHY`.
- **Sampling:** sampled traces can diagnose paths but cannot alone prove universal enforcement.
- **Aggregation lag:** delayed dashboards cannot prove present authorization currentness.
- **Split view:** regions can report different current generations; aggregation must preserve divergence rather than average it away.
- **Cardinality attack:** attacker-controlled paths/headers/IDs can exhaust metric dimensions; prefer route templates and bounded enums.
- **Privacy overcollection:** joining identity, federation and outage histories can create an unnecessary behavioral graph.
- **Client spoof/staleness:** PWA telemetry is supporting evidence, never the authority oracle for server enforcement.

## Capability isolation matrix

| Capability | Federation/current-authority dependency unavailable | Isolation direction |
|---|---|---|
| static/app shell/help | usually no consequence | keep independent where practical |
| unique local draft/save | local preservation | keep usable; do not couple to telemetry/IdP availability |
| local export | bounded local confidentiality | preserve subject to product/session policy; validation OPEN |
| authenticated remote read | disclosure consequence | current server admission required to sensitivity policy |
| queued sync/mutation | remote consequence | hold and re-evaluate after recovery |
| role/delegation/policy mutation | authority consequence | fail safe; isolate recovery/control paths |
| destructive/external action | high consequence | current authoritative admission mandatory |
| analytics/marketing | nonessential to core safety | must not block core local/recovery path |

## PWA / managed-iPad transfer

A company iPad can be online while federation currentness is unavailable, or offline while local records remain useful. Generic direction:
- Service Worker/app shell and IndexedDB/local state may preserve local utility but do not repair server trust dependencies;
- local draft/save should not require analytics, federation resolver or telemetry exporter merely to succeed;
- reconnect should not create a synchronized retry storm across every queued operation;
- current server authority is established before consequence-bearing queue drain;
- stale client telemetry cannot prove current server enforcement;
- unique local flight/logbook data remains preserved even when remote authority or telemetry is unavailable;
- no claim is made about iPadOS background execution, persistent storage, MDM, physical network transitions or Safari/Home Screen behavior until physical validation.

## UX transfer — Track B

Expose capability consequence, not internal dependency names. Prefer semantic states such as:
- `You can keep working on this device. Sync is paused.`
- `Access cannot be checked right now. Saved changes will not be submitted yet.`
- `Connection is available, but submission is still being checked.`
- `Some saved changes need review before they can be submitted.`

A green connectivity icon must not imply authorization readiness. Recovery messaging must remain keyboard/screen-reader perceivable and not rely on color alone.

## MINTTAP DECISION — generic governance

1. Model federation/authorization dependencies as a graph of capability and resource failure domains, not one health boolean.
2. Isolate local-data preservation and low-risk local work from IdP/resolver/control-plane/analytics/telemetry outages where architecture permits.
3. Bound downstream waits and retry amplification; exact algorithms are Software Engineering responsibilities.
4. Protect current-authority/reconciliation paths from queue/retry/background-refresh storms.
5. Re-admit queued consequences only after current security floor, actor/delegation/policy and conflict state are checked.
6. Treat health as layered evidence: reachability, readiness, currentness, enforcement and reconciliation.
7. `UNKNOWN` telemetry state is not `HEALTHY`; absence, lag and sampling are explicit evidence limitations.
8. Prefer low-cardinality capability/dependency/generation aggregates; separate security incident evidence from ordinary analytics/availability telemetry.
9. Client/PWA telemetry supports diagnosis but never establishes server authority or convergence by itself.
10. Actual topology, thresholds, SLOs, provider behavior, managed-iPad runtime and physical/human evidence remain OPEN.

## VALIDATION — 160-case destructive campaign

Families include: IdP hard outage/latency; resolver outage; JWKS/status timeout; DNS/TLS failure; one-region/partial-region failure; control-plane outage; stale security generation; nested browser/proxy/API/service retries; retry synchronization; malformed/absent Retry-After; shared connection/worker-pool exhaustion; queue backlog/recovery storm; poison message; duplicate/lost ACK; stale operation after delegation revoke/reauthorize; current-floor probe failure; circuit-open/half-open races; fallback misclassification; static/local path accidentally coupled to auth dependency; telemetry exporter blocking app path; metrics backend outage; missing telemetry interpreted green; sampling false confidence; aggregation lag; region split view; high-cardinality route/header attack; raw token/claim leakage; identity correlation; false-green `/health`; endpoint 200 with stale policy; queue depth low with invalid operations; Service Worker stale/current combinations; IndexedDB local draft; offline cold start; reconnect stampede; long-offline iPad; Shared iPad/user switch; storage pressure; accessibility of degraded/recovery state; keyboard/screen reader; non-color status; human comprehension; incident reconstruction; privacy retention/access review; progressive reopen and relapse.

Generic campaign definition is PASS. Product/provider/browser/device execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION

- **TRANSFER VALIDATION:** 174 consequence-specific degradation remains the admission model; isolation exists to preserve safe capability classes rather than to fail open stale authority.
- **TRANSFER VALIDATION:** NIST cyber-resiliency framing supports continuing mission-essential functions in adverse conditions while recovering/adapting; it does not imply bypassing authorization.
- **TRANSFER VALIDATION:** OpenTelemetry low-cardinality route/attribute guidance supports bounded observability rather than identity-rich metric dimensions.
- **CONTRADICTION:** `generic health is green, therefore authorization is safe` is rejected.
- **CONTRADICTION:** `circuit breaker opened, therefore use cached authority` is rejected.
- **CONTRADICTION:** `more user-level telemetry always improves outage diagnosis` is rejected.
- **CONTRADICTION:** `provider recovered, therefore drain the backlog at full rate` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate dependency graph, hosting/CDN/API/queue topology, provider/IdP/resolver contracts, resource pools, retry ownership, queue semantics, SLO/error budgets, security-floor representation, telemetry stack/cardinality/retention, managed-iPad/MDM, physical Safari/Home Screen, aviation/legal requirements and human/AT evidence.

DEPENDENCY — Software Engineering: implement/test timeout budgets, retry ownership, isolation pools, circuit/bulkhead behavior, bounded queues, progressive drain, idempotency, current-floor probes and telemetry backpressure.

DEPENDENCY — Design Studio: consume accessible degraded/recovery semantics. Current Web Design evidence remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human evidence remain OPEN.

CHANGE WATCH: provider/federation failure semantics; OpenTelemetry semantic-convention stability; Safari/iPadOS PWA runtime/storage/background behavior; NIST control updates.

## Gate

**175 PASS (generic).** The Web Manager can now map authorization dependency failure propagation; separate semantic and resource dependencies; define isolation/load-shedding/retry ownership requirements without stealing implementation ownership; distinguish layered health from false-green status; and define privacy-bounded degraded-mode observability that does not turn client telemetry into authority evidence.

Next adjacent bottleneck: **PWA degraded-mode SLO/error-budget semantics, brownout admission & recovery-proof governance** — connect consequence-specific capability states to measurable service objectives without inventing product numbers; define how error budgets interact with security floors; and prevent availability pressure from normalizing unsafe stale-authority exceptions.