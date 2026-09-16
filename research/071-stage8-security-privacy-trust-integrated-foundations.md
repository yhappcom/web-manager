# 071 — Stage 8 Security / Privacy / Trust — Integrated Foundations

Status: **PASS — FOUNDATION/PRACTITIONER CORE BODY**  
Owner: **Track E — Web Architecture, Security & Operations**  
Primary dependency: **Track A — Web Platform & Browser**  
Date: 2026-09-16

## Purpose

Build the Stage 8 security/privacy/trust core as one integrated body rather than a header checklist. The objective is defensive Web Manager judgment for a public Apple/Android app-company website: identify assets and trust boundaries, reason about browser/server threats, derive controls from threats, understand privacy as a separate risk discipline, and know what remains unproven without production evidence.

This block consumes Track A's existing URL/origin/HTTP/TLS/browser/cookie foundations. It does not rewrite those primers.

---

## 1. First-principles operating model

### SOURCE
MDN describes the same-origin policy as a critical browser security mechanism that restricts how a document/script from one origin can interact with resources from another origin. Origin is principally the scheme/host/port tuple. Cross-origin network access and cross-origin script/data access are not identical capabilities; CORS can selectively relax browser read access. Browser storage such as Web Storage and IndexedDB is origin-partitioned, while cookies use domain/path/site semantics that differ from the origin model.

RFC 8446 defines TLS 1.3's secure-channel goals as server authentication (client authentication optional), confidentiality and integrity. TLS protects the transport channel; it does not prove that application logic, JavaScript, dependencies, endpoints or people are trustworthy.

OWASP guidance treats application security as a collection of threat-specific defensive practices rather than one control.

### SYNTHESIS
Security reasoning starts with:

`valuable asset → actor → entry/data flow → trust boundary → attacker capability → abuse/failure → impact → preventive control → detective/recovery control → residual risk`

Not:

`header list → green scanner → secure site`.

A useful separation is:

`network-channel security ≠ browser isolation ≠ application authorization ≠ input/output safety ≠ deployment integrity ≠ dependency integrity ≠ privacy ≠ human trust`.

A control only earns credit for the threat it actually changes.

---

## 2. Threat modeling for an app-company website

### SOURCE / established method
Threat modeling commonly identifies system components/data flows/trust boundaries and asks what can go wrong. OWASP also emphasizes business-process threat modeling: technically valid steps can still be abused by reordering, repetition, concurrency or false assumptions about user intent.

### Reusable Web Threat Model Record
For each meaningful website capability record:
- capability/page/process;
- protected assets: user data, credentials/session, support channel, release/download identity, legal/privacy truth, analytics identifiers, deployment credentials, domain/DNS, brand trust;
- actors: anonymous visitor, authenticated user if applicable, support operator, deployer, third-party provider, malicious site, compromised dependency/account;
- data flows and stores;
- browser/server/third-party trust boundaries;
- attacker preconditions/capabilities;
- abuse cases and impact;
- existing controls and their exact scope;
- detection/logging/recovery;
- residual risk;
- owner/escalation path;
- evidence state: SOURCE / OBSERVED / OPEN / VALIDATION.

### App-company-specific high-value identity surfaces
Even a mostly informational app-company site can carry consequential identity:
- official app/store links;
- support/contact instructions;
- privacy/account-deletion instructions;
- release/status/security notices;
- company/domain identity.

Compromise or misleading content on these surfaces can redirect users or destroy trust without requiring an authenticated web application.

---

## 3. Origin and browser trust boundaries

### SOURCE
Same-origin policy prevents arbitrary cross-origin script reads of protected data. It does not mean cross-origin requests cannot occur: links, forms, images, scripts, frames and other mechanisms have different cross-origin behavior. CORS is a server-declared browser permission mechanism for cross-origin reads; it is not authentication and does not stop non-browser clients from making HTTP requests.

### SYNTHESIS
`same origin`, `same site`, `same domain` and `allowed by CORS` are not synonyms.

Before configuring CORS/cookies/frames, identify which boundary the requirement actually crosses. Broadly allowing origins to fix a development error can destroy a security boundary without solving authentication or authorization.

### Failure cases
- Treating CORS as server-side access control.
- Assuming SOP prevents cross-site state-changing requests.
- Assuming subdomains are automatically equally trusted.
- Assuming a cookie's Domain/Path provides the same isolation as origin-scoped storage.

---

## 4. HTTPS/TLS properties and limits

### SOURCE
TLS 1.3 provides an authenticated secure channel with confidentiality and integrity when authentication/validation is correctly performed. RFC 8446 also documents limits: TLS does not conceal all traffic metadata/length and cannot make compromised endpoints safe.

### SYNTHESIS
HTTPS answers primarily: **“Is this browser communicating over a protected channel with the authenticated endpoint represented by this certificate/connection?”** It does not answer:
- Is the website code free of XSS?
- Is the user authorized for this object/action?
- Is a third-party script benign?
- Is the backend free of injection?
- Is a support instruction truthful?
- Is collected data necessary?

Therefore the lock/HTTPS indicator is a prerequisite trust signal, not proof of application trustworthiness.

### VALIDATION for production
Actual `minttap.app` TLS versions/certificate chain/HSTS/redirect behavior are OPEN and require live inspection before claims.

---

## 5. Cookies, sessions and authentication boundaries

### SOURCE
MDN documents cookie attributes with different jobs:
- `Secure` constrains sending to secure contexts;
- `HttpOnly` prevents JavaScript access to the cookie;
- `SameSite` controls cross-site sending and can mitigate some CSRF/cross-site leakage;
- Domain/Path scope cookie delivery but Path is not a security boundary.
`SameSite=None` requires `Secure` in modern browsers. Browser defaults and third-party-cookie behavior are change-sensitive.

### SYNTHESIS
`cookie ≠ session ≠ authentication ≠ authorization`.

A cookie may carry an identifier; server-side session state may map it to an identity; authentication establishes identity; authorization decides whether that identity may perform the requested action. Each request that changes or discloses protected state still needs the appropriate authorization decision.

### Defensive session model if MintTap web ever authenticates
- minimize cookie scope/lifetime;
- use Secure/HttpOnly where appropriate;
- choose SameSite from actual navigation/integration requirements, not habit;
- rotate/revoke session credentials when risk warrants;
- enforce authorization server-side;
- treat CSRF separately where ambient credentials can authorize state-changing requests;
- avoid sensitive tokens in URLs/client-readable storage without a justified threat analysis.

### OPEN
Whether `minttap.app` currently has authentication, account sessions, cookies or user-specific web data is unknown.

---

## 6. XSS, CSRF, injection and clickjacking — mechanism-first distinctions

### XSS
**Threat:** attacker-controlled data becomes executable content in another user's browser under the trusted site's origin.

**Control families:** context-appropriate output encoding/escaping, safe DOM APIs/framework defaults, sanitization for intentionally accepted HTML, avoiding dangerous sinks, and CSP as defense in depth. CSP does not excuse unsafe output handling.

**Impact connection:** origin authority can expose DOM data, perform same-origin actions, alter support/store links or misuse client-accessible credentials.

### CSRF
**Threat:** a malicious site causes a victim's browser to send a state-changing request that carries ambient authority such as cookies.

**Control families:** anti-CSRF tokens for applicable state-changing operations, SameSite cookies as partial defense, origin/fetch-metadata validation where appropriate, safe HTTP semantics, and re-authentication/confirmation for high-impact actions.

**Distinction:** SOP can prevent reading many cross-origin responses but does not by itself prevent all cross-origin writes/requests.

### Injection
**Threat:** untrusted data crosses from data into an interpreter/query/command language and changes intended execution.

**Control families:** parameterized APIs/prepared statements, strict typed interfaces, avoiding command construction, allow-list validation where appropriate, least privilege, and separate secrets/credentials. Escaping rules are context-specific; one universal sanitizer is not a general solution.

### Clickjacking
**Threat:** an attacker frames or overlays a trusted interface and tricks the user into activating it.

**SOURCE:** CSP `frame-ancestors` controls which parent origins may embed a document; MDN notes X-Frame-Options as an older, less expressive mechanism. `frame-src` controls what the page itself may load in frames and is a different directive.

**Control families:** derive an embedding policy from actual product needs; use `frame-ancestors` and compatibility defense where warranted. SameSite cookies may reduce some authenticated framing impact but are not the primary UI-redress control.

### Transfer rule
Do not use attack names as checkboxes. For every issue identify `source → trust boundary → dangerous operation/authority → impact` before choosing controls.

---

## 7. CSP and security headers derived from threats

### SOURCE
CSP can restrict resource sources, form targets, embedding parents and other document capabilities; Report-Only/reporting mechanisms can observe policy violations. `frame-ancestors` has no `default-src` fallback and cannot be supplied through a meta element.

### SYNTHESIS
A security header is a **policy enforcement surface**, not a badge. The correct sequence is:

`asset/threat → required browser capability → least necessary policy → compatibility/dependency inventory → report/observe → enforce → monitor regression`.

### Header families and their jobs
- **CSP:** reduce/contain script/resource/content injection and navigation/embedding capabilities according to directives actually configured.
- **frame-ancestors / X-Frame-Options:** embedding/clickjacking boundary.
- **HSTS:** HTTPS transport downgrade/HTTP retry boundary after policy is known to the browser; requires deployment/domain planning.
- **Referrer-Policy:** control referrer information disclosure.
- **Permissions-Policy:** restrict selected powerful feature use/delegation.
- **X-Content-Type-Options:** reduce MIME-sniffing ambiguity where supported.

These are not interchangeable. A “strict” header set can also break analytics, store widgets, support tooling, fonts/media or future integrations if deployed without dependency evidence.

### Operational pattern
Start with actual resource/feature inventory. For CSP, prefer nonce/hash/strict source approaches where architecture permits rather than maintaining uncontrolled host allowlists. Use reporting carefully: reports themselves can contain URLs/context and create privacy/operational data that needs governance.

### CHANGE WATCH
Browser support, reporting behavior and header semantics evolve; recheck current platform documentation before production changes.

---

## 8. Third-party, dependency, supply-chain and secrets risk

### SOURCE
OWASP secrets guidance emphasizes centralized storage/provisioning/auditing/rotation and warns against plaintext/hardcoded secrets in source/configuration. It explicitly recommends relying on the chosen secrets-management system's current official documentation for implementation specifics.

### SYNTHESIS
A third-party script executes with far more authority than a simple outbound link. Loading it into the first-party page can create simultaneous:
- confidentiality risk;
- integrity/XSS-equivalent risk if supplier/CDN/account is compromised;
- availability/performance risk;
- privacy/tracking risk;
- CSP complexity;
- incident-response dependency.

A dependency decision therefore needs both **runtime authority** and **supply-chain lifecycle** analysis.

### Reusable Third-Party Trust Record
Record:
- business/task necessity;
- execution context and origin;
- data accessible/sent;
- cookies/storage/network behavior;
- required CSP/permissions;
- update/version ownership;
- compromise/blast radius;
- failure behavior;
- removal path;
- privacy/legal review trigger;
- performance cost handoff to Track C.

### Secrets boundary
Public browser bundles cannot safely contain server secrets. “Obscuring” a key in JavaScript is not secret management. Distinguish publishable client identifiers from credentials that grant privileged authority; the latter belong behind controlled server/deployment boundaries with least privilege, rotation and audit.

---

## 9. Privacy is not merely confidentiality

### SOURCE
NIST Privacy Framework describes privacy risk management as an organizational discipline for identifying/managing risks to individuals while enabling products/services. It is explicitly a living framework.

### SYNTHESIS
`secure collection ≠ justified collection`.

Encryption can protect unnecessary data perfectly while the collection itself still creates privacy risk. Privacy analysis therefore begins before security controls:

`purpose → minimum data → lawful/appropriate basis and user expectation → collection → processing/sharing → retention → access/deletion → disclosure/communication → retirement`.

### Web data-minimization questions
For analytics, ads, support forms, error telemetry or personalization:
1. What decision/function requires this datum?
2. Can the purpose be met with less precise/less persistent data?
3. Is identity necessary?
4. Is cross-site/cross-device linkage necessary?
5. Who receives it?
6. How long is it retained?
7. What happens when consent/permission changes where applicable?
8. Can users understand the practice from the site's communication?
9. Can collection be removed without breaking the core task?

### Marketing transfer validation
Marketing Manager's canonical evidence verifies Firebase Analytics and Google Mobile Ads in MintTap **app release implementation branch 1.0.29**, but explicitly does not prove current Store production availability. That native-app evidence does **not** prove `minttap.app` uses those services. Website analytics/advertising remains OPEN until web runtime/code evidence exists.

This is a useful contradiction guard: `company uses vendor somewhere ≠ every product surface sends data to vendor`.

### LEGAL/PLATFORM ESCALATION
Consent, privacy notice, retention and jurisdiction-specific legal obligations require current legal/platform review. Web Manager can define data-flow evidence and minimization requirements but must not invent legal conclusions.

---

## 10. Support abuse, phishing and trust communication

### SYNTHESIS
Trust is partly a security property of **recognizable, consistent, verifiable identity**. A legitimate site can be secure technically and still train users into unsafe behavior.

For app-company support/governance surfaces:
- keep official domains/channels explicit and consistent;
- never ask for credentials/secrets that support does not need;
- make account/recovery/security instructions specific about what the company will and will not request;
- treat outbound store/download links as integrity-sensitive content;
- distinguish status/security notices from marketing copy;
- preserve accessible, non-color-only warning/status communication;
- design anti-abuse friction proportionally so it does not block legitimate users.

### Failure mode: trust theater
Padlocks, generic “bank-level security,” security badges or vague privacy promises are not substitutes for evidence. Claims should map to implemented controls and be narrow enough to remain true.

### Design Studio handoff
If security warnings, external-link confirmation, destructive/recovery flows, cookie/privacy controls or trust notices become real project surfaces, Track E supplies threat/consequence requirements. Design Studio/Layout-Interaction and Content Design own reusable presentation/interaction/content evidence. Security must not force dark patterns or inaccessible warnings.

---

## 11. Defense in depth and residual risk

### SYNTHESIS
No single layer is assumed perfect.

Example XSS defense chain:
`safe templating/encoding → safe DOM usage → sanitization where HTML is required → CSP containment → HttpOnly limits credential readout → authorization/server validation → monitoring/response`.

Example authenticated state-change chain:
`authentication → scoped session → authorization → CSRF defense → input validation/business invariant → audit/detection → recovery`.

Defense in depth is not “more controls is always better.” Each control has compatibility, operational and privacy cost. Record what failure it contains and what remains possible after it fails.

Residual risk belongs in the decision record rather than being hidden by a PASS label.

---

## 12. Cross-track transfer matrix

### Track A — Platform & Browser
Canonical owner of origin, HTTP/TLS, cookie/storage and browser mechanics. Track E consumes these mechanics and owns security/operations decisions. If production evidence contradicts assumed browser behavior, return a transfer-validation case to A rather than rewriting the platform primer.

### Track B — UX / IA / Content Architecture
Consumes security requirements for recovery, support, privacy, external links, destructive actions and trust communication. B must prevent security friction from making legitimate tasks ambiguous or impossible.

### Track C — Performance / Accessibility / Quality
Security controls and third parties can affect performance and compatibility. CSP violations, consent tooling, authentication states and warnings need accessibility/cross-browser regression evidence. A security control that silently breaks the primary task is not production-ready.

### Track D — Search / Discovery / Analytics
Security/privacy can constrain analytics instrumentation and crawler-visible behavior. Do not block public discovery accidentally with auth/security middleware. Analytics requirements must pass data-minimization/privacy review before instrumentation.

### Track E — owner
Owns threat model, security/privacy architecture requirements, operational control evidence, residual risk and escalation.

---

## 13. Integrated diagnostic competency cases

### Case A — “CORS error; allow `*`”
Reject solution-first reasoning. Identify caller origin, requested resource, credentials, intended trust relationship and whether browser read permission is actually required. CORS does not replace authentication/authorization.

### Case B — “HTTPS means the support form is secure”
HTTPS protects channel confidentiality/integrity/authentication. Still inspect data necessity, server validation, injection/output paths, retention, access, abuse/spam, third-party processors and privacy communication.

### Case C — “Set SameSite, CSRF solved”
SameSite is one browser cookie control with navigation/integration semantics. Determine whether ambient credentials authorize state changes and whether anti-CSRF tokens/origin checks or stronger confirmation are needed.

### Case D — “Add CSP from an online generator”
First inventory scripts/styles/fonts/media/frames/forms and required integrations. Derive policy from threats and architecture; observe/report, then enforce and regression-test. A copied policy can either remain too broad or break the site.

### Case E — compromised analytics/support script
Treat as first-party execution authority if loaded into the page. Evaluate accessible DOM/data, session-token exposure, outbound requests, integrity of store/support links, CSP containment, kill switch/removal, provider account compromise and incident communication.

### Case F — “Collect more analytics now; maybe useful later”
Fail data-minimization gate. Define decision/use first, collect the least data that supports it, version the event definition, define retention and privacy/legal review triggers.

### Case G — phishing using MintTap brand
Technical website controls cannot eliminate off-site impersonation. Preserve strong official-domain/store/support identity, avoid unsafe support habits, maintain incident/escalation process, and make user-facing claims/instructions verifiable.

---

## 14. Stage 8 core competency gate

PASS at FOUNDATION/PRACTITIONER core-body level if Web Manager can:
1. build an asset/actor/data-flow/trust-boundary threat model before selecting controls;
2. distinguish TLS channel security, origin isolation, CORS, cookie/site semantics, authentication and authorization;
3. explain XSS/CSRF/injection/clickjacking mechanisms and derive bounded defensive controls;
4. derive CSP/security-header requirements from actual threats/dependencies rather than scanner scores;
5. evaluate third-party runtime authority, supply-chain lifecycle and secret boundaries;
6. separate privacy purpose/minimization from security confidentiality;
7. identify support/phishing/trust-communication risks without trust theater;
8. use defense in depth while recording residual risk and operational cost;
9. route implementation, design, marketing, analytics and legal dependencies to their canonical owners;
10. refuse production-security claims without actual MintTap runtime/config/data-flow evidence.

**Result: PASS — core Stage 8 foundation/practitioner body established.**

This does not yet close Stage 8. A final integration/release-readiness block should stress-test the model against an app-company architecture, security-header/data-flow evidence plan, incident/recovery boundaries and specialist escalation criteria before the curriculum gate closes.

---

## 15. MintTap OPEN / VALIDATION register

Do not infer any of the following until verified:
- actual `minttap.app` hosting/CDN/origin topology;
- HTTP→HTTPS/HSTS/TLS/certificate behavior;
- CSP or other security headers;
- CORS policy;
- forms/support/contact endpoints;
- authentication/account/session behavior;
- cookies, local/session storage, IndexedDB or service-worker state;
- analytics/advertising on the website;
- third-party scripts/widgets/fonts/media processors;
- personal-data fields/data flows/processors/retention;
- dependency/build/deployment pipeline;
- secret storage/rotation/access model;
- DNS/domain registrar controls;
- logging/monitoring/incident response;
- backups/rollback/security communication process;
- vulnerability/security contact process.

Production validation requires live response/header/browser/storage/network inspection plus architecture/configuration evidence and, where relevant, specialist security/privacy/legal review.

---

## Sources rechecked 2026-09-16

Primary/current references used:
- RFC Editor — TLS 1.3 / RFC 8446 (secure-channel goals and limits).
- MDN Web Docs — Same-origin policy; HTTP cookies / Set-Cookie; third-party cookies; CSP and `frame-ancestors`; X-Frame-Options; clickjacking.
- OWASP Cheat Sheet Series — application-security defensive guidance; secrets management; business-logic threat modeling.
- NIST Privacy Framework — organizational privacy-risk management.

CHANGE WATCH: browser cookie defaults/third-party-cookie behavior, CSP/reporting support, privacy/platform requirements and security recommendations must be rechecked before production decisions.