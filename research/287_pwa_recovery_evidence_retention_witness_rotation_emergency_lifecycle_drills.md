# 287 — PWA Recovery Evidence Retention, Witness Rotation, Emergency-Credential Lifecycle & Normalization Drills

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-26  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B recovery UX; Track C destructive validation; Track D recovery diagnostics.  
Dependencies: 285–286 stale-client rebootstrap, recovery ceremony, durable succession evidence, anti-equivocation and predecessor-consequence closure.

## Problem

286 established that catastrophic recovery needs durable succession evidence, independent witnesses, anti-equivocation, predecessor rejection and emergency-authority retirement. The adjacent problem is temporal: recovery evidence, witnesses, operators and emergency credentials themselves age, rotate, expire or become compromised.

Central rule: **retaining evidence bytes is not the same as retaining the ability to verify them, and restoring a successor is not the same as proving obsolete recovery authority is extinct.**

## Five-track balance

- **A Platform/Browser:** dependency supplier. Service Worker/runtime, Cache Storage and IndexedDB can retain old generations independently; update and cache state are not a single app version.
- **B UX/IA/Content:** consumer. Recovery UX must distinguish local data preserved, trust/runtime stale, revalidation required, remote consequence contained and recovery complete.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1048 → 1056 defined cases**; physical-device/AT/human execution remains OPEN.
- **D Search/Discovery/Analytics:** challenger. May measure observed recovery adoption and contradictions, but silence or majority observation cannot prove dormant-fleet extinction or elect authority.
- **E Architecture/Security/Operations:** bottleneck owner. Owns verifier-retention requirements, witness rotation/independence, emergency capability extinction and normalization drills.

## SOURCE

### NIST SP 800-184 — recovery is planned, tested and improved

NIST SP 800-184 treats recovery as a discipline requiring planning, playbooks, realistic testing and continual improvement. Its playbook checklist includes formal recovery processes, critical resources, dependency maps, responsible personnel and recovery criteria.

Sources:
- https://csrc.nist.gov/pubs/sp/800/184/final
- https://doi.org/10.6028/NIST.SP.800-184

**TRANSFER VALIDATION:** recurring recovery drills should test the complete recovery/normalization path, not merely service availability. Product-specific authority, evidence schema and drill cadence remain OPEN.

### W3C Service Workers — cache generations are author-managed

The current Service Workers Candidate Recommendation Draft states that Cache objects are separate from the HTTP cache, are author-managed, do not update automatically and do not disappear merely because the Service Worker script updates. Authors should version caches and use them only with worker versions that can safely operate on them.

Source:
- https://www.w3.org/TR/service-workers/

**TRANSFER VALIDATION:** worker update, cache migration, verifier/bootstrap migration and application-data migration are distinct states.

### WebKit storage policy — standalone does not imply durable backup

WebKit documents origin and overall quotas, eviction under storage pressure, and best-effort versus persistent storage. A standalone Home Screen Web App receives the same origin/overall quota as the browser context. Persistent mode changes eviction treatment; it is not a backup/restore guarantee.

Source:
- https://webkit.org/blog/14403/updates-to-storage-policy/

**CHANGE WATCH:** iOS/iPadOS/WebKit storage policy and heuristics can change.

### Safari 26 — installability semantics differ from Chromium assumptions

WebKit documents that on iOS 26 and iPadOS 26 any site may be added to the Home Screen and opened as a web app; a manifest or Service Worker is not an installability prerequisite, though both can enhance the experience.

Source:
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

**CHANGE WATCH:** platform-specific install and Home Screen behavior must be verified against target OS/WebKit versions.

## SYNTHESIS 1 — evidence retention includes verifier context

Long-lived recovery evidence may become unusable if future verifiers lack the material and semantics required to interpret it. Retention planning therefore considers, as applicable to the chosen design:
1. original evidence bytes;
2. public verification material and lineage binding;
3. algorithm/canonicalization identifiers and semantics;
4. key/certificate/witness status needed to interpret historical evidence;
5. policy/version meaning and recovery-event context.

Exact cryptography, schema and retention horizon remain product-specific and OPEN.

Guards:
- `evidence bytes retained ≠ evidence still verifiable`;
- `archive exists ≠ future verifier can interpret it`.

## SYNTHESIS 2 — historical verification and current authority are separate

A retired witness/key may remain necessary to verify legitimate historical evidence without retaining authority to approve new recovery events.

Guards:
- `historical verifier retained ≠ current signer authorized`;
- `historical verification needed ≠ retain historical private signing authority`.

The system should make retirement direction explicit: historical verification support must not silently become a current authorization path.

## SYNTHESIS 3 — witness rotation has two obligations

Planned witness rotation must establish the successor and remove the predecessor's ability to create new current recovery authority. A temporary overlap may be necessary for continuity, but indefinite dual-current authority defeats retirement.

Guards:
- `new witness active ≠ old witness powerless`;
- `rotation completed operationally ≠ predecessor authority extinct`.

## SYNTHESIS 4 — witness independence can decay

Independence is not permanently established at ceremony time. Separate witnesses can later converge onto the same IdP/account-recovery path, administrator, HSM/provider control plane, backup path or organizational operator.

Therefore recurring drills/reviews should reassess failure-domain independence, not merely count keys or approvals.

Guard: `historically independent quorum ≠ currently independent quorum`.

## SYNTHESIS 5 — emergency credentials are capability debt

Expiry timestamps and secret deletion are necessary controls but are not complete extinction evidence. Derived sessions/tokens, workers, compatibility bridges, admin/recovery endpoints, replicas and restored backups may preserve material capability.

Guards:
- `credential expired ≠ authority extinct`;
- `secret deleted ≠ derived authority extinct`;
- `primary endpoint rejects ≠ authority extinct everywhere`.

Closure needs representative negative evidence at every material consequence boundary.

## SYNTHESIS 6 — recovery drills must include normalization

A complete generic drill exercises:
1. preserve unique data/evidence;
2. establish legitimate recovery/successor bootstrap;
3. restore runtime/admission;
4. re-verify retained historical evidence;
5. test predecessor/emergency rejection;
6. retire temporary and derived authority;
7. rejoin dormant clients;
8. reconcile ambiguous queued/prior effects;
9. observe normalization and contradiction signals.

Guard: `success-path recovery drill ≠ normalization drill`.

## SYNTHESIS 7 — drills can create new bypass debt

Temporary credentials, alternate endpoints, manual exceptions, compatibility bridges and emergency operator access introduced for a drill can outlive the drill.

The drill therefore records and retires every temporary capability it creates. Closure requires negative testing after retirement.

Guard: `drill ended ≠ drill-created authority retired`.

## SYNTHESIS 8 — long-offline PWA is a mandatory recovery actor

An EFB-like iPad can return with:
- old Service Worker/runtime;
- old Cache Storage/bootstrap/session/policy;
- unique local records;
- queued intents;
- historical evidence.

The drill is incomplete if it validates only the online fleet. Rejoin preserves unique user data before destructive trust/runtime repair and treats cached authority as potentially stale.

Guards:
- `online fleet normalized ≠ dormant fleet path validated`;
- `stale trust state ≠ stale user data`;
- `IndexedDB/Cache deletion ≠ organizational revocation proof`.

## SYNTHESIS 9 — PWA state is multidimensional

Service Worker generation, controlling worker, cache generation, data schema, verifier/bootstrap generation, session/admission generation and policy generation can diverge.

Therefore:
- `worker current ≠ cache current`;
- `worker current ≠ verifier current`;
- `worker current ≠ schema current`;
- `Home Screen installed ≠ current organizational admission`.

## SYNTHESIS 10 — persistent storage is not backup

WebKit persistent storage can reduce eviction risk, but it does not establish backup integrity, restore correctness, cross-device recovery or organizational durability.

Guard: `persistent storage granted ≠ backup verified`.

For an EFB-like product, unique local operational records require an explicit durability/recovery design whose actual implementation remains OPEN.

## SYNTHESIS 11 — telemetry cannot prove dormant absence

Track D can observe last-seen generations, recovery adoption, predecessor attempts/rejections and contradictions among observed clients. It cannot prove that a powered-off or long-offline device does not exist.

Guards:
- `zero observed stale clients ≠ zero stale clients exist`;
- `traffic silence ≠ predecessor authority extinct`.

Material-boundary rejection is stronger retirement evidence than client census alone.

## SYNTHESIS 12 — platform-specific install behavior is not recovery authority

Safari 26's Home Screen behavior broadens what users can open as a web app, but installability says nothing about current verifier lineage, storage durability, unattended background execution, sync authority or recovery completeness.

Guard: `installable/installed ≠ durable ≠ current ≠ authorized`.

## MINTTAP DECISION / DIRECTION

1. Treat recovery evidence retention as a verifier-lifecycle problem, not a byte-retention problem.
2. Separate historical verification capability from current signing/recovery authority.
3. Rotate witnesses with explicit predecessor retirement and periodically reassess failure-domain independence.
4. Treat emergency credentials and drill-created exceptions as capability debt requiring extinction evidence.
5. Require normalization drills to include dormant-client rejoin and negative predecessor/emergency testing.
6. Preserve unique offline PWA data before destructive runtime/trust repair.
7. Model worker/cache/schema/verifier/session/policy generations separately.
8. Do not treat WebKit persistent storage, Home Screen installation or telemetry silence as backup/currentness/retirement proof.
9. Keep actual MintTap/LogMate authority, storage, MDM, sync, retention and recovery implementation OPEN until verified.

## DEPENDENCY / TRANSFER

- **A → E/C:** Service Worker/cache/storage mechanics explain how stale generations survive independently; they do not establish organizational authority.
- **E → B:** recovery and normalization states become task-truth requirements; Design Studio owns reusable interaction treatment.
- **E → C:** C receives witness-rotation, emergency-extinction, dormant-rejoin and evidence-verifiability invariants.
- **E → D:** D measures observed convergence/contradiction while acknowledging dormant-fleet epistemic limits.
- **Software Engineering:** implementation of evidence schema, verifier preservation, migration, fault injection, credential/session invalidation and recovery harnesses remains engineering evidence.
- **Marketing:** latest owned-web/Store routing work does not change this security gate; avoid duplicating acquisition discipline.
- **Design Studio:** latest canonical evidence remains portfolio work and provides no physical-iPad/PWA/AT/human validation that promotes this gate.

## Track C destructive additions — defined, not executed

1049. **Verifier-context loss:** retained recovery bytes cannot be verified after required historical context disappears.  
1050. **Dual-current witness rotation:** successor is activated but predecessor can still approve new current recovery events.  
1051. **Independence-decay blindness:** nominally separate witnesses now share a recovery/control failure domain but are still counted as independent.  
1052. **Emergency-expiry theater:** expired credential still has a live derived session/token or alternate material path.  
1053. **Secret-deletion theater:** original secret is deleted while worker/admin/compatibility/replica authority survives.  
1054. **Success-only drill:** successor path passes but predecessor/emergency negative tests and normalization are omitted.  
1055. **Drill-created bypass debt:** temporary recovery exception remains materially capable after the drill.  
1056. **Dormant-PWA omission:** online fleet normalizes while a long-offline client later returns with unique data and stale trust/runtime state.

Execution, physical-device, AT and representative-human PASS are not claimed.

## OPEN

Actual MintTap/LogMate recovery authority topology, witness/quorum model, cryptographic algorithms/keys/certificates, verifier-retention schema, retention horizon, emergency credentials, auth/session/token derivation, providers, backups/PITR, Service Worker/cache/schema generations, IndexedDB durability, sync/queue semantics, managed-iPad/MDM/ADE configuration, legal/aviation/safety obligations and human/accessibility behavior remain OPEN.

## CHANGE WATCH

- W3C Service Worker lifecycle/update algorithms and active Candidate Recommendation Draft changes.
- iOS/iPadOS/WebKit Home Screen, storage, eviction, background and managed-device behavior.
- Recovery/cryptographic standards and platform/provider recovery controls.

## VALIDATION

Generic gate passes because the model now distinguishes evidence retention from future verifiability, historical verification from current authority, witness rotation from predecessor extinction, credential expiry from capability extinction, success-path restoration from normalization, and online recovery from dormant-PWA recovery.

Production validation remains OPEN until real backend/runtime/managed-iPad/storage/AT/human evidence exists.

## Next high-value target

**288 — executable PWA recovery test harness, fault-injection taxonomy & evidence-capture schema.** Convert the generic recovery/normalization model into repeatable browser/backend/device experiments, define what evidence each test must capture, and specify which physical-iPad observations are required before any product claim can move beyond OPEN.
