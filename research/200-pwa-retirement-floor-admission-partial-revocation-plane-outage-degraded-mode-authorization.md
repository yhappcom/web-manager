# 200 — PWA Retirement-Floor Admission Under Partial Revocation-Plane Outage, Fail-Safe Boundaries & Degraded-Mode Authorization

Status: **PASS (generic) / PRODUCT + IDENTITY + PROVIDER + REGION + MANAGED-IPAD + RUNTIME + SAFETY/LEGAL + HUMAN/AT VALIDATION OPEN**  
Date: 2026-09-21  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA disconnected mechanics; Track B degraded-state semantics and recovery UX requirements; Track C destructive assurance; Track D privacy-bounded outage telemetry.  
Dependencies: 171–199, especially 198–199.

## Problem
199 established that authority retirement is a distributed convergence problem. The adjacent failure is harder: a resource server, region or reconnecting PWA may need to decide what to do while the very plane that supplies current revocation/currentness evidence is partially unavailable.

A blanket `fail open` is unsafe because stale authority can silently outlive retirement. A blanket `fail closed` is also not a complete design principle because it can destroy useful offline operation, prevent local preservation of irreplaceable records, or turn a control-plane outage into an avoidable mission/business outage. The security question is therefore not “open or closed?” globally. It is: **which operation may proceed, against which data, with what authority source, for how long, under which previously admitted floor, and with what reconciliation requirement?**

Central rule: **control-plane unavailability does not create authority. Degraded operation may preserve previously authorized/local capability, but it must not silently mint, extend, upgrade or resurrect authority whose current validity cannot be established.**

## Five-track balance
- **A Platform/Browser:** supplies Service Worker/offline/cache/session mechanics and distinguishes local computation/data preservation from server authorization. Browser connectivity signals are not authorization/currentness evidence.
- **B UX/IA/Content:** owns user/operator semantics for `LOCAL ONLY`, `DEGRADED`, `CURRENTNESS UNAVAILABLE`, `QUEUED / RE-ADMISSION REQUIRED`, and recovery. Reusable interaction design remains Design Studio-owned.
- **C Performance/Accessibility/Quality:** owns outage/fault-injection matrices, stale-cache tests, recovery-order tests and positive/negative authorization oracles. Physical Safari/iPadOS, AT and human validation remain OPEN.
- **D Search/Discovery/Analytics:** consumes coarse outage/recovery telemetry. Analytics cannot substitute for policy/currentness evidence and must not become a shadow authorization plane.
- **E Architecture/Security/Operations:** **highest-risk owner**; owns operation classification, degraded-mode authorization envelope, retirement-floor monotonicity, recovery admission and anti-extension rules.

## SOURCE

### NIST SP 800-53 Rev.5 — secure failure and recovery
Current SP 800-53 Rev.5 (Release 5.2.0 planning note dated 2025-08-27) remains the current control catalog. Its secure-failure/recovery engineering principle states that failure or recovery should not violate security policy; systems may continue in normal, degraded or alternative secure operations if security properties remain enforced, or shut down when they cannot.

Source: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** “fail secure” does not mean every function must become unavailable. It means degraded/recovery behavior must preserve the relevant security policy. MintTap/LogMate operation-specific policy remains OPEN.

### NIST SP 800-207 / NCCoE ZTA — decision and enforcement are distinct
NIST Zero Trust Architecture separates policy decision/administration from policy enforcement points. The policy engine decides grant/deny/revoke; enforcement points protect resources and enforce those decisions.

Sources:
- https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf
- https://pages.nist.gov/zero-trust-architecture/VolumeB/architecture.html

**TRANSFER VALIDATION:** this separation is useful for reasoning about a failed decision/currentness dependency versus a still-running enforcement point. It does not imply MintTap uses ZTA or prescribe a particular PDP/PEP product.

### RFC 7662 — cached authorization freshness is an explicit security/performance trade-off
RFC 7662 permits resource servers to cache introspection responses but warns that stale cached `active` state can permit a revoked token to remain usable. If an introspection response contains `exp`, it must not be cached beyond that time.

Source: https://www.rfc-editor.org/rfc/rfc7662.html

**TRANSFER VALIDATION:** an outage does not make a stale cached authorization result fresher. A cache may support a deliberately bounded degraded envelope only when its semantics and upper bound are known; it must not be extended merely because the live introspection/currentness service is unavailable.

## SYNTHESIS 1 — classify operations before choosing degraded behavior
Do not attach one fail-open/fail-closed rule to an entire application. Classify operations by consequence and authority need.

Generic classes:
1. **Local preservation:** write/edit unique local domain data without remote side effects. This can often remain available if local integrity rules hold.
2. **Local read/use:** read already-local data or perform local computation. Authorization/privacy requirements may still apply, but no new server authority is implied.
3. **Deferred intent:** record an intent locally for later server submission. The intent is not an accepted remote mutation; it requires future re-admission.
4. **Remote low-consequence read:** may be eligible for bounded cached authorization only if product policy explicitly permits it and freshness is bounded.
5. **Remote consequence-bearing mutation:** generally requires current-enough server-side authorization/currentness evidence appropriate to the risk. An outage must not convert stale evidence into current evidence.
6. **Authority/security administration:** role, credential, recovery, policy, custody, deletion/hold or similar authority-changing actions require stronger currentness and must not be enabled merely to improve availability.

**MINTTAP DIRECTION:** for a LogMate-like offline EFB, preserve local flight/logbook work and allow deferred intent where safe; do not equate offline usability with permission to perform remote consequence-bearing mutation under stale authority.

## SYNTHESIS 2 — use a degraded authorization envelope, not an outage exception
A degraded envelope should bind at least:
- admitted retirement/security generation or floor known before outage;
- operation/resource scope;
- authority evidence type and its verified validity bound;
- maximum degraded interval if one exists;
- whether operation is local-only, deferred, or remotely effective;
- whether new privilege/scope can be acquired (normally no);
- whether refresh/reissue is allowed;
- recovery/reconciliation requirements;
- telemetry/evidence requirements that do not themselves become authority.

Persistent guards:
- `authorization service unavailable ≠ previous authorization renewed`;
- `cached active=true ≠ current active=true`;
- `degraded mode enabled ≠ stale authority promoted`;
- `offline local save ≠ remotely admitted mutation`;
- `queue accepted locally ≠ server accepted operation`;
- `availability pressure ≠ permission to lower retirement floor`.

## SYNTHESIS 3 — outage must not extend a previously verified bound
If authority was valid only until `T`, loss of introspection/currentness at `T-1` does not create `T+Δ` authority. If a cache entry was valid for N seconds, the inability to refresh it does not justify resetting its age. If a retirement floor `R` was admitted, a restored region with `R-1` does not become acceptable because the central plane is down.

This is the anti-extension rule:

**A failure in the mechanism that could have supplied fresher authorization cannot increase the lifetime, scope, privilege or generation of the last trustworthy authorization evidence.**

If the architecture cannot establish a trustworthy bound, the affected remote authority is `UNKNOWN`, not implicitly usable.

## SYNTHESIS 4 — distinguish local capability from remote authority
PWA architecture makes this distinction operationally important.

A Service Worker can serve an app shell; IndexedDB can retain local records; cached data can support local workflow; a UI can allow the user to create/edit records. None of these establish that the server would currently authorize a mutation.

For a disconnected LogMate-like iPad:
- preserve unique local records;
- identify local-only versus previously acknowledged records;
- retain queued intent with idempotency/provenance needed for later reconciliation;
- display state that does not imply server acceptance;
- never advance server/currentness floor from a client-local clock, Service Worker version, cached identity or queue age;
- on reconnect, obtain authenticated current server state and re-admit consequence-bearing queued work.

**CONTRADICTION:** destructive “logout cleanup” that erases unique unsynchronized records can satisfy an authentication goal while violating durability/recovery goals. Authorization quarantine and data preservation must be separable.

## SYNTHESIS 5 — fail-safe is operation-specific, not globally fail-closed
NIST secure-failure principles support continued degraded operation when security policy remains preserved. Therefore “fail closed” should mean **deny the operation whose required authorization property cannot be established**, not “crash or erase the entire application.”

Examples at generic level:
- live revocation/currentness unavailable + local draft save → potentially continue locally;
- live currentness unavailable + remote privilege escalation → deny;
- live introspection unavailable + cached low-risk read authorization still inside a verified bound → potentially continue only if policy explicitly permits that bounded mode;
- cached authority bound expired → deny remote use even if outage continues;
- retirement floor known as R + region restored at R-1 → quarantine consequence-bearing path until reconciled to at least R;
- unique local data + stale session → preserve data, reject stale remote authority, require reauthentication/re-admission later.

Exact classification is product/risk/legal/aviation dependent and remains OPEN.

## SYNTHESIS 6 — partial outage is more dangerous than total outage
A total outage is visible. A partial outage can produce split enforcement:
- Region A reaches current introspection; Region B relies on stale cache.
- RP A receives logout; RP B misses it.
- API mutation path requires live currentness; background worker uses a cached authorization snapshot.
- foreground PWA reauthenticates while a stale Service Worker queue retries with retired credentials.

Therefore degraded-mode state must be evaluated per **consequence-bearing enforcement domain**, not inferred from global health or one successful endpoint.

A useful status model:
- `NORMAL` — required currentness dependencies available and current floor enforced;
- `DEGRADED-BOUNDED` — explicitly permitted operation within a verified prior bound;
- `LOCAL-ONLY` — local preservation/use with no claim of remote admission;
- `RE-ADMISSION REQUIRED` — intent/data preserved but remote consequence pending current authority;
- `QUARANTINED` — enforcement domain cannot safely establish required floor/currentness;
- `UNKNOWN` — evidence insufficient to bound the authority state.

## SYNTHESIS 7 — recovery is a forward convergence ceremony
When revocation/currentness dependencies return, do not simply clear a global `degraded` flag.

Generic recovery sequence:
1. keep unique local data and pending intent preserved;
2. authenticate the recovered currentness/revocation plane;
3. obtain current admitted retirement/security generation `Rcurrent`;
4. compare each region/resource server/RP with `Rcurrent`;
5. invalidate or age out stale authorization caches according to verified semantics;
6. run negative retired-authority probes and positive current-authority probes on consequence-bearing domains;
7. reconcile PITR/restored regions before reopening them;
8. rebootstrap reconnecting PWA clients forward;
9. re-admit queued consequence-bearing work under current authority;
10. only then return each scoped domain from `DEGRADED/QUARANTINED` to `NORMAL`.

Persistent guard: **`revocation plane recovered ≠ enforcement plane converged`.**

## SYNTHESIS 8 — availability design belongs upstream of the outage
If a product needs high availability for consequence-bearing operations, the answer is not to improvise fail-open during an incident. Design beforehand for an independent-enough/current-enough authorization path, bounded token/session semantics, replicated enforcement evidence, or a product-specific degraded capability that preserves security properties.

Redundancy itself must be checked for correlated identity/KMS/network/provider/control-plane dependencies. `two authorization services ≠ two independent failure domains` remains applicable.

**DEPENDENCY — Software Engineering:** actual implementation requires concrete auth/session/token/provider state machines, cache TTLs, request paths, background workers, region topology, queue semantics and fault injection. Software Engineering Studio remains Foundation-stage; its current Android/Chromium/Keystore evidence does not establish Safari/iPadOS/EFB behavior.

## SYNTHESIS 9 — degraded-mode UX must not lie about authority
Track B requirements consumed from E:
- distinguish `saved on this device` from `synced/accepted`;
- distinguish `service unavailable` from `permission denied` where disclosure is safe;
- do not label queued work `complete` before server admission;
- expose recovery/retry state without encouraging repeated destructive submissions;
- do not promise a reconnection time from a security validity bound;
- preserve accessibility of degraded/recovery state announcements.

Design Studio remains canonical for reusable interaction patterns. Current Design Studio Web evidence is Stage 3 PRACTICE / NOT PASSED, so these are requirements, not validated UX solutions.

## SYNTHESIS 10 — observability must identify degraded enforcement domains without becoming authority
Useful evidence can include:
- revocation/currentness dependency availability;
- last successfully observed admitted floor per enforcement domain;
- age of cached authorization evidence;
- number of operations shifted to local-only/deferred/quarantine;
- stale-client reconnect/re-admission outcomes;
- negative retired-authority and positive current-authority probe outcomes.

Do not infer authorization from analytics delivery, operator dashboard freshness or absence of denied requests. Minimize personnel identifiers and sensitive token/session detail in telemetry.

## Track C destructive campaign — 360 cases total
Add eight high-value cases to the 352-case campaign:
1. introspection becomes unavailable one second before cached authorization expires; resource server must not reset/extend the cache age;
2. central currentness plane is down while Region A has floor R and Region B has R-1; B is quarantined for consequence-bearing operations rather than lowering R;
3. local PWA can create a unique flight record during outage, but remote queue admission remains pending and record survives forced reauthentication;
4. foreground session is reauthenticated after recovery while stale Service Worker/background queue retries retired authority; server rejects stale authority and preserves queued domain data for controlled re-admission;
5. all retired-authority probes fail because the service itself is down; positive current-authority oracle also fails, preventing false security-convergence PASS;
6. a low-consequence read is explicitly permitted under a verified cached bound; the same authority is rejected for a higher-consequence mutation;
7. PITR restores a healthy-looking region with pre-retirement floor; health check passes but admission remains blocked until current floor reconciliation and paired authorization probes pass;
8. revocation plane recovers but one RP/resource server remains on stale state; global incident status cannot promote that enforcement domain to NORMAL.

Campaign status: **DEFINED, NOT EXECUTED**. Provider/IAM, physical iPad/Safari/Home Screen, AT, representative-human and canonical product-runtime execution remain OPEN.

## Cross-track transfer / contradiction checks
### A → E
Offline/cache mechanics explain persistence of stale observations. **CONTRADICTION:** `navigator.onLine`, Service Worker state, IndexedDB contents or client clock cannot prove current server authorization.

### E → B
B receives degraded-state semantics and the requirement to separate local preservation, deferred intent and remote acceptance. It must not invent a visual pattern as evidence of correct authorization.

### E → C
C must fault-inject partial rather than only total outages, test expiry edges, stale regions/background paths and pair negative retired-authority probes with positive current-authority probes.

### E → D
D may measure degraded-domain duration and recovery coverage but cannot define authorization truth from analytics events.

### Design Studio dependency
`progress/WEB_STATUS.md` is W121 / Stage 3 PRACTICE / NOT PASSED. Physical-device/PWA, screen-reader and representative-human UX evidence remains OPEN.

### Software Engineering dependency
`progress/STATUS.md` remains Foundation study underway with no specialist Foundation PASS. Current bounded Android/Chromium/Keystore evidence does not transfer to iOS/Safari/EFB or canonical product authorization behavior.

## OPEN
- actual MintTap/LogMate identity/federation/provider architecture;
- whether OAuth/OIDC/introspection exists at all;
- actual operation consequence classes and aviation/legal/safety constraints;
- actual token/session/cache validity bounds and provider outage semantics;
- actual region/resource-server enforcement topology;
- actual background-worker/Service-Worker queue credentials and retry behavior;
- actual managed-iPad/WebKit offline/session/storage behavior;
- actual acceptable degraded duration and business continuity objective;
- actual PITR/recovery reconciliation implementation;
- human/AT comprehension of local-only/deferred/quarantined states.

## CHANGE WATCH
- Provider-specific token/session revocation and outage semantics.
- WebKit/iPadOS PWA background/session/storage behavior.
- OAuth/OIDC specifications and provider conformance behavior.
- NIST control-catalog updates after SP 800-53 Release 5.2.0.

## Gate judgment
**PASS (generic).** The Web Manager can now reason about partial revocation/currentness-plane failure without collapsing into a global fail-open/fail-closed binary; classify operations by consequence and authority requirement; define bounded degraded envelopes that cannot extend stale authority; preserve PWA local utility/data independently from remote mutation authority; and specify forward convergence after control-plane recovery.

This is not production certification. Product/provider/runtime/managed-iPad/safety/legal/privacy/human evidence remains OPEN.

## Adjacent-value check and next highest-value target
The directly adjacent question is now **degraded-authorization lease provenance, trusted-time dependence & partition-duration uncertainty**. The next cycle should determine how a system proves the age/validity of a cached authorization lease when clocks drift or are attacker-controlled, how server-issued expiry/currentness evidence survives partitions without client clocks becoming authority, and how recovery handles operations created near or across an uncertain lease boundary without silently converting UNKNOWN into authorized history.