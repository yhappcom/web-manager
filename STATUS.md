# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-21

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Curriculum completion is not production certification. Detailed guards and studies live in `research/README.md` and numbered research artifacts. Five specialist tracks remain mandatory; Web Manager coordinates rather than acting as a sixth specialist.

## Continuous expert maintenance
083–170 — **PASS at recorded generic gates.**  
171–200 — **PASS (generic)** across federation/currentness, recovery authority, constitutional policy/governance keys, exact-artifact supply chain, transparency, preservation/portability/escrow, custody anti-rollback, continuity admission/conflict/floor retirement, policy/key succession/reconstitution, break-glass lifecycle, emergency identity/custody, material/session invalidation, orphaned-authority discovery, revocation convergence and degraded authorization under partial revocation-plane outage.  
201 PWA Degraded-Authorization Lease Provenance, Trusted-Time Dependence & Partition-Duration Uncertainty — **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**.

## 171–201 integrated checkpoint
- Authority, evidence, observation and convergence remain separate layers. Offline-first utility preserves unique local data without making stale authority current.
- Continuity generation issuance, admission, distribution and recovery effectiveness are distinct; conflicting valid-looking heads are incident evidence, not majority elections.
- Currentness floors survive ordinary control-plane loss in an independent-enough failure domain but remain rollback evidence rather than unilateral authority.
- Reconstitution/break-glass authority is exceptional, incident-bound, scoped and extinguishable; recovery completion requires negative authorization evidence across applicable API/session/region/PITR paths.
- Emergency-custody succession is an authorization transition, not additive roster maintenance. Material rotation, authenticator invalidation, session invalidation and effective authority extinction are distinct.
- Authority retirement is a convergence claim across explicit consequence-bearing enforcement surfaces. Revocation requested/accepted/observed/enforced are distinct; residual authority is actively revocable, verified bounded-expiry or UNKNOWN.
- Partial revocation/currentness-plane outage is handled per operation and enforcement domain, not by one global fail-open/fail-closed switch. Secure degraded operation may preserve local capability while denying the specific remote action whose required current authorization cannot be established.
- A failure in the mechanism that could supply fresher authorization cannot increase the lifetime, scope, privilege or generation of the last trustworthy authorization evidence. Outage never resets a cache/lease age or lowers an admitted retirement floor.
- **Time-bounded authorization separates issuer time statement, verifier wall time, elapsed duration and uncertainty. A signed expiry, client wall clock, monotonic timer or connectivity event is not by itself a complete currentness oracle.**
- **Temporal uncertainty consumes the safe side of an authorization bound: when the proven time interval straddles expiry, validity is UNCERTAIN rather than optimistically current. Reboot/restore/process-epoch changes invalidate elapsed-time assumptions unless continuity is independently established.**
- **PWA local preservation, local use, deferred intent and remotely effective mutation remain separate. Operations created near an uncertain lease boundary retain their data/provenance without being falsely promoted to historically authorized; reconnect performs current re-admission.**
- Recovery is forward convergence: time/currentness service recovery alone does not prove enforcement convergence, and synchronization now does not retroactively resolve historical boundary uncertainty.

## Persistent guards added through 201
Retain all prior guards, plus: `signed expiry ≠ trustworthy current time`; `authenticated time source ≠ correct time guaranteed`; `wall clock available ≠ wall clock trustworthy`; `monotonic elapsed time ≠ authoritative UTC`; `client clock later ≠ server lease expiry proven`; `client clock earlier ≠ server lease still valid`; `clock uncertainty overlaps expiry ≠ authorization valid`; `connectivity event timestamp ≠ authoritative partition boundary`; `lease artifact authentic offline ≠ lease currently usable offline for remote authority`; `restored lease record ≠ restored trustworthy lease age`; `time service recovered ≠ authorization convergence complete`; `clock synchronized now ≠ past boundary uncertainty retroactively resolved`.

## Five-track state
- **A Platform/Browser:** high dependency supplier; browser session/cookie/SW/Cache Storage/IndexedDB/disconnected mechanics plus wall-clock/elapsed-time/runtime-epoch mechanics support analysis, but client state/time cannot establish server revocation/currentness. Exact WebKit/Chromium sleep/background/reboot timer semantics remain implementation evidence.
- **B UX/IA/Content:** very high dependency pressure; owns NORMAL/DEGRADED-BOUNDED/LOCAL-ONLY/BOUND-UNCERTAIN/RE-ADMISSION REQUIRED/QUARANTINED/UNKNOWN semantics while consuming Design Studio evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure; owns destructive campaigns through 201's **368-case** authority/revocation/outage/time/partition/restore/offline-client campaign. Execution, physical-device, AT and human validation remain OPEN.
- **D Search/Discovery/Analytics:** bounded consumer; timing/outage/recovery telemetry remains observation evidence only and must not become an authorization clock/oracle.
- **E Architecture/Security/Operations:** highest-risk owner; 201 closes the generic lease-provenance, trusted-time-dependence, uncertainty-boundary and partition-duration reasoning gate.

## Cross-repository evidence
Design Studio `progress/WEB_STATUS.md` is **W121 EXECUTION-PRIORITY GATE; Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. Exact-source runtime, independent browser/native, physical-device/PWA, field Core Web Vitals, full WCAG, screen-reader and human UX evidence remain OPEN.

Software Engineering Studio `progress/STATUS.md` is **ACTIVE — FOUNDATION STUDY UNDERWAY** and states no specialist has passed Foundation. Its bounded Android/Chromium/Keystore evidence does not transfer to physical iOS/Safari/EFB or canonical product runtime. Exact server/client clock APIs, monotonic-clock persistence boundaries, WebKit/Chromium timer semantics, token validation, regional time synchronization, revocation/cache convergence, background queues, PITR anti-resurrection and positive/negative authorization tests remain implementation dependencies.

## Production OPEN register
Actual `minttap.app` and LogMate-like production facts remain OPEN unless verified from canonical project/runtime evidence, including managed-iPad/WebKit/MDM behavior; PWA storage/update/background/sync; auth/session/offline authorization; identity/federation/provider/region/control-plane topology; token/session/revocation/cache/lease validity and outage semantics; server trusted-time topology and clock uncertainty; operation consequence classification; queue/retry semantics; recovery/constitutional policy; supply-chain/admission/enforcement; witness/archive/preservation/escrow topology; policy/key hierarchy; currentness-floor topology; reconstitution/emergency identities/custody; backup/PITR/deletion/hold; legal/aviation/safety obligations; and physical-device/security/privacy/human validation.

## Freshness / current external precedent
- NIST SP 800-53 Rev.5 remains current; Release 5.2.0 was issued 2025-08-27. SC-45 treats synchronized system time as a security dependency; SC-45(1)/(2) provide authoritative and secondary-source precedent. SP 800-53A Rev.5 includes assessment objectives for time synchronization. This does not establish MintTap time topology.
- RFC 7519 remains a useful standards example: `exp` is evaluated against current date/time and only small clock-skew leeway is contemplated. This does not establish that MintTap uses JWT.
- RFC 5905 remains the NTPv4 core specification with later updates. Its security analysis distinguishes authenticated timing information from guaranteed-correct time and exposes the circular dependence between time and cryptographic validity. Legacy NTP authentication details are not copied as current design guidance.
- NIST SP 800-207 / current NCCoE ZTA material remains useful precedent for separating policy decision/administration from enforcement. It does not establish MintTap architecture.
- NIST SP 800-63B-4 is the current final authentication/authenticator/session baseline (2025) and distinguishes authenticator lifecycle from independently managed IdP/RP sessions.
- RFC 9700 / BCP 240 (January 2025) remains current OAuth 2.0 Security BCP. RFC 7009 and RFC 7662 remain relevant protocol precedents.
- NIST SP 800-61 Rev.3 was finalized 2025-04-03 and supersedes Rev.2.
- NIST SP 800-209 Rev.1 remains an Initial Public Draft dated 2026-07-22; CHANGE WATCH only.
- NIST SP 800-57 Part 1 Rev.5 remains final; Rev.6 is Initial Public Draft and CHANGE WATCH only.
- WebKit/iPadOS PWA timer/suspension/recovery/session/background behavior, secure-time deployment practices and provider global-sign-out/token-revocation/outage semantics remain CHANGE WATCH.

## Next learning mode
Highest-value adjacent generic work is **trusted-time source compromise, clock-rollback detection & temporal-epoch succession across restore/reboot**: determine how authorization behaves when the time source itself is malicious, stale or correlated with the compromised control plane; how rollback/forward-jump evidence is preserved without elevating one clock into an oracle; how temporal epochs are superseded after reboot/restore; and how current authorization recovers without laundering operations whose historical timing remains unprovable.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–201 PASS** at generic gates.
- Product/device/AT/security/privacy/legal/aviation/provider/data-model/backend/crypto/backup/compromise/recovery/evidence/policy-runtime/supply-chain/transparency/deletion/retention/migration/re-attestation/preservation/portability/escrow/runtime/personnel validation remains OPEN.
- Reporting remains coarse/checkpoint-based.