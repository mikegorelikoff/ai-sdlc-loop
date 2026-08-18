---
name: ai-sdlc-loop-qa
description: Build risk-based QA plans with acceptance scenarios, regression targets, validation evidence, manual checks, and explicit signoff. Use for QA planning, smoke and regression scope, exploratory checks, acceptance validation, or release verification.
---

# AI SDLC Loop — QA

Follow `steps/manifest.toon`. Keep acceptance observable, distinguish executed evidence from planned checks, and persist durable QA plans as TOON.

| Step | Purpose |
| --- | --- |
| [`plan`](steps/01-plan.md) | Bound risks and acceptance scope. |
| [`context`](steps/02-context.md) | Select minimum sufficient evidence. |
| [`artifact`](steps/02-artifact.md) | Emit the canonical TOON QA plan. |
| [`evidence`](steps/04-evidence.md) | Validate coverage and evidence state. |
| [`signoff`](steps/03-signoff.md) | Return readiness and next ownership. |

Use `scripts/qa_plan.py` when a deterministic `ai-sdlc-loop-qa/v1` artifact is needed. Read `references/qa-plan.md` for scenario and signoff quality rules.

Route executable command selection to `ai-sdlc-loop-validation`, scenario-to-test design to `ai-sdlc-loop-test-cases`, security abuse coverage to `ai-sdlc-loop-security-testing`, and final readiness evidence back to `ai-sdlc-loop-verify`.
