---
name: ai-sdlc
description: Route the complete AI SDLC Loop across its Specify, Implement, Verify, and Commit skills with TOON evidence and explicit approval gates.
---

# AI SDLC Loop

Use this skill when a user asks to change code through AI SDLC Loop or requests the minimal Harness-compatible delivery flow. Resolve the next step through `steps/manifest.toon`; stage ownership remains with the named skill.

## Contract

1. Route specification work to `ai-sdlc-specify`.
2. Route authorized source changes to `ai-sdlc-implement`.
3. Route evidence collection and promotion to `ai-sdlc-verify`.
4. Route commit preparation and execution to `ai-sdlc-commit`.
5. Never perform a stage-owned action from this router when the owning skill or shared runtime is unavailable.

## Safety

- Treat `.ai-sdlc-loop/` as generated local workflow state, not source scope.
- Do not bypass a missing, rejected, stale, or mismatched receipt.
- Do not add extra commands to verification without stating them.
- Stop when changed paths escape the specification.
- Keep secrets out of requests, approval reviewer fields, commit messages, and artifacts.
