# 160 — PWA Recovery-Closure Evidence Retention, Verifier Independence & Closure-Claim Anti-Forgery

Status: **PASS (generic) / PRODUCT + EVIDENCE-STORE + PROVIDER + VERIFIER + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 159 closure proof/downstream reconciliation; 136–137 checkpoint/verifier lifecycle; Track A SW/cache/offline-client mechanics; Track B truthful evidence-confidence UX; Track C destructive anti-forgery/restore validation; Track D diagnostic signals only.

## Why this study exists

159 made `CLOSED` a bounded evidence claim. The next failure is self-attestation: if the same mutable incident database stores the effect, decides closure, stores the evidence, and later verifies that closure, compromise or point-in-time restore can rewrite the entire story consistently. A second failure is privacy over-retention: retaining every provider payload forever may improve apparent auditability while creating a larger sensitive-data target. A third is stale-client forgery: an old Service Worker, replica, backup, export, or offline device may surface a historically authentic `CLOSED` claim after the authoritative closure generation has been reopened or superseded.

The problem is therefore not “make logs immutable.” It is to preserve enough independently verifiable, privacy-bounded evidence to distinguish a current closure claim from stale, forged, replayed, truncated, or self-certified claims.

## SOURCE

### NIST SP 800-53 Rev. 5.1 — audit information needs protection and separation
NIST SP 800-53 Rev. 5.1 includes AU-9 Protection of Audit Information with enhancements for separate systems/components, cryptographic protection, restricted privileged access, dual authorization and read-only access; AU-10 covers non-repudiation/identity binding/chain of custody/digital signatures; AU-11 covers retention and long-term retrieval.

Source: https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

**TRANSFER VALIDATION:** closure evidence should not depend solely on the same privilege/failure domain whose actions it is meant to substantiate. This does not prescribe a particular storage product or mandate every enhancement for MintTap.

### NIST log-management status — final baseline plus revision change watch
NIST's Log Management project states that SP 800-92 Rev.1 remains a draft while the original SP 800-92 remains final; the revision focuses on organization-wide log-management planning, including generation, transmission, storage, access and disposal.

Sources:
- https://csrc.nist.gov/projects/log-management
- https://csrc.nist.gov/pubs/sp/800/92/final
- https://csrc.nist.gov/pubs/sp/800/92/r1/ipd

**CHANGE WATCH:** do not silently treat Rev.1 draft text as final requirements. Its status must be rechecked before policy-sensitive use.

### OWASP Logging Cheat Sheet — integrity, trust zones and minimization
OWASP states that event data arriving from another trust zone may be missing, modified, forged or replayed; source verification and integrity/non-repudiation may therefore matter. It recommends tamper detection, restricted/monitored log access, secure transmission and careful exclusion/masking/hashing/encryption of sensitive values such as access tokens, passwords, keys and sensitive personal data. Retention should satisfy required periods without indefinite over-retention.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

**TRANSFER VALIDATION:** “retain evidence” does not mean “retain every raw secret/provider payload.” Verification evidence and recoverable sensitive content are different assets.

### RFC 9162 — append-only/inclusion/consistency proofs as a transferable pattern
Certificate Transparency v2 defines Merkle inclusion proofs and consistency proofs. Consistency proofs establish that a later tree extends an earlier tree without changing its earlier prefix; the RFC also distinguishes auditing one log view from detecting inconsistent views presented to different observers.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION, NOT IMPLEMENTATION PRESCRIPTION:** append-only commitments and independently compared checkpoints are useful mental models for closure-claim lineage. MintTap does not thereby need Certificate Transparency, a public transparency log, Merkle trees, or blockchain.

## SYNTHESIS — closure evidence is not the closure authority

Separate at least four conceptual roles:
1. **effect/incident authority** — current operational state and consequence;
2. **closure decision authority** — decides whether the declared invariant is satisfied or residual risk accepted;
3. **evidence store/anchor** — retains evidence sufficient to substantiate what was decided and on what basis;
4. **verifier** — checks evidence/lineage/currentness without gaining power to create a new closure decision.

These roles may share infrastructure in a small system, but their trust semantics must remain distinguishable. A verifier that can silently rewrite the evidence it verifies is not independent for that failure mode.

Persistent guards:
- `closure row exists ≠ closure claim trustworthy`;
- `closure claim authentic ≠ closure claim current`;
- `evidence retained ≠ evidence independently verifiable`;
- `hash matches ≠ source statement true`;
- `signature valid ≠ signer authorized for this closure generation`;
- `append-only history ≠ semantic legitimacy`;
- `independent storage ≠ independent administration`;
- `replica count > 1 ≠ failure-domain independence`;
- `provider receipt retained ≠ provider state still current`;
- `audit evidence sufficient ≠ raw sensitive payload retained`;
- `offline client remembers CLOSED ≠ server closure remains current`;
- `backup restored successfully ≠ restored closure generation accepted`.

## Closure-claim envelope

A generic closure claim should be bound to enough context to make replay/substitution detectable. Conceptually include or commit to:
- effect/incident identity and causal lineage;
- closure generation;
- declared closure scope/invariant;
- authoritative decision/policy generation;
- evidence-set identifier/commitment and evidence freshness bounds;
- mandatory downstream reconciliation summary;
- residual-risk decision identity/expiry where applicable;
- predecessor closure/reopen lineage;
- decision/verifier identity and authorization context;
- creation/observation time from an appropriate authoritative context;
- status such as `CLOSED-MONITORED`, `REOPENED`, `SUPERSEDED`;
- integrity/authenticity mechanism appropriate to consequence.

Exact schema and cryptography remain product-specific.

## Authenticity, integrity, completeness and currentness are different questions

A robust verifier asks separately:
1. **Integrity:** are these committed bytes/fields unchanged?
2. **Authenticity:** is the producer/verifier identity binding valid under the relevant trust generation?
3. **Authorization:** was that actor permitted to make this closure decision for this scope?
4. **Completeness/continuity:** is required lineage present, or was a reopen/superseding event omitted?
5. **Currentness:** is this the accepted current closure generation rather than an authentic historical one?
6. **Semantic support:** do the referenced evidence and current provider/downstream state support the closure invariant?

Cryptography can strongly help with the first two and lineage commitments, but it cannot prove that a provider statement was truthful, that an omitted downstream never existed, or that the closure invariant was correctly chosen.

## Independent verification is failure-mode specific

Do not use “independent” as a binary label. Ask independent from what:
- same database mutation privilege;
- same cloud account/root credential;
- same deployment pipeline;
- same operator/custodian;
- same backup/PITR domain;
- same signing key/trust root;
- same provider observation source;
- same network/identity dependency.

A separate bucket in the same compromised account may be operationally separate but not independent against account-root compromise. Conversely, complete organizational separation may be unnecessary for lower-consequence evidence. Independence requirements follow the threat/consequence model.

## Anti-forgery / anti-resurrection model

### Generation and lineage
Closure, reopen and reclosure are forward events. Never mutate historical closure into “never happened.” A later accepted generation supersedes earlier claims while retaining lineage.

### Monotonic currentness floor
A restore or stale replica must not lower the accepted closure/reopen generation. The system needs a currentness mechanism strong enough that a pre-reopen backup cannot make historical `CLOSED` authoritative again. This may reuse the anti-rollback/checkpoint patterns from 099, 136 and 153; exact implementation remains OPEN.

### Evidence commitments
Where consequence justifies it, retain compact commitments/identifiers to the evidence set and critical decision context separately from mutable operational rows. A commitment proves only the committed representation; canonicalization/versioning must be explicit if hashes/signatures are used.

### Independent observation
For high-consequence closure, preserve at least one verifier/anchor path whose compromise is not identical to ordinary incident-row mutation, when the threat model justifies it. This can be separate protected audit infrastructure, provider-signed/identified receipts plus independent currentness checks, or another bounded mechanism. No universal architecture is prescribed.

### Negative verification
After reopen/supersession, explicitly test that old closure claims fail current-authority checks even if their historical integrity/authenticity still verifies.

## Privacy-minimized evidence retention

Retain the minimum evidence necessary for the declared proof and investigation/retention obligations. Separate:
- **proof metadata/commitments** — IDs, generations, non-secret digests, decision lineage, timestamps/currentness context;
- **provider evidence** — bounded receipts/status references needed for reconciliation;
- **sensitive recoverable content** — retained only when justified, access-controlled/encrypted and lifecycle-governed;
- **secrets/bearer material** — do not retain merely to make an audit look complete.

Hashing is not automatic anonymization. Low-entropy identifiers or small domains may be guessable; hashes can also remain personal data depending on context/jurisdiction. Product/legal privacy validation remains OPEN.

Retention periods are consequence/legal/product specific. Evidence must not be destroyed before required retention, but indefinite retention is not a generic security virtue.

## Provider evidence and freshness

A provider receipt can substantiate that a provider returned a statement at a point in time. It does not automatically prove:
- the provider state remained unchanged;
- all provider replicas had converged;
- the statement came from the authoritative endpoint unless source/authentication is established;
- the provider was truthful/correct;
- the statement remains current after policy/key/account changes.

Closure proof therefore records freshness/currentness semantics separately from integrity/authenticity.

## Backup, replica and PITR recovery

On restore:
1. recover business/incident data;
2. recover or reacquire accepted closure/reopen currentness floor from the stronger recovery evidence path;
3. reject operational closure rows below that floor as historical/stale;
4. verify lineage/evidence commitments for accepted generations;
5. reconcile provider/downstream current state where evidence freshness no longer suffices;
6. do not “repair” disagreement by deleting the stronger contradiction.

`PITR timestamp newer than incident row ≠ closure claim newer than independent accepted lineage`.

## PWA / Service Worker / managed-iPad application

For a LogMate/EFB-like PWA:
- Service Worker/cache/IndexedDB may retain an authentic historical closure state while offline;
- local display state is not an independent verifier of server closure currentness;
- reconnect must compare current server generation/currentness before presenting old `CLOSED` as current or replaying mutations;
- an old closure claim may remain visible as historical provenance while UI truthfully marks `REVALIDATION REQUIRED` or `SUPERSEDED`;
- unique local flight data remains preservable/exportable even when closure authority cannot be validated;
- cached evidence must not contain bearer recovery credentials merely for offline audit display;
- browser storage durability, eviction, backup and managed-iPad behavior remain OPEN until physical/runtime validation.

## Cross-track integration

### Track A — Platform & Browser
Own exact persistence/cache/SW/offline queue behavior and reconnect semantics. Dependency: prove that cached historical closure cannot silently become current authority after reconnect/update/restore.

### Track B — UX / IA / Content
Own truthful distinction among `HISTORICAL CLOSURE`, `CLOSED — VERIFIED CURRENT`, `REVALIDATION REQUIRED`, `REOPENED`, `SUPERSEDED`, and evidence-unavailable states. Avoid presenting cryptographic jargon as user reassurance without operational meaning.

### Track C — Performance / Accessibility / Quality
Own destructive restore/replay/forgery/currentness tests and accessible state presentation. Verify evidence-service outage behavior without allowing silent fail-open closure.

### Track D — Search / Discovery / Analytics
Diagnostic consumer only. Analytics may detect old-closure clients or anomalous generation use, but analytics data cannot independently certify closure and telemetry silence cannot prove currentness.

### Track E — Owner
Own evidence trust boundaries, retention/minimization, verifier independence, closure generation/currentness, anti-resurrection and recovery governance.

## MINTTAP DECISION — minimal generic model

1. Treat closure as a versioned claim with lineage, not a mutable incident boolean.
2. Separate historical authenticity from current authority; an authentic old `CLOSED` claim may be superseded.
3. Preserve enough evidence-set commitment and decision context to detect substitution/truncation appropriate to consequence.
4. Require verifier/evidence independence relative to the threat being defended against; do not infer independence from extra replicas alone.
5. Keep closure/reopen currentness monotonic across restore and stale replicas.
6. Reconcile stale provider evidence rather than treating signed/retained receipts as timeless truth.
7. Minimize evidence: retain proof metadata and necessary provider evidence without storing bearer secrets or unnecessary sensitive payloads.
8. Preserve closure→reopen→reclosure provenance; never rewrite history to simplify dashboards.
9. Offline PWA state may preserve historical evidence but cannot mint or resurrect current server closure authority.
10. Do not claim product PASS until actual evidence store, provider semantics, verifier trust, backup/restore, SW and managed-iPad behavior are tested.

## VALIDATION — 72-case anti-forgery/evidence campaign

1 closure row changed without evidence commitment; 2 detect; 3 evidence commitment changed; 4 detect; 5 closure signed by unauthorized actor; 6 reject; 7 valid signature under retired key; 8 historical verify/current reject; 9 closure N authentic; 10 reopen N+1 exists; 11 stale replica serves N; 12 currentness check rejects; 13 backup predates N+1; 14 restore; 15 monotonic floor prevents resurrection; 16 PITR contains newer wall-clock row but older authority lineage; 17 reject as current; 18 provider receipt authentic but expired/stale; 19 requery; 20 provider unavailable; 21 closure confidence degrades rather than fabricate; 22 two replicas share same compromised admin; 23 do not count as independent; 24 separate evidence store but same root credential; 25 independence claim bounded; 26 verifier read-only but deployment pipeline compromised; 27 threat analysis; 28 evidence store unavailable; 29 consequence-specific fail/degrade path; 30 raw access token appears in evidence; 31 redact/do not persist; 32 hashed low-entropy identifier; 33 privacy review; 34 provider payload contains PII; 35 minimize/encrypt/access-control; 36 retention expiry; 37 dispose according to policy while retaining permitted non-secret lineage if required; 38 closure proof needs disposed raw payload; 39 evidence design failure surfaced; 40 append-only commitment valid but semantic evidence false; 41 do not equate integrity with truth; 42 valid leaf but omitted reopen branch; 43 continuity/currentness detects; 44 split-view verifier observations; 45 investigate; 46 old Service Worker caches CLOSED N; 47 server is REOPENED N+1; 48 reconnect displays superseded/revalidation state; 49 offline device never reconnects; 50 local historical display cannot authorize remote mutation; 51 unique flight data remains readable/exportable; 52 cache eviction removes local closure evidence; 53 server evidence remains authoritative; 54 local device clock wrong; 55 does not choose generation; 56 closure claim copied between users/effects; 57 target binding rejects; 58 closure claim copied between environments; 59 environment/trust binding rejects; 60 canonicalization version mismatch; 61 verification fails safely/legacy verifier isolated; 62 evidence verifier key rotation; 63 historical verify without enabling old current signing; 64 evidence service operator tries to create closure; 65 role separation rejects; 66 incident operator tries to delete reopen evidence; 67 protected audit path detects/prevents; 68 accessibility exposes current/historical distinction without color alone; 69 keyboard/focus on revalidation action; 70 screen-reader wording does not say “fixed” for historical closure; 71 end-to-end restore + long-offline iPad reconnect; 72 prove old closure remains historical while current lineage and local data survive.

## CONTRADICTION / failure-mode analysis

### Immutable-self-attestation
An append-only log controlled by the same compromised root can be consistently rewritten before anchoring or can record false statements immutably. Append-only is useful but not equivalent to independent truth.

### Signature theater
A signature proves a key signed bytes. It does not prove the key was authorized for that closure generation, the evidence was complete, or the claim is still current.

### Replica-count theater
Three replicas under one administrator/account can fail together. Independence is about failure domains and privileges, not count.

### Privacy-by-hoarding
Keeping every raw provider response, token and user record forever creates evidence volume while increasing confidentiality and breach risk. Proof design should minimize retained sensitive content.

### Historical-closure resurrection
A backup restores a perfectly authentic `CLOSED` claim while omitting a later reopen. Currentness/lineage, not row validity alone, must reject it.

### Offline-client authority confusion
A stale PWA showing `CLOSED` may be historically correct and currently wrong. Preserve the history, revalidate currentness, and never derive server authority from cached display state.

## OPEN

Product/runtime evidence is required for actual closure/evidence schema, consequence classes, provider receipts, audit infrastructure, independent verifier/anchor, signing/key/trust model, canonicalization, retention/legal/privacy requirements, backup/PITR semantics, replica topology, identity/admin separation, Service Worker cache/data model, managed-iPad storage/update behavior, native-mobile sync and aviation obligations.

## CHANGE WATCH

- NIST SP 800-92 Rev.1 status and finalization;
- NIST SP 800-53/AU control revisions;
- OWASP logging guidance;
- cryptographic algorithm/key guidance used by any chosen evidence mechanism;
- provider receipt/API/currentness semantics;
- WebKit/iPadOS PWA storage/update/background behavior;
- privacy/legal/aviation retention requirements.

## Gate result

**PASS (generic).** Track E now has a reusable closure-evidence retention, verifier-independence and anti-forgery model. Production validation remains OPEN.
