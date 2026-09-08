---
name: ai-sdlc-loop-orchestrate
description: Route the complete AI SDLC Loop across Specify, Implement, Engineering Quality Gate, Verify, and Commit with deterministic TOON evidence and explicit approval gates.
---

# AI SDLC Loop

Use this skill when a user asks to change code through AI SDLC Loop or requests the minimal Harness-compatible delivery flow. Resolve the next step through `steps/manifest.toon`; stage ownership remains with the named skill.

## Contract

1. Route specification work to `ai-sdlc-loop-specify`.
2. Route authorized source changes to `ai-sdlc-loop-implement`.
3. Route every completed implementation to `ai-sdlc-loop-engineering-quality-gate`.
4. Route evidence collection and promotion to `ai-sdlc-loop-verify` only after a current ready quality report exists.
5. Route commit preparation and execution to `ai-sdlc-loop-commit`.
6. Never perform a stage-owned action from this router when the owning skill or shared runtime is unavailable.

## Safety

- Treat `.ai-sdlc-loop/` as generated local workflow state, not source scope.
- Do not bypass a missing, rejected, stale, or mismatched receipt.
- Do not add extra commands to verification without stating them.
- Do not bypass, synthesize, or reuse a stale engineering quality report.
- Stop when changed paths escape the specification.
- Keep secrets out of requests, approval reviewer fields, commit messages, and artifacts.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-orchestrate
--phase <entrypoint>` with each completed ID as `--completed-step <id>`.
Read only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; owning stage receipts
still gate actions. Use only entrypoints declared in `steps/manifest.toon`.

## Chat Output Contract

Primary: Stage / State / Owning skill / Gate / Evidence.
Rows represent individual stage records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Feature scope / Status / Blocker / Evidence / Required action.
Clarification: Missing feature scope / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.
