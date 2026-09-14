# 028 — Web Foundations: DNS, Domain, Resolution & Hosting Path

Status: **FOUNDATION COMPLETE**
Research date: 2026-09-14
Curriculum: Stage 1 — Web Foundations

## Why this study exists

Study 027 established that a Web URL contains a host such as `minttap.app`, but it deliberately stopped before explaining how that host becomes reachable network information. This study fills that gap.

A Web Manager needs to understand DNS well enough to distinguish:
- a domain-registration problem from a DNS problem;
- a recursive-resolver problem from an authoritative-DNS problem;
- a DNS problem from an HTTP/hosting problem;
- a cached old answer from a currently published authoritative answer;
- a hostname from the server/platform that eventually serves the website.

The goal here is first-principles understanding, not provider-specific DNS configuration.

---

## 1. DNS is a distributed hierarchical naming system

### SOURCE
RFC 1034 describes DNS as a tree-structured domain name space containing resource records, served by name servers and queried through resolvers. IANA identifies the root zone as the highest level of the DNS naming hierarchy and maintains delegation data for top-level domains.

### FOUNDATION
DNS is commonly introduced as "the Internet's phone book". That analogy is useful but incomplete.

DNS is more accurately a **distributed, hierarchical database and query system for names and associated data**.

It is:
- **hierarchical** because names exist in a tree;
- **distributed** because no single ordinary server stores all authoritative DNS data;
- **delegated** because responsibility for different branches of the tree can be assigned to different authoritative zones;
- **typed** because DNS records have different meanings, not merely IP-address mappings.

### Important correction
DNS does **not** mean "a database that converts every domain name to one IP address".

A name can have:
- IPv4 address data;
- IPv6 address data;
- an alias relationship;
- authoritative name-server information;
- mail-routing information;
- verification text;
- no address record at all.

DNS is broader than host-to-IP lookup.

---

## 2. The DNS namespace is a tree

A fully conceptual view of `minttap.app` is:

```text
.                 root
└── app            top-level domain (TLD)
    └── minttap    domain beneath .app
        ├── www
        ├── support
        └── ...
```

The trailing root dot is normally omitted in everyday URLs, so users write:

`minttap.app`

rather than the fully qualified textual form:

`minttap.app.`

### SOURCE
RFC 1034 defines the domain name space as a tree. IANA's Root Zone Database records delegations for TLDs such as generic and country-code top-level domains.

### FOUNDATION
The labels in a domain name are interpreted hierarchically from right to left for delegation purposes:

`minttap.app`

means a name `minttap` under the `.app` branch of the DNS tree.

This does **not** mean a browser literally sends a web request to "the root, then .app, then MintTap". DNS resolution and HTTP fetching are separate stages. The resolver uses the DNS hierarchy to discover authoritative information; only after usable network destination information is obtained can later connection stages proceed.

---

## 3. Domain, zone and host are related but different

### Domain
A **domain** is a branch/subtree of the DNS namespace identified by a domain name.

### Zone
A **zone** is an administrative portion of the DNS namespace for which DNS data is served authoritatively.

A zone boundary exists when responsibility is delegated.

Therefore:
- every zone refers to part of the domain namespace;
- a domain and a zone are not automatically identical concepts;
- child domains can be delegated into their own zones.

### Host
A **host** in a URL is the host component used for network authority. It may be expressed as a domain name such as `minttap.app`.

### Web Manager implication
Do not use these sentences as if they mean the same thing:
- "We own the domain."
- "The DNS zone is configured."
- "The host resolves."
- "The website is serving."

Each describes a different layer/state.

---

## 4. Delegation: how responsibility is distributed

### SOURCE
RFC 1034 explains that DNS authority is divided into zones and referrals can direct a resolver toward name servers closer to the desired information. IANA's root zone contains delegation information for TLDs.

### FOUNDATION
A resolver trying to learn about `minttap.app` can conceptually follow authority downward:

```text
root zone
   ↓ referral/delegation
.app authoritative infrastructure
   ↓ referral/delegation
minttap.app authoritative name servers
   ↓ authoritative answer
requested DNS data
```

The root is not expected to know MintTap's final web-server IP address. Its primary role in this path is to provide information leading toward the authoritative infrastructure for the next delegated level.

Likewise, the `.app` TLD infrastructure need not serve MintTap's final web record directly; it can identify the authoritative name servers responsible for `minttap.app`.

### Durable principle
DNS scales because authority is **delegated**, not because one global server holds every final answer.

---

## 5. Resolver vs authoritative server

### SOURCE
RFC 9499 distinguishes DNS server roles and warns that the generic term "DNS server" can hide important differences.

An **authoritative server** knows data for zones from local authoritative knowledge and can answer for those zones without querying another server for that data.

A **recursive resolver** receives a query from a client and works to obtain the final answer, often answering from cache when possible or querying other DNS servers when necessary.

### FOUNDATION
These roles should be mentally separated:

```text
browser / OS
    ↓ asks for name information
stub/local resolver layer
    ↓
recursive resolver
    ↓ iterative discovery when cache insufficient
root / TLD / authoritative DNS
```

The user's device generally does not need to understand and query the entire DNS hierarchy itself for every page load. A recursive resolver commonly performs the resolution work on its behalf.

### Common misconception
"The DNS server" is too vague for incident analysis.

Ask instead:
- Which resolver did the client query?
- Was the answer cached?
- Which servers are authoritative for the zone?
- What is the authoritative answer now?

---

## 6. Recursive and iterative behavior are different

### SOURCE
RFC 9499 defines recursive mode as a server receiving a query and either answering from cache or pursuing the information needed to return the final answer/error. It distinguishes this from iterative resolution, where referrals lead the resolver toward another server.

### FOUNDATION
A simplified resolution sequence is:

1. A client asks a recursive resolver for information about `minttap.app`.
2. If a valid cached answer exists, the resolver may return it immediately.
3. If not, the resolver can begin or continue resolution using authoritative DNS information.
4. It can consult root authority and receive a referral toward `.app`.
5. It can query the relevant `.app` authority and receive a referral toward `minttap.app`'s authoritative name servers.
6. It queries an authoritative server for the requested record type.
7. It returns the resulting answer to the client and may cache it according to DNS caching rules.

This is a conceptual path. Real implementations can optimize, pre-cache, parallelize or otherwise avoid repeating every step.

---

## 7. Root hints bootstrap recursive resolution

### SOURCE
IANA states that recursive-resolver operators typically configure a root hints file containing names and IP addresses of authoritative root name servers. RFC 9499 uses this as the basis for the root-hints concept.

### FOUNDATION
A resolver faces a bootstrap question:

> If DNS is needed to find name servers, how does the resolver initially know where the DNS hierarchy starts?

One answer is **root hints**: preconfigured information that lets the resolver begin with the root-server system.

This is conceptually important because DNS cannot depend on an endless circular DNS lookup to discover its own first starting point.

---

## 8. Resource records: DNS stores typed data

DNS answers are expressed through **resource records (RRs)**.

### A record
RFC 1035 defines type `A` as a host address record in the original IPv4-oriented DNS model.

Practical meaning: maps a DNS owner name to an IPv4 address.

### AAAA record
RFC 3596 defines `AAAA` to store one IPv6 address.

Practical meaning: maps a DNS owner name to an IPv6 address.

### NS record
RFC 1035 defines `NS` as identifying an authoritative name server for the relevant domain/zone context.

### CNAME record
RFC 1035 defines `CNAME` as the canonical-name relationship for an alias.

Conceptually:

```text
alias.example → canonical-target.example
```

It is not simply "another A record".

### MX record
Identifies mail-exchange routing information. It demonstrates why DNS cannot be reduced to web-host IP lookup.

### TXT record
Carries text-string data and is widely used by higher-level systems for policy/verification purposes.

### SOA record
Marks the start of a zone of authority and contains zone-management metadata.

### Web Manager implication
Before changing DNS, always ask:
- What record type is being changed?
- What exact owner name does it apply to?
- What system depends on it?
- Is the record part of web delivery, email, verification, delegation or another service?

Changing a DNS zone casually can affect services unrelated to the website.

---

## 9. A/AAAA records do not prove "the origin server" identity

### SYNTHESIS
Suppose `minttap.app` resolves to one or more IP addresses.

That does not prove:
- the IP belongs to one dedicated physical server;
- that machine stores the final HTML file;
- there is no CDN/proxy/load balancer in front;
- the same address always serves every user;
- the backend topology can be inferred from the public DNS answer.

The IP information tells the client where networking can continue. Modern serving architecture can still contain multiple layers behind or around that destination.

This preserves the distinction from Study 027:

`public name / addressability ≠ backend implementation topology`

---

## 10. DNS caching and TTL

### SOURCE
RFC 1035 defines the TTL field as the interval for which a resource record may be cached before it should be discarded / the source consulted again. RFC 9499 carries forward and clarifies current terminology around TTL and caching.

### FOUNDATION
**TTL (Time to Live)** is not "the exact time until the Internet updates".

It is a caching lifetime associated with DNS data.

If an answer was cached earlier, a resolver can continue using that cached information until its usable cache lifetime ends, subject to protocol and implementation behavior.

### Operational consequence
Changing an authoritative DNS record does not imply every client worldwide instantly starts using the new answer.

Different resolvers may:
- have no cached old answer and obtain the new one quickly;
- still have a previously cached answer;
- have cached negative information;
- observe the change at different times depending on prior query timing and cache state.

### Important misconception: "DNS propagation"
The phrase is commonly used, but it can create the wrong mental model of a new record physically spreading everywhere like a file copy.

A better model is:

**authoritative data changes + previously cached data expires at different times + resolvers query again**.

There can also be delegation/provider-specific delays, but cache expiration is central to ordinary DNS-change observations.

---

## 11. Negative caching exists

### SOURCE
RFC 9499 defines negative caching as storing knowledge that something does not exist or does not yield an answer, based on the DNS negative-caching specification.

### FOUNDATION
Resolvers may cache negative results as well as successful ones.

Therefore this sequence is possible:

1. `new.minttap.app` is queried before the DNS record exists.
2. A resolver receives a valid negative response and caches it.
3. The DNS record is then added.
4. A client using that resolver can temporarily continue seeing the previous negative state until the applicable cache behavior allows re-querying.

This is another reason "I added the record, so everybody must see it now" is not a safe assumption.

---

## 12. DNS resolution and website hosting are separate layers

A successful DNS lookup answers a naming question. It does not prove the website works.

After DNS, later stages still include:
- network path/connectivity;
- HTTPS/TLS authority and encryption;
- HTTP request/response;
- web-server/CDN/application routing;
- document/resource correctness;
- browser rendering/runtime.

Possible states:

| DNS | Later web stack | User result |
|---|---|---|
| works | works | page may load |
| fails | irrelevant/unreachable by name | page fails by hostname |
| works | TLS fails | secure page fails |
| works | HTTP returns 404/500 | DNS is not the root cause |
| works | HTML/JS broken | name resolution is still healthy |

### Web Manager diagnostic rule
`domain exists` ≠ `DNS is correct` ≠ `host is reachable` ≠ `HTTPS is valid` ≠ `website works`.

---

## 13. Registrar, registry, DNS operator and hosting provider are not the same role

### FOUNDATION
These roles are often bundled by commercial providers but should remain conceptually separate.

**Registrar**
- provides domain-registration services to registrants under the relevant registry system.

**Registry / TLD operator**
- operates registration/delegation infrastructure for a top-level domain according to its role/policies.

**Authoritative DNS provider/operator**
- serves authoritative DNS data for the domain's zone.

**Hosting / web platform provider**
- serves or helps execute the website/application after clients reach the relevant web infrastructure.

One company may provide several of these services, but the roles are different.

### MintTap implication
Migrating website hosting does not inherently require transferring domain registration. Likewise changing authoritative DNS service does not inherently mean changing the public domain name.

This separation is important for portability and incident response.

---

## 14. Nameserver delegation vs ordinary DNS records

A critical management distinction:

- changing the authoritative **nameserver delegation** determines which DNS servers are responsible for the zone;
- changing an ordinary record inside the zone modifies data served by that authority.

These have different blast radii.

A mistaken web `A`/`AAAA`/alias-related change can break a web hostname.
A mistaken zone delegation can make a much larger set of records unreachable, potentially affecting web, mail, verification and other services.

### Expert habit begun at foundation level
Always identify whether the proposed change affects:
1. registration;
2. delegation;
3. authoritative zone data;
4. web hosting/application routing.

Do not describe all four as "changing the domain".

---

## 15. What `minttap.app` resolution looks like conceptually

Without assuming MintTap's actual current DNS provider or records, the durable model is:

```text
User enters https://minttap.app/
        ↓
Browser/OS needs network information for host minttap.app
        ↓
Recursive resolver queried
        ↓
Valid cache hit?
   ├─ yes → cached DNS answer used
   └─ no  → resolver follows DNS authority/delegations
              root
                ↓
              .app authority
                ↓
              authoritative DNS for minttap.app
                ↓
              requested RR answer / alias path / error
        ↓
Resolver returns usable result to client
        ↓
Networking / TLS / HTTP stages begin
```

DNS is therefore **before** ordinary HTTPS resource exchange but is not itself the HTTPS request.

---

## 16. Failure-mode classification

### Case A — domain registration/lifecycle problem
Possible symptom: domain delegation or ownership/control state is no longer valid.

Layer: registration/registry governance.

### Case B — delegation problem
Possible symptom: parent zone directs resolvers to incorrect/unreachable authoritative name servers.

Layer: DNS delegation.

### Case C — authoritative record problem
Possible symptom: authoritative DNS responds, but the required owner/type contains wrong or missing data.

Layer: authoritative zone data.

### Case D — stale cache
Possible symptom: authoritative data is correct now, but one resolver continues returning an older cached answer.

Layer: recursive caching.

### Case E — DNS works but page fails
Possible symptom: correct address information is returned, but TLS or HTTP fails.

Layer: not DNS; continue diagnosis downstream.

### Case F — only one network/user sees failure
Do not immediately edit authoritative DNS. Compare resolver answers, cache state and network path before changing canonical configuration.

---

## 17. Common misconceptions corrected

### Misconception 1
"A domain name is just a friendly IP address."

**Correction:** DNS names can have many record types and the system is broader than address mapping.

### Misconception 2
"The root server stores the IP of every website."

**Correction:** the hierarchy relies on delegation/referral. The root zone primarily contains top-level delegation information, not every site's final record.

### Misconception 3
"DNS server" identifies one specific role.

**Correction:** authoritative servers and recursive resolvers perform different functions; RFC 9499 explicitly warns that generic naming can be ambiguous.

### Misconception 4
"TTL is how long a DNS change takes to propagate."

**Correction:** TTL governs caching lifetime of RR data. Observed change timing depends on cache history and other operational factors.

### Misconception 5
"If DNS resolves, the website is healthy."

**Correction:** TLS, HTTP, application and browser layers can still fail.

### Misconception 6
"Moving hosting means moving the domain."

**Correction:** domain registration, authoritative DNS and hosting are separable roles.

---

## 18. MintTap operating principles derived from the foundation

### SYNTHESIS / MINTTAP DECISION
For future `minttap.app` operations:

1. Treat domain registration, parent delegation, authoritative DNS and hosting as separate control layers.
2. Maintain an explicit inventory of production DNS records and what service each supports.
3. Never delete or repurpose a DNS record merely because it appears unrelated to the website without identifying its consumer.
4. Before DNS changes, record current values and TTLs and define a rollback target.
5. When migrating hosting, preserve meaningful public hostnames where possible and change resolution/routing behind them deliberately.
6. Diagnose authoritative answers separately from recursive cache observations.
7. Do not claim a DNS incident merely because a page is unavailable.
8. Subdomain decisions should be treated as both naming/IA decisions and DNS/origin/security decisions.

These are operating conclusions, not claims that MintTap's current real DNS configuration has been inspected in this study.

---

## 19. Knowledge check

A Stage-1 learner should now be able to answer:

1. Why is DNS more than a domain-to-IP address book?
2. Explain the hierarchy in `minttap.app` from root to TLD to domain.
3. What is the difference between a domain and a DNS zone?
4. What is delegation?
5. What is the difference between a recursive resolver and an authoritative server?
6. Why does a recursive resolver need a bootstrap mechanism such as root hints?
7. What do A, AAAA, NS and CNAME records conceptually represent?
8. Why does a successful A/AAAA lookup not reveal the complete hosting topology?
9. What does TTL actually control?
10. Why can two users temporarily observe different DNS answers after a change?
11. What is negative caching?
12. Why are registrar, registry, authoritative DNS and hosting separate concepts?
13. Why can changing nameserver delegation have a larger blast radius than changing one web record?
14. If DNS returns the expected address but HTTPS fails, which layer should be investigated next?

---

## 20. Stage-1 connection to surrounding studies

Study 027:
`URL contains host / origin semantics`

Study 028:
`host name → DNS resolution / delegated authority / record answer`

Study 030 later:
`resolved destination → TLS secure authority relationship`

Study 029 (next):
`HTTP request/response semantics after the connection path is available`

The curriculum order places HTTP before TLS detail for conceptual clarity, even though real HTTPS transport establishes TLS before HTTP application messages are exchanged.

---

## Sources

Primary / authoritative:
- IETF RFC 1034, *Domain Names — Concepts and Facilities*, November 1987: https://www.rfc-editor.org/rfc/rfc1034.html
- IETF RFC 1035, *Domain Names — Implementation and Specification*, November 1987: https://www.rfc-editor.org/rfc/rfc1035.html
- IETF RFC 9499, *DNS Terminology*, March 2024, current terminology reference replacing RFC 8499: https://www.rfc-editor.org/rfc/rfc9499.html
- IETF RFC 3596 / STD 88, *DNS Extensions to Support IP Version 6*: https://www.rfc-editor.org/rfc/rfc3596.html
- IANA, *Root Zone Management*: https://www.iana.org/domains/root
- IANA, *Root Zone Database*: https://www.iana.org/domains/root/db
- IANA, *Root Files / Root Hints*: https://www.iana.org/domains/root/files

Supplementary instructional context:
- ICANN, *The Domain Name System*: https://www.icann.org/resources/pages/dns-2022-09-13-en

## Evidence classification

- `SOURCE`: DNS hierarchy, zones, resolvers, authoritative servers, resource records, TTL, root zone/root hints and record-type semantics from RFC/IANA sources.
- `SYNTHESIS`: operational layer separation, "propagation" correction, failure classification and hosting-independence conclusions.
- `MINTTAP DECISION`: future MintTap DNS changes should be inventory-based, rollback-aware and distinguish registration/delegation/zone/hosting layers.
- `OPEN`: actual current `minttap.app` registrar, authoritative DNS provider, record inventory, DNSSEC state and hosting mapping are intentionally not asserted here.
- `DEPENDENCY`: none from Design Studio; this is protocol/infrastructure foundation knowledge.
- `VALIDATION`: no live DNS inspection is needed to establish these foundation concepts. Actual MintTap configuration must be separately inspected before project decisions.
- `CHANGE WATCH`: DNS core architecture is durable, but provider controls, TLD policies and actual MintTap delegation/records can change; RFC 9499 should be preferred over superseded RFC 8499 terminology.
