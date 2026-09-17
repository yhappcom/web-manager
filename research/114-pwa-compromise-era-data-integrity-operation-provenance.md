# 114 — PWA Compromise-Era Data Integrity & Operation Provenance

Status: **PASS (generic) / PRODUCT RUNTIME + CRYPTOGRAPHIC + MANAGED-IPAD VALIDATION OPEN**  
Date: 2026-09-18  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 093 offline authorization/session boundaries; 098 stale-client containment; 099 trust authenticity/anti-rollback; 101 mixed-epoch recovery; 103 backup assurance; 113 hostile-origin compromise scoping; Track A IndexedDB/browser storage mechanics; Track C adversarial validation; Software Engineering Data/Quality/Systems for implementation evidence.

## Purpose

113 established that after arbitrary hostile same-origin code may have executed, preserving irreplaceable local records is necessary but does not prove their integrity. This study closes the adjacent generic question: **what evidence can distinguish user-authored domain records, local mutations, queued operations and remotely acknowledged effects after possible same-origin compromise, and how should recovery degrade when retrospective integrity proof never existed?**

This is generic security/operations judgment. Exact MintTap/LogMate record schema, event model, IndexedDB layout, server acknowledgement protocol, cryptographic keys, user/device identity, audit architecture and managed-iPad behavior remain OPEN.

## 1. Five-track balance

- **A Platform/Browser:** supplies the storage/transaction mechanics. IndexedDB transaction completion/durability is persistence evidence, not author/provenance evidence.
- **B UX/IA/Content:** consumes truthful integrity states and must distinguish preserved, verified, server-acknowledged, locally changed, conflicting and unverifiable records.
- **C Quality:** high-pressure consumer; owns tamper, interruption, replay, partial-acknowledgement and evidence-loss campaigns.
- **D Discovery/Analytics:** incident telemetry can corroborate server-observed events but is not a domain-record oracle; privacy minimization remains mandatory.
- **E Architecture/Security/Operations:** highest-risk owner; owns evidence hierarchy, authority/provenance boundaries, reconciliation and degraded recovery policy.

E remains the bottleneck; A and C are the strongest dependencies. Equal allocation is not justified.

## 2. SOURCE — local database commit proves storage transition, not trustworthy authorship

The W3C Indexed Database API defines read/write and version-change transactions and a durability hint. `strict` may cause the user agent to consider a transaction committed only after outstanding changes are written to persistent storage; `relaxed` can complete earlier. These semantics answer a durability question, not who caused the write or whether the value is semantically legitimate.

Source:
- https://www.w3.org/TR/IndexedDB/ (checked 2026-09-18)

**SYNTHESIS:** hostile same-origin JavaScript that legitimately holds application-origin access can use the same storage APIs as normal application code. A successful IndexedDB transaction cannot retrospectively distinguish a user action from hostile script mutation.

Guards:
- `transaction committed ≠ user authored`;
- `durably stored ≠ semantically trustworthy`;
- `schema valid ≠ provenance valid`;
- `record visible after restart ≠ record integrity proven`.

## 3. Evidence must be modeled by authority domain, not by one local history

Useful evidence classes are conceptually independent:
1. **current local value** — what the database contains now;
2. **local mutation history** — prior revisions/events if the product actually records them;
3. **user-intent evidence** — evidence tied to an explicit user action, if independently protected;
4. **device/application provenance** — which authorized device/app/trust generation originated an operation;
5. **remote receipt/acknowledgement** — what a remote authority actually accepted and identified;
6. **independent audit evidence** — records stored outside the compromised client authority;
7. **backup/export snapshots** — prior recoverable state with known capture identity/time/generation;
8. **domain reconciliation evidence** — invariants, duplicate/conflict rules and reviewed semantic outcomes.

A single compromised origin-controlled store cannot become independent evidence merely by storing both the record and its audit log in adjacent object stores.

Guards:
- `record + local audit entry ≠ two independent witnesses`;
- `append-only by application convention ≠ tamper-evident against arbitrary same-origin code`;
- `client timestamp ≠ trusted chronology`;
- `device identifier ≠ proof the legitimate application produced the operation`.

## 4. SOURCE — audit evidence gains value when protected outside the compromised system

NIST SP 800-171 Rev.3 requires audit records to capture event type, time, location/source, outcome and associated identities; it requires audit information/tools to be protected from unauthorized access, modification and deletion, and calls for correlation across repositories. NIST SP 800-92 explains why retaining logs both locally and in a log-management infrastructure can preserve evidence when an attacker alters/destroys system-local logs. OWASP Top 10:2025 A09 similarly calls for audit trails with integrity controls and warns against local-only, tamperable logging.

Sources:
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html
- https://csrc.nist.gov/pubs/sp/800/92/final
- https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/

**TRANSFER VALIDATION:** these are general audit/security principles, not a requirement to upload sensitive flight-record content. For an offline-first PWA, independently protected remote acknowledgement/audit evidence can become a corroborating source once connectivity exists; while offline, no such remote witness should be invented.

Guards:
- `local log exists ≠ local log survived same-origin compromise`;
- `central log exists ≠ central log contains enough domain evidence`;
- `audit integrity protected ≠ underlying business action legitimate`;
- `remote telemetry exists ≠ upload full user record content`.

## 5. Remote acknowledgement must bind to an operation identity and semantics

A bare HTTP success code or `sync complete` flag is weak provenance. Stronger acknowledgement conceptually binds at least:
- stable operation identifier/idempotency identity;
- actor/device/trust generation where the product defines them;
- operation type and target identity;
- semantic payload identity or canonical digest where justified;
- server decision/outcome and server-side sequence/version;
- acknowledgement identity/time under server authority.

RFC 9421 HTTP Message Signatures demonstrates an Internet-standard mechanism for authenticating selected HTTP message components and warns that unsigned components remain modifiable. RFC 9530 defines content/representation digests; RFC 9421 explicitly notes that signing a digest field is insufficient unless the receiver also validates that digest against the actual content.

Sources:
- https://www.rfc-editor.org/rfc/rfc9421.html
- https://www.rfc-editor.org/rfc/rfc9530.html

**TRANSFER VALIDATION:** this does **not** decide that MintTap/LogMate should implement HTTP Message Signatures. It establishes the durable principle that integrity evidence is only as strong as the exact semantics/components covered and verified.

Guards:
- `HTTP 2xx ≠ acknowledged domain state identified`;
- `signature valid ≠ unsigned semantics protected`;
- `digest signed ≠ content verified unless digest is recomputed`;
- `server acknowledged operation ≠ user intended operation if hostile client authority created it`.

## 6. Acknowledgement proves server observation, not necessarily legitimate user intent

If hostile same-origin code possessed valid session/device authority, the server may have correctly authenticated and accepted an attacker-generated operation. Cryptographic/server acknowledgement can prove **what the server accepted**, not necessarily **what the human intended**.

Therefore distinguish:
- **authentic transport/actor authority**;
- **operation integrity**;
- **user intent**;
- **domain validity**;
- **current authorization**.

These can diverge during compromise.

Guards:
- `authenticated request ≠ legitimate user intent`;
- `server accepted ≠ incident-safe`;
- `cryptographically authentic ≠ currently authorized after revocation`;
- `operation integrity ≠ operation correctness`.

## 7. Event sourcing / append-only history is useful only with an independent tamper boundary

An immutable-style event model can improve reconstruction, conflict analysis and auditability, but if hostile same-origin code can append arbitrary events, rewrite the event store, alter sequence metadata or control the signing key, the model does not by itself prove history.

Useful strengthening patterns may include product-specific combinations of:
- server-assigned monotonic versions/receipts;
- independently protected audit service;
- hash chaining or Merkle-style commitments anchored outside the client authority;
- hardware/platform-backed keys where platform policy and key usage are actually validated;
- signed exports/backup manifests under an authority not exposed to ordinary application script;
- human/domain reconciliation for residual ambiguity.

No one pattern is mandated generically.

Guards:
- `append-only data model ≠ append-only security boundary`;
- `hash chain stored beside mutable data ≠ independent tamper evidence`;
- `signature exists ≠ signing key isolated from hostile execution`;
- `hardware-backed key available ≠ web PWA can use it for the required unattended semantics`.

## 8. Trusted chronology cannot be reconstructed from client wall-clock alone

Offline devices can have inaccurate clocks; hostile code can also write arbitrary application timestamps. A chronology should therefore preserve multiple notions where available:
- user-entered domain time/date;
- local observed wall-clock time;
- local monotonic/session ordering where available;
- server receipt/sequence time;
- backup/export generation;
- trust/key/schema generation.

Do not rewrite user-entered flight dates merely because security chronology is uncertain.

Guards:
- `client timestamp ordered ≠ events occurred in that trusted order`;
- `server receipt time ≠ user action time`;
- `domain date ≠ security-event timestamp`.

## 9. Compromise-era reconciliation should classify, not silently overwrite

A generic post-incident reconciliation matrix can classify each record/operation as:
- **independently corroborated** — sufficient external/previously protected evidence supports the relevant state;
- **server-acknowledged pre-compromise** — remote state is known, subject to scope/timing confidence;
- **local-only, provenance bounded** — created in a period/generation with usable evidence but not remotely acknowledged;
- **potentially exposed/modified** — hostile execution could have affected it;
- **conflicting** — local and independently observed state disagree;
- **unverifiable** — preserved bytes exist but no independent historical integrity evidence can settle authorship/mutation;
- **invalid/rejected** — current domain/security policy establishes it must not be replayed.

`unverifiable` is a legitimate end state. It must not be silently converted to `clean` merely to finish recovery.

## 10. Safe degraded recovery when retrospective proof never existed

When a product did not previously create independent integrity/provenance evidence, incident response cannot manufacture it afterward. The safe generic direction is:
1. preserve the original artifact/state and its uncertainty;
2. freeze automatic remote replay for ambiguous operations;
3. restore trusted executable/authority planes under 113;
4. compare against any independent server acknowledgement, backups and domain invariants that do exist;
5. separate confirmed remote state from local-only state;
6. allow review/export/manual reconciliation rather than destructive normalization where domain risk permits;
7. mark provenance confidence explicitly in recovery evidence;
8. resume automatic replay only for operations that satisfy current authorization/reconciliation policy.

Guards:
- `no integrity evidence ≠ data known corrupted`;
- `no integrity evidence ≠ data known clean`;
- `recovery completed ≠ every historical record provenance resolved`;
- `manual review available ≠ manual review can cryptographically prove history`.

## 11. Privacy boundary — forensic usefulness does not justify recording everything

OWASP logging guidance warns against recording passwords, session identifiers and other sensitive information. Audit design should therefore capture the minimum metadata needed for correlation/integrity/reconciliation rather than copying full sensitive domain payloads into multiple security systems.

Source:
- https://top10proactive.owasp.org/the-top-10/c9-security-logging-and-monitoring/

MINTTAP/LogMate-like direction:
- prefer stable pseudonymous identifiers, operation/version identifiers, outcome, trust/schema generation and narrowly scoped digests where they actually serve an integrity purpose;
- do not put tokens, secrets, full flight-record content or unrestricted attachment contents into general telemetry merely for future incident convenience;
- retention/access policy remains product/legal/privacy specific and OPEN.

Guard: `more forensic data ≠ better privacy/security system`.

## 12. Track B truthful integrity/recovery UX

Candidate semantic states include:
- verified against protected history;
- confirmed on server;
- saved locally, not yet confirmed;
- preserved but integrity cannot be verified;
- changed during an uncertain period;
- conflict requires review;
- excluded from automatic sync;
- manually reconciled;
- replay authorized.

Avoid labels such as `safe`, `corrupt` or `restored` when the evidence only establishes a narrower fact.

## 13. Track C validation campaign

Exact product validation should include at least:
1. hostile script changes a record without touching local history;
2. hostile script changes record and local history together;
3. hostile script appends a syntactically valid fake event;
4. local transaction commits under strict/relaxed/default durability;
5. operation queued offline before compromise and acknowledged after;
6. attacker-generated operation receives valid server acknowledgement;
7. legitimate operation has no acknowledgement because network fails;
8. duplicate replay with stable operation ID;
9. conflicting local/server versions;
10. partial batch acknowledgement;
11. acknowledgement received but local ack write interrupted;
12. local ack claims success but server has no matching receipt;
13. stale session/device authority sends after revocation;
14. server receipt predates/overlaps hostile-origin window;
15. client clock deliberately skewed;
16. user-entered domain date differs from security-event time;
17. local hash chain rewritten with mutable records;
18. externally anchored audit evidence detects divergence;
19. backup predates compromise but misses later legitimate local records;
20. recovery preserves unverifiable records without auto-replay;
21. manual reconciliation does not mutate original evidence before capture;
22. telemetry contains no tokens/secrets/full record payloads;
23. browser restart/storage pressure during evidence preservation;
24. Chromium vs independent engine comparison;
25. Safari/WebKit Home Screen on target managed iPad;
26. accessible presentation of verified/unverified/conflict states;
27. malicious data cannot inject/forge security log presentation;
28. audit/log service unavailable while client remains offline;
29. server acknowledgement/signature verification fails closed without deleting local record;
30. new trust generation cannot retroactively relabel old unverifiable events as verified.

No runtime PASS is inferred from standards.

## 14. Cross-repository transfer

### Design Studio
Canonical `progress/WEB_STATUS.md` checked 2026-09-18: Web Design remains **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**. W066 is the first executed MintTap widget-runtime evidence and exposes real overflow/Material-layer failures; no widget runtime PASS, browser/Safari/screen-reader/physical-device PASS exists. Integrity/reconciliation states therefore remain requirements, not validated product UX.

### Software Engineering Studio
Canonical `progress/STATUS.md` checked 2026-09-18: every specialist remains **Foundation IN STUDY**. Systems S004 supplies dependency/build identity evidence only. Exact event model, persistence schema, cryptographic key isolation, operation IDs, acknowledgement protocol, audit service, replay/idempotency and mobile/browser implementation remain engineering handoffs.

## 15. MINTTAP / LogMate-like operational judgment

For an offline-first EFB-like PWA, the highest-value rule is **preserve uncertain records while preventing uncertain authority from creating irreversible remote effects**.

A future architecture should make it possible, where justified by product risk, to distinguish:
- local durable save;
- operation creation;
- operation queued;
- operation transmitted;
- server received/accepted/rejected;
- server state/version acknowledged;
- reconciliation completed;
- replay currently authorized.

These are separate facts. A single `synced=true` flag is inadequate incident evidence for high-value offline-authoritative data.

Exact need for cryptographic record/operation evidence depends on actual threat/risk and must not be imposed before product requirements and engineering feasibility are known.

## 16. Durable synthesis

After possible hostile same-origin execution, the right question is not `does the record still exist?` but:

**which authority observed or committed each state transition, which evidence remained outside the compromised authority, what did the server actually acknowledge, and which uncertainty must remain explicit before remote replay resumes?**

Persistent guards:
- `transaction committed ≠ user authored`;
- `durably stored ≠ semantically trustworthy`;
- `record + local audit entry ≠ two independent witnesses`;
- `append-only data model ≠ append-only security boundary`;
- `client timestamp ≠ trusted chronology`;
- `HTTP 2xx ≠ acknowledged domain state identified`;
- `server acknowledged operation ≠ user intended operation`;
- `authenticated request ≠ legitimate user intent`;
- `signature valid ≠ unsigned semantics protected`;
- `no integrity evidence ≠ data known corrupted ≠ data known clean`;
- `unverifiable` is a valid recovery state;
- `more forensic data ≠ better privacy/security system`;
- `synced=true ≠ provenance/reconciliation evidence`.

## 17. OPEN / next boundary

Product/runtime OPEN:
- actual authoritative record classes and risk;
- exact local history/event model and whether one exists;
- operation IDs/idempotency/replay protocol;
- server acknowledgement/version semantics;
- independent audit/log infrastructure;
- cryptographic keys and isolation from ordinary same-origin script;
- backup/export provenance;
- trusted-time/sequence sources;
- accessible reconciliation UX;
- target Safari/WebKit/managed-iPad behavior.

Highest-value adjacent generic boundary: **evidence-preserving incident acquisition and chain-of-custody for an offline PWA client**. Once a client may contain both irreplaceable records and compromise evidence, recovery actions themselves can overwrite caches, worker state, timestamps, outbox metadata or local history. The next study should determine how to preserve diagnostically useful state without turning Web Manager into a forensic-tool discipline, while prioritizing user-data survival and privacy and explicitly distinguishing operational recovery evidence from formal legal-forensic chain of custody.