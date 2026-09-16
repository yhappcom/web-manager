# MintTap Web Manager Status

Operating state: **ACTIVE — FIVE-TRACK BALANCED DEEP LEARNING + PWA STRATEGIC SPECIALIZATION**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play, strategic PWA/Web App capability

## Operating model
GitHub is canonical memory. `LEARNING_ROADMAP.md` is the vertical beginner→expert curriculum; `SPECIALIST_TRACKS.md` is the horizontal five-track expertise model. Web Manager coordinates A Platform/Browser, B UX/IA/Content, C Performance/Accessibility/Quality, D Search/Discovery/Analytics and E Architecture/Security/Operations by evidence/risk/dependency value rather than equal volume.

PWA is a **strategic high-priority cross-track specialization**, not a sixth track.

# Curriculum state
Stages 1–8: **COMPLETE — FOUNDATION/PRACTITIONER GATES PASSED.** These are transferable competency gates, not production certification.

- Stage 1 Web Foundations: 027–033
- Stage 2 Website Anatomy / Content / IA: 034–038
- Stage 3 UX & Interaction: 039–044
- Stage 4 Web Design Literacy: 045–050
- Stage 5 Accessibility: 051–058
- Stage 6 Search / Discovery / Content Quality: 059–065
- Stage 7 Web Performance / Browser Runtime: 066–070
- Stage 8 Security / Privacy / Trust: 071–072

# PWA strategic specialization
073 — **PWA Cross-Track Foundations: Service Workers, Offline, Install, Storage, Updates & Platform Reality — PASS.**

074 — **PWA Data Durability & Synchronization Architecture Boundaries — PASS.**

Integrated PWA model now extends to:
`secure origin → service-worker/cache/app shell → IndexedDB structured local state → atomic local mutation/outbox → transport opportunity → authenticated idempotent remote apply → acknowledgement → pull/reconciliation → conflict/recovery → independent backup/restore → target-device validation`.

Retained judgments through 074:
- local save, queued sync, transmission, remote acknowledgement, replication and backup are distinct states;
- IndexedDB provides local transactions/schema versioning, not cross-device transactions or synchronization;
- schema upgrades can be blocked by old open connections and must be coordinated with page/service-worker version transitions;
- same-origin Web Locks can coordinate tabs/workers but cannot prevent cross-device/retry duplicates;
- durable offline sync requires stable record/change identity, outbox, retry, idempotency/deduplication, acknowledgement, remote-change discovery, deletion semantics and conflict policy;
- acknowledgement loss creates an ambiguous-delivery case, so transport reliability alone does not remove idempotency requirements;
- conflict resolution is domain semantics, not a transport feature; silent last-write-wins is not assumed for logbook-like records;
- browser persistent storage and synchronized replicas are not independent backups;
- Background Sync and Periodic Background Sync are not universal browser capabilities and cannot be correctness dependencies;
- foreground/open/resume/manual sync paths must recover durable pending work even if optional background APIs never fire;
- WebSocket/WebTransport are server-oriented transports; WebRTC data channels prove peer transport exists but not zero-intervention discovery/signaling/background feasibility; Web Bluetooth remains platform-limited/experimental;
- direct local-network peer sync on a managed EFB remains OPEN pending discovery/addressing, secure-context/TLS, local-network/privacy policy, connectivity and suspension evidence;
- server relay, direct peer and user-mediated export/import are separate architecture options; automatic sync and disaster-recovery backup should remain independent concerns;
- long-offline operation must resume from durable checkpoints and reconcile changes/conflicts rather than blindly overwrite or restart full state;
- production/device claims require the actual managed iPad OS/browser/policy matrix.

## EFB / LogMate-like scenario boundary
**Established in principle:** offline shell/content plus structured local records are feasible web-platform patterns; durable outbox/reconciliation can be specified independently of transport.

Still **OPEN / requires implementation + target-device validation**:
- managed company iPad permits required Home Screen/storage/export/network capabilities;
- actual schema/data model and migration behavior;
- authoritative replica and conflict semantics;
- background synchronization support/reliability on target platform;
- unattended PWA↔native-phone discovery and transport;
- hotspot/Bluetooth/local-network feasibility under company/OS policy;
- authentication/pairing persistence and lost-device behavior;
- independent backup/export/restore on permitted destinations;
- long-offline, duplicate/retry, update-with-pending-outbox and storage-loss recovery.

# Balanced track state
- **A Platform & Browser:** strong foundation; 073–074 materially deepen service-worker/storage/IndexedDB/concurrency/transport boundaries.
- **B UX/IA/Content:** foundation/practitioner complete; PWA handoff now includes local-only/queued/sending/synced/conflict/auth-blocked/recovery state language.
- **C Performance/Accessibility/Quality:** substantial foundation/practitioner; target-device PWA validation matrix now includes crash/outbox, schema upgrade, long offline, duplicate ack loss, backup restore and update transition failures.
- **D Search/Discovery/Analytics:** search/discovery mature; **Stage 9 Analytics/Experimentation is now the highest-value vertical bottleneck**. PWA offline/install/sync measurement will be a major application case.
- **E Architecture/Security/Operations:** security/privacy foundation PASS; PWA durability/sync threat, backup, migration and transport requirements are now bounded, with implementation evidence still OPEN.

# Cross-repository evidence
Design Studio latest checked 2026-09-16: Web Design Stage 1/2 PASS, Stage 3 PRACTICE; W023 provides bounded integrated Chromium transfer but route/network/cross-browser/AT/physical-device/field/human evidence remains OPEN. PWA runtime quality is not inferred from it.

Software Engineering remains the implementation dependency for schema/data IDs, transaction boundaries, migration harness, outbox/idempotent endpoint, conflict algorithm, backup format and target managed-iPad transport experiments. Web Manager retains web capability/risk contracts rather than duplicating engineering.

Marketing must consume verified capability truth; “works offline,” “automatically syncs,” “background sync” or “safe backup” claims remain prohibited until their specific evidence contracts pass.

# Production OPEN register
Actual `minttap.app` routes/runtime, hosting/CDN/origin, TLS/HSTS/headers/CSP/CORS, forms/endpoints, authentication/session, cookies/storage/service worker, web analytics/ads, third parties, personal-data flows/processors/retention, dependencies/build/deployment pipeline, secrets, DNS/registrar controls, monitoring/incidents/rollback, vulnerability contact, and production accessibility/search/performance/security evidence remain OPEN.

PWA additionally requires manifest/install identity, worker scope/version/update policy, CacheStorage/IndexedDB schema, persistence/quota/eviction evidence, offline contract, update/migration strategy, standalone/browser parity, backup/export/restore, synchronization protocol/transport and managed-EFB validation.

# Highest-value next work
Return to the largest vertical curriculum gap: **Stage 9 Analytics / Experimentation (Track D)**. Build the first substantial integrated body from `decision/task semantics → observable event → privacy/minimization → instrumentation contract → offline delivery/idempotency → aggregation/segmentation → attribution/inference limits → experiment/qualitative evidence → decision threshold → re-observation`. Use PWA install/standalone/offline/sync states as major application cases without allowing analytics to become a synchronization correctness dependency.

PWA implementation validation resumes when Software Engineering or actual managed-EFB evidence becomes available.

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model.
- `LEARNING_ROADMAP.md`: canonical vertical curriculum.
- `research/README.md`: staged/specialization research index.
- Stages 1–8: COMPLETE at intended foundation/practitioner level.
- PWA: 073–074 specialization checkpoints PASS; production/device validation OPEN.
- Next vertical block: Stage 9 Analytics / Experimentation.
- Reporting remains coarse/checkpoint-based.