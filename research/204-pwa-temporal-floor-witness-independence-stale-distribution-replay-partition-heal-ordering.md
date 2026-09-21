# 204 — PWA Temporal-Floor Witness Independence, Stale-Distribution Replay & Partition-Heal Ordering

Status: **PASS (generic) / PRODUCT + WITNESS + REGION + TIME-TOPOLOGY + IDENTITY + PROVIDER + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime state mechanics; Track B recovery/degraded-state semantics; Track C destructive assurance; Track D bounded monitoring.  
Dependencies: 171–203, especially 199–203.

## Problem

203 separated temporal/currentness epoch issuance, admission, distribution, observation and enforcement. The next failure class appears when a partition leaves multiple authentic but differently aged floor statements, a restored node replays an older distribution message, or a witness survives the incident but is accidentally treated as a unilateral authority.

Central rule: **a witness/floor can constrain rollback without becoming authority to invent a successor. Authenticity is insufficient for freshness, and partition healing must converge monotonically before consequence-bearing traffic is reopened.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Service Worker, IndexedDB, Cache Storage and client clocks can retain observations but cannot witness global authority or prove partition order.
- **B UX/IA/Content:** high dependency pressure. Consumes `LOCAL-ONLY`, `EPOCH-STALE`, `FLOOR-CONFLICT`, `RE-ADMISSION REQUIRED`, `QUARANTINED`, `UNKNOWN` semantics without implying local-data loss.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns replay, fork, partition-heal, restore and offline-client destructive tests. Campaign reaches 392 defined cases; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Monitoring can surface conflicting heads/floors but cannot elect one.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns witness independence, stale-distribution rejection, lineage ordering and monotonic partition healing.

## SOURCE

### RFC 9162 — consistency proves append-only extension; view consistency still needs cross-observation

RFC 9162 defines Merkle consistency proofs: a later tree can prove that an earlier tree is an exact prefix, rather than merely presenting another valid signature. It separately identifies consistency of the log view presented to all query sources as something auditors/monitors must check; failure can yield signed evidence of misbehavior.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** authenticated lineage/consistency proof is a useful precedent for ordering observations without wall-clock or majority election. Certificate Transparency is not adopted as MintTap architecture.

### TUF — rollback, fast-forward and freeze are distinct freshness attacks

TUF explicitly distinguishes rollback, fast-forward and indefinite-freeze attacks. A larger version number is therefore not automatically safer: an attacker can fast-forward metadata to poison future update acceptance, while repeated authentic old metadata can freeze a client.

Sources:
- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/spec/

**TRANSFER VALIDATION:** monotonic version/floor checks require authenticated succession and bounded currentness; `highest observed generation wins` is not a safe generic election rule.

### Sigstore/Rekor — transparency requires monitoring; one signed checkpoint is not global non-equivocation

Sigstore documents Rekor as append-only and cryptographically verifiable, while also stating that long-term trust requires monitoring. Its threat model recommends consistency auditing and communication among monitors to detect inconsistent views. Rekor checkpoints bind log identity, tree size and root hash, but monitoring remains necessary.

Sources:
- https://docs.sigstore.dev/about/security/
- https://docs.sigstore.dev/about/threat-model/
- https://docs.sigstore.dev/logging/overview/

**TRANSFER VALIDATION:** independently retained checkpoints/witness observations can constrain rollback and expose equivocation, but a witness is not automatically authorized to create policy/currentness successors.

### Sigstore timestamp evolution — signed evidence can still depend on the wrong clock/trust domain

Sigstore documents that Rekor v1 integrated time came from Rekor's internal clock and was not externally verifiable; Rekor v2 uses a timestamp authority separate from Rekor. This is a useful current example of separating log inclusion from time authority.

Source: https://docs.sigstore.dev/cosign/verifying/timestamps/

**TRANSFER VALIDATION:** witness/log independence has dimensions: administrative, storage, identity/key, network, clock/time and recovery. Different service names do not prove independent failure domains.

## SYNTHESIS 1 — witness independence is multidimensional, not binary

A useful witness/floor claim records independence across at least:
- administrative control and privileged identities;
- signing/recovery keys;
- storage/backup/PITR;
- deployment/control plane;
- network/routing dependency;
- time source;
- monitoring/alert path;
- recovery/reconstitution authority.

A witness sharing one of these may still add evidence, but the correlated failure must remain explicit.

Persistent guards: `separate endpoint ≠ independent witness`; `separate storage ≠ independent administration`; `witness survived ≠ witness may authorize successor`.

## SYNTHESIS 2 — witness is a constraint oracle, not a successor oracle

A witness can say: "I previously observed admitted floor F / checkpoint H." That can reject F-1 or a history inconsistent with H. It cannot, solely because it survived, declare F+1 current, choose among conflicting successor lineages, authorize a replacement time source, or lower policy requirements.

The safe generic role is **anti-rollback constraint + contradiction evidence**. Successor admission remains with current policy/recovery authority.

`witness can reject rollback ≠ witness can create currentness`.

## SYNTHESIS 3 — stale but authentic distribution is replay, not recovery

A distribution message needs more than a valid signature. Generic admission should bind:
- lineage/predecessor or consistency relationship;
- generation/floor identity;
- target enforcement domain where applicable;
- policy/key epoch;
- freshness/expiry or other bounded-currentness semantics where the design requires it;
- anti-rollback comparison against locally/independently retained floor evidence.

After restore or partition, a valid old message below the admitted floor remains stale. Reboot, cache loss, PITR or control-plane outage does not reset the recipient's security history.

`signature valid ≠ distribution current`; `restore completed ≠ rollback floor reset`.

## SYNTHESIS 4 — E+1 versus E+2 requires authenticated lineage, not numeric maximization

If E+1 and E+2 are both observed, ordering is safe only when E+2 is authenticated as a legitimate successor/extension under the relevant policy. Numeric magnitude alone is insufficient because fast-forward poisoning is a known class of attack.

Possible generic states:
- **LINEAR SUCCESSOR:** E+2 proves authorized succession from E+1/current lineage;
- **CONCURRENT/CONFLICTING:** both valid-looking but no admissible ordering proof;
- **STALE:** candidate is below an already admitted floor;
- **UNKNOWN:** required lineage/currentness evidence is unavailable.

Do not resolve CONCURRENT/CONFLICTING by wall-clock, region majority, availability, largest integer or telemetry count.

`higher generation ≠ authoritative successor`.

## SYNTHESIS 5 — partition healing is a staged security transition

Generic heal sequence:
1. stop consequence-bearing routing across unresolved conflicting enforcement domains;
2. preserve unique data and conflicting evidence;
3. obtain current independent-enough floor/witness/policy evidence;
4. classify candidate lineages as successor, stale, conflicting or unknown;
5. admit one current lineage only through authorized succession/reconstitution rules;
6. distribute without lowering any already admitted floor;
7. invalidate/quarantine stale authorization caches, sessions or queued authority assumptions;
8. run retired-authority negative and current-authority positive probes per consequential surface;
9. reconcile restored/PITR nodes and long-offline clients;
10. reopen remote consequence-bearing routing only for scoped converged surfaces.

`partition healed at network layer ≠ authorization partition healed`.

## SYNTHESIS 6 — healing order must not transiently re-enable retired authority

A dangerous sequence is reconnect → resume traffic → refresh policy. A stale region can briefly accept retired authority before learning the new floor.

Safer generic ordering is **quarantine/re-admission first, current floor second, enforcement proof third, traffic reopening last**. Exact mechanisms are implementation-dependent and remain OPEN.

`connectivity restored ≠ traffic safe to resume`.

## SYNTHESIS 7 — witness conflict is incident evidence, not a quorum shortcut

Two witnesses may hold incompatible authentic checkpoints. That can indicate partition, delayed observation, stale replay, restoration error or equivocation. Without a specified admitted lineage/quorum policy, count cannot decide truth.

A quorum, threshold or witness set can only be relied upon if its membership, independence assumptions, succession and compromise recovery are themselves governed. This study does not invent a MintTap quorum.

`more matching witnesses ≠ authority unless policy says so and assumptions hold`.

## SYNTHESIS 8 — long-offline PWA heals forward without replaying every missed epoch

A company iPad may reconnect after E→E+3 while retaining local records created under E. Generic handling:
1. preserve unique local records and provenance;
2. isolate cached session/floor/SW state from remote authority;
3. obtain current authenticated floor and lineage evidence;
4. reject stale distribution/cache state even if still authentic;
5. re-evaluate session/token and queued operations under current authority;
6. re-admit consequence-bearing operations individually or by defined safe batch semantics;
7. preserve historical uncertainty rather than claiming missed epochs were observed.

The client need not download every historical epoch to preserve data, but it cannot use an old authentic epoch to reopen retired authority.

## SYNTHESIS 9 — monitoring is necessary evidence, not admission authority

Track D can compare checkpoint/floor fingerprints, stale-replay rejection rates, regional convergence coverage and offline-client rebootstrap outcomes. Monitoring can reveal equivocation or partial healing. It cannot itself authorize the winning lineage.

`monitor detected conflict ≠ monitor authorized resolution`.

## SYNTHESIS 10 — product claims require scoped proof and explicit UNKNOWN

A generic convergence record should identify:
- lineage/floor admitted;
- witness evidence and independence assumptions;
- stale/conflicting candidates rejected or quarantined;
- enforcement surfaces tested;
- paired negative/positive authorization results;
- restored/PITR/offline-client reconciliation state;
- remaining UNKNOWN surfaces.

Absence of observed conflict is not proof that no hidden stale surface exists.

## Track C destructive campaign — 392 cases total

Add eight high-value cases to the 384-case campaign:

1. restored region receives correctly signed E-1 distribution after previously admitting E+1 — replay rejected;
2. attacker supplies authentic-looking generation E+999 without authorized lineage — numeric maximum does not win;
3. witness W1 and W2 hold incompatible authentic heads after partition — no count/clock election without governed policy;
4. witness survives control-plane loss but shares the compromised recovery identity/KMS — independence claim downgraded;
5. network partition heals and traffic resumes before stale region ingests current floor — retired credential must never gain a transient success window;
6. E+1 and E+2 arrive out of order; E+2 has valid authenticated succession from E+1 — ordered by lineage rather than arrival time;
7. PITR restores control-plane distribution state but independent floor remains ahead — restored state cannot lower floor;
8. long-offline iPad reconnects with authentic E cache after E→E+3; unique local data survives, stale authority is rejected, current queue is re-admitted without rewriting historical observation.

Campaign status: **DEFINED, NOT EXECUTED**. Exact witness/provider topology, regional distribution, identity/key custody, physical iPad/Safari/Home Screen, AT, human and product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Browser persistence can retain a local floor observation but browser storage durability and anti-tamper properties are not assumed. Exact WebKit/Chromium behavior remains runtime evidence.

### E → B
B consumes explicit `FLOOR-CONFLICT`, `EPOCH-STALE`, `LOCAL-ONLY`, `RE-ADMISSION REQUIRED`, `QUARANTINED`, `UNKNOWN` states. UX must preserve user data and explain remote unavailability without claiming data corruption.

### E → C
C receives stale-replay, fast-forward, witness-correlation, partition-heal race, PITR anti-rollback and offline-client forward-convergence cases.

### E → D
D may observe/check consistency and convergence but may not elect authority or suppress unresolved conflict for dashboard simplicity.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN. This artifact defines semantics and operational requirements, not interaction styling.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage with no specialist Foundation PASS. Exact witness storage, cryptographic lineage, regional floor distribution, routing quarantine, restore behavior, PWA queues and positive/negative authorization probes remain implementation/runtime dependencies.

## MINTTAP DECISION / DIRECTION

1. Treat witness/floor evidence as rollback constraint and contradiction evidence, not unilateral successor authority.
2. Evaluate witness independence across administration, keys, storage, control plane, network, time and recovery; do not infer independence from endpoint/vendor labels.
3. Reject authentic stale distribution after restore/partition using admitted floor plus authenticated lineage/currentness evidence.
4. Never elect E+2 solely because its generation is numerically larger; require authorized succession/consistency evidence.
5. Heal partitions monotonically: quarantine/re-admission before floor refresh, prove enforcement before reopening consequence-bearing traffic.
6. Preserve unique offline PWA data while rejecting stale authority and re-admitting remote work under current authority.
7. Keep actual witness count, quorum, provider, floor representation, lineage format, routing and recovery topology OPEN until canonical runtime evidence exists.

## OPEN / VALIDATION

- actual MintTap/LogMate witness/checkpoint/floor topology and independence;
- actual cryptographic lineage/consistency mechanism;
- actual floor persistence across restore/PITR and region rebuild;
- actual regional distribution and routing quarantine ordering;
- actual authentication/session/token/lease behavior during heal;
- WebKit/iPadOS storage/update/background/restart behavior;
- offline queue and Service Worker retry semantics;
- physical-device, managed-EFB, AT, human, safety/legal/aviation validation.

## VALIDATION / GATE

**PASS (generic).** The Web Manager can now distinguish witness constraint from successor authority, reject stale-but-authentic distribution after restore/partition, order candidate epochs through authenticated lineage rather than clock/majority/numeric maximization, and define monotonic partition healing that does not transiently re-enable retired authority. Product/runtime validation remains OPEN.

## Next highest-value adjacent question

**205 — witness-set succession, quorum-policy rollback & equivocation recovery under witness loss.** Determine how witness membership/threshold policy itself changes without letting an old witness set resurrect retired authority; how to recover when enough witnesses are unavailable or compromised without silently weakening the floor; and how a long-offline PWA distinguishes a legitimate witness-set succession from replayed old quorum evidence.