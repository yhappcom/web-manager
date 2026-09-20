# 185 — PWA Transparency Evidence Retention, Witness-Key Succession & Compromise-Era Checkpoint Survivability

Status: **PASS (generic) / PRODUCT + SECURITY + TRANSPARENCY-TOPOLOGY + KEY-CUSTODY + RETENTION + MANAGED-IPAD + RUNTIME + PRIVACY + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-21
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A offline/cache observation mechanics; Track B verification/recovery UX; Track C destructive retention/key-transition validation; Track D privacy-bounded evidence measurement.
Dependencies: 182–184 constitutional-policy generations, exact-artifact lineage, transparency/equivocation evidence, witness independence and monitor-compromise recovery.

## Problem
184 established that transparency is evidence rather than authority, that witness independence is a failure-domain property, and that conflicting signed checkpoints must survive as incident evidence. The next problem is temporal: logs, witnesses, monitors, organizations, providers and cryptographic keys change or disappear, while long-offline PWA clients may reconnect after multiple transitions. Historical evidence must remain verifiable enough to investigate past state without granting obsolete or compromised keys current authority, and retention must not become an identity-rich permanent dossier.

Central rule:

> **Retain the minimum authenticated evidence needed to prove historical checkpoint identity, continuity/conflict and key-transition context; separate historical verification eligibility from current signing/admission authority; preserve compromise-era uncertainty instead of laundering it through key rotation or PITR; and keep client/fleet evidence bounded by purpose and privacy.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. SW/Cache Storage/IndexedDB can retain old observations but cannot confer currentness; eviction and long-offline gaps make client history incomplete by design.
- **B UX/IA/Content:** consumer. Owns comprehensible states for historical evidence unavailable, current verification pending, local work preserved and remote privileged submission paused.
- **C Performance/Accessibility/Quality:** validator. Owns key-transition, retention-gap, PITR, offline-client, privacy and accessible-state destructive testing.
- **D Search/Discovery/Analytics:** bounded consumer. Evidence-health telemetry must not expose long-lived device/user/flight dossiers.
- **E Architecture/Security/Operations:** **highest-risk owner**. Owns retention classes, key succession, compromise boundaries, archive verification and evidence reconstitution.

## SOURCE
### RFC 9162 — signed tree heads are authenticated snapshots, not timeless current authority
RFC 9162 defines signed tree heads containing log identity, tree head data and signature. It also identifies privacy risks when tree heads/proofs are used in ways that can mark individual clients. Transferable property: retain authenticated checkpoints as evidence, but do not infer that an old valid checkpoint is current or globally non-equivocating.

Source: https://www.rfc-editor.org/rfc/rfc9162.html

**TRANSFER VALIDATION:** Certificate Transparency is not a MintTap constitutional-policy protocol. Its signed-head and privacy properties transfer; its exact retention periods and ecosystem policy do not.

### C2SP checkpoint/witness specifications — unknown signatures can be ignored; witnesses carry continuity state
C2SP checkpoint semantics permit clients to ignore unknown signatures, enabling log-key rotation and witness cosigning. The witness protocol requires a witness to validate a log checkpoint against trusted origin keys and prior witnessed state, preserving append-only continuity. The development transparency-log policy specification makes log/witness keys and quorum explicit inputs for offline checkpoint validation.

Sources: https://c2sp.org/tlog-checkpoint ; https://c2sp.org/tlog-witness ; https://c2sp.org/tlog-policy

**SYNTHESIS:** Historical verification needs the applicable historical verification context, not permanent current trust in every old key. A key registry/policy generation must distinguish which key was acceptable for which evidence interval and purpose.

### Sigstore/Rekor — sharding supports freezing a tree and rotating signing keys
Sigstore documents Rekor sharding as a way to freeze the current log and rotate signing keys while preserving access to entries across shards. Sigstore also describes its trust root as rotated keyholders protected through TUF-based trust-root distribution and notes that long-term transparency trust requires monitoring.

Sources: https://docs.sigstore.dev/logging/sharding/ ; https://docs.sigstore.dev/about/security/ ; https://docs.sigstore.dev/logging/overview/

**TRANSFER VALIDATION:** Rekor is implementation precedent. It demonstrates that active signing can move to a successor key/tree while historical evidence remains queryable; it does not prescribe this project's topology or retention period.

### NIST SP 800-57 Part 1 Rev.5 — key lifecycle, compromise and archival verification are distinct concerns
NIST SP 800-57 Part 1 Rev.5 is the current final general key-management recommendation. It covers key lifecycle, compromise, archive, backup and trust-anchor concerns. The durable principle is that a key may cease being acceptable for new protection/signing while attributes or verification material can remain necessary for audit or archived-data verification; compromise changes how prior signatures/evidence must be assessed.

Source: https://www.nist.gov/publications/recommendation-key-management-part-1-general-1

**CHANGE WATCH:** Rev.6 remains separate change-watch material; no draft-only rule is promoted here.

## SYNTHESIS — evidence classes must not collapse
Keep at least these concepts separate:
1. **current authority material** — keys/policy generations allowed to authorize or sign new current transitions;
2. **historical verification material** — public keys/certificates/policies needed to verify retained historical signatures;
3. **checkpoint evidence** — signed tree/checkpoint identity, size/root and applicable cosignatures;
4. **continuity evidence** — consistency proofs or authenticated predecessor/successor relationships where retained;
5. **conflict evidence** — competing signed views, incident observations and relevant provenance;
6. **compromise metadata** — which key/operator/generation was suspected or known compromised and the bounded interval/evidence basis;
7. **client observation evidence** — optional bounded PWA observation used for comparison, not authority.

Persistent guards:
- `old key verifies history ≠ old key may sign new history`;
- `key retired ≠ historical evidence must be deleted`;
- `key compromised ≠ every pre-compromise signature automatically trustworthy`;
- `key rotated ≠ compromise-era uncertainty resolved`;
- `checkpoint retained ≠ consistency path retained`;
- `latest checkpoint retained ≠ conflict evidence retained`;
- `archive restored ≠ missing interval reconstructed`;
- `PITR recovered old key/policy ≠ old authority reactivated`;
- `historical verifier available ≠ verifier belongs on current admission path`;
- `client retained old checkpoint ≠ client is authoritative witness`;
- `more retained telemetry ≠ stronger evidence`.

## Minimum survivable evidence model
A generic minimum cannot prescribe byte-level schema, but a defensible retained checkpoint record should be able to answer, where the actual protocol supports it:
- what log/origin and checkpoint generation/tree size/root were observed;
- which log/witness signatures were attached and under which verification-policy/key generation they were validatable;
- enough immutable identity/digest/provenance to detect substitution;
- predecessor/successor or consistency evidence needed for the intended continuity claim;
- explicit conflict records when competing valid-looking views were observed;
- key lifecycle state relevant to interpretation: active, retired, revoked/compromised, successor generation and bounded compromise uncertainty where known;
- source/purpose and retention class without unnecessary user/device/flight payload.

Do **not** assume every leaf, proof, raw request, device identifier or user context must be retained forever. Evidence sufficiency is claim-specific.

## Witness/log key succession
### Planned succession
A planned key transition should preserve an authenticated relationship between old verification context and new verification context without allowing the old key to remain a current signer indefinitely. Useful properties:
- exact effective generation/boundary is recorded;
- old public verification material remains available as long as retained evidence requires it and algorithms remain acceptable for historical verification;
- new checkpoints use the successor current key according to current policy;
- verifier selection is based on authenticated generation/context, not trial-and-error downgrade;
- old private signing material is removed/disabled according to the real key-management design.

### Compromise succession
If the old signing/witness key is compromised, its signature over a successor is not sufficient independent evidence of safe succession. Preserve the compromise boundary and surviving independent evidence. Historical signatures inside an uncertain compromise interval remain **UNKNOWN/suspect according to actual incident evidence**; rotating the key does not retroactively certify them.

`cryptographically valid under compromised key ≠ historically legitimate`.

## Retention across provider/organization loss
Evidence survivability should not depend exclusively on the component whose behavior is under investigation. Depending on the real threat model, this can require retained authenticated checkpoint/conflict evidence outside the mutable log/monitor/witness failure domain. The generic requirement is failure-domain analysis, not a mandated public archive or vendor.

If a provider or organization disappears:
- preserve public verification context and evidence needed for retained claims;
- preserve provenance of successor custody/verification policy;
- do not treat new provider ownership as retroactive authority over old evidence;
- mark unrecoverable intervals UNKNOWN rather than fabricating continuity.

## PITR and backup
PITR is a major resurrection hazard. A restore can bring back:
- an old active-key flag;
- old witness latest-checkpoint state;
- a policy that trusts a retired key for current signing;
- a monitor DB before a known conflict;
- deleted compromise metadata.

Generic recovery therefore reconciles restored state against a surviving current security/key floor before reopening consequence-bearing paths. Conflict and compromise records must not be silently lost merely because the restored snapshot predates them.

## Long-offline PWA/EFB boundary
A company iPad may reconnect after log/witness/key generations have changed.

Generic direction:
1. preserve unique local flight/logbook records and drafts;
2. treat locally cached checkpoints, policies and public keys as historical observations only;
3. obtain current authenticated server/security/transparency context when connectivity returns;
4. validate any useful retained historical observation under the appropriate historical verification context;
5. do not reactivate an obsolete key because the device can still verify it;
6. preserve/report a genuine signed conflict in bounded form if discovered;
7. re-admit queued privileged operations under current server authority;
8. do not require replay of every missed transparency generation as executable policy state.

Browser storage eviction means absence of a local checkpoint is not evidence that no checkpoint/conflict existed. Client storage is not the durable transparency archive.

## Privacy and retention minimization
Transparency evidence can become surveillance if it accumulates stable device identity, precise timestamps, user identity, flight/location/network history and long retention.

Generic minimization:
- retain evidence by security claim, not by maximal observability;
- prefer checkpoint/generation/digest/key-generation identifiers over raw business payloads;
- separate incident evidence from analytics;
- avoid stable per-device identity unless a demonstrated security requirement justifies it;
- bound timestamps/retention/access where precision is unnecessary;
- preserve conflicts without attaching unrelated user/flight content;
- define deletion/archival review independently from current-key rotation.

No product retention duration is selected here; legal, aviation, privacy and incident-response requirements remain OPEN.

## Track B transfer
User-facing recovery should communicate consequences rather than cryptographic internals:
- local work is saved;
- security verification is being refreshed;
- affected remote submission is paused until current verification is restored;
- historical verification uncertainty, when relevant to an admin/support workflow, must not be rendered as ordinary user blame or silent data deletion.

Screen-reader and representative-human comprehension remain OPEN.

## Track C destructive campaign
Define a **240-case generic campaign** spanning:
- planned log/witness key rotation with old public verification retained;
- old private key accidentally remains current signer;
- verifier trial-and-error accepts obsolete key;
- compromised old key signs successor;
- compromise date/interval uncertain;
- pre/post-compromise evidence mixed in one green state;
- key retired and verifier material deleted too early;
- algorithm no longer acceptable for new signing but historical verification still needed;
- checkpoint retained without applicable historical policy/key context;
- checkpoint retained without required continuity proof;
- conflict evidence overwritten by latest head;
- witness PITR restores old latest-checkpoint state;
- monitor PITR removes known conflict;
- backup restores retired key as active;
- provider loss removes sole copy of verification metadata;
- organization succession confuses custody with authority;
- shard/frozen-tree history becomes unreachable;
- archive integrity valid but provenance missing;
- archive restore fabricates a green gap;
- retention deletion removes incident boundary before case closure;
- excessive retention creates device/user dossier;
- exact timestamps correlate with flight/location history;
- analytics pipeline receives checkpoint conflict payloads;
- long-offline iPad holds obsolete key/policy/checkpoint;
- stale SW serves old verifier policy;
- IndexedDB eviction removes local observation;
- client clock misorders generations;
- reconnect treats local old key as current;
- reconnect queue drains before current server authority;
- current server context is unavailable but local drafts remain safe;
- multiple clients report same stale checkpoint and are mistaken for authority;
- signed historical conflict survives client reinstall but not server retention;
- historical verifier is exposed in primary mutation path;
- key compromise plus monitor compromise;
- witness compromise plus provider loss;
- accessibility status fails to distinguish saved-local vs submitted-remote;
- operator mistakes successful historical signature verification for current authorization.

Campaign definition PASS; execution remains OPEN.

## MINTTAP DECISION — generic governance
1. Separate current signing/admission authority from historical verification material.
2. Retain authenticated checkpoint/conflict/key-lifecycle evidence according to the claims that must survive, not a maximal raw-history default.
3. Preserve explicit compromise/uncertainty boundaries across key rotation, PITR and provider/organization change.
4. Never let key rotation retroactively certify a compromise-era interval.
5. Never let PITR reactivate retired/compromised current authority without reconciliation to the surviving security floor.
6. Keep historical verifiers isolated from the primary current-admission path where implementation permits; Software Engineering must validate the actual design.
7. Preserve signed conflicting checkpoints as incident evidence even when a newer legitimate head exists.
8. Do not interpret missing client evidence as proof of absence; browser storage can be evicted or stale.
9. Let long-offline PWA clients skip obsolete executable generations and converge on current server authority while preserving local data.
10. Keep transparency retention privacy-bounded; do not create permanent per-device/user/flight observation dossiers.
11. Do not choose retention durations, archive providers, witness/log topology, key algorithms, custody or quorum without product/security/legal/engineering evidence.

## OPEN / DEPENDENCY / VALIDATION
- Whether MintTap/LogMate requires a constitutional transparency system: **OPEN**.
- Actual log/witness/monitor key topology, rotation/revocation mechanism and historical verifier: **Software Engineering/Security dependency**.
- Exact evidence schema and which consistency/inclusion proofs must be retained: **OPEN; protocol/claim dependent**.
- Retention duration and deletion/legal hold requirements: **Privacy/legal/aviation/incident-response dependency**.
- Independent archive/provider/failure-domain topology: **OPEN**.
- Physical iPadOS/Safari/Home Screen/MDM/Shared-iPad storage/update behavior: **OPEN**.
- Screen-reader and representative-human comprehension: **OPEN**.
- 240-case campaign execution: **OPEN**.
- Production validation remains OPEN; this PASS is generic competency only.

## CHANGE WATCH
- C2SP transparency-log policy and current witness/checkpoint specifications are evolving; re-check before implementation.
- Sigstore/Rekor deployment, trust-root and sharding mechanics are implementation precedent, not product requirements.
- NIST key-management revisions and post-quantum transition guidance may alter algorithm/key-lifecycle decisions; current product crypto choices remain OPEN.
- Browser/iPadOS storage/background/update behavior remains separately change-sensitive.

## Adjacent next bottleneck
**PWA transparency archive integrity, historical-verifier isolation & evidence-deletion/crypto-erasure governance**: determine how retained historical evidence is independently integrity-protected and restorable; how legacy verification code/algorithms are sandboxed away from current mutation authority; how deletion, legal hold and crypto-erasure interact with incident evidence; and how archive compromise/recovery avoids converting an evidence store into a new trust anchor or privacy dossier.