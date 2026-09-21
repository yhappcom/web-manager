# 207 — PWA Recovery-Anchor Succession, Bootstrap-Channel Compromise & Zero-State Provisioning

Status: **PASS (generic) / PRODUCT + RECOVERY-ANCHOR + PROVISIONING + MDM + MANAGED-IPAD + RUNTIME + SECURITY/LEGAL + HUMAN VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/platform transport; Track B recovery UX; Track C destructive assurance; Track D bounded observation.  
Dependencies: 171–206, especially 204–206.

## Problem
206 established exceptional witness-policy reconstitution through a separately governed recovery anchor. The adjacent failure is one level higher: the recovery anchor itself must rotate, may be compromised, and must bootstrap factory/new/erased clients without turning WebPKI, MDM, support content, newest-looking metadata, or physical possession of old media into an accidental super-root.

Central rule: **recovery-anchor succession is a versioned trust-policy transition; delivery/provisioning channels transport candidate trust material but do not automatically authorize it. If the current recovery anchor is itself untrustworthy, ordinary continuity cannot be fabricated and a separately governed reconstitution basis is required. There is no generic mechanism that eliminates the need for some explicitly accepted initial trust basis.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. HTTPS, secure context, browser storage and Service Worker can fetch/cache bootstrap material; Apple managed-device mechanisms can provision certificates/configuration where supported. None independently proves constitutional recovery authority.
- **B UX/IA/Content:** high dependency pressure. Must distinguish `ANCHOR UPDATE REQUIRED`, `ANCHOR RECONSTITUTION REQUIRED`, `BOOTSTRAP CHANNEL UNTRUSTED`, `LOCAL DATA PRESERVED`, `REMOTE AUTHORITY QUARANTINED`, `RE-ADMISSION REQUIRED`.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign reaches **416 defined cases**; execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. May observe anchor/package adoption and conflict but cannot elect trust by popularity, indexing or telemetry majority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns anchor succession/reconstitution, channel separation, provisioning classes, anti-downgrade/extinction and recovery evidence.

## SOURCE

### TUF — initial root and root-key succession
TUF clients start from trusted root metadata obtained out of band. Root rotation proceeds incrementally: version N+1 must satisfy the threshold of the currently trusted root N and the threshold declared by N+1; trusted root metadata is persisted to non-volatile storage. TUF also warns that threshold Root compromise requires out-of-band recovery rather than pretending ordinary continuity survived.

Sources:
- https://theupdateframework.github.io/specification/
- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** predecessor+successor authorization and explicit initial bootstrap are strong precedents. TUF is not adopted as MintTap architecture.

### Apple managed-device provisioning is a real transport/provisioning mechanism, not generic recovery authority
Apple Platform Deployment documents declarative device management and certificate/identity configurations. Certificate configurations can deploy certificates/identities on iPadOS and support Device Enrollment and Automated Device Enrollment. Apple also documents that device-management-installed certificates can receive automatic trust in specified cases, and that a device management service can remove certificates it installed. Current Apple guidance additionally notes implementation differences among device-management services.

Sources:
- https://support.apple.com/guide/deployment/declarative-device-management-manage-apple-depc30268577/1/web/1.0
- https://support.apple.com/guide/deployment/depbdaa1115b/web
- https://support.apple.com/guide/deployment/depcdc9a6a3f/web

**TRANSFER VALIDATION:** managed iPad provisioning can materially affect bootstrap design. It does not establish that LogMate has MDM, that MDM is independent of the failed anchor, or that an MDM-delivered certificate should be MintTap's constitutional recovery anchor.

### NIST SP 800-57 Part 1 Rev.5
The current final NIST key-management baseline explicitly treats trust anchors, compromise, recovery, cryptoperiods and key lifecycle as security dependencies.

Source: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

**TRANSFER VALIDATION:** anchor replacement is lifecycle/governance work, not merely certificate deployment. Exact hierarchy remains product/security architecture evidence.

## SYNTHESIS 1 — ordinary anchor succession and anchor reconstitution are distinct
Let recovery-anchor policy A authorize recovery packages. A normal A→A+1 transition can preserve continuity only when A remains trustworthy enough to authorize its successor under the admitted policy. The successor must also satisfy its own admission requirements where policy requires.

If A is compromised beyond that assumption, an A-signed A+1 does not repair trust. The system enters **ANCHOR RECONSTITUTION**, requiring another explicitly governed basis rather than silently weakening validation.

`old anchor signs successor ≠ safe succession when old anchor is compromised`.

## SYNTHESIS 2 — avoid infinite regress by making the initial trust assumption explicit
No generic protocol can prove an ultimate trust anchor solely from untrusted network state. A client must begin from some accepted basis: built-in material, enterprise/device provisioning, controlled physical ceremony/media, independently verified operator action, or another product-specific mechanism.

The engineering goal is not to hide this assumption behind another URL. It is to minimize its scope, protect its custody, make replacement/reconstitution explicit, and preserve anti-rollback evidence where possible.

`bootstrap mechanism exists ≠ trust assumption eliminated`.

## SYNTHESIS 3 — authorization and distribution/provisioning remain separate
WebPKI/TLS, CDN, support pages, MDM, QR transfer, removable media, Apple Configurator and manual configuration can deliver bytes/configuration. A channel may be highly authenticated and still not possess authority to redefine the recovery constitution.

Conversely, an authorized successor anchor that cannot reach a device is an availability failure, not permission to accept a stale reachable anchor.

`managed delivery ≠ recovery authorization`; `channel authenticated ≠ anchor current`.

## SYNTHESIS 4 — bootstrap-channel compromise must not silently become anchor compromise
Model at least these failure domains separately where applicable:
- recovery-anchor signing/custody;
- WebPKI/origin/CDN;
- MDM enrollment and administrator authority;
- device identity/provisioning service;
- support/operator workflow;
- physical/offline bootstrap media;
- storage/PITR/backup;
- personnel/recovery governance.

A channel is useful as independent recovery evidence only to the extent that its decisive compromise path is independent of the modeled anchor failure.

`different product name/vendor ≠ independent bootstrap channel`.

## SYNTHESIS 5 — zero-state clients after anchor rotation need a current initial basis
A factory/new/erased client lacks durable local anti-rollback history. It cannot distinguish A from retired A-1 merely because A has a larger generation or newer wall-clock date. Provisioning must therefore supply or authenticate a current initial basis according to a separately defined bootstrap policy.

For managed iPad, Apple mechanisms show that device-management enrollment can provision trusted certificates/configurations, but exact LogMate eligibility, supervision/enrollment mode, MDM vendor behavior and recovery independence remain OPEN.

`device erased ≠ safe to forget retired anchors`; `zero-state ≠ newest-state`.

## SYNTHESIS 6 — old bootstrap media/configuration must become historical-only
Anchor succession is incomplete if old installation media, QR packages, configuration profiles, support documents or MDM declarations can still create current remote authority on a newly provisioned device.

Retirement requires inventory plus scoped extinction evidence. Unknown copies remain `UNKNOWN`, not falsely `DESTROYED`. Where physical/offline material cannot be recalled, server-side current admission must still prevent that material from restoring retired authority.

`old media unavailable to inventory ≠ old media nonexistent`.

## SYNTHESIS 7 — managed-device trust installation can be powerful and therefore dangerous
Apple documents automatic trust for certificates installed through supported device-management paths in defined circumstances. That makes MDM a potentially strong provisioning mechanism but also means MDM administrator/enrollment compromise can be security-critical if product architecture elevates MDM-delivered material into recovery authority.

Therefore do not equate `MDM-installed` with `constitutionally authorized` without an explicit product threat model.

## SYNTHESIS 8 — long-offline EFB recovery preserves operational data before trust reset
For a company iPad that missed A→A+2 or was erased/re-enrolled:
1. preserve/export unique local operational records when they still exist and can be safely acquired;
2. classify the client as current/restored/zero-state rather than assuming continuity;
3. isolate stale anchor/session/SW state from remote authority;
4. obtain a current bootstrap basis through the admitted provisioning/recovery policy;
5. reject retired anchors/packages for current remote authority;
6. re-evaluate sessions, device identity and queued mutations under current policy;
7. reconcile data without rewriting uncertain historical authorization.

PWA data preservation remains independent from trust-anchor acceptance.

## SYNTHESIS 9 — positive successor proof must be paired with retired-anchor extinction
A+1 working proves availability, not A's retirement. Generic convergence requires scoped negative tests showing retired A/bootstrap package/media cannot authorize consequence-bearing operations, plus positive tests for A+1 and restore/PITR/new-client cases.

`new anchor provisions successfully ≠ retired anchor extinct`.

## SYNTHESIS 10 — channel migration and anchor migration are separate axes
Changing MDM vendor, WebPKI certificate, CDN/origin, provisioning endpoint or support workflow does not necessarily change the recovery anchor. Conversely, rotating the recovery anchor does not require treating every delivery channel as a new trust root.

This separation reduces unnecessary coupling and clarifies incident scope.

## Track C destructive campaign — 416 cases total
Add eight cases to the 408-case campaign:
1. compromised A signs A+1 after A crossed its compromise threshold — reject ordinary succession; require anchor reconstitution;
2. valid A→A+1 succession delivered only by compromised CDN — candidate remains verifiable by anchor policy; distribution compromise must not rewrite content;
3. attacker-controlled MDM pushes a new certificate labeled recovery root — managed installation alone cannot redefine constitutional authority;
4. zero-state iPad receives retired A from old enrollment/profile media and current A+2 from current provisioning — apply bootstrap policy, not newest-looking/network popularity;
5. old QR/offline bootstrap package remains physically available after A+1 — server rejects retired current authority even if bytes/signature remain authentic;
6. PITR restores old MDM declaration plus A while server enforcement has A+1 — no anchor resurrection;
7. A+1 provisions successfully but one region still accepts A — convergence fails negative extinction oracle;
8. long-offline/erased company iPad returns with unique records or restored backup after anchor rotation — preserve data, bootstrap current authority, re-admit queue without rewriting historical uncertainty.

Campaign status: **DEFINED, NOT EXECUTED**.

## Cross-track transfer / contradiction
### A → E
Browser secure context and managed-device transport/provisioning are mechanisms, not constitutional authority. Exact Safari/iPadOS/MDM enrollment, certificate trust, removal, reinstall/restore and PWA storage behavior require runtime/product evidence.

### E → B
Recovery UX must distinguish data preservation, device enrollment, trust bootstrap and remote re-admission. User support content cannot silently become a root-of-trust channel.

### E → C
C receives anchor-compromise, MDM-compromise, zero-state, stale-media, PITR, regional-extinction and long-offline cases.

### E → D
Telemetry may show anchor adoption/conflicts but cannot choose authority.

### Design Studio dependency
Design Studio Web remains W121 / Stage 3 PRACTICE / NOT PASSED. This study defines state semantics, not visual treatment; physical PWA/screen-reader/human evidence remains OPEN.

### Software Engineering dependency
Software Engineering Studio remains Foundation-stage. Exact secure anchor storage, serialization/signatures, managed-iPad provisioning, WebKit behavior, restore/reinstall and positive/negative authorization execution remain implementation evidence.

## MINTTAP DECISION / DIRECTION
1. Treat recovery-anchor policy as versioned security authority with explicit normal succession and exceptional reconstitution paths.
2. Do not make WebPKI, CDN, MDM, support pages, newest generation or device wall clock unilateral trust-reset authorities by accident.
3. Keep authorization separate from distribution/provisioning; assess independence against modeled failure domains.
4. Define zero-state bootstrap explicitly after anchor rotation; erased/new clients cannot manufacture anti-rollback history.
5. Retire old bootstrap media/configuration at server admission as well as operational inventory; unknown copies remain UNKNOWN.
6. For LogMate-like iPads, preserve unique local data before trust changes and re-admit remote work under current authority.
7. Require successor-positive and retired-anchor-negative evidence across regions, restore/PITR and new-client provisioning.
8. Keep actual MintTap/LogMate recovery-anchor hierarchy, MDM topology, cryptography and provisioning policy OPEN.

## OPEN / VALIDATION
- actual recovery-anchor hierarchy, custody, threshold and reconstitution basis;
- actual company-iPad enrollment/supervision/MDM and administrator topology;
- whether MDM is independent enough for any recovery role;
- exact initial anchor provisioning for factory/new/erased clients;
- old profile/media retirement and server-side extinction behavior;
- exact browser/PWA anchor persistence across reinstall/restore/erase;
- physical iPad/Safari/MDM, security/privacy, safety/legal/aviation, AT and human validation.

## CHANGE WATCH
- Apple device-management/declarative configuration capabilities and OS/version support change; re-check exact target iPadOS and MDM implementation before prescription.
- TUF bootstrap/root-rotation guidance and NIST key-management guidance remain precedent, not MintTap architecture.

## VALIDATION / GATE
**PASS (generic).** The Web Manager can now distinguish recovery-anchor succession from reconstitution, separate authorization from bootstrap transport/provisioning, model zero-state clients after anchor rotation, avoid infinite-regress handwaving by making the initial trust basis explicit, and require old-anchor extinction without sacrificing offline operational data. Product/runtime validation remains OPEN.

## Next highest-value adjacent question
**208 — recovery-anchor custody succession, organizational/provider loss & bootstrap survivability.** Determine how anchor authority survives loss of personnel, MDM tenant/provider, Apple/enterprise enrollment dependencies or company control-plane access without creating an always-online super-root; how custody succession and provider migration are evidenced; and how new/erased/long-offline devices bootstrap when both normal provisioning and one recovery distribution path are unavailable.