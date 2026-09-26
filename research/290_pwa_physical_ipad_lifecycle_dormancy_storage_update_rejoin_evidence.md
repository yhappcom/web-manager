# 290 — Physical-iPad Lifecycle, Dormancy, Storage, Update & Rejoin Evidence Limits

Status: **PASS (generic) / PHYSICAL + MANAGED-IPAD + PRODUCT EXECUTION OPEN**  
Date: 2026-09-27  
Primary owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: 288–289; Track A platform mechanics; Track E authority/currentness.

## Purpose
Define what compressed PWA tests can prove and what requires real elapsed physical-iPad evidence. The central rule is: **offline duration is not one variable and evidence does not promote across untested dimensions.**

## SOURCE
- WebKit storage policy documents origin/overall quota and eviction, including storage pressure; persistent storage changes eviction treatment but is not backup: https://webkit.org/blog/14403/updates-to-storage-policy/
- Storage API persistence is browser-policy dependent: https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- Service Workers are event-driven and lifecycle/update behavior remains CHANGE WATCH: https://www.w3.org/TR/service-workers/
- Apple/WebKit platform behavior and physical-device inspection remain version-specific CHANGE WATCH.

## Five-track allocation
- **A:** lifecycle/controller/cache/storage mechanics and browser-version boundaries.
- **B:** truthful offline/saved/queued/revalidating/recovery UX consumes outcomes.
- **C:** owns evidence dimensions, promotion rules and physical-device campaign design.
- **D:** may measure observed outcomes but telemetry cannot prove unobserved durability.
- **E:** owns current admission, queued-effect adjudication and destructive-recovery authority.

## Evidence dimensions
Record independently: elapsed dormancy; process/lifecycle disruption; network condition; runtime/Service Worker generation; schema generation; storage condition; Safari/Home Screen launch context; device/iPadOS/WebKit version; managed/unmanaged state; instrumentation; unique local data; remote authority/currentness change.

### Dormancy ladder
- **D0:** compressed deterministic offline interval.
- **D1:** same-day physical elapsed interval.
- **D2:** multi-day physical elapsed interval.
- **D3:** elapsed interval matching a declared product support window.
- **D4:** representative operational dormancy on the actual managed/company-device class.

These are test classes, not WebKit guarantees. Do not invent a universal safe number of days.

### Lifecycle ladder
- **L0:** background/foreground.
- **L1:** termination and relaunch.
- **L2:** physical device restart.
- **L3:** deliberate iPadOS/WebKit update transition.
- **L4:** verified managed-device policy/lifecycle transition.

### Storage ladder
- **S0:** ordinary storage conditions.
- **S1:** actually reproduced storage-pressure exposure.
- **S2:** persistence-state comparison.
- **S3:** destructive-loss/recovery drill.

Persistent storage is not backup, restore, semantic integrity or sync evidence.

### Update/rejoin ladder
- **U0:** no material remote/runtime change.
- **U1:** server/API/policy change.
- **U2:** Service Worker/runtime change.
- **U3:** schema migration.
- **U4:** session/admission/recovery-authority change.
- **U5:** multiple-generation transition.

## Promotion rules
A PASS proves only its tested envelope. Example: T3+D2+L2+S0+U2 on one unmanaged Home Screen iPad does not prove S1 pressure survival, L3 OS-update behavior, D3 support-window durability, T4 managed-device behavior or fleet-wide durability.

Guards:
- `compressed offline PASS ≠ long-dormant iPad durability PASS`;
- `survived relaunch ≠ survived restart ≠ survived OS transition`;
- `persistent storage ≠ backup`;
- `no eviction observed ≠ eviction impossible`;
- `bytes survived ≠ semantic integrity proven`;
- `network restored ≠ sync/convergence proven`;
- `update available ≠ update adopted ≠ data migrated ≠ session current`;
- `Home Screen launch ≠ offline durability proof`;
- `debugger-observed timing ≠ uninstrumented timing equivalence`.

## Physical-iPad evidence record
Capture device model; iPadOS/Safari/WebKit version; launch mode; managed state; D/L/S/U class; elapsed interval; storage/persistence context; actual controller/cache/runtime/schema state; unique-data integrity summary; debugger state; current-admission evidence; migration/queue/convergence outcome; cleanup/normalization result.

When timing/lifecycle matters, pair diagnostic instrumented runs with uninstrumented behavioral runs.

## LogMate/EFB transfer
A company-iPad offline-support duration must be a product requirement before D3 can be designed. Generic WebKit evidence cannot manufacture that requirement. Unique flight/logbook data raises the consequence of destructive recovery, so preserve local data/provenance before repair. Direct unattended device-to-device sync, background execution, hotspot behavior and storage durability remain OPEN until separately validated.

## Track C destructive additions — defined, not executed
1073. **Duration-threshold invention:** undocumented elapsed threshold treated as platform guarantee.  
1074. **Dimension collapse:** dormancy/lifecycle/storage/update collapsed into one “offline” PASS.  
1075. **Persistence-as-backup:** persistence grant treated as recoverability proof.  
1076. **No-eviction promotion:** one non-eviction observation treated as impossibility proof.  
1077. **Home-Screen durability fallacy:** install/launch success treated as offline durability.  
1078. **Single-envelope fleet promotion:** one device/OS envelope promoted to fleet claim.  
1079. **Rejoin-as-sync PASS:** connectivity restoration treated as semantic convergence.  
1080. **Instrumentation equivalence:** debugger-observed lifecycle promoted to uninstrumented behavior.

All are **DEFINED / NOT EXECUTED**.

## MINTTAP DECISION / DIRECTION
Use D/L/S/U evidence labels for future physical-iPad validation. Keep product support duration, managed-fleet configuration and production runtime facts OPEN. Next: managed-iPad/MDM policy boundary and deployment evidence contract.
