# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and strategic web-app/PWA capability. Canonical curriculum: `../LEARNING_ROADMAP.md`; horizontal ownership: `../SPECIALIST_TRACKS.md`.

Evidence vocabulary: `SOURCE`, `SYNTHESIS`, `MINTTAP DECISION/DIRECTION`, `OPEN`, `DEPENDENCY`, `VALIDATION`, `CHANGE WATCH`, `TRANSFER VALIDATION`, `CONTRADICTION`.

## Sequential curriculum — COMPLETE
- Stage 1 Web Foundations: 027–033 — **PASS**
- Stage 2 Website Anatomy / Content / IA: 034–038 — **PASS**
- Stage 3 UX & Interaction: 039–044 — **PASS**
- Stage 4 Web Design Literacy: 045–050 — **PASS**
- Stage 5 Accessibility: 051–058 — **PASS**
- Stage 6 Search / Discovery / Content Quality: 059–065 — **PASS**
- Stage 7 Performance / Browser Runtime: 066–070 — **PASS**
- Stage 8 Security / Privacy / Trust: 071–072 — **PASS**
- Stage 9 Analytics / Experimentation: 075–076 — **PASS**
- Stage 10 App-Company Web Strategy & Growth: 077–078 — **PASS**
- Stage 11 Web Operations & Platform Architecture: 079–080 — **PASS**
- Stage 12 Advanced / Expert Web Management: 081–082 — **PASS / FINAL CURRICULUM GATE**

Curriculum passes are competency gates, not production certification.

## Strategic PWA foundation
073 — **PWA Cross-Track Foundations — PASS.**  
074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

## Continuous expert maintenance/application
083–090 cover storage durability/change watch; iOS/iPadOS capability; irreplaceable-data recovery/offline authorization; direct transport/WebRTC managed-network boundaries; offline navigation/update recovery; testing/diagnostics; release/support/incident evidence.  
091–098 cover long-offline compatibility/API retirement; release supply-chain; session/offline authorization; account/device/key recovery; XSS/unlocked-data authority; sensitive-context isolation; explicit trust bridges; stale-client revocation/data-preserving containment.  
099 — **PWA Trust-Policy Authenticity, Authority Recovery & Anti-Rollback Boundaries — PASS (generic).**  
100 — **PWA Trusted-State Persistence, Reset/Reinstall Bootstrap & Recovery — PASS (generic).**  
101 — **PWA Mixed-Epoch Recovery Provenance & Reconciliation — PASS (generic).** Restore is a vector of record/trust/key/schema/protocol/outbox/ack epochs; integrity, provenance, reader/domain acceptance, reconciliation and replay authorization remain separate gates.  
102 — **PWA Portable Recovery Artifact Confidentiality, Custody & Import Authority — PASS (generic).** Portable Files/cloud/share artifacts are a new trust boundary; encryption is separated from recoverability/key custody; import is hostile-input processing; bearer/session/device/trust restoration and metadata leakage are constrained.  
103 — **PWA Backup Freshness, Completeness, Recoverability Evidence & Privacy-Safe Assurance — PASS (generic) / PRODUCT RESTORE-DRILL + TARGET-DEVICE VALIDATION OPEN.** Backup assurance is capture frontier → completeness → serialization → custody → integrity/authenticity → key → reader/schema → semantic restore → reconciliation → restore rehearsal.  
104 — **PWA Offline-First Recovery Objectives, Exposure Budgets & Long-Offline Operations — PASS (generic) / PRODUCT THRESHOLDS + TARGET-DEVICE VALIDATION OPEN.** Recovery objectives are a vector covering local durable save, external-protection exposure, restore readiness, recovery duration, sync convergence, long-offline survivability and trust revalidation.  
105 — **PWA Recovery-Risk Release Governance, Rollout Gates & Forward-Only State — PASS (generic) / PRODUCT RELEASE POLICY + TARGET-RUNTIME VALIDATION OPEN.** Recovery-critical releases consume evidence/risk margin, not user records; rollout requires exact-artifact/migration/restore/mixed-generation/fault/breaker evidence; service-worker activation is a compatibility decision; code rollback does not imply schema/key/trust/remote-effect rollback and may require compatibility bridge + forward repair.  
106 — **PWA Release Compatibility Contracts, Retirement Proof & Data-Preserving Unsupported States — PASS (generic) / PRODUCT SUPPORT HORIZON + TARGET-RUNTIME VALIDATION OPEN.** Compatibility is a reader/writer/schema/protocol/API/trust/worker/backup vector; deprecation differs from sunset; retirement requires positive migration/recovery evidence; ordinary runtime support may end before a narrow current-authority recovery path; `unsupported` must not silently discard authoritative local data.

## High-value current guards
- `storage API available ≠ persistence granted ≠ backup ≠ tested restore`;
- `local save ≠ sync queued ≠ remote acknowledgement ≠ reconciliation ≠ backup`;
- `automated browser PASS ≠ Safari PASS ≠ physical iPad PASS ≠ managed-EFB product PASS`;
- `backup file exists ≠ backup current ≠ backup complete ≠ restore works`;
- `backup age ≠ data-loss exposure`; `sync backlog ≠ backup backlog`;
- `offline ≠ app unavailable`; `online ≠ sync authorized`;
- `healthy average ≠ vulnerable cohort healthy`; `no telemetry received ≠ objective met`;
- `restore completed ≠ records/trust/keys/outbox share one coherent recovery epoch`;
- `hash matches ≠ artifact provenance established ≠ application semantics accepted`;
- `outbox item present ≠ never applied remotely ≠ replay authorized`;
- `authority revoked remotely ≠ disconnected client informed ≠ local capability immediately unavailable`;
- `network restored ≠ trust restored ≠ replay authorized`;
- `HTTPS policy fetch succeeded ≠ policy authorized by an independent trust root`;
- `encrypted at rest ≠ protected from authorized same-origin script while unlocked`;
- `different path ≠ different origin security boundary`; `different origin ≠ no trust bridge`;
- `postMessage origin validated ≠ message authorized ≠ payload semantically valid ≠ transaction current`;
- `CORS allowed ≠ caller authenticated ≠ caller authorized ≠ mutation safe`;
- `origin deployment complete ≠ all installed clients updated`; `origin repaired ≠ installed fleet clean`;
- `user selected file ≠ trusted recovery artifact`;
- `backup encrypted ≠ backup recoverable ≠ key independently protected`;
- `build passed ≠ rollout safe`; `artifact published ≠ installed fleet converged`;
- `canary healthy ≠ long-offline cohort compatible`;
- `code version N ≠ cache/schema/trust/API generation N`;
- `code rollback ≠ schema rollback ≠ key/trust rollback ≠ remote side-effect rollback`;
- `connected fleet converged ≠ long-offline fleet recoverable`;
- `deprecated ≠ non-operational`; `deprecation header emitted ≠ migration completed`;
- `sunset announced ≠ every client received the announcement`;
- `app version supported ≠ every dependent generation compatible`;
- `zero observed old clients ≠ zero old clients`;
- `legacy write disabled ≠ legacy data unreadable`;
- `normal sync retired ≠ recovery import must be retired simultaneously`;
- `unsupported for sync ≠ unsupported for local read/export/recovery`;
- `legacy protocol vulnerable ≠ legacy records malicious`.

## Specialist relationships
A Platform/Browser owns reusable mechanics; B UX/IA/Content owns task/information/state structure; C Performance/Accessibility/Quality owns runtime/inclusive/regression evidence; D Search/Discovery/Analytics owns discoverability/measurement; E Architecture/Security/Operations owns trust/risk/operations. Web Manager coordinates portfolio decisions.

Design Studio remains canonical for reusable visual/interaction evidence. Marketing owns acquisition/channel/community strategy. Software Engineering owns implementation/code/runtime validation. Use explicit handoffs and evidence boundaries.

## Current evidence boundary
Generic PWA architecture through compatibility-contract/retirement-proof governance is sufficient for implementation handoff. Product feasibility/certification still requires exact-artifact evidence on target managed devices plus applicable security, privacy, accessibility and operational validation.

Current next generic boundary, only if implementation evidence remains unavailable: **compatibility-bridge minimization and attack-surface debt** — retaining old readers/migrators/recovery endpoints prevents data stranding but expands parser/protocol/security surface. Determine how to keep recovery compatibility narrow, isolated and testable; how to retire vulnerable legacy parsers without losing old artifacts; and how bridge debt enters security/change governance. Consume Software Engineering parser/data evidence rather than duplicate implementation theory.

## Study quality standard
Substantial work includes precise vocabulary, first-principles mechanics, authoritative evidence, counterexamples/failure analysis, cross-domain effects, bounded project relevance, durable-vs-changeable classification, validation requirements and explicit decision ownership.
