# 273 — PWA Recovery-Root Compromise, Emergency-Authority Abuse & Post-Reset Recovery-Root Retirement

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/offline rejoin mechanics; Track B truthful recovery/degraded-state UX; Track C destructive validation; Track D bounded incident/convergence diagnostics.  
Dependencies: 260–272 dependency/topology/re-entry/revocation/rotation/emergency-reset governance.

## Problem

272 established that a compromised R1/R2 lineage cannot manufacture a clean R3 merely by cross-signing or increasing a generation number. The adjacent failure is harder: the contingency/break-glass/rebootstrap authority used to establish R3 is itself suspected compromised, abused, over-scoped, or left permanently powerful after recovery.

Central rule: **a recovery root is not exempt from the trust model. Treat it as a high-consequence authority with its own failure domains, scope, activation evidence, abuse controls, lifecycle and retirement path. If it becomes suspect, preserve data and incident evidence, fence the consequences it can authorize, move to a trust basis outside its compromise set or governed rebootstrap, and do not let successful emergency use turn it into a permanent super-root.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Service Worker, Cache Storage, IndexedDB, install state and reconnect can retain pre-reset state but cannot establish emergency organizational authority.
- **B UX/IA/Content:** high dependency pressure. Recovery UX must distinguish `data preserved`, `authority unavailable`, `revalidation required`, `limited capability`, `recovery succeeded` and `recovery authority retired`; it must not imply that local data is corrupt merely because authority is suspect.
- **C Performance/Accessibility/Quality:** destructive campaign expands **936 → 944 defined cases**. Execution, physical-device, AT and human PASS remain OPEN.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Measures emergency-authority activations, scope use, stale recovery-root sightings, retirement rejection and unknown/offline tail; telemetry cannot authorize emergency access.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns recovery-root compromise scoping, break-glass abuse resistance, successor trust establishment, retirement and anti-resurrection.

## SOURCE

### NIST SP 800-57 Part 1 Rev. 5 — compromise and recovery are lifecycle problems

NIST SP 800-57 Part 1 Rev. 5 provides general key-management guidance. Its recovery guidance distinguishes lost/inaccessible material from material that may have been compromised; when compromise is suspected, replacement should occur as soon as practical after recovery to limit exposure. It also treats protection, backup, archive, recovery and compromise as lifecycle concerns rather than one-time setup.

Source: https://doi.org/10.6028/NIST.SP.800-57pt1r5

**TRANSFER VALIDATION:** this is cryptographic key-management guidance, not a PWA architecture prescription. The reusable principle is that recovery material does not become indefinitely safe merely because it enabled recovery once.

**CHANGE WATCH:** NIST published an Initial Public Draft of SP 800-57 Part 1 Rev. 6 on 2025-12-05. Rev. 5 remains the final publication at this checkpoint; Rev. 6 draft is change-watch evidence, not a replacement final authority.

### RFC 6024 — trust-management authority compromise is explicitly recoverable

RFC 6024 requires trust-anchor management to support recovery from compromise or loss of a trust-anchor private key, including the private key authorized to serve as trust-anchor manager. It also notes that initial/bootstrap management keys may be transported and checked out-of-band.

Source: https://www.rfc-editor.org/rfc/rfc6024

**TRANSFER VALIDATION:** the reusable lesson is recursive: the authority that manages trust is itself part of the compromise model. Do not copy its protocol into MintTap/LogMate.

### RFC 5934 — contingency authority is useful but powerful

TAMP describes an optional contingency private key as a possible recovery mechanism when an apex operational trust-anchor key is compromised, while also documenting severe consequences of compromise of management/apex authority.

Source: https://www.rfc-editor.org/rfc/rfc5934

**TRANSFER VALIDATION:** a contingency mechanism can reduce recovery dependence, but it creates another high-value authority that needs isolation, scope and lifecycle governance.

### RFC 5011 / RFC 6781 — if trusted in-band basis is gone, out-of-band recovery may be necessary

RFC 5011 states that if all trust-anchor keys at a trust point are compromised, manual or other out-of-band update is required. RFC 6781 recommends independently authenticated verification of replacement trust material after trust-anchor compromise and discusses standby keys stored separately from active keys.

Sources:  
https://www.rfc-editor.org/rfc/rfc5011  
https://www.rfc-editor.org/rfc/rfc6781

**TRANSFER VALIDATION:** DNSSEC mechanisms/timers are not product defaults. The bounded principle is that recovery must survive the actual compromise domain; a supposedly separate emergency key in the same failed domain does not.

## SYNTHESIS 1 — recovery root is an authority, not a magical exception

Calling an object `recovery`, `break-glass`, `contingency` or `offline root` does not exempt it from authentication, authorization, provenance, scope, currentness or compromise analysis.

Guards:
- `named recovery root ≠ uncompromised recovery root`;
- `emergency authority ≠ authority without governance`;
- `rarely used ≠ low consequence`.

## SYNTHESIS 2 — compromise scope follows capability, not label

If recovery authority can admit a new revocation source, replace policy roots, reset device trust or authorize publication, compromise impact includes those consequences. A narrowly scoped recovery authority for one domain must not silently become universal administration.

Guards:
- `recovery for scope S ≠ universal super-root`;
- `can reset trust ≠ can rewrite historical provenance`;
- `can admit successor ≠ can erase incident evidence`.

## SYNTHESIS 3 — break-glass activation needs bounded authority evidence

Emergency activation should bind at least the incident/reason, actor/approver basis, affected scope, allowed consequences, start/expiry or review trigger, recovery generation, compensating controls and exit/retirement criteria appropriate to consequence. A permanent hidden bypass is not an emergency mechanism.

Guards:
- `emergency declared ≠ every control bypassed`;
- `break-glass credential accepted ≠ requested consequence authorized`;
- `activation logged ≠ activation justified`.

## SYNTHESIS 4 — recovery-root compromise cannot be repaired by self-certification

If recovery root Q is suspected compromised, a Q-signed statement that Q is clean or that Q2 is its legitimate successor is not sufficient by itself. The successor trust basis must survive the Q compromise model or use governed rebootstrap.

Guards:
- `Q says Q is clean ≠ Q clean`;
- `Q signs Q2 ≠ Q2 independent when Q is compromised`;
- `higher recovery generation ≠ clean recovery basis`.

## SYNTHESIS 5 — independence is a failure-domain property

A recovery key in a separate file but under the same IdP, cloud account, HSM administrators, CI secret store, device-management plane, operator quorum, backup set or recovery workflow may be correlated with the primary failure.

Evaluate credential, signer, storage, administration, identity, provider/control-plane, deployment, reviewer/personnel and restoration dependencies.

Guard: `different key bytes ≠ independent recovery authority`.

## SYNTHESIS 6 — emergency availability may degrade without destroying data

When neither ordinary nor emergency authority is sufficiently trustworthy, high-consequence mutation/publication may need to stop temporarily. Preserve/read/recovery/export capabilities may remain available where they do not recreate the compromised consequence.

Guards:
- `no clean authority ≠ delete local records`;
- `publication fenced ≠ application data invalid`;
- `trust unavailable ≠ provenance unavailable`.

## SYNTHESIS 7 — successful reset creates a retirement obligation

Once R3/current authority is safely established, the emergency authority that enabled it should not remain indefinitely hot merely because it worked. Re-evaluate exposure during incident use, rotate/replace where needed, reduce scope, return it to controlled standby or retire it according to the architecture.

Guards:
- `recovery succeeded once ≠ recovery root safe forever`;
- `incident closed ≠ emergency authority retired`;
- `credential unused after reset ≠ credential unable to authorize`.

## SYNTHESIS 8 — retirement needs negative proof, not inactivity

No observed use of Q after R3 establishment is weak evidence. Material boundaries should reject obsolete Q consequences, and background/admin/manual/recovery paths must be included where applicable. Historical Q verification material may remain for provenance without current authorization.

Guards:
- `zero Q use ≠ Q retired`;
- `Q removed from one secret store ≠ Q rejected everywhere`;
- `historical Q verifier retained ≠ current Q authority retained`.

## SYNTHESIS 9 — do not rotate emergency authority back into the same correlated domain

Post-incident Q2 placement must be informed by the compromise graph. Replacing Q with Q2 in the same failed account, admin plane, HSM policy or backup topology recreates the same recovery weakness.

Guard: `new recovery key ≠ new recovery failure domain`.

## SYNTHESIS 10 — emergency authority should not become the normal control plane

Frequent use of Q because normal authority is inconvenient converts contingency into shadow architecture. Repeated activation is an architecture-review signal, not evidence that Q should be permanently enabled.

Guards:
- `frequent emergency use ≠ normal admission`;
- `operational convenience ≠ recovery justification`;
- `temporary superuser path ≠ preferred steady-state path`.

## SYNTHESIS 11 — human/operator emergency authority is also in scope

A break-glass process may depend on people rather than a single key. Shared accounts, one-person override, unreviewed support tooling or a quorum controlled by one administrative domain can still be correlated. Personnel/process authority needs the same consequence and independence analysis.

Guard: `two human approvals ≠ independent control when both share one compromised admin plane`.

## SYNTHESIS 12 — offline clients must not resurrect retired recovery authority

A long-offline PWA may return with Q-era reset material, cached decisions and queued operations. It may preserve historical evidence but cannot cause central authority to reactivate Q. Rejoin requires current trust/rebootstrap, runtime/schema/session checks and operation-level revalidation.

Guards:
- `offline client remembers Q ≠ Q current`;
- `Q-era queue preserved ≠ Q-era execution authorized`;
- `old recovery object verifies historically ≠ old recovery object admissible now`.

## SYNTHESIS 13 — backup/PITR must not resurrect the emergency super-root

Pre-retirement backups can restore Q credentials, caches or configuration. Restore success must be followed by reconciliation against a current anti-rollback reference outside the restored failure domain or governed rebootstrap.

Guard: `backup restores Q configuration ≠ Q authority restored`.

## SYNTHESIS 14 — runtime delivery and emergency authority remain separate

Service Worker update, MDM, push, API or app-shell delivery can carry Q2/R3 material but cannot establish organizational authority by transport alone.

Guards:
- `worker delivered Q2 ≠ Q2 trusted`;
- `MDM installed reset material ≠ reset authority independently proven`;
- `online after incident ≠ emergency authority normalized`.

## SYNTHESIS 15 — recovery-root health needs periodic challenge without routine activation

A cold recovery mechanism that is never tested may fail when needed; a permanently active one increases attack surface. The governance problem is to validate reachability, custody, authorization logic, independence assumptions and retirement/replacement procedures without turning recovery authority into routine mutation authority.

Guard: `recovery drill PASS ≠ routine recovery authority should remain active`.

## PWA / LogMate-like EFB application case

Scenario: R1/R2 were compromised; emergency root Q admitted R3. Incident review then finds that Q shared the same cloud identity administration plane as the compromised signers, and a six-week-offline company iPad returns with Q-era reset metadata plus unique flight records.

Safe generic sequence:
1. preserve unique local records, queue payloads and provenance before authority cleanup;
2. classify Q as suspect for the consequences reachable through the shared administration plane;
3. fence Q-authorized high-consequence replay/publication at authoritative server boundaries;
4. keep safe local preservation/read/recovery capability where possible;
5. establish Q2/current recovery basis from a trust path outside the Q compromise set, or invoke governed rebootstrap if none survives;
6. bind Q2 scope and activation to the minimum recovery consequences required;
7. reconcile current R3/R4 authority, policy, schema, session/device incarnation and queued operations individually;
8. prove obsolete Q rejection across API, background job, admin/manual and recovery paths that can create material effect;
9. rotate/retire Q and any exposed emergency credentials; preserve historical verification/provenance separately;
10. prevent PITR/offline return from reactivating Q by current anti-rollback/rebootstrap checks;
11. return Q2 to controlled standby or retire/replace it according to architecture rather than leaving it as normal superuser authority.

This is a generic architecture pattern. It is **not** evidence that LogMate currently uses such keys, cloud identity, MDM, direct sync, or any specific aviation-security architecture.

## Cross-track transfer

### Track A — Platform/Browser

**DEPENDENCY:** browser persistence can retain obsolete reset material for long periods. Worker/controller/cache freshness cannot prove current recovery authority. IndexedDB/Cache Storage preservation must remain separable from queued operation authorization.

### Track B — UX/IA/Content

**TRANSFER VALIDATION:** recovery UX should communicate capability truth: local data preserved, remote effects paused, revalidation required, or recovery completed. Avoid copy that equates authority compromise with user-data corruption or implies sync success before acknowledgement/reconciliation.

### Track C — Quality / destructive campaign

Add eight defined cases:
1. **Recovery-root self-clearance** — compromised Q signs `Q healthy`; high consequence must not reopen solely from that statement.
2. **Recovery-root self-successor** — compromised Q alone signs Q2; independence requirement must fail.
3. **Same-plane replacement** — Q2 uses new key bytes but same compromised IdP/admin/HSM failure domain; do not claim independent recovery.
4. **Emergency-authority permanence** — R3 works, Q remains indefinitely able to publish; retirement gate must remain open.
5. **Inactivity-equals-retirement theater** — no Q use observed; direct obsolete-Q negative test still required where material.
6. **Offline-Q resurrection** — long-offline iPad presents valid historical Q reset object; preserve data but reject Q-era authority.
7. **PITR emergency-root resurrection** — backup restores Q configuration after retirement; current anti-rollback/rebootstrap must prevent reactivation.
8. **Worker-delivery authority theater** — Service Worker/MDM successfully delivers Q2; semantic trust must remain unproven without recovery-basis validation.

Campaign total: **944 defined cases**. This is definition coverage, not execution PASS.

### Track D — Discovery/Analytics

**DEPENDENCY:** telemetry may observe emergency activation, stale-Q attempts, Q2 adoption, rejection and unknown fleet tail. It must not elect or legitimize a recovery root. Unknown/offline devices remain uncertainty, not implicit zero risk.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate-like web/PWA requirements:
- model emergency/recovery authority as a first-class high-consequence authority, not an undocumented bypass;
- bind recovery scope to explicit consequences and compromise assumptions;
- evaluate independence by failure domain, not by key count/name/location alone;
- preserve unique offline data independently of authority validity;
- require post-reset retirement/rotation and negative rejection proof for obsolete emergency authority;
- do not allow restore/offline return to resurrect retired recovery authority;
- treat repeated emergency use as architecture-review evidence;
- keep actual product thresholds, authority topology, MDM/provider choices and aviation/legal requirements OPEN until canonical runtime/project evidence exists.

## OPEN

Production validation remains OPEN for:
- whether MintTap or LogMate has any recovery root, break-glass credential, offline trust anchor or emergency admin path;
- actual signer/key/HSM/IdP/cloud/MDM/operator failure domains;
- exact consequence classes and degraded-mode policy;
- managed-iPad/WebKit storage/update/rejoin behavior;
- session/device/principal identity and queued-operation semantics;
- backup/PITR topology and anti-rollback reference;
- physical-device, accessibility, security/privacy, human, legal and aviation validation.

## External specialist boundary

Design Studio Web remains Stage 3 PRACTICE / NOT PASSED at W121; physical-device/PWA, screen-reader and representative-human UX evidence remain OPEN. Software Engineering Studio remains FOUNDATION STUDY UNDERWAY; M006 provides bounded Safari Service Worker lifecycle transfer only, with installed PWA, fresh-origin-down Safari cold start, physical iOS/iPadOS and canonical-product runtime still OPEN. No external gate is promoted by this study.

## CHANGE WATCH

- NIST SP 800-57 Part 1 Rev. 6 is an Initial Public Draft dated 2025-12-05; re-check when finalized.
- Apple/WebKit/iOS/iPadOS PWA and managed-device behavior remains platform/version/enrollment specific.
- Browser runtime changes do not alter the semantic separation between data preservation, transport and organizational authority.

## Gate assessment

**PASS (generic).** The Web Manager can now reason about recovery-root compromise, emergency-authority abuse, failure-domain independence, data-preserving degradation, successor recovery, post-reset retirement, offline/PITR anti-resurrection and cross-track validation without promoting unknown product facts.

## Next highest-value adjacent target

**274 — recovery-authority custody succession, quorum loss & organizational continuity after personnel/provider loss.** Determine how a safely isolated emergency authority remains usable when custodians leave, provider/HSM/IdP access is lost, quorum members become unavailable, or organizational control changes—without weakening recovery into shared permanent credentials or creating an unrecoverable cold root.