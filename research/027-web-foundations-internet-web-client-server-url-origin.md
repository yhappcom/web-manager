# 027 — Web Foundations: Internet, Web, Client–Server, URL & Origin

Status: **FOUNDATION COMPLETE**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Why this study exists

A Web Manager should not begin with hosting vendors, frameworks or page templates. Those are implementations built on a more durable model: the Internet transports data; the Web is one service built on that infrastructure; browsers and servers communicate about identified resources; URLs identify targets; and an origin defines a fundamental authority/security boundary.

This study deliberately rebuilds that mental model from first principles. It does not attempt to cover DNS, HTTP message syntax or TLS mechanics in depth; those are the next Stage 1 blocks.

## 1. Internet is not the Web

### SOURCE
MDN describes the Internet as the technical infrastructure/network connecting computers, while the Web is a service built on top of that infrastructure. Other services, such as email, also use the Internet.

### FOUNDATION
**Internet**: the interconnected networking infrastructure that lets computers exchange data.

**World Wide Web**: a distributed information/application system that uses web technologies such as URLs, HTTP(S), HTML and browsers over that network infrastructure.

Therefore:

`Internet ⊃ Web`

The Web depends on Internet/networking infrastructure, but the Internet is not synonymous with the Web.

### Common misconception
"The website is down, therefore the Internet is down" is invalid reasoning. A user may have working Internet connectivity while DNS, a particular origin, CDN, application or resource fails.

### Web Manager implication
Incident diagnosis must name the failed layer. "Website unavailable" is a symptom, not a root cause.

## 2. Client and server are roles

### SOURCE
RFC 9110 defines an HTTP client as a program that establishes a connection for sending HTTP requests and a server as a program that accepts connections to service requests with responses. It explicitly notes that client/server are roles for a particular connection; the same program can act as a client in one context and server in another.

### FOUNDATION
A browser is commonly the **client** for a website request. The program serving the requested representation is acting as the **server**.

Simplified interaction:

`user action → client request → server processing → server response → client interpretation`

But "client = user's device" and "server = one physical computer" are simplifications, not definitions. Modern delivery can involve DNS infrastructure, proxies, CDNs, load balancers, edge services and multiple application systems.

### Important distinction
A browser is not merely a file viewer. It is a user agent that performs navigation, networking, security checks, document parsing, rendering, script execution, storage and interaction behavior.

## 3. Resource, representation and location are different ideas

### SOURCE
HTTP semantics operate on target resources through representations. RFC 9110 emphasizes that HTTP presents a uniform interface independent of how the service/resource is implemented.

### FOUNDATION
A **resource** is the thing conceptually identified by a URL in the Web/HTTP namespace. A response body is a **representation** of resource state, not necessarily "the resource itself" or a literal disk file.

For example:

`https://minttap.app/en/apps/example/`

might be handled by:
- a static HTML file;
- a server-side renderer;
- an edge function;
- a framework route backed by a database;
- a cached representation generated earlier.

The public URL does not reveal or require one of those implementations.

### Web Manager implication
Public URL architecture should be designed around durable user/resource meaning, not around current server directory names or framework internals.

## 4. URL as the Web-facing identifier/address model

### SOURCE
The WHATWG URL Standard is the contemporary browser-oriented Living Standard for URL parsing and interoperable URL behavior. It explicitly standardizes on the term URL for contemporary implementations. RFC 9110 defines the `http` and `https` URI schemes used by HTTP.

### FOUNDATION
For ordinary Web Manager work, **URL** is the practical primary term.

Example:

`https://minttap.app:443/en/apps/example/?ref=home#features`

Conceptually it contains:
- scheme: `https`
- host: `minttap.app`
- port: `443` (normally omitted because it is the HTTPS default)
- path: `/en/apps/example/`
- query: `?ref=home`
- fragment: `#features`

The components do different jobs. The host participates in identifying the network authority/origin. The path identifies a target within that origin's namespace. Query data can further parameterize the target/request semantics. A fragment identifies a secondary reference within the resulting resource/representation and is not part of the HTTP request target sent to the origin server.

### URL is not proof of availability
RFC 9110 explicitly notes that the presence of an HTTP(S) URI does not imply a server currently exists or maps it to a resource.

Therefore a syntactically valid URL can still fail to resolve, connect, authenticate or return a useful resource.

## 5. Host, domain and origin must not be conflated

### FOUNDATION
**Host** is the host identifier in a URL authority, commonly a domain name such as `minttap.app`.

**Domain name** is part of the DNS naming system; DNS mechanics are Study 028.

**Origin** is a web authority/security concept. For HTTP(S), RFC 9110 defines the origin from the tuple:

`scheme + host + port`

Example normalized origin:

`https://minttap.app:443`

The browser-facing serialization normally omits the default `:443`.

These are different origins:
- `http://minttap.app`
- `https://minttap.app`
- `https://www.minttap.app`
- `https://minttap.app:8443`

Even if one organization controls all of them, differing scheme, host or port makes them distinct origins unless a separate mechanism deliberately connects behavior between them.

## 6. Why origin matters

### SOURCE
MDN describes the same-origin policy as a critical browser security mechanism restricting interaction between documents/scripts from different origins. It prevents one malicious origin from freely reading protected information belonging to another origin.

### FOUNDATION
Origin is not just a URL-format detail. It is one of the Web's principal security boundaries.

This affects later Web Manager topics including:
- cross-origin API requests/CORS;
- cookies and storage scope;
- embedded resources;
- authentication;
- content security;
- subdomain architecture;
- app/web integrations.

### Common misconception
"Both URLs belong to MintTap, so the browser treats them as the same site/origin" is not a safe assumption. Organizational ownership and browser origin identity are different concepts.

## 7. What happens when a user enters `https://minttap.app/` — first-pass model

At this stage, the correct simplified mental model is:

1. The user gives the browser a URL/navigation intent.
2. The browser parses the URL and determines the scheme, host, target path and origin.
3. The host must ultimately be resolved to reachable network infrastructure. DNS details follow in Study 028.
4. For HTTPS, a secure connection/authority relationship must be established. TLS details follow in Study 030.
5. The client sends an HTTP request for the target resource. HTTP mechanics follow in Study 029.
6. The serving system returns an HTTP response/representation or a redirect/error.
7. The browser interprets received HTML/CSS/JavaScript and related resources. Rendering/runtime details follow in Studies 031–032.
8. The user sees and interacts with the resulting document/application under browser security and interaction rules.

This sequence is intentionally incomplete but correctly separates the major layers.

## 8. Durable mental model vs implementation fashion

### SYNTHESIS
The following concepts are durable enough to learn before frameworks/providers:
- network infrastructure is not the Web itself;
- clients request and servers respond under protocol semantics;
- URLs identify Web targets;
- public resource identity is separate from backend implementation;
- origin is based on scheme/host/port and is security-significant;
- a browser performs substantially more work than simply displaying server files.

React, Next.js, Flutter Web, Firebase Hosting, Cloudflare, Vercel and similar technologies should later be understood as implementations within this model, not as definitions of the Web.

## 9. MintTap application

For `minttap.app`, Web Manager decisions should therefore preserve these distinctions:

- `minttap.app` as a domain/host is not the entire website architecture;
- `/ko/`, `/en/`, `/apps/...` are public resource namespaces, not required disk folders;
- changing hosting provider should not automatically require changing meaningful public URLs;
- adding a subdomain creates DNS, navigation and potentially origin/security consequences;
- HTTP and HTTPS versions are not the same origin;
- a public URL contract should outlive a particular framework or hosting implementation where practical.

## 10. Failure-layer exercise

Symptom: `https://minttap.app/en/` does not display.

Do not immediately say "server problem." Candidate layers include:
- malformed/incorrect URL;
- DNS resolution failure;
- network routing/connectivity failure;
- TLS/certificate/authority failure;
- HTTP redirect/status/configuration failure;
- origin application failure;
- representation/content failure;
- browser rendering/script failure.

A Web Manager's first diagnostic skill is **layer separation**.

## 11. Knowledge check

A Stage-1 learner should now be able to answer:

1. Why are Internet and Web not synonyms?
2. Why are client/server better understood as roles than physical machine categories?
3. Why can a URL remain stable while the backend implementation changes completely?
4. Break `https://minttap.app/en/apps/x/?from=home#pricing` into its major components.
5. Are `http://minttap.app` and `https://minttap.app` the same origin? Why not?
6. Are `https://minttap.app` and `https://www.minttap.app` the same origin? Why not?
7. Why is origin important beyond URL formatting?
8. Why is "the server is broken" an inadequate first diagnosis for a page that will not load?

## 12. Boundaries / next studies

Not yet treated in sufficient depth:
- how DNS actually resolves a domain;
- IP addresses and DNS record hierarchy;
- HTTP request/response message structure;
- methods/status/headers/caching;
- TCP vs QUIC/HTTP versions;
- TLS handshake/certificate trust;
- browser document parsing/rendering/runtime;
- DOM/accessibility tree;
- browser storage.

These are intentionally deferred so the foundation remains layered rather than becoming one giant glossary.

## Sources

Primary/authoritative:
- IETF RFC 9110, HTTP Semantics (Standards Track), June 2022: https://www.rfc-editor.org/rfc/rfc9110.html
- WHATWG URL Living Standard, accessed 2026-09-14: https://url.spec.whatwg.org/

High-quality instructional/reference:
- MDN, How the web works, accessed 2026-09-14: https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works
- MDN, How does the Internet work?, accessed 2026-09-14: https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/How_does_the_Internet_work
- MDN, Same-origin policy, accessed 2026-09-14: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy
- MDN, Origin glossary, accessed 2026-09-14: https://developer.mozilla.org/en-US/docs/Glossary/Origin

## Evidence classification

- `SOURCE`: RFC/WHATWG/MDN definitions and protocol/browser behavior above.
- `SYNTHESIS`: layer-separation and durable-public-URL conclusions.
- `MINTTAP DECISION`: treat meaningful public URLs as long-lived product/web contracts rather than provider/framework implementation paths.
- `OPEN`: exact MintTap host/subdomain architecture remains project-specific.
- `DEPENDENCY`: Design Studio not required for this protocol-level foundation block.
- `VALIDATION`: no implementation test required; this block establishes standards-based concepts.
- `CHANGE WATCH`: WHATWG URL is a Living Standard; browser/security implementation details should be refreshed when operational decisions depend on them.
