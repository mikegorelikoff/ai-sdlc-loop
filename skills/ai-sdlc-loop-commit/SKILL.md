---
name: ai-sdlc-loop-commit
description: Require separate fingerprint-bound approval and create one traceable Git commit without implicit publication.
---

# AI SDLC Loop — Commit

Follow `steps/manifest.toon`. Implement approval never authorizes commit.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-commit
--phase <entrypoint>` with each completed ID as `--completed-step <id>`.
Read only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; owning stage receipts
still gate actions. Use only entrypoints declared in `steps/manifest.toon`.

## Deterministic Execution Contract

- D: use [the owning Python entry point](../ai-sdlc-loop-shared-runtime/scripts/loop.py) with explicit inputs; success covers only executed checks.
- S: interpret sources for the native artifact defined by this skill; cite unresolved decisions.
- H: validate native outputs before handoff. Runtime owns IDs, counts, routing and completion; confidence/chat grants no approval.
- Read explicit paths; reuse only current evidence. At most two repairs; then report BLOCKED with failed check, evidence and action.

## Chat Output Contract

Primary: Commit / Branch / Included scope / Approval / Evidence; secondary: Remaining path / Reason / Evidence.
Rows represent individual commit records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Commit approval / Status / Blocker / Evidence / Required action.
Clarification: Missing commit approval / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.
