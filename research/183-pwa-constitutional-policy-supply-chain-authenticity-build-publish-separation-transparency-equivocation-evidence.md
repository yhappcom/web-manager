# 183 — PWA Constitutional-Policy Supply-Chain Authenticity, Build/Publish Separation & Transparency/Equivocation Evidence

Status: **PASS (generic) / PRODUCT + SECURITY + SOFTWARE-SUPPLY-CHAIN + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A HTTP/cache/SW/currentness mechanics; Track B recovery/change-state UX; Track C destructive provenance/equivocation validation; Track D privacy-bounded generation/convergence measurement.
Dependencies: 176–182 brownout/exception governance, emergency/recovery reconstitution, quorum liveness, constitutional policy generations and governance-key transitions.

## Problem
182 established that constitutional recovery policy is a higher-order authority transition. The next gap is supply-chain authenticity: even if the correct successor policy was approved, the artifact that is built, signed, published, cached, admitted by regions and eventually observed by PWA clients can be substituted or forked.

Central rule:

> **Approval of policy semantics is not proof that the exact approved bytes became the artifact enforced everywhere. Bind approval, canonical artifact identity, provenance, signing/publication, regional admission and enforcement evidence into a verifiable lineage; separate roles/failure domains enough to resist substitution; treat transparency as detection evidence rather than authorization; and treat competing valid-looking views as an incident/UNKNOWN state until reconciled. Offline clients may retain observations but never become trust anchors.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. HTTP/CDN/cache/SW/IndexedDB explain how stale or forked policy observations persist. Browser state cannot establish supply-chain legitimacy.
- **B UX/IA/Content:** high-pressure consumer. Must distinguish update available, governance update pending, privileged submission paused, current policy re-established and local work preserved without exposing security topology.
- **C Performance/Accessibility/Quality:** high-pressure validator. Owns artifact substitution, signer/publisher compromise, cache split view, rollback, transparency inconsistency and long-offline-client campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Observe generation/digest/admission/convergence with low-cardinality telemetry; do not collect policy bodies, custodian identities, signing secrets or incident dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns exact-artifact lineage, signer/publisher separation, provenance trust boundary, transparency semantics, equivocation detection and enforcement proof.

## SOURCE
### NIST SP 800-218 SSDF v1.1 — protect software and collect provenance
NIST SSDF groups practices around preparing the organization, protecting software, producing well-secured software and responding to vulnerabilities. The current final v1.1 includes PS.3.2 for collecting and sharing provenance data for software-release components and treats protection against tampering/unauthorized access as a core outcome.

Source: https://csrc.nist.gov/pubs/sp/800/218/final

**CHANGE WATCH:** NIST SP 800-218 Rev.1 / SSDF v1.2 is an Initial Public Draft published 2025-12-17; its comment period closed 2026-01-30. It is not substituted for the current final baseline.
Source: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd

### NIST SP 800-53 Release 5.2.0 — software update/integrity emphasis
Release 5.2.0 explicitly strengthens controls/discussion around software update/patch reliability, software integrity and validation. It supports treating deployment artifact integrity as a security property, not merely CI convenience.
Source: https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls

### SLSA v1.2 — provenance and build trust boundaries
SLSA defines provenance as verifiable information tracking an artifact through the moving parts that produced it. Current Build-track guidance distinguishes provenance existence, signed provenance from hosted build platforms and hardened build platforms; provenance is evidence about production lineage, not proof that policy semantics were legitimately authorized.
Sources: https://slsa.dev/spec/v1.2/provenance ; https://slsa.dev/spec/v1.2/build-track-basics

**TRANSFER VALIDATION:** Constitutional policy may be configuration/data rather than compiled software. SLSA concepts transfer to exact-artifact lineage and builder trust boundaries, but this study does not claim a MintTap/LogMate SLSA level.

### in-toto — authorized supply-chain steps and link metadata
in-toto models a signed layout describing authorized supply-chain steps/functionaries and signed link metadata recording commands/materials/products. It demonstrates a useful separation between intended supply-chain procedure and evidence of what individual steps produced.
Source: https://in-toto.io/docs/getting-started/

### RFC 9162 Certificate Transparency v2 — inclusion, append-only consistency and split-view limit
RFC 9162 uses append-only Merkle trees, inclusion proofs and consistency proofs. It also explicitly notes that a misbehaving log can present inconsistent views to different clients; detecting that requires sharing/comparing log responses and is not solved merely by each client validating its own view.
Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** Certificate Transparency is not a constitutional-policy protocol. Its transparency properties provide a model for inclusion/append-only evidence and, importantly, the limitation that one valid local log view does not prove global non-equivocation.

## SYNTHESIS — exact lineage, not a chain of green checkmarks
Keep separate:
1. **authorized semantics** — human/governance decision about policy meaning;
2. **canonical source/artifact input** — immutable source identity used to produce deployable policy;
3. **canonicalization/build/packaging** — deterministic or otherwise evidenced transformation into deployable bytes;
4. **artifact identity** — digest/immutable identifier of exact deployable bytes;
5. **provenance/attestation** — evidence of how/by whom/where the artifact was produced;
6. **signing/authorization binding** — cryptographic authentication of the exact authorized artifact/generation;
7. **publication** — artifact becomes retrievable;
8. **regional admission** — controlled region accepts that artifact as eligible;
9. **runtime enforcement** — consequence path actually uses it;
10. **transparency observation** — evidence that an artifact/checkpoint was publicly or independently observable;
11. **client observation** — browser/PWA saw some artifact; never authority;
12. **historical verification** — verify old lineage without granting old artifact current authority.

Persistent guards:
- `policy approved ≠ exact deployed artifact approved`;
- `CI green ≠ artifact authentic`;
- `artifact signed ≠ policy semantics authorized`;
- `provenance present ≠ provenance producer trustworthy`;
- `digest matches publication ≠ runtime enforces that digest`;
- `transparency inclusion PASS ≠ artifact authorized`;
- `append-only consistency PASS ≠ global non-equivocation proven`;
- `two valid signed artifacts exist ≠ both may be current`;
- `CDN returned signed artifact ≠ region admitted it`;
- `region reports generation G ≠ consequence path enforces G`;
- `client cached G+1 ≠ server G+1 legitimate/current`;
- `offline client saw checkpoint X ≠ X is current authority floor`;
- `historical provenance verifies ≠ historical artifact executable`.

## Approval-to-artifact binding
Approval should bind the exact successor semantics to an immutable artifact identity or to an unambiguous canonicalization procedure whose output identity is then checked before signing/admission. A mutable branch, filename, release label, CDN URL or database row name is not enough.

Generic requirements:
- preserve immutable source revision/material identity for the approved change;
- make transformation/canonicalization rules explicit enough that a verifier can determine what was approved versus what was produced;
- bind signer/publisher admission to the expected digest/generation rather than a mutable label;
- reject post-approval mutation that changes artifact identity without a new authorized transition;
- keep policy authorization evidence separate from build/provenance evidence: both may be required, neither substitutes for the other.

No product serialization/canonicalization format is selected here.

## Build, signer and publisher separation
A single operator controlling source mutation, approval evidence, build output, signing key, publication and regional admission creates a high-concentration failure domain. Generic governance should separate these capabilities enough that compromise of one step does not silently manufacture an apparently legitimate successor.

This does **not** mandate a specific CI vendor, HSM, Sigstore, SLSA level or number of humans. It requires explicit trust-boundary analysis and evidence that user-controlled build steps cannot rewrite trusted provenance/signing assertions unnoticed.

Useful separation questions:
- Can policy authors mutate provenance or signing identity?
- Can build steps access the signer secret or redefine what is being signed?
- Can a publisher replace bytes while retaining a valid-looking mutable URL/version label?
- Can a region admit an artifact without checking expected identity/authorization lineage?
- Can the same compromised credential alter source, approve, sign, publish and suppress evidence?

## Transparency is detection evidence, not an authorization plane
A transparency mechanism can make policy-artifact/checkpoint history observable and make deletion/rewrite harder to hide. It must not become a second mechanism for granting policy authority.

Generic properties worth evaluating where threat/risk justifies them:
- append-only history or equivalent tamper-evident lineage;
- inclusion evidence for an artifact/checkpoint;
- consistency evidence between older/newer checkpoints;
- independent monitors/observers where feasible;
- retained signed conflicting views as incident evidence;
- privacy-bounded entries: digest/generation and minimum metadata rather than policy bodies, identities or sensitive incident detail.

Important limit from RFC 9162 transfer: a log can equivocate by presenting different internally valid views. Therefore `valid local consistency proof` alone is insufficient evidence that all observers saw the same history.

## Equivocation and split-view handling
Distinguish:
- **artifact substitution:** approved A becomes published B;
- **policy fork:** two differently authorized-looking artifacts claim the same/current generation;
- **transparency split view:** observers receive incompatible signed checkpoints/log views;
- **regional enforcement split:** regions enforce different policy generations/artifacts;
- **benign rollout skew:** planned temporary difference that remains bounded and evidenced.

Generic incident posture:
1. preserve conflicting signed/digest/checkpoint evidence;
2. do not resolve by newest client timestamp or majority of stale clients;
3. establish surviving authoritative governance/security floor outside the suspected failure domain;
4. identify which artifact/generation was legitimately authorized and produced;
5. reconcile publication/admission/enforcement domains;
6. re-admit queued privileged operations under current authority;
7. prove controlled-domain convergence before reopening high-consequence paths.

A fork is not automatically proof of malicious attack; it is an incident/UNKNOWN state until cause and legitimate lineage are established.

## CDN/cache/HTTP boundary — Track A transfer
CDN and browser caches distribute bytes; they do not establish constitutional legitimacy. Cache freshness, ETag validation or a 200 response cannot substitute for policy-generation/currentness checks.

Required distinctions:
- content freshness versus authority currentness;
- immutable artifact retrieval versus mutable pointer/current-generation discovery;
- cached historical artifact versus current executable artifact;
- Service Worker cache population versus server-side admission;
- CDN purge completion versus regional enforcement convergence.

## PWA / EFB transfer
For a LogMate-like company-iPad PWA:
- local flight/logbook records and drafts remain usable while policy supply-chain authenticity is unresolved;
- SW/Cache Storage/IndexedDB may preserve artifact/checkpoint observations for diagnostics but cannot authorize remote consequence;
- long-offline iPads may skip many policy/transparency checkpoints; reconnect should obtain current server authority and does not need to replay every historical artifact as executable state;
- a cached newer-looking policy must not overrule the server's authenticated current floor;
- queued privileged operations are re-admitted after current policy/artifact lineage is established;
- policy artifact update, Service Worker update, app/schema migration, authentication/session recovery and sync reconciliation remain separate state machines;
- no assumption is made about iPadOS background fetch/push/MDM distribution or direct device-to-device policy propagation. Physical Safari/Home Screen/managed-device evidence remains OPEN.

## UX transfer — Track B
User-facing state should express consequence, not internal cryptography:
- governance/security update verification in progress;
- local work remains saved;
- privileged remote actions are temporarily paused;
- pending actions will be checked before submission when current policy is established.

Do not expose signer IDs, log topology, monitor endpoints, policy digests or internal failure-domain maps to ordinary users. Accessibility and representative-human comprehension remain OPEN.

## Track C destructive campaign
Define a **224-case generic campaign** spanning:
- source changes after approval;
- mutable branch/tag resolves differently at build time;
- canonicalization ambiguity produces different bytes;
- builder substitutes artifact;
- build step forges user-controlled provenance fields into trusted assertions;
- provenance signer compromised;
- policy signer signs unauthorized artifact;
- valid signature on wrong generation/digest;
- publisher swaps artifact after signing;
- mutable CDN URL serves different valid-looking bytes;
- region admits without digest/authorization check;
- region reports G but enforcement path still uses G-1;
- two valid-looking artifacts claim G;
- planned rollout skew mistaken for safe convergence;
- malicious/failed transparency log serves split views;
- inclusion exists but no consistency with prior checkpoint;
- local consistency passes while two observers hold conflicting signed heads;
- monitor outage falsely reported green;
- telemetry pipeline suppresses conflicting generation;
- PITR restores old signer/provenance/publisher state;
- rollback restores historically signed easier policy;
- stale CDN/SW/IndexedDB keeps obsolete artifact;
- client clock makes stale checkpoint appear current;
- long-offline iPad reconnects with obsolete/newer-looking cached artifact;
- queued privileged operation drains before lineage/admission check;
- local unique data is deleted because policy authenticity is unresolved;
- privacy-heavy transparency entries leak identities/topology;
- screen-reader/user message confuses app update with governance verification;
- accessibility failure blocks safe degraded-state recovery;
- attacker controls source+CI but not signer;
- attacker controls signer+publisher but not constitutional authorization;
- attacker controls transparency service but not admission authority;
- same credential controls source, approval, signer and evidence suppression;
- provenance valid but references incomplete/wrong materials;
- historical provenance accepted as current authorization;
- current artifact authentic but runtime loads a different cached policy.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Bind constitutional approval to exact immutable policy artifact identity/generation, not mutable names or URLs.
2. Separate authorization evidence, build/provenance evidence, artifact signature, publication, regional admission and runtime enforcement.
3. Treat provenance as evidence about production lineage, never as proof of semantic authorization by itself.
4. Analyze source/build/signer/publisher/admission/evidence failure-domain concentration; do not allow a convenient pipeline to silently become constitutional authority.
5. Verify artifact identity at admission/enforcement boundaries appropriate to the real implementation.
6. Treat transparency as tamper/equivocation-detection evidence, not a policy authority plane.
7. Preserve conflicting signed/checkpoint evidence and treat split views as incident/UNKNOWN until reconciled.
8. Do not infer global non-equivocation from one valid local transparency view.
9. Make policy/artifact generations forward-moving and rollback/PITR resistant at the authority layer.
10. Keep CDN/cache/SW freshness separate from constitutional currentness.
11. Preserve unique local PWA/EFB work during authenticity incidents; re-admit remote consequences only after current server lineage/admission is established.
12. Keep transparency/convergence telemetry low-cardinality and privacy-bounded.
13. Do not select a CI provider, SLSA level, Sigstore/Rekor, in-toto deployment, HSM, signer type, canonicalization scheme or monitor quorum without canonical product/security/engineering evidence.

## OPEN / DEPENDENCY / VALIDATION
- Actual MintTap/LogMate constitutional policy representation, canonicalization, build/publish pipeline, signer, provenance, CDN/region topology and admission path: **OPEN**.
- Whether a transparency log is justified at all for the product threat model: **OPEN**.
- Exact CI/CD, artifact signing, provenance generation, immutable storage and enforcement implementation: **Software Engineering/security dependency**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad/offline runtime: **OPEN**.
- Legal/aviation/investment retention/evidence obligations: **OPEN**.
- Screen-reader/representative-human comprehension: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- NIST SP 800-218 v1.1 remains the current final SSDF baseline used here; Rev.1/SSDF v1.2 remains Initial Public Draft as of 2026-09-20.
- SLSA v1.2 is the current approved specification referenced here; monitor future revisions before product requirements are frozen.
- Transparency implementation behavior and browser/iPadOS capabilities remain separately change-sensitive.

## Adjacent next target
Highest-value adjacent Stage-8/PWA question: **constitutional-policy transparency witness independence, checkpoint gossip & monitor-compromise recovery** — how to detect/retain evidence of split views without assuming one transparency operator or one client fleet is honest/current; how witness/monitor independence differs from numerical multiplicity; how compromised transparency evidence is reconstituted; and how offline PWA clients contribute observations without becoming authority or privacy-heavy tracking beacons.