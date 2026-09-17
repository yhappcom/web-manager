# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-17  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. Sequential curriculum Stages 1–12 are complete. Future work is targeted expert maintenance/application selected from live evidence, change-watch, risk and specialist dependencies. Curriculum completion is not production certification. Detailed historical guards and study summaries live in `research/README.md` and the numbered research artifacts; this status intentionally stays checkpoint-oriented.

## Continuous expert maintenance
083–101 — **PASS at their recorded generic gates; product/device/runtime validation remains OPEN where stated in the research index.**  
102 PWA Portable Recovery Artifact Confidentiality, Custody & Import Authority — **PASS (generic) / PRODUCT BACKUP-CRYPTO + TARGET-DEVICE VALIDATION OPEN**.

## 102 material findings
- portable recovery crosses a new trust boundary: user-selected/imported bytes are not trusted merely because the user chose them;
- Web Share is user-mediated, secure-context-only and currently limited-availability; successful invocation does not establish destination confidentiality, retention or continued application custody;
- backup encryption, key protection and recoverability are independent properties; device-only keys can defeat portability while co-locating directly usable key material with ciphertext can defeat separation;
- `saved in Files/iCloud` is not a universal confidentiality claim: Apple distinguishes Standard vs Advanced Data Protection, some metadata remains separately protected, and managed-device policy can restrict iCloud services;
- portable artifacts must not silently restore session/device/pairing/trust authority merely because old data is valid;
- imported backups are hostile-input candidates until bounded parsing, integrity/provenance, key binding, schema/domain, trust/protocol and reconciliation gates pass;
- metadata outside the protected envelope can leak product/account/device/time/version information even when record payloads are encrypted;
- retention/version rotation is part of the recovery protocol: more copies are not monotonically safer when old records, keys, credentials, tombstones or vulnerable formats persist.

## Persistent guards added by 102
`user selected file ≠ trusted recovery artifact`.  
`share sheet completed ≠ destination confidential ≠ backup still under application custody`.  
`backup encrypted ≠ backup recoverable ≠ key independently protected`.  
`ciphertext + directly usable key in same artifact ≠ meaningful key/data separation`.  
`device-bound key ≠ portable recovery capability`.  
`portable recovery key ≠ acceptable bearer-secret exposure`.  
`saved to cloud ≠ end-to-end encrypted under every account configuration`.  
`file contents encrypted ≠ filename/size/timestamps/manifest metadata confidential`.  
`Files destination available on consumer iPad ≠ permitted on managed EFB`.  
`recognized extension ≠ recognized content ≠ valid manifest ≠ authorized recovery`.  
`decrypt succeeded ≠ semantic validation succeeded`.  
`backup proves possession of old data ≠ current account authentication`.  
`backup import accepted ≠ old session/device credential should be reactivated`.  
`payload encrypted ≠ backup privacy complete`.  
`more backup copies ≠ monotonically safer recovery`.

## Five-track state
All tracks retain integrated foundation/practitioner coverage; allocation is risk/evidence-gap driven.
- **A Platform/Browser:** strong dependency supplier. Exact managed-iPad File selection/share/cloud/storage behavior remains target-device evidence.
- **B UX/IA/Content:** consumes distinct states: backup created, saved, encrypted, recoverable, imported, verified, decrypted, compatible, locally recovered and sync-ready must not collapse into one success label.
- **C Performance/Accessibility/Quality:** owns corrupt/hostile/large file, wrong-key, interruption, cross-version, accessibility and physical-device validation matrices.
- **D Search/Discovery/Analytics:** backup filenames, manifest IDs, recovery secrets and imported user metadata are not analytics/discovery payloads by default.
- **E Architecture/Security/Operations:** current highest-risk owner; 102 closes the generic portable-artifact confidentiality/custody/import-authority prerequisite for implementation handoff.

## Cross-repository evidence
Design Studio checked 2026-09-17: Web Design is **Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED**; W053 graph-integrity closure target is ready but execution remains OPEN. No cross-browser, Safari, screen-reader, physical-device or human UX PASS is inferred.

Software Engineering Studio checked 2026-09-17: all specialists remain **Foundation IN STUDY**. D003/D005/D006 remain the relevant implementation-method evidence for reader compatibility, validate-before-publish and replay/reconciliation. Q005 adds a reusable symptom→isolation→causal-test debugging method, but does not constitute PWA backup/runtime evidence.

## Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes exact managed-iPad OS/WebKit/MDM policy; Home Screen storage/reset behavior; Files/iCloud/share availability; worker/cache/update behavior; schema/protocol/API compatibility; accessible degraded/recovery UX; network restrictions; pairing/sync transport; backup/export/import/restore; diagnostics and fleet update policy.

Auth/security/recovery OPEN includes actual authentication/session/token/cookie architecture; offline authorization; passkey/local-unlock design; authoritative local data classes; encryption-at-rest threat model; DEK/KEK/recovery hierarchy; backup format/component inclusion; key recoverability; device replacement/revocation; trust-state store; anti-rollback/rebootstrap; mixed-epoch reconciliation; hostile import limits; retention/version rotation and metadata confidentiality.

Runtime/control-plane/supply-chain OPEN includes actual origin/script/CSP/Trusted Types topology; third parties; bridge/network policy; worker scope; signing/bootstrap trust; trusted-time/rotation/recovery authority; CI/dependency/provenance/deployment identity; DNS/provider recovery and credential/key rotation drills.

## Next learning mode
102 closes the generic portable-artifact confidentiality/custody/import-authority prerequisite. Avoid inventing a product backup format or cryptographic hierarchy without implementation/security evidence. Highest-value next generic work, if exact implementation evidence is still absent, is **backup freshness, completeness and recoverability evidence**: prove that backup captured the latest authoritative local records/outbox, reached durable external custody, remains decryptable/readable across supported versions and has been restore-tested without turning recovery telemetry into a privacy leak. Consume Software Engineering recovery/fault-injection evidence when it becomes available.

## Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–102 PASS** at generic gates.
- Product/device/AT/security/privacy validation remains OPEN.
- Reporting remains coarse/checkpoint-based.
