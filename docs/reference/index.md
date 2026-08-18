# Reference

This page summarizes exact public contracts. Source files and `--help` output remain authoritative.

## Installation profiles

| Profile | Skill root |
| --- | --- |
| `codex-project` | `.agents/skills` |
| `claude-code-project` | `.claude/skills` |
| `agent-project --skills-root PATH` | Safe project-relative `PATH` |

Install locally with `python3 install.py PROFILE`. Verify with `python3 install.py verify PROFILE`. Named profiles reject `--skills-root`; the generic profile requires it.

## Installed inventory

Guided entry and diagnostics:

- `ai-sdlc-loop-flow`
- `ai-sdlc-loop-doctor`

Lifecycle skills:

- `ai-sdlc-loop-orchestrate`
- `ai-sdlc-loop-specify`
- `ai-sdlc-loop-implement`
- `ai-sdlc-loop-verify`
- `ai-sdlc-loop-commit`

Delivery-control skills:

- `ai-sdlc-loop-approvals-sandbox`
- `ai-sdlc-loop-branching`
- `ai-sdlc-loop-requirements-review`
- `ai-sdlc-loop-test-cases`
- `ai-sdlc-loop-qa`
- `ai-sdlc-loop-validation`
- `ai-sdlc-loop-code-review`
- `ai-sdlc-loop-security-testing`
- `ai-sdlc-loop-commit-prep`
- `ai-sdlc-loop-conventional-commit`
- `ai-sdlc-loop-release-readiness`

Internal runtime: `ai-sdlc-loop-shared-runtime`.

The generated [skill catalog](skills.md) derives names and descriptions from each `SKILL.md`. Exact commands are in [Command reference](commands.md); schemas and authority boundaries are in [Contracts](contracts.md).

## Runtime commands

The shared CLI exposes `specify`, `approve`, `implement-check`, `verify`, `commit`, `promote`, and `status`:

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py --help
```

## Durable formats

Loop-owned specifications, state, approvals, evidence, install records, review artifacts, release decisions, and promotion output use canonical TOON. JSON-named durable output is rejected.
