# 259 — PWA Acknowledgement Credential Rotation, Recipient Compromise & Ledger-Correction Governance

Status: **PASS (generic) / PRODUCT + DOMAIN-AUTHORITY + DATA-MODEL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**
Date: 2026-09-24
Primary owner: **Track E — Web Architecture, Security & Operations**
Consumers: Track A credential/session mechanics; Track B compromise/recovery UX; Track C destructive validation; Track D bounded assurance measurement.
Dependencies: 094, 122–125, 138–141, 161, 198–200, 241–258, especially authority succession, compromise-era evidence, incarnation identity and acknowledgement applicability.

## Problem
258 established that acknowledgement is scoped evidence, not a boolean. The adjacent failure boundary is what happens when the credential, device, recipient, verifier, or remediation operator that produced acknowledgement evidence is later suspected or proven compromised. Two opposite errors are dangerous: trusting all old ACKs forever because their bytes still verify, or deleting/blanket-invalidating all historical ACKs and losing evidence that may predate compromise.

Central rule: **credential validity, ACK authenticity, ACK applicability, historical evidentiary value and current recipient authority are distinct questions. Rotation creates a successor authority epoch; compromise scopes uncertainty according to evidence and time/lineage rather than granting the compromised actor power to self-clear. Ledger mistakes are corrected by supersession/correction provenance, not destructive history rewrite.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns session/token/credential lifecycle and browser/PWA storage mechanics. Credential rotation does not itself determine domain ACK semantics.
- **B UX/IA/Content:** high dependency pressure. Owns truthful states such as `credential compromised`, `historical ACK under review`, `current state re-verification required`, and `ledger corrected` without false finality or destructive reset. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **824 → 832 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. May measure compromise-to-reverification latency, affected ACK classes and correction debt; telemetry cannot clear compromise or rewrite ledger truth.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns compromise scoping, rotation/succession, independent re-verification, ledger correction provenance and self-clear resistance.

## SOURCE

### NIST SP 800-63B — authenticator lifecycle separates binding, compromise, renewal and revocation
NIST SP 800-63B treats authenticator binding as an explicit association, recommends retaining records of authenticators associated with an identity, requires stronger controls for binding replacement/additional authenticators, and treats loss/theft/unauthorized duplication as compromise conditions requiring prompt suspension/revocation/destruction as practical. Renewal binds a successor authenticator before the replaced authenticator may be revoked.

Source: https://pages.nist.gov/800-63-3/sp800-63b.html#sec6

**TRANSFER VALIDATION:** bounded identity precedent for explicit credential epochs and successor binding. It does not define LogMate acknowledgement authority.

### RFC 7009 — credential revocation has scope and propagation behavior
OAuth token revocation invalidates the presented token and can, according to policy, invalidate related tokens/grants. The RFC notes that propagation delay can exist and that clients must be prepared for unexpected invalidation.

Source: https://www.rfc-editor.org/rfc/rfc7009

**TRANSFER VALIDATION:** bounded precedent that revocation is a state transition with possible related scope and propagation lag, not proof that all dependent application evidence is instantly reconciled.

### NIST SP 800-53 AU-9 — audit/remediation evidence requires protection
AU-9 requires protecting audit information and audit tooling from unauthorized access, modification and deletion. Prior study 258 already uses this as bounded precedent for consequence-bearing remediation evidence.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** supports correction-by-provenance rather than silent destructive editing. It does not prescribe a specific append-only database.

## SYNTHESIS 1 — split five questions after compromise
For an ACK produced under credential K4, ask separately:
1. do the ACK bytes/proof still verify under historical verifier context?
2. was K4 authorized for this recipient/consequence when the ACK was created?
3. what is the known/suspected compromise interval?
4. is this ACK within or outside that uncertainty interval?
5. is the recipient currently authorized/current under successor policy?

A yes to (1) does not imply yes to (2)–(5).

Guards: `signature/proof verifies ≠ credential uncompromised`; `historically authentic ACK ≠ currently applicable ACK`; `current credential revoked ≠ every historical statement false`.

## SYNTHESIS 2 — compromise creates an evidence interval, not automatic history deletion
If compromise time is bounded, evidence clearly before that boundary may retain historical value under the applicable policy; evidence in the uncertain interval requires review/quarantine; post-revocation evidence must not regain current authority merely because old cryptographic material still verifies.

If compromise time is unknown, widen uncertainty rather than inventing a precise cutoff. Preserve original ACK, compromise report, affected credential epoch and later disposition.

Guard: `compromise discovered at t ≠ compromise began at t`; `cannot prove pre-compromise ≠ proven forged`.

## SYNTHESIS 3 — rotation is successor binding, not historical rewrite
Credential K5 replacing K4 should have an explicit succession relation and current authorization basis. Do not re-sign old ACKs under K5 and claim they were originally produced by K5. Historical K4 ACKs remain attributed to K4/its recipient incarnation; K5 is used for new current-state evidence after re-verification.

Guard: `successor credential current ≠ predecessor evidence re-authored`; `re-signing old ACK ≠ original trust restored`.

## SYNTHESIS 4 — current state needs independent re-verification after recipient compromise
A compromised client or credential must not clear its own compromise state by sending `ACK CURRENT` using the same suspect authority. Re-entry needs a current bootstrap/authority path independent enough for the consequence: successor credential binding, current policy/floor, server-side or organizational evidence, and negative rejection of predecessor authority where controlled.

No universal requirement for a particular cryptographic ceremony is asserted; strength follows consequence and actual architecture.

Guard: `compromised recipient says recovered ≠ recovery proven`; `same compromised credential approves successor ≠ independent succession`.

## SYNTHESIS 5 — operator compromise is distinct from recipient compromise
A remediation operator may have authority to dispatch, inspect or reconcile ACKs without authority to fabricate recipient application. If an operator credential is compromised, scope affected ledger mutations and approvals separately from recipient-generated evidence. Do not infer every recipient state false, and do not allow the operator to erase its own suspicious mutations.

Guard: `operator can administer ledger ≠ operator can attest recipient state`; `operator compromise ≠ recipient compromise`.

## SYNTHESIS 6 — ledger correction is a new provenance event
A false ledger row should not be silently edited from `ACKNOWLEDGED` to `NOT_ACKNOWLEDGED`. Preserve:
- original ledger event identity/content;
- discovery/contradiction evidence;
- correction event identity;
- correcting authority and policy generation;
- reason/evidence reference;
- superseded/invalidated scope;
- resulting current projection/state;
- unresolved uncertainty if applicable.

This permits reconstruction of what the system believed and why that belief changed.

Guard: `ledger corrected ≠ old event never existed`; `current projection ≠ rewritten history`.

## SYNTHESIS 7 — correction authority must not be the sole subject of its own correction
Where consequence is material, a credential/operator accused of producing false ACK state cannot be the sole authority that marks those entries valid again or deletes the contradiction. Separation can be organizational, cryptographic, workflow-based or verifier-based depending on architecture.

Guard: `can write ledger ≠ can self-exonerate`; `admin privilege ≠ independent correction authority`.

## SYNTHESIS 8 — revocation propagation does not instantly settle dependent ACK state
RFC 7009 explicitly allows propagation delay in token revocation. Analogously, credential revocation should trigger dependency analysis: which ACKs, recipient sessions, queued operations, exports or closure claims depended on that credential? Mark affected states for review/reverification rather than assuming instantaneous global convergence.

Guard: `credential revoked centrally ≠ dependent closure reconciled everywhere`.

## SYNTHESIS 9 — backup/restore and reincarnation must not resurrect revoked ACK authority
If a PWA restore contains K4-era local state after K4 compromise/revocation, preserve unique data but do not restore K4's acknowledgement authority. Current bootstrap establishes the current incarnation and successor credential/floor before new ACK generation.

Guard: `credential bytes restored ≠ credential authority restored`; `old local ACK cache restored ≠ server remediation reopened as current`.

## SYNTHESIS 10 — compromise-aware ACK states need more than valid/invalid
Useful generic states include:
- `HISTORICAL-VALID-BOUNDED`;
- `UNDER-COMPROMISE-REVIEW`;
- `SUPERSEDED-BY-CORRECTION`;
- `REVERIFICATION-REQUIRED`;
- `CURRENT-REVERIFIED`;
- `REJECTED-AS-POST-REVOCATION`;
- `UNKNOWN`.

Exact names are implementation-specific. The principle is to preserve uncertainty instead of forcing every historical ACK into true/false.

## SYNTHESIS 11 — closure claims inherit credential-compromise dependencies
If closure C12 relied on ACK A12 from K4 and K4 later enters a material compromise interval, C12 may require reopening or scoped revalidation. This does not mean every closed workflow globally reopens. Dependency edges and consequence scope determine blast radius.

Guard: `ACK questioned ≠ all closures invalid`; `closure once valid ≠ immune to later contradiction`.

## SYNTHESIS 12 — analytics observes compromise debt, never resolves it
Track D may measure counts/age of ACKs under review, time to successor re-verification and affected recipient classes. Analytics loss or event arrival order cannot establish compromise start, credential succession or correction authority.

Guard: `telemetry says rotated ≠ rotation authority proven`.

## SYNTHESIS 13 — Service Worker/session freshness is not credential assurance
A new Service Worker, fresh page load or successful session refresh may coexist with compromised recipient credentials or stale acknowledgement state. PWA update mechanics remain orthogonal to acknowledgement-authority recovery.

Guard: `Service Worker current ≠ ACK credential current`; `session refreshed ≠ compromise cleared`.

## SYNTHESIS 14 — long-offline clients need data-preserving quarantine
A company iPad returning after K4 revocation may contain unique unsynced flight/logbook data. Preserve those records and provenance, fence consequence-bearing outbound mutation, establish current authority/K5, then revalidate queued operations and generate current ACKs. Do not erase unique records merely to eliminate old credentials.

Guard: `credential compromised ≠ unique local data disposable`.

## SYNTHESIS 15 — negative evidence is required where predecessor rejection is controllable
After K5 succession, test not only that K5 can produce an accepted current ACK, but that K4 cannot close a current consequence, replay an old ACK into a new projection/incarnation, or self-approve its own recovery.

Guard: `successor works ≠ predecessor extinct`.

## SYNTHESIS 16 — product facts remain OPEN
This study does not assert that MintTap/LogMate uses signed ACKs, OAuth tokens, device keys, a particular MDM, append-only storage, or a specific compromise-response process. Those are product/runtime questions for canonical project evidence and Software Engineering implementation validation.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. model ACK credential/verifier/recipient authority as versioned epochs with explicit succession/revocation;
2. after compromise, separate historical cryptographic validity from current applicability;
3. retain an uncertainty interval when compromise timing is not proven;
4. require independent-enough successor binding/re-verification for material consequences;
5. prohibit compromised recipients/operators from sole self-clear authority;
6. correct ledger mistakes through provenance-bearing supersession rather than destructive edit;
7. propagate credential compromise through dependent ACK/closure claims by explicit dependency scope;
8. preserve unique offline data while quarantining obsolete authority;
9. test predecessor rejection as well as successor acceptance;
10. keep telemetry, Service Worker and session freshness outside semantic acknowledgement authority.

## EFB / LogMate-like application case
Assume iPad incarnation I4 used credential K4 and ACKed projection P12. Later K4 is suspected compromised, with compromise start unknown. I4 then returns after a long offline period containing unique unsynced flight records and a cached `ACK P12`. A remediation operator account O7 also edited the ledger during the incident and is later suspected compromised.

Safe generic sequence:
1. preserve I4 unique records, cached ACK and original ledger events as evidence;
2. fence K4/O7 from current consequence-bearing mutation;
3. record compromise intervals as unknown/bounded rather than inventing exact start times;
4. classify K4-era ACKs by scope/time/evidence and mark uncertain ones `REVERIFICATION-REQUIRED` rather than deleting them;
5. establish current organizational bootstrap and successor recipient/incarnation credential K5 through an independent-enough path;
6. reconcile P12/current projection and queued records under current schema/policy without re-authoring historical data;
7. produce new K5-bound current acknowledgement where required;
8. prove K4 cannot close current acknowledgement/remediation consequences;
9. review O7 ledger mutations separately; preserve original rows and append correction/supersession events where evidence warrants;
10. reopen only dependent closure claims whose evidence materially relied on affected ACKs;
11. retain unresolved uncertainty where evidence cannot distinguish legitimate from compromise-era actions.

This is architecture guidance, not a claim about current LogMate implementation.

## Track C destructive campaign — +8 defined cases
825. **Historical-validity blanket deletion** — K4 compromise causes every old ACK and its provenance to be deleted. Expected: fail.
826. **Cryptographic-validity laundering** — K4 ACK still verifies, therefore it is accepted as current after K4 revocation. Expected: fail.
827. **Compromise-discovery timestamp laundering** — discovery time is asserted as exact compromise start without evidence. Expected: fail.
828. **Compromised self-clear** — K4/compromised client alone authorizes K5 and marks itself current. Expected: fail.
829. **Operator self-exoneration** — suspected O7 silently edits/removes its own disputed ledger mutations. Expected: fail.
830. **Restore authority resurrection** — backup restores K4 credential/ACK cache and current authority is inferred. Expected: fail.
831. **Successor-only positive test** — K5 ACK succeeds but K4 predecessor acceptance/replay is never tested. Expected: fail.
832. **Compromise-as-data-destruction** — old credential presence causes unique offline records to be wiped before recovery/provenance preservation. Expected: fail.

**VALIDATION:** these are defined destructive cases, not executed PASS.

## Cross-track transfer
- **A → E:** authenticator/token/session lifecycle supplies mechanics; E owns consequence-bearing ACK authority and compromise dependency.
- **E → B:** UX must distinguish historical evidence, under-review state and current re-verification without implying forgery or finality before evidence supports it.
- **E → C:** destructive validation must exercise compromise interval, rotation, restore/reincarnation and self-clear failure paths.
- **E → D:** analytics can quantify compromise/reverification debt but cannot create or correct authority state.

## External specialist boundary
Design Studio Web remains Stage 3 PRACTICE / NOT PASSED with physical-device/PWA, screen-reader and representative-human evidence OPEN. Software Engineering Studio remains Foundation IN STUDY; current Safari/PWA evidence is bounded transfer evidence and installed/physical iOS/iPadOS product runtime remains OPEN. This generic study promotes neither external gate.

## OPEN / VALIDATION
- actual acknowledgement credential/key/token architecture;
- exact compromise detection and trusted-time evidence;
- recipient/operator authority model;
- ledger storage, transaction and correction implementation;
- key/credential rotation and revocation propagation behavior;
- restore/reinstall/re-enrollment behavior on managed physical iPad;
- current LogMate auth/session/onboarding implementation;
- aviation/legal retention and dispute requirements;
- physical-device, AT, human and security validation.

## Gate result
**PASS (generic).** The Web Manager can now distinguish ACK proof validity from credential authority/current applicability, scope compromise uncertainty without blanket historical erasure, rotate acknowledgement authority through explicit successor binding, correct ledger errors without rewriting history, and prevent compromised actors from self-clearing. Production certification remains OPEN.

## Next high-value target
**260 — compromise dependency-graph reconstruction, closure-claim transitive invalidation & bounded reauthorization.** Determine how to reconstruct which ACKs/closures/exports actually depended on a compromised credential/operator, avoid both global panic reopening and missed transitive impact, preserve unaffected evidence, and safely reauthorize only the minimal consequence subgraph after independent re-verification.