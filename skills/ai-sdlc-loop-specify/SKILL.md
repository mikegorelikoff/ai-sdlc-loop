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
