# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-17  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification. Detailed historical guards and study summaries live in `research/README.md` and numbered research artifacts; this status intentionally stays checkpoint-oriented.

## Continuous expert maintenance
083–102 — **PASS at their recorded generic gates; product/device/runtime validation remains OPEN where stated in the research index.**  
103 PWA Backup Freshness, Completeness, Recoverability Evidence & Privacy-Safe Assurance — **PASS (generic) / PRODUCT RESTORE-DRILL + TARGET-DEVICE VALIDATION OPEN**.

## 103 material findings
- backup assurance is a chain, not a boolean: capture frontier, completeness, serialization, custody, integrity/authenticity, key availability, reader/schema support, semantic restore, reconciliation and restore rehearsal are distinct;
- NIST SP 1339 and SP 800-53 CP-9 distinguish regular backup/testing from actual restoration assurance; CISA likewise recommends regular availability/integrity testing in disaster-recovery scenarios;
- freshness must be measured against the latest committed authoritative local frontier, not wall-clock/file age alone; remote sync freshness is not local-backup freshness;
- completeness requires explicit required-component/dependency closure and mixed-epoch acceptance, not merely a matching file/record count;
- generic Files/share handoff may not let a PWA prove continued durable external custody after control leaves the application;
- restore drills provide stronger evidence than backup creation and should exercise key acquisition, current supported reader, domain validation, expected recovery frontier, outbox/ack ambiguity and reconciliation;
- previous restore evidence has a bounded applicability envelope and must be reconsidered after format/schema/key/storage/reconciliation/platform changes;
- recovery observability must exclude records, keys, tokens, filenames and unnecessary stable identifiers; client success events are evidence inputs, not independent durable-custody proof.

## Persistent guards added by 103
`backup file exists ≠ backup current ≠ backup complete ≠ restore works`.  
`backup integrity verified ≠ semantic recovery verified`.  
`decrypt/read succeeded ≠ supported application state restored`.  
`backup job reported success ≠ recovery objective proven`.  
`one green backup indicator ≠ end-to-end recoverability evidence`.  
`recent timestamp ≠ latest authoritative state captured`.  
`last sync current ≠ local backup current`.  
`remote state current ≠ unsynced local state protected`.  
`latest record present ≠ recovery set complete`.  
`all files copied ≠ dependency closure proven`.  
`export/share completion ≠ externally durable custody verified`.  
`restore UI reached ≠ restore drill passed`.  
`restore drill passed once ≠ all future builds/artifacts recoverable`.  
`more recovery telemetry ≠ more trustworthy recovery`.  
`client reports backup success ≠ independently trustworthy durable-custody proof`.

## Five-track state
All tracks retain integrated foundation/practitioner coverage; allocation remains risk/evidence-gap driven.
- **A Platform/Browser:** strong dependency supplier. Exact managed-iPad file/share/storage/background behavior remains target-device evidence.
- **B UX/IA/Content:** consumes truthful states for not-yet-protected, preparing, locally-created, externally-handed-off, verified, stale, compatibility-unknown and restore-tested conditions.
- **C Performance/Accessibility/Quality:** now has a concrete 20-case future restore/failure matrix spanning interruption, corruption, wrong key, cross-version, mixed ack/replay, reset, managed-iPad restriction, accessibility and telemetry leakage.
- **D Search/Discovery/Analytics:** recovery telemetry is operational assurance data, not acquisition analytics; raw backup/user/secret metadata remains excluded by default.
- **E Architecture/Security/Operations:** current highest-risk owner; 103 closes the generic backup freshness/completeness/recoverability-evidence prerequisite.

## Cross-repository evidence
Design Studio checked 2026-09-17: canonical Web Design status is **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**; W053 execution remains OPEN and W054 defines a product evidence package but is not runtime evidence. No cross-browser, Safari, screen-reader, physical-device, field-CWV or human UX PASS is inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain **Foundation IN STUDY**. D003/D005/D006 remain relevant to reader compatibility, validate-before-publish and replay/reconciliation; Q003/Q005 provide interleaving and causal-diagnosis methods; F006 now supplies executable stream-framing/ack-boundary evidence but not PWA/mobile runtime proof.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy; Home Screen storage/reset behavior; Files/iCloud/share availability; background execution; worker/cache/update behavior; schema/protocol/API compatibility; accessible degraded/recovery UX; network restrictions; pairing/sync transport; backup/export/import/restore; diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture; offline authorization; passkey/local-unlock design; authoritative local data classes; encryption-at-rest threat model; DEK/KEK/recovery hierarchy; backup format/component inclusion; capture frontier/checkpoint; key recoverability; device replacement/revocation; trust-state store; anti-rollback/rebootstrap; mixed-epoch reconciliation; hostile import limits; retention/version rotation; metadata confidentiality; restore-test support envelope and telemetry privacy review.

Runtime/control-plane/supply-chain OPEN includes actual origin/script/CSP/Trusted Types topology; third parties; bridge/network policy; worker scope; signing/bootstrap trust; trusted-time/rotation/recovery authority; CI/dependency/provenance/deployment identity; DNS/provider recovery and credential/key rotation drills.

## Next learning mode
103 closes the generic backup assurance prerequisite. Avoid inventing product RPO/RTO/SLO numbers or claiming automatic backup from API availability. Highest-value next generic work, if exact implementation evidence remains absent, is **offline-first recovery objectives and failure budgets**: adapt RPO-like local-data exposure, backup lag, restore-test recency, recovery time, sync backlog and long-offline operation to a device-authoritative PWA without blindly importing server-centric disaster-recovery metrics. Tie metrics to truthful user guarantees and operational alerts while leaving thresholds product-evidence-driven.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–103 PASS** at generic gates.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
