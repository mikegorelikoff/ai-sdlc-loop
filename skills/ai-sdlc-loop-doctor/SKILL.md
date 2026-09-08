---
name: ai-sdlc-loop-doctor
description: Diagnose an AI SDLC Loop installation and preview a safe package upgrade plan using deterministic, read-only TOON evidence.
---

# AI SDLC Loop Doctor

Use this skill when installation verification fails, installed skills drift, runtime requirements are uncertain, or a maintainer needs to compare an installed package with a candidate package before approving an upgrade.

## Contract

1. Diagnostics are read-only and emit `ai-sdlc-loop-doctor-report/v1`.
2. Check Python, Git, install record, profile, exact inventory, digests, step manifests, and shared runtime.
3. Every failed check includes remediation text but Doctor never executes it.
4. Upgrade planning compares current installed content with a local candidate package and emits `ai-sdlc-loop-upgrade-plan/v1`.
5. Doctor never installs, replaces, removes, or repairs files and never broadens host authority.

## Usage

```sh
python3 scripts/doctor.py check --project-root . --profile codex-project
python3 scripts/doctor.py upgrade-plan --project-root . --profile codex-project --package-root /path/to/ai-sdlc-loop
```

Resolve the active procedure through `steps/manifest.toon`. Durable machine output is TOON.

## Step selector

| Step | Procedure |
| --- | --- |
| `preflight` | [`steps/01-prepare.md`](steps/01-prepare.md) |
| `context` | [`steps/02-context.md`](steps/02-context.md) |
| `execute` | [`steps/03-diagnose.md`](steps/03-diagnose.md) |
| `validate` | [`steps/04-validate.md`](steps/04-validate.md) |
| `handoff` | [`steps/05-handoff.md`](steps/05-handoff.md) |

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `execute-procedure` | [`steps/03-diagnose.md`](steps/03-diagnose.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

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
