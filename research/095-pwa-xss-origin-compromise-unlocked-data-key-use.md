# 095 — PWA XSS/Origin Compromise Against Unlocked Data & Key-Use Authority

Status: **PASS (generic) / PRODUCT IMPLEMENTATION + TARGET-DEVICE VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: Track A same-origin/Web Crypto/Service Worker mechanics; Track B truthful locked/unlocked/recovery UX; Track C security/failure validation; Software Engineering implementation evidence; Design Studio state communication evidence.

## Why this block exists

094 separated account recovery, device recovery and cryptographic key lifecycles. The next boundary is what encryption-at-rest can and cannot protect once trusted-origin JavaScript is executing while local data is usable.

Durable guards:

`encrypted at rest ≠ protected from authorized same-origin script while unlocked`.

`non-extractable key ≠ unusable by compromised authorized script`.

`same-origin isolation from other sites ≠ isolation from hostile code executing as this origin`.

`CSP/Trusted Types reduce injection risk ≠ origin compromise becomes harmless`.

This study does not choose a LogMate/MintTap key hierarchy or JavaScript framework. It defines the security boundary an implementation must satisfy.

---

## 1. SOURCE — current standards/platform evidence

### 1.1 XSS executes with the target origin's authority

MDN's current XSS guidance states that successful XSS subverts the intended same-origin isolation by causing attacker-controlled code to execute in the target site's own context; such code can access/modify page and local-storage content and make credentialed HTTP requests available to that origin.

Source: https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS

The same-origin policy isolates different origins, including origin-scoped browser storage such as IndexedDB, but that boundary does not distinguish trusted application code from injected hostile code after both execute as the same origin.

Source: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy

**SYNTHESIS:** origin isolation is valuable against other origins; it is not an intra-origin privilege boundary between legitimate and injected JavaScript.

### 1.2 Web Crypto deliberately does not promise secure key-storage architecture

Web Cryptography Level 2 states that CryptoKey storage is scoped to the execution environment/origin and explicitly warns that the specification places no normative requirement on underlying key-material storage or zeroization. More importantly for this block, it warns that script injection can abuse key sharing/cryptographic capability; raw key non-extractability is not equivalent to preventing authorized script from invoking allowed cryptographic operations.

Source: https://www.w3.org/TR/WebCryptoAPI/#security-considerations

**SYNTHESIS:** if application JavaScript is legitimately able to decrypt a record for the user, hostile JavaScript executing with equivalent origin/application authority may be able to ask the same key object or application decrypt path to perform useful operations even when raw key export is prohibited.

### 1.3 CSP is defense in depth, not a substitute for safe data handling

MDN's current CSP guidance describes CSP as a mechanism that can constrain script/resource execution and recommends sanitization as well; it explicitly treats CSP as defense in depth rather than a replacement for input sanitization.

Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP

OWASP's XSS Prevention Cheat Sheet likewise treats framework protections, contextual output encoding and sanitization as primary controls and CSP as an additional layer.

Source: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

**SYNTHESIS:** a strong CSP reduces exploitability and blast radius, but a policy that permits the compromised first-party application code needed to run the product cannot make arbitrary trusted-origin code safe by definition.

### 1.4 Trusted Types narrows DOM injection sinks, but policy correctness still matters

MDN documents `require-trusted-types-for 'script'` as enforcing typed values at DOM XSS injection sinks and `trusted-types` as restricting policy creation. MDN also notes Trusted Types became Baseline 2026 across latest browser/device versions, while older environments may not support it.

Sources:
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/trusted-types

WebKit documents Trusted Types support in Safari 26.0.

Source: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/

**CHANGE WATCH:** target managed-iPad OS/Safari version and exact enforcement must be verified. Baseline/latest-browser evidence cannot certify an older or policy-constrained EFB.

**SYNTHESIS:** Trusted Types can materially shrink DOM-XSS sink exposure, but an unsafe Trusted Types policy can still bless unsafe content; Trusted Types also does not establish build/deployment provenance or protect against already-authorized malicious first-party code.

### 1.5 Service Worker expands persistence/control consequences of origin compromise

The Service Workers specification requires secure contexts, applies CSP delivered with the worker script to that worker, and treats the origin—not a URL path—as the relevant security boundary. Service Workers persist independently of a single document and can mediate requests in their controlled scope.

Source: https://www.w3.org/TR/service-workers/

**TRANSFER from 092:** a compromised deployment/origin that installs or updates a malicious worker may persist privileged behavior beyond the initially compromised page. `origin repaired ≠ installed fleet clean` remains the correct operational guard.

---

## 2. Threat-model separation

Encryption-at-rest must be evaluated against a named attacker/state. At minimum distinguish:

1. **storage-only attacker:** obtains ciphertext/storage bytes but cannot execute as the application origin and lacks usable unwrap/decrypt authority;
2. **lost-device user without local unlock:** possesses device but cannot satisfy intended local gate;
3. **cross-origin web attacker:** controls another origin but not target-origin execution;
4. **XSS/DOM injection attacker:** gains code execution in an active target-origin document;
5. **malicious/compromised first-party dependency:** authorized code shipped inside the origin/application;
6. **compromised Service Worker/update channel:** privileged origin code persists/intercepts within scope;
7. **browser/OS/device compromise:** below the ordinary web-origin boundary.

A design may materially improve classes 1–3 while doing little against 4–6 once decryption authority is available to ordinary application script. Do not advertise class-1 protection as class-4 protection.

---

## 3. The key distinction: key extraction vs key use

Consider a non-extractable DEK represented by a `CryptoKey`.

Raw export may fail, yet the application still needs some operation such as:

`ciphertext → decrypt(DEK, ciphertext) → plaintext record → render/use`.

If hostile same-origin script can reach the CryptoKey, the decrypt wrapper, decrypted state, DOM, application store, message channel or export/sync path, it may not need raw key bytes at all.

Therefore:

`raw key theft blocked ≠ plaintext disclosure blocked ≠ fraudulent cryptographic operation blocked`.

The security review must trace **capability use**, not only key extraction.

### Required questions

- Where does the usable key reference exist, and for how long?
- Which code paths can invoke decrypt/encrypt/sign/unwrap?
- Where does plaintext live after decryption: JS object, framework store, DOM, worker message, export buffer?
- Can third-party code execute while those capabilities exist?
- Can a Service Worker or compromised dependency alter code/resources before local unlock?
- Can decrypted records or recovery material be exfiltrated through allowed network destinations?
- Does logout/lock actually end application access, or only change visible UI?

---

## 4. Key-use lifetime and plaintext lifetime

Minimizing lifetime is useful but must not be oversold.

Possible conceptual states:

`locked → unlock ceremony → key/unwrap capability available → record decrypted for task → task complete → plaintext/reference release → relock`.

A shorter usable-key/plaintext window can reduce exposure duration to opportunistic compromise. It does **not** prove zeroization, prevent compromise during the window, or protect against hostile code that is already running before unlock and simply waits for the capability to appear.

Web Crypto provides no normative guarantee that underlying key material is zeroized when references disappear. Consequently:

`reference dropped ≠ key material proven zeroized`.

`UI says locked ≠ cryptographic capability proven unavailable`.

Exact browser/device behavior is implementation evidence.

---

## 5. Defense layers and their real boundaries

### 5.1 Prevent hostile code from entering/executing

Controls include contextual encoding, sanitization, avoiding dangerous DOM APIs, framework-safe rendering, strict CSP, dependency governance and release provenance.

**Owner boundary:** Software Engineering owns concrete framework/code implementation; Web Manager owns the web trust requirements and validation contract.

### 5.2 Reduce DOM-XSS sink surface

Trusted Types enforcement can force sensitive DOM sinks through reviewed policies. Policy allowlisting is preferable to allowing arbitrary policies.

**Failure mode:** a policy that simply returns attacker-controlled input as trusted content defeats the intended transformation boundary.

### 5.3 Constrain script/resource/network authority

A strict CSP can constrain script origins/nonces/hashes and outbound connection destinations (`connect-src`) and can make common exfiltration/execution paths harder.

**Boundary:** CSP is not a general data-loss-prevention system. Data may be leaked through any allowed channel or abused locally; an authorized malicious first-party script may already satisfy the policy.

### 5.4 Minimize third-party execution in sensitive contexts

Analytics, advertising, support widgets and tag managers should not automatically receive the same execution authority as a locally unlocked record workspace. Architectural separation may be more meaningful than trying to make every third party 'careful'.

**MINTTAP DIRECTION:** for an EFB/logbook-like PWA, do not assume advertising/analytics scripts belong in the same unlocked sensitive application execution context. Exact monetization/product requirements remain OPEN and Marketing-owned where applicable.

### 5.5 Separate reconstructible/public surfaces from sensitive application authority

Different origins can create a real browser security boundary where product architecture permits it. A path such as `/marketing` vs `/app` on the same origin is not an equivalent security boundary merely because URLs differ.

**Guard:** `different path ≠ different origin security boundary`.

Whether separate origins are operationally justified is an architecture decision requiring routing, auth, CSP, storage, service-worker scope and UX trade-off analysis.

---

## 6. Service Worker-specific compromise chain

A high-risk chain for an installed PWA is:

`release/dependency/origin compromise → malicious worker/script publication → client update/install → controlled navigation/resource path → wait for local unlock → abuse decrypt/plaintext/sync/export capability → persist until clean generation actually controls client`.

This connects 092 supply-chain integrity, 088 update recovery and 094 key lifecycle.

A repair must therefore prove at least:

1. production origin serves authorized clean artifacts;
2. compromised worker is no longer controlling the client;
3. cached malicious assets are not authoritative/active;
4. sensitive credentials/recovery material exposed during the incident are rotated/recovered as policy requires;
5. authoritative user records/outbox survive remediation;
6. exact client generation is reconciled and diagnostics establish recovery without destructive origin wipe by default.

---

## 7. Cross-track transfer

### Track A — Platform/Browser
Owns origin, storage, Web Crypto, CSP/Trusted Types and Service Worker mechanics. Current high-value CHANGE WATCH is exact Safari/WebKit support/enforcement on target EFB versions.

### Track B — UX/IA/Content
Must distinguish truthful states such as `locked`, `locally unlocked`, `reauthentication required`, `sync disabled`, `security recovery required`. It must not claim 'encrypted = safe' without a threat-model qualifier.

### Track C — Quality/Accessibility
Owns fault/security acceptance matrices. Security-state messaging must remain perceivable and operable under keyboard/AT/reflow conditions, but Design Studio retains reusable interaction/visual ownership.

### Track D — Search/Analytics
Public discovery pages do not require access to unlocked application records. Analytics/diagnostics must be privacy-minimized and must not turn CSP/network allowances into unnecessary sensitive-context exfiltration paths.

### Track E — Architecture/Security/Operations
Owns threat model, origin segmentation, CSP/Trusted Types requirements, worker/update trust, incident containment and key-use/recovery governance.

---

## 8. Exact-artifact validation contract

Generic theory is PASS; product security is not.

Required implementation/target-device tests should include:

1. stored XSS attempt at every rich-text/HTML-capable input surface;
2. DOM-XSS sink inventory plus Trusted Types enforcement/violation evidence where supported;
3. CSP Report-Only rollout followed by enforced policy and negative tests for inline/eval/unapproved script;
4. network exfiltration attempts against allowed/disallowed `connect-src` destinations;
5. compromised first-party dependency simulation in a controlled test build: can it read decrypted state or invoke decrypt/export/sync paths?
6. hostile script present before local unlock: does it gain useful capability after unlock?
7. hostile script introduced after unlock: what plaintext/key-use capability is reachable?
8. relock/logout: prove capability/data state changes, not only UI changes;
9. malicious-worker controlled fixture followed by clean-worker recovery without deleting authoritative records/outbox;
10. target Safari/Home Screen execution on exact managed iPad OS/WebKit/MDM policy;
11. independent engine comparison before cross-browser claims;
12. diagnostics confirm generation/policy state without logging plaintext, tokens, recovery secrets or keys.

**Software Engineering handoff:** implementation should expose deterministic security test seams where feasible rather than relying only on manual penetration attempts. Exact framework sink inventory, key ownership, worker code and storage design are implementation-owned.

---

## 9. Product-specific implications for EFB/LogMate-like PWA

### MINTTAP/LOGMATE DIRECTION

Until exact product evidence exists:

- treat local encryption primarily as protection whose value depends on the stated threat model, not as proof against XSS/origin compromise;
- keep irreplaceable authoritative records/outbox distinct from reconstructible cache during incident cleanup;
- avoid destructive `clear site data` remediation as the default security response;
- minimize sensitive-context third-party script authority;
- require clean-worker/control-generation evidence after origin/update compromise;
- do not promise immediate offline revocation or secure hardware-backed key storage from generic Web Crypto evidence;
- do not claim an exact cryptographic design before Software Engineering/security validation.

### OPEN

Actual product repository/framework, HTML/rendering sinks, CSP, Trusted Types, dependency graph, analytics/ads, worker implementation, auth/session design, key hierarchy, plaintext lifetime, local-unlock behavior, MDM restrictions and managed-iPad browser version remain unverified.

---

## 10. CHANGE WATCH

- Trusted Types is newly Baseline 2026 and Safari support arrived in Safari 26.0; exact target-fleet support must be tracked.
- Service Worker specification/browser behavior continues to evolve; worker CSP/update behavior remains platform-sensitive.
- Any future browser primitive that provides stronger device-bound/hardware-backed application key semantics must be evaluated separately; do not infer it from Web Crypto alone.

---

## 11. Gate assessment

**PASS (generic).** Web Manager can now distinguish storage encryption from runtime origin compromise, key extraction from key use, same-origin isolation from same-origin hostile execution, and CSP/Trusted Types prevention layers from post-compromise guarantees.

**PRODUCT VALIDATION OPEN.** No claim is made that MintTap/LogMate currently has XSS, lacks CSP, uses Web Crypto, encrypts local records, or exposes recovery keys. Those are unknown until exact implementation evidence exists.

## Next high-value question

Do not repeat generic XSS/CSP primers. First consume Software Engineering or product evidence if it becomes available. Otherwise the next adjacent PWA trust question is **sensitive-context origin/third-party isolation and capability minimization**: whether marketing/analytics/ads/support/public content should share origin, Service Worker scope and execution authority with an offline locally authoritative PWA, including CSP/connect-src, iframe/sandbox/storage/auth continuity and operational trade-offs.