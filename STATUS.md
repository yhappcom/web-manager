# MintTap Web Manager Status

Operating state: **ACTIVE — CONTINUOUS EXPERT MAINTENANCE / APPLICATION + FIVE-TRACK COORDINATION + PWA SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. The sequential `LEARNING_ROADMAP.md` curriculum is complete through Stage 12. `SPECIALIST_TRACKS.md` remains the horizontal five-track model. Future work is not a synthetic Stage 13: use live project evidence, change-watch, incidents, specialist dependencies and identified evidence gaps to select targeted expert study/application.

# Curriculum state
Stages 1–12: **COMPLETE at their defined curriculum gates.** Curriculum completion is not production certification.

Stage 12 Advanced / Expert Web Management: **081–082 PASS / CLOSED.**

# Continuous expert maintenance checkpoints
083 — **PWA Storage Durability & Service-Worker Standards Change Watch — PASS (2026-09-16).**  
084 — **iOS/iPadOS PWA Install, Background & Authentication Reality — PASS (2026-09-16).**  
085 — **PWA Irreplaceable Data Recovery, Offline Authorization & Device-Loss Security — PASS (2026-09-16).**

Material 085 findings:
- offline identity evidence, server-session validity, local unlock, offline authorization and queued-mutation acceptance are separate states;
- WebAuthn Level 3 became a W3C Recommendation on 2026-08-25 and supplies strong scoped public-key authentication, but does not itself define offline authorization or local-database encryption;
- same-origin browser storage and HTTPS do not provide a complete device-loss/XSS/data-at-rest security guarantee;
- Web Crypto supplies low-level cryptographic primitives, not a complete client-side encryption/key-recovery architecture;
- `saved locally ≠ persistent ≠ synchronized ≠ backed up ≠ restorable ≠ authorized offline ≠ safe after device loss`;
- remote sync/replication is a backup only if retention, corruption/deletion coupling, historical recovery and tested restore satisfy an explicit Recovery Contract;
- export is incomplete until destination commit, integrity/version, retention, import/migration, reconciliation and user-task restore are proven;
- remote revocation cannot instantly control a disconnected client; the residual offline authorization window must be explicit;
- destructive logout can conflict with availability when unsynchronized irreplaceable records exist;
- user-facing `Saved`, `Waiting to sync`, `Synced`, `Conflict`, `Backup current`, and `Backup overdue/not verified` are distinct safety-relevant states;
- long-offline restore must preserve the original copy, validate/migrate schema/protocol, replay idempotently and reconcile before old data is retired.

084 retained findings:
- iOS/iPadOS 26 Home Screen web-app behavior no longer uses manifest/Service Worker as developer-side installability gates;
- Web Push/Badging are specific event-driven background capabilities, not arbitrary background synchronization;
- Background Sync/Periodic Background Sync must not be EFB correctness dependencies;
- iOS/iPadOS 17.2 Home Screen creation copies current cookies but not other local storage and does not establish ongoing Safari↔web-app state sharing.

083 retained durability findings:
- persistence request/state/quota diagnostics do not create backup;
- modern WebKit storage policy supersedes historical fixed-quota folklore;
- eviction remains possible; irreplaceable local records require independent recovery and tested restore.

# Expert operating model
`portfolio intent → product/task ownership → canonical truth → constraints/guardrails → specialist evidence → decision rights/escalation → release/operation → observed outcome → incident/feedback → learning → debt/change-watch → review/supersession`.

# PWA strategic specialization
073–074 establish PWA foundations/data-sync boundaries; 075–085 transfer measurement, portfolio, release, operations, expert governance, durability, current iOS/iPadOS capability, and recovery/offline-auth security evidence.

Persistent guards:
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore ≠ analytics arrival`.
`Home Screen installed ≠ background synchronization available`.
`push event execution ≠ arbitrary background execution`.
`previously authenticated ≠ currently server-authorized ≠ authorized indefinitely offline`.
`HTTPS + same-origin storage ≠ device-loss/XSS/data-at-rest security guarantee`.
`Web Crypto available ≠ safe key-management/recovery architecture established`.
`origin deployment complete ≠ all installed clients updated`.
`origin rollback complete ≠ installed client recovered`.

For LogMate/EFB, correctness baseline is now: transactional local save + durable outbox + explicit durability states + independent recovery path + tested clean restore + bounded offline authorization + idempotent reconnect/reconciliation. Direct unattended PWA↔native transport remains separate and OPEN.

# Five-track state
All tracks have integrated foundation/practitioner coverage. Current maintenance allocation remains risk/evidence-gap driven.

- **A Platform/Browser:** strong current PWA mechanics/change-watch; supplies origin/storage/WebAuthn/Web Crypto semantics.
- **B UX/IA/Content:** materially deepened by 085; owns explicit durability/auth/recovery state language and journeys.
- **C Performance/Accessibility/Quality:** production browser/device evidence remains OPEN; recovery and destructive-action states require keyboard/AT/physical-device validation.
- **D Search/Discovery/Analytics:** strong; privacy-minimized sync/backup observability must not replicate sensitive logbook content or be mistaken for durability proof.
- **E Architecture/Security/Operations:** remains highest-consequence PWA owner; 085 strengthens threat, offline-auth, device-loss, backup/restore and revocation boundaries. Implementation proof remains a Software Engineering dependency.

# Cross-repository evidence
Design Studio Web Design latest checked 2026-09-16: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W036 shared action-oracle provenance is ready but multi-engine execution remains OPEN. No Safari, cross-browser, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering owns actual encryption/key handling, schema/protocol migrations, outbox/reconciliation, backup/import implementation, automated tests and target-device runtime evidence. Web Manager owns requirements, threat/recovery contracts and acceptance boundaries.

Design Studio owns reusable visual/interaction expertise. Marketing owns channel/acquisition/community strategy. Software Engineering owns implementation/code/runtime/device validation.

# Production OPEN register
Actual `minttap.app` production state remains OPEN unless verified from project evidence.

PWA/EFB OPEN includes target managed-iPad OS/WebKit/MDM policy, Shared iPad status, Home Screen permission/retention, persistence behavior, LogMate identity/authentication model, offline authorization lifetime, logout/revocation semantics, encryption/key-management decision if any, schema/migrations/outbox, independent backup destination, managed-device export/share feasibility, clean restore, storage-pressure/long-inactivity behavior, reconnect retry behavior, and direct unattended PWA↔native transport.

# Next learning mode
Highest-value adjacent PWA target after 085: **direct PWA↔native transport feasibility and security boundary**, decomposed into discovery, local-network permission, signaling/addressing, TLS/secure context, WebRTC/WebSocket/WebTransport/Bluetooth capability boundaries, background/suspension behavior, pairing/authentication and managed-iPad policy. Do not select a transport from generic support tables; require current platform evidence and Software Engineering target-device handoff.

# Persistence state
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–085 PASS**.
- PWA production/device validation remains project-specific.
- Reporting remains coarse/checkpoint-based.
