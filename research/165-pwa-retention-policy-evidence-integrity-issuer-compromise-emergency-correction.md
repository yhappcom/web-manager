# 165 — PWA Retention-Policy Evidence Integrity, Issuer Compromise & Emergency Correction

Status: **PASS (generic) / PRODUCT + LEGAL + IDENTITY/KEY + PROVIDER + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 099 trust-policy anti-rollback; 138+ compromise recovery lineage; 160–161 evidence/verifier/key compromise; 164 deletion/hold policy convergence; Track A offline/SW trust; Track B incident/review UX; Track C destructive compromise testing.

## Why this study exists

164 assumes policy inputs can be authenticated and checked for currentness. That assumption fails if the policy issuer, signing credential, administrative identity, policy repository or deployment path is compromised, or if an authorized operator publishes a catastrophically over-broad rule by mistake.

Central rule:

> **A policy artifact can be authentic yet unsafe, and a compromised predecessor authority cannot authorize its own successor. Emergency correction must reduce harmful authority monotonically, preserve evidence, establish successor trust from an independent surviving basis, and force clients to revalidate before consequence-bearing deletion, retention release or republish.**

## Five-track balance

- **A Platform/Browser:** cached SW/policy can be stale or attacker-influenced; browser state cannot establish successor policy trust.
- **B UX/IA:** owns honest `policy unavailable/revalidation required/restricted pending review` states without exposing sensitive incident detail.
- **C Quality:** owns forged/stale/over-broad policy, issuer compromise, split-view, rollback, offline reconnect and recovery tests.
- **D Search/Analytics:** derived systems consume corrected disposition and must not continue processing merely because an old policy was once valid.
- **E Architecture/Security/Operations:** owns issuer authority, compromise windows, emergency suspension, successor establishment, anti-rollback and correction provenance.

E remains the bottleneck. This study reuses prior crypto/evidence findings instead of writing another key-management primer.

## SOURCE / transfer

NIST defines emergency revocation as revocation of keying material in response to actual or suspected compromise. NIST SP 800-57 Part 1 Rev.5 defines key revocation as making affected entities aware that a key should be removed from operational use before its cryptoperiod ends. The same body of guidance distinguishes key lifecycle states including compromised and destroyed states and requires compromise-recovery planning. These concepts transfer to policy-signing/verifier credentials: suspected compromise is not ordinary rotation and relying parties need an authenticated way to stop accepting affected authority.

Sources:
- https://csrc.nist.gov/glossary/term/emergency_revocation
- https://csrc.nist.gov/glossary/term/key_revocation
- https://csrc.nist.gov/glossary/term/key_states
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

NIST SP 800-53 Rev.5/Release 5.2.0 provides outcome-oriented security/privacy controls and configuration/change-control concepts, including restricting and auditing changes and reviewing systems for unauthorized changes. The durable transfer is independent authorization/evidence for high-consequence policy change, not a claim that MintTap is required to implement a particular federal control baseline.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**CHANGE WATCH:** SP 800-57 Part 1 Rev.6 remains an Initial Public Draft as of this study; Rev.5 remains the final baseline.

Source:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

## Failure classes must be separated

### Planned rotation
Old issuer/key is healthy but being replaced. Historical verification can remain valid while new policy issuance moves to the successor.

### Suspected compromise
The start of attacker control may be unknown. Artifacts in the uncertainty window cannot be promoted to trustworthy merely because their signatures verify.

### Confirmed compromise
Affected issuer/key/admin authority is no longer trusted for new consequence-bearing policy. Damage assessment determines which historical generations are suspect.

### Authorized mistake
The issuer was legitimate but the rule was semantically wrong or over-broad. Cryptographic authenticity does not make the outcome correct.

### Repository/deployment compromise
The signing authority may be healthy while distribution serves rollback, omission or split views. `signature valid` does not prove currentness or non-equivocation.

Persistent guards:
- `signature valid ≠ policy semantically correct`;
- `issuer authenticated ≠ issuer uncompromised`;
- `authorized change ≠ safe change`;
- `new policy has higher version ≠ successor trust established`;
- `compromised old issuer signs successor ≠ successor independently trusted`;
- `emergency rollback ≠ safe restoration of old authority`;
- `policy revoked ≠ all offline clients learned revocation`;
- `one client sees corrected policy ≠ fleet convergence`;
- `historical policy authentic ≠ historical disposition still current`.

## Policy authority model

A policy/disposition artifact should be verifiable against more than a payload signature. Generic evidence dimensions include:
- policy generation and predecessor/lineage;
- issuer/role and authorization scope;
- rule-set/schema version;
- effective/currentness boundary;
- target data/operation scope;
- trust-anchor/verifier generation;
- revocation/suspension state;
- independent checkpoint or other anti-rollback evidence where risk justifies it;
- change approval/provenance sufficient to distinguish planned from emergency change.

Exact schema remains OPEN.

## Compromise response

### 1. Suspend consequence-bearing use
When a material issuer/policy compromise is suspected, stop accepting affected authority for irreversible or hard-to-recover actions such as destructive deletion, hold release followed by destruction, or stale-data republish. Preserve unique local data.

### 2. Establish a compromise window
Do not equate detection time with compromise start. Classify generations/evidence as trusted-before-boundary, suspect-window, rejected-after-known-compromise, or unverifiable where evidence is insufficient. This reuses 161's long-horizon trust model.

### 3. Recover successor authority independently
A successor cannot derive its legitimacy solely from the compromised predecessor. Recovery needs a surviving trust path: independent organizational recovery authority, pre-established recovery anchor, independently protected control plane or other product-specific mechanism validated outside the compromised domain.

### 4. Issue a new authority/policy floor
The successor generation identifies revoked/suspended predecessor authority and establishes the minimum acceptable current policy generation. Old backups, replicas, SW caches and offline devices cannot lower it.

### 5. Re-evaluate effects
Find destructive actions, hold activations/releases, imports, exports, search/analytics processing and offline admission decisions made under suspect policy. Do not automatically invert them: use 157–159 effect reconciliation/compensation/closure governance.

### 6. Normalize and retire emergency authority
Temporary recovery credentials and emergency paths are retired after successor trust and policy convergence are verified. Recovery capability must not become a permanent superuser.

## Emergency correction is forward-only

A bad policy generation G may have said `DELETE_ELIGIBLE` when the correct disposition should have been `RESTRICTED_HELD`, or the inverse. Restoring G-1 is unsafe because G-1 can be stale in unrelated dimensions.

Prefer a new corrective generation G+1 that:
- names/supersedes the defective generation;
- scopes the correction;
- states the new current disposition under surviving authority;
- preserves the fact that G existed;
- triggers effect reconciliation;
- does not erase evidence of actions already taken.

`rollback bytes ≠ rollback consequences`.

## Mistake vs malicious compromise

A semantic mistake may not require revoking the cryptographic issuer if evidence shows the key/identity remained secure. But the defective policy still needs explicit supersession and impact reconciliation. Conversely, suspected key/admin compromise can require suspension even before a bad semantic rule is identified.

Do not use cryptographic revocation as a substitute for policy-quality governance, and do not use a corrected rule as proof the issuer was never compromised.

## Split-view and omission

An attacker controlling distribution can serve policy G+2 to one client and stale G to another. Therefore:
- currentness must not rely only on locally highest-seen version if a fresh client has no prior floor;
- high-consequence clients need an authenticated current-floor source or equivalent anti-rollback mechanism;
- inconsistent authoritative views are a security signal, not a last-write-wins conflict;
- offline clients cannot prove no newer policy exists.

No blockchain requirement is inferred.

## PWA / long-offline iPad

A long-offline company iPad can hold a perfectly authentic policy signed by a key that was compromised or retired while the device was offline. On reconnect:
1. preserve unique unsynced local flight/user data;
2. obtain current trust/policy floor independently of cached SW and local policy;
3. reject predecessor authority below the floor;
4. quarantine operations created under suspect generations until re-authorized/reconciled;
5. do not let local device time decide whether a signature predates compromise;
6. update local policy/projections only after successor trust is established;
7. keep local data export/recovery possible even if remote mutation remains blocked.

A Service Worker update is not a trust reset. Conversely, an old SW does not retain policy authority merely because it controls the page.

## Restore/PITR

Restore can resurrect both a compromised issuer credential and policy artifacts it signed. Before ordinary traffic:
- recover current trust/revocation/policy floor outside the restored failure domain;
- prevent restored signing credentials from becoming active automatically;
- identify suspect-window policies/effects;
- re-evaluate restored queues/jobs and disposition projections;
- rebuild derived systems after corrected authority is established.

`backup contains valid signing key ≠ key may return to active use`.

## B/D transfer

UX should distinguish operationally meaningful states such as `Policy revalidation required`, `Restricted pending review`, and `Local data preserved; remote changes paused`. Do not claim a legal violation or attacker identity before evidence supports it. Search/analytics must honor the corrected disposition and participate in effect reconciliation without using old policy as an independent authority.

## MINTTAP DECISION — generic governance

1. Treat policy issuer/key/admin compromise as a distinct incident from planned rotation and semantic policy error.
2. Suspend consequence-bearing use of suspect authority; preserve unique local data rather than destructively guessing.
3. Establish successor policy trust from an independent surviving basis; never let a compromised predecessor authorize its own replacement as the sole trust path.
4. Correct policy forward with a new generation; do not restore old bytes as if consequences never happened.
5. Bind policy currentness to an authenticated floor/lineage so backup, replica, SW and offline clients cannot downgrade authority.
6. Reconcile effects executed under suspect/defective policy using existing compensation/closure governance.
7. Keep emergency recovery authority bounded and retire it after normalization.
8. Separate cryptographic authenticity, issuer authorization, currentness and semantic correctness.
9. Preserve minimum incident/policy provenance while minimizing sensitive legal/user payload.
10. Keep actual issuer topology, legal authority and product implementation OPEN.

## VALIDATION — 72-case destructive issuer/policy campaign

1 planned issuer rotation; 2 old historical verification retained; 3 new issuance uses successor; 4 old issuer cannot issue new current policy; 5 suspected admin compromise; 6 suspend destructive policy use; 7 detection time known; 8 compromise start unknown; 9 create suspect window; 10 do not invent exact boundary; 11 confirmed key compromise; 12 emergency revoke; 13 stale verifier misses revocation; 14 current floor rejects; 15 compromised issuer signs successor; 16 reject as sole successor trust; 17 independent recovery anchor establishes successor; 18 new floor advances; 19 forged high generation; 20 signature/issuer check fails; 21 authentic over-broad hold; 22 semantic review detects; 23 corrective G+1 narrows scope; 24 preserve G evidence; 25 authentic erroneous delete policy; 26 destruction not yet executed; 27 correction prevents; 28 destruction already executed; 29 reconcile effect not byte rollback; 30 erroneous hold release; 31 downstream delete queued; 32 re-authorize queue under current policy; 33 split view G/G+2; 34 detect contradiction; 35 no LWW; 36 omission of revocation record; 37 floor/currentness check detects; 38 policy repo PITR rollback; 39 external floor dominates; 40 restored signing credential present; 41 remains inactive; 42 restored old async policy job; 43 reject stale generation; 44 old SW serves policy UI; 45 cannot establish current authority; 46 new SW installed; 47 does not itself prove trust migration; 48 IndexedDB old policy remains; 49 migrate/revalidate; 50 offline iPad created operation under suspect policy; 51 preserve operation/data; 52 quarantine remote mutation; 53 device clock claims pre-compromise; 54 not accepted as temporal proof; 55 unique unsynced flight data exists; 56 preserve/export; 57 policy service unavailable; 58 no irreversible guess; 59 outage prolonged; 60 governed escalation required; 61 emergency credential activated; 62 scope/time bounded; 63 recovery complete; 64 emergency credential revoked; 65 search projection still uses bad policy; 66 rebuild/reconcile; 67 analytics pipeline still processes held data; 68 stop/reconcile; 69 accessible revalidation state specified; 70 human/AT observation OPEN; 71 physical Safari/iPadOS recovery OPEN; 72 actual legal/product issuer topology OPEN.

## OPEN / CHANGE WATCH

OPEN: actual MintTap/LogMate policy issuer/admin/key/trust topology; legal-review authority; KMS/HSM; independent recovery anchor; policy schema; compromise detection; managed-iPad trust refresh; Service Worker integration; effect inventory; provider restore behavior; physical Safari/iPadOS and human/AT evidence.

CHANGE WATCH: NIST SP 800-57 Rev.6 draft progression; browser/WebKit/managed-web-app behavior; provider IAM/KMS/signing/rollback features; any product/legal change affecting policy issuer authority.

## Gate result

**PASS (generic).** Web Manager can now distinguish planned rotation, issuer compromise, semantic policy error and distribution rollback; establish forward-only correction and independent successor-trust requirements; and apply them to restore/offline-PWA scenarios without inventing production facts.

## Next highest-value adjacent target

**PWA policy decision explainability, legal-review provenance minimization & contest/appeal correction**: determine how a user/operator can receive a truthful reason and challenge path without exposing privileged/sensitive legal material, how corrections propagate when an applicability decision changes, and how explanation records avoid becoming permanent personal-data or security-sensitive dossiers.