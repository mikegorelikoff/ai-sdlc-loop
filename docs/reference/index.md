# Reference

This page summarizes exact public contracts. Source files and `--help` output remain authoritative.

## Installation profiles

| Profile | Skill root |
| --- | --- |
| `codex-project` | `.agents/skills` |
| `claude-code-project` | `.claude/skills` |
| `agent-project --skills-root PATH` | Safe project-relative `PATH` |

Install locally with `python3 install.py PROFILE`. Verify with `python3 install.py verify PROFILE`. Named profiles reject `--skills-root`; the generic profile requires it.

## Current source inventory

The v0.3.0 source installs the 21 entries below. Immutable
`v0.1.1` retains its previous 17-member inventory.

Guided entry and diagnostics:

- `ai-sdlc-loop-flow`
- `ai-sdlc-loop-doctor`

Lifecycle skills:

- `ai-sdlc-loop-orchestrate`
- `ai-sdlc-loop-specify`
- `ai-sdlc-loop-implement`
- `ai-sdlc-loop-engineering-quality-gate`
- `ai-sdlc-loop-verify`
- `ai-sdlc-loop-commit`

Delivery-control skills:

- `ai-sdlc-loop-approvals-sandbox`
- `ai-sdlc-loop-branching`
- `ai-sdlc-loop-requirements-discovery`
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

The shared CLI exposes `specify`, `approve`, `implement-check`, `verify`,
`evidence-check`, `steps`, `commit`, `promote`, and `status`:

```sh
python3 .agents/skills/ai-sdlc-loop-shared-runtime/scripts/loop.py --help
```

## Engineering quality gate commands

The quality-gate helper exposes deterministic `context`, `finalize`, and
read-only `verify` actions:

```sh
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py context --help
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py finalize --help
python3 .agents/skills/ai-sdlc-loop-engineering-quality-gate/scripts/engineering_quality_gate.py verify --help
```

Run `context` against the current repository and feature, finalize one
repository-relative TOON draft against that context, then run `verify` on
`.ai-sdlc-loop/<feature>/quality-gate.toon` before entering Loop Verify. Exact
arguments and output invariants live in the installed skill's step documents
and schemas; these helper actions grant no source-mutation authority.

## Durable formats

Loop-owned specifications, state, approvals, engineering quality context and reports, evidence, install records, review artifacts, release decisions, and promotion output use canonical TOON. JSON-named durable output is rejected. The engineering report uses `ai-sdlc-engineering-quality-gate/v1`; Verify accepts only a current `PASS` or `PASS_WITH_FINDINGS` report whose `final_decision.ready_for_next_stage` is true.

- `ai-sdlc-loop-hierarchical-decomposition`: evidence-backed hierarchy and verified branch packets; see [decomposition](decomposition.md).
