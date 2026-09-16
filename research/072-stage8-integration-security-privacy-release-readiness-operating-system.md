# 072 — Stage 8 Integration — Security / Privacy Release-Readiness Operating System

Status: **PASS — STAGE 8 FOUNDATION/PRACTITIONER INTEGRATION GATE**  
Owner: Track E, consuming Tracks A–D dependencies  
Date: 2026-09-16

## Purpose

Test whether 071's security/privacy/trust body can be used as an operational system for a public app-company website without inventing MintTap production facts. This block adds release evidence, incident/recovery, vulnerability-reporting and escalation discipline, then stress-tests representative architectures.

## 1. Security release-readiness chain

`resource/process inventory → data-flow/trust-boundary model → abuse/threat cases → control requirements → implementation evidence → negative/abuse testing → privacy review → dependency/third-party review → recovery/rollback evidence → residual-risk decision → release → monitoring → incident learning`

A release is not “secure” because a scanner is green. Release readiness is bounded evidence that identified material threats have appropriate preventive/detective/recovery controls and known residual risk.

## 2. Minimum Security/Privacy Release Record

For each material page/process/change preserve:
- release/commit/deployment identity;
- affected routes/endpoints/origins;
- assets/data handled;
- threat-model revision;
- auth/session/authorization implications if any;
- browser policy changes: CORS/CSP/cookies/frames/permissions;
- new/changed third parties and data flows;
- dependency/version changes;
- secrets/config changes without storing secret values in the record;
- privacy purpose/minimization/retention implications;
- security regression evidence;
- accessibility/performance/task regression handoffs;
- logging/detection changes;
- rollback/revocation capability;
- residual risks/exceptions and owner;
- specialist/legal escalation state;
- post-release observation trigger.

## 3. Release gate severity model

Do not invent a universal numeric risk score. Use consequence/reach/reversibility/evidence quality.

**Block release** when evidence shows or reasonably indicates a material unauthorized disclosure/action, credential/secret exposure, executable injection, broken authorization, dangerous dependency compromise, misleading security/privacy behavior, or an uncontained high-impact trust failure and no approved mitigation exists.

**Require explicit exception/owner** when residual risk is understood but cannot yet be removed and the product owner/security specialist has enough evidence to judge consequence and containment.

**Do not block solely on** a generic scanner score, absent header that has no applicable threat, or a single theoretical finding without demonstrating applicability. Investigate first.

## 4. Incident response is part of design

### SOURCE
NIST SP 800-61r3 (final April 2025) integrates incident response into broader cybersecurity risk management rather than treating it as an isolated after-the-fact procedure. NIST CSF 2.0 organizes cybersecurity outcomes across Govern, Identify, Protect, Detect, Respond and Recover.

### SYNTHESIS
A control without a failure plan is incomplete. For consequential web assets define before release:
`detect → triage → contain → preserve evidence → eradicate/fix → restore → communicate → monitor recurrence → learn/update model`.

Not every event is a public incident. Severity and communication must be evidence-based; avoid both silence-by-default and premature speculative notices.

### App-company examples
- compromised store/download link: contain publishing path/account, restore verified destination, audit affected period, coordinate user communication if harm plausibly occurred;
- leaked deployment secret: revoke/rotate first, determine scope/use, preserve evidence, remove source/history exposure as appropriate, review privilege and detection;
- compromised third-party script: disable/remove or constrain integration, inspect accessible data/actions and affected period, coordinate vendor evidence, regression-test replacement;
- phishing impersonation: preserve evidence, use provider/domain abuse channels, reinforce official identity/support guidance, investigate whether internal accounts/content were also compromised.

## 5. Vulnerability disclosure boundary

### SOURCE
RFC 9116 defines `security.txt` as a machine-parsable way to advertise vulnerability-disclosure contacts/practices and specifies the `/.well-known/security.txt` location for web services. OWASP recommends a clear reporting route and organizational routing for incoming security reports.

### SYNTHESIS
`security.txt` is a routing mechanism, not a bug-bounty promise, security certification or incident-response system. Publish it only when a monitored contact and response process actually exist. The contact path must not become an abandoned trust signal.

### OPEN
MintTap currently has no verified vulnerability-reporting contact/process in this study. Do not publish invented addresses/policies.

## 6. Representative architecture stress tests

### Scenario 1 — static company/product site, no login
Risk is not zero. Highest-value assets include domain/DNS/deployment authority, store links, support/privacy truth and third-party scripts. Controls prioritize deployment/account integrity, HTTPS, least third-party authority, content integrity, framing/injection boundaries where applicable, dependency governance and recovery. Authentication-specific controls are not fabricated.

### Scenario 2 — support form added
New boundaries: user input, backend/mail/ticket processor, abuse/spam, personal data, retention and output rendering. Required work: data minimization, server validation, injection/output-safety analysis, rate/abuse strategy, processor/data-flow record, privacy communication, logging without excessive sensitive content, failure/retry semantics and deletion/retention ownership.

### Scenario 3 — authenticated web account/deletion flow
New assets: identity/session/account state and destructive authority. Required work expands to authentication/session lifecycle, server authorization, CSRF where ambient credentials apply, re-authentication/confirmation for consequential actions, audit/recovery, privacy/legal requirements and accessible error/recovery UX. Merely adding SameSite or a confirmation dialog is insufficient.

### Scenario 4 — analytics/ads added to website
First establish purpose and minimum event/data set. Then map third-party execution/network/storage, consent/legal/platform requirements where applicable, CSP/performance impact, data retention/access, opt-out/withdrawal behavior where required, event-version governance and downstream decision use. Native-app SDK presence is not evidence of website necessity.

### Scenario 5 — external support/chat widget
Treat widget as a third-party runtime principal. Inventory DOM/data access, cookies/storage, network destinations, user-entered sensitive data, CSP requirements, failure/availability, accessibility, performance, vendor account compromise and kill-switch/removal path. Prefer a plain link/contact route if the widget's authority/cost exceeds demonstrated value.

### Scenario 6 — CDN/hosting migration
Security review includes DNS/certificate/TLS, origin exposure, cache of sensitive responses, headers, redirects, deployment credentials, provider IAM, logs, rollback, old-host retirement and supply-chain/account recovery. A visually identical migration can materially change trust boundaries.

## 7. Negative testing derived from threat model

Testing should target invariants, not just happy paths:
- unauthorized user/object/action rejected server-side;
- untrusted text remains data in every output context;
- state-changing requests cannot rely solely on cross-origin read blocking;
- embedding policy matches actual business requirement;
- CSP blocks the intended dangerous class without breaking required resources;
- secrets are absent from public bundles/logs/artifacts where they grant privilege;
- third-party failure/disable path preserves the core task where possible;
- privacy withdrawal/denial states do not deceptively block unrelated core tasks;
- security warnings/errors are keyboard/AT/readable and do not rely on color alone;
- rollback/revocation actually restores a known-safe state.

General code-level implementation/testing belongs to Software Engineering; Track E supplies these web security invariants and consumes returned evidence.

## 8. Evidence confidence and escalation

### Web Manager may own
- inventory and data-flow requirements;
- browser/web threat model;
- security-header/cookie/CORS requirements at architecture level;
- third-party trust record;
- privacy minimization questions;
- release evidence record;
- monitoring/rollback/contact requirements;
- identifying when evidence is insufficient.

### Escalate to security specialist when
- authentication/authorization design is nontrivial;
- sensitive/high-impact personal or financial data is handled;
- cryptographic design beyond standard platform use is proposed;
- exploitable injection/access-control/secret compromise is suspected;
- complex CSP/CORS/cross-origin integration creates uncertainty;
- incident scope/forensics materially affects users;
- penetration testing or adversarial validation is needed.

### Escalate to privacy/legal when
- legal basis/consent/notice/retention/deletion/cross-border or jurisdiction obligations must be decided;
- analytics/advertising/identifiers/processors create regulatory uncertainty;
- breach/security communication has legal notification implications.

### Cross-track escalation
B for task/recovery/trust content structure; C for accessibility/performance/cross-browser regression; D for analytics/search measurement constraints; Design Studio for presentation/interaction evidence; Marketing for acquisition/ad strategy; Software Engineering for implementation/code/test architecture.

## 9. Contradiction checks

- **HTTPS + vulnerable app:** no contradiction; TLS and application safety are different layers.
- **CSP blocks third party + business says required:** not proof CSP is wrong; validate necessity, least authority and policy architecture.
- **Analytics desired + minimization rejects fields:** business curiosity does not override privacy purpose discipline; redesign measurement.
- **Security friction lowers conversion:** neither conversion nor security wins automatically; identify consequence, alternative control and user harm.
- **scanner PASS + no threat model:** scanner is evidence for bounded checks, not integration-gate proof.
- **native app vendor evidence + clean web network trace:** preserve surface distinction; do not force company-wide vendor assumptions.

## 10. Stage 8 competency assessment

Roadmap exit capability requires recognizing ordinary website security/privacy risks, knowing when specialist security/legal review is required, and evaluating trust claims against evidence.

Assessment result:
1. threat/trust-boundary diagnosis — PASS;
2. TLS/origin/cookie/session boundary reasoning — PASS;
3. XSS/CSRF/injection/clickjacking defensive distinctions — PASS;
4. threat-derived CSP/header reasoning — PASS;
5. dependency/supply-chain/secrets reasoning — PASS;
6. privacy/minimization/analytics-ad boundary — PASS;
7. support/phishing/trust communication — PASS;
8. release/negative-test/residual-risk governance — PASS;
9. incident/recovery/vulnerability-reporting boundary — PASS;
10. specialist/legal escalation — PASS;
11. production MintTap validation — OPEN by design, because real runtime/project evidence is unavailable.

**STAGE 8 FOUNDATION/PRACTITIONER INTEGRATION GATE: PASS.**

This pass establishes transferable judgment; it does not certify `minttap.app` as secure/private/compliant.

## 11. Next curriculum boundary

Stage 9 — Analytics / Experimentation is now the highest-value curriculum gap, led primarily by Track D with Stage 8 privacy/minimization as a mandatory dependency and Track B task semantics as a measurement dependency.

Start from `business/user decision → observable behavior → event semantics → data minimization → instrumentation → aggregation/segmentation → inference limits`, not from vendor dashboards.

## Sources rechecked 2026-09-16
- NIST CSF 2.0 (2024) — risk-governance outcome framework.
- NIST SP 800-61r3 final (2025-04-03) — incident response integrated into cybersecurity risk management.
- RFC 9116 — `security.txt` vulnerability-disclosure routing format/location.
- OWASP Vulnerability Disclosure Cheat Sheet — organizational reporting/routing practices.
- 071 source set remains inherited for TLS, browser security, attack/control, privacy and secrets foundations.

CHANGE WATCH: incident guidance, browser security behavior, platform/privacy rules and vendor integrations require current verification before production use.