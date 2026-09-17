# 109 — PWA Recovery Corpus Longevity, Format-Spec Escrow & Future Converter Reconstruction

Status: **PASS (generic) / PRODUCT FORMAT-ESCROW + LONGEVITY-DRILL VALIDATION OPEN**  
Date: 2026-09-17  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 101–108 recovery/provenance/bridge chain; Track A representation/runtime mechanics; Track C preservation/regression evidence; Software Engineering implementation/toolchain evidence; Design Studio runtime/recovery-state evidence.

## Purpose

108 established that a recovery converter is security-critical infrastructure and that exact-artifact provenance, dependency state and historical semantic regression evidence must close on the same shipped converter. A longer-lived problem remains: a recovery promise may outlive the original parser library, package registry, build toolchain, browser generation, developer team or CI service.

The goal is therefore not to preserve an old executable forever. It is to preserve enough **non-secret representation knowledge and governed evidence** that a future team can reconstruct and validate a safe converter under a current toolchain without silently changing the historical data contract.

This is preservation architecture applied to an offline-first PWA recovery obligation. It is not a product backup-format specification and does not infer MintTap or LogMate production formats.

## 1. Track balance

- **A Platform/Browser:** supplies representation, encoding, file/import and runtime constraints. Browser APIs are not the durable format specification.
- **B UX/IA/Content:** consumes truthful states such as historical artifact recognized, current converter unavailable, reconstruction required, quarantine and recovered/reconciled.
- **C Quality:** owns fixture/oracle integrity, historical-generation coverage, reconstruction drills and semantic differential evidence.
- **D Discovery/Analytics:** usage telemetry can prioritize preservation effort but cannot prove dormant artifacts no longer exist.
- **E Architecture/Security/Operations:** highest-risk owner; owns preservation package boundaries, custody, authority procedure, longevity review and retirement/reconstruction governance.

E remains the bottleneck. The adjacent problem is no longer how to keep a vulnerable parser alive, but how to keep its *data contract intelligible* after its implementation disappears.

## 2. SOURCE — long-term accessibility depends on format sustainability, not file possession alone

The Library of Congress Sustainability of Digital Formats program evaluates formats using disclosure, adoption, transparency, self-documentation, external dependencies, patent impact and technical protection mechanisms. Its current 2025–2026 Recommended Formats Statement also evaluates institutional capability such as staff expertise, software/hardware/OS availability, workflows and access options.

Sources:
- https://www.loc.gov/preservation/digital/formats/index.html
- https://www.loc.gov/preservation/digital/formats/intro/format_eval_rel.shtml
- https://wwws.loc.gov/preservation/resources/rfs/introduction.html

**SYNTHESIS:** long-term recoverability is not a property of bytes alone. It depends on whether future maintainers can discover what those bytes mean, identify the applicable generation, reconstruct significant semantics and obtain tools/knowledge sufficient to interpret them.

Guards:
- `artifact retained ≠ artifact interpretable`;
- `format name retained ≠ format semantics retained`;
- `source code retained ≠ buildable converter retained`;
- `buildable converter retained ≠ trustworthy converter retained`.

## 3. Preserve the representation contract, not merely the implementation

The Library of Congress dataset guidance prefers platform-independent, character-based and publicly documented formats where they preserve full detail/precision. It specifically calls for applicable data dictionaries, schemas, technical specifications, software/version information, field references, checksums and permanent version specifiers, and recommends self-contained data where external services may disappear.

Source:
- https://wwws.loc.gov/preservation/resources/rfs/data.html

This is not a direct mandate for an application backup format; the Library's RFS is aimed primarily at published content. It is nevertheless strong **TRANSFER VALIDATION** for the preservation principle that interpretation knowledge and external dependencies are part of long-lived usability.

A product recovery-format escrow package should therefore preserve, where applicable and non-secret:
1. format identifier and generation/version-selection rule;
2. byte/container structure and character encoding;
3. field names, types, units, cardinality, null/missing semantics and defaults;
4. ordering and duplicate rules where semantically relevant;
5. identifier scope/stability rules;
6. date/time/time-zone and numeric precision/rounding rules;
7. normalization/canonicalization rules;
8. attachment/resource referencing rules;
9. integrity/authenticity envelope layout and algorithm identifiers;
10. compression/container semantics and bounded resource expectations;
11. schema/domain migration invariants;
12. unknown-field/forward-extension behavior;
13. historical defects/ambiguities and reviewed interpretation decisions;
14. current canonical normalized representation expected from each historical generation.

**MINTTAP DIRECTION:** preserve these as reviewable documentation/schema/fixtures rather than assuming future engineers can reverse-engineer the old application.

Guard: `old source repository available ≠ historical format contract documented`.

## 4. Significant properties must be explicit

PREMIS preservation metadata distinguishes objects, events, agents and rights and includes `significantProperties`; PREMIS 3 also expanded representation of software/hardware environments because correct interpretation can depend on a technical stack.

Source:
- https://www.loc.gov/standards/premis/version-3-0-dd-announcement.html

**TRANSFER VALIDATION:** a recovery escrow needs to say what must survive conversion, not merely whether parsing succeeded. For an application record this can include domain identifiers, timestamps, quantities, ordering/causality markers, tombstones, provenance fields, attachment bindings and other semantics that the product explicitly declares authoritative.

Exact significant properties are product/domain decisions and remain OPEN.

Guards:
- `all bytes converted ≠ all significant semantics preserved`;
- `schema-valid output ≠ domain-equivalent output`;
- `UI looks similar ≠ recovery semantics preserved`.

## 5. Corpus, oracle and specification are different evidence

A durable recovery contract needs at least three independent but cross-linked layers:

### Specification
Explains the grammar/representation and domain interpretation rules.

### Fixture corpus
Provides bounded examples for every promised historical generation, boundary condition and selected malformed/adversarial cases.

### Semantic oracle
Defines the expected current normalized meaning of each valid fixture and expected rejection/quarantine behavior of invalid/ambiguous fixtures.

No one layer substitutes for the others. A specification may omit an ambiguity; a fixture set may miss a legal production case; an oracle may accidentally encode a historical bug.

Guards:
- `specification complete on paper ≠ corpus coverage complete`;
- `corpus passes ≠ specification unambiguous`;
- `oracle exists ≠ oracle independent/correct`;
- `old parser output ≠ authoritative oracle`.

## 6. Corpus longevity needs its own provenance and fixity

RFC 8493 BagIt is an informational packaging format designed for reliable storage/transfer. It separates opaque payload from metadata tags and manifests, defines completeness and checksum validity, and explicitly says its integrity assurances are not protection against active attacks.

Source:
- https://www.rfc-editor.org/rfc/rfc8493.html

BagIt is not prescribed as the product escrow format. It supplies useful design evidence: preservation material can be packaged with a complete inventory and fixity manifests while leaving payload semantics to separate documentation.

A recovery-escrow evidence set should therefore bind:

`escrow-package generation × inventory × file digests × spec revision × fixture-corpus digest × oracle revision × significant-property definition × tool/dependency references × review/authority record`

and periodically verify fixity/readability.

Guards:
- `checksum valid ≠ artifact authentic`;
- `package complete ≠ semantics sufficient`;
- `BagIt-valid ≠ recovery-authorized`;
- `fixity PASS ≠ future converter correctness`.

## 7. Preserve dependency knowledge without making dependencies the only route

The Library of Congress explicitly treats external dependencies as a sustainability factor and considers software/hardware/OS availability in long-term preservation capability.

**SYNTHESIS:** an escrow should preserve dependency/toolchain knowledge sufficient to understand historical behavior, but the recovery contract should avoid requiring one obsolete dependency to remain executable forever.

Useful non-secret evidence includes:
- historical parser/converter package names and exact versions/digests where known;
- language/runtime/compiler/toolchain versions;
- lock/resolution files and SBOM/provenance references from 108;
- relevant standards/spec revisions;
- known implementation quirks and vulnerability history;
- build/test commands or reproducible build definition where available;
- environment assumptions that affected semantics;
- migration order and compatibility constraints.

This material supports diagnosis and reconstruction. It does **not** automatically authorize execution of an archived binary or vulnerable dependency.

Guards:
- `dependency archived ≠ dependency should be executed`;
- `container/VM image preserved ≠ future safe execution environment established`;
- `toolchain emulation possible ≠ clean reconstruction unnecessary`.

## 8. Secrets and live authority do not belong in format-spec escrow

A future converter may need to understand the *shape* and algorithm identifiers of encrypted/signed envelopes, but preservation of format semantics must not require storing production signing keys, live recovery secrets, session credentials or reusable device authority beside the corpus.

Separate:
- **representation knowledge** — what fields/envelopes mean;
- **test material** — synthetic keys/fixtures sufficient to exercise algorithms;
- **current authority procedure** — how legitimate recovery authority is established at reconstruction time;
- **production secrets** — governed by their own key/recovery lifecycle, not embedded in the format escrow.

Guards:
- `format reconstruction requires understanding cryptography ≠ escrow should contain production keys`;
- `historical signature fixture valid ≠ historical signer currently authorized`;
- `archived credential bytes exist ≠ credential authority should be restorable`.

## 9. Documentation itself can decay

Documentation can become unusable through dead links, proprietary notation, undocumented schemas, missing character encoding, inaccessible binary office formats or reliance on a departed maintainer's tacit knowledge.

**MINTTAP DIRECTION:** for the durable core, prefer self-contained, reviewable, broadly implementable representations: UTF-8 text/Markdown, machine-readable schemas where useful, small binary fixtures with explicit digests, data dictionaries and stable copies/references of the exact public standards relied upon where licensing permits. Record external canonical URLs but do not make a live URL the only copy of product-owned semantics.

This does not require flattening all information to plain text. Precision and completeness outrank aesthetic simplicity.

Guard: `documentation URL retained ≠ documentation retained`.

## 10. Format evolution must preserve a version graph

A list of format versions is insufficient when migrations skip generations or interpretation rules changed conditionally. Preserve a version/compatibility graph that answers:
- how an artifact generation is identified;
- which reader/converter generations understand it;
- direct-to-current vs sequential migration requirements;
- semantic changes and invariant changes at each edge;
- known lossy/ambiguous edges;
- when an old writer/API was retired but recovery remained supported;
- which current normalized representation and reconciliation policy applies.

The graph should distinguish *format generation* from app version, schema version, key/trust generation and sync protocol generation, consistent with 101/106.

Guard: `app version history ≠ recovery format history`.

## 11. Reconstruction drill — the escrow is not proven until old implementation is absent

The strongest generic validation is a periodic reconstruction exercise in which the candidate team does **not** rely on the original parser executable as the implementation under test.

A high-value drill:
1. select a promised historical generation;
2. provide only the governed escrow package plus currently approved development environment;
3. reconstruct a minimal bounded decoder/converter;
4. run historical-valid and adversarial fixtures;
5. compare against independent semantic oracles/significant properties;
6. migrate to current canonical representation;
7. exercise quarantine/reconciliation and no-credential-revival rules;
8. test interruption/resource bounds;
9. bind result to new artifact provenance/dependencies as required by 108;
10. record gaps that required undocumented tribal knowledge.

If reconstruction needs the original maintainer to explain an undocumented rule, the escrow has exposed a defect rather than passed.

Guards:
- `old converter still runs ≠ future reconstruction proven`;
- `documentation reviewed ≠ reconstruction drill passed`;
- `clean-room/current-toolchain converter built ≠ semantic recovery passed`.

## 12. Preservation refresh and change watch

The NDSA Levels of Digital Preservation are explicitly a framework for assessing and improving preservation programs; version 2.1 was released in March 2026, demonstrating that preservation practice itself evolves.

Sources:
- https://www.ndsa.org/publications/levels-of-digital-preservation/
- https://www.ndsa.org/2026/03/23/announcing-version-2_1-of-the-ndsa-levels-of-digital-preservation.html

**SYNTHESIS:** escrow is a maintained preservation object, not a one-time archive. Trigger review when:
- backup/recovery format changes;
- significant domain semantics change;
- schema/protocol/key/trust envelopes change;
- parser/dependency/toolchain is retired or vulnerable;
- supported browser/OS baseline materially changes;
- a reconstruction drill finds undocumented assumptions;
- custody/storage/fixity policy changes;
- a format generation approaches retirement.

**CHANGE WATCH:** preservation guidance, cryptographic algorithms, standards links, dependency availability and browser/toolchain support change over time.

## 13. Security and privacy boundary

A corpus designed for longevity can become a durable privacy leak if real user backups are copied into it. 108's default remains: synthetic/minimized fixtures first; sanitized incident reproduction only under explicit approval; real production data exceptional and separately governed.

The escrow inventory should not include production tokens, passphrases, DEKs/KEKs, live private keys, personal flight records or user-identifying filenames merely to make reconstruction convenient.

Guard: `more realistic corpus ≠ better-governed corpus`.

## 14. C — validation campaign

Exact-product validation should include at least:
1. every promised historical generation has an identifier and specification entry;
2. version-selection ambiguity is detected rather than guessed;
3. field types/units/null/default/ordering semantics are documented;
4. significant properties have product ownership and expected preservation rules;
5. every generation has synthetic valid fixtures and independent expected normalized output;
6. malformed/adversarial fixtures define reject/quarantine behavior;
7. corpus/spec/oracle files have inventory and digests;
8. inventory/fixity verification detects omission/corruption;
9. missing external documentation does not make product-owned semantics uninterpretable;
10. historical dependency/toolchain identities are recorded without requiring their execution;
11. production secrets are absent from escrow and synthetic cryptographic fixtures remain usable;
12. app-version history cannot be mistaken for format-generation history;
13. a current-toolchain reconstruction succeeds without original parser executable;
14. reconstructed converter passes 108 provenance/dependency admission;
15. reconstructed converter preserves independent semantic oracles/significant properties;
16. reconstruction does not revive historical credentials/trust/session authority;
17. mixed-epoch/outbox cases still enter 101 reconciliation rather than blind replay;
18. interruption/resource exhaustion preserves opaque artifact and live state;
19. escrow restore/readability is tested from an independent custody copy;
20. accessibility/recovery-state behavior remains separately validated on actual product UI/runtime.

## 15. Design Studio transfer

Canonical Design Studio `progress/WEB_STATUS.md` checked 2026-09-17: Web Design remains Stage 1 PASS / Stage 2 PASS / Stage 3 PRACTICE / NOT PASSED. W060 corrected real MintTap source assumptions, but W059 runtime execution remains blocked; no browser/Safari/screen-reader/physical-device PASS transfers.

**DEPENDENCY:** Web Manager supplies recovery states and semantic preservation requirements. Design Studio owns reusable interaction/render evidence for recognized-but-unavailable, quarantine, reconstruction-required and recovered states.

## 16. Software Engineering transfer

Canonical Software Engineering Studio `progress/STATUS.md` checked 2026-09-17: every specialist remains Foundation IN STUDY. Its architecture/data/quality evidence provides contract/invariant/recovery/test methods, but no exact product format or reconstruction proof.

**DEPENDENCY:** Software Engineering owns exact schema/parser/converter implementation, current-toolchain reconstruction and executable tests. Web Manager owns the PWA recovery-preservation contract, authority boundaries and evidence required to claim long-lived recoverability.

## 17. EFB/LogMate bounded application

A LogMate-like managed-iPad PWA can plausibly create a stronger longevity obligation than a disposable web cache because an old offline backup may contain irreplaceable flight records. Generic direction:

`preserve opaque user artifact + preserve non-secret representation contract + preserve synthetic historical corpus/oracle + preserve migration/reconciliation invariants + periodically reconstruct under current trusted tooling`.

Do not preserve a vulnerable executable or production secret merely because it once decoded the file.

Exact LogMate backup format, authoritative record fields, retention horizon, encryption/key architecture, iPad Files/MDM custody and legal/operational retention obligations remain OPEN.

MintTap production architecture was not inspected and no equivalent irreplaceable-data requirement is inferred.

## 18. Gate

**PASS (generic)** because this study establishes:
- why long-lived recovery requires representation knowledge beyond bytes/source code;
- a non-secret format-spec escrow content model;
- significant-property, specification, fixture and oracle separation;
- inventory/fixity packaging principles without confusing checksums with authenticity;
- dependency/toolchain knowledge preservation without perpetual executable authority;
- secret/authority separation;
- version/compatibility graph requirements;
- a future current-toolchain reconstruction drill;
- 20 exact-product validation cases and cross-repository ownership boundaries.

**OPEN:** exact product format generations, significant properties, schemas/data dictionaries, historical fixtures/oracles, escrow custody, retention horizon, cryptographic envelope, current build tooling, reconstruction drill, managed-iPad/browser/runtime evidence and product security/privacy approval.

## Next high-value boundary

**Recovery escrow custody, independence and organizational survivability:** a complete format/corpus escrow can still fail if it lives only in the same GitHub organization, cloud account, IAM/control plane or personnel trust domain as production. Study independent custody, access/recovery authority, integrity/authenticity over long retention, key/personnel turnover, repository/provider loss, disaster exercises and how to avoid turning escrow into a high-value secret/data aggregation target. Keep exact provider selection and enterprise policy OPEN until product evidence exists.
