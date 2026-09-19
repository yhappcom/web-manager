# 166 — PWA Policy-Decision Explainability, Provenance Minimization & Contest/Appeal Correction

Status: **PASS (generic) / PRODUCT + LEGAL + POLICY-RUNTIME + HUMAN/AT + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track B explanation/contest UX; Track C validation; Track A offline/currentness mechanics; Track D bounded downstream correction.  
Dependencies: 159–165 closure/deletion/retention/policy lineage, especially 164 policy convergence and 165 issuer compromise/correction.

## Why this study exists

164–165 establish that deletion/retention outcomes are versioned policy decisions and that authentic policy can still be stale, compromised or semantically wrong. The next failure mode is human: a user or operator sees `restricted`, `not deleted`, `revalidation required`, or a corrected outcome but cannot understand why, cannot challenge an incorrect applicability fact, or is shown so much internal/legal/security material that the explanation itself becomes a privacy/security incident.

Central rule:

> **A consequence-bearing policy outcome needs a truthful, usable reason and correction path, but explanation is a purpose-limited projection of authoritative decision provenance — not a dump of the legal file, threat model, policy engine trace, privileged review, or personal-data history. A successful contest creates a new corrective decision generation and downstream reconciliation; it does not rewrite the old decision out of history.**

## Five-track balance and allocation

- **A Platform/Browser:** dependency supplier. Cached/offline explanation can be historically authentic yet stale; SW/IndexedDB cannot decide legal applicability or current appeal status.
- **B UX/IA/Content:** high dependency pressure. Owns plain-language reason hierarchy, challenge path, status/progress, accessibility and distinction between user-facing explanation and internal evidence.
- **C Performance/Accessibility/Quality:** high dependency pressure. Owns wrong-reason, stale-reason, inaccessible contest, correction propagation and sensitive-detail leakage tests.
- **D Search/Discovery/Analytics:** bounded consumer. Derived systems receive corrected disposition; analytics may measure aggregate workflow health but must not become a permanent subject-level legal/appeal dossier.
- **E Architecture/Security/Operations:** **bottleneck/owner**. Owns reason provenance, authorization/currentness, minimum disclosure, contest lifecycle, correction lineage, downstream reconciliation and incident boundaries.

No separate legal doctrine is invented. Product/jurisdiction applicability remains OPEN.

## SOURCE

### NIST security/privacy controls

NIST SP 800-53 Rev.5 remains the current final control catalog, with Release 5.2.0 issued in 2025. Its integrated PII Processing and Transparency family is useful as a control/governance source, not as a claim that MintTap is federally required to implement the catalog. SP 800-53A Rev.5 provides assessment procedures for the same control model.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

The NIST redress model is especially transferable: effective redress includes plain-language mechanisms for requesting access/correction, resources to adjudicate requests, means to correct/amend data, reasons for denied correction, a way to record objections, and review/appeal of initial determinations. The durable engineering lesson is that redress is a lifecycle with explanation, evidence intake, adjudication and correction — not merely a support inbox.

### NIST Privacy Framework

NIST Privacy Framework 1.0 is a voluntary, technology- and jurisdiction-agnostic privacy-risk framework. It frames privacy risk around problems individuals can experience from data processing across the lifecycle. This supports evaluating explanation/contest records themselves as data-processing operations with privacy consequences.

Sources:
- https://www.nist.gov/privacy-framework/privacy-framework
- https://www.nist.gov/privacy-framework/getting-started-0

**CHANGE WATCH:** NIST's Privacy Framework page currently exposes Privacy Framework 1.1 as an Initial Public Draft; do not treat 1.1 as the final baseline until NIST finalizes it.

### EDPB / ICO transfer evidence

EDPB's current data-subject-rights guidance identifies rights to information, access, rectification, erasure, restriction, objection and, in applicable cases, protections around solely automated decisions. It also says organizations should establish procedures that facilitate rights requests. Its SME guidance notes that where corrected personal data was passed to third parties, recipients generally need to be informed of the rectification unless impossible or disproportionate.

Sources:
- https://www.edpb.europa.eu/topics/key-gdpr-concepts/data-subject-rights_en
- https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en

ICO's current rectification guidance says organizations should investigate accuracy challenges, consider the individual's evidence, and either correct/delete/complete the data or explain why correction is refused; it also discusses notifying recipients of correction. ICO separately emphasizes meaningful transparency rather than tick-box notice. Current UK guidance is under review following the Data (Use and Access) Act, so exact UK-law conclusions are CHANGE WATCH and remain outside this generic gate.

Sources:
- https://ico.org.uk/for-the-public/your-right-to-get-your-data-corrected/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-rectification
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-is-the-right-to-be-informed-and-why-is-it-important/

## SYNTHESIS — four distinct records

Do not collapse these into one blob:

1. **Authoritative decision record** — decision generation, policy generation, scoped inputs, disposition, issuer/authority/currentness and predecessor/supersession lineage.
2. **User/operator explanation projection** — minimum reason category, affected operation/data scope, current status, what can be done next, currentness/revalidation state.
3. **Contest/redress record** — challenge identity, challenged decision generation, claimed incorrect fact/reason, evidence references, adjudication state and outcome.
4. **Privileged/sensitive review evidence** — legal analysis, security incident details, internal investigations or third-party confidential material where such material actually exists.

The fourth category is not automatically present and must not be invented. Where it exists, it does not automatically belong in categories 1–3.

Persistent guards:
- `explanation available ≠ all internal evidence disclosed`;
- `reason withheld in detail ≠ no meaningful reason can be given`;
- `policy engine trace ≠ user explanation`;
- `legal citation ≠ plain-language explanation`;
- `user-facing explanation ≠ legal advice`;
- `contest submitted ≠ challenged decision suspended`;
- `contest pending ≠ destructive action remains safe`;
- `appeal won ≠ old decision never existed`;
- `corrected input ≠ downstream effects automatically corrected`;
- `recipient notified ≠ recipient converged`;
- `analytics event recorded ≠ redress evidence retained appropriately`;
- `offline explanation authentic ≠ explanation current`.

## Explanation model: disclose consequence and controllable reason, not the whole case file

A generic explanation projection should be capable of answering, where supported by current authority:
- **What happened?** e.g. deletion is not currently authorized / remote change paused / data retained under a current disposition.
- **What is affected?** a bounded record/operation category, not unnecessary sensitive detail.
- **Why at a useful level?** a stable reason class such as `retention obligation active`, `policy revalidation required`, `conflicting authority under review`, `request facts need verification`, or `decision corrected/superseded`.
- **What can the person do?** provide/correct facts, request review, wait for revalidation, export preserved local data where authorized, or contact the designated review channel.
- **Is this current?** decision/explanation generation and a visible stale/revalidation state where relevant.

Do not expose signing-key identifiers, internal security topology, attacker hypotheses, privileged legal reasoning, third-party personal data, secret hold criteria, or full policy-engine traces merely to appear transparent.

## Reason codes and prose

Use a two-layer pattern:
- a stable internal **reason class/code** for machine reconciliation and regression testing;
- localized plain-language explanation generated from an approved content mapping for the current decision generation.

The code must not itself encode sensitive subject facts. Avoid identifiers such as `HOLD_CRIMINAL_INVESTIGATION_...` when a less revealing scoped class suffices.

`reason code stable ≠ wording immutable`: user-facing wording can improve without changing the underlying authoritative outcome, but content/version provenance should make it possible to know what explanation was actually presented when consequence matters.

## Contest / appeal lifecycle

Generic lifecycle:

`DECIDED → EXPLAINED → CONTESTED → IN_REVIEW → UPHELD | CORRECTED | PARTIALLY_CORRECTED | UNRESOLVED → NOTIFIED → RECONCILING → CONVERGED`

This is conceptual, not a required product enum.

### Contest intake
Bind the challenge to the exact decision generation and affected scope. Accept correction of applicability facts/evidence without forcing the user to know internal policy names or legal citations.

### Safety while pending
Whether an operation is paused during review is consequence-specific. Do not infer a universal legal stay. For irreversible/high-consequence destruction where material applicability is genuinely unresolved, the existing 164–165 safety model favors governed restriction/review over destructive guessing while preserving unique data. Exact product/legal behavior remains OPEN.

### Adjudication
The reviewer needs current authoritative policy/evidence, not only the snapshot that produced the challenged outcome. Separate factual correction from policy interpretation and from issuer compromise. A user proving an address/date/account fact wrong does not prove the policy itself invalid; a policy correction does not imply the user's prior evidence was false.

### Correction
Correction is forward-only. Create a new decision generation that references/supersedes the challenged generation and records the minimum correction provenance. Do not mutate the old row into `always correct` or delete the existence of the adverse decision where history must remain auditable.

### Propagation
A corrected disposition triggers the existing effect-reconciliation machinery: primary record, queues/jobs, search/index, analytics-derived processing, exports/import admission, offline fleet and external recipients/processors as applicable. `correction committed centrally ≠ correction propagated`.

## Provenance minimization

A redress system can become a more sensitive dossier than the underlying product data. Minimize by separating:
- opaque decision/contest identifiers from user-visible prose;
- structured reason class from free-text evidence;
- evidence reference from evidence payload;
- operational workflow telemetry from adjudication content;
- current explanation from historical privileged review material.

Avoid retaining every screen, chat, location, device fingerprint, legal memo and reviewer note merely because a contest occurred. Retention should be purpose/scoped and governed under the same deletion/hold framework studied in 162–165.

Free-text contest input is high-risk: it may contain health, employment, aviation, financial or third-party information not otherwise required. Constrain prompts, provide structured fields where possible, warn against unnecessary third-party/sensitive content, and isolate access.

## Security and abuse boundary

Explanation can leak security posture. During issuer compromise or incident response:
- say `policy revalidation required` or equivalent when that is all that is established;
- do not identify an attacker or compromised credential before evidence supports it;
- do not expose exact anti-rollback floor, key topology or bypass conditions;
- rate/abuse controls must not silently erase legitimate challenge paths;
- support agents cannot become an alternate policy-authority path simply because they can edit explanation text.

`support can explain ≠ support can authorize disposition`.

## PWA / long-offline iPad

A long-offline company iPad may hold an explanation generated under decision D and policy P even after server state has advanced to D+1/P+1.

On reconnect:
1. preserve unique unsynced local flight/user data;
2. treat cached explanation as historical UI evidence, not current policy authority;
3. obtain current trust/policy/decision floor outside cached SW state;
4. if D was contested/corrected while offline, present `superseded/corrected` rather than silently replacing history;
5. quarantine stale consequence-bearing queued operations until current decision admission;
6. allow a locally drafted contest to sync as a request, but do not let device time or offline UI mark it adjudicated;
7. do not let stale reason text reveal privileged details that current policy no longer permits;
8. keep accessibility and export/recovery paths usable while remote mutation is restricted.

Service Worker update and explanation refresh are distinct from policy/trust migration.

## UX / accessibility transfer to Track B and Design Studio

The explanation surface should provide:
- a concise current state heading;
- plain-language primary reason;
- affected scope;
- next available action/review path;
- current/pending/corrected/superseded status;
- non-color-only status cues;
- keyboard/touch operability and durable focus after async status updates;
- status announcements that do not repeatedly spam assistive technology;
- recovery after offline/retry without duplicate contest submission.

Design Studio remains canonical for reusable visual/interaction patterns. Web Manager supplies the state semantics and evidence requirements, not a new visual system.

## Track D transfer

Search/index and analytics do not decide appeals. They consume corrected disposition. Measurement should prefer aggregate workflow metrics such as request volume, age bands, failure rates and propagation latency rather than permanent subject-level reason histories. Do not use analytics identifiers as the canonical contest/evidence key.

## MINTTAP DECISION — generic governance

1. Treat explanation as a minimum-disclosure projection of authoritative decision provenance, not a policy/legal/security dump.
2. Bind explanation and contest to explicit decision/policy generations and affected scope.
3. Maintain a usable challenge/review path for consequential policy outcomes where applicable; exact legal rights remain jurisdiction/product specific.
4. Separate factual correction, policy correction and issuer/security compromise.
5. Correct forward with a new decision generation; preserve supersession lineage.
6. Trigger downstream effect reconciliation after correction; central correction alone is not convergence.
7. Keep privileged/sensitive review evidence separate and access-controlled; do not copy it into user-visible or analytics records.
8. Minimize free text and subject-level telemetry; explanation/redress records themselves are privacy-governed data.
9. Cached/offline PWA explanation never establishes current authority; preserve unique local data during revalidation.
10. Keep actual legal applicability, review authority, SLA, schema, reason taxonomy and managed-device behavior OPEN until canonical product/legal/runtime evidence exists.

## VALIDATION — 84-case destructive explainability/redress campaign

1 current decision has reason class; 2 reason prose maps correctly; 3 explanation names affected scope; 4 explanation has next action; 5 no internal key topology leak; 6 no privileged legal memo leak; 7 no third-party PII leak; 8 generic reason not misleading; 9 reason wording localization; 10 untranslated fallback remains understandable; 11 long reason reflows; 12 200% zoom; 13 text spacing; 14 keyboard reaches review action; 15 touch target usable; 16 focus retained after async update; 17 status announced once; 18 no AT spam; 19 reason cannot be color-only; 20 support agent changes prose only; 21 support cannot change disposition; 22 user contests exact D generation; 23 user does not know policy ID; 24 contest still valid; 25 structured fact correction accepted; 26 unnecessary free text avoided; 27 free text contains third-party data; 28 access/minimization controls apply; 29 duplicate submit retry; 30 idempotent request identity; 31 ACK lost; 32 no duplicate adjudication; 33 contest pending; 34 irreversible action handling follows current governed policy; 35 contest does not invent universal stay; 36 reviewer uses current policy; 37 stale review snapshot detected; 38 factual error corrected; 39 policy remains valid; 40 policy error corrected; 41 user evidence not falsely discredited; 42 issuer compromise discovered; 43 separate incident path; 44 correction creates D+1; 45 D retained as superseded history; 46 explanation D+1 says corrected; 47 old explanation marked historical; 48 primary projection corrected; 49 queued job stale; 50 re-authorize/reconcile; 51 search index stale; 52 reconcile; 53 analytics derived processing stale; 54 reconcile/minimize; 55 external recipient notified where applicable; 56 notification ACK missing; 57 do not claim convergence; 58 recipient impossible to reach; 59 bounded unresolved state; 60 old export contains D; 61 import cannot resurrect disposition; 62 PITR restores D; 63 current floor restores D+1; 64 old SW shows D reason; 65 cannot establish authority; 66 IndexedDB has D contest state; 67 migrate/reconcile; 68 offline iPad drafts contest; 69 preserve locally; 70 reconnect submits request; 71 device clock not adjudication proof; 72 contest resolved while device offline; 73 reconnect shows superseded/corrected; 74 unique unsynced flight data remains exportable; 75 remote mutation remains gated; 76 policy service unavailable; 77 truthful revalidation state; 78 no attacker attribution without evidence; 79 rate limiting under abuse; 80 legitimate challenge path remains; 81 aggregate analytics has no legal memo; 82 deletion/retention applies to contest dossier; 83 physical Safari/iPad + screen-reader/human validation OPEN; 84 actual MintTap/LogMate legal/product workflow OPEN.

## OPEN / CHANGE WATCH

OPEN: actual MintTap/LogMate decision schema; policy/reason taxonomy; legal-review and appeal authority; jurisdiction-specific rights and response times; privileged-material rules; external recipients/processors; notification channels; support roles; analytics schema; local/offline contest persistence; managed-iPad/WebKit behavior; physical-device, screen-reader and human comprehension evidence.

CHANGE WATCH: NIST Privacy Framework 1.1 draft progression; NIST SP 800-53 updates; EDPB guidance; UK ICO guidance following the Data (Use and Access) Act; browser/WebKit offline/storage/update behavior; applicable Korean/EU/UK/aviation rules if product scope requires them.

## Gate result

**PASS (generic).** Web Manager can now distinguish authoritative decision provenance, minimum user explanation, contest/adjudication records and privileged evidence; design a forward-only correction/reconciliation lifecycle; and apply it to stale/offline PWA state without claiming unknown legal or product facts.

## Adjacent-value check

The directly adjacent unresolved question is no longer basic explanation. It is **redress identity, authorization and anti-abuse without exclusion**: how to verify that a person/device/authorized representative may inspect or challenge the relevant decision without turning identity proofing into excessive data collection, while preventing account-takeover attackers, abusive automation and support impersonation from learning or mutating sensitive policy state. This is a materially distinct identity/security block and is the next high-value target.