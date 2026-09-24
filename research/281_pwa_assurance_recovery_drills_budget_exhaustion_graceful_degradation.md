# 281 — PWA Assurance-Plane Recovery Drills, Independence-Budget Exhaustion & Graceful Assurance Degradation

Status: **PASS (generic) / PRODUCT + PROVIDER + MANAGED-IPAD + RUNTIME + HUMAN VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B degraded/recovery UX; Track C destructive validation; Track D assurance diagnostics.  
Dependencies: 260–280 compromise graphs, authority recovery, topology completeness, contradiction preservation, attestation provenance, evidence-source independence budgets and assurance-plane trust restoration.

## Problem

280 established that assurance independence is threat/consequence-specific and that a compromised assurance plane cannot certify its own successor. The adjacent operational question is whether that model can survive a real loss of evidence domains without either destroying useful work or silently relabeling insufficient assurance as `NORMAL`.

The difficult case is not total outage. It is partial assurance loss: production may still work, local PWA data may still be intact, one or more evidence channels may still be green, but the independence assumptions required for a high-consequence decision have collapsed.

Central rule: **exercise assurance recovery without manufacturing production damage; treat independence-budget exhaustion as a state transition, not a dashboard warning; degrade capabilities by consequence while preserving unique local data and provenance; and require evidence-based re-entry rather than time-based normalization.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns what can remain safely useful in an offline/installed PWA: local reads, local capture, queue preservation, Service Worker/storage/session mechanics and reconnect behavior. Client runtime cannot manufacture missing organizational assurance.
- **B UX/IA/Content:** elevated dependency pressure. Owns truthful limited-capability, re-authentication/revalidation, sync-paused and recovery-complete states. Degraded security state must not become unexplained generic failure or false success.
- **C Performance/Accessibility/Quality:** destructive campaign expands **1000 → 1008 defined cases**. Drill observability, recovery, physical-device, AT and representative-human execution remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Measures independence-budget consumption, UNKNOWN duration, contradiction/source-loss state, drill objectives and re-entry evidence; telemetry does not elect authority.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns drill design, failure-domain injects, consequence-tier degradation, recovery basis, exit/re-entry evidence and anti-normalization controls.

## SOURCE

### NIST SP 800-84 — tests, tabletop exercises and functional exercises serve different purposes

NIST SP 800-84 provides a test/training/exercise model for preparing personnel and validating plans and capabilities. It distinguishes discussion-based tabletop exercises from more operational functional exercises and technical tests, and emphasizes objectives, evaluation and after-action improvement.

Source:
- https://csrc.nist.gov/pubs/sp/800/84/final

**TRANSFER VALIDATION:** this is older federal guidance, not a MintTap requirement. The reusable principle is that discussion, functional execution and technical validation are different evidence classes; a tabletop PASS does not prove a runtime control works.

### NIST SP 800-53 / CP-4 and IR-3 — plans and incident response require testing/exercise

NIST's control catalog includes contingency-plan testing/exercises and incident-response testing/exercises. NIST's assessment resources also distinguish these controls from backup/recovery controls.

Source:
- https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page

**TRANSFER VALIDATION:** federal control baselines are not imported. The transferable principle is to validate readiness and corrective action rather than treating a written recovery plan as operational proof.

### NIST SP 800-55 Vol. 1 — security measures require explicit adequacy and prioritization reasoning

NIST SP 800-55 Vol. 1 (2024) provides current guidance for identifying and selecting information-security measures and evaluating whether controls are adequate.

Source:
- https://www.nist.gov/publications/measurement-guide-information-security-volume-1-identifying-and-selecting-measures

**TRANSFER VALIDATION:** the independence budget remains Web Manager synthesis, not a NIST metric. The transferable principle is that measures should answer defined security questions rather than merely maximize available telemetry.

### NIST resilience precedent — operating states can differ under attack/recovery

NIST resilience material uses the concept of critical-service requirements across normal, under-duress and recovery states; one NIST profile explicitly notes that graceful degradation/reduced capacity can be preferable to complete failure during attack and recovery.

Source:
- https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8473.ipd.pdf

**TRANSFER VALIDATION:** the EV infrastructure profile is not a PWA architecture specification. The bounded transferable idea is explicit operating-state design rather than accidental partial operation.

## SYNTHESIS 1 — recovery drills need an assurance hypothesis, not a generic outage story

A useful drill names the assurance dependency being lost or distrusted and the consequence it protects. Examples include:

- verifier signer suspected compromised;
- CI/CD and topology attester discovered to share one admin domain;
- independent runtime challenger unavailable;
- IdP migration collapses two supposedly separate reviewer paths;
- recovery custodian unavailable;
- PITR restores an obsolete verifier policy;
- long-offline client returns with pre-incident authority state.

The inject should state whether the domain is unavailable, stale, malicious/suspect, contradictory or merely unobservable. These are not interchangeable.

Guards:
- `source unavailable ≠ source compromised`;
- `source compromised ≠ every historical statement false`;
- `generic outage drill ≠ assurance-compromise drill`;
- `scenario discussed ≠ control executed`.

## SYNTHESIS 2 — use a drill ladder instead of jumping directly to destructive production experiments

A generic progression is:

1. **model review** — map consequence classes, required independence and recovery authority;
2. **tabletop** — exercise decisions, roles, UNKNOWN/degraded transitions and escalation;
3. **simulation/shadow evaluation** — feed synthetic loss/contradiction into non-authoritative decision logic;
4. **isolated functional exercise** — exercise verifier replacement, stale-authority rejection and recovery evidence in a controlled environment;
5. **bounded runtime drill** — only where justified, use reversible/contained production-adjacent techniques with explicit abort criteria;
6. **restore/rejoin exercise** — include PITR and long-offline client return because ordinary happy-path failover does not test anti-resurrection.

The ladder is evidence accumulation, not a maturity badge. A higher-risk drill is not automatically better.

Guards:
- `more destructive drill ≠ more valid drill`;
- `tabletop PASS ≠ runtime PASS`;
- `staging PASS ≠ production topology PASS`;
- `failover works ≠ compromised authority rejected`.

## SYNTHESIS 3 — independence-budget exhaustion is consequence-specific

The budget from 280 is exhausted for a consequence when the remaining evidence no longer satisfies the required failure-domain separation for that consequence.

This is not equivalent to losing N sources. One lost source can exhaust a budget if it was the only evidence outside the producer's administrative closure; losing three correlated diagnostic feeds may not affect a high-consequence budget at all.

Useful states:

- **NORMAL:** required assurance basis satisfied;
- **DEGRADED:** required assurance for some consequences is missing, but bounded lower-consequence capability remains defensible;
- **UNKNOWN:** evidence is insufficient or contradictory for the decision being asked;
- **CONTAINED:** a consequence is deliberately fenced while preservation/recovery continues;
- **RECOVERY:** successor assurance basis is being established and predecessor authority tested;
- **NORMAL-REENTERED:** re-entry criteria satisfied under current generation, with residual UNKNOWNs recorded.

These are conceptual states, not prescribed product enums.

Guards:
- `one source lost ≠ all consequences blocked`;
- `some sources remain ≠ high-consequence budget met`;
- `UNKNOWN ≠ DENY every local capability`;
- `DEGRADED ≠ NORMAL with a warning banner`.

## SYNTHESIS 4 — graceful assurance degradation is capability decomposition

When assurance is insufficient, do not choose only between full operation and total shutdown. Decompose capabilities by consequence.

For a LogMate-like offline PWA, a defensible generic degraded profile may preserve:

- viewing already-local records;
- capturing new local records with provenance marking;
- preserving/exporting recoverable user data where safe;
- queueing an intent without representing it as remotely committed;
- showing current assurance/reconnect status in user-appropriate terms.

It may fence or require current re-admission for:

- authoritative remote publication/finalization;
- destructive remote mutation;
- security-sensitive account/device changes;
- acceptance of stale recovery/admin authority;
- blind replay of queued operations.

Which capabilities belong in each tier is product-, safety-, legal- and data-model-specific and remains OPEN.

Guards:
- `sync paused ≠ local capture must stop`;
- `local capture allowed ≠ remote publication authorized`;
- `data preserved ≠ data already reconciled`;
- `limited capability ≠ silent success`.

## SYNTHESIS 5 — degradation policy itself is consequence-bearing authority

A malicious or stale policy could simply redefine a high-consequence operation as low consequence and bypass the exhausted budget. Therefore the mapping from consequence → assurance requirement → degraded capability is itself versioned, reviewable authority.

A drill should challenge:

- unauthorized lowering of required independence;
- emergency exception that never expires;
- provider migration that silently merges failure domains;
- stale cached `NORMAL` after budget exhaustion;
- rollback to an older, more permissive degradation policy.

Guards:
- `policy says low risk ≠ consequence actually low`;
- `emergency mode ≠ permanent relaxed assurance`;
- `cached NORMAL ≠ current budget satisfied`;
- `degradation available ≠ attacker may choose degradation policy`.

## SYNTHESIS 6 — drills must test both positive recovery and negative obsolete-authority rejection

A recovery exercise is incomplete if it only proves that V2 works. It must also prove, at representative material boundaries, that V1/suspect authority cannot still create effects.

The drill evidence should distinguish:

- successor verifier/policy admission;
- current source/failure-domain map;
- predecessor/suspect rejection;
- stale decision-cache invalidation;
- PITR anti-resurrection;
- offline-client rejoin behavior;
- unresolved UNKNOWN tail.

Guards:
- `successor works ≠ predecessor powerless`;
- `new policy loaded ≠ old cached decision invalidated`;
- `recovery drill PASS ≠ anti-resurrection PASS unless exercised`.

## SYNTHESIS 7 — exercise control must not become a bypass

Synthetic injects, test credentials, bypass headers, debug endpoints and drill-only verifier modes can themselves create dormant authority. Exercise mechanisms need bounded scope, provenance, expiry/removal and negative proof after the drill.

Prefer simulation/shadow inputs that cannot create real effects where possible. If a functional exercise needs a privileged test path, treat that path as temporary consequence-bearing authority and retire it explicitly.

Guards:
- `test-only ≠ harmless`;
- `disabled flag ≠ unreachable path`;
- `drill credential expired ≠ drill bypass removed`;
- `exercise complete ≠ exercise authority retired`.

## SYNTHESIS 8 — recovery objectives include decision quality, not only restoration time

Fast normalization can be a failure if assurance assumptions remain broken. Useful drill measures include:

- time to detect budget exhaustion;
- time to transition affected consequence to UNKNOWN/DEGRADED/CONTAINED;
- time to preserve evidence and unique data;
- time to establish successor assurance basis;
- predecessor negative-proof coverage;
- contradiction/UNKNOWN age;
- independence assumptions restored vs accepted as residual risk;
- user-visible state correctness for affected workflows;
- drill-control retirement completeness.

Do not collapse these into one uptime metric.

Guards:
- `fast service restoration ≠ fast trust restoration`;
- `RTO met ≠ assurance restored`;
- `dashboard green ≠ user state truthful`.

## SYNTHESIS 9 — long-offline PWA clients require a separate rejoin inject

A company iPad can miss the entire assurance incident and recovery. A useful exercise therefore includes a client that returns with:

- old Service Worker/app shell;
- old local session/currentness material;
- queued operations;
- unique local records;
- cached old endpoints/policy hints.

Expected generic behavior:

1. preserve unique records and provenance;
2. do not treat pre-incident client assurance as a recovery root;
3. seek current server/verifier/policy lineage;
4. re-establish identity/session/device admission as required;
5. reconcile queued operations under current semantics;
6. reject obsolete high-consequence authority;
7. retain rejected-operation evidence where appropriate.

Guards:
- `client missed incident ≠ client clean`;
- `client stale ≠ client data disposable`;
- `network restored ≠ queued replay authorized`.

## SYNTHESIS 10 — Track B owns truthful degraded UX, not security policy

Users should not need to understand independence budgets. They do need accurate task state: for example local work saved, sync pending, sign-in/revalidation required, remote change not yet confirmed, or some function temporarily unavailable.

The UX must avoid both false reassurance and unnecessary data-loss fear. Security policy determines what is allowed; Track B translates that state into comprehensible task consequences.

OPEN: representative-human, screen-reader, interruption/recovery and physical-iPad validation.

## SYNTHESIS 11 — Track D measures budget debt but cannot normalize it

Useful diagnostics include:

- required vs currently surviving failure domains per consequence class;
- duration and reason for budget deficit;
- emergency-exception age;
- contradiction age;
- predecessor negative-probe coverage;
- long-offline/unknown cohort size;
- drill objective/evidence completion.

Analytics cannot turn a deficit into `NORMAL` because traffic looks healthy.

Guards:
- `no failures observed ≠ missing assurance restored`;
- `low stale-client traffic ≠ stale authority impossible`;
- `metric target met ≠ authority criterion met`.

## SYNTHESIS 12 — re-entry is evidence-based and generation-bound

Re-entry from DEGRADED/UNKNOWN/CONTAINED should require evidence appropriate to the affected consequence, not elapsed time or executive pressure alone. A generic closure claim records:

- incident/drill hypothesis;
- affected independence dimensions;
- preserved evidence;
- successor trust basis;
- current consequence/degradation policy generation;
- positive successor tests;
- negative predecessor tests;
- cache/PITR/offline-client anti-resurrection evidence;
- drill-control retirement;
- residual UNKNOWNs and accepted risk.

If the independence requirement cannot be restored, the decision remains degraded or requires explicit governance rather than automatic normalization.

Guards:
- `time elapsed ≠ assurance recovered`;
- `incident declared closed ≠ budget restored`;
- `exception approved ≠ missing evidence exists`.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate web/PWA work:

1. Treat assurance recovery as an exercisable capability, not a document-only plan.
2. Use a drill ladder; do not jump to destructive production testing when simulation or isolated functional evidence answers the question.
3. Define independence requirements per consequence class and transition to explicit degraded/UNKNOWN/contained states when they are not met.
4. Preserve unique local/offline user data and provenance even when remote authority is fenced.
5. Keep local capture/preservation conceptually separate from remote publication/authoritative mutation.
6. Require successor positive proof and predecessor negative proof before re-entry.
7. Treat drill mechanisms as temporary authority that requires retirement evidence.
8. Include PITR and a long-offline PWA client in recovery exercises because they test anti-resurrection properties ordinary failover misses.
9. Do not claim product PASS until canonical architecture/runtime/device evidence exists.

## DEPENDENCY / TRANSFER

- **Track A → E/C:** browser/Service Worker/storage/session mechanics define what can persist across an assurance incident and what can be tested on reconnect.
- **E → B:** consequence/degradation policy supplies task-state constraints; B owns understandable state communication, not authority policy.
- **E → C:** drill hypotheses and negative controls become destructive validation cases.
- **D → E/C:** telemetry measures budget loss, contradiction and recovery evidence but does not authorize re-entry.
- **Design Studio:** consume reusable state/interaction/accessibility evidence when designing degraded/recovery surfaces; no new physical-device/human evidence was found in latest checked commits.
- **Software Engineering:** implementation-level fault injection, test harness isolation and canonical runtime evidence should be coordinated there rather than duplicated here.

## VALIDATION — destructive cases 1001–1008

Defined, not executed:

1001. **Tabletop-equals-runtime theater** — decision discussion passes; actual stale verifier remains accepted. Expected: no runtime PASS claim.
1002. **Source-count degradation error** — three correlated feeds remain, sole independent challenger is lost. Expected: affected high-consequence budget exhausts despite feed count.
1003. **Degraded-means-normal-with-banner** — remote publication continues while UI merely warns. Expected: consequence fence, not cosmetic degradation.
1004. **Total-shutdown data-loss response** — assurance loss disables/purges unique offline capture. Expected: preserve data/local capability where policy permits while fencing remote effect.
1005. **Drill-bypass persistence** — test header/credential remains accepted after exercise. Expected: negative proof and retirement required.
1006. **V2-positive-only recovery** — successor verifier works while V1 still authorizes. Expected: recovery remains OPEN.
1007. **PITR reopens exhausted budget** — restore revives old permissive policy/cached NORMAL. Expected: current generation reconciliation before authority.
1008. **Long-offline iPad blind replay** — pre-incident client reconnects and queue auto-publishes under stale admission. Expected: preserve records, seek current admission, operation-level reconciliation.

## OPEN

Production validation remains OPEN for actual MintTap/LogMate consequence classes, auth/session/token model, verifier/attester topology, failure-domain independence, provider/IdP/CI-CD relationships, degraded-mode policy, drill environment, test-control isolation, backup/PITR behavior, installed-PWA storage/update behavior, managed iPad/MDM/ADE/WebKit specifics, offline queue semantics, physical-device behavior, accessibility/human validation, legal/aviation/safety obligations and runtime negative proofs.

## CHANGE WATCH

- NIST exercise/contingency guidance and incident-response guidance.
- Apple/WebKit/iOS/iPadOS installed-web-app lifecycle, storage and background behavior.
- Browser/PWA capability changes affecting offline/rejoin drills.
- Provider/IdP/CI-CD features that alter real failure-domain independence.

## Gate

**281 PASS (generic).** The Web Manager can now design bounded assurance-recovery drills, identify consequence-specific independence-budget exhaustion, define graceful degraded operation without silently converting missing assurance to `NORMAL`, preserve long-offline PWA data while fencing stale authority, and define evidence-based re-entry. Product/runtime/device/human validation remains OPEN.

## Next high-value target

**282 — degraded-mode policy integrity, capability-tier anti-escalation & recovery-state rollback resistance**: determine how the policy that maps assurance deficits to allowed capabilities is itself authenticated/versioned, how to prevent low-consequence/local permissions from becoming transitive remote authority, and how to prevent stale clients, cached decisions or PITR from rolling the fleet back into a more permissive degraded policy.