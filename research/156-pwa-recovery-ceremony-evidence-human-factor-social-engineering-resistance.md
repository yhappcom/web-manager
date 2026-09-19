# 156 — PWA Recovery-Ceremony Evidence, Human-Factor Failure & Social-Engineering Resistance

Status: **PASS (generic) / PRODUCT + ORGANIZATION + IDENTITY + PROVIDER + MANAGED-IPAD + CEREMONY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 154 authority-floor escrow; 155 custody/succession/anti-capture; Track A browser/authentication mechanics; Track B truthful high-risk confirmation UX; Track C ceremony/destructive validation; Track D diagnostics only.

## Why this study exists

155 established survivable custody and succession without allowing one surviving insider or emergency mechanism to become permanent authority. That model can still fail at the moment humans exercise it. A legitimate custodian can be phished, pressured, fatigued, shown the wrong incident/package, routed through a compromised communication channel, or asked to approve a technically authentic but semantically wrong recovery target.

The objective is therefore to make a recovery ceremony **target-bound, participant-bound, evidence-bearing and resistant to social-engineering shortcuts**, while ensuring the audit trail is not itself a reusable recovery credential.

## SOURCE

### NIST SP 800-63B-4 — phishing resistance is protocol property, not user vigilance
NIST SP 800-63B-4, published July/August 2025 and superseding SP 800-63B, defines phishing resistance as preventing disclosure of authentication secrets or valid authenticator outputs to an impostor verifier without relying on claimant vigilance. Manual-entry OTP and out-of-band authenticators are not phishing-resistant because outputs are not bound to the specific authenticated session. NIST recognizes channel binding and verifier-name binding as phishing-resistant approaches.

Sources:
- https://csrc.nist.gov/pubs/sp/800/63/b/4/final
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/

### CISA — phishing-resistant MFA preferred; ordinary push approval is fatigue-prone
CISA recommends phishing-resistant MFA such as FIDO/WebAuthn or PKI for high-value targets. Its guidance distinguishes ordinary push notifications, which remain vulnerable to push bombing/MFA fatigue and user error, from stronger methods; number matching improves resistance to push bombing but is still not phishing-resistant.

Source:
- https://www.cisa.gov/sites/default/files/2023-01/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf

### NIST SP 800-61 Rev. 3 — incident response is an organizational risk-management activity
NIST finalized SP 800-61 Rev. 3 on 2025-04-03, superseding Rev. 2. It integrates incident response across CSF 2.0 functions rather than treating recovery as an isolated technical act. Transfer: recovery identity, communications, governance and evidence must survive the same incident that may have compromised ordinary systems.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations

### NIST SP 800-53 / 800-53A / 800-84 — separation, assessment and exercises
The controls and assessment/exercise guidance used by 155 remain applicable: separation of duties reduces unchecked privilege abuse; contingency/incident roles must be assessable; exercises must test people and plans rather than only system availability.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final
- https://csrc.nist.gov/pubs/sp/800/84/final

## SYNTHESIS — a ceremony is an authorization protocol with humans in the loop

A recovery ceremony is not secure merely because every participant authenticated successfully. It must bind at least:
- **incident** — why extraordinary recovery is occurring;
- **target** — which environment/account/control plane is being recovered;
- **package/checkpoint** — exactly which authority-floor/recovery material is admitted;
- **requested consequence** — what authority the ceremony will create or restore;
- **participants and roles** — who is acting as custodian/approver/executor/verifier under which current succession generation;
- **ceremony generation/nonce** — which unique recovery attempt the approvals belong to;
- **time/currentness context** — enough to reject replay or stale approvals;
- **closure state** — whether temporary authority was retired and the new state resealed.

Persistent guards:
- `participant authenticated ≠ recovery request legitimate`;
- `quorum authenticated ≠ target/package correct`;
- `message came from colleague account ≠ colleague initiated request`;
- `out-of-band ≠ independent if both channels share the same compromised identity/provider/device`;
- `number matching ≠ phishing resistance`;
- `approval recorded ≠ approver understood consequence`;
- `ceremony transcript complete ≠ transcript safe to replay`;
- `audit evidence sufficient ≠ recovery secret should be logged`;
- `urgent incident ≠ identity/target binding optional`;
- `human confirmation ≠ cryptographic session binding`.

## Target binding before approval

The ceremony should expose a stable, independently verifiable recovery descriptor before any consequential approval. A generic descriptor can include:
- incident identifier and declared trigger;
- organization/environment/tenant/account target;
- authority-floor/checkpoint identifier and digest;
- requested recovery operation and bounded consequence;
- policy/custody generation;
- unique ceremony identifier/nonce;
- expiry or bounded validity where meaningful;
- expected participant roles;
- independent verification instructions.

The purpose is not to make humans compare long hashes manually. It is to ensure the authentication/approval mechanism and the independent verification path refer to the **same named recovery object** rather than a generic `Approve recovery?` prompt.

## Authentication and approval are separate semantics

Phishing-resistant authentication should be preferred for high-consequence recovery participants where feasible. But even strong authentication only proves the authenticated actor controlled the authenticator for that verifier/session. It does not prove:
- the incident is real;
- the target is correct;
- the package is fresh;
- the requested consequence is authorized;
- another participant is uncompromised;
- the operator interpreted the request correctly.

Therefore participant authentication is necessary evidence, not the complete authorization decision.

## Out-of-band verification: independence must be modeled, not named

An OOB verification path is useful only to the extent it avoids the suspected failure domain. Examples of correlated failure include:
- corporate email and chat both depend on the same compromised SSO;
- voice call and SMS both depend on the same hijacked telephone account;
- two apps run on the same compromised endpoint;
- recovery portal and approval portal share the same compromised DNS/origin/admin plane;
- both `independent` contacts are read from the same attacker-modifiable directory.

The ceremony therefore records **verification-channel provenance and failure-domain assumptions**. Exact channels/providers are product/organization-specific OPEN decisions.

## Approval fatigue and unsolicited-request rule

High-consequence recovery must not train custodians to approve repeated prompts until one succeeds. Generic controls:
1. unsolicited recovery prompts are reject/report events, not routine workflow;
2. repeated failed/denied prompts increase suspicion rather than social pressure to approve;
3. approval prompts show target/consequence/ceremony identity, not generic `Allow`;
4. no approval should be obtained by repeatedly reissuing an equivalent prompt after denial without a separately governed reason;
5. the system should distinguish `DENIED`, `EXPIRED`, `CANCELLED`, `SUSPECTED SOCIAL ENGINEERING`, and `TECHNICAL FAILURE` where operationally useful;
6. emergency urgency must not turn a weak push prompt into sufficient evidence.

## Coercion and duress boundary

No generic technical design can prove that a human participant is free from coercion. The correct security posture is to avoid claiming that ordinary authentication or quorum solves coercion.

Possible organizational controls can include independent participants/failure domains, bounded authority, delayed or staged high-consequence transitions where compatible with incident needs, independent review, and explicit duress/escalation procedures. Exact procedures are security/organizational/legal OPEN decisions.

`authenticated human action ≠ voluntary human action` is therefore a persistent boundary.

## Ceremony evidence without credential leakage

A durable ceremony record should support later reconstruction of **what was authorized and by which governed roles** without storing reusable recovery material.

Useful evidence classes can include:
- ceremony ID/generation and timestamps;
- target/incident/package identifiers or non-secret digests;
- policy/custody generation;
- participant role identifiers and authenticated decision results;
- verifier/session or attestation references where safe and appropriate;
- approval/denial/abort state transitions;
- authority-floor before/after references;
- temporary-authority creation/retirement evidence;
- resealing/rotation completion evidence;
- contradictions, exceptions and residual uncertainty.

Do **not** infer that auditability requires storing:
- private keys or recovery shares;
- OTPs/recovery codes;
- bearer session tokens;
- raw secrets used to reconstruct escrow;
- reusable signed approval objects if replay would confer authority.

Where signatures/assertions are retained for audit, the authorization service must still enforce ceremony generation, expiry/currentness, target binding and one-time/consumed semantics. `signature retained for verification ≠ signature remains executable`.

## Transcript integrity and replay

A transcript can be authentic yet dangerous if copied into a later ceremony. Recovery approval must therefore be bound to the unique ceremony and target rather than treated as a timeless statement such as `Alice approves disaster recovery`.

Replay defenses can include unique ceremony identifiers/nonces, current policy/custody generation, target/package binding, bounded validity, consumed-state semantics and authoritative server-side state. Exact mechanism belongs to implementation validation.

## Human-readable confirmation design — Track B dependency

The recovery UX should make consequential distinctions visible without forcing users to interpret raw security internals. Requirements include:
- name the target/environment and operation;
- state whether local data preservation, server authority restoration, key recovery or account recovery is occurring;
- surface unexpected generation/package mismatch as a stop condition, not a warning users routinely bypass;
- provide an explicit safe abort/report path;
- avoid countdowns, dark patterns or repeated prompts that manufacture urgency;
- preserve accessibility under degraded conditions;
- do not imply success until authoritative closure/resealing state is known.

Design Studio owns reusable interaction design. Web Manager owns these web/security requirements and evidence boundaries.

## PWA / Service Worker / managed-iPad application

A stale or compromised PWA can present convincing recovery UI while lacking current organizational authority. Therefore:
- recovery ceremony authority is server/organization-side and cannot be minted by cached Service Worker state;
- old PWA UI may display historical information, but consequential approval must bind to current authoritative ceremony state;
- an offline iPad containing unique flight records may be a recovery **data source**, not a ceremony participant merely because it possesses cached credentials;
- local export/preservation can remain available while organizational recovery is unresolved;
- reconnect should reconcile local data against current recovered authority without replaying old approval artifacts;
- a Service Worker update or `online` state does not prove ceremony/current-custody convergence.

Actual WebKit/MDM/keychain/browser-authenticator behavior and direct device-to-device synchronization remain OPEN until runtime evidence exists.

## Cross-track integration

### Track A — Platform & Browser
Owns exact WebAuthn/authenticator/browser/SW/session mechanics and proves what session binding/local state can and cannot establish. Transfer: browser authentication mechanics do not establish incident/package legitimacy.

### Track B — UX / IA / Content
Owns recovery information architecture and truthful confirmation/abort/report states. Consumes target-binding requirements rather than inventing security semantics.

### Track C — Performance / Accessibility / Quality
Owns destructive ceremony drills: phishing simulation, repeated-prompt fatigue, stale/replayed approval, wrong-target/package, compromised channels, inaccessible/degraded UI and post-recovery negative authorization.

### Track D — Search / Discovery / Analytics
Telemetry may help detect unusual ceremony attempts or measure recovery progress. Analytics is not a source of participant legitimacy, target authenticity or authority-floor currentness.

### Track E — Owner
Owns ceremony authorization semantics, failure-domain independence, evidence minimization, replay resistance, social-engineering boundaries and closure governance.

## MINTTAP DECISION — minimal sufficient generic model

If high-consequence recovery exists:
1. treat the ceremony as a versioned authorization protocol, not a meeting/checklist;
2. bind approvals to incident + target + package/checkpoint + consequence + ceremony generation;
3. prefer phishing-resistant participant authentication where feasible, while keeping authentication distinct from recovery authorization;
4. verify critical recovery facts through a genuinely independent path appropriate to the suspected failure domain;
5. reject generic/repeated approval prompts and make unsolicited prompts reportable security events;
6. never rely on number matching, OOB codes or human vigilance as proof of phishing resistance;
7. preserve a minimized, integrity-protected ceremony record that excludes reusable secrets/credentials;
8. make retained approvals non-replayable through ceremony/currentness/target/consumption semantics;
9. preserve local PWA/iPad data independently from organizational authority recovery;
10. close recovery only after temporary authority retirement, resealing/rotation and negative authorization tests.

## VALIDATION — 56-case recovery-ceremony / human-factor campaign

1. legitimate ceremony; 2. wrong incident ID; 3. wrong tenant/environment; 4. wrong authority-floor package; 5. authentic but stale package; 6. forged package; 7. package digest mismatch; 8. wrong requested consequence; 9. participant authentic but wrong role; 10. former custodian authenticates; 11. successor authenticates under stale generation; 12. phishing-resistant authenticator succeeds; 13. OTP phished; 14. ordinary push fatigue attack; 15. number-matching social engineering; 16. attacker-controlled verifier; 17. compromised corporate email; 18. compromised chat; 19. email+chat share same SSO failure domain; 20. phone/SMS account hijacked; 21. two channels share compromised endpoint; 22. independent contact directory tampered; 23. unsolicited approval prompt; 24. repeated prompt after denial; 25. prompt text hides target; 26. prompt text hides consequence; 27. fake urgency/countdown; 28. safe abort works; 29. report-suspicion path works; 30. one participant coerced; 31. colluding quorum; 32. one participant unavailable; 33. verifier/auditor unavailable; 34. ceremony expires; 35. cancelled ceremony replayed; 36. prior successful approval replayed; 37. same approval applied to different target; 38. same approval applied to different package; 39. same approval applied to later custody generation; 40. transcript tampered; 41. transcript authentic but incomplete; 42. transcript contains secret accidentally; 43. logs contain bearer token accidentally; 44. audit signature retained but execution state consumed; 45. telemetry unavailable; 46. ceremony still independently auditable; 47. stale Service Worker renders old recovery UI; 48. server rejects stale ceremony; 49. offline iPad preserves unique records; 50. offline iPad cannot authorize organizational recovery; 51. reconnect does not replay historical approvals; 52. accessibility at zoom/reflow/keyboard/AT remains usable; 53. temporary authority retired; 54. new escrow resealed; 55. predecessor/emergency credential negative test fails authorization as expected; 56. full exercise survives compromised ordinary communications without granting attacker or stale actor recovery authority.

## CONTRADICTION / failure-mode analysis

### Authenticated-person-is-legitimate-request theater
Strong authentication proves an actor/session property, not the truth of the incident, package or requested consequence.

### Out-of-band-is-independent theater
Two channels that share the same SSO, endpoint, provider, directory or attacker-controlled control plane are not meaningfully independent for that failure.

### Number-matching-is-phishing-resistant theater
Number matching can mitigate push bombing, but NIST's current phishing-resistance definition excludes manual-entry OOB/OTP flows from phishing-resistant status.

### Transcript-everything theater
Logging secrets, recovery shares or reusable approval artifacts increases compromise blast radius. Audit evidence should prove the ceremony without becoming another credential store.

### Human-read-and-click theater
Long warning text does not cryptographically bind approval to the intended target and can worsen fatigue. Human-readable consequence disclosure complements, not replaces, protocol binding.

### Offline-iPad-is-trusted-witness theater
A company iPad may preserve unique operational data. Its possession, cached login or stale PWA state does not establish current recovery authority or participant legitimacy.

## OPEN

Product/runtime evidence is still required for:
- actual MintTap/LogMate recovery operations and consequence classes;
- identity provider, authenticator and WebAuthn/passkey deployment;
- recovery portal/origin/DNS/provider topology;
- organizational communication and independent-verification channels;
- actual custody/succession/quorum policy;
- ceremony object/schema, nonce/currentness/consumption semantics;
- audit store, retention, redaction and key management;
- managed-iPad/WebKit/MDM authenticator behavior;
- accessibility and human usability under incident stress;
- legal/employment/aviation constraints on recovery roles and records.

No production PASS is claimed.

## CHANGE WATCH

- NIST SP 800-63B-4 is the current final authentication baseline; do not regress to withdrawn SP 800-63B requirements as current policy.
- NIST SP 800-61 Rev. 3 is the current final incident-response baseline and supersedes Rev. 2.
- Browser/platform authenticator behavior, passkey/WebAuthn deployment details and managed-iPad capabilities require current runtime/platform verification.
- CISA guidance is operational guidance, not a substitute for protocol-specific NIST/WebAuthn evidence.

## Gate result

**PASS (generic).** The Web Manager can now distinguish participant authentication from ceremony authorization; bind recovery approvals to incident/target/package/consequence/generation; reason about correlated OOB channels, approval fatigue, coercion limits and social engineering; preserve auditability without logging reusable credentials; prevent ceremony transcript replay; and keep PWA/iPad data recovery separate from organizational recovery authority. Production and human/runtime validation remain OPEN.

## Next highest-value adjacent work

**PWA recovery-ceremony compromise containment, partial-ceremony abort & safe restart.** If compromise or contradiction is discovered after some participants have approved or after temporary recovery authority has been partially created, determine how to invalidate the ceremony generation, quarantine partial artifacts, preserve forensic evidence, prevent approval carry-over, and restart without either resurrecting predecessor authority or permanently locking out legitimate recovery.