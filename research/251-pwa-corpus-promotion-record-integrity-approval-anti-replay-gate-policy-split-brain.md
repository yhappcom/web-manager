# 251 — PWA Corpus-Promotion Record Integrity, Approval Anti-Replay & Gate-Policy Split-Brain Resistance

Status: **PASS (generic) / PRODUCT + GOVERNANCE + CORPUS + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A platform/runtime currentness mechanics; Track B recovery/status UX; Track C destructive gate validation; Track D bounded divergence/rollout metrics.  
Dependencies: 137, 171–250, especially anti-rollback/fork recovery, governance succession, branch convergence, oracle/corpus provenance, retirement/replay resistance and promotion authority.

## Problem
250 separated corpus authorship, semantic authority, promotion and gate enforcement. The next failure surface is the promotion control plane itself. A valid corpus can still be misused when its promotion record is replayed outside its approved scope, when CI/recovery/PWA clients observe different current gate policies, when a superseded approval remains accepted, or when a compromised promotion service rewrites history while claiming a clean successor state.

Central rule: **a promotion record is a provenance-bearing authorization object, not a boolean label. Bind it to exact corpus identity, semantic/policy generation, gate/consequence scope, governance generation, predecessor/floor, validity/currentness conditions and approval evidence; require monotonic/fork-aware gate-policy convergence; and preserve compromised historical records while moving current authority to an independently established successor.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Supplies exact Service Worker/cache/runtime generation and client currentness mechanics; browser update success cannot elect gate policy.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `PROMOTION-PENDING`, `PROMOTION-STALE`, `GATE-POLICY-CONFLICT`, `REVALIDATION-REQUIRED`, `HISTORICAL-ONLY` and `BOOTSTRAP-REQUIRED` states without destructive reset.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns destructive anti-replay/split-brain validation. Campaign expands **760 → 768 defined cases**; defined cases are not execution PASS.
- **D Search/Discovery/Analytics:** bounded consumer. Measures gate-policy generation distribution, stale tails, conflict sightings and convergence windows with explicit denominators; telemetry cannot choose canonical policy.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns promotion-record integrity, currentness, revocation/supersession, anti-replay, split-brain containment, recovery and publication/consumption policy.

## SOURCE

### NIST configuration change-control precedent
NIST SP 800-53 CM-3 / assessment guidance treats controlled change as requiring designated approval, documentation, retained records and review; automated mechanisms may inhibit change until required approvals are received. This is bounded governance precedent for retaining promotion authorization and preventing an artifact from becoming current merely because it exists.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-53ar1.pdf

**TRANSFER VALIDATION:** a MintTap corpus-promotion record is not a NIST configuration item, but approval-record integrity/currentness is analogous. NIST does not prescribe the MintTap schema or quorum.

### TUF — rollback/freeze and consistent repository views
TUF documents rollback and indefinite-freeze attacks. Snapshot metadata records versions/hashes of targets metadata so clients cannot safely combine metadata from different repository states; Timestamp is short-lived and points to Snapshot, helping clients detect stale views.

Sources:
- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/docs/metadata/

**TRANSFER VALIDATION:** bounded precedent for authenticated currentness, anti-rollback and coherent metadata views. MintTap does not adopt TUF as its promotion protocol.

### RFC 9162 — consistency and split-view reasoning
Certificate Transparency v2 defines signed tree heads and consistency proofs between tree states and explicitly treats consistency of the view presented to all query sources as an audit property. One signed view is not proof that every observer received the same view.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** bounded anti-equivocation precedent only; MintTap does not adopt Certificate Transparency infrastructure.

### SLSA — provenance must be verified against expectations
Current SLSA documentation identifies v1.2 as current and treats provenance as verifiable information that is useful only when consumers inspect it against expectations. This supports separating authenticated promotion metadata from the consumer policy that decides whether it is applicable.

Source: https://slsa.dev/

**TRANSFER VALIDATION:** bounded supply-chain precedent; corpus promotion remains a MintTap-specific governance model.

### Current cross-repository boundary
Design Studio Web remains **W121 / Stage 3 PRACTICE / NOT PASSED**; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Software Engineering Studio remains **Foundation IN STUDY / no specialist PASS**; repaired exact-fixture macOS Safari Service Worker registration→control→V1→V2 update/controller replacement→fresh-WebDriver V2 control recovery is bounded PASS, while origin-down fresh cold-start, installed PWA, physical iOS/iPadOS/EFB and canonical-product runtime remain OPEN.

**DEPENDENCY:** generic promotion-record governance does not upgrade those gates.

## SYNTHESIS 1 — promotion record is an authorization object
A promotion record should bind at least:
1. exact corpus identity/digest and generation;
2. semantic/policy/schema/parser/verifier generations where material;
3. gate and consequence scope;
4. governance/approval-policy generation;
5. predecessor/floor or supersession relation;
6. approvals and their applicable roles/currentness;
7. effective interval/expiry where relevant;
8. known coverage debt/exceptions;
9. record format/version and verification context.

A detached `approved=true`, branch tag or mutable database field is insufficient for consequence-bearing use.

Guards: `approval bit present ≠ promotion record valid`; `record signature valid ≠ record applicable`; `corpus digest matches ≠ gate scope matches`.

## SYNTHESIS 2 — anti-replay is multidimensional
A previously authentic approval can be replayed against:
- a different corpus with a friendly/reused identifier;
- a different gate or operation class;
- a successor semantic/policy generation;
- a successor governance generation;
- a later interval after expiry/revocation/supersession;
- a lower predecessor/floor after the consumer has advanced.

Therefore anti-replay cannot be reduced to signature verification or timestamp comparison.

Guard: `historically authorized ≠ currently authorized here`.

## SYNTHESIS 3 — promotion currentness needs monotonic consumer state
Consequence-bearing consumers should remember or obtain an authenticated minimum promotion/gate-policy floor appropriate to their trust model. A client that has accepted G20 must not silently accept authentic G17 merely because G17 remains cryptographically verifiable.

TUF rollback/freeze reasoning is a bounded precedent for this property.

Guards: `authentic old policy ≠ acceptable policy`; `server says latest ≠ client may forget known floor`.

## SYNTHESIS 4 — CI, recovery and PWA are separate consumers that can split
CI may enforce policy P20 while recovery tooling still accepts P18 and an offline PWA returns with P12. Each component can be internally consistent yet the product system is split-brain.

Model a **gate-policy generation** independently from app build and Service Worker generation. Promotion publication is not complete until required consequence boundaries have converged or are explicitly isolated/degraded.

Guard: `CI current ≠ recovery current ≠ fleet current`.

## SYNTHESIS 5 — split-brain is not resolved by newest timestamp or majority
If CI reports P20 and recovery reports a conflicting P20B, do not choose the branch with the newest timestamp, most clients or fastest endpoint. Establish canonical successor from governance/bootstrap evidence and preserve the conflict.

RFC 9162 provides bounded precedent that consistency across observers is a separate property from validity of an individual signed view.

Useful state: `GATE-POLICY-CONFLICT`.

Guards: `most-observed policy ≠ canonical policy`; `newest signed policy ≠ canonical successor`.

## SYNTHESIS 6 — coherent publication prevents mix-and-match
A consumer must not combine corpus C20 from one state, promotion record R19 from another and exception E20B from a third merely because each object individually verifies. The accepted set must belong to a coherent authorized snapshot/lineage or have an explicit composition rule.

TUF Snapshot metadata is bounded precedent for preventing mix-and-match across repository states.

Guard: `all components authentic ≠ component set coherent`.

## SYNTHESIS 7 — revocation and supersession are not historical deletion
When a promotion record is superseded or revoked for current use, preserve the original record and append the successor/revocation assertion. Historical analysis may still need to know that C17 was authorized during interval I17.

If the original approval was later discovered compromised, record that contradiction and affected interval/claims rather than silently editing history.

Guards: `revoked current authority ≠ historical record erased`; `compromised approver ≠ every prior record automatically false`.

## SYNTHESIS 8 — control-plane compromise requires independent recovery
If the promotion service or signing authority is compromised, it cannot self-certify that its own successor state is clean. Recovery must rely on the previously defined independent governance/bootstrap/recovery basis appropriate to the failure hypothesis.

Preserve disputed records as evidence, move current authority to a successor generation, and require consequence boundaries to reject compromised predecessor authority.

Guard: `new key signed by compromised old authority ≠ trust restored`.

## SYNTHESIS 9 — cache and Service Worker mechanics cannot establish promotion currentness
A Service Worker may cache a promotion manifest or gate policy. Cache hit, successful update, `controllerchange`, `skipWaiting()` or app-shell freshness says nothing about whether the cached policy remains current or canonical.

Track A owns lifecycle mechanics; Track E owns authenticated currentness and bootstrap; Track C validates stale/fork/restart sequences.

Guard: `cached signed promotion ≠ current promotion`.

## SYNTHESIS 10 — offline clients preserve floors and evidence, not authority
A long-offline iPad returning with P12/C12 should preserve those objects for historical interpretation. It must not use them to authorize current sync merely because they were valid when cached. Conversely, current server P20 cannot simply discard unique offline data because the device is stale.

Sequence: preserve unique data/evidence → obtain current bootstrap/canonical gate-policy generation → detect rollback/fork/conflict → migrate schema/data separately → re-evaluate queued operations under current authorized corpus/policy.

Guard: `offline cached authority valid then ≠ authority valid now`.

## SYNTHESIS 11 — analytics detects divergence but cannot elect truth
Track D may measure policy-generation distribution, stale-client tail, conflict sightings, superseded-record use and convergence latency. Sampling gaps and offline clients must remain explicit.

Guard: `telemetry majority ≠ canonical gate policy`; `zero conflict observed ≠ no split view exists`.

## SYNTHESIS 12 — currentness failure should be fail-closed only for the affected consequence
Unknown promotion currentness need not blank the entire application. Preserve read-only/local unique-data access where safe while isolating consequence-bearing sync, mutation, release or recovery operations that require current authority.

Track B must communicate this without implying data loss or universal outage.

Guard: `authority uncertain ≠ destroy data`; `sync blocked ≠ local record unavailable`.

## MINTTAP DECISION / DIRECTION
Generic policy only; actual product implementation remains OPEN.

1. Treat corpus-promotion records as scoped, provenance-bearing authorization objects, not mutable approval flags.
2. Bind approvals to exact corpus, semantic/policy and governance generations plus gate/consequence scope and currentness conditions.
3. Enforce anti-replay across corpus identity, scope, generation, governance, interval and consumer floor.
4. Maintain an authenticated gate-policy generation/floor distinct from app/Service Worker build generation.
5. Treat CI, recovery tooling and PWA clients as separate policy consumers; detect and contain split-brain explicitly.
6. Do not resolve conflicting valid-looking gate policies by newest timestamp, majority or endpoint availability.
7. Require coherent policy/corpus/exception snapshots or explicit composition rules; reject mix-and-match state.
8. Supersede/revoke by append-only successor evidence; preserve historical promotion records and contradictions.
9. Recover promotion-control-plane compromise from an independent bootstrap/governance basis; predecessor authority must be negatively retired at consequence boundaries.
10. Long-offline PWA rejoin preserves unique data and historical policy evidence, then obtains current canonical policy before operation-level re-admission.

## Track C destructive oracle additions — 760 → 768 defined cases
These are **defined tests, not executed PASS**.

1. **Cross-corpus approval replay** — valid approval for C20 is attached to friendly-ID C20B with different digest. Expected: reject.
2. **Cross-scope approval replay** — approval for read-only validation is reused for mutation/release gate. Expected: reject scope mismatch.
3. **Superseded-policy rollback** — consumer that accepted P20 receives authentic P17. Expected: reject below current floor / require authorized recovery.
4. **Gate-policy split-brain** — CI sees P20 while recovery sees conflicting P20B. Expected: `GATE-POLICY-CONFLICT`; no majority/newest election.
5. **Mix-and-match snapshot** — C20 + R19 + E20B all verify individually. Expected: reject incoherent set unless explicit authorized composition exists.
6. **Promotion-service self-clear** — compromised promotion signer issues a new key/policy and declares itself recovered. Expected: independent recovery/bootstrap required.
7. **Cached-Service-Worker promotion replay** — returning PWA uses cached signed P12 promotion after canonical P20. Expected: historical-only; current bootstrap/re-admission required.
8. **Offline-data destruction on stale policy** — stale iPad is reset because its gate policy is obsolete. Expected: preserve unique data/evidence; isolate authority-bearing operations instead.

Campaign total: **768 defined cases**. Execution, physical-device, AT and human validation remain OPEN.

## VALIDATION ladder
Generic reasoning PASS requires:
- bounded authoritative precedents for controlled approval records, anti-rollback/currentness, coherent metadata views and split-view reasoning;
- promotion-record schema/authority separation;
- multidimensional anti-replay model;
- gate-policy generation/floor and split-brain model;
- compromise/recovery and historical-retention rules;
- PWA offline/rejoin transfer analysis;
- destructive cases defined.

Product/runtime PASS additionally requires actual:
- corpus/promotion record formats and signing/verification path;
- governance generation, approval topology and revocation/supersession process;
- CI/recovery/runtime gate-policy consumers and enforced floors;
- conflict/convergence telemetry with explicit denominators;
- Service Worker/cache/update/restart and offline rejoin execution;
- physical iPadOS/WebKit/MDM evidence where in scope.

## OPEN
- Actual MintTap/LogMate promotion record schema, signer, approval topology, CI/recovery/admission gates and policy-distribution mechanism are unknown.
- No product-specific quorum, expiry or storage mechanism is prescribed.
- Physical iPadOS/WebKit/MDM PWA lifecycle/storage/sync behavior remains unverified.
- Production legal/aviation/safety obligations remain unknown.

## CHANGE WATCH
- NIST SP 800-53/800-128 change-control updates.
- TUF metadata/currentness guidance and RFC 9162-related transparency practice; both remain bounded precedents only.
- SLSA current specification/tooling; v1.2 is current documentation as checked 2026-09-23.
- Browser/OS PWA cache/update/storage behavior and actual product policy distribution once evidence exists.

## Gate
**251 generic PASS.** Product/governance/runtime/device validation remains OPEN.

Next highest-value adjacent question: **252 — gate-policy distribution compromise, consumer checkpoint recovery & partial-fleet convergence debt**: determine how consumers authenticate policy distribution when CDN/origin/cache paths disagree, how a client recovers when its stored monotonic floor/checkpoint is lost or corrupted without enabling rollback, and how to govern a partially converged fleet where some clients cannot yet consume the successor policy generation.