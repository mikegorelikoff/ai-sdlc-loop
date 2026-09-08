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

## Chat Output Contract

Primary: Scenario ID / Actor / setup / Action / Expected result / Execution status / Evidence; secondary: Regression target / Risk / Execution status / Evidence.
Rows represent individual scenario id records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Acceptance outcome / Status / Blocker / Evidence / Required action.
Clarification: Missing acceptance outcome / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `plan` | `prepare` | none | `inspect-and-plan` | [`steps/01-plan.md`](steps/01-plan.md) — `required` |
| `context` | `clarify`, `route` | `plan` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `artifact` | `execute` | `context` | `emit-qa-plan` | [`steps/02-artifact.md`](steps/02-artifact.md) — `on-demand` |
| `evidence` | `validate` | `artifact` | `validate-evidence` | [`steps/04-evidence.md`](steps/04-evidence.md) — `before-completion` |
| `signoff` | `complete`, `handoff` | `evidence` | `handoff-result` | [`steps/03-signoff.md`](steps/03-signoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc-loop/install/<profile>.toon` for `agent-project`.
