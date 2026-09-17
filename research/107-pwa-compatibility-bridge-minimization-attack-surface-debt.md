# 107 — PWA Compatibility-Bridge Minimization, Parser Isolation & Attack-Surface Debt

Status: **PASS (generic) / PRODUCT LEGACY FORMAT + TARGET-RUNTIME VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 101–106 recovery/provenance/release/retirement chain; Track A browser/file/service-worker boundaries; Track B recovery-only UX; Track C adversarial parser/compatibility evidence; Track D bounded retirement evidence; Design Studio W057 runtime closure boundary; Software Engineering parser/data implementation evidence when available.

## Purpose

106 established that ordinary runtime support may end before a narrow recovery path. That creates a second-order risk: every retained legacy reader, migrator, parser, protocol adapter or recovery endpoint remains code and semantics that can be attacked. This study defines how to preserve old authoritative user data without preserving obsolete authority or an indefinitely expanding compatibility surface.

This is not a parser implementation guide and does not select MintTap/LogMate legacy formats, sandbox technology, endpoint topology, support horizon or numeric limits.

## 1. Track balance

- **A Platform/Browser:** supplies file-selection, origin, storage and worker execution boundaries; browser APIs do not turn hostile artifacts into trusted inputs.
- **B UX/IA/Content:** consumes truthful states: recovery-only, artifact unsupported, artifact quarantined, conversion required, records preserved, support required.
- **C Quality:** owns malformed/adversarial corpus, resource-bound tests, semantic migration oracles, accessibility of failure/recovery states and regression evidence.
- **D Discovery/Analytics:** bridge usage can inform retirement but absent long-offline users remain UNKNOWN; diagnostics must not leak artifact contents.
- **E Architecture/Security/Operations:** highest-risk owner. Owns bridge inventory, authority minimization, isolation, patchability, retirement and debt governance.

Allocation remains E-heavy because a bridge exists specifically at a trust/compatibility boundary and may process old attacker-controlled artifacts with old semantics.

## 2. SOURCE — externally supplied/restored data remains untrusted

OWASP MASWE-0050 explicitly includes backups, local files, document pickers and archives among externally originated/untrusted data and identifies unsafe deserialization, path traversal, XXE and parser vulnerabilities as consequences of weak validation. The OWASP File Upload Cheat Sheet similarly recommends defense in depth: allow only required types, distrust Content-Type, bound size, validate content, isolate storage/processing where possible, and keep processing libraries securely configured/current.

Sources:
- https://mas.owasp.org/MASWE/MASVS-CODE/MASWE-0050/
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

**SYNTHESIS:** a backup produced by an old version is historically legitimate data, but at import time it still crosses a current trust boundary. Provenance may raise confidence in origin; it does not prove the old parser path is memory-safe, resource-bounded, semantically current or authorized to mutate live state.

Guards:
- `legacy artifact historically legitimate ≠ artifact safe to parse with privileged current authority`;
- `artifact authenticated ≠ parser invulnerable`;
- `format recognized ≠ semantic migration safe`;
- `recovery compatibility retained ≠ legacy runtime authority retained`.

## 3. Bridge debt is security debt with a data-preservation purpose

A compatibility bridge may include:
1. legacy file/backup reader;
2. archive/decompression layer;
3. schema migrator;
4. old protocol decoder/translator;
5. recovery-only API endpoint;
6. old key/trust envelope decoder;
7. native/deep-link handoff compatibility;
8. stale outbox translator.

Each retained component adds dependencies, input grammars, authorization decisions, test combinations, observability needs and incident obligations. Its value is preventing data stranding; its cost is continuing attack surface.

**MINTTAP DIRECTION:** maintain a bridge register with: supported input generations, authority granted, parser/dependency owner, isolation boundary, resource limits, semantic output contract, test corpus, last-use evidence, known vulnerabilities, retirement condition and fallback recovery route.

Guard: `bridge still useful ≠ bridge should remain broad`.

## 4. Minimize capability, not recoverability

A recovery bridge should normally be narrower than the retired runtime:
- **read/convert rather than write old format**;
- **current-code initiated rather than old-client-controlled**;
- **candidate/quarantine output rather than direct live-state mutation**;
- **no restoration of old sessions/device credentials/trust authority**;
- **no automatic outbox replay before reconciliation**;
- **no arbitrary filesystem/path/network access derived from artifact fields**;
- **only the minimum format generations explicitly promised**.

This preserves 106's reader/writer asymmetry while reducing authority.

Guards:
- `can decode old record ≠ may execute old operation`;
- `can migrate old schema ≠ may revive old credential`;
- `can inspect artifact ≠ may publish to live state`;
- `recovery endpoint reachable ≠ unrestricted legacy API available`.

## 5. Parser isolation is a boundary, not a magic shield

OWASP's file guidance recommends sandboxing where available and emphasizes that no single validation technique is sufficient. Archives additionally require checks around paths, compression/expanded size and contents; OWASP WSTG documents archive traversal/symlink hazards.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files/

For a browser PWA, exact process-level sandbox control is largely UA-owned. Therefore product architecture must not claim a custom native-style sandbox unless runtime evidence proves one. Useful application-level containment still includes bounded input size/depth/count, staged parsing, no direct publication, strict schema/domain validation, no executable interpretation, and explicit failure/quarantine.

**CHANGE WATCH:** exact worker/process isolation behavior is browser implementation territory and must not be assumed identical across Chromium and Safari/WebKit.

Guard: `Web Worker used ≠ security sandbox proven`.

## 6. Prefer canonical current representation after conversion

Keeping many legacy semantics alive throughout the application multiplies attack and reasoning surface. A safer generic shape is:

`legacy artifact → bounded decoder → intermediate validated model → current domain validator/migrator → quarantine candidate → reconciliation → current canonical representation`

After successful conversion, ordinary application logic should consume the current representation, not branch indefinitely on legacy generations.

**SYNTHESIS:** compatibility belongs at the edge of recovery, not distributed through every business path.

Guards:
- `legacy field parsed ≠ legacy field meaning accepted`;
- `syntactic conversion complete ≠ domain invariants preserved`;
- `migration succeeded once ≠ bridge regression-safe`.

## 7. Vulnerable legacy parser retirement

If a retained parser becomes known unsafe, preserving it indefinitely to avoid data stranding is not acceptable. Generic response order:
1. disable exposure through ordinary runtime/remote interfaces;
2. preserve opaque original artifacts where policy permits;
3. determine whether a patched/current parser can read the format safely;
4. if not, develop a narrowly scoped replacement converter under Software Engineering/security review;
5. validate against benign historical corpus plus malformed/adversarial mutants;
6. convert into quarantine/current representation;
7. reconcile semantics before publication/replay;
8. remove the vulnerable parser from shipped/current authority when replacement evidence passes.

**CONTRADICTION resolved:** 106 says retain recovery compatibility; security says remove vulnerable code. The compatible answer is to retain the **recovery obligation/capability**, not necessarily the vulnerable implementation.

Guards:
- `legacy parser retired ≠ legacy artifact must be discarded`;
- `old implementation removed ≠ recovery contract necessarily ended`;
- `artifact preserved ≠ unsafe parser must remain installed`.

## 8. Recovery endpoint isolation

A server-side recovery endpoint, if a product uses one, should not become a permanent alternate API. Generic controls include current authentication/authorization, narrow operation set, explicit supported artifact generations, bounded payload/resource consumption, no old credential revival, idempotent/stable operation identity where mutation is unavoidable, quarantine before publication, and separate monitoring/rate controls.

This is a web-architecture requirement, not proof of a current MintTap/LogMate server design.

Guard: `recovery-only route exists ≠ attacker should gain legacy mutation semantics`.

## 9. Attack-surface debt enters release governance

105's release gate should treat bridge additions/extensions as explicit security debt. A release that creates a new format or migration boundary should answer:
- what previous bridge remains required after this release?
- does the new format allow an older bridge to contract?
- what parser/dependency versions are now security-critical?
- what oldest artifact corpus must remain in regression tests?
- what bridge can be removed after positive recovery/retirement proof?
- does the release increase privileged input grammars without a corresponding retirement plan?

**MINTTAP DIRECTION:** bridge debt should have an owner and retirement condition at creation. “Temporary compatibility” without a removal gate becomes indefinite attack surface.

Guards:
- `new migration path added ≠ old path can be forgotten`;
- `no recent bridge use ≠ safe to delete bridge`;
- `bridge tests pass ≠ dependency vulnerabilities absent`.

## 10. C — validation campaign

Exact-product evidence should include at least:
1. smallest/largest valid legacy artifacts;
2. truncated/corrupt input;
3. spoofed extension/MIME/magic bytes;
4. excessive nesting/count/expanded-size archive;
5. traversal and archive-symlink cases where applicable;
6. duplicate/conflicting identifiers;
7. semantically invalid but syntactically valid records;
8. old credential/session/trust material ignored or quarantined;
9. already-applied stale outbox operation not blindly replayed;
10. delete/tombstone ordering ambiguity;
11. parser timeout/resource exhaustion path preserves current state;
12. crash/interruption during conversion preserves original + live state;
13. unsupported generation fails closed without deleting artifact;
14. vulnerable parser disabled while replacement recovery route works;
15. recovery-only endpoint cannot perform ordinary legacy mutation;
16. current representation has no hidden legacy-mode branch after conversion;
17. regression mutant drops/changes a field and semantic oracle detects it;
18. keyboard/zoom/screen-reader recovery/error state;
19. Safari/WebKit managed-iPad exact file/import behavior;
20. exact artifact/build/parser/dependency identities recorded.

## 11. B — truthful recovery UX

User-visible states should distinguish `file selected`, `checking`, `recognized`, `unsupported`, `quarantined`, `converted`, `records recovered`, `pending operations need review`, and `sync/replay authorized`. Do not collapse them into “import successful.”

When a parser is retired for security, the user should not be instructed to install an unsafe old version merely to recover data unless a separately reviewed support procedure explicitly requires it.

## 12. D — evidence without surveillance

Useful bridge metrics can be aggregate format generation, result class, parser version and failure category. Do not collect record contents, filenames, keys/tokens or stable device identity merely to justify retirement. Long-offline non-reporting remains UNKNOWN.

Guard: `bridge usage telemetry low ≠ no stranded artifacts exist`.

## 13. Design Studio transfer

Canonical Design Studio `progress/WEB_STATUS.md` checked 2026-09-17: Stage 1 PASS, Stage 2 PASS, Stage 3 PRACTICE/NOT PASSED. W057 requires executable W053/W056 evidence and explicitly claims no runtime/cross-browser/Safari/screen-reader/physical-device PASS yet.

**DEPENDENCY:** Web Manager defines truthful recovery/security states; Design Studio owns reusable interaction/visual implementation evidence. No design runtime PASS is imported here.

## 14. EFB/LogMate bounded application

For a LogMate-like company iPad PWA, historical backup/import files may be irreplaceable evidence. The generic preference is therefore **preserve opaque artifact + narrow current-code recovery**, not **ship every old parser forever** and not **delete unsupported artifacts**.

Exact company-iPad Files/share behavior, browser process isolation, parser implementation, backup formats, MDM constraints and direct device synchronization remain OPEN.

MintTap production architecture was not inspected; do not assume it shares the EFB authoritative-local-data model.

## 15. Gate

**PASS (generic)** because this study establishes:
- why recovery compatibility creates attack-surface debt;
- the distinction between recovery obligation and legacy implementation retention;
- least-capability/read-convert-quarantine architecture;
- parser/input isolation principles and browser limits;
- vulnerable-parser replacement/retirement path;
- release-governance debt register and a 20-case validation campaign.

**OPEN:** exact legacy formats, parsers/dependencies, sandbox/process behavior, limits, server recovery endpoints, support horizons and managed-iPad runtime evidence.

## Next high-value boundary

**Recovery bridge provenance and dependency/supply-chain closure:** once a narrow bridge is security-critical, its parser libraries, converters, build artifacts and historical test corpus become part of the recovery trust chain. Determine what provenance/update/vulnerability evidence is needed before a bridge may remain enabled, and how to patch/replace it without invalidating old-artifact recoverability. Consume Software Engineering supply-chain evidence rather than duplicate general dependency-management theory.