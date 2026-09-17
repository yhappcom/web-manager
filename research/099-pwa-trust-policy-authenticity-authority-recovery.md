# 099 — PWA Trust-Policy Authenticity, Authority Recovery & Anti-Rollback Boundaries

Status: **PASS (generic) / PRODUCT CRYPTOGRAPHIC + CONTROL-PLANE VALIDATION OPEN**  
Evidence date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: A Platform/Browser, B UX/IA/Content, C Quality/Accessibility, D Discovery/Analytics

## Why this block

098 established that a stale/offline client must re-establish current trust before remote mutation or outbox replay. The next failure is deeper: if the origin, CDN, deployment account or policy control plane itself is compromised, merely fetching a newer policy from that same authority does not prove that the policy is legitimate.

This block studies the generic security model needed to reason about authenticated trust-policy changes, key rotation, rollback/freeze resistance and recovery bootstrap. It does **not** prescribe a MintTap/LogMate cryptographic design.

## Track allocation

- **E owns** authority hierarchy, provenance, signing/recovery policy, rollback/freeze containment and incident recovery.
- **A supplies** browser secure-context/Web Crypto/update/storage mechanics and the limits of same-origin delivery as an independent trust proof.
- **B consumes** trustworthy-vs-unverifiable update/recovery states without inventing certainty.
- **C owns** negative tests for invalid/expired/rolled-back/frozen policy, key transitions and target-device behavior.
- **D consumes** the rule that discovery/analytics/config channels are not security-policy roots.

Track E remains the highest-risk bottleneck. Exact product implementation remains the evidence blocker.

## History/problem — transport security is not policy authenticity after authority compromise

HTTPS authenticates the TLS endpoint and protects transport. Earlier 092 work established that a compromised deployment/origin can still serve malicious bytes over valid HTTPS. The same applies to revocation/trust policy: if the client trusts any policy merely because it arrived from the currently configured origin, compromise of that origin can authorize the attacker's own policy.

### Guard

`HTTPS policy fetch succeeded ≠ policy authorized by an independent trust root`.

A second signature layer is useful only when its signing authority is meaningfully separated from the compromised delivery authority and the verifier enforces it correctly.

## SOURCE — TUF separates update roles and protects against rollback/freeze

The Update Framework (TUF) is a mature software-update security model. Its current specification uses separate Root, Targets, Snapshot and Timestamp roles. Roles may require a threshold of signatures. Clients ship with trusted root keys, verify signed metadata, reject metadata version rollback, and use expiration to detect freeze attacks. Root-key transitions are chained: an intermediate new root is verified against thresholds from both the immediately previous trusted root and the new root. Outdated clients can walk intermediate root versions rather than blindly jumping to an unrelated newest key set.

TUF is not automatically the correct implementation for a web PWA policy channel. It is used here as reusable security evidence for authority separation, threshold trust, version continuity, expiry and recovery from key compromise.

### SYNTHESIS

A policy signature answers only part of the problem. A robust verifier needs to know:

1. **which authority/key is allowed** to sign this policy class;
2. **which policy version/generation is acceptable** relative to already trusted state;
3. **whether the policy is fresh enough** for the security decision;
4. **whether a key transition preserves trust continuity**;
5. **what happens when freshness cannot be established** because the client is offline;
6. **what recovery authority exists** if the normal signing/deployment path is compromised.

### Guards

`signature mathematically valid ≠ signer authorized for this policy`.

`newer timestamp ≠ authorized policy generation`.

`higher version ≠ safe policy`.

`valid old signature ≠ current policy`.

## SOURCE — HTTP Message Signatures illustrate verification-context requirements

RFC 9421 defines HTTP Message Signatures and explicitly requires more than successful cryptographic verification: the key and algorithm must be appropriate for the message context, expected components must be covered, time boundaries must be enforced, and applications may require nonces or additional signed fields. It warns about insufficient coverage, replay and key/algorithm mix-up/downgrade.

### TRANSFER VALIDATION

This supports a generic PWA policy rule: do not verify only a detached blob and then trust surrounding unsigned routing/audience/version fields. The signed semantic envelope must cover the values that determine how the policy is interpreted.

A generic policy envelope may need authenticated fields such as:

- policy type/purpose;
- product/environment/audience;
- monotonic generation/version;
- issued-at / not-before / expiry where appropriate;
- minimum supported client/protocol generation;
- revoked bridge/device/key identifiers where applicable;
- successor key/authority information when rotating;
- payload digest or canonicalized policy body;
- signature algorithm/key identifier constrained by local policy.

This is an implementation handoff vocabulary, not a final schema.

### Guard

`signed payload ≠ signed interpretation context`.

## Web Crypto capability and its boundary

W3C Web Crypto exposes signature verification primitives to web applications. This means a PWA can technically verify signatures using key material it already trusts. But API availability does not establish safe bootstrap, key storage, canonicalization, anti-rollback state, clock reliability or recovery policy.

### Guard

`SubtleCrypto.verify available ≠ trustworthy policy-update system established`.

A verifier implemented in same-origin JavaScript also inherits 095/092 risks: a compromised currently executing application can potentially bypass its own verification logic unless the architecture establishes a stronger trusted execution/update boundary. Therefore client-side policy signatures are not automatically a cure for malicious Service Worker/application-code compromise.

## Bootstrap is the root problem

Every signature system eventually asks: why does the client trust the verification key?

Possible generic bootstrap classes include:

- key/hash pinned in a shipped application artifact;
- trusted root metadata persisted from an earlier verified state;
- OS/native/MDM provisioned trust material;
- server-delivered key with no independent trust anchor;
- user/admin mediated recovery material.

Only the first three can potentially add independence from a currently compromised ordinary origin, and each has lifecycle/availability costs. The fourth merely moves the same trust problem into another fetched file.

### Guard

`public key fetched from compromised origin ≠ independent authenticity proof`.

For a pure web PWA, bootstrap and self-protection are especially constrained because the origin normally supplies both verifier code and data. Exact feasibility requires Software Engineering/security architecture evidence; do not claim native-style update trust from generic Web Crypto availability.

## Key rotation — planned rotation and compromise recovery are different

OWASP key-management guidance requires lifecycle planning for generation, distribution, rotation, compromise and recovery. It also recommends separating keys by purpose and documenting compromise-recovery procedures.

A planned signing-key rotation can preserve continuity by having the currently trusted authority authorize the successor. A compromise recovery is harder because the current key may no longer be trustworthy.

### Generic distinction

- **planned rotation:** old trusted authority can authorize successor under normal policy;
- **suspected compromise:** old authority may not be sufficient evidence for successor;
- **confirmed compromise:** recovery requires a separately protected recovery/root authority or trusted re-bootstrap path;
- **lost key without compromise:** availability/recovery problem, not necessarily integrity compromise.

### Guards

`key rotated ≠ old key proven uncompromised`.

`old key revoked ≠ offline client learned revocation`.

`successor signed only by compromised key ≠ compromise recovery proven`.

## Threshold/role separation as blast-radius control

TUF demonstrates why one omnipotent online signing key is a weak update architecture. Threshold signatures and role separation can ensure that compromise of one key or one online role is insufficient for arbitrary update authorization.

### MINTTAP DIRECTION

For any future security-critical offline policy/update channel, evaluate whether deployment authority, ordinary online policy authority and recovery/root authority should be distinct. Do not implement threshold signing merely because TUF does; first prove that the product threat model and operational capacity justify the complexity.

### Guard

`more keys ≠ more security unless authority, custody and recovery are actually separated`.

## Rollback, freeze and fast-forward reasoning

### Rollback
An attacker replays an older but correctly signed policy that re-enables a retired bridge/key/protocol. A client that persists the highest trusted generation can reject lower generations.

### Freeze
An attacker withholds newer policy and keeps a client on an old still-valid state. Expiration/freshness limits can detect some freeze conditions, but an offline EFB cannot always obtain trusted current time or fresh metadata.

### Fast-forward
An attacker may try to push an implausibly high generation so future legitimate generations appear older. A bare `max(version)` rule is therefore insufficient without authenticated transition rules and recovery handling.

### Guards

`monotonic version check ≠ freeze resistance`.

`expiry check ≠ trustworthy wall clock`.

`highest version seen ≠ legitimate authority transition`.

`offline beyond policy freshness window ≠ user data invalid`.

## Offline freshness is a product-security trade-off

A long-offline EFB creates an unavoidable tension. If security-critical policy must be fresh, the application may eventually need to deny selected remote/bridge capabilities when freshness cannot be re-established. If it allows indefinite use of stale trust, revocation cannot take effect while disconnected.

This must not silently become a data-loss policy.

A generic degraded state is:

`policy freshness unknown/expired → preserve authoritative local records/outbox → deny or constrain security-sensitive bridge/replay capability according to explicit product policy → recover/revalidate when trusted connectivity/authority returns`.

### Guards

`policy expired ≠ local records expired`.

`cannot prove current trust ≠ erase local state`.

`security-sensitive bridge blocked ≠ core local task necessarily blocked`.

Exact offline authorization duration remains PRODUCT OPEN.

## Clock/time boundary

Expiry-based anti-freeze mechanisms depend on time. Browser/device clocks can be wrong or manipulated; network time is unavailable offline; a signed server time assertion itself needs freshness/replay semantics.

### VALIDATION requirement

Any product design relying on `issuedAt`, `expiresAt` or certificate-like time windows must explicitly document its trusted-time assumption and test clock rollback/forward, long offline duration, reboot and reconnect.

Do not infer that `Date.now()` is a secure trusted clock.

## Recovery from compromised delivery/control plane

A generic recovery sequence should distinguish:

1. detect/suspect compromise;
2. stop the smallest unsafe online capability;
3. preserve authoritative local records/outbox;
4. establish recovery authority independent enough from the compromised path;
5. rotate/revoke affected keys/credentials;
6. publish a new authenticated trust generation;
7. allow stale clients to establish a verifiable chain/re-bootstrap path;
8. repair worker/shell/runtime using 092/095 evidence;
9. revalidate schema/protocol/outbox compatibility;
10. resume remote capability only after current trust and runtime integrity are proven.

### Guard

`new signed policy accepted ≠ compromised worker/runtime repaired`.

Policy authenticity and runtime integrity are complementary, not substitutes.

## UX/content contract

Track B/Design Studio should distinguish truthful states such as:

- **Security policy cannot be verified — records remain saved locally**;
- **Synchronization paused until current trust can be verified**;
- **This installation is too old to establish current trust — recovery/update required**;
- **Security recovery completed** only after the actual runtime/policy acceptance contract passes.

Do not tell the user that data is corrupt merely because authority freshness is unknown. Do not tell the user an update is safe merely because it downloaded successfully.

## Accessibility/quality validation

Track C should eventually execute negative matrices for:

- valid current signature;
- invalid signature;
- valid signature from unauthorized key;
- old valid policy replay;
- expired policy;
- future-dated policy / clock rollback / clock jump;
- generation fast-forward attempt;
- planned key rotation;
- missing intermediate key transition;
- compromised-key recovery path;
- offline beyond freshness window;
- stale Service Worker serving old policy;
- repaired origin with compromised installed worker;
- policy verification failure while authoritative unsynced records exist;
- keyboard/focus/status-message/recovery semantics;
- Chromium + independent engine, Safari/managed iPad separately.

Positive-only signature tests are insufficient. RFC 9421 explicitly notes the need for invalid-signature negative testing to prove verification is actually enforced.

## Track D transfer

Search, campaign, analytics, remote-config and attribution channels must not become implicit security-policy roots merely because they already distribute configuration. Cached/indexed URLs and analytics parameters are untrusted inputs to security decisions unless separately authenticated and authorized.

### Guard

`remote config delivered ≠ security authority established`.

## Design Studio dependency

Canonical Design Studio Web status on 2026-09-17 is Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED. W050 extends tenant/context isolation to offline outbox provenance but execution remains OPEN; no Safari, screen-reader, physical-device or human-UX PASS exists. Consume its truthful-state and provenance requirements without upgrading them to product evidence.

## Software Engineering dependency

Canonical Software Engineering Studio remains Foundation IN STUDY. F005 separates error/timeout observation from cleanup/terminal resource state; D006 retains retry/idempotency/conflict work. These reinforce that a failed trust fetch or caller timeout is not proof that underlying work or queued operations are safely terminated. No product signing/bootstrap/runtime implementation evidence exists yet.

## VALIDATION handoff

Before choosing a product cryptographic design, engineering/security evidence must answer:

1. What exact policy/update asset is security-critical?
2. Which authority is allowed to sign each policy class?
3. Where does initial trust material come from?
4. Can the currently executing origin/worker bypass verification?
5. What semantic fields are signed and canonicalized?
6. What monotonic state is persisted, and can storage eviction/reset remove anti-rollback memory?
7. What trusted-time assumption exists?
8. How are planned rotation and compromise recovery different?
9. Is there a separately protected recovery/root authority?
10. How does a long-offline client traverse missed trust generations?
11. What happens when trust cannot be refreshed but unsynced records exist?
12. How are worker/runtime repair and policy repair proven independently?
13. How is key custody/audit/recovery operated in practice?
14. What target managed-iPad/MDM constraints alter the model?

## CHANGE WATCH

- TUF specification and conformance behavior should be rechecked before implementation; current official specification index is actively maintained.
- Web Crypto Level 2 remains evolving; do not generalize future API additions to deployed Safari/managed iPad without target evidence.
- Browser/OS managed-device policy can materially alter bootstrap, key storage and recovery options.
- Cryptographic algorithm/key-management recommendations are security-sensitive and require current specialist review before implementation.

## Integrated judgment

The durable rule is:

> A stale client must not trust a policy merely because it is newer or arrived over HTTPS. Security-critical policy needs an explicit authority, authenticated interpretation context, continuity/anti-rollback rules and a recovery path whose trust does not collapse into the same compromised delivery channel. When current trust cannot be established, contain the smallest unsafe capability while preserving authoritative local data.

This closes the generic authority-authenticity prerequisite. Product cryptographic architecture and managed-device execution remain OPEN.