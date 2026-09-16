# MintTap Web Manager Status

Operating state: **ACTIVE — FIVE-TRACK BALANCED DEEP LEARNING**  
Last sync: 2026-09-16  
Domain: `minttap.app`  
Platforms: iOS / App Store, Android / Google Play

## Operating model
GitHub is canonical memory. `LEARNING_ROADMAP.md` is the vertical beginner→expert curriculum; `SPECIALIST_TRACKS.md` is the horizontal five-track expertise model. Web Manager coordinates rather than acting as a sixth specialist. Work is allocated by prerequisite gap, evidence maturity, risk, dependency pressure and live-project value.

Tracks: A Web Platform & Browser; B Web UX/IA/Content Architecture; C Web Performance/Accessibility/Quality; D Search/Discovery/Analytics; E Web Architecture/Security/Operations.

Learning sequence: `history/problem → design principle → standard → current implementation → limitations/failure → cross-domain connection → operational judgment → integrated competency`.

---

# Curriculum state
Stages 1–7: **COMPLETE — FOUNDATION/PRACTITIONER GATES PASSED.**
- Stage 1 Web Foundations: 027–033
- Stage 2 Website Anatomy / Content / IA: 034–038
- Stage 3 UX & Interaction Foundations: 039–044
- Stage 4 Web Design Literacy: 045–050
- Stage 5 Accessibility: 051–058
- Stage 6 Search / Discovery / Content Quality: 059–065
- Stage 7 Web Performance / Browser Runtime: 066–070

These passes do not imply production validation.

# Stage 8 — Security / Privacy / Trust
Status: **ACTIVE — CORE FOUNDATION/PRACTITIONER BODY PASS; INTEGRATION GATE OPEN.**

071 — **Integrated Security / Privacy / Trust Foundations — PASS.**

Track E owned the body and consumed Track A platform/browser foundations rather than duplicating HTTP/TLS/origin/cookie primers.

Established security model:
`asset → actor → data flow → trust boundary → attacker capability → abuse/failure → impact → preventive control → detective/recovery control → residual risk`.

Retained judgments through 071:
- network-channel security, browser isolation, application authorization, input/output safety, deployment/dependency integrity, privacy and human trust are distinct layers;
- same-origin, same-site, same-domain and CORS permission are not synonyms; CORS is not authentication/authorization;
- HTTPS/TLS provides authenticated-channel confidentiality/integrity properties but does not prove application, dependency, endpoint or human trustworthiness;
- cookie, session, authentication and authorization are separate concepts; Secure/HttpOnly/SameSite/Domain/Path attributes solve different problems;
- XSS, CSRF, injection and clickjacking require mechanism-specific defenses rather than attack-name checklists;
- CSP/security headers are policies derived from actual threats and dependencies, not scanner badges; report/observe/enforce/regression is preferred to copied header sets;
- third-party scripts create runtime-authority, supply-chain, privacy, performance and incident-response risk simultaneously;
- privileged secrets do not belong in public browser bundles; secrets need controlled storage/provisioning/access/rotation/audit boundaries;
- secure collection does not imply justified collection: privacy starts with purpose and data minimization before confidentiality controls;
- support/phishing defense includes consistent official identity and safe support habits; generic security badges/claims are trust theater without evidence;
- defense in depth records the failure contained by each control and the residual risk rather than assuming more controls always means more safety.

Reusable artifacts inside 071:
- Web Threat Model Record;
- Third-Party Trust Record;
- privacy/data-minimization question set;
- cross-track transfer matrix;
- seven integrated diagnostic cases.

## Balanced track interpretation
- **A Platform & Browser:** strongest foundation and direct dependency provider for Stage 8. No need to repeat platform primers; production contradictions should return as transfer validation.
- **B UX/IA/Content:** consumes recovery/support/privacy/external-link/destructive-action/trust requirements; production task evidence OPEN.
- **C Performance/Accessibility/Quality:** mature foundation/practitioner; consumes CSP/consent/auth/warning/third-party regression requirements; production cross-browser/AT/field evidence OPEN.
- **D Search/Discovery/Analytics:** search foundation mature, analytics depth remains Stage 9; Stage 8 establishes a privacy/minimization gate before instrumentation.
- **E Architecture/Security/Operations:** 071 closes the largest first-principles gap. Highest-value remaining Stage 8 work is integration/release-readiness and incident/escalation competency, not another attack primer.

## Cross-repository evidence
Design Studio latest checked 2026-09-16: Web Design Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE; W021 execution matrix exists but integrated browser runtime, true HTTP/network, cross-browser, screen-reader, physical-device, field and human evidence remain OPEN. Security handoffs must preserve those evidence boundaries.

Marketing Manager latest checked 2026-09-16: MintTap release branch `1.0.29` evidence includes Firebase Analytics and Google Mobile Ads in the native app implementation, but Store production availability remains UNKNOWN. This is transfer evidence only and **does not prove `minttap.app` uses analytics/ads**.

Software Engineering Studio repository exists but no `STATUS.md` was available at the checked path; no software-engineering evidence was inferred.

## Stage 8 production OPEN register
Actual `minttap.app` hosting/CDN/origin topology, TLS/HSTS/redirects, headers/CSP, CORS, forms/endpoints, auth/session, cookies/storage/service worker, web analytics/ads, third parties, personal-data flows/processors/retention, dependencies/build/deployment pipeline, secrets, DNS/registrar controls, logging/monitoring, incident/rollback/security communication and vulnerability contact process remain OPEN.

Do not infer these from generic patterns or native-app code.

Highest-value next block:
072 — **Stage 8 Integration & Security/Privacy Release-Readiness Operating System.** Stress-test 071 against representative app-company architecture/data-flow cases; derive evidence/release gates, incident/recovery and escalation boundaries; close Stage 8 only if the curriculum exit capability is demonstrated without inventing production facts.

---

# Persistence state
- `AGENTS.md`: five-track + large-bundle governance active.
- `SPECIALIST_TRACKS.md`: canonical horizontal model active.
- `LEARNING_ROADMAP.md`: canonical vertical curriculum active.
- `research/README.md`: staged research index canonical.
- Stages 1–7: complete at intended foundation/practitioner level.
- Stage 8: **ACTIVE; 071 PASS; integration gate OPEN.**
- Reporting: coarse checkpoint-based.
- Next: **072 Stage 8 integration/release-readiness gate**.