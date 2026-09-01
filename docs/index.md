# AI SDLC Loop

**Ship a bounded change through Specify → Implement → Engineering Quality Gate → Verify with explicit approval before code mutation and commit.**

AI SDLC Loop is the focused delivery member of the AI SDLC product family. It installs 19 working `ai-sdlc-loop-{slug}` skills and one shared runtime while keeping specifications, approvals, repository-grounded quality reports, QA plans, evidence, and release decisions in deterministic local TOON artifacts.

[Start with a project-scoped install](start-here.md){ .md-button .md-button--primary }
[Read the workflow model](how-it-works.md){ .md-button }

## Why use it?

- Keep implementation and commit authority behind separate explicit approvals.
- Bound source changes to declared repository paths.
- Require a current deterministic engineering quality report before Verify.
- Run verification through explicit argv-safe commands.
- Preserve redacted, deterministic evidence without runtime telemetry.
- Promote supported results into AI SDLC Harness workflows.

## Quick start

Install for a Codex project:

```sh
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-loop/v0.2.0/install.sh | sh -s -- codex-project
```

Verify in a separate step:

```sh
python3 .ai-sdlc-loop/install/install.py verify codex-project
```

The installer preserves unrelated skills and writes a TOON inventory below `.ai-sdlc-loop/install/`.
Immutable `v0.1.1` retains its 17-member inventory; the current unreleased
source uses the 20-member inventory documented on this site.

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

- [AI SDLC Harness](https://github.com/mikegorelikoff/ai-sdlc-harness) structures the broader delivery lifecycle.
- **AI SDLC Loop** provides the smaller approval-gated delivery cycle.
- [Context Guard](https://github.com/mikegorelikoff/ai-sdlc-context) controls avoidable context growth.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics) measures local adoption evidence.

The products are complementary and independently installed.
