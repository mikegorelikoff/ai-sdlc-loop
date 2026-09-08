---
name: ai-sdlc-loop-flow
description: Guide a Loop request through read-only Explore and fingerprinted Apply, selecting exactly one owning skill without broadening approval or execution authority.
---

# AI SDLC Loop Flow

Use this skill when the contributor wants one readable entrypoint and should not need to guess which Loop skill owns the next action.

## Contract

1. Run Explore first. It is read-only and emits `ai-sdlc-loop-flow/v1` TOON.
2. Explain the selected stage, owning skill, evidence, blockers, and planned writes.
3. Apply must rebuild the route and reject fingerprint drift.
4. Apply selects exactly one owning skill. It never performs that skill's protected action.
5. Approval receipts, sandbox permissions, command execution, source mutation, and commit authority remain with their owning skills and host.

## Usage

```sh
python3 scripts/flow.py explore --root . --feature example --intent "fix the parser" --full-flow --format toon
python3 scripts/flow.py apply --root . --card decision.toon
```

Resolve the active procedure through `steps/manifest.toon`. Durable machine output is TOON.

## Step selector

| Step | Procedure |
| --- | --- |
| `clarify` | [`steps/01-clarify.md`](steps/01-clarify.md) |
| `route` | [`steps/02-route.md`](steps/02-route.md) |
| `execute` | [`steps/03-apply.md`](steps/03-apply.md) |
| `validate` | [`steps/04-validate.md`](steps/04-validate.md) |
| `handoff` | [`steps/05-handoff.md`](steps/05-handoff.md) |
| `complete` | [`steps/06-complete.md`](steps/06-complete.md) |

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `clarify` | `clarify`, `prepare` | none | `inspect-and-route` | [`steps/01-clarify.md`](steps/01-clarify.md) — `required` |
| `route` | `route` | `clarify` | `inspect-and-route` | [`steps/02-route.md`](steps/02-route.md) — `required` |
| `execute` | `execute` | `route` | `execute-procedure` | [`steps/03-apply.md`](steps/03-apply.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `on-demand` |
| `complete` | `complete` | `handoff` | `handoff-result` | [`steps/06-complete.md`](steps/06-complete.md) — `before-completion` |

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
