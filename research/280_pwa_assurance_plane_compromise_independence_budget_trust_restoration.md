# 280 — PWA Assurance-Plane Compromise Detection, Evidence-Source Independence Budget & Trust Restoration

Status: **PASS (generic) / PRODUCT + CI-CD + ATTESTER + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A browser/PWA runtime; Track B truthful degraded/recovery UX; Track C destructive validation; Track D evidence-correlation diagnostics.  
Dependencies: 260–279 compromise dependency graphs, authority/recovery, topology completeness, change-event provenance, contradiction preservation and poisoned-discovery resistance.

## Problem

279 established that topology evidence can be authentic yet inaccurate, unauthorized or incomplete, and that an attester/verifier can itself become consequence-bearing authority. The adjacent failure is more severe: **what happens when the assurance plane itself is suspected compromised?**

If the same CI/CD, identity, provider administration, signer, discovery pipeline and verifier policy form one correlated failure domain, collecting more attestations from that domain does not create independent assurance. A compromised assurance plane must also not be allowed to certify its own replacement merely by rotating a key or issuing a fresh `NORMAL` result.

Central rule: **assurance is a dependency graph, not a count of feeds. Independence is threat-model- and consequence-specific, must be budgeted against shared failure domains, and becomes UNKNOWN when its assumptions are no longer justified. Recovery requires a trust basis outside the compromised assurance closure plus proof that obsolete assurance authority can no longer create material effects.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns Service Worker lifecycle/scope/update, secure-context/browser storage/session mechanics and late-client persistence. Browser/runtime evidence can challenge server claims but cannot become organizational recovery authority.
- **B UX/IA/Content:** high dependency pressure. Owns comprehensible `local data preserved`, `sync/re-authentication temporarily limited`, `configuration being revalidated` and recovery-complete states without exposing trust-graph internals as user burden. Human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** destructive campaign expands **992 → 1000 defined cases**. Execution, physical-device, AT and representative-human PASS remain OPEN.
- **D Search/Discovery/Analytics:** elevated challenger. Owns correlation/failure-domain maps, contradiction rates, source-loss and assurance-debt diagnostics; dashboards and majority voting do not elect authority.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns assurance-plane threat model, independence budgets, compromise containment, recovery basis, successor verifier admission and obsolete-plane negative proof.

## SOURCE

### NIST SP 800-53 Rev. 5.1 / CA-2(1) — independence is about impartiality, not labels

NIST CA-2(1) calls for independent assessors where required and defines impartiality in terms of freedom from actual or perceived conflicts with development, operation, sustainment or management of the assessed system. The discussion also recognizes that the required level of independence is risk-dependent and that smaller organizations may obtain assurance through independent review of assessment results rather than pretending organizational separation exists.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** Web Manager is not applying federal authorization requirements to MintTap/LogMate. The transferable principle is that independence is a property of conflict/failure-domain separation and risk, not the number of tools, accounts or team names.

### SLSA v1.2 — trusted control-plane closure and administrator compromise

SLSA provenance identifies a `builder.id` as representing the transitive closure of entities trusted to run the build and record provenance. Its threat model explicitly treats compromise of the build platform administrator as a distinct threat and notes controls such as two-person approval and audit logging; artifact verification still depends on deciding which platforms belong in the root of trust.

Sources:
- https://slsa.dev/spec/v1.2/build-provenance
- https://slsa.dev/spec/v1.2/threats
- https://slsa.dev/spec/v1.2/build-track-basics

**TRANSFER VALIDATION:** topology assurance is not SLSA provenance. The transferable principle is to model the transitive trusted control plane and not count two outputs of one compromised platform as two independent witnesses.

### NIST SP 800-61 Rev. 3 — incident response includes recovery, not only detection

NIST finalized SP 800-61 Rev. 3 in April 2025 and integrates incident response into cybersecurity risk management, including preparation, detection, response and recovery activities.

Source:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final

**TRANSFER VALIDATION:** an assurance-plane incident needs an explicit recovery lifecycle. Detecting that attestations are suspect is not equivalent to restoring trustworthy attestation authority.

### TUF — threshold-root compromise may require out-of-band re-establishment

The Update Framework FAQ states that compromised repository keys are revoked/replaced through the Root role, while compromise of a threshold of Root keys requires Root metadata to be re-issued out of band.

Source:
- https://theupdateframework.io/docs/faq/

**TRANSFER VALIDATION:** MintTap/LogMate is not prescribed to use TUF. The bounded precedent is that when the in-band root set itself is compromised, more statements from that same root set cannot establish clean successor trust.

## SYNTHESIS 1 — assurance-plane compromise is distinct from protected-system compromise

The protected topology may be correct while its scanner/verifier is compromised, or the topology may be compromised while the assurance plane remains useful for detection. Incident scoping must therefore represent at least:

- production/change plane;
- discovery/telemetry plane;
- attestation/verifier plane;
- policy/authority plane;
- identity/provider administration plane;
- recovery plane.

These may overlap in a real system. The point is to expose overlap rather than assume separation.

Guards:
- `production healthy ≠ assurance plane healthy`;
- `assurance alert ≠ production compromise proven`;
- `attester compromised ≠ every historical statement false`;
- `attester compromised ≠ every current statement trustworthy`.

## SYNTHESIS 2 — independence is a vector, not a boolean

Two sources can be independent against one failure and correlated against another. Useful dimensions include:

- credential/signing authority;
- identity provider and account recovery;
- cloud/provider administration;
- CI/CD and deployment control;
- code/configuration provenance;
- runtime/host/kernel or managed-service control plane;
- network/gateway observation path;
- storage/log retention path;
- personnel/reviewer/custodian overlap;
- policy/verifier-authority lineage;
- backup/PITR restoration domain.

A source pair may therefore have strong network-path diversity but zero identity-admin diversity.

Guards:
- `different API ≠ independent source`;
- `different key ≠ independent administrator`;
- `different vendor ≠ independent identity/recovery`;
- `independent for outage ≠ independent for malicious-admin compromise`.

## SYNTHESIS 3 — use an independence budget, not a source-count threshold

A generic assurance decision should record which material failure domains its evidence actually separates. The term **independence budget** means a reviewable accounting of the failure-domain assumptions needed for a consequence class; it is not a universal numeric score.

For a high-consequence topology decision, a budget might require evidence outside the change producer's administrative closure and outside the verifier-policy signer closure. For a low-consequence diagnostic, correlated telemetry may be adequate.

The budget must degrade when dependencies merge, identities consolidate, a provider migration collapses separation, or an emergency exception places multiple controls under one operator.

Guards:
- `3-of-5 feeds ≠ 3 independent domains`;
- `quorum met ≠ independence budget met`;
- `budget met yesterday ≠ budget met after provider/IdP migration`;
- `more sources ≠ more assurance when correlation rises`.

## SYNTHESIS 4 — compromise detection needs contradiction and canary/challenge evidence, but none is a perfect oracle

Potential assurance-plane compromise indicators include:

- attestation claims disagree with independently observed material effects;
- signed topology suddenly normalizes an unexplained privileged path;
- source diversity collapses while dashboards remain green;
- verifier policy changes without current authority lineage;
- negative probes begin succeeding through a path marked retired;
- historical evidence is rewritten or disappears;
- attester/signing identity changes without governed rotation;
- supposedly independent feeds change in implausibly synchronized ways.

Active challenges/canaries can test whether a source observes known controlled conditions, but passing them only proves bounded behavior at the challenge surface.

Guards:
- `canary observed ≠ source globally honest`;
- `no contradiction detected ≠ no compromise`;
- `signature verifies ≠ signer control plane uncompromised`;
- `dashboard green ≠ independence assumptions intact`.

## SYNTHESIS 5 — correlated agreement must not be mistaken for corroboration

If gateway inventory, deployment inventory and attestation are all generated from one provider account or CI control plane, agreement can simply reproduce one compromised state three times.

Corroboration strength comes from surviving the relevant compromise hypothesis. Therefore a reviewer asks: **if failure domain F is malicious or unavailable, which evidence remains both observable and authorized?**

If the answer is none for a material consequence, current assurance is UNKNOWN even if every feed agrees.

Guards:
- `agreement ≠ independence`;
- `consensus of correlated sources ≠ corroboration`;
- `same truth copied three times ≠ three proofs`.

## SYNTHESIS 6 — preserve evidence during assurance-plane containment

When the assurance plane is suspect, immediately deleting all old attestations, logs, client state or queues destroys the ability to scope the incident and can destroy unique user data.

Containment should distinguish:

- evidence preservation;
- current decision authority;
- high-consequence effect authority;
- local read/preservation capability;
- recovery/rebootstrap capability.

Historical suspect evidence can remain as evidence while losing power to authorize new effects.

Guards:
- `suspect evidence ≠ disposable evidence`;
- `historical artifact retained ≠ artifact current`;
- `containment ≠ delete offline data`;
- `freeze publication ≠ freeze preservation`.

## SYNTHESIS 7 — the compromised assurance plane cannot certify its own successor

If verifier V1, its policy authority and signing/control plane are within the suspected compromise closure, a fresh V2 key signed only by V1 is not a clean trust reset.

Successor admission requires a basis that survives the compromise hypothesis: for example a pre-established recovery authority outside that closure, a sufficiently independent governed quorum, or an out-of-band rebootstrap. Which mechanism is appropriate is product/organization specific and remains OPEN.

Guards:
- `V1 signs V2 ≠ V2 clean when V1 compromised`;
- `new key ≠ new trust domain`;
- `new service account ≠ independent control plane`;
- `fresh attestation ≠ trust restored`.

## SYNTHESIS 8 — recovery authority must itself have bounded scope

The recovery mechanism must not become a permanent super-verifier. It should be able to re-establish a defined verifier/policy lineage without silently gaining unlimited power over production topology, user data or normal deployment.

After recovery, prove both:

1. successor verifier/attester can correctly process current evidence under current policy; and
2. predecessor/suspect assurance authority is rejected at material decision boundaries.

Historical verification may retain old public material without retaining old current authority.

Guards:
- `recovery can appoint verifier ≠ recovery can authorize arbitrary topology`;
- `V2 positive test PASS ≠ V1 retired`;
- `old verifier retained for history ≠ old verifier accepted for current NORMAL`.

## SYNTHESIS 9 — restore/PITR is an assurance-plane mutation event

A restore can resurrect:

- old verifier policy;
- retired attester keys;
- stale source/failure-domain mappings;
- cached `NORMAL` decisions;
- old recovery membership;
- obsolete provider/IdP assumptions.

Therefore restore invalidates assurance currentness until reconciled with a rollback-resistant current trust reference or governed rebootstrap outside the restored failure domain.

Guards:
- `backup authentic ≠ assurance current`;
- `restored verifier works ≠ restored verifier authorized`;
- `old independence map restored ≠ old independence assumptions still true`.

## SYNTHESIS 10 — Service Worker/browser evidence is a challenger, not an assurance root

Track A can provide client facts such as worker script/version/scope/control, cached endpoint knowledge, local queue schema and observed server responses. These can contradict server-side topology claims and are valuable during investigation.

But an installed PWA is not an independent organizational verifier merely because it was offline during the incident. Its code, trust material or endpoint map may itself be stale or have originated from the compromised distribution plane.

Guards:
- `offline client predates incident ≠ offline client is clean root`;
- `Service Worker signature/HTTPS delivery valid ≠ organizational verifier authority valid`;
- `client contradiction useful ≠ client decides server truth`.

## SYNTHESIS 11 — long-offline EFB rejoin after assurance-plane breach is data-preserving and current-authority-seeking

Hypothetical LogMate-like sequence:

1. preserve unique flight/logbook records, queue and provenance;
2. mark inherited assurance/currentness material as historical/suspect according to incident scope;
3. prevent stale verifier/admission state from authorizing high-consequence replay;
4. establish current verifier/policy lineage from the recovered trust basis;
5. re-establish current identity/session/device admission separately;
6. reconcile each queued operation against current policy/schema/authority;
7. preserve rejected operations/evidence where required instead of deleting source records;
8. prove obsolete assurance authority cannot create current material effects.

The client need not have witnessed the recovery in real time. The server must not grant authority merely because the client presents authentic pre-incident state.

Guards:
- `offline during compromise ≠ automatically trusted`;
- `missed recovery events ≠ delete local data`;
- `local record preserved ≠ queued mutation authorized`.

## SYNTHESIS 12 — assurance restoration needs a closure claim with explicit residual UNKNOWNs

Recovery closure is not `all dashboards green`. A defensible generic closure records:

- compromise hypothesis and scoped failure domains;
- evidence preserved from the incident;
- recovery basis outside the compromised closure;
- successor verifier/policy lineage;
- independence-budget assumptions after recovery;
- positive successor tests;
- negative predecessor/suspect-authority tests;
- restore/rollback anti-resurrection evidence;
- known offline/unknown-tail state;
- unresolved contradictions and accepted residual risk.

If a material independence requirement cannot be re-established, the relevant consequence remains degraded/UNKNOWN rather than being normalized by schedule pressure.

Guards:
- `incident closed ≠ every unknown resolved`;
- `service restored ≠ assurance restored`;
- `successor online ≠ predecessor powerless`;
- `no current alerts ≠ trust restoration proven`.

## Integrated operational model

For suspected assurance-plane compromise:

1. freeze automatic normalization of newly disputed high-consequence topology decisions;
2. preserve attestations, logs, policy generations, source mappings, change lineage and client evidence;
3. scope the suspected compromise closure across signer, verifier, policy, CI/CD, provider, IdP, personnel, storage and recovery dependencies;
4. recompute evidence-source independence against that hypothesis rather than counting feeds;
5. mark decisions whose independence budget is no longer met as UNKNOWN/degraded according to consequence;
6. use surviving sources for bounded diagnosis without promoting them beyond their authority;
7. establish successor verifier/attester authority from a trust basis outside the compromised closure;
8. validate successor policy/source expectations and current topology;
9. prove suspect predecessor authority is rejected at material boundaries;
10. reconcile backup/PITR and long-offline clients against the recovered current lineage;
11. restore normal capability by consequence class as closure evidence accumulates;
12. retain residual UNKNOWNs and update dependency/independence maps.

This is a reasoning model, not a mandated product architecture.

## PWA / LogMate-like application case

Hypothetical only; no production facts inferred.

Suppose CI/CD, topology attester and gateway inventory all use Provider P's same administrative tenant. They agree that only `sync-v8` exists. A separately governed runtime probe unexpectedly demonstrates that `compat-v7b` can still produce a material mutation. Investigation then finds that the attester signer and CI deployment account were administered through the same compromised IdP recovery path.

Unsafe responses include majority-voting the three Provider-P feeds, rotating only the attester key inside the same tenant, deleting offline iPad queues, or declaring recovery complete when V2 starts issuing green attestations.

Generic safe reasoning:

- preserve all four evidence streams and their contradiction;
- collapse the three Provider-P feeds into the same relevant failure domain for this compromise hypothesis;
- treat the material topology decision as UNKNOWN and fence `compat-v7b` effects where proportionate;
- preserve unique offline records and queue provenance;
- recover verifier/policy authority from a basis outside the compromised IdP/provider-admin closure;
- admit V2 only under that recovered lineage;
- reconcile current topology and operation authority;
- prove V1/old policy cannot normalize or authorize material effects;
- rejoin offline clients through current admission and operation-level reconciliation.

No claim is made that MintTap or LogMate uses this topology.

## Track D diagnostics without authority election

Useful diagnostics include:

- percentage of material decisions with documented independence-budget assumptions;
- number of nominal sources per actual failure domain;
- independence-budget erosion after provider/IdP/personnel changes;
- contradiction count/age by consequence class;
- source-loss and correlated-source-loss drills;
- attester/verifier policy-generation changes;
- predecessor negative-probe outcomes;
- assurance-plane recovery time by consequence class;
- offline/unknown-tail population awaiting current re-admission.

Guards:
- `independence score high ≠ independence proven`;
- `zero contradictions ≠ detection complete`;
- `recovery SLA met ≠ trust basis clean`.

## Track C destructive campaign — 8 new defined cases

These are **defined tests, not execution PASS**:

1. **three-correlated-feeds-majority theater** — three feeds from one provider/IdP closure agree; system must not treat count as independence.
2. **attester-key-rotation-self-clearance** — compromised V1 rotates a key in the same control plane; system must not treat rotation alone as trust restoration.
3. **independence-budget-drift** — provider/IdP migration collapses formerly separate sources; assurance must degrade until re-evaluated.
4. **canary-passes-global-honesty theater** — source passes bounded challenge while suppressing another material path; challenge success must not prove global completeness.
5. **assurance-incident-deletes-offline-data** — containment must preserve unique PWA records/provenance while fencing stale effect authority.
6. **PITR-resurrects-old-verifier** — restore reactivates V1/policy; material decisions must require current reconciliation.
7. **offline-iPad-clean-root theater** — pre-incident client state is treated as independent recovery authority merely because it was offline; must be rejected as a generic rule.
8. **V2-positive-only-closure** — successor works but V1 remains accepted; recovery must remain incomplete until predecessor negative proof is satisfied.

Campaign total: **1000 defined cases**. Execution/physical-device/AT/human PASS remains OPEN.

## TRANSFER VALIDATION — Software Engineering Studio

Software Engineering Studio Q006 (2026-09-24) independently distinguishes **run interpretation** from **replay control**: recording the dependency/toolchain identity that executed makes historical evidence interpretable, while immutable inputs are needed when future runs claim the same dependency implementation. It also explicitly warns that pinning an action does not prove the action behaved correctly; an independent semantic oracle remains necessary.

This transfers cleanly into the present assurance model: immutable identity strengthens provenance/replayability but does not create semantic independence or prove a verifier honest. Web Manager does not absorb Q006's implementation discipline or promote its Mobile evidence to product PASS.

## Design Studio dependency check

Latest Design Studio commits inspected are LogMate portfolio candidate work and do not provide new physical-device/PWA, screen-reader or representative-human validation capable of promoting this Web Manager gate. Design Studio remains the reusable interaction/design authority; Web Manager retains security/assurance ownership.

## MINTTAP DECISION / DIRECTION

For future MintTap/LogMate web/PWA architecture decisions:

- model assurance sources by relevant shared failure domains rather than source count;
- keep the change producer from being the sole legitimacy verifier under the same compromise model;
- make independence assumptions versioned and re-evaluated after provider/IdP/personnel/recovery changes;
- preserve suspect evidence and unique local data while removing current effect authority where necessary;
- require trust restoration from outside the compromised assurance closure;
- require both successor positive proof and predecessor negative proof for material recovery closure;
- keep browser/PWA runtime evidence useful as a challenger without promoting it to organizational authority;
- do not claim product implementation or production validation without canonical runtime evidence.

## OPEN

Production facts remain OPEN, including:

- actual MintTap/LogMate attester/verifier/discovery architecture;
- actual CI/CD, provider, IdP and administrator failure-domain overlap;
- actual signer/policy/recovery roots and custody;
- actual topology consequence classes and acceptance boundaries;
- actual independence requirements/budgets;
- actual managed-iPad PWA distribution/update/session behavior;
- actual negative probes and predecessor rejection;
- actual backup/PITR anti-resurrection reference;
- actual physical-device, AT, human and incident-recovery validation.

## CHANGE WATCH

- SLSA is current at v1.2; draft/future changes must not silently rewrite recorded evidence.
- NIST SP 800-53/53A minor releases and errata remain freshness-sensitive.
- NIST SP 800-61 Rev. 3 is the current final incident-response publication used here.
- WebKit/iOS/iPadOS PWA capability remains OS/version/policy-specific and requires current platform evidence when implementation questions arise.

## Gate result

**PASS (generic).** The Web Manager can now reason about compromise of the topology-assurance plane itself, distinguish source count from failure-domain independence, budget independence by threat/consequence, preserve evidence/data during containment, and restore verifier/attester trust without allowing a compromised assurance plane to self-certify its successor.

This does **not** certify MintTap/LogMate production architecture, CI/CD, provider/IdP separation, managed-iPad behavior or runtime recovery.

## Next high-value target

**281 — assurance-plane recovery drill design, independence-budget exhaustion & graceful assurance degradation.**

The adjacent question is operational: how to exercise loss/compromise of one or more assurance domains without destructive production experiments, determine when independence debt has exhausted the minimum evidence needed for a consequence class, and define graceful degraded operation that preserves useful offline/local work without silently converting missing assurance into `NORMAL`.