# 219 — PWA Currentness-Witness Trust, Collector Compromise, Equivocation & Independent Convergence Attestation

Status: **PASS (generic) / PRODUCT + WITNESS/COLLECTOR + DISTRIBUTED-ENFORCEMENT + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline-state mechanics; Track B uncertainty/reconciliation UX; Track C destructive and independence validation; Track D observation/measurement.  
Dependencies: 122–137, 171–218 and earlier authority/currentness/recovery/evidence work.

## Problem
218 established that policy publication, distribution, consumption, enforcement and observation are separate, and that a convergence claim needs a known enforcement-set denominator. The adjacent failure is that the **observation plane itself can lie**. A collector can be compromised, replay a once-valid witness, omit an inconvenient endpoint, accept duplicate identities, or present different fleet views to different operators. If policy publication, enforcement telemetry and convergence declaration share one compromise domain, a green dashboard can become self-attestation rather than assurance.

Central rule: **currentness witnesses are evidence about enforcement, not authority; convergence confidence depends on provenance, freshness, denominator integrity, anti-replay/anti-equivocation properties and appropriate independence from the authority/enforcement domains being assessed. No single collector, signature, dashboard or transparency receipt proves the underlying enforcement statement is true.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Exact Service Worker/cache/storage/network behavior explains stale local reports and offline gaps; browser state does not make a witness current.
- **B UX/IA/Content:** high dependency pressure. Must communicate `current`, `partially corroborated`, `collector degraded`, `fork detected`, `unknown tail`, and `data preserved / sync blocked` without converting uncertainty into an unsafe override.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **504 → 512 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May aggregate witness age, fork/conflict counts, collector disagreement and unknown-tail age, but analytics cannot decide authority or suppress contradictory evidence.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns witness trust model, collector failure domains, anti-replay/equivocation evidence, independent corroboration, witness succession/revocation and convergence-claim closure.

## SOURCE

### NIST SP 800-53 Rev.5 / SP 800-53A Rev.5 — control operation and assurance are separate
NIST SP 800-53 treats security/privacy functionality and assurance as distinct concerns. SP 800-53A supplies assessment procedures for obtaining evidence that controls operate as intended.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** an enforcement plane declaring itself current is not equivalent to independently supported assurance that it is current. NIST does not prescribe MintTap's witness protocol.

### RFC 9162 — signed views can still equivocate
Certificate Transparency v2 explicitly identifies a misbehaving log presenting different conflicting Merkle-tree views to different parties. Append-only and view-consistency auditing relies on comparing signed tree heads/consistency evidence; a signature alone does not establish non-equivocation.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** a signed collector checkpoint can be authentic and still be one side of a split view. CT is a precedent for anti-equivocation reasoning, not a requirement to implement CT for MintTap policy telemetry.

### RFC 9943 — transparency separates signed statements from registration receipts
RFC 9943 defines signed statements and transparency-service receipts as separate artifacts. Registration/transparency makes a statement auditable; it does not make the issuer's statement substantively true.

Source:
- https://www.rfc-editor.org/rfc/rfc9943.html

**TRANSFER VALIDATION:** external registration or receipt can strengthen evidence provenance and detect omission/fork classes, but `transparent ≠ truthful` and `receipt verifies ≠ enforcement state true`.

## SYNTHESIS 1 — model four identities, not one
For a convergence observation distinguish:
1. **enforcement-point identity** — what boundary actually made the consequence-bearing decision;
2. **witness identity** — what component observed/tested that boundary;
3. **collector identity** — what service aggregated/normalized witness evidence;
4. **attestor/auditor identity** — what independent party or process corroborated the convergence claim.

These can intentionally collapse in low-risk cases, but the collapse is a trust decision, not a fact hidden by one service account.

`endpoint identity ≠ witness identity`; `witness identity ≠ collector identity`; `collector authenticated ≠ collector independent`.

## SYNTHESIS 2 — a signed witness proves origin/integrity, not truth
A useful witness should bind endpoint, policy namespace/generation, evaluator version, tested capability, predecessor rejection floor, observation sequence/time, nonce/challenge where applicable, result, collector route and evidence provenance.

A valid signature can establish who signed which bytes. It does not prove the endpoint really enforced the claimed policy, that the witness observed the intended endpoint, or that the collector did not omit contradictory reports.

`signed witness ≠ truthful witness`; `signature valid ≠ endpoint tested`; `endpoint tested ≠ complete enforcement set tested`.

## SYNTHESIS 3 — freshness needs anti-replay context
Wall-clock timestamps alone are weak replay defenses. Where architecture permits, bind observations to authenticated policy generations, monotonic witness/collector sequences, challenge/nonces, bounded validity windows and predecessor floors. Preserve enough lineage to distinguish a late-delivered current observation from an old observation replayed after rollback.

`recently received ≠ recently observed`; `fresh timestamp ≠ fresh authority`; `once-valid witness ≠ current witness`.

## SYNTHESIS 4 — collector compromise is an omission and framing problem
A compromised collector need not forge endpoint signatures. It can:
- omit stale endpoints;
- redefine the denominator;
- delay contradictory evidence;
- replay a prior all-green bundle;
- merge two logical endpoints under one identity;
- classify UNKNOWN as healthy;
- expose different dashboards to different operators.

Therefore the convergence bundle must bind the **enforcement-set inventory revision**, included and excluded members, unknown/unreachable tail, evidence window, collector version/configuration and unresolved contradictions.

`all collected green ≠ all endpoints green`; `collector says denominator N ≠ denominator N independently complete`.

## SYNTHESIS 5 — equivocation requires comparison across views
If collector C signs bundle B1 for operator O1 and conflicting B2 for O2, each signature can verify. Detection requires an overlapping comparison surface: independent auditor, replicated observer under a distinct failure domain, externally anchored checkpoint, cross-operator gossip, or equivalent mechanism appropriate to risk.

RFC 9162 is useful precedent: signed heads plus comparison/consistency evidence expose conflicting views. The exact MintTap mechanism is **OPEN**.

`one valid view ≠ one global view`; `two valid signatures ≠ views consistent`; `fork detected ≠ root cause proven`.

## SYNTHESIS 6 — independence is about failure domains, not vendor count
Two collectors are not meaningfully independent if they share the same credentials, database, deployment pipeline, cloud account, policy publisher, administrator, telemetry source or compromise path. Conversely, full organizational separation is not always necessary; independence should be proportional to consequence and explicitly modeled.

`two collectors ≠ two independent collectors`; `different service name ≠ different failure domain`; `same raw source + two dashboards ≠ independent corroboration`.

For high-consequence authority extinction, prefer at least one corroborating path that does not depend solely on the authority/publisher being assessed.

## SYNTHESIS 7 — corroboration is claim-specific
Independent evidence need not duplicate the entire monitoring stack. It can target the dangerous claim:
- active challenge of predecessor rejection at selected enforcement points;
- provider/API query from a separately governed credential;
- independent checkpoint of the enforcement-set inventory;
- read-only audit path into regional enforcement state;
- PITR/rejoin destructive test;
- cross-check of accepted/rejected operation outcomes.

The goal is not maximal telemetry duplication; it is breaking common-mode false confidence for the material assertion.

`independent corroboration ≠ duplicate everything`; `sample corroboration ≠ universal proof`.

## SYNTHESIS 8 — convergence closure needs contradiction handling
A convergence state should not be Boolean. Useful generic states include:
- **CORROBORATED-CURRENT** — required evidence and independence criteria met for stated scope;
- **CURRENT-UNILATERAL** — current evidence exists but only inside one trust/failure domain;
- **PARTIAL** — some required points or evidence classes unresolved;
- **CONTRADICTED** — authentic evidence disagrees;
- **FORK-SUSPECTED / FORK-PROVEN** — incompatible views require investigation;
- **UNKNOWN** — evidence unavailable or denominator unresolved.

A contradictory authentic witness must not be averaged away by a majority of green metrics unless the policy explicitly defines a justified quorum model.

`majority green ≠ contradiction resolved`; `dashboard aggregate healthy ≠ material red evidence irrelevant`.

## SYNTHESIS 9 — witness/collector succession is not authority succession
Witness keys, collectors and schemas need rotation/replacement. Successor observation infrastructure must preserve lineage and anti-replay floors without inheriting policy-authoring power. A retired witness may remain verifiable historically but must not create fresh currentness claims.

`new collector active ≠ old collector extinct`; `historical witness verifies ≠ witness may issue current observation`; `collector succession ≠ policy authority succession`.

Compromise recovery must distinguish compromise window, historical verification and current acceptance exactly as earlier evidence/key lifecycle work requires.

## SYNTHESIS 10 — PWA/offline clients are evidence tails, not local auditors of global convergence
A long-offline company iPad can truthfully report its own cached generation and local state, but cannot prove fleet currentness. On return:
1. preserve unique flight/logbook data;
2. authenticate current policy/currentness basis;
3. classify its old witness/cache as historical;
4. update evaluator/schema as required;
5. re-test admission/predecessor rejection;
6. release queued consequence-bearing work only under current rules.

If the collector plane is degraded or forked, local data utility can continue within explicitly safe offline capability while remote mutation remains blocked.

`client self-report ≠ fleet attestation`; `offline evidence preserved ≠ offline authority current`.

## SYNTHESIS 11 — evidence-plane outage must not become security bypass
If witness/collector infrastructure is unavailable, distinguish:
- enforcement itself remains safely current but assurance is temporarily degraded;
- enforcement currentness cannot be established;
- collector is suspected compromised;
- conflicting evidence exists.

These states justify different operational responses. Do not silently map all to `monitoring unavailable, proceed normally` or `monitoring unavailable, policy absent`.

`collector unavailable ≠ enforcement failed`; `collector unavailable ≠ enforcement proven current`; `assurance degraded ≠ restriction waived`.

## SYNTHESIS 12 — closure statements must be scoped and reproducible
A defensible generic statement is:

> For enforcement-set revision I and capability scope S, reachable members demonstrated generation G-or-later enforcement and predecessor rejection during interval T; required corroboration paths C1/C2 agreed; unresolved tail U is restricted from consequence-bearing admission; no unresolved contradictory signed view is known within the stated evidence scope.

Do not claim global impossibility of stale authority or collector compromise.

## MINTTAP DECISION / DIRECTION
1. Treat witness/collector evidence as an **assurance plane**, never as policy-authoring authority.
2. Bind convergence bundles to enforcement-set inventory revision, scope, policy/evaluator generation, freshness context and unresolved tail.
3. For material revocation/authority-extinction claims, require claim-specific corroboration outside the sole authority/publisher failure domain where practical.
4. Preserve contradictory authentic evidence; do not normalize it away into a dashboard percentage.
5. Model collector/witness succession and revocation separately from policy authority succession.
6. For offline-first LogMate-like use, preserve unique data while withholding consequence-bearing sync when currentness evidence is insufficient or forked.

These are generic architecture directions, not assertions about current MintTap/LogMate implementation.

## OPEN / DEPENDENCY
- Exact MintTap/LogMate enforcement-set inventory, witness schema, collector topology, credentials and failure domains: **OPEN**.
- Whether any current product uses signed witnesses, transparency/checkpoints or independent collectors: **OPEN**.
- Exact iPadOS/WebKit/Service Worker/storage/background behavior: **Track A + Software Engineering runtime dependency**.
- Operator-facing degraded/fork/reconciliation UX: **Track B consuming Design Studio; human validation OPEN**.
- Physical iPad, Safari, MDM, network-partition and reconnect evidence: **OPEN**.
- Legal/aviation retention or evidentiary requirements: **OPEN**.

## Track C destructive campaign — 504 → 512 defined cases
Add:
1. **Replay after rollback:** collector replays a genuinely signed G12 witness after endpoint rollback to G10.
2. **Denominator omission:** collector drops one stale provider-console path and reports 100% convergence.
3. **Split-view collector:** O1 receives all-green bundle B1 while O2 receives B2 containing a stale region; both collector signatures verify.
4. **Shared-domain pseudo-independence:** two collectors use separate processes but the same credential/database/deployment account; one compromise controls both.
5. **Duplicate endpoint identity:** stale region reports using the identity of a current region and overwrites its witness.
6. **Contradiction laundering:** one authentic red witness is averaged into an overall green SLO and closure is declared.
7. **Collector succession replay:** retired collector key remains accepted for new convergence bundles after successor activation.
8. **Long-offline iPad under collector incident:** device returns with unique data while assurance plane is fork-suspected; data remains preserved and remote mutation remains blocked until current admission evidence is restored.

These are **defined failure oracles, not executed PASS evidence**.

## TRANSFER / CONTRADICTION
- **Track A:** cached/browser-local evidence can explain stale observations but cannot establish fleet authority/currentness.
- **Track B:** uncertainty/fork/degraded-assurance states need comprehensible, accessible communication without a user-controlled security downgrade.
- **Track C:** implementation must test replay, omission, split-view, duplicate identity, collector succession and common-mode compromise; reading alone is not runtime PASS.
- **Track D:** telemetry can expose witness age/disagreement/unknown tails; analytics is not a convergence authority.
- **Design Studio:** current Web status remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and human UX evidence remain OPEN.
- **Software Engineering Studio:** Foundation remains in study; physical iOS/Safari/EFB and exact-product runtime remain OPEN. No generic Web Manager synthesis upgrades those execution gates.

## Persistent guards added
`collector authenticated ≠ collector independent`; `signature valid ≠ endpoint tested`; `endpoint tested ≠ complete enforcement set tested`; `recently received ≠ recently observed`; `once-valid witness ≠ current witness`; `all collected green ≠ all endpoints green`; `collector denominator ≠ independently complete denominator`; `one valid view ≠ one global view`; `two valid signatures ≠ views consistent`; `two collectors ≠ two independent failure domains`; `same raw source + two dashboards ≠ independent corroboration`; `majority green ≠ contradiction resolved`; `new collector active ≠ old collector extinct`; `historical witness verifies ≠ witness may issue current observation`; `client self-report ≠ fleet attestation`; `collector unavailable ≠ enforcement proven current`; `assurance degraded ≠ restriction waived`; `transparent ≠ truthful`; `receipt verifies ≠ enforcement state true`.

## Gate result
**219 PASS (generic).** The knowledge gate closes because witness/collector trust, replay, omission, equivocation, failure-domain independence, corroboration, succession, contradiction handling and offline-PWA consequences now have explicit evidence boundaries and destructive oracles. Product/runtime validation remains OPEN.

## Next high-value adjacent question
**220 — convergence-attestation quorum policy, witness diversity degradation & emergency assurance-mode transitions**: determine when multiple corroborators may form a quorum, how weights/thresholds avoid pseudo-independence and correlated failure, how to operate when witness diversity collapses, and how emergency assurance degradation can preserve availability without silently converting missing assurance into authorization.