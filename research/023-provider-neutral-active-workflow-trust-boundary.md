# 023 — Provider-Neutral Active Workflow Trust-Boundary Contract

Status: **PRACTICE / CONTROLLED WORKFLOW-CONTRACT VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Before Firebase Hosting vs Cloudflare Workers POC deployment automation is enabled, what provider-neutral workflow contract should prevent untrusted pull-request code, stale artifacts, over-privileged tokens or unsafe rollback from crossing into deployment authority?

This study extends 021–022 from release-governance decisions into an executable **workflow-zone contract**. It does not enable a live deployment workflow.

---

## RELATED DOMAIN CHECK

Latest Design Studio Web status still has no substantive `W###`. Layout/Interaction has advanced through `L005` and `I004` and continues to require state meaning that survives visual-channel loss and supports recovery/conflict semantics.

**HANDOFF:** future Web Design / Layout-Interaction work should treat validation, build, deploy, rollback, blocked, stale-artifact and credential-boundary states as semantic workflow states. Their presentation must not rely on color alone.

---

# SOURCE — GitHub Actions trust boundaries

GitHub's secure-use guidance states that privileged `pull_request_target` and `workflow_run` workflows can expose repository write access or secrets, and warns against checking out or executing untrusted pull-request content in those privileged contexts.

Primary sources checked 2026-09-14:
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

GitHub recommends least-privilege `GITHUB_TOKEN` permissions. Fork pull-request workflows normally receive reduced/read-only permissions and no secrets unless repository settings deliberately weaken those protections.

Primary sources:
- https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

GitHub workflow artifacts expose a SHA-256 digest on upload, and download performs digest validation. GitHub documents digest mismatch as a warning in the run UI/logs.

Primary source:
- https://docs.github.com/en/actions/tutorials/store-and-share-data

GitHub OIDC permits a job with `id-token: write` to request an OIDC JWT and exchange it for a short-lived cloud credential. GitHub explicitly recommends defining cloud-side trust conditions so untrusted repositories/workflows cannot obtain cloud access tokens.

Primary sources:
- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
- https://docs.github.com/en/actions/reference/security/oidc

### SYNTHESIS

The deployment trust boundary should not be expressed as one large workflow with shared privilege. The useful abstraction is four zones with different trust and authority:

1. untrusted PR validation;
2. trusted build/gate;
3. deployment;
4. rollback.

Artifact identity is part of authorization: a release gate that approves source but deploys a different artifact has broken provenance.

---

# MINTTAP DECISION — four workflow zones

## Zone 1 — PR_VALIDATE

Purpose: test proposed code/content.

Contract:
- trigger: `pull_request`;
- may execute untrusted PR code;
- `GITHUB_TOKEN`: `contents: read` only in the baseline specimen;
- no repository/provider secrets;
- no `id-token: write`;
- no deployment authority;
- workflow/policy definition must come from the protected governance source.

PR artifacts are **test evidence only** and cannot be promoted directly into deployment.

## Zone 2 — TRUSTED_BUILD

Purpose: build the deployable artifact from the protected, accepted source state.

Contract:
- source must be protected `main` or an explicitly trusted manual source;
- must not execute untrusted PR checkout content;
- no deployment credential;
- no provider secret/OIDC token;
- produced artifact must have a digest bound into the release manifest.

## Zone 3 — DEPLOY

Purpose: deploy only the artifact already authorized by the release gate.

Contract:
- release manifest `ci_state` must be `ALLOW`;
- workflow and policy source must be protected;
- artifact origin must be `TRUSTED_BUILD`;
- artifact digest must exactly match the approved manifest digest;
- digest mismatch is **fail-closed** even though GitHub's built-in artifact validation documents a mismatch as a warning;
- deployment authority exists only in this zone;
- preferred provider credential mode is short-lived OIDC when the selected provider supports and validates it;
- fallback may use a minimal environment-scoped provider secret, but only in the deploy job;
- privileged `pull_request_target` / `workflow_run` paths must not execute or trust artifacts from untrusted PR code.

## Zone 4 — ROLLBACK

Purpose: restore a known-good release, not create a new release under emergency pressure.

Contract:
- trusted manual trigger;
- explicit authorization and reason;
- deploy credential only in rollback job;
- select a **previously approved artifact digest**;
- do not rebuild current source as part of rollback.

This preserves the meaning of rollback: redeploy known-good bytes rather than generate unknown new bytes from a potentially changed toolchain/source state.

---

# MINTTAP DECISION — provider credential boundary

Two provider-neutral credential modes are recognized:

1. `OIDC_SHORT_LIVED` — preferred when supported and validated; only deploy/rollback job receives `id-token: write` and the provider trust policy must constrain which repository/workflow/environment may exchange the token.
2. `ENVIRONMENT_SCOPED_SECRET` — fallback when OIDC is unavailable or unsuitable; credential must be minimal and scoped to the deploy job/environment rather than PR/build zones.

Provider choice does not change the preceding trust model.

---

# MINTTAP DECISION — artifact handoff

A PR workflow artifact is not a deployable artifact merely because tests passed.

The canonical deployment object is:

**accepted source snapshot → trusted build → artifact digest → release manifest ALLOW → deploy exact digest**.

If a future implementation uses cross-workflow artifact transfer, provenance/origin and digest verification must be explicit. `workflow_run` must not be treated as inherently trusted because GitHub's own security guidance warns that artifacts received from other workflows may contain untrusted content.

---

# IMPLEMENTED PRACTICE

New artifacts:
- `tools/validate_active_workflow_contract.py`
- `control/tests/active_workflow_contract_cases.json`

Controlled validation result:

**12 / 12 expected outcomes matched.**

Validated cases:
1. valid four-zone contract passes;
2. PR validation cannot receive OIDC/write-level token permission;
3. PR validation cannot receive secrets;
4. trusted build cannot use untrusted PR source;
5. deploy artifact digest mismatch fails;
6. deploy rejects PR-validation artifact origin;
7. environment-scoped minimal secret is accepted as provider-neutral fallback;
8. privileged `pull_request_target` executing untrusted code fails;
9. privileged `workflow_run` consuming/executing an untrusted PR artifact fails;
10. rollback may not rebuild source;
11. rollback must select a previously approved artifact digest;
12. deploy workflow source must be protected.

### VALIDATION BOUNDARY

This proves the internal contract logic only. It does **not** prove actual GitHub branch protection, environment protection, OIDC provider trust, Firebase permissions or Cloudflare permissions are configured correctly.

---

# PRACTICAL POC CONSEQUENCE

The future Firebase vs Cloudflare POC should use the same four zones and the same artifact/authorization model. Provider comparison should then ask only how each provider implements the final credential/deploy/rollback edge, rather than allowing provider-specific tooling to redefine the security model.

This avoids a common architectural inversion: choosing a vendor action first and then inheriting its trust model accidentally.

---

# DESIGN STUDIO HANDOFF

Future operational UI/prototype work should expose:
- validation vs deploy distinction;
- artifact identity/digest mismatch;
- trusted build vs PR artifact origin;
- blocked credential boundary;
- rollback target and reason;
- known-good rollback vs new build;
- provider authentication mode where operator action is required.

States must be textual/structural/programmatic, not color-only.

---

# OPEN / LIMITS

Still not production PASS:
- actual `.github/workflows` implementation;
- exact GitHub branch protection / CODEOWNERS enforcement verification;
- environment-protection availability on the current private-plan combination;
- exact Firebase Hosting authentication/deploy/rollback implementation;
- exact Cloudflare Workers authentication/deploy/rollback implementation;
- observed OIDC claims and provider trust policy;
- GitHub artifact retention/immutability policy for long-term rollback;
- signed attestation where justified;
- concurrency / deployment serialization;
- provider-side rollback semantics and retention;
- immutable release-history storage;
- action/reusable-workflow SHA pinning in the eventual live workflow.

## Highest-value next block

**Firebase Hosting vs Cloudflare provider-edge POC contract mapping.** Without deploying yet, map each provider's current official authentication, preview/production deploy, rollback/version retention, headers/redirect/static-file behavior and provider-specific constraints onto the four-zone contract. Identify which assertions can be executed immediately and which require account/domain authority.
