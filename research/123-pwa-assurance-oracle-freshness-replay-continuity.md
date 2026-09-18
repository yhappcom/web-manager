# 123 — PWA Assurance-Oracle Freshness, Replay Resistance & Continuity

Status: **PASS (generic) / PRODUCT RUNTIME + CLOCK/ORACLE + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 117–122 containment/exception/assurance chain; Track A browser/PWA lifecycle mechanics; Track C oracle/provenance validation; Track D observation-window/denominator discipline; Software Engineering for exact challenge, evidence and clock implementation.

## Purpose

122 established that a high-impact control claim may need evidence outside the failure domain of the control itself. Independence is still insufficient if the independent oracle can replay an old PASS, suppress a new FAIL, present a stale signed snapshot as current, or silently stop running.

This study separates **authenticity, integrity, freshness, liveness, coverage and continuity**. It deliberately does not assume a perfect trusted clock and does not prescribe a specific MintTap/LogMate cryptographic protocol.

## 1. Five-track balance

- **A Platform/Browser:** supplies Service Worker lifecycle, offline/reconnect and local-clock/browser-state mechanics. A client can legitimately remain offline longer than an assurance window.
- **B UX/IA/Content:** consumes stale/unknown/restricted assurance states; a user-facing “secure/current” state must not be inferred from an old successful check.
- **C Quality:** owns oracle freshness tests, replay/suppression mutants, negative challenges, evidence provenance and exact runtime/config identity.
- **D Search/Analytics:** owns observation-window and denominator discipline: a fresh result for observed clients does not cover absent clients.
- **E Architecture/Security/Operations:** highest-risk owner; defines which claims require freshness/liveness/continuity, challenge semantics, failure response and bounded evidence retention.

E remains the bottleneck; C receives strong dependency pressure. A is a prerequisite because offline PWA semantics make continuous-client liveness an invalid universal requirement.

## 2. SOURCE — authenticity does not establish freshness

RFC 9421 HTTP Message Signatures supports signed `created`, `expires` and `nonce` metadata, but its replay-security discussion explicitly requires application policy. A valid signature can be replayed; a nonce can provide a per-message unique value, and creation/expiration times can bound utility. A verifier can also issue a fresh nonce and require a new signature.

Source checked 2026-09-18:
- https://www.rfc-editor.org/rfc/rfc9421.html

**SYNTHESIS:** cryptographic authenticity answers who/what signed covered material under a key; it does not by itself answer whether the evidence was generated for the current challenge or current control state.

Guards:
- `signature valid ≠ evidence fresh`;
- `evidence authentic ≠ evidence live`;
- `created timestamp signed ≠ timestamp independently trustworthy`;
- `old PASS authentic ≠ current control PASS`.

## 3. SOURCE — replay resistance can use uniqueness/challenge as well as clocks

RFC 9449 DPoP requires a unique `jti`, checks proof creation time within an acceptable window, and supports server-provided nonce. Its security analysis notes that server nonces can bound proof lifetime despite arbitrarily large client/server clock skew and can prevent pre-generated proofs from being accepted as proof of current key possession.

Source:
- https://www.rfc-editor.org/rfc/rfc9449.html

NIST defines replay resistance as protection against capture and retransmission of authentication/access-control information to produce an unauthorized effect.

Source:
- https://csrc.nist.gov/glossary/term/replay_resistance

**TRANSFER VALIDATION:** DPoP is an OAuth proof protocol, not a generic monitoring design. The reusable principle is narrower: when the verifier needs evidence of a current interaction, a verifier-chosen unpredictable challenge can establish challenge-response freshness without trusting a client-supplied wall clock as the sole freshness oracle.

Guards:
- `clock disagreement ≠ freshness impossible`;
- `nonce unique ≠ all replay prevented unless verifier binds/checks the right context`;
- `challenge answered ≠ historical continuity proven`.

## 4. SOURCE — signed time and trusted time are different claims

RFC 6019 states that a signing-time attribute does not necessarily provide confidence in when the signature was produced and points to RFC 3161 for timestamps from a trusted entity. RFC 3161 defines a Time-Stamp Authority protocol for evidence that data existed before a particular time and includes nonce/timeliness checks.

Sources:
- https://www.rfc-editor.org/rfc/rfc6019.html
- https://www.rfc-editor.org/rfc/rfc3161.html

NIST SP 800-53 AU-8 addresses timestamps and synchronization with authoritative time sources for audit records.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**SYNTHESIS:** a timestamp is evidence only under assumptions about its producer, clock source, accuracy and binding. Not every assurance claim needs a formal TSA; monotonic sequence, server challenge, receipt ordering or bounded observation can sometimes answer the actual question more directly.

Guards:
- `timestamp present ≠ trusted chronology`;
- `trusted chronology useful ≠ external timestamp authority required for every probe`;
- `wall-clock time ≠ only usable freshness primitive`.

## 5. Six separate assurance properties

For each evidence object distinguish:

1. **authenticity** — expected producer/key generated or authenticated the evidence;
2. **integrity** — relevant evidence fields were not modified undetected;
3. **freshness** — evidence belongs to an acceptable current/recent challenge/state window;
4. **liveness** — the oracle/probe is presently capable of producing a new result when expected;
5. **coverage** — which control path, capability, population and configuration the result actually tested;
6. **continuity** — whether there is an unexplained gap, rollback, fork or suppression between prior and current evidence.

A seventh operational property, **availability**, asks whether evidence can be obtained; unavailable evidence is not automatically negative evidence about the production control.

Guards:
- `fresh ≠ comprehensive`;
- `live oracle ≠ correct oracle`;
- `continuous sequence ≠ every relevant population covered`;
- `missing evidence ≠ control failed`, but `missing expected evidence ≠ assurance PASS`.

## 6. Threat/failure model for stale assurance

An assurance system can falsely look green when:
- an old signed PASS is replayed;
- a valid health object has no bounded age;
- a failed probe is dropped while the last PASS remains displayed;
- the probe scheduler stops but dashboard state remains green;
- clock rollback makes old evidence appear younger;
- producer sequence resets after rollback/redeploy without detection;
- two replicas fork sequence/state and both issue plausible evidence;
- challenge/result is not bound to exact control/configuration/release identity;
- a fresh probe exercises a shadow/test path rather than production enforcement;
- only current admitted clients are probed while long-offline/exception populations are omitted.

**SYNTHESIS:** stale evidence is not only a timestamp problem. It is a binding, challenge, sequencing, gap-detection and coverage problem.

## 7. Evidence envelope

For a high-impact control claim, a generic evidence envelope should be able to bind, where proportionate:
- claim/control identity;
- exact enforcement endpoint/path;
- expected allow/deny input class;
- configuration/policy/trust/API generation;
- probe/oracle identity;
- verifier-issued challenge or equivalent uniqueness token;
- result and response identity;
- producer sequence/epoch where used;
- producer-observed and/or verifier-receipt time with source/uncertainty;
- evidence-sink receipt/order identity;
- coverage scope/population;
- expiration/recheck policy;
- predecessor/continuity reference where continuity matters.

This is a conceptual envelope, not a product schema decision.

## 8. Freshness patterns without a perfect clock

### A. Bounded verifier receipt age
The verifier records when it received evidence using its own trusted-enough operational clock. Useful for dashboard staleness, but does not prove when the producer actually generated the result if transport can be delayed.

### B. Verifier challenge-response
Verifier sends an unpredictable challenge and accepts only a result bound to that challenge and expected control identity. Strong for “oracle can exercise the control now.” It does not prove there were no failures between challenges.

### C. Monotonic sequence/epoch
Evidence carries a sequence within an explicitly identified epoch; the sink rejects rollback/duplicate sequence and detects gaps. This can detect replay/rollback without deriving wall-clock age, but reset/fork/epoch authority must be governed.

### D. Append/receipt ordering at an independent sink
A protected sink records receipt/order and can expose missing or reordered evidence. It cannot make a lying producer truthful; it improves continuity/provenance.

### E. Trusted timestamping
Useful when proof of existence before/at a defensible time is itself required. It adds operational/key/policy dependencies and should be proportionate.

**MINTTAP DIRECTION:** combine only the properties needed for the risk. Do not build a forensic timestamping infrastructure merely to show an ordinary low-impact monitor ran recently.

## 9. Continuity is stronger than a fresh point sample

A new challenge can prove that the oracle is responsive now. It cannot prove the control remained effective during the preceding gap.

Example:
- 09:00 PASS;
- monitoring silently stops;
- 11:00 forbidden path becomes available;
- 12:00 monitoring resumes and PASSes.

The 12:00 PASS is fresh and authentic but does not erase the two-hour assurance gap.

Therefore preserve explicit states such as:
- `CURRENT-PASS`;
- `CURRENT-FAIL`;
- `STALE`;
- `GAP/UNKNOWN`;
- `ORACLE-UNAVAILABLE`;
- `COVERAGE-INSUFFICIENT`.

Guard: `fresh PASS now ≠ continuous PASS since last observation`.

## 10. Suppression resistance and fail-safe presentation

If expected evidence is missing, the UI/automation must not indefinitely retain the last green state without age/gap semantics. A monitoring outage and a production-control failure are different diagnoses, but both prevent a current assurance claim.

Generic direction:
- last-known result retains its historical truth and timestamp/provenance;
- current assurance transitions to stale/unknown after the defined evidence window;
- alerting distinguishes oracle failure from production-control failure;
- an attacker/operator should not be able to silence only FAIL events while leaving PASS history apparently current without a detectable sequence/gap anomaly where high assurance requires it.

Guards:
- `last known good ≠ currently good`;
- `probe outage ≠ production outage`;
- `probe outage ≠ assurance remains green`;
- `failure suppressed ≠ failure did not occur`.

## 11. Binding freshness to the exact control state

A fresh result for policy generation G12 cannot automatically assure G13 after configuration, deployment, key, API or routing changes.

Evidence should identify the relevant state sufficiently to answer the claim. Where exact source→build→deployment→runtime identity is unavailable, keep the gap OPEN rather than treating “recent” as equivalent to “same system.”

Guards:
- `recent probe ≠ current configuration probed`;
- `same URL ≠ same enforcement generation`;
- `same application version ≠ same edge/provider policy`.

This transfers Software Engineering A005's repeated-change lesson: independently editable semantic copies can partially migrate. It does not import Engineering's bounded Python evidence as PWA runtime proof.

## 12. PWA / Service Worker application

Service Worker lifecycle makes freshness multidimensional. Separate at least:
- server currently serves expected worker bytes/headers;
- update check was recently performed;
- target client fetched/installed/activated expected generation;
- expected worker currently controls that client;
- local cache/schema/trust state is compatible;
- remote API authorization is current;
- fleet convergence denominator is known.

A fresh server-side check cannot establish an offline iPad's local worker generation. A fresh client self-report cannot establish current remote mutation authorization. An offline client also cannot be required to continuously answer a liveness challenge while legitimate offline use is a product requirement.

Guards:
- `fresh origin evidence ≠ fresh installed-client evidence`;
- `client offline ≠ oracle failure if continuous client observation was never required`;
- `client reconnects ≠ prior offline interval retrospectively assured`.

## 13. EFB / LogMate-like operating model

For a company iPad that may remain offline:
- local record access/recovery can remain available according to product policy without continuous server assurance;
- remote mutation authority is evaluated at re-entry using current server-side policy;
- re-entry can use a fresh server challenge/session/trust check rather than trusting old client PASS evidence;
- compromise-era outbox remains subject to provenance/reconciliation, even after fresh authentication;
- fleet dashboards distinguish `known current`, `known stale`, `known offline`, `retired`, and `unknown` rather than converting absence into PASS;
- managed-iPad/WebKit/MDM behavior remains exact-runtime OPEN.

This preserves the prior invariant: `offline usefulness ≠ indefinite remote authority`.

## 14. Track C adversarial validation campaign

Future product evidence should include at least:
1. replay previous authentic PASS;
2. replay previous signed FAIL as current;
3. omit timestamp but replay challenge response;
4. reuse old challenge/nonce;
5. duplicate sequence number;
6. sequence rollback;
7. sequence gap;
8. epoch reset with authorized reset record;
9. unauthorized epoch reset;
10. two producer replicas fork sequence;
11. client clock far ahead;
12. client clock far behind;
13. server clock step/rollback simulation;
14. delayed network delivery;
15. dropped FAIL event;
16. stopped scheduler with stale green dashboard;
17. evidence sink unavailable;
18. oracle unavailable while control remains healthy;
19. control fails while oracle remains live;
20. fresh probe against obsolete configuration generation;
21. fresh probe against shadow path instead of production enforcement;
22. valid signature with insufficient covered context;
23. expired evidence accepted incorrectly;
24. new challenge answered with stale cached result;
25. Service Worker server generation current/client generation stale;
26. client current/remote API trust stale;
27. long-offline client absent from denominator;
28. reconnect after assurance window;
29. outbox replay after fresh login but before reconciliation;
30. exception expiry plus stale PASS replay;
31. rollback revives old oracle epoch;
32. privacy minimization prevents user-record duplication;
33. probe side effects remain isolated;
34. stale/unknown user-facing state remains accessible at zoom/reflow/AT;
35. independent reviewer can reconstruct freshness/coverage claim from preserved evidence.

## 15. Cross-repository transfer

### Design Studio
Latest canonical Web status is W075, Stage 3 PRACTICE / NOT PASSED. It preserves per-scenario EXECUTED-PASS/FAIL/NOT-EXECUTED/BLOCKED provenance and now targets Customize browser closure, non-drag reorder equivalence, reflow/forced-colors and independent engine. Persistence, Sync and FlightRecord projection remain not implemented. This supports the provenance principle but is not security-oracle evidence.

### Software Engineering
Latest global status remains Foundation IN STUDY across all specialists. A005 now has bounded executable evidence showing a partial repeated-change migration can leave observers with inconsistent semantics. Transfer: freshness evidence must bind to relevant policy/configuration generation rather than merely recent time. No Dart/Flutter/PWA runtime proof follows from that Python model.

### Marketing
Latest canonical activity concerns semantic localization governance; no material evidence changes this security/assurance boundary, so no discipline duplication is warranted.

## 16. Operational judgment — freshness/continuity matrix

For each high-value assurance claim record:
- claim and consequence;
- expected evidence cadence/event trigger;
- authenticity/integrity mechanism;
- freshness mechanism (age/challenge/sequence/receipt/etc.);
- clock/time assumptions and uncertainty;
- liveness expectation;
- continuity/gap rule;
- exact control/configuration binding;
- coverage/population denominator;
- stale/unknown transition;
- suppression/replay tests;
- independent sink/failure-domain rationale;
- privacy/availability cost;
- OPEN exact product facts.

This avoids two extremes: trusting any signed green blob forever, and demanding perfect global time/continuous connectivity from an offline-first PWA.

## 17. PASS gate

Generic PASS requires ability to:
- distinguish authenticity, integrity, freshness, liveness, coverage and continuity;
- explain why signed/timestamped evidence can still be stale or replayable;
- use verifier challenge/nonce and sequence/receipt patterns without assuming a perfect client clock;
- distinguish current point evidence from continuous historical assurance;
- fail current assurance to stale/unknown when expected evidence disappears without falsely diagnosing the production control;
- bind assurance to relevant control/configuration generation;
- apply the model to Service Worker/origin/client/remote-authority/fleet claims;
- preserve legitimate long-offline EFB use without granting stale remote authority;
- keep exact product/runtime/clock/oracle architecture OPEN.

**Assessment: PASS (generic).**

## Persistent guards added by 123

- `signature valid ≠ evidence fresh`;
- `evidence authentic ≠ evidence live`;
- `old PASS authentic ≠ current control PASS`;
- `created timestamp signed ≠ timestamp independently trustworthy`;
- `clock disagreement ≠ freshness impossible`;
- `timestamp present ≠ trusted chronology`;
- `fresh ≠ comprehensive`;
- `live oracle ≠ correct oracle`;
- `missing evidence ≠ control failed`, but `missing expected evidence ≠ assurance PASS`;
- `fresh PASS now ≠ continuous PASS since last observation`;
- `last known good ≠ currently good`;
- `probe outage ≠ production outage`;
- `probe outage ≠ assurance remains green`;
- `recent probe ≠ current configuration probed`;
- `fresh origin evidence ≠ fresh installed-client evidence`;
- `client reconnects ≠ prior offline interval retrospectively assured`.

## OPEN / next boundary

Actual MintTap/LogMate oracle, monitoring, challenge, sequence, evidence-sink, trusted-time, session, API/trust generation, Service Worker, fleet inventory and managed-iPad implementation remain OPEN.

The highest-value adjacent generic boundary is **assurance evidence retention, key/epoch rotation and long-term verifiability**: a result may have been authentic and fresh when produced yet become unverifiable or misleading after signing-key rotation, certificate expiry/revocation, evidence-format migration, retention pruning or oracle-epoch reset. Study how to preserve enough provenance for incident/postmortem decisions without treating historical authorization as current authorization or building unnecessary non-repudiation infrastructure.