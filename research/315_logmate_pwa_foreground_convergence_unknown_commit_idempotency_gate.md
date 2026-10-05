# 315 — LogMate PWA Foreground Convergence, Unknown-Commit Recovery & Idempotency Gate

Status: **PASS (generic/platform + canonical-source integration) / production Sync protocol + runtime + physical/managed-iPad validation OPEN**  
Evidence date: 2026-10-05  
Curriculum: Stage 8 Security / Privacy / Trust continuous expert application  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A HTTP/browser/Service-Worker mechanics; Track C fault-injection validation; Track B Sync-state semantics; Track D privacy-aware diagnostics.

## Why this checkpoint exists

313 established that persistent origin storage is not backup or remote convergence. 314 established the authenticated/authorized server boundary for LogMate operational Sync metadata. The next unresolved correctness problem is what happens after an offline PWA has a durable local mutation but the network/process fails while remote outcome is uncertain.

A company-iPad EFB must not require unattended Background Sync for correctness. It also must not translate a timeout, process termination or lost response into a second logical flight mutation.

## Canonical evidence read

At run start Web Manager `main` was `ad826c92cfdc2d0bfac98d1d942469f7ac35fba3`. Required operating files, 313/314, research index and recent commits were read.

Canonical LogMate `main` was `059d643f080781cce71f1bd00ccef659a446de8c`. The frozen `accountOperationalMeta/{uid}` authority contract remains, while production ledger Sync storage, receipts, cursors, ordering, bootstrap and reconciliation remain future contracts. No current canonical-source evidence promotes a production Background-Sync or exactly-once implementation to PASS.

Latest Design Studio evidence is roster/parser research and does not close PWA runtime gates. Latest Software Engineering Studio evidence concerns screen/theme architecture, not Sync. Marketing's latest MintTap audit adds an important transfer rule: currently accessible source that cannot reproduce a claimed shipped behavior must not be promoted to production evidence.

## SOURCE — HTTP retry semantics

RFC 9110 defines an idempotent method by intended server effect. Its practical reason is directly relevant: when a connection closes before the client can read a response, an idempotent request can be retried even if the original may have succeeded. A client should not automatically retry a non-idempotent request unless application semantics make it idempotent or the client can determine the original was not applied.

Sources:
- https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods
- https://www.rfc-editor.org/rfc/rfc9112.html#name-retrying-requests

## SOURCE — Background execution is not portable convergence authority

MDN currently marks Background Synchronization and `ServiceWorkerRegistration.sync` as Limited Availability / not Baseline. Periodic Background Sync and Background Fetch are also limited/experimental.

WebKit documents standards-based Web Push for iOS/iPadOS Home-Screen web apps and bounded background push handling. That proves some event-driven background capability, not connectivity-return outbox convergence.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/sync
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Periodic_Background_Synchronization_API
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/backgroundFetch
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/

## SOURCE — database atomicity does not create request exactly-once

Firestore transactions never partially apply successful writes, but the transaction function may run more than once after concurrent edits. Firestore-triggered Cloud Functions document at-least-once event delivery and no ordering guarantee, and explicitly require idempotent functions.

Sources:
- https://firebase.google.com/docs/firestore/manage-data/transactions
- https://firebase.google.com/docs/firestore/extend-with-functions

## SYNTHESIS — UNKNOWN is a first-class state

A client can know that it transmitted a mutation without knowing whether the authoritative server committed it.

Persistent guards:
- `request failed locally ≠ server did not commit`;
- `timeout ≠ rejection`;
- `ACK missing ≠ commit missing`;
- `connection closed ≠ operation absent`;
- `UNKNOWN outcome ≠ safe to mint a new operation identity`;
- `transaction atomic ≠ request exactly once`;
- `event delivered ≠ delivered exactly once`;
- `network restored ≠ foreground Sync`;
- `Service Worker supported ≠ Background Sync supported`;
- `background opportunity ≠ convergence`.

## Portable convergence contract

The portable correctness path is:

`local transactional mutation → durable outbox → eligible foreground authenticated Sync → idempotent server admission/commit → receipt/ACK → durable local acknowledgement → reconciliation`

Foreground convergence does **not** mean a manual Sync button is mandatory. Launch, resume, auth-ready and eligible foreground reconnect can automatically drain pending work. Correctness must still hold when the PWA receives no useful execution while suspended or terminated.

Background facilities may later accelerate convergence if independently validated. They must not be a prerequisite for preserving unique pilot records.

## Stable logical operation identity

A retry of one logical user intent must retain one stable operation identity across:
- reload;
- PWA termination;
- device reboot;
- network retry;
- authentication refresh;
- Service Worker replacement;
- response loss.

Conversely, equal payloads are not proof of equal user intent.

Guards:
- `same payload ≠ same logical operation`;
- `retry of same logical operation ≠ new operation ID`;
- `same operation ID + contradictory immutable intent ≠ silently accepted retry`.

The exact identifier format, generation mechanism, admission store and retention period remain Software Engineering / product-contract decisions. This checkpoint defines required semantics, not implementation syntax.

## Failure windows

Use explicit fault windows rather than a generic “sync failed” state:

- **W0** local intent exists before durable local transaction;
- **W1** ledger/outbox durable, request not transmitted;
- **W2** request transmitted, authoritative outcome UNKNOWN;
- **W3** server committed, response/ACK not observed;
- **W4** ACK observed, local acknowledgement not yet durable;
- **W5** local acknowledgement durable, reconciliation incomplete;
- **W6** reconciliation complete.

W2–W5 must survive retry/restart without creating a second material effect for the same logical operation.

## Dedup/admission and retention boundary

Idempotent admission needs an authoritative way to recognize a previously admitted operation. A dedup record that expires before the supported offline/retry horizon can re-open duplicate-effect risk when an old client returns.

But indefinite retention is not automatically justified. Dedup/receipt retention must be reconciled with:
- maximum supported offline/retry horizon;
- backup/restore and stale-device return;
- account deletion;
- privacy/data minimization;
- protocol/schema migration;
- operational incident evidence.

Guard: `dedup record expired ≠ old client can safely mint/replay as new intent`.

No retention duration is invented here.

## Track transfers

### Track A — Web Platform & Browser
Own HTTP retry semantics, foreground lifecycle opportunities, Service-Worker/background capability distinctions and Safari/Home-Screen behavior. Do not convert API presence into delivery guarantee.

### Track B — Web UX / IA
Keep user-visible states semantically separate:
`Saved on this device → Waiting to sync → Syncing → Verifying outcome → Remotely acknowledged → Reconciled / Needs attention`.

Do not label UNKNOWN as definitively failed if the server may have committed. Do not promise “will sync automatically when online” until the target iPad lifecycle actually proves that claim.

### Track C — Performance / Accessibility / Quality
Fault-inject every W0–W6 boundary. Accessibility applies to Sync status/recovery messaging as well as happy-path controls. Automated/emulator PASS does not promote Safari/Home-Screen/physical/managed-iPad behavior.

### Track D — Search / Discovery / Analytics
Diagnostics observe; they do not elect authority. Payload-free useful signals include pending-count bucket, oldest-pending-age bucket, retry count, UNKNOWN duration, outcome class and reconciliation latency. Do not collect flight-record payload merely to diagnose retry behavior.

### Track E — Architecture / Security / Operations
Own authenticated admission, authorization, receipt semantics, dedup retention, reconciliation, deletion interaction and incident evidence. 314's identity/Rules/IAM boundary remains prerequisite.

## Deterministic validation bundle

Minimum product-level cases:

1. offline mutation creates ledger + durable outbox atomically;
2. reload preserves operation identity;
3. process termination preserves identity;
4. device reboot preserves identity;
5. foreground reconnect drains eligible work;
6. suspended reconnect is not assumed to drain;
7. terminated-app reconnect is not assumed to drain;
8. terminate before request → one later effect;
9. terminate after send/before response → one effect after recovery;
10. server commit + response loss → replay resolves without duplicate effect;
11. ACK observed + crash before local ACK persistence → replay resolves safely;
12. local ACK persisted + crash before reconciliation → recovery completes reconciliation;
13. concurrent duplicate submissions of same operation → one material effect;
14. same operation ID with contradictory immutable intent → deterministic reject/conflict;
15. expired auth while queued → no unauthorized mutation;
16. refreshed auth → same logical operation can resume according to policy;
17. revoked/unauthorized account → queued mutation does not bypass current authorization;
18. transient 5xx/timeout → UNKNOWN/retry policy does not mint new intent;
19. Service Worker update during pending work → outbox/identity preserved;
20. executable-cache retirement → ledger/outbox unchanged;
21. Safari tab foreground recovery;
22. Home-Screen foreground recovery;
23. physical-iPad termination/reboot recovery;
24. representative managed-EFB restriction/network recovery;
25. duplicate admission after long offline interval inside supported horizon;
26. stale retry beyond dedup horizon follows explicit safe policy;
27. account deletion includes operation/receipt metadata according to retention policy;
28. final reconciliation proves one logical intent maps to one intended remote material effect.

## CONTRADICTION / transfer validation

Marketing's 2026-10-05 production-source authority correction is directly reusable as an evidence-governance rule: source-level claims that cannot be reproduced from the currently authoritative source must be downgraded, not defended by prior narrative. Apply the same rule to LogMate Sync. A future UI, design note, emulator test or generic Firebase capability cannot establish deployed Sync behavior.

No contradiction was found with Design Studio or Software Engineering evidence because neither currently claims production Sync convergence.

## MINTTAP DECISION

For LogMate-like EFB use, design correctness around durable local state plus foreground convergence. Treat Background Sync/Web Push/background execution as optional, separately validated accelerators.

Do not claim exactly-once transport. Require idempotent application semantics such that retries of one stable logical operation converge to one intended material effect.

## OPEN / VALIDATION

Still OPEN:
- canonical LogMate operation/record identity schema;
- production Sync API and authoritative admission store;
- receipt/status-query contract;
- ordering/conflict/version semantics;
- reconciliation algorithm;
- dedup/receipt retention duration;
- deployed auth/revocation/Rules/IAM from 314;
- physical Safari/Home-Screen behavior;
- representative managed-EFB behavior;
- deletion/privacy/aviation retention obligations;
- backup/restore interaction with pending outbox and operation identities.

## CHANGE WATCH

Revalidate Background Sync, Periodic Background Sync, Background Fetch and WebKit/iPadOS lifecycle support on material browser/OS changes. Capability expansion can improve latency/convenience; it does not erase the need for replay-safe convergence.

## Gate result

**PASS** for generic protocol/platform reasoning and canonical-source integration.  
**NO production PASS.** Product promotion requires an actual LogMate Sync contract/implementation plus deterministic fault-injection and physical/managed-iPad evidence.
