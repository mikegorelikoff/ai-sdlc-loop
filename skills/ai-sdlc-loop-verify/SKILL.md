---
name: ai-sdlc-loop-verify
description: Require a current ready engineering quality report, execute explicit checks, persist redacted TOON evidence, compute readiness, and emit Harness-compatible TOON promotion artifacts.
---

# AI SDLC Loop — Verify

Follow `steps/manifest.toon`. Before executing checks, use
`ai-sdlc-loop-engineering-quality-gate` to verify the current report and fail
closed on missing, non-ready, invalid, or drifted evidence. Execute only stated
argv-safe commands through the shared runtime.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-verify
--phase <entrypoint>` with each completed ID as `--completed-step <id>`.
Read only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; owning stage receipts
still gate actions. Use only entrypoints declared in `steps/manifest.toon`.

## Chat Output Contract

Primary: Check / Expected / Actual / Status / Evidence; secondary: Artifact / Freshness / Evidence.
Rows represent individual check records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Current quality evidence / Status / Blocker / Evidence / Required action.
Clarification: Missing current quality evidence / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.
