# 522 — Applied Stage 8: Offline UTC LWW Clock Trust, Recovery and Remote-Admission Boundary

**Reviewed:** 2026-10-27 KST. **State:** SOURCE + SYNTHESIS + CONTRADICTION + bounded 20/20 synthetic Node model; exact Dart/compiled-Web/remote Sync/managed EFB VALIDATION OPEN. **Owner:** E Web Architecture, Security & Operations. A supplies clock/browser mechanics, C independent execution, B status/recovery UX, D claim governance. Web Manager coordinates; PWA is cross-track, not a sixth track.

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

[Research-only Node model](handoffs/pwa_lww_clock_policy_model.mjs) was executed on **Node v22.16.0, 2026-10-27**, **20/20 deterministic checks PASS**. It implements only the stated UTC ordering, UTF-8 ordinal tie-break and same-ID/digest rule with synthetic one-record fixtures. Cases T01–T20 cover delivery inversion, tie-break, retry/collision, future clock, correction/tombstone dominance, old backup restamping counterexample, rollback, operational-date separation, precision collision, offset normalization caveat, serverSequence separation, anomaly-warning independence, owner check omission and history custody.

**Independence/negative controls:** T10 deliberately demonstrates the *incorrect* restamp-on-import rule; T17 deliberately demonstrates that a pure comparator does **not** enforce owner isolation; T14's strict `Z` parser is a model choice, **not** a claim that the approved wire format forbids RFC 3339 offsets. A 6-hour anomaly threshold in T16 is arbitrary demonstration-only, not an approved operational threshold. T19 explicitly falsifies a first model draft that used JavaScript \`Date.parse\` millisecond timestamps and would have collapsed distinct microsecond edits into a false tie; the corrected model compares exact six-digit microseconds using \`BigInt\`. T20 rejects nonexistent calendar dates rather than accepting normalized parser output. This correction is a **research-oracle hardening**, not proof of the product's actual timestamp precision. This model does not execute LogMate Dart, Flutter Web, Sembast, Firebase, actual iOS/iPadOS, managed MDM, real LBK or remote Sync. PASS means the model behaves as written, not that product behavior is correct.

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

---

## 8. Applied continuation — UTF-8 identity ordering, cross-runtime tie-break and Flight identity admission (2026-10-27)

**Gate:** SOURCE + SYNTHESIS + CONTRADICTION + 18/18 local Node synthetic diagnostics PASS; actual LogMate Dart comparator, compiled Web, authenticated remote Sync, alias resolution, Safari and managed EFB **NOT EXECUTED / OPEN**. This extends §§3–7's approved UTC LWW policy without changing it. Track E owns remote admission and release consequences; A owns encoding/browser mechanics; C owns independent execution; B/D consume UX/claim implications.

### 8.1 Pinned product and standards [SOURCE]

- [LogMate approved Manual Delta Sync contract](https://github.com/yhappcom/logmate/blob/main/docs/specs/local-first-manual-delta-sync-contract.md), approved 2026-10-17, §§2–5, 7, 10–12: equal original modifiedAtUtc for different operations uses **normalized Operation ID UTF-8 bytewise lexicographic** tie-break, not locale collation or server delivery order. Same ID+digest is retry; same ID/different digest rejects. Distinct CREATEs also require a **separate** Owner + operational LocalDate + confirmed complete Airline FlightIdentifier identity gate; material sector conflict is REVIEW_REQUIRED. Production Manual Sync and server comparator are not implemented.
- Source inspected read-only 2026-10-27: [local_manual_identity_factory.dart](https://github.com/yhappcom/logmate/blob/main/lib/application/logbook/local_manual_identity_factory.dart) generates 16 random bytes as **32 lowercase ASCII hex digits** for normal local IDs. [repository_types.dart](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/repository_types.dart) OperationId(String) checks nonblank only, not hex/ASCII/NFC/well-formed Unicode. [sync_persistence.dart](https://github.com/yhappcom/logmate/blob/main/lib/repository/logbook/sync_persistence.dart) encodes modifiedAtUtcMicros as a **decimal string**, creates its own key-sorted JSON digest and has no remote decoder/winner comparator. F1 tests cover local binding/digest, not remote admission.
- [LogMate roadmap §4.4](https://github.com/yhappcom/logmate/blob/main/docs/roadmap-reconciliation-2026-10-24.md) explicitly marks original UTC preservation across mutation kinds, backup versions and remote Apply NOT VERIFIED; only supported simple Flight CREATE is F1 eligible.
- [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629) defines UTF-8 and scalar-value byte ordering. [ECMAScript](https://262.ecma-international.org/) / [MDN Array.sort](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) ordinary JS string order uses UTF-16 code units. [RFC 8785 §3.2.3](https://www.rfc-editor.org/rfc/rfc8785.html) explicitly uses UTF-16 **JSON property-name** sorting, which is not the approved **Operation ID UTF-8** tie-break. [WHATWG Encoding](https://encoding.spec.whatwg.org/) replaces lone surrogate code units during UTF-8 conversion; [ECMAScript normalize](https://tc39.es/ecma262/#sec-string.prototype.normalize) is explicit, not automatic. No claim is made that the product's custom JSON encoder implements JCS.

### 8.2 Failure-mode and positive-control matrix [SYNTHESIS / CONTRADICTION]

| Case | Exact consequence | Evidence boundary |
| --- | --- | --- |
| Two normal generated 32-hex IDs | UTF-8 byte order agrees with UTF-16 order | **Positive current-scope protection**; no observed production mismatch |
| Equal UTC, ID X=U+E000, ID Y=U+10000 | UTF-8 X < Y, but JS UTF-16 X > Y | A default JS/Dart/server string comparator could choose the opposite winner **if non-ASCII IDs are admitted**; future-wire conditional, not shipped defect |
| ID U+00E9 vs e + combining acute | Distinct bytes, potentially identical after NFC | “Normalized ID” profile and migration timing are unspecified; silent normalization after digest/receipt changes identity |
| Lone surrogate U+D800 vs U+FFFD | Node UTF-8 encoding replaces lone surrogate with U+FFFD | Different JS strings can become identical bytes; reject malformed IDs or define an explicit reversible wire profile |
| Microsecond instants differing by 1 μs | JS Date.parse can collapse to same millisecond | Compare exact integer microseconds, not Date or floating Number; F1 decimal-string encoding is a positive source control |
| Distinct CREATE Record IDs, same date/complete flight number | Per-Record LWW cannot merge them by itself | Independent verified alias/identity admission needed; sector conflict must remain reviewable |
| Future-stamped DELETE vs later real-world UPDATE | Approved UTC LWW may retain DELETE as current | Encoding correctness cannot repair the owner-approved clock-skew trade-off; retain losing history |

**Key distinction:** Operation ID is a secondary deterministic tie-break, **not** a chronological sequence number or universal Record identity. The OperationId type comment prohibiting canonical Sync ordering can be read consistently as prohibiting use as a *primary* time/sequence key; it does not negate the explicitly approved equal-UTC tie-break. UTF-16 JSON key ordering cannot be reused for the UTF-8 Operation ID comparator. The currently generated hex IDs avoid the Unicode ordering contradiction; the permissive public constructor and future remote import make it a **pre-implementation contract/test requirement**, not a present exploit.

**Conditional convergence proof:** For an already admitted **same stable Record**, the same immutable operation set, an exact total order on (original UTC microseconds, normalized UTF-8 ID), and same-ID/digest collision rejection yield an arrival-order-independent winner. This does **not** prove whole-ledger convergence: independent CREATEs need an alias mapping, and sector mismatch, DELETE/RESTORE, user-confirmed Order/Page/Baseline and Custom Definition changes have separate review/structural semantics. A winner comparator alone cannot prove one-flight-once aggregation.

### 8.3 Bounded executable falsification [VALIDATION — SYNTHETIC ONLY]

[Research-only Node diagnostic U01–U18](handoffs/pwa_sync_identity_order_lab.mjs) covers ASCII ordering, BMP/non-BMP reversal, wrong JS-default winner, NFC and malformed surrogate behavior, UTC priority, delivery inversion, equal-UTC tie, same-ID retry/digest collision, far-future integer precision, Date.parse microsecond collapse, future tombstone, independent Record IDs vs Flight key, sector conflict and fixed-valid-ID comparator associativity.

A **local Node 22.16.0 equivalent** completed **18/18 PASS** on 2026-10-27. The GitHub lab was committed for reproducibility; no independent CI run of its exact GitHub blob was retrieved. Deliberate counterexamples are expected results, **not** observed LogMate defects. U12's far-future precision example does not imply that a normal 2026 epoch-microsecond value exceeds JavaScript's safe-integer limit. The lab does not run Dart, compiled Flutter Web, Firebase, alias resolution, Sembast, Safari or managed iPad.

### 8.4 Exact-product acceptance and decisions [VALIDATION PLAN / DEPENDENCY]

| Gate | Required positive and negative oracle | Owner |
| --- | --- | --- |
| ID01–03 | Dart, compiled Web and server use one documented normalized ID profile. Test normal hex, non-ASCII BMP/non-BMP, NFC-equivalent, malformed-surrogate and invalid UTF-8 IDs. Reject unsupported IDs before publication or prove UTF-8 bytewise comparison; never silently rewrite existing IDs/digests. | Engineering Sync + A/C |
| ID04–06 | Pin exact original UTC microsecond wire precision/range and integer roundtrip, same-time tie and malformed time rejection; no covert clock correction or Number/Date precision loss. | Engineering + E/C |
| ID07–09 | Same-ID/same-digest ACK-loss retry, same-ID/changed-digest reject, opposing server arrival order and multiple-replica convergence with losing Revision/payload preserved. | Engineering + E/C |
| ID10–12 | Two offline CREATEs with verified same complete Airline FlightIdentifier/date: one canonical alias/aggregate with both source histories; conflicting sector REVIEW_REQUIRED without double count or silent merge; partial flight IDs, GA and Simulator excluded from unsupported inference. | Product Sync/Import + C |
| ID13–15 | Future DELETE vs later real-world UPDATE, explicit RESTORE, old LBK replay and A→B→C transfer preserve original UTC/ID/digest; Owner/stream/current-policy admission is independent. | Product Sync/Backup + E/C |
| ID16–18 | Reopen, two browser tabs, installed Safari and representative managed EFB: inspect record/history/outbox/37-store state, Receipt/cursor, truthful Sync state and no assumed background or native-storage sharing. | A/C + Engineering, B/D transfer |

**MINTTAP DECISION — existing vs proposed:** Approved UTC LWW, UTF-8 tie-break, no inter-device clock correction, immutable IDs and explicit review/restore remain unchanged. **Proposed, not approved:** specify/version a strict ID wire profile (prefer preserving existing 32-hex path), require exact byte comparator if Unicode admitted, define UTC precision/range, and prove Flight alias admission independently. No silent narrowing of historical IDs, retroactive normalization, localeCompare or JSON-key sort substitution. Owner/Engineering approval is needed for wire restrictions or migrations.

**TRANSFER VALIDATION:** Design Studio Web Stage 3/W121 still lacks installed-browser/human/AT recovery sign-off; distinguish Saved locally, Review duplicate, Sync pending, Server accepted, Current winner and Recoverable history. Marketing D8–D10 must not claim seamless merge, unattended Sync or guaranteed latest human edit. Software Engineering D006 owns generic replication/convergence and Q004/Q006 independent oracle discipline; Web Manager owns browser encoding/managed-iPad release-admission transfer, not duplicate foundations.

**OPEN:** actual product ID normalization, remote comparator/decoder, non-ASCII admission, timestamp range/precision, cross-device Flight alias implementation, browser/Dart/managed EFB execution. **CHANGE WATCH:** OperationId constructor/generator, F1 encoder, future server comparator, compiler runtime, Unicode/encoding, Safari/MDM. **Stop check:** encoding, precision, alias, duplicate admission and cross-track consequences were integrated in one pass; the next decisive step requires exact implementation/runtime evidence, not another synthetic model. **Gate unchanged:** Stage 8 applied ACTIVE · Production validation OPEN · PWA release HOLD.


---

## 9. Exact committed synthetic-oracle CI provenance and false-green controls (2026-10-28 KST)

**Scope / SOURCE.** This checkpoint does not add a new Sync policy or infer a LogMate product test. It resolves the prior §8.3 gap between a *local equivalent* Node execution and an execution of the **exact committed GitHub blobs**, while reusing the backup/restore findings owned by [298](298_pwa_durable_local_state_device_backup_restore_failure_domain_contract.md). Read-only authorities rechecked: [LogMate approved Manual Delta Sync contract](https://github.com/yhappcom/logmate/blob/d3bc214fe9b4b7bf84702f898b4e6993a4127e2f/docs/specs/local-first-manual-delta-sync-contract.md) (2026-10-17, implementation NOT COMPLETE); [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629) for UTF-8 ordinal byte semantics; [ECMAScript Array.sort](https://tc39.es/ecma262/#sec-array.prototype.sort) for default string comparison; [GitHub workflow token least privilege](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication). The last three are standards/platform/workflow sources, not observations of LogMate runtime.

**Actual hosted execution / VALIDATION.** [GitHub Actions run 40528164581](https://github.com/yhappcom/web-manager/actions/runs/40528164581), job **122273315436**, executed on GitHub-hosted `ubuntu-24.04`, Node **v22.16.0**, exact checkout **`0ac172bdfbd9e0d1c2cdc5a7fb8392e08d0853ba`** at 2026-10-27 15:09 UTC (2026-10-28 00:09 KST). All four independently stored public research scripts executed and the workflow passed **61 bounded synthetic checks**: 18 Operation-ID/Unicode ordering, 20 UTC-clock/tombstone policy examples, 13 JavaScript JSON semantic-ambiguity checks and 10 repeated-restore hold-key model tests. Node syntax checks passed; the workflow additionally required the expected **18/18, 20/20, 13/13, 10/10 and zero-failure** output signatures. This closes **exact committed public Node model CI execution**, not product correctness, model independence from its own assertions, Dart/Web parity, real file restore or managed-EFB validation.

**Failure and correction / CONTRADICTION.** Initial [run 40528043894](https://github.com/yhappcom/web-manager/actions/runs/40528043894) also completed all four scripts, but had no explicit fixed-case-count gate. The first attempt to add fixed-count checks produced a malformed workflow; [run 40528108635](https://github.com/yhappcom/web-manager/actions/runs/40528108635) failed **with zero jobs**, a workflow-definition NON-EXECUTION, **not** a failed model or product assertion. The workflow was corrected and rerun successfully as 40528164581. This is a concrete demonstration that a red workflow can mean syntax/non-execution and that a dynamic `n/n PASS` string is weaker than an independently checked expected case count. Fixed counts still cannot establish whether an oracle's expected behavior is correct.

**Operational control / SYNTHESIS.** The canonical [public-only workflow](https://github.com/yhappcom/web-manager/blob/main/.github/workflows/stage8_public_synthetic_oracles.yml) uses `permissions: contents: read`, pinned checkout/setup-node action commits, `persist-credentials: false`, bounded timeout, explicit source SHA and no private LogMate checkout, fixture, secret, Firebase account, production endpoint or device. The previous private-LogMate checkout failure documented in 298 is not silently bypassed by this workflow. Avoid confusing public reproducibility with authorization to access private product source. For any future product-level CI, use an Engineering-authorized, isolated target and a separate independent oracle with negative/failure cases.

**Five-track decision / DEPENDENCY and TRANSFER VALIDATION.** **E** remains highest-risk owner for remote admission, data custody and release authorization. **A** owns UTF-8/UTF-16/clock/browser semantics and supplies the standard-based expected values. **C** owns the exact-source CI, fixed-count/non-execution distinctions and eventual Dart/compiled-Web/physical-device failure oracles. **B** consumes the unresolved Saved locally / Sync pending / Server accepted / Conflict review distinctions through Design Studio W121, which remains Stage 3 PRACTICE. **D** consumes privacy-minimized claim evidence through Marketing D8–D10 HOLD; a synthetic green workflow cannot support seamless PWA/Sync claims. Software Engineering [VALIDATION_STANDARD](https://github.com/yhappcom/software-engineering-studio/blob/main/methods/VALIDATION_STANDARD.md) remains the implementation-level claim→oracle→environment→observation→limit owner.

**Gate and adjacent-question stop check / OPEN.** Generic public-model CI is now **EXECUTED PASS** at its bounded level. **Actual LogMate Manual Sync remains NOT IMPLEMENTED**, and the independent Dart comparator, compiled Web/JS, authenticated server, real Flight alias, LBK v2 FILE custody, Safari Home Screen and managed EFB tests remain **OPEN**. Highest-value next action is an authorized exact-product W-012→W-013→W-014 and dual-replica ID01–ID18 execution, not adding more model-only variants. **Applied Stage 8 ACTIVE · Production validation OPEN · PWA release HOLD.**
