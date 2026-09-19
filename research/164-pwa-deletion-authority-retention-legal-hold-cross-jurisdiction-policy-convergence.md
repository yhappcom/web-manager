# 164 — PWA Deletion Authority, Retention/Legal-Hold Precedence & Cross-Jurisdiction Policy Convergence

Status: **PASS (generic) / PRODUCT + LEGAL + AVIATION + PROVIDER + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 013 legal-trigger registry; 159 bounded closure; 162 destruction/redaction; 163 deletion propagation/backup expiry/offline resurrection; Track A offline/SW/storage mechanics; Track B truthful state UX; Track C destructive policy-convergence validation; Track D minimised measurement.  
External transfer: Design Studio W113 production-closure matrix; Software Engineering Studio foundation evidence including M006 generic Chromium service-worker/offline transfer. Neither is promoted to product/Safari/EFB PASS.

## Why this study exists

163 established that deletion is a bounded claim over controlled domains and that stale backups, exports and offline devices must not resurrect intentionally unavailable lineage. The adjacent failure is treating deletion intent as if it always authorizes immediate destruction.

Real systems can receive simultaneously valid but differently scoped inputs: a user deletion request, an ordinary retention expiry, a statutory preservation requirement, litigation/evidence preservation, security-incident preservation, or a product-specific record-retention rule. The Web/PWA client is not a legal decision-maker and cannot safely collapse these into `delete=true` or `keep=true`.

Central rule:

> **Deletion intent, destruction authority and retention authority are distinct. A governed policy outcome must be computed by an authoritative policy plane from verified, scoped and current obligations; clients enforce the outcome but do not invent legal precedence. Holds suppress otherwise-authorized destruction only for their justified scope and lifetime, and release of the last applicable hold must trigger a fresh current-policy decision rather than silently restoring the pre-hold state.**

This is systems/security governance, not legal advice. Exact jurisdiction, aviation, tax, employment, investment, litigation and product obligations remain OPEN until actual product facts and qualified review establish them.

## Five-track balance and allocation

- **A Platform/Browser — critical dependency supplier:** owns SW lifecycle, Cache/IndexedDB/OPFS/local export and reconnect mechanics. Browser state can cache an outcome but cannot determine legal authority or policy precedence.
- **B UX/IA/Content — high dependency pressure:** owns truthful distinctions among deletion requested, restricted/held, deletion eligible, deletion executing, completed, unknown/conflict and local-copy reconciliation. It must not expose sensitive hold reasons unnecessarily.
- **C Performance/Accessibility/Quality — high pressure:** owns destructive conflict/release/reconnect/restore tests, semantic state announcements and negative tests against premature destruction or indefinite retention.
- **D Search/Discovery/Analytics — bounded consumer:** derived stores consume authoritative disposition; analytics must not infer legal status or retain a subject-level global hold graph without necessity.
- **E Architecture/Security/Operations — highest-risk owner:** owns policy inputs, scope, currentness, precedence mechanism, hold lifecycle, release/re-evaluation, restore/offline gates and audit evidence.

Allocation remains E-heavy, with A/C as execution dependencies and B as the main truthfulness dependency. Legal interpretation is explicitly outside the Web Manager's authority.

## SOURCE

### Korea — destruction is not unconditional when another law requires preservation

Korea's Personal Information Protection Act, effective 2026-09-11, Article 21 states that personal information that becomes unnecessary because the retention period expired or the processing purpose was achieved must be destroyed without delay, **except where another law requires preservation**. Where that exception applies, Article 21(3) requires the retained personal information/file to be stored and managed separately from other personal information. Article 21(2) requires destruction to prevent recovery or reproduction.

Primary source:
- https://law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0021&lsiSeq=283839&urlMode=lsScJoRltInfoR

Article 36 provides a data subject's correction/deletion request route and states that the controller must investigate and take necessary action without delay except where another law provides a special procedure. This does not authorize a web client to decide what other law applies.

Primary source:
- https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1033214661

**TRANSFER VALIDATION:** Korean law itself demonstrates that `deletion requested/retention expired` and `destruction currently authorized` can differ. The durable architecture lesson is to represent the applicable preservation basis and scope outside the client, isolate retained data appropriately, and re-evaluate when the basis ends. Exact MintTap/LogMate obligations remain OPEN.

### EU/UK — erasure rights coexist with legal obligations and legal claims

European Commission GDPR guidance states that personal data should be stored no longer than necessary, while retention periods must account for legal obligations requiring fixed preservation periods. Its rights guidance states that erasure is not obligatory where data is needed because law requires retention or for the exercise of legal claims. Restriction of processing is a distinct state: in specified circumstances storage may continue while further processing is constrained.

Sources:
- https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en
- https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/dealing-requests-individuals_en

The UK ICO likewise states that the right to erasure does not apply where processing is necessary to comply with a legal obligation or for establishment, exercise or defence of legal claims.

Source:
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/

The EDPB's 2025 coordinated-enforcement report, published in 2026, specifically notes that controllers may reject erasure to the extent data is necessary for a legal obligation and identifies the interaction between retention periods and erasure as an area requiring careful implementation.

Source:
- https://www.edpb.europa.eu/system/files/2026-02/edpb_cef-report_2025_right-to-erasure_en.pdf

**TRANSFER VALIDATION:** these sources support a general systems distinction among erasure intent, lawful retention/restriction and eventual destruction. They do **not** establish that GDPR/UK GDPR applies to MintTap/LogMate, nor do they establish aviation-record obligations.

## History/problem → design principle

A naive implementation commonly has one of two dangerous shapes:

1. `userRequestedDeletion = true → delete everywhere`; or
2. `legalHold = true → retain everything indefinitely`.

The first can destroy data that current authority requires to be preserved. The second turns an exception into silent permanent retention and violates minimization/expiry discipline.

The design principle is **scoped policy convergence**:
- collect verified policy inputs;
- bind each input to data scope, purpose, jurisdiction/authority basis, start/currentness and release/expiry semantics;
- compute one authoritative operational disposition for each affected lineage/scope;
- expose only that disposition to ordinary clients;
- preserve provenance sufficient to explain why a disposition existed without turning the policy system into a privacy-rich dossier;
- recompute when any material input changes.

## SYNTHESIS — separate four things that are often collapsed

### 1. Deletion intent
A request or lifecycle event saying data should be removed if no superior/current preservation basis applies.

Examples: user request, account closure, purpose completion, retention-period expiry. This is an input, not proof that destruction is currently authorized.

### 2. Retention/hold authority
A verified current basis requiring or permitting defined data to remain unavailable for ordinary use but preserved for a bounded purpose/scope. The legal meaning is external to client code.

### 3. Operational disposition
The current server-authoritative result, for example:
- `DELETE_ELIGIBLE`
- `RESTRICTED_HELD`
- `DELETE_EXECUTING`
- `DELETED_SCOPED`
- `REVIEW_REQUIRED`
- `POLICY_CONFLICT_UNKNOWN`

These are generic semantic examples, not a mandated schema.

### 4. Physical propagation/destruction state
Whether primary stores, replicas, indexes, backups, managed clients and other controlled domains have actually converged to the disposition. 163 owns this layer.

Persistent guards:
- `deletion requested ≠ destruction authorized`;
- `retention required ≠ ordinary processing allowed`;
- `hold active ≠ retain every related byte`;
- `hold released ≠ delete immediately without re-evaluation`;
- `one jurisdiction says retain ≠ every jurisdiction/data scope says retain`;
- `client locale ≠ governing jurisdiction`;
- `device location ≠ sufficient legal applicability fact`;
- `policy input authentic ≠ policy input current`;
- `policy engine produced outcome ≠ legal interpretation proven correct`;
- `restriction/hold ≠ silent normal availability`;
- `last hold removed ≠ pre-hold policy state restored`.

## Policy input model

A reusable policy input should be able to carry, at minimum:
- opaque policy/obligation identifier;
- authority/source class and version;
- applicable data/record/subject scope;
- purpose for which retention or deletion is allowed/required;
- jurisdiction/applicability facts or a reference to the approved legal determination;
- effective-from/currentness generation;
- expiry, release condition or explicit `no automatic expiry` state;
- ordinary-use restrictions while held;
- downstream/backup implications where known;
- evidence provenance and responsible owner;
- review/change-watch trigger.

Do not place raw legal memoranda, unnecessary personal details or secret investigation facts in browser-readable policy objects.

### Authority boundary

The authoritative policy plane may consume legal/compliance decisions, but the browser/PWA receives a minimum operational outcome. A Service Worker should not contain a table such as `EU => delete, KR => retain`, and device GPS/locale should not choose the legal rule.

`browser policy cache = enforcement hint/state`, not legal authority.

## Precedence without hard-coding legal conclusions

The system needs deterministic conflict handling, but a generic technical precedence such as `HOLD always beats DELETE` is too broad if `HOLD` itself is stale, forged, over-scoped or no longer applicable.

A safer sequence is:
1. authenticate each policy input and its issuer/owner;
2. verify currentness/version and applicability scope;
3. reject expired/revoked/superseded inputs;
4. detect unresolved contradictions rather than choosing by client-side priority;
5. compute the current operational disposition under an approved policy rule set;
6. bind the result to a monotonic disposition/deletion generation;
7. require downstream systems and reconnecting clients to enforce that generation.

If the authoritative plane cannot resolve a material conflict, consequence-bearing destruction should enter `REVIEW_REQUIRED` / `POLICY_CONFLICT_UNKNOWN`, not guess. This fail-safe must itself have an owner, review SLA and expiry/escalation path so uncertainty does not become permanent retention.

## Hold lifecycle

Generic lifecycle:

`PROPOSED → VERIFIED/APPLICABLE → ACTIVE → MODIFIED/SUPERSEDED → RELEASED/EXPIRED → RETIRED`

Side states:
`DISPUTED`, `UNKNOWN`, `REVOKED`, `EVIDENCE-STALE`.

### Activation
Activation must identify scope and ordinary-use restrictions. A hold on one record class must not silently freeze an entire account if that is not justified by the authoritative decision.

### While active
Held data should be isolated or access-restricted according to the applicable policy. Korea PIPA Article 21(3) provides a concrete example of separate storage/management when preservation is required by another law; other regimes may use different mechanisms.

### Release
Release is an event, not deletion authority. On release:
1. create a new policy/disposition generation;
2. re-evaluate all remaining current obligations and purposes;
3. if deletion is now authorized, create/advance the deletion generation;
4. propagate under 163's bounded-deletion model;
5. retain minimum release/re-evaluation provenance;
6. prevent old hold snapshots/backups/offline clients from reasserting the retired hold as current authority.

`hold released ≠ old deletion request forgotten` and `hold released ≠ immediate destructive guess`.

## Multiple jurisdictions and policy convergence

Cross-jurisdiction handling is not `pick the strictest law` as a universal algorithm. Different rules can apply to different controller roles, establishments, users, processing purposes, record classes and legal bases. A system must preserve the legal applicability decision as an external governed input.

Generic convergence rules:
- bind obligations to **scope**, not merely country labels;
- allow multiple concurrent obligations for one lineage;
- preserve the source/version of each applicability decision;
- require explicit conflict/review when approved rules cannot derive one operational disposition;
- never infer jurisdiction solely from UI language, IP address, App Store country, device locale or current GPS;
- when an applicability fact changes, issue a new policy generation rather than rewriting history;
- use CHANGE WATCH for law/guidance/provider changes.

### Cross-border/offline consequence

A PWA may be installed in one jurisdiction, used in another and remain offline while policy changes on the server. The local device therefore cannot safely choose a disposition from physical location. It can continue preserving unique local data while withholding destructive/remote-authority actions until it obtains current authoritative disposition.

## PWA / EFB application

### Long-offline company iPad

A LogMate-like iPad may contain:
- remotely replicated records;
- unique unsynced flight records;
- stale deletion requests;
- stale hold/disposition state;
- an old Service Worker and cached UI.

On reconnect:
1. preserve unique local data before destructive reconciliation;
2. obtain current disposition generation from the authoritative plane, not cached SW/IndexedDB state;
3. classify local lineage as unique local, stale remote copy, held/restricted, deletion-eligible or unresolved;
4. block stale upload if current server disposition forbids resurrection;
5. do not auto-delete unique local data merely because a stale local/server marker appears to say `DELETE`;
6. do not auto-republish held/deleted remote lineage merely because local bytes are newer by device clock;
7. surface an accessible reconciliation state when authority is unresolved.

No assumption is made that company iPad MDM, background execution, direct device-to-device sync or remote wipe is available. Those remain product/runtime OPEN.

### Service Worker/update boundary

A Service Worker may cache presentation and network behavior, but:
- old SW cannot extend a released hold;
- new SW cannot manufacture destruction authority;
- SW update does not prove IndexedDB disposition migration;
- offline queue replay must carry lineage/generation and be re-authorized server-side;
- cached `held`/`deleted` UI is not authoritative after reconnect.

## Restore, backup and disaster recovery

A backup can contain both payload and a historical policy state. Restoring both together creates a dangerous time machine.

Before ordinary service reopens:
- recover a non-rollback-prone current policy/disposition floor;
- identify holds released after the snapshot and holds activated after the snapshot;
- re-evaluate restored data against the current floor;
- quarantine records whose disposition is unresolved;
- rebuild search/analytics projections only from reconciled state;
- suppress restored queues/jobs that encode stale policy decisions.

A restored old `ACTIVE HOLD` must not override a later verified release, and a restored old `DELETE_ELIGIBLE` must not destroy data that a later current hold protects.

## B UX / information architecture transfer

User-facing status should communicate operational truth without exposing sensitive legal/investigation detail. Candidate semantic states:
- **Deletion requested — review/processing pending**;
- **Deletion temporarily restricted** — some data is preserved under an applicable requirement; ordinary use may be limited;
- **Deletion eligible** — no current blocking requirement is represented by the authoritative policy outcome;
- **Deletion in progress**;
- **Deletion complete within stated controlled scope**;
- **Policy status requires review**;
- **Offline local copy requires reconciliation**.

The exact copy requires product/legal/design review. Do not display `legal hold` or detailed reasons to every user if that disclosure is not authorized. Accessibility requires semantic status, focus/error handling and non-color-only distinctions. Design Studio W113 still has no production runtime/independent-browser/physical-device/screen-reader/human UX PASS.

## D search/analytics transfer

Search indexes, analytics and support systems consume the disposition; they do not decide it. A held record may need to disappear from ordinary product search while remaining in a restricted preservation domain. Metrics should prefer aggregate counts by state/storage class and avoid permanent subject-level hold dimensions.

`not searchable ≠ destroyed`; `retained for restricted purpose ≠ available for analytics`.

## Software Engineering transfer boundary

Software Engineering Studio currently remains at Foundation across specialists. Its M006 evidence proves a generic controlled Chromium Service Worker can serve explicitly precached content while offline and a negative uncached resource fails under the same emulation. It explicitly does not prove Safari/iPadOS/EFB, LogMate Flutter web, storage eviction, update/restart or production behavior.

Web Manager therefore hands off implementation questions rather than inventing them:
- disposition-generation schema and transaction boundaries;
- server-side admission/replay gates;
- policy-floor durability/restore ordering;
- held-data access isolation;
- offline queue lineage;
- local unique-data classification;
- exact Service Worker/update migration behavior.

## MINTTAP DECISION — generic governance

1. Treat deletion intent, retention/hold authority, operational disposition and physical propagation as separate state dimensions.
2. Keep legal/applicability interpretation outside browser/PWA code; clients consume minimum authoritative outcomes.
3. Represent retention/holds as scoped, versioned, currentness-checked inputs with explicit lifecycle and owner.
4. Do not use country, locale, IP, GPS or App Store region alone as a legal-precedence engine.
5. When verified obligations conflict and no approved rule resolves them, block consequence-bearing destruction and enter governed review; do not silently retain forever.
6. A hold suppresses destruction only for its justified scope/purpose/lifetime and does not authorize ordinary reuse of retained data.
7. Release of a hold creates a new policy generation and mandatory re-evaluation; it neither deletes automatically nor resurrects pre-hold state.
8. Restore/PITR must reconcile both later deletion and later hold/release generations before reopening.
9. Offline clients preserve unique local data under ambiguity but cannot use stale local policy to mutate remote authoritative state.
10. Minimize policy/hold telemetry and user-facing reasons; do not turn compliance evidence into a sensitive global dossier.
11. Exact MintTap/LogMate legal, aviation and jurisdiction-specific conclusions remain OPEN for qualified review and product evidence.

## VALIDATION — 96-case destructive policy-convergence campaign

1 deletion request accepted; 2 no hold; 3 disposition delete-eligible; 4 generation advances; 5 hold arrives before destruction; 6 currentness verified; 7 disposition restricted-held; 8 destruction blocked; 9 held data removed from ordinary search; 10 preservation remains; 11 analytics tries reuse; 12 deny unless separately authorized; 13 hold scoped to one record; 14 unrelated record remains independently evaluated; 15 over-broad account freeze attempted; 16 detect scope defect; 17 forged hold; 18 reject; 19 stale signed hold; 20 reject currentness; 21 hold issuer authority revoked; 22 reject successor use; 23 two current obligations agree retain; 24 deterministic result; 25 two obligations agree delete-eligible; 26 deterministic result; 27 obligations conflict; 28 review-required not destructive guess; 29 review queue unavailable; 30 no silent completion; 31 review ages; 32 escalation/owner required; 33 user locale changes; 34 no legal disposition change from locale alone; 35 device GPS crosses border; 36 no client-side law switch; 37 IP geolocation differs; 38 no authority switch; 39 approved applicability decision changes; 40 new generation recorded; 41 hold expires by configured date; 42 verify actual release/currentness before acting; 43 hold manually released; 44 re-evaluate remaining obligations; 45 another hold remains; 46 keep restricted; 47 last hold released; 48 old deletion intent still present; 49 fresh disposition computed; 50 deletion generation advances if authorized; 51 release event lost to one replica; 52 stale hold cannot dominate newer floor; 53 pre-hold backup restored; 54 later active hold reapplied; 55 held-era backup restored after release; 56 later release floor dominates; 57 old delete-eligible snapshot restored after later hold; 58 no premature destruction; 59 search index restored with held record visible; 60 rebuild/suppress; 61 analytics projection restored; 62 reconcile purpose/disposition; 63 old async delete job restored; 64 server re-authorizes against current generation; 65 old async retain job restored; 66 cannot extend retired hold; 67 offline iPad misses hold activation; 68 reconnect gets current disposition; 69 stale upload conflicts with held/deleted lineage; 70 block ordinary republish; 71 offline iPad has unique unsynced flight record; 72 preserve pending classification; 73 mixed local DB unique+stale copies; 74 classify per lineage; 75 stale SW shows delete complete; 76 current server says held; 77 UI updates without destructive guess; 78 stale SW shows held; 79 current server says released/delete-eligible; 80 stale SW cannot extend hold; 81 IndexedDB contains old policy generation; 82 migration/revalidation required; 83 offline queue lacks generation; 84 reject/quarantine rather than guess; 85 malicious client edits hold state; 86 server ignores client authority claim; 87 policy evidence store unavailable; 88 no consequence-bearing destruction under unknown authority; 89 policy telemetry contains raw legal memo; 90 minimization defect; 91 user status reveals sensitive investigation reason; 92 disclosure defect; 93 keyboard/screen-reader state semantics specified; 94 observed AT/human PASS remains OPEN; 95 physical managed-iPad multi-generation convergence remains OPEN; 96 actual aviation/legal applicability remains OPEN.

## CONTRADICTION / failure modes

### Delete-button absolutism
A user action is treated as immediate destruction authority. This confuses intent with current disposition and can violate preservation requirements.

### Hold absolutism
Any hold-like flag freezes an entire user/account forever. This defeats scope, minimization, expiry and review.

### `Strictest law wins` pseudo-law engine
A developer encodes country labels and picks the longest retention or fastest deletion without an approved applicability analysis. This is not defensible legal reasoning and is brittle under changing facts.

### Client-jurisdiction inference
Locale, IP or GPS changes the retention policy locally. A roaming/offline EFB makes this especially unsafe.

### Release rollback
Removing a hold restores the policy state that existed when the hold began. This ignores later requests, later obligations and changed policy.

### Compliance time machine
PITR restores an old hold/deletion state and ordinary service trusts it before obtaining the current policy floor.

### Indefinite uncertainty
Fail-safe `UNKNOWN` has no owner, review trigger or expiry/escalation, becoming permanent silent retention. Fail-safe operation needs governance, not just blocking.

## OPEN / DEPENDENCY

- Actual MintTap/LogMate legal entity, controller/processor roles and launch jurisdictions: OPEN.
- Actual Korean/EU/UK/US/other applicability: OPEN.
- Actual aviation/airline/employer/authority logbook-record retention requirements: OPEN; no conclusion made here.
- Actual investment/tax/customer-support/security-incident/litigation preservation obligations: OPEN.
- Actual data classes and local-vs-server authority for LogMate flight records: OPEN.
- Actual policy/disposition schema, issuer authority, generation/floor and rollback-resistant storage: OPEN.
- Actual provider object-lock/retention/backup semantics: OPEN.
- Actual Service Worker/IndexedDB/Cache/OPFS/offline queue implementation: OPEN.
- Actual managed-iPad/MDM reachability and deletion/restriction capabilities: OPEN.
- Actual legal-review workflow and user-notification/disclosure constraints: OPEN.
- Actual screen-reader/human UX validation: OPEN.

## CHANGE WATCH

- Korea PIPA and PIPC retention/destruction guidance.
- EU GDPR/EDPB and UK ICO erasure/restriction/retention guidance.
- Any applicable aviation/employment/tax/investment/legal-claims retention rules once product scope is known.
- Browser/WebKit storage/update behavior and managed-web-app/MDM capabilities.
- Provider retention/object-lock/backup/PITR semantics.
- Product decision changing whether local EFB data is authoritative, replicated or cached.

## Gate result

**PASS (generic).** Web Manager can now separate deletion intent from destruction authority and retention authority; model scoped/versioned holds without embedding legal conclusions in PWA clients; require fresh re-evaluation on hold release; prevent restore/offline clients from reviving stale policy; and state cross-jurisdiction uncertainty honestly.

Production/legal/aviation/provider/managed-fleet validation remains OPEN.

## Next highest-value adjacent target

**PWA retention-hold evidence integrity, policy-issuer compromise & emergency legal-policy rollback resistance**: determine how a forged, compromised or mistakenly over-broad hold/deletion policy is contained; how policy issuer/key compromise changes trust in historical dispositions; how emergency correction avoids both destructive rollback and indefinite retention; and how offline clients recover current policy authority without trusting an attacker-controlled predecessor generation.