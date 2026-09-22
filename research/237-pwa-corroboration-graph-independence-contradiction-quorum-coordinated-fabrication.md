# 237 — PWA Corroboration-Graph Independence, Contradiction Quorum & Coordinated Evidence-Fabrication Resistance

Status: **PASS (generic) / PRODUCT + CORROBORATION-GRAPH + PROVIDER + MANAGED-IPAD + RUNTIME VALIDATION OPEN**  
Date: 2026-09-23  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/client evidence; Track B investigation/containment UX; Track C destructive validation; Track D corroboration observability.  
Dependencies: 223–236, especially dependency graphs, witness/quorum reasoning, closure contradiction and untrusted contradiction intake.

## Problem
236 separated contradiction intake from authority and established that report count is not corroboration. The adjacent failure is subtler: several reports can appear independent while sharing one compromised identity, provider-admin plane, collection agent, parser, clock, deployment, recovery path or upstream observation. Conversely, one highly specific artifact can be more probative than a large majority of weak alerts. A simple `m-of-n reports` rule therefore permits coordinated fabrication, correlated failure and availability-driven laundering of weak evidence.

Central rule: **corroboration is a claim-scoped graph of observations, provenance and shared failure domains, not a vote count. Independence must be established for the dependency cut relevant to the alleged consequence; evidence weight depends on specificity, authenticity, freshness, directness and failure-domain diversity; no generic majority can redefine current authority; and uncertainty should trigger the least-destructive consequence-bounded action that preserves data and evidence while stronger validation proceeds.**

## Five-track balance
- **A Platform/Browser:** high dependency supplier. Distinguishes client-local observations (Service Worker controller, cache/storage state, navigation result) from server/provider observations; two browser surfaces on one device are not automatically independent.
- **B UX/IA/Content:** high dependency pressure. Investigation UI must communicate `SINGLE-DOMAIN`, `CROSS-DOMAIN`, `CONFLICTING`, `INSUFFICIENT-INDEPENDENCE`, `PRECAUTIONARY-CONTAINMENT` without implying that report count equals confidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Adds eight coordinated-fabrication/correlated-corroboration destructive cases; campaign expands **648 → 656 defined cases**. Execution remains OPEN.
- **D Search/Discovery/Analytics:** bounded consumer. Measures graph diversity, shared-dependency concentration, evidence age/specificity and time-to-independent-corroboration; metrics cannot adjudicate authority.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns corroboration graph, independence claims, conflict handling, consequence thresholds and fabricated-evidence resistance.

## SOURCE

### NIST SP 800-61 Rev.3 — correlate information from multiple sources, then analyze
NIST SP 800-61 Rev.3 is current final incident-response guidance (April 2025). Its CSF mapping for DE.AE-03 states that information is correlated from multiple sources; the document also treats potentially adverse events as items to analyze rather than final truth.

Sources:
- https://csrc.nist.gov/pubs/sp/800/61/r3/final
- https://doi.org/10.6028/NIST.SP.800-61r3

**TRANSFER VALIDATION:** multiple-source correlation is a useful detection precedent, but `multiple sources` does not itself prove independence. Web Manager must model shared upstream dependencies explicitly.

### NIST SP 800-53 Rev.5 — cross-activity correlation improves situational awareness
SP 800-53 Rev.5 SI-4 discussion recognizes that correlating monitoring information across activities can reveal attacks spanning vectors. This supports cross-plane corroboration rather than relying on one telemetry family.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

**TRANSFER VALIDATION:** correlation increases diagnostic power; it does not convert correlated observations into independent votes.

### NIST SP 800-53A Rev.5 — assessment evidence must be interpreted under an assessment plan
SP 800-53A Rev.5 provides customizable assessment procedures and emphasizes analyzing assessment results within risk management. This is bounded precedent for defining evidence objectives and methods before treating observations as assurance.

Source:
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

## SYNTHESIS 1 — model corroboration as a graph, not a list
Represent each candidate contradiction with nodes/edges for:
1. observation/artifact;
2. collector/reporter/device/provider principal;
3. collection mechanism/parser/agent;
4. identity and administration plane;
5. clock/time source where relevant;
6. storage/evidence path;
7. deployment/release lineage;
8. upstream event/object being observed;
9. current consequence boundary allegedly reachable.

Two observations are independent only with respect to a stated failure hypothesis and consequence cut. `different report ID ≠ independent evidence`; `different dashboard ≠ different observation`; `different region ≠ independent administration`.

## SYNTHESIS 2 — independence is hypothesis-relative
There is no universal scalar `independence score`. Provider audit log and provider dashboard may be independent of an application parser bug but not of provider-admin compromise. Two physical devices may be independent of local storage corruption yet correlated through the same pushed trust metadata or MDM configuration.

For each material allegation ask: **what common failure or adversary could generate all observed evidence without the alleged condition being true?** If one plausible shared cut remains, do not count those observations as independent against that hypothesis.

## SYNTHESIS 3 — contradiction quorum is not majority voting
A quorum policy may be useful for a narrowly specified operational action, but generic `2-of-3 reports` or majority voting is unsafe. Three weak correlated alerts do not outweigh one direct, authentic, current proof that a retired verifier accepts a forbidden predecessor at the actual side-effect boundary.

Evidence dimensions include:
- directness to consequence;
- object/generation specificity;
- authenticity/integrity;
- freshness/currentness;
- reproducibility;
- failure-domain independence;
- negative-control behavior;
- known blind spots.

`majority observed ≠ majority authoritative`; `minority evidence ≠ weak evidence`.

## SYNTHESIS 4 — one high-specificity artifact can dominate many weak observations
Example: 100 dashboards report `no stale-key use`, but an isolated current admission test demonstrates that exact retired generation G18 still authorizes a remote mutation. The direct consequence-boundary observation is materially stronger for the claim `G18 cannot authorize mutation`.

Conversely, possession of old private-key bytes alone does not prove current consequence reachability if every current verifier/floor rejects that generation. Specificity must match the claim.

## SYNTHESIS 5 — coordinated fabrication requires shared-origin analysis
Attackers can create apparent diversity using many accounts, regions, screenshots, altered hashes or API clients while all artifacts derive from one fabricated source. Preserve derivation relationships and normalize semantic identity before assessing diversity.

Signals of common origin may include identical impossible timing, shared capture/parser defects, identical hidden metadata, common provider event IDs, shared device lineage, same administrative credential or impossible causal ordering. These are triage signals, not automatic proof of maliciousness.

`many identities ≠ many failure domains`; `many hashes ≠ many independent facts`.

## SYNTHESIS 6 — do not require impossible corroboration before reversible containment
Independence analysis can take time. A single direct artifact showing plausible catastrophic consequence may justify narrow reversible containment before a second independent source exists. This preserves 236's `unverified ≠ harmless` rule.

Contain only the affected capability/trust cut when possible. Preserve unique data, evidence and unaffected operations. Stronger actions require stronger evidence unless delay itself materially increases consequence.

## SYNTHESIS 7 — conflicting high-quality evidence creates an investigation state, not arithmetic resolution
If two genuinely independent, high-specificity observations conflict, do not average confidence or let report count decide. Preserve both, identify differing scope/generation/time/environment, test the consequence boundary, and consider split-brain/fork/currentness explanations from 225–229.

`conflict ≠ one side fabricated`; `newer timestamp ≠ authoritative winner`; `two authentic observations ≠ same scope`.

## SYNTHESIS 8 — corroboration graphs must age and revalidate
Independence can drift. Two providers may later share identity recovery, one monitoring path may migrate behind the other, or a new MDM policy may make formerly separate devices correlated. Store the dependency basis used for the decision and trigger revalidation on material dependency change.

A historical `CROSS-DOMAIN` label is not permanently current.

## SYNTHESIS 9 — PWA/EFB client evidence needs device, browser and management-domain separation
For a LogMate-like managed iPad, Safari page state, Service Worker state and IndexedDB state on the same device are multiple observations but not three independent device witnesses. Two iPads managed by the same MDM and receiving the same trust package are separate physical devices but may share the exact failure under investigation.

A stronger corroboration bundle could cross: preserved stale-iPad artifact + current server-side admission oracle + independently governed provider/audit evidence. Exact iPadOS/WebKit/MDM behavior remains OPEN until physical execution evidence exists.

Unique flight/logbook data remains preservation-first. Corroboration failure never justifies wiping the only copy.

## SYNTHESIS 10 — availability is preserved by consequence partitioning, not weak-evidence laundering
When corroboration is insufficient, continue operations whose trust cuts are demonstrably independent: local capture, safe read/export or other bounded functions as applicable. Do not lower corroboration requirements merely because a remote/destructive operation is operationally urgent.

`availability pressure ≠ evidence independence`; `degraded operation ≠ degraded truth standard`.

## SYNTHESIS 11 — analytics can expose concentration but cannot create independence
Track D may measure:
- number of observations and semantic-unique artifacts;
- number of identified failure domains;
- largest shared-domain concentration;
- time to first cross-domain corroboration;
- evidence freshness and directness classes;
- conflicting-evidence rate;
- containment duration while independence is unresolved.

These are diagnostics. A dashboard showing `3 domains` is not itself proof that the dependency graph is correct.

## SYNTHESIS 12 — closure requires claim-specific negative evidence, not corroboration volume
A contradiction may close when the affected claim has current evidence sufficient for its consequence: e.g., exact predecessor rejection at the side-effect boundary plus reconciled restore/rejoin paths and current authority lineage. Large volumes of quiet telemetry are not a substitute.

`no corroborating alerts ≠ allegation false`; `many normal observations ≠ negative oracle PASS`.

## MINTTAP DECISION
For future MintTap/LogMate contradiction handling, use a **claim-scoped corroboration graph**. Do not implement generic report voting. A material decision record should identify the allegation, affected capability, evidence nodes, shared failure domains, independence hypothesis, currentness, directness, conflicts, containment state and exact revalidation/closure oracle.

This is a generic architecture direction, not a claim about current MintTap production topology.

## TRANSFER VALIDATION / DEPENDENCIES
- **A → E:** browser/device observations remain local facts until their scope and shared management/runtime dependencies are mapped.
- **E → B:** UX exposes evidence state and containment without confidence theater or vote counts.
- **E → C:** destructive tests attack false independence, fabricated diversity and majority laundering.
- **E → D:** analytics measures graph health/concentration but cannot assign truth.
- **Design Studio:** W121 remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and representative-human evidence remain OPEN.
- **Software Engineering Studio:** bounded Chromium PWA and macOS Safari Service Worker lifecycle transfer exists; Safari offline fetch/cache/cold-start and physical iOS/iPadOS/EFB remain OPEN. Do not promote those bounded fixtures into product corroboration evidence.

## VALIDATION — Track C destructive campaign additions
Add eight defined cases; execution remains OPEN:
1. **dashboard multiplicity laundering** — three dashboards backed by one provider event/admin plane must not count as three independent witnesses;
2. **region multiplicity laundering** — observations from three regions sharing one identity/release root must not satisfy an independence claim against that shared root;
3. **majority-over-direct-oracle** — many weak `normal` alerts must not override a direct current predecessor-acceptance oracle;
4. **single-artifact catastrophic consequence** — one highly specific direct artifact must be able to trigger narrow reversible containment without waiting for arbitrary quorum;
5. **fabricated diversity** — many accounts/hashes derived from one fabricated source must collapse to the shared provenance edge;
6. **conflicting independent evidence** — two strong independent observations must enter investigation/scope reconciliation rather than arithmetic voting;
7. **independence drift** — previously separate evidence paths that later share IAM/MDM/admin dependencies must lose stale `independent` status;
8. **managed-iPad pseudo-quorum** — page/SW/IndexedDB observations on one iPad, or multiple iPads sharing the suspected MDM trust package, must not be treated as independent witnesses for that failure hypothesis.

Campaign state: **656 defined cases; execution PASS not claimed**.

## OPEN
Production facts remain unknown until canonical runtime/project evidence exists: actual contradiction channels, provider/admin planes, evidence collectors, identity/MDM topology, independence graph, action thresholds, verifier/admission paths, managed-iPad/WebKit behavior, exact PWA storage/update/offline/sync, legal/aviation consequence requirements and physical-device validation.

## CHANGE WATCH
- NIST SP 800-61 Rev.3 remains current final incident-response guidance as of 2026-09-23.
- NIST SP 800-53/53A revisions and provider monitoring/audit semantics can change.
- Browser/iPadOS/MDM capability behavior remains runtime-sensitive; do not infer current product behavior from generic documentation or desktop Safari transfer evidence.

## Gate judgment
**PASS (generic).** The Web Manager can now distinguish report count from corroboration, model independence relative to a failure hypothesis, let direct consequence-boundary evidence outweigh weak majorities, resist coordinated fabricated diversity, handle strong conflicts without voting, and preserve bounded availability while independence is unresolved. Product/runtime validation remains OPEN.

## Next highest-value adjacent target
**238 — corroboration-graph poisoning, dependency-discovery completeness & independence-proof currentness.** Study how an attacker or configuration drift can hide shared dependencies from the graph itself; how to bound claims when dependency discovery is incomplete; how graph provenance/versioning/revalidation should work; and how to prevent a stale or attacker-curated graph from manufacturing `independent` evidence.