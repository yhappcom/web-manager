# 522 — Applied Stage 8: Offline UTC LWW Clock Trust, Recovery and Remote-Admission Boundary

**Reviewed:** 2026-10-27 KST. **State:** SOURCE + SYNTHESIS + CONTRADICTION + bounded 18/18 synthetic Node model; exact Dart/compiled-Web/remote Sync/managed EFB VALIDATION OPEN. **Owner:** E Web Architecture, Security & Operations. A supplies clock/browser mechanics, C independent execution, B status/recovery UX, D claim governance. Web Manager coordinates; PWA is cross-track, not a sixth track.

## 1. Why this is a distinct high-value Stage 8 bottleneck [HISTORY / DEPENDENCY]

The earlier 298/RB research separated a restored source Operation ID and `eligibleProven` binding from new-device remote authority. The next adjacent question is **whether the approved user-edit-time ordering policy can produce a surprising or hard-to-recover winner after an offline device clock is wrong**, especially when a managed EFB iPad and Native phone each retain a complete local ledger. This is not another Service Worker or LBK primer.

**Product authority:** [LogMate manual-delta Sync contract, main@d3bc214f, approved 2026-10-17](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/specs/local-first-manual-delta-sync-contract.md). It explicitly specifies (1) source-command `modifiedAtUtc` UTC LWW for ordinary record snapshots, (2) **no inter-device clock-skew correction** as an owner decision, (3) normalized Operation ID UTF-8 ordinal tie-break for different IDs at equal UTC, (4) immutable original Operation ID and digest for retries, (5) serverSequence as delivery order rather than winner order, (6) losing Revision/payload history preserved, (7) DELETE tombstones and explicit RESTORE intents, (8) backup/replay cannot acquire a fresh edit timestamp, and (9) Manual Sync production **NOT IMPLEMENTED**. F1 local persistence is partial implemented evidence, not authenticated server convergence.

**Question:** Which consequences follow *logically from the approved policy*, which are only plausible environmental inputs, and what should Engineering test without silently changing the owner's policy?

## 2. Primary mechanics and source maturity [SOURCE / STANDARD / CHANGE WATCH]

- [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339): unambiguous UTC instants, explicit offsets, fractional seconds and leap-second representation. It specifies interchange representation, **not** that a client clock is correct or that later timestamp means later human intent.
- [MDN Date.now, reviewed 2026-10-27](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now): epoch-relative wall-clock reading; browser implementations may reduce precision. [MDN performance.now](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now): monotonic interval measurement is distinct from wall-clock UTC; browser sleep behavior can vary. Neither grants a cross-device globally authoritative edit clock.
- [Dart DateTime.now](https://api.dart.dev/dart-core/DateTime/DateTime.now.html) constructs current local date/time; UTC conversion changes representation, **not clock correctness**. Exact LogMate future `modifiedAtUtc` writer has not been shown to use a particular clock source.
- [RFC 5905 NTPv4](https://www.rfc-editor.org/info/rfc5905/): network time synchronization is a separate protocol/operational service, not a guarantee of trustworthy time on an offline, managed, or user-adjusted iPad. Do not assume NTP reachability or MDM clock settings.
- [Web Manager 298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md) and [521](521_stage8_pwa_sembast_cross_tab_replay_wasm_web_opener_admission_20261027.md) establish backup provenance, restored authority, browser transaction callback replay and current runtime uncertainty. **This study owns only the web/PWA admission and operational consequences of the product's approved ordering semantics**; Software Engineering owns production comparator/wire implementation.

**Four independent time domains:**
1. `modifiedAtUtc`: original accepted user command's UTC instant; product-selected LWW winner input.
2. `serverSequence`: authenticated server delivery/cursor order, not event-time winner.
3. `acceptedAtUtc` / `updatedAtUtc` / `UtcEpochMicros`: existing repository audit fields, **not automatically equivalent** to the new Sync wire field.
4. Flight operational local date and flight UTC/dayOffset: aviation-domain record facts, not Sync mutation time.

A fifth independent notion is server receipt time; it can diagnose anomaly or establish receipt chronology but **must not silently replace** the approved source-command UTC as the winner key. Same-user authentication and valid checksum establish neither clock accuracy nor ordering of real-world intentions.

## 3. Deterministic policy consequences [SYNTHESIS / CONTRADICTION]

| Scenario | Approved LWW result | Important boundary |
| --- | --- | --- |
| Phone edit UTC 10:05, tablet edit UTC 10:00 delivered later | Phone 10:05 wins | Server sequence cannot reverse this |
| Tablet's clock accidentally one day ahead, edits first; phone edits later in real time at normal UTC | Tablet's future-stamped version wins | UTC ordering does not prove real-world intent ordering |
| User explicitly corrects the phone record later, but phone clock is still behind future timestamp | Earlier future-stamped version can continue winning | “Make a new edit” may not remediate until the timestamp exceeds the future value |
| Future-stamped DELETE vs later real-time UPDATE | DELETE can remain current tombstone | Losing UPDATE must remain recoverable history; no silent data deletion |
| Old LBK import or Delta replay | Original `modifiedAtUtc` preserved | Re-stamping on import could improperly revive an older value |
| Two different operations share the same UTC | UTF-8 ordinal higher normalized ID wins | Deterministic but not evidence of which intent occurred later |
| Same ID, different digest | Reject as collision/tampering | Never use timestamp or tie-break to legitimize a changed payload |
| Wrong owner / stale stream | LWW comparison alone can still produce a winner | Authentication/owner/stream/admission checks must happen independently |

**CONTRADICTION:** “UTC timestamp” is a standardized *representation of an instant*, not proof of synchronized clocks; “latest UTC wins” is the **approved policy**, not a promise to recover human chronological intent. A future-dated winner is a **policy trade-off and test case**, not evidence that LogMate currently has an exploitable production Sync defect. Production Sync is absent.

**Important UX implication:** A newer user action can become a *losing* revision even though the app saved it locally. If this occurs, the UI must distinguish “saved locally,” “transmitted,” “server accepted,” “current winning record,” and “recoverable losing revision.” Do not display “your latest correction is active everywhere” from a local success or ACK alone.

## 4. Failure and adversarial taxonomy [SYNTHESIS / OPERATIONAL JUDGMENT]

- **Accidental clock forward:** manual device date change, incorrect system time, restore of an offline device, or a hypothetical time service fault. Each is an input scenario, **not an observed LogMate/iPad event**.
- **Clock rollback:** later user intent can carry smaller `modifiedAtUtc`; monotonic `performance.now()` is only an elapsed-time tool, not a portable cross-reboot UTC replacement.
- **Long offline period:** the application cannot assume it can contact trusted time or Firebase; on reconnect, elapsed time and server delivery order are distinct from original command time.
- **Timestamp precision collision:** same-instant or rounded timestamps invoke deterministic Operation ID tie-break. Cross-platform exact wire precision, normalization, and UTF-8 comparison must be tested; no product wire precision was assumed.
- **Future-dated tombstone:** ordinary record DELETE is subject to LWW; compaction and history retention become important for recovery.
- **Replayed/ported source operation:** preserve original edit time, Operation ID, owner and origin lineage; do not restamp during PWA↔Native file transfer or B→C backup.
- **Malicious same-owner client / corrupted file:** a digest can be recomputed by an attacker controlling the file; authenticated owner, payload validation and policy admissibility are distinct. No external attacker or compromise is alleged.
- **Timestamp parsing ambiguity:** RFC 3339 offsets denote equivalent instants; leap-second, precision and invalid input behavior need an explicit product wire schema, not JavaScript `Date.parse` guesswork.
- **UI/status mismatch:** a local commit or server receipt is not a winning projection or cross-device convergence; disclose review and recovery states without implying an automatic fix.
- **Unbounded clock anomaly telemetry:** raw flight records, UID, Operation ID or precise user clock state must not be leaked into analytics. Diagnostic collection is a separate privacy decision.

## 5. Executed bounded diagnostic [VALIDATION — SYNTHETIC ONLY]

[Research-only Node model](handoffs/pwa_lww_clock_policy_model.mjs) was executed on **Node v22.16.0, 2026-10-27**, **18/18 deterministic checks PASS**. It implements only the stated UTC ordering, UTF-8 ordinal tie-break and same-ID/digest rule with synthetic one-record fixtures. Cases T01–T18 cover delivery inversion, tie-break, retry/collision, future clock, correction/tombstone dominance, old backup restamping counterexample, rollback, operational-date separation, precision collision, offset normalization caveat, serverSequence separation, anomaly-warning independence, owner check omission and history custody.

**Independence/negative controls:** T10 deliberately demonstrates the *incorrect* restamp-on-import rule; T17 deliberately demonstrates that a pure comparator does **not** enforce owner isolation; T14's strict `Z` parser is a model choice, **not** a claim that the approved wire format forbids RFC 3339 offsets. A 6-hour anomaly threshold in T16 is arbitrary demonstration-only, not an approved operational threshold. This model does not execute LogMate Dart, Flutter Web, Sembast, Firebase, actual iOS/iPadOS, managed MDM, real LBK or remote Sync. PASS means the model behaves as written, not that product behavior is correct.

## 6. Policy-preserving controls vs owner decisions [MINTTAP DECISION — PROPOSED, NOT APPROVED]

**Preserve existing approved semantics:** immutable original `modifiedAtUtc`, Operation ID/digest, losing history, explicit RESTORE, serverSequence for delivery only, and user-triggered Manual Sync. Do **not** silently clamp future timestamps, rewrite timestamps at import, change winner to server receipt time, introduce hybrid logical clocks, or convert LWW to server-order wins: each would materially change the owner-approved contract.

**Candidate controls for owner/Engineering review:**
1. **Input/wire admissibility:** validate timestamp syntax/range/precision and identity before remote mutation. Exact accepted range, clock anomaly threshold, policy for offline commands beyond threshold and response UX require owner decision. Hard rejection risks trapping legitimate offline edits.
2. **Non-authoritative anomaly evidence:** compare original source UTC against an independently recorded trusted server time *when available* and flag anomalous skew without rewriting history or deciding winner solely from that comparison. Server time does not reconstruct actual past offline edit chronology.
3. **Explicit recovery:** preserve losing revisions and offer an owner-verified new correction when its timestamp can legitimately win; a future-dated outlier may require a separately approved recovery operation rather than repeated edits or forged timestamps.
4. **Account/stream authority:** verify current authenticated owner, stable record identity, operation digest/idempotency, current server policy and accepted schema before applying LWW. Restored `eligibleProven` evidence cannot grant remote permission.
5. **EFB operational support:** capture OS/browser/MDM clock policy, offline interval, app/Worker generation, UTC encoding, pending operation and last known authenticated contact without assuming background execution or direct device-to-device transport.
6. **Privacy:** diagnostic event categories can say “timestamp anomaly detected” without recording flight payload, UID, exact flight date, operation IDs or full device-clock history.

**Alternative trade-offs (NOT authorized):** server receipt time eliminates one clock-skew comparison but destroys offline original-edit semantics; HLC/causal clocks can preserve additional ordering information but require schema, merge and migration decisions; clamping a future timestamp can alter tombstone/backup/replay outcomes; a blanket future-date reject can block legitimate offline records. None should be adopted as a covert security patch.

## 7. Integrated falsifiable product acceptance [VALIDATION PLAN — NOT RUN]

Use exact product source/commit, normal Flutter/Dart and compiled-Web artifacts, version-matched dependency lock, independent expected values, two distinct replicas and an authorized isolated Firebase emulator. Seed **synthetic** records only. Tie tests to the existing W-012/013/014 and approved Manual Sync implementation work; do not launch a parallel product test initiative.

- **CL01–CL04 — representation and local custody:** original accepted user command generates one stable UTC/Operation ID; local revision/outbox/binding transaction and retries preserve identity; explicit UTC offset/precision/invalid/leap-second contract; equal UTC UTF-8 tie-break independent of locale and JS UTF-16 sorting.
- **CL05–CL08 — ordering and anomaly:** two offline replicas with opposing wall-clock offsets, forward/rollback, equal timestamps and reversed server delivery; assert approved winner plus retained losing payload. Include a future-dated DELETE and later real-world UPDATE; do not silently rewrite timestamps.
- **CL09–CL12 — restore and authority:** v2 37-store LBK A→B→C retains original source edit time and Operation ID; old backup does not resurrect tombstone; wrong UID, same-ID different digest, stale restored binding and unbound/unverified remote admission fail closed. If Sync publisher is absent, mark remote tests NOT EXECUTABLE, not PASS.
- **CL13–CL16 — browser and managed EFB:** same tests under compiled Flutter Web/Sembast Web, Safari tab vs Home Screen separate containers, device restart/offline rejoin, managed iPad clock/MDM/network policy. Explicitly prove file transfer and current server receipts; no unattended sync assumption.
- **CL17–CL20 — human/ops/observability:** user-facing locally-saved vs losing/winning/unknown states, accessible recovery action and no silent history erasure; redacted anomaly telemetry; interrupted Manual Sync/ACK-loss replay; source→artifact→served HTTPS origin→device custody and rollback. Negative controls must execute and produce independent FAIL where injected.

**Independent oracles:** original source `modifiedAtUtc` and command identity, exact winner/tombstone, retained losing revisions, owner/replica/stream state, server receipt/delivery/cursor, no duplicate aggregate, backup semantic snapshot and human/AT status interpretation. A green SHA-256 checksum, later serverSequence, local UI “Saved”, or one-device emulator PASS cannot stand in for these.

## 8. Five-track allocation, specialist transfer and release gate [TRANSFER VALIDATION / DEPENDENCY]

| Track | Current pressure | Specific contribution |
| --- | --- | --- |
| **E** | **Highest**: approved LWW clock trust vs remote admission, recovery and privacy | Own this study; distinguish policy risk, security validation and owner changes |
| **A** | High prerequisite: wall clock, browser Date/performance time, Safari/IndexedDB origin | Supply platform/serialization mechanics; no invented OS guarantees |
| **C** | High independent validation debt | Exact Dart/JS comparator, negative fixtures, dual-replica/device tests and real artifact oracles |
| **B** | UX dependency, Design Studio Stage 3 PRACTICE/W121 | Distinguish local save, losing revision, sync ACK, winner and recovery; no design signoff claimed |
| **D** | Lower immediate implementation pressure, Marketing D8/D9 HOLD | Privacy-minimized observability and no public “automatic conflict-free Sync” claim |

**Peer boundaries:** [Design Studio Web status](https://github.com/yhappcom/design-studio/blob/main/progress/WEB_STATUS.md) has Stage 3 runtime/AT evidence OPEN; [Marketing STATUS](https://github.com/yhappcom/marketing-manager/blob/main/STATUS.md) keeps LogMate PWA/Sync claim HOLD; [Engineering validation standard](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) requires claim→oracle→environment→observation→limit. All peer repositories and LogMate were read-only.

**CHANGE WATCH / OPEN:** future approved Sync wire schema, original `modifiedAtUtc` source/precision, any clock anomaly policy, actual device time controls, Safari/managed iPad execution, backup/export file path, remote admission and real product convergence. **No change to the owner-approved UTC LWW contract is proposed as completed.**

**Adjacent-question checkpoint:** after future-clock dominance, the same study examined deletion/tombstone, replay/restamp, equal-time ties, owner/stream authority, browser precision, operational dates, recoverable history, accessibility and privacy. The next meaningful boundary is an **authorized exact-product two-replica Sync execution and owner decision on anomaly handling**, not more synthetic permutations. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**
