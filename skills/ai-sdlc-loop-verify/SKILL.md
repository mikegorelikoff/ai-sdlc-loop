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
