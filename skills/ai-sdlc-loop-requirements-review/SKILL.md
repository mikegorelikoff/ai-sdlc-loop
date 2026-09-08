---
name: ai-sdlc-loop-requirements-review
description: Review requirements for missing actors, workflows, business rules, acceptance logic, scope boundaries, and dependencies. Use before implementation when a request, story, PRD, or specification needs a testability and delivery-gap check.
---

# AI SDLC Loop — Requirements Review

Follow `steps/manifest.toon`. Report evidence-backed gaps without inventing product decisions. Persist durable reviews as TOON.

| Step | Purpose |
| --- | --- |
| [`scope`](steps/01-scope.md) | Bound sources and review authority. |
| [`context`](steps/02-context.md) | Select requirements evidence. |
| [`review`](steps/03-review.md) | Identify typed gaps and coverage. |
| [`validate`](steps/04-validate.md) | Check evidence and readiness logic. |
| [`handoff`](steps/05-handoff.md) | Return blockers and next owner. |

Use `scripts/requirements_review.py` for canonical `ai-sdlc-loop-requirements-review/v1` output and read `references/quality-bar.md` before signoff. Route accepted requirements to `ai-sdlc-loop-specify` and missing scenario design to `ai-sdlc-loop-test-cases`.

## Chat Output Contract

Primary: Requirement ID / Gap category / Severity / Impact / Evidence / Resolution.
Rows represent individual requirement id records. Show unresolved blockers before nonblocking findings; a completed review is not delivery approval.
Summary: Status / Decision / Evidence. Failure: Requirement package / Status / Blocker / Evidence / Required action.
Clarification: Missing requirement package / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
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
| `scope` | `prepare` | none | `bound-review` | [`steps/01-scope.md`](steps/01-scope.md) — `required` |
| `context` | `clarify`, `route` | `scope` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `review` | `execute` | `context` | `review-requirements` | [`steps/03-review.md`](steps/03-review.md) — `on-demand` |
| `validate` | `validate` | `review` | `validate-review` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `complete`, `handoff` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

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
