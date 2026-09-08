---
name: ai-sdlc-loop-implement
description: Enforce the fingerprint-bound Implement approval, constrain source mutation to approved paths, and hand the bounded diff to the mandatory engineering quality gate.
---

# AI SDLC Loop — Implement

Follow `steps/manifest.toon`. This is the only Loop skill that authorizes the
requested source mutation, and only after a matching approval receipt. A
completed implementation is not ready for Verify until
`ai-sdlc-loop-engineering-quality-gate` produces a current ready report.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-implement
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

Primary: File / component / Change / Requirement ID / Verification / Evidence; secondary: Check / Status / Evidence.
Rows represent individual file / component records. Show the user decision before detail; preserve source order and explicit authority.
Summary: Status / Decision / Evidence. Failure: Implementation approval / Status / Blocker / Evidence / Required action.
Clarification: Missing implementation approval / Why required / Known evidence / Options. Next action: Owner / Next action / Expected evidence.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or question.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check; [shared limits](../ai-sdlc-loop-shared-runtime/references/chat-output.md) bound repair and preserve native outputs.
