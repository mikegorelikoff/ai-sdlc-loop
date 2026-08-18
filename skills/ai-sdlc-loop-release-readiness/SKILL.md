---
name: ai-sdlc-loop-release-readiness
description: Decide whether a release candidate is ready from exact commit identity, CI and validation gates, approvals, blockers, and residual risks. Use before tagging, publishing, deployment handoff, or release signoff.
---

# AI SDLC Loop — Release Readiness

Follow `steps/manifest.toon`. Never infer a passing gate and never tag or publish from this review skill. Persist durable reviews as TOON.

| Step | Purpose |
| --- | --- |
| [`identify`](steps/01-identify.md) | Pin release and commit identity. |
| [`context`](steps/02-context.md) | Select current evidence. |
| [`assess`](steps/03-assess.md) | Record gates, blockers, and risks. |
| [`validate`](steps/04-validate.md) | Enforce readiness invariants. |
| [`handoff`](steps/05-handoff.md) | Return release decision and owner. |

Use `scripts/release_readiness.py` for canonical `ai-sdlc-loop-release-readiness/v1` output and read `references/quality-bar.md` before signoff. Route missing checks to `ai-sdlc-loop-validation`, acceptance gaps to `ai-sdlc-loop-qa`, and an approved release commit to `ai-sdlc-loop-commit`.
