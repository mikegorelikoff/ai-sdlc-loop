---
name: ai-sdlc-loop-requirements-review
description: Review requirements for missing actors, workflows, business rules, acceptance logic, scope boundaries, and dependencies. Use before implementation when a request, story, PRD, or specification needs a testability and delivery-gap check.
---

# AI SDLC Loop — Requirements Review

Follow `steps/manifest.toon`. Report evidence-backed gaps without inventing product decisions. Persist durable reviews as TOON.

| Step | Purpose |
| --- | --- |
| [`scope`](steps/01-scope.md) | Bound sources and review authority. |
| [`context`](steps/02-context.md) | Select requirements evidence. |
| [`review`](steps/03-review.md) | Identify typed gaps and coverage. |
| [`validate`](steps/04-validate.md) | Check evidence and readiness logic. |
| [`handoff`](steps/05-handoff.md) | Return blockers and next owner. |

Use `scripts/requirements_review.py` for canonical `ai-sdlc-loop-requirements-review/v1` output and read `references/quality-bar.md` before signoff. Route accepted requirements to `ai-sdlc-loop-specify` and missing scenario design to `ai-sdlc-loop-test-cases`.
