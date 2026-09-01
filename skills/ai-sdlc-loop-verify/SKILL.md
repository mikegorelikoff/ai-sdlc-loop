---
name: ai-sdlc-loop-verify
description: Require a current ready engineering quality report, execute explicit checks, persist redacted TOON evidence, compute readiness, and emit Harness-compatible TOON promotion artifacts.
---

# AI SDLC Loop — Verify

Follow `steps/manifest.toon`. Before executing checks, use
`ai-sdlc-loop-engineering-quality-gate` to verify the current report and fail
closed on missing, non-ready, invalid, or drifted evidence. Execute only stated
argv-safe commands through the shared runtime.
