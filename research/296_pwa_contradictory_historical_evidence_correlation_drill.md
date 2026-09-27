# 296 — PWA Contradictory Historical Evidence, Correlation & Compromise-Drill Contract

Status: **PASS (generic research gate) / PRODUCT + RUNTIME + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-28  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Validation owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: Track A browser/runtime/currentness mechanics; Track B recovery-state UX; Track D supporting diagnostics only.

## Purpose

Study 295 established that mathematical signature validity, historical validity and current authority are different questions after a key/root compromise. This study makes the next question falsifiable: when timestamp, checkpoint, audit and witness evidence conflict, when are they actually independent, when must apparently multiple sources collapse into one failure domain, and what minimum evidence can move a long-offline PWA artifact out of H2/UNKNOWN?

This is a generic evidence/adjudication contract. It does **not** assert that MintTap or LogMate currently uses signatures, RFC 3161 timestamps, Evidence Records, independent witnesses, MDM, a particular sync protocol or any described key hierarchy.

## SOURCE

### RFC 3161 — compromise changes the meaning of timestamp evidence
RFC 3161 states that if a TSA private key is compromised, the corresponding certificate is revoked and tokens signed with that key cannot simply be trusted. It identifies an audit trail and timestamps from two different TSAs as possible ways to discriminate genuine tokens from false backdated tokens.

Source: https://www.rfc-editor.org/rfc/rfc3161.html

The reusable lesson is bounded: a second timestamp can add evidence, but RFC 3161 does not establish a generic “two sources means independent” quorum rule. Independence still depends on the failure being investigated.

### RFC 4998 — long-term evidence requires timely renewal and failure diversity
RFC 4998 explains why long-term signature evidence decays: hash/signature algorithms may weaken, certificates may become invalid, and timestamp mechanisms themselves can become unsafe. Archive timestamps therefore need renewal before the relevant mechanism loses security. It also recommends redundant Evidence Records using different hash algorithms and different TSAs using different signature algorithms to reduce retrospective common-mode failure.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

This supports two distinct rules:
1. post-hoc renewal cannot manufacture proof that a disputed artifact existed before an already-passed compromise boundary;
2. redundancy quality depends on meaningful failure diversity, not copy count.

RFC 4998 currently has a reported technical erratum concerning hash-tree-renewal ordering. This study does not depend on that disputed construction detail.

### NIST SP 800-86 — preserve evidence before destructive analysis
NIST SP 800-86 recommends a clear chain of custody, logging custody/actions/times, making a copy and examining the copy, verifying integrity of original and copy, recording collection/analysis steps and tools, and generally preserving evidence by default when preservation need is unclear.

Source: https://csrc.nist.gov/pubs/sp/800/86/final

For a PWA recovery workflow this is an operational precedent, not a claim that every application incident is a legal forensic investigation.

## SYNTHESIS — evidence independence is claim-specific

Independence is not a permanent property of a source. It is evaluated for a particular:

`claim × threat × consequence`.

Two observations can be independent for availability diagnosis while correlated for historical creation-time proof. Two vendors can still share one identity provider, administrator, signing root, clock, storage plane, build pipeline or cloud control plane.

Use the following correlation dimensions when a source is material to adjudication:

| Code | Failure domain | Questions |
|---|---|---|
| K | Key/root | Same signing key, root, HSM trust domain, recovery root or verifier authority? |
| A | Administration | Same privileged operators, recovery account, admin plane or approval path? |
| S | Storage | Same mutable database, backup lineage, object store or replicated corruption domain? |
| C | Clock | Same time source, client clock, timestamp authority or derived timestamp? |
| P | Pipeline/runtime | Same parser, canonicalizer, build, deployment, runtime or defective verifier? |
| N | Network/observation | Same gateway, collector, proxy, telemetry ingest or observation point? |
| O | Organization/control plane | Same provider/account/tenant/control plane capable of affecting nominally separate services? |
| D | Derivation | Is one artifact copied, transformed, exported, summarized or replayed from another? |

A source pair may be independent on one dimension and correlated on another. The adjudicator records the dimensions that are decisive for the exact claim instead of producing a global “independent=true”.

## Evidence-role discipline

Evidence is classified by what it can actually establish:

- **R0 Object integrity/identity** — bytes/digest/object binding.
- **R1 Existence-before** — defensible evidence that an object existed no later than a bounded time.
- **R2 Receipt/existence-after** — a system observed/received an object at or after some time; this does not establish its creation time.
- **R3 Origin/authentication** — evidence binding an object/action to an authenticated signer/principal under the relevant verifier assumptions.
- **R4 Ordering/continuity** — evidence of sequence, lineage, inclusion or transition.
- **R5 Currentness/revocation** — evidence about current validity, revocation, epoch or policy state.
- **R6 Current admission/consequence** — evidence that a current trusted boundary admitted the material consequence under current semantics.
- **R7 Acknowledgement/convergence** — evidence that the relevant parties reached the required committed/converged state.

No role silently promotes into another. In particular:

`digest matches ≠ creation time proven`  
`server receipt at T ≠ client creation at T`  
`signature verifies ≠ signer uncompromised at signing time`  
`clock synchronized ≠ independent existence-before proof`  
`analytics observed ≠ current authority`  
`transport succeeded ≠ R7 convergence`.

## Contradiction classes

Use explicit contradiction classes rather than averaging evidence:

- **C0 compatible** — evidence is mutually consistent within stated uncertainty.
- **C1 clock-only** — discrepancy is bounded to clock source/uncertainty and does not change the material consequence.
- **C2 receipt-vs-creation** — receipt/observation is being compared with a claimed creation time.
- **C3 signature-vs-compromise-window** — signature verifies mathematically but temporal trust relative to compromise is unresolved.
- **C4 materially independent witness disagreement** — sources that remain independent for the claim disagree on a material fact.
- **C5 derived-copy pseudo-consensus** — multiple observations trace to one source/derivation lineage.
- **C6 historical-vs-currentness** — historical authenticity is adequate but current authority/revocation/policy disagrees.
- **C7 lineage/fork** — individually valid-looking histories cannot be composed into one justified lineage.
- **C8 irreducible** — evidence cannot defensibly resolve the material claim.

C4–C8 are not resolved by timestamp averaging, “newest wins”, source-count majority or vendor-count majority without an independently justified trust model.

## H2 promotion contract

An H2/UNKNOWN artifact may move to a bounded historical class only when all material conditions are satisfied:

1. **Stable object identity** — the bytes/digest/semantic object being adjudicated are unambiguous.
2. **Narrow claim** — the historical proposition and requested consequence are explicit.
3. **Role fit** — decisive evidence actually supplies the required R-role.
4. **Correlation analysis** — material K/A/S/C/P/N/O/D dependencies are documented.
5. **Decisive path outside the suspect domain** — the conclusion is not solely authorized by the failure domain under investigation.
6. **Contradiction disposition** — material contradictions are resolved, bounded, or explicitly retained.
7. **Provenance** — original, copied, reconstructed, migrated and re-signed material remain distinguishable.
8. **No retrospective invention** — evidence created after the critical event is not treated as if it existed before that event.

If these conditions are not met, retain H2/UNKNOWN for the disputed claim. “Cannot verify” does not mean false; “unknown” does not mean normal.

Historical H0/H1 classification does not create current authority. Any new material consequence requires current R5/R6 adjudication and, where the sync contract requires it, R7 acknowledgement/convergence.

## PWA / long-offline EFB application

For a long-offline company iPad returning after a possible trust compromise:

1. preserve unique local bytes, provenance and relevant runtime/generation evidence before reset, reinstall, cache clearing or destructive migration;
2. identify object/runtime/schema/policy/key/peer generations;
3. establish current bootstrap through a path that is not solely authorized by the suspect predecessor;
4. classify predecessor-era material using the evidence roles and correlation matrix;
5. keep H2/H3 material quarantined from unjustified current consequences while preserving it where defensible;
6. migrate runtime/verifier/schema without rewriting historical provenance;
7. re-adjudicate queued operations against current consequence semantics;
8. require successor-positive and predecessor-negative evidence;
9. establish acknowledgement/convergence according to the actual sync contract.

A later successful sync must not retroactively clear a previously unresolved historical contradiction.

## VALIDATION — deterministic compromise/correlation campaign

The following fixture families are **DEFINED / NOT EXECUTED**. Concrete implementation waits for actual product architecture.

| Case | Injection | Required oracle |
|---|---|---|
| 1149 | two logs derived from one canonical event | D correlation collapses pseudo-witness count |
| 1150 | two signatures under one decisive root/key domain | K correlation prevents false independence |
| 1151 | nominally separate services under one privileged admin path | A correlation recorded |
| 1152 | two timestamps derived from one clock/TSA path | C correlation recorded |
| 1153 | two evidence paths processed by one defective parser/runtime/deployment | P correlation recorded |
| 1154 | two observations behind one gateway/collector | N correlation recorded |
| 1155 | separate services sharing a decisive provider/control plane | O correlation recorded |
| 1156 | client claimed creation time conflicts with server receipt time | R2 is not promoted to R1 |
| 1157 | mathematically valid signature lies in unresolved compromise window | retain H2/C3 absent decisive external evidence |
| 1158 | newest timestamp conflicts with stronger bounded evidence | no newest-wins shortcut |
| 1159 | majority sources are derived from one source | no source-count majority shortcut |
| 1160 | post-compromise timestamp added to old bytes | no retroactive R1 promotion across passed critical event |
| 1161 | historically supported object is currently revoked/rejected | H0/H1 does not compose into R6 |
| 1162 | telemetry says operation succeeded but authority evidence is absent | observation does not become R6/R7 |
| 1163 | reconstruction/re-signing drops original-vs-derived distinction | FAIL provenance invariant |
| 1164 | late evidence renewal after mechanism already became unsafe | no normalization of missed renewal boundary |
| 1165 | unresolved H2 later synchronizes successfully | H2 remains unresolved unless new decisive evidence exists |
| 1166 | cache clear/reinstall/reset occurs before disputed evidence capture | FAIL evidence-preservation invariant |
| 1167 | debugger/instrumented harness passes | no promotion to ordinary physical-runtime PASS |
| 1168 | deterministic/backend fixture passes | no promotion to managed-iPad/native-peer PASS |

### Minimum reproducibility/evidence bundle
Each executed fixture should preserve:
- immutable fixture/run ID;
- canonical input bytes and digest;
- semantic object identity/generation tuple;
- evidence-role map;
- K/A/S/C/P/N/O/D correlation map;
- acquisition/source provenance;
- original-vs-analysis-copy identity and integrity check;
- injected fault and exact expected oracle;
- actual verdict and contradiction class;
- runtime/tool/version/configuration;
- cleanup/recovery actions and whether they mutate evidence;
- unresolved assumptions and escalation tier.

A PASS without enough evidence to reproduce the decisive observation is not promoted.

## Validation-tier boundary

### Deterministic/backend evidence can settle
When concrete architecture exists, deterministic fixtures can test:
- correlation collapse;
- evidence-role enforcement;
- contradiction classification;
- H2 preservation/promotion logic;
- current queue re-adjudication;
- successor-positive/predecessor-negative decision rules;
- destructive-reset guards;
- provenance preservation.

### Representative physical evidence remains required
Backend evidence cannot prove:
- iPadOS/WebKit Home Screen lifecycle behavior;
- real process termination/suspension/relaunch timing;
- actual storage persistence/eviction under device pressure;
- MDM/ADE/network/trust policy envelope;
- native-peer discovery/execution opportunity;
- unattended/background execution opportunity;
- VoiceOver/keyboard/assistive-technology recovery behavior;
- real end-to-end acknowledgement/convergence on representative devices.

These remain OPEN until representative managed-iPad/native-peer execution exists.

## TRANSFER VALIDATION / CONTRADICTION

- **Track A** supplies secure-context, Service Worker, storage, lifecycle and browser-currentness facts. Browser/runtime currentness does not create cryptographic authority.
- **Track B** consumes H-class, contradiction and consequence states to design truthful recovery UX. Visual reassurance must not normalize H2/UNKNOWN.
- **Track C** owns the destructive campaign, reproducibility discipline and tier non-transitivity.
- **Track D** may detect contradictions, lag, rejection and convergence signals. Analytics remains supporting observation unless the architecture explicitly makes a system an authoritative evidence source.
- **Software Engineering** should implement fixture generators, oracles and fault injection only after the real key/session/sync/data architecture is known.
- **Design Studio** may represent contested/recovered/rejected states but cannot change their authority semantics.

## MINTTAP DECISION / DIRECTION

For any company PWA that can hold unique offline work:
- preserve disputed local evidence before destructive recovery;
- never infer independence from source count or vendor labels;
- keep historical validity separate from current authority;
- require claim-specific failure-domain analysis for decisive evidence;
- preserve UNKNOWN rather than forcing operational convenience into NORMAL;
- treat later transport/sync success as new evidence, not retroactive proof;
- keep deterministic PASS, physical-device PASS and managed-fleet PASS non-transitive.

For the LogMate-like EFB scenario, do not promise automatic safe rejoin after trust compromise. The answer depends on actual current bootstrap, key/root/session/sync architecture, management policy and representative-device evidence.

## OPEN

Actual MintTap/LogMate production facts remain OPEN: signing/checkpoint architecture, keys/roots/HSMs, independent witnesses, audit topology, time sources, auth/session model, sync protocol, server receipt semantics, MDM/ADE policy, storage policy, runtime/schema generations, backend transaction semantics and compromise procedures.

No production PASS is claimed.

## CHANGE WATCH

Recheck current PKIX/TSP/long-term-evidence guidance and product browser/OS/security architecture before implementation. Platform capability support, managed-device policy and browser lifecycle behavior remain version-sensitive.

## Next high-value question

Convert this adjudication contract into an **executable validation handoff specification** once concrete product architecture is available: fixture schema, verdict oracle, fault-injection interface, evidence-bundle format, deterministic-vs-physical escalation rules, and explicit managed-iPad/native-peer acceptance criteria.