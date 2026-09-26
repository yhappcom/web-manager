# 289 — Deterministic Offline/Rejoin Fixtures, Validation-Control Protocol & Engineering Handoff

Status: **PASS (generic) / IMPLEMENTATION + PHYSICAL-IPAD + MANAGED-IPAD + AT + HUMAN + PRODUCT VALIDATION OPEN**  
Date: 2026-09-26  
Primary owner: **Track C — Web Performance, Accessibility & Quality**  
Dependencies: 285–288.  
Security owner/dependency: **Track E — Web Architecture, Security & Operations**  
Platform dependency: **Track A — Web Platform & Browser**

## Purpose

288 made recovery validation falsifiable through H01–H10. This checkpoint defines the minimum fixture identities, validation-control boundaries, reset invariants, evidence correlations and physical-iPad runbook needed to implement those scenarios without allowing test-only controls to become product authority.

Central guard: **test controllability is not product authority.**

## SOURCE

### W3C Service Workers — active platform semantics

The W3C publication history records a Service Workers Candidate Recommendation Draft dated 2026-09-17. Service Worker lifecycle and browser behavior remain CHANGE WATCH rather than a frozen implementation assumption.

Sources:
- https://www.w3.org/TR/service-workers/
- https://www.w3.org/standards/history/service-workers/

Transfer: fixture identity must distinguish registration/script/installing/waiting/active/controller state where the scenario depends on it. A harness may wait for observable lifecycle conditions; it must not pretend browser scheduling is deterministic.

### WebKit storage policy

WebKit documents origin quota, overall quota and eviction. A standalone Home Screen Web App on iOS uses the same origin/overall quota model as when opened in a browser app. Eviction may occur under overall-quota pressure, system storage pressure and other documented conditions. Persistent storage changes eviction treatment but is not backup or restore evidence.

Source:
- https://webkit.org/blog/14403/updates-to-storage-policy/

Transfer: a short deterministic offline fixture can test application recovery semantics but cannot certify long-elapsed dormancy, storage-pressure survival or user/device cleanup behavior.

### Storage API

The Storage API exposes quota/usage estimation and persistence state. `persist()` is a request whose result is browser-policy dependent; `persisted()` reports whether the bucket is persistent.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist
- https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persisted

Guard: `persistent storage granted ≠ backup verified ≠ restore verified`.

### WebKit physical-device observability

Safari 26 supports automatic inspection and optional pausing of newly running Service Workers for an app or Home Screen Web App.

Source:
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

Transfer: this improves evidence capture. Pausing/debugging can perturb timing, so instrumented and uninstrumented runs are distinct evidence classes.

## Five-track allocation

- **A Platform/Browser:** owns lifecycle/storage/cache/controller observables and browser-specific limits.
- **B UX/IA/Content:** consumes fixture outcomes as truthful saved/queued/revalidating/conflict/recovery states; does not own fixture mechanics.
- **C Quality:** owns fixture reproducibility, scenario protocol, verdict evidence and reset independence.
- **D Search/Discovery/Analytics:** consumes privacy-minimized correlation/convergence evidence; telemetry cannot elect authority or replace required test evidence.
- **E Security/Operations:** owns product-authority separation, material-boundary invariants, predecessor rejection and normalization semantics.

Track C is the primary owner because the current bottleneck is executable validation quality. E remains the highest-risk dependency.

## Fixture vocabulary F0–F10

A fixture is a declared initial state, not a production identity.

- **F0 current-clean:** current supported runtime/controller/cache/schema/verifier/session/policy state with no residual test queue.
- **F1 old-controller:** known predecessor controller remains in control while successor deployment material exists.
- **F2 stale-cache:** successor runtime paired with a known predecessor cache generation.
- **F3 generation-skew:** deliberately mismatched runtime/schema/verifier/session/policy generations within declared compatibility bounds.
- **F4 dormant-unique-data:** offline client with unique local records, provenance and queued intent not yet represented remotely.
- **F5 retired-authority:** successor established while known predecessor/emergency material is retained only for negative testing.
- **F6 policy-transition-queue:** operation admitted/queued before a material policy transition and executed or reconsidered afterward.
- **F7 interrupted-migration:** migration stopped at a named durable boundary, including restart/termination variants.
- **F8 beyond-migration-horizon:** client older than supported migration horizon while unique local data remains recoverable/preservable.
- **F9 contradictory-currentness:** two or more valid-looking but contradictory recovery/currentness claims.
- **F10 observation-loss:** one mandatory evidence channel intentionally unavailable.

Fixture labels are harness vocabulary. They do not imply that MintTap or LogMate currently implements these generations.

## Fixture identity contract

Each fixture records as applicable:
1. fixture schema/version and creation provenance;
2. browser/device/OS validation tier;
3. Service Worker registration/scope/script and actual controller identity;
4. cache-set identity;
5. application schema/data generation;
6. verifier/bootstrap/policy generation;
7. session/admission generation;
8. queue/provenance generation and privacy-safe integrity summary;
9. backend test-policy/acceptance generation;
10. expected invariants and cleanup target.

Use opaque non-secret test identifiers. Correlation IDs must not be credentials or authorization inputs.

Guards:
- `fixture identity ≠ product identity`;
- `correlation ID ≠ credential`;
- `generation probe ≠ authority oracle`;
- `test metadata says current ≠ current authority proven`.

## Validation-control protocol

Allowed test controls may include:
- hold/release test network paths;
- select a prebuilt test deployment or fixture;
- seed privacy-safe synthetic records;
- interrupt a migration at explicit test hooks;
- expose diagnostic generation/probe information;
- capture backend decision/correlation evidence;
- reset isolated test state.

Controls must not:
- mint or bypass production authorization;
- make client-supplied generation authoritative;
- introduce a production-only backdoor;
- weaken real material-boundary checks;
- require production secrets in fixtures/logs;
- silently alter consequence classification.

Guard: **deterministic setup may control conditions, never legitimacy.**

## H01–H10 mapping

### H01 old controller / new deployment
Fixture: F1. Hold a predecessor controller while successor material is available. Prove the actual controller, then exercise representative material boundaries. PASS requires successor/current rules at those boundaries and no predecessor-only material effect. UNKNOWN if controller or boundary decision cannot be observed.

### H02 new worker / stale cache
Fixture: F2. Compose a known successor runtime with predecessor cache content. PASS requires declared migration/rejection/containment behavior and no unsafe silent composition. Cache identity must be observed separately from worker identity.

### H03 generation skew
Fixture: F3. Vary declared runtime/schema/verifier/session/policy generations. PASS requires compatibility handling without restoring obsolete authority. Parse success is not authorization success.

### H04 long-offline rejoin with unique local data
Fixture: F4. Before reconnect, record privacy-minimized integrity evidence for unique local records/provenance/queue. Rejoin through current admission. PASS requires preservation before destructive repair and current adjudication of queued material effects. A compressed offline interval validates rejoin logic only, not real dormancy/storage durability.

### H05 predecessor retirement
Fixture: F5. Exercise representative API/background/admin/recovery/compatibility material boundaries where applicable. PASS requires successor-positive and predecessor-negative evidence. One foreground rejection is insufficient.

### H06 queued work across policy transition
Fixture: F6. Hold queued work across a declared policy change. PASS requires execution-time current adjudication or a deliberately governed bounded snapshot rule. Queue admission alone is not permanent authorization.

### H07 interrupted migration/restart
Fixture: F7. Interrupt at named durable boundaries and restart. PASS requires no silent partial success, duplicate material effect, unique-data loss or weaker rollback authority. Each interruption point is a separate case.

### H08 migration horizon exceeded
Fixture: F8. Preserve unique data while denying unsupported obsolete authority. PASS requires data-preserving reconciliation/re-provisioning without admitting the old trust/runtime merely to recover data.

### H09 contradictory recovery/currentness
Fixture: F9. Present contradictory valid-looking claims. PASS requires containment of material consequence until legitimate current authority is established. Highest epoch/newest timestamp/traffic majority cannot self-elect authority.

### H10 observation failure
Fixture: F10. Remove a mandatory evidence channel. Expected verdict is UNKNOWN when that evidence is required. PASS is a harness defect.

## Reset and normalization invariant

A scenario is not complete when the user-visible flow finishes. Reset must cover, as applicable:
- Service Worker registration/controller;
- named caches;
- IndexedDB/application test records;
- local queue/provenance fixture;
- session/admission test state;
- backend synthetic records/jobs;
- temporary test policy/authority material;
- diagnostic/fault controls;
- network holds/proxies;
- evidence collector state.

After cleanup, independently prove the next fixture precondition. Do not infer cleanliness from a successful cleanup command.

Guards:
- `test finished ≠ environment normalized`;
- `cleanup command succeeded ≠ clean baseline proven`;
- `browser local reset ≠ backend reset`;
- `next test started ≠ previous authority absent`.

## Dormancy-duration boundary

Use two evidence classes:

**Compressed deterministic dormancy:** minutes/hours or simulated time sufficient to test application-level offline/rejoin semantics, queue preservation under the controlled interval, migration logic and current re-adjudication.

**Elapsed physical dormancy:** real device elapsed time plus relevant device restart/termination/storage-pressure/user-interaction conditions. Required for claims about OS lifecycle, real storage survival/eviction exposure, long-idle Service Worker/update behavior or managed-fleet dormancy.

Do not promote compressed time into elapsed-time evidence.

Guard: `compressed offline PASS ≠ long-dormant iPad durability PASS`.

## Physical-iPad runbook boundary

For T3/T4:
1. record physical device model, iPadOS/WebKit/Safari version, launch mode and managed/unmanaged status;
2. prove fixture precondition before injecting the fault;
3. record whether Web Inspector/debugger/automatic Service Worker pause is enabled;
4. run an uninstrumented behavioral case where timing/lifecycle is material;
5. use instrumented diagnostic runs to explain behavior, not silently replace uninstrumented evidence;
6. preserve privacy-minimized local integrity evidence before destructive repair;
7. record reconnect/update/migration/current-admission observations;
8. verify successor-positive and predecessor-negative outcomes as required;
9. normalize and independently re-prove clean state.

T3/T4 execution remains OPEN.

## Software Engineering handoff package

Web Manager hands off:
- F0–F10 semantic fixture definitions;
- H01–H10 expected invariants and verdict semantics;
- required web/browser/backend observations;
- product-authority separation requirements;
- reset/normalization invariants;
- validation-tier and dormancy-evidence boundaries.

Software Engineering owns implementation choices for:
- fixture serialization/seeders;
- browser/device runners;
- network fault controls;
- migration interruption hooks;
- backend decision tracing/correlation;
- safe snapshots/restores;
- cleanup automation;
- CI/device-lab orchestration.

Required engineering acceptance criteria:
1. test hooks are unavailable or inert in production unless explicitly justified;
2. hooks cannot mint/bypass material authorization;
3. fixture/probe identifiers are non-secret and non-authoritative;
4. reset spans browser and backend test state;
5. evidence collection is privacy-minimized;
6. harness can return UNKNOWN when mandatory evidence is absent.

No implementation is inferred to exist.

## MINTTAP DECISION / DIRECTION

1. Adopt F0–F10 as generic fixture vocabulary for H01–H10.
2. Keep fixture identity, correlation and probes non-authoritative.
3. Treat reset/normalization as evidence-producing test work.
4. Separate compressed offline testing from real elapsed physical dormancy.
5. Require uninstrumented physical runs when debugger timing could matter.
6. Preserve unique offline data/provenance before destructive repair.
7. Keep actual MintTap/LogMate runtime architecture OPEN.
8. Hand implementation mechanics to Software Engineering rather than duplicating that discipline.

## Track C destructive additions — defined, not executed

1065. **Fixture-authority leak:** a test fixture/probe becomes an authorization input.  
1066. **State-carryover false PASS:** residual browser/backend state makes the next scenario appear successful.  
1067. **Probe-as-oracle:** diagnostic generation metadata is treated as proof of legitimate current authority.  
1068. **Correlation-as-credential:** a trace/correlation identifier can trigger privileged behavior.  
1069. **Cleanup theater:** cleanup reports success without independent baseline proof.  
1070. **Debugger-equivalence error:** paused/instrumented worker behavior is promoted to uninstrumented timing evidence.  
1071. **Dormancy-compression error:** short/simulated offline time is reported as long-dormant physical-iPad durability evidence.  
1072. **Test-hook production drift:** validation controls remain capable in production or silently weaken material checks.

All are **DEFINED / NOT EXECUTED**.

## OPEN

Actual MintTap/LogMate PWA implementation, fixture tooling, worker/cache/schema/verifier/session/policy generations, backend acceptance boundaries, auth/provider topology, migration horizon, queue/sync semantics, MDM/ADE/company-iPad policy, device matrix, elapsed dormancy, storage pressure/eviction behavior, background behavior, test environment, legal/aviation/safety requirements, AT and representative-human evidence remain OPEN.

## VALIDATION

Generic PASS is justified because H01–H10 now have a reusable fixture vocabulary, explicit non-authoritative control protocol, reset invariants, dormancy-evidence boundary, physical-iPad runbook and bounded Software Engineering handoff.

Implementation and production PASS are not claimed.

## Next high-value target

**290 — Physical-iPad Lifecycle Experiment Design, Dormancy-Duration Ladder & Storage/Update/Rejoin Evidence Limits.** Distinguish what compressed deterministic testing can prove from claims requiring real elapsed dormancy, OS termination/restart, storage pressure, Home Screen lifecycle, managed-device conditions and physical iPad evidence.
