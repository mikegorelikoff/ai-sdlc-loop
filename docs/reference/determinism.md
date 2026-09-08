---
title: Deterministic execution
description: Product-specific execution boundaries, fixed inputs, serialization and reproducibility checks.
---

# Deterministic execution boundaries

Mechanical discovery, parsing, state validation and serialization belong to Python helpers. Semantic interpretation remains with the skill, using the evidence and native output named in its own execution contract. A successful helper is evidence of its implemented checks, not proof of semantic correctness or user approval.

The table maps each skill to its existing entry point. Other local helpers retain their existing contracts; this registry does not replace CLI help or install a new workflow engine. Source order remains semantic for histories; mappings and generated file collections use canonical ordering.

| Skill | Python entry point | Owned Python files |
| --- | --- | ---: |
| `ai-sdlc-loop-approvals-sandbox` | `skills/ai-sdlc-loop-approvals-sandbox/scripts/approval_plan.py` | 1 |
| `ai-sdlc-loop-branching` | `skills/ai-sdlc-loop-branching/scripts/branch_plan.py` | 1 |
| `ai-sdlc-loop-code-review` | `skills/ai-sdlc-loop-code-review/scripts/review_readiness.py` | 1 |
| `ai-sdlc-loop-commit-prep` | `skills/ai-sdlc-loop-commit-prep/scripts/check_commit_ready.py` | 1 |
| `ai-sdlc-loop-commit` | `skills/ai-sdlc-loop-shared-runtime/scripts/loop.py` | 1 |
| `ai-sdlc-loop-conventional-commit` | `skills/ai-sdlc-loop-conventional-commit/scripts/validate_commit_msg.py` | 1 |
| `ai-sdlc-loop-doctor` | `skills/ai-sdlc-loop-doctor/scripts/doctor.py` | 1 |
| `ai-sdlc-loop-engineering-quality-gate` | `skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py` | 1 |
| `ai-sdlc-loop-flow` | `skills/ai-sdlc-loop-flow/scripts/flow.py` | 1 |
| `ai-sdlc-loop-implement` | `skills/ai-sdlc-loop-shared-runtime/scripts/loop.py` | 1 |
| `ai-sdlc-loop-orchestrate` | `skills/ai-sdlc-loop-orchestrate/scripts/loop.py` | 1 |
| `ai-sdlc-loop-qa` | `skills/ai-sdlc-loop-qa/scripts/qa_plan.py` | 1 |
| `ai-sdlc-loop-release-readiness` | `skills/ai-sdlc-loop-release-readiness/scripts/release_readiness.py` | 1 |
| `ai-sdlc-loop-requirements-discovery` | `skills/ai-sdlc-loop-requirements-discovery/scripts/requirements_discovery.py` | 1 |
| `ai-sdlc-loop-requirements-review` | `skills/ai-sdlc-loop-requirements-review/scripts/requirements_review.py` | 1 |
| `ai-sdlc-loop-security-testing` | `skills/ai-sdlc-loop-security-testing/scripts/security_review_matrix.py` | 1 |
| `ai-sdlc-loop-shared-runtime` | `skills/ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_state_machine.py` | 35 |
| `ai-sdlc-loop-specify` | `skills/ai-sdlc-loop-shared-runtime/scripts/loop.py` | 1 |
| `ai-sdlc-loop-test-cases` | `skills/ai-sdlc-loop-test-cases/scripts/case_matrix.py` | 1 |
| `ai-sdlc-loop-validation` | `skills/ai-sdlc-loop-validation/scripts/run_validation.py` | 2 |
| `ai-sdlc-loop-verify` | `skills/ai-sdlc-loop-shared-runtime/scripts/loop.py` | 1 |

## Reproducibility and failure policy

State serialization rejects unknown fields, duplicate stage identities, invalid statuses and ambiguous mapping keys. Quoted values preserve commas, line breaks and control characters. The state API accepts an explicit `observed_on` date; default observation time remains a domain input. Equal-content atomic writes are safe no-ops; failed replacement preserves the previous artifact. Repeated identical assumptions are not duplicated.

Each skill bounds semantic repair to two attempts and preserves the owning runtime's stricter retry policy. Validation errors do not authorize a new route or overwrite valid evidence. Native formats remain native; presentation statuses never control lifecycle transitions.

The artifact writer includes its own decision journal reference on the first section write. Backbone and Loop refreshes use the shared OKF renderer, preserve original provenance on an unchanged write, and invalidate verification when the body changes. Context Guard keeps its native metadata format.
