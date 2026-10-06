# 317 — LogMate PWA Layered Admission, App Attestation & Replay-Safe Offline Retry Gate

Status: **PASS (generic/platform) / production Sync + runtime + physical/managed-iPad validation OPEN**  
Evidence date: 2026-10-06  
Curriculum: Stage 8 Security / Privacy / Trust continuous expert application  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 314 authenticated/authorized server boundary; 315 UNKNOWN-commit/idempotency; 316 dedup/receipt retention and stale replay.

## Why this checkpoint exists

315–316 establish durable logical-operation identity and authoritative dedup/reconciliation. The adjacent security question is whether authentication, authorization and app attestation can be treated as the operation identity or commit receipt. They cannot.

For a long-offline LogMate-like PWA/EFB, durable user intent may outlive transient authentication and attestation tokens. Reconnection must preserve the logical operation while reacquiring current admission proof.

## SOURCE — Firebase Authentication currentness

Firebase Admin SDK ID-token verification validates token format/signature/expiry but does not check revocation by default. Revocation-aware verification is a separate current-state check. Revoking refresh tokens prevents new ID tokens from existing sessions, while already-issued ID tokens can remain active until natural expiry.

Sources:
- https://firebase.google.com/docs/auth/admin/verify-id-tokens
- https://firebase.google.com/docs/reference/admin/node/firebase-admin.auth.baseauth

## SOURCE — App Check is a separate attestation layer

Firebase App Check protects backend resources by attesting the app/client. Web reCAPTCHA Enterprise App Check tokens have configurable TTL from 30 minutes to 7 days; shorter TTL improves exposure bounds but increases attestation latency/quota/cost. Web token auto-refresh must be enabled explicitly.

Baseline App Check uses reusable session tokens. Limited-use tokens and replay protection are separate mechanisms. Replay protection is beta; consuming a token adds a backend network round trip and may increase attestation cost/quota pressure. Firebase recommends selective use for sensitive operations.

Sources:
- https://firebase.google.com/docs/app-check/web/recaptcha-enterprise-provider
- https://firebase.google.com/docs/app-check/enable-enforcement
- https://firebase.google.com/docs/reference/js/app-check
- https://firebase.google.com/docs/reference/admin/node/firebase-admin.app-check.verifyappchecktokenoptions
- https://firebase.google.com/docs/app-check/cloud-functions

## SOURCE — privileged Firestore backend bypasses client Rules

Firestore server client libraries bypass Cloud Firestore Security Rules and authenticate through Google Application Default Credentials/IAM. Therefore client Rules do not prove that a privileged backend correctly authorizes an end-user mutation.

Sources:
- https://firebase.google.com/docs/firestore/security/rules-query
- https://firebase.google.com/docs/firestore/security/test-rules-emulator

## SYNTHESIS — four identities/proofs must remain separate

Separate:
1. **logical operation identity** — durable identity of one user intent;
2. **request-attempt identity** — one network execution attempt;
3. **subject authority proof** — current authenticated/authorized user/session state;
4. **app attestation proof** — current evidence that the request comes from an accepted app/client context.

Persistent guards:
- `valid App Check ≠ authenticated user`;
- `authenticated user ≠ authorized mutation`;
- `authentic app/client ≠ trusted payload`;
- `request attempt ≠ logical operation`;
- `credential refresh ≠ new logical operation`;
- `App Check accepted/consumed ≠ application mutation committed`;
- `Security Rules PASS ≠ privileged backend mutation authorized`;
- `credential expired/revoked ≠ durable local flight evidence should be deleted`.

A portable retry after long offline is:

`same durable logical operation + current authorization + current attestation where required + new request attempt`.

Transient Auth/App Check material should not become the durable identity of queued flight intent.

## UNKNOWN-commit interaction

Limited-use-token consumption and application commit are different state transitions. A token can be consumed before application logic fails; an application commit can succeed while the response is lost. Therefore App Check consumption cannot replace 315's authoritative receipt/reconciliation or 316's dedup memory.

If the first request outcome is UNKNOWN, retry uses the same logical operation identity while reacquiring current admission proof. Minting a new operation merely because credentials or attestation changed can convert one user intent into two material effects.

## Privileged-backend admission

If a future LogMate Sync service uses Firestore server SDKs, IAM governs the service principal's database access. The Sync service must separately enforce the product's current subject/operation authorization, operation lineage, contradiction handling, idempotent admission and authoritative receipt/reconciliation. No current LogMate production implementation is inferred.

## Cross-track transfer

- **Track A:** owns browser token lifecycle, Service Worker/lifecycle opportunities and platform capability distinctions.
- **Track B:** preserves semantic states such as locally saved, waiting, verifying outcome, remotely acknowledged and needs attention. Attestation refresh must not be presented as a new user mutation.
- **Track C:** fault-injects auth/attestation expiry, revocation, token consumption, response loss and backend admission boundaries. Emulator evidence does not promote physical Safari/Home-Screen/managed-iPad behavior.
- **Track D:** observes payload-minimized admission/retry/reconciliation classes; telemetry cannot elect authority.
- **Track E:** owns layered admission, privileged-backend authorization, idempotency, authority retirement and operational lifecycle.

## VALIDATION — integrated 52-case bundle

Retain 315 cases 1–28 and 316 cases 29–40. Add:

41. valid app attestation + unauthenticated subject → reject;
42. valid app attestation + authenticated but unauthorized subject → reject;
43. valid subject authority + missing/invalid required attestation → reject without losing local evidence;
44. queued operation survives Auth/App Check expiry and reacquires current proof without changing logical operation ID;
45. queued operation whose subject authority was revoked does not mutate remotely;
46. limited-use token consumed but application logic fails → no false commit receipt;
47. authoritative commit succeeds but response is lost → fresh-proof retry of same operation resolves to one material effect;
48. same consumed limited-use token replay is detected where replay protection is enabled;
49. privileged server-SDK path cannot rely on client Firestore Rules as end-user authorization;
50. Service Worker/app update during queued work preserves operation lineage and re-adjudicates current admission;
51. Auth/App Check outage preserves unique local evidence and does not downgrade remote authorization;
52. account deletion, stale-device/backup return or backend/attestation migration does not restore predecessor mutation authority or reset dedup lineage.

## CHANGE WATCH — Firebase Extensions lifecycle

Firebase Extensions is deprecated and the managed service shuts down on **2027-03-31**. Installed resources can continue running, but managed update/reconfiguration/uninstall/config export disappears. Official function-kit replacements are not guaranteed for every extension. Migration tooling warns that forced cutover can cause brief downtime while Eventarc provisions.

This is operationally relevant only if a future production deletion/admission path actually depends on an extension. That production fact remains OPEN.

Sources:
- https://firebase.google.com/docs/extensions/faq-and-troubleshooting
- https://firebase.google.com/docs/extensions/users/migrate
- https://firebase.google.com/docs/extensions/migration-best-practices

## MINTTAP DECISION

For LogMate-like offline PWA Sync, do not bind durable queued intent to transient Auth/App Check credentials. Preserve one logical operation identity, reacquire current admission proof at each eligible attempt, and keep authoritative idempotency/receipt/reconciliation independent of attestation-token replay protection.

Do not infer a Firebase/App Check/Firestore production architecture from this generic gate.

## OPEN

Canonical LogMate `main` remains `059d643f080781cce71f1bd00ccef659a446de8c` at this checkpoint. Production Sync admission/dedup/receipt/reconciliation, App Check use/enforcement, Auth revocation policy, privileged-backend design, account-deletion behavior and physical Safari/Home-Screen/representative managed-iPad validation remain OPEN.

## Gate

**PASS generic. NO production PASS.**
