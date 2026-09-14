# 030 — HTTPS, TLS, Certificates & Browser Trust — Integrated Foundations

Status: **STAGE 1 CORE COMPLETE — FOUNDATION/PRACTITIONER CHECKPOINT**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Purpose

This study establishes the Web Manager's first-principles model of HTTPS/TLS and the Web PKI. It deliberately avoids treating HTTPS as “HTTP plus a padlock” or certificates as files that merely need renewal.

The professional questions are:

1. What problems does plaintext HTTP leave unsolved?
2. What security properties does TLS actually provide, and what does it not hide?
3. Why did SSL evolve into TLS, and why did TLS 1.3 substantially simplify the protocol?
4. Why are both asymmetric and symmetric cryptography involved?
5. What does a browser actually validate when it accepts a public website certificate?
6. How do roots, intermediates, leaf certificates, hostname verification, SNI, ALPN and HSTS fit together?
7. Why can a site have a “valid certificate” yet still fail securely?
8. How should a Web Manager diagnose failures across browser ↔ edge ↔ origin boundaries?
9. What is special about MintTap using the `.app` top-level domain?

This is Stage 1 depth. TLS/Web PKI will be reopened in Stage 8 security/privacy and Stage 11 operations.

---

# 1. The problem HTTPS solves

## SOURCE

RFC 9846, the current TLS 1.3 specification published in July 2026, defines TLS as a secure channel intended to provide:

- **authentication** — the server side is authenticated; client authentication is optional;
- **confidentiality** — protected application data is visible only to the endpoints;
- **integrity** — modification of protected data can be detected.

RFC 6797's HSTS rationale similarly notes that ordinary transport such as TCP does not itself provide confidentiality, channel integrity, or secure host identification.

## FOUNDATION

Plain HTTP can transfer correct-looking pages while still leaving a network attacker able, in principle, to:

- read traffic;
- alter traffic;
- impersonate a destination if the client has no authenticated binding to the intended service.

These are three different problems. Encryption alone is not sufficient because an encrypted channel to the wrong party is still the wrong channel.

## SYNTHESIS

A useful mental model is:

`HTTPS = HTTP semantics carried over a TLS-protected connection, plus application rules for verifying the intended service identity.`

TLS protects the channel; HTTP still supplies the application semantics learned in Study 029.

---

# 2. Historical evolution — SSL → TLS

## SOURCE

RFC 6101 preserves SSL 3.0 as a historical protocol. It records SSL 3.0 as a Netscape-originated protocol designed to prevent eavesdropping, tampering and message forgery.

RFC 2246 standardized TLS 1.0 in 1999 and explicitly states that TLS was based on SSL 3.0. TLS 1.0 and SSL 3.0 were similar but not wire-compatible.

RFC 8996 formally deprecated TLS 1.0 and TLS 1.1 in 2021.

In July 2026, RFC 9846 replaced RFC 8446 as the current TLS 1.3 specification. RFC 9846 retains TLS version 1.3 and is backward-compatible with RFC 8446, but tightens and clarifies requirements, including forbidding negotiation of TLS 1.0/1.1.

## FOUNDATION

The important historical line is not a list of version numbers. It is a progressive reduction of insecure/legacy options and protocol complexity.

`SSL 3.0 → TLS 1.0 → TLS 1.1 → TLS 1.2 → TLS 1.3`

The modern direction is toward:

- fewer legacy algorithms;
- authenticated encryption;
- forward-secret public-key key exchange;
- fewer round trips;
- less handshake plaintext after ServerHello;
- clearer key separation;
- fewer downgrade/compatibility traps.

## CURRENT-STANDARD CORRECTION

Do not cite RFC 8446 as the final current normative TLS 1.3 specification without qualification. As of July 2026, **RFC 9846 obsoletes RFC 8446**.

This is a good example of why the Web Manager must distinguish durable concepts from living standards.

---

# 3. TLS 1.2 → TLS 1.3: why the protocol changed

## SOURCE — RFC 9846

RFC 9846 identifies major TLS 1.3 changes from TLS 1.2, including:

- legacy symmetric algorithms removed; remaining record protection uses AEAD;
- cipher-suite meaning simplified so authentication/key exchange are not bundled the old way;
- static RSA and static Diffie-Hellman key exchange removed;
- public-key key exchange provides forward secrecy;
- handshake messages after ServerHello are encrypted;
- key derivation redesigned around HKDF and improved separation;
- handshake state machine substantially simplified;
- legacy compression removed;
- version negotiation moved to an extension-based mechanism;
- session resumption/PSK mechanisms consolidated;
- optional 0-RTT added, with weaker replay/security properties than ordinary 1-RTT traffic.

RFC 9846 also tightens RFC 8446 in 2026, including banning KeyShare reuse between connections and forbidding TLS 1.0/1.1 negotiation.

## SYNTHESIS

TLS 1.3 should be understood as an architectural cleanup driven by accumulated protocol experience, not merely “stronger encryption.”

It narrows the number of ways peers can create an allegedly secure connection. Fewer legacy choices reduce downgrade, configuration and implementation complexity.

## Web Manager judgment

A server saying “TLS enabled” is not enough. The protocol version, supported algorithms, certificate validation and application integration all determine whether the resulting connection is appropriate.

---

# 4. Why asymmetric and symmetric cryptography both appear

## FOUNDATION

The tasks are different.

### Asymmetric cryptography / authenticated key establishment
Useful for establishing/authenticating secrets between peers that did not already share one and for proving possession of a private key associated with an authenticated identity.

### Symmetric cryptography
Efficiently protects large amounts of application traffic after shared traffic keys have been established.

TLS therefore does not normally encrypt every web byte directly with a server's certificate public key.

The handshake authenticates/negotiates and establishes shared keying material; the record protocol then protects application data with derived traffic keys.

## SOURCE

RFC 9846 explicitly separates:
- the **handshake protocol**, which authenticates peers, negotiates parameters and establishes shared key material; and
- the **record protocol**, which protects application traffic using the negotiated traffic keys.

## Misconception corrected

**“The SSL certificate encrypts the website.”**

Too imprecise. A certificate participates in authentication/key binding. The negotiated TLS session keys protect the actual traffic.

---

# 5. Certificate ≠ trust by itself

## FOUNDATION

An X.509 certificate is a signed data structure that binds identifiers and other claims to a public key under a PKI policy.

For a public website, browser acceptance requires more than “a certificate exists.” The browser/relying party needs to determine that:

1. the certificate is within its validity period;
2. signatures/path constraints validate through an acceptable certification path;
3. the path terminates at a trust anchor the client accepts;
4. the intended service identity matches the certificate;
5. applicable usage/constraints/policies are satisfied;
6. browser/root-program requirements such as Certificate Transparency are satisfied where required;
7. no fatal protocol/certificate condition invalidates the connection.

## SOURCE — RFC 5280

RFC 5280 defines Internet X.509 PKI certificate/path validation concepts. A valid path begins at a trust anchor selected as a matter of local policy. Different applications can rely on different trust anchors.

## Critical consequence

There is no single universal “Internet root certificate list” that every browser/OS must use identically.

Trust is ultimately a relying-party policy decision. Chrome, Mozilla, Apple and operating systems maintain their own trust programs/policies and can impose requirements beyond bare RFC path validation.

---

# 6. Root → intermediate → leaf model

## FOUNDATION

A common publicly trusted website chain is conceptually:

`trust anchor/root → intermediate CA → subscriber/leaf TLS certificate`

### Root / trust anchor
A public key/CA identity already trusted by the browser or platform according to local/root-program policy.

### Intermediate CA
A CA certificate signed beneath another CA. It allows operational issuance without routinely using the root private key.

### Leaf / subscriber certificate
The certificate presented for the website/service and containing the service identifiers/public key information used in server authentication.

## SOURCE

RFC 5280 defines certification-path processing. Current Chrome and Mozilla root policies separately govern which public roots remain accepted in their products.

## Operational implication

A server often must provide the appropriate leaf and intermediate chain material. The root is ordinarily already trusted by the client and need not be transmitted as the thing that creates trust.

“Certificate installed” does not prove the served chain is usable by every target client.

---

# 7. Domain control and service identity are related but not identical concepts

## SOURCE — current public Web PKI policy

CA/Browser Forum TLS Baseline Requirements govern issuance of publicly trusted TLS server certificates and require validation of domain/IP control according to defined methods.

As of Baseline Requirements v2.3.0 (7 September 2026), publicly trusted subscriber certificates issued between **15 March 2026 and 15 March 2027** have a maximum validity period of **200 days**. The already-adopted schedule reduces this to 100 days from 15 March 2027 and 47 days from 15 March 2029.

## SOURCE — RFC 9525

RFC 9525 (2023) is the current IETF service-identity verification specification and obsoletes RFC 6125.

For DNS names, it directs clients to verify the appropriate `subjectAltName` DNS identifier. Strings in the certificate subject Common Name are no longer a valid substitute for service identity under this specification.

Wildcard matching is constrained so the wildcard occupies the complete left-most label.

## SYNTHESIS

CA issuance asks, roughly: **was the applicant authorized to obtain a certificate for this name?**

Client identity verification asks: **does the service I intended to reach match an acceptable identifier in the certificate I was presented?**

These are related phases but not the same check.

---

# 8. SAN and hostname verification

## FOUNDATION

Suppose a client intends to connect to `minttap.app`.

A certificate for `other.example` can be perfectly well signed by a trusted CA and still be wrong for `minttap.app`.

The client must compare its reference service identity to identities presented in the certificate under the applicable verification rules.

## SOURCE — RFC 9525

Current IETF guidance:
- service identity should be represented in `subjectAltName`;
- Common Name matching is obsolete for this purpose;
- DNS wildcard use is constrained;
- DNS/IP identifiers are type-specific and must be matched accordingly.

## Diagnostic category

A hostname mismatch is not primarily:
- DNS failure;
- HTTP 404;
- expired-certificate failure;
- “encryption failed.”

It is an **authenticated service identity mismatch**.

---

# 9. SNI — why the TLS client tells the server which name it wants

## SOURCE — RFC 6066, updated by current TLS work

Server Name Indication (`server_name`) allows the client to include the desired server name in ClientHello. This addresses hosting environments where multiple virtual services/certificates share one underlying network address.

## FOUNDATION

DNS can resolve many names to the same edge/server IP. Before HTTP is exchanged, the TLS endpoint may need to know which certificate/configuration to use.

SNI supplies that routing/certificate-selection clue during the TLS handshake.

## Important boundary

`Host` / `:authority` in HTTP and SNI in TLS are at different protocol layers. They frequently refer to related host identity, but they are not interchangeable fields.

A mismatch between TLS routing/certificate selection and later HTTP routing can produce failures that look confusing unless the layers are separated.

## Privacy boundary

TLS protects application traffic, but TLS does not automatically hide every piece of connection metadata. Classic SNI is one example of handshake metadata that historically exposed destination naming information. Later privacy mechanisms such as ECH are a separate advanced topic.

---

# 10. ALPN — selecting HTTP/1.1 vs HTTP/2 inside TLS

## SOURCE — RFC 7301

ALPN allows a TLS client to advertise supported application-layer protocols in ClientHello and the server to select one during the handshake without an additional round trip.

It was motivated in part by HTTP/2 deployment.

## FOUNDATION

For HTTPS over TCP, one TLS endpoint can support multiple application protocols. ALPN can negotiate, for example, whether the protected connection will carry `http/1.1` or `h2`.

HTTP/3 uses QUIC/TLS integration rather than simply being “HTTP/2 over the same TCP TLS connection,” but protocol negotiation remains conceptually connected.

## Web Manager implication

When browser DevTools reports HTTP/2 or HTTP/3, protocol selection is connected to TLS/transport negotiation. Do not treat HTTP version and TLS as unrelated configuration islands.

---

# 11. HSTS — solving the insecure bootstrap/downgrade problem

## SOURCE — RFC 6797

HTTP Strict Transport Security allows a host to tell a user agent that interactions should occur only via secure transport. A conformant user agent can rewrite insecure HTTP references to HTTPS before dereferencing and treats secure transport errors as fatal for an HSTS host.

## Problem

If a user first enters or follows `http://example.com`, a server-side 301 redirect to HTTPS occurs **after** an insecure HTTP request has already been attempted. An active network attacker could interfere before the redirect is received.

HSTS reduces this bootstrap downgrade opportunity after policy is known.

## HSTS preload

Browsers can ship a preloaded HSTS policy rather than waiting for a site's first secure response. Preload behavior is browser implementation/ecosystem policy rather than a mechanism fully defined by RFC 6797 itself.

---

# 12. MintTap-specific fact: `.app` is HSTS preloaded at the TLD level

## SOURCE — Google Registry

Google Registry states that the `.app` top-level domain is included in the HSTS preload list and that HTTPS is required for `.app` websites, without each registrant needing an individual preload registration.

## MINTTAP CONSEQUENCE

`minttap.app` is not a domain where plaintext HTTP can be treated as a usable fallback strategy in normal preload-aware browsers.

HTTPS readiness is therefore a **domain prerequisite**, not an optional post-launch hardening step.

Before a future deployment is exposed to users, certificate issuance, TLS termination, host routing and renewal must already work.

## Important distinction

The `.app` preload property does **not** mean:
- Google supplies MintTap's certificate automatically;
- TLS configuration cannot fail;
- the origin is automatically protected behind a CDN;
- every browser's trust store is identical;
- HSTS replaces certificate validation.

It means preload-aware user agents know that `.app` should use HTTPS before receiving an HSTS header from that specific host.

---

# 13. Certificate lifetime is now an automation issue, not an annual calendar reminder

## SOURCE — CA/Browser Forum TLS BR v2.3.0, 7 Sep 2026

Maximum public subscriber certificate validity:

- before 15 Mar 2026: maximum 398 days;
- 15 Mar 2026 → before 15 Mar 2027: maximum **200 days**;
- 15 Mar 2027 → before 15 Mar 2029: maximum **100 days**;
- 15 Mar 2029 onward: maximum **47 days**.

Domain/IP validation reuse periods are also being reduced, eventually reaching 10 days in 2029.

## SYNTHESIS

The industry direction makes manual certificate lifecycle operation increasingly inappropriate.

The strategic response is not “set more calendar reminders.” It is to design for automated issuance, renewal, deployment and failure monitoring.

This is especially relevant to an app company whose website must remain available for store review, privacy/support URLs, account-deletion surfaces and user trust.

## CHANGE WATCH

The CA/Browser Forum Baseline Requirements and individual browser root-program policies are living policy. Re-check them at implementation time.

---

# 14. Browser trust is broader than PKIX path validation

## SOURCE — Chrome / Mozilla

Chrome Root Program Policy 1.8 (5 Feb 2026) states that Chrome verifies website certificates against its recognized root-store policy and performs additional evaluations of HTTPS security properties.

Mozilla Root Store Policy 3.1, effective 1 Jul 2026, similarly governs which CAs/root certificates Firefox trusts and requires conformance with CA/Browser Forum requirements plus Mozilla-specific requirements.

## SOURCE — Certificate Transparency

Chrome's CT policy requires publicly trusted website certificates to satisfy Certificate Transparency rules in Chrome except in defined circumstances. Apple also maintains a CT policy for publicly trusted TLS server certificates on Apple platforms.

## SYNTHESIS

A certificate can be structurally valid under basic X.509 processing but still not be accepted by a browser because modern Web PKI trust combines:

`PKIX path validation + service identity verification + browser root policy + CT/policy constraints + TLS protocol checks`

This explains why “OpenSSL says the chain validates” and “Safari/Chrome trusts the website” are not always equivalent statements.

---

# 15. Expiration, clock, chain and trust failures

A Web Manager should keep these failure classes distinct.

## A. Expired / not-yet-valid certificate
Certificate validity interval and the client's notion of time do not agree.

Potential evidence:
- `notBefore` / `notAfter` values;
- client/server time context;
- browser certificate details.

## B. Hostname mismatch
The intended service identity does not match a valid presented identifier.

Potential evidence:
- requested hostname;
- SAN entries;
- wildcard rule applicability.

## C. Missing/wrong intermediate chain
The client cannot construct an acceptable path to a trust anchor even though the leaf itself looks plausible.

Potential evidence:
- served chain;
- intermediate issuer relationships;
- target client differences.

## D. Untrusted root / policy distrust
The path terminates at a CA/trust configuration not accepted by that client or the hierarchy is constrained/distrusted by product policy.

## E. TLS protocol negotiation failure
No acceptable/common protocol/version/parameter set exists, or the handshake fails before HTTP begins.

## F. SNI/routing mismatch
The edge chooses the wrong virtual host/certificate because server-name routing is missing or misconfigured.

## G. CT/root-program policy failure
The chain may be cryptographically plausible but fail browser Web PKI policy.

## H. Local interception / enterprise root behavior
A device may trust a locally installed interception CA, producing a different chain from what another client observes.

This is why one successful browser does not prove universal trust compatibility.

---

# 16. Revocation: necessary concept, imperfect operational mechanism

## SOURCE

RFC 5280 defines CRLs as a mechanism for communicating revoked certificates and identifies timeliness/granularity limitations inherent in periodically issued lists.

Modern browser/root-program policy has continued to evolve revocation requirements. Chrome's 2026 program material explicitly notes privacy, performance and timeliness challenges with status mechanisms such as CRLs/OCSP and connects shorter certificate lifetimes with reducing reliance on them.

## FOUNDATION

Expiration and revocation solve different problems:

- **expiration** says a certificate is no longer valid after a scheduled time;
- **revocation** is intended to invalidate a certificate before its scheduled expiry, for example after key compromise or mis-issuance.

## SYNTHESIS

Do not build an operational model that assumes a compromised public certificate will instantly disappear from every client's trust decision everywhere.

Short-lived certificates, automation, browser-specific status mechanisms and CA incident response all contribute to modern Web PKI risk reduction.

---

# 17. TLS termination: browser-facing TLS is not necessarily origin-facing TLS

## FOUNDATION / SYNTHESIS

A common CDN architecture is:

`browser ==TLS A==> CDN/edge ==TLS B (or other protected/private hop)==> origin`

TLS A and TLS B are **different connections with different peers, keys and certificates/policies**.

If an edge terminates public HTTPS, the browser authenticates the edge-facing service configuration. The edge then separately communicates with the origin according to the provider's origin policy.

## Operational consequence

A browser can show a completely valid HTTPS connection while edge → origin TLS is separately misconfigured, downgraded, privately trusted or failing.

Conversely, a perfectly configured origin certificate does not matter to users if the public edge is presenting the wrong certificate.

## MintTap validation question for a real project

Verify independently:

1. browser → public edge TLS;
2. public edge → origin transport/TLS;
3. certificate/hostname policy on each TLS hop;
4. renewal ownership for each certificate involved.

Do not call this “end-to-end encryption” without defining the actual endpoints.

---

# 18. HTTPS does not guarantee the website is trustworthy or safe

TLS can authenticate that the client established a protected connection to a service identity under the applicable trust model. It does not prove:

- the company is honest;
- page content is factually correct;
- the application has no XSS/injection/business-logic flaws;
- the server itself is uncompromised;
- third-party JavaScript is safe;
- analytics/privacy practices are appropriate;
- downloaded software is benign;
- the domain is not a phishing domain with its own valid certificate.

## Web Manager rule

Do not use the padlock/HTTPS state as a generalized “trustworthiness” claim in website content or internal security reasoning.

HTTPS is a secure-channel property, not a moral or application-security certification.

---

# 19. What TLS does not hide

TLS protects application content within its security model, but it does not make a connection invisible.

Depending on network/protocol features, observers can still learn or infer some metadata such as:

- destination IP address;
- timing;
- traffic volume/length patterns;
- some handshake metadata;
- DNS queries when DNS itself is not separately protected;
- classic SNI hostname information when ECH is not used.

RFC 9846 explicitly notes that TLS confidentiality does not inherently hide transmitted data length.

## Boundary

ECH, encrypted DNS and traffic-analysis resistance are important but belong to later security/privacy study. They are not prerequisites for Stage 1 TLS competence.

---

# 20. TLS connection establishment — Web Manager mental model

A simplified TLS 1.3 mental model:

1. client opens/reuses an appropriate network transport path;
2. client sends ClientHello with supported TLS capabilities and extensions such as SNI/ALPN;
3. server selects compatible parameters and sends ServerHello;
4. shared handshake secrets/keys are derived;
5. server sends encrypted handshake material including certificate/authentication proof under the TLS 1.3 flow;
6. client validates certificate/path/service identity and handshake proof according to its policy;
7. peers prove handshake integrity/completion;
8. derived application traffic keys protect higher-layer application data;
9. HTTP then operates within the secure channel (or HTTP/3 integrates TLS 1.3 with QUIC's connection model).

This intentionally omits cryptographic implementation detail while preserving diagnostic boundaries.

---

# 21. 0-RTT is a performance/security trade-off, not “free faster TLS”

## SOURCE — RFC 9846

TLS 1.3 can send 0-RTT early data in resumption scenarios, but early data has weaker security properties, especially replay considerations, than normal post-handshake application data.

## CROSS-DOMAIN CONNECTION

HTTP method semantics from Study 029 now matter directly.

Potentially replayable early data must not be treated as universally safe for state-changing operations merely because TLS accepted it.

This is an example of why HTTP semantics and TLS cannot be studied as isolated layers.

Stage 7/8 will revisit concrete deployment policy.

---

# 22. Certificate Transparency as Web PKI accountability

## FOUNDATION

Certificate Transparency (CT) provides publicly auditable logging mechanisms around certificate issuance. Browser policies can require evidence that a publicly trusted certificate has been logged appropriately.

## SOURCE

Chrome's current CT policy evaluates website certificates for CT compliance. Apple's policy likewise requires qualifying publicly trusted TLS server certificates to satisfy Apple's CT policy.

## SYNTHESIS

A CA signature answers “a trusted issuer signed this certificate.” CT adds an ecosystem accountability mechanism intended to make issuance observable rather than silently relying only on issuer secrecy/behavior.

CT does not replace domain validation, certificate signatures or browser trust stores.

---

# 23. Current Web PKI direction — automation and agility

Three current trends are operationally important:

1. **shorter public certificate lifetimes** — already 200 days as of September 2026 under CA/B BRs;
2. **stronger automated issuance/renewal expectations** in browser root programs;
3. **reduction of legacy/multi-purpose trust infrastructure** in modern browser root-store programs.

Chrome Root Program 1.8 and Mozilla Root Store Policy 3.1 both contain active 2026 changes aimed at reducing root/PKI attack surface and increasing automation/agility.

## Web Manager implication

Certificate management is no longer a setup task completed once at domain launch. It is a continuous operational dependency comparable to DNS and deployment health.

A mature launch plan must assign ownership for:
- automated issuance;
- renewal;
- deployment/reload;
- expiry/failure monitoring;
- emergency replacement/revocation response;
- edge/origin certificate separation;
- policy change watch.

---

# 24. Failure diagnosis model

When `https://minttap.app` fails, avoid the sentence “SSL is broken.”

Use a layered evidence path:

1. **URL / origin intent** — what host/scheme is the client trying to reach?
2. **DNS** — did the intended name resolve?
3. **network/transport** — is the endpoint reachable?
4. **TLS ClientHello routing** — SNI/transport reaches the intended virtual service?
5. **version/parameter negotiation** — common acceptable TLS setup?
6. **certificate presentation** — what leaf/intermediates were actually served?
7. **time validity** — notBefore/notAfter/client clock?
8. **path building** — acceptable chain to target client's trust anchor?
9. **service identity** — SAN matches the reference hostname?
10. **browser policy** — CT/root-program/security policy accepted?
11. **ALPN/application protocol** — what HTTP protocol was selected?
12. **HTTP** — only now inspect redirect/status/header/application behavior.
13. **edge → origin** — if a CDN/proxy is involved, separately diagnose that hop.

This preserves layer discipline from Studies 027–029.

---

# 25. Representative diagnostic cases

## Case A — DNS works, browser says certificate name is wrong
Do not change DNS first merely because the hostname is involved.

Primary layer: certificate service-identity/SNI/virtual-host configuration.

## Case B — one old device fails, current browsers work
Possible categories include trust-store/root compatibility, chain construction, TLS-version/cipher compatibility or clock problems. Compare evidence before changing production configuration.

## Case C — CDN page shows valid HTTPS but origin health check fails TLS
Treat browser→edge and edge→origin as separate TLS connections.

## Case D — browser redirects `http://minttap.app` before a visible HTTP response
For `.app`, HSTS preload is an expected explanation; do not assume the origin emitted the redirect.

## Case E — certificate renews successfully but users later see trust failure
Successful issuance does not prove successful deployment. Verify the certificate actually served at each public edge, its chain, SANs and validity.

## Case F — TLS handshake succeeds but website returns 404/500
TLS has already succeeded. Diagnose HTTP/application behavior rather than certificate issuance.

---

# 26. MintTap operating directions derived from this study

These are **MINTTAP DIRECTIONS**, not claims about the current production configuration.

1. Treat HTTPS as mandatory from the first deploy because `.app` is HSTS preloaded.
2. Prefer automated publicly trusted certificate issuance/renewal; manual renewal should not be the long-term operating model.
3. Validate both `minttap.app` and any intended subdomains explicitly in certificate/routing design.
4. If using a CDN/edge, document browser→edge and edge→origin TLS as separate security boundaries.
5. Monitor certificate expiry/renewal/deployment, not merely CA issuance success.
6. Record who owns DNS, certificate issuance, edge TLS, origin TLS and emergency replacement.
7. Test target browsers/platforms rather than assuming one trust store proves universal compatibility.
8. Never market HTTPS/padlock as proof that the company or application is generally “safe.”
9. At implementation time, re-check CA/B BRs and Chrome/Mozilla/Apple trust requirements because these are living policies.
10. Treat SNI/ALPN/TLS evidence as part of network diagnosis before blaming HTTP/application code.

---

# 27. Common misconceptions corrected

1. **HTTPS means the server's files are encrypted at rest.** False; HTTPS concerns transport security.
2. **A certificate itself encrypts all traffic.** False; TLS derives traffic keys and uses symmetric record protection.
3. **A trusted CA signature means the certificate is valid for any hostname.** False; service identity must match.
4. **Common Name is the modern hostname-verification field.** Outdated; RFC 9525 uses subjectAltName identifiers and rejects CN-ID as service identity.
5. **A root CA must be sent by the server.** Trust anchors are normally already configured locally; sending one does not create trust.
6. **TLS 1.3's current RFC is 8446.** Outdated as of July 2026; RFC 9846 obsoletes it.
7. **Public certificates still last about one year.** Outdated for newly issued certificates in the current period; CA/B BR maximum is 200 days from 15 Mar 2026 to 15 Mar 2027.
8. **HSTS is just an HTTPS redirect.** False; the user agent applies a transport policy before insecure dereferencing.
9. **`.app` means MintTap does not need TLS configuration.** False; preload forces secure use but does not issue/configure certificates.
10. **Valid HTTPS means the site is benign.** False; phishing and vulnerable apps can have valid HTTPS.
11. **CDN HTTPS means the same TLS session reaches the origin.** Usually false in terminating proxy architectures.
12. **If TLS works, HTTP must work.** False; TLS only establishes/protects the channel used by the application protocol.

---

# 28. Integrated competency checkpoint

Stage 1 TLS core is considered passed only if the Web Manager can explain and apply all of the following:

1. confidentiality vs integrity vs authentication;
2. why encrypted-but-unauthenticated communication is insufficient;
3. SSL → TLS evolution and why TLS 1.3 simplified the protocol;
4. current RFC 9846 status vs historical RFC 8446;
5. handshake vs record protocol roles;
6. asymmetric authentication/key establishment vs symmetric traffic protection;
7. certificate, public key and private key roles;
8. root/intermediate/leaf and certification-path reasoning;
9. trust anchor as relying-party policy rather than a universal Internet constant;
10. SAN/service-identity verification and why CN matching is obsolete;
11. SNI purpose and its layer difference from HTTP Host/:authority;
12. ALPN purpose and relationship to HTTP protocol selection;
13. HSTS vs HTTP redirect and why preload changes the first-contact model;
14. `.app` HSTS-preload consequences for MintTap;
15. expiry vs revocation and their operational differences;
16. browser/root-program/CT policy as additional Web PKI trust layers;
17. CDN edge TLS vs origin TLS as separate connections/security boundaries;
18. why certificate automation is increasingly mandatory operationally;
19. representative browser TLS failure diagnosis before HTTP begins;
20. what HTTPS does not prove or conceal.

Assessment: **PASS for Stage 1 progression.**

The domain remains open for advanced Stage 8/11 study.

---

# 29. Design Studio relationship / handoff

## DEPENDENCY CHECK

The current study is network security/platform foundation, not visual-design research. No Design Studio artifact needs modification.

Relevant future overlap with Web Design exists in:
- browser security/error states;
- user trust communication without deceptive “secure” claims;
- performance/loading implications of connection establishment;
- designing graceful operational error/support surfaces.

The latest Design Studio Web specialist is still at its own Foundation baseline and expects browser/performance/accessibility constraints to be integrated later. No immediate handoff is required.

## HANDOFF TRIGGER

Reconnect with Design Studio during Stage 3/4/7 when TLS/network failures or loading behavior become visible UX/state-design problems.

---

# 30. OPEN / VALIDATION / CHANGE WATCH

## OPEN — actual MintTap production facts not inferred here

Unknown until checked in a live project:
- current registrar/DNS/CDN/hosting topology;
- current certificate issuer and chain;
- actual SAN inventory;
- current TLS versions/ALPN results;
- whether a CDN terminates TLS;
- edge→origin encryption/trust mode;
- renewal mechanism and ownership;
- certificate/CT monitoring;
- redirect/HSTS headers at the application level;
- subdomain inventory.

## VALIDATION — future project launch

Validate with real browser/network evidence:
- public certificate chain;
- hostname/SAN match;
- expiry and renewal behavior;
- target Apple/Android/browser trust;
- SNI virtual-host selection;
- ALPN/HTTP protocol negotiation;
- HSTS/preload behavior;
- CDN edge and origin hop separately;
- failure alerts/monitoring.

## CHANGE WATCH

Re-check before production decisions:
- current TLS RFC status and errata;
- CA/Browser Forum TLS Baseline Requirements;
- Chrome Root Program;
- Mozilla Root Store Policy;
- Apple trust / Certificate Transparency policy;
- certificate lifetime and validation-reuse schedule;
- CT requirements;
- browser support/deprecation behavior.

---

# Sources

## Current primary standards

- IETF RFC 9846 — The Transport Layer Security (TLS) Protocol Version 1.3, July 2026: https://www.rfc-editor.org/rfc/rfc9846.html
- IETF RFC 9525 — Service Identity in TLS, November 2023: https://www.rfc-editor.org/rfc/rfc9525.html
- IETF RFC 5280 — Internet X.509 PKI Certificate and CRL Profile: https://www.rfc-editor.org/rfc/rfc5280.html
- IETF RFC 6066 — TLS Extensions / Server Name Indication: https://www.rfc-editor.org/rfc/rfc6066.html
- IETF RFC 7301 — TLS Application-Layer Protocol Negotiation: https://www.rfc-editor.org/rfc/rfc7301.html
- IETF RFC 6797 — HTTP Strict Transport Security: https://www.rfc-editor.org/rfc/rfc6797.html
- IETF RFC 8996 — Deprecating TLS 1.0 and TLS 1.1: https://www.rfc-editor.org/rfc/rfc8996.html

## Historical primary references

- IETF RFC 6101 — SSL 3.0 historical record: https://www.rfc-editor.org/rfc/rfc6101.html
- IETF RFC 2246 — TLS 1.0 historical standard: https://www.rfc-editor.org/rfc/rfc2246.html
- IETF RFC 8446 — original TLS 1.3 standard, now obsoleted by RFC 9846: https://www.rfc-editor.org/rfc/rfc8446.html

## Current public Web PKI / browser policy

- CA/Browser Forum — TLS Baseline Requirements v2.3.0, 7 Sep 2026: https://cabforum.org/working-groups/server/baseline-requirements/requirements/
- Chrome Root Program Policy v1.8, updated 5 Feb 2026: https://www.chromium.org/Home/chromium-security/root-ca-policy/
- Chrome Certificate Transparency Policy: https://googlechrome.github.io/CertificateTransparency/ct_policy.html
- Mozilla Root Store Policy v3.1, effective 1 Jul 2026: https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/
- Apple Certificate Transparency policy: https://support.apple.com/103214
- Google Registry `.app`: https://www.registry.google/domains/app/

---

# Evidence classification

- **SOURCE:** TLS properties/current protocol from RFC 9846; path validation from RFC 5280; service identity from RFC 9525; SNI/ALPN/HSTS from their IETF RFCs; public-cert policy from current CA/B and browser/root-program documents; `.app` preload from Google Registry.
- **SYNTHESIS:** layered diagnosis model; certificate ≠ trust mental model; edge/origin TLS separation; automation-as-operating-model conclusion; cross-layer HTTP/TLS reasoning.
- **MINTTAP DIRECTION:** HTTPS-ready first deployment; automated certificate lifecycle; explicit edge/origin ownership; separate-hop validation; trust claims kept narrow and evidence-based.
- **OPEN:** actual `minttap.app` live certificate, topology and renewal configuration.
- **DEPENDENCY:** no immediate Design Studio work; future browser security/error-state and loading UX overlap.
- **VALIDATION:** real target-browser/edge/origin TLS evidence required before production confidence.
- **CHANGE WATCH:** RFC, CA/B, Chrome, Mozilla, Apple and CT policy changes.