# MintTap Web Manager Research Index

This directory is the source-grounded learning and decision-support layer for the MintTap company website and `minttap.app` domain.

The purpose is not to accumulate generic web articles. Each study must improve a real MintTap decision, establish a reusable operating rule, expose an unresolved risk, or define a validation method.

## Evidence labels

- `SOURCE` — authoritative source explicitly establishes the fact or requirement.
- `SYNTHESIS` — conclusion derived from multiple sources or evidence.
- `MINTTAP DECISION` — project-specific operating/design choice.
- `OPEN` — unresolved question.
- `DEPENDENCY` — external information or specialist work needed.
- `VALIDATION` — practical proof needed before production confidence.
- `CHANGE WATCH` — policy/standard/platform detail requiring later re-checking.

## Completed studies

- `001-app-launch-website-foundations.md` — Apple/Google launch web requirements.
- `002-multi-app-information-architecture.md` — multi-app company/app/support/governance IA.
- `003-privacy-support-account-deletion-architecture.md` — per-app privacy/support/deletion and App Data Contract.
- `004-store-website-content-synchronization.md` — Product Truth, screenshot evidence and release synchronization.
- `005-domain-hosting-security-baseline.md` — HTTPS/TLS, machine files, headers, DNS, rollback and monitoring.
- `006-accessibility-production-baseline.md` — WCAG 2.2 AA internal production baseline.
- `007-localization-architecture.md` — Korean/English locale URLs, hreflang and localization controls.
- `008-seo-structured-data-crawlability.md` — canonical, robots, sitemap, schema and Search Console.
- `009-seo-independent-verification-social-preview.md` — indexability classes and Open Graph baseline.
- `010-company-app-marketing-content-model.md` — Claim Registry, evidence, screenshots and truthful marketing.
- `011-operational-release-change-watch-controls.md` — continuous release/change-watch operating loop.
- `012-implementation-provider-comparison-methodology.md` — static-first architecture and hosting-provider comparison.
- `013-jurisdiction-legal-compliance-trigger-map.md` — fact-driven Korea/U.S./EU legal trigger framework.
- `014-provider-poc-specification.md` — identical Firebase vs Cloudflare provider-neutral POC and assertion contract.
- `015-machine-readable-control-artifact-model.md` — canonical JSON truth records, JSON Schema, stable IDs, semantic fingerprints and dependency/invalidation model.
- `016-control-artifact-validation-specimen.md` — executable structural + semantic validation specimen; 5/5 expected outcomes.
- `017-release-chain-semantic-integrity.md` — release/store, privacy/data, locale, legal trigger and operational-surface validation; 12/12 expected outcomes.
- `018-semantic-fingerprint-dependency-impact.md` — semantic fingerprint comparison and dependency propagation; 5/5 expected outcomes.
- `019-typed-dependency-approval-freshness.md` — typed impact severity, cycle detection and fingerprint-bound approval freshness; 6/6 expected outcomes.
- `020-derived-release-manifest-gate-waivers.md` — derived `PASS / NEEDS_REVIEW / BLOCKED` gate plus scoped auditable waivers; 8/8 expected outcomes.
- `021-release-provenance-reviewer-authorization-ci.md` — source/tool/policy-bound release provenance, issue-class reviewer authorization, self-approval rejection and fail-closed CI semantics; 9/9 expected outcomes.

## Practice artifacts

Current synthetic validation corpus includes:
- `control/schemas/v1/record.schema.json`;
- synthetic canonical records under `control/records/`;
- `control/tests/cases.json`;
- `control/tests/impact_cases.json`;
- `control/tests/dependency_governance_cases.json`;
- `control/tests/release_gate_cases.json`;
- `control/tests/release_provenance_cases.json`;
- `tools/validate_control.py`;
- `tools/compute_impact.py`;
- `tools/validate_dependency_governance.py`;
- `tools/evaluate_release_gate.py`;
- `tools/evaluate_release_provenance.py`.

These are synthetic research fixtures, not actual MintTap product/legal/store facts.

## Current research queue

See root `STATUS.md` for the authoritative queue. Highest-value next work:

1. protected policy ownership + reviewer quorum/revocation + workflow threat model, including controls preventing untrusted PR code from altering the gate or obtaining deployment authority;
2. execute the Firebase Hosting vs Cloudflare Workers POC when provider accounts/domain authority are available;
3. real-browser Korean/English typography/localization/accessibility/search/social/marketing/legal transfer validation on that POC;
4. apply Legal Trigger Registry when MintTap entity/market/audience/data/transaction facts are available;
5. app-specific user/market evidence when actual product pages are assigned.

## Design Studio relationship

Reusable design expertise remains canonical in `yhappcom/design-studio`. MintTap-specific web decisions and production findings stay here first.

Relevant domains: Typography / Type Design, Color, Layout / Spatial & Interaction, Web Design.

Current transfer note: Web Design still has no substantive W### at latest check. Web Manager governance now distinguishes release decision, CI authorization, reviewer authorization, source/attestation freshness, clean pass, pass-with-waiver, needs-review and blocked states. These remain semantic/control states only; visual treatment is a Design Studio/Web Design responsibility and must not rely on color alone.

When MintTap implementation confirms, limits or contradicts reusable Design Studio evidence, record it here first and hand it back to the appropriate specialist when justified.
