# 268 — PWA Re-entry Prerequisite Attestation Integrity, Cross-Control Evidence Correlation & False-Composition Resistance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + RUNTIME + DOMAIN-AUTHORITY VALIDATION OPEN**  
Date: 2026-09-24  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Consumers: Track A runtime/evidence-source mechanics; Track B truthful re-entry UX; Track C destructive validation; Track D bounded correlation/coverage diagnostics.  
Dependencies: 122–126 assurance independence/oracle continuity, 260–267 dependency/completeness/topology/exception/re-entry governance.

## Problem

267 established consequence-scoped prerequisite graphs for staged re-entry. The next failure boundary is composition: every prerequisite can appear individually green while the combined high-consequence decision is still unsound because the attestations share a hidden failure domain, describe different epochs/scopes, depend circularly on one another, or were evaluated by a compromised/stale verifier.

Central rule: **a set of individually valid attestations is not automatically a valid composite re-entry proof. Composition must bind claim, subject/topology, consequence, policy/configuration epoch, evidence time, verifier/trust context, dependencies and correlation/failure-domain information; contradictions or missing composition prerequisites block only the affected consequence rather than laundering uncertainty into NORMAL.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Identifies which runtime facts actually come from browser/Service Worker/cache/storage/network surfaces and where several signals may derive from one source. Runtime currentness cannot authorize semantic re-entry.
- **B UX/IA/Content:** high dependency pressure. Must distinguish `prerequisites individually available`, `composition pending`, `evidence conflicted`, `revalidation required`, `limited consequence available`; exact interaction/human/AT validation remains OPEN.
- **C Performance/Accessibility/Quality:** high dependency pressure. Destructive campaign expands **896 → 904 defined cases**; execution PASS is not claimed.
- **D Search/Discovery/Analytics:** bounded observer/challenger. Can detect suspicious correlation, epoch skew, source concentration and contradiction rates, but analytics cannot elect authoritative truth or grant re-entry.
- **E Architecture/Security/Operations:** **highest-risk owner.** Owns composite-proof contracts, verifier/source independence requirements, contradiction handling, bounded challenge/revalidation and consequence-scoped closure.

## SOURCE

### NIST SP 800-53A Rev. 5 — assessment evidence supports objective determinations; assessment context matters

NIST SP 800-53A Rev. 5 provides assessment procedures for security/privacy controls and is current at Release 5.2.0 (2025-08-27). Its assessment model supports evidence-based determinations rather than treating a control label as self-proving.

Source: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

**TRANSFER VALIDATION:** supports explicit assessment evidence and claim boundaries. It does not define a PWA re-entry attestation format or require cryptographic signatures for every control result.

### NIST SP 800-137 / 800-137A — current control effectiveness and monitoring-program completeness are separate concerns

SP 800-137 frames continuous monitoring as ongoing visibility into assets, threats/vulnerabilities and deployed-control effectiveness aligned with risk tolerance. SP 800-137A evaluates both effectiveness and completeness of the monitoring program, including strategy, procedures, operations and analysis of monitoring data.

Sources: https://www.nist.gov/publications/information-security-continuous-monitoring-iscm-federal-information-systems-and  
https://csrc.nist.gov/pubs/sp/800/137/a/final

**TRANSFER VALIDATION:** supports checking whether evidence collection itself has adequate coverage and remains current. A green observed control does not establish that all relevant surfaces were observed.

### NIST SP 800-207 — trust decisions can consume multiple sources; source plurality is not automatic independence

SP 800-207 describes a policy engine trust algorithm consuming multiple information sources such as policy data, subject attributes/roles, historical behavior, threat intelligence and metadata. Zero trust removes implicit trust based merely on location/ownership.

Source: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

**TRANSFER VALIDATION:** supports explicit multi-input decision reasoning and avoiding implicit trust. It does not establish that multiple inputs are independent or sufficient; Web Manager therefore records correlation/failure domains separately.

## SYNTHESIS 1 — attestation validity has several layers

For a re-entry prerequisite, distinguish:
1. **artifact integrity/authenticity** — evidence was not silently altered and its asserted producer/context is credible where required;
2. **claim validity** — the evidence actually supports the stated bounded claim;
3. **applicability** — subject, consequence, topology, policy/configuration/schema epoch and time match the decision being made;
4. **dependency validity** — prerequisite assumptions and inherited evidence remain current;
5. **composition validity** — the set of prerequisites jointly satisfies the consequence graph without hidden contradiction/correlation invalidating the inference.

Guards:
- `attestation authentic ≠ claim applicable`;
- `claim applicable alone ≠ composite proof valid`;
- `all prerequisite rows green ≠ re-entry proven`.

## SYNTHESIS 2 — bind attestations to a composition context

A reusable generic attestation should carry or resolve enough context to establish:
- claim/control identity and version;
- subject/device/incarnation/service/topology scope;
- consequence/capability scope;
- policy/configuration/schema/authority epoch as relevant;
- evidence observation interval and freshness rule;
- verifier/evaluator identity and trust/policy context;
- source/collector identity;
- prerequisite/dependency references;
- known blind spots/coverage boundary;
- result and contradiction state.

The composite decision also needs a **composition context** defining the target consequence and required compatible epochs/scopes. This need not be one monolithic token; it is a semantic contract.

Guard: `same label ≠ same composition context`.

## SYNTHESIS 3 — epoch skew can create a false green composition

Example: identity is green under authority epoch A9, policy is green under P14, predecessor rejection was tested against P13/A8, and queue reconciliation used schema S11 while the target consequence requires P14/A9/S12. Each record can be historically valid, but they do not prove one current path.

Do not solve this by demanding identical timestamps. Instead define compatibility/currentness relationships among epochs and dependencies.

Guards:
- `individually fresh ≠ mutually compatible`;
- `same day ≠ same authority epoch`;
- `newest evidence ≠ compatible evidence`.

## SYNTHESIS 4 — multiple green signals can share one hidden failure domain

Identity-health, policy-health and rejection-health dashboards may all derive from one compromised collector, one stale configuration registry, one credential, one telemetry pipeline or one operator. Counting three greens then overstates assurance.

Record correlation dimensions where material: source, collector, verifier, credential, administration, deployment path, storage, provider and operator/failure domain.

Guards:
- `three green controls ≠ three independent assurances`;
- `different dashboard widgets ≠ different evidence sources`;
- `different control names ≠ different failure domains`.

## SYNTHESIS 5 — independence is risk-proportionate, not ceremonial

Not every prerequisite requires an independent verifier. For high-consequence re-entry, however, a composition that depends entirely on the same failure domain should be recognized as concentrated assurance. Independent-enough challenge can be required for selected decisive claims: predecessor rejection, current authority, high-impact publication/finalization, or contradiction resolution.

Guard: `independence useful ≠ duplicate every control assessment`.

## SYNTHESIS 6 — circular evidence cannot bootstrap itself into NORMAL

A can depend on B while B's green state depends on A's asserted NORMAL. Example: policy-current attestation is accepted only after queue drain, while queue-drain attestation assumes policy-current. The graph can produce mutually supportive green records with no external anchor.

Detect cycles in the **evidence-dependency graph**, not only runtime dependencies. Break them with a bounded recovery root/bridge whose authority is independently established and expires after use.

Guards:
- `mutual attestation ≠ independent foundation`;
- `cycle closed logically ≠ trust bootstrapped safely`.

## SYNTHESIS 7 — contradiction outranks convenient composition

If one current source says predecessor E1 is rejected and another bounded test shows E1 accepted, the system must not average or majority-vote them into green. Preserve both records, classify scope/epoch/source, determine whether one is stale/inapplicable, and revalidate the affected consequence.

Guards:
- `more green signals ≠ contradiction resolved`;
- `majority telemetry ≠ semantic authority`;
- `one contradiction ≠ universal compromise`.

## SYNTHESIS 8 — composite proof should fail closed by consequence, not erase useful lower states

If publication composition fails because predecessor-rejection evidence is stale, local preservation/read may remain safe. Re-entry state should degrade only the consequences whose proof depends on the failed/missing attestation, unless the contradiction has broader scope.

Guard: `publication proof incomplete ≠ local data inaccessible`.

## SYNTHESIS 9 — attestation freshness is event/assumption sensitive

TTL is insufficient. Evidence can become stale immediately after a material change in policy, credential, topology, verifier, schema, route or control implementation. Conversely, older evidence can remain valid for a historical claim.

Composition should check invalidation triggers and assumption generations, not only age.

Guards:
- `TTL unexpired ≠ attestation current`;
- `old evidence ≠ useless historical evidence`.

## SYNTHESIS 10 — verifier compromise scopes composite uncertainty transitively

If verifier V3 is compromised, identify which attestations V3 produced/validated and which composite re-entry decisions relied on them. Do not invalidate unrelated evidence merely because it coexisted. Do not preserve affected NORMAL merely because other green prerequisites remain.

Guard: `one verifier compromised ≠ every control compromised ≠ compositions depending on it safe`.

## SYNTHESIS 11 — Service Worker/browser evidence is especially easy to over-compose

A worker version, controller state, cache generation and online signal may all be observed from the same client/runtime. They can provide useful Track A facts but cannot independently prove server rejection, credential currentness, queue semantic validity or organizational admission. A single client that reports all four is still one bounded observation domain.

Guards:
- `four browser signals ≠ four independent authority proofs`;
- `Service Worker current + online ≠ publication authorized`.

## SYNTHESIS 12 — late-returning offline clients require local composition

A returning iPad cannot inherit a composite proof generated for the online cohort. Its local worker/cache/schema/queue/incarnation state must be bound to current central authority/rejection evidence. Preserve unique records first, then build only the consequence proof that applies to that client.

Guard: `fleet composite proof ≠ late-client composite proof`.

## SYNTHESIS 13 — analytics can challenge composition but cannot authorize it

Track D can surface:
- improbable perfect correlation among controls;
- shared collector/verifier concentration;
- epoch skew;
- contradiction frequency;
- stale attestation age;
- cohort gaps.

These metrics are diagnostic evidence. They can trigger challenge/revalidation but do not grant NORMAL.

Guard: `correlation alert cleared ≠ authority granted`.

## SYNTHESIS 14 — operator UX must not flatten composition uncertainty

Track B should distinguish at least conceptually:
- prerequisites available but composition not evaluated;
- composition valid for limited consequence;
- evidence conflict/revalidation required;
- prerequisite missing/stale;
- high-consequence action blocked while preservation/recovery remains available.

Exact copy/visual treatment remains Design Studio + human/AT validation OPEN.

Guard: `all checks displayed green ≠ operator should see NORMAL`.

## SYNTHESIS 15 — re-entry closure records should preserve why composition was accepted

For a material consequence, closure should retain enough provenance to reconstruct:
- required prerequisite set/version;
- attestation identifiers and applicability context;
- correlation/independence assessment where required;
- contradictions and disposition;
- decision authority/policy generation;
- residual offline/unknown-tail obligations;
- re-degradation triggers.

This supports later compromise or topology-change impact reconstruction without rewriting history.

Guard: `decision outcome retained ≠ decision basis reconstructable`.

## SYNTHESIS 16 — composition policy itself is versioned authority

Changing which prerequisites are required, which independence constraints apply, or which epoch relationships are compatible changes re-entry semantics. Treat material composition-policy change as governed/versioned policy; do not silently reinterpret historical closure records under new rules.

Guard: `new composition policy ≠ old closure historically invalid by default`.

## SYNTHESIS 17 — bounded challenge path prevents both blind trust and permanent deadlock

When composition fails because evidence conflicts or correlation is too concentrated, a challenge path should specify what can resolve it: targeted negative test, independent-enough observation, current bootstrap, verifier replacement, policy refresh, or consequence-specific manual review. Challenge authority must itself have bounded scope and provenance.

Guard: `composition blocked ≠ bypass composition`.

## SYNTHESIS 18 — generic composite decision pattern

For target consequence C:
1. load current composition policy CP and required prerequisite claims;
2. verify each attestation's integrity/authenticity as required;
3. verify claim semantics and subject/consequence/topology applicability;
4. check policy/configuration/schema/authority epoch compatibility;
5. validate inherited dependencies and invalidation triggers;
6. map shared source/verifier/credential/admin/failure domains;
7. apply risk-proportionate independence/challenge requirements;
8. surface contradictions without majority laundering;
9. preserve lower-consequence capabilities not affected by the failed proof;
10. record the composite decision and re-degradation triggers.

This is a reasoning contract, not a mandated implementation architecture.

## Track C destructive campaign additions — 896 → 904

1. **all-green-shared-collector:** identity/policy/rejection attestations all derive from one compromised collector. Expected: correlation recognized; high-consequence composition challenged.
2. **epoch-mix false composition:** individually fresh A9/P14 evidence combined with predecessor rejection from incompatible A8/P13. Expected: composition blocked until compatible proof.
3. **circular-attestation bootstrap:** queue-current depends on policy-current while policy-current depends on queue-current; both become green. Expected: cycle detected and bounded external recovery root required.
4. **majority-green contradiction laundering:** three dashboards green while direct predecessor negative test shows obsolete path accepted. Expected: contradiction preserved and affected consequence revalidated.
5. **TTL-only freshness:** attestation remains under age threshold after material credential/topology change. Expected: invalidation trigger forces reassessment.
6. **late-client fleet-proof inheritance:** six-week-offline iPad receives online-cohort NORMAL without local applicability checks. Expected: local preserve/rejoin/composition.
7. **browser-signal independence theater:** worker/controller/cache/online signals from one client counted as four independent assurances. Expected: one bounded runtime observation domain.
8. **verifier-compromise non-propagation:** V3 compromise recorded but composite publication decisions depending on V3 remain NORMAL. Expected: transitive affected-composition review without blanket global invalidation.

These are defined cases, not executed product evidence.

## EFB / LogMate-like application case

Scenario: central recovery reports identity A9 green, policy P14 green, server predecessor rejection green and queue migration green. A company iPad returns after six weeks offline with unique flight records. Investigation shows identity/policy/rejection dashboards all consumed the same configuration registry snapshot, while a direct negative request from a bounded test client shows one obsolete E1 route still accepted.

Generic safe handling:
1. preserve the iPad's unique records/queue/provenance;
2. do not inherit online-cohort NORMAL;
3. retain all green attestations but mark their shared source/failure domain;
4. preserve the E1 acceptance contradiction rather than majority-voting it away;
5. block only consequences requiring proven predecessor rejection (for example remote finalization/publication in the generic model);
6. independently-enough revalidate E1 rejection/current policy path;
7. bind the iPad's incarnation/schema/queue state to compatible current epochs;
8. re-evaluate the composite prerequisite graph;
9. admit only proven consequence states;
10. retain re-degradation triggers and unresolved fleet-tail obligations.

This does not establish LogMate's actual flight-record authority model or aviation compliance.

## MINTTAP DECISION / DIRECTION

- Treat material re-entry as **composite evidence**, not a checklist of independent-looking booleans.
- Preserve attestation provenance, applicability and correlation/failure-domain information sufficient for later challenge.
- Do not require artificial independence everywhere; require independent-enough challenge where consequence and concentration justify it.
- Contradictions block affected consequence closure until dispositioned; metrics/majority cannot vote semantic truth into existence.
- Preserve lower-consequence recovery/data access when high-consequence composition is incomplete, unless the contradiction actually reaches those capabilities.
- Do not promote browser/Service Worker currentness to semantic authority.

## DEPENDENCY / TRANSFER

- **Track A:** supply exact runtime/source boundaries for worker/cache/storage/network signals; avoid presenting co-derived signals as independent authority evidence.
- **Track B:** design truthful composition-pending/conflicted/limited states; Design Studio/human/AT validation required before product PASS.
- **Track C:** execute the 904-case campaign when implementation/runtime evidence exists.
- **Track D:** measure correlation, epoch skew and coverage as challenge signals only.
- **Software Engineering:** implementation-level attestation schema, verifier code, dependency graph and failure injection belong there when a canonical product contract exists.

## OPEN

- Actual MintTap/LogMate prerequisite graph and consequence taxonomy.
- Actual attestation format, signing/authentication needs, verifier identities and trust roots.
- Actual backend/session/credential/policy/schema/queue epochs.
- Actual MDM/ADE/managed-iPad topology and long-offline fleet inventory.
- Required independence thresholds/challenge rules by consequence.
- Physical iOS/iPadOS installed-PWA behavior and exact Safari/WebKit lifecycle.
- Human/operator comprehension, screen-reader/AT behavior and wording.
- Domain/legal/aviation authority and retention requirements.

## CHANGE WATCH

- NIST SP 800-53A/800-137/800-207 updates remain bounded governance/security precedent, not product semantics.
- Browser/WebKit/Chromium runtime behavior and Apple managed-device/PWA policy remain version-sensitive.
- Any future browser attestation/device-integrity capability must be assessed separately; do not infer availability or authority from generic web APIs.

## Gate

**PASS (generic)** because the Web Manager can distinguish attestation integrity, applicability, dependency and composition; diagnose epoch skew/correlation/cycles/contradictions; scope verifier compromise transitively; preserve consequence-specific degraded states; and define a bounded challenge/revalidation path without claiming product runtime evidence.

Production/device/domain/AT/human validation remains OPEN.

## Next high-value target

**269 — composite-proof revocation, decision-cache invalidation & stale-NORMAL resurrection resistance**: determine how a previously valid composite re-entry decision is invalidated when one prerequisite is revoked/contradicted, how cached `NORMAL` decisions across browser/server/offline clients are fenced, and how restored backups or long-offline devices are prevented from resurrecting a superseded composite authorization while preserving unique data.