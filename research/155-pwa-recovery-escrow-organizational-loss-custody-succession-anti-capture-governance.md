# 155 — PWA Recovery-Escrow Organizational-Loss Survivability, Custody Succession & Anti-Capture Governance

Status: **PASS (generic) / PRODUCT + ORGANIZATION + PROVIDER + MANAGED-IPAD + CUSTODY-RUNTIME VALIDATION OPEN**  
Date: 2026-09-19  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 126 organizational-loss recovery authority/provenance; 154 authority-floor escrow/disaster recovery; Track A local-runtime evidence boundary; Track B truthful recovery UX; Track C destructive organizational-loss drills; Track D diagnostics only.

## Why this study exists

154 established that catastrophic control-plane loss requires an independently recoverable anti-resurrection authority floor, while the escrow/recovery copy must not become a second ordinary authorization oracle. That still leaves an organizational failure mode: technically intact recovery material may be unusable because the legitimate custodians are unavailable, deceased, departed, compromised or organizationally displaced. The opposite failure is equally dangerous: succession may concentrate recovery power in one surviving insider or leave stale former custodians with permanent shadow authority.

The objective is therefore to preserve **recoverability through personnel/organizational change without making succession itself an authorization bypass or permanent alternate control plane**.

## SOURCE

### NIST SP 800-53 Rev. 5 / Release 5.2.0 — separation of duties and least privilege
AC-5 requires identifying duties that need separation and defining access authorizations to support that separation. Its discussion explicitly frames separation of duties as reducing abuse of authorized privileges and malevolent activity without collusion. AC-6 requires least privilege for users and processes. These controls support separating custody, recovery approval, execution and audit rather than giving one role end-to-end recovery power.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

### NIST SP 800-53A Rev. 5 — contingency roles/responsibilities must be assessable
CP-02 assessment procedures expect contingency plans to address roles, responsibilities, assigned individuals/contact information, maintenance of essential functions and eventual restoration without deterioration of planned controls. The plan is reviewed, distributed to key contingency personnel and updated when organization/system/environment changes. Transfer lesson: a recovery design is incomplete if only named people know how it works or if succession is undocumented and untested.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

### NIST SP 800-34 Rev. 1 — recovery requires coordinated planning and testing
NIST contingency guidance treats recovery as coordinated plans, procedures and technical measures, including alternate processing/storage strategies. Recovery viability therefore depends on organizational preparation and testing, not merely possession of backup bytes.

Source:
- https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final

### NIST SP 800-84 — exercise people and plans, not only systems
NIST's test/training/exercise guidance exists to train personnel, exercise plans and test systems for adverse situations. Transfer: organizational-loss recovery needs drills that remove normal custodians/admins from the scenario rather than repeatedly testing with the same experts who designed the system.

Source:
- https://csrc.nist.gov/pubs/sp/800/84/final

### NIST SP 800-57 Part 1 Rev. 5 — split knowledge and key recovery are distinct concepts
NIST defines split knowledge as dividing key material into shares such that fewer than the threshold reveal no key knowledge; key recovery is the authorized retrieval/reconstruction of keys or key information from backup/archive. These mechanisms can reduce single-custodian exposure for suitable cryptographic material, but they do not themselves establish who is legitimately authorized after organizational change.

Sources:
- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://csrc.nist.gov/glossary/term/split_knowledge
- https://csrc.nist.gov/glossary/term/key_recovery

### NIST two-person control / dual authorization
NIST's glossary describes two-person control as continuous control by at least two authorized individuals, each able to detect incorrect or unauthorized procedures. This supports dual-control concepts for high-consequence recovery, while not prescribing a universal quorum for MintTap/LogMate.

Source:
- https://csrc.nist.gov/glossary/term/two_person_control

## SYNTHESIS — survivability and anti-capture are simultaneous requirements

A recovery custody system fails in two opposite directions:

1. **organizational-loss lockout** — valid recovery material exists but no legitimate path remains to use it;
2. **organizational capture** — one surviving insider, stale custodian, compromised succession record or emergency shortcut gains durable authority beyond the recovery event.

The design objective is not maximum redundancy of privileged people. It is a bounded succession system where loss of ordinary personnel does not destroy recovery, while no individual, stale role or emergency mechanism silently becomes permanent production authority.

Persistent guards:
- `recovery material survives ≠ recovery authority survives`;
- `named custodian unavailable ≠ next available employee authorized`;
- `successor designated ≠ successor authenticated/current`;
- `quorum reached ≠ recovery intent legitimate`;
- `split knowledge ≠ separation of recovery duties`;
- `dual control ≠ independent failure domains`;
- `emergency authority activated ≠ permanent authority granted`;
- `former custodian departed ≠ old share/credential harmless`;
- `custody rotated ≠ old recovery package automatically invalidated`;
- `organizational chart current ≠ cryptographic custody current`;
- `recovery completed ≠ temporary recovery authority retired`.

## Recovery roles: separate semantics before choosing people

Generic recovery should distinguish roles such as:
- **custodian** — protects a recovery share/package/material;
- **recovery approver** — establishes that recovery conditions and policy requirements are met;
- **recovery executor** — performs the technical reconstruction/reconstitution;
- **independent verifier/auditor** — checks evidence, lineage, ceremony and retirement of temporary authority;
- **organizational authority/succession authority** — authorizes legitimate role replacement under defined governance.

A product need not implement these as five separate humans or systems. The important property is that high-consequence recovery does not accidentally collapse custody + approval + execution + audit into one unchecked actor.

## Succession lifecycle

Succession must be an explicit lifecycle, not an emergency improvisation.

A generic role state model:
`NOMINATED → VERIFIED → ACTIVE → SUSPENDED/UNAVAILABLE → REPLACED → RETIRED/REVOKED`.

Useful rules:
1. successor identity and organizational authority are authenticated independently of the material being recovered;
2. activation has an effective generation/epoch and audit provenance;
3. predecessor authority is explicitly retired/revoked when replacement becomes authoritative;
4. stale copies/shares/credentials are treated as potentially live until rotation/resealing proves otherwise;
5. succession records themselves have version/lineage/currentness semantics;
6. emergency succession cannot lower the recovered authority floor from 154;
7. no client, offline PWA or ordinary production request can select a historical custodian generation.

## Quorum and multi-party custody: what they solve and what they do not

Threshold/split-knowledge or dual-control arrangements can reduce single-person loss/compromise risk. They do **not** automatically solve:
- collusion;
- all custodians sharing one identity/provider/device/location failure domain;
- stale organizational membership;
- coerced or socially engineered approvals;
- incorrect recovery target/package;
- freshness/rollback of the authority floor;
- permanent emergency authority after recovery.

Therefore `k-of-n` is not itself a security conclusion. Exact quorum, geography, provider, hardware and ceremony are product-specific OPEN decisions.

## Anti-capture governance

A recovery path should be difficult to capture permanently even when emergency access is necessary.

Generic controls:
- recovery authority is **purpose-scoped** to a named incident/reconstitution target;
- activation is **time/epoch bounded** where technically meaningful;
- recovery action cannot silently rewrite succession rules that authorize itself;
- changing custodians/quorum/recovery policy requires a separately governed transition;
- high-consequence changes preserve predecessor/successor provenance and independent review;
- emergency recovery credentials are not copied into ordinary long-lived admin roles;
- post-recovery reconstitution creates/activates current production authority under the recovered floor, then removes temporary recovery access;
- unresolved contradiction about successor legitimacy yields `RECOVERY-AUTHORITY-UNKNOWN`, not first-come-first-served control.

## Succession-document and identity failure modes

A signed/current-looking succession document can still be wrong if:
- the signer was no longer authorized when it became effective;
- a later superseding succession event is missing;
- the named successor account was compromised/recycled;
- organizational identity and technical credential refer to different people/entities;
- the document survived but the verifier/trust root did not;
- two valid-looking branches nominate different successors.

Therefore organizational succession requires the same broad lessons learned for technical authority lineage: authenticity, currentness, continuity, non-equivocation where required, and bounded recovery when evidence is incomplete.

## Personnel departure and stale-share retirement

When a custodian leaves or changes role:
1. remove ordinary account/access paths promptly;
2. mark custody role transition with a new generation/epoch;
3. assess whether the former custodian could retain usable recovery material;
4. rotate/reseal/re-share material when consequence warrants it;
5. update independent custody records and recovery instructions;
6. test that the new custodian set can recover without the former member;
7. verify that the former set can no longer independently satisfy current recovery policy where that property is required.

Deleting an employee account is insufficient if they possessed an offline share or physical recovery artifact.

## Organizational-loss scenarios

Recovery planning should deliberately test scenarios beyond ordinary administrator absence:
- all normal production admins unavailable;
- one custodian unavailable;
- multiple custodians unavailable but threshold still satisfiable;
- threshold cannot be met;
- one surviving custodian malicious/compromised;
- former custodian presents an old share;
- successor record is stale;
- two succession branches conflict;
- identity provider is part of the outage;
- primary corporate communication channel is compromised;
- audit/verifier role is unavailable;
- provider account ownership has changed;
- company reorganization/merger/name change breaks role assumptions;
- founder/owner unavailable;
- disaster spans normal geographic custody domains.

A successful drill must demonstrate both **recoverability** and **non-capture**.

## Post-recovery resealing and shadow-authority elimination

Recovery is not complete when production comes back online. Reconstitution must remove temporary authority.

Generic sequence:
1. establish recovered authority floor and legitimate recovery participants;
2. reconstitute current production authority;
3. rotate/revoke temporary recovery credentials and compromised/ambiguous credentials;
4. reseal/re-share escrow material against the new current authority/custody generation;
5. supersede old recovery packages without losing historical verification evidence needed for audit;
6. verify ordinary request paths cannot invoke recovery authority;
7. re-establish monitoring and independent audit;
8. run a post-recovery negative test proving predecessor/emergency paths no longer authorize;
9. record remaining uncertainty and residual risk explicitly.

`production responding normally` is not sufficient closure evidence.

## PWA / Service Worker / EFB application

The organizational custody model remains server/organization-side authority. A long-offline company iPad may contain irreplaceable flight records and old runtime state, but:
- it cannot nominate a recovery custodian;
- cached admin/session/policy state cannot satisfy current organizational succession;
- device possession does not prove current organizational role;
- local records should remain preservable/exportable while remote authority is unresolved;
- reconnect after organizational recovery must reconcile against the newly established current authority/custody generation;
- a stale PWA must not offer a UI path that implies an old administrator/custodian can reactivate predecessor authority.

Actual managed-iPad identity, device management, local key storage, offline export and sync behavior remain OPEN.

## Cross-track integration

### Track A — Platform & Browser
Dependency supplier. Establishes which local SW/cache/IndexedDB/session artifacts can survive organizational recovery. Transfer: local persistence does not convey organizational recovery authority.

### Track B — UX / IA / Content
Owns truthful degraded/recovery states. User-facing wording must distinguish `your local data is preserved` from `organizational recovery authority has been re-established`; avoid destructive cleanup prompts and false administrator-success signals.

### Track C — Performance / Accessibility / Quality
High-pressure consumer. Owns organizational-loss tabletop/destructive drills, stale-share/credential tests, conflicting succession evidence, post-recovery negative authorization tests and accessible recovery UX.

### Track D — Search / Discovery / Analytics
Supporting consumer only. Telemetry may identify affected users/devices and recovery progress, but analytics cannot establish custodian legitimacy or succession currentness.

### Track E — Owner
Owns custody topology, succession semantics, separation of duties, emergency activation, anti-capture, resealing and shadow-authority retirement.

## MINTTAP DECISION — minimal sufficient generic model

If this class of recovery authority is implemented:
1. define custody, approval, execution, audit and succession semantics before assigning individuals;
2. avoid one-person end-to-end recovery for high-consequence authority where the threat model requires separation;
3. make succession versioned, authenticated, currentness-aware and explicitly revoke predecessor custody;
4. treat quorum/split knowledge as mechanisms, not proof of legitimate recovery;
5. test organizational loss with normal experts intentionally absent;
6. preserve a bounded emergency path without making it an ordinary fallback authorization plane;
7. after recovery, rotate/reseal material and prove emergency/predecessor paths no longer authorize;
8. keep offline PWA data preservation independent of organizational authority recovery;
9. do not choose quorum counts, providers, hardware, geography or legal succession rules until actual product/organization requirements exist.

## VALIDATION — 52-case organizational-loss / anti-capture campaign

1. all normal admins unavailable; 2. one custodian unavailable; 3. threshold still satisfiable; 4. threshold unsatisfiable; 5. one custodian compromised; 6. one custodian malicious; 7. two custodians collude; 8. all custodians share same IdP outage; 9. all shares share same physical site; 10. former employee presents old share; 11. former account disabled but offline share retained; 12. successor correctly nominated; 13. successor document forged; 14. authentic but stale successor document; 15. two authentic successor branches conflict; 16. successor account compromised; 17. successor identity recycled; 18. organization renamed/restructured; 19. founder/owner unavailable; 20. provider account owner unavailable; 21. corporate email compromised; 22. IdP unavailable; 23. audit role unavailable; 24. recovery approver unavailable; 25. executor unavailable; 26. one person holds custodian+approver roles unexpectedly; 27. one person holds executor+auditor roles unexpectedly; 28. quorum reached with wrong recovery target; 29. quorum reached on stale package; 30. emergency recovery invoked legitimately; 31. emergency authority exceeds purpose; 32. emergency authority exceeds time/epoch; 33. emergency actor edits its own succession policy; 34. temporary credential leaks; 35. production restored but temporary authority remains; 36. post-recovery rotation succeeds; 37. resealing succeeds with new custody generation; 38. old package remains historically verifiable but non-authoritative; 39. old quorum cannot satisfy current recovery policy; 40. new quorum recovery drill succeeds; 41. ordinary request path cannot consult escrow; 42. client cannot select custodian generation; 43. stale Service Worker exposes old admin UI but server denies; 44. offline iPad contains unique records; 45. local export works while organizational authority unknown; 46. device possession does not confer recovery role; 47. reconnect reconciles to new authority generation; 48. accessible UX distinguishes data preservation from authority restoration; 49. telemetry unavailable but recovery legitimacy remains independently verifiable; 50. succession evidence gap produces UNKNOWN not auto-permit; 51. post-recovery negative test proves predecessor/emergency path rejected; 52. full organizational-loss exercise restores service without predecessor resurrection or single-insider capture.

## CONTRADICTION / failure-mode analysis

### More-custodians-is-more-resilient theater
Adding people without independent failure domains, current role governance and revocation can increase attack surface without materially improving recoverability.

### Quorum-is-authorization theater
A threshold proves enough shares/signers participated. It does not prove the target, incident, package or participants are currently legitimate.

### HR-offboarding-is-key-revocation theater
Disabling an account does not invalidate offline shares, printed recovery material or copied secrets.

### Emergency-means-bypass theater
Emergency conditions justify a pre-governed bounded path, not abandonment of every security boundary.

### Recovery-complete-when-online theater
Service restoration with surviving temporary recovery credentials creates shadow authority and leaves the incident unresolved.

### PWA-device-as-successor theater
Possession of an offline company iPad can preserve business evidence; it does not establish organizational succession or recovery authority.

## OPEN

Actual MintTap/LogMate corporate roles, legal succession, staffing, provider account ownership, IdP/admin topology, recovery custodians, quorum, key/share mechanism, HSM/KMS, physical storage, geographic distribution, audit role, communication channels, emergency contacts, insurance/legal/aviation obligations, managed-iPad identity and runtime behavior remain unknown. No concrete person count, quorum, provider, hardware token, jurisdictional succession rule or ceremony is asserted.

## CHANGE WATCH

- NIST SP 800-53 / 800-53A patch releases and contingency-control changes.
- NIST SP 800-57 Part 1 Rev. 6 remains draft; reassess split-knowledge/key-storage guidance when finalized.
- Provider KMS/HSM recovery, account ownership, break-glass and quorum capabilities.
- Organizational/legal succession requirements relevant to the actual company and jurisdiction.
- WebKit/iPadOS managed-device identity/storage behavior where product recovery claims depend on it.

## Gate result

**PASS (generic).** The Web Manager can now distinguish technical escrow survivability from organizational recovery authority; design explicit custody/succession lifecycles; apply separation-of-duty and multi-party mechanisms without treating quorum as legitimacy; test organizational loss and insider capture; and require post-recovery resealing plus proof that temporary/predecessor authority is gone.

Product/organization/provider/managed-iPad/custody-runtime validation remains **OPEN**.

## Adjacent-question check and next target

The immediately adjacent question completed in this bundle was **post-recovery resealing and shadow-authority elimination**, because stopping at succession activation would leave a dangerous permanent emergency plane.

The next highest-value boundary is **PWA recovery-ceremony evidence, human-factor failure & social-engineering resistance**: establish how recovery participants verify the exact target/package/incident and each other under degraded communications, prevent approval fatigue/coercion/channel compromise, and preserve independently reviewable ceremony evidence without turning audit artifacts into reusable recovery credentials.