# 285 — PWA Stale-Client Rebootstrap, Downgrade Resistance & iPad Recovery Containment

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-25  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B recovery UX; Track C destructive validation; Track D rebootstrap diagnostics.  
Dependencies: 266–284 authority/currentness, anti-rollback, degraded-policy integrity, Service Worker distribution, mixed-generation adjudication and predecessor consequence closure.

## Problem

284 established that mixed client/runtime generations are normal and that stale clients do not retain stale remote authority. The adjacent problem is a client that has been offline long enough that its runtime, Service Worker, cached policy, session and queued operations all predate a security-relevant transition.

Central rule: **rebootstrap is not one update event. Transport authenticity, bootstrap-authority currentness, runtime adoption and queued-operation admission are separate transitions. A stale PWA may preserve unique local data while being denied material remote authority until current admission is re-established.**

## Five-track balance

- **A Platform/Browser:** high prerequisite supplier. Owns Service Worker lifecycle/update/control, storage and installed-web-app mechanics.
- **B UX/IA/Content:** elevated consumer. Owns truthful recovery states without exposing users to trust-root internals.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1032 → 1040 defined cases**. Runtime/device/AT/human execution remains OPEN.
- **D Search/Discovery/Analytics:** challenger. Measures rebootstrap attempts, predecessor rejection and time-to-current-admission; telemetry cannot elect authority.
- **E Architecture/Security/Operations:** highest-risk owner. Owns current bootstrap authority, downgrade resistance, remote-effect fencing and recovery containment.

## SOURCE

### W3C Service Workers — update/control is a runtime mechanism

Service Worker registration, update and client-control semantics persist independently of a single document lifetime. A newly installed/activated worker and existing controlled clients therefore require explicit lifecycle reasoning.

Source:
- https://www.w3.org/TR/service-workers/

**TRANSFER VALIDATION:** worker update/activation is evidence about browser runtime state. It is not evidence that organizational trust/currentness, user session authority, queued-operation authorization or server policy migrated.

### WebKit — iOS/iPadOS Home Screen web-app behavior is platform/version specific

WebKit documents Home Screen web apps, Service Worker support, Web Push, storage quotas/eviction and current install behavior. Safari 26 / iOS 26 / iPadOS 26 changed Home Screen behavior so a site added to Home Screen opens as a web app by default unless the user disables “Open as Web App”; WebKit explicitly notes that Service Workers are not an installability prerequisite on iOS/iPadOS.

Sources:
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- https://webkit.org/blog/14403/updates-to-storage-policy/
- https://webkit.org/blog/14787/webkit-features-in-safari-17-2/

**CHANGE WATCH:** these are WebKit/Apple platform behaviors, not universal PWA semantics. Managed/company iPad behavior, MDM/ADE restrictions, update timing and unattended execution require separate product/device evidence.

### WebKit — local storage is durable-looking but not a recovery authority

WebKit documents quota and eviction behavior and states that Home Screen web apps receive browser-app-class quota behavior. WebKit also documents that login cookies can be copied when a web app is created while other local storage is not copied.

**TRANSFER VALIDATION:** local data can be valuable and may persist, but quota/persistence/runtime behavior does not make local policy/session/bootstrap state an authoritative recovery root.

### TUF — current trust must resist rollback/freeze

The Update Framework separates trusted metadata roles, versions/expiry and root rotation so clients can detect rollback/freeze. Root compromise can require recovery outside the compromised normal path.

Source:
- https://theupdateframework.github.io/specification/latest/

**TRANSFER VALIDATION:** MintTap/LogMate is not assumed to use TUF. The reusable principle is that a predecessor trust state cannot be allowed to self-elect merely because current publication is unavailable.

### RFC 9162 — consistency evidence is not global currentness by itself

Certificate Transparency defines Merkle inclusion/consistency proofs and auditing. It also notes that checking consistent views across all entities is harder and requires sharing log responses; gossip is not defined by the RFC as a complete protocol.

Source:
- https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** cryptographic continuity can prove bounded history properties without proving organizational currentness or eliminating split-view concerns.

## SYNTHESIS 1 — rebootstrap has four distinct closures

Treat stale-client recovery as at least four evidence transitions:

1. **transport authenticity** — the client reaches an authenticated secure endpoint;
2. **bootstrap/currentness** — the response belongs to the currently authorized organizational lineage/policy;
3. **runtime adoption** — the browser/PWA has adopted the required application/worker/runtime generation;
4. **operation admission** — each queued material operation is adjudicated under current consequence semantics.

Guards:
- `HTTPS works ≠ bootstrap current`;
- `bootstrap current ≠ worker updated`;
- `worker updated ≠ session current`;
- `worker updated ≠ queued operation reauthorized`.

## SYNTHESIS 2 — fallback and downgrade are different operations

Availability fallback may choose another currently authorized endpoint, mirror or transport route. Authorization downgrade chooses an older/weaker policy because the current path is unavailable.

The former can be defensible when equivalence/currentness is established. The latter restores predecessor authority and is not an availability optimization.

Guards:
- `current endpoint unavailable ≠ predecessor acceptable`;
- `fallback route works ≠ fallback authority current`;
- `locally valid old root ≠ current root`.

## SYNTHESIS 3 — publication transport cannot manufacture organizational legitimacy

HTTPS, CDN, Service Worker, push, MDM or a bootstrap endpoint can transport successor material. Successful delivery proves a delivery fact. It does not independently establish that the material is the legitimate successor of the organizational authority being replaced.

Conversely, compromise of one publication channel does not automatically prove compromise of every independent organizational recovery authority. Threat domains must be modeled rather than collapsed.

## SYNTHESIS 4 — stale Service Worker is neither disposable data nor a trust root

A stale worker/cache can contain useful code/data needed to render local records or export them. It must not be allowed to self-authorize obsolete remote effects.

Recovery therefore preserves unique user data and provenance first, while treating worker/cache/policy/session state as evidence whose authority may need re-establishment.

Guards:
- `stale runtime ≠ corrupt user data`;
- `unique local data ≠ current local authority`;
- `worker cache available ≠ predecessor remote effect allowed`.

## SYNTHESIS 5 — runtime migration must not erase recovery evidence

A destructive “clear site data and reinstall” procedure can remove the very offline records/queue/provenance that make recovery necessary. Generic recovery ordering is therefore data-preservation-first unless verified product architecture proves equivalent durable copies exist.

This does not imply every cache/session/token must be preserved. Separate unique domain data/provenance from replaceable runtime/cache/credential material.

## SYNTHESIS 6 — iOS/iPadOS installability assumptions must be current

Safari 26 / iOS 26 / iPadOS 26 has no developer-side installability requirement for Home Screen web-app presentation: users can add any site and choose web-app behavior. A manifest remains useful for metadata/experience, and Service Workers remain useful for offline behavior, but neither should be described as an Apple installability prerequisite.

This differs from common Chromium-oriented PWA explanations and is **CHANGE WATCH**.

**MINTTAP DECISION:** future product requirements must say “Home Screen web app / installed web experience” precisely by platform/version rather than importing Chromium install criteria into iPadOS.

## SYNTHESIS 7 — storage persistence and recovery authority are orthogonal

WebKit quota/persistence behavior can improve local durability but does not create backup, restore proof, current authority or cross-device synchronization.

Guards:
- `quota available ≠ data persistent`;
- `persistent storage ≠ backup`;
- `local record survived ≠ queued mutation authorized`;
- `Home Screen install ≠ unattended background sync guaranteed`.

## SYNTHESIS 8 — recovery UX communicates task truth, not cryptographic internals

Track B should consume E’s security states and expose user-relevant distinctions such as:
- local data preserved;
- connection/current admission required;
- revalidation required;
- conflict/rejection;
- remote confirmation.

Exact wording and interaction design remain Design Studio + representative-human/AT validation.

Guards:
- `upload attempted ≠ synced`;
- `runtime updated ≠ recovery complete`;
- `cannot prove current authority ≠ local data lost`.

## SYNTHESIS 9 — telemetry is diagnostic, not an authority oracle

Track D may measure rebootstrap success/failure, runtime generation, predecessor attempts/rejections, queued-intent age and reconnect→current-admission latency. Dormant clients are intrinsically under-observed.

Therefore:
- `majority rebootstrap success ≠ predecessor extinct`;
- `zero old-client traffic ≠ no old client can return`;
- `dashboard green ≠ trust migration complete`.

## SYNTHESIS 10 — recovery containment is consequence-specific

If current bootstrap/currentness cannot be established, the safe response need not make the entire app useless. Local read/capture/export may remain available when product/domain policy permits, while remote publication, destructive mutation or other material effects are fenced.

This reuses 266–284 degraded-capability governance. Exact consequence classes remain product-specific and OPEN.

## SYNTHESIS 11 — predecessor extinction requires negative evidence

Deleting old keys/configuration or observing successor success is not enough. Closure requires evidence that material API, worker, background, admin/recovery and compatibility boundaries reject predecessor authority where it matters.

Guards:
- `successor published ≠ predecessor powerless`;
- `old root deleted ≠ predecessor authority extinct`;
- `new worker active ≠ old compatibility path fenced`.

## SYNTHESIS 12 — LogMate-like long-offline iPad recovery sequence

Generic sequence, not an implementation claim:

1. preserve unique local flight/logbook records, queue and provenance;
2. classify cached runtime/policy/session/bootstrap material as potentially stale;
3. establish authenticated transport and current organizational bootstrap/admission separately;
4. migrate runtime when required and platform behavior permits;
5. map queued intents to current semantics/consequence;
6. revalidate or hold each material effect rather than inheriting stale allows;
7. keep local preservation, remote admission, execution and acknowledgement as separate states;
8. retain predecessor rejection at authoritative boundaries even when a device cannot update immediately.

Direct unattended device-to-device sync, hotspot discovery, background execution, MDM repair, persistent storage and cross-device communication remain OPEN until separately verified.

## MINTTAP DECISION / DIRECTION

1. Model stale-PWA rebootstrap as transport → current bootstrap → runtime adoption → operation admission, not one “update complete” flag.
2. Never turn current-path failure into predecessor-authority fallback.
3. Preserve unique local records/provenance before destructive runtime repair.
4. Treat Service Worker/cache/session state as replaceable or historical evidence unless current authority is separately established.
5. Keep iOS/iPadOS behavior explicitly separate from Chromium PWA assumptions; Safari 26 install behavior is CHANGE WATCH.
6. Keep local durability, backup, synchronization and authorization as separate guarantees.
7. Use consequence-specific containment when currentness is unknown rather than silently downgrading or erasing data.
8. Close predecessor retirement with negative evidence at material boundaries.
9. Keep production PASS OPEN until physical managed-iPad/WebKit/runtime/backend/human evidence exists.

## DEPENDENCY / TRANSFER

- **A → E/C:** Service Worker lifecycle, Home Screen web-app behavior and storage mechanics constrain rebootstrap but do not define authority.
- **E → B:** security/currentness states become task-truth UX requirements; Design Studio owns reusable interaction treatment.
- **E → C:** C receives downgrade, data-loss and stale-authority invariants for destructive validation.
- **E → D:** D measures recovery and contradictions; it cannot elect current authority.
- **Software Engineering:** implementation of bootstrap lineage, server admission, queue migration, backup/export and fault injection remains engineering evidence.
- **Design Studio:** latest canonical commits remain LogMate portfolio work; no new physical-device PWA, screen-reader or representative-human validation promotes this gate.

## Track C destructive additions — defined, not executed

1033. **TLS-equals-currentness:** valid HTTPS bootstrap response is accepted as current organizational authority without lineage/currentness proof.  
1034. **Availability downgrade:** current bootstrap fails and the client/server restores predecessor remote authorization.  
1035. **Worker-activation theater:** Service Worker activation is treated as session/policy/queued-operation reauthorization.  
1036. **Destructive recovery:** reinstall/clear-site-data destroys unique local records or provenance before verified durable recovery.  
1037. **User trust-root election:** ordinary recovery UI asks the user to choose which conflicting authority/root is “trusted.”  
1038. **Platform-assumption drift:** Chromium install/update assumptions are applied to iPadOS and hide an unsupported recovery dependency.  
1039. **Telemetry extinction theater:** low/zero predecessor traffic is treated as proof that dormant predecessor clients cannot return.  
1040. **Successor-only closure:** successor bootstrap/runtime tests pass while a worker/admin/compatibility boundary still accepts predecessor authority.

Execution, physical-device, AT and representative-human PASS are not claimed.

## OPEN

Actual MintTap/LogMate bootstrap topology, authority lineage, auth/session/token model, Service Worker/update timing, managed-iPad/MDM/ADE behavior, storage persistence, local schema, queue semantics, backup/export, server admission, compatibility paths, consequence classes, legal/aviation/safety requirements and human/accessibility behavior remain OPEN.

## CHANGE WATCH

- Safari/WebKit/iOS/iPadOS Home Screen web-app, Service Worker, storage, push/background and managed-device behavior.
- Service Worker specification evolution and browser implementation differences.
- TUF/CT references are bounded security precedents, not prescribed MintTap architecture.

## VALIDATION

Generic gate passes because the model now distinguishes runtime mechanics, publication transport, organizational currentness, operation admission, local-data preservation and predecessor retirement, and supplies destructive cases for those boundaries.

Production validation remains OPEN.