# 197 — PWA Recovery-Drill Evidence Anti-Forgery, Emergency-Custody Succession & Personnel-Loss Recovery

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + CRYPTO + PERSONNEL + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A PWA/offline observation boundaries; Track B drill/live/succession state semantics; Track C destructive assurance; Track D privacy-bounded security telemetry.
Dependencies: 183–196.

## Problem
196 established that recovery authorization evidence, emergency identity and drill evidence are separate assurance objects. The next failure class is subtler: an attacker or former custodian may not need to forge every byte. They may replay a valid drill artifact as if it were a real recovery, omit an inconvenient activation/extinction record, preserve an old custody list, or retain enough emergency material after role change to remain effective.

Central rule: **evidence authenticity, sequence completeness, ceremony purpose, custody currentness and personnel authorization are separate properties. A valid old artifact does not prove a current recovery ceremony, and successful handoff does not prove the former custodian is extinct.**

## Five-track balance
- **A Platform/Browser:** Service Worker, Cache Storage, IndexedDB and offline client state can retain drill/recovery observations but cannot prove ceremony purpose, evidence completeness, current custody or personnel authorization.
- **B UX/IA/Content:** owns unmistakable semantics for simulation/drill, live incident, custody transfer pending, former-custodian extinction pending, evidence conflict/UNKNOWN and normal restored. Design Studio remains canonical for reusable interaction/human evidence.
- **C Performance/Accessibility/Quality:** owns replay/omission/splicing/personnel-loss/negative-extinction campaigns. Physical Safari/iPadOS, screen-reader and representative-human validation remain OPEN.
- **D Search/Discovery/Analytics:** receives coarse outcomes only. Analytics is neither the authoritative ceremony ledger nor a staff/custody dossier.
- **E Architecture/Security/Operations:** **highest-risk owner**; owns evidence anti-forgery/anti-omission requirements, custody succession, personnel-loss recovery and recovery-ceremony discrimination.

## SOURCE

### NIST SP 800-53 Rev.5 / Release 5.2.0 — account, audit and personnel lifecycle are linked
NIST SP 800-53 Rev.5 remains the current control catalog, with Release 5.2.0 issued 2025-08-27. AC-2 explicitly links account management with personnel termination/transfer and includes emergency accounts among account types; AU-family controls protect audit information; PS-4/PS-5 address termination and transfer. Transfer: exceptional-access evidence and custody cannot be governed independently from personnel lifecycle.
Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### NIST CSF 2.0 — access must be reviewed when roles or employment change
Current CSF 2.0 PR.AA-05 requires access permissions, entitlements and authorizations to be defined, managed, enforced and reviewed using least privilege and separation of duties. Its implementation examples include reviewing access whenever someone changes roles or leaves and promptly rescinding privileges no longer needed.
Source: https://csrc.nist.gov/projects/cybersecurity-framework/filters

### Microsoft Entra emergency-access guidance — current vendor-specific custody/personnel precedent
Current Microsoft Entra emergency-access guidance recommends emergency-only use, separate secure custody, monitoring, regular validation, and explicitly calls for changing safe combinations after personnel with access leave. It also calls for repeating checks after IT staff departures/role changes and relevant subscription changes. This is a **vendor-specific operational precedent**, not a universal MintTap account count, credential form or cadence.
Source: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access

### CISA privileged-access precedent — remove former-position access before granting new-role access
CISA guidance for privileged accounts emphasizes unique accounts, prompt termination when a user leaves, removal of access from a former role when roles change, and restriction/review of elevated privileges. Transfer: role succession must be an authorization transition, not an additive accumulation of old and new privilege.
Source: https://www.cisa.gov/sites/default/files/2023-12/HPH-Sector-Mitigation-Guide-TLP-CLEAR._508c.pdf

## SYNTHESIS 1 — anti-forgery must include anti-replay, anti-splicing and anti-omission
A cryptographic signature over one evidence object answers only a bounded authenticity/integrity question. It does not establish that:
- the object belongs to a live rather than simulated ceremony;
- the object is the latest admitted generation;
- all required predecessor/successor records are present;
- no activation/action/extinction record was selectively omitted;
- records from different ceremonies were not spliced;
- the signer/approver was currently authorized when the object was created.

Generic evidence envelope should therefore bind, according to the actual architecture:
1. **ceremony identity** — unique identifier and explicit `DRILL` / `LIVE` purpose class;
2. **policy/currentness generation** — the policy and recovery generation under which the ceremony is evaluated;
3. **predecessor binding** — enough lineage to reject detached/replayed old artifacts;
4. **scope/target binding** — exact bounded systems/actions the ceremony authorizes or tests;
5. **actor/role evidence** — identities/roles as evaluated under the then-current authorized-custodian state;
6. **ordered phase evidence** — eligibility → authorization → activation → actions → successor admission → extinction where applicable;
7. **completion/closure state** — including UNKNOWN/incomplete rather than silently treating absence as success;
8. **historical verification context** — sufficient verifier/policy context to interpret old evidence without retaining reusable emergency authority.

Persistent guards:
- `artifact signature valid ≠ ceremony current`;
- `artifact signature valid ≠ ceremony complete`;
- `all visible records valid ≠ no required record omitted`;
- `drill artifact authentic ≠ live activation authorized`;
- `same recovery generation label ≠ same ceremony`;
- `latest timestamp ≠ latest admitted ceremony`;
- `closure record missing ≠ ceremony safely closed`;
- `evidence retained ≠ reusable authority retained`.

### Purpose-class anti-replay
A drill must not be made distinguishable from a live incident only by UI text, ticket title or analytics label. The authoritative recovery/evidence model needs a purpose distinction that consequence-bearing admission checks can consume. A replayed `DRILL` artifact must fail if presented as `LIVE`; a `LIVE` artifact cannot be downgraded to drill merely to hide a real exceptional activation.

Exact encoding/signature/container design remains a Software Engineering/crypto implementation dependency.

## SYNTHESIS 2 — completeness is a protocol property, not a storage property
Immutable storage can preserve an incomplete ceremony perfectly. A complete evidence model therefore needs explicit expected phases/records or an equivalent closure protocol, not merely a directory of signed files.

If a ceremony ends before expected extinction/closure evidence exists, record **INCOMPLETE/UNKNOWN**. Do not synthesize a clean closure later from operator recollection. A later re-attestation may describe what can now be established; it does not retroactively create missing original evidence.

Where evidence is replicated to independent-enough sinks, disagreement is incident evidence. Copy count is not a majority election. Preserve conflicting views and reconcile against authenticated lineage/current policy rather than selecting the most convenient copy.

## SYNTHESIS 3 — custody succession is a security transition
Personnel departure, role transfer, incapacity or organizational loss can invalidate the assumptions behind emergency custody even if the underlying emergency account/key has not changed.

Separate:
1. **custody roster/policy** — who may retrieve/authorize/use which material under which conditions;
2. **authority material** — account, authenticator, key, sealed secret, device or provider capability;
3. **custody evidence** — issuance/receipt/transfer/reseal/revocation evidence;
4. **effective access** — whether a former custodian can still exercise any consequence-bearing path;
5. **historical attribution** — enough identity/role context to interpret past ceremonies after the person leaves.

Generic succession sequence:
1. detect personnel/role/custody change;
2. freeze or bound affected exceptional use if current custody cannot be established;
3. preserve historical evidence before mutation;
4. revoke/remove the departing person's ordinary and emergency access paths as applicable;
5. rotate/reseal/reissue shared or potentially exposed emergency material when the threat model requires it;
6. establish successor custody under current policy;
7. verify retrieval/readiness without normalizing daily emergency use;
8. execute **former-custodian negative authorization tests** across relevant provider/account/device/vault/session/recovery paths;
9. update independent-enough custody/evidence records;
10. retain historical attribution without retaining former operational authority.

`new custodian can retrieve` is a positive availability oracle. `former custodian can no longer act` is a distinct negative security oracle. Both are required for a strong succession claim.

Persistent guards:
- `employee removed from directory ≠ emergency custody revoked`;
- `new custodian added ≠ old custodian extinct`;
- `safe combination changed ≠ all copied/exported material invalidated`;
- `credential rotated ≠ old session/provider recovery path invalidated`;
- `device returned ≠ authenticator/private material unrecoverable`;
- `historical actor record retained ≠ former actor remains authorized`;
- `role transfer complete in HR ≠ authorization transfer complete in every failure domain`.

## SYNTHESIS 4 — personnel-loss recovery must tolerate unavailable custodians without creating unilateral shadow authority
A recovery design that requires one specific person forever is organizationally fragile. A design where any surviving custodian can unilaterally reconstruct unrestricted authority is abuse-prone. Generic requirements therefore separate survivability from unilateral authority.

Personnel-loss scenarios to model include:
- planned departure/role change;
- abrupt termination where pre-notification revocation may be required;
- incapacity/death/unreachable custodian;
- simultaneous loss of multiple custodians;
- merger/reorganization or provider-organization transfer;
- malicious former custodian retaining copied material;
- custodian and ordinary IdP/control-plane failure occurring together.

Exact threshold, number of custodians, secret-sharing method, hardware, legal custody and succession authority remain OPEN. Do not invent a `2-of-3` or similar rule from generic precedent.

## SYNTHESIS 5 — drill/live discrimination needs consequence-bearing enforcement
A genuine recovery ceremony and a drill may use similar actors, credentials and screens. Distinction must therefore survive copied screenshots, replayed tickets and stale client caches.

Generic direction:
- drill identifiers are unique and non-reusable;
- drill scope is bounded to approved fixtures/safe actions where possible;
- live activation requires the current live incident-eligibility/admission path, not merely a valid drill record;
- evidence phases bind to one ceremony identity/purpose;
- closure/extinction records bind to the same ceremony lineage;
- replayed drill evidence cannot advance the live currentness/recovery floor;
- telemetry may observe outcomes but cannot flip purpose or admission state.

## PWA / EFB boundary
A company iPad/PWA remains a recovery **client/subject**, not emergency-custody authority or ceremony oracle.

For a long-offline iPad returning after staff/custody succession or a drill/live recovery:
1. preserve unique local flight/logbook records before destructive migration;
2. treat cached staff names, recovery roles, drill IDs, keys, policy, Service Worker and IndexedDB state as historical observations;
3. obtain current authenticated server policy/currentness/custody-recovery generation;
4. never infer current staff authorization from an old locally cached custody roster;
5. reject queued consequence-bearing work whose authority depended on retired emergency material/personnel;
6. reconcile acknowledged history versus local-only work;
7. resubmit local-only work under current normal authority;
8. keep offline client timestamps and cached drill/live labels from becoming ceremony-currentness or personnel-authority oracles.

No claim is made here that Safari/iPadOS provides unattended background sync, persistent storage guarantees, direct device-to-device synchronization, or MDM-mediated recovery behavior. Those remain runtime VALIDATION/CHANGE WATCH.

## UX / accessibility transfer
Track B should distinguish at least: **DRILL**, **LIVE INCIDENT**, **CUSTODY TRANSFER PENDING**, **FORMER-CUSTODIAN EXTINCTION PENDING**, **EVIDENCE INCOMPLETE/CONFLICT**, and **NORMAL RESTORED**. Human-facing labels cannot override enforcement state. Do not expose unnecessary custodian identity or recovery topology to ordinary product users.

Design Studio W121 remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and representative-human validation remain OPEN. Therefore no human-comprehension PASS is inferred from these semantics.

## Privacy / analytics transfer
Custody and recovery evidence can expose staff identity, role, device, physical custody location, network path and organizational weakness. Retain only what the security/audit purpose requires under applicable policy. Product analytics should consume coarse status/timing where justified and must not become the authoritative evidence store or a permanent personnel-surveillance system.

## Track C destructive campaign
Define a **336-case generic campaign**, extending 196's 328 cases with at least these adjacent classes:
- valid DRILL authorization replayed as LIVE;
- valid LIVE evidence relabeled as DRILL to hide exceptional use;
- activation/action record omitted while closure remains present;
- records from two valid ceremonies spliced into one apparently complete sequence;
- old custody roster replayed after personnel departure;
- former custodian removed from ordinary IdP but retains emergency authenticator;
- shared emergency secret rotated while an old provider/session/recovery path still works;
- new custodian retrieval succeeds but former-custodian negative oracle fails;
- abrupt personnel loss occurs simultaneously with normal IdP/audit outage;
- immutable evidence sink receives an incomplete ceremony and falsely reports `complete`;
- long-offline PWA treats cached former staff/custody state as current;
- analytics/ticketing replay is accidentally accepted as authoritative ceremony evidence.

Campaign definition is not execution.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** NIST SP 800-53 links account, audit and personnel lifecycle controls; it does not prescribe MintTap ceremony format, quorum or cryptography.
- **TRANSFER VALIDATION:** CSF 2.0 PR.AA-05 supports prompt authorization review/rescission on role/employment change; it does not define emergency-custody topology.
- **TRANSFER VALIDATION:** current Microsoft Entra guidance explicitly connects emergency-account validation/custody with staff departures and role changes; this is provider-specific operational precedent.
- **TRANSFER VALIDATION:** CISA privileged-access guidance supports prompt removal of former-role access and separation of elevated/routine privilege; it does not define MintTap break-glass succession.
- **CONTRADICTION:** signed evidence objects without ceremony purpose/lineage/completeness rules can still be replayed, omitted or spliced.
- **CONTRADICTION:** adding a successor custodian while leaving the predecessor effective is accumulation, not succession.
- **CONTRADICTION:** a successful positive recovery drill without a former-authority negative oracle cannot prove privilege extinction.

## MINTTAP DECISION / DIRECTION
1. Treat evidence authenticity, ceremony purpose, sequence completeness, currentness and actor authorization as separate properties.
2. Bind drill/live purpose and ceremony identity into the authoritative evidence/admission model; do not rely on UI/ticket labels.
3. Represent incomplete or conflicting ceremony evidence as UNKNOWN/incident evidence rather than manufacturing clean closure.
4. Treat emergency-custody succession as an authorization transition requiring both successor availability and predecessor extinction evidence.
5. Link personnel termination/transfer to emergency custody, shared-material rotation/reseal where applicable, session/provider-recovery invalidation and independent evidence updates.
6. Do not invent universal custodian counts, quorum, secret-sharing schemes or rotation cadence without actual provider/threat-model evidence.
7. Keep PWA/EFB clients outside emergency custody/ceremony authority; preserve local data and rebootstrap forward to current authenticated state.
8. Preserve historical actor attribution separately from reusable operational authority.

## OPEN / DEPENDENCY / VALIDATION
**OPEN:** actual MintTap/LogMate IAM/federation/provider topology; emergency account/key/authenticator form; custodian roster and succession policy; vault/KMS/device/network failure domains; session/provider recovery semantics; evidence schema/signature/container; personnel/HR integration; drill/live admission implementation; legal/privacy/aviation requirements; physical iPad/WebKit/MDM behavior; human/AT comprehension.

**DEPENDENCY — Software Engineering:** implementable ceremony/evidence state machine, anti-replay/anti-splicing binding, actor/policy generation checks, provider/session invalidation, custody transition, fault injection and negative authorization tests. Software Engineering Studio remains Foundation and provides no product PASS for this block.

**DEPENDENCY — Design Studio:** operator state semantics and error/recovery presentation. W121 remains execution-priority Stage 3 PRACTICE / NOT PASSED.

**VALIDATION:** execute the 336-case campaign against actual provider/runtime architecture; test staff departure/role-change and abrupt-custodian-loss scenarios; prove old sessions/authenticators/provider-recovery paths fail; test evidence omission/splicing/replay; validate Safari/iPadOS reconnect behavior; validate operator comprehension with AT and representative humans.

**CHANGE WATCH:** NIST 800-53/CSF mappings; provider emergency-access/custody guidance; browser/WebKit/MDM/session behavior; identity-provider recovery semantics.

## Gate result
**PASS (generic).** The adjacent generic boundary is now explicit: recovery evidence must resist replay/omission/splicing, emergency custody must have a personnel-aware succession lifecycle, and handoff requires both successor readiness and former-authority extinction. Production/runtime/provider/personnel/crypto/device/human validation remains OPEN.

## Next high-value target
**PWA emergency-custody material rotation, authenticator/session invalidation & orphaned-authority discovery after personnel change**: determine how to prove every consequential copy/session/recovery route derived from retired custody is either invalidated or explicitly bounded UNKNOWN; how to discover orphaned emergency authority across provider, vault, device and regional caches without treating inventory as proof of absence; and how long-offline PWA clients converge without resurrecting retired personnel authority.