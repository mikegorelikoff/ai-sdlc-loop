# AI SDLC Loop

**Ship a bounded change through Specify → Implement → Verify with explicit approval before code mutation and commit.**

AI SDLC Loop is the focused delivery member of the AI SDLC product family. It installs 16 working `ai-sdlc-loop-{slug}` skills and one shared runtime while keeping specifications, approvals, QA plans, evidence, and release decisions in deterministic local TOON artifacts.

[Start with a project-scoped install](start-here.md){ .md-button .md-button--primary }
[Read the workflow model](how-it-works.md){ .md-button }

## Why use it?

- Keep implementation and commit authority behind separate explicit approvals.
- Bound source changes to declared repository paths.
- Run verification through explicit argv-safe commands.
- Preserve redacted, deterministic evidence without runtime telemetry.
- Promote supported results into AI SDLC Harness workflows.

## Quick start

Install for a Codex project:

```sh
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.1.1/install.sh | sh -s -- codex-project
```

Verify in a separate step:

```sh
python3 .ai-sdlc-loop/install/install.py verify codex-project
```

The installer preserves unrelated skills and writes a TOON inventory below `.ai-sdlc-loop/install/`.

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

- [AI SDLC Harness](https://github.com/mikegorelikoff/ai-sdlc-harness) structures the broader delivery lifecycle.
- **AI SDLC Loop** provides the smaller approval-gated delivery cycle.
- [Context Guard](https://github.com/mikegorelikoff/ai-sdlc-context) controls avoidable context growth.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics) measures local adoption evidence.

The products are complementary and independently installed.
