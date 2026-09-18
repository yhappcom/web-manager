# 133 — PWA Reconciliation Auditability & User-Correction Provenance

Status: **PASS (generic) / PRODUCT + MANAGED-IPAD + DATA-MODEL + PRIVACY/LEGAL VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 131–132 reconciliation/schema evolution; Track B correction/review explanation UX; Track C provenance/replay/privacy oracles; Software Engineering Data D003/D006 for implementation-level migration/sync evidence.

## Purpose

132 established that migration must preserve original intent rather than silently manufacture a current decision. The adjacent problem is what survives after migration, conflict resolution and later correction: can the system explain how the authoritative current state came to exist without retaining an unlimited duplicate history of user data or pretending that every correction rewrites history?

Central rule:

> **Preserve enough provenance to distinguish original intent, automated transformation, conflict decision and later correction; do not confuse an auditable derivation chain with immutable business data, unlimited logging, or heavyweight event sourcing.**

## 1. Five-track balance

- **A Platform/Browser — dependency supplier:** local IndexedDB/worker generations can hold pending provenance, but browser storage availability/persistence is not an audit archive.
- **B UX/IA/Content — elevated consumer:** owns truthful `original / transformed / conflicted / corrected / authoritative` explanation and accessible correction/recovery flows.
- **C Quality — high dependency pressure:** owns lineage completeness, duplicate/replay, compaction, deletion/retention, mixed-generation and privacy-leak oracles.
- **D Search/Analytics — constrained consumer:** operational telemetry may measure correction/reconciliation outcomes, but analytics must not become a shadow provenance database.
- **E Architecture/Security/Operations — highest-risk owner:** owns provenance boundaries, integrity, retention/minimization, authority and incident/audit interpretation.

Allocation remains E-heavy, with B/C pressure elevated because an audit trail that users cannot interpret or that leaks unnecessary content is not a satisfactory control.

## 2. SOURCE — provenance distinguishes entities, activities, agents and derivation

W3C PROV is a domain-agnostic provenance model. Its core distinguishes entities, activities and agents; derivation relates resulting entities to inputs, and responsibility can be associated with agents. Revision is a specialized derivation. PROV also supports invalidation and provenance of provenance.

Sources checked 2026-09-18:
- https://www.w3.org/TR/prov-dm/
- https://www.w3.org/TR/prov-o/
- https://www.w3.org/TR/prov-primer/

**TRANSFER VALIDATION:** MintTap/LogMate does not need to implement PROV-O/RDF. The reusable principle is that current data, transformation activity and responsible actor are different objects. A corrected record should not be modeled as if the original entity never existed when historical derivation matters.

Guards:
- `current value ≠ complete provenance`;
- `revision exists ≠ original entity must remain executable`;
- `actor recorded ≠ actor currently authorized`;
- `provenance model useful ≠ W3C PROV implementation required`.

## 3. Separate correction from mutation, transformation and adjudication

Use distinct semantic event classes:
1. **original intent** — what a user/system actually authored locally, with original schema/policy/base context;
2. **automated transformation** — deterministic migration/normalization into a candidate current representation;
3. **admission/rejection** — current server/domain/security policy decision;
4. **conflict adjudication** — automated or human decision between competing states/intents;
5. **user correction** — a new explicit assertion that changes the authoritative record because the user says the prior/current value is inaccurate or incomplete;
6. **administrative correction** — privileged correction with actor/reason scope;
7. **invalidation/tombstone** — prior entity no longer current/usable, where domain semantics require it.

A user correction is a new decision, not retroactive proof that the earlier value was never entered. An automated migration is not a user correction.

Guards:
- `correction applied ≠ original intent rewritten`;
- `migration transformed value ≠ user corrected value`;
- `conflict resolved ≠ one branch never existed`;
- `current authoritative ≠ historically original`.

## 4. SOURCE — rectification and provenance can coexist with minimization

GDPR Article 5 establishes purpose limitation, data minimisation, accuracy and storage limitation for personal data; Article 16 provides a right to rectification of inaccurate data and completion of incomplete data. Article 17 separately establishes erasure conditions, with specified exceptions. These rules do not establish a universal product retention period or require an immutable history of every edit.

Sources checked 2026-09-18:
- https://eur-lex.europa.eu/eli/reg/2016/679/oj (Articles 5, 16, 17)

**TRANSFER / LEGAL BOUNDARY:** These are EU-law examples relevant to privacy architecture, not a determination that GDPR applies to a particular MintTap/LogMate record or that a specific audit history must be retained. Actual jurisdiction, legal basis, retention and aviation-record obligations remain specialist/legal OPEN.

Operational consequence: provenance must be purpose-bound. Keeping every prior full payload forever merely because it may be useful later can conflict with minimization/storage-limitation principles. Conversely, blindly overwriting all history can destroy evidence needed for recovery, dispute resolution, security or domain obligations.

Guards:
- `auditability required ≠ retain every payload forever`;
- `rectification right ≠ silently rewrite all historical evidence`;
- `historical provenance useful ≠ unlimited retention justified`;
- `data minimization ≠ no provenance`.

## 5. SOURCE — logging must be purpose-specific and protect sensitive data

OWASP Logging guidance distinguishes security/application logs from audit/transaction trails, warns against both too much and too little logging, recommends excluding/masking sensitive data, protecting log integrity and detecting stopped/tampered logging, and states logs should not be kept beyond required retention.

Source checked 2026-09-18:
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

**SYNTHESIS:** reconciliation provenance should not be dumped indiscriminately into generic telemetry/security logs. The business provenance store, security log and analytics stream have different purposes, access controls and retention needs.

Guards:
- `logged ≠ audited`;
- `audit trail ≠ security log ≠ analytics event stream`;
- `more detail ≠ better assurance`;
- `centralized logs ≠ authoritative business provenance`.

## 6. Minimal provenance envelope

A generic reconciliation/correction envelope may need only the fields required to answer the consequence-relevant questions:
- stable record/entity identity;
- logical operation/correction identity;
- predecessor/base authoritative revision or branch identity;
- event class (`original`, `transform`, `reject`, `resolve`, `correct`, `invalidate`);
- actor class/identifier at the minimum necessary granularity;
- device/client/application/worker/API/policy generation where material;
- transformation/conflict-policy identifier and version;
- reason/reason-code where meaningful;
- server receipt/application time and ordering evidence where material;
- resulting authoritative revision;
- integrity/provenance reference to original payload or retained recovery object;
- retention/privacy classification.

Do not automatically duplicate the entire business record in every provenance entry. When content-level reconstruction is unnecessary, a digest/reference plus bounded retained source may be enough; when exact recovery is required, content retention must be justified separately.

## 7. Provenance graph, not mutable status fields

A single mutable record with fields such as `lastEditedBy`, `lastConflictReason`, `wasMigrated=true` loses earlier derivation information as subsequent changes occur. Prefer a bounded append-style lineage of material state transitions while allowing the current projection to remain efficient.

This does **not** require full event sourcing. The current authoritative record may remain the operational source of truth while a separate bounded provenance chain records only consequence-relevant transitions.

Guards:
- `append-style provenance ≠ event-sourced application`;
- `current projection stored ≠ lineage unnecessary`;
- `lineage retained ≠ replay log must rebuild entire application`.

## 8. Correction must create a new current assertion

Example:
- Offline iPad records `flightNumber=AB123` under revision R4.
- Migration changes only representation, not value.
- Server detects a conflict with R5 and asks for review.
- User determines `AB124` is correct.

The final authoritative R6 should be explainable as: original AB123 → representation transform → conflict against R5 → user correction AB124 → admitted R6. The system must not label AB124 as the user's original offline input.

Where the domain allows direct overwrite without historical retention, provenance can still retain a minimal correction fact rather than a complete old payload.

Guard: `user confirmed current result ≠ user authored every transformed intermediate`.

## 9. Automated conflict resolution needs policy provenance

If a conflict is auto-resolved, record enough to identify the policy/version and inputs relevant to the decision. If policy later changes, historical outcomes remain attributable to the policy actually used; they should not be silently reinterpreted as if the new policy made the old decision.

Guards:
- `automatic resolution deterministic ≠ resolution self-explanatory`;
- `policy updated ≠ historical decision re-adjudicated`;
- `historical policy identified ≠ historical policy still executable`.

## 10. Provenance compaction

Long-lived offline products can accumulate lineage. Compaction must preserve the claims that still matter.

Possible bounded strategies, selected per consequence:
- retain all material correction/conflict decisions but drop routine no-op sync events;
- retain hashes/references after full payload recovery horizon expires;
- checkpoint a verified lineage segment and retain its boundary identities/integrity evidence;
- aggregate operational metrics separately from record provenance;
- redact/pseudonymize actor/device identifiers when exact identity is no longer needed and policy permits;
- retain rejected original payload only through a defined recovery/dispute horizon, then preserve a non-content fact if justified.

Compaction must never create false continuity.

Guards:
- `compacted ≠ equivalent to original detail`;
- `hash retained ≠ content recoverable`;
- `summary retained ≠ every intermediate state reconstructable`;
- `retention expired ≠ invent missing provenance`.

## 11. Deletion, erasure and tombstones

Business deletion, synchronization tombstone, privacy erasure and provenance invalidation are different operations.

- A **domain delete** may need a tombstone long enough to prevent stale-client resurrection.
- A **privacy erasure** may require removal/anonymization of personal content subject to applicable obligations/exceptions.
- A **provenance fact** that a transition occurred may or may not need the deleted content itself.
- A **security/audit record** may have a different lawful/operational retention basis.

Do not keep a full deleted payload in an audit trail merely to make delete synchronization easy. Conversely, deleting a tombstone too early can allow a long-offline writer to resurrect state.

Guards:
- `business record deleted ≠ every provenance fact deleted`;
- `provenance fact retained ≠ deleted payload must be retained`;
- `tombstone retained ≠ full record retained`;
- `privacy erasure request ≠ synchronization safety may be ignored`.

Actual legal resolution is OPEN.

## 12. User-visible explanation boundary

Track B should not expose an internal event ledger verbatim. Users need a task-oriented explanation:
- what is current;
- what they originally entered where recoverable/appropriate;
- what changed automatically;
- what conflicted;
- what decision is required or was made;
- whether sync is complete;
- whether the old value remains recoverable/exportable;
- whether a correction affects only current state or also pending copies.

Avoid false certainty such as `Synced` when the operation was only uploaded, or `You changed X` when migration/default logic produced X.

Accessibility of comparison/correction flows, focus restoration after conflict resolution and Undo behavior remain runtime validation. Design Studio W084 is useful transfer evidence for semantic focus restoration but is not a PWA product PASS.

## 13. Offline/EFB-specific provenance boundary

For a long-offline company iPad:
- local original intent may exist before server receipt;
- local clock is contextual evidence, not authoritative global ordering;
- app/worker/schema/policy generation at creation may matter;
- reconnect can produce transform/reject/conflict/correction stages;
- server receipt does not retroactively make the local operation server-authoritative at creation time;
- a later native-mobile correction must not erase the fact that the EFB branch existed if that provenance remains within policy.

Local provenance stored only in browser storage inherits the same durability/eviction/backup uncertainty as other local data. It is not an independent audit archive until actual storage/recovery architecture proves that claim.

Guards:
- `local provenance present ≠ durable audit archive`;
- `server received operation ≠ server authored original intent`;
- `later correction wins ≠ offline branch never existed`.

## 14. Integrity and trust boundaries

Provenance entries themselves can be forged, replayed, truncated or reordered. Reuse 122–125 assurance rules:
- protect material provenance from unauthorized modification/deletion;
- distinguish producer authenticity from freshness/continuity;
- do not trust client-provided actor/time/policy claims without server-side validation where consequence requires it;
- retain enough ordering/receipt evidence to detect obvious truncation or replay where needed;
- do not turn every product edit into a heavyweight non-repudiation system unless consequence justifies it.

Guards:
- `provenance recorded ≠ provenance trustworthy`;
- `signed provenance ≠ provenance complete`;
- `client timestamp ≠ authoritative chronology`;
- `auditability required ≠ public transparency log/PKI required`.

## 15. Analytics boundary

Track D may measure counts/rates such as migration rejection, conflict incidence, correction completion and stale-client recovery, but analytics should use purpose-minimized event attributes. It should not receive complete flight/investment payloads merely to count reconciliation outcomes.

Absence of correction events cannot prove no conflicts occurred: offline clients, instrumentation failure, blocked analytics or abandonment can suppress telemetry.

Guards:
- `analytics event emitted ≠ provenance committed`;
- `no conflict telemetry ≠ no conflicts`;
- `analytics retention ≠ business-provenance retention`.

## 16. Track C validation campaign

1. original offline operation survives migration without in-place provenance rewrite;
2. deterministic transform records transformer/version;
3. transform changes semantics → review/reject rather than false equivalence;
4. user correction creates new event/revision;
5. UI does not label transformed value as original user input;
6. admin correction distinguishes actor/role from user correction;
7. auto-conflict resolution records policy version;
8. policy changes later → old resolution attribution remains stable;
9. duplicate retry does not create duplicate correction events;
10. ambiguous ACK preserves one logical correction identity;
11. concurrent corrections retain competing branch identities until adjudicated;
12. delete tombstone prevents stale resurrection without retaining unnecessary full payload;
13. rejected operation recovery object survives reload/restart through defined horizon;
14. recovery horizon expires → UI does not claim content remains recoverable;
15. provenance compaction preserves predecessor/result boundary identities;
16. compaction hash/reference cannot be mistaken for recoverable content;
17. retention deletion does not break current authoritative projection;
18. retention deletion does not falsely claim full historical reconstruction;
19. analytics pipeline receives minimized outcome data, not full payload by default;
20. security log does not duplicate secrets/session identifiers/business payload unnecessarily;
21. provenance-store access is authorization tested;
22. provenance tamper/delete attempt is detectable at the selected assurance level;
23. stopped provenance capture is detectable where continuity is required;
24. client clock rollback does not reorder authoritative server chronology blindly;
25. stale worker/client submits old provenance format → migration/rejection preserves original;
26. server-side actor/policy context overrides untrusted client claims where required;
27. correction after native-mobile/EFB branch conflict remains explainable after restart;
28. privacy erasure/retention workflow distinguishes payload, tombstone and minimal provenance fact;
29. focus after conflict/correction/Undo returns to a semantically valid owner rather than a vanished control;
30. physical Safari/iPadOS termination during provenance/correction publication → product validation required before PASS.

## 17. Cross-repository evidence

Design Studio `progress/WEB_STATUS.md` checked 2026-09-18: **W084 UNDO-RESTORATION FOCUS RUNTIME CLOSURE; Stage 3 PRACTICE / NOT PASSED**. W084 strengthens the distinction between restored configuration and current semantic focus owner. Persistence/offline/Sync, Safari/Firefox, screen reader, physical device, field-CWV and human UX remain OPEN.

Software Engineering Data `progress/DATA_STATUS.md` checked 2026-09-18: **Stage 1 IN STUDY / NOT YET PASSED**. D003 supplies migration-publication boundaries; D006 supplies operation identity, ACK ambiguity, deduplication and cursor/effect atomicity. Web Manager consumes these as bounded implementation evidence rather than claiming product/runtime PASS.

## 18. MINTTAP DIRECTION

For PWA/EFB-like products, keep current authoritative state efficient while preserving a bounded, purpose-specific provenance chain for material offline intent, migration, conflict and correction transitions. Separate business provenance from security logs and analytics. Retain full old payloads only when recovery/dispute/domain consequence justifies them; otherwise preserve smaller lineage facts/references after the relevant horizon.

Do not select event sourcing, W3C PROV serialization, cryptographic transparency logs, concrete retention periods or aviation-specific record rules until actual product data contracts, jurisdictions and consequence requirements are verified.

## 19. OPEN / VALIDATION / CHANGE WATCH

**OPEN:** actual record sensitivity; legal jurisdiction; aviation/investment retention duties; correction rights/process; exact operation/provenance schema; actor identity model; retention horizons; tombstone horizon; audit access; server/backend; managed-iPad durability; actual analytics/logging architecture.

**VALIDATION:** real correction/reconciliation flow; crash boundaries around current-record + provenance publication; retention/compaction; privacy deletion; Safari/iPadOS storage/restart; accessibility/focus; backend authorization; native↔PWA conflict provenance.

**CHANGE WATCH:** applicable privacy/aviation/investment rules; chosen browser/backend/storage behavior; product schema/API/conflict policy; logging/analytics providers and retention controls.

## 20. Persistent guards

`current value ≠ complete provenance`.  
`correction applied ≠ original intent rewritten`.  
`migration transformed value ≠ user corrected value`.  
`current authoritative ≠ historically original`.  
`auditability required ≠ retain every payload forever`.  
`data minimization ≠ no provenance`.  
`audit trail ≠ security log ≠ analytics event stream`.  
`append-style provenance ≠ event-sourced application`.  
`user confirmed current result ≠ user authored every transformed intermediate`.  
`policy updated ≠ historical decision re-adjudicated`.  
`compacted ≠ equivalent to original detail`.  
`hash retained ≠ content recoverable`.  
`business record deleted ≠ every provenance fact deleted`.  
`tombstone retained ≠ full record retained`.  
`local provenance present ≠ durable audit archive`.  
`provenance recorded ≠ provenance trustworthy`.  
`signed provenance ≠ provenance complete`.  
`analytics event emitted ≠ provenance committed`.  
`no conflict telemetry ≠ no conflicts`.

## 21. Gate assessment

**PASS (generic).** The Web Manager can now distinguish current state, original intent, automated transformation, conflict adjudication and correction; design a bounded provenance model without defaulting to event sourcing; reason about minimization/retention/tombstone/logging boundaries; and define validation oracles.

This does **not** certify actual MintTap/LogMate retention, privacy compliance, managed-iPad durability, backend atomicity, correction UX, accessibility or legal/safety requirements.

## 22. Next adjacent target

Highest-value continuation: **PWA provenance publication atomicity & partial-history recovery** — determine how current authoritative state and its provenance/receipt are published without split-brain histories when a crash occurs between business-state commit, provenance commit and acknowledgement; define repair/rebuild boundaries when the current projection survives but lineage is missing, or lineage survives while the projection did not commit.