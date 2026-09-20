# 184 — PWA Constitutional-Policy Transparency Witness Independence, Checkpoint Gossip & Monitor-Compromise Recovery

Status: **PASS (generic) / PRODUCT + SECURITY + TRANSPARENCY-TOPOLOGY + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A cache/SW/offline observation mechanics; Track B verification-pending/degraded-state UX; Track C destructive split-view/witness/monitor validation; Track D privacy-bounded transparency measurement.
Dependencies: 176–183 brownout/exception governance, emergency/recovery reconstitution, constitutional policy generations, exact-artifact supply-chain lineage and transparency/equivocation evidence.

## Problem
183 established that transparency is detection evidence, not constitutional authority, and that one internally valid log view cannot prove global non-equivocation. The adjacent problem is operational: adding more witnesses, monitors or PWA observers does not automatically add independent evidence. They may share the same operator, cloud, identity plane, DNS, network path, build system, signer, storage or administrative recovery path; a compromised monitor may suppress or fabricate observations; a long-offline client may hold useful historical evidence but cannot safely become a trust anchor.

Central rule:

> **Numerical multiplicity is not witness independence. Treat log, witness, monitor, distributor, admission authority and client observer as distinct roles; evaluate their correlated failure domains; preserve signed conflicting checkpoints as incident evidence; reconstitute compromised observation infrastructure from surviving authenticated evidence without letting the transparency plane mint constitutional authority; and let PWA clients contribute only privacy-bounded observations, never authority.**

## Five-track balance
- **A Platform/Browser:** high-value dependency supplier. HTTP/CDN/SW/Cache Storage/IndexedDB explain delayed, stale and partitioned checkpoint observation. Browser observation is evidence, never current authority.
- **B UX/IA/Content:** high-pressure consumer. Owns understandable states such as verification pending, privileged submission paused, local work preserved and current policy re-established without exposing witness topology or cryptographic internals.
- **C Performance/Accessibility/Quality:** high-pressure validator. Owns correlated-witness failure, checkpoint fork, monitor compromise, stale-client, privacy and accessibility campaigns.
- **D Search/Discovery/Analytics:** bounded consumer. Transparency-health telemetry must remain low-cardinality and avoid stable per-device observation histories that become tracking identifiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns witness/monitor trust boundaries, failure-domain independence, gossip/checkpoint evidence, observation-plane compromise and reconstitution.

## SOURCE
### RFC 9162 Certificate Transparency v2 — split views require comparison outside one local view
RFC 9162 defines append-only Merkle-tree transparency and explicitly states that a misbehaving log can present conflicting views to different parties. It notes that append-only violations can be detected by multiple clients comparing signed tree heads; gossip is described as an active area rather than a complete protocol in the RFC. It also warns that proof-fetching patterns can create privacy concerns.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** CT is a TLS-certificate transparency protocol, not a MintTap/LogMate constitutional-policy protocol. The transferable property is that local cryptographic consistency does not establish global non-equivocation and that comparison/monitoring has privacy and availability consequences.

### C2SP Transparency Log Witness Protocol v1.0.0 — stateful consistency verification and cosigned checkpoints
The C2SP witness protocol specifies a witness identified by name/public key that tracks the latest checkpoint it verified for a log. A log normally supplies a new checkpoint plus a consistency proof; the witness verifies the log signature and consistency with its prior checkpoint before returning a timestamped cosignature. The protocol requires persistence of the new checkpoint before success and atomic check/update behavior to avoid rollback races. It also explicitly notes an unresolved monitor-retrieval problem: clients must not be partitioned from monitors by split or stale views.

Source: https://c2sp.org/tlog-witness

**SYNTHESIS:** A witness is useful because it carries authenticated continuity state across checkpoints. It does not judge whether the policy content is semantically legitimate, and a set of witnesses is not independent merely because several keys/signatures are present.

### transparency.dev witness model — witness vs monitor distinction
The transparency.dev witness implementation and public material distinguish witnesses, which check append-only consistency and countersign checkpoints, from ecosystem-specific monitors/verifiers that inspect log contents. This is useful role separation: global-view consistency and semantic/content legitimacy are different properties.

Sources: https://github.com/transparency-dev/witness ; https://blog.transparency.dev/can-i-get-a-witness-network

**TRANSFER VALIDATION:** The public witness-network design is precedent, not a mandatory MintTap architecture. No witness count/quorum or public network is selected here.

### Sigstore/Rekor — transparency requires monitoring
Sigstore documents Rekor as an append-only software-signature transparency log and explicitly notes that long-term trust requires monitoring. Its monitoring material demonstrates consistency checking and identity/event monitoring as separate operational functions.

Sources: https://docs.sigstore.dev/about/security/ ; https://docs.sigstore.dev/logging/overview/

**TRANSFER VALIDATION:** Rekor is software-supply-chain infrastructure. It demonstrates operational transparency roles but does not define constitutional policy authority for this project.

## SYNTHESIS — six roles that must not collapse conceptually
Keep separate:
1. **log/operator** — commits entries/checkpoints and serves proofs;
2. **witness** — retains prior trusted checkpoint state and cosigns only append-only evolution it can verify;
3. **monitor** — obtains enough history/checkpoints to evaluate contents, omissions, unexpected artifacts or ecosystem rules;
4. **distributor/gossip channel** — moves checkpoints/cosignatures between parties so targeted split views are harder to sustain;
5. **constitutional/admission authority** — decides which exact policy artifact/generation may be executable;
6. **client observer** — browser/PWA may retain what it saw and later report bounded evidence.

Persistent guards:
- `three witness signatures ≠ three independent failure domains`;
- `witness quorum met ≠ policy semantics authorized`;
- `monitor green ≠ witness/log uncompromised`;
- `monitor saw no conflict ≠ no conflict existed`;
- `checkpoint cosigned ≠ every client/region saw that checkpoint`;
- `gossip received ≠ gossip source authoritative`;
- `client reports checkpoint X ≠ X is current constitutional floor`;
- `many clients report X ≠ X legitimate by majority vote`;
- `witness key valid ≠ witness state/history uncompromised`;
- `monitor restored from backup ≠ missing observation interval reconstructed`;
- `transparency plane recovered ≠ policy/admission plane recovered`.

## Witness independence is a failure-domain property
A useful independence review asks whether apparently separate witnesses share:
- operator/administrator or privileged support account;
- cloud/provider/region/site;
- IdP, MFA/recovery path or organization email domain;
- DNS/registrar/network edge;
- software image/build pipeline/update signer;
- key custody/HSM/KMS control plane;
- database/storage/PITR authority;
- monitoring/alerting/evidence sink;
- funding/legal organization or incident responder capable of coordinated override.

No generic design can guarantee complete independence. The operational requirement is to make correlated domains explicit and avoid claiming N independent witnesses merely from N keys/processes.

### Numerical quorum is not enough
A 2-of-3 rule can still be one failure domain if the same administrator, IdP or deployment pipeline controls all three. Conversely, diversity that materially reduces correlated compromise can matter even when the system still has shared dependencies. Product topology and risk appetite are OPEN; this study deliberately does not choose M-of-N.

## Witness state and compromise
C2SP's witness model depends on retained latest-checkpoint state. This creates important failure modes:
- state rollback can make an old checkpoint look like the witness's latest known state;
- concurrent updates must not race backwards;
- key compromise can produce apparently valid cosignatures without honest consistency checking;
- key rotation without authenticated state continuity can sever the evidence chain;
- restoring witness storage from PITR must not silently erase later signed checkpoints.

Generic response to suspected witness compromise:
1. stop counting the suspect witness as fresh independent evidence;
2. preserve its signed checkpoints/cosignatures and conflict evidence;
3. compare against surviving witnesses/monitors and authoritative log/artifact lineage without treating majority as constitutional authority;
4. establish whether witness key, state, software, administrator or dependency was compromised;
5. rotate/reconstitute witness identity/state under an authenticated recovery path;
6. publish/record the new witness generation and old-compromise boundary where the actual design supports this;
7. re-evaluate quorum/availability policy rather than silently lowering it;
8. prove resumed consistency observation before restoring its evidentiary weight.

A compromised witness cannot repair constitutional policy authority; it can only be repaired as an observation/consistency actor.

## Monitor compromise and evidence reconstitution
Monitors differ from witnesses because they inspect content/history or ecosystem-specific expectations. A monitor can fail by omission as well as fabrication: not alerting on a bad entry may be the attack.

Generic recovery requirements:
- retain immutable/signed checkpoints and enough independent history outside the monitor's mutable database where justified;
- distinguish `no alert` from `verified no violation`;
- mark observation gaps explicitly rather than backfilling them as green;
- compare surviving checkpoints/history across independent sources;
- replay/recompute monitoring rules from authenticated retained history where possible;
- preserve an UNKNOWN interval if evidence was never retained or cannot be reconstructed;
- do not let a repaired monitor retroactively certify an interval for which the necessary evidence is absent;
- keep monitor configuration/rule provenance separate from the log's own checkpoint evidence.

`monitor backup restored ≠ monitor assurance restored`; restoration must address both software/configuration trust and evidence continuity.

## Checkpoint gossip/distribution
Gossip is evidence comparison, not policy voting. Useful generic properties are:
- checkpoints/cosignatures are authenticated and immutable enough to compare;
- observers can retain conflicting signed views rather than overwriting them with the newest response;
- replay/staleness is distinguishable from a genuine fork where possible;
- distribution paths are diverse enough that one network/CDN partition is not automatically global truth;
- clients/monitors do not select constitutional authority by local wall clock or apparent majority;
- conflict triggers incident/UNKNOWN handling and controlled-domain reconciliation.

RFC 9162's model is especially important here: multiple parties comparing signed heads can expose inconsistent views, but the RFC does not supply a universal gossip solution. Product protocol selection remains OPEN.

## Availability and fail-open pressure
Witness/monitor infrastructure can be unavailable. That creates a familiar security/reliability tension.

Generic rule:
- a transparency outage does not grant new constitutional authority;
- a previously admitted/current policy may remain usable only according to the real product's already-defined security/currentness policy;
- new constitutional transitions requiring witness evidence should not silently bypass that requirement because witnesses are slow/unavailable;
- local PWA work and unique data preservation remain separable from privileged remote consequence;
- if a product later chooses bounded fail-open semantics for a transparency check, that is a security/product decision requiring explicit threat model, expiry, observability and validation—not a generic default from this study.

## PWA / EFB observer boundary
A LogMate-like company-iPad PWA can be a useful **observer** without becoming an authority plane.

Allowed generic direction:
- retain a small bounded record of relevant signed checkpoint/generation observations when operationally justified;
- on reconnect, compare the retained observation with authenticated current server/transparency evidence;
- if a genuine signed conflict is found, preserve/report bounded evidence and pause affected privileged remote consequences;
- preserve local flight/logbook records and drafts throughout;
- never treat the device's wall clock, cached policy, Service Worker, IndexedDB or local majority of devices as constitutional authority;
- do not require every offline client to replay every missed checkpoint as executable policy state.

### Privacy boundary
A fleet-wide gossip system can accidentally become a tracking system. Avoid designs that require stable public per-device identifiers, precise long-term device observation timelines, flight payloads, user identity, location/network history or complete local cache inventories merely to compare checkpoints.

Prefer, subject to actual engineering/security validation:
- checkpoint/generation/digest-level evidence;
- coarse failure reason and bounded timestamps where necessary;
- server-side aggregation that does not expose a device dossier;
- explicit retention limits;
- upload only on meaningful conflict or bounded diagnostic sampling where possible.

No production telemetry schema is selected here.

## Track B UX transfer
Ordinary users should see consequence-oriented states, not transparency topology:
- security/governance verification is in progress;
- local work remains saved and available;
- affected remote privileged action is temporarily paused;
- pending work will be checked before submission after verification recovers.

Do not surface witness IDs, quorum counts, checkpoint hashes or monitor topology unless a specialist/admin diagnostic surface genuinely requires them. Screen-reader and representative-human comprehension remain OPEN.

## Track C destructive campaign
Define a **232-case generic campaign** spanning:
- three witnesses under one administrator/IdP/cloud/KMS;
- witness key compromise with honest state;
- honest key with rolled-back state;
- witness software supply-chain compromise;
- atomic-state update race;
- PITR resurrecting pre-conflict witness state;
- witness key rotation without checkpoint-state continuity;
- valid cosignature over stale checkpoint;
- log targets one witness set and clients with one fork and monitors with another;
- witness quorum numerically met but correlated;
- one witness unavailable and operator silently lowers threshold;
- monitor suppresses alert;
- monitor rule/config rollback;
- monitor backup restored with observation gap hidden as green;
- monitor sees stale partition indefinitely;
- distributor/CDN serves stale cosigned checkpoint;
- two signed conflicting checkpoints retained by different observers;
- client timestamp makes old checkpoint look current;
- majority of stale clients outvotes a fresh minority;
- malicious clients fabricate unsigned conflict reports;
- legitimate signed conflict report causes telemetry-cardinality explosion;
- per-device checkpoint reporting becomes stable tracking identifier;
- flight/user/location data leaks into transparency telemetry;
- long-offline iPad skips many checkpoint generations;
- stale SW/IndexedDB reports obsolete observation;
- reconnect drains privileged queue before current authority/transparency check;
- transparency outage incorrectly deletes local unique data;
- witness outage incorrectly blocks safe local draft/read/export;
- screen reader cannot distinguish local-save success from remote-submit pause;
- human operator mistakes monitor green for policy authorization;
- region admission uses transparency quorum as authorization substitute;
- transparency compromise plus constitutional signer compromise;
- transparency compromise without constitutional compromise;
- constitutional compromise while witnesses honestly expose the bad transition;
- evidence conflict survives but incident tooling overwrites it with newest head;
- recovery rotates witness key but retains compromised administrator;
- recovery restores monitor but not rule provenance;
- all observation paths share DNS/registrar failure;
- all witnesses share one provider support recovery path;
- client fleet is partitioned from monitors while both views remain locally consistent.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Treat witness independence as a failure-domain property, not a count of signatures or processes.
2. Keep log, witness, monitor, distributor/gossip, constitutional admission authority and client observer conceptually distinct.
3. Witnesses verify append-only continuity; they do not authorize policy semantics.
4. Monitors inspect ecosystem-specific content/history; monitor silence is not proof of safety.
5. Preserve signed conflicting checkpoints/cosignatures as incident evidence; do not overwrite conflict with the newest response.
6. Do not resolve split views by client wall clock, simple majority or number of stale devices.
7. Treat witness/monitor compromise recovery as evidence-plane reconstitution, not constitutional-authority recovery.
8. Do not silently lower witness requirements because a witness is unavailable; any degraded rule must be pre-governed and explicitly validated.
9. Keep witness state/key rotation rollback-resistant and preserve authenticated continuity across planned rotation; compromise recovery requires a stronger surviving basis.
10. Mark unreconstructable monitoring intervals UNKNOWN rather than retroactively green.
11. Allow PWA clients to retain/report bounded signed observations where useful, but never make them trust anchors or policy voters.
12. Keep transparency observation telemetry privacy-bounded and avoid stable per-device dossiers.
13. Preserve unique local PWA/EFB work during transparency incidents; re-admit remote privileged operations only after current server authority and applicable evidence are re-established.
14. Do not select a witness network, quorum, gossip protocol, transparency provider or client-reporting design without canonical product/security/engineering evidence.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate needs a transparency log/witness system at all: **OPEN; threat-model decision**.
- Actual log/witness/monitor/provider/region topology and failure domains: **OPEN**.
- Exact constitutional-policy admission rule and whether transparency evidence is required synchronously/asynchronously: **OPEN**.
- Witness quorum, key custody, rotation/recovery, monitor history retention and gossip/distribution protocol: **Security/Software Engineering dependency**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad behavior and offline observation storage: **OPEN**.
- Privacy/legal/aviation obligations for retained/uploaded checkpoint evidence: **OPEN**.
- Screen-reader/representative-human comprehension: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- RFC 9162 remains an Experimental IETF RFC; its gossip discussion is not a universal production protocol.
- C2SP `tlog-witness` v1.0.0 is the protocol version reviewed here; monitor future revisions, especially monitor retrieval/distribution semantics.
- Public witness-network and Sigstore/Rekor deployment details are implementation precedent, not product requirements; re-check before any architecture decision.
- Browser/iPadOS background execution, storage durability and managed-device behavior remain separately change-sensitive.

## Adjacent next target
Highest-value adjacent Stage-8/PWA question: **constitutional transparency evidence retention, witness-key succession & compromise-era checkpoint survivability** — determine what minimum signed checkpoint/conflict evidence must survive witness/log/monitor key rotation, organization/provider loss, PITR and long offline intervals; how to verify historical evidence without granting obsolete keys current authority; and how to avoid turning retained transparency history into an identity-rich permanent dossier.