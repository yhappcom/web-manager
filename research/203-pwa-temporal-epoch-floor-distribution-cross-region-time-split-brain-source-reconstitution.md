# 203 — PWA Temporal-Epoch Floor Distribution, Cross-Region Time Split-Brain & Source Reconstitution

Status: **PASS (generic) / PRODUCT + TIME-TOPOLOGY + IDENTITY + PROVIDER + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime lifecycle mechanics; Track B degraded/recovery state semantics; Track C destructive convergence assurance; Track D bounded telemetry.  
Dependencies: 171–202, especially 199–202.

## Problem

202 established that trusted time has provenance, uncertainty and temporal epochs, and that a compromised source cannot be repaired merely by accepting a new clock reading. The adjacent distributed-systems problem is harder: a new temporal/currentness epoch can be validly admitted at one control-plane location while regions, resource servers, restored nodes and long-offline PWA clients still enforce an older but internally consistent epoch. A replacement time source can also appear healthy while its admission was authorized by the same compromised trust path it is intended to replace.

Central rule: **temporal/currentness epoch issuance, admission, distribution, observation and enforcement are distinct. A region that has not proved the current admitted floor must not infer it from locally consistent time, and a compromised source/trust path must not unilaterally authorize its own successor.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Cached time/session/SW/IndexedDB state and runtime clocks are observations, not global epoch admission. Exact WebKit/Chromium lifecycle semantics remain runtime evidence.
- **B UX/IA/Content:** very high dependency pressure. Owns understandable `NORMAL`, `TIME-SPLIT`, `EPOCH-STALE`, `LOCAL-ONLY`, `RE-ADMISSION REQUIRED`, `QUARANTINED`, `UNKNOWN` semantics without implying local-data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns cross-region split, stale-floor, source-reconstitution, PITR and offline-client destructive tests. Campaign reaches 384 defined cases; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Region/source/epoch telemetry can detect disagreement but cannot elect the authoritative epoch or source.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns floor distribution, enforcement convergence, split-brain quarantine and source-reconstitution admission.

## SOURCE

### RFC 5905 — NTP source selection is explicit mitigation, not blind endpoint trust

RFC 5905 describes selection, clustering and combining across associations and identifies false-ticker mitigation. It also notes that stale associations retain prior values while synchronization distance grows until they become unfit. The protocol therefore does not justify treating a locally retained time sample as indefinitely current, nor does mere endpoint count prove independent authority.

Source: https://www.rfc-editor.org/rfc/rfc5905.html

**TRANSFER VALIDATION:** time-source disagreement and staleness require explicit fitness/currentness reasoning. MintTap/LogMate source topology and thresholds remain OPEN.

### RFC 9523 — Khronos is a watchdog against time-shifting attacks, not a universal authority oracle

RFC 9523 is an Informational IETF publication describing Khronos, a companion/watchdog for NTPv4 intended to improve resistance to time-shifting attacks. It samples from a pool and is designed to detect/mitigate malicious time behavior without replacing the wire protocol.

Source: https://www.rfc-editor.org/rfc/rfc9523.html

**TRANSFER VALIDATION:** diversity/watchdog logic can provide contradiction evidence, but an Informational algorithm is not a MintTap architecture prescription and does not turn majority agreement into authority.

### RFC 8915 — secure transport/source identity does not solve source correctness or succession governance

NTS provides server identity, packet authentication, replay protection and request-response consistency and warns against silent downgrade to unprotected NTP.

Source: https://www.rfc-editor.org/rfc/rfc8915.html

**TRANSFER VALIDATION:** a reconstituted source still needs admission under a current trust policy; transport authentication alone cannot prove that the successor source is authorized or semantically correct.

### NIST SP 800-53 / 800-53A — authoritative and secondary time are governed and assessable dependencies

SC-45 and its enhancements treat synchronization, authoritative sources and secondary sources as explicit security controls; SP 800-53A requires examination/testing of the mechanism rather than assertion alone.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** source/floor topology and convergence must be testable. Exact provider, region and tolerance policy remains OPEN.

### RFC 9769 — current NTP evolution does not remove the trust/currentness problem

RFC 9769 (May 2025, Standards Track) updates RFC 5905 with NTP interleaved modes to improve timestamp accuracy. Its security considerations retain the general NTP security model.

Source: https://www.rfc-editor.org/rfc/rfc9769.html

**CHANGE WATCH:** accuracy improvements do not replace source-admission, anti-rollback or distributed enforcement requirements.

## SYNTHESIS 1 — separate epoch issuance, admission, distribution, observation and enforcement

A reusable distributed model is:
1. **ISSUED** — a candidate epoch/floor statement exists;
2. **ADMITTED** — current policy accepts it as successor/current;
3. **DISTRIBUTED** — a target enforcement domain has received authenticated evidence;
4. **OBSERVED** — monitoring/telemetry sees the claimed state;
5. **ENFORCED** — consequence-bearing authorization actually rejects retired epochs and accepts the current one where appropriate.

Persistent guards:
- `epoch issued ≠ epoch admitted`;
- `epoch admitted centrally ≠ epoch distributed everywhere`;
- `epoch observed ≠ epoch enforced`;
- `region clock healthy ≠ region floor current`;
- `same UTC estimate ≠ same admitted security epoch`.

## SYNTHESIS 2 — cross-region time split-brain is an authorization incident, not a clock-election contest

Two regions can each be internally consistent while one enforces epoch/floor E and another E+1. They can even report similar UTC while disagreeing about retired authority. Conversely, regions can share E+1 but disagree materially on time uncertainty.

Therefore classify independently:
- temporal estimate/uncertainty;
- admitted epoch/floor generation;
- policy/key generation;
- enforcement result for retired/current authority.

If consequence-bearing routing can reach both regions, unresolved disagreement is a security boundary. Do not choose the region whose answer preserves availability, newest wall-clock timestamp, largest generation observed without authenticated lineage, or majority region count.

`region majority ≠ authority election`.

## SYNTHESIS 3 — a floor is useful only if distribution cannot silently lower it

Once an enforcement domain has admitted floor F, ordinary outage/retry/restart must not lower it to F-1. A newly restored region that only has F-1 must remain `EPOCH-STALE`/`RE-ADMISSION REQUIRED` until it obtains admissible current evidence.

Distribution must preserve:
- authenticated lineage to the admitted floor;
- anti-rollback comparison against independently surviving local/remote evidence where applicable;
- explicit target/enforcement-domain identity;
- acknowledgement/observation distinct from enforcement proof;
- inability of a stale control-plane snapshot to redefine currentness.

`distribution failure ≠ permission to lower floor`.

## SYNTHESIS 4 — source reconstitution needs authority outside the compromised source path

If source S or its administrative/trust path is suspected compromised, S cannot become the sole oracle that S2 is its legitimate successor. Reconstitution must bind the successor to current policy/recovery authority and preserve the compromised interval as historical uncertainty.

Generic sequence:
1. mark affected source/path and dependent temporal assumptions suspect;
2. preserve contradiction/evidence without inventing cause;
3. restrict consequence-bearing decisions that require unresolved time/currentness;
4. obtain current policy/reconstitution authority from an independent-enough admitted path;
5. establish successor source identity/configuration and failure-domain claims;
6. validate successor observations against surviving floors/independent evidence;
7. issue/admit a new temporal epoch;
8. distribute it and prove scoped enforcement convergence;
9. retire the compromised source/path for current decisions;
10. keep old historical timing UNKNOWN where evidence cannot resolve it.

Persistent guard: `new source authentic ≠ new source admitted`; `compromised source endorses successor ≠ successor trusted`.

## SYNTHESIS 5 — source replacement and epoch succession are different transitions

A source can rotate while the security epoch remains continuous if continuity is independently proven under policy. Conversely, the same source identity can require a new epoch after restore, rollback or trust compromise.

`source identity changed ≠ epoch necessarily changed`; `source identity unchanged ≠ epoch continuity proven`.

This prevents operational tooling from conflating provider configuration with authorization history.

## SYNTHESIS 6 — convergence proof needs paired negative and positive oracles per consequential surface

A scoped region/enforcement convergence claim should include, where applicable:
- current admitted floor/epoch evidence;
- region/resource-server/RP identity;
- retired-epoch negative authorization probe;
- current-authority positive probe;
- time-source/uncertainty status;
- restored/PITR-node reconciliation status;
- unresolved UNKNOWN surfaces.

A negative probe alone can pass because the service is broken. A positive probe alone can pass while retired authority remains accepted. Both are needed for consequence-bearing convergence.

`all health checks green ≠ epoch convergence proven`.

## SYNTHESIS 7 — routing/load balancing must not turn split-brain into probabilistic authorization

During a split, retries or load balancing can cause the same retired credential to fail in one region and succeed in another. Client retry logic must not search for a permissive region. Server-side routing/failover must not demote currentness to improve success rate.

For PWA queues, repeated retry is transport behavior only; it must not become an authority-selection algorithm.

`retry eventually succeeds ≠ authorization valid`.

## SYNTHESIS 8 — offline PWA forward convergence crosses epochs without treating cache as authority

A long-offline company iPad may miss source compromise, source reconstitution and several epoch/floor transitions. On reconnect:
1. preserve unique local flight/logbook records;
2. isolate cached session/time/floor/SW state from remote authority;
3. obtain current authenticated policy/currentness/epoch floor;
4. reject any attempt to lower the current server floor to accommodate the client;
5. re-evaluate retained session/token under current server authority;
6. distinguish acknowledged remote data from local-only/deferred intent;
7. re-admit consequence-bearing queued operations under current authority;
8. preserve historical creation-time uncertainty rather than rewriting it.

The iPad does not need to reconstruct every missed epoch merely to preserve local data, but remote mutation cannot inherit authority from a missed historical lease.

## SYNTHESIS 9 — telemetry detects split-brain but cannot repair it

Track D may record region epoch IDs, source-set fingerprints, uncertainty bands, stale-floor rejections and convergence coverage. Those signals are useful diagnostics but can be stale, sampled, delayed or derived from the same compromised clock.

Telemetry cannot:
- elect a winning region;
- authorize a successor source;
- lower a floor;
- convert historical UNKNOWN into VALID.

`telemetry consensus ≠ authorization consensus`.

## SYNTHESIS 10 — recovery admission is forward-only for current authority, not retroactive chronology repair

Once source reconstitution and regional convergence succeed, current operations can return to NORMAL. Operations created during the disputed interval retain their provenance and are admitted now, rejected, quarantined or require domain-specific review according to current policy. Recovery does not manufacture historical time proof.

`current regional convergence ≠ historical chronology complete`.

## Track C destructive campaign — 384 cases total

Add eight high-value cases to the 376-case campaign:

1. region A admits E+1 while region B remains internally healthy on E; retired credential succeeds only in B — no global NORMAL;
2. regions report nearly identical UTC but different admitted retirement floors — time agreement does not hide authority split;
3. load balancer retries a denied retired credential into a stale permissive region — retry cannot become authority selection;
4. PITR-restored region boots with valid-looking old source configuration and E-1 while independent floor says E+1 — region remains stale/quarantined;
5. compromised source S signs/authenticates traffic for proposed successor S2 without independent recovery-policy admission — S2 not promoted;
6. successor source is independently admitted and healthy, but one enforcement region still accepts old epoch — recovery incomplete;
7. long-offline iPad reconnects after E→E+3 and source replacement; unique local records survive while stale authority is rejected and queue is re-admitted;
8. all retired-epoch negative probes fail because a region is entirely unavailable; paired current-authority positive probe prevents false convergence PASS.

Campaign status: **DEFINED, NOT EXECUTED**. Provider/IAM/time topology, regional routing, server clocks, physical iPad/Safari/Home Screen, AT, human and canonical product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Browser clocks, Service Worker lifecycle and local storage can preserve observations and work, not global floor authority. Exact target-runtime behavior remains implementation evidence.

### E → B
B consumes explicit split/stale/quarantine/re-admission states. UX must distinguish preserved local data from unavailable remote authorization and avoid implying data loss.

### E → C
C receives paired positive/negative regional convergence oracles, split-routing cases, restored-node anti-rollback and offline-client forward-convergence cases.

### E → D
D can detect disagreement and measure recovery coverage but cannot elect the current epoch/source.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN. This artifact defines semantics/requirements, not interaction styling.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage with no specialist Foundation PASS. Exact regional topology, time-source clients, floor storage/distribution, routing behavior, token validation, PWA queues, WebKit timers and positive/negative authorization tests remain implementation/runtime dependencies.

## MINTTAP DECISION / DIRECTION

1. Treat temporal/currentness epoch issuance, admission, distribution, observation and enforcement as separate states.
2. Never use region count, local clock health, telemetry consensus or availability-biased routing to elect authority during split-brain.
3. Once a floor is admitted, ordinary outage/restore cannot lower it.
4. Reconstitute a compromised time source only through current independent-enough policy/recovery authority; the compromised source cannot unilaterally authorize its successor.
5. Require scoped paired retired-authority negative and current-authority positive oracles before claiming enforcement convergence.
6. Preserve unique offline PWA data across missed epochs; re-admit remote work under current authority without rewriting historical uncertainty.
7. Keep actual source count, providers, regions, floor representation, tolerance, routing, lease policy and recovery authority OPEN until canonical runtime evidence exists.

## OPEN / VALIDATION

- actual MintTap/LogMate region/resource-server/RP topology;
- actual server time-source hierarchy, NTS/other secure-time support and failure-domain independence;
- actual temporal/currentness floor representation and storage;
- floor distribution/acknowledgement/enforcement mechanism;
- actual routing/load-balancer retry behavior during partial split;
- actual authentication/session/token/lease model and validation path;
- actual PITR/restored-node anti-rollback behavior;
- WebKit/iPadOS clock/sleep/background/restart behavior;
- offline queue and Service Worker retry semantics;
- physical-device, managed-EFB, AT, human, safety/legal/aviation validation.

## VALIDATION / GATE

**PASS (generic).** The Web Manager can now distinguish temporal/currentness epoch issuance/admission/distribution/enforcement, diagnose cross-region time/floor split-brain without availability-biased election, define source-reconstitution admission that does not trust the compromised source to authorize its successor, and specify forward convergence for long-offline PWAs. Product/runtime validation remains OPEN.

## Next highest-value adjacent question

**204 — temporal-floor witness independence, stale-distribution replay & partition-heal ordering.** Determine how a floor/witness can prove enough independence without becoming a unilateral super-root; how replayed but authentic distribution messages are rejected after partitions/restores; how concurrent E+1/E+2 observations are ordered without wall-clock election; and how regions/PWA clients heal a partition without transiently re-enabling retired authority.