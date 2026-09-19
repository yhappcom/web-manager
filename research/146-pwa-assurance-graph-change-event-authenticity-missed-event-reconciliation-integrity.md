# 146 — PWA Assurance-Graph Change-Event Authenticity, Missed-Event Detection & Reconciliation Integrity

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + PROVIDER-EVENT + RECONCILIATION-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 143–145; Track A browser/SW/platform generation identity; Track C evidence provenance and reconciliation tests; Track B degraded-state UX; Track D bounded anomaly signals.

## Why this study exists

145 made assurance invalidation selective by using typed dependencies. That model is only as trustworthy as the facts that change those dependencies. A forged `IdP changed` event can cause denial-of-service invalidation; a missed key/provider/WebKit/MDM change can preserve stale green assurance; and an over-privileged reconciliation service can become a new oracle that silently rewrites security truth.

The problem is therefore not merely event delivery. It is **authenticated observation + durable event handling + independent reconciliation + bounded authority + explicit uncertainty**.

## SOURCE

### Continuous monitoring requires visibility, not blind trust in a feed
NIST SP 800-137 defines information-security continuous monitoring as ongoing visibility into assets, threats/vulnerabilities and control effectiveness, with information sufficient to respond when controls become inadequate. This supports periodic/current-state observation as a backstop to event-driven monitoring rather than assuming one event stream is complete.

Source: https://doi.org/10.6028/NIST.SP.800-137

NIST CSF 2.0 and SP 1303 frame cybersecurity risk management as an ongoing process of monitoring, evaluation and adjustment. They do not make one telemetry source authoritative merely because it is automated.

Sources:
- https://doi.org/10.6028/NIST.CSWP.29
- https://doi.org/10.6028/NIST.SP.1303

### Event envelopes provide identity/context, not automatic authenticity
CloudEvents standardizes event context such as event identity/source/type/time and is useful transfer evidence for durable event identity and duplicate handling. It does **not** mean that receiving a syntactically valid event proves the sender is authorized or that the event is true. Transport/source authentication and provider-specific verification remain separate controls.

Source: https://cloudevents.io/

### Provenance systems distinguish actor/step evidence from mere artifact existence
in-toto is designed to make intended supply-chain steps, actors and ordering verifiable. It is not a PWA assurance-event protocol, but provides useful transfer evidence for binding a statement to an expected actor/context instead of trusting an unscoped payload.

Source: https://in-toto.io/docs/what-is-in-toto/

## SYNTHESIS — four different facts must not collapse

For a material dependency change, distinguish:

1. **DELIVERY FACT** — a message arrived;
2. **SOURCE-AUTH FACT** — the message came through an authenticated/verified source path appropriate to that provider/control;
3. **SEMANTIC FACT** — the payload identifies a recognized dependency and meaningful old/new state or generation;
4. **CURRENT-STATE FACT** — authoritative observation now agrees that the dependency is in that state.

Persistent guards:
- `event received ≠ event authentic`;
- `event authentic ≠ event semantically valid`;
- `event semantically valid ≠ current state independently confirmed`;
- `signed webhook ≠ provider account uncompromised`;
- `TLS protected ≠ business event authorized`;
- `event ID unique ≠ event true`;
- `no event observed ≠ no change occurred`;
- `reconciliation says current ≠ reconciliation oracle infallible`.

## Event source classes and confidence

Do not force every source into one trust tier. Record source class and verification method.

Examples:
- provider webhook with provider-specific authenticity verification;
- deployment/control-plane event from an authenticated internal system;
- periodic provider/API read of current state;
- browser/device observation such as served build/SW generation;
- operator-declared custody/personnel change;
- telemetry/anomaly candidate requiring confirmation.

Analytics or anomaly detection can open a review but cannot by itself authorize trust-floor change, revoke a recovery authority or assert a new key generation.

`telemetry anomaly ≠ dependency truth`.

## Minimal durable change-event envelope

A future implementation should preserve enough information to make processing replay-safe and auditable without storing unnecessary secrets:

`eventId | sourceId | sourceClass | dependencyId | eventType | claimedOldGeneration | claimedNewGeneration | observedAt | receivedAt | verificationMethod/result | payloadDigest/reference | processingState | provenance`

Where provider semantics do not supply old/new generations, do not fabricate them. Record the observed state and let reconciliation determine transition semantics.

### Idempotency and ordering

Duplicate delivery is ordinary. Processing the same authenticated event twice must not create two dependency transitions or repeatedly invalidate evidence.

`duplicate delivery ≠ duplicate state transition`.

Event timestamps are evidence, not universal ordering authority. Provider clocks, delayed delivery and retries can reorder messages. Prefer monotonic/provider generation/version when the provider actually guarantees one; otherwise compare against current-state observation and preserve ambiguity.

`later receivedAt ≠ later dependency state`.
`later event time ≠ authoritative successor`.

## Forged-event and invalidation-DoS resistance

A candidate event must not directly fan out through the assurance graph before source verification and semantic admission.

Pipeline:
1. ingest as `CANDIDATE`;
2. authenticate/verify source according to source class;
3. bind event to known dependency identity and allowed event type;
4. reject or quarantine impossible/unauthorized generation transitions;
5. deduplicate/idempotently admit;
6. when consequence is high or event is ambiguous, confirm current state via a sufficiently independent observation path;
7. commit dependency transition;
8. run 145 targeted invalidation/recompute;
9. record propagation result and required revalidation.

A forged event may therefore create an investigation record without being allowed to invalidate the entire graph.

## Missed-event detection

Event-driven monitoring is low-latency evidence, not completeness proof. Use reconciliation as a backstop.

### Reconciliation invariant

For each material dependency with an observable current state:

`recorded generation/state ↔ independently observed current state`

Classify the result:
- **MATCH** — no unexplained drift;
- **ADVANCED / EVENT-MISSED** — observed state is a legitimate newer state not recorded by event flow;
- **ROLLBACK / REGRESSION SUSPECTED** — observed state appears older or violates a floor;
- **DIVERGENT / MULTI-VIEW** — different authoritative observations disagree;
- **UNOBSERVABLE** — current state cannot presently be verified;
- **UNKNOWN-PROVENANCE** — observation exists but source/identity binding is insufficient.

Do not silently normalize drift. First preserve the mismatch and its provenance; then admit a correction/transition according to policy.

`reconciliation found drift ≠ history should be rewritten`.

## Reconciliation authority must be bounded

A reconciliation component is dangerous if it can both decide what reality is and mutate every security state to match its own answer.

Separate where practical:
- **observer** — reads provider/runtime state;
- **admission logic** — validates identity/generation/transition semantics;
- **assurance graph updater** — records admitted dependency transition;
- **risk/recovery authority** — separately authorizes exceptional rollback/reset when required.

For a small company these can be modules/process roles rather than four services, but their authority semantics should remain distinct.

The reconciliation path may normally advance recorded state to a verified legitimate successor or mark uncertainty. It must not gain a generic `set any trust generation` capability merely because it can read provider state.

`can observe state ≠ may authorize arbitrary state`.

## Oracle compromise and independent observation

Independence is consequence-based, not ceremonial. For ordinary low-impact deployment metadata, one authenticated control plane may be sufficient. For trust-root, recovery authority or anti-rollback floor changes, a single compromised source should not automatically redefine truth if the threat model requires stronger assurance.

Useful independent comparisons can include, when actually available:
- provider control-plane read vs received webhook;
- deployment manifest/release provenance vs served runtime generation;
- MDM inventory vs physical-device observation;
- identity directory vs recovery-authority inventory;
- key/trust metadata vs independently retained checkpoint/anchor evidence.

Do not claim these sources are independent until their shared failure domains are known.

`two APIs ≠ two independent observers`.

## Event loss, outage and catch-up

If the event channel is unavailable:
- mark monitoring coverage degraded rather than green;
- retain last verified state and its age;
- reconcile current state when the source becomes reachable;
- process discovered transitions idempotently;
- do not infer every intermediate event if only current state is knowable;
- trigger targeted assurance invalidation from the earliest defensible changed generation/window.

For long outages, absence of detailed intermediate history can narrow assurance even if the final current state is known.

`current state recovered ≠ complete transition history recovered`.

## PWA / EFB application

A long-offline company iPad is both a consumer of trust state and a possible observation point, but not an omniscient event source. On reconnect:
- stale Service Worker/cache/local metadata cannot declare current server trust state;
- server-side event history cannot prove the physical iPad actually installed/activated a new worker or policy;
- served runtime/build/SW generation evidence and managed-device state remain separately scoped;
- local irreplaceable flight data remains preserved while remote mutation can stay gated if assurance dependencies are unknown/divergent.

`server rollout event ≠ physical iPad converged`.
`iPad reports old generation ≠ server rollback proven`.

Track A must supply exact browser/SW/storage mechanics when they matter; this study does not infer unattended background execution, direct sync, storage persistence or MDM capabilities.

## Cross-track transfer

### Track A — Platform & Browser
Own exact observable browser/SW/runtime generation semantics. Define what can actually be observed from page, worker, server and managed-device surfaces. Do not treat a deployment event as proof of activation on a device.

### Track B — UX / IA
Consume states such as monitoring degraded, reconciliation required, divergent observations and local-data-preserved/remote-write-blocked. Do not expose raw security graph complexity to ordinary users.

### Track C — Quality
Own replay/duplicate/out-of-order/missed-event/reconciliation test evidence. Validate that targeted invalidation occurs once, interruption resumes safely, and contradictory observations remain visible.

### Track D — Search / Analytics
May provide anomaly candidates and measurement of event/reconciliation health. Analytics cannot become an authorization oracle.

### Track E — Owner
Own source admission, event semantics, reconciliation authority, failure-domain analysis, anti-rollback interaction and incident handling.

## MINTTAP DECISION — minimal viable pattern

Do not build an enterprise event bus or GRC platform merely for this model. If implementation becomes necessary, use the smallest mechanism that preserves:
1. authenticated/verified material event sources;
2. stable event identity and idempotent admission;
3. explicit dependency identity/generation;
4. durable event + processing provenance;
5. periodic/event-triggered current-state reconciliation;
6. bounded reconciliation authority;
7. uncertainty/divergence states;
8. 145 typed targeted invalidation;
9. independent confirmation only where consequence/threat model justifies it.

Cadence remains product/provider dependent. Do not invent a universal hourly/daily reconciliation interval.

## VALIDATION — 30-case campaign

1. valid provider event admitted once; 2. duplicate event no duplicate transition; 3. same ID/different payload quarantined; 4. forged webhook rejected; 5. valid transport but unknown dependency rejected; 6. unauthorized event type rejected; 7. old event delivered after new state does not rollback; 8. delayed event preserves provenance; 9. timestamp skew does not define successor; 10. provider generation safely orders where guaranteed; 11. event channel outage marks monitoring degraded; 12. missed event found by reconciliation; 13. reconciliation MATCH causes no invalidation; 14. observed newer state creates one admitted transition; 15. observed older state becomes rollback suspicion, not automatic downgrade; 16. two observations disagree and state becomes DIVERGENT; 17. unobservable provider becomes UNKNOWN rather than green; 18. compromised analytics signal cannot invalidate graph; 19. compromised reconciliation observer cannot invoke arbitrary reset; 20. observer/admission interruption resumes idempotently; 21. propagation interruption resumes from durable transition; 22. provider webhook and provider read share failure domain and are not mislabeled independent; 23. independent retained checkpoint contradicts provider state and contradiction remains open; 24. Service Worker deployment event does not prove device activation; 25. physical iPad old worker observation does not prove server rollback; 26. long-offline iPad crosses multiple epochs and receives targeted validation; 27. stale backup cannot resurrect processed-event cursor/state; 28. current state recovered after outage but missing transition history remains bounded; 29. reconciliation correction cannot erase original event history; 30. forged event → quarantine → independent current-state check → no graph invalidation demonstrates DoS resistance end to end.

## CONTRADICTION / failure-mode analysis

### Event-sourcing theater
A beautifully structured event stream can still be wrong if the source account/control plane is compromised. Schema quality is not source truth.

### Reconciliation theater
Polling the same compromised source that emitted the event may detect delivery loss but not source compromise. Independence claims require failure-domain analysis.

### Over-invalidation
Treating every anomaly as a dependency change turns security monitoring into an attacker-controlled DoS switch.

### Silent auto-healing
Automatically rewriting the graph to match the latest observation destroys the evidence needed to diagnose rollback, split-brain or source compromise.

### Cursor false confidence
A stored `last processed event` cursor can prove local processing position only under the source's actual semantics. It does not prove no provider event was omitted unless the provider offers and the implementation validates such completeness guarantees.

## OPEN

Actual MintTap/LogMate event providers, webhook verification methods, IdP/key/MDM APIs, event sequence guarantees, runtime generation identifiers, reconciliation APIs, independent observation paths, event/evidence storage, source credentials, provider failure domains, managed-iPad observability and consequence thresholds are unknown. No production PASS is claimed.

## CHANGE WATCH

- Provider webhook/API authenticity and replay semantics are provider-specific and can change; verify selected provider documentation at implementation time.
- CloudEvents is transfer evidence for event context/interoperability, not an authentication protocol.
- Browser/WebKit/MDM observable state remains platform/version sensitive.
- NIST continuous-monitoring guidance is durable governance evidence but does not prescribe this PWA-specific implementation.

## Gate result

**PASS (generic).** The Web Manager can now distinguish delivery, source authenticity, semantic admission and current-state truth; resist forged invalidation triggers; use reconciliation to detect missed events without granting it arbitrary reset authority; preserve divergence/uncertainty; and connect admitted transitions to 145 targeted dependency propagation.

Production/provider/managed-EFB runtime assurance remains **OPEN**.

## Next highest-value adjacent question

**PWA assurance-event retention, cursor/checkpoint continuity & monitoring-gap reconstruction.** After source authenticity and reconciliation, the next bottleneck is proving what monitoring interval is actually covered across retention expiry, provider cursor reset, backup restore, event-store compaction and long outages—without claiming completeness that the upstream provider cannot prove.