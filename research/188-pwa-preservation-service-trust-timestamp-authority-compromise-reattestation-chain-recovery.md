# 188 — PWA Preservation-Service Trust, Timestamp-Authority Compromise & Re-attestation-Chain Recovery

Status: **PASS (generic) / PRODUCT + TSA/PRESERVATION + CRYPTO + LEGAL + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A offline/browser observation; Track B uncertainty/recovery UX; Track C destructive validation; Track D privacy-bounded preservation telemetry.
Dependencies: 183–187 exact-artifact provenance, transparency evidence, archive integrity, historical-verifier isolation, migration/algorithm retirement and bounded re-attestation.

## Problem
187 separated original evidence, historical validation context, migrated representation and later preservation assurance. The next failure domain is the preservation authority itself. A Time-Stamping Authority (TSA), long-term archive/preservation service, validation authority or its signing key can fail, be compromised, cease operation, equivocate, or become untrustworthy after it has issued evidence. If later preservation assertions are treated as authority rather than bounded evidence, compromise can rewrite chronology or launder an UNKNOWN historical interval into apparent certainty.

Central rule:

> **A preservation service may contribute bounded evidence about existence, validation or continuity; it is not the original authority and must not be able to rewrite historical chronology by itself. Compromise recovery preserves prior evidence and uncertainty, establishes a new preservation generation from independent current trust, and never treats redundancy as automatic majority authority.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Service Worker/Cache Storage/IndexedDB can retain old timestamp/re-attestation observations but are not clocks, TSAs or preservation authorities.
- **B UX/IA/Content:** consumer. Owns comprehensible distinctions among preserved locally, timestamp verified, preservation chain uncertain, and remote submission paused.
- **C Performance/Accessibility/Quality:** validator. Owns compromise-boundary, chain-recovery, stale-client, split-evidence, privacy and AT/human campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Preservation health telemetry must avoid raw evidence, stable device IDs and flight/user/location dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns preservation-service trust scope, compromise response, successor generation, chronology continuity and restore/reconciliation.

## SOURCE
### RFC 3161 — Time-Stamp Protocol
RFC 3161 defines a TSA as a source of proof that a datum existed before a particular time. Its security considerations are explicit: when a TSA private key is compromised, the corresponding certificate is revoked and tokens signed by that key cannot simply be trusted. An audit trail may help distinguish genuine from false backdated tokens, and timestamps from two different TSAs are another possible mitigation. RFC 3161 is updated by RFC 5816.

Source: https://www.rfc-editor.org/rfc/rfc3161.html

### RFC 4998 — Evidence Record Syntax
RFC 4998 addresses long-term evidence as timestamp mechanisms, certificates and algorithms age. It requires renewal before critical mechanisms lose assurance and specifically notes the risk of Timestamping Unit private-key compromise. It recommends, for risk reduction, at least two redundant Evidence Records using different hash algorithms and different TSAs/signature algorithms. This is survivability evidence, not a rule that two providers form an authorization majority.

Source: https://www.rfc-editor.org/rfc/rfc4998.html

### RFC 4810 — Long-Term Archive Service requirements
RFC 4810 supplies the long-term archive requirements behind ERS and warns against collapsing archive/preservation and all trust material into one authority capable of manufacturing apparently valid evidence. This supports separation between preserved objects, preservation evidence and independent trust/policy inputs.

Source: https://www.rfc-editor.org/rfc/rfc4810.html

### RFC 9921 — current timestamp-token integration evidence
RFC 9921 (February 2026) defines COSE header parameters for RFC 3161 timestamp tokens and reiterates the need for prompt reporting of compromised keys. It is current evidence that RFC 3161 timestamp semantics remain relevant in modern signed-object ecosystems; it does not mandate COSE or RFC 3161 for MintTap/LogMate.

Source: https://www.rfc-editor.org/rfc/rfc9921.html

### NIST SP 800-102 freshness correction
NIST withdrew SP 800-102, Recommendation for Digital Signature Timeliness, on **2025-07-01**. NIST stated that ANSI X9.95 and ISO/IEC 18014 provide more relevant/comprehensive timestamp guidance. Therefore SP 800-102 is historical context only and must not be cited as the current NIST timestamp baseline.

Source: https://csrc.nist.gov/pubs/sp/800/102/final

## SYNTHESIS — trust layers that must remain separate
Separate at least:
1. **original evidence/signature**;
2. **original event/claim time**;
3. **TSA token / preservation assertion**;
4. **TSA/preservation-service certificate/key/policy generation**;
5. **certificate/status/compromise evidence applicable to that generation**;
6. **later renewal/re-attestation**;
7. **archive/preservation chain provenance**;
8. **current admission authority**.

Persistent guards:
- `timestamp token signature valid ≠ claimed chronology globally trustworthy`;
- `TSA trusted now ≠ every historical token trusted`;
- `TSA compromised now ≠ every pre-compromise token automatically forged`;
- `certificate revoked ≠ compromise boundary automatically known precisely`;
- `new TSA token covers old evidence ≠ old UNKNOWN interval becomes known-good`;
- `two TSA tokens agree ≠ two independent failure domains proven`;
- `redundant preservation evidence ≠ majority authority`;
- `successor preservation service active ≠ predecessor history rewritten`;
- `archive can verify chain ≠ archive may mint original chronology`;
- `client clock agrees ≠ trusted timestamp established`;
- `PWA cached token ≠ current preservation state`.

## Compromise-boundary model
A preservation-service compromise creates at least three temporal regions, but their exact boundaries may be unknown:
- **pre-compromise evidence with independent corroboration** — potentially retainable under the applicable historical policy;
- **compromise/uncertain interval** — `UNKNOWN` unless trustworthy evidence discriminates genuine from attacker-created assertions;
- **post-reconstitution generation** — new preservation assertions under newly established current trust.

Do not derive the boundary solely from the compromised service's own clock/log after compromise. Preserve revocation/incident/audit/conflict evidence. If no trustworthy boundary can be established, widen UNKNOWN rather than backdating certainty.

RFC 3161's statement that compromised-key tokens cannot be trusted is intentionally conservative. Its audit-trail/two-TSA observations are recovery evidence, not permission to auto-accept a token merely because another service agrees.

## Preservation-service succession and recovery
Generic recovery state machine:
1. detect/suspect compromise or service loss;
2. freeze new reliance on the affected preservation generation where consequence-bearing decisions depend on it;
3. preserve original tokens, certificates/status material, audit/conflict evidence and known observations;
4. determine the evidence-backed compromise/uncertainty interval without relying solely on the suspect service;
5. establish a successor preservation generation from current independent trust/policy;
6. bind any renewal/re-attestation explicitly to predecessor evidence identity and the known uncertainty state;
7. publish successor lineage without claiming that successor signatures repair predecessor uncertainty;
8. reconcile archives, regions and clients against the surviving current preservation floor;
9. reopen bounded reliance only after enforcement/verification evidence;
10. retain compromise metadata needed to prevent later migration/PITR from laundering the incident.

`successor signed predecessor chain ≠ predecessor chain retroactively trusted`.

## Independent evidence and redundancy
RFC 4998's recommendation for different TSAs, hash algorithms and signature algorithms is useful resilience guidance. Independence must nevertheless be assessed by failure domain: two providers may share CA roots, cloud/KMS, administrators, identity recovery, software supply chain, network/time source or organizational control.

Multiple preservation observations improve survivability and contradiction detection. They do not create a generic voting system. A 2-of-3 result is not legitimate unless a product-specific policy deliberately defines and validates such semantics; no such MintTap/LogMate policy is known.

When independent evidence conflicts:
- preserve every authenticated conflicting assertion;
- do not choose the newest timestamp or simple majority automatically;
- identify failure-domain/provenance differences;
- keep affected chronology `UNKNOWN/INCIDENT` until current authorized reconciliation establishes what can actually be concluded.

## Time-source and chronology limits
A timestamp proves only the bounded claim supported by its protocol/policy and trust context. It does not prove semantic correctness of the underlying record. Client wall clocks, HTTP Date headers, analytics ingestion times and PWA queue timestamps are not substitutes for a trusted preservation timestamp.

Later timestamps can prove that a digest/evidence package existed no later than the later timestamp to the extent the later TSA is trustworthy. They cannot prove that an original business event happened at the original claimed time unless the evidence chain/policy supports that inference.

## PITR, archive restore and provider loss
Restore can resurrect:
- a compromised TSA key/certificate as apparently active;
- a pre-incident trust registry;
- missing revocation/compromise metadata;
- a preservation chain before successor reconstitution;
- an old verifier that accepts suspect generations as current.

After restore, reconcile against surviving current preservation/security/deletion/hold floors. A backup's internally consistent old trust view is historical evidence, not current authority.

Provider cessation without compromise differs from compromise. Historical tokens may remain interpretable under applicable policy when a provider simply ceases operation, while current issuance stops. Exact legal/trust-service consequences are jurisdiction/profile dependent and remain OPEN.

## PWA/EFB boundary
A long-offline company iPad may return with old TSA tokens, preservation envelopes, certificates, cached status and an obsolete Service Worker. Generic reconnect order:
1. preserve unique local flight/logbook records and drafts;
2. treat local timestamps and cached preservation material as observations, not current authority;
3. obtain current authenticated server security/preservation generation;
4. reconcile local evidence identity and any known compromise/retirement intervals;
5. migrate/renew preservation evidence only through current authorized server-side policy where required;
6. keep original evidence and UNKNOWN/incident markers intact;
7. re-admit queued consequence-bearing operations under current authority after reconciliation.

Do not assume iPadOS can run a long-term verifier, background renewal job or trustworthy wall-clock service while suspended/offline. Physical Safari/Home Screen/MDM evidence remains OPEN.

## Privacy and minimization
Preservation continuity does not justify permanent telemetry dossiers. Evidence packages should avoid stable device identifiers, raw flight/user/location/network histories and unrelated account metadata unless a specific obligation requires them. Compromise investigations may require temporary additional evidence; retention scope and expiry must remain explicit.

A long-offline client may contribute a bounded observation such as a checkpoint/token digest already held before an incident, but client fleet observations must not become a tracking beacon or authority vote.

## Track C destructive campaign
Define a **264-case generic campaign** spanning:
- TSA private-key compromise before/after token issuance;
- unknown compromise start time;
- forged backdated token;
- certificate revocation metadata absent/stale;
- suspect TSA audit trail modified;
- two TSA tokens agree but share KMS/admin/root dependency;
- independent TSAs disagree;
- successor TSA re-attests predecessor UNKNOWN as clean;
- preservation service becomes original-authority oracle;
- archive rewrites original event time during migration;
- later strong timestamp launders invalid/unknown evidence;
- provider cessation misclassified as compromise;
- compromise misclassified as ordinary retirement;
- PITR resurrects compromised key/trust registry;
- restore loses revocation/incident metadata;
- regional split view of current preservation generation;
- stale CDN distributes retired trust material;
- stale SW/IndexedDB retains suspect token as current;
- client clock manipulated while offline;
- long-offline iPad returns across several TSA/key generations;
- queue drains before preservation/security reconciliation;
- background renewal assumption fails on iPadOS;
- client fleet gossip leaks stable identity/location;
- privacy deletion collides with incident evidence hold;
- screen reader cannot distinguish `timestamp verified` from `historical chronology uncertain`;
- human operator treats two matching timestamps as majority authority;
- successor service outage pressures fail-open acceptance of old suspect evidence;
- algorithm retirement and TSA compromise occur in overlapping interval.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat timestamp/preservation services as bounded evidence providers, never as original business authority or current remote-admission authority.
2. Preserve original evidence, token identity, applicable verification context and compromise/incident metadata across provider/key succession.
3. On TSA/preservation compromise, establish an evidence-backed uncertainty interval; do not let a suspect service define its own clean boundary.
4. Successor preservation generations may renew continuity but may not erase predecessor INVALID/UNKNOWN or manufacture earlier chronology.
5. Redundant TSAs/evidence records improve survivability only when their failure domains are understood; no automatic majority semantics are inferred.
6. Keep current authority, historical verification and preservation issuance as separate capabilities.
7. Reconcile PITR/restores against surviving current preservation/security floors before accepting restored trust state.
8. Preserve unique local PWA/EFB data across offline/reconnect; cached timestamp material remains observation only and remote consequence is re-admitted under current server authority.
9. Minimize preservation telemetry and keep incident evidence retention bounded/governed.
10. Treat NIST SP 800-102 as withdrawn historical material as of 2025-07-01; use current standards/profiles at implementation time.
11. Keep exact product TSA/preservation architecture, trust-service/legal profile, compromise policy, algorithms, managed-iPad behavior and runtime validation OPEN.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate needs a TSA or long-term preservation service at all: **OPEN**.
- Actual TSA/preservation provider, policy, CA/status model and key hierarchy: **OPEN / Security + Software Engineering dependency**.
- Actual event-time/evidentiary requirements: **legal/aviation dependency**.
- Exact compromise-boundary and historical-token acceptance policy: **product/security/legal dependency**.
- Multi-provider independence/failure domains: **OPEN**.
- Archive/verification implementation and restore behavior: **Software Engineering dependency**.
- Physical iPadOS/Safari/Home Screen/MDM long-offline behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 264-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- Timestamp/trust-service profiles are jurisdiction/use-case dependent; current ANSI X9.95 / ISO/IEC 18014 / applicable trust-service rules must be checked at implementation time.
- RFC 3161 is updated by RFC 5816; modern integrations such as RFC 9921 do not change the need to verify current protocol/profile requirements.
- NIST SP 800-102 is withdrawn; do not revive it as current guidance.
- PQC/key-management transition guidance continues to evolve.
- Browser/iPadOS storage/background/runtime behavior remains change-sensitive.

## Adjacent next bottleneck
**PWA preservation-policy continuity, trust-service exit/portability & cross-provider re-anchoring**: determine how a product exits or replaces a preservation provider without silently changing historical validation policy, how trust anchors/status/audit evidence remain portable after provider cessation, how cross-provider renewal binds exact predecessor evidence without chronology laundering, and how long-offline clients converge across provider migration while keeping obsolete provider roots off current admission paths.