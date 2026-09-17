# 106 — PWA Release Compatibility Contracts, Retirement Proof & Data-Preserving Unsupported States

Status: **PASS (generic) / PRODUCT SUPPORT HORIZON + TARGET-RUNTIME VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 091 long-offline compatibility as indexed; 098 stale-client revocation; 100–105 recovery/release chain; Track A service-worker/client-generation mechanics; Track B unsupported/recovery UX; Track C compatibility/fault evidence; Track D privacy-bounded fleet evidence; Software Engineering D003/D005/D006/Q003/Q006.

## Purpose

105 established that release rollback does not imply durable-state rollback and that long-offline clients make rollout completion an evidence problem. This study closes the next generic boundary: **what must remain compatible, what evidence is sufficient to retire an old contract, and what must happen when a long-offline authoritative client returns after its normal compatibility horizon has ended?**

This is not a generic API-versioning primer and does not select MintTap/LogMate numeric support periods, mandatory-update deadlines, schema frameworks, key schedules, server topology or managed-iPad behavior.

---

## 1. Track balance and allocation

- **A Platform/Browser — dependency supplier.** Installed service-worker registrations and clients can outlive a deployment event; browser update mechanics do not guarantee fleet convergence.
- **B UX/IA/Content — major consumer.** `deprecated`, `update required`, `online action unavailable`, `records preserved`, `export/recovery available`, and `unsupported` must be truthful and distinct.
- **C Performance/Accessibility/Quality — major evidence consumer.** Owns compatibility matrix execution, old-artifact restore, stale-client reconnect, degraded-state accessibility and regression oracles.
- **D Search/Discovery/Analytics — bounded consumer.** Deprecation/fleet evidence must not infer absent offline clients are gone or justify unnecessary stable identifiers.
- **E Architecture/Security/Operations — primary owner.** Owns compatibility contract, retirement gate, bridge lifetime, emergency exceptions and unsupported-state policy.

**Allocation:** E remains highest-risk because premature retirement can strand authoritative local data. A/C are critical dependencies. B consumes the resulting state contract. D remains bounded.

---

## 2. SOURCE — deprecation and sunset are different lifecycle signals

RFC 9745 (Standards Track, March 2025) defines the HTTP `Deprecation` response header. Deprecation informs consumers that a resource will be or has been deprecated; **deprecation itself does not change resource behavior**. It can be accompanied by a `deprecation` link relation to migration/documentation material.

RFC 9745 explicitly distinguishes deprecation from `Sunset`: RFC 8594's `Sunset` header can signal when a resource is expected to become unresponsive. RFC 9745 requires a Sunset timestamp, when both are present, not to precede the Deprecation timestamp.

Sources:
- https://www.rfc-editor.org/rfc/rfc9745.html
- https://www.rfc-editor.org/rfc/rfc8594.html

**SYNTHESIS:** lifecycle communication has at least three states: preferred/current → deprecated-but-operational → retired/non-operational. Treating deprecation as immediate failure removes the migration window; treating sunset as merely documentation risks clients continuing after service withdrawal.

**Guards:**
- `deprecated ≠ non-operational`;
- `sunset announced ≠ every client received the announcement`;
- `sunset date reached ≠ stale authoritative local data expendable`;
- `deprecation header emitted ≠ migration completed`.

**CHANGE WATCH:** RFC 9745 is current Standards Track evidence as of 2026-09-17. Deprecation/Sunset are HTTP-resource lifecycle signals; they do not define a complete offline-PWA recovery policy.

---

## 3. Compatibility is a multidimensional contract, not one app version

A device-authoritative PWA can depend simultaneously on:
1. **reader contract** — can current code read old local records/backups?
2. **writer contract** — can it write a representation safely consumable by supported readers?
3. **schema/domain contract** — are field meanings, invariants, tombstones and identifiers preserved?
4. **sync protocol contract** — can old/new clients express operations without ambiguity or duplication?
5. **API contract** — will server endpoints accept the supported client's requests and response semantics?
6. **trust/key contract** — can the client validate current authority and access/recover its legitimate data?
7. **worker/shell/cache contract** — can installed page/worker/resource generations coexist safely?
8. **backup/import contract** — can supported recovery artifacts still be decrypted, parsed, validated and reconciled?
9. **bridge/native handoff contract** — are cross-context/native links/messages still accepted safely?

A semantic app version is only a label over this vector.

**Guards:**
- `app version supported ≠ every dependent generation compatible`;
- `API responds 2xx ≠ operation semantics compatible`;
- `schema parses ≠ domain meaning preserved`;
- `old reader works ≠ old writer remains safe`;
- `new reader accepts old data ≠ old client can safely accept new server semantics`.

---

## 4. Define support as an explicit compatibility envelope

A retirement policy should identify an **applicability envelope**, not simply “N-2”. Useful dimensions are:
- client/document build generation;
- service-worker/cache generation;
- local schema/data generation;
- protocol/API generation;
- trust/key generation;
- backup format generation;
- target browser/OS/support class;
- offline duration/reconnect path where relevant.

A product may choose N/N-1/N-2 as an operational shorthand, but that shorthand is safe only if it maps to tested combinations. A client that skipped ten releases may still possess a schema explicitly supported by a migration bridge; conversely an N-1 client can be unsafe after a security/trust break.

**MINTTAP DIRECTION (generic):** publish/encode support policy in terms that engineering and recovery tests can map to actual generations. Do not make semantic-version distance the sole retirement oracle.

---

## 5. Retirement requires positive proof, not disappearance from telemetry

A contract should not be removed merely because old clients stopped appearing. Long-offline clients are systematically under-observed.

Generic retirement evidence should answer:
1. **replacement readiness:** is a supported successor path available and tested?
2. **migration/recovery readiness:** can the oldest declared supported state reach a current safe state?
3. **artifact restore:** can backups from the retiring generation still be recovered through the declared path?
4. **outbox/reconciliation:** can pending operations from that generation be identified and reconciled without blind replay?
5. **trust/key continuity:** can legitimate stale clients re-establish current authority without accepting revoked authority?
6. **unsupported containment:** if direct sync is no longer allowed, are local records preserved and is a safe export/recovery path available where promised?
7. **communication:** has deprecation/sunset been communicated through channels the applicable client can actually observe when online?
8. **observability limits:** are unobserved/offline cohorts represented as UNKNOWN rather than zero?
9. **security exception:** is continued compatibility itself unsafe because of a known vulnerability or compromised authority? If so, is a data-preserving recovery path retained?

**Guards:**
- `zero observed old clients ≠ zero old clients`;
- `migration code exists ≠ oldest supported artifact migrates correctly`;
- `replacement endpoint live ≠ stale outbox safely translatable`;
- `support window elapsed ≠ recovery obligation automatically disappears`.

---

## 6. Contract → deprecate → restrict → retire → recover

A safer generic lifecycle is:

### Phase 0 — Current
Contract is preferred and fully supported.

### Phase 1 — Deprecated but operational
Signal deprecation; provide successor/migration guidance; collect bounded compatibility evidence. Do not silently change semantics merely because the deprecation signal exists.

### Phase 2 — Restricted legacy
Stop new dependency formation and optional legacy capabilities where safe. Keep the minimum reader/migration/recovery bridge needed for declared supported stale states. Old writers may be disabled before old readers if writes could create ambiguous or insecure state.

### Phase 3 — Normal retirement
Withdraw ordinary online operation only after retirement evidence passes. Preserve the declared recovery/export/migration route for legitimate stale authoritative data where product policy promises it.

### Phase 4 — Recovery-only compatibility
A retired client may be denied normal sync yet allowed a narrow, current-authority-mediated recovery path: update/upgrade, isolated import, export, reconciliation or support-assisted recovery. Recovery authority must not revive obsolete session/device/trust credentials.

### Phase 5 — End of recovery support
Only after explicit product/legal/security policy and evidence; do not infer this from API shutdown alone. Exact obligations are product/jurisdiction-specific and OPEN.

**SYNTHESIS:** ordinary runtime compatibility and recovery compatibility can have different lifetimes. Keeping a narrow recovery reader/importer longer than a writable legacy API can reduce attack surface while avoiding silent data loss.

---

## 7. Reader/writer asymmetry is a useful retirement tool

Compatibility need not be symmetric.

Examples:
- a current client can retain a **reader/migrator** for old schema while refusing to emit old schema;
- a server can reject obsolete write semantics while still offering a bounded migration/reconciliation endpoint;
- a backup importer can read an old artifact into quarantine without restoring obsolete credentials or immediately replaying its outbox;
- an old client can be allowed local read/export while online mutation/sync is blocked pending update.

This supports expand→migrate→contract evolution from 105.

**Guards:**
- `legacy write disabled ≠ legacy data unreadable`;
- `normal sync retired ≠ recovery import must be retired simultaneously`;
- `reader retained ≠ obsolete authority retained`;
- `recovery endpoint exists ≠ unrestricted legacy API required`.

---

## 8. Long-offline stale client reconnect protocol

A returning client should not jump directly from network reachability to replay.

Generic order:
1. identify local build/schema/protocol/trust/outbox generations without exposing sensitive record content;
2. obtain current trusted policy/authority;
3. classify client as normal-supported / migration-required / recovery-only / security-blocked / unknown;
4. preserve local records/outbox before mutation;
5. if migration-required, use tested forward path and re-evaluate trust/protocol compatibility;
6. reconcile remote acknowledgement/tombstone/conflict state;
7. authorize only operations expressible safely under current semantics;
8. quarantine ambiguous operations rather than dropping or blind-replaying them;
9. surface truthful user state and recovery/export choices;
10. record privacy-bounded outcome evidence.

**Guards:**
- `network reachable ≠ compatibility established`;
- `client authenticated ≠ protocol supported`;
- `update required ≠ local records invalid`;
- `unsupported for sync ≠ unsupported for local read/export/recovery`;
- `operation cannot be translated ≠ operation may be discarded`.

---

## 9. Service Worker mechanics constrain retirement claims

Service-worker registrations persist independently of individual page objects, and update checks/install/activation do not imply every old controlled client has converged immediately. `ServiceWorkerRegistration.update()` checks for a changed worker script, but browser update mechanics are not fleet-retirement proof.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration
- https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update

**TRANSFER VALIDATION from Track A:** origin-side removal of old resources or deployment of a new worker cannot prove an installed offline client has received deprecation, migrated state or released old cached dependencies.

**Guards:**
- `origin no longer serves legacy shell ≠ no legacy installed client exists`;
- `worker update available ≠ client updated`;
- `client updated ≠ local schema/protocol/trust migration complete`.

---

## 10. Security-driven retirement is exceptional but still data-preserving

Sometimes continued legacy compatibility is itself unsafe: compromised signing/trust authority, exploitable parser, broken authentication/session semantics, or protocol behavior that cannot be safely translated.

In that case ordinary deprecation periods may be shortened or bypassed. But security urgency should narrow **authority**, not erase legitimate local evidence.

Preferred containment hierarchy where technically possible:
1. deny unsafe remote mutation/bridge;
2. revoke obsolete credential/authority;
3. require current trusted update/rebootstrap;
4. preserve local records and recovery artifact;
5. use isolated/quarantined migration with current code;
6. reconcile before replay;
7. destroy data only under explicit product/user/legal policy, not as a side effect of incompatibility.

**Guards:**
- `legacy protocol vulnerable ≠ legacy records malicious`;
- `credential revoked ≠ record ownership erased`;
- `security retirement accelerated ≠ destructive reset justified`.

---

## 11. B — truthful unsupported-state UX contract

An unsupported client must not collapse all states into “update required.” The UI requirements should distinguish, when true:
- normal use supported;
- online sync/update required but records are saved locally;
- compatibility migration required;
- recovery-only mode;
- security-sensitive online capability blocked;
- export/recovery available;
- some pending operations require review;
- support required because automatic recovery cannot be proven safe.

Never promise “nothing will be lost” without restore/migration evidence. Never imply local records were synchronized merely because update completed.

**DEPENDENCY:** exact interaction/copy/accessibility implementation belongs to Design Studio/product content. Web Manager owns truthful state requirements.

---

## 12. C — retirement proof campaign

Future exact-product evidence should include at least:
1. oldest declared supported client → current server normal path;
2. oldest supported schema/backup → current reader/migrator;
3. client one generation beyond normal support → recovery-only path;
4. long-offline client that never received deprecation signal;
5. old worker/cache controlling while API contract enters deprecation;
6. deprecated endpoint remains behaviorally stable until intended restriction;
7. Sunset reached while client has unsynced local records;
8. old writer disabled while old reader/export remains available;
9. old backup containing obsolete credentials imported without credential revival;
10. stale outbox with already-applied remote operation;
11. stale update reordered after delete/tombstone;
12. trust/key generation retired while records remain decryptable/recoverable through current authority;
13. unknown/unrecognized generation enters quarantine rather than destructive migration;
14. recovery-only endpoint cannot be used as unrestricted legacy API;
15. security emergency bypasses normal timeline but preserves local records;
16. no telemetry from long-offline cohort is reported as UNKNOWN;
17. keyboard/zoom/screen-reader semantics for unsupported/recovery state;
18. target Safari/WebKit/Home Screen behavior on managed iPad;
19. exact artifact/build/worker/schema/protocol identifiers bound to results;
20. regression mutant silently drops an old field and is killed by semantic oracle.

**DEPENDENCY:** Software Engineering Q006 provides `fault point → recovery action → independent terminal-state oracle → regression sensitivity`; D003/D005/D006/Q003 constrain schema/restore/replay/interleaving. No PWA runtime PASS is inferred from those studies.

---

## 13. D — deprecation/retirement measurement without surveillance

Useful evidence can include coarse build/schema/protocol/support class, deprecation-observed state, migration/recovery outcome and error class. It should not require record content, backup filenames, tokens/keys or unnecessary stable device identity.

A denominator problem remains: disconnected clients cannot report themselves. Therefore observed fleet distributions are evidence about **observed clients**, not proof of total installed-fleet extinction.

**Guards:**
- `observed migration rate high ≠ all authoritative clients migrated`;
- `deprecation telemetry absent ≠ deprecation received`;
- `retirement analytics useful ≠ stable user/device tracking necessary`.

---

## 14. Cross-repository transfer

### Design Studio
Canonical Web Design status checked 2026-09-17: Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED. W057 freezes adjacent theory and requires executable W053/W056 evidence with screenshot, semantics/accessibility tree, focus trace, logs, task result and automated accessibility evidence. No browser/Safari/screen-reader/device PASS is imported.

### Software Engineering Studio
Canonical global status checked 2026-09-17: every specialist remains Foundation IN STUDY. Q006 and D003/D005/D006/Q003 are methodology/semantics dependencies only. M002 separately reinforces that lifecycle/background opportunity is not durable-state correctness, but native mobile evidence is not browser/PWA evidence.

**CONTRADICTION CHECK:** neither repository supplies target managed-iPad retirement proof, so product validation remains OPEN.

---

## 15. MINTTAP / LogMate bounded direction

For a LogMate-like EFB with authoritative local records, “unsupported” should default to **unsupported online contract**, not “records disposable.” A stale client may need a current-code recovery bridge even after its ordinary API/writer contract is retired. The narrowest safe recovery capability is preferable to indefinite unrestricted legacy operation.

For MintTap, actual production data authority, PWA deployment, API, schema, worker and backup topology were not inspected in this run. Do not transfer the EFB authority model to MintTap production without project evidence.

No support duration, N-k horizon, mandatory-update interval, Sunset date, retention duration or recovery-only lifetime is selected here.

---

## 16. Retirement decision record template

Before retiring a recovery-relevant contract, record:
- contract/resource/generation being retired;
- preferred successor;
- deprecation date and communication surfaces;
- planned ordinary-operation sunset;
- oldest supported input/artifact/client state;
- reader vs writer vs sync vs recovery support after sunset;
- migration/recovery evidence IDs bound to exact artifacts;
- long-offline/unknown cohort treatment;
- security exception rationale if accelerated;
- local-data preservation behavior;
- outbox/reconciliation behavior;
- accessibility/degraded-state evidence;
- observability limitations;
- rollback/forward-repair relationship;
- final authority approving end of recovery support.

This is governance evidence, not a claim that HTTP headers alone enforce retirement.

---

## 17. CHANGE WATCH

Re-evaluate when:
- HTTP Deprecation/Sunset standards materially change;
- browser/Service Worker update behavior changes;
- iOS/iPadOS Home Screen/MDM support changes;
- actual product API/schema/key/backup/support policy is available;
- security incidents force accelerated retirement;
- legal/records-retention obligations become applicable;
- target-device runtime evidence changes the feasible recovery path.

---

## 18. Gate assessment

**FOUNDATION:** PASS — deprecation, sunset, compatibility envelope and recovery support are distinguished.  
**PRACTITIONER:** PASS — reader/writer/API/protocol/schema/key/backup/worker contracts and lifecycle phases can be diagnosed.  
**ADVANCED:** PASS — long-offline clients, security retirement, recovery-only compatibility, outbox reconciliation and telemetry bias are integrated.  
**EXPERT JUDGMENT:** PASS (generic) — a retirement-proof gate and data-preserving unsupported-state model can be defended without inventing product thresholds.

**PRODUCT VALIDATION:** OPEN — exact support horizon, server/API behavior, worker/cache generations, schema/key/backup compatibility, managed-iPad runtime, accessibility and real recovery evidence remain unknown.

## 19. Next adjacent boundary

The next high-value generic question is **compatibility-bridge minimization and attack-surface debt**: retaining old readers/migrators/recovery endpoints prevents data stranding but expands parser/protocol/security surface. Determine how to keep recovery compatibility narrow, isolated and testable; how to retire vulnerable legacy parsers without losing old artifacts; and how bridge debt enters security/change governance. Consume Software Engineering parser/data evidence rather than rebuilding implementation theory.