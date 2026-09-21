# 201 — PWA Degraded-Authorization Lease Provenance, Trusted-Time Dependence & Partition-Duration Uncertainty

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime clocks and disconnected mechanics; Track B uncertain-boundary/offline-state semantics; Track C destructive time/partition assurance; Track D privacy-bounded timing telemetry.  
Dependencies: 171–200, especially 199–200.

## Problem

200 established that a partial revocation/currentness-plane outage cannot extend the lifetime, scope, privilege or generation of previously trustworthy authorization. The adjacent problem is temporal: **how does an enforcement domain know that a previously admitted authorization lease is still inside its bound when its wall clock may drift, jump, be user-adjusted or attacker-influenced, and when the network partition prevents fresh authoritative currentness evidence?**

A timestamp is not automatically trusted time. A signed server `expires_at` proves what the issuer stated, but a verifier still needs a sufficiently trustworthy temporal basis to determine whether that deadline has passed. A local monotonic elapsed-time source can be useful for measuring duration inside one live runtime epoch, but it does not by itself establish UTC, survive reboot, prove time across suspension, or establish server authority. A browser/PWA wall clock is particularly unsuitable as an independent authorization oracle.

Central rule: **a lease has provenance only when the system can identify who issued the bound, what authority/floor/scope it binds, what temporal basis the verifier used, and what uncertainty applies. Loss of trustworthy temporal evidence cannot lengthen the lease.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns browser wall-clock/elapsed-time/runtime-lifecycle mechanics and the fact that Service Worker, page and storage state do not create authoritative server time. Exact WebKit/Chromium clock/suspension semantics require implementation/runtime validation.
- **B UX/IA/Content:** very high dependency pressure. Owns semantics for `LOCAL-ONLY`, `BOUND VERIFIED`, `BOUND UNCERTAIN`, `RE-ADMISSION REQUIRED`, `QUARANTINED` and recovery messaging, while Design Studio owns reusable interaction treatment.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns wall-clock jump, drift, reboot/suspension, partition-edge, stale-cache, restore and positive/negative authorization tests. Physical iPad/Safari/Home Screen, AT and human validation remain OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Timing/outage telemetry can diagnose duration and recovery coverage but is not an authorization clock or currentness oracle.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns lease provenance, authoritative-time dependency, uncertainty accounting, anti-extension and recovery/admission rules.

## SOURCE

### RFC 7519 — expiration is evaluated against current time

RFC 7519 §4.1.4 defines `exp` as the time on or after which a JWT must not be accepted; processing requires current date/time to be before `exp`. It permits only small leeway for clock skew. `iat` identifies issue time and may be used to determine token age. JWT is used here only as a standards example of a time-bounded credential, not as evidence that MintTap/LogMate uses JWT.

Source: https://www.rfc-editor.org/rfc/rfc7519.html

**TRANSFER VALIDATION:** a cryptographically authentic expiry statement still depends on the verifier's current-time basis. Clock-skew allowance is an explicit bounded tolerance, not permission to renew a lease during a partition.

### NIST SP 800-53 Rev.5 / SP 800-53A Rev.5 — synchronized time is a security dependency and must be assessed

SP 800-53 SC-45 requires synchronization of clocks within/between system components. SC-45(1) adds comparison with an organization-defined authoritative time source and resynchronization beyond a defined difference; SC-45(2) provides for a geographically separate secondary authoritative source. AU-8 notes that time service can be critical to access control, identification and authentication. SP 800-53A includes explicit examination/testing objectives for the synchronization mechanism.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf

**TRANSFER VALIDATION:** trusted time is not merely logging hygiene when authorization expiry depends on it. MintTap-specific synchronization granularity, source hierarchy and failover topology remain OPEN.

### RFC 5905 — authenticated time and correct time are distinct

RFC 5905 defines NTPv4 and explicitly discusses the circular dependency between time synchronization and cryptographic validity. Its security considerations note that authentication of an NTP server/message does not by itself guarantee that the time is correct; clients use multiple associations/selection logic to mitigate false time sources. RFC 5905 has subsequent updates and its legacy authentication details must not be copied blindly.

Source: https://www.rfc-editor.org/info/rfc5905/

**TRANSFER VALIDATION:** `time response authentic ≠ time value correct`. A production trusted-time design requires its own source/failure-domain/threat analysis rather than treating one authenticated timestamp as an infallible oracle.

## SYNTHESIS 1 — separate four temporal questions

For authorization decisions, distinguish:

1. **Issuer time statement:** what issue/expiry/not-before values did the authority bind into the credential/lease?
2. **Verifier wall time:** what civil/UTC time does the enforcement component currently believe?
3. **Elapsed duration:** how much time has elapsed since a trusted observation within a particular runtime/boot epoch?
4. **Uncertainty bound:** how wrong could the verifier's temporal estimate plausibly be under the admitted time-source/synchronization evidence?

Collapsing these creates false certainty. A valid signature protects the issuer's statement from modification; it does not prove the verifier's clock. A monotonic timer can resist ordinary wall-clock jumps for elapsed duration inside its supported epoch; it does not establish UTC or continuity across every reboot/suspension/platform lifecycle.

Persistent guards:
- `signed expiry ≠ trustworthy current time`;
- `authenticated time source ≠ correct time guaranteed`;
- `wall clock available ≠ wall clock trustworthy`;
- `monotonic elapsed time ≠ authoritative UTC`;
- `client clock later ≠ server lease expired with proven chronology`;
- `client clock earlier ≠ server lease still valid`.

## SYNTHESIS 2 — lease provenance is more than an expiry timestamp

A reusable degraded-authorization lease record should conceptually bind at least:

- issuer/authority identity and admitted policy/currentness generation;
- subject/session/credential lineage where applicable;
- resource and operation scope;
- issuance/currentness observation identifier;
- absolute expiry or maximum duration semantics, if defined;
- verifier observation point and temporal basis;
- allowed clock-skew/uncertainty policy;
- refresh/reissue prohibition or rules;
- consequence class;
- whether use is local-only, deferred or remotely effective;
- recovery/re-admission requirements.

This is a generic reasoning model, not a proposed MintTap schema.

**MINTTAP DIRECTION:** do not make `Date.now()` or an iPad's displayed clock the authority for whether a remote consequence-bearing queue item is currently authorized. Product implementation remains a Software Engineering dependency.

## SYNTHESIS 3 — uncertainty consumes the safe side of the lease

If current time is only known within an uncertainty interval, security-sensitive expiry must not choose the optimistic edge merely to preserve availability.

Conceptually, if a verifier can only establish that current time lies in `[t_low, t_high]` and an authorization expires at `T_exp`:

- if `t_high < T_exp`, expiry may still be inside the proven bound, subject to all other policy conditions;
- if `t_low >= T_exp`, it is expired;
- if the interval straddles `T_exp`, temporal validity is **UNCERTAIN**, not automatically valid.

The exact uncertainty model and consequence policy are implementation/product decisions. The key invariant is that uncertainty cannot be converted into extra authority.

`clock uncertainty overlaps expiry ≠ authorization valid`.

For high-consequence remote mutation, unresolved temporal uncertainty normally requires re-admission/current evidence rather than optimistic execution. Lower-consequence behavior may have a separately approved bounded policy, but that policy must be explicit and must not reset the original bound.

## SYNTHESIS 4 — wall-clock jumps and monotonic elapsed time solve different problems

A local wall clock can move because of synchronization correction, user changes, timezone presentation errors, restore/VM behavior or attack. Therefore lease-age calculations based only on repeated wall-clock subtraction can be unsafe.

A monotonic elapsed-time source, where the platform guarantees appropriate semantics, is useful for measuring elapsed duration without ordinary wall-clock rollback. But it has boundaries:

- it may be scoped to a boot/runtime epoch;
- exact suspend/sleep/background semantics are platform/API specific;
- persistence across process death/reboot cannot be assumed;
- restoring a persisted monotonic counter value does not recreate the original clock epoch;
- it cannot prove UTC/current server generation.

**DEPENDENCY — Track A / Software Engineering:** exact JavaScript/WebKit/Chromium timer behavior, sleep/background/reboot behavior and implementation APIs must be validated in the target runtime before being used for a security claim.

## SYNTHESIS 5 — partition duration is not safely inferred from one endpoint's clock

A partition has at least two relevant boundaries: last trustworthy contact/currentness observation and first trustworthy recovery observation. If either boundary is temporally uncertain, exact partition duration may also be uncertain.

Do not infer `partition lasted N` solely from:
- client-created timestamps;
- queue timestamps;
- Service Worker activation time;
- IndexedDB record time;
- `navigator.onLine` transitions;
- one analytics event stream;
- one restored server's wall clock.

Where the exact duration cannot be proven, preserve an interval/bound or mark it UNKNOWN. The security decision should use the conservative proven information rather than fabricate precision.

Persistent guard: `connectivity event timestamp ≠ authoritative partition boundary`.

## SYNTHESIS 6 — server-issued expiry survives storage; temporal authority does not automatically survive disconnection

A signed/authenticated server lease can be stored offline and remain authentic as an artifact. That preserves **what the server authorized and until what stated bound**. It does not give the offline client an independent trustworthy current-time service.

Therefore:
- artifact authenticity may survive the partition;
- currentness/freshness evidence ages during the partition;
- the client must not refresh or extend the server lease locally;
- if the verifier cannot establish that the lease remains within its admitted temporal bound, remotely consequential authority becomes UNCERTAIN/expired according to policy;
- local preservation can continue independently where safe.

`lease artifact authentic offline ≠ lease currently usable offline for remote authority`.

## SYNTHESIS 7 — reboot, restore and rollback are temporal epoch boundaries

A reboot, browser/process restart, device restore, VM snapshot/PITR or storage rollback can break assumptions that were valid within a prior elapsed-time epoch. A persisted `last_seen_monotonic=...` value cannot be treated as if it belongs to the new epoch without a platform-proven continuity mechanism.

After such a boundary, an enforcement domain must either:
- re-establish trusted temporal/currentness evidence;
- use another independently valid bound whose semantics survive the boundary; or
- classify the affected authorization as requiring re-admission/UNKNOWN.

PITR is especially dangerous because data can look internally consistent while time/currentness state has moved backward. Existing anti-rollback retirement/currentness floors from 171–200 still apply.

`restored lease record ≠ restored trustworthy lease age`.

## SYNTHESIS 8 — offline operations near the lease boundary are data first, authority later

For a LogMate/EFB-like PWA, an operation created while offline near an uncertain authorization boundary should not be discarded merely because its authorization cannot be proven. Preserve the domain data and provenance separately from the authority decision.

Classify at least conceptually:
- **local record/data:** preserve if locally valid and irreplaceable;
- **local intent:** preserve with provenance/idempotency metadata where applicable;
- **remote admission:** pending until current server authority evaluates it;
- **historical claim that it was authorized at creation time:** only assert if the required temporal/currentness evidence actually proves that fact.

If an operation's creation time lies in an uncertainty interval crossing the lease boundary, do not rewrite history as `authorized`. Preserve `BOUNDARY-UNCERTAIN`/equivalent evidence and let current policy determine whether the operation may now be admitted, rejected, transformed or require user/operator review.

**MINTTAP DIRECTION:** unique offline flight/logbook data must survive authorization quarantine. Current server admission after reconnect must not silently mutate uncertain historical authorization into a false claim that the old lease was valid at creation time.

## SYNTHESIS 9 — recovery requires time/currentness rebootstrap before NORMAL

After connectivity/time service/currentness recovery:

1. preserve unique local data and original timing/provenance observations;
2. obtain authenticated current server/policy/retirement floor;
3. re-establish acceptable time-source/synchronization evidence for enforcement domains that rely on time;
4. detect clock jumps/rollback and invalidate assumptions tied to superseded temporal epochs;
5. reevaluate retained credentials/leases against current policy;
6. run retired/expired-authority negative probes and current-authority positive probes on consequential paths;
7. re-admit queued operations under current authority;
8. keep historical `BOUNDARY-UNCERTAIN` facts distinct from current admission outcome;
9. promote an enforcement domain to NORMAL only when scoped currentness/time/enforcement evidence supports it.

`time service recovered ≠ authorization convergence complete`; `clock synchronized now ≠ past boundary uncertainty retroactively resolved`.

## SYNTHESIS 10 — trusted time is itself a dependency graph

A time-dependent authorization system inherits failure modes from:
- time source(s);
- source authentication/integrity;
- network path;
- synchronization daemon/runtime;
- host/VM/device clock;
- browser/runtime API semantics;
- clock monitoring and drift thresholds;
- regional failover;
- restore/snapshot lifecycle;
- policy defining acceptable uncertainty.

NIST SC-45's primary/secondary authoritative-source framing is useful precedent for avoiding an unexamined single source, but exact architecture is product/infrastructure specific.

**CONTRADICTION:** adding a time server does not eliminate time trust. It adds a dependency whose correctness, independence, availability and compromise behavior must be understood.

## Track C destructive campaign — 368 cases total

Add eight high-value cases to the 360-case campaign:

1. client wall clock is manually moved backward before cached authorization expiry; remote authority must not gain extra lifetime;
2. client wall clock jumps forward and back across expiry; unique local data survives while remote authorization state does not oscillate into renewed validity;
3. verifier's uncertainty interval straddles expiry; high-consequence remote mutation is not optimistically admitted;
4. process/browser restart destroys the prior monotonic epoch while persisted lease metadata remains; verifier must not reuse stale elapsed-time assumptions as proof;
5. device sleeps/backgrounds across the lease boundary; target-runtime test must establish timer semantics rather than assume them;
6. PITR restores pre-expiry authorization/cache and old clock-sync state; current retirement floor/time evidence prevents resurrection;
7. reconnect establishes current authority but cannot reconstruct exact historical partition boundary; current operation may be re-admitted without rewriting historical `BOUNDARY-UNCERTAIN` evidence;
8. all expired-authority probes fail because the service is unavailable while current-authority probes also fail; no false convergence PASS.

Campaign status: **DEFINED, NOT EXECUTED**. Exact provider/IAM, server clock, browser timer, physical iPad/Safari/Home Screen, AT, representative-human and canonical product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Browser/runtime clocks and offline storage can retain observations, not manufacture server currentness. Exact timer/suspension semantics are implementation evidence, not generic assumptions.

### E → B
B receives distinct semantics for `BOUND VERIFIED`, `BOUND UNCERTAIN`, `LOCAL-ONLY`, `RE-ADMISSION REQUIRED` and current admission. Historical uncertainty must not be hidden by a successful later sync.

### E → C
C must test clock rollback/forward jumps, skew thresholds, sleep/background, process death/reboot, restore/PITR, partition edges and paired positive/negative authorization oracles.

### E → D
D may record coarse partition/recovery timing for diagnostics but analytics timestamps are observation evidence, not trusted authorization time.

### Design Studio dependency
Canonical Design Studio Web status remains W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN; Web Manager does not invent interaction treatment here.

### Software Engineering dependency
Canonical Software Engineering Studio remains Foundation study underway with no specialist Foundation PASS. Exact server/client clock APIs, monotonic-clock persistence boundaries, WebKit/Chromium timer semantics, token validation, region synchronization and fault injection require implementation/runtime evidence there or in the product repository.

## OPEN

- actual MintTap/LogMate identity/token/session architecture and whether JWT/OAuth exists at all;
- actual authorization lease model, if any;
- actual server time-source hierarchy, synchronization/monitoring thresholds and regional failure domains;
- actual provider token expiry/skew semantics;
- actual operation consequence classes and acceptable uncertainty;
- exact JavaScript/WebKit/Chromium/iPadOS timer behavior across sleep/background/process death/reboot;
- actual Service Worker/background queue credential behavior;
- actual managed-iPad time-management/MDM constraints;
- actual PITR/VM/container time behavior;
- aviation/legal/safety requirements affecting offline authorization;
- human/AT comprehension of boundary-uncertain versus currently admitted states.

## CHANGE WATCH

- WebKit/iPadOS PWA background/suspension/timer behavior;
- Chromium/browser timer implementation changes relevant to target runtime;
- provider-specific expiry/skew/revocation semantics;
- NTP standards updates and deployed secure-time practices;
- NIST SP 800-53 control-catalog updates.

## Gate judgment

**PASS (generic).** The Web Manager can now reason about time-bounded degraded authorization without treating a client wall clock, signed expiry, monotonic timer or connectivity timestamp as a complete currentness oracle; distinguish issuer statement, verifier wall time, elapsed duration and uncertainty; preserve offline data across uncertain lease boundaries; and require forward time/currentness rebootstrap without retroactively laundering historical uncertainty.

This is not production certification. Product/provider/time-service/runtime/managed-iPad/safety/legal/privacy/human evidence remains OPEN.

## Adjacent-value check and next highest-value target

The directly adjacent high-value question is **trusted-time source compromise, clock-rollback detection & temporal-epoch succession across restore/reboot**. The next cycle should determine how a system reacts when the time source itself is malicious or correlated with the compromised control plane; how rollback/forward-jump evidence is preserved without making one clock authoritative; how temporal epochs are superseded after reboot/restore; and how current authorization can recover without falsely reclassifying operations whose historical timing remains unprovable.