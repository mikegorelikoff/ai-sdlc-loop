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
