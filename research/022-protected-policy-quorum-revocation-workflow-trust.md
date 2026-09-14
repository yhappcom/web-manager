# 022 — Protected Policy Ownership, Reviewer Quorum, Revocation & Workflow Threat Model

Status: **PRACTICE / CONTROLLED POLICY + WORKFLOW TRUST VALIDATION COMPLETED**  
Research date: **2026-09-14**

## Question

Can MintTap harden the 021 release-provenance model so that policy changes themselves require authorized ownership, selected issue classes require multiple independent reviewers, revoked reviewers stop counting immediately, emergency override is explicit/time-bounded, and untrusted PR code cannot enter a privileged deployment path?

This study extends 021 into:

**protected policy → reviewer quorum/revocation → bounded break-glass → workflow trust boundary → CI allow/fail**.

All fixtures remain synthetic. No active production workflow is enabled by this study.

---

## RELATED DOMAIN CHECK

### Web Manager

021 already established source/tool/policy-bound release provenance, issue-class reviewer authorization, self-approval rejection and fail-closed CI. The next canonical queue item was policy ownership, reviewer quorum/revocation and workflow threat modeling.

### Design Studio

Latest Web Design status still has no substantive `W###`. These are governance semantics only.

**HANDOFF:** future release-review UI should clearly distinguish ordinary approval, quorum incomplete, revoked reviewer, emergency break-glass and workflow-security block without relying on color alone.

---

# SOURCE — GitHub code ownership and deployment review

GitHub CODEOWNERS can require review from code owners when branch protection is configured accordingly. This is useful for policy-file ownership, but CODEOWNERS alone is not equivalent to MintTap issue-class authorization or reviewer quorum.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

GitHub protected environments can require reviewers and optionally prevent self-review. GitHub documents that one required reviewer approval is sufficient for the environment job to proceed and that availability depends on repository visibility/plan.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

### SYNTHESIS

Repository/file ownership and release-issue authorization are different controls. MintTap should use platform ownership/review controls where supported, while keeping issue-class quorum and revocation explicit in the release governance model.

---

# SOURCE — untrusted workflow code

GitHub's secure-use guidance warns that `pull_request_target` and `workflow_run` become dangerous when privileged workflows check out or execute untrusted pull-request content. GitHub recommends avoiding that pattern and limiting tokens/secrets by least privilege.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

GitHub also creates a job-scoped `GITHUB_TOKEN`; its permissions should be minimized to what the workflow actually requires.

Primary source, checked 2026-09-14:
- https://docs.github.com/en/actions/concepts/security/github_token

### SYNTHESIS

The release gate is not trustworthy merely because its validator logic is correct. The workflow context that executes that validator must prevent untrusted PR code from gaining write/secrets/deployment authority or modifying the trusted gate before privileged execution.

---

# MINTTAP DECISION — protected policy ownership

The reviewer/waiver policy is itself security-sensitive control data.

Current PRACTICE rule:

```text
policy changed
+ no designated policy-owner approval
→ BLOCKED
```

A policy file must not be able to authorize its own change simply because the proposed content names a new owner. Production should bind ownership to a protected path/ruleset or equivalent trusted control outside the changed policy payload.

---

# MINTTAP DECISION — issue-class quorum

Each issue class may define its required number of independent reviewers.

Example:

```json
{
  "issue_rules": {
    "LEGAL_BLOCK": {"quorum": 2},
    "APPROVAL_STALE": {"quorum": 1}
  }
}
```

A reviewer counts only when:
- reviewer exists;
- reviewer is active;
- issue class is authorized for that reviewer;
- reviewer is not the release author;
- reviewer identity is unique within the quorum.

A revoked/inactive reviewer does not count toward quorum even if their historical approval is still present in the fixture.

---

# MINTTAP DECISION — revocation

Reviewer authorization is evaluated at current gate time, not only approval time.

Current PRACTICE rule:

```text
historical approval
+ reviewer now inactive/revoked
→ approval no longer satisfies current quorum
```

This makes revocation operationally effective. Production still needs a durable revocation timestamp/history model and policy for whether already-deployed historical releases remain valid records.

---

# MINTTAP DECISION — break-glass

Emergency override is a separate state, not an ordinary waiver.

A valid break-glass record currently requires:
- explicit `BREAK_GLASS` permission;
- active emergency actor;
- actor different from release author;
- issue class explicitly listed as break-glass eligible;
- approved status;
- non-empty reason;
- incident reference;
- explicit expiry that is not past.

When valid, the release is classified:

```text
PASS / WITH_BREAK_GLASS
```

not `PASS / CLEAN`.

Expired or unauthorized emergency approval fails closed.

---

# MINTTAP DECISION — workflow trust boundary

The controlled model identifies a privileged workflow when any of the following are available:
- write-capable repository token;
- secrets;
- deployment authority.

If a privileged `pull_request_target` or `workflow_run` path explicitly checks out untrusted code, the release path is blocked with:

`UNTRUSTED_CODE_IN_PRIVILEGED_WORKFLOW`.

A normal `pull_request` validation job may evaluate untrusted code only when kept read-only, without secrets and without deployment authority.

Self-hosted runners are separately treated as unsafe for untrusted code in the PRACTICE model because persistence can enlarge the blast radius.

---

# IMPLEMENTED PRACTICE

New artifacts:
- `tools/evaluate_policy_workflow_trust.py`
- `control/tests/policy_workflow_trust_cases.json`

The evaluator checks:
1. policy-owner approval for policy changes;
2. issue-class reviewer quorum;
3. reviewer active/revoked state;
4. release-author self-approval exclusion;
5. time-bounded break-glass authorization;
6. privileged workflow + untrusted checkout combination;
7. untrusted code on self-hosted runners;
8. final `PASS / BLOCKED` and CI `ALLOW / FAIL`.

---

# CONTROLLED VALIDATION

Result:

```text
10 / 10 expected outcomes matched
```

Validated cases:
1. policy change without designated owner approval → `BLOCKED`;
2. policy-owner-approved change → `PASS / CLEAN`;
3. two independent eligible reviewers satisfy quorum 2;
4. one reviewer against quorum 2 → `BLOCKED`;
5. revoked reviewer does not count toward quorum;
6. release author self-approval does not count;
7. valid time-bounded break-glass → `PASS / WITH_BREAK_GLASS`;
8. expired break-glass → `BLOCKED`;
9. privileged `pull_request_target` + untrusted checkout → `BLOCKED`;
10. ordinary untrusted `pull_request` with read-only/no-secret/no-deploy context → validation may proceed.

---

# PROFESSIONAL IMPLICATIONS

## 1. Control policy is part of the trust boundary

A reviewer registry or quorum table is not ordinary content. If an attacker can modify the policy and immediately use the modified policy, authorization becomes circular.

## 2. Quorum must be evaluated from current authority

Stored approvals are insufficient when reviewer authority has since been revoked.

## 3. Emergency access must remain visibly exceptional

`WITH_BREAK_GLASS` must be distinguishable from a clean release and later revalidated/audited.

## 4. CI security is workflow architecture, not only validator code

A correct gate executed after untrusted code receives privileged credentials can still be bypassed or exfiltrated.

## 5. Read-only PR validation and privileged deployment should be separate trust zones

Untrusted code can be tested without giving it deployment authority.

---

# PORTABLE WORKFLOW DIRECTION

Preferred future split:

```text
UNTRUSTED VALIDATION ZONE
pull_request
→ read-only token
→ no repository/environment secrets
→ no deployment credentials
→ test/build static evidence only

TRUSTED RELEASE ZONE
trusted base/default-branch source
→ protected gate logic/policy
→ provenance/reviewer/quorum checks
→ approved environment/OIDC when supported
→ deploy only after CI ALLOW
```

Do not activate `pull_request_target` merely to obtain secrets for PR code.

No active GitHub Actions workflow is added in 022 because repository enforcement capabilities and hosting/deployment provider remain unresolved.

---

# DESIGN STUDIO HANDOFF

Future release-review interfaces should expose:
- quorum requirement and remaining reviewer count;
- revoked/ineligible approvals;
- policy ownership failure;
- `PASS / WITH_BREAK_GLASS` as clearly exceptional;
- emergency expiry/incident reference;
- workflow-security block reason;
- separation between content/release problem and CI trust-boundary problem.

Long reviewer IDs, incident references and security explanations should be tested under Korean/English, narrow widths and enlarged text.

---

# OPEN / LIMITS

Still not production PASS:
- CODEOWNERS/branch protection/ruleset enforcement is not activated or verified end-to-end;
- current private-repository capability constraints remain relevant;
- reviewer identity is still synthetic rather than authenticated GitHub/SSO identity;
- revocation history and effective-time semantics are simplified;
- quorum policy schema is not finalized;
- break-glass actor authorization source is synthetic;
- no out-of-band emergency approval channel is defined;
- trusted workflow source pinning and reusable-workflow ownership are not implemented;
- GitHub Actions permission matrix is not yet encoded as policy;
- fork approval settings are not verified;
- self-hosted runners are not used/validated;
- no hosting provider/deployment credential trust relationship exists yet;
- no real MintTap release has passed this model.

## Highest-value next block

Implement **trust-boundary specification for the future active release workflow**, including exact trigger separation, token permission matrix, trusted workflow/policy ownership, fork behavior, artifact handoff, deployment credential boundary and rollback authority.

That block should end with a provider-neutral workflow contract ready to apply during the Firebase vs Cloudflare POC, without prematurely activating deployment automation.
