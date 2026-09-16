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

Material 084 findings:
- iOS/iPadOS 26 changes Home Screen behavior materially: every site added to Home Screen opens as a web app by default unless the user disables `Open as Web App`; WebKit states there are zero developer-side installability requirements in Safari;
- manifest presence and Service Worker presence are therefore no longer iOS/iPadOS 26 installability gates, although both remain useful for controlled metadata/offline behavior;
- Home Screen creation remains a user/device action and generic platform support does not establish managed-EFB MDM permission or retention;
- Web Push/Badging establish specific event-driven background capability for Home Screen web apps, not arbitrary continuous/background synchronization;
- Background Sync and Periodic Background Sync remain non-Baseline/limited cross-browser capabilities and must not be correctness dependencies for a managed-iPad EFB workflow;
- Service Workers are event-driven/disposable; durable sync state belongs in persistent application/protocol state, not worker globals;
- since iOS/iPadOS 17.2, creating a Home Screen web app copies current cookies, including cookie-based login state, but does not copy other local storage and does not create ongoing shared browser↔web-app state;
- offline identity/local access/server-session validity/server authorization/queued-mutation acceptance are separate states and require an explicit product security contract;
- `installable ≠ offline-capable ≠ background-capable ≠ synchronized ≠ backed up`.

083 retained durability findings:
- `StorageManager.persist()` is a browser-controlled persistence request; persistence state/quota diagnostics do not create backup;
- modern WebKit storage policy supersedes historical fixed-quota folklore and uses disk-relative quota/eviction policy;
- eviction remains possible; irreplaceable local records require independent recovery and tested restore;
- exact managed-iPad artifact/device tests remain required for persistence, long-offline survival, schema migration, worker/cache update, storage pressure and recovery claims.

# Expert operating model
`portfolio intent → product/task ownership → canonical truth → constraints/guardrails → specialist evidence → decision rights/escalation → release/operation → observed outcome → incident/feedback → learning → debt/change-watch → review/supersession`.

Retained expert judgments:
- fact/observation/inference/forecast/preference/decision remain distinct evidence classes;
- consequential decisions require owner, alternatives, uncertainty, residual-risk ownership, validation and supersession triggers;
- specialist evidence ownership does not automatically confer authority to accept cross-product/security/privacy/legal risk;
- decision speed scales with downside, uncertainty and reversibility;
- localization is semantic/product/release/locale/region/support lineage, not translation completion;
- accessibility/privacy/security/performance/reliability act as guardrails around optimization;
- incidents require systemic learning;
- competitor implementation is precedent, not proof of outcome or fit;
- current platform behavior must not be fossilized into permanent company doctrine;
- migration/replatforming requires requirement/risk/TCO justification and continuity/recovery planning.

# PWA strategic specialization
073–074 establish PWA foundations/data-sync boundaries; 075–084 transfer measurement, portfolio, release, operations, expert governance, durability and current iOS/iPadOS capability evidence.

Persistent guards:
`public website ≠ installable web experience ≠ offline-capable task ≠ synchronized product`.
`local save ≠ persistent storage ≠ sync queued ≠ transport attempt ≠ remote acknowledgement ≠ reconciliation ≠ backup ≠ tested restore ≠ analytics arrival`.
`Home Screen installed ≠ background synchronization available`.
`push event execution ≠ arbitrary background execution`.
`browser login state ≠ Home Screen application state except bounded installation-time cookie transfer documented by WebKit`.
`origin deployment complete ≠ all installed clients updated`.
`origin rollback complete ≠ installed client recovered`.
`same source ref ≠ same accepted PWA artifact when build/post-build/origin differs`.

For LogMate/EFB, correctness must not depend on Background Sync. The robust baseline remains durable outbox + foreground/resume/reconnect/manual/next-launch retry + idempotent remote apply + acknowledgement + reconciliation. Optional background opportunities may improve latency only after target-platform validation.

# Five-track state
All five tracks have integrated foundation/practitioner coverage. Maintenance allocation remains risk/evidence-gap driven. 083–084 are primarily A+E because current PWA browser/platform truth and data/session durability are high-consequence dependencies for B/C/D and the EFB scenario.

- **A Platform/Browser:** owns current WebKit/iOS/iPadOS installability, worker lifecycle, Push/Badging, storage and browser-state semantics; current change-watch materially strengthened by 083–084.
- **B UX/IA/Content:** consumes explicit install/offline/auth/sync/recovery states; avoid ambiguous `Saved`/`Synced` claims.
- **C Performance/Accessibility/Quality:** production browser/device evidence remains open; target tests must include terminate/offline relaunch, long-offline resume, update with pending data and accessible recovery states.
- **D Search/Discovery/Analytics:** install opportunity/installed launch/push permission/sync completion are separate observables; analytics cannot prove durability or installation population.
- **E Architecture/Security/Operations:** co-owns auth/offline authorization, outbox/reconciliation, recovery, worker deployment and managed-device policy boundaries.

# Cross-repository evidence
Design Studio Web Design latest checked 2026-09-16: Stage 1/2 PASS, Stage 3 PRACTICE / NOT PASSED; W033 product-like resumption target is ready but browser execution remains open. No browser-runtime, cross-browser, Safari, screen-reader, physical-device, field-CWV or human-UX PASS may be inferred.

Software Engineering latest checked 2026-09-16: Foundation remains in study; A003 now has executable evidence that same source/call shape can still break semantic contracts. Web Manager transfers this to skipped-version PWA schema/protocol reasoning, but implementation/device validation remains Software Engineering ownership.

Design Studio owns reusable visual/interaction expertise. Marketing owns channel/acquisition/community strategy. Software Engineering owns implementation/code/runtime/device validation. Web Manager owns web portfolio truth, cross-surface requirements, evidence integration, operational acceptance and expert decision governance.

# Production OPEN register
Actual `minttap.app` IA/runtime/framework/provider/DNS/CDN/environments/CI-CD/security/privacy/accessibility/analytics/PWA state remains OPEN unless verified from project evidence. Actual app/store/support/localization/release states likewise require current evidence.

PWA/EFB OPEN includes target managed-iPad OS/WebKit/MDM policy, Shared iPad status, Home Screen permission/retention, actual persistence behavior, LogMate authentication/offline-authorization contract, schema/migrations/outbox, backup/restore destination and UX, storage-pressure/long-inactivity behavior, exact reconnect/resume retry behavior, and direct unattended PWA↔native transport.

# Next learning mode
Continue balanced change-watch + evidence-gap work. Highest-value adjacent PWA target after 084: **backup/export/recovery UX + privacy/security and device-loss handling**, integrated with offline authentication, user-visible durability states, long-offline/skipped-version recovery and target-device validation contracts. Then revisit direct PWA↔native transport only with authoritative platform evidence and Software Engineering handoff rather than speculation.

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model.
- `LEARNING_ROADMAP.md`: sequential curriculum complete through Stage 12.
- `research/README.md`: research and maintenance index.
- Stages 1–12: COMPLETE at defined curriculum gates.
- Continuous maintenance: **083–084 PASS**.
- Production/device validation remains project-specific.
- Reporting remains coarse/checkpoint-based.
