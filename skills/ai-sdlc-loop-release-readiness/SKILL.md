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

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `identify` | `prepare` | none | `identify-candidate` | [`steps/01-identify.md`](steps/01-identify.md) — `required` |
| `context` | `clarify`, `route` | `identify` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `assess` | `execute` | `context` | `assess-release` | [`steps/03-assess.md`](steps/03-assess.md) — `on-demand` |
| `validate` | `validate` | `assess` | `validate-readiness` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `complete`, `handoff` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-loop-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc-loop/install/<profile>.toon` for `agent-project`.
