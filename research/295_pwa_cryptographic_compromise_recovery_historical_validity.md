# 295 — PWA Cryptographic Compromise Recovery, Historical-Validity Windows & Trust Re-establishment

Status: **PASS (generic evidence/contract) / PRODUCT CRYPTOGRAPHIC ARCHITECTURE + RUNTIME VALIDATION OPEN**  
Date: 2026-09-27  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A runtime/currentness mechanics; Track C falsifiable evidence and destructive validation; 290–294 PWA lifecycle, managed-device, authority, sync and recovery-state contracts. Track B consumes consequence states; Track D consumes privacy-minimized diagnostics only.

## Scope
This study addresses the Stage 8 question that remains after 294: how to preserve and classify historical PWA/offline artifacts when a signing/verifier key or trust root is suspected compromised, and how to establish successor trust without allowing a compromised predecessor to authorize its own replacement. It does not assert that MintTap or LogMate currently uses PKI, TSA, signed queues, signed checkpoints, a particular key hierarchy, or any production cryptographic design.

## SOURCE
- NIST SP 800-57 Part 1 Rev. 5 distinguishes an originator-usage period, during which a key may apply cryptographic protection, from a recipient-usage period, during which protected information may be processed. Public verification material can therefore remain useful after private signing use ends.
- RFC 5280 distinguishes revocation reasons including keyCompromise and cACompromise. Its invalidityDate can represent when a private key was known or suspected to have been compromised and can precede the CRL revocation-processing date.
- RFC 3161 states that if a TSA private key is compromised, tokens signed with that key cannot simply be trusted; an audit trail or independent timestamp evidence may help discriminate genuine tokens from false backdated tokens.
- RFC 3628 similarly requires a TSA/TSU to stop issuing on actual or suspected compromise and, where possible, provide information that identifies affected tokens.

Primary references:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/info/rfc5280/
- https://www.rfc-editor.org/info/rfc3161/
- https://www.rfc-editor.org/info/rfc3628/

## SYNTHESIS — three capabilities must not collapse
Keep separate:
1. **Data preservation** — bytes/semantic records and provenance remain available for recovery or adjudication.
2. **Historical verification** — evidence supports a bounded claim about a historical artifact.
3. **Current authority** — an actor/key/root may create a new current consequence.

`data preserved ≠ historically trusted ≠ currently authorized`.

Retaining an old public verifier for historical processing does not authorize new signatures. Retaining historical evidence does not require retaining a historical private signing key.

## Compromise chronology t0–t5
- **t0 — last independently supported good evidence**: latest point supported outside the suspect authority/failure domain.
- **t1 — earliest plausible compromise/invalidity**: may be uncertain or bounded rather than a single timestamp.
- **t2 — detection/suspicion**: compromise becomes known or suspected.
- **t3 — containment/revocation publication**: affected authority is disabled/revoked/quarantined.
- **t4 — independently established successor trust**: successor authority is established through evidence not solely controlled by the compromised predecessor.
- **t5 — predecessor consequence closure**: old authority can no longer create current product consequences.

Do not collapse t1 into t2 or t3. RFC 5280 invalidityDate exists precisely because invalidity/compromise can precede revocation processing.

## Historical classification H0–H5
Classification is object- and consequence-specific.

- **H0 independently supported historical** — artifact has adequate evidence outside the suspect failure domain for the historical claim being made.
- **H1 historical-only / no current authority** — may be retained/verified for bounded historical use but cannot create a new current consequence.
- **H2 contested window / UNKNOWN** — evidence cannot defensibly place the artifact on one side of the compromise boundary.
- **H3 post-compromise or untrusted-originator evidence** — artifact cannot receive the claimed authority from the compromised signer/root.
- **H4 recovered/derived evidence** — reconstruction, migration, re-signing or repair exists, but provenance must state that it is derived and must not masquerade as original evidence.
- **H5 rejected/quarantined** — current policy rejects the requested consequence while preserving defensible evidence where required.

`signature mathematically verifies ≠ artifact predates compromise`.
`cannot verify ≠ proven false`.
`UNKNOWN ≠ NORMAL`.

## Successor-trust invariant
A compromised predecessor must not be the sole decisive authority for its successor.

The eventual product architecture may use a separately governed recovery root, independently authenticated operator action, quorum/witness evidence, or another mechanism. This study does not select one. The validation invariant is:

**successor-positive + predecessor-negative**

- successor-positive: evidence establishes the successor under a current trusted recovery path;
- predecessor-negative: evidence establishes that the predecessor cannot continue producing accepted current consequences.

A valid-looking certificate/statement from the old root alone is insufficient when that root is the compromised domain under investigation.

## Evidence reconstruction contract
For each material historical object preserve, where available:
- immutable object/digest or canonical committed bytes;
- semantic object identity and generation;
- claimed creation/signing time and the source of that time;
- key/certificate/root/verifier generation;
- independent timestamp/checkpoint/witness/audit evidence and its failure domain;
- revocation reason, revocation-processing time and invalidity/compromise evidence;
- device-clock source and uncertainty where relevant;
- contradictions and missing evidence;
- reconstruction/migration actions with original-vs-derived provenance;
- final H-class plus the exact consequence decision.

A device wall clock, server receipt time, CRL publication time, analytics event or one mutable audit store is not automatically an independent proof of creation time.

## Contradiction handling
1. Preserve original evidence before repair.
2. Identify whether apparently independent witnesses share keys, administrators, storage, clock, deployment pipeline or other failure domains.
3. Separate cryptographic validity from temporal and policy validity.
4. Prefer bounded intervals to invented exact compromise times.
5. Keep contradictory material explicit; do not average or majority-vote evidence without a justified trust model.
6. If evidence cannot resolve ordering or authenticity for the requested consequence, retain H2/UNKNOWN.
7. Re-adjudicate current consequences under current policy even when historical authenticity is adequate.
8. Record any manual/operator decision as a new provenance event rather than rewriting historical provenance.

## PWA / LogMate-like application
For a long-offline company iPad returning with unique local work and predecessor-era runtime/verifiers:
1. preserve unique local data and provenance before destructive repair;
2. identify runtime/schema/policy/key/peer generations;
3. obtain current bootstrap through an independently trusted current path;
4. classify historical artifacts against the compromise window;
5. migrate verifier/runtime/schema without granting historical material new authority;
6. re-adjudicate queued material operations under current consequence semantics;
7. quarantine H2/H3 material where current consequences cannot be justified;
8. prove successor-positive and predecessor-negative conditions;
9. then establish acknowledgement/convergence according to the actual sync contract.

Service Worker update, reinstall, cache clear, reconnect, reauthentication or successful transport does not by itself re-establish cryptographic trust.

## Track C destructive additions — DEFINED / NOT EXECUTED
1135. Revocation-processing time is treated as compromise start.  
1136. Mathematical signature validity is promoted to historical trust.  
1137. All predecessor-era artifacts are blanket-invalidated despite independent historical evidence.  
1138. All pre-detection artifacts are grandfathered despite an unresolved compromise window.  
1139. Compromised predecessor solely authorizes its successor.  
1140. Successor-positive evidence is accepted without predecessor-negative validation.  
1141. Historical verifier accidentally remains enabled for new/current authority.  
1142. H2/UNKNOWN is coerced into normal/current state.  
1143. Reconstructed or re-signed evidence masquerades as original provenance.  
1144. Two witnesses are treated as independent despite a shared material failure domain.  
1145. Historically signed offline queue bypasses current re-adjudication.  
1146. Service Worker/runtime update is treated as cryptographic trust recovery.  
1147. Emergency recovery bridge remains a permanent authority path.  
1148. Cleanup/reset destroys evidence needed to classify the compromise window.

All remain **DEFINED / NOT EXECUTED** until concrete product architecture and representative fixtures exist.

## TRANSFER VALIDATION / CONTRADICTION
- Track A supplies browser/runtime/currentness facts but does not create cryptographic authority.
- Track B consumes H-class/consequence distinctions for truthful recovery UX without inventing trust.
- Track C owns destructive tests, predecessor-negative checks and evidence-promotion discipline.
- Track D diagnostics/analytics are supporting observations only; they are not timestamp, authority or convergence oracles.
- Software Engineering should implement concrete key-generation, fixture and fault-injection harnesses only after actual product cryptographic architecture is known.
- Design Studio may later represent contested/recovered/rejected states but visual treatment cannot normalize UNKNOWN.

## MINTTAP DECISION / DIRECTION
For any company PWA that can retain unique offline work, preserve evidence before destructive recovery and separate historical readability from current authority. If cryptographic signing/checkpointing is later adopted, design explicit compromise-window and successor-trust procedures before relying on the mechanism for durable offline authority.

For the LogMate-like EFB scenario, do not promise that an old offline iPad can automatically rejoin after a trust compromise. Rejoin safety depends on the actual key/root/session/sync architecture and representative-device evidence.

## OPEN / VALIDATION
MintTap/LogMate cryptographic architecture, keys, roots, signing/checkpoint use, independent witnesses, audit topology, MDM policy, runtime/schema generations and production compromise procedures remain **OPEN**. No production PASS is claimed.

## CHANGE WATCH
Recheck current NIST key-management guidance, PKIX/TSP standards and the product's actual browser/OS/runtime architecture before implementation or after material cryptographic-policy/platform changes.

## Next high-value question
Build a falsifiable **contradictory historical-evidence adjudication matrix**: determine independence when timestamp/checkpoint/audit/witness evidence conflicts or shares failure domains, preserve UNKNOWN without false normalization, and define the minimum evidence required to move a long-offline PWA artifact from H2 into a bounded historical or current consequence class.
