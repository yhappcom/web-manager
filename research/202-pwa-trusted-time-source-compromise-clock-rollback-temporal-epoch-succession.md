# 202 — PWA Trusted-Time Source Compromise, Clock-Rollback Detection & Temporal-Epoch Succession

Status: **PASS (generic) / PRODUCT + TIME-TOPOLOGY + IDENTITY + PROVIDER + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime clock and lifecycle mechanics; Track B temporal-uncertainty/recovery semantics; Track C destructive time/restore assurance; Track D privacy-bounded timing telemetry.  
Dependencies: 171–201, especially 199–201.

## Problem

201 established that an authentic expiry statement still needs a sufficiently trustworthy temporal basis and that reboot/restore/process changes can break elapsed-time assumptions. The adjacent problem is stronger: **what if the time source itself is malicious, stale, delayed, correlated with the compromised control plane, or rolled backward together with application state?**

A secure time transport can authenticate who sent a time statement and protect it from modification/replay, but it cannot make a compromised or incorrect source truthful. Likewise, a local monotonic clock can help detect some elapsed-time anomalies inside one admitted runtime epoch but cannot prove UTC, survive arbitrary restore, or independently establish server authorization.

Central rule: **time is security evidence with provenance, uncertainty and an epoch; it is not a universal oracle. A temporal epoch may advance only from evidence that is admissible under the current trust/currentness policy, and a new epoch must not retroactively legitimize operations whose historical timing remains unprovable.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns the distinction among civil wall time, monotonic/elapsed clocks, browser/runtime lifecycle and persisted observations. Exact WebKit/Chromium suspend/reboot/timer semantics remain runtime evidence.
- **B UX/IA/Content:** very high dependency pressure. Owns comprehensible semantics for `TIME-VERIFIED`, `TIME-UNCERTAIN`, `EPOCH-SUPERSEDED`, `LOCAL-ONLY`, `RE-ADMISSION REQUIRED` and historical uncertainty without implying data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns malicious/stale source, rollback, forward jump, split-source, reboot, restore and post-recovery positive/negative authorization tests. Physical-device, AT and human validation remain OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Telemetry can expose clock/source disagreement and recovery coverage but cannot decide authorization currentness.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns source trust/failure-domain analysis, anti-rollback floors, temporal-epoch admission/succession and recovery convergence.

## SOURCE

### RFC 8915 — Network Time Security authenticates NTP exchanges but does not turn one source into an infallible clock

RFC 8915 specifies Network Time Security (NTS) for NTP client-server mode. Its objectives include server identity, packet authentication, replay prevention and request-response consistency. Its security considerations also discuss delay attacks, compromised server-cookie keys, use of multiple time sources/network paths as mitigation, and NTS-stripping risk. It explicitly recommends against silently falling back from NTS-protected to unprotected NTP without explicit user action.

Source: https://www.rfc-editor.org/rfc/rfc8915.html

**TRANSFER VALIDATION:** authenticated time transport improves provenance and anti-replay; it does not prove that the authenticated source's time is semantically correct or independent of a compromised control plane. A failure of secure time must not silently downgrade to weaker time and thereby extend authorization.

### NIST SP 800-53 Rev.5 / SP 800-53A Rev.5 — time synchronization is a governed security dependency

SC-45 treats clock synchronization as a system security dependency; enhancements include comparison with an organization-defined authoritative source and a geographically separate secondary source. Assessment objectives in SP 800-53A require examining/testing the synchronization mechanism rather than merely asserting that it exists.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** independent-enough sources and assessment matter when time participates in authorization. The exact MintTap/LogMate source hierarchy, acceptable uncertainty, synchronization interval and failure domains remain OPEN.

### RFC 5905 — source selection and correctness are distinct from authentication

RFC 5905's NTP model uses multiple associations, selection/combining logic and distance/error concepts rather than treating any received timestamp as absolute truth. Its security discussion distinguishes authentication from guaranteed correctness and exposes circular dependencies between time and cryptographic validity.

Source: https://www.rfc-editor.org/rfc/rfc5905.html

**TRANSFER VALIDATION:** source agreement/selection is evidence, not proof of universal correctness; correlated sources can fail together.

### Roughtime remains CHANGE WATCH, not a current production baseline

`draft-ietf-ntp-roughtime-18` (16 March 2026) describes an experimental protocol intended to provide rough secure time even to clients without an initial time estimate and to produce evidence of inconsistencies between time servers. The Internet-Draft expired on 17 September 2026 and is not an RFC/final standard.

Source: https://www.ietf.org/archive/id/draft-ietf-ntp-roughtime-18.html

**CHANGE WATCH:** useful conceptual precedent for inconsistency evidence, but do not prescribe Roughtime for MintTap/LogMate or treat the expired draft as normative current deployment guidance.

## SYNTHESIS 1 — separate source authenticity, source correctness, source independence and source freshness

A time observation has at least four distinct security properties:

1. **authenticity/integrity** — did it come from the claimed source without modification/replay?
2. **correctness/accuracy** — is the claimed time sufficiently close to the required reference for the decision?
3. **independence** — can the source fail or be compromised independently of the application/control-plane authority it is meant to constrain?
4. **freshness/currentness** — is this observation recent enough under the admitted policy to support the present decision?

Persistent guards:
- `authenticated time ≠ correct time`;
- `correct-looking time ≠ independent time`;
- `multiple endpoints ≠ multiple failure domains`;
- `fresh packet ≠ fresh authority generation`;
- `secure transport ≠ trustworthy source semantics`.

A set of three hostnames behind one provider/account/control plane may still be one correlated failure domain. Conversely, source disagreement is incident evidence; it is not permission to choose whichever source preserves availability.

## SYNTHESIS 2 — source compromise cannot be repaired by majority count alone

If sources disagree, simple majority is not generically sufficient. A majority can share the same compromised upstream, administrator, DNS/control plane, network path or restored snapshot. The decision must consider admitted source identity, provenance, failure-domain independence, uncertainty/error bounds and current policy.

A reusable classification is:
- `ADMISSIBLE-CONSISTENT` — current admitted source evidence is mutually compatible within required bounds;
- `ADMISSIBLE-DIVERGENT` — admitted sources conflict beyond policy tolerance;
- `STALE` — authentic but outside freshness/currentness bounds;
- `UNTRUSTED` — source/path is not admitted for the decision;
- `UNKNOWN` — evidence is insufficient to classify safely.

`majority time ≠ authoritative time`.

For consequence-bearing remote authorization, unresolved `ADMISSIBLE-DIVERGENT`/`UNKNOWN` time normally prevents promotion to NORMAL. Local preservation remains separable.

## SYNTHESIS 3 — clock rollback/forward jump is evidence, not self-interpreting proof

A verifier can observe discontinuities between:
- current wall clock and last admitted wall-clock observation;
- wall-clock delta and monotonic elapsed delta inside the same proven epoch;
- local clock and one or more admitted external sources;
- regional clocks/currentness floors;
- restored state and independently surviving anti-rollback evidence.

A backward jump can indicate synchronization correction, user action, VM/device restore, stale snapshot or attack. A forward jump can cause premature expiry or misleading chronology. Therefore detection should preserve the observation and invalidate affected assumptions; it should not invent a cause without evidence.

Persistent guards:
- `clock rollback detected ≠ attacker proven`;
- `clock rollback not detected ≠ rollback impossible`;
- `forward jump ≠ real elapsed duration proven`;
- `clock corrected now ≠ prior chronology repaired`.

## SYNTHESIS 4 — temporal epochs need explicit admission and succession

A **temporal epoch** is the bounded context in which a verifier's elapsed-time/current-time assumptions are admitted as mutually meaningful. Epoch identity is conceptual, not a required product field.

Events that may require a new epoch include reboot, process/runtime restart where timer continuity is not guaranteed, VM/device restore, PITR, time-source trust-policy change, detected rollback beyond tolerance, or loss/recovery of trusted-time evidence.

Generic succession:
1. preserve prior epoch observations and unresolved uncertainty;
2. freeze or downgrade consequence-bearing operations whose temporal proof depends on the superseded epoch;
3. obtain current authenticated policy/currentness floor;
4. obtain admissible time-source evidence under that policy;
5. compare against independently surviving anti-rollback/currentness evidence;
6. admit a new temporal epoch with explicit uncertainty/freshness bounds;
7. reevaluate retained credentials/leases for **current** use;
8. re-admit queued remote work under current authority;
9. never rewrite historical uncertain timing merely because the new epoch is healthy.

Persistent guard: `new temporal epoch admitted ≠ old temporal uncertainty resolved`.

## SYNTHESIS 5 — anti-rollback needs a floor outside the rollback domain

If application state, authorization cache and time evidence are restored together from the same snapshot, they can be internally consistent yet collectively stale. A rollback-resistant design therefore needs some currentness/retirement/epoch evidence that survives in an independent-enough failure domain, consistent with the continuity-floor work in 171–200.

The surviving floor need not itself tell exact UTC. It can establish a monotonic security fact such as `policy/currentness generation must be >= G` or `temporal epoch E0 is retired`. This prevents an old snapshot from becoming current merely because its own clock and credentials agree with each other.

`anti-rollback floor ≠ trusted UTC`; `trusted UTC ≠ anti-rollback floor`.

Both may be needed for a time-bounded authorization claim.

## SYNTHESIS 6 — secure-time fallback must not become security downgrade

RFC 8915's NTS-stripping discussion provides a useful generic warning: when the stronger time channel fails, automatically falling back to an unauthenticated/weaker source can let an attacker convert availability pressure into a security downgrade.

Generic rule:
- loss of the admitted time source/channel may move an enforcement domain to `TIME-UNCERTAIN`, `DEGRADED-BOUNDED`, `LOCAL-ONLY` or `RE-ADMISSION REQUIRED`;
- it does not automatically authorize a weaker source;
- any fallback source must already be admitted by policy with its own provenance, uncertainty and failure-domain analysis;
- fallback cannot extend an existing authorization bound.

`primary time unavailable ≠ weaker time automatically admissible`.

## SYNTHESIS 7 — current recovery and historical truth are separate

After source compromise or rollback, a system can often restore **current** authorization safely without proving exact historical UTC for every offline operation. That distinction is essential for LogMate/EFB-like workflows.

For each affected operation preserve separately:
- domain data and user intent;
- observed client/local timestamp(s);
- temporal epoch/source evidence available at creation;
- whether historical authorization was proven, disproven or `UNKNOWN/BOUNDARY-UNCERTAIN`;
- current re-admission outcome after recovery.

A later server acceptance means `admitted now under current policy`; it does not necessarily mean `old lease was valid when created`.

`current re-admission PASS ≠ historical authorization PASS`.

## SYNTHESIS 8 — LogMate/EFB offline iPad remains a data-preserving client, not a secure-time authority

A company iPad may have a user-visible clock, platform synchronization and browser/runtime timers, but generic Web Manager knowledge cannot elevate any of those into an independent server-security oracle. Exact managed-iPad, iPadOS/WebKit, MDM, sleep/background and clock-setting behavior remains runtime/provider evidence.

For a long-offline PWA that reconnects after a time-source compromise or epoch change:
1. preserve unique local flight/logbook records before authorization cleanup;
2. quarantine cached time/currentness/session claims from remote authority;
3. obtain current authenticated server policy/currentness/retirement floor;
4. establish an admitted new temporal basis where required;
5. keep old operation timestamps/provenance as observations, not rewritten truth;
6. re-admit remote queue items under current authority;
7. surface unresolved historical timing only where product/safety/legal semantics require it.

No assumption is made that direct unattended device-to-device sync, background execution or persistent secure time exists on iPadOS.

## SYNTHESIS 9 — telemetry can detect contradiction but cannot close it alone

Track D timing telemetry can be valuable for:
- source disagreement;
- regional clock offset/drift;
- rollback/forward-jump events;
- epoch transitions;
- time-service outage/recovery;
- queue items created in uncertain intervals.

But analytics timestamps may themselves inherit the same clock problem. Telemetry is therefore observation evidence with provenance, not the authorization clock. Privacy/data-minimization constraints still apply; do not retain unnecessary user/device detail merely to improve time diagnostics.

`telemetry agrees ≠ authority proven`; `telemetry disagrees ≠ data may be discarded`.

## SYNTHESIS 10 — recovery convergence requires both temporal and authorization oracles

A scoped promotion from degraded/uncertain state to NORMAL should require, where applicable:
- current admitted policy/currentness floor;
- admissible time-source set and source/failure-domain status;
- acceptable uncertainty/freshness evidence;
- new temporal epoch admitted after rollback/restore when needed;
- retired/expired authority negative probes;
- current authority positive probes;
- region/resource-server/RP convergence;
- PITR/restored-node anti-rollback reconciliation;
- offline PWA forward rebootstrap and queue re-admission.

A healthy time service is not sufficient if enforcement still accepts retired authority; healthy authorization is not sufficient to prove historical timestamps.

`time convergence ≠ authorization convergence`; `authorization convergence now ≠ historical chronology complete`.

## Track C destructive campaign — 376 cases total

Add eight high-value cases to the 368-case campaign:

1. an authenticated primary time source is maliciously shifted backward while a secondary admitted source disagrees; no silent availability-biased source selection;
2. three apparent sources share one compromised upstream/control plane and agree on false time; endpoint majority is not treated as independence proof;
3. NTS-protected source becomes unavailable and a network attacker blocks recovery; client does not silently fall back to unauthenticated NTP to preserve authorization;
4. wall clock rolls backward while monotonic elapsed time continues in the same proven runtime epoch; affected lease cannot gain lifetime;
5. device/server reboot destroys monotonic continuity and starts a new epoch; persisted old elapsed values are not reused as current proof;
6. PITR restores application DB, authorization cache and clock state together while an independent currentness/epoch floor is newer; stale snapshot cannot re-enter NORMAL;
7. new temporal epoch and current authority are successfully admitted after reconnect, but an offline operation's historical timing remains unprovable; current re-admission does not rewrite history;
8. time service and authorization service both appear healthy after recovery, but one region still enforces a retired epoch/floor; no global convergence PASS.

Campaign status: **DEFINED, NOT EXECUTED**. Exact provider/IAM, server clock discipline, NTS/time topology, browser timers, physical iPad/Safari/Home Screen, AT, representative-human and canonical product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Browser/runtime clocks provide platform observations. Exact timer continuity, suspend behavior and device clock controls require target-runtime evidence before supporting a security claim.

### E → B
B consumes distinct semantics for current recovery versus historical uncertainty. A successful reconnect must not present an uncertain old operation as if its original authorization/timing were proven.

### E → C
C receives explicit source-compromise, rollback, fallback-downgrade, epoch-succession and restore cases plus paired positive/negative authorization oracles.

### E → D
D may observe source/epoch disagreement and recovery coverage but must not convert analytics chronology into authority.

### Design Studio dependency
Design Studio remains canonical for interaction treatment. Current `progress/WEB_STATUS.md` is W121 / Stage 3 PRACTICE / NOT PASSED with physical-device/PWA, screen-reader and representative-human evidence OPEN. This study defines states/requirements only.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage with no specialist Foundation PASS. Exact clock APIs, server synchronization, WebKit/Chromium timer continuity, secure-time client support, regional source topology, persisted epoch identifiers/floors, queue behavior and product authorization tests remain implementation/runtime evidence.

## MINTTAP DECISION / DIRECTION

1. Treat trusted time as a dependency graph with source provenance, freshness, uncertainty and failure-domain analysis; do not define one clock as an infallible oracle.
2. Do not let secure-time outage silently downgrade to weaker time or extend authorization.
3. Preserve independent-enough monotonic security/currentness floors across restore; do not confuse them with exact UTC.
4. Treat reboot/restore/rollback or material time-trust change as temporal-epoch boundaries when continuity cannot be proven.
5. Preserve unique offline data across temporal quarantine; separate historical timing/authorization evidence from current re-admission.
6. Keep product-specific source count, provider, uncertainty thresholds, fallback rules, lease duration and consequence policy OPEN until canonical architecture/runtime evidence exists.

## OPEN / VALIDATION

- actual MintTap/LogMate authentication/token/session/lease model;
- server/region/managed-device time sources and synchronization topology;
- whether any NTS or equivalent secure-time mechanism is deployed;
- source administrative/network/provider failure-domain independence;
- exact acceptable uncertainty/skew and consequence classification;
- WebKit/iPadOS/MDM wall-clock and monotonic-timer behavior across sleep/background/reboot/restore;
- persistence/anti-rollback mechanism for temporal/currentness floors;
- legal/aviation requirements for event timestamps and historical chronology;
- physical-device, security/privacy, AT and representative-human validation.

## CHANGE WATCH

- NIST SP 800-53/53A updates affecting time synchronization controls/assessment;
- NTP/NTS implementation and deployment guidance;
- `draft-ietf-ntp-roughtime` status after draft-18 expiry on 2026-09-17;
- WebKit/iPadOS clock/timer/background/restore behavior;
- provider secure-time and global authorization/revocation semantics.

## Gate result

**202 generic gate: PASS.**

Reason: the Web Manager can now distinguish secure transport from correct/independent time, analyze correlated source compromise, detect rollback without overclaiming cause, define temporal-epoch succession after reboot/restore, combine time evidence with independent anti-rollback floors, prevent fallback downgrade, preserve uncertain historical provenance, and recover current authorization without laundering old timing uncertainty.

Production/device/runtime validation remains OPEN.

## Next highest-value adjacent work

**203 — Temporal-Epoch Floor Distribution, Cross-Region Time Split-Brain & Recovery Admission Under Source Reconstitution.**

Focus: how a newly admitted temporal/currentness epoch is distributed without one region advancing while another remains on a stale but internally consistent time basis; how split-brain time/currentness evidence is detected and quarantined; how reconstituted time sources are admitted after source compromise without trusting the compromised source to authorize its own successor; and how offline PWA clients converge across that transition without treating cached time as authority.