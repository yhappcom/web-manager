# 206 — PWA Witness-Policy Reconstitution Anchoring, Client Bootstrap & Anti-Downgrade Recovery Packages

Status: **PASS (generic) / PRODUCT + RECOVERY-ANCHOR + WITNESS + CLIENT-BOOTSTRAP + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/runtime state; Track B recovery/rebootstrap semantics; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–205, especially 188–205.

## Problem

205 established ordinary witness-policy succession: membership and threshold are versioned authority policy, and a successor cannot self-appoint. The hard boundary is total or threshold-level witness loss/compromise where ordinary predecessor quorum is no longer trustworthy. At that point a system still needs a way to establish a successor without converting any network-delivered `root.json`, restored snapshot, support instruction or cached PWA state into an implicit trust reset.

Central rule: **reconstitution is a change of trust anchor, not a special case of ordinary update. When predecessor quorum is no longer trustworthy, continuity cannot be invented; the new trust basis must be authenticated through a separately governed recovery anchor/channel and clients must preserve that the transition was exceptional.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Browser secure context/TLS, Service Worker, Cache Storage and IndexedDB can transport/cache a recovery package, but cannot make an otherwise untrusted package authoritative.
- **B UX/IA/Content:** high dependency pressure. Owns `RECONSTITUTION REQUIRED`, `BOOTSTRAP REQUIRED`, `RECOVERY PACKAGE STALE/CONFLICT`, `LOCAL-ONLY`, `RE-ADMISSION REQUIRED`, `QUARANTINED`, `UNKNOWN`; recovery must not imply local-data deletion.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **408 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Can observe recovery-package fingerprints/adoption/conflicts; public search, analytics, telemetry popularity and support-page discovery cannot establish a trust anchor.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns recovery-anchor governance, bootstrap package admission, anti-replay/anti-downgrade, scope, extinction and post-reconstitution convergence.

## SOURCE

### TUF — threshold root compromise requires out-of-band re-issuance

TUF's current FAQ states that compromised keys are normally revoked/replaced by Root, but if a threshold of Root keys is compromised, the Root file must be re-issued out of band. TUF security guidance also treats root/threshold compromise as qualitatively stronger than ordinary online-role compromise and emphasizes freshness, rollback resistance, threshold signatures and compartmentalized trust.

Sources:
- https://theupdateframework.io/docs/faq/
- https://theupdateframework.github.io/security.html

**TRANSFER VALIDATION:** when ordinary root/witness continuity is no longer trustworthy, a separately trusted bootstrap path is required. TUF does not prescribe MintTap's recovery channel or client ceremony.

### Sigstore — initial trust root is explicit bootstrap material

Sigstore's current installation guidance initializes a TUF client with an explicitly obtained root file; that root starts the chain from which later roots are downloaded. Sigstore's policy-controller also supports an explicitly configured initial TUF `root.json`, or explicit out-of-band keys/certificates when TUF is not used. Sigstore documents its public trust root as originating in a public root-key signing ceremony.

Sources:
- https://docs.sigstore.dev/cosign/system_config/installation/
- https://docs.sigstore.dev/policy-controller/overview/
- https://docs.sigstore.dev/about/security/

**TRANSFER VALIDATION:** bootstrap trust is not derived merely from the same remote repository whose content is being authenticated. Explicit initial trust material/channel is a useful precedent; no Sigstore mechanism is adopted as MintTap architecture.

### NIST SP 800-57 Part 1 Rev.5 — trust anchors and key lifecycle are explicit security dependencies

NIST SP 800-57 Part 1 Rev.5 is the current final general key-management recommendation and covers trust anchors, key compromise, recovery, cryptoperiods and key-management lifecycle. Rev.6 remains an Initial Public Draft and therefore CHANGE WATCH rather than a final baseline.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r6/ipd

**TRANSFER VALIDATION:** recovery of a high-level trust basis is a key-management/governance problem, not a UI retry. Exact recovery-anchor form remains product/security architecture evidence.

## SYNTHESIS 1 — reconstitution changes the trust basis

Ordinary succession proves continuity from admitted W to W+1. Reconstitution after threshold compromise/loss cannot honestly claim that proof. A generic recovery record therefore distinguishes:
- prior admitted witness policy/floor;
- reason ordinary succession is unavailable/untrustworthy;
- independent recovery authority/anchor used;
- incident/reconstitution identity;
- successor witness policy;
- scope and activation constraints;
- old-policy retirement/extinction requirements;
- evidence gaps/UNKNOWNs.

`reconstitution package valid ≠ predecessor quorum satisfied`.

## SYNTHESIS 2 — recovery anchor must not collapse into the failed witness plane

A recovery anchor/channel is only useful against the modeled failure if it does not share the same decisive compromise path. Independence can involve administration, custody, KMS/HSM/recovery, storage/PITR, deployment, identity/federation, network/distribution and personnel.

A second URL, mirror or cloud account is not automatically independent.

`different endpoint ≠ independent recovery anchor`.

## SYNTHESIS 3 — HTTPS is transport protection, not sufficient trust-reset authorization

A restored/new client may receive a recovery package over HTTPS. That authenticates the TLS endpoint under the Web PKI model; it does not by itself prove that the service's constitutional witness-policy reset was authorized, especially when the incident may include origin/control-plane compromise.

`HTTPS-delivered recovery package ≠ authorized trust reset`.

Exact product bootstrap may deliberately bind Web PKI plus another recovery anchor, but that is an OPEN architecture decision.

## SYNTHESIS 4 — anti-downgrade package needs predecessor context and one-way recovery identity

A reusable recovery package conceptually binds:
- package/reconstitution identity;
- affected product/service and authority scope;
- last-known/retired witness-policy identifiers or an explicit statement that continuity cannot be proven;
- successor witness policy and recovery generation/floor;
- recovery-anchor identity and authorization evidence;
- incident/purpose (`RECONSTITUTION`, not ordinary update);
- issue/admission constraints and any bounded validity;
- client applicability/bootstrap class;
- explicit retirement of superseded recovery package/policy where applicable;
- hashes/identifiers sufficient to prevent mix-and-match of policy, scope and ceremony evidence.

A random nonce alone is not generic replay protection for a client that has never seen the nonce. Non-replayability comes from a durable admitted recovery generation/floor plus package identity/lineage and current recovery policy.

`unique package ID ≠ replay-proof bootstrap`.

## SYNTHESIS 5 — new, restored and long-offline clients have different prior state

Three bootstrap classes must not be conflated:
1. **Existing current-enough client:** possesses a durable admitted floor/anchor and can reject lower recovery generations.
2. **Restored/rollback client:** may possess authentic but stale local trust state; restore/PITR must not erase anti-rollback evidence if an independent surviving floor exists.
3. **New/zero-state client:** has no historical local floor and therefore requires an authentic initial recovery/bootstrap anchor delivered by a trusted distribution/provisioning path. It cannot infer legitimacy from `highest generation`, majority of mirrors, current wall clock or popularity.

`zero local history ≠ permission to trust the newest-looking package`.

## SYNTHESIS 6 — rebootstrap must be one-way at current-authority level

After recovery generation R is admitted, predecessor witness policy W may remain for historical verification but must not regain consequence-bearing remote authority. Generic proof pairs:
- negative oracle: W/revoked recovery package cannot authorize a consequential operation in each scoped enforcement domain;
- positive oracle: successor policy W' can authorize the intended operation;
- regional/currentness convergence evidence;
- restore/PITR replay test;
- offline-client rebootstrap test.

`new policy works ≠ old policy extinct`.

## SYNTHESIS 7 — recovery-package distribution and recovery authorization are separate

CDN, app website, MDM, QR/manual transfer, enterprise configuration, removable media or support workflow may distribute bytes. Distribution availability is not authorization. Conversely, a valid recovery package that cannot reach a client is an availability problem, not evidence that a weaker package may be substituted.

`recovery package reachable ≠ recovery package authorized`; `authorized package unreachable ≠ weaker package authorized`.

Actual company-iPad/MDM provisioning capabilities are OPEN and require platform/product evidence.

## SYNTHESIS 8 — package freshness cannot rely only on client wall clock

A recovery package may contain time bounds, but long-offline/restored clients can have uncertain time. Existing clients should prefer durable recovery generation/floor and authenticated lineage/currentness evidence; time is supplementary according to the admitted policy. Zero-state bootstrap requires a trusted initial anchor/provisioning ceremony and cannot manufacture freshness from local time.

`package unexpired by device clock ≠ package current`.

## SYNTHESIS 9 — conflicting recovery packages are incident evidence

If two independently valid-looking reconstitution packages install different successors and neither can be ordered under an admitted recovery lineage, do not choose by generation, issue time, mirror count, region majority or telemetry adoption. Quarantine consequence-bearing admission and preserve both packages/evidence.

`two recovery-anchor-valid packages ≠ choose the numerically newer one`.

## SYNTHESIS 10 — LogMate/EFB long-offline recovery preserves data before authority

For a company iPad that missed total witness loss and reconstitution:
1. preserve unique local flight/logbook records and provenance;
2. isolate cached session/witness/recovery state from remote authority;
3. determine bootstrap class and obtain an authorized current recovery package/anchor;
4. admit current recovery generation/witness policy without claiming missed ordinary continuity;
5. reject retired W and stale recovery packages for current remote authority;
6. re-evaluate session/token/queue under current policy;
7. upload/reconcile consequence-bearing work only after current re-admission;
8. retain historical UNKNOWN where prior authorization/timing cannot be reconstructed.

PWA local data survival and remote authorization remain separate.

## SYNTHESIS 11 — bootstrap pinning has lifecycle and replacement cost

A built-in or enterprise-provisioned recovery anchor improves resistance to network trust reset only if its replacement/compromise lifecycle is governed. An immutable anchor with no survivable replacement path can turn compromise or organizational loss into permanent lockout; an easily replaceable anchor can become the reset vulnerability.

`pinned anchor ≠ complete recovery design`.

Exact root-of-trust hierarchy is OPEN and requires security architecture/Software Engineering validation.

## SYNTHESIS 12 — reconstitution evidence must survive the incident it proves

Recovery package, ceremony authorization, retired-policy identity, successor admission and extinction evidence must not exist only inside the same failed control plane. This consumes 188–197 evidence-survivability/custody findings rather than creating a second evidence primer.

## Track C destructive campaign — 408 cases total

Add eight cases to the 400-case campaign:
1. attacker serves self-signed/newer recovery package over valid HTTPS after origin compromise — transport authenticity cannot authorize trust reset;
2. threshold-compromised W signs its own successor and labels it reconstitution — failed predecessor cannot become the sole recovery anchor;
3. restored client receives authentic stale recovery package R-1 after R was admitted — reject rollback despite valid signature;
4. zero-state client receives two valid-looking packages from mirrors with generations 8 and 999 — no numeric election; bootstrap anchor/lineage required;
5. valid current recovery package is unavailable while stale package is reachable — availability failure does not authorize downgrade;
6. current W' works after rebootstrap but retired W still authorizes in one region — recovery not converged;
7. PITR restores W plus stale recovery package after W' admission — independent floor/recovery generation prevents resurrection;
8. long-offline iPad returns with unique data and W after total reconstitution — data preserved, authorized current package bootstraps W', retired authority rejected, queue re-admitted without rewriting missed history.

Campaign status: **DEFINED, NOT EXECUTED**. Exact anchors, keys, MDM/provisioning, region topology, WebKit/iPadOS behavior, AT/human and product execution remain OPEN.

## Cross-track transfer / contradiction checks

### A → E
Secure-context/TLS/browser storage mechanics transport and persist bootstrap material but do not establish constitutional recovery authority. Exact WebKit persistence, restore and MDM behavior remain implementation evidence.

### E → B
Recovery UX must distinguish local-data safety from remote-authority quarantine. `BOOTSTRAP REQUIRED` must not be phrased as account/data loss, and user-facing recovery instructions cannot silently turn support content into an authority channel.

### E → C
C receives trust-reset, stale-package, zero-state, origin-compromise, PITR, regional-extinction and long-offline-client cases.

### E → D
D may observe package fingerprints/adoption/conflicts. Search ranking, analytics majority and telemetry adoption cannot select a recovery package.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human evidence remain OPEN. This study defines recovery-state semantics and assurance boundaries, not visual treatment.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage with no specialist Foundation PASS. Exact recovery-package serialization/signatures, secure anchor storage, MDM/provisioning, regional enforcement, restore/PITR and WebKit/iPadOS rebootstrap require implementation/runtime evidence.

## MINTTAP DECISION / DIRECTION

1. Treat total/threshold witness failure as explicit trust-anchor reconstitution, never as ordinary witness update.
2. Do not let the failed witness plane, HTTPS origin, mirror majority, highest generation, client wall clock or telemetry popularity independently authorize a trust reset.
3. Bind recovery packages to explicit reconstitution identity, scope, successor policy and durable recovery generation/floor; preserve exceptional provenance.
4. Separate package distribution from package authorization and availability from authority.
5. Define bootstrap classes for current, restored/rollback and new/zero-state clients; zero-state trust requires an authentic initial anchor/provisioning path.
6. Require post-rebootstrap negative proof for retired policy plus positive proof for successor policy; current functionality alone is not extinction proof.
7. Preserve unique offline PWA data before changing trust state, then re-admit consequence-bearing queues under current authority.
8. Keep actual recovery-anchor hierarchy, package format, cryptography, MDM/provisioning and product topology OPEN until canonical implementation/runtime evidence exists.

## OPEN / VALIDATION

- actual MintTap/LogMate recovery anchor(s), custody, independence and compromise model;
- actual bootstrap distribution/provisioning channel for new/restored/company-iPad clients;
- exact recovery-package serialization, signature, generation/floor and validity rules;
- actual witness/recovery policy storage and anti-rollback behavior across reinstall/restore/PITR;
- actual regional enforcement and old-policy extinction;
- actual MDM/company-iPad provisioning capabilities;
- WebKit/iPadOS storage/update/background/restart behavior;
- physical-device, managed-EFB, AT, human, security/privacy, safety/legal/aviation validation.

## CHANGE WATCH

- NIST SP 800-57 Part 1 Rev.6 remains Initial Public Draft; Rev.5 remains the final baseline for this study.
- TUF/Sigstore bootstrap/recovery guidance and client conformance evolve; re-check before implementation prescription.

## VALIDATION / GATE

**PASS (generic).** The Web Manager can now distinguish ordinary witness succession from exceptional trust-anchor reconstitution; define bootstrap classes without trusting newest-looking network state; separate recovery distribution from authorization; preserve anti-downgrade state across restore/offline scenarios; and require paired successor-positive/retired-negative proof after rebootstrap. Product/runtime validation remains OPEN.

## Next highest-value adjacent question

**207 — recovery-anchor succession, bootstrap-channel compromise & zero-state client provisioning after anchor rotation.** Determine how the recovery anchor itself is rotated/reconstituted without creating an infinite trust regress; how a compromised MDM/WebPKI/support/distribution channel is separated from recovery authorization; how factory/new/erased clients obtain a current anchor after rotation; and how old bootstrap media/configuration is retired without making offline operational data unrecoverable.