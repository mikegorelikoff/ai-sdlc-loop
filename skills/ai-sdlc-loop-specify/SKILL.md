---
name: ai-sdlc-loop-specify
description: Produce a bounded deterministic AI SDLC Loop specification and TOON state before any code mutation.
---

# AI SDLC Loop — Specify

For raw feature/task notes with an unresolved business approach, first use
`ai-sdlc-loop-requirements-discovery` to compare options and prepare questions.
Bring the owner's accepted direction into Specify.

Follow `steps/manifest.toon` in dependency order. Use the shared runtime command `specify`; never edit source during this skill.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-specify
--phase <entrypoint>` with each completed ID as `--completed-step <id>`.
Read only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; owning stage receipts
still gate actions. Use only entrypoints declared in `steps/manifest.toon`.

## Chat Output Contract

Primary: Requirement ID / Bounded behavior / Allowed path / Acceptance / Evidence.
Rows represent individual requirement id records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Allowed scope / Status / Blocker / Evidence / Required action.
Clarification: Missing allowed scope / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.
