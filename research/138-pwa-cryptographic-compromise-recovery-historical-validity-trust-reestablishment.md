# 138 — PWA Cryptographic Compromise Recovery, Historical-Validity Windows & Trust Re-establishment

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + CRYPTO/KEY + COMPROMISE-DRILL VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 111–121 compromise/containment/normalization; 122–126 evidence/key/verifier continuity; 135–137 provenance/checkpoint/crypto lifecycle; Track A long-offline browser state; Track B truthful recovery UX; Track C destructive compromise validation; Software Engineering owns eventual implementation.

## Purpose

137 separated planned crypto rotation from compromise. This study closes the adjacent generic question: what can still be claimed about historical evidence after a signing/verifier/trust key may have been compromised, and how can successor trust be established without letting the compromised authority simply bless its own replacement?

Central rule:

> **Compromise changes the evidentiary meaning of old-key signatures. Scope claims using independently trustworthy evidence and an explicit uncertainty window; stop current authority immediately enough for the consequence; and re-establish successor trust from an authority/failure domain not solely controlled by the compromised key.**

This study does not select PKI, KMS/HSM, certificate format, timestamp authority, transparency log, algorithm, key hierarchy or product recovery topology.

## 1. Five-track balance

- **A Platform/Browser — high dependency supplier:** long-offline PWA clients may retain old trust state and miss compromise/revocation/rebootstrap messages. Browser lifecycle constrains convergence, not cryptographic truth.
- **B UX/IA/Content — elevated consumer:** owns truthful `historically verified`, `affected window`, `cannot currently verify`, `read/export only`, `re-entry required`, and `current writes blocked` states.
- **C Quality — high dependency pressure:** owns compromise-time ambiguity, stale/offline client, forged successor, rollback, restore and physical-device matrices.
- **D Search/Analytics — constrained consumer:** telemetry can estimate exposure/observed generations but cannot establish compromise time, fleet completeness or historical authenticity.
- **E Architecture/Security/Operations — highest-risk owner:** owns incident scope, revocation/containment, historical-validity policy, successor-trust bootstrap, evidence preservation and normalization.

Allocation remains E-heavy with A/C prerequisites and B consequence communication.

## 2. SOURCE — compromise is a key lifecycle/incident state, not ordinary expiry

NIST SP 800-57 Part 1 Rev.5 remains the current final general key-management recommendation as of this study; NIST also published an initial public draft of Rev.6 in December 2025. NIST key-management guidance treats compromise/revocation as lifecycle concerns and SP 800-61 Rev.3 (April 2025) integrates incident response with cybersecurity risk management and recovery.

Sources checked 2026-09-19:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd
- https://csrc.nist.gov/pubs/sp/800/61/r3/final

**SYNTHESIS:** do not process suspected compromise as a scheduled rollover. Incident evidence, containment, recovery and later normalization are separate phases.

Guards:
- `key expired ≠ key compromised`;
- `key rotated ≠ compromise contained`;
- `new key generated ≠ successor trust established`;
- `incident closed operationally ≠ historical evidence fully classified`.

**CHANGE WATCH:** SP 800-57 Rev.6 is draft, not final; use Rev.5 as current final until NIST changes publication status.

## 3. SOURCE — a valid old-key signature does not establish when it was created

A digital signature proves the cryptographic relation to the key and signed bytes under the verification context. If the private key was later stolen, an attacker can generally create new signatures that also verify mathematically. RFC 5126's long-term-signature model uses trusted time/validation evidence to preserve claims when signing or validation keys are later revoked/compromised. Current CA/Browser Forum Code Signing Baseline Requirements similarly allow a historical compromise/revocation date and describe timestamped code before that date as potentially remaining valid.

Sources:
- https://www.rfc-editor.org/rfc/rfc5126.html
- https://cabforum.org/working-groups/code-signing/requirements/

These are transfer evidence, not a mandate to implement CAdES or public code-signing PKI.

Guards:
- `signature verifies now ≠ artifact existed before compromise`;
- `artifact timestamp field says T ≠ trusted existence at T`;
- `key revoked now ≠ every earlier signature automatically false`;
- `pre-compromise-looking metadata ≠ pre-compromise provenance`.

## 4. Historical-validity window model

Do not invent one precise compromise instant unless evidence supports it. Track at least:
1. **last independently trusted evidence point (LITEP)** — latest checkpoint/anchor/receipt known independently before suspected compromise;
2. **earliest plausible compromise time (EPCT)** — earliest evidence-supported point compromise may have existed;
3. **detection time** — when the organization learned/suspected it;
4. **containment/revocation effective boundary** — when current acceptance stopped in each relevant system/fleet;
5. **successor-trust activation boundary** — when new trust became independently acceptable.

Possible classification:
- **PRE-COMPROMISE-ANCHORED** — historical claim is bound to sufficiently independent evidence predating the affected window;
- **AFFECTED-WINDOW / UNCERTAIN** — old-key signature may be genuine but timing/authorship cannot be established strongly enough;
- **POST-CONTAINMENT-OLD-AUTHORITY** — old-key current authority rejected;
- **SUCCESSOR-TRUSTED** — accepted under re-established trust;
- **UNVERIFIABLE** — required historical context/evidence unavailable.

The exact product thresholds depend on consequence, retention and threat model.

Guards:
- `compromise detected at T ≠ compromise began at T`;
- `last known good at T ≠ first known bad immediately after T`;
- `cannot establish timing ≠ proven forged`;
- `historically anchored ≠ currently authorized`.

## 5. Revocation is necessary but not retroactive omniscience

Revocation/containment prevents or limits future reliance; it does not tell a verifier which already-existing old-key objects were attacker-created. RFC 5011 demonstrates a deeper trust-anchor problem: if an existing trust anchor is compromised, an attacker holding it may be able to introduce apparently valid trust data; the protocol therefore includes explicit revocation/update state and recognizes distributed-observer limitations.

Source:
- https://www.rfc-editor.org/rfc/rfc5011.html

**TRANSFER VALIDATION:** this is DNSSEC-specific. The reusable principle is that compromise of the authority used to authorize trust updates makes self-authorized recovery suspect.

Guards:
- `revocation distributed ≠ compromise history reconstructed`;
- `revocation signed by compromised key ≠ independent successor authorization`;
- `one client observed revocation ≠ offline fleet observed revocation`;
- `old key removed from server ≠ old client trust removed`.

## 6. Successor trust must not depend solely on the compromised authority

RFC 6024 requires trust-anchor management to support compromise/loss recovery and notes that initial trust-anchor-manager material may be established out-of-band. RFC 6781 advises authenticating replacement anchored keys out-of-band when trust-anchor keys are compromised. These are protocol-specific transfer patterns, not product prescriptions.

Sources:
- https://www.rfc-editor.org/rfc/rfc6024.html
- https://www.rfc-editor.org/rfc/rfc6781.html

A successor may be accepted only through a recovery authority/failure domain whose trust was not solely derived from the compromised key. Candidate architecture patterns, to be selected later by threat model, include pre-positioned independent recovery authority, independently anchored checkpoint/trust material, authenticated administrative recovery with separation of duties, or another already-trusted superior authority.

Guards:
- `compromised key signs successor ≠ successor independently trusted`;
- `same organization controls new key ≠ cryptographic continuity proven`;
- `new TLS session works ≠ provenance trust re-established`;
- `account admin can recover service ≠ admin alone may rewrite historical trust`.

## 7. Recovery authority itself is a high-value attack surface

A dormant recovery key/account/process can become the easiest route to authority. Recovery must therefore be inventoried, protected, tested and constrained. A recovery mechanism that can replace trust should not silently have broader business-data mutation powers than necessary.

**MINTTAP DIRECTION:** separate, where architecture permits, trust-rebootstrap authority from ordinary data mutation, deployment and analytics authority. Record recovery provenance and require stronger operational evidence for exceptional trust replacement.

Guards:
- `independent recovery authority exists ≠ recovery authority is secure`;
- `offline recovery material ≠ automatically trustworthy forever`;
- `two approvers ≠ two independent credentials/failure domains`;
- `recovery succeeded ≠ least privilege preserved`.

## 8. Preserve evidence before destructive normalization

SP 800-61 Rev.3 supports integrating incident response and recovery rather than treating recovery as an isolated cleanup task. Prior Web Manager studies 111–121 established evidence-preserving containment. Apply that boundary here: do not erase affected keys, verifier context, old heads, client states, logs or suspect packages before sufficient acquisition/classification when consequence warrants it.

However, evidence preservation does not mean keeping compromised private keys available to live production paths.

Guards:
- `preserve evidence ≠ preserve live authority`;
- `destroy compromised private key ≠ destroy public verification context`;
- `restore clean runtime ≠ erase incident lineage`;
- `forensic copy retained ≠ production may trust it`.

## 9. Historical evidence after compromise

Do not choose between the two false extremes: “everything old is invalid” and “everything with a valid old signature is valid.” Instead classify each claim by evidence composition. Potential supporting evidence includes independently retained checkpoints, prior receipts, trusted timestamp/validation evidence, backups proven to predate the affected window, or external witnesses where the actual architecture has them.

Each evidence source has its own failure domain and claim. A backup timestamp supplied by the same compromised system is not independent merely because it is old-looking.

Guards:
- `backup dated before compromise ≠ backup independently known to predate compromise`;
- `checkpoint verifies under old key ≠ checkpoint predates compromise`;
- `independent copy ≠ independent authenticity evidence`;
- `multiple matching copies ≠ multiple independent trust roots`.

## 10. Long-offline PWA/EFB recovery

A company iPad may be offline throughout detection, revocation and successor activation. On reconnect:
- treat locally stored old-key material as historical input, not proof of current trust;
- obtain current compromise/trust policy through a currently trusted re-entry path;
- compare local lineage against independently accepted pre-compromise/successor checkpoints where available;
- preserve local irreplaceable user data and original intent even if its remote publication authority is blocked;
- separate local read/export from remote mutation;
- do not let a stale Service Worker, cached policy, old API or imported package choose the retired trust epoch;
- quarantine ambiguous affected-window operations for explicit reconciliation rather than silently discarding or publishing them.

Guards:
- `offline client never saw revocation ≠ old key remains authorized`;
- `local data readable ≠ local provenance currently trusted`;
- `new Service Worker installed ≠ successor trust established`;
- `reconnect online ≠ compromise policy converged`;
- `user can export uncertain data ≠ uncertain data authorized for sync`.

Actual Safari/WebKit/managed-iPad storage, key, file/share and rebootstrap behavior remains OPEN.

## 11. UX boundary

Expose consequence, uncertainty and available action rather than raw cryptographic jargon. Candidate user-facing states include:
- historical data verified against evidence known before the affected window;
- historical authenticity uncertain for a named period;
- local records preserved but remote synchronization temporarily blocked;
- current trust re-established; affected records still require review;
- verification context unavailable, so authenticity cannot presently be established.

Never use a generic green “secure” state for a record whose current authorization and historical authenticity have different outcomes.

Design Studio Web is currently Stage 3 PRACTICE / NOT PASSED (W089). Persistence/offline/Sync, Safari/Firefox, screen reader, physical-device/layout/IME and human UX remain OPEN; no recovery UX PASS transfers.

## 12. Data/distributed-systems boundary

Software Engineering Data remains Stage 1 IN STUDY / NOT PASSED. D006's bounded evidence that durable replication progress must not outrun semantic effects transfers to compromise recovery: a client/server must not advance a “trust recovered” cursor/epoch before required trust-state and quarantine/reconciliation effects are durably published. D005 crash/durability evidence also reinforces that write success and durable recovery are separate.

**DEPENDENCY:** Software Engineering owns actual transactional publication, durable receipts, key storage, verifier implementation and crash behavior. Web Manager specifies web/PWA trust requirements only.

## 13. Trust re-establishment states

A useful generic operational state machine:
- `SUSPECTED` — compromise not yet confirmed; containment may still be required;
- `COMPROMISED/REVOKED-CURRENT` — old current authority rejected;
- `EVIDENCE-SCOPING` — historical claims classified against independent evidence;
- `SUCCESSOR-PREPARED` — new material exists but is not yet trusted;
- `SUCCESSOR-INDEPENDENTLY-BOUND` — recovery evidence satisfies declared trust-bootstrap policy;
- `FLEET-CONVERGING` — server/online clients updated; offline denominator incomplete;
- `NORMALIZED-WITH-RESIDUALS` — current authority restored; affected-window/historical exceptions remain explicit;
- `UNVERIFIABLE` — required evidence unavailable.

Do not make `NORMAL` the fallback state for unknown clients or histories.

## 14. Track C destructive validation campaign

1. scheduled rotation without compromise → ordinary transition path, no false incident classification;
2. suspected compromise with unknown start → uncertainty window retained;
3. detection timestamp incorrectly used as compromise start → oracle rejects exact historical claim;
4. old signature before independently anchored checkpoint → historical classification according to declared policy;
5. old signature after containment → no current authority;
6. old-key artifact claims pre-compromise timestamp but lacks independent time evidence → affected-window/uncertain;
7. compromised old key signs successor → no independent successor trust;
8. pre-positioned independent recovery authority authorizes successor → verify recovery-policy constraints;
9. recovery authority itself revoked/expired → no silent fallback;
10. two recovery approvers share one credential/failure domain → independence claim fails;
11. revocation published while iPad offline → old local authority remains blocked on reconnect;
12. stale Service Worker serves old trust policy → current server/rebootstrap policy wins;
13. cached API accepts retired epoch locally → remote current authority rejects;
14. old export imported after compromise → historical verification and current admission separated;
15. backup predates detection but provenance of backup time is same compromised system → not independent timing evidence;
16. independent checkpoint survives but full payload missing → continuity/timing claim separated from content availability;
17. full payload survives but checkpoint absent → content availability does not create authenticity;
18. forged successor uses same subject/key label → identity string does not establish lineage;
19. legitimate successor has new subject label but valid independent transition → do not reject on label mismatch alone;
20. client advances trust epoch before quarantine state commit → fail recovery atomicity oracle;
21. server commits successor trust but ACK lost → retry must be idempotent;
22. restore backup containing old active key state → current revocation floor prevents rollback;
23. device clock rollback → compromise policy does not depend solely on wall clock;
24. revocation/policy object replayed from older epoch → anti-rollback rejects current authority;
25. current trust restored while affected historical records unresolved → truthful partial-normalization state;
26. compromised private key destroyed while public historical verifier retained → historical verification may remain possible;
27. incident evidence archived but accidentally reachable by primary verifier endpoint → isolation failure;
28. analytics reports zero old clients while long-offline device reconnects → fleet completeness claim fails;
29. accessible recovery UX distinguishes local preservation, historical uncertainty and sync authority;
30. physical Safari/iPadOS offline-through-compromise→rebootstrap→reconciliation remains required before product PASS.

## 15. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-19: **W089 KEYBOARD-LAYOUT SHORTCUT SERVED-RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. Persistence/offline/Sync, cross-browser/Safari/Firefox, screen-reader, physical-device/layout/IME, field-CWV, full-WCAG and human UX remain OPEN.

Software Engineering Data `progress/DATA_STATUS.md` checked 2026-09-19: **Stage 1 IN STUDY / NOT YET PASSED**. D005/D006 provide bounded durability/sync/cursor evidence only; actual LogMate persistence/Sync and Flutter/mobile transfer remain OPEN.

## 16. MINTTAP DIRECTION

For any future consequence-bearing PWA provenance design:
- define compromise evidence and containment authority before an incident;
- maintain a current minimum accepted trust epoch that stale clients/imports cannot lower;
- distinguish detection, earliest plausible compromise, last independently trusted evidence and successor activation;
- preserve independently trustworthy pre-compromise evidence where the threat model justifies historical claims;
- do not let a compromised root be the sole authority for its successor;
- preserve irreplaceable local user data while separately blocking uncertain remote mutation;
- record trust-rebootstrap provenance and residual uncertainty;
- test long-offline client convergence and rollback resistance destructively.

Do not add timestamping, public transparency, offline roots or multi-party recovery merely because they are available patterns. Minimum sufficient design depends on actual consequence and product architecture.

## 17. OPEN / next bottleneck

Production OPEN: actual key/trust hierarchy, compromise detection source, revocation semantics, recovery authority, timestamp/checkpoint/anchor topology, trust-policy distribution, fleet denominator, browser key storage, managed-iPad behavior, legal/aviation/investment consequence, incident retention and destructive compromise drills.

Highest-value adjacent generic work: **PWA compromise-era trust-policy distribution & offline re-entry authenticity** — once successor trust exists centrally, determine how a long-offline client can authenticate the new minimum trust epoch/revocation state without accepting a replayed old policy or allowing a compromised old authority to bootstrap the client into an attacker-controlled successor. This should integrate secure-context/Service-Worker/cache behavior, monotonic trusted-state floors, recovery packages and physical-device validation boundaries.