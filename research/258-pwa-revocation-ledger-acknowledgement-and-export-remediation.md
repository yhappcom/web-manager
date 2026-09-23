# 258 — PWA Revocation-Delivery Ledger Durability, Acknowledgement Forgery Resistance & Export-Remediation Closure

Status: **PASS (generic) / PRODUCT + DOMAIN-AUTHORITY + DATA-MODEL + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A transport/restore mechanics; Track B remediation UX; Track C destructive validation; Track D bounded convergence measurement.  
Dependencies: 074, 117–136, 171–257, especially durable provenance, consumer floors/checkpoints, device incarnation, replay-safe admission and downstream projection revocation.

## Problem
257 established that a canonical correction does not prove downstream convergence. The next failure boundary is evidence about convergence itself. A recipient can claim `applied`; an acknowledgement can be replayed from another projection or incarnation; backup/restore can resurrect stale application state while preserving a newer server-side acknowledgement; and an exported PDF/CSV/report can leave organizational control entirely.

Central rule: **delivery, receipt, verification, semantic application, durable local commit and acknowledgement are different events. Acknowledgement is evidence about a scoped recipient/projection/incarnation state, not self-authenticating truth. External-copy remediation can close an organizational obligation without pretending that every uncontrolled byte was remotely erased.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Owns HTTP response semantics, browser storage/restore, Service Worker delivery/retry and platform backup facts. A network success cannot prove semantic application.
- **B UX/IA/Content:** high dependency pressure. Owns truthful `pending`, `received`, `applied`, `needs review`, `outside control`, `replacement issued` and `closure with residual copy risk` states. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **816 → 824 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded consumer. Measures ledger state, age and recipient class without becoming the authoritative acknowledgement store or collecting dispute payload unnecessarily.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns ledger integrity, acknowledgement binding, anti-replay, restore/reincarnation reconciliation, export-remediation state and closure evidence.

## SOURCE

### RFC 9110 — 202 Accepted is explicitly noncommittal
RFC 9110 states that `202 Accepted` means processing has been accepted but not completed and might never be acted upon. HTTP does not later resend a final status code for the asynchronous operation; a 202 representation should point to status monitoring where appropriate.

Source: https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted

**TRANSFER VALIDATION:** strong protocol precedent for separating transport/request acceptance from later semantic completion. It does not define product acknowledgement semantics.

### NIST SP 800-53 Release 5.2.0 — audit evidence needs protection
AU-9 requires protection of audit information and logging tools against unauthorized access, modification and deletion, with alerting on detected unauthorized change. Its enhancements include separate repositories, cryptographic integrity protection and constrained privileged access.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** strong bounded precedent for treating a consequence-bearing acknowledgement ledger as protected evidence rather than ordinary mutable analytics. It does not require a specific LogMate storage architecture.

### Apple Platform Deployment — backup/restore can restore app data without restoring the same management authority
Apple's current managed-device documentation says backups can contain managed app data; restore behavior depends on enrollment and management settings. For account-driven enrollment, restoring a backup does not restore the device-management enrollment profile. On other managed paths, restored app data and management/enrollment can also follow distinct rules. Apple additionally documents that restoring to another device can remove the old management configuration and then trigger fresh enrollment where applicable.

Sources:
- https://support.apple.com/guide/deployment/back-up-managed-apple-devices-depd44f04xc3/1/web/1.0
- https://support.apple.com/guide/deployment/restore-managed-apple-devices-depd44f04xc4/1/web/1.0

**CHANGE WATCH / TRANSFER VALIDATION:** current Apple deployment behavior is OS/enrollment/version specific. It supports the generic distinction `restored app data ≠ restored authority/incarnation` and makes backup/restore an explicit acknowledgement-ledger test case.

### Apple Return to Service — erase/re-enrollment is a lifecycle transition
Current Apple deployment documentation describes Return to Service as erasing prior user data and re-enrolling/reconfiguring the device; current versions can preserve managed app binaries while still erasing locally stored user-generated app data.

Source: https://support.apple.com/guide/deployment/dep17cb455a0/web

**TRANSFER VALIDATION:** bounded managed-device precedent for distinguishing physical hardware from administrative incarnation and local application state.

## SYNTHESIS 1 — use a revocation-delivery ledger, not one boolean
A useful generic ledger separates at least:
- `revocation_id` and subject projection/version;
- successor/minimum acceptable projection generation;
- recipient identity/class;
- recipient administrative incarnation where known;
- dispatch attempt(s) and transport channel;
- receipt evidence where available;
- authenticated current-state verification event;
- semantic application result;
- durable local commit/checkpoint result;
- acknowledgement evidence;
- acknowledgement verifier/policy generation;
- supersession/revocation of the acknowledgement itself;
- unresolved/remediation state.

Do not collapse these into `revoked=true` or `ack=true`.

Guards: `sent ≠ received`; `received ≠ verified`; `verified ≠ applied`; `applied in memory ≠ durably committed`; `acknowledged ≠ forever current`.

## SYNTHESIS 2 — acknowledgement must be consequence- and projection-scoped
An acknowledgement should identify what was actually applied. At minimum its evidence model needs enough binding to distinguish:
- recipient/installation/incarnation;
- logical subject;
- revoked predecessor projection;
- successor/current projection or floor;
- consequence scope;
- application/checkpoint generation;
- acknowledgement time/evidence context;
- current verifier/policy generation.

An `ACK` for P10 must not close P12 remediation. An ACK from old incarnation I4 must not automatically close successor I5. A display-only acknowledgement must not close an export-blocking consequence.

Guards: `recipient ACK ≠ all projections current`; `ACK for predecessor ≠ ACK for successor`; `ACK from old incarnation ≠ ACK from current incarnation`; `display current ≠ export current`.

## SYNTHESIS 3 — self-report alone is weak evidence
A compromised or stale client can say `I applied P12`. Treat a self-report as one evidence item, not the semantic fact itself. Stronger patterns can combine:
1. authenticated recipient/incarnation context;
2. server-issued revocation/projection challenge or stable subject identity;
3. current-state fetch/verification;
4. local atomic application plus durable checkpoint/floor update;
5. acknowledgement bound to that state;
6. server-side anti-replay/consumed-state checks;
7. later negative tests showing P8/P10 cannot be republished at the relevant boundary.

No generic requirement here mandates signatures on every ACK. The control strength should match consequence and actual architecture.

Guard: `client says current ≠ current proven`.

## SYNTHESIS 4 — acknowledgement forgery includes replay and context substitution
Forgery is broader than inventing bytes. Failure classes include:
- replaying an authentic old ACK for a newer projection;
- moving an ACK between recipients/incarnations;
- changing consequence scope around an otherwise authentic ACK;
- accepting an ACK after its verifier/authority generation is retired;
- copying server-side `acknowledged=true` during restore without restoring/re-establishing corresponding client state;
- manufacturing ACK from transport success (`200`, `204`, push delivery, queue dequeue).

Guards: `authentic ACK ≠ applicable ACK`; `transport success ≠ application ACK`; `ledger row copied ≠ state re-established`.

## SYNTHESIS 5 — 202/queue acceptance is not remediation completion
A revocation endpoint may validly return 202 while work remains pending. Even 200/204 only proves the semantics of that HTTP request as defined by the endpoint; it does not generically prove every downstream recipient durably applied a correction.

For asynchronous processing, track accepted/processing/applied/failed/unknown separately and expose a status/reconciliation path where consequence requires it.

Guard: `202 accepted ≠ remediation complete`; `job completed ≠ recipient applied`.

## SYNTHESIS 6 — the authoritative ledger must survive ordinary application restore semantics
If acknowledgement state is security/assurance evidence, do not assume browser IndexedDB, Cache Storage, app local state or ordinary device backup is its only durable copy. Client-local state can be evicted, restored from an older backup or moved across device incarnations.

Generic direction:
- keep canonical server/organizational remediation evidence in a protected failure domain appropriate to consequence;
- keep client checkpoint/floor sufficient to reject predecessor replay;
- on restore/reinstall/reincarnation, reconcile both sides instead of trusting either side alone;
- preserve contradiction if server says `ACK P12` but restored client presents P8.

Guard: `server ACK exists ≠ restored client state matches`; `client checkpoint exists ≠ canonical ledger intact`.

## SYNTHESIS 7 — contradiction is evidence, not permission to overwrite
Example: server ledger says incarnation I4 acknowledged P12 yesterday. A backup restore today presents P8 on physical device H1. Do not silently rewrite the ledger to P8 and do not silently trust the old ACK for the restored runtime.

Record the contradiction, identify current incarnation/authority, preserve unique local data, require current bootstrap, reconcile projection lineage and re-establish a current acknowledgement after durable application.

Guard: `same hardware + prior ACK ≠ restored runtime current`.

## SYNTHESIS 8 — device reincarnation terminates acknowledgement inheritance by default
A new enrollment/incarnation can inherit physical hardware and perhaps recovered data, but consequence-bearing acknowledgement should not transfer automatically. The successor may need to prove current projection/application again.

Historical ACK remains useful provenance: `I4 applied P12 at t`. It does not become `I5 has applied P12` merely because I5 runs on the same serial-number iPad.

Guard: `historical ACK retained ≠ successor ACK inherited`.

## SYNTHESIS 9 — external exports create remediation obligations, not remote-control powers
Once a PDF, CSV, printed report, email attachment, screenshot or third-party import leaves the controlled system, there may be no technical channel to delete or mutate every copy. A truthful remediation model separates:
- controlled copy revoked/replaced;
- recipient identified/unknown;
- correction/replacement notice sent;
- recipient acknowledgement received where possible;
- downstream system replacement confirmed where possible;
- external copy outside technical control;
- legal/organizational follow-up required;
- residual risk accepted by authorized role;
- closure basis and date.

Guard: `export remediated ≠ every external byte erased`.

## SYNTHESIS 10 — closure is obligation-scoped
Remediation closure should answer: **what obligation is closed?** Possible scopes differ:
- prevent future in-product publication of P8;
- bring managed active devices to P12;
- notify known report recipients;
- replace a controlled downloadable report;
- record that an uncontrolled historical copy cannot be recalled;
- satisfy a domain/legal process defined elsewhere.

A closed managed-fleet obligation does not imply external-recipient closure. Conversely, inability to erase an uncontrolled copy does not necessarily mean the internal remediation workflow can never close; it may close with documented residual state if the applicable authority permits.

Guard: `workflow closed ≠ world state erased`; `residual external copy ≠ silently ignored`.

## SYNTHESIS 11 — recipient retirement is not acknowledgement
If a device/recipient is legitimately retired, its active convergence obligation can transition according to policy, but retirement evidence is not retroactive proof that it applied the revocation. Preserve state such as `RETIRED-WITHOUT-ACK` rather than converting it to `CURRENT`.

Guard: `recipient retired ≠ revocation applied`.

## SYNTHESIS 12 — acknowledgement evidence has its own retention and privacy boundary
Do not dump full disputed payloads into the ledger. Often the ledger needs stable identifiers, generations, state transitions, timestamps, bounded reason classes and evidence references. Sensitive correction narrative can remain in the appropriate protected domain.

Retention should be consequence-driven and validated against actual legal/aviation/product requirements; those requirements remain OPEN here.

Guard: `auditability ≠ duplicate sensitive payload everywhere`.

## SYNTHESIS 13 — analytics observes the ledger; analytics is not the ledger
Track D may measure:
- time dispatch→receipt;
- receipt→application;
- application→ack;
- stale/offline/unknown counts;
- reincarnation reconciliation;
- export-remediation age/class.

Analytics event loss, sampling, ad blocking or deletion must not change authority state. Product analytics must not elect `ACKNOWLEDGED`.

Guard: `analytics event observed ≠ authoritative acknowledgement`; `no analytics event ≠ not applied`.

## SYNTHESIS 14 — Service Worker and push remain delivery accelerators
A Service Worker can receive/fetch/retry and Web Push can wake/notify supported installations, but neither proves that record-level state was durably changed. Browser lifecycle can terminate work; installed/uninstalled/permission/offline states vary by platform.

The safe generic boundary remains: delivery hint → authenticated current state → monotonic verification → durable domain application → scoped ACK.

Guard: `Service Worker handled event ≠ domain state durably applied`.

## SYNTHESIS 15 — export replacement must preserve provenance
When an exported report is replaced, preserve enough relation to show:
`Export E8 (based on P8) → revoked/superseded → Export E12 (based on P12)`.

Do not overwrite E8's historical issuance record as though it never existed. The actual external file may remain outside control; the system's provenance should still show that E8 is no longer the current approved projection.

Guard: `replacement issued ≠ predecessor never issued`.

## SYNTHESIS 16 — closure needs negative evidence at the consequence boundary
For managed recipients, strong closure includes positive successor evidence and negative predecessor evidence. Examples:
- P12 can be read/exported as allowed;
- P8 cannot be newly published/exported after reconciliation;
- backup restore cannot clear the P12 floor;
- stale ACK cannot close P12;
- new incarnation cannot inherit I4 ACK without revalidation;
- delayed Service Worker/push message cannot roll back current projection.

For uncontrolled exports, negative technical deletion evidence may be impossible; closure must instead accurately record the bounded remediation action and residual control limit.

## MINTTAP DECISION / DIRECTION
For generic PWA/EFB reasoning:
1. maintain a protected, append/provenance-oriented revocation/remediation ledger rather than a mutable boolean;
2. bind ACK evidence to recipient/incarnation, subject, projection/floor, consequence and policy/verifier context;
3. treat client self-report as evidence, not authority;
4. preserve anti-replay state for ACKs across retries and restore;
5. reconcile contradictions between server ledger and restored/local state without destructive overwrite;
6. do not inherit ACK automatically across device reincarnation;
7. separate managed-recipient convergence from external-export remediation;
8. close obligations by explicit scope and retain residual `OUTSIDE-CONTROL` state where appropriate;
9. keep analytics and push/SW transport outside semantic authority;
10. require predecessor-rejection tests where the consequence boundary is under technical control.

These are generic architecture decisions. Actual LogMate/MintTap backend, export/report authority, aviation/legal retention, MDM topology, cryptographic ACK design and runtime transaction boundaries remain OPEN.

## EFB / LogMate-like application case
Assume company iPad incarnation I4 accepted projection P8, went offline, and later server correction produced P12. The organization dispatched revocation V12. Server ledger later contains `I4 ACK P12`. The iPad is then restored from an older backup or re-enrolled as I5; local PWA data presents P8 plus unique unsynced flight records. Separately, a PDF E8 generated from P8 had previously been emailed externally.

Safe generic sequence:
1. preserve unique local records and historical provenance;
2. identify current administrative incarnation; do not infer I5 currentness from I4 ACK;
3. authenticate current bootstrap/policy and obtain current projection floor P12;
4. retain the I4 ACK as historical evidence but mark current-runtime applicability unresolved;
5. reconcile P8→P12 and revalidate queued operations without deleting unique data;
6. durably commit current projection/floor on I5;
7. generate a new scoped acknowledgement for I5 if policy requires;
8. reject replay of I4/P8 acknowledgement or stale delayed revocation messages;
9. mark E8 superseded and issue corrected E12 where required;
10. record known external recipient notification/acknowledgement where available;
11. if E8 cannot be technically recalled, retain `EXTERNAL-COPY-OUTSIDE-CONTROL` rather than false deletion;
12. close only the obligations whose evidence criteria are actually satisfied.

This sequence is architecture guidance, not a claim that current LogMate implements it.

## Track C destructive campaign — +8 defined cases
817. **Transport-success acknowledgement laundering** — 202/200/push delivery converted directly to `APPLIED`. Expected: fail.
818. **Cross-projection ACK replay** — authentic ACK for P10 closes P12. Expected: fail.
819. **Cross-incarnation ACK inheritance** — I4 ACK automatically marks I5 current after restore/re-enrollment. Expected: fail.
820. **Server/client contradiction overwrite** — server ACK P12 + restored P8 silently collapses to one side without reconciliation. Expected: fail.
821. **Analytics-as-authority** — telemetry event marks recipient acknowledged despite missing canonical application evidence. Expected: fail.
822. **External-delete theater** — internal replacement marks emailed/downloaded E8 globally deleted. Expected: fail.
823. **Retirement-as-ACK** — retired unknown device converted from `PENDING` to `CURRENT`. Expected: fail.
824. **Stale ACK after restore** — restored/replayed ACK clears a higher monotonic projection floor or closes a newer revocation. Expected: fail.

**VALIDATION:** these are defined destructive cases only. No execution PASS is claimed.

## Cross-track transfer
- **A → E:** HTTP/browser/SW/backup mechanics define what delivery and restore can prove; E must not overclaim semantic application.
- **E → B:** expose truthful pending/current/outside-control states without destructive reset or false finality.
- **E → C:** test ACK replay, restore contradiction, incarnation transition and export-remediation leakage.
- **E → D:** provide bounded state classes/identifiers; D measures latency/debt but cannot close authority state.

## OPEN
- Actual product recipient registry and identity model.
- Whether a server-side revocation ledger exists and its transaction/retention model.
- Actual acknowledgement protocol, authentication, signatures/MACs, keys or anti-replay mechanism.
- Actual PWA IndexedDB/Cache/Service Worker behavior on physical managed iPadOS.
- Actual backup/restore/re-enrollment policy and whether app data is backed up.
- Actual export/report formats, destinations and recipient control.
- Legal/aviation requirements for correction notice, recall, retention, audit or non-repudiation.
- Actual backend outbox/job/queue semantics and consequence-specific closure thresholds.
- Human/screen-reader UX validation for stale/revoked/remediation states.

## CHANGE WATCH
- Apple managed-device backup/restore and Return to Service behavior by iOS/iPadOS release and enrollment mode.
- WebKit background/push/PWA lifecycle behavior.
- NIST SP 800-53 current release and audit-control revisions.

## Gate assessment
**258 PASS (generic).** The Web Manager can now distinguish revocation dispatch, receipt, application, durable commit and acknowledgement; design acknowledgement anti-replay/context binding; reason about backup/restore and device-incarnation contradictions; and close export remediation without claiming impossible remote deletion. Product/runtime/domain/legal validation remains OPEN.

## Next high-value target
**259 — acknowledgement-key/credential rotation, recipient compromise & ledger-correction governance.** Study how to scope prior ACK evidence when a recipient credential/device is later compromised; rotate acknowledgement authority without blanket historical invalidation; correct a false ledger entry without erasing audit history; and prevent a compromised client or remediation operator from self-clearing its own stale/revoked state.