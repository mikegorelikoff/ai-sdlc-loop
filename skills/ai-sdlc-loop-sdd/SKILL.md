---
name: ai-sdlc-loop-sdd
description: Create and validate a bounded AI SDLC Loop implementation specification before code mutation. Use for a medium or large change that needs an explicit change contract, acceptance scenarios, allowed paths, and a fingerprint-bound implementation approval.
---

# AI SDLC Loop — Specification-Driven Development

`ai-sdlc-loop-sdd` is the Loop-native SDD entry point. It writes the same
bounded, fingerprinted TOON specification as `ai-sdlc-loop-specify`; the latter
remains available for existing callers. Use the namespaced SDD skill in Loop
installations so it is present in every supported project profile.

For raw feature notes with an unresolved business approach, use
`ai-sdlc-loop-requirements-discovery` first. Use
`ai-sdlc-loop-requirements-review` when actors, rules, acceptance logic, or
dependencies are incomplete. Follow `steps/manifest.toon` in dependency order;
this skill never authorizes source mutation.

## Deterministic step selection

Use the sibling shared runtime `scripts/loop.py steps --skill ai-sdlc-loop-sdd
--phase <entrypoint>` with each completed ID as `--completed-step <id>`. Read
only `selected_paths` and `required_references`. The selector validates
dependencies and returns `authorizes_execution: false`; the generated
fingerprint still requires explicit Implement approval.

## Deterministic Execution Contract

- D: use [the owning Python entry point](../ai-sdlc-loop-shared-runtime/scripts/loop.py) with explicit inputs; success covers only executed checks.
- S: interpret sources for the native artifact defined by this skill; cite unresolved decisions.
- H: validate native outputs before handoff. Runtime owns IDs, counts, routing and completion; confidence/chat grants no approval.
- Read explicit paths; reuse only current evidence. At most two repairs; then report BLOCKED with failed check, evidence and action.

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

