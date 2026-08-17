---
name: ai-sdlc
description: Run a minimal approval-gated Specify, Implement, Verify workflow with deterministic local evidence and Harness-compatible promotion.
---

# AI SDLC Loop

Use this skill when a user asks to change code through AI SDLC Loop or requests the minimal Harness-compatible delivery flow.

## Contract

1. Identify the project root, a lowercase hyphenated feature name, the bounded request, and the smallest allowed path set.
2. Run `scripts/loop.py specify`. Show the resulting spec fingerprint to the user.
3. Before editing source, ask the user to approve or reject Implement for that exact fingerprint. Never record approval on the user's behalf.
4. After explicit approval, run `approve --action implement`, then `implement-check`. Only then edit files, and only below the allowed paths. Preserve unrelated work.
5. Run `verify` with explicit relevant commands. Report failures and do not imply readiness when any command fails.
6. If the user requests a commit, show the verified fingerprint and ask for a separate explicit commit approval. Never infer it from Implement approval.
7. After approval, record `approve --action commit` and run `commit`. Do not push, tag, publish, or open a pull request unless separately requested.
8. Use `promote` when Harness-compatible evidence is requested.

## Safety

- Treat `.ai-sdlc-loop/` as generated local workflow state, not source scope.
- Do not bypass a missing, rejected, stale, or mismatched receipt.
- Do not add extra commands to verification without stating them.
- Stop when changed paths escape the specification.
- Keep secrets out of requests, approval reviewer fields, commit messages, and artifacts.
