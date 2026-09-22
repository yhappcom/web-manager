# 230 — PWA Successor-Authority Distribution, Recovery-Key Custody & Compromise-Resistant Bootstrap Ceremony

Status: **PASS (generic) / PRODUCT + PROVIDER + PERSONNEL + MANAGED-IPAD + CEREMONY + RUNTIME VALIDATION OPEN**  
Date: 2026-09-22  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A PWA/client bootstrap mechanics; Track B recovery-state UX; Track C ceremony/bootstrap destructive validation; Track D recovery observability.  
Dependencies: 219–229, especially quorum diversity, emergency authority, dependency graphs, proof lineage, monotonic floors, anti-rollback anchors and fork recovery.

## Problem
229 established that a compromised normal anchor set cannot certify its own replacement. That creates the next question: how can an independently governed successor be authenticated and distributed without making the recovery mechanism a permanently usable bypass?

Central rule: **recovery authority must be independently protected, narrowly scoped and deliberately activated. Possession of recovery material is not equivalent to permission to use it; successful ceremony execution is not equivalent to successor fleet convergence. Successor trust requires an authenticated bootstrap lineage, bounded authority, evidence-bearing activation and post-recovery extinction/fencing of temporary recovery capability.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. A PWA client can retain a previously trusted minimum/checkpoint and verify an authenticated successor package, but Service Worker/Cache/IndexedDB state is not sovereign recovery authority. Long-offline bootstrap is client-relative and needs server-side admission after return.
- **B UX/IA/Content:** high dependency pressure. Recovery UI must distinguish LOCAL-SAFE, BOOTSTRAP-REQUIRED, RECOVERING and CURRENT without telling users preserved local data is lost or that connectivity alone restored trust.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight custody/ceremony/bootstrap destructive cases; campaign expands **592 → 600 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May measure ceremony activation, successor adoption, stale-tail age and rejected obsolete authority; analytics is not an activation or bootstrap authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns recovery authority scope, custody, activation, successor distribution, ceremony evidence and closure.

## SOURCE

### NIST SP 800-57 Part 1 Rev.5 — key management, compromise and split knowledge
NIST SP 800-57 Part 1 Rev.5 is current final general key-management guidance. It warns that additional key copies/locations increase compromise exposure even when they improve continuity, requires compromised keys to be revoked/replaced with damage assessment, and defines split knowledge as dividing key shares such that fewer than the required threshold do not reveal the key.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/split_knowledge
- https://csrc.nist.gov/glossary/term/key_recovery

**TRANSFER VALIDATION:** this does not prescribe a MintTap threshold or ceremony. It supports the separation between availability copies and independent custody, and between key reconstruction and authorization to exercise recovery authority.

### TUF — offline root threshold and root-compromise recovery
TUF separates roles and supports thresholds. Its current FAQ states that ordinary role-key compromise is repaired through Root authority, while compromise of a threshold of Root keys requires Root metadata to be re-issued out of band. Offline threshold keys reduce the likelihood that ordinary repository compromise captures recovery authority.

Sources:
- https://theupdateframework.io/spec/
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** TUF is an update framework, not an application admission protocol. The reusable pattern is role separation plus an independently protected bootstrap path when the normal root threshold is no longer trustworthy.

### RFC 9943 — transparency is evidence, not bootstrap authority
RFC 9943 provides signed-statement transparency, append-only/non-equivocation properties and receipts. It explicitly states that transparency does not prevent dishonest or compromised issuers; relying parties decide which issuers/transparency services to trust.

Source:
- https://www.rfc-editor.org/rfc/rfc9943.html

**TRANSFER VALIDATION:** transparency can preserve ceremony/successor statements and expose inconsistency, but a receipt does not grant recovery authority.

## SYNTHESIS 1 — recovery material and recovery authorization are different objects
A recovery private key/share, HSM capability or offline credential is sensitive material. Policy authorization to use it for a specific compromise scope is a separate decision. A custodian who can technically participate must not automatically have unilateral policy authority to trigger recovery.

`can sign recovery statement ≠ authorized to recover`; `key share held ≠ recovery approved`.

## SYNTHESIS 2 — custody independence is a failure-domain claim
Putting shares in different safes is insufficient if one identity administrator, cloud account, password vault, CI path, HSM administrator or recovery process can reach all of them. Independence must be evaluated across personnel, identity, device/HSM, physical/storage, administration and recovery dependencies.

`three custodians ≠ three independent failure domains`; `different location ≠ independent administration`.

## SYNTHESIS 3 — recovery authority should be dormant and capability-bounded
Recovery authority should not function as a standing alternate production writer. Its allowed actions should be narrower than normal authority: establish a successor trust basis/floor, revoke/retire compromised authority, and emit required recovery evidence. Product-data mutation, ordinary admin actions and unrelated policy bypass remain outside scope unless independently justified.

`recovery authority exists ≠ recovery bypass always enabled`; `root recovery capability ≠ product mutation capability`.

## SYNTHESIS 4 — ceremony activation needs explicit preconditions and evidence
A recovery ceremony should conceptually bind incident/compromise scope, predecessor authority under suspicion, required participant classes/threshold, current recovery-policy generation, successor identity/key material, minimum floor/checkpoint, effective scope/generation, evidence record and closure requirements. Exact product schema remains OPEN.

Ceremony evidence should establish who/what participated, which policy/version governed, what artifact was produced and whether the resulting successor was independently verified. A meeting record alone is not cryptographic or runtime proof.

`ceremony occurred ≠ ceremony authorized`; `minutes signed ≠ successor verified`.

## SYNTHESIS 5 — threshold improves compromise resistance only under independent custody
A k-of-n threshold can prevent one lost/compromised share from controlling recovery, but correlated custody can collapse the intended threshold. Threshold choice is therefore downstream of threat/failure-domain analysis, not a universal number.

`k-of-n configured ≠ k independent compromise domains`; `threshold met ≠ policy conditions met`.

## SYNTHESIS 6 — successor distribution needs authenticated lineage, not discovery alone
Regions and clients need a way to authenticate the successor against a trust basis not wholly controlled by the compromised predecessor. Discovery channels (DNS, API, push, MDM, support page, telemetry) may tell a client that recovery happened; they do not by themselves establish successor authority if they share the compromised trust cut.

`successor discovered ≠ successor authenticated`; `MDM delivered ≠ recovery lineage verified`.

## SYNTHESIS 7 — long-offline PWA bootstrap must preserve data before authority migration
A company iPad may miss the entire compromise and ceremony. On return, preserve unique flight/logbook data first. Its cached old root/floor can be useful to reject obvious downgrade, but cannot choose a successor after the old authority was compromised. Obtain an authenticated successor/checkpoint through the governed bootstrap path, migrate worker/schema/policy as required, then re-admit queued consequence-bearing operations individually.

`offline client has old trusted root ≠ old root remains current`; `successor package received ≠ queued writes authorized`.

## SYNTHESIS 8 — recovery testing must not normalize emergency authority
Recovery material that is never tested can fail when needed; exercising production recovery authority routinely can turn it into a standing bypass. Test the ceremony, custody availability, reconstruction/threshold mechanics, successor artifact generation and verifier path in isolated/non-production or tightly bounded destructive exercises. Where a production-side negative oracle is required, test rejection/fencing without granting broad product authority.

`recovery drill PASS ≠ production recovery authority activated`; `never used in production ≠ untested`.

## SYNTHESIS 9 — ceremony evidence itself needs anti-replay/currentness
An old valid recovery package must not be reusable after policy, custodian set, successor generation or compromise scope changes. Bind recovery artifacts to predecessor/scope, current recovery-policy generation, successor generation and minimum floor; maintain anti-rollback lineage and expiration/retirement semantics appropriate to the claim.

`valid old ceremony signature ≠ current recovery authorization`; `same successor key ≠ same recovery event`.

## SYNTHESIS 10 — bootstrap completion and fleet convergence are separate gates
The successor may be validly established while regions, offline clients and downstream writers still retain old authority. Track successor establishment separately from obsolete-authority extinction and client convergence. Keep assurance debt until stale branches/writers/credentials and offline tails are reconciled or bounded.

`successor authority established ≠ fleet converged`; `primary region current ≠ stale tail extinct`.

## SYNTHESIS 11 — recovery authority needs its own compromise/replacement path
The recovery basis can itself be lost or compromised. It must not be an unexplained final magical root. Governance needs a separately reasoned path for recovery-authority rotation/replacement, including what happens when the required threshold is unavailable or suspected compromised. Exact organizational mechanism is product/personnel design and remains OPEN.

`recovery root exists ≠ recovery root immortal`; `lost recovery threshold ≠ lower threshold automatically`.

## SYNTHESIS 12 — ceremony closure requires extinction of temporary power
After successor authority is established, temporary credentials, reconstructed key material, elevated roles, temporary HSM sessions, emergency policy and recovery-mode endpoints must be retired or returned to dormant state, with negative evidence where feasible. Otherwise the ceremony leaves a new standing bypass.

`ceremony complete ≠ temporary authority extinct`; `successor works ≠ recovery channel safely dormant`.

## MINTTAP DECISION / DIRECTION
1. Separate custody of recovery material from policy authorization to invoke recovery.
2. Treat recovery-key/share independence as a multi-dimensional failure-domain claim, not a count of people or locations.
3. Keep recovery authority dormant and narrower than normal production authority; do not create a standing product-mutation bypass.
4. Require evidence-bearing, version-bound ceremony activation with explicit compromise scope, successor, floor and closure obligations.
5. Select any threshold only after dependency/failure-domain analysis; do not canonize a generic k-of-n number.
6. Authenticate successor distribution through an independent bootstrap lineage; discovery/telemetry/MDM alone is insufficient authority.
7. For long-offline PWA clients, preserve unique data first, bootstrap current successor trust, then re-admit queued consequence individually.
8. Test recovery mechanics without normalizing production emergency authority; preserve negative rejection/fencing evidence.
9. Make recovery artifacts anti-replay and generation-bound.
10. Keep successor establishment, obsolete-authority extinction and fleet convergence as separate closure gates.
11. Define recovery-authority rotation/compromise handling rather than treating the recovery root as permanent magic.
12. Close ceremonies by proving temporary recovery capability is dormant/extinct again.

## Track C destructive campaign — +8 defined cases
593. **Custody monoculture:** three shares are held by three people but all depend on one SSO/admin recovery account; claimed threshold independence must fail.
594. **Standing recovery bypass:** recovery signer can directly mutate ordinary product data outside an incident; capability scoping must reject the path.
595. **Stale ceremony replay:** a previously valid recovery package is replayed after recovery-policy/custodian generation advances; bootstrap must reject it.
596. **Discovery-as-authority:** compromised DNS/MDM/support channel announces attacker successor without independent lineage; client must not trust discovery alone.
597. **Threshold without policy authorization:** enough shares reconstruct/sign but required incident/approval preconditions are absent; recovery must remain unauthorized.
598. **Long-offline iPad misses ceremony:** client returns with unique data and compromised historical root; preserve data, bootstrap successor, reject old remote authority and re-admit queued work.
599. **Temporary-power residue:** successor is live but emergency HSM session/credential/recovery endpoint remains usable; closure must remain OPEN.
600. **Recovery-threshold loss:** required recovery shares are unavailable; system must not silently lower threshold because availability is urgent.

These are **defined destructive cases, not executed PASS evidence**.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate recovery authority, keys, HSMs, custodians, personnel separation, provider/IAM and physical custody: OPEN.
- Actual threshold/approval policy and legal/organizational succession: OPEN.
- Actual successor distribution/bootstrap protocol and anti-replay schema: OPEN.
- Actual managed iPad/iPadOS/WebKit/MDM trust-bootstrap behavior: OPEN.
- Actual ceremony tooling, isolated drill environment and downstream fencing oracles: OPEN.
- Physical-device, AT, representative-human and product runtime evidence: OPEN.
- Aviation/legal obligations affecting custody, offline data and recovery authority: specialist evidence required.

## CHANGE WATCH
- NIST SP 800-57 Part 1 Rev.5 remains current final general key-management guidance; later revisions/drafts must be checked before implementation decisions.
- TUF specification/FAQ are bounded update-system precedents, not MintTap protocol requirements.
- RFC 9943 is current Standards Track transparency precedent; transparency remains evidence rather than recovery authority.
- Browser/iPadOS/MDM behavior is platform/version-sensitive and requires current physical-device evidence.

## Gate judgment
**230 PASS (generic).** We can separate recovery custody from authorization, reason about threshold/failure-domain independence, define a dormant bounded recovery capability and evidence-bearing ceremony, authenticate successor distribution without trusting compromised discovery, and preserve long-offline PWA data while requiring current bootstrap before remote consequence. Product/provider/personnel/device/ceremony/runtime validation remains OPEN.

## Next highest-value adjacent question
**231 — recovery-authority rotation, custodian succession & loss-of-threshold survivability:** determine how dormant recovery authority itself changes over years without creating overlapping standing roots, how personnel departure/incapacity and organizational transfer alter custody, how clients verify a recovery-root rotation they may miss while offline, and what bounded options remain when the intended threshold is permanently lost without silently weakening trust.