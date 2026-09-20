# 179 — PWA Emergency-Authority Compromise, Break-Glass Credential Recovery & Trust Reconstitution

Status: **PASS (generic) / PRODUCT + SECURITY + LEGAL + PROVIDER + MULTI-REGION + MANAGED-IPAD + RUNTIME + HUMAN/AT VALIDATION OPEN**
Date: 2026-09-20
Primary owner: **Track E — Web Architecture, Security & Operations**
Major consumers: Track A session/SW/cache/currentness mechanics; Track B compromise/recovery UX semantics; Track C destructive recovery validation; Track D privacy-bounded incident telemetry.
Dependencies: 173–178 distributed security-state convergence, fail-safe degradation, recovery proof, exception provenance/expiry, compensating-control assurance and break-glass separation.

## Why this study exists
178 established that break-glass must be narrow, expiring, independently governed and observable. The adjacent catastrophic case is compromise of the emergency credential, approval plane, recovery root, or evidence plane itself. A system that can revoke ordinary credentials but requires a compromised emergency root to authorize its own replacement has not established a trustworthy recovery path.

Central rule:

> **Compromise recovery is a trust-reconstitution protocol, not credential rotation. A compromised emergency authority cannot be the sole authority that blesses its successor. Reconstitution requires surviving evidence/authority outside the compromised failure domain, invalidates inherited privileged state, advances a non-rollback security generation, and re-admits consequences only after current enforcement is proven.**

## Five-track balance
- **A Platform/Browser:** dependency supplier. Sessions, cookies, bearer artifacts, Service Worker, Cache Storage, IndexedDB, device clocks and reconnect observations may carry stale privileged state but cannot establish successor authority.
- **B UX/IA/Content:** owns safe semantics for `privileged access suspended`, `local work preserved`, `re-authentication/re-approval required`, `submission paused`, and recovery completion without disclosing sensitive recovery topology.
- **C Performance/Accessibility/Quality:** owns destructive validation across credential/session replay, region split-view, PITR, stale clients, recovery races, evidence loss and accessible/human-comprehensible degraded states.
- **D Search/Analytics:** bounded consumer. Compromise/recovery telemetry is security evidence, not acquisition analytics; avoid durable per-person privileged-history graphs and raw credential/case payloads.
- **E Security/Operations:** **bottleneck/owner**. Owns compromise declaration, emergency-floor advancement, successor trust establishment, credential/session invalidation, recovery independence, regional convergence, rollback resistance and closure evidence.

## SOURCE
### NIST SP 800-63B-4 — Authentication and Authenticator Management
NIST published SP 800-63B-4 on 2025-08-01 as the current authentication/authenticator-management guideline. Authenticator lifecycle management treats compromise, replacement/recovery, binding and revocation as security-sensitive lifecycle events rather than mere credential edits.
Source: https://www.nist.gov/publications/nist-sp-800-63b-4digital-identity-guidelines-authentication-and-authenticator

Transfer: subscriber authenticator guidance does not itself define an enterprise break-glass recovery architecture. It supports the narrower principle that compromise must change authenticator trust state and that recovery/binding is security-sensitive.

### NIST SP 800-63-4 — Digital Identity Guidelines
The 2025 final suite covers identity proofing, authentication, authenticator management and federation. It supports keeping identity/authentication/federation lifecycle evidence distinct rather than treating one recovered login as proof that every delegated or emergency authority is restored.
Source: https://www.nist.gov/publications/nist-sp-800-63-4-digital-identity-guidelines

### OWASP Top 10:2025 — Broken Access Control
OWASP continues to require server-side access control, deny-by-default and testing of access-control paths. Recovery and emergency routes remain access-control surfaces; a special recovery endpoint is not exempt because it is operationally exceptional.
Source: https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

### CISA emergency compromise precedent
CISA Emergency Directive 24-02 required analysis of exposed correspondence, reset of compromised credentials and additional protection of privileged cloud accounts after compromise. This is incident-specific evidence, not a universal recovery recipe, but it reinforces that credential compromise can require both invalidation and broader privileged-account remediation rather than a cosmetic password change.
Source: https://www.cisa.gov/news-events/alerts/2024/04/11/cisa-issues-emergency-directive-24-02-mitigating-significant-risk-nation-state-compromise-microsoft

## SYNTHESIS — distinguish compromise scopes
Do not collapse these states:
1. **emergency authenticator/credential compromise**;
2. **emergency session/bearer artifact compromise**;
3. **approver identity compromise**;
4. **approval-policy/control-plane compromise**;
5. **recovery-root/custody compromise**;
6. **audit/evidence-plane compromise**;
7. **regional policy-state compromise**;
8. **client/PWA stale privileged observation**.

A response that fixes one layer does not prove the others are safe.

Persistent guards:
- `credential rotated ≠ emergency trust reconstituted`;
- `old root signed successor ≠ successor independently trusted`;
- `operator reauthenticated ≠ compromised approval policy repaired`;
- `new key active ≠ old sessions invalidated`;
- `session revoked centrally ≠ every region enforced revocation`;
- `region current ≠ offline client current`;
- `audit clean ≠ evidence plane uncompromised`;
- `PITR restored configuration ≠ pre-compromise authority safe to reuse`;
- `same human recovered ≠ same emergency authority generation restored`;
- `local data preserved ≠ privileged state preserved`.

## Compromise declaration and containment
A credible compromise signal should move affected emergency authority into a containment/reconstitution state rather than waiting for normal expiry. Generic actions are consequence- and evidence-dependent, but the model requires:
- identify affected authority generation and potentially exposed dependent sessions/artifacts;
- suspend or revoke affected emergency consequence authority where current evidence supports doing so;
- preserve independent incident evidence without making evidence preservation an excuse to leave privileged authority executable;
- advance a security floor that rollback/PITR cannot silently cross;
- preserve safe local/read/export capability classes where they do not depend on the compromised authority;
- avoid asserting a complete blast radius until evidence supports it.

`cannot prove unaffected` is not identical to `proven compromised`; UNKNOWN remains explicit and may still require conservative admission for high-consequence paths.

## Successor trust cannot bootstrap solely from the compromised root
The central recovery problem is successor establishment. If root R is suspected attacker-controlled, `R signs R2` only proves that the holder of R approved R2 — precisely the fact no longer trusted.

A successor emergency authority therefore needs a surviving recovery basis outside the compromised failure domain. Depending on the real architecture this could involve independently governed custody, provider recovery, organizational identity/proofing, pre-established alternate roots or another governed mechanism. This study deliberately does **not** prescribe a specific quorum, HSM, key ceremony, provider, human role or cryptographic construction.

Generic requirements:
- recovery authority was established before or independently of the compromised authority, or is re-established through a separately trusted process;
- successor generation is explicitly new and cannot inherit old emergency sessions/tokens merely because subject names match;
- recovery evidence identifies what trust was relied upon and what remained outside the suspected failure domain;
- any unavoidable residual dependence is recorded as risk, not disguised as independence.

## Credential recovery is not authority recovery
Recovery layers remain separate:
- recover/rebind human authenticator;
- re-establish approver eligibility;
- repair approval policy/control plane;
- establish successor emergency authority generation;
- terminate/reconcile prior sessions and bearer artifacts;
- restore independent observation/audit;
- prove regional enforcement/convergence;
- conduct post-reconstitution review.

A person regaining account access does not automatically regain emergency authority. Likewise, restoring an IdP or vault does not prove that their pre-compromise contents are authoritative.

## Sessions, tokens and replay after root rotation
Successor trust must address artifacts minted before/during compromise. Generic direction:
- do not rely only on key replacement if old bearer/session artifacts remain accepted;
- bind admission to current emergency/security generation where the implementation can enforce it;
- treat ambiguous artifacts minted inside the compromise window according to actual threat/evidence rather than timestamps supplied by an untrusted client;
- reauthentication alone is insufficient if the authorization generation or approval state is stale;
- delayed queue items are re-admitted against current authority at consequence time.

No universal token lifetime or session-invalidation mechanism is prescribed; Software Engineering must validate the real stack.

## Multi-region convergence and rollback resistance
Emergency-root reconstitution is distributed security state:
1. successor trust authorized through surviving recovery authority;
2. successor generation published;
3. each region admits it and rejects superseded compromised authority according to the incident floor;
4. sessions/tokens/queues are reconciled;
5. actual consequence-path enforcement is probed;
6. progressive reopen occurs only where proof is sufficient.

A region that cannot establish the current floor is `UNKNOWN`, not implicitly safe. PITR/backup restoration cannot lower the incident floor or reactivate a compromised emergency generation. Provider/config rollback must reconcile before privileged traffic reopens.

## Evidence-plane compromise
If the emergency operator or attacker could alter the only logs, absence of suspicious entries is weak evidence. Reconstitution should therefore distinguish:
- evidence known intact;
- evidence suspected altered;
- evidence unavailable;
- evidence reconstructed from independent sources.

Do not fabricate certainty. Historical audit repair may create new provenance about the repair; it does not retroactively make missing original evidence authentic.

Privacy minimization still applies: record security-relevant generation, capability, reason class, approval/use/revocation/recovery and outcome metadata where needed, not unnecessary user content or raw flight payloads.

## PWA / managed-iPad transfer
A LogMate-like PWA must survive privileged trust reconstitution without turning stale browser state into authority.

- Preserve unique local flight/logbook records and drafts.
- Treat cached emergency/recovery state in Service Worker, Cache Storage or IndexedDB as observation/presentation state only.
- If an emergency root rotates while the iPad is offline, the old root does not remain usable for new remote consequences merely because the device did not receive the event.
- On reconnect, establish current server security generation before privileged queue drain.
- Queue items authored while the old authority appeared valid are re-admitted under current policy; same-user recovery does not automatically grandfather them.
- Service Worker update, application update, data/schema migration, identity recovery and emergency-authority reconstitution are separate transitions.
- No generic claim is made that iPadOS background execution, push, MDM or device ownership propagates revocation/recovery reliably. Physical Safari/Home Screen/MDM validation remains OPEN.

## UX transfer — Track B
User/operator-facing states should communicate consequence without exposing recovery secrets:
- `Privileged actions are temporarily suspended while access is being re-established.`
- `Your work is saved on this device; submission is paused.`
- `Re-authentication or approval is required before this action can continue.`
- `Access has been re-established; pending actions are being checked before submission.`

Do not claim `everything is safe` merely because login works again. Do not imply local-data loss when only remote privileged authority is suspended. Accessible status, focus behavior, non-color signaling, screen-reader and representative-human validation remain OPEN.

## MINTTAP DECISION — generic governance
1. Treat emergency-authority compromise recovery as trust reconstitution, not simple credential rotation.
2. A compromised emergency/recovery root cannot be the sole authority that approves its own successor.
3. Keep authenticator recovery, approver eligibility, approval-policy repair, successor emergency authority, session invalidation, evidence recovery and regional convergence distinct.
4. Advance a rollback-resistant incident/security generation when compromise requires revocation of inherited privileged state.
5. Require current server-side admission for consequence-bearing privileged operations; browser/PWA cache cannot preserve old emergency authority.
6. Preserve unique offline local data independently from privileged authority state.
7. Re-admit queued operations after reconstitution rather than automatically replaying them because they were authored earlier.
8. Treat compromised/missing audit evidence as compromised/UNKNOWN, not clean.
9. Reopen progressively only after actual enforcement/reconciliation evidence, not merely successful credential rotation or endpoint health.
10. Do not invent MintTap/LogMate recovery roots, quorum, credential form, compromise windows, session lifetimes, provider behavior, legal/aviation authority or physical-iPad behavior.

## VALIDATION — 192-case destructive campaign
Families include: emergency credential copied; authenticator lost/stolen; session token stolen; approver account takeover; approval-policy admin compromised; vault/recovery code compromise; recovery-root compromise; attacker rotates root; old root signs successor; compromised IdP rebinds approver; same actor controls recovery quorum; independent root unavailable; provider support impersonation; evidence plane tampered; logs deleted; telemetry outage; compromise-window timestamp ambiguity; old session survives rotation; bearer replay; region accepts old generation; region misses revoke; split-view successor roots; DNS/control-plane outage during recovery; PITR resurrects old root; backup restore contains old sessions; configuration rollback; stale CDN; stale Service Worker/IndexedDB; long-offline iPad; reconnect after multiple emergency generations; queue authored pre-compromise and committed post-recovery; client clock rollback; delayed push; Shared iPad account switch; MDM ownership mistaken for authority; local data incorrectly deleted; reauthentication mistaken for reauthorization; new credential but stale approval policy; new root but stale audit plane; false-green recovery probe; progressive reopen relapse; inaccessible recovery state; screen-reader/human misunderstanding; privacy-heavy incident logging; post-recovery review skipped.

Generic campaign definition is PASS. Product/runtime/device/human execution remains OPEN.

## TRANSFER VALIDATION / CONTRADICTION
- **TRANSFER VALIDATION:** 178 supplies bounded break-glass and approval-independence boundaries; 173–177 supply convergence, recovery proof, exception provenance, rollback resistance and local-data preservation.
- **TRANSFER VALIDATION:** NIST SP 800-63B-4 establishes authenticator lifecycle/recovery as security-sensitive and the current 800-63-4 suite keeps identity/authentication/federation concepts distinct.
- **TRANSFER VALIDATION:** OWASP Broken Access Control keeps exceptional/recovery routes subject to server-side deny-by-default authorization.
- **TRANSFER VALIDATION:** CISA compromise response precedent supports credential reset plus additional privileged-account remediation after compromise, while remaining incident-specific.
- **CONTRADICTION:** `rotate the break-glass password/key and trust is restored` is rejected.
- **CONTRADICTION:** `the compromised root signed the new root, therefore succession is trustworthy` is rejected.
- **CONTRADICTION:** `the same operator successfully logged in again, therefore old privileged queues/sessions are safe` is rejected.
- **CONTRADICTION:** `PITR restored the old emergency configuration, therefore it is valid again` is rejected.
- **CONTRADICTION:** `the offline iPad never saw revocation, therefore its cached emergency authority remains valid` is rejected.

## OPEN / DEPENDENCY / CHANGE WATCH
OPEN: actual MintTap/LogMate emergency/recovery architecture, compromise classes, consequence taxonomy, credential/authenticator technologies, approver/recovery roots and failure domains, provider support/recovery, key/session/token representation, authoritative time, regional topology, rollback/PITR semantics, audit/evidence stack, legal/aviation constraints, managed-iPad/Safari/MDM behavior and human/AT evidence.

DEPENDENCY — Software Engineering: validate the actual implementation's credential/session invalidation, generation binding, successor-root establishment, anti-replay, queue re-admission, region convergence, rollback/PITR resistance, evidence protection and progressive reopen. Generic web research does not prove any concrete implementation.

DEPENDENCY — Design Studio: validate accessible compromise/recovery/local-preservation/submission-paused/recheck semantics. Current Web Design evidence remains Stage 3 PRACTICE / NOT PASSED; physical-device/PWA, screen-reader and representative-human evidence remain OPEN.

CHANGE WATCH: NIST 800-63/800-53 lifecycle guidance, CISA privileged/emergency-access guidance, OWASP access-control guidance, provider privileged-recovery mechanisms, browser session/security behavior and Safari/iPadOS PWA/MDM behavior.

## Gate
**179 PASS (generic).** Web Manager can now model emergency-path compromise as trust reconstitution rather than credential rotation; reject self-blessed successor roots; separate human authenticator recovery from emergency authority, session, approval-policy and evidence recovery; require rollback-resistant regional convergence before privileged reopen; preserve unique local PWA data while stale privileged state is contained; and keep product/runtime/security/legal/device claims OPEN.

Next adjacent bottleneck: **PWA emergency trust reconstitution ceremony, recovery-root survivability & organizational succession** — determine how pre-established recovery authority survives personnel/provider/organization loss, how custody transfer avoids both orphaned authority and unilateral takeover, how recovery evidence is made independently verifiable, and how long-offline managed devices converge without importing obsolete emergency credentials.