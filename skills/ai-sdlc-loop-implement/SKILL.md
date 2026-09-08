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
